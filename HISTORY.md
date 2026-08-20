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

## 20 Aug 2026 - Correction: `gplsrc/sdclient.h` is live, and the account-ACL verifier is written

**Commit:** this one.

**CORRECTION TO PROJECT_STATUS.md's "WHAT IS LEFT" ITEM 6 AND TO COMMIT
`18fdfa8`, both of which said to delete `gplsrc/sdclient.c` AND
`gplsrc/sdclient.h`.** The `.c` was dead and is deleted. **The `.h` is not
dead and would have broken the build.** `gplsrc/op_tio.c` takes `SV_PROMPT`
(`:3732`), `SrvrRespond` (`:3812`) and `SrvrEndCommand` (`:3817`) from it,
`op_tio` is in `gpl.src:70`, and the only `-I` the build passes is `gplsrc` -
so `gplsrc/sdclilib/sdclient.h` is not reachable and cannot stand in.

**MEASURED BOTH WAYS RATHER THAN ARGUED**, by moving the header aside and
building:

```
header present  ->  op_tio.o built, make sd exit 0
header absent   ->  op_tio.c:98:10: fatal error: sdclient.h: No such file
                    make exit 2, op_tio.o not built
```

**HOW THE WRONG CLAIM GOT MADE, because the shape of it will recur.** The
three arguments recorded for the deletion - stripped from `SRCS` at
`Makefile:66`, absent from `gpl.src`, orphan `.o` rule at `Makefile:214` -
are every one of them a statement about the `.c` file. None was ever evidence
about the header. The entry then carried a warning not to confuse
`gplsrc/sdclient.h` with `gplsrc/sdclilib/sdclient.h`, which read as the
header question having been examined; it had been examined only far enough to
tell the two apart. **A `.c` and a `.h` with one basename are not one fact.**

**The guard against a repeat is in the file, not in a document.**
`gplsrc/sdclient.h` now opens its `START-HISTORY` with a dated note naming the
three symbols and their line numbers.

**NOT ADDED TO UPSTREAM_FIXES.md, deliberately.** `sdb64` has the identical
dead `.c`, the identical orphan rule at `sd64/Makefile:132`, and the same live
header - but nothing there misbehaves, because request 24 is still upstream's
live login. Dead code and a naming trap are not a defect.

**ALSO: `gplbld/verify-accountacl.ps1`, section 8's oldest unwritten item.**
It asserts that the ACL `CREATE.ACCOUNT` applies (`CREATEA:618`,
`secure.account.dir`, through `!ps_script`) is byte-identical to the one
`gplbld/secure-account-dirs.ps1` applies. The rule is in two places on purpose
- they cannot share a file - so a measurement was always the intended guard,
and `CREATEA`'s comment had promised this filename since 19 Aug.

**THE CONTROL IS THE DESIGN.** Both halves are idempotent, so running the
script over a directory `CREATE.ACCOUNT` has just stamped leaves it identical
**whether the script applied the rule or did nothing at all** - a test without
a control here would pass with the script deleted. It therefore reads the DACL
three times: after `CREATE.ACCOUNT`, after `icacls /reset`, after the script.
The middle reading is asserted to have landed - `sdusers` back, inheritance
back on, differs from the first - before the third is believed.

**Its mechanics were measured on a scratch tree before it was wired up**, so
the first real run has only the SD-side question open: `/reset` does unprotect
and restore the inherited `sdusers` ACE; the stamp is
`D:PAI(A;OICI;FA;;;SY)(A;OICI;FA;;;BA)(A;OICI;0x1301bf;;;<grp>)`; re-stamping
reproduces it byte for byte. Rights are asserted as masks (`F` 2032127, `M`
1245631, `(OI)(CI)` 3) and identities by SID, because both halves grant
`*S-1-5-18` and `*S-1-5-32-544` so that a localised Windows works.

**Wired in two places it would otherwise have broken:** step 4 of
`post-cycle-elevated.ps1` (`-AclPrefix`, default `sdacl2`), and
`assert-current.ps1`'s `$neverShipped` - without the second it would report
the tree stale *because it exists*, then refuse to run on the strength of its
own newness, which is the toll `verify-setpw.ps1` already recorded.

**WHAT IS STILL OPEN:** the tree is STALE and owes one cycle. `make sd` is
green; nothing has been measured against an install. **The cycle deletes
`C:\ProgramData\SD`, taking `APIPORT=4243` and every `$cred` record with
it**, so `SET.PASSWORD DON` and re-enabling `APIPORT` are owed afterwards.
`verify-accountacl.ps1` has never run against SD.

---

## 20 Aug 2026 - The client libraries get the project licence header, and lose ScarletDME

**Commit:** this one, plus `winsdclilib` `9d8af57` and `sdclilib32` `52226a8`.

**WHAT WAS ASKED:** the project licence header and "Modifications Copyright
Donald Montaine" on every source file in both client repositories, ScarletDME
references gone, and `qm-connect` renamed `sd-connect`.

**THE LINE THAT MATTERED: QM IDENTIFIERS AN APPLICATION RESOLVES ARE NOT
BRANDING.** `qmclilib.dll` is the filename mvDeveloper loads; `qmclilib.def`
carries the `QMConnect`/`QMRead`/... names a QM application imports BY NAME;
`qmclilib.h` declares them; `qmcompat.c` implements `QMConnectLocal`. Renaming
any of them ends QM compatibility, which is the entire reason `sdclilib32`
exists. Owner confirmed: branding only. `qm-connect` -> `sd-connect` is a tool
name and moved.

**THE LICENCE, AND A CORRECTION THE OWNER SUPPLIED.** The first plan kept the
GPL grant in `err.h`, `revstamp.h` and `sdclient.h` intact, on the reasoning
that GPL -> LGPL is not a relicensing the GPL permits. The owner said that
wording was the port's own and should have said LGPL. **The Linux tree settles
it**: `sdb64`'s `err.h` says GPL version **2** and has **no** linking
exception; ours says version **3** and has one. The port wrote both, and a
linking exception is precisely what is added when LGPL-style linking is meant.
So it is our notice with a typo, and correcting it is not touching Ladybridge's
grant.

**COPYRIGHT NOTICES STAY, and the owner is right that the GPL never permits
removing them.** They are also the provenance - they say where the file came
from - so they earn their place twice.

**THE MISTAKE WORTH THE ENTRY: THE FIRST PASS EDITED THE MIRROR.** All seven
shared files diverged from `gplsrc/sdclilib`, which is exactly what
`VENDORING.md` exists to prevent and exactly what shipped a SCRAM-less
`qmclilib.dll` on 19 Aug. Caught by scanning for what was left rather than by
any guard - **nothing in the tooling checks that divergence**, which is worth
knowing. Undone by restoring from the source of truth, redone there, synced
out, and the nine shared files then checked byte-identical **by hash**.
**Edit the source of truth; never the mirror.**

**THREE SMALLER BREAKAGES FROM PREPENDING A HEADER BLINDLY**, all caught before
commit: `build.cmd` had `rem` lines above `@echo off`, so cmd would have echoed
them; `generate_pdf.py` lost its shebang from line 1; and two files stated their
title twice. **A header is not always safe to put at the top of a file.**

**`sdclilib32` WAS MIXED CRLF AND LF.** It had never been a git repository, so
nothing had normalised it, and prepending an LF block to a CRLF file produced
files that were both. Now LF with a `.gitattributes`. It matters beyond
tidiness: "are these files byte-identical" is a check this project runs, and a
line-ending difference turns a real answer into a false one.

**ScarletDME IS NOW ABSENT FROM EVERYTHING A USER SEES.** The message
catalogue never had it - `changelog:2194` records that cleanup being done
deliberately. `gpl.bp/LOGIN` held a commented-out pre-fork banner, one
character from printing at every login; removed. What remains is history and
attribution and stays: the changelog, `contrib`, `sdb_ai/README.md`'s account
of the fork, and source comments.

**THE LIVE BANNER STILL CREDITS LADYBRIDGE** - `(c) 2000-2026 by Ladybridge
Systems and Other Contributors`. Left alone: an attribution notice, and whose
names join it is the owner's call.

**AND THE CHANGELOG ENTRY COST A FOURTH CYCLE.** `sdsys/changelog` ships, so
writing the entry for the banner removal - which CLAUDE.md requires in the same
commit - made the install stale one minute after it had gone green. **The
lesson is the one this file already carries in the other direction: finish
EVERY source change before cycling, and the changelog is a source change.**

Verified on the 12:58:06 install, `assert-current` exit 0: lcnames 142/142,
keys 10/10, editkeys 14/14, credacl, nocase, osusers, setpw 4/4, check-local,
fold 10/10, createaccount, tiers, scramlogin `sdscram5` 40/40, apiport
`sdapi6`, tierapi `sdtapi3` 16/16.

---

## 20 Aug 2026 - All three account tiers reach the API, through the real client

**Commit:** this one. Twenty-ninth session.

**THE QUESTION, FROM THE OWNER:** can mvDeveloper connect as a standard user
and as a programmer, not just as an administrator?

**ANSWERED BY DRIVING THE CLIENT mvDeveloper ACTUALLY LOADS**, rather than by
reasoning about the protocol or by clicking through a GUI once.
`gplbld/verify-tierapi.ps1` runs `qm-connect.exe`, which links against the
32-bit `qmclilib.dll` in `Projects/sdclilib32` - the same file that sits beside
`mvDeveloper.exe`. **16/16 on the 09:09:06 install.**

```
STANDARD       sdtapi11   connects   VOC 393
PROGRAMMER     sdtapi12   connects   VOC 411
ADMINISTRATOR  sdtapi13   connects   VOC 421
```

**THE TIER DOES NOT GATE THE LOGIN, AND THAT IS THE DESIGN.** Nothing in the
SCRAM exchange or in `vb.account` consults the VOC. What the tier gates is what
happens after: 393 is `newvoc` minus `TIER.OMIT.STANDARD`, so a standard
account has no `basic`, `ed`, `run`, `sed`, `cd` or `sh`. It connects with a
developer tool and then cannot edit or compile. **A developer wants
PROGRAMMER.** If the login ever does start consulting the tier, this test is
what notices.

**THE TWO CONTROLS ARE THE POINT.** Three tiers connecting proves only that
three accounts exist unless something is also refused, and both refusals came
back with the right message rather than merely failing:

```
wrong password              ->  "Invalid username or password"
tier 1 -> tier 3's account  ->  "User not allowed in requested account"
```

The second is `vb.account`'s `ACC$GROUP` check, which is the whole reason an
account name is not just a label.

**WHAT THE SCRIPT DOES NOT DO, and it is deliberate**: it does not test the
GUI. It tests the library the GUI loads. The remaining gap is whether
mvDeveloper itself is happy, which needs a person and takes a minute.

**ONE UGLINESS RECORDED RATHER THAN HIDDEN**: `qm-connect.exe` takes the
password as `argv[4]`, so it reaches the process list. That is qm-connect's
interface and not a choice made by the test, which is why it generates
single-use passwords on accounts it deletes. The irony against the same day's
`SET.PASSWORD` work is noted in the script's header.

---

## 20 Aug 2026 - SET.PASSWORD refuses a trailing token, and a verifier cried wolf

**Commit:** this one. Twenty-ninth session, second cycle of the day.

**THE DEFECT, FOUND BY THE OWNER TYPING IT.** `SET.PASSWORD DON <password>`
read one token as the verb and one as the account and never looked for a third,
so the password was discarded in silence and the hidden prompts appeared as
though nothing had happened. Everything visible said it worked - and it did,
just not the way the person typing it believed. The password had already
reached SD's command stack by then.

`SET_ACC_PASSWORD` now asks the parser for one more token and stops with
message **5276** if there is one. The guard sits BEFORE the administrator
check on purpose: the password is exposed the moment it is typed, so telling
the person immediately matters more than telling them they were not allowed to
set that account anyway.

**IT IS DELIBERATELY NOT "ACCEPT IT IF GIVEN".** A password on a command line
is the thing the credential model exists to avoid; making the convenient form
work would undo it.

**`gplbld/verify-setpw.ps1` IS THE CHECK AND THE CONTROL IS THE POINT** - the
same command without the token must reach the password prompt, or "it refused"
proves nothing. 4/4. It is listed in `assert-current.ps1`'s `$neverShipped`,
because a verify script cannot reach an installed tree and without that line
WRITING a test would make every test refuse to run.

**AND A VERIFIER FAILED FOR A REASON THAT WAS NOT SD.** `verify-lcnames.ps1`
came back **135/142** minutes after the install, five named failures, all in
later blocks - and the obvious reading was that the BASIC change had broken VOC
resolution. It had not. The failing block replayed by hand answered correctly,
and a re-run on a quiet machine was **142/142**.

Its `Invoke-SD` drives SD through `Start-Job` with a 45-second timeout and an
explicit `<<TIMED OUT>>` path, so contention on a machine still settling after
an install is the likely cause. **Likely, not proven** - the raw output was not
kept, and saying so is better than inventing a cause. It fails in the SAFE
direction, a false FAIL rather than a false PASS, which is why it is recorded
as a trap and not a defect. **Re-run before believing it.**

**THE SECOND CYCLE OF THE DAY TOOK THE OWNER'S CREDENTIAL AGAIN.** `DON` had a
password at 08:54; the 09:09:06 cycle deleted the data tree and it went with
`APIPORT`. That cost was documented before the first cycle and NOT restated
before the second, which is the mistake worth recording: the cost of a cycle
should be said before running one, not after.

---

## Correction: 20 Aug 2026 - "$cred is empty" was access denied, not empty

**Commit:** this one. Twenty-ninth session.

**THE CLAIM THAT WAS WRONG.** This session reported `$cred records: 0` twice and
concluded that `SET.PASSWORD` had not been run. The store was not empty either
time: `verify-scramlogin` had already left `SDSCRAM2` in it, `verify-apiport`
`SDAPI3`, and by the second reading the owner had added `DON`.

**WHAT ACTUALLY HAPPENED.** `$cred` is ACL'd to SYSTEM and Administrators -
`secure-cred.ps1` does that, and `verify-credacl.ps1` exists to prove it. An
unelevated `Get-ChildItem` on it throws *Access to the path ... is denied*, and
the probe was written with `-ErrorAction SilentlyContinue`, which turned the
exception into an empty collection. `.Count` on that is `0`.

**WHY IT IS WORTH AN ENTRY.** The ACL was known, documented, and verified green
in the same session, and the check was still written as though it would answer.
**An unelevated probe of `$cred` cannot tell empty from forbidden**, and the
shape of the mistake - a silenced error read as data - is not specific to this
directory.

**THE RULE:** `-ErrorAction Stop` on anything that reads a secured path, or do
not ask. Elevated, the answer came back immediately: three records, all
version 2, `SCRAM-SHA-256`, `i=600000`.

**AND THE ELEVATED PROBE PRINTED THE KEY MATERIAL IT PROMISED NOT TO.** It
split records on `@FM` (`0xFE`) and `$cred` is a DIRECTORY file, so on disk the
field marks are NEWLINES. The split produced one field, every
`if field count >= 6, print lengths only` guard was skipped, and the whole
record - salt, StoredKey, ServerKey - went into the transcript. **A redaction
that depends on a successful parse is not a redaction**: it has to be the
default, with the parse only able to add detail. StoredKey is the value whose
holder can impersonate the server to that account, which is why the ACL exists
at all.

---

## 20 Aug 2026 - assert-current demanded a full cycle for a markdown file

**Commit:** this one. Twenty-ninth session.

**FOUND BY DOING IT.** Editing `gplsrc\sdclilib\VENDORING.md` to record the
client packaging work turned `assert-current` red - on a tree that had cycled
an hour earlier and passed the whole suite. It printed *"run 'make sd'"* and
*"Run one cycle"*, and **both would have been pointless**: a rebuild has
nothing to read in a `.md` and an install has nothing to receive, since nothing
under `gplsrc` is installed at all. `stage.py` ships `sdsys`.

**WHY IT MATTERS MORE THAN THE ten minutes it costs.** The next session would
either have spent an install on a documentation edit, or learned that the
guard cries wolf - and the guard's whole value is that it is believed. This
file already records three earlier false stales of the same shape:
`localtest\`, `__pycache__\` and `sdclilib\tests\`. This is the fourth route in.

**FIXED IN BOTH CHECKS, DIFFERENTLY, BECAUSE THEY ASK DIFFERENT QUESTIONS.**

- **A2** asks *"is any SOURCE newer than the binaries"*. Nothing compiles a
  `.md` or `.txt`, so the extension is excluded outright, beside the existing
  build-product filter.
- **B** asks *"is any source newer than the INSTALL"*, and there a blunt
  extension filter would hide a document somebody later ships. So it asks
  `$shipsAs` - the existing valve that re-watches a `$neverShipped` file the
  moment it appears quoted or path-prefixed in `stage.py` or `sd.iss`. A `.md`
  that ships is watched; one that does not, is not.

**THE DIRECTION OF THE RISK IS WHY THEY DIFFER**, and this file has said it
before: a false stale costs one install, a false current costs an
investigation. A2 cannot produce a false current from a document because
documents are not compiled; B could, so B keeps the valve.

**MEASURED WITH ITS CONTROL, which is the only thing that makes it mean
anything** - a guard that stopped catching real staleness would be worse than
the false alarm it was fixing:

```
a new .c  under gplsrc, newer than the install  ->  exit 1    STALE   (control)
a new .md under gplsrc, newer than the install  ->  exit 0            (treatment)
both removed                                    ->  exit 0
```

---

## 20 Aug 2026 - The client library becomes something you can install

**Commit:** this one, plus `winsdclilib` `254fb1d`. Twenty-ninth session.

**THE PROBLEM, IN THE OWNER'S WORDS: "the user has to know where to look for
the dlls in the installed sd for windows system".** The only way to obtain the
client library was to find it inside an installed SD server, under
`C:\Program Files\SD`, on a machine that had one - which is the wrong shape
for a client, whose whole purpose is to run on a machine that is NOT the
server and reach it over an ssh tunnel.

**EACH CLIENT PROJECT NOW BUILDS ITS DLL TWICE.** Owner's decision, and the
second name is the same library rather than a variant:

| Project | keeps | adds |
|---|---|---|
| `winsdclilib` | `sdclilib.dll` | `sdclient.dll` |
| `sdclilib32` | `qmclilib.dll` | `qmclient.dll` |

The old names do not move - `qmclilib.dll` in particular is the name a QMClient
application asks for and is the entire reason that project exists. The new
names are for new work and are what the installers put on PATH.

**A SECOND LINK, NOT A COPY OF THE FILE, and the reason is not obvious.** An
import library records the name of the DLL its symbols come from. Copy
`sdclilib.dll` to `sdclient.dll` and the only implib you have still says
`sdclilib.dll`, so an application linked against it loads the wrong file at run
time - or nothing at all on a machine where the package installed only the
other name, and the error then names a DLL the developer never asked for.

**IN THE 32-BIT PROJECT IT IS WORSE, because the `.def` sets that name too.**
`LIBRARY qmclilib.dll` in `qmclilib.def` overrides whatever `-o` says. So
`qmclient.def` is **generated** from it by rewriting that one line, and is not
kept: two hand-maintained copies of a 99-name export list would eventually
differ by one name, and that failure shows up only at run time and only for
whoever called it.

**BOTH `make check` TARGETS NOW RUN A TEST THROUGH EACH IMPORT LIBRARY.** That
is the only thing that catches either mistake, and the 32-bit one repeats the
QM ALIAS test rather than the smoke test deliberately: it resolves QM exports,
so it fails if the generated `.def` lost the export list, AND it loads
`qmclient.dll`, so it fails if the `LIBRARY` line left the implib pointing at
`qmclilib.dll`. Those are the only two ways the second name can be wrong.

**TWO INSTALLERS**, `winsdclilib/sdclient.iss` and `sdclilib32/qmclient.iss`,
both packaging an already-built tree exactly as `gplbld/sd.iss` does and
building nothing themselves - so ISCC fails naming the missing file if you did
not build first. Own AppIds, own directories, so neither conflicts with nor
requires the server and a machine may carry all three. **PATH is appended to,
never prepended**, so an existing server install keeps finding its own
`sdclilib.dll` first - which matters, because `make check-local` in this tree
depends on PATH resolving to the installed server pair.

The 32-bit one is deliberately **not** `ArchitecturesInstallIn64BitMode`, so it
stays a 32-bit install and `{autopf32}` resolves to `Program Files (x86)` on
64-bit Windows and `Program Files` on 32-bit. Marking it would also refuse to
run on 32-bit Windows, the one platform with no alternative package.

**BOTH INSTALLERS WERE INSTALLED AND VERIFIED LATER THE SAME DAY**, once the
owner was at the keyboard - the UAC prompts that had failed then succeeded,
which is the same finding this file already records rather than a new one.

**TESTED AS A CONSUMER SEES THEM.** `smoke_test.c` compiled against the
INSTALLED headers and import libraries only, then run from a neutral directory
whose `PATH` held the installed `bin` and `System32` and nothing else, so the
installed DLL was the only one reachable. All four combinations passed:
`-lsdclient`, `-lsdclilib`, `-lqmclient`, `-lqmclilib`.

**AND THE PATH ORDERING WAS MEASURED RATHER THAN ASSERTED.** Three
`sdclilib.dll` now sit on the machine `PATH` - server at [8], the two client
packages at [9] and [10]. `SDConnectLocal` is the discriminator: it starts
`sd.exe` from beside the DLL, and the client packages have none, so a wrong
resolution fails outright. `local-connect-test.exe` on the raw machine `PATH`
answered *"PASS: DON admitted, SDSYS refused"*.

**ONE THING THE TEST ITSELF GOT WRONG FIRST, and it is the trap both Makefiles
already guard**: the compile step did not put the compiler's own directory on
`PATH`, so `cc1.exe` could not resolve its DLLs and gcc exited 1 with
completely empty output - four "LINK FAILED" lines and no reason. A
hand-written test has to carry that guard too.

**TWO LATENT DEFECTS IN `winsdclilib`'s MAKEFILE, FOUND BY THE FIRST CLEAN
BUILD FROM A PLAIN MSYS2 SHELL**, and both are faults the 32-bit project met
first and already guards against:

- **`CC ?= gcc` never fired.** Make defines `CC` itself, as `cc`, so `?=` is a
  no-op and the compiler was whatever `cc` named. From the UCRT64 shell the
  README tells you to use, that is the right one and the bug is invisible.
  From a plain MSYS2 shell it is the POSIX gcc, and the build fails on
  `strcpy_s` and `sprintf_s` - UCRT functions the msys runtime does not have -
  **which reads as broken source rather than as the wrong compiler**.
- **the PATH prepend split at the drive-letter colon.** Harmless while `CC` was
  a bare `gcc` and the prepend never ran; fatal once `CC` defaults to an
  absolute path, leaving gcc exiting 1 with completely empty output.

**The 32-bit project's makefile carries the long form of both explanations, and
it is worth noticing that neither was copied back when the 64-bit one was
written.** A guard learned in one of three sibling projects does not propagate
by itself.

**TWO STALE README CLAIMS CORRECTED in `winsdclilib`:** "the prebuilt Windows
DLL and import library included with this repository" - `.gitignore` excludes
every DLL, so nothing prebuilt ships and a clone has to build - and
"`SDConnectLocal` is Linux-specific and is not part of this Windows DLL", which
stopped being true when `SDConnectLocal()` was built (section 7 step 11). It
starts `sd.exe` and talks to it over a pipe, and `make check-local` exercises
it.

**`sdclilib32` BECAME A GIT REPOSITORY THE SAME DAY**, closing the
longest-standing exposure this file records: it had been built from since
15 Aug and versioned nowhere, so every sync of it existed on disk alone.
Owner created `github.com/dmontaine/sdclilib32` (public); initial import
`cf5a72a`, **12 files and no binaries**, checked against the remote tree rather
than assumed. `qmclient.def` is excluded along with the build products — it is
generated, and committing it would create the second hand-kept copy of a
99-name export list that generating it exists to prevent.

**All three repositories are pushed:** `sd4windows` `d92217d`, `winsdclilib`
`254fb1d`, `sdclilib32` `cf5a72a`.

---

## 20 Aug 2026 - SCRAM phase 5: the cleartext login is retired

**Commit:** this one. Twenty-ninth session.

**WHAT CHANGED.** `APISRVR`'s `vb.login` no longer authenticates anything: it
answers message **5275** and drops the connection. Requests 47 and 48 are the
only network login. `vb.local.login` (25) is untouched - `SDConnectLocal` sends
no password and never did.

**24 STAYS IN THE PRE-AUTHENTICATION GATE, THOUGH IT IS RETIRED.** Removing it
from that list would have answered an old client with 5270 *"Not logged in"* -
true, and useless: it reads as a client bug rather than as a protocol that
moved. Three lines buy a reply that names the cause, and an old client is
exactly the caller that will be reading it.

**THE DESIGN DOCUMENTS LISTED ONE CLIENT AND THE TREE HELD FOUR.**
`grep -rn SrvrLogin` finds them; neither `docs/SCRAM_AUTH.md` nor
`docs/SCRAM_HANDOFF.md` mentioned more than `sdclilib.c`.

| | State |
|---|---|
| `gplsrc/sdclilib/sdclilib.c` | speaks SCRAM since phase 4 |
| `sdsys/GPL.BP/SDCLIENT` (`!sdclient`) | **sent request 24 - would have broken silently** |
| `gplbld/verify-scramlogin.ps1` | the test client; sends 24 on purpose |
| `gplsrc/sdclient.c` | **dead**, see below |

**`!sdclient` IS THE BASIC-CALLABLE HALF OF THE API**, what `sdclilib.dll` is
to an application outside SD. It is catalogued in `gcat` on every install, has
no caller anywhere in this tree and no test, so nothing would have reported the
break. Owner's decision, 20 Aug 2026: give it SCRAM rather than leave it broken
or delete it.

**AND IT IS NOT THE REMOVED qmnet, which is the fact that made the decision
easy.** qmnet was `net_open()` in C, port 4245, `server;file` VOC references,
credentials in `sd.conf` under a substitution cipher, removed 18 Aug 2026
(`op_dio1.c:627`) - and that removal note keeps qmclient explicitly, because
the API is mitigated by requiring an ssh tunnel. `!sdclient` opens **4243**,
the API port. Different facility, opposite decision, and one letter apart in
the QM names they inherit.

**THE CLASS IS `$internal` NOW.** SCRAM needs `SDEXT`, which BCOMP admits only
to a program compiled `$internal` (`BCOMP:3777`). The flag is a property of
that object code and not of its callers: the class calls no `KERNEL` function
and runs nothing locally - `execute()` and `call()` send their argument to the
remote server - so there is no method through which a caller could borrow it.
`sdsys/bp/TESTSDCLI` is deliberately **not** `$internal` and drives the class
anyway, which demonstrates that rather than asserting it. Recompiling
`SDCLIENT` now needs `sd -internal` from an elevated window.

**`gplsrc/sdclient.c` STILL BUILDS A CLEARTEXT REQUEST 24 AT LINE 609 AND IS
LEFT ALONE.** `Makefile:66` strips it from `SRCS`, it is absent from
`gpl.src`, and no target depends on `sdclient.o` - the rule at `Makefile:214`
is an orphan. Nothing links it, so phase 5 does not break it. Deleting source
is its own decision and was not in scope; recorded so the next reader does not
re-derive that it is dead.

**THE VERIFIER GAINED SIXTEEN CHECKS AND CLOSED BOTH RECORDED GAPS.**
`verify-scramlogin.ps1` went from 24 to **40**, all passing on the 07:52:25
install:

- **every refusal asserts its message TEXT**, read from the installed
  `messages` record rather than hard-coded - 5017 for a wrong password *and*
  for an unknown account, 5272 for replay / tampered nonce / `y,,` / `m=`,
  5273 for 48-without-47, 5275 for request 24. A refusal that fires on the
  wrong branch refuses just as firmly and used to pass.
- **5274 is exercised**, by renaming `$cred` for one client-first and renaming
  it back in a `finally`, with a second attempt in the outer `finally`. It is
  the server-fault path and nothing had ever reached it. A run that ended with
  the credential store renamed would refuse every login on the machine, which
  is why the restore is in two places.
- **step 9b drives `!sdclient` through `TESTSDCLI`**, with a wrong-password
  control inside the test program.
- **"request 24 still accepted" was inverted, not deleted.** It is now the
  proof the old path is gone. Its control in step 9 still works and the reason
  is worth stating: `Test-SentContains` reads what the SCRIPT sent, not what
  the server accepted, so the packet still carries the password and the server
  now throws it away.

**WHAT IT COST.** One `cycle.ps1 -SkipInstall` to find out the BASIC compiled -
it did, first time, 0 errors and no `is not assigned a value` - and one full
cycle. **The full cycle deleted `C:\ProgramData\SD`**, so `APIPORT` went back
to commented out and `$cred` came back empty, which is the price the previous
session declined to pay to keep the owner's mvDeveloper working. It has to be
put back by hand: uncomment `APIPORT`, restart, `SET.PASSWORD` per account.

**THE LESSON WORTH CARRYING: grep for the REQUEST NUMBER, not for the client
you have in mind.** The design documents had been read carefully and were
simply incomplete. What found the fourth speaker was `grep -rn "SrvrLogin"`
across the whole tree, not reading the phase description again.

---

## 19 Aug 2026 - End of the twenty-eighth session: what is left standing

**Commit:** this one. Handoff summary; the detail is in the entries below.

**WHAT THIS SESSION DID.** SCRAM phases 3 and 4 - the server exchange and the
client - both written and both verified; the three client locations
synchronised with this tree made the source of truth; the orphaned Windows test
accounts removed; and mvDeveloper, the 32-bit shipping client, authenticating
over SCRAM against SD.

**THE TREE IS COMMITTED AND PUSHED**, both `sd4windows` (`main`) and
`winsdclilib` (`master`). `sdclilib32` is still not a git repository, so its
half of the sync exists on disk only - the single largest gap in what a cold
start can recover.

**A CYCLE IS OWED, FOR ONE LOGGING-ONLY CHANGE, AND IT WAS LEFT UNRUN
DELIBERATELY.** `assert-current` refuses: `gplsrc/sdclilib/sdclilib.c` carries
the `SD_CLIENT_DEBUG` auto-logging of `ba29603` and the install is 22:25:09.
**Cycling would delete `APIPORT=4243` and every `$cred`**, and the owner's
editor was working when the session ended - so the next session should choose
knowingly rather than run the cycle by reflex, and put both back if it does.
Nothing functional is missing from the install; only the ability to
self-enable packet logging.

**THE JUDGEMENT BEHIND THAT IS WORTH STATING**, because it cuts against this
project's usual reflex. The standing rule is cycle-then-measure, and leaving a
tree stale is normally the wrong answer. Here the stale item is a diagnostic
that changes no behaviour, and the cost of cycling is landing the owner back on
the problem that took most of the session to find. Measurement can wait; a
working editor at the end of a session should not be thrown away to satisfy a
guard that is red for a logging statement.

**LIVE STATE THAT NOTHING IN THE TREE RECORDS:**

- `APIPORT=4243` enabled by hand in the installed `sd.conf`, loopback only.
- `don` has an API credential; `SET.PASSWORD` was run this session.
- `C:\Program Files (x86)\BLC\mvDeveloper\qmclilib.dll` is the current 32-bit
  build, with the previous one beside it as `qmclilib.dll.bak-before-autodebug`.
- `SD_CLIENT_DEBUG` has been unset. A running editor keeps its inherited copy
  and its open log handle until restarted, so
  `%LOCALAPPDATA%\SD-verify\mvdeveloper-client.log` may still be growing; it
  holds everything the session reads and writes and can be deleted.
- `SDQM1` is in the `ACCOUNTS` register and wants `DELETE.ACCOUNT`.
- Three profile directories outlive their deleted accounts:
  `C:\Users\sdacct6`, `sdacct9`, `sdacct10`.

**NEXT:** phase 5, retiring `SrvrLogin`. The mvDeveloper run is the evidence it
is safe - the shipping 32-bit client sends 47 and 48 and never sends 24.

---

## 19 Aug 2026 - mvDeveloper authenticates with SCRAM, and the instrument that showed it

**Commit:** this one, plus `ba29603` and `winsdclilib` `5553ae3`.

**THE RESULT.** The 32-bit editor - the shipping client the whole KDF decision
was made for - connected over SCRAM-SHA-256 and worked. From its own packet
log: requests 47 and 48 sent, **24 never**, `i=600000`, the server's `v=`
returned and accepted by the client, account attach accepted, then
`SSELECT VOC` and a working session. **No password in the 1,005 bytes the
session exchanged.** Phase 6's real acceptance test, passed before phase 6.

**HOW IT GOT THERE, INCLUDING THE PART THAT WAS MY OWN DOING.** The editor
first reported "could not connect": `APIPORT` was commented out, because the
day's cycles had rebuilt `C:\ProgramData\SD` and a fresh install ships it that
way. Re-enabled. Then "connection error": `$cred` was empty, because a cycle
takes the credentials too - by design, the plaintext was never stored - so
every account needs `SET.PASSWORD` again after one. **Both were consequences of
cycling, not faults**, and both will recur.

**THEN IT STOPPED BEING DIAGNOSABLE, WHICH IS THE USEFUL PART OF THIS ENTRY.**
Everything testable was correct: the port answered, `don` had a credential
(request 47 returned a real server-first), `sdu_don` granted the account, the
64-bit DLL passed end to end, the **32-bit** DLL connected under
`qm-connect.exe`, and the DLL beside `mvDeveloper.exe` was byte-identical to
that one. A working library, a working server, and a client saying "connection
error" - which is all `QMConnect` gives an application that does not print
`QMError()`.

**SO THE LIBRARY WAS MADE TO SAY WHAT HAPPENED.** `SD_CLIENT_DEBUG` used to
choose the log's PATH only; logging still had to be started by the application
calling `SDDebug(1)`. Fine for code you can edit, useless for a closed-source
client - which is exactly the case that needs it. It now turns logging on by
itself. Placed after the initialisation loops, because `SDDebug()` reports a
log it could not open by writing into `session[].sderror` and the clearing loop
would have wiped that very message.

**WHAT ACTUALLY FIXED THE CONNECTION IS NOT ESTABLISHED, and inventing a cause
would be worse than saying so.** Between the failing attempt and the working
one the editor was restarted and `SET.PASSWORD` had been run; the DLL was also
replaced, but only with one that adds logging, so it cannot be the cause. The
likeliest reading is that the failing attempt predated the credential.

**The lesson is about instrumentation, not about SCRAM.** A generic client-side
error message turned a five-minute question into most of a session, and the
answer was to stop inferring from the outside and make the library talk.

**Housekeeping:** the deployed `qmclilib.dll` is the current build, with the
previous one kept beside it as `qmclilib.dll.bak-before-autodebug`.
`SD_CLIENT_DEBUG` has been unset - it logs everything a session reads and
writes, so it is not something to leave on. `SDQM1` is in the `ACCOUNTS`
register from the 32-bit reproduction and wants `DELETE.ACCOUNT`.

---

## 19 Aug 2026 - The orphaned Windows test accounts removed

**Commit:** this one. Eight local users and ten local groups, left behind by
test runs across several sessions.

```
users   sdacct6, sdacct8, sdacct9, sdacct10, sdacct11, sdacct12, sdacct13, sdacl1
groups  sdu_ for each of those, plus sdu_sdacct4 and sdu_sdadopt1, whose
        users had already gone
```

**Each was re-checked before removal rather than trusted from a list**, since
deleting a local account cannot be undone: not in a protected set, exists, has
the `SD account` description `CREATE.ACCOUNT` writes, and has **no record in
the SD `ACCOUNTS` register**. That last one is what "orphaned" means here, and
it is the check that would have stopped a live account being taken.

Protected and untouched: `don`, `Administrator`, `Guest`, `DefaultAccount`,
`WDAGUtilityAccount`, both `CodexSandbox*` accounts - which belong to other
tooling on this machine and are nothing to do with SD - and the `sdusers`,
`sdadmins`, `sdsshonly` and `sdu_don` groups.

Verified beforehand that none of the eight owned a running process, and that
none was a member of `Administrators` or `sdadmins`. `sdusers` and `sdadmins`
now contain `don` alone; group membership went with the users.

**THREE PROFILE DIRECTORIES SURVIVE THEIR ACCOUNTS** - `C:\Users\sdacct6`,
`sdacct9` and `sdacct10`, the three that had ever been logged into. Left
deliberately: removing an account is one thing, removing a directory that might
hold data is another, and section 7 step 1c has not settled whether cleanup
should take them.

**THE UNDERLYING CAUSE IS UNCHANGED AND IS WORTH KEEPING IN VIEW: a cycle
deletes the data tree but not the Windows accounts.** So the SD register looks
clean after every cycle while the Windows side keeps accumulating, which is
exactly how eight of them built up unnoticed. `verify-apiport.ps1` and
`verify-scramlogin.ps1` remove their own in a `finally`;
`verify-createaccount.ps1` deliberately does not.

---

## 19 Aug 2026 - The three client locations synchronised, and the arrow turned round

**Commit:** this one, plus `winsdclilib` `07a71c6` and `e35376a`, both pushed.
Closes the phase 6 blocker recorded two entries below.

**THE PROBLEM.** `Projects/winsdclilib` had not moved since 15 Aug 2026 while
this tree added `SDConnectLocal`, `sysdir()`, the socket-or-pipe transport
layer and then SCRAM-SHA-256. `Projects/sdclilib32` built from
`../winsdclilib`. So the 32-bit `qmclilib.dll` intended to ship with
mvDeveloper was being built from source with **no SCRAM in it** - still
sending the password in clear - and **nothing in either project would have
reported it**. `sdclilib32`'s own Makefile comment had predicted exactly this
failure in the abstract: "a forked copy quietly goes stale".

**CHECKED BEFORE OVERWRITING ANYTHING**, because VENDORING.md recorded
`winsdclilib` as *upstream* and this directory as the vendored copy, and
overwriting upstream with a copy is how work gets lost:

- every function in `winsdclilib/sdclilib.c` was present here;
- every `#define` likewise;
- the `_MSC_VER` guards survive in both;
- the only thing it had that this tree lacked was the **comment** explaining
  the `SV_EMSG_PAIR`/`SV_ECONTXT` transposition. The values were already
  identical - `winsdclilib` fixed it in `a1987b0` and this tree fixed it
  independently, each with its own note.

So the repo copy was a genuine content superset and the sync could only add.

**THE ARROW NOW POINTS OUTWARDS.** `gplsrc/sdclilib` is the source of truth;
`winsdclilib` is a mirror; `sdclilib32` holds no source at all and its
`SRCDIR` was repointed from `../winsdclilib` to this tree. **One hop instead
of two**, so the middle copy cannot lag again. VENDORING.md was rewritten
around the new direction rather than deleted - it still records why
`SDConnectLocal` and the transport layer exist.

**`sdclilib.c` WAS CRLF, AND IS NOW LF.** The only such file in the directory,
inherited with the vendored import and predating the SCRAM work - the phase 4
diff was 266 lines, not a whole-file rewrite, which is what proves it was
already CRLF. This tree's rule is that every file stays LF and `winsdclilib`
normalises to LF, so leaving it would have guaranteed a permanent byte
difference between two copies meant to be identical. Exactly one CR removed
per line, and `git diff --ignore-cr-at-eol` is empty.

**`make check` EARNED ITS KEEP.** `internal_state_test.c` includes
`sdclilib.c` directly, so it needed `-lbcrypt` as well - missing in all three
Makefiles and both `build.cmd` scripts. Only the test link failed; every DLL
built fine, so nothing but running the tests would have found it.

**Verified after the sync**, in both external projects and by **both** build
routes, Makefile and `build.cmd`: smoke and internal-state pass in each, plus
the QM alias test in `sdclilib32`. `qmclilib.dll` is PE32 i386 and imports only
`bcrypt`, `KERNEL32`, `msvcrt` and `WS2_32` - all Windows, so it remains a
single file that can be copied beside an application, which is the constraint
that chose PBKDF2 over Argon2 in the first place.

**Still open:** `sdclilib32` is not a git repository, and is now the weakest of
the three - its half of this sync exists on disk and nowhere else.

---

## 19 Aug 2026 - The phase 4 packet check ran: 47 and 48 sent, 24 never

**Commit:** this one. Completes the entry below, which recorded the check as
written but not run because UAC was declined. It was run afterwards, elevated,
as `verify-apiport.ps1 -Prefix sdapi2` against the **21:58:11** install.

```
request types sent: 1, 2, 3, 21, 47, 48
   client sent SCRAM client-first (47)      PASS
   client sent SCRAM client-final (48)      PASS
   client sent NO cleartext login (24)      PASS
   password absent from the bytes sent      PASS   963 bytes reassembled
   same search finds the user name          PASS   <- the control
```

**So "the client speaks SCRAM" stops being an argument from source.** The
server still serves request 24; a client that had fallen back would have been
admitted just as readily and every other check would still have been green.

The cycle that install came from was owed for a one-paragraph `changelog`
entry - `sdsys` is watched and ships, so a text file there makes the tree stale
exactly as a program would. That is the guard working, and the cost is a
reminder to write the changelog entry **before** the cycle rather than after.

---

## 19 Aug 2026 - SCRAM phase 4: the client stops sending the password

**Commit:** this one. **Install 21:43:02**, `sd.exe` `417CDC4FCA73FB27`,
`assert-current` exit 0.

**`SDConnect` no longer sends `SrvrLogin`.** `gplsrc/sdclilib/scram_client.h`
holds the primitives and the derivation; `scram_login()` in `sdclilib.c` runs
the exchange. `QMConnect`'s signature, return and `QMError()` are unchanged,
which is what makes this viable for a third-party client whose source nobody
has. `login_data` is gone from the file entirely.

**A HEADER OF static FUNCTIONS, NOT A SECOND .c FILE.** The client ships as one
binary - source may be split, the binary may not - and it lets
`gplbld/verify-scramclient.c` include the same file and test it against the RFC
7677 vectors. A separate implementation written to agree with the first would
prove only that somebody made the same assumption twice. It is the arrangement
`gplsrc/sd_scram.c` and `gplbld/verify-scram.c` already use server-side.

**27/27 on the vectors, AND RUN 32-BIT AS WELL.** `/c/msys64/mingw32/bin/gcc`
with `-static-libgcc` produces a PE32 i386 binary that passes identically.
**That is the constraint the entire KDF decision rested on** - Argon2 was
rejected because a 32-bit process cannot afford its memory - so it was measured
rather than assumed. Everything comes from `bcrypt.dll`, part of Windows, so
the DLL stays a single file; base64 is implemented in the header rather than
taken from `crypt32`.

**Verified end to end by `verify-apiport.ps1 -Prefix sdapi1`:** right password
admitted with `WHO -> 1 SDAPI1`, wrong password refused, `SDSYS` refused. That
last one matters beyond the login - it is the `ACC$GROUP` grant check reading
the identity SCRAM established, so section 7 step 6c still works on top of the
new path.

**BUT A SUCCESSFUL LOGIN DOES NOT PROVE THE CLIENT SPOKE SCRAM, and noticing
that is the useful part of this entry.** The server still serves request 24, so
a client that had fallen back to the cleartext login would have been admitted
just as readily and every check above would still be green. Source says a
fallback is impossible - nothing calls `SrvrLogin`, `login_data` is gone - but
that is an argument, not a measurement.

**So `verify-apiport.ps1` gained a packet-type check**, using the client's own
`SDDebug(1)` log via a new `SD_CLIENT_DEBUG` guard in
`tests/remote_connect_test.c`: 47 and 48 present, **24 absent**, and the
password absent from the traffic with the user name found by the same search
as its control. **It has not been run** - UAC was declined on the re-run - and
is owed as `-Prefix sdapi2`.

**THE PASSWORD SEARCH NEARLY BECAME A CHECK THAT COULD NOT FAIL.** `debug()`
dumps 16 bytes per line with a printable column beside them, so a 20 character
password is SPLIT ACROSS TWO LINES and a plain text search of the log would
never have found it - passing whether or not the password had been sent. The
check reassembles the byte stream from the hex columns first, and the user name
control exists to prove the search can find something.

**`assert-current` now excludes `gplsrc\sdclilib\tests\`, in both checks.**
Section 7 step 11 had recorded that editing `remote_connect_test.c` owed a full
cycle before `verify-apiport.ps1` would run again - and `verify-apiport` calls
`assert-current` first, so **improving the test blocked the test**. Nothing in
that directory ships or is compiled into anything; a cycle that reinstalls
none of it is not a guard, it is a toll. Same reasoning as the `localtest\` and
`__pycache__` exclusions already there.

**A PHASE 6 BLOCKER, FOUND RATHER THAN CREATED: THE 32-BIT SHIPPING DLL BUILDS
FROM A STALE COPY.** `Projects/winsdclilib/sdclilib.c` is 112 KB against this
repository's 138 KB, and the repo copy is a strict **superset** - every
function in `winsdclilib` is in it, plus `SDConnectLocal`, `sd_exe_path`,
`sysdir` and the four `transport_*` functions. So `winsdclilib` is an older
ancestor with nothing of its own, and `Projects/sdclilib32/Makefile` points
`SRCDIR` at it. **The `qmclilib.dll` mvDeveloper will use therefore has no
SCRAM in it and will not get any from editing this repository.** Phase 6 is
"rebuild the 64-bit and 32-bit DLLs" and cannot be done until that is settled -
point `SRCDIR` here, or bring `winsdclilib` up to this copy. Owner's call; not
touched here because phase 4 could be built and verified without it. The
SCRAM_HANDOFF note that said "both DLLs build from one sdclilib.c" was
describing an intention, not the tree.

**A CORRECTION THIS ENTRY FORCES.** The post-cycle suite passed on the
21:03:41 install; phase 4's cycle replaced that tree at 21:43:02, so those
numbers again describe a tree that no longer exists. The only source change
between them was the client library - which is **not** a licence to carry them
forward, `gcat` being a build product. Owed again, and cheap: no install, only
running.

**Still open:** phase 5, retiring `SrvrLogin`, which is the point of no return.

---

## 19 Aug 2026 - The post-cycle suite re-run on 21:03:41, green but for the one an agent cannot run

**Commit:** this one. Closes the "post-cycle suite is owed" correction made in
the entry below, which was made in the same session that then discharged it.

**Everything passed.** `verify-lcnames` **142/142**, `verify-keys` **10/10**,
`verify-editkeys` **14/14**, `verify-nocase` and `verify-credacl` exit 0,
`verify-osusers` all 23 PASS, `make check-local` PASS (`DON` admitted, `SDSYS`
refused), `verify-scramlogin` **24/24**, and
`post-cycle-elevated.ps1 -TierPrefix sdtierl -Account sdacct19` all exit 0 -
`verify-fold` **10/10**, `verify-tiers` all passed with standard `COUNT VOC`
**393**.

**`probe-keys.ps1` WAS NOT RUN, AND ITS REFUSAL IS THE POINT.** It answers
*"standard input is redirected, so this is not a console"* and exits 2. It is
the only instrument here that measures a key press rather than a byte
sequence, and §5.18's lesson is that a pipe is not a console - so refusing is
it working, not it failing. It needs a human at cmd, PowerShell or Windows
Terminal.

**UAC WAS REACHABLE, WHICH IS WHY THE ELEVATED HALF RAN AT ALL.**
`verify-osusers`' two self-elevating phases and `post-cycle-elevated.ps1`
launched with `Start-Process -Verb RunAs -Wait` all prompted and succeeded.
That does not change the standing rule - it works when someone is at the
keyboard, and nothing should be built assuming it.

**THE INTERMITTENT `verify-lcnames` CHECK PASSED, AND THE CAPTURE WAS BOTCHED
A THIRD TIME IN THE SAME WAY.** 142/142 on the first run after the cycle,
which is a third data point against "first run after a cycle" being the
trigger. But the run was piped into `Select-String`, so its transcript holds
**one** `PASS` line instead of 142 - exactly the mistake PROJECT_STATUS item 3
was written to prevent, made by the session that had just read the warning.

**`Start-Transcript` cannot save a piped run, and this is the general shape of
it.** It records what reaches the **host**; a caller-side pipe consumes the
objects before they get there. So a script writing its own transcript gives no
protection against the caller piping it - the fix has to be at the call site,
which is why the instruction is now written as a bare command with nothing
after it rather than as advice.

**Litter left: five `ACCOUNTS` records, no Windows accounts.** `SDACCT19`,
`SDSCRAM1`, `SDTIERL1`, `SDTIERL2`, `SDTIERL3`. Every Windows user, group and
`user_accounts` directory was cleaned up by the scripts; the SD half is left
by design so a half-failed `CREATE.ACCOUNT` cannot hide. Next free `sdacct20`,
`sdtierm`, `sdscram2`.

---

## 19 Aug 2026 - SCRAM phase 3 verified: 24/24, and the exchange is what runs

**Commit:** this one. Closes the two entries below. **Install 21:03:41**,
`sd.exe` `D796556A8106325A`, `assert-current` exit 0 before and after.

**`gplbld/verify-scramlogin.ps1 -Prefix sdscram1` passed 24 of 24.** Run by the
repository owner from an elevated prompt; the transcript is at
`%LOCALAPPDATA%\SD-verify\verify-scramlogin-20260819-210415.log` and was read
back rather than taken on the summary line, per CLAUDE.md's rule that nothing
becomes "verified" without being observed.

**The results that carry weight, as opposed to "the login worked":**

- **Mutual authentication.** The server answered
  `v=le6vgqqoodvYIbI1oP07beHpCGv8oIroJZi1i64SEoY=` and the test client
  computed the same value independently in .NET from `ServerKey`. Two
  implementations agreeing, not one agreeing with itself.
- **The password is not on the wire — and the detector is not blind.** The
  byte search found no password in the SCRAM traffic, and the *same* search
  found it in a request-24 login. Without that control the check would have
  passed just as well if it could never find anything.
- **Replay is refused, and the freshness it depends on was measured
  separately.** Two exchanges for one account got different server nonces, and
  a client-final captured from the exchange that *succeeded* was refused when
  replayed against a fresh client-first.
- **Every refusal fired:** wrong password, tampered nonce, client-final with no
  client-first, unknown account, the `y,,` downgrade, an `m=` mandatory
  extension.
- **`iterations` came back 600000**, so the credential is at full cost rather
  than some debugging value.
- **Request 24 still works**, which makes "phase 3 is additive" a measurement.

**Two gaps in the suite, recorded so they are not mistaken for coverage.** The
`5272` refusals assert only that `server.error` was non-zero and never check
the message text; `5274` is unexercised, being the server-fault path. `5017`
and `5273` were both seen reaching the client. Neither gap needs a cycle to
close.

**§8's ACLs got one result out of this for free.** `accounts record created`
passing means **`CREATE.ACCOUNT` still works with `secure.account.dir` inside
it** - which PROJECT_STATUS had named as the first thing to check, because
`!ps_script` needs the session to hold privilege. It says nothing about
whether the ACL applied is correct; `verify-accountacl.ps1` is still unwritten.

**And the `$CRED` ACL survived a tree built from nothing.** An unelevated
`Test-Path` on `C:\ProgramData\SD\sdsys\$cred\SDSCRAM1` answers *Access is
denied*.

**A CORRECTION THIS CYCLE FORCED.** PROJECT_STATUS carried the line "THE
POST-CYCLE RUN IS COMPLETE AND EVERYTHING PASSED. Nothing is owed." That was
true of the tree the cycle deleted. Every figure in that file quoted against
the 14:54:36, 15:16:15, 15:30:36, 16:38:01 and 16:54:55 installs is now
history, and only `verify-scramlogin` has run against 21:03:41. The line has
been replaced with one saying so. **This is the failure mode the cycle rule
exists to prevent, appearing in the document that states the rule.**

**Left behind:** `SDSCRAM1` in the `ACCOUNTS` register, deliberately, for
`DELETE.ACCOUNT`. Next free prefix `sdscram2`. `sd.conf` restored, `APIPORT`
gone, SD running.

**Still open:** phase 4, the client half in `sdclilib.c`; and the post-cycle
suite against 21:03:41.

---

## 19 Aug 2026 - A cycle spent on one line of sd.iss, and the rule that was already written down

**Commit:** this one. Follows the SCRAM phase 3 entry below; the cycle that
entry asked for is what hit this.

**THE FAULT.** `gplbld/sd.iss:1046` wrapped `#13#10#13#10 +` onto its own line.
ISPP treats a line whose first non-blank character is `#` as a preprocessor
directive, so it read the Pascal character constant as a directive named
`13#10#13#10` and answered *"Error on line 1046 ... Unknown preprocessor
directive. Compile aborted."* It came from the account-ACL work of the same
day, whose `sd.iss` changes were written and never put through ISCC.

**THE RULE WAS ALREADY IN THE FILE.** `sd.iss`'s `InitializeWizard` comment
says, verbatim, not to start a line with `#` because ISPP reads it as a
directive, and names the exact error text. It sits ~480 lines above where the
new message was added. **A comment that far from the code being written is not
a guard**, which is the general lesson: the same distance defeats any rule
recorded only as prose near an unrelated function.

**WHAT IT COST.** `cycle.ps1` stops the service at step 1, stages and
bootstraps at step 2, checks the staged tree at step 3, and only reaches ISCC
at step 4 - so the whole of that ran before a one-line syntax error surfaced.
It also left **SD stopped**, because `Fail` exits without restarting it and
said nothing about having done so.

**BOTH ARE STRUCTURAL NOW.**

- `cycle.ps1` lints `sd.iss` for lines starting with `#` that are not known
  ISPP directives, **before step 1** - so the same mistake costs seconds and
  names the line, instead of a stage and a bootstrap and an error message that
  does not say what is wrong. Checked in both directions: 0 findings on the
  fixed file, and all 10 reported when the wrap is reintroduced everywhere the
  idiom appears.
- `cycle.ps1`'s `Fail` now reports when it is leaving the SD service stopped,
  and says that both trees are untouched until step 6. It deliberately does
  **not** restart it: a re-run stops it again immediately, and starting a
  server against a half-staged tree is worse than leaving it down. The point
  is only that it should never be a surprise.

**THE FIX IS VERIFIED AS FAR AS IT CAN BE WITHOUT ELEVATION.** `ISCC` was run
standalone against the staged tree left by the failed cycle, writing to a
scratch directory: *Successful compile*, exit 0. That also compiled §8's
`SecureAccountDirs` Pascal for the first time, which had never been through
ISCC either. It does not cover uninstall, delete or install - steps 5 to 7,
which only a real cycle exercises.

**Still open:** the cycle itself, and everything downstream of it.

---

## 19 Aug 2026 - SCRAM phase 3: the server exchange, written and not compiled

**Commit:** this one. Phase 3 of [docs/SCRAM_AUTH.md](docs/SCRAM_AUTH.md).
**The install was already STALE when this started and still is.** Nothing here
has been compiled or run against a server.

**What went in.** `APISRVR` gains `vb.scram.first` (request 47) and
`vb.scram.final` (48), shared exits `scram.bad.message` / `scram.crypto.failed`
/ `scram.bad.cred` / `exit.vb.scram.fail`, and `scram.trim.body`. Messages
`5272` "Invalid authentication message", `5273` "Authentication sequence
error", `5274` "Authentication service unavailable"; every credential failure
answers the existing `5017` and sleeps 3, as `vb.login` does. `vb.login` is
untouched and still serves request 24.

**The two questions the previous handoff left open, answered from the code.**
Per-session state is ordinary program variables — `APISRVR` is one process per
connection running one `loop`, so nothing survives between connections and
nothing needs a session key. They are initialised before the loop, not in the
`kernel(K$CPROC.LEVEL,0)` first-time block, so `scram.stage` is never merely
unassigned. The "already logged in" guard sits on **both** handlers: the main
loop's gate only *admits* 24/25/47/48 to an unauthenticated session and does
not block them afterwards.

**`deffun valid_os_name` moved to the top of `APISRVR`.** It was inside
`vb.login`, which phase 5 deletes; that would have taken the declaration with
it and left `vb.scram.first` calling an undeclared function. Placed **below**
the `common /$APISRVR/` block rather than above it, because CPROC is the only
program here showing the two together and it declares after `syscom.h`'s
common — the order known to compile.

**`ON ... GOSUB` clamps rather than falls through, which is why adding two
entries was safe.** `computed_jump()` in `gplsrc/op_jumps.c` with
`pick_style = FALSE` forces an out-of-range index to the last label, and the
last label is `vb.illegal.action`. Checked rather than assumed, because the
opposite would have made every action above 48 a silent success.

**`bbcmp.py` does not support DEFFUN and it does not matter.**
`gplbld/bootstrap.py:54` sends only `BBPROC`, `BCOMP`, `PATHTKN` through it;
`APISRVR` is compiled by the real `BCOMP` and already had a `deffun`.

**`gplbld/verify-scramlogin.ps1` is new and speaks the protocol directly**,
because `sdclilib.c` does not speak SCRAM until phase 4, so a test through the
client library would test nothing. It builds packets from
`[4 byte length][2 byte type][payload]` and waits for the `0x06` ACK, as
`OpenSocket()` does.

**Its client half is proven; that is the only thing verified here.**
`-SelfTest` is unelevated, needs no server and no install, and drives the
script's own `New-ScramProof` — the same function the live checks use, not a
copy — against the RFC 7677 §3 vectors. **5/5**: SaltedPassword, StoredKey,
ServerKey, ClientProof, ServerSignature. So a later disagreement with SD is
SD's.

**The suite is built around the refusals and two controls**, since a login path
that says "yes" proves little: wrong password, a replayed client-final from the
exchange that succeeded, a tampered nonce, 48 with no 47, unknown account,
`y,,` downgrade, `m=` extension. The controls are that two exchanges for one
account get different server nonces, and that the same byte search which finds
no password in the SCRAM traffic **does** find it in a request-24 login — a
search that can never find anything passes just as well.

**User enumeration was introduced deliberately and is recorded, not hidden.**
An account with no usable credential fails at 47, a wrong password at 48; same
message, different round trip. RFC 5802's dummy-salt answer needs a secret
`APISRVR` can read and cannot write, which means seeding it in `CRED_SET` and
re-opening verified phase 2 work. Deferred because it changes no stored
credential and no wire format. `SCRAM_AUTH.md` "Still open" has the design.

**Still open:** the whole of it, until a cycle. `make sd` is owed as well —
four `gplsrc` files are newer than `bin\sdclilib.dll`.

---

## 19 Aug 2026 - Account ACLs: the blocker was a wrong premise; code written, nothing verified

**Commit:** this one. **Session ended mid-task**, out of credits. **The install
is STALE** and nothing below has been compiled or run.

**THE BLOCKER WAS WRONG, AND MEASUREMENT IS WHAT SHOWED IT.** For four sessions
PROJECT_STATUS said the per-account ACLs were blocked because locking a
directory "still gates administrators out of other accounts, which §5.6 says
must always work". **§5.6 says no such thing**: its table grants the
group-check bypass to an ELEVATED session, not an ordinary one. And on the
16:54:55 install, with a second account made for the purpose, an unelevated
`don` was already refused by SD - `LOGTO SDACL1` answered "User not allowed in
requested account" - while the FILE system let the same session list that
account's directory and write into it. `CPROC`'s `logto.authorised` has admitted
only elevation, freshly obtained privilege, or `ACC$GROUP` membership since
14 Aug 2026. **The concern predates that restoration and was never re-checked.**

**So this work aligns the file layer with a rule SD already enforces.** That is
the whole reason it is safe to do, and it is why the "decision" dissolved
instead of being made.

**WRITTEN, WITH WHAT WAS ACTUALLY DONE TO EACH:**

* `gplbld/secure-account-dirs.ps1` - NEW, the re-apply half. **Run by hand and
  it works**: stamping `user_accounts/sdacl1` took don's access from "6 entries
  and writing ALLOWED" to DENIED, propagated to `voc` beneath it, and left
  don's OWN account still listing 7 entries as the control.
* `CREATEA` gained `secure.account.dir`, stamping a new account from its
  `ACC$GROUP` through `!ps_script`. **Never compiled.**
* `sd.iss` gained `SecureAccountDirs` - container first, then re-apply, after
  `AdoptAccount` - and its message joins the closing dialog. **Never through
  ISCC.**
* `stage.py` ships both scripts. `sdsys/messages/10055` is new.
* **No verifier exists.** `CREATEA`'s comment promises
  `gplbld/verify-accountacl.ps1`; write it or change the comment.

**LEFT ON THE MACHINE: `sdacl1`** - Windows user, group `sdu_sdacl1`, register
record, and a directory whose ACL was replaced by hand. A cycle removes the
directory but NOT the user or the group. `don`'s own account was deliberately
left untouched.

**THE RULE IS DELIBERATELY IN TWO PLACES.** `CREATEA` builds the icacls inline;
the script has the same rule. They cannot share a file - the script installs to
`{app}` and SD exposes no `system()` key for the program directory. **The guard
is meant to be a measurement**: a verifier asserting a `CREATE.ACCOUNT`
directory and a script-stamped one come out identical.

**FIRST THING TO CHECK AFTER THE CYCLE: that CREATE.ACCOUNT still works.**
`secure.account.dir` runs inside it and `!ps_script` needs the session to hold
privilege. If account creation breaks, that is where to look.

---

## 19 Aug 2026 — An install spent on the intermittent check: three explanations dead

**Commit:** this one, over `8825928`. **Install:** **16:54:55**. Owner
authorised the cycle for this and nothing else; no source changed.

**The question:** `verify-lcnames.ps1` had failed once after the 15:30:36
install and four times after the 16:38:01 one, passing on an immediate re-run
both times. It had been written up as "the first run after a cycle".

**The measurement:** a cycle, then the verifier driven **UNPIPED** immediately
afterwards - before anything else touched SD - and then five more times.

```
run 1 (straight after the install)   142 / 142
runs 2 - 6                           142 / 142
```

**It did not reproduce, and that is worth more than it sounds.** Three
explanations are now dead:

1. **"The first run after a cycle is different."** This cycle's first run was
   clean, so whatever it is, it is intermittent rather than tied to the install
   boundary. The name it was filed under was wrong.
2. **"The first `sd` creates the shared segment."** `C:\ProgramData\SD\shm`
   already held `sd_shm_716d0301` **before any of these runs**, because the
   installer's ADOPT step runs SD. This was the lead the release-string
   correction opened, and it is closed.
3. **The `$RELEASE` prompt and the revision cross-check**, ruled out earlier and
   restated: both sides of each are the display string `W1.0-0` and they match,
   `op_sys.c:378` returning `SD_REV_STAMP` for `system(1012)`.

**What is left: an intermittent failure of roughly 2 runs in 10, cause
unknown.** Kept in the file rather than closed, because of what it costs if
ignored - the discipline here is "cycle, then measure", and a check that fails
without meaning it teaches whoever meets it to re-run until green, which is how
a real failure gets waved through. **If it recurs, capture the run UNPIPED**:
both original sightings were lost because the run went through `Select-String`,
so `Start-Transcript` recorded the command and not the answers.

---

## 19 Aug 2026 — Correction: W1.0-0 is a display string, not the release

**Commit:** this one, over `f988f48`. Documents only. Owner's correction.

The entry below ruled out the `$RELEASE` prompt as the cause of the first-run
verifier failures on the grounds that "both read `W1.0-0`". **That reasoning was
shallow.** `W1.0-0` is the DISPLAY string - the 18 Aug entry in this file says
so in its title - and the release identity is `MAJOR_REV`/`MINOR_REV`/`BUILD` =
**1/0/2**, the openQM **2.6-6** lineage, which `MESSAGES/0000` still carries.

**The ruling-out itself still holds**, and is now stated for what it is: both
sides of `LOGIN:444` are the display string and they match, and `LOGIN`'s second
check, `compare(system(1012), SD.REV.STAMP)`, compares that string with itself
(`op_sys.c:378` returns `SD_REV_STAMP`). What was wrong was implying that
agreement between display strings settled the release question.

**AND THE CORRECTION POINTS AT THE LEAD.** `sysseg.c:58` builds
`SYSSEG_REVSTAMP` from `MAJOR_REV`/`MINOR_REV`/`BUILD`, and `sysseg.h:69`
already records in terms that **it does not catch a shared-segment layout
change**, precisely because the release identity does not move when the port
does. A cycle deletes both trees, so the first `sd` after one creates the
segment while later runs attach to it - an install boundary that behaves
differently on the first pass, which is the shape of what is being seen.
**Not measured. It is a lead, not a finding.**

---

## 19 Aug 2026 — OS.EXECUTE is gated: the C half of step 7 is closed

**Commit:** this one, over `69015c3`. **Install:** **16:38:01**, `sd.exe`
`4042F21834AFDD75`. `verify-osusers.ps1` **24/24**.

**The hole, measured with its control before the change** - one unelevated
session standing in DON, unlisted in OS.USERS:

```
SH echo ...               ->  "don is not permitted to use the operating system shell"
os.execute ... capturing  ->  output captured, and the plain form ran too
```

Same user, same session: the visible route refused and the real one open. Any
account that could write a program had the operating system. After the change:
*"don is not permitted to use OS.EXECUTE at line 2 of ..."*.

**The gate is in C, in `sh()`** (`op_sh.c`, `os_permitted()`), because
OS.EXECUTE is its own BASIC statement - `BCOMP:9643` -> `OP.SH`/`OP.SHCAP` ->
`sh()` - and CPROC's `os.command:` gate is not on that path and cannot be.

**Three ways in, and the first is what keeps SH working.** `HDR_INTERNAL`: the
SH verb reaches the OS by CPROC itself doing `os.execute`, so in C the verb and
the statement are the same code and cannot be told apart. CPROC is `$internal`
and has already applied the finer rule, so trusting the marker leaves SH
unchanged - and it cannot be forged, because `BCOMP:2864` honours `$INTERNAL`
only for a session that is itself internal AND elevated. Then an elevated
session, and OS.USERS field 2.

**Nothing system-side changes, and it was checked rather than assumed:** all 13
programs in the shipped tree that call `os.execute` are `$internal`.

**THE TRUTH TABLE IS WHAT MAKES IT EVIDENCE.** A gate that refused everything,
or that read field 1 by mistake, could not produce this:

```
unlisted            SH refused    OS.EXECUTE refused
SH=yes OS.EX=no     SH RUNS       OS.EXECUTE refused
SH=no  OS.EX=yes    SH refused    OS.EXECUTE RUNS
elevated            SH runs       OS.EXECUTE RUNS
```

The middle two rows are one record each, read in one session, and they are the
whole proof that the two fields are independent. `verify-osusers.ps1` gained a
third elevated phase to write the second of them.

**A trap this file already documents caught me anyway.** The first version of
the OS.EXECUTE helper both printed and returned, so PowerShell handed the caller
an array with the printed lines in front of the answer, and two checks compared
'refused' against `System.Object[]` and failed **on a gate that was working**.
`Invoke-ElevatedPhase` in that same script carries a comment about exactly this.
It now reports through a script-scope variable.

**Still open, and it is next step 3: the first verifier run after a cycle fails
checks the second passes.** 138/142 then 142/142 with nothing changed between.
The `$RELEASE` prompt was the obvious suspect and is ruled out - `LOGIN:444`
fires only on a stamp mismatch, and both read `W1.0-0`. Not understood, and it
undermines "cycle, then measure" until it is.

---

## 19 Aug 2026 — $COMMAND.STACK moves, and section 3 gets a control it owns

**Commit:** this one, over `0394af4`. **Install:** **15:30:36**.
`verify-lcnames.ps1` **142/142**.

`$COMMAND.STACK` was the last upper-case VOC id and the only one left after the
ten file pointers. **It is X-type, not an F/Q pointer**, and it needed different
work: `CPROC` and `LOGIN` reach it by **RECORD read**, and a record read matches
the id exactly - `_VOC_REF` folds a FILE name, never a record id - so both
spellings are tried by hand. `CREATEA` writes the lower-case one.

**`CPROC` keeps whichever spelling matched in `cs.id`**, because the `release`
has to name the record the `readu` locked. Releasing the other spelling would
leave the lock held for the life of the session - a quiet, permanent fault, and
the reason that line is not simply the literal it used to be.

**THE INSTRUMENT IS THE `stacks` FILE, NOT THE VOC.** `CPROC` writes it only
when it found the record AND the record is X-type, so the file appearing is the
read having succeeded. Section 5b measures both readings: the shipped
lower-case id, and the id toggled back to `$COMMAND.STACK` to stand for an
account created before the rename. **Both save the stack**, which is exactly
what the changelog promises and is the half that would otherwise be assumed.

**SECTION 3'S CONTROL IS NO LONGER A SHIPPED ID.** `$HOLD` held that job until
18 Aug, `BP` until 19 Aug, `$COMMAND.STACK` until later the same day - each
rename ate the control before it, which is a pattern rather than bad luck. It is
now a record the test writes itself in upper case and reads back in upper case,
and no future rename can consume it. Without a control every assertion in that
section would pass equally well on a VOC that had been lower-cased by accident.

**One check failed once and has not since, and the cause was not established.**
§6's "CT VOC COPYP shows a bare V type code" failed on the first run against
this install and passed on the next three; the record is correct by hand. A
mechanism with that exact shape exists and is worth knowing about:
`LOGIN:444` compares the VOC's `$RELEASE` against `SD.REV.STAMP` and prompts in
a loop that only Y or N escapes, so **a piped session answers it with its next
command** - one stray prompt swallows a verb and the dependent check reports a
bare False. It would hit any piped verifier here. Recorded in the header rather
than closed.

**Suite on the same install:** `verify-keys` 10/10, `verify-editkeys` 14/14,
credacl/nocase/osusers exit 0, `make check-local` PASS,
`post-cycle-elevated -TierPrefix sdtierm -Account sdacct20` all exit 0.
Next free names `sdacct21`, `sdtiern`.

---

## 19 Aug 2026 — The ten F/Q file-pointer VOC ids are lower case

**Commit:** this one, over `0d85619`. **Install:** **15:16:15**.
`verify-lcnames.ps1` **135/135**, and the whole suite with it.

`VOC NEWVOC ACCOUNTS MESSAGES SYSCOM QFILE DICT.DICT MD SD.ACCOUNTS OS.USERS`
became `voc newvoc accounts messages syscom qfile dict.dict md sd.accounts
os.users` in both `newvoc` and `voc_template`, plus the two Q-pointer field 3s
(`md` -> `voc`, `sd.accounts` -> `accounts`), 24 literals across 21 BASIC
programs, `third.compile`'s three `CD` targets, and message 2022.

**Three literals deliberately stay upper case, and each would be a defect to
"fix".** `DELETEF:48`'s `banned.files` is compared with
`locate upcase(file.name) in banned.files` - only the LEFT side is upcased, so
lowering the list lets `DELETE.FILE voc` past the guard and delete the account's
VOC. `SETFILE:130`/`:150` keep `'QFILE'`: the code already tries the exact id
then `downcase()`, covering a pre-rename account and a renamed one at once, and
lowering the default would break the older half. Annotated in place.

**Three `"VOC"` literals are the `@VOC` system variable**, not the file -
`BCOMP:294`, `ICOMP:201`, `bbcmp.py:1814`, in the `@`-variable name table
between `USER4` and `WHO`.

**One comparison did have to move**: `LOGIN:647` `if id = 'MD'` - `id` comes
from a READNEXT over the update VOC, whose record is now `md`, so every account
being updated would have been asked about a type change it should never see.
`upcase(id)` now.

**THE FIRST VERIFIER RUN FAILED FOUR CHECKS AND THE TEST WAS WRONG, NOT THE
RENAME.** An account's VOC is built from `newvoc`; `voc_template` becomes
SDSYS's own. `ACCOUNTS`, `MESSAGES`, `QFILE` and `OS.USERS` are in
`voc_template` **only**, so in DON's account "Record not found" is the correct
answer. All four were correct in SDSYS all along. The verifier now asks each id
where it lives and asserts the absence as well.

**`$COMMAND.STACK` DID NOT MOVE, and it is not an F/Q pointer.** X-type
(`CREATEA:752` writes `'X'`), grouped with the pointers only because it was the
last upper-case id. Its readers - `CPROC:3611`, `:3623`, `LOGIN:489` - do exact
RECORD reads with no fold, on the login and prompt paths, and moving it takes
`verify-lcnames` §3's last control with it. Its own step, and next.

**Suite on the 15:16:15 install:** `verify-lcnames` 135/135, `verify-keys`
10/10, `verify-editkeys` 14/14, credacl/nocase/osusers exit 0,
`make check-local` PASS, `post-cycle-elevated -TierPrefix sdtierl -Account
sdacct19` all exit 0 with `verify-tiers` 22/22 still at 393/411/421 - the tiers
and `CREATE.ACCOUNT` are unaffected by the renamed `newvoc`. Next free names
`sdacct20`, `sdtierm`.

**`cycle.ps1 -SkipInstall` earned its keep**: the bootstrap compiled all of it
clean before an install was spent, which is what PROJECT_STATUS 5.12 recommends
for a BASIC change of this size.

---

## 19 Aug 2026 — The editor keys measured: 14/14, and the whole suite with them

**Commit:** this one, over `1f92080`. **Install:** **14:54:36**, `sd.exe`
`FA5B47C0F6CF32D6`. The cycle the entry below said was owed was run by the
owner; everything in it is now measured.

**`gplbld\verify-editkeys.ps1` — 14 of 14.** Before and after, same
instrument:

```
SED     AB DEL C            ABC  ->  AC
UPDREC  field AB, X DEL     XB   ->  AB
UPDREC  field AB, RIGHT X   CXAB ->  AXB
```

**The controls are what make it evidence.** With no erase byte the same runs give
`ABC` and `XAB`, so the erase is what changed them; and the Delete key still
deletes FORWARDS in both editors, so the two keys were fixed rather than
swapped. That last check is taken with the cursor NOT at the end of the line —
at the end, deleting forwards does nothing and the check would pass on a Delete
key that had stopped working altogether.

**The rest of the suite on the same install:** `verify-keys` 10/10,
`verify-lcnames` 121/121, `verify-credacl`/`-nocase`/`-osusers` exit 0,
`make check-local` PASS, and `post-cycle-elevated.ps1 -TierPrefix sdtierk
-Account sdacct18` all exit 0 with `verify-fold` 10/10 and `verify-tiers` 22/22
at 393/411/421. Register back to `DON` and `SDSYS`, `bp` and `bp.out` empty.

**THE FIRST RUN FAILED 7 OF 14 AND THE FIX WAS MINE, NOT SD's.** The seed helper
was written as a single line — `open 'F' to f then write .. ; print 'OK' end
else print 'FAIL'` — which **compiles clean, reports `0 error(s)`, and then
stops at run time with "Unassigned variable END"**: the inline `THEN` takes
statements to the end of the line, so `END` is read as a variable. The block
form works. Worth keeping because SED's seven checks passed in that same run, so
the failure looked at first like a fix that had only half worked.

---

## 19 Aug 2026 — Backspace in the full-screen editors, and the test that was "the work"

**Commit:** this one, over `679f47c`. **A CYCLE IS OWED** — `SED` and `UPDREC`
are BASIC, only a bootstrap compiles them, and elevation was declined twice at
the end of the session. Nothing below is measured on the new build.

**Owner: "fix backspace in ED and UPDATE.RECORD".**

**ED was never affected and §5.17 was wrong to list it.** It is the LINE editor
and reads with `input`, so the `_KEYCODE` fix of 19 Aug already covers it.
Measured: DEL erases backwards in ED today. `ED:3436` passes *"Not full screen
editor"* and there is no path from `ED` to `SED`.

**The two that were affected, measured on the 10:06:08 install before changing
anything:**

```
SED    type AB, DEL, C          -> ABC   deleted forwards   (Ctrl-H gave AC)
UPDREC field AB, type X, DEL    -> XB    deleted forwards   (Ctrl-H gave AB)
```

**And UPDREC was worse than a dead key: its arrows typed themselves into the
record.** Its only cursor bindings were `char(203)`-`char(212)`, an 8-bit
terminal convention nothing on this platform emits, and no escape sequence was
bound at all. `get.key` walks the multi-character table, fails, and the bytes
fall through as text. **Measured: field `AB`, press Right, type `X`, save ->
`CXAB`.** Silent data corruption in a data-entry screen, which is why the arrows
were fixed here too and not left for later.

**`SED`'s arrows were already right** and are the worked example `UPDREC` copies:
`SED:4489` binds Ctrl-B, `ESC [ D`, `ESC O D` and `char(203)` to `F.LEFT`. All
three measured working. Only its erase keys were wrong.

**THE INSTRUMENT IS THE SAVED RECORD, AND THAT IS THE REUSABLE PART.** §5.17 said
this needed "a test that drives a full-screen editor, and nothing here does that
yet", and assumed a console. It does not need one: `SED` and `UPDREC` read the
keyboard with `keyin()`, which reads **standard input**, so a full-screen editor
is drivable from a pipe exactly as the command-line editor is. Type, save, quit,
read the record back with `CT`. The screen is never inspected.
`gplbld\verify-editkeys.ps1` is that test, 14 checks.

**WHAT IT COST: AN HOUR TO A RECORD LOCK THAT OUTLIVES ITS PROCESS.** A bounded
run that times out kills SD mid-edit; `LIST.READU` then shows an `RU` lock owned
by a dead user; `UNLOCK USER n` and `UNLOCK FILE ...` will not take it from an
ordinary account session; and every later run on that record id stops on *"Wait
for lock to be released? Y or N only"*. One timeout poisons the id for the life
of the install. **The verifier now uses a fresh random record id per case** and
reports stale locks rather than failing on them. They clear with `sd -CLEANUP`,
which removes only users whose process is gone (`clopts.c:242`), or at the next
cycle, which rebuilds the shared memory segment.

**Correction, and it corrects something written earlier the same day.** This file
said an agent shell CANNOT raise a UAC prompt; the twenty-seventh session
overturned that after four successes. Both are too strong. The same mechanism
then failed **twice** at the end of this session, returning *"The operation was
canceled by the user"* **with no way for the caller to tell a declined prompt
from one that never appeared**. It tracks whether someone is at the keyboard.
**Try it; never build a step that depends on it.**

---

## 19 Aug 2026 — All three console hosts read; the keyboard subject is closed

**Commit:** this one, over `1f466f4`. Documents only.

**Windows Terminal read, and it is byte for byte identical to cmd and
PowerShell.** All three send `ESC [ D/C/A/B` for the arrows, `127` for
Backspace and `ESC [ 3 ~` for Delete — exactly what the `windows` terminfo
entry binds. **§5.18 now rests on measurement at both ends of the chain**, with
no inferred link: SD never sends `smkx` (read from source), and no console ever
sends the application-mode spelling (read from three consoles).

**Both fixes from the previous two entries confirmed live.** The probe stayed
installed, so the run worked where the deletion had broken it; and the same
17-byte reading that hit the pager in PowerShell now completes with no pager at
all, which is `@(0,0)`.

**The keyboard subject that opened this session is finished** apart from next
step 2, backspace inside `ED` and the `UPDATE.RECORD` screens, which is a
separate mechanism — those carry their own key tables and neither the `_KEYCODE`
binds nor the terminal type reaches them.

---

## 19 Aug 2026 — Correction: probe-keys.ps1 deleted the command it had just taught

**Commit:** this one, over `f17380d`. `gplbld\probe-keys.ps1` only.

**Owner: "tried it in terminal and it said zzkeyprobe did not exist."** Reported
after successful cmd and PowerShell readings, and the session was unelevated.

**The cause is the script's own design, not SD.** It removed `ZZKEYPROBE` when
the operator left SD. The probe is meant to be run once per console host, so
the first run teaches `RUN BP ZZKEYPROBE` and the operator naturally types it in
the next window — where the previous run had already deleted it. **A probe that
deletes the command it just taught you is a trap of its own making.**

**Elevation was checked first and is not the cause** — measured, an elevated
`sd` session lands in `DON`, not `SDSYS`, so the account would have been the
same either way. Worth recording because §5.6's "administrator rights on entry
to SDSYS" makes the opposite sound plausible.

**Fixed three ways.** The program is now **left installed** and `-Keep` is
replaced by `-Cleanup`, which is a mode that removes and stops. After the
compile the script checks the **object** exists in `bp.out` rather than trusting
`0 error(s)` — RUN needs the object, and the first sign of trouble was otherwise
SD refusing at a prompt with the script already gone. And it prints the account
and paths it is using.

**`-Cleanup` is exempt from both guards**, the console test and
`assert-current`. Removing a file needs neither, and a guard that blocks the
undo is one that gets worked around.

**Measured:** `-Cleanup` with nothing installed exits 0 and says so; with the
probe installed it removes source and object and exits 0; a measuring run piped
into still exits 2.

---

## 19 Aug 2026 — The console reading: every key matches, and §5.18 is closed

**Commit:** this one, over `7de04ee`. Documents only.

**Owner ran `gplbld\probe-keys.ps1` in a cmd console.** Every key sends what
the `windows` terminfo entry binds:

```
Left       27 91 68      ESC [ D     kcub1=\E[D
Right      27 91 67      ESC [ C     kcuf1=\E[C
Up         27 91 65      ESC [ A     kcuu1=\E[A
Down       27 91 66      ESC [ B     kcud1=\E[B
Backspace  127           DEL         kbs=\177
Delete     27 91 51 126  ESC [ 3 ~   kdch1=\E[3~
```

**Not one `ESC O` in it.** §5.18 argued from the protocol that the application
cursor mode spelling could never arrive, because nothing in SD sends `smkx`.
That was the last inferred link in the chain and it is now a direct reading.
Backspace and Delete are distinct bytes, so the two keys do not collide.

**cmd and PowerShell were both read and are byte for byte identical.** Windows
Terminal was not; acceptable rather than a gap, since all three reach SD through
the same `msys-2.0.dll` console layer and the 19 Aug backspace work already
measured DEL from all three.

**The PowerShell run also exposed a flaw in the probe itself**: SD's pagination
fired after 17 bytes. Harmless there — it came after the reading — but a longer
session would hit "Press RETURN to continue" mid-listing, and the key pressed to
dismiss it is itself a keystroke, so the instrument would interfere with its own
measurement. Fixed with `@(0,0)`: a cursor POSITIONING call disables pagination
where a special function like `@(-1)` does not. 40 arrow presses now list 120
bytes uninterrupted on an 80x24 terminal.

**Correction to this file's own housekeeping: PROJECT_STATUS.md had TWO
"WHAT TO DO NEXT" lists.** Replacing the header on the twenty-seventh session
left the twenty-sixth's list in place further down, and its item 1 was
"finish the post-cycle run on the 09:10:45 install" — work completed that same
morning. A cold reader following the second list would have redone finished
work against a superseded install. **The two are now one index in the header
and one detail block below it, with matching numbers**, and the header says so.
Worth watching for whenever a header is replaced wholesale rather than edited.

---

## 19 Aug 2026 — probe-keys.ps1: the first instrument here that is not a pipe

**Commit:** this one, over `a71d124`. No source change under `gplsrc` or
`sdsys`, so the 10:06:08 install stays current.

`gplbld\probe-keys.ps1` compiles `ZZKEYPROBE` into the caller's own `bp`,
starts a plain `sd` in the current console, and prints every byte each key
sends — naming an arrow's spelling, `ESC [ D` or `ESC O D`, as it goes. The
program is left installed; `-Cleanup` removes it. **It removed the program on
exit at first, and that was wrong — see the correction below.**

**Why it is worth a script rather than a paste of BASIC.** Every other
instrument in `gplbld` drives SD down a pipe, which measures what SD does with
a byte and never what the console produces from a key press. That gap let
`verify-keys` pass 6/6 on backspace on the same install where backspace was
being reported dead. **It refuses if stdin is redirected**, so it cannot quietly
become another pipe measurement.

**Registered in `assert-current.ps1`'s `$neverShipped`** — a new file under
`gplbld` that is not in that list makes every install look stale.

**`sd <command>` is elevation-gated** (`sd.c:734`, 15 Aug), so the script cannot
run the program itself; the operator types `RUN BP ZZKEYPROBE`. Elevating to
avoid that would change the session under test.

**Verified before handing it over:** the BASIC compiles (0 errors), the decoder
was fed `ESC [ D`, `ESC O C`, DEL and Ctrl-H down a pipe and named all four
correctly, and the redirect guard exits 2. The console reading itself is the
owner's to take — that is the whole point of it.

---

## 19 Aug 2026 — Clear screen was never broken (closes part of the entry below)

**Commit:** this one, over `17fcae2`. No code change.

**Owner, at a real console: "cs works correctly".** The entry below left clear
screen open because nothing in `gplbld` can watch a screen. It agrees with what
was already measured — `@(-1)` emits `ESC [ H ESC [ J`, `@(5,3)` emits
`ESC [ 4 ; 6 H`, and `clear` is identical in `vt100`, `linux` and `windows`, so
the terminal-type change could not have affected it either way. Read it as
collateral in the original four-item report, not a fifth fault.

**Still owed from that report: a person confirming the arrows** in cmd,
PowerShell and Windows Terminal. `verify-keys` 10/10 proves the bindings
resolve; it cannot prove a key press arrives, because it drives SD down a pipe.

---

## 19 Aug 2026 — The arrow keys: the default terminal type was the cause

**Commit:** this one, over `3d05dad`. **Install:** **10:06:08**, `sd.exe`
`FA5B47C0F6CF32D6`, terminfo 100.

**Finished the post-cycle run owed on the 09:10:45 install** — `verify-credacl`,
`-nocase`, `-osusers`, `make check-local`, and `post-cycle-elevated.ps1`
(`-TierPrefix sdtieri -Account sdacct16`) all passed. Then took a fresh cycle for
the work below and ran the whole suite again on it: `verify-lcnames` 121/121,
`verify-keys` 10/10, `verify-fold` 10/10, `verify-tiers` 22/22 at 393/411/421.

**Correction: an agent shell CAN raise a UAC prompt.** PROJECT_STATUS had it as
a working constraint, and `post-cycle-elevated.ps1` exists because of it.
`Start-Process -Verb RunAs -Wait` prompted and succeeded four separate times
this session, including for `cycle.ps1`. The true constraint is narrower — no
interactive desktop, e.g. over ssh.

**The owner reported left arrow, right arrow, backspace and clear screen dead in
cmd, PowerShell and Windows Terminal.** Cause: the `login` paragraph's
`TERM VT100`, changed from `TERM LINUX` on 18 Aug on the reasoning that "on
Windows the sensible default is VT100". Backwards. `vt100` binds the arrows to
`ESC O A/B/C/D`, which a terminal sends **only in application cursor mode**, and
`smkx` — the string that enters that mode — **occurs nowhere in the tree except
the capability-name table** at `gplsrc/ti_names.h:179`. So the arrows had never
worked under that default. `kbs` was the same one key over, which is what §5.17
patched in `_KEYCODE` on 19 Aug without reaching the cause.

**Fixed by the owner's ruling**: `terminfo.src` gains `windows`, a byte-exact
copy of `linux`; the `login` paragraph in `voc_template` and `newvoc` selects it;
`LOGIN:116`'s fallback matches. **The cull was discussed and not done** — all 62
definitions still ship. `verify-keys.ps1` grew 6 → 10 checks with an arrow
section that tells "both arrows worked", "only LEFT worked" and "neither worked"
apart in one run.

**Measured along the way, and worth keeping:** `system(7)` already answers
`vt100` before `LOGIN` can look, so `LOGIN:115`'s `env('TERM')` branch is dead —
**neither `$TERM` nor `sd -TERM <type>` changes the terminal type**, only typing
`TERM x`. And `sd.exe` links `msys-2.0.dll`, so the terminal layer is Cygwin's
console handler.

**Clear screen is still open and is not an SD defect so far.** `@(-1)` emits
`ESC [ H ESC [ J` and `@(5,3)` emits `ESC [ 4 ; 6 H`, both correct. **A pipe is
not a console and every instrument in `gplbld` is a pipe** — the same gap that
let `verify-keys` pass 6/6 on backspace while the owner was reporting it broken.

**What it cost: one build, to an `sdtic` defect — `UPSTREAM_FIXES.md` #9.**
`reset_buffers()` sat inside the "this entry compiled" guard, so a failed entry
left `strings[]` and `str_count` to accumulate into the next one. The 62-entry
database with one bad entry **segfaulted at 24 files of 100** and printed none
of its diagnostics, because stdout was block buffered to a file. `sdtic` also
returned 0 whatever happened, so `make terminfo` reported success. Both fixed.
It was found by giving the new entry the description
`Windows console (cmd, PowerShell, Windows Terminal)` — `get_token()` splits on
commas, so the words after the first one were read as capability names.

**Also: `make sdtic` is not a supported target.** It leaves `C_FLAGS` empty, so
gcc defaults to gnu23 where `bool` is a keyword and `sdtic.c:148`'s
`typedef int16_t bool` will not compile. Use `make sd`.

---

## 19 Aug 2026 — Both fixes measured on the 09:10:45 install; the left arrow is open

**Commit:** this one, over `1943704`. **Install:** **09:10:45**, `sd.exe`
`339AB7157F002679`, `assert-current` exit 0.

**`verify-keys.ps1` 6/6** and **`verify-lcnames.ps1` 121/121**, so both changes
in `1943704` are now measured rather than merely written.

**Section 9 is the answer for `bp.OUT`:** `BASIC bp ZZRLC1` produced
`LOWER=YES MIXED=NO UPPER=NO` on exact-match VOC reads — the id created is
`bp.out`, not the unreachable mixed-case `bp.OUT` — and `BASIC BP ZZULC1`
afterwards answered `UPPERCOMPILE=OK` with no "already exists". That second one
is the regression proper: the failure was never in the compile that made the
file but in the next one, typed the other way.

**Backspace has a before and after.** On 07:41:45, piping `COUNTX<DEL> VOC` ran
`COUNTX VOC` — not erased. On 09:10:45 it runs `COUNT VOC`, `^H` still erases,
and the no-erase control is still refused.

**A false alarm in `Remove-Probes`, and it is instructive.** It printed
"WARNING: bp.OUT is still there - a later BASIC BP <x> will fail" on a
perfectly good install. Two things were wrong. The warning TEXT described the
failure the fix had just removed. And the removal itself used the old mixed-case
spelling: measured directly, `DELETE.FILE bp.OUT FORCE` removed nothing while
`DELETE.FILE bp.out FORCE` answered "DATA portion 'BP.OUT' deleted / VOC entry
'bp.out' deleted". **Why the mixed spelling is not folded to the lower one is
not established** and is recorded as an open question rather than guessed at.

**THE LEFT ARROW IS OPEN, AND THE `_KEYCODE` CHANGE IS EXONERATED BY
MEASUREMENT.** The owner reported it immediately after the backspace fix. Driven
from a pipe on the fixed install, `ESC O D` (vt100's `kcub1`) still resolves to
`K$LEFT` and moves the cursor, while `ESC [ D` is discarded — so the binding is
intact and the only added binding, `char(127)`, cannot affect a three-byte
escape sequence. What is NOT established is what the Windows console emits for
Left, or whether SD ever sends `smkx` to put it in application cursor key mode;
`vt100` and `xterm` both use `kcub1=\EOD` with `smkx=\E[?1h\E=`, so the
terminal type is not the lever. §8 has the measurements and the next step.

**Left unfinished by the session, not by the work:** `verify-credacl`,
`-nocase`, `-osusers`, `make check-local` and `post-cycle-elevated.ps1` were not
reached. Next free names are `sdacct16` and `sdtieri`.

---

## 19 Aug 2026 — The backspace key did nothing in any Windows console

**Commit:** this one. **Install:** NOT CYCLED — it rides the same owed cycle as
the `bp.OUT` entry below. Baseline measured on the 07:41:45 install *before* the
fix, which is what makes it evidence: piping `COUNTX<DEL> VOC` ran `COUNTX VOC`
and answered "not in your VOC"; the same with Ctrl-H ran `COUNT VOC` and counted
422; and the no-erase control was refused.

Reported by the owner: backspace dead in cmd, PowerShell and Windows Terminal,
and in PuTTY unless its "Backspace key" setting was changed to Control-H.

**A terminal sends one of two bytes for backspace — Ctrl-H (8) or DEL (127) —
and nothing says which.** `_KEYCODE` built its table from terminfo, so SD
accepted whichever byte `kbs` named and let the other fall through as a literal;
`CPROC:835`/`972` have a `case` for `K$BACKSPACE` and none for 127. Every
Windows console host sends **DEL**, and `LOGIN:116` defaults an unset `TERM` to
`vt100`, whose `kbs` is `^H`. The two never met.

**No choice of terminal type could have fixed it, and that is the reusable
part.** Of the 62 entries in `terminfo.src`, 51 say `^H`, one says `^Y`, eight
have no `kbs`, and **only `xterm` and `linux` say DEL**. The owner had tried
`vt100-w` because it reads like a Windows variant — it is the **wide**
132-column variant, `cols#132` and a different `rs2`, with every key capability
identical to `vt100`. `vt100-at` (AccuTerm, an actual Windows emulator) is
`kbs=^H` as well.

**A first grep said only two entries had an unusual `kbs` and was wrong about
which**, because `\\177` is DEL and **prints as nothing** — `kbs=[]` in the
output was `kbs=[DEL]`. Parsing the capability properly, rather than eyeballing
grep output, is what turned the answer up.

**The fix binds both bytes, before the terminfo binds**, so `bind`'s
replace-on-existing behaviour lets terminfo override either: `vt100-at` keeps
DEL as its Delete key via `kdch1=\\177`, while `vt100` — which has no `kdch1` at
all — leaves 127 unclaimed and gains a working backspace.

**Defaulting `LOGIN:116` to `xterm` was the other candidate and was rejected.**
The owner confirmed `TERM xterm` fixes all three consoles, but `xterm`'s `kbs`
is DEL, so it would break every terminal that sends `^H` — the same bug pointing
the other way — besides changing `cols`, colours and the function keys for
everyone.

**It is testable from a pipe**, because `keyin()` reads stdin and a piped byte
reaches the command-line editor exactly as a keystroke does — the same property
behind the BOM trap in §6. `gplbld/verify-keys.ps1` is new, unelevated, and
needs no account and no terminal.

**Not fixed, and recorded as next step 3:** `ED` and the `UPDATE.RECORD` screens
read raw bytes at `UPDREC:2171` and carry their own tables (`char(127)` →
`K$DELETE` at `UPDREC:2416`, `SED:4497`), so on a DEL terminal backspace there
still deletes **forwards**. The two bindings are trivial; the test that drives a
full-screen editor does not exist yet, and that is the actual work.

---

## 19 Aug 2026 — bp.OUT is fixed and BP and GPL.BP have moved

**Commit:** this one. **Install:** NOT CYCLED — the change landed after the
07:41:45 install and is unmeasured. `gplsrc` is untouched, so `make sd` is not
owed; `cycle.ps1` alone is. Block-balance pre-flight: 12 BASIC files, 0 with a
changed opener/closer delta — which §5.12 says in terms is **necessary and not
sufficient**.

**The defect first, because it had to go before `BP` could move.** `BASIC:132`
built the object file name from the token **as typed**, so `BASIC bp X` asked
for `bp.OUT` — while `CREATE.FILE` writes the VOC id as typed and upper-cases
the directory to `BP.OUT` (`CREATEF:378`, `UPSTREAM_FIXES.md` #6). The
three-case fold tries as typed, all lower, all upper and **reaches no
mixed-case id**, so the next `BASIC BP Y` found no VOC entry, tried to create
`BP.OUT`, and stopped with `Data pathname 'BP.OUT' already exists` — for ever,
since nothing clears it but deleting the file.

**The fix is two halves and either alone still produces a mixed name.** The
name now comes from the VOC record that answered the `open` — the read was
already there at `BASIC:143` and threw the answer away — **and the suffix
follows that name's case**, because `'.OUT'` is a literal and would rebuild
`bp.OUT` from a lower-case id. `out.suffix` rather than a literal in two
places: the Q-pointer branch appends the same suffix to a file name in another
account, and what creates the object file there is this same program applying
this same rule.

**`MICRO` was a tenth comparison site, and the earlier audit could not have
found it.** `MICRO:134` tested `InfileName[-2,2] = "BP"` to decide whether to
offer *"Compile?"*. That is a comparison against a **substring of a file name**,
not against a VOC id, which is the shape the 281-site grep of 18 Aug looked
for. It had been silently broken since 5.12 (a) made the per-account file `bp`
— the prompt simply stopped appearing. `upcase()`d now.

**What the id move cost:** four `voc_template` record renames (there the id
*is* the file name), the `"BP"` default source file in `BASIC`, `CATALOG` ×3,
`CPROC`, `CREATEA`, `FORMAT` and `GENERATE`; `openseq 'gpl.bp'` in `ERRGEN`,
`OPGEN` and `REVSTAMP`; five `$include GPL.BP` lines in `BBPROC` and
`PROG_INFO`; `first.compile`, `second.compile` and `bootstrap.py`;
`docs/TCL_VERBS.md`; a changelog entry; `verify-fold.ps1`'s SDSYS path.

**Two files had no `START-HISTORY` block at all** — `MICRO` and `PROG_INFO` —
so they were given one rather than the dated line going unrecorded.

**`verify-lcnames.ps1` gained §9, and its first act is to delete the object
file.** With one already present BASIC's `open` succeeds and the create branch,
the only place the name is built, is never reached — so the section would pass
while measuring nothing. It then reads the account VOC with **exact-match
reads**: `CT` folds and would answer for any spelling, while a `read` of a VOC
record does not fold at all, so `bp.out` / `bp.OUT` / `BP.OUT` are
distinguishable. The second assertion is the regression proper — a further
compile typed `BASIC BP`, because the failure was never in the compile that
made the file but in the next one, typed the other way.

**`$COMMAND.STACK` is now the only control left** in §3. Whatever moves it must
bring a replacement, and the obvious one is a record the verifier makes itself
rather than a shipped id.

---

## 19 Aug 2026 — A splatting mistake wore the tier filter's disguise

**Commit:** this one. **Install:** unchanged, 07:41:45, `sd.exe`
`339AB7157F002679`. `verify-fold` 10/10, `verify-createaccount` all PASS
including `voc (exact case)`, `verify-tiers` **22/22 on 393 / 411 / 421**.
Every verifier has now run against this install.

`post-cycle-elevated.ps1`, written earlier the same day, called
`& $path @($s.Args)`. **`@(...)` is an array subexpression, not splatting** —
splatting is `@name` on a variable — so the array went in as one positional
argument and was stringified. `verify-tiers.ps1` ran with
`$Prefix = "-Prefix sdtierg"` and tried to create accounts named
`-Prefix sdtierg1`.

**What made it expensive is what it looked like.** `CREATE.ACCOUNT` refused the
malformed name, `LOGTO` left every session in SDSYS, and the run reported all
three tiers holding **429** records with **0 of 18** capabilities withheld and
all **10** administration verbs present in a STANDARD account — the exact shape
of the silent full-VOC failure PROJECT_STATUS §5.12 warns about. 429 is simply
`voc_template`'s record count. The discriminator was one line in `sdsys/audit`:
`LOGTO REFUSED account=-PREFIX reason=not in the register`.

**Array splatting would not have fixed it either**, which is worth recording
because it is the obvious next guess. Measured against a probe script:
`& $p @($a)` gives `-Prefix sdtierg`; `& $p @a` on an array gives `-Prefix`,
because elements bind positionally; only `& $p @h` on a **hashtable** binds by
name and gives `sdtierg`.

**Two blind spots let it through, and both are worth more than the fix.**
`verify-tiers.ps1` section 1 tested `$out -notmatch $t.Name` — **a check that
could never fail**, since SD echoes the command it is given, so the name is in
the output whether the verb worked or refused. It now asserts the
`accounts\<NAME>` register record exists. And `verify-createaccount.ps1` had no
`Start-Transcript`; it was the only verifier without one, and an elevated
window does not paste its output back, so its exit 2 left no record at all.

**`CREATE.ACCOUNT` was never broken**, and the diagnostic that proved it did so
by creating a real account: `zzprobeacct` came out complete, with its directory
holding `$hold $hold.dic $svlists bp cat voc` — the lower-case `voc` from
`CREATEA:581`, confirming the rename in the same measurement that cleared the
verb.

Register and `user_accounts` were returned to `DON`/`SDSYS` and `don`
afterwards. Spent names now run to `sdacct15` and `sdtierh`.

---

## 19 Aug 2026 — Every SDSYS file name is lower case on disk

**Commit:** this one. **Install:** 07:41:45, `sd.exe` `339AB7157F002679`,
`assert-current` exit 0. `verify-lcnames.ps1` **115/115** (was 57),
`verify-credacl` / `-nocase` / `-osusers` exit 0, `make check-local` PASS.

§5.12 (a)'s wide half, and the answer to the owner's question of 18 Aug 2026:
`bp` and `voc` — and `gpl.bp`, `newvoc`, `voc_template`, `messages`, `syscom`,
`sd.voclib`, `accounts`, `bp.out`, `gpl.bp.out`, `pcode.out`, `$hold`,
`$hold.dic`, `$map`, `$map.dic`, `$ipc`, `$cred`, `voc.dic`, `dict.dic`,
`dir_dict`, `accounts.dic`, `os.users`, `os.users.dic`, `pstmp` — are lower
case in the installed `sdsys`, and each account's `voc` with them. 2,968 files
renamed plus 73 record ids in `gplbld/FILES_DICTS`.

**The VOC ids did not move.** Only the path text in fields 2 and 3 and the
directories themselves. `$include GPL.BP x`, `BASIC GPL.BP *` and `CD VOC` are
untouched, and `bp` / `$COMMAND.STACK` typed in lower case are still answered in
upper — the controls that say this is a rename and not a sweep.

**What decided the disk names, and it was one list.** `create.file <path>
DYNAMIC` in BASIC is a *language statement* that takes the path exactly as
given — not the `CREATE.FILE` verb, which upper-cases it (`CREATEF:378`,
`UPSTREAM_FIXES.md` #6). So `BBPROC`'s `FILES_LIST` and its `'.dic'` suffix
decide the case of everything the bootstrap creates, and `CREATEA:581` plus
`create.dir.file` decide it per account. No `CREATEF` change was needed, and
upstream #6 is still live and still unsent.

**No migration, and NTFS is the reason** — every one of these is reached
through a path in a VOC record or built from `@sdsys`, and NTFS matches without
regard to case. That is also why a *missed* reference would still have resolved,
so `verify-lcnames.ps1` §2a compares against the real directory listing with
`-ceq`; `Test-Path` could not have made the assertion at all.

**`git mv` fails differently for a directory than for a record.** With
`core.ignorecase` true, `git add -A` after the filesystem rename staged 2,968
**additions and no deletions** — `lstat("sdsys/GPL.BP/…")` still succeeds
against `sdsys/gpl.bp/`. The old index entries have to be removed by name with
`git -c core.ignorecase=false rm -r --cached <OLD>`. 2,950 then came out as
renames and 18 as add/delete pairs, those being the small records whose content
changed too.

**An agent shell cannot raise a UAC prompt, and this is the session that found
out.** `Start-Process -Verb RunAs` returned "The operation was canceled by the
user" **without ever displaying one**: a detached process has no desktop to show
consent on. Every elevated step — `cycle.ps1` and three verifiers — has to be
started by a human. `gplbld/post-cycle-elevated.ps1` is new and reduces the
three verifiers to one elevated command, each run without `-Keep` so nothing is
left behind; it is in `assert-current`'s `$neverShipped` list, or adding it
would itself have made the install stale.

**Two cheap checks that are worth doing before spending a cycle**, because both
catch the mistake this change was most likely to make and neither needs an
install: import `stage.py` and compare `SDSYS_SHIP`/`SDSYS_EMPTY` against
`os.listdir(sdsys)` as a set, case-exactly (`os.path.exists` cannot say this on
NTFS); and parse every `gplbld\*.ps1` with
`[System.Management.Automation.Language.Parser]::ParseFile`.

**Left deliberately:** `$COMO`, the one per-account on-disk name still upper
case — `COMO:44` and `PHANTOM:59` define the on-disk name and the VOC id with
one `$define`, and nothing in `gplbld` drives `COMO` to test a split with.
The empty `C:` directory in the installed `sdsys` survived the rename unchanged
and is still untraced.

---

## 18 Aug 2026 - The TCL commands are lower case, and a probe found the site the whole change depended on

**Commit:** this one and `8f808a3`. **Install:** 22:55:26, `sd.exe`
`A71C53652197195E`, `assert-current` exit 0. `verify-lcnames.ps1` **57/57**,
`verify-tiers.ps1` 22/22 with `COUNT VOC` 393 / 411 / 421, `verify-fold.ps1`
10/10, `make check-local` PASS, `verify-credacl` / `-nocase` / `-osusers`
exit 0.

**Correction to `8f808a3`'s commit message**, which says the fold was verified
"on the 22:57 install". It was the **22:49:57** cycle; 22:55:26 is this one.
The verification itself stands, 57/57.

### The probe that saved it

The previous entry's audit concluded "dispatch was never the risk", from reading
`PARSER:160`, which does fold three ways. **That was wrong, and only a probe
showed it.** A VOC record was written with the id `zzprobev` and dispatched:

```
zzprobev  ->  File name required            (dispatched)
ZZPROBEV  ->  ZZPROBEV is not in your VOC   (not)
```

`CPROC:1401` is where a typed verb is actually resolved, and it went **as
entered, then UPPER, then upper-with-hyphens-as-dots** — no lower-case attempt.
It is not among the 74 fold sites because its third tier is a `change()` rather
than a plain read, so it matched neither scripted shape and was passed over.
**Renaming the ids without this would have made every verb typed in upper case
fail, for every user, on the first login after the upgrade.**

**Why nothing earlier could have caught it:** nothing SD ships was lower case,
so every measurement to date exercised the fold's UPWARD half. The downward half
had never fired for a verb or a keyword. `verify-lcnames.ps1` §8 is now the
standing probe — it MAKES a lower-case verb and a lower-case keyword and reaches
them by typing the names in UPPER case, with a control for each.

### The rename

**792 ids**: 384 in `NEWVOC`, 397 in `VOC_TEMPLATE`, 11 in `SD.VOCLIB`, plus
field 3 of the 22 R records (which name the `SD.VOCLIB` record they point at)
and the contents of `TIER.OMIT.STANDARD` (18) and `TIER.ADD.ADMINISTRATOR` (10).

**Excluded, each for its own reason**: the 14 `$`/`%`/`@` records, which are
being renamed one at a time; the F/Q **file pointers** (`VOC`, `BP`, `NEWVOC`,
`GPL.BP`, `ACCOUNTS`, `MESSAGES`, `SYSCOM`, `QFILE`, `DICT.DICT`, `MD`,
`SD.ACCOUNTS`, `OS.USERS`, `BP.OUT`, `GPL.BP.OUT`), which are file names and
move with 5.12 (a); the two `T` tier-list records, which are data and never VOC
entries; and `!`, `#`, `&`, which have no case to change.

**`git mv` per file is not how to do 792 renames, and a plain `git add -A` does
not work at all.** `core.ignorecase` is true in this repository, so after the
filesystem renames `git add -A` reported only the content changes and **none**
of the renames — the index kept the old spellings and the commit would have
been silently wrong. Rename on disk through a temporary name, then
`git -c core.ignorecase=false add -A .`: one call, 787 staged as `R` and 5 as
add/delete pairs because their content had changed too.

**The evidence, on the installed system:**

```
CT VOC LIST         ->  VOC list
CT VOC CREATE.FILE  ->  VOC create.file
CT VOC VOC          ->  VOC VOC        <- the control: file pointers did not move
COUNT VOC / count voc                  ->  422 both ways
LIST VOC WITH TYPE = "F" / lower case  ->  11 both ways
```

**The bootstrap is itself a test of the fold** and it is the first one that
runs: `bootstrap.py` types `SECOND.COMPILE`, `THIRD.COMPILE` and
`RUN GPL.BP WRITE_INSTALL_DICTS NO.PAGE` in upper case against ids that are now
lower case. A broken fold fails there, loudly, before anything is installed.

**The tiers were the thing most likely to break quietly and did not.**
`verify-tiers.ps1` 22/22 with all three `COUNT VOC` figures exact, both shipped
tier lists matching the test's own copy, and both list records still absent from
every VOC. The `upcase()` on both sides of those comparisons, added in the
previous commit, is what made the list contents and the ids independent.

**`docs/TCL_VERBS.md` is left in upper case on purpose** — it is a comparison
against OpenQM 2.6.6, which spells them that way — with a note at the top saying
what is now stored and that it makes no difference to what you type.

---

## 18 Aug 2026 - Folding every remaining exact-match VOC lookup, before the TCL commands move

**Commit:** this one. **Install:** 22:37:20, `sd.exe` `A71C53652197195E`,
`assert-current` exit 0. `verify-lcnames.ps1` **50/50**, `verify-tiers.ps1`
22/22 with `COUNT VOC` 393 / 411 / 421, `make check-local` PASS,
`verify-credacl` / `-nocase` / `-osusers` exit 0.

**The owner asked for the TCL commands in lower case as well.** This entry is
the audit and the scaffolding; the rename itself has not been done.

**Dispatch was never the risk.** `PARSER:160` and `PARSER:270` already fold as
typed → lower → upper, so a verb typed in any case resolves. **Comparisons
were.** A grep for `= '<ID>'` over `GPL.BP` against the 390 word-shaped
`VOC_TEMPLATE` ids returned 281 sites, and all but nine are false positives:
`BCOMP`, `ICOMP` and `ACOMP` compare SDBasic language keywords and intrinsic
names; `ED`, `SED`, `DEBUG` and `PROC` compare their own sub-commands. Both are
separate namespaces and both compare against tokens that are already upcased.

**The nine that mattered, all folded and all additive** (every shipped id is
upper case, so the new attempts cannot fire until an id moves):

* `UPDREC:2584` — read the account VOC with `upcase(token)` and **nothing else**.
  5.12 had listed this as one of two sites "left deliberately... dictionary or
  token ids". It is not: it reads the VOC, which is a DYNAMIC file and therefore
  an exact byte match, and with upcase alone every keyword would come back -1.
* `QPROC:3835` — the query processor's VOC token read, as-typed only. Converted
  with a `fold.found` flag rather than three copies of the body, which carries
  `RETURN` and `GOTO`. The dictionary reads either side of it are untouched.
* `CPROC:397`, `CPROC:2723`, `APISRVR:486` — the LOGIN paragraph, read by exact
  literal. `new.sentence` now carries the id that matched, not the one asked for.
* `LOGIN:576`/`CREATEA:640` and `LOGIN:586`/`CREATEA:652` — **the tier filter,
  and the only silent failure in the set.** The guard compares an id from
  `READNEXT` against `'TIER.OMIT.STANDARD'`; the omit list holds verb ids
  compared against that id. Move one side without the other and nothing is
  omitted, so a STANDARD account is handed the compiler, both editors and
  `DELETE.CATALOG` — and it looks exactly like a filter that worked. Both sides
  `upcase()` now. `verify-tiers.ps1` 22/22 afterwards, all three counts exact.
* `DELETEF:172` — the banned-file guard. `file.name` reaches the `locate` **as
  typed** whenever the exact read at the top of `delete.file` succeeded; the
  `upcase()` at :148 is only in the else branch. So once `VOC` is `voc`,
  `DELETE.FILE voc` walks past the guard and deletes the account's VOC. Both
  sides `upcase()` now. Measured after: `DELETE.FILE VOC` answers "Cannot delete
  system file VOC" and `COUNT VOC` still counts 422. **The lower-case-exact path
  cannot be demonstrated until an id actually moves**, which is honest rather
  than tidy.
* `SETFILE:124` and `:136` — the default `QFILE` pointer, exact read then exact
  comparison. **Compiled, not run**: the block is only reached from the
  interactive prompt path.

**V-type field 4 is a separate namespace and stays upper case.** Of 17 distinct
dispatch strings only three are words — `UNION`, `INTERSECTION`, `DIFFERENCE`
on `LIST.UNION` / `LIST.INTER` / `LIST.DIFF`, compared with `=` in `LSTMRG`.
They are record content, not ids, so nothing needs to move.

### The audit found a live defect the $hold rename had already shipped

On the 22:26:18 install, with the VOC id already `$hold`:

```
CT VOC $HOLD     ->  VOC $hold                 (CT:202 folds the record id)
LIST VOC $hold   ->  1 record(s) listed
LIST VOC $HOLD   ->  0 record(s) listed, '$HOLD' not found
```

`QPROC`'s `check.record` read the record id exactly and had no fold at all, so
`CT` and `LIST` disagreed about the same name. The changelog entry written
earlier the same day promised "the old spelling still works when you type it" —
true of `COUNT`, `CT` and `ED`, false of `LIST`. Both are corrected: the read
now folds and rewrites `id` to the spelling that matched, and the changelog
carries a `CORRECTION` entry.

**`verify-lcnames.ps1` tested `CT` and `COUNT`, and neither could ever have
shown this, because both fold.** A verb that folds cannot be the instrument for
a verb that does not. It now tests `LIST` both ways with an absent-id control,
which is what takes it from 46 checks to 50.

**What the rename itself still costs:** 387 command ids in `NEWVOC`, 400 in
`VOC_TEMPLATE`, 11 in `SD.VOCLIB`, each a case-only `git mv` in two steps; the
contents of `TIER.OMIT.STANDARD` (18) and `TIER.ADD.ADMINISTRATOR` (10);
`verify-tiers.ps1`'s name lists; `docs/TCL_VERBS.md`. The 14 `$`/`%`/`@`
records and the F/Q file pointers are deliberately excluded — they are file
names, not commands, and belong with 5.12 (a).

---

## 18 Aug 2026 - The second VOC-id rename, and two harness defects the documented post-cycle sequence exposed

**Commit:** this one. **Install:** 21:29:59, `sd.exe` `A71C53652197195E`,
`assert-current` exit 0. `verify-lcnames.ps1` **46/46**, `verify-fold.ps1`
10/10, `make check-local` PASS, `verify-credacl` / `-nocase` / `-osusers`
exit 0.

**The VOC id `$HOLD` is now `$hold`** — PROJECT_STATUS.md §5.12 (b), the second
rename after `$savedlists`, and the one the fold work of the previous session
was built for. Changed: `CLEANAC:72`, `MICRO:60`, `SPVIEW` (95, 106, 346),
`_NEXTPTR:39`, `_PRFILE:56`, `SETPTR` (334, 612, 639, 811), `CREATEA:759`,
`MESSAGES` 7119/7131/7170, `NEWVOC/SP.VIEW`'s description text, and
`VOC_TEMPLATE/$HOLD` renamed to `$hold`.

**`VOC_TEMPLATE` was the new part.** `$savedlists` had no record there, so this
was the first rename where the VOC id *is* a file name on disk: `BBPROC:181`
copies each `VOC_TEMPLATE` record into SDSYS's own VOC by id. `core.ignorecase`
is true in this repository, so the rename went through a temporary name —
`git mv '$HOLD' 'zz$hold.tmp'` then `git mv 'zz$hold.tmp' '$hold'`. Fields 2 and
3 still read `$HOLD` / `$HOLD.DIC`: those are SDSYS's names **on disk**, which is
5.12 (a)'s wide half and deliberately did not move.

**The `"$HOLD "` prefix moved too, and both sides fold rather than flip.**
`SETPTR` writes that marker in front of a hold-file record name and
`to_file.c`'s `start_file()` reads it back. It is never looked up in a VOC, but
it is displayed by `sysmsg(7120)` and `sysmsg(7171)`, and the previous session's
`to_file.c` comment had explicitly deferred it to this work. `SETPTR`'s three
tests took `downcase(...)` and the C took `MemCompareNoCase`, because the BASIC
half is built by the bootstrap and the C half by `make sd` — neither may depend
on the other having moved.

**`UPSTREAM_FIXES.md` #8 came out of that line.** `memcmp(pu->file_name,
"$HOLD ", 6)` reads six bytes of an allocation sized `strlen + 1`, and
`SETPTR ... AS PATHNAME /tmp` makes that five. Present on `sdb64` `main` and
`origin/dev`. `MemCompareNoCase` returns at the first difference, so the fix
carried the overread away with it; upstream's fix is `strncmp`.

**No migration, measured two ways.** `verify-lcnames.ps1` §5a renames the id
back to `$HOLD` with a BASIC toggle in `bp`, then measures `open '$hold'`
(answers `OPENED=YES`, the direct test of the hard-coded literal) and
`SETPTR ... AS NEXT` (writes `ZZN..._0001`). **The second exists because
`_NEXTPTR` fails silently**: it presets `seqno` to `'0'` and only a successful
`open 'DICT','$hold'` replaces it with `fmt(...,"4'0'R")`, so a missed lookup
writes `_0` and a hit writes four digits. The assertion is on the **width**, not
on `_0001` — `$NEXT` persists in `$hold.dic`, so a second run on one install
legitimately gets `_0002` and an exact match would fail on a change that works.

### Harness defect 1: `BASIC bp X` leaves a `bp.OUT` nothing can open again

`verify-nocase.ps1` and `verify-osusers.ps1` both exited 2 on the fresh install
with `Data pathname 'BP.OUT' already exists / Unable to open newly created
output file`, which reads exactly like the broken-bootstrap install of 16 Aug.

`BASIC:132` builds the object file name from the source name **as typed**, so
`BASIC bp X` asks for `bp.OUT`. `BASIC:135` opens it through the three-case
fold, finds nothing, and `BASIC:157` runs `CREATE.FILE DATA bp.OUT DIRECTORY` —
which stores the VOC id as typed (`bp.OUT`) and the directory upper-cased
(`BP.OUT`). That is `UPSTREAM_FIXES.md` #6. **The fold tries as typed, all
lower, all upper, and none of those reaches a mixed-case id**, so the next
`BASIC BP Y` finds no VOC record, tries to create `BP.OUT`, and the directory is
already there — permanently.

It appeared only now because 5.12 (a) made the per-account file `bp`, so scripts
and people type `bp`; before that everyone typed `BP` and the two spellings
agreed. `verify-lcnames.ps1`'s `Remove-Probes` now runs
`DELETE.FILE bp.OUT FORCE`, and only when that run created the file. **The
underlying defect is not fixed** and is item 3 of PROJECT_STATUS's next steps:
`BASIC:135` already knows which VOC record answered, and that is where the
object name should come from.

### Harness defect 2: `assert-current` check A2 made `make check-local` a permanent false stale

A2 flags any file under `gplsrc` newer than the oldest binary in `bin\`. It did
not inherit check B's `localtest\` exclusion, and `make check-local` builds
`gplsrc\sdclilib\localtest\local-connect-test.exe`. So from the moment the
documented post-cycle sequence reached step 2, every `assert-current` said STALE
and every verify script refused — and no reinstall clears it, because the next
`check-local` recreates the file. Check B's comment, added 17 Aug for
`__pycache__` and `localtest`, describes this failure precisely; A2 was written
on 18 Aug and was one place short. Both exclusions are now in both checks.

**Also corrected:** this file and PROJECT_STATUS carried `gcat` 132 and
`GPL.BP.OUT` 193. Those are pre-SDNet-removal figures. Every cycle run on
18 Aug 2026 reported **129** and **190**, including the ones that passed 36/36
before this session.

---

## 18 Aug 2026 - A silent install blocked on a message box, and CurPageChanged was the entry point nobody guarded

**Commit:** see the commit that carries this entry. Twenty-fourth session,
after the entry below.

**What was wrong.** `cycle.ps1 -Silent` passes `/VERYSILENT`, which skips the
wizard. It did not skip `CurPageChanged`, and the box at `sd.iss:1338` - the
one saying SD will not touch an OpenSSH Server that is already installed -
appeared with nothing behind it and copied not one file until somebody clicked
OK. **`CurPageChanged` fires in silent mode**: Inno creates the wizard form and
simply does not show it, so "the page was never displayed" is not the same as
"the page never changed". The box also explains why two options are "absent
from this page", which is incoherent in a mode that shows no pages.

**The fix** is the guard the file already used - `if WizardSilent then Exit;` -
as the first statement of `CurPageChanged`. Verified by running a `-Silent`
cycle through: no dialog, no `MainWindowTitle` on the setup process (the
previous run showed "Setup"), install at 21:03:32, `assert-current` exit 0, and
`verify-lcnames.ps1` 36/36 on that install.

**Two claims made earlier in the same session were wrong, and the corrections
are worth more than the fix.**

1. **"`sd.iss` uses plain `MsgBox` at all six sites and none are guarded" is
   false.** Five of six were already guarded, deliberately and with a comment
   explaining why - `WizardSilent` in `CurStepChanged`, `UninstallSilent` in
   `CurUninstallStepChanged`. The fault was one missed entry point, not a
   file-wide pattern, and describing it as the latter would have sent the next
   session rewriting five working call sites.
2. **`SuppressibleMsgBox` was the wrong prescription**, offered before reading
   the surrounding code. It is driven by `/SUPPRESSMSGBOXES`, which
   PROJECT_STATUS.md section 6 records as MEASURED on 14 Aug 2026 not to reach
   `[Code]` message boxes at all - which is precisely why the author chose
   `WizardSilent` instead. Taking it would have added a second idiom that does
   not work beside a first one that does.

**A claim in PROJECT_STATUS.md section 6 was also incomplete and is corrected
in place**: "`gplbld/sd.iss` now checks both" was true of the install and
uninstall paths and silently not true of `CurPageChanged`.

---

## 18 Aug 2026 - The first VOC id is lower case, and a rename cannot be tested by "not found"

**Commit:** see the commit that carries this entry. Twenty-fourth session.

**What changed.** PROJECT_STATUS.md 5.12 (b), first rename: the VOC id
`$SAVEDLISTS` is now `$savedlists`. With it went the 13 hard-coded
`open "$SAVEDLISTS"` literals in `GPL.BP` and their `recordlocku`/`write`
pairs, COPYLST's four name comparisons, `CREATEA:759`, `MESSAGES`
3248/3249/3250/6462, and the `EDIT.LIST` record in both `NEWVOC` and
`VOC_TEMPLATE`. The name on disk, `$svlists`, did not move: (a) and (b) are
independent, and this is what showed it. Verified `verify-lcnames.ps1` 36/36 on
the 20:34:25 install.

**No migration, and it was simulated rather than assumed.** An account created
before the rename holds `$SAVEDLISTS` while the code now opens the literal
`$savedlists`; what reaches it is `_VOC_REF` folding UP as well as down, added
the session before. `verify-lcnames.ps1` section 5 writes a BASIC toggle into
the account's `bp`, renames the id back to `$SAVEDLISTS`, drives
`SAVE.LIST`/`GET.LIST` through it, and restores it. A failure part-way leaves
the account on `$SAVEDLISTS`, which is the state the section asserts works.

**Correction to a claim made earlier the same session: "not found" is the wrong
instrument.** Two checks asserted that `CT VOC $SAVEDLISTS` would now answer
"Record not found". Both failed on the 20:21:53 install. **`CT` folds the
record id as well as the file name** (`CT:202`, one of the 74 fold sites), so
it finds the record whichever case is typed - and `CT:215` prints the id it
MATCHED, not the one typed. That echo is a better instrument than the one
intended: typing `$SAVEDLISTS` and being answered `VOC $savedlists` is the
rename demonstrated, and the control is `CT VOC $hold` still answering
`VOC $HOLD`. The changelog entry claiming `CT VOC $SAVEDLISTS` no longer finds
a record was corrected before the commit.

**Two harness facts, each of which cost a cycle:**

1. **A verify script is exempt from `assert-current`; `sdsys/changelog` is
   not.** `verify-lcnames.ps1` is in the `$neverShipped` list, so editing it
   does not void an install; the changelog ships, so editing it does. Both were
   corrected in one go, which voided the 20:21:53 install and bought a second
   cycle. Order the exempt fixes first, re-measure, then touch `sdsys`.
2. **`cycle.ps1 -Silent` is not unattended.** `sd.iss` uses plain `MsgBox` at
   all six sites and Inno suppresses only `SuppressibleMsgBox`, so
   `/VERYSILENT` skips the wizard and still blocks on every prompt. The box
   that blocked was `sd.iss:1338`, which says "the two ssh options are absent
   from this page" - about a page silent mode never showed. Not fixed.

**Also corrected in passing.** `cycle.ps1`'s wholeness hint had read "want ~132
/ ~193" since SDNet was removed (`c893308`) took three programs out; the true
figures are 129 and 190, and the guard thresholds (100/150) never needed to
move. And PROJECT_STATUS.md's header had carried a BEL byte where the backslash
in `gplbld\assert-current.ps1` belonged, so the one command it tells a new
session to run named a path that does not exist.

**Still open.** `$HOLD` is the next id and is wider - `to_file.c` builds `$HOLD`
paths in C, and `SETPTR`, the spooler and `CLEANAC` all name it. `$HOLD`, `BP`
and `$COMMAND.STACK` are the controls in `verify-lcnames.ps1` section 3 today,
so whichever moves next takes its own control with it.

---

## 18 Aug 2026 - Repository renamed to sd4windows

**Commit:** see the commit that carries this entry.

Owner's instruction. The local working tree moved from
`C:\Users\dmont\Projects\sdb_ai_windows` to
`C:\Users\dmont\Projects\sd4windows`, and the GitHub repository from
`dmontaine/sdb_ai_windows` to `dmontaine/sd4windows`.

**Earlier entries in this file still name the old path, and that is correct** -
rule 1 is append-only, and a command recorded in a 15 Aug entry was run against
the path that existed then. Read `sdb_ai_windows` in any entry above this one as
today's `sd4windows`.

**The vendored tree `sdb_ai/sd64` is NOT renamed.** That is the upstream variant
the port is built on (section 2), not the repository, and its name is part of
how the three generations are told apart.

Updated: `CLAUDE.md`, `PROJECT_STATUS.md` (3 places), `gplbld/cycle.ps1` and
`gplbld/verify-apiport.ps1` `.EXAMPLE` blocks, and `.claude/settings.local.json`
(untracked, but its permission entries match on the literal path). Build output
under `gplobj/`, `bin/`, `stage/` and `pcode_bld.log` carries the old path in
debug strings and is regenerated by the next build; none of it is tracked.

---

## 18 Aug 2026 - The fold reached only half the lookups, the per-account files went lower case, and a C change was cycled without being compiled

**Commit:** see the commit that carries this entry. Twenty-third session.

Two sessions ran concurrently in this repository, both on "pull continue",
started five minutes apart. The older one (started 19:07) did §5.12 (a) and
`COPYP`; the newer one found the collision at 19:14 by noticing `git status`
had gone from clean to seven modified files mid-session, stopped editing, and
messaged the finding across. The owner then stopped the older session and had
the newer take over its uncommitted work. **`git status` at session start is a
snapshot, not a subscription** - nothing warns you that another session is
writing to the same tree.

### The fold covered the command line and not the BASIC OPEN statement

`GPL.BP/_VOC_REF` was not among the 36 files commit `0d62cf9` changed, and it
had no fold of any kind - one exact-match read at `:72`, then the `PATH:` /
`Account:File` special syntax. It is `pcode_voc_ref`, which
`get_voc_file_reference()` (`op_dio1.c:481`) recurses into, so it resolves the
name for **every** BASIC `OPEN` (`op_dio1.c:624`) and for `op_seqio.c:193`,
`:453`.

**The 74 folded sites work by trying a name in three cases and handing each one
down to that exact-match read.** That is why every verb passed the earlier
verification while nothing had actually been fixed for programs. A hard-coded
literal got no fold at all, so `open "$SAVEDLISTS"` - in `SAVELST`, `GETLIST`,
`DELLIST`, `LSTMRG`, `COPYLST`, `SAVESTK`, `CLEANAC`, `UPDREC` and the three
`_` recursives, 13 sites - would have broken at the first VOC-id rename.

Measured on the 18:54:10 install before the change, with a probe program written
straight into an account's `BP` (a directory file, so a record is a file on
disk): VOC id `zzprobe1` could not be opened as `ZZPROBE1` while
`COUNT ZZPROBE1` found it, and VOC id `ZZPROBE2` could not be opened as
`zzprobe2`. Fixed at `_VOC_REF:102` with a flag and a `goto` rather than a
nested block, so the special syntax kept its indentation - the file already
jumps to `parse.as.q.pointer` from inside its own case statement. The Q-pointer
target at `:272` took the PLAIN shape. `verify-fold.ps1` gained section 4, which
compiles a probe because no verb can reach this lookup. 10 of 10 on the 19:46:12
install.

### §5.12 (a), the per-account file names

A new account holds `$hold`, `$hold.dic`, `$svlists` and `bp`. `CREATEA`'s
`os.name` values and `create.dir.file`'s `.dic` suffix, the create-if-missing
fallbacks in `SAVELST`, `COPYLST` and `SAVESTK`, and `to_file.c`'s three
hold-file paths. The VOC ids are unchanged, which is why this could go first.
No migration: each account's VOC names its own files and NTFS matches either
case. `verify-lcnames.ps1`, 26 of 26, with `VOC` still upper case as the
deliberate control and `cat` lower since before the port.

`Test-Path` cannot make this assertion - NTFS matches `$HOLD` against `$hold`,
so it passes whichever case was written. Every name check compares against the
directory listing with `-ceq`.

### A C change was cycled, installed, tested and passed without being compiled

**`cycle.ps1` contains no `make`.** It stages whatever is already in `bin\`.
`to_file.c` was edited at 19:15 and cycled at 19:38 against `bin/sd.exe` built
at **17:17**.

Both `assert-current` checks passed, and neither was wrong to. Check A compares
installed `sd.exe` against `bin/sd.exe` - equal, because both were stale. Check
B compares source mtimes against the **install** time, and 19:15 is older than
19:39. The script's header reasons carefully about the opposite direction
("most changes here are BASIC, so hashing `sd.exe` is not enough"); nothing
covered this half.

**And the test for the change passed too**, which is what made it invisible: the
change was `$HOLD` to `$hold` in a relative path, NTFS matches either, so both
binaries behave identically. `verify-lcnames.ps1` §4 carried a comment claiming
it measured the C literal. It cannot, on Windows, and the comment was corrected
rather than the check removed - it is still a good regression guard on
`CREATEA`'s rename.

`assert-current` check **A2** now refuses any file under `gplsrc` newer than the
oldest binary in `bin\`, naming it; run against the tree as it stood it printed
`18 Aug 19:15:43 gplsrc	o_file.c`. Oldest rather than `sd.exe` alone, so
`gplsrc\sdclilib` and `gplsrc\sdsvc` count. The discriminator is the hash:
`DA280984D21571B4` to `A6AAAB58AAB676F4`.

Whether `cycle.ps1` should run `make` is **not decided**. Building inside an
elevated cycle would leave objects owned by an elevated token, and the build
needs an MSYS2 login shell where the cycle is PowerShell.

### Correction: the five malformed VOC_TEMPLATE entries were never broken

Supersedes the claim made in PROJECT_STATUS §8 from 16 Aug 2026 and repeated in
the entry below, *SDNet removed, UNLOCK repaired...*, and in the `changelog`
entry shipped 18 Aug 2026 saying `UNLOCK` "never worked".

`CPROC:1410`, in the source and directly beside the test, says the type code
**may be followed by comment text with no intervening space** - the PI /
PI-open / UniVerse rule - and `CPROC:1433` tests `voc.entry.type[1,1]`. So
`Verb to unlock records` is a `V` with a comment and dispatches normally. The
record is not shifted either: fields 2 and 3 are correct in both the "malformed"
and the correct records.

Measured rather than re-read: `verify-lcnames.ps1` section 6 builds a VOC record
from scratch with a descriptive type field, pointing at `$COPYP`, and it answers
`File name required` - which only a dispatched verb produces. The older
concurrent session had independently measured that `COPYP` already worked on the
18:54:10 install before changing it.

So `UNLOCK` was not repaired on 18 Aug 2026 and `COPYP` was not repaired on the
23rd session; both were working. The restart-SD workaround used that day to
clear a stuck record lock was never necessary. Both records are still bare `V`,
because the inconsistency with every other verb is what produced the misreading,
but that is tidying and not a fix. An `UPSTREAM_FIXES.md` entry reporting all
five to upstream was written and **withdrawn** - `../sdb64` has all five, but
there is no defect to report. `LOAD.LANGUAGE` was also found not to exist: it
was removed with the language verbs in `ecd62b2` on 17 Aug 2026, and was never
the zero-byte file PROJECT_STATUS described.

---

## 18 Aug 2026 - SDNet removed, UNLOCK repaired, and a killed session explained three failures at once

**Commit:** this one. Twenty-second session. `gplbld/verify-nonet.ps1`,
**16 of 16**, exit 0, on the **18:54:10** install, `sd.exe`
**`DA280984D21571B4`**.

**IT WAS STILL THERE.** The owner believed the network file capability had gone
with telnet, for the same reason - the client protocol is insecure. It had not:
`netfiles.c` (1,227 lines) was compiled, `op_dio1.c:635` treated any VOC file
reference containing `;` as `server;remote_file` and called `net_open()`, and
the three server verbs shipped. **The `NETFILES` parameter that looks like an
off switch was parsed, stored in the shared segment, reported by `CONFIG` - and
tested nowhere.** `net_open()` read host, user and password from `sd.conf`,
connected on port 4245, and de-obfuscated the password with a rolling
substitution over a fixed alphabet; the code's own comment at `netfiles.c:564`
calls it "a very simple encryption".

**LATENT, NOT LIVE, AND THE DISTINCTION WAS WORTH ESTABLISHING BEFORE ACTING.**
A server must be named in an `[sdnet]` section of `sd.conf`; with none defined
every remote open failed `ER_SERVER`. Neither the shipped nor the installed
`sd.conf` had one.

**THE SEPARABILITY CHECK CAME FIRST**, because the owner's condition was that
the remote API keep working. **`sdnet.h` is NOT SDNet** despite the name - it is
the socket/termios portability header (`SOCKET`, `closesocket`, `NetError`),
included by `sdclilib.c`, `linuxio.c`, `lnxport.c` and `op_skt.c`. Deleting it
would have broken the client library. Only `netfiles.c` and its call sites were
the feature.

**Removed:** `netfiles.c`; 30 `NET_FILE` branches across `op_dio3` (12),
`dh_ak` (6), `op_lock` (5), `op_dio4` (2), `op_dio1` (2), `op_dio2` (1); the
`;` dispatch; the `net_*` prototypes in `sd.h`; `DELSRVR`, `SETSRVR`,
`LISTSRVR`; `DELETE.SERVER`, `SET.SERVER`, `LIST.SERVERS`. **Kept
deliberately:** `sdnet.h`, `APISRVR`, the `NETFILES` parse (or an existing
`sd.conf` stops SD starting - the `CREATUSR` trap), the `sysseg` field (removing
it shifts the shared-segment layout), and `K_GET_SDNET_CONNECTIONS`, which now
returns an empty list so `INT$KEYS.H` numbering does not move.

**THREE TRAPS, ALL FOUND BY THE COMPILER:** `gpl.src` is the build list
(`Makefile:61`), not the `*.c` wildcard, so deleting the file gave "No rule to
make target 'netfiles.o'"; `sd.h` changed and the Makefile tracks no header
dependencies, so objects had to be cleared; and removing a branch orphans its
locals - but one orphaned declaration was still needed by the surviving `else`,
so a blanket delete broke the build.

**`UNLOCK` WAS REPAIRED IN THE SAME CYCLE, AND IT HAD JUST COST REAL TIME.** Its
`VOC_TEMPLATE` entry held the description, "Verb to unlock records", in field 1
where the type code belongs - one of the five malformed entries §8 recorded on
16 Aug. Field 1 is now `V`. There is no description field to move the text to;
correct records do not carry one. **`COPYP` still needs the identical fix.**

**AND THE THING THAT COST THE MOST: ONE KILLED SESSION CAUSED THREE SEPARATE
FAILURES THAT LOOKED UNRELATED.** A `verify-fold.ps1 -Cleanup` run was killed at
a `DELETE.FILE` prompt. It left (a) the update lock `DELETEF:145` takes on the
VOC record, so later attempts **blocked silently** - SD echoed the command and
printed nothing, which reads like another prompt and is not; (b) its user-table
slot occupied, so `sdwind` would not shut down and the next `cycle.ps1` refused
to start with "SD is still running: sdwind(8792)" **while the service itself was
already Stopped**; and (c) no way to clear (a), because `UNLOCK` is the command
for exactly that and was the malformed entry above.

Two attempts were spent guessing at which prompt had caught it. What identified
it was **bounding the harness**: `Invoke-SD` now runs SD in a job with a 45
second timeout and returns whatever SD printed, so the empty output after
`:DELETE.FILE zzlcfold1 FORCE` became visible and named the cause. Both
verifiers carry the timeout and a note saying what a timed-out call leaves
behind.

**`FORCE` is still right and stays**: `DELETEF` prompts separately for the DATA
and DICT parts, each in an unbounded `until yn = 'Y' or 'N'` loop, and **only
when the stored path differs from the default name** - which is exactly what
`CREATE.FILE`'s upper-casing of a lower-case name produces. So a lower-case file
cannot be deleted from a script the way an upper-case one can, which will be met
again during the renames.

---

## 18 Aug 2026 - The name fold gained a lower-case attempt, at 74 sites rather than the eight that were written down

**Commit:** this one. Twenty-second session. `gplbld/verify-fold.ps1`, **5 of 5**,
exit 0, on the **16:24:23** install.

**What changed.** Every lookup that resolved a name tried it AS TYPED and then,
if that failed, in UPPER case - and nothing else. The chain is now **as typed →
lower → upper**. Purely additive: every id on today's tree is upper case, so the
new attempt cannot hit until renames start. It closes the live defect where
`CREATE.FILE testlc` registers the VOC entry as `testlc`, reports "Created DATA
part as TESTLC", and `COUNT TESTLC` then answers "File not found" - the name the
command itself just printed.

**§5.12 SAID EIGHT SITES. THERE WERE 76, IN 38 FILES.** The list in the document
was the subset someone had looked at. 63 were converted by a scripted transform
over the two regular shapes, 11 by hand where the shape was irregular, 4 left
deliberately: `CPROC:2600` and `LOGIN:690` read `ACCOUNTS` by **account name**,
which stays upper case and is what makes signing in case insensitive, and
`QPROC:3848`/`UPDREC:2584` have no as-typed attempt at all, so there is no fold
to extend.

**FOUR TRAPS, AND THE LAST TWO ARE THE ONES WORTH REMEMBERING** because they
passed a clean compile:

1. **Fold sites nest.** `CPROC`'s RUN block holds three, one inside another, so
   indices taken before the first edit are stale by the second. Batch conversion
   silently skipped the outer sites. Recompute after every conversion.
2. **A converted site re-detects itself** - the inserted `end else` becomes the
   line above the `upcase` attempt, so a one-line "already done?" test loops
   forever.
3. **`if cond then <statement>` followed by `else` / `end` is a block whose
   opening line does not end in `then`.** Missing it stopped the matching-end
   search one `end` early, so the inserted `end` landed inside the wrong block
   and put `return` on the wrong side of a branch in `BCOMP`'s
   `open.include.record`. **It compiled and it balanced.**
4. **The trailing rewrite is not always `X = upcase(X)`.** `BCOMP`'s
   `get.file.ref` has `token = upcase(token.string)`. Rebuilding it from the
   left-hand side gave `token = downcase(token)`, reading `token` before it was
   assigned - **"Unassigned variable in $BCOMP"**, which stopped the bootstrap
   while it was compiling `TERM`. Mirror the existing line; do not regenerate it.

**THE COST WAS ONE BOOTSTRAP, AND THAT IS THE POINT OF `-SkipInstall`.** Traps 3
and 4 were invisible to review and to a block-balance check - the count is
unchanged whether the `end` is in the right place or not - and the bootstrap
found both in four minutes without spending an install. The balance check is
still worth running (36 files, 0 unbalanced) but it is necessary, not
sufficient; that is now written into §5.12.

**Verified, not assumed.** The verifier creates a lower-case file and checks the
name `CREATE.FILE` reported back now resolves; an upper-case file is the control,
because a fold that resolved everything downward would pass the first check and
break every existing system; and a name in no case at all must still be refused,
because a fold that answered "found" to everything would pass both.

---

## 18 Aug 2026 - The global catalogue was writable from inside SD, and is now gated and locked

**Commit:** this one. Twenty-second session. `gplbld/verify-catgate.ps1`,
**25 of 25**, exit 0, on the **11:35:44** install.

**What was wrong.** `CATALOG` selects the global catalogue two ways and checked
one. The `GLOBAL` keyword tested `K$ADMINISTRATOR` (since 13 Aug 2026); a call
name beginning `*`, `!`, `_` or `$` selects `CAT_GLOBAL` at `CATALOG:158`,
`:172` and `:183` and tested nothing, so `CATALOG BP $MYPROG` was allowed where
`CATALOG BP MYPROG GLOBAL` was refused. `DELCAT` had no privilege test anywhere
in it, by either route. `gcat` holds `$LOGIN` as object code and `CPROC:315`
calls it for every session, so this was code execution in everybody's session
and, through `DELETE.CATALOG $LOGIN`, a way to stop the machine signing in.
Both need only `CATALOG`/`DELETE.CATALOG` in the VOC, which PROGRAMMER has and
STANDARD does not (`NEWVOC/TIER.OMIT.STANDARD`).

**Why it mattered more than the handoff thought.** PROJECT_STATUS had `gcat` as
an Explorer/RDP exposure that `RDPUSER` would unlock. It was reachable from
inside SD with no desktop, no RDP and no `OS.EXECUTE`.

**Fixed** with one test where `mode` is finally known (`CATALOG:191`, so a
fourth route inherits it) and a pre-loop scan in `DELCAT:89` (before the loop,
so a mixed list deletes nothing rather than stopping half way). The keyword's
own test was left where it is - it reports while parsing. Upstream has both:
`UPSTREAM_FIXES.md` entry 7, checked against `../sdb64`.

**And locked**, owner's decision the same day: `gplbld/secure-gcat.ps1` puts
`sdusers:(OI)(CI)(RX)` on `gcat` and, after a second instruction, on
`GPL.BP.OUT` as well; `sd.iss`'s `SecureGcat` runs it at `ssPostInstall` beside
the credential store and the shell list. A gate in a program protects that
program; the ACL protects the directory from code not yet written.

**The price, accepted deliberately:** cataloguing globally now needs a genuinely
elevated session, because `sd.exe` stays unelevated for life and a filtered
token carries `Administrators` deny-only - so a session that reached SDSYS
through the elevation helper has `K$ADMINISTRATOR` true and is refused by NTFS.
Measured: an unelevated write into `gcat` throws. The changelog says so in
plain English.

**What it cost: five verifier runs, and not one of them was the fix.** Worth
recording because every failure was in the scaffolding and each looked at first
like a defect in the change:

1. **A probe the account did not have.** Section 3 used `CREATE.ACCOUNT` to show
   the session was unprivileged. That verb is ADMINISTRATOR-only, so a
   PROGRAMMER account has no such verb and SD answered "not a known verb" - the
   check reported the session as *privileged*. Replaced with `CATALOG ... GLOBAL`,
   the pre-existing gate, so the new code does not vouch for itself.
2. **A prompt down a pipe.** Cataloguing the same name `LOCAL` after private
   makes `check.private` (`CATALOG:463`) ask "Program is also in private
   catalogue. Remove?" in an unbounded `loop ... until yn = 'Y' or 'N' repeat`.
   The pipe had no answer, the prompt ate the remaining commands, and the run
   stopped dead with no summary. Two different program names fixed it;
   `NO.QUERY` would have silenced it by *deleting* the other entry, which is not
   what the check is for.
3. **A teardown with two lifetimes in it.** An auto-clean for leftover accounts
   called the whole of `Remove-Made`, which also deleted the control's own
   `gcat` entry mid-run and failed sections 4 and 7. Split into
   `Remove-Account` and `Remove-Fixtures`.
4. **A check that could never pass — and a wrong finding published from it.**
   A precondition tested `sdsys\VOC\<name>` as a file. **A VOC record is not a
   file: `VOC` is a DYNAMIC file** (`CREATEA:575`), on disk a directory of
   `%0`/`%1` buckets - `sdsys\VOC` holds two files whatever its record count. It
   refused a `CREATE.FILE` that had printed "Created DATA part as ..." directly
   above the refusal. **That check had already produced a confident, wrong
   diagnosis** of run 3 - "CREATE.FILE wrote no VOC entry" - which was reported
   to the owner and is retracted here. The step now asks SD what it did.

**Still unexplained**, and now in §8 rather than guessed at: on the one run that
reused a scratch file name a previous run had `DELETE.FILE`d, `BASIC` produced
no `.OUT`. Not reproduced. The verifier uses per-run names and prints SD's
output, so a recurrence carries its own evidence.

**The general lesson, which this file has now recorded in a new form:** a
control that cannot be built is "could not be run", never a FAIL. Four of the
five runs reported failures against the code under test when the scaffolding
had collapsed. `verify-catgate.ps1` now exits 2 with SD's own output whenever a
fixture step fails.

**Two findings for the per-account ACL work that is next**, both cheap and both
changing how it should be built:

- **No new mapping is needed.** §5.7 assumed per-account ACLs would add a
  Windows-user-to-account mapping. `LOGTO` is already gated on membership of the
  account's `ACC$GROUP` (`CPROC:3697`), written by `CREATEA:545` as `sdu_<name>`
  and maintained by `GRANT` (`GRANTA:201`). Granting the account directory to
  `ACC$GROUP` makes the file layer mirror the SD layer exactly.
- **A create-time write would not reach existing accounts.** Every ACL step
  names a fixed path and none carries a `Check`, so an install over an existing
  tree re-applies all of them - which is why `gcat` will reach an old tree even
  though `NEWVOC` will not (`sd.iss:167`, `Check: DataTreeAbsent`). Nothing
  enumerates accounts, so a per-account ACL set by `CREATEA` alone would exist
  only on accounts made afterwards, with no migration and a tree that looks
  correct. The work needs a re-apply step as well.

---

## 18 Aug 2026 - One upstream defect from this session's findings, and five that are ours

**Commit:** this one. Twenty-first session.

`UPSTREAM_FIXES.md` gains **entry 6**: `CREATE.FILE` writes the VOC entry under
the name as typed (`CREATEF:108`, `:460`) but upper-cases the name on disk and
the paths in fields 2 and 3 (`:301`, `:374`), so `CREATE.FILE testlc` reports
"Created DATA part as TESTLC" and then `COUNT TESTLC` answers "File not found"
while `COUNT testlc` works. Verified against `git -C ../sdb64 show` on **both
`main` and `origin/dev`** - identical line numbers - and not Windows-specific,
since the mismatch is between the VOC id and the stored path rather than between
the path and the filesystem. No fix proposed: either direction closes it and the
choice is a policy decision for upstream, not for a port.

**Checked and deliberately NOT added, so nobody re-checks them:**

- **`SET_PASSWD`'s `pterm` save/restore** (saves the value it just wrote). The
  lines carry a `14 Aug 26 Windows port` marker and replaced an
  `OS.EXECUTE "sudo passwd"`; `_INPUT` does the same save/restore correctly, so
  the flaw is not a shared misunderstanding. **Ours.**
- **`` `e `` not being an escape in PowerShell 5.1.** `gplbld` scripts exist only
  in this port. **Ours.**
- **`CC ?= gcc` never firing in `gplsrc/sdclilib/Makefile`.** `sdb64` has no
  `gplsrc/sdclilib` at all - the client DLL came from `winsdclilib`. **Ours.**
- **`TERM LINUX` in `NEWVOC/LOGIN`.** Correct on Linux; only wrong here. Same
  reasoning as `CASE_INSENSITIVE_FILE_SYSTEM`. **Not a defect upstream.**
- **`PTERM` returning the new value rather than the previous one.** The stack
  diagram in `op_pterm()` documents exactly that, and a negative argument is the
  documented way to read without setting. **Behaviour, not a bug.**

**One thing left unexamined rather than cleared:** the installed `sdsys` holds an
empty directory literally named `C:`. Something builds a path where a bare file
name was expected. It is probably ours - a Windows path reaching code that wanted
a name - but nobody has traced it, so it is neither fixed nor reported.

---

## Correction: 18 Aug 2026 - piped answers DO work, and a working run was killed

**Commit:** this one. Twenty-first session. Corrects the §6 trap added in
`883b9a6`, "The fold is 'as typed, then upper'...", written the same day.

That entry claimed a confirming verb "reads the keyboard directly" so piped `Y`
lines "are **not** consumed as answers". **Both halves were wrong.** Measured
with a throwaway file: `DELETE.FILE sdtrap` with two `Y` lines behind it in the
pipe deletes the DATA portion, the DICT portion and the VOC entry, reporting
each. Surplus `Y` lines merely arrive at the prompt as unknown verbs.

**What is true** is that a prompt consumes **the next line in the pipe** whatever
it was meant to be — so `DELETE.FILE x` followed by `OFF` feeds `OFF` to the
prompt, loses the command, and then, the answer being neither Y nor N, re-asks
on an exhausted pipe for ever. §6 now says that instead.

**The mistake underneath it was procedural, and is the part worth keeping.** The
"it hangs" reading came from starting a background task, reading its output file
a second or two later, seeing only the command echo, and concluding a hang. The
second attempt - `Y Y Y OFF` - would have worked; it was killed while running.
Three `sd.exe` processes died that way and were then written up as evidence for
the wrong diagnosis. **Sampling an output file early is not observing a hang.**

Nothing was broken by it: the probe file and record were cleaned up either way,
and the BASIC-program route it recommends is still the cleanest for a record.

---

## 18 Aug 2026 - The default terminal type is VT100, not LINUX

**Commit:** this one. Twenty-first session. Owner's decision, following the
entry below, which found the VOC `LOGIN` paragraph and noted `TERM LINUX` on
its second line.

`NEWVOC/LOGIN` and `VOC_TEMPLATE/LOGIN` now say `TERM VT100`. It said
`TERM LINUX`, inherited from the Linux original, and `TERM` confirmed the
session device really was `linux` rather than that being a dead line.

**Checked before the edit, not after:** `vt100` is shipped in SD's own terminfo
(`terminfo/v/vt100`, installed), and `TERM VT100` on the 07:28:34 install
answered `Device : vt100` with no error and the page size intact.

**Edited byte-for-byte rather than with sed.** `TERM LINUX` and `TERM VT100`
are both 10 characters, so no record framing could shift - and the two files
are NOT identical: `NEWVOC/LOGIN` ends without a trailing newline and
`VOC_TEMPLATE/LOGIN` ends with one. A line-based rewrite risked normalising
that, and these are database records, not source files.

**An existing account keeps `linux` until its VOC is updated**, and then takes
the new value without asking: `update.voc` prompts only when the record TYPE
changes (`LOGIN:613`) and both old and new are `PA`, so `LOGIN:657` writes it
straight in. The release string moved in the same version, so every existing
account is offered the update at its next sign-in anyway.

**Not installed.** Source only; a cycle is owed.

---

## Correction: 18 Aug 2026 - the case inversion contradiction is resolved, and the setters are not dead

**Commit:** this one. Twenty-first session. Corrects the entry immediately
below, "Case inversion is off for real sessions; the contradiction is narrowed,
not closed", same day and same session.

**The VOC `LOGIN` PARAGRAPH turns it off.** `NEWVOC/LOGIN` is a `PA` record,
copied into every account VOC, and its fourth line is `PTERM CASE NOINVERT`.
`CPROC:397` runs it at session start and `CPROC:2701` runs it again on every
`LOGTO`. So `LOGIN:266` executes and does set the flag TRUE, exactly as its
source says; the paragraph runs afterwards and wins. Confirmed live with
`CT VOC LOGIN` against DON's own VOC.

**What the entry below got wrong:** it called the terminal half a "dead-setter
cleanup". The three C setters and `LOGIN:266` are not dead, they are
OVERRIDDEN, and removing them would be deleting working code that a shipped
configuration record happens to countermand. Nothing needs removing. The
authoritative place to change this behaviour is the paragraph, in
`NEWVOC/LOGIN` and `VOC_TEMPLATE/LOGIN`. Its conclusion still stands and is
now better founded: inversion off is DELIBERATE and shipped, which is what
§5.12 wants, so §7 step 8's terminal half needs no work at all.

**How it was cracked, after eight hypotheses had been eliminated by reading:**
by watching the ECHO instead of the flag. With inversion on, an upper-case
command comes back lower case. `PTERM CASE INVERT` then `LOGTO DON` echoed as
`logto don` - so the flag really was on and really did invert - and the command
after it echoed upper case again, while no banner appeared. That fixed the
reset inside `LOGTO` and ruled out `$LOGIN` re-running, which turned a
whole-session mystery into one grep for `pterm(` across `GPL.BP`. The eight
eliminated candidates were all about C and about `$LOGIN`; not one of them was
about a VOC record, which is where the answer was.

**Also noted:** line 2 of the same paragraph is `TERM LINUX`, and `TERM`
confirms the session device is `linux`. Not a fault - SD ships its own
terminfo and `sdsys/terminfo/l/linux` is installed - but it is a §5.16
Linux-ism in shipped configuration.

**No source changed**, so the 07:28:34 install stays current.

---

## 18 Aug 2026 - Case inversion is off for real sessions; the contradiction is narrowed, not closed

**Commit:** this one. Twenty-first session. On the 07:28:34 install.

§7 step 8 gated its terminal half on a contradiction: three places set
`case_inversion` TRUE, one of them `LOGIN:266` unconditionally, and yet
`SYSTEM(1001)` reads 0. It also named the thing to establish first - whether
that 0 is the reading for the sessions users actually get, in which case §5.12
is already satisfied and the work is removing dead setters.

**It is established, and by behaviour rather than by a flag.** Three readings
agree: `SYSTEM(1001)` = 0, `PTERM DISPLAY` says "Case inversion: Off" through a
different opcode, and - decisively - the `verify-osusers.ps1` probes send
`SH New-Item -ItemType File -Path C:\Users\dmont\...` and it reached PowerShell
with its case intact and created the marker. With inversion on that arrives as
`nEW-iTEM -iTEMtYPE fILE` and fails. An instrument can be wrong about a flag;
it cannot invent a file.

**So the terminal half is a cleanup, not a behaviour change.** SD accounts are
ssh-only, ssh gives SD piped stdin, and that is the path measured.

**The contradiction itself is NOT resolved, and that is the honest state.**
Eight candidates were eliminated so the next session does not re-walk them:
the two `PT$INVERT`/`PT_INVERT` constants (both 2), a missing include in LOGIN
(it has one), two copies of the variable (`Public` is `extern` outside `sd.c`),
the instrument (two opcodes plus behaviour), the early `return` at LOGIN:198
(that is the `mode = 2 or 3` path, and the banner at 209 proves it was not
taken), `@TRUE` being negative and so meaning "report only" (it is 1, measured),
the setter being broken (`PTERM CASE INVERT` works and sticks), and SET_PASSWD
resetting it at login (it is called from CREATEA and PS_SCRIPT, not LOGIN).

**Left to try:** whether `pterm(` at LOGIN:266 compiled to the opcode or bound
to the catalogued `$PTERM` verb, which parses `@sentence` and would ignore its
arguments; and a `display` beside line 266, which costs one cycle and answers
it outright. Staleness is ruled out - `gcat/$LOGIN` and `GPL.BP.OUT/LOGIN` are
both 6,160 bytes at 07:28.

**A separate defect found on the way, recorded and not fixed.** `op_pterm`'s
own stack diagram says it returns the NEW value and that a NEGATIVE argument is
what reports without setting. `SET_PASSWD:88` does
`was.inverted = pterm(PT$INVERT, @false)` - so it saves the "off" it has just
written, and the restore at line 98 can never put On back. Latent rather than
live, because inversion is off everywhere anyway. Ours, not upstream: the lines
carry a `14 Aug 26 Windows port` marker.

---

## 18 Aug 2026 - The release string is W1.0-0, and only the release string

**Commit:** this one. Twenty-first session. Owner's instruction.

`SD_REV_STAMP` / `SD.REV.STAMP` is `"W1.0-0"`. The W is for Windows; 1.0-1 and
1.0-2 were releases of SD this port was built from, not releases of the port.
Four files: `gplsrc/revstamp.h`, `gplsrc/sdclilib/revstamp.h`,
`sdsys/GPL.BP/REVSTAMP.H`, and the `$RELEASE` records in `NEWVOC` and
`VOC_TEMPLATE` - which must carry the same string, because `LOGIN:430` compares
them and a mismatch asks every user to update their VOC.

**Correction: the first attempt renumbered too much and was reverted whole.**
It also changed `BUILD` from 2 to 0 in all three headers and `AppVer` in
`gplbld/sd.iss`, on the reasoning that `revstamp.h`'s own comment block names
those as the places to keep in step. **That comment is about the openQM
lineage, which is not the SD release.** `MAJOR_REV`/`MINOR_REV`/`BUILD` stay
1/0/2 and `MESSAGES/0000` stays `2.6-6`; the SD release number is a DISPLAY
string, mainly the login header (`LOGIN:209`). Owner, 18 Aug 2026.

**`sd.iss`'s `AppVer` follows it**, asked rather than assumed, so the installer
becomes `sd-setup-W1.0-0.exe`. Safe alongside the old one: `cycle.ps1:212`
takes the NEWEST `sd-setup-*.exe` by write time, and a failed `ISCC` stops the
run before that line, so a leftover cannot be installed by accident.

**`W1.0-0` passes `MATCHFIELD(voc.rec<2>, "0X0A", 1)` unchanged**, checked
before the edit rather than after: `0X` consumes the leading letter. The
pattern is there to strip a TRAILING alphabetic suffix - measured on the same
run, `2.6-6a` comes back as `2.6-6`. A release string that started with a
letter was the one way this change could have broken every login.

**Built, not installed.** `make sd` exit 0; `bin/sd.exe --version` answers
`String Database (sd) Version W1.0-0 64 Bit`, and `SDTIC W1.0-0` appears in the
terminfo step. The client DLL includes `revstamp.h` but uses no symbol from it,
so the string is absent from `sdclilib.dll` by design, not by a stale build.

---

## 18 Aug 2026 - The OS.USERS admit path runs: a shell granted and taken back

**Commit:** this one. Twenty-first session. On the 07:00:00 install.

`gplbld/verify-osusers.ps1`, **18 of 18 checks, 13 of them decisive, exit 0**.
§7 step 7 is closed and the `changelog` entry that was held back for it is
written. §4 carries the table and what each row is for. `OS.USERS` was empty
again afterwards, the BP probe gone and no markers left, all checked directly
rather than taken from the script's own summary.

**The first run FAILED and the fault was the harness, not SD.** `New-ProbeCmd`
built the probe without its `SH ` prefix - the smoke test had added it in the
caller and the script did not - so every probe went in as a bare `New-Item`,
SD answered *"New-Item is not in your VOC"* (message 5051), no marker appeared,
and **six decisive checks failed without the gate under test ever being
reached**. It read exactly like a working boundary.

**That is the failure mode worth remembering: a probe that never arrives looks
identical to one that was refused.** Both leave no marker. `Test-ProbeRan` now
scans for 5051 on the probe command itself and stops with exit 2 - "the test
could not be run" - at all three places a probe is fired, including inside the
elevated half, which reports it back as `elev_reached`.

**Re-running cost no cycle, and would have cost one.** `assert-current.ps1`
watches all of `gplbld`, so editing the test would have demanded a reinstall to
re-run the test - the self-blocking trap already recorded against
`verify-tiers.ps1` on 17 Aug. `verify-osusers.ps1` joined `$neverShipped`
(`assert-current.ps1:88`), which is self-policing: a name quoted in `stage.py`
or `sd.iss` is put back under the guard.

**What the run established.** `@LOGNAME` is `don` in lower case, not
`$env:USERNAME` upcased, which is why the script asks SD for the record key.
An unelevated `OPENPATH` of `OS.USERS` succeeds although the file is (RX) to
`sdusers` - the one thing that could have made the design not work at all. The
two refusals carry different messages, 5240 for the metacharacter ban and 10053
for the gate, so an elevated session that is not listed still has the ban and
nothing regressed. And the shell goes away again when the record does, which is
what stops the whole thing being read into an install that admits everybody.

**Three more bugs in the script, all caught before the run rather than by it.**
A PowerShell function returns everything it writes, so the two helpers that both
printed and returned would have handed their caller an array with the printed
lines in front of the answer - `$rc -ne 0` on a string array; they report through
a script-scope variable now and have no return value at all. `Set-Content
-Encoding UTF8` writes a BOM on 5.1, which lands on the first line of the result
file the elevated half passes back and would have silently lost whichever key was
there. And the "already listed" gate trusted SD's read alone, which mattered
because the script REMOVES the record when it finishes: a pre-existing record -
somebody's real shell permission - would have been destroyed by a test. The
filesystem is asked as well now, `OS.USERS` being (RX) to `sdusers`.

**A defect found in the shared idiom and fixed only in the new script:**
`` `e `` is not an escape sequence in Windows PowerShell 5.1 - it arrived in
PowerShell 6 - so the ANSI strip that `verify-nocase.ps1` and `verify-tiers.ps1`
both carry has never removed an escape sequence. Measured: `TERM 200,9999` comes
back as `TERM<ESC>[7G200,9999` with the strip applied. `verify-osusers.ps1` uses
`[char]27`. The other two are untouched deliberately - the line is inert for
them, both match on substrings that no escape sequence sits inside, and changing
a passing verifier for a cosmetic gain was not worth the risk. §6.

---

## 17 Aug 2026 - OS.USERS: SH is permitted by a list, and ssh lands in SD

Twentieth session, commit f6eef22 and this one. Section 7 step 7, which this
file had held open as "owner's call" since 15 Aug 2026.

**The problem, which section 8 had already named.** CPROC's os.command gate
admitted only K$ADMINISTRATOR, which is IsElevated(), and an ssh session can
never be elevated - so programmers, the one group that needs a shell, were the
one group that could never have one, while OS.EXECUTE stayed ungated for
everyone. The visible control was denied to the people who needed it and the
capability it guards was open to those who did not.

**What was built.** @SDSYS/OS.USERS, a directory file, one record per account
keyed by account name: field 1 SH, field 2 OS.EX. Dictionary Name (D 0),
SH (D 1), OS.EX (D 2) plus @ID and an @ default listing, held as source in
gplbld/FILES_DICTS and written at bootstrap by WRITE_INSTALL_DICTS. Message
10053. Admin edits it with ED from SDSYS.

**Not in NEWVOC, and the owner was right to query it.** The tier lists live
there because CREATEA already has NEWVOC open (CREATEA:593); CPROC does not, so
the saving vanishes. Worse, everything in NEWVOC is copied into every account's
VOC unless excluded in TWO places, and the tier lists' fail-safe is PERMISSIVE -
a missing record means the FULL VOC. A permission list needs the opposite
default and must not inherit that convention. This was caught by being asked
"why is it in newvoc", after the design was already written.

**Both files must be staged, and that is not obvious.** WRITE_INSTALL_DICTS
OPENPATHs the dictionary rather than creating it, so an unstaged OS.USERS.DIC
means the entries are skipped with "ERROR OPENING FILE" and the file ships with
no dictionary at all.

**The ACL is the entire control**, and secure-osusers.ps1 grants sdusers (RX) -
read, not modify - which is the difference from secure-cred.ps1: CPROC reads the
list from the USER'S OWN process, so they must read it and must never write it.
Wired as SecureOsUsers in [Code] with the exit code checked. Verified on the
22:43:52 install: sdusers:(OI)(CI)(RX), no inherited entries, write raises
UnauthorizedAccessException, read succeeds. It worked on its first install,
which $CRED did not.

**Verified: the refusal.** `SH dir` as an unlisted don answers "don is not
permitted to use the operating system shell". **NOT verified: the admit path.**
OS.USERS is still empty, so SH has only ever been refused by the list and never
allowed by it. The changelog entry for OS.USERS is deliberately unwritten until
that is seen.

**Half the feature is missing and it is the half that makes it a boundary.**
Field 2 OS.EX is stored, dictionaried and read by nobody: OS.EXECUTE compiles
straight to OP.SH/OP.SHCAP into op_sh.c without touching CPROC, so gating it
needs C - two bits beside USR_ADMIN (sysseg.h, 0x0100 and 0x0200 free), a kernel
key gated on HDR_INTERNAL as K$ADMINISTRATOR is, LOGIN seeding them, a check in
sh(). Until then an unlisted programmer with BASIC still has full OS access from
a program, so OS.USERS is an auditable record and not yet a wall.

**SH implies OS.EX and cannot not**: CPROC runs the verb by calling os.execute.
The useful combination is OS.EX yes with SH no - programs may shell out, the
person at the prompt may not.

**Two build notes worth keeping.** Inno's Pascal Script has NO NESTED FUNCTIONS;
declaring one reports "'BEGIN' expected" at the inner declaration, which does not
name the cause. And pterm() cannot be called from a user account - internal only,
compiling as "Matrix PTERM is not referenced in a DIM statement" - so SYSTEM() is
the route to those values from a probe.

## 17 Aug 2026 - The ssh ForceCommand is applied, and scp is answered by pulling

Same session. allow-ssh-groups.ps1 -Installed was run elevated by the owner and
reported working; the config was then read here - marker block present,
AllowGroups over sdusers and Administrators, ForceCommand naming sd.exe,
sshd_config.before-sd kept, sshd Running. The ssh login itself was the owner's
test, not observed here: it needs a credential this session does not have.

**It stays GLOBAL rather than Match Group sdsshonly**, reaffirmed now that
OS.USERS exists. The group form would hand remote administrators a PowerShell
prompt, which is more than the global form gives them; and shell access is now
grantable per account, so nobody is stranded by forcing everyone into SD.

**The recorded cost - scp and sftp die machine-wide - is INBOUND ONLY, and that
is the whole of the answer.** ForceCommand applies where this machine is the ssh
SERVER. WinSCP or scp running ON this machine, connecting outward, makes it the
CLIENT and sshd_config is not consulted. So an administrator copies files by
PULLING them from a console or Remote Desktop session, both untouched because
administrators are never put in sdsshonly. Outbound is not firewalled: all three
profiles report DefaultOutboundAction NotConfigured, i.e. the Windows default of
Allow.

**Do not "fix" the scp cost with a Match Group administrators exemption without
reading 5.13.1.** Beyond giving admins a shell instead of SD, it may not even
work: sshd_config takes the FIRST obtained value for a keyword and
allow-ssh-groups.ps1 inserts its block BEFORE the first Match, so a later
ForceCommand none is not guaranteed to override the earlier global one. That was
left unresolved - sshd -T needs the host keys and refuses unelevated with "no
hostkeys available" - and it does not need resolving, because pulling avoids the
question.

**One consequence of the two changes together, worth stating plainly:** before
OS.USERS, ForceCommand closed the shell escape absolutely, because SH needed
elevation and ssh cannot elevate. It now makes the escape GRANTABLE - a listed
account lands in SD and can shell out from there. That is the intent, but it
means ssh confinement is now only as tight as OS.USERS is kept.

---

## 17 Aug 2026 - SYSTEM(91) said "not Windows", and that killed QPROC's case work

Twentieth session, commit f792a9d and this one. Verified on the 20:34:04
install, behaviour as well as flag.

op_sys.c case 91 - SYSTEM(91), "Windows?" - answered 0. On Windows. Inherited
from sdb64 where returning 0 is correct, so there is no upstream defect.

**What it broke.** QPROC:82 reads it into is.windows and QPROC:499 is

    if is.windows and is.dir then is.case.insensitive = @true

which is the ONLY route by which the query processor treats a directory file's
ids as case insensitive. FL$FLAGS cannot supply it - op_dio2.c:439 answers
FL_FLAGS only when (dynamic && internal), and a directory file is neither, so
QPROC:498 reads 0 for one however the flag is set. So SELECT against a
directory file has never matched an id typed in a different case, and the code
to make it match sat there unreachable.

**The same shape as the DHF_NOCASE entry below, one layer up.** Both were
correct code behind a switch that answered for the wrong platform: a macro
nobody defines in the C layer, a "not Windows" flag in the BASIC layer. Worth
remembering as a search: in a port, look for the platform predicates before
looking for missing code.

**Measured, treatment and control:**

    SELECT BP  WITH @ID = "sue"   directory file, record SUE  ->  1 record(s)
    SELECT VOC WITH @ID = "who"   dynamic file,   record WHO  ->  0 record(s)

The control is the point. A directory file matching across case proves nothing
on its own - everything matching would look identical. VOC is dynamic with
NOCASE off and stays case sensitive, so one matched and the other did not.

**Blast radius was checked before the change, not after.** The only other
reader of SYSTEM(91) is APISRVR:954, which is commented out, and
is.case.insensitive upper-cases both sides of a COMPARISON only (QPROC 4034,
4447, 7059, 7198), storing nothing - the same strategy taken at dh_open.c:529,
not the upper-casing 5.12 rejected.

**Two things the survey ruled OUT of step 8, recorded so they are not
rediscovered.** 707 upcase( calls in GPL.BP, most of which must stay: VOC verb
lookup, Y/N answers, record types - CPROC upcases verbs, which is why typing
listf finds LISTF. And the terminal half is blocked: case_inversion is XOR 0x20,
true inversion rather than force-upper, set in THREE places (linuxio.c:240,
linuxio.c:313, GPL.BP/LOGIN:266), yet SYSTEM(1001) reads 0 in a piped session,
contradicting all three. Read it from a real console or ssh session before
touching any of them.

**Incidental, and it cost a compile:** pterm() cannot be called from a user
account. It is internal-only and compiles as "Matrix PTERM is not referenced in
a DIM statement". SYSTEM() is the route to these values from a probe.

---

## 17 Aug 2026 - Step 8's file-name half: DHF_NOCASE on, upper-casing left off

Twentieth session, commits 0cc600f and 2b6aa92 plus this one. Verified on the
20:10:31 install.

CASE_INSENSITIVE_FILE_SYSTEM is referenced at 9 sites in this tree and defined
nowhere - and never defined in ../sdb64 either, so it is dead in both and there
is no upstream defect: on a case-sensitive Linux filesystem, off is correct.

**The 9 sites are two competing strategies, not one feature.** dh_open.c:529
makes the COMPARISON case insensitive by setting DHF_NOCASE on directory files.
The other 8 - dh_misc.c:143, op_dio2.c at 634, 726, 788, 916, 928, op_dio4.c at
1154 and 1285 - normalise paths and ids to UPPER case so that case-SENSITIVE
comparisons agree with the filesystem. Both solve the same problem and only one
can be right, so **defining the macro would have taken both**.

Took the comparison. Left the upper-casing off, because 5.12 chose lower case
and (b) is its opposite: user-visible (OS_CWD would answer C:\PROGRAMDATA\SD), and
worthless on Windows, where the filesystem already matches case-insensitively
without being asked. (b) is not internally consistent either - op_dio4.c:1155
guards on Option(OptSelectKeepCase) and op_dio4.c:1285 does not.

**Nothing is persisted.** Directory files have no header, so the flag lives only
in the shared FILE_ENTRY; dynamic files still take theirs from disk at
dh_open.c:549. No format change and nothing to migrate.

**Measured, with the control that makes it mean something:**

    before (17:36:21 install)   DIRFILE=0   DHFILE=0
    after  (20:10:31 install)   DIRFILE=1   DHFILE=0

BP is a directory file and VOC is dynamic. One moved and one did not, so the
flag is being read rather than invented.

**Correction inside the same session, worth keeping because it changed the cost
of the work by an order of magnitude.** Commit 0cc600f claimed the decisive
observable was a record lock on sue colliding with one on SUE, needing two
concurrent sessions and beyond any one-command script. That confused the change
with its consequence: op_lock.c has honoured DHF_NOCASE since long before the
port, so what this port changed is whether the flag is SET - and FILEINFO(f,
FL$NOCASE) answers that in one unelevated session. The lock collision remains
inferred from op_lock.c:996 rather than observed. The changelog states it plainly
because it is what a user needs to know; the caveat that it is an inference from
source lives in section 7 step 8, where the next session will look.

**The trick that made the test cheap:** BP is itself a directory file, so a
BASIC program is a file on disk. The probe was placed by writing it, not by
driving ED through a pipe. Reusable for anything else needing BASIC on an
installed system.

**gplbld/verify-nocase.ps1** wraps it, registered in assert-current.ps1's
$neverShipped. Unlike verify-credacl.ps1 two commits earlier, its glue was
exercised against a known state before shipping - the pre-change binary, where
it correctly produced FAIL with "installed sd.exe predates dh_open.c:529".

**A self-inflicted cost worth recording.** A source edit to sd.iss landed 33
seconds after a completed cycle, which voided taking any measurement from that
install - the trap CLAUDE.md names as editing source while a test is in flight.
Reverting does not help, because assert-current compares mtimes and a reverted
file is newer still. The fix is the prescribed order: finish every source
change, then one cycle, then measure. **Do not reason past the guard on the
grounds that the changed file was only the installer script** - that is the
ninth-session mistake the file forbids by name.

---

## 17 Aug 2026 - $CRED is verified closed, and the verify script had the same bug

Twentieth session, closing the entry below. Cycle run, install at 17:36:21,
`assert-current` clean. `gplbld/verify-credacl.ps1` unelevated as `GITORLI\don`,
exit 0:

    ordinary user can create a record in $CRED   expected no   observed no   PASS
    DACL is readable by an ordinary user         expected no   observed no   PASS

`icacls C:\ProgramData\SD\sdsys\$CRED` now answers *Access is denied* where the
17:08:32 install printed `GITORLI\sdusers:(I)(OI)(CI)(M)`. The decisive one is
the first row - `[System.IO.File]::Open(...CreateNew)` raising
`UnauthorizedAccessException` - because that is the escalation itself rather
than a reading of a listing.

**THE VERIFY SCRIPT FAILED ITS FIRST RUN, AND ON THE BUG IT WAS WRITTEN TO
CATCH ELSEWHERE.** `$acl = & icacls.exe $store 2>&1` sat under
`$ErrorActionPreference = 'Stop'`, so the *Access is denied* that proves the ACL
is right arrived as a terminating `NativeCommandError` and killed the script at
the moment it had its answer. Same defect as the missing `try`/`catch` in
`secure-cred.ps1`, written up at the top of that file in the same commit, one
file away.

Fixed by lowering EAP across that one call rather than wrapping it: here
*denied* is the healthy path and must be read and scored, not caught and turned
into a failure.

**Worth keeping as a rule:** in this codebase, `2>&1` on a native command under
`Stop` is a trap every time, and the right handling depends on whether stderr
means failure. `secure-cred.ps1` catches it, because for that script any stderr
from `icacls` is a failure. `verify-credacl.ps1` reads it, because for that one
stderr is the expected result.

**Also confirmed here:** `verify-credacl.ps1` was edited after the install and
`assert-current` still reported clean, which is the `$neverShipped` registration
in `assert-current.ps1` doing its job - without it the script would have refused
itself, the trap that list already records `verify-tiers.ps1` hitting.

---

## 17 Aug 2026 - Why secure-cred.ps1 did not take: -File does not strip quotes

Twentieth session. Answers the entry below, which measured the open ACL but
left the cause as two candidates. It is candidate (a), and it was measured
rather than reasoned to.

`sd.iss` passed the store as `-Path '{#DataDir}\sdsys\$CRED'` - single quoted -
to `powershell.exe -File`. **`-File` does not run its arguments through the
expression parser**, so it neither expands variables nor strips quotes, and
`$Path` arrived as `'C:\ProgramData\SD\sdsys\$CRED'` with the quotes as part
of the value. `Test-Path` said no, `secure-cred.ps1` exited 2 with
"does not exist - nothing secured" - which was true - and the `[Run]` entry
discarded the exit code. Every visible sign said the install had worked.

Measured by driving `powershell.exe` from a batch file, so the command line
arrives as raw as Inno's does, against a probe script that printed its own
argument and its length:

    -File    -Path '...\sdsys\$CRED'   ->  ['...\sdsys\$CRED']  151 chars
    -File    -Path "...\sdsys\$CRED"   ->  [...\sdsys\$CRED]    149 chars
    -Command -Path "...\sdsys\$CRED"   ->  [...\sdsys\]         144 chars
    -Command -Path '...\sdsys\$CRED'   ->  [...\sdsys\$CRED]    149 chars

**The comment in `sd.iss` that mandated the single quotes was reasoning about
`-Command`.** It said double quotes would expand `$CRED` and silently leave
`-Path` as `...\sdsys\`. Row 3 shows that is exactly right - for `-Command`.
The entry used `-File`, where row 2 shows double quotes are correct and safe.
The author reasoned correctly about the wrong parser, and rows 3 and 4 are why
the belief was reasonable rather than careless.

**The fix PROJECT_STATUS proposed last session was also wrong.** It suggested
escaping the `$` with a backtick; `-File` delivers the backtick literally too,
so that would have failed the same way with a different wrong path. The fix is
plain doubled double-quotes, like every other script argument in the file.

**Candidate (b), ordering against the data-tree `icacls`, was never the cause.**
The `icacls` was already ahead of it in `[Run]`.

**The control that made this cheap:** on the same broken install, `icacls` on
`audit`, `sd-elevate.log` and `PSTMP` all answered *Access is denied*
unelevated, because their `/inheritance:r` had run and removed `sdusers`
entirely. `$CRED` was the only one of the four that would still print its ACL.
Three siblings locked, one not, and the only difference between the four call
sites was the quoting on that one line.

**What changed.** The `[Run]` entry became `SecureCredStore` in `[Code]`, called
at `ssPostInstall` ahead of `AdoptAccount`, double quoted, **with the exit code
checked** and a failure named in the closing `MsgBox`. A `[Run]` entry cannot
check an exit code - this file already records the same mistake being made
about the OpenSSH entry - and the rationale for not checking, copied from
`secure-audit.ps1`, does not carry: a missed audit ACL leaves an editable
trail, a missed credential ACL leaves an escalation open.

`secure-cred.ps1` also gained the `try`/`catch` the other three `secure-*.ps1`
have. It was the only one without, and under `$ErrorActionPreference='Stop'`
the `2>&1` on the `icacls` call turns any stderr line into a terminating
`NativeCommandError` - which, uncaught in a script the installer runs hidden,
exits with no message anyone would see.

**`gplbld/verify-credacl.ps1` is new**, and is the part that stops this
recurring: nothing checked any of these four ACLs, which is why it shipped
broken and stayed broken for a session. It **refuses to run elevated** - the
ACL grants `Administrators` Full, so an elevated run passes however broken the
ACL is - and its decisive check is a write into `$CRED` rather than a reading
of the listing. It is registered in `assert-current.ps1`'s `$neverShipped`
list; without that it would have refused itself, the trap that list already
records `verify-tiers.ps1` hitting.

**Cost:** no install. The whole diagnosis was unelevated, from a batch file and
a four-line probe script.

**What is NOT done: none of it has been observed on an install.** `ISCC`
compiles the changed `sd.iss` clean, `[Code]` section included, and
`secure-cred.ps1` was run against a stand-in store and produced exactly two
ACEs. One cycle is owed. Until then `verify-credacl.ps1` refuses, correctly,
because source is newer than the install.

**Also fixed here, unrelated and one character:** PROJECT_STATUS.md carried
`gplbld\verify-apiport.ps1` with the `\v` replaced by a literal vertical tab
(0x0B), inside a code block offered as a command to run. An earlier session's
Python edit had eaten it as an escape. Same trap bit twice more this session
while writing these files, both times caught by scanning the result for control
characters - worth doing after any scripted edit to these documents.

---

## 17 Aug 2026 - Correction: secure-cred.ps1 did not take, and $CRED is open

From `62b4740`, and it corrects the entry below within the same session. The
API was verified working and `$CRED` was reported as locked to SYSTEM and
Administrators. **The lock did not apply.** Measured unelevated on the
17:08:32 install:

    icacls C:\ProgramData\SD\sdsys\$CRED
      GITORLI\sdusers:(I)(OI)(CI)(M)
      BUILTIN\Administrators:(I)(OI)(CI)(F)
      NT AUTHORITY\SYSTEM:(I)(OI)(CI)(F)

`(I)` is inherited: the data tree's Modify for every SD user, which is exactly
what secure-cred.ps1 was written to remove. So the escalation stands - an SD
user can overwrite another account's Argon2 verifier with one derived from a
password they choose and authenticate through the API as that account - and the
API working is what makes it reachable rather than theoretical.

**It was nearly signed off.** The verify-apiport run passed every check it
makes, and none of them looks at the ACL; the ACL was checked only because
listing $CRED as an unelevated user succeeded when it should not have. **A
harness that asserts what it set out to prove and not what it changed will do
this again** - the run asserted the port was on loopback, and never asked
whether the store it protects was protected.

**Why it did not run is NOT established.** Two candidates, the first favoured:
the `-Path '...'` single quoting added to stop PowerShell expanding `$CRED` may
arrive at the script with the quotes still attached, because Inno builds a raw
command line and `powershell.exe -File` does not strip single quotes the way
the PowerShell language does - `Test-Path` then fails and the script exits 2
silently, since the installer deliberately does not check its exit code. Or the
entry runs before the data-tree icacls and inheritance re-applies.

**A reproduction attempt was inconclusive and is recorded so it is not
repeated:** running the script by hand UNELEVATED fails with `icacls: Access is
denied`, because changing a DACL needs more than the Modify sdusers holds. That
says nothing about the elevated install-time path.

**Cheapest next step:** run it elevated with the installer's literal argument
form, printing `$Path` before `Test-Path`. If the quoting is the cause, escape
the `$` for PowerShell rather than quoting the path - and check the exit code,
because a credential store left wide open must not be a silent step.

---

## 17 Aug 2026 - The API works: section 7 step 6 closed

From `01d2c2b`. `gplbld/verify-apiport.ps1 -Prefix sdapi2`, all checks passed,
17:09. The front door section 1 names is open.

    right password  ->  admitted, WHO -> 1 SDAPI2
    WRONG password  ->  refused: Invalid username or password
    SDSYS           ->  refused: User not allowed in requested account

**THE WRONG-PASSWORD LINE IS THE ONE THAT MATTERS.** It is the first time
`!CRED_VERIFY` has executed in this project at all: SDConnectLocal sends no
password, so step 6a had been built, compiled and never run since 17 Aug
morning, and every earlier "evidence for 6c" came from a path that never
reached the credential check.

**And the two refusals carry DIFFERENT messages, which is the evidence rather
than a detail.** `sysmsg(5017)` is the credential check rejecting the password;
`sysmsg(10003)` is the group test refusing the account. A single catch-all
refusal would have proved only that something said no, and would have been
equally consistent with a transport that rejects everything.

**What this closes.** Step 6a ($CRED instead of /etc/shadow), 6b (@logname from
the verified identity rather than the client's assertion), 6c (the ACC$GROUP
grant check) and 6d (login_user deleted) are all now run rather than merely
built - and with them the remote transport itself: the listener in sdwind, the
per-connection fork+exec, and PF_INET re-enabled in start_connection().

**Asserted in the same run:** the listener is bound to 127.0.0.1 and NOT to
0.0.0.0, which is posture B holding in practice and not just in the design; and
the harness put everything back - port closed, Windows account removed, sd.conf
restored from its backup.

**The road here, for anyone reading back:** a native listener handing the
socket to an MSYS2 child could not work (measured, with a control), so the
listener went into sdwind on the Cygwin side; the client half never needed
touching because SDConnect has always been TCP; SET.PASSWORD had no VOC entry;
and $CRED had never been created by anything. Four separate stoppers, each of
which looked like the last one until it was measured.

---

## 17 Aug 2026 - $CRED was never created, so SET.PASSWORD never worked

From `fa3dccb`. Running the API harness found a defect in the product rather
than in the harness, and an old one: the credential store has never existed on
any install.

    :SET.PASSWORD SDAPI1
    Cannot open the $CRED register.  Has the install completed?

**Nothing creates it.** `sd -i` creates VOC, VOC.DIC, ACCOUNTS.DIC, $MAP and
DICT.DIC and no more; `CRED_SET` opens `$CRED` and returns ER$NVR if it is not
there; `stage.py` listed it among the files "the bootstrap and the running
system create for themselves", which was simply wrong. So SET.PASSWORD has
failed on every install ever built, and nobody saw it: section 5.6 took
passwords off the console login and left the credential machinery callerless,
and no VOC pointed at SET.PASSWORD until the morning of 17 Aug 2026. The API
could not authenticate anybody because no account could hold a credential.

**Now staged as a directory file and locked to SYSTEM and Administrators.**
Owner's ruling. `gplbld/secure-cred.ps1` runs from the installer after the
data-tree icacls - the same ordering `secure-audit.ps1` needs, or inheritance
puts the tree's Modify straight back.

**THE RISK IS WRITING, NOT READING, and the distinction matters.** `$CRED`
holds a per-account salt and an ARGON2 VERIFIER, never a password
(`INT$KEYS.H:263`). Reading a verifier is worth little. But the data tree
grants sdusers Modify - measured on `$MAP`, which is what `$CRED` would have
inherited - so any SD user could have OVERWRITTEN another account's verifier
with one derived from a password they chose, then authenticated through the API
as that account. That is the escalation the ACL closes. sdusers get nothing at
all here, which is the difference from the audit trail, where they keep
append-only so SD can write it as the user.

**THE FILE SHAPE IS NOT A CONTROL.** Directory file or dynamic file, the same
bytes are equally readable to anyone with access - `VOC` and `$MAP` are dynamic
and their `%0` is plainly greppable. The ACL is the whole of the protection,
and choosing dynamic would have bought obscurity while feeling like security.

**THE SERVICE ACCOUNT IS WHAT MAKES THE TIGHT ACL WORKABLE, and it was checked
rather than assumed:** `Win32_Service` reports `StartName = LocalSystem`, so
sdwind forks `sd -n -q` children that read `$CRED` as SYSTEM and the API path
is unaffected. An elevated administrator running SET.PASSWORD is unaffected. An
ordinary console user cannot read it, deliberately - which is consistent with
SET.PASSWORD being an administration verb, and carries a corollary worth
knowing before somebody tries it: copying SET.PASSWORD into a user's VOC will
not work at the file layer until section 5.7's service model lands. The program
permits it; the ACL does not.

**And the API gate has no elevation bypass**, which was worth checking once it
was clear API sessions run as SYSTEM: `APISRVR:449` tests the VERIFIED USERNAME
from `kernel(K$USERNAME,0)` against the account's group, not the process token,
so SDSYS stays refused however privileged the process is. That is precisely why
step 6c insisted the identity come from K$USERNAME.

**A trap in the installer entry, which would have failed silently.** The path
is single quoted, unlike every other entry in sd.iss, because PowerShell
EXPANDS `$CRED` inside a double-quoted string. Undefined, so `-Path` would have
become the sdsys directory itself and the credential store would have been left
wide open with the step reporting success.

**Verified by staging, not by reading:** a cold `stage.py --force` into a
scratch tree puts `$CRED` in the staged data tree and `secure-cred.ps1` in
ProgramFiles. Not installed - a cycle is owed.

---

## 17 Aug 2026 - The API test harness: one command, and three cells

From `054ef11`. `SET.PASSWORD` verified on the 16:28:43 install first -
`verify-tiers.ps1 -Prefix sdtierc` passed every check with `COUNT VOC` 421 on
the derived figure, and reading the account VOCs as bytes, independently of the
script's own `LIST VOC`, put `SET.PASSWORD` in the ADMINISTRATOR account and in
neither of the others.

**Then the harness the remote transport has been waiting for.**
`gplbld/verify-apiport.ps1` is one elevated command: it creates a throwaway
account, sets a GENERATED password on it, adds APIPORT to the installed
sd.conf, restarts SD, asserts what is listening, drives a client session, and
puts all of it back in a finally block so a failure part way still restores.

**The password is generated, never hardcoded, and never on a command line.** It
reaches SD on stdin, which is section 5.6.1's rule - a command line is readable
through Task Manager, Win32_Process and ETW. A throwaway account rather than a
real one, because setting a password on somebody's account to run a test leaves
a credential behind that nobody asked for.

**THREE CELLS, AND THE WRONG-PASSWORD ONE HAS NO PRECEDENT HERE.**
`tests/remote_connect_test.c` checks that the right password is admitted, that
a WRONG password is refused, and that SDSYS is refused whatever the password.
The middle cell is the first thing in this project that can ever reach
`!CRED_VERIFY`: `SDConnectLocal` sends no password at all, so step 6a has never
been executed by anything. If a wrong password is admitted, the other two
results are worthless and APILOGIN=0 is the first thing to suspect.

**TWO DEFECTS FOUND BY RUNNING IT RATHER THAN READING IT**, both in the harness
and both worth the run:

- Unescaped backslashes in a diagnostic string - three compiler warnings, and
  the message printed as "C:ProgramDataSDsd.conf".
- `APIHOST` passed through from the top-level Makefile as an EMPTY value, which
  **overrides a `?=` default rather than leaving it alone**. The test was handed
  an empty host and answered "Invalid host name", which reads as a broken
  listener rather than a makefile mistake. Defaulted at both levels now.

**And verify-apiport.ps1 had to join assert-current's neverShipped list**, or it
would refuse to run because of its own existence - exactly the trap that list
was added for on 17 Aug when verify-tiers.ps1 blocked itself.

**Not run.** A cycle is owed for the test source and the sdclilib Makefile;
neither ships, but `gplsrc` is a watched tree and the guard is deliberately
blunt. `make sd` is not needed.

---

## 17 Aug 2026 - SET.PASSWORD becomes the tenth administration verb

From `e0d9d4d`. The API could not admit anybody, and the reason was not the
transport: `APILOGIN=1` makes `APISRVR` call `!CRED_VERIFY`, and NO ACCOUNT
COULD BE GIVEN A PASSWORD. `GPL.BP/SET_ACC_PASSWORD` existed, compiled, and was
catalogued as `$SET.PASSWORD` - it is in `gcat` on every install - and **no VOC
anywhere pointed at it**, so there was no way to type the command.

**Owner's ruling: it is an administrator verb.** *"The administrator can always
remove it from the exclusion list if they want users to set their own."* So it
joins the nine in `NEWVOC/TIER.ADD.ADMINISTRATOR`, making ten, with a
`VOC_TEMPLATE/SET.PASSWORD` record of `V` / `CA` / `$SET.PASSWORD`.

**THE PROGRAM WAS NOT GATED, AND MUST NOT BE.** It already tells the two cases
apart: `SET_ACC_PASSWORD:69` refuses somebody else's account without
administrator rights, and `:109` demands the current password for your own. So
an administrator who copies the verb into a user's VOC gets precisely the
behaviour the ruling describes - that user can change their own password and
nobody else's. A wholesale `K$ADMINISTRATOR` gate, which is what the other nine
carry, would have made that copy do nothing, and would have quietly inverted
the decision into "only administrators, ever".

**ADMINISTRATOR `COUNT VOC` moves 420 to 421.** Standard and programmer are
unchanged, the verb living in `VOC_TEMPLATE` alone.

**AND THE VERIFY SCRIPT HAD A HOLE THAT THIS VERY EDIT WOULD HAVE FALLEN
THROUGH.** `verify-tiers.ps1` cross-checked `$Withheld` against the shipped
`TIER.OMIT.STANDARD` - its comment says why, "a test that carries its own stale
copy of the thing under test is no test" - and did NOT do the same for
`$AdminVerbs` against `TIER.ADD.ADMINISTRATOR`. Updating the record and not the
test, or the other way about, would have passed silently. It went unnoticed
while the add list never changed; the first change to it is what exposed it.
Both lists are cross-checked now, and the hardcoded 18s and 9s are `.Count` of
the lists themselves.

**Not installed.** A cycle is owed for two data records and the BASIC comment
changes; `make sd` is not needed, no C changed. After it, `SET.PASSWORD` is
what makes the first real API login possible.

---

## 17 Aug 2026 - The remote transport is built: APIPORT, and a listener in sdwind

From `7fe6f38`. Option A, built after the measurement in the entry below killed
option B. **Compiles clean and has never run** - a cycle is owed, and this one
is real C.

**What it is.** `sdwind` - the one process SD already keeps running - now
binds a loopback socket, and forks and execs `sd -n -q` per connection with
the socket on descriptors 0 and 1. That is exactly the contract
`etc/xinetd.d/qmclient` describes and `start_connection()` reads; Windows has
neither xinetd nor systemd socket activation, so the half the operating system
supplies on Linux is now ours.

**APIPORT, and it defaults to OFF.** New parameter, `struct CONFIG` into
`SYSSEG`, readable as `CONFIG('APIPORT')`. It is in the segment rather than
`PCFG` because `sdwind` is what reads it and loads no per-process config.
Zero means no listener - which is what the `memset` already gives - and there
is deliberately no fallback to 4243: opening a port every local process can
reach is an act, not a side effect of installing. The socket is bound to
`INADDR_LOOPBACK` and that is **not** configurable, because posture B says
nothing of SD's own faces the network and a bind address in a conf file is a
way to get that wrong by accident.

**`start_connection()` accepts `PF_INET` again, reversing upstream's Feb 2024
narrowing to AF_UNIX.** The identity that narrowing bought - `getpeereid()`,
the kernel naming the local user - has no Windows equivalent, measured: native
sshd cannot see an MSYS2 AF_UNIX socket at all. So the identity moved rather
than being lost: `$CRED` establishes it (step 6a) and the `ACC$GROUP` test
confirms the account (step 6c). `peer_usr_id` and `peer_grp_id` are left
UNASSIGNED rather than filled in with something plausible, so nothing
downstream can mistake a TCP peer for an authenticated OS user.

**Three things found while building it:**

- **The commented-out upstream `PF_INET` block could never have compiled.** It
  names `MAX_IP_ADDR_STR_LEN`, which is defined nowhere in the tree; the
  buffer is `MAX_SOCKET_ADDR_STR_LEN`. Enabling it verbatim would not have
  built, which is worth knowing before anyone tries the same in `sdb64`.
- **The daemon's minute timer had to move off the iteration count and onto the
  clock.** `select()` returns as soon as a connection arrives, so the old
  `timer++` per pass would have run `check_lost_users()` once per API
  connection instead of once every five minutes.
- **Children are reaped in the loop rather than by a `SIGCHLD` handler**, because
  `SIG_IGN` auto-reaps and would then make `system()` in `check_lost_users()`
  fail with `ECHILD`.

**The client half needed no work at all** - `SDConnect()` has always opened an
AF_INET socket - and `sdclilib.dll` is byte-identical at `8D1517D1CD2B83AB`.
`sd.exe` is now `55AAB5890E80733D` and `sdwind.exe` `6A4006E91EC6431E`, built
after `rm -f gplobj/*.o`, which was required rather than tidy: `config.h` and
`sysseg.h` both changed and the Makefile tracks no header dependencies.

**THE SHARED SEGMENT LAYOUT CHANGED** and `SYSSEG_REVSTAMP` does not catch it -
the same trap as the `PCFG` change of 16 Aug 2026. Harmless across a real
install; fatal if one rebuilt binary is copied onto a running system.

**What it still lacks is a RUN, and the cycle alone will not give one**,
because a fresh install opens no port. Testing it needs `APIPORT=4243` added
to the installed `sd.conf` and SD restarted - `read_config()` runs only when
the segment is created - and then a client driven through `SDConnect()`, which
is the only path that reaches step 6a's `$CRED` check at all.

---

## 17 Aug 2026 - The remote transport: a native listener cannot hand a socket to an MSYS2 child

From `7fe6f38`. No source changed; this is a measurement taken before building,
at the repository owner's instruction to settle the question rather than pick by
elimination.

**THE QUESTION.** Section 7 step 6a/6b needs a listener and a per-connection
spawn, which Windows has no xinetd for. The attractive option was a NATIVE
listener - it keeps the traffic off a loopback TCP port that any local process
can reach - passing the accepted `SOCKET` to the MSYS2 `sd.exe` as its standard
input, exactly as step 11's working local transport passes pipes.

**IT CANNOT WORK.** The Cygwin child agrees the descriptor is a socket and can
write to it, and cannot read a byte of it:

| stdin | pending pre-spawn | getsockname(0) | send(0) | select() | read |
|---|---|---|---|---|---|
| pipe (CONTROL) | - | FAIL ENOTSOCK | FAIL | 0 | - |
| pipe (CONTROL) | - | FAIL ENOTSOCK | FAIL | **1** | **OK** |
| SOCKET | 0 bytes | OK AF_INET | OK | 0 | EAGAIN |
| SOCKET | **13 bytes** | OK AF_INET | OK | **0** | **EAGAIN** |

The parent proves with `ioctlsocket(FIONREAD)` that the bytes are pending
**before the child exists**, so "the child saw nothing" cannot be "nothing was
sent". The control is the same descriptor number in a separate run: swap the
socket for a pipe and the payload arrives.

**THE HARNESS WAS WRONG TWICE AND THE CONTROL CAUGHT BOTH, which is the
reusable part.** First it sent only *after* spawning the child, so it measured
a channel nobody had written to yet - and the pipe, which step 11 proved
honest, reported "no data" alongside the socket. Then it used `hStdError` as
the control channel, which is an OUTPUT handle, so Cygwin builds fd 2
write-only and a read-select on it can never fire. **Neither wrong answer
could have survived a control, and neither would have been visible without
one.** A third slip was of the kind this project keeps recording: a run taken
from a binary older than its source, because a `cmd /c` build had silently not
happened - the same "date what you are testing" failure as the install trees.

**Why it fails.** A socket is not passed between processes by handle
inheritance; Windows documents `WSADuplicateSocket()` for that. The handle is
real enough for `getsockname` and `send`, which go straight to the kernel
object, but the receive path stays bound to the originating process's Winsock
context. And the `WSADuplicateSocket` route would need the rebuilt socket
injected into Cygwin's descriptor table - `cygwin_attach_handle_to_fd()`, the
always-ready path step 11 already measured and rejected. Both routes are shut
by measurement rather than by argument.

**What it leaves.** The listener belongs on the Cygwin side, where `sdwind`
already lives: MSYS2, already persistent, able to `accept()` and fork+exec
`sd -n -q` with the socket on descriptor 0 exactly as xinetd does on Linux.
That needs `start_connection()`'s `PF_INET` branch, which returns FALSE today -
upstream narrowed it to AF_UNIX in Feb 2024, and the peer identity that bought
(`getpeereid`) is precisely what step 6a replaced with `$CRED`.

**Also established while reading, and it shrinks the step:** the CLIENT half
needs no work at all. `SDConnect()` already does `socket(AF_INET, SOCK_STREAM)`
and `connect()`. And the retained `etc/xinetd.d/` files are pre-2024
archaeology - they say `protocol = tcp` on 4243, which the current
`start_connection()` would refuse.

**Not built, and nothing in the repository changed**, so the 13:43:00 install
stays current and no cycle is owed. The probe is in a session scratchpad and
will be lost: `sockprobe_parent.c` (native UCRT64, `-lws2_32`) and
`sockprobe_child.c` (MSYS2). Land them beside step 11's `select_probe_*.c` with
the next change that owes a cycle anyway.

---

## 17 Aug 2026 - The owed cycle ran, and the cycle script failed a good install

From `d7cc7a7`. The harness-only cycle the previous entry owed, run. **Nothing
was wrong with SD**: install 13:43:00, `assert-current` exit 0, `sd.exe`
`81D0856F5493385E` and `sdclilib.dll` `8D1517D1CD2B83AB` unchanged, tree whole -
`gcat` 132, `GPL.BP.OUT` 193, `$BCOMP` 87,992, `$CPROC` 25,208 - and
`make check-local` passes on the installed pair, `WHO -> 2 DON` with `SDSYS`
refused. Step 11 stays closed and step 6c's evidence now reproduces on a third
install.

**A FOURTH HARNESS DEFECT, AND IT IS THE MIRROR OF THE FIRST THREE.** Where
defect 1 printed a wrong number as a result, this one **failed an install that
was fine**. `cycle.ps1` step 8 stopped at 13:36:30 with `no
C:\ProgramData\SD\sdsys\gcat after the install - it did not complete`; the
install completed normally at 13:43 and every catalogue figure was correct.

**Cause: `& $setup.FullName` does not wait.** PowerShell's call operator returns
immediately for a GUI-subsystem process, and Setup.exe is one - PE subsystem
**2**, read off `sd-setup-1.0-2.exe` rather than assumed. The 300-second count
deadline therefore started when the **wizard opened** rather than when it was
dismissed. Five minutes spent reading the closing dialog was indistinguishable
from an install that never ran - and the non-silent default exists precisely to
ask the operator to read those pages (PROJECT_STATUS section 7 step 3), so the
defect was aimed at its own intended use. Fixed with `Start-Process -Wait`, the
count deadline kept as the backstop in case Inno ever respawns itself for
elevation.

**Why it matters as much as a false pass:** the symptom is identical to the
broken-bootstrap install of 16 Aug 2026, which is the one failure this script
exists to catch, and the natural response is to spend another cycle
investigating a tree that is already correct.

**The file count is not the check, and this run is the second time that has
mattered.** The tree measured **3,473** files against the **3,483** recorded on
the 12:28:49 install, with nothing missing: the difference is whether SD is
running, since the live segment and the logs sit inside `sdsys`. A file-by-file
comparison of the stage against the install came back empty, `audit` and
`ACCOUNTS/DON` being the only extras. PROJECT_STATUS section 7 step 2 still says
to count files.

**No cycle is owed for the fix.** `cycle.ps1` is in `assert-current`'s
`$neverShipped` list, so editing it cannot make the installed tree differ from
source - the self-policing exclusion added earlier the same day, working as
intended.

---

## 17 Aug 2026 - The cycle: step 11 verified on a real install, and three harness defects

From `a1849b7`. The cycle the previous entry owed, run - and it found nothing
wrong with SD and three things wrong with the tooling around it.

**Step 11 is closed.** `assert-current` exit 0 against the 12:28:49 install
(`sd.exe` `81D0856F5493385E`, `sdclilib.dll` `8D1517D1CD2B83AB`), tree whole -
`gcat` 132, `GPL.BP.OUT` 193, `$BCOMP` 87,992, `$CPROC` 25,208, 3,483 files -
and `make check-local` passes on the INSTALLED pair: `DON` admitted with
`WHO -> 2 DON`, `SDSYS` refused. **That refusal is the first verified evidence
for step 6c**, the `ACC$GROUP` grant check. `ACCOUNTS/DON` field 5 reads
`ADMINISTRATOR` on this install too, so the tier work came through the cycle
intact.

**THE FIRST DEFECT IS THE ONE WORTH REMEMBERING, BECAUSE IT PRINTED A WRONG
NUMBER AS A RESULT.** `cycle.ps1` step 8 reported `GPL.BP.OUT 5` on an install
that was fine and finished with 193. It waited for `gcat\$CPROC` to exist and
then counted, and `$CPROC` is nowhere near the last file written, so it measured
a half-copied tree. **A number read off a tree that is still being written is
the exact failure step 3 exists to catch** - and here the script was doing it
itself and presenting the answer. It now waits for the installed counts to reach
the STAGED ones, which are known because they were measured minutes earlier, and
fails if they never do. Reported against the stage rather than a remembered
constant, so it stays true when the counts legitimately change.

It was caught only by not believing it: `assert-current` exited 0, the script
said CYCLE COMPLETE, and the tree was in fact perfect. The tell was that the
install had finished two seconds before the transcript ended, which is far too
fast for 3,483 files.

**`CC ?= gcc` in `gplsrc/sdclilib/Makefile` had never fired.** `?=` means "if
UNDEFINED", and GNU make's built-in `CC` has origin `default`, which is defined -
so `CC` stayed `cc`. The DLL escaped it because the top-level Makefile passes
`CC=` explicitly; `make check-local` did not, so it compiled a NATIVE UCRT64
test with the MSYS2 compiler.

**And `make check-local` had no PATH to run with**, answering `Error 127` -
which reads as a broken transport, one commit after a transport was fixed. A
plain MSYS2 login shell has neither the installed bin, which the loader is
*meant* to fall through to, nor `System32`, which a native binary needs to
resolve `api-ms-win-crt-*.dll`. The failure names an api-ms-win-crt DLL and so
reads as a broken toolchain rather than a search path. **`make check-local` now
runs from `sd64`**, where it gets the right compiler, and the target puts both
directories on PATH for the run. The instruction in section 7 step 11 said to
run it from `gplsrc/sdclilib`, and that is corrected in both places.

---

## 17 Aug 2026 - Step 11 works: SDConnectLocal carries a session, and step 6c has its first evidence

From `dc1e021`. The transport of the previous entry, built.

`local_connect_test` exits 0, four runs, unelevated: `SDConnectLocal("DON")` is
admitted and `WHO` answers `19 DON`; `SDConnectLocal("SDSYS")` is refused with
"User not allowed in requested account". **The refusal is the important half.**
It is the `ACC$GROUP` grant check in `APISRVR` - section 7 step 6c, built on
17 Aug and never run until now - and `DON` succeeding on its own would have been
equally consistent with a check that never executed. Two earlier attempts
elsewhere in this project proved nothing for exactly that reason.

No orphaned `sd.exe` survives a run, which is the EOF path working: closing our
copies of the child's ends is what lets the child see its stdin close and exit.

**What changed is all client-side except one refusal.** `SDConnectLocal()` makes
two anonymous pipes and hands them to the child as its standard handles;
`session[].hPipe` became `hPipeRd`/`hPipeWr`, an anonymous pipe being one-way.
The command line is `-Q -C1!0`, and the ORDER matters: `sd.c` parses
`-C<tx>!<rx>` and answers with `dup2(RxPipe, 0); dup2(TxPipe, 1)`, so rx is 0
and tx is 1. The previous entry and PROJECT_STATUS both said `-C0!1`, which
would have crossed the streams - caught by reading the parse rather than by
running it, and it is the kind of thing that would have read as "the transport
still does not work".

**Inheritance is restricted to exactly two handles** with
`PROC_THREAD_ATTRIBUTE_HANDLE_LIST`, not left as plain `bInheritHandles = TRUE`.
This library loads into somebody else's application, and that flag inherits
EVERY inheritable handle the process owns - a file or socket handle the host
happens to hold would be copied into a long-lived `sd.exe` and kept alive for
the whole session with nothing to show why. The pattern was validated in the
probe before being written into the library, and the probe confirmed it took
effect in a way worth recording: the child's attached descriptor number dropped
from 4 to 3, one fewer handle having been inherited.

**`sd.c`'s `-C <pipename>` branch now refuses with a diagnostic instead of
hanging.** The code behind it is correct and the flaw is not in it, so
`win32pipe.c` stays; but a path that leaves the server alive, silent and never
answering is the worst thing to leave callable, and it had already cost one
session's diagnosis.

**What this measurement is and is not.** A development smoke test: the new
`sdclilib.dll` paired in a scratch directory with the INSTALLED `sd.exe`, which
the DLL finds beside itself through `GetModuleFileName`. That is the pair that
matters, since the server needed no change - but `assert-current` is stale, a
cycle is owed, and `make check-local` after it is the authoritative run.

---

## 17 Aug 2026 - Step 11: the transport choice was between three options, not two

From `7dee1a6`. No SD change; a probe, a measurement and a correction to how the
question was posed.

The handoff put the local-transport decision to the owner as two options: give
`CN_PIPE` its own `ReadFile`/`PeekNamedPipe` I/O, or move to a loopback socket
and give up the peer identity that chose the named pipe. He asked which to
recommend, and reading the code to answer showed the question had a false
premise.

**THE PEER IDENTITY NEVER CAME FROM THE PIPE.** There is no
`ImpersonateNamedPipeClient` and no `GetNamedPipeClientProcessId` anywhere in
`gplsrc`. `SDConnectLocal()` gets identity because it spawns `sd.exe` with
`CreateProcessA`: the server is a child running under the caller's own token, so
`GetUserNameA()` and `IsElevated()` inside it report the calling user. The pipe
only carries bytes. That makes the socket option's stated cost illusory - and
the named pipe's stated benefit illusory with it.

**So the real question was never identity, it was which transport Cygwin's
select() handles honestly** - and there is a third answer. Hand the child
inherited pipe handles as its STANDARD handles, and Cygwin builds descriptors 0
and 1 itself at startup, sees `FILE_TYPE_PIPE`, and installs its pipe handler,
whose `select()` is `PeekNamedPipe`-based.

**Measured rather than argued**, with the control in the same process and the
same run - one native UCRT64 parent, one MSYS2 child, both descriptors put
through the same `select()` milliseconds apart:

```
inherited(fd 0)  empty=0  data=1     <- honest
attached(fd 4)   empty=1  data=1     <- always ready: the stopper, reproduced
inherited read: [HELLO-INHERITED]    <- and usable, not merely honest
```

Identical on four runs. `empty=0` is the whole finding: always-ready is a
property of injecting a RAW HANDLE through `cygwin_attach_handle_to_fd()`, not
of pipes. Reproducing the bad case beside the good one in a single binary is
what makes it evidence rather than a hopeful reading.

**The evidence was partly already in hand and had been walked past all day.**
Every `Invoke-SD` in this session piped from PowerShell - a native parent - into
`sd.exe`, a Cygwin child, and SD read each command, blocked properly and exited
at EOF. That is the proposed mechanism minus the return path, exercised a dozen
times while the transport was written up as blocked.

**It needs nothing in the server.** `sd.c:441` already accepts `-C<tx>!<rx>` and
does `dup2(RxPipe, 0); dup2(TxPipe, 1);`, so with the handles arriving on 0 and
1, `-C0!1` is a no-op `dup2` that only sets `CN_PIPE`. The change is client-side
and removes code. The comment at that line already said the descriptor form was
"what a Unix parent doing fork-then-exec with inherited descriptors would still
send"; it was kept for a caller nobody could survey, and turns out to be the
shape the Windows client wants too.

**The harness is in the repository this time** -
`gplsrc/sdclilib/tests/select_probe_{child,parent}.c` and
`make check-select-probe` - because the previous step 11 probe was built outside
it and the handoff had to say "worth rebuilding if this is picked up again". It
needs both toolchains in one target, which nothing else here does, and the
UCRT64 `bin` must be on PATH or `gcc` exits 1 having printed nothing at all: the
driver finds its own `cc1.exe` but `cc1` cannot load its DLLs.

**Still unchecked before code is written:** how `-Q` / `is_sdApiSrvr` behaves
with stdin and stdout as the protocol channel rather than a terminal.

---

## 17 Aug 2026 - Section 8: the ADMINISTRATOR tier, and the hole that made the tiers temporary

From `9cb2095`. Still uncompiled - a cycle is owed and now carries three
commits.

**Owner's rulings, 17 Aug 2026, all three given in one exchange:**
"administrators get the whole voc"; the four verbs left owed a ruling
(`MODIFY`, `COMPILE.DICT`, `GENERATE`, `PHANTOM`) are "all should be programmer
and above"; and the tier is to be recorded rather than left as a create-time
decision.

**The administrator ruling was never a no-op.** The nine administration verbs -
`CREATE.ACCOUNT`, `DELETE.ACCOUNT`, `MODIFY.ACCOUNT`, `UPDATE.ACCOUNT`,
`GRANT`, `REVOKE`, `LIST.GRANTS`, `UNLOCK`, `ENCRYPT.FIELD` - live in
`VOC_TEMPLATE` and never in `NEWVOC`, and `CREATEA` copies every account's VOC
from `NEWVOC`. So an SD administrator had to `LOGTO SDSYS` to administer
anything. The owner's justification checked out for seven of the nine: the
programs gate themselves on `K$ADMINISTRATOR`. `UPDATE.ACCOUNT` does not - it
is `CPROC` internal verb 15 - and `ENCRYPT.FIELD` points at `$CRYPTO`, which is
not in this tree at all. Both are on the list anyway, and PROJECT_STATUS
section 8 says so.

**They are read out of `VOC_TEMPLATE`, not moved into `NEWVOC`**, because the
fallbacks only point the safe way while `NEWVOC` holds nothing administrative.
A lost omit list means "no policy" and gives the full VOC; with
`CREATE.ACCOUNT` in `NEWVOC`, one missing record would hand every account SD
creates the power to make more.

**THE FINDING, and it came out of checking the owner's gating claim rather than
out of looking for it.** `UPDATE.ACCOUNT` is ungated, and it calls
`$LOGIN(,2)`, which is `LOGIN`'s `update.voc` - and that routine re-copied the
whole of `NEWVOC` with no tier filter. It hands a standard account back
`BASIC`, `CATALOG`, `RUN`, `ED`, `SED`, `COPY` and `DELETE.CATALOG`. Worse, the
same routine is reached from an **ordinary login**: if the account's `$RELEASE`
level differs from `SD.REV.STAMP`, any user is asked "Update VOC to new
release?" and `Y` restores everything. No privilege, no verb. **So the tiers
built the day before survived exactly until the next release stamp moved.**

The fix needed the tier persisted, which nothing did. `ACC$TIER` is `ACCOUNTS`
field 5 - the first use of the "start at field 5" that the `ACC$USERS` removal
note reserved on 15 Aug, field 4 being poisoned by records written between 13
and 14 Aug. A blank field means the full VOC: it can only occur on an account
created before this change, which already holds one.

**A regression the tier work would have shipped, caught on the way past.**
`ADOPT` takes no tier keyword and `adopt-account.ps1` passes none, so the
installing user's own account - `don`'s - would have come out STANDARD, with no
`BASIC`, no `ED` and no `CATALOG`. It would have read as "SD is broken after
installing it". `ADOPT` now defaults to the administrator tier; an explicit
keyword still wins.

**Correction to the previous entry.** That entry recorded avoiding `CONTINUE`
in `CREATEA` because "its behaviour inside `LOOP ... REPEAT` is not
demonstrated anywhere here". It is demonstrated - in `LOGIN`, inside
`update.voc` itself, where a declined type change skips the write. `LOGIN` uses
`CONTINUE`; `CREATEA` keeps its flag, and the wrong comment is left standing
there rather than corrected by a second uncompiled change.

**Cost:** one alias again, found by reading records rather than names - `CD` is
`Verb to compile dictionaries|CA|$CD`, the same program as `COMPILE.DICT`, so
omitting one without the other would have voided the ruling. That is the second
time in two sessions.

**Still open:** the 30/45/65 split of the 149 verbs, and everything below it in
section 8 - the tiers remain enforced by the user's own Windows token until
per-account ACLs exist.

**And the cycle became one command, `gplbld/cycle.ps1`.** Owner's instruction,
17 Aug 2026: "this is many more steps than in the past using 2 or 3 different
types of shells. In the past they were all powershell and fewer steps." He was
right, and the hand-run sequence had just failed twice in one attempt, both
times on something a script cannot get wrong:

- **The SD service was still running.** The staged `etc/fstab` points
  `/dev/shm` at the live tree, so the bootstrap's `sd -start` collided with the
  live server and `sd -i` produced nothing. The staged tree was left in the
  seed state - `gcat` 4 entries, `$BCOMP` 70,697, `$CPROC` 0 bytes, no `VOC` -
  which is exactly the state that shipped a catalogue-less install on 16 Aug.
  **Nothing of the tier work was compiled**, so that attempt tested nothing.
- **`ISCC` was run from `C:\WINDOWS\system32`**, where the relative
  `gplbld\sd.iss` does not resolve. Inno answers "The system cannot find the
  path specified" without naming the file it could not find - and that error
  is the only reason the broken staging tree was not packaged into an
  installer.

The script stops the service and waits for `sdwind` to go, derives every path
from its own location, re-checks the staged tree before building anything, and
refuses unelevated *before* the seed phase rewrites the staging tree rather
than after, which is where `bootstrap.py` checks. CLAUDE.md's testing section
now points at it and says not to hand-run the steps.

**One thing it deliberately does not do:** kill a surviving `sd` process. It
names what is still running and stops, because a live `sd` is somebody's
session.

**Correction, same day: the stray installer was never in `system32`.** This
entry and PROJECT_STATUS both said `C:\WINDOWS\system32\193`, because that is
what ISCC printed. The owner went to delete it and there was no such directory.
It was in **`C:\WINDOWS\SysWOW64\193`**: `C:\Program Files (x86)\Inno Setup 6\`
is a **32-bit** binary, and WOW64 silently redirects a 32-bit process's writes
to `system32` into `SysWOW64`. **ISCC reports the path it was asked for, not the
one it got**, so any path handed to it is subject to that rewrite - though only
`system32` is redirected, and only a relative path resolved against an elevated
shell's default directory lands there at all. Both directories are gone now.

**And its first run found a bug in itself, of exactly the class it was written
to prevent.** The wholeness check used `$out` for the `GPL.BP.OUT` count, and
**PowerShell variable names are case-insensitive**, so it overwrote the `$Out`
PARAMETER with the number 193. ISCC was handed `/O193` and wrote the installer
into a relative `193\` directory under the shell's cwd -
`C:\WINDOWS\system32\193\sd-setup-1.0-2.exe`. The check caught it, but reported
`no sd-setup-*.exe is in 193`, which names the symptom and not the cause. Every
local in that block is prefixed now, and `-Stage` and `-Out` are both required
to be rooted and are resolved absolute up front - a relative path there fails
not by breaking but by working somewhere nobody will look, which is the same
fault as the `ISCC` invocation the script replaced.

**That run also spent the risk this session was carrying:** the staged tree came
out whole - `gcat` **132**, `GPL.BP.OUT` **193**, `$BCOMP` **87,992**, `$CPROC`
**25,208** - so `SECOND.COMPILE` ran `BASIC GPL.BP *` over the changed `CREATEA`
and `LOGIN` without an error, and `bootstrap.py` dies on any. **The tier work
compiles.**

**AND THE ADMINISTRATOR TIER HAS RUN**, on the 10:34 install that the fixed
script produced, `assert-current` exit 0. Measured without elevation, by
reading the installed tree: `ACCOUNTS/DON` field 5 reads `ADMINISTRATOR` with
field 4 empty, so `ACC$TIER` is written, the poisoned field was skipped, and the
`ADOPT` default fired on the install's own account. DON's VOC holds all nine
administration verbs - checked by their unique PROGRAM names, `$CREATEA`,
`$DELACC`, `$MODIFYA`, `$GRANTA`, `$UNLOCK`, `$CRYPTO`, because `GRANT` is a
substring of `LIST.GRANTS` - all eighteen withheld ids, and neither `TIER.*`
list record.

**`COUNT VOC` answered 420, which is the derived figure exactly**: installed
`NEWVOC` holds 410 names, less `%t` (a dynamic-file artefact rather than a
record) and the two list records leaves 407 copied, plus the nine, plus
`CREATEA`'s own four. Deriving it first and measuring second is what makes it
evidence; 420 observed and then rationalised would not have been.

**Along the way, an item that had stood open in the PROJECT_STATUS header for
two sessions closed for free: an unelevated interactive session works.** `WHO`
answers `2 DON`. The header called it a tooling limit and pointed at section 6;
it was not one. Piping `"\n<commands>\nOFF\n"` into `sd.exe` from PowerShell
drives an ordinary session, the blank first line absorbing the BOM exactly as
`verify-createaccount.ps1` had been doing since 14 Aug.

**And `assert-current.ps1` had to stop counting the test scripts, having blocked
one.** `verify-tiers.ps1` was written after the 10:33:57 install; the first
thing it does is call `assert-current`, which then refused **because of
`verify-tiers.ps1`** - a verification script blocking itself over a file that
can never enter an install. The advice it printed made it worse: it named
`stage.py --force --bootstrap` and the steps after it, so following it meant
hand-running the sequence `cycle.ps1` exists to replace, against a machine whose
SD service was still up. That is the run that died on `sd -start` reporting
"Semaphores are already present" - `sd -stop` shut the daemon down and the
semaphores outlived it - and left the staged tree in the seed state.

The exclusion uses the rule `localtest\` and `__pycache__` already use: a file
neither compiled into `sd.exe` nor staged into the install cannot make the
installed tree differ from source. **It is self-policing**, because an exclusion
list is exactly the thing that rots into a false "current": each name is checked
against `stage.py` and `sd.iss`, and one that appears there is watched again.
The first version of that check matched the bare name and instantly reinstated
`assert-current.ps1`, because `stage.py:268` discusses it in a **comment** - so
it now requires the name to be quoted or path-prefixed, the way a ship list
names a file rather than the way prose mentions one. Verified both directions:
`deny-logon.ps1`, `adopt-account.ps1`, `install-service.ps1` and
`sd-elevate.ps1` are all still detected as shipping.

**ALL THREE TIERS THEN RAN AND PASSED**, 17 Aug 2026 11:31:38,
`gplbld/verify-tiers.ps1 -Keep -Prefix sdtierb`, 22 of 22. `COUNT VOC` landed on
every derived figure exactly - **393** standard, **411** programmer, **420**
administrator - and the withheld/administration split came out 0/18 and 0/9 for
standard, 18/18 and **0/9** for programmer, 18/18 and 9/9 for administrator.
The programmer row is the one that carries meaning: the eighteen present and the
nine absent is the only control on the add list, and a copy loop that omitted
nothing would pass the other two rows. `UPDATE.ACCOUNT` in the standard account
left it at 393 with all eighteen still missing - before `ACC$TIER` it restored
every one.

**Confirmed twice, by two instruments.** The script asks SD; the same numbers
were then re-derived by reading the account VOCs as raw bytes and matching the
on-disk record framing, `\0\0\0` + id + type letter, learned by dumping DON's
`%0`. That framing matters because a naive substring search cannot answer this
at all - `ED` occurs inside half the file, and `GRANT` inside `LIST.GRANTS`.

**A verifier that erases its own evidence is not a verifier, and the first run
was one.** It cleaned up by default, and the VOCs live in the account
directories it deleted - so it left three `ACCOUNTS` records, nothing to count,
and a PASS/FAIL table that existed only in a console window nobody would paste
back. It now writes a transcript to `C:\ProgramData\SD\verify\` with the verdict
line written BEFORE the transcript closes, and it detects an `ACCOUNTS` record
left by an earlier run and asks for a fresh `-Prefix`, rather than letting
`CREATE.ACCOUNT` refuse the name several steps later for a reason that reads
like a tier fault.

---

## 17 Aug 2026 - Section 8: the PROGRAMMER tier, built and uncompiled

From `ecd62b2`. Session ended here on credits; this is the handoff.

`CREATE.ACCOUNT ... PROGRAMMER` gives the full VOC, `ADMINISTRATOR` implies it,
and a plain account now gets NEWVOC less the thirteen ids in
`NEWVOC/TIER.OMIT.STANDARD`. Before this every account got a byte-identical VOC
whatever keyword was given - the mechanical root of section 8's "enforced
backwards".

**Owner ruled nine verbs; four exact aliases had to follow or the ruling would
have been void** - `CATALOGUE` and `CATALOG` are both `$CATALOG`,
`DELETE.CATALOGUE` and `DELETE.CATALOG` are both `$DELCAT`, `EDIT` and `ED` are
both `$ED`, and `COPYP` is Pick-style `COPY`. Reading the records is what found
them; the names alone would not have.

**Two constructs were deliberately avoided in the BASIC**, because none of it
compiles until the next bootstrap and a novel statement that does not mean what
it does elsewhere costs a whole cycle: `delete(rec, 1)` (that function appears
nowhere in GPL.BP, and SDCLIENT defines a *subroutine* of the same name) and
`CONTINUE` (BCOMP lists it, but its behaviour inside LOOP...REPEAT is
demonstrated nowhere here, and a skip that did not skip would copy everything
and look like success). A `copy.it` flag and a `for` loop from field 2 say the
same thing in constructs the file already uses.

**Left for the owner:** `MODIFY` is a record editor and the most likely thing
to undo the rest; `COMPILE.DICT` and `GENERATE` are dictionary compilers;
`PHANTOM` runs catalogued programs. None added - extending a ruling is not
applying it. And the 30/45/65 split of the 149 verbs is untouched.

## 17 Aug 2026 - Section 8, first increment: MICRO and the language verbs are out

From `35b3b87`. Owner picked the three-tier VOC work over the transport when
asked. This is the part he had already ruled on and which needs no tier
machinery, done first so it lands on its own.

**Removed from both VOCs:** `MICRO` (an external editor, so a containment
escape of the same class as `SH`), `NLS`, `SET.LANGUAGE`, `LOAD.LANGUAGE`.
`VOC_TEMPLATE` 434 -> 430, `NEWVOC` 411 -> 408.

**The four programs are KEPT and are now callerless**, which is the precedent
`$CRED` set. Checked before removing: nothing anywhere calls `$MICRO`, `$NLS`,
`$SETLANG` or `$LOADLANG`, and `K$SET.LANGUAGE` in `INT$KEYS.H` is kernel key
38 - a different thing with a confusingly similar name, left alone.

**Two things the inventory corrected.**

**The decision space is 149 verbs, not the 144 section 8 recorded.** That count
matched the literal string `V` in field 1 and missed five records whose type
field is descriptive text starting with V. SD reads the FIRST CHARACTER
(`voc.rec[1,1]`, `CPROC:3376`), so "Verb to compile SDBasic program" is a V and
"Remote item to list files" is an R. `NEWVOC` carries descriptions where
`VOC_TEMPLATE` carries bare letters, and `CREATEA:530` normalises them down on
the way into a new account - which is why both forms work and why counting the
literal letter undercounts.

**And section 8's finding is now counted rather than asserted.** Only **24
records** separate `VOC_TEMPLATE` from `NEWVOC`, and every one is account
administration or a file pointer - `CREATE.ACCOUNT`, `GRANT`, the `*.COMPILE`
verbs, `GPL.BP`, `MESSAGES` and so on. **A standard account still gets `BASIC`,
`CATALOG`, `RUN`, `ED`, `SED`, `COPY`, `SH`, `!` and `DELETE.CATALOG`.** So the
gap between the two tiers that exist is administration, not capability, exactly
as section 8 said - and now with a number on it.

**Not built yet:** the `PROGRAMMER` keyword beside `ADMINISTRATOR`
(`CREATEA:610`) and a way for the copy loop (`CREATEA:520`) to skip what a tier
does not get. An omit-list held as data beats a second and third `NEWVOC`
directory: three directories drift, and the reduced VOC is meant to be a
starting posture a site curates.

## 17 Aug 2026 - Step 11 does not work: a Cygwin fd from a raw HANDLE is always "ready"

Corrects and supersedes the entry below, which said step 11's cause was "found
and fixed". The access-argument fix was real and is kept; it was not the whole
story, and the rest is not fixable by tweaking flags.

**With the fix in, `sd.exe` stopped exiting and started HANGING** - progress,
and the next symptom. `strace` on it, serving a real pipe, loops forever:

```
dtable::select_read: //./pipe/SDProbePipe5 fd 0
select: sel.always_ready 1
set_bits: ready 1
read: 1 = read(0, 0x…, 1)
```

**`sel.always_ready 1`.** A descriptor built by `cygwin_attach_handle_to_fd()`
from a raw Windows HANDLE has no real `select` support, so the runtime reports
it readable unconditionally. SD asks exactly that question before every read
(`linuxio.c:535`, `:383`, `:456`), so it spins one byte at a time, never
blocks, never frames a packet and never replies. The client waits for a
response that cannot come.

**This also corrects a diagnosis in the entry below.** That said `poll()`
"reports readable" while `read()` gives EBADF, as though poll were working and
disagreeing. **Poll was never working** - it answers ready unconditionally,
which is why it said ready in the EBADF case too. Same observation, wrong
conclusion, because the earlier probe never tested poll against an EMPTY pipe.

**Three defects were still found and fixed on the way, and all three stand:**
the `-C` argument mismatch (also in `sdb64`, UPSTREAM_FIXES.md #4), `sd.exe`
being looked for inside the data tree, and the access argument having to match
how the HANDLE was opened.

**TWO TOOLS DID THE WORK AND NEITHER WAS AN INSTALL CYCLE.** A standalone probe
- twenty lines of C, MSYS2 gcc, a PowerShell harness playing the pipe server -
settled the access argument by trying six combinations. Then **`strace`, which
is in MSYS2 at `/c/msys64/usr/bin/strace.exe` and works on `sd.exe`**, answered
in one run what three cycles could not: the failing path prints nothing, exits
nothing, and lies through `poll()`. There is no `gdb` in this install.

**What is left is a design decision, recorded in section 7 step 11:** give
`CN_PIPE` its own `ReadFile`/`PeekNamedPipe` I/O instead of borrowing
descriptors 0 and 1, which keeps the peer identity a named pipe was chosen for;
or move to a loopback socket, where Cygwin's select works and `CN_SOCKET` is
already exercised, and authenticate some other way.

## 17 Aug 2026 - Step 11 ran and failed; poll() said the descriptor was fine and read() said EBADF

From `4a92f19`, after the cycle that produced the 07:20:40 install.

**Step 6c compiled.** `gcat/$APISRVR` 9,323 bytes against 9,129 after 6a - the
second consecutive first-compile that passed. 6c still has no run.

**Step 11 ran and failed:** `SDConnectLocal("DON")` answered `Connection closed
by server`. What made it expensive is that **every diagnostic short of the read
said the system was healthy**:

- the named pipe CONNECTED, so `win32_attach_client_pipe` had opened it;
- `sd.exe` exited **0** - not a crash, not `exit(1)`;
- **both its streams were empty**;
- and inside it, `poll()` reported the descriptor **readable, `POLLIN` set**.

**The fault: `cygwin_attach_handle_to_fd()`'s access argument must match how
the HANDLE was opened, not describe what the descriptor is for.** The handle is
`CreateFile`d `GENERIC_READ | GENERIC_WRITE`; attaching descriptor 0 with
`GENERIC_READ` - the obvious thing to write - **succeeds and returns 0**, and
the descriptor then fails `read()` with `EBADF`. SD polls before reading
(`linuxio.c:535`), passed the poll, failed the read, took the connection-lost
branch and exited silently.

**The prediction recorded in step 11 was wrong**, and worth noting because it
was confidently written: it said the likely fault was the call not honouring a
requested descriptor number. It honours it exactly.

**HOW IT WAS FOUND, AND THIS IS THE PART TO REUSE.** A standalone probe -
twenty lines of C compiled with MSYS2 gcc outside the repository, driven by a
PowerShell harness acting as the pipe server - tried six combinations of the
name and access arguments against a real pipe with real data waiting. **It
needed no install cycle.** Three cycles would not have found this: the failing
path prints nothing, exits 0, and lies through `poll()`. When the unknown is
one library call, isolate the call.

Also fixed: `make check-local` built the test beside the build tree's
`sdclilib.dll`, which has no `sd.exe` next to it, so the test would have loaded
the wrong pair. It builds into `localtest/` now, where the loader falls through
to PATH and the installed pair.

**The fix is unverified in place** - the probe proves the mechanism, not the
integration - and a cycle is owed to try it.

## 17 Aug 2026 - Section 7 step 11: SDConnectLocal could never have worked, and now might

From `c7c15f7`. Owner chose the smaller of three scopes when asked: fix
`SDConnectLocal`, leave the remote transport alone.

**Three independent faults, none of them subtle once the two sides were read
against each other.** The client library launches `sd.exe -Q -C <pipe name>`
with the name as a SEPARATE argument; `sd.c` parsed `sscanf(argv[arg],
"-C%d!%d", ...)` and `exit(1)`ed otherwise, so `argv[arg]` was exactly `"-C"`,
matched nothing, and the child died during argument parsing. **The same
mismatch is in `sdb64` byte for byte** - UPSTREAM_FIXES.md #4. The client also
looked for `sd.exe` at `<sysdir>\bin\sd.exe`, inside the DATA tree, where the
pcode file lives. And the path it built was unquoted, under `C:\Program
Files`, which `CreateProcessA` with a NULL application name resolves by trying
`C:\Program.exe` first.

**`gplsrc/win32pipe.c` is new and is the third `windows.h` file**, after
`win32sem.c` and `win32audit.c`. The pipe is a native object made by the UCRT64
client and `sd.exe` is MSYS2, so `open()` cannot reach it - the Cygwin runtime
does not map `\\.\pipe\` names. `CreateFile` plus
`cygwin_attach_handle_to_fd()`, which `msys-2.0.dll` exports at ordinal 379,
puts it on descriptors 0 and 1 so the whole terminal and packet layer above is
untouched.

**AN HOUR WENT INTO THE WRONG FILE FIRST.** `gplsrc/sdclient.c` looks exactly
like the client and is **excluded from the build** - `Makefile:66`,
`SRCS := $(TEMPSRCS:sdclient.c=)`. The shipping client is
`gplsrc/sdclilib/sdclilib.c`, and its `sysdir()` had already been corrected on
14 Aug, so one of the "faults" found in the dead file did not exist in the live
one. **Check what the Makefile builds before reading a file as authoritative.**

**Two things the compiler caught that reading had not.** `win32pipe.c` first
included `sd.h`, which reaches `linuxlb.h`, which declares `GetUserNameA()` and
`Sleep()` with types that conflict with the real Windows ones - the reason the
other two `win32*.c` files include only `windows.h` and their own header, and
why this returns `int` rather than `bool`. And `GetModuleHandleEx(FROM_ADDRESS)`
given a function address is a function-pointer-to-object-pointer conversion,
which `-Wpedantic` reports; the address of a static datum does the same job.

**The vendored library's own docs were wrong.** Both `README.md` and
`USER_GUIDE.md` said the Windows DLL does not provide `SDConnectLocal` and that
it is "Linux-specific". It is exported at ordinal 6, checked with `objdump -p`,
and its transport is a named pipe, which has no Linux equivalent in that
library at all. Corrected in place.

**A claim in PROJECT_STATUS was too strong and is narrowed:** "the transport
blocks step 6" is true of 6a and 6b, which live in `vb.login`, and **false of
6c**, which lives in `vb.account` and is reachable from a local session.
`vb.local.login` authenticates nothing by design - the process owner is the
identity - so a local client is the cheapest route to the first evidence step 6
has ever had.

**Evidence: `make sd` clean and warning-free, both toolchains, 07:06.** That is
all. Nothing has called any of it. The first thing likely to be wrong is
whether `cygwin_attach_handle_to_fd()` honours a requested descriptor number or
allocates the lowest free one.

## 17 Aug 2026 - Section 7 step 6c: the API applies the grant check

From `c1d2183`. Step 6 is now built in full and none of 6c has been through a
compiler; the next `stage.py --bootstrap` is its first, as the last one was
6a's.

**What went in.** `APISRVR`'s `vb.account` tests membership of the Windows
group named in the account's `ACC$GROUP`, which is the rule CPROC's
`logto.authorised` applies at LOGTO. Until now an API session that
authenticated could switch to **any** account by name: the check existed before
the port and was lost in it, because it tested a Linux group, and it could not
be restored until step 6a gave the API a credential model.

**Three things were decided rather than defaulted**, and the block comment in
the file carries the reasoning: the identity tested is `kernel(K$USERNAME,0)`
rather than the local `logname`, so the grant check and the audit trail can
never disagree about who acted; an account with an empty `ACC$GROUP` is refused
rather than having `sdu_<name>` guessed for it, which is step 5a's rule; and
the refusal reuses `sysmsg(10003)`, the missing-account message, so the API
cannot be used to enumerate accounts. SDSYS is refused through the API as a
consequence, which is intended - administration needs elevation and an API
session cannot have it.

**A wrong claim was caught before it was committed, and it produced a section 6
trap worth more than the code.** The first draft of both the comment and the
step argued that copying `logto.authorised` verbatim would be dangerous because
`K$INTERNAL` is permanently true inside `APISRVR`, the program being
`$internal`. **They are two different flags.** `$internal` is `HDR_INTERNAL` in
the program header; `K$INTERNAL` reads `internal_mode`, a session flag set only
by `sd -internal` or `sd -I`, both behind `check_admin()`. An API session has
the first and not the second, so that gate is permanently SHUT, not open. Both
flags are live in that one file, which is where it will be misread again.
Checking what set the flag took one grep and reversed the conclusion.

## Correction: 17 Aug 2026 - "sd -stop left the daemon running" was wrong; sd -stop never ran

Corrects the entry below, *Seventeenth session: the owed cycle ran, and step 6a's
BASIC compiles*, and the PROJECT_STATUS.md section 6 trap it produced. Same
session, an hour later, `06bc63f` already pushed.

**The claim was that a cleanup script ran `sd -stop | Out-Null`, that the daemon
survived it, and that the explanation had been discarded with the output.**
`sd -stop` was never reached. The script hung in its *start* helper, several
steps earlier.

**What it actually is:** `Start-Process -Wait` with `-RedirectStandardOutput`
never returns from `sd -start`, because `sd -start` forks `sdwind` and the
daemon inherits the redirect handles and holds them for its whole life.
PowerShell waits for streams that will never close. **The command succeeds and
the script hangs anyway.** Section 6 has it, with the recovery and with the two
working ways to start SD from a script.

**How it was caught, and it was available the first time.** The run wrote
`stopA-start.out`, **29 bytes**, `SD (64 Bit) has been started` - so the step
that appeared to be hanging had in fact completed. `sd.exe` was gone and
`sdwind.exe` pid 13188 was alive with a **dead parent**. Reading the output
files in order, rather than reasoning from "the daemon is still up", gives the
answer immediately.

**Why the wrong version was believable, which is the part worth keeping.** A
surviving `sdwind` really is the signature of the known `sd -stop` EPERM defect
(section 6, 14 Aug), the script really did contain an `| Out-Null`, and the
project's own documentation had just been extended with a trap about discarding
output. Three true things pointed at a conclusion that was not tested against
the one cheap question: *had the script reached that line at all?* **A
plausible mechanism is not evidence that the mechanism fired.**

**Nothing here implicates SD.** `stop_sd()` is not under suspicion, no
diagnostic of it is owed, and the section 7 items are unaffected. Both hangs
this session were the harness.

## 17 Aug 2026 - Seventeenth session: the owed cycle ran, and step 6a's BASIC compiles

From `b6758aa`. No source changed this session, deliberately — the whole point
was to run the cycle the entry below left owed, and a source edit would have
voided it. `assert-current` still exits 0 on the resulting install, so the next
session can measure before it edits.

**Install of 17 Aug 06:07:30.** `gcat` 132, `GPL.BP.OUT` 193, `$BCOMP` 87,992,
`sd.exe` `201A9902D4323765`. A file-list comparison of the staged tree against
the install came back **empty in the "staged but not installed" direction** —
the 11 extras are install-time artefacts only (`ACCOUNTS/DON`, `audit`,
`sdsvc.log`, `sd-elevate.log`, `adopt-account.log`, the live segment, `don`'s
account directories). That comparison is a better check than counting files,
which is what §7 step 2 asks for, and costs the same.

**The result that mattered: `APISRVR` compiled.** `SECOND.COMPILE` during this
bootstrap was the first compiler of any kind to see the step 6a BASIC, and
`bootstrap.py` dies on any error or `is not assigned a value` warning.
`gcat/$APISRVR` **9,129 bytes / md5 `84f7d949…`** against **9,056 /
`49c28f05…`** in the previous stage — changed, so it is genuinely the new
source, and it passed. The previous handoff named this as the single most
likely place to break. It did not break. **What it does at run time is still
entirely unverified** and blocked on the transport, not on this.

**§7 step 1a closed with its control.** `NOSUCHPARAM=1` → exit 1,
`Unrecognised configuration parameter 'NOSUCHPARAM=1'`; `CREATUSR=1` → exit 0,
`SD (64 Bit) has been started`. Two earlier attempts at this proved nothing
because only a segment *creation* reaches `read_config()`, and a treatment
that starts is also what a parser reached by nobody would do.

**What it cost, and both are in §6 rather than here.** An ordinary SD session
cannot be read without a console — three wrong ways, each failing differently,
and `sd WHO` being refused unelevated is the gate working rather than a broken
install. And a cleanup script that ran `sd -stop | Out-Null` threw away the one
message explaining why the daemon survived, then blocked in `Start-Service`
waiting on a service that could not start over a live segment. **That is the
existing "stdout-only harness is blind" trap repeated by someone who had read
it.** Whether `sd -stop` failed or correctly reported a stuck daemon is
unknown, for that reason, and is deliberately NOT recorded as an SD defect.

**Still open from this session:** nobody reported the two wizard pages, which
ran again and are still unread; and the `sd -stop` question above, which needs
one elevated rerun capturing both streams.

## 17 Aug 2026 - Section 7 step 6a built: the API authenticates against $CRED

From `e3b4b25`. Continues the sixteenth session below without an install
between, so **the cycle that was open is now closed by these source changes**
and `assert-current` will fail until the next one runs.

**The last pre-step-6 measurement first, while the install was still current.**
§2 asked whether a real API login presents a domain-qualified name, since
`!valid_os_name` at `APISRVR:894` rejects a backslash and would refuse
`GITORLI\don` before authenticating. **SD's user name is `don`, bare** —
`WHO.AM.I` says so where Windows `whoami` says `gitorli\don`, because
`process.username` comes from the MSYS2 runtime's own lookup. So the call is a
**smell, not a defect**. **Its limit, stated because it cannot be closed here:**
this is a workgroup machine, and MSYS2 renders a domain user as `DOMAIN+user`,
where `+` fails that same charset just as `\` does.

**WHAT WAS BUILT.** `!CRED_VERIFY` replaces `login(username, password)` at
`APISRVR:940`; `login_user()` is **deleted** from `linuxio.c`, taking
`/etc/shadow` and — closing step 6d — its `setgid`/`setuid` with it;
`PASSWD_FILE_NAME` is out of `sdnet.h` and the prototype out of `sd.h`; and
`op_login()` stays as a fail-closed stub, because `opcodes.h` is positional and
`BCOMP`'s `int.intrinsics` is matched to it by position. `make sd` clean after
`rm -f gplobj/*.o`, which was required rather than tidy — three headers changed.

**THE PART THAT WAS NOT OBVIOUS, AND A DEFECT CAUGHT IN THE DESIGN BEFORE IT
WAS WRITTEN.** Checking the password is the easy half; the session identity —
`process.username` and `my_uptr->username`, which `@logname`, `K$USERNAME` and
**the audit trail** all read — is set in C, and `op_login()` used to set it as
a side effect of the `/etc/shadow` check. Removing that leaves BASIC no route.
The first plan was to make `K_USERNAME` settable. **It would have renamed the
session to `"0"`:** both readers call `kernel(K$USERNAME, 0)`, and
`k_get_c_string()` renders that integer as the string `"0"`, which any
"set if non-empty" rule accepts — and `HDR_INTERNAL` would not have caught it,
because `APISRVR` *is* `$internal`. A new key, `K_SET_USERNAME` = 60, cannot
break a reader. It is gated on `HDR_INTERNAL` exactly as `K_ADMINISTRATOR` is,
for the reason step 4 stamps the trail in C: an ungated setter hands back the
ability to claim somebody else's name.

**NOT RUN, and it cannot be yet** — no API client, `SDConnectLocal()` never
exercised, and the transport measured unportable the day before. It sits in §4
Not verified. The BASIC has not been through a compiler either; `bbcmp.py`
builds only the bootstrap seed, so `SECOND.COMPILE` is its first, and both new
statements were instead checked against existing usage —
`call !CRED_VERIFY(...)` against `SET_ACC_PASSWORD:113`, `void kernel(...)`
against `AUTOLOGOUT:58`.

**HANDOFF PASS, and three stale claims found in PROJECT_STATUS while making
it.** All three were §4 **Not verified** entries that §4 **Verified**
contradicted, which is the worst way for this file to be wrong — a cold session
reading the pessimistic half would redo finished work or distrust a working
system. The login rule was recorded as "built and has never run" a week after
being measured 5 of 5 and then 6 of 6; the service likewise, with header item 2
recording it closed and verified on the same page; and two staging claims had
been overtaken by every stage built since. **Corrected in place, struck through
rather than deleted**, so the mistake stays visible. The header also still
called §8's `CA`-resolution question a blocker after it had been answered.

**The lesson for this file, and it is a §0 rule 3 failure rather than an
accident:** an entry moved into Verified must be struck out of Not verified in
the same edit. Closing one half and leaving the other is how the two halves came
to disagree, and nothing checks it.

---

## 16 Aug 2026 - Sixteenth session: the install of 17:51:35 was a failed bootstrap

From `222701a`. **Correction to the fifteenth session's entry below, and to §8.**

**CREATUSR IS GONE — §7 step 1a.** The `struct PCFG` field, its default,
`op_config.c`'s answer and `CONFIG`'s print. `op_pconfig()` never had a branch.
`make sd` clean after `rm -f gplobj/*.o`, which was **required rather than
tidy**: `config.h` changed and the Makefile tracks no header dependencies, so
every field after the removed one shifts under any stale object.

**The parser still accepts and discards `CREATUSR=`.** `read_config()`'s chain
ends in `else { "Unrecognised configuration parameter" }`, which aborts and
stops SD starting, and `../sdb64` still parses the parameter — so deleting the
branch would turn a tidy-up into a failure to start for anyone whose `sd.conf`
came from a Linux install. No `sd.conf` on this machine has one; all four were
checked. Three lines against a startup failure.

**THE FINDING THAT MATTERS: NO SD SESSION HAS EVER RUN ON THE 17:51:35
INSTALL.** It is 337 files short — `gcat` **4** entries not 132, `GPL.BP.OUT`
**3** not 193, `gcat/$CPROC` **0 bytes**, no `$LOGIN`, no `VOC`. Found by
accident: a control/treatment test of the CREATUSR parser failed in **all four
cells**, including the installed binary with the default config, every one
dying `Unable to load '$CPROC' object code` with `0xC0000005`. An equal failure
on both sides cannot be caused by what differs between them — the control is
what turned a puzzling result into a diagnosis.

**What happened.** `C:\Users\dmont\stagetest` is **healthy** (16:18, 3,475
files, `gcat` 132, `$CPROC` 25,208) and is **not what was packaged**. The
installer of **17:34:39** was built from a tree whose bootstrap had died after
the seed phase: the installed `gcat` holds `bbcmp.py`'s objects (`$BCOMP`
70,697) where a finished tree holds `BCOMP`'s (87,992), stamped 17:28. Every
static file installed correctly, which is why the tree looked whole.

**Why nothing caught it.** `assert-current.ps1` compares an install against
**source**, and `gcat`, `GPL.BP.OUT` and `VOC` are build products with no
source counterpart — it exited 0 over this tree and was right to. `stage.py`
checked the bootstrap's **exit code**, which was 0.

**Fixed at the point it can be caught:** `stage.py`'s
`check_bootstrap_complete()` judges the tree the bootstrap left, on five facts,
and refuses to stage one that fails any. Exercised against both trees when
written — silent on the healthy stage, five faults on the broken install.

**CORRECTION TO §8's `CA`-RESOLUTION QUESTION, WHICH WAS NEVER A QUESTION.**
The fifteenth session read `gcat` holding 4 entries with no `$QPROC`, and
concluded *"This is a gap in the model, NOT evidence of a broken tree"* on the
grounds that `COUNT VOC` 431 is recorded repeatedly. It was evidence of a
broken tree. **`$QPROC` is in `gcat` at 54,073 bytes** in the healthy stage,
exactly where a `CA` verb's program should be, and those 431s were measured on
earlier installs. The tell was in the same reading and was passed over:
`gcat/$CPROC` was 0 bytes. Scoping the `gcat` lock is unblocked, against 132
entries rather than 4.

**`gplbld/secure-accounts.ps1` IS WIRED INTO NOTHING** — absent from
`stage.py`'s ship list and unmentioned in `sd.iss`, so it neither ships nor
runs. **Left that way deliberately.** Wiring it in alone would break account
access: it leaves `sdusers` nothing inheritable on `user_accounts`, so a new
account directory carries `CREATOR OWNER` and no `sdu_<name>`, and the
account's own user — and anyone `GRANT`ed it — is refused at the file layer.
Its partner half does not exist; `CREATEA` contains no `icacls` anywhere,
checked. Both halves land together or neither does.

**THE CYCLE RAN AND THE RESULT IS WHOLE.** Install of **22:57:00**,
`assert-current` exit 0, `sd.exe` `7A383F487235134B`: `gcat` **132**,
`GPL.BP.OUT` **193**, `gcat/$CPROC` **25,208**, `$QPROC` 54,073, `VOC` present,
3,477 files, `ACCOUNTS/DON` present — and an **unelevated** `sd` answered `WHO`
→ **`2 DON`**, `OFF` exit 0. `CREATUSR` is absent from the installed
`gcat/$CONFIG` (3,153 bytes) while `DEADLOCK` is present, which is the control
that makes the search mean anything.

**One thing is NOT verified and it is recorded rather than glossed:** the
`CREATUSR=` accept-and-ignore branch. `read_config()` runs **only when the
shared segment is created** — an attaching session takes `pcfg` out of the
segment — so no ordinary session can reach the parser. **Three attempts to test
it were blind, and so were their controls**, which is what eventually exposed
the mechanism: `sd --version` returns before the config is read at all, and a
normal session never reads it. The test is `sd -start` with `SD_CONFIG` naming
a conf carrying the line, plus a control carrying a genuinely unknown one that
must be refused. Elevated, service stopped; fold it into the next cycle's start
rather than tearing down a good system.

**§8's LOAD-BEARING UNTESTED QUESTION IS SETTLED, AND IT KILLS THE LINUX CLIENT
CONTRACT.** The question was whether Win32-OpenSSH supports `-L
port:/path/to/socket`. It does — the client parsed it against a malformed
control that was rejected as `Bad local forwarding specification`. **The
blocker is elsewhere and is fatal:** a socket bound by MSYS2 is, seen from
native Windows, a **54-byte regular file** reading `!<socket >52445 s <cookie>`
— the Cygwin emulation, a TCP port plus a shared secret — where a real Windows
AF_UNIX socket is a zero-length reparse point. Demonstrated on one socket at
one moment: MSYS2's own client **connected** and the server logged the accept,
while native `curl.exe --unix-socket` on the same path failed in 0 ms and the
server saw nothing. So `sshd`, a native Windows program, cannot reach a socket
SD creates, and `ssh -L <port>:/tmp/sdsys/sdclient.socket` cannot be ported.
**This decides the named pipe**, which §8 had already argued for.

**The first run of that test produced a confident wrong answer**, and it is
recorded because the shape recurs: MSYS2's emulation needs the server to
actively `accept()` for the client's cookie handshake to finish, so a
`listen()`-then-sleep server times out *every* client. Native curl failed, and
it would have been written up as proof — except the control failed too, and an
equal failure on both sides cannot be caused by what differs between them.

**§7 STEP 6a DECIDED, NOT BUILT: `$CRED`, not `LogonUser`.** Owner's call when
asked. The design is worked out and written into step 6a, including the part
that is not obvious: the hard bit is not checking the password but **setting
the identity afterwards**, since `process.username` is set in C and
`K_USERNAME` is read-only. The answer is the `K_ADMINISTRATOR` precedent — a
setter gated on `HDR_INTERNAL`, which `APISRVR` carries and ordinary BASIC
cannot reach. An ungated setter would let any program rewrite the identity the
audit trail is stamped from.

**§7 STEP 1c CLOSED, AND WITH IT STEP 1 ENTIRELY.** `DELETE.ACCOUNT`'s "SD
created it" branch had never executed. `sdacct14` was made by
`verify-createaccount.ps1 -Keep` from an **unelevated** session at 23:34 —
and **authenticated over ssh and ran `whoami`**, answering `gitorli\sdacct14`,
so the account was real and carried a password SD set. Fifteen seconds later
`DELETE.ACCOUNT sdacct14`, again unelevated into SDSYS, removed all four
halves: Windows user, `sdu_sdacct14`, account directory, `ACCOUNTS` record.

**The branch is established by state rather than by reading the message, and
that is worth being precise about.** `DELACC`'s three cases leave different
things behind and only `case sd.made.it` (`sysmsg(10028)`) deletes the Windows
user — 10036 leaves it, 10037 means it never existed. It existed and it is
gone. The directory mtimes corroborate in DELACC's own order: `user_accounts`
23:34:29, `PSTMP` 23:34:31 (the privileged half through `!ps_script`),
`ACCOUNTS` **last** at 23:34:32, which is the deliberate ordering that leaves a
failed run re-runnable. The 10028 line went to the operator's screen and was
not read by this session.

**A useful by-product: `whoami` running proves `ForceCommand` is off here.**
Re-measured after the 22:57:00 install, `sshd_config` is the pristine
`11:11:30 / 2297 bytes` with no `AllowGroups`, no `ForceCommand` and no marker
block. That is two rules working as designed at once — the uninstaller removes
them, and the installer will not re-apply them on a machine that already had an
ssh server. It also re-confirms the "leave an ssh server we did not install
alone" branch on a second install. It does mean **applying them is a manual
step of every fresh install on this machine**.

**And that hunt turned up a trap worth more than the change that found it:**
`struct PCFG` is described in `config.h` as "loaded per process", and **it is
also in the shared segment** (`sysseg.c:288` writes a template, `:142`
memcpy's it into every attaching session). So removing one `bool` from it
altered a layout two binaries must agree on, and the only guard,
`SYSSEG_REVSTAMP`, is `MAJOR_REV/MINOR_REV/BUILD` — the release number, which
did not change. Harmless as shipped, since an install replaces every binary at
once; it would bite anyone copying a rebuilt `sd.exe` onto a running system.

---

## 16 Aug 2026 - Fifteenth session: the ssh server stops being optional

From `5e986b6`.

**INSTALLED AND MEASURED, on the 17:51:35 install** — `assert-current` exit 0,
`sd.exe` `239BB9C3E43E4829`. What that proves is the **"leave an ssh server we
did not install alone"** branch, which is the half this machine can prove: the
firewall rule stayed `Enabled True / Private / RemoteAddress Any` and
`sshd_config` stayed byte-identical at `11:11:30 / 2297 bytes`, both compared
against a baseline taken before the install. PATH 7 entries / 0 empty.
`ssh-firewall.ps1` shipped.

**The mandatory-install branch is still unobserved** and cannot be observed
here — see the closing section.

**Changed again AFTER that cycle, so these are unverified:** the closing dialog
was trimmed, the first page was rewrapped, and `gplbld/secure-accounts.ps1` was
added. The install is therefore no longer current and `assert-current` fails by
design.

**What prompted it.** The owner asked three questions about the installer:
whether to offer a location other than `Program Files`, whether the first page
should say what the installer is about to do, and whether the ssh features
should be optional so a local-only user can decline them. Answering the third
turned up the real defect: `sd.iss` applies the `sdsshonly` deny rights
unconditionally and `CREATEA:442` joins every non-administrator account to that
group, so **on a machine with no ssh server every account SD creates can sign in
nowhere at all** — console denied, RDP denied, no ssh. The only usable accounts
were the installer's own (`ADOPT`) and `... ADMINISTRATOR`, which answers "the
second person needs to run SD" with "make them a machine administrator".

**The owner's answer was to make ssh mandatory** rather than to add a local
account kind: *"That allows a local user to emulate remote users by just
ssh'ing to their own computer."* This keeps §5.6.2 and `CREATEA` untouched and
removes a whole fork — no third account kind, no conditional deny rights, one
access path to test. §8 had already reached half of it, saying posture B "makes
the ssh install path load-bearing"; nobody had followed that into the installer.

**One amendment was made to the owner's shape and accepted.** Installing the
capability creates `OpenSSH-Server-In-TCP` and enables it — measured on this
machine, `Enabled True, Inbound, Profile Private, RemoteAddress Any` — so
"always install" would open port 22 to the LAN on every install, including for
the local-only user whose case made ssh mandatory. **The checkbox was inverted
rather than deleted**: the server is always installed, and the opt-in became
"let other computers connect", which is where the risk actually sits. The local
user ends up with a machine no more exposed than before.

**What changed:** `installssh` task deleted; `install-ssh.ps1` runs under
`Check: SshServerAbsent`. New `gplbld/ssh-firewall.ps1` and the `sshremote`
task. `installssh\allowgroups` promoted to `limitssh`. `SshWasAbsent` cached in
`InitializeSetup`. New `SshReport` and `ApplySshFirewall`. A memo page after
`wpWelcome` listing every machine-level change. `stage.py` ships the new script.

**Two comments in `sd.iss` were found asserting checks nobody had written**, and
this is the part worth carrying forward. One claimed `CurStepChanged` reported
the OpenSSH exit code; the other claimed it checked `deny-logon.ps1` "so it
cannot fail silently, which is the mistake the OpenSSH step made" — while making
that same mistake one entry above. `CurStepChanged` read neither: a `[Run]`
entry discards its exit code. Both corrected in place per the standing rule.
The OpenSSH half is now genuinely checked, from machine state rather than an
exit code, which also answers correctly when the capability was already there.
**`deny-logon.ps1` is still unchecked** and is recorded in §7 step 3 — it needs
`LsaEnumerateAccountRights`, so there is no state Inno can read.

**What is still open, and it is the whole of the verification.** The mandatory
path **cannot be tested on this machine**, which already has OpenSSH:
`SshServerAbsent` is false here, so only the "already present, leave it alone"
branch runs and both new tasks are hidden. Structurally the same hole that has
kept the `AllowGroups` task unseen since 14 Aug. It needs the VM from §7 step 2
(`Windows 11 Clone`, snapshot `Before SD install`).

**Not done, and not answered:** question 1. The recommendation was to leave the
destination page as it is and harden `{app}` with `icacls` unconditionally,
because nothing does today — `{app}` relies entirely on Program Files' inherited
ACL, and it holds `sd-elevate-helper.ps1`, which `sd-elevate.ps1:111` resolves
with `$PSScriptRoot` and launches `-Verb RunAs`. Install anywhere with a loose
root ACL and that is arbitrary code as administrator: the same class as the
`PSTMP` fix of the previous session. The owner has not ruled on it.

**The data-location half of question 1 is ANSWERED, by the owner, and it needs
no code:** mount a second disk at an empty NTFS folder — `C:\ProgramData\SD` —
and the database is on its own volume with nothing in SD changed. That avoids
all of `stage.py`'s embedded paths, the `ACCOUNTS/SDSYS` rewrite and
`check_no_stage_paths()`. Two caveats: the mount must exist **before** the
install, and the MSYS2 layer is the thing to watch rather than Windows, since a
volume mount point is a reparse point and the POSIX runtime sometimes presents
those as symlinks — `sdrealpath()` and the `/dev/shm` `fstab` mapping both land
on it. Recorded in §5.8.

### What the file-permission thread turned up, and it outgrew the session

Asked whether the "everything under SD is readable by every SD user" limit was a
Windows limitation. **It is not — Windows is the more expressive of the two**,
and the Linux original is weaker than remembered. Checked against the real
`installsd.sh` from `codeberg.org/stringdatabase/sd-scripts`, not the
experimental `installsdai.sh` in this tree: every mode in it is 644, 654, 755 or
775, there is no `setfacl` and no `umask`, `chmod -R 755 $sdsysdir` makes SDSYS
world-readable, and the only directory-creation mode in the C is
`mkdir(path, 0777)` (`sddefs.h:105`). `CREATEA` at `f9edab0` sets
`chown user:sdu_<user>` and `chmod g+s`, but **nothing removes other-read**. So
the Windows port is already stricter, because `icacls /inheritance:r` strips the
inherited `BUILTIN\Users:(RX)`.

**Measured on the installed tree:** `gcat` and `GPL.BP.OUT` both carry
`sdusers:(I)(OI)(CI)(M)`. Any SD user can rewrite catalogued pcode that every
other session executes, including an administrator inside an elevated-helper
session whose `!ps_script` calls build what the privileged helper runs. Same
shape as the `PSTMP` fix.

**Two collisions with the unelevated-token model shape all the remedies**, and
both were found by tracing rather than by reading:

1. **`sd.exe` stays unelevated for life**, so all of SD's file I/O uses the
   invoking user's token even inside an SDSYS session, and an unelevated
   administrator's `Administrators` membership is deny-only. So `sdusers:M` on
   `sdsys` is load-bearing — it is what lets `CREATE.ACCOUNT` write `ACCOUNTS`.
   A wholesale read-only `sdsys` would break account registration.
2. **The account directory cannot be locked when it is created.** `CREATEA:328`
   creates it and population runs to about line 600 as the invoking user, so the
   per-account ACL has to go on at the very end — and `DELETE.ACCOUNT` then has
   to remove the directory through the elevated helper, because an administrator
   not in `sdu_<name>` cannot delete it from an ordinary session.

`gplbld/secure-accounts.ps1` was written for the container half: the
`secure-psdir.ps1` pattern with `AD` instead of `WD`, `DC` withheld so one user
cannot delete another's account, and `CREATOR OWNER` inheriting into
subdirectories as well as files — the last is load-bearing, since with `sdusers`
holding nothing inheritable it is the only thing granting the creating session
rights to the directory it just made.

**A correction made in this session's own notes:** the claim that "`gcat` holds
only SD's four own programs, so locking them is small" is built on an untraced
model. `LIST` is `V`/`CA`/`$QPROC` and `$QPROC` is in neither `gcat` nor
`GPL.BP.OUT`, yet `COUNT VOC` returning 431 is a repeatedly recorded
measurement — so `CA` resolution works by a path nobody here has followed. §8
carries it; trace it before scoping the lock.

**Two defects found in the shipped `VOC_TEMPLATE`**, neither related to the ssh
work: five entries hold their DESCRIPTION in field 1 where the type code belongs
and so cannot work — `COPYP`, `DELETE.SERVER`, `LOAD.LANGUAGE`, `SET.SERVER`,
`UNLOCK` — and `SET.SERVER`/`DELETE.SERVER`/`LIST.SERVERS` have no compiled
program behind them at all. `UNLOCK` is the one that matters: it is what clears
a stuck record lock, and it needs the missing `V` line.

**The three-tier user model** the owner set out — application user, programmer,
administrator, with a new `PROGRAMMER` keyword on `CREATE.ACCOUNT` — is in §8
with the 144-verb split and the finding that **the two tiers that exist today
are enforced backwards**: `SH` is gated on `IsElevated()`, which an ssh session
can never be, while `OS.EXECUTE ... CAPTURING` is ungated, so tiers 1 and 2 have
identical actual power.

---

## 16 Aug 2026 - Fourteenth session, closing summary

`99e936f` to `00432d8`. Started from a handoff reading "elevation is built and
bootstrapped, and has never been run". It runs, and nothing in it is
unverified.

**Six defects, seven install cycles, and not one defect was visible by reading
the code.** Every one sat at a seam between two halves that were each correct
alone and had been reviewed as such:

1. `CPROC` obtained privilege and then refused the LOGTO that obtained it.
2. The helper could never run any script SD sent it - `-File` against a file
   with no `.ps1` extension.
3. Four failure exits released nothing, leaking the helper on a refused LOGTO.
4. `LISTMEM` carried an elevation guard it could never satisfy.
5. Privileged scripts were readable AND writable by every SD user.
6. Uninstalling left an empty PATH entry, one per cycle.

Also built: the helper log and the ACL that keeps SD users off it. Also closed:
7 step 5, `GRANT`/`REVOKE` watched writing their records.

**What actually did the finding.** The audit trail named defect 1 from an
adjacent GRANTED/REFUSED pair before any source was opened, exposed defect 3
through an `ELEVATION RELEASED` that never appeared, and later corrected this
session's own wrong account of which runs had elevated. Defect 6 came from the
owner reading his PATH. The remaining three came from running the thing and
reading the message it gave.

**Two comments in the source were wrong in the way that had caused the defect**
- `PS_SCRIPT` arguing a script was safe because the installer "grants narrowly",
which is narrow against the world and not against SD's own users. Both were
corrected in place rather than replaced, so the mistaken reasoning stays
visible to whoever reads it next.

**Three wrong hypotheses were tested and discarded** before the right one, each
without touching the machine: MSYS2 argv mangling of `"\\"`, SD's child
context, and - for the watchdog - a launch method that turned out to be
innocent. Cheap to test, and each one narrowed the field.

**Two corrections to claims made during the session**, both recorded rather
than quietly dropped: "no UAC prompt appeared" during the watchdog attempts
(the trail proved elevation had succeeded three times, and the helper DETECTION
was what failed), and "WATCHDOG FAILED" (the process being watched was the
measuring shell's own).

Left open, none blocking: the PSTMP fix rests on a measured mechanism rather
than a measured attack, nothing here automating two concurrent SD users; the
helper log cannot say which operation each `ran` line was, `!ps_script` reusing
one temp file name; and `sdsvc-sd.log` still captures nothing, which is the
prerequisite for the `shm_unlink` errno.

---

## 16 Aug 2026 - The privileged script was writable by every SD user

Fourteenth session. Found while writing up the helper log, fixed on the
owner's instruction. **Unbuilt when written.**

`!ps_script` wrote each script with `openpath '.'` - the current account
directory, `C:\ProgramData\SD\sdsys` for an SDSYS session - where the data
tree's grant is inherited as `sdusers:(OI)(CI)(M)` on every file. Checked on
the installed tree, not assumed.

**The disclosure was the lesser half.** `!set_passwd`'s script carries a new
Windows password in clear until it is deleted a moment later, so another SD
user could read it. **The serious half is elevation:** another SD user could
REWRITE a pending script between SD writing it and the elevated helper
executing it, and the helper runs what it finds with full privilege. That is a
local privilege escalation.

**The reasoning that caused it is in the source, and was corrected in place
rather than quietly replaced.** `PS_SCRIPT`'s description argued the file was
safe because the installer breaks inheritance on `C:\ProgramData\SD` and
"grants narrowly", so the script was "protected by work already done, with no
icacls call of its own". The grant is narrow against the WORLD; it is not
narrow against SD's own users, who all hold Modify. A true statement about the
wrong threat.

**The fix:** `@sdsys\PSTMP`, created by the installer through the new
`gplbld/secure-psdir.ps1`. `sdusers` gets list/create/traverse **on the
container only, with no inheritance flags**, so it reaches no file;
`CREATOR OWNER:(OI)(IO)(F)` hands each script to the session that wrote it;
Administrators and SYSTEM keep `(OI)(CI)(F)`, which is how the elevated helper
reads it. `DC` is withheld so nobody can delete another's file to take its
name.

**The semantics were measured before building anything** - a file created in
such a directory comes out `don:(I)(F)`, `Administrators:(I)(F)`,
`SYSTEM:(I)(F)`, with `sdusers` absent, and its creator can still read, write
and delete it.

`!ps_script` **fails closed** if the directory is missing rather than falling
back to the old location. Verified this cannot break the bootstrap:
`bootstrap.py` only compiles and never reaches `!ps_script`; the installer's
`adopt-account` step does reach it but runs at `ssPostInstall`, after `[Run]`.

The routine got **shorter**: `@sdsys` is already a Windows pathname - `sd.conf`
carries `SDSYS=C:\ProgramData\SD\sdsys` and `@ds` is the backslash - so the
`ospath`/`K$WINPATH` conversion that existed only to convert a POSIX working
directory is gone.

---

## 16 Aug 2026 - The helper log, and why not AppData

Fourteenth session, `0f33cf9`, verified on the 16:02:58 install. Owner's
decision after asking where such a log should live.

`C:\ProgramData\SD\sd-elevate.log`, created by the installer through the new
`gplbld/secure-log.ps1`, with **`sdusers` absent from the ACL entirely**.
Measured both ways: `don` unelevated is refused the contents **and the ACL** -
`icacls` itself answers `Access is denied` - and after one `LOGTO SDSYS` plus
`CREATE.ACCOUNT` the file holds `helper up`, six `ran ... -> 0` lines, `stop
requested` and `helper exiting`.

**AppData was the owner's suggestion and was rejected on a measurement, not a
preference.** `%LOCALAPPDATA%` grants the user Full Control and, decisively,
the user **owns** it; an owner keeps implicit `WRITE_DAC`, so the person the
log is about could reset any ACL placed on it. `C:\ProgramData\SD` is owned by
`BUILTIN\Administrators` and cannot be taken back by an ordinary SD user. A
second problem settled it independently: the helper runs as whichever
administrator consented at the UAC prompt, so with a standard user at the
keyboard the log would land in a profile that need not be the session's.

**The ACL is stricter than the audit trail's**, which reads backwards until you
see why: `audit` must keep `sdusers:AppendData` because unelevated SD sessions
write it themselves, and nothing unelevated ever writes this one.

`!elevate` was left unchanged on purpose. Nothing in BASIC can name the file -
the installed tree maps only `/dev/shm`, so `/` is `C:\Program Files\SD` and no
POSIX path reaches the data tree - and `sd-elevate.ps1` derives it from
`%ProgramData%` exactly as the installer does, so the two cannot drift.
It logs **only if the file already exists**: creating one on demand would
inherit the data tree's Modify for every `sdusers` member, and a record of
privileged work its own subjects can rewrite is worse than none.

**Known limit, recorded rather than left to be discovered:** every `ran` line
names the same path, `!ps_script` reusing one temp file per user number, so the
log gives the count and each exit code but not which operation was which.
Naming them needs `!ps_script` to pass a label. **Logging the script body is
permanently out** - `!set_passwd` travels the same path carrying a new Windows
password in clear, which is also recorded in PROJECT_STATUS.md as an unfixed
exposure in its own right.

---

## 16 Aug 2026 - LIST.GRANTS verified; the elevation work is finished

Fourteenth session, `d3de6b9`, on the 15:26:33 install (`assert-current` exit
0, `gcat/!OS_GROUP` 1,933).

    LIST.GRANTS DON       ->  Windows accounts granted DON: don
    LIST.GRANTS SDACCT12  ->  Windows accounts granted SDACCT12: sdacct12

`CREATE.ACCOUNT USER sdacct12` was run in the same session as a deliberate
regression check - the fix changed how `ps` is built for **every** action, not
only LISTMEM - and created the account correctly, groups and all, through the
elevated helper. No helper or pipe survived the session.

**Four defects in one feature, in one day, none of them visible by reading the
code**, and all four at a seam rather than inside a component:

1. `CPROC` obtained privilege and then refused the LOGTO that obtained it.
2. The helper could never run any script SD sent it (`-File` versus a file with
   no `.ps1` extension).
3. Four failure exits released nothing, leaking the helper on a refused LOGTO.
4. `LISTMEM` carried an elevation guard it could never satisfy.

Each half was correct alone and had been reviewed as such. What was never
exercised was the join. The practical lesson for this project is in the cost
ratio: four fresh install cycles found all four, while reading the same code
across two sessions found none.

**The audit trail did most of the diagnosing.** Defect 1 was named by
`ELEVATION GRANTED` and `LOGTO REFUSED` appearing in the same second, before
any source was opened; defect 3 by `ELEVATION RELEASED` never appearing at all;
and the trail later corrected this session's own mistaken account of which runs
had elevated successfully.

---

## 16 Aug 2026 - LIST.GRANTS carried a guard it could never satisfy

Fourteenth session. `GRANT`/`REVOKE` were watched writing their audit records -
`GRANT account=SDACCT11 to=don` 14:48:22, `REVOKE account=SDACCT11 from=don`
14:48:24 - which **completes §7 step 5**. `LIST.GRANTS`, run in the same
session, failed three times out of three with `Cannot read the members of group
sdu_sdacct11, status: 5`.

`OS_GROUP` builds an elevation guard **unconditionally, before the action
dispatch**, and every action appends its body to it. The writing actions pass
it because `!ps_script` hands them to the session's elevated helper. **LISTMEM
is deliberately kept local** - it needs the script's output, which `ps_script`
cannot return - so it runs inside `sd.exe`, which is unelevated for life by
design, and exits 5 before reaching `Get-LocalGroupMember`. The one action that
could not satisfy the guard was the one still carrying it.

A seam, like the other three: the guard predates the split, and when LISTMEM
was carved out to stay local it was not carved out of the guard. The
`valid_os_name` test immediately above **was** excluded for LISTMEM at the same
time, so exclusions were being considered; this one was missed.

**Two wrong hypotheses were tested and discarded first**, both cheaply and
without touching the machine. That the script was mangled crossing the
MSYS2-to-Windows `execv` boundary, `"\\\\"` being the obvious candidate - run
through `C:\\msys64\\usr\\bin\\bash.exe` it arrives intact and exits 0. And that
SD's child context was to blame - cwd of the account directory, closed stdin,
`SD_SESSION=1` - every variation exits 0. The reproduction only became faithful
once the guard was included, which is when it returned 5 with no output. **The
first repro copied the `case act = 'LISTMEM'` line alone and missed that it
appends to a script already begun**; that is the mistake to avoid repeating in
this file, where `ps =` and `ps :=` differ by one character.

Fixed by building the guard only for the actions that go to the helper.
**Unbuilt when written.**

---

## 16 Aug 2026 - The -OwnerPid watchdog works; the test harness did not

Fourteenth session, no source change. The helper's own log:

    14:41:42 helper up, pid 11260, serving session 3004
    14:41:44 session 3004 has gone - exiting

**Two seconds**, matching the 2000ms idle wake at `sd-elevate-helper.ps1:78`.
A privileged process does not outlive the session that asked for it.

**Tested against a dummy owner process, not `sd.exe`**, so what is proven is
the helper's half. That SD hands it the right pid is still inferred from
`K$WINPID` existing for that purpose, not observed.

**Three attempts through a real SD session failed first, and neither failure
was the watchdog.** First `[Diagnostics.Process]::Start` with redirected stdin
- no UAC prompt appeared at all, where the piped form always raises one.
Then a background job, which produced no session. The cause of both is at
`sd-elevate.ps1:103`: `-Start` waits a bounded time for the helper to answer
PING and then gives up, so a UAC click that arrives late leaves no helper for
any test to find.

**Correction to a claim made during this session.** The isolated run was first
reported as WATCHDOG FAILED, "helper alive +33.8s". That was wrong. The pid
being watched was the measuring shell's own: the lookup was
`Get-CimInstance Win32_Process | Where CommandLine -like "*sd-elevate-helper*"`
**without excluding self**, and the search string is present in the searching
process's own command line. The run then ended trying to `Stop-Process` itself.
The same self-match had already been noticed and guarded against earlier in the
session; the guard was simply not carried into this query.

**The answer came from `-LogFile`**, passed for the first time here. Two lines
settled what three attempts without it could not, which turns the open question
about a helper log from an argument into a measurement.

---

## 16 Aug 2026 - Elevation verified end to end

Fourteenth session, `3e010cf` and `2f32f6f`, on the 14:21:50 install.
**An unelevated SD session created a Windows account.**

`sd` → `LOGTO SDSYS` → UAC accepted → `WHO` says `2 SDSYS from DON` →
`CREATE.ACCOUNT USER sdacct11` → `User sdacct11 Created`, in `sdusers`,
`sdsshonly` and `sdu_sdacct11`, not an administrator, SD side registered →
`LOGTO DON` → `OFF`. No helper and no pipe survive. The trail:

    ELEVATION GRANTED account=SDSYS
    LOGTO account=SDSYS
    ELEVATION RELEASED account=DON
    LOGTO account=DON

with ten seconds between grant and release - `CREATE.ACCOUNT` working through
the helper. **`ELEVATION RELEASED` also answers a question left open below:**
the helper exits because `LOGTO` out of SDSYS sends `STOP`, not because the
watchdog found a corpse. Declining the prompt was re-measured on this same
build and is still refused with `sysmsg(10002)`.

**Three installs were needed, each a full uninstall with both trees deleted.**
That is the cycle rule working rather than overhead: the first install produced
defect 1, the second produced defect 2, and neither would have been visible in
a tree carrying a mixture of the two.

Still open, none of it blocking: the `-OwnerPid` watchdog has never been
exercised, since every helper so far was told to stop; `GRANT`/`REVOKE` has
still not been watched writing a record; and the helper writes no log unless
`-LogFile` is passed, which `!elevate` never does.

---

## 16 Aug 2026 - LOGTO SDSYS works; the helper could never run a script

Fourteenth session, continuing below. `3e010cf` built and installed:
**`LOGTO SDSYS` from an ordinary unelevated prompt now succeeds** — UAC
prompts, the administrator consents, `WHO` answers `2 SDSYS from DON`, and
`LOGTO DON` moves back out. First time observed.

`CREATE.ACCOUNT` then failed with `Create User Failed, OS Error: 127` —
**not** the 5 an unprivileged attempt gives, so the privilege was real and
reaching the helper.

`sd-elevate-helper.ps1:122` ran scripts with `powershell -File`. **`-File`
refuses any file not named `*.ps1`** — measured: exit `-196608`, nothing
executed, "the file does not have a '.ps1' extension". `!ps_script` names these
`$PS.TMP.<userno>`, so **-File could never have run a single one**, and
`!ps_script`'s own local path uses `Get-Content | Invoke-Expression` for that
exact reason. The helper was written to do the same job a different way, and
the difference was the bug. Fixed by making the two identical in how they
execute and different only in privilege; the corrected form was measured
standalone before being committed - scripts exiting 0, 1 and 5 report 0, 1
and 5.

**Two defects in one feature, both invisible to reading and both caught by
running it once.** Each half was correct alone: the elevation mechanism was
measured end to end in the thirteenth session, and `!ps_script` had worked for
months. What failed was each seam between them.

**The helper writes no log unless `-LogFile` is passed, and `!elevate` never
passes one**, so `Say "ran $req -> $code"` went nowhere and this was diagnosed
entirely from outside the process. Where such a log should live is not decided
- not the data tree, which every `sdusers` member can write.

Unverified when written: the helper fix, and `ELEVATION RELEASED` / `LOGTO
account=SDSYS`, which have still never appeared in a trail.

---

## 16 Aug 2026 - Elevation ran for the first time, and refused itself

Fourteenth session. Packaged, installed and ran the elevation work of
`ea052a4`/`6dadaa1`. **The mechanism works. The feature did not.**

`LOGTO SDSYS` from an ordinary unelevated prompt raised a real UAC prompt,
started the helper, and wrote `ELEVATION GRANTED account=SDSYS` to the trail —
then refused the LOGTO with `sysmsg(10003)` and wrote `LOGTO REFUSED
account=SDSYS reason=not granted` **in the same second**.

`logto.authorised` (`CPROC:3602`) asks `kernel(K$ADMINISTRATOR,-1)`, which
reads `USR_ADMIN` — seeded once from `IsElevated()` at process start
(`kernel.c:195`). **SD stays unelevated for life by design**, the privilege
being the helper's, so that flag is false and always will be. `CPROC:2639` does
set it, 40 lines after the test that needed it. `6dadaa1` removed the old
`K$ADMINISTRATOR` gate and added `elevate('START')` without joining the halves;
the feature could never have worked, and no test between them would have
noticed, because each half is correct alone.

**Fixed in `CPROC`, unbuilt at the time of writing:** `elev.obtained`, cleared
per-LOGTO, set on a successful `START`, accepted by `logto.authorised`; plus
`logto.privilege.undo` at the four failure exits between the elevation and the
move, none of which released the helper.

**What it cost, and what earned it back.** Three elevated steps from the owner
and two UAC clicks. Against that, **the audit trail diagnosed the bug on its
own** — the adjacent `GRANTED`/`REFUSED` pair named the failing branch before
any source was read, and the absent `ELEVATION RELEASED` exposed the leaked
helper as a second defect. The feature verified a week ago paid for itself
here.

**Also measured, and still open:** declining the prompt is already correct
(`sysmsg(10002)`, `reason=elevation refused or unavailable`); no helper
outlived a session, but only because the process died, so the `-OwnerPid`
watchdog remains untested; and `ELEVATION RELEASED` and `LOGTO account=SDSYS`
have still never been observed.

---

## 16 Aug 2026 - Elevation without an elevated terminal

Thirteenth session, `ea052a4` and `6dadaa1`. **Built and bootstrapped; nothing
has run it.** PROJECT_STATUS.md item 1 carries the state and the test.

**It started as a complaint about the installer's dialog.** It told
administrators to open an ELEVATED command prompt, and the owner said that was
never the specification. Checking rather than assuming: the gate on
`CREATE.ACCOUNT` (`CREATEA:90`) is `rev 0.9.0` and traces to the initial import
— **not ours**. What was ours was making an elevated terminal the only way to
satisfy it. Underneath, Windows genuinely requires an elevated token to create
a local user (`CREATE_USER:48`), and no SD change removes that.

**The design is the owner's.** Three were offered — one prompt per account, one
per session, or a LocalSystem service with no prompt at all — and the owner
proposed a fourth that was better than any of them: hang elevation off `LOGTO
SDSYS`, using the reserved `LOGIN` paragraph as the hook. That collapsed a
problem rather than solving it. Elevation becomes a property of *being in
SDSYS*, which CPROC already tracks, so `USR_ADMIN` keeps its meaning and no
existing gate changes. The rule that came with it: **no `ELEVATE` verb**, since
"there should never be an elevation from within a normal session".

The check went into `CPROC`'s `int.logto` rather than the VOC paragraph, which
runs *after* the move — that would have left the session standing in SDSYS
unelevated while a paragraph tried to eject it.

**A process's token is fixed at creation**, so `sd.exe` stays unelevated for
life and an elevated helper does the privileged work. That is the smaller
exposure: in an elevated terminal everything typed is privileged; here only
what SD sends is.

**Measured before it was written, because two guesses were wrong.** The
integrity label was *not* the obstacle to an unelevated session reaching its
elevated helper — **the pipe's DACL is**, and without an explicit ACE the
connect is refused outright. And a helper serving repeated requests works with
a single prompt: a session that had just been refused `New-LocalGroup` had one
created for it through the pipe, exit code intact.

**Two kernel keys, both for facts BASIC could not reach.** `K$WINPATH` (58) —
`OS$FULLPATH` returns a POSIX path whatever its comment claims, and `!ps_script`
has been working around that by naming files relative to a shared working
directory, which does not stretch to `Start-Process`. `K$WINPID` (59) — the
helper watches its owning session with `Get-Process`, and the MSYS2 pid is not
that number.

**ssh exclusion became structural.** §5.6.2 already required administrator work
to happen at the console; it was enforced by an SD flag test. UAC needs an
interactive desktop, so it is now enforced by Windows. The cost is that a
remote-control tool must be installed **as a service**, or it cannot render the
secure desktop and the operator sees a frozen screen — said plainly in the
installer dialog, because the alternative is an unexplainable hang.

**What is known to work:** the pipe mechanism end to end, and the BASIC
compiles and catalogues — the bootstrap of 13:38:41 completed, and
`bootstrap.py` dies on any compile error or missing-`$define` warning.
`GPL.BP.OUT` 192→193, `!ELEVATE` in the catalogue. **What is unknown:** every
call site. No `LOGTO SDSYS` has been typed against this build, and the helper's
owner-watchdog is coded and untested.

---

## 16 Aug 2026 - The audit log, and step 5f closes with it

Thirteenth session, after the restart fix was verified. **Built, not verified**
— the call sites are BASIC and only a bootstrap compiles them, so nothing has
been observed being written.

**`audit_message()` in `k_error.c`**, beside `log_message()` so the contrast is
visible: `errlog` **discards its oldest half** at the `ERRLOG` size, which is
right for diagnostics and disqualifying for an audit trail, where the record
somebody would like discarded is exactly the one an investigator wants. The
audit file rotates instead — renamed `audit.<yyyymmdd-hhmmss>` at 1MB, nothing
deleted, pruning left to the site.

**BASIC reaches it as `kernel(K$AUDIT, text)`**, key 57. A kernel key rather
than an opcode because an opcode would mean touching the compiler; `op_logmsg`
was the precedent for the opcode route and `K$RUNEXE` for this one.

**The caller passes what happened and never who did it.** Timestamp, username,
uid and pid are stamped in C from `my_uptr`. §5.6 had already flagged that
`CPROC` reassigns `logname` when it drops to sdsys, so a trail that trusted its
BASIC caller would attribute a step-up to the account being entered — the
warning was in the spec and this is what it was asking for.

**Call sites.** `LOGIN` has exactly one success exit and one
`terminate.connection`, so both records are written once rather than at each
gate; an `audit.reason` is set at each refusal and **defaults to `unspecified`**
so that a refusal added later still produces a line — a vague record is
recoverable, a missing one is not. `CPROC` covers `LOGTO` success and all three
refusals, including the failed step-up the spec called the most interesting line
in the trail. `GRANTA` writes after the group edit, which **closes §7 step 5f**;
its header had named this file as one of its first callers and now says so in
the past tense.

**Then the trail was made append-only, the same session.** The first version
inherited `Modify` from the data tree, so the users it recorded could read,
rewrite and delete it. Owner's decision on being shown that: *"admins are
highly trusted - we are increasing security not maximizing it"*, so
Administrators and SYSTEM keep full control and the floor is raised against
ordinary SD users only. `secure-audit.ps1` leaves `sdusers:(AD,RA,S)`.

**The measurement that redirected the design.** `open(O_WRONLY|O_APPEND)`
**fails with errno 13** against an append-only ACL — the MSYS2 runtime maps
`O_WRONLY` to `GENERIC_WRITE`, which contains `FILE_WRITE_DATA`. Granting
`WriteData` to make it work gives back exactly what the ACL was for: measured
with it, an ordinary user **can** truncate the trail to nothing and **can**
overwrite individual records in place. Since `audit_message()` is deliberately
silent, shipping the POSIX version would have lost every ordinary user's
records without a word — the failure this port keeps having. So the write went
to `win32audit.c`, one `CreateFile` asking for `FILE_APPEND_DATA` alone; that
is the second `windows.h` file after `win32sem.c`, and the same shape.

Measured as an unelevated `sdusers` member against the shipped ACL: append
works; read, truncate, overwrite, rename and delete are all refused.

**Rotation had the same trap one level down.** A plain `rename()` leaves the
new file to be created by the next writer, which inherits `Modify` — so the
trail would have gone quietly back to editable at the first rotation, long
after anyone was looking. `win32_audit_rotate()` copies the DACL off the file
being rotated away and re-applies it `PROTECTED`; measured, the new file
matches the old with no inherited entry.

**VERIFIED ON A FRESH INSTALL, 12:18:42 the same day** (`assert-current` exit
0). The trail after an install and one unelevated session:

```
12:18:55 user=don uid=1 pid=522 LOGIN account=SDSYS
12:19:43 user=don uid=2 pid=529 LOGIN account=DON
12:19:43 user=don uid=2 pid=529 LOGTO REFUSED account=SDSYS reason=session is not elevated
12:19:43 user=don uid=2 pid=529 LOGTO account=DON
```

Line 1 is the installer's own account step; the rest is `sd` run as `don`.
Line 3 is the failed step-up the specification called the most interesting
line in the trail. Then, **as unelevated `don` against the real file**: read,
truncate, overwrite in place, rename and delete all refused, file unchanged at
287 bytes, and `icacls` itself refused — `(AD,RA,S)` carries no `READ_CONTROL`.

**Still unobserved:** `GRANT`/`REVOKE` writing a record (step 5f). It needs an
elevated session and a second Windows user.

**Incidental finding, and it corrects how this file and PROJECT_STATUS quote
hashes.** Two builds of identical source give different `sd.exe` hashes — the
PE `TimeDateStamp` is the link time, measured at `12:13:44`. Nothing embeds
`__DATE__`. `assert-current` is unaffected (it compares the installed file
with the `bin/` file it was copied from), but a hash names one build, not a
source state, and a mismatch across two builds means nothing.

---

## 16 Aug 2026 - A segment from a previous boot stops meaning wreckage

Thirteenth session, `8a1568d`→. Measurement first, on the still-open cycle;
then one source file changed, which ended it.

**The twelfth session's pending measurement passed.** Boot 10:50:51 with `shm`
empty: `sd -start` exit 0, `sdwind` up, service RUNNING (`sdsvc.log:10-13`),
and unelevated `don` reached account `DON` (`WHO` → `1 DON`, `OFF` → 0). The
prediction in that session's entry was that the failure alternates, and this is
the half that confirms it — **the leftover segment was the entire fault, and
the diagnosis needed no correction.**

**The fix**, `sysseg.c`: `sd_state()` now answers `SD_STOPPED` instead of
`SD_WRECKAGE` for a segment whose mtime predates boot, and unlinks it.
Reporting alone was not enough — `bind_sysseg()` looks for a segment before
creating one and would have answered "SD is already started" (`sysseg.c:132`),
so `sd -start` would have failed a second way instead of the first.

**Why it is safe, since this is the file where "already started" has been wrong
twice before.** The test is asked **only after the daemon is known to be
gone**, so a running system is never examined and a clock corrected after boot
cannot cause a live segment to be destroyed; the worst a wrong answer can do is
leave real wreckage looking like wreckage. `boot_time()` is
`time(NULL) - /proc/uptime`, checked against
`Win32_OperatingSystem.LastBootUpTime` and agreeing to the second, and it
answers 0 when unreadable — which restores the old behaviour exactly rather
than guessing.

**What it does not do.** The `shm_unlink()` failure at shutdown is untouched
and still unexplained: the leak is now harmless, not absent. A pre-boot segment
with a **mismatched revstamp** is still not cleared, because `sd_state()` reads
no further on a mismatch — reachable only by upgrading across an unclean stop,
and `sd -stop` remains the way out.

**VERIFIED THE SAME SESSION, and this is the controlled result the eleventh,
twelfth and thirteenth sessions were all working towards.** Fresh install at
11:12:25 (uninstall, both trees deleted and confirmed gone, reinstall from a
rebuilt installer; `assert-current` exit 0, `sd.exe` `D2AAB6203CB80661`). A
segment was then left in `C:\ProgramData\SD\shm` deliberately — mtime 11:15:45,
no daemon, service stopped — and the machine rebooted at 11:19:16:

- `sd -start` **exit 0**, `sdwind` up, service RUNNING.
- **The segment in `shm` is stamped 11:19:25, not 11:15:45.** The survivor was
  discarded and a fresh one created. That is the evidence the new path ran.
- Unelevated `don` reached account `DON`; `WHO` → `1 DON`, `OFF` → exit 0.

**The same state produced exit 1 at the 10:31 boot**, so this is a controlled
before-and-after rather than a system that might have worked anyway.

The stderr line added for this, `Discarding the shared segment left by the
previous boot`, **was not observed** — it went to `sdsvc-sd.log`, which
captured nothing for the fourth time. The mtime carried the proof instead.

**Two findings from building the fixture, both worth more than the fixture.**
The `shm_unlink()` failure is **shutdown-specific, not stop-specific**: a plain
`Stop-Service SD` on a running machine exited 0 and left `shm` empty (11:07:34),
against exit 1 with the segment left behind at the 10:31 shutdown. And the
reason it is only ever seen at shutdown is that **`sdsvc` already cleans up
after a dead daemon** — killing `sdwind` under a running service made the
wrapper notice and run `sd -stop` itself (11:14:34). That watchdog cannot help
when the machine is going down, which is the one time it would matter. It is
also why the fixture has to be built with the service stopped: killing `sdwind`
under a running service tidies the segment away, and the test would then pass
for the wrong reason.

---

## 16 Aug 2026 - The service fails its first restart, because /dev/shm is a real directory

Twelfth session, `fab17f2`→. **No source was changed**: the whole session is a
measurement and a diagnosis, taken on the install of 10:23:47 with
`assert-current` passing at 10:36.

**The restart test had already run before the session started.** The machine
rebooted at 10:31:21. `Get-Service SD` was `Stopped`/Automatic with no
`sdwind`, and SCM event 7024 recorded a service-specific error. The eleventh
session's last open item is therefore answered, in the negative.

**What `C:\ProgramData\SD\sdsvc.log` held:**

```
10:23:52  service starting                              <- install-time start
10:23:58  SD is running (sdwind.exe is up)
10:31:05  service stopping: "sd -stop" exited with 1    <- shutdown
10:31:30  service starting                              <- boot
10:31:31  "sd -start" exited with 1
10:31:41  SD did not start: sdwind.exe is not running
10:31:41  cleared the half-started segment: "sd -stop" exited with 0
```

**The cause.** `etc/fstab` binds `/dev/shm` to `C:\ProgramData\SD\shm`, which is
NTFS (`stage.py:196`, and it has to leave Program Files because `shm_open()`
creates files there and ordinary users need to write them). On Linux `/dev/shm`
is tmpfs and empties at boot. Here it does not. So the segment that the
shutdown `sd -stop` failed to unlink was still on disk when the machine came
back, and `sd -start` correctly refused it as `SD_WRECKAGE` (`sysseg.c:506`) —
correctly by its own rules, which were written for a filesystem that forgets.

**How it was pinned without any of the messages.** `sdsvc-sd.log`, which exists
solely to capture what `sd` and `sdwind` say, was 0 bytes for the third time
running, so both the shutdown `errno` and the boot refusal were lost. What
settled it instead was **the mtime of the `shm` directory: 10:31:41.396**, the
recovery `sd -stop`. A directory mtime moves only on add or remove. Nothing was
added — `sd -start` exited one second in, before `bind_sysseg()`, which unlinks
after itself on failure (`sysseg.c:332`, `:343`) — so an entry was *removed*,
and it must have been there at boot. The one-second failure independently rules
out both ten-second waits, the daemon poll and `sem_open`.

The two remaining links are single-code-path rather than observed, and are
recorded as such: `stop_sd()` has exactly one `return FALSE`, `shm_unlink()`
failing with errno other than ENOENT (`sysseg.c:785`), so `sd -stop` exit 1
means the file was left behind; and a fast `sd -start` failure over a segment
with no daemon can only be the `SD_WRECKAGE` branch.

**Not upstream.** `../sdb64` still uses System V IPC (`shmget`, `IPC_RMID`), and
those segments are kernel objects that vanish at reboot. The defect follows from
§5.1, this port's move to POSIX shared memory, and cannot occur upstream. No
`UPSTREAM_FIXES.md` entry — recorded so a later session does not re-check.

**A second finding, from asking why the service never retried.**
`install-service.ps1:114` configures two restarts, and `sc qfailureflag SD`
returns `FAILURE_ACTIONS_ON_NONCRASH_FAILURES: FALSE`. Windows applies recovery
actions only to a service that *crashes*; `sdsvc.exe` exits reporting
`SERVICE_STOPPED` with an error, which does not count. The policy has never
run. Worth noting in both directions: had it run, the 5-second retry would have
found the `shm` that the failed start had just cleaned, succeeded, and hidden
this bug behind an alternating-boot flap.

**What the eleventh session got right.** Its honest-failure work is the only
reason any of this was diagnosable. The service refused to report `RUNNING` over
a dead SD, wrote down how far it got, and ran `sd -stop` behind the failure — so
the machine was left clean rather than poisoned, and the log carried the exit
codes the diagnosis was built from.

**Left open at the handoff:** the fix is not written and not decided. The
preferred shape is to treat a segment older than the current boot as
`SD_STOPPED` rather than `SD_WRECKAGE`, since no process from before a reboot
can hold it — which restores Linux semantics and is needed whatever else is
done, because power loss and task-kill will always be able to leave a segment
behind. PROJECT_STATUS.md header item 1 has the alternatives. The machine was
left with `shm` empty and the service `Stopped`, deliberately, so that the
owner's next reboot measures whether the boot-time start works at all once the
leftover is gone.

## 16 Aug 2026 - Native Win32 semaphores, and the service finally works

Eleventh session, `6755f92`→`ec0d1de`. The owner stated the requirement that
settled the design: **a production system with nobody logged in at the machine,
available to every user from system startup.** That rules out starting SD in a
user session, so session 0 had to work - and POSIX `sem_open()` cannot work
there at all.

**He also asked whether to install a native Windows compiler.** He already has
one: `Makefile:89`, UCRT64 gcc, which builds the client DLL and the service
wrapper. It would not have helped anyway - the failure is the RUNTIME, not the
compiler, and the same source calls `fork()` and `sem_open()` whoever compiles
it. MSVC specifically would force the whole fork→CreateProcess migration up
front with no working baseline, against a 2007 GNU C codebase and a GNU make
build. Recorded because the question will recur.

**What was built.** POSIX named semaphores replaced by Win32 ones in the
`Global\` namespace. `Global\` is the half that lets a session-0 service and a
session-1 user name the same object - a bare name is session-local and would
have reproduced the fault wearing a different hat. They are created granting
SYSTEM, Administrators and `sdusers`, because a default descriptor grants the
creator's token and nothing else, which would start the service and then refuse
every user on the machine *while looking healthy*. `start_sd()` now waits for
`sdwind` to publish its pid: a Win32 semaphore dies with its last handle, so
`sd -start` must not create the set and exit before the daemon attaches - and
it also stops `sd -start` reporting success without ever looking.

**The shared segment was deliberately left on POSIX `shm_open()`.** `sdwind`
reached `get_semaphores()` in session 0, so it had already mapped the segment.
Replacing what is not broken would have widened the change for nothing.

**windows.h could not go in `sdsem.c`, and that is measured rather than
stylistic.** `linuxlb.h` defines `GetCurrentProcessId()` as a nought-argument
macro against w32api's `VOID` form, SD declares its own `Sleep`, and the
`Private` macro expands inside the w32api headers - three compile errors, all
from one include. So `win32sem.c` includes windows.h and **no SD header at
all**, and `sdsem.c` talks to it through `void*` handles. The owner sanctioned
the exception; keeping it to one file with no SD headers is what keeps it
auditable, and PROJECT_STATUS.md 5.4's rule still stands everywhere else.

**Verified, on a fresh install.** Service `Running`, `sdwind` alive at t+30s -
past the ten-second mark that had killed it every time - all six
`Global\sd_sem_716d0302_*` openable, and `adopt-account` reporting `don now has
an SD account`, which closes §7 step 1f. Then the half that had never been
tested and is what the requirement rests on: **from an unelevated session-1
process, a bare `sd` answered `2 DON`** - an ordinary user inside an SD that a
LocalSystem service started in session 0, nobody having typed anything. No
regression either: 11 of 11 on the login rule, `GRANT`/`REVOKE` and
`LIST.GRANTS`, 16 of 16 on `CREATE.ACCOUNT`.

**Still unproven: a RESTART**, which is the last clause of the requirement.
Everything above was measured on the install's own start. The machine is left
with a working install and `assert-current` passing, so it needs no rebuild -
just a reboot and an unelevated `sd`. PROJECT_STATUS header item 1 carries the
three commands.

**Unexplained and left that way: `sdsvc-sd.log` captured nothing**, twice, and
the second attempt fixed a real bug in it (a non-inheritable `NUL` handle,
where `STARTF_USESTDHANDLES` is all-or-nothing) without changing the outcome.
It does not matter while the service works and `sdsvc.log` carries the useful
lines, but **it must not be read as evidence that a child was silent**.

## 16 Aug 2026 - SD will not run under LocalSystem, and sem_open times out saying so

Eleventh session, later the same day, `0bb5e0b`→. The service was taken on as a
fix and turned into a design finding: **SD cannot be started by a LocalSystem
process in session 0 at all**, so no version of `sdsvc.c` can make the 15 Aug
service work. The owner decides what replaces it.

**Three starts on one install, and the third is the control.** The service
(LocalSystem, session 0) leaves `sdwind` dead after ~10 seconds, twice to the
second. A scheduled task as SYSTEM in session 0, **with no service anywhere**,
kills it in the same ~10 seconds. Started from an interactive elevated session
it is alive at 40 seconds and has been all along.

**What it says, once it could say anything.** `sdwind` used to exit 1 or 2 in
silence; with a message added it prints **`sdwind: Error 116 getting
semaphores`**. errno 116 is `ETIMEDOUT` and it means it literally - the probe
`sem_open` at `sdsem.c:82` **blocks for about ten seconds and times out**. That
is the entire ten-second lifetime, and it means **`sdwind` never reaches its
main loop**: a note earlier in this session reasoning about `check_lost_users()`
and `sleep(60)` was analysing code that never runs. It looks alive because it is
sitting in `sem_open`.

**It is not a cross-session problem, and a claim that it was is withdrawn.**
An earlier probe concluded "a session-0 service cannot serve a session-1 user";
it had raced with `sdwind`'s death and could not tell a refusal from a stale
set. In the deciding probe **both** processes were SYSTEM in session 0 - one
created the semaphores and its own child could not open them. Whether an
ordinary user can attach to a service-started SD is still unknown and cannot be
asked until SD survives in session 0.

**Four wrong turns, all from the same habit - inferring a mechanism instead of
measuring it.** `CREATE_NO_WINDOW` was removed as a candidate cause and changed
nothing. A first `sdwind` check asked whether the process EXISTED and was
satisfied 500ms in by one already exiting, which made the service report RUNNING
*and* skip its own cleanup. Two runs of child-output capture produced an empty
file that read exactly like a silent program. And "a failing session-1 sd kills
the daemon" fitted three observations and was killed by one control that ran no
`sd` at all.

**What was fixed and is worth keeping whatever is decided.** `sysseg.c`:
`start_sd()` never checked `fork()`, so a `-1` fell into the parent branch and a
failed start reported success - upstream's too, `UPSTREAM_FIXES.md` #3, along
with the silent daemon. `sdwind.c` says why it will not start. `sdsvc.c` waits
for `sdwind` to *survive* rather than appear, watches it afterwards instead of
sleeping on `INFINITE`, logs to `ProgramData\SD\sdsvc.log`, and runs `sd -stop`
behind a failure. Measured result: `shm` empty afterwards and `adopt-account`
reporting the honest `SD has not been started` instead of `Error 116`. **A
failed service no longer breaks the machine**, which it did all morning -
including taking out the installer's own account step.

**Still open:** the service itself. Candidates, none tested - a service under a
normal local account rather than LocalSystem (needs an account with a password,
so the owner must make it); no service at all, starting SD in a user session as
before 15 Aug; or finding what times out inside the MSYS2 runtime, where
`cygserver` is the usual answer to IPC that works interactively and not as a
service. **§7 step 1f stays regressed** until the service is settled - the
installer gives the installing user no SD account, now for the honest reason
that SD is not running.

## 16 Aug 2026 - The cycle ran: four of five pass, and the service is the one that does not

Eleventh session, `a60b76b`→. The tenth session handed over three pieces written
and never run. All three now work; the fourth thing it wrote, the service, does
not.

**The installer would not build, and had not for a session.** `sd.iss:560`:
ISPP reads any line whose first non-blank character is `#` as a preprocessor
directive, so the wrapped Pascal constant `#13#10#13#10` aborted the compile
with `Unknown preprocessor directive`. The 15 Aug service message pushed that
constant onto its own line and `sd.iss` was never compiled again before the
handoff. Joined to the line above; ISCC then compiled in 3.9 seconds. The cycle
script aborted before uninstalling, which is the only reason the machine still
had a working SD to fall back on — ordering that deliberately.

**Test (a): the service reports `Running` and starts nothing.** `Get-Service SD`
Running / Automatic / LocalSystem with `sdwind` absent, on the install and again
after a restart of it. It is not inert: `sd -start` creates the segment and six
semaphores as `NT AUTHORITY\SYSTEM` and leaves them, and every later `sd` then
dies `Error 116 getting semaphores` (`sdsem.c:121`, errno 116 = ETIMEDOUT)
rather than `SD has not been started`. **It broke the install as it happened** —
`adopt-account.log` shows the installer's own account step failing the same way,
so a fresh install left `don` with no SD account and §7 step 1f regressed.

**A wrong conclusion, corrected inside the same session.** A probe running
`sd -start` as SYSTEM through `cmd /c ... > file 2>&1` produced no `sdwind`, and
this was written up as "`sd -start` does not work as LocalSystem in session 0".
It does. Run as SYSTEM in session 0 through `Start-Process` with **no
redirection**, `sdwind` came up fine. The failing probe had redirection in it,
which is the §6 trap about `sdwind` inheriting the caller's handles - so the
probe tested the trap, not the service. **The fault is in how `sdsvc` launches
`sd`**: `CREATE_NO_WINDOW`, or the minimal environment a service inherits from
the SCM (`sdsvc.c:119` passes `NULL` for environment and working directory).
Untested, and it needs a fresh install because only a real service reproduces it.

**Two defects worth fixing whatever the cause turns out to be.** `sdsvc.c:196`
checks only that `CreateProcess` succeeded and never reads `rc` — and checking
the exit code would not have helped, because `sd -start` exits reporting
success; the honest test is whether `sdwind` is running. And `sdwind` cannot say
why it died: `sdwind.c:71-91` exits 1 or 2 with no message, discarding the
`errmsg` that `get_semaphores()` just filled in. Its exit code still
discriminates - 1 shared memory, 2 semaphores.

**Tests b, c, d and e all pass** (§4). The login rule 5 of 5, including
`14 SDSYS from DON`; `LIST.GRANTS` with two adjacent member lines, no CR and no
blank line, on a fresh install rather than a hand-recompiled `OS_GROUP`;
`CREATE.ACCOUNT` 16 of 16; and the uninstaller removing the service while
keeping the 3,486-file data tree.

**A testing lesson banked, because the harness lied first.** The first run of
the b/c/d tests reported three passes that were not: "bare sd lands in DON"
matched the word DON inside `Account DON not in register`, and both
`LIST.GRANTS` format checks passed vacuously on zero member lines. **A check
whose subject never appeared must report NOT MEASURED, not PASS** - a blocked
test otherwise reads as a working one, which is the same class of error as
measuring against a stale tree. The harness now distinguishes the three states.

**Still open:** the service, and §7 step 1f with it. The machine has no SD
installed - test (e) took it off, which is where a cycle starts.

## 15 Aug 2026 - Header item 2 closed, and the SH gate turns out never to have touched programs

Tenth session. Everything that can be verified on one machine now has been, so
the next subject is §7 step 2, the second machine.

**The install was stale before any of it could start, and that is the ordinary
case.** The ninth session left `C:\Program Files\SD\usr\bin\sd.exe` at 09:58 and
hash-identical to `bin/sd.exe`; five commits between 10:32 and 11:54 — three of
them C source — made it stale by lunchtime, while PROJECT_STATUS still said it
was current. So the cycle began where the owner's rule says it does: `make sd`,
`stage.py --force --bootstrap`, ISCC, uninstall, delete both trees, install,
re-apply the ssh block by hand. Installed and built `sd.exe` then hashed the
same, `81594E79CC2B560C`. The item now carries the one-line hash check instead
of a date to be trusted.

**2b — an ssh session lands inside SD.** `ssh sdacct6@localhost whoami`
answered SD's banner and a `:` prompt, exit 0, with `whoami` never running.
`verify-createaccount.ps1` cannot make that measurement: it accepts *either*
proof of admission by design, because it has to run either side of
`allow-ssh-groups.ps1`. `CREATE.ACCOUNT USER sdacct6` was 16 of 16 on the way,
and `scp` to that account was measured dead — exit 255, `Received message too
long` — which the `changelog` had asserted and nobody had watched.

**2c — `SH` sets `SD_SESSION`, and it took three runs for a reason worth
keeping.** `SH Get-ChildItem Env:SD_SESSION` printed `SD_SESSION 1`. But
`SH sd --version` printed **nothing at all**, which reads exactly like a command
that never ran. It had run and had refused: `sd.c:301` prints that refusal with
`fprintf(stderr,` and the harness captured only stdout. `Get-Command sd` inside
the same child resolved correctly, so it was never a PATH problem. The refusal
was then watched on both child paths, including `sh(FALSE)` — the identical one
the `SH` verb uses — rather than being inferred from the captured variant.

**The owner's question turned §7 step 7 around.** He pointed out that BASIC
programs run OS commands and act on the result, `EXECUTE ... CAPTURING`. Step 7
had said a `SH` a program can call but a person at a prompt cannot is "a
distinction that does not exist today". It does, and always has:
`OS.EXECUTE ... CAPTURING` is its own statement, `BCOMP:9647` emitting
`OP.SHCAP` straight into `op_sh.c`, and **neither `kernel(K$ADMINISTRATOR,-1)`
nor `!valid_shell_cmd` is anywhere on that path** — both live only in `CPROC`'s
`os.command:` handler, which is the TCL verb. Measured unelevated with the
control that makes it mean something: in one session `SH` at the `:` prompt was
refused `Command requires administrator privileges`, and a program in `don`'s
own BP ran `OS.EXECUTE 'echo SDMARKER-OK' CAPTURING` and printed the result
back. The form that *does* break is `EXECUTE 'SH ...' CAPTURING`, which routes
through TCL. What is left of step 7 is only the elevated console prompt.

**A defect found by reading the closing dialog, which compiling never would.**
It ended by offering `net localgroup sdusers <name> /add` for somebody who
already has a Windows account. That cannot work — `sdusers` grants access to the
files, login needs a linked SD account, so such a user meets `Account X not in
register`, which is precisely the symptom `don` had before step 1f. Owner's
decision: drop the lines rather than document `ADOPT`, which stays undocumented.
`sd.iss:493`, with a `changelog` entry. **Correction to PROJECT_STATUS §7 step
3 while there: its "nobody has seen the closing dialog" was wrong — the owner
has, and had screenshotted it.** The `AllowGroups` subtask is still unseen and
cannot be seen on this machine, being hidden by `Check: SshServerAbsent`.

**Two traps banked.** MSYS2 `python` given `gplbld\stage.py` with a backslash
mis-resolves `sys.path[0]` and dies `No module named 'bootstrap'`, which reads
as a missing file; forward slash fixes it, and it would have cost a round trip
in the elevated window that is the only place staging runs. And a stdout-only
test harness sees SD's refusals as silence, which is the trap above generalised:
the gate under test is the output most likely to be on stderr.

**Still open:** `sdacct6` is left in place as step 1c's test subject, password
`Sd-Test-1`; the staged tree and installer are one commit stale, carrying the
old dialog until the next rebuild.

**LATER THE SAME SESSION — §7 step 2 ran, on a VirtualBox guest.** The owner
had a Windows 11 instance on this machine, which is the second machine the step
had been waiting on since 14 Aug. Clone taken, snapshotted `Before SD install`,
NIC switched to bridged — NAT will not do, because the host has to open a
connection *to* the guest.

**The install half was clean first time.** `sd.exe` sha256 `81594E79CC2B560C`
and the counts 19 / 3,456 / `gcat` 130 / `GPL.BP.OUT` 191, all identical to the
build machine, on a guest with no MSYS2, no `gplsrc` and no development tree.
`COUNT VOC` answered 431. The installer's own account step ran there too. So
the staged tree really is self-contained, which is the claim step 2 existed to
test and which nothing on the build machine could have established.

**The RDP half cost most of an hour, and none of it was SD.** Three connection
attempts failed for rig reasons: the guest's network was classified Public, so
the Remote Desktop firewall rules did not apply; and beneath that, **nothing
was listening on 3389 at all** even though `fDenyTSConnections` was 0, no Group
Policy overrode it, and `TermService` was Running. `TermService` builds the
listener when it starts and cannot be restarted, so enabling RDP under a
running service does nothing until a reboot — while the Settings toggle,
the registry value and the service state all read as correct. `netstat -an |
findstr 3389` was the only honest check and should have been the first thing
asked for. Both are now §6 traps, along with `mstsc` prefilling the username
from the *host*, which would have silently turned the treatment into a repeat
of the control.

**Then it passed, control and treatment.** `CREATE.ACCOUNT USER sdacct7` on the
guest, which SD put in `sdsshonly`; from the host, `VIRTUAL\don` **admitted**
and `VIRTUAL\sdacct7` **refused** with `The connection was denied because the
user account is not authorized for remote login` — the deny right's own
wording, not a credentials failure. §5.6.2 is complete.

**THE SESSION ENDED HERE, WITH SOURCE FINISHED AND NOTHING TESTED.** Credits
ran out before the cycle could run. Three things were written and never
executed — the login rule, the service, and the `LIST.GRANTS` carriage-return
fix — and PROJECT_STATUS header item 1 is the cycle plus the order to test
them in. Nothing is half-applied; the tree builds.

**The sequencing rule was broken twice, and is now enforced rather than
remembered.** CLAUDE.md has required since 15 Aug that a test cycle begin with
a fresh install. It says when a cycle *begins* and said nothing about what
*ends* one, and that gap was enough: "install, start testing, edit source, keep
reading results" passes it while measuring a tree that no longer exists. Both
failures were that shape — `sd.iss` edited after the installer was built with
the run in flight read anyway, and `GPL.BP/OS_GROUP` hand-recompiled into the
installed tree with `LIST.GRANTS` then measured on it. The owner asked whether
more was needed to make the rule absolute; the answer was yes.
`gplbld/assert-current.ps1` now answers one question — does the installed tree
match source — and `verify-createaccount.ps1` refuses to run without it.
**Hashing `sd.exe` is not sufficient and that is the whole point of its second
check**: run against the tree at the time it reported the binary MATCHING and
five source files newer, which is exactly the case a binary-only guard waves
through. `verify-sshonly.ps1` and `verify-allowgroups.ps1` are exempt — they
test Windows behaviour, not SD, and run on machines with no install.

**NOBODY LOGS IN TO AN ACCOUNT BUT THEIR OWN** — owner's rule, replacing what
§5.6 had said since 14 Aug. An administrator has access to all accounts *once
they have logged into SD, not before*, so entry is always your own account and
`LOGTO` moves you, which is where the grant is tested and where elevation
already passed everything. Two things let somebody stand in an account without
ever standing in their own, and both are gone from `GPL.BP/LOGIN`: an elevated
session with no account named went to SDSYS, and `-A<anyone>` skipped the
`ACC$GROUP` test when elevated. `-INTERNAL` stays exempt because during a
bootstrap there is no account to land in and nothing to `LOGTO` from — and if
that exemption is ever broken, nothing can be built or installed at all.

**SD RUNS AS A SERVICE, and it is a separate native program for a reason worth
keeping.** A service must call `StartServiceCtrlDispatcher`, and `sd.exe` is
built against the MSYS2 POSIX runtime where `linuxlb.c` records a deliberate
decision to keep `windows.h` out — `IsElevated()` uses `getgrouplist()` rather
than `GetTokenInformation()` precisely so that it need not. Adding a service
entry point to `sd.exe` would have overridden that in passing. §5.3 already
keeps two toolchains on purpose, so `gplsrc/sdsvc/sdsvc.c` is built with the
UCRT64 compiler beside the client DLL; `objdump` shows only ADVAPI32, KERNEL32
and UCRT, no `msys-2.0.dll`. It sits in its own directory because `SRCS` is
`$(wildcard *.c)` over `gplsrc`, which would otherwise compile Win32 code with
the POSIX flags. The installer creates it **before** the account step, so
`adopt-account.ps1` finds SD already up and the race that cost an install
earlier the same day has nothing left to lose.

**Three owner corrections, each a contradiction already sitting in the
source**: `ADOPT` was named in the installer's failure dialog, the one place in
the product documenting a verb §7 step 1f says stays undocumented; `-internal`
was listed in the `changelog` among the gated switches although `sd --help`
does not publish it; and the closing dialog told the user to run `sd -start`
and `sd -ASDSYS`, both wrong once SD is a service and login is your own account
only.

**LATER STILL — §7 step 5, the GRANT verb.** `GPL.BP/GRANTA` serves `GRANT
<account> TO <user>`, `REVOKE <account> FROM <user>` and `LIST.GRANTS
<account>` from one program behind three VOC entries. 16 of 16 on a fresh
install, with every SD-side claim checked against `Get-LocalGroupMember`
afterwards — the point of the step being that SD writes nothing to its own
record. `!os_group` gained `LISTMEM`; `ACC$USERS` went in 5d's order, the
`USERS` column out of `ACCOUNTS.DIC^@` first, and `LIST ACCOUNTS` survived it.
Field 4 is deliberately not reused: records written 13–14 Aug still carry a
grant list there and an installed tree is never upgraded.

**Only (f) is left, and it is blocked on step 4** — the audit record has
nowhere to be written until the audit file exists.

**Three things the owner corrected or caught, all of which stood in the source
contradicting decisions already recorded.** `ADOPT` was printed by the
installer's failure dialog, the one place in the product documenting a verb
that §7 step 1f says stays undocumented; it now names `adopt-account.ps1`,
which ships beside `sd.exe` and is the same code path. `-internal` was listed
in the `changelog` among the gated switches, and `sd --help` does not publish
it — nor `-restart`, `-cleanup`, `-suspend`, `-resume`, `-d` or `-m`, all of
which that entry also named, while claiming *every* switch, which was wrong
anyway because `-P -C -N -Q` are deliberately ungated. And he flagged a build
check reporting "the fix did not land" — my check, not the fix: it grepped the
whole file and matched the comments explaining the removal.

**Two defects found only by running it.** `LIST.GRANTS` blank-lined every
member, because PowerShell ends lines CRLF and `trim()` takes spaces but not
the carriage return — which also made `OS_GROUP`'s own promise that a `LISTMEM`
name can be fed back to `DELMEM` false, since a CR fails `!valid_os_name`. And
the installer gave the installing user no account, reporting `code 3`:
`adopt-account.ps1` looked for `sdwind` once, immediately after `sd -start`
returns, and `sd -start` forks the daemon and returns before it is in the
process table. That race had been won on every previous install and was lost
with a VM running. Both now in §6, together with the same trap one level up —
`Start-Process <setup> -Wait` never returns, because the installer's own
account step starts `sdwind` and it inherits the handles.

**A documentation defect worth more than the code it sat beside:** `stage.py`
described `NEWVOC` and `VOC_TEMPLATE` **backwards**, and those two lines are
the first thing anyone adding a verb reads. `VOC_TEMPLATE` is the
administrative superset that becomes SDSYS's VOC; `NEWVOC` is what `CREATEA`
copies into each new account. The difference is access control —
`CREATE.ACCOUNT` and `DELETE.ACCOUNT` are in one and not the other — so a new
administrative verb put in `NEWVOC` on the strength of that comment would have
been handed to every account SD creates.

**Left dirty, deliberately and recorded:** the installed tree carries a
hand-recompiled `OS_GROUP`, so it is not a clean install; and the staged tree
and installer predate four source changes. Both are in the header.

**A correction inside this: `LogonUser` cannot test the RDP path.** A probe row
written this session asked for logon type 10 and read the `87
ERROR_INVALID_PARAMETER` back as a finding. There is no logon type 10 for
`LogonUser` — `RemoteInteractive` is an LSA audit value — so the row said
nothing about SD. It does confirm the step's premise: RDP is only observable by
making a real RDP connection, which is why a second machine was required rather
than merely convenient.

---

## 15 Aug 2026 - Step 1f built, and ADOPT's first run locked the owner out of his console

Eighth session. `gplbld/adopt-account.ps1` gives the installing user an SD
account; `sd.iss` calls it from `[Code]` at `ssPostInstall` rather than `[Run]`,
because a `postinstall` entry runs as the original unelevated user - one of the
three reasons the old SDSYS password step never worked. The script starts SD if
it must, judges on the `ACCOUNTS` record rather than the exit status, and puts
the machine back as it found it.

**The verb ran for the first time and made the account - and confined `don` to
ssh.** `CREATEA` applies the ssh-only restriction as the `else` of the
`ADMINISTRATOR` keyword, so an adopted account, which is by definition the
installer's and an administrator's, went into `sdsshonly` and its two
deny-logon rights. He kept the session he was in; the next sign-out would have
taken his console and RDP both.

**Owner's rule, stated when it surfaced: no administrator account carries a
lockout risk.** An OS administrator created outside SD has no SD account at all;
one created inside SD must be able to log into the machine and into SD. So
`CREATEA` now skips the restriction for an adopted account and for anyone
Windows already calls an administrator.

**That second test could not be asked before today.**
`Get-LocalGroupMember -Group "S-1-5-32-544"` answers "Group ... was not found"
while `-SID` returns the members, so `!is_grp_member` took its no-such-group
path and answered false for every administrator, silently. Fixed to use `-SID`
for a SID-shaped group, which `!os_group` already accepted.

**Both fixes then compiled and verified on this machine**, by running the same
verb again minutes later: `ADOPT sdadopt1`, a throwaway Windows account, printed
"keeps the Windows sign-in rights it already had" and `sdsshonly` was left
holding only `sdacct4`/`sdacct5`. `don` restricted before, `sdadopt1` not after,
nothing else changed. Two more branches fell out for free: `ADOPT` on a name
with no Windows account refuses with "Invalid user name", and `sd` typed
unelevated put `don` in his own account, `WHO` answering `5 DON` - which is step
1f working for a real person, and also shows the rewritten `IS_GRP_MEMBER` still
admits him through the `sdusers` gate.

## 15 Aug 2026 - Step 1f closed on a real install, and three new access rules

End of the eighth session, `4f28a27`..`207dd9c`.

**The installer gives its user an SD account, proven by installing.**
`gplbld/adopt-account.ps1` runs `CREATE.ACCOUNT USER <installer> ADOPT`;
`sd.iss` calls it from `[Code]` at `ssPostInstall`, not `[Run]`, because a
`postinstall` entry runs as the original unelevated user. It took two failures
to get there and both are worth keeping:

- **`ADOPT` confined the owner to ssh.** `CREATEA` applied the ssh-only
  restriction as the `else` of `ADMINISTRATOR`, so an adopted account - the
  installer's, an administrator's - went into `sdsshonly` and its deny-logon
  rights. Owner's rule: no administrator account carries a lockout risk.
  `!is_grp_member` could not have tested for it either, because
  `Get-LocalGroupMember -Group` refuses a SID; it takes `-SID`.
- **The step then failed on a real install and said nothing.** `$PSScriptRoot`
  is EMPTY in a param default when a script has `[CmdletBinding()]` and a
  mandatory parameter, so `-AppDir` was empty and PowerShell exited 1 before
  touching SD. Every run by hand had passed `-AppDir`, so only an install could
  show it. The script now logs to `<DataDir>\adopt-account.log` and the
  installer passes `-AppDir`.

**Three rules from the owner, all built:** nothing may be typed after `sd`
without elevation - switches *and* a bare command, since `sd LISTF` ran for
anybody; every ssh session lands in SD through a global `ForceCommand`,
administrators included, with console and RDP untouched; and SD refuses to
start inside itself, `op_sh.c` marking the shell and `sd.c` reading the mark.
`-P -C -N -Q` are deliberately ungated: SD spawns itself with them.

**And a correction to that work, from the owner:** "an SD account has no
shell" was false - `SH` hands one back - and it had been offered as the reason
the second-instance guard need not be a boundary. His answer is a menu system
inside SD; restricting `SH` is undecided.

**The machine was rebuilt from nothing** and now runs the repository: uninstall,
delete both trees and every test account, re-stage, ISCC, install. 3,455 files,
`gcat` 130, and the installed catalogue carries the owner's banner - the first
time this machine has run what the repository says.

## 15 Aug 2026 - Rebuilt, reinstalled, and step 1d proven on the install

Eighth session, after the two entries below. Re-staged with the ACCOUNTS/SDSYS
fix (3,471 files, `GPL.BP.OUT` 191 objects, dev tree untouched), ISCC at 06:47
(4,795,558 bytes), installed. `C:\Program Files\SD\usr\bin` is now the 06:23
build; the data tree was left alone as designed, so the installed catalogue is
still the sixth session's and the corrected one waits in the stage for a clean
machine.

Step 1d then re-run against the installed binary, every branch: `already
started` naming pid 14980 with `Get-Process` agreeing; daemon killed and segment
left, `sd -start` exit 1 telling the user to run `sd -stop`; `sd -stop` exit 0
emptying `shm` silently; `sd -start` back up as 7388. Left running.

One new trap: `sd -start` hangs a shell whose stdout is a pipe even when sd's
own output goes to a file - `sdwind` inherits the shell's pipe too.

## 15 Aug 2026 - The bootstrap was compiling the development tree

Eighth session, found by running the first elevated `stage.py --force
--bootstrap` and reading its output. `ACCOUNTS/SDSYS` field 1 is the SDSYS
account directory and the tracked record names `/usr/local/sdsys`, so after
login `GPL.BP`/`GPL.BP.OUT` resolved to the Linux dev tree while `gcat` came
from the config file: 190 objects written there, catalogued into the stage,
staged `GPL.BP.OUT` left with the 12 that `sd -i` and `bbcmp.py` write directly.

**The owner's own banner edit is what caught it** - he had changed
`GPL.BP/LOGIN:175` days earlier, and the staged `gcat/$LOGIN` printed the old
line, matched the dev tree's but for 3 bytes, and had no `sdusers` literal in
it. That is a pre-step-0 LOGIN, in a tree that was one command from being
installed. Every staged tree so far has been built this way; it never showed
because the dev tree's programs work and because the critical ones were
recompiled by hand on the installed system afterwards.

Fixed in `stage.py` (point the record at the staged tree before the bootstrap,
retarget to production after) and `bootstrap.py` (`check_account_record`
refuses a mismatch, tested both ways). `check_no_stage_paths` was passing
vacuously for the same reason - the embedded path was the dev tree's.

Also closed: the elevated half of the elevation check. Both gates passed in an
elevated window and the bootstrap ran through, `SECOND.COMPILE` 0 errors.

## Correction: 15 Aug 2026 - the install, the stage and the installer were dated wrong

Eighth session, by listing the files. The install is 14 Aug **19:05** (the
table said "CURRENT, 16:15" in one row and 19:05 in the next); `stagetest` is
**19:14, 3,287 files**, not 16:15/3,285; the installer is **19:15,
4,776,555 bytes**, not 16:17/4,771,110; the installed tree is **3,412** files,
not 3,270. Nothing decided on them changes - 19:05 still predates the 21:29
build carrying step 1d. **Date artefacts, do not remember them.**

Also: SD is **not running**, and `C:\ProgramData\SD\shm` holds the segment and
six semaphores from 14 Aug 21:58 - the stale-segment state, free test of the
step 1d fix once a new binary is installed.

## 15 Aug 2026 - The bootstrap refuses an unelevated window

Eighth session, from `317ad58`. The bootstrap's four `sd -internal` steps stand
in SDSYS, which has needed elevation since 14 Aug, and nothing said so:
unelevated it failed at `SECOND.COMPILE`, minutes in. `bootstrap.py` now
refuses at the door; `stage.py` imports the same test for `--bootstrap`, which
otherwise copies thousands of files first.

The test is `544 in os.getgroups()`, `IsElevated()`'s own (`linuxlb.c`). MSYS2
Python is a Cygwin build with no `ctypes.windll`, so the group route is the only
one available there anyway; the `os.name == 'nt'` branch is for a native Windows
Python. Not fixed by exempting `-INTERNAL`, which would restore the 13 Aug
bypass.

Watched unelevated: a nonexistent `--sysdir` draws the elevation refusal rather
than `no such sysdir`, so the check is genuinely first; `stage.py --bootstrap`
leaves no staging directory; `--help` works; without `--bootstrap` it reaches
its `objdump` check. **Nobody has seen the check pass** - that comes with the
rebuild.

## 14 Aug 2026 - Step 1c runs; user-visible Linux-isms swept

Seventh session, after the entry below. All five programs compiled `0 error(s)`
and catalogued; no `is not assigned a value`, so `K$INTERNAL` and messages
10036-10039 resolve. Run from an elevated console:

- `CREATE.ACCOUNT USER don` refused with message 10038. Was `Create User
  Failed, OS Error: 1`.
- `DELETE.ACCOUNT sdacct1` took the "no such Windows account" branch, removed
  the directory and the record. **First run of DELETE.ACCOUNT in this
  codebase.** Checked after: `sdacct4`/`sdacct5` users and `sdu_` groups
  untouched.

Untested still: the "SD created it" delete branch, and `ADOPT`.

**Linux-isms, found by the owner from `LIST ACCOUNTS` output.** The `ACC$GROUP`
column heading read `Linux Group`. Fixed in
`gplbld/FILES_DICTS/ACCOUNTS.DIC^GROUP`. **The repository holds no dynamic
files** - they are built at install time, which is what keeps it auditable
(CLAUDE.md) - so a dictionary is edited in the repository and never patched in
an installed tree. Swept the rest at the same time: messages 2004 and 6075 both
said "Linux" and neither has a caller; reworded. `grep -i linux` over
`sdsys/MESSAGES` and `gplbld/FILES_DICTS` is now clean.

## 14 Aug 2026 - DELETE.ACCOUNT decided and built, and two more helpers found reading /etc

Seventh session of 14 Aug 2026. **PROJECT_STATUS §7 step 1c is decided and
written; none of it has been compiled**, which is the first thing to know about
everything below.

**The decision, from the repository owner.** DELETE.ACCOUNT offers to delete
the Windows account only when SD created it. The provenance question turned out
to have an answer already sitting on disk: CREATE_USER stamps every account it
creates with the description "SD account", so nothing new is recorded and
existing accounts answer without migration. Measured on this machine -
`sdacct5` reads exactly `SD account`, 10 characters, and `don` reads empty.

**It is a marker and not a proof**, and the failure is deliberately one-sided:
an account whose description somebody edited is reported as not SD's, so it is
left alone and a human tidies it. The opposite mistake deletes a real login.
Litter is recoverable; a deleted account is not.

**THE PREMISE I HAD WAS WRONG, AND THE OWNER CORRECTED IT MID-BUILD.** I read
CREATEA lines 145-151 as "CREATE.ACCOUNT adopts an existing Windows user", and
started fixing `!is_user` so that the adopt branch would work. The owner's
rule: **the only pre-existing OS user that may be given an SD account is the
installer's, and after that every SD user's OS account is created from within
SD.** So the adopt branch is not something the model wants at all.

**That correction landed on a genuinely dangerous change.** `!is_user` read
/etc/passwd, which MSYS2 does not have, so it answered false for every user;
the adopt branches never ran; CREATE.ACCOUNT fell through to create_user(),
which fails on an existing account. The verb therefore **refused a pre-existing
user - the correct behaviour - entirely because a helper was broken**, while
reporting it as "Create User Failed, OS Error: 1". Repairing the helper on its
own would have brought the adopt branches to life and turned that refusal into
a silent adoption of somebody's existing Windows login. The general form is now
in section 6: **when a fix makes a helper answer correctly, check what its
callers were relying on it getting wrong.**

**So the rule was written into CREATEA in the same change as the fix.** The two
adopt branches are gone and replaced by an explicit refusal (message 10038).
The single sanctioned exception is a new `ADOPT` keyword, gated on `K$INTERNAL`
rather than `K$ADMINISTRATOR` - so `sd -internal`, which means the bootstrap
and the install, can use it and an administrator at a console cannot. That
distinction is the whole point: every elevated session is an administrator, but
only the install is internal.

**THE THIRD MEMBER OF A FAMILY, AND THE FAMILY IS NOW CLOSED.** `!is_grp_member`
had this same /etc defect, was found in the sixth session when it refused every
login with "not registered for SD use", and was fixed - alone. `!is_group` and
`!is_user` had it too and nothing connected them, because the symptoms were
unrelated: DELETE.ACCOUNT silently never removing an account's sdu_ group, and
CREATE.ACCOUNT's misleading refusal. `grep -rn 'openpath "/etc"' GPL.BP` now
returns nothing.

**Two smaller things in the same change.** The `config('CREATUSR')` gate is
gone from DELACC, which was its last caller and unblocks step 1a. And the
ACCOUNTS record is deleted **last** instead of first: it used to go first, so
anything failing afterwards left a group or an OS account with no register
entry pointing at it, and DELETE.ACCOUNT could not be re-run because it starts
by reading that record.

**What was measured, and it is all PowerShell rather than BASIC:** the absence
of /etc/passwd and /etc/group under both roots; the marker on sdacct5; and the
three answers is_sd_user must distinguish, against real accounts - sdacct5 as
SD's, `don` as **not** SD's, sdacct1 as absent. That last row is the one that
matters: DELETE.ACCOUNT would refuse to touch the machine administrator's
login. **The transport was proved by SD's own artefact** - a quoted value
containing a space survives os.execute, which nothing had shown before and
which is_sd_user depends on.

**What is open.** None of the BASIC is compiled; ERRGEN makes an undefined
$define a compile-time warning and a run-time abort, and K$INTERNAL and
messages 10036-10039 are new references. The installer's SD account is decided
but only half built: the ADOPT door exists, nothing calls it, and `don` is
still refused at his own machine.

## Correction: 14 Aug 2026 - a blank Path is not an elevation test, and it was written into PROJECT_STATUS as one

Seventh session of 14 Aug 2026, correcting commit `653e016`, which recorded
that the `sdwind` daemon left running at the end of the session (pid 4696) had
been **started elevated**, and gave as its evidence that an unelevated session
could not read the process's `Path`.

**The claim was wrong and the evidence was not evidence.** Four daemons were
started during the day: the two started from an elevated window had an
unreadable `Path`, the two started unelevated did not. That correlation was
taken for a test. The fifth, pid 4696, has a blank `Path` **and** grants
`OpenProcess(PROCESS_TERMINATE)` to an ordinary session - which an elevated
process cannot do, and which the orphaned pid 5080 had refused with
`Access is denied` an hour before. So 4696 is stoppable without elevation, and
the row said the opposite.

**Why it matters more than the fact itself.** The claim was written as
"evidence for the elevation:", i.e. presented as measured, in a file whose §0
rule 2 exists to stop exactly that. It also had a practical edge: a session
reading it would have believed an ordinary `sd -stop` could not stop SD, and
would have raised a UAC prompt it did not need.

**Why `Path` is blank is still unknown**, and the correction does not depend on
knowing: the process's own shell reads its `Path` fine, the daemons started by
a tool session read fine, and this one does not. Recorded as unexplained rather
than guessed at.

**The replacement is to ask for the right you care about.** "Can this session
stop that process" is `OpenProcess(PROCESS_TERMINATE)`; §6 carries the
one-liner. **This is the third instrument in this project to be wrong** -
after `Measure-Object -Line` undercounting the file, and a UAC registry reading
that had gone stale within a session - and all three failed the same way: they
answered a question next to the one being asked.

## 14 Aug 2026 - The EPERM warning fired, and the first attempt to test it tested the wrong binary

Seventh session of 14 Aug 2026, closing the one branch the entry below left
unwatched. **PROJECT_STATUS §7 step 1d is now fully observed.**

**The false start, which is the part worth reading.** The recipe written into
the PROJECT_STATUS header named
`C:\Program Files\SD\usr\bin\sd.exe`, with "install the new binaries" listed as
the job *before* it - so it read as runnable on its own. Run that way it
exercised the **19:05 build, which has none of this work in it**: elevated
`-stop`, elevated `-start`, then `sd -stop` in an ordinary `cmd` window, which
printed `SD (64 Bit) has been shut down` and said nothing else. **That is
indistinguishable from the fix failing**, and it is what the reader would
reasonably have concluded.

It was not wasted: it is the defect reproduced on a real console, where the
fourth session's observation of it was the only one before. `sdwind` was left
running as pid 13840 with `C:\ProgramData\SD\shm` **emptied** - the segment
goes and the daemon stays, which is also why no later `sd -stop` can reach such
a daemon.

**The real run.** Elevated
`& 'C:\Users\dmont\Projects\sdb_ai_windows\sdb_ai\sd64\bin\sd.exe' -start`,
then the same full path with `-stop` from an ordinary PowerShell window:

```
Warning: sdwind (pid 5080) is still running.
It belongs to a session with more privilege than this one, so it could not be
signalled.
Stop it from an elevated session with "Stop-Process -Id 5080 -Force" before
starting SD again, or the machine will run two daemons.
SD (64 Bit) has been shut down
```

**Three confirmations, and the third was not designed for.** `Get-Process
sdwind` answered **5080**, so `win_pid()` translates in the stop path as well
as the start path. `C:\ProgramData\SD\shm` was **empty**, so the teardown still
happened - the warning is a warning and not a failure, which is what step 1d
asked for. And `Stop-Process -Id 5080` **from that same unelevated session was
refused `Access is denied`**, so the message's account of *why* it could not
signal is corroborated by a different mechanism rather than being SD's guess.

**The general form, and it belongs with the instrument entries above.** A test
recipe that names a path names a *binary*, and an installed binary is only the
current one immediately after an install. **Write the full path to the build
under test**, and when a test reports nothing, establish which binary answered
before concluding anything about the code.

**Left on the machine:** `sdwind` 5080, orphaned and elevated, with SD stopped.
Clearing it needs an elevated `Stop-Process`; PROJECT_STATUS carries it.

## 14 Aug 2026 - sd -start and sd -stop stop lying about sdwind, and the fix was not where the step said it was

Seventh session of 14 Aug 2026, from commit `5800942`. **Closes PROJECT_STATUS
§7 step 1d**, except for one path that needs an elevated window and one that
cannot be fixed at all.

**What was wrong.** Both commands answered from *objects* rather than from
*processes*. The shared segment and the semaphore set outlive the processes
that create them, so `sd -start` said "SD is already started" off a segment
whose daemon had been killed - leaving the system unusable while the command
that would fix it reported success - and `sd -stop` threw away `kill()`'s
return value, so an unelevated session that could not signal an elevated
daemon printed "SD (64 Bit) has been shut down" and left it running.

**What was built**, all in `gplsrc/sysseg.c` unless said otherwise:

- `sd_state()`, which attaches the segment, checks `sysseg->sdwind_pid` with
  `kill(pid, 0)` - treating `EPERM` as a yes, because a process you may not
  signal is still a process - counts live sessions in the user table the same
  way, and answers `SD_STOPPED` / `SD_RUNNING` / `SD_WRECKAGE`. It reads
  nothing past `revstamp` unless the revstamp is this build's, so a segment
  from another build is left to `bind_sysseg`'s own mismatch message.
- `start_sd()` calls it *before* `bind_sysseg()` and reports accordingly.
- `stop_sd()` keeps the pid, checks `kill()`'s result, treats `ESRCH` as the
  outcome it wanted, waits for the daemon **in the liveness poll** - which had
  always walked the user table only, the other half of why nothing noticed -
  and warns afterwards, distinguishing "could not be signalled" from "did not
  stop when asked".
- `win_pid()`, wrapping `cygwin_internal(CW_CYGWIN_PID_TO_WINPID, pid)`.
- `gplsrc/sdsem.c`: the leftover-semaphore message no longer says "SD is
  already started".

**THE FINDING THAT MATTERS MOST: the step named the wrong file.** §7 step 1d
pointed at `sysseg.c` line 503 and at `bind_sysseg`'s `"SD is already started."`
The string the broken machine actually produced was **`sdsem.c` line 86's**,
which has no full stop, because `get_semaphores(TRUE)` runs before the segment
is looked at. A fix confined to the two places the step named would have left
the behaviour exactly as found. **The control run is what caught it** - running
the *old, installed* binary against the live wreckage first, and reading the
message closely enough to notice the missing full stop.

**THE OTHER FINDING: SD's pids are MSYS2 pids.** The daemon called itself
**pid 87**; `Get-Process sdwind` called it **14712**. Everything SD holds is
the runtime's numbering. This is not cosmetic in a message that says "stop this
process": `Stop-Process -Id 87` does not fail, it acts on an unrelated Windows
process. Hence `win_pid()`. It answered 14712 against the live daemon, matching
`Get-Process` exactly. **`sysdump.c` line 95 still prints the untranslated
number.**

**What it cost, and the luck in it.** The machine was found already sitting in
the broken state - segment and all six semaphores present under
`C:\ProgramData\SD\shm`, no `sdwind` process - left there by the sixth session.
So the lie and its repair were watched **on the same wreckage**, an hour apart,
rather than on a reconstruction.

**Deliberately not done: `sd -start` does not clear the wreckage for you.**
Sessions can still be attached to a segment whose daemon has died, and an
`sd -stop` would end them, so the count of live sessions is printed and the
person at the keyboard decides. Revisit only with a reason.

**What is still open.**

- ~~**The `EPERM` warning has never been watched.**~~ **Watched later the same
  session — see the entry above this one.** Left here struck through rather
  than edited out, because the entry either side of it describes work done
  while it was true.
- **A third face of the same defect cannot be fixed where the others were.**
  Measured by unlinking the segment under a live daemon: `sd -stop` printed
  success, exit 0, and left `sdwind` running. `sysseg->sdwind_pid` is the only
  record of the daemon's identity, so with the segment gone there is nothing to
  signal and no way to know there was anything to signal. The answer, if it
  ever matters, is a **pid file beside the segment** rather than a field inside
  it.

**Also in this session.** The sign-on banner in `GPL.BP/LOGIN` was changed to
"SD for Windows..." and lost its "(AI modified)" note - an edit found
uncommitted in the working tree, finished with its `START-HISTORY` line and a
changelog entry. And PROJECT_STATUS was brought inside all three of §0 rule 5's
budgets for the first time since the rule was written: header 271 -> 179 (limit
200), §7 310 -> 258 (limit 300), whole file 3,659 -> under 3,500. The step 0
material was compressed in §4 and §7 as rule 5 prescribes, and the §5.6.1
weighing below was moved here.

## 14 Aug 2026 - Moved from PROJECT_STATUS §5.6.1: the password model's login and LOGTO rules

Moved verbatim in the seventh session of 14 Aug 2026 under §0 rule 5, step 0
having been built over it. `logto.step.up` and `ACC$USERS` are both deleted;
what replaced them is at the top of PROJECT_STATUS §5.6. Kept because it is the
only full statement of how the 13 Aug 2026 password model decided access, and a
future session asking "was a step-up prompt ever tried?" deserves the answer.

> `LOGIN` sets `@logname` to the authenticated account and sets
> `K$ADMINISTRATOR` on entry to SDSYS. **Two deliberate ways in without a
> password**, both gated on `K$ADMINISTRATOR` (which comes from the OS via
> `IsAdmin()` and cannot be self-granted): an administrator running an internal
> command, which is the install path since the bootstrap cannot type a password;
> and an account with no password yet, with a warning. So a half-configured
> system is not an open one.
>
> **How `LOGTO` decides.** `CPROC`'s `logto.authorised` runs immediately after
> the ACCOUNTS read, where the deleted `ACC$GROUP` test used to sit. The early
> `K$ADMINISTRATOR` test at the top of `int.logto` is gone — it asked whether the
> caller was already privileged, which is the wrong question when entering SDSYS
> is what confers privilege. In order:
>
> 0. **The target must be a registered account name.** Anything not in ACCOUNTS
>    is refused before authorisation is considered.
> 1. An administrator running an internal command is admitted, as at `LOGIN`.
> 2. **A session standing in SDSYS may enter any account**, no grant needed.
> 3. Otherwise you may enter your own account, or one whose `ACC$USERS` names
>    you. Refusal is `sysmsg(10003)` and the session stays where it was.
> 4. Entering SDSYS additionally runs `logto.step.up`: three tries at **your own**
>    password through `!CRED_VERIFY(@logname, ...)`, with `PT$INVERT` and the
>    input prompt character cleared around the read (§6).

## Correction: 14 Aug 2026 - the UAC slider had moved back, and a recorded reading went stale within a session

Seventh session of 14 Aug 2026. The sixth session recorded, as a correction,
that `ConsentPromptBehaviorAdmin` read **0** and `PromptOnSecureDesktop` read
**0** - the owner having moved the UAC slider to "Never notify" mid-session.
Read again in the seventh session, they are **5 and 1**: back at the Windows
default.

**Nothing about the access model turns on it**, and that was the point of the
sixth session's entry too: token filtering is `EnableLUA`'s doing, `EnableLUA`
is 1 in both readings, and `IsElevated()` answers false in an ordinary
administrator's session either way.

**What it changes is what a session can arrange for itself.** At 5 and 1 an
elevation request raises a consent prompt on the secure desktop, so the
elevated half of a test is something the person at the keyboard has to do, not
something a session can quietly arrange. That is why the `EPERM` half of step
1d is still unwatched.

**The general form, and it is the same shape as the `Measure-Object` entry
above: a machine setting is not a fact about the machine, it is a reading with
a timestamp.** Anything a user can change with a slider should be re-read in
the session that depends on it.

## Correction: 14 Aug 2026 - the line-count "correction" was itself wrong, and the instrument was the cause

Sixth session of 14 Aug 2026. **This entry reverses the entry below headed
"Correction: 14 Aug 2026 - PROJECT_STATUS said it was ~3,190 lines; it was
2,729"**, recorded earlier the same session in commit `ca6e13b`. That entry
stays where it is, per rule 1 — but **do not act on it**, and note that the
command it recommends at the end is the broken one.

That commit claimed the fifth session's figure of "about 3,190 lines" was an
unchecked estimate, and that PROJECT_STATUS really measured 2,729. **The fifth
session was right.** Measured properly:

| Commit | Recorded in the file | Real count |
|---|---|---|
| `2890198` | 2,924 | **2,925** |
| `c99f927` | "about 3,190" | **3,188** |

**Every figure the earlier sessions wrote down was accurate to within a line or
two.** The error was introduced by the tool used to audit them:
`(Get-Content file | Measure-Object -Line).Lines` **does not count blank lines**,
so it undercounts this file by roughly 15%. `.Count` on the array is right.

**The part worth carrying is not the arithmetic.** A wrong measurement was used
to overturn a correct record, the wrong method was then written into
PROJECT_STATUS as the recommended way to measure, and every subsequent session
would have inherited it — each one "confirming" a number that was wrong in the
same direction. It survived three commits and about a dozen re-measurements
inside one session, because re-running the same broken instrument agrees with
itself every time.

**The general form belongs beside §0 rule 2:** *an instrument you have not
checked is not evidence.* Rule 2 asks whether a claim was observed; this asks
whether the thing that did the observing was ever tested. The two failures look
identical from the outside — a confident number, repeated.

**Also corrected in passing:** the section sizes quoted in the header (§6 "812
lines", §4 "456", §5 "887") were undercounts from the same method. Real sizes at
the close of this session are §5 1,006, §6 969, §4 605.

---

## 14 Aug 2026 - Step 0 is CLOSED: all five rules of 5.6 observed end to end

Sixth session of 14 Aug 2026, last entry. **The access model decided in the
fifth session is built, installed and verified.** The remaining two rules were
watched over ssh as `sdacct5`, an ordinary non-administrator SD account created
by `CREATE.ACCOUNT`:

| Typed | Answer |
|---|---|
| `sd` | a `:` prompt, **nothing asked** — no account name, no password |
| `who` | `3 SDACCT5` |
| `LOGTO SDSYS` | `SDSYS Account access is restricted to privileged users` |
| `LOGTO SDACCT1` | `User not allowed in requested account` |

**Both refusals were worth running because they come from different code.**
`LOGTO SDSYS` is stopped by the elevation gate in `int.logto`, above the
ACCOUNTS read; `LOGTO SDACCT1` is stopped by the restored `ACC$GROUP` test in
`logto.authorised`, below it. Between them they cover every branch this session
changed in `CPROC`. The first also **confirms step 0f by measurement**: an ssh
session cannot be elevated, so ssh cannot reach SDSYS — the local-only property
the owner specified earlier the same day, tested rather than argued.

`sd` landing in `SDACCT5` with nothing asked is the whole reversal in one line:
the operating system authenticated the user, and SD asked it who they were.

### What it took to get there, which is the part worth reading

The code was written in about an hour. **Everything after that was the
environment**, and none of it was visible from the source:

- `-ASDSYS` instead of `-internal` for the compile, because `BCOMP` gates
  `$internal` on `K$INTERNAL` *and* `K$ADMINISTRATOR` — eleven cascading errors
  that looked like broken source.
- `!VALID_OS_NAME` missing from the bootstrap's pass 1 list, because the
  restored `sdusers` gate made `LOGIN` reach it at first login.
- The bootstrap needing `sdusers`, a group only the installer creates.
- `LIST ACCOUNTS` hanging on the fifth account, because a piped session cannot
  answer a pagination prompt.
- `sd -start` reporting success off a stale shared segment with `sdwind` dead.
- A random 24-character password lost with the run that generated it.

**Five of those six were pre-existing and had simply never been reached.** Only
`VALID_OS_NAME` was caused by this session's own change. A full bootstrap and one
hand-driven login found all of them; nothing short of that would have.

### State at the close

Step 0 is closed and **step 1 is the next subject**, with step 1d promoted:
`sd -start` and `sd -stop` both lie about `sdwind`, this session hit both, and
they share a cause. `DELETE.ACCOUNT` (step 1c) now has **three** half-removed
accounts to decide against — `sdacct1` to `sdacct3`, SD side only — plus two
complete ones left by `-Keep`, `sdacct4` and `sdacct5`. **Nobody knows
`sdacct4`'s password**: it was random, and the run that made it hung before
printing it.

---

## 14 Aug 2026 - The access model is live, and the refusals are observed

Sixth session of 14 Aug 2026, later the same evening. Binaries built, tree
staged and bootstrapped, installer built and run, `LOGIN` and `CPROC` recompiled
against the new binaries. **The reversal decided in the fifth session now
behaves as designed on a real machine.**

### The decisive test

From an **unelevated** session belonging to `don`, a machine administrator:

| Command | Result |
|---|---|
| `sd` | **refused** — `Account DON not in register`, `sysmsg(5018)` |
| `sd -ASDSYS` | **refused** — `SDSYS Account access is restricted to privileged users`, `sysmsg(10002)` |
| `sd -internal BASIC GPL.BP LOGIN`, **elevated** | worked |

**The first row is the whole point.** An hour earlier that same command put
`don` straight into SDSYS, because the installed binary still seeded
`K$ADMINISTRATOR` from `IsAdmin()`. **And `sysmsg(10002)` fired for the first
time in this codebase's history** — PROJECT_STATUS §5.6 had recorded it as a
message that existed and had never had a caller.

Four of §5.6's five rules are now observed. The two outstanding need a second
account to exist, and creating one needs elevation.

### Two bugs the bootstrap caught, which nothing else would have

**1. `!VALID_OS_NAME` was missing from the pass 1 compile list.** `SECOND.COMPILE`
logs in; the restored `sdusers` gate makes `LOGIN` call `!IS_GRP_MEMBER`, which
calls `!VALID_OS_NAME`; that had never been compiled at that point, so the
bootstrap died at `000000D7: Unable to load '!VALID_OS_NAME' object code` before
compiling anything, and left the staged tree not installable. **Caused by this
session's own change**, and invisible until a full bootstrap ran. One line in
`GPL.BP/BBPROC`. The general rule is now a trap in §6: **anything `LOGIN` calls
becomes a bootstrap dependency.**

**2. The bootstrap started needing `sdusers`, which only the installer creates.**
Circular — building the product would have required a group that installing it
produces, so a clean build machine could not bootstrap at all. **Owner's
decision, 14 Aug 2026: exempt internal mode from the `sdusers` gate.** It opens
no hole: `sd -INTERNAL` names SDSYS for itself in `sd.c`, and SDSYS requires
elevation, so an internal caller has already passed a strictly harder test.

### The bootstrap-elevation trap, measured

§6 predicted the bootstrap would need elevation once `K$ADMINISTRATOR` meant
elevated. **It does.** Unelevated, `sd -i` answered
`Command requires administrator privileges`; `stage.py` reported
`the bootstrap failed; the staged tree is not installable` and, usefully, said
so rather than producing a broken artefact quietly. The same command from an
elevated window completed: 3,286 files, 10.4 MB, everything `0 error(s)`.

**A process note worth keeping:** the first staging attempt was run through
`| tail`, so the shell reported exit 0 — `tail`'s status, not `stage.py`'s. The
failure was visible only by reading the output. **Do not judge a staged tree by
an exit code that passed through a pipe.**

### Installer behaviour, confirmed rather than assumed

Setup found the existing database and **left it alone**, saying so in a dialog:
*"the newly built system files were NOT installed over it"*. That is §6's
staleness trap behaving as designed and now visible to the user, where it once
cost a full day of investigation. **The consequence to remember: an install
updates `C:\Program Files` and not `C:\ProgramData\SD\sdsys`**, so `LOGIN` and
`CPROC` had to be copied across and recompiled by hand afterwards.

### Left open

`WARNING: GRANT.POS is assigned a value but never used`, emitted when `CPROC`
compiles **inside the staged tree** and not when the identical file compiles on
the installed tree. `grant.pos` does not exist in the source — the staged copy
is md5-identical to the repository's and the token appears nowhere in `sdsys`.
It belonged to the deleted `ACC$USERS` grant list. Benign, and written up in §6
with the test that would settle it. **Two explanations were offered for it
during the session and both were wrong**; it is recorded as unexplained rather
than explained badly.

---

## 14 Aug 2026 - LOGIN and CPROC compile, 0 errors each, and the new login is running

Sixth session of 14 Aug 2026, in an elevated window driven by the repository
owner. **The first time either program had ever been through a compiler.** Both
returned `0 error(s)` and were catalogued; `gcat/$LOGIN` moved from 16:15:56 to
18:54:15 and 5,319 bytes, checked as written rather than as reported.

### The invocation, because getting it wrong cost a round trip

The first attempt used **`-ASDSYS` and a pipe**, and produced 11 errors in
`LOGIN` and roughly eighty in `CPROC` — `Unrecognised compiler directive` on
`$internal` and `$flags trusted`, `Misformed $CATALOGUE`, then
`Expected / after common block name` through every include. **None of it was the
source.** `BCOMP` gates the `$internal` directive on `K$INTERNAL` *and*
`K$ADMINISTRATOR`, so standing in SDSYS is not enough — which is written in
`gplbld/bootstrap.py` line 189, in a file read earlier in the same session. With
internal mode off, the directives are rejected and everything downstream
cascades.

**The right form is `-internal` with the command as separate arguments**, as
`bootstrap.py` line 214 does it:
`sd.exe -internal BASIC GPL.BP LOGIN`. No pipe, so no BOM — the piped attempt
also had the first two characters of `CATALOG` eaten and ran `TALOG`. `CATALOG`
is not needed separately; the `$catalog` directive writes `gcat`.

**Nothing was catalogued by the failed attempt**, so the machine was never in a
broken state. A `gcat.before-step0` backup had been taken first regardless.

### The behavioural evidence arrived sideways

The `LOGIN` compile printed `Warning: account SDSYS has no password set.` The
`CPROC` compile, one command later, **did not** — that line lives in the deleted
`authenticate.account`, so its disappearance dates the changeover precisely. And
the `CPROC` compile then succeeded *through* the new `LOGIN`, which means **the
`sdusers` gate admits a member** and **the `K$FORCED.ACCOUNT` branch reaches
SDSYS**. `!is_grp_member` working at login matters on its own: §6 records the
day it returned false for everybody and terminated every connection.

**This is the permissive half only.** The installed `sd.exe` is still the
14 Aug 16:15 binary seeding `K$ADMINISTRATOR` from `IsAdmin()`, so no refusal
has been tested and none can be until the new binaries are installed.

### One warning, and it exposed something else

`PRIVILEGED_COMMANDS is assigned a value but never used`. **Not caused by the
edit.** Its only consumer sits inside `$ifndef IS_INSTALL` at `CPROC` 1466 and
1479, and `define_install.h` reads `$define IS_INSTALL` both in the repository
and at `C:\ProgramData\SD\sdsys\GPL.BP\define_install.h`. `CPROC`'s own header
says *"The install script overwrites this file with IS_INSTALL commented out,
and CPROC will be recompiled."* **It never did.** So on every installed system
the privilege raise/drop around `$CREATEA` — the `!EUID_RESTORE`/`!EUID_SET`
pair — is dead by preprocessor as well as dead by platform. Written up as a trap
in PROJECT_STATUS §6.

### Correction: the machine's UAC policy moved mid-session

§4 recorded `ConsentPromptBehaviorAdmin = 5`, measured in the fifth session. It
now reads **0**, with `PromptOnSecureDesktop = 0` — the owner moved the UAC
slider to "Never notify" during the session, in the belief that it would let
this agent issue elevated commands. **It did not, and that was measured:** the
session still reports `elevated: False`, `S-1-5-32-544` is absent from the
process token, and `id -G` returns no 544. The slider does not clear
`EnableLUA`, which is what creates the split token, so a process must still
*request* elevation — it simply is not prompted now.

**`EnableLUA = 0` would break the model**, collapsing `IsElevated()` into
`IsAdmin()`, putting every administrator into SDSYS always, and making SDSYS
reachable over ssh against the local-only decision. **And it would make step 0e
meaningless**, because the refusal half of the test could never fire and would
record false passes. Noted here because the intent behind the change was
helpful and the reasoning is worth keeping.

---

## 14 Aug 2026 - Grants are Windows group membership; ACC$USERS is dead

Sixth session of 14 Aug 2026, immediately after the access-model build. Decision
from the repository owner, settling the one consequence that build left open.

**Entry to an account is membership of the Windows group named in its
`ACC$GROUP`.** `CREATE.ACCOUNT` already writes `sdu_<name>` and puts the
account's own user into it, so granting somebody a *second* account is adding
them to that group and nothing else. The operating system holds the grant.

**This kills `ACC$USERS`**, the multivalued grant list added on 13 Aug 2026 as
part of the account-password model. It was already authorising nothing after the
access-model build — `logto.authorised` asks the group now — so this decision
turns "dead code nobody has decided about" into "dead code with a removal
order". PROJECT_STATUS §7 step 5 carries that order, and it matters: the
dictionary item and the records must go before the `$define` in `SYSCOM/KEYS.H`,
or `LIST ACCOUNTS` breaks while passing through the intermediate state.

**What the verb becomes.** `GRANT <account> TO <user>` and
`REVOKE <account> FROM <user>`, over `!os_group`'s `ADDMEM` and `DELMEM`. That
subroutine already exists, is idempotent, and already returns status 5
specifically for "not elevated" rather than a localised Windows error string, so
the work is argument parsing and messages rather than new machinery. The step
also picks up two things that were not obvious until the grant moved into the
OS: **listing who may enter an account stops being something a dictionary item
can show** and needs a new `LISTMEM` action, and **a granted user cannot use the
grant until they sign out and back in**, because group membership is fixed in
the access token at logon. The second is the most confusing property of the
whole model and the verb is where it should be explained.

### Correction folded in with it

`SYSCOM/KEYS.H` line 263 carried a comment reading *"ACC$GROUP is dead; SD no
longer consults operating system groups"*. **True for exactly one day.** `LOGIN`
and `CPROC` both depend on that field again as of the access-model build, so the
header was telling the next reader the opposite of what the code does. Corrected
in the same commit, and `ACC$USERS`'s define now says it is dead rather than
describing what it used to do.

---

## Correction: 14 Aug 2026 - PROJECT_STATUS said it was ~3,190 lines; it was 2,729

Sixth session of 14 Aug 2026. PROJECT_STATUS's header claimed the file had gone
"back up to about 3,190" lines after the fifth session wrote the access-model
reversal into it. **Measured at commit `c99f927`, it was 2,729** — the estimate
was made while editing and never re-checked, and it survived into the very
commit titled "State the line count the next session will actually see".

Harmless in itself, but it is the §0 rule 5 trigger that decides whether a
session spends its time on a rollover instead of on the work, so an inflated
figure costs a session. **Measure it:**
`(Get-Content PROJECT_STATUS.md | Measure-Object -Line).Lines`.

---

## 14 Aug 2026 - The Linux access model is built: no password at login, elevation for SDSYS

Sixth session of 14 Aug 2026, carried by the commit this entry ships in. It
implements the reversal that the fifth session decided and did not build —
PROJECT_STATUS §7 step 0, parts a to d. **The C compiles clean. NOTHING HAS BEEN
RUN**, for a reason that is itself one of the findings below.

### What changed

| Where | What |
|---|---|
| `gplsrc/linuxlb.c` | **`IsElevated()` added beside `IsAdmin()`.** `IsAdmin()` is untouched |
| `gplsrc/kernel.c` | `USR_ADMIN` seeded from `IsElevated()` instead of `IsAdmin()`, so `K$ADMINISTRATOR` means **elevated** |
| `gplsrc/sddefs.h` | comment only: `SD_ADMIN_GID` now has two callers asking two different questions |
| `GPL.BP/LOGIN` | the three `f9edab0` cases restored; `authenticate.account` **deleted**; no password is asked for anywhere |
| `GPL.BP/CPROC` | `logto.step.up` **deleted**; `ACC$GROUP` test restored in `logto.authorised`; `LOGTO SDSYS` requires elevation; the `system(27) = 0` block removed outright |

**`IsElevated()` needs no Win32 call**, which was the one design choice here.
§7 step 0a offered `GetTokenInformation(TokenElevation)` or the "deny only"
marker. It is neither: it is `getgroups()` against `SD_ADMIN_GID`, the exact
call `IsAdmin()` was moved *off* on 14 Aug. §5.6.1 had already measured both in
one unelevated administrator session — `getgroups()` no, `getgrouplist()` yes —
so the elevation test was a measured fact sitting unused in the file, and using
it keeps `windows.h` out of a POSIX-runtime translation unit (§5.4).

### Two findings that would have cost a session each

**1. `ACCOUNTS/SDSYS` carries `ACC$GROUP = sdsys`, and no such Windows group
exists.** Restoring the group test verbatim, as step 0b says to, **would have
refused SDSYS to everybody including an elevated administrator**. On Linux
`sudo sd` ran `!EUID_SET('sdsys')` in `CPROC` *before* `LOGIN`, so `@logname`
became `sdsys` and `!is_grp_member`'s "is this your own group account?"
shortcut (`IS_GRP_MEMBER` line 83) matched. Windows has no effective-user drop,
so `@logname` stays `don` and the shortcut cannot fire. **An elevated session
therefore skips the group test in both `LOGIN` and `logto.authorised`** — which
is Linux behaviour anyway, since root is not in the group either. Measured, not
assumed: the record was read off disk, `C:\ProgramData\SD\sdsys\ACCOUNTS\SDSYS`
= `C:\ProgramData\SD\sdsys`, empty, `sdsys`.

**2. `K$ADMINISTRATOR` now means elevated, and `BCOMP` gates `$internal` on it.**
So **compiling any `$internal` program now requires an elevated session**, and
that includes `bootstrap.py`, which runs `sd -internal SECOND.COMPILE`
(`gplbld/bootstrap.py` line 192). `sd -INTERNAL` names SDSYS for itself in
`sd.c`, so it goes through the new elevation gate. This is not a defect in the
model — leaving `-INTERNAL` outside the gate would restore exactly the bypass
the 13 Aug session removed — but **the bootstrap now needs an elevated shell and
nothing says so yet.** `bootstrap.py` line 195 records that the *previous* login
change broke this same path and "Nobody noticed because nobody had re-run the
bootstrap since."

### What it cost, and what could not be checked

**`gplbld/bbcmp.py` cannot compile `LOGIN` at all** — it aborts with "VOID
statement not coded". This was checked properly rather than assumed: HEAD's
unmodified `LOGIN` was compiled as a control and **failed identically** (line
204 against the modified file's 210). So the Python compiler is not a syntax
checker for these two programs; SD's own `BCOMP` is, via `SECOND.COMPILE`, and
that now needs elevation. **This is why nothing is verified.**

### Still open

- **`ACC$USERS` no longer authorises anything.** The grant list built on 13 Aug
  is still written, still shown by `LIST ACCOUNTS`, still editable by
  `MODIFY ACCOUNTS`, and is now consulted by nothing. §7 step 5 ("give grants a
  verb") was written against it and needs re-deciding: under §5.6 the grant *is*
  membership of the account's `sdu_` group, so the verb may be an OS-group edit.
  **Existing grants silently stop working**, which is in the changelog.
- **`sysmsg` 10030 and 10031 have no caller**, as do `$CRED`, `!CRED_SET`,
  `!CRED_VERIFY` and `SET.PASSWORD` — the last four deliberately, per the
  owner's decision that the API keeps a password (§8).
- **`CPROC` line 1481 still calls `!EUID_SET('sdsys')`** to drop back after a
  privileged command, paired with `!EUID_RESTORE`. Same dead Linux mechanism as
  the block removed at line 280, left alone because it is outside step 0.

### Decision recorded the same session: elevation is local by design

From the repository owner, 14 Aug 2026: administrators having **less** remote
access is intended. To elevate you must be local to the machine — sitting at it,
or on a secure remote client that gives a real interactive desktop session, such
as AnyDesk. **This settles §7 step 0f and inverts it.** The question was "does
elevation work over ssh, and is it acceptable if it does not"; it is now "confirm
ssh cannot reach SDSYS", and if it can, that is a gap to close rather than a
feature to keep. It sits consistently with §5.6.2: ordinary accounts arrive over
ssh, the console belongs to administrators.

---

## Correction: 14 Aug 2026 - Windows CAN limit sudo, and the password model was built on the belief that it could not

Fifth session of 14 Aug 2026, after the rollover. **No code changed.** This
entry records a decision from the repository owner that reverses the identity
model in PROJECT_STATUS 5.6, and — more usefully for anyone reading cold — the
mistaken belief that produced 5.6 in the first place.

### The belief, and where it came from

PROJECT_STATUS 5.6.1 said of `sudo` on Windows: *"It has no sudoers file and no
per-command policy - it asks UAC to elevate your own token."* Every word of
that is true of `sudo.exe`. It was read as **"Windows cannot limit who may
elevate"**, and the consequence drawn was that mimicking the Linux access model
would give every user on the machine access to SDSYS.

In the owner's words, 14 Aug 2026: *"The reason we got off on another track is
because I had taken away the impression that we could not mimic the linux
access process because of differences between linux and windows. That was my
lack of understanding. My understanding was that access to sudo could not be
limited on Windows (no sudoers group), which would give everyone access to
SDSYS."*

**That belief is why SD grew account passwords.** 5.6's "every account carries
its own password", decided 13 Aug 2026 and built across two sessions -
`$CRED`, `!CRED_SET`, `!CRED_VERIFY`, `SET.PASSWORD`, the `LOGIN` password
prompt, `logto.step.up`, commit `272ce92` "Require an account password at
login" - exists to replace a control that was thought to be missing and was
not.

### The measurement that closed it

Read off this machine's live policy, fifth session:

| Setting | Value | Meaning |
|---|---|---|
| `EnableLUA` | 1 | UAC on, tokens filtered |
| `ConsentPromptBehaviorUser` | 3 | **a standard user is prompted for an ADMINISTRATOR's credentials** on the secure desktop |
| `ConsentPromptBehaviorAdmin` | 5 | an administrator gets a consent prompt only |
| `LocalAccountTokenFilterPolicy` | not set | default remote restriction applies |

A standard user **cannot elevate as itself**. It can only elevate by supplying
someone else's administrator credentials, which it does not have. So:

| | Linux | Windows |
|---|---|---|
| who may become root | listed in sudoers | member of `Administrators` |
| a normal account tries it | not in sudoers, refused | prompted for credentials it has not got |
| an administrator tries it | in sudoers, password | consent prompt, elevated |

**`Administrators` is the sudoers file, and SD has been maintaining it all
along** without anybody noticing that was what it was doing:
`CREATE.ACCOUNT USER x` leaves x out of it, `CREATE.ACCOUNT USER x
ADMINISTRATOR` puts x in (verified 14 Aug 2026, fourth session).

And the distinction the model needs is readable. In an ordinary unelevated
window belonging to `don`, who is in `Administrators` in the SAM:

    Elevated now: False
    BUILTIN\Administrators   Alias   S-1-5-32-544   Group used for deny only

**This is the same fact 5.6.1 measured on 14 Aug with a C probe and read the
other way.** That session compared `getgroups()` against `getgrouplist()`,
found that only `getgrouplist()` sees `Administrators` in an unelevated
session, and concluded that `getgrouplist()` was the *right* answer and
`getgroups()` the wrong one. The measurement was correct; the conclusion was
half of one. They are two useful tests: `getgrouplist()` answers "is an
administrator" and gates `sd -start`, the token answers "is elevated right now"
and gates SDSYS.

### What the Linux version actually does

Confirmed twice: the owner tested it in a Debian virtual machine with SD
installed, and it is in this repository's own pre-port `LOGIN` at commit
`f9edab0`, lines 185-270, which is the specification to build from.

    if not(is_grp_member(lgn.id,'sdusers')) then     -> 5009 not registered for SD use
    case kernel(K$FORCED.ACCOUNT,0) # ''             -> sd -Aname
       IF initial.account = "SDSYS" and not(K$ADMINISTRATOR) -> 10002 restricted to privileged users
       if not(is_grp_member(lgn.id,acc.rec<ACC$GROUP>))      -> 10003
    case kernel(K$ADMINISTRATOR,-1)  ;* user id 0, "sudo sd"
       initial.account = "SDSYS"                     -> dropped straight into SDSYS
    case 1                            ;* Must be console
       initial.account = upcase(@logname)            -> the linked account, by name

**No password prompt anywhere in that path.** The OS has authenticated you; SD
asks it who you are. Typing `sd` puts you in the SD account with your own name
and nowhere else; no such account means no login; `sudo sd` puts you in SDSYS.

The owner had forgotten the third of those and re-derived it from the VM:
*"If you have sudo access, you login with sudo sd and are automatically placed
in the SDSYS account (I had forgotten that part)."*

There is also a fifth rule nobody had recorded: **`sd -Aname` for another
account was gated at login by `is_grp_member(you, acc.rec<ACC$GROUP>)`** - the
account's own OS group - separately from `LOGTO`.

### Correction: `ACC$GROUP` is not dead

PROJECT_STATUS 5.6.1 recorded `ACC$GROUP` as "dead but still populated on old
records". **Wrong.** `CREATEA` line 455 writes it on every new account as
`sdu_<name>`, and `CREATE.ACCOUNT` creates that Windows group. Only the code
that *read* it was deleted, on 13 Aug 2026.

That makes the restoration much smaller than it looks. The write side of the
Linux model was never removed:

| Piece | State |
|---|---|
| `ACC$GROUP` = `sdu_<name>` | written on every account, `CREATEA` 455 |
| the `sdu_<name>` Windows group | created by `CREATE.ACCOUNT`, verified |
| `sdusers` membership | added, `CREATEA` 345 |
| `!is_grp_member` on Windows | works, verified 7 of 7 |
| messages 5009, 5018, 10002, 10003 | all present; **10002 has never had a caller** |

### The decision

**Mimic the Linux version.** The owner, asked whether to keep the password
machinery and which mechanism should gate account entry, answered both the same
way: *"I would prefer to mimic the linux process if available on Windows."*
Since the elevation control exists, it is available.

**The credential machinery is kept, and this is the part that stops it being a
demolition.** Asked whether `$CRED` should be deleted outright, the owner
answered that **the API is a separate door and still needs a password**: *"the
gate in linux is that the api goes through an ssh tunnel and does not have
access to the server without an account password."* So `$CRED`, `!CRED_SET`,
`!CRED_VERIFY` and `SET.PASSWORD` change owner rather than dying - off the
console, onto the API.

That also corrects PROJECT_STATUS 8, which had reasoned that because the API is
piped through ssh (posture B, settled 14 Aug 2026), ssh had already
authenticated the user and peer identity would be enough. **Two gates, not
one.** Which password is still open: Linux uses the OS account's, through
`login_user()` reading `/etc/shadow`, which MSYS2 does not have.

### The risk that is left, and it fails closed

`LocalAccountTokenFilterPolicy` is not set, so the default UAC remote
restriction applies and a local account logging on **over the network gets a
filtered token**. 5.6.2 makes SD accounts ssh-only, so an SD administrator
arriving over ssh may be unable to elevate, and so unable to reach SDSYS
remotely. **Untested.**

Worth being precise about the direction: the feared failure was that everybody
would get SDSYS. This is the opposite - an administrator gets *less* than
expected, nobody gets more. So it does not block the work. It may also simply
be the design, since 5.6.2 already gives the console and RDP to administrators
and ssh to everyone else.

### What is not done

**Nothing is built.** PROJECT_STATUS 7 step 0 is the whole of the work and the
next session should start there and do nothing else first, because it changes
`LOGIN`, `CPROC` and `kernel.c` and several later items are written against the
model it replaces. Nothing was added to `sdsys/changelog` either: login
behaviour changing is exactly what rule 8 covers, but the behaviour has not
changed yet, and the changelog entry belongs in the commit that changes it.

## 14 Aug 2026 - PROJECT_STATUS rolled over from 4,112 lines

Fifth session of 14 Aug 2026, starting at commit `33495e0`. **The only subject
was the rollover** that §0 rule 5 had been calling for since 13 Aug 2026, and
which the fourth session had named as the most overdue item in the file and as
"a job for a session that starts with it rather than one that reaches it".

**No code changed. Nothing was built and nothing was tested.** No claim moved
between §4 Verified and §4 Unverified in either direction, and nothing that had
been observed was deleted. This entry exists so that a future session can tell
what was cut from what was never there.

### What it achieved, and what it did not

**4,112 lines to 2,924 — 29%, and still above the ~2,000 limit.** That is
recorded honestly in the file's header rather than glossed, because the next
session inherits it. Where the remainder sits:

| Section | Was | Now |
|---|---|---|
| header (before §0) | 340 | 147 |
| §0–§3 | 309 | 247 |
| §4 Verified / Unverified | 828 | 456 |
| §5 Decisions | 1,169 | 887 |
| §6 Traps | 882 | 812 |
| §7 Next steps | 173 | 155 |
| §8 Open questions | 410 | 219 |

**§6 is now the largest section and the main remaining candidate.** It was
compressed — several entries re-narrated how the trap was found, which HISTORY
already carries — but **no trap was removed**, and none should be: §0 rule 4
makes them the highest-value part of the file. Taking §6 below about 600 means
reading every entry against its HISTORY counterpart, which is a session's work
on its own and was not attempted here.

**§4 was cut hardest** and is now claim, decisive measurement and nothing else.
The 13 Aug 2026 foundations — the binaries building, the IPC probes, the shared
segment lifecycle, the bootstrap, the credential round trip, the `LOGTO` suite,
the drive-letter fix, the data tree needing no C source, the staged tree running
with MSYS2 off PATH — became a table of one-line claims, each naming the HISTORY
entry that carries it. Nothing there was contradicted; it was superseded as a
*headline* by the installed system running end to end, which is a different
thing and is why the claims were kept rather than deleted.

Two §4 entries were merged rather than trimmed, because the later one strictly
covers the earlier: "THE STAGED TREE INSTALLS AND RUNS" was dropped in favour of
"A GENUINE FIRST INSTALL WORKS", and the earlier ssh-only proof was folded into
the `CREATE.ACCOUNT` 16-of-16 entry, which measured the same three things on an
account SD created rather than one a test harness made.

### One correction to the file, made in passing

§7's step numbering was rewritten. Steps 1, 2 and 3 had been "finish the install
layout", "finish the OS account work" and "build the staging script then the
installer" — **all three are done**, and step 1's own text had said so in three
places while still standing at the top of the list. They are replaced by the
loose ends that actually remain. **Steps 4 to 13 keep their old numbers**,
because the rest of the file refers to them by number; the four cross-references
that pointed at the old 1, 2, 3 and 0 were repointed rather than left dangling.

### Archived here because it had no other home

Three blocks were carried out of PROJECT_STATUS verbatim. Everything else that
was cut was a second copy of something this file already held.

---

#### 1. The development-tree machine state, as it stood 13 Aug 2026

Removed from §3, where it described a tree that is no longer how the system is
reached — the installed tree at `C:\ProgramData\SD` is. **The scratch account
passwords below are real and were still set when this was archived.** Delete
those accounts before that machine is used for anything that matters.

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

---

#### 2. The API exposure question, and the two postures not taken

Removed from §8, where it sat in a `<details>` block under
"SETTLED 14 Aug 2026: the API is piped through ssh — posture B". The decision
stands; this is the record of what was weighed against it.

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

**The installer now offers B as a checkbox** (decided 14 Aug 2026, §5.9):
opt-in, off by default, withheld with an explanation if the machine already
has an ssh server. That does not decide the posture question — it makes B
reachable by someone who would not otherwise know how, which is the case the
repository owner raised: ten people on a local network, installed by someone
with little administrative knowledge. Read §5.9's two caveats before
recommending it, particularly that ssh gives those ten people **no isolation
from each other's data** until §5.7's service model exists.

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

---

#### 3. The `IsAdmin()` / `sdadmins` question, and the two options not taken

Removed from §8, where it sat in a `<details>` block under
"SETTLED 14 Aug 2026: `IsAdmin()` tests Windows `Administrators`". Option 2 was
taken and is written up in §5.6.1. The reason option 1 was rejected is the part
worth carrying and is now summarised in §8: it inherits the
sign-out-and-back-in trap in §6, so `sd -start` would have failed for the
installing user on every fresh install.

**Promoted to the top of this section on 14 Aug 2026.** This was a tidy-up
question with no deadline. It is now the one thing standing between the
installer and a machine that has never had SD on it, so it needs an answer
before the installer can ship.

**What forces it.** `IsAdmin()` (`gplsrc/linuxlb.c` line 75) is
`getgrnam(SD_ADMIN_GROUP)` and returns FALSE when the group is absent, failing
closed by design. `SD_ADMIN_GROUP` is `"sdadmins"` (`gplsrc/sddefs.h` line
131). `sd.c` line 613 refuses `sd -start` with "Command requires administrator
privileges" when it is false. **`gplbld/sd.iss` creates `sdusers` — for the
ACL — and never `sdadmins`.** Nothing in `gplbld/` mentions it. So a clean
machine gets an install in which nobody is an SD administrator, `sd -start`
refuses, and the postinstall `SET.PASSWORD SDSYS` step fails identically. It
works on this machine only because `sdadmins` was created by hand on 13 Aug
2026 and this account's token carries it — the same "leftover state hides the
bug" shape as the `DataTreeAbsent` defect (§4).

**The three answers, and none has been taken.** Adding two `net localgroup
sdadmins` lines to the `.iss` would work, but it decides this question by
accident, which is why it was not done:

1. **Keep an OS-level check on `sdadmins`**, and have the installer create it
   and enrol the installing user, exactly as it already does for `sdusers`.
   Cheapest, and consistent with what the code says today. Note it inherits the
   sign-out-and-back-in trap in §6, so `sd -start` would not work for the
   installing user until they log in again — which for the postinstall
   `SET.PASSWORD` step means it fails on a fresh install every time.
2. **Gate on Windows `Administrators` instead.** Starting a server is an
   administrative act, the group always exists, and it needs no installer step
   at all. It also sidesteps (1)'s re-logon problem, since an elevated token
   carries it immediately. Against it: §5.6 deliberately separated SD
   administration from Windows administration.
3. **Drop the OS check**, and let `sd -start` be gated by file permissions on
   the data tree alone — which the ACLs now genuinely enforce (§4). Most in
   keeping with §5.6, and the largest change.

§5.6 removes the *need* for the group as an identity mechanism, but both it and
`IsAdmin()` are committed (`f56de86`, `9c00730`) and the check runs before any
account exists or any password can be prompted for, so it cannot simply be
deleted: that would leave `sd -start` ungated. Until this is settled, leave
`IsAdmin()` in place.

**Do not delete the `sdadmins` group from this machine** while the question is
open: the token carries it, which is what allows the shipped `sd.exe` to run
`-start` and `-stop` here without the probe build of §6, and it is for the
moment the source of `K$ADMINISTRATOR` for every session (§5.6). Deleting and
recreating it is worse than leaving it — a recreated group has a new SID, which
this token would not carry until the next logon.

## 14 Aug 2026 - AllowGroups applied for real: the lockout did not happen

Fourth session of 14 Aug 2026, last piece of it. `allow-ssh-groups.ps1
-Installed` was run against this machine's live `C:\ProgramData\ssh\sshd_config`
for the first time. Exit 0, `sshd` restarted and came back Running, and the
block landed immediately before `Match Group administrators` — the placement
`verify-allowgroups.ps1` exists to guarantee, now confirmed in the live file
rather than in a copy of the template.

    # --- BEGIN SD ssh-only model - PROJECT_STATUS.md 5.6.2 ---
    AllowGroups sdusers GITORLI\sdusers Administrators GITORLI\Administrators
    # --- END SD ssh-only model ---
    Match Group administrators

**The open question was whether those patterns match anybody**, and §5.6.2 had
warned that getting it wrong locks the machine's own administrator out of ssh.
Answered by control and treatment, with no password handled — `BatchMode=yes`
fails authentication either way, so the *reason* was read out of the
`OpenSSH/Operational` log:

| account | groups | sshd logged |
|---|---|---|
| `don` | `sdusers` + `Administrators` | `Connection reset by **authenticating user** don` |
| `CodexSandboxOffline` | neither, and **enabled** | `not allowed because none of user's groups are listed in AllowGroups`, `**invalid user**` |

So the patterns match, a non-member is refused for exactly the intended reason,
and the administrator kept ssh. `sdsshonly` accounts are members of `sdusers`
too — `CREATEA` adds both — so they are allowed by construction.

### Two things about measuring this that would have gone wrong

**The client cannot tell you the answer.** Both cases produced an identical
`Permission denied (publickey,password,keyboard-interactive)`. A test that
judged on the client's message or exit code would have called the working
configuration broken, or the broken one working. Only the server log
distinguishes refused-by-group from failed-to-authenticate.

**The first control was confounded and nearly passed for evidence.**
`WDAGUtilityAccount` is disabled, and produced a bare `Connection reset` with
no log line at all — a different-looking failure that could as easily have been
the disabled account as the group check. It was redone with an enabled
non-member. Recorded because the confounded version looked like a clean
negative result.

### What stays unknown, deliberately

Which of the four patterns matched. `AllowGroups` is a union and all four were
written on purpose, precisely so the bare-versus-`COMPUTER\` question would not
have to be answered per Windows build. It stays open unless somebody narrows
the list intentionally, and the trade is described in §5.6.2.

---

## 14 Aug 2026 - STEP 0 IS CLOSED: CREATE.ACCOUNT passes 16 of 16, end to end

Fourth session of 14 Aug 2026, third run of `verify-createaccount.ps1`, with
the CRLF fix in place and a fresh account name. **Every check passed.**

    the Windows account exists      PASS      account is enabled           PASS
    member of sdusers               PASS      member of sdu_sdacct2        PASS
    member of sdsshonly             PASS      NOT an administrator         PASS
    message 10034 (ssh only) shown  PASS      account directory            PASS
    VOC / $HOLD / $SVLISTS / BP     PASS      record in ACCOUNTS           PASS
    LogonUser INTERACTIVE           refused 1385     PASS
    LogonUser NETWORK_CLEARTEXT     admitted         PASS
    ssh with the password SD set    admitted         PASS

**This closes the chain the test was written to close.** SD creates the
account, SD restricts it, and the restriction is then shown to hold from
outside — on an account SD created rather than one the harness made for itself,
with a password SD generated and set. `CREATEA` line 400 has run, and §5.6.2 is
now proven at both ends: the mechanism, and the verb that drives it. RDP
remains the only unwatched part, and it needs a second machine.

Two things it settled in passing. `SET_PASSWD` works end to end against a real
Windows account — the password SD set is the one ssh accepted. And a brand-new
account can ssh in **with a password** immediately; only key authentication
waits for a first password login, which confirms that distinction rather than
assuming it.

`Warning unable to setgid bit on Group Folder, status: 1` prints on every
account creation. It is the `sudo chmod g+s` Linux-ism in `CREATEA`, harmless,
and now observed rather than predicted. Its Windows equivalent is the
inheritable ACE the installer already sets.

### What it cost, which is the part worth remembering

Three runs, and **four separate faults, none of them in `CREATE.ACCOUNT`**:

1. the install was four commits stale, and nothing said so
2. a PowerShell pipeline puts a phantom empty line after every command, which
   an `input` statement eats
3. `sd -stop` reported success while leaving `sdwind` running
4. the test asserted `$SAVEDLISTS` and a file count, both wrong

Every one of them presented as "CREATE.ACCOUNT is broken". The verb was correct
throughout. The general lesson is in §6 three times over: date the thing you
are testing, measure how your harness talks to SD before trusting a transcript
of it, and make a test's own assertions as suspect as the code they check.

### Left on the machine

`C:\ProgramData\SD\user_accounts\sdacct1` and `sdacct2`, with their `ACCOUNTS`
records and no Windows account behind them. The Windows side of both is gone.
That is deliberate — removing the SD side is `DELETE.ACCOUNT`'s job and §7 step
1c has not settled what that should do — and it is now two worked examples of
exactly the state 1c has to decide about.

---

## 14 Aug 2026 - The ssh-only branch runs, and the password bug is a CRLF

Fourth session of 14 Aug 2026, immediately after the entry below. The install
was rebuilt and refreshed — 18 files in `C:\Program Files\SD`, 3,268 under
`sdsys`, `MESSAGES/10034` present — and `verify-createaccount.ps1` run again.

**`CREATEA` line 400 executed for the first time.** `sdacct1 may sign in over
ssh only` was printed from message 10034; membership of `sdusers`,
`sdu_sdacct1` and `sdsshonly` all confirmed, `Administrators` correctly absent;
account directory, `VOC`, `$HOLD`, `BP`, private catalogue and `ACCOUNTS`
record all made. That is what step 0 existed to answer and it is answered.

### Two of the four remaining failures were the test's own fault

- It asserted `$SAVEDLISTS`. `CREATEA` prints `Creating $SAVEDLISTS...` and
  creates a directory called **`$SVLISTS`** — the message carries the VOC name,
  the directory carries the DH file name. The account was complete all along.
- The file-count check expected 16 program files. A real install has **18**:
  `unins000.exe` and `unins000.dat` are the installer's and are not in the
  stage. The expected number was wrong, not the install.

Both are worth recording rather than quietly fixing, because both produced a
red FAIL against something that was working, in a test whose entire purpose is
to be believed.

### The other two were one cause, and it was measured rather than deduced

The previous entry declined to conclude that piped input was at fault, because
the echo was demonstrably lossy. That caution was right, and the answer came
from an experiment instead: pipe `AAA` and `BBB` into SD two ways and count the
prompts.

**PowerShell writes CRLF between pipeline objects, and SD treats CR and LF each
as a line terminator.** So an array of commands arrives with a phantom EMPTY
line after every one of them. At the TCL prompt that is invisible — an empty
command reprints the prompt — which is why it survived every scripted session
until one of them hit an `input` statement:

    input pw1 HIDDEN   <- phantom after the CREATE.ACCOUNT line: EMPTY
    input pw2 HIDDEN   <- the real password
    input yn           <- the next phantom: EMPTY, so not Y, so no retry

`pw1 # pw2`, so the password was never set. The account stayed **disabled**,
because `SET_PASSWD` runs `Enable-LocalUser` inside the same script, and all
three logon measurements then failed for want of a password — `LogonUser`
answering 1326 was reporting a missing password, not a deny right. The only
visible trace was a stray `Command not found` on stderr: the second password
falling through to the TCL prompt.

The fix is one string with LF separators rather than an array. `Invoke-SD` in
`verify-createaccount.ps1` now does that; §6 carries the trap and the code.

### A note on the echo, which cost time twice

SD's `[K` erase-line sequences make every line appear twice in a captured
transcript, and can truncate one copy — this run rendered
`CREATE.ACCOUNT USER sdacct1` as `CREATE.ACCOUSER sdacct1` on a line that
executed perfectly. **The echo is not a record of what SD consumed.** Two
sessions in a row tried to read consumption off it; the two-minute experiment
answered it outright.

### Still open

The test has not yet passed. It needs one more run with the CRLF fix and a
fresh account name — the SD side of `sdacct1` is left behind deliberately, so
`CREATE.ACCOUNT` will refuse that name, and the script now says so up front
instead of discovering it after making a Windows account.

---

## 14 Aug 2026 - Step 0 ran, and found that this machine's install is four commits behind

Fourth session of 14 Aug 2026. `gplbld/verify-createaccount.ps1` ran for the
first time, from an elevated window, and reported 14 of 16 checks failed.
**`CREATE.ACCOUNT` is not broken.** The installed system it was pointed at
predates the commit that made `CREATE.ACCOUNT` work.

| | |
|---|---|
| `C:\Program Files\SD\usr\bin\sd.exe` built | 14 Aug 2026 **08:32:44** |
| commit `2fd0aff`, "Make CREATE.ACCOUNT work" | 14 Aug 2026 **09:50:56** |
| `MESSAGES/10032`–`10035` in the installed tree | **absent**, all four |

`2fd0aff` changed `op_dio2.c`, `CREATEA`, `OS_GROUP` and added messages 10032
and 10033; 10034 and 10035 came with the ssh-only branch after it. None of it
is in the installed tree. A `find` of the working tree against the staged tree
returns exactly `CREATEA`, `OS_GROUP` and those four messages — the delta is
that commit and nothing else.

So the run exercised the **pre-fix** `op_dio2.c`, whose `OS_PATHNAME` case
split on `/` alone and rejected every native Windows path, and the **pre-fix**
`CREATEA`, which has no ssh-only branch at all. `Invalid account pathname` is
the symptom the comment at `op_dio2.c:650` was written to describe, down to it
occurring after the Windows user had been created.

### What it did establish

`CREATE_USER` reached the OS from an elevated session and made a real Windows
account. The account was left disabled and passwordless, which is correct
rather than a fault: `SET_PASSWD` runs `Enable-LocalUser` *inside* the password
script, so an account whose password was never set stays inert. `LogonUser`
answering 1326 for both logon types follows from that and says nothing about
the deny rights. Cleanup worked; the machine was left with no `sdacct1`, no
`sdu_sdacct1`, an empty `sdsshonly` and no account directory.

### What is deliberately NOT concluded

The transcript shows `SET_PASSWD`'s first prompt reading empty and the second
reading the password. It is tempting to call that a piped-input defect, and
this entry does not, for two reasons: a session earlier the same day set
passwords through a pipe successfully (`sdtest1`, `sdtest2`) and `SET_PASSWD`
has not changed since 05:51; and the same transcript rendered the command as
`CREATE.ACCOUSER sdacct1`, four characters short, on a line that executed
correctly — so the echo is not a reliable record of what SD consumed.
Re-measure against a current build before diagnosing. Two entries in this file
already correct conclusions drawn from a single unreliable observation.

### The general finding, which is bigger than this test

**A `uninsneveruninstall` data tree does not get upgraded, and nothing says
so.** `sd.iss` skips the whole `sdsys` set when the directory already exists —
deliberately, so an upgrade cannot overwrite a live database — and the
installer says so in a dialog. What nobody had joined up is that this machine
has therefore been running a data tree from 08:32 all day while the repository
moved on, and every test run against "the installed system" since then has been
testing 08:32's BASIC. §5.9 already records that upgrading an existing database
is unsolved and needs a migration story; this is the first time it has actually
cost anything.

---

## 14 Aug 2026 - sd -stop says it stopped the daemon when it did not

Fourth session of 14 Aug 2026, found while clearing up after the hang recorded
below. Not caused by that hang — the hang only put the machine in the state
that exposes it.

`sdwind` had been started by an **elevated** script. `sd -stop` run from an
ordinary session printed `SD (64 Bit) has been shut down`, unlinked the shared
segment and all six semaphores — `C:\ProgramData\SD\shm` was empty afterwards
— and left the daemon running. It was still there, idle, minutes later.
`Stop-Process` on it from the same ordinary session was refused with
`Access is denied`.

That refusal is the mechanism. `sysseg.c` line 503 is

```c
if (sysseg->sdwind_pid > 0)
  kill(sysseg->sdwind_pid, SIGTERM);
```

An unelevated process signalling an elevated one gets `EPERM`. The return value
is discarded, and the liveness poll immediately below it walks the **user
table** only — it has never waited for `sdwind` — so nothing notices and the
success message is printed unconditionally.

**§4's verification of `sd -stop` is not invalidated.** That test started and
stopped SD at the same elevation, which is the case that works, and it remains
true. What is new is the case where the two differ, which nobody had tried:
elevation is not something the daemon or the stop path has ever had to think
about, and until `CREATE.ACCOUNT` needed an elevated window there was no reason
for a start and a stop to straddle one.

**The consequence to watch is not the orphan itself.** It is that the orphan
holds a mapping of an unlinked segment and keeps running `check_lost_users()`
against it, while the next `sd -start` creates a fresh segment — so the machine
runs two daemons, one of them operating on memory nothing else can see.

The fix is small and is not written: check the return, report `EPERM` in
words, do not make it fatal because the segment teardown that follows is still
correct. PROJECT_STATUS.md §7 step 1d, and §6 carries the trap.

---

## Correction: 14 Aug 2026 - "redirect to a file" does not defeat the sdwind handle trap

Fourth session of 14 Aug 2026. The repository owner ran
`gplbld/verify-createaccount.ps1` in an elevated window — the first time it has
ever run — and it printed

```
  SD is not running, starting it
```

and then sat there indefinitely.

**SD was fine.** `Get-Process sd` showed nothing, `sdwind` was running, and no
Windows account, group or account directory had been created. The script never
got past starting SD.

### What was wrong, and what was wrong in this repository's own advice

PROJECT_STATUS.md §6 has carried the trap for a while: `sd -start` spawns
`sdwind`, which inherits stdout and stderr, so anything capturing that output
blocks until the *daemon* exits rather than until `sd -start` does. The entry
ended "Check with `Get-Process sdwind` rather than waiting, **and redirect to a
file when starting from a script**."

**That last clause is wrong, and it is what caused this.** The script's
`Invoke-Native` helper redirects both streams to files, exactly as instructed,
and hung anyway. `Start-Process -Wait` with `-RedirectStandardOutput` does not
return until the redirected **handles** are released, and `sdwind` holds them
open for its whole life. Whether the other end is a pipe or a file is
irrelevant — the wait is on the handle.

The remedy is the *other* half of the same entry, taken literally: do not wait
on the process at all. Start it, then poll for `sdwind`. That is now `Start-SD`
in `verify-createaccount.ps1`, and §6 carries the correction and the code.

### Why nothing caught it earlier

`verify-sshonly.ps1`, which produced this project's ssh-only verification and
which `verify-createaccount.ps1` copied its helpers from, **never starts SD**.
It had no reason to. So the one caller that does start SD was also the one
place `Invoke-Native` was wrong, and only on the branch taken when SD happens
to be down — which it was not on the day the script was written.

Same family as the `<sysdir>/bin` daemon bug recorded on 14 Aug 2026: a path
that works in every situation anyone happened to be in, and fails in the one
nobody was.

---

## 14 Aug 2026 - AllowGroups is written, and a session with no elevated window

Fourth session of 14 Aug 2026, from commit `9b44d4b`. It opened intending to do
step 0 — run `gplbld/verify-createaccount.ps1` — and could not: the permission
layer refused to launch an elevated process at all. **Step 0 did not run and is
unchanged.** Nothing was half-done by the attempt; the script's own guard exits
2 before touching anything when it is not elevated.

So the session took the work that needed no elevation, which turned out to be
most of what was left in §7 step 1.

### The installer's closing dialog now leads with CREATE.ACCOUNT (step 1b)

It used to end with `net localgroup sdusers <name> /add`, as though adding
somebody to a group were how you gave them SD. It is not, and it never made the
Windows account — which is the question that started the whole §5.6.1
discussion. It now gives `sd -start`, `sd -ASDSYS`,
`CREATE.ACCOUNT USER <name>`, says an elevated window is needed and why, says
accounts made that way are ssh-only, and gives the `ADMINISTRATOR` keyword. The
`net` command stays as the fallback it always was: somebody who already has a
Windows account.

Nobody has seen it on screen. `sd.iss` compiles; that is a different claim, and
the two defects already recorded in that script both compiled perfectly.

### AllowGroups, the second layer of §5.6.2 (step 1c)

`gplbld/allow-ssh-groups.ps1`, offered by `sd.iss` as a **child** of the
OpenSSH task and removed again on uninstall. The design decisions and why they
are what they are now live in §5.6.2; the four that would be easy to undo by
accident are: resolve the administrators group from `S-1-5-32-544` rather than
writing its localised name, write both the bare and `COMPUTER\` forms of each
group, insert **before** the first `Match` block, and make it a child task so
that "SD does not configure an ssh server it did not install" is structural
rather than remembered.

**What is proven is the editing, not the effect.** `verify-allowgroups.ps1`
runs the shipped script's own functions — lifted out by parsing the file, so
they cannot drift apart — against
`C:\Windows\System32\OpenSSH\sshd_config_default`, the template `sshd` copies
on first start. That template is world readable, so the test needs no
elevation, no `sshd` and no network, and passes 20 checks. Whether the patterns
**match the right people** is a property of Win32-OpenSSH's group lookup and
cannot be established offline. That is the lockout risk and it is open; §7 step
0a is how to close it, and §4 Unverified says what to watch.

**The test earned itself on the first run.** The block ended with a blank line
for readability. The blank line falls outside the markers, so removal left it
behind and every apply/remove cycle grew `sshd_config` by one line — in a file
belonging to somebody else. The check that caught it was not "did it remove the
line" but "is the file byte-for-byte the file it was". Both the specific fix
and that general shape are in §6.

The Inno brace-comment trap also caught this session, in a new `[Code]` comment
explaining that a procedure must run before `{app}` is deleted. It is now
recorded in §6 that the trap does not need carelessness about braces — only
prose about the installer, which is what installer comments are made of.

### Still open at the end of it

Step 0 and the new step 0a, both one command in an elevated window, and both
waiting on the same thing. `stage.py` now stages a third script, so the
installer needs a full `stage.py` rebuild rather than a re-run of `ISCC`.

---

## 14 Aug 2026 - A test for CREATE.ACCOUNT, and two traps in scripting SD at all

Same session as the ssh-only work below, after it. `CREATE.ACCOUNT`'s ssh-only
branch at `CREATEA` line 400 had still never executed — the `sdsshonly` group
did not exist when the verb was last run, and by now it does.

**`gplbld/verify-createaccount.ps1` is written and has NOT been run.** It needs
an elevated window. Recording it here rather than waiting, because the script
is the work and its result is a separate fact.

It goes further than checking the verb returns: it takes the account SD
produced and puts it through the three measurements that proved §5.6.2 —
`LogonUser` INTERACTIVE refused `1385`, `NETWORK_CLEARTEXT` admitted, and a
real ssh login with the password **SD itself set**. A pass would close the
chain end to end rather than checking group membership and inferring the rest.

Its cleanup removes the **Windows** half only, leaving the `ACCOUNTS` record
and the account directory. That is deliberate: removing those is
`DELETE.ACCOUNT`'s job and §7 step 1c has not decided what `DELETE.ACCOUNT`
should do, so a cleanup here would presuppose the decision. It also means
whoever runs it sees what a half-removed account looks like, which is the thing
1c has to settle.

The helpers are **copied** from `verify-sshonly.ps1` rather than shared. That
script had just produced the session's main result; factoring its internals
into a module would need another elevated run to prove the refactor changed
nothing, which is a poor trade for eighty lines. A third caller is the point to
make a common file.

### What was verified without elevation, which is most of it

Driven unelevated against the installed tree, with SD started from
`C:\Program Files\SD\usr\bin\sd.exe`: `COUNT VOC` returned **431 record(s)
counted** and `WHO` returned `SDSYS`, through `sd -ASDSYS` with no password,
since SDSYS has none set and `LOGIN` admits an administrator.

`CREATE.ACCOUNT USER sdacct1` then parsed, ran, and stopped at **`Create User
Failed, OS Error: 5`** — `ERROR_ACCESS_DENIED`, the elevation gate in
`CREATE_USER` — having created **nothing**, confirmed by checking for both the
Windows user and the account directory afterwards. So the VOC entry, the verb,
the parsing and the failure path are all confirmed on the installed system, and
only the privileged half is untested.

### Two traps, and they compound

Both cost time before the above worked, and both make SD look broken when it
is not.

1. **`Start-Process -RedirectStandardInput` makes SD exit.** It prints its
   banner, shows one prompt, answers `Process terminated` and stops. This is
   the same behaviour §6 already recorded for a `<` redirect: SD wants a pipe,
   not a file handle. The redirect had been chosen deliberately, to avoid the
   `2>&1` trap found earlier the same day — one trap's fix walking into
   another.

2. **A PowerShell pipe prepends U+FEFF to the first line.** So
   `@('COUNT VOC','WHO','OFF') | & sd.exe -ASDSYS` answers `COUNT is not in
   your VOC` for a good command, while `WHO` on the second line runs fine.
   Setting `$OutputEncoding` to `ASCIIEncoding` does **not** fix it — its
   preamble is empty and the BOM still arrives, so it comes from somewhere
   else and was not chased further. The fix is a blank sacrificial first line:
   the BOM lands on a line that was empty anyway.

   They compound because the first line of a scripted session is the one that
   matters, and because the obvious defence against the second — redirect from
   a file instead of piping — is the first.

---

## Correction: 14 Aug 2026 - RDP to this machine from itself: measured, and it does not work

Corrects the entry immediately below, "RDP denial CAN probably be tested on one
machine", which predicted that offering a *different* account would get past
`0x708` and reach the logon check. **It does not.** Measured the same day:

| attempt | credentials offered | result |
|---|---|---|
| `mstsc /v:localhost` | the signed-in user's own | `0x708` |
| `mstsc /v:localhost` | the probe account's | `0x708` |
| `mstsc /v:10.0.0.3` (the machine's own Wi-Fi address) | the probe account's | `0x708` |

The refusal arrives **before any credential prompt**, so the account offered
never enters into it, and reaching the machine by its LAN address rather than
by `localhost` makes no difference. RDP was enabled throughout -
`fDenyTSConnections` 0, `rdp-tcp` listening, inbound firewall rules on for all
profiles.

**No rule is being derived from this.** The observation is exactly the three
rows above: this machine will not RDP to itself, so the RDP half of §5.6.2
needs a separate client machine. Whether that is a session-count limit, a
loopback restriction, or something else is not established and does not need
to be.

**The lesson, which is the reason for two correction entries in one day.** One
error message produced two confident conclusions - first that the test was
impossible on one machine, then that it was possible with a different account -
and neither had been measured. The measurement cost one attempt. Both times the
inference was published to three files *in order to save a future session
time*, which is what made being wrong expensive rather than cheap. Reach and
confidence were added in the same step as the guess; the record should have
carried the observation and stopped there.

---

## Correction: 14 Aug 2026 - RDP denial CAN probably be tested on one machine

Corrects "14 Aug 2026 - The ssh-only model is proven, and three false failures
on the way", immediately below, which said the `0x708` failure meant "no
variation of it will work on one machine" and moved the RDP test to the second
machine on that basis. **The reasoning was wrong**, and it was wrong in the
direction that costs most: it declared a test impossible and parked it.

`0x708` is *"you already have a console session in progress"*. It is the
**same-user** case. `mstsc /v:localhost` had defaulted to the signed-in user's
own credentials, and asking to connect to a console session you are already
sitting in is circular, so RDP refuses before authentication. The error was
read as a statement about how many sessions a Windows client SKU permits, and
it is not one.

What a client SKU actually does: several user sessions may exist at once - that
is Fast User Switching - but only one may be **connected**, and an incoming RDP
logon **takes the console over** rather than being refused for coexisting with
it. So a *different* user, with no session to collide with, has nothing to
trigger `0x708` and should reach the logon check where the deny right is
evaluated.

The attempt is therefore worth making with the **probe account's** credentials.
Outcomes: refused with "the system administrator has restricted the types of
logon ... that you may use" means the right holds and nothing happens to the
console; admitted means the right does not hold, §5.6.2 is half wrong, and the
console session is disconnected - recoverable by signing in again, with
processes in the disconnected session still running.

The second machine remains the definitive test, for a better reason than the
one originally given: it is the configuration a real user is in, and it does
not put the tester's own session at risk.

**The general lesson, which is why this is an entry and not an edit.** An error
message was taken as evidence for a broader claim than it supported, and the
broader claim was then written into three places at once - precisely so that a
future session would not re-attempt the test. Confidence and reach were added
in the same step. Prefer to record what was observed (`0x708`, same user,
before authentication) and keep the conclusion narrow.

---

## 14 Aug 2026 - The ssh-only model is proven, and three false failures on the way

Third session of 14 Aug 2026, covering the commit that carries this entry, on
top of `61b9408`. One subject: §5.6.2, which the previous session left decided,
implemented, shipped in the installer and completely unexercised.

### What was proven

`gplbld/verify-sshonly.ps1`, new and tracked, against a real Windows account:
thirteen checks, all passing. The result in one line — **joining `sdsshonly`
takes away the console and leaves ssh alone.**

| | control, no SD group | in `sdsshonly` |
|---|---|---|
| `LogonUser` INTERACTIVE | admitted | **refused 1385** |
| `LogonUser` NETWORK_CLEARTEXT | admitted | admitted |
| `ssh` with a password | admitted | **admitted** |
| `ssh` with a key | admitted | admitted |

The account did not merely authenticate: the test asserts on `whoami` coming
back, so a shell ran under that token. And the verdict does not rest on the
test's own reporting — the installed sshd, which is the only one that counts,
logged `Accepted password for sdsshprobe` and `Accepted publickey for
sdsshprobe` to `OpenSSH/Operational` at the same moment.

`deny-logon.ps1` ran against a real group for the first time; it had only ever
been tried on a throwaway. `SeDenyNetworkLogonRight` was confirmed untouched,
which is the one thing in the design that had to be got right.

**Still not observed: RDP refusal, and it needs two machines.** There is no
`LogonUser` type for it — RDP is logon type 10 and `LogonUser` cannot produce
one — so only a real Remote Desktop connection exercises the right. The probe
account was left alive to do that by hand, and the attempt on 14 Aug 2026
failed for a reason unrelated to the design: `mstsc /v:localhost` answers
`0x708`, "you already have a console session in progress", refusing **before
authentication** because a Windows client SKU allows one session and the
console holds it. No variation of it will work on one machine. The test moves
to the second machine, with this one as the RDP client.

### Why the script is a file rather than a session

§7 step 2 has to repeat all of this on the second machine, which is being built
precisely because this one has a development tree. A test that exists only as
typed commands would have been retyped from memory, differently.

### The control column earned its place immediately

The first run refused the **key** login on both sides of the experiment. Read
without a control that is "the deny rights break ssh", and §5.6.2 would have
been abandoned on a false result. An equal failure on both sides cannot have
been caused by the thing that differs between them.

The real cause turned out to be worth knowing on its own: **a Windows account
that has never logged on has no user profile**, and Win32-OpenSSH resolves
`AuthorizedKeysFile .ssh/authorized_keys` relative to the home directory — so
the planted key was never read. Shown in both directions across runs: refused
twice with no prior login; accepted after one password login, which creates the
profile. **This applies to accounts `CREATE.ACCOUNT` makes**, and it is in the
product changelog for that reason.

### Three false failures, all now traps in §6

Every one of them reported a failure that had not happened, which is the
expensive kind.

1. **`native.exe 2>&1` under `$ErrorActionPreference = 'Stop'`.** PowerShell
   5.1 wraps native stderr in `ErrorRecord`s and `Stop` makes them throw. `ssh`
   writes `Warning: Permanently added 'localhost' ...` to stderr **on a
   successful login**, so the script died on a success message and printed
   `FAILED` with a stack trace. Fixed by routing every external program through
   one `Invoke-Native` helper built on `Start-Process` with separate stream
   files. There is no inline `2>&1` left in the script.

2. **`sshd -d` from an elevated prompt authenticates nobody.** sshd must run as
   SYSTEM to build a user token; elevation is not enough and there is no flag
   for it. It answers `get_user_token - unable to generate user token ... as i
   am not running as system` and fails at `mm_answer_pwnamallow`, before
   authentication is attempted — so a DEBUG3 log that looks like a total
   authentication failure is really a diagnostic that cannot work. Both rounds
   of a diagnostic script were void. The installed service's reasons are in the
   `OpenSSH/Operational` event log and were enough.

3. **A human retyping a 36-character random password.** Three `Failed password`
   entries in the event log pointed at a design problem that did not exist —
   `LogonUser` had accepted the same string on the same account minutes
   earlier. `ssh` honours `SSH_ASKPASS` with `SSH_ASKPASS_REQUIRE=force`, so
   the password test is now automated; the secret travels in an environment
   variable cleared in a `finally`, never in a file. The generated password now
   also avoids `l I 1 O 0` and every shell metacharacter.

### A question asked and answered by measuring

`New-LocalUser` joins no group at all, and `CREATE_USER` adds none either, so
an SD account is in `sdusers`, `sdu_<name>` and `sdsshonly` and **not
`BUILTIN\Users`**. While the ssh failures were unexplained this looked like a
likely cause, and the tempting fix was to add `Users` defensively in
`CREATEA`. It was measured instead: the account logged in over ssh and ran a
command *before* `Users` was added, and adding it changed nothing. **No code
was changed**, and §4 records the measurement so the question is not reopened.

### What it cost, and what is still open

Three elevated runs, two of which failed for reasons that had nothing to do
with the subject. Open: RDP refusal; `CREATE.ACCOUNT` with `sdsshonly` present,
which has still never executed that branch; `AllowGroups`; and SD itself driven
over an ssh session.

---

## 14 Aug 2026 - SD runs as an ordinary user, and sshd finally starts

The end of the second session of 14 Aug 2026. Both results came from the
repository owner rebooting, which is worth noting on its own: the two things
blocking verification all day were a stale access token and a half-applied
Windows capability, and one restart cleared both.

### SD runs unelevated, which it never had

From a **normal PowerShell window** — no elevation, no MSYS2, nothing set in
the environment:

```
sd -start      SD (64 Bit) has been started     sdwind running: True
COUNT VOC      431 record(s) counted
WHO            2 SDSYS
sd -stop       SD (64 Bit) has been shut down   sdwind gone
```

Three things close together:

- **§5.6.1 in the real world.** `IsAdmin()` admitted an administrator who had
  not elevated. The earlier proof used a probe built with a synthetic gid; this
  is the shipped binary in an ordinary session, which is the case that matters.
- **§5.7's ACL model from the user's side.** The token now carries `sdusers`,
  and that grants the data tree — 3,264 files listed unelevated — **and**
  `/dev/shm`, mapped into `C:\ProgramData\SD\shm`, which is what `sd -start`
  needs in order to allocate semaphores. Before the reboot the same session was
  refused on every path inside `C:\ProgramData\SD`; nothing else changed.
- **The sign-out requirement is real and sufficient.** It is documented in §6
  and in the installer's closing dialog, and this is it being demonstrated
  rather than asserted.

**What it does not show, and is now the most visible gap:** `sd -start` had to
be typed. An installed system does not come up on boot, because there is no
service. After every restart somebody must start SD by hand. That is §5.7's
service model and it is hard to miss now that everything else works.

### sshd runs, and the installer step was still wrong

`Get-WindowsCapability -Online` reported `State : Installed` after the reboot,
so the brace fix earlier in the session was the whole of that bug.

**But the service was left `Stopped`, `StartType=Manual`, with no
`sshd_config`** — and that turned out to be a second defect rather than an
artefact of the terminated run. The capability installs the *files*; the
**service does not exist until after a reboot**. The step ran
`Add-WindowsCapability`, `Set-Service` and `Start-Service` in one breath, so on
a machine that needs the restart, `Set-Service` throws "no such service", hits
the catch, and reports **total failure for what is actually a success needing a
reboot**.

Fixed by moving the whole thing out of the `.iss` into
`gplbld/install-ssh.ps1`, which distinguishes the cases and **exits 2 for
"restart required"**. Being told to reboot is useful; being told it failed is
not. Moving it to a file is also the direct lesson of the brace bug: an inline
`[Run]` parameter cannot be read or parse-checked, and a shipped script can —
both scripts are now parse-checked before they are believed.

Run against the already-installed capability it reported `sshd is Running,
StartType=Automatic`, two listeners on port 22, the firewall rule enabled, and
`sshd_config` created. sshd writes that file on first start, which is the
earliest moment `AllowGroups` (§5.6.2) could be edited into it — worth knowing,
because there was nothing to edit before now.

### Where this leaves the ssh-only model

**Built, and completely untested through ssh** — but the blocker is gone. This
machine has a running `sshd` for the first time, so the ordered test in §4 can
be done here rather than waiting for the second machine. The step that matters
is proving an account in `sdsshonly` **can** still ssh in: if Win32-OpenSSH
needs something the deny rights remove, the model fails closed and nobody
reaches SD at all.

## 14 Aug 2026 - SD accounts become ssh-only, and the API goes through ssh too

**Decision from the repository owner**, 14 Aug 2026: accounts SD creates reach
the machine over ssh and nothing else; local terminal access is for
administrators, who have ordinary Windows accounts; and **the API is piped
through ssh as well**. That last clause settles §8's "how should the API be
exposed" — posture B, which is what the owner had already done to OpenQM.

Asked whether `CREATE.ACCOUNT ... ADMINISTRATOR` should still create the
Windows account, the answer was **yes, unrestricted, keep the keyword**. So the
keyword now decides two things at once:

| | `CREATE.ACCOUNT USER x` | `... x ADMINISTRATOR` |
|---|---|---|
| Windows group | standard user | `Administrators` |
| Administers SD | no | yes |
| Console / RDP | **denied** | allowed |
| ssh | yes | yes |

### The design, and the two things it turns on

**Two rights, and deliberately not a third.**
`SeDenyInteractiveLogonRight` blocks the console and
`SeDenyRemoteInteractiveLogonRight` blocks Remote Desktop.
**`SeDenyNetworkLogonRight` must not be set** — Win32-OpenSSH authenticates
with a network logon, cleartext-network for passwords and S4U for keys, so
denying it would remove the one route the design exists to preserve. That is
the whole risk in one sentence.

**The rights go on a GROUP, applied once by the installer, not per account.**
`CREATE.ACCOUNT` adds every non-administrator account to `sdsshonly`; that
membership is all account creation does. Rejected alternatives, and why:

- There is **no PowerShell cmdlet for user rights** — measured,
  `Get-Command *AccountRight*` returns nothing — so a per-account grant means
  P/Invoke or `secedit` on the hot path of every creation.
- **`secedit` is a read-modify-write of the entire USER_RIGHTS area.** Running
  it per account rewrites unrelated machine policy and races anything else
  editing it.
- A group is **inspectable**: "who is confined to ssh?" is one membership list
  rather than a walk through `secpol.msc`.
- SD already has `!os_group("ADDMEM", ...)`, written and verified.

**It cannot be `sdusers`**, which is the trap worth naming: that group grants
access to the data *files* and administrators are in it too, so denying console
logon there would lock administrators out of their own machine.

### What was built

`gplbld/deny-logon.ps1`, shipped to `C:\Program Files\SD\` by `stage.py` and
run once by the installer. It uses `LsaAddAccountRights` through P/Invoke —
surgical, one SID and one right — rather than `secedit`. It lives in a file
rather than inline in the `.iss` deliberately: an inline `[Run]` parameter is
exactly where the OpenSSH brace bug hid, and a file can be read and
parse-checked on its own.

`CREATEA` gained the `else` branch to the `ADMINISTRATOR` test, plus messages
10034 and 10035. It compiles with 0 errors.

### Verified, and the part that is not

Against a throwaway group:

| Right | Before | After |
|---|---|---|
| `SeDenyInteractiveLogonRight` | `Guest` | `sddenyprobe,Guest` |
| `SeDenyRemoteInteractiveLogonRight` | *absent* | `sddenyprobe` |
| `SeDenyNetworkLogonRight` | `Guest` | `Guest` — untouched |

`Guest` surviving in the first row is the case for LSA over `secedit`
demonstrated rather than argued. Idempotent on a second run; a missing group
exits 1 saying so.

**One trap in reading it back:** `secedit /export` writes resolvable local
groups **by name**, not by SID, so a check that greps the exported policy for a
SID reports "absent" when the right is present. The first attempt at this test
did exactly that and reported a false negative.

**Nothing has been tested through ssh**, because this machine still has no
`sshd` — the install hit the Features-on-Demand delay, was terminated part-way
and left a pending reboot. The untested list is in §4, and item 2 on it is the
one that matters: if Win32-OpenSSH turns out to need something these rights
remove, the model fails **closed** and nobody reaches SD at all. It should be
proven on a machine with `sshd` before anyone relies on it.

`AllowGroups` in `sshd_config` — the owner's second layer — is designed in
§5.6.2 and **not implemented**. It needs care: it means writing to a file SD
does not own, and the list must include administrators or the machine's own
administrator loses ssh.

## 14 Aug 2026 - the OpenSSH option never worked, and never said so

Found by the repository owner ticking the box during a normal interactive
install and then asking why there was no ssh server. There was not, and there
never had been on any install.

`gplbld/sd.iss` had:

```
try {{ Add-WindowsCapability ... ; Start-Service sshd }} catch {{ exit 1 }}
```

**In Inno, `{{` is the escape for a literal `{`, and `}` needs no escape at
all** — so `}}` is not an escape, it is two closing braces. The install log
records `Parameters:` *after* expansion, and shows what PowerShell actually
received:

```
try { Add-WindowsCapability ... ; Start-Service sshd }} catch { exit 1 }}
```

Single opening braces, doubled closing ones. Parsed without running it, that
gives "The Try statement is missing its Catch or Finally block" — so nothing
executed at all.

**It failed in total silence, by design.** The entry carries
`skipifdoesntexist` and checks no exit code, because §5.9 requires that a
failed ssh install must not fail the SD install. Correct rule, but it means a
step that could never run looked identical to one that ran fine: no `sshd.exe`,
no service, nothing on port 22, and not a word anywhere. The only evidence is
the expanded `Parameters:` line in the log.

Fixed by writing `}` singly. The corrected string was parsed before being
believed:

```powershell
[System.Management.Automation.Language.Parser]::ParseInput($s, [ref]$null, [ref]$err)
```

as shipped → parse error; as fixed → OK. That check costs nothing and is worth
doing to any generated PowerShell.

### And then the corrected command exposed a second problem

Running it for real showed the step is **slow**, which §5.9 had not
anticipated — it had planned for failure, not for duration. With the capability
`NotPresent`, `Add-WindowsCapability` fetches from Features on Demand and hands
off to `TiWorker`, which worked for minutes, grew its working set by 16 MB in a
four-second sample, and set **`RebootPending`**.

Because the `[Run]` entry is `runhidden` with no progress, the wizard sits on
"Installing OpenSSH Server..." saying nothing, and it reads as a hang. It was
reported as one during this very session. The run was terminated part-way,
which left the capability unapplied and the reboot pending — the outcome that
argues hardest for the guidance now in §5.9:

- say on the tasks page that it takes minutes;
- never kill `TiWorker`, since interrupting servicing mid-operation is how the
  component store gets corrupted;
- and tell the user about the pending reboot, which SD itself never needs.

**Still unverified:** that `sshd` runs once servicing completes, and everything
downstream of it — which now includes the repository owner's decision that SD
accounts are to be ssh-only.

## 14 Aug 2026 - CREATE.ACCOUNT runs for the first time, and can make an administrator

Carries out §7 step 1 the same day the administrator decision was made. The
verb had **never been executed**, on Windows or otherwise, since the port
began.

### What the repository owner clarified, and why it removed a config option

> `CREATUSR` isn't an active verb in SD, everything is handled by
> `CREATE.ACCOUNT`. We have only accounts, not accounts and users like in QM
> and ScarletDME.

Confirmed by the TCL verb list they supplied the same day, now tracked at
[docs/TCL_VERBS.md](docs/TCL_VERBS.md): `CREATE.USER`, `DELETE.USER`,
`ADMIN.USER`, `LIST.USERS` and `PASSWORD` are all in the "in OpenQM, not in SD"
column. There is no user concept to manage separately.

So the `config('CREATUSR')` gate in `CREATEA` was **removed**. It asked
permission to do the second half of the only thing the verb does, which stops
making sense once account and OS account are the same object. `config.c` still
parses the parameter and `CONFIG` still prints it; `DELACC` still consults it,
which is now an asymmetry and is written up as §7 step 1c.

**Correction to the entry below and to what §7 said.** It claimed `CREATUSR`
"is not in the shipped `sd.conf` and defaults off", and gave that as one of two
things blocking the verb. **That was wrong.** `config.c` line 98 sets
`pcfg.create_user = 1` — it defaulted **on** and blocked nothing. The real
blocker was the pathname validator below, which nobody had looked at because
the verb had never been run far enough to reach it.

### The defect that had been waiting at the end of it

`CREATEA` line 257 calls `ospath(pathname, OS$PATHNAME)`. That is the **C**
validator in `op_dio2.c`, not the BASIC `VALID_OS_PATH` that was fixed on
13 Aug — two validators with similar names, different implementations, and only
the C one on this path. It split the pathname on `/` alone and ran
`valid_name()` over each component, and `valid_name()` rejects everything in
`df_restricted_chars`, which contains **both `:` and `\`**. So
`C:\ProgramData\SD\user_accounts` was a single component holding two forbidden
characters, and no native Windows path could pass.

**The symptom was a half-made account**, which is why it is worth recording.
`CREATE.ACCOUNT` printed `User sdtest1 Created`, prompted for and set the
Windows password — and only then stopped with `Invalid account pathname`. The
Windows account existed, nothing in SD did, and the message named a pathname
while the visible work had apparently succeeded.

Fixed by skipping an optional drive letter and splitting on either separator.
**`df_restricted_chars` was deliberately not widened**: `op_dio3.c` and
`op_dio4.c` use it to map record ids onto filenames and back, which is a
different job, and changing it would change how records are named on disk
without being reversible for files that already exist.

### The `ADMINISTRATOR` keyword

```
CREATE.ACCOUNT USER <name> {ADMINISTRATOR} {NO.QUERY}
```

Keywords already follow the name, so it fits the existing shape. Matched on the
token text rather than by adding a `KW$` constant — `SYSCOM/PARSER.H` is a
positional table of 216 entries shared by every verb, and extending it to serve
one verb is a larger and riskier change than this warranted. The cost is that
`ADMINISTRATOR` cannot be abbreviated, unlike `NO.QUERY`.

The grant goes through `!os_group`, which learned to take a **security
identifier** as well as a name: `Add-LocalGroupMember` has a parameter set that
accepts one, and `BUILTIN\Administrators` is renamed on a localised Windows so
the name cannot be written out. Same reasoning as `icacls` in `sd.iss`. Two new
messages, 10032 and 10033 — note 10030 and 10031 were **already taken** by
`CPROC`'s step-up prompts, which is worth checking before claiming a number.

The grant is deliberately placed **after** the `sdusers` add rather than
instead of it. They answer different questions: `sdusers` grants access to the
database files, `Administrators` decides who administers SD. An administrator
who has not elevated does not carry `Administrators` in their token either, so
they need `sdusers` to reach the data tree exactly as an ordinary user does.

### Verified

Run elevated — `CREATE_USER` needs an elevated token — and driven through a
pipe with the password first, per §6.

| | `CREATE.ACCOUNT USER sdtest1` | `... sdtest2 ADMINISTRATOR` |
|---|---|---|
| Windows local user, enabled | yes | yes |
| member of `sdusers` | yes | yes |
| `sdu_<name>` group created | yes | yes |
| account dir, VOC, `$HOLD`, `$SAVEDLISTS`, BP, private catalogue | yes | yes |
| record in `ACCOUNTS` | yes | yes |
| **member of Administrators** | **no** | **yes** |

So `CREATE_USER`, `SET_PASSWD` and `OS_GROUP` have all now executed against
real Windows accounts, which closes the creation half of "every OS account
operation is unverified". `DELETE.ACCOUNT` and `MODIFY.ACCOUNT` still have not
been run.

**Both test accounts were removed afterwards.** They were real Windows accounts
with a known password and one of them was a local administrator; leaving them
would have been a live hole rather than untidiness. One empty `sdu_sdtest2`
group survived a cancelled elevation prompt and is harmless.

## 14 Aug 2026 - a Windows administrator is an SD administrator

**Decision from the repository owner**, reversing the "SDSYS is the only
administrator" half of §5.6 and settling §8's `IsAdmin()`/`sdadmins` question
on the same day that question was promoted to blocking. In their words: if you
can log in as an administrator to the OS, you are an administrator of SD; the
installer has to be an administrator, so the person who installs SD administers
it. Normal accounts are created as standard local accounts, and an
administrator is made deliberately with a keyword at account creation.

### How it came up, because three problems turned out to be one

It surfaced from a plain interactive install rather than from design work.
Running the wizard as a normal user would:

1. The final dialog told the user to run `net localgroup sdusers <name> /add`,
   which the owner queried — SD has `CREATE.ACCOUNT`, which already does
   exactly that (`CREATEA` line 340, `os_group("ADDMEM", "sdusers", ...)`) and
   creates the Windows user besides. The installer was advertising a manual
   workaround as though it were the design.
2. The "set the SDSYS password now" step ran and never let anyone type.
3. Which raised the question of why there was a second password at all.

And the answer to (3) exposed a drift that had been there since 13 Aug: §5.6
said OS groups were dropped from SD's logic entirely, but `IsAdmin()` was still
the real source of `K$ADMINISTRATOR`, and §5.6 itself carved out "an
administrator running an internal command" as a password-free way in. **So an
OS administrator was already being admitted without the SDSYS password.** The
written decision and the behaviour had come apart; this closes the gap in
favour of the behaviour, and takes option 2 of the three that §8 had listed.

It also kills the `sdadmins` defect found earlier the same day — the installer
created `sdusers` and never `sdadmins`, so a clean machine got an install
nobody could start. There is now no private group to create.

### `getgrouplist()`, not `getgroups()` — and this is the whole of it

Measured with a C probe on 14 Aug 2026, from an **unelevated** session
belonging to a machine administrator:

| Call | Source | Contains Administrators (544)? |
|---|---|---|
| `getgroups()` | the process token | **NO** |
| `getgrouplist()` | the account's groups in the SAM | **YES** |

A UAC-filtered token carries Administrators as "deny only" and Cygwin omits it,
so `getgroups()` really means *is elevated*, not *is an administrator*.
`IsAdmin()` used `getgroups()`. It uses `getgrouplist()` now, which is the
question the owner actually asked.

**And the gid, never the name.** `getgrnam("Administrators")` gives 544 and
`getgrgid(544)` gives it back, because Cygwin maps built-in SIDs to their RID —
the same reason `Users` is 545. **`Administrators` is renamed on a localised
Windows**, so a lookup by name fails on a German or French machine while the
number does not. `sd.iss` had already had to learn this for `icacls`, where it
writes `*S-1-5-32-544`. `SD_ADMIN_GROUP "sdadmins"` in `sddefs.h` becomes
`SD_ADMIN_GID 544`, still `#ifndef`-guarded so the probe trick in §6 works.

### Verified

Built clean. Then, from an **unelevated administrator session** — the case the
old test would have got wrong:

- **Positive:** the shipped build ran `sd -start`, the daemon came up, `sd
  -stop` took it down. This is decisive rather than incidental: gid 544 is
  **not** in `getgroups()` here, so it can only have been found through
  `getgrouplist()`.
- **Negative:** `sd.c` and `linuxlb.c` rebuilt with `-DSD_ADMIN_GID=99999`
  refused with "Command requires administrator privileges", exit 1 — so the gid
  really is what is tested, and §6's override still works.

### Also changed

The installer's postinstall "Set the SDSYS administrator password now" step is
**removed**, not fixed. It is unnecessary under this model, and it was broken
twice over: `sd -internal` needs a running server and the installer never runs
`sd -start`, so it died with "SD has not been started"; and Inno logged it as
`Run as: Original user`, so it ran unelevated with a token that does not carry
`sdusers` and could not have opened the database either. `nowait` meant the
console vanished before either message could be read. All three would have to
be fixed together if a password step is ever wanted back.

`sdusers` is untouched and still needed: it grants access to the data tree,
which is an ACL question rather than an authorisation one. Worth keeping
straight — an administrator who has not elevated does not carry Administrators
in their token either, so they need `sdusers` to reach the files exactly as an
ordinary user does.

### Still to do

`CREATE.ACCOUNT USER <name> {ADMINISTRATOR}` — the keyword that makes an
administrator rather than a standard local account. The existing syntax puts
keywords after the name (`{NO.QUERY}`), so it fits without disturbing anything.
Not built in this commit. Note `CREATE.ACCOUNT` has still never been run at
all, and `CREATUSR` is not in the shipped `sd.conf` so OS user creation is
disabled out of the box — both have to be dealt with before the verb works.

The installer's closing dialog still points at `net localgroup`, which is the
thing that started this. It should lead with `CREATE.ACCOUNT` and keep the
manual command as the fallback for someone who already has a Windows account —
deliberately **not** reworded yet, because pointing users at a verb that
currently errors would be worse than the present text.

## 14 Aug 2026 - the daemon is fixed and renamed `sdwind`, and it starts

Closes the entry below, which found that `sd -start` could never launch the
daemon on an installed system, and carries out the rename the repository owner
asked for. Both in one change because they are the same lines.

### The fix

Two call sites built a path to an executable from `sysseg->sysdir`:

- `gplsrc/sysseg.c`, `start_sd()`, `"%s/bin/sdlnxd"`
- `gplsrc/sdlnxd.c`, `check_lost_users()`, `"'%s/bin/sd' -cleanup"` — the
  cleanup session fired when a user's process has vanished

Both resolved to `C:\ProgramData\SD\sdsys\bin`, which holds `pcode` and
`pcode.old` and no executables at all. The second one had not been noticed when
the entry below was written; it was found by reading the file while renaming
it, which is an argument for doing the rename rather than deferring it.

**Both now resolve against the running executable**, through a new
`gplsrc/exepath.c`:

```c
bool exe_directory(char* buff, int buff_len);   /* readlink("/proc/self/exe") */
```

That was chosen over hardcoding the new location deliberately: the launcher and
the launched then stay together **by construction**, so the next layout change
cannot reintroduce this. It is also the same rule the MSYS2 runtime itself uses
to find its POSIX root, which is why `sd.exe` and its DLLs must share a
directory. `/proc/self/exe` is a Linux interface that the MSYS2 runtime
implements; measured 14 Aug 2026, it resolves correctly through a path
containing spaces and reports the name **without** the `.exe` extension, which
is what is wanted since `execl()` and `system()` both append it — and is how
the code it replaces named `sdlnxd` and `sd`.

`exepath.o` is added to `gpl.src` and to the daemon's own link line, which is
short (`sdwind.o sdsem.o exepath.o`) and cannot reach `linuxlb.c`.

**And the forked child now `_exit()`s instead of returning.** This is the half
that made the bug invisible: on a failed `execl`, or a `snprintf` overflow,
control fell back into the caller's code inside a child that had already
`daemon()`ed, so a missing daemon produced no message and no failed exit
status. It now prints what it could not start and why, and leaves. The general
lesson is in §6 — a forked child that fails must `_exit()`, never `return`.

### The rename

`sdlnxd` means "SD Linux daemon", which is the wrong name in a Windows-only
repository. `gplsrc/sdlnxd.c` → `gplsrc/sdwind.c` (via `git mv`, so the history
follows), the `sdlnxd_pid` field in the shared segment struct, `sysdump.c`'s
report line, the `Makefile` target and its entry in the `sd:` prerequisites, two
ship-list entries in `gplbld/stage.py`, and one comment in
`gplbld/bootstrap.py`.

The name itself now lives in **one place**, `SDWIND_NAME` in `sddefs.h`, used
both by `start_sd()` to launch it and by the daemon's own errlog prefix, so the
two cannot drift apart and a further rename is a single line.

**A correction to the caution in the entry below**, which said renaming
`sdlnxd_pid` "changes the layout of the shared segment struct". It does not —
renaming a field of the same type at the same offset changes no layout, so
`revstamp.h` and the segment version needed no thought after all. What *does*
change across this commit is the daemon's **file name**, which matters only to
an existing install: an old tree has `sdlnxd.exe` and a new `sd.exe` will look
for `sdwind`. Upgrading an existing install is unsolved anyway (§5.9.1).

`gplbld/sd.iss` needed no change, as predicted — the daemon ships under the
`ProgramFiles\*` glob and is not named anywhere in the installer.

### Verified

Built clean (`make sd`, exit 0, `Linking sdwind`, `Linking sd`); the four
changed or new C files compile with no warnings under `-Wall -Wextra`, the only
one reported being a pre-existing unused parameter in `create_shared_segment`.

Then, on the **development** tree, `sd -start` left
`bin/sdwind` running and `sd -stop` removed it. That proves the mechanism but
not the bug, since `<sysdir>/bin` holds executables there — so the staged tree
was rebuilt with a full bootstrap, the installer recompiled, and the machine
cleaned and installed from scratch:

- `sdwind.exe` **running as pid 9740 out of `C:\Program Files\SD\usr\bin\`**,
  while `<sysdir>\bin` held only `pcode, pcode.old`. The old path could not
  have worked; this is the case that had never once succeeded.
- `COUNT VOC` 431 records, `WHO` `2 SDSYS`, and `sd -stop` took the daemon down.
- The install re-counted at **3,264 of 3,264** files, which also confirms the
  installer still works after `stage.py` changed.

Not verified: what the daemon *does*. `check_lost_users()` runs every five
minutes and shells out to `sd -cleanup` only when it finds a user table entry
whose process has gone. Nothing has made a session go missing, so that path —
including the second fixed call site — has still never executed. It was
unreachable before today, the daemon never having run.

`errlog` stayed empty through the whole cycle, as it did before the fix, so
that open question is not explained by the daemon and remains in §4.

## 14 Aug 2026 - `sd -start` cannot start the daemon on an installed system

Found immediately after the entry below, while scoping the `sdlnxd` → `sdwind`
rename the repository owner asked for. The rename turned up a defect, which is
the more useful half of this entry.

**`gplsrc/sysseg.c` line 405** builds the daemon's path as `"%s/bin/sdlnxd"`
from `sysseg->sysdir`, so on an installed system it execs
`C:\ProgramData\SD\sdsys\bin\sdlnxd`. That directory holds `pcode` and
`pcode.old` and nothing else. The daemon ships to
`C:\Program Files\SD\usr\bin\sdlnxd.exe`.

**Why it was there and why it is now wrong.** The Linux install put the
executables and the pcode composite library in the same
`/usr/local/sdsys/bin`, so `sysdir` was a correct base. §5.8 split them —
binaries to `C:\Program Files\SD\usr\bin`, `pcode`/`pcode.old` staying with
SDSYS because `BCOMP` addresses them relative to `@sdsys` — and this call site
was not moved with them. The split itself is recorded in §6 as "two unrelated
things in one directory"; what was missed is that a C runtime string also
depended on them being one thing.

**It fails silently and the symptom is an absence.** The `execl` is in a forked
child that has already called `daemon(1, 1)`, so nothing is printed anywhere
and `sd -start` still reports success. `sysseg->sdlnxd_pid` stays at -1, which
is exactly the value meaning "failed to start", and `sd -stop` then correctly
skips the kill. SD works completely — shared segment, `COUNT VOC` reporting
431, `WHO`, `LIST ACCOUNTS` — because none of that needs the daemon. The only
thing that shows it is `Get-Process sdlnxd` returning nothing, which is what
the entry below logged as an unexplained observation before this was chased.

**It works in development**, where `<sysdir>/bin` genuinely does hold the
executables, which is why 13 Aug 2026 recorded the daemon starting and staying
up and why nothing had contradicted that until an install existed to test. Same
family as the `/bin/bash` trap in §6: correct in the development tree, wrong in
the installed one, and invisible until the two differ. The generalisation is
now in §6 — **when anything moves between the trees, grep the C for the old
location**, because the compiler cannot see a runtime string.

Not fixed here. It is §7 step 1a together with the rename, since they are the
same lines, and the fix should resolve against the executable's own directory
rather than hardcode the new path — otherwise the next layout change repeats
it.

**The rename scope, recorded so it need not be re-derived.** Tracked source
only: `gplsrc/sdlnxd.c` (rename the file too), `gplsrc/sysseg.c`,
`gplsrc/sysseg.h` (`int sdlnxd_pid` in the shared segment struct),
`gplsrc/sysdump.c`, `Makefile` (target plus the `sd:` prerequisite list),
`gplbld/stage.py` (two ship-list entries) and one comment in
`gplbld/bootstrap.py`. `gplbld/sd.iss` does **not** name it — it ships under
the `ProgramFiles\*` glob — and `gpl.src` does not list it either, since it
links separately from `sdlnxd.o` and `sdsem.o`. `bin/` and `gplobj/` are build
output; `AI_Modification_Notes/` is a historical record and should keep the old
name, as should this file's earlier entries.

## 14 Aug 2026 - the installer fix is verified: a first install lays down 3,264 files

Closes the correction below, "the installer was NOT verified for a first
install". The fix committed in `5748a51` was run for the first time and it
works. This entry is the evidence, because the previous round of testing was
green against a database the installer had never written and the lesson taken
from that was to **count what was installed**.

**Method, and it matters that the machine was cleaned first.** The broken
install left by the previous session was removed in one elevated pass:
`C:\Program Files\SD\unins000.exe /VERYSILENT`, then `C:\Program Files\SD` and
`C:\ProgramData\SD` deleted outright, then the `sdusers` group removed. The
data tree was copied to `C:\Users\dmont\sd-preclean-backup` first; only
`sdsys/$HOLD` and `sd.conf` survived the copy, which is of no consequence
because the tree being discarded was the 16-file broken one, but it is recorded
rather than glossed.

**The installer under test was rebuilt from the tracked source**, not taken on
trust from the previous session's output directory:

```sh
cd sdb_ai/sd64
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" /DStage=C:\Users\dmont\stagetest \
    /O"C:\Users\dmont\sdout" gplbld\sd.iss
```

The staged tree at `C:\Users\dmont\stagetest` was reused unchanged. That is
worth being explicit about: the `.exe` provably corresponds to the committed
`sd.iss`, and only the packaging step was redone.

**What a genuine first install produced.** Counted, not inferred:

| Measure | Broken (before fix) | Now | Staged source |
|---|---|---|---|
| files under `C:\ProgramData\SD\sdsys` | 16 | **3,264** | 3,264 |
| directories under it | - | 44 | 44 |
| `gcat` entries | 0 | 129 | 129 |
| `GPL.BP.OUT` entries | 0 | 11 | 11 |
| `Installing the file` lines in the Inno log | 15 | 3,279 | - |
| Inno log length | 145 lines | 16,507 lines | - |

A `Compare-Object` of every staged path against every installed path reported
**no differences in either direction** - nothing skipped and nothing extra. The
install log line count is the cheapest possible check of this class and is
worth keeping in mind for next time: 145 lines against 16,507 is not a
difference anyone has to squint at.

**And the installed system runs**, observed twice in two separate elevated
passes:

- `sd -start` from `C:\Program Files\SD\usr\bin\sd.exe`
- `COUNT VOC` reporting **431 records**
- `LIST ACCOUNTS` reporting `Pathname: C:\ProgramData\SD\sdsys`
- `WHO` reporting `3 SDSYS`
- `sd -stop`

each preceded by `Warning: account SDSYS has no password set`, which is the
correct state for a tree whose installation has not been finished by setting
one, and which confirms the ordering decision in §5.9: every internal command
works while SDSYS has no credential.

**The rest of the installer's job, all confirmed on the same run.** The ACLs
are exactly `GITORLI\sdusers:(OI)(CI)(M)`, `BUILTIN\Administrators:(OI)(CI)(F)`
and `NT AUTHORITY\SYSTEM:(OI)(CI)(F)`, with no `BUILTIN\Users` - and this time
that was also confirmed **from the outside**, which the previous round did not
do: an ordinary unelevated session, whose token does not yet carry `sdusers`,
is refused on every path inside `C:\ProgramData\SD`. `Test-Path` on the
directory itself still answers True, because listing the parent is permitted;
only the contents are denied. Anyone checking this should look inside rather
than at the directory entry. Also present: `sdusers` created with `GITORLI\don`
in it, `user_accounts`, `group_accounts` and `shm` created, exactly one
`C:\Program Files\SD\usr\bin` entry on the system PATH, 15 files in
`C:\Program Files\SD`, and no `gplbld` anywhere in the data tree.

### The finding this run produced: the installer creates `sdusers`, never `sdadmins`

**Not observed, deduced - and it predicts that a clean-machine install produces
a system nobody can start.** Recorded here because it is the same shape as the
bug just fixed: invisible on this machine because of state left over from
earlier work.

`IsAdmin()` in `gplsrc/linuxlb.c` line 75 is `getgrnam(SD_ADMIN_GROUP)`, and
returns FALSE if the group does not exist - deliberately failing closed.
`SD_ADMIN_GROUP` is `"sdadmins"` (`gplsrc/sddefs.h` line 131). `gplsrc/sd.c`
line 613 refuses `sd -start` with "Command requires administrator privileges"
when `IsAdmin()` is false.

`gplbld/sd.iss` creates **`sdusers`** - for the ACL - and nothing in `gplbld/`
mentions `sdadmins` at all. So on a machine that has never had SD development
on it, `getgrnam("sdadmins")` returns NULL, nobody is an SD administrator, and
`sd -start` refuses. The postinstall `SET.PASSWORD SDSYS` step would fail the
same way, since `sd -internal` is gated identically.

Everything above ran here only because `sdadmins` was created by hand on
13 Aug 2026 and this account's token carries it. §4 already records, from an
earlier session, that `sd -start` refuses while the group is absent and
succeeds once built against a group the token holds - so the behaviour is
verified even though this particular consequence was not exercised.

**This is deliberately not fixed in this commit**, because the obvious fix
prejudges an open question. §8's "what happens to `IsAdmin()` and `sdadmins`?"
asks whether `sd -start` keeps an OS-level check at all, and if it does,
whether the right group is `sdadmins` or Windows `Administrators`. Adding two
`net localgroup sdadmins` lines to the `.iss` would settle that by accident.
The question now has a forcing function it did not have before: without an
answer the installer cannot produce a working system on a clean machine.

### Two smaller observations, neither chased down

- **`Get-Process sdlnxd` reported nothing immediately after `sd -start`**, in
  both passes, while `COUNT VOC` then worked and reported 431 records. §4
  records from 13 Aug 2026 that `sd -start` "spawned `sdlnxd`, which stayed
  running". SD itself is plainly fine - the shared segment is created and
  answered - so this is about the daemon's lifetime, not the server's. It may
  be that `sdlnxd` exits promptly when nothing needs the network layer, or that
  it was not yet visible at the moment of the check. Not investigated, and
  stated as an observation rather than a conclusion.
- **`errlog` was empty** after a full start/command/stop cycle on the fresh
  tree, where earlier sessions saw "User n (pid, don)" lines written to it.
  Also not chased.

### A note on the harness, not on SD

The first elevated pass ran everything correctly but died before writing its
own summary log, showing a burst of PowerShell errors as the window closed. The
suspicion at the time was the `sd -stop` process-group trap in §6, since that
trap's signature is exactly "the shell above it vanished with exit status
zero". **It was not that.** A second pass under `Start-Transcript`, with marker
files bracketing every `sd -stop`, reached all nine markers and ran to
completion - so `sd -stop` is behaving, and the fix recorded in §6 holds. The
fault was in the throwaway script's own logging helper, which called
`.TrimEnd()` on the result of piping an empty result set through `Out-String`.
Worth one line here only so that nobody re-opens the `sd -stop` question on the
strength of the first observation.

## Correction: 14 Aug 2026 - the installer was NOT verified for a first install

Corrects the entry "The staged tree is bootstrapped" and the §4 claim added
with it, both of which said the installer worked. **It works on the upgrade
path. A first install produced a broken database.**

`gplbld/sd.iss` gated the data tree with `Check: DataTreeAbsent`, which tested
`DirExists` directly. A Check function is evaluated **per file**. The first
file of the sdsys set created `C:\ProgramData\SD\sdsys`, every later evaluation
therefore answered False, and the remaining ~3,260 files were silently skipped.
The result: 16 files installed, no `gcat`, no `GPL.BP.OUT`, no working
database - and Setup exited 0.

**Why the first round of testing missed it, which is the part worth learning
from.** The machine already had a data tree, put there by hand earlier in the
day while testing install-by-copy. So the only path exercised was the upgrade
one, which skips the whole set consistently and looks identical whether the
Check is right or wrong. Every observable was green: exit 0, files in Program
Files, correct ACLs, SD starting and reporting 431 records - because SD was
reading the hand-made tree, not anything the installer had laid down. The test
that would have caught it is the one that had been deferred all along, and the
reason for deferring it was that the machine was not clean.

The lesson is not "test on a clean machine", which was already written down. It
is that **an install test which does not COUNT what was installed proves very
little**: every high-level check passed against a database the installer had
not written. §7 step 1 now says to count the files and not trust the exit code.

**Fixed but NOT verified.** `InitializeSetup` caches the answer once, before
any file is copied, and `DataTreeAbsent` returns the cached value. The
installer was rebuilt with the fix. It has never been run - the session ended
first, and the machine is left carrying the broken install. The state block at
the top of PROJECT_STATUS.md says what is there and how to clear it.

Two smaller findings from the same round, both real:

- **The uninstaller left a dead directory on the system PATH.** Inno cannot
  undo an appended `[Registry]` value, because the `olddata` constant means it
  cannot know which part it contributed. `RemoveFromPath` now strips it by
  name at `usUninstall`. The uninstaller otherwise did the important thing
  correctly: `C:\ProgramData\SD` survived untouched, which is what a silent
  uninstall must do.
- **A brace comment in an Inno `[Code]` section cannot mention a
  brace-delimited constant.** The comment ends at the first closing brace and
  the prose after it is parsed as code, so the error points at English several
  lines from any statement. The `(* *)` form works - and must not mention
  itself either, which ended the comment the same way and cost a second
  compile.

---

## 14 Aug 2026 - The configuration file finds itself, and the last Inno blocker goes

Instruction from the repository owner: fix the configuration lookup so it does
not need `SCARLET_CONFIG`, and if a variable is still needed, rename it to
`SD_CONFIG`. Both done. This was the last of the four things §5.16 listed as
standing between the staged tree and an Inno package.

**What it was.** The server read `SCARLET_CONFIG` and fell back to
`/etc/sd.conf`; the client library read `SD_CONFIG` and fell back to `sd.ini`
in the Windows directory, with a comment claiming the two matched. They did
not, so setting the variable you would expect configured exactly one of them.
Worse for an install: once the binaries ship with `msys-2.0.dll` beside them
the POSIX root moves to `C:\Program Files\SD\`, so `/etc/sd.conf` resolves
*inside* Program Files — read-only to ordinary users, and separated from the
data it describes. The install test on this day had to set the variable by
hand, which is not an install.

**What it is now.** Both read `SD_CONFIG`; both fall back to
`%ProgramData%\SD\sd.conf`, with the literal `C:\ProgramData\SD\sd.conf` only
as a last resort. `%ProgramData%` rather than the literal because that folder
can be relocated and the variable holds where it actually is — the same
reasoning as deriving PowerShell's path from `%SystemRoot%` earlier in the day.
`SCARLET_CONFIG` is no longer read at all: it named a project this is not part
of, and §5.16's standing rule is to convert rather than tolerate. The
`sd.ini`-in-`C:\Windows` fallback is gone too.

The two values are `SD_CONFIG_ENV` and `SD_CONFIG_DEFAULT` in `gplsrc/sddefs.h`
and are **duplicated** in `sdclilib.c`, because the client is a separate
toolchain that must not include the server's headers (§5.2). Both files say so;
change them together.

Also fixed while here: one caller of `GetConfigPath()` in `sdfix.c` passed a
201-byte buffer where every other passes `MAX_PATHNAME_LEN + 1`, so the
function's contract was whatever the smallest caller happened to be.

**Verified** with `SD_CONFIG` and `SCARLET_CONFIG` both explicitly unset: the
staged tree, installed by copying to `C:\ProgramData\SD\`, started and reported
431 records from `COUNT VOC` and `Pathname: C:\ProgramData\SD\sdsys` from
`LIST ACCOUNTS`.

**Two traps found on the way, and the second one cost the most time in this
session.**

The UCRT64 compiler needs its own `bin` directory on PATH even when invoked by
absolute path. `gcc.exe` finds its DLLs beside itself; the `cc1.exe` it spawns
does not, and resolves them through PATH. Without it, `gcc --version` works and
compiling a one-line program **exits 1 with completely empty stdout and
stderr** — which reads as a broken compiler, not a search path. The Makefile
now sets it from `$(dir $(UCRT_CC))`, so the build no longer depends on the
developer's shell.

And `make sd` lists `sdclilib` as a *prerequisite*, so when the client failed
to build, make stopped before linking `sd` — and left `bin/sd.exe` at its
previous contents. Every test after that measured a binary that did not contain
the change being tested, including a password prompt that was blamed in turn on
`$CRED`, on the CRLF fix, and on `LOGIN`, none of which had anything to do with
it. **After a build failure, check the timestamp on `bin/sd.exe` before
believing any test result.**

**Where this leaves the installer.** All four blockers in §5.16 are cleared. The
remaining work is the `.iss` itself, the `icacls` step, prompting for the SDSYS
password last, and the uninstaller's policy for `C:\ProgramData\SD\`. Two things
are still untested and both need something this session did not have: an install
onto a machine with **no development tree**, and `C:\Program Files\SD\`, which
needs elevation to create.

**State left on this machine.** `C:\ProgramData\SD\sdsys` is a freshly
bootstrapped install with **no SDSYS password and no ACLs**, and it is what SD
now reads by default. The development tree at `/usr/local/sdsys` is unchanged
but is reachable only with `SD_CONFIG=/etc/sd.conf`.

---

## 14 Aug 2026 - The staged tree is bootstrapped, and installing it found four bugs

Instruction from the repository owner: fix the staging gap and pre-bootstrap
the tree. Both done, and the tree has now been **installed and run**, which
had never happened — §4's "the installer is the least tested part of the
system" was accurate, and this is what testing it cost.

**What was built.** `gplbld/bootstrap.py` encodes the sequence that
PROJECT_STATUS §3 carried only as prose and `installsdai.sh` as line numbers.
`gplbld/stage.py --bootstrap` runs it against the staged tree, then retargets
the SDSYS account record to the production path and **checks that nothing else
in the tree embeds the build path** rather than trusting the sweep somebody did
once. `gplbld/pcode_bld.py` takes the sysdir as an argument instead of having
`/usr/local/sdsys` hardcoded.

**The staging gap was worse than "Python is required".** `gplbld/` was not
staged at all, so `bbcmp.py`, `pcode_bld.py` and the `FILES_DICTS` that
`WRITE_INSTALL_DICTS` reads were simply absent — the tree could not have been
installed on any machine, with or without Python. `FILES_DICTS` is now copied
in for the bootstrap and removed afterwards: it is a build input, not data.

**Four bugs, all found by running the thing rather than reading it.**

1. **`sd -stop` killed its own caller.** `stop_sd()` did
   `kill(uptr->pid, SIGTERM)` guarded only by `uptr->uid`, and `kill(0, ...)`
   signals the whole process group. A build script called `sd -stop` and the
   Python process driving it and the shell above that both vanished, silently,
   with exit status zero. It took three attempts to see, because every symptom
   said "the script stopped half way" rather than "something killed me". The
   liveness poll twenty lines below always tested `pid > 0`; this loop did not.
2. **An over-long `SH1` corrupted the parameter after it.** `config.c` used a
   plain `strcpy` into an 80-byte buffer and `sortmem`/`sortmrg` are next in
   the struct, so the 93-character PowerShell value overran and SD refused to
   start with "Invalid value for SORTMRG configuration parameter" — naming a
   parameter the file does not contain. `MAX_SH_CMD_LEN` is 255 now and both
   copies are checked. The other `strcpy` calls in that parser have the same
   shape and are **not** audited.
3. **A CRLF `sd.conf` corrupted every string parameter.** Only `'\n'` was
   stripped, so the carriage return stayed on the value and `SDSYS` became
   `C:\ProgramData\SD\sdsys\r`. Numeric parameters were fine because `sscanf`
   stops at the `\r`, which is what made it look like a path fault. It could
   only ever appear in the *shipped* configuration, never the developer's own
   hand-written LF one - the worst place for a bug to hide.
4. **`ACCOUNTS` records are newline-delimited, not `\xfe`-delimited**, being a
   directory-type file. Rewriting field 1 with the DH field mark flattened the
   record and discarded the account name and the grant list. Caught by looking
   at the bytes, not by any check.

**And three corrections to the recorded bootstrap sequence**, which had rotted
without anyone knowing:

- The last three steps need `-internal`. Written as plain `sd RUN ...` and
  `sd THIRD.COMPILE`, they now sit at the `Account:` prompt that §5.6
  introduced on 13 Aug 2026 and the connection is terminated. Nobody had
  re-run the bootstrap in between.
- `sd -i` completes its work and then dies on signal 6, so its exit status is
  meaningless and the step is judged on what it created.
  `installsdai.sh` had commented the line out, which is why this never showed.
- `THIRD.COMPILE` compiles dictionary I-types and prints no "n error(s)"
  summary, so a build check that demands one fails on a healthy system.

**Verified.** The full bootstrap ran against the staged tree, `SECOND.COMPILE`
compiling 190 programs with no errors. The tree was then installed by copying
to `C:\ProgramData\SD\` and run from the staged binaries: `COUNT VOC` reported
431 records, `WHO` reported `2 SDSYS`, and `LIST ACCOUNTS` showed the
production pathname with the account name and grant list intact. **No Python
and no compiler were used at install time.**

Not proved: the machine still has a development tree, so an accidental
dependency could still be hiding; and `C:\Program Files\SD\` was not used,
since creating it needs elevation. The install also had to be told where its
configuration was, because the compiled fallback `/etc/sd.conf` resolves inside
`C:\Program Files\SD\` once the POSIX root moves. That is the last Inno
blocker and it is now the top of §7.

---

## 14 Aug 2026 - PowerShell becomes the shell, and two standing rules

Follows directly from the entry below, which found that `OS.EXECUTE` ran
`/bin/bash -c` while an installed SD ships no shell. Instruction from the
repository owner: point `SH1` at PowerShell and update the `OS.EXECUTE`
strings.

**It simplified the code rather than complicating it.** The five programs
written earlier the same day each built a PowerShell script and then wrapped it
in bash single quotes to protect it. With PowerShell as the shell the command
*is* the script, so the wrapper and the `>/dev/null 2>&1` came out of all of
them. `!ps_script` changed most: it used to `cat` its temporary file into
PowerShell's stdin, and now names the file **relative to the working
directory** — which removes the need for a Windows pathname that BASIC has no
way to produce, and makes it work whether SDSYS sits at a POSIX path or a
Windows one.

`op_sh.c` derives the PowerShell path from `%SystemRoot%` rather than writing
`C:\Windows`, because the system drive is not guaranteed. It must contain no
spaces: `clparse()` splits on them and does not honour quotes, which rules out
naming PowerShell through anything in Program Files.

**Two measurements decided the design, rather than assumption.**
`Invoke-Expression` propagates a script's exit status and `& .\script.ps1`
does not — a script ending `exit 7` gave 7 through the first and 1 through the
second. `Invoke-Expression` also runs text rather than a file, so the execution
policy does not apply and nothing needs `-ExecutionPolicy Bypass`. Both probes
were re-run afterwards with bash out of the loop: `is_grp_member` 7 of 7,
`ps_script` 5 of 5.

**Two standing rules were given at the same time and are now §5.16.** Every
remaining Linux-ism is to be converted to its Windows equivalent where one
exists, rather than wrapped or tolerated — `/bin/bash` is the cautionary case,
since it looked like an inert default and silently broke every installed
system. And where Linux parity conflicts with the Inno installer, the installer
wins. That second rule settles the pre-bootstrap question in the installer's
favour: the staged tree ships `gcat`, `GPL.BP.OUT` and `PCODE.OUT` empty today,
which would make an end user run the BASIC bootstrap with Python and a
compiler, and that is not something an installer should do.

§5.16 carries the working list of Linux-isms still in the tree and what
"Inno compatible" requires, in dependency order.

---

## 14 Aug 2026 - OS accounts come back, and the shell they need is missing

Covers the working tree at the time of writing; committed in the same change as
this entry.

**A decision was reversed by the repository owner.** PROJECT_STATUS §5.6 said
"Create no OS users and no OS groups at all", on the reasoning that OS account
creation was Linux baggage that did not transfer. The owner's position, stated
on 14 Aug 2026: the *linkage* between an SD account and an OS user is worth
keeping, and Windows offers the same thing through `net user` and
`net localgroup`. The original reasoning was wrong about what was Linux
specific — the mechanism was, the intent was not.

**Read the reversal narrowly.** Provisioning came back; authorisation did not.
Every account still carries its own password, SDSYS is still the only
administrator, and `LOGIN` was not touched. The owner asked for the `sdusers`
login gate back "if it is possible", and it now is — but restoring it is a
separate act, and it pulls against §5.6's "administration is a matter of knowing
the SDSYS password" in a way that is not yet resolved. That tension is recorded
rather than silently decided.

**What was built.** `GPL.BP/CREATE_USER` (`New-LocalUser`),
`GPL.BP/DELETE_USER` (`Remove-LocalUser`), `GPL.BP/SET_PASSWD` (`Set-LocalUser`,
prompting inside SD), `GPL.BP/OS_GROUP` (the four group operations behind one
subroutine, per §5.14), `GPL.BP/PS_SCRIPT` (run a script carrying a secret), and
`GPL.BP/IS_GRP_MEMBER` rewritten. Call sites in `CREATEA`, `DELACC` and
`MODIFYA` swapped. All ten compile clean.

**Three findings, in the order they matter.**

1. **`OS.EXECUTE` needs a shell an installed system does not have, and this is
   not new.** `op_sh.c` defaults to `/bin/bash -c`; `gplbld/stage.py` ships no
   shell. On an installed tree `/bin/bash` resolves inside `C:\Program
   Files\SD\` and is not there. So every `OS.EXECUTE` in the system fails once
   installed, while working perfectly in development. It was found by asking
   whether the new work would survive the Inno installer — a question worth
   asking earlier than it was. Now a trap in §6, with three options and no
   decision.
2. **Elevation is a hard constraint, not a detail.** An ordinary SD session has
   a UAC-filtered token — `BUILTIN\Administrators` present as "Group used for
   deny only" — and `net localgroup ... /add` answers "System error 5. Access is
   denied." Measured, not assumed. Every helper tests for elevation explicitly
   and returns status 5, rather than parsing a localised message.
3. **Windows `sudo` is not Linux `sudo`.** `sudo.exe` ships on build 26200 but
   is disabled by default and enabled from Developer Settings. There is no
   sudoers file and no per-command policy: it asks UAC to elevate your own
   token. "Only the sdsys user can `sudo sd`" holds, but through Administrators
   membership and UAC, not policy. Worth writing down because the Linux
   intuition is misleading here.

**Passwords stay off the command line.** `net user <name> <password> /add` would
expose the password to any local user through Task Manager, `Get-CimInstance
Win32_Process` or ETW — the pattern §8 already rejected for batch login. The
owner chose a temporary script file instead. `!ps_script` writes it inside the
SDSYS directory, where §5.7's ACL inheritance protects it with no permission
call of its own; that is the first practical use of the "noacl breaks chmod but
not inheritance" finding.

**Correction to an earlier instruction.** §6 said the fix for `is_grp_member`
was "to delete these calls, not repair them". That was written when SD was
expected to stop touching OS groups. The routine was repaired instead: it asks
`Get-LocalGroupMember` and distinguishes member, not-a-member and no-such-group
by exit code, which parsing `net localgroup` output cannot do without depending
on the language Windows is installed in. Seven cases verified from inside SD.
Note it costs a bash plus a PowerShell start on a path that runs at every login;
the fast answer is `getgrnam()` behind a KERNEL key, which is known to work but
is new C code.

**Also done, and it was §7 step 2.** `!valid_os_path` accepts backslashes and
spaces, so `C:\Program Files\SD\usr\bin` passes and the binaries can move. 16
cases verified. The protection moved to the call site, which single-quotes:
single rather than double, because bash still reads a backslash as an escape
inside double quotes, so a path ending in a separator would escape the closing
quote.

**What was deliberately not done.** No Windows account was created or deleted —
`sudo` is disabled here, and throwaway OS accounts were not made without the
owner's say-so — so none of the account operations have ever run. `CREATEA`
still carries `sudo chmod g+s`, which is meaningless on Windows and will warn on
every account creation; it goes with §5.7's `icacls` step, whose inheritable
ACEs are its real equivalent.

---

## 13 Aug 2026 — Second prune of PROJECT_STATUS, and the §5.6 reasoning moved here

Rollover, not new work, at the end of the session. PROJECT_STATUS had reached
2123 lines against the ~2000 in §0 rule 5. Trimmed: §4's `LOGTO` case-by-case
table and the escalation program listing (both duplicated entries already in
this file), §5.1, §5.5, §5.8's `sdrealpath` correction, §5.11's purge account
and §5.15's itemised removal list — all of which describe finished work whose
detail is here. §5.6's "what is still missing" list was split, since several of
its bullets described work that was subsequently done.

The one piece that was **moved rather than trimmed** is below: §5.6's reasoning
was not recorded anywhere else, so it is set out here in full before being
reduced to conclusions in PROJECT_STATUS. §5.6 had grown to 255 lines, most of
it the *why* behind decisions that are now built and verified. Nothing was
dropped.

### Why the identity model has the shape it does

### You log in as yourself, then move; the login identity follows you

This is how shared access works and it is what makes it attributable:

- A person logs in with **their own account name and password**. That
  establishes the session identity.
- Access to other accounts is **granted, not shared**. Once in, a person may
  `LOGTO` any account they have been given access to. There is no second
  password to know and none to share.
- **`@logname` does not change on `LOGTO`.** The login identity persists for
  the life of the session, which is the whole mechanism — everything
  downstream attributes to the person who authenticated, not to the account
  they are standing in.
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

### Why the step-up asks for your own password, not an SDSYS one

`LOGTO SDSYS` requires a password again — the one exception to "granted, not
prompted" — on the grounds that entering administration deserves a deliberate
act rather than an unguarded session becoming an administrative one.

**The password it asks for is the person's own.** This matters and is easy to
get backwards. Re-entering your own credential is re-authentication: it
confirms the person at the keyboard is still the one who logged in, changes
nothing about attribution, and introduces no new secret. An SDSYS password
would be a second shared secret held by every administrator, which is precisely
the OpenQM weakness this model exists to remove — the audit log would still
name the person, but the credential behind the most privileged account in the
system would be shared, and unrotatable without telling everyone.

Log the step-up separately from the `LOGTO` itself, both when it succeeds and
when it fails; a failed step-up is the single most interesting line in the
audit trail.

### Why the credential register is a separate file

`$CRED` is not part of the ACCOUNTS record and must stay that way. `LOGIN`
opens `ACCOUNTS` at line 175, in the user's own process, **before** any
authentication — it must, to know the account exists — and eleven other
programs open it too, including `_VOC_REF` for routine resolution. Verifiers
stored there would let any user pull every account's Argon2 hash and attack it
offline.

In stage 1 `$CRED` is still readable by everyone, since Windows has no setuid
and there is no privileged helper short of §5.7's service, so this does not fix
the exposure. It makes the boundary **exist**, so that §5.7 can later lock one
file to the service account without restructuring ACCOUNTS or migrating data.

## 13 Aug 2026 — Correction: the API server does have a credential check, and it cannot work

Investigation, no code. Prompted by the repository owner's background on
OpenQM: it was very insecure, remote access worst of all, telnet was replaced
with ssh only, and the API never got the same treatment. Since §1 now makes the
API the front door, the question moved to the top.

### Correction

§5.6 and §7 step 6 both said the API server "has no credential check of its
own". **That is wrong.** `APISRVR` line 921 calls `login(username, password)`,
which reaches `op_login()` and then `login_user()` in `linuxio.c`. There are
two paths and the port breaks each in an opposite direction:

- `APILOGIN=1`, which is what `sd.conf` ships, reads `PASSWD_FILE_NAME` —
  `/etc/shadow`. **MSYS2 has neither `/etc/shadow` nor `/etc/passwd`**, the
  same NSS change behind the `is_grp_member` trap. `fopen` returns NULL and it
  returns FALSE, so every API login is refused. The API is **closed, not
  open** — which is the good version of broken, but it means the interface the
  product now exists for does not function at all.
- `APILOGIN=0` skips passwords entirely and trusts `getpeereid()` on an AF_UNIX
  socket — mab's Feb 2024 hardening, and the right model. But **MSYS2 emulates
  AF_UNIX over a TCP loopback socket with a handshake file**, so it is not a
  filesystem object with permissions and "local socket" means much less than
  it does on Linux.

What is genuinely missing, as opposed to broken, is authorisation *after*
connect: `SrvrAccount` reaches any account by name and `@logname` comes from
the client. Both now written into §7 step 6 as ordered work.

### The exposure question, recorded as an open question rather than a decision

The repository owner raised a web front end as a way to make all API access
local — SD behind it, never on the network. Recorded in §8 with three postures
(SD's socket exposed; ssh tunnel; web front end) and, deliberately, with the
argument **against** the web front end given equal weight, because it is the
repository owner's own and it is a serious one: web servers invite attack,
every attacker knows how, scanning is constant and automated, and a custom
protocol on a non-standard port does not attract the same volume. Obscurity is
not security but it is a real reduction in opportunistic traffic.

The counter recorded alongside it is that a web tier does not add network
exposure, it moves it — the comparison is IIS exposed versus `APISRVR` exposed,
and `APISRVR` is 2007 code with fixed 32-byte credential buffers that nobody
has fuzzed. But that argument only beats the status quo, not the ssh tunnel,
which exposes nothing either.

The observation that may settle it: **§1 points at the tunnel.** If the target
user is a Windows developer using SD as a back end, their application is the
front end. SD does not need a web tier to be secure, it needs to stop listening
on the network. Whether SD offers a browser UI is then a product question, and
separating the two is probably what makes either decidable.

Two constraints recorded for whichever posture wins: attribution has to survive
the extra hop, with the front end asserting identity and SD still enforcing the
grant list; and connection pooling breaks `@logname` regardless of `NUMUSERS`,
which is only a default — the repository owner notes OpenQM systems run several
hundred users.

### The network-layer argument, added the same day

The repository owner's second point for the API posture: with a private API you
keep VPN, IP restriction and similar controls that a public web server forfeits
by definition. Recorded in §8, with the structural form of it — a public web
application must accept anonymous connections as far as the login page, so its
TLS stack, HTTP parser, router, session handling and password reset are all
reachable pre-authentication by everyone, while an IP-restricted API has a
pre-authentication surface reachable by nobody. That is a difference in kind
rather than obscurity.

Recorded alongside it, so the record is not misread later: the axis is *public
versus private*, not web versus API. A web front end on an internal network
keeps the same controls, so C's security cost over B is a second codebase to
patch rather than an exposed one.

**And the finding that makes this actionable: SD never binds a listening
socket.** `sd -N` runs per connection with the socket as stdin and stdout —
**xinetd** bound port 4243, spawned per connection and supplied `only_from`.
xinetd does not exist on Windows, so the service replacing it inherits the bind
address, the port, per-connection spawning and access control, and none of it
is implemented. The recommendation recorded is to **bind loopback by default**,
so posture B is what a default install gets without anyone deciding, and to
settle whether `only_from` is reimplemented or replaced by a Windows Firewall
rule written at install time. This also explains why §8's note about keeping
`etc/xinetd.d/` as documentation of the service topology was worth following.

## 13 Aug 2026 — Embedded Python removed; SD is a back end for the API

Decision from the repository owner on 13 Aug 2026, prompted by the staging
script's warning about the 195 MB Python standard library. The answer was not
"ship it" or "trim it" but that embedded Python was never what this is for:
**SD for Windows is a back end data store for Windows developers, reached
through the API.** Recorded as §5.15, and as a scope statement in §1 because it
is the tie-breaker for anything else that asks whether a feature earns its
place.

### Why it was a removal, not a flag

`-DEMBED_PYTHON` looked like a one-line change on `Makefile:73`. It is not:
`gplsrc/sdext_py.c` and `gplsrc/op_sdpyobj.c` carry **no `EMBED_PYTHON` guards
at all** and are listed in `gpl.src`, so they cannot compile without the Python
headers however the flag is set. Removing the flag alone would have broken the
build. And CLAUDE.md's rule against `#ifdef` branches for dead platform code
applies in spirit, so the whole thing went:

- `gplsrc/sdext_py.c`, `gplsrc/op_sdpyobj.c`, `gplsrc/sdext_python_inc.h`, and
  their two entries in `gpl.src`
- the `EMBED_PYTHON` blocks in `op_sdext.c` and `sd.c`
- `PY_HDRS`, `PY_LDFLAGS` and `-DEMBED_PYTHON` in the Makefile
- 20 `GPL.BP/PY_*` programs, `SYSCOM/SDPYFUNC.H`, 4 `sdsys/BP/PY_*` tests
- the `SD_Py*` error codes in `gplsrc/err.h` and the `SD_Py*`/`SD_Obj_*` SDEXT
  keys in `SYSCOM/KEYS.H`

`gplbld/gen_includes.py` regenerated `SYSCOM/ERR.H` and `GPL.BP/ERRTEXT.H` from
the edited `err.h` without being asked twice, which is the first real use of
the tool written earlier the same day.

### Two things that bit, both now traps in §6

**The opcode table is positional.** `kernel.c` builds its dispatch table from
`opcodes.h`, so deleting `op_sdpyobj` broke the link. Deleting the `_opc_` line
would have been far worse — it renumbers every opcode after `0xCFFE` and
invalidates all compiled pcode everywhere. The file's own convention is to
retire an opcode in place by pointing it at `op_illegal` with a generic name,
as `OP_09`, `OP_9E` and `OP_BB` already do; `OP_CFFE` is now one of them.

**And `BCOMP` has a parallel positional list.** It registers intrinsics in
`int.intrinsics` and dispatches through an `on i goto` whose entries are
matched **by position**. Removing `SDPYOBJ` from one without the other would
have silently misrouted every intrinsic after it — a fault that compiles
cleanly and produces wrong code. Both were removed in the same edit.

Also met: the Makefile does not track header dependencies, so editing
`opcodes.h` left a stale `kernel.o` and the link failed pointing at
`kernel.c`, a file that had not been touched.

### Verified

- `make sd` from clean links with no Python, and `objdump -p bin/sd.exe` no
  longer names `msys-python3.12.dll`.
- `SECOND.COMPILE` compiled **187 programs with no errors** — 207 less the 20
  `PY_*` programs, exactly as expected — after recompiling `BCOMP` first,
  since the intrinsic table changed.
- `COUNT VOC` still reports 432 records, `WHO` reports `SDSYS`, and
  `COUNT NOSUCHFILE` still expands to "File not found".
- The staged tree fell from **16.2 MB to 9.6 MB**, and the DLL closure from
  seven to four. `msys-intl-8` and `msys-iconv-2` went too: they were only ever
  present because Python pulled them in.

### What else it took with it

`python-devel` and `gettext-devel` leave the build dependencies (§2).
`gettext-devel` was only ever there because `python3-config --ldflags --embed`
emits `-lintl`, so an unrelated-looking dependency disappeared with the
interpreter. Plain `python` stays: `gplbld/bbcmp.py` is the only thing that can
compile BASIC before a BASIC compiler exists. It is a developer dependency —
an installed system needs no Python at all.

### Consequence to weigh

If the API is the primary interface, §7 step 6 — bringing `APISRVR` under the
identity model — matters more than its position suggests. `APISRVR` has **no
credential check of its own** and its `logname` comes from the client, so any
session it accepts reaches any account by name. That was tolerable as a side
entrance. As the main door it is not. Flagged, not reordered; that is the
repository owner's call.

## 13 Aug 2026 — Staging script written, and it immediately found an install blocker

First cut of `gplbld/stage.py`, §7 step 3a. It assembles both install roots
from an explicit whitelist, computes the MSYS2 DLL closure, writes `sd.conf`
and `etc\fstab`, and emits a `MANIFEST.txt` outside both roots so two builds
can be diffed. 3087 files, 16 MB.

### The whitelist justified itself on the first run

Within minutes of the first staged tree existing, running `sd.exe` from it with
MSYS2 off PATH surfaced something that no amount of reading would have found:

> Warning: '/dev/shm' does not exists or is not a directory.

**Shipping `msys-2.0.dll` beside the executable relocates the entire POSIX
namespace.** The runtime derives its root from the DLL's own directory by
stripping **two** path components — matching MSYS2's `<root>\usr\bin`. This was
guessed wrong twice (parent-of-DLL-directory, then DLL-directory) before being
measured directly with `cygpath -w /` against the staged tree:

| `msys-2.0.dll` at | `/` becomes |
|---|---|
| `<X>\SD\usr\bin\` | `<X>\SD\` |
| `<X>\SD\bin\` | `<X>\` |
| `<X>\SD\` | the parent of `<X>` |

So `/dev/shm`, `/etc/sd.conf` and `/tmp` all move with the DLL. §5.8 said
"binaries and the MSYS2 DLLs beside them in `C:\Program Files\SD\`", which
would have put the POSIX root at `C:\Program Files\` and required creating
`C:\Program Files\dev`. The layout table now says `C:\Program Files\SD\usr\bin`
and the reason is recorded in §6, because it looks like gratuitous Unix-ism
and will otherwise get "tidied up" by a future session.

**Second problem, following from the first.** `/dev/shm` cannot live under
Program Files at all: `shm_open()` creates files in it, so every SD user needs
write access, and Program Files is read-only to ordinary users by design.
Cygwin reads `<root>\etc\fstab`, and a bind entry moves it — verified working:

```
C:/ProgramData/SD/shm /dev/shm ntfs binary 0 0
```

With that in place the staged `sd.exe` ran on a `PATH` of
`C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem` — no `msys64`, no Git
for Windows — and answered `SD is not active.` with no warnings and exit 0.
That is the correct answer, not a failure: the running server's shared segment
belongs to the `msys64` POSIX root and the staged process has its own, which is
the §6 PATH trap behaving exactly as documented.

### What the closure turned out to be

Seven MSYS2 DLLs for the server — `msys-2.0`, `msys-crypt-2`,
`msys-python3.12`, `msys-intl-8`, `msys-iconv-2`, `msys-gcc_s-seh-1`, and
`libsodium-26` from `/usr/local/bin` because it is built from source. Only
`kernel32` and `ntdll` come from Windows. Three of the seven are reachable only
transitively, so direct imports would not have been enough — `objdump -p`
walked recursively, rather than `ldd`, so the answer does not depend on the
loader's search order and would be the same on a machine that could not run the
binary.

`sdclilib.dll` needs **nothing** but Windows system DLLs, which confirms §5.3's
claim about the two toolchains by measurement rather than by assertion.

### Left open

- **The embedded Python standard library is not staged.**
  `msys-python3.12.dll` is in the closure so `sd.exe` loads, but
  `usr/lib/python3.12` is 195 MB and the `PY_*` family will fail without it.
  Ship it, ship a subset, or make `EMBED_PYTHON` optional — undecided, and the
  script prints a warning saying so rather than quietly omitting it.
- `sdsys/BP` ships and contains test programs. The Linux install did the same.
- Nothing sets ACLs yet; that is installer work, not staging.
- **No install has been done from the staged tree.** The run above proves the
  binaries load, not that an install works. Step 3b is still ahead.

## 13 Aug 2026 — Installer: the shell script port is dropped

Decision from the repository owner on 13 Aug 2026, **reversing** the revision
made earlier the same day and recorded in §5.9 as "Two installers, in order:
build-from-source now, Inno Setup later". No code; §5.9 and §7 step 3 rewritten.

### What changed

`installsdai.sh` and `deletesdai.sh` will **not** be ported to Windows. Two
scripts replace them: one that builds a **staging directory** containing
exactly what an install consists of, and one that turns that directory into an
**Inno Setup installer**. The pattern is one the repository owner has used on
another project.

The position has now moved three times, which is worth setting out so a future
session can see it was deliberate rather than drifting:

1. Go straight to Inno Setup, `installsdai.sh` being apt/dnf/zypper, systemd,
   xinetd and `/etc` throughout.
2. No — do the Linux method on Windows first: download, install dependencies,
   compile, install, as a development tool.
3. No — skip it. What that would produce is a *developer* setup script, and §2
   and §3 already serve that reader. The bootstrap sequence, which is the part
   with real value, has to be driven by whichever installer gets written, so
   it is written once either way.

### Why the Linux script existed — the point that settles it

From the repository owner, and this is the part that should stop the question
being reopened. `installsdai.sh` was **not** a developer convenience on Linux;
it was load-bearing. ScarletDME targeted Fedora, Debian, Arch and OpenSUSE
across several versions each, every one with a different compiler, libc and set
of package names. No single binary works across that spread, so **the end user
had to compile**, and the script existed to abstract apt from dnf from pacman
from zypper and drive a build on the user's own machine.

None of that holds on Windows. There is one target, one ABI, and SD ships its
own runtime beside `sd.exe` (§5.8), so there is nothing to adapt to and the
user needs no compiler. Strip the distro handling out of `installsdai.sh` and
what remains is a developer setup tool covered by §2 and §3 already. The
requirement that justified the script is a Linux-specific one that the port
does not inherit — so this is a case where the Windows install ends up
genuinely simpler than the Linux original, which is not true of much else here.

### Why the staging script is the valuable half

Not mainly packaging. Three reasons, and the middle one is the strongest:

- It makes §5.8 executable. The install layout is prose in PROJECT_STATUS; a
  staging script is that layout in a form that either runs or does not, and it
  forces the `<sysdir>/bin` split to be decided rather than remembered.
- **It is a whitelist, and whitelists find accidental dependencies.** `gplsrc`
  sat in the data tree for as long as it did because `installsdai.sh` copied it
  wholesale and nobody asked why — a fault that cost most of a session earlier
  the same day. A script that copies only what is on an explicit list,
  installed onto a machine with no development tree, surfaces that class of
  problem immediately. The installer is the least tested part of the system;
  making it cheap to rerun is what changes that.
- It is where the MSYS2 DLL closure gets **computed by walking the imports**
  rather than guessed. Missing one gives exit code 53 and no message at all.

### Corrections to §5.9 as it stood

- It said the Inno Setup compiler was **not installed**. It is installed on
  this machine.
- It framed the shell-script port as what was wanted first. That is reversed.

### Kept from the old scripts

`deletesdai.sh` is not ported but should be **read** before an uninstaller is
written. Inno supplies an uninstaller; it does not answer what happens to
`C:\ProgramData\SD\`, which holds the user's database. Removing it on uninstall
is a catastrophe and leaving it makes reinstall awkward, because accounts and
`$CRED` are already there. The old script is where the current answer is
recorded.

### Numbering

§7 step 3 is now the staging script and Inno pair, absorbing what was step 9;
steps 9 to 13 shifted down by one. Steps 1, 2 and 4 to 8 are unchanged. The
staging script still cannot jump the queue — step 1 has to settle the layout
for it to have something to stage, and step 2 has to fix `VALID_OS_PATH`,
which rejects both the space and the backslash in `C:\Program Files`.

## 13 Aug 2026 — §3 of PROJECT_STATUS pruned

Housekeeping, recorded so a future session knows the section was shortened
deliberately rather than left incomplete. §3 went from 175 lines to 113, and
the file from 1814 to about 1750.

**Nothing was moved, because everything cut was already here.** What went was
the narrative of a completed bring-up: the `gcat/$CPROC` placeholder
investigation and the `is_bootstrap` red herring (this file, "SD runs. Full
bootstrap completes", and the entry above it), the step-by-step account of what
each bootstrap command produced, the correction of the earlier "`sd -i` blocks
silently" report, and the note that the `/etc/group` blocker had gone. §3 also
still opened with "SD still does not start", three paragraphs above the text
saying it does — stale wording that had survived two sessions.

What was kept is what a session needs to act: the build commands, the bootstrap
sequence itself with the two counter-intuitive steps flagged and a pointer here
rather than an explanation, the state of this machine including every password
and scratch account, and the scripted-session pattern. The "laid down already"
and "machine as this session ended" tables were merged, since the second had
overtaken the first.

The trigger was rule 5 in §0 — the file was at 1814 lines against a ~2000
rollover — but the reason to do it now rather than at 2000 is the rest of that
rule: work had just landed, so the instructions that had been carried out were
the easiest thing in the file to shed.

## 13 Aug 2026 — Batch login raised and designed; admin helpers set as a goal

No code. Two things from the repository owner, both recorded in
PROJECT_STATUS.md rather than here because both are still ahead of the work:
the full reasoning for the first is in §8 under "how does a scheduled job log
in", and the second is §5.14.

**Batch login.** Every account now carries a password (§5.6), which breaks the
`sd -internal SECOND.COMPILE` shape the install script uses and the cron jobs MV
users expect. The design chosen is the repository owner's: an `ALLOWED` item in
SDSYS's VOC listing `ACCOUNT, VOC name` pairs, so that only an administrator can
authorise unattended work, paired with a batch account that grants nobody so
that only an administrator can maintain what runs. It needs no new C code —
`SYSTEM(1026)` already exposes the command line to `LOGIN`.

Recorded here mainly so the alternatives are not proposed again: a password on
the command line is readable by any local user; a password file works and could
be made defensible but a capability list beats a stored credential; and hashing
the VOC entry to detect tampering pins one hop only, because a transitive
closure discovered at run time cannot be hashed. §8 carries the reasoning and
the constraints that came out of working it through.

The install half of the problem turned out not to be a problem: `LOGIN` admits
an administrator to an account with no verifier yet, so an installer that sets
the SDSYS password **last** needs no credential during the bootstrap. That is
now an ordering requirement on §7 step 3.

**Admin helpers.** A goal for after the system runs well: forms in place of
remembered command lines and hand-edited records. The part that matters before
then is the sequencing rule it implies — put administrative logic in
subroutines with a verb over it, so a form can call the same code later. §7 was
renumbered to add both; steps 1 to 9 are unchanged.

## 13 Aug 2026 — The data tree no longer holds C source, and `ERRGEN` turned out to be booby-trapped

Carries out §7 step 1, parts a, b and c. The data tree can now be built and
compiled with `gplsrc`, `gplobj` and `gplbld` absent, which was the blocker on
moving SDSYS to `C:\ProgramData\SD\`.

### What changed

- `GPL.BP/APISRVR` lines 64-65, the `$execute 'BASIC GPL.BP REVSTAMP'` and
  `$execute 'RUN GPL.BP REVSTAMP'` pair, are commented out, exactly as
  `GPL.BP/CPROC` 139-140 already were. `$include revstamp.h` stays.
- `GPL.BP/ERRTEXT` line 33, `$execute 'RUN GPL.BP ERRGEN'`, is commented out
  for the same reason. **This one was not known about** — see below.
- New `gplbld/gen_includes.py` replaces both generators at build time. It
  regenerates `GPL.BP/REVSTAMP.H` from `gplsrc/revstamp.h`, and `SYSCOM/ERR.H`
  and `GPL.BP/ERRTEXT.H` from `gplsrc/err.h`. `--check` reports drift without
  writing, ignoring the generation timestamp.
- The three generated files are regenerated in the repository, which is what
  the drift below made necessary.

### The second `$execute`, which cost the session most of its time

Running `SECOND.COMPILE` with `gplsrc` absent did not simply succeed. It failed
several programs in, with `Unassigned variable ER$ARGS at line 60 of $CATALOG`
— a **run time** abort in a program that had just compiled with no errors.

The cause was `GPL.BP/ERRTEXT`, which carries `$execute 'RUN GPL.BP ERRGEN'`.
`ERRGEN` is a build tool of the same family as `REVSTAMP`: it reads
`./gplsrc/err.h` and writes `SYSCOM/ERR.H` and `GPL.BP/ERRTEXT.H`. Its
statement order is the problem:

```
   openseq 'GPL.BP', 'ERRTEXT.H' to out.f ...
   weofseq out.f                                  <- truncates output 1
   openseq 'SYSCOM', 'ERR.H' to syscom.f ...
   weofseq syscom.f                               <- truncates output 2
   ... writes three header lines to out.f ...
   openseq "./gplsrc/err.h" to in.f else abort    <- only now reads its input
```

With `gplsrc` absent it truncated both outputs and then aborted. `SYSCOM/ERR.H`
was left at **zero bytes**, so every `ER$` constant in the system became
undefined. That does not fail a compile — it produces
`WARNING: ER$ARGS is not assigned a value` and a `0 error(s)` result — so the
compile reported success and wrote broken objects into the global catalogue.
`$CATALOG` and `$BCOMP` were among them, which meant the compiler chain had to
be repaired before anything else could be recompiled. Recovery is in §6 of
PROJECT_STATUS.md.

The lesson is not about `gplsrc`. It is that **a missing `$define` in SD is a
warning at compile time and an abort at run time**, in a program that may not
run until much later.

### The generated files had drifted, and `ERRGEN` would have destroyed the drift

Porting `ERRGEN` and `REVSTAMP` to Python and diffing the output against the
tracked files showed how far they had come apart:

- `GPL.BP/ERRTEXT.H` was generated on 1 Jul 2024 and matched byte for byte for
  all 199 of its entries — and was missing the 42 error codes added to
  `gplsrc/err.h` since. Those errors had no text at all.
- `SYSCOM/ERR.H` matched byte for byte for 199 of its 241 `$define` lines. The
  other 42, the `SD_*` crypto, SDEXT and embedded-Python codes, had been
  **hand-edited**: they kept the C spelling (`SD_Mem_Err` rather than
  `SD$Mem.Err`) and, more seriously, carried the **opposite sign** to the C
  header. `gplsrc/err.h` says `-10100`; the BASIC copy said `10100`.
- `GPL.BP/REVSTAMP.H` was missing one history line. The `$define`s agreed.

Nothing in the BASIC layer references any of the 42 names — the `SD_EUID_SET`
and `SD_EUID_RESTORE` used by `GPL.BP/EUID_SET` and `EUID_RESTORE` are SDEXT
function keys from `SYSCOM/KEYS.H`, values 102 and 103, not error codes — so
regenerating was safe, and it makes the BASIC copy agree with the C.

Note what this means about the `$execute` that was removed: it ran `ERRGEN` on
**every compile of `ERRTEXT`**, so any such compile on a tree that still had
`gplsrc` would have silently overwritten those hand edits. The directive was a
hazard quite apart from the data-tree question.

### Verified this session

- `SECOND.COMPILE` compiled **207 programs with no errors** against a
  `<sysdir>` with `gplsrc`, `gplobj` and `gplbld` moved away — twice: once with
  the original headers and again after regenerating them. (207 rather than the
  204 recorded earlier because the credential programs were added since.)
- `COUNT VOC` still reports 432 records, `WHO` still reports `SDSYS`, and
  `COUNT NOSUCHFILE` still expands to "File not found", which exercises
  `!ERRTEXT` and so the regenerated `ERRTEXT.H`.
- `gen_includes.py --check` reports all three files in sync after the
  regeneration, and reported each of them stale before it.

### Still open

- **`GPL.BP/OPGEN` is not ported.** It generates `GPL.BP/OPCODES.H` from
  `gplsrc/opcodes.h` and reads `./gplsrc` the same way, but **nothing ever
  `$execute`d it** — it is a manual tool, so it did not block this work and
  removing `gplsrc` does not break any compile. It cannot be run on an
  installed system any more, so it must be ported before opcodes can be
  regenerated. It was left alone deliberately rather than ported badly: its
  hex formatting has behaviour that reading the source does not settle
  (`OP.STOP` is commented `;* 00` while `OP.ABORT` is `;* 1`, from the same
  `oconv(value, 'MX')`), and a wrong opcode table is not a failure that
  announces itself.
- **`WRITE_INSTALL_DICTS` still reads `@sdsys:"/gplbld/FILES_DICTS"`.** It is
  an install-time step rather than part of `SECOND.COMPILE`, so it did not
  affect the test above, but it is the last thing that wants `gplbld` in the
  data tree and the installer work has to deal with it.
- The move itself — `SDSYS` to `C:\ProgramData\SD\` and the binaries to
  `C:\Program Files\SD\` — is unblocked but not done.

## 13 Aug 2026 — Correction: `gplsrc` in the data tree was a misdiagnosis. Session ended on credits

**Session ended here, mid-investigation but at a clean stopping point.** The
next session's first move is §7 step 1a, which is a two-line edit. Everything
below is what was learned; nothing was changed in the code for it.

### The decision

The repository owner chose the **data-only** option for
`C:\ProgramData\SD\`: no `gplsrc`, no `gplobj`, no `gplbld` in the database.
So `REVSTAMP`'s dependency on `./gplsrc/revstamp.h` had to be removed rather
than relocated — and investigating how showed the dependency is much smaller
than this file claimed.

### Correction to §6

§6 said "the runtime tree needs `gplsrc`, `gplobj` and `gplbld/FILES_DICTS`",
on the evidence that `installsdai.sh` copies all three and that
`SECOND.COMPILE` aborts at APISRVR without them. The symptom was real; **the
diagnosis was wrong**. What actually happens:

- `SECOND.COMPILE` is a paragraph: `TERM 120,9999` then `BASIC GPL.BP *`. It
  compiles everything and runs nothing.
- `APISRVR` lines 64-66 are `$execute 'BASIC GPL.BP REVSTAMP'`,
  `$execute 'RUN GPL.BP REVSTAMP'`, `$include revstamp.h`. The second is a
  compile-time directive that **runs** REVSTAMP, which opens
  `./gplsrc/revstamp.h`. That is the whole of it — one file, two lines.
- `CPROC` carries the identical pair **already commented out** (139-140),
  with mab's note that the build should compile and run REVSTAMP to sync the
  headers. The fix was already sitting one file away.
- `REVSTAMP` is a build tool that translates the C header into the BASIC
  include `GPL.BP/REVSTAMP.H`. That include is **tracked in the repository and
  already in sync** — both say 1.0-2 — and the C header's own comment says the
  BASIC copy is normally edited by hand.

No consumer was found for `gplobj` in the data tree at all.
`gplbld/FILES_DICTS` is an install-time input, which the installer should read
from the source tree rather than from the database.

### Also settled this session

`C:\ProgramData\SD\` holds three siblings — `sdsys`, `user_accounts`,
`group_accounts` — not SDSYS with the accounts nested inside it. One root is
what makes §5.7 a single `icacls` rather than a grant per location.

And `<sysdir>/bin` turned out to be two unrelated things sharing a directory:
the executables, and the SD file `BCOMP` opens as `@sdsys:@ds:'bin'` for the
pcode composite library. The move must split them, not relocate the directory.

### State of the machine

SD is running from `/usr/local/sdsys` with the current binaries. Passwords:
SDSYS `hunter2`, SUE `correcthorse`, PAT `batterystaple`; JANE and KIM have
none. PAT lives under `C:\ProgramData\SD\user_accounts`, the other three are
still under `/home/sd/user_accounts`. The scratch programs in `<sysdir>/BP`
are listed in §3 — note `SUE/BP/ESCALATE`, the privilege-escalation proof,
which is now harmless but should go with the rest.

---

## 13 Aug 2026 — Administrator rights become the SDSYS account's, and an escalation is closed

§7 item 2, and it grew a third part when the fix turned out not to be one.

### The two ends it started as

`K_ADMINISTRATOR` in `op_kernel.c` was open at both ends. Any positive
argument set the flag, so a BASIC program could grant itself administrator
rights; and `|| IsAdmin()` meant an argument of zero *re-granted* rather than
cleared whenever the caller was in the OS group, so the flag could not be
given up. Nothing cleared it on leaving SDSYS either, so rights followed a
session into whatever account it moved to next.

Fixed by gating the set on `process.program.flags & HDR_INTERNAL` — the
established "this program was compiled `$internal`" test, already used in
`op_jumps.c` and `op_lock.c` — and by having `LOGIN` and `CPROC` set the flag
on entry to SDSYS and clear it on entry to anything else. `sd -ASUE` on a
machine whose token holds `sdadmins` now reports 0 where it reported 1.

### Why that was not enough, demonstrated

The `HDR_INTERNAL` gate only asks whether the *program* is internal, and
anyone could make one: `sd -internal` was not gated, and `BCOMP` accepted the
`$internal` directive on the strength of internal mode alone. The account SUE
compiled this in her own `BP` and ran it:

```
$internal
      program escalate
      crt 'before: ' : kernel(26, -1)
      void kernel(26, 1)
      crt 'after:  ' : kernel(26, -1)
      end
```

`before: 0`, `after: 1`. Key 26 is `K$ADMINISTRATOR`, written as a literal
because an ordinary account cannot reach SDSYS's `INT$KEYS.H` — no obstacle
whatever. **This was run before the fix, not reasoned about**, which is the
only reason the fix is known to be a fix: the same program now fails to
compile, and SUE stays at 0.

`BCOMP` now requires `kernel(K$ADMINISTRATOR, -1)` as well as internal mode
before accepting `$internal`. Building a system program is an administrative
act, so it needs SDSYS.

### And the rule that ties it together

Decision from the repository owner, arriving mid-fix: **`-internal` may only
enter SDSYS, and must know its password.** Implemented in `sd.c` — any other
account with `-INTERNAL` is refused rather than quietly redirected — and by
deleting the internal-mode bypass from `LOGIN`'s `authenticate.account`, which
was the last route into administration that did not involve the SDSYS
password. `LOGIN`'s "administrator with no account named lands in SDSYS" case
went with it, so plain `sd` now asks which account.

**The install is unaffected, and the reason is worth recording**: `sd -i` runs
`$BBPROC`, which never calls `$LOGIN` — it only compiles it. Checked before
the bypass was removed, because removing it blind would have broken the
bootstrap. And on a fresh install SDSYS has no credential yet, so the
"no password set" branch admits an administrator with a warning.

### Verified

`sd -internal -ASUE` refused; `sd -internal` prompts and admits on `hunter2`,
refuses three wrong ones; plain `sd` prompts for the account; SUE reports 0,
SDSYS 1, and SUE stepping up to SDSYS and out again goes 0 → 1 → 0;
escalation fails to compile; `BASIC GPL.BP CPROC` still builds a system
program, which is the regression that matters since `BCOMP` itself changed;
`COUNT VOC` still reports 432; the whole `LOGTO` suite still passes.

### Left standing, deliberately

`kernel.c` still seeds the flag from `IsAdmin()` at process start. It now
decides one thing only — whether a credential-less account can be entered
during a fresh install — and confers no standing privilege, since `LOGIN`
clears it a moment later for any account that is not SDSYS. Removing it
entirely would take the fresh-install path with it.

---

## 13 Aug 2026 — Accounts move to ProgramData, and SD learns to read a Windows path

Decision from the repository owner: SD accounts live under
`C:\ProgramData\SD\user_accounts` and `C:\ProgramData\SD\group_accounts`.
Settles the question opened earlier the same day. `/home/sd` was the right
place while an SD account was an operating system user; under §5.6 it is not
one, so nothing about the Linux location carried over.

### What that turned out to require

Writing the location into `sd.conf` did not work, and the reason was not the
location. Creating the account succeeded and then `openpath` on it failed with
ER_FNF, "file not found", against a path that plainly existed. Measured with a
probe over five spellings:

| Spelling | Before | After |
|---|---|---|
| `C:\ProgramData\SD\user_accounts\PAT\VOC` | FAIL 3003 | OK |
| `C:/ProgramData/SD/user_accounts/PAT/VOC` | FAIL 3003 | OK |
| `/c/ProgramData/SD/user_accounts/PAT/VOC` | OK | OK |
| `c:\ProgramData\...` (lower-case drive) | FAIL 3003 | OK |
| `C:\ProgramData/SD/...` (mixed) | FAIL 3003 | OK |

**The MSYS2 runtime was never the problem.** A five-line C probe confirmed
`stat()` accepts every one of those spellings. The fault was `sdrealpath()` in
`linuxlb.c`, SD's own hand-rolled `realpath()`, which every `openpath` reaches
through `fullpath()`. Its opening `switch` treats anything not starting with
`/` as a *relative* path and prepends the working directory, and its scanner
only ever splits on `/`. So `C:\ProgramData\SD` resolved to
`/usr/local/sdsys/C:\ProgramData\SD`.

It now folds backslashes to `/` and treats a leading drive letter as the root,
with `root_len` replacing the three hardcoded `outpath + 1` root tests. `DS`
stays `/`: this changed what SD accepts, not what it emits.

**Why it was hard to see, and this is the part worth keeping.**
`open_file()` calls `fullpath()` without checking the result, and `fullpath()`
copies its scratch buffer out whether `sdrealpath()` succeeded or not. An
unresolvable path therefore does not fail at the resolver — it produces an
arbitrary string, and the `stat()` a few lines later reports "file not found"
about something nobody passed in. The swallowed return value is still there;
it is in §6 now.

### Corrections to §5.8

That section claimed MSYS2 "accepts `C:/ProgramData/SD/sdsys` with forward
slashes throughout, so stage 1 can move to the correct location while keeping
`/` as the separator". Half right in a way that misleads: the runtime does,
SD did not, and the sentence would have sent the next session looking at mount
tables. Corrected in place, with this entry as the record.

The same claim's consequence was also wrong. Moving `SDSYS` and the binaries
was described as decoupled from the `@ds` question; in fact it was blocked by
the resolver, and now genuinely is decoupled. Flipping `dir.separator` to `\`
has also become testable for the first time, since a backslash no longer
breaks path resolution.

### Verified

`sd -APAT` run from `C:\Windows`, with `USRDIR=C:\ProgramData\SD\user_accounts`
in `sd.conf`, prompted for the password and landed in the account directory.
`COUNT VOC` still reports 432 and the whole LOGTO suite still passes against
the rebuilt binary — stated explicitly because `sdrealpath()` sits on the path
of every file open in the system.

Two cosmetic leftovers, both tied to `@ds` being `/`: the stored path reads
`C:\ProgramData\SD\user_accounts/PAT`, because `CREATEA` joins with `@ds`; and
`@PATH` reports `/c/ProgramData/SD/user_accounts/PAT`, because it comes from
`getcwd()`, which is always POSIX under MSYS2.

### Also recorded, not built

Two goals from the repository owner, now §5.12 and §5.13. **Everything that can
be lower case should be** — account names, file and field names, and the case
inversion at login — with the warning that the comparisons have to become case
insensitive first, or `sue` and `SUE` become different accounts. And
**disabling `SH` and `!` on Linux was a mistake**: programs need Windows
utilities, and shell-out grants nothing the user does not already have at a
command prompt.

### The changelog gap

`sdb_ai/sd64/sdsys/changelog` is the product changelog, ships with the system,
and **the port had added nothing to it** — 841 lines ending at upstream's
Version 1.0-2, while PROJECT_STATUS.md and HISTORY.md carried everything. That
is the wrong division: those two are the state of the work and the reasoning,
and neither is what a user reads. A "Windows port - unreleased" section now
heads the file, covering the identity model, the account move, Windows paths,
the POSIX IPC switch and the no-binaries rule. Maintaining it is now rule 8 in
§0 and a line in CLAUDE.md.

---

## 13 Aug 2026 — SD outside the MSYS2 shell: it works, and one PATH trap is nasty

No code changed. Prompted by the question of whether logging in will one day be
"global and not require MSYS2". Half of that is already true and had never been
tested, so it was.

**The shell dependency is already gone.** `sd.exe` run from a plain PowerShell
prompt answered `COUNT VOC` with 432 records. POSIX paths still resolve —
`/usr/local/sdsys`, `/etc/sd.conf` — because the translation lives in
`msys-2.0.dll`, not in bash. What remains is the *runtime* dependency, which is
stage 2 and unchanged.

It needs two directories on PATH, not one: `C:\msys64\usr\bin` for the runtime
and `C:\msys64\usr\local\bin` for `libsodium-26.dll`, which sits there because
libsodium is built from source into `/usr/local`. Miss either and the loader
fails before `main` with exit code 53 and **no message at all**.

**The trap worth the entry.** Put `C:\Program Files\Git\usr\bin` ahead of
MSYS2 on PATH — Git for Windows ships its own MSYS2 runtime, and it is on
nearly every developer machine — and `sd.exe` starts, runs, and reports
**"SD has not been started"** while the server is running perfectly. The
runtime derives its POSIX root from the location of the DLL that loaded it, so
`/dev/shm` resolves inside Git's installation, where no shared segment exists.
The message names the wrong problem completely.

Both are arguments for shipping the DLLs beside `sd.exe` under
`C:\Program Files\SD\` (§5.8), since Windows searches the executable's own
directory before PATH. §5.8 now says so.

**Where it is still not shell-agnostic: reading a password.** Scripted stdin
from either Windows shell corrupts the first line, which is the password.
PowerShell 5.1 puts a UTF-8 BOM on the stream, so `abc` arrives as six
characters and `abcdef` as nine — measured by counting the asterisks SD echoes,
and `$OutputEncoding` does not suppress it. `cmd.exe` adds a character per line
and an extra empty line that eats one of the three tries. A pipe from bash is
correct, with LF or CRLF. These are artefacts of the sending shell rather than
SD faults, but they surface as "Invalid username or password", which sends you
looking in the wrong place. Also confirmed from `cmd.exe`: a `<` redirect from
a regular file cannot be read at all, so that earlier finding is SD's input
layer and not something about bash.

**What was not tested, and cannot be from here.** Nobody has typed at SD from a
real Windows console. Every test above used redirected stdin, so how the MSYS2
tty layer behaves in `conhost` or Windows Terminal — echo, masked input, arrow
keys, terminfo — is unknown, and the scripted corruption above says nothing
about it. That is now in §4 as the unverified item that "does SD need MSYS2"
actually turns on, and it needs a person at a keyboard.

---

## 13 Aug 2026 — What logging in actually looks like, seen as an ordinary user

No code changed. This entry records what was observed when the question "how
does one log into SD from the command line" was asked, because most of it had
never been seen from outside the administrator's seat.

Every session on this machine is an SD administrator: the token carries
`sdadmins` and `kernel.c` seeds `USR_ADMIN` from `IsAdmin()`. So the ordinary
user's experience was invisible here. A **non-administrator probe** — the §6
recipe with `SD_ADMIN_GROUP` naming a group nobody holds, the inverse of the
probe built when the group work landed — made it visible. The recipe is now in
§6 next to the original.

| Entered as | What happens |
|---|---|
| `sd` or `sd -A`, administrator | straight into SDSYS, prompts for the SDSYS password |
| `sd`, ordinary user | prompts `Account:` then `Password:` |
| `sd -ASUE` | prompts for SUE's password |
| `sd -ASUE WHO` | same, runs the one command, exits |
| `sd -internal` | SDSYS with no password; administrators only |

Three things worth knowing came out of it:

**SD no longer needs an operating system group to use.** The probe logged into
SUE with the account's own password and `SYSTEM(1050)` reported 0. Nothing
about the Windows account mattered. That is what §5.6 was for, and it had never
been shown from the outside.

**The SDSYS password alone makes you an SD administrator.** The same probe ran
`sd -ASDSYS`, gave `hunter2`, and arrived with `SYSTEM(1050)` at 1, because
`LOGIN` sets the flag on entry to SDSYS. Administration is now a matter of
knowing that password rather than of Windows group membership.

**Administrator rights follow you out of SDSYS.** `LOGTO KIM` from there left
the flag at 1 while standing in KIM. This was known to be true while
`IsAdmin()` is true, and blamed on the `op_kernel.c` set hole; here `IsAdmin()`
was false and the flag still persisted, because **no code attempts to clear
it**. §7 item 2 now names both ends of the problem rather than one.

Two smaller findings, both in §6. `sd -A` with no account name sets
`CMD_QUERY_ACCOUNT` and nothing anywhere reads that flag, so bare `-A` is
identical to plain `sd` — for an administrator, going straight into SDSYS
instead of asking which account, the opposite of the option's name. And the
`Account:` prompt echoes in lower case, because `LOGIN` turns `PT$INVERT` on
before it; harmless, but it is the visible face of the case-inversion trap that
cost real time on the password read.

---

## 13 Aug 2026 — SDSYS is the exception; LOGTO takes account names only

Decisions from the repository owner, answering both questions the entry below
raised, and the code that carries them out. Made and built the same day.

### SDSYS reaches every account, without exception

The grant check as first built tested `@logname` and nothing else, so an SDSYS
login could not enter an account that had not granted it — recorded as an open
question because §5.6 did not say. The answer is that SDSYS is the exception:
administration that cannot enter an account cannot repair one.

**The test is the account you are standing in, `who`, not the one you logged in
as.** That reading was chosen deliberately and is worth understanding, because
the alternative is defensible and one line away. Keying on `@logname` would
have meant that the model's own recommended route into administration — log in
as yourself, `LOGTO SDSYS` with your own password — did *not* carry the
exception, while a direct SDSYS login did. The account would be an exception
only for people who knew the shared SDSYS password, which is the arrangement
§5.6 exists to get away from. Keying on `who` gives the exception to whoever is
standing in SDSYS however they got there, and `@logname` still names them.

Observed both ways: logged in as SDSYS, `LOGTO JANE` and `LOGTO KIM` were
admitted although neither grants SDSYS; logged in as SUE, `LOGTO KIM` was
refused, `LOGTO SDSYS` with SUE's own password was admitted, and `LOGTO KIM`
from there was admitted as `LOGNAME=SUE WHO=KIM`.

The one edge to know: stepping *out* of SDSYS puts you in an ordinary account
and you no longer carry the exception. SDSYS → KIM → JANE is refused at the
second move. Returning to SDSYS is never blocked, since it is your own account
by name if you logged in as it, and a grant plus your own password if not.

### LOGTO takes an account name and nothing else

`int.logto` treated anything absent from ACCOUNTS as a pathname to change
directory to. That was the hole the entry below recorded: it reached an
account's directory without ever consulting the grant list, and it was open to
anyone the OS group made an administrator, which on a machine with `sdadmins`
is every session. Rather than resolve paths back to accounts — which needs the
resolved directory, so it means moving before authorising and unwinding on
refusal — the capability is gone. An unregistered directory is not an account.

An unknown name now gives the same refusal as an ungranted one, so the register
cannot be probed for which account names exist. The cost is that a typo reads
as "User not allowed in requested account"; `LOGIN` already makes the same
trade with "Invalid username or password".

`APISRVR`'s `SrvrAccount` took "account name or path" in the same way and now
takes a name only. **Nothing else there was gated and nothing was added**: the
API server has no credential model, its `logname` arrives from the client, and
putting a grant check on top of that would look like a control without being
one. It is now §7 item 4, with the authentication named as the part that has to
come first.

Found while making that change: `revert.to.old.account` put the *directory*
back after a refused account switch but not `account.path`, so `@PATH` was left
holding the path the session had failed to reach. Pre-existing, and made more
visible by the new refusal, which reaches revert with `account.path` empty. It
now restores both.

### What this changed in the record

PROJECT_STATUS §4 had recorded, under Verified, "An SDSYS login cannot `LOGTO`
an account that has not granted it". That observation was correct when made and
is now false by decision, not by error — the behaviour changed the same day.
The bullet has been replaced by what was observed after the change. §8's two
open questions are marked settled rather than deleted.

---

## 13 Aug 2026 — LOGTO is gated by grants, and the shipped binary is verified

Continues the entry below, "Account credentials: register, helpers and login",
which stopped with `LOGTO` untouched. Covers the commit carrying this entry.

### What was built

The second half of §5.6. Entry to an account is now authorised, not assumed.

| Piece | Where |
|---|---|
| `ACC$USERS`, field 4 of ACCOUNTS, the grant list | `sdsys/SYSCOM/KEYS.H` |
| Its dictionary item, and `USERS` added to the default listing | `gplbld/FILES_DICTS/ACCOUNTS.DIC^USERS`, `…^@` |
| `logto.authorised`, the grant check | `sdsys/GPL.BP/CPROC` |
| `logto.step.up`, re-authentication for SDSYS | `sdsys/GPL.BP/CPROC` |
| Messages 10030 and 10031 | `sdsys/MESSAGES` |

The early "is the caller privileged" test at the top of `int.logto` is gone.
It had been `system(27) = 0` and then `K$ADMINISTRATOR`, and both ask the wrong
question: entering SDSYS is what confers administrator rights, so requiring
them to get in is backwards. Authorisation now happens in one place, below the
ACCOUNTS read, where the target account is known — the spot the deleted
`ACC$GROUP` test used to occupy, and it fails the same way that test did.

The step-up asks for **the caller's own** password, not an SDSYS one. This is
the easy thing to get backwards and the whole point of the model: re-entering
your own credential proves the person at the keyboard is still the one who
logged in, and introduces no shared secret. An SDSYS password would be a second
secret held by every administrator, unrotatable without telling all of them.

`KEYS.H` already carried the history line "20240330 mab add ACC$USERS" for a
define that was not in the file. The 0.6.4 changelog describes the same design
— "A list of allowed users is found in ACCOUNTS record, field <ACC$USERS>" — so
field 4 restores what upstream intended rather than inventing a layout.

### What was observed

Two scratch accounts, JANE and SUE, driven from a real login as SUE. The grant
check refused `LOGTO JANE` before the grant and admitted it after; refused
`LOGTO SDSYS` before the grant; and after granting, refused three wrong
passwords and admitted the right one. `LOGTO SUE` into her own account needs no
grant, as it must. A refused `LOGTO` leaves the session where it was and does
not drop the connection.

`@logname` survives all of it — `LOGNAME=SUE WHO=JANE`, and `LOGNAME=SUE
WHO=SDSYS` after stepping up. Administration is reached from a personal
identity, which is what makes the audit log (now §7 item 1) worth writing.

`sd -internal` still enters SDSYS with no password and moves with no grant, so
the bootstrap is untouched. Full table in PROJECT_STATUS §4.

**The shipped `bin/sd.exe` was exercised for the first time.** The token now
carries `sdadmins` — the re-logon that group membership needs had happened
between sessions — so `-stop`, `-start`, `-internal` and a password login all
ran against the real binary rather than the probe build. That closes two
entries that had stood in §4 as unverified since the group work landed.

### Traps found, all of them cheap to hit again

**A confirmation prompt reached by a script spins for ever at full CPU.**
`CATALOG BP WHOAMI GLOBAL` asks "Program is also in private catalogue.
Remove?". The piped input had already run out, the read returned end of file,
and the prompt loop asked again — half a megabyte of repeated prompt in about
two minutes. It reads like a hang; it is the opposite of the lock-wait hang
already in §6, which idles. This one matters beyond testing: §5.9's installer
will drive SD from a script.

**A scripted session must be piped, not redirected.** `cat cmds | sd -AACCOUNT`
works; `sd -AACCOUNT < cmds` stops after the password prompt and exits 0. Both
are non-tty stdin. Not investigated further.

**`OSPATH()` is `$internal`-only**, and fails like `KERNEL` does: the compiler
decides it is an array and complains that it is not in a `DIM` statement.

**`$catalog NAME` in the source catalogues privately**, so the program is
invisible from other accounts. `CATALOG BP NAME GLOBAL`, or a `$`/`!`/`*`
prefix, is what makes it global.

### What is still open

The audit log, which is the remaining half of §5.6 and is now the first item in
§7. Two questions for the repository owner went into §8: whether an
administrator should be able to enter an account that has not granted them —
as built, SDSYS cannot — and the bare-pathname branch of `LOGTO`, which reaches
an account directory without a grant check and is open to anyone the OS group
makes an administrator. Neither is a regression; both are consequences of §5.6
as written, and closing the second means restructuring `int.logto` rather than
inserting a test.

`CREATE.ACCOUNT` was not used to build the test accounts, because `CREATEA`
still shells out to `sudo usermod` and `groupadd`. A scratch program made them
instead. The verb has still never run on Windows.

### Stale entry removed from PROJECT_STATUS §4

§4 still listed "Bootstrap pass 1 has never completed — `sd -i` attaches and
then blocks silently" under *Not verified*, while the *Verified* list directly
above it recorded the complete bootstrap running and 204 programs compiling.
Both were written in the same session; the second superseded the first and the
first was never taken out. The claim itself was corrected on 13 Aug 2026 in
"Correction: `sd -i` was not deadlocked, and not on a semaphore" — the cause
was a stale record lock left by a killed run. The bullet is now removed.

---

## 13 Aug 2026 — Account credentials: register, helpers and login. Session ended on credits

**Session ended mid-task, with LOGTO still to do.** Resume at PROJECT_STATUS
§5.6, which lists the exact insertion points, and read the machine state at the
end of §3 before touching anything.

### What was built

The first half of the identity model in §5.6. Accounts now have their own
passwords, stored as an Argon2 verifier.

| Piece | Where |
|---|---|
| `$CRED` register keyed by account | `<sysdir>/$CRED`, fields in `INT$KEYS.H` |
| `!CRED_SET`, `!CRED_VERIFY` | `GPL.BP/CRED_SET`, `GPL.BP/CRED_VERIFY` |
| `SET.PASSWORD [account]` | `GPL.BP/SET_ACC_PASSWORD` |
| Login password prompt | `LOGIN`, `authenticate.account` |

`$CRED` is a separate file from `ACCOUNTS` on purpose: `LOGIN` opens `ACCOUNTS`
before authenticating anything and eleven other programs open it too, so a
verifier stored there would be readable by every user.

The libsodium primitives were verified before anything was built on them —
neither `!SD_GET_SALT` nor `!SD_KEY_FROM_PW` had ever had a caller. Both work
on Windows.

`LOGIN`'s three account-determination cases collapsed into one, since entry no
longer varies by how you arrived. Two deliberate ways in without a password,
both gated on `K$ADMINISTRATOR` — which now comes from OS group membership via
`IsAdmin()` and cannot be self-granted: an administrator running an internal
command, because the bootstrap runs through `LOGIN` and cannot type a password;
and an account with no password yet, with a warning. Note `-internal` alone is
unguarded in `sd.c`, so the administrator test is the gate, not internal mode.

### Two traps, one of which would have shipped

**`pterm(PT$INVERT, @true)` silently upcases input.** `LOGIN` turns case
inversion on before prompting, so `hunter2` arrived as `HUNTER2`. The password
verified correctly by hand and failed at login with nothing visibly wrong — the
record was found, the salt and derived key were the right lengths, `STATUS()`
was zero. Every intermediate check passed because the only fault was the case of
the bytes. Found by dumping `seq()` of each character. Inversion is now saved,
cleared around the password read, and restored.

**`$internal` is only accepted under `sd -internal`**, gated by `BCOMP` on
`kernel(K$INTERNAL, -1)`. From an ordinary session the directive is rejected and
then every internal-only statement it enables reports "Unrecognised statement",
so the reported lines are all several lines below the actual cause.

Also `WRITE ... THEN` is not valid BASIC here; it produces an unrecognised
statement plus a spurious complaint about text after the final `end`.

### What is not done

`LOGTO` is untouched, so **any authenticated session can still enter any
account** — the login prompt is the only real control at the moment. Still to
write: the grant check on the target account, the step-up password on
`LOGTO SDSYS` against the person's own credential, and confirming `@logname`
survives the move. The `op_kernel.c` set hole is also still open, which is why
administrator rights cannot currently be cleared once `IsAdmin()` is true.

Everything this session was run against the probe build with `SD_ADMIN_GROUP`
overridden to `Users`. `bin/sd.exe` is current but has never been run.

---

## 13 Aug 2026 — History rewritten to purge every binary. All earlier hashes are stale

**Read this before following any commit hash quoted in an entry below.** The
repository history was rewritten on 13 Aug 2026 with `git filter-repo`, so
every hash recorded in earlier entries refers to the pre-rewrite history and no
longer resolves. Mapping for the commits those entries name:

| Subject | Old | New |
|---|---|---|
| Remove superseded Linux artifacts and untrack generated files | `3b4600e` | `b234541` |
| Replace the client library with the enhanced winsdclilib port | `202b965` | `df4202a` |
| Add PROJECT_STATUS, HISTORY and CLAUDE.md for cross-session handoff | `139cdfd` | `af5c9ab` |
| Record the BASIC layer survey in the handoff documents | `4e525d6` | `edd941f` |
| Survey every BASIC to C linkage; record the privilege model finding | `a70520a` | `2416abd` |
| Base SD administrator rights on group membership, not uid zero | `f56de86` | `5509ce9` |
| Raise the PROJECT_STATUS rollover limit to 800 lines | `3248b72` | `2b85a87` |
| Start runtime bring-up; verify the IPC port; unify the admin check | `9c00730` | `016756c` |
| Decide the identity model, install layout, data protection and audit | `59c1de7` | `4b6353b` |
| Require the password again on LOGTO SDSYS | `c1fd5b9` | `d40c068` |
| Raise the PROJECT_STATUS rollover limit to 2000 lines | `a054dbb` | `9d2338b` |
| Start SD for the first time; correct the bootstrap sequence | `fcfce5f` | `4fed1f7` |
| Rule out a semaphore deadlock; find the real bootstrap blocker | `ff0d239` | `a43de38` |
| Base the BASIC privilege tests on K$ADMINISTRATOR | `5c09f0f` | `13c2fcd` |
| Remove the OS group tests; SD now runs | `91c63d8` | `a35d20f` |

Subjects did not change, so matching by subject is reliable where this table is
not enough. Commit count is unchanged at 17.

### What was removed

The previous entry untracked the binaries going forward but left them in
history, where a clone still fetched them. This finishes the job.

- **Windows build output**: `sd.exe`, `sdconv.exe`, `sdfix.exe`, `sdidx.exe`,
  `sdlnxd.exe`, `sdtic.exe`, `sdclilib.dll`, `libsdclilib.dll.a`, and the whole
  `gplobj/*.o` set — about 90 object files.
- **Linux build output that a extension-based sweep missed entirely**:
  `bin/sd`, `bin/sdconv`, `bin/sdfix`, `bin/sdidx`, `bin/sdlnxd`, `bin/sdtic`.
  These are ELF binaries with **no file extension**, left from before the port,
  along with `libsdcli.so`, `sdclilib.so` and `libsdcli.dll.a`. Finding them
  needed a scan of every blob in history for NUL bytes rather than a glob —
  worth remembering the next time something claims to be binary-free.
- **62 compiled `terminfo/` files**, generated by `sdtic` from `terminfo.src`
  and already ignored going forward.
- **Compiled I-type object code inside two install dictionary items**,
  `DICT.DIC^TYPE.CODE` and `DICT.DIC^FORMAT.CODE` in `gplbld/FILES_DICTS`. The
  repository owner pointed out that the install recompiles every I-type, so the
  object code is not needed. Verified rather than assumed: after stripping,
  `THIRD.COMPILE` prints "Compiling TYPE.CODE", which it had not before because
  the compiled form was already present, and `LIST DICT VOC` then resolves the
  I-types normally (`IS.REMOTE I 1L`, `TYPE I 2L`). Field 15 is the source
  checksum and was kept; only the trailing object code fields were blanked,
  which is the shape `DICT.DIC^SMV` already had. This was applied across all
  history by a blob callback, so the object code never existed here — which is
  why there is no separate commit for it, the one that made the change became
  empty and was pruned.

Result: **zero blobs containing NUL bytes anywhere in history**, verified by
walking every object. `.git` fell from about 5.7 MB to 2.3 MB. The four largest
remaining blobs are all legitimate text source — `BCOMP`, `bbcmp.py`, `SED` and
`QPROC`.

`bin/README` was deliberately kept, so the directory is still documented.

### Method, and the safety net

`git filter-repo` was downloaded for this (with permission) since MSYS2 has no
pip and `filter-branch` is deprecated. It needs Git for Windows on `PATH` when
run from the MSYS2 shell, which is not the default. It also removes the
`origin` remote as a safety measure, so that had to be re-added before pushing.

**A full bundle of the pre-rewrite repository was taken first** and is at
`pre-rewrite-backup.bundle` in this session's scratchpad. That is outside the
repository and will not survive the machine; if the old history matters, copy
it somewhere durable now. Recovery is `git clone pre-rewrite-backup.bundle`.

---

## 13 Aug 2026 — SD runs. Full bootstrap completes; no binaries in the repository

Two changes, one of them a reversal of policy set earlier the same day.

### The OS group membership tests are gone

`is_grp_member` calls removed from `LOGIN` (the `sdusers` login gate and the
`ACC$GROUP` account gate), `CPROC` (`LOGTO`) and `APISRVR` (three sites), along
with the `deffun` declarations, which had no callers left. This is §5.6: SD
consults no operating system group.

**It also means nothing currently restricts entry to any account.** That is the
intended interim state — account credentials replace the groups — but the
system is open until that is built, and should not be exposed to anything
meanwhile. §7 step 1 is now the credential model, and it is urgent rather than
merely next.

The calls in `CREATEA` and `MODIFYA` were left deliberately. They guard
`OS.EXECUTE` calls to `useradd`, `usermod` and `groupadd`; removing the guard
alone would let those shell-outs run unconditionally, which is worse than
leaving them in place. They go when the OS account commands go, as one change.

### The bootstrap now runs to completion, and SD answers commands

| Step | Result |
|---|---|
| `sd -i` | 9 programs compiled, `VOC` and dictionaries created |
| `SECOND.COMPILE` | **204 programs compiled with no errors** |
| `WRITE_INSTALL_DICTS` | dictionary entries written, "COMPLETE" |
| `THIRD.COMPILE` | I-types compiled |
| `BASIC GPL.BP CPROC` | real 24 KB `gcat/$CPROC`, replacing the placeholder |

```
sd -ASDSYS WHO          -> 7 SDSYS
sd -ASDSYS COUNT VOC    -> 431 record(s) counted
sd -ASDSYS SELECT VOC   -> 431 record(s) selected to list 0
```

Reading records back works. `@ds` hardcoded to `/` compiled 204 programs, which
settles that question for stage 1.

Three things were learned getting there, all recorded as traps.

**Grep the BASIC case-insensitively.** There were five `system(27)` privilege
tests, not four: `WRITE_INSTALL_DICTS` spells it `SYSTEM(27)`. A case-sensitive
sweep found four, and the survivor stopped the bootstrap two steps later. This
directly caused a wasted cycle.

**`KERNEL` is only available to `$internal` programs.** `WRITE_INSTALL_DICTS`
is not one, and `KERNEL(K$ADMINISTRATOR, -1)` there produced "WARNING: KERNEL is
not assigned a value" — the compiler treating it as a variable, not an unknown
function. `SYSTEM(1050)` returns the same `USR_ADMIN` flag (`op_sys.c` case
1050) with no such restriction, and is the right call for non-internal code.

**The runtime tree needs `gplsrc`, `gplobj` and `gplbld/FILES_DICTS`.**
`installsdai.sh` copies all three into `<sysdir>`, and the list recorded in §3
had omitted them. `REVSTAMP` opens `./gplsrc/revstamp.h` relative to the account
directory, so `SECOND.COMPILE` aborted at APISRVR with "Cannot open gplsrc
revstamp.h", which reads like a compiler fault and is a missing directory.

The stale-lock trap recorded in the entry below proved itself twice more: an
aborted `SECOND.COMPILE` left a lock on the sequential file `REVSTAMP` writes,
and the retry sat at 0.47 s of CPU over 78 s until SD was restarted. The
documented fix — stop and start — worked both times.

Still outstanding: every catalogue write prints "Unable change ownership of
directory error ... err: 1000", which is `CATALOG` doing the Linux `chown` to
`sdsys:sdusers`. Non-fatal, and it belongs with the rest of the OS account work.
Also `LOGIN` carried a mangled banner, `END-HISTORYPTION:`, where the AI cleaning
cycles had merged `END-HISTORY` and `START-DESCRIPTION:`; repaired in passing.

### No binaries in the repository

Decision from the repository owner, **reversing** the position recorded earlier
the same day that linked binaries in `bin/` were tracked so the install scripts
could deploy them from a clone. Everything must be auditable from source — the
same reason the pcode build is Python rather than a shipped binary.

Eight files untracked: `sd.exe`, `sdconv.exe`, `sdfix.exe`, `sdidx.exe`,
`sdlnxd.exe`, `sdtic.exe`, `sdclilib.dll`, `libsdclilib.dll.a`. They are still
built by `make sd` and still needed at runtime; they were untracked, not
deleted. `.gitignore` now excludes `bin/` and every `.exe`, `.dll`, `.a`, `.o`,
`.so`, `.lib` and `.obj` anywhere in the tree, and CLAUDE.md carries the
constraint so it is read before anything is added back.

The consequence for §5.9 is that installing means building: `installsdai.sh`
does `cp -R bin "$sdsysdir"` and tests for `bin/sd`, both of which assumed a
clone already held the binaries.

**The binaries remain in git history**, so a clone still fetches them and the
audit goal is only half met. Purging needs a history rewrite and a force push,
which is destructive to existing clones and breaks the commit hashes this
archive quotes. Not done without asking; recorded as an open question in §8.

---

## 13 Aug 2026 — Privilege tests moved to K$ADMINISTRATOR; bootstrap pass 1 completes

**SD compiled BASIC and created database files on Windows for the first time.**

### The change

Three privilege tests in the BASIC layer asked `SYSTEM(27)`, which is
`getuid()`. There is no uid zero on Windows, so each answered the same way
permanently (§5.5). They now ask `KERNEL(K$ADMINISTRATOR, -1)`:

| File | Was | Effect on Windows |
|---|---|---|
| `BBPROC` (~line 129) | `system(27) # 0` | bootstrap always refused |
| `CATALOG` (~line 105) | `system(27) # 0` | `CATALOG GLOBAL` always refused |
| `CPROC` `int.logto` (~line 2461) | `system(27) > 0` | `LOGTO SDSYS` always refused |

`LOGIN:217` already used `K$ADMINISTRATOR` and needed no change.

**The tests alone would have achieved nothing**, because nothing set the flag.
`CPROC` was the only thing that ever called `kernel(K$ADMINISTRATOR, 1)`, and
only inside its `system(27) = 0` branch, which never runs here — so
`K$ADMINISTRATOR` answered "no" for everybody and swapping one always-false
test for another would have changed the message and not the outcome. So
`kernel.c` now seeds `USR_ADMIN` from `IsAdmin()` where the user table entry is
initialised, next to the existing `USR_PHANTOM` and `USR_SDAPISRVR` flags.

That keeps the OS group as the source of administrator status for now, which is
the interim position: when the credential model in §5.6 lands, entry to SDSYS
becomes what sets the flag. It also means the seeding is the single place to
change, rather than scattered tests.

`CPROC`'s `system(27) = 0` "entered as root?" branch at line 272 was left as
found. It guards `EUID_SET`, which has no Windows equivalent, and its
`kernel(K$ADMINISTRATOR, 1)` is now redundant.

### Result

`sd -i` exits 0. It compiled `CPROC`, `LOGIN`, `BASIC`, `BCOMP`, `PTERM`,
`CATALOG`, `PARSER`, `IS_GRP_MEMBER` and `TERM` with zero errors each, and
created `VOC`, `ACCOUNTS.DIC`, `$HOLD.DIC`, `$MAP`, `$MAP.DIC`, `$IPC`,
`DICT.DIC`, `DIR_DICT` and `VOC.DIC`. `GPL.BP.OUT` went from 4 objects to 11.

So the compiler chain works — `BCOMP`, `@ds` path resolution, the pcode loader
— and so does DH file creation. Both were unverified. The `@ds` question raised
in §6 is answered for stage 1: hardcoded `/` is correct on the MSYS2 runtime.

### Where it stops now

`SECOND.COMPILE` fails with "This user is not registered for String Database
(sd) use" — `LOGIN:193`, `is_grp_member(lgn.id,'sdusers')`, failing because
`IS_GRP_MEMBER` parses `/etc/group` and MSYS2 has no such file. Predicted in
the entry below and hit exactly where predicted. Pass 1 escaped it only because
`-i` runs `$BBPROC` instead of `LOGIN`. Under §5.6 the calls get deleted.

### Method note worth keeping

Testing a BASIC edit needs three steps, not one: edit the repository copy, copy
it to `<sysdir>/GPL.BP/`, then compile it. `$BBPROC` is compiled by
`gplbld/bbcmp.py`. Skipping the copy leaves the running system on the old code
with no indication anything was missed. Recorded as a trap.

All of this still runs against the probe build with `SD_ADMIN_GROUP` overridden
to `Users`, since the token has yet to pick up `sdadmins`.

---

## 13 Aug 2026 — Correction: `sd -i` was not deadlocked, and not on a semaphore

Corrects the entry below, "SD started for the first time; the bootstrap
deadlock was not one", which recorded `sd -i` as blocking silently and named a
semaphore deadlock as the first thing to eliminate. It is neither.

### It is not a semaphore deadlock

Established two independent ways.

A `sem_getvalue()` probe against all six named semaphores read **1 (free) on
every one**, both at idle and while a process was blocked. And `LockSemaphore`
in `sdsem.c` is a spin loop — `while (sem_trywait(...) != 0) RelinquishTimeslice;`
where `RelinquishTimeslice` is `sched_yield()` — so a process stuck there would
burn CPU continuously. The blocked process used 0.36 s over 95 s of wall clock.
Whatever it was waiting on, it was sleeping, not spinning.

### What it actually was: a stale record lock, self-inflicted

`strace` (MSYS2's, which launches rather than attaches) showed the process
stat'ing `/tmp/bbproc.log` and then `clock_nanosleep(0.250000000)`, over and
over. That is the record-lock wait path in `op_dio3.c` around line 1065:
conflicting lock held by another user → `Sleep(250)` → re-execute the opcode →
repeat, with no timeout and no message. `BBPROC:118` opens `/tmp/bbproc.log`
with `openseq ... overwrite`, which is what wanted the lock.

The lock was left behind by earlier `sd -i` runs that this session killed. The
lock table lives in the shared segment, so a process killed with SIGTERM or
SIGKILL never releases what it held, and every later run waits on it forever.
`sd -stop` followed by `sd -start` clears it, because the segment is unlinked
and recreated empty. Recorded as a trap in §6 — the symptom (no output, no
return, no CPU) reads exactly like a deadlock and is not one.

### What is really blocking bootstrap pass 1

On a clean lock table `sd -i` does not hang at all. It returns immediately with

```
Command requires administrator privileges
```

and aborts. That message is **not** `check_admin()` in `sd.c` — it is
`BBPROC:133`, `if system(27) # 0`, which is always true on Windows because
`SYSTEM(27)` is `getuid()` and there is no uid zero. It is the §5.5 trap hit
for real, and it is the same message from a different place, which is what made
it confusing earlier in the session.

**So runtime bring-up and the identity work have converged.** Pass 1 cannot
proceed until the privilege tests move to `KERNEL(K$ADMINISTRATOR, -1)` per
§5.6. The probe build's `SD_ADMIN_GROUP` override cannot help, because BBPROC
tests `SYSTEM(27)` directly and never consults `K$ADMINISTRATOR`. §7 has been
reordered accordingly.

### Also confirmed while investigating

`sd -stop` works, including the new liveness poll that replaced the System V
attach count. It reported a clean shutdown and left `/dev/shm` completely
empty — segment and all six semaphores unlinked — after which `sd -start`
brought the system up again. The full start/stop/restart cycle runs. That
closes an item listed as unverified.

Also: `sd -start` does not hang when its output goes to a file rather than a
pipe, confirming the diagnosis in the entry below that the apparent hang is
`sdlnxd` inheriting stdout and stderr.

---

## 13 Aug 2026 — SD started for the first time; the bootstrap deadlock was not one

Covers the documentation commit after `a054dbb`. No code changed. **SD created
its shared segment and ran, which it had never done before.**

### Correction: the recorded bootstrap sequence was wrong

PROJECT_STATUS §3 described a deadlock — `sd -i` reporting "SD has not been
started" while `sd -start` could not run because `config.c` demands
`<sysdir>/gcat/$CPROC`, which only the last bootstrap step creates. It suggested
reading the `is_bootstrap` flag in `sd.c` to resolve the ordering.

There is no deadlock. The sequence as recorded omitted two steps that
`installsdai.sh` performs. The installer creates an **empty placeholder** at
line 468:

```sh
# Fool sd's vm into thinking gcat is populated
sudo touch /usr/local/sdsys/gcat/\$CPROC
```

then runs `sd -start` at line 590, *before* `sd -i` at line 604. `read_config()`
only calls `access(path, 0)`, so an empty file satisfies it; the real catalogue
overwrites the placeholder at the end. Confirmed by creating the placeholder by
hand, after which `-start` proceeded.

Two things worth recording about the investigation. The `$CPROC` check exists in
the original Ladybridge source as well — `gplsrc/config.c` in the external
reference tree — so it is not something the AI cleaning cycles introduced, which
was the first suspicion. And `is_bootstrap` is a red herring: it is set at
`sd.c:321` and never consulted by `bind_sysseg`.

### SD started

With the placeholder in place and a probe binary built per §6 (both `sd.c` and
`linuxlb.c` recompiled with `-DSD_ADMIN_GROUP='"Users"'`, since the token still
lacks `sdadmins`), `sd -start` created `/dev/shm/sd_shm_716d0301` at 100 KB and
six semaphores `sd_sem_716d0302_0` through `_5`, and spawned `sdlnxd`, which
stayed up. That is the `shm_open`/`ftruncate`/`mmap` creation path in
`sysseg.c` executing for the first time. The standalone lifecycle test recorded
earlier had exercised the same calls, but never from within SD.

Multi-process attach followed for free: `sd -i` attached to the existing
segment, was allocated a user table slot, and wrote to `<sysdir>/errlog` —
"User 2 (pid 1931, don)". Both were listed as unverified.

### Where it stops now

`sd -i` blocks silently. No output at all, and it never returns. It is blocked
rather than looping — 0.36 s of CPU over 95 s of wall clock — and behaves
identically whether given `/dev/null` or a real pty via `script`. The suspicion
worth eliminating first is a semaphore deadlock, because that would mean a
defect in the `sdsem.c` port rather than another missing install step. Reading
`$BBPROC` is the other thread to pull, since `-i` installs it as the command
processor and it is the only thing running at that point.

### Two traps found the hard way

`sd -start` appears to hang. It has not: it spawns `sdlnxd`, which inherits
stdout and stderr, so any shell capturing output blocks until the *daemon*
exits rather than until `sd -start` does. The parent returned long before.

`sd -SUSPEND` is sticky and survives the process, because the flag lives in the
shared segment. Every later invocation dies with "SD is suspended" and no hint
of why. This was self-inflicted here — a diagnostic loop ran `-SUSPEND` and the
next twenty minutes of "SD is suspended" looked like a new failure. `sd -RESUME`
clears it. Neither verb calls `check_admin()`, so any user can suspend a running
system; worth revisiting under §5.6.

---

## 13 Aug 2026 — PROJECT_STATUS rollover limit raised to 2000 lines

Supersedes the entry below, "PROJECT_STATUS rollover limit raised to 800 lines",
on the figure only. Its reasoning still holds; the number was still too small.

800 was set earlier the same day, after 400 proved too tight, and was binding
again within hours — the identity, install layout, data protection and audit
decisions took the file to 826. Raising it twice in one day is the signal: the
figure was being chosen to feel tidy rather than to serve a purpose.

**The purpose, stated by the repository owner: stop the file growing to several
thousand lines, as happened on another project, where it stops being something
anyone reads.** It is not there to keep the document at a convenient size, and
approaching it is not a problem. 2000 leaves real headroom — roughly two and a
half times the current content, and far enough below the failure case that this
should not need revisiting.

The wording in both PROJECT_STATUS §0 and CLAUDE.md now carries that intent, so
a later session does not read the number as a budget and start compressing live
material to stay under it. Added a note on *when* to prune: just after work
lands, when instructions that have been carried out turn into history and shed
easily — not when a line count is approached.

---

## 13 Aug 2026 — Step-up authentication on LOGTO SDSYS

Follows the entry below, which this refines rather than corrects. Covers the
documentation commit after `59c1de7`. No code changed.

That entry recorded `LOGTO` as needing no password, access being by grant. The
repository owner added one exception: **`LOGTO SDSYS` prompts for the password
again.** Entering administration should be a deliberate act, not something an
unguarded session drifts into.

**The password asked for is the person's own, not an SDSYS password**, and the
distinction is the whole value of the change. Re-entering your own credential
is re-authentication — it confirms the person at the keyboard is still the one
who logged in, keeps attribution intact, and creates no new secret. An SDSYS
password would be a second shared secret held by every administrator, which is
exactly the OpenQM weakness this model was built to remove: the audit log would
still name a person, but the credential guarding the most privileged account in
the system would be shared, and unrotatable without telling everybody.

The step-up is logged separately from the `LOGTO`, on success and on failure. A
failed step-up is the most interesting single line the audit trail can carry.

---

## 13 Aug 2026 — Identity, install layout and data protection decided

Covers the documentation commit that follows `9c00730`. No code changed. Four
decisions from the repository owner, and the investigation that informed them.

### The decisions

1. **Every SD account carries its own password; OS groups are dropped from SD
   entirely.** SD has no users, only accounts — user accounts for one person,
   group accounts reachable by many. **SDSYS is the only administrator**,
   entered by password prompt from `sd -ASDSYS` or `LOGTO SDSYS`. This is the
   PICK / UniVerse / OpenQM model. Now PROJECT_STATUS §5.6.
2. **The install layout follows Windows standards**, not Unix: binaries under
   `C:\Program Files\SD\`, data and configuration under `C:\ProgramData\SD\`.
   Now §5.8.
3. **The installer becomes an Inno Setup binary** (preferred) or a PowerShell
   script, replacing `installsdai.sh`. Now §5.9.
4. **The data tree must be protected from snooping.** Now §5.7.

### This supersedes a decision made the same day

`f56de86` and `9c00730` had just committed the opposite model: SD administrator
rights from membership of an `sdadmins` local group, with `IsAdmin()` resolving
it through `getgrnam()`. That work is not wasted — `IsAdmin()` still gates
`sd -start`, which happens before any account or password exists — but it is no
longer the identity model. See §8 for what remains to decide about it.

### Corrections to what §8 recorded as evidence

The open question in §8 listed evidence favouring an internal administrator
flag. Two of the three points were wrong, and are corrected here.

**Wrong: "SD already has the machinery — login records carry `LGN$ADMIN`."**
The `$LOGINS` register was removed on 12 Jun 2024. There is no `$LOGINS` file
in `sdsys/`; every read and write of it is commented out in `LOGIN` and
`APISRVR`, including both `kernel(K$ADMINISTRATOR, lgn.rec<LGN$ADMIN>)` calls,
which were the only consumers of the flag. `LGN$ADMIN` survives in
`INT$KEYS.H` as a `$define` pointing at a file that no longer exists. An
internal flag would therefore have meant reintroducing a retired register, not
reusing existing machinery. `ACCOUNTS` cannot substitute directly — it is keyed
per account, not per user — though under the decision actually taken that turns
out to be exactly the right granularity.

**Overstated: "on the current design the OS is still the authority."** It is
not, inside the BASIC layer. `op_kernel.c` grants `USR_ADMIN` unconditionally
for any positive argument, so any user who can run BASIC can call
`kernel(K$ADMINISTRATOR, 1)` and become an SD administrator — which is exactly
what `CPROC` does. `IsAdmin()` is consulted only when the argument is zero,
which also reads backwards: passing "clear" *grants* admin to a group member.
The OS was genuinely authoritative only at `sd -start`. This hole must be
closed under the new model too, or the SDSYS password gate is decorative.

**Refined, not wrong: the re-logon delay.** It was recorded that an OS group
cannot make the installing user an administrator immediately, because Windows
fixes group membership in the token at logon. That is correct for `IsAdmin()`,
which reads the token via `getgroups()`. It is *not* correct for the BASIC
layer's `is_grp_member`, which reads the group's member list and so sees a new
member at once. The two would have disagreed for one logon — SD granting access
the OS would still refuse — which is worse than failing closed. Moot under the
decision taken, but worth not rediscovering.

### `/etc/group` does not exist under MSYS2 — a blocker, found before it bit

`IS_GRP_MEMBER` reads `/etc/group` as a text file. MSYS2 and Cygwin dropped
`/etc/passwd` and `/etc/group` years ago in favour of direct SAM/AD lookups, and
neither file is present on this machine. So `is_grp_member` sets status 1 and
returns false for every caller, which fails the `sdusers` test at `LOGIN` 193
and terminates every connection with "This user is not registered for SD use".

This sits one step past where runtime bring-up stopped, so it would have been
met head-on in the next session. It is *not* the `getgrnam()` path verified in
§4 — that goes through the NSS layer and works correctly. Under decision 1 the
`is_grp_member` calls are deleted rather than repaired, which disposes of the
blocker as a side effect.

### Data protection: what was found, and why it is stage 2

The premise behind decision 4 was that OS directory permissions keep an
account's contents private. Two findings, both verified on this machine.

**`chmod` cannot secure anything here.** The MSYS2 mount is `noacl`
(`none / cygdrive binary,posix=0,noacl,user`). `chmod 0770` on a test directory
left it `drwxr-xr-x` and changed no ACE. `C:\ProgramData` grants
`BUILTIN\Users:(I)(OI)(CI)(RX)` by inheritance, so a directory created there is
world readable and snooping requires no privilege at all.

**But ACL inheritance is unaffected by `noacl`, which makes the fix
practical.** Breaking inheritance and granting narrowly works, needs no
elevation for a directory you own, and — the useful part — files subsequently
created *through the MSYS2 shell* inside that directory inherit the restricted
ACL correctly, because NTFS applies inheritance in the kernel at creation time,
below the runtime. Verified by writing through MSYS2 into a locked directory
and reading back the resulting ACE. So the installer sets permissions once with
`icacls` and everything SD creates afterwards is protected automatically. This
also answers the `chmod g+s` problem left open earlier: the setgid directory
behaviour *is* inheritable ACEs.

Use SIDs rather than names in the installer — `*S-1-5-18` for SYSTEM,
`*S-1-5-32-544` for `BUILTIN\Administrators` — so a localised Windows does not
break it. `/inheritance:r` must come first; `/grant` alone leaves the inherited
`Users:(RX)` in place and the tree stays readable.

**The limit, and it is architectural.** Every SD process opens the database
directly — `dh_open()` → `dio_open()` → `open()` — in its own process, under the
invoking user's token. `connection_type` (`CN_CONSOLE`, `CN_SOCKET`, `CN_PIPE`)
describes only the terminal transport; there is no data server. So any ACL
strong enough to stop a user reading the files in Explorer also stops SD reading
them on that user's behalf. **While SD runs as the invoking user, account
passwords organise access but do not secure it.**

Real protection needs `sdlnxd` to become a Windows service under a dedicated
service account that owns the tree, with session processes spawned under the
*service* identity and users reaching them over the named pipe. That is the
direct Windows equivalent of the Linux original dropping to the `sdsys` user via
`EUID_SET`, not a Windows novelty. It requires console `sd.exe` to become a
client rather than doing its own file I/O, which is the substantial part, and it
belongs with the stage 2 `fork` → `CreateProcess` work. Until then the
achievable goal is blocking everyone who is not an SD user, which is worth
having and is not the same as privacy between accounts.

### Also found

The server and client disagree about the configuration file. `GetConfigPath()`
in `inipath.c` reads `SCARLET_CONFIG`, falling back to `/etc/sd.conf`;
`sysdir()` in `sdclilib/sdclilib.c` reads `SD_CONFIG`, falling back to `sd.ini`
in the Windows directory — and its comment claims the two match. They do not.
`sdnet.h` also hardcodes `PASSWD_FILE_NAME "/etc/shadow"`. Folded into §5.8.

The password machinery decision 1 needs already exists and is wired: `SD_SALT`
(100) and `SD_KEYFROMPW` (101) reach `crypto_pwhash` (Argon2) through SDEXT, and
`_INPUT` already supports masked entry via `IN$PASSWORD`. No new C code is
needed for salt, derive and compare.

### Where the verifiers must not go

The first draft of §5.6 said to add salt and verifier as ACCOUNTS fields 4 and
5, appended for backward compatibility. That is wrong and was corrected before
this entry was committed. `LOGIN` opens `ACCOUNTS` at line 175 in the user's own
process *before* authenticating — it has to, in order to know the account exists
— and eleven other programs open it as well, `_VOC_REF` among them for routine
resolution. Every SD user's process can therefore read it, and verifiers stored
there would let any user harvest every account's Argon2 hash for offline attack.

They go in a separate register keyed by account name. In stage 1 that file is
still readable by everyone, since Windows has no setuid and there is no
privileged helper short of the service model, so the split does not fix the
exposure. Its value is that the boundary exists from the start, so the service
model can lock one file down without restructuring ACCOUNTS or migrating data.

### Several people per account, and why one password each is not enough

Noted by the repository owner: a user account is sometimes reached by more than
one person — cover during holidays, assistants. A per-account password supports
that with no mechanism at all, which is a genuine advantage over the OS group
model where each person had to be enrolled and removed.

The first draft of §5.6 stopped there and listed the consequences — no
attribution, and rotation for everyone when one person's access is withdrawn —
as costs inherent to shared credentials, to be stated rather than engineered
away. **The repository owner rejected that**, and correctly: a single password
shared between people is a classic weakness, and raising the security level
above OpenQM was one of the motives for this whole change. A model that cannot
name who logged in fails the goal that prompted it.

An intermediate draft proposed a credential list per account — one name, salt
and verifier per person permitted into it. The repository owner replaced that
with something simpler and better, which is what §5.6 now records: **you log in
as your own account, and the login identity follows you.** Access to other
accounts is granted rather than shared, `LOGTO` needs no second password,
`@logname` never changes, and every login and every `LOGTO` is written to an
audit log as "SUE logged to JANE at *date/time*".

Sue covering for Jane is therefore not a shared password at all. Sue is granted
access to JANE, logs in as SUE, does `LOGTO JANE`, and the log records it.
Withdrawing the cover removes one grant; nobody's password changes, because
nothing was ever shared. Administration comes under audit for free, since SDSYS
is reached by `LOGTO SDSYS` from a named identity.

Grants are recorded on the target account — JANE lists who may enter JANE —
because that answers the question administration actually asks and puts
revocation in one place. `$LOGINS` chose the opposite direction with
`LGN$VALID.ACCOUNTS` and `LGN$BANNED.ACCOUNTS` per user; that register is gone
and there is no reason to inherit its shape. Worth recording that this session
earlier argued against reviving `$LOGINS` on the grounds that it was retired
deliberately — that argument survives, and the model arrived at needs no global
user register at all.

Attribution is SD-internal and does not depend on the service model, so it can
land with the password work. It records who authenticated, not who is at the
keyboard — accountability, not proof of identity.

**The audit log cannot be the existing one.** `LOGMSG` reaches `log_message()`
in `k_error.c`, which writes `<sysdir>/errlog` and, on reaching the configured
`ERRLOG` size, discards the oldest half of the file. Correct for a diagnostic
log, disqualifying for an audit trail. The trail needs its own append-only file
that rotates rather than truncates. Also note `CPROC` reassigns `logname` when
it drops to `sdsys` (around line 278); under this model nothing may overwrite
the login identity.

Separately, none of this makes accounts *private* from each other in stage 1.
Entering an account requires the user's own token to hold read and write on that
account's directory, and the OS cannot tell that token apart from the same
person browsing the directory in Explorer. Privacy between accounts waits for
§5.7.

### Still open

Recorded in §8: whether `sd -start` keeps an OS-level check now that
`IsAdmin()` has no other purpose, and whether the console entry point survives
the service model. Both shape stage 2.

---

## 13 Aug 2026 — Runtime bring-up started; IPC verified; session ended on credits

**Session ended mid-task.** Handing off to another account. Resume at
PROJECT_STATUS §3, "Runtime bring-up", and answer the question at the top of §8
before doing further identity work.

Built the runtime environment for the first time: `/etc/sd.conf` pointing at
`/usr/local/sdsys`, that tree populated from `sd64/sdsys` plus `bin` and
`terminfo`, and the account directories under `/home/sd`. None of this is in
the repository; it exists only on this machine.

**The IPC port is now largely de-risked.** `sd -start` was blocked behind the
administrator check, so rather than leave the shared memory work unexercised,
the create/attach/detach/unlink cycle was run standalone at 3 MB in the shape
`sysseg.c` uses: create, size, map, attach from a second mapping, verify size
and content, verify writes are visible through both mappings, create six
semaphores, verify exclusion while held and reacquisition after posting, unmap,
unlink, and verify a later attach gives ENOENT. Everything behaved. That was
the largest single unknown in the port.

**`IsAdmin()` was proved in the linked binary, in both directions.** `sd -start`
refused while `sdadmins` did not exist, and got past the check once built
against a group the token holds. On the way, `check_admin()` in `sd.c` turned
out to be a third privilege path that the earlier survey missed: it tested
`geteuid() != 0` and `in_group("admin")` rather than `IsAdmin()`. It now defers
to `IsAdmin()`, so there is one definition of an SD administrator.
`SD_ADMIN_GROUP` was made `#ifndef`-guarded so a site, or a probe build, can
override it.

**A correction worth recording.** When `sd -start` first printed "Command
requires administrator privileges", that was reported as the new `IsAdmin()`
working. It was not — it was `check_admin()`, which at that point did not call
`IsAdmin()` at all. The conclusion happened to be right in the end, but it was
asserted before being checked.

**The friction that matters for the design.** The `sdadmins` group was created
and `GITORLI\don` enrolled, and it still did not take effect: Windows fixes
group membership in the access token at logon, so the group resolved by name
while `getgroups` did not list it. Elevation does not help. That directly
contradicts the requirement that the installing user become an administrator
automatically, and is the strongest argument for the internal-flag alternative
raised the same day. Recorded as the open question at the top of PROJECT_STATUS
§8, unanswered.

**Bootstrap progress.** `gplbld/bbcmp.py` and `gplbld/pcode_bld.py` both run on
Windows unmodified — `gcat` now holds `$BBPROC`, `$BCOMP` and `!PATHTKN`, and
`PCODE.OUT` is populated. The sequence stops at `sd -i`, which reports "SD has
not been started" while `sd -start` refuses because `config.c` requires
`gcat/$CPROC`, which only the last bootstrap step produces. That ordering is
the immediate puzzle and is written up in §3. Given the isolation testing
above, suspect the bootstrap sequence rather than the IPC port.

---

## 13 Aug 2026 — PROJECT_STATUS rollover limit raised to 800 lines

**Commit:** documentation only.

The limit was ~400 and was raised to ~800 on the repository owner's
instruction. Earlier entries below refer to the old figure; they are left as
written, per the append-only rule, and this entry supersedes them on that
point.

400 proved too tight for the size of this port. The file crossed it twice in a
single day of work and both crossings forced a compression pass, which is
attention spent on housekeeping rather than on the port. The material was
genuinely needed — the privilege model, the BASIC layer survey and the identity
decision are all things a new session has to know before touching anything.

A note was added alongside the rule making the intent explicit: the limit is a
prompt to prune, never a reason to leave a finding out. Where something must
go, detail duplicated in HISTORY.md goes first, since nothing is lost by it.

An alternative was considered and not taken: splitting the §5 decisions into a
separate ARCHITECTURE file. Raising the limit keeps one document to read first,
which is the property that makes the handoff work across accounts.

---

## 13 Aug 2026 — Windows identity model decided; IsAdmin() reimplemented

**Commit:** see below. Code change is confined to `IsAdmin()` in `linuxlb.c`
and `SD_ADMIN_GROUP` in `sddefs.h`.

Context from the repository owner: on Linux, SD itself creates OS user
accounts, and administrator access is obtained by running `sudo sd`. Both
needed rethinking for Windows.

**What SD does today.** Every account operation shells out through `sudo`:
`useradd -m` in `CREATE_USER`, `passwd` in `SET_PASSWD`, `usermod -aG` in
`CREATEA` and `MODIFYA`, `groupadd` in `CREATEA`, `userdel` and `groupdel` in
`DELACC`, and `chmod g+s` in `CREATEA`. The installer creates the `sdusers`
group and the `sdsys` system user. SD's security model is therefore delegated
to the operating system: its accounts are real OS users and file access is
enforced by group ownership plus setgid directories.

**Three things established before deciding.**

`sudo sd` can survive as a command form: `sudo.exe` is present at
`C:\WINDOWS\system32\sudo.exe` on this machine, though disabled. But it does
not restore the mechanism — an elevated MSYS2 process still reports
`uid=197609`, because Cygwin derives the uid from the security identifier and
elevation does not change it. What elevation changes is group membership and
integrity level.

The original had a Windows answer and it should not be copied. `LOGIN` in the
external GPL.BP tree sets `lgn.id = 'Console'` and forces
`lgn.rec<LGN$ADMIN> = @true` for any console session, with a neighbouring
comment explaining that authentication was "alien" to Windows 95/98/ME. On a
modern system that would make anyone able to run `sd.exe` an SD administrator.

`chmod g+s` is the one command with no equivalent. Everything else maps to
`New-LocalUser`, `New-LocalGroup`, `Add-LocalGroupMember` and so on; the setgid
directory behaviour is inheritable ACEs, `icacls <dir> /grant "<g>:(OI)(CI)M"`.

**Decisions taken.** SD no longer creates or deletes OS accounts; it maps onto
Windows users and groups that already exist. This keeps OS-enforced file
security without SD holding standing administrative rights, and does not break
on a domain-joined machine. Administrator rights come from membership of the
`sdadmins` local group rather than from elevation, which separates SD
administration from Windows administration, needs no UAC prompt, and works for
a service.

**Implemented.** `IsAdmin()` was `getuid() == 0`. It now resolves
`SD_ADMIN_GROUP` with `getgrnam()` and tests the primary group and the
supplementary list, failing closed when the group does not exist. Verified
first that the mechanism works at all: `getgrnam()` resolves Windows local
groups on the MSYS2 runtime (`Users` 545, `Administrators` 544) and reports
membership accurately. The function body was then exercised as a standalone
copy against member, non-member, absent-group and primary-group cases, all four
as intended. The linked `sd.exe` path remains unexercised because SD does not
start.

**Deliberately not done, and why.** The BASIC side is untouched.
`sdsys/GPL.BP.OUT` contains only a README — there are no compiled objects in
the tree — and the installer compiles the BASIC with
`bin/sd -internal BASIC GPL.BP CPROC` after `gplbld/pcode_bld.py`. A BASIC edit
is therefore inert until SD runs and can compile it, so writing those changes
now would produce source that cannot be tested and does not match anything
executable. Recorded as a trap.

Note that the new `IsAdmin()` does **not** by itself unblock SDSYS or
`CATALOG GLOBAL`: those sites test `SYSTEM(27)` directly rather than
`K$ADMINISTRATOR`, so they still always deny. That is part of the pending
BASIC work, not an oversight.

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
