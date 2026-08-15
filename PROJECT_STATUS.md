# PROJECT STATUS

Living handoff document for the SD Windows port. This project moves between
sessions, machines and accounts; anything not written here is lost. Read this
file first. Read [HISTORY.md](HISTORY.md) only if you need the record of how
something came to be the way it is.

**Last updated:** 15 Aug 2026, eighth session, from commit `317ad58`. Closed
the previous header item: `bootstrap.py` and `stage.py --bootstrap` now refuse
an unelevated window up front, before any work (§4, §6). The seventh session
closed **§7 step 1d** and **§7 step 1c**; step 0 closed in the sixth, and the
access model is live.

**START HERE, in order:**

1. **Rebuild stage + installer, install the new binaries.** The installed
   `sd.exe` is **14 Aug 19:05** and predates step 1d; the repo build is
   15 Aug 06:23. `stage.py --force --bootstrap` from an **elevated** window,
   then ISCC, per the top of `gplbld/sd.iss`. **`C:\Users\dmont\stagetest` was
   re-staged 15 Aug 06:43 with the `ACCOUNTS/SDSYS` fix (§6) — 3,471 files,
   `gcat` 130 entries** (129 before: the dev tree it used to compile was a
   program short). ISCC and the install are what remain. A reinstall does
   **not** replace the data tree (§6).
2. **§7 step 1f** — the installer's SD account. `ADOPT` exists, nothing calls
   it, so `don` is still refused at his own machine.
3. **§7 step 2** — second machine. Only place RDP and a clean install can be
   tested.

**Untested branches from step 1c:** `DELETE.ACCOUNT`'s "SD created it" delete
(use `sdacct4` — real Windows account, password known to nobody) and `ADOPT`.

**Machine, 15 Aug 2026 06:25.** **SD is NOT running and the machine is back in
the stale-segment state** — `C:\ProgramData\SD\shm` holds the segment and all
six semaphores, dated 14 Aug 21:58, with no `sdwind` process. That is a
ready-made test for the installed binary the moment it is replaced: today's
19:05 one answers `SD is already started`, the current build says the segment is
stale and names `sd -stop` (§7 step 1d). **`bin/` is current** — `make sd`
exit 0, all six relinked 15 Aug 06:23, `terminfo` 99 files. Installed BASIC is
current for
`IS_USER`, `IS_GROUP`, `IS_SD_USER`, `DELACC`, `CREATEA`; `$LOGIN`/`$CPROC` are
sixth-session and still print the old banner. `gcat.bak` is the rollback.
`sdacct1` removed by `DELETE.ACCOUNT`; `sdacct2`/`sdacct3` half-removed,
`sdacct4`/`sdacct5` complete. UAC is at the default (`ConsentPromptBehaviorAdmin`
5, `PromptOnSecureDesktop` 1), so elevation raises a secure-desktop prompt — an
AI session cannot self-elevate; ask.

**A test naming `C:\Program Files` tests the installed binary**, which is only
current just after an install. That cost a round of the `EPERM` test.

**THE ACCESS MODEL, BUILT AND VERIFIED.** Full statement in §5.6; the short
form, because it changes what every other item in this file assumes:

- **SD login takes no password at all.** The operating system has already
  authenticated you. Typing `sd` puts you in **the SD account with your own
  name**, and nowhere else. **No linked SD account means no login.**
- **`sudo sd` — any elevated session — puts you straight into SDSYS.** That is
  the only route into administration, and **`Administrators` is the sudoers
  file**: `CREATE.ACCOUNT USER x` does not add to it, `... ADMINISTRATOR` does.
- **ELEVATION IS LOCAL BY DESIGN** — owner's decision, and confirmed rather
  than assumed: an ssh session cannot reach SDSYS (§4). Administrators having
  *less* remote access than ordinary users is the intent.
- **The API is the exception and still wants a password** (§8). Nothing of the
  password work was deleted: `$CRED`, `!CRED_SET`, `!CRED_VERIFY` and
  `SET.PASSWORD` all stay, as the API's credential rather than the console's.
- **`ACC$USERS` IS DEAD — THE GRANT IS WINDOWS GROUP MEMBERSHIP.** Entry to an
  account is membership of its `ACC$GROUP` group, so `GRANT`/`REVOKE` become
  verbs over `!os_group` (§7 step 5). **Grants recorded on 13 or 14 Aug
  silently stopped working**, and **anyone granted an account cannot use it
  until they sign out and back in** — group membership is fixed in the token at
  logon (§6).
- **SD ACCOUNTS BRING THEIR OWN OS ACCOUNT, WITH ONE EXCEPTION** — owner's
  decision, 14 Aug 2026, seventh session. **The only pre-existing OS user that
  may be given an SD account is the installer's**, done at install time; every
  other SD account creates its OS account from within SD. `CREATE.ACCOUNT`
  refuses a name that already exists in Windows, and the single sanctioned door
  is `ADOPT`, gated on `K$INTERNAL` so the install can use it and a console
  cannot. **The installer's account does not exist yet** — §7 step 1f.

**Also true and worth having in one place:** `AllowGroups` is applied and
enforced on this machine, by control and treatment (§4), and the lockout risk
is closed by measurement. **§5.6.2 is complete except RDP**, which **cannot be
tested from one machine** and waits on the second (§7 step 2). Nothing is left
half-applied.

**STATE OF THIS MACHINE, 14 Aug 2026 - READ FIRST.** There is a **working SD
install** on it, from the fixed installer:

| Thing | State |
|---|---|
| **The install is from 14 Aug 19:05 and is BEHIND the repository** | Corrected 15 Aug 2026 by dating the files: this row said "CURRENT, reinstalled 16:15", and the row below it said 19:05. 19:05 is right — the sixth session reinstalled after 16:15. **Date it again before trusting it**; it does not update itself, and a reinstall will not replace the data tree |
| `C:\Program Files\SD` | **18 files**, binaries in `usr\bin` including `sdwind.exe`; `sd.exe` is **14 Aug 19:05**, 1,926,742 bytes. 18 rather than the stage's 16 because `unins000.exe` and `unins000.dat` are the installer's |
| `C:\ProgramData\SD\sdsys` | **3,412 files on 15 Aug 2026 - a working database.** The compiled `gcat/$CREATEA` **contains the ssh-only branch**; `MESSAGES/10032`–`10035` are all present. It was 3,270 on 14 Aug and 3,268 as staged: the count drifts upward as accounts are created, so a difference from the stage is not a fault |
| SDSYS password | **not set, and it no longer matters** — nothing on the console asks for one. The password prompt is gone from the installed system too, as of the sixth session: the `Warning: account SDSYS has no password set` line no longer appears |
| **THE ACCESS MODEL IS LIVE** | sixth session, 14 Aug 2026. Binaries **19:05** in `C:\Program Files\SD\usr\bin` (`sd.exe` 1,926,742 bytes, carrying `IsElevated()`), and `GPL.BP\LOGIN`/`CPROC` recompiled against them and catalogued. **An unelevated `sd` no longer reaches SDSYS** — it refuses with `sysmsg(5018)`, and `sd -ASDSYS` with `sysmsg(10002)`. Both observed, §4 |
| **THE INSTALLED BINARIES ARE CURRENT AGAIN** | 15 Aug 2026: installed from `sd-setup-1.0-2.exe` built 06:47 (4,795,558 bytes) out of the re-staged tree, so `C:\Program Files\SD\usr\bin` is the 06:23 build and **step 1d is now proven on the install as well** (§4). The *data* tree was left alone, as designed — so the installed catalogue is still the sixth session's and the corrected one sits in the stage |
| **`GPL.BP\LOGIN` IS AHEAD OF THE CATALOGUE TOO** | seventh session: the sign-on banner changed in the repository, and the installed `gcat/$LOGIN` is still 18:54:15. It is cosmetic, and it needs the same elevated recompile as everything else in `GPL.BP` |
| Reinstalling over this | the installer **found the existing database and left it alone**, saying so in a dialog — §6's staleness trap, working as designed. So a reinstall updates `C:\Program Files` and **not** `C:\ProgramData\SD\sdsys`: after one, copy `GPL.BP\LOGIN`/`CPROC` across and recompile, or the machine runs yesterday's BASIC on today's binaries |
| Rollback, if login ever breaks | **`gcat.before-step0` is GONE**, deleted in the sixth session once the refusals were verified — it held the *pre-change* catalogue, and going back to the password model stopped being something anyone would want. **The way back now is `C:\Users\dmont\gcat.rollback`**, a complete 129-entry catalogue bootstrapped from the same sources. It restores *today's* behaviour rather than yesterday's, which is the more useful direction. It was copied out of `C:\Users\dmont\stagetest` on 15 Aug 2026 because the next step is `stage.py --force`, which deletes that tree — **if you re-stage, the rollback lives outside the staging directory or it does not survive** |
| `sdusers` group | exists, with `GITORLI\don` in it |
| `sdadmins` group | exists, **created by hand on 13 Aug, not by the installer**, and nothing references it any more (§8). Leave it alone |
| System PATH and the Settings > Apps entry | both present |
| `C:\ProgramData\SD` ACL | locked to sdusers/Administrators/SYSTEM. An unelevated session **cannot read inside it** until `don` signs out and back in; `Test-Path` on the directory itself still says True, so look at the contents |
| MSYS2 dev tree at `/usr/local/sdsys` | still reachable with `SD_CONFIG=/etc/sd.conf`. Its `bin/` was refreshed with the `sdwind` build on 14 Aug 2026 and the stale `sdlnxd.exe` removed; `pcode`/`pcode.old` are still beside them, since the dev tree keeps the old unsplit layout |
| **The machine was rebooted** on 14 Aug 2026 | `don`'s token now carries `sdusers`, so **an ordinary unelevated session runs SD** — verified, §4. The sign-out trap in §6 is cleared *on this machine only*; it applies afresh to every new user added to the group |
| **OpenSSH Server** | **installed, `sshd` Running / Automatic**, listening on 22, firewall rule enabled |
| **`AllowGroups` IS APPLIED** | 14 Aug 2026, by `allow-ssh-groups.ps1 -Installed`. `C:\ProgramData\ssh\sshd_config` carries `AllowGroups sdusers GITORLI\sdusers Administrators GITORLI\Administrators` between SD's markers, before the `Match` block. **Only members of `sdusers` or `Administrators` can ssh into this machine at all** — verified, §4. The original is at `sshd_config.before-sd`; `allow-ssh-groups.ps1 -Remove` reverses it. Left in place deliberately: it is what the installer would have written |
| `sdsshonly` group | **exists now**, created 14 Aug 2026 by `verify-sshonly.ps1`, with both deny rights applied to it. So `CREATE.ACCOUNT` for a non-administrator will work here. It is left in place deliberately — it is what the installer would have created |
| Test accounts, Windows side | **`sdacct4` and `sdacct5` EXIST and are real, enabled, ssh-only accounts**, left by `-Keep` in the sixth session. `sdacct5` is the one §5.6 was verified with and is worth keeping until step 1 is done; **nobody knows `sdacct4`'s password** — it was random and the run that generated it hung before printing it. `sdacct1`, `sdacct2`, `sdacct3` and `sdsshprobe` are gone from Windows. Remove the two with `verify-createaccount.ps1 -Cleanup -Account <name>` |
| Test accounts, **SD side** | `sdacct2`–`sdacct5` + SDSYS. `sdacct1` was removed by `DELETE.ACCOUNT` on 14 Aug 2026, the first run of that verb. `sdacct2` and `sdacct3` are still half-removed (no Windows account) and are spare test cases for the same branch; `sdacct4` and `sdacct5` are complete on both sides. Use a fresh `-Account` name when re-running `verify-createaccount.ps1`; SD refuses a reused one |
| SD | **running, pid 7388 from the installed 06:23 binary**, 15 Aug 2026 06:53, segment and six semaphores present. It also ran as the seventh session ended, `sdwind` 4696 from `sdb_ai\sd64\bin`; **an ordinary session held terminate rights on it**, measured with `OpenProcess(PROCESS_TERMINATE)`, so `Stop-Process` reaches an unelevated-started daemon. **Corrected earlier: a blank `Path` is not evidence a process was started elevated** — §6 |
| SD at boot | **does not start.** There is no service (§5.7), so `sd -start` must be typed after every restart |

Nothing needs cleaning off before the next piece of work. To start over anyway,
elevated: `C:\Program Files\SD\unins000.exe /VERYSILENT`, delete
`C:\Program Files\SD` and `C:\ProgramData\SD`, then `Remove-LocalGroup sdusers`
— but leave `sdadmins` alone, for the reason in §8.

**THE STAGED TREE AND THE INSTALLER DO NOT CARRY THE STEP 1D FIX.** Dated
15 Aug 2026: `C:\Users\dmont\stagetest` is 14 Aug **19:14**, 3,287 files, its
`sd.exe` the 19:05 one; `C:\Users\dmont\sdout\sd-setup-1.0-2.exe` is **19:15**,
4,776,555 bytes. Both were checked rather than assumed —
`MESSAGES/10032`–`10035` present, the three `.ps1` scripts in `ProgramFiles`,
and `gcat/$CREATEA` containing the string `sdsshonly`, the ssh-only branch shown
present in pcode rather than inferred from source. **Not verified: that this
particular installer installs.** It compiled; nobody has run it. Neither
artefact survives a rebuild of the machine; both are reproduced by the commands
at the top of `gplbld/sd.iss`.

**Where to start next. The full list is §7; what follows is only what a session
starting cold would otherwise get wrong.**

**Every elevated command in this file is written out in full on purpose.** An
elevated window opens in `C:\WINDOWS\system32`, never in the repository, so a
relative path fails with "the argument ... does not exist" — which reads like a
missing script rather than a wrong working directory.

**Re-running `CREATE.ACCOUNT` needs a FRESH account name.** The SD side of a
previous run is left behind deliberately (§7 step 1c), so the verb refuses a
reused one:

```powershell
powershell -File C:\Users\dmont\Projects\sdb_ai_windows\sdb_ai\sd64\gplbld\verify-createaccount.ps1 -Account sdacct6
```

**`AllowGroups` is left applied here deliberately** — it is what the installer
would have written. `allow-ssh-groups.ps1 -Remove` reverses it;
`verify-allowgroups.ps1` re-checks the file editing with no elevation, no
`sshd` and no network. **Before applying it on another machine**, read the §4
entry: a client cannot tell an `AllowGroups` refusal from a failed
authentication, so the reason has to come out of the `OpenSSH/Operational` log,
and the control account must be an **enabled** one.

**Read first if anything to do with compilation misbehaves:** the `ERRGEN` trap
in §6. An undefined `$define` in SD is a *warning* at compile time and an abort
at run time, in a program that may not run until much later.

---

## 0. Maintenance rules

Revised 14 Aug 2026, seventh session, on the owner's instruction: **the
documentation was taking more of a session than the work.** The rules below
replace a longer set that caused it.

**Audience: the next AI session. Not the owner — he does not read these.** Write
for a cold agent that will act on this: terse, factual, `file:line` over
description. No emphasis for effect, no narrative, no argument. The `changelog`
is the exception and stays plain English for users.

1. **Same commit as the work.** If a commit changes what builds, runs, is
   decided, or is next, it changes this file.
2. **Verified means you watched it, this session.** Compiling is not running.
   Otherwise it goes in §4 Not verified, whatever an earlier session claimed.
3. **One fact, one place.** Do not restate a finding in the header, §4, §6, §7
   and HISTORY. Put it where it belongs and point at it. Duplication is the
   main way this file got large.
4. **§6 traps: anything that cost real time.** What happens, what to do. This
   section is meant to grow; never cut a trap for size.
5. **Size is a ~3,500 line ceiling and nothing more.** Do not print line counts
   in the text and do not re-measure to keep a printed number true — that loop
   cost a dozen tool calls on 14 Aug 2026. When a §7 step closes, compress its
   §4 and §7 material to the conclusion in the same commit; that is enough to
   hold the size without a rollover.
6. **Corrections: fix the text, say so in one line, move on.** No separate
   ceremony. HISTORY stays append-only.
7. **Absolute dates.** Never "today" or "last session".
8. **User-visible changes go in `sdb_ai/sd64/sdsys/changelog`**, same commit.
   New or changed verbs, messages, files, login behaviour, configuration.
   Refactors, findings and traps do not.

