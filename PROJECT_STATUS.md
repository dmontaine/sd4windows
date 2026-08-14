# PROJECT STATUS

Living handoff document for the SD Windows port. This project moves between
sessions, machines and accounts; anything not written here is lost. Read this
file first. Read [HISTORY.md](HISTORY.md) only if you need the record of how
something came to be the way it is.

**Last updated:** 13 Aug 2026 · **describes the tree as of commit** `9753ef9`
(the most recent commit to change code or build)

---

## 0. Maintenance rules

These are binding. A stale status file is worse than none, because the next
session will act on it.

1. **Update this file in the same commit as the work it describes.** Not
   afterwards, not "at the end". If a commit changes what builds, what runs,
   what is decided, or what is next, it changes this file too.
2. **Never promote anything into Verified without evidence in that session.**
   "It compiles" is not "it runs". "It ran once" is not "it is tested". If you
   did not observe it yourself, it belongs in §4 Unverified, whatever a
   previous session claimed.
3. **Record corrections, do not quietly overwrite.** If something here turns
   out to be wrong, fix it *and* note the correction in HISTORY.md. A future
   session that reads only the corrected text cannot tell it was ever wrong,
   which is how the same wrong turn gets taken twice.
4. **Traps in §6 are the highest value part of this file.** Anything that cost
   more than about fifteen minutes to work out goes there, phrased as what
   happens and what to do.
5. **Roll over when this file exceeds ~2000 lines**, or when any section is
   mostly historical. Move the settled material to HISTORY.md, newest first,
   and leave behind only what a new session needs to act today. §1–§7 are
   permanent sections; keep them, shorten them.

   **Understand what the limit is for.** It exists to stop this file sprawling
   to the point where nobody reads it — a handoff document that has grown to
   several thousand lines has stopped being a handoff document. It is not a
   target to sit near, and it is never a reason to leave a finding out. If
   something is worth recording, record it and trim elsewhere; detail that also
   exists in HISTORY.md is the first thing to cut, since nothing is lost by it.

   Prune when a section has gone stale, not when a number is approached. The
   best moment is just after work lands: instructions that have been carried
   out become history, and shed easily.
6. **HISTORY.md is append-only.** Never delete or rewrite an entry. Correct it
   with a new entry that references the old one.
7. **State the date as an absolute date.** Never "today", "last week", "the
   previous session".
8. **Anything a user would notice goes in `sdb_ai/sd64/sdsys/changelog`**, in
   the same commit. That is the product changelog, it ships with the system,
   and the port had added nothing to it for its first several sessions while
   these two files carried everything. They are not a substitute: this file is
   the state of the work, HISTORY.md is why it was done, the changelog is what
   changed for someone using SD. New verbs, new or moved files, changed
   behaviour at login, new messages and new configuration all belong there;
   refactors, findings and traps do not.

Checklist before you end a session:

- [ ] §3 Current state matches what is actually in the tree
- [ ] §4 Verified / Unverified is honest, and nothing was promoted without evidence
- [ ] §6 Traps gained anything that cost you real time
- [ ] §7 Next steps reordered, with anything finished removed
- [ ] Anything user visible added to `sdb_ai/sd64/sdsys/changelog`
- [ ] Any correction to earlier claims noted in HISTORY.md
- [ ] Header date and commit above updated

---

## 1. Goal and scope

Convert ScarletDME/SD from Linux to Windows.

**This repository is Windows only.** Linux development continues in a separate
repository. Do not add `#ifdef` branches to keep Linux building; replace Linux
code outright. This was an explicit instruction and it is what makes the source
readable.

Two stages:

- **Stage 1 (current).** Build and run on the MSYS2 POSIX runtime. The runtime
  supplies `fork`, `termios` and the passwd database, so only what it genuinely
  lacks has to be rewritten. Produces a working baseline to test against.
- **Stage 2 (not started).** Move to native Win32 and drop the
  `msys-2.0.dll` dependency: `fork` → `CreateProcess`, `termios` → Console API,
  passwd/group → Windows authentication.

The client library is already at stage 2 — see §5.3.

## 2. Environment

MSYS2 lives at `C:\msys64`. It was installed but completely empty of tooling
when this work started; everything below was installed during the port.

| Component | Version | Used for |
|---|---|---|
| msys `gcc` | 15.2.0 | server and utilities (POSIX runtime) |
| msys `make` | 4.4.1 | all builds |
| ucrt64 `gcc` (`C:\msys64\ucrt64\bin\gcc.exe`) | 16.1.0 | client DLL (native Win32) |
| `python` + `python-devel` | 3.12.13 | `EMBED_PYTHON` |
| libsodium | 1.0.20 | encryption |

Installed with pacman: `gcc make pkgconf libxcrypt-devel libbsd python-devel
gettext-devel mingw-w64-ucrt-x86_64-gcc`.

`gettext-devel` is needed only because `python3-config --ldflags --embed`
emits `-lintl`; the runtime `libintl` package does not carry the link library.

**libsodium is not packaged for the MSYS2 runtime** — only for
mingw64/ucrt64/clang64, which are ABI incompatible with it. It is built from
source into `/usr/local`:

```sh
curl -fLO https://download.libsodium.org/libsodium/releases/libsodium-1.0.20-stable.tar.gz
tar xzf libsodium-1.0.20-stable.tar.gz && cd libsodium-stable
./configure --prefix=/usr/local --disable-dependency-tracking && make -j4 && make install
```

Rebuilding the machine means redoing that step, or `make` will fail to link.

### External reference trees

Neither is part of this repository, both will be absent on a fresh machine, and
nothing in the build depends on either.

**`C:\Users\dmont\Projects\gplsrc`** — original GPL ScarletDME C source. Value
is limited; Ladybridge stripped the Windows code thoroughly and only
`qmclient.c` holds any, which `gplsrc/sdclilib/` has since superseded. Still
useful for recovering text mangled by the `qm`→`sd` rename, which is how the
corrupted `#include` in `sdclient.c` was confirmed.

**`C:\Users\dmont\Projects\GPL.BP`** — original ScarletDME BASIC source, 212
files. **This one is genuinely valuable**, unlike the C tree. It retains real
Windows code that this repository's `sdsys/GPL.BP` had stripped: 21 files carry
Windows logic there against 6 here, and every file present in both lost all of
it. See §5.4.

### Relationship to sdb64

`sdb64` is the active project. This tree, `sdb_ai`, is an experimental variant
that has been through five major AI cleaning and validation cycles, which is
why the code reads more cleanly than its age suggests. Those cycles are also
capable of introducing new problems — see the `VALID_OS_PATH` trap in §6.

## 3. Current state

### Building

From `sdb_ai/sd64`, and only from there (see §6):

```sh
make sd
```

Produces in `sdb_ai/sd64/bin`:

| Artifact | Kind |
|---|---|
| `sd.exe` `sdconv.exe` `sdfix.exe` `sdidx.exe` `sdlnxd.exe` `sdtic.exe` | PE32+, MSYS2 runtime |
| `sdclilib.dll` + `libsdclilib.dll.a` | PE32+, native UCRT64 |

`make sdclilib` builds just the client. `terminfo/` (99 files) is generated by
the `terminfo` target and is not tracked.

### Runtime bring-up — in progress, this is where to resume

SD still does not start, but the environment now exists and the bootstrap is
part way through. **Everything below is on this machine only; none of it is in
the repository.**

Laid down already:

| Thing | State |
|---|---|
| `/etc/sd.conf` | written, `SDSYS=/usr/local/sdsys` (copy of `sd64/sd.conf`) |
| `/usr/local/sdsys` | populated from `sd64/sdsys`, plus `bin`, `terminfo`, `Makefile`, `gpl.src`, `terminfo.src` |
| `/home/sd/user_accounts`, `/home/sd/group_accounts` | created |
| `sdadmins` local group | created, `GITORLI\don` enrolled — **now unnecessary under §5.6**, pending §8 |
| `gcat` | `$BBPROC`, `$BCOMP`, `!PATHTKN` built by `gplbld/bbcmp.py` |
| `PCODE.OUT` | built by `gplbld/pcode_bld.py` |

The bootstrap sequence, taken from `installsdai.sh`. **The sequence recorded
here previously was wrong** — it omitted two steps, which is what made the
ordering look like a deadlock. Corrected, with the installer's line numbers:

```sh
python3 gplbld/bbcmp.py /usr/local/sdsys GPL.BP/BBPROC  GPL.BP.OUT/BBPROC   # done
python3 gplbld/bbcmp.py /usr/local/sdsys GPL.BP/BCOMP   GPL.BP.OUT/BCOMP    # done
python3 gplbld/bbcmp.py /usr/local/sdsys GPL.BP/PATHTKN GPL.BP.OUT/PATHTKN  # done
python3 gplbld/pcode_bld.py                                                 # done
touch <sysdir>/gcat/'$CPROC'            # installer line 468 - the missing step
sd -start                               # installer line 590 - before -i, done
sd -i                                   # installer line 604 - bootstrap pass 1
sd -internal SECOND.COMPILE
sd RUN GPL.BP WRITE_INSTALL_DICTS NO.PAGE
sd THIRD.COMPILE
sd -internal BASIC GPL.BP CPROC         # writes the real gcat/$CPROC
```

**The puzzle is solved, and it was never an ordering problem.** `sd -start`
runs *before* `sd -i`, and `config.c` is satisfied because the installer first
creates an **empty placeholder**:

```sh
# Fool sd's vm into thinking gcat is populated
sudo touch /usr/local/sdsys/gcat/\$CPROC
```

`read_config()` only does `access(path, 0)` on `<sysdir>/gcat/$CPROC`, so an
empty file passes. The real catalogue overwrites it at the last step. Note the
check is in the original Ladybridge source too (`gplsrc/config.c` in the
external reference tree), so it is not something the AI cleaning cycles
introduced. `is_bootstrap` is a red herring for this: it is set at `sd.c:321`
and never consulted by `bind_sysseg`.

**Runtime bring-up is complete. SD runs.** The whole bootstrap sequence above
was executed successfully on 13 Aug 2026 and the system answers commands:

```
sd -ASDSYS WHO          -> 7 SDSYS
sd -ASDSYS COUNT VOC    -> 431 record(s) counted
sd -ASDSYS SELECT VOC   -> 431 record(s) selected to list 0
```

What each step produced: `sd -i` compiled the nine bootstrap programs and
created `VOC` and the dictionaries; `SECOND.COMPILE` compiled **204 programs
with no errors** and catalogued them; `WRITE_INSTALL_DICTS` wrote the
dictionary entries; `THIRD.COMPILE` compiled the I-types; and
`BASIC GPL.BP CPROC` replaced the placeholder with a real 24 KB
`gcat/$CPROC`.

