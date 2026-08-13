# PROJECT STATUS

Living handoff document for the SD Windows port. This project moves between
sessions, machines and accounts; anything not written here is lost. Read this
file first. Read [HISTORY.md](HISTORY.md) only if you need the record of how
something came to be the way it is.

**Last updated:** 13 Aug 2026 · **describes the tree as of commit** `3248b72`
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
5. **Roll over when this file exceeds ~800 lines**, or when any section is
   mostly historical. Move the settled material to HISTORY.md, newest first,
   and leave behind only what a new session needs to act today. §1–§7 are
   permanent sections; keep them, shorten them.

   The limit is a prompt to prune, not a reason to leave something out. If a
   finding is worth recording, record it and trim elsewhere. Detail that also
   exists in HISTORY.md is the first thing to cut, since nothing is lost.
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
| `sdadmins` local group | created, `GITORLI\don` enrolled — **not yet effective, see §6** |
| `gcat` | `$BBPROC`, `$BCOMP`, `!PATHTKN` built by `gplbld/bbcmp.py` |
| `PCODE.OUT` | built by `gplbld/pcode_bld.py` |

The bootstrap sequence, taken from `installsdai.sh`. The first two steps are
done; the third is where it stopped:

```sh
python3 gplbld/bbcmp.py /usr/local/sdsys GPL.BP/BBPROC  GPL.BP.OUT/BBPROC   # done
python3 gplbld/bbcmp.py /usr/local/sdsys GPL.BP/BCOMP   GPL.BP.OUT/BCOMP    # done
python3 gplbld/bbcmp.py /usr/local/sdsys GPL.BP/PATHTKN GPL.BP.OUT/PATHTKN  # done
python3 gplbld/pcode_bld.py                                                 # done
sd -i                                  # <-- STOPS HERE: "SD has not been started"
sd -internal SECOND.COMPILE
sd RUN GPL.BP WRITE_INSTALL_DICTS NO.PAGE
sd THIRD.COMPILE
sd -internal BASIC GPL.BP CPROC        # this is what finally creates gcat/$CPROC
```

**The immediate puzzle.** `sd -i` reports "SD has not been started", which is
`bind_sysseg` being called with create false — it is trying to attach to a
segment nobody has created. But `sd -start` cannot run yet either, because
`config.c` refuses to start until `<sysdir>/gcat/$CPROC` exists, and `$CPROC`
is only produced by the last step of the list above. Resolve that ordering
first: either `-start` precedes `-i` in a way `installsdai.sh` does not make
obvious, or `-i` is supposed to create the segment itself. Read the `-i`
handling in `sd.c` around the `is_bootstrap` flag before changing anything.

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
- The new `IsAdmin()` logic (§5.6), against member, non-member, absent group
  and primary group. `getgrnam()` resolves Windows local groups on the MSYS2
  runtime and reports membership accurately.
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
  port and it is now largely closed, though still not exercised *by SD itself*.
- `gplbld/bbcmp.py` and `gplbld/pcode_bld.py` both run on Windows and produce
  `gcat` entries and `PCODE.OUT`.

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

### 5.5 The privilege model does not survive the move (blocks administration)

This is the most consequential linkage and is not about platform detection at
all. `IsAdmin()` in `linuxlb.c` is `return (getuid() == 0)`, and `SYSTEM(27)`
returns `getuid()` straight through. Under MSYS2 `getuid()` is 197609 — never
zero, and there is no uid 0 on Windows, where administrator is a token
privilege rather than a user id.

So every privilege test in the BASIC layer resolves the same way, permanently:

| Site | Test | Result on Windows |
|---|---|---|
| `CPROC` | `new.account = "SDSYS" and system(27) > 0` | always true — **SDSYS access always denied** |
| `CATALOG` | `system(27) # 0` for `CATALOG GLOBAL` | always true — **global cataloguing always denied** |
| `CPROC` | `system(27) = 0` "entered as root?" | always false — the drop to `sdsys` never runs |
| `BBPROC` | `system(27) # 0` | always true |
| `op_kernel.c` | `K$ADMINISTRATOR` via `IsAdmin()` | never granted |