**Time budget: documentation is a small fraction of a session.** If it is
approaching half, stop and cut.

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
mingw-w64-ucrt-x86_64-gcc`. **`python-devel` and `gettext-devel` are no longer
needed** (13 Aug 2026), both dropped with embedded Python (§5.15).

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

**The unmodified Linux version is at
<https://codeberg.org/stringdatabase/sdb64>** (given by the repository owner,
14 Aug 2026). `sdb64` is the active project; **this tree, `sdb_ai`, is an
experimental variant** that has been through five major AI cleaning and
validation cycles, which is why the code reads more cleanly than its age
suggests — and why those cycles can also introduce new problems, as the
`VALID_OS_PATH` trap in §6 shows. Check `sdb64` before assuming a difference is
deliberate; several things this port has "found" turned out to be inherited
rather than introduced. It is a network resource, so it is available on any
machine.

**The TCL verb surface is written down**, in
[docs/TCL_VERBS.md](docs/TCL_VERBS.md) — SD's commands against OpenQM 2.6.6,
supplied by the repository owner 14 Aug 2026. Read it before adding or renaming
a verb. The important structural fact it records: **SD has accounts, not
accounts and users.** `CREATE.USER`, `DELETE.USER`, `ADMIN.USER` and
`LIST.USERS` are all deliberately absent, which is why `CREATE.ACCOUNT`
provisions the operating system account itself and why the `CREATUSR` gate was
removed (§7 step 1a).

Two local trees, neither part of this repository, both absent on a fresh
machine, and nothing in the build depends on either:

- **`C:\Users\dmont\Projects\gplsrc`** — original GPL ScarletDME C source.
  Limited value: Ladybridge stripped the Windows code thoroughly. Still useful
  for recovering text mangled by the `qm`→`sd` rename.
- **`C:\Users\dmont\Projects\GPL.BP`** — original ScarletDME BASIC source, 212
  files. **This one is genuinely valuable.** It retains real Windows code that
  this repository's `sdsys/GPL.BP` had stripped: 21 files carry Windows logic
  there against 6 here, and every file present in both lost all of it. See
  §5.4.

## 3. Current state

### Building

From `sdb_ai/sd64`, and only from there (see §6):

```sh
make sd
```

Produces in `sdb_ai/sd64/bin`:

| Artifact | Kind |
|---|---|
| `sd.exe` `sdconv.exe` `sdfix.exe` `sdidx.exe` `sdwind.exe` `sdtic.exe` | PE32+, MSYS2 runtime |
| `sdclilib.dll` + `libsdclilib.dll.a` | PE32+, native UCRT64 |

`make sdclilib` builds just the client. `terminfo/` (99 files) is generated by
the `terminfo` target and is not tracked.

### Bootstrapping a machine from nothing

**SD runs**, and the bootstrap **is a script now, not prose:
`gplbld/bootstrap.py`.** Run it through `gplbld/stage.py --bootstrap`, which is
how an install is built (§5.16), so **an end user never runs any of this** —
the staged tree ships the result. The script is the authority on the sequence;
what follows is only what reading it will not tell you.

The shape, for orientation: compile `BBPROC`, `BCOMP` and `PATHTKN` with
`gplbld/bbcmp.py`, build the pcode with `gplbld/pcode_bld.py`, `touch` an empty
`<sysdir>/gcat/'$CPROC'`, then `sd -start`, `sd -i`, and four `sd -internal`
steps ending `BASIC GPL.BP CPROC`, which writes the real `gcat/$CPROC`.

**It takes an elevated window, and both scripts refuse one that is not**
(15 Aug 2026): those four steps stand in SDSYS, which unelevated is refused.
§6 has the mechanism.

**Three things about that sequence that look wrong and are not**, each of which
cost time when it was rediscovered:

- **The last three steps need `-internal`.** Written as plain `sd RUN ...` they
  sit at an `Account:` prompt until the connection is terminated, because plain
  `sd` with no account named stopped putting an administrator into SDSYS on
  13 Aug 2026 (§5.6).
- **`sd -i` finishes its work and then dies on signal 6.** Its exit status says
  nothing, so judge it on what it created — `VOC`, `VOC.DIC`, `ACCOUNTS.DIC`,
  `$MAP`, `DICT.DIC`. `installsdai.sh` sidestepped this by commenting the line
  out, which is why it never surfaced.
- **The `touch` is what lets `sd -start` run before anything is catalogued.**
  `read_config()` only does `access(path, 0)` on `<sysdir>/gcat/$CPROC`, so an
  empty file satisfies it and the last step overwrites it. There is no ordering
  deadlock; if it looks like one, read the HISTORY entry "SD runs. Full
  bootstrap completes" before re-deriving it.

`gplbld/FILES_DICTS` is copied into `<sysdir>/gplbld/` for the bootstrap and
removed afterwards — `WRITE_INSTALL_DICTS` reads it as
`@sdsys:"/gplbld/FILES_DICTS"`. It is a build input, not data, so it must not
still be there when the tree ships. **`gplsrc`, `gplobj` and `gplbld` do not
belong in `<sysdir>` at all** (13 Aug 2026); `gplbld/gen_includes.py` does at
build time what the `$execute` lines in `APISRVR` and `ERRTEXT` used to do at
compile time.

Two things to expect while running it: **an aborted run leaves record locks
behind**, so `sd -stop` and `sd -start` before retrying or the next run waits
forever at no CPU (§6); and **every catalogue write prints `Unable change
ownership of directory error <path> err: 1000`**, which is `CATALOG` doing the
Linux `chown` to `sdsys:sdusers` and has no Windows meaning. Non-fatal.

### The development tree, and why it is no longer the way in

**The MSYS2 development tree at `/usr/local/sdsys` still exists on this machine
and is still reachable with `SD_CONFIG=/etc/sd.conf`**, but it is not how the
system is used any more and the installer must not reproduce its layout. Its
full state as it stood on 13 Aug 2026 — the scratch accounts `JANE`, `SUE`,
`KIM` and `PAT`, their plaintext test passwords, the recorded grants, and the
scratch `BP` programs — is archived in the HISTORY entry "PROJECT_STATUS rolled
over from 4,112 lines". **Those passwords are real and still set; delete the
scratch accounts before this machine is used for anything that matters.**

### Picking it up again

**With nothing set in the environment, SD reads `C:\ProgramData\SD\sd.conf`**
and therefore the installed tree at `C:\ProgramData\SD\sdsys` (changed
14 Aug 2026). It has the ACLs, so an unelevated session that has not signed out
since being added to `sdusers` cannot read it at all (§6).

**CORRECTED 14 Aug 2026, seventh session.** The recipe here was
`sd -start ; sd -ASDSYS` then `COUNT VOC`, from an ordinary window; **the
second half is now refused** with `sysmsg(10002)`, which is the point of §5.6.
`sd -start` still works unelevated — starting the server is `IsAdmin()`'s
question, not `IsElevated()`'s — so it is an **elevated** window for SDSYS, or
an ordinary one for the account named after your own Windows user.

```powershell
sd -start                    # ordinary window; check with Get-Process sdwind
```

**A scripted session must be piped, not `<`-redirected, and the pipe must send
one string with LF separators** — an array puts a phantom empty line after
every command that an `input` statement then eats. Both traps are in §6, with
the working form. Leave a prompt unanswered at end of input and SD spins at
full CPU (§6).

## 4. Verified vs unverified

Keep this split honest. It is the single most useful thing in the file.

### Verified by observation

**Entries are claim, decisive measurement, and nothing else.** Every one of
them has a HISTORY entry carrying how it was found and what it cost; that is
where to go when a claim here looks surprising.

**15 Aug 2026 — §7 STEP 1d HOLDS ON THE INSTALLED BINARY, NOT JUST THE BUILD.**
All four branches against `C:\Program Files\SD\usr\bin\sd.exe`, **run twice**:
the first pass had a daemon restarted by hand in the middle of it, so it was
redone start to finish from one unelevated session with every pid accounted
for. Second pass: `sd -start` on a live daemon → exit 1, `SD is already started
- sdwind is running as pid 7388`, `Get-Process` agreeing on **7388**, so the pid
translation works in the install too; daemon killed with the segment left →
exit 1, `SD did not shut down cleanly ... Run sd -stop`, and the seven `shm`
files **still there**, since clearing them is the user's decision; `sd -stop` →
exit 0, `shm` empty, no spurious warning; `sd -start` → up as pid 5500. The
14 Aug binary answered `SD is already started` to the killed-daemon case and did
nothing.

**The fifth branch too — the `EPERM` warning, on the install, with the daemon
started elevated by the owner and `sd -stop` run from an ordinary session.**
`sd -stop` exited 0, emptied `shm`, and printed `Warning: sdwind (pid 4620) is
still running.` with the privilege reason and the `Stop-Process -Id 4620 -Force`
command; `sdwind` was indeed still there afterwards. Corroborated the way §4
asks: `Stop-Process` from that same unelevated session was **refused, Access is
denied**, and the daemon measured **High integrity** (`S-1-16-12288`) against
the session's Medium (`S-1-16-8192`). **So the seventh session's claim stands
and the doubt raised against it was mine, not the file's** — the daemon killed
unelevated earlier that morning cannot have been the elevated one.

**15 Aug 2026 — THE BOOTSTRAP REFUSES AN UNELEVATED WINDOW, BEFORE DOING
ANYTHING.** Four unelevated runs: a **nonexistent** `--sysdir` drew the
elevation refusal and not `no such sysdir`, so the check is genuinely first;
`stage.py --bootstrap` left no staging directory; `--help` works on both;
`stage.py` without `--bootstrap` reached its `objdump` check, so plain staging
stays ungated. `os.getgroups()` here carries no 544 (§5.6.1). **The elevated
half ran too**, 06:31: both gates passed in an elevated window and the whole
bootstrap ran behind them — `SECOND.COMPILE` 0 errors throughout, 3,291 files
staged. What that run also exposed is the `ACCOUNTS/SDSYS` trap in §6.

**ADDED 14 Aug 2026, SEVENTH SESSION — `sd -start` AND `sd -stop` NOW TELL THE
TRUTH ABOUT `sdwind` (§7 step 1d), AND THE MACHINE SUPPLIED ITS OWN TEST CASE.**
It was found sitting in the broken state — segment and all six semaphores under
`C:\ProgramData\SD\shm`, **no `sdwind` process at all** — so the before and
after below are the same wreckage an hour apart, not a reconstruction.

Every branch was run. The **control** matters most: the installed 19:05 binary,
against that same wreckage, answered `SD is already started` — **with no full
stop**, which is `sdsem.c` line 86 and not the `bind_sysseg` string §7 step 1d
named. `get_semaphores(TRUE)` runs before the segment is looked at, so **a fix
confined to the two places the step named would have changed nothing the user
sees.** The new build then said the segment was stale and named `sd -stop`;
`sd -stop` emptied `shm` with no spurious warning; `sd -start` really started,
`sdwind` at Windows pid 14712; a second `sd -start` reported it already running
**as pid 14712**, matching `Get-Process` against the **87** it would have
printed untranslated (§6, the MSYS2-pid trap); and with the segment unlinked by
hand it fell through to the reworded semaphore message. `make sd` exits 0 with
no warnings, `gcc -fsyntax-only -std=gnu17 -Wall -Wformat=2` clean.
- **THE `EPERM` WARNING FIRED**, watched in two real console windows: an
  elevated `sd -start` from the repository build, then `sd -stop` from an
  ordinary PowerShell, which printed
  `Warning: sdwind (pid 5080) is still running.` and named the command to clear
  it. **Three confirmations, the third not designed for.** `Get-Process sdwind`
  answered **5080**, so `win_pid()` translates in this path too;
  `C:\ProgramData\SD\shm` was **empty**, so the teardown still happened and the
  warning is a warning and not a failure; and `Stop-Process -Id 5080` **from
  that same unelevated session was refused `Access is denied`**, so the
  message's account of *why* is corroborated by another mechanism.
- **Observed instead, and it is a defect the fix cannot reach:** with the
  segment unlinked under a live daemon, `sd -stop` reported success, exit 0,
  and left `sdwind` running. §6 carries it.

**§7 STEP 1c RUNS — 14 Aug 2026, seventh session, elevated console.** All five
programs compiled `0 error(s)`, catalogued, no `is not assigned a value` (so
`K$INTERNAL` and messages 10036–10039 resolve).

- `CREATE.ACCOUNT USER don` → `Windows account don already exists.  SD accounts
  create their own OS account`. The explicit refusal, on the account it exists
  to protect. Was `Create User Failed, OS Error: 1`.
- `DELETE.ACCOUNT sdacct1` → directory prompt, then `Windows account sdacct1
  does not exist, nothing to delete`; no group warning, `sdu_sdacct1` having
  already gone. **First run of `DELETE.ACCOUNT` in this codebase.**
- Checked after, not assumed: `user_accounts\sdacct1` gone, `ACCOUNTS` down to
  4 accounts + SDSYS, and `sdacct4`/`sdacct5` users and `sdu_` groups
  untouched.

**Measurements behind step 1c**, PowerShell rather than BASIC:

- **`/etc/passwd` and `/etc/group` are absent under both roots** the MSYS2
  runtime can use, while `getent passwd` returned `don` with his SID and
  `Get-LocalGroup` returned `sdu_sdacct5` with its SID, from the same machine.
  That is the whole basis of the three-helper trap in §6.
- **The `SD account` marker is real, and SD wrote it.** `Get-LocalUser sdacct5`
  returns a description of exactly `SD account`, 10 characters, stamped by
  `CREATE_USER` on 14 Aug 2026; `don`'s is empty. **This also proves a quoted
  value containing a space survives SD's `os.execute` path**, which is what
  `!is_sd_user` depends on and what nothing had previously shown.
- **The three answers `!is_sd_user` needs are distinct on real accounts**, run
  as PowerShell against this machine: `sdacct5` → 0 (SD's), `don` → 1 (**not**
  SD's, so `DELETE.ACCOUNT` would refuse to touch the machine
  administrator's login), `sdacct1` → 2 (absent — the half-removed case).
  `is_user`: `don` → yes, `sdacct1` → no. `is_group`: `sdu_sdacct5` → yes,
  `sdu_sdacct1` → no.

**14 Aug 2026, SIXTH SESSION — STEP 0, COMPRESSED TO ITS CONCLUSIONS** under §0
rule 5. HISTORY carries the working detail; these are the claims and what
decided them.

- **`LOGIN` and `CPROC` both compile, `0 error(s)` each, and are catalogued.**
  `gcat/$LOGIN` moved to 18:54:15 and 5,319 bytes — the pcode checked as
  written rather than as reported. Neither had been through a compiler before.
- **The new `LOGIN` is what runs**, dated exactly: the `LOGIN` compile printed
  `Warning: account SDSYS has no password set.` and the `CPROC` compile one
  command later did not, that line living in the deleted
  `authenticate.account`. `CPROC` then compiled *through* the new `LOGIN`, so
  the `sdusers` gate admits a member and `K$FORCED.ACCOUNT` reaches SDSYS.
  Only one warning, structural and not from the edit (§6, `IS_INSTALL`), and no
  `is not assigned a value` lines, so both pass the ERRGEN gate.
- **THE REFUSALS, which are the part that proves it.** From an **unelevated**
  session against the newly installed binaries: `sd` refused with
  `Account DON not in register` (`sysmsg(5018)`), `sd -ASDSYS` refused with
  `SDSYS Account access is restricted to privileged users` (`sysmsg(10002)`),
  while `sd -internal BASIC ...` **elevated** worked twice. An hour earlier the
  first of those put a machine administrator straight into SDSYS. **And
  `sysmsg(10002)` fired for the first time in this codebase's history.**
  **Both were then reproduced by the repository owner in a plain `cmd`
  console**, which mattered because the runs above went through a pipe and §6
  records a piped session as not equivalent to a real one. Incidental and worth
  keeping: extra words on those command lines were **ignored**, so a user
  refused at the door cannot smuggle a command in as an argument.
- **§5.6 IS COMPLETE — ALL FIVE RULES, BOTH `LOGTO` PATHS**, over ssh as
  `sdacct5`, a normal non-administrator account: `sd` gave a `:` prompt with
  nothing asked, `who` confirmed `3 SDACCT5`, `LOGTO SDSYS` was refused by the
  elevation gate (**an ssh session cannot be elevated** — the local-only
  property, tested rather than argued) and `LOGTO SDACCT1` by the restored
  `ACC$GROUP` test. **The two refusals come from different code**, which is why
  both were run; between them they cover every branch the session changed.
- **`CREATE.ACCOUNT` still passes 16 of 16** under the elevated-only gate,
  re-run as `sdacct3`. Its ssh-only restriction holds by the three decisive
  measurements: `LogonUser INTERACTIVE` refused 1385, `NETWORK_CLEARTEXT`
  admitted, ssh with the password SD set admitted. **That run does not test SD
  login and is easy to read as if it does** — all sixteen checks are
  Windows-side. Ignore `Command not found` in its section 1; the script's own
  header records it as a stray stderr artefact of how passwords are fed in.

**The foundations, observed 13 Aug 2026.** Nothing since has contradicted any
of them, and re-verifying them is not worth a session's time.

| What was shown | HISTORY entry |
|---|---|
| All six binaries compile, link and run; the client DLL builds with zero warnings under `-Wall -Wextra -Wpedantic` and exports 51 `SD*` symbols | "First native Windows build" |
| MSYS2 runtime probes: `fork`/`waitpid`, `termios`, `getpwuid`, `shm_open`+`mmap`, `sem_open` all work; **`shmget` and `semget` fail at runtime with ENOSYS** (§5.1) | "Runtime bring-up started; IPC verified" |
| The whole shared-segment lifecycle at 3 MB in the shape `sysseg.c` uses, then SD creating it itself; multi-process attach; the full start/stop/restart cycle leaving `/dev/shm` empty | "SD started for the first time", "SD runs. Full bootstrap completes" |
| The complete bootstrap, `SECOND.COMPILE` compiling 204 then 207 programs with no errors, `COUNT VOC` 431–432, `SELECT VOC` | "SD runs. Full bootstrap completes" |
| **`@ds` is correct for stage 1** — 204 programs compiled with `dir.separator` hardcoded to `/` (still live for stage 2, §6) | "SD runs. Full bootstrap completes" |
| Account passwords end to end: salt, Argon2 derivation, `!CRED_SET`/`!CRED_VERIFY` round trip, case-insensitive names, fail-closed on unknown account and empty password, no trace of the password in the record | "Account credentials: register, helpers and login" |
| **The whole `LOGTO` grant suite in both directions**, including the SDSYS exception belonging to the account you stand in, and `@logname` surviving every hop | "LOGTO is gated by grants, and the shipped binary is verified" |
| Administrator rights became the SDSYS account's, and a demonstrated privilege escalation was closed | "Administrator rights become the SDSYS account's" |
| **Drive-letter paths work after the `sdrealpath()` fix** — all five spellings open the same file; accounts under `C:\ProgramData\SD` work end to end | "Accounts move to ProgramData, and SD learns to read a Windows path" |
| **The data tree needs no C source** — `SECOND.COMPILE` clean with `gplsrc`, `gplobj` and `gplbld` all absent; `gen_includes.py` reproduces the generators it replaces | "The data tree no longer holds C source" |
| **SD needs the MSYS2 DLLs, not the MSYS2 shell**, and the staged tree runs with MSYS2 entirely off PATH — four DLLs, only `kernel32` and `ntdll` from Windows | "SD outside the MSYS2 shell", "Staging script written" |
| `terminfo` regenerates byte identically with and without the `O_BINARY` correction, so that change is protective rather than a repair | "Correction: the `O_BINARY` override was not corrupting data" |

**`IsAdmin()` works in the linked binary, in both directions**, and that is
worth restating rather than filing: `sd -start` refused with "Command requires
administrator privileges" while the group was absent and got past the check
once built against a group the token holds. The probe recipe in §6 is the only
way to see this system as a non-administrator on a machine whose account is one.

#### The installed system

- **A GENUINE FIRST INSTALL WORKS, AND THE FILES WERE COUNTED** — 14 Aug 2026,
  on a machine cleaned first, with the installer rebuilt from the tracked
  `gplbld/sd.iss`. **3,264 files** under `C:\ProgramData\SD\sdsys` against a
  broken run's 16, 129 `gcat` entries, 11 `GPL.BP.OUT`, and a `Compare-Object`
  of every staged path against every installed one reporting **no differences
  in either direction**. It then ran: `COUNT VOC` **431**, `LIST ACCOUNTS`
  giving `Pathname: C:\ProgramData\SD\sdsys`, `WHO` `3 SDSYS`. Everything else
  the installer owns was confirmed on the same run — `sdusers` with
  `GITORLI\don` in it, `user_accounts`/`group_accounts`/`shm`, exactly one PATH
  entry, no `gplbld` in the data tree, `sd.conf` present.

- **CORRECTED 14 Aug 2026, and the lesson outlives the fix.** An earlier claim
  that the installer worked was true of the **upgrade** path only. A genuine
  first install **produced a broken database**: `Check: DataTreeAbsent` is
  evaluated *per file*, so the first file created the directory, every later
  evaluation answered False, ~3,260 files were silently skipped — and **Setup
  still exited 0**. `InitializeSetup` now caches the answer once. **An install
  test that does not COUNT what was installed proves very little.**

- **THE INSTALLED SYSTEM RUNS AS AN ORDINARY USER** — 14 Aug 2026 after a
  reboot, from a normal unelevated window with nothing set in the environment:
  `sd -start`, `COUNT VOC` 431, `WHO`, `sd -stop`, `sdwind` appearing and
  going. The first time SD was used the way a user would use it, and it closes
  three things: **§5.6.1 in the real world**, `IsAdmin()` having admitted an
  administrator who had not elevated; **§5.7's ACL model from the user's
  side**, the token now carrying `sdusers`; and **the sign-out requirement**,
  which is real and sufficient — the same session had been refused on every
  path inside `C:\ProgramData\SD` before the reboot, and nothing else changed.

  **What it does not show:** `sd -start` had to be typed. An installed system
  does **not** come up on boot — there is no service (§5.7) — so after every
  restart someone must start SD by hand. That is now the most visible gap in a
  system that otherwise installs and runs.

- **The upgrade path works too, and it is a different path.** Over an existing
  data tree, `/VERYSILENT`: the `sdsys` tree **does not appear in the install
  log at all** and the database was untouched; the four MSYS2 DLLs and
  `etc\fstab` land in `usr\bin`, and an `Uninstall` key puts SD in Settings.

- **An installed system finds its configuration with nothing set in the
  environment** — reading `C:\ProgramData\SD\sd.conf` through `%ProgramData%`.

- **The uninstaller runs, and keeps the data.** `/VERYSILENT`, exit 0:
  `C:\Program Files\SD` and the Settings > Apps entry removed,
  **`C:\ProgramData\SD` left completely intact**. It used to leave the PATH
  entry behind, which Inno cannot undo by itself because `[Registry]` appends
  with `olddata`; **fixed** by `RemoveFromPath` at `usUninstall`. It leaves the
  `sdusers` group deliberately — a kept data tree is ACL'd to it.

- **The daemon starts on an installed system, and it is called `sdwind`.** It
  had **never** started from an install. `start_sd()` asks `exe_directory()`
  and launches it from beside the running executable, so the two cannot drift
  apart: `sd -start` from `C:\Program Files\SD\usr\bin\sd.exe` left
  `sdwind.exe` running out of that directory, while `<sysdir>\bin` held only
  `pcode, pcode.old` — the old path could not possibly have worked. The
  daemon's own `check_lost_users()` had the same defect and is fixed with it,
  not separately verified. **Why it was silent is the trap in §6.**

- **The ACLs are right, and this time that was checked from the outside.** The
  data tree carries exactly `GITORLI\sdusers:(OI)(CI)(M)`,
  `BUILTIN\Administrators:(OI)(CI)(F)` and `NT AUTHORITY\SYSTEM:(OI)(CI)(F)`,
  with no `BUILTIN\Users` — and an unelevated session whose token does not carry
  `sdusers` was refused on every path inside `C:\ProgramData\SD`, so the lockout
  is real and not just a listing. **`Test-Path` on the directory itself still
  answers True** (§6). Check the contents, or you will conclude the ACL never
  applied.

- **OpenSSH Server installs, and `sshd` runs** — `Installed` after a reboot, so
  the corrected `Add-WindowsCapability` line works and the brace bug (§6) was
  the whole of it. `install-ssh.ps1` then reported `sshd is Running,
  StartType=Automatic`, 2 listeners on port 22, the firewall rule enabled, and
  `C:\ProgramData\ssh\sshd_config` created — which sshd writes on first start,
  and is the earliest point at which `AllowGroups` could be edited into it.

  **And it exposed an installer defect that is now fixed.** The capability
  installed but the **service did not exist until after a reboot**, so a step
  running `Add-WindowsCapability`, `Set-Service` and `Start-Service` in one
  breath reported total failure for a success needing a restart.
  `install-ssh.ps1` now **exits 2 for "restart required"**.

- **`sd.iss` compiles with all of the above in it** — `ISCC.exe` exit 0. That is
  the *only* claim: see §4 Unverified for what compiling does not show.

#### Elevation, and who may reach SDSYS

- **WINDOWS DOES LIMIT WHO MAY ELEVATE, AND `Administrators` IS THE SUDOERS
  FILE.** Measured 14 Aug 2026, fifth session, on this machine's live policy.
  **This is the measurement §5.6's reversal rests on**, and it contradicts the
  belief that sent the port down the password route:

  | Setting | Value | What it means |
  |---|---|---|
  | `EnableLUA` | 1 | UAC on, tokens filtered |
  | `ConsentPromptBehaviorUser` | 3 | **a standard user is prompted for an ADMINISTRATOR's credentials** on the secure desktop — it cannot elevate as itself |
  | `ConsentPromptBehaviorAdmin` | 5 → **now 0**, see below | an administrator gets a consent prompt only |
  | `LocalAccountTokenFilterPolicy` | **not set** | the default remote restriction applies — see below |
  | `FilterAdministratorToken` | not set | — |

  **The UAC slider moves, so read it rather than remembering it.** The sixth
  session recorded `ConsentPromptBehaviorAdmin` at **0** and
  `PromptOnSecureDesktop` at **0**, the owner having moved the slider to "Never
  notify"; the seventh session read **5 and 1** — back at the Windows default,
  so **elevating raises a consent prompt on the secure desktop again**, which
  is what makes the elevated half of a test something a person has to be asked
  for rather than something a session can arrange. **THE ACCESS MODEL IS
  UNAFFECTED EITHER WAY AND THAT WAS MEASURED, NOT ASSUMED:** token filtering
  is `EnableLUA`'s doing and `EnableLUA` is 1 in both readings. In an ordinary
  session belonging to `don`, an administrator, `S-1-5-32-544` is **absent from
  the process token** and `id -G` returns no 544, so `IsElevated()` answers
  false where it should. Only the *prompt* changes.

  **`EnableLUA = 0` WOULD BREAK IT, AND WOULD ALSO MAKE §7 STEP 0e MEANINGLESS.**
  With no split token every administrator session is elevated, so `IsElevated()`
  collapses into `IsAdmin()`, plain `sd` puts any administrator into SDSYS
  always, and **SDSYS becomes reachable over ssh**, contradicting the local-only
  decision in §5.6. Worse for the work: **the refusal half of step 0e could
  never fire**, because no session would be unelevated, and the tests would
  record false passes. **The test machine must have `EnableLUA = 1`.**

  So a normal SD account, which `CREATE.ACCOUNT USER x` deliberately leaves out
  of `Administrators` (§4 above), **cannot elevate and therefore cannot reach
  SDSYS**. That is the Linux rule, enforced by the OS.

- **AN UNELEVATED ADMINISTRATOR'S TOKEN CARRIES `Administrators` AS "GROUP USED
  FOR DENY ONLY".** Observed the same session, in an ordinary PowerShell window
  belonging to `don`, who is in `Administrators` in the SAM:

  ```
  Elevated now: False
  BUILTIN\Administrators   Alias   S-1-5-32-544   Group used for deny only
  ```

  **That string is the whole of the distinction §7 step 0 needs.** It is the
  same fact §5.6.1 measured on 14 Aug with a C probe and read the other way:
  `getgrouplist()` answers "is an administrator", the token answers "is elevated
  right now", and the new model wants both — see §5.6.1's correction.

- **`sudo.exe` is present on this build and enabled in inline mode**
  (`Enabled = 3`). It was enabled by hand on 14 Aug 2026; **the installer does
  not install or enable it** — `gplbld/sd.iss` does not mention `sudo` anywhere,
  checked the same session. It is not needed: "Run as administrator" produces
  the same elevated token on every Windows version.

#### The account model and the ssh-only model

- **The five new OS-facing BASIC helpers work, and the shell is PowerShell.**
  Observed 14 Aug 2026 from inside SD, then re-observed after `op_sh.c` was
  changed to default `SH`/`SH1` to PowerShell — every case still passed, so
  `OS.EXECUTE` reaches PowerShell and the exit status carries back through
  `OS.ERROR()` with bash out of the loop entirely.

  **`!valid_os_path`** 16 of 16 — Windows, POSIX and mixed paths pass; empty,
  over 255 characters, and every shell metacharacter refused. **`!is_grp_member`**
  7 of 7, including the rev 0.9.0 "own group account" case, closing the §6 trap
  that had it answering no for everyone. **`!ps_script`** 5 of 5, carrying a
  secret off the command line and returning `exit 42` as 42, a `throw` as 1, an
  empty script as -1.

  All ten changed or new `GPL.BP` programs compiled with 0 errors and no "not
  assigned a value" warnings. **One measurement decided the design:**
  `Invoke-Expression` propagates a script's `exit` status where
  `& .\script.ps1` does not — 7 through the first, 1 through the second — and
  it is not subject to the execution policy, so nothing needs
  `-ExecutionPolicy Bypass`.

- **A Windows administrator is an SD administrator, tested two ways.** From an
  **unelevated** session belonging to a machine administrator — the case the
  previous test would have got wrong. Positive: the shipped build ran
  `sd -start`, the daemon came up, `sd -stop` took it down. That is decisive
  rather than incidental, because **gid 544 is not in `getgroups()` in that
  session**, so it can only have been found through `getgrouplist()`. Negative:
  `sd.c` and `linuxlb.c` rebuilt with `-DSD_ADMIN_GID=99999` refused with
  "Command requires administrator privileges", exit 1. See §5.6.1.

- **`CREATE.ACCOUNT` RUNS, AND IT HAD NEVER BEEN RUN BEFORE.** From an elevated
  session, both halves of the account are made — Windows user enabled, in
  `sdusers` with its `sdu_` group, account directory, VOC, `$HOLD`,
  `$SAVEDLISTS`, BP, private catalogue, `ACCOUNTS` record — and the
  `ADMINISTRATOR` keyword does exactly what §5.6.1 decided: **without it the
  account is not in `Administrators`, with it it is.** The add went in **by
  SID**, `!os_group` accepting `S-1-5-32-544`, because the name is localised.
  `CREATE_USER`, `SET_PASSWD` and `OS_GROUP` have executed against real Windows
  accounts. **`DELETE.ACCOUNT` and `MODIFY.ACCOUNT` still have not.**

- **The deny-logon rights are applied correctly, and nothing else is
  disturbed.** `gplbld/deny-logon.ps1` as the installer invokes it:
  `SeDenyInteractiveLogonRight` went from `Guest` to `sddenyprobe,Guest`,
  `SeDenyRemoteInteractiveLogonRight` from absent to `sddenyprobe`, and
  **`SeDenyNetworkLogonRight` was left untouched** — the row that matters, ssh
  authenticating with a network logon (§5.6.2). The surviving `Guest` entry is
  the argument for `LsaAddAccountRights` over `secedit` shown working.
  Idempotent; a missing group exits 1 saying so.

  **A caveat on reading this back.** `secedit /export` writes resolvable local
  groups **by name**, not by SID, so a verification that greps for a SID
  reports "not present" when it is. That is what the first attempt did.

- **THE SSH-ONLY MODEL WORKS.** Observed by `gplbld/verify-sshonly.ps1` against
  a real Windows account. This is §5.6.2, which had been decided, built,
  shipped in the installer and never once exercised. Thirteen checks, all
  passing:

  | | control, in no SD group | after joining `sdsshonly` |
  |---|---|---|
  | `LogonUser` INTERACTIVE — the console | admitted | **refused 1385** |
  | `LogonUser` NETWORK_CLEARTEXT — ssh password auth | admitted | admitted |
  | **`ssh` with a password** | admitted | **admitted** |
  | `ssh` with a key | admitted | admitted |

  **The bottom two rows of the middle column are the whole design.** The console
  is closed by the deny rights and ssh is not, measured on the same account
  minutes apart with nothing else changed. `1385` is
  `ERROR_LOGON_TYPE_NOT_GRANTED`. `ssh` **ran a shell**, not merely
  authenticated — the test asserts on `whoami` — and the `OpenSSH/Operational`
  log recorded `Accepted password` and `Accepted publickey ... ED25519` from the
  installed service at the same moment, so the verdict does not rest on the
  test's own reporting.

  **Why there is a control column at all.** The first run refused the key login
  on *both* sides. Measured alone, the treatment side would have read as "the
  deny rights break ssh" and §5.6.2 would have been abandoned on a false
  result. An equal failure on both sides cannot have been caused by the thing
  that differs between them. **Keep the control.**

- **A brand new Windows account cannot use ssh KEY authentication until it has
  logged in once.** A property of Windows, not of anything here: an account that
  has never logged on has no profile and no home directory, and Win32-OpenSSH
  resolves `AuthorizedKeysFile .ssh/authorized_keys` relative to the home
  directory, so a planted key is never read. Observed in both directions — the
  key refused twice with no prior login, then accepted after one password login
  created the profile, with group membership identical either way. **It applies
  to accounts `CREATE.ACCOUNT` makes.** Password authentication is unaffected
  and works immediately; only keys wait.

- **`BUILTIN\Users` membership is not required for an SD account.** Asked
  because `New-LocalUser` joins no group and `CREATE_USER` adds none, so an SD
  account is in `sdusers`, `sdu_<name>` and `sdsshonly` and nothing else.
  Measured rather than assumed: the account logged in over ssh and ran `whoami`
  **before** `Users` was added, and adding it changed nothing.

- **`CREATE.ACCOUNT`'S SSH-ONLY BRANCH WORKS, AND THE RESTRICTION IT APPLIES
  HOLDS. 16 of 16, END TO END.** Observed 14 Aug 2026 by
  `gplbld/verify-createaccount.ps1 -Account sdacct2` from an elevated window,
  against the install rebuilt the same session. `CREATEA` line 400 had never
  executed before — `sdsshonly` did not exist the first time the verb ran.

  What SD made: an **enabled** Windows account, in `sdusers`, `sdu_sdacct2` and
  `sdsshonly` and **not** in `Administrators`; message 10034, `sdacct2 may sign
  in over ssh only`; the account directory with `VOC`, `$HOLD`, `$SVLISTS`, `BP`
  and a private catalogue; and the `ACCOUNTS` record. Then the same three
  measurements that proved §5.6.2, on an account **SD created** with a password
  **SD set**:

  | Measurement | Result |
  |---|---|
  | `LogonUser` INTERACTIVE (console) | **refused 1385** |
  | `LogonUser` NETWORK_CLEARTEXT | **admitted** |
  | real `ssh sdacct2@localhost whoami` | **admitted** |

  **So the chain is closed:** SD creates the account, SD restricts it, and the
  restriction holds when tested from outside. That is the whole of the ssh-only
  model except RDP, demonstrated on an account created by the verb rather than
  by a test harness. It also settled `SET_PASSWD` end to end — the password SD
  generated and set was the one ssh accepted.

  **`Warning unable to setgid bit on Group Folder, status: 1` prints on every
  account creation.** Expected and harmless — the `sudo chmod g+s` Linux-ism in
  `CREATEA` (§5.16, §7 step 1e), now observed rather than predicted.

- **`AllowGroups` IS APPLIED AND ENFORCED, AND THE ADMINISTRATOR IS NOT LOCKED
  OUT.** Observed on this machine's live `C:\ProgramData\ssh\sshd_config`.
  **This was the lockout risk, and it is now measured rather than reasoned
  about.** `allow-ssh-groups.ps1 -Installed` exited 0 and wrote
  `AllowGroups sdusers GITORLI\sdusers Administrators GITORLI\Administrators`
  between its markers **immediately before the `Match` block** — the placement
  `verify-allowgroups.ps1` exists to guarantee, confirmed in the live file. The
  original is at `sshd_config.before-sd`; `sshd` restarted and came back
  Running.

  Then control and treatment, by real ssh connections with no password handled,
  so the **reason** is read out of the `OpenSSH/Operational` log rather than the
  exit code:

  | account | groups | sshd logged |
  |---|---|---|
  | `don` | `sdusers` + `Administrators` | `Connection reset by **authenticating user** don` |
  | `CodexSandboxOffline` | neither, **and enabled** | `**not allowed because none of user's groups are listed in AllowGroups**` |

  **The client message is identical in both cases** —
  `Permission denied (publickey,password,keyboard-interactive)`. That is the
  trap, and it is why this was done through the log: only the log distinguishes
  refused-by-group from failed-to-authenticate, marking a group-refused account
  `invalid user` against `authenticating user` for an allowed one.

  So the patterns match a real member, a non-member is refused for exactly the
  intended reason, and the machine's own administrator kept ssh. An `sdsshonly`
  account is in `sdusers` too, so ssh-only accounts are allowed by construction.

  **A first control was confounded and is recorded because it nearly passed for
  evidence.** `WDAGUtilityAccount` is **disabled**, and produced a bare
  `Connection reset` with no log line — a different-looking failure that could
  as easily have been the disabled account as the group check. It was redone
  with an **enabled** non-member, which is the one in the table.

