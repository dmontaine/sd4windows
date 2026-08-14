# PROJECT STATUS

Living handoff document for the SD Windows port. This project moves between
sessions, machines and accounts; anything not written here is lost. Read this
file first. Read [HISTORY.md](HISTORY.md) only if you need the record of how
something came to be the way it is.

**Last updated:** 13 Aug 2026 · **describes the tree as of commit** `68e229e`.
The last commit to change code was `557195f`, which took C source out of the
data tree (§7 step 1, parts a to c, now done); everything since is
documentation. §3 was pruned on 13 Aug 2026 — the bring-up narrative it used to
carry is in HISTORY.md, not lost.

**Next session starts at §7 step 1** — the move itself. `SDSYS` to
`C:\ProgramData\SD\` and the binaries to `C:\Program Files\SD\`. What was
blocking it is gone: nothing compiled from the data tree reads `gplsrc` any
more, and `SECOND.COMPILE` has been run with `gplsrc`, `gplobj` and `gplbld`
absent (§4). Read the `ERRGEN` trap in §6 first if anything to do with
compilation misbehaves.

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

**Who it is for** (stated by the repository owner, 13 Aug 2026): a Windows
developer using SD as a **back end data store, reached through the API**. That
is what settled §5.15, and it should be the tie-breaker on anything else that
asks "is this feature worth carrying?" — it is also why the API's missing
credential model (§5.6, §7 step 6) is more pressing than its position suggests.

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
| `python` | 3.12.13 | the build scripts in `gplbld/` — **not** linked into SD |
| libsodium | 1.0.20 | encryption |

Installed with pacman: `gcc make pkgconf libxcrypt-devel libbsd python
mingw-w64-ucrt-x86_64-gcc`.

**`python-devel` and `gettext-devel` are no longer needed** (13 Aug 2026), both
dropped with embedded Python (§5.15). `gettext-devel` was only ever there
because `python3-config --ldflags --embed` emits `-lintl` and the runtime
`libintl` package does not carry the link library — so removing the interpreter
took a second, unrelated-looking dependency with it.

Plain `python` is still required, and always will be: `gplbld/bbcmp.py` is the
only thing that can compile BASIC before there is a BASIC compiler. It is a
**developer** dependency — an installed system needs no Python at all.

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

### Bootstrapping a machine from nothing

**SD runs.** The sequence below completed on 13 Aug 2026 and the system answers
commands (§4). It is the order `installsdai.sh` uses, with that script's line
numbers, and it is what an installer has to reproduce:

```sh
python3 gplbld/bbcmp.py <sysdir> GPL.BP/BBPROC  GPL.BP.OUT/BBPROC
python3 gplbld/bbcmp.py <sysdir> GPL.BP/BCOMP   GPL.BP.OUT/BCOMP
python3 gplbld/bbcmp.py <sysdir> GPL.BP/PATHTKN GPL.BP.OUT/PATHTKN
python3 gplbld/pcode_bld.py
touch <sysdir>/gcat/'$CPROC'            # line 468 - empty placeholder, required
sd -start                               # line 590 - before -i, not after
sd -i                                   # line 604 - bootstrap pass 1
sd -internal SECOND.COMPILE
sd RUN GPL.BP WRITE_INSTALL_DICTS NO.PAGE
sd THIRD.COMPILE
sd -internal BASIC GPL.BP CPROC         # writes the real gcat/$CPROC
```

Two steps look wrong and are not. The `touch` is what lets `sd -start` run
before anything is catalogued — `read_config()` only does `access(path, 0)` on
`<sysdir>/gcat/$CPROC`, so an empty file satisfies it and the last step
overwrites it. There is no ordering deadlock; if it looks like one, read the
HISTORY entry "SD runs. Full bootstrap completes" before re-deriving it.

Three things worth knowing before running it:

- **`gplsrc`, `gplobj` and `gplbld` do not belong in `<sysdir>`** (13 Aug 2026).
  `APISRVR` and `ERRTEXT` each carried a `$execute` that ran a build tool
  against `./gplsrc`; both are commented out and `gplbld/gen_includes.py` does
  that work at build time. `SECOND.COMPILE` compiled 207 programs with no
  errors without them (§4). `installsdai.sh` still copies them and should stop.
- **An aborted run leaves record locks behind**, so `sd -stop` and `sd -start`
  before retrying, or the next run waits forever at no CPU (§6).
- **Every catalogue write prints `Unable change ownership of directory error
  <path> err: 1000`.** That is `CATALOG` doing the Linux `chown` to
  `sdsys:sdusers`, which has no Windows meaning. Non-fatal, and it goes with
  the rest of the OS-account work in §5.6.

### This machine as the session ended (13 Aug 2026)

None of this is in the repository. The layout is the pre-§5.8 one, under `/etc`
and `/usr/local`; there is no reason to redo it by hand, but **the installer
must not reproduce it**.

| Thing | State |
|---|---|
| `/etc/sd.conf` | `SDSYS=/usr/local/sdsys`; `USRDIR`/`GRPDIR` point at `C:\ProgramData\SD\` |
| `/usr/local/sdsys` | fully bootstrapped, SD answers commands |
| SD server | started, `sdlnxd` running |
| Binary used | `/usr/local/sdsys/bin/sd.exe`, the shipped build — the probe is no longer needed here, since the token now carries `sdadmins` |
| `sdadmins` local group | created, `GITORLI\don` enrolled — **unnecessary under §5.6**, but do not delete it yet (§8) |
| **SDSYS password** | **`hunter2`** — set during testing, change it |
| Scratch accounts | `JANE`, `SUE`, `KIM` under `/home/sd/user_accounts`; `PAT` under `C:\ProgramData\SD\user_accounts`. Passwords **`correcthorse`** (SUE) and **`batterystaple`** (PAT). Delete all of them before this machine is used for anything real |
| Grants recorded | `JANE` grants `SUE`; `SDSYS` grants `SUE`; `KIM` and `PAT` grant nobody, which is what makes them useful |
| `gplsrc`, `gplobj`, `gplbld` | **moved out of `<sysdir>`** into a session scratchpad. Do not put them back |
| `<sysdir>/C:` | an empty directory left by the `sdrealpath()` bug before it was fixed (§5.8). Harmless, and not evidence of anything |

**Scratch test programs in `<sysdir>/BP`**, none of them in the repository:
`CREDTEST`, `CREDRT`, `SETPW`, `INTEST`, `VTEST`, `MKACC`, `GRANT`, `WHOAMI`,
`MKDICT`, `MKBP`, `PROBE`, plus `SUE/BP/ESCALATE` (§4), which no longer
compiles. `SETPW` and `MKACC` hold passwords in plain text and go with the
scratch accounts. Two are worth keeping until there are real verbs for the job:
`WHOAMI` prints `@LOGNAME`, `@WHO`, `@PATH` and `SYSTEM(1050)`, and is
catalogued **globally** so it runs from an account with no `BP` file; `MKACC`
skips an account already in ACCOUNTS rather than rewriting it, so re-running it
does not wipe the grant lists.

A **non-administrator probe** sits at `/tmp/nonadmin/sd_nonadmin.exe`, built
per §6 with `SD_ADMIN_GROUP` naming a group nobody holds. It is the only way to
see this system as an ordinary user, since every session here is otherwise an
SD administrator. `/tmp` does not survive a rebuild; the recipe in §6 does.

### Picking it up again

`echo hunter2 | sd -internal COUNT VOC` should report 432 records and
`echo hunter2 | sd -ASDSYS WHO` should report `SDSYS`. **Both need the password
now** — the internal no-password path is gone (§5.6). If they fail, SD is not
started: `bin/sd.exe -stop` then `bin/sd.exe -start`, redirecting output to a
file (§6).

**A scripted session must be piped from an MSYS2 shell** and cannot use a `<`
redirect (§6):

```sh
cat commands.txt | /usr/local/sdsys/bin/sd.exe -ASDSYS 2>&1 | tr -d '\r'
```

with the password as the first line of `commands.txt` and `OFF` as the last.
Leave a prompt unanswered at end of input and SD spins at full CPU (§6).

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
  `LOGTO KIM` left `SYSTEM(1050)` at 1 while standing in KIM. **Fixed later
  the same day** — see the privilege-escalation entry below.
- **Privilege escalation was demonstrated, then closed.** Before the fix, the
  account SUE compiled this in her own `BP` and ran it from an ordinary
  session:

  ```
  $internal
        program escalate
        crt 'before: ' : kernel(26, -1)
        void kernel(26, 1)
        crt 'after:  ' : kernel(26, -1)
        end
  ```

  It printed `before: 0` / `after: 1` and `SYSTEM(1050)` then reported 1 —
  a plain user account making itself an administrator in three lines. Key 26
  is `K$ADMINISTRATOR`, written as a literal because an ordinary account
  cannot reach SDSYS's `INT$KEYS.H`, which is no obstacle to anyone.

  After the fix the same program fails to compile — `$internal` is refused,
  so `KERNEL` is taken for an undimensioned array — and SUE stays at 0. The
  other route is closed too: `sd -internal -ASUE` is refused by `sd.c`.
- **The rest of the account model still behaves after all of that.** `sd`
  with no account named now prompts `Account:` even for a member of
  `sdadmins`; `sd -internal` prompts for the SDSYS password and refuses three
  wrong ones; the whole `LOGTO` suite above still passes; and
  `BASIC GPL.BP CPROC` still compiles a system program, which is the one that
  matters, since `BCOMP` itself changed.
- **The data tree needs no C source.** `SECOND.COMPILE` compiled **207
  programs with no errors** against a `<sysdir>` with `gplsrc`, `gplobj` and
  `gplbld` moved away — run twice, once with the original include files and
  again after regenerating them, both clean. Afterwards `COUNT VOC` still
  reports 432 records, `WHO` still reports `SDSYS`, and `COUNT NOSUCHFILE`
  still expands to "File not found", which exercises `!ERRTEXT` and therefore
  the regenerated `ERRTEXT.H`. 207 rather than the 204 recorded earlier
  because the credential programs were added since. Observed 13 Aug 2026.
- **The staged tree runs with MSYS2 entirely off PATH.** `gplbld/stage.py`
  built the tree; `sd.exe` from
  `<stage>\ProgramFiles\usr\bin\` then ran with `PATH` cut down to
  `C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem` — no `msys64`, no
  Git for Windows — and answered `SD is not active.` cleanly, with no warnings
  and exit 0. That proves the computed DLL closure is complete — only
  `kernel32` and `ntdll` come from Windows — and that the `usr\bin` plus
  `etc\fstab` arrangement resolves `/dev/shm` correctly. "SD is not active" is
  the right answer, not a failure: the running server's segment belongs to the
  `msys64` POSIX root and this process has its own. Observed 13 Aug 2026 at
  3087 files and 16 MB with embedded Python, and **3059 files and 9.6 MB after
  §5.15 removed it**, the closure dropping from seven DLLs to four —
  `msys-intl-8` and `msys-iconv-2` turned out to be there only because Python
  was.
- **`gplbld/gen_includes.py` reproduces the generators it replaces.** Its
  output matched the tracked files byte for byte on everything that had
  genuinely been generated from the current C headers — all 199 entries of
  `GPL.BP/ERRTEXT.H` and 199 of the 241 `$define` lines in `SYSCOM/ERR.H` —
  and the differences it reported were all real drift, described in the
  HISTORY entry. `--check` reports the three files in sync after regeneration
  and reported each of them stale before it.

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
- **Contention.** Two sessions have now coexisted — an interactive one sitting
  at a password prompt on `/dev/pty0` and a second running `LISTU`, which
  listed both (users 8 and 9, 13 Aug 2026). So multi-user attach works. What
  is still untried is two sessions *competing*: record locking between real
  users, and the API server path.
- Writing and reading application data. The bootstrap creates and reads system
  files, and the scratch accounts hold nothing but a VOC.
- **`CREATE.ACCOUNT` on Windows.** JANE and SUE were built by a scratch program
  (§3) precisely because `CREATEA` shells out to `sudo usermod` and `groupadd`.
  The verb itself has never been run here.
- **The installer, and this is the least tested part of the system.** Nothing
  has ever been installed from a staged tree, and `installsdai.sh` is entirely
  Linux and is not being ported (§5.9). Until an install is done on a machine
  with no development tree, what SD depends on by accident is unknown — which
  is precisely how `gplsrc` stayed in the data tree.

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
takes a name only. Note that nothing else there is gated: once a session is
accepted it reaches any account by name, because the `LOGTO` grant check does
not cover that path.

**Correction (13 Aug 2026): this section used to say the API server "has no
credential model yet".** That is wrong. `APISRVR` line 921 calls
`login(username, password)`, which is a real connect-time check — it simply
**cannot succeed on Windows**, because it reads `/etc/shadow`, which MSYS2 does
not have (§6). So the API is currently closed rather than open. What is
genuinely missing is authorisation *after* connect, and an authentication
mechanism that can work at all. See §7 step 6 and the open question in §8.

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
- **Administrator rights are the SDSYS account's, and nothing else's**
  (13 Aug 2026). `LOGIN` sets `USR_ADMIN` on entry to SDSYS and clears it on
  entry to anything else; `CPROC` does the same on every `LOGTO`, so the
  rights are given up on the way out. `kernel.c` still seeds the flag from
  `IsAdmin()` at process start, but that now decides only one thing — whether
  a credential-less account can be entered during a fresh install — and no
  longer confers standing privilege. Observed: `sd -ASUE` on a machine whose
  token holds `sdadmins` reports `SYSTEM(1050)` as 0.
- **Only an `$internal` program may set the flag, and only SDSYS may build
  one.** Both ends of `K_ADMINISTRATOR` in `op_kernel.c` were open: any
  positive argument granted the flag, and `|| IsAdmin()` meant an argument of
  zero re-granted rather than cleared. The set is now gated on
  `process.program.flags & HDR_INTERNAL`, and `BCOMP` accepts the `$internal`
  directive only for a caller who is in SDSYS. The second half is what makes
  the first half real: internal mode alone was not a gate, because
  **`sd -internal` is not itself gated** and an ordinary account could compile
  a three-line internal program that granted itself rights. That was
  demonstrated before it was fixed — see §4.
- **`sd -INTERNAL` means SDSYS, and asks for its password** (decided by the
  repository owner, 13 Aug 2026). Naming any other account with `-INTERNAL` is
  refused in `sd.c` rather than quietly redirected. The no-password bypass for
  an administrator running an internal command is gone with it: that was the
  last route into administration that did not involve knowing the SDSYS
  password. The install is unaffected — `sd -i` runs `$BBPROC`, which never
  reaches `LOGIN`, and until the installer sets a password SDSYS has no
  credential to check, so the "no password yet" branch admits an
  administrator with a warning.
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
| Binaries, and the MSYS2 DLLs beside them | `C:\Program Files\SD\usr\bin\` | `/usr/local/bin` |
| Mount table, mapping `/dev/shm` out to writable space | `C:\Program Files\SD\etc\fstab` | — |
| Configuration | `C:\ProgramData\SD\sd.conf` | `/etc/sd.conf` |
| The SDSYS account | `C:\ProgramData\SD\sdsys\` | `/usr/local/sdsys` |
| User accounts | `C:\ProgramData\SD\user_accounts\` | `/home/sd/user_accounts` |
| Group accounts | `C:\ProgramData\SD\group_accounts\` | `/home/sd/group_accounts` |
| POSIX shared memory | `C:\ProgramData\SD\shm\` | `/dev/shm` |

**`usr\bin` is load-bearing, not tidiness** (established 13 Aug 2026). Shipping
`msys-2.0.dll` beside the executable relocates the POSIX root to the DLL's
directory minus **two** components, so only that depth puts `/` on
`C:\Program Files\SD\`. The full rule, the measurements behind it, and the
`fstab` entry that moves `/dev/shm` back to writable space are in §6 — read it
before changing where anything goes.

**Three siblings under one root**, not SDSYS with the accounts nested inside
it. That is what makes §5.7 practical: one `icacls` on `C:\ProgramData\SD\`
with inheritance doing the rest, rather than a grant per location repeated
every time an account is created.

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

### 5.9 One installer: a staging script, then Inno Setup (decided 13 Aug 2026)

**Revised twice on 13 Aug 2026; this is the current decision and it reverses
the middle one.** The `installsdai.sh` port is **dropped**. Two scripts replace
it: one that builds a **staging directory** holding exactly what an install
consists of, and one that turns that directory into an **Inno Setup
installer**. Neither the shell installer nor `deletesdai.sh` gets ported.

The three positions in order, so the change is legible: go straight to Inno →
no, do the Linux method on Windows first, since `installsdai.sh` is
apt/dnf/zypper, systemd, xinetd and `/etc` throughout → no, skip it. The
reasoning is in the HISTORY entry for 13 Aug 2026, "Installer: the shell script
port is dropped".

**Why the Linux script existed, and why that reason does not transfer.** This
is the part worth understanding before anyone proposes porting it again.
`installsdai.sh` was not a developer convenience — it was load-bearing.
ScarletDME targeted Fedora, Debian, Arch and OpenSUSE across several versions
each, every one with its own compiler, libc and package names. No single binary
works across that, so **the end user had to compile**, and the script existed to
abstract apt from dnf from pacman from zypper and drive a build on the user's
own machine.

Windows has none of that. One target, one ABI, and SD ships its own runtime
beside `sd.exe` (§5.8), so there is nothing to adapt to and the user needs no
compiler at all. The requirement that made the script necessary on Linux simply
does not exist here — which is why what is left of it, once the distro handling
is stripped out, is a developer setup tool that §2 and §3 already cover. Note
this makes the Windows install genuinely *simpler* than the Linux original,
which is not true of much else in this port.

**The staging script is the valuable half**, and not mainly because of
packaging:

- **It makes §5.8 executable.** The install layout is prose here; a staging
  script is that layout in a form that either runs or does not. It is what
  forces the `<sysdir>/bin` split (§6) to be decided rather than remembered.
- **It is a whitelist, and whitelists find accidental dependencies.** This is
  the strongest argument for it. `gplsrc` sat in the data tree for as long as
  it did because `installsdai.sh` copied it wholesale and nobody asked why —
  a fault that cost most of a session on 13 Aug 2026. A script that copies
  only what is on a list, installed on a machine with no development tree,
  surfaces that class of thing at once. The installer is the least tested part
  of this system (§4); making it cheap to rerun is what changes that.
- **It is where the DLL closure is computed, not guessed.** §5.8 requires the
  MSYS2 DLLs beside `sd.exe`. Which ones — `msys-2.0.dll`, `libsodium-26.dll`,
  and whatever python, intl, bsd and crypt pull in — must be **derived by
  walking the imports**, because missing one gives exit code 53 and no message
  at all (§6). Python in `gplbld/`, beside `bbcmp.py`, `pcode_bld.py` and
  `gen_includes.py`, is the natural home.

**Inno Setup then packages the staged directory.** It stages *pre-compiled*
artefacts rather than building on the target, which is what an end user should
get, and it collides with §5.11 only in appearance: the staged artefacts are
release artefacts built elsewhere, not tracked files. The `.iss` script does
belong in this repository. **Correction to what this section said before: the
Inno Setup compiler is installed on this machine** — it was recorded as absent.

**`deletesdai.sh` is not ported, but read it before writing the uninstaller.**
Inno gives you an uninstaller for free; it does not answer the question that
matters. `C:\ProgramData\SD\` holds the user's database. Removing it on
uninstall is a catastrophe, and leaving it makes reinstall awkward because
accounts and `$CRED` are already there. Decide deliberately; the old script is
where the current answer is written down.

What the installer is responsible for, given §5.6 to §5.8:

- Lay down `C:\Program Files\SD\` and `C:\ProgramData\SD\`.
- Set the ACLs on the data tree with `icacls`, breaking inheritance first
  (§5.7). This is the step that makes the data private, and nothing SD does at
  runtime can substitute for it.
- Prompt for the initial SDSYS password and write the salt and verifier into
  the ACCOUNTS record.
- Create no OS users and no OS groups at all (§5.6).
- Register the service, once §5.7's service model exists.
- Run the BASIC bootstrap sequence in §3.

Inno Setup is a separate toolchain and is not part of `make`. Still to decide:
whether CI produces the installer, and what the uninstaller does with the data
tree.

**This is a hobby project with no release schedule and no architecture
document to satisfy.** That is context worth having when weighing "do it
properly" against "do it now": the answer here is usually to do the thing that
keeps development moving and record honestly what it does not yet do. The two
handoff files and the changelog are the only process there is.

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
- **`SDEXT`** — used by the `EUID_*` pair and the libsodium wrappers. The
  `PY_*` family was the third caller and is gone (§5.15).
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

- **Installing now means building** — but only for whoever runs the staging
  script, which is the point of it (§5.9). `installsdai.sh` does `cp -R bin
  "$sdsysdir"` and tests for `bin/sd`, both of which assumed a clone already
  contained the binaries; that is one of the reasons it is not being ported.
  The end user gets the Inno Setup installer and needs neither a clone nor a
  toolchain.
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

### 5.14 Administration should be forms, not remembered command lines (goal, 13 Aug 2026)

Goal from the repository owner on 13 Aug 2026, for **after the system runs
well** — not now, and not a reason to hold anything else up. Much of what
administration currently requires is a command line somebody has to remember,
or a record edited by hand in `MODIFY`. The intent is a set of admin helpers
that put a form in front of the same work.

Recording it here because it changes how several things on the §7 list should
be built, and it is cheaper to know that before writing them than after:

- **The grants verb** (§7 step 5) is the clearest case. `ACC$USERS` is edited
  through `MODIFY ACCOUNTS` today. Whatever shape it takes — `GRANT`/`REVOKE`
  or a `SET.ACCESS` screen — a form is the destination, so put the work in a
  subroutine the form can call rather than in the verb itself.
- **The batch allowlist** (§8) is the same: `ED VOC ALLOWED` is workable and a
  form is better, particularly as it is the one place that has to enforce the
  no-arguments and VOC-type rules recorded there.
- **`SET.PASSWORD`** already exists and is prompt-driven, which is the right
  precedent.

The general rule that follows: **new administrative capability goes in a
subroutine with a verb over it**, not in a verb that holds the logic. A form
added later then calls the same subroutine instead of reimplementing it or
shelling out to the verb. `GPL.BP/CRED_SET` and `CRED_VERIFY` with
`SET_ACC_PASSWORD` over them are the pattern to copy.

### 5.15 Embedded Python is dropped; the API is the point (decided 13 Aug 2026)

Decision from the repository owner on 13 Aug 2026, and it is a **statement
about what SD for Windows is for**, not just a packaging choice: the intended
user is a Windows developer using SD as a **back end data store, reached
through the API**. Embedded Python was not part of that, so it is gone rather
than shipped unused.

Removed outright, not left behind an `#ifdef` — the same reasoning as the Linux
code in §1, and two of the files could not have stayed anyway:

| Gone | Note |
|---|---|
| `gplsrc/sdext_py.c`, `gplsrc/op_sdpyobj.c`, `gplsrc/sdext_python_inc.h` | **unguarded** and listed in `gpl.src`, so they could not compile without the Python headers at all |
| `EMBED_PYTHON` blocks in `op_sdext.c` and `sd.c` | the `SD_Py*` SDEXT keys now fall through to the unknown-key response, which is what they are |
| `PY_HDRS`, `PY_LDFLAGS`, `-DEMBED_PYTHON` in the Makefile | |
| 20 `GPL.BP/PY_*` programs, `SYSCOM/SDPYFUNC.H`, 4 `sdsys/BP/PY_*` test programs | nothing outside them called them, so the removal is self-contained |
| The `SD_Py*` error codes in `gplsrc/err.h` and the `SD_Py*`/`SD_Obj_*` keys in `SYSCOM/KEYS.H` | `gplbld/gen_includes.py` regenerated `SYSCOM/ERR.H` and `GPL.BP/ERRTEXT.H` from the edited header, which is the first real use of that tool |

**Three consequences worth carrying forward.**

- **Two build dependencies disappear, not one.** `python-devel` obviously, and
  `gettext-devel` because it was only ever needed to satisfy the `-lintl` that
  `python3-config --ldflags --embed` emits (§2). Plain `python` is still
  needed by `gplbld/`, for the developer only.