The `CATALOG GLOBAL` one matters beyond administration, because cataloguing is
part of getting compiled BASIC into service.

`EUID_SET`/`EUID_RESTORE` are the mechanism the root branch would have used.
They reach `sdext_eguid.c` through `SDEXT`, which calls `getpwnam`, `setegid`
and `seteuid`. Native Windows has no equivalent; impersonation there is
`LogonUser` plus `ImpersonateLoggedOnUser`.

Nothing here is fixed by flipping `SYSTEM(91)`. It needed a decision about what
"administrator" means on Windows; that decision is §5.6.

### 5.6 Identity model on Windows (decided 13 Aug 2026)

Two decisions from the repository owner, replacing the Linux model where SD
creates OS accounts and `sudo sd` confers administrator rights.

**SD no longer creates or deletes OS accounts.** An administrator creates
Windows users out of band; SD maps its accounts onto users and groups that
already exist, and manages only its own group membership. This keeps file
security enforced by the OS without SD needing standing administrative rights,
and it does not break on a domain-joined machine, where creating local users
would be wrong.

**SD administrator rights come from membership of the `sdadmins` local group**,
not from elevation. This separates SD administration from Windows
administration: it can be granted without handing out machine admin, needs no
UAC prompt, and works for a service or other non-interactive process.

`SD_ADMIN_GROUP` in `sddefs.h` names the group. `IsAdmin()` in `linuxlb.c`
resolves it with `getgrnam()` and tests the primary group and the supplementary
list. If the group does not exist, nobody is an administrator — it fails
closed. Verified on the MSYS2 runtime: `getgrnam()` resolves Windows local
groups correctly (`Users` 545, `Administrators` 544), membership is reported
accurately, and all four paths behave (member, non-member, absent group,
primary group).

Done: `IsAdmin()` and `SD_ADMIN_GROUP`.

Still to do, and none of it is verifiable until SD runs (§6):

- `CPROC` and `CATALOG` test `SYSTEM(27)` **directly**, not `K$ADMINISTRATOR`,
  so the new `IsAdmin()` does not reach them and SDSYS and `CATALOG GLOBAL`
  are still refused. They should ask `KERNEL(K$ADMINISTRATOR, -1)` instead.
  `SYSTEM(27)` should keep meaning "uid", which on Windows is simply not a
  privilege answer.
- The `OS.EXECUTE` account commands in `CREATE_USER`, `SET_PASSWD`, `CREATEA`,
  `DELACC` and `MODIFYA` must stop calling `useradd`, `passwd`, `usermod`,
  `userdel` and `groupadd`, and either map onto existing Windows users or
  refuse with a clear message.
- `chmod g+s` has no Windows equivalent. The setgid directory behaviour is
  inheritable ACEs: `icacls <dir> /grant "<group>:(OI)(CI)M"`.
- The installer must create the `sdadmins` group and stop creating `sdsys`
  as an OS user.

### 5.7 Other BASIC to C linkages, surveyed

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

### 5.8 What is tracked

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
- **Editing BASIC source changes nothing on its own.** `sdsys/GPL.BP.OUT`
  holds only a README — there are no compiled objects in the tree. The
  installer compiles the BASIC at install time with
  `bin/sd -internal BASIC GPL.BP CPROC`, after `gplbld/pcode_bld.py` builds the
  pcode. So a BASIC edit is inert until SD runs and can compile it, and every
  BASIC-side fix is gated behind runtime bring-up.
- **Privilege tests do not fail, they answer wrongly.** `IsAdmin()` is
  `getuid() == 0` and `SYSTEM(27)` is `getuid()`, which is 197609 here. Nothing
  errors; the branches simply always take one side, so the symptom is "SDSYS
  access is restricted" or "Command requires administrator privileges" from
  code that looks correct. See §5.5 before debugging any permission complaint.
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

0. **Answer the open question at the top of §8 first** if any further identity
   work is planned. It changes §5.6.

1. **Finish runtime bring-up.** Environment and the first bootstrap steps are
   done; resume at the `sd -i` ordering puzzle described in §3. The shared
   memory and semaphore code has now been verified in isolation (§4), so
   suspect the bootstrap sequence rather than the IPC port.