- **`allow-ssh-groups.ps1` edits `sshd_config` correctly** — 20 checks by
  `gplbld/verify-allowgroups.ps1` against
  `C:\Windows\System32\OpenSSH\sshd_config_default`, the template `sshd` copies
  on first start. **The test needs no elevation, no `sshd` and no network**,
  because that template is world readable, so it re-runs on any machine; it
  lifts the functions out of the shipped script by parsing it, so it cannot
  drift from the code it checks. The checks cover: the block lands **before**
  the first `Match`; exactly one `AllowGroups` survives three applies; remove is
  an exact inverse of add; a foreign `AllowUsers`/`DenyUsers`/`AllowGroups`/
  `DenyGroups` is detected and not merged into (§5.9), while
  `AllowAgentForwarding` and `#AllowGroups` are correctly *not* taken for
  policy, and SD's own block is not mistaken for a foreign one.

  **It found a real defect on the first run** — a readability blank line falling
  outside the markers, so every apply/remove cycle grew the file by a line (§6).
  Also observed unelevated: **`-Check` resolves the administrators group from
  `S-1-5-32-544`**, which is the half that is wrong on a localised Windows if
  written as a literal.

### Not verified — treat as unknown

- **No staged tree has yet been built with the `ACCOUNTS/SDSYS` fix** (§6).
  The next `stage.py --force --bootstrap` is the first, and `SECOND.COMPILE`
  will be compiling the staged sources for the first time — expect differences,
  and expect `check_no_stage_paths` to have something real to say.
- **`MODIFY.ACCOUNT` has never been run.** `CREATE.ACCOUNT` and
  `DELETE.ACCOUNT` both have (§4 Verified).
- **`DELETE.ACCOUNT`'s "SD created it" branch is untested** — the prompt and
  `!delete_user`. Only the "no such Windows account" branch has run.
  `sdacct4` is the disposable case to test it with: real Windows account,
  password unknown to anyone.
- **`CREATE.ACCOUNT ... ADOPT` is untested**, and nothing calls it (§7 1f).
- **RDP refusal, and it CANNOT BE TESTED ON THIS MACHINE.** The last unobserved
  claim in §5.6.2 (§4 Verified covers the rest).
  `SeDenyRemoteInteractiveLogonRight` is confirmed **applied** to `sdsshonly`
  in machine policy, but nothing has watched it refuse a session.

  It cannot be automated — there is no `LogonUser` logon type corresponding to
  RDP's logon type 10, so only a real Remote Desktop connection exercises the
  right.

  **THIS MACHINE CANNOT RDP TO ITSELF. Measured 14 Aug 2026, three attempts**,
  so do not spend more time on it here. All three answered:

  ```
  Your computer could not connect to another console session on the remote
  computer because you already have a console session in progress.
  Error code: 0x708
  ```

  | attempt | credentials offered | result |
  |---|---|---|
  | `mstsc /v:localhost` | the signed-in user's own | `0x708` |
  | `mstsc /v:localhost` | the probe account's | `0x708` |
  | `mstsc /v:10.0.0.3` (own Wi-Fi address) | the probe account's | `0x708` |

  **The refusal comes before any credential prompt**, so which account is
  offered never enters into it, and addressing the machine by its LAN address
  rather than `localhost` makes no difference either. RDP was enabled
  throughout — `fDenyTSConnections` 0, `rdp-tcp` listening, inbound firewall
  rules on for all profiles, all checked the same day.

  That is the whole of what was observed. It is deliberately not turned into a
  statement about how many sessions Windows permits: two such statements were
  derived from this error already and both were wrong (HISTORY.md, two
  `Correction:` entries of 14 Aug 2026).

  **So the test needs a separate client machine** — §7 step 2. Run
  `verify-sshonly.ps1 -Keep` on the machine under test and RDP to it from a
  different one.

- **That SD itself works over an ssh session** — `sd -ASOMEACCOUNT` typed at a
  real terminal reached over ssh. The ssh transport is proven and SD is proven,
  but not the two together, and it is also the oldest open question in this
  section: how the MSYS2 tty layer behaves at a real console rather than with
  redirected stdin.

