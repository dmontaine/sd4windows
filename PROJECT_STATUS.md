# PROJECT STATUS

Living handoff document for the SD Windows port. This project moves between
sessions, machines and accounts; anything not written here is lost. Read this
file first. Read [HISTORY.md](HISTORY.md) only if you need the record of how
something came to be the way it is.

**Last updated:** 18 Aug 2026, twenty-first session, on the 07:00:00 install.
**§7 STEP 7 IS CLOSED. `OS.USERS` PERMITS A SHELL, AND THAT HAD NEVER BEEN
SEEN** — `gplbld/verify-osusers.ps1`, **18 of 18 checks, 13 of them decisive,
exit 0**, and the tree was left as it was found. §4 has the table. The
`changelog` entry it was waiting on is written, which makes the install stale
by one file again; that is the normal end of a cycle here, not a fault.

**THE SD RELEASE STRING IS `W1.0-0` — SOURCE ONLY, NOT YET BUILT.** Owner,
18 Aug 2026. **It is the display string and nothing else**: `SD_REV_STAMP` in
`gplsrc/revstamp.h` and `gplsrc/sdclilib/revstamp.h`, `SD.REV.STAMP` in
`sdsys/GPL.BP/REVSTAMP.H`, and the `$RELEASE` records in `NEWVOC` and
`VOC_TEMPLATE` — which must carry the same string or `LOGIN:430` asks every
user to update their VOC. **`MAJOR_REV`/`MINOR_REV`/`BUILD` (still 1/0/2) and
`MESSAGES/0000` (`2.6-6`) are the openQM lineage and are NOT the SD release —
do not renumber them.** A first attempt changed `BUILD` and was reverted.
`gplbld/sd.iss`'s `AppVer` follows (owner, 18 Aug), so the installer becomes
**`sd-setup-W1.0-0.exe`**. `cycle.ps1` picks the NEWEST `sd-setup-*.exe` by
write time, so the `sd-setup-1.0-2.exe` left in `C:\Users\dmont\sdout` cannot
be installed by accident.

**`W1.0-0` SURVIVES `MATCHFIELD(...,"0X0A",1)` INTACT**, checked 18 Aug 2026 —
a leading letter is consumed by `0X`. That pattern exists to strip a TRAILING
alphabetic suffix: `2.6-6a` → `2.6-6`.

**NOTHING ELSE IS BLOCKING AND THE NEXT SUBJECT IS THE OWNER'S CHOICE.** By this
file's own ordering the candidates are **§7 step 8**, the rest of lower case
(§5.12 — the file-name half is done, the other 8 `CASE_INSENSITIVE_FILE_SYSTEM`
sites were deliberately not taken); **§8's per-account ACLs, "the B work"**,
which §5.7 says is what finally makes accounts private from each other; and the
**C half of step 7** — `OS.EXECUTE` is still ungated for everybody, so an
unlisted programmer with `BASIC` reaches the OS from a program whatever
`OS.USERS` says.

**WHERE THIS SESSION LEFT IT — read these five, in order:**

