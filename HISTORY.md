# HISTORY

Append-only record for the SD Windows port. This is the overflow and archive
for [PROJECT_STATUS.md](PROJECT_STATUS.md), which holds only what a new session
needs to act on today.

Read this when you need to know *why* something is the way it is, whether an
approach has already been tried, or whether a claim in PROJECT_STATUS was ever
corrected.

---

## Rules

1. **Append-only. Never delete or rewrite an entry.** If an entry turns out to
   be wrong, add a new entry that says so and references it by date and
   heading. The wrong turn is part of the record; erasing it invites a repeat.
2. **Newest first.** New entries go directly below this rules block.
3. **Every entry carries an absolute date and the commits it covers.** Never
   "today" or "last session".
4. **Entries are written to be read cold**, by someone with no memory of the
   session, possibly on another account. Spell out names and paths.
5. **Corrections get their own entry**, headed `Correction:`. This is how a
   future session learns that a confident earlier claim was wrong.
6. Suggested shape, not mandatory: what changed, why, what it cost, what is
   still open.

---

## 13 Aug 2026 — Surveyed every BASIC to C linkage

**Commits:** documentation only; no code changed. Follows the GPL.BP survey
below, which covered platform detection only.

Interfaces enumerated and checked: `SYSTEM(n)` (19 keys in use), `OSPATH()`
(15 keys), `KERNEL()` (around 120 keys), `SDEXT`, `OS.EXECUTE` (10 files), and
the compiler chain.

**The privilege model is the serious finding, and it is not a detection
problem.** `IsAdmin()` in `linuxlb.c` is `return (getuid() == 0)`, and
`SYSTEM(27)` returns `getuid()` unchanged. `getuid()` under MSYS2 was measured
at 197609, and Windows has no uid 0 at all — administrator there is a token
privilege. So every privilege test answers the same way permanently, and
nothing errors:

- `CPROC` — `new.account = "SDSYS" and system(27) > 0` is always true, so
  **SDSYS access is always denied**
- `CATALOG` — `system(27) # 0` guarding `CATALOG GLOBAL` is always true, so
  **global cataloguing is always denied**, which reaches into the compile
  workflow and not just administration
- `CPROC` — the `system(27) = 0` "entered as root?" branch never runs, so the
  drop to `sdsys` via `EUID_SET` never happens
- `K$ADMINISTRATOR` in `op_kernel.c` consults `IsAdmin()` and so is never
  granted implicitly

`EUID_SET`/`EUID_RESTORE` reach `sdext_eguid.c` through `SDEXT` and call
`getpwnam`, `setegid` and `seteuid`. Native Windows has no equivalent;
impersonation is `LogonUser` plus `ImpersonateLoggedOnUser`.

The useful part is that this concentrates: everything routes through
`IsAdmin()` or `SYSTEM(27)`, so one decision about what "administrator" means
on Windows and one function body covers it. Recorded as next step 4.

**`VALID_OS_NAME` undoes a documented Windows fix.** It rejects spaces in user
names, and both `ADMUSER` and `CREATEU` in the external tree carry the line
"15 Apr 05 2.1-12 Allow spaces in user names for Windows compatibility". A
2005 change made deliberately for Windows was removed by the cleaning cycles
twenty-one years later. Called from `CREATEA` and `APISRVR`. This is the second
instance of that pattern after `VALID_OS_PATH`, which is enough to treat it as
a class rather than a coincidence.

**`PLATFORM_NAME` reaches the compiler.** It is `"Linux"` in `sddefs.h`,
returned by `SYSTEM(1010)`, and `BCOMP` does
`add 'SD.':upcase(system(1010)) to defined.tokens` — so the BASIC compiler
defines the token `SD.LINUX`. The external tree does the same with `QM.`.
Nothing tests the token in either tree, so it is latent rather than broken, but
any BASIC source asking `SYSTEM(1010)` is told "Linux".

Surveyed but not yet examined in detail: the 15 `OSPATH` keys in `op_dio2.c`
(all path semantics, including `OS$FULLPATH`, documented as "Return full DOS
file name"), and the platform sensitive `KERNEL` keys (`K$SETUID`, `K$SETGID`,
`K$USERS.UID`, `K$IN.GROUP`, `K$TTY`, `K$RUNEXE`, `K$INIPATH`). `OS_CHOWN` is
an SD addition called from `CATALOG` with no Windows meaning.