- **Which of `AllowGroups`' four patterns actually matched.** It is applied and
  enforced (§4 Verified), but `AllowGroups` is a union and all four patterns
  were written deliberately, so the bare and `COMPUTER\` forms cannot be told
  apart from that result. Deliberate — see §5.6.2 — and it stays unknown unless
  somebody narrows the list on purpose. **Also unknown: what the installer's
  own path through it does**, since the measurement ran the script by hand on a
  machine that already had OpenSSH and so never sees the tick box.

- **The installer's own behaviour with the new options.** `sd.iss` compiles
  (§4 Verified) and that is all. Nobody has seen the reworded closing dialog,
  the `installssh\allowgroups` subtask appear under its parent, or
  `ApplyAllowGroups` report any of its three outcomes. Compiling an Inno script
  proves the Pascal parses, nothing more — and the two defects this file has
  already recorded in that script (the brace bug, the per-file `Check`) both
  compiled perfectly.

- **Whether `OS.EXECUTE` works at all on an installed system.** It almost
  certainly does not — see the shell trap in §6.

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
- **The installer on a machine with no development tree.** The first-install
  path itself is now verified here (§4 above), so this is no longer "the least
  tested part of the system" — but the accidental-dependency question is
  untouched, and it is precisely how `gplsrc` stayed in the data tree.
  `installsdai.sh` is entirely Linux and is not being ported (§5.9).

  **The `sdadmins` prediction that used to sit here is gone**, and not by being
  tested: §5.6.1 made `IsAdmin()` gate on Windows `Administrators`, which
  always exists, so there is no longer a group a clean machine could be missing.

- **What the daemon actually does for the system.** Fixed and verified
  14 Aug 2026 (see §4 Verified), so what remains unknown is only its *effect*:
  `check_lost_users()` shells out to `sd -cleanup` every five minutes when it
  finds a user table entry whose process is gone. That path has never been
  exercised — no session has been killed and the cleanup watched — and it was
  unreachable until today, since the daemon was never running. It matters for
  the API (§7 step 6), which is the daemon's other reason to exist.

- **Why `errlog` stayed empty** through a full start / command / stop cycle on
  the freshly installed tree, 14 Aug 2026, where earlier sessions saw
  "User n (pid, don)" lines written to it. Still empty after the daemon was
  fixed, so it is not explained by that. Not chased.

## 5. Decisions and why

Do not undo these without reading the reasoning.

### 5.1 POSIX IPC replaces System V

System V IPC compiles and links on MSYS2 then fails at runtime with ENOSYS
(§6); native Windows has none at all. POSIX named shared memory and semaphores
work on both and are the right direction for stage 2 anyway, since POSIX shared
memory is backed by `CreateFileMapping`. `sysseg.c`, `sdidx.c` and `sdwind.c`
use `shm_open`/`ftruncate`/`mmap`/`munmap`; `sdsem.c` uses
`sem_open`/`sem_trywait`/`sem_post`; names come from `SD_POSIX_SHM_NAME` and
`SD_POSIX_SEM_FMT` in `sddefs.h`.

Two spots needed more than substitution — `munmap` must be told the mapping
length that `shmdt` derived from the address, so it is recorded at attach, and
`stop_sd()` waited on the System V attach count, which POSIX does not expose,
so it polls the user table with `kill(pid, 0)`. Full reasoning in the HISTORY
entry "First native Windows build".

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
has had its Windows branches removed — `LOGIN` 16 references to none, `CONFIG`
5 to none, `CPROC` 5 to none, `CREATEA` 4 to none, `PARSER` 3 to none. The
logic still exists in the external `GPL.BP` tree (§2) and what each file did is
listed in the HISTORY entry "Surveyed the BASIC layer (GPL.BP)". Start with
`CPROC`'s `dir.separator`, because compilation depends on it (§6) — and note
`LOGIN`'s Windows branch forced administrator rights on any console session,
which §5.6 deliberately does not adopt.

Order matters: restoring the BASIC branches while `SYSTEM(91)` still returns
zero is harmless, but flipping `SYSTEM(91)` first turns on paths that are no
longer there.

### 5.5 The Linux privilege model does not survive the move

Background for §5.6, which replaces it. `IsAdmin()` was `getuid() == 0` and
`SYSTEM(27)` returns `getuid()`, which is 197609 under MSYS2 — never zero, so
every privilege test answered the same way permanently and the symptom was a
refusal from code that looks correct (§6). `EUID_SET`/`EUID_RESTORE` were the
mechanism the root branch used, reaching `sdext_eguid.c` through `SDEXT`;
Windows has no equivalent short of `LogonUser` plus `ImpersonateLoggedOnUser`,
which is the shape §5.7's service model needs. Full site-by-site table in the
HISTORY entry "Surveyed every BASIC to C linkage".

### 5.6 Identity model: accounts with passwords (13 Aug 2026), and administration is the OS's (14 Aug 2026)

**REVERSED 14 AUG 2026, FIFTH SESSION. BUILT IN THE SIXTH — §7 step 0 a-d.
NOT COMPILED AND NOT RUN**, so everything below describes source, not observed
behaviour.
Decision from the repository owner: **mimic the Linux version.** SD login takes
no password; the operating system has already authenticated you, and SD asks
the OS who you are. The owner verified the Linux behaviour in a Debian virtual
machine the same day, and it is also in this repository's own pre-port `LOGIN`
at commit `f9edab0`, which is the authority to read before building it.

**Why it was not done this way in the first place**, recorded because it is the
whole reason two sessions went another way: the owner's understanding was that
**Windows cannot limit who may run `sudo`** — no sudoers file — so mimicking
Linux would hand SDSYS to everybody. **That is not the case**, and the
measurement is in §4 Verified. `Administrators` membership *is* the sudoers
file, and SD already maintains it.

The model, in five rules:

| | |
|---|---|
| `sd`, no account named | you land in **the SD account with your own name** |
| no SD account of that name | refused — `sysmsg(5018)`, "Account %1 not in register" |
| not in `sdusers` | refused at the door — `sysmsg(5009)`, "not registered for SD use" |
| **`sudo sd`, or any elevated session** | **straight into SDSYS**, no account named and no password |
| `sd -Aname` | `ACC$GROUP` must name a group you are in; SDSYS additionally needs elevation — `sysmsg(10002)` |
| **an elevated session, at either test** | **passes without the group check**, in `LOGIN` and in `LOGTO` alike. Not a convenience — `ACCOUNTS/SDSYS` names a group Windows does not have, so the check would refuse administration to everybody (§6). Linux root does not pass it either |

**All five messages already exist** (5009, 5018, 10002, 10003), and 10002 has
never had a caller.

**What makes it work on Windows was already built** — the write side of this
model was never removed, only its readers: `ACC$GROUP` is written as
`sdu_<name>` on **every** account (`CREATEA` 455), the `sdu_<name>` group is
created by `CREATE.ACCOUNT` and `sdusers` joined at `CREATEA` 345 (both
verified, §4), `!is_grp_member` works 7 of 7, and the sudoers list is
`Administrators`, which `CREATE.ACCOUNT USER x` stays out of and
`... ADMINISTRATOR` joins. **Correction:** §5.6.1 once called `ACC$GROUP` "dead
but still populated on old records"; it is written correctly on every new
account and only its reader had been deleted.

**What this reverses**, from `272ce92` "Require an account password at login",
built over two sessions: **no password is asked for at `sd`, at `sd -Aname` or
at `LOGTO SDSYS`**, and the SDSYS re-prompt is gone — the gate is elevation,
applied at login, so there is nothing to step up into.

**The credential machinery is NOT deleted** (owner's decision, 14 Aug 2026).
`$CRED`, `!CRED_SET`, `!CRED_VERIFY` and `SET.PASSWORD` all stay: **the API is
a separate door and does require an account password**, on top of the ssh
tunnel (§8). The register changes owner rather than becoming dead code.

**Understand what the security position now rests on.** Nothing in SD checks a
secret at login; access is entirely OS group membership. That is **not** a
weakening, and §5.7 already explains why: every SD process opens the database
under the invoking user's own token, so "account passwords organise access;
they do not secure it". The password model implied a boundary the filesystem
never enforced. This states the real position instead of dressing it up.

**One property to accept consciously.** `Administrators` is machine-wide, so
anyone in it for an unrelated reason — the machine's own administrator, a
domain admin, an IT tool's service account — gets SDSYS. Linux sudoers is
machine-wide too, so this is parity rather than a Windows weakness, but it
should be a decision rather than a discovery.

---

**The superseded 13 Aug 2026 decision, in three lines**, because 5.6.1 and
5.6.2 are written on top of it. **SD has no concept of users, only accounts.**
Every account carried its own password (**reversed for login, retained for the
API**); SDSYS was the only administrator (**reversed** — an *elevated* Windows
administrator); OS groups were dropped from SD's logic entirely (**reversed** —
they are now the whole model: `sdusers` at the door, `ACC$GROUP` per account,
`Administrators` for SDSYS). §5.5 records the Linux model it replaced, and the
full reasoning is in HISTORY under "Moved from PROJECT_STATUS §5.6".

### 5.6.1 A Windows administrator is an SD administrator (decided 14 Aug 2026)

**Decision from the repository owner, 14 Aug 2026**, reversing "SDSYS is the
only administrator" above and settling §8's `IsAdmin()`/`sdadmins` question,
which had become blocking. In the owner's words: if you can log in as an
administrator to the OS, you are an administrator of SD; the installer has to
be an administrator, so the person who installs SD is an SD administrator
without any further step.

**What forced it.** Three problems turned out to be one: the installer creates
`sdusers` and never `sdadmins`, so a clean machine got an install nobody could
start; the postinstall "set the SDSYS password" step could not work; and
`IsAdmin()` was still the real source of `K$ADMINISTRATOR` despite §5.6 saying
OS groups were gone, so `sd -internal` **already** admitted an OS administrator
without a password. The behaviour and the written decision had drifted apart,
and this closed the gap in favour of the behaviour.

**What "administrator" tests, and it is not elevation.** Measured 14 Aug 2026
with a C probe, from an unelevated session belonging to a machine
administrator:

| Call | Source | Contains Administrators? |
|---|---|---|
| `getgroups()` | the process token | **NO** — a UAC-filtered token carries it "deny only", and Cygwin drops it |
| `getgrouplist()` | the account's groups in the SAM | **YES** |

`IsAdmin()` used `getgroups()`, which would have meant "elevated", not
"administrator". It uses `getgrouplist()` now.

**PARTLY REVERSED 14 Aug 2026, fifth session — both answers are wanted, for
different questions** (§5.6, §7 step 0). `getgrouplist()` stays as `IsAdmin()`
and keeps gating `sd -start`, because starting the server should not demand
elevation of somebody already an administrator. But `K$ADMINISTRATOR`, which
decides who reaches SDSYS, must mean **elevated**, so it needs the token
answer: hence `IsElevated()` beside `IsAdmin()` rather than a change to it.
The table above turned out to describe two useful tests, not a right one and a
wrong one.

**Test gid 544, never the name.** Cygwin maps built-in SIDs to their RID, so
`getgrnam("Administrators")` resolves to 544 and back — but **it is renamed on
a localised Windows**, so the number is portable and the name is not.
`gplbld/sd.iss` writes `*S-1-5-32-544` for `icacls`, and `CREATEA` does the
same at its Administrators add.

**Consequences to know.**

- Actions needing an elevated token still fail when unelevated — creating a
  Windows account among them. An SD administrator is able to *administer SD*,
  not to do every administrative thing; §5.7's service model is the answer.
- **`sdusers` is unaffected and still needed.** It grants file access to
  `C:\ProgramData\SD`, which is an ACL question, not an authorisation one. An
  elevated administrator reaches the tree through the `Administrators` ACE
  without it; everyone else needs the group, and still needs to sign out and
  back in after being added (§6).
- **Normal accounts are standard local accounts.** Administrators are made
  deliberately, with a keyword.
- **The SDSYS password stopped conferring administration, and then stopped
  existing.** This bullet said it "still guards the SDSYS account, and every
  account still carries its own password"; the reversal at the top of §5.6
  removed console passwords altogether. Corrected 14 Aug 2026, seventh session.

**Where the credential machinery lives**, built 13 Aug 2026 and now the API's
rather than the console's (§7 step 6). Salt generation (`SD_SALT`, 100), Argon2
derivation (`SD_KEYFROMPW`, 101) and the masked `IN$PASSWORD` prompt were
already in C, so salt-derive-compare needed no new C code:

| Piece | Where |
|---|---|
| `$CRED` register, keyed by account, `CRED$SALT` + `CRED$VERIFIER` | `<sysdir>/$CRED`, defines in `INT$KEYS.H` |
| `!CRED_SET` / `!CRED_VERIFY` | `GPL.BP/CRED_SET`, `GPL.BP/CRED_VERIFY` |
| `SET.PASSWORD [account]` verb | `GPL.BP/SET_ACC_PASSWORD` |

**Its callers are gone** — the login prompt with `authenticate.account`, the
`ACC$USERS` grant list, and `logto.step.up`. **The password model's own login
and `LOGTO` rules moved to HISTORY.md**, 14 Aug 2026 seventh session, under §0
rule 5. `@logname` is still untouched by any of it: the only assignments
anywhere are `LOGIN` 235, `CPROC` 250 and 282 (both initialisation) and
`APISRVR`.

**Two decisions from the repository owner, both 13 Aug 2026, both settled.**

- **SDSYS reaches every account, without exception.** Administration that
  cannot enter an account cannot repair one. The test is **the account you are
  standing in** (`who`), not the one you logged in as, so stepping *out* of
  SDSYS loses the exception — SDSYS→KIM→JANE is refused at the second move;
  return to SDSYS first. `@logname` still names the person either way, so what
  accounts for the access is the audit record, not a refusal.
- **`LOGTO` takes an account name and nothing else.** It used to treat anything
  absent from ACCOUNTS as a pathname to `cd` to, reaching an account's directory
  without consulting its grant list. Closed by removing the capability rather
  than resolving paths back to accounts: an unregistered directory is not an
  account. An unknown name gives the same refusal as an ungranted one, so the
  register cannot be probed. `APISRVR`'s `SrvrAccount` took a name **or** a path
  the same way and now takes a name only; note nothing else there is gated,
  because the `LOGTO` grant check does not cover that path.

**Correction (13 Aug 2026): the API server does have a credential check.** It
is `APISRVR` line 921, `login(username, password)` — a real connect-time check
that simply **cannot succeed on Windows**, because it reads `/etc/shadow`,
which MSYS2 does not have (§6). So the API is currently closed rather than
open. What is genuinely missing is authorisation *after* connect, and an
authentication mechanism that can work at all (§7 step 6, §8).

**Correction (14 Aug 2026): SD creates and deletes OS accounts after all.**
Decision from the repository owner, reversing "Create no OS users and no OS
groups at all": the *linkage* between an SD account and an OS user is worth
keeping, and Windows offers it through the `*-LocalUser` and `*-LocalGroup`
cmdlets. **Read the two halves apart, because conflating them is the easy
mistake** — provisioning is back, but authorisation is still §5.6's, and
nothing consults a Windows group to decide who may log in. The owner asked for
the `sdusers` login gate back "if it is possible"; it is now possible, because
`IS_GRP_MEMBER` works, but **it has not been restored** and `LOGIN` is
untouched. That is a separate, deliberate act — §7 step 1b.

**What was built, 14 Aug 2026**, and has since been run against real Windows
accounts on the creating side (§4):

| Piece | Where |
|---|---|
| `!create_user` — `New-LocalUser`, created disabled | `GPL.BP/CREATE_USER` |
| `!delete_user` — `Remove-LocalUser`, profile left alone | `GPL.BP/DELETE_USER` |
| `!set_passwd` — prompts in SD, `Set-LocalUser`, enables | `GPL.BP/SET_PASSWD` |
| `!os_group(action, group, member)` — the four group operations | `GPL.BP/OS_GROUP` |
| `!ps_script` — runs a script carrying a secret | `GPL.BP/PS_SCRIPT` |
| `!is_grp_member` — asks Windows, not `/etc/group` | `GPL.BP/IS_GRP_MEMBER` |

**Two things decide whether any of it works.** **Elevation is not optional** —
creating a local user or changing a local group needs an elevated token, and an
ordinary SD session has a UAC-filtered one (`BUILTIN\Administrators` present as
*"Group used for deny only"*, measured 14 Aug 2026). Every helper therefore
tests for elevation explicitly and returns status 5 rather than guessing from a
localised error message, so **account creation works from the installer and
from an elevated terminal, and not from a normal session**. And **`OS.EXECUTE`
needed a shell an installed system does not have**, resolved by making
`SH`/`SH1` PowerShell — the one that would have bitten silently (§6).

**`sudo` on Windows: the binary is a convenience, but ELEVATION is now a
prerequisite.** Corrected 14 Aug 2026, fifth session, because the earlier
wording here caused a real wrong turn.

**What was said, and why it misled.** This paragraph read "it has no sudoers
file and no per-command policy". True of `sudo.exe`, and it was taken to mean
that **Windows cannot limit who may elevate**, which would have handed SDSYS to
every user and is the reason §5.6's password model was built instead.
**Elevation is limited, and tightly** — the control is not a file, it is the
`Administrators` group:

| | Linux | Windows |
|---|---|---|
| who may become root | listed in sudoers | member of `Administrators` |
| a normal account tries it | not in sudoers, refused | **prompted for an administrator's credentials** it does not have |
| an administrator tries it | in sudoers, password | consent prompt, elevated |

Measured on this machine (§4 Verified): `EnableLUA=1` with
`ConsentPromptBehaviorUser=3` means a standard user attempting elevation is
asked for **somebody else's** administrator credentials on the secure desktop.
They cannot elevate as themselves. **`CREATE.ACCOUNT USER x` leaves x out of
`Administrators` and `... ADMINISTRATOR` puts x in, so SD has been maintaining
the sudoers list all along.**

**`sudo.exe` itself is still not a prerequisite**, and the installer does not
install or enable it — checked 14 Aug 2026, `sd.iss` does not mention it. It is
Windows 11 24H2 and later only, so requiring it would exclude Windows 10 and
Server, and **"Run as administrator" on a terminal produces the identical
elevated token on every Windows version**. `sudo sd` is the convenient
spelling, not the mechanism. It was enabled on this machine on 14 Aug 2026 **in
inline mode** (`Enabled=3`), which matters: the default when enabled is "in a
new window", which would break an interactive `sudo sd` because the session
needs the same console.

**The one real risk, and it fails CLOSED.** `LocalAccountTokenFilterPolicy` is
not set on this machine, so the default UAC remote restriction applies and a
local account logging on **over the network gets a filtered token**. Since
§5.6.2 makes SD accounts ssh-only, an SD administrator arriving over ssh may be
unable to elevate at all, and so unable to reach SDSYS remotely. **Nobody gets
extra access — the failure is that an administrator gets less** — so it does not
block §7 step 0, but it must be measured before anyone relies on remote
administration. It may also simply be the design: §5.6.2 already says the
console and RDP belong to administrators and ssh is for everyone else.

**Passwords never go on a command line.** Decision from the repository owner,
14 Aug 2026, consistent with §8: `net user <name> <password> /add` exposes the
password to any local user through Task Manager, `Get-CimInstance
Win32_Process` or ETW. `!ps_script` writes the script to a file inside the
SDSYS directory instead, runs it and deletes it. The file is protected by
§5.7's ACL inheritance rather than by a permission call of its own, which is
the first practical use of that finding.

**What is still missing or dead.**

- **The audit records.** Nothing is written yet for a login, a `LOGTO` or a
  failed step-up, which is the remaining half of this model (§7 step 4). Until
  it lands the grant check controls access but leaves no trace of who used it —
  and attribution, not access control, is what this model is for.
- **There is no verb for managing grants.** `ACC$USERS` has a dictionary entry
  so `LIST ACCOUNTS` shows it and `MODIFY ACCOUNTS` can edit it, but nothing
  offers `GRANT`/`REVOKE` (§7 step 5).
- **`$CRED` must stay a separate file from ACCOUNTS**, which eleven programs
  open before any authentication. Reasoning in HISTORY.
- `ACC$GROUP` is dead but still populated on old records and still shown by
  `LIST ACCOUNTS`. Remove it with the OS account commands, as one change.
- The `is_grp_member` calls in `CREATEA` (line 323) and `MODIFYA` (96, 99, 125)
  were left where the others were deleted: they guard `OS.EXECUTE` calls to
  `useradd`, `usermod` and `groupadd`, and removing only the guard would let
  those shell-outs run unconditionally. They go with the Linux account commands.
- `CPROC`'s `system(27) = 0` "entered as root?" branch at line 272 was left
  alone. It guards `EUID_SET`, which has no Windows equivalent (§5.5), and its
  `kernel(K$ADMINISTRATOR, 1)` is now redundant.

**How the administrator flag is held.** `LOGIN` sets `USR_ADMIN` on entry to
SDSYS and clears it entering anything else; `CPROC` does the same on every
`LOGTO`. Only an `$internal` program may set the flag and only SDSYS may
compile one. Privilege tests ask the flag, not the uid: `kernel(K$ADMINISTRATOR,
-1)` in an `$internal` program, `SYSTEM(1050)` anywhere else (§6). `kernel.c`
seeds the flag from `IsAdmin()` at process start, which is what makes a Windows
administrator an SD one.

**The model in one paragraph.** A person logs in as **themselves**, then moves.
Access to other accounts is **granted, not shared**, so there is no second
password to know and none to rotate; `@logname` does not change on `LOGTO`, so
everything downstream attributes to whoever authenticated; and every login and
`LOGTO` is logged. `LOGTO SDSYS` re-prompts — the one exception to "granted,
not prompted" — and **asks for the caller's own password, not an SDSYS one**,
which is easy to get backwards and is the whole point: an SDSYS password would
be a second shared secret held by every administrator, which is the OpenQM
weakness this exists to remove.

**What the audit half has to do, when it is built** (§7 step 4). Attribution is
SD-internal and does not depend on §5.7's service model, so it lands with the
password work; it records who authenticated, not who is at the keyboard.

- **Not the existing `errlog`.** `log_message()` in `k_error.c` **discards the
  oldest half** of `<sysdir>/errlog` at the configured `ERRLOG` size — correct
  for diagnostics, disqualifying for an audit trail. Its own file, append-only,
  rotating rather than truncating.
- **Record grants on the target account** — JANE lists who may enter JANE —
  rather than as destinations on the source. It answers the question
  administration actually asks, and revocation happens in one place. `$LOGINS`
  chose the other direction and that register is gone (§6).
- **Watch `CPROC` reassigning `logname`** when it drops to `sdsys` (around line
  278). Nothing may overwrite the login identity.

**Understand the security consequence before relying on any of this.** A
password gate inside SD is not a file security boundary — see §5.7.
### 5.6.2 SD accounts are ssh-only; the console belongs to administrators (decided 14 Aug 2026)

**VERIFIED 14 Aug 2026 AT BOTH ENDS, EXCEPT RDP** — the mechanism (§4,
"THE SSH-ONLY MODEL WORKS", re-runnable with `gplbld/verify-sshonly.ps1`) and
the verb that drives it (§4, "`CREATE.ACCOUNT`'S SSH-ONLY BRANCH WORKS", on an
account SD created with a password SD set). The risk named below — that denying
the wrong right locks everybody out — was the thing tested, and it did not
happen. RDP is the only part of this section nobody has watched. Everything
else here is reasoning that stands on its own; read it before changing any of
it.

**Decision from the repository owner, 14 Aug 2026.** Accounts SD creates reach
the machine **over ssh and nothing else**. Local terminal access — the physical
console, and Remote Desktop — is for administrators, who have ordinary Windows
accounts. **The API is piped through ssh as well**, which settles the open
question in §8 about how it should be exposed.

This sits on top of §5.6.1: an administrator is a Windows administrator.
Answered by the owner the same day, `CREATE.ACCOUNT USER <name> ADMINISTRATOR`
**keeps creating the Windows account and leaves it unrestricted** — an
administrator gets a normal Windows account with console access. Only accounts
without the keyword are confined to ssh. So the keyword now decides two things
at once, which is worth stating plainly:

| | `CREATE.ACCOUNT USER x` | `CREATE.ACCOUNT USER x ADMINISTRATOR` |
|---|---|---|
| Windows group | standard user | `Administrators` |
| Administers SD | no | yes |
| Local console / RDP | **denied** | allowed |
| ssh | yes | yes |

**The two rights, and why not a third.** Windows expresses this as user rights
assignment: `SeDenyInteractiveLogonRight` blocks the console, and
`SeDenyRemoteInteractiveLogonRight` blocks Remote Desktop. **Do not deny
network logon.** Win32-OpenSSH authenticates with a network logon — cleartext
network logon for passwords, S4U for public keys — so denying it would lock out
the very access this is meant to preserve. That is the trap in this design and
it is the one thing to get right.

**Apply the rights to a GROUP, once, not to each account.** SD adds every
non-administrator account it creates to `sdsshonly`, and the installer applies
the deny rights to that group a single time. Granting them per account was
rejected because there is **no PowerShell cmdlet for account rights**
(measured: `Get-Command *AccountRight*` returns nothing), so each grant means
`LsaAddAccountRights` through P/Invoke or a `secedit` export-edit-import —
and `secedit` is a **read-modify-write of the entire USER_RIGHTS area**, so
running it per account rewrites machine policy repeatedly and races anything
else editing it. A group is also **inspectable**: "who is confined to ssh?" is
one membership list rather than a walk through `secpol.msc`.

**It cannot be `sdusers`.** That group grants access to the data *files* and
administrators are in it too, so denying console logon there would lock
administrators out of their own console. The two groups answer different
questions and must stay separate — the same distinction §5.6.1 draws between
`sdusers` and `Administrators`.

**`AllowGroups` in `sshd_config` is the second layer**, suggested by the
repository owner: the deny rights stop local logon, `AllowGroups` decides who
may ssh at all. Two cautions made it an installer offer rather than something a
verb does silently — it writes to a file SD does not own and which may be
managed by policy (§5.9 already forbids reconfiguring an ssh server SD did not
install), and the list **must include administrators** or the machine's own
administrator loses ssh.

**Written, applied and verified by control and treatment on 14 Aug 2026** (§4).
The lockout did not happen. How the two cautions are answered, since changing
any of it re-opens them:

- **Not a verb, and not even an unconditional installer step.** It is a
  **child** of the OpenSSH task in `sd.iss`. Inno only enables a child task
  when its parent is ticked, and the parent is hidden entirely on a machine
  that already has an ssh server — so "we did not install it, we do not
  configure it" is structural rather than a check somebody has to remember.
  The same `Check` is repeated on the child, because a subtask does not
  inherit its parent's.
- **The administrators group is resolved from `S-1-5-32-544`**, not written as
  a name — the literal `Administrators` is wrong on a localised Windows, and
  `sshd`'s `AllowGroups` has no SID syntax, so it has to be looked up and
  written out. `CREATEA` does the same thing at its Administrators add.
- **Four patterns for two groups**, bare and `COMPUTER\`-qualified.
  Win32-OpenSSH matches groups as `domain\group` with the computer name
  standing in for the domain, and reports of the bare form working vary by
  version. `AllowGroups` is a union, so a pattern that matches nothing costs
  nothing — and the failure being avoided is a lockout.
- **Before the first `Match` block**, because everything after a `Match` line
  belongs to it and the shipped `sshd_config` ends with
  `Match Group administrators`. Appending would apply `AllowGroups` to
  administrators only, which reads as working.
- **Removed on uninstall**, since it is the one thing SD writes outside its own
  tree, and the original is kept as `sshd_config.before-sd`.

**What ssh-only does not mean.** The deny rights control *where* an account may
log in, not *what it may run*. An ssh session lands in whatever `DefaultShell`
names, `cmd.exe` by default. Confining a user to SD rather than to a shell is a
separate control and is not part of this decision.

### 5.7 Where the OS still has to be involved: protecting the data tree

Dropping OS groups from SD's logic (§5.6) does not remove the need for OS file
permissions, and the two do not compose the way one would hope.

**The tension.** Every SD process opens the database directly — `dh_open()` →
`dio_open()` → `open()` — in its own process, under the invoking user's token.
`connection_type` describes only the terminal transport; there is no data
server. So any ACL strong enough to stop a user reading the files in Explorer
also stops SD reading them on that user's behalf. **While SD runs as the
invoking user, account passwords organise access; they do not secure it.**

**This is what decides whether accounts are private from each other.** To enter
account B a user's token must have read and write on B's directory, because
their own process does the I/O, and the OS cannot distinguish "entered with the
right password" from "opened in Explorer". So stage 1 offers only two options,
neither wanted: grant every SD user access to every account directory, which
gives no protection between accounts at all; or set per-user ACLs per account,
which duplicates the password gate in the OS, reintroduces what §5.6 removed
and adds a Windows-user-to-account mapping to maintain.

- **What is achievable in stage 1.** Lock the tree to `sdusers` plus
  `Administrators`, so no other account on the machine can browse it. That
  blocks everyone who is not an SD user; it does not stop one SD user reading
  another's account files directly.
- **The real answer, and it is stage 2.** `sdwind` becomes a Windows service
  running as a dedicated service account — a virtual account, `NT SERVICE\SD`,
  needs no password management — which owns the tree exclusively. Session
  processes are spawned under the *service* identity and the user reaches their
  session over the named pipe, so the user's own token never touches the data.
  The question then dissolves: accounts become private *because* of the
  password rather than in spite of it, and shared accounts still work because
  the OS never sees individual people at the file layer. This is the direct
  Windows equivalent of the Linux original dropping to the `sdsys` user via
  `EUID_SET` (§5.5), not a Windows novelty. The substantial part is making
  console `sd.exe` a client of the service instead of doing its own file I/O.

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

**Three requirements from the repository owner (13 Aug 2026), all now met**:
SD's home is under `C:\Program Files`; the login starts from any directory
(`sd -ASUE` from `C:\Windows` works, because `sd.exe` finds its DLLs beside
itself rather than on PATH); and on login the current directory is the
account's, which `LOGIN` does with `ospath(acc.path, OS$CD)`. **Do not break
the third** — it is what makes an account feel like a place rather than a
setting.

`ProgramData` is the correct home for machine-wide mutable state and has no
space in its name. `Program Files` does, which is why the `VALID_OS_PATH` and
`OSPATH()` validators both had to learn to accept one (§6).

**Ship the MSYS2 DLLs beside `sd.exe`.** Windows searches the executable's own
directory before PATH, which removes both PATH traps in §6: the
exit-53-with-no-message when `libsodium-26.dll` is missing, and — much worse —
Git for Windows's rival `msys-2.0.dll` being picked up, which makes SD report
"SD has not been started" while it is running. Relying on PATH order is not a
supportable install. Moving off `/usr/local/sdsys` matters on its own merits
too: it resolves inside the MSYS2 install tree, so reinstalling MSYS2 would
destroy the database.

**The configuration file is settled, 14 Aug 2026.** Server and client both read
`SD_CONFIG` and both fall back to `%ProgramData%\SD\sd.conf`, with
`C:\ProgramData\SD\sd.conf` as the last resort. `SCARLET_CONFIG` is gone, and
so is the `sd.ini`-in-`C:\Windows` fallback. The two values live in
`SD_CONFIG_ENV` and `SD_CONFIG_DEFAULT` in `gplsrc/sddefs.h` and are
**duplicated in `sdclilib.c`**, because the client is a separate toolchain that
must not include the server's headers (§5.2) — **change both together.**
`sdnet.h` still hardcodes `PASSWD_FILE_NAME "/etc/shadow"` (§7 step 6).

**`sdrealpath()` was the blocker on all of this, and it is fixed** (13 Aug
2026). It treated anything not starting with `/` as relative and never treated
`\` as a separator, so `C:\ProgramData\SD` became
`/usr/local/sdsys/C:\ProgramData\SD` and every open failed with ER_FNF naming
nothing near the cause. It now folds backslashes and treats a leading drive
letter as the root; all five spellings open the same file (§4). `DS` is still
`/` — this changed what SD **accepts**, not what it produces.

**Stored and displayed paths still come out half POSIX**, and both work:
`CREATEA` joins `CONFIG('USRDIR')` with `@ds`, so an ACCOUNTS record reads
`C:\ProgramData\SD\user_accounts/PAT`, and `@PATH` comes from `getcwd()`, so it
reports `/c/ProgramData/SD/user_accounts/PAT`. Both are tidied by the `@ds` /
`dir.separator` question (§6), which is **testable for the first time** now
that a `\` separator no longer breaks path resolution.

### 5.9 One installer: a staging script, then Inno Setup (decided 13 Aug 2026)

**Revised twice on 13 Aug 2026; this is the current decision.** The
`installsdai.sh` port is **dropped**. Two scripts replace it: one that builds a
**staging directory** holding exactly what an install consists of, and one that
turns that directory into an **Inno Setup installer**. Neither the shell
installer nor `deletesdai.sh` gets ported — though `deletesdai.sh` is still
worth reading before touching the uninstaller, since it is where the Linux
answer to "what happens to the database" is written down. Reasoning for all
three positions is in the HISTORY entry "Installer: the shell script port is
dropped".

**Why the Linux script existed, and why that reason does not transfer**, so
nobody proposes porting it again. `installsdai.sh` was load-bearing:
ScarletDME targeted Fedora, Debian, Arch and OpenSUSE across several versions
each, so **the end user had to compile**, and the script abstracted apt from
dnf from pacman from zypper and drove a build on the user's own machine.
Windows has one target and one ABI, and SD ships its own runtime beside
`sd.exe` (§5.8), so the user needs no compiler at all. What is left once the
distro handling is stripped out is a developer setup tool that §2 and §3
already cover — which makes the Windows install genuinely *simpler* than the
Linux original, unlike much else in this port.

**The staging script is the valuable half**, and not mainly for packaging:

- **It makes §5.8 executable.** The layout is prose here; a script is that
  layout in a form that either runs or does not.
- **It is a whitelist, and whitelists find accidental dependencies.** `gplsrc`
  sat in the data tree for as long as it did because `installsdai.sh` copied it
  wholesale and nobody asked why — a fault that cost most of a session on
  13 Aug 2026.
- **It is where the DLL closure is computed, not guessed**, by walking the
  imports — missing one gives exit code 53 and no message at all (§6).

**Inno Setup then packages the staged directory**, staging *pre-compiled*
artefacts rather than building on the target. That collides with §5.11 only in
appearance: the staged artefacts are release artefacts built elsewhere, not
tracked files, and the `.iss` script does belong in this repository. The
compiler is on this machine at
`C:\Program Files (x86)\Inno Setup 6\ISCC.exe`; it is a separate toolchain and
is not part of `make`. Still to decide: whether CI produces the installer.

What the installer is responsible for: lay down both roots; **set the ACLs on
the data tree with `icacls`, breaking inheritance first** (§5.7), which is the
step that makes the data private and which nothing at runtime substitutes for;
create `sdusers` and `sdsshonly`; run — or ship the result of — the bootstrap
in §3; and register the service once §5.7's model exists. What the uninstaller
does is §5.9.1.

**Optional OpenSSH Server, opt in and off by default (decided 14 Aug 2026).**
Decision from the repository owner. The case for offering it: SD will often be
installed by someone with little administrative knowledge who wants the ten
people on their local network to reach it. Good security is the default; the
easy path exists but has to be chosen. Note the Linux script installed and
enabled ssh **unconditionally** — that behaviour is not inherited but
re-decided, which §5.16's rule 2 permits.

Requirements, and each of these has already cost something:

- **Unchecked by default**, and clearly worded: it starts a service listening
  on port 22 and adds a firewall rule, granting remote shell access to the
  whole machine, not just to SD.
- **If OpenSSH Server is already present, say so and do not offer the option.**
  Detect it **without elevation** — `%SystemRoot%\System32\OpenSSH\sshd.exe` on
  disk, or an `sshd` service registered; `Get-WindowsCapability -Online`
  requires elevation (measured 14 Aug 2026). Never silently reconfigure or
  restart an ssh server the machine already has: it may be managed by policy.
  This is also what makes the `AllowGroups` subtask structurally unreachable on
  such a machine (§5.6.2).
- **A failure to install it must not fail the SD install.** It is a Features on
  Demand capability, blockable by policy, a metered connection or an offline
  machine. Report it and carry on.
- **And it is SLOW, which is worse than a failure.** Measured 14 Aug 2026:
  `Add-WindowsCapability` hands off to `TiWorker`, which worked for minutes and
  left **`RebootPending` True**. The `[Run]` entry is `runhidden` with no
  progress, so the wizard says nothing and it reads as a hang — it was reported
  as one during testing. **Say it will take minutes** next to the checkbox;
  **never kill it**, because interrupting `TiWorker` mid-servicing is how the
  component store gets corrupted; and say that the reboot is real, since SD
  itself needs none.
- **The uninstaller must not remove it**, for the same reason it must not
  remove the database: it may predate SD or be in use by something else.

**Be honest about the ten-users-over-ssh case.** Each of those people needs a
Windows account on the machine, which is exactly what the OS account
provisioning restored on 14 Aug 2026 makes manageable (§5.6). But **it does not
give them isolation from each other's data**, and will not until §5.7's service
model lands: every SD process opens the database under the invoking user's own
token, so all ten need file access to the tree and can read each other's
account directories outside SD. Anyone deploying this way should be told that
plainly.

### 5.9.1 What the uninstaller does (decided 14 Aug 2026)

Decision from the repository owner, settling the question §5.9 raised.

**Yes, it is the standard Windows uninstall** — Inno registers under the
`Uninstall` key, so SD appears in Settings > Apps and `unins000.exe` is what
that runs. Nothing has to be built for it.

**The default must not touch accounts, the database or the configuration.**
Most of this comes free: Inno removes only the files it installed, from its own
log, and removes a directory only if it is empty, so everything the bootstrap
and the running system create — `VOC`, `ACCOUNTS`, `$CRED`, the accounts,
`errlog` — is invisible to it. Two things are not free:

- **`sd.conf` is installed**, so Inno would remove it like any other file. It
  is marked `uninsneveruninstall`, and `onlyifdoesntexist` as well so an
  upgrade does not overwrite settings the user has edited.
- **Pre-bootstrapping widens the boundary.** The staged tree ships a populated
  `gcat` and `GPL.BP.OUT`, so those *are* installed files and Inno removes
  them. That is correct — they are program, not data — but the line between
  "shipped" and "user's" now runs through the middle of
  `C:\ProgramData\SD\sdsys`, so anything added to the ship list has to be
  looked at with the uninstaller in mind.

**Removing the data is a separate, opt-in choice**, asked from `[Code]` and
defaulting to keeping it. Two conditions: the prompt must say exactly what it
destroys and where, and a **silent uninstall must never delete it** — an
unattended removal that takes the database with it is the worst possible
default. (`/SUPPRESSMSGBOXES` does not do what you would expect here — §6.)

**This is a hobby project with no release schedule and no architecture document
to satisfy.** Worth having when weighing "do it properly" against "do it now":
the answer is usually to do the thing that keeps development moving and record
honestly what it does not yet do. The two handoff files and the changelog are
the only process there is.

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

**Installing means building** — but only for whoever runs the staging script,
which is the point of it (§5.9). The end user gets the Inno Setup installer and
needs neither a clone nor a toolchain.

**History was rewritten on 13 Aug 2026 to purge every binary**, past and
present, verified by walking every object for NUL bytes. **Every commit hash
changed**; the mapping is in the HISTORY entry "History rewritten to purge
every binary". The install recompiles I-types, so dictionary items carry source
and checksum only — if a `FILES_DICTS` item ever regains a compiled tail, strip
it.

### 5.12 Lower case everywhere it can be (decided 13 Aug 2026)

Goal from the repository owner on 13 Aug 2026. **Everything that can be lower
case should be lower case.** SD is inconsistent about it today — BASIC source
is free-form and usually written in lower case, while file names, field names
and account names are forced up. The end state is lower case throughout, with
existing upper-case code converted rather than tolerated.

Not started, and it is a wide change rather than a deep one. Three things force
case up today: **account names**, which `KEYS.H` declares "forced to
uppercase" and which `LOGIN`, `CPROC` and the credential helpers all
`upcase()` on the way in — the `$CRED` register is keyed the same way, which is
why account names are case insensitive at login; **the terminal itself**, since
`LOGIN` sets `pterm(PT$INVERT, @true)` so typed input is case-inverted (the
visible half of the §6 trap that silently upcased a password); and dictionary
and VOC item ids throughout `NEWVOC` and `FILES_DICTS`.

**Sequencing matters.** Case insensitivity of *comparison* is what makes the
current upcasing harmless, so removing the upcasing first would make `sue` and
`SUE` different accounts. `CASE_INSENSITIVE_FILE_SYSTEM` (§7 step 8) is the
file-name half of the same problem, already written but never defined, so the
two belong together.

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

Recorded here because it changes how several things on the §7 list should be
built, and that is cheaper to know before writing them than after. **The rule
that follows: new administrative capability goes in a subroutine with a verb
over it**, not in a verb that holds the logic, so a form added later calls the
same subroutine instead of reimplementing it or shelling out to the verb.
`GPL.BP/CRED_SET` and `CRED_VERIFY` with `SET_ACC_PASSWORD` over them are the
pattern to copy, and `SET.PASSWORD` is already prompt-driven, which is the
right precedent.

The two clearest cases are **the grants verb** (§7 step 5), edited through
`MODIFY ACCOUNTS` today, and **the batch allowlist** (§8), where `ED VOC
ALLOWED` is workable and a form is better — particularly as it is the one place
that has to enforce the no-arguments and VOC-type rules recorded there.

### 5.15 Embedded Python is dropped; the API is the point (decided 13 Aug 2026)

Decision from the repository owner on 13 Aug 2026, and it is a **statement
about what SD for Windows is for**, not just a packaging choice: the intended
user is a Windows developer using SD as a **back end data store, reached
through the API**. Embedded Python was not part of that, so it is gone rather
than shipped unused.

Removed outright rather than left behind an `#ifdef`, the same reasoning as the
Linux code in §1. The C sources, the Makefile flags, 20 `GPL.BP/PY_*` programs,
`SYSCOM/SDPYFUNC.H`, the `SD_Py*` error codes and the SDEXT keys all went; the
itemised list is in the HISTORY entry "Embedded Python removed".