**Two things to know before rebuilding this environment.** The runtime tree
needs more than §3 used to list — `installsdai.sh` also copies `gplsrc`,
`gplobj` and `gplbld/FILES_DICTS` into `<sysdir>`, and `REVSTAMP` opens
`./gplsrc/revstamp.h` relative to the account directory, so `SECOND.COMPILE`
aborts without it. And a run that aborts part way leaves record locks behind,
so restart SD before retrying (§6).

**Known cosmetic failure.** Every catalogue write prints `Unable change
ownership of directory error <path> err: 1000`. That is `CATALOG` doing the
Linux `chown` to `sdsys:sdusers`, which has no Windows meaning. Non-fatal —
cataloguing succeeds — but it should go with the rest of the OS-account work
in §5.6.

### The machine as this session ended (13 Aug 2026)

None of this is in the repository; it is the state of this machine only.

| Thing | State |
|---|---|
| `/usr/local/sdsys` | fully bootstrapped, SD runs commands |
| SD server | started, `sdlnxd` running |
| Binary used | **`/usr/local/sdsys/bin/sd.exe`, the shipped build.** The probe is no longer needed |
| **SDSYS password** | **`hunter2`** — set during testing, change it |
| **SUE password** | **`correcthorse`** — scratch account, delete it |
| `$CRED` register | holds SDSYS and SUE |
| Scratch accounts | `JANE`, `SUE`, `KIM` still under `/home/sd/user_accounts`; `PAT` under `C:\ProgramData\SD\user_accounts`, all built by `BP/MKACC` |
| **PAT password** | **`batterystaple`** — scratch account, delete it |
| Grants recorded | `JANE` grants `SUE`; `SDSYS` grants `SUE`; `KIM` and `PAT` grant nobody, which is what makes them useful |
| `sd.conf` | `USRDIR`/`GRPDIR` point at `C:\ProgramData\SD\`; `SDSYS` is still `/usr/local/sdsys` |

**The probe build is obsolete on this machine.** The Windows token now carries
`sdadmins` — the re-logon the group needed has happened — so `IsAdmin()` is
satisfied and the shipped binary does everything the probe was built for. Left
in `/tmp/sd_probe.exe` if a machine without the group ever needs it.

**Scratch test programs left in `<sysdir>/BP`**, none of them in the
repository: `CREDTEST`, `CREDRT`, `SETPW`, `INTEST`, `VTEST` from the previous
session, and `MKACC`, `GRANT`, `WHOAMI`, `MKDICT` from this one. `SETPW` sets
the SDSYS password to `hunter2` in plain text and `MKACC` sets SUE's to
`correcthorse` — delete both, and all three scratch accounts, before this
machine is used for anything real. `WHOAMI` prints `@LOGNAME`, `@WHO` and
`@PATH` and `SYSTEM(1050)`, which is how a login or a `LOGTO` is watched from
either side; it is catalogued **globally**, so it runs from an account with no
`BP` file. `MKACC` skips an account already in ACCOUNTS rather than rewriting
it, so re-running it does not wipe the grant lists.

There is also a **non-administrator probe** at `/tmp/nonadmin/sd_nonadmin.exe`,
built per §6 with `SD_ADMIN_GROUP` naming a group nobody holds. It is the only
way to see this system as an ordinary user, since the token here carries
`sdadmins` and every session is otherwise an SD administrator. `/tmp` does not
survive a machine rebuild; the recipe in §6 does.

To pick up where this stopped: `sd -internal COUNT VOC` should report 432
records without prompting (administrator + internal path), and
`echo hunter2 | sd -ASDSYS WHO` should report `SDSYS` after a password prompt.
If the first fails, SD is not started: `bin/sd.exe -stop` then
`bin/sd.exe -start`, redirecting output to a file (§6).

**An earlier report of `sd -i` "blocking silently" was wrong**, and the cause
is worth knowing — see the stale record lock trap in §6. It was self-inflicted
by killing earlier runs.

**The `/etc/group` blocker behind that is gone**, since the `is_grp_member`
calls in `LOGIN` and `CPROC` were deleted rather than repaired (§5.6). It
survives only in `CREATEA` and `MODIFYA`, where it guards `OS.EXECUTE` calls to
`useradd` and friends and must go with them.

Note the environment above uses `/etc` and `/usr/local`, which §5.8 replaces
with `C:\ProgramData\SD\`. It was laid down before that decision; there is no
reason to redo it by hand, but the installer must not reproduce it.

## 4. Verified vs unverified

Keep this split honest. It is the single most useful thing in the file.

### Verified by observation

- All six binaries compile, link and run. `sd.exe` prints `SD has not been
  started`, which specifically exercises the new `sem_open` probe path.
- `sdtic.exe` compiled `terminfo.src` into 99 terminfo files — real work, not
  just a banner.
- Client DLL compiles with **zero warnings** under `-Wall -Wextra -Wpedantic`,
  both bundled test suites pass, and it exports 51 `SD*` symbols including
  `SDConnectLocal`.
- MSYS2 runtime behaviour, tested by compiling and running probes:
  `fork`/`waitpid`, `termios`, `getpwuid`, `shm_open`+`mmap`, `sem_open`,
  `mmap(MAP_SHARED|MAP_ANONYMOUS)` all work. `shmget` and `semget` **fail at
  runtime with ENOSYS**.
- `terminfo` regenerates byte identically with and without the `O_BINARY`
  correction, confirming that change is protective rather than a repair.
- The group-based `IsAdmin()` logic, against member, non-member, absent group
  and primary group. `getgrnam()` resolves Windows local groups on the MSYS2
  runtime and reports membership accurately. (Superseded as the identity model
  by §5.6, but the observation stands and `IsAdmin()` still gates `sd -start`.)
- **`IsAdmin()` in the linked binary.** `sd -start` refused with "Command
  requires administrator privileges" while the group was absent, and got past
  that check once built against a group the token holds. So `check_admin()`
  and `IsAdmin()` work in the real executable, in both directions.
- **The whole shared segment lifecycle**, exercised at 3 MB in the shape
  `sysseg.c` uses: create, size, map, attach from a second mapping, confirm the
  attach sees the right size and content, write through one mapping and read it
  through the other, create six semaphores, confirm one excludes while held and
  can be reacquired after posting, unmap, unlink, and confirm a later attach
  gives ENOENT. All as intended. This was the largest single unknown in the
  port; it has since been exercised by SD itself as well — see below.
- `gplbld/bbcmp.py` and `gplbld/pcode_bld.py` both run on Windows and produce
  `gcat` entries and `PCODE.OUT`.
- **SD has started.** `sd -start` (probe build, §6) created the shared segment
  and all six semaphores *itself* — `/dev/shm/sd_shm_716d0301` at 100 KB and
  `sd_sem_716d0302_0` through `_5` — and spawned `sdlnxd`, which stayed
  running. This is the `shm_open`/`ftruncate`/`mmap` **creation** path in
  `sysseg.c` executing for the first time; it had never run before, and it was
  the largest remaining unknown after the standalone lifecycle test. Observed
  13 Aug 2026.
- The `gcat/$CPROC` placeholder satisfies `read_config()`. An empty file is
  enough, as the check is only `access(path, 0)`.
- **Multi-process attach works.** A second process (`sd -i`) attached to the
  segment created by `sd -start`, was allocated a user table slot, and wrote to
  `<sysdir>/errlog` — "User 2 (pid 1931, don)", "User 5 (pid 2050, don)". This
  was listed as unverified until now.
- SD writes `<sysdir>/errlog` correctly, including on receipt of SIGTERM.
- **`sd -stop` works, including the new liveness poll.** It reported "SD (64
  Bit) has been shut down", and `/dev/shm` was left completely empty — the
  segment and all six semaphores unlinked. `sd -start` then brought the system
  up again from nothing. So the full start/stop/restart cycle runs, which
  closes the `stop_sd()` item that was listed as unverified.
- **Account passwords work end to end.** `!SD_GET_SALT` returns a fresh
  24-character salt per call and `!SD_KEY_FROM_PW` a reproducible 44-character
  Argon2 key that changes with either password or salt — libsodium works on
  Windows, and neither routine had a caller before. Round trip through
  `!CRED_SET` / `!CRED_VERIFY`: the right password verifies, the wrong one does
  not, account names are case insensitive, an unknown account and an empty
  password both fail closed, and re-setting the same password yields a new salt
  and verifier that still verifies. The stored record holds salt and key only,
  with no trace of the password.
- **Login authenticates.** `echo hunter2 | sd -ASDSYS WHO` reports `SDSYS`; a
  wrong password is refused three times and terminates the connection; and
  `sd -internal COUNT VOC` still returns 432 records through the administrator
  install path. Observed 13 Aug 2026.
- **The complete bootstrap runs, and SD answers commands.** Every step from
  `sd -start` through `BASIC GPL.BP CPROC` completed on 13 Aug 2026;
  `SECOND.COMPILE` alone compiled 204 programs with no errors. `WHO` reports
  `7 SDSYS`, `COUNT VOC` reports 431 records and `SELECT VOC` selects them. So
  the compiler chain (`BCOMP`, `@ds` path resolution, the pcode loader), DH
  file creation, and reading records back all work.
- **`@ds` is correct for stage 1.** 204 programs compiled with
  `dir.separator` hardcoded to `/`, which settles the open question in §6 for
  the MSYS2 runtime. It remains live for stage 2.
- **`K$ADMINISTRATOR` answers truthfully.** With `USR_ADMIN` seeded from
  `IsAdmin()`, the rewritten test in `BBPROC` granted access under the probe
  build (group `Users`, which the token holds). It had refused everybody before.
- **The six semaphores are not a bottleneck under normal running.** Sampled
  with a `sem_getvalue()` probe both at idle and while another process was
  waiting on a record lock: all six read 1 (free) throughout.
- **The shipped binary does everything the probe did.** Once the token carried
  `sdadmins`, `/usr/local/sdsys/bin/sd.exe` ran `-stop`, `-start`, `-internal`
  commands and a password login, all of which call `check_admin()` or
  `IsAdmin()`. The probe build is no longer needed on this machine. Observed
  13 Aug 2026.
- **LOGTO is gated by the grant list, in both directions.** Observed 13 Aug
  2026, logged in as SUE with SUE's own password:

  | Command | Result |
  |---|---|
  | `LOGTO JANE`, no grant | "User not allowed in requested account", stays in SUE |
  | `LOGTO JANE` after granting SUE on JANE | enters JANE |
  | `LOGTO SUE` (own account, no grant) | enters, as it must |
  | `LOGTO KIM`, an account that grants nobody | refused |
  | `LOGTO SDSYS`, no grant | refused |
  | `LOGTO SDSYS`, granted, wrong password ×3 | refused, stays in SUE, connection kept |
  | `LOGTO SDSYS`, granted, own password | enters SDSYS |
  | `LOGTO /home/sd/user_accounts/JANE` | refused — a path is not an account |
  | `LOGTO NOSUCHACCOUNT` | refused, wording identical to an ungranted account |

- **SDSYS reaches every account.** Logged in as SDSYS, `LOGTO JANE` and
  `LOGTO KIM` were both admitted although neither grants SDSYS. Stepping on
  from KIM to JANE was refused, because the exception belongs to the account
  you are standing in — recorded here because it is the one surprising edge of
  the rule.
- **The exception carries through a step-up.** Logged in as SUE, `LOGTO KIM`
  was refused; `LOGTO SDSYS` with SUE's own password was admitted; and
  `LOGTO KIM` from there was admitted, reporting `LOGNAME=SUE WHO=KIM`. So a
  person reaches an ungranted account only through administration, and the
  session still names them throughout.

- **`@logname` survives `LOGTO`.** `WHOAMI` reported `LOGNAME=SUE WHO=SUE`
  before, `LOGNAME=SUE WHO=JANE` after `LOGTO JANE`, and `LOGNAME=SUE
  WHO=SDSYS` after stepping up into SDSYS. The login identity persists into
  administration, which is what makes the audit trail worth writing.
- **The step-up asks for the caller's own password, and only that.** SUE
  entered SDSYS with `correcthorse`, SUE's password; SDSYS's own password
  (`hunter2`) is not what is asked for and would not have worked.
- **The install path still bypasses everything.** `sd -internal` entered SDSYS
  with no password, moved to JANE with no grant and back with no step-up, and
  `COUNT VOC` still reports 432 records. The bootstrap is unaffected by any of
  this; re-observed after the pathname removal.
- **Drive-letter paths work, after the `sdrealpath()` fix (§5.8).** A probe
  opened the same file through `C:\ProgramData\SD\user_accounts\PAT\VOC`,
  `C:/...`, `/c/...`, a lower-case drive letter and a mixed
  `C:\ProgramData/SD/...`. Before the fix every drive-letter form failed with
  ER_FNF and only `/c/...` worked. The MSYS2 runtime was never the problem —
  a C probe confirmed `stat()` accepts all of them.
- **Accounts under `C:\ProgramData\SD` work end to end.** `sd -APAT` run from
  `C:\Windows`, with `USRDIR=C:\ProgramData\SD\user_accounts` in `sd.conf`,
  prompted for PAT's password and landed in the account directory. The full
  bootstrap still answers (`COUNT VOC` reports 432) and the whole LOGTO suite
  above still passes against the rebuilt binary — worth stating, because
  `sdrealpath()` is on the path of every file open in the system.
- **SD does not need the MSYS2 *shell*, only its DLLs.** `sd.exe` run straight
  from a PowerShell prompt, with `C:\msys64\usr\bin` and
  `C:\msys64\usr\local\bin` on PATH, answered `COUNT VOC` with 432 records.
  POSIX paths still resolve — `/usr/local/sdsys`, `/etc/sd.conf` — because the
  translation is done by `msys-2.0.dll`, not by bash. So the shell dependency
  is already gone; what remains is the runtime dependency, which is stage 2.
- **SD no longer needs an operating system group to use.** Observed with a
  probe whose `SD_ADMIN_GROUP` names a group nobody holds (§6), which is the
  only way to be a non-administrator on this machine. `sd -ASUE` prompted for
  the account name's password and entered SUE with `SYSTEM(1050)` reporting
  **0** — not an administrator, and nothing about the Windows account
  mattered. That is the whole point of §5.6, and it had never been shown from
  the outside.
- **The SDSYS password alone makes you an SD administrator.** The same
  non-administrator probe ran `sd -ASDSYS`, was prompted, gave `hunter2`, and
  arrived with `SYSTEM(1050)` reporting **1**. `LOGIN` sets the flag on entry
  to SDSYS, so administration is now genuinely a matter of knowing the SDSYS
  password rather than of Windows group membership.
- **Administrator rights follow you out of SDSYS.** In that same session,
  `LOGTO KIM` left `SYSTEM(1050)` at 1 while standing in KIM. Nothing clears
  the flag on the way out — see §7 item 2, which this makes sharper: the
  `op_kernel.c` hole is why it *cannot* be cleared while `IsAdmin()` is true,
  but here `IsAdmin()` was false and it still persisted, because no code tries.

### Not verified — treat as unknown

- **Typing at SD from a real Windows console.** Everything above was driven
  with redirected stdin, never an actual console, so how the MSYS2 tty layer
  behaves in `conhost` or Windows Terminal — echo, masked input, arrow keys,
  terminfo — is unknown. The scripted-input corruption in §6 says nothing about
  it either way: those are artefacts of how the shells write to a pipe. This is
  the one question that has to be answered by a person at a keyboard, and it
  matters, because it is what "does SD need MSYS2" really turns on.
- Semaphore locking under contention. The semaphores have never been observed
  held, so the `sdsem.c` port is exercised only in the uncontended case.
- `SDConnectLocal()` at runtime. It needs a running server and a configuration
  file (§5.8).
- **Anything requiring two processes at once, or contention.** The accounts
  above were driven one session at a time. Record locking between real users
  and the API server path are both untried.
- Writing and reading application data. The bootstrap creates and reads system
  files, and the scratch accounts hold nothing but a VOC.
- **`CREATE.ACCOUNT` on Windows.** JANE and SUE were built by a scratch program
  (§3) precisely because `CREATEA` shells out to `sudo usermod` and `groupadd`.
  The verb itself has never been run here.
- The installer. `installsdai.sh` is still entirely Linux.

## 5. Decisions and why

Do not undo these without reading the reasoning.

### 5.1 POSIX IPC replaces System V

System V IPC compiles and links on MSYS2 and then fails at runtime with ENOSYS
(§6); native Windows has none at all. POSIX named shared memory and semaphores
work on both, and are the right direction for stage 2 anyway, since POSIX
shared memory is backed by `CreateFileMapping`.

- `sysseg.c`, `sdidx.c`, `sdlnxd.c`: `shmget`/`shmat`/`shmdt` →
  `shm_open`/`ftruncate`/`mmap`/`munmap`
- `sdsem.c`: `semget`/`semop`/`semctl` → `sem_open`/`sem_trywait`/`sem_post`
- Names come from `SD_POSIX_SHM_NAME` / `SD_POSIX_SEM_FMT` in `sddefs.h`

Two spots needed more than substitution: `munmap` must be told the mapping
length that `shmdt` derived from the address, so it is recorded at attach; and
`stop_sd()` waited on the System V attach count, which POSIX does not expose,
so it now polls the user table with `kill(pid, 0)`. Full reasoning in the
HISTORY entry for 13 Aug 2026, "First native Windows build".

### 5.2 Client library is vendored, not referenced

`gplsrc/sdclilib/` is a vendored copy of `github.com/dmontaine/winsdclilib`
at `b662456`, replacing the old `gplsrc/sdclilib.c`. It sits in its own
directory because its `sdclient.h`, `err.h` and `revstamp.h` are different
files from `gplsrc`'s, and `revstamp.h` stamps the shared memory segment.

Local additions (`SDConnectLocal`, `sysdir`, the transport layer) are recorded
in `gplsrc/sdclilib/VENDORING.md`. **Read that before syncing upstream.**

### 5.3 Two toolchains on purpose

The server is built against the MSYS2 runtime; the client DLL is native
UCRT64 and needs no `msys-2.0.dll`. The runtimes never meet — a client links
the DLL and reaches the server over a socket or a named pipe, always as
separate processes. Override with `UCRT_CC=...`.

### 5.4 The BASIC layer has its own platform switch (not yet touched)

The C code and the BASIC source in `sdsys/GPL.BP` work together — notably for
compilation — and the BASIC side has a platform abstraction of its own that
nothing has yet been done about.

Two SYSTEM keys are the entire bridge:

| Key | Meaning | State |
|---|---|---|
| `SYSTEM(91)` | "is this Windows" | hardcoded to `0` in `op_sys.c` |
| `SYSTEM(1006)` | "is this Windows NT style" | returns `is_nt`, declared `init(FALSE)` in `kernel.h` and **never assigned anywhere** |

Both say "not Windows", so every Windows path in the BASIC layer is dead code.
`is_nt` is dormant in exactly the way `CASE_INSENSITIVE_FILE_SYSTEM` is.

Flipping them is not a one line change, because this repository's BASIC source
has had its Windows branches removed. Files present in both trees lost all of
it — `LOGIN` 16 references to none, `CONFIG` 5 to none, `CPROC` 5 to none,
`CREATEA` 4 to none, `PARSER` 3 to none. The logic still exists in the external
`GPL.BP` tree and can be recovered from there; what each file did is listed in
the HISTORY entry for 13 Aug 2026, "Surveyed the BASIC layer (GPL.BP)". The one
to start with is `CPROC`'s `dir.separator`, because compilation depends on it
(§6). Note that `LOGIN`'s Windows branch forced administrator rights on any
console session, which §5.6 deliberately does not adopt.

Order matters: restoring the BASIC branches while `SYSTEM(91)` still returns
zero is harmless, but flipping `SYSTEM(91)` first turns on paths that are no
longer there.

### 5.5 The Linux privilege model does not survive the move

Background for §5.6, which replaces it. `IsAdmin()` in `linuxlb.c` was
`getuid() == 0` and `SYSTEM(27)` returns `getuid()` straight through. Under
MSYS2 `getuid()` is 197609 — never zero, and Windows has no uid 0 at all. So
every privilege test in the BASIC layer answers the same way permanently, and
the symptom is a refusal from code that looks correct rather than an error
(§6). The sites are `CPROC` (SDSYS entry, and the "entered as root" drop that
never runs), `CATALOG` (`CATALOG GLOBAL`, which matters beyond administration
because cataloguing is part of getting compiled BASIC into service), `BBPROC`,
and `K$ADMINISTRATOR` in `op_kernel.c`. Full table in the HISTORY entry for
13 Aug 2026, "Surveyed every BASIC to C linkage".

`EUID_SET`/`EUID_RESTORE` were the mechanism the root branch used, reaching
`sdext_eguid.c` through `SDEXT` for `getpwnam`, `setegid` and `seteuid`. Native
Windows has no equivalent; impersonation there is `LogonUser` plus
`ImpersonateLoggedOnUser`. That is the shape §5.7's service model needs.

### 5.6 Identity model: accounts with passwords, no OS groups (decided 13 Aug 2026)

Decision from the repository owner on 13 Aug 2026, superseding the `sdadmins`
group model committed earlier the same day in `f56de86`. **SD has no concept of
users, only accounts** — user accounts intended for one person, and group
accounts reachable by many. Authorisation is entirely internal:

- **Every account carries its own password.** Entry is by password prompt,
  whether from `sd -ASDSYS` at the shell or `LOGTO SDSYS` inside SD. This is
  the PICK / UniVerse / OpenQM model.
- **SDSYS is the only administrator.** There is no separate administrator
  account, group or flag. If you know the SDSYS password, you are in.
- **OS groups are dropped from SD's logic entirely.** No `sdadmins`, no
  `sdusers` login gate, no `ACC$GROUP` membership test.

This resolves the open question that stood in §8 (should admin status live
inside SD or in an OS group). Neither of the two options recorded there was
taken; the answer is a third. §5.5 records the Linux privilege model this
replaces, and is retained for background only.

**What already exists and can be reused.** The password machinery is present
and wired:

| Piece | Where |
|---|---|
| Salt generation, `SD_SALT` (100) | `op_sdext.c` → `sd_encrypt_sodium.c` |
| Argon2 key derivation, `SD_KEYFROMPW` (101) | `crypto_pwhash`, same file |
| Masked prompt, `IN$PASSWORD` | `_INPUT` |

So salt, derive and compare is available today without new C code.

**Built and working as of 13 Aug 2026** — see §4 for what was observed:

| Piece | Where |
|---|---|
| `$CRED` register, keyed by account, `CRED$SALT` + `CRED$VERIFIER` | `<sysdir>/$CRED`, defines in `INT$KEYS.H` |
| `!CRED_SET(account, password, ok)` | `GPL.BP/CRED_SET` |
| `!CRED_VERIFY(account, password, ok)` | `GPL.BP/CRED_VERIFY` |
| `SET.PASSWORD [account]` verb | `GPL.BP/SET_ACC_PASSWORD` |
| Password prompt at login, 3 attempts | `LOGIN`, `authenticate.account` |
| `ACC$USERS`, the grant list, field 4 of ACCOUNTS | `SYSCOM/KEYS.H`, dictionary item in `gplbld/FILES_DICTS` |
| `LOGTO` grant check | `CPROC`, `logto.authorised` |
| `LOGTO SDSYS` step-up, 3 attempts | `CPROC`, `logto.step.up` |

`LOGIN` sets `@logname` to the authenticated account and sets
`K$ADMINISTRATOR` on entry to SDSYS. Two deliberate ways in without a password,
both gated on `K$ADMINISTRATOR` (which comes from the OS group via `IsAdmin()`
and cannot be self-granted): an administrator running an internal command,
which is the install path since the bootstrap cannot type a password; and an
account with no password yet, with a warning. So a half-configured system is
not an open one.

**How `LOGTO` decides, as built on 13 Aug 2026.** `CPROC`'s `logto.authorised`
runs where the deleted `ACC$GROUP` test used to sit, immediately after the
ACCOUNTS read, and the early `K$ADMINISTRATOR` test at the top of `int.logto`
is gone — it asked whether the caller was already privileged, which is the
wrong question when entering SDSYS is what confers privilege. In order:

0. **The target must be a registered account name.** Anything not in ACCOUNTS
   is refused before authorisation is even considered — see the pathname
   decision below.
1. An administrator running an internal command is admitted, as at `LOGIN`.
   The bootstrap has no terminal to type a password at.
2. **A session standing in SDSYS may enter any account**, no grant needed.
3. Otherwise you may enter your own account, or one whose `ACC$USERS` names
   you. Refusal is `sysmsg(10003)`, "User not allowed in requested account",
   and the session stays where it was.
4. Entering SDSYS additionally runs `logto.step.up`: three tries at **your own**
   password through `!CRED_VERIFY(@logname, ...)`, with `PT$INVERT` and the
   input prompt character cleared around the read (§6). If you have no
   credential of your own, an administrator is warned and admitted, exactly as
   `LOGIN` treats an account with no password.

`@logname` is untouched by any of it. The only assignments to it anywhere are
`LOGIN` 235, `CPROC` 250 and 282 (both initialisation, the second in a branch
that never runs on Windows), and `APISRVR`. Confirmed by observation as well as
by reading — see §4.

**SDSYS reaches every account, without exception (decided 13 Aug 2026).**
Decision from the repository owner, settling the question this raised when the
grant check was first built. Administration that cannot enter an account cannot
repair one, so SDSYS is not subject to the grant list.

The test is **the account you are standing in** (`who`), not the one you logged
in as, so it holds whether you entered SDSYS directly or stepped up into it
from your own identity — and `@logname` still names the person either way, so
what accounts for the access is the audit record, not a refusal. The
consequence to know: stepping *out* of SDSYS into another account puts you in
that account, and you no longer carry the exception. Going from SDSYS to KIM to
JANE is refused at the second move; return to SDSYS first. Getting back in is
never blocked, because SDSYS is your own account by name if you logged in as
it, and a grant plus your own password if you did not.

**`LOGTO` takes an account name and nothing else (decided 13 Aug 2026).**
Decision from the repository owner. It used to treat anything absent from
ACCOUNTS as a pathname to change directory to, which reached an account's
directory without ever consulting its grant list — the hole recorded in §8 when
the grant check landed, now closed by removing the capability rather than by
resolving paths back to accounts. An unregistered directory is not an account.

An unknown account name gives the same refusal as an account that has not
granted you, so the register cannot be probed to discover which names exist.
That does mean a typo reads as "User not allowed in requested account", which
is the same trade `LOGIN` already makes with "Invalid username or password".

`APISRVR`'s `SrvrAccount` took a name **or** a path in the same way and now
takes a name only. Note that nothing else there is gated: the API server has no
credential model yet, so any session it accepts can still reach any account by
name. The `LOGTO` grant check does not cover that path.

**What is still missing.**

- **The audit records.** Nothing is written yet for a login, a `LOGTO` or a
  failed step-up, which is the remaining half of this model and now the first
  item in §7. Until it lands, the grant check controls access but leaves no
  trace of who used it — and attribution, not access control, is what this
  model is for.
- **There is no verb for managing grants.** `ACC$USERS` has a dictionary entry
  so `LIST ACCOUNTS` shows it and `MODIFY ACCOUNTS` can edit it, which is what
  the 0.6.4 changelog assumed, but nothing offers `GRANT`/`REVOKE`. The scratch
  `BP/GRANT` on this machine is a stand-in, not a design.

- **The credential register is a separate file, not part of the ACCOUNTS
  record**, and must stay that way. `LOGIN` opens `ACCOUNTS` at line 175, in
  the user's own process, before any authentication — it must, to know the
  account exists — and eleven other programs open it too, including `_VOC_REF`
  for routine resolution. Verifiers stored there would let any user pull every
  account's Argon2 hash and attack it offline. In stage 1 `$CRED` is still
  readable by everyone (Windows has no setuid, and there is no privileged
  helper short of §5.7's service), so this does not fix the exposure — it makes
  the boundary exist, so §5.7 can lock one file to the service account without
  restructuring ACCOUNTS or migrating data.
- `ACC$GROUP` is dead but still populated on old records, and `LIST ACCOUNTS`
  still shows it. Remove it with the OS account commands, as one change.
- **`K$ADMINISTRATOR` still comes from the OS group, which is interim.**
  `kernel.c` seeds `USR_ADMIN` from `IsAdmin()` when the user table entry is
  initialised, so on a machine where you are in `sdadmins` **every session you
  start is an SD administrator**, including one logged in as an ordinary
  account. That is what makes the bare-pathname branch of `logto.authorised`
  reachable in ordinary use (§8). Under this model SDSYS entry should be what
  sets the flag; that change waits on the `op_kernel.c` hole below, since
  otherwise any BASIC can set it anyway.
- The privilege tests themselves ask the flag, not the uid: `BBPROC`,
  `CATALOG GLOBAL` and `CPROC` use `kernel(K$ADMINISTRATOR, -1)`, and
  `WRITE_INSTALL_DICTS` uses `SYSTEM(1050)` because `KERNEL` is only available
  to `$internal` programs (§6). Use `SYSTEM(1050)` in anything not internal.
- The `is_grp_member` calls in `CREATEA` (line 323) and `MODIFYA` (96, 99, 125)
  were deliberately left where the others were deleted. They guard
  `OS.EXECUTE` calls to `useradd`, `usermod` and `groupadd`; removing only the
  guard would let those shell-outs run unconditionally, which is worse than
  leaving them. They go when the OS account commands go, as one change.
- `CPROC`'s `system(27) = 0` "entered as root?" branch at line 272 was left
  alone. It guards `EUID_SET`, which has no Windows equivalent (§5.5), and its
  `kernel(K$ADMINISTRATOR, 1)` is now redundant.
- `op_kernel.c` still grants `USR_ADMIN` unconditionally for any positive
  argument (§6), so any BASIC can self-grant. Pre-existing, not made worse by
  the above, but it must be closed before the SDSYS gate means anything.
- The `OS.EXECUTE` account commands in `CREATE_USER`, `SET_PASSWD`, `CREATEA`,
  `DELACC` and `MODIFYA` stop calling `useradd`, `passwd`, `usermod`, `userdel`
  and `groupadd` outright. Under this model they manage SD accounts and their
  passwords, and touch no OS account at all.

**You log in as yourself, then move; the login identity follows you.** This is
how shared access works, and it is what makes it attributable:

- A person logs in with **their own account name and password**. That
  establishes the session identity.
- Access to other accounts is **granted, not shared**. Once in, a person may
  `LOGTO` any account they have been given access to. There is no second
  password to know and none to share.
- **`@logname` does not change on `LOGTO`.** The login identity persists for
  the life of the session, which is the whole mechanism — everything downstream
  attributes to the person who authenticated, not to the account they are
  standing in.
- **Every login and every `LOGTO` is written to an audit log**, in the form
  "SUE logged to JANE at *date/time*".

So the holiday and assistant case is not a shared password. If Sue covers for
Jane, Sue is granted access to JANE; she logs in as SUE, does `LOGTO JANE`, and
the log records that she did. Withdrawing it removes one grant and changes
nobody's password. Nothing is ever shared, so nothing has to be rotated.

This is what raises the bar above OpenQM, where an account password is a single
shared secret with no record of who used it. It also puts administration under
audit for free: SDSYS is reached by `LOGTO SDSYS` from your own identity, and
that entry is logged like any other.

**`LOGTO SDSYS` requires the password again** (decided 13 Aug 2026). It is the
one exception to "granted, not prompted", on the grounds that entering
administration deserves a deliberate act rather than an unguarded session
becoming an administrative one.

**The password it asks for is the person's own, not an SDSYS password.** This
matters and is easy to get backwards. Re-entering your own credential is
re-authentication: it confirms the person at the keyboard is still the one who
logged in, changes nothing about attribution, and introduces no new secret. An
SDSYS password would be a second shared secret held by every administrator,
which is precisely the OpenQM weakness this model exists to remove — the audit
log would still name the person, but the credential behind the most privileged
account in the system would be shared and unrotatable without telling everyone.
Log the step-up separately from the `LOGTO` itself, both when it succeeds and
when it fails; a failed step-up is the single most interesting line in the
audit trail.

Attribution is SD-internal and does **not** depend on the service model in
§5.7, so it lands with the password work. It records who authenticated, not who
is at the keyboard — accountability, not proof of identity.

**The audit log must not be the existing `errlog`.** The `LOGMSG` verb reaches
`log_message()` in `k_error.c`, which writes to `<sysdir>/errlog` and, when the
file reaches the `ERRLOG` configured size, **discards the oldest half**. That is
correct for a diagnostic log and disqualifying for an audit trail, which must
not lose records silently. Write the audit trail to its own file, append-only,
and rotate rather than truncate.

`ACCOUNTS` needs the grants. Record them **on the target account** — JANE lists
who may enter JANE — rather than as a list of destinations on the source. It
answers the question administration actually asks ("who can get into JANE?"),
and revocation happens in one place. Note `$LOGINS` chose the other direction,
`LGN$VALID.ACCOUNTS` and `LGN$BANNED.ACCOUNTS` on each user; that register is
gone (§6) and there is no reason to inherit its shape.

Watch that `CPROC` currently reassigns `logname` when it drops to `sdsys`
(around line 278). Under this model nothing may overwrite the login identity.

**Understand the security consequence before relying on this.** A password
gate inside SD is not a file security boundary — see §5.7.

### 5.7 Where the OS still has to be involved: protecting the data tree

Dropping OS groups from SD's logic (§5.6) does not remove the need for OS file
permissions, and the two do not compose the way one would hope.

**The tension.** Every SD process opens the database directly — `dh_open()` →
`dio_open()` → `open()` — in its own process, under the invoking user's token.
`connection_type` (`CN_CONSOLE`, `CN_SOCKET`, `CN_PIPE`) describes only the
terminal transport; there is no data server. So any ACL strong enough to stop a
user reading the files in Explorer also stops SD reading them on that user's
behalf. **While SD runs as the invoking user, account passwords organise
access; they do not secure it.**

**This is what decides whether accounts are private from each other.** For a
user to enter account B, their Windows token must have read and write on B's
directory, because their own process does the I/O. The OS cannot distinguish
"entered with the right password" from "opened in Explorer" — it is the same
token either way. So in stage 1 there are only two options, and neither is what
was wanted: grant every SD user access to every account directory, which gives
no protection between accounts at all; or set per-user ACLs per account
directory, which is OS-level authorisation duplicating the password gate,
reintroducing exactly what §5.6 removed and adding a Windows-user-to-account
mapping to maintain.

Under the service model the question dissolves: no end user holds any file
access, SD is the only reader, and SD checks the password. Accounts become
private from each other *because* of the password rather than in spite of it,
and shared accounts still work, because the OS never sees individual people at
the file layer.

What is achievable now, and what is not:

- **Achievable in stage 1.** Lock the tree to a single identity plus
  `Administrators`, so no other account on the machine can browse it. This
  blocks everyone who is not an SD user. It does not stop an SD user reading
  another account's files directly, since SD runs as them.
- **The real answer, and it is stage 2.** `sdlnxd` becomes a Windows service
  running as a dedicated service account — a virtual account, `NT SERVICE\SD`,
  needs no password management — which owns the tree exclusively. Session
  processes are spawned under the *service* identity, not the user's, and the
  user reaches their session over the named pipe. The user's own token never
  touches the data. This is the direct Windows equivalent of the Linux original
  dropping to the `sdsys` user via `EUID_SET` (§5.5); it is not a Windows
  novelty. It requires console `sd.exe` to become a client of the service
  rather than doing its own file I/O, which is the substantial part.

**Mechanics, verified on this machine 13 Aug 2026.** `C:\ProgramData` grants
`BUILTIN\Users:(I)(OI)(CI)(RX)` by inheritance, so the default is world
readable and snooping needs no privilege at all. Breaking inheritance and
granting narrowly works and needs no elevation for a directory you own:

```sh
icacls <dir> /inheritance:r /grant "*S-1-5-18:(OI)(CI)F" \
    /grant "*S-1-5-32-544:(OI)(CI)F" /grant "<principal>:(OI)(CI)M"
