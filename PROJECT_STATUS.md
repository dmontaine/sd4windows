# PROJECT STATUS

Living handoff document for the SD Windows port. This project moves between
sessions, machines and accounts; anything not written here is lost. Read this
file first. Read [HISTORY.md](HISTORY.md) only if you need the record of how
something came to be the way it is.

**Last updated:** 13 Aug 2026 · **describes the tree as of commit** `9c00730`
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

Checklist before you end a session:

- [ ] §3 Current state matches what is actually in the tree
- [ ] §4 Verified / Unverified is honest, and nothing was promoted without evidence
- [ ] §6 Traps gained anything that cost you real time
- [ ] §7 Next steps reordered, with anything finished removed
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

**An earlier report of `sd -i` "blocking silently" was wrong**, and the cause
is worth knowing — see the stale record lock trap in §6. It was self-inflicted
by killing earlier runs.

**The blocker behind that.** `IS_GRP_MEMBER` reads `/etc/group`, which does not
exist under MSYS2, so the `sdusers` test at `LOGIN` 193 refuses every
connection. See §6. Under §5.6 the fix is to delete those calls rather than
repair them, so this and the account password work land together. Note it may
not be reached yet — pass 1 runs `$BBPROC`, not `LOGIN`.

**State of the machine as this was written.** SD is started and `sdlnxd` is
running, from a probe binary built with `-DSD_ADMIN_GROUP='"Users"'` (§6). The
shared segment and semaphores are live in `/dev/shm`. A stray `sdprobe` from a
killed run may need `pkill -f sdprobe`. Stopping and restarting SD needs the
probe too, since `-start` and `-stop` both call `check_admin()`.

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

### Not verified — treat as unknown

- **Bootstrap pass 1 has never completed.** `sd -i` attaches and then blocks
  silently (§3). Everything past it in the bootstrap sequence is untried.
- Semaphore locking under contention. The semaphores have never been observed
  held, so the `sdsem.c` port is exercised only in the uncontended case.
- `SDConnectLocal()` at runtime. It needs a running server and a configuration
  file (§5.8).
- **Anything requiring a second user, or contention.** Everything so far is one
  process at a time. Record locking between real users, `SDConnectLocal()`, and
  the API server path are all untried.
- Writing and reading application data. The bootstrap creates and reads system
  files; no user account has been created and no user data written.
- The installer. `installsdai.sh` is still entirely Linux.
- **The shipped binary.** Everything was run with the probe build overriding
  `SD_ADMIN_GROUP` to `Users`. `bin/sd.exe` differs only in that constant, but
  has not been exercised.
- **Anything about `sd -start` in the shipped binary.** All of the above was
  observed with a probe build overriding `SD_ADMIN_GROUP` to `Users` (§6),
  because the token still lacks `sdadmins`. The admin check is the only
  difference between that binary and `bin/sd.exe`, but it has not been
  confirmed by running the real one.

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

**What has to be built.**

