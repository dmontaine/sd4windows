# PROJECT STATUS

Living handoff document for the SD Windows port. This project moves between
sessions, machines and accounts; anything not written here is lost. Read this
file first. Read [HISTORY.md](HISTORY.md) only if you need the record of how
something came to be the way it is.

**Last updated:** 13 Aug 2026 · **describes the tree as of commit** `139cdfd`
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
5. **Roll over when this file exceeds ~400 lines**, or when any section is
   mostly historical. Move the settled material to HISTORY.md, newest first,
   and leave behind only what a new session needs to act today. §1–§7 are
   permanent sections; keep them, shorten them.
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

The client library is already at stage 2 — see §5.4.

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
it. See §5.5.

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

### Not yet working

Nothing has ever started SD. There is no `/etc/sd.conf` and no `sdsys`
directory, so the shared segment has never been created. See §4 and §7.

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

### Not verified — treat as unknown

- **SD has never started.** The `shm_open`/`ftruncate`/`mmap` *creation* path
  in `sysseg.c` has never executed. Only the "not started" probe has.
- Multi-process attach, semaphore locking under contention, and `stop_sd()`'s
  new liveness poll.
- `SDConnectLocal()` at runtime. It needs a running server and an `sd.ini`.
- Any database read or write.
- The installer. `installsdai.sh` is still entirely Linux.

## 5. Decisions and why

Do not undo these without reading the reasoning.

### 5.1 POSIX IPC replaces System V

MSYS2 ships the genuine Cygwin `sys/shm.h`, so System V code **compiles and
links cleanly** and then fails at runtime with ENOSYS. Native Windows has no
System V IPC at all. POSIX named shared memory and named semaphores work on
both.

- `sysseg.c`, `sdidx.c`, `sdlnxd.c`: `shmget`/`shmat`/`shmdt` →
  `shm_open`/`ftruncate`/`mmap`/`munmap`
- `sdsem.c`: `semget`/`semop`/`semctl` → `sem_open`/`sem_trywait`/`sem_post`
- Object names come from `SD_POSIX_SHM_NAME` / `SD_POSIX_SEM_FMT` in `sddefs.h`

This is also the right direction for stage 2, since POSIX shared memory is
backed by `CreateFileMapping` anyway.

### 5.2 Two things needed more than a substitution

- `munmap` must be told the mapping length that `shmdt` derived from the
  address, so the size is recorded at attach time.
- `stop_sd()` waited on the System V attach count, which POSIX shared memory
  does not expose. It now polls the user table with `kill(pid, 0)`. That is
  more robust than the original: it also catches a process that died without
  clearing its own table entry.

### 5.3 Client library is vendored, not referenced

`gplsrc/sdclilib/` is a vendored copy of `github.com/dmontaine/winsdclilib`
at `b662456`, replacing the old `gplsrc/sdclilib.c`.

It sits in **its own directory** because its `sdclient.h`, `err.h` and
`revstamp.h` are different files from the ones in `gplsrc`. `revstamp.h` feeds
`MAJOR_REV`/`MINOR_REV`/`BUILD` into `SYSSEG_REVSTAMP` in `sysseg.c`, which
stamps the shared memory segment — displacing the server's copy would be a bad
trade for a flatter layout.

Local additions (`SDConnectLocal`, `sysdir`, the transport layer) are recorded
in `gplsrc/sdclilib/VENDORING.md`. **Read that before syncing upstream.**

### 5.4 Two toolchains on purpose

The server is built against the MSYS2 runtime; the client DLL is native
UCRT64 and needs no `msys-2.0.dll`. The runtimes never meet — a client links
the DLL and reaches the server over a socket or a named pipe, always as
separate processes. Override with `UCRT_CC=...`.

### 5.5 The BASIC layer has its own platform switch (not yet touched)

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
`GPL.BP` tree and can be recovered from there:

- `CPROC` — `dir.separator = if windows then '\' else '/'`, now hardcoded `'/'`
- `CREATEA` — `if windows then pathname = upcase(pathname)`, twice
- `LOGIN` — Windows console sessions identified as `Console`, forced to
  administrator, login id and account paths upcased
- `CONFIG` — `SPOOLER` hidden on Windows, `CODEPAGE` shown only on Windows
- `PARSER` — a colon mid-token is a drive letter on Windows, not a delimiter
- `INT$KEYS.H` — `OPT.SELECT.KEEP.CASE`, `OS$FULLPATH`

Order matters: restoring the BASIC branches while `SYSTEM(91)` still returns
zero is harmless, but flipping `SYSTEM(91)` first turns on paths that are no
longer there.

### 5.6 What is tracked

Linked binaries in `bin/` are tracked, because the install scripts deploy them
from the repository. Compiler intermediates, generated `terminfo/`, pcode
scratch and the client's build products are not. See `.gitignore`.

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
  `revstamp.h` — see §5.3.
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

1. **Runtime bring-up.** Create a minimal `/etc/sd.conf` and `sdsys` directory
   and actually start SD. This is the first real test of the shared memory
   creation path, the semaphores and multi-process attach — the largest block
   of unverified work in §4.
2. **Enable `CASE_INSENSITIVE_FILE_SYSTEM`.** Referenced at 9 sites in
   `dh_misc.c`, `dh_open.c`, `op_dio2.c`, `op_dio4.c` but never defined
   anywhere. Windows filesystems *are* case insensitive, so this is a
   correctness gap and the code is already written.
3. **Exercise `SDConnectLocal()`** once a server runs. Needs an `sd.ini` in the
   Windows directory with an `[sd]` section and `SDSYS=`, or `SD_CONFIG` set.
4. **Fix `VALID_OS_PATH`** so it accepts backslashes and spaces. Cheap, and it
   blocks account creation and `PY_RUNFILE` on any native Windows path. Widen
   the character set without weakening the shell metacharacter protection it
   exists to provide — quoting the path at the `OS.EXECUTE` site is the safer
   way to allow spaces. Note `CREATEA` runs `sudo chmod g+s`, which has no
   native Windows equivalent and needs its own answer.

5. **Restore the BASIC layer's Windows branches** from the external `GPL.BP`
   tree (§5.5), then set `SYSTEM(91)` to 1 and assign `is_nt`. In that order:
   flipping the switches first would enable paths that are no longer present.
   Start with `CPROC`'s `dir.separator`, since compilation depends on it.

6. **Port the installer.** `installsdai.sh` is apt/dnf/zypper, systemd, xinetd
   and `/etc` paths throughout. It also tests for `bin/sd`, which is now
   `bin/sd.exe` (also `cp -R bin` and the `/usr/local/bin/sd` symlink).
7. **Stage 2, native Win32.** `fork` → `CreateProcess` (all five call sites are
   fork+exec, none need copy-on-write, so this is tractable), `termios` →
   Console API, passwd/group → Windows authentication.

## 8. Open questions

- `usr/lib/systemd/` and `etc/xinetd.d/` are kept deliberately. They have no
  function on Windows but they document the service topology — socket
  activation, ports, per-connection instances — that a Windows service must
  reproduce. Remove once that design is captured elsewhere.
- The client library is LGPL-3.0-or-later with a linking exception, while the
  rest of the tree is GPL-3.0. That is compatible and intentional for a client
  library, but it is a real licensing boundary worth being aware of.