```

Use SIDs, not names — `*S-1-5-18` is SYSTEM, `*S-1-5-32-544` is
`BUILTIN\Administrators` — so the installer is not broken by a localised
Windows. `/inheritance:r` first is essential; `/grant` alone leaves the
inherited `Users:(RX)` in place and the tree stays readable.

**The useful surprise: `noacl` breaks `chmod`, but not ACL inheritance.** The
MSYS2 mount is `noacl` (§6), so `chmod` is a no-op and cannot be used to secure
anything. But files created *through MSYS2* inside a locked directory still
inherit the restricted ACL correctly, because NTFS applies inheritance at
creation time in the kernel, below the runtime. Confirmed by writing through
the MSYS2 shell into a locked directory and reading back the resulting ACE.
So the installer sets permissions once with `icacls` and everything SD creates
afterwards is protected automatically. This is what makes the approach
practical, and it also answers the `chmod g+s` problem: the setgid directory
behaviour *is* inheritable ACEs.

### 5.8 Install layout follows Windows standards (decided 13 Aug 2026)

Decision from the repository owner on 13 Aug 2026: SD for Windows follows
Windows conventions, not Unix ones. Putting the system under `/etc` and
`/usr/local` was a stage 1 expedient and is not where it belongs.

Target layout:

| What | Where | Replaces |
|---|---|---|
| Binaries | `C:\Program Files\SD\` | `/usr/local/bin` |
| SDSYS and the database | `C:\ProgramData\SD\` | `/usr/local/sdsys` |
| Configuration | `C:\ProgramData\SD\sd.conf` | `/etc/sd.conf` |
| User accounts | `C:\ProgramData\SD\user_accounts` | `/home/sd/user_accounts` |
| Group accounts | `C:\ProgramData\SD\group_accounts` | `/home/sd/group_accounts` |

**What this has to deliver, from the repository owner (13 Aug 2026).** Three
requirements, and two of them already hold:

1. **SD's home is under `C:\Program Files`.** Not done.
2. **The user can start the SD login from any directory.** Already true —
   `sd -ASUE` run from `C:\Windows` logged in normally. What it needs is for
   `sd.exe` to be found and to load the right DLLs, which is why they ship
   beside it (below) rather than being hunted for on PATH.
3. **On login the current directory is the account's directory**, as on Linux.
   Already true: `LOGIN` does `ospath(acc.path, OS$CD)` and sets `@PATH` from
   the result. Logging in as SUE from `C:\Windows` reported
   `PATH=/home/sd/user_accounts/SUE`. Nothing to build, but do not break it —
   it is what makes an account feel like a place rather than a setting.

`ProgramData` is the correct home for machine-wide mutable state, and it has no
space in its name, which sidesteps the `VALID_OS_PATH` trap (§6) for a default
install. `Program Files` does contain a space, so binaries are on the wrong
side of that trap and it must be fixed regardless.

**Ship the MSYS2 DLLs beside `sd.exe` in `C:\Program Files\SD\`.** Windows
searches the executable's own directory before PATH, so this removes both PATH
problems found on 13 Aug 2026 (§6): the exit-53-with-no-message when
`libsodium-26.dll` is missing, and — much worse — Git for Windows's rival
`msys-2.0.dll` being picked up, which makes SD report "SD has not been started"
while it is running. Relying on PATH order is not a supportable install.

Moving off `/usr/local/sdsys` matters on its own merits: it currently resolves
to `C:\msys64\usr\local\sdsys`, inside the MSYS2 install tree, so reinstalling
MSYS2 destroys the database.

**Current state is worse than just the Unix paths — the server and client do
not agree on how to find the configuration:**

| | Environment variable | Fallback |
|---|---|---|
| Server, `GetConfigPath()` in `inipath.c` | `SCARLET_CONFIG` | `/etc/sd.conf` |
| Client, `sysdir()` in `sdclilib/sdclilib.c` | `SD_CONFIG` | `sd.ini` in the Windows directory |

The client's comment claims `SD_CONFIG` matches the server. It does not — the
server reads `SCARLET_CONFIG`. Unify on one variable and one file. Also drop
the `sd.ini`-in-`C:\Windows` fallback: writing there has required
administrator rights since Vista and it is 16-bit-era practice.
`sdnet.h` additionally hardcodes `PASSWD_FILE_NAME "/etc/shadow"`.

**The accounts moved on 13 Aug 2026, and drive letters work now.** Decision
from the repository owner: SD accounts live under `C:\ProgramData\SD\`, beside
the rest of the data. `/home/sd` was the right place while an SD account was an
operating system user; under §5.6 it is not one, so the Linux location decided
nothing. `USRDIR` and `GRPDIR` in `sd.conf` carry it, and the compiled defaults
in `config.c` match.

**Correction to what this section used to say.** It claimed MSYS2 accepts
`C:/ProgramData/SD/sdsys` "with forward slashes throughout", so stage 1 could
move location while keeping `/`. The runtime does — `stat()` accepts
`C:/...`, `C:\...` and `/c/...` equally, all measured — but **SD did not**.
`sdrealpath()` in `linuxlb.c`, which every `openpath` goes through, treated
anything not starting with `/` as a *relative* path and glued the working
directory in front of it, and never treated `\` as a separator. So
`C:\ProgramData\SD` became `/usr/local/sdsys/C:\ProgramData\SD` and every open
failed with ER_FNF, "file not found", naming nothing near the cause.

That function now folds backslashes to `/` and treats a leading drive letter as
the root. All five spellings — `C:\...`, `C:/...`, `/c/...`, lower-case drive,
and mixed — open the same file (§4). `DS` is still `/`; this changed what SD
**accepts**, not what it produces.

Two consequences worth carrying forward:

- **The rest of the move is now much less risky.** `SDSYS=C:\ProgramData\SD\sdsys`
  and binaries under `C:\Program Files\SD\` were blocked by exactly this, and
  are not any more.
- **Stored and displayed paths still come out half POSIX.** `CREATEA` joins
  `CONFIG('USRDIR')` to the account name with `@ds`, which is `/`, so the
  ACCOUNTS record reads `C:\ProgramData\SD\user_accounts/PAT`; and `@PATH`
  comes from `ospath("", OS$CWD)`, which is `getcwd()` and always POSIX, so it
  reports `/c/ProgramData/SD/user_accounts/PAT`. Both work. Both are tidied by
  the `@ds` / `dir.separator` question (§6), which is now **testable** for the
  first time, since a `\` separator no longer breaks path resolution.

### 5.9 The installer becomes an Inno Setup binary (decided 13 Aug 2026)

Decision from the repository owner on 13 Aug 2026. `installsdai.sh` is
apt/dnf/zypper, systemd, xinetd and `/etc` paths throughout and does not
survive the move. It is replaced by an **Inno Setup installer** (preferred) or
failing that a PowerShell script.

What the installer is now responsible for, given §5.6 to §5.8:

- Lay down `C:\Program Files\SD\` and `C:\ProgramData\SD\`.
- Set the ACLs on the data tree with `icacls`, breaking inheritance first
  (§5.7). This is the step that makes the data private, and nothing SD does at
  runtime can substitute for it.
- Prompt for the initial SDSYS password and write the salt and verifier into
  the ACCOUNTS record.
- Create no OS users and no OS groups at all (§5.6).
- Register the service, once §5.7's service model exists.
- Run the BASIC bootstrap sequence in §3.

Inno Setup is a separate toolchain that is **not currently installed** and is
not part of the build. Decide whether the `.iss` script lives in this
repository — it should — and whether CI needs to produce the installer.

### 5.10 Other BASIC to C linkages, surveyed

Full findings in the HISTORY entry for 13 Aug 2026, "Surveyed every BASIC to C
linkage". What still needs attention:

- **`SYSTEM(n)`** — 19 keys used; only 27 (§5.5), 91 and 1006 (§5.4) and 1010
  matter. 1010 returns `PLATFORM_NAME`, `"Linux"` in `sddefs.h`, which `BCOMP`
  turns into the compiler token `SD.LINUX`. Nothing tests that token, so it is
  latent, but user code asking `SYSTEM(1010)` is told "Linux". The rest are
  platform neutral.
- **`OSPATH(path, key)`** — 15 keys into `op_dio2.c`, all path semantics.
  `OS$FULLPATH` is documented "Return full DOS file name"; `OS_CHOWN` has no
  Windows meaning. **Enumerated, not reviewed.**
- **`KERNEL(key, ...)`** — around 120 keys; the platform sensitive ones are
  `K$ADMINISTRATOR` (§5.6), `K$SETUID`, `K$SETGID`, `K$USERS.UID`,
  `K$IN.GROUP`, `K$TTY`, `K$RUNEXE`, `K$INIPATH`. **Enumerated, not reviewed.**
- **`SDEXT`** — used by the `PY_*` family, the `EUID_*` pair and the libsodium
  wrappers.
- **`OS.EXECUTE`** — shell-outs in 10 files; the account commands are §5.6.
- **The compiler chain** carries no platform branches beyond `@ds` (§6) and the
  token above.

### 5.11 No binaries in the repository (decided 13 Aug 2026)

Decision from the repository owner on 13 Aug 2026, **reversing** the earlier
position that linked binaries in `bin/` were tracked so the install scripts
could deploy them from a clone.

**Nothing binary is tracked. Everything must be auditable from source.** That
is the same reason the pcode build is Python in `gplbld/` rather than a shipped
binary. `.gitignore` now excludes `bin/` and every `.exe`, `.dll`, `.a`, `.o`,
`.so`, `.lib` and `.obj` anywhere in the tree. Compiler intermediates,
generated `terminfo/`, pcode scratch and the client's build products remain
excluded as before.

Anything that genuinely has to ship as a binary ships **outside** the
repository, as a release artefact. Do not add a convenience exception.

Consequences to carry into the installer work (§5.9):

- **Installing now means building.** `installsdai.sh` does `cp -R bin
  "$sdsysdir"` and tests for `bin/sd`, both of which assumed a clone already
  contained the binaries. The Inno Setup installer either bundles artefacts
  built elsewhere or drives a build.
- The eight files removed from tracking — `sd.exe`, `sdconv.exe`, `sdfix.exe`,
  `sdidx.exe`, `sdlnxd.exe`, `sdtic.exe`, `sdclilib.dll`, `libsdclilib.dll.a` —
  are still produced by `make sd` and still needed at runtime. They were
  untracked, not deleted.
- **History was rewritten on 13 Aug 2026 to purge them**, so nothing binary
  exists anywhere in the repository, past or present — verified by walking
  every object for NUL bytes. That also removed the pre-port Linux ELF
  binaries (`bin/sd` and friends, which have no extension and which an
  extension-based sweep missed), the 62 generated `terminfo/` files, and the
  compiled I-type object code embedded in two `gplbld/FILES_DICTS` items.
  **Every commit hash changed**; the mapping is in the HISTORY entry
  "History rewritten to purge every binary".
- The install recompiles I-types, so dictionary items carry source and checksum
  only. If a `FILES_DICTS` item ever regains a compiled tail, strip it.

### 5.12 Lower case everywhere it can be (decided 13 Aug 2026)

Goal from the repository owner on 13 Aug 2026. **Everything that can be lower
case should be lower case.** SD is inconsistent about it today — BASIC source
is free-form and usually written in lower case, while file names, field names
and account names are forced up. The end state is lower case throughout, with
existing upper-case code converted rather than tolerated.

Not started, and it is a wide change rather than a deep one. What is known to
force case up today, from work already done:

- **Account names.** `KEYS.H` says "Id = account name (forced to uppercase)",
  and `LOGIN`, `CPROC` and the credential helpers all `upcase()` on the way in.
  The `$CRED` register is keyed the same way, which is why account names are
  case insensitive at login.
- **The terminal itself.** `LOGIN` sets `pterm(PT$INVERT, @true)`, so typed
  input is case-inverted: type `SUE` and the prompt echoes `sue`. This is the
  visible half of the trap in §6 that silently upcased a password.
- Dictionary and VOC item ids, which are conventionally upper case throughout
  `NEWVOC` and `FILES_DICTS`.

Sequencing matters. Case insensitivity of *comparison* is what makes the
current upcasing harmless; removing the upcasing without making the
comparisons case insensitive would make `sue` and `SUE` different accounts.
`CASE_INSENSITIVE_FILE_SYSTEM` (§7) is the file-name half of the same problem
and is already written but never defined, so the two belong together.

### 5.13 Shell access is restored, not blocked (decided 13 Aug 2026)

Correction from the repository owner on 13 Aug 2026: disabling the user's
ability to shell out with `SH` or `!` in the Linux version **was a mistake**,
and Windows makes it a worse one. Many programs have to reach Windows
utilities, and there is no way to do that with shell access blocked.

Not urgent, but it belongs on the list rather than in anyone's memory. Note
this pulls in the opposite direction to the security work in §5.6 and §5.7, so
it is worth being explicit: shell-out runs as the invoking user and always did.
It grants no access the user does not already have at a command prompt, which
is precisely why §5.7's service model — not a block on `SH` — is what makes the
data tree private.

## 6. Traps

Each of these cost real time. Read before debugging anything similar.

- **MSYS2 declares System V IPC but does not implement it.** Headers are the
  real Cygwin ones, so it compiles and links; `shmget`/`semget` return ENOSYS
  at runtime. There is no `cygserver` in MSYS2. Test primitives by *running*
  them, not by checking for headers.
- **`make` must run from `sd64`.** The Makefile uses `MAIN := $(shell pwd)/`,
  so running it from `gplsrc` produces paths like `gplsrc/gplsrc/...`. The
  installer does `cd .../sd64 && make -B`.
- **Link order matters.** The PE/COFF linker resolves strictly left to right,
  so libraries must follow the objects that reference them. ELF hid this with
  `-Wl,--no-as-needed`, which is itself ELF only and has been removed.
- **`.PHONY` is required for `sdclilib` and `terminfo`.** Neither names a file,
  and `VPATH` covers `gplsrc`, so make finds the *directories* and decides the
  target is already satisfied. Symptom: "is up to date" for something that was
  never built.
- **Do not let the client's headers displace the server's.** Specifically
  `revstamp.h` — see §5.2.
- **`O_BINARY`/`O_TEXT` overrides.** `sddefs.h` and `sdtic.c` each hardcoded
  them to zero, correct on Linux. Both are now `#ifndef` guarded. This changes
  nothing on the MSYS2 runtime, which opens files in binary mode by default,
  but it matters for stage 2 where the native CRT defaults to text mode.