- **The credential register goes in a separate file, not in the ACCOUNTS
  record.** One entry per account, holding its salt and verifier.
  `LOGIN` opens `ACCOUNTS` at line 175, in the user's own process, before any
  authentication — it must, to know the account exists — and eleven other
  programs open it too, including `_VOC_REF` for routine resolution. So every
  SD user's process can read it. Verifiers stored there would let any user pull
  every account's Argon2 hash and attack it offline. Use a separate register
  keyed by account name holding only salt and verifier. In stage 1 that file is
  still readable by everyone (Windows has no setuid, and there is no privileged
  helper short of §5.7's service), so this does not fix the exposure — it makes
  the boundary exist, so §5.7 can lock one file to the service account without
  restructuring ACCOUNTS or migrating data.
- `ACC$GROUP` becomes dead. The remaining ACCOUNTS fields are unchanged.
- Neither entry path prompts. `int.logto` (`CPROC` around line 2451) goes
  straight from account name to a `system(27) > 0` test to `is_grp_member` to
  `chdir`; `sd -A` at `LOGIN` around line 207 does the same. Both need the
  prompt, and both currently refuse SDSYS unconditionally on Windows because
  `system(27)` is never zero (§5.5).
- **The password is asked for at login, and again on `LOGTO SDSYS`.** Every
  other `LOGTO` tests the grant on the target account and writes the audit
  record without prompting. Give one failure message for an unknown account
  name and a bad password alike, and keep the existing three-tries-and-`sleep`
  behaviour.
- `is_grp_member` calls are removed rather than fixed — `LOGIN` 193 and 224,
  `CPROC` 2507, `APISRVR` 359, 914 and 961, `CREATEA` 323, `MODIFYA` 96, 99
  and 125. This also disposes of the `/etc/group` blocker in §6 rather than
  requiring it be repaired.
- **Done 13 Aug 2026: the privilege tests ask the administrator flag.**
  `BBPROC`, `CATALOG`'s `CATALOG GLOBAL` and `CPROC`'s `LOGTO SDSYS` use
  `not(kernel(K$ADMINISTRATOR, -1))`. `WRITE_INSTALL_DICTS` uses
  `not(SYSTEM(1050))` instead, because `KERNEL` is only available to
  `$internal` programs and it is not one — `SYSTEM(1050)` reports the same
  `USR_ADMIN` flag (`op_sys.c` case 1050) and is the public accessor. Use it
  for any non-internal program. `SYSTEM(27)` keeps meaning "uid", which on
  Windows is simply not a privilege answer.
- **Done 13 Aug 2026: the `is_grp_member` calls are gone** from `LOGIN`,
  `CPROC` and `APISRVR`, along with their now-dead `deffun` declarations. That
  removed both the `sdusers` login gate and the `ACC$GROUP` account gate.
  **Nothing now restricts entry to any account** — that is the intended
  interim state, but it means the system is open until the credential model
  lands, and it should not be exposed to anything until then.

  The calls in `CREATEA` (line 323) and `MODIFYA` (96, 99, 125) were
  deliberately left. They guard `OS.EXECUTE` calls to `useradd`, `usermod` and
  `groupadd`; removing only the guard would let those shell-outs run
  unconditionally, which is worse than leaving them. They go when the OS
  account commands go, as one change.

  For those tests to mean anything, `kernel.c` now seeds `USR_ADMIN` from
  `IsAdmin()` when the user table entry is initialised. Previously nothing set
  the flag on Windows — `CPROC` only set it inside its `system(27) = 0` branch,
  which never runs — so `K$ADMINISTRATOR` answered "no" for everybody. This is
  an interim arrangement that keeps the OS group as the source; when the
  credential model lands, SDSYS entry becomes the thing that sets it.

  `CPROC`'s `system(27) = 0` "entered as root?" branch at line 272 was left
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
| SDSYS, database, accounts | `C:\ProgramData\SD\` | `/usr/local/sdsys` |
| Configuration | `C:\ProgramData\SD\sd.conf` | `/etc/sd.conf` |

`ProgramData` is the correct home for machine-wide mutable state, and it has no
space in its name, which sidesteps the `VALID_OS_PATH` trap (§6) for a default
install. `Program Files` does contain a space, so binaries are on the wrong
side of that trap and it must be fixed regardless.

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

**Sequencing note.** MSYS2 accepts `C:/ProgramData/SD/sdsys` with forward
slashes throughout, so stage 1 can move to the correct *location* while keeping
`/` as the separator. That decouples this work from the `@ds` /
`dir.separator` question (§6), which is load-bearing for compilation and should
not be disturbed at the same time.

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
- **They remain in git history**, so a clone still fetches them and the audit
  goal is only half met. Purging them needs a history rewrite and a force push,
  which is destructive to anything already cloned; it was deliberately not done
  without asking. See §8.

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

1. **Build the account credential model** (§5.6). This is now the critical
   path, and it is urgent rather than merely next: removing the
   `is_grp_member` gates left nothing restricting entry to any account. Build
   the credential register as a separate file, prompt for name and password at
   login, prompt again on `LOGTO SDSYS`, set `K$ADMINISTRATOR` on SDSYS entry,
   and close the `op_kernel.c` set hole. The bootstrap now runs, so this is
   testable end to end for the first time.
2. **Implement the account credential model** (§5.6). Build the credential
   register as a separate file — one entry per account, listing each permitted
   person with salt and verifier — and prompt for name and password in
   `int.logto` and the `sd -A` path, setting `@logname` from the credential that
   succeeded. Remove every `is_grp_member` call, set `K$ADMINISTRATOR` on SDSYS
   entry and point `CPROC` and `CATALOG` at it instead of `SYSTEM(27)`. Close
   the `K$ADMINISTRATOR` set hole in `op_kernel.c` at the same time, or the gate
   is decorative. Cannot be tested until step 1 lands (§6).
3. **Move to the Windows install layout** (§5.8). Relocate to
   `C:\Program Files\SD\` and `C:\ProgramData\SD\`, unify the server and client
   configuration variable, drop the `sd.ini`-in-`C:\Windows` fallback. Keep `/`
   as the separator for now so this does not disturb `@ds` (§6).
4. **Fix `VALID_OS_PATH`** so it accepts backslashes and spaces. Now mandatory
   rather than cheap housekeeping, because step 3 puts binaries under a path
   containing a space. Widen the character set without weakening the shell
   metacharacter protection it exists to provide — quoting the path at the
   `OS.EXECUTE` site is the safer way to allow spaces.
5. **Add the audit log** (§5.6). Its own append-only file that rotates rather
   than truncates — *not* `<sysdir>/errlog`, which discards its oldest half on
   reaching the `ERRLOG` size. Records every login, every `LOGTO` and every
   failed attempt, attributed to the login identity.
6. **Write the Inno Setup installer** (§5.9), replacing `installsdai.sh`. The
   ACL step is the one that actually makes the data private; nothing at runtime
   substitutes for it.
7. **Enable `CASE_INSENSITIVE_FILE_SYSTEM`.** Referenced at 9 sites in
   `dh_misc.c`, `dh_open.c`, `op_dio2.c`, `op_dio4.c` but never defined
   anywhere. Windows filesystems *are* case insensitive, so this is a
   correctness gap and the code is already written.
8. **Exercise `SDConnectLocal()`** once a server runs. Needs the configuration
   file from §5.8, or `SD_CONFIG` set.
9. **Restore the BASIC layer's Windows branches** from the external `GPL.BP`
   tree (§5.4), then set `SYSTEM(91)` to 1 and assign `is_nt`. In that order:
   flipping the switches first would enable paths that are no longer present.
   Start with `CPROC`'s `dir.separator`, since compilation depends on it.
10. **Stage 2, native Win32.** `fork` → `CreateProcess` (all five call sites
    are fork+exec, none need copy-on-write, so this is tractable), `termios` →
    Console API, passwd/group → Windows authentication. **The service-account
    model in §5.7 belongs here**, and until it lands the data tree is not
    genuinely private from SD's own users.

## 8. Open questions

The identity question that stood here — admin flag inside SD, or OS group — was
**answered on 13 Aug 2026** and is now §5.6. Neither option was taken. See the
HISTORY entry "Identity, install layout and data protection decided" for the
reasoning and for the corrections to the evidence that was recorded here.

### Open: purge the binaries from git history?

§5.11 untracked the eight binaries, so no future commit carries one. But every
commit up to and including `5c09f0f` still contains them, so a clone still
fetches roughly 3 MB of unauditable object code. If the goal is that nothing
binary is in the repository, the history has to be rewritten — `git filter-repo`
or equivalent, followed by a force push.

That was deliberately **not** done without asking, because it rewrites published
history: every existing clone diverges and has to be re-cloned or reset, and
commit hashes referenced elsewhere (including in HISTORY.md) stop resolving.
Given the project's own record keeping quotes hashes, that cost is real.

Options, in rough order of disruption: leave history alone and treat the policy
as forward-only; rewrite and force push, accepting the churn while the project
is still single-developer; or start a fresh repository from the current tree and
archive the old one. The middle option is cheapest *now* and gets more expensive
with every clone that exists.

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
can be deleted once nothing references it.

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