Everything else checked is platform neutral: terminal type, endianness,
version, times, queue and select state, and the compiler chain apart from `@ds`
and the token above.

PROJECT_STATUS passed 400 lines during this update and was rolled over per its
own rule: §5.1 and §5.2 were merged and shortened, since the full reasoning
already lives in the entry below, and §5 was renumbered.

---

## 13 Aug 2026 — Surveyed the BASIC layer (GPL.BP) for platform code

**Commits:** documentation only; no code changed.

Context supplied by the repository owner: `sdb64` is the active project, and
this tree is an experimental variant that has been through five major AI
cleaning and validation cycles — which is why the code reads more cleanly than
its age suggests. The original ScarletDME BASIC source was made available at
`C:\Users\dmont\Projects\GPL.BP` for comparison, on the basis that the C code
and the BASIC code work together for things like compilation.

**The BASIC layer has a platform switch that nothing had looked at.** Two
SYSTEM keys are the whole bridge between the C code and the BASIC source:
`SYSTEM(91)` ("is this Windows") is hardcoded to zero in `op_sys.c`, and
`SYSTEM(1006)` ("Windows NT style") returns `is_nt`, which `kernel.h` declares
`init(FALSE)` and which is never assigned anywhere. Both answer "not Windows",
so every Windows path in the BASIC layer is dead code. `is_nt` is dormant in
exactly the way `CASE_INSENSITIVE_FILE_SYSTEM` is.

**Unlike the C reference tree, the external GPL.BP is a real asset.** It holds
Windows logic in 21 files against 6 here, and every file present in both trees
lost all of it: `LOGIN` went from 16 references to none, `CONFIG` 5 to none,
`CPROC` 5 to none, `CREATEA` 4 to none, `PARSER` 3 to none. Details of what
each did are in PROJECT_STATUS §5.5. This is the opposite of the finding for
the C tree, where the Windows code was genuinely gone and only comments
remained.

**`@ds` turned out to be load-bearing for compilation**, which is the
connection the owner pointed at. `BCOMP` opens `@sdsys:@ds:'bin'` and builds
source paths with it; `BASIC` builds its source and output paths the same way.
It is SYSCOM slot 57, fed from `dir.separator`, which the original set as
`if windows then '\' else '/'` and which `CPROC` here hardcodes to `'/'`.
Correct on the MSYS2 runtime, and a live question for stage 2.

**One Windows blocker was introduced by the cleaning cycles, not inherited.**
`VALID_OS_PATH` does not exist in the external tree; it is dated 2026/06/10 in
this one. Its permitted character set omits the backslash and it rejects spaces
as shell metacharacters, so it rejects `C:\SD\accounts` and everything under
`C:\Program Files`. It guards `CREATEA` (account creation) and `PY_RUNFILE`.
Worth recording as a caution: the cleaning cycles can introduce Windows
problems as readily as they remove clutter, so "the original did not have this"
is not a safe assumption in either direction.

Smaller Linux remnants: `/tmp/api_srvr.log` and `/tmp/bbproc.log` in `APISRVR`
and `BBPROC`, and `sudo chmod g+s` in `CREATEA`. `OS_CHOWN` is implemented in
`op_dio2.c` and called from `CATALOG` via `ospath()`; it has no meaning on
Windows. The BASIC compiler itself (`BCOMP`, `ACOMP`) carries no platform
branches in either tree beyond the `@ds` use above.

Nothing was changed. The ordering constraint is recorded in PROJECT_STATUS §7:
restore the BASIC branches first, flip the SYSTEM keys second, because doing it
the other way enables paths that are no longer there.

---

## 13 Aug 2026 — Client library replaced with the vendored winsdclilib port

**Commit:** `202b965`

Vendored `github.com/dmontaine/winsdclilib` at `b6624565cacb365d0a2788545495a7fa3ba3f743`
(5 Aug 2026) into `gplsrc/sdclilib/`, replacing `gplsrc/sdclilib.c`.

**Why it was safe.** `sdclilib` is not listed in `gpl.src`, so it was never
linked into the server — it only ever produced the shared library. Replacing it
could not destabilise the server work.