- **`ssh -T git@github.com` hangs in a non-interactive shell** on the first
  connection, waiting at the host key prompt. Use
  `ssh -o BatchMode=yes -o StrictHostKeyChecking=accept-new`.
- **Rebuild from clean when switching toolchains.** Stale objects from another
  compiler link into nonsense. `rm -f gplobj/*.o`.
- **`@ds` is load-bearing for compilation.** `BCOMP` opens `@sdsys:@ds:'bin'`
  and builds source paths with it; `BASIC` builds its source and output paths
  the same way. It is SYSCOM slot 57, fed from `dir.separator`, which `CPROC`
  now hardcodes to `'/'`. That is correct on the MSYS2 runtime and is a live
  question for stage 2. If compilation starts failing on path resolution, look
  here first.
- **Adding yourself to a Windows group does not take effect in the session you
  add it from.** Group membership is fixed in the access token at logon, so
  `sdadmins` resolves by name immediately (`getgrnam` finds gid 197613) while
  `getgroups` still does not list it. Elevation does not help — the elevated
  token comes from the same logon. **Sign out and back in, or reboot.** This
  bears directly on the requirement that the installing user become an
  administrator automatically: they cannot use it until they log in again.
- **To test admin-gated paths before that re-logon**, rebuild with the group
  overridden to one the token already holds, e.g.
  `-DSD_ADMIN_GROUP='"Users"'`, and link a probe binary. `SD_ADMIN_GROUP` is
  `#ifndef`-guarded for this. Both `sd.c` and `linuxlb.c` must be rebuilt —
  overriding only `sd.c` does nothing, because `IsAdmin()` lives in
  `linuxlb.c`. Build the object list from `gpl.src`, not `gplobj/*.o`: the
  latter includes the standalone utilities and gives multiple `main`s.

  **The same trick inverted is how you see what an ordinary user sees.** Name a
  group nobody holds — `-DSD_ADMIN_GROUP='"nosuchgroup"'` — and the session is
  not an SD administrator, which is otherwise impossible to arrange on a
  machine whose token carries `sdadmins`. Everything a normal user meets at
  login is behind that. Recompile the two files with the existing objects:

  ```sh
  cd sdb_ai/sd64
  CF="-std=gnu17 -w -D_FILE_OFFSET_BITS=64 -Igplsrc -I/usr/local/include \
      $(python3-config --includes) -DEMBED_PYTHON -DGPL -g \
      -DSD_ADMIN_GROUP='\"nosuchgroup\"'"
  gcc $CF -c gplsrc/sd.c -o /tmp/na/sd.o
  gcc $CF -c gplsrc/linuxlb.c -o /tmp/na/linuxlb.o
  gcc $(sed 's|^|gplobj/|;s|$|.o|' gpl.src | grep -v '/\(sd\|linuxlb\)\.o') \
      /tmp/na/sd.o /tmp/na/linuxlb.o \
      -lm -lcrypt -ldl -lbsd -L/usr/local/lib -lsodium \
      $(python3-config --ldflags --embed) -o /tmp/na/sd_nonadmin.exe
  ```