- **The install gets much smaller and one open question closes.**
  `msys-python3.12.dll` leaves the DLL closure, and with it the unresolved
  question of whether to ship the 195 MB Python standard library — which
  `gplbld/stage.py` was warning about. There is nothing to decide any more.
- **It reorders §7.** If the API is the primary interface then step 6, bringing
  `APISRVR` under the identity model, and exercising `SDConnectLocal()` are
  more important than their positions suggest. `APISRVR` currently has **no
  credential check of its own** (§5.6), which matters a great deal more for a
  product whose main door is the API than for one where it is a side entrance.
  Not reordered yet — flagged, because it is the repository owner's call.

## 6. Traps

Each of these cost real time. Read before debugging anything similar.

- **MSYS2 declares System V IPC but does not implement it.** Headers are the
  real Cygwin ones, so it compiles and links; `shmget`/`semget` return ENOSYS
  at runtime. There is no `cygserver` in MSYS2. Test primitives by *running*
  them, not by checking for headers.
- **The Makefile does not track header dependencies, so edit a header and
  `make` links stale objects.** Changing `opcodes.h` on 13 Aug 2026 left
  `kernel.o` untouched and the link failed with `undefined reference to
  op_sdpyobj` pointing at `kernel.c`, a file that had not been edited. Delete
  the affected object, or `rm -f gplobj/*.o`, after touching any header.