**Why it is better.** No longer the partial Visual Studio port described by the
stale snapshot that used to sit in `examples/windows.c/winsdclilib/`. It
combines the complete Linux client behaviour with a Winsock transport and
carries fixes the old code lacks: an index-buffer overflow, `realloc` ordering
on a failed grow, short sends, malformed response lengths, and abandoning a
connection whose stream can no longer be trusted. Verified by building rather
than trusting the README — zero warnings under `-Wall -Wextra -Wpedantic`, both
bundled test suites pass.

**Why its own directory.** Its `sdclient.h`, `err.h` and `revstamp.h` are
different files from the ones in `gplsrc`. `revstamp.h` feeds
`MAJOR_REV`/`MINOR_REV`/`BUILD` into `SYSSEG_REVSTAMP` in `sysseg.c`, which
stamps the shared memory segment. Flattening the layout would have displaced
the server's copy.

**`SDConnectLocal` restored.** Absent upstream because that project targets a
Windows client talking to a *remote Linux* server, where a local connection has
no meaning — the user identified this, and it is correct. It matters again now
the server runs on Windows, and the Python wrapper binds it. Modelled on
`gplsrc/sdclient.c:666`: named pipe, `CreateProcess` of `sd.exe -Q -C <pipe>`,
`ConnectNamedPipe`, then `SrvrLocalLogin` and `SrvrAccount`. Two deliberate
improvements on that original — `ERROR_PIPE_CONNECTED` treated as success
rather than failure, and the process handle closed as well as the thread handle
(the original leaked it). Supporting it needed `sysdir()` and a transport layer
(`transport_recv`/`transport_send`/`transport_live`/`transport_error`) so
packet I/O works over socket or pipe. Upstream's error handling and connection
abandonment were left untouched; only byte moving is dispatched.

**Also fixed.** `sdclilib` and `terminfo` both needed `.PHONY`: neither names a
file and `VPATH` covers `gplsrc`, so make found the directories and considered
the targets satisfied. This is why an earlier session saw `terminfo` report "is
up to date" for something it had never built.

**Removed.** The stale `examples/windows.c/winsdclilib/` snapshot, and the
`sdclilib.so`/`libsdcli.so` pair built from the old client.

**Still open.** `SDConnectLocal` has never run. It needs a live server and an
`sd.ini`.

---

## 13 Aug 2026 — Correction: the `O_BINARY` override was not corrupting data

**Commit:** `202b965`

An earlier claim in this session's reporting — that hardcoding `O_BINARY` to
zero meant SD was writing binary files in text mode and corrupting them — was
**wrong**, and was stated with more confidence than the evidence supported.

On finding the same override a second time in `sdtic.c` (which does not include
`sddefs.h` and so carries its own copy), the prediction was that the 99
generated terminfo files were corrupted. Tested by regenerating
them with and without the correction: **byte identical**. The MSYS2 runtime
opens files in binary mode by default, so discarding the flag changes nothing
there.

The `#ifndef` guards in `sddefs.h` and `sdtic.c` are kept because they are
correct and will matter for stage 2, where the native Windows CRT defaults to
text mode. Both source comments were rewritten to say this plainly instead of
implying an active bug.

**Lesson worth keeping:** the compiler warning was real and worth chasing; the
conclusion drawn from it was not verified before being asserted. Regenerating
the artifact and comparing bytes took under a minute.

---

## 13 Aug 2026 — Removed superseded Linux artifacts

**Commit:** `3b4600e`

Deleted the six Linux ELF binaries in `bin/` (superseded by the `.exe` builds),
and `pcode_bld.log`, `pass1`, `pass2` — pcode build scratch. `pass1` and
`pass2` are byte identical and are written by the `pass1()`/`pass2()` stages of
`gplbld/bbcmp.py`.

Untracked but kept on disk: `terminfo/`, all 99 files of which are generated by
the `terminfo` make target. Verified by deleting the directory and rebuilding
before committing to the change.

Tracked files went from 3,446 to 3,255.

**Kept deliberately**, despite having no function on Windows: `usr/lib/systemd/`
and `etc/xinetd.d/`. They document the service topology a Windows service must
reproduce. Also kept: `installsdai.sh` and `deletesdai.sh`, which are the
targets of the port rather than obsolete output.