- **A second `msys-2.0.dll` earlier on PATH makes SD lie about being started.**
  `sd.exe` runs, and reports "SD has not been started" while the server is
  running perfectly. Observed with `C:\Program Files\Git\usr\bin` — Git for
  Windows ships its own MSYS2 runtime — ahead of `C:\msys64\usr\bin`. The
  runtime derives its POSIX root from the location of the DLL that loaded it,
  so `/dev/shm`, `/etc` and everything else resolve inside the *other*
  installation, where the shared segment does not exist. The message names the
  wrong problem entirely, and Git for Windows is on nearly every developer
  machine. Two protections, both in §5.8's direction: put the DLLs beside
  `sd.exe`, since Windows searches the executable's own directory first, and
  never rely on PATH order.
- **Running `sd.exe` outside the MSYS2 shell needs two directories on PATH**,
  not one: `C:\msys64\usr\bin` for the runtime and `C:\msys64\usr\local\bin`
  for `libsodium-26.dll`, which is there because libsodium is built from source
  into `/usr/local` (§2). Missing either gives exit code 53 and **no message at
  all** — the loader fails before `main`.
- **`sd -A` with no account name does nothing.** `sd.c` sets
  `CMD_QUERY_ACCOUNT` for it and **nothing reads the flag** — `CMD.QUERY.ACCOUNT`
  is defined in `INT$KEYS.H` and referenced nowhere else in the BASIC. So bare
  `-A` behaves exactly like plain `sd`, which for an administrator means going
  straight into SDSYS rather than being asked which account, the opposite of
  what the option name promises. Either wire it up or drop it.