- **Retire an opcode in place; never delete the line.** `opcodes.h` is a
  positional table — removing an `_opc_` entry renumbers every opcode after it
  and invalidates all compiled pcode everywhere. The file's own convention is
  to keep the slot and point it at `op_illegal` with a generic name, as
  `OP_09`, `OP_9E` and `OP_BB` do. `OP_CFFE` is now one of them (§5.15).
  **And the BASIC side has to move with it**: `BCOMP` registers intrinsics in
  `int.intrinsics` and dispatches through an `on i goto` list that is matched
  to it **by position**, so an entry removed from one must be removed from the
  other in the same edit or every intrinsic after it dispatches to the wrong
  handler.
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
- **Shipping `msys-2.0.dll` beside `sd.exe` moves the whole POSIX namespace,
  and the rule is "strip two path components".** This is the sharp edge of
  §5.8's decision to put the DLLs next to the executable, and it is not
  obvious: the runtime derives its POSIX root from the DLL's own location, by
  removing **two** components from the directory holding it — matching MSYS2's
  own `<root>\usr\bin`. Measured on 13 Aug 2026 with `cygpath -w /` against a
  staged tree, after guessing wrong twice:

  | `msys-2.0.dll` at | `/` becomes |
  |---|---|
  | `<X>\SD\usr\bin\` | `<X>\SD\` |
  | `<X>\SD\bin\` | `<X>\` |
  | `<X>\SD\` | the parent of `<X>` |

  So `/dev/shm`, `/etc/sd.conf` and `/tmp` all move with it. The first symptom
  is a warning that `/dev/shm` does not exist, followed by every POSIX shared
  memory call failing — which is the entire IPC layer (§5.1). **Put the
  binaries in `C:\Program Files\SD\usr\bin\`**, so the root lands on
  `C:\Program Files\SD\` and everything POSIX stays inside SD's own directory.
  One level up and the root is `C:\Program Files\` itself, which would mean
  creating `C:\Program Files\dev`.

  **`/dev/shm` then has to be moved back out**, because `shm_open()` creates
  files in it so every SD user needs write access, and Program Files is
  read-only to ordinary users by design. Cygwin reads `<root>\etc\fstab` and a
  bind entry does it — verified working:

  ```
  C:/ProgramData/SD/shm /dev/shm ntfs binary 0 0
  ```

  `gplbld/stage.py` writes that file. Note the same relocation is why
  `/etc/sd.conf` would resolve inside `C:\Program Files\SD\`, which is another
  reason to finish unifying the configuration variable (§5.8) rather than lean
  on the fallback path.
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
- **The API's two security mechanisms both stop working on Windows, in
  opposite directions.** `login_user()` in `linuxio.c` has two paths and the
  port breaks each differently:

  - With `APILOGIN=1`, which is what `sd.conf` ships, it reads
    `PASSWD_FILE_NAME`, `/etc/shadow`. **MSYS2 has neither `/etc/shadow` nor
    `/etc/passwd`** — the same NSS change behind the `is_grp_member` trap
    above. `fopen` returns NULL and it fails closed, so every API login is
    refused. Safe, but the API is unusable.
  - With `APILOGIN=0` it skips passwords and trusts `getpeereid()` on an
    AF_UNIX socket — mab's 2024 hardening, and the right model. **But MSYS2
    emulates AF_UNIX over a TCP loopback socket with a handshake file.** It is
    not a filesystem object with permissions, so "local socket" is a far
    weaker statement here than on Linux, and any local process can reach the
    port. Do not carry the Linux reasoning across unexamined.

  The Windows equivalent of `SO_PEERCRED` is a **named pipe** with
  `ImpersonateNamedPipeClient` or `GetNamedPipeClientProcessId`, on a pipe
  whose security descriptor you control. `connection_type` already has
  `CN_PIPE`, so the concept is present in the code.
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
- **`<sysdir>/bin` is two unrelated things in one directory.** It holds the
  executables the install copies there, *and* an SD file that `BCOMP` opens as
  `@sdsys:@ds:'bin'` to read and write the pcode composite library, records
  `pcode` and `pcode.old` (around line 1611, the recursive-compilation path).
  They share a directory only because the Linux install put everything under
  `/usr/local/sdsys/bin`. When the binaries move to `C:\Program Files\SD\`
  (§5.8), **the pcode library stays behind with SDSYS** — it is data, and
  `BCOMP` addresses it relative to `@sdsys`. Move the whole directory and
  recursive compilation breaks, at a distance, with nothing pointing here.
- **`SECOND.COMPILE` aborts at APISRVR with "Cannot open gplsrc revstamp.h",
  and the cause is two lines in APISRVR — not a missing directory.** This was
  recorded here as "the runtime tree needs `gplsrc`, `gplobj` and
  `gplbld/FILES_DICTS`", which is what `installsdai.sh` copies and what makes
  the symptom go away. **That diagnosis was wrong** (13 Aug 2026).
  `APISRVR` lines 64-66 are:

  ```
  $execute 'BASIC GPL.BP REVSTAMP'
  $execute 'RUN GPL.BP REVSTAMP'
  $include revstamp.h
  ```

  Compile-time directives that *run* `REVSTAMP`, which opens
  `./gplsrc/revstamp.h` relative to the account directory. `SECOND.COMPILE` is
  only the paragraph `TERM 120,9999` then `BASIC GPL.BP *`, so it aborts when
  it reaches APISRVR and nowhere else. **`CPROC` carries the identical two
  lines already commented out** (139-140), with a note that the build should
  compile and run REVSTAMP to sync the two headers — so the intended fix is
  already demonstrated one file away.

  `REVSTAMP` is a build tool: it translates the C header into the BASIC
  include `GPL.BP/REVSTAMP.H`, which is tracked in the repository. **Both
  `$execute` lines are now commented out** (13 Aug 2026) and
  `gplbld/gen_includes.py` does the translation at build time.

  **And there was a second one, which is the dangerous one — `ERRTEXT` runs
  `ERRGEN`.** `GPL.BP/ERRTEXT` line 33 carried `$execute 'RUN GPL.BP ERRGEN'`,
  and `ERRGEN` reads `./gplsrc/err.h` to generate `SYSCOM/ERR.H` and
  `GPL.BP/ERRTEXT.H`. It **truncates both outputs with `weofseq` before it
  opens its input**, so with `gplsrc` absent it destroys them and then aborts.
  `SYSCOM/ERR.H` is left at zero bytes.

  What that looks like is nothing like a missing file. Every `ER$` constant in
  the system becomes undefined, and an undefined `$define` in SD is **not a
  compile error** — the compiler takes the name for a variable, prints
  `WARNING: ER$ARGS is not assigned a value`, reports `0 error(s)`, and writes
  the broken object into the global catalogue. The failure arrives later, at
  run time, as `Unassigned variable ER$ARGS at line 60 of $CATALOG` in a
  program that compiled cleanly. Read every `WARNING: ... is not assigned a
  value` as a probable missing include.

  **Recovering a poisoned catalogue.** Once `$CATALOG` or `$BCOMP` is broken
  you cannot simply recompile, because compiling and cataloguing go through
  them. Restore `SYSCOM/ERR.H` from the repository first, then:

  - `sd -internal BASIC GPL.BP CATALOG` recompiles it correctly and then
    aborts trying to catalogue it with the old broken `$CATALOG`. The object
    is already written, so copy it into place by hand:
    `cp <sysdir>/GPL.BP.OUT/CATALOG <sysdir>/gcat/'$CATALOG'` — the catalogue
    entry is just a copy of the object, which is the same trick the bootstrap
    uses for `gcat/$CPROC`.
  - With `$CATALOG` working, `sd -internal BASIC GPL.BP BCOMP` repairs the
    compiler, and `SECOND.COMPILE` then repairs everything else.
- **`SECOND.COMPILE` must be run under `sd -internal`, not `sd -ASDSYS`.**
  `BCOMP` gates the `$internal` directive on `kernel(K$INTERNAL, -1)` **and**
  `kernel(K$ADMINISTRATOR, -1)` (line 2860), so being in SDSYS is not enough.
  Run from an ordinary SDSYS session it reports `Unrecognised compiler
  directive` on the `$internal` line of every internal program and then a
  cascade of consequential errors — right bracket not found, misformed
  `$CATALOG`, matrix not in a DIM statement — none of which names the cause.
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

Reordered 13 Aug 2026 to the repository owner's stated priorities: finish the
install layout, then make installing work end to end, and only then go back to
the identity model.

1. **Finish the move to the Windows install layout** (§5.8). The accounts are
   done. What remains is `SDSYS` itself to `C:\ProgramData\SD\`, binaries to
   `C:\Program Files\SD\` **with the MSYS2 DLLs beside them** — the exe's own
   directory is searched first, which is the only reliable answer to the PATH
   traps in §6 — unifying the server and client configuration variable, and
   dropping the `sd.ini`-in-`C:\Windows` fallback. The `sdrealpath()` fix
   removed what was blocking all of it.

   **The data tree holds data only, and that part is done** (decided by the
   repository owner, 13 Aug 2026; carried out the same day). No `gplsrc`, no
   `gplobj`, no `gplbld` under `C:\ProgramData\SD\`. The `$execute` pairs in
   `APISRVR` and `ERRTEXT` are commented out, `gplbld/gen_includes.py`
   regenerates the three derived include files at build time, and
   `SECOND.COMPILE` has been run clean with all three directories absent (§4).
   Two loose ends it left, neither blocking:

   - **`GPL.BP/OPGEN` is not ported** to `gen_includes.py`. It generates
     `GPL.BP/OPCODES.H` from `gplsrc/opcodes.h` and reads `./gplsrc` the same
     way the others did, but nothing ever `$execute`d it, so it breaks no
     compile — it simply cannot be run on an installed system any more. Port
     it before opcodes ever need regenerating, and verify byte for byte
     against the tracked `OPCODES.H`; its hex formatting is not obvious from
     the source (`OP.STOP` is commented `;* 00`, `OP.ABORT` `;* 1`).
   - **`WRITE_INSTALL_DICTS` reads `@sdsys:"/gplbld/FILES_DICTS"`.** It is an
     install step rather than part of a compile, so it did not affect the
     test, but it is the last thing wanting `gplbld` in the data tree and step
     3 has to deal with it.

   **Now the move itself**, which is what remains of this step.
   `<sysdir>/bin` holds the pcode library as well as the executables and must
   be **split, not moved** (§6): binaries to `C:\Program Files\SD\`,
   `pcode`/`pcode.old` stay with SDSYS.
2. **Fix `VALID_OS_PATH`** so it accepts backslashes and spaces. Not
   housekeeping: step 1 puts binaries under a path containing a space, and
   this rejects both. Widen the character set without weakening the shell
   metacharacter protection it exists to provide — quoting the path at the
   `OS.EXECUTE` site is the safer way to allow spaces.
3. **Build the staging script, then the Inno Setup installer** (§5.9). The
   `installsdai.sh` port is dropped; these two replace it, and this step
   absorbs what used to be step 9.

   a. **The staging script — first cut done**, `gplbld/stage.py`. It builds
      both install roots from an explicit whitelist, computes the MSYS2 DLL
      closure with `objdump -p` walked transitively, writes `sd.conf` and
      `etc\fstab`, and emits `MANIFEST.txt` so two builds can be diffed. The
      staged `sd.exe` runs with MSYS2 off PATH (§4). What it left open:

      - **The `ACCOUNTS/SDSYS` record ships `/usr/local/sdsys`** as the
        account path — a Linux path, which the staging script copies
        verbatim. It has to become the production path, and that decision is
        tied to whether the staged tree is pre-bootstrapped (below).
      - **`sdsys/BP` ships and holds test programs** (`sdTests`,
        `BIGSTR_TEST` and the like). Harmless, and the Linux install did the
        same, but decide whether an end user should get them. The `PY_*` ones
        went with §5.15.
      - **Consider pre-bootstrapping.** §5.9 says the installer stages
        pre-compiled artefacts, but the script stages `gcat`, `GPL.BP.OUT` and
        `PCODE.OUT` **empty**, which means the target still has to run the
        bootstrap. Running it on the build machine at the production path and
        staging the result would make the install a file copy — no Python, no
        compiler, nothing to fail half way — at the cost of fixing the data
        tree's location. Only `ACCOUNTS/SDSYS` embeds it, so the cost is
        small; a sweep of the live tree found nothing else.
      - **Nothing sets the ACLs yet**, and that is the step that makes the
        data private (§5.7). It belongs in the installer, not the staging.
   b. **Install from the staged tree onto a machine with no development
      tree.** This is the point of the exercise and it has **not** been done:
      the run above proves the binaries load, not that an install works. It is
      what finds anything depended on by accident, which is how `gplsrc`
      survived in the data tree for as long as it did.
   c. **The Inno Setup script**, `.iss` tracked in this repository, packaging
      that directory. The compiler is installed on this machine. The `icacls`
      step is the one that actually makes the data private (§5.7); nothing at
      runtime substitutes for it.
   d. **Decide what the uninstaller does with `C:\ProgramData\SD\`** before
      shipping one. It holds the user's database. Read `deletesdai.sh` for the
      current answer rather than porting it.

   **Set the SDSYS password last**, after the whole bootstrap has run. `LOGIN`
   admits an administrator to an account with no verifier yet, so every
   internal command in the sequence works while SDSYS has no credential, and
   nothing has to carry a password through the build. This is the whole of the
   install half of the batch-login question in §8; get the ordering wrong and
   it becomes a real problem instead of a non-problem.
4. **Add the audit log** (§5.6). The missing half of the identity model:
   access is controlled, nothing records who used it. Its own append-only file
   that rotates rather than truncates — *not* `<sysdir>/errlog`, which discards
   its oldest half on reaching the `ERRLOG` size. Records every login, every
   `LOGTO`, and every failed step-up, attributed to `@logname`. A failed
   step-up is the single most interesting line in the trail.
5. **Give grants a verb.** `ACC$USERS` can only be edited through
   `MODIFY ACCOUNTS` today. Decide the shape — `GRANT account TO account` and
   `REVOKE`, or a `SET.ACCESS` screen — and write the audit record from it.
6. **Bring the API server under the same model** — and it is more pressing
   than this position suggests, because §1 now says the API is the product's
   front door. **The API does not work on Windows at all**: `APISRVR` line 921
   calls `login(username, password)` → `login_user()` in `linuxio.c`, which
   with `APILOGIN=1` reads `/etc/shadow`, which MSYS2 does not have. It fails
   closed, which is the good version of broken, but it is broken. The shape of
   the work, in value order:

   a. **Authenticate against `$CRED` instead of the OS**, or drop the password
      check entirely in favour of peer identity — which of those depends on
      the exposure decision in §8. `!CRED_VERIFY` exists and is verified
      working (§4), so this is small.
   b. **Set `@logname` from what was verified**, not from the client. It comes
      from the client today (lines 900 and 963), which is what stops the grant
      check being copied across from `LOGTO`.
   c. **Apply the grant check to `SrvrAccount`** once (b) makes it meaningful.
   d. **Delete the `setuid`/`setgid` calls in `login_user()`.** SD accounts are
      not OS users under §5.6, and they are largely no-ops on MSYS2 anyway.
      They go with the rest of the OS-account work.

   `sdnet.h` still hardcodes `PASSWD_FILE_NAME "/etc/shadow"`, which is what
   that authentication used to be, and goes with (a).
7. **Put `SH` and `!` back** (§5.13). Shell access was disabled on Linux and
   that was a mistake; on Windows it stops programs reaching the utilities
   they need. Find what disabled it — a config option, a `K$SECURE` test, or a
   removed verb — and restore it deliberately.
8. **Make everything lower case that can be** (§5.12), folding in
   **`CASE_INSENSITIVE_FILE_SYSTEM`**, which is referenced at 9 sites in
   `dh_misc.c`, `dh_open.c`, `op_dio2.c` and `op_dio4.c` and defined nowhere.
   Windows filesystems *are* case insensitive, so that half is a correctness
   gap with the code already written. Do the case-insensitive comparisons
   first, or `sue` and `SUE` become different accounts.
9. **Let a scheduled job log in** (§8). The allowlist and the batch account
   that grants nobody. Not urgent — the install half of the problem is solved
   by ordering (step 3) — but it is what MV users expect and it needs no new
   C code. Build it against the constraints written into §8, particularly the
   no-arguments rule, which is the part doing the security work.
10. **Write the admin helpers** (§5.14). Forms over the administrative work
    that is command lines and hand-edited records today, once the system runs
    well enough to be worth using. The sequencing note matters more than the
    step: put administrative logic in subroutines from now on, so a form can
    call it later without reimplementing it.
11. **Exercise `SDConnectLocal()`** once a server runs. Needs the configuration
    file from §5.8, or `SD_CONFIG` set.
12. **Restore the BASIC layer's Windows branches** from the external `GPL.BP`
    tree (§5.4), then set `SYSTEM(91)` to 1 and assign `is_nt`. In that order:
    flipping the switches first would enable paths that are no longer present.
    Start with `CPROC`'s `dir.separator`, since compilation depends on it —
    and note that is now testable, since `sdrealpath()` accepts `\` (§5.8).
13. **Stage 2, native Win32.** `fork` → `CreateProcess` (all five call sites
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

### Open: how does a scheduled job log in, now that every account has a password?

Raised by the repository owner on 13 Aug 2026. Every account carries a password
(§5.6), and MV users expect to run work unattended — cron jobs, scheduled
tasks, and the `sd -internal SECOND.COMPILE` shape the install script uses. The
design below is the repository owner's; the constraints under it came out of
working through it and are recorded so they are not re-derived.

**The install case is not part of this and is already solved.** `LOGIN`'s
`authenticate.account` checks `$CRED` first and admits an administrator, with a
warning, to an account that has no verifier yet; `sd -i` never reaches `LOGIN`
at all. So an installer that runs the whole bootstrap and calls `SET.PASSWORD`
as its **last** step needs no credential during the build. That is an ordering
requirement on §7 step 3, not an open question.

**The design.** An `X`-type VOC item named `ALLOWED` in **SDSYS's** VOC, whose
lines are `ACCOUNT, VOC name` pairs. `LOGIN` consults it: the account to enter
comes from the list, and so does the command that may run. Because the item
lives in SDSYS, only an administrator can add to it — but the job runs in the
named account, so **nothing runs with administrator rights**; SDSYS is the
storage location for the policy, not the context it executes in.

Paired with it: **a dedicated batch account that grants nobody.** An account
with an empty `ACC$USERS` is already refused to everyone, and SDSYS already
reaches every account without a grant, so only the administrator can enter it
to edit its VOC or recompile its BP programs. Both halves of that are existing,
observed behaviour (§4) — this is a deployment convention, not a new mechanism,
which is its main virtue. `KIM` on the current test machine is already this
shape.

**The mechanism exists.** `SYSTEM(1026)` returns the command from the command
line (`op_sys.c`, case 1026, from `single_command` in `sd.c`), and `CPROC` does
not pick it up until line 556, so `LOGIN` can read it and decide before
authenticating. No new C code is needed.

**Constraints to build to.**

- **One token, no arguments, and enforce it.** This is what does the actual
  security work, not "must be in VOC" — every verb is a VOC item (`COPY` is a
  `CA` entry for `$COPY`, `LIST` is `CA` for `$QPROC`), so requiring VOC
  membership excludes almost nothing. With no arguments a verb entry is
  useless and only a paragraph is worth listing. Reject a command with
  anything after the first word.
- **Accept only `PA` and `S` VOC types** when the list is consulted, so a
  mislisted verb fails when the administrator sets it up rather than spinning
  on a prompt at 3am.
- **Any prompt must be fatal in this mode.** A scripted session that reaches an
  unanswered prompt spins at full CPU (§6).
- **The name must be unique across the list**, or `-A` must be present and
  match. `-A` naming a different account is a refusal, never a silent override.
- **Set `@logname` explicitly** so the audit record reads as an allowlist entry
  rather than as a login. Attribution is the point of §5.6 and an unattended
  job has no person behind it.
- **Catalogue batch programs locally**, not globally, so they do not appear in
  `gcat` and become runnable from every account.

**What was rejected, and why, so it is not proposed again.**

- **A password on the command line.** Command lines are readable by any local
  user through Task Manager, `Get-CimInstance Win32_Process` and ETW.
- **A password file** works today — `cat pw | sd -ABATCH CMD`, and note `<`
  redirection does not (§6) — and an ssh-style refusal to use a file with a
  loose ACL would make it defensible. It was passed over because a capability
  list is better than a stored credential in two ways: there is no secret to
  leak or rotate, and a stolen credential grants an *interactive session*
  while a list grants only a fixed set of commands.
- **Hashing the VOC entry to detect tampering** pins one hop and no further: a
  paragraph reading `RUN BP NIGHTLY` can be pinned, but `BP NIGHTLY` cannot,
  and a transitive closure discovered at run time cannot be hashed at all.
  Storing the command text in the list rather than a name to look up gets the
  same protection for nothing — the approved thing and the executed thing
  become the same object. Whether the list holds a name or the command text is
  still to decide.

**What this depends on, and what it does not fix.**

- **The batch account is the one account where per-directory ACLs work in
  stage 1.** §5.7's dilemma — grant every SD user access to every account, or
  duplicate the password gate in ACLs — exists because a user's own process
  must read the files of any account they enter. No ordinary user is ever
  meant to run in the batch account, so there is exactly one principal to
  grant: whatever the scheduled task runs as, plus `Administrators`. An
  `icacls` on that directory closes the tampering gap properly, today, with no
  stage 2 dependency. Fold it into §5.9's ACL step.
- **The account boundary is not a data boundary.** `ACC$USERS` gates `LOGTO`,
  not file opens, so a Q-pointer in the batch account's VOC reaches another
  account's files with no grant at all. "Runs without administrator rights" is
  true and worth having; it is not a sandbox. Every grant added to let a job
  reach real data widens what a compromised batch account reaches.
- **Still open: who may trigger it.** The list says what may run unattended,
  not who may fire it, so any local user who can run `sd.exe` can start a
  listed job. With the batch account ACL'd away from them that is a matter of
  causing a job to run at the wrong time rather than of reading or altering
  anything — tolerable, but it argues for listing only work that is safe to
  trigger and ideally idempotent. An optional third column naming an OS
  principal is the escape hatch if that is not enough.

### Open: how should the API be exposed? (raised 13 Aug 2026)

Background from the repository owner: OpenQM was very insecure and **remote
access was the worst of it**. Telnet was removed and replaced with ssh only;
the API never got the same treatment. §1 now makes the API the product's front
door, so this is the security question that matters most.

**Where it actually stands** — see the trap in §6 and the correction in §5.6.
The API has a connect-time credential check that cannot succeed on Windows, so
it is closed rather than open. That buys time; it does not buy a design.

**Three postures, and they are not ranked.**

| | What faces the network | SD's own network exposure |
|---|---|---|
| **A** | SD's own socket, as shipped | full, and it is 2007 code |
| **B** | ssh tunnel or VPN; SD is local only | none |
| **C** | a web front end; SD is local only behind it | none |

**B is what the repository owner already did to OpenQM**, and it carries to
Windows unchanged — OpenSSH ships as a Windows optional feature and port
forwarding works. It is the conservative answer and costs nothing new.

**C was the repository owner's idea**, and its merit is that it makes the
*simplest* API authentication the correct one rather than forcing a bigger one.
If the only client is one local process, a **named pipe whose ACL admits
exactly one principal** — an IIS app pool virtual account, or a Kestrel service
account — is a stronger statement than any credential that client could
present. No `$CRED` check in the API path, no TLS in SD, no certificate story.
That is less code, not more. It is also the one case where Windows ACLs work
cleanly, for the same reason as the batch account above: one principal to
grant, so §5.7's dilemma never arises.

**The argument against C, and it is a serious one** (repository owner,
13 Aug 2026): web servers invite attack. Every hacker knows how to attack one,
scanning is constant and automated, and a custom protocol on a non-standard
port simply does not attract the same volume. Obscurity is not security, but it
is a real reduction in *opportunistic* attack traffic, and a web tier is a
whole additional codebase and patching burden. **This is recorded as an option
to be convinced of, not a decision.**

The honest counter is that C does not *add* network exposure, it *moves* it:
the comparison is not "web server versus nothing" but "IIS exposed versus
`APISRVR` exposed", and `APISRVR` is 2007 Ladybridge code with fixed 32-byte
credential buffers that nobody has ever fuzzed. Obscurity cuts both ways —
fewer people attack it, and fewer people have found its bugs. But that argument
favours C only over **A**. Against **B** it has no force at all, because B
exposes nothing either.

**Which is worth noticing: §1 points at B.** If the target user is a Windows
developer using SD as a back end, *their* application is the front end, and it
sits on the same machine or reaches SD over a tunnel. SD does not need to ship
a web tier to be secure — it needs to stop listening on the network. A web
front end is then a **product** decision, about whether SD offers a browser UI,
rather than a security mechanism. Keeping those two questions apart is probably
what makes this decidable.

**The network-layer argument, and it is the strongest one for B** (repository
owner, 13 Aug 2026). A private API can be put behind controls that run *before
a byte reaches SD* — VPN, a Windows Firewall rule scoped by remote address or
interface, or IPsec Connection Security Rules, which can require the peer to be
an authenticated domain machine without a line of application code. A public
web server forfeits all of it by definition: if it is public, anyone may reach
it.

The sharper form of that, which is structural rather than obscurity: **a public
web application must accept anonymous connections as far as the login page.**
Its TLS termination, HTTP parser, router, session handling, login form,
password reset and static file serving are all reachable pre-authentication, by
everyone, by design. An IP-restricted API has a pre-authentication surface
reachable by nobody. That is a real difference in kind.

**The refinement that keeps this honest, so it is not read as "web is
insecure":** the axis is *public versus private*, not web versus API. A web
front end on an internal network behind the same VPN keeps every one of those
controls. Deployed privately, C's security cost over B is a second codebase to
patch, and its benefit is a browser UI — which is the product question again,
not a security one.

**Where these controls have to live, and nothing does it yet.** SD never binds
a listening socket. `sd -N` runs per connection with the socket as stdin and
stdout; **xinetd** bound port 4243, spawned an instance per connection and
supplied `only_from`. xinetd does not exist on Windows, so the service that
replaces it inherits all four responsibilities, and none of them are
implemented. Two consequences:

- **Make it bind to loopback by default**, so posture B is what you get without
  anyone deciding anything, and listening more widely takes a deliberate act.
- `only_from` has no Windows equivalent unless the replacement implements it or
  the install writes a Windows Firewall rule. Decide which; a firewall rule is
  less code and easier to audit.

These are the deployer's controls rather than SD's, so they are reasons to
permit a posture, not a substitute for SD's own authentication (§7 step 6).
Both, not either.

**Two things that apply to B and C alike.**

- **Attribution has to survive the extra hop.** If a front end is the only
  client, every SD session carries *its* identity and `@logname` stops naming a
  person — which destroys what §5.6 is for. The workable split is that the
  front end **asserts identity** (trusted because of the pipe ACL) and SD still
  **enforces authorisation**, checking the target account's `ACC$USERS` itself.
  The grant list stays where it can be audited, and the front end never becomes
  the authorisation authority. Same shape as the batch-login conclusion above:
  an asserted capability, not a shared secret. The cost to accept consciously
  is that compromising the front end compromises attribution entirely.
- **Connection pooling breaks identity, and this is not about `NUMUSERS`.**
  A pooled connection reused across users breaks both `@logname` and account
  isolation, so it needs a session per user or a `LOGTO` with the identity
  reset per request. Note `NUMUSERS=20` in `sd.conf` is only a default —
  OpenQM systems run several hundred users — so the ceiling is a tuning
  question, but the identity problem is not, and retrofitting it is painful.

**What this makes more valuable than its position suggests.**
`SDConnectLocal()` becomes the production entry point under either B or C
rather than a curiosity, and it has never been run (§4). The client DLL is
already the right shape for it: native UCRT64, and confirmed this session to
depend on nothing but Windows system DLLs, so a .NET or native client can use
it with no MSYS2 runtime anywhere in the client tier. That separation was made
for a different reason (§5.3) and happens to be exactly what this needs.

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