**Two consequences worth carrying forward.** It took **two** build dependencies
with it, not one — `python-devel`, and `gettext-devel`, which existed only to
satisfy the `-lintl` that `python3-config --ldflags --embed` emits (§2); plain
`python` is still needed by `gplbld/`, for the developer only. And it
**reorders §7**: if the API is the primary interface, then step 6 and
exercising `SDConnectLocal()` matter more than their positions suggest. Not
reordered yet — flagged, because it is the repository owner's call.

### 5.16 Convert every remaining Linux-ism, and the installer outranks Linux parity (decided 14 Aug 2026)

Two standing instructions from the repository owner, given together on
14 Aug 2026. They are ordering rules for everything below, not a task.

**1. Every Linux-ism that remains is to be converted to its Windows
equivalent where one exists.** Not wrapped, not guarded by a flag, not left
because it is harmless — converted, in the spirit of §1's "replace Linux code
outright". `/bin/bash` was one and it turned out to be load-bearing (§6): it
looked like an inert default and it silently broke every installed system.
Treat the rest the same way, and assume each one is hiding a consequence until
shown otherwise.

**2. Where Linux parity and the Inno installer conflict, the installer wins.**
The instruction was "mimic the Linux version if possible, but the Inno
installer is more important than Linux version compatibility." So when a Linux
behaviour cannot be reproduced on Windows without making the install worse,
drop the behaviour rather than complicating the install. This settles the
pre-bootstrap question below in the installer's favour.

**Known Linux-isms still in the tree**, as a working list rather than a
complete audit:

| What | Where | Windows equivalent |
|---|---|---|
| `sudo chmod g+s` on a new account directory | `GPL.BP/CREATEA` | inheritable ACEs, set once by the installer (§5.7) |
| `PASSWD_FILE_NAME "/etc/shadow"` | `gplsrc/sdnet.h` | `$CRED`, or peer identity (§7 step 6) |
| `PLATFORM_NAME "Linux"`, so `SYSTEM(1010)` says Linux and `BCOMP` emits the `SD.LINUX` token | `gplsrc/sddefs.h` | a Windows name; nothing tests the token yet, so it is latent |
| `SYSTEM(91)` hardcoded 0, `is_nt` never assigned | `op_sys.c`, `kernel.h` | §5.4, and restore the BASIC branches first |
| `setuid`/`setgid` in `login_user()` | `gplsrc/linuxio.c` | nothing; SD accounts are not OS users (§5.6) |
| `EUID_SET`/`EUID_RESTORE` | `sdext_eguid.c`, `CPROC` line 272 | the service model (§5.7); no direct equivalent |
| `usr/lib/systemd/`, `etc/xinetd.d/` | tree | a Windows service; kept deliberately as documentation of the topology |
| `installsdai.sh`, `deletesdai.sh` | root | not ported, by decision (§5.9) |
| `@ds` hardcoded `/` | `CPROC` | live for stage 2 only; `/` is correct on the MSYS2 runtime (§6) |

**What "Inno compatible" required, in dependency order — all seven are now
decided, and all but the service registration are done:**

1. **No dependency on a shell Windows does not ship.** Done 14 Aug 2026 (§6).
   This was the one that would have shipped broken.