- **Case inversion makes the account prompt echo in lower case.** `LOGIN` turns
  `PT$INVERT` on before prompting, so typing `SUE` displays `sue`. It is only
  the echo — `LOGIN` upcases the answer — but it looks like the terminal is
  mangling input. Same mechanism as the password trap below, which is not
  cosmetic at all.
- **Editing BASIC source changes nothing on its own**, and there are two copies
  of it. `sdsys/GPL.BP.OUT` in the repository holds only a README; the compiled
  objects live in the deployed tree. A repository edit must be copied to
  `<sysdir>/GPL.BP/` and then compiled before it has any effect. `$BBPROC` is
  rebuilt with `python3 gplbld/bbcmp.py <sysdir> GPL.BP/BBPROC
  GPL.BP.OUT/BBPROC`; the rest are compiled by the bootstrap itself, and
  `bin/sd -internal BASIC GPL.BP CPROC` at the end. Forgetting the copy step
  gives a silent no-op — the edit is real, the running system never sees it.
- **Privilege tests do not fail, they answer wrongly.** `IsAdmin()` is
  `getuid() == 0` and `SYSTEM(27)` is `getuid()`, which is 197609 here. Nothing
  errors; the branches simply always take one side, so the symptom is "SDSYS
  access is restricted" or "Command requires administrator privileges" from
  code that looks correct. See §5.5 before debugging any permission complaint.