2. **Enable `CASE_INSENSITIVE_FILE_SYSTEM`.** Referenced at 9 sites in
   `dh_misc.c`, `dh_open.c`, `op_dio2.c`, `op_dio4.c` but never defined
   anywhere. Windows filesystems *are* case insensitive, so this is a
   correctness gap and the code is already written.
3. **Exercise `SDConnectLocal()`** once a server runs. Needs an `sd.ini` in the
   Windows directory with an `[sd]` section and `SDSYS=`, or `SD_CONFIG` set.
4. **Finish the identity model** (§5.6). `IsAdmin()` is done; the BASIC side is
   not, and none of it can be tested until step 1 lands (§6). Point `CPROC` and
   `CATALOG` at `KERNEL(K$ADMINISTRATOR, -1)` instead of `SYSTEM(27)`, stop the
   `OS.EXECUTE` account commands creating and deleting OS users, translate
   `chmod g+s` to an inheritable ACE, and have the installer create the
   `sdadmins` group instead of the `sdsys` OS user.

5. **Fix `VALID_OS_PATH`** so it accepts backslashes and spaces. Cheap, and it
   blocks account creation and `PY_RUNFILE` on any native Windows path. Widen
   the character set without weakening the shell metacharacter protection it
   exists to provide — quoting the path at the `OS.EXECUTE` site is the safer
   way to allow spaces. Note `CREATEA` runs `sudo chmod g+s`, which has no
   native Windows equivalent and needs its own answer.

6. **Restore the BASIC layer's Windows branches** from the external `GPL.BP`
   tree (§5.4), then set `SYSTEM(91)` to 1 and assign `is_nt`. In that order:
   flipping the switches first would enable paths that are no longer present.
   Start with `CPROC`'s `dir.separator`, since compilation depends on it.

7. **Port the installer.** `installsdai.sh` is apt/dnf/zypper, systemd, xinetd
   and `/etc` paths throughout. It also tests for `bin/sd`, which is now
   `bin/sd.exe` (also `cp -R bin` and the `/usr/local/bin/sd` symlink).
8. **Stage 2, native Win32.** `fork` → `CreateProcess` (all five call sites are
   fork+exec, none need copy-on-write, so this is tractable), `termios` →
   Console API, passwd/group → Windows authentication.

## 8. Open questions

### Decide first: should admin status live inside SD instead of in an OS group?

**Raised by the repository owner on 13 Aug 2026 and not yet answered. It
affects §5.6, so settle it before doing more work there.**

The proposal is that an SD account carries an administrator flag, so admin
status is determined entirely within SD and no OS group is involved.

Evidence gathered since that decision was made, all of which favours the
proposal:

- The owner also requires that the person installing becomes an administrator
  automatically. With an OS group they cannot — Windows fixes group membership
  at logon, so a freshly enrolled installer must sign out and back in before
  they can administer anything (§6). An internal flag has no such delay.
- SD already has the machinery. Login records carry `LGN$ADMIN`, and
  `K$ADMINISTRATOR` already reads and writes an administrator bit on the user
  entry. An internal flag uses what exists rather than adding a mechanism.
- It removes a Windows-specific install step (creating a local group, which
  needs elevation) and the local-versus-domain group question with it.

The cost is that SD alone then decides who is an administrator, with no
operating system gate behind it. On the current design the OS is still the
authority.

Note these are not exclusive: `IsAdmin()` could remain as written and the
BASIC layer consult `LGN$ADMIN`, with either sufficing. That keeps central
management possible for sites that want it, at the price of two paths to audit.

If the internal flag is adopted, `IsAdmin()` and `SD_ADMIN_GROUP` as committed
should be revisited, and the `sdadmins` group already created on this machine
becomes unnecessary.

### Other

- `usr/lib/systemd/` and `etc/xinetd.d/` are kept deliberately. They have no
  function on Windows but they document the service topology — socket
  activation, ports, per-connection instances — that a Windows service must
  reproduce. Remove once that design is captured elsewhere.
- The client library is LGPL-3.0-or-later with a linking exception, while the
  rest of the tree is GPL-3.0. That is compatible and intentional for a client
  library, but it is a real licensing boundary worth being aware of.