2. **The layout move** (§5.8) — `C:\Program Files\SD\usr\bin\` and
   `C:\ProgramData\SD\`. Done; `gplbld/stage.py` builds exactly that.
3. **One configuration file, found without an environment variable.** Done
   14 Aug 2026, verified with nothing set (§4, §5.8).
4. **Pre-bootstrap the staged tree.** Done 14 Aug 2026 —
   `gplbld/stage.py --bootstrap` runs the bootstrap on the build machine at
   the production path and ships the filled `gcat` and `GPL.BP.OUT`, so
   **installing is a file copy and the end user needs neither Python nor a
   compiler.** Rule 2 above is what decided it: the alternative was staging
   `gplbld/` and requiring Python on every target, which contradicts "the data
   tree holds data only". The cost is that the data tree's location becomes
   fixed, and only `ACCOUNTS/SDSYS` embeds it.

   **Before this the staged tree was not installable at all** — `gplbld/` was
   absent from `SDSYS_SHIP`, so `bbcmp.py`, `pcode_bld.py` and the
   `FILES_DICTS` that `WRITE_INSTALL_DICTS` reads as
   `@sdsys:"/gplbld/FILES_DICTS"` were all missing. Precisely the class of
   thing §5.9 predicted the whitelist would expose.
5. **`icacls` on `C:\ProgramData\SD\`**, breaking inheritance first (§5.7).
6. **Set the SDSYS password last**, after the bootstrap, since `LOGIN` admits
   an administrator to an account with no verifier yet.
7. **Decide what the uninstaller does with the data tree.** Settled, §5.9.1.

**Elevation is a point in the installer's favour, not against it.** Inno runs
elevated, which is exactly what the OS account commands need (§5.6) — so
creating the initial accounts is something the installer can do and a normal
session cannot.

## 6. Traps

Each of these cost real time. Read before debugging anything similar.

- **`ACCOUNTS/SDSYS` CARRIES `ACC$GROUP = sdsys`, AND NO SUCH WINDOWS GROUP
  EXISTS.** Found 14 Aug 2026, sixth session, by reading the record off disk
  rather than trusting §5.6's summary of it:
  `C:\ProgramData\SD\sdsys\ACCOUNTS\SDSYS` is three fields — the path, empty,
  and `sdsys`. The installer creates `sdusers`; `CREATE.ACCOUNT` creates
  `sdu_<name>`; **nothing anywhere creates `sdsys`.**

  So **restoring the `ACC$GROUP` test verbatim, as §7 step 0b said to, refuses
  SDSYS to everybody** — an elevated administrator included, because
  `!is_grp_member` returns false with status 1 for a group that does not exist.
  On Linux this worked by accident of a mechanism Windows does not have: `sudo
  sd` ran `!EUID_SET('sdsys')` in `CPROC` *before* `LOGIN`, so `@logname` became
  `sdsys` and `IS_GRP_MEMBER` line 83's "is this your own group account?"
  shortcut matched. Windows has no effective-user drop, `@logname` stays `don`,
  and the shortcut cannot fire.

  **The fix, in `LOGIN` and in `logto.authorised` both: an elevated session
  skips the group test.** That is Linux behaviour anyway — root is not in the
  group either. The general form is the one this file keeps re-learning:
  **a rule transcribed from the Linux source can depend on a Linux mechanism
  that was never ported.**

- **`OpenProcess(PROCESS_TERMINATE)` RETURNING A HANDLE DOES NOT MEAN YOU CAN
  TERMINATE.** 15 Aug 2026: it returned one for a High-integrity `sdwind` from a
  Medium-integrity session, and `Stop-Process` on that same pid seconds later
  was refused `Access is denied`. The file used that probe once as evidence of
  terminate rights (§4). **Trust the operation, not the probe** — the cheap
  check has at least one false positive in it.

- **`sd -start` HANGS ANY CALLER THAT WAITS FOR ITS OUTPUT STREAMS TO CLOSE.**
  15 Aug 2026, twice, in two different shells: `sd -start > f 2>&1` from bash
  left the *shell* running for ever, and PowerShell
  `Start-Process -Wait -RedirectStandardOutput` timed out at two minutes — both
  times **SD had done its job**, the daemon was up and the output file held
  `SD (64 Bit) has been started`. `sdwind` inherits the handles and outlives
  `sd`, so waiting on the streams means waiting on the daemon. Wait on the
  **process**, as `bootstrap.py` does, or run it in a real console. A hang here
  is not a failed start — look at the daemon before believing it.

- **THE BOOTSTRAP COMPILED INTO THE DEVELOPMENT TREE, AND THE STAGED CATALOGUE
  CAME OUT HOLDING 13 Aug PROGRAMS.** 15 Aug 2026. `sdsys/ACCOUNTS/SDSYS` ships
  with field 1 = `/usr/local/sdsys`, and field 1 is the **account directory**:
  after login `GPL.BP` and `GPL.BP.OUT` resolve through it, while `gcat` comes
  from the config file. So `SECOND.COMPILE` compiled 190 programs into
  `/usr/local/sdsys/GPL.BP.OUT` and catalogued them into the stage, whose own
  `GPL.BP.OUT` held **12** objects — exactly what `sd -i` and `bbcmp.py` write
  through sysdir paths.

  **The tracer was the sign-on banner.** The owner had changed
  `GPL.BP/LOGIN:175` in the repository; the staged `gcat/$LOGIN` printed the
  old text, matched the dev tree's byte for byte but for 3, and carried no
  `sdusers` literal — a pre-step-0 LOGIN in a tree about to be installed. On a
  clean machine that path does not exist at all, so **step 2 would have tested
  a tree built from nothing.**

  Fixed by pointing the record at the staged tree **before** the bootstrap
  (`stage.py`) and refusing a mismatch (`bootstrap.py:check_account_record`).
  **`check_no_stage_paths` had been passing vacuously** for the same reason:
  the path embedded was the dev tree's, which it does not look for.

  **Confirmed by re-staging the same hour:** staged `GPL.BP.OUT` 12 → **191**
  objects, tree 3,291 → **3,471** files, `gcat/$LOGIN` now carrying both the new
  banner and the `sdusers` gate, `check_no_stage_paths` still clean, and the dev
  tree receiving **0** files against 191 on the run before.

- **`K$ADMINISTRATOR` NOW MEANS ELEVATED, AND `BCOMP` GATES `$internal` ON IT —
  SO COMPILING SD's OWN PROGRAMS NEEDS AN ELEVATED WINDOW.** 14 Aug 2026, sixth
  session. `sd -INTERNAL` names SDSYS for itself in `sd.c`, so it goes through
  the elevation gate like anything else and `LOGIN` refuses it with
  `sysmsg(10002)`. `bootstrap.py:239` is one of four such steps.

  **The build scripts say so up front now instead of failing half way**,
  15 Aug 2026: `bootstrap.py:74` `is_elevated()`, refused at
  `bootstrap.py:151`, and the same test at `stage.py:338` for `--bootstrap`,
  which otherwise copies several thousand files before finding out. The test is
  `544 in os.getgroups()` — `IsElevated()`'s, imported by `stage.py` rather
  than restated.

  Do **not** fix it instead by letting `-INTERNAL` skip the gate — that restores
  exactly the bypass the 13 Aug session removed. And note the comment at
  `bootstrap.py:242` records the *previous* login change breaking this same
  path, unnoticed for the same reason: **nobody re-runs the bootstrap, so it
  rots silently.**

- **`sd -start` SAID "SD is already started" WHEN `sdwind` WAS DEAD, AND DID
  NOTHING — FIXED 14 Aug 2026, seventh session (§7 step 1d).** Kept because the
  *shape* recurs: the segment and the semaphores are objects, objects outlive
  the processes that made them, so anything that asks an object whether a
  system is running will eventually lie. On a binary that predates the fix, the
  way out is still `sd -stop` then `sd -start`.

  **Start the daemon from an UNELEVATED session where you can.** One started
  elevated cannot be stopped by an ordinary one — the entry below — so an
  unelevated start leaves it stoppable from either.

- **THREE HELPERS READ `/etc/passwd` AND `/etc/group`, WHICH MSYS2 DOES NOT
  HAVE. ONE WAS FIXED ON 14 Aug 2026 AND THE OTHER TWO WERE NOT.** The fixed
  one, `!is_grp_member`, had refused every login with "not registered for SD
  use" and its trap is below. **`!is_user` and `!is_group` had exactly the same
  defect and were found a session later**, in the seventh, while doing §7 step
  1c — nothing had connected them, because each failure looked like something
  else entirely.

  **They fail CLOSED and therefore SILENTLY**: the read fails, status is set to
  1, and the answer is "no such user" or "no such group" for names that plainly
  exist. Measured 14 Aug 2026: no `/etc/passwd` or `/etc/group` under either
  root the runtime can use — `C:\msys64\etc` on a development machine,
  `C:\Program Files\SD\etc` on an installed one, which holds only `fstab` —
  while `getent passwd` answered correctly from the same shell and
  `Get-LocalGroup` returned `sdu_sdacct5` with its SID. **The capability was
  never missing; only the file was.**

  **What each one cost, and neither symptom named the cause:**

  | | |
  |---|---|
  | `!is_group` | `DELACC` gates the removal of an account's `sdu_` group on it, so **`DELETE.ACCOUNT` silently left the group behind on every account it removed** |
  | `!is_user` | `CREATEA` asks it whether the OS account exists. False for everyone sent it to `create_user()`, which fails on an existing account — so the verb refused a pre-existing user, which **is** the rule (§5.6), but reported it as `Create User Failed, OS Error: 1` |

  **THE SECOND ONE IS THE INSTRUCTIVE ONE: right behaviour resting on a broken
  lookup.** Repairing `!is_user` alone would have brought `CREATEA`'s adopt
  branches to life and turned a refusal into a **silent adoption of somebody's
  existing Windows login**. That nearly happened in the seventh session and was
  caught by the repository owner. **When a fix makes a helper answer correctly,
  check what its callers were relying on it getting wrong** — the two were
  changed in the same commit, with the rule written into `CREATEA` explicitly.

  **There are no more.** `grep -rn 'openpath "/etc"' GPL.BP` returned nothing
  after the two fixes, seventh session — that was the whole family.

- **A BLANK `Path` FROM `Get-Process` DOES NOT MEAN "ELEVATED", AND IT LOOKS
  EXACTLY LIKE IT DOES.** 14 Aug 2026, seventh session. Four `sdwind` daemons
  were started that day; the two started from an elevated window had an
  unreadable `Path` and the two started unelevated did not, so the field was
  taken as an elevation test and written into this file as a measurement. **It
  is not one.** A fifth daemon had a blank `Path` *and* granted
  `OpenProcess(PROCESS_TERMINATE)` to an ordinary session — which an elevated
  process cannot do, and which the orphaned one had refused with
  `Access is denied` an hour earlier.

  **Ask for the right you care about, rather than reading a field that
  correlates with it.** "Can this session stop that process" is
  `OpenProcess(PROCESS_TERMINATE)`, and it answers in one call:

  ```powershell
  Add-Type -Namespace W -Name K -MemberDefinition '[DllImport("kernel32.dll", SetLastError=true)] public static extern IntPtr OpenProcess(uint a, bool i, uint p);'
  [W.K]::OpenProcess(1, $false, <pid>)   # IntPtr.Zero means refused
  ```

  The type does not survive between PowerShell tool calls; re-add it each time.
  **This is the third instrument in this file to be wrong** after
  `Measure-Object -Line` and the UAC registry reading, and the general form is
  §0 rule 2's: **an instrument you have not checked is not evidence.** A
  correlation over four samples is not a check.

- **SD PRINTS MSYS2 PROCESS IDS, AND WINDOWS HAS NEVER HEARD OF THEM.**
  Measured 14 Aug 2026, seventh session: the running daemon called itself
  **pid 87**; `Get-Process sdwind` called it **14712**. `getpid()` under the
  MSYS2 runtime answers with the runtime's own numbering, and **every pid SD
  holds is that kind** — the user table, `sysseg->sdwind_pid`, `sysdump`'s
  `sdwind pid:` line.

  **This is worse than cosmetic in any message that says "stop this process".**
  `Stop-Process -Id 87` does not fail; it acts on whatever unrelated Windows
  process holds 87. **Translate before printing:**
  `cygwin_internal(CW_CYGWIN_PID_TO_WINPID, pid)` from `<sys/cygwin.h>`, which
  `win_pid()` in `sysseg.c` wraps. It answered correctly on the live daemon —
  14712, matching `Get-Process` exactly — and returns 0 when it cannot
  translate, so a caller can fall back to printing no number rather than a
  wrong one. **`sysdump.c` line 95 still prints the untranslated pid.**

- **A PIPED SD SESSION CANNOT ANSWER "Press RETURN to continue", SO ANY
  `LIST` THAT OUTGROWS A PAGE HANGS FOREVER.** Measured 14 Aug 2026, sixth
  session: `verify-createaccount.ps1` stopped dead at `LIST ACCOUNTS` **on the
  fifth account**, leaving an `sd.exe` blocked on stdin and no error message of
  any kind. Three earlier runs had passed because four accounts fitted on one
  page. **The bug was always there; the register just grew.**

  **Append `NO.PAGE` to every `LIST` in a scripted session** — `bootstrap.py`
  line 205 already does it for `RUN GPL.BP WRITE_INSTALL_DICTS`. Fixed in
  `verify-createaccount.ps1` in the same session.

  **The general form is the useful part: a test that passes today because the
  data is small is not a passing test.** This one degraded silently from green
  to hung with no code change at all.

  **And you may not be able to clean up after it.** The stuck `sd.exe` was
  started by an *elevated* session, so an unelevated `Stop-Process` answers
  *Access is denied* — the same asymmetry this section records for `sd -stop`.
  Kill it from the window that started it.

- **ANYTHING `LOGIN` CALLS BECOMES A BOOTSTRAP DEPENDENCY, BECAUSE
  `SECOND.COMPILE` LOGS IN.** Measured 14 Aug 2026, sixth session. Restoring the
  `sdusers` gate made `LOGIN` call `!IS_GRP_MEMBER`, which calls
  `!VALID_OS_NAME` — and the bootstrap died at
  `000000D7: Unable to load '!VALID_OS_NAME' object code in !IS_GRP_MEMBER`
  **before compiling anything**, leaving the staged tree not installable.

  The fix is one line in `GPL.BP/BBPROC`'s pass 1 list (line ~222):
  `src.list<-1> = 'VALID_OS_NAME'`. **The rule to carry forward: if you add a
  call to `LOGIN` or `CPROC`, add its target — and its target's targets — to
  that list.** Check the whole chain; `VALID_OS_NAME` calls nothing, which is
  the only reason this one stopped at one line.

  **And the same change made the bootstrap need `sdusers` to exist**, which only
  the *installer* creates — circular, and it would have refused the bootstrap on
  any clean build machine. Resolved by the owner's decision of 14 Aug 2026 to
  **exempt internal mode from the `sdusers` gate**, which opens no hole because
  `-INTERNAL` already requires elevation. See §5.6.

- **OPEN QUESTION, NOT A TRAP: `WARNING: GRANT.POS is assigned a value but never
  used` when `CPROC` is compiled inside the staged tree.** 14 Aug 2026, sixth
  session. **`grant.pos` does not exist in the source.** Established properly:
  the staged `CPROC` is md5-identical to the repository's
  (`4c46731048f6ffe38f1e626ea7522016`), and a case-insensitive search of the
  whole `sdsys` tree finds `grant` only inside comments. The variable was real
  once — it belonged to the 13 Aug `ACC$USERS` grant list — and its deletion is
  what makes the warning strange.

  **It does not appear when the same `CPROC` is compiled on the installed
  tree**, which points at the staged tree rather than the source. Benign: it is
  the "assigned but never used" class, not the `is not assigned a value` class
  `bootstrap.py` line 229 treats as fatal, and the compile reports `0 error(s)`.
  **The test that would settle it** is compiling `CPROC` alone against a freshly
  staged tree: if the warning survives, it is in the source and the search above
  is wrong; if not, it leaks across programs within one `SECOND.COMPILE`.

- **`IS_INSTALL` IS STILL DEFINED ON EVERY INSTALLED SYSTEM, SO EVERY
  `$ifndef IS_INSTALL` BLOCK IN `CPROC` IS COMPILED OUT THERE.** Found 14 Aug
  2026, sixth session, from a single compile warning —
  `PRIVILEGED_COMMANDS is assigned a value but never used`.

  `CPROC`'s own header, lines 27-31, says: *"The install script overwrites this
  file with IS_INSTALL commented out, and CPROC will be recompiled."*
  **It never did.** `GPL.BP/define_install.h` reads `$define IS_INSTALL` in the
  repository *and* at `C:\ProgramData\SD\sdsys\GPL.BP\define_install.h`.

  What that switches off is the privileged-command handling at `CPROC` 1466 and
  1479: the `locate` against `privileged_commands`, and the
  `!EUID_RESTORE`/`!EUID_SET` pair that raises privilege around `$CREATEA` and
  drops it again. So that mechanism is **dead twice over** — by preprocessor
  here, and by platform anyway, since `!EUID_SET` is the Linux effective-user
  drop Windows has no equivalent of (§5.5). Removing it is therefore safer than
  it looks, but **do not read a `$ifndef IS_INSTALL` block and assume it runs**:
  on a developer's bootstrapped tree it may, on an installed system it does not.

  **The general form, and it is the third time this file has recorded it:** a
  comment describing what the install *will* do is not evidence that it does.

- **`gplbld/bbcmp.py` CANNOT COMPILE `LOGIN`, so it is not a syntax checker for
  the BASIC layer.** It aborts with "VOID statement not coded". 14 Aug 2026,
  sixth session — and **checked with a control before being believed**: HEAD's
  unmodified `LOGIN` was put through the same compiler and failed identically,
  at pass2 line 204 against the modified file's 210. The Python compiler builds
  the bootstrap seed only; SD's own `BCOMP` compiles the rest through
  `SECOND.COMPILE`. **Which means a change to `LOGIN` or `CPROC` cannot be
  checked at all without a working installed system** — worth knowing before
  planning a session around editing them.

- **Scripting SD from PowerShell: the input must be a PIPE, and the pipe puts
  a BOM on the first line.** Both measured 14 Aug 2026 against the installed
  tree. They compound, because the first line of a scripted session is usually
  the one that matters.

  **`Start-Process -RedirectStandardInput` does not work.** SD prints its
  banner, shows one prompt and answers `Process terminated`, then exits — the
  same behaviour this section already records for a `<` redirect, and for the
  same reason: SD wants a pipe, not a file handle.

  **The pipe prepends U+FEFF to the first line**, so

  ```powershell
  @('COUNT VOC','WHO','OFF') | & sd.exe -ASDSYS
  ```

  answers `COUNT is not in your VOC` for a perfectly good `COUNT VOC`, while
  `WHO` on the second line runs fine. Setting `$OutputEncoding` to
  `ASCIIEncoding` does **not** fix it — checked, its preamble is empty and the
  BOM still arrives, so it is not coming from there.

  **Send a blank sacrificial first line.** The BOM lands on a line that was
  empty anyway, SD says `is not in your VOC` about nothing, and the real
  commands follow untouched:

  ```powershell
  @('', 'COUNT VOC', 'WHO', 'OFF') | & sd.exe -ASDSYS   # 431 record(s) counted
  ```

  Strip the terminal escapes from the output (`` -replace "`e\[[0-9]*[A-Za-z]", '' ``)
  or every line arrives wrapped in `[K` and cursor moves.

- **In PowerShell 5.1, `native.exe 2>&1` turns every stderr LINE into a
  terminating error when `$ErrorActionPreference = 'Stop'`.** Found 14 Aug
  2026. PowerShell wraps native stderr in `ErrorRecord`s
  (`NativeCommandError`), and under `Stop` an `ErrorRecord` throws.

  **It fails on success, which is what makes it expensive.** `ssh` prints
  `Warning: Permanently added 'localhost' to the list of known hosts` to
  **stderr after logging in successfully**. `verify-sshonly.ps1` reported
  `FAILED` with a stack trace for a login that had worked.

  Do not redirect native stderr inline. Use `Start-Process` with
  `-RedirectStandardOutput` and `-RedirectStandardError` to separate files and
  read `.ExitCode`; `Invoke-Native` in `verify-sshonly.ps1` is the pattern.
  Feed stdin from an empty file at the same time, so anything that decides to
  prompt gets EOF and fails instead of hanging for ever.

- **`sshd -d` started from an elevated administrator prompt cannot
  authenticate ANY account.** sshd must run as **SYSTEM** to build a user
  token, and it says so — `get_user_token - unable to generate user token for
  <name> as i am not running as system`. It fails at `mm_answer_pwnamallow`,
  *before* authentication is attempted, so the DEBUG3 log looks exactly like a
  total authentication failure that has nothing to do with what is being
  tested. Elevation is not enough and there is no flag for it.

  **Read the installed service's reasons instead** — it runs as SYSTEM and logs
  to the `OpenSSH/Operational` event log:

  ```powershell
  Get-WinEvent -LogName 'OpenSSH/Operational' -MaxEvents 40 |
      Sort-Object TimeCreated |
      ForEach-Object { "{0:HH:mm:ss}  {1}" -f $_.TimeCreated, $_.Message }
  ```

  At the default level that already distinguishes `Failed password for <name>`
  from `Accepted password for <name>` from "user not allowed", which was
  enough to tell an authentication failure from a rights refusal.

- **Do not make a person retype a random password into a test.** Found 14 Aug
  2026. A 36-character password containing `l`, `I`, `1`, `O` and `0` was
  typed by hand three times and logged three `Failed password` entries,
  pointing at a design problem that did not exist — `LogonUser` had accepted
  the same string on the same account minutes earlier.

  `ssh` takes no password on the command line, but it does honour
  **`SSH_ASKPASS` with `SSH_ASKPASS_REQUIRE=force`** (measured here on
  OpenSSH_for_Windows_9.5), so a helper program can supply it and the test can
  be automated. Pass the secret to the helper in an **environment variable**
  rather than writing it into the helper file, and clear it in a `finally`.
  Where a password must still be readable by a human, generate it from an
  alphabet with no ambiguous glyphs and no shell metacharacters.

- **In an Inno `[Run]` parameter, `{{` escapes a literal `{` but `}` MUST BE
  WRITTEN SINGLY — and `}}` gives you two.** Found 14 Aug 2026. The OpenSSH
  step read `try {{ ... }} catch {{ exit 1 }}`, which expanded to
  `try { ... }} catch { exit 1 }}`: correct opening braces, doubled closing
  ones. PowerShell answered "The Try statement is missing its Catch or Finally
  block" — before running anything.

  **It failed in complete silence and had done so on every install**, because
  the entry has `skipifdoesntexist` and checks no exit code — deliberately,
  since §5.9 says a failed ssh install must not fail the SD install. Ticking
  the box produced no `sshd.exe`, no service and no message anywhere.

  **Check the install log, not the `.iss`.** Inno logs `Parameters:` after
  expansion, which is the only place the doubled brace is visible. And the
  quickest test of any generated PowerShell is to parse it without running it:

  ```powershell
  [System.Management.Automation.Language.Parser]::ParseInput($s, [ref]$null, [ref]$err)
  ```

  This is a different fault from the brace-comment trap below; they share only
  the character.

- **A brace comment in an Inno `[Code]` section cannot mention a
  brace-delimited constant.** `{ ... {app} ... }` ends at the FIRST closing
  brace, and everything after it is parsed as code — the error points at the
  prose, several lines from anything that looks like a statement. Use the
  `(* ... *)` form, and do not write `(*` or `*)` inside that either, which
  ends it the same way. Cost two compile failures on 14 Aug 2026.

  **Hit again the same day**, in a new `[Code]` procedure whose comment
  explained that it must run before `{app}` is deleted. The trap does not need
  you to be careless about braces; it needs you to write prose about the
  installer, which is what a comment in an installer is for. If a `[Code]`
  comment mentions a path, use `(* ... *)` without thinking about it.

- **An installer edit to a file SD does not own must be an exact inverse.**
  `allow-ssh-groups.ps1` fenced its `AllowGroups` block between two comment
  markers and then wrote a blank line after the closing one, for readability.
  The blank line is outside the fence, so removal left it — and every
  apply/remove cycle grew `sshd_config` by one line, for ever, in a file that
  belongs to somebody else. Found 14 Aug 2026 by `verify-allowgroups.ps1`,
  which asks whether add-then-remove reproduces the original **byte for byte**
  rather than whether it looks right.

  The general form: anything that edits a foreign configuration file needs a
  test that applies it repeatedly and removes it, and compares against the
  original text. "It removed the line" is not the check; "the file is the file
  it was" is.

- **A test for a config edit does not need the real config.**
  `C:\Windows\System32\OpenSSH\sshd_config_default` is the template `sshd`
  copies to `C:\ProgramData\ssh\sshd_config` on its first start, and unlike the
  copy it is **world readable**. So the whole of `AllowGroups`' file handling
  is testable unelevated, on any machine, with no `sshd` — which is what
  `verify-allowgroups.ps1` does. Worth remembering as a shape: the risky half
  of "edit a system file" is usually the editing, and the editing usually has a
  readable stand-in for its input.

- **FIXED 14 Aug 2026, kept because the shape recurs: the `<sysdir>/bin` split
  left two C call sites pointing at the old location, and both failed
  silently.** `sysseg.c` execed `"%s/bin/sdlnxd"` from `sysseg->sysdir`, and
  the daemon's `check_lost_users()` built `'<sysdir>/bin/sd' -cleanup` the same
  way. Both were right while the Linux install kept executables and the pcode
  library in one directory; §5.8 split them and neither call site moved.
  **So the daemon never started on an installed system**, and nothing said so —
  the `execl` sits in a forked child that has already `daemon()`ed, so there was
  no message and `sd -start` still reported success. `sdwind_pid` stayed at -1,
  which is exactly the value meaning "failed to start", so `sd -stop` skipped it
  and even that looked normal.

  **The symptom is an absence**, the hard kind to notice: SD works completely
  because none of it needs the daemon. Only looking for the process shows it.
  And it **worked perfectly in development**, where `<sysdir>/bin` does hold the
  executables — the same family as the `/bin/bash` trap above.

  **Two general lessons.** When anything moves between the development and
  installed trees, **grep the C for the old location** — the compiler cannot
  help, because these are runtime strings. And **a forked child that fails must
  `_exit()`, not `return`**: returning put it back into the caller's code as a
  duplicate process, which is what made this produce no symptom at all. Both
  call sites now resolve against `exe_directory()` (`exepath.c`).

- **`Test-Path` says True for a directory you cannot read, so it is no test of
  an ACL.** `Test-Path C:\ProgramData\SD` answers True from a session that is
  refused on every path inside it, because listing the *parent* is what that
  question actually asks. On 14 Aug 2026 this briefly read as "the installer's
  `icacls` step did not apply" — it had applied perfectly. **Check the contents:**
  `Get-ChildItem` on the tree, or `icacls` on it, both of which fail honestly
  with "Access is denied". The same caution applies to any scripted check of
  §5.7's work.

- **The ACL lockout's symptom is "Error 13 allocating semaphores", which names
  nothing useful.** After the installer sets the ACLs, a session whose token
  does not carry `sdusers` cannot reach `C:\ProgramData\SD` — and since
  `etcstab` maps `/dev/shm` there, the first thing to fail is semaphore
  allocation. Errno 13 is EACCES. Observed 14 Aug 2026 immediately after
  installing: the installing user is added to `sdusers`, but **Windows fixes
  group membership in the access token at logon**, so until they sign out and
  back in they match none of the three ACEs on their own database. The
  installer says so in a dialog at the end for exactly this reason. Anyone who
  dismisses it gets an error about semaphores and no path forward. Worth
  reporting EACCES on `/dev/shm` distinctly in `sdsem.c` at some point.

- **`/SUPPRESSMSGBOXES` does not suppress `MsgBox` calls from `[Code]`.**
  Measured 14 Aug 2026: a `/VERYSILENT /SUPPRESSMSGBOXES` install still stopped
  and waited for someone to click OK. An unattended deployment would hang
  indefinitely. The test that works is `WizardSilent` in the install path and
  `UninstallSilent` in the uninstall path — two different flags for the same
  job. `gplbld/sd.iss` now checks both.

- **The UCRT64 compiler needs its own `bin` on PATH even when it is invoked by
  absolute path, and it fails with no message whatsoever.** `gcc.exe` finds its
  DLLs beside itself, but the subprograms it spawns — `cc1.exe`, down in
  `ucrt64/lib/gcc/...` — do not, and resolve their UCRT64 DLLs through PATH.
  Without it, `gcc --version` works fine and **compiling `int main(void){return
  0;}` exits 1 with completely empty stdout and stderr.** That reads as "the
  compiler is broken", not as a search-path problem, and it does not look like
  anything in the source. The Makefile now prepends `$(dir $(UCRT_CC))` to PATH
  for the `sdclilib` target, so it no longer depends on the developer's shell.
  Found 14 Aug 2026.

- **`make sd` lists `sdclilib` as a prerequisite, so when the client fails to
  build, `sd.exe` is never relinked — and you go on testing the old one.**
  `sd: $(SDOBJS) sdclilib sdtic ...`. Make builds prerequisites first, the
  client failed, make stopped, and `bin/sd.exe` kept an earlier timestamp and
  earlier contents. Every test then measured a binary that did not contain the
  change under test, which sent a good hour into diagnosing SD behaviour that
  had already been fixed in source. **After any build failure, check the
  timestamp on `bin/sd.exe` before believing a test result.** `make exit=0` and
  a `Linking sd` line are the things to look for.

- **`sd -stop` used to kill its own caller, and everything else in the process
  group.** `stop_sd()` in `sysseg.c` looped over the user table doing
  `kill(uptr->pid, SIGTERM)` guarded only by `uptr->uid`. **`kill(0, SIGTERM)`
  does not mean "no process" — it means every process in the caller's process
  group**, so a table entry that had been claimed but not yet filled in, or
  left by a process that died between the two, made `sd -stop` terminate
  whatever launched it. Found on 14 Aug 2026 while building the installer: a
  build script called `sd -stop`, and the Python process driving it and the
  shell above that both vanished, with no error anywhere and an exit status of
  zero. It reads as "the script silently stopped half way". Fixed — the test is
  `uptr->pid > 0`, which the liveness poll twenty lines below always had. A
  negative pid is the same hazard, since `kill(-n)` also signals a group.
  **The general lesson: never pass an unvalidated pid to `kill()`.**

- **An over-long `SH` or `SH1` in `sd.conf` silently corrupted the parameters
  declared after them.** `config.c` copied both with a plain `strcpy` into
  `char[MAX_SH_CMD_LEN+1]`, which was 80, and `sortmem` and `sortmrg` are the
  next two fields in `struct config`. The PowerShell `SH1` value is 93
  characters, so it overran, and SD refused to start with **"Invalid value for
  SORTMRG configuration parameter" — naming a parameter the file does not
  contain.** Fixed twice over: `MAX_SH_CMD_LEN` is 255, and both copies are
  length-checked and refuse the value with an honest message. The other
  `strcpy` calls in that parser have the same shape and have not been audited;
  `SORTWORK`, `SPOOLER`, `STARTUP` and the rest are all unbounded.

- **`config.c` stripped `\n` but not `\r`, so a CRLF `sd.conf` corrupted every
  string parameter.** Only `'\n'` was removed, which is right for a Unix file
  and wrong for every configuration file written on Windows — `gplbld/stage.py`
  writes CRLF, as Notepad does. The carriage return stayed on the end of the
  value, so `SDSYS` became `C:\ProgramData\SD\sdsys\r` and every path built
  from it was wrong. Numeric parameters were unaffected, because `sscanf` stops
  at the `\r`, which is what made it look like a path problem rather than a
  parsing one. **This appeared only in the shipped configuration, never in the
  developer's own**, since the hand-written `/etc/sd.conf` is LF. Fixed.

- **`ACCOUNTS` is a directory-type file, so its records are text files whose
  field marks are NEWLINES, not `\xfe`.** Splitting a record on the `\xfe`
  field mark used inside a DH file finds nothing, yields the whole record as
  field 1, and rewriting field 1 then flattens the record to a single line —
  silently discarding the account name and the `ACC$USERS` grant list. Done
  once on 14 Aug 2026 while retargeting the SDSYS account path, and caught only
  by looking at the bytes. Check the file type before assuming a delimiter.

- **RESOLVED 14 Aug 2026, kept because the diagnosis generalises.**
  `OS.EXECUTE` ran `/bin/bash -c`, and an installed system has no bash. It was
  true of *every* `OS.EXECUTE` in the system, not just the account commands
  that exposed it: `gplbld/stage.py` ships the executables, the client DLL and
  the MSYS2 DLL closure and **no shell at all**, and on an installed tree the
  POSIX root is `C:\Program Files\SD\` (the two-component rule below), so
  `/bin/bash` resolved to a file that does not exist. **It would have failed on
  the installed system while working perfectly in development**, where MSYS2's
  own bash is present.

  **The fix was to point `SH` and `SH1` at PowerShell**, on the repository
  owner's instruction — chosen over shipping `bash.exe` or naming some other
  Windows shell, because the five new OS-facing programs are PowerShell scripts
  already and it removes a quoting layer rather than adding one. `op_sh.c`
  derives the path from `%SystemRoot%` rather than writing `C:\Windows`, and
  `sd.conf` and `stage.py` carry the same values so they stay visible and
  overridable. **The path must contain no spaces:** `clparse()` splits on them
  and does not honour quotes.

  Two consequences: every `OS.EXECUTE` string in those programs lost its bash
  quoting layer, so the command now *is* the PowerShell script; and
  `!ps_script` names its temporary file **relative to the working directory**
  instead of `cat`-ing it into stdin, which removes the need for a Windows
  pathname that BASIC cannot produce. PowerShell ships with Windows, so **SD no
  longer depends on a shell it would have to install** — which is what made
  this an installer problem rather than a tidiness one.

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
- **`whoami /groups` LISTS `Administrators` IN A SESSION THAT CANNOT USE IT,
  and the qualifier is easy to miss.** An unelevated administrator's token
  carries `BUILTIN\Administrators` marked **"Group used for deny only"** — it is
  present so it can be *denied* against, not granted. Read the line and not just
  the group name, or an unelevated session looks fully privileged.

  **This cost two sessions of design.** It is the same fact as
  `getgroups()` versus `getgrouplist()` (§5.6.1), and on 14 Aug 2026 it was
  measured correctly and then read as "elevation cannot be distinguished, so
  Windows cannot limit who becomes an administrator" — which is what sent the
  port down the account-password route in §5.6. **A control being in an
  unfamiliar place is not the control being absent.** The general form: before
  concluding a platform lacks a capability, find where that platform puts it.

- **Adding yourself to a Windows group does not take effect in the session you
  add it from.** Group membership is fixed in the access token at logon, so
  `sdadmins` resolves by name immediately (`getgrnam` finds gid 197613) while
  `getgroups` still does not list it. Elevation does not help — the elevated
  token comes from the same logon. **Sign out and back in, or reboot.** This
  bears directly on the requirement that the installing user become an
  administrator automatically: they cannot use it until they log in again.
- **To see what an ordinary user sees, build a probe with a gid nobody holds.**
  Otherwise impossible on a machine whose account is a Windows administrator,
  and everything a normal user meets at login is behind it. `SD_ADMIN_GID` is
  `#ifndef`-guarded for exactly this. **Both `sd.c` and `linuxlb.c` must be
  rebuilt** — overriding only `sd.c` does nothing, because `IsAdmin()` lives in
  `linuxlb.c`. Build the object list from `gpl.src`, not `gplobj/*.o`: the
  latter includes the standalone utilities and gives multiple `main`s.

  **Recipe corrected 14 Aug 2026** — it named `SD_ADMIN_GROUP`, which is gone
  (§5.6.1), and still carried the `python3-config` flags that went with
  embedded Python in §5.15, so it had not compiled since 13 Aug. Re-run and
  verified in this form:

  ```sh
  cd sdb_ai/sd64
  mkdir -p /tmp/na
  CF="-std=gnu17 -w -D_FILE_OFFSET_BITS=64 -Igplsrc -I/usr/local/include \
      -DGPL -g -DSD_ADMIN_GID=99999"
  gcc $CF -c gplsrc/sd.c      -o /tmp/na/sd.o
  gcc $CF -c gplsrc/linuxlb.c -o /tmp/na/linuxlb.o
  gcc $(sed 's|^|gplobj/|;s|$|.o|' gpl.src | grep -v '/\(sd\|linuxlb\)\.o') \
      /tmp/na/sd.o /tmp/na/linuxlb.o \
      -lm -lcrypt -ldl -lbsd -L/usr/local/lib -lsodium \
      -o /tmp/na/sd_nonadmin.exe
  ```

  `sd_nonadmin.exe -start` then answers "Command requires administrator
  privileges". Inverted — a gid the account *does* hold — it is also how to
  test an admin-gated path.
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

  So `/dev/shm`, `/etc/sd.conf`, `/tmp` and the API's socket path all move with
  it. The first symptom is a warning that `/dev/shm` does not exist, followed by
  every POSIX shared memory call failing — the entire IPC layer (§5.1). **Put
  the binaries in `C:\Program Files\SD\usr\bin\`**, so the root lands on
  `C:\Program Files\SD\`. One level up and the root is `C:\Program Files\`
  itself, which would mean creating `C:\Program Files\dev`.

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
- **FIXED 14 Aug 2026, kept for the diagnosis.** `/etc/group` does not exist
  under MSYS2 — it and Cygwin dropped `/etc/passwd` and `/etc/group` for direct
  SAM/AD lookups — but `IS_GRP_MEMBER` read it as a text file, so it set status
  1 and returned false for everyone, failing the `sdusers` test at `LOGIN` 193
  and terminating every connection with "This user is not registered for SD
  use". Note this is *not* the `getgrnam()` path verified in §4: that goes
  through the NSS layer and works correctly; reading the file directly does not.
  **The fix was to repair the routine, not to delete its callers** —
  `IS_GRP_MEMBER` now asks `Get-LocalGroupMember` and distinguishes member /
  not-a-member / no-such-group (§4). The earlier instruction here to delete the
  calls was written under the superseded assumption that SD would stop touching
  OS groups entirely; see the correction in §5.6.
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
  `GetNamedPipeClientProcessId`, on a pipe whose security descriptor you
  control. `connection_type` already has `CN_PIPE`.
- **`chmod` is a no-op on the MSYS2 runtime — the mount is `noacl`.** `chmod
  0770` leaves a directory `drwxr-xr-x` and changes no ACE; the real permissions
  stay whatever was inherited, which under `C:\ProgramData` includes
  `BUILTIN\Users:(OI)(CI)(RX)`. Nothing in SD can secure a directory by mode
  bits. Use `icacls` from the installer, `/inheritance:r` first (§5.7).
  Inheritance itself is unaffected by `noacl` and does work — see §5.7.
- **The two configuration paths are duplicated in two toolchains.** Settled
  14 Aug 2026 — both server and client read `SD_CONFIG` and fall back to
  `%ProgramData%\SD\sd.conf` — but the values live in `sddefs.h` **and** in
  `sdclilib.c`, which cannot include the server's headers (§5.2). Change one
  without the other and the client silently looks somewhere else.
- **`sd -start` looks like it hangs, but it has succeeded.** It spawns
  `sdwind`, which inherits stdout and stderr. Any shell that captures output —
  a pipe, command substitution, a tool that reads the process's output — then
  blocks until the *daemon* exits, not until `sd -start` exits. The parent has
  already returned. Check with `Get-Process sdwind` rather than waiting. **This
  became live again on 14 Aug 2026**: while the daemon was never starting,
  there was nothing to block on and a piped `sd -start` returned immediately.

  **Correction, 14 Aug 2026 — "redirect to a file when starting from a script"
  WAS THE ADVICE HERE AND IT IS NOT ENOUGH.** `Start-Process -Wait` with
  `-RedirectStandardOutput`/`-RedirectStandardError` does not return until the
  redirected **handles** are released, and `sdwind` holds them, so the
  destination being a file rather than a pipe changes nothing. The wait is on
  the handle.

  **The only remedy that works is not waiting on the process.** Start it and
  poll for the daemon:

  ```powershell
  $null = Start-Process -FilePath $sdExe -ArgumentList '-start' -NoNewWindow
  for ($i = 0; $i -lt 30; $i++) {
      if (Get-Process sdwind -ErrorAction SilentlyContinue) { break }
      Start-Sleep -Milliseconds 500
  }
  ```

  `verify-createaccount.ps1` has this as `Start-SD`. **The symptom is a script
  that prints "SD is not running, starting it" and then sits there for ever
  while SD is in fact perfectly up** — `Get-Process sd` shows nothing,
  `Get-Process sdwind` shows the daemon, and nothing has been created. It is
  safe to interrupt.

  **And interrupting it leaves the daemon holding the script's own scratch
  files.** `sdwind` inherited the redirected handles, so
  `%TEMP%\sd-createaccount-probe\native.err` and `native.out` cannot be deleted
  or rewritten while it lives. The next run then fails at its own setup with
  "The process cannot access the file 'native.err' because it is being used by
  another process", which points at the wrong thing entirely. Observed
  14 Aug 2026. Kill the daemon, then re-run.

- **A POWERSHELL PIPELINE PUTS A PHANTOM EMPTY LINE AFTER EVERY COMMAND, AND
  AN `input` STATEMENT EATS IT.** PowerShell writes **CRLF** between pipeline
  objects and SD treats CR and LF **each** as a line terminator, so
  `@('A','B') | sd.exe` arrives as `A`, empty, `B`, empty.

  At the TCL prompt this is invisible — an empty command just reprints `:` —
  which is why it went unnoticed for as long as scripts only sent commands.
  **At an `input` statement it is fatal**, and it silently destroyed
  `verify-createaccount.ps1` on 14 Aug 2026:

  | `SET_PASSWD` | reads | gets |
  |---|---|---|
  | `input pw1 HIDDEN` | the phantom after the `CREATE.ACCOUNT` line | **empty** |
  | `input pw2 HIDDEN` | the real password | the password |
  | `input yn` | the next phantom | **empty**, so not `Y`, so no retry |

  `pw1 # pw2`, so the password was never set; the account stayed **disabled**,
  because `SET_PASSWD` runs `Enable-LocalUser` inside the same script; and all
  three logon measurements then failed for want of a password. The whole
  visible trace was a stray `Command not found` on **stderr** — the second
  password falling through to the TCL prompt.

  **The fix is to send one string with LF separators**, not an array:

  ```powershell
  $body = "`n" + (($commands + @('OFF')) -join "`n") + "`n"
  $out = $body | & $sdExe -ASDSYS
  ```

  Measured, not deduced, by piping two commands both ways and counting prompts.
  The leading newline also serves as the BOM sink the trap above needs.
  **Do not try to read the echo back to check** — SD's `[K` erase-line
  sequences make every line appear twice and can truncate one copy; this
  transcript rendered `CREATE.ACCOUNT USER sdacct1` as `CREATE.ACCOUSER
  sdacct1` on a line that executed correctly.

- **THE INSTALLED DATA TREE IS NEVER UPGRADED, SO "TEST IT ON THE INSTALLED
  SYSTEM" QUIETLY MEANS "TEST AN OLD BUILD".** `sd.iss` skips the entire
  `sdsys` set when `C:\ProgramData\SD\sdsys` already exists, and the tree is
  `uninsneveruninstall` — both deliberate, so that an upgrade cannot overwrite
  a live database (§5.9). The consequence nobody had joined up: on
  14 Aug 2026 this machine ran an 08:32 data tree and an 08:32 `sd.exe` for the
  rest of the day while the repository moved on, and **every test run against
  "the installed system" after that was testing 08:32's code.** It cost a full
  investigation of a `CREATE.ACCOUNT` failure that had been fixed at 09:50.

  **Before trusting any result from `C:\Program Files\SD`, date it.** The
  binary's `LastWriteTime` against `git log` is usually enough; the data tree is
  harder, because BASIC ships compiled — the quick tell is whether a message the
  new code prints exists at all:

  ```powershell
  Get-Item 'C:\Program Files\SD\usr\bin\sd.exe' | Select-Object LastWriteTime
  Test-Path 'C:\ProgramData\SD\sdsys\MESSAGES\10034'
  ```

  A `find <tree> -newer <stage>/MANIFEST.txt` over `sdsys/GPL.BP` and
  `sdsys/MESSAGES` names the delta exactly. **Refreshing means uninstall, delete
  `C:\ProgramData\SD`, reinstall** — the procedure at the top of this file.
  There is no upgrade path (§7 step 3), and it will cost more once a tree holds
  real data.

- **`sd -stop` LEAVES `sdwind` RUNNING WHEN THE STOPPING SESSION IS LESS
  ELEVATED THAN THE STARTING ONE. IT NOW SAYS SO; IT STILL CANNOT STOP IT.**
  Observed 14 Aug 2026, fourth session; the *silence* was fixed in the seventh
  (§7 step 1d), the underlying refusal cannot be — an unelevated process is not
  allowed to signal an elevated one, and `Stop-Process` from the same session
  is refused `Access is denied` at the same boundary.

  **REPRODUCED ON THE INSTALLED BINARY FROM A REAL CONSOLE, 14 Aug 2026,
  seventh session:** elevated `sd -start`, then `sd -stop` typed in an ordinary
  `cmd` window. `SD (64 Bit) has been shut down`, **`C:\ProgramData\SD\shm`
  emptied**, `sdwind` still running as pid 13840. The segment goes and the
  daemon stays, which is also why **the fix cannot help a second time on that
  daemon** — no segment, no `sdwind_pid` to read (the trap below).

  **What to do:** kill it by **Windows** pid from an elevated window,
  `Stop-Process -Id <pid> -Force`. The warning now prints that pid, translated
  (see the MSYS2-pid trap above). A second `sd -stop` will not help, because
  the segment it read `sdwind_pid` from has already gone.

  **What to watch for:** an orphaned `sdwind` holds a mapping of an unlinked
  segment and keeps running `check_lost_users()` against it. Starting SD again
  creates a *fresh* segment, so the machine ends up with two daemons and one of
  them is working on memory nothing else can see. Check `Get-Process sdwind`
  after any `sd -stop` that spanned an elevation boundary.

- **`sd -stop` STILL SAYS "has been shut down" WITH THE DAEMON RUNNING, IF THE
  SEGMENT HAS ALREADY GONE — AND THIS ONE IS NOT FIXABLE WHERE THE OTHERS WERE.**
  Measured 14 Aug 2026, seventh session, by unlinking the segment under a live
  daemon: `sd -stop` printed success, exit 0, and `Get-Process sdwind` still
  showed 14712. **`sysseg->sdwind_pid` is the only record of the daemon's
  identity, so with the segment gone `stop_sd()` has nothing to signal and no
  way to know there was anything to signal.** The residue of §7 step 1d, and the
  answer if it ever matters is a **pid file beside the segment** rather than a
  field inside it.
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
  the symptom go away. **That diagnosis was wrong** (13 Aug 2026). `APISRVR`
  lines 64-66 are `$execute 'BASIC GPL.BP REVSTAMP'`, `$execute 'RUN GPL.BP
  REVSTAMP'` and `$include revstamp.h` — compile-time directives that *run*
  `REVSTAMP`, which opens `./gplsrc/revstamp.h` relative to the account
  directory. `CPROC` carries the identical two lines already commented out, so
  the intended fix was demonstrated one file away. **Both are now commented
  out** and `gplbld/gen_includes.py` does the translation at build time.

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
- **FIXED 14 Aug 2026 — `OSPATH(path, OS$PATHNAME)` rejected every native
  Windows path, and it is a *different* validator from `VALID_OS_PATH`.** This
  is the C twin of the entry below, and fixing the BASIC one did not touch it.
  `op_dio2.c` split the path on `/` alone and ran `valid_name()` over each
  component; `valid_name()` refuses everything in `df_restricted_chars`, which
  contains **both `:` and `\`**. So `C:\ProgramData\SD\user_accounts` arrived
  as a single component holding two forbidden characters, and no native path
  could pass.

  **The symptom was a half-made account.** `CREATE.ACCOUNT` stopped with
  "Invalid account pathname" (`CREATEA` line 257) *after* creating the Windows
  user and setting its password — so the OS account existed, nothing in SD did,
  and the message named a pathname problem in a verb whose visible work had
  apparently succeeded.

  Now: an optional drive letter is skipped, and the split accepts `/` or `\`,
  whichever comes first. **`df_restricted_chars` was deliberately NOT widened**
  — `op_dio3.c` and `op_dio4.c` use it to map record ids onto filenames, which
  is a different job, and changing it would change how records are named on
  disk without being reversible for existing files.

  **The general lesson:** there are two path validators with similar names and
  different implementations, one in BASIC and one in C. Fixing either says
  nothing about the other, and only the C one is on `CREATE.ACCOUNT`'s path.

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

In the order they should be taken. **Steps 4 to 13 keep the numbers they have
carried since 13 Aug 2026**, because the rest of this file refers to them by
number; steps 1 to 3 were renumbered on 14 Aug 2026 when the install layout,
the staging script and the Inno installer were all finished and removed.

0. **CLOSED — 14 Aug 2026, sixth session. THE LINUX ACCESS MODEL IS RESTORED,
   INSTALLED AND VERIFIED END TO END (§5.6, §4).** All five rules observed, both
   `LOGTO` paths, and `CREATE.ACCOUNT` still at 16 of 16. Kept here rather than
   deleted because the sub-steps record how it was done and what it cost; the
   next subject is step 1.

   **Read `git show f9edab0:sdb_ai/sd64/sdsys/GPL.BP/LOGIN` first**, lines
   185-270. That is this repository's own pre-port source and it is the
   specification — the five rules in §5.6 are transcribed from it, not designed.

   **What was built:** `IsElevated()` beside `IsAdmin()` in `linuxlb.c` (it is
   `getgroups()`, the call `IsAdmin()` was moved *off*, because a UAC-filtered
   token drops a deny-only `Administrators` — so the two calls answer two
   different questions and both are wanted); `kernel.c` seeding `USR_ADMIN`
   from it; `LOGIN` restored from `f9edab0` with `authenticate.account` deleted;
   `CPROC` losing `logto.step.up` and regaining the `ACC$GROUP` test. `$CRED`,
   `!CRED_SET`, `!CRED_VERIFY` and `SET.PASSWORD` are all kept and recorded as
   callerless. **One deliberate departure from `f9edab0`: an elevated session
   skips the `ACC$GROUP` test**, because `ACCOUNTS/SDSYS` names a Linux group
   and restoring the test verbatim refuses SDSYS to everybody (§6).

   **THE RECIPE THAT COST A ROUND TRIP, BECAUSE EVERY LATER STEP NEEDS IT.**
   Recompiling anything in `GPL.BP` on an installed system takes `-internal`,
   the command as separate arguments, an **elevated** window, and no pipe:

   ```powershell
   & 'C:\Program Files\SD\usr\bin\sd.exe' -internal BASIC GPL.BP LOGIN
   ```

   **Not `-ASDSYS`** — `BCOMP` gates `$internal` on `K$INTERNAL` *and*
   `K$ADMINISTRATOR`, so standing in SDSYS is not enough, and with `-ASDSYS`
   every directive is rejected as unrecognised and each `common` block fails
   after it: 11 cascading errors that look like broken source and are not.
   **And not piped** — the BOM trap in §6 turned `CATALOG` into `TALOG`.
   `CATALOG` is not needed separately: the `$catalog` directive writes `gcat`.
   **Back up `gcat` first**, because a bad `$LOGIN` locks you out of SD:

   ```powershell
   Copy-Item 'C:\ProgramData\SD\sdsys\gcat' 'C:\ProgramData\SD\sdsys\gcat.bak' -Recurse -Force
   ```

   **Success is stricter than `0 error(s)`**: require also that no
   `is not assigned a value` line appears, which is the ERRGEN trap and what
   `bootstrap.py` line 229 checks. `PRIVILEGED_COMMANDS is assigned a value but
   never used` is expected (§6, `IS_INSTALL`), and so is
   `Unable change ownership of directory ... err: 1000`.

1. **Finish the loose ends the account model left.** The model itself is proven
   (§4, §5.6.1, §5.6.2); none of this is large, and it should not be left to
   drift.

   a. **`CREATUSR` is dead config and is now UNBLOCKED.** `DELACC` was its last
      caller and stopped using it on 14 Aug 2026 (1c), so the three remaining
      pieces can go: `config.c` parses it, `op_config.c` answers it, `CONFIG`
      prints it. Nothing else reads it.

      **Correction, 14 Aug 2026:** this file previously said `CREATUSR` "is not
      in the shipped `sd.conf` and defaults off", and gave that as a blocker.
      **That was wrong** — `config.c` line 98 sets `pcfg.create_user = 1`, so
      it defaulted **on** and never blocked anything. The real blocker was the
      pathname validator in §6.
   b. **MOVED INTO STEP 0b, 14 Aug 2026.** Restoring the `sdusers` gate is no
      longer a question that needs settling against §5.6.1 — the reversal in
      §5.6 answers it. The gate goes back.
   c. **DONE 14 Aug 2026, seventh session — compiled, catalogued and run (§4).**
      Two branches still untested: the "SD created it" delete, and `ADOPT`.

      **Owner's decision: `DELETE.ACCOUNT` offers to delete the OS account only
      when SD created it.** The three answers are all different and all acted
      on: SD made it → prompt, defaulting to no; somebody else made it → say so
      and leave it; not there at all → say so, which is the half-removed case.
      `!is_sd_user` (new) answers by reading back the description
      `CREATE_USER` already stamps on every account it creates, so nothing new
      is recorded and existing accounts answer correctly with no migration.
      **It is a marker, not a proof** — an administrator can edit a
      description — so it is trusted to *withhold* deletion and never to compel
      it: the one-sided failure leaves litter instead of deleting a login.

      **Also in this step:** the `config('CREATUSR')` gate is gone (unblocking
      1a), and **the `ACCOUNTS` record is deleted last rather than first**, so
      a failure part way leaves the account registered and the verb re-runnable
      instead of leaving orphans nothing can address.

      **The three half-removed accounts are the test case**, and they now have
      an answer: `sdacct1`–`sdacct3` have no Windows account, so the verb
      reports that and removes the SD side. Measured: `is_sd_user` answers
      `sdacct5` → SD's, `don` → **not SD's**, `sdacct1` → absent.
   d. **DONE AND FULLY OBSERVED — 14 Aug 2026, seventh session. One related
      defect cannot be fixed here at all and is a trap instead (§6).**
      `sd -start` and `sd -stop` now ask the `sdwind` process instead of the
      shared segment. Every branch was watched, including the `EPERM` warning,
      which needed two console windows at different elevations. §4 has them.

      **Three things it taught, all of which cost the next reader nothing now
      and would have cost a session each:**

      - **THE MESSAGE THE USER SEES COMES FROM `sdsem.c`, NOT `sysseg.c`.**
        This step named `sysseg.c` line 503 and `bind_sysseg`'s "SD is already
        started."; the string that actually appeared on the stale system was
        **`sdsem.c` line 86's**, which has no full stop and fires first,
        because `get_semaphores(TRUE)` runs before the segment is looked at.
        **Fixing only the two places this step named would have left the bug
        exactly where it was found.** The control run in §4 is what caught it.
      - **The pid in a "stop this process" message must be translated** or it
        names an unrelated Windows process — the MSYS2-pid trap in §6.
      - **`sd -start` does not clear the wreckage for you**, deliberately.
        Sessions can still be attached to a segment whose daemon has died, and
        an `sd -stop` would end them; the count is printed instead so the
        person at the keyboard decides. Reconsider only with a reason.

      **And a fourth thing, from the run that verified it:** a test recipe that
      names `C:\Program Files` tests **the installed binary**, which is only the
      current one just after an install. The first attempt at the `EPERM` test
      did exactly that and reported nothing, which is indistinguishable from
      the fix not working. **State the full path to the build under test.**
   e. **Remove `sudo chmod g+s` from `CREATEA`**, whose Windows equivalent is
      the inheritable ACE the installer already sets (§5.7). It warns on every
      account creation today (§4).
   f. **NEXT, AND IT IS THE ONE THING STOPPING THE ACCESS MODEL BEING TRUE FOR
      A REAL PERSON: give the installer an SD account, at install time.**
      Owner's decision, 14 Aug 2026. Today `don` — who installed SD — types
      `sd` and is refused with `Account DON not in register`, because every
      other account creates its own OS account and his existed first.

      **The SD half is built and the install half is not.** `CREATE.ACCOUNT
      USER x ADOPT` attaches an account to an existing OS account, creating no
      user and setting no password; it is gated on `K$INTERNAL`, so it is
      reachable from `sd -internal` and **not** from a console, which keeps the
      rule a rule for administrators while giving the install one door. What
      remains is calling it: `gplbld/sd.iss` needs a post-install step running

      ```
      sd -internal CREATE.ACCOUNT USER <installing user> ADOPT
      ```

      with the installing user's name, which Inno has, and tolerating the
      account already existing on a reinstall. **Test it on the second machine
      (step 2)** — an install is the only place it happens, and this machine's
      install cannot be re-run without the staleness trap muddying what is
      being tested.
2. **Install on a genuinely clean machine, and test RDP there.** Still the test
   that matters: this machine has a development tree, so an accidental
   dependency could survive, and it is the only place two of the open questions
   can be answered. **The repository owner is building a second machine for
   this** (14 Aug 2026), which is what it has been waiting for.

   **Rebuild the installer first**, and **re-run `stage.py`, not just `ISCC`** —
   a new `gplbld/` script that `stage.py` copies into `ProgramFiles` produces,
   if skipped, an installer whose step cannot find its own script. `stage.py`
   raises rather than warning if a source is missing, so a full rebuild cannot
   get this wrong; only a shortcut can. Full sequence at the top of
   `gplbld/sd.iss`; the `--bootstrap` stage is the slow part.

   What to check there, in order: **count the files** under `sdsys` — do not
   trust Setup's exit code, §4 records why; `sd -start` and `COUNT VOC`
   reporting 431; that `sdwind` is running; then **RDP refusal**, with
   `verify-sshonly.ps1 -Keep` on the machine under test and an RDP connection
   from a different one; and then the rest of §4 Unverified that needs a second
   machine.
3. **Installer loose ends**, none of them blocking:

   - **Nobody has seen the closing dialog or the `AllowGroups` subtask on
     screen** (§4 Unverified). The script compiles; that is a different claim,
     and both defects this file has recorded in that script compiled perfectly.
   - **`GPL.BP/OPGEN` is not ported** to `gen_includes.py`. It generates
     `GPL.BP/OPCODES.H` from `gplsrc/opcodes.h` and reads `./gplsrc` the way
     the others did, but nothing ever `$execute`d it, so it breaks no compile —
     it simply cannot be run on an installed system. Port it before opcodes
     ever need regenerating, and verify byte for byte against the tracked
     `OPCODES.H`; its hex formatting is not obvious from the source.
   - **`sdsys/BP` ships and holds test programs** (`sdTests`, `BIGSTR_TEST`).
     Harmless, and the Linux install did the same, but decide whether an end
     user should get them.
   - **There is no upgrade path for the data tree**, and §6 records what that
     already cost. It will cost more once there is real data in a tree.
4. **Add the audit log** (§5.6). The missing half of the identity model:
   access is controlled, nothing records who used it. Its own append-only file
   that rotates rather than truncates — *not* `<sysdir>/errlog`, which discards
   its oldest half on reaching the `ERRLOG` size. Records every login, every
   `LOGTO`, and every failed step-up, attributed to `@logname`. A failed
   step-up is the single most interesting line in the trail.
5. **GIVE GRANTS A VERB. THE GRANT IS WINDOWS GROUP MEMBERSHIP** — owner's
   decision, 14 Aug 2026, sixth session, settling what the access-model reversal
   left open. Entry to an account is membership of the group named in its
   `ACC$GROUP`, so `GRANT` and `REVOKE` edit that Windows group and write
   nothing to the account record. **`ACC$USERS` is dead and is removed as part
   of this step.**

   **Most of this already exists.** `!os_group` (`GPL.BP/OS_GROUP`) takes
   `ADDMEM` and `DELMEM` against a group name or SID, is idempotent, and returns
   **5 specifically for "not elevated"** rather than a localised error string.
   `!is_grp_member` reads the other direction. So the verb is argument parsing,
   two calls and the messages — not new machinery.

   a. **`GRANT <account> TO <user>` and `REVOKE <account> FROM <user>`**, both
      resolving `<account>` through ACCOUNTS to its `ACC$GROUP` and calling
      `!os_group('ADDMEM'/'DELMEM', that.group, user)`. Refuse an account with
      no `ACC$GROUP` rather than guessing the `sdu_` name — an empty field means
      a record older than `CREATE.ACCOUNT`'s group work, and inventing the name
      would silently create a group nothing else uses.
   b. **It requires elevation, and it should say so before it tries.** Gate on
      `kernel(K$ADMINISTRATOR,-1)` as `CREATEA` line 87 does, so the refusal is
      SD's and not PowerShell's. `!os_group`'s status 5 is the backstop, not the
      user-facing message.
   c. **SAY THE SIGN-OUT PART OUT LOUD IN THE VERB'S OWN OUTPUT.** §6: group
      membership is fixed in the access token at logon, so somebody granted an
      account **cannot use it until they sign out and back in**, and until then
      SD will refuse them with `sysmsg(10003)` as though the grant had not
      worked. This is the single most confusing thing about the model and the
      grant is the moment to explain it.
   d. **Remove `ACC$USERS`, in this order**, because the pieces depend on each
      other: the dictionary item `gplbld/FILES_DICTS/ACCOUNTS.DIC^USERS` (the
      "Granted to" column), then field 4 on existing records, then the
      `$define` in `SYSCOM/KEYS.H` line 269, then `stage.py`'s comment at line
      167 which describes the SDSYS record as carrying it. Doing the define
      first breaks `LIST ACCOUNTS` on the way past.
   e. **Decide how "who may enter this account" is answered**, because it stops
      being a field the dictionary can show. Listing members needs
      `Get-LocalGroupMember`, which is a new `!os_group` action —
      `LISTMEM` — rather than an I-descriptor. Worth doing at the same time:
      an account whose grants cannot be listed cannot be audited by eye.
   f. **Write the audit record from the verb** (§7 step 4). Windows records the
      group edit in its own security log; what SD owes is *who ran GRANT*,
      attributed to `@logname`, in the audit file step 4 introduces.
   g. **Put the work in a subroutine with the verb over it** (§5.14), so the
      admin form that step 10 wants can call the same code rather than
      reimplementing it. `!os_group` exists for exactly this reason.
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

### Open: what may a scheduled job run? (the login half is now answered)

**REWRITTEN 14 Aug 2026, seventh session, because its premise died.** This was
"how does a scheduled job log in, now that every account has a password?",
raised by the repository owner on 13 Aug 2026 and built on the password model,
`ACC$USERS` and `authenticate.account` — none of which exist now. **The login
half answers itself under §5.6:** a scheduled task runs as a Windows user, and
if that user has an SD account, `sd` puts it there with nothing asked. The
batch account is a Windows account plus its SD account, and it grants nobody
because nobody else is in its `ACC$GROUP` group. **No credential is involved
anywhere**, which is what the whole of the rejected reasoning below was for.

**What is still open is the capability list**, and the design is the owner's:
an `X`-type VOC item named `ALLOWED` in **SDSYS's** VOC, holding
`ACCOUNT, VOC name` pairs. Only an administrator can edit it, because it lives
in SDSYS; the job still runs in the named account, so **nothing runs with
administrator rights**. **The mechanism exists and needs no new C code:**
`SYSTEM(1026)` returns the command from the command line (`op_sys.c` case 1026,
from `single_command` in `sd.c`) and `CPROC` does not pick it up until line
556, so `LOGIN` can read and decide first.

**Constraints to build to**, worked out once and recorded so they are not
re-derived: **one token, no arguments, enforced** — this is what does the
security work, not "must be in VOC", since every verb is a VOC item and with no
arguments a verb entry is useless; **accept only `PA` and `S` VOC types**, so a
mislisted verb fails when it is set up rather than at 3am; **any prompt is
fatal in this mode** (§6, the spinning prompt); **the name must be unique
across the list** or `-A` must match, never a silent override; **set `@logname`
explicitly**, since an unattended job has no person behind it; and **catalogue
batch programs locally**, so they do not become runnable from every account.

**Rejected, so it is not proposed again:** a password on the command line
(readable through Task Manager, `Win32_Process` and ETW) and a password file —
both moot now that login takes no password, but the reasoning that killed them
still holds for any future secret: a capability list has nothing to leak or
rotate, and a stolen credential grants an *interactive session* where a list
grants a fixed set of commands. **Hashing the VOC entry** was rejected on its
own merits and still is: it pins one hop and no further, and storing the
command text rather than a name gets the same protection for nothing.

**What it does not fix.** The account boundary is **not** a data boundary — a
Q-pointer in the batch account's VOC reaches another account's files, so "runs
without administrator rights" is worth having but is not a sandbox. And **who
may trigger a job is still open**: the list says what may run, not who may fire
it. The batch account is also the one place per-directory ACLs work in stage 1,
since exactly one principal ever runs there; fold that `icacls` into §5.9.

### SETTLED 14 Aug 2026: the API is piped through ssh — posture B

**Answered by the repository owner**, in the same instruction that made SD
accounts ssh-only (§5.6.2): *"Even the API is piped through ssh."* **Posture B
below was taken** — SD listens locally, ssh carries the traffic, and nothing of
SD's own faces the network.

What that settles, beyond the choice itself:

- **CORRECTED 14 Aug 2026, fifth session — THE API STILL NEEDS AN ACCOUNT
  PASSWORD.** This bullet used to say the API "stops needing a network
  credential model of its own", reasoning that ssh had already authenticated
  the user so peer identity would do. **The repository owner corrected it: in
  the Linux version the ssh tunnel is only the first gate, and the API has no
  access to the server without an account password.** Two gates, not one.

  **This is what saves the credential machinery.** §5.6's reversal takes
  passwords off the console login, which left `$CRED`, `!CRED_SET`,
  `!CRED_VERIFY` and `SET.PASSWORD` with no caller. They are the API's gate
  instead, and are **not to be deleted** (§7 step 0d).

  **What is not settled is which password.** On Linux the API check is
  `login_user()` reading `/etc/shadow`, so it is the *operating system*
  account's password. MSYS2 has no `/etc/shadow` (§6), so the Windows options
  are `$CRED`, which exists and is verified working, or `LogonUser` against the
  Windows account, which would match Linux more closely at the cost of handling
  a Windows credential inside SD. **Decide it with §7 step 6a**, and note the
  no-password-on-a-command-line rule in §5.6.1 applies to whichever is chosen.
- **The AF_UNIX weakness in §6 matters less, but does not vanish.** Binding to
  loopback is not the same as authenticating the peer. A **named pipe** with
  `GetNamedPipeClientProcessId` remains the right Windows answer, and
  `connection_type` already has `CN_PIPE`.
- **It makes the ssh install path load-bearing**, which is why the silent
  failure fixed on 14 Aug 2026 mattered more than an optional extra.

**The client side, as it actually works today.** Supplied by the repository
owner, 14 Aug 2026 — the command their Gambas3 client runs on Linux:

```sh
sshpass -p <password> ssh -L <port>:/tmp/sdsys/sdclient.socket -N <user>@<host> &
```

The contract is: **ssh forwards a local TCP port to a UNIX domain socket on the
server**, and the client library connects to `localhost:<port>`. Four things
about it do not survive the move to Windows, and together they are larger than
the `login_user()` work in §7 step 6:

1. **Nothing on Windows creates that socket.** `start_connection()`
   (`linuxio.c` 130-131) reads `sun_path` from a socket it has *already been
   given* — the server does not listen, it is spawned per connection with the
   socket on its stdin, by xinetd or systemd socket activation. **Windows has
   neither**, so the listener and the per-connection spawn have to be built.
   That is what the retained `etc/xinetd.d/` and `usr/lib/systemd/` document,
   and it belongs with §5.7's service model.
2. **`/tmp/sdsys/sdclient.socket` resolves inside `C:\Program Files\SD\`** by
   the two-component POSIX-root rule in §6 — and Program Files is read-only to
   ordinary users. It needs the same `etc/fstab` bind `/dev/shm` already got.
   The same trap, one directory along.
3. **MSYS2's AF_UNIX is emulated over a TCP loopback socket** with a handshake
   file (§6), not a filesystem object with permissions, so the Linux reasoning
   — local socket, therefore local users only, therefore `getpeereid()` is
   meaningful — **does not carry**. Strongest argument for the named pipe.
4. **`sshpass` does not exist on Windows**, and a password on a command line is
   visible in the process list anyway. A Windows client wants key-based
   authentication, which removes the need to hold a password at all.

**Untested and load-bearing:** whether Win32-OpenSSH supports `-L
port:/path/to/socket` — forwarding to a UNIX domain socket rather than a
host:port. OpenSSH has done so since 6.7 on Unix; whether the Windows port does
it, and whether it can reach an MSYS2-emulated socket, has not been measured.
If it cannot, the transport needs rethinking rather than porting.

**The original question and all three postures** — A, SD's own socket faces the
network; B, ssh or VPN carries it and SD is local only; C, a web front end in
front of a local-only SD — were moved to HISTORY.md on 14 Aug 2026, under
"PROJECT_STATUS rolled over from 4,112 lines". Read it before proposing A or C
again: the case for and against each was worked through at length, and the two
arguments that decide it are that **§1 already points at B** (if the target user
is a Windows developer, their application is the front end) and that C's cost
over B is a second codebase to patch while its benefit — a browser UI — is a
product question rather than a security one.

### Settled: the binaries were purged from history on 13 Aug 2026

Done, and force pushed. See §5.11 and the HISTORY entry. **Any clone taken
before that date is incompatible** and must be re-cloned; do not merge or push
from one. The only remaining copy of the pre-rewrite history is a bundle in a
session scratchpad, which will not survive the machine — see the HISTORY entry
if it is wanted.

### SETTLED 14 Aug 2026: `IsAdmin()` tests Windows `Administrators`, and `sdadmins` is gone

A Windows administrator is an SD administrator; the decision and its measured
basis are in **§5.6.1**. `sdadmins` is referenced by nothing, the installer
need not create it, and it may be deleted from this machine. The two options
not taken are in HISTORY under "PROJECT_STATUS rolled over from 4,112 lines";
one reason is worth carrying: keeping an OS check on `sdadmins` inherits the
sign-out-and-back-in trap in §6, so `sd -start` would have failed for the
installing user on every fresh install.

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