- **`/etc/group` does not exist under MSYS2, so `is_grp_member` fails for
  everyone.** MSYS2 and Cygwin dropped `/etc/passwd` and `/etc/group` in favour
  of direct SAM/AD lookups, but `IS_GRP_MEMBER` reads `/etc/group` as a text
  file. It sets status 1 and returns false always, which fails the `sdusers`
  test at `LOGIN` 193 and terminates every connection with "This user is not
  registered for SD use". **This sits one step past where runtime bring-up
  stopped (§3) and would otherwise be met head-on.** Note this is *not* the
  `getgrnam()` path verified in §4 — that goes through the NSS layer and works
  correctly; reading the file directly does not. Under §5.6 the fix is to
  delete these calls, not repair them.
- **`chmod` is a no-op on the MSYS2 runtime — the mount is `noacl`.** `chmod
  0770` leaves a directory `drwxr-xr-x` and changes no ACE; the real permissions
  stay whatever was inherited, which under `C:\ProgramData` includes
  `BUILTIN\Users:(OI)(CI)(RX)`. Nothing in SD can secure a directory by mode
  bits. Use `icacls` from the installer, `/inheritance:r` first (§5.7).
  Inheritance itself is unaffected by `noacl` and does work — see §5.7.
- **The server and client disagree about the configuration file.** The server
  reads `SCARLET_CONFIG` (`inipath.c`), the client reads `SD_CONFIG`
  (`sdclilib/sdclilib.c`), and the client's comment wrongly claims they match.
  Setting the variable you would expect fixes one and not the other. See §5.8.
- **`sd -start` looks like it hangs, but it has succeeded.** It spawns
  `sdlnxd`, which inherits stdout and stderr. Any shell that captures output —
  a pipe, command substitution, a tool that reads the process's output — then
  blocks until the *daemon* exits, not until `sd -start` exits. The parent has
  already returned. Check with `Get-Process sdlnxd` rather than waiting, and
  redirect to a file when starting from a script.
- **A yes/no prompt with no input left spins forever, at full CPU.**
  `CATALOG BP X GLOBAL` asks "Program is also in private catalogue. Remove?".
  Fed from a pipe that has run dry, the read returns end of file, the prompt
  loop treats it as neither yes nor no, and it asks again immediately — for
  ever. It produced half a megabyte of repeated prompt in about two minutes and
  had to be killed, which then left record locks behind (below). This is not
  specific to `CATALOG`: **any** confirmation prompt reached by a script will do
  it, which matters for §5.9's installer. Answer every prompt a scripted run can
  reach, and if something hangs at 100% CPU rather than idling, look for a
  prompt rather than a lock.
- **Drive a scripted SD session through a pipe, not a `<` redirect.**
  `cat commands | sd -AACCOUNT` works. `sd -AACCOUNT < commands` stops dead
  after the password prompt and exits 0, as though the session had been closed.
  Confirmed from `cmd.exe` as well as from bash, so it is SD's input layer and
  not a shell: it cannot read a password from a regular file.
- **And pipe it from an MSYS2 shell, not a Windows one.** Both Windows shells
  corrupt the first line, which is the password, in their own way:

  | Piped from | What SD receives |
  |---|---|
  | bash, LF text | correct |
  | bash, CRLF text | correct, plus one empty command per line |
  | Windows PowerShell 5.1 | first line **three characters longer** — a UTF-8 BOM on the stream, and `$OutputEncoding` does not suppress it |
  | `cmd.exe` | one character longer per line, plus an empty line that eats one of the three password tries |

  Measured by counting the asterisks SD echoes: `abc` arrived as six characters
  from PowerShell, `abcdef` as nine. These are artefacts of the sending shell,
  not SD faults, but they make "log in from PowerShell" fail with nothing worse
  than "Invalid username or password", which sends you looking in the wrong
  place.
- **`OSPATH()` is only available to `$internal` programs**, like `KERNEL` — and
  it fails the same confusing way. In an ordinary program the compiler takes it
  for an array and reports "Matrix OSPATH is not referenced in a DIM statement"
  plus "WARNING: OSPATH is not assigned a value", never "unknown function".
- **`$catalog NAME` in the source catalogues *privately*.** The compile says
  "NAME added to private catalogue" and the program is then invisible from
  every other account, which reads like the catalogue being broken. Global
  cataloguing needs the verb — `CATALOG BP NAME GLOBAL` — or one of the
  `$`, `!`, `*` prefix characters, which imply global mode.
- **`fullpath()` ignores the failure it is told about, and garbage flows on.**
  `open_file()` in `op_dio1.c` calls `fullpath(pathname, mapped_name)` without
  looking at the result, and `fullpath()` copies its scratch buffer into the
  caller's whether `sdrealpath()` succeeded or not. So an unresolvable path
  does not fail where it went wrong: it produces an arbitrary `pathname`, and
  the `stat()` a few lines later reports ER_FNF, "file not found", about a
  string nobody ever passed in. This is what made the drive-letter problem in
  §5.8 so hard to see. The resolver now accepts drive letters, but the
  swallowed return value is still there.
- **Killing an SD process leaves its record locks behind, and the next run
  waits for them forever.** The lock table lives in the shared segment, so a
  process killed with SIGTERM or SIGKILL never releases what it held. The next
  process that wants the same record takes the lock-wait path in `op_dio3.c`
  (around line 1065): "conflicting lock held by another user" → `Sleep(250)` →
  re-execute the opcode → repeat, with no timeout and no message. The symptom
  is a process that produces no output, never returns, and uses almost no CPU
  — which reads exactly like a deadlock and is not one. **`sd -stop` followed
  by `sd -start` clears it**, because the segment is unlinked and recreated
  empty. Diagnose with `strace`, which shows the offending path being stat'ed
  every 250 ms; and note the semaphores are *not* involved, so their values
  all read 1 while this is happening.
- **`sd -SUSPEND` is sticky and survives the process.** The flag lives in the
  shared segment (`SSF_SUSPEND`), so every later invocation stops at "SD is
  suspended" with no hint of why, including ones that would otherwise do
  useful work. `sd -RESUME` clears it. Neither `-SUSPEND` nor `-RESUME` calls
  `check_admin()`, so any user can suspend a running system — worth revisiting
  under §5.6.