1. **THE `$CRED` ESCALATION IS CLOSED AND VERIFIED — 17:36:21 install, and
   again on the 20:10:31 one.** The cause was candidate (a), proven,
   not inferred: `powershell.exe -File` does not strip single quotes, so
   `sd.iss`'s `-Path '...\sdsys\$CRED'` reached `secure-cred.ps1` with the
   quotes still in the value. `Test-Path` failed on a path that really did not
   exist, the script exited 2 saying so, and the `[Run]` entry discarded the
   code. Measured 17 Aug 2026 with a probe script and a raw command line:

   ```
   -File    -Path '...\sdsys\$CRED'   ->  ['...\sdsys\$CRED']  151 chars
   -File    -Path "...\sdsys\$CRED"   ->  [...\sdsys\$CRED]    149 chars
   -Command -Path "...\sdsys\$CRED"   ->  [...\sdsys\]         144 chars
   ```

   **The comment that caused it was reasoning about `-Command`.** Its claim —
   double quotes expand `$CRED` and leave `-Path` as `...\sdsys\` — is true of
   `-Command` (row 3) and false of `-File`. **The fix this file proposed last
   session, a backtick before the `$`, is also wrong**: `-File` delivers the
   backtick literally too. The fix is plain doubled double-quotes, like every
   other script argument in `sd.iss`.

   **Candidate (b), ordering, was never the cause** — the data-tree `icacls`
   was already ahead of it in `[Run]`.

   **What changed:** `sd.iss` `[Run]` entry → `SecureCredStore` in `[Code]` at
   `ssPostInstall` (`sd.iss:867`), double quoted, **exit code checked**, and a
   failure named in the closing `MsgBox` rather than passed over. Called first
   at `ssPostInstall`, ahead of `AdoptAccount`. `secure-cred.ps1` gained the
   `try`/`catch` the other three `secure-*.ps1` have — it was the only one
   without, and under `$ErrorActionPreference='Stop'` the `2>&1` on `icacls`
   can terminate it unhandled. `ISCC` compiles clean, `[Code]` section and all.

   **`gplbld/verify-credacl.ps1` is new and is how this stops regressing.**
   Nothing checked these ACLs before, which is why it shipped broken and
   stayed broken for a session. **Run it UNELEVATED** — the ACL grants
   `Administrators` Full, so an elevated run passes whatever the ACL says, and
   the script refuses to run elevated. Its decisive check is a write into
   `$CRED`, not a listing.

   **THE UNELEVATED DISCRIMINATOR, before and after any cycle:** `icacls`
   `C:\ProgramData\SD\sdsys\$CRED`. On the broken 17:08:32 install it PRINTS,
   showing `sdusers:(I)(OI)(CI)(M)`. On a good one it answers **Access is
   denied**, which is what `audit`, `sd-elevate.log` and `PSTMP` all already
   answered in the same measurement — three siblings locked, this one not.

   **VERIFIED ON THE 17:36:21 INSTALL AND AGAIN ON THE 20:10:31 ONE, 17 Aug
   2026. This item is CLOSED.**
   `verify-credacl.ps1` unelevated as `GITORLI\don`: exit 0, `assert-current`
   clean. The decisive check is the write, and it is refused —
   `UnauthorizedAccessException` creating a record in `$CRED` — with the DACL
   no longer readable at all. §4 has it.

2. **THE API WORKS. §7 STEP 6 IS CLOSED — VERIFIED ON A REAL INSTALL,
   17 Aug 2026, 17:09.** `gplbld/verify-apiport.ps1 -Prefix sdapi2`, all
   checks passed. The remote transport carried a session, **`$CRED` ran for
   the first time in this project's history**, and the `ACC$GROUP` check ran:

   ```
   right password  ->  admitted, WHO -> 1 SDAPI2
   WRONG password  ->  refused: Invalid username or password
   SDSYS           ->  refused: User not allowed in requested account
   ```

   **The two refusals carry DIFFERENT messages and that is the evidence.**
   `sysmsg(5017)` is `!CRED_VERIFY` rejecting the credential (6a) and
   `sysmsg(10003)` is the group test refusing the account (6c). One catch-all
   message would have proved only that something said no.

   **Also asserted in the same run:** the listener is bound to **127.0.0.1 and
   not 0.0.0.0**, and everything was put back — port closed, account removed,
   `sd.conf` restored.

3. **§7 STEP 11 IS CLOSED AND §7 STEP 6c HAS ITS FIRST EVIDENCE.** Details
   below and in §7 step 11.
4. **§8's THREE TIERS ARE VERIFIED, 22 of 22.** §8 and the tables below.
5. **§7 STEP 7 IS CLOSED — `OS.USERS` ADMITS AS WELL AS REFUSES.** §4 has the
   table; the next subject is at the top of this file.

**THE CYCLE IS ONE COMMAND AND IS NOT TO BE HAND-RUN** — `gplbld/cycle.ps1`,
elevated. It writes a transcript to `%LOCALAPPDATA%\SD-verify`. See "START
HERE".

**THE VERIFY SCRIPTS, each one command. Two are new on 17 Aug 2026, and the
two unelevated ones are the cheap checks to run after any cycle:**

```
gplbld\verify-tiers.ps1 -Keep -Prefix <fresh>   elevated;   §8 three tiers
cd sdb_ai/sd64 && make check-local              UNELEVATED; step 11 + 6c
gplbld\verify-credacl.ps1                       UNELEVATED; step 6, $CRED ACL
gplbld\verify-nocase.ps1                        UNELEVATED; step 8, DHF_NOCASE
gplbld\verify-osusers.ps1                       UNELEVATED; step 7, SH admitted
```

**`verify-credacl.ps1` REFUSES to run elevated** — the ACL grants
`Administrators` Full, so an elevated run passes however broken it is.

**`make` MUST BE RUN THROUGH AN MSYS2 LOGIN SHELL** — see below. And
**`make check-local` runs from `sd64`, NOT from `gplsrc/sdclilib`**: from there
it picks up the MSYS2 `cc` instead of the UCRT64 compiler and cannot run.

**`make` MUST BE RUN THROUGH AN MSYS2 LOGIN SHELL**, and this cost four
attempts:

```powershell
& 'C:\msys64\usr\bin\bash.exe' -lc "cd /c/Users/dmont/Projects/sdb_ai_windows/sdb_ai/sd64 && make sd"
```

A plain non-login shell has no usable Windows `TMP`, so the **UCRT64** compiler
in the `sdsvc` rule falls back to `C:\WINDOWS\` and dies with **"Cannot create
temporary file in C:\WINDOWS\: Permission denied"** — which reads like a
permissions problem and is an environment one. Setting `TMP`/`TEMP` by hand does
not fix it, in either Windows or POSIX form. **`sdsvc` has no prerequisites so
it rebuilds on every `make sd`**, which is why this blocks the whole build
rather than one target.

**§8 is the section to read**; what went in this session:

- **`ADMINISTRATOR` accounts get the 9 administration verbs**, owner's ruling
  "administrators get the whole voc". They were in `VOC_TEMPLATE` alone, so an
  SD administrator had to `LOGTO SDSYS` to administer anything.
- **`MODIFY`, `COMPILE.DICT`, `CD`, `GENERATE`, `PHANTOM`** join the standard
  omit list — owner, "all should be programmer and above". 13 ids → **18**.
- **THE TIERS WERE UNDOABLE BY ANY USER AT A PROMPT AND ARE NOT NOW.**
  `LOGIN:501 update.voc` re-copied the whole of `NEWVOC`; it is reached from an
  ordinary login by the `$RELEASE` question at `LOGIN:419`. The tier is now
  recorded at `ACCOUNTS` field 5 (`ACC$TIER`, `KEYS.H:281`) and `LOGIN` applies
  the omit list. **This is the one to check on the cycle** — §8, "how to test
  it", has the three-account recipe and its controls.
- **`ADOPT` defaults to the administrator tier**, or the installing user's own
  account comes out standard with no `BASIC`, no `ED` and no `CATALOG`.

**IT COMPILES, IT IS INSTALLED, AND THE ADMINISTRATOR TIER HAS RUN.** 17 Aug
2026, on the 10:34 install, `assert-current` exit 0. `gcat` **132**,
`GPL.BP.OUT` **193**, `$BCOMP` **87,992**, `$CPROC` **25,208**.

**Verified without elevation, by reading the install:**

- **`ACC$TIER` is written and `ADOPT` defaults to ADMINISTRATOR** —
  `ACCOUNTS/DON` field 5 reads `ADMINISTRATOR`, **field 4 empty**, so the
  poisoned field was skipped as intended. `SDSYS` reads blank, which is right:
  its record comes from the bootstrap, not `CREATEA`.
- **An administrator gets all 9 administration verbs**, checked by their
  **unique program names** (`$CREATEA` `$DELACC` `$MODIFYA` `$GRANTA`
  `$UNLOCK` `$CRYPTO`) rather than by verb id, because `GRANT` is a substring
  of `LIST.GRANTS`.
- **Neither `TIER.*` list record reached a VOC**, and all 18 withheld ids are
  present in DON's — correct for an administrator.
- **`COUNT VOC` in DON's account is 420, which is the derived figure exactly.**
  Installed `NEWVOC` holds 410 names, less `%t` (a dynamic-file artefact, not a
  record) and the two list records = **407 copied**, + 9 administration verbs,
  + `CREATEA`'s own four (`$COMMAND.STACK`, `$HOLD`, `$SAVEDLISTS`, `BP`).
- **AND AN UNELEVATED INTERACTIVE SESSION WORKS ON THIS INSTALL** — `WHO`
  answers **`2 DON`**. That was an open item in this header for two sessions.

**ALL THREE TIERS RUN, AND THE DURABILITY FIX HOLDS — 17 Aug 2026, 11:31:38.**
`gplbld/verify-tiers.ps1 -Keep -Prefix sdtierb`, **22 of 22 checks passed**;
transcript at `C:\ProgramData\SD\verify\verify-tiers-20260817-113138.log`.
**`COUNT VOC` landed on all three derived figures exactly:**

| | `COUNT VOC` | withheld 18 | administration 9 |
|---|---|---|---|
| STANDARD | **393** | 0 / 18 | 0 / 9 |
| PROGRAMMER | **411** | 18 / 18 | **0 / 9** |
| ADMINISTRATOR | **420** | 18 / 18 | 9 / 9 |

**The PROGRAMMER row is the one that means anything** — the 18 present and the
9 absent is the only control on the add list, and without it a copy loop that
omitted nothing would pass the other two rows. **`UPDATE.ACCOUNT` in the
standard account left it at 393 with all 18 still missing**; before `ACC$TIER`
it restored every one of them.

**CONFIRMED TWICE, BY TWO INSTRUMENTS.** The script asks SD (`COUNT VOC`,
`LIST VOC`); the numbers above were then re-derived independently by reading the
account VOCs as bytes and matching the on-disk record framing
(`\0\0\0` + id + type letter, learned from DON's `%0`), which has no substring
ambiguity — `ED` matches almost anything by naive search. Both agree.

**Cleaned up 17 Aug 2026** — `ACCOUNTS` is back to `DON` and `SDSYS`,
`assert-current` exit 0. `verify-tiers.ps1` removes only the Windows half, so
each run leaves its `ACCOUNTS` records behind for `DELETE.ACCOUNT`, and
**re-running it needs a fresh `-Prefix`**; it now says so rather than failing
inside `CREATE.ACCOUNT` several steps later.

**§7 step 11's FIX is in the same owed cycle**, and it is C — it went in after
the 07:20:40 install and has never been installed. `assert-current` fails and is
right to; it listed ten stale files on 17 Aug at 10:0x.

**A `gplbld` or Makefile edit forces a relink even when no C changed**, because
the staleness guards compare mtimes and are deliberately blunt — a false
"stale" costs one install, a false "current" costs an investigation. Just run
`make sd` again and take the new hash; do not loosen the check.

**§7 STEP 6c HAS COMPILED — that risk is spent.** The 07:20:40 bootstrap took
it: `gcat/$APISRVR` **9,323 bytes** against 9,129 after 6a and 9,056 before.
`gcat` 132, `GPL.BP.OUT` 193. What 6c still lacks is a RUN.

**§7 STEP 11 IS CLOSED — VERIFIED ON A REAL INSTALL, 17 Aug 2026.** The cycle
ran, `assert-current` exit 0 against the **12:28:49** install (`sd.exe`
**`81D0856F5493385E`**, `sdclilib.dll` **`8D1517D1CD2B83AB`**), and
**`make check-local` PASSES**:

```
connecting to DON ...      admitted     WHO -> 2 DON
connecting to SDSYS ...    refused: User not allowed in requested account
PASS: DON admitted, SDSYS refused.
```

**AND THAT REFUSAL IS THE FIRST VERIFIED EVIDENCE FOR §7 STEP 6c** — the
`ACC$GROUP` grant check in `APISRVR`, built this morning and never run. `DON`
admitted alone would be equally consistent with a check that never executed.
The installed tree is whole: `gcat` **132**, `GPL.BP.OUT` **193**, `$BCOMP`
**87,992**, `$CPROC` **25,208**, **3,483 files**. `ACCOUNTS/DON` field 5 reads
`ADMINISTRATOR` on this install too.

**THAT CYCLE HAS NOW RUN — 13:43:00, `assert-current` exit 0, `make check-local`
passes.** It exposed a **fourth** harness defect, again about the tooling and
not about SD.

**THE FOURTH DEFECT: `cycle.ps1` FAILED AN INSTALL THAT WAS PERFECTLY FINE.**
Step 8 stopped with `no C:\ProgramData\SD\sdsys\gcat after the install - it did
not complete`; the install finished normally seven minutes later and the tree
was whole. **Cause: `& $setup.FullName` — PowerShell's call operator does not
wait for a GUI-subsystem process**, and Setup.exe is one (PE subsystem **2**,
read off `sd-setup-1.0-2.exe` rather than assumed). So the 300-second count
deadline started when the **wizard opened** instead of when it was dismissed,
and reading the closing dialog — which the non-silent default exists to invite
(§7 step 3) — is what exceeded it. **Fixed with `Start-Process -Wait`**; the
count deadline is kept as the backstop for the respawn case.

**A FALSE FAILURE HERE COSTS AS MUCH AS A FALSE PASS.** It reads exactly like
the broken-bootstrap install of 16 Aug, which is the one thing this script
exists to catch, and the natural response is to spend another cycle.

**AND THE FILE COUNT IS NOT THE CHECK.** This tree is **3,473** files at rest
against the **3,483** recorded on the 12:28:49 install, and **nothing was
missing** — the difference is whether SD is running, since the live segment and
the logs sit inside `sdsys`. The stage-against-install file comparison came back
empty, with `audit` and `ACCOUNTS/DON` the only extras. §7 step 2 still says to
count files.

**THREE HARNESS DEFECTS THE PREVIOUS CYCLE EXPOSED, ALL FIXED, NONE ABOUT SD:**

1. **`cycle.ps1` step 8 counted MID-INSTALL** and reported `GPL.BP.OUT` **5** on
   an install that was fine and finished with 193. It waited for
   `gcat\$CPROC` to exist, which is nowhere near the last file written. **A
   number read off a half-copied tree is the exact failure step 3 exists to
   catch, and it was being printed as the result.** It now waits for the
   installed counts to REACH the staged ones — which are known, having just
   been measured — and **fails** if they never do.
2. **`CC ?= gcc` in `gplsrc/sdclilib/Makefile` never fired.** `?=` means "if
   UNDEFINED", and make's built-in `CC` has origin `default`, which is defined —
   so `CC` stayed `cc`. The DLL escaped it because the top-level passes `CC=`;
   `make check-local` did not, and built a NATIVE test with the MSYS2 compiler.
3. **`make check-local` had no `PATH` to run with**, and answered **"Error 127"**
   — which reads as a broken transport. A plain MSYS2 login shell has neither
   the installed bin (the loader is *meant* to fall through to it) nor
   `System32`, and the test is a native UCRT64 binary resolving
   `api-ms-win-crt-*.dll` through the OS. **`make check-local` now runs from
   `sd64`**, not from `gplsrc/sdclilib`, so it gets the right compiler.

**The fix was the transport, and the two options in the old handoff were not
the only two.** A descriptor Cygwin builds itself from an **inherited standard
handle** answers `select()` honestly; the always-ready behaviour belongs to
**injecting a raw HANDLE**, not to pipes. **And the peer identity never came
from the named pipe** — nothing in `gplsrc` ever asks a pipe who is on the
other end; `sd.exe` is a CHILD and runs under the caller's token. §7 step 11.

**§7 STEP 11's OLD PATH DOES NOT WORK, AND `sd.c` NOW SAYS SO RATHER THAN
HANGING — READ §7 STEP 11 BEFORE REVIVING IT.** Three real defects were found
and fixed (`-C` argument mismatch, `sd.exe` location, and the access argument to
`cygwin_attach_handle_to_fd()`), and a fourth thing is not a defect and stopped
that approach: **a descriptor made from a raw HANDLE is reported PERMANENTLY
READY by `select()`**, so SD's `sdpoll()` always says "input waiting" and
`sd.exe` spins reading one byte at a time, silent, never answering.
**Do not go looking for another flag** — six name/access combinations,
`O_NONBLOCK` and `F_SETOWN` were all measured.

**That is history now: the transport was replaced, not repaired.** The pipes are
handed to the child as its STANDARD HANDLES and `make check-local` passes. Only
the `-C <pipename>` calling convention still leads to the always-ready path, and
`sd.c` refuses it with a diagnostic rather than hanging. **This paragraph said
"`make check-local` HANGS today", and it did**; it is kept because the
measurement behind it is still the reason not to revive that path.

**`strace` IS IN MSYS2 AND IS WHY THIS WAS DIAGNOSED AT ALL** —
`/c/msys64/usr/bin/strace.exe`, works on `sd.exe`, one run where three install
cycles would have shown nothing. There is no `gdb` here.

**`sd.exe`'s hash has moved three times today and only once for a code change**,
so do not read meaning into a difference from an older note: relinking restamps
the PE `TimeDateStamp`. **`A89DDE70D6AA319F` is the one to install.**

**The installs of 06:07:30 and 07:20:40 were both whole**, and what was measured
on them stands: `gcat` **132**, `GPL.BP.OUT` **193**, `$BCOMP` **87,992** (not
the 70,697 seed), and **every staged file present** — a file-list comparison of
the stage against the install came back empty, the extras being only
install-time artefacts (`ACCOUNTS/DON`, `audit`, the logs, the live segment).
**That comparison is a better check than counting files** and costs the same;
§7 step 2 still says to count.

**§7 STEP 6a's BASIC HAS BEEN THROUGH A COMPILER AND PASSED.** That was the
predicted failure point of the last handoff and it held: `SECOND.COMPILE` on
this bootstrap was `APISRVR`'s first, `bootstrap.py` dies on any error, and it
did not. `gcat/$APISRVR` **9,129 / `84f7d949…`** against **9,056 /
`49c28f05…`** before. **It still has never RUN, and the transport no longer
excuses it.** Corrected 17 Aug 2026: this said the transport blocked it, and the
LOCAL transport now works — but `SrvrLocalLogin` sends no password, so it never
reaches 6a's `$CRED` check at all. **6a needs the REMOTE path**, which is
§7 step 6a/6b and the next subject. **6c, the `ACC$GROUP` grant check, HAS now
run** — §7 step 11.

**§7 step 1a is CLOSED, with the control** — §7 has both lines. That was the
last unverified branch of step 1.

**CLOSED 17 Aug 2026 — an unelevated interactive session HAS now been checked**,
on the 10:34 install: `WHO` answers **`2 DON`** and `COUNT VOC` **420**. It was
never a tooling limit after all — piping `"`n<commands>`nOFF`n"` into `sd.exe`
from PowerShell drives an ordinary session perfectly well, the blank first line
absorbing the BOM exactly as `verify-createaccount.ps1` has always done. **The
note that stood here said it could not be done and blamed §6**; it is left
visible because two sessions deferred a check that cost one command.

**THE ssh SERVER IS NO LONGER OPTIONAL.** Owner's decision, fifteenth session,
reversing the opt-in of 14 Aug. §5.9 has the reasoning and what changed.

**THE 17:51:35 INSTALL WAS A FAILED BOOTSTRAP AND NO SD SESSION EVER RAN ON IT.**
Found and replaced 16 Aug 2026, sixteenth session; kept here because of what it
voids and what it teaches. It was 337 files short — `gcat` **4 entries not
132**, `GPL.BP.OUT` **3 not 193**, `gcat/$CPROC` **0 bytes** (the touched
placeholder), **no `$LOGIN`, no `VOC`** — and every cell of a four-way control
died `Unable to load '$CPROC' object code`, exit `0xC0000005`.
**SO EVERY SD-SIDE CLAIM RESTING ON THAT INSTALL IS VOID**, including the one
in §8 that became an open question. The Windows-side ssh measurements below
stand: they never start SD.

**Cause, now a trap in §6 and a gate in `stage.py`:** the installer of
**17:34:39** was built from a staging tree whose bootstrap had died after the
**seed** phase — its `gcat` held `bbcmp.py`'s objects (`$BCOMP` 70,697) where a
finished tree holds `BCOMP`'s (87,992). `C:\Users\dmont\stagetest` was healthy
and was not what got packaged. **`assert-current` cannot see this** — it
compares the install against SOURCE, and `gcat` is a build product, so it
exited 0 over the broken tree and was right to.

**WHAT STANDS from that install:** the **"leave an ssh server we did not
install alone"** branch, measured against a pre-install baseline — firewall
rule still `Enabled True / Private / Any`, `sshd_config` still `11:11:30 /
2297 bytes`, PATH 7/0. **The mandatory-install branch is structurally
untestable on this machine**, which already has OpenSSH — only the "leave it
alone" branch runs here and both new tasks are hidden. It needs the VM from
step 2. §7 step 3.

**THE REWRAPPED FIRST PAGE IS VERIFIED — owner, 17 Aug 2026: it renders FULL
WIDTH.** The 16 Aug fix worked: paragraphs are one long line and the memo
word-wraps to whatever width it has, instead of the hand-broken ~50-character
column it replaced. Do not reintroduce a line break or an indent inside a
paragraph there (`sd.iss:563` says why). **AND THE CLOSING DIALOG HAS NOW BEEN
READ ON SCREEN — owner, 17 Aug 2026, on the 13:43:00 install: "looks fine".**
That was an open item here; §7 step 3's source re-check and what is on screen
now agree. **It does not cover the ssh half** — `limitssh` and `sshremote` stay
hidden on this machine and still need the VM.

**`gplbld/secure-accounts.ps1` IS NOT WIRED IN AND MUST NOT BE WIRED IN ALONE.**
It is in neither `stage.py`'s ship list (`stage.py:427`) nor `sd.iss`, so it
neither ships nor runs — it was written and left. **Do not just add it:** it
breaks inheritance on `user_accounts` and leaves `sdusers` nothing inheritable,
so a directory created under it carries `CREATOR OWNER` and no `sdu_<name>` —
the account's own user, and anyone `GRANT`ed it, would be refused at the file
layer. Its partner half does not exist: **`CREATEA` contains no `icacls`
anywhere**, checked. Land both halves together or neither.

**From the FIFTEENTH session, not this one:** an up-front wizard page listing
what the installer changes on the machine, and two comments in `sd.iss`
corrected that claimed `CurStepChanged` checked things it never read (the
OpenSSH exit code — now replaced by `SshReport` reading machine state — and
`deny-logon.ps1`, still unchecked, §7 step 3).

**AND ITS LONG DESIGN THREAD, WHICH PRODUCED NO CODE BUT MOST OF THE VALUE.**
File permissions, the three-tier user model, and two defects in the shipped
`VOC_TEMPLATE`. **It is all in §8, and §8 is the one to read** — it holds the
finding that the two user tiers which exist today are **enforced backwards**,
which is still open and still the thing to act on before designing more of them.
**Its `CA`-resolution question is ANSWERED and is no longer a blocker** —
`$QPROC` is in `gcat` at 54,073 bytes; the question came from measuring the
broken install. Scoping the `gcat` lock is against 132 entries, not 4.

**Previous session (fourteenth, `99e936f`→`00432d8`):**
**ELEVATION WITHOUT AN ELEVATED TERMINAL IS COMPLETE — built, installed and
verified end to end**, with the watchdog, the audit trail, the helper log and
its ACL. **§7 step 4 and step 5 are both closed.** **Six defects were found and
fixed on the way and NOT ONE was visible by reading the code** — every one sat
at a seam between two halves that were each correct alone (item 1). Seven full
install cycles; that rule paid for itself repeatedly.

**A TEST CYCLE STARTS WITH A FRESH INSTALL — uninstall, delete BOTH trees,
reinstall — AND ENDS AT THE NEXT SOURCE CHANGE.** Owner's rule, in CLAUDE.md.
**Never a reinstall over the top**, and **do not reason your way out of it from
file hashes**: the ninth session tried, and 4 matching files out of ~3,455 is
not evidence a tree is current. **The second half of that rule was added on
15 Aug 2026 after the rule was broken twice in one session** — both times by
editing source while a test was in flight and reading the results anyway.
**It is enforced now**: `gplbld/assert-current.ps1` exits non-zero unless the
installed tree matches source, and `verify-createaccount.ps1` refuses without
it. Call it first from anything new that tests the install.

**START HERE, in order:**

**1. RUN THE CYCLE FIRST — but know that it only carries HARNESS fixes.**
`assert-current` fails and should: `gplsrc/sdclilib/Makefile` moved at 12:32:56,
after the measurements. **`make sd` is NOT needed** — the installed binaries
(`81D0856F5493385E` / `8D1517D1CD2B83AB`) are the current build. **Everything
this session claims was already verified on the 12:28:49 install**, so the
cycle is owed for cleanliness, not to settle anything.

**Both verifications are one command each and both have passed**, so re-running
them after the cycle is a re-confirmation rather than an open question:

```sh
cd sdb_ai/sd64 && make check-local
```
```powershell
gplbld\verify-tiers.ps1 -Keep -Prefix sdtierc
```

**`check-local` is UNELEVATED and from an MSYS2 LOGIN shell** — `make` is not a
Windows command, PowerShell has no `&&`, and a non-login shell has no usable
`TMP`; all three were got wrong here. **From `sd64`, NOT from
`gplsrc/sdclilib`**: that directory's `CC` is the MSYS2 `cc`, and it builds a
native test that cannot run. The target builds into `localtest/`
**deliberately**, so the loader does not find the build tree's `sdclilib.dll`
(which has no `sd.exe` beside it) and falls through to PATH and the installed
pair instead — and the target now puts the installed bin and `System32` on PATH
for the run, without which it answers `Error 127`.

**`verify-tiers.ps1` is ELEVATED and needs a FRESH `-Prefix` each run**, because
it leaves its `ACCOUNTS` records behind for `DELETE.ACCOUNT`. Both scripts write
transcripts to `%LOCALAPPDATA%\SD-verify`, which is outside the trees the cycle
deletes.

**THE CYCLE IS ONE COMMAND NOW — `gplbld/cycle.ps1`.** Owner's instruction,
17 Aug 2026: it had grown to four commands across three shells and it used to
be PowerShell and fewer steps. **Elevated PowerShell, from anywhere:**

```powershell
C:\Users\dmont\Projects\sdb_ai_windows\sdb_ai\sd64\gplbld\cycle.ps1
```

Stops the service, stages, bootstraps, checks the staged tree is whole, builds
the installer, uninstalls, deletes **both** trees, installs, then runs
`assert-current`. `-SkipInstall` stops after the installer, which is the cheap
way to find out whether a BASIC change compiles. `-Silent` for `/VERYSILENT`.

**IT WAS WRITTEN AFTER THE HAND-RUN SEQUENCE FAILED TWICE IN ONE ATTEMPT**, and
both faults are now impossible rather than documented:

- **The SD service was still running.** The staged `etc/fstab` points
  `/dev/shm` at the **live** tree, so the bootstrap's `sd -start` collided with
  the live server, `sd -i` produced nothing, and the staged tree was left in
  the seed state — `gcat` **4**, `$BCOMP` **70,697**, `$CPROC` **0 bytes**,
  no `VOC`. **That is the state that shipped a catalogue-less install on
  16 Aug.** Step 1 now stops the service and waits for `sdwind` to go.
- **`ISCC` was run from `C:\WINDOWS\system32`**, where `gplbld\sd.iss` does not
  resolve. It answers **"The system cannot find the path specified"** without
  naming the file. Every path in the script is absolute and derived from the
  script's own location.

**AND THE SCRIPT'S FIRST RUN HIT THE SAME FAULT FROM THE INSIDE.** Its
wholeness check used `$out` for the `GPL.BP.OUT` count and **PowerShell
variable names are case-insensitive**, so it overwrote the `$Out` **parameter**
with **193**. ISCC got `/O193` and wrote a perfectly good installer to a
relative `193\`. **A relative path here does not fail, it succeeds somewhere
nobody looks** — which is why `-Stage` and `-Out` are now required to be rooted
and are resolved absolute before anything runs, and why every local in that
block is prefixed. Cleaned up 17 Aug 2026.

**AND IT DID NOT LAND WHERE ISCC SAID IT DID — `ISCC` IS 32-BIT.** It reported
`C:\WINDOWS\system32\193\sd-setup-1.0-2.exe`; the file was in
**`C:\WINDOWS\SysWOW64\193\`**, because `C:\Program Files (x86)\Inno Setup 6\`
is a 32-bit binary and **WOW64 silently redirects a 32-bit process's writes to
`system32` into `SysWOW64`**. This file said "delete `system32\193`" and there
was no such directory, which is corrected here rather than replaced because the
mistake is the instructive part: **ISCC reports the path it was ASKED for, not
the one it got**, so any path handed to it is subject to that rewrite. Only
`system32` is affected, and only for a relative path resolved against an
elevated shell's default directory — but that is exactly the case this hit.

**Still elevated, and that is checked first** — `--bootstrap` ends in
`sd -internal` steps SDSYS refuses unelevated, and `bootstrap.py:179` only
notices after the seed phase has already rewritten the staging tree.
**`stage.py` refuses to stage a tree whose bootstrap did not finish**;
`cycle.ps1` step 3 tests the same thing again, because that is what stands
between a silent bootstrap failure and an installer built from the wreckage.
`assert-current` **cannot** see that failure: it compares the install against
SOURCE and `gcat` is a build product. `gcat` 132 / `GPL.BP.OUT` 193 /
`$BCOMP` 87,992 — the script prints all three.

**The wizard pages are no longer owed.** The first page is verified full width
(header); the closing dialog's content was re-read out of `sd.iss` on 17 Aug
and carries no `net localgroup` offer. Only its on-screen rendering is
unreported, and nothing depends on it.

**2. THEN PICK UP §7.** Step 1 is **closed entirely** — 1a went on 17 Aug with
its control; step 4 and step 5 are closed; **step 6 is now built in full —
a, b, c and d — and NOT RUN** (§4 Not verified). What is left, in the order it
makes sense:

- **STEP 11, AND IT IS NOW THE SHORTEST PATH TO EVIDENCE.** `SDConnectLocal()`
  is built and has never been called. A local session reaches `SrvrAccount`,
  so **it can test step 6c without ssh, a tunnel or a remote client** — which
  is the first evidence step 6 would have of any kind. Run the cycle, then
  write something small that calls the DLL.
- **THEN THE REMOTE TRANSPORT**, which is what 6a and 6b still wait on: the
  listener and per-connection spawn Windows has no xinetd or systemd for. That
  work belongs with §5.7's service model.
- **The transport, and it is now forced rather than optional.** The Linux
  client contract cannot be ported — measured, §8 — so the API cannot be
  exercised end to end until a **named pipe** exists. That work belongs with
  §5.7's service model, not with step 6, and it is what unblocks verifying
  everything step 6 has built.
- **The VM work**, which this machine cannot do: the mandatory-ssh install
  branch (§7 step 3), and §5.6.2's remaining ssh items.
- **§8's three-tier model**, where the live finding is that the two tiers which
  exist today are **enforced backwards**. It is blocked on per-account ACLs,
  and `gplbld/secure-accounts.ps1` is half of those and **must not be wired in
  alone** — see below.

**FOUR THINGS THIS SESSION LEARNED THE HARD WAY. They cost a cycle each and
none of them is about SD:**

1. **An uninstaller fix cannot be verified in the cycle that ships it.**
   `unins000.exe` is generated at INSTALL time, so the uninstall that begins a
   cycle always runs the PREVIOUS install's code. Verify such a change by
   running uninstall and install as SEPARATE steps and reading the state in
   between.
2. **Read the registry, never `%PATH%`.** A shell opened before an install
   keeps its own copy. That appearance — "SD is not on PATH" — misled twice in
   one session; both times the registry was right.
3. **Exclude your own shell from any `Get-CimInstance Win32_Process | Where
   CommandLine -like` search.** The search text is in your own command line, so
   you match yourself. This produced a false "WATCHDOG FAILED" and a
   `Stop-Process` aimed at the measuring shell.
4. **`sd-elevate.ps1` gives UAC consent a bounded wait.** A slow click leaves
   `-Start` giving up with no helper for any test to find. Three attempts at
   the watchdog died on this before it was understood.

**AND ONE ABOUT THIS FILE.** Four of the six defects were fixed by reading the
comments around the code, and two of those comments were WRONG in a way that
had caused the defect — `PS_SCRIPT` arguing a file was safe because the
installer "grants narrowly" (narrow against the world, not against SD's own
users). **Both were corrected in place rather than replaced**, so the mistaken
reasoning stays visible. Do the same.


1. **CLOSED AND VERIFIED END TO END — ELEVATION WITHOUT AN ELEVATED TERMINAL.**
   16 Aug 2026, fourteenth session, `3e010cf` and `2f32f6f`. **An unelevated SD
   session created a Windows account.** Two defects had to be fixed first; both
   are below because they are what to look for if this regresses.

   **THE MEASUREMENT, on the 14:21:50 install** — `assert-current` exit 0,
   installed `gcat/$CPROC` 25,208 and `sd-elevate-helper.ps1` carrying
   `Get-Content -LiteralPath`. **Check those two, not `sd.exe`**, which neither
   fix touches and which is unchanged at `239BB9C3E43E4829` across all three
   builds of this session.

   - `sd` unelevated → `LOGTO SDSYS` → **UAC prompt, accepted** → `WHO` answers
     `2 SDSYS from DON`.
   - `CREATE.ACCOUNT USER sdacct11` → **`User sdacct11 Created`**, password
     set, added to `sdusers` and `sdsshonly`, `sdu_sdacct11` created, account
     directories built, registered. Windows side confirmed: enabled,
     description `SD account`, **not** an administrator.
   - `LOGTO DON` → back out, `OFF`, exit 0. **No helper process and no
     `sd-elev-*` pipe survive.**
   - **The trail, which is the proof the mechanism did what it looked like:**
     `ELEVATION GRANTED account=SDSYS` / `LOGTO account=SDSYS` /
     `ELEVATION RELEASED account=DON` / `LOGTO account=DON`, with ten seconds
     between the grant and the release — `CREATE.ACCOUNT` working through the
     helper. **`ELEVATION RELEASED` proves `LOGTO` out of SDSYS sends `STOP`
     deliberately**, rather than the helper dying of a watchdog.
   - **Declining the prompt is refused**, `sysmsg(10002)`, re-measured on this
     same build. The matching trail line
     (`reason=elevation refused or unavailable`) was observed on the first
     build of the session, not this one.

   **DEFECT 1, `CPROC`.** `logto.authorised` (`CPROC:3602`) tested
   `kernel(K$ADMINISTRATOR,-1)`, which reads `USR_ADMIN`: a session flag seeded
   **once** from `IsElevated()` at process start (`kernel.c:195`) and settable
   only by an `$internal` program (`op_kernel.c:325`). **SD stays unelevated
   for life by design**, the privilege being the helper's, so that flag is
   false and always will be. `CPROC:2639` sets it 40 lines after the test that
   needed it. `6dadaa1` removed the old gate and added `elevate('START')`
   without joining the halves, so **`LOGTO SDSYS` refused the elevation it had
   just obtained**. **Signature: `ELEVATION GRANTED` and `LOGTO REFUSED ...
   reason=not granted` in the same second.** Fixed with `elev.obtained`,
   cleared per-LOGTO — a session flag would carry a grant into the next LOGTO
   and admit a caller to an account just refused — plus
   `logto.privilege.undo` at the **four** failure exits between the elevation
   and the move, none of which released the helper.

   **DEFECT 2, `sd-elevate-helper.ps1`.** It ran scripts with
   `powershell -File`, and **`-File` refuses any file not named `*.ps1`**:
   measured, exit **-196608**, nothing executed. `!ps_script` names these
   `$PS.TMP.<userno>`, so **that path could never have run a single request**.
   `!ps_script`'s own local path uses `Get-Content | Invoke-Expression` for
   exactly this reason; the helper now does the same, so the two differ only in
   privilege. **Signature: `Create User Failed, OS Error: 127`** — and note it
   is **not** the `5` an unprivileged attempt gives, which is what says the
   privilege was real and the fault was downstream of it.

   **STILL OPEN, neither in the way of the feature:**

   - ~~The `-OwnerPid` watchdog is untested.~~ **VERIFIED 16 Aug 2026.** Its
     own log: `helper up, pid 11260, serving session 3004` at 14:41:42, then
     `session 3004 has gone - exiting` at 14:41:44 — **two seconds**, matching
     the 2000ms idle wake at `sd-elevate-helper.ps1:78`. Tested against a
     **dummy owner process rather than `sd.exe`** — but the trail then showed
     it is **also proven against a real one, twice**: the sessions at 14:31:14
     and 14:39:18 entered SDSYS, were killed outright, and **wrote no
     `ELEVATION RELEASED`**, so SD never sent `STOP`; no helper or pipe
     survived either (checked 14:32:42 and 14:40:25). Only the watchdog can
     have removed them, which also settles that `K$WINPID` hands over the right
     pid.
     **HOW TO RUN IT AGAIN, because three attempts through a real SD session
     all failed first:** `sd-elevate.ps1:103` gives consent a bounded wait, so
     a slow UAC click makes `-Start` give up and no helper ever exists. Launch
     the installed helper directly instead — `Start-Process powershell -Verb
     RunAs ... -File <helper> -PipeName x -OwnerPid <dummy> -LogFile <path>` —
     then kill the dummy. **And exclude your own shell from any
     `Get-CimInstance Win32_Process | Where CommandLine -like` search**: the
     search text is in your own command line, and matching yourself reports a
     live "helper" and can end with `Stop-Process` killing the shell doing the
     measuring. That happened here and produced a false FAILED.
   - ~~`GRANT`/`REVOKE` has not been watched writing a record.~~ **DONE
     16 Aug 2026, §7 step 5 COMPLETE.** `GRANT account=SDACCT11 to=don` at
     14:48:22 and `REVOKE account=SDACCT11 from=don` at 14:48:24, both from an
     unelevated session that had entered SDSYS. The Windows group was edited
     and correctly reverted, so the machine is as it was.
   - ~~`LIST.GRANTS` is broken.~~ **FIXED AND VERIFIED 16 Aug 2026** on the
     15:26:33 install: `LIST.GRANTS DON` prints `don`, and `LIST.GRANTS
     SDACCT12` prints `sdacct12` on an account created moments earlier.
     **What it was:** `OS_GROUP` prepends an elevation guard to **every**
     action's script, each action appending its body to it. The writing actions
     pass it because `!ps_script` sends them to the elevated helper, but
     **`LISTMEM` is deliberately kept local**, so it ran in the
     permanently-unelevated `sd.exe` and hit `exit 5` before reaching
     `Get-LocalGroupMember` — `status: 5`, always, for anyone without an
     elevated terminal. The guard is now built only for the actions that go to
     the helper. **`CREATE.ACCOUNT` was re-run in the same session as a
     regression check**, since that edit changed how `ps` is built for every
     action: `sdacct12` created correctly, groups and all.
   - ~~The helper writes no log.~~ **BUILT AND VERIFIED 16 Aug 2026**, owner's
     decision. `C:\ProgramData\SD\sd-elevate.log`, beside `sdsvc.log`,
     created by the installer through `gplbld/secure-log.ps1`.

     **Both halves measured on the 16:02:58 install.** The ACL: `don`
     unelevated is refused reading it **and refused reading its ACL** —
     `icacls` itself answers `Access is denied` — because `sdusers` is absent
     entirely, which is stricter than the audit trail's `AppendData`. Nothing
     unelevated writes this file, so nothing unelevated needs rights to it.
     The content, after one `LOGTO SDSYS` + `CREATE.ACCOUNT`:

     ```
     16:04:10 helper up, pid 6808, serving session 9308
     16:04:12 ran C:\ProgramData\SD\sdsys\$PS.TMP.2 -> 0    (six of these)
     16:04:20 stop requested
     16:04:20 helper exiting
     ```

     `stop requested` is `LOGTO` out of SDSYS sending `STOP`, the same event
     `ELEVATION RELEASED` records from SD's side. `serving session 9308` is
     `sd.exe`'s Windows pid — `K$WINPID` again.

     **`!elevate` is unchanged and deliberately so**: nothing in BASIC can name
     the file, the installed tree mapping only `/dev/shm`, so `/` is
     `C:\Program Files\SD` and no POSIX path reaches the data tree.
     `sd-elevate.ps1` derives it from `%ProgramData%` exactly as the installer
     does (`DataDir` is `{commonappdata}\SD`), so the two cannot drift.
     **It logs only if the file already exists** — creating it on the fly would
     inherit the data tree's Modify for every `sdusers` member.
     **AppData was raised by the owner and rejected on measurement:**
     `%LOCALAPPDATA%` grants Full Control **and the user owns it**, so an
     owner's implicit `WRITE_DAC` lets the subject of the log reset any ACL put
     on it; `C:\ProgramData\SD` is owned by `BUILTIN\Administrators`. Second
     reason: the helper runs as whichever administrator consented, so with a
     standard user at the keyboard the log would scatter across profiles.

     **KNOWN LIMIT, not a defect:** every `ran` line names the same path,
     because `!ps_script` reuses one temp file per user number. The log gives
     the count and each exit code but **not which operation was which** — in a
     failure you learn that the third step returned 1, not that the third step
     was the `sdsshonly` add. Fixing it means `!ps_script` passing a label;
     **logging the script body is permanently out** — see the next item.
   - ~~The script `!ps_script` writes can contain a password in clear.~~
     **FIXED AND VERIFIED 16 Aug 2026** on the 16:26 install: `PSTMP` exists,
     `don` unelevated is refused even reading its ACL, and — the useful part —
     **`adopt-account` succeeded during the install itself**, which is
     `!ps_script` going through the new directory before any test of mine ran.
     `assert-current` exit 0.
     What it was: And the disclosure
     was the lesser half: the account directory carries
     `sdusers:(OI)(CI)(M)`, inherited by every file, so another SD user could
     **rewrite a pending script between SD writing it and the elevated helper
     running it** — arbitrary content executed with full privilege, a local
     privilege escalation rather than a leak.
     **The fix:** scripts go in `@sdsys\PSTMP`, created by the installer
     through the new `gplbld/secure-psdir.ps1`. Directory ACL: `sdusers` gets
     list/create/traverse **on the container only, with no inheritance**, so it
     lands on no file; `CREATOR OWNER:(OI)(IO)(F)` gives each script to the
     session that wrote it; Administrators/SYSTEM keep `(OI)(CI)(F)` so the
     helper can read it. `DC` is withheld, so one user cannot delete another's
     file to take its name.
     **Semantics measured before building** — a file created there comes out
     `don:(I)(F)`, `Administrators:(I)(F)`, `SYSTEM:(I)(F)`, **`sdusers`
     absent**, and the creator can still read, write and delete it.
     **`!ps_script` fails closed** if `PSTMP` is missing rather than falling
     back. Checked that this cannot break the bootstrap: `bootstrap.py` only
     compiles and never reaches `!ps_script`. The installer's own
     `adopt-account` step does, but runs at `ssPostInstall`, after `[Run]`.
     **`PS_SCRIPT` got shorter, not longer** — `@sdsys` is already a Windows
     path (`sd.conf`: `SDSYS=C:\ProgramData\SD\sdsys`, `@ds` is `\`), so the
     `ospath`/`K$WINPATH` conversion is gone.
     **The description block that justified the old location was wrong and is
     corrected in place**: it argued the file was safe because the installer
     "grants narrowly", which is narrow against the world and not against SD's
     own users.
     **TO TEST:** install; `C:\ProgramData\SD\sdsys\PSTMP` should exist with
     that ACL; `CREATE.ACCOUNT` should still work end to end. A stronger check
     needs a second SD user attempting to read another's `$PS.TMP.<n>`
     mid-flight, which nothing automates today.

   - ~~The uninstaller left an empty PATH entry every cycle.~~ **FIXED AND
     VERIFIED 16 Aug 2026**, over a deliberate two-part cycle: **31 entries /
     24 empty → 6 / 0** when the fixed uninstaller ran, → **7 / 0** after the
     install. Every accumulated empty cleared in one pass, the six real entries
     intact and in order. Owner read the system PATH and found **23 empty
     entries in 30**. `RemoveFromPath` (`sd.iss`) keeps the separator *before*
     our directory and skips the one *after* it: correct for an entry in the
     middle, but Inno always **appends**, so ours is always last, the tail is
     empty and the kept separator dangles. The next install appends after it,
     so the run grows by one per cycle. Simulated against this machine's real
     PATH: old code leaves **30 entries, 24 empty**; fixed code leaves **6, 0
     empty**. The fix is a `while` loop rather than one strip, so **the next
     uninstall clears the whole accumulated run**, not just the slot it made —
     it can only ever delete separators, never an entry, which is what makes
     that safe on a PATH we do not own.
     **ISCC ALONE REBUILDS THIS** — `sd.iss` is not copied into
     `ProgramFiles` by `stage.py`, so no bootstrap is needed, unlike every
     other change today.
     **AN UNINSTALLER FIX CANNOT BE VERIFIED IN THE CYCLE THAT SHIPS IT, and
     that cost a cycle on 16 Aug 2026.** `unins000.exe` is generated AT INSTALL
     TIME by whichever installer runs, so the uninstall at the start of a cycle
     is performed by the PREVIOUS install's code. The fixed installer went on at
     16:31:23 and the PATH still grew by one, 30/23 → **31/24**, because the
     uninstall before it ran the old uninstaller. Nothing is wrong with the fix;
     it is one cycle out of phase, and the same applies to any future change to
     `RemoveFromPath`, `RemoveAllowGroups` or anything else at `usUninstall`.
     **HOW IT WAS VERIFIED, and the shape is reusable:** uninstall and install
     as SEPARATE steps, reading
     `HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment`
     in between. The intermediate state is the whole test and a single
     uninstall-then-install cycle hides it.
     **ALWAYS READ THE REGISTRY, NEVER `%PATH%`.** A shell open before an
     install keeps its own copy, and that appearance — "SD is not on PATH" —
     is what raised this in the first place. It happened twice on 16 Aug 2026.
     **And the report was half a false alarm worth remembering:** SD *was* on
     the PATH; the pasted value came from a shell opened before the install.
     Windows broadcasts the change and running processes keep their copy. Check
     the registry, not `$env:PATH`, when asked this.

   **Description of the feature follows.** 16 Aug 2026, thirteenth session,
   `ea052a4` and `6dadaa1`.

   **What it does.** `LOGTO SDSYS` obtains OS privilege for the session, with
   Windows asking the administrator to consent; leaving SDSYS gives it up.
   An ordinary command prompt is all that is needed. **There is no `ELEVATE`
   verb and there must not be** — owner's rule, 16 Aug 2026: *"there should
   never be an elevation from within a normal session"*. `CPROC`'s `LOGTO`
   handling is `!elevate`'s only caller.

   **Why it exists.** The installer dialog told administrators to open an
   ELEVATED command prompt. That was never the intent. The gate on
   `CREATE.ACCOUNT` (`CREATEA:90`) is **rev 0.9.0 and predates this port** —
   what was ours was making an elevated terminal the only way to satisfy it.
   Windows genuinely requires an elevated token to create a user, so the token
   is now obtained for the moment it is needed. A process's token is fixed at
   creation and nothing can elevate a running one, so `sd.exe` stays unelevated
   for life and an elevated **helper process** does the privileged work — a
   smaller exposure than an elevated terminal, where everything typed is
   privileged.

   **It cannot work over ssh, and that is the point.** UAC draws its consent
   dialog on the interactive desktop; an ssh session has none, so elevation
   fails and the `LOGTO` is refused. §5.6.2's rule is now enforced by Windows
   rather than by a test in SD that could drift. **A remote-control tool must
   be installed AS A SERVICE** or it cannot show the secure desktop and the
   operator sees a frozen screen — this is in the installer dialog.

   **The pieces:** `gplbld/sd-elevate.ps1` (`-Start`/`-Run`/`-Stop`),
   `gplbld/sd-elevate-helper.ps1` (elevated, hosts the pipe),
   `GPL.BP/ELEVATE` (`!elevate`), `CPROC` `int.logto`, and `!ps_script`, which
   is the chokepoint that routes a script to the helper. `!create_user` and
   `!os_group` were converted from `os.execute` to `!ps_script` for it;
   **`LISTMEM` deliberately was not** — it needs the script's output, which
   `ps_script` cannot return, and it is a read needing no privilege.

   **MEASURED ALREADY, so do not re-derive it:**

   - The mechanism end to end: one UAC prompt, a helper serving repeated
     requests, a local group created through the pipe by a session that had
     just been refused doing it directly, exit codes intact.
   - **The explicit pipe DACL is load-bearing.** Without it the pipe takes the
     elevated creator's default rights and the unelevated SD session is
     refused outright. The integrity label was a red herring.
   - `K$WINPATH` (58) and `K$WINPID` (59) exist because BASIC could reach
     neither fact: `OS$FULLPATH` returns a POSIX path whatever its comment
     says, and `getpid()` gives the MSYS2 number, not the one `Get-Process`
     uses (`sysseg.c`, `win_pid()`).
   - **THE BASIC COMPILES AND CATALOGUES.** The bootstrap of 13:38:41 ran to
     completion, and `bootstrap.py` dies on any compile error or "not assigned
     a value" warning. `GPL.BP.OUT` 192→193, `gcat` 131→132, `!ELEVATE`
     present in the catalogue.

   **THE BUILD LOOP, THREE TIMES THIS SESSION AND WORTH KNOWING.** No C
   changed, so **`make sd` is not needed** and skipping it keeps `bin/sd.exe`
   at `239BB9C3E43E4829` — relinking changes the hash for nothing (the
   `TimeDateStamp` note below). **`stage.py` has no incremental mode**: it
   refuses without `--force` and wipes with it (`stage.py:380`), so a one-line
   `.ps1` change costs the same full elevated bootstrap as a BASIC change.

   ```sh
   python3 gplbld/stage.py --stage /c/Users/dmont/stagetest --force --bootstrap
   ```
   ```powershell
   & 'C:\Program Files (x86)\Inno Setup 6\ISCC.exe' /DStage=C:\Users\dmont\stagetest /O"C:\Users\dmont\sdout" gplbld\sd.iss
   ```

   `--bootstrap` needs an **elevated** window and the **service stopped**
   (`stage.py:358`, and the staged `etc/fstab` points `/dev/shm` at the live
   tree). It is also the **first compile of the fix** — `bootstrap.py` dies on
   any compile error or "not assigned a value" warning, and `bbcmp.py` cannot
   check `CPROC` beforehand because it does not support `DEFFUN`. Then
   uninstall, delete BOTH trees, install, `assert-current`, retest as above.

2. **CLOSED AND VERIFIED — THE SERVICE SURVIVES A RESTART, INCLUDING ONE WITH
   A LEFTOVER SEGMENT.** 16 Aug 2026, thirteenth session, `sysseg.c`. The
   owner's requirement — *a production system with nobody logged in at the
   machine, available to every user from system startup* — **is met.**

   **The measurement, on the fresh install of 11:12:25** (`assert-current`
   exit 0, installed `sd.exe` `D2AAB6203CB80661`). A segment was left in
   `C:\ProgramData\SD\shm` deliberately, mtime **11:15:45**, no daemon, service
   stopped so nothing could tidy it. Boot **11:19:16**:

   - `sd -start` **exit 0**, `sdwind` up, service RUNNING (`sdsvc.log`).
   - **The segment in `shm` is stamped 11:19:25, not 11:15:45** — the survivor
     was discarded and a fresh one created. That mtime is the proof the new
     path ran, and it is what to check if this ever regresses.
   - Unelevated `don` → account `DON`, `WHO` → `1 DON`, `OFF` → exit 0.

   **The identical state produced exit 1 at the 10:31 boot before the fix**
   (twelfth session), which is what makes this a controlled result rather than
   a working system that might have worked anyway.

   **The fix.** `sd_state()` downgrades `SD_WRECKAGE` to `SD_STOPPED` and
   unlinks the segment when the segment's mtime predates boot —
   `segment_predates_boot()`, `boot_time()`, `sysseg.c`. Boot time is
   `time(NULL) - /proc/uptime`; **that arithmetic was checked against
   `Win32_OperatingSystem.LastBootUpTime` and agrees to the second.** Deliberate
   properties, all in the file's comments: it is asked **only after the daemon
   is known to be gone**, so a live segment is never tested and a clock
   corrected after boot cannot destroy one; it unlinks rather than only
   reporting, because `bind_sysseg()` would otherwise attach and answer "SD is
   already started" (`sysseg.c:132`); it is unreadable-`/proc/uptime`-safe, in
   that `boot_time()` answering 0 restores exactly the old behaviour.

   **Known limit, deliberate:** a pre-boot segment whose **revstamp does not
   match** is still not cleared — `sd_state()` reads no further on a mismatch,
   so only the existing "revstamp mismatch" message fires and `sd -stop` is
   still the way out. Reachable only by upgrading across an unclean stop.

   **Not an upstream defect.** `../sdb64` uses System V (`shmget`/`IPC_RMID`),
   whose segments vanish at reboot. No `UPSTREAM_FIXES.md` entry — do not
   re-check.

   **TO RE-RUN THIS TEST** (it is the regression test for the restart
   requirement, and there is no automated one): stop the service, `sd -start`
   from an elevated window, `Stop-Process -Name sdwind -Force`, confirm the
   segment is still in `shm`, reboot, then check the segment's mtime is the new
   boot time. **The service must be STOPPED while the fixture is built** —
   `sdsvc` watches the daemon and runs `sd -stop` when it dies (`sdsvc.log`,
   11:14:34), so killing `sdwind` under a running service tidies the segment
   away and the test passes for the wrong reason.

   **The stderr line (`Discarding the shared segment left by the previous
   boot`) was NOT observed** — it goes to `sdsvc-sd.log`, which captured
   nothing again. Its absence there means nothing; the mtime is the evidence.

   **Still open, none of it in the way of the restart requirement:**

   - **Why `shm_unlink()` fails at shutdown** (`sysseg.c`, the one `return
     FALSE` in `stop_sd()`). The fix above makes the leak harmless, **not
     absent**. **Narrowed on 16 Aug 2026: it is SHUTDOWN-specific, not
     stop-specific.** A plain `Stop-Service SD` on a running machine exited
     **0** and left `shm` empty (11:07:34), against exit **1** with the segment
     left behind during the 10:31 shutdown. So `sd -stop` is not simply broken:
     at shutdown it races the system tearing down processes, which fits the
     standing guess that `sdwind` still holds the mapping and Windows will not
     delete an open file without `FILE_SHARE_DELETE`. Still needs the errno.
   - **`sdsvc` already cleans up after a dead daemon, and that is why the leak
     is only ever seen at shutdown.** Kill `sdwind` under a running service and
     the wrapper notices, runs `sd -stop` and clears the segment
     (`sdsvc.log`, 11:14:34, `"sd -stop" exited with 0`). It cannot help when
     the machine itself is going down — which is exactly when it matters.
   - **`sdsvc-sd.log` captures nothing** — 0 bytes, three attempts, and it is
     the reason the twelfth session had to reconstruct a chain from exit codes
     and a directory mtime. Fixing it is the prerequisite for the errno above.
   - **The configured recovery actions never fire.** `sc qfailureflag SD` →
     `FAILURE_ACTIONS_ON_NONCRASH_FAILURES: FALSE`; `sdsvc.exe` exits reporting
     `SERVICE_STOPPED`, which Windows does not count as a crash, so the two
     restarts at `install-service.ps1:114` are dead config. Note both ways: had
     they fired they would have **masked** this bug rather than fixed it.

   **The `changelog` says SD runs as a service and recovers from an unclean
   shutdown. Both are now measured true.** Nothing has shipped yet.
2. **CLOSED 16 Aug 2026 — the login rule, `LIST.GRANTS` and `CREATE.ACCOUNT`
   are all verified on a fresh install** (§4). That was the whole of what the
   tenth session left written and unrun, bar the service.

3. **CLOSED — §7 step 1f, the installer's own account step.** Re-read on the
   10:23 install, twelfth session: `adopt-account.log` says `don now has an SD
   account` and `don keeps the Windows sign-in rights it already had`, and
   `ACCOUNTS/DON` is there. The earlier regression was the broken service
   poisoning the semaphores under it, and it went with the Win32 change.

4. **§7 STEP 4, THE AUDIT LOG, IS BUILT AND VERIFIED** on the fresh install of
   16 Aug 2026 12:18:42 — records observed for a login, a `LOGTO`, and a
   refused step-up, and every tampering route refused (§7 step 4). It took
   step 5f with it, so **§7 step 5 is complete apart from one untested path:
   `GRANT`/`REVOKE` has not been watched writing a record**, since it needs an
   elevated SD session and a second Windows user. The trail is **append-only
   to the users it records**, which is why `win32audit.c` is the second file
   allowed to include `windows.h`.

5. **SD IS INSTALLED, RUNNING, AND THE INSTALL IS CURRENT — THE CYCLE IS
   OPEN.** The install of **16:36:52** carries everything in item 1 and no
   source has changed since. **Seven full cycles were built on 16 Aug 2026**;
   `sd.exe` is `239BB9C3E43E4829` on every one, **no C changed all day**, so
   identify a build by `gcat/$CPROC` 25,208, `gcat/!OS_GROUP` 1,933, and the
   presence of `secure-psdir.ps1` and `sd-elevate.log`. **Five full cycles were built
   today** (13:52:43, 14:14:28, 14:21:50, 15:26:33, 16:02:58); `sd.exe` is
   `239BB9C3E43E4829` on every one of them, **no C having changed all day**, so
   identify a build by `gcat/$CPROC` 25,208, `gcat/!OS_GROUP` 1,933 and the
   presence of `C:\Program Files\SD\secure-log.ps1`. Identify it by `gcat/!OS_GROUP` 1,933 and `gcat/$CPROC`
   25,208 rather than by `sd.exe`, which is `239BB9C3E43E4829` on every install
   of this session — **no C changed all day**. Four full cycles were built
   (13:52:43, 14:14:28, 14:21:50, 15:26:33); each one surfaced or confirmed a
   different defect, which is the fresh-install rule earning its cost.

   Three installs were built this session (13:52:43, 14:14:28, 14:21:50), each
   from a full uninstall and both trees deleted. Two audit trails were copied
   out before being wiped: `C:\Users\dmont\audit-dump.txt` is the failed run,
   `audit-dump2.txt` the successful one. Both are quoted in item 1 and neither
   is needed again.

   Bootstrap sanity, four runs now: `PCODE.OUT` 56, `BP.OUT` and `cat` empty
   throughout; `gcat` and `GPL.BP.OUT` went 131/192 → **132/193** when
   `GPL.BP/ELEVATE` was added, which is the expected +1 and not drift.

   **A HASH DOES NOT IDENTIFY A BUILD, ONLY AN ARTEFACT — 16 Aug 2026,
   measured.** Two builds of identical source produce different `sd.exe`
   hashes: the PE header carries a `TimeDateStamp` set by the linker to the
   link time (read it back at offset `e_lfanew+8`; it was `12:13:44`, the
   link). Nothing embeds `__DATE__`/`__TIME__` — it is the linker.
   **Consequences:** `assert-current` is unaffected, because it compares the
   installed file against the `bin/` file it was copied from, and that is the
   same artefact. But **a hash quoted in this file identifies one build, and a
   later build of the same source will not match it.** Do not read such a
   mismatch as a source difference; it usually means somebody re-ran `make`.

   **The build sequence, since it was reconstructed from `sd.iss` this
   session** — MSYS2 is at `C:\msys64` and the Bash tool is Git Bash, which has
   no toolchain at all:

   ```sh
   cd sdb_ai/sd64 && make sd
   python3 gplbld/stage.py --stage /c/Users/dmont/stagetest --force --bootstrap
   ```
   ```powershell
   & 'C:\Program Files (x86)\Inno Setup 6\ISCC.exe' /DStage=C:\Users\dmont\stagetest /O"C:\Users\dmont\sdout" gplbld\sd.iss
   ```

   `--bootstrap` **needs an elevated window** (`stage.py:358`) and **needs the
   SD service stopped**: the staged `etc/fstab` points `/dev/shm` at the
   production `C:\ProgramData\SD\shm` (`stage.py:196`), so its opening
   `sd -stop` would otherwise tear down the running system. Package with `/O`
   so the installer lands outside the repository.

**Two things the owner has NOT decided, and nobody should decide for him:**
whether `SH` itself is restricted (the menu system is his answer instead — §6),
and that the ssh `ForceCommand` **kills scp and sftp on the machine**, which
follows from forcing the command and is stated in the `changelog`.

**Untested branch from step 1c:** `DELETE.ACCOUNT`'s "SD created it" delete.
**The test subject is `sdacct9`, made by `CREATE.ACCOUNT` on 16 Aug 2026 and
left in place for this** — `sdacct6` was the tenth session's and its SD side did
not survive the fresh install. It is SD's own, so `!is_sd_user`
answers yes and the prompting branch is the one that fires. Password
`Sd-Test-1`. For the other direction — an account SD did *not* make — use
`New-LocalUser sdadopt3 -NoPassword` and adopt it.

**Machine, ninth session, 15 Aug 2026.** **The install is clean and the machine
runs the repository** — counts and dates in header item 1, which is the one
place they live. **`don` has an SD account**, made by the installer's own step;
`sdusers` and `sdu_don` hold him, **`sdsshonly` is empty** — the adopt log says
`don keeps the Windows sign-in rights it already had`, so the lockout fix has
now held on two real installs. **No `sd*` Windows users exist**, but the groups
`sdu_sdacct4` and `sdu_sdadopt1` outlived theirs (machine table). **SD is not
running** and `C:\ProgramData\SD\shm` is empty, so `sd -start` starts cleanly —
**from an elevated window, which is new**: the gate now covers `-start`.
**`bin/` is current**, `make sd` clean, and the installed `sd.exe` hashes the
same. **No `gcat.bak` on the new tree**; the rollback is
`C:\Users\dmont\gcat.rollback` (129 entries, and it predates the corrected
catalogue — it restores a working system, not this one). UAC is at the default
(`ConsentPromptBehaviorAdmin` 5, `PromptOnSecureDesktop` 1): elevation raises a
secure-desktop prompt, **an AI session cannot self-elevate; ask**.

**`C:\ProgramData\SD\adopt-account.log`** is the installer's own account step
talking, and the first place to look if a future install produces no `DON`.

**A test naming `C:\Program Files` tests the installed binary**, which is only
current just after an install. That cost a round of the `EPERM` test.

**THE ACCESS MODEL, BUILT AND VERIFIED.** Full statement in §5.6; the short
form, because it changes what every other item in this file assumes:

- **SD login takes no password at all.** The operating system has already
  authenticated you. Typing `sd` puts you in **the SD account with your own
  name**, and nowhere else. **No linked SD account means no login.**
- **NOBODY LOGS IN TO ANY ACCOUNT BUT THEIR OWN — owner's rule, 15 Aug 2026,
  tenth session, and it REPLACES what stood here.** An administrator "has
  access to all accounts, once they have logged into SD, not before": entry is
  always your own account, and **`LOGTO` is what moves you**, which is where
  the grant is tested and where an elevated session gets everything (`CPROC`,
  `logto.authorised`). **`Administrators` is still the sudoers file**:
  `CREATE.ACCOUNT USER x` does not add to it, `... ADMINISTRATOR` does.

  **WHAT THIS REPLACED:** an elevated session went **straight into SDSYS** with
  no account named, and `sd -A<anyone>` admitted an administrator to any
  account at all, because the `ACC$GROUP` test was skipped when elevated. Both
  let somebody stand in an account without ever standing in their own. Built in
  `GPL.BP/LOGIN` 15 Aug 2026 — **NOT YET VERIFIED, §4 Not verified.**
  **`sd -ASDSYS` is refused now**, so anything driving SD as SDSYS sends
  `LOGTO SDSYS` after logging in; `verify-createaccount.ps1` was changed for it.
  **`-INTERNAL` is the exception and has to be** — it forces SDSYS and is the
  install and bootstrap door, and during a bootstrap there is no account for
  anyone to land in and nothing to `LOGTO` from.
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
- **NOTHING MAY BE TYPED AFTER `sd` WITHOUT ELEVATION** — owner's rule,
  15 Aug 2026. The switches and **a bare command both**: `sd LISTF` ran LISTF
  for anybody. `check_admin()` asks `IsElevated()` now, not `IsAdmin()`, and
  covers `-CLEANUP -D -L -M -U -SUSPEND -RESUME -INTERNAL` as well as the four
  it had. Plain `sd` is untouched. **`-P -C -N -Q` are deliberately NOT gated:
  SD spawns itself with them** for phantoms, the client library, network and
  the API, and those children carry an ordinary token. **The rule closes
  because of the two before it:** the console belongs to administrators, and
  an ssh session arrives *inside SD* rather than at a prompt.
- **EVERY ssh SESSION LANDS IN SD, ADMINISTRATORS INCLUDED** — owner's rule,
  15 Aug 2026. A global `ForceCommand` in `allow-ssh-groups.ps1`'s marked
  block, **not** the `DefaultShell` registry key, which `-Remove` could not
  reverse. ssh only: console, RDP and remote-control tools are untouched.
  **scp and sftp stop working**, which follows from forcing the command.
  **And SD refuses to start inside itself**: `op_sh.c` marks the shell `SH`
  launches with `SD_SESSION`, `sd.c` refuses when it sees it. A guard, not a
  boundary — the user owns that shell — and it is the accident it is for.
- **AN SD ACCOUNT HAS A SHELL ONLY IF ITS SESSION IS ELEVATED** — corrected
  twice, and this is the measured version (§4, 15 Aug 2026, ninth session).
  `SH` is gated at `GPL.BP/CPROC:3321` on `kernel(K$ADMINISTRATOR, -1)`, which
  is `IsElevated()`, so an ordinary SD user is refused with `sysmsg(2001)`.
  **An ssh session cannot be elevated, so `ForceCommand` does keep an ssh user
  inside SD.** The 15 Aug correction that said otherwise was reasoning from
  `SH` existing, not from running it. **Restricting `SH` further is still not
  decided** — but note it is already restricted, so the open question is
  narrower than it looks, and the owner's menu-system answer addresses the
  elevated console rather than ssh. Nobody should implement more without asking.
- **SD ACCOUNTS BRING THEIR OWN OS ACCOUNT, WITH ONE EXCEPTION** — owner's
  decision, 14 Aug 2026, seventh session. **The only pre-existing OS user that
  may be given an SD account is the installer's**, done at install time; every
  other SD account creates its OS account from within SD. `CREATE.ACCOUNT`
  refuses a name that already exists in Windows, and the sanctioned door is
  `ADOPT`, gated on `K$INTERNAL`, which the install uses. **The installer's
  account is made at install time from 15 Aug 2026** — §7 step 1f.
  **`K$INTERNAL` IS NOT A WALL AND IS NOT MEANT TO BE** (owner, 15 Aug 2026):
  an elevated administrator can run `sd -internal CREATE.ACCOUNT USER x ADOPT`
  by hand and give another administrator an account. That is accepted, and it
  **stays undocumented** — not in the `changelog`, not in the installer's
  dialog. What the gate stops is an ordinary console session adopting somebody's
  existing Windows login.

**Also true and worth having in one place:** `AllowGroups` was applied and
enforced on this machine, by control and treatment (§4), and the lockout risk
is closed by measurement. **§5.6.2 IS COMPLETE, RDP INCLUDED** — 15 Aug 2026,
tenth session, on a VirtualBox guest (§4). Nothing is left half-applied.

**STATE OF THIS MACHINE — READ FIRST. SD IS INSTALLED AND RUNNING, AND THE
INSTALL IS ONE BUILD STALE**, as of 17 Aug 2026: the tree is the whole and
working 22:57:00 install, and **§7 step 6a's source landed after it** —
`op_kernel.c`, `linuxio.c`, `keys.h`, `sd.h`, `sdnet.h`, `APISRVR`,
`INT$KEYS.H`. `bin/sd.exe` is already rebuilt and clean. **Stop the service
before staging with `--bootstrap`.**

| Thing | State |
|---|---|
| **The install** | **PRESENT, 16 Aug 2026 22:57:00**, sixteenth session, and **whole** — 3,477 files in the data tree, `gcat` 132, `GPL.BP.OUT` 193, `sd.exe` **`7A383F487235134B`** (the `CREATUSR` build). `assert-current` exit 0 and a session runs (§4). `C:\ProgramData\SD` is `uninsneveruninstall`, so **a fresh cycle deletes it by hand as well** |
| `C:\Program Files\SD` | binaries in `usr\bin`. 19 rather than 18 files because `adopt-account.ps1` ships beside the other three `.ps1` scripts. Count and date in header item 1 |
| `C:\ProgramData\SD\sdsys` | a working database built entirely from the repository: the installed `gcat/$LOGIN` carries the owner's banner and `gcat/$CREATEA` the lockout fix. Counts in header item 1; expect them to drift upward as accounts are created |
| SDSYS password | **not set, and it no longer matters** — nothing on the console asks for one. The password prompt is gone from the installed system too, as of the sixth session: the `Warning: account SDSYS has no password set` line no longer appears |
| **THE ACCESS MODEL IS LIVE** | sixth session, and tightened in the eighth by three owner rules (header). An unelevated `sd` refuses SDSYS with `sysmsg(10002)`; a bare `sd` lands you in your own account |
| **THE INSTALL IS NOT CURRENT** | It **was** — `assert-current` exit 0 on the 22:57:00 install of 16 Aug 2026, and everything in §4 dated that day was verified on it. Step 6a's source then landed, which is what ended that cycle, exactly as the rule says. Note editing `PROJECT_STATUS.md`/`HISTORY.md` does **not** end a cycle — the check looks at `gplsrc`, `sdsys` and `gplbld` only |
| `GPL.BP\LOGIN` vs the catalogue | in step at last - the banner reached the machine with the clean install, not by hand |
| Reinstalling over this | **DON'T** — the rule in the header. The installer **finds an existing database and leaves it alone**, saying so in a dialog, which is §6's staleness trap working as designed: a reinstall-over updates `C:\Program Files` and **not** `C:\ProgramData\SD\sdsys`, so the machine runs yesterday's BASIC on today's binaries. Copying `GPL.BP` across and recompiling by hand was the old workaround; a fresh install is the rule that replaced it |
| Rollback, if login ever breaks | **`gcat.before-step0` is GONE**, deleted in the sixth session once the refusals were verified — it held the *pre-change* catalogue, and going back to the password model stopped being something anyone would want. **The way back now is `C:\Users\dmont\gcat.rollback`**, a complete 129-entry catalogue bootstrapped from the same sources. It restores *today's* behaviour rather than yesterday's, which is the more useful direction. It was copied out of `C:\Users\dmont\stagetest` on 15 Aug 2026 because the next step is `stage.py --force`, which deletes that tree — **if you re-stage, the rollback lives outside the staging directory or it does not survive** |
| `sdusers` group | exists, with `GITORLI\don` in it |
| `sdadmins` group | exists, **created by hand on 13 Aug, not by the installer**, and nothing references it any more (§8). Leave it alone |
| System PATH and the Settings > Apps entry | both present |
| `C:\ProgramData\SD` ACL | locked to sdusers/Administrators/SYSTEM. An unelevated session **cannot read inside it** until `don` signs out and back in; `Test-Path` on the directory itself still says True, so look at the contents |
| MSYS2 dev tree at `/usr/local/sdsys` | still reachable with `SD_CONFIG=/etc/sd.conf`. Its `bin/` was refreshed with the `sdwind` build on 14 Aug 2026 and the stale `sdlnxd.exe` removed; `pcode`/`pcode.old` are still beside them, since the dev tree keeps the old unsplit layout |
| **The machine was rebooted** on 14 Aug 2026 | `don`'s token now carries `sdusers`, so **an ordinary unelevated session runs SD** — verified, §4. The sign-out trap in §6 is cleared *on this machine only*; it applies afresh to every new user added to the group |
| **OpenSSH Server** | **installed, `sshd` Running / Automatic**, listening on 22, firewall rule enabled |
| **`AllowGroups` AND `ForceCommand` ARE APPLIED - 17 Aug 2026, twentieth session** | Owner ran `allow-ssh-groups.ps1 -Installed` elevated and reported it working; the config was then read here: marker block present, `AllowGroups sdusers GITORLI\sdusers Administrators GITORLI\Administrators`, `ForceCommand "C:\Program Files\SD\usr\bin\sd.exe"`, `sshd_config.before-sd` kept, sshd Running. **It remains a manual step of every fresh install here** - the uninstaller removes it (`sd.iss`, `RemoveAllowGroups`) and `limitssh` is hidden where an ssh server already exists, so it must be re-run after every cycle. **The ssh login itself was tested by the owner, not observed here** - it needs a credential this session does not have |
| OpenSSH firewall rule | `Enabled True / Private / RemoteAddress Any`, unchanged across the install — `ssh-firewall.ps1` never runs here, the whole ssh step being hidden by `SshServerAbsent`. **Not a defect and not evidence about `sshremote`**, which is untestable on this machine (§7 step 3) |
| `sdsshonly` group | **exists now**, created 14 Aug 2026 by `verify-sshonly.ps1`, with both deny rights applied to it. So `CREATE.ACCOUNT` for a non-administrator will work here. It is left in place deliberately — it is what the installer would have created |
| Test accounts, Windows side | **`sdacct6`, `sdacct8`, `sdacct9` and `sdacct10` exist as Windows users** — `CREATE.ACCOUNT` refuses a name Windows already has, so **the next free one is `sdacct11`**. **`sdacct6`, `8`, `9`, `10`, `11`, `12` and `13` exist as Windows users**, each made by `CREATE.ACCOUNT` from an unelevated session and kept — password `Sd-Test-1`, in `sdusers`, their own `sdu_` group and `sdsshonly`, none an administrator. **Only `sdacct13` has an SD side**, the rest having gone with successive fresh installs. **The next free name is `sdacct14`.** `sdacct10`: 16 Aug 2026, made by `CREATE.ACCOUNT` and kept, password `Sd-Test-1`, in `sdusers`, `sdu_sdacct10` and `sdsshonly`, not an administrator, **but its SD side did not survive the 13:52:43 install**, so step 1c needs a fresh subject. **Two `sdu_` groups outlived their users**, `sdu_sdacct4` and `sdu_sdadopt1`: the eighth session's "every `sdu_` group but `sdu_don` was removed" is wrong. Harmless, left alone — but `DELETE.ACCOUNT`'s group cleanup is the thing to suspect if it matters later. `New-LocalUser sdadopt3 -NoPassword` for an adopt test |
| **`don` HAS AN SD ACCOUNT** | 16 Aug 2026, **made by the installer this time** — header item 3, §7 step 1f closed. `ACCOUNTS/DON` present and `adopt-account.log` says `don now has an SD account`. Its `don keeps the Windows sign-in rights it already had` line still appears, so the lockout fix holds |
| `sdsshonly` | exists, holding **`sdacct6`** and nothing else — the lockout fix means no administrator is in it, and `sdacct6` is there because that is what `CREATE.ACCOUNT` does to a non-administrator |
| Installed BASIC | the repository's, compiled by the bootstrap that built the stage - no hand-patching survives on this machine |
| Accounts, **SD side** | **`SDSYS` and `DON` only** — `DON` made by the installer's own step on the 22:57:00 install, `adopt-account.log` showing it through to `Adding to register of accounts`. Every `sdacctN` SD side went with the install, as always. **Windows side, `sdacct6, 8, 9, 10, 11, 12, 13` remain**, password `Sd-Test-1`. **`sdacct14` was created and then deleted whole** by §7 step 1c's test, so **it is free again and is the next name to use** |
| SD | **running.** The installer started it; service `Running`, `sdwind` up, one segment in `shm` stamped 13:52:49. **Stop the service before `stage.py --bootstrap`.** `sd -start` **needs an elevated window**: the gate covers `-start` |
| SD at boot | **THE SERVICE SURVIVES A RESTART, INCLUDING ONE WITH A LEFTOVER SEGMENT** — fixed and verified 16 Aug 2026, thirteenth session, header item 2. `sd -stop` still leaks the segment at shutdown; `sd_state()` now discards a pre-boot survivor, so the leak is harmless rather than absent |

Nothing needs cleaning off before the next piece of work. To start over anyway,
elevated: `C:\Program Files\SD\unins000.exe /VERYSILENT`, delete
`C:\Program Files\SD` and `C:\ProgramData\SD`, then `Remove-LocalGroup sdusers`
— but leave `sdadmins` alone, for the reason in §8.

**THE STAGED TREE AND THE INSTALLER ARE 16 Aug 2026, eleventh session, AND WERE
INSTALLED FROM.** `C:\Users\dmont\stagetest` re-staged at **07:49–07:55** and
`C:\Users\dmont\sdout\sd-setup-1.0-2.exe` built from it at **07:55**
(4,826,686 bytes). That installer was run and the result counted and hashed
(header item 5), so "it compiled" is not the claim — though on this occasion
"it compiled" was itself the problem: the previous installer had **not**, for a
whole session (§6, `sd.iss:560`).

ISCC alone is not enough when a `gplbld/` script changed —
`stage.py` copies those into `ProgramFiles` — and **`stage.py --bootstrap`
refuses an unelevated window**. Neither artefact survives a rebuild of the
machine; both are reproduced by the commands at the top of `gplbld/sd.iss`.

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

**THERE ARE THREE GENERATIONS, AND KNOWING WHICH ONE A LINE CAME FROM IS OFTEN
THE WHOLE ANSWER.** Stated by the repository owner, 15 Aug 2026:

1. **`sdb64`** — <https://codeberg.org/stringdatabase/sdb64>, the unmodified
   Linux version and the active upstream project. **Cloned locally at
   `../sdb64` since 15 Aug 2026**, with `main` checked out and `origin/dev`
   fetched, so both branches are readable without the network:
   `git -C ../sdb64 show origin/dev:sd64/<path>`. It is also a network
   resource, so a machine without the clone loses nothing but convenience.
   **Diffing against it is the cheapest way to attribute a surprise** — it is
   what settled §5.13 and §7 step 7.
2. **`sdb_ai`** — an experimental variant the owner produced by putting `sdb64`
   through **five AI cleaning and validation cycles**. This is why the code
   reads more cleanly than its age suggests, and why those cycles also
   introduce problems of their own.
3. **SD for Windows** — this repository, the port, built on top of `sdb_ai`.

**GENERATION 2 IS TAGGED IN THE SOURCE AND IS WORTH GREPPING FOR.** Every
change from the cleaning cycles carries a `Modified by Composer AI - 2026/06/10`
comment: **226 of them across 73 files** — 53 in `gplsrc`, 20 in `sdsys` —
measured 15 Aug 2026, all bearing that one date. **A line with that marker is
neither upstream nor port work**, so when something surprises you, grep for the
marker before treating it as intended and check the behaviour against `sdb64`.

**Two have already cost real time**: the `VALID_OS_PATH` trap in §6, and the
`SH` administrator gate at `GPL.BP/CPROC:3321` (§4, §7 step 7), which a session
mistook for a Ladybridge decision it would have been wrong to reverse. Several
other things this port has "found" turned out to be inherited from generation 1
rather than introduced — so the check runs both ways.

#### The generation-2 audit — BASIC side, done 15 Aug 2026

All 20 `sdsys` markers read against `sdb64`. **The whole validation layer is a
generation-2 invention**: `!valid_os_name`, `!valid_shell_cmd` and
`!valid_os_path` **do not exist upstream on either branch**, and neither do
their call sites. Three groups:

- **`!valid_os_name` — 8 call sites, and one of them is a live problem.**
  Charset is `A-Za-z0-9._-` only, length `MAX.USERNAME.LEN` = 32
  (`INT$KEYS.H:32`). **No backslash and no space**, so it rejects
  `DOMAIN\user` and any Windows name containing a space. Benign where the name
  is one SD is about to *create* (`CREATEA`, `CREATE_USER`, `SET_PASSWD` —
  refusing an awkward name is reasonable), **questionable where the name
  already exists**: `DELACC:240` and `MODIFYA:103/127` refuse to clean up or
  amend an account whose name it dislikes, which leaves litter nothing can
  address. **And `APISRVR:894` applies it to the API login name before
  authenticating** — §1 makes the API the product's front door and §7 step 6
  owns it. `SDCLIENT:249` does the same for remote logins. **NOT YET MEASURED:
  whether a real API login presents a domain-qualified name.** That measurement
  is what decides whether this is a defect or only a smell; make it before
  touching step 6.
- **`!valid_shell_cmd` rejects `;|&$` + backquote + `<>`**, so **even an
  elevated `SH` cannot pipe or redirect** — `SH dir | findstr x` is refused.
  This belongs with §7 step 7's decision: lifting the administrator gate alone
  would still leave shell-out unable to do the thing §5.13 wants it for.
- **The rest are benign or genuinely good.** Empty-input early returns in
  `IS_GROUP`, `IS_GRP_MEMBER`, `IS_USER`, `USERNAME`, `USERNO`, `ABSPATH`;
  fail-closed on empty password/salt in `SD_KEY_FROM_PW`; file-handle open-state
  tracking in `WRITE_INSTALL_DICTS`. **`LOGIN:172` is a cycle repairing itself**
  — it closes an unterminated banner string an earlier cycle left, which had
  caused `Unrecognised statement`.

#### The generation-2 audit — C side, 15 Aug 2026

**Method, stated because it bounds the claim: every marker was grouped by its
own stated intent, and then each group that can CHANGE BEHAVIOUR was read.**
Groups that cannot — analyser annotations, uninitialised-local fixes — were
classified from their comments and not read individually. So "audited" here
means *every behaviour-changing category*, not every one of the 206 lines.

**The C markers are a different animal from the BASIC ones and are mostly
GOOD.** 206 markers over 53 `gplsrc` files, static-analyser hardening rather
than policy. **Nothing here should be reverted wholesale**; the BASIC side's
verdict does not carry over.

| Category | n | Verdict |
|---|---|---|
| `noreturn` / fall-through annotations | ~24 | cosmetic, safe |
| uninitialised locals on switch-default paths | ~15 | genuine fixes |
| allocation guards ending in `k_error("Insufficient memory…")` | ~15 | **right answer** — loud, immediate, matches the codebase |
| `strtok`→`strtok_r` (`messages.c`, `netfiles.c`, `op_dio2.c`, `sdidx.c`) | 5 | correct — `savep` is function-scoped in every case |
| `message` pointed at a string literal (`messages.c`) | 3 | improvement, and dead code either way (`k_error()` longjmps above) |
| NULL-chunk guards in string padding (`op_str5.c`) | 3 | correct — implicit trailing spaces |
| abort an AK node split on `k_alloc` failure (`dh_ak.c`) | 3 | defensible: orphans a node on OOM vs upstream's NULL-deref mid-split |
| `timeout` read uninitialised (`op_seqio.c`) | 2 | genuine fix — `sq_file->timeout` is where it lives |
| free merge buffers on open failure (`op_sort.c`) | 1 | genuine leak fix |
| `w_addr < 0` always false on an unsigned | 1 | genuine bug fix |
| `groups` allocated every call, never freed | 1 | genuine leak fix |
| **`malloc(1)` → static buffer** | 2 | **DEFECT — fixed** |
| **cleanup gated on the ELSE indicator** | 1 | **DEFECT — fixed** |
| **trigger setup skipped on `k_alloc` failure** | 1 | **flagged, NOT fixed** |

**THE SECOND DEFECT IS THE SERIOUS ONE, AND IT WAS LIVE.** `op_seqio.c`'s
`op_openseq()` had `if (status)` where upstream has `if (process.status)`,
"because `process.status` may be cleared for `ER_RNF` before resources are
freed". It is cleared deliberately, and the two mean different things: `status`
goes on the e-stack as the **ELSE indicator**, while `process.status` is what
`STATUS()` returns — line 597's `ER_RNF; /* Transformed to zero later */` is
that transformation arriving. **So every `OPENSEQ` of a not-yet-existing file —
the normal way to create one — ran the failure cleanup on a successful open**:
`k_free(fvar)` while `fvar_descr->data.fvar` already pointed at it, plus
`k_free(sq_file)` and its pathname, and a decremented `ref_ct`. A use-after-free
handed straight to the BASIC programme, and **silent**, because `process.status`
was 0 by then so the `k_error()` at the foot of the block could not fire.
**Not OOM-gated like the others — this fired on ordinary use.** Reverted to
upstream's test; `make sd` clean.

**FLAGGED, NOT FIXED — `dh_open.c:257`.** On `k_alloc` failure for the trigger
name it silently opens the file **without its trigger**: `DHF_TRIGGER` never
set, so writes bypass the trigger's validation. Same loud-to-silent trade as
the `malloc(1)` defect, but OOM-only, and the right remedy — `k_error()` like
the ~15 other allocation sites, or failing the open — changes open-failure
semantics. **Decide it deliberately rather than in passing.** (The guard also
contains a dead `if (p == NULL) { p = NULL; }`.)

**The pattern to carry forward:** generation 2's failure mode is **turning a
loud failure into a quiet one**, and once — in `op_openseq` — turning a success
into a silent corruption. When a marker adds a guard, the question is never
"is the guard right" but **"what does it do instead, and who can tell?"**

**ONE REAL DEFECT, FOUND AND FIXED.** `ctype.c`'s `CNullString()` and
`op_sdext.c`'s `NullString()` both guarded their `malloc(1)` and returned a
**`static char empty[1]`** on failure. Their results are **owned and freed by
the caller** — `op_sdext.c:258` frees every non-NULL entry of `SDMEArgArray`
in a loop, and both functions feed it (`NullString()` at line 170, and
`Extract()`→`CNullString()` at line 184). So an out-of-memory produced
`free()` of static storage: **heap corruption discovered somewhere else
entirely, in place of upstream's immediate NULL dereference.** Strictly worse,
and on the credential path — line 227 hands that array to `sd_KeyFromPW()`.
**Fixed by returning NULL**, which the release loop already tests for.
`make sd` clean afterwards. **Only reachable when a 1-byte `malloc` fails, so
it is latent rather than live** — but it is the shape to look for elsewhere: a
cleaning-cycle guard that changes who owns a pointer.

**WORTH SENDING UPSTREAM.** This is the one case where generation 2 found a
genuine flaw: `sdb64` has `p = malloc(1); *p = '\0';` with no check at all, so
upstream NULL-dereferences on the same out-of-memory. The fix committed here is
better than both and applies to `sdb64` unchanged. **Written up in
[UPSTREAM_FIXES.md](UPSTREAM_FIXES.md), which is maintained from now on** —
CLAUDE.md carries the rule.

#### What `sdb64`'s dev branch has that we want — reviewed 15 Aug 2026

13 commits, 14 files, `main..origin/dev`, heading for 1.0-3.

**TAKEN.** **`ER_SRVRERR 4100`, `ER_INV_NBR 4101`** into `gplsrc/err.h`,
`gplsrc/sdclilib/err.h` and `sdsys/SYSCOM/ERR.H` — purely additive, no conflict.
Clean rebuild after `rm -f gplobj/*.o`, no warnings.

**FOUND AND DELIBERATELY LEFT ALONE: `SV_EMSG_PAIR` AND `SV_ECONTXT` ARE
TRANSPOSED BETWEEN THE TWO PROJECTS.** `sdb64` dev has `EMSG_PAIR=6,
ECONTXT=7`; the vendored `winsdclilib` client here has them the other way
round. A caller compiled against one header talking to a library built from the
other reads each state as the other one.

**This session renumbered ours to match upstream and then reverted it**, on
learning the client library's provenance (§5.3 below): `sdb64` did not
originate this file. **Which numbering is right cannot be determined from this
repository** and is written up in [UPSTREAM_FIXES.md](UPSTREAM_FIXES.md) #2
with what would settle it. Until then the vendored copy keeps `winsdclilib`'s
values, because a vendored copy stays faithful to its source, and
**`sdsys/SYSCOM/sdclilib.h` deliberately defines NEITHER**, so no BASIC commits
to a numbering by accident. The cost is that our BASIC cannot yet tell a
transport failure from a context error.

**Incidental but useful: these constants are duplicated in FOUR files** —
`gplsrc/sdclilib/sdclient.h`, `sdclilib.h`, `sdclilib.bi`, and
`sdsys/SYSCOM/sdclilib.h`. Changing two of four is what surfaced the conflict,
as a redefinition warning. **`grep -rn "define SV_"` before touching them.**

**ALREADY HERE, INDEPENDENTLY.** Dev's `GetResponse()` fix — return TRUE after
re-fetching the error text rather than reporting a server-side error as a
transport failure — **is already in our stage-2 client**, with a fuller comment
and a better fallback path. Nothing to take. Worth knowing the two trees agreed.

**NOT APPLICABLE.** `_XOPEN_SOURCE` Fedora 44 warnings (Linux); `op_sdpyobj.c`
and `sdext_py.c` (embedded Python, dropped — §5.15); `SDConnectUDS` syslog
(Unix domain sockets).

**CORROBORATION FOR §7 STEP 6d, AND IT IS WORTH HAVING.** Dev comments out the
`getpwnam`/`setgid`/`setuid` block in `SDConnectLocal` — independently reaching
the conclusion step 6d already holds, that these calls make no sense when the
local connection is forked from a running SD. **Upstream also gives a reason we
did not have: it breaks an Apache-spawned process** while working from a test C
program. Our client has no such block, so nothing to do, but step 6d is now
backed by somebody else's field experience.

**OWNER'S CALL, NOT TAKEN.** Dev bumps to **1.0-3** (`revstamp.h`, `$RELEASE`,
`sddefs.h`, `sdclient.h`); we are 1.0-2, and release identity is not something
to change by inference. **`APISRVR` is 2,147 changed lines**, mostly
reformatting with real error checking inside it; ours has already diverged and
§7 step 6 owns it — revisit when step 6 is done, not before, or the reformat
will bury the port's own changes.

**The TCL verb surface is written down**, in
[docs/TCL_VERBS.md](docs/TCL_VERBS.md) — SD's commands against OpenQM 2.6.6,
supplied by the repository owner 14 Aug 2026. Read it before adding or renaming
a verb. The important structural fact it records: **SD has accounts, not
accounts and users.** `CREATE.USER`, `DELETE.USER`, `ADMIN.USER` and
`LIST.USERS` are all deliberately absent, which is why `CREATE.ACCOUNT`
provisions the operating system account itself and why the `CREATUSR` gate was
removed (§7 step 1a).

### The sibling repositories, and what "in sync" means

**Four repositories are in play, all cloned beside this one as of
15 Aug 2026**, and three of them are **maintained**, not merely consulted:

| Path | What it is | Our duty |
|---|---|---|
| `../sdb64` | upstream Linux project, `main` + `origin/dev` | **read-only.** Fixes it needs go in [UPSTREAM_FIXES.md](UPSTREAM_FIXES.md) |
| `../winsdclilib` | the Windows client library, vendored into `gplsrc/sdclilib/` (§5.3) | **maintain.** Holds the client documentation and is to be the basis of an eventual **SD for Windows client installer** |
| `../linuxsdclilib` | the Linux client library, imported 5 Aug 2026 | **keep in sync** with the above where the code is shared |
| this repository | the port | — |

**THE SAME CONSTANT LIVES IN A DOZEN PLACES ACROSS THESE FOUR TREES.** That is
not hypothetical — it is how the `SV_EMSG_PAIR`/`SV_ECONTXT` transposition
survived from 5 to 15 Aug 2026 in three repositories at once. **Before changing
any shared constant, grep all four**:

```sh
grep -rn "define SV_" ../sdb64 ../winsdclilib ../linuxsdclilib . --include=*.h --include=*.bi --include=*.c
```

`sdb64` is the authority for anything it defines first; the client repositories
are the authority for the Windows/Linux transport code they own. **Neither is
simply "upstream" for `gplsrc/sdclilib/`** — see §5.3's round trip.

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

**`ApplyDenyLogon` WORKS — VERIFIED 17 Aug 2026, elevated, on the 20:34:04
install.** `sd.iss` `[Run]` entry → `[Code]`, exit code checked. The rights
read back from `secedit /export /areas USER_RIGHTS`:

```
SeDenyInteractiveLogonRight       = *S-1-...-1016,sdsshonly,Guest   PRESENT
SeDenyRemoteInteractiveLogonRight = *S-1-...-1016,sdsshonly         PRESENT
SeDenyNetworkLogonRight           = Guest                           ABSENT
```

**All three rows are wanted, and the third is wanted ABSENT** — setting it
would deny the network logon Win32-OpenSSH authenticates with and break ssh
outright, which is the one thing §5.6.2 exists to preserve.

**The first reading of this said all three were absent, and that was the
CHECK being wrong, not the machine.** See the `deny-logon.ps1` caveat above:
by-name not by-SID, and UTF-16LE. Both were already documented and a
hand-rolled check hit both anyway.

**17 Aug 2026 - `OS.USERS` REFUSES AN UNLISTED ACCOUNT, twentieth session.** On
the 22:43:52 install, unelevated, `SH dir` piped into `sd.exe` as `don`:

```
don is not permitted to use the operating system shell
```

That is the new message 10053 with `@logname` substituted, from `CPROC`'s
rewritten `os.command` gate. **The ACL is verified with it and separately**:
`icacls` shows `sdusers:(OI)(CI)(RX)` with no inherited entries, a write into
`OS.USERS` raises `UnauthorizedAccessException`, and a read succeeds - which is
the exact split `CPROC` needs, since it reads the list in the user's own
process. `secure-osusers.ps1` worked on its first install.

**18 Aug 2026 - THE ADMIT PATH RUNS. `gplbld/verify-osusers.ps1`, 18 of 18
checks, 13 of them decisive, exit 0 on the 07:00:00 install**, twenty-first
session. The whole of §7 step 7 is now observed rather than argued:

| | plain `SH` | `SH` with a pipe |
|---|---|---|
| unelevated, unlisted | refused 10053 | refused 10053 |
| **elevated**, unlisted | ran | refused **5240** |
| unelevated, **listed** | **ran** | **ran** |
| unelevated, unlisted again | refused 10053 | — |

**What each row is for.** Row 3 is the reading nobody had ever taken. Row 4 is
what stops it being read into an install that admits everybody — the shell goes
away again when the record does. Row 2 is the "regresses nothing" claim, and
its two cells carry **different messages**: 5240 is `!valid_shell_cmd` refusing
the pipe, 10053 is the gate refusing the person, so the ban is intact for an
elevated session that is not listed.

**What was scored is a marker FILE each probe creates**, not the message — SD
echoes the command back, so a message can be present without the command having
run. `@LOGNAME` is **`don`, lower case**, and the record is keyed by it.
Unelevated `OPENPATH` of a file that is (RX) to `sdusers` **succeeds**, which is
what makes the design work at all. Transcript in `%LOCALAPPDATA%\SD-verify`;
`OS.USERS` was empty again afterwards, checked directly.

**17 Aug 2026 — CASE INSENSITIVE QUERIES AGAINST A DIRECTORY FILE WORK, and
this is the BEHAVIOUR rather than the flag.** On the 20:34:04 install,
`verify-nocase.ps1` exit 0 with `SYSTEM(91)` answering 1, and then by hand,
treatment and control in one session:

```
SELECT BP  WITH @ID = "sue"   directory file, record is SUE  ->  1 record(s)
SELECT VOC WITH @ID = "who"   dynamic file,   record is WHO  ->  0 record(s)
```

**THE CONTROL IS THE DYNAMIC FILE AND IT IS WHY THIS MEANS ANYTHING** — a
directory file matching across case proves nothing if everything matches. `VOC`
is dynamic with `NOCASE` off and stays case sensitive, so `"who"` finds nothing
while `"sue"` finds `SUE`.

**This is `QPROC:499` running for the first time.** It is gated on
`SYSTEM(91)`, which answered 0 on Windows until this session.

**17 Aug 2026 — DIRECTORY FILES OPEN `DHF_NOCASE`, twentieth session.** On the
20:10:31 install, `gplbld/verify-nocase.ps1` unelevated as SD account `DON`,
exit 0, `assert-current` clean:

```
directory file (BP) reports FL$NOCASE   expected 1   observed 1   PASS
dynamic file (VOC) reports FL$NOCASE    expected 0   observed 0   PASS
```

**BOTH ROWS ARE DECISIVE AND THE SECOND IS WHY THE FIRST MEANS ANYTHING.** Both
read 0 before the change (17:36:21 install), so the directory file moved and
the dynamic file did not — the flag is being read rather than invented, and
`dh_open.c:549` still takes a dynamic file's flags from its own header.

**This is the flag being SET, not the lock collision.** `op_lock.c` has honoured
`DHF_NOCASE` since long before the port; what this port changed is whether a
directory file gets it. A two-session `READU` test would exercise `op_lock.c`,
which is not what changed.

**17 Aug 2026 — `$CRED` IS CLOSED TO ORDINARY USERS, twentieth session.** On the
17:36:21 install, `gplbld/verify-credacl.ps1` unelevated as `GITORLI\don`, exit
0, `assert-current` clean. **The decisive measurement is a write, not a
listing**: `[System.IO.File]::Open(...CreateNew)` on a record inside
`C:\ProgramData\SD\sdsys\$CRED` raises `UnauthorizedAccessException`, and
`icacls` on the same path answers **Access is denied** where the 17:08:32
install printed `GITORLI\sdusers:(I)(OI)(CI)(M)`.

**A listing alone would not have been evidence** — inherited entries, deny ACEs,
group nesting and token filtering all change what one means — which is why the
script asks the filesystem the question an attacker would ask. **And it must be
run UNELEVATED**: the ACL grants `Administrators` Full, so an elevated run
passes however broken the ACL is. The script refuses to run elevated.

**16 Aug 2026 — §7 STEP 1c IS CLOSED: `DELETE.ACCOUNT`'s "SD CREATED IT" BRANCH
HAS RUN, sixteenth session.** `sdacct14` made by `verify-createaccount.ps1
-Keep` from an **unelevated** session at 23:34 — and it **authenticated over
ssh and ran `whoami`**, answering `gitorli\sdacct14`, so the account was real
and carried a password SD set. Fifteen seconds later `DELETE.ACCOUNT sdacct14`
from an unelevated session that had entered SDSYS removed **all four halves**:
Windows user, `sdu_sdacct14`, the account directory, and the `ACCOUNTS` record.

**Which branch fired is established by state, not by reading the message.**
`DELACC`'s three cases are distinguishable by what they leave behind, and only
`case sd.made.it` (`sysmsg(10028)`) deletes the Windows user — 10036 leaves it
and 10037 means it never existed. It existed, and it is gone. Corroborated by
the directory mtimes, which land in DELACC's own order: `user_accounts`
23:34:29, `PSTMP` 23:34:31 (the privileged half going through `!ps_script`),
**`ACCOUNTS` last at 23:34:32**, which is the deliberate ordering that leaves a
failed run re-runnable. **The `10028` line itself was not read by this
session** — it went to the operator's screen.

**16 Aug 2026 — THE LOGIN RULE AND THE COMMAND-LINE GATE, 6 of 6 WITH THE
CONTROL, on the fresh install, sixteenth session.** Unelevated: bare `sd` →
`8 DON` and `sd -ADON` → `9 DON` admitted; `sd -ASDSYS` refused `You can only
log in to your own account - use LOGTO to reach another`; `sd LISTF` and
`sd -start` refused `This command needs an elevated session`, **exit 1**; and
`sd --version` **exit 0**, the control without which a gate that refuses
everything would look correct.

**16 Aug 2026 — `CONFIG` NO LONGER LISTS `CREATUSR`.** 56 lines, running
`CMDSTACK` → `DEADLOCK` straight past where it sat. The user-visible half of
§7 step 1a; the compiled-object check is separate, below.

**16 Aug 2026 — THE INSTALL IS WHOLE AND A SESSION RUNS ON IT, sixteenth
session.** On the install of **22:57:00**, `assert-current` exit 0, `sd.exe`
`7A383F487235134B`: `gcat` **132**, `GPL.BP.OUT` **193**, `gcat/$CPROC`
**25,208**, `$LOGIN` 5,615, `$QPROC` 54,073, `VOC` present, 3,477 files,
`ACCOUNTS/DON` present. Then the part the previous install could not do at all:
an **unelevated** `sd` answered `WHO` → **`2 DON`** and `OFF` → exit 0.
**Both halves matter** — the counts say the bootstrap finished, the session
says the tree works, and the 17:51:35 install passed nothing but a file copy.

**16 Aug 2026 — `CREATUSR` IS GONE FROM THE COMPILED CATALOGUE, not just from
the source.** Installed `gcat/$CONFIG` is 3,153 bytes and does **not** contain
the string `CREATUSR`, while it does contain `DEADLOCK` — the control, without
which the search proves nothing.

**16 Aug 2026 — THE LOGIN RULE, 5 of 5, eleventh session, on the fresh
install.** Written 15 Aug and never run until now. `sd -internal` → `12 SDSYS`,
so the bootstrap and install door still reaches SDSYS — the one to check before
anything else, because nothing can be installed without it. A bare elevated
`sd` → `13 DON`. `LOGTO SDSYS` from there → **`14 SDSYS from DON`**, which names
where it came from and is the decisive form. `sd -ASDSYS` → **`You can only log
in to your own account - use LOGTO to reach another`**, sysmsg(10051), and it did
not reach SDSYS.

**16 Aug 2026 — `LIST.GRANTS` ON A FRESH INSTALL, eleventh session.** The CR fix
had only ever been seen on a hand-recompiled `OS_GROUP`. `LIST.GRANTS SDACCT9`
with two members printed `'   don'` and `'   sdacct9'` **adjacent, neither
carrying a CR and no blank line between them**, read back with control
characters made visible rather than by eye. `GRANT`/`REVOKE` round-tripped
against `Get-LocalGroupMember` both ways, each printing the sign-out line.

**16 Aug 2026 — `CREATE.ACCOUNT`, 16 of 16 on a fresh install, eleventh
session.** `verify-createaccount.ps1 -Account sdacct9` exit 0: both halves of
what it makes, the ssh-only branch, and all three logon measurements —
`LogonUser` INTERACTIVE **refused 1385**, NETWORK_CLEARTEXT **admitted**, ssh
**admitted**. `sdacct9` is left in place, password `Sd-Test-1`.

**16 Aug 2026 — THE UNINSTALLER REMOVES THE SERVICE, test (e), eleventh
session.** Service gone (`sc query SD` → 1060), `C:\Program Files\SD` gone, and
**`C:\ProgramData\SD` kept, 3,486 files** — which is the other half of the test:
the user's database is `uninsneveruninstall` and must survive.

**16 Aug 2026 — NO REGRESSION FROM THE Win32 SEMAPHORES, eleventh session.**
The IPC change rewrote the layer every SD session depends on, so the morning's
tests were re-run against it on the same install: **11 of 11** on the login
rule, `GRANT`/`REVOKE` and `LIST.GRANTS` (still no CR, still no blank line),
and **16 of 16** on `CREATE.ACCOUNT` for `sdacct10`, ssh-only branch and all
three logon measurements included.

**16 Aug 2026 — THE SERVICE WORKS, AND AN ORDINARY USER REACHES IT, eleventh
session, on a fresh install.** The whole chain, one install: the service
`Running`, `sdwind` **alive at t+30s** — past the ten-second mark that had
killed it every previous time — all six `Global\sd_sem_716d0302_*` openable,
and `adopt-account.log` reading **`don now has an SD account`** with
`ACCOUNTS/DON` present, which closes §7 step 1f.

**Then the half that had never been tested, and it is the one the requirement
rests on.** From an **unelevated** session-1 process (`GITORLI\don`, elevated
`False`, session `1`): all six semaphores opened, and a bare `sd` answered
**`2 DON`** — an ordinary user logged in to an SD started by a LocalSystem
service in session 0, with nobody having typed anything. **The restart has now
been measured and it fails — see the entry below; this one still stands for
everything short of a reboot.**

**16 Aug 2026 — THE SERVICE DOES NOT SURVIVE A RESTART, AND WHY, twelfth
session, on the same install.** Machine rebooted 10:31:21; `Get-Service SD`
`Stopped`/Automatic, no `sdwind`, SCM event 7024. From
`C:\ProgramData\SD\sdsvc.log`: shutdown 10:31:05 `sd -stop` **exit 1**, boot
10:31:30 `sd -start` **exit 1 one second later**, then the service's own
recovery `sd -stop` **exit 0** at 10:31:41.

**The segment survived the reboot, and the decisive measurement is a directory
mtime.** `C:\ProgramData\SD\shm` has LastWriteTime **10:31:41.396** — the
recovery `sd -stop`. A directory mtime moves only when an entry is added or
removed; nothing was added, because `sd -start` exited one second in, before
`bind_sysseg()`, which unlinks after itself on failure (`sysseg.c:332`,
`:343`). So an entry was **removed at 10:31:41**, and was therefore present at
boot. One second also excludes both ten-second waits — the daemon poll and
`sem_open`.

The rest is single-code-path rather than observed, because `sdsvc-sd.log`
captured nothing: `sd -stop` exit 1 can only be `shm_unlink()` failing with
errno ≠ ENOENT (`sysseg.c:785`, the one `return FALSE` in `stop_sd()`), and a
one-second `sd -start` failure over a present segment with no daemon is
`SD_WRECKAGE` (`sysseg.c:506`). Header item 1 has the fix options; §6 has the
trap.

**16 Aug 2026 — §7 STEP 1f, BY THE INSTALLER RATHER THAN BY HAND, twelfth
session.** `adopt-account.log` on the 10:23 install reads `don now has an SD
account` and `don keeps the Windows sign-in rights it already had`, and
`ACCOUNTS/DON` exists. Read off the installed tree, not re-run.

**16 Aug 2026 — SD WILL NOT RUN UNDER LocalSystem IN SESSION 0 ON POSIX
SEMAPHORES, test (a), eleventh session. Fixed by the entry above; kept because
it is why the Win32 change exists.** Header item 1 carries the reasoning and what is left to
decide. The measurements: `sdwind` dies at **~10s** started by the service and
**~10s** started by a scheduled task as SYSTEM with no service anywhere, and is
**alive at 40s** started from an interactive elevated session — one install,
one sitting. It dies saying **`sdwind: Error 116 getting semaphores`**, errno
116 = `ETIMEDOUT`, because the probe `sem_open` at `sdsem.c:82` **blocks about
ten seconds and times out**. Both processes in that probe were SYSTEM in
session 0, so it is **not** a cross-session problem.

**16 Aug 2026 — AND THE SERVICE NO LONGER LIES OR LEAVES WRECKAGE, eleventh
session.** Same install. It reports `STOPPED` with `sdwind.exe has GONE after 5
seconds` rather than `Running` over a dead SD, and `sd -stop` behind the failed
start leaves **`shm` empty** — after which `adopt-account` reports the honest
`SD has not been started` instead of `Error 116 getting semaphores`. Before
this, a failed service left every later `sd` on the machine broken.

**15 Aug 2026 — §7 STEP 5: GRANT, REVOKE AND LIST.GRANTS WORK, 16 of 16 on a
fresh install, tenth session.** Every SD-side claim checked against
`Get-LocalGroupMember` afterwards, because the point of the step is that SD
writes nothing to its own record: `GRANT SDACCT8 TO don` → `don may now use
account SDACCT8` **and don in `sdu_sdacct8`**; `REVOKE` → out of it again.
Both print the sign-out line (5c). The idempotent paths say so rather than
implying they acted — a second `GRANT` answers `already a member`, a second
`REVOKE` answers `has not been granted`. Refusals: unknown account →
`Account not registered in ACCOUNTS file`; unknown user → `There is no Windows
account named nosuchuser`, **and it did not add them**. **`LIST ACCOUNTS`
still works** with the `Granted to` column gone, which is what 5d's ordering
was for.

**Two defects found by running it that compiling could not have shown.**
`LIST.GRANTS` printed a blank line after every member: PowerShell ends lines
CRLF, the capture splits on the LF, and `trim()` removes spaces but **not the
carriage return**. It reads as untidiness and is not — a name carrying a CR
fails `!valid_os_name`, so `OS_GROUP`'s own promise that a `LISTMEM` name can
go straight back to `DELMEM` was false. Fixed by `convert char(13):char(10)`
before the trim, **verified on a hand-recompiled `OS_GROUP` rather than a
fresh install** — re-check it on the next one, it is one command.

**And the installer failed to give the installing user an account**, reporting
`code 3` — the `adopt-account.ps1` race now in §6. It had never fired before
because the machine had never been loaded enough to lose it.

**15 Aug 2026 — §7 STEP 2 RAN ON A SECOND MACHINE, tenth session. THE INSTALL
IS SELF-CONTAINED AND THE RDP REFUSAL IS MEASURED.** VirtualBox guest
`VIRTUAL`, Windows 11 Pro, bridged at 10.0.0.143, from snapshot `Before SD
install`. **No MSYS2, no `gplsrc`, no development tree** — which is the whole
reason the step existed, because an accidental dependency on any of them can
only show up here.

**The install is byte-identical to the build machine's**: `sd.exe` sha256
`81594E79CC2B560C`, and **19 / 3,456 / `gcat` 130 / `GPL.BP.OUT` 191** — the
same four counts. `sd -start` exit 0, `sdwind` up, and **`COUNT VOC` answered
`431 record(s) counted`**, which is the number that says the database is whole
rather than merely present. `adopt-account.log` shows the installer's account
step ran there too: `don now has an SD account`, `don keeps the Windows sign-in
rights it already had` — the lockout fix on a machine that never had the bug.

**RDP, control then treatment, which is the half one machine cannot do.**
`CREATE.ACCOUNT USER sdacct7` on the guest put it in `sdusers`, `sdu_sdacct7`
and `sdsshonly`, not `Administrators`, saying `sdacct7 may sign in over ssh
only`. Then from the host, same target, same port, same firewall rules,
differing only by `sdsshonly` membership:

- **control — `VIRTUAL\don` → ADMITTED.** Without it a refusal is
  indistinguishable from RDP being off, which is not hypothetical: three
  earlier attempts failed for rig reasons alone.
- **treatment — `VIRTUAL\sdacct7` → REFUSED, `The connection was denied because
  the user account is not authorized for remote login`.** That wording is
  `SeDenyRemoteInteractiveLogonRight` specifically, **not** a credentials
  failure, which is the distinction that makes it evidence.

`LogonUser` locally on the guest agreed on the two types it can test —
INTERACTIVE **refused 1385**, NETWORK_CLEARTEXT **admitted**. **It cannot test
the RDP path at all**: there is no logon type 10 for `LogonUser`
(`RemoteInteractive` is an LSA audit value), and asking for one returns
`87 ERROR_INVALID_PARAMETER`. A tenth-session probe row claimed otherwise and
was wrong. **So RDP genuinely required the second machine** — the step was right
to insist.

**15 Aug 2026 — AN ssh SESSION LANDS INSIDE SD (header 2b), tenth session.**
`ssh sdacct6@localhost whoami` against the fresh install answered **SD's banner
and a `:` prompt, exit 0 — `whoami` never ran**. That is the decisive form:
sshd discards the client's command and runs SD. `verify-createaccount.ps1`
deliberately accepts *either* proof of admission, because it must run either
side of `allow-ssh-groups.ps1`, so it cannot make this measurement — it was made
separately. `CREATE.ACCOUNT USER sdacct6` was **16 of 16** on the way past,
including the ssh-only branch and the three logon measurements: `LogonUser`
INTERACTIVE **refused 1385**, NETWORK_CLEARTEXT **admitted**, ssh **admitted**.

**And scp is dead, measured rather than asserted.** `scp` to that account
**exit 255**, `Received message too long` / `Ensure the remote shell produces no
output for non-interactive sessions` — which is what forcing a command that
prints a banner does. The `changelog` already said so; now it is observed.

**15 Aug 2026 — `SH` SETS `SD_SESSION` AND `sd` REFUSES IN THE SHELL IT HANDS
BACK (header 2c), tenth session.** Elevated live session on the install:
`SH Get-ChildItem Env:SD_SESSION` printed **`SD_SESSION 1`**, so `op_sh.c:312`
is observed and not just `sd.c`'s half. The refusal was then watched on **both**
child paths — `OS.EXECUTE 'sd --version' CAPTURING` (`sh(TRUE)`) and
`OS.EXECUTE 'sd --version'` with no CAPTURING (**`sh(FALSE)`, the identical path
the `SH` verb takes**) — each answering `SD is already running in this session -
type EXIT to return to it.`

**Why it took three runs, and it is a testing trap not a defect:**
`SH sd --version` in the piped elevated session produced **no output at all**.
The refusal is `fprintf(stderr, ...)` at `sd.c:301`, and the capture took only
stdout. `Get-Command sd` inside the same child resolved to
`C:\Program Files\SD\usr\bin\sd.exe`, so it was never a PATH failure.
**`CAPTURING` sees it because `op_sh.c:281-282` dup2s the pipe onto BOTH 1 and
2**; a bare `2>` on the `sd` invocation does the same for the uncaptured form.

**15 Aug 2026 — AN ORDINARY USER'S PROGRAM REACHES THE OS, IN THE SAME SESSION
WHERE `SH` IS REFUSED. Owner's question, tenth session.** One **unelevated**
session on the install, with the control first: `SH echo ...` at the `:` prompt
→ **`Command requires administrator privileges`**; then a program compiled `0
error(s)` in `don`'s own BP running `OS.EXECUTE 'echo SDMARKER-OK' CAPTURING
CAP` → **`SDMARKER-OK` captured and printed back**. The control is what makes it
mean anything: same session, same user, one route refused and the other open.

**So the gate does not break programs, and §7 step 7's premise was wrong** —
see the correction there. `OS.EXECUTE ... CAPTURING` is its own BASIC statement,
`BCOMP:9647` → `OP.SHCAP` (`0xCF99`, `opcodes.h:505`) → `op_shcap()` →
`sh(TRUE)`, and **neither `kernel(K$ADMINISTRATOR,-1)` nor `!valid_shell_cmd`
is anywhere on that path**. Both live only in `CPROC`'s `os.command:` handler.
**The form that does break is `EXECUTE 'SH ...' CAPTURING`**, which goes through
TCL and therefore through the gate; the statement used directly does not.

**15 Aug 2026 — THE COMMAND LINE IS CLOSED TO AN UNELEVATED SESSION, AND SD
WILL NOT START INSIDE ITSELF. CONFIRMED ON THE INSTALLED BINARY, ninth
session.** 19 of 19, unelevated, against `C:\Program Files\SD\usr\bin\sd.exe`
**dated 09:58 and hash-identical to `bin/sd.exe`** — the fresh install, so this
is the shipped gate and not only the build's. All twelve guarded switches
(`-start -stop -restart -cleanup -d -l -m -u -suspend -resume -internal
-k ALL`) and the bare commands `LISTF` and `WHO` refused with `This command
needs an elevated session`, **exit 1**; `--version` answered `String Database
(sd) Version 1.0-2 64 Bit`, **exit 0**, which is the control — a gate that
refuses everything proves nothing. With `SD_SESSION=1` set, all four forms
tried including `--version` answered `SD is already running in this session`,
so the guard is genuinely before the gate as `comlin()` intends.

**Still not watched: the marker being set by a real `SH`**, which needs an
**elevated** live session for the reason in the next entry; only `sd.c`'s half
of that pair has run.

**15 Aug 2026 — `SH` IS ALREADY RESTRICTED, AND IT REFUSES AN ORDINARY SD
USER.** Observed while trying to close item 2c: from an unelevated session
standing in `DON` on the installed system, `SH cmd /c echo ...` answered
**`Command requires administrator privileges`** (`sysmsg(2001)`) and the
session carried on to `OFF`. The gate is **`GPL.BP/CPROC:3321`**, in the
`os.command:` handler — `if not(kernel(K$ADMINISTRATOR, -1))`, added by
"Composer AI - 2026/06/10" together with `valid_shell_cmd`. `K$ADMINISTRATOR`
is seeded from `IsElevated()` (§7 step 0), so **`SH` needs an elevated session,
not merely an administrator's account.**

**Two things follow, and the second is a correction.**

- **WHAT REFUSES TODAY IS AN AI CLEANING-CYCLE ADDITION, NOT THE LINUX
  PREVENTION AND NOT A PORT DECISION.** Established 15 Aug 2026 after the owner
  said the Linux block had been reversed early on: **the original ScarletDME
  `CPROC` has no gate here at all** — `C:\Users\dmont\Projects\GPL.BP\CPROC`'s
  `os.command:` goes straight to `os.execute`, no `kernel(K$ADMINISTRATOR,-1)`
  and no `valid_shell_cmd`. The gate's own comment dates it **2026/06/10**,
  months before the port, and `git log -S` puts it in this repository at the
  **initial import** (`f9edab0`). **`SH` and `!` have been in `VOC_TEMPLATE` as
  `V`/`OS` since that same import** and were never removed here. So this is §2's
  warning firing exactly as written — check `sdb64` before assuming a difference
  is deliberate — and it is the second instance after `VALID_OS_PATH`.
  **§7 step 7 is therefore NOT a search for a Linux block**: whatever Linux did,
  what stands in the way on Windows is one AI-authored `if`.
- **CORRECTION to 15 Aug's "an SD account DOES have a shell".** True only of an
  **elevated** session. An ssh session cannot be elevated (§4, local-only by
  design), so **an ssh user can never reach `SH`, and `ForceCommand` does keep
  them inside SD** — the hole that correction described is not reachable by the
  people it was worried about. Whoever can use `SH` is at an elevated console
  and could run anything anyway.

**Not watched, and it is what item 2c still needs:** `SH` succeeding from an
**elevated** session, and `SD_SESSION` being set in the shell it returns
(`op_sh.c:312`).

The matrix is `verify-gate.ps1`, written this session and **not tracked** — it
lives in the session scratchpad. Two things in it are the reusable part:
`--version` as the control, and **stderr redirected to a file rather than
`2>&1`**, because PowerShell 5.1 wraps a native exe's stderr in an ErrorRecord
and `$ErrorActionPreference = 'Stop'` then aborts on the first refusal — the
exact line the test exists to observe (§6, the PowerShell traps).

**15 Aug 2026 — §7 STEP 1f IS CLOSED ON A REAL INSTALL.** The installer's
`[Code]` step made the account: `ACCOUNTS` holds `DON` and `SDSYS`,
`user_accounts\don` exists, `sdu_don` has him, `sdsshonly` is **empty** — the
lockout fix holding on the installer's own path — and `adopt-account.log`
records `AppDir=C:\Program Files\SD`, `don keeps the Windows sign-in rights it
already had`, and the daemon put back as it was found. The install underneath
it is the corrected one: **3,455 files, `gcat` 130, and the installed
`gcat/$LOGIN` carries the new banner** — the first time the repository's own
catalogue has been on this machine.

**15 Aug 2026 — `ADOPT` RAN FOR THE FIRST TIME, AND IT LOCKED THE OWNER OUT OF
HIS OWN CONSOLE.** `adopt-account.ps1` against the install, elevated:
`don now has an SD account` — `ACCOUNTS/DON` written, `sdu_don` created, VOC,
`$HOLD`, `$SAVEDLISTS`, BP and private catalogue made. **And `don may sign in
over ssh only`**: the verb put him in `sdsshonly`, which carries both deny-logon
rights, so the next sign-out would have shut him out of the console and RDP.
Membership confirmed with `Get-LocalGroupMember` and removed by hand. §6 has the
fix and the rule behind it. Unelevated first, as a control: the same script was
refused with `sysmsg(10002)` and changed nothing.

**AND THE FIX IS VERIFIED, BY THE SAME VERB MINUTES APART.** `IS_GRP_MEMBER`
and `CREATEA` recompiled on the install, `0 error(s)` each, then
`ADOPT sdadopt1` — a throwaway Windows account — printed **`sdadopt1 keeps the
Windows sign-in rights it already had`** and `Get-LocalGroupMember sdsshonly`
now lists only `sdacct4`, `sdacct5`: **`don` restricted before the fix,
`sdadopt1` not after it**, nothing else changed. `sdusers`, `sdu_sdadopt1`,
`ACCOUNTS/SDADOPT1` and `user_accounts\sdadopt1` all correct. Two more things
fell out: `ADOPT` on a name with no Windows account refused with
`Invalid user name`, which is its other untested branch, and **`sd` typed
unelevated put `don` in his own account — `WHO` answered `5 DON`**, so the
`sdusers` gate still admits him through the rewritten `IS_GRP_MEMBER`.

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

**14 Aug 2026, seventh session — the same §7 step 1d branches on the repository
build, against wreckage the machine supplied itself.** Superseded by the entry
above, which re-ran all of it on the installed binary; compressed on close to
the two things that entry does not carry.

- **The control is why the fix works at all.** The old binary answered
  `SD is already started` against a dead daemon — `sdsem.c:86`, **not** the
  `bind_sysseg` string §7 step 1d named, because `get_semaphores(TRUE)` runs
  first. A fix confined to the two places the step named would have changed
  nothing the user sees. §7 step 1d records the lesson.
- **A defect the fix cannot reach:** with the segment unlinked under a live
  daemon, `sd -stop` reports success, exit 0, and leaves `sdwind` running. §6.

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

  **A caveat on reading this back, AND IT HAS NOW CAUGHT TWO ATTEMPTS.**
  `secedit /export` writes resolvable local groups **by name**, not by SID, so
  a verification that greps for a SID reports "not present" when it is.
  **There is a second half: the file is UTF-16LE** (`FF FE`), so
  `Get-Content` without `-Encoding Unicode` can match nothing at all — which
  looks identical. On 17 Aug 2026 a hand-rolled check hit **both** at once and
  reported all three rights absent on a machine where two were correctly
  present. **Use `gplbld/verify-sshonly.ps1`**, which gets both right
  (`:421-432`) and carries this warning in its own comment. Do not hand-roll
  it a third time.

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

- **`OS.EXECUTE` IS UNGATED FOR EVERYBODY, and `OS.USERS` field 2 does not
  change that.** §7 step 7. The `SH` half is verified (§4); `OS.EX` is stored,
  dictionaried and read by nobody, so an unlisted programmer with `BASIC` still
  has full OS access from a program. Gating it needs C.

- **§7 STEP 11 HAS BEEN CALLED AND DOES NOT WORK — 17 Aug 2026, on the
  08:03:49 install.** `SDConnectLocal("DON")` never returns; `sd.exe` spins
  silently because `select()` calls the attached descriptor permanently ready
  (§6). **Three defects behind it were found and fixed and those fixes stand.**
  What remains is a design choice, in §7 step 11, not a bug hunt.

  **So it is NOT currently a route to evidence for §7 step 6c**, which is what
  this entry claimed when the test was written. 6c is still reachable that way
  in principle — a local session does reach `SrvrAccount` — but only once the
  transport carries a session at all.

- **§7 STEP 6 IS BUILT IN FULL AND HAS NEVER RUN — 17 Aug 2026.** The API
  authenticates against `$CRED`, `login_user()` is deleted, `K_SET_USERNAME`
  carries the verified identity, and `vb.account` applies the `ACC$GROUP`
  grant check.

  **6a and 6d ARE COMPILED; 6c IS NOT.** It went in after the 06:07:30 install
  and the next `stage.py --bootstrap` is its first compiler — the same position
  6a was in a few hours earlier, and the same place a mistake will surface.
  **What to check when it compiles:** that `is_grp_member` resolves, and that
  the inline `deffun` beside the call does not upset `SECOND.COMPILE` the way
  `DEFFUN` upsets `bbcmp.py` (`APISRVR` already had one at line 898, so it
  should not, and that is the reason to expect it rather than a measurement).

  **THE COMPILE HALF IS NOW VERIFIED and the risk it carried is spent.**
  Seventeenth session: `SECOND.COMPILE` during the 06:07:30 bootstrap was
  `APISRVR`'s first compiler of any kind and it passed — `bootstrap.py` dies on
  any error or `is not assigned a value` warning, and did not. The evidence is
  `gcat/$APISRVR` **9,129 bytes, md5 `84f7d949…`**, against **9,056 /
  `49c28f05…`** in the previous stage; `gcat` 132 and `GPL.BP.OUT` 193 say the
  bootstrap finished rather than stopping at the seed. So `call !CRED_VERIFY(…)`
  and `void kernel(K$SET.USERNAME, …)` are both accepted BASIC. **Nothing about
  what they DO is verified by this** — a compile proves syntax.

  **THE TRANSPORT DOES NOT BLOCK ALL OF IT, WHICH THIS FILE SAID UNTIL 17 Aug
  2026 AND WAS TOO STRONG.** The two halves have different prerequisites:

  - **6c IS TESTABLE WITHOUT ssh**, through `SDConnectLocal()` (step 11, now
    built). A local session reaches `vb.account`, which is exactly what 6c
    guards. **`vb.local.login` authenticates nothing, deliberately** — a local
    client already runs as the user, so `logname` stays as
    `kernel(K$USERNAME,0)`, which is the identity 6c tests. **That makes step
    11 the cheapest route to the first evidence step 6 has ever had.**
  - **6a and 6b are NOT**, and there the old reasoning stands: they live in
    `vb.login`, the remote path, which needs a client and a transport that is
    **measured unportable** (§8).

  **What to watch when something can finally call `vb.login`:** that an account
  with no `$CRED` entry is refused; that an account with one is admitted; that
  `@logname` afterwards is the name that was verified and not the client's
  assertion; and that `kernel(K$SET.USERNAME,…)` is **refused from a program
  that is not `$internal`**, which is the gate protecting the audit trail.

  **What to watch for 6c, which is reachable sooner:** that a member of an
  account's `sdu_` group is admitted; that a non-member is refused with
  `sysmsg(10003)`; that an account with an empty `ACC$GROUP` is refused rather
  than admitted; and that SDSYS is refused.

- ~~**THE LOGIN RULE IS BUILT AND HAS NEVER RUN**~~ — **VERIFIED TWICE SINCE**,
  and this entry was left standing wrongly for a week: 5 of 5 on 16 Aug 2026
  (eleventh session) and 6 of 6 with the control on the 22:57:00 install
  (sixteenth). §4 Verified has both. The original text asked for exactly the
  checks that were then made — an elevated `sd` landing in `DON`,
  `LOGTO SDSYS` working from there, `sd -ASDSYS` refused, `sd -internal` still
  reaching SDSYS, and `verify-createaccount.ps1` still passing 16 of
  16.
- ~~**THE SERVICE IS BUILT AND HAS NEVER RUN**~~ — **CLOSED AND VERIFIED**,
  header item 2: it runs, an ordinary user reaches it, and it survives a
  restart including one with a leftover segment. Every question this entry
  raised was answered — the SCM reaches Running, `sdwind` appears, `sd -start`
  does work under LocalSystem, ordinary sessions attach to a SYSTEM-created
  segment, and the uninstaller removes the service. `sdsvc.c` is still native
  UCRT64 for the reason recorded there: a service must call
  `StartServiceCtrlDispatcher` and `sd.exe` is MSYS2-POSIX.

  §5.7 still reserves *the identity half* — a service account owning the tree,
  sessions over a named pipe — for stage 2. **What is done is the lifecycle
  half only**, and it changes nothing about who owns the files. **The named
  pipe is no longer optional**, though: §8's transport measurement forces it.
- ~~**The lockout fix is compiled and run on THIS machine only.**~~ It has
  since gone out through the installer on two machines and on every fresh
  install here — `adopt-account.log`'s `keeps the Windows sign-in rights it
  already had` line is the tell, and it appeared again on 22:57:00.
- ~~**No staged tree has yet been built with the `ACCOUNTS/SDSYS` fix.**~~ Many
  have; `check_no_stage_paths` is clean on every stage since, and
  `retarget_sdsys_account()` is now a normal part of `stage.py --bootstrap`.
- **`MODIFY.ACCOUNT` has never been run.** `CREATE.ACCOUNT` and
  `DELETE.ACCOUNT` both have (§4 Verified).
- ~~**`DELETE.ACCOUNT`'s "SD created it" branch is untested**.~~ **RUN AND
  VERIFIED 16 Aug 2026**, sixteenth session, on `sdacct14` — §4 Verified. All
  three of `DELACC`'s cases have now executed at some point.
- ~~**`CREATE.ACCOUNT ... ADOPT` is untested**, and nothing calls it.~~ **The
  installer calls it on every install** and `adopt-account.log` records it —
  §7 step 1f, closed 15 Aug 2026.
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

#### The client library has its OWN lineage, and it is a round trip

Stated by the repository owner, 15 Aug 2026. **The three generations in §2 do
not describe `gplsrc/sdclilib/` — it came a different way:**

1. **`sdb64`'s own C developer started a partial Windows API library**, the
   Visual Studio port whose Winsock transport the README still credits.
2. **The owner set AI on it and it was completed**, becoming
   **`github.com/dmontaine/winsdclilib`**.
3. **Vendored into this repository** 13 Aug 2026 from commit `b6624565`
   (5 Aug 2026) — `gplsrc/sdclilib/VENDORING.md` is the record, and the whole
   directory is a vendored copy kept faithful to its source on purpose.
4. **Their developer then forked `winsdclilib` back**, and changes from it are
   in `sdb64`'s `dev` branch now.

**So for this directory, code has flowed BOTH ways, and "upstream" is
ambiguous** — the reverse of every other file in the port, where `sdb64` is
plainly the source. Two consequences worth acting on:

- **Do not "align with upstream" reflexively here.** A session did exactly that
  with `SV_EMSG_PAIR`/`SV_ECONTXT` and had to revert it (§2's dev-branch review,
  UPSTREAM_FIXES.md #2).
- **An AI completed step 2**, so this directory carries the same risk §2
  describes for generation 2 — plausible-looking decisions nobody made
  deliberately. It has **no `Composer AI` markers**, so that grep does not find
  them here; the tell is absent and the suspicion still applies.

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
| **`sudo sd`, or any elevated session** | **your own account, like everybody else** — corrected 15 Aug 2026, tenth session. It used to go straight into SDSYS; see the header. `LOGTO SDSYS` afterwards |
| `sd -Aname` | **refused unless `name` is your own account** — `sysmsg(10051)`. `-INTERNAL` is exempt and forces SDSYS, needing elevation — `sysmsg(10002)` |
| **an elevated session, in `LOGTO`** | **passes without the group check**, which is now the only place that bypass lives. Not a convenience — `ACCOUNTS/SDSYS` names a group Windows does not have, so the check would refuse administration to everybody (§6). Linux root does not pass it either |

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

- **The audit records — BUILT AND VERIFIED 16 Aug 2026** (§7 step 4). Login,
  refused login, `LOGTO`, refused `LOGTO` and `GRANT`/`REVOKE` all write to
  `<sysdir>/audit`. The identity is stamped in C from `my_uptr`, which is what
  the `logname` warning below was asking for.
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

**REVERSED 16 Aug 2026: OpenSSH Server is ALWAYS INSTALLED, and what is opt-in
is the network exposure.** Owner's decision. The `installssh` task is gone;
`sd.iss` runs `install-ssh.ps1` under `Check: SshServerAbsent`.

Why: SD accounts sign in over ssh and nothing else (§5.6.2), and the API is
carried over ssh (§8, posture B — which already said this "makes the ssh
install path load-bearing"). So an install without ssh is one nobody but the
installing user can use: every non-administrator account `CREATE.ACCOUNT`
makes is denied console and RDP (`CREATEA:442`, unconditional) with nothing to
fall back on. **A local-only machine is served by `ssh localhost`**, which is
what decided it — it needs no network.

**The new opt-in is `sshremote`, off by default**, and it is stricter than what
it replaces. Installing the capability creates `OpenSSH-Server-In-TCP` **and
enables it for any remote address** — measured 16 Aug 2026: `Enabled True,
Inbound, Profile Private, RemoteAddress Any` — so the old ticked box opened
port 22 to the LAN as a side effect nobody chose. `gplbld/ssh-firewall.ps1`
scopes the rule to `127.0.0.1,::1` unless the task is ticked. `RemoteAddress`
rather than `Enabled False`: both leave loopback working, but a disabled rule
reads as something switched off and gets switched back on.

**What did NOT change, and must not**: "never reconfigure or restart an ssh
server we did not install" is a separate rule from optionality. `SshWasAbsent`
is cached in `InitializeSetup` — from `ssPostInstall` the live test answers
False everywhere, so "did we put this here?" is otherwise unanswerable, and
both the firewall step and the report depend on it. `limitssh` (was
`installssh\allowgroups`) is now top-level and **its own `Check` is the only
thing left** keeping it off somebody else's server.

**The uninstaller does not widen the rule back.** Deliberate asymmetry with
`RemoveAllowGroups`: restoring it means opening a port on the way out.

**The original reasoning for the opt-in, kept because the requirements below
still stand:** SD will often be installed by someone with little administrative
knowledge who wants the ten people on their local network to reach it. Good
security is the default; the easy path exists but has to be chosen. Note the
Linux script installed and enabled ssh **unconditionally** — that behaviour is
not inherited but re-decided, which §5.16's rule 2 permits. **That re-decision
has now landed on the same answer the Linux script had, by a different route.**

Requirements, and each of these has already cost something:

- ~~**Unchecked by default**~~ — superseded above. The wording requirement
  survives and moved to the exposure task: it starts a service listening on
  port 22 and adds a firewall rule, granting remote shell access to the whole
  machine, not just to SD.
- **If OpenSSH Server is already present, say so and do not offer the option.**
  Detect it **without elevation** — `%SystemRoot%\System32\OpenSSH\sshd.exe` on
  disk, or an `sshd` service registered; `Get-WindowsCapability -Online`
  requires elevation (measured 14 Aug 2026). Never silently reconfigure or
  restart an ssh server the machine already has: it may be managed by policy.
  This is also what makes the `AllowGroups` subtask structurally unreachable on
  such a machine (§5.6.2).
- **A failure to install it must not fail the SD install.** It is a Features on
  Demand capability, blockable by policy, a WSUS with no FoD source, a metered
  connection or an offline machine. Report it and carry on.
  **The rule survived 16 Aug 2026 but its consequence did not.** The no-ssh
  state used to be one the user chose; it is now one the machine can impose,
  and in it **no account but the installing user's can sign in anywhere**. So
  it is reported in as many words with the retry command — `SshReport` in
  `sd.iss`, from machine state (`sshd.exe` present, `Services\sshd` key
  present) rather than from an exit code.
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

### 5.13.1 The ForceCommand scp cost has a workaround: pull, do not push (17 Aug 2026)

**The global `ForceCommand` stays global** — owner reaffirmed 17 Aug 2026, after
`OS.USERS` (§7 step 7) made shell access grantable per account. The
`Match Group sdsshonly` alternative was considered and rejected again: it would
hand remote administrators a PowerShell prompt, which is more than the global
form gives them.

**The recorded cost — scp and sftp stop working machine-wide — is INBOUND
only, and that is the whole of the answer.** `ForceCommand` applies to sessions
where this machine is the ssh **server**. WinSCP or scp running **on** this
machine, connecting outward, makes it the **client**, and `sshd_config` is not
consulted at all.

**So an administrator copies files by PULLING them**, from a console or Remote
Desktop session — both of which are untouched, because administrators are never
put in `sdsshonly` (`CREATEA:492`). Outbound is not firewalled: all three
profiles report `DefaultOutboundAction = NotConfigured`, i.e. the Windows
default of Allow (measured 17 Aug 2026).

**What genuinely cannot be done: pushing a file TO this machine over ssh.**
Nobody can, administrators included. That is the accepted cost, and the reason
it is acceptable is the paragraph above.

**Do not "fix" this with a `Match Group administrators` exemption without
reading this first.** Beyond giving admins a shell instead of SD, it may not
even work: `sshd_config` takes the FIRST obtained value for a keyword, and
`allow-ssh-groups.ps1` inserts its block **before** the first `Match`
(`Add-OurBlock`), so a later `ForceCommand none` is not guaranteed to override
the earlier global one. That was not resolved — `sshd -T` needs the host keys
and refuses unelevated with "no hostkeys available" — and it does not need to
be, because pulling avoids the question entirely.

### 5.13 Shell access is restored, not blocked (decided 13 Aug 2026)

Correction from the repository owner on 13 Aug 2026: disabling the user's
ability to shell out with `SH` or `!` in the Linux version **was a mistake**,
and Windows makes it a worse one. Many programs have to reach Windows
utilities, and there is no way to do that with shell access blocked.

**MEASURED AGAINST `sdb64` ITSELF, 15 Aug 2026, ninth session — THE PREMISE
ABOVE IS NOT TRUE OF THE CURRENT LINUX VERSION.** With the upstream repository
cloned locally at `../sdb64`, **neither branch blocks anything**: `main` and
`origin/dev` both have `GPL.BP/CPROC` line 3252's `os.command:` running
straight into `os.execute` with no test, both carry `SH` and `!` in
`VOC_TEMPLATE` as `V`/`OS`, and `op_sh.c` has no privilege check on either.
`K$SECURE` exists upstream but is not this — `INT$KEYS.H:68` defines it as
"Secure system (login required)?", a login flag. **Neither branch contains a
single `Composer AI` marker**, which is the cleanest confirmation that all 226
belong to generation 2 (§2).

So there is **nothing upstream to restore**, and the only thing that has ever
blocked shell-out in this lineage is the generation-2 gate at `CPROC:3321`.
Whatever the block the owner remembers was, it is not in `sdb64` today. That
does not settle whether the gate should stay — §7 step 7 — it only removes
"Linux did it" as an argument on either side.

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

- **`` `e `` IS NOT AN ESCAPE IN WINDOWS POWERSHELL 5.1, so every ANSI strip in
  `gplbld` is dead code.** 18 Aug 2026. `` `e `` arrived in PowerShell 6, so
  ``"`e\[[0-9]*[A-Za-z]"`` is the literal letter `e` and matches nothing SD
  emits. Measured: `TERM 200,9999` comes back as `TERM<ESC>[7G200,9999` with the
  strip applied. **Use `[char]27`.** `verify-osusers.ps1` does;
  `verify-nocase.ps1` and `verify-tiers.ps1` still carry the dead line and have
  never been hurt by it, because both match on substrings that no escape
  sequence sits inside. It looks like working code, which is the trap.

- **`struct PCFG` IS IN THE SHARED SEGMENT, WHATEVER ITS HEADER COMMENT SAYS,
  AND `SYSSEG_REVSTAMP` WILL NOT CATCH A CHANGE TO IT.** 16 Aug 2026,
  sixteenth session, found while removing one `bool` from it (§7 step 1a).
  `config.h` introduces `PCFG` as "Config parameters loaded per process", which
  reads as process-private and is why the first reading of this was that the
  layout did not matter. It is: `sysseg.c:288` copies a template into the
  segment at `pcfg_offset`, and **every attaching session does
  `memcpy(&pcfg, ..., sizeof(struct PCFG))`** at `sysseg.c:142`.

  So adding, removing or reordering a `PCFG` field **changes a layout two
  binaries have to agree on**, and the only compatibility check is
  `sysseg->revstamp` — which is `MAJOR_REV/MINOR_REV/BUILD` (`sysseg.c:57`),
  the release number. **Two builds of the same release have the same revstamp
  and are not required to have the same `PCFG`.**

  **The failure is silent and does not look like a layout problem:** the
  session reads every field after the changed one shifted, so `SH`/`SH1` come
  out truncated or shifted and `OS.EXECUTE` fails in ways that point at
  PowerShell. **A full install cycle is what makes it safe** — every binary is
  replaced at once — so this only bites somebody copying a freshly built
  `sd.exe` over an installed one while SD is running. Do not do that after
  touching `config.h`; `sd -stop`, replace, `sd -start`.

- **`read_config()` RUNS ONLY WHEN THE SEGMENT IS CREATED, so a configuration
  change cannot be tested from an ordinary session.** Same session. An
  attaching session takes `pcfg` from the segment (above) and never opens the
  file, and `bind_sysseg()` returns at `sysseg.c:150` before the read when
  `create` is false. **`sd --version` returns earlier still**, before any of
  it. Three tests of a parser change were run before this was understood and
  **all three were blind — including their controls**, which is what eventually
  gave it away: a control that refuses to fail is not a passing test, it is a
  broken instrument. **The only route in is `sd -start`** (elevated, service
  stopped) with `SD_CONFIG` naming the file under test.

- **A STAGE WHOSE BOOTSTRAP DIED AFTER THE SEED PHASE PACKAGES AND INSTALLS IN
  SILENCE, AND `assert-current` CANNOT SEE IT.** 16 Aug 2026, sixteenth
  session; it cost the whole of the fifteenth session's SD-side results and
  produced a false open question in §8. The bootstrap's early phase compiles
  `BBPROC`, `BCOMP` and `PATHTKN` with `bbcmp.py` and **touches an empty
  `gcat/$CPROC`**; if it stops there, the tree still looks populated — every
  static file is present and correct — but `gcat` holds **4** entries against
  132, `GPL.BP.OUT` **3** against 193, and there is no `$LOGIN` and no `VOC`.
  `ISCC` packages it happily and Setup exits 0.

  **`assert-current` is blind to it by construction**: it compares the install
  against **source**, and `gcat`/`GPL.BP.OUT`/`VOC` are build products with no
  source counterpart. It exited 0 over this tree.

  **The symptom, if you install one:** every `sd` invocation dies
  `Unable to load '$CPROC' object code`, exit `0xC0000005`. It reads as a
  corrupt binary, and it is a missing catalogue.

  **The one-second check, and it discriminates where a file count does not:**

  ```powershell
  (Get-Item 'C:\ProgramData\SD\sdsys\gcat\$CPROC').Length   # 25208, never 0
  ```

  **`$CPROC` at 0 bytes means the bootstrap never finished.** A whole-tree file
  count is a poor instrument here — 3,139 against 3,475 is a 10% shortfall that
  reads as rounding. Sizes discriminate too: seed `$BCOMP` is 70,697,
  `BCOMP`-compiled is 87,992.

  **IT IS ENFORCED NOW, not remembered:** `stage.py`'s
  `check_bootstrap_complete()` runs on those five facts immediately after the
  bootstrap and refuses to stage a tree that fails any of them. **It judges the
  tree, not the exit code**, because the exit code was 0 here. Exercised
  against both trees when written: silent on the healthy stage, five faults on
  the broken install.

- **`/dev/shm` IS A REAL DIRECTORY HERE, SO POSIX SHARED MEMORY OUTLIVES THE
  MACHINE.** 16 Aug 2026, twelfth session. `etc/fstab` binds it to
  `C:\ProgramData\SD\shm` on NTFS (`stage.py:196`), because `shm_open()` creates
  files and Program Files is read-only to ordinary users. On Linux `/dev/shm` is
  tmpfs and empties at every boot, so **any reasoning of the form "a segment
  that exists means a system that might still be live" is wrong on this port**.
  It broke the service across a restart: an unclean `sd -stop` left the segment,
  it survived the reboot, and `sd -start` refused it as `SD_WRECKAGE` for ever
  after (header item 1). The same applies to anything else that assumes
  `/dev/shm` is volatile. Win32 semaphores are **not** affected — they are
  kernel objects and do vanish (`sdsem.c`), which is why the two now behave
  differently across a reboot.

- **A NON-CRASHING SERVICE NEVER GETS ITS RECOVERY ACTIONS.** 16 Aug 2026,
  twelfth session. `sc failure` is ignored unless the service process crashes;
  a service that reports `SERVICE_STOPPED` with an error code is a "non-crash
  failure" and needs `sc failureflag <name> 1` as well. `install-service.ps1:114`
  configures two restarts and `sc qfailureflag SD` says
  `FAILURE_ACTIONS_ON_NONCRASH_FAILURES: FALSE`, so they have never once run.
  **Check the flag before believing a recovery policy exists** — and note it
  cuts both ways here: had those restarts fired, the retry would have found a
  `shm` the failed start had just cleaned and succeeded, hiding the bug above.

- **A LINE OF `sd.iss` STARTING WITH `#13#10` IS READ AS A PREPROCESSOR
  DIRECTIVE.** 16 Aug 2026, eleventh session. ISPP treats any line whose first
  non-blank character is `#` as a directive, so a wrapped Pascal string constant
  aborts the compile with `Unknown preprocessor directive` and a line number,
  saying nothing about string continuation. Mid-line `#13#10` is fine, which is
  why the rest of that `MsgBox` works. **Keep `#13#10` off the start of a line**
  — join it to the line above. Cost an elevated run: `sd.iss:560` was edited on
  15 Aug when the service message was added and never compiled again before the
  handoff.

- **THE CLAUDE CODE `Bash` TOOL IS NOT MSYS2, AND `make ... | tail` REPORTS
  EXIT 0 HAVING BUILT NOTHING.** 16 Aug 2026, eleventh session. `make` is not on
  that shell's PATH; the failure is `make: command not found` on stdout and the
  pipe reports `tail`'s status, so it reads as a successful build. Same swallowed
  status as the `stage.py` case in HISTORY. **Build through
  `C:\msys64\usr\bin\bash.exe -lc "make -C <abs path> sd"`** and read the linker
  lines, not the exit code.

- **`cygwin_attach_handle_to_fd()` GIVES A DESCRIPTOR THAT `select()` CALLS
  PERMANENTLY READY, AND THAT DEFEATS SD's INPUT LAYER.** 17 Aug 2026,
  seventeenth session, §7 step 11. **This is the finding that matters and it
  is not a flag to fix** — see §7 step 11 for what it costs.

  A descriptor built from a raw Windows HANDLE has no real `select` support in
  the Cygwin runtime. `strace` on `sd.exe` serving a named pipe shows, forever:

  ```
  dtable::select_read: //./pipe/SDProbePipe5 fd 0
  select: sel.always_ready 1
  set_bits: ready 1
  read: 1 = read(0, 0x…, 1)
  ```

  **`sel.always_ready 1`.** So `sdpoll()` — `poll()`, `linuxio.c:757` — always
  answers "readable", whether or not anything has arrived. SD asks exactly that
  question before every read (`linuxio.c:535`, `:383`, `:456`), so it spins
  reading one byte at a time and never blocks, never frames a packet, and never
  replies. Symptom: `sd.exe` alive, silent, at high CPU, and a client waiting
  for a response that cannot come.

  **AND IT MADE AN EARLIER DIAGNOSIS HERE WRONG.** This entry first said poll
  "reports readable" while `read()` gives `EBADF`, as though poll were
  functioning and disagreeing with read. **Poll was never functioning**: it
  answers ready unconditionally, which is why it also said ready in the `EBADF`
  case. The access-argument fact below is still true and still worth having —
  it is just not what poll was telling us.

  **The access argument must match how the HANDLE was opened.** Open
  `GENERIC_READ | GENERIC_WRITE` and attach descriptor 0 with `GENERIC_READ` —
  the obvious thing to write — and the attach **succeeds**, returning 0, while
  `read()` then fails `EBADF`. The name argument is not involved: the pipe
  name, `NULL` and `/dev/null` behave identically, `NULL` additionally giving
  `EFAULT` on the attach, and POSIX `O_RDONLY`/`O_RDWR` values fail like
  `GENERIC_READ`. `O_NONBLOCK` is harmless; `F_SETOWN` fails `EINVAL` and does
  not matter, `O_ASYNC` being 0 here (`sddefs.h:96`).

- **THERE ARE TWO "INTERNAL"S AND THEY ARE NOT THE SAME FLAG.** 17 Aug 2026,
  seventeenth session, caught while writing §7 step 6c and before it reached a
  commit — an earlier draft of that step reasoned from the wrong one and its
  conclusion was wrong.

  - **`$internal` in a program's header** is `HDR_INTERNAL`. It is a property
    of the PROGRAM. `BCOMP` checks it to allow `KERNEL` to be called at all,
    and `op_kernel.c` gates `K_SET_USERNAME` on it (§7 step 6a).
  - **`K$INTERNAL`** reads `internal_mode` (`op_kernel.c:140`). It is a
    property of the SESSION, set only by `sd -internal` or `sd -I`
    (`sd.c:338`, `sd.c:349`), **both behind `check_admin()`** — so it already
    implies an elevated session.

  **A program can be `$internal` in a session that is not `internal_mode`, and
  `APISRVR` is exactly that**: `$internal` at line 64, spawned with `-C`/`-N`/
  `-Q`, never `-internal`. So `kernel(K$INTERNAL,-1)` is FALSE inside it.
  **Both flags are live in that one file**, which is where this will be misread
  again. Reading the header flag as the session one makes a gate look
  permanently open when it is permanently shut.

- **AN ORDINARY SD SESSION CANNOT BE READ WITHOUT A CONSOLE, AND THE THREE
  WRONG WAYS EACH FAIL DIFFERENTLY.** 17 Aug 2026, seventeenth session, trying
  to confirm the `WHO` → `2 DON` result on a fresh install without a human at a
  terminal. All three cost a round trip:

  - **`sd WHO` is refused unelevated BY DESIGN** — `This command needs an
    elevated session`, `sd.c:525`, owner's rule of 15 Aug: *a command is a
    parameter too*. **This is not a defect and not a broken install**; it is
    the gate working. Plain `sd` with nothing after it is the untouched path.
  - **The installed `sd.exe` launched from an MSYS2 shell answers `SD has not
    been started`** while the service is Running with a live segment. Almost
    certainly two Cygwin universes: `sd.exe` loads its own
    `msys-2.0.dll` from `usr\bin`, so its POSIX root is `C:\Program Files\SD`
    and `/dev/shm` is SD's, while the parent shell is `C:\msys64`. **Launch it
    from a native Windows shell**, which is how a user runs it anyway.
  - **Launched natively with stdin/stdout redirected it blocks in terminal
    setup** and writes nothing at all — killed after two minutes, no output on
    either stream. `termios` → Console API is §7 step 13, unported.

  **So a `WHO` measurement needs a person at a terminal**, and a claim of one
  in §4 belongs to whichever install a person was sitting at. What CAN be read
  without a console: `adopt-account.log`, which records a full BASIC session
  the installer ran (banner, `Creating VOC...`, `Adding to register of
  accounts...`) and so rules out the catalogue-less failure mode.

- **ENABLING REMOTE DESKTOP DOES NOTHING UNTIL THE MACHINE REBOOTS, AND THE
  SETTINGS TOGGLE REPORTS SUCCESS EITHER WAY.** 15 Aug 2026, tenth session,
  setting up §7 step 2's RDP test. `fDenyTSConnections` read **0**, no Group
  Policy key, `TermService` **Running** — and **nothing listening on 3389**.
  `TermService` creates the listener when it starts and **cannot be restarted**
  (`Restart-Service` fails "stop failed"), so switching RDP on under a running
  service leaves it off until a restart. **`netstat -an | findstr 3389` is the
  only honest check**; the toggle, the registry value and the service state all
  looked correct while the port was shut. Cost three rounds of firewall changes
  that were never the problem — the guest's network was also classified
  **Public**, which really does block the RDP rules, so there was a plausible
  wrong answer sitting in the way.

- **`mstsc` PREFILLS THE USERNAME FROM THE HOST, WHICH SILENTLY RUINS AN
  RDP CONTROL/TREATMENT TEST.** Same session. The credential dialog opens on the
  *client* with the local user already filled in, so accepting it authenticates
  as the wrong account against a workgroup guest. **Qualify it —
  `GUEST\account`** — via "More choices" → "Use a different account", and leave
  "Remember me" unticked or the next run is ambiguous. An account-name mistake
  produces a credentials error that reads much like a deny-rights refusal; only
  the wording separates them (§4).

- **A TEST THAT CAPTURES ONLY stdout SEES SD's REFUSALS AS SILENCE.** 15 Aug
  2026, tenth session. `SH sd --version` produced **no output whatever** in a
  piped session, which reads like the command never ran; it had, and had
  refused, on `stderr` (`sd.c:301` and most `fprintf(stderr,` sites like it).
  **A gate under test is exactly the output most likely to be on stderr**, so a
  stdout-only harness is blind to the thing it exists to watch. Two working
  forms: `OS.EXECUTE ... CAPTURING` gets both, because `op_sh.c:281-282` dup2s
  the pipe onto **1 and 2**; otherwise redirect `sd`'s own stderr to a **file**
  — never `2>&1`, which PowerShell 5.1 turns into an ErrorRecord (below).

- **`Start-Process -Wait` WITH REDIRECTED OUTPUT NEVER RETURNS FROM
  `sd -start`, BECAUSE `sdwind` INHERITS THE REDIRECT HANDLES.** 17 Aug 2026,
  seventeenth session. `sd -start` forks the daemon and exits; the daemon keeps
  the inherited write ends of `-RedirectStandardOutput` / `-Error` open for its
  whole life, and PowerShell waits for those streams to close. **The command
  has succeeded and the script hangs anyway**, with the success message already
  in the file.

  **Measured, 06:29:45:** `stopA-start.out` **29 bytes**, `SD (64 Bit) has been
  started`; `sd.exe` gone; `sdwind.exe` pid 13188 alive **with a dead parent**;
  `Start-Process -Wait` still blocked. Recovery is `Stop-Process -Name sdwind
  -Force`, delete the segment, `sc.exe start SD`.

  **TO START SD FROM A SCRIPT: use `sc.exe start SD` and poll, or run
  `sd -start` with NO redirection and judge it from state** — daemon up,
  segment present — rather than from its stdout. The same hazard applies to any
  launcher that both redirects and waits.

  **CORRECTION, AND THE MISTAKEN REASONING IS LEFT HERE ON PURPOSE.** This
  entry first said the hang was `| Out-Null` discarding a message from
  `sd -stop`, that `sd -stop` "did not take the daemon down", and that whether
  SD had failed was unknown. **All of that was wrong, and it was wrong because
  a surviving `sdwind` was read as evidence about the cleanup without checking
  the script had ever reached the cleanup.** It had not: the 06:08 run hung
  inside its *start* helper, before printing that step's result and before any
  `sd -stop` existed. **`sd -stop` was never run, so nothing here implicates
  it, and `stop_sd()` is not under suspicion at all.** The lesson that survives
  is the one the entry above already gives — read what the run actually wrote,
  in order, before inferring which step you are standing in. A 29-byte output
  file said "this step succeeded" and was there to be read the first time.

- **MSYS2 `python` GIVEN A BACKSLASHED RELATIVE SCRIPT PATH DIES
  `No module named 'bootstrap'`.** 15 Aug 2026, tenth session.
  `python.exe gplbld\stage.py ...` mis-resolves `sys.path[0]`, so `stage.py`'s
  `from bootstrap import is_elevated` fails and it reads as a missing file
  rather than a path-separator problem. **Use `gplbld/stage.py`.** Cheap here,
  expensive in an elevated window, which is the only place staging can run.

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

- **CREATING AN SD ACCOUNT COULD LOCK A WINDOWS ADMINISTRATOR OUT OF THEIR OWN
  CONSOLE, AND `!is_grp_member` COULD NOT HAVE STOPPED IT.** 15 Aug 2026, both
  found in one run of `ADOPT` (§4).

  `CREATEA` applies the ssh-only restriction as the `else` of the
  `ADMINISTRATOR` keyword, so an *adopted* account — the installer's, and by
  definition an administrator — landed in `sdsshonly` and its two deny-logon
  rights. Nothing is visible until the next sign-in, and then the console and
  RDP are both gone.

  **Owner's rule, 15 Aug 2026: no administrator account carries a lockout
  risk.** An OS administrator made outside SD simply has no SD account; one
  made *inside* SD must be able to use both the machine and SD. So `CREATEA`
  now skips the restriction for an adopted account **and** for anyone Windows
  already calls an administrator, tested by SID.

  **Which needed a second fix, because the test could not be asked.**
  `Get-LocalGroupMember -Group "S-1-5-32-544"` answers `Group ... was not
  found` while `-SID` returns the members — measured — so `!is_grp_member` took
  its "no such group" path and answered **false for every administrator**, fail
  closed and silent. It now uses `-SID` for a SID-shaped group, matching
  `!os_group`, which always accepted either.

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
  is not a failed start — look at the daemon before believing it. What works
  from PowerShell: `Start-Process ... -PassThru -NoNewWindow` with the output
  redirected to files, then `$p.WaitForExit(20000)`; `-Wait` is the form that
  hangs.

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
  `etc\fstab` maps `/dev/shm` there, the first thing to fail is semaphore
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

  **FIXED AT SOURCE 15 Aug 2026, because `sd64/Makefile` was only ever covering
  its own route.** The client library has three documented ways to build it and
  the 14 Aug fix protected one. The other two — `make` run **inside**
  `gplsrc/sdclilib/`, and `build.cmd` from a Windows prompt — both still failed
  silently, and `build.cmd` is what the README recommends first. Both now put
  the compiler's directory on PATH themselves, derived from `$(CC)` /
  `%GCC%` so overriding the compiler moves it too. **The fix is in
  `winsdclilib` as well** (`../winsdclilib`), since the vendored copy came from
  there and the two build files are byte-identical.

  **Before and after, both observed this session:**
  `make CC=/c/msys64/ucrt64/bin/gcc.exe check` from a plain MSYS2 shell gave
  the empty exit 1; the same command now compiles and passes both test suites.
  `build.cmd` from `cmd.exe` now exits 0 on a clean tree. It does **not** bite
  in an MSYS2 **UCRT64** shell, which already has the directory on PATH — that
  is why the README's `make` instructions were written and never noticed it.

- **`NoDefaultCurrentDirectoryInExePath` IS SET ON THIS MACHINE, so `cmd` will
  not run an executable sitting in the current directory.** A bare
  `smoke-test.exe` answers `is not recognized as an internal or external
  command` with the file plainly there, which reads as a build failure rather
  than a lookup rule. `winsdclilib`'s `build.cmd` invoked both its tests that
  way and now uses `.\`. Found 15 Aug 2026, after the PATH fix above exposed
  it — the script had never got that far before.

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

  **AND IT REACHES THE INSTALLER TOO, one level up.** 15 Aug 2026, tenth
  session: `Start-Process <setup.exe> -Wait` never returned, although Setup had
  finished and left no process — because the installer's own `[Code]` account
  step runs `adopt-account.ps1`, which starts `sdwind`, which inherits the
  handles and outlives everything. **Anything that starts SD, however
  indirectly, cannot be waited on.** Poll for what you actually want — here,
  `C:\Program Files\SD\usr\bin\sd.exe` existing.

  **The converse cost an install the same day**: `adopt-account.ps1` looked for
  `sdwind` ONCE, immediately after `sd -start` returned, and `sd -start` forks
  the daemon and returns before it is in the process table. On an idle machine
  that race is always won; with a VM running it was lost, and the installer
  finished having given the installing user no SD account, reporting only
  `code 3` in a dialog. **Poll for the daemon; never look once.**

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

1. **CLOSED 16 Aug 2026, sixteenth session — the loose ends the account model
   left are all tied off.** a and c went that session, b was superseded by
   step 0b, and d, e and f were already done. The model itself was proven
   earlier (§4, §5.6.1, §5.6.2). Kept below because the sub-steps record what
   each cost and what to look for if any of it regresses.

   a. **DONE 16 Aug 2026, sixteenth session — `CREATUSR` IS GONE, WITH ONE
      DELIBERATE EXCEPTION.** Removed: the `struct PCFG` field (`config.h`),
      its default (`config.c`), `op_config.c`'s answer, and `CONFIG`'s print.
      `op_pconfig()` never had a branch for it. `make sd` clean after
      `rm -f gplobj/*.o` — **required, not tidiness: `config.h` changed and
      the Makefile tracks no header dependencies**, so every field after the
      removed one shifts and stale objects read the wrong offsets.

      **AND IT CHANGED A SHARED-SEGMENT LAYOUT, which is not obvious from the
      header comment saying `PCFG` is "loaded per process".** A template copy
      lives in the segment at `sysseg->pcfg_offset` and every attaching session
      does `memcpy(&pcfg, ..., sizeof(struct PCFG))` (`sysseg.c:142`, `:288`).
      Removing the `bool` shifts `dumpdir` and everything after it by one byte.
      **`SYSSEG_REVSTAMP` DOES NOT CATCH THIS** — it is
      `MAJOR_REV/MINOR_REV/BUILD` (`sysseg.c:57`), i.e. release identity, and
      this release did not change. Harmless as shipped, because an install
      replaces every binary at once; the hazard is copying one rebuilt
      `sd.exe` onto a running system. §6 has it.

      **THE PARSER STILL ACCEPTS AND DISCARDS `CREATUSR=`, on purpose.** The
      chain in `read_config()` ends in `else { "Unrecognised configuration
      parameter" }`, which **aborts and stops SD starting** — so deleting the
      branch would turn a tidy-up into a failure to start for anyone whose
      `sd.conf` carries the line. **`../sdb64` still parses it**, so a file
      copied from a Linux install can have one. No `sd.conf` on this machine
      does (all four checked), which is why this is cheap insurance rather
      than a fix.

      **VERIFIED 17 Aug 2026, seventeenth session, WITH THE CONTROL** — on the
      06:07:30 install, `assert-current` exit 0:

      ```
      control   NOSUCHPARAM=1  ->  exit 1, stderr:
                                   Unrecognised configuration parameter 'NOSUCHPARAM=1'
      treatment CREATUSR=1     ->  exit 0, stdout: SD (64 Bit) has been started
      ```

      **The control is what makes this mean anything**, and is why two earlier
      attempts proved nothing: `read_config()` runs **only when the segment is
      created** (`sysseg.c:150-157` — an attaching session takes `pcfg` from the
      segment instead), so nothing an ordinary session does reaches the parser,
      and a treatment that starts is also what a parser reached by nobody would
      do. The test is therefore `sd -start` against each conf **with SD fully
      stopped first**, elevated. A third earlier attempt was blind for a
      different reason (`--version` returns earlier still).

      **Correction, 14 Aug 2026:** this file previously said `CREATUSR` "is not
      in the shipped `sd.conf` and defaults off", and gave that as a blocker.
      **That was wrong** — `config.c` line 98 set `pcfg.create_user = 1`, so
      it defaulted **on** and never blocked anything. The real blocker was the
      pathname validator in §6.
   b. **MOVED INTO STEP 0b, 14 Aug 2026.** Restoring the `sdusers` gate is no
      longer a question that needs settling against §5.6.1 — the reversal in
      §5.6 answers it. The gate goes back.
   c. **CLOSED 16 Aug 2026, sixteenth session — BOTH REMAINING BRANCHES HAVE
      NOW RUN.** The "SD created it" delete was measured on `sdacct14` (§4);
      `ADOPT` runs on every install through `adopt-account.ps1` (step 1f).
      Built 14 Aug 2026, seventh session — compiled, catalogued and run.

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
   e. **DONE 15 Aug 2026, eighth session** (`a83ac44`), and this entry was left
      open by mistake — closed in the ninth on finding `CREATEA:333` saying
      "THE setgid BIT IS GONE, AND SO IS sudo". The `sudo chmod g+s`, the seven
      `set.owner` calls and the subroutine behind them are all removed; the
      Windows equivalent is the inheritable ACE the installer sets (§5.7).
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

      **BUILT 15 Aug 2026.** `gplbld/adopt-account.ps1` does it — starts SD if
      it must, runs the verb, judges on the `ACCOUNTS` record rather than the
      exit status, restores what it found; exit 0 adopted, 2 already there,
      3 no server, 1 refused. `sd.iss` calls it from `[Code]` at
      `ssPostInstall`, **not `[Run]`**: a `postinstall` entry runs as the
      original, unelevated user, which is one of the three reasons the old
      SDSYS password step never worked. The closing dialog reports all three
      outcomes.

      **CLOSED 15 Aug 2026, ON A REAL INSTALL (§4).** The installer's `[Code]`
      step made the account, the log records it, and `don` types `sd` and lands
      in `DON`. Two defects were found on the way and are worth keeping:
      `ADOPT` confined him to ssh (§6, the lockout fix), and the step failed
      once with **`$PSScriptRoot` empty in a param default** — the script has
      `[CmdletBinding()]` and a mandatory parameter, which makes it so, and the
      installer now passes `-AppDir` rather than depending on it. **That
      failure was silent until the script was made to write
      `<DataDir>\adopt-account.log`**, which is the first place to look if an
      install ever produces no account.
2. **DONE 15 Aug 2026, tenth session (§4).** A VirtualBox guest served as the
   second machine: install byte-identical, all four counts matching, `COUNT VOC`
   431, and **the RDP refusal measured with a control**. §5.6.2 is complete.

   **The rig is reusable and worth keeping.** VM `Windows 11 Clone`, snapshot
   `Before SD install`, NIC **bridged** — NAT cannot be used, since the host must
   open a connection *to* the guest. Bridging over the WiFi adapter worked here,
   which is not guaranteed; the host ARP entry carrying the VM's own MAC is how
   to tell it is working before blaming anything else. Files reach the guest
   through `VBoxManage sharedfolder add --transient --automount`, which needs no
   guest credentials — **do not drive the guest with `guestcontrol`**, which
   does. Read §6's two RDP traps before setting it up again; between them they
   cost most of an hour.

   **Left undone deliberately:** the ssh task on screen, which needs a fresh
   wizard run (step 3).

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

   - **CORRECTED 15 Aug 2026: the owner has seen the closing dialog and has
     screenshotted it before now.** This file's "nobody has seen it" was simply
     wrong. It was watched again in the tenth session, and **reading it found a
     defect that compiling never would**: it ended by offering
     `net localgroup sdusers <name> /add` for somebody who already has a Windows
     account, which **cannot work** — `sdusers` grants access to the files,
     login needs a linked SD account, so such a user is refused with `Account X
     not in register`, the exact symptom `don` had before step 1f. **Owner's
     decision, 15 Aug 2026: drop those lines**, rather than document `ADOPT`,
     which stays undocumented. Done, `sd.iss:493`, with a `changelog` entry.

     **AND READ ON SCREEN 17 Aug 2026, owner, on the 13:43:00 install:
     "looks fine".** So the source re-check below and the rendered dialog
     agree, and this bullet is closed. The `limitssh` paragraph below is not.

     **RE-CHECKED AGAINST SOURCE 17 Aug 2026 and it has stayed dropped:**
     `net localgroup` occurs in `sd.iss` at lines 67 and 926 **only inside
     comments recording why it went**, and nowhere in the string the closing
     `MsgBox` emits. Reading the whole box again found nothing else of that
     kind. **Grep the emitted string, not the file**, if this is ever checked
     again — the comments are the reason a plain grep looks alarming.

     **The `AllowGroups` task is still unseen** and cannot be seen here — it is
     hidden by `Check: SshServerAbsent` on this machine (header item 1). **It is
     no longer a subtask**: renamed `limitssh` and promoted on 16 Aug 2026 when
     its parent went (§5.9).
   - **CLOSED AND VERIFIED 17 Aug 2026 (§4) — `deny-logon.ps1`'s outcome is
     now checked, and the rights are confirmed applied.** It moved from
     `[Run]` to `ApplyDenyLogon` in `[Code]` at `ssPostInstall`
     (`sd.iss:691`), exit code checked, failure
     named in the closing `MsgBox`. **The script was never the problem** — it
     validates every `NTSTATUS` and throws, so its exit code always meant
     something; `[Run]` simply discarded it. Third such step fixed this session,
     after `SecureCredStore` and alongside the two the file already had.

     **Ordering: it now runs after the whole `[Run]` section instead of before
     the data-tree `icacls`, and that is safe** — the rights are held by the
     GROUP, so nothing already done depends on when they land, and it is called
     **before `AdoptAccount`**, so no SD account exists before the confinement.

     **No read-back here, deliberately:** confirming the rights afterwards needs
     `LsaEnumerateAccountRights`, and `verify-sshonly.ps1` already dumps and
     checks them. A second implementation would be a second thing to keep true.

     **Cost if it regresses:** an account in `sdsshonly` on a machine where the
     rights never landed is not confined at all — it can sign in at the console
     — and before this the install said nothing.
   - **THE MANDATORY-SSH PATH CANNOT BE TESTED ON THIS MACHINE**, which already
     has OpenSSH — `SshServerAbsent` is false here, so only the "already
     present, leave it alone" branch ever runs, and `sshremote` and `limitssh`
     are both hidden. Structurally the same hole as the `AllowGroups` task
     above. **It needs the VM from step 2** (`Windows 11 Clone`, snapshot
     `Before SD install`).
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
4. **BUILT AND VERIFIED 16 Aug 2026, thirteenth session**, on the fresh
   install of 12:18:42 (`assert-current` exit 0). `audit_message()` in
   `k_error.c`, reached from BASIC as `kernel(K$AUDIT, text)` (key 57,
   `keys.h` and `INT$KEYS.H`).

   **The trail after an install and one unelevated session** — the installer's
   own account step is the first line, the rest is `sd` run as `don`:

   ```
   12:18:55 user=don uid=1 pid=522 LOGIN account=SDSYS
   12:19:43 user=don uid=2 pid=529 LOGIN account=DON
   12:19:43 user=don uid=2 pid=529 LOGTO REFUSED account=SDSYS reason=session is not elevated
   12:19:43 user=don uid=2 pid=529 LOGTO account=DON
   ```

   **`GRANT`/`REVOKE` (step 5f) is the one path NOT yet observed** — it needs
   an elevated SD session and a second Windows user. Everything else above is
   measured.

   - **`<sysdir>/audit`, and it rotates rather than truncates.** At 1MB the
     file is renamed `audit.<yyyymmdd-hhmmss>` and a new one started, so SD
     never discards a record. Pruning is left to the site, deliberately.
   - **The caller passes what happened, never who did it.** The timestamp,
     username, uid and pid are stamped in C from `my_uptr`. §5.6 warns that
     `CPROC` reassigns `logname` on the drop to sdsys, so a trail that trusted
     the BASIC caller would attribute a step-up to the account being entered.
   - **Call sites.** `LOGIN` — success at its one `ok = @true`, refusal at its
     one `terminate.connection`, with an `audit.reason` set at each gate and
     defaulting to `unspecified` so a refusal added later still records.
     `CPROC` — `LOGTO` success after the move and the admin flag, refusal at
     all three gates including **the failed step-up** (SDSYS asked for by an
     unelevated session). `GRANTA` — `GRANT`/`REVOKE` after the group edit,
     which closes §7 step 5f.
   - Uses `ERRLOG_SEM` rather than a seventh semaphore: both are log writes,
     and `NUM_SEMAPHORES` is part of the shared segment layout (`sysseg.h`).
   - Silent on failure, deliberately — an unwritable audit file must not be
     what stops somebody logging in.

   **THE TRAIL IS APPEND-ONLY TO THE USERS IT RECORDS.** Owner's decision,
   16 Aug 2026 — *"admins are highly trusted, we are increasing security not
   maximizing it"* — so Administrators and SYSTEM keep `F` and this raises the
   floor against ordinary SD users only. `secure-audit.ps1`, run by the
   installer **after** the data-tree `icacls` (before it, inheritance puts
   `Modify` straight back), breaks inheritance and leaves `sdusers:(AD,RA,S)`.

   **Measured as an unelevated member of `sdusers`, all of it, 16 Aug 2026:**

   | operation | result |
   |---|---|
   | append a record | works |
   | read the file | refused |
   | truncate to nothing | refused |
   | overwrite a record in place | refused |
   | rename or delete | refused |

   **THIS IS WHY `win32audit.c` EXISTS**, and it is the second `windows.h`
   file after `win32sem.c`. `open(O_WRONLY|O_APPEND|O_CREAT)` **fails with
   errno 13** against that ACL: the MSYS2 runtime maps `O_WRONLY` to
   `GENERIC_WRITE`, which contains `FILE_WRITE_DATA`. Granting `WriteData` to
   make the POSIX open work hands back exactly what the ACL was for — measured
   with it, an ordinary user **can** truncate the trail and **can** overwrite
   individual records. `CreateFile` asking for `FILE_APPEND_DATA` alone works
   and the ACL can withhold everything else. **Do not "simplify" this back to
   `dio_open()`** — the first version of this step did exactly that, and
   because `audit_message()` is silent it would have lost every ordinary
   user's records without a word.

   **Rotation carries the ACL** (`win32_audit_rotate()`): a plain `rename()`
   leaves the next file to be created by the next writer, which inherits
   `Modify` — so the trail would silently become editable from the first
   rotation onwards. The DACL is read from the file being rotated away and
   re-applied `PROTECTED`. Measured: the new file matches the old exactly,
   with no inherited `(I)` entry. **Symptom if this ever breaks: `icacls` on
   `audit` shows an inherited `sdusers:(I)(M)`.**

   **VERIFIED ON THE INSTALLED SYSTEM, 16 Aug 2026 12:18–12:20**, install of
   12:18:42, `assert-current` exit 0. Every tampering route was tried **as
   unelevated `don`, a real `sdusers` member, against the real file**: read,
   truncate, overwrite in place, rename and delete were all refused and the
   file stayed at 287 bytes. Appending through SD worked throughout, and
   `icacls` itself is refused — `(AD,RA,S)` carries no `READ_CONTROL`, so an
   ordinary user cannot even read the permissions.

   **To re-run it:** `sd` unelevated, `LOGTO SDSYS` (expect the `LOGTO
   REFUSED` line), `LOGTO` your own account, `OFF`; then read
   `C:\ProgramData\SD\sdsys\audit` **from an elevated window** — an ordinary
   one cannot, which is the point, and is why this cannot be checked by a
   script running as the user it audits.
5. **CLOSED 16 Aug 2026, fourteenth session — (f) INCLUDED.** `GRANT
   account=SDACCT11 to=don` and `REVOKE account=SDACCT11 from=don` were watched
   reaching the audit trail at 14:48, from an unelevated session that had
   entered SDSYS; the Windows group was edited and correctly reverted.
   **`LIST.GRANTS` was broken the whole time and is fixed** — header item 1,
   defect 4. §4 has the original run, 16 of 16 on a fresh install. `GPL.BP/GRANTA` serves **`GRANT
   <account> TO <user>`, `REVOKE <account> FROM <user>` and `LIST.GRANTS
   <account>`** from one program behind three `VOC_TEMPLATE` entries; bare
   `GRANT <account>` lists too. `!os_group` gained `LISTMEM` (e). `ACC$USERS`
   is gone (d) and **field 4 is not reused** — records written 13–14 Aug still
   carry a grant list there and an installed tree is never upgraded.

   **(f) IS THE ONE THING LEFT AND IT IS BLOCKED**: the audit record wants
   step 4's file, which does not exist. `GRANTA`'s header names it as one of
   that file's first callers. Windows logs the group edit meanwhile, so the
   change is not unrecorded — only SD's half of it is.

   **The original statement of the step follows, because the reasoning is
   still the specification.**

   Entry to an account is membership of the group named in its
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
6. **CLOSED 17 Aug 2026, NINETEENTH SESSION — THE API WORKS END TO END.**
   Verified on the 17:09 run of `gplbld/verify-apiport.ps1 -Prefix sdapi2`
   against the 16:5x install: a remote session opened over the loopback port,
   **the wrong password was refused by `!CRED_VERIFY` (6a) and SDSYS by the
   `ACC$GROUP` test (6c)**, with different messages, which is what makes the
   admitted case mean anything. 6b follows from 6a, and 6d went with
   `login_user()`.

   **What is left of step 6 is nothing blocking.** The transport is loopback
   TCP with ssh carrying it (posture B), `APIPORT` defaults off, and the
   listener lives in `sdwind`. The sub-steps below are kept because they record
   what each cost and what to look at if any of it regresses.

   **The original statement follows, because the reasoning is still the
   specification.**

   **Bring the API server under the same model** — and it is more pressing
   than this position suggests, because §1 now says the API is the product's
   front door. **The API does not work on Windows at all**: `APISRVR` line 921
   calls `login(username, password)` → `login_user()` in `linuxio.c`, which
   with `APILOGIN=1` reads `/etc/shadow`, which MSYS2 does not have. It fails
   closed, which is the good version of broken, but it is broken. The shape of
   the work, in value order:

   **THE REMOTE TRANSPORT: A NATIVE LISTENER HANDING THE ACCEPTED SOCKET TO AN
   MSYS2 CHILD CANNOT WORK. MEASURED 17 Aug 2026, WITH A CONTROL.** This was
   the option worth checking before building anything, because it would have
   kept the traffic off a TCP port any local process can reach. It is closed.

   A native parent accepts a loopback connection and passes the accepted
   `SOCKET` to a Cygwin child as its **standard input**, the way step 11's
   working local transport passes pipes. The child agrees it is a socket and
   can write to it — **and cannot read a byte of it**:

   | stdin | pending pre-spawn | `getsockname(0)` | `send(0)` | `select()` | read |
   |---|---|---|---|---|---|
   | pipe (CONTROL) | — | FAIL `ENOTSOCK` | FAIL | 0 | — |
   | pipe (CONTROL) | — | FAIL `ENOTSOCK` | FAIL | **1** | **OK** |
   | SOCKET | 0 bytes | OK `AF_INET` | OK | 0 | `EAGAIN` |
   | SOCKET | **13 bytes** | OK `AF_INET` | OK | **0** | **`EAGAIN`** |

   **The bottom row is the finding.** The parent proves with
   `ioctlsocket(FIONREAD)` that 13 bytes are pending **before the child
   exists**, so "the child saw nothing" cannot be "nothing was sent". Both
   `select()` and non-blocking `recv()` report empty.

   **The control is the same descriptor number in a separate run** — swap the
   socket for a pipe and the payload arrives. Two earlier versions of this
   harness were wrong and the control caught both: sending only *after*
   spawning (measuring a channel nobody had written to), and using `hStdError`
   as the control (an OUTPUT handle, so Cygwin builds fd 2 write-only and a
   read-select can never fire).

   **Why, and why the other route is closed too.** A socket is not passed
   between processes by handle inheritance — Windows documents
   `WSADuplicateSocket()` for it. The handle is real enough for `getsockname`
   and `send`, which go straight to the kernel object, but the receive path
   stays bound to the originating process's Winsock context. And the
   `WSADuplicateSocket` route needs the rebuilt socket injected into Cygwin's
   descriptor table — `cygwin_attach_handle_to_fd()`, which is the
   **always-ready** path step 11 measured and rejected. **Both routes are shut
   by measurement, not by argument.**

   **So the listener belongs on the Cygwin side**, where `sdwind` already is:
   MSYS2, already the persistent daemon, so it can `accept()` and fork+exec
   `sd -n -q` with the socket on descriptor 0 exactly as xinetd does on Linux,
   with no Windows novelty in the path at all. That needs `start_connection()`'s
   `PF_INET` branch, which currently `return FALSE`s — upstream narrowed it to
   AF_UNIX in Feb 2024, and the peer identity that narrowing bought
   (`getpeereid`) is precisely what (a) below replaced with `$CRED`.

   **The probe is kept and is one command** — `make check-sock-probe` from
   `gplsrc/sdclilib`, sources at `tests/sock_probe_{parent,child}.c`, beside
   step 11's `select_probe_*.c`. It reproduces all four cells above.

   **BUILT 17 Aug 2026, NINETEENTH SESSION, AND NOT RUN.** Everything below
   compiles clean and no part of it has been exercised; the install of
   13:43:00 predates it. **`APIPORT` DEFAULTS TO OFF**, so a fresh install
   still opens no port and the cycle will not test the listener unless the
   conf is edited — see "how to test it" below.

   - **`APIPORT=<port>` is the new configuration parameter**, `struct CONFIG`
     → `SYSSEG` (`config.h`, `config.c`, `sysseg.h`, `sysseg.c`), readable as
     `CONFIG('APIPORT')` (`op_config.c`). **It is in the segment, not `PCFG`**,
     because `sdwind` is what reads it and `sdwind` loads no per-process
     config. Zero means no listener, which is what a `memset` of the struct
     already gives — there is deliberately no fallback to 4243.
   - **The listener is in `sdwind`** (`open_api_listener()`,
     `accept_api_session()`), because it is the one process SD already keeps
     running. **Bound to `INADDR_LOOPBACK` and not configurable** — posture B
     says nothing of SD's own faces the network, and a bind address in a conf
     file is a way to get that wrong by accident.
   - **The main loop now waits on `select()` and drives its minute timer from
     the CLOCK**, not from the iteration count. It had to change: `select()`
     returns as soon as a connection arrives, so counting iterations would run
     `check_lost_users()` once per API connection.
   - **Children are reaped in the loop, not in a `SIGCHLD` handler.**
     `SIG_IGN` would auto-reap and then make `system()` in `check_lost_users()`
     fail with `ECHILD`.
   - **`start_connection()` accepts `PF_INET` again** (`linuxio.c`), with the
     reversal argued in the code comment. `peer_usr_id`/`peer_grp_id` are
     **left unassigned** rather than filled in plausibly: nothing downstream
     may treat a TCP peer as an authenticated OS user.
   - **The commented-out upstream `PF_INET` block could never have compiled** —
     it names `MAX_IP_ADDR_STR_LEN`, which is defined nowhere in the tree. The
     buffer is `MAX_SOCKET_ADDR_STR_LEN` (109, `sddefs.h:250`).
   - `sd.conf` carries `#APIPORT=4243` commented out with the reasoning, and
     the `changelog` has the user-facing entry.

   **HOW TO TEST IT, and it needs more than the cycle.** A fresh install opens
   no port, so: run the cycle, then add `APIPORT=4243` to
   `C:\ProgramData\SD\sd.conf`, then **restart SD** — `read_config()` runs
   only when the segment is created (§7 step 1a), so a running system will not
   pick it up. Then check `netstat -an | findstr 4243` shows a **127.0.0.1**
   listener and not `0.0.0.0`, and drive it with the client library.
   **`SDConnect()` is the call, not `SDConnectLocal()`** — and it is the only
   path that reaches step 6a's `$CRED` check, because `SrvrLocalLogin` sends no
   password. **Expect the same control as step 11**: an account the user is
   granted admitted, `SDSYS` refused.

   **THE `$CRED` FILE WAS NEVER CREATED BY ANYTHING, AND `SET.PASSWORD` HAS
   THEREFORE FAILED ON EVERY INSTALL EVER MADE** — `Cannot open the $CRED
   register`, measured 17 Aug 2026 on the 16:45:49 install. Nobody saw it
   because §5.6 left the credential machinery callerless and no VOC pointed at
   `SET.PASSWORD` until that morning. `stage.py` listed `$CRED` among the files
   "the bootstrap and the running system create for themselves" and **that
   comment was wrong**: `sd -i` creates `VOC`, `VOC.DIC`, `ACCOUNTS.DIC`,
   `$MAP` and `DICT.DIC` and no more, and `CRED_SET` opens without creating.

   **FIXED: it is staged as a directory file** (`SDSYS_EMPTY`, the same shape
   as `ACCOUNTS` — an empty directory is one) **and locked by
   `gplbld/secure-cred.ps1`**, which the installer runs after the data-tree
   `icacls`, like `secure-audit.ps1` and for the same ordering reason.

   **THE LOCK DID NOT ACTUALLY TAKE UNTIL 17 Aug 2026, TWENTIETH SESSION.** The
   call was quoted for `-Command` and made with `-File`, so it secured nothing
   and said nothing. Header item 1 has the measurement, the fix and the
   discriminator; `gplbld/verify-credacl.ps1` is the check that did not exist.
   **Both halves of this step are now closed and observed.**

   **SYSTEM AND ADMINISTRATORS ONLY. `sdusers` GET NOTHING** — owner's ruling,
   17 Aug 2026. **The risk is writing, not reading**: `$CRED` holds a salt and
   an **Argon2 verifier**, never a password (`INT$KEYS.H:263`), so reading one
   is worth little — but inherited `Modify`, which is what the data tree grants
   and what `$MAP` demonstrably has, would let any SD user **overwrite another
   account's verifier** with one derived from a password they chose and then
   authenticate through the API as that account. A straight escalation.

   **THE FILE SHAPE IS NOT A CONTROL.** A dynamic file would put the same bytes
   in `%0`; `VOC` and `$MAP` are dynamic and plainly greppable. The ACL is the
   whole of the protection.

   **WHO CAN STILL REACH IT — the service account decides this, and it was
   checked rather than assumed: `Win32_Service` `StartName` is `LocalSystem`.**
   So `sdwind` forks `sd -n -q` children that read `$CRED` as **SYSTEM**, and
   the API path works under the tight ACL. An elevated administrator running
   `SET.PASSWORD` works. **An ordinary console user cannot**, deliberately —
   and that is consistent with `SET.PASSWORD` being an administration verb.
   **The corollary is worth knowing before somebody tries it:** copying
   `SET.PASSWORD` into a user's VOC will not work at the file layer until
   §5.7's service model lands. The program permits it, the ACL does not.

   **AND THE API GATE HAS NO ELEVATION BYPASS — checked, because a SYSTEM-owned
   session could plausibly have had one.** `APISRVR:449` tests
   `is_grp_member(kernel(K$USERNAME,0), acc.group)`, the **verified username**,
   not the process token, so SDSYS stays refused however privileged the process
   is. That is exactly why 6c insisted the identity come from `K$USERNAME`.

   **A TRAP IN THE INSTALLER ENTRY, and it would have failed silently:** the
   path is **single quoted**, unlike every other entry in `sd.iss`, because
   PowerShell **expands `$CRED`** inside a double-quoted string. Undefined, so
   `-Path` would have become `...\sdsys\` and the store would have been left
   wide open with the step reporting success.

   **The old statement of the blocker follows.**

   **NOTHING COULD SET AN ACCOUNT PASSWORD.** `APILOGIN=1` makes `APISRVR` call
   `!CRED_VERIFY`, and `APISRVR:1002` says it plainly: *an account that has
   never had a password set cannot be reached*. **`GPL.BP/SET_ACC_PASSWORD`
   exists and NO VOC ANYWHERE POINTS AT IT** — checked, both `VOC_TEMPLATE`
   and `NEWVOC`, and nothing references `SETPASS` or `SET_ACC_PASSWORD`. So
   there is no `SET.PASSWORD` verb at any tier and no way to give an account
   the credential the API demands.

   **This is §5.6's "callerless" note coming due.** Taking passwords off the
   console login left `$CRED`, `!CRED_SET`, `!CRED_VERIFY` and
   `SET_ACC_PASSWORD` with no caller, and they were kept precisely because the
   API would be their caller (§8). The API half now exists; the half that
   writes the credential still has no door.

   **ANSWERED AND BUILT 17 Aug 2026 — `SET.PASSWORD` IS AN ADMINISTRATION
   VERB, THE TENTH.** Owner's ruling: *"the administrator can always remove it
   from the exclusion list if they want users to set their own"*. So the verb
   is placed, not gated — `VOC_TEMPLATE/SET.PASSWORD` (`V`/`CA`/`$SET.PASSWORD`)
   plus `SET.PASSWORD` in `NEWVOC/TIER.ADD.ADMINISTRATOR`, and nothing in the
   program changed.

   **DO NOT ADD A WHOLESALE `K$ADMINISTRATOR` GATE TO IT.** The program already
   tells the two cases apart — `SET_ACC_PASSWORD:69` refuses somebody else's
   account without admin rights, `:109` demands the current password for your
   own — so an administrator who copies the verb into a user's VOC gets exactly
   the behaviour the ruling describes. A blanket gate would make that copy do
   nothing, which is the opposite of the decision.

   `APILOGIN=0` is NOT an alternative test route: it skips the password by
   design and so tests nothing of 6a.

   **Installed and verified 17 Aug 2026** on the 16:28:43 install:
   `verify-tiers.ps1 -Prefix sdtierc` passed every check, `COUNT VOC` 421 on
   the derived figure, and `SET.PASSWORD` read directly out of the account VOCs
   is present for ADMINISTRATOR and absent for STANDARD and PROGRAMMER.

   **THE TEST HARNESS IS BUILT AND HAS NOT BEEN RUN** — one elevated command:

   ```
   gplbld\verify-apiport.ps1 -Prefix sdapi1
   ```

   It creates a throwaway account, sets a **generated** password on it (never
   hardcoded, never on a command line, delivered on stdin — the section 5.6.1
   rule), adds `APIPORT` to the installed `sd.conf`, **restarts SD** because
   `read_config()` runs only when the segment is created, asserts the listener
   is on **127.0.0.1 and not 0.0.0.0**, drives the client, and puts all of it
   back in a `finally` block. `-Keep` leaves it standing.

   **The client half is `make check-remote`** (`tests/remote_connect_test.c`),
   and it carries THREE cells:

   | cell | expected | what it proves |
   |---|---|---|
   | right password, granted account | admitted | the transport carries a session |
   | **WRONG password, same account** | **refused** | **`$CRED` actually ran** |
   | right password, `SDSYS` | refused | the `ACC$GROUP` check ran |

   **The wrong-password cell has no precedent anywhere in this project** —
   `SDConnectLocal` sends no password, so nothing has ever reached
   `!CRED_VERIFY`. If it is admitted, everything else the test says is
   worthless, and `APILOGIN=0` is the first thing to suspect.

   **Two defects were found by running it rather than reading it**, both in the
   harness: unescaped backslashes in a diagnostic (three warnings, and the
   message printed mangled), and `APIHOST` passed through as empty from the
   top-level Makefile, which **overrides a `?=` default rather than leaving it
   alone** — the test was handed an empty host and answered `Invalid host
   name`, which reads as a broken listener.

   **`verify-apiport.ps1` is in `assert-current`'s `$neverShipped` list**, or it
   would refuse to run because of its own existence — the trap that list was
   added for.

   **A CYCLE IS OWED BEFORE IT CAN RUN**, for `remote_connect_test.c` and the
   sdclilib Makefile. Neither ships; `gplsrc` is watched and the guard is
   deliberately blunt. `make sd` is not needed.

   a. **DECIDED 16 Aug 2026 — `$CRED`, not `LogonUser`.** Owner's call when
      asked; the alternative was authenticating the Windows account itself,
      which matches Linux more closely but puts a real Windows credential on
      the wire and inside SD. `$CRED` keeps it out. **Not built yet**, but the
      shape is settled and the awkward part is already solved:

      **The obstacle is not the checking, it is setting the identity
      afterwards.** `!CRED_VERIFY` is BASIC and `APISRVR` can simply call it,
      but the session identity — `process.username` and `my_uptr->username`,
      which is what `@logname`, `K$USERNAME` and **the audit trail** all read —
      is set in C by `op_login()` (`op_kernel.c:760`), and `K_USERNAME` is
      **read-only** (`op_kernel.c:233`). There is no route from BASIC.

      **Do it the way `K_ADMINISTRATOR` already does it**, which is the
      precedent and keeps the audit trail honest: make `K_USERNAME` settable
      **only when `process.program.flags & HDR_INTERNAL`**
      (`op_kernel.c:325`). Ordinary BASIC cannot reach `KERNEL` at all — BCOMP
      rejects it — and **`APISRVR` is `$internal`** (line 59), so it can. A
      plain settable `K_USERNAME` would let any program rewrite the identity
      the trail is stamped from, which is exactly what §7 step 4 stamps in C
      to prevent. **Do not skip the gate.**

      **The edits, in order:** `op_kernel.c` gate-and-set `K_USERNAME`;
      `APISRVR:921` swap `login(username, password)` for `!CRED_VERIFY` plus
      `kernel(K$USERNAME, username)`; gut `login_user()` in `linuxio.c` so
      nothing reads `/etc/shadow` (this closes **6d** with it, the
      `setuid`/`setgid` going the same way); drop `PASSWD_FILE_NAME` from
      `sdnet.h` and the prototype from `sd.h`. **`APISRVR:921` is the ONLY
      caller of the `login()` intrinsic** — checked; `LOGIN:60` is an
      unrelated subroutine of the same name. **Retire the opcode in place if
      you retire it at all** (§6): `OP_CF0A` is positional, and `BCOMP`'s
      `int.intrinsics` and its `on i goto` list are matched to it by position,
      so leaving the slot alone is much the safer course.

      **BUILT 17 Aug 2026, COMPILED 17 Aug 2026, AND NOT RUN — §4 Not
      verified.** `make sd` clean after `rm -f gplobj/*.o`, no warnings, and
      `SECOND.COMPILE` accepted the BASIC on the 06:07:30 bootstrap (§4 has the
      object sizes). There is no API client on this machine, `SDConnectLocal()`
      has never been exercised (step 11), and the transport the Linux client
      uses **cannot work here at all** (§8, measured 16 Aug), so nothing can
      call it yet.

      **A DEFECT WAS CAUGHT IN THIS DESIGN BEFORE IT WAS WRITTEN, and it is
      why the key is a new one.** The first plan was to make `K_USERNAME`
      settable. **It would have renamed the session to `"0"`:** the two
      readers, `APISRVR:125` and `CPROC:273`, both call
      `kernel(K$USERNAME, 0)`, and `k_get_c_string()` renders that integer as
      the string `"0"` — non-empty, so a "set if non-empty" rule fires, and
      `HDR_INTERNAL` does not save it because APISRVR is `$internal`. **A new
      key cannot break a reader.** `K_SET_USERNAME` / `K$SET.USERNAME` is 60,
      the first free number in both `keys.h` and `INT$KEYS.H`.

      **What went in:** `K_SET_USERNAME` in `op_kernel.c`, gated on
      `HDR_INTERNAL` and setting both `process.username` and
      `my_uptr->username`; `APISRVR:940` calling `!CRED_VERIFY` and then
      `kernel(K$SET.USERNAME, username)`; **`login_user()` deleted** from
      `linuxio.c`, which closes **6d** — its `setgid`/`setuid` went with it;
      `PASSWD_FILE_NAME` out of `sdnet.h` and the prototype out of `sd.h`;
      and **`op_login()` left in place as a fail-closed stub**, because
      `opcodes.h` is positional and `BCOMP`'s `int.intrinsics` is matched to
      it by position (§6).

      **The BASIC has NOT been through a compiler** — `bbcmp.py` builds only
      the bootstrap seed, so `APISRVR` is first compiled by `SECOND.COMPILE`
      during the next `stage.py --bootstrap`, which dies loudly on an error.
      Both new statements were checked against existing usage instead:
      `call !CRED_VERIFY(...)` matches `SET_ACC_PASSWORD:113`, and
      `void kernel(...)` matches `AUTOLOGOUT:58`.
   b. **DONE 17 Aug 2026, as a consequence of (a).** `@logname` no longer
      comes from the client's assertion: `vb.login` sets `logname` and
      `K$SET.USERNAME` from the name `!CRED_VERIFY` was given, so the identity
      exists only if verification passed. **`APILOGIN=0` is unchanged and is
      not a gap** — that path deliberately takes the identity from the ssh
      tunnel that already authenticated, and checks no password here.
   c. **BUILT 17 Aug 2026, seventeenth session, AND NOT COMPILED OR RUN.**
      `vb.account` applies the `ACC$GROUP` membership test, refusing an account
      whose group field is empty rather than guessing `sdu_<name>` (step 5a's
      rule). **Read the block comment in `APISRVR` before touching it** — it
      records the three things that were decided rather than defaulted:

      - **Only the group test transfers from `logto.authorised`**; its other
        three gates describe session state an API session cannot have, so
        they are dead weight rather than a hazard. **Read them with §6's "two
        internals" trap in hand** — an earlier draft of this step asserted
        that `K$INTERNAL` was permanently true here because `APISRVR` is
        `$internal`, and that is wrong: they are different flags.
      - **The identity is `kernel(K$USERNAME,0)`, not the local `logname`**,
        which holds the same value today. `K$USERNAME` reads
        `process.username`, which is what `audit_message()` stamps in C. A
        grant check that could disagree with the trail about who acted would
        make the trail worthless.
      - **SDSYS is refused through the API and that is intended.**
        `ACCOUNTS/SDSYS` carries `ACC$GROUP = sdsys`, not a Windows group
        (§6), so the test answers false. Administration needs elevation and
        an API session cannot have it.

      **The refusal reuses `sysmsg(10003)`**, the missing-account message, so
      a caller cannot tell "no such account" from "not granted" and the API
      does not enumerate accounts.

      **Nothing has compiled this** — same position 6a was in before the last
      cycle, and the next `stage.py --bootstrap` is its first compiler.
      `is_grp_member` starts PowerShell, which its own header flags as slow on
      a per-login path; that cost now lands on every API account switch too.
   d. **Delete the `setuid`/`setgid` calls in `login_user()`.** SD accounts are
      not OS users under §5.6, and they are largely no-ops on MSYS2 anyway.
      They go with the rest of the OS-account work.

   `sdnet.h` still hardcodes `PASSWD_FILE_NAME "/etc/shadow"`, which is what
   that authentication used to be, and goes with (a).
7. **BUILT, INSTALLED, AND HALF VERIFIED — 17 Aug 2026, twentieth session.
   `SH` is permitted by a list, not by elevation.** On the 22:43:52 install
   `CPROC` compiled, `WRITE_INSTALL_DICTS` wrote all five `OS.USERS.DIC`
   records, the ACL took, and an unlisted account is refused with message
   10053 (§4).

   **THE ADMIT PATH IS VERIFIED — `gplbld/verify-osusers.ps1`, 18 of 18, exit 0
   on the 07:00:00 install of 18 Aug 2026.** §4 has the table and what each row
   is for. The `changelog` entry it was waiting on is written.

   **THE SCRIPT RUNS UNELEVATED AND PROMPTS FOR UAC TWICE ITSELF.** The
   measurement must not be elevated or `CPROC:3448` admits it on
   `K$ADMINISTRATOR` and `OS.USERS` is never consulted; writing the record and
   removing it again must be, because that ACL is the whole protection. The two
   halves cannot share a token, and elevating is the easy direction.

   **IT IS EXEMPT FROM `assert-current`'s STALENESS GUARD** — added to
   `$neverShipped` (`assert-current.ps1:88`) with the other verifiers, or
   editing the test would demand a reinstall to re-run the test. That list is
   self-policing: a name that turns up quoted in `stage.py` or `sd.iss` is put
   back under the guard.

   **THE PROBLEM IT SOLVES (§8).** The gate at `CPROC`'s `os.command:` label
   admitted only `K$ADMINISTRATOR`, which is `IsElevated()`, and an ssh session
   can never be elevated — so programmers, the one group that needs a shell,
   were the one group that could never have one. Meanwhile `OS.EXECUTE` stayed
   ungated for everybody. The visible control was denied to the people who
   needed it and the capability it guards was open to those who did not.

   **WHAT WAS BUILT:** `@SDSYS/OS.USERS`, a directory file, **one record per
   account**, keyed by account name. Field 1 `SH`, field 2 `OS.EX`, each `yes`
   or anything else. Dictionary `OS.USERS.DIC` with `Name` (D 0), `SH` (D 1),
   `OS.EX` (D 2), plus `@ID` and an `@` default listing, shipped as source in
   `gplbld/FILES_DICTS` and written at bootstrap by `WRITE_INSTALL_DICTS`.
   Both files are staged empty by `stage.py` — **`WRITE_INSTALL_DICTS`
   `OPENPATH`s the dictionary rather than creating it**, so if it were not
   staged the entries would be skipped and the file would ship with no
   dictionary. Admin edits with `ED` from SDSYS. New message 10053.

   **NOT IN `NEWVOC`, and that was reconsidered mid-design.** The tier lists
   live there because `CREATEA` already has it open (`CREATEA:593`); `CPROC`
   does not, so the saving vanishes. Worse, everything in `NEWVOC` is copied
   into every account's VOC unless excluded in **two** places, and the tier
   lists' fail-safe is *permissive* — a missing record means the FULL VOC.
   A permission list needs the opposite default and must not inherit that
   convention.

   **THE ACL IS THE ENTIRE CONTROL.** `gplbld/secure-osusers.ps1` grants
   `sdusers` **(RX) — read, not modify**, which is the difference from
   `secure-cred.ps1`: `CPROC` reads the list from the user's own process, so
   they must read it and must never write it. Called from `[Code]` as
   `SecureOsUsers`, **exit code checked**, failure named in the closing box.
   Without it any SD user adds their own name and the file is decoration —
   exactly what happened to `$CRED`.

   **ELEVATION STILL PASSES ON ITS OWN**, deliberately: an empty `OS.USERS`
   must not lock the machine's own administrator out of `SH`, which is the
   lockout `ADOPT` caused with `sdsshonly` on 15 Aug 2026.

   **The metacharacter ban is lifted for a listed account only** (owner). An
   elevated session that is not listed keeps `!valid_shell_cmd` exactly as
   before, so this adds capability and regresses nothing.

   **WHAT IS NOT DONE, AND IT IS HALF THE FEATURE.** **Field 2 `OS.EX` is
   stored, dictionaried and read by nobody.** `OS.EXECUTE` is a BASIC
   statement compiling straight to `OP.SH`/`OP.SHCAP` into `op_sh.c`, never
   touching `CPROC`, so gating it needs **C**: two bits beside `USR_ADMIN`
   (`sysseg.h`, `0x0100` and `0x0200` are free), a kernel key gated on
   `HDR_INTERNAL` as `K$ADMINISTRATOR` is — or a programmer sets the bit
   themselves — `LOGIN` seeding them, and a check in `sh()`. Until then an
   unlisted programmer with `BASIC` still has full OS access from a program,
   so **this is an auditable permission record, not yet a boundary**.

   **Note `SH` implies `OS.EX` and cannot not**: `CPROC:3465` runs the verb by
   calling `os.execute`, so the two flags are not independent in that
   direction. The useful combination is `OS.EX` yes with `SH` no — programs may
   shell out, the person at the prompt may not.

   **Owner wants a form for account setup with these privileges** eventually
   (§5.14); `ED` is the interim editor.

   *(A "NOT COMPILED" paragraph stood here and was wrong by the time it was
   written — the 22:43:52 cycle compiled `CPROC`, as this step's own first line
   says. Removed 18 Aug 2026.)*

8. **Make everything lower case that can be** (§5.12). **STARTED 17 Aug 2026,
   twentieth session: the file-name half is done in source and NOT VERIFIED.**

   **`CASE_INSENSITIVE_FILE_SYSTEM` IS NOT ONE THING, AND THAT IS THE FINDING.**
   9 sites, defined nowhere — **and never defined in `../sdb64` either**, so it
   is dead in both trees and there is no upstream defect (on a case-sensitive
   Linux filesystem, off is correct). The 9 split into two **competing
   strategies** for the same problem, and only one can be right:

   a. **`dh_open.c:529` — make the COMPARISON case insensitive.** One site.
      Sets `DHF_NOCASE` on directory files. **This is the one that was taken.**
   b. **The other 8 — normalise every path and id to UPPER case** so that
      case-sensitive comparisons agree with the filesystem: `dh_misc.c:143`,
      `op_dio2.c` at 634 (`!OSPATH` input), 726 (`OS_CWD` output), 788
      (directory listings), 916 and 928 (both `OSRENAME` paths), `op_dio4.c`
      1154 and 1285 (`SELECT` over a directory file). **Left off, because
      §5.12 chose lower case** — upper-casing every path is the opposite of
      the goal, and it is user-visible: `OS_CWD` would start answering
      `C:\PROGRAMDATA\SD`. It also buys nothing on Windows, where the
      filesystem already matches case-insensitively without being asked.

   **DEFINING THE MACRO WOULD THEREFORE HAVE BEEN WRONG** — it would have taken
   (a) and (b) together. (a) is now unconditional instead, per CLAUDE.md's rule
   against `#ifdef` branches, and the macro name now governs only (b).
   `op_dio4.c:1155` already guards on `Option(OptSelectKeepCase)` and
   `op_dio4.c:1285` does not, so (b) is not even internally consistent.

   **WHY (a) MATTERS:** a directory file's record ids **are** file names, and
   NTFS resolves `SUE` and `sue` to one file — so without it SD takes **two
   record locks** (`op_lock.c:996`) and **two transaction cache entries**
   (`txn.c:302`) on what is one file. It does **not** change reads or writes:
   `dir_read`/`dir_write` open by name and NTFS was already case insensitive.

   **Nothing is persisted by it.** Directory files have no header, so the flag
   lives only in the shared `FILE_ENTRY`; dynamic files still take theirs from
   disk (`dh_open.c:549`). No format change, nothing to migrate, and it cannot
   corrupt an existing database.

   **VERIFIED 17 Aug 2026 on the 20:10:31 install — `DIRFILE=1`, `DHFILE=0`,
   `gplbld/verify-nocase.ps1` exit 0, unelevated.** §4 has it. The measurement
   is one command, no account creation, nothing to clean up by hand.

   **CORRECTION, same session:** this entry first said the decisive observable
   was a lock on `sue` colliding with one on `SUE` and so "needs two concurrent
   sessions". **That was wrong, and it confused the change with its
   consequence.** What this port changed is whether `DHF_NOCASE` is *set*;
   `op_lock.c` has honoured the flag since long before the port. So the
   decisive reading is `FILEINFO(f, FL$NOCASE)` — one session, one account.

   **THE DYNAMIC FILE IS THE CONTROL.** A directory file answering 1 proves
   nothing alone; `VOC` takes its flags from its own header (`dh_open.c:549`),
   untouched here, so it must still answer 0. One moves, one does not.

   **BEFORE, measured by hand on the 17:36:21 install** (pre-change binary):

   ```
   DIRFILE=0     BP,  a directory file      -> must become 1
   DHFILE=0      VOC, a dynamic file        -> must stay   0
   ```

   **The probe is placed by writing a file, not by driving `ED` through a
   pipe** — `BP` *is* a directory file, so a record is just a file on disk.
   That trick is what makes this cheap, and it is worth remembering for any
   future test that needs BASIC on an installed system.

   **`changelog` ENTRY WRITTEN 17 Aug 2026, once the flag was observed.**

   **IT DESCRIBES THE LOCK COLLISION, WHICH IS INFERRED AND NOT OBSERVED — be
   straight about that if it is ever queried.** What was measured is that the
   flag is SET. That locks then collide follows from `op_lock.c:996`, which
   case-folds the id with `memucpy` when the flag is on, so two sessions
   locking `sue` and `SUE` produce one folded id and one lock entry. Sound, and
   still a reading of source rather than a measurement. A two-session `READU`
   test is the thing that would close it.

   **THE BASIC LAYER HAD THE SAME DEFECT AND IT IS NOW FIXED AND VERIFIED —
   17 Aug 2026, 20:34:04 install, behaviour as well as flag (§4).** `op_sys.c` `case 91` (`SYSTEM(91)`, "Windows?") answered
   **0**, inherited from `sdb64` where it is correct, so every BASIC program
   asking whether it is on Windows was told no — on Windows. Now 1.

   **What that actually broke:** `QPROC:82` reads it into `is.windows` and
   `QPROC:499` is `if is.windows and is.dir then is.case.insensitive = @true`
   — **the only route** by which the query processor treats a directory file's
   ids as case insensitive. `FL$FLAGS` cannot supply it: `op_dio2.c:439`
   answers `FL_FLAGS` only when `(dynamic && internal)`, and a directory file
   is neither, so `QPROC:498` reads 0 for one however the flag is set. **So
   `SELECT ... WITH @ID = "sue"` never matched record `SUE`**, and the code to
   make it match has sat there unreachable.

   **Same shape as `CASE_INSENSITIVE_FILE_SYSTEM`**: correct code, already
   written, never switched on. `is.case.insensitive` upper-cases both sides of
   a comparison only (`QPROC` 4034, 4447, 7059, 7198) and stores nothing, so it
   is the same strategy as (a) and not the upper-casing §5.12 rejected. The
   only other reader, `APISRVR:954`, is commented out. **`ISWIN` moved 0 → 1
   across the two installs and the `SELECT` behaviour was measured with its
   control; `verify-nocase.ps1` carries the row.** `changelog` entry written.

   **THE TERMINAL HALF IS NOT STARTED, AND THE EVIDENCE CONTRADICTS THE
   SOURCE. DO NOT CHANGE IT UNTIL THAT IS RESOLVED.** `case_inversion` is XOR
   `0x20` — true inversion, not force-upper (`op_tio.c:1133`) — and **three**
   places set it TRUE, not the one §5.12 implies: `linuxio.c:240`
   (`start_connection`), `linuxio.c:313` (`init_console`) and `LOGIN:266`.
   `LOGIN:266` is **unconditional** — the `if/else` opened at 233 closes at
   264 — and LOGIN demonstrably runs, because `WHO` answers `2 DON`.

   **Yet `SYSTEM(1001)` reads 0.** Measured repeatedly, 17 Aug 2026, on the
   20:34:04 install. Something either does not run or resets it, and which is
   not known. **A change made on top of this would be a change made on top of
   a contradiction.**

   **18 Aug 2026 — THE THING THIS STEP SAID TO ESTABLISH FIRST IS ESTABLISHED:
   INVERSION IS OFF FOR THE SESSIONS REAL USERS GET, AND THAT IS WHAT §5.12
   WANTS.** On the 07:28:34 install, three independent readings agree:

   ```
   SYSTEM(1001)                      0          op_sys.c case 1001
   PTERM DISPLAY                     Off        op_pterm, a different opcode
   SH New-Item -ItemType File ...    ran        mixed case reached PowerShell
   ```

   **The third is the one that settles it.** The `verify-osusers.ps1` probes
   send a mixed-case command through the input path; with inversion on it would
   have arrived as `nEW-iTEM -iTEMtYPE fILE`, and instead it created its marker.
   That is behaviour, not a flag reading, and it cannot be an instrument fault.

   **So the terminal half is a DEAD-SETTER cleanup, not a behaviour change.**
   SD accounts are ssh-only and ssh gives SD piped stdin, so 0 is the reading
   for every account that can log in. Nothing has to change for §5.12; removing
   the three setters is tidying.

   **RESOLVED, 18 Aug 2026, AND IT IS CONFIGURATION RATHER THAN A DEFECT: THE
   VOC `LOGIN` PARAGRAPH TURNS IT OFF AFTERWARDS.** `NEWVOC/LOGIN` is a `PA`
   record, copied into every account VOC, and it reads:

   ```
   PA
   TERM LINUX
   TERM 120,36
   PTERM CASE NOINVERT      <- this line
   ```

   `CPROC:397` runs it at session start and **`CPROC:2701` runs it again on
   every `LOGTO`**. So `LOGIN:266` does execute and does set the flag TRUE;
   the paragraph runs later and wins. Confirmed live with `CT VOC LOGIN`.

   **SO THE SETTERS ARE NOT DEAD, THEY ARE OVERRIDDEN — and the previous
   entry's "dead-setter cleanup" was wrong.** Nothing in C or in `$LOGIN`
   needs removing, and **the authoritative place to change this behaviour is
   the paragraph**, in `NEWVOC/LOGIN` and `VOC_TEMPLATE/LOGIN`. Inversion
   being off is deliberate and shipped, which is what §5.12 wants, so **§7
   step 8's terminal half needs no work at all.**

   **THE VISIBLE PROOF, worth keeping because it is how this was cracked:**
   with inversion on, an upper-case command echoes back lower case.
   `PTERM CASE INVERT` then `LOGTO DON` echoed as `logto don`, and the command
   after it echoed upper case again — so the flag was on, `LOGTO` turned it
   off, and no banner appeared, meaning `$LOGIN` had not re-run.

   **LINE 2 IS NOW `TERM VT100`, owner's decision 18 Aug 2026** — it said
   `TERM LINUX`, inherited from the Linux original, and `TERM` confirmed the
   session device really was `linux`. Changed in `NEWVOC/LOGIN` and
   `VOC_TEMPLATE/LOGIN`, **byte-for-byte** (`TERM LINUX` and `TERM VT100` are
   both 10 characters, so no record framing moved — and the two files differ,
   `NEWVOC/LOGIN` having no trailing newline where `VOC_TEMPLATE/LOGIN` has
   one). `vt100` is shipped in SD's own terminfo and `TERM VT100` was checked
   on the 07:28:34 install before the edit: `Device : vt100`, no error.
   **NOT YET INSTALLED — needs a cycle.**

   **An existing account keeps `linux` until its VOC is updated**, and then
   picks it up silently: `update.voc` only prompts when the record TYPE
   changes (`LOGIN:613`) and both are `PA`, so `LOGIN:657` just writes it.

   **EIGHT CANDIDATES WERE ELIMINATED GETTING HERE, kept so nobody re-walks
   them.** 18 Aug 2026: (1) `PT$INVERT` and
   `PT_INVERT` disagreeing — both 2, `INT$KEYS.H:146` and `keys.h:181`;
   (2) `LOGIN` not including `int$keys.h` — it does, line 73; (3) two copies of
   `case_inversion` — `Public` is `extern` (`sddefs.h:261`) everywhere but
   `sd.c`, so there is one; (4) the instrument — two opcodes and behaviour
   agree; (5) the early `return` at `LOGIN:198` skipping line 266 — that is the
   `mode = 2 or 3` VOC-upgrade path, and the banner at `LOGIN:209` proves it
   was not taken; (6) `@TRUE` being negative and so meaning "report only" —
   it is 1, measured; (7) the setter being broken — `PTERM CASE INVERT` turns
   it On in the same session and it stays On; (8) `SET_PASSWD` resetting it at
   login — it is called from `CREATEA` and `PS_SCRIPT`, not `LOGIN`.

   **A SEPARATE REAL DEFECT, FOUND ON THE WAY AND NOT FIXED: `SET_PASSWD`'s
   case-inversion save/restore can never restore On.** `op_pterm`'s own stack
   diagram says the value returned is the **NEW** value, and a **negative**
   argument is what reports without setting. So `SET_PASSWD:88`
   `was.inverted = pterm(PT$INVERT, @false)` sets it off and saves the *off* it
   just wrote, and `SET_PASSWD:98` restores that. The fix is to read with
   `pterm(PT$INVERT, -1)` first, then set. **Harmless today only because
   inversion is already off everywhere**; it is latent, and it is ours — the
   lines carry a `14 Aug 26 Windows port` marker — so no `UPSTREAM_FIXES.md`
   entry.

   **WHAT WAS NARROWED, 17 Aug 2026, so the next attempt starts further on:**

   - `connection_type` **defaults to `CN_CONSOLE`** (`kernel.h:54`); only
     `-pipe`-style and socket invocations move it (`sd.c` 407, 423, 471). So a
     plain `sd.exe` is `CN_CONSOLE` and `op_tio.c:3258` should reach
     `init_console()`.
   - **The console path refuses an ordinary user**, measured: `sd.exe RUN BP X`
     with no pipe answers *"This command needs an elevated session"*. That is
     §5.6.2 working as designed, and it is why the console reading cannot be
     taken unelevated.
   - **The piped path is the one that matters anyway.** SD accounts are
     ssh-only, and ssh gives SD piped stdin — so the 0 above is the reading for
     the sessions real users get. **If it is 0 there, §5.12's terminal concern
     may already be satisfied for every account that can actually log in**, and
     the work would be removing three dead setters rather than changing
     behaviour. That is the thing to establish first.
   - `pterm()` **cannot be called from a user account** — internal only, and
     compiles as *"Matrix PTERM is not referenced in a DIM statement"*.
     `SYSTEM(1001)` is the route from a probe.

   **AND 707 `upcase(` CALLS IN `GPL.BP` ARE NOT ALL IN SCOPE.** Most are VOC
   verb lookup, `Y`/`N` answers and record types, which must stay — CPROC
   upcases verbs so lower-case typing still finds `LISTF`. The account-name
   subset is about 11 sites: `LOGIN` 281, 321, 339, 383, 690 and `CPROC` 2531,
   2577, 2579, plus the audit lines 2601, 2619, 3686.

   **WHAT IS LEFT of step 8** is the wide half §5.12 describes: account names
   (`LOGIN`, `CPROC`, the `$CRED` register), the terminal's `PT$INVERT`, and
   dictionary and VOC ids. (a) is the enabling change for the account half —
   `$CRED` and `ACCOUNTS` are directory files — but removing the `upcase()`
   calls is still what makes `sue` and `SUE` one account, and that is untouched.
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
11. **BUILT 17 Aug 2026, seventeenth session, AND NOT RUN.** `SDConnectLocal()`
    **could never have worked**, on this platform or any other, and it took
    three independent faults with it. Two were in the shipping path and are
    fixed; the third was in dead code.

    a. **The client and the server disagreed about `-C`.** `SDConnectLocal()`
       builds `sd.exe -Q -C \\.\pipe\~SDPipe<pid>-<n>` — the pipe name as a
       SEPARATE argument — while `sd.c` parsed `sscanf(argv[arg],
       "-C%d!%d", …)` and `exit(1)`ed on anything else. `argv[arg]` is exactly
       `"-C"`, so it matched nothing and the child died during argument
       parsing. **The same mismatch is in `sdb64`**, byte for byte —
       UPSTREAM_FIXES.md #4. `sd.c` now takes either form, and **consumes the
       name argument**, which it must: the option loop stops at the first
       argument not beginning with `-`, so the pipe name would otherwise be
       taken for a command to execute.
    b. **The client looked for `sd.exe` inside the DATA tree** —
       `<sysdir>\bin\sd.exe`, i.e. `C:\ProgramData\SD\sdsys\bin`, which exists
       and holds the pcode file. It is now found **beside the DLL** through
       `GetModuleHandleEx(FROM_ADDRESS)` + `GetModuleFileName`, which needs no
       configuration and follows the install wherever `{app}` puts it, since
       `stage.py` ships both in `usr\bin`. **The path is now quoted too**: it
       is under `C:\Program Files`, and an unquoted spaced path in
       `CreateProcessA` with a NULL application name makes Windows try
       `C:\Program.exe` first — a hijack, not just a bug.
    c. **`gplsrc/sdclient.c` had a fourth fault and does not matter**: it reads
       `C:\Windows\sd.ini`, which nothing creates. **That file is excluded
       from the build** (`Makefile:66`, `SRCS := $(TEMPSRCS:sdclient.c=)`) —
       the shipping client is `gplsrc/sdclilib/sdclilib.c`, whose `sysdir()`
       was already corrected on 14 Aug. **Read the right file**: an earlier
       hour of this session was spent analysing the dead one.

    **`gplsrc/win32pipe.c` is new, and is the THIRD `windows.h` file** after
    `win32sem.c` and `win32audit.c`. The pipe is a native object created by the
    UCRT64 client and `sd.exe` is MSYS2, so `open()` cannot reach it — the
    Cygwin runtime does not map `\\.\pipe\` names at all. It is opened with
    `CreateFile` and pushed into the Cygwin descriptor table with
    `cygwin_attach_handle_to_fd()`, exported by `msys-2.0.dll` (ordinal 379,
    checked), so everything above it reads and writes 0 and 1 unchanged.

    **It must not include `sd.h`, and neither do the other two.** `sd.h`
    reaches `linuxlb.h`, which declares `GetUserNameA()` and `Sleep()` with
    types that conflict with the real Windows ones — two "conflicting types"
    errors, measured. That is why it returns `int` rather than `bool`, as
    `win32audit.h` does.

    **DOES NOT WORK, AND THE REASON IS ARCHITECTURAL RATHER THAN A BUG LEFT TO
    FIND. 17 Aug 2026, measured on the 08:03:49 install.** Three real defects
    were fixed on the way and all three were worth fixing; a fourth thing is
    not a defect at all and stops this approach.

    **THE STOPPER: a descriptor made by `cygwin_attach_handle_to_fd()` is
    reported PERMANENTLY READY by `select()`** — `sel.always_ready 1` in
    `strace`, §6. SD decides whether input is waiting by asking `sdpoll()`
    (`linuxio.c:535`, `:383`, `:456`). Told "yes" unconditionally, it spins
    reading one byte at a time for ever: **`sd.exe` alive, silent, and never
    answering.** `make check-local` hung, and `SDConnectLocal("DON")` never
    returned. **Fixed by replacing the transport, not by repairing this** — see
    the top of this step; only the `-C <pipename>` convention still reaches the
    always-ready path, and `sd.c` now refuses it rather than hanging.

    **The three fixes are still right and still needed by any successor**: the
    `-C` argument mismatch, the `sd.exe` location, and the access argument
    below. None of them is undone by this.

    **BUILT AND WORKING — 17 Aug 2026. `SDConnectLocal()` CARRIES A SESSION.**
    Four runs, unelevated, `local_connect_test` exit **0** each time:

    ```
    connecting to DON ...
      admitted
      WHO -> 19 DON
    connecting to SDSYS (this MUST be refused) ...
      refused: User not allowed in requested account
    PASS: DON admitted, SDSYS refused.
    ```

    **AND THAT IS ALSO THE FIRST EVIDENCE OF ANY KIND FOR §7 STEP 6c** — the
    `ACC$GROUP` grant check in `APISRVR`, built 17 Aug and never run. **The
    control is what makes it evidence**: `DON` admitted alone would be equally
    consistent with a check that never executed, and `SDSYS` refused with
    "User not allowed in requested account" is that check running.
    **No orphaned `sd.exe` survives a run**, which is the EOF path working:
    closing our copies of the child's ends is what lets it see stdin close.

    **AND IT IS NOW VERIFIED ON A REAL INSTALL.** The first measurement was a
    development smoke test — the new DLL paired in a scratch directory with the
    installed `sd.exe`. **The cycle then ran and `make check-local` passed on
    the installed pair**, `assert-current` exit 0, 12:28:49 install,
    `WHO -> 2 DON`. Both runs agree; the header has the figures.

    **`make sd` clean, no warnings, both toolchains:** `sd.exe`
    **`81D0856F5493385E`**, `sdclilib.dll` **`8D1517D1CD2B83AB`**.

    **WHAT CHANGED.** All of it client-side except one refusal:

    - `SDConnectLocal()` makes **two anonymous pipes** and hands them to the
      child as its **standard handles**; `session[].hPipe` became `hPipeRd` /
      `hPipeWr`, because an anonymous pipe is one-way and the pair is what the
      duplex named pipe used to be alone.
    - The command line is now **`-Q -C1!0`**. **Note the order** — `sd.c`
      parses `-C<tx>!<rx>` and answers with `dup2(RxPipe, 0); dup2(TxPipe, 1)`,
      so rx must be 0 and tx must be 1. `-C0!1` would cross the streams, and an
      earlier note in this file said exactly that; it was wrong.
    - **Inheritance is restricted to exactly those two handles** with
      `PROC_THREAD_ATTRIBUTE_HANDLE_LIST`. Plain `bInheritHandles = TRUE`
      inherits **every** inheritable handle the process owns, and this library
      is loaded into somebody else's application — a handle it happens to hold
      to a file or a socket would be copied into a long-lived `sd.exe` and kept
      alive for the whole session, with nothing to show why.
    - `sd.c`'s **`-C <pipename>` branch now refuses with a diagnostic** instead
      of hanging. The code behind it is correct and the flaw is not in it, so
      `win32pipe.c` stays; but silent-and-never-answering is the worst thing to
      leave callable.
    - `ConnectNamedPipe` and `DisconnectNamedPipe` are gone: an anonymous pipe
      is connected the moment it exists.

    **The reasoning that got here, kept because the framing was the error:**

    **FIRST, THE FRAMING WAS WRONG: THE PEER IDENTITY NEVER CAME FROM THE
    PIPE.** There is no `ImpersonateNamedPipeClient` and no
    `GetNamedPipeClientProcessId` anywhere in `gplsrc` — checked.
    `SDConnectLocal()` gets identity because it **spawns `sd.exe` with
    `CreateProcessA`**, so the server is a CHILD running under the caller's own
    token and `GetUserNameA()`/`IsElevated()` inside it report the calling user.
    The named pipe only carries bytes. **So the socket option's stated cost is
    illusory — and so is the named pipe's stated benefit.**

    **THE THIRD OPTION: hand the child inherited pipe handles as its STANDARD
    HANDLES** — `CreatePipe` twice, `STARTUPINFO.hStdInput`/`hStdOutput`,
    `bInheritHandles = TRUE` — instead of opening a named pipe after the fact.
    Cygwin then builds descriptors 0 and 1 itself at startup, sees
    `FILE_TYPE_PIPE`, and installs its pipe handler, whose `select()` is
    `PeekNamedPipe`-based and answers honestly.

    **MEASURED, with the control in the same process and the same run** —
    `make check-select-probe`, `gplsrc/sdclilib/tests/select_probe_*.c`,
    identical on four runs:

    ```
    inherited(fd 0)  empty=0  data=1     <- select() tells the truth
    attached(fd 4)   empty=1  data=1     <- always ready: the stopper
    inherited read: [HELLO-INHERITED]    <- and it reads
    ```

    **The control is what makes it mean anything**: both descriptors were
    measured by the same `select()` call with the same timeout, milliseconds
    apart, in one Cygwin child spawned by one native parent. The only
    difference is how the descriptor was made. **`empty=0` is the whole
    finding** — always-ready is a property of injecting a RAW HANDLE, not of
    pipes.

    **IT NEEDS NOTHING IN THE SERVER.** `sd.c:441` already accepts
    `-C<tx>!<rx>` and does `dup2(RxPipe, 0); dup2(TxPipe, 1);`, so with the
    handles arriving on 0 and 1, **`-C0!1` is a no-op `dup2` that just sets
    `CN_PIPE`**. `win32pipe.c` leaves the hot path. The change is client-side
    only and REMOVES code rather than adding a `CN_PIPE` branch through the
    input layer.

    **NOT YET CHECKED:** how `-Q` / `is_sdApiSrvr` behaves with stdin and
    stdout as the protocol channel rather than a terminal. Read that before
    writing code.

    **The two options as originally framed, kept because they are the fallback
    if the above meets something:**

    - **Give `CN_PIPE` its own I/O.** Read and write the HANDLE with
      `ReadFile`/`WriteFile` and answer readiness with `PeekNamedPipe`, instead
      of borrowing descriptors 0 and 1 and `sdpoll()`. Contained — `CN_PIPE`
      is in only TWO places in the server (`sd.c:423`, `op_tio.c:3902`) against
      a dozen for `CN_SOCKET` — but it means a `CN_PIPE` path through the input
      layer. **Prefer this over the socket** if the third option fails.
    - **Use a loopback socket instead**, where Cygwin's `select` genuinely
      works and `CN_SOCKET` is already exercised. Cheaper, but reachable by any
      local process, so it needs authentication invented for it — new security
      surface in the one path that currently has a clean answer.

    **Do not spend another cycle looking for a flag.** Six combinations of the
    name and access arguments, `O_NONBLOCK`, and `F_SETOWN` were all measured;
    the always-ready behaviour is a property of the Cygwin file handler for a
    raw HANDLE, not a setting.

    **The failure and its diagnosis, in the order they were found:**

    - **Observed:** `SDConnectLocal("DON")` → `Connection closed by server`,
      test exit 1.
    - **The pipe was fine.** A probe standing in for the client showed
      `sd.exe` opening the pipe and then exiting **0** — not a crash, not
      `exit(1)`, and **silent on both streams**.
    - **THE PREDICTION IN THIS STEP WAS WRONG.** It said the likely fault was
      `cygwin_attach_handle_to_fd()` not honouring a requested descriptor
      number. It honours it exactly, measured.
    - **The real fault: its access argument must MATCH THE HANDLE**, not
      describe what the descriptor is for. The handle is opened
      `GENERIC_READ | GENERIC_WRITE`, so **both** calls must pass that.
      Passing `GENERIC_READ` for descriptor 0 — the obvious thing to write —
      **succeeds**, and the descriptor then fails `read()` with `EBADF`.

    - **After that fix `sd.exe` STOPPED EXITING and started hanging**, which
      was progress and was also the next symptom. `strace` then showed the
      always-ready loop above, which is the stopper.

    **HOW IT WAS FOUND, AND THIS IS THE REUSABLE PART. Two tools, neither of
    them an install cycle:**

    - **A standalone probe** — twenty lines of C built with MSYS2 gcc outside
      the repository, driven by a PowerShell harness acting as the pipe
      server — settled the access argument by trying six combinations against
      a real pipe with real data. **When the unknown is one library call,
      isolate the call.**
    - **`strace`, which is in MSYS2 at `/c/msys64/usr/bin/strace.exe`** and
      works on any Cygwin binary, `sd.exe` included:

      ```sh
      strace -o log.txt -- "C:\Program Files\SD\usr\bin\sd.exe" -Q -C \\.\pipe\NAME
      ```

      **It answered in one run what three cycles could not**, because the
      failing path prints nothing, exits nothing, and lies through `poll()`.
      There is no `gdb` in this MSYS2 install; `strace` is the tool to reach
      for. Both harnesses are worth rebuilding if this is picked up again.

    **`make sd` clean, no warnings**, both toolchains, `sd.exe`
    **`04CA97C138ADB148`** as installed at 08:03:49.

    **The vendored client's own docs were wrong and are corrected**: both
    `README.md` and `USER_GUIDE.md` said the Windows DLL does not provide
    `SDConnectLocal` and that it is "Linux-specific". It is exported —
    ordinal 6, checked with `objdump -p` — and its transport is a **named
    pipe**, which has no Linux equivalent in that library at all.

    **THE TEST IS WRITTEN AND COMPILES; IT HAS NOT BEEN RUN.**
    `gplsrc/sdclilib/tests/local_connect_test.c`, clean under
    `-Wall -Wextra -Wpedantic`. **Run it after the cycle, UNELEVATED:**

    ```sh
    cd sdb_ai/sd64 && make check-local
    ```

    **It carries its own control, and the control is the reason to trust it:**

    | account | expected | why |
    |---|---|---|
    | `DON` | admitted | `ACC$GROUP` is `sdu_don` and `GITORLI\don` is a member — both checked on the installed tree |
    | `SDSYS` | **refused** | `ACC$GROUP` is `sdsys`, which is not a Windows group |

    **`DON` succeeding on its own would prove nothing** — a grant check that
    never ran would admit it too. Exit codes say which happened: 1 `DON`
    refused, 2 `SDSYS` admitted (so the check did not run and the first result
    is worthless), 3 the session opened but `WHO` failed.

    **It is deliberately NOT in `make check`.** Everything there runs without a
    server; this measures the INSTALLED tree and is therefore subject to the
    cycle rule.
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

### Open: how many kinds of user does SD have, and what enforces each (raised 16 Aug 2026)

Owner's model, three tiers: **application users** dumped into a menu, never
seeing `:`, holding object code and no source; **programmers**, at the prompt,
with read/write/catalog/execute/create/delete in their own account and any
`GRANT`ed account including a shared-program one, needing *some* `SH`;
**db administrators**, everything. In Pick the last two were the same because
Pick *was* the OS. §5.6.1 already split them here, so deviating is not new.

**THE TWO TIERS THAT EXIST TODAY ARE ENFORCED BACKWARDS**, and this is the
finding to act on before designing more of them:

- `SH` at the prompt is gated on `IsElevated()`, and an ssh session **can never
  be elevated** — so no ssh user ever gets `SH`, including the programmers who
  need it.
- `OS.EXECUTE ... CAPTURING` is **ungated** (§7 step 7, measured with a
  control) — so anyone who can write and run a program has full OS execution
  under their own token.

So the visible control is denied to the people who need it and the capability
it guards is open to everyone who does not. **Tiers 1 and 2 have identical
actual power.**

**No privilege concept exists to hang tiers on.** Only `USR_ADMIN`
(`sysseg.h:158`), one session flag seeded from `IsElevated()` at process start.
Nothing in `SYSCOM`; `PRIVILEGED_COMMANDS` is a local in `IS_INSTALL`, not a
mechanism.

**Owner's approach, 16 Aug 2026: capability by VOC content.** Take **`BASIC`,
`CATALOG`, `RUN`, `ED` and `SED`** off accounts that do not need them — no
compiler, no way to catalogue, no way to run an imported object, no editor to
put any of them back with. Idiomatic MV, needs no C. Plus break off
(`OPT.NO.USER.ABORTS` exists) and `ForceCommand` on by default.

**`COPY` belongs on the list too** — it writes a record into VOC as effectively
as `ED` does. **`EXECUTE`/`PERFORM` do NOT and cannot**: corrected 16 Aug 2026,
they are BASIC statements, not VOC verbs, so they are not in the 434 and cannot
be removed. What they run still resolves through VOC, so removing `BASIC` denies
it to programs as well as to the prompt — which is what makes the whole approach
work with one mechanism.

**THREE TIERS, AND A NEW `PROGRAMMER` KEYWORD ON `CREATE.ACCOUNT`** (owner,
16 Aug 2026) beside the existing `ADMINISTRATOR`. Standard gets a reduced VOC,
`PROGRAMMER` a full one plus limited shell, `ADMINISTRATOR` everything.
**An admin can add anything back to any account**, so the reduced VOC is a
starting posture the site curates, not a wall.

**The decision space is 144 verbs, not 434** — the other 248 are `K` keywords
(query syntax) plus 15 `F`, 11 `R`, 4 `PA`, 2 `S`, 2 `Q`, 2 `PH`, 1 `X`.
First-pass split is roughly 30 admin / 45 programmer / 65 standard, so
**`PROGRAMMER` sits much closer to `ADMINISTRATOR` than to standard**: the real
line is between running an application and building one.

**Owner's rulings, 16 Aug 2026:** `MICRO` **removed** — it launches an external
editor, so it is a containment escape of the same class as `SH`. Language verbs
**removed**, SD is English only: `LOAD.LANGUAGE`, `SET.LANGUAGE`, `NLS`.

**DONE 17 Aug 2026, seventeenth session — all four are out of both VOCs.**
`VOC_TEMPLATE` 434 → **430**, `NEWVOC` 411 → **408** (`LOAD.LANGUAGE` was
already admin-only). **The four programs are KEPT and are now callerless**, as
`$CRED` and its friends are (§7 step 0): `GPL.BP/MICRO`, `NLS`, `SETLANG` and
`LOADLANG` still compile and still catalogue, and nothing can reach them.
**Checked before removing** — nothing anywhere calls `$MICRO`, `$NLS`,
`$SETLANG` or `$LOADLANG`, and `K$SET.LANGUAGE` in `INT$KEYS.H` is kernel key
38, unrelated to the verb and untouched.

**THE INVENTORY, MEASURED 17 Aug 2026, because the numbers here were slightly
wrong.** By the **first character** of field 1, which is what SD reads
(`voc.rec[1,1]`, `CPROC:3376`):

| | `VOC_TEMPLATE` | `NEWVOC` |
|---|---|---|
| **V verbs** | **149** | **136** |
| K keywords | 248 | 249 |
| F / R / P / S / Q / X | 37 | 26 |

**So the decision space is 149 verbs, not the 144 recorded above** — that count
matched the literal string `V` and missed five records whose type field is
descriptive text beginning with V. **`NEWVOC` deliberately carries descriptions
where `VOC_TEMPLATE` carries bare letters**, and `CREATEA:530` normalises them
down to the type letter on the way in, which is why both forms work.

**AND THE GAP BETWEEN THE TWO TIERS TODAY IS ADMINISTRATION, NOT CAPABILITY** —
this is §8's finding, counted. Only **23 records** are in `VOC_TEMPLATE` and not
`NEWVOC` (24 before `LOAD.LANGUAGE` went): **9 administration verbs**
(`CREATE.ACCOUNT`, `DELETE.ACCOUNT`, `MODIFY.ACCOUNT`, `UPDATE.ACCOUNT`,
`GRANT`, `REVOKE`, `LIST.GRANTS`, `UNLOCK`, `ENCRYPT.FIELD`), the 3 `*.SERVER`
verbs, and **11 SDSYS plumbing records** — `$HOLD` `ACCOUNTS` `BP` `BP.OUT`
`GPL.BP` `GPL.BP.OUT` `MESSAGES` `QFILE` and `FIRST/SECOND/THIRD.COMPILE`.
**A standard account still gets `BASIC`, `CATALOG`, `RUN`, `ED`, `SED`, `COPY`,
`SH`, `!` and `DELETE.CATALOG`** — every capability on the removal list.

**THE 9 ARE NOW THE ADMINISTRATOR TIER.** Owner's ruling, 17 Aug 2026:
"administrators get the whole voc". It was never a no-op — an SD administrator
had to `LOGTO SDSYS` to administer anything. Safe because the programs gate
themselves: `CREATEA:109`, `DELACC:60`, `MODIFYA:48`, `GRANTA:86`, `UNLOCK:61`
each open `if not(kernel(K$ADMINISTRATOR, -1)) then stop sysmsg(2001)`.
**Two do not and are on the list anyway** — `UPDATE.ACCOUNT` is `V|IN|15`,
`CPROC:1521`, ungated; `ENCRYPT.FIELD` points at **`$CRYPTO`, which is not in
this tree at all** and is as broken in SDSYS's VOC as it will be in an admin's.

**The 11 plumbing records are NOT copied**, and that is a decision, not an
oversight: `ACCOUNTS`, `BP.OUT`, `GPL.BP`, `GPL.BP.OUT` and `QFILE` are
**relative** pointers (`F|ACCOUNTS|ACCOUNTS.DIC`), so in a user account they
name files that are not there and `LIST ACCOUNTS` fails to open rather than
lists; the `*.COMPILE` records are bootstrap paragraphs; `$HOLD` and `BP` are
already made per-account by `CREATEA`'s `create.dir.file`.

**THE MECHANISM IS BUILT — 17 Aug 2026 — AND HAS NOT BEEN COMPILED OR RUN.**
A cycle is owed; `make sd` is NOT needed (only BASIC and data changed since the
08:03:49 install, `sd.exe` `04CA97C138ADB148`). **`stage.py --bootstrap` is
`CREATEA`'s and `LOGIN`'s first compiler for this change**, and that is where a
mistake will surface. Files: `CREATEA`, `LOGIN`, `SYSCOM/KEYS.H`,
`NEWVOC/TIER.OMIT.STANDARD`, `NEWVOC/TIER.ADD.ADMINISTRATOR`, `MESSAGES/10052`,
`gplbld/stage.py` (comment only).

**A BAD `$LOGIN` LOCKS YOU OUT OF SD** — §7 step 0 says back `gcat` up before
recompiling one on an installed system, and this change touches `LOGIN`. The
cycle route does not have that hazard (the bootstrap builds a fresh tree), but
the recovery route does.

**What was avoided, and why the list matters more than usual here** — none of
this compiles until the cycle: `CONTINUE` is used in `LOGIN` **because that
file demonstrates it** and not in `CREATEA`, which does not; both loops use an
explicit id comparison rather than `LOCATE`; `update.voc.tier` and
`tier.acc.name` are initialised at the top of `LOGIN` because BCOMP's
**"is not assigned a value"** is what `bootstrap.py:229` fails the bootstrap
on, and both are read textually above the `get.acc.tier` that sets them.

- **`PROGRAMMER` keyword** at `CREATEA`, beside `ADMINISTRATOR`, matched on
  token text for the same reason (the `KW$` table is positional and shared).
- **`tier`** — `STANDARD` / `PROGRAMMER` / `ADMINISTRATOR`, a string not a flag,
  because it is written to the register and read back. It replaced a boolean
  `full.voc` that could not tell the top two apart. `PROGRAMMER` **cannot
  downgrade** `ADMINISTRATOR`; both keywords are accepted in either order.
- **`NEWVOC/TIER.OMIT.STANDARD`** lists what a standard account does not get —
  **18 ids** since 17 Aug. **`NEWVOC/TIER.ADD.ADMINISTRATOR`** lists the 9 an
  administrator gets on top, read out of `VOC_TEMPLATE`. Field 1 is a
  description; fields 2+ are ids. **Held as data so the shipped posture changes
  without recompiling**, and in `NEWVOC` because that file is already open in
  the loop and already shipped.
- **READ OUT OF `VOC_TEMPLATE` RATHER THAN MOVED INTO `NEWVOC`, and that is the
  whole design.** The fallbacks only point the safe way while `NEWVOC` holds
  nothing administrative: a lost omit list means "no policy" and gives the full
  VOC, so `CREATE.ACCOUNT` in `NEWVOC` would let one missing record hand every
  account the power to make more. The add list fails the other way — lost, an
  administrator gets a programmer's VOC and finds out at once. `stage.py:117`
  says the same and is amended to say why it survives the tiers.
- **A missing or empty list gives every account the full VOC** — the old
  behaviour exactly, which is the safe way round for a lost record.
- **Both list records' descriptions start with "T"**, not a VOC type letter, so
  if a skip ever broke they would land inert rather than as fake verbs.
- **`ADOPT` defaults to `ADMINISTRATOR`** (`CREATEA`, end of `more.args`).
  Without it the installing user lands STANDARD with no `BASIC`, no `ED` and no
  `CATALOG` — `adopt-account.ps1:195` passes no tier keyword and never had one
  to pass. **A regression the tier work itself would have introduced**, and it
  would have read as "SD is broken after installing it". A default, not an
  override: an explicit keyword still wins, and `make.admin` is untouched.

**WHAT IS ON THE LIST AND WHY.** Owner's rulings, 16–17 Aug: `BASIC`,
`CATALOG`, `RUN`, `ED`, `SED`, `COPY`, `DELETE.CATALOG`, `SH`, `!`. **Plus four
exact aliases, because leaving them would void the ruling** — measured, not
guessed: `CATALOGUE`→`$CATALOG`, `DELETE.CATALOGUE`→`$DELCAT`, `EDIT`→`$ED`,
and `COPYP` (`$COPYP`, "Pick style COPY", the same capability by another
program). **Thirteen ids.**

**RULED 17 Aug 2026 — all four are PROGRAMMER AND ABOVE**, so all four are on
the omit list: **`MODIFY`** (`$MODIFY`, a record editor, the same class as
`ED`), **`COMPILE.DICT`** (`$CD`) and **`GENERATE`** (`$GENERAT`), the
dictionary compilers, and **`PHANTOM`**, which runs a catalogued program in the
background. **This moves `PHANTOM` out of ADMINISTRATOR-only** in the split
below. **Plus a fifth id: `CD` is an exact alias of `COMPILE.DICT`** — both
`Verb to compile dictionaries|CA|$CD`, and `THIRD.COMPILE` uses it that way.
**Eighteen ids.** Reading the records found it; the name alone would not have,
and this is the second time — see the four aliases above.

**NOT DONE:** the 30/45/65 split of the 149 verbs. What exists is the
capability cut, not the full three-tier curation.

**THE HOLE THAT MADE THE TIERS TEMPORARY, FOUND AND FIXED 17 Aug 2026.**
`LOGIN:501 update.voc` re-copied **the whole of `NEWVOC` with no tier filter**,
handing a standard account back `BASIC`, `CATALOG`, `RUN`, `ED`, `SED`, `COPY`
and `DELETE.CATALOG` — and writing `TIER.OMIT.STANDARD` into its VOC as a
record. **Reached two ways, neither needing privilege:** `UPDATE.ACCOUNT`
(`CPROC:1521`, internal verb 15, ungated), and — worse, because it needs no
verb — the `$RELEASE` test at **`LOGIN:419`**, which asks **any** user "Update
VOC to new release?" whenever the account's release level differs from
`SD.REV.STAMP`. One `Y`. **So the tiers survived exactly until the next release
stamp moved**, which is not a boundary anyone would notice.

**The fix needs the tier RECORDED, because it was a create-time decision with
nothing persisting it.** `ACC$TIER` = **`ACCOUNTS` field 5**, `KEYS.H:281` —
the first use of the "start at field 5" that the `ACC$USERS` note reserved
(field 4 is poisoned). `CREATEA` writes it on **every** path including `ADOPT`;
`LOGIN` reads it at all three `update.voc` call sites and applies the same omit
list. **A blank field means the full VOC**, the pre-tier behaviour: blank can
only occur on an account created before this, which already holds a full VOC,
and an update only ever writes — it never deletes.

**And a correction to yesterday's comment:** `CREATEA` says `CONTINUE`'s
behaviour inside `LOOP ... REPEAT` "is not demonstrated anywhere here" and used
a flag instead. **It is demonstrated — `LOGIN`, in `update.voc` itself**, where
a declined type change skips the write. `LOGIN` uses `CONTINUE`; `CREATEA`
keeps its flag, and the wrong note is left standing there rather than corrected
by a second uncompiled change.

**DONE AND PASSED — 17 Aug 2026, 11:31:38, 22 of 22.** `gplbld/verify-tiers.ps1`
is this recipe as one elevated command, and the header has the table. What
follows is what it checks and why each part is there.

**HOW TO TEST IT** — no elevation needed beyond `CREATE.ACCOUNT` itself, and it
carries its own controls. Three accounts, not
one: `CREATE.ACCOUNT USER <a>`, `USER <b> PROGRAMMER`, `USER <c> ADMINISTRATOR`.

- `<a>`'s VOC lacks all **eighteen**; `<b>`'s has them. **Checking only `<a>`
  proves nothing** — a copy loop that skipped everything would also pass it.
- `<c>` has the eighteen **and** the nine, `<b>` has the eighteen and **not**
  the nine. That second half is the control for the add list.
- No account's VOC holds `TIER.OMIT.STANDARD` or `TIER.ADD.ADMINISTRATOR`.
- `ACCOUNTS` field 5 reads `STANDARD` / `PROGRAMMER` / `ADMINISTRATOR`, and
  **`DON`'s reads `ADMINISTRATOR`** — that is the `ADOPT` default, and the
  installing user's own account is the one a broken default breaks.
- **Then the durability half, which is the point of recording the tier:**
  `UPDATE.ACCOUNT` in `<a>` must leave it without the eighteen. Before this
  change it restored every one of them.
`SET.TRIGGER`, `UPDATE.RECORD`, `MODIFY`, `HSM`, `GENERATE` are **PROGRAMMER**.
`SET.SERVER`, `DELETE.SERVER`, `LIST.SERVERS` **removed** — SDNet server details
were not held securely in this version.

**THE SPLIT ITSELF, first pass, rulings above already applied.** Tiers are
cumulative: `PROGRAMMER` gets standard plus its own, `ADMINISTRATOR` gets
everything. **Not reviewed by the owner yet** — expect entries to move.

REMOVED from every tier (7):
`MICRO` `LOAD.LANGUAGE` `SET.LANGUAGE` `NLS` `SET.SERVER` `DELETE.SERVER`
`LIST.SERVERS`

ADMINISTRATOR only (25) — `PHANTOM` moved to PROGRAMMER, owner 17 Aug 2026:
`CREATE.ACCOUNT` `DELETE.ACCOUNT` `MODIFY.ACCOUNT` `UPDATE.ACCOUNT`
`CLEAN.ACCOUNT` `GRANT` `REVOKE` `LIST.GRANTS` `CONFIG` `LISTU` `LIST.READU`
`LIST.LOCKS` `CLEAR.LOCKS` `LOCK` `UNLOCK` `LOGOUT` `SET.DATE`
`UMASK` `PSTAT` `PDEBUG` `PDUMP` `DUMP` `ENCRYPT.FIELD` `SH` `!`

PROGRAMMER adds (47):
`BASIC` `CATALOG` `CATALOGUE` `DELETE.CATALOG` `DELETE.CATALOGUE`
`COMPILE.DICT` `PHANTOM` `RUN` `MAP` `DEBUG` `ED` `EDIT` `SED` `MODIFY` `UPDATE.RECORD`
`SET.TRIGGER` `HSM` `GENERATE` `CREATE.FILE` `DELETE.FILE` `CLEAR.FILE`
`CONFIGURE.FILE` `ANALYSE.FILE` `ANALYZE.FILE` `FSTAT` `CREATE.INDEX`
`DELETE.INDEX` `BUILD.INDEX` `MAKE.INDEX` `LIST.INDEX` `COPY` `COPYP` `DELETE`
`RENAME` `REFORMAT` `SREFORMAT` `SEARCH` `LIST.DIFF` `LIST.ITEM` `SORT.ITEM`
`LIST.COMMON` `DELETE.COMMON` `LIST.VARS` `CD` `CNAME` `REPORT.SRC`
`REPORT.STYLE` `FORMAT`

STANDARD — what an application needs (70):
`SELECT` `SSELECT` `QSELECT` `NSELECT` `GET.LIST` `SAVE.LIST` `FORM.LIST`
`COPY.LIST` `MERGE.LIST` `DELETE.LIST` `LIST.UNION` `LIST.INTER` `CLEAR.SELECT`
`CLEARSELECT` `LIST` `SORT` `SUM` `LIST.LABEL` `SORT.LABEL` `LIST.FILES`
`SETPTR` `SPOOL` `SP.OPEN` `SP.CLOSE` `SP.VIEW` `PRINTER` `COMO` `LOGTO`
`QUIT` `STOP` `ABORT` `CLEAR.ABORT` `GO` `IF` `SET` `SHOW` `OPTION` `ALIAS`
`SET.EXIT.STATUS` `SET.FILE` `TERM` `PTERM` `DATE` `TIME` `DATE.FORMAT` `WHO`
`WHO.AM.I` `STATUS` `MESSAGE` `LOGMSG` `BELL` `ECHO` `HUSH` `PAUSE` `SLEEP`
`CLR` `CS` `CT` `CLEAR.INPUT` `CLEARINPUT` `CLEAR.PROMPTS` `CLEARPROMPTS`
`CLEAR.DATA` `CLEARDATA` `CLEAR.STACK` `GET.STACK` `SAVE.STACK` `RELEASE`
`AUTOLOGOUT` `CLEAR.STACK`

**Two notes on the lists.** `COPYP` is in PROGRAMMER but is one of the five
malformed entries above, so it does not work today either way. And `LIST` and
`SELECT` must stay in STANDARD, yet they read **any** file the account can open
— so the VOC tier decides what a user may DO and the per-account ACL decides
what they may REACH. Neither substitutes for the other.

**How it would be built:** a second, reduced `VOC_TEMPLATE` plus the
`PROGRAMMER` keyword in `CREATEA` beside `ADMINISTRATOR`, so the tier is chosen
where `sdsshonly` and `Administrators` are already chosen. It wants the
per-account ACL under it first, or an administrator's reduced VOC is one `COPY`
away from being undone by its own user.

**FIVE VOC_TEMPLATE ENTRIES ARE MALFORMED AND CANNOT WORK.** Found 16 Aug 2026.
Field 1 holds the DESCRIPTION where the type code belongs, so the record is
shifted by one: `COPYP`, `DELETE.SERVER`, `LOAD.LANGUAGE`, `SET.SERVER`,
`UNLOCK`. Compare `LIST.SERVERS`, which is correct — `V` / `CA` / `$LSTSRVR`.
Three are being removed anyway; **`COPYP` and `UNLOCK` need the missing `V`
line**, and `UNLOCK` is what an administrator reaches for to clear a stuck
record lock.

**ANSWERED 16 Aug 2026, sixteenth session: A `CA` VERB'S PROGRAM LIVES IN
`gcat`, EXACTLY WHERE IT LOOKS AS THOUGH IT SHOULD.** `$QPROC` is there at
**54,073 bytes** in a healthy tree, alongside 131 others. Nothing needs tracing
and there is no gap in the model.

**The question was manufactured by measuring a broken install**, and the
reasoning is kept because the mistake is the instructive part. What stood here
was: *"The installed system has 4 entries in `gcat` (`!PATHTKN`, `$BBPROC`,
`$BCOMP`, `$CPROC`), 3 objects in `GPL.BP.OUT`, and an empty `cat` — against 144
verbs ... **This is a gap in the model, NOT evidence of a broken tree**, because
`COUNT VOC` returning 431 is recorded repeatedly on real installs."* It was
evidence of a broken tree. Those four are `bbcmp.py`'s **bootstrap seed**, and
`COUNT VOC` 431 was measured on *earlier, working* installs — the one in front
of it had never run at all. **The tell was there and was read past:
`gcat/$CPROC` was 0 bytes**, which is the placeholder `bootstrap.py` touches.

**The general form, and this file has now recorded it twice:** a number read off
the installed tree describes whatever that tree is, and "SD demonstrably works,
so this must be a subtlety I have not traced" is the reasoning to distrust.
**Date the tree first.** Scoping the `gcat` lock is therefore unblocked — 132
entries is the real figure, not 4.

**Not related:** PROC, the pre-BASIC language, was removed from sd-ai and
remains upstream (owner, 16 Aug 2026). `QPROC` and `BBPROC` are not PROC despite
the names.

**It is only durable with per-account ACLs (§7 step 3 / the B work).** A VOC
the user can write is a VOC they can put `BASIC` back into, and SD object code
is portable pcode, so without `DC` withheld they can drop an object into
another account. Locking `<account>\VOC` read-only to `sdu_<name>` is what makes
the reduced VOC stay reduced. **So the tier work is blocked on B, not the other
way round.**

**Two residual holes, both real, neither closed by any of the above:**

1. **Injection through the application's own `OS.EXECUTE` or `EXECUTE`.** Tier-1
   programs legitimately need OS access, so the capability stays; an app that
   builds a command from user input is an escape and the user compiles nothing.
   `!valid_shell_cmd`'s ban on `; | & $ < >` guards the `SH` path only.
2. **A machine whose ssh server SD did not install**, where `ForceCommand` is
   never written (§5.9, structural). The user lands in `cmd.exe` and never meets
   SD's VOC at all.

**The real fix for (1) is program provenance** — a catalogued program written by
a programmer may `OS.EXECUTE`, an ad-hoc one may not. Setuid-shaped, new
machinery, and it depends on the `gcat` ACL work: "catalogued" means nothing
until users cannot rewrite each other's entries. Left open deliberately.

**And the floor under all of it:** until §5.7's service model, every tier is
enforced by the user's own Windows token. Tier 3 is real because Windows
enforces it. Tiers 1 and 2 are only ever as real as the ACLs.

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

**MEASURED 16 Aug 2026, sixteenth session — THE LINUX CLIENT CONTRACT CANNOT BE
PORTED, AND THE REASON IS NOT ssh.** This was the "untested and load-bearing"
item here; it is now settled, and it settles the transport with it.

- **The ssh client accepts the syntax.** `-L 9999:/tmp/sdclient.socket` on
  OpenSSH_for_Windows_9.5p2 reaches host-key verification, i.e. it parsed —
  against a malformed control that is rejected outright with `Bad local
  forwarding specification`. So `-L port:/unix/socket` is **not** the blocker.
- **The blocker is that MSYS2's AF_UNIX is not a socket Windows can see.** A
  socket bound by MSYS2 at `/tmp/x.sock` is, from native Windows, a **54-byte
  regular file** reading `!<socket >52445 s <cookie>` — the Cygwin emulation,
  a TCP port plus a shared secret. A native Windows AF_UNIX socket is a
  zero-length reparse point.
- **Demonstrated, not inferred**, with a control on one socket at one moment:
  MSYS2's own client **connected** and the server logged the accept; native
  `curl.exe --unix-socket` on the same path failed in 0 ms and the server saw
  nothing.

**So `sshd`, a native Windows program, cannot reach a socket SD creates through
the MSYS2 runtime**, and `ssh -L <port>:/tmp/sdsys/sdclient.socket` cannot work
here however the rest is built. **This decides the named pipe** — already
called "the strongest argument" below, now a measurement rather than an
argument — or a loopback TCP socket with authentication of its own.

**A note on the rig, because the first attempt produced a confident wrong
answer.** MSYS2's emulation needs the server to actively `accept()` for a
client's cookie handshake to complete, so a `listen()`-then-sleep server times
out *every* client. That run had the control failing too, which is the only
reason it was not written up as proof.

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