---

## 13 Aug 2026 — First native Windows build

**Commit:** `143c959`

All six binaries compile, link and run as native PE32+ executables for the
first time.

**The central problem.** MSYS2 ships the genuine Cygwin `sys/shm.h`, so SD's
System V IPC code compiled and linked without a warning and would have failed
at runtime with ENOSYS. Found by compiling and *running* probe programs rather
than checking for headers — which is the only reason it surfaced in minutes
instead of during a confusing debugging session later. MSYS2 has no
`cygserver`, so there is no way to enable System V IPC.

POSIX named shared memory and named semaphores do work, so:

- `sysseg.c` — `shmget`/`shmat`/`shmdt` → `shm_open`/`ftruncate`/`mmap`/`munmap`
- `sdsem.c` — `semget`/`semop`/`semctl` → `sem_open`/`sem_trywait`/`sem_post`
- `sdidx.c`, `sdlnxd.c` — their own copies of the attach code

Two places needed more than substitution: `munmap` must be told the mapping
length that `shmdt` derived from the address, and `stop_sd()` waited on the
System V attach count, which POSIX shared memory does not expose. It now polls
the user table with `kill(pid, 0)`, which also catches a process that died
without clearing its own entry.

**Other platform fixes.** `O_ASYNC` has no equivalent — verified first that
`keyin()` and `keyboard_pending()` test stdin with `sdpoll()` independently, so
input still works without SIGIO. `environ` was remapped to glibc's internal
`__environ`. `linux/limits.h` → `limits.h` in four files. `sdclient.c:127` read
`SDnclude <io.h>`, corrupted by the `qm`→`sd` rename; the upstream GPL source
has a clean `#include`.

**Build.** Libraries had to move after the objects that reference them, since
the PE/COFF linker resolves strictly left to right; ELF had masked this with
`-Wl,--no-as-needed`. Dropped `-DLINUX` (never tested for anywhere in the
source), `-fPIE` (the default here) and `-soname` (no PE equivalent — replaced
by an import library). libsodium is not packaged for the MSYS2 runtime and is
built from source into `/usr/local`.

**Two premises that turned out to be wrong**, both worth recording:

- *"gcc is on this computer under C:\msys64."* MSYS2 was installed but
  contained no toolchain at all — `mingw64/bin` was empty and there was no
  `gcc.exe` or `make.exe` anywhere. It had never been run; pacman performed
  first-time setup on first invocation. Everything in PROJECT_STATUS §2 was
  installed during this work.
- *"Many files in gplsrc still contain Windows code."* They do not. Of ten
  files matching Windows API idioms, nine matched only on comments or on
  `BOOL`/`SOCKET`, which are the project's own typedefs. Only `qmclient.c`
  holds real Windows code, and it includes `windows.h` unconditionally — it was
  always the Windows client, not stripped server code. The reference tree's
  value is archaeology: in `op_kernel.c`, both there and in this repository, a
  `/* Construct command for CreateProcess */` comment sits directly above a
  `fork()` call in `op_phantom()`, marking where Windows code used to be.

  The reference tree is a separate checkout at `C:\Users\dmont\Projects\gplsrc`
  and is not part of this repository.

**The finding that most de-risked the port:** all five `fork()` call sites are
fork+exec, none rely on copy-on-write semantics. The usual "cannot port this to
Windows because of `fork`" obstacle does not apply.

---

## 13 Aug 2026 — Repository created

**Commit:** `1285c13`

Initial import of the working tree and push to
`github.com/dmontaine/sdb_ai_windows`.

`.gitattributes` sets `* -text`: the tree is a Linux-targeted package stored on
a Windows host, and a clone on a machine with `core.autocrlf=true` would inject
CRLF into the shell installers. The executable bit was restored on
`installsdai.sh` and `deletesdai.sh`, which Windows had dropped
(`core.filemode=false` staged everything as `100644`). The ELF binaries in
`bin/` were deliberately left non-executable, since `installsdai.sh:514` does
`chmod -R 755` on the installed directory itself.

Git identity was set repo-locally rather than globally, to avoid changing
machine-wide state.