- **Grep the BASIC case-insensitively.** It is case-insensitive source, and it
  is not consistent: four `system(27)` privilege tests are lower case and the
  fifth, in `WRITE_INSTALL_DICTS`, is `SYSTEM(27)`. A case-sensitive sweep
  found four of five and the survivor stopped the bootstrap two steps later.
  Use `grep -i` for anything you intend to be exhaustive.
- **`KERNEL` is only available to `$internal` programs.** In one that is not,
  the compiler does not recognise it as a function and treats it as a variable
  — the symptom is "WARNING: KERNEL is not assigned a value" and an error
  count, not "unknown function". `SYSTEM(1050)` gives the same administrator
  flag without the restriction.
- **`$internal` itself is only accepted under `sd -internal`.** `BCOMP` gates
  the directive on `kernel(K$INTERNAL, -1)` (around line 2852). Compile an
  `$internal` program from an ordinary session and the directive is rejected,
  after which every internal-only statement it enables — `set.status` among
  them — reports "Unrecognised statement". The errors point at those lines, not
  at the directive, so the cause is several lines above the first complaint.
  Compile with `sd -internal BASIC GPL.BP <prog>`.
- **`pterm(PT$INVERT, @true)` silently upcases input, including passwords.**
  `LOGIN` turns case inversion on before prompting. A password typed as
  `hunter2` arrives as `HUNTER2`, so it verifies correctly by hand and fails at
  login with nothing visibly wrong: the record is found, the salt and derived
  key are the right lengths, and `STATUS()` is zero. Save and clear `PT$INVERT`
  around any password read, and restore it afterwards. This cost real time and
  would otherwise have shipped.
- **`WRITE ... THEN` is not valid.** Use a bare `write`, or
  `write rec to file, id on error ... end`. The compiler reports
  "Unrecognised statement" on the `write` line and then "Non-comment text found
  after final end statement" at the end of the program, because the unmatched
  `end` throws off everything after it.
- **The runtime tree needs `gplsrc`, `gplobj` and `gplbld/FILES_DICTS`**, not
  just `sdsys` and `bin`. `installsdai.sh` copies all of them into `<sysdir>`.
  `REVSTAMP` opens `./gplsrc/revstamp.h` relative to the account directory, so
  without it `SECOND.COMPILE` aborts at APISRVR with "Cannot open gplsrc
  revstamp.h" — which reads like a compiler fault and is a missing directory.
- **`errlog` throws away its own history.** `log_message()` in `k_error.c`
  discards the oldest half of `<sysdir>/errlog` when it reaches the `ERRLOG`
  configured size. Fine for diagnostics, fatal for anything you need to trust
  later — do not put audit records there (§5.6).
- **`VALID_OS_NAME` rejects spaces in user names**, undoing a change the
  original made *for* Windows — `ADMUSER` and `CREATEU` both carry the note
  "15 Apr 05 2.1-12 Allow spaces in user names for Windows compatibility".
  Called from `CREATEA` and `APISRVR`.
- **`VALID_OS_PATH` rejects every native Windows path.** Its permitted
  character set is letters, digits and `._-/:` — no backslash — and it rejects
  spaces deliberately, as shell metacharacters. So `C:\SD\accounts` fails on
  the backslash and anything under `C:\Program Files` fails on the space.
  Callers: `CREATEA` (account creation, before `OS.EXECUTE`) and `PY_RUNFILE`.
  It is **not** in the external GPL.BP tree; it was added by the AI cleaning
  cycles, so there is nothing upstream to copy and it must be fixed directly.
  A reminder that the cleaning cycles can introduce Windows problems as well as
  remove clutter.

## 7. Next steps

In the order they should be taken.

1. **Add the audit log** (§5.6). This is now the missing half of the identity
   model: access is controlled, but nothing records who used it. Its own
   append-only file that rotates rather than truncates — *not* `<sysdir>/errlog`,
   which discards its oldest half on reaching the `ERRLOG` size. Records every
   login, every `LOGTO`, and every failed step-up, attributed to `@logname`.
   A failed step-up is the single most interesting line in the trail.
2. **Fix the two ends of the administrator flag.** `op_kernel.c` grants
   `USR_ADMIN` for any positive argument, so BASIC can self-grant and both the
   SDSYS gate and the new `LOGTO` gate are decorative against anyone who can
   run a program. At the other end, **nothing clears the flag when you leave
   SDSYS** — observed, §4 — so administrator rights follow you into whatever
   account you move to. `CPROC` should clear it on any `LOGTO` away from
   SDSYS, which only works once `op_kernel.c` allows clearing. Doing both is
   what lets SDSYS entry, rather than the OS group, become the source of the
   flag (§5.6).
3. **Give grants a verb.** `ACC$USERS` can only be edited through
   `MODIFY ACCOUNTS` today. Decide the shape — `GRANT account TO account` and
   `REVOKE`, or a `SET.ACCESS` screen — and write the audit record from it.
4. **Bring the API server under the same model.** `APISRVR` now takes account
   names only, like `LOGTO`, but nothing else about it is gated: it has no
   credential check of its own, so any session it accepts reaches any account.
   Its `logname` comes from the client (lines 900 and 963), so the grant check
   cannot simply be copied across — the authentication has to come first.
   `sdnet.h` still hardcodes `PASSWD_FILE_NAME "/etc/shadow"` (§5.8), which is
   what that authentication used to be.
5. **Finish the move to the Windows install layout** (§5.8). The accounts are
   done. What remains is `SDSYS` itself to `C:\ProgramData\SD\`, binaries to
   `C:\Program Files\SD\` with the MSYS2 DLLs beside them, unifying the server
   and client configuration variable, and dropping the
   `sd.ini`-in-`C:\Windows` fallback. The `sdrealpath()` fix removed what was
   blocking all of it.
6. **Put `SH` and `!` back** (§5.13). Shell access was disabled on Linux and
   that was a mistake; on Windows it stops programs reaching the utilities
   they need. Find what disabled it — `PT$INVERT`-style config, a `K$SECURE`
   test, or a removed verb — and restore it deliberately.
7. **Make everything lower case that can be** (§5.12). Account names, file and
   field names, and the case inversion at login. Do the case-insensitive
   comparisons first, or `sue` and `SUE` become different accounts; fold
   `CASE_INSENSITIVE_FILE_SYSTEM` (below) into the same piece of work.
6. **Fix `VALID_OS_PATH`** so it accepts backslashes and spaces. Now mandatory
   rather than cheap housekeeping, because step 5 puts binaries under a path
   containing a space. Widen the character set without weakening the shell
   metacharacter protection it exists to provide — quoting the path at the
   `OS.EXECUTE` site is the safer way to allow spaces.
7. **Write the Inno Setup installer** (§5.9), replacing `installsdai.sh`. The
   ACL step is the one that actually makes the data private; nothing at runtime
   substitutes for it.
8. **Enable `CASE_INSENSITIVE_FILE_SYSTEM`.** Referenced at 9 sites in
   `dh_misc.c`, `dh_open.c`, `op_dio2.c`, `op_dio4.c` but never defined
   anywhere. Windows filesystems *are* case insensitive, so this is a
   correctness gap and the code is already written.
9. **Exercise `SDConnectLocal()`** once a server runs. Needs the configuration
   file from §5.8, or `SD_CONFIG` set.
10. **Restore the BASIC layer's Windows branches** from the external `GPL.BP`
    tree (§5.4), then set `SYSTEM(91)` to 1 and assign `is_nt`. In that order:
    flipping the switches first would enable paths that are no longer present.
    Start with `CPROC`'s `dir.separator`, since compilation depends on it.
11. **Stage 2, native Win32.** `fork` → `CreateProcess` (all five call sites
    are fork+exec, none need copy-on-write, so this is tractable), `termios` →
    Console API, passwd/group → Windows authentication. **The service-account
    model in §5.7 belongs here**, and until it lands the data tree is not
    genuinely private from SD's own users.

## 8. Open questions

The identity question that stood here — admin flag inside SD, or OS group — was
**answered on 13 Aug 2026** and is now §5.6. Neither option was taken. See the
HISTORY entry "Identity, install layout and data protection decided" for the
reasoning and for the corrections to the evidence that was recorded here.

### Settled: SDSYS is the exception, and LOGTO takes names only

Both questions raised by the grant check on 13 Aug 2026 were **answered the
same day by the repository owner** and are now written into §5.6. SDSYS reaches
every account without exception, and `LOGTO` accepts a registered account name
only — direct directory access by path is not supported, which closes the
bypass rather than trying to resolve paths back to accounts.

### Settled: the binaries were purged from history on 13 Aug 2026

Done, and force pushed. See §5.11 and the HISTORY entry. **Any clone taken
before that date is incompatible** and must be re-cloned; do not merge or push
from one. The only remaining copy of the pre-rewrite history is a bundle in a
session scratchpad, which will not survive the machine — see the HISTORY entry
if it is wanted.

### Open: what happens to `IsAdmin()` and `sdadmins`?

§5.6 removes the need for both, but they are committed (`f56de86`, `9c00730`)
and `IsAdmin()` is still what gates `sd -start` in `sd.c` — a check that runs
before any account exists or any password can be prompted for. Decide whether
`sd -start` keeps an OS-level check (Windows `Administrators` membership is the
obvious candidate, since starting a service is an administrative act), or
whether starting the server becomes a matter of file permissions on the data
tree alone. Until that is settled, leave `IsAdmin()` in place; it is doing no
harm and removing it would leave `sd -start` ungated.

The `sdadmins` local group on this machine becomes unnecessary under §5.6 and
can be deleted once nothing references it. **Do not delete it yet**: the token
now carries it, which is what allows the shipped `bin/sd.exe` to run `-start`
and `-stop` here without the probe build, and removing it would put this
machine back to needing the probe. It is also, for the moment, the source of
`K$ADMINISTRATOR` for every session (§5.6).

### Open: does the console path survive the service model?

§5.7's service-account model is what makes the data tree genuinely private, but
it requires SD session processes to run as the service rather than as the
invoking user. `sd -ASDSYS` typed at a shell currently runs as that user and
opens the database itself. Decide whether the console entry point becomes a
client of the service, is dropped in favour of a client tool, or stays as a
privileged path used only by administrators. This shapes stage 2 and should be
settled before the `fork` → `CreateProcess` work starts, since that is where
the process creation identity is decided.

### Other

- `usr/lib/systemd/` and `etc/xinetd.d/` are kept deliberately. They have no
  function on Windows but they document the service topology — socket
  activation, ports, per-connection instances — that a Windows service must
  reproduce. Remove once that design is captured elsewhere.
- The client library is LGPL-3.0-or-later with a linking exception, while the
  rest of the tree is GPL-3.0. That is compatible and intentional for a client
  library, but it is a real licensing boundary worth being aware of.
