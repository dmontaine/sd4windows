# PROJECT STATUS

Living handoff document for the SD Windows port. This project moves between
sessions, machines and accounts; anything not written here is lost. Read this
file first. Read [HISTORY.md](HISTORY.md) only if you need the record of how
something came to be the way it is.

***SEVENTY-NINTH SESSION, 29 Aug 2026 — THE ADMINISTRATOR ACCESS MODEL IS REWRITTEN BY THE OWNER. READ PRE_RELEASE 56 BEFORE TOUCHING `LOGIN`, `CPROC` OR `CREATEA`.*** Started as PRE_RELEASE **31**, one of the three open **B** entries, whose ruling named a prerequisite nobody had done: *trace the ssh and API routes before choosing where the fix goes.* **The trace is what moved the model.** ***BOTH DOORS ARE GATED AT CONNECTION TIME AND A `LOGTO` CANNOT REACH EITHER*** — ssh at `sshd_config` then `LOGIN:427`/`:477`, the API at `APISRVR:1463` inside the SCRAM handshake — so the ruling's ssh and API halves were already satisfied and only `os.execute` was in question. **Two things the entry did not have**: `sh` (`CPROC:3519`) is a **second** gate on the same flag, and `IsAdmin()` answers TRUE for every API session unless it carries `kernel.c:240`'s `CN_SOCKET` guard, because `getuid()` stays SYSTEM through `AssumeUserIdentity()`. ***PUT TO THE OWNER, HE REVERSED HIS OWN 29 Aug RULING AND REPLACED IT WITH A WHOLE MODEL*** — administrators elevated **at login** into **SDSYS**, **no account of their own**, and **the rights of whatever account they logto**. **It supersedes three recorded decisions, all taken knowingly**: 15 Aug's *"nobody logs in to an account but their own"*, the 29 Aug ruling on 31 (withdrawn the same day, **B → S**, because clause 5 is what `CPROC:2735` already does), and **PRE_RELEASE 2, a closed B, now re-opened**. ***AND IT COSTS ADMINISTRATORS ssh***, which is a consequence rather than a choice: UAC has no desktop there and they no longer have an account to fall back to. ***MEASURED AND UNWELCOME: A NON-ADMINISTRATOR CAN REACH SDSYS TODAY*** — `elevate('START')` gates on `Start-Process -Verb RunAs` and tests nobody's identity, so an administrator's password is enough, and the trail then names the wrong person. **Open count 17 → 19** from `test-fixlist-units.ps1`, **188 passed / 0 failed**.

***AND THEN 56 WAS BUILT, EXCEPT FOR THE ONE PIECE THAT NEEDS A RULING.*** Five of its six product changes are written: **`K$OS.ADMINISTRATOR` (63)** — *is the signed-in **person** an administrator*, carrying `kernel.c:240`'s **`CN_SOCKET` guard**, without which it answers TRUE for every API session; **`LOGIN` elevates an administrator and lands them in SDSYS**; **the `sdusers` gate exempts them**; **`logto sdsys` is refused unless the person is an administrator**; and `ELEVATE`'s *"only one caller"* note is amended, LOGIN being the second. ***THE C HALF IS MEASURED AND THE BASIC HALF IS NOT***: `make sd` **exit 0 with 0 warnings in the whole log**, `op_kernel.o`'s mtime moved so the compile is proved rather than assumed, `bin/sd.exe` relinked 09:36 at 1,960,318 bytes. **The BASIC is uncompiled — a cycle is what tests it.** ***THE `sdusers` GATE IS THE FINDING WORTH READING***: it runs at `LOGIN:380`, **before** the account is chosen, and the model gives an administrator no account — so nothing would ever have put them in that group and **every administrator would have been refused at the door.** Found by reading; it would otherwise have cost a cycle and looked like a broken login. ***AND THEN THE LAST TWO PIECES WENT IN.*** **`CREATEA` no longer writes an ADMINISTRATOR-tier account into `os.users`** — and that is not a withdrawal of access but the same 27 Aug ruling arriving by 56's route: an administrator is elevated at login into SDSYS, where `USR_ADMIN` answers `os_permitted()` at `op_sh.c:161` **before** the file is read. Writing it there **leaked `OS.EXECUTE` past a `LOGTO`**, because `os.users` is keyed on the person. **ssh and the API are untouched** — both are connection-time group tests and cannot follow a `LOGTO`. ***SO PRE_RELEASE 31 SHOULD NOW PASS WITH NO EDIT TO `verify-apiadmin` AT ALL***, its original `expected False` being right again. ***AND THE HELPER IS ONE PER USER, WHICH IS THE COST OF 56 FOUND BEFORE IT WAS PAID***: elevating at login made `sd-elevate.ps1 -Start` run on every `sd.exe`, and its shortcut needs `IsInRole` on the **process** token — False for an *unelevated* administrator — so it prompted **every time**, against 13 unelevated verifiers that pipe straight into `sd.exe`. **`sudo` does not help and was measured**: its own help says it prompts on every invocation, no cache, unlike Unix — and it ships, which `sd.iss` refuses. **The pipe is now `sd-elev-<logname>`; `PING <pid>` registers and `STOP <pid>` deregisters, so the helper still dies with its sessions — it just has more than one.** Both scripts **parse 0 errors with functions found**, no BOM, CR 0. ***STILL OPEN AND IT IS THE LARGER HALF***: those 13 verifiers mean *"run `sd` as an ordinary user"*, which works only because the owner is an administrator **with an account** — a combination clause 2 abolishes. **The suite needs a real non-administrator account for that half.** ***AND `adopt` IS RULED UNNECESSARY BUT NOT REMOVED*** — 20 files including the installer's wizard flow, kept separate on purpose so a broken install has one candidate cause; harmless meanwhile, since the account is simply never entered.

***IT ALL COMPILES — `cycle.ps1 -SkipInstall`, 29 Aug 2026 10:22, AND THE STAGED TREE WAS READ RATHER THAN THE RUN'S OUTPUT BELIEVED*** (the 26 Aug precedent). Installer `sd-setup-W1.0-0.exe` **4,891,787 bytes**. `gpl.bp.out/TIERGATE` **and** `gcat/!TIER_ALLOWS` both exist; **all eight** changed programs recompiled at 10:22 — `CPROC`, `LOGIN`, `ELEVATE`, `GRANTA`, `MODIFYA`, `APISRVR`, `CREATEA`, `TIERGATE`; messages **10126** and **10127** staged; both elevate scripts staged **byte-identical** to source (their 10:13 stamp is preserved source mtime, checked with `cmp`, not a stale copy). ***THE WARNING CLASS IS CLEARED TOO, WHICH A GREEN BUILD DOES NOT NORMALLY PROVE***: `bootstrap.py`'s `check_compile()` **dies** on any *"is not assigned a value"* warning — the ERRGEN trap, a run-time abort in a program that may not run for weeks — so reaching ISCC clears `admin.login`, `tg.why`, `ma.why` and TIERGATE's locals. ***THE COUNTS ARE NOW `gcat` 127 / `gpl.bp.out` 186***, and **the 125 / 184 recorded under §"THE MACHINE" is a stale baseline, not a disagreement**: `PROFILE_DIR` arrived with PRE_RELEASE 36 on 28 Aug after that line was written, and `TIERGATE` is the second — both checked present rather than assumed. ***AND THEN IT RAN. FULL CYCLE 29 Aug 10:35:46, `-Run b59`.*** ***ELEVATED 19 OF 19 — 397 PASS, 0 FAIL, 0 SKIP, GREEN FOR THE FIRST TIME*** — and ***PRE_RELEASE 31 IS CLOSED***: `verify-apiadmin` **22/22** with `[PASS] control: local elevated session refused OS.EXECUTE: expected False, got False`, after failing on five consecutive runs, **and with no edit to the verifier at all**. 56 stopped `CREATEA` writing administrators into `os.users`, so `os_permitted()` falls through to a lookup that finds nothing. ***THE RECORDED "21/23" WAS WRONG IN THE DENOMINATOR*** — b58's own log reads 21 PASS / **1** FAIL, so it was always 22; carry **22/22**. ***UNELEVATED 8 OF 13, AND ALL FIVE FAILURES ARE ONE CAUSE — NOW PRE_RELEASE 59.*** `verify-lcnames` names it: *"the session is in the account, not SDSYS"*, `[FAIL] WHO names the account`. With `osusers`, `nocase`, `lineendings`, `batchjob` — every one assumes an administrator lands in an ordinary account, which clause 2 abolishes. ***NOT PRODUCT DEFECTS: NOT ONE SCORED A FALSE PASS***, each refused the null case out loud, which is the instrument rule holding on the first run that broke its premise. ***NO UAC STORM — THE HELPER WIDENING HELD***: every step logged in and `assert-current` passed in each. ***AND THE TRANSCRIPTS ARE UTF-16***: a plain `grep` for `[PASS]` reports **0 PASS / 0 FAIL** on a full 25KB log, which reads exactly like a step that did nothing — `Get-Content` or `iconv -f UTF-16LE` first.

***AND THEN A SECOND OWNER'S RULE, PRE_RELEASE 57 — A GRANT MAY GO DOWN OR SIDEWAYS, NEVER UP.*** *"Standard accounts can not be given access to programmer accounts … Only windows administrators can enter SDSYS, rights to SDSYS can not be granted."* ***IT CAME OUT OF MEASURING WHAT A GRANT ACTUALLY HANDS OVER***, which nothing had written down: **the verb set follows the ACCOUNT** — the tier is applied to the account's own physical VOC at creation (`CREATEA:1184`), so a standard user entering a programmer account got **+42 verbs** — while **`sh`/`os.execute` follow the PERSON** and a `LOGTO` never moves them (`CPROC:3548` says so outright). New `gpl.bp/TIERGATE` (`!tier_allows`), messages **10126** and **10127**, changelog entry. ***FOUR CALLERS, TWO OF THEM GATES***: `logto.authorised` and **`APISRVR`'s `vb.account`** — the API reaches an account through neither `LOGIN` nor CPROC, exactly as the 17 Aug `ACC$GROUP` note says, so **omitting it would have been the way round the whole rule**; `GRANTA` and `MODIFYA`'s ADD arm are the courtesy refusals. ***A CHECK ONLY AT GRANT TIME WOULD BE UNSOUND***: the grant IS a Windows group membership, so `net localgroup` makes one without SD, and `modify.account b programmer` can raise a tier after a legal grant with nothing revisiting the group. **`REVOKE` and `… DELETE` are deliberately unguarded** — taking access away is always allowed. **`!tier_allows` is `$internal` because `net_path_permitted`'s allow-list excludes `@sdsys/accounts`**, so an API session could not otherwise read it. ***UNCOMPILED, and one piece is left: promoting an account silently strands the grants it just voided*** — the gate holds, but nothing reports it. **57's "Left to settle" has the two options; the owner's call.**

***SEVENTY-EIGHTH SESSION, 29 Aug 2026 — THE 21 SILENT HEADINGS ARE DONE, AND THE NOTE IS NOW A TRIPWIRE.*** The smallest of the six decisions taken on 29 Aug, and the only one that needed no install, no elevation and no cycle. **All 21 struck-but-silent sections in PRE_RELEASE_FIXES.md carry `DONE <date>` in their own heading** — 5, 10, 13, 14, 15, 19, 21, 22, 23, 25, 26, 27, 30, 32, 33, 35, 36, 37, 38, 40, 41 — **each date taken from that entry's own index row or section body, not from the session it was noticed in** (21, 30, 32 and 33 are 27 Aug; the rest 28 Aug). `test-fixlist-units.ps1` **184 passed / 0 failed** and its NOTE is gone. ***THE POINT WAS THE GUARD, AND THE GUARD WAS MEASURED IN BOTH DIRECTIONS RATHER THAN ARGUED***: the same re-opening — row 41 un-struck — now **FAILS, exit 1**, and scored **184 passed / 0 failed, exit 0** against the old silent heading. **21 `Edit` calls, no script, and the bytes checked after**: 21 insertions / 21 deletions, every added line a `## ` heading, no BOM, CR 0, em dashes +21. ***THE OPEN COUNT IS UNCHANGED AT 17*** — this was never an entry, so closing it moves nothing. **Nothing under `gplsrc` or `sdsys` was touched, so the cycle owed since session 75 is still owed.**

***SEVENTY-SEVENTH SESSION, 29 Aug 2026 — DECISIONS ONLY. SIX RULINGS RECORDED, NOTHING BUILT, NOTHING TOUCHED UNDER `gplsrc` OR `sdsys`.*** The owner asked for the decisions and said explicitly **not** to start the work. **The three that were his** — PRE_RELEASE **31**, **34**, **39** — are ruled and written into PRE_RELEASE_FIXES.md with his words quoted. **The three verifier questions he handed back** (*"your call on the verification utilities i have no opinion"*) are decided too, and two of them are now **PRE_RELEASE 54 and 55** rather than a paragraph in this box. ***THE OPEN COUNT IS 17 — READ IT FROM `gplbld/test-fixlist-units.ps1`, 184 passed / 0 failed, NEVER FROM PROSE.*** It went 15 → 17 by **filing**, not by breaking: 54 and 55 were always tasks and were merely uncounted. ***31 CHANGED CHARACTER UNDER ITS RULING AND THAT IS THE ONE TO READ BEFORE TOUCHING IT***: it was filed as a stale verifier on its own conclusion that *"the product is doing what PRE_RELEASE 2 designed"*, and the owner's rule — *"any administrator keeps universal rights ... no matter which account they logto"* — **is wider than the code**. `CPROC:2713` clears `USR_ADMIN` on a `LOGTO`, so an administrator with no `os.users` record **is refused today**; `don` passes only because PRE_RELEASE 2 listed him, which made the passing case an accident of another entry. **Sev S → B, and it is a C change.** ***AND 55 GOT SMALLER BY BEING READ RATHER THAN RESTATED***: `release.ps1` calls `mkdoc.py`, `mkpdf.ps1` and `checklinks.py` and **neither `mktclsyntax.py` nor `tclmap.py`** — both of which already compute the roster and already `exit 1` on disagreement, which is why they sat refusing for a week with nothing knowing. **The comparison was built; the wiring was missing.** ***NOTHING IS IN FLIGHT AND NOTHING IS WAITING ON THE OWNER.*** Two commits, both pushed. **THE CYCLE FROM SESSION 75 IS STILL OWED** — sessions 76 and 77 were both documentation-only, so `assert-current` still exits 1 and the box below still opens with the right first step.

***SEVENTY-FIFTH SESSION, 28 Aug 2026 — PRE_RELEASE 36 IS DONE: ALL FOUR RULINGS BUILT, COMPILED, INSTALLED AND OBSERVED.*** The sweep reclaimed **5 of 5** after a restart and `C:\Users` fell **61 → 56 by exactly those five**; `create.account` refuses a live profile directory (`verify-profiledir.ps1` **14/14**). *(Getting there: `make sd` 20:44 — `sdsvc.exe` 144,301 → 146,089 bytes — because the first cycle at 20:40:17 staged the **26 Aug** binary and `cycle.ps1` does not build. Three defects were found and fixed on the way, **49**, **50** and **51**, and two of the three were instruments rather than the product.)* ***THE START HERE BOX CARRIES A FIVE-STEP LIST THE OWNER ASKED TO BE REMINDED OF: `make sd`, cycle, suite `-Run b55`, RESTART, then read `C:\ProgramData\SD\reclaim-profiles.log`.*** **The restart is the step that actually tests 36** — the sweep runs only when `sdsvc.exe` starts the service, and the hives it waits on come down at shutdown. `DELETE_USER` takes the DIRECTORY first and removes the `ProfileList` entry only if that succeeded, which **reverses part of 32 on the owner's ruling**: the entry is the only handle any sweep has, and 28 Aug measured three folders on this host that nothing could find without it. Both halves are kept together otherwise and recorded under `C:\ProgramData\SD\profile-reclaim`; `gplbld/reclaim-profiles.ps1` takes the pair at every boot and **reads the RECORD, not `ProfileList`**. `create.account` refuses a name whose profile directory is still there and names it (`gpl.bp/PROFILE_DIR`, 10124/10125). **New status 8** — left behind AND not recorded — so 6's new promise of a reclaim is never printed about a pair nothing is coming back for. ***THE WINDOWS HALF IS MEASURED AND THE BASIC HALF IS NOT***: `sdsvc.c` compiles 0 warnings under `-Wall -Wformat=2`; `gplbld/test-reclaim-units.ps1` drives the sweep's refusal table **39/39** with no install, elevation or store, and its **positive control fails 34/5** against a copy with the containment check removed; the sweep was watched running three ways unelevated. ***THE STORE GETS AN ACL OF ITS OWN AND THAT IS NOT TIDINESS***: `C:\ProgramData\SD` grants `sdusers:(OI)(CI)M` to everything underneath, so a reclaim store left to inherit would be **a list of directories every SD user can edit and LocalSystem later deletes** — `PS_SCRIPT`'s SDSYS\PSTMP escalation in a new place. `gplbld/secure-reclaim.ps1` at install time, `DELETE_USER` on an older tree, and the sweep re-asserts it every boot. ***THE SWEEP NO LONGER SKIPS A RECORD ON ITS OWNER, AND THE ACL IS NOW THE WHOLE OF THAT CONTAINMENT — PRE_RELEASE 43, owner's ruling 28 Aug 2026.*** The owner check refused **every record `DELETE_USER` will ever write**: an elevated process owns what it creates by its **own** SID, not `BUILTIN\Administrators`. Measured on the 20:48:24 install — five genuine records, five refusals, nothing reclaimable on any machine. **The 39/39 above is exactly how it got shipped**: every accepted row handed in SYSTEM or Administrators and none handed in what the producer actually writes, so the suite drove every way the guard said no and never the one path where it had to say yes. The rows are turned round and the control is `-Sweep` at the pre-43 copy, **37/2**, red on those two alone. **32's regression test is re-scoped** from *"the entry is gone"* to *"the entry is gone when the directory went"*.

***SEVENTY-THIRD SESSION, 28 Aug 2026 — THE CYCLE RAN, THE SUITE RAN, AND THE DOOR STEP FAILED TWICE. ONE FAULT IS FIXED; THE OTHER RE-OPENS PRE_RELEASE 19.*** ***INSTALL 28 Aug 15:29:59, `assert-current` exit 0 live*** — the owner's cycle shipped PRE_RELEASE 42 (`CREATEA`, `SET_PASSWD`, message 10122). ***FAULT 1, FIXED — PRE_RELEASE 43***: `verify-doors-suite.ps1` passed `'-Password', ''` for Suspend and Remove, and **`Start-Process -ArgumentList` carries `[ValidateNotNullOrEmpty()]`, which on a COLLECTION validates every ELEMENT** — one `''` rejects the whole list and **nothing elevates**. Create carried a password and ran 8/8; Suspend and Remove died before their UAC prompt. The pair is built conditionally now, the argv and its count are printed, an empty element is refused by name, and `gplbld/test-doorsargv-units.ps1` guards it — **35/35, and its positive control against a copy carrying the old form fails 27/8.** ***FAULT 2, AND IT IS THE INSTRUMENT — PRE_RELEASE 19 IS RE-OPENED ON ONE ROW OF SEVEN***: `verify-doors.ps1:255` anchored *"logto entered the account"* on the account name **anywhere in the transcript**, and the session echoes what it is fed. **On the b50 Control leg SD printed 5161 *"Unable to change to new directory"* and `WHO` answered `91 DON`, and the row scored PASS** — as it did on `sddr2`, which is what *"logto ADMITTED"* below rests on. **The check now anchors on `WHO`'s answer with 5161 as a disqualifier**, both directions measured against the real transcript. ***THE CAUSE IS PRE_RELEASE 44 AND IT IS WINDOWS, NOT SD***: `don` is in `sdu_sddrb50a` **on the machine** and **not in his token**, which was fixed at logon — measured both ways, with `sdusers` present as the control. **ssh and the API authenticate afresh and are unaffected; the REFUSAL half of all three doors still stands**, because `logto.authorised` runs at `CPROC:2679`, before the chdir at `:2691`. ***THE ELEVATE-ONCE REWORK IS DONE AND WITNESSED — `-Run b54`, 28 Aug 2026 19:28.*** ***ALL FIVE DOOR LEGS GREEN THROUGH THE HELPER, ONE UAC PROMPT INSTEAD OF THREE***, and the elevated half's only failure is 31's known control again. `Create`, `Suspend` and `Remove` each printed `via helper:` with the password **masked**; the run left **no accounts, 0 orphan SIDs, no stray `sd.exe`**, its work directory gone, the helper stopped and its pipe closed. **The four pre-fix leaked directories were removed by hand after measuring all four empty; `C:\Users\dmont\AppData\Local\Temp` now holds none.** ***ONE FALSE ALARM ON THE WAY, AND IT IS NOW A §6 TRAP***: the check for a surviving helper matched **its own query process**, because a `CommandLine -like '*sd-elevate-helper*'` filter names the thing it is looking for. **The pipe being absent is what actually proved it gone** — evidence that cannot name itself.

***THE ELEVATE-ONCE REWORK AS BUILT — PRE_RELEASE 48, on the owner's ruling.*** The door suite's three elevated legs now go through **one resident helper**, reusing the shipped `sd-elevate.ps1` rather than growing a second copy of elevation code. ***A SUITE RUN GOES FROM FOUR PROMPTS TO TWO, NOT ONE***: `sd-elevate.ps1` hard-codes a 300 s per-request timeout, which each door leg fits inside and `VerifyInstall2`'s 19 verifiers do not — **taking it to one means editing a shipped file and spending a cycle, which is his call.** **`-NoHelper` keeps the route `b53` went green on**, and `test-doorsargv-units.ps1` drives both — **51 of 51**. ***THE PASSWORD MOVED FROM A COMMAND LINE INTO A FILE, AND THAT IS A STEP UP — MEASURED***: `Win32_Process.CommandLine` hands a same-user process the argument **verbatim**, while a `%TEMP%` file carries SYSTEM, Administrators and the user only, and is deleted in the `finally`. **The old comment had it backwards.** ***TWO DEFECTS FELL OUT OF TESTING IT, BOTH FIXED — PRE_RELEASE 47***: `$work` was created above the residue check so **every refused run leaked a temp directory (four were on disk, all measured empty)**, and two runs in the same second collided on the `HHmmss` name and **died exit 1 from a script whose refusal code is 2**. ***UNRUN — `-Run b54` is what exercises the helper***, and if it cannot start, the suite falls back to a prompt per leg rather than failing.

***PRE_RELEASE 19 IS CLOSED — `-Run b53`, 28 Aug 2026 18:02. ALL FIVE DOOR LEGS GREEN, BOTH TOKENS EXERCISED.*** `Create` **13/13**, `Control` **8/8**, `Suspend` **5/5**, `Refused` **5/5**, `Remove` **4/4**; *"verify-doors-suite: PASSED - all 5 legs green, both tokens exercised."* ***ALL THREE DOORS ADMITTED THEN ALL THREE REFUSED, THE SUSPENSION THE ONLY CHANGE*** — ssh and `logto` in SD's own words (10107), the API by the controlled pair. **The `logto` door is genuinely covered**: `WHO` answered `91 SDDRB53A from SDDRB53B`, so the session *arrived*, and 5161 did not appear. ***AND THE REFUSED LEG PROVED THE ORDERING***: *"logto: it was NOT 5161 instead of the suspension"* passed, so `logto.authorised` (`CPROC:2679`) stops it before the token-dependent chdir (`:2691`) — which is why every refusal measured while 44 was unfixed was still trustworthy. **Step 19 `verify-tierapi` is green, so PRE_RELEASE 46 is confirmed fixed**; the elevated half's only failure is `verify-apiadmin`, PRE_RELEASE 31's known control. **Nothing left behind**: no accounts, no `sdu_` groups, no `ACCOUNTS` records, **0 orphan SIDs**, only profile directories (35/36). **One non-decisive row FAILED in the Refused leg and is fixed**: it asserted 5161 always appears, but the suspension stops the local `LOGTO` before the chdir — the claim is Control-only now, and the Refused phase asserts the ordering instead. **`b53` is spent; `b54` is next.**

***THE `logto` DOOR OPENED ON `-Run b52`, AND THE ONLY THING STILL FAILING IS THE CHECK.*** 17:41:23, the full suite: **13 unelevated steps and all 19 elevated ones** — the first time the elevated half has run on this install, on the owner's `-ContinueOnFailure` ruling. ***`Create` 13/13 with the helper granted and Windows agreeing; `WHO` answered `91 SDDRB52A from SDDRB52B` and 5161 DID NOT APPEAR***, so PRE_RELEASE 44's two-account cure works and the non-decisive local witness failed in the same transcript as designed. **`Remove` 4/4 took both accounts away.** ***THE CHECK WAS WRONG IN THE OPPOSITE DIRECTION TO THE ORIGINAL***: it required the account to be the whole of the second field, and `WHO` appends `from <ACCOUNT>` only on the success path — the first version matched the name anywhere and passed on failure, its replacement matched only at end of line and failed on success, and **both were written from a transcript of the path they were not meant to catch.** Now anchored on the shape plus a second decisive row on the `from <helper>` clause, **five paths measured**. ***THREE FAILURES IN THE RUN, ALL THREE DIAGNOSED, NONE OF THEM THE PRODUCT***: the door check above; `verify-apiadmin` step 14, **byte-identical to b49's and three runs before it**, PRE_RELEASE 31 open; and `verify-tierapi` step 19, **PRE_RELEASE 46, new** — it carried ADMINISTRATOR **417** while `verify-tiers` carried **416** and the tree says 416, one fact in two files with nothing comparing them. **`gplbld/test-tiercounts-units.ps1` is the class fix**, 13/13, control against the pre-fix pair from `git show` fails 12/1. **`b52` is spent; `b53` closes 19.**

***TWO RULINGS TAKEN AND ONE BUILT, 28 Aug 2026: "two accounts, as the door table says" (PRE_RELEASE 44) and "rerun with `-ContinueOnFailure`".*** The door pair now creates a **helper account `<prefix>b`**, grants it into the account's `sdu_` group and issues the `LOGTO` **from inside the helper's ssh session** — a fresh logon whose token carries the group. The local `LOGTO` still runs and is recorded **non-decisive**, so the transcript carries the reason the helper exists. ***UNRUN — the Create leg is elevated, so `-Run b52` is what tests it***, and it now costs **four UAC prompts and two profile directories**. All three refusal paths were re-exercised unelevated (**exit 2, nothing created**), all four scripts parse 0 errors with no BOM, `test-doorsargv-units` **35/35**. **`CREATE.ACCOUNT ... PROGRAMMER SSH` was checked against `CREATEA:1409`'s own case block rather than assumed** — `SSH` and `BOTH` are branches of one loop. ***BOTH FIXES ARE WITNESSED, NOT MERELY WRITTEN — `-Run b51`, 16:51:50.*** Twelve unelevated steps exit 0; the door step exit 1 with **`Create` 8/8 on `argv (15)`, `Control` 2 of 7 FAILED (both `logto`, while ssh and the API admitted in the same leg), `Remove` 2/2 on `argv (13)`** — ***and `Remove` ran as a suite step for the first time ever***, so `sddrb51a` left no Windows account, no `sdu_` group and no `ACCOUNTS` record. **The three-door comparison inside one leg is what makes 44 solid**: same account, same session, two doors in and one out. ***ON THE MACHINE NOW: `sddrb50a` IS STILL LIVE, ENABLED AND UNSUSPENDED*** in `sdusers`, `sdssh` and `sdapi` — its Remove leg never ran. **START HERE has the command that takes it away.**

***SEVENTY-SECOND SESSION, 28 Aug 2026 — THE THREE DOORS ARE COVERED AND PRE_RELEASE 19 IS CLOSED.*** *(Corrected 28 Aug 2026 by the seventy-third session: the `logto` door was not covered — see above. The ssh and API doors, and all three refusals, stand.)* The `verify-doors` pair ran end to end on `sddr2` and **every leg passed**: `Create` 8/8, ***`Control` 6/6 — ssh, `logto` and the API ALL ADMITTED*** — `Suspend` 5/5, ***`Refused` 4/4 — ALL THREE REFUSED***. `LOGIN:477` and `CPROC:3776` said it in SD's own words (10107), **ssh after the banner** so authentication had succeeded and the refusal is SD's, with the account **still in `sdssh`** so no Windows group moved. ***THE API DOOR WAS REACHED FOR THE FIRST TIME***, and since it cannot identify its own refusal, **the controlled pair is the proof**: same account, same password, same call, admitted then refused, the suspension the only change. ***THE OWNER'S RULING — "19 stays B until the doors are covered" — IS SATISFIED BY A PASSING RUN RATHER THAN BY ARGUMENT.*** ***THE FIRST CONTROL RUN FAILED, AND THE FAULT WAS THE VERIFIER***: `CREATE.ACCOUNT` prompts for the **Windows** password, which is what sshd checks, while the API does SCRAM against a PBKDF2 verifier in `sdsys\$cred` that **only `MODIFY.PASSWORD` writes** — route granted, credential absent, with the account already in `sdapi`. `Create` now sets it; **SD confirmed the diagnosis in its own words**: *"Account SDDR2A has no password set. Setting the first one."* **The product half is PRE_RELEASE 42, open, the owner's call.** ***BOTH UNELEVATED LEGS WERE RUN BY THE AGENT***, its token measured first (`IsInRole(Administrator)` **False**). **`sddr1` and `sddr2` are spent — a prefix is single-use once its account has reached the Control leg.** `gplbld` and docs only, **no cycle**, `assert-current` **exit 0**.

***SEVENTY-FIRST SESSION, 28 Aug 2026 — PRE_RELEASE 10, 40 AND 41 ARE DONE. TWELVE ENTRIES CLOSED TODAY.*** All three are `gplbld` only, **no cycle**, and `assert-current` is **exit 0** after all of it. ***10 WAS NOT "TWO VERIFIERS" — IT WAS 23 FILES AND 24 OCCURRENCES, AND IT WAS STILL SPREADING***: three of the 23 were written the same day by copying `probe-catprivate.ps1`'s `Invoke-SD` *"unchanged"*. All converted to `([char]27 + …)`, and **guarded by a test rather than 23 comments** — `test-verdict-units.ps1` scans the whole directory, **tokenising rather than grepping**, because the first version failed on two files whose *comments* correctly quote the dead form. ***40 IS FIXED IN THE TWO RUNNERS, NOT IN FIFTEEN VERIFIERS***: they close what a step left open, **name the step that leaked**, and `VerifyInstall1` restores its own with `-Append` — one place, and it also covers the case a `try`/`finally` does not, a step that dies outright. ***41'S POSITIVE CONTROL FOUND A SAFETY BUG IN 41'S OWN FIX***: under a permissive pattern the new `C:\Users` scan returned **`All Users`, a junction to `C:\ProgramData`**, for which the code prints `Remove-Item -Recurse -Force`. **Reparse points are now excluded in both copies.**

***SEVENTY-FIRST SESSION, 28 Aug 2026 — PRE_RELEASE 19 IS MEASURED DOWN TO THE THREE DOORS, AND ITEM 5.5 IS DELIVERED.*** ***`verify-tierchange` 28 PASS / 0 FAIL, first run, `-Prefix sdtc1`*** — the required keyword (10111 and **nothing moved**), what leaves with ADMINISTRATOR (Windows `Administrators` **and** the `os.users` record, both asserted present first so their removal is a transition), and the "left alone" count. ***THE ARITHMETIC CONFIRMED ITSELF***: `D = 397` from **both** `A + added − removed` **and** `P + kept`, two independent routes to the same number, with no count typed anywhere. ***ONE ROW OF 19'S TABLE IS LEFT — THE THREE DOORS — AND IT IS PRE_RELEASE 38's, NOT SOMETHING THIS FILE CAN REACH.*** ***RULED BY THE OWNER, 28 Aug 2026: "19 stays B until the doors are covered."*** **Not to be struck, folded into 38, or downgraded** because the other six rows are measured — what closes it is coverage of `LOGIN:477`, `CPROC:3776` and `APISRVR:507`, not argument. **19 is a `B` and it led with three claims that are now false, two of which were false when written.** *"Not one line of `tier.set` has executed"* — `verify-tiers` section 6 ran, 33 PASS. *"The test cannot be piped"* — ***wrong when written***: a password prompt is answered by the next LINE of one string, which is §6's own fix, and `verify-tiers` had been creating accounts that way for weeks; `verify-acctmsgs` did it four times twice over on 28 Aug. *"There is no verifier"* — half true. ***WHAT IS ACTUALLY LEFT OF 19 IS THREE ROWS***, and `gplbld/verify-tierchange.ps1` (new, **item 5.5's owed measurement**) covers them: **the required keyword (10111), what leaves with ADMINISTRATOR (Windows `Administrators` + the `os.users` record), and the "left alone" count**. ***THE THREE DOORS ARE STILL NOT COVERED BY ANYTHING*** — they need an unelevated session, an ssh login and an API pair. That is PRE_RELEASE 38. **`sdtc1` is free.**

***SEVENTY-FIRST SESSION, 28 Aug 2026 — ALL EIGHT UNWITNESSED FIXES ARE MEASURED AND STRUCK: 5, 13, 14, 15, 22, 26, 27 AND 37.*** ***`verify-vocverbs` 36 PASS / 0 FAIL; `verify-acctmsgs` 31 PASS / 0 FAIL / 0 SKIP***, both on the 28 Aug 00:53:34 install, **no cycle spent**. ***NEITHER SCRIPT PASSED FIRST TIME AND NEITHER FIRST FAILURE WAS THE PRODUCT.*** `verify-vocverbs` stopped at 21 of 22 because **`LIST.INDEX` prompts when given no index name** and the prompt ate the `OFF`; `verify-acctmsgs` **SKIPped** entry 22's refusal arm because the password it guessed — 150 characters, on my stated grounds that 127 is a hard SAM limit — **was accepted**. Both are fixed and both were re-run. ***ENTRY 22's REFUSAL ARM NEEDED THE MACHINE'S PASSWORD POLICY CHANGED***, which was the owner's ruling and his to make: `net accounts /minpwlen:14`, run, `/minpwlen:0` to put it back — **and it is back, read after the run**. The password is now **chosen from the policy** rather than guessed. ***`sdmsga` AND `sdmsgb` ARE SPENT — use `sdmsgc`; `zzprf` is re-runnable as it stands.*** **Nothing was left behind by any run**, read from disk: `C:\Users` holds only `b48adm`, `dmont` and `Public`.

**SEVENTY-FIRST SESSION, 28 Aug 2026 — PRE_RELEASE 5, 13, 14, 15 AND 26 ARE MEASURED AND DONE.** ***`verify-vocverbs` 36 PASS / 0 FAIL / 0 SKIP*** on the 28 Aug 00:53:34 install, owner's elevated terminal. **Five of the eight unwitnessed fixes are struck; 22, 27 and 37 remain** and `verify-acctmsgs.ps1` has not been run. ***IT TOOK TWO RUNS, AND THE FIRST FAILURE WAS THE VERIFIER, NOT THE PRODUCT***: 21 of 22, failing on the entry 15 FIXTURE, because `LIST.INDEX <file>` with no index name **prompts** (`LISTI:117`), ate the `OFF` after it, and the session sat until the 60-second timeout — `CREATE.INDEX` had already printed *"Added index for F1"*. Fixed to `LIST.INDEX <file> ALL`, with three fixture instruments instead of one. ***THE CLASS IS WIDER THAN ONE VERB — anything driven down a pipe must NAME every optional argument***; `LISTI:117`, `DELETEI:101`, `DELETEF:117` and `DELACC:96` all prompt when theirs is omitted, and the tell is a transcript whose last line is a prompt and whose next command never appears. **No stray `sd.exe`** — checked after the timeout, only the normal `sdwind`.

**SEVENTY-FIRST SESSION, 28 Aug 2026 — THE EIGHT UNWITNESSED FIXES NOW HAVE TWO VERIFIERS.** `gplbld/verify-vocverbs.ps1` (entries **5, 13, 14, 15, 26**, no accounts) and `gplbld/verify-acctmsgs.ps1` (**22, 27, 37**, four throwaway accounts) — **both need an ELEVATED shell, so neither has been run**; the commands are in START HERE with full paths. `gplbld/test-vocverbs-units.ps1` is new, needs no install, and **passed 40 of 40** driving the first script's matchers against synthetic transcripts of a fixed build *and* of the defect. All three are on `assert-current`'s `$neverShipped`, and ***`assert-current` is exit 0 live after adding them*** — the 00:53:34 install is still the one that can test the fixes, and nothing under `gplsrc`/`sdsys` was touched so that it stays that way. ***THREE OF THE SEVENTIETH SESSION'S SUGGESTED TESTS ARE WRONG*** — 26's `force` form cannot fail, 22's `a` is accepted here (minimum password length is 0), 13's bare form stops at 3290. START HERE has all three.

**SEVENTIETH SESSION, 28 Aug 2026 — NINE PRE-RELEASE FIXES SHIPPED INTO AN INSTALL, ONE OF THEM MEASURED.** ***GREEN: install 28 Aug 00:53:34, `assert-current` exit 0, `verify-tiers` 33 PASS / 0 FAIL.*** Entries **5, 13, 14, 15, 22, 25, 26, 27, 37** are written, compiled and installed; ***only 25 is DONE***, because `verify-tiers` measured it (ADMINISTRATOR **416**, STANDARD and PROGRAMMER unmoved) and **nothing has exercised the other eight** — they need a session that runs `.d`, `qselect`, `delete.file`, `delete.index`, `modify.account add`, and a `create.account` with a bad password. **PRE_RELEASE 36 is RULED and not built; 41 is new** (the cleanup sweep reports zero while orphan directories remain). **Still open: 6 and 12**, both because their own entries were wrong about what they needed — 6 is an investigation, 12 is C at `op_dio3.c:853`. **`verify-tiers` gained section 6 (SUSPENDED) and `sdtier`/`sdtierb` are spent — use `sdtierc`.**

**Last updated:** 29 Aug 2026, **EIGHTY-SECOND session** — ***THE 81st SESSION'S LAST EDIT WAS LEFT HALF-APPLIED IN THE WORKING TREE, AND IT IS NOW FINISHED.*** ***NOTHING HAD DIVERGED FROM GitHub***: `main` and `origin/main` were both `c6165b6`, zero ahead and zero behind. **The inconsistency was uncommitted, not unpushed** — `PRE_RELEASE_FIXES.md` sat modified with the 81st session's closures of **56**, **57** and **58** and its new entry **62**, cut off mid-edit in two places: ***row 56 was never struck while its own section said DONE***, and ***NEXT FREE ID still read 62, the id already used***. `test-fixlist-units.ps1` named both (**201 / 2**, exit 1) — the guard working exactly as rule 4 and rule 5 were written for. **Both fixed; it is 203 / 0, exit 0, and the open count is 18, not 20.** ***THREE BLOCKERS LEFT, NOT FIVE.*** ***AND ENTRY 2 NEEDS RE-READING BEFORE IT IS WORKED***: it was re-opened as downstream of 56 and its stated premise — *"56 abolishes the administrator account this attached to"* — died with clause 2's reversal, so it is open on a reason that no longer holds. **No cycle spent. Nothing under `gplsrc` touched, and nothing under `sdsys` until 63 — which changed twelve `voc_template` records and is why `assert-current` is red.** **Earlier the same day, the EIGHTY-FIRST session:** ***ENDED OUT OF CREDITS, GREEN, EVERYTHING COMMITTED AND PUSHED — TRUE OF THE COMMIT AND NOT OF THE WORKING TREE, WHICH IS THE GAP THE 82nd CLOSED.*** Install **18:55:20**, `sd.exe` **`4732ECF659E8DB40`**, `assert-current` **exit 0 live**, `check-stale-leads` **exit 0**, `test-fixlist-units` **203/0**, **open count 20**. ***THE ONE THING OWED IS A SUITE RUN — `b67`, AND EXPECT 14 OF 14 UNELEVATED, NOT 13***, because `verify-txn.ps1` joined that list. **The session did, in order:** step 1's measurement (the elevation discriminator already existed — **no new kernel key**), step 2 (56 clause 2 and 57's promotion report, built and cycled), `b65` 12/13 with `verify-batchjob` diagnosed as the verifier rather than the product, the re-aim of that row at SDSYS on the owner's ruling, ***`b66` GREEN IN BOTH HALVES — 13/13 and 19/19 — CLOSING PRE_RELEASE 59***, the `SDCoreWindowsDocs` rename propagated (**two of the eight references were warnings that had INVERTED**), ***PRE_RELEASE 11 — THE SILENT TRANSACTION DATA LOSS — FIXED with a standing verifier***, and **PRE_RELEASE 39 built with its `-Remove` path deliberately UNRUN**. ***THEN 61 AND 62 WERE MEASURED, AND 61 CLOSED AS NOT A DEFECT WITH ITS PREMISE INVERTED.*** ***`listf` IN SDSYS SHOWS `$MAP` AS `DH`, NOT `Err 30`*** — and the three files involved do three different jobs, which the entry had compared as if they did one: **`voc_template` field 1 is a TYPE CODE** and becomes SDSYS's VOC (`stage.py:119`, and the live bytes at `sdsys/voc/%0` offset 11280); **`newvoc` field 1 is a DESCRIPTION whose FIRST CHARACTER IS THE TYPE CODE** — `CREATEA:1233` replaces the field with its own first character (`rec<1> = if upcase(rec[1,1]) = 'P' then rec<1>[1,2] else rec[1,1]`, two for a `P` type; again at `:1292`), so the description does not survive into an account's VOC but ***its first letter is load-bearing***, and 392 of 392 agree with `voc_template`'s type code; and ***`listf`'s Description column is a LOOKUP into `newvoc`***, `voc.dic` holding `IF @ = '' THEN F1 ELSE @`. ***THE CONTROL IS WHAT SETTLED IT***: neither `File for MAP output` nor `File - Vocabulary` appears anywhere in SDSYS's VOC file while `listf` displayed both, so the column cannot be reading the record — **and an earlier explanation of mine, that it worked because SD dispatches on `voc.entry.type[1,1]`, named the wrong CALLER — it is `CREATEA:1233` deriving the account's type code from field 1's first character, not `CPROC`'s dispatch — but ***the first character IS load-bearing and that half stands.*** A second pass then over-corrected it to "the field is simply dropped, so the check measured the wrong property", and **that was wrong too**: the 392-of-392 check was measuring exactly the right invariant.** ***THE UPSTREAM REPORT CARRIED THE SAME FALSE CLAIM AND WAS `PROPOSED` — ONE STEP FROM BEING SENT***; withdrawn in UPSTREAM_FIXES.md with the method failure kept, because *"the same record shipped twice, one copy right"* is what a directory-wide convention looks like when one record is examined. **62 is traced and stays open**: both routes into SDSYS now test the person before anything prompts (`LOGIN:568` needs an already-elevated session AND an administrator; `CPROC:2634` refuses 10002 **before** `elevate('START')`, and `keys.h:201`'s `K_OS_ADMINISTRATOR` cannot be forged or moved by a `LOGTO`) — ***but `10002`, `not an administrator` and `LOGTO REFUSED` get ZERO hits across every `verify-*.ps1`, so it is asserted by reading and by nothing else.*** ***THEN 2 WAS RULED, BUILT, CYCLED AND VERIFIED ON `-Run b69` — AND IT FILED TWO ENTRIES OF ITS OWN.*** Install **22:04:34**, `assert-current` **exit 0 live**: `os.users\don` reads **`yes|yes`** and `verify-osusers` took the ***"already listed"*** branch where `b68` had nothing to park, **all twenty rows passing**. ***BUT `b69` IS NOT GREEN***: `verify-apiadmin` **21/23**, and the failing row is *"control: local elevated session refused OS.EXECUTE"* — **expected refused, observed it RAN**. ***THAT IS THE `LOGTO` LEAK THE OWNER ACCEPTED, MEASURED ON THE FIRST RUN AFTER THE RULING, AND IT IS THE PRODUCT RATHER THAN THE TEST*** — filed as **64**, with the instruction **not** to simply flip the expected value. **65** is the second consequence: `os.users` now accumulates an orphaned record per ADMINISTRATOR-tier throwaway account, three left by `b69` with their Windows accounts **gone**, checked. ***TWO BLOCKERS LEFT: 39 AND 64.*** *(As written before that run: "TWO BLOCKERS LEFT: 2 AND 39" — 62 closed on `-Run b68`, `verify-sdsysgate` 10 decisive of 10, refused by identity with both disqualifiers absent.)* *(As written before that run: "THREE BLOCKERS LEFT: 2, 39 AND 62")* — and **2 is a `B` that had been left out of the blockers table.** **New: 63, `M`** — ten of SDSYS's sixteen files print a bare `F` where a description belongs, the `voc.dic` fallback meeting files that have no `newvoc` record. ***63 IS BUILT, CYCLED AND VERIFIED ON THE OWNER'S "do them all" — CLOSED, AND `b67` IS GREEN IN BOTH HALVES ON THE SAME INSTALL***: twelve `voc_template` records changed — the ten given `File - …` descriptions, plus `edit` and `micro` reduced to a bare `V` as the last two of the five §8 called malformed. ***A COMMENT ON A VERB RECORD IS INVISIBLE AND ON A FILE RECORD IS THE FIX***, which is why the two halves look opposite. ***AND `CPROC:1410` MAKES THE FORM LEGITIMATE*** — a type code may be followed by comment text — which HISTORY's *"the five malformed VOC_TEMPLATE entries were never broken"* established on 18 Aug, **after an upstream entry about those five had also been written and withdrawn**. ***THREE MISREADINGS, TWO WITHDRAWN UPSTREAM REPORTS, ONE CAUSE.*** ***VERIFIED ON THE 20:31:49 INSTALL, `assert-current` EXIT 0 LIVE***: an elevated `listf` shows all sixteen files described, **zero bare type codes left**, and `$MAP` still `DH` — the control. **`-Run b67`: `VerifyInstall1` every step exit 0, `VerifyInstall2` 19 of 19, 655 `[PASS]`, zero `[FAIL]` across 21 transcripts. `b54`–`b67` spent; use `b68`.** ***AND THE TRANSCRIPTS ARE UTF-16***, so a plain `grep -a '[PASS]'` over them matches nothing and reports a clean-looking `PASS=0 FAIL=0` — **strip NULs first and check the PASS count is non-zero before believing the FAIL count.** **Open count 18 → 17.** *(As written earlier the same session: "THREE BLOCKERS LEFT — 56, 57 AND 58 CLOSED THE SAME DAY: 39 wants task 7.2's guest; 61 wants one measurement before the `F` goes in; 62 wants the `elevate('START')` re-measurement that 56 left behind.")* *(As written by the 81st session, before those three closed: "FIVE BLOCKERS LEFT: 39 wants task 7.2's guest; 61 wants one measurement before the `F` goes in; 56's remainder is the `elevate('START')` identity hole; 57's promotion report is unexercised; 2 and 58 are downstream of 56.")* *(Earlier the same session: ***PRE_RELEASE 11 IS FIXED: THE SILENT TRANSACTION DATA LOSS IS GONE.***)* A nested `commit` abandoned the outer transaction and its writes vanished with no error, no warning and nothing in the log. `end_txn_level()` is lifted out of `rollback()` and called from `op_txncmt()` too — **one function, two callers, because the defect was that this bookkeeping had one place and one caller** — placed **before** `exit_op_txncmt:` so the three `k_error()` paths do not pop a level they did not commit. ***MEASURED, install 18:36:04, `sd.exe` `4732ECF659E8DB40`***: new `gplbld/verify-txn.ps1` **9 of 9** — the outer write reads `outer` where it read `base`, `SYSTEM(1008)` delta `0` where it was `+2`, the parent reinstated where the session had been left in no transaction. **Wired into `VerifyInstall1` AFTER being measured; the unelevated half is 14 steps now — expect 14 of 14 on `b67`.** ***ONE ROW FAILED FIRST TIME AND THE PRODUCT WAS RIGHT*** — the baseline is taken outside the outer transaction, so the inner depth is 2 above, not 1; the instrument was corrected, not `txn.c`. ***ONE THING FILED RATHER THAN FIXED***: on the commit-failure paths `process.txn_id` is already zeroed, so nothing rolls back and the level stays counted — pre-existing, not widened, and it needs a ruling about the records already written. **UPSTREAM 17 updated with the shape.** *(Earlier the same session: ***GREEN IN BOTH HALVES FOR THE FIRST TIME, AND PRE_RELEASE 59 IS CLOSED.***)* `-Run b66`: **unelevated 13 of 13, elevated 19 of 19, 1,106 `[PASS]`, zero `[FAIL]`, zero table rows scoring FAIL.** ***THE RE-AIMED `verify-batchjob` ROW MEASURED RATHER THAN MERELY PASSING*** — `ELEVATED in SDSYS, no entry: still runs` **decisive**, with **neither** `SDSYS-ENTRY-PRESENT` **nor** `SDSYS-PLANT-FAILED` anywhere in the transcript; both of those also give exit 0 while measuring nothing, so **read the row and the markers, not the exit code**. ***SDSYS CHECKED CLEAN WITH A CONTROL***: no `ZZBATCHS` in `bp`/`bp.out`, `batch.jobs` empty, `zzbatch` 0 hits in the VOC buckets against a control finding `listf` 6 / `count` 18 / `who` 15 — **the first attempt at that check found the probe absent AND the control absent, so it was measuring nothing**; `grep -a -F` is what reads a dynamic file's buckets. **59 closed: two verifiers converted, TWO NEEDED NO CHANGE AT ALL** (`lcnames` back to 142 of 142, `osusers` 44/0 — both recovered the moment clause 2 was reversed), **and `batchjob` re-aimed on the owner's ruling. Open count 22 → 21. b54–b66 spent; use `b67`.** *(Earlier the same session: ***STEP 2 BUILT, CYCLED AND INSTALLED.***)* Full cycle **15:33:45**, `assert-current` **exit 0 live**, 184 programs at **0 errors** and **0 of the fatal *"is not assigned a value"* class**. Three changes, one cycle: **`LOGIN:414`** loses the administrator exemption so the `sdusers` gate is uniform across all three tiers (`-INTERNAL` still exempt — the bootstrap and the `adopt` recovery); **`LOGIN:568`** becomes `case kernel(K$ADMINISTRATOR, -1) and kernel(K$OS.ADMINISTRATOR, 0)`, so an unelevated administrator falls through to `case 1` and lands in their **own account**; and **`MODIFYA`** gains 57's promotion report (`promo.snapshot`/`promo.report`, messages **10128**/**10129**). ***DO NOT REDUCE THE CASE TO ONE KEY*** — the first is the `kernel.c:240` seed and is the mechanism, the second is belt to its braces, and `K$OS.ADMINISTRATOR` alone is TRUE for the very case that must not reach SDSYS. ***ADMINISTRATORS KEEP ssh***, which the withdrawn model had taken. ***THE PROMOTION REPORT IS MEASURED ACROSS THE REGISTER WRITE*** rather than computed from ranks, so a demotion prints nothing, an already-refused membership is not claimed, and an unreadable group says so instead of reporting a comfortable zero. ***A LOCKOUT WAS TRACED FOR AND IS NOT THERE***: `AdoptAccount` runs unconditionally in `sd.iss` and `adopt-account.ps1` enters through `sd -internal`, which stays exempt — so a failed adopt is a setback, not a lockout; its wizard text no longer names a specific refusal, because which one you get now depends on how far adopt got. ***PREDICTION TO SCORE `b64` AGAINST: PRE_RELEASE 59's THREE UNCONVERTED VERIFIERS SHOULD RECOVER*** — `lcnames`, `osusers`, `batchjob` all assumed an administrator lands in an ordinary account, which is true again; **if they do not, that is the finding.** ***`sd` WAS DELIBERATELY NOT DRIVEN BY HAND*** — CLAUDE.md's opening trap, and the canonical `Invoke-SD` prefixes `LOGTO SDSYS`, which would hide the answer. **Verified by reading the install, not the run**: `gpl.bp.out` 186 / `gcat` 127 unchanged, objects recompiled 15:33:14, the two messages installed at 424 and 308 bytes, mirrored count 2982 → 2984. **Earlier the same session:** ***STEP 1 IS MEASURED, AND 56 CLAUSE 2 NEEDS NO NEW KERNEL KEY.*** ***THE CAUTION WAS RIGHT: `IsAdmin()` IS TRUE FOR AN UNELEVATED ADMINISTRATOR***, so `K$OS.ADMINISTRATOR` cannot carry clause 2's `:513` branch alone — but `IsElevated()` is **FALSE** there and **SD already exposes it**: `K$ADMINISTRATOR` is seeded from it at `kernel.c:240` and **still holds that seed at `LOGIN`'s `begin case` (`:420`)**, which is where the branch decides. **Established by exhaustive grep rather than assumed** — three live writers of the flag exist, `LOGIN:615` and `CPROC:2769`/`:2781`, and both `CPROC` sites are in the `LOGTO` path, which cannot run before `LOGIN`. ***DO NOT WRITE THE OBVIOUS BASIC PROBE — IT READS 1 IN BOTH LEGS AND WOULD REPORT THE OPPOSITE***, because `LOGIN:615` sets the flag for everyone who reached SDSYS, which today is every administrator. The instrument is `gplbld/probe-osadmin.ps1` (+`.c`), an **instrument and not a verifier**, on `$neverShipped` in the commit that creates it; **run it unelevated AND elevated — the pair is the measurement**, and it refuses out loud if run by a non-administrator, whose `IsAdmin() = FALSE` is word for word the answer step 1 hoped to see. Its own first run **refused a good measurement** by anchoring on a string it prints twice; re-anchored on the single `ANSWER:` line. **No cycle spent, no product code touched.** ***NEXT IS STEP 2: `LOGIN`'s `:398` EXEMPTION REMOVAL AND `:513` BRANCH, WITH 57's PROMOTION REPORT — ONE CYCLE, BOTH TOUCH `MODIFYA`/`LOGIN`.*** **Earlier the same day, the EIGHTIETH session:** ***56 CLAUSE 2 IS REVERSED: THE ADMINISTRATOR'S PERSONAL ACCOUNT COMES BACK, AND THE QUEUED `adopt-account` REMOVAL IS CANCELLED.*** Owner: *"that is precisely why administrators also had a personal account. They got SDSYS in one of two ways, by starting SD in an elevated session or by logging to SD after logging into their personal account."* **The property already holds for standard and programmer** — `LOGIN:399`'s `sdusers` test refuses an outside-SD account with 5009 — **and 56's own `:398` comment says the administrator exemption was forced by clause 2.** ***DO NOT DO THE 20-FILE ADOPT REMOVAL***; adopt is how the installer gets that account, and nothing had been removed because it was deliberately kept separate. **`LOGIN:398`'s exemption goes and `:513` must stop sending every `K$OS.ADMINISTRATOR` to SDSYS.** ***AND "is THIS SESSION elevated" HAS NO KEY YET*** — `K_ADMINISTRATOR` is a settable flag, `K_OS_ADMINISTRATOR` asks about the person; **measure `IsAdmin()` unelevated before designing.** **Three tiers stand; 57 stands. Nothing built — three rulings arrived and none cost a wasted change, because the earlier parts stopped at tracing.** ***ENDED OUT OF CREDITS, GREEN, EVERYTHING COMMITTED AND PUSHED.*** `assert-current` **exit 0**, units **51/0**, `test-fixlist-units` **202/0**, open count **22**, **no cycle spent all session**. ***THE NEXT SESSION'S FIRST STEP IS THE `IsAdmin()` MEASUREMENT IN THE BOX BELOW — everything after it is designed and nothing after it is built.*** *(`generate_gap_analysis_pdf.py` in the repo root is deliberately UNTRACKED — another AI is editing the documentation; leave it alone and never `git add -A` here.)* *(Earlier the same session: ***THREE TIERS; "TWO TIERS" GIVEN AND WITHDRAWN THE SAME HOUR.*** Owner: *"we need three tiers because we create accounts in SD not in windows except for the installer … one I had forgotten about."* The trace that produced the reversal is kept: `CREATE.ACCOUNT … ADMINISTRATOR` makes a Windows administrator (`CREATEA:813`), which is **the direction the design wants** — SD is the authority for who administers SD. ***AND IT LEFT A PROPERTY THE CODE DOES NOT HAVE***: *"an Administrator created outside SD has no access until a matching SD administrator account exists"* — `LOGIN:513` sends any `K$OS.ADMINISTRATOR` to SDSYS and `LOGIN:398` skips the `sdusers` gate, so at the console they are in with no SD account. **Owner's call, and a change to 56.** **57 stands.**)* *(Earlier the same session: ***TWO RULINGS TAKEN AND TRACED: "Two tiers" — since withdrawn — and 57.*** ***THE TRACE FOUND THAT `CREATE.ACCOUNT … ADMINISTRATOR` MAKES THE USER A WINDOWS ADMINISTRATOR*** — `CREATEA:813` → `os_group("ADDMEM", "S-1-5-32-544", …)` — which under 56 yields an administrator elevated into SDSYS who **never enters the account just made for them**. **Footprint: 15 tier literals in 4 files; the 57 `K$ADMINISTRATOR`/`K$OS.ADMINISTRATOR` uses are a different thing and stay.** **Stop offering the tier, keep recognising it** — `accounts\don` holds `ADMINISTRATOR` today and the data tree is never upgraded. **Both changes touch `MODIFYA`: one cycle.**)* *(Earlier the same session: ***PRE_RELEASE 60 CLOSED AND VERIFIED, AND A NEW PRODUCT DEFECT FILED AS 61, `B`.*** `sdsys/newvoc/$MAP` has **no type code**: field 1 is the description where every other file record has `F`, **including our own `voc_template/$MAP`** — the same record shipped twice, one copy right. Once the four dead records went, `$MAP` was **the only `Err 30` left**. ***UPSTREAM HAS THE IDENTICAL SPLIT***, so it is filed in UPSTREAM_FIXES.md too. **Filed, not fixed** — settle which file feeds SDSYS's VOC first.)* *(Earlier the same session: ***BOTH OWNER RULINGS BUILT: "1. sweep  2. delete dead voc".*** The sweep removes stray `sdtu*` accounts inside the elevated child Create already raises (**no extra prompt**), with the candidate list built **in the elevated process and never passed in** — three conditions, all printed. `verify-catgate` now deletes `<ACCT>BP.OUT` through SD, and **`gplbld/clean-deadvoc.ps1` (NEW, elevated) clears the four already there** — `b59`, `b60`, `b61`, `b63`, one per run as predicted. It is on `$neverShipped` **in the commit that creates it**, and `assert-current` is exit 0 live with it listed.)* *(Earlier the same session: ***TWO OF PRE_RELEASE 59's FOUR VERIFIERS ARE CONVERTED AND GREEN. UNELEVATED 10 OF 13, ELEVATED 19 OF 19 (`b63`).*** `verify-nocase` 3 of 3 and `verify-lineendings` 17 of 17, both as a real non-administrator over ssh — including lineendings' **straddle** (CRLF on the 2048-byte buffer boundary, `2047`) and its **lone-CR control** (a CR surviving as data). ***THE CLASSIFICATION IN 59 WAS WRONG AND IS CORRECTED: only two of the four were mechanical.*** `verify-lcnames` needs its **53 call sites classified** account-side vs SDSYS-side (four are `LOGTO SDSYS`, and they work only because the administrator lands in SDSYS — the same fact that breaks the other 49); `verify-batchjob`'s elevated leg `Push-Location`s into the account and under 56 does not get a session there, **so check it before converting**. ***AND A Ctrl-C DOES NOT RUN THE `finally` — MEASURED ON `b62`***, which stranded `sdtub62` and burned the token; `VerifyInstall1` now names any orphan and its remove command before creating anything, reporting rather than acting. ***`b63` IS SPENT — USE `b64`, AND SPEND IT ON A RUN THAT CARRIES A CONVERSION.***)* *(Earlier the same session: ***`verify-nocase` GREEN ON `b61`, 3 OF 3.*** Unelevated **9 of 13**, elevated **19 of 19**, doors 5 of 5. PRE_RELEASE 59's whole apparatus is witnessed — elevated create, the ACE for the unelevated parent, ssh as the account, PROGRAMMER tier, elevated remove. ***SO THE "ONE FIRST" CAUTION IS PAID OFF AND `verify-lineendings.ps1` IS CONVERTED TOO*** (unrun); `lcnames`, `batchjob` and `osusers` are left. **The refusal tests are a table cross-checked against `VerifyInstall1`'s own `$needsTestUser`, read out of its source** — a verifier converted but unlisted is untested, one listed but unwired is skipped, both silent. **Units 51 / 0.** ***FILED FROM THE LOG: PRE_RELEASE 60***, `verify-catgate` leaving one dead VOC record in SDSYS per run, its `Remove-Item` doing the thing the comment above it forbids.)* *(Earlier the same session: ***`b60`: ELEVATED 19 OF 19, THE MACHINERY WITNESSED, THE TIER WRONG AND FIXED.*** Create `before=False after=True` on both halves, the ACE landed, and **the unelevated parent's own write succeeded** — the only token that could answer; Remove clean; `verify-doors-suite` 5 of 5 in the same run. ***THE TIER WAS WRONG AND SD SAID SO***: ssh exit 0 into the account, then *"BASIC is not in your VOC"* — `TIER.OMIT.STANDARD` withholds `basic` and `run`, and all four verifiers compile a probe. **PROGRAMMER now, still a non-administrator.** ***THE UNIT TEST ROW WAS ITSELF THE BUG***, encoding STANDARD as a rule it would have defended. **Two `%TEMP%` leaks found by looking rather than by failing** — the denied fixture (`icacls /remove:d` did nothing and its output was silenced) and `Invoke-SdAsTestUser`'s work directory. **Units 45 / 0.**)* *(Earlier the same session: ***THE WIRING, TWO BLOCKERS, AND THE PIPED-STDIN FIX.*** SD answered `:Process terminated` — **sysmsg 5020, `CPROC:473`, the `K$LOGOUT` arm: a forced logout, not a refusal** — and `sdtestuser-admin`'s artefact check refused rather than reading the banner as success. ***THE CAUSE WAS ON DISK, DATED 14 Aug 2026***: `Start-Process -RedirectStandardInput` hands sd.exe a file handle and SD exits; it now pipes inside a `Start-Job` with `LOGTO SDSYS` and a timeout. **`RedirectStandardInput` was never grepped for, which is CLAUDE.md's standing rule, and a run paid for it.** **Units 41 / 0**, guard tokenised with the module as its control. That run created nothing, so `b60` was reused for the full run above.)* *(Earlier the same session: ***THE WIRING, AND TWO BLOCKERS FOUND ON THE WAY.*** `VerifyInstall1` makes and removes the throwaway non-administrator account, `verify-nocase.ps1` is converted, `test-sdtestuser-units.ps1` **34 / 0**. ***THE FIRST BLOCKER MEANT THE SUITE COULD NOT HAVE RUN AT ALL***: session 79's three new scripts were never listed on `assert-current`'s `$neverShipped`, so it exited **1** naming them and every verifier that calls it refuses — **measured by running it, exit 0 live afterwards.** ***THE SECOND IS THAT AN ACCOUNT DIRECTORY IS NOT REACHABLE BY THE UNELEVATED PARENT*** (SYSTEM, Administrators and its own `sdu_` group only), while all four verifiers plant probes through the file system; `Create` now adds one ACE, and a **group would not have worked** — PRE_RELEASE 44. **A third was introduced and caught: `Set-StrictMode` at file scope leaks through a dot-source into the caller.** **No cycle spent, nothing under `gplsrc` or `sdsys` touched, `assert-current` exit 0.)* ***READ THE BOX — ITEM 0 HAS THE `b60` RESULT AND ITEM 1 THE TWO COMMANDS.*** *(Previously: 29 Aug 2026, **SEVENTY-NINTH session** — ***BUILT, CYCLED AND MEASURED.*** Started on PRE_RELEASE **31**, one of the three open **B** entries; its trace moved the owner to rewrite the whole administrator access model (**56**), then to add a tier ordering on grants (**57**). Both are built and compiled; **cycle 29 Aug 10:35:46, `-Run b59`: ELEVATED 19 of 19, 397 PASS / 0 FAIL / 0 SKIP — green for the first time — and PRE_RELEASE 31 CLOSED**, with no edit to its verifier. **UNELEVATED 8 of 13**, all five failures one cause, filed as **59**, whose foundation is built and unit-tested (21/21) with the wiring left. **Open count 17 → 21** from `gplbld/test-fixlist-units.ps1` (200 passed, 0 failed) — it rose by **filing**, not by breaking. **Ended short on credits, green, everything committed and pushed.)* *(Previously: 29 Aug 2026, **SEVENTY-EIGHTH session** — the 21 silent headings done and the checker's NOTE gone; open count 17, 184 passed / 0 failed.)* *(Previously: 29 Aug 2026, **SEVENTY-SEVENTH session** — six decisions recorded and **none started**, at the owner's instruction.)* **Ended out of credits, green, everything committed and pushed.** ***THE CYCLE FROM SESSION 75 IS STILL OWED — `assert-current` exits 1 until it runs, and that is the first thing in the box below.*** *(Previously: 28 Aug 2026, **SEVENTY-THIRD session** — install **28 Aug 15:29:59**, `assert-current` **exit 0**, the suite's twelve unelevated steps all exit 0 and **the thirteenth (the door step) failed**; two faults found, one fixed, one re-opening PRE_RELEASE 19.)* ***READ THE BOX AT "NEXT SESSION: START HERE" FIRST.*** *(Previously: 28 Aug 2026, **SEVENTY-FIRST session**, which ended **out of credit mid-task, green and pushed at `67cf316`**.)* ***READ THE BOX AT "NEXT SESSION: START HERE" FIRST AND PRINT THE TWO COMMANDS IT OPENS WITH — the owner is waiting for them.*** Thirteen pre-release entries closed; **no cycle was spent all session**, so the 28 Aug 00:53:34 install is still the one that can test things. Everything below this line is the **SIXTY-NINTH session** and earlier.

**Previously:** 27 Aug 2026, **SIXTY-NINTH session**, which ended on credit with **both repositories pushed and clean, the install green and current, and nothing half-done.** ***GREEN: install 27 Aug 22:52:21, `assert-current` exit 0, `-Run b49` 30 of 31 steps, 963 `PASS` / 1 `[FAIL]` / 0 `[SKIP]`*** — the one failure is PRE_RELEASE 31's known stale control. **`b49` is spent; use `b50`.** ***CLOSED THIS SESSION: PRE_RELEASE 23, 32, 33, the shipped-scripts documentation gap, item 5.1 and item 5.2's ssh door.*** ***OPEN AND ALL YOURS: seven pre-release entries — 31, 34, 36 (**RULED 27 Aug, not built — the entry says what to implement**), 37, 38, 39, 40 — plus three measurements that need no ruling: 5.2's API door, 5.4's unrun probe, and 5.5.*** Everything below is the **SIXTY-EIGHTH session** and earlier.

***THE DEVELOPMENT PHASE IS CLOSED AND THE STATED 1.0-0 GATE IS EMPTY.*** 7.18 and H.5 both closed on 26 Aug 2026. **`H.2` — documentation — is the only open row in the table, section 7 has nothing left in it, and nothing is broken or half-done.**

***THIS FILE WAS PRUNED ON 26 Aug 2026 FOR THE DOCUMENTATION PHASE, AND ROUGHLY HALVED.*** Two sections had grown past the point where a cold session could read them, and together they were about half of it: **section 7, in which every step is closed**, and **"START HERE — IT IS SHORT"**, which twelve sessions had each added a handoff to the top of without removing the one below. Both are compressed to their conclusions under §0 rule 5; the record moved **verbatim** to HISTORY.md as two `ARCHIVE 26 Aug 2026` entries, which carry the measurements, and **nothing was deleted**. §"DOCUMENTATION DECISIONS" and §"THESE FOUR ARE THE BRIEF" were deliberately left untouched — they are the live brief for H.2.

***IT IS STILL OVER §0 RULE 5's ~3,500 LINE CEILING, AND CLOSING THAT GAP IS A DECISION, NOT AN EDIT.*** What is left is §6 traps — which rule 4 says never to cut for size and which is now the largest section — and §5's decisions, which are the *why* that does not survive in a diff. **Do not quietly cut either to make a number.** Raised for the owner 26 Aug 2026; until he rules, the ceiling stands as written and the two protected sections stand as written.

***READ THE TASK TABLE BELOW BEFORE ANSWERING "WHAT IS LEFT", AND RUN THE CHECKER FIRST.*** `python sdb_ai/sd64/gplbld/check-stale-leads.py` — one second, exit 0 today, and it is the difference between the table and a guess. It exists because the owner was given a different list three times in one session, and he was right: **four entries led with a status they had themselves withdrawn**, step 14 saying *"WHAT IS STILL A DECISION"* **338 lines above** *"STEP 14 IS CLOSED"*.

***H.2 — THE `User` SET IS 18 PAGES AND `Technical` HAS STARTED (26 Aug 2026). THE TESTER SET IS 15 PAGES AND THE OWNER HAS ANSWERED THE REVIEW LIST. SIXTEEN OF THE EIGHTEEN QUESTIONS ARE APPLIED; TWO ARE OPEN AND ARE AT THE TOP OF `QUESTIONS-2026-08-26.md`*** — **q7**, the `limitssh` default (re-asked with four options; he said the proposal was not clear) and **q14**, whether the unmeasured ssh-elevation caveat is stated to testers. ***THE DOCUMENTATION AND ITS TOOLCHAIN NO LONGER LIVE HERE***: repository `SDCoreWindowsDocs`, working tree `C:\Users\dmont\Projects\SDCoreWindowsDocs`, branch `main`, pushed. `mkdoc.py` and `mkpdf.ps1` are **gone from `gplbld` and off `$neverShipped`** (q15).

***TWO FULL-SCREEN EDITORS ARE BACK, `edit` AND `micro`, AND BOTH ARE UNCOMPILED SOURCE UNTIL SOMEBODY RUNS A CYCLE.*** Owner, 26 Aug 2026, reversing the 17 Aug removal of `MICRO`. **One program, two VOC entries**: `sdsys/gpl.bp/EDIT` is the old `MICRO` ported with its three defects fixed (§UPSTREAM_FIXES #16), and it reads field 1 of the command line to choose between `edit.exe` and `micro.exe`. `newvoc/edit` and `newvoc/micro` (and both `voc_template` records) are `CA $EDIT`; the old `MICRO` source is deleted. **`edit` was already in `TIER.OMIT.STANDARD`; `micro` was added to it**, so the list is **42** and a standard account's count does not move — it is on both sides of the arithmetic. `gplbld/install-editors.ps1` is new and shipped, `sd.iss` runs it unconditionally, and it **refuses to fall back to a per-user winget install**. ***THERE ARE TWO GATES, NOT ONE*** (owner, 26 Aug 2026): the VOC tier decides who has the verb, and **`os.users` field 2 - the `OS.EXECUTE` field - decides whether it runs**. `check.permitted` in `EDIT` tests it rather than leaving it to `os_permitted()`, which would never see it: the program is `$internal`, so `op_sh.c:157` admits it on `HDR_INTERNAL`. It also refuses a session with **no terminal** - an API session or a piped script. **The editors should work over ssh**: `connection_type` is `CN_CONSOLE` for an ssh session (`kernel.h:55` is the default and only `-P`, `-C` and `-N` change it), so `op_sh.c:348` does not pipe the child and the editor gets the terminal. **Not measured.** ***GREEN AND CURRENT AS OF 26 Aug 2026 17:14. THIS IS THE STATE TO START FROM.*** Cycle complete, install **17:14:03**, `sd.exe` **`8E6A6CF45AA6F20A`** (moved from `5BD2F83F43BB9B27` - the first C change since 25 Aug: `win32vt.c` and the `sdtermlb.c` reorder). `assert-current` **exit 0**. Suite **`-Run b46`: 31 of 31 steps exited 0 - 12 unelevated + 19 elevated, 991 `PASS`, 0 `[FAIL]`, 0 `[SKIP]`** - ***`b46` IS SPENT, USE `b47`***. *(This line read "19 of 19" until 26 Aug 2026: that is the elevated half's own summary, quoted alone. Corrected from the transcripts, with the counts remeasured - §6, "the PASS count was grepped out of files nothing could read".)* **Verified in the install by reading it, not by trusting the run**: `gcat/$EDIT`, `newvoc/micro` -> `$EDIT`, `TIER.OMIT.STANDARD` 42, `voc_template/$licence` 44,529 bytes, `$contrib` 627, the micro syntax file and `install-editors.ps1` both shipped, and no Black Oak in the licence. ***AND `config gpl` / `config contrib` RUN END TO END***: 915 lines back through `Invoke-SD`'s harness, the whole GPL present, no Black Oak - so the 44 KB VOC record, the one part of that design nobody had exercised, works. ***WHAT IS NOT DONE: `edit` and `micro` HAVE NOT BEEN RETRIED SINCE THE VT CHANGE***, so ANSI positioning from a PowerShell window is built and installed but unwitnessed. ***THE SHIPPED-SCRIPTS GAP IS CLOSED (27 Aug 2026, sixty-ninth session)*** — `Technical/02` covers all of them and tester page 01 now prints the `install-ssh.ps1` retry command it used only to promise. **It is 26 scripts, not the 25 recorded here**: measured by listing `C:\Program Files\SD` rather than reasoning from `$neverShipped`, and `micro-home.ps1` shipped the same day with PRE_RELEASE 29. **Two things are still open and neither is started**: **bundling micro with the installer** (decided 26 Aug, licence question settled, nothing built); and questions **7** and **14** in `QUESTIONS-2026-08-26.md`. 

***THE EDITORS RUN. `edit` AND `micro` BOTH TESTED ON THE INSTALL OF 26 Aug 2026 AND BOTH WORK*** (owner). The fault that stopped them first time was a **POSIX path handed to a Windows program**: `fileinfo(FL$PATH)` answers `/cygdrive/c/...` - measured with `ANALYSE.FILE`, and **`sd.conf`'s `C:\ProgramData\...` makes it look otherwise, which is why it was measured**. `kernel(K$WINPATH)` converts it, and an empty answer is refused rather than passed on. ***IT WAS NOT AN ERROR AT EITHER END***: Windows read the path as drive-relative, so micro said *"parent dirs don't exist"* and Microsoft Edit said nothing at all. ***STILL UNCOMPILED AFTER THAT CYCLE***: a blank line before each of the four prompts. ***IT COMPILES. MEASURED, NOT REPORTED*** — `cycle.ps1 -SkipInstall`, 26 Aug 2026 14:13, and the staged tree at `C:\Users\dmont\stagetest` was read rather than the run's output believed: `ProgramData\sdsys\gcat\$EDIT` and `gpl.bp.out\EDIT` both exist, `newvoc/edit` and `newvoc/micro` both read `CA $EDIT`, `TIER.OMIT.STANDARD` holds 42, `ProgramFiles\install-editors.ps1` is there and the old `gpl.bp/MICRO` is gone. **`gcat` is still 125 and `gpl.bp.out` still 184** — `$MICRO` left as `$EDIT` arrived. ***IT HAS STILL NEVER RUN***: `-SkipInstall` stops before installing, so `C:\ProgramData\SD` is untouched and no session has typed `edit`. **A full `cycle.ps1` is what tests it**, and the mark-token conversion added afterwards has not been compiled at all. ***THE MARK GRAMMAR IS `~` PLUS ONE CHARACTER, FIVE TOKENS, AND `~` IS THE ONLY ESCAPE:*** `~~` value mark, `` ~` `` subvalue mark, `~!` text mark, `~-` a literal tilde where one would be misread, `~,` a literal comma where one would read as a run separator. **Consecutive marks are separated by a comma** - `~!,~!,~~`. **The refusal is gone**: the conversion is lossless for every record. All of it is the owner's, 27 Aug 2026, and `~!` is his own correction of his first `` `~ `` - see the START HERE box for why that mattered. `gplbld/test-edittokens-units.py` proves it in Python, exhaustively, and is on `$neverShipped`. ***DECIDED 26 Aug 2026, NOT YET BUILT: `micro` WILL SHIP WITH SD RATHER THAN BE FETCHED BY winget.*** Owner's ruling, and **his reason is the one that decides it, not size**: a bundled micro is *pinned to the SD release*, so *"if someone asks us a question about 1.0-0 we know exactly which micro they have installed"*. winget cannot give that - two machines installed a month apart run different editors and nobody knows. It also fixes the case the present design structurally cannot: **an offline machine, a policy-blocked winget or a Server SKU with no App Installer gets no `micro` at all today.** ***SEQUENCING IS HIS AND IT IS DELIBERATE: finish the current validation pass first, and only when that is stable add micro and cycle again.*** **Licence is clear** - micro is MIT, so binary redistribution is permitted provided the copyright and permission notice ship with it, and aggregating an MIT program beside GPL-3 SD raises nothing. **The no-binaries rule is not in the way either**: it governs the REPOSITORY, and the installer already carries binaries the repository does not hold - `dll_closure()` computes the MSYS2 DLL set off the build machine and nothing binary is tracked. **Measured for the decision**: micro's win64 zip is 5,148,356 bytes against an installer of 4,830,157. ***THE THIRD-PARTY LICENCE QUESTION IS SETTLED AND NEEDED NO JUDGEMENT***: micro's repository root carries **`LICENSE` (1,086 bytes) and `LICENSE-THIRD-PARTY` (64,173 bytes)**, so upstream has already assembled the dependency notices. **Ship all three files together** - the executable and both licence files in the same directory - and the obligation is met by mirroring what micro itself distributes. *(An earlier note here said micro carried no third-party file. That was wrong: it read the contents of `LICENSE` rather than the repository listing.)* ***AND `micro` HIGHLIGHTS SD BASIC; `edit` CANNOT.*** `gplbld/microcfg/syntax/sdbasic.yaml` **ships** (so it is NOT on `$neverShipped`) and is **generated from `BCOMP`'s own tables** by `mkbasicsyntax.py` — 218 statements, 37 reserved words, 176 intrinsics. `EDIT` names `C:\Program Files\SD\micro` in `MICRO_CONFIG_HOME`, which is micro's only machine-wide config route; the other two are per-profile and SD's accounts have no Windows profile. Detection is on the working copy's name — a BP record is written as `<record>.editing.sdbasic`. `checksyntax.py` is the control (**24 patterns, 0 bad**): inside a double-quoted YAML scalar `\.` is not a legal escape, so a natural-looking regex invalidates the whole file and **micro reports that by not highlighting**.

***THE DOCUMENTATION GETS ITS OWN GitHub REPOSITORY, AND IT WILL NOT CARRY THE NO-BINARIES RULE — OWNER, 26 Aug 2026.*** That **reverses** §"WHERE THE WORK LIVES", which said documentation lives here; the entry keeps what the old ruling was protecting against, because **drift is now caught by a person or not at all**. ***`sd4windows` is unchanged — no binary becomes trackable in THIS repository.*** ***AND THE MOVE IS NOW COMPLETE***: `SDCoreWindowsDocs` exists, the tree was moved by the owner out of `sdhelp` to `C:\Users\dmont\Projects\SDCoreWindowsDocs` and restructured into `Testing` / `User` / `Technical`, each `markdown` + `html` + `pdf`, and the two render scripts went with it. **The P-drive copy is stale.**

***THE INTERPRETER DECISION IS ANSWERED — OWNER, 26 Aug 2026: THE MSYS2 PYTHON.*** `mkdoc.py` is the only thing in the whole build with a third-party dependency — `markdown` — and the gap was bigger than the package: it was installed for the **Windows** python (3.13.14) and not for the **MSYS2** python `setup-devbox.ps1` installs (3.12.13), so on a fresh box `python mkdoc.py` failed at the *interpreter*. **`python-markdown` is now in `setup-devbox.ps1`'s package list**, and `-CheckOnly` names it as the one thing missing on this host.

***ONE COMMAND IS STILL OWED ON THIS MACHINE, AND NOTHING IS BLOCKED ON IT.*** The package is chosen but not installed for the MSYS2 python here; `mkdoc.py` runs under the **Windows** python (3.13.14, `markdown` 3.10.2) and that is what rendered every page of the tester set. Either re-run `setup-devbox.ps1` elevated, or install the one package inside MSYS2: `pacman -S --needed python-markdown`. ***`mkdoc.py` ITSELF IS NO LONGER IN THIS REPOSITORY*** — see the H.2 entry.

***THE MACHINE — INSTALL 27 Aug 2026 19:37:47, GREEN AND CURRENT.*** Three cycles ran that day: 17:25:59 shipped PRE_RELEASE 29, 23 and 21; **18:58:55 shipped 29's rewrite** after the first version was measured and found to fix nothing; **19:37:47 shipped the two faults that still stopped it**, and `micro` is witnessed working on that one. `assert-current` **exit 0 live**: `sd.exe` `DF77FD6D61DE5184` unmoved (all BASIC), `bin\` built 26 Aug 20:40, **`gcat` 125 / `gpl.bp.out` 184**. *(Staleness pattern, kept: 26 Aug 20:40 three C files → owner's 21:17:22 cycle; `gpl.bp/EDIT` → his 27 Aug 12:05 cycle; the three-fix batch → 17:25:59; 29's rewrite → 18:58:55.)* ***`-Run b48` RAN AGAINST THE 18:58:55 INSTALL (the BASIC is unchanged since, only `EDIT` and the helper moved): 30 of 31, 971 `PASS`, 3 `[FAIL]`, 0 `[SKIP]`*** — see START HERE item 1. **`b48` is spent twice over; the next run is `b49`.** The host previously carried a **FULL** install (**26 Aug 2026, 17:14:03**) with the suite green — **31/31 steps, every one exit 0: 12 unelevated + 19 elevated, `-Run b46`. 991 `PASS`, 0 `[FAIL]`, 0 `[SKIP]`.** `sd.exe` `8E6A6CF45AA6F20A`, `gcat`/`gpl.bp.out` 125/184. **`b46` is spent — use `b47`.** `assert-current` was **exit 0 run live at the start of the sixty-third session** and is **now expected to FAIL** until the cycle runs — the binary moved, the install did not. ***THE COUNTS ABOVE ARE NOT THE ONES THE RUN REPORTED, AND THE DIFFERENCE IS AN INSTRUMENT DEFECT — §6, "the PASS count was grepped out of files nothing could read".*** The 61st session recorded this run as *"19 of 19 steps exited 0"*, which is the **elevated half's own line** and reads like a 19-step suite; the unelevated 12 ran and passed too. ***Guest `sdStandalone-C1` remains***, powered off, carrying the stand-alone install that closed H.5; **it shares MAC `080027AECE7C` with `Windows 11 - Template`, so never run both at once.** ***[STALE — `sdStandalone-C1` IS NO LONGER REGISTERED, MEASURED 2 Sep 2026, SO NOTHING COLLIDES AND EVERY REMAINING VM MAY RUN CONCURRENTLY. See the fuller note at "ONE THING IS LEFT ON THE MACHINES".]*** Delete it by hand when nobody needs that install: `VBoxManage unregistervm sdStandalone-C1 --delete`. `sshRemoteTest-C1` is gone, deleted by the 7.18 cleanup.

***THE `SD TCL` REFERENCE HAS STARTED AND IT LIVES IN THE `User` SET, NUMBERED FROM 19.*** Owner's ruling, 26 Aug 2026, on both questions: the TCL pages continue `User/` rather than taking a set of their own, and they are named `NN-sd-tcl-<topic>.md`. **The plan is 14 topic pages plus a generated syntax card at `33`, and it is checked rather than asserted** — every one of the **144** verbs is on exactly one page, verified in both directions. ***`19` TO `32` ARE ALL WRITTEN (27 Aug 2026) AND THE ROSTER CLOSES AT 144 OF 144.*** ***THE ROSTER IS 144, NOT 140***, and the difference is the four records that are a keyword AND a verb — `break`, `count`, `display`, `off` — which `CPROC:1718` re-parses from field 3. **SD's own VOC dictionary agrees**: its I-type `DISPATCH` encodes the same rule, and `count voc with dispatch # ""` answers 144. `tools\sdtcl.ps1` is how the TCL pages are measured.

***THE DOCUMENTATION PHASE IS FINDING DEFECTS, AND THEY HAVE THEIR OWN LIST: [PRE_RELEASE_FIXES.md](PRE_RELEASE_FIXES.md).*** **Thirty-four entries as of 27 Aug 2026.** 24 to 28 from writing SD TCL `30` to `32`; 29 the owner's `micro`-cannot-save; 30 and 31 the two verifier issues `b48` surfaced (30 fixed, 31 open for the owner); **33 and 34 from writing `Technical/02`** — a shipped script whose own usage text omits the switch it requires, and a whole documentation set with no working release command. **It is maintained the way UPSTREAM_FIXES.md is**: add an entry in the same commit as the finding, move it to DONE when fixed. Writing a reference checks every claim against what SD does, which is not the same exercise as testing that it works, and it is turning things up that neither the suite nor the docs did on their own.

***ONE DEFECT IS RAISED AND UNDECIDED, AND THE DOCUMENTATION PHASE WILL MEET IT.*** `sdsys\changelog` ships into the **data tree**, which the installer never overwrites, so a user's changelog is frozen at their install date — in the one file whose entire job is telling them what changed. It probably wants moving to `{app}` beside the documentation. Raised 25 Aug 2026; not decided, and not yet a task.

---

## THE TASK TABLE — READ THIS BEFORE ANSWERING "WHAT IS LEFT"

Owner's instruction, 26 Aug 2026, after being given a different list of
outstanding work three times in one session: **a table at the top, checked off
as items finish, so nobody searches history to find out what is done.**

***IT IS THE AUTHORITY ON STATUS. The entries below carry the reasoning; this
carries the state.*** If they disagree, that is a defect — and it is checked
rather than trusted: `python sdb_ai/sd64/gplbld/check-stale-leads.py` verifies
every row against its entry, **in both directions**, and exits non-zero on
drift. Run it before answering the question this table exists to answer.

**`ID` is what the checker matches on. Do not renumber; steps 4–13 have carried
their numbers since 13 Aug 2026 and the rest of the file cites them.**

| | ID | what | settled |
|---|---|---|---|
| ✅ | **7.0** | Linux access model restored, installed, verified end to end | 14 Aug 2026 |
| ✅ | **7.1** | Account-model loose ends; `CREATUSR` gone | 16 Aug 2026 |
| ✅ | **7.2** | Second machine — the VirtualBox rig. **Still the rig for 4** | 15 Aug 2026 |
| ✅ | **7.3** | Installer loose ends — **every bullet closed.** The last was the remote-block control, and it was the only thing in the stated 1.0-0 gate. See item 4 | 25 Aug 2026 |
| ✅ | **7.4** | Built and verified | 16 Aug 2026 |
| ✅ | **7.5** | `GPL.BP/GRANTA`, (f) included | 16 Aug 2026 |
| ✅ | **7.6** | The API works end to end | 17 Aug 2026 |
| ✅ | **7.7** | `SH` and `OS.EXECUTE` permitted by a list, both halves | 17 Aug 2026 |
| ✅ | **7.8** | Lower case everywhere, both halves | 22 Aug 2026 |
| ✅ | **7.9** | Scheduled jobs — closed and measured | 23 Aug 2026 |
| ➖ | **7.10** | Removed from this project — owner | 23 Aug 2026 |
| ✅ | **7.11** | `SDConnectLocal()` carries a session | verified |
| ➖ | **7.12** | Rewritten on the owner's ruling. **Do not restore the old shape** | 21 Aug 2026 |
| ➖ | **7.13** | Dropped as a migration — owner | 23 Aug 2026 |
| ✅ | **7.14** | **API session identity — shape (b), the session becomes the authenticated user.** Decided 23 Aug, closed 24th: `verify-apiidentity` exit 0, `ZZAPI` owned by the user where `b28` had `NT AUTHORITY\SYSTEM` | 24 Aug 2026 |
| ✅ | **7.15** | Data tree private from SD's own users — ACL lock, all four writers | 24 Aug 2026 |
| ✅ | **7.16** | SD reads and writes CRLF, both halves | 24 Aug 2026 |
| ✅ | **7.17** | `setup-devbox.ps1` ran end to end | 24 Aug 2026 |
| ✅ | **H.1** | The cycle and suite record — ***FULL install 29 Aug 15:33:45, `-Run b66`: UNELEVATED 13 OF 13, ELEVATED 19 OF 19, 1,106 `[PASS]`, ZERO `[FAIL]`, AND ZERO TABLE ROWS SCORING FAIL. GREEN IN BOTH HALVES FOR THE FIRST TIME.*** **PRE_RELEASE 59 CLOSES with it** — all five of its verifiers pass, and `verify-batchjob`'s re-aimed row reads `ELEVATED in SDSYS, no entry: still runs` **PASS, decisive**, with neither refusal marker firing. ***SDSYS WAS CHECKED CLEAN AFTERWARDS***, since that row is the first thing to plant a probe there deliberately: no `ZZBATCHS` in `bp` or `bp.out`, `batch.jobs` empty, and `zzbatch` **0 hits** in the VOC buckets against a control that finds `listf` 6, `count` 18, `who` 15. ***SPENT: b54–b66 — USE `b67`.*** *(Previous: `-Run b65`, unelevated 12 of 13, the one failure `verify-batchjob` before it was re-aimed.)* **The one failure is `verify-batchjob` exit 1**, 9 of its 10 rows passing, and it is **the verifier and not the product** — see PRE_RELEASE 59. ***`verify-lcnames` IS BACK TO 142 OF 142*** (it was 107 of 128 on `b60`) and `verify-osusers` 44 / 0, which is 56 clause 2's reversal landing exactly where it was predicted to. ***SPENT: b54–b65 — USE `b66`.*** **The `b64` token bought nothing**: an interrupted parent stranded `sdtub64`, and `b65`'s sweep removed it (`DELETE.ACCOUNT`, both halves gone, checked afterwards). ***COUNT `[FAIL]` WITH THE BRACKETS***: a bare `FAIL` also matches `verify-fold`'s negative-control row *"expected FAIL, observed FAIL, result PASS"*, which is a check working correctly. *(Previous: FULL install 29 Aug 10:35:46, `-Run b59`: ELEVATED 19 of 19, 397 PASS / 0 FAIL / 0 SKIP — GREEN FOR THE FIRST TIME, and `verify-apiadmin` 22/22 CLOSES PRE_RELEASE 31.)* **UNELEVATED 8 of 13**, and all five failures are **PRE_RELEASE 59**, one cause: `lcnames`, `osusers`, `nocase`, `lineendings`, `batchjob` all assume an administrator lands in an ordinary account, which 56 abolishes. **Not product defects — every one refused the null case out loud.** ***CARRY 22/22 FOR `verify-apiadmin`, NOT 21/23***: b58's own log reads 21 PASS / 1 FAIL, so it was always 22 checks. ***SPENT: b54–b59 — use `b60`.*** ***READ THESE TRANSCRIPTS WITH `Get-Content` OR `iconv -f UTF-16LE`: THEY ARE UTF-16, and a plain `grep` reports 0 PASS / 0 FAIL on a full log*** — which reads exactly like a step that did nothing. *(Previous: FULL install 28 Aug 21:27:34, `-Run b58`: 13 of 13 unelevated + 18 of 19 elevated)*, `assert-current` exit 0 live. The one failure is `verify-apiadmin` **21/23**, the stale control of PRE_RELEASE 31, now identical across **five** runs — treat any other number there as news. **`verify-doors-suite` is green**, first time in b56 (PRE_RELEASE 44's verifier half). ***SPENT: b54, b55, b56, b57, b58 — use `b59`***, and `b55` is the cautionary one: it was burnt against a stale tree, refused eleven steps, and still left `sdsshb55` behind, because the two `assert-current`-exempt scripts run anyway. *(Previous entry, kept for the shape: 27 Aug 22:52:21, `-Run b49`, 30 of 31 steps, 963 `PASS`.)* | 28 Aug 2026 |
| ➖ | **H.2** | ***SUPERSEDED 30 Aug 2026 — COMBINED INTO PRE_RELEASE 80, THE SINGLE DOCUMENTATION AUDIT.*** Documentation — ***THE TESTER SET IS 15 PAGES, REVIEWED, AND 16 OF THE 18 QUESTIONS ARE ANSWERED AND APPLIED*** (26 Aug 2026). Lives in `SDCoreWindowsDocs` at `C:\Users\dmont\Projects\SDCoreWindowsDocs`, branch `main`, with its own toolchain in `tools\`. **Open: q7 the `limitssh` default, q14 the unmeasured ssh-elevation caveat** — both at the top of `QUESTIONS-2026-08-26.md`. ***THE `User` SET IS 32 PAGES — 18 SD BASIC plus SD TCL `19` to `32`, ALL FOURTEEN TOPIC PAGES — and the `Technical` set has its first, `01` Restricted Commands. `docmap` 411 of 411, `checklinks` 183 links 0 broken on `User`, HTML and PDF both current (27 Aug 2026). ***THE `tclmap` FIGURE BELOW IS STALE AND THE TREE IS RED — MEASURED 31 Aug 2026: roster `146`, assigned `143`, exit `1`, three `NO PAGE` rows for `remote.api`, `remote.ssh` and `ssh.server`.*** The roster is COMPUTED from `newvoc` plus `TIER.ADD.ADMINISTRATOR`, so it grew on its own when entry 78 added those verbs on 30 Aug; nobody ran it. **Read PRE_RELEASE 80, which now carries the measurement and the reason it went unseen** — `tclmap.py` lives in the other repository and no tier-1 check here runs it. `18` and `Technical/01` are generated and partition the roster, 447 of 447. ALL 143 TCL VERBS HAVE A PAGE — 144 until `encrypt.field` went (PRE_RELEASE 53); `tclmap` 143 of 143, 0 exempt. LEFT: the generated TCL syntax card at `33`. OPEN: document `09` is 8 of 8 restricted commands and may belong in `Technical` too — the owner's call.*** ***THE SHIPPED-SCRIPTS GAP IS CLOSED***: `Technical/02` The Installed Scripts covers all **26** that ship, and tester `01` now prints the `install-ssh.ps1` retry command. **`Technical` still has no cross-page link, so `release.ps1` cannot complete on that set — PRE_RELEASE 34, the owner's call**. ***AND NOW PRE_RELEASE 58: THE WHOLE ACCESS MODEL THE DOCUMENTATION DESCRIBES HAS CHANGED*** — administrators elevated at login into SDSYS with no account of their own and **no ssh**, grants downward only, SDSYS never granted. **Filed and deliberately not started**: 56 and 57 both still have unsettled pieces, and writing a reference against a model in motion is how the tester set described `encrypt.field` for a week after it was deleted. **It collides with 34 and 55 — do them together** ***— AND THAT IS EXACTLY WHAT THE OWNER RULED ON 30 Aug 2026: ALL THREE ARE NOW ONE TASK, PRE_RELEASE 80.*** *"Wrap all the outstanding documentation pre-release tasks into a single documentation audit task that validates and updates the whole documentation tree against the final install image. This task will be done just before the final release 1.0 wrap up. In this task you take control of the gap analysis, you validate, correct and build all the documentation both yours and the other AI's."* **This row is SUPERSEDED, not finished** — the work above is untouched and is what 80 carries out; what has gone is its separate number, so nobody plans it twice. ***THE ROW ITSELF PREDICTED THE COMBINATION*** with *"writing a reference against a model in motion is how the tester set described `encrypt.field` for a week after it was deleted"*, and the model has moved five more times since it was written: **56**, **67**, **75**, **76**, **77**, **78** and **79**. **Read PRE_RELEASE 80, not this row** | ➖ 30 Aug 2026 |
| ✅ | **H.3** | Data-tree upgrade path — `-Compare` 55 PASS / 0 FAIL / 1 SKIP, and `RefreshDictionaries` 76 of 76 | 26 Aug 2026 |
| ✅ | **H.3a** | VFS stripped from the C, cycled and checked on the installed tree | 25 Aug 2026 |
| ✅ | **H.4** | ***The ssh scoping BLOCKS a remote machine — proven.*** Rule `Any` → host dial CONNECTED 23ms; rule `127.0.0.1` → dropped 4003ms, with port 5040 on the same guest answering in 23ms as the witness | 25 Aug 2026 |
| ✅ | **H.4a** | **The ssh remote-block RUNBOOK — run and passed.** Kept for the next guest: item 5's SKIP wants the same rig. ***The `Open` leg must run FIRST***, and the precondition is a **Private** network profile on the guest | 25 Aug 2026 |
| ✅ | **H.5** | Stand-alone install — ***CLOSED. 21 PASS / 0 FAIL / 0 SKIP*** on guest `sdStandalone-C1`, 01:46:11. The SKIP fired its strong form (`no ssh server on this machine at all`); pages seen and correct with **no `sshremote`/`apiremote` boxes**; preflight question answered — it still refuses | 26 Aug 2026 |
| ✅ | **7.18** | ***THE LAST DEVELOPMENT TASK — CLEAN UP. DONE.*** Two runs of `cleanup-devlitter.ps1` either side of a reboot: **0 profile dirs, 0 `ProfileList` entries, 0 `sd*` users, only `sdout` in `~`, clone gone** — read back independently. **Nothing over-deleted**: the five real SD groups, `don` and `test1` all present | 26 Aug 2026 |

**Legend** — ✅ closed and verified · ◐ **partly**: some parts closed,
some open, and the row says which · ⬜ open · ➖ removed or superseded,
kept so the number is not reused.

***◐ IS NOT A SOFTER ⬜.*** It means the entry legitimately contains **both** a
closure and an open claim, and the checker REQUIRES both to be present — an
entry with only one of them is drift, so it either gets ticked or gets marked
open. **No row carries ◐ today**; 7.3 and H.5 were the last two and both closed
on 25 and 26 Aug 2026. When one is used again, name the remainder in the row
itself so nobody has to open the entry to find out what is left.

***WHAT IS NOT IN THIS TABLE, ON PURPOSE.*** §4's *"Not verified — treat as
unknown"* holds the **exercise gaps** — semaphore contention, competing
sessions, real application data, interactive SD over ssh at a real terminal,
`K$SET.USERNAME`'s non-`$internal` refusal, and the daemon's `check_lost_users`
symptom-without-cause. **None is a task with an owner; each is a thing nobody
has yet had cause to run.** Swept 26 Aug 2026: six stand, one struck.

## THE DESTINATION: SD MUST BE MOVEABLE TO A NEW COMPUTER

Owner, 2 Sep 2026, giving the reason behind PRE_RELEASE 135: *"eventually we
will need a utility that allows sd to be moved to a new computer — when that
happens, everything needs to come back the way it was — so uninstall,
reinstall is kind of a shadow of that."*

***THIS IS A DIRECTION, NOT A TASK, AND IT CHANGES HOW THE UNINSTALL/REINSTALL
ENTRIES SHOULD BE FIXED.*** 120, 132, 134 and 135 all look like installer
defects on their own. They are the same question asked four times: **what does
SD need in order to put a machine back the way it was?** A fix that restores
the property by accident of the local machine — a surviving group, a directory
the uninstaller happened not to take — closes the entry and **does nothing for
the move**, because on a new computer none of those local things exist.

**THE TEST TO APPLY TO EACH FIX: would it still work if the only thing carried
to the new machine were the data tree?** The register survives a move;
`sdu_<name>` groups, ACLs, LSA rights and the uninstall log do not.

- **134's manifest is the right shape** — it compares a tree against itself and
  will compare a moved tree just as well.
- **135 is where the choice bites**, and it is recorded in that entry: the
  `sdu_*` groups are the cheap enumeration and survive a reinstall, while the
  `accounts` register is the one that survives a move.

***AND THE ONE STRUCTURAL OBSTACLE IS ALREADY KNOWN, SO DO NOT REDISCOVER IT***
— CLAUDE.md: `gpl.bp`, `syscom`, `newvoc`, `voc_template` and `messages` are
replaced on an upgrade, **but no existing account, including SDSYS's own, ever
gains a new verb**, because `voc` is neither replaced nor preserved. **A
register-driven restore that needs a NEW verb would not resolve on precisely
the upgrade and reinstall paths it exists to serve.** The established
install-time route into SD is `adopt-account.ps1` — `-start`, `sd -internal
<existing verb>`, `-stop` — and it calls a verb that already exists.

## NEXT SESSION: START HERE, IT IS SHORT

> # ⇩⇩⇩ HANDOFF 18, 2 Sep 2026 — ***THE GUEST RUN LOST ITS DATABASE HALF-WAY AND PRODUCED THREE ENTRIES INSTEAD OF CLOSING SIX. A CYCLE IS OWED. `sd.iss` HAS CHANGED AND `assert-current` IS RED BY DESIGN.*** ⇩⇩⇩
>
> ***WHAT HAPPENED, IN ONE LINE: THE UNINSTALLER'S TWO QUESTIONS WERE BOTH
> ANSWERED BACKWARDS, THE DATA TREE WENT, AND FOUR ENTRIES THAT NEEDED IT COULD
> NOT BE WITNESSED.*** That is **PRE_RELEASE 139**, and it is a finding rather
> than an accident — see below.
>
> ### ***THE STATE OF GUEST `Windows 11 - Test 10` RIGHT NOW***
>
> **No SD at all** — `C:\ProgramData\SD` and `C:\Program Files\SD` both absent,
> `sdssh`/`sdapi`/`sdsshonly` gone. **`sdusers` and `sdu_ZZ135` survive, and
> `zz135` is still an ENABLED Windows account with its password.** So the guest
> is *not* clean and `create.account zz135` will be refused — **use a new name.**
>
> ***ONE FREE MEASUREMENT IS SET UP AND WAITING, TAKE IT ON THE NEXT INSTALL.***
> `sync-route-groups.ps1` seeds `sdssh` **from `sdusers`**, which still holds
> `zz135`; the register will be empty, so `restore-sshonly.ps1` adds nobody to
> `sdsshonly`. **Predicted: `zz135` comes back able to ssh in, not confined, with
> no SD account.** Read the four groups *before* creating anything.
>
> ### ***WHAT IS BUILT AND UNWITNESSED***
>
> **139's ASKING half.** Both uninstaller questions now go through one
> `KeepOrDelete()` in `sd.iss` with **command links labelled Keep and Delete**
> (owner's ruling). ***THE MAPPING IS INVERTED FROM THE OLD CODE AND THAT IS
> FORCED, NOT CHOSEN***: focus follows `Labels[0]`, so the safe answer must be
> first — **Keep = IDYES, Delete = IDNO**, where both call sites used to test
> `= IDYES` for delete. **The inversion lives in one function on purpose.**
> Every property was measured with `gplbld/probe-taskdialog.iss`, which is kept
> and is on `$neverShipped`; **three of its six findings are invisible to a
> compiler** — `MB_DEFBUTTON2` compiles and dies at run time with *"Invalid
> Buttons"*, and the uninstaller context had to be proved separately.
> **`MinVersion=10.0`** went in beside it (owner: *"I would allow 10 & 11 nothing
> earlier … just because 10 is still in extended support"*) — **it was absent, so
> Inno's Windows 7 SP1 default had been applying.**
>
> ***139's RECORDING half is NOT built and is the open part***: the database
> question confirms nothing afterwards and writes no log, while the accounts
> question does both — so nothing on disk can say which was chosen. That is why
> this entry cannot state whether the click was wrong or the code was.
>
> ### ***NEXT STEPS, IN ORDER***
>
> 1. **A CYCLE.** `sd.iss` ships and has changed, so `assert-current` is red and
>    the 17:45:23 installer is now behind source. `gplbld/check-iss.ps1`-style
>    compile-checking is already done — **`sd.iss` compiles, 4,750 lines, ISCC
>    exit 0** — but nothing has been installed.
> 2. **Re-run the guest sequence properly**: install → read the four groups →
>    create the witness account under a NEW name → `capture-state -Label first
>    -Manifest` → interactive uninstall, **Keep on both questions** → reinstall →
>    `capture-state -Label after` → diff. That closes **120, 132, 134, 135**, and
>    now also witnesses **139's new dialog**.
> 3. **136 and 70 never needed the database** and are still witnessable on any
>    fresh install: `listf` in a created account showing descriptions, and
>    `[locked]` after the type code in a VOC record surviving `update.account`
>    with message 10165 naming it.
>
> ***OPEN 19***: 16, 65, 66, 70, 80, 89, 93, 96, 102, 114, 120, 132, 133, 134,
> 135, 136, **137, 138, 139**. ***NEXT FREE PRE_RELEASE ID: 140. NEXT RUN TOKEN:
> `b103`.*** **All nine free checks green.**
>
> ### ***THE THREE THINGS MOST LIKELY TO BE GOT WRONG NEXT***
>
> 1. ***138 IS NOT A BUG IN THE CREDENTIAL CODE.*** An administrator has TWO
>    accounts — unelevated lands in their own, elevated lands in SDSYS — and the
>    install sets a password for the first while the second has none. **Nothing
>    is broken; one of two needed credentials is set and nothing says there are
>    two.** `LOGIN:955` needs a **tty**, and `kernel.c:251` takes it from
>    `ttyname(fileno(stdin))`, so **every piped route skips the prompt** — which
>    is why no cycle has ever met it and why **no verifier can**.
> 2. ***DO NOT RE-DERIVE `TaskDialogMsgBox` FROM THE HELP.*** It is a compressed
>    `.chm` and cannot be searched from the build tree. Everything known about it
>    is in `probe-taskdialog.iss`, measured; re-run that instead.
> 3. ***A `#` AT THE START OF A LINE IN AN `.iss` IS A PREPROCESSOR DIRECTIVE***
>    — it cost two aborted compiles today, in the same file, on the same line
>    number. `cycle.ps1:301` holds the whitelist that tells a real directive from
>    a wrapped `#13#10`; **a bare `^\s*#` test is wrong and flags `sd.iss`'s own
>    `#define` block.**
>
> # ⇩⇩⇩ HANDOFF 17, 2 Sep 2026 — ***HANDOFF 16'S STEP 1 IS DONE. IT ALL COMPILES. THE ONLY THING LEFT IS THE GUEST RUN, AND IT NEEDS A PERSON.*** ⇩⇩⇩
>
> ***STEP 1 PASSED — `cycle.ps1 -SkipInstall`, 2 Sep 17:44:46, elevated, and
> the STAGED TREE WAS READ RATHER THAN THE RUN'S OUTPUT BELIEVED*** (the 26 and
> 29 Aug precedent). `CREATEA` and `LOGIN` both **0 error(s)**, both added to
> the global catalogue, both present in staged `gcat` and `gpl.bp.out` at
> **17:45**; staged `messages/10165` **byte-identical to source**; staged tree
> whole — **gcat 133, gpl.bp.out 192, `$CPROC` 26,128, `$BCOMP` 88,070**.
>
> ***THE INSTALLER TO WITNESS WITH IS `C:\Users\dmont\sdout\sd-setup-W1.0-0.exe`,
> 4,959,678 BYTES, BUILT 17:45:23.*** **The host install is deliberately STALE**
> — `-SkipInstall` stops before installing — and **SD is STOPPED** (step 1 stops
> it and this path never restarts it): `sc.exe start SD` from an elevated prompt
> if you want the host back, or just cycle.
>
> ### ***HANDOFF 16'S FACTS WERE ONE CYCLE STALE, AND THREE OF THEM WOULD HAVE MISDIRECTED THE GUEST RUN***
>
> **A FULL cycle ran at 17:03:23** — install **17:04:18**, `assert-current`
> **green** — *after* the 17:01:52 ISPP failure that box calls the last run of
> the day, and *before* the box was written at 17:30. So:
>
> - the `sd.iss` `[Dirs]`/`[Code]`, the new shipped `restore-sshonly.ps1` and
>   the `stage.py` list change were **already compiled and installed**, not
>   pending;
> - the installer on the share was **4,957,848 at 17:03:57**, not 4,955,186 at
>   16:40:42;
> - the only uncompiled work was commit `5510aa6` — **`CREATEA`, `LOGIN`,
>   message `10165`** — which is what 17:44:46 has now built.
>
> ### ***STEP 2 IS UNCHANGED AND IS NOW THE ONLY THING BLOCKING SIX ENTRIES***
>
> Handoff 16's Step 2 table stands **verbatim** — 120+132, 134, 135, 136, 70,
> and the one non-administrator account that 135, 70 and 136 all ride on.
> ***THE ONE CORRECTION: THE GUEST'S COPY IS NOW THREE BUILDS STALE***, not two.
> `C:\Users\Public\sd-setup-W1.0-0.exe` there is still the **14:18:50** binary;
> take the **4,959,678-byte, 17:45:23** one from `\\vboxsvr\sdout\` and check its
> length before installing.
>
> ### ***FILED TODAY: PRE_RELEASE 137. NEXT FREE ID: 138.***
>
> ***A CYCLE'S TRANSCRIPT LOST 1,789 LINES OF ISCC OUTPUT FROM A FRESH WINDOW***,
> and `cycle.ps1`'s "this window has already run a cycle" flag was wrong **both
> ways** the same day — the flagged log is complete, the unflagged one is not.
> It read as *"message 10165 never went into the installer"*, and the evidence
> that settled it was **the installer size, which GREW**. The verdict was never
> at risk (`cycle.ps1:469` gates on `$LASTEXITCODE`), but **a compile error
> lands in exactly the dropped region — the front.** Two `cycle.ps1` changes went
> in with it, neither shipped: the flag's comment now carries the measurement,
> and **step 4 refuses an installer older than its own ISCC start** — the
> previous code took the newest `sd-setup-*.exe` in `$Out`, which on an ISCC that
> exited 0 without writing is the *previous* cycle's binary.
>
> **All nine free checks green after the edits** — tiercounts 15/15, fixlist,
> verdict 140/140, sdtestuser, suiteonly 48/48, retired-wording 30/30,
> stemcoverage, dirscoverage, stale-leads 0.
>
> # ⇩⇩⇩ HANDOFF 16, 2 Sep 2026 — ***EVERYTHING IS COMMITTED AND PUSHED AT `8087936`. NOTHING BUILT AFTER THE 16:13 INSTALL HAS BEEN COMPILED OR WITNESSED. START WITH `-SkipInstall`.*** ⇩⇩⇩
>
> ***THE ONE SENTENCE THAT MATTERS: SIX ENTRIES WERE BUILT TODAY AND NOT ONE OF
> THEM HAS BEEN THROUGH A COMPILER.*** The session ended on credits, green on
> every free check and red on `assert-current` by design. **Do not report any of
> it as working.**
>
> ### ***STEP 1 — PROVE IT COMPILES, AND EXPECT THIS TO FIND SOMETHING***
>
> ```
> C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\cycle.ps1 -SkipInstall
> ```
>
> **ELEVATED PowerShell.** It carries **three BASIC changes** (`CREATEA` ×2,
> `LOGIN` ×3 including new code), a **new message** (`10165`), **seven new
> `[Dirs]` entries**, a **new `[Code]` function** in `sd.iss`, a **new shipped
> script**, and a **`stage.py`** list change. ***THE LAST `cycle.ps1` OF THE DAY
> STOPPED ON A FAULT OF MINE*** — `#13#10` at the start of a line, which ISPP
> reads as a directive — **and its guard caught it before ISCC ran, which is the
> precedent for expecting this step to earn its keep.** Nothing below is worth
> starting until it reports a successful compile.
>
> ### ***STEP 2 — ONE GUEST RUN CLOSES SIX ENTRIES***
>
> **`Windows 11 - Test 10` is still in the state the four witnesses left it**,
> and it is the rig. ***RE-COPY THE INSTALLER FIRST — THE COPY ON THE GUEST IS
> TWO BUILDS STALE AND USING IT WOULD SCORE A FALSE FAILURE ON EVERY ENTRY
> BELOW.*** `C:\Users\Public\sd-setup-W1.0-0.exe` there is the **14:18:50**
> binary. After the cycle, copy the new one from `\\vboxsvr\sdout\` and check
> its length.
>
> **The sequence, ELEVATED throughout, is the one 134 asks for and it witnesses
> everything at once**: install → `capture-state.ps1 -Label first -Manifest` →
> **interactive** uninstall KEEPING the database → reinstall →
> `capture-state.ps1 -Label after -Manifest` → diff.
>
> | entry | what passes |
> |---|---|
> | **120 + 132** | all six of `bp`, `bp.out`, `batch.jobs`, `cat`, `prt`, `$hold` present, and **no `NOT locked` text of any kind** in the closing box |
> | **134** | nothing in the first manifest missing from the second |
> | **135** | needs a **non-administrator SD account created first** — nothing has exercised the live `Add-LocalGroupMember` |
> | **136** | `listf` in a created account shows descriptions, not bare `F` |
> | **70** | put `[locked]` after the type code in one VOC record, run `update.account`, see it skipped and **named** by message 10165 |
>
> ***135 AND 70 BOTH NEED AN ACCOUNT THAT DOES NOT EXIST YET.*** `create.account`
> a PROGRAMMER with `ssh`, grant it `api`, record its membership of `sdssh`,
> `sdapi`, `sdsshonly` **before** the uninstall. That one account is the witness
> for both, and 136's `listf` check rides on it too.
>
> ### ***WHAT IS TRUE RIGHT NOW***
>
> - **Host install 16:13:21**, `assert-current` **exit 1** naming `sd.iss`,
>   `stage.py`, `restore-sshonly.ps1` and the BASIC — **correct, not a fault.**
> - **All eight free checks green**: fixlist **247/0**, dirscoverage, stemcoverage,
>   retired-wording 30/30, verdict 140/140, sdtestuser 54/0, suiteonly 48/48,
>   tiercounts 15/15, check-stale-leads 0.
> - **Installer on the share: 4,955,186, built 16:40:42** — and **it predates
>   the BASIC and `sd.iss` work**, so it is not the one to witness with either.
> - **`Windows 11 - SD ssh baseline`** is the untouched re-run rig, licensed
>   (shared hardware UUID) with its own MAC.
> - ***OPEN 16***: 16, 65, 66, 70, 80, 89, 93, 96, 102, 114, 120, 132, 133, 134,
>   135, 136. **Closed today: 74, 118.** **Filed today: 132, 133, 134, 135, 136.**
>   ***NEXT FREE PRE_RELEASE ID: 137. NEXT RUN TOKEN: `b103`.***
> - **B blockers: 65, 70, 80, 93, 120, 132, 136** — 70 and 136 raised today, 80
>   gained a second item.
>
> ### ***THE THREE THINGS MOST LIKELY TO BE GOT WRONG NEXT***
>
> 1. ***70 IS HALF BUILT.*** The `[locked]` flag is in; **new verbs reaching
>    existing accounts is not**, and its stated mechanism has a hole —
>    `update.account` is in `TIER.ADD.ADMINISTRATOR`, so **only ADMINISTRATOR
>    accounts have the verb**, while the closing box tells the reader to run it
>    in each account. Settle that before building the first half.
> 2. ***133 IS A WORDING FIX AND MUST NOT BE FIXED BY GATING THE ACTION.*** The
>    step 3 box claims ssh was untouched while `sshd_config` was rewritten; the
>    rewrite is CORRECT there and required (`sd.iss:1443`). Only the message is
>    wrong.
> 3. ***THREE PROBES I WROTE TODAY REPORTED A DENIAL AS A VALUE*** — a firewall
>    rule, a process start time, and a directory entry count. **Every probe that
>    reads something an unelevated session may not reach needs its own control**,
>    the way the firewall line now prints `483 rules visible` beside its answer.
>
> ***THE DESTINATION SECTION ABOVE THIS BOX IS NEW AND IS THE REASON 135 WAS
> BUILT THE WAY IT WAS.*** Read it before fixing 120, 132, 134 or 135 further.
>
> # ⇩⇩⇩ HANDOFF 15, 2 Sep 2026 — ***THE WITNESS RUN IS COMPLETE. ALL FOUR STEPS RAN ON `Windows 11 - Test 10`. 74 AND 118 CLOSED; 120 STAYS OPEN WITH ITS FIX PROVED INCOMPLETE; 132 AND 133 FILED.*** ⇩⇩⇩
>
> ***THE FOUR RESULTS IN ONE PLACE.*** **74 — WITNESSED, CLOSED**: the
> interactive uninstall left `sdusers,sdu_don` and took `sdssh`, `sdapi`,
> `sdsshonly`, which is the row's own criterion, and the cycle could never have
> supplied it (`cycle.ps1:497` is `/VERYSILENT`). **118 — WITNESSED, CLOSED, BOTH
> HALVES MEASURED**: over-the-top install, `sshd_config` mtime `15:44:32`
> unmoved and `sshd` process `4964` created `15:44:34`, predating it — file not
> rewritten, service not bounced. **120 — ITS THREE DIRECTORIES PASS AND THREE
> MORE OF THE SAME CLASS ARE STILL DESTROYED**: `cat`, `prt`, `$hold` all
> `exists=False`, and only `cat` is hardened so only `cat` said so. **89A — the
> API box was not offered and `SD-API-In-TCP` stayed `(no rule)` against a
> control of 483 visible rules.**
>
> ***TWO NEW ENTRIES CAME OUT OF IT, AND NEITHER IS A REPEAT OF 120.*** **132,
> `B`** — `SDSYS_PRESERVE` names ten directories and `[Dirs]` protects three,
> hand-enumerated; the *"YOUR DATA IS UNTOUCHED"* box at `sd.iss:3954` is
> generated from the ten-entry list, so three of its six named promises —
> *anything you catalogued*, *the print queue*, *held output* — are false on
> this path. **The fix is a tier-1 guard comparing the two lists, not more
> names.** **133, `S`** — the closing box told the reader ssh was untouched on
> step 3 while `sshd_config` had just been rewritten and `sshd` bounced; the
> message is gated on `not SshWasAbsent` and the action on `not TrueUpgrade`,
> which are independent. **118's defect on a path 118's fix does not reach.**
>
> ~~***ONE MEASURED THING IS UNEXPLAINED AND 132 IS BLOCKED ON IT***~~
> ***RESOLVED THE SAME DAY. 132 IS UNBLOCKED, THE MECHANISM HAS NO EXCEPTION,
> AND THE `entries=0` THAT RAISED THE QUESTION WAS NOT A MEASUREMENT.***
> **`dumps` is not a survivor**: `secure-dumps.ps1:64` creates it when absent
> and its `[Run]` entry (`sd.iss:828`) has no `Check:` and no `Tasks:`, so it
> runs on every install. **`$cred` was never observed empty**: both it and
> `dumps` are `/inheritance:r` with grants to SYSTEM and Administrators only, so
> an unelevated `don` gets *"Access is denied"* — `Test-Path` said `True` from
> the parent listing while `Get-ChildItem -ErrorAction SilentlyContinue`
> returned nothing and `.Count` gave **0**. **So the rule is the plain one**: an
> empty preserved directory the installer recorded is removed at uninstall
> unless something puts it back, and exactly two things do — a `[Dirs]` entry,
> or a create-if-missing hardening script. `cat`, `prt`, `$hold` have neither.
> ***AND `$cred` WAS THEN READ ELEVATED ON THE GUEST RATHER THAN LEFT AS THE
> BETTER EXPLANATION: 1 ENTRY, NON-EMPTY, LEFT ON CONTENT.*** Every directory
> in the sweep now has a measured reason and none is unexplained.
>
> ***AND THEN 132 WAS BUILT ON THE OWNER'S INSTRUCTION — "build 132 with dirs
> entries for cat, prt and $hold". BOTH HALVES ARE IN; NEITHER IS WITNESSED.***
> Three `[Dirs]` entries in `sd.iss` with `uninsneveruninstall`, and
> **`gplbld/test-dirscoverage-units.ps1`**, which reads `SDSYS_EMPTY` and
> `SDSYS_PRESERVE` out of `stage.py` and the `[Dirs]` block out of `sd.iss` and
> fails anything in both python lists with neither an entry nor a declared
> exemption. **Proved red both ways before green** — three lines removed gives
> exit 1 naming exactly `$hold, cat, prt`; three lines present *without*
> `uninsneveruninstall` also gives exit 1, because that flag is tested rather
> than assumed. **Four null cases exit 2, plus a `bp` canary.** Live: **11 at
> risk, 6 with entries, 5 declared exempt, 0 unprotected.** It is on
> `assert-current`'s `$neverShipped` in the same commit, and `assert-current`
> was run after and names only `gplbld\sd.iss` — which is the expected red, a
> cycle being owed again.
>
> ***BOTH OUTSTANDING QUESTIONS WERE THEN RULED THE SAME DAY — "your choice on
> both ... as long as the directories are not needed and reinstalled when the
> install after removal happens" — AND THE CONDITION DECIDED THE FIRST ONE.***
>
> **(1) THE FOUR CONTENT-PROTECTED DIRECTORIES NOW HAVE `[Dirs]` ENTRIES TOO**
> — `$cred`, `os.users`, `os.users.dic`, `batch.jobs.dic`. ***HAVING CONTENT
> DOES NOT MEET THE RULING***: it means the uninstaller does not TAKE the
> directory, not that anything REINSTALLS it, so a site whose `$cred` happened
> to be empty would lose it exactly as `cat` did and no later install would put
> it back. **`[Dirs]` is the only one of the two mechanisms that heals.** The
> guard's `content` exemption kind is deleted rather than emptied, with the
> distinction kept as a comment, and an exemption whose `kind` it cannot verify
> is now a **failure** rather than a typo. **10 of 11 at risk hold an entry, 1
> exempt (`dumps`), 0 unprotected.**
>
> ***THE RULING'S OTHER HALF WAS CHECKED RATHER THAN ASSUMED***: `sd.iss:4465`
> removes the database with `DelTree(DataPath, True, True, True)` from `[Code]`,
> which never consults the uninstall log — so `uninsneveruninstall` cannot keep
> anything the user asked to destroy. **Nothing needs them absent either**: a
> `[Dirs]` entry only ever creates, and `secure-cred.ps1` and
> `secure-osusers.ps1` both exit 2 on a missing path, so guaranteeing existence
> can only move them from failure to success.
>
> **(2) CLAUDE.md's tier-1 list now names `test-stemcoverage-units` and
> `test-dirscoverage-units` too.** Both had shipped without being added, so
> *"run the free tests"* meant a list that excluded them — **the same
> two-lists-kept-by-hand shape both guards exist to catch, in the file that
> tells the next session what to run.** The rule that a new free guard is
> registered there in the commit that creates it is written into that sentence.
>
> ***AND THE OWNER'S OBSERVATION AFTER ALL THAT IS WIDER THAN ANY OF IT, AND IS
> NOW 134***: *"all the system files and directories that existed when sd was
> first installed need to exist after it is reinstalled."* **120 and 132 are its
> directory-shaped subset** — preserved directories that ship empty — and
> `test-dirscoverage-units` guards only that. **The invariant covers every file
> and directory in both trees and nothing checked it.**
> ***`capture-state.ps1 -Manifest` IS BUILT FOR IT***, off by default: sorted,
> root-relative `D `/`F ` lines so two captures diff cleanly, and **a directory
> this process may not read is NAMED, with the tree marked `NOT COMPARABLE`.**
> That guard is the point — a subtree readable before and denied after would
> diff as hundreds of deleted files and read as data loss. **Proved by running
> it unelevated on purpose**: 136 entries in `Program Files\SD`, 3618 in
> `ProgramData\SD`, and `NOT COMPARABLE: 3` naming `profile-reclaim`,
> `sdsys\$cred`, `sdsys\dumps`. ***THE WITNESS IS FREE IF IT RIDES THE RUN 120
> AND 132 ALREADY NEED*** — `-Label first -Manifest`, uninstall keeping the
> database, reinstall, `-Label after -Manifest`, diff. **ELEVATED, or the
> capture says NOT COMPARABLE and means it.**
>
> ***FOUR NEGATIVE CONTROLS, ALL RED WITH THE RIGHT MESSAGE***: entries removed
> (names `$hold, cat, prt`), entries present without `uninsneveruninstall`, an
> exemption relabelled to an unverifiable kind, and `secure-dumps.ps1` doctored
> so it no longer creates — the last proving the machine-checked reason really
> is checked. Every branch of the guard has now been exercised.
>
>
> ***THAT IS THE THIRD TIME IN ONE SESSION A PROBE OF MINE REPORTED A DENIAL AS
> A VALUE***, after `SD-API-In-TCP : (no rule)` and `sshd process started :`
> (empty). **The shape is always the same — `-ErrorAction SilentlyContinue`
> feeding a count, a property or an `else` branch, so "could not look" and
> "nothing there" print identically.** Every probe that reads something an
> unelevated session may not reach needs its own control, the way the firewall
> line now prints `483 rules visible` beside its answer.
>
> ***THE GUEST IS NOW: SD INSTALLED (over-the-top, `SD` service Running,
> Automatic), ssh Running, API off, `cat`/`prt`/`$hold` MISSING.*** It is the
> state 132 and 133 were found in, so **keep it until they are built** — and the
> baseline clone `Windows 11 - SD ssh baseline` is untouched and is the re-run
> rig.
>
> ***THE GUEST IS MID-SEQUENCE AND MUST NOT BE REBUILT.*** `Test 10` has the
> **new** installer on it (`C:\Users\dmont\sdout\sd-setup-W1.0-0.exe`,
> 4,954,811 bytes, built 2 Sep **14:18:50** — it carries 118, 120 and 89A).
> Step 1 was installed with **ssh server TICKED, ssh-remote UNTICKED, API
> UNTICKED**. Nothing else has been done to it.
>
> ***RESUME IN THIS ORDER. DO NOT SKIP THE CLONE — IT BANKS A ~20-MINUTE
> DOWNLOAD.***
>
> ***ITEMS 1 AND 2 ARE DONE — 2 Sep 2026. RESUME AT ITEM 3, THE INTERACTIVE
> UNINSTALL.*** Snapshot A clean (its reading is recorded below); the baseline
> clone exists as ***`Windows 11 - SD ssh baseline`***, MAC `080027276562`,
> hardware UUID `59d00c9d-…` shared with the Template as the licence needs, all
> **three** shares inherited. **Checked across every registered guest: 7 VMs, 7
> distinct MACs, no collision** — so it may run alongside the others.
>
> 1. ~~**Snapshot A** (read-only, command below)~~ — **DONE, clean.**
> 2. ~~**Shut `Test 10` down and CLONE it.**~~ — **DONE.** That clone is "SD + ssh server,
>    nothing else" and is the owner's re-run rig. `clonevm` refuses a running VM.
>    ***CLONE WITH `--options=keephwuuids` OR THE CLONE IS UNLICENSED*** — and
>    **not** `keepallmacs`; the two are decided separately, see the rig section's
>    "THE TWO CLONE OPTIONS ARE NOT A PAIR".
> 3. ~~Boot it back and do **step 2**: an **INTERACTIVE uninstall, KEEPING the
>    database** = **74**.~~ — ***DONE, AND 74 HOLDS.*** `sdssh`, `sdapi`,
>    `sdsshonly` gone; `sdusers` and `sdu_don` still there. The accounts-removal
>    offer was declined (**No**, its default) — it is a different branch and not
>    part of 74.
> 4. **Step 3**: reinstall, **database KEPT** = **120 + 89A**. Expect **no
>    hardening warning**, `sdsys\bp`, `bp.out`, `batch.jobs` all present, the
>    **API box NOT offered**, and `SD-API-In-TCP` unchanged.
>    ***THE TASKS PAGE IS SHOWN ON THIS PATH AND THAT IS CORRECT*** —
>    `SdWasInstalled` is false once the uninstall key is gone, so `TrueUpgrade`
>    is false; `sd.iss:1443`'s comment covers exactly this case.
>    ***AND THIS STEP IS EXPECTED TO MOVE `sshd_config`'s mtime.*** Record the
>    new value: it, not snapshot A's, is what step 4 compares against.
> 5. **Step 4**: install again over the top = **118**. `sshd_config` mtime must
>    **NOT** move ~~from the value snapshot A records~~ ***from the value STEP 3
>    leaves. CORRECTED 2 Sep 2026 — SNAPSHOT A'S VALUE IS ALREADY DEAD AND
>    COMPARING AGAINST IT WOULD FILE A FALSE FAILURE AGAINST 118.***
>
> ***WHY THE ANCHOR MOVED, BECAUSE THE ORIGINAL INSTRUCTION LOOKS RIGHT.***
> `TrueUpgrade = DataTreeUpgrade and SdWasInstalled` (`sd.iss:1461`), and 118
> gates `ApplyAllowGroups` on `not TrueUpgrade` (`sd.iss:3585`). **Step 2's
> uninstall runs `RemoveAllowGroups`** — `sd.iss:1443` says so in as many words
> — **so snapshot A's `14:59:00` was destroyed by design, not by a defect**, and
> the witness measured it: mtime `14:59:00` → **`15:30:04`**, `AllowGroups line`
> now **empty**. **Step 3 is a fresh install** (`SdWasInstalled` false) so
> `ApplyAllowGroups` runs again and the mtime moves again, correctly. **Only
> step 4 is a `TrueUpgrade`**, and only there must it hold still. A session that
> took the instruction literally would score step 4 against `14:59:00`, see a
> move it was told to treat as failure, and file against a fix that worked.
>
> ```
> $o = '\\vboxsvr\xfer\witness-test10-1-after-install.txt'
> "=== STEP 1 AFTER INSTALL  Test 10  $(Get-Date -Format s) ===" | Set-Content $o -Encoding utf8
> "sd groups : $((Get-LocalGroup | Where-Object Name -like 'sd*' | ForEach-Object Name) -join ',')" | Add-Content $o
> foreach ($d in 'bp','bp.out','batch.jobs','accounts') { "sdsys\$d : $(Test-Path "C:\ProgramData\SD\sdsys\$d")" | Add-Content $o }
> $c = Get-Item 'C:\ProgramData\ssh\sshd_config' -ErrorAction SilentlyContinue
> "sshd_config mtime : $(if($c){$c.LastWriteTime.ToString('s')}else{'(no file)'})" | Add-Content $o
> "sshd_config.before-sd : $(Test-Path 'C:\ProgramData\ssh\sshd_config.before-sd')" | Add-Content $o
> "AllowGroups line : $((Select-String -Path 'C:\ProgramData\ssh\sshd_config' -Pattern '^AllowGroups' -ErrorAction SilentlyContinue).Line)" | Add-Content $o
> "APIPORT in sd.conf : $((Select-String -Path 'C:\ProgramData\SD\sd.conf' -Pattern 'APIPORT' -ErrorAction SilentlyContinue | ForEach-Object { $_.Line.Trim() }) -join ' | ')" | Add-Content $o
> $f = Get-NetFirewallRule -DisplayName 'SD-API-In-TCP' -ErrorAction SilentlyContinue
> "SD-API-In-TCP : $(if($f){($f | Get-NetFirewallAddressFilter).RemoteAddress}else{'(no rule)'})" | Add-Content $o
> "sshd service : $((Get-Service sshd -ErrorAction SilentlyContinue).Status)" | Add-Content $o
> ```
>
> **ELEVATED on the guest.** Results come back through `\\vboxsvr\xfer` →
> `C:\Users\dmont\sdxfer` on the host, so they are READ, not pasted.
>
> ***SNAPSHOT A IS TAKEN AND IT IS CLEAN — 2 Sep 2026 15:14:26, 598 bytes, 12
> lines, `witness-test10-1-after-install.txt`. THE BASELINE IS SAFE TO CLONE.***
> ***THE VALUE STEP 4 COMPARES AGAINST IS `sshd_config` mtime
> `2026-09-02T14:59:00`.*** `sshd_config.before-sd` present, `sshd` **Running**,
> `sdsys\bp`, `bp.out`, `batch.jobs`, `accounts` all True.
> **API UNTICKED CONFIRMED AT REST** — `# APIPORT=4243` commented out in
> `sd.conf`, `SD-API-In-TCP` **(no rule)**; that pair is the "unchanged" step 3
> compares against, so step 3 expects **no rule**, not a rule with old scope.
> ***ALL FIVE GROUPS ARE EXPECTED ON A FIRST INSTALL AND `sdapi` IS NOT A
> LEAK*** — `sdapi,sdssh,sdsshonly,sdusers,sdu_don`: `sdusers` and `sdsshonly`
> are unconditional `[Run]` steps (`sd.iss:702`, `:726`), `sdssh` and `sdapi`
> come from `SyncRouteGroups`, **deliberately ungated** (`sd.iss:3564`, its own
> rationale at `:3579`), and `sdu_don` is adopt's per-user group
> (`CREATEA:545`). **The tick governs the route, not the group's existence.**
>
> ### ***THE STEP 2 WITNESS BLOCK — ELEVATED on the guest, AFTER the interactive uninstall***
>
> **Deliberately the same probes as snapshot A so the two files diff against
> each other**, plus three the uninstall is the only step that can answer.
> Parse-checked before hand-over: 96 tokens, 0 errors, no BOM, no CR.
>
> ```
> $o = '\\vboxsvr\xfer\witness-test10-2-after-uninstall.txt'
> "=== STEP 2 AFTER INTERACTIVE UNINSTALL, DATABASE KEPT  Test 10  $(Get-Date -Format s) ===" | Set-Content $o -Encoding utf8
> "sd groups : $((Get-LocalGroup | Where-Object Name -like 'sd*' | ForEach-Object Name) -join ',')" | Add-Content $o
> foreach ($d in 'bp','bp.out','batch.jobs','accounts') { "sdsys\$d : $(Test-Path "C:\ProgramData\SD\sdsys\$d")" | Add-Content $o }
> "ProgramData\SD kept : $(Test-Path 'C:\ProgramData\SD')" | Add-Content $o
> "Program Files\SD gone : $(-not (Test-Path 'C:\Program Files\SD'))" | Add-Content $o
> "sdwind service : $(if (Get-Service sdwind -ErrorAction SilentlyContinue) { (Get-Service sdwind).Status } else { '(no service)' })" | Add-Content $o
> $c = Get-Item 'C:\ProgramData\ssh\sshd_config' -ErrorAction SilentlyContinue
> "sshd_config mtime : $(if($c){$c.LastWriteTime.ToString('s')}else{'(no file)'})" | Add-Content $o
> "sshd_config.before-sd : $(Test-Path 'C:\ProgramData\ssh\sshd_config.before-sd')" | Add-Content $o
> "AllowGroups line : $((Select-String -Path 'C:\ProgramData\ssh\sshd_config' -Pattern '^AllowGroups' -ErrorAction SilentlyContinue).Line)" | Add-Content $o
> "APIPORT in sd.conf : $((Select-String -Path 'C:\ProgramData\SD\sd.conf' -Pattern 'APIPORT' -ErrorAction SilentlyContinue | ForEach-Object { $_.Line.Trim() }) -join ' | ')" | Add-Content $o
> $f = Get-NetFirewallRule -DisplayName 'SD-API-In-TCP' -ErrorAction SilentlyContinue
> "SD-API-In-TCP : $(if($f){($f | Get-NetFirewallAddressFilter).RemoteAddress}else{'(no rule)'})" | Add-Content $o
> "sshd service : $((Get-Service sshd -ErrorAction SilentlyContinue).Status)" | Add-Content $o
> ```
>
> ***SCORE IT AGAINST 74***: `sdssh`, `sdapi`, `sdsshonly` **gone** and
> `sdusers` **still there**; `sdu_don` is not part of 74's claim either way.
> `ProgramData\SD kept` **True** and `Program Files\SD gone` **True** are what
> *"keeping the database"* means, and `sdwind service` should read
> **`(no service)`**. **`sshd service` must still be `Running`** — the uninstall
> is not entitled to take ssh away from the machine.
>
> ***IT RAN, 2 Sep 2026 15:32:59, AND EVERY ONE OF THOSE HELD — 74 IS
> WITNESSED.*** `witness-test10-2-after-uninstall.txt`, 625 bytes, 15 lines.
> `sd groups : sdusers,sdu_don` (the three route groups gone), all four
> `sdsys\…` **True**, `ProgramData\SD kept` **True**, `Program Files\SD gone`
> **True**, `sdwind service` **`(no service)`**, `sshd service` **Running**,
> `SD-API-In-TCP` **(no rule)** and `APIPORT` still commented — the last two
> unmoved from snapshot A, as an uninstall that never had the API on should
> leave them.
>
> ***AND THE `sdusers` DOUBT RAISED AGAINST `sd.iss:1965` IS WITHDRAWN — THE
> SHIPPED TEXT IS RIGHT AND THE GREP WAS READING HALF A SENTENCE.*** `:1966`
> says it outright: *"sdusers stays because deleting it would orphan the
> permissions on your database. The other three groups SD Core made — sdssh,
> sdapi and sdsshonly — ARE removed, without asking"* — which is exactly what
> the witness shows. **`:1965` is the KEPT list, not the removed list.** Filing
> that from the grep alone would have been an invented defect against correct
> shipped wording.
>
> ***THE STEP 1 AND STEP 2 WITNESSES WERE RUN UNELEVATED, MEASURED AFTER THE
> FACT — `elevated : False`, `VIRTUAL\don`. BOTH VERDICTS STILL STAND, AND ONE
> LINE IN THEM DOES NOT.*** Everything 74 rests on is a **positive** reading,
> and a denial can only turn a `True` into a `False`: three route groups absent
> from a list that still showed `sdusers,sdu_don`, four `sdsys\…` `True`,
> `sshd_config`'s mtime read successfully (which also proves `ProgramData\ssh`
> is readable unelevated), `sshd` `Running`.
>
> ***THE EXCEPTION IS `SD-API-In-TCP : (no rule)`, WHICH IS A NULL CASE THE
> BLOCK FAILED TO REFUSE.*** `Get-NetFirewallRule -ErrorAction SilentlyContinue`
> with an `else` branch prints `(no rule)` for **"no such rule"** and for
> **"could not look"** alike. It cost nothing on steps 1 and 2 — the API was
> never on — but **steps 3 and 4 both assert that rule is UNCHANGED**, and an
> unchanged-looking answer produced by a failed lookup is exactly the false
> green §0 is about. **The step 3 block therefore enumerates once, prints
> `firewall CONTROL : <n> rules visible`, and filters in memory**; `n = 0` means
> the verdict line beneath it is void. It also records its own
> `ran as … elevated=` line, so no later reader has to ask this question again.
> ***AND SNAPSHOT A CARRIES A LEAD ON THE RESTART, WHICH IS WHY IT IS WORTH
> READING RATHER THAN FILING.*** `AllowGroups sdssh VIRTUAL\sdssh Administrators
> VIRTUAL\Administrators` — `allow-ssh-groups.ps1:134` composes that prefix from
> `$env:COMPUTERNAME` **at write time**, and the write is `ApplyAllowGroups`
> inside the 14:59 install, i.e. **after** the restart. So the machine was still
> named `VIRTUAL` afterwards, and a `Rename-Computer -Restart` would have left a
> different name. ***THAT WEAKENS THE RENAME CANDIDATE BELOW WITHOUT KILLING
> IT*** — it does not exclude a rename issued and not applied. `VIRTUAL` itself
> is the shared clone hostname (§427, §1300), not a finding.
>
> ***THE GUEST RESTARTED ITSELF DURING STEP 1, BEFORE THE PASSWORD WINDOW, AND
> THE CAUSE IS NOT CONFIRMED.*** **The installer is RULED OUT, measured**:
> `sd.iss:2033` sets `NeedsRestart := False`, there is no `AlwaysRestart` /
> `RestartIfNeededByRun` / `restartreplace` anywhere, and `install-ssh.ps1:77`
> *prints* "RESTART REQUIRED" and `exit 2` rather than acting. **Most likely
> Windows Update** (OpenSSH Server is a Feature-on-Demand pulled from WU). **The
> other candidate is a `Rename-Computer -Restart` handed over for the NEW clones
> and possibly run on this one** — establish which before filing anything.
> ***WHAT IT COST***: the closing box appeared, so the installer's post-install
> code including `ApplyAllowGroups` completed; what was interrupted is the
> window that opens AFTER the installer — the password step — so `don` probably
> has no SD password. **Recoverable, and none of the four witnesses need it.**
>
> ***OPEN 13*** — 16, 65, 66, 70, 74, 80, 89, 93, 96, 102, 114, 118, 120.
> ***FOUR OF THEM ARE B AND THEY ARE WHAT GATES W1.0-0: 65, 80, 93, 120.***
> **Fifteen closed today**: 3, 28, 67, 112, 113, 115, 123, 124, 125, 126, 127,
> 128, 129, 130, 131. **Five filed**: 127-131. ***NEXT FREE PRE_RELEASE ID: 132.
> NEXT RUN TOKEN: `b103`*** — ***`b101` AND `b102` ARE BOTH SPENT.***
>
> ~~***A CYCLE IS OWED — `assert-current` EXITS 1 NAMING `gplbld\sd.iss`***~~
> ***THE CYCLE RAN, 2 Sep 2026. INSTALL `02 Sep 16:13:21`, `assert-current`
> EXIT 0 LIVE*** — `sd.exe` **`1D908330609D69CD`**, `bin\` built 02 Sep
> 00:36:48 with no source newer, **3028 files across the 6 mirrored
> directories**, no renames, no deletions, no leftovers in `C:\Program Files\SD`
> (35 checked). Tier-1 all green after the day's work: fixlist **243/0**,
> retired-wording **30/30**, verdict **140/140**, suiteonly **48/48**,
> sdtestuser **54/0**, tiercounts **15/15**, check-stale-leads **0**.
>
> ***AND THE CYCLE DESTROYED THE ARTEFACT THE DAY'S FOUR WITNESSES WERE TAKEN
> AGAINST, WHICH IS A PROPERTY OF THE RIG AND NOT A FAULT IN THE RUN.***
> `cycle.ps1` writes the installer straight into `C:\Users\dmont\sdout\`, **the
> share the guests install from**, so it is overwritten in place:
> **4,954,811 bytes at 14:18:50 → 4,955,213 bytes at 16:13:00.** The witnessed
> binary is gone from the share. ***THE ONE SURVIVING COPY IS ON THE GUEST***,
> `C:\Users\Public\sd-setup-W1.0-0.exe` on `Test 10`, copied there at ~15:52
> because running an installer off the share had already cost a Network Error
> once (§427). **Keep it.**
>
> ***AND THEN A THIRD BUILD AT 16:40:42 — `cycle.ps1 -SkipInstall`, SUCCESSFUL
> COMPILE, 4,955,186 bytes. THAT IS THE ONE CARRYING THE SEVEN NEW `[Dirs]`
> ENTRIES.*** ***SO THE COPY ON THE GUEST IS NOW STALE AND USING IT WOULD SCORE
> A FALSE FAILURE.*** `C:\Users\Public\sd-setup-W1.0-0.exe` on `Test 10` is the
> **14:18:50** binary — the one witnessed today, and the one WITHOUT the fix.
> **Re-copy from `\\vboxsvr\sdout\` before witnessing 120 and 132**, or the run
> will find `cat`, `prt` and `$hold` still missing and it will look like the fix
> does not work. **Check the length: 4955186.**
>
> ***THE 402-BYTE DELTA IS BUILD NONDETERMINISM RATHER THAN A CONTENT CHANGE,
> AND THAT IS REASONED, NOT MEASURED.*** No shipped file changed between the two
> builds — the working tree was clean and the only commit in between,
> `cbe6ac2`, touches `PROJECT_STATUS.md` and `PRE_RELEASE_FIXES.md` alone — so
> Inno's own timestamps and compression are the remaining explanation.
> **If a witness result is ever challenged on "was it the same installer",
> that is the gap**: nothing hashed the two, and by then one of them was gone.
> **The cheap fix is to copy the installer aside with its build time in the name
> before a witness run, not after.**
>
> ### ***STEP 1 — BUILD THE INSTALLER (ELEVATED)***
>
> ```
> C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\cycle.ps1 -SkipInstall
> ```
>
> **ELEVATED PowerShell.** `sd.iss` has not been through ISCC — there is no
> staged tree on this host to compile it against standalone, so this is the
> first thing that will read the Pascal. **Nothing below is worth starting
> until it reports a successful compile.**
>
> ### ***`b101` SPENT AT STEP 2 — 112's WIRING WAS WRONG TWICE, BOTH NOW FIXED***
>
> **`test-stemcoverage-units` stopped the run and named `sdvv`**, the family
> `VerifyInstall2:240` composes for `verify-vocverbs`; it was never added to
> `clean-test-profiles.ps1`'s `$stems`. ***AND A SECOND FAULT WAS FOUND BY
> READING, WHICH WOULD HAVE COST THE ELEVATED HALF OF ANOTHER RUN***:
> `verify-vocverbs.ps1:209` capped `-Prefix` at **7** characters and `exit 2`s
> otherwise, and **`sdvvb101` is 8** — `sdvvb99` is 7 and passes, `sdvvb100` is
> 8 and does not, so it was wired in during the `b99` era and broke on the next
> run rather than the one that wired it. **The cap protected nothing**
> (`MAX_ID_LEN` 255, `gplsrc/sddefs.h:281`) and is now `{1,14}`; the CASE half
> of that refusal is the real one and is kept.
>
> ***AND THE SCOPE CALL WENT THE OTHER WAY: `sdvv` IS NOT IN `$stems`.*** A stem
> is a claim the sweep will meet the name, and this family only names SD files
> inside the SDSYS account directory. It is declared in a new **`$notProfiles`**
> in the same file — **in the SWEEP, not beside the composition in the runner**,
> because the discipline that has failed five times is *"open
> `clean-test-profiles.ps1` when you invent a family"*, and a runner-side
> declaration would let the next author skip that file and still go green.
> `test-stemcoverage-units` reads it, **prints every exemption**, and refuses a
> name in both lists, an unparsable list, or a declared family the rule can
> already reach. **Proved red and green both ways. Full detail in
> PRE_RELEASE_FIXES 112.**
>
> ### ***`b102` IS GREEN IN BOTH HALVES, AND THE TWO NEW STEPS BOTH MEASURED***
>
> `VerifyInstall1` **every step exit 0, 311 PASS / 0 FAIL / 0 SKIP**;
> `VerifyInstall2` **all 23 steps exit 0**. The two steps 112 wired in have now
> run inside a suite: **`probe-akwrite` 18 of 18** and **`verify-vocverbs` 36 of
> 36** at `[22/23]`, `prefix sdvvb102` echoed, clean-up control green. **The 36
> is the same count the 28 Aug hand-run got, so the wiring cost it nothing.**
>
> ***TWO READING TRAPS THIS RUN PAID FOR, BOTH ABOUT COUNTING RATHER THAN THE
> PRODUCT.*** **(1) A `[PASS]` scan UNDERCOUNTS and can call a real step empty**
> — `verify-sdsysgate` reports in a **Result column** (`PASS   yes`), so a token
> scan reads **0 rows** on a step that ran **10 decisive checks**. Read a
> verifier's own summary line, not your own tally. **(2) `verify-apiadmin` reads
> `22/23` and that is the STEADY STATE** — 22 PASS / 0 FAIL on 31 Aug, 1 Sep and
> 2 Sep alike. ***THE `22/22` RECORDED FOR `b59` IS STALE***: the verifier now
> emits 23 rows, one is unreported, and no run has ever failed on it. **Do not
> spend a session rediscovering either.**
>
> ### ***WHAT IS OUTSTANDING, AND WHAT IT COSTS***
>
> | | needs |
> |---|---|
> | **74** | an INTERACTIVE uninstall on a guest — its wording half is witnessed, the behaviour half is not, and **the cycle cannot supply it**: `cycle.ps1:497` uninstalls `/VERYSILENT`, which now takes the skip path. Afterwards `Get-LocalGroup sdssh, sdapi, sdsshonly` gone, `sdusers` still there |
> | **118, 120, 89A** | ***BUILT, NOT WITNESSED.*** All three need the guest session below. **Do not let "built" become "witnessed"** — 120's own row says so about its finding and it applies twice over to its fix |
> | **89A's two riders** | ***THE RULING WAS "HIDE THE BOX" AND HIDING IT ALONE WOULD HAVE BEEN WORSE.*** `ApplyApiFirewall` is gated in the same edit, or a hidden task reads as unselected and **closes port 4243 on every reinstall**; and `ApiListenerAfterwards` now reads the preserved `sd.conf`, or the account summary claims *"Nothing can reach this account from another machine"* on a machine still running the API |
> | **THE GUEST SESSION** | ***ONE SITTING WITNESSES FOUR, AND THE ORDER IS THE POINT.*** **(1)** install, **(2)** *interactive* uninstall keeping the database — that is **74**, and the cycle cannot supply it (`cycle.ps1:497` uses `/VERYSILENT`); afterwards `sdssh`, `sdapi`, `sdsshonly` gone and `sdusers` still there. **(3)** reinstall with the database KEPT — that is **120**: expect **no hardening warning** and `sdsys\bp`, `bp.out`, `batch.jobs` all present. **(4)** a second, over-the-top install — that is **118**: `sshd_config` and `sshd.pid` mtimes must **NOT** move. **89's Defect A rides on step 3's path too** |
> | **96, 102** | **C on paths that fail silently.** Both shapes are chosen and written into their rows. Each wants a session that BEGINS with it, not one that ends on it. **102 is the larger**: the owner reversed the recorded decision — *"they are deleted, transactions are all or nothing"* — so a half-applied commit must now undo its writes |
> | **65, 66, 70, 89, 114, 118** | build work, no ruling outstanding |
> | **16, 80, 93, 120** | the big ones. **120's finding is attested by the owner and needs no re-measuring**; only a fix and its witness are left |
>
> ### ***FOUR THINGS TODAY PAID FOR — READ THESE BEFORE REPEATING THEM***
>
> ***A LINT PROVES THE PHRASES IN IT ARE GONE, NEVER THAT THE CLAIM IS.*** 130's
> false claim had **ten** copies. Three sweeps each ended in *"that is all of
> them"* and each was wrong; sweeps one and two searched for the **wording** of
> the copies already found, and only the third searched for the **idea**
> (`don't need`, `need not`, `without a password`). The outlier sat in the
> `/SILENT` refusal, which nobody looks at. **I twice told the owner the sweep
> was complete when it was not.**
>
> ***A WITNESS OFTEN COSTS A BOOT RATHER THAN A GUEST.*** The "Before you
> install" page says *"Nothing has happened yet - Cancel stops without changing
> anything"*, and it means it. **129 and 74's wording half were both read by
> launching the installer, paging down and cancelling** — no install, no
> password, and the guest stayed a clean spare. Reach for that before spending a
> rig.
>
> ***MEASURE WHAT AN ACL DOES, NOT WHAT IT SAYS.*** 28's witness was blocked
> because reading the DACL needs `READ_CONTROL`, which is deliberately not
> granted. **Testing the behaviour was both possible and stronger**: as
> `GITORLI\don`, unelevated, in `sdusers` — listing refused, creating allowed,
> `Test-Path` on a real dump refused. Identity asserted, both directions
> measured.
>
> ***A REMEMBERED IMPRESSION IS NOT A MEASUREMENT OF WHICH TOOL WAS USED.*** The
> `guestcontrol` ban was struck in four places on the strength of *"several
> sessions used guest control"*, and restored an hour later: **every mention in
> the record is the ban, never a use**, and HISTORY.md:7929 is a session
> documenting that it took the other route BECAUSE of the rule. The observation
> was true; the attribution was mine and wrong.
>

> # ⇩⇩⇩ A CYCLE IS OWED, 2 Sep 2026 — ***130 IS FIXED IN SOURCE. THEN ONE `Test 6` INSTALL CLOSES 130 AND 125 TOGETHER.*** ⇩⇩⇩
>
> ***`assert-current` IS EXPECTED RED*** — `LOGIN`, `SET_ACC_PASSWORD`, three
> messages, `sd.iss` and the wording lint all changed after the last install.
> **No `make sd`**: nothing under `gplsrc` was touched. **Elevated PowerShell:**
>
> ```
> C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\cycle.ps1
> ```
>
> ### ***THEN ONE `Test 6` INSTALL, BOTH BOXES UNTICKED — IT CARRIES FIVE WITNESSES***
>
> **Install `\\vboxsvr\sdout\sd-setup-W1.0-0.exe` on `Test 6`** — ordinary
> prompt, it elevates itself — and on the tasks page leave **BOTH** the ssh
> boxes **AND** the API boxes **unticked**. That single choice is what makes the
> run worth five things:
>
> | | must read |
> |---|---|
> | **130** — the installer's closing box | ***"A PASSWORD IS REQUIRED. Until this account has one it cannot be used at all - not here at the keyboard, not over ssh, and not through the SD Core API."*** No *"IF YOU SET NO PASSWORD… can be used ONLY at this computer"* |
> | **130** — the post-install password window (`SET_ACC_PASSWORD`) | *"A password is required. Pressing Enter on an empty line does not give you an account without one…"* No *"set no password for now"* |
> | **130** — first `sd`, message 10089 | *"A password is required. Pressing Enter on an empty line does not give you an account without one - it ends this session…"* |
> | **123/124** — the closing box's OTHER branch | the ***`not ApiWanted`*** text, which `Test 4` could not show because the API was ticked there: *"With no ssh server and no API, the accounts you create have no way to sign in yet. Administrators still use SD Core by typing "sd"…"* |
> | **125** — both halves at last | `CREATE.ACCOUNT USER zz125 SSH` → **10161**, and `CREATE.ACCOUNT USER zz125b API` → **10162**. ***10162 is the whole reason this must be `Test 6`***: it fires only when `config('APIPORT')` is 0, which is why `Test 4` could not give it |
>
> ***EXPECT TWO PASSWORD PROMPTS AND HAVE THEM READY*** — SDSYS at the first
> `sd`, then one per account created. **A driving session cannot answer those**;
> they are the one thing that needs a person at the keyboard.
>
> ***AND `Test 7` EXISTS AS THE SPARE, 2 Sep 2026***, MAC `080027FA4150` —
> **distinct, which is this session's own confirmation that a default clone
> regenerates the MAC** rather than an inference from the older clones: it was
> created today and came up unique.
>
> ### ***A NEW CLONE HAS NO SHARED FOLDERS, AND THAT IS THE FIRST THING THAT WILL STOP YOU***
>
> ***MEASURED 2 Sep 2026, AFTER IT COST A DETOUR.*** Launching the installer on a
> fresh `Test 6` gave ***"Windows cannot access `\\vboxsvr\sdout\sd-setup-W1.0-0.exe`"***
> — not a network fault: `showvminfo --machinereadable | grep SharedFolder`
> returned **nothing** for `Test 6`, `Test 7` **and `Template`**, against three
> mappings on `Test 4`. **The shares were added per-VM to `Test 1`-`Test 5` and
> `Template` never had them, so a clone inherits none.** This file's *"five
> guests, all with three permanent shares"* was true of the guests that then
> existed and is not a property of a new one.
>
> ***THE FIX IS ONE COMMAND, AND THE GUEST MUST BE POWERED OFF*** — a running VM
> is locked and a permanent add fails:
>
> ```
> C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\vm-shares.ps1 -Vm "Windows 11 - Test 6"
> ```
>
> **Ordinary prompt, no elevation.** Done for `Test 6` and `Test 7` on 2 Sep
> 2026, three mappings each. ***AND `-Vm` IS NOW MANDATORY***: it used to default
> to `'Windows 11 - Test 1'`, a guest deleted that morning — but a script that
> **changes VM configuration** should not carry a default at all, because the
> default configures whichever guest it names rather than the one meant.
>
> ***WORTH RULING ON: SHOULD `Template` CARRY THE THREE SHARES?*** It would save
> this step on every clone, and **76's warning does not apply** — that one is
> about priming `Template` with the **OpenSSH capability**, which would leave
> every clone with no ssh question and no firewall restriction. Shared folders
> have no such second effect: they add no capability to the guest and change
> nothing the installer asks. **The owner's call; not done.**
>
> ***THE RIG COUNT IS FIVE, AND ONLY FIVE ARE TEST GUESTS.*** `Test 3`, `Test 4`,
> `Test 5`, `Test 6`, `Test 7` — `Test 1` and `Test 2` were deleted 2 Sep 2026.
> `VBoxManage list vms` returns **seven** entries, and the other two are not
> rigs: **`Windows 11 - Template`** is the clone source (never install on it),
> and **`Beardog`** is nothing to do with this work. **Count the guests, not the
> list** — every MAC is unique either way and nothing collides.
>
> ***WHAT EACH GUEST IS FOR, SO NONE IS SPENT BY ACCIDENT — 2 Sep 2026, END OF DAY.***
>
> | guest | state | shares |
> |---|---|---|
> | `Test 3` | **used**, from earlier work | — |
> | `Test 4` | **used** — SD installed, ssh declined, `zz125` created. 67, 126 and 125's ssh half came off it | yes |
> | `Test 5` | **clean spare**, never installed | yes |
> | `Test 6` | **used** — both boxes unticked; 125's 10162, and 130's three primary sites | yes |
> | `Test 7` | **used** — both boxes unticked; 130's item 1 | yes |
> | `Test 8` | **clean spare**, created 2 Sep, MAC `080027E3DC77` | **yes, added the same day** |
>
> ### ***`Template` NOW CARRIES THE THREE SHARES, SO NEW CLONES INHERIT THEM — 2 Sep 2026, OWNER'S CALL***
>
> Until today every fresh clone came up with **0** mappings — `Test 6`, `Test 7`
> and `Test 8` all did — and that is what the *"Windows cannot access
> `\\vboxsvr\sdout`"* Network Error was on `Test 6`, discovered with an installer
> already open. `Template` was given `sdout`, `xfer` and `gplbld` on 2 Sep 2026,
> so **a clone made from here on arrives ready.** ***CONFIRMED, NOT ASSUMED***:
> `Test 9` and `Test 10`, the first clones made after the change, both came up
> with **3 shares** and distinct MACs (`08002742FD05`, `08002767A08B`) — so the
> inheritance works and the per-clone `vm-shares.ps1` step is retired. **Check a
> new clone anyway if anything looks wrong**, since it costs one line:
>
> ```
> VBoxManage showvminfo "<guest>" --machinereadable | findstr SharedFolderName
> ```
>
> **Three lines means ready. Nothing means run `vm-shares.ps1 -Vm "<guest>"`,
> with the guest powered off.**
>
> ***THIS IS NOT A CRACK IN 76's WARNING, AND THE DIFFERENCE IS THE WHOLE POINT.***
> 76 says do not prime `Template` with the **OpenSSH capability**, because every
> clone would then have **no ssh question and no firewall restriction** at
> Windows' `RemoteAddress=Any` — the priming would change what the installer
> asks and what the guest ends up exposing. **A shared folder adds no capability
> to the guest, changes no `[Tasks]` answer, and alters nothing the installer
> inspects**; it only makes `\\vboxsvr\...` resolve. ***SO: CAPABILITIES NO,
> PLUMBING YES*** — and do not let "we primed `Template` once" become an argument
> for the other kind.
>
> ***DO NOT RUN THE CYCLE WHILE THAT GUEST RUN IS IN FLIGHT*** — it rebuilds the
> `sdout` installer the guest installs from. Cycle first, then the guest.
>
> ***AND THE MAC WARNING DOES NOT APPLY TO THE TEST CLONES — MEASURED 2 Sep
> 2026.*** `Template` is `080027AECE7C` and collides with `sdStandalone-C1`;
> `Test 3` `080027C61086`, `Test 4` `0800271DABE7`, `Test 5` `08002734F731`,
> `Test 6` `080027C3E817` are **all distinct**, so the Test guests can run
> concurrently. They share the computer name `VIRTUAL`, which costs nothing here
> because the shares are host-side.
>
> # ⇩⇩⇩ HANDOFF 13, 2 Sep 2026 — ***THE `Test 4` RUN HAPPENED. 123 AND 124 ARE CLOSED. 67 IS ONE COMMAND SHORT, AND 129 CAME OUT OF THE SAME SCREENS.*** ⇩⇩⇩
>
> ***THE FIRST THING TO DO IS ONE COMMAND ON THE GUEST, AND IT CLOSES 67.***
> `Test 4` is installed, SD is on it, and the ssh boxes were left blank through a
> full install. **Elevated PowerShell on `Test 4`:**
>
> ```
> Get-WindowsCapability -Online -Name 'OpenSSH.Server*' | Select-Object Name, State
> ```
>
> **`NotPresent` closes 67. `Installed` is the finding.** ***DO NOT ACCEPT THE
> CLOSING BOX AS THE ANSWER***: it said *"NO ssh server was installed"*, but
> `SshReport` branches on `SshServerPresentAfterwards` and `install-ssh.ps1` is
> gated on `SshServerWanted` — **the same flag** — so the report and the action
> agree by construction and would agree even if the script had run. The machine
> has to be asked.
>
> ***123 AND 124 ARE WITNESSED AND STRUCK.*** The ssh box rendered **unticked**
> with the cost and the API alternative on its label; the Ready page listed only
> PATH and API with **no ssh line**; the closing box gave *"NO ssh server was
> installed, because you did not ask for one"* and, on the `ApiWanted` branch,
> *"Accounts you gave API access can still sign in over the SD Core API."*
> **The API box was ticked on purpose to reach that branch** — the other one is
> also corrected text but never has to name the API as a route.
>
> ***129 FILED, AND IT IS THE INSTALLER CONTRADICTING ITSELF IN ONE RUN.***
> "Before you install" says ***"scp and sftp STOP WORKING FOR EVERYONE on this
> computer"***; the closing box on the same install says ***"scp and sftp are
> unaffected on this computer."*** The second is true. `DisclosureText`
> (`sd.iss:1663`) is one static string with no parameters, and
> `ApplyAllowGroups:2016` returns having done nothing when there is no server.
> **123 made "no ssh" the common case and this text did not move with it.**
> Also `"the ssh-only model"` at `:1774` is 124's retired premise in compressed
> form, which the lint cannot see because only the long phrase is registered.
>
> ***66 WAS SEEN HAPPENING RATHER THAN READ.*** Owner: *"It is still downloading
> the full screen editors."* It held up the end of the install, and with 123
> making the OpenSSH capability opt-in **it is now the only unbounded download
> left in a default install.**
>
> ### ***`Test 4` IS A STANDING RIG FOR THREE ENTRIES RIGHT NOW — NO ssh SERVER, API ON, SD INSTALLED. DO NOT REUSE IT UNTIL THESE ARE TAKEN.***
>
> **One elevated session on `Test 4` closes 67, 126 and 125's ssh half.** Run
> them in this order — 67's check must come first, before anything could put an
> ssh server on the machine. **Elevated PowerShell on the guest:**
>
> ```
> Get-WindowsCapability -Online -Name 'OpenSSH.Server*' | Select-Object Name, State
> ```
>
> **`NotPresent` closes 67.** Then, still elevated, start SD — an administrator
> lands in SDSYS:
>
> ```
> sd
> ```
>
> and at the `:` prompt:
>
> ```
> ssh.server install
> ```
>
> ***ANSWER `n`.*** **126** is the prompt itself — new message **10163**, naming
> the time cost before committing to the download — and `n` aborts via 10145
> changing nothing. ***DO NOT ANSWER `y`***: that starts the Windows Update
> download this entry exists to warn about, and spends the rig.
>
> ```
> create.account USER zz125 SSH
> ```
>
> **125's ssh half** is message **10161** — it must say the account is set up for
> ssh but this machine has no ssh server, and name what activates it. The grant
> is not refused; that is 125's whole ruling, *warn, do not prohibit*.
>
> ***125's API HALF CANNOT BE TAKEN ON `Test 4`***, because the API is ON there —
> 10162 only fires when `config('APIPORT')` is 0. **That is what `Test 6` is
> for**: install on it with **both** the ssh and API boxes unticked, and then
> `create.account USER zz125b API` gives 10162 while `... SSH` gives 10161, both
> halves in one run. **It also shows the `not ApiWanted` closing-box branch**,
> which `Test 4` did not exercise because the API box was ticked there.
>
> ***67 IS CLOSED, AND 126 AND 125 ARE BLOCKED BEHIND 130 — 2 Sep 2026.*** The
> guest was driven from the host with `keyboardputscancode` and `screenshotpng`,
> no guest credentials, and **the technique works**: chunk the typed line with
> **every backslash sent on its own**, screenshot **before** Enter, put the
> deterministic work in a script on the `xfer` share and have it **write its
> answer back to the share**, so the result is read as text rather than off a
> screenshot. `\\vboxsvr\xfer\a.ps1` arrived intact that way.
>
> ***67 CLOSED ON THE MACHINE'S OWN ANSWER***: `capability :
> OpenSSH.Server~~~~0.0.1.0  STATE=NotPresent`, `sshd service : ABSENT`,
> `sshd.exe : False`, with `elevated: True` and `sd.exe : True` asserted beside
> them so the reading cannot be a failed query or a bare machine.
>
> ***THEN `sd` ON THE GUEST HIT 130 AND THE RUN STOPPED THERE.*** SDSYS has no
> password, 10089 offers *"press Enter on an empty line"* for none, and taking
> that offer **ends the session** (10095, `Connection terminated`). **A password
> has to be set on `Test 4` before 126 and 125 can be taken**, and setting one is
> the owner's to do — not something to be typed from here.
>
> ***`Test 1` AND `Test 2` ARE GONE, CONFIRMED BY THE OWNER 2 Sep 2026.***
> `VBoxManage list vms` shows only `Template`, `Test 3`, `Test 4`, `Test 5`,
> `Test 6`. This file recorded `Test 1` as *"the only machine in the
> uninstall-then-reinstall state"* with *"do not delete it while 120 is open"*.
>
> ***BUT 120's FINDING DOES NOT NEED RE-MEASURING, AND THAT IS THE OWNER'S WORD,
> 2 Sep 2026***: *"I viewed the changes during 120 testing; since the rig does
> not exist, take my word that the test completed successfully."* **He watched
> it on `Test 1` before that guest was deleted.** So the entry's measurements
> stand as written and **nobody should rebuild a rig merely to confirm the
> defect is real** — that would be spending an install plus an
> uninstall-then-reinstall to re-learn what is already attested.
>
> ***WHAT HIS ATTESTATION DOES NOT COVER, AND THE DISTINCTION WILL MATTER
> LATER***: it stands behind the **finding**, not behind any **fix**. When 120
> is built, witnessing the fix still needs a machine that has been through an
> uninstall-then-reinstall with the database kept — because that is the only
> path that produces the state, and `sdsys\bp` and `batch.jobs` are on the
> preserved list either way. **Do not let "120 was attested" become "120's fix
> was witnessed".**
>
> ***`Test 5` IS STILL SEALED*** — `Test 4` is spent as a first-install rig now
> that SD is on it, and `Test 6` exists as of 2 Sep 2026. **Open count 18. Next
> free PRE_RELEASE id: 131.**
>
> # ⇩⇩⇩ RUNBOOK, 2 Sep 2026 — ***(THIS RUN IS DONE; KEPT FOR THE NEXT GUEST.)*** ⇩⇩⇩
>
> ***WHY IT CANNOT BE THE HOST, MEASURED NOT ASSUMED.*** All three witnesses need
> a machine where `SshWasAbsent` is true. The host has `sshd` **Running** and the
> capability **Installed**, so: the `sshserver` task carries
> `Check: SshServerAbsent` (`sd.iss:228`) and is **hidden entirely**, and
> `SshReport` branches on `SshServerPresentAfterwards` =
> `(not SshWasAbsent) or SshServerWanted`, so **the no-ssh paragraph never
> fires**. Making the host qualify means `ssh.server remove`, which is a reboot
> plus a ~19-minute reinstall and is forbidden as a test.
>
> ***AND NOT `Test 1` OR `Test 2` EITHER.*** `Test 1` has ssh Running **and is
> 120's only evidence — do not delete or reinstall it.** `Test 2` had the
> capability re-downloaded during 122's work, so it reads `Installed`.
> ***`Test 3` HAS BEEN USED; `Test 4` AND `Test 5` HAVE NOT.*** Use **`Test 4`**
> and ***keep `Test 5` UNTOUCHED AS THE RETRY***: the moment SD is installed on
> `Test 4` it stops being a first-install-with-no-ssh machine, and 123's witness
> **is** the first-install wizard. A missed screen costs the spare, not a rebuild.
> `Windows 11 - Template` has no OpenSSH capability and is the clone source —
> **do not prime it with one, that is 76's warning**: every clone would then have
> no ssh question and no firewall restriction at Windows' `RemoteAddress=Any`.
>
> ***BEFORE STARTING — DO NOT RUN `cycle.ps1` WHILE THIS IS IN FLIGHT.*** It
> rebuilds `C:\Users\dmont\sdout\sd-setup-W1.0-0.exe`, which is the exact file
> the guest installs from over the `sdout` share, so a cycle **silently swaps the
> installer under test**. The current one is **01:10, 2 Sep**, built by the cycle
> `assert-current` then passed, so it also carries 128 and message 10164.
>
> **On the guest, in an ordinary prompt — the installer asks for elevation
> itself. Reach shares BY NAME, never by drive letter (the letters move):**
>
> ```
> \\vboxsvr\sdout\sd-setup-W1.0-0.exe
> ```
>
> ***FIRST, THE PRECONDITION — A RUN ON A GUEST THAT ALREADY HAS ssh MEASURES
> NOTHING AND LOOKS FINE.*** Elevated PowerShell on the guest, before installing:
>
> ```
> Get-WindowsCapability -Online -Name 'OpenSSH.Server*' | Select-Object Name, State
> ```
>
> **It must read `NotPresent`.** If it does not, that guest is spent — switch to
> `Test 5` and say so.
>
> ### ***WHAT EACH SCREEN MUST SAY, AND THE WORDING THAT WOULD MEAN FAILURE***
>
> | | must read | fails if |
> |---|---|---|
> | **123** the tasks page | the ssh box is **UNTICKED**, and its label carries the time cost (*"downloads from Windows Update … up to about an hour"*) **and** the API alternative (*"can also be reached through the API instead"*) | the box is ticked, or absent (then the precondition was wrong) |
> | **124** "Before you install" | ssh **or over the API** | ***any*** occurrence of *"and nothing else"* |
> | **67** the install itself | **leave the ssh box alone** and let it run | an OpenSSH server appears anyway |
> | **123/124** the closing box | *"NO ssh SERVER WAS INSTALLED, because you did not ask for one … Use SD Core by typing sd as an administrator"* | it claims ssh was limited, or repeats the retired premise |
>
> ***THEN THE ONE CHECK THAT DECIDES 67***, elevated on the guest after the
> install — this is the whole entry, and it is the reason to leave the box alone
> rather than untick and re-tick it:
>
> ```
> Get-WindowsCapability -Online -Name 'OpenSSH.Server*' | Select-Object Name, State
> ```
>
> **Still `NotPresent` closes 67.** `Installed` means a full install still forces
> the server, which is 67 unfixed and is the finding.
>
> **Captures**: the guest writes to `\\vboxsvr\xfer` and they are readable
> directly from `sdxfer` on the host. ***`capture-state.ps1` defaults `-OutDir`
> to `Y:\` and must be given `-OutDir \\vboxsvr\xfer` every time.***
> ***`guestcontrol` STAYS FORBIDDEN — it needs guest credentials. A WITHDRAWAL
> OF THIS RULE WAS WRITTEN AND REVERSED THE SAME HOUR ON 2 Sep 2026, AND THE
> REVERSAL IS THE PART WORTH READING.*** The owner said *"I have had several
> sessions where guest control was used and screenshots were taken
> automatically"*, and I struck the rule in four places on that. **He then
> corrected it himself**: *"it may have not been guestcontrol — I just saw them
> typing and they mentioned getting screenshots so that they could click
> controls."*
>
> ***TYPING PLUS SCREENSHOTS IS THE CREDENTIAL-FREE ROUTE, NOT `guestcontrol`***
> — `keyboardputscancode` to type and `screenshotpng` to see what to click is
> exactly that description, and it is what this file already recommends. **The
> record agrees and is one-sided**: every mention of `guestcontrol` in
> PROJECT_STATUS.md and HISTORY.md is the ban, never a use, and HISTORY.md:7929
> is a session writing down *"HOW THE GUEST WAS DRIVEN, since §7 step 2 forbids
> `guestcontrol`"* — a session documenting that it used the other route
> **because** of this rule.
>
> ***THE LESSON IS ABOUT THE EVIDENCE, NOT THE RULE.*** "Sessions drove the VM
> directly" is true and is the useful fact; *"therefore they used
> `guestcontrol`"* is an inference, and it was mine rather than his. A
> remembered impression of what a past session did is not a measurement of
> which tool it called — the transcripts are, and they say the opposite.
>
> # ⇩⇩⇩ HANDOFF 12, 1 Sep 2026 — ***THE ssh/API THREAD (116-126) IS BUILT, GREEN AND PUSHED. NO CYCLE OWED; ONLY THE RUNTIME WITNESSES REMAIN TO CLOSE THE ENTRIES.*** ⇩⇩⇩
>
> ***EVERYTHING IS BUILT AND SHIPPED.*** 124/115/125/126 were pushed as source and
> cycled clean: the BASIC (`PS_SCRIPTO`/`SSHSRVR`/`REMOTESSH`/`REMOTEAPI`/`CREATEA`/
> `MODIFYA`) BCOMP-compiled, `assert-current` is green, tier-1 all green (fixlist
> 241/0, retired-wording 11/11, check-stale-leads 0). `main` is in sync with
> origin. **No cycle is owed.**
>
> ***WHAT IS LEFT IS THE RUNTIME WITNESS*** — reading each reworded/added path off
> a screen is what moves these from built to CLOSED (compiling is not running).
> Nothing breaks if it waits; the code is shipped. All are installed now:
> **126** — `ssh.server install` on a no-ssh machine now asks before downloading;
> answering n aborts. **124** — the "Before you install" page, the
> `ssh.server remove` prompt (10144), and `SshReport` no longer say "ssh and
> nothing else". **115(b)** — `ssh.server` with no keyword no longer leads with
> `remove-ssh:`. **115(a)** — an acting verb in an elevated `sd.exe` (`remote.ssh
> off` then `on`) shows only its sysmsg, no raw `ssh-firewall:` lines. **125** —
> `create.account USER x SSH` on a machine with no ssh server prints 10161; with
> the API off, `... API` prints 10162.
>
> ***NOTHING OPEN FROM THIS THREAD*** — 126 (the `ssh.server install` time-cost
> prompt, message 10163) is built with the rest; only the runtime witnesses above
> remain, and those CLOSE entries rather than fix anything. ***NEXT PRE_RELEASE
> ID: 127.*** The tier-1 wording lint (`test-retired-wording-units`) now guards
> the retired ssh phrasings (117/121/124) — register a phrase in its `$RETIRED`
> table whenever you retire wording.
>
> ***THE BROADER OPEN LIST, UNCHANGED BY THIS SESSION*** — fixlist open set: 3, 16,
> 28, 65, 66, 67, 70, 74, 80, 89, 93, 96, 102, 112, 113, 114, 115, 118, 120, 123,
> 124, 125, 126. The last five are built-this-session and witness-owed; **118** is
> the untouched one worth a look — an upgrade rewrites `sshd_config` and restarts
> `sshd` having just told the reader it changed nothing about ssh.
>
> ***AND SIX ROWS WERE STALE AGAINST THIS VERY HANDOFF — CORRECTED 2 Sep 2026, NOT
> REBUILT. NOTHING WAS RUN AND NO CODE WAS TOUCHED; THIS IS THE INDEX CATCHING UP.***
> **115, 123, 124, 125 and 126 still read *"not built; wants a cycle"*** while the
> paragraphs above say they were cycled and installed. The rows are the index the
> next session reads, so each now says **built-and-installed, witness owed**, and
> names **where the witness can be taken**: 115 both halves and 124's 10144 prompt
> and 125's 10162 are **host-doable and need no cycle and no guest**; 126, 125's
> 10161 want a **no-ssh guest**; 123 (and 67 with it) wants an **interactive
> wizard**, which a cycle's silent install cannot supply.
>
> ***THE SIXTH IS 89, AND CORRECTING IT MOVED THE DEFECT RATHER THAN CLOSING IT.***
> Its row said Defect A's answer *"is 88's ruling, which is ruled and NOT BUILT"* —
> but **88 was built, witnessed and struck on 1 Sep**. Read from `sd.iss` rather
> than assumed: `ShouldSkipPage:1412` skips the tasks page on `TrueUpgrade`, which
> is `DataTreeUpgrade and SdWasInstalled` (`:1397`), ***so 88 answers Defect A on a
> TRUE UPGRADE AND ONLY THERE.*** After an **uninstall** the key is gone,
> `SdWasInstalled` is false, the page **is shown**, `sd.conf` stays
> `onlyifdoesntexist` over the kept tree (`:573-576`), and `ApplyApiFirewall` still
> runs because `TrueUpgrade` is false — **the firewall moves and the listener does
> not, which is the original defect.** ***THAT IS 120's PATH***, so 89 and 120 want
> looking at together rather than separately.
>
> ***THEN ALL 23 OPEN ENTRIES WERE AUDITED AGAINST SOURCE, 2 Sep 2026, AND ALL 23
> ARE GENUINELY OPEN — NONE IS CLOSABLE.*** Do not re-run this; read it. **Nothing
> built** (grep-confirmed the defect is still there): 16 (msg 2602 still names no
> holder), 28 (no `secure-dumps.ps1`, no `DUMPDIR`), 66 (`install-editors.ps1:137`
> still has no `--version`), 70, 74 (no `Remove-LocalGroup` in `sd.iss`), 96 (no
> `log_message` in `linuxlb.c`/`op_sh.c`), 102's ruling half, 112, 114, 118, 120,
> 80. ***118's PROOF IS WORTH KEEPING***: `sd.iss:3387` gates `ApplyApiFirewall` on
> `not TrueUpgrade` while **`SyncRouteGroups:3394` and `ApplyAllowGroups:3396` are
> NOT gated** — that is the whole defect, in three lines. **Built, witness owed**
> (`assert-current` exit 0, so the install matches source): 67, 113, 115, 123, 124,
> 125, 126.
>
> ***3 WAS REPRODUCED LIVE AND THE CONTROLS ARE WHY IT COUNTS.*** In the installed
> SDSYS voc buckets: `listf` **7**, `count` **20**, `who` **17** — so the method
> finds what is there — and `%L`/`%G`/`%E` **0 each**, while all three are in
> `voc_template` and `newvoc`. `voc_template` is **430**. ***THE FIRST ATTEMPT
> SCORED A FALSE 0 ON EVERYTHING***, controls included, because the live `voc` is a
> **directory of bucket files** (`%0`, `%1`) and grep was pointed at the directory.
> The controls caught it; without them it would have read as a much bigger finding.
>
> ***65 AND 93 SHOW CLEAN RIGHT NOW AND THAT IS NOT A PASS.*** `os.users` holds only
> `don`, the register only `don` and `sdsys` — because the tree is freshly
> installed and **the litter needs a suite run to exist.** Their evidence stands
> from `b84`/`b100`, not from today. The mechanism was confirmed instead:
> `remove-sdaccounts.ps1` removes the Windows accounts and touches **neither**
> `os.users` **nor** `ACCOUNTS`, which is 65's harness half and 93's cause in one
> script. **`DELACC:492` deletes the register record unconditionally**, so the
> product path is not what rots the register — the harness teardown is.
>
> ***115 IS WITNESSED AND STRUCK, 2 Sep 2026, AND DRIVING ITS THIRD VERB IS WHAT
> FOUND 127.*** Owner ran an elevated `sd.exe` on the host: `remote.ssh`,
> `ssh.server` and `remote.api` all reported **without the helper script's name
> in front**, `remote.ssh off`/`on` printed **one line each** with no
> `ssh-firewall:` prose, and a closing `remote.ssh` came back byte-identical to
> the opening one. ***THE THIRD VERB WAS NOT PEDANTRY***: `REMOTEAPI:229-231`
> carries its **own** copy of the strip — identical text, not shared code — so
> the other two passing proved nothing about it. **Two of three is the shape that
> has bitten this project repeatedly**; drive all the copies.
>
> ***127 FILED, AND IT IS THE SECOND "FIX LANDED IN ONE COPY" IN TWO DAYS.***
> `remote.api` printed `action : Show` followed by `before : active=1
> commented=0` — the exact lie `remove-ssh.ps1:85-89` diagnosed and fixed on
> 30 Aug (*"a label that promises a second half has to deliver one"*), in the
> sibling script the fix never reached: **`api-listener.ps1:104` is
> unconditional**. It also records the smaller collision the 30 Aug fix created
> where it DID land — `ssh.server` now prints `state` twice and `sshd.exe`
> twice in a four-line report. ***`test-retired-wording-units` CANNOT CATCH THIS
> CLASS***: it matches retired phrases, and this is label logic. **NEXT FREE
> PRE_RELEASE ID: 128.**
>
> ***113 IS WITNESSED AND STRUCK, 2 Sep 2026, BY RE-RUNNING THE INSTRUMENT THAT
> FOUND IT.*** `gplbld/probe-akwrite.ps1` — **unelevated, `don`'s own account,
> self-cleaning, 18 of 18, exit 0** — issues in its step-5 cleanup the identical
> three deletes that produced the original observation. `DELETE.FILE AKPDIR` and
> `DELETE.FILE AKPDCT`, the two DIRECTORY files that never had an index, printed
> **no `Failed to delete index directory`**, where both printed 2636 before;
> `DELETE.FILE AKPF`, the indexed one, stayed clean as the control. ***USING THE
> ORIGINAL PROBE RATHER THAN A NEW TEST IS THE POINT*** — a test written after a
> fix tends to agree with it.
>
> ***AND THE RETURN-CODE HALF NEEDED NO EXTRA MACHINERY, WHICH IS WORTH KNOWING
> BEFORE SOMEBODY BUILDS SOME.*** 113's sharper half is `@system.return.code`
> being set on a success, and there is no TCL way to print it. At **both** sites
> — `DELETEF:308-313`, `:394-398` — that assignment sits **inside the same
> guard as `display sysmsg(2636)`**, so the two fire together or not at all and
> **the message's absence IS the evidence for the return code.** Reading the
> source decided what the screen had to show; without it this looked like it
> needed a BASIC program written and catalogued to print one variable.
>
> ***`probe-akwrite` IS THE PATTERN FOR A CHEAP WITNESS*** — unelevated, makes and
> removes its own fixture in `don`, asserts `no stray sd.exe session is left
> behind`, needs no cycle, no run token and no elevation. Rostered in
> `assert-current.ps1`, deliberately in neither runner (that wiring is **112**,
> the owner's call). **Open count 22.**
>
> ***ENTRY 3 IS STRUCK AS NOT A DEFECT, AND IT HAD BEEN WRONG SINCE 26 Aug.***
> `voc_template` is a **DIRECTORY file**, so its ids are stored as filenames with
> restricted characters escaped (`op_dio3.c:1346` encodes, `op_dio4.c:1121-1150`
> decodes, tables at `sd.h:114-115`). ***`%E` IS THE FILE FOR RECORD `=`, `%G`
> FOR `>`, `%L` FOR `<`*** — position for position in `*,=><%/+:;?\"` against
> `ACEGLPSVXYZBQ`. There is no record named `%L`, so *"Record not found"* is the
> right answer. **The entry contained its own disproof**: it reported `ct voc =`
> returning `K`/`25` as a separate oddity, and that IS `%E` decoded and present.
>
> ***THE METHOD FAILURE IS THE LESSON AND IT BEAT CONTROLS THREE TIMES*** — 26
> Aug, 28 Aug *"re-validated against the LIVE VOC"*, 31 Aug on a fresh install
> with `listf`/`count`/`who` as controls, **and I repeated it once more today
> before reading the encoder.** The controls were sound and irrelevant: they
> proved the grep could find a record that was there. ***A CONTROL TESTS THE
> INSTRUMENT, NOT THE QUESTION*** — nothing in `listf` passing could reveal that
> `%L` was the wrong string to ask for. When a subject is absent and the controls
> are present, the next move is to check that the subject's NAME is what you
> think it is, not to trust the shape of the result.
>
> ***128 FILED, `B`, AND IT IS WHAT THE DIAGNOSIS WAS ACTUALLY WORTH.***
> `dir_select()`'s decode loop (`op_dio4.c:1140-1147`) discards two characters on
> an unknown `%` escape, and on a **trailing** `%` consumes the string's own NUL
> — `strchr(df_substitute_chars, '\0')` returns that table's terminator, so the
> `!= NULL` guard passes — then walks `p` past the end of `name`
> (`char[MAX_PATHNAME_LEN + 1]`, stack) with `q` writing back into it. **A file
> called `draft%` in any directory file reproduces it, and a user's own `bp` is a
> directory file.** Read, not run. **`sdb64` is byte-identical** at its
> `:1178-1187`, so it is also **UPSTREAM_FIXES 35**. **Open count 22; next free
> PRE_RELEASE id 129.**
>
> # ***THE CYCLE RAN. 127 AND 128 ARE INSTALLED; 128 IS WITNESSED AND OWES ONE RULING; 127's WITNESS IS THE NEXT ELEVATED SESSION.***
>
> ***THE CYCLE IS CONFIRMED RATHER THAN TAKEN ON TRUST***: `assert-current`
> **exit 0**, *"the installed tree matches source"*, log
> `cycle-20260902-003922.log` (626 KB), installed `sd.exe` **`1d908330609d69cd`**
> byte-identical to the built one, and both edited scripts present in
> `C:\Program Files\SD` carrying their new labels.
>
> ***128 WITNESSED, 10 OF 10, UNELEVATED IN `don`'s OWN BP*** — `SELECT BP`
> answered **4 record(s) selected** over four planted fixtures and `LIST BP`
> printed `=` (from `%E`) and `ZZ128PLAIN`. **The discriminator is
> `ZZ128UNK%1` coming back whole**: the old loop would have returned
> `ZZ128UNK`, so this is positive evidence the new branch ran, not merely the
> absence of a crash.
>
> ***AND THE INSTRUMENT'S FIRST RUN WAS VOID, WHICH IS THE CONTROL WORKING.***
> `LIST.ITEM` printed nothing and **the control row failed beside the
> subjects** — that is what said the readout was broken rather than the
> product. Had the control passed while the subjects failed, the honest
> reading would have been a regression. `LIST BP` replaced it.
>
> ***ONE RULING IS OWED ON 128 AND IT IS WHY THE ROW IS NOT STRUCK.*** The same
> transcript ends `'ZZ128TAIL%' not found` / `'ZZ128UNK%1' not found`, because
> `map_t1_id()` re-encodes `%` as `%P`. **The ids are now reported truthfully
> and still do not re-open.** That is strictly better than before on every axis
> — no memory unsafety, no collision, a plain *not found* instead of a silent
> wrong answer — **but whether such a file should instead be SKIPPED (so
> `SELECT` says 2 and never names it) is a behaviour choice, not a defect, and
> it is the owner's.** One line either way.
>
> ***127 IS WITNESSED AND STRUCK, AND 124's 10144 HALF WENT WITH IT — ONE
> ELEVATED SESSION, 2 Sep 2026.*** `remote.api` reads `lines  : active=1
> commented=0` where it read `before :`, with `state` still appearing exactly
> once — which is why the label was NOT copied from the sibling fix.
> `ssh.server` reads `machine sshd.exe=True service=Running …` where it read
> `state   …`, so **`state` appears once where it appeared twice**. *(`sshd.exe`
> still appears on two lines, now scoped by `machine`; improved rather than
> eliminated, and said so in the row.)*
>
> ***124's 10144 PROMPT PRINTED THE CORRECTED WORDING*** — *"sign in over ssh,
> **or over the API** … for an account that has **only ssh** … that is its only
> way in"* — matching `sdsys/messages/10144` byte for byte, and `n` gave 10145
> *"Nothing was changed."* **Host confirmed untouched afterwards**: `sshd`
> Running/Automatic, `sshd.exe` present, firewall `Enabled=True
> RemoteAddress=Any`, identical to the pre-115 reading. ***124 STAYS OPEN ON THE
> WIZARD HALF ALONE*** — the "Before you install" page and `SshReport`, which
> ride 123/67's interactive install.
>
> ***SO THE HOST-DOABLE WITNESSES ARE EXHAUSTED.*** What is left needs either an
> **interactive wizard** (123, 67, and 124's remainder — one run closes three)
> or a **no-ssh guest** (126, 125's 10161). **Open count 21.**
>
> # ***128 IS CLOSED — BOTH HALVES CYCLED, INSTALLED AND WITNESSED, 2 Sep 2026. OPEN COUNT 20.***
>
> `assert-current` **exit 0**, installed `messages/10164` reads `'%1' invalid
> name`, and the witness is **12 of 12** unelevated in `don`'s own BP.
>
> ***THE COMPILE WAS PROVED BY NAME, SEPARATELY AND FIRST.*** `cycle.ps1
> -SkipInstall` logged `Compiling gpl.bp QPROC` then `$QPROC added to global
> catalogue`, with `gpl.bp.out/QPROC` and `gcat/$QPROC` staged — **not inferred
> from a bare `0 error(s)`**. That run is also what would have caught 114's
> hung-compiler case before an install was spent, which is the argument for
> doing the cheap one first on any BASIC change.
>
> ***BOTH ANSWERS CAME OUT OF ONE `LIST`, AND THE CONTROL IS THE POINT***:
> `'ZZ128GONE' not found` beside `'ZZ128TAIL%' invalid name` and
> `'ZZ128UNK%1' invalid name`. **`ZZ128GONE` got into that list because a saved
> list is a snapshot of IDS, not of records** — five were `SELECT`ed and
> `SAVE.LIST`ed, then that one file was deleted from disk, so `GET.LIST`
> restored an id whose record was genuinely gone. That is the ordinary
> stale-saved-list case, not a contrivance, and it is the only clean way to get
> a truly absent id into the same output as the present-but-unusable ones.
> ***HAD `QPROC` BEEN CHANGED TO SAY "invalid name" ABOUT EVERYTHING, THAT ROW
> WOULD HAVE GONE RED*** — asserted in both directions.
>
> # ***(HISTORICAL — THE CYCLE THIS DESCRIBED HAS RUN.) 128's WORDING HALF WAS BASIC AND UNBUILT.***
>
> ***128's RULING WAS GIVEN, WITHDRAWN AND REPLACED WITHIN ONE EXCHANGE, AND NO
> CODE WAS WRITTEN FOR THE WITHDRAWN SHAPE.*** Owner first ruled *"automatic
> conversion of the file name, replace `%` with `_`"*; shown that it makes
> `SELECT` **rename files on disk**, and that the same pass must not touch
> **`%E`/`%G`/`%L` — the legitimate encodings of `=`/`>`/`<`, whose renaming
> would destroy live VOC records** — he withdrew it: ***"drop the rename, do A
> with the 'invalid name' response".*** **Tracing before building is what kept
> that off the disk**; the cost of finding it after a cycle would have been the
> cycle plus a corrupted SDSYS VOC.
>
> ***BUILT IN SOURCE***: `QPROC` separates *"the record is not there"* from
> *"the file IS there under a name this encoding cannot produce"* and reports
> the second with new message **10164** (`'%1' invalid name`). The test is
> **exact, not a guess about `%`** — `ospath(fileinfo(data.f, FL$PATH) : @ds :
> id, OS$EXISTS)` on the failure path only, gated on `is.dir` (`QPROC:512`).
>
> ***AND THE "not found" IT REPLACES WAS NEVER A MESSAGE***: `QPROC:2217` builds
> it as a hard-coded literal, which is why **7304 (`'%1' not found`) has no
> caller anywhere in the tree**. No shared id to break, so 10164 is new and 7304
> is left orphaned as it was.
>
> **BASIC is unbuilt. `-SkipInstall` is the documented cheap compile check, in an
> ELEVATED PowerShell:**
>
> ```
> C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\cycle.ps1 -SkipInstall
> ```
>
> then the full `cycle.ps1` to install it, and the witness is `SELECT BP` over a
> file called `draft%` reading **invalid name**. `test-sysmsg-units` is 44/0 and
> **does not cover 10164** — no verifier names it, same as 10160.
>
> # ⇩⇩⇩ HANDOFF 11, 1 Sep 2026 — ***116, 121 AND 122 CLOSED; A TIER-1 WORDING LINT ADDED. THE HOST IS GREEN AND NOTHING IS OWED.*** ⇩⇩⇩
>
> ***NOTHING OWED — THE HOST IS GREEN.*** Three cycles ran this session; the last,
> **install 20:29:20**, shipped the 122 fix (`gplbld\install-ssh.ps1`) and
> `assert-current` reads *"the installed tree matches source"*. Earlier: 16:55:19
> witnessed the 113/112 build, then **installer 19:18** shipped 121's
> `messages/10148` reword. 121 was then witnessed on guest **`Windows 11 - Test 2`**
> (installed from the 19:18 share installer): `ssh.server remove` printed message 10148 with
> *"running the SD INSTALLER on this machine again … stops rather than guess …
> ssh.server install is NOT affected"* and **no "refuse to install here again"**.
> **116, 121 CLOSED this session; 116 was witnessed on the host, 121 on Test 2.**
>
> ***122 CLOSED*** — `install-ssh.ps1:46` now detects the `UninstallPending`
> state (an earlier `ssh.server remove` staged behind a reboot) and names why the
> re-download is happening, instead of letting a ~19-min FoD re-download look like
> a fresh install of a still-running server. Witnessed on guest `Windows 11 -
> Test 2` (in `UninstallPending`) by running the source script over the `gplbld`
> share; the three explanatory lines printed. The re-download is **inherent** —
> re-adding is the only supported way to cancel a staged removal and a FoD keeps
> no local payload — so it is named, not avoided. **115** (script-prose vs message
> duplication, which 121 grew out of) is the one still open from this thread.
>
> ***NEW TIER-1 CHECK: `test-retired-wording-units.ps1`, 9/9, WIRED INTO CLAUDE.md's
> tier-1 list.*** It scans every message file and shipped script for phrases that
> were deliberately reworded and fails if one reappears in any copy — it named
> `10148` in a second before the reword. **When you retire wording, add the old
> phrase + replacement to its `$RETIRED` table in the same commit.** It caught the
> exact class that cost this session a ~19-min ssh reinstall to find on a screen.
>
> ***122'S OPEN QUESTION IS ANSWERED***: after `ssh.server install` re-downloaded,
> `Get-WindowsCapability … State` read **`Installed`** and `sshd` Running/Automatic,
> so the staged removal was cancelled and the host's ssh survives a reboot. 122 is
> a pure inefficiency, not an illusory restore.
>
> **Tier-1 all green this session**: fixlist **241/0**, verdict 140/140,
> suiteonly 48/48, tiercounts 15/15, sdtestuser 54/0, retired-wording **9/9**,
> check-stale-leads exit 0. ***NEXT PRE_RELEASE ID: 123. NEXT RUN TOKEN: `b101`***
> (no suite ran this session).
>
> # ⇩⇩⇩ HANDOFF 10, 1 Sep 2026 — ***THE VM RUN IS FINISHED. 78, 76, 88, 117 AND 119 CLOSED; 116-120 FILED. ONE CYCLE IS OWED AND IT IS THE FIRST THING TO DO.*** ⇩⇩⇩
>
> # ***START HERE: RUN THE CYCLE. NOTHING BELOW IS IN FLIGHT AND NOTHING IS HALF-BUILT.***
>
> Ended short of credits with **four source changes made after the last build**,
> so `assert-current` **is expected to FAIL right now** — that is the state the
> session left, not a fault. In an **elevated PowerShell**:
>
> ```
> C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\cycle.ps1
> ```
>
> ***WHAT THAT CYCLE IS CARRYING, AND WHY EACH ONE STAYS OPEN UNTIL IT RUNS:***
>
> | | what is unbuilt | what witnessing it needs |
> |---|---|---|
> | **113** | `DELETEF` now tests `OS$EXISTS` before reporting 2636 | **a compile** — nesting was checked at both sites, three `if`s and three `end`s, but *a BASIC change is not verified until it builds* |
> | **119** | six **double**-quoted strings the rename missed | the cycle, then any interactive install |
> | **116** | `remove-ssh.ps1`'s reworded paragraph | ***the expensive one*** — it only prints after a real `ssh.server remove`, so a reboot and a ~19-minute reinstall |
> | **112** | two corrected comments in `VerifyInstall2` | nothing; comments only, step count unchanged at **22** |
>
> **The free tier-1 checks were all green at the end**: `test-fixlist-units`
> 241/241, `test-verdict-units` 140/140, `test-suiteonly-units` 48/48,
> `check-stale-leads` exit 0. **Run those first after the cycle** — they cost
> seconds and one of them has already named in a second what a whole suite run
> was spent discovering.
>
> ***THE CYCLE RAN AT 16:24 AND 117 AND 119 ARE NOW WITNESSED ON A SCREEN.*** Owner
> ran `cycle.ps1`: 640 KB log, all 8 steps, installer 16:24:44, host installed
> **16:25:06**, `sd.exe` `517019EE20D2BD0C`, and **`assert-current: the installed
> tree matches source`**. The rebuilt installer was then run on the guest and
> photographed: caption **`Setup - SD Core W1.0-0`**, heading *"What SD Core
> changes on this computer"*, closing box **"SD Core is installed"**, and the ssh
> box reading **"limited to members of `sdssh`"**. ***116 IS STILL UNWITNESSED AND
> IS THE EXPENSIVE ONE***: its paragraph only prints after a real
> `ssh.server remove`, which costs a reboot and a ~19-minute reinstall.
>
> ***WATCHING THE INSTALL FOUND WHAT RE-READING THE DIFF WOULD NOT.*** The
> progress line still said *"Creating and starting the SD service…"* — **section
> parameters are DOUBLE-quoted and the transform only walked single-quoted
> Pascal strings**, so eight user-visible strings were missed. Six fixed; two
> left with reasons (see 119). **The host is now one build behind source again.**
>
> ***NEXT PRE_RELEASE ID: 121. NEXT RUN TOKEN: `b101`*** (no suite ran this
> session; the install is 16:25:06 and `assert-current` was green at that
> moment, but **six strings changed after it**, so it will now fail until the
> next cycle).
>
> ### ***WHAT THE VM RUN CLOSED, AND THE ONE CORRECTION IT FORCED***
>
> **78** — both `ssh.server` verbs have now run. **76** — the tickbox arrived
> **ticked** on a machine whose rule was already `Any`, which was its last
> untested leg. **88** — both branches witnessed: page **skipped** on a true
> upgrade, **shown** after an uninstall, with the API boxes at their declared
> defaults because the key was gone.
>
> ***AND 74'S "SHOWS AT UNINSTALL" WAS FALSE.*** The four-group paragraph is on
> the **BEFORE-YOU-INSTALL** page, under `WHAT UNINSTALLING DOES NOT REMOVE`
> (`sd.iss:1787`). An interactive uninstall was run looking for it and **no such
> dialog exists**. The naming half is now seen — by scrolling that page — and
> every sentence of it was checked against the uninstall measured minutes
> earlier. **Only "remove the three" is left, and that is the owner's.**
>
> ### ***THE GUEST IS INSTALLED, WORKING AND IDLE — AND CARRIES 120***
>
> `Windows 11 - Test 1` has SD installed (16:04 reinstall), ssh Running,
> confinement re-applied, rule `Any`. **Do not delete it while 120 is open**:
> it is the only machine in the uninstall-then-reinstall state, and rebuilding
> that costs an install plus the ssh remove/reboot/install cycle.
>
> ***120 IS THE FIND OF THE DAY AND IT IS A `B`.*** After uninstall-then-
> reinstall with the database kept, **`sdsys\bp` and `sdsys\batch.jobs` are
> simply not there**, so the hardening reports `code 2` and does nothing — and
> **the two commands the box tells the administrator to run name those same
> missing paths**, so the remedy fails too. `batch.jobs.dic` is the control: it
> exists and IS locked correctly, so the machinery works and this is an absence.
>
> ### ***DRIVING A GUEST — THE THREE THINGS THAT COST TIME***
>
> **`keyboardputscancode` + `screenshotpng` needs no guest credentials**, so
> `guestcontrol` stays forbidden and unnecessary. ***`keyboardputstring` DROPS
> CHARACTERS — IT DROPPED ONE ON A 12-CHARACTER CHUNK***, turning `\\vboxsvr`
> into `\vboxsvr`. **Send each `\` as its own call and screenshot before Enter.**
> ***A CONSOLE THE INSTALLER OPENS FOR ITSELF TAKES NO INJECTED KEYSTROKES AT
> ALL***: three `y`s aimed at `check-install`'s prompt landed in the PowerShell
> window behind it as `y : The term 'y' is not recognized`, and the owner had to
> type it. **Inno's own GUI pages take them fine** — Alt+N, Alt+I, Alt+Y, Alt+F
> and PgDn all worked. **PgDn is how you read a disclosure memo**, and 74 was
> closed by scrolling one.
>
> ### ***THE FILES, ALL READABLE FROM THE HOST***
>
> `C:\Users\dmont\sdxfer` holds captures `01`-`08` and the `leg3*`/`leg4*` logs,
> plus the driver scripts. **They are untracked and a clean checkout loses
> them**; the captures are the evidence behind 74, 76, 88 and 120.


> # ⇩⇩⇩ HANDOFF 9, 1 Sep 2026 — ***LEG 3 IS DONE AND 78 IS CLOSED. THE GUEST IS UPGRADED AND IDLE; LEG 4 IS THE INTERACTIVE UNINSTALL.*** ⇩⇩⇩
>
> ***DO NOT RUN `cycle.ps1` WHILE A GUEST RUN IS IN FLIGHT.*** It rebuilds
> `C:\Users\dmont\sdout\sd-setup-W1.0-0.exe`, and that is the exact file the
> guests install from over the `sdout` share — a cycle silently swaps the
> installer under test. **The source edit below was therefore made and NOT
> built.**
>
> ***THE HOST HAS ONE UNBUILT SOURCE CHANGE AND NOTHING ELSE MOVED.***
> `sd.iss:33` `#define AppName` is now `"SD Core"` (entry **119**, the owner's
> catch: the wizard caption read *"Setup - SD W1.0-0"*). **No cycle, no ISCC, so
> it is unwitnessed** — that is why 119 is still OPEN. The last install here is
> still 12:50:27 with `b100` green in both halves; **next run token `b101`.**
> ***NEXT PRE_RELEASE ID: 120.***
>
> ### ***THE GUEST: `Windows 11 - Test 1`, POWERED ON AND IDLE AT AN ELEVATED PROMPT***
>
> Legs 1, 2 and 3 are done. **SD is upgraded** (second install 15:16→15:22),
> **the ssh server is back, Running/Automatic**, and `check-install` reported
> **every row `[ok]`**. Captures `01`–`05` and five `leg3*` logs are in
> `C:\Users\dmont\sdxfer`, readable directly from the host.
>
> ***LEG 4 IS THE INTERACTIVE UNINSTALL, AND IT IS THE ONLY WAY TO SEE 74.***
> The closing disclosure shows only on the interactive path — a cycle's
> `UninstallSilent` skips it — and it must name **all four** groups: `sdusers`,
> `sdssh`, `sdapi`, `sdsshonly`. **74 is BUILT, UNSEEN.**
>
> ***THEN LEG 4b, WHICH IS THE ONLY REMAINING WAY TO CLOSE 76.*** After the
> uninstall the key is gone, so `TrueUpgrade` is false and **the tasks page is
> shown** — with the ssh rule sitting at **`RemoteAddress=Any`**, which is the
> machine 76's open branch has been waiting for. **Reinstall and look at whether
> "allow remote access" arrives pre-ticked.**
>
> ### ***WHAT LEG 3 BOUGHT — FOUR MEASUREMENTS AND FOUR NEW ENTRIES***
>
> **78 CLOSED.** `ssh.server install` ran **14:52:57 → ~15:12, nineteen minutes**
> and reported **10147**; **10142 never fired**, so remove needs a reboot and
> install does not. The reboot's completion of the staged removal was measured
> too — `sshd.exe` absent, service NOT REGISTERED, capability `NotPresent` —
> which is what makes 10148 true on both sides. **SD's `sshd_config` block
> survived the whole round trip.**
>
> **88 WITNESSED on a true upgrade**: tasks page **skipped**, Ready memo with
> **no task section**, and the firewall gates held — both rules `Any` before
> *and* after. **76's missing "before" reading is now on the record.**
>
> ***THE PREFLIGHT REFUSAL IS RUN RATHER THAN CODE-READ, WITH ITS CONTROL***:
> `CANNOT DETERMINE`/exit 2 in the broken state, `CLEAR`/exit 0 once the
> capability was back. **Take that reading BEFORE `ssh.server install` or it is
> gone** — the entry is 116.
>
> **FILED: 116** (the remove warning names `setup.exe`'s refusal, not
> `ssh.server install` — and 78 and HANDOFF 8 both misread it), **117**
> (`sd.iss:2005` says ssh is limited to `sdusers`; the file says `sdssh`),
> **118** (an upgrade rewrites `sshd_config` and restarts `sshd` one dialog
> after promising it changed nothing about ssh), **119** (above). **115 gained
> the install path**, which moves its cause: `ps_script` discards only the
> captured copy, so the helper's console output reaches the user on every path.
>
> ### ***DRIVING THE GUEST — WHAT WORKS AND THE TWO TRAPS***
>
> **`keyboardputscancode` + `screenshotpng` needs no guest credentials**, so
> `guestcontrol` stays forbidden and unnecessary. Deterministic steps go in a
> script on the read-write `xfer` share and the typed command stays short.
> ***`keyboardputstring` DROPS CHARACTERS — IT DROPPED ONE ON A 12-CHARACTER
> CHUNK***, turning `\\vboxsvr` into `\vboxsvr`. **Send each `\` as its own
> call and screenshot before Enter, every time.** ***AND A NEW CONSOLE THE
> INSTALLER OPENS DOES NOT TAKE THEM AT ALL***: three `y` keystrokes aimed at
> `check-install`'s prompt all landed in the PowerShell window behind it as
> `y : The term 'y' is not recognized`. Harmless, but the owner had to type it.


> # ⇩⇩⇩ HANDOFF 8, 1 Sep 2026 — ***A VM RUN IS PAUSED MID-FLIGHT. `Windows 11 - Test 1` HAS A REBOOT PENDING AND THE SEQUENCE RESUMES THERE.*** ⇩⇩⇩
>
> ***THE HOST IS GREEN AND IDLE. NOTHING IS OWED ON IT.*** Install **12:50:27**,
> `sd.exe` **517019EE20D2BD0C**, `assert-current` **exit 0**, and the full suite
> **`b100` passed both halves** (19 + 22 steps, 753 `[PASS]`, 0 `[FAIL]`, no
> `PARTIAL`). **Next run token `b101`. Next PRE_RELEASE id 116.**
>
> ### ***THE VM: WHERE IT IS AND WHAT TO TYPE NEXT***
>
> Guest **`Windows 11 - Test 1`**, four-leg runbook (78 / 76 / 88 / 74). **Legs 1
> and 2b are done. The guest is powered on with a REBOOT PENDING.**
>
> **State:** full install with **every box ticked** (so `RemoteAddress=Any` on
> both rules, and `addtopath` was selected); SD account `vmtest1` created;
> `ssh.server remove` accepted and **staged behind the reboot** — `sshd.exe` is
> still present and the service still `Running`, which is correct and expected.
> Captures `01-clean` and `02-after-install1` are in `C:\Users\dmont\sdxfer`.
>
> **Resume by rebooting the guest, then, in an ELEVATED guest PowerShell:**
>
> ```
> & \\vboxsvr\gplbld\capture-state.ps1 -Label 04-removed-postreboot -OutDir \\vboxsvr\xfer
> ```
> *(`03-removed-prereboot` was skipped — the helper printed its own before/after
> state in the run itself, which is the same reading.)*
>
> Then `& "C:\Program Files\SD\usr\bin\sd.exe"` → `ssh.server install`.
>
> ***DO NOT DELETE `C:\ProgramData\ssh` BEFORE TRYING THAT INSTALL.*** The
> removal left it in place and warned that **SD will refuse to install here
> again while `sshd_config` is present** without Windows' own copy beside it.
> **Whether that refusal actually fires is worth measuring** — if it does the
> guard works, if it does not the message is overclaiming. Clear the directory
> only after seeing which.
>
> ***`sd` IS NOT ON THE PATH IN A SHELL OPENED BEFORE THE INSTALL.*** Use the
> full path with `&`. A shell opened *after* it should have it, since
> `addtopath` is a task and it was ticked — **that is an untested 89 data point
> worth one command**: `[Environment]::GetEnvironmentVariable('Path','Machine')`.
>
> ### ***WHAT THE VM RUN HAS ALREADY BOUGHT***
>
> **78 is half closed** — `ssh.server remove` ran and did all three things the
> entry demanded: warned (10144) because `vmtest1` existed, asked `(y/<n>)` with
> default no, and said the removal is staged behind a restart (10148), **with
> `before`/`after` state printed in the same run as the evidence**. Only
> `install` is left.
>
> **115 filed** — the three verbs print their helper script's raw diagnostics at
> the user, prefixed `remove-ssh:`, and on the report path that is *all* the user
> gets, so *"is ssh installed?"* is answered by something calling itself
> **remove**. On the `remove` path the same facts are then repeated by 10148 in
> better prose — the duplication `SSHSRVR:77` predicted and thought it had
> avoided.
>
> ***AND A CORRECTION TO MY OWN RUNBOOK, WHICH COST NOTHING BUT WOULD HAVE***:
> the bare `ssh.server` report does **not** print 10147 — that is the INSTALL
> success message. I derived the expectation from the message text instead of the
> code path. **Both entries now say so.**
>
> **80 gained an undocumented behaviour**: `CPROC:1499` folds `-` to `.` when
> resolving a verb, so `create-account` works. Controlled (`clear-select` works,
> `zzz-nosuch` does not, `CT VOC create-account` is not found). The audit must
> decide whether to document it.
>
> ### ***THE RIG, SO NOBODY REBUILDS IT***
>
> **Five guests, `Test 1`–`Test 5`, all with three permanent shares** — see the
> next handoff box for the commands and the drive-letter trap. `sdxfer` on the
> host is where captures land and **they are readable directly**; the guest needs
> to send back only the two screenshots (legs 3 and 4) and raw SD output.


> # ⇩⇩⇩ HANDOFF 7, 1 Sep 2026 — ***102's LOCK HALF DONE AND MEASURED. 114 FILED: THE COMPILER HANGS ON A TYPO.*** ⇩⇩⇩
>
> ***THE MACHINE IS GREEN AND CURRENT. NOTHING IS IN FLIGHT AND NOTHING IS
> HALF-BUILT.*** Cycle **12:49:06 → 12:51:23**, install **12:50:27**, installed
> `sd.exe` **517019EE20D2BD0C** = the 11:24:10 build, `assert-current` **exit
> 0**, `check-datatree-litter` **CLEAN**, and the user table is clean — the three
> orphaned sessions went with the tree.
>
> `VerifyInstall1 -Only verify-txn`: ***PASSED, 9 of 9 decisive, exit 0*** —
> *"commit ends its own level, and a nested commit keeps the parent"*, banner'd
> `PARTIAL, 1 of 14`. **That is the check this edit needed**: clearing
> `commit_txn_id` on the success path sits directly in `op_txncmt`'s commit
> route. `probe-txnlock` **13 of 13** re-run on the fixed binary, which also
> proves the abort path still works **with the new `unlock_txn` inside
> `txn_abort()`** — a function that runs on every abort, not just this one.
>
> ### ***`b100` IS GREEN IN BOTH HALVES — THE FULL SUITE OWED SINCE `b91` IS PAID***
>
> ***UNELEVATED 19 OF 19 + ELEVATED 22 OF 22, EVERY STEP EXIT 0.***
> `VerifyInstall1: every step exited 0.` and `VerifyInstall2: all 22 steps
> exited 0.` — **`PARTIAL` appears 0 times in either half**, which is what
> separates a full run from a targeted one. Ran 12:59:34 → 13:21:02 against the
> 12:50:27 install.
>
> ***753 `[PASS]`, 0 `[FAIL]`, COUNTED WITH THE BRACKETS***, across **505,993
> bytes** of logs from 25 files. **The null-case guard holds**: both counters
> zero on half a megabyte would be a suite that did nothing, and PASS is 753.
> *(Count with the brackets — a bare `FAIL` also matches `verify-fold`'s
> negative-control row, which is a check working correctly.)*
>
> **Read the mixed encodings with `Get-Content`**: the runner's numbered step
> logs and `post-cycle-elevated-*` are **UTF-16LE**, the verifiers' own
> transcripts are **UTF-8 with BOM**. A plain `grep` reports 0/0 on a full log.
>
> ***SPENT: `b100`. USE `b101`.*** ***NEXT FREE PRE_RELEASE ID: 115.***
>
> ### ***THE GREEN RUN LEFT THE ACCOUNT REGISTER 14/15 INVALID — THAT IS 93, MEASURED***
>
> The register held **15 records for `b100`'s accounts and one surviving
> directory**. The Windows accounts were correctly gone; the register was not.
> **Controlled** — `SDSYS` and `don` both still resolve. ***AND NO STEP WENT
> RED***, because nothing asserts the register is internally consistent: the same
> class as 112, and *"the register contains only valid records"* is assertable
> today whichever way 93 is eventually fixed. Entry 93 carries the numbers.
>
> **The 14 profile directories left in `C:\Users` are NOT the same thing and are
> not a defect**: each still has its `ProfileList` entry, **14 of 14**, so that is
> entry 36's pending-reclaim state waiting on a restart, not 83's orphaned
> directory. **They look identical in a directory listing**, which is why it was
> checked before being reported.
>
> ***ONE CYCLE ATTEMPT DIED AT STEP 1 AND THE SECOND WORKED, AND THE SIZE IS THE
> TELL.*** `cycle-20260901-124650.log` is **692 bytes** and stops dead at
> `== [1] Stopping SD` with no transcript end; `cycle-20260901-124906.log` is the
> real one, 640 KB, its step 1 reading `SD is stopped`. **A cycle log in the
> hundreds of bytes is a cycle that never started** — read the size before the
> contents.
>
> ### ***80 NOW CARRIES AN OWNERSHIP TRANSFER, AND THE GAP ANALYSIS HAS A FILE***
>
> Owner, 1 Sep 2026, on `generate_gap_analysis_pdf.py` at the repository root:
> *"That is a file from the other AI's gap analysis which it used to add
> additional documentation. During step 80 you can adopt it and use it as an aid
> in auditing the whole documentation tree, both what you produced and what the
> other AI produced. **You will be allowed to make whatever edits are needed to
> make the documentation speak with one voice and at that point you will own the
> whole documentation tree.**"*
>
> ***THE DIVIDED AUTHORSHIP IS THE DEFECT BEING FIXED***, which is why 80 is one
> task and not a list of corrections. **Entry 80 carries the detail**: what the
> file is (846 lines, a `reportlab` generator whose content is embedded in the
> source, so it is auditable as text), what it renders, and that it **re-runs
> today**.
>
> ***IT IS AN AID, NOT A WORK LIST, AND IT IS ALREADY STALE — CHECKED.*** It
> proposes documenting **`ENCRYPT.FIELD`**, a verb this tree **deleted** (25, 52,
> 53), and treats `LIST.LOCKS` as absent while `list.locks` is a live
> ADMINISTRATOR verb here. Dated **29 Aug**, it predates 56's access model, 78's
> three verbs and everything since. **Validate it against the final image before
> applying any of it.**
>
> ***IT IS UNTRACKED AND 80 RUNS LAST.*** Nothing in the repository preserves it;
> a clean checkout loses the only copy. **Committing it unchanged and unused is
> the cheap insurance** — 38 KB of Python, and the no-binaries rule is about
> build output. **Not done: it is the owner's file and his call.**
>
> ### ***THE VM RIG IS FIVE GUESTS NOW, AND EVERY EARLIER SENTENCE SAYING OTHERWISE IS STALE***
>
> ***`Windows 11 - Test` IS GONE AS "THE ONLY RIG". THE OWNER BUILT `Windows 11
> - Test 1` … `Test 5`, 1 Sep 2026***, all clones of `Windows 11 - Template`.
> **Snapshots are not used** — owner: *"it is quicker to clone the template than
> to do a snapshot"*, which extends 24 Aug's *"CLONE, DO NOT SNAPSHOT"*.
>
> ***CORRECTED 2 Sep 2026 — "FIVE GUESTS, Test 1–Test 5" IS STALE. READ THE LIST
> FROM `VBoxManage list vms`, NEVER FROM THIS FILE.*** Measured that day: `Test
> 1` and `Test 2` are **gone** (120's row already said so) and `Test 6`–`Test
> 10` have been added, so the live set is **`Test 3`–`Test 10` plus `Template`**
> — eight, not five. All eight checked carry the same three `MachineMapping`
> shares. A rig list in a document is out of date the next time somebody clones
> a guest; the hypervisor is the only thing that knows.
>
> ***AND EVERY CLONE REPORTS ITS HOSTNAME AS `VIRTUAL`, WHICH COST TIME ON 2 Sep
> 2026.*** They are clones of one template, so `$env:COMPUTERNAME` is `VIRTUAL`
> on all of them and **a result file cannot say which guest produced it**. Put
> the guest name in the FILENAME and in the text you write, by hand — the
> machine will not do it for you, and a witness that cannot name its own subject
> is worth very little.
>
> ***DO NOT ASSUME A GUEST IS CLEAN — 2 Sep 2026 SPENT TWO ON IT.*** `Test 6`
> looked untouched and held a full SD install, uninstall key and leftover
> `sdu_ZZ125` groups; `Test 5` was picked next and had problems of its own;
> `Test 10` was the clean one. **Check `C:\ProgramData\SD`, `C:\Program
> Files\SD`, the `SD *` uninstall key and `sd*` local groups before starting
> anything**, because a first-install test that begins on a dirty guest is not
> the test it says it is.
>
> ***ALL FIVE NOW CARRY THREE PERMANENT SHARES*** (`MachineMapping`, so they
> survive the reboots leg 2 of the runbook needs), set up on the host 1 Sep and
> **read back from the VM config rather than trusted from the exit codes**, with
> the untouched `Template` as the control:
>
> | share | host | mode |
> |---|---|---|
> | `sdout` | `C:\Users\dmont\sdout` | read-only — the installer |
> | `xfer` | `C:\Users\dmont\sdxfer` | read-write — **results come back as text** |
> | `gplbld` | `…\sd64\gplbld` | read-only — `capture-state.ps1` |
>
> `C:\Users\dmont\sdxfer` **did not exist and was created.** The guests were all
> `poweroff`, which is required: **a running VM is locked and a PERMANENT
> `sharedfolder add` fails on it.**
>
> ***REACH THEM BY NAME — `\\vboxsvr\sdout`, `\\vboxsvr\xfer`,
> `\\vboxsvr\gplbld` — NOT BY DRIVE LETTER.*** Adding a third share moved the
> letters last time; two shares came up `Y:`+`Z:`, one came up `Z:` alone, and
> there are three now. ***IT BITES `capture-state.ps1` SPECIFICALLY***: its
> `-OutDir` defaults to **`Y:\`** and must be overridden with
> `-OutDir \\vboxsvr\xfer` every time. **`guestcontrol` stays forbidden** — it
> needs guest credentials. *(A withdrawal of that rule was written and reversed
> on 2 Sep 2026; the rig section has why, and it is worth reading before
> anyone withdraws it again.)*
>
> **The three commands, written out so this does not depend on a scratch file**
> — run per guest, with the guest **powered off**, then read the result back
> with `VBoxManage showvminfo <vm> --machinereadable | findstr SharedFolder`:
>
> ```
> VBoxManage sharedfolder add "<vm>" --name sdout  --hostpath C:/Users/dmont/sdout --automount --readonly
> VBoxManage sharedfolder add "<vm>" --name xfer   --hostpath C:/Users/dmont/sdxfer --automount
> VBoxManage sharedfolder add "<vm>" --name gplbld --hostpath C:/Users/dmont/Projects/sd4windows/sdb_ai/sd64/gplbld --automount --readonly
> ```
> **No `--transient`** — that form is for a VM already running and locked, and
> these must outlive a reboot.
>
> ### ***THE FOUR-LEG VM RUN, IN ORDER, AND THE ORDER IS THE POINT***
>
> **One guest closes 78 and 76's open leg, answers 88, and witnesses 74.** Each
> leg's end state is the next leg's precondition, which is why it is a sequence
> and not a list:
>
> 1. **Install #1**, ticking ssh **and** "allow remote access" — leaves the rule
>    **open**, which is what leg 3 needs.
> 2. **78** — `create.account` first so `remove` has an account to warn about,
>    then `ssh.server remove` (expect **10144** stranding warning, **10148**
>    reboot-staged) → **reboot** → `ssh.server install` (expect **10142**) →
>    **reboot** → `ssh.server` (expect **10147**). ***`remove` BEFORE `install`
>    IS NOT ARBITRARY***: entry 67 says an SD install always puts the OpenSSH
>    server on, so `install` would be a no-op straight after leg 1.
> 3. **76 + 88 together** — force `remoteip=any`, then install a SECOND time and
>    read the tasks page **before touching it**. Box **ticked** → 76's open leg
>    passes; **unticked** → 88 confirmed and 76's live-rule default is being
>    overridden by `UsePreviousTasks`. **They predict opposite things and one
>    install settles both.**
> 4. **74** — interactive uninstall, screenshot the closing page: all four groups
>    named (`sdusers`, `sdssh`, `sdapi`, `sdsshonly`) with `sdsshonly` called out
>    as the one to remove by hand. A cycle's uninstall is silent, which is why
>    this never gets seen.
>
> **`capture-state.ps1 -Label <n> -OutDir \\vboxsvr\xfer` at every boundary**, in
> an elevated guest shell — it reads `RemoteAddress`, the field a session once
> failed to read and drew a withdrawn conclusion from.
>
> ***67 IS NOT IN THIS BUNDLE.*** Its measurement is already on the record from
> 30 Aug; what is open is the third API-only mode, a ruling and a build.
>
> ### ***102 — WHAT WAS BUILT, AND WHAT IS HONESTLY NOT PROVEN***
>
> `txn_abort()` (`txn.c:389`) now releases `commit_txn_id`'s record locks.
> `k_error` **longjmps**, so the five `goto exit_op_txncmt` in the commit loop
> are **dead code** and `unlock_txn(commit_txn_id)` after the loop was never
> reached; `txn_abort()` tested only `process.txn_id`, which `op_txncmt` zeroes
> at the top. **The fix is on the far side of the longjmp because there is
> nowhere else it can go**, and it is one release rather than five guards so a
> sixth error path is covered without anybody remembering — 101 added two of the
> five in a single day.
>
> ***STILL OPEN AND UNCHANGED***: the level stays counted, the cache stays
> orphaned, the written records stay written. **That is the ruling half.**
>
> ***THE FAULT NOW FIRES ON DEMAND — A FIRST FOR THIS FAMILY.***
> `gplbld/probe-txnlock.ps1` **13 of 13** holds the victim record's file open
> with `FileShare.Read`, so `remove()` is genuinely refused and SD prints
> **`Delete error in transaction commit`**. The session survives the abort and
> the post-`COMMIT` marker is absent, both asserted.
>
> ***BUT THE LOCK STATE IS NOT MEASURED, AND AN EARLIER READING OF IT IS
> WITHDRAWN.*** A positive control settled it: three programs — `READU` then end,
> `READU` then `STOP`, `READU` then `RELEASE` — **all three** reported *"There
> are no active file, read or update locks held by any user"*, **including the
> one that released nothing**. So `LIST.READU` cannot see a held lock from the
> same session after the program ends, and *"no lock after the failed commit"* is
> the **null case**, not evidence. It needs a **second concurrent session**
> watching the first while it lives; that is all that is still owed on the lock
> half. **The fix itself rests on control flow that is not in doubt.**
>
> ### ***114 — A TYPO HANGS THE BASIC COMPILER, AND HUNG COMPILES COST SESSIONS***
>
> `BEGIN TRANSACTION` with **no final `END`** → the compiler **never returns**
> (killed at 41s). **The same source with `END` added** → `Expected TRANSACTION
> after END`, **0.5s**. One line apart. Each hang was killed from outside and
> **left a session slot behind**; three accumulated. The correct block is
> `COMMIT` **inside**, closed by `END TRANSACTION`, then `END`.
>
> # ⇩⇩⇩ HANDOFF 6, 1 Sep 2026 — ***100 CLOSED AND MEASURED. 112 FILED: A VERIFIER NOTHING RUNS. 96 IS A RULING.*** ⇩⇩⇩
>
> ***OPEN COUNT: 18 — 100 STRUCK, 112 AND 113 FILED.*** Open: 3, 16, 28, 65, 66,
> 67, 70, 74, 76, 78, 80, 88, 89, 93, 96, 102, **112**, **113**.
> `check-stale-leads` **exit 0**. **`b99` is spent. Next free run token is
> `b100`.** ***NEXT FREE PRE_RELEASE ID: 114.***
>
> ### ***113 — FOUND BY RUNNING, AND IT IS 104's FIX OVERSHOOTING***
>
> `DELETE.FILE` prints **`Failed to delete index directory`** for every file that
> **never had** one, and sets `@system.return.code` to an error on a delete that
> fully succeeded. **The ordering in the probe's own cleanup is the giveaway**:
> `AKPF`, which *had* a built index, deleted silently and cleanly; `AKPDIR` and
> `AKPDCT`, two DIRECTORY files with no index ever, **both reported failure**.
> `DELETEF:271` reads a non-empty `FL$AKPATH` for an ordinary file and `:287`
> treats "nothing there to delete" as "could not delete". **101 got this exact
> distinction right the same day** by tolerating `ENOENT`. Not cosmetic: a script
> checking the return code of a successful `DELETE.FILE` now sees an error.
>
> ### ***THE STATE, MEASURED***
>
> Cycle **10:52:42 → 10:54:25**, install **10:53:32**, `assert-current` **exit
> 0**, installed `sd.exe` **3DFDB5CEB208E67C** — the hash of the 10:45:33 build,
> so the fix is the binary that is running. `check-datatree-litter` **CLEAN, exit
> 0, 3618 entries**. **Nothing is in flight and nothing is half-built.**
>
> `-Run b99 -Only verify-tierchange`: **28 of 28 decisive checks, exit 0**,
> correctly banner'd `PARTIAL, 1 of 22`. ***A FULL SUITE IS STILL OWED*** and has
> not run since `b91`.
>
> ### ***100 — CLOSED, AND THE PROBE IS WHY***
>
> All seven `get_ak_node` callers test the answer and abort on 0. **Node 0 is the
> AK index header**, so the untested value had the caller write a data node over
> the header every query on that key reads from — reported by `dh_err`, but
> *after* the damage, and nothing re-heals it.
>
> ***THE ENTRY'S GRANTED FIX WAS INSUFFICIENT AS WRITTEN.*** It and UPSTREAM 30
> enumerated **two** of `get_ak_node`'s three failure exits. **The middle branch
> returned a NON-ZERO number on failure** — the head of the free chain, with
> `free_chain` never advanced, i.e. a node the file also believes is free. Seven
> perfect caller-side guards would still have had a hole, so the convention was
> made total inside the function. Filed into UPSTREAM 30.
>
> ***THE MEASUREMENT, BY `gplbld/probe-akwrite.ps1` — 18 OF 18, UNELEVATED.***
> `BUILD.INDEX` over **1900 records (1200 distinct keys + 700 on one key)**:
> `1900 records processed`, the `En` column **N → Y**, and the AK subfile
> **8192 → 49152 bytes**, so the build allocated **40960 bytes = 10 nodes, every
> one through `get_ak_node()`**. The index then answered `SAMEKEY` → **700**
> (past `AK_BIG_REC_SIZE` 3300 — the big-record chain), `K000001` → **1**,
> `K001200` → **1** (past `DH_AK_NODE_SIZE` 4096 — splits and internal nodes).
>
> ***THE PROBE'S FIRST RUN SCORED 15/15 WHILE MEASURING ALMOST NOTHING, AND THAT
> IS THE MOST PORTABLE THING HERE.*** `CREATE.INDEX` **defines an index without
> building it** — `gpl.bp/CREATEI:33`, *"the two commands are identical except
> that MAKE.INDEX automatically goes on to build the index."* So `En` stayed `N`,
> the subfile stayed at header-plus-one-node, and three SELECTs answered
> **correctly off a sequential scan**. **Correct answers from an index that was
> never populated.** The `En` control and a node-count floor sized from the key
> data are what refuse it now. ***ASK WHAT THE RIGHT ANSWER WOULD LOOK LIKE IF
> THE CODE HAD NEVER RUN.***
>
> **Still not seen to fire, as filed**: the guards need an induced write failure
> on an AK subfile. 100 closes on the **101/103/104 shape** — normal path proven
> unregressed *by execution*, fault fixed by reading.
>
> ### ***112 — `verify-vocverbs.ps1` IS RUN BY NOTHING, AND A COMMENT SAID IT WAS***
>
> **It is a step in neither runner, and `verify-tierchange` does not raise it**
> — its only external calls are `Start-Job` and `assert-current.ps1`.
> **`VerifyInstall2.ps1:451` and `:146` say otherwise and are false.** That
> comment is why `-Only verify-tierchange` was handed over as 100's deciding
> step; it ran green and drove **no index at all**.
>
> ***AND WIRING IT IN WOULD STILL MEASURE NOTHING***, for two independent
> reasons: its fixture indexes a file whose **DATA part is empty**, and it uses
> **`CREATE.INDEX`, which never builds**. So the AK write path had **never been
> exercised by anything in the tree**. Fourth instance of the class — 54, 82,
> 107. **`probe-akwrite.ps1` is rostered in `assert-current.ps1` and is in
> neither runner on purpose: wiring it in is the owner's ruling**, as 54, 82,
> 106 and 107 all were.
>
> ***A GPLBLD SCRIPT WITH NO ROSTER LINE TAKES `assert-current` TO EXIT 1*** —
> `assert-current.ps1:818` said so and it is now confirmed rather than quoted:
> the probe was copied in, the tree went red, the roster line was added, and it
> is **exit 0** again.
>
> ### ***100 — WHAT WAS BUILT***
>
> All seven `get_ak_node` callers now test the answer and abort on 0, in each
> function's own idiom. **Node 0 is the AK index header** (`dh_file.c:331` maps
> it there deliberately), so the untested value had the caller write a data node
> over the header every query on that key is read from — reported correctly by
> `dh_err`, but *after* the damage, and nothing re-heals it.
>
> ***THE ENTRY'S GRANTED FIX WAS INSUFFICIENT AS WRITTEN, AND THIS IS THE PART
> WORTH READING.*** The entry and UPSTREAM 30 both enumerated **two** of
> `get_ak_node`'s three failure exits. **The middle branch returns a NON-ZERO
> number on failure** — `new_node_num` is set from `GetAKFwdLink` before the free
> node is read, so a failed read hands back the head of the free chain with
> `free_chain` never advanced, i.e. a node the file also believes is free.
> **Seven perfect caller-side guards would still have had a hole**, so the
> convention was made total inside the function instead. Filed into UPSTREAM 30.
>
> **`:3460` needed a temporary** (`old_root_node_num`) — it assigned straight
> into `node_ptr->node_num`, so a test after the store reads a value already
> committed.
>
> ***STILL NOT EXECUTED, AND THE FIX DOES NOT CHANGE THAT.*** Forcing it needs an
> induced write failure on an AK subfile, which the suite cannot make. It closes
> on the **101/103/104 shape**: normal path confirmed unregressed by the cycle,
> fault fixed by reading. **Do not wait for it to fire.**
>
> ### ***96 — DO NOT BUILD THE FIX ITS ROW RECOMMENDS. IT CRASHES.***
>
> Sized as the second cheap one; traced before writing code, and it is not
> cheap. `log_printf` → `log_message` → `k_error.c:582` `if (sysseg->errlog)`,
> **unguarded**, and `sysseg` is `init(NULL)` (`sysseg.h:138`). **`comlin()` runs
> at `sd.c:175` and `bind_sysseg()` at `sd.c:180`**, so `comlin` → `check_admin`
> → `IsElevated` runs **before shared memory is bound**: the recommended
> diagnostic is a **null-pointer crash at start-up**, on the very `sd.c:838` path
> the row calls "the plainest". `log_printf` also **displays on the user's
> terminal** (`k_error.c:873`) whenever a session is logged in.
>
> ***SO THE SHAPE IS A RULING AND IT IS OWED BY THE OWNER***, three options in
> the row: **(a)** guarded `log_message`, accepting that `sd.c:838` logs nothing;
> **(b)** plus `check_admin` telling the truth on its own `stderr`; **(c)** the
> tri-state, four callers. **Nothing was built.** Two corrections to the row are
> already in it: **nine** undetermined paths not seven, and `op_sh.c:173`'s
> `ENOENT` is the *designed* NO rather than an undetermined one.
>
> ### ***WHAT IS NEXT AFTER THIS, BY COST***
>
> ***THE §5.23 SWEEP FAMILY IS NOW EXHAUSTED EXCEPT FOR RULINGS — 100 WAS THE
> LAST OF IT THAT NEEDED NONE.*** What is left in that family is **102** (its
> **lock release is separable and needs no ruling**; the half-applied-commit
> question does) and **96** above. **93** is a **B**, its shape ruled 1 Sep, and
> **not started** — the largest thing with a clear mandate. **112** is cheap but
> is a wiring decision, so it is his.
>
> So, in order: **102's lock release** (no ruling needed), then **93**, with
> **96**, **112** and **102's ruling** waiting on him.
>
> # ⇩⇩⇩ HANDOFF 5, 1 Sep 2026 — ***6/110/111 AND 101/99/95 ALL CLOSED AND MEASURED. NOTHING IS OWED.*** ⇩⇩⇩
>
> ***OPEN COUNT: 17*** (6, 110, 111, 101, 99, 95 struck this session). **Next
> free run token is `b99`** (`b98` spent below; `b95`/`b96`/`b97` appear in logs).
>
> ***ALSO THIS SESSION, NOT A PRE_RELEASE ENTRY***: `sd.iss:4008` `FileCopy` →
> `CopyFile` (Inno renamed the support function; it warned on every build).
> Verified by `cycle.ps1 -SkipInstall` 10:32 — installer builds clean, warning
> gone, no new Hint/Warning. Build tooling, invisible to users, so no changelog.
>
> ### ***101, 99, 95 — CLOSED ON THE 10:18:45 INSTALL***
>
> The `txn.c` sweep's three cheapest "take the answer" fixes.
>
> | | proved by |
> |---|---|
> | **101** (B) `txn.c:197` bare `remove()` → the twin's `S_IFREG` guard + `-ER_PERM` + `log_permissions_error` + raise 1423 | `verify-txn` PASSED — `op_txncmt`'s commit/nested-commit machinery unregressed. The edit is additive on the FAILURE path only, so the success delete is byte-for-byte unchanged; fault proven by reading + the twin (**103/104** shape) |
> | **99** (M) `APISRVR:1524` takes `K$SET.USERNAME`'s answer, refuses on mismatch (new msg **10160**) | `verify-apiidentity` PASSED 4/0 — `[PASS] the API session writes as the authenticated user`. 10160 installed byte-identical |
> | **95** (M) `dh_file.c` clears `FILE_UPDATED` on success, not before; the two silent failure paths now log | `verify-txn` writes records in a transaction and asserts they landed (a success-path header flush); the bootstrap flushes headers for ~180 programs; `assert-current` exit 0 |
>
> **All three faults need an induced failure the suite cannot make** — a
> `remove()` that fails, an I/O error, a 33-char account — so the verifiers
> confirm the **normal paths unregressed** and the fault fixes stay proven by
> reading, exactly as filed. Two entry claims corrected by measuring: 95's
> "fourteen sites" is **twelve**, and 101's error-path comment "three `goto`" is
> now **five**. `test-sysmsg-units` is **44/0** — it does NOT cover 10160 (no
> verifier names it); 10160 is confirmed by the install.
>
> ### ***THE TRAP THIS BATCH PAID FOR — START-HISTORY COMMENTS AFTER THE BUILD***
>
> I added the required `START-HISTORY` lines to `txn.c`/`dh_file.c`/`APISRVR`
> **after** `make sd`, so those two C files became newer than every binary in
> `bin\`. `assert-current` compares source against the **oldest** binary
> (`sdclilib.dll`), so it refused, and the first `-Run b95` verify aborted on it.
> **`make sd` alone does not fix it** — it only relinks `sd.exe` (whose source
> changed), leaving the other seven binaries older than the edits and still the
> oldest. The recovery was `rm -f bin/*.exe bin/*.dll && make sd` (relink all,
> fresh mtimes) then one more cycle to reinstall, because rebuilding changed
> `sd.exe`'s hash. **Lesson: add the `START-HISTORY` line as part of the edit,
> before the build — the build is the last thing before the cycle.**
>
> ### ***110 AND 111 — CLOSED ON `-Run b94`, INSTALL 09:34:24***
>
> | | |
> |---|---|
> | **110** | `verify-delaccount -Prefix sddelb94` **exit 0, 56 PASS / 0 FAIL**; `[PASS] the data warning preceded it (10158)` on both asserted legs, and 10158 renders on all three delete legs. 10084/10085 unchanged |
> | **111** | `verify-tiers -Prefix sdtiertb94` **exit 0, 35 PASS / 0 FAIL** — **33 before**, so the count itself shows the two new checks ran. Both halves of 10159 asserted separately; the restore leg and the write-once `ACC$PRIOR.TIER` guard still pass |
>
> **`test-sysmsg-units` 44/0**, `msg 10158 matches as rendered (multi-line, 8
> escapes)` — it read **43/1** before the install, so that check is known to be
> capable of failing. `assert-current` exit 0 with **3023** mirrored files
> against 3021, which is the two new messages.
>
> ***THAT WAS A PARTIAL RUN AND IS NOT A PASSING SUITE.*** `-Only` was used
> deliberately; the full suite is still owed at the next milestone, which is
> where regressions in things nobody touched get caught.
>
> ***THE ONE THING NOT MEASURED***: the blank lines between paragraphs as a
> person sees them at a terminal. `Show-Raw` skips empty lines by construction
> and the raw capture double-spaces every break, so **both log views disagree
> with each other and neither is the terminal.** The text and the `%1`
> substitution are measured; the spacing is not.
>
> ### ***110 AND 111 — WHAT THEY ARE***
>
> | | |
> |---|---|
> | **110** | new message **10158**, `DELACC` prints it immediately before the confirmation and **outside the `loop`**, so a mistyped answer does not repeat it. Says the data goes and offers `modify.account x suspended`. The `y/<n>` default of **n** is untouched |
> | **111** | new message **10159**, `MODIFYA` prints it beside 10109/10113 **on the suspend path only**. What is lost (local login, ssh, API, `logto`), what is untouched (the Windows account, its password, its groups, administrator rights included), and what lifts it |
>
> **10159 is not covered by `test-sysmsg-units`**: `verify-tiers` matches with
> `Get-Said` and hand-written regexes rather than `Get-SysMsgPattern`. A wording
> drift there shows up as a visible FAIL on the step, which is the safe
> direction, but nothing checks the pattern against the message file.
>
> ***A TRAP WORTH KEEPING: `cycle.ps1` STOPS ANY TRANSCRIPT ITS WINDOW ALREADY
> HAS OPEN*** (`cycle.ps1:96`, deliberate, and correct). So a wrapper that starts
> its own transcript and then calls it gets **an empty log and a meaningless
> exit 0** — `$LASTEXITCODE` is never set either. **Read
> `%LOCALAPPDATA%\SD-verify\cycle-<stamp>.log`, which is the one that has the
> run in it.**
>
> ### ***ENTRY 6 — CLOSED AND MEASURED***
>
> *"That has been hanging around forever, can we just finish the research and
> fix it?"* — **finished, fixed, and confirmed on the 09:11:07 install.**
>
> ### ***THE CLOSING MEASUREMENT***
>
> `check-datatree-litter` **CLEAN, exit 0, 3611 entries**, against the identical
> measurement finding exactly one on the 00:02:57 install. **Two controls make
> that a result rather than an absence of work:**
>
> | | |
> |---|---|
> | **the operation ran** | `user_accounts\don` created **09:11:32.047**, on this install — so `make_path()` did execute over `C:/ProgramData/SD/user_accounts/don`. A clean scan of a tree where no account was created proves nothing |
> | **it was the fixed binary** | `assert-current` **exit 0**, installed `sd.exe` `82F6FD720D581A42` — the hash of the 08:59:15 build, against `EED6F0D0E11C2239` before it |
>
> **On the old install `don` and `C:` shared a creation tick. Now `don` arrives
> alone.** `gplbld/check-datatree-litter.ps1` stays as the standing check —
> unelevated, read-only, and **it was proved against the litter before it was
> trusted to report its absence.** Not wired into either runner; that is the
> owner's call.
>
> ### ***THE CAUSE — `make_path()` MKDIR'd THE DRIVE LETTER***
>
> `fullpath()` emits `C:/ProgramData/SD/user_accounts/don` for a drive-lettered
> path — `op_dio2.c:1192` has carried that measurement since 21 Aug.
> `make_path()` splits on `DS`, which is `/`, and mkdirs every cumulative
> prefix. **The first prefix is the bare `C:`, and the MSYS2 runtime reads that
> as a relative FILENAME, not a drive** — so it is created in the process's
> current directory, which for `CREATE.ACCOUNT` is SDSYS. Fixed at both copies,
> `gplsrc/op_dio2.c:1537` and `gplsrc/sdidx.c:601`; `make sd` exit 0.
>
> Measured with a standalone MSYS2 probe rather than read: old function litters
> and still builds its target, new function litters not and still builds its
> target, **4 of 4**, and the name the probe makes is byte-identical to the one
> in `sdsys`.
>
> ### ***THE SEVEN SECONDS WAS AN INSTRUMENT FAULT, AND IT IS THE LESSON***
>
> Handoff 4 concluded from the table below that `C:` *"precedes the account
> directory by seven seconds, so it is not made by whatever builds that
> directory"* — **and that is what eliminated the true cause.** The two figures
> were different fields:
>
> | | CreationTime | LastWriteTime |
> |---|---|---|
> | `sdsys\C:` | **00:03:24.957** | 00:03:24.957 |
> | `user_accounts\don` | **00:03:24.957** | 00:03:31.189 |
>
> **Same creation tick to seven decimal places.** `don`'s LastWriteTime advanced
> because VOC, `$hold`, `$savedlists`, `bp` and `cat` were created inside it over
> the next six seconds. One `make_path()` call, microseconds apart.
>
> **It was never adopt-specific either.** Every `make_path()` over a
> drive-lettered path does it; it stops after the first because `stat("C:")`
> then succeeds and the loop skips it — which is also why the mtime never moved,
> the observation that produced "likely adopt-specific".
>
> ***HOW TO EVEN SEE IT: `find . -name 'C:'` AND `Test-Path` BOTH REPORT
> NOTHING***, for two different reasons — MSYS mangles the argument, and a colon
> in a Windows path names an alternate data stream. Its real NTFS name is
> `U+0043 U+F03A`; through the POSIX runtime the same directory reads
> `U+0043 U+003A`. **That is why the checker above exists** — a search by name
> keeps coming back clean, and three sessions believed one.
>
> **The existing litter is not removed by the fix, only never made again.** The
> cycle deletes both trees anyway, so it goes with them.
>
> ### ***THE SIX CLOSED TODAY, AND WHAT PROVED EACH***
>
> | entry | sev | what it was | proved by |
> |---|---|---|---|
> | **94** | **B** | `CREATEA`'s five group adds read `OS.ERROR()`, which had no causal connection to `os_group` | `verify-createaccount` **18/18**, `verify-routes`, `verify-sshonly` |
> | **97** | **B** | two `delete … on error null` sites asserted the delete had happened | `verify-tierchange` — the only verifier matching both 10113 and 10115 |
> | **98** | **B** | `ELEVATION GRANTED` written 85 lines before anything was granted | `verify-sdsysgate` — the only verifier matching `ELEVATION GRANTED` |
> | **103** | M | the truncate's return discarded at six of seven sites | `verify-lineendings` **17/17**, the only verifier driving `openseq` |
> | **104** | M | `DELETE.FILE` orphaned a relocated index and discarded the delete | the cycle's compile; no verifier reaches the path |
> | **105** | M | `verify-apiadmin`'s compile check rested on its disqualifier | red/green against the real `b91` transcript, then `verify-apiadmin` exit 0 |
>
> ***94, 97 AND 98 ARE THE SAME DEFECT THREE TIMES — A FUNCTION'S ANSWER
> DISCARDED*** — which is why they were done as one batch: one cycle, one set of
> `-Only` steps.
>
> ### ***FIVE RULINGS AND TWO CORRECTIONS, ALL FROM 1 Sep 2026***
>
> | | |
> |---|---|
> | **20** | ***RULED NOT A DEFECT — STRUCK.*** Suspend withdraws SD access only and touches Windows not at all, and that is correct; delete is the destructive verb. `MODIFYA:127`, `:856`, `:905-909` are right as written and **are not to be rewritten** |
> | **93** | ***THE SHAPE IS RULED AND IT IS NONE OF THE THREE THE ENTRY OFFERED***: *"there should be NO invalid records in it"* — the requirement is on the FILE, not on any reader. **And the directory goes with the record.** Not started |
> | **110** | **NEW** — `DELETE.ACCOUNT`'s confirmation must say the DATA goes and suggest suspend |
> | **111** | **NEW** — suspending must say what it did *not* do: SD access gone, Windows untouched |
> | **78** | ***NOT UNBUILT — IT IS VM-BLOCKED.*** The code is built and mostly proven; `ssh.server install`/`remove` have never run and want a guest VM. **A marker now says so in its first sentence instead of its last** |
>
> ***TWO OF THOSE ARE CORRECTIONS TO THIS SESSION'S OWN WORK AND ARE WORTH
> READING AS SUCH.*** **20** was briefly recorded as a *confirmed defect* on a
> misreading of a shorter answer, then struck when the owner gave the fuller
> statement — the analysis written for the unwanted fix is kept, labelled, and
> the section heading was struck too (`test-fixlist-units` caught that drift).
> **78** was excluded from the BASIC batch as *"a feature, three new
> administrator commands"* after reading only the opening of a 9,500-character
> row; its own last line said it was VM-blocked all along.
>
> ***AND A QUESTION THE OWNER ASKED THAT IS WORTH KEEPING***: can a suspended
> administrator log in **elevated**? **No** — `LOGIN:625` gates the SDSYS
> landing case on `sd_admin_tier(@logname)`, `SDADMIN:121` returns false unless
> `ACC$TIER` is exactly `ADMINISTRATOR`, so the case never fires and the login
> falls through to an ordinary one where `:687` refuses it. **That gate is
> PRE_RELEASE 91's, closed 31 Aug** — before it, the landing case tested only
> the two Windows keys.
>
> ***OPEN COUNT: 23*** — from `test-fixlist-units`, not by counting headings.
> 28 at the start of the day, six closed, `20` struck, `110` and `111` filed.
> **Next run token is `b94` — measured free, 0 occurrences across every log.**
>
> ***THE COST MODEL WAS CORRECTED BY THE OWNER AND IT CHANGES HOW WORK IS
> SEQUENCED***: *"running cycle is fast, expensive is having to run the full
> verification-suite which should be avoided in favor of running `-Only` when
> possible."* **So do not batch source changes to save cycles** — batch them
> when they are logically related, and hand over the deciding `-Only` step,
> found by grepping the verifiers for what changed. ***`-Run` IS ALSO NEEDED
> UNELEVATED*** for any step in `$needsTestUser` (`verify-nocase`,
> `verify-lineendings`, `verify-logtoaccess`): the account is `sdtu$Run` and
> `VerifyInstall1:634` gates it, so without one the step is dropped **before**
> `-Only` filters and `-Only` then refuses the name and exits 2.
>
> ***THE STATE, MEASURED***: cycle **00:01:56**, install **00:02:57**,
> `assert-current` **exit 0**, `sd.exe` **EED6F0D0E11C2239** (unmoved — 94/97/98
> are BASIC and messages only). **197 of 197 compile units at `0 error(s)`** with
> `CREATEA`, `LOGIN` and `MODIFYA` all in it. `-Run b93` ran **6 of 22 elevated
> steps, all exit 0**, each printing `assert-current` first so none measured a
> stale tree. **New message 10157; next free is 10158.**
>
> ***WHAT IS STILL OWED ON THESE SIX, SAID PLAINLY: NONE OF THE THREE PRODUCT
> FIXES HAS BEEN SEEN TO FIRE.*** 103, 104 and 97 all need an induced failure — a
> read-only file, a mandatory lock, a full disk — and `weofseq` has no verifier
> at all. ***98 IS THE EXCEPTION AND IS THE CHEAPEST THING OWED ANYWHERE***: set
> SDSYS's `ACC$TIER` to `SUSPENDED`, log in as an administrator and read the
> trail. **No induced fault, and it is the one measurement that tells the old
> ordering from the new.**
>
> ### ***THE 31 Aug SUITE HISTORY, KEPT***
>
> ***FOUR RUNS ON 31 Aug. BOTH FAILURES WERE INSTRUMENTS, NOT THE PRODUCT, BOTH
> ARE FIXED, AND THE FOURTH RUN IS CLEAN.*** Nothing found in any of them is a
> defect in SD.
>
> | run | result | what failed | now |
> |---|---|---|---|
> | `b88` 22:03 | stopped at **step 2 of 19**, never handed over | `test-stemcoverage-units` exit 1, naming `sdtc` as a family the litter sweep could not see | **PRE_RELEASE 108, fixed** |
> | `b89` 22:11 | **19 of 19** unelevated, **21 of 22** elevated | `verify-tierchange` step 7 — its 10115 check could never match, whatever the product did | **PRE_RELEASE 109, fixed** |
> | `b90` 22:45 | `-Only verify-tierchange`, **28 of 28**, exit 0, `PARTIAL` | nothing | 109 confirmed on a real run |
> | ***`b91` 22:55*** | ***19 OF 19 UNELEVATED + 22 OF 22 ELEVATED, EVERY STEP EXIT 0*** | ***nothing*** | ***THE GREEN FULL RUN*** |
>
> ***BOTH FAILURES FAILED SAFE, WHICH IS THE PART TO KEEP***: `b88`'s runner
> refused to hand over rather than reporting over the gap, and `b89`'s
> `verify-tierchange` printed the raw SD output beside the verdict, which is the
> only reason the false `FAIL` was readable as one.
>
> ### ***READ THE COUNT BEFORE YOU QUOTE IT — `17` AND `19` ARE BOTH RIGHT***
>
> ***THE UNELEVATED HALF IS `19` STEPS, NOT `17`, AND THIS BOX SAID `17` FOR TWO
> SESSIONS.*** Both numbers are true of different things and the wrong one was
> repeated into PROJECT_STATUS and HISTORY on `0c2cdc0` before anyone measured
> it:
>
> - **`19` is what the RUNNER reports** — every step, and the number to quote.
> - **`17` is `verify-*.ps1` steps only**, which is what PRE_RELEASE 107's
>   arithmetic counts (`17 + 22 = 39` against 44 in the directory). **107 is
>   correct; it just is not counting the same thing.**
> - The difference is the **two `test-*-units` steps**, `test-tiercounts-units`
>   and `test-stemcoverage-units`.
>
> **Measured three ways that agree**: `VerifyInstall1.ps1` names 19,
> `post-cycle-unelevated` lists 19, and `b89` and `b91` each ran 19.
> ***AND THE SUMMARY FILE CARRIES A UTF-8 BOM***, so a `grep '^test-'` over it
> silently misses the first row and answers `1` where the truth is `2` — which
> is exactly how a count like this goes wrong.
>
> ### ***THE TWO STEPS THAT WERE NEW ON `b89` — BOTH GREEN ON `b91`***
>
> | new step | runner | state |
> |---|---|---|
> | `verify-basicfuncs.ps1` | **VerifyInstall1**, beside `verify-txn` | ***PASSED on `b89` and `b91`.*** PRE_RELEASE 106, §5.24 |
> | `verify-tierchange.ps1` | **VerifyInstall2**, after `verify-tiers` | 27 of 28 on `b89` (its own bug), **28 of 28 on `b90`**, ***and green inside the full `b91`*** |
>
> ***TOKENS, MEASURED NOT ASSUMED***: `b88`, `b89`, `b90` and `b91` are all
> spent. **The next full run is `b92`** — check it the way these were, by
> grepping the logs and reading the CONTEXT of every hit, because `b88`, `b90`
> and `b91` all showed hits that turned out to be hex inside SHA hashes.
>
> ### ***THREE ENTRIES FIXED AFTER `b91`, CYCLED AND INSTALLED — 23:42:48***
>
> ***`b91`'S GREEN IS HISTORICAL: IT VALIDATED THE TREE AS AT 22:55 AND SAYS
> NOTHING ABOUT THE CODE BELOW.*** The cycle of 23:41:36 shipped all three and
> `assert-current` is **exit 0** again — `sd.exe` **EED6F0D0E11C2239**, `bin\`
> 23:37:44, install **23:42:48**, `gcat` **133** / `gpl.bp.out` **192**.
> *(§"THE MACHINE"'s 125/184 is a 27 Aug figure and superseded; nothing here
> added a program.)*
>
> | entry | what changed | proven how far |
> |---|---|---|
> | **105** | `gplbld/verify-apiadmin.ps1:306` — a positive `0 error(s)` anchor per probe, count derived from `$probes` | Red/green against the real `b91` transcript; **two false-pass paths closed**. `gplbld` only, no cycle |
> | **104** | `gpl.bp/DELETEF:275`, `:350` — both `dummy = ospath(akpath, …)` now tested, reported with **sysmsg 2636**, upstream's own message that `MKINDX:355` already uses for the same call | ***COMPILES***: the cycle log line 376 `Compiling gpl.bp DELETEF`, `:380` `$DELETEF added to global catalogue`, **and 197 of 197 compile units reported `0 error(s)`** |
> | **103** | `gplsrc/dh_file.c` `SetFileSize` returns the real status; `op_seqio.c` `op_weofseq` and `OPENSEQ … OVERWRITE` set `-ER_IOE` so their existing `k_error` can fire | `make sd` exit 0, **0 warnings, 0 errors**, only `dh_file.o` and `op_seqio.o` rebuilt. **Installed** |
>
> ### ***WHAT IS OWED IS TWO TARGETED STEPS, NOT A SUITE RUN***
>
> ***OWNER, 31 Aug 2026: "running cycle is fast, expensive is having to run the
> full verification-suite which should be avoided in favor of running `-Only`
> when possible."*** **The cycle is the cheap half.** CLAUDE.md already says to
> keep full runs to milestones; this is the cost model behind it, and it means
> **do not batch source changes merely to save cycles.**
>
> **The deciding steps were found by grepping the verifiers for what changed**,
> not guessed: `openseq` appears only in `verify-lineendings`, `DELETE.FILE` in
> `verify-txn` among others, and `105` changed `verify-apiadmin` itself.
>
> ***✅ RUN 23:48:03 AND BOTH PASSED — `PARTIAL, 2 of 19, all exited 0`.***
> `verify-lineendings` **17 of 17** and `verify-txn` **9 of 9**, and each printed
> `assert-current` against **`sd.exe EED6F0D0E11C2239`** first, so they measured
> the NEW binary rather than a stale one. **`verify-lineendings` is the only
> verifier that drives `openseq`** — READSEQ, the 2047/2048 straddle, READCSV and
> all three CRLF writers came back clean, so **103's changed path carries no
> regression.**
>
> ```
> C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\VerifyInstall1.ps1 -Run b92 -Only verify-lineendings,verify-txn
> ```
> ***AN ORDINARY UNELEVATED PROMPT.*** ***`-Run` IS REQUIRED HERE EVEN THOUGH
> NEITHER STEP TAKES A PREFIX***: `verify-lineendings` is in `$needsTestUser`,
> the account is `sdtu$Run`, and `VerifyInstall1:634` gates it on `-Run` — with
> none, the step is dropped from the list **before** `-Only` filters, so `-Only`
> then refuses the name and exits 2. **Confirmed on the run above.**
>
> ```
> C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\VerifyInstall2.ps1 -Run b92 -Only verify-apiadmin
> ```
> ***AN ELEVATED PROMPT — THIS IS THE ONE STILL OWED.*** **`b92` is free for it**
> (its 30 grep hits were two contexts, a GUID fragment and a hex hash) and **is
> deliberately reused across both**:
> the prefix families are disjoint — `sdtu` for the unelevated test account,
> `sdapia` for the elevated step — so neither name is built twice, which is the
> actual rule behind not reusing a token.
>
> ***NEITHER FIX CAN BE PROVEN TO FIRE, AND THAT IS RECORDED RATHER THAN
> GLOSSED***: both need an induced failure — a read-only file, a mandatory lock,
> a full disk — and neither has a verifier. **`weofseq` appears in no verifier at
> all.** The steps above prove the paths still work, not that the new reporting
> triggers.
>
> ***THE "THREE VERIFIERS" CLAIM IN 107 WAS WRONG AND IS CORRECTED HERE.***
> `verify-tierchange.ps1` does **not** raise `verify-acctmsgs` or
> `verify-vocverbs` — it only names them in comments (`:94`, `:120`) as the
> shape it copied. **`verify-doors-admin.ps1` raises `verify-acctmsgs`, which
> raises `verify-vocverbs`, and that chain hangs off `verify-doors-suite.ps1`,
> already a step** (`VerifyInstall1.ps1:550`) — as `VerifyInstall1`'s own header
> says at `:67-68`. **So those two were never orphaned, and ONE verifier was new
> on `b89`, not three.**
>
> **The step counts are settled**: `VerifyInstall1` **17**, `VerifyInstall2`
> **22**, both observed on `b89`. `b85` ran 16 and 21.
>
> ### ***WHAT IS OWED AFTER THE RUN***
>
> **1. THE AUDIT IS ANALYSIS, NOT MEASUREMENT. `98`–`105` ARE ALL `NOT
> EXECUTED`** — read from control flow, and each row says so. The suite does not
> confirm any of them; they need induced faults. ***`98` IS THE EXCEPTION AND THE
> CHEAPEST THING OWED***: set SDSYS's `ACC$TIER` to `SUSPENDED`, log in as an
> administrator, read the trail. It is the only open entry whose trigger needs
> no induced fault at all.
>
> **2. ~~THREE SEVERITY RULINGS ARE HIS AND ONLY HIS.~~ ***RULED 31 Aug 2026:
> THE OWNER RAISED THEM. `97`, `98` AND `100` ARE NOW `B`.*** ** Every
> recommend-**B** in the file has been granted; **each row records the ruling and
> its date in the SEV cell.** ***AND THE LIST IN THIS ITEM WAS SHORT BY ONE***:
> it named `98` and `100`, but **`97` carried a recommend-**B** too** — found by
> grepping the file for the recommendation rather than trusting this box, which
> is the same lesson as the `sdtc` stem two items down. ***THE OPEN `B` SET IS NOW
> EIGHT, GREPPED RATHER THAN COUNTED BY HAND: `65`, `80`, `93`, `94`, `97`, `98`,
> `100`, `101`.*** (`19` is **B** but struck — done, not open.)
>
> ***`101` WAS FILED `B` BY THE AGENT ON ITS OWN JUDGEMENT*** — because its
> trigger is an ordinary state (a read-only file, an ACL denial, a file another
> process holds open) rather than an induced fault, which is the property that
> makes `93` and `94` **B**. **The reasoning is in the row; overrule it there if
> he disagrees.** **Unchanged by the 31 Aug ruling, which raised the other
> three rather than touching this one.**
>
> **3. A GUARD IS OWED AND WAS DELIBERATELY NOT BUILT.** `54`, `106` and `107`
> are the same defect three times: **a verifier in neither runner, found only by
> a person re-deriving counts by hand.** Nothing checks that every
> `verify-*.ps1` is either a runner step or a named child. **A tier-1 unit test
> would catch it, needs no install and no elevation, and would have caught all
> three.** It is recorded in `107` rather than written, because it is a new
> instrument and the session ended.
>
> ### ***STATE***
>
> ***NOTHING IS IN FLIGHT. NO PRODUCT SOURCE CHANGED THIS SESSION.*** Everything
> is documentation, two new `gplbld` files, and step rows in the two runners —
> **no `gplsrc`, no `gpl.bp`, no `sd.iss`.** `assert-current` passed at the end
> and the install is the 13:33:28 one. `git status` shows only the owner's
> untracked `generate_gap_analysis_pdf.py`; **leave it alone.**
>
> **The six §5.23 sweeps are DONE** — the box below is kept for its numbering
> and its three lessons, which are worth more than any single entry. **Open
> entries: 28**, from `test-fixlist-units` rather than by counting headings.

> # ⇩⇩⇩ HANDOFF 2, 31 Aug 2026 — OUT OF CREDITS AGAIN. NEW ACCOUNT. THE AUDIT IS THE WORK. ⇩⇩⇩
>
> ***READ §5.23 FIRST. IT IS THE OWNER'S RULING AND IT IS WHAT EVERY OPEN ENTRY
> BELOW IS MEASURED AGAINST:*** a query must never answer wrongly, and *"this is
> a database application — no failure is more severe than misreported data, not
> just to the administrator but for every user."*
>
> ***NOTHING IS IN FLIGHT. NO SOURCE CHANGE IS UNCOMMITTED OR UNBUILT.*** The
> last commit touching anything outside the four documentation files is
> **`a02fbf4`** (`verify-tiers.ps1`). Everything after it — 93, 94, 95, 96, 97
> and §5.23 — is documentation. `git status` shows only an untracked
> `generate_gap_analysis_pdf.py`, which is **the owner's, not this work's**;
> leave it alone.
>
> ### ***THE VERIFICATION DEBT, WHICH IS THE POINT OF THIS BOX***
>
> **1. THREE FILED ENTRIES ARE `NOT EXECUTED` AND SAY SO IN THEIR OWN ROWS.**
> They are read from control flow against their callers, which is honest
> analysis and is *not* a measurement. Each row names what would force it:
> * **95** — `dh_flush_header` clears `FILE_UPDATED` before it can fail. Needs an
>   **induced write failure**. `dh_close.c:45` is the case that does not
>   self-heal.
> * **96** — `IsAdmin`/`IsElevated`/`os_permitted` answer "no" and "could not
>   tell" with the same `FALSE`. Needs an **induced name-service failure**; on
>   Cygwin an unreachable domain controller is the realistic route.
> * **97** — `MODIFYA:1442`/`:1445` assert a removal from a discarded `delete`.
>   Needs an **induced delete failure** (lock or permission).
>
> **94 IS THE EXCEPTION AND IS CONFIRMED BY EXECUTION** — probe run 31 Aug, in
> `don`'s own `bp`, unelevated, removed afterwards. Do not re-prove it.
>
> **2. `verify-tiers.ps1` HAS NOT RUN SINCE IT CHANGED.** `a02fbf4` added the
> missing `os.users` disclosure to `Remove-Made`. ***PARSE-CHECKED CLEAN 31 Aug
> — 0 errors, 9 functions found, no BOM past offset 0*** — so it loads, per the
> "verify a script loads" rule. **It has not been executed.** Run it.
>
> **3. ***THE FULL SUITE IS OWED AND ONLY THE OWNER CAN RUN IT.*** The last full
> run is **`b85`**; `b86` was `-Only verify-doors-suite`. CLAUDE.md requires a
> full run **before a handoff**, and §4.0.1 forbids the agent running
> `VerifyInstall1`. **This hand-over is going out without it. Say so rather than
> treating b85 as current.**
>
> ```
> C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\VerifyInstall1.ps1 -ThenElevated -Run b87
> ```
> ***An ordinary unelevated prompt*** — it elevates the second half itself.
>
> ### ***RULINGS OWED BY THE OWNER — DO NOT DECIDE THESE ALONE***
>
> * **97 → recommend B.** Filed **M** on its trigger only. *"A privilege removal
>   reported as complete when it did not happen"* is the class the 93 ruling
>   named; the row says so and leaves the lever with him.
> * **65 → B was an inference**, flagged in its own row. Confirm it.
> * **67, 89, 88, 20** are listed as *candidates, my reading* in §5.23's triage
>   table and have never had his eye on them.
>
> ### ***DO NOT RE-FIND THESE. ALL FOUR LOOKED LIKE DEFECTS AND ARE NOT.***
>
> * **`_WRITEV:50`/`:51`** — the same `write … on error null` as 97's sites and
>   **correct**. `op_dio3.c:921` hands `process.status` to the caller and `:923`
>   raises 1408 when it is negative and the caller had no `ON ERROR`;
>   `write_record` sets it (`:357`). It suppresses the *inner* abort so the
>   *outer* opcode can decide. **This read as a defect with a blast radius of
>   every `WRITEV` statement** (`pcode_bld.py:83` confirms `_WRITEV` is what
>   `op_writev` recurses into) before the status path was traced.
> * **`DELACC:499`** — third `delete … on error null`, and **asserts nothing**.
>   Its banner: a missing record is the ordinary case, no message either way.
>   The message is the entire difference between it and `MODIFYA:1442`.
> * **`win32s4u.c` / `ImpersonatingUser()`** — already fixed by an earlier
>   session; it asks Windows, and `K_IMPERSONATING` returns **both** fields so
>   the two can visibly disagree. `RevertUserIdentity` has no caller **by
>   design** (`op_kernel.c:286`).
> * **`CREATEA:1882`, `MODIFYA:440`, `:472`** — all take `os_group`'s return and
>   branch on it. `:1882` is **in the same file as 94's five defects**, which is
>   why 94 is an outlier rather than a convention.
>
> ### ***THE SWEEPS — WHAT IS DONE AND WHAT IS NOT, WITH SIZES***
>
> **The method, once, because every sweep below uses it:** find the sites
> mechanically, **exclude comment lines**, then read what gates each one.
> ***EXCLUDING COMMENTS IS NOT OPTIONAL*** — 94's first pass scored `CREATEA:823`
> OK by matching an `os.execute` inside a `* was:` comment, i.e. it cleared the
> very site whose comment recorded the change. And per the instrument rules, a
> sweep that could have matched nothing must **say so**: print the site count and
> refuse a zero.
>
> ***DONE — do not repeat these:***
> * `OS.ERROR()` across `gpl.bp` — 14 sites, 5 defective (**94**), 9 correct.
> * `gplsrc` identity/privilege — `IsAdmin`, `IsElevated`, `os_permitted`,
>   `win32s4u.c`, `op_kernel.c` (**96**, plus the clean results above).
> * `gplsrc` persistence write/close returns — one discarded call in the whole
>   file layer (**95**); 14 sites check their writes.
> * `on error null` across `gpl.bp` — **all 11 sites classified** (**97**; three
>   are reads, `_WRITEV`×2 and `DELACC:499` cleared above).
> * `sysmsg` success-assertions, **`10xxx` range only** — ours and port-era.
> * ***the `void <fn>(…)` sweep across `gpl.bp` — 84 non-comment sites, not the
>   77 this box estimated. 2 defective (**98**, **99**), 5 already filed (**94**),
>   77 correct.*** Done 31 Aug 2026. **The count was measured, not carried over**;
>   the sweep printed it and refused a zero, and 0 false positives survived a
>   check for `void` inside a trailing `;*` comment or a string literal.
>
> # ✅ ALL SIX SWEEPS ARE DONE — 31 Aug 2026. EIGHT ENTRIES, 98 TO 105, AND FIVE UPSTREAM.
>
> ***THE AUDIT §5.23 CALLED FOR IS COMPLETE. NOTHING BELOW IS OWED ANY MORE***;
> the six items are kept with their numbers and their original text because
> every entry cites *"sweep N of the six"*. **What is still owed is
> VERIFICATION, not analysis** — see the debt box above, which the audit did not
> reduce: **every one of 98–105 is `NOT EXECUTED`**, read from control flow, and
> the full suite is still the owner's to run with `b85` still the last one.
>
> | sweep | product |
> |---|---|
> | 1 `void <fn>()` | **98**, **99** — 84 sites, not 77 |
> | 2 `dh_ak.c` | **100** + UPSTREAM 30 — the worst found; no self-heal |
> | 3 `txn.c` | **101** (the only **B**), **102** + UPSTREAM 31, 32 |
> | 4 `status()` | **103** + UPSTREAM 33 — *the specified sweep was clean* |
> | 5 `sysmsg` upstream | **104** + UPSTREAM 34 — *the specified sweep was clean* |
> | 6 the verifiers | **105** — the archetype was already fixed |
>
> ***THREE LESSONS WORTH MORE THAN ANY SINGLE ENTRY.*** **(a) SIZE BY THE
> OPERATION, NOT THE KEYWORD** — sweeps 4 and 5 found nothing where they were
> pointed and everything one family over. **(b) VERIFY THE CLAIM THE NEGATIVE
> RESULT RESTS ON** — "a bare `write` aborts loudly" was inherited from this box
> and had to be proved (`op_dio3.c:650`, `:436`) before 123 sites could be
> called safe; proving it once made sweep 5 cheap. **(c) GREP THE RECORD BEFORE
> FILING, NOT ONLY BEFORE RUNNING** — `3312` and `6686` both read as port gaps
> and are both deliberate removals already recorded (§"SDNet is gone", §5.19).
> **Two false entries avoided by a grep that cost seconds.**
>
> *(Original heading and items follow, unchanged.)*
>
> ***NOT DONE, IN THE ORDER I WOULD RUN THEM. THE NUMBERS ARE STABLE — 1 IS DONE
> AND KEEPS ITS NUMBER, BECAUSE 98 AND 99 BOTH CITE "SWEEP 1 OF THE SIX".***
>
> **1. ✅ THE `void <fn>(…)` SWEEP ACROSS `gpl.bp` — DONE 31 Aug 2026. 84 SITES,
> NOT 77. TWO DEFECTS: 98 AND 99.** ***BOTH ARE THE SAME MECHANISM AND IT IS NOT
> THE ONE THIS BOX PREDICTED.*** The prediction was 65/72/94's shape — a status
> discarded and the caller re-deriving it from something that does not know.
> **What the other 79 sites actually hold is a kernel call whose return is an
> informational echo**, and discarding those is correct. ***THE DEFECT IS THE
> NARROWER CASE WHERE THE RETURN IS THE DESIGNED AND ONLY REPORT OF A REFUSAL***
> — `K_ADMINISTRATOR` (`op_kernel.c:395`) and `K_SET_USERNAME` (`:257`) each set
> a flag or a name **only** behind `HDR_INTERNAL`, then answer with the state as
> it actually stands, under a comment saying a refusal is deliberately not an
> error. **Four sites take that answer and throw it away**: `LOGIN:718`,
> `CPROC:2848`, `CPROC:2860` (98) and `APISRVR:1524` (99).
> ***THE CLASSIFICATION, SO NOBODY RE-READS 84 LINES:*** 41 `kernel` — 18
> `K$AUDIT` (returns 0 always and says so, `op_kernel.c:652`), 11
> `K$SUPPRESS.COMO`, 5 `K$SET.OPTIONS` (no result assigned, so 0), 4 echoes
> (`K$TERM.TYPE`, `K$CPROC.LEVEL`, `K$AUTOLOGOUT`, and `K$SET.USERNAME` = 99),
> 3 `K$ADMINISTRATOR` = 98; 12 `qdisp` and 6 `bindkey` and 3 `@(0,0)` — display
> layer, and `QD$INIT` **is** checked at `QPROC:696`; 6 `ospath` — 4 cache
> flushes and 2 deletes, both litter-only (`CREATEA:1593` is the one-shot ADOPT
> marker and is deliberately removed twice, banner at `:1570`); 5 `os_group` =
> **94, already filed**; 4 `SDCLIENT`; 2 `fcontrol`; 2 `elevate`; 1 `iconv`;
> 1 `selectinfo` (a documented side-effect call, `QPROC:684`); 1 `pterm`.
> ***THE HOUSE-CORRECT IDIOM IS IN THE TREE TWICE AND IS WORTH COPYING***:
> `SDCLIENT:955` `void write.socket(…)` then `return (status() = 0)`, and
> `INLINE:411` `void iconv(s, conv.code)` then `if status() = 0 then exit`.
> **Discarding the value while reading the status is not the defect; discarding
> both is.**
>
> **2. ✅ `dh_ak.c` — DONE 31 Aug 2026. ONE DEFECT, 100, AND IT IS THE WORST FOUND
> BY ANY OF THE SWEEPS SO FAR.** ***THE FILE IS WELL CHECKED INTERNALLY AND THAT
> IS WHY THE ONE GAP MATTERS***: `update_internal_node`, `free_ak_node`,
> `free_ak_big_rec`, `ak_clear` and `delete_ak` are all called as
> `if (!fn(…))` at every site — **53 call sites swept, and the house habit is to
> test.** `get_ak_node` is the exception: it returns **0 for failure**, says so
> explicitly at `:2716`, and **not one of its seven callers asks**. `dh_file.c:331`
> maps node 0 to `offset = 0`, which is the AK header, so the failure path writes
> a data node over the index header — **the only entry in this audit with no
> self-heal**, which is the argument for raising it above 95's **M**.
> ***CLEARED, SO NOBODY RE-FINDS THEM***: `ak_delete` returning `void` is
> **correct** — it reports through the global `dh_err`, which `:192` copies to
> `process.status`, and upstream is identical; and the three lesser discards
> (`:2702`, `:3707`, `:3913`) **leak space rather than answer wrongly**, which is
> stated in 100's row so they are not re-filed as accuracy. ***ALL OF IT IS
> UPSTREAM'S***, byte-identical at `ae0cc5f` — **`UPSTREAM_FIXES.md` 30**, filed
> the same day, because a defect in both trees goes in both files.
>
> **2b. THE PREDICTION IN THIS BOX WAS RIGHT ABOUT THE FILE AND WRONG ABOUT THE
> MECHANISM.** It expected a silent index update failure. **The update paths are
> not silent** — `dh_err` reaches `process.status` on every one of them. What is
> wrong is the *order*: the error is reported **after** the header is overwritten,
> so the caller is correctly told about a failure that has already been made
> permanent. **Ask "when is it reported", not only "is it reported".**
> ***THIS IS THE ONE THAT MOST DIRECTLY OWNS §5.23'S RULING.*** An alternate key
> index that silently fails to update does not corrupt a record — **it makes
> `SELECT`, `LIST` and every query built on that key return the wrong rows**,
> which is *"an administrator receiving an answer that is wrong"* in its purest
> form, and for every user rather than only an administrator. **95 was found in
> `dh_file.c`, its neighbour, by exactly the question to ask here:** is a status
> discarded, and is state updated as though the work succeeded?
>
> **3. ✅ `txn.c` — DONE 31 Aug 2026. TWO DEFECTS, 101 AND 102, AND 101 IS THE
> FIRST `B` ANY SWEEP HAS PRODUCED.** ***THE FILE IS OTHERWISE CLEAN AND THAT WAS
> CHECKED, NOT ASSUMED***: `dh_write`, `dir_write`, `dh_delete` and all three
> `alloc_txn` sites are tested, and `dh_fsync`, `dio_close`, `unlock_txn` and
> `suspend_updates` are all **`void`** — there is nothing to discard. **`rollback()`
> is clean by design**: nothing is written before commit, so it has no operation
> that can fail. ***THE ONE DISCARDED STATUS IN THE WHOLE FILE IS `remove(path)`
> AT `:197`*** — and the contrast is one `switch` wide, because the other three
> arms of the same `switch` all test their operation and raise 1422 or 1423.
> **101 is filed `B` on the trigger**: unlike 95, 96, 97 and 100 it needs no
> induced fault, only a read-only or open file, which puts it with 93 and 94.
> ***102 IS ENTRY 11's LEFTOVER AND THE REASON IT NEEDED FINDING AGAIN IS A
> FILING ONE.*** 11 says *"filed here rather than guessed at"* and `txn.c:249`
> says *"it is filed rather than fixed here"* — **but 11 is `~~11~~`, struck, so
> nothing open tracked it and `test-fixlist-units` counted it closed.** The
> header of PRE_RELEASE_FIXES.md already warns about exactly this: *"read the
> table, never the section headings."* **A live defect in a closed entry's prose
> is invisible to the thing that decides what ships.** *(New in 102 and not in
> 11: `k_error` `longjmp`s rather than returning, so `unlock_txn` is skipped and
> **every record lock is held for the life of the process**.)*
>
> **3b. `system(1008)`/`txn_depth` IS ALREADY FILED UPSTREAM AND WAS NOT
> RE-FOUND** — `UPSTREAM_FIXES` 17, and §5.23's table entry for 11 covers it.
>
> *(The original note follows.)* Entry **11** (nested `commit` silently
> losing the outer transaction's writes, **DONE**) came out of here and is proof
> the class lives in this file. Nothing else in it has been swept. **Silent loss
> on commit or rollback is the corollary's worst case.**
>
> **4. ✅ DONE 31 Aug 2026 — AND THE SWEEP AS SPECIFIED CAME BACK CLEAN. THE ONE
> DEFECT, 103, IS ONE KEYWORD FAMILY OVER.** ***READ THIS BEFORE SIZING SWEEP 5
> OR 6 — IT IS THE REUSABLE LESSON.*** **150 `write`/`delete`-family sites, not
> 129, and not one is a new defect.** 123 bare, 18 with a real `on error`, 5
> `on error null` (**97's**), and the 4 that looked like `then`/`else` are bare
> `delete`s inside an `if … then`. ***THE "BARE ABORTS LOUDLY" CLAIM WAS
> VERIFIED, NOT INHERITED, BECAUSE THE WHOLE NEGATIVE RESULT RESTS ON IT***:
> `op_dio3.c:650` raises 1406 and `:436` raises 1405 when `P_ON_ERROR` is unset,
> and `k_error.c:31` makes both fatal. **The 18 handlers are exemplary** — 13
> print `status()` and `stop`, and 5 set a flag read on the very next line.
> ***THAT FLAG IDIOM IS THE HOUSE-CORRECT ANSWER TO `on error`***
> (`CREATEA:1172`→`:1175`, `MODIFYA:763`→`:780`, `:1049`→`:1051`,
> `:1419`→`:1422`, `CRED_SET:167`→`:181`) and is what a fix elsewhere should
> copy.
>
> **4b. WHAT THE DEFECT ACTUALLY WAS, AND WHY THE FRAMING MISSED IT.** The box
> sized this sweep by `write`/`delete`, and `gpl.bp` handles those correctly
> everywhere. **The truncate family is where it goes wrong**: `chsize64` has 7
> call sites, **6 discard the return and 1 checks it** (`sdfix.c:2493`, the
> control). `dh_file.c:831` is the archetype — `bool SetFileSize(…) {
> chsize64(…); return TRUE; }`, **a status-typed function that cannot fail
> because it does not look**, so `dh_clear` could not check it even if it tried.
> `op_seqio.c:1542` and `:803` are the ones that answer wrongly: **`WEOFSEQ` and
> `OPENSEQ … OVERWRITE` leave the old tail and report success**, and
> `QPROC:673` is `weofseq csv.f`, so a CSV export can carry rows from a previous
> longer run. ***SIZE THE NEXT SWEEP BY THE OPERATION, NOT BY THE KEYWORD.***
>
> *(The original note follows.)* **`status()`-never-checked — 129 bare `write`/`delete`
> statements against 275 `status()` references.** The inverse of sweep 1: not a
> discarded return, but an operation whose status **nobody reads**. ***MIND THE
> TWO LEGITIMATE PATTERNS BEFORE FILING ANYTHING***: a **bare** `write`/`delete`
> with no `on error` and no `then`/`else` **aborts loudly** via
> `k_error(sysmsg(1406)/(1405))` (`op_dio3.c:650`, `:435`) and is *safe*; and
> `on error null` is correct where an **outer** opcode reads `process.status`,
> which is exactly why `_WRITEV` is not a defect. **The defect is only where the
> status reaches nobody and an assertion follows.**
>
> **5. ✅ DONE 31 Aug 2026 — ALL 22 SUCCESS-ASSERTIONS IN THE NAMED RANGES ARE
> CORRECTLY GATED. NOTHING FILED FROM THE SWEEP'S OWN TARGET; 104 WAS FOUND IN
> PASSING.** ***THE UPSTREAM RANGES ARE IN BETTER SHAPE THAN THE `10xxx` ONE,
> WHICH IS THE OPPOSITE OF WHAT THE BOX EXPECTED*** — the port-era range gave
> **94**, and Ladybridge's gave nothing. **23 assertions identified from the
> message texts, 22 with call sites**, all gated: `6136`/`6137`/`6141` on
> `ospath(…, OS$DELETE)` with 6138/6142 on the else; `6153`/`6155` on
> `osrename` with 6154/6156; `6158`, `6194`, `3029`–`3031`, `3038`–`3042`,
> `3221`, `3251`, `6189`/`6190` all behind either an `on error … stop` or a
> **bare** `write`/`delete` — **which sweep 4 verified really does abort.** *That
> verification is what made this sweep cheap, and it is why the two sweeps
> belong in this order.*
>
> **5b. TWO THINGS READ AS DEFECTS AND ARE NOT. DO NOT RE-FIND THEM.**
> * ***`AUTOLOGOUT:52` PRINTS 2500 "Autologout period set to %1" AND THE
>   `void kernel(K$AUTOLOGOUT, period)` IS AT `:58`, SIX LINES BELOW.*** It
>   looks exactly like **98**'s assert-before-do and it is not: `:52` is in the
>   **query** branch (`token.type = PARSER$END`), reporting
>   `kernel(K$AUTOLOGOUT, -1)`, and **the set branch prints nothing at all.**
> * ***`DELETE:178` HAS ITS `delete` AND ITS `on error` ON SEPARATE LINES***,
>   which reads like a bare delete followed by a dangling clause. **It is a real
>   continuation** — the same idiom appears 8 times across `APISRVR`, `ED` and
>   `_WRITEV`, and `_WRITEV:38` is one 97 already cleared. `delete.record` is in
>   fact **deliberately careful**: `record.count += 1` **before** the delete and
>   `-= 1` inside the handler, so 3221 counts only successes.
>
> **5c. FIVE MESSAGES HAVE NO CALLER, AND ONE OF THEM IS ALREADY EXPLAINED.**
> `6055`, `6056`, `6057`, `6058` are dead in **both** trees — Ladybridge's own
> litter, noted in UPSTREAM 34. **`3312` "Server configuration updated" is dead
> HERE and live upstream (2 callers), and that is `DELSRVR`/`SETSRVR`, which the
> port removed on purpose** — §"SDNet is gone", 21 Aug 2026, with `verify-nonet`
> guarding it. ***Checked against the record before being written up, which is
> the only reason it is not filed as a gap.***
>
> *(The original note follows.)* **`sysmsg` success-assertions — `3029`–`3042`
> (catalogue), `6055`–`6058` (user create/delete), `6136`–`6194` (delete, rename,
> copy), plus `2500`, `3221`, `3251`, `3312`. Lower prior than the `10xxx` range
> because they are Ladybridge's rather than port artefacts — **but they are where
> `UPSTREAM_FIXES.md` entries would come from**, and the owner's standing
> instruction is to file upstream what upstream also has. **A defect in both trees
> goes in BOTH files.**
>
> **6. ✅ DONE 31 Aug 2026 — ONE HARDENING, 105. THE INSTRUMENTS ARE IN GOOD
> SHAPE AND THE ARCHETYPE IS ALREADY FIXED.** ***`verify-apiidentity.ps1`, THE
> FILE THIS ITEM WAS WRITTEN ABOUT, NOW CARRIES EVERYTHING THE RULE ASKS FOR***
> — an explicit `$disqualifiers` list (`:591`), named success anchors (*"anchor:
> sysmsg 6129, the LAST message on the happy path"*, `:585`; 6189 at `:686`) and
> **VOID rather than a pass** when its control fixture fails. **Do not re-audit
> it.** ***313 assertions across 43 verifiers swept; both mechanical defect
> signatures came back EMPTY*** — **0** case-insensitive hash/base64
> comparisons, and `-ceq`/`-cne` correctly used in the 5 files where case
> decides. ***`verify-osusers.ps1` IS THE MODEL TO COPY***: a three-state
> verdict (**2 = could not run**, distinct from failed), `Assert-ProbeRan`, and
> a `LOGNAME=` probe-ran guard — **stronger than `Write-Verdict`, which has only
> two states.** **105 is the one finding**: `verify-apiadmin.ps1:306` anchors on
> the two probe NAMES, which `BASIC:330` prints *before* compiling (2812) and
> `BCOMP:12079` prints again on failure (2612), so the check rests entirely on
> its disqualifier. **The anchor it should use already exists** — `BCOMP:1540`
> prints *"0 error(s)"* on the happy path.
>
> **6b. THE STRUCTURAL NUMBERS ARE A LEAD, NOT A CHARGE.** `Write-Verdict` is in
> **9 of 43**, a disqualifier control in **11 of 43**, a named success anchor in
> **4 of 43**. ***A FILE WITHOUT THE WORD STILL ANCHORED CORRECTLY EVERYWHERE IT
> WAS READ***, so these are idiom counts and filing them as defects would be the
> overclaiming this project punishes — but they are where a next pass should
> look first.
>
> *(The original note follows.)* **The verifiers themselves** — the meta-sweep, and the reason to bother is on
> the record: `verify-apiidentity` reported a refused step as *"confirmed"*, and
> three false verdicts in one day came from instruments that never reached the
> condition they claimed to measure. **Anchor on the SUCCESS wording, refuse the
> null case.** `test-verdict-units` covers `Write-Verdict` across 9 files; **the
> step logic inside each verifier is not covered by anything.**
>
> *(The 91/92 hand-over box below is now history. Both are closed.)*

> # ⇩⇩⇩ HANDOFF, 31 Aug 2026 — OUT OF CREDITS. NEW SESSION, DIFFERENT ACCOUNT. ⇩⇩⇩
>
> ***THE WORK IS RULED, TRACED AND NOT STARTED. THREE CHANGES, IN THIS ORDER.***
> Read **PRE_RELEASE 91** and **§5.22** first; both were written today for this
> hand-over and between them carry the whole model.
>
> **1. ✅ PRE_RELEASE 91 IS CLOSED — `-Run b85`, GREEN IN BOTH HALVES.**
> ***UNELEVATED 18 OF 18, ELEVATED 21 OF 21, 290 `[PASS]`.***
> `verify-logtoaccess: PASSED - 6 of 6 decisive checks passed` —
> `arrivals into SDTUB85` **2**, `back at home in DON` **1**, no 10003, no 5161,
> both controls green. **The ruling on 19 is met by a passing leg, not by
> argument.**
>
> ***THE ONE `[FAIL]` IN 290 IS FILED AS 92 AND IS NOT A VERDICT.***
> `verify-doors`' **non-decisive local witness** (`5 of 5 decisive, 7 rows`).
> **91 is what changed it**: an administrator as themselves now passes
> `logto.authorised` above the SUSPENDED block, as an elevated session always
> did, so `WHO` said `107 DON` and the leg saw 5161 rather than 10107. **That is
> 5.22 working**; the row's `expected True` is what is now wrong. ***NOT
> FLIPPED*** — entry 64 carries that instruction for this exact reflex.
> **Measured across 23 transcripts**: PASSED on every run to 09:57, FAILED on
> both after 91 landed.
>
> ***AND 65's OPEN QUESTION IS ANSWERED BY THE SAME RUN: THREE LEAKERS, NOT
> TWO.*** `verify-tiers` leaks the same way and 65 never named it.
>
> *(The state this box described before that run:)*
> **PRE_RELEASE 91 — CYCLED AND INSTALLED 31 Aug 2026.**
> ***FULL CYCLE, INSTALL 31 Aug 13:33:28, `assert-current` EXIT 0 LIVE***
> (3,020 files across the six mirrored directories, `sd.exe`
> **`87701F86382AEA63`**, `bin\` 00:59:39 with no source newer — unchanged, and
> correctly so, because this change is BASIC only). ***THE NEW PROGRAM IS IN
> THE INSTALLED TREE, READ OFF DISK RATHER THAN INFERRED***:
> `C:\ProgramData\SD\sdsys\gcat\!SD_ADMIN_TIER` and `gpl.bp.out\SDADMIN` both
> **472 bytes stamped 13:32** — the install, not the 13:14 staged build —
> against `!TIER_ALLOWS` **827** as the control.
>
> ***`-Run b83` RAN AND THE 91 ROW PASSED. THE PRODUCT IS FIXED.***
> Unelevated **17 of 18 exit 0**, and the one failure was
> `verify-logtoaccess` — ***THE INSTRUMENT, NOT THE PRODUCT***, with every
> product row in it green:
>
> ```
> [PASS] arrivals into SDTUB83 (0 = refused first, 1 = the flag was cleared): expected 2, got 2
> [PASS] SD did NOT say 10003 ...        [PASS] SD did NOT say 5161 ...
> [PASS] control: sdtub83 was refused with 10003
> [PASS] control: sdtub83 did NOT arrive in DON
> ```
>
> The transcript shows it plainly: `LOGTO SDTUB83` → `78 SDTUB83 from DON`,
> `LOGTO DON` → `78 DON`, `LOGTO SDTUB83` → `78 SDTUB83 from DON`. **The second
> entry into an ungranted account is what 91 refused and it now succeeds.**
>
> ***THE FAILING ROW TAUGHT SOMETHING WORTH KEEPING: `from X` NAMES THE
> SESSION'S HOME ACCOUNT, NOT THE PREVIOUS HOP.*** The row expected an arrival
> back into `DON` and got 0, because going home prints a bare `78 DON`. **The
> three hops settle it**: hop 2's previous account was SDTUB83 and it printed no
> clause at all, which a "previous hop" reading cannot explain. `verify-doors`
> says the same in its own words and this file was written having read it —
> the lesson is its own header's: *look at the output the tool prints on the
> path you are measuring, not the one next to it.* Fixed with `Count-AtHome`
> and **re-tested against the real b83 lines, with negative controls both ways**
> (neither counter matches the other's shape). A second fix went in with it:
> `Invoke-SdAsTestUser` returns an OBJECT, and the control rows had been passing
> through **accidental stringification** of `@{ExitCode=…; Out=…; Err=}`.
>
> ***`b83` IS SPENT — USE `b84`. AND THE WHOLE ELEVATED HALF NEVER RAN***: the
> runner correctly refused to hand over on a failing step. The test account was
> removed cleanly (`sdu_SDTUB83` and the OS user both Deleted; one profile
> directory Windows would not release yet).
>
> *(The compile that preceded it: `cycle.ps1 -SkipInstall` 13:13:42, ISCC exit
> 0, installer **4,940,170**
> bytes. **`SDADMIN` 0 errors**, `!SD_ADMIN_TIER` **added to global catalogue**;
> `CPROC` and `LOGIN` **0 errors each**. ***READ RATHER THAN BELIEVED*** (the
> 26 Aug precedent): `gcat/!SD_ADMIN_TIER` and `gpl.bp.out/SDADMIN` both exist
> at **472 bytes** against `!TIER_ALLOWS` **827** as the control, both stamped
> 13:14. ***AND NO NEW ERRGEN WARNING*** — `CPROC`'s `PRIVILEGED_COMMANDS` one
> is pre-existing at `:245` and is **not** in this diff (checked). `SDADMIN`'s
> *"Final END statement is missing"* is the house pattern: **`TIERGATE` emits
> the identical warning.** At that point the installed tree was still untouched
> and stale, and the SD service was left stopped — **both since overtaken by
> the full cycle above.**
>
> ***COUNTS: `gcat` 133, `gpl.bp.out` 192 — AND 192 IS NOT THE 191 PREDICTED.***
> The prediction was wrong because the baseline it came from was stale, not
> because this added two: **`PS_SCRIPTO` landed on 31 Aug after the "190" in
> this box was written.** The delta is confirmed directly instead — `gpl.bp`
> sources **204 → 205**, the one addition being `SDADMIN`.)*
>
> **WHAT IS IN THE TREE:** `logto.authorised` has a **fourth bypass** that asks
> the PERSON — `kernel(K$OS.ADMINISTRATOR, 0)` **and** the `ADMINISTRATOR` tier
> on that person's own register entry — and `LOGIN:573` and `CPROC:2662` ask the
> same pair. The bare `K$ADMINISTRATOR` bypass is gone.
>
> ***THE OWNER RULED "CLOSE BOTH NOW" ON 31 Aug 2026, AND IT TURNED OUT TO BE
> THREE GATES.*** His correction is what started it — *"a windows administrator
> does not have access unless they are granted access and to grant access they
> have to have a personal account first"* — and it is right: `CREATEA:821` puts
> you in `sdusers` only by creating your account, and `:1441`/`:847` join
> Administrators only on the ADMINISTRATOR keyword, so **for anybody SD created
> the two halves always agree**. Only a person made a Windows administrator
> **outside** SD diverged, and they reached SDSYS because no gate tested the
> tier.
>
> **All three now read `kernel(K$OS.ADMINISTRATOR, 0) and sd_admin_tier(@logname)`:**
> `LOGIN:573`, `CPROC`'s `logto sdsys` door at `:2662`, and `logto.authorised`.
> ***THE THIRD WAS NOT IN THE RULING AND IS WHY IT WOULD HAVE FAILED WITHOUT
> IT***: `logto sdsys` sets `elev.obtained`, which is a bypass in its own right,
> so closing the other two alone would still have admitted exactly the person
> the ruling excludes. **The bare `K$ADMINISTRATOR` bypass is DELETED.**
>
> **New shared function `gpl.bp/SDADMIN` (`!sd_admin_tier`)** — three gates, two
> programs, one copy. **Adding a program needs no build-list change**, checked
> against the commit that added `TIERGATE`.
>
> ***TWO TRAPS PAID FOR ON THE WAY, BOTH ALREADY ON DISK.*** `AND` DOES NOT
> SHORT-CIRCUIT (`CREATEA:382` — a defect that hid from 10 June to 21 Aug 2026),
> so the register read runs on every login and every logto; a first draft of the
> LOGIN comment claimed the opposite and is corrected. And a second handle on
> `accounts` is mandatory, not tidiness — `LOGIN`'s `get.acc.tier` records that
> reusing one with a live select list on channel 12 ends the walk *"with no
> error and no sign of it"*, which is why `SDADMIN` opens its own.
>
> ***TWO THINGS THIS ENTRY SAID WERE WRONG, AND BOTH ARE CORRECTED IN 91.***
> **(a) The fix it named would have fixed nothing.** `LOGIN:573`'s pair ANDs on
> `K$ADMINISTRATOR` — the flag `:2825` clears and LOGIN never sets for an
> unelevated administrator — so it is FALSE in both failing cases. LOGIN asks
> *"did this session START elevated"*; this asks *"may this person ENTER this
> account"*. **(b) SDSYS was never part of the lockout**: `logto sdsys` is gated
> at `CPROC:2662` on `K$OS.ADMINISTRATOR`, which a `logto` cannot move, and
> `elevate('START')` then sets `elev.obtained` — a fresh UAC consent is the way
> back, not a reconnection.
>
> ***AND THE SCOPE IS WIDER THAN "AFTER ONE LOGTO".*** LOGIN arms
> `K$ADMINISTRATOR` only on its SDSYS case (`:591`, `:674`), so an administrator
> signing in **as themselves** — the only thing ssh can do — was refused with
> 10003 on their **FIRST** `logto`. §5.22 row 1 was implemented nowhere.
>
> ***THE VERIFIER IS WRITTEN AND HAS NEVER RUN: `gplbld/verify-logtoaccess.ps1`.***
> In `VerifyInstall1` because an **elevated** runner could not measure it at
> all — an elevated session lands in SDSYS. ***UNELEVATED IS 18 STEPS NOW, NOT
> 17***, so expect 18 on `b83` and do not read the extra one as drift.
>
> ***ITS DECIDING ROW IS A COUNT: ARRIVALS INTO THE TARGET = 2.*** Three logtos
> in one session. **0 is the unelevated defect** (refused on the first), **1 is
> the elevated one** (the first worked and cleared the flag), 2 is the fix — a
> single successful logto would not have told them apart. The throwaway account
> is both the ungranted target and the **non-administrator control** refused
> with 10003, without which the run cannot tell *"the administrator path works"*
> from *"the gate is open to everybody"*. Four preconditions **refuse out loud**,
> the load-bearing one being *the caller must NOT already be granted the target*.
>
> ***THE `$refusers` GUARD FOUND A REAL DEFECT IN IT BEFORE IT RAN*** — the
> parameters were `Mandatory`, so the **binder** would have refused ahead of the
> body and an unattended suite would have got a prompt rather than a message.
> Registered in **four** places in the same commit: `assert-current`'s
> `$neverShipped`, `test-verdict-units`' `$targets`, `VerifyInstall1`'s steps
> and `$needsTestUser`, and `test-sdtestuser-units`' `$refusers`.
>
> ***A WRITTEN VERIFIER IS NOT COVERAGE — 91 STAYS OPEN UNTIL A LEG PASSES.***
> It does not cover the **elevated-start** half (UAC has no desktop in a nested
> elevation, §4.0.1) or the **tier half's negative case** (needs a second
> Windows administrator); its header names both.
>
> **2. EMPTY `TIER.ADD.ADMINISTRATOR`.** The 24 restricted commands stay in
> `voc_template` (so SDSYS keeps them) and no created account gets them —
> §5.22's table. ADMINISTRATOR-tier VOC **420 → 396**, identical to PROGRAMMER.
> **Both count constants and `verify-tiers`' assertions invert with it**
> (`administration verbs MISSING` becomes 24 for all three tiers).
> ***RUN `test-tiercounts-units.ps1` AFTER EVERY EDIT*** — it now checks all
> three copies, including `$AdminVerbs`, and it is free.
>
> **3. ⚠️ REPOINT `tclmap`'s ROSTER AT `voc_template` — DO NOT SKIP THIS.**
> `SDCoreWindowsDocs/tools/tclmap.py:24` computes the roster as *123 in
> `newvoc` **plus** `TIER.ADD.ADMINISTRATOR`*. Emptying that list would drop 24
> **shipping** verbs out of documentation coverage and the checker would go
> **green** with 24 undocumented verbs. Same class as the red-tree finding below.
>
> # ⇩⇩ THE MACHINE, AS LEFT ⇩⇩
>
> - ***`b54`–`b82` SPENT. USE `b83`.***
> - ***OPEN COUNT 16, READ FROM `test-fixlist-units.ps1` AND NEVER FROM PROSE***:
>   3, 6, 16, 20, 28, **65**, 66, 67, 70, 74, 76, 78, 80, 88, 89 — **15**.
>   **91 CLOSED on `-Run b85`; 92 filed from that run and CLOSED on
>   `-Only verify-doors-suite -Run b86`** (all 5 legs green, 68 `[PASS]`, zero
>   `[FAIL]`; both new rows pass in BOTH phases, and the ordering claim still
>   holds on the helper — `WHO` said `41 SDDRB86B`). *(`b54`–`b86` spent — use
>   `b87`. Profile dirs `C:\Users\sddrb86a` and `sddrb86b` remain: PRE_RELEASE
>   35/36, expected, and the names are taken until a restart.)*
>   *(Was 14 + 91 when this box was written. **65 was RE-OPENED 31 Aug 2026** —
>   its product half is fixed and proven on `b74`, its HARNESS half is not, and
>   `-Run b84` reproduced the symptom: `os.users` holding `SDRTB84A` and
>   `SDTIERTB843` as `yes|yes` with both Windows accounts ABSENT. 85 and 90
>   closed earlier the same day.)*
> - **The installed tree is STALE and correct** — `sd.iss` moved after the
>   09:54:22 install. `assert-current` names it.
> - ***88 IS BUILT AND NOT CYCLED***, and a cycle alone cannot test it: see the
>   three-step sequence further down. ISCC exit 0.
> - **The doc tree is RED and has been since 30 Aug** — `tclmap` exits 1,
>   roster 146, three `NO PAGE`. `append.sd.path` makes it four. PRE_RELEASE 80.
> - **Nothing is uncommitted.**
>
> # ⇩⇩ WHAT TODAY COST, SO IT IS NOT PAID TWICE ⇩⇩
>
> ***FIVE SILENT TRAPS, EVERY ONE FOUND BY MEASUREMENT AND NONE BY READING.***
>
> | trap | it looked like |
> |---|---|
> | `RegKeyExists(HKLM,…)` from `[Code]` reads **WOW6432Node** — Setup is 32-bit. `HKLM64` FOUND, `HKLM` and `HKLM32` not | compiles clean, `TrueUpgrade` permanently False, 88 silently does nothing |
> | `{#SetupSetting}` written in a **comment** aborts ISCC | "Insufficient parameters" against a line of English |
> | `[Code]` Pascal strings get **no** constant expansion, so `{{` there is two braces | wrong key, silent False |
> | the helper's two capture routes disagreed — field marks vs raw CRLF | one line of boxes |
> | `verify-tiers`' `$AdminVerbs` was a **third** copy of the admin list | 20 minutes into a suite run |
>
> ***AND EVERY DEFECT CLOSED TODAY WAS FOUND BY THE OWNER AT A TERMINAL, NOT BY
> A TEST.*** The tasks page, the silent reports, the field marks, the Ready
> page, and 91. Two instruments were built to move some of that onto the
> machine — `probe-taskflags.ps1` and `test-tiercounts-units`' `$AdminVerbs`
> check — **but the pattern is the thing to remember when choosing what to
> check by hand.**
>
> # ⇩⇩ OPEN QUESTIONS RAISED TODAY AND NOT ANSWERED ⇩⇩
>
> - ***CAN A GROUP ACCOUNT BE GIVEN A TIER?*** `CREATE.ACCOUNT GROUP <name>`
>   documents no tier keyword and defaults to `STANDARD` (`CREATEA:295`), but
>   the keyword parser's `ADMINISTRATOR`/`PROGRAMMER` arms carry **no
>   account-type test** and I could not establish whether that loop is reached
>   on the GROUP path. **If group accounts really are STANDARD-only, nobody can
>   run `basic` or `ed` in a shared work area** — `CREATEA`'s own header calls
>   GROUP *"how work is shared"*. Two commands settle it:
>   `create.account group zzgrp`, then `logto zzgrp` and `count voc` (355 =
>   STANDARD); then whether `create.account group zzgrp2 programmer` is
>   refused. `delete.account` both afterwards.
> - **PRE_RELEASE 70's other half** — nothing RUNS `update.account` on an
>   upgrade. The Ready page now TELLS the administrator to; making the
>   installer do it is still open, with `upgrade-dicts.ps1` as the precedent.

> # ⇩⇩⇩ 31 Aug 2026, 03:00 — PAUSED FOR SLEEP MID-TASK. THE NEXT STEP IS ONE VERB. ⇩⇩⇩
>
> ***THE OWNER IS RESUMING THIS SAME SESSION, NOT STARTING A NEW ONE*** — but
> this block is written as if he were not, because that is what it is for.
>
> # ⇩⇩⇩ 88 IS BUILT. TESTING IT NEEDS A SECOND INSTALL, BECAUSE A CYCLE CANNOT REACH IT. ⇩⇩⇩
>
> ***AN UPGRADE NOW SKIPS THE TASKS PAGE AND FIRES NONE OF ITS ACTIONS.***
> ISCC exit 0, **not yet cycled.** `SdWasInstalled` sampled once in
> `InitializeSetup`, `TrueUpgrade = DataTreeUpgrade and SdWasInstalled`,
> `ShouldSkipPage` back for `wpSelectTasks` alone, and **five action gates** —
> `install-ssh.ps1`, `addtopath`, and the two `ApplyXxxFirewall` call sites.
>
> ***THE ORDER OF TESTING MATTERS AND IS NOT OBVIOUS.*** `cycle.ps1`
> uninstalls and deletes both trees, so **its install is a FIRST install** and
> takes the page-shown path. It proves nothing about the upgrade.
>
> 1. ```
>    C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\cycle.ps1
>    ```
>    **Elevated.** First-install path: the tasks page MUST still appear and
>    behave exactly as before. `gpl.bp.out` 190 → 191.
>
> 2. Then run the installer it built **a second time, over the finished
>    install**:
>    ```
>    C:\Users\dmont\sdout\sd-setup-W1.0-0.exe
>    ```
>    **It asks for elevation itself.** ***THIS is the upgrade path.*** The tasks
>    page must **NOT** appear; ***"Ready to Install" must NOT list any
>    additional tasks*** but describe the upgrade and name the four commands;
>    and the closing box must carry the matching paragraph.
>
>    ***THE READY PAGE IS THE HALF THAT WAS MISSED FIRST TIME.*** Skipping the
>    tasks page leaves the tasks SELECTED, and Inno's memo lists selected
>    tasks — so the upgrade promised four things the gates guarantee it will
>    not do. Owner saw it immediately. `UpdateReadyMemo` now rewrites that page
>    on an upgrade only.
>
> 3. Afterwards, confirm nothing moved: `remote.ssh` and `remote.api` must
>    report the same state as before the second install, and
>    `append.sd.path` must still show SD on the PATH.
>
> ***TWO SILENT TRAPS WERE PAID FOR BUILDING IT, BOTH CAUGHT BY A THROWAWAY
> PROBE.*** `{#SetupSetting}` written in a *comment* aborts the compile — ISPP
> expands a brace-hash inside comments too. And ***`RegKeyExists(HKLM, …)`
> FINDS NOTHING FROM `[Code]`***: Setup is a 32-bit process, so plain `HKLM` is
> redirected to `WOW6432Node`. Measured with SD installed as the control —
> `HKLM` not found, `HKLM32` not found, **`HKLM64` FOUND**. **That one compiles
> clean and would have left `TrueUpgrade` permanently False, the whole entry
> doing nothing while every test reported success.**
>
> # ⇩⇩ 31 Aug 2026 — SUITE GREEN ON `-Run b81`. ⇩⇩
>
> ***UNELEVATED 17 OF 17 EXIT 0. ELEVATED 20 OF 21, AND THE ONE WAS THE
> VERIFIER, NOT THE PRODUCT*** — `verify-tiers` carried a THIRD stale copy of
> the admin list (`$AdminVerbs`); fixed, and **re-run on `-Run b82`: exit 0,
> 33 of 33.** Install 09:54:22, `assert-current` **exit 0 live** in the rerun.
>
> ***SO THE `!ps_script` REFACTOR SURVIVED 10 OF ITS 14 CALLERS***, which is the
> regression half of the test plan below, done: the credential path
> (`createaccount`, `delaccount`, `accountrules`, `setpw`, `profiledir` — i.e.
> `CREATE_USER`, `SET_PASSWD`, `OS_GROUP`, `PROFILE_DIR`, `CRED_SET`),
> `APISRVR` across six API steps, and `ELEVATE` in **every** step that does
> `logto sdsys`. **None of them behaves differently, which is exactly what was
> wanted — they were only ever meant to keep their silence.**
>
> ***AND TWO ROWS PROVE `append.sd.path` ON A LIVE ACCOUNT RATHER THAN IN THE
> STAGE***: `sdtiertb823 COUNT VOC 420`, and `sdtiertb821 administration verbs
> MISSING 24` — a standard account is missing all twenty-four, the new verb
> included, so the `voc_template`-only placement holds where it matters.
>
> ***AND THE FOUR REPORTS PRINT — PRE_RELEASE 90 IS CLOSED, 31 Aug 2026.***
> Measured in SDSYS on the installed tree: `append.sd.path` gives the whole
> `sd-path` report with all eleven PATH entries numbered on their own lines;
> `remote.api` four lines, `remote.ssh` two, `ssh.server` four. **No boxes, no
> single-line run, no empty last line**, so `tidy.out`'s CR-strip,
> LF-to-field-mark and trailing-field trim all hold. **Found and closed by a
> real terminal twice over — the silence, then the field marks — and no unit
> test could have caught either, because neither route exists off a live
> session.**
>
> ***AND THE ACTION PATH IS MEASURED TOO — `append.sd.path` IS DONE.*** `on`,
> `off`, `on` in SDSYS: **one line each, no report above**, so the capture
> stays silent on success as designed. ***THE MACHINE WAS THEN READ RATHER
> THAN THE MESSAGES BELIEVED***: the system PATH is **11 entries, 11
> non-empty**, same order as before, SD back at `[10]`. **Value kind still
> `ExpandString`** — the `SetEnvironmentVariable` corruption did not happen —
> and **zero empty entries**, so 16 Aug's accumulated-separator bug did not
> recur across a real remove-then-add.
>
> ***SO 89's DEFECT B IS CLOSED. WHAT IS LEFT OF 89 IS DEFECT A, AND ITS ANSWER
> IS 88 — RULED, NOT BUILT.***
>
> **`b54`–`b82` SPENT. USE `b83`.**
>
> # ⇩⇩ THE `!ps_script` REFACTOR TOUCHES 14 PROGRAMS. THE PLAN, KEPT. ⇩⇩
>
> ***PRE_RELEASE 90 MOVED `!ps_script`'s BODY.*** Four verbs gained NEW
> behaviour (they print a report); the other ten must behave **identically**,
> so most of this is regression testing, not feature testing. **The owner asked
> the right question — "shouldn't I test all the possible affected commands?"
> — after being handed a two-command list. He should have had this.**
>
> **The 14, and what reaches each:**
>
> | program | reached by |
> |---|---|
> | `ELEVATE` | ***`logto sdsys` ITSELF.*** If this broke you cannot enter SDSYS at all, so every other test below implicitly proves it |
> | `CREATE_USER`, `SET_PASSWD`, `OS_GROUP`, `PROFILE_DIR`, `CRED_SET` | `create.account` — **and the INSTALLER's own account step**, so a clean install is already evidence |
> | `CREATEA` | `create.account` |
> | `MODIFYA` | `modify.account` |
> | `DELETE_USER` | `delete.account` (`$DELACC`) |
> | `APISRVR` | any API login |
> | `APNDPATH`, `REMOTEAPI`, `REMOTESSH`, `SSHSRVR` | the four report verbs — **the only ones whose behaviour is meant to change** |
>
> ***SO: FULL CYCLE, THEN THE FULL SUITE.*** The suite already covers
> create/delete/modify account, the API and the tiers — which is most of the
> ten. `-Only` is the wrong tool here; this is the milestone case §"The full
> verify suite runs at milestones" was written for.
>
> ```
> C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\cycle.ps1
> ```
>
> ```
> C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\VerifyInstall1.ps1 -ThenElevated -Run b81
> ```
>
> **Both ELEVATED PowerShell.** ***SPENT: `b54`–`b80`; `b81` IS FREE.***
>
> ***THEN THE FOUR REPORTS BY HAND, BECAUSE NO SUITE STEP RENDERS ONE*** — the
> same blind spot the tasks page had:
>
> ```
> append.sd.path
> remote.api
> remote.ssh
> ssh.server
> ```
>
> Each must print its script's report **laid out on separate lines**. A single
> line studded with boxes is the field-mark bug again; nothing at all is the
> original defect.
>
> ***AND THE ACTIONS, WHICH MUST BE UNCHANGED — ONE LINE EACH, NO REPORT:***
> `append.sd.path on` / `off`, `remote.ssh on` / `off`, `remote.api on` /
> `local` / `off`.
>
> ***DO NOT TEST `ssh.server remove`.*** It strands every SD account whose only
> route is ssh — the API is an independent way in (PRE_RELEASE 124), so it is
> "their only way in" only for an account that was never granted API access —
> and it completes on a reboot. `ssh.server` bare and `install` are safe;
> `remove` is not a test, it is a rebuild. ***(Wording corrected 2 Sep 2026: this
> line carried "they sign in over ssh and nothing else", the premise 124 retired
> as FALSE. `test-retired-wording-units` scans shipped messages and scripts only,
> so the internal documents are where that premise can survive — grep them when
> you retire wording, the lint will not.)***
>
> **`remote.api off` is reversible but real**: it rewrites `sd.conf` and wants a
> service restart, so put it back with `remote.api on` when done.
>
> # ⇩⇩ `append.sd.path` COMPILES. IT HAS NOT RUN. THAT IS THE NEXT STEP. ⇩⇩
>
> ***`cycle.ps1 -SkipInstall`, 31 Aug 2026 09:06:15: ISCC exit 0,
> `sd-setup-W1.0-0.exe` 4,931,937 bytes.*** **The staged tree was READ rather
> than the run's output believed** (26 Aug precedent): `gpl.bp.out/APNDPATH`
> 783 bytes, `gcat/$APNDPATH` present, `voc_template/append.sd.path` staged,
> messages **10152–10156** all five there, `TIER.ADD.ADMINISTRATOR` 24 verbs.
> ***`gpl.bp.out` 189 → 190***, `gcat` 131. **And the admin-only placement
> proved itself**: `newvoc` still 395 names, `newvoc/append.sd.path` absent.
>
> ***COMPILING IS NOT RUNNING, AND NOTHING HAS RUN IT.*** It wants a FULL
> cycle, then the verb exercised:
>
> ```
> C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\cycle.ps1
> ```
>
> ***ELEVATED PowerShell.*** ~20 minutes, and it ends with `assert-current`.
> Then, in SD as an administrator: **`append.sd.path`** bare must report and
> change nothing; **`on`** then **`off`**; and a **non-administrator must be
> refused with 2001**. The `-Show` leg is the cheap one and needs no elevation
> of its own.
>
> **Then it still needs a doc page**, or `tclmap` goes to 147 with **four**
> `NO PAGE` rows instead of three.
>
> ***AND `cycle.ps1` STEP 1 STOPS THE SD SERVICE AND NOTHING RESTARTS IT***
> (`:218`). Put it back by hand afterwards, as the 30 Aug run had to.
>
> # ⇩⇩ THE ORIGINAL INSTRUCTION, KEPT FOR ITS REASONING ⇩⇩
>
> ***BUILD `append.sd.path on | off`. THE NAME IS RULED; DO NOT RE-DEBATE IT.***
> Owner, 31 Aug 2026. `set.path` was rejected with evidence — inside SD "path"
> means the ACCOUNT's path (`pathname` is a VOC keyword, `where` prints
> *"account pathname"*, `@PATH`), and `os.path` collides with
> `gpl.bp/VALID_OS_PATH`. Three-segment verbs are normal here
> (`set.exit.status`, `who.am.i`).
>
> **Model it on `gpl.bp/REMOTEAPI`**, which is the same shape: a verb that
> drives a shipped PowerShell script. **The script is already built and
> tested** — `gplbld/sd-path.ps1`, `-Show` / `-Add` / `-Remove`,
> `test-sdpath-units.ps1` **24 of 24**. The verb is the only missing piece.
>
> | it must touch | why |
> |---|---|
> | `sdsys/gpl.bp/` new program | modelled on `REMOTEAPI` |
> | `sdsys/voc_template/append.sd.path` | ***voc_template ONLY, NEVER newvoc*** — `verify-tiers.ps1:41`: *"putting it in newvoc hands it to every account SD creates"* |
> | `sdsys/newvoc/TIER.ADD.ADMINISTRATOR` | → 24 verbs. Administrator-only, owner's instruction |
> | `gplbld/verify-tiers.ps1` | ADMINISTRATOR → **420** = 392 + 24 + 4, ***re-derived from the directory, not adjusted by one*** — that block says so |
> | elevation | HKLM needs the elevated helper; `ps_script` is warranted here, not the overkill 67 warned of |
> | a doc page | or `tclmap` goes to 147 with **four** `NO PAGE` rows |
>
> # ⇩⇩ AND THE DOCUMENTATION TREE IS RED RIGHT NOW. IT HAS BEEN SINCE 30 Aug. ⇩⇩
>
> ***`tclmap.py` EXITS 1: roster `146`, assigned `143`, `NO PAGE` for
> `remote.api`, `remote.ssh`, `ssh.server`.*** Measured 31 Aug 2026. **The
> checker is not at fault** — it COMPUTES the roster from `newvoc` plus
> `TIER.ADD.ADMINISTRATOR`, so it noticed the moment entry 78 added those verbs.
> **Nobody ran it.** ***H.2's "tclmap 143 of 143, 0 exempt" WAS STALE AND IS
> CORRECTED.*** The real finding is in PRE_RELEASE 80: **`tclmap.py` lives in
> the OTHER repository and no tier-1 check here runs it**, so adding an
> administrator verb in this repo silently breaks a checker in that one.
>
> ```
> cd C:\Users\dmont\Projects\SDCoreWindowsDocs
> python tools\tclmap.py C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\sdsys\newvoc
> ```
>
> **An ordinary unelevated prompt.**
>
> # ⇩⇩ THE OTHER RULING OF 31 Aug, AND IT IS NOT BUILT ⇩⇩
>
> ***AN UPGRADE SKIPS THE TASKS PAGE ENTIRELY.*** Owner: *"if the admin wants to
> make additional choices, we have given them the command line tools."*
> **PRE_RELEASE 88 carries it, and the trap with it**: skipping the page does
> NOT deselect the tasks, so the page-skip alone would turn *visible but inert*
> into ***invisible but active***. It needs `ShouldSkipPage(wpSelectTasks)` on
> `DataTreeUpgrade` **and** the four gates returning no-change. **Not built.**
>
> ***OPEN COUNT 14***: 3, 6, 16, 20, 28, 66, 67, 70, 74, 76, 78, 80, 88, 89.
> ***SPENT: `b54`–`b80`. USE `b81`.*** **The installed tree is STALE and that is
> correct** — `sd.iss`, `stage.py` and `sd-path.ps1` have all moved since the
> 01:05:10 install; `assert-current` names them. A cycle clears it.
>
> # ⇩⇩ 30 Aug 2026, 23:35 — A LITTER CLEAR IS HALF DONE AND WANTS A REBOOT. ⇩⇩
>
> ***`C:\Users` IS 268 → 89 sd* DIRECTORIES. THE REMAINING 89 ARE HIVE-LOCKED
> AND NEED A REBOOT, THEN ONE MORE RUN — NOTHING ELSE IS OUTSTANDING FROM IT.***
> `cleanup-devlitter.ps1` elevated: users **1 → 0**, `sdu_` groups 0, home `sd*`
> items **1 → 0** (`sdxfer`), profiles **252 → 163 removed, 0 failed**, `sdout`
> still present. It **exits 1 by design** — `clean-test-profiles.ps1` refuses to
> let a sweep of what it could see read as a sweep of the machine. The 16 with no
> `ProfileList` entry were then removed by hand (**16 removed, 0 failed**), which
> is what the record already said that class costs. **To finish:**
>
> ```
> C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\cleanup-devlitter.ps1
> ```
>
> **Elevated, after a restart.** `b48adm` is deliberately untouched — a live
> local account, outside every stem.
>
> ***AND IT FOUND PRE_RELEASE 86 ON THE WAY: THE SWEEP HAD WALKED PAST 25 OF THE
> 268 AND REPORTED SUCCESS.*** `sdgate` and `sdtu` were never added to
> `clean-test-profiles.ps1`'s `$stems`, so 25 directories were invisible to the
> only thing that sweeps them. **Fixed and self-tested; 268 of 268 now inside the
> rule.** The entry leaves one recommendation unbuilt — nothing compares `$stems`
> against the names `VerifyInstall2.ps1` actually builds, so a fourth family will
> be missed the same way.
>
> # ⇩⇩⇩ 31 Aug 2026, 02:00 — RESOLVED. 85's FLAGS WERE RIGHT; THE WIZARD WAS SHOWING THE OLD INSTALL'S ANSWERS. ⇩⇩⇩
>
> ***NOTHING BELOW THIS BLOCK NEEDS DOING. IT IS KEPT BECAUSE ITS "RULED OUT"
> TABLE IS SOUND MEASUREMENT AND BECAUSE THE CONCLUSION IT REACHED WAS
> WRONG*** — the previous session ended on *"the three flags did not work"*,
> and they do.
>
> ***MEASURED BY `gplbld/probe-taskflags.ps1`, WRITTEN THIS SESSION.*** It
> drives the tasks page through Inno's **own** click path
> (`TNewCheckListBox.CheckItem`, the method a mouse click calls) and reads the
> states back. **Unelevated, ~3 seconds, no cycle, no install, no run token.**
>
> ```
> C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\probe-taskflags.ps1
> ```
>
> **An ordinary unelevated prompt.** It compiles a probe installer with no
> `[Files]`, no `[Run]` and no app dir, which aborts at the tasks page: it
> installs nothing.
>
> | leg | what it shows |
> |---|---|
> | 1, `UsePreviousTasks=no` | **all three flags behave.** Tick parent → child stays unchecked; untick child → parent stays ticked; re-tick parent → child stays unchecked. **The ssh pair is identical on all five transitions, so 67 stands too** |
> | 2, `UsePreviousTasks=yes` + a restored selection | **both API boxes arrive CHECKED** — the owner's report, from the same binary and the same flags |
>
> ***THE CAUSE IS `UsePreviousTasks`, WHICH `sd.iss` NEVER SETS, SO IT IS
> `yes`.*** Inno reads `Inno Setup: Selected Tasks` from the uninstall key at
> startup and uses it as the page defaults, **overriding every `unchecked`
> flag**. This machine's value reads
> `addtopath,sshremoteopen,apiremote,apiremote\apinetwork` — **written by the
> pre-fix build and restored faithfully by the fixed one.** ***FILED AS
> PRE_RELEASE 88, AND IT IS A DECISION, NOT A FIX*** — `yes` is Inno's default
> and matches this project's own "an upgrade does not re-ask" policy, but it
> means a tightened default never reaches an existing site.
>
> ***HIS SENTENCE COVERED TWO THINGS AND ONLY ONE WAS EVER A DEFECT.*** *"If
> one is checked they both are checked"* is the restored **arrival** state;
> *"and vice versa"* is untick-parent-unticks-child, which is **correct Inno
> behaviour and cannot be disabled**. Once either box is touched the flags take
> over and behave.
>
> ***INNO IS 6.7.3***, from the same registry key — the open version question.
>
> ***AND THE PROBE ITSELF MISLED HIM TWICE BEFORE IT WAS RENAMED.*** Its window
> is a real Inno wizard, it forces `SshServerAbsent := True` so the dependent
> ssh pair exists to test, and he read it as `sd-setup` showing an "install the
> server" box on a machine that has one. **It now says so in the title bar and
> across the page.** `sd.iss` derives that flag from the machine at `:1105`, so
> the real wizard hides that box here: **four boxes = the probe, three = the
> installer.**
>
> # ⇩⇩ THE SUPERSEDED HANDOFF FOLLOWS. ITS TABLE IS STILL TRUE. ⇩⇩
>
> ***THE OWNER RAN THE NEW INSTALLER AND THE API BOXES STILL MOVE TOGETHER:***
> *"the api checks move together if one is checked they both are checked and
> vice versa."* **The three flags are in `sd.iss` and they did not change the
> behaviour.** Session ended here, out of credits, mid-diagnosis.
>
> ***WHAT IS ALREADY RULED OUT — MEASURED, NOT ASSUMED. DO NOT REDO THIS.***
>
> | ruled out | how |
> |---|---|
> | he ran a stale installer | only ONE `sd-setup*.exe` exists on the machine, `C:\Users\dmont\sdout\sd-setup-W1.0-0.exe`, built **01:14:09**; `sd.iss` mtime is **01:10:33**, so the change was in it |
> | ISCC compiled a different file | `cycle.ps1:468` passes `$Iss`, and `$Iss = Join-Path $Gplbld 'sd.iss'` (`:171`) — the file that was edited |
> | a duplicate task definition | `grep apiremote` finds **one** `Name:` for each of parent and child, at `sd.iss:425` and `:427` |
> | `[Code]` overriding the checkboxes | **nothing** matches `TasksList`, `WizardSelectTasks`, `CheckItem`, `Checked[` anywhere in `sd.iss` |
> | a compile warning about the flags | ISCC exit 0, and its only warning is the pre-existing `FileCopy` hint at line 3797 |
>
> ***THE FLAGS THEMSELVES ARE STRUCTURALLY IDENTICAL TO THE ssh PAIR***, which
> is the pattern 67 used: parent `checkablealone`, child `unchecked
> dontinheritcheck`, no `GroupDescription` on the child. The only difference is
> that the API parent also carries `unchecked` (75's ruling: the API defaults
> OFF) and the ssh pair carries `Check: SshServerAbsent`.
>
> # ⇩⇩ ANSWERED WITHOUT ASKING — BOTH BRANCHES AT ONCE. SEE THE TOP. ⇩⇩
>
> ***THE QUESTION BELOW WAS THE RIGHT ONE AND DID NOT NEED A PERSON.*** The ssh
> pair is the control, and `probe-taskflags` runs it alongside the API pair on
> every invocation: **ssh correct, API correct, and both wrong only when a
> previous selection is restored.** That is a third answer the two branches
> below did not have, and it is the true one.
>
> ***ASK WHETHER THE ssh PAIR ON THE SAME PAGE BEHAVES CORRECTLY.*** It carries
> the same two flags, so it is the control:
>
> - **ssh correct, API wrong** → something specific to the API pair. The
>   `unchecked` on the parent and the absent `Check:` are the only candidates.
> - **BOTH wrong** → the flags are not doing this on his Inno, and ***67's
>   "FIX IS PROVEN" CLAIM IS WEAKER THAN IT READS***. Read it again before
>   trusting it: what was measured on 30 Aug was the OUTCOME — *"the server IS
>   installed and remote access IS blocked"*, `RemoteAddress=127.0.0.1` — **not
>   the checkbox behaviour on the page.** If both pairs move together, 67 needs
>   re-opening too.
>
> **Also worth pinning down: WHICH direction he saw.** Checking the CHILD and
> having the parent become checked is **correct** Inno behaviour, not a bug —
> a child cannot be selected without its parent. Only *parent ticks child* is
> the defect. His sentence covers both directions and only one of them is wrong.
>
> ***THE INNO VERSION WAS BEING READ WHEN THE SESSION ENDED*** and is not yet
> known beyond "Inno Setup 6" (`C:\Program Files (x86)\Inno Setup 6\ISCC.exe`;
> its `VersionInfo` reads `0.0.0.0`, so use `iscc /?` or the IDE's About box).
>
> # ⇩⇩ MACHINE STATE, AS LEFT ⇩⇩
>
> - **The installed tree is STALE and that is correct** — `sd.iss` moved after
>   the 01:05:10 install. `assert-current` exits 1 naming **one** file. A cycle
>   clears it; nothing is broken.
> - **The SD service is Running.** `cycle.ps1 -SkipInstall` stopped it (`:218`
>   — step 1 stops it and nothing restarts it) and it was restarted by hand.
> - ***SPENT: `b54`–`b80`. USE `b81`.***
> - **Open count 14**: 3, 6, 16, 20, 28, 66, 67, 70, 74, 76, 78, 80, **88**,
>   **89**. *(85 CLOSED 31 Aug 2026; 88 and 89 opened after it.)*
>
> ***AND A NEW STANDING RULING CAME OUT OF IT — §5.21, NO CONTROL MAY BE
> INERT.*** Owner, 31 Aug 2026, after the probe showed him an "install the
> server" box on a machine that has one: *"no option should be available that
> the user can click thinking that an action is going to take place, but
> nothing happens."* **That box was the probe's own artifact, but the rule is
> general and the audit it prompted found two real ones** — `apiremote` cannot
> change the listener on an upgrade (`sd.conf` is `onlyifdoesntexist`) and
> unticking `addtopath` never removes SD from `PATH`. **PRE_RELEASE 89 has the
> audit of all seven boxes; neither defect is fixed, and which way each goes is
> the owner's call.**
>
> ***THE THREE PROBES ARE NOW IN `gplbld` AND WIRED INTO NOTHING.***
> `probe-nolockmsg.ps1` (12 and 87), `probe-tasklock.ps1` (24) and
> `check-msglen.py`. **All three are on `$neverShipped`**, listed in the commit
> that added them. **Promoting them to suite steps is the owner's call** — it
> costs two more steps against a full run he has asked to keep short.
>
> # ⇩⇩ SUPERSEDED — 85 AND 67 CLOSED WITHOUT THE LOOK. 74 STILL WANTS THE VM. ⇩⇩
>
> ***DO NOT RUN THE INSTALLER TO LOOK AT THE TASKS PAGE ON THIS HOST.***
> `probe-taskflags.ps1` answers it in 3 seconds, and — more to the point — this
> machine's recorded task selection means the real wizard here shows the OLD
> install's answers (PRE_RELEASE 88), so looking measures the wrong thing.
> **74 is unaffected: it needs an interactive UNINSTALL, and that still wants
> the VM.** The block below is kept for its cancelling-writes-nothing note.
>
> # ⇩⇩ BATCH 3 IS BUILT AND WAITING ON YOUR EYES. ONE LOOK CLOSES 85 AND 67. ⇩⇩
>
> ***THE INSTALLER IS ALREADY BUILT — NO CYCLE NEEDED TO LOOK.***
> `cycle.ps1 -SkipInstall` at 31 Aug 01:14:09: ISCC exit 0,
> `C:\Users\dmont\sdout\sd-setup-W1.0-0.exe`, 4,925,443 bytes. **Run it to the
> tasks page, look, and CANCEL — cancelling writes nothing.**
>
> ```
> C:\Users\dmont\sdout\sd-setup-W1.0-0.exe
> ```
>
> **Double-click it, or an ordinary prompt; it asks for elevation itself.**
>
> ***WHAT TO LOOK FOR — 85.*** Tick *"Provide the SD API (port 4243)"*. The
> child *"Let other computers on your network reach it"* must stay **UNTICKED**.
> Then tick the child and untick it again: the parent must stay **TICKED**.
> Before this the two moved together, which put port 4243 on the network by
> default. ***WHAT TO LOOK FOR — 67***: the ssh pair does the same thing, and
> `Test-Path 'C:\Windows\System32\OpenSSH\sshd.exe'` must be **False** before
> the server-absent box means anything.
>
> ***ISCC's EXIT CODE IS NOT EVIDENCE HERE. IT COMPILED THE BROKEN VERSION
> TOO.*** No cycle and no suite run ever sees this page.
>
> ***74 IS NOT ON THIS HOST.*** It needs an **interactive uninstall** to show
> the closing disclosure, and a cycle's uninstall is `/VERYSILENT`
> (`cycle.ps1:497`), so it never appears. An interactive uninstall here would
> take the install with it — **it wants the VM, the rig that closed 39.**
>
> ***AND THE SD SERVICE WAS PUT BACK.*** `cycle.ps1` step 1 stops it and
> nothing restarts it (`:218`); it was restarted by hand and reads **Running**.
> **The installed tree is STALE** — `sd.iss` moved — which is correct and
> costs nothing until the next real cycle.
>
> # ⇩⇩ BATCH 2 IS DONE AND MEASURED. 12, 24 AND 87 ALL CLOSED. OPEN COUNT 13. ⇩⇩
>
> ***INSTALL 31 Aug 01:05:10, `sd.exe` `87701F86382AEA63`, `assert-current`
> exit 0 live.*** Both probes green on it, and **12/87's is a before-and-after
> on the same instrument** rather than a fresh green: one install earlier the
> same probe printed *"…must already hold an u"*, and now all three lines of
> message 10151 arrive.
>
> ***THE TWO PROBES LIVE ONLY IN A SCRATCHPAD AND WILL NOT SURVIVE THE
> SESSION.*** `probe-nolockmsg.ps1` (seconds, unelevated, no run token) and
> `probe-tasklock.ps1` (~15s, one consent of its own). **Neither is in
> `gplbld` and neither is wired into a runner**, so nothing re-checks 12, 24 or
> 87 ever again. **Promoting them is the owner's call**, and the cost is two
> more suite steps against a full run he has already asked to keep short —
> `nolockmsg` is the cheap one and covers the defect that hid for years.
>
> ***AND 87 IS THE ARGUMENT FOR MEASURING RATHER THAN REVIEWING.*** The bound
> is compiled in, so no unit test could have caught it, and it survived every
> source reading this project has done. It was found by looking at what a
> message actually printed.
>
> # ⇩⇩ HOW BATCH 2 GOT THERE ⇩⇩
>
> ***MEASURED ON THE 00:48:04 INSTALL, THEN THE TREE MOVED AGAIN — `sd.exe` IS
> NOW `87701F86…`, WAS `8E1264DB…`.*** A second cycle is owed:
>
> ```
> C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\cycle.ps1
> ```
>
> **Elevated PowerShell.** After it, re-run the two probes in the scratchpad —
> `probe-tasklock.ps1` and `probe-nolockmsg.ps1`, both **unelevated**, the first
> raising one consent of its own for `sd -cleanup`.
>
> ***24 IS CLOSED, AND THE CONTROL IS WHY IT COUNTS.*** A background session
> took `LOCK 5`, was killed with `taskkill /F`, and ***the lock SURVIVED the
> kill*** — without that row, `sd -cleanup` freeing it afterwards would have
> scored a pass for something the kill had already done. Then `sd -cleanup`
> elevated, exit 0, and `LIST.LOCKS` answered **"No task locks reserved by any
> user"**.
>
> ***12's BRANCH WORKS AND THE MEASUREMENT FOUND A SECOND DEFECT.*** The refusal
> printed *"no lock is held on it"* and **not** *"Possible full disk"* — the
> success anchor appears only in 10151, the disqualifier only in 1407. **But it
> arrived cut mid-word at "A WRITE must already hold an u".**
>
> ***THAT IS 87, AND IT IS BIGGER THAN 12.*** `k_error()` sizes its buffer from
> `MAX_ERROR_LINES * MAX_EMSG_LEN` (241) and bounds the write with
> `MAX_ERROR_LINES + MAX_EMSG_LEN` (84) — **`+` where the allocation used `*`**
> — so **every** error message in the product has been truncated at ~84
> characters. ***DO NOT "FIX THE TYPO"***: passing the corrected 241 would let
> `vsnprintf` write to `n + 241` in a 241-byte buffer, because `n` is already 10
> bytes of `"%08X: "` prefix. It is `sizeof(s) - n`.
>
> # ⇩⇩ BATCH 2 WAS BUILT HERE. `sd.exe` HAS MOVED TWICE. ⇩⇩
>
> ***`bin/sd.exe` IS NOW `8E1264DB…`, WAS `4732ECF6…`. THE INSTALLED TREE IS
> BEHIND THE SOURCE UNTIL A CYCLE RUNS*** — `assert-current` will refuse, and
> that is correct, not a fault to work around:
>
> ```
> C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\cycle.ps1
> ```
>
> **Elevated PowerShell.** `make sd` **exit 0, no warnings**; exactly
> `clopts.o` and `op_dio3.o` rebuilt, which is the tell that the build did the
> two changes and nothing else.
>
> ***TWO FIXED AND COMPILED, BOTH STILL OPEN BECAUSE COMPILING IS NOT
> RUNNING.*** **24** — `sd -cleanup` never released a dead session's task
> locks; the loop tested `process.user_no` where the three below it test
> `user_no`. It released **nothing** rather than the wrong thing, because
> `cleanup()` never becomes a user so that value is 0 and a free slot is 0 too.
> **12** — a `WRITE` refused for want of a lock said *"(Possible full disk?)"*;
> new message **10151** names the missing lock. **To close each: a cycle, then
> the measurement named in its row.**
>
> ***TWO EXAMINED AND DELIBERATELY NOT BUILT, BECAUSE BOTH ARE DECISIONS.***
> **28** — its only C-shaped option is a restrictive ACL written by `pdump.c`,
> and `win32audit.h` already argues against exactly that shape for this tree
> (*"rather than rebuilt from anything that could drift out of step with the
> installer"*). **The recommendation is the installer option**: `DUMPDIR` to an
> administrator-only directory with a `secure-dumps.ps1`. **16** — names *"two
> independent things to decide"*, diagnosis and recovery, and its third piece
> is §6's open question about `check_lost_users()`, which 24 does **not**
> answer: 24 changes what cleanup releases, not whether the sweep calls it.
>
> ***BUT 24 DID MOVE 16's GROUND***: 16's chain says *"`sd -cleanup` clears it"*
> and for task locks that was false. The administrator's route was broken as
> well as awkward; one of those two is now fixed.
>
> # ⇩⇩ BATCH 1 IS RUN AND GREEN. 73 IS CLOSED. OPEN COUNT 16 → 15. ⇩⇩
>
> ***`-Run b80`, UNELEVATED, `PARTIAL - 2 of 17 step(s), all exited 0`.***
> `test-stemcoverage-units` **19 of 19**; `verify-sdsyswrite` **12 of 12, zero
> FAIL**. **17 and not 16** is the arithmetic that says the new step was added
> rather than substituted. ***SPENT: `b79` AND `b80` — USE `b81`.*** `b79` bought
> nothing: it refused on `assert-current` before `verify-sdsyswrite` ran, but the
> runner had already made and removed `sdtub79`.
>
> ***68's FIX IS NOW POSITIVELY CONFIRMED, NOT INFERRED.*** `unelevated SDSYS can
> write $cred` and `… os.users` are both **True** from the session shape that
> used to fail, on a file written to be red until 68 was fixed. **Step 6's
> evidence**: probe `ZZAUD2B5E158F1D01`, before `len=53441 token=False`, SD
> answered *"User not allowed in requested account"*, after `len=53754
> token=True`. ***THE GROWTH WAS 313 BYTES, NOT ONE RECORD*** — `LOGTO SDSYS`
> audits its own elevation — **which is why the check is the NAME and not the
> size**. The unelevated process could not read the file at all (`icacls …
> Access is denied`), so the three-step shape was forced by the ACL.
>
> ***THE ONE THING THAT COST A RUN, AND IT IS WRITTEN UP IN `assert-current.ps1`
> FOR THE FOURTH TIME***: a new `gplbld` script must be listed on
> `$neverShipped` **in the commit that creates it**, or the tree reports STALE
> merely because the file exists and every verifier calling `assert-current`
> refuses. `test-stemcoverage-units.ps1` was not listed, so `b79`'s
> `verify-sdsyswrite` exited **2** — refused, nothing measured — while the step
> that made the tree stale had itself passed in the same run.
>
> ***AND `-Only` WITH TWO NAMES USED TO NEED QUOTING — FIXED, BOTH FORMS NOW
> BIND.*** `-Only a,b` failed parameter transformation before anything ran,
> because PowerShell parses `a,b` in argument position as an ARRAY and `$Only`
> was `[string]`; only `-Only 'a,b'` worked, and every CLAUDE.md example is
> single-name so nothing said so. **Both runners are `[string[]]` as of 31 Aug
> 2026** and join at the call site, so `suite-only.ps1` and its **48** unit tests
> are untouched — one copy of the filter still decides what runs. **Measured on
> all four forms**: no `-Only` and `-Only ''` stay falsy and pass through, `a,b`
> and `'a,b'` both join to `a,b`.
>
> ***BATCH 1 WAS: 73's MISSING LEG AND 86's CHECKER.*** Both are
> `gplbld` only — no cycle, no source under `gplsrc` or `sdsys`, nothing
> installed. **73** gains step 6 of `verify-sdsyswrite.ps1`, the positive control
> on the SESSION: the audit trail is the one protected store `sdusers` may
> append to, so a green step 6 means any failure on the two write rows is about
> `$cred` and `os.users`, and a red one means the session itself is the problem
> and those rows say nothing. ***IT HAS NOW RUN AND IS GREEN — see the b80 block
> above; this paragraph described it while it was still unrun.*** **86**'s checker is `test-stemcoverage-units.ps1`, and it
> found `sdprof` and `sdsw` on its first run, which is **four** families missed
> across three occasions. ***IT IS NOW A STEP IN `VerifyInstall1`, SO THE
> UNELEVATED HALF IS 17 STEPS, NOT 16*** — a `16 of 16` on the next run means it
> was substituted rather than added, which is the arithmetic 82 was checked by.
>
> ***`b78` IS SPENT — USE `b79`.*** The owner ran
> `VerifyInstall2.ps1 -Run b78 -Only verify-tiers`: **33 of 33 PASS, exit 0**,
> `assert-current` clean against the 22:42:46 install. **That closes `b77`'s four
> failures** — `omit list length 41/41` and `shipped TIER.OMIT.STANDARD 0/0`.
>
> # ⇩ THE CYCLE IS PAID. 56, 57 AND 31 ARE IN AND MEASURED. ⇩
>
> ***CYCLE 29 Aug 10:35:46, `-Run b59`. ELEVATED 19 OF 19 — 397 PASS, 0 FAIL,
> 0 SKIP, GREEN FOR THE FIRST TIME. PRE_RELEASE 31 IS CLOSED.*** Read H.1 for
> the numbers and PRE_RELEASE 59 for the five unelevated failures, which are
> the harness and not the product. ***USE `b60`; b54–b59 are spent.***
>
> ### ⇩ WHAT TO PICK UP, IN ORDER ⇩
>
> # ⇩ HANDOFF, 29 Aug 2026. GREEN. NOTHING IS IN FLIGHT AND NOTHING IS HALF-BUILT. ⇩
>
> ***OUT OF CREDITS AT 19:10 — AND THEN A TABLE FIX WAS STARTED AND LEFT
> HALF-APPLIED. THE 82nd SESSION FINISHED IT.*** **"Nothing is half-built" was
> true of the commit and false of the working tree**: `PRE_RELEASE_FIXES.md` sat
> **uncommitted** with the closures of 56, 57 and 58 and the new entry 62, and
> two pieces missing — **row 56 unstruck against a section saying DONE**, and
> **NEXT FREE ID still reading 62**. `test-fixlist-units` caught both.
> ***NOTHING HAD DIVERGED FROM GitHub***: `main` and `origin/main` were both
> `c6165b6`. **The lesson for a handoff line: "committed and pushed" is a claim
> about `git log`, and `git status` is the other half of it.**
> Install **29 Aug 18:55:20**, `sd.exe` **`4732ECF659E8DB40`**,
> `assert-current` **exit 0 live**, `check-stale-leads` **exit 0**,
> `test-fixlist-units` **203 / 0**, **open count 18**.
>
> ### ⇩⇩ HANDOFF, 30 Aug 2026, END OF THE 85th SESSION. START HERE. ⇩⇩
>
> # ⇩⇩ CYCLED AND RUN. `-Run b73` GREEN IN BOTH HALVES: 37 STEPS, 693 PASS, 0 FAIL. ⇩⇩
>
> Install **20:24:50**, `assert-current` **exit 0 live** in the step transcripts.
> **UNELEVATED 16 OF 16 (278 `[PASS]`), ELEVATED 21 OF 21 (415 `[PASS]`), ZERO
> `[FAIL]` ANYWHERE.** ***COUNT `[FAIL]` WITH THE BRACKETS*** — a bare `FAIL`
> also matches `verify-fold`'s negative-control row. **Two steps use no `[PASS]`
> marker at all and were read separately**: `verify-sdsysgate` (*"10 decisive
> check(s), 0 failed"*) and `verify-apiidentity` (a four-row table). **The step
> logs are UTF-16** — `grep` finds nothing in them until the nulls are stripped,
> which reads exactly like a clean file.
> ***SPENT: `b54`–`b73`, `sdswa1`–`sdswa5`, `sdtierv`, `sdtierw`, `sdapiaz1`.
> USE `b74`.***
>
> ***82 IS CLOSED.*** `test-tiercounts-units.ps1` is the **first** banner in the
> `VerifyInstall1` log, **ahead of `verify-credacl`**, and the unelevated half
> ran **16 of 16** — up from 15, which is the arithmetic that says the new step
> was added rather than substituted. **676 → 693 is exactly its 13 plus 65's
> four**, which is how the totals were reconciled rather than eyeballed.
>
> ### ⇩⇩ HANDOFF, 30 Aug 2026, END OF THE 85th SESSION. START HERE. ⇩⇩
>
> ***CYCLED AND RUN. `-Run b77`: 37 STEPS, 702 `[PASS]`, 4 `[FAIL]` — AND ALL
> FOUR ARE ONE INSTRUMENT, NOT THE PRODUCT.*** Install **22:44**, unelevated
> **16 of 16** (278 PASS, 0 FAIL), elevated **20 of 21** (424 PASS, 4 FAIL).
> ***SPENT: `b54`–`b77`. USE `b78`.***
>
> # ⇩⇩ 1. THE ONE THING THAT MUST BE FIXED, AND IT IS THE OWNER'S FINDING ⇩⇩
>
> ***THE TWO API TASKS ARE A LINKED PAIR — TICK OR UNTICK ONE AND THE OTHER
> MOVES.*** Owner, watching the wizard during this batch's install: *"the two API
> entries are linked together like the ssh entries were before they were fixed.
> If you select or delete one, you select or delete both."* **PRE_RELEASE 85,
> re-opened.**
>
> **The cause is a missing flag.** `apiremote\apinetwork` has no
> **`dontinheritcheck`**, so Inno checks the child whenever the parent is
> checked. ***THAT REVERSES THE WHOLE POINT OF 85***: ticking *"provide the SD
> API"* re-ticks *"let other computers reach it"*, so the default opens **port
> 4243 to the network** again.
>
> ***THE PATTERN TO COPY IS THREE LINES AWAY, AT `sd.iss:187-193`:***
> `Flags: checkablealone` on `sshserver`, `Flags: unchecked dontinheritcheck` on
> `sshserver\sshremote`. **Mine has neither**, and additionally puts a
> `GroupDescription` on the CHILD that the ssh child does not have. **Three
> flags, and it needs its own cycle.**
>
> ***AND THE LESSON IS ABOUT THE CAVEAT I WROTE.*** *"Only ISCC can judge
> `sd.iss`"* — ISCC judged it fine. **ISCC CHECKS THAT TASKS COMPILE, NOT THAT
> THEY BEHAVE.** No cycle and no suite can catch this: the wizard is interactive.
> **It took the owner's eyes on a real install.**
>
> # ⇩⇩ 2. THE FOUR FAILURES, ALREADY FIXED, NEEDING ONLY A RUN ⇩⇩
>
> All four are `verify-tiers` and all four are **42-against-41**:
> `shipped TIER.OMIT.STANDARD matches this test: expected 0, got 1`,
> `omit list length: expected 42, got 41`, and two more.
> ***THE PRODUCT WAS RIGHT THROUGHOUT***: `sdtiertb771 COUNT VOC: expected 355,
> got 355` **PASS**, installed list 42 lines with `sort.item` gone.
>
> **`verify-tiers` carries its OWN copy of the withheld NAMES** and only the
> count constant had been updated. Caught by **that file's own cross-check**.
> ***`test-tiercounts-units` DID NOT AND CANNOT*** — it reconciles the COUNTS
> each verifier claims, and both counts were already right. **Same shape as 82,
> one level down.** Fixed; 41 names both sides, `Compare-Object` difference **0**.
> **`gplbld` only, no cycle — the four rows should go green on `b78`.**
>
> # ⇩⇩ 3. WHAT `b77` PROVED ⇩⇩
>
> - ***83, on the decisive branch***: `verify-delaccount` **54 of 54, zero FAIL**
>   (was 53/1), and the row that flipped is this one —
>   `the ProfileList entry was KEPT with it: expected True, got True`, with the
>   pin biting, 10075 shown and the pair recorded. **The message stopped lying
>   without being reworded**, which is why that shape was chosen.
> - ***44, in the real scenario rather than a fixture***: `verify-doors` printed
>   `:LOGTO SDDRB77A` / `Unable to change to new directory` / `The grant is in
>   place, but this sign-in cannot use it yet.` — all three together.
> - **7's product half**, above. **65 reproduced again**, both arms.
>
> ***TWO ARE DONE, INSTALLED AND NOT WITNESSED, AND SAY SO:*** **8** — nothing in
> the suite presses F1, so no run can show 10149; one keystroke witnesses it.
> **79** — the wording is confirmed on the install, but **every verifier types an
> explicit `Y`**, so no run exercises a default.
>
> # ⇩⇩ 4. START WITH THE FREE TESTS, THEN `-Only`, THEN A FULL RUN ⇩⇩
>
> **NINE** free tests, seconds, no install or elevation — all run 30 Aug 2026,
> all exit 0: `suiteonly` 48/48, `tiercounts` 13/13, `fixlist` **223**/0,
> `verdict` 126/126, `sdtestuser` 51/0, `sysmsg` 43/0, `deletioncheck`,
> `check-stale-leads`, and ***`stemcoverage` 19 of 19 — NEW, PRE_RELEASE 86***.
> **Then the cheap targeted
> run for 85's fix, ELEVATED:**
> `C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\VerifyInstall2.ps1 -Run b78 -Only verify-tiers`
> — but ***85 needs a CYCLE first***, because `sd.iss` only takes effect through
> one, and the wizard has to be looked at by a person.
>
> # ⇩⇩ THE FULL SUITE IS NO LONGER THE DEFAULT. OWNER'S RULING, 30 Aug 2026. ⇩⇩
>
> *"Add `-Only`, and drop the full run to milestones."* **A full run is ~20
> minutes** — 4.6 unelevated, 15 elevated — and the step that decides a change
> is usually **30 to 90 seconds** of it. **CLAUDE.md carries the rule**; the
> short form is: free unit tests on every change, `-Only` for the step that
> decides it, **full suite before a release and before a handoff.**
>
> ***BOTH HALVES ARE PROVEN. NOTHING ABOUT `-Only` IS UNRUN.***
> `VerifyInstall2.ps1 -Run b76 -Only verify-fold`, elevated, 30 Aug 2026:
> `***** PARTIAL RUN - 1 of 21 step(s), because -Only was given *****`, the step
> named, *"This run says NOTHING about the steps it did not run"*, `verify-fold`
> **10 of 10**, `===== post-cycle summary - PARTIAL, 1 of 21 step(s) =====`, and
> `VerifyInstall2: PARTIAL - 1 of 21 step(s) run, all exited 0.` **Seconds
> instead of fifteen minutes**, and `assert-current` ran inside the step and read
> **exit 0**, so the `$neverShipped` addition holds on the elevated path too.
> ***SPENT: `b54`–`b76`. USE `b77`.***
>
> ***ALWAYS TAKE A FRESH TOKEN, EVEN FOR A ONE-STEP RUN.*** `b76` created no
> account — `verify-fold` makes SD files and cleans them up — so it is arguably
> still usable. **Working that out per step is exactly the judgement that costs a
> run when it is wrong**, and tokens are free. Burn one.
>
> ***PROVEN UNELEVATED, BOTH DIRECTIONS, NO SUITE SPENT:***
> `VerifyInstall1.ps1 -Yes -Only test-tiercounts-units` → `PARTIAL RUN - 1 of 12`,
> 13/13, `PARTIAL - 1 of 12 step(s) run, all exited 0`, **exit 0 in seconds**.
> `-Only verify-nope` → **exit 2**, naming `verify-nope.ps1`, listing the valid
> names, *"Nothing was run"*. `-Only` with `-ThenElevated` → **exit 2** before
> anything is spent, printing both commands.
>
> ***AND THE REFUSAL LISTED ONLY THE STEPS THAT RUN WOULD HAVE MADE*** —
> `verify-nocase` and `verify-lineendings` were absent because no `-Run` meant
> they were skipped. **That is why the filter is applied LAST**, after the door
> and write steps are appended and after the test-account skips.
>
> # ⇩⇩ `-Run b75`: 37 STEPS, 705 PASS, 1 FAIL — AND THE 1 IS 83. ⇩⇩
>
> **Unelevated 16 of 16 (278 `[PASS]`), elevated 21 of 21 (427 `[PASS]`).**
> ***84 IS CLOSED***: `verify-notyet` **14 of 14**, up from 12/13, with both the
> repaired check and its new matcher control green.
>
> ***THE SINGLE FAILURE IS 83 AND IT IS IDENTICAL TO `b74`*** —
> `verify-delaccount` **53 PASS + 0 N/A of 54**, failing only
> `the ProfileList entry was KEPT with it`. **It will keep failing until 83 is
> ruled on. That failure is real: do not silence it.**
>
> ***AND 65 REPRODUCED ON A SECOND RUN, SO THE PIN IS DETERMINISTIC*** —
> `the pin blocked the profile removal (this leg is decisive)` and
> `os.users record is gone (the DECISIVE one)` both green again, with step 3's
> subject still taking status 0 and still saying `CONFIRMATORY, not decisive`.
>
> # ⇩⇩ `-Run b74`: THE RIG BIT. 65 IS CLOSED, AND IT FOUND TWO MORE THINGS. ⇩⇩
>
> **19 of 21 elevated steps exited 0; the two that did not are `verify-notyet`
> (84, now fixed) and `verify-delaccount` (83, open and real).**
>
> ***65 IS CLOSED, ON THE DECISIVE BRANCH, WHICH TOOK THREE ATTEMPTS TO REACH.***
> `the pin blocked the profile removal (this leg is decisive): expected True, got
> True`, then ***`65: status 6/7/8 - the os.users check below is DECISIVE`***, and
> on that branch ***`os.users record is gone (the DECISIVE one)`***. **10075
> shown, the directory KEPT, the reclaim record written and naming it, 10123
> absent.** `verify-delaccount` **53 PASS / 1 FAIL of 54**. **Step 3's subject
> still took status 0 and still said so**, so one run now covers both arms —
> which is exactly what the third subject was bought for.
>
> # ⇩⇩ 36's RECLAIM PROMISE WAS KEPT END-TO-END, AND NOBODY HAD EVER SEEN IT ⇩⇩
>
> From `C:\ProgramData\SD\reclaim-profiles.log`, **21:18:26**, after a later step
> restarted the service:
>
> ```
> --- S-1-5-21-...-3863
>     sid=...-3863 account=SDDELB74H directory=C:\Users\sddelb74h
>     before: directory present, ProfileList entry gone
>     after:  directory gone, ProfileList entry gone
>     reclaimed - both halves gone, record cleared
> reclaim-profiles: 12 considered, 1 reclaimed, 11 still pending, 0 refused
> ```
>
> ***1 OF 12, AND IT WAS THE RIGHT ONE.*** The other eleven were still pinned by
> live hives and stayed pending. **A sweep that reclaimed everything would have
> proved much less than one that reclaimed exactly the pair whose lock had gone.**
>
> # ⇩⇩ 83 — AND THE SWEEP'S LOG IS THE SECOND WITNESS FOR IT ⇩⇩
>
> ***`before: directory present, ProfileList entry gone` IS THE SPLIT 36 EXISTS TO
> PREVENT***, read by a different program four minutes after `verify-delaccount`
> reported the same thing. `DELETE_USER:270`'s `Remove-CimInstance` removes both
> halves in Windows' own order, so the entry can go while the directory stays;
> the guard at `:281` governs only **SD's own second removal** and never fires.
> **The code measures honestly — the MESSAGE over-promises**: 10075 says *"SD has
> kept the profile's registry entry with the directory"*, and that clause was
> false on the only run that has ever printed it. **Three shapes in the entry;
> the choice is yours.** ***THE RECOVERY IS NOT AT RISK*** — the sweep reads the
> record, not `ProfileList`, which is why it still worked.
>
> # ⇩⇩ WHY THAT RIG HAD TO BE BUILT — 65 AFTER `b73` ⇩⇩
>
> `verify-delaccount` went **42 PASS / 0 FAIL / 0 N/A** (38 → 42) and all three
> states were measured — `os.users\SDDELB73S` **absent at preflight**,
> **`yes | yes` after `create.account`**, **gone after `delete.account`**.
> ***BUT ITS OWN LINE 89 READS "65: status 0 - the os.users check above is
> CONFIRMATORY, not decisive", SO IT EXERCISED THE ARM THAT ALREADY WORKED.***
>
> ***AND THAT IS STRUCTURAL, NOT LUCK — RE-RUNNING `b74` WOULD DO THE SAME
> THING.*** Step 2 makes the profile with **`CreateProfile`**, which never loads
> a hive, so `Remove-Item` on `C:\Users\<name>` always succeeds and
> `DELETE_USER:282` always reaches `exit 0`. **As built the verifier CANNOT reach
> 6/7/8.** The status is decided by `$dirleft`/`$keyleft` at
> `DELETE_USER:277-283`, so the decisive branch needs the profile directory to be
> **undeletable while the verb runs** — an open handle without
> `FILE_SHARE_DELETE` under it is enough, or `LoadUserProfile` with no matching
> unload.
>
> ***ONE RIG SETTLES TWO ENTRIES, AND IT IS NOW BUILT.*** `verify-delaccount.ps1`'s
> own header said its keep-both arm *"has not run on this host yet"* — so **36's
> keep-both assertions (the reclaim record, 10075's rendering) have never fired
> either.** Step 6 pins one file inside `<prefix>h`'s profile open with
> `FileShare.Read`; deleting a file needs `FILE_SHARE_DELETE` from every other
> handle on it, so the pin blocks `Remove-Item` on the file, which blocks
> `-Recurse` on the directory — **no interop, no logon, no password.**
> ***A THIRD SUBJECT RATHER THAN PINNING THE FIRST WAS THE OWNER'S CALL***:
> pinning `<prefix>s` cost nothing extra per run but would have traded status 0's
> coverage away for 6/7/8's. **Step 3 and its checks are untouched.**
>
> ***A CASE-ONLY DIFFERENCE WOULD HAVE FAKED A PASS AND DID NOT.*** The account
> is `sddelb73s`; the record is **`SDDELB73S`**, because `grant.os.access` keys on
> `acc.uname`. **A `-ceq` in `Get-OsUsersRecord` would have scored step 1 FAIL and
> step 3's *"gone"* a pass for the wrong reason.** It is case-insensitive on
> purpose and the comment there says so — do not tighten it.
>
> ***`verify-delaccount`'s SD-MADE SUBJECT IS AN ADMINISTRATOR NOW.***
> `<prefix>s` is created `ADMINISTRATOR BOTH`, because only that tier is given an
> `os.users` record and a STANDARD subject would have scored *"the record is
> gone"* by never having had one. It is in Windows Administrators for the seconds
> it exists. **The control `<prefix>b` is deliberately not.**
>
> ***TWO ONE-LINE RULINGS ARE WAITING AND BOTH ARE NOW CHEAP TO GIVE.*** 7 and 9
> were *"decide"* entries; the deciding information was already in the record and
> is now in each entry.
>
> - **7 — `sort.item`: confirmed an oversight, not a decision.** `d913eac`'s
>   read-only-inspector ruling **names `list.item` and not `sort.item`**, which
>   are `$QPROC` 10 and 11 — one program. **Fixing it is 82's shape**: omit
>   43→42 lines, **STANDARD 354 → 355**, PROGRAMMER and ADMINISTRATOR unmoved,
>   and `verify-tiers.ps1`, `verify-tierapi.ps1` and `test-tiercounts-units.ps1`
>   all carry 354. **Not built — tier membership has always been his.**
> - **9 — `umask`: half of it was ruled on 24 Aug and the entry did not know.**
>   `d913eac` deleted `voc_template/umask` outright, so *"ship a VOC record"* is
>   already refused. ***AND `op_umask` IS LIVE — `CPROC:325` calls `umask(002)`
>   at every start-up***, so *"delete the routine"* taken literally breaks
>   start-up. **The dead part is `int.umask` alone** (`CPROC:3371`, verb 35).
>
> ***THE HABIT THAT PAID FOR ITSELF TWICE: RUN THE FREE UNITS TESTS FIRST.***
> All four are green as of 30 Aug 20:15 — `tiercounts` 13/13, `sdtestuser`
> 51/0, `verdict` 126/126, `fixlist` **218/0** — plus `check-stale-leads`
> **exit 0**, and **a whole suite run (`b70`) was spent discovering what
> `test-tiercounts-units` names in under a second.** They need no install, no
> elevation and no token.
>
> ### ⇩ EVERYTHING BELOW IS THE 84th SESSION'S HANDOFF, STILL CURRENT ⇩
>
> ***TWO THINGS BUILT AND NOT YET SEEN, NEITHER PROVABLE BY A CYCLE:***
> **74**'s uninstall disclosure now names all four groups, and it shows only at
> an **interactive** uninstall — `UninstallSilent` skips it, so it wants the
> path 39 used. **77**'s dialog lost a sentence that went stale within hours
> (it told the reader to edit `sd.conf` by hand, and **78** shipped `remote.api`
> in the same install); that needs a **second install over an existing tree**,
> since a cycle deletes it.
>
> ***THE BEST REMAINING RETURN ON ONE SITTING IS A VM CLONE WITH NO OpenSSH.***
> **67**'s absent-server wizard case, **76**'s open branch of the scope default,
> and **78**'s `ssh.server install|remove` all want that same rig. One guest,
> three legs closed. `Windows 11 - Template` is the clone source and has no
> OpenSSH capability — **do not prime it with one, that is 76's own warning.**
>
> ***AND `b71` IS RECORDED RATHER THAN TIDIED AWAY.*** It stalled after step 9
> wrote `OK`, both processes at exactly **0 CPU**, no children but a console,
> nothing executing; step 9 itself had completed cleanly. **The block was on the
> next console write**, which reads as a wedged console rather than a defect.
> **Unproven — file it only if it recurs at a DIFFERENT step.** It left
> `sdacctb71`, `sdaclb71`, `sdcatgb71` in the register and `SDACCTB71` on disk.
>
> # ⇩⇩ `-Run b72`: GREEN IN BOTH HALVES. 36 STEPS, 676 PASS, 0 FAIL. ⇩⇩
>
> ***UNELEVATED 15 OF 15 (265 `[PASS]`), ELEVATED 21 OF 21 (411 `[PASS]`), ZERO
> `[FAIL]` ANYWHERE.*** Install **18:03:57**, `assert-current` **exit 0 live**.
> ***COUNT `[FAIL]` WITH THE BRACKETS*** — a bare `FAIL` also matches
> `verify-fold`'s negative-control row, which is a check working correctly.
> **And the runner's own log reads 0 PASS / 0 FAIL, which is EXPECTED under
> `-Quiet`** — the per-check markers live in the 21 step logs, so a non-zero
> PASS total across those is the control that the logs were actually read.
>
> ***SPENT: `b54`–`b72`, `sdswa1`–`sdswa5`, `sdtierv`, `sdtierw`, `sdapiaz1`.
> USE `b73`.*** **`b71` bought nothing**: it stalled after step 9 wrote `OK`,
> with both processes at exactly 0 CPU, no children but a console, and nothing
> executing. **Step 9 itself had completed cleanly** (*"10 decisive check(s),
> 0 failed"*, `sdgateb71` removed). **The block was on the next console write**,
> which points at a wedged console rather than a defect — unproven, and worth
> filing only if it recurs at a DIFFERENT step. `b71` left `sdacctb71`,
> `sdaclb71`, `sdcatgb71` in the register and `SDACCTB71` on disk.
>
> ***54 CLOSES ON THIS RUN.*** `verify-profiledir` is step 13 and has now run
> twice, `b70` and `b72`, exit 0 both times, with its prefix derived from the
> `-Run` token each time — a fixed one would have passed on `b70` and failed on
> `b72`, so the second run is what proves the wiring. **36's last leg had never
> fired since the day it was written.**
>
> ***AND 82 IS WHAT THIS RUN LEFT BEHIND.*** `test-tiercounts-units.ps1` is in
> neither runner. It caught the stale 416 in under a second when finally run, and
> a whole suite run had already been spent finding the same thing. **Run it
> before any suite run that follows a change to either tier list.**
>
> # ⇩⇩ THE TASK TABLE IS FULLY CLOSED. EVERYTHING LEFT IS IN PRE_RELEASE_FIXES. ⇩⇩
>
> ***H.2 WAS THE LAST OPEN ROW AND IT IS NOW ➖, COMBINED INTO PRE_RELEASE 80.***
> Owner's ruling, 30 Aug 2026: *"wrap all the outstanding documentation
> pre-release tasks into a single documentation audit task that validates and
> updates the whole documentation tree against the final install image … you
> take control of the gap analysis, you validate, correct and build all the
> documentation both yours and the other AI's."* **H.2, 34 and 55 are one task
> now**, and 80 runs **LAST, just before the 1.0 wrap-up**.
>
> ***DO NOT READ "TASK TABLE CLOSED" AS "NEARLY DONE".*** Every row is ✅ or ➖,
> which means only that nothing is left that the TABLE tracks. **27 fixlist
> entries are open, three of them blockers — 72, 77 and 80.** The table is the
> authority on tasks; PRE_RELEASE_FIXES is now the authority on what ships.
>
> ***WHY THE DOCUMENTATION WAITS, AND IT IS NOT PROCRASTINATION.*** The model
> has moved seven times in a week — 56, 67, 75, 76, 77, 78, 79 — and H.2's own
> row predicted the cost of not waiting: *"writing a reference against a model
> in motion is how the tester set described `encrypt.field` for a week after it
> was deleted."* **Wiring `release.ps1` early would have been worse than not
> wiring it**: both generators `exit 1` on a roster disagreement, and 78 alone
> takes the TCL verb count 143 → 146, so every run would refuse until the pages
> caught up.
>
> # ⇩⇩ 77 IS FIXED AND 78 IS BUILT. BOTH NEED ONE CYCLE. ⇩⇩
>
> ***RUN `cycle.ps1` ELEVATED — `assert-current` IS RED AND THIS IS BASIC.***
> `C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\cycle.ps1`
>
> ***THEN READ `verify-tiers` FIRST***: ADMINISTRATOR moves **416 → 419** and
> **PROGRAMMER 396 and STANDARD 354 must NOT move.** That asymmetry is the check
> on the arithmetic — if either of the other two moved, one of the three new
> verbs reached `newvoc`, which hands it to every account SD creates.
>
> ***78, ALL THREE VERBS, BUILT AND UNCOMPILED.*** `remote.api on|local|off`,
> `remote.ssh on|off`, `ssh.server install|remove`. Three new scripts
> (`api-listener.ps1`, `restart-sd.ps1`, `remove-ssh.ps1`), three `gpl.bp`
> programs, three `voc_template` records, three `TIER.ADD.ADMINISTRATOR` lines,
> **messages 10131–10148**, and the changelog.
>
> ***TWO DEFECTS WERE CAUGHT BEFORE THE CYCLE, WHICH IS THE POINT OF LOOKING.***
> The includes were wrong — `K$ADMINISTRATOR` and `K$WINPATH` are in
> `INT$KEYS.H`, not `KEYS.H` — so the first draft would have failed BCOMP on
> unknown symbols and cost a whole cycle to find out. And `restart-sd.ps1` is
> deliberately not `Restart-Service`, because `cycle.ps1:299` already measured
> that stopping the service does not always take `sdwind` with it.
>
> ***A CLAIM IN `cycle.ps1` IS WRONG AND IS CORRECTED IN THE NEW CODE.*** It says
> *"sd -stop refuses while users are logged in"*. **It does not** —
> `stop_sd()` (`gplsrc/sysseg.c:766`) SIGTERMs every user-table entry with a uid
> and a pid > 0, with no such check. **So `remote.api`'s restart ends the
> administrator's own session**, which is why its Y/N warning comes before the
> restart and nothing printed after it matters. `cycle.ps1`'s comment still
> needs fixing — it is not wrong about what to DO, only about why.
>
> ***OWNER'S RULE, 30 Aug 2026 — Y/N PROMPTS MUST SHOW THEIR DEFAULT***, written
> `<y>/n` or `y/<n>`. **The sweep is FILED AND MOSTLY DONE as 79**: 11 messages
> reworded, 9 code sites changed. ***THE PROMPTS WERE NOT ALL ONE SHAPE, WHICH
> IS THE THING TO KNOW*** — three of them (`3044`, `10008`, `6588`) **already
> defaulted to N and simply never said so**, so they needed wording only.
> **`6521` is used twice in `ED`** and a `head -1` grep found one.
> ***AND THE MESSAGES CANNOT BE EDITED BY HAND***: each ends in a trailing space
> that `Edit` and `Write` both strip, so a scripted byte substitution was used
> under CLAUDE.md's own exemption, verified at +2 bytes per file with the tail
> intact. **Left open in 79 on purpose**: the three multi-way prompts (Y/N/Q,
> Y/N/A, Y/N/Q/?) whose default is a ruling; `ED`'s `yes.no`, which has **six**
> callers of which only one is inventoried; and four dead messages.
>
> # ⇩⇩ 77: THE UPGRADE DIALOG SAID THE OPPOSITE OF WHAT RAN — FIXED. ⇩⇩
>
> ***IT FIRES ON `not DataTreeAbsent`; `DataTreeUpgrade` IS `not
> DataTreeWasAbsent` — THE SAME PREDICATE — AND IT GATES THE UPGRADE BRANCH.***
> So *"the newly built system files were NOT installed over it"* is printed
> exactly when they are, and *"upgrading in place is not yet supported"* has been
> false since 25 Aug. **Measured on the owner's 30 Aug reinstall**: `voc.dic`,
> `dict.dic`, `accounts.dic`, `$map.dic` and three `os.users.dic` records all
> carry **16:40:08**. **This is entry 71's stale claim shipped to users.**
>
> ***AND 78 IS FILED: `remote.api`, `remote.ssh`, `ssh.server` — the owner's
> three administrator commands.*** They close the one objection 75 left open,
> and the scripts they wrap are already installed and re-runnable.
>
> # ⇩⇩ 67's TASKS PAGE WAS WRONG AND IS FIXED — AND THE FIX IS PROVEN. ⇩⇩
>
> ***30 Aug 2026, MEASURED ON A REAL INSTALL: the server IS installed and remote
> access IS blocked.*** `sshd.exe` present, `sshd` Running/Automatic,
> `RemoteAddress=127.0.0.1`. **That also settles the dash empirically** — a
> parent in Inno's grayed state with `checkablealone` IS selected, so
> "install the server, no remote access" works.
>
> ***TWO MISSING `[Tasks]` FLAGS MEANT TWO OF THE THREE STATES COULD NOT BE
> EXPRESSED.*** Owner at the wizard, 30 Aug 2026: *"I click install the server
> and both check boxes are filled. I unclick let other computer connect and it
> also deletes installing the server."* **Read out of `ISetup.chm` rather than
> assumed a second time**: `dontinheritcheck` stops a child being ticked with its
> parent, and `checkablealone` is what lets a parent stay ticked when no child
> is — *"by default … unchecking all of the task's children will cause the task
> to become unchecked."* **Fixed on `sshserver` and `sshserver\sshremote`.**
> The dependency half never needed code and is confirmed by the same topic:
> *"A child task can't be selected if its parent task isn't selected."*
>
> ***REBUILD, THEN LOOK — NO INSTALL NEEDED.*** `-SkipInstall` stops after
> building the installer and leaves the tree alone; running the `.exe` to the
> tasks page and cancelling writes nothing.
>
> ***AND THE ABSENT-SERVER CASE IS ONLY NOW REACHABLE ON THIS HOST***: removing
> the OpenSSH capability is staged behind a **reboot**, so the first attempt
> still had `sshd.exe` on disk and the wizard correctly showed the server-present
> box. **Check `Test-Path 'C:\Windows\System32\OpenSSH\sshd.exe'` is `False`
> before reading anything into the page.**
>
> # ⇩⇩ AND: THIS INSTALL HAS NO API LISTENER. DO NOT SPEND `b70` ON IT. ⇩⇩
>
> ***THE 30 Aug CYCLE WAS INSTALLED WITH THE API BOX UNTICKED, AND UNDER 75 THAT
> NOW MEANS NO LISTENER AT ALL.*** Measured: `# APIPORT=4243` is **commented** in
> `C:\ProgramData\SD\sd.conf`, and **nothing is listening on 4243** while the SD
> service is Running. **That is 75 working exactly as ruled — it is not a
> defect.**
>
> ***BUT NINE SUITE VERIFIERS NEED THE API, AND EVERY ONE OF THEM WILL FAIL.***
> `verify-apiadmin`, `verify-apiidentity`, `verify-apiname`, `verify-apiport`,
> `verify-accountacl`, `verify-peerlog`, `verify-scramlogin`, `verify-tierapi`
> (all `VerifyInstall2`) and `verify-doors-suite` (`VerifyInstall1`). **A run of
> `b70` on this install reads as a catastrophic regression and is nothing of the
> kind.** Re-install with the API box **ticked** first, or do not run the suite.
>
> ***AND IT IS THE COST FLAGGED IN 75, ARRIVING ONE CYCLE LATER.*** The old
> behaviour of an unticked API box was *"listener up, reachable from this machine
> only"*. There is no such state now: ticked means listening AND open to the
> network, unticked means no API at all. **If the intent was "keep the API but
> shut the port", that third state has to go back — the owner's call, and this
> install is the case for it.**
>
> ### ⇩ 67, 75 AND 76 ARE CYCLED. WHAT IS PROVEN AND WHAT IS NOT. ⇩
>
> ***CYCLE RAN 30 Aug 2026 AND `assert-current` IS EXIT 0 LIVE.*** The installer
> compiled, so ISCC accepted the rewritten `[Code]` and `[Tasks]`.
>
> ***76 IS PROVEN, AND THE PROOF IS THAT THE OWNER COULD DO IT AT ALL.*** This
> machine already had ssh; he unticked "allow remote access" and the rule is now
> **`RemoteAddress=127.0.0.1`**, read live. **Before this change that box was not
> shown on a machine with an ssh server and `ApplySshFirewall` exited before
> touching anything**, so the ability to turn it off is itself the measurement.
>
> ***THE `-ScopeFile` READER IS MEASURED TOO***: against the live rule at
> `127.0.0.1` it writes `restricted`, exit 0.
>
> ***WHAT IS NOT PROVEN, SAID PLAINLY: THE "OPEN" BRANCH OF THE DEFAULT.*** I
> cannot show the box ARRIVED matching the prior scope, because nobody recorded
> what the scope was before the cycle. **Closing it needs one of two things** —
> the owner saying whether the box was ticked when he reached it, or a machine
> whose rule is `Any` at install time (a clone, per 76's own warning about
> priming the Template). **Do not claim that leg until one of those happens.**
>
> ***75 IS MEASURED ON THE INSTALLED TREE***: message **10100 is gone** (with
> `10101` present as the control), **no `$standalone` marker was written**, and
> `assert-current` counts **2984** mirrored files where it counted **2985**
> before — one file, the deleted message.
>
> ***67's ABSENT-SERVER CASE IS UNEXERCISED.*** Both this host and
> `Windows 11 - Test` already have ssh, so the install box and its indented child
> have not been seen. **That needs a clone with no OpenSSH capability**, and it
> is the one leg of the ruling nobody has watched.
>
> ### ⇩ THE COMMAND THAT BUILT THE ABOVE, KEPT FOR THE SHAPE ⇩
>
> ***RUN THIS, IN AN ELEVATED PowerShell, WHENEVER `assert-current` IS RED.***
> `C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\cycle.ps1`
>
> ***AND WATCH THE WIZARD, BECAUSE THE WIZARD IS THE CHANGE.*** `cycle.ps1`
> installs **attended** — there is no `-Silent` and `sd.iss` refuses one — so
> this cycle is also the test. **What to look for on the tasks page:**
>
> | this machine | expect |
> |---|---|
> | ssh server ABSENT | **"Install the OpenSSH server"**, and **indented under it** "Let other computers … connect over ssh". Untick the parent → the child greys out and clears. **That is the ruling, and it is Inno enforcing it, not a message** |
> | ssh server PRESENT | the remote box **alone**, no install box — and it starts **matching this machine's current firewall scope** |
>
> **The rig `Windows 11 - Test` has SD installed with both boxes unchecked, so
> it is the "already has ssh" case; this host is too.** To see the absent case
> you need a clone with no OpenSSH capability.
>
> ***THE OWNER'S RULING, 30 Aug 2026, WHICH IS WHAT 67 AND 76 NOW BUILD:***
> *"if an ssh server is installed, the user should have a separate choice to
> allow remote access. If a server is not installed the user should have two
> choices, install the server, and allow remote access. Allowing remote access
> should not be an option if they choose not to install the ssh server."*
>
> ***75 WENT IN THE SAME PASS ON HIS INSTRUCTION, BECAUSE EVERY `Check:` IN THE
> FILE CARRIED `not StandaloneChosen`.*** The mode page, both radio buttons,
> `StandaloneChosen`, `StandaloneWasMarked`, `WriteStandaloneMarker`,
> `ShouldSkipPage`, `ModeChoiceText`, `DisclosureText`'s parameter and its three
> branches, `CREATEA`'s marker read, **message 10100 and `verify-standalone.ps1`
> both deleted**. `SummaryPage` is back on `wpWelcome`. **The API box is a
> service switch now** — unticked installs the no-listener `sd.conf`.
>
> ***ONE COST OF 75 IS FLAGGED AND UNRULED — READ IT BEFORE THE CYCLE.*** There
> were three API states; there are now two. **A program on the SAME machine
> using the API now needs the box ticked, and ticking it also opens port 4243 to
> the network.** Built as ruled because the ruling is explicit; **putting the
> local-only state back is the owner's call.**
>
> ***HOW 76's HARD PART WAS AVOIDED, BECAUSE IT IS THE REUSABLE BIT.*** The
> entry hunted for a way to tell SD's own ssh server from a foreign one, and
> could not find one that survived uninstall-then-reinstall. **The ruling
> dissolves it: default the box to the truth.** `GetSshRuleIsOpen` reads the live
> `RemoteAddress` in `InitializeSetup`, so an installer who touches nothing
> changes nothing, on any server, without SD ever needing to recognise whose it
> is. **§5.9 is narrowed, not abandoned** — `sshd_config` is still never written
> for a server SD did not install.
>
> **Pre-flighted, not guessed**: `stage.py` compiles, `ssh-firewall.ps1`,
> `assert-current.ps1` and `verify-upgrade.ps1` parse with 0 errors, every Pascal
> helper is defined before its call site, and no file gained a BOM, a CR or a
> non-ASCII byte. ***ONLY ISCC CAN JUDGE `sd.iss`, AND ONLY AGAINST A STAGED
> TREE — WHICH IS THE CYCLE.*** A `[Code]` error surfaces at its build step.
>
> ### ⇩ AND BEFORE THAT, THE RUN THAT CLOSED 68 ⇩
>
> ***`-Prefix sdswa5`: 7 PASS / 0 FAIL / 0 SKIP.*** Install **30 Aug 12:02:00**,
> `assert-current` **exit 0 live**, and the installed `gpl.bp/CRED_SET` is
> **byte-identical to source** (`sha256 2657b46b…`) carrying the fix's marker —
> **so the green run measured the fix and not a stale tree, checked rather than
> assumed.** The anchor is the SUCCESS wording, `Password set for account
> SDSWA5`, where the two previous runs printed *"Unable to set password …
> status 3035/3037"*. **All three controls green, tally equals the row count.**
>
> **Spent: `sdswa1`–`sdswa5`, `b54`–`b69`, `sdapiaz1`.** The suite itself has not
> been run since `b66`; **use `b70`** when it is. *(`assert-current` was exit 0
> after that run and is RED again now, deliberately — the installer work above
> landed after it.)*
>
> ***WHAT IS LEFT, IN ORDER.*** **(1) 72's proof — the recipe is in the "72 IS
> FIXED AND NOT YET PROVEN" paragraph below**, and the provocation has to be two
> passwords that do not match, because 68 being fixed removed the failure it used
> to rely on. **(2) The four unbuilt rulings,
> 66, 67, 75 and 76 — they interact, so rule on them together.** **(3) H.2, the
> documentation**, still blocked behind 56/57 settling. **(4) 73 stays open on
> ONE leg** — its own design called for an audit/log append as the control that
> should still SUCCEED, and `verify-sdsyswrite` has no such row, so a change that
> broke append everywhere would read green there.
>
> ***THE CHANGELOG IS ALREADY WRITTEN AND NEEDS NOTHING*** — the 30 Aug entry
> *"SETTING A PASSWORD WORKS FROM SDSYS WHICHEVER WAY YOU REACHED IT"* is at the
> TOP of `sdsys/changelog` (newest first) and its closing sentence is still
> exactly true. **A session that greps its tail will conclude it is missing.**
>
> ### ⇩ HOW 68 WAS FINISHED, KEPT BECAUSE IT IS THE SAME MISTAKE TWICE ⇩
>
> ***`sdswa4` WAS 6 PASS / 1 FAIL AND THE FAILURE HAD MOVED — 3035 → 3037.***
> That is the two-stage status earning its keep on the run after it was added:
> the elevated write succeeded and only the read-back failed.
>
> ***WHY 3037 HAPPENED, BECAUSE IT IS THE SAME MISTAKE TWICE IN ONE WEEK.***
> The read-back was copied from `MODIFYA`, where it is valid, into the one file
> where it cannot be. **`secure-osusers.ps1` grants `sdusers` `(OI)(CI)(RX)`,
> read-only**, so MODIFYA's unelevated read-back genuinely works and `os.users`
> PASSED on the identical route in the same run. ***`secure-cred.ps1` grants
> `sdusers` NOTHING — not write, and NOT READ EITHER*** — so the process that
> NEEDS the fallback cannot read `$cred` back. **Measured, not reasoned: an
> unelevated shell gets `Permission denied` listing `$cred`, while
> `os.users/don` reads `y e s \r \n y e s \r \n`.** ***AND `read ... else` HID
> IT***: a permission denial and a missing record take the SAME else branch, so
> *"wrote it and could not look"* was scored as *"wrote it and it did not read
> back"*. **First the close-before-write rule applied in one file and not the
> other; now a read-back rule lifted from the file where it holds into the one
> where it does not.**
>
> ***THE FIX: THE HELPER VERIFIES ITS OWN WRITE***, being the only party that
> can read the file. It returns **2** for wrote-but-mismatched → `ER$WRITE.ERROR`,
> while any other non-zero — including `ps_script`'s `-1` for *could not run* —
> stays `ER$PERM`. **The SD-side read-back now runs only on the direct-write
> path**, where the process demonstrably has access. ***`-cne` and not `-ne`,
> bench-measured***: PowerShell's default comparison is case-INSENSITIVE and
> every value is base64, so `-ne` ACCEPTS a record differing in case alone and
> reports it verified.
>
> **Pre-flighted before the cycle, so it was not spent on a script that never
> loads**: the emitted PowerShell parsed (0 errors), round-tripped
> byte-identical, and SD saw **6 fields**; `CRED_SET` BOM-free, LF-only, ASCII,
> `then`/`end` balance unchanged from HEAD. **All of it held on the real run.**
>
> ***READ THE THREE CONTROLS BEFORE THE VERDICT.*** Setup must create the
> account, the unelevated session must have REACHED SDSYS and read it, and the
> ELEVATED control must still write `$cred`. **A green run with a broken control
> is not a pass** — that is the exact failure the file was written to avoid, and
> its own tally refuses itself if pass+fail+skip does not equal the row count.
>
> ***WHAT THE FIX IS, AS BUILT.*** 68 is two writes SD makes
> to stores an unelevated process cannot touch: `$cred` (`secure-cred.ps1` grants
> `sdusers` nothing) and `os.users` (`secure-osusers.ps1` grants read-only).
> Both now fall back to `ps_script`, which hands the work to the elevated helper
> when `K$ADMINISTRATOR` is set (`PS_SCRIPT:166`), and both read the record back
> before reporting success. **Three things were measured before a line was
> written and each would have corrupted a store silently**: the field mark on
> disk is **CRLF** (`od -c` on `os.users/don`), every value is **base64** so
> ASCII is safe (`sd_scram.c:26`), and `pstmp` is already hardened for
> credential material (`secure-psdir.ps1`, CREATOR OWNER, added 16 Aug for
> exactly this). ***AND THE ONE THING THAT WENT WRONG WAS A RULE APPLIED IN ONE
> FILE AND NOT THE OTHER***: `MODIFYA` does the elevated write AFTER `close` and
> says why; `CRED_SET` did not, and that is what `226ef0e` fixes.
>
> ***72 IS FIXED AND NOT YET PROVEN ON THE PATH THAT MATTERS.*** `DELETE_USER`
> now uses `ps_script` rather than `os.execute`, and `CREATEA` reads the
> rollback's result instead of `void`ing it (new message **10130**). The 11:25
> install carried it, but `verify-sdsyswrite`'s cleanup rows run through the
> ELEVATED helper, so they do not exercise it. **To prove it, reproduce `john`:
> from your OWN account, `logto sdsys`, `create.account user testrb none`, give
> a password, answer N.** Before the fix the account survived and the message
> said *"Nothing was created"* anyway. **Once 68 is fixed the password will not
> fail, so provoking this needs a different failure — the two passwords not
> matching will do it.**
>
> ***FOUR RULINGS ARE TAKEN AND UNBUILT, AND THEY ALL TOUCH THE INSTALLER.***
> **66** bundle the editors (decided 26 Aug, never built). **67** refuse `SSH`
> and `BOTH` when no ssh server is installed — *the condition is the MACHINE, not
> the install*, which dissolves the upgrade problem; **the open question is how
> BASIC asks, and `ospath` with a Windows path should be MEASURED before anything
> is designed around it.** **75** remove the stand-alone mode and make the two
> remote boxes service switches rather than firewall switches — mostly a
> deletion, since `sd_conf_standalone()` already is "no listener". **76** a
> machine that already has ssh is never asked and its firewall never set.
> **They interact; rule on them together rather than one at a time.**
>
> ***THE RIG IS `Windows 11 - Test` AND IT IS THE ONLY GUEST.*** Three PERMANENT
> shares — `sdout` (read-only, the installer), `xfer` (results back to
> `C:\Users\dmont\sdxfer`), `gplbld` (read-only, the tracked
> `capture-state.ps1`). Reach them by name, `\\vboxsvr\<share>`, **not by drive
> letter — adding the third share moved the letters.** SD is installed there
> with both remote boxes unchecked, which is 67 and 75's measured baseline.
>
> ***AND ONE WARNING ABOUT MY OWN ADVICE, RECORDED AS PRE_RELEASE 76.*** Priming
> the Template with the OpenSSH capability saves ~45 minutes per clone **and
> would leave every clone with no ssh question and NO FIREWALL RESTRICTION**,
> at Windows' default of `RemoteAddress=Any`. Do not do it without fixing 76
> first.
>
> ### ⇩ 30 Aug 2026 — 39 IS CLOSED ON A REAL UNINSTALL, AND THE RUN FOUND A WORSE ONE (72). OPEN COUNT 22. ⇩
>
> ***THE INTERACTIVE UNINSTALL RAN IN `Windows 11 - Test` AND THE SWEEP DID WHAT
> IT PROMISED***: `mode : REMOVE`, `keep : don`, `token: elevated`,
> **`removed 2 of 2 account(s); kept 1`**, each with `group sdu_<name> removed`
> and `user removed`. **Before/after agree** — local users 9 → 7,
> `sdusers`/`sdssh`/`sdapi` down to `don`, `sdsshonly` **empty**, `Administrators`
> untouched, and ***`sshd_config`'s SD block gone***. **`tim`, a Windows account
> SD never made, was untouched — the control this run got for free.**
> ***TWO LEGS ARE UNEXERCISED AND SAID SO RATHER THAN TICKED***: the
> last-administrator refusal never had to fire (this guest has an administrator
> outside `sdusers`), and the keep-the-database branch went untested because the
> tree came out absent.
>
> ***AND THE RUN'S REAL RESULT IS 72, WHICH IS WORSE THAN WHAT IT WAS TESTING.***
> `john` — half-created by 68's failure — is **in no group at all**: not
> `sdusers`, not `sdsshonly`, no `sdu_JOHN`. **So he was never confined** (that
> group is what denies console and RDP) **and the sweep cannot see him**, its
> candidate set being `sdusers` *"because CREATE.ACCOUNT adds every account it
> makes and nothing else does"* — **a premise 68 falsifies.** He survived the
> uninstall as an enabled Windows account with a password.
>
> ***AN INSTRUMENT FAULT OF MY OWN, RECORDED BECAUSE THE RECORD ALREADY WARNED
> OF IT.*** `capture-state.ps1` used a bare `Tee-Object`, which in PS 5.1 writes
> **UTF-16**, so the captures came back NUL-separated and `grep` matched nothing
> — the identical trap §"reading the transcripts" documents for the SD-verify
> logs, walked into one day later. **Fixed to `Out-File -Encoding utf8`.**
> ***MOVED INTO THE REPOSITORY 30 Aug 2026 ON THE OWNER'S INSTRUCTION***, and it
> is now `gplbld/capture-state.ps1` — **the canonical copy; anything under
> `C:\Users\dmont\sdxfer` is a copy for the guest to reach and may be stale.**
> **It is on `assert-current.ps1`'s `$neverShipped` list** (`:560`), which is not
> optional: a `gplbld` script that is not named there is newer than the install
> the moment it is written, and `assert-current` then refuses the tree *because
> of the new file* — the trap that cost a run on 25 Aug. **Measured after adding
> it: `assert-current` exit 0, *"no source file is newer than the install"*.**
> It takes `-OutDir` now, so it is not tied to `Y:`.
>
> ### ⇩ 30 Aug 2026 — THE 39 RIG IS SET UP. NEW ENTRIES 66 AND 67. ⇩
>
> ***67 IS THE ONE TO READ, BECAUSE IT TOUCHES THE INSTALL MODEL AND IT CAME OUT
> OF THE 39 RIG BEING SLOW.*** Owner asked why declining ssh still installs the
> ssh server. **It does**: `sshremote` and `apiremote` are FIREWALL tasks, and
> `sd.iss:719` gates the capability install on `SshServerAbsent and not
> StandaloneChosen` **without testing `sshremote`**, while `FullRadio.Caption`
> says *"optional remote ssh"*. ***AND IT IS NOT A TICKBOX***: `deny-logon.ps1:29`
> denies interactive and RDP logon but NOT network logon, so an SD account's only
> two routes are ssh and the API **even locally** — a local user reaches SD by
> `ssh localhost` with the port shut. **"No ssh server" is therefore a decision
> that nobody logs in interactively, which is a third install mode, not a
> checkbox.**
>
> ***THE ACCESS POLICY WAS RESTATED AND IT IS ALL ALREADY RECORDED — NOTHING NEW
> WAS FILED FROM IT.*** Only administrators log in directly, at the keyboard or
> through RDP/AnyDesk; OS users the customer adds get no SD; multi-user RDP is
> not supported, only a single remote session. **§5.6.2 (`:5808`) and the
> `RDPACCOUNT` deletion (HISTORY.md:11345) already carry it.** ***AND IT SETTLES
> 67's OPEN QUESTION — "does anything else need ssh?" NO***: an administrator
> reaches SDSYS by elevating at the console (`LOGIN:568`), which never touches
> ssh, so in an API-only install the ssh server has no consumer at all. **The one
> thing such an install gives up is an interactive SD session for a
> NON-administrator, and the mode page has to say so in those words.**
>
> ***A CLAIM I MADE AND HAD TO WITHDRAW, WRITTEN DOWN SO IT IS NOT REPEATED.***
> I told the owner a customer-added Windows ADMINISTRATOR still gets SD. **Wrong**
> — it conflated the data-tree ACL (`Administrators` do get filesystem access,
> `sd.iss:577`) with SD login, which refuses them at **`LOGIN:414` with 5009**
> like anyone made outside SD. 56 removed that exemption on 29 Aug and `-Run b66`
> proved it. **The wrong claim reached entry 67 before it was caught; it is
> corrected there.**
>
> ***AND A STANDING CORRECTION ON HOW TO WRITE THIS UP — THIRD TIME THE OWNER HAS
> GIVEN IT.*** *"We are not trying to prevent an administrator from making a
> non-standard system… this is our default setup, not a prevention against users
> doing whatever they want to."* **`:3772` already overrules the argument that a
> gate an elevated administrator can pass is not worth building.** The caveat is
> written into `LOGIN:410-413`, which is why it keeps being re-argued — **it is
> not wrong, it is the wrong emphasis.** State what the shipped default does and
> stop. Saved to the session memory file as `defaults-not-prevention`.
>
> ***`Windows 11 - Test` IS READY TO BOOT AND NEEDS NOTHING FROM THE HOST.*** The
> owner's first attempt at 39 was abandoned — installing in a VM was slow,
> mostly the OpenSSH capability download — and he cloned a fresh guest.
> **Both shared folders are PERMANENT on that VM (`MachineMapping`), not
> transient, so they survive the power cycles an overnight install needs**;
> the `--transient` form the record documents is for a VM that is already
> running and locked. NIC is **bridged**, which §5.9's remote-block control
> needs. ***`Windows 11 - Test` IS THE ONLY RIG — THERE IS NO SECOND GUEST.***
> An earlier `Windows 11 - Removal Test` was **deleted** when this clone was
> made, so anything in the record naming it is stale; `VBoxManage list vms`
> registers only `Beardog`, `Windows 11 - Template` and `Windows 11 - Test`.
> **The Template is the clone source, and cloning is the documented way to get
> another attempt** (24 Aug: `clonevm`, ~25 s, `--options keephwuuids,keepallmacs`).
>
> ***THE TWO CLONE OPTIONS ARE NOT A PAIR AND MUST BE DECIDED SEPARATELY —
> OWNER, 2 Sep 2026, CORRECTING A SESSION THAT DROPPED BOTH.*** The string above
> reads as one recipe and is why they got treated as one.
>
> - ***`keephwuuids` IS REQUIRED: WITHOUT IT THE CLONE IS UNLICENSED.*** Windows
>   ties its digital licence to the hardware UUID, so a fresh one is new
>   hardware and the guest deactivates. **This is the owner's correction and it
>   is not negotiable against tidiness.**
> - **`keepallmacs` is NOT wanted here.** A duplicate MAC is why
>   `sdStandalone-C1` carried *"never run both at once"* (§70), and §427 values
>   the Test guests being able to run concurrently. Let VirtualBox generate one.
>
> ***MEASURED 2 Sep 2026 ACROSS EVERY REGISTERED GUEST, WHICH IS WHAT SETTLED
> IT*** — `Template`, `Test 10`, `Test A`, `Test B`, `Test C` **all share
> hardware UUID `59d00c9d-e374-4cbd-aa87-c4cf197890aa`** and **all five MACs are
> distinct**. So `keephwuuids` without `keepallmacs` is already the practice on
> this machine; nothing here changes it, it was simply never written down with
> its reason. **VBoxManage is 7.2.14 and its own usage prints `--options=`**, so
> use the `=` form:
>
> ```
> "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" clonevm "<source>" --name "<new>" --options=keephwuuids --register
> ```
>
> | share | host | guest | mode |
> |---|---|---|---|
> | `sdout` | `C:\Users\dmont\sdout` | `Z:` | read-only — holds `sd-setup-W1.0-0.exe`, **2 Sep 14:18:50, 4,954,811 bytes** (measured 2 Sep; the cell read *29 Aug 22:04:17* until then) |
> | `xfer` | `C:\Users\dmont\sdxfer` | `Y:` | read-write — results come back to the host as text |
>
> ***THE LETTERS IN THIS TABLE ARE STALE AND `Z:` IS NOT `sdout` — USE THE UNC
> PATH. 2 Sep 2026.*** `Z:\sd-setup-W1.0-0.exe` fails with
> `CommandNotFoundException`, which reads like a missing file and is not one.
> **Measured on `Test 10`: the session was `elevated : False`, `VIRTUAL\don`,
> and its filesystem drives are `C,D,P,X,Y,Z` — so `Z:` EXISTS and simply is
> not the share holding the installer.** The likely cause is that the table
> above dates from the **two**-share era and `Template` now maps **three**
> (`sdout`, `xfer`, `gplbld`), so the auto-mounted letters shifted; **the
> mapping is not re-derived here because `Get-PSDrive`'s `DisplayRoot` answers
> it in one line on the guest and a written-down letter is what went stale in
> the first place.**
>
> ***AN EARLIER VERSION OF THIS NOTE BLAMED UAC'S LINKED TOKEN AND THAT WAS
> WRONG*** — a guess written as a mechanism, disproved by the probe in the same
> exchange. Kept visible because the wrong explanation is more plausible than
> the right one and the next session will reach for it too. **`\\vboxsvr\sdout\…`
> and `\\vboxsvr\xfer\…` work regardless**, which is why every witness block
> here is written that way and why none of them ever hit this.
>
> **And for an INSTALLER, copy it to the guest's local disk first rather than
> running it off the share** — §427 records a *"Windows cannot access
> `\\vboxsvr\sdout`"* Network Error on `Test 6` **found with an installer
> already open**. `Copy-Item` then check `.Length` against the known size before
> running it; a short copy is otherwise indistinguishable from the real thing
> until it fails somewhere expensive.
>
> ***THE INSTALLER ALREADY CARRIES 39's FIX AND NEEDS NO CYCLE*** — built 22:04:17,
> after `sd.iss` (18:52), `remove-sdaccounts.ps1` (18:48) and `stage.py` (18:51),
> and nothing shipped has changed since. `remove-sdaccounts.ps1` parse-checks
> clean, no BOM; its interface is `-Remove -Keep <user>`, report-only by default.
> **`gplbld/capture-state.ps1` is the instrument** — run it `-Label before` and
> `-Label after` in an ELEVATED **guest** PowerShell, reached over a share; it
> distinguishes "not present" from "could not read" in every section, so an empty
> list is never reported as nothing there.
> ***TWO COUPLINGS TO KNOW BEFORE THE RUN***: both uninstall prompts sit behind
> `if not DirExists(DataPath) then Exit` (`sd.iss:3521`), so the accounts question
> only fires while `C:\ProgramData\SD` still exists; and `UninstallSilent` skips
> both, which is why a cycle can never test this.
>
> ***NEW: 66, THE EDITORS ARE STILL DOWNLOADED AND UNPINNED.*** Owner, 30 Aug.
> The decision to bundle was taken 26 Aug and nothing was built. **The sharp part
> is that the editor documentation was measured against micro 2.0.15 and
> Microsoft Edit v1.2.1 while `install-editors.ps1:137` passes no `--version`.**
>
> ***AND ONE THING WITHDRAWN RATHER THAN FILED.*** The owner reported that SD's
> own verbs took only dots, not dashes. **They take both** — `CPROC:1465-1473`
> tries the verb as entered, lower, upper, then upper- and lower-case with
> hyphens changed to dots, added 18 Aug 2026. There are **zero** dash-named VOC
> records, so the fold is the whole mechanism and it is not verb-specific. He
> withdrew it as a typo; **no entry filed, and this note exists so nobody files
> one later.**
>
> ### ⇩ 64 IS RULED, FIXED, RUN AND CLOSED — NO PRODUCT CHANGE. ⇩
>
> ***OWNER, 29 Aug 2026: "LEAVE ssh, API AND `os.execute` RIGHTS THE WAY THEY ARE
> FOR THE ADMINISTRATOR'S PERSONAL ACCOUNT."*** So the `LOGTO` leak is intended
> behaviour, said out loud, and entry 64's first branch is taken: **nothing in
> `CREATEA`, `MODIFYA`, `LOGIN` or `CPROC` is touched.**
>
> ***HE GOT THERE BY SPECIFYING THE WHOLE MODEL AND THEN WITHDRAWING THE PARTS
> THAT NEEDED CODE.*** Worth reading before re-opening any of it: os.execute on
> the personal account, administrator commands by `LOGTO SDSYS`, elevated login
> straight into SDSYS, no SDSYS over ssh or the API, ssh/API per account, and
> the personal account defaulting to Developer. ***THREE OF THE SIX WERE ALREADY
> BUILT*** — `CPROC:2570-2590` checks `K$OS.ADMINISTRATOR`, calls
> `elevate('START')` for one UAC consent and sets `elev.obtained`, which is what
> `logto.authorised` accepts; `LOGIN:568` sends an elevated session to SDSYS;
> `kernel.c:240`'s `CN_SOCKET` guard keeps `K$ADMINISTRATOR` off every API
> session. **The other three were withdrawn.** *(And "Developer" is `PROGRAMMER`
> here — the tiers are STANDARD / PROGRAMMER / ADMINISTRATOR, with `SUSPENDED` a
> fourth value in `ACC$TIER` that is a state, not a tier.)*
>
> ***MEASURED FROM THE LIVE `b69` INSTALL WHILE RULING, NOT INFERRED***:
> `accounts\DON` field 5 = `ADMINISTRATOR` (`CREATEA:1583` forces it on adopt),
> `os.users\don` = `yes`/`yes`, and `don` is in `sdssh`, `sdapi`, `sdusers`,
> `Administrators`, NOT `sdsshonly`. **ssh is held twice over** —
> `sshd_config:88` names `Administrators` separately, so `sdssh` cannot remove
> it (`MODIFYA:557`). **None of the three is removable, and `os-on` cannot be
> self-granted either**: `MODIFYA:583`/`:719` key on the Windows group by SID,
> not the SD tier, and `:719` sits before the `os.users` open.
>
> ***THE FIX IS `verify-apiadmin.ps1:602`, AND IT IS RUN AND GREEN.*** A
> different claim with a different name, not an inverted boolean, which entry 64
> forbids: **the POSITIVE CONTROL** — *"the probe CAN see OS.EXECUTE run (local,
> listed administrator)"*, expecting `$true`. It does the job the API row was
> missing, since a refusal is only evidence if the probe could have seen a
> success, and while both legs were refused no run ever demonstrated that it
> could.
>
> ***MEASURED ON `-Prefix sdapiaz1`, ELEVATED, NO CYCLE SPENT*** — the product is
> unchanged and `assert-current.ps1:550` exempts the file. **22 PASS / 0 FAIL /
> 1 SKIP**, every Expected matching Observed, the new row `True`/`True`. **The
> rows either side still hold, which is what makes it mean anything**: *"API
> session was refused OS.EXECUTE by name"* `True`, *"API session CANNOT run
> OS.EXECUTE"* `False`/`False`. The SKIP is the standing `n/a` on *"API session
> is NOT running as SYSTEM"*, unanswerable once OS.EXECUTE was refused.
> `test-fixlist-units` **206 / 0**, **open count 17 → 16**.
>
> ***THE RUN LEFT NOTHING BEHIND, CHECKED***: `sdapiaz1` gone from
> `Get-LocalUser` and from `sdsys\accounts`, and **`os.users` gained no record**.
> **That narrows 65** — the orphans come from the ADMINISTRATOR-tier verifiers
> (`sdrtb69a`, `sdtapib693`, `sdtiertb693`), not from every verifier, so start
> there. `sdapiaz1` is spent; it deliberately avoided `sdapiab70`, which a later
> `VerifyInstall2 -Run b70` will take.
>
> ### ⇩ HANDOFF, 29 Aug 2026. CYCLED AND RUN. ONE REAL FAILURE, AND IT IS THE PRODUCT. ⇩
>
> ***INSTALL 29 Aug 22:04:34, `assert-current` EXIT 0 LIVE, `test-fixlist-units`
> 205 / 0, `check-stale-leads` EXIT 0, OPEN COUNT 17. EVERYTHING IS COMMITTED AND
> PUSHED, AND `git status` WAS CHECKED AS WELL AS `git log`*** — that pair is the
> gap this session opened with.
>
> ***`-Run b69` IS NOT GREEN, AND THAT IS THE FINDING RATHER THAN A FAULT TO
> CHASE.*** `VerifyInstall1` every step exit 0; **`VerifyInstall2`: 1 of 20 steps
> did not exit 0** — `verify-apiadmin` at **21/23**. Across 22 transcripts, **654
> `[PASS]` and 2 `[FAIL]`** (the same row, twice: its own log and the runner's).
>
> ***THE FAILING ROW IS THE `LOGTO` LEAK THE OWNER ACCEPTED, NOW MEASURED —
> FILED AS 64, WHICH IS THE FIRST THING TO READ.*** *"control: local elevated
> session refused OS.EXECUTE"*, **expected refused, observed it RAN**; it read
> `False`/`False` on `b67` and `b68`. **It is the product doing what it was ruled
> to do, and an existing security control saying so.** ***DO NOT JUST FLIP THE
> EXPECTED VALUE*** — that encodes the leak as intended without anybody saying it
> was.
>
> ***AND 65: `os.users` NOW ACCUMULATES ORPHANS.*** After `b69` it holds
> `SDRTB69A`, `SDTAPIB693` and `SDTIERTB693` beside `don`, and **all three
> Windows accounts are gone** — checked, not assumed. One or more per suite run.
>
> **`b54`–`b69` are spent; use `b70`.**
>
> ***ENTRY 2, ON THE OWNER'S RULING: `os.sh` / `os.exec` ARE RESTORED TO THE
> ADMINISTRATOR ARM*** (`CREATEA:1613`), where `7aee48d` removed them for a
> model reversed four hours later. ***THE `LOGTO` LEAK IS AN ACCEPTED COST, NOT
> AN OVERSIGHT*** — he was shown it and the session-flag alternative and chose
> this. **The paragraph explaining why the lines were dangerous still sits
> directly beneath them and every word of it is still true; it is simply no
> longer decisive. Do not "fix" it back without a ruling.**
>
> ### ⇩ WHAT TO PICK UP, IN ORDER ⇩
>
> | | |
> |---|---|
> | **1** | ***65 — read `DELACC` first, and start at the ADMINISTRATOR-TIER verifiers.*** `verify-apiadmin` on `sdapiaz1` left NO `os.users` record, so it is `sdrt`/`sdtapi`/`sdtiert` that leak, not every verifier. Entry 2's original text says `DELETE.ACCOUNT` removes the record *"where SD is deleting the Windows login itself"*, which is exactly what these verifiers do, so either that path is not firing or its condition is narrower than the text claims. **`gplbld` and BASIC only — no cycle needed to find out, one to fix it.** |
> | **2** | ***72 — a half-created account is in no group, so nothing confines it and no sweep can find it.*** Measured 30 Aug; it is what 39's run turned up and it is a **B**. `CREATEA` makes the Windows user, sets the password, THEN joins the groups, so 68's failure leaves an account SD has disowned. |
> | **3** | **39 is CLOSED** — the interactive uninstall ran on `Windows 11 - Test`, `removed 2 of 2, kept 1`, `sshd_config`'s SD block gone. **Two legs stayed unexercised and are named in the row, not ticked**: the last-administrator refusal and the keep-the-database branch. |
>
> ***THAT DECISION WAS TAKEN 29 Aug 2026 — SEE THE 64 SECTION ABOVE. NOTHING IS
> NOW WAITING ON THE OWNER.***
>
> ***READING THE TRANSCRIPTS HAS A TRAP THAT COST A FALSE CLEAN THIS SESSION.***
> The per-step logs under `%LOCALAPPDATA%\SD-verify` are **UTF-16**, so a plain
> `grep -a '\[PASS\]'` matches **nothing** and reports `PASS=0 FAIL=0` — which
> reads as a green run and is a dead instrument. **Strip the NULs first**
> (`tr -d '\000' < log | grep …`) **and check the PASS count is non-zero before
> believing the FAIL count.** On `b69` that is the difference between "654 and 2"
> and "clean".
>
> ### ⇩ `b68` WAS GREEN AND 62 IS CLOSED. ⇩
>
> ***`-Run b68`: `VerifyInstall1` every step exit 0, `VerifyInstall2` 20 OF 20***
> — the new step joined that half — **655 `[PASS]`, zero `[FAIL]` across 22
> transcripts. `b54`–`b68` are spent; use `b69`.**
>
> ***62 IS MEASURED AND THE `B?` RESOLVES TO "NOT A B".*** `verify-sdsysgate`
> **10 decisive checks, 0 failed**: a real non-administrator landed in its own
> account over ssh and its `LOGTO SDSYS` was ***refused BY IDENTITY —
> `reason=not an administrator`*** in the audit, with **both disqualifiers
> absent** (no `reason=elevation refused or unavailable`, so `elevate('START')`
> was never reached; no `ELEVATION GRANTED account=SDSYS`). **The verifier stays
> a standing suite step, so the property cannot silently regress.**
>
> ### ⇩ CYCLED, SUITED AND VERIFIED — 63 IS CLOSED TOO. ⇩
>
> ***INSTALL 29 Aug 20:31:49, `sd.exe` `4732ECF659E8DB40`, `assert-current`
> EXIT 0 LIVE*** — *"no source file is newer than the install"*. The twelve
> `voc_template` records of PRE_RELEASE 63 are in it.
>
> ***`-Run b67` IS GREEN IN BOTH HALVES***: `VerifyInstall1` every step exit 0,
> `VerifyInstall2` **19 of 19**, **655 `[PASS]` and zero `[FAIL]`** across 21
> transcripts. **`b54`–`b67` are spent; use `b68`.**
>
> ***AND 63 IS VERIFIED BY THE ONLY THING THAT COULD*** — an elevated `listf` in
> SDSYS. All sixteen files now carry a description, **zero bare type codes left
> in the column**, and ***`$MAP` still reads `DH`***, which is the control: it is
> the row that started 61 and it was never broken.
>
> ***READING THOSE TRANSCRIPTS HAS A TRAP AND IT COST A FALSE ZERO HERE.***
> The per-step logs under `%LOCALAPPDATA%\SD-verify` are **UTF-16**, so a plain
> `grep -a '\[PASS\]'` matches **nothing** and reports `PASS=0 FAIL=0` — which
> reads as a clean run and is a broken instrument. **Strip the NULs first**
> (`tr -d '\000' < log | grep …`) **and check the PASS count is non-zero as a
> control before believing the FAIL count.**
>
> ### ⇩ WHAT THIS SESSION DID, IN ORDER ⇩
>
> | | |
> |---|---|
> | **step 1** | measured the elevation discriminator — `IsAdmin()` is TRUE unelevated, `IsElevated()` is not, and `K$ADMINISTRATOR`'s process-start seed already answers it. **No new kernel key was needed** |
> | **step 2** | 56 clause 2 (`LOGIN:414` gate, `LOGIN:568` branch) and 57's promotion report, built and cycled |
> | **`b65`** | 12 of 13 — `verify-batchjob`'s elevated row failing, diagnosed as the verifier, not the product |
> | **the ruling** | `verify-batchjob` re-aimed at SDSYS |
> | **`b66`** | ***13 of 13 and 19 of 19, green in both halves. PRE_RELEASE 59 CLOSED*** |
> | **rename** | the docs directory is `SDCoreWindowsDocs`; eight live references updated, two of them warnings that had **inverted** |
> | **PRE_RELEASE 11** | ***the silent transaction data loss is FIXED and has a standing verifier*** |
> | **PRE_RELEASE 39** | the uninstaller's account prompt, **built; its `-Remove` path is UNRUN** |
>
> ### ⇩ THE TWO BLOCKERS LEFT — 39 AND 64 — AND WHAT EACH IS WAITING ON ⇩
>
> ***2 CLOSED ON `-Run b69` AND IS OFF THIS LIST; 64 TOOK ITS PLACE.*** The row
> below is kept for the trace, which is the reusable part. **64 is new and is
> the one that wants a ruling.**
>
> ***62 CLOSED ON `-Run b68` AND IS OFF THIS LIST*** — measured, not reasoned:
> `verify-sdsysgate` 10 of 10, refused by identity, both disqualifiers absent.
> **Its row below is kept for the design note, which is the reusable part.**
>
> ***56, 57, 58 AND 61 ALL CLOSED ON 29 Aug 2026 AND ARE OFF THIS LIST.*** 56's
> model is built, cycled and proved by `-Run b66`; 57 likewise, its "installed
> and unrun" having been a testing gap rather than outstanding work; 58's
> `Administrator` set is written; **61 was not a defect at all** — see below.
> **56's one remainder was re-filed as 62 rather than dropped.**
>
> | | waiting on |
> |---|---|
> | **2** | ***MEASURED AND LIVE: AN UNELEVATED ADMINISTRATOR HAS NO `sh`, NO `!` AND NO `OS.EXECUTE`. IT WANTS THE OWNER'S RULING, NOT A GUESS.*** The evidence is in **`b68`'s own transcript** — `[PASS] unlisted: refused with message 10053`, `expected don, got don`, `[PASS] unlisted: OS.EXECUTE from a program is refused`. **`verify-osusers` scores those green because it tests the GATE, not the POLICY.** `os.users` holds **0 records**. ***THE CAUSE IS A CHANGE MADE FOR A MODEL WITHDRAWN FOUR HOURS LATER***: `7aee48d` (10:16) removed the ADMINISTRATOR default *"because 56 elevates an administrator at login into SDSYS"*, and `af5490e` (14:58) reversed exactly that. **The 26/27 Aug instruction — *"os.execute, ssh and api by default without escalating"* — is unmet, and "without escalating" is the case that broke.** ***DO NOT JUST PUT THE TWO LINES BACK***: `os.users` is keyed on the person and survives a `LOGTO` (`op_sh.c:167`), which 56 forbids — whereas `CPROC:2781` already clears the session flag on any `LOGTO` away from SDSYS, so flag-carried access is account-scoped for free. ***AND THE NAIVE FLAG FIX IS A TRAP***: `LOGIN:568` gates the SDSYS branch on that same flag, so setting it at login would send an unelevated administrator back to SDSYS and undo the reversal. **A fix must land after that branch decides.** *(Was: a re-read before any work, because its stated premise is gone.* It was re-opened as downstream of 56 and says *"56 abolishes the administrator account this attached to"* — **clause 2's reversal gave that account back.** Left open rather than quietly closed: whether its `os.users` half still matters under the model that actually shipped **has not been measured**. It is a `B`, so it belongs in this table and was missed out of it once — **now measured, and the answer is above.**)* |
> | **39** | ***a real interactive uninstall on task 7.2's guest.*** Nothing has been deleted by it, the last-administrator refusal is unprovokable here, and the prompt cannot be reached from a cycle at all — see the box below. **Do not tick it until it has run** |
> | **62** | ***THE VERIFIER IS BUILT AND WIRED AND HAS NEVER RUN — `gplbld/verify-sdsysgate.ps1`, step in `VerifyInstall2`, and it closes on `b68`.*** ***sysmsg 10002 IS NOT A USABLE ANCHOR AND THAT IS THE WHOLE DESIGN***: `CPROC` prints it on **both** refusal paths (`:2637` identity, `:2651` failed elevation), and the account is reached over ssh, which has no desktop, so `elevate('START')` would fail there anyway — **a 10002 check would pass with the gate deleted.** The audit **reason** is the only discriminator, so the step is **elevated**: the trail is locked to SYSTEM and Administrators (measured — an unelevated read is *"Permission denied"*). Ten decisive checks, a null case, a reader control and two disqualifiers. **Verified only as far as unelevated allows** — parse 0 errors / 2 functions, BOM 0, CR 0, both guards run and return exit 2 against a control reading 0, `assert-current` **exit 0 live** with it on `$neverShipped`. *(Was: a verifier, not a code change — the hole is closed and nothing tests it.* Both routes now test the person before anything prompts: `LOGIN:568` needs an already-elevated session AND an administrator, and `CPROC:2634` refuses with 10002 **before** `elevate('START')`. **Traced by source only**: `10002`, `not an administrator` and `LOGTO REFUSED` get **zero hits across every `gplbld/verify-*.ps1`**. PRE_RELEASE 59's `sdtestuser` machinery already builds the account it needs — now built as above.)* |
>
> ***61 CLOSED AS NOT A DEFECT, AND THE PREMISE WAS INVERTED.*** `listf` shows
> `$MAP` as **`DH`**, not `Err 30`. The three files do three different jobs and
> the entry compared two of them as if they did one: **`voc_template` field 1 is
> a type code** and becomes SDSYS's VOC, **`newvoc` field 1 is a description
> whose FIRST CHARACTER is the type code** — `CREATEA:1233` replaces the field
> with `rec[1,1]` (two characters for a `P` type), so the description does not
> reach an account's VOC but **its first letter is load-bearing** — and
> **`listf`'s Description column is a lookup into `newvoc`** (`voc.dic`:
> `IF @ = '' THEN F1 ELSE @`). The control that settled it: neither description
> string appears anywhere in SDSYS's VOC file, while `listf` displayed both.
> ***THE UPSTREAM REPORT CARRIED THE SAME FALSE CLAIM AND WAS ONE STEP FROM
> BEING SENT*** — withdrawn in UPSTREAM_FIXES.md. **The one real wart it exposed
> is filed as 63, `M`**: ten of SDSYS's sixteen files print a bare `F` where a
> description belongs, because they have no `newvoc` record to look up.
> **58 no longer blocks 34 and 55, but they still collide — do them together.**
>
> ***NOTHING NEEDS A DECISION FROM THE OWNER TO PROCEED.*** 61's was the one
> exception and it is closed; **39's is not a decision but a rig**, and 2 and 62
> both want a measurement that nobody has to rule on first.
>
> # ⇩ 39 IS BUILT BUT ITS `-Remove` PATH IS UNRUN — IT WANTS THE VirtualBox RIG. ⇩
>
> ***THE UNINSTALLER NOW OFFERS TO TAKE THE WINDOWS ACCOUNTS SD CREATED***, as
> a second prompt after the database one, both defaulting to keep. New shipped
> script `gplbld/remove-sdaccounts.ps1`, and the closing disclosure names the
> accounts at last. **Install 29 Aug 18:5x, `assert-current` exit 0 live.**
>
> ***"THE INSTALLING PERSON" RESOLVES TO `{username}` AT UNINSTALL TIME*** — the
> entry told the next session to settle that first, so: the installer's identity
> is **not** persisted, deliberately. An uninstall may happen years later under a
> different administrator, and an exclusion naming a deleted account protects
> nobody. **The owner's purpose clause is the real requirement** and is
> implemented as a property that is checked: the sweep **refuses outright** if it
> would remove the last local administrator, and that **overrides a Yes**.
>
> ***READ THIS BEFORE TICKING 39: THE `-Remove` PATH HAS NEVER RUN.*** Only the
> read-only half is measured — the candidate set, the `-Keep` exclusion, all
> three refusals, the gate ordering (every refusal precedes every write), and the
> `cmd /c` log redirection. **Nothing has been deleted.**
>
> ***AND THE PROMPT CANNOT BE REACHED FROM A CYCLE AT ALL, FOR TWO REASONS.***
> `cycle.ps1` uninstalls `/VERYSILENT`, so `UninstallSilent` short-circuits
> before it; and `cycle.ps1:486` records the harder one — ***"an uninstaller fix
> cannot be verified in the cycle that ships it"***, because `unins000.exe` is
> generated at INSTALL time. This change reaches an uninstaller only at the
> **next** install. **So it wants task 7.2's guest, not this machine** — a real
> uninstall that deletes accounts should not be exercised where the accounts
> matter.
>
> # ⇩ PRE_RELEASE 11 IS FIXED — THE SILENT TRANSACTION DATA LOSS. CYCLED AND MEASURED. ⇩
>
> ***THE WORST THING ON THE LIST IS GONE.*** A nested `commit` used to abandon
> the outer transaction: its writes were lost with **no error, no warning and
> nothing in the log**, while the inner ones landed. `op_txncmt()` undid neither
> half of what `op_txnbgn()` did, and `BCOMP`'s `st.commit` jumps past the
> `OP.TXNEND` that would have called `rollback()`.
>
> ***THE FIX IS ONE FUNCTION WITH TWO CALLERS.*** `end_txn_level()` is lifted out
> of `rollback()` and called from `op_txncmt()` too — **the defect was that this
> bookkeeping lived in one place with one caller**, so a second copy would have
> been the same thing waiting to happen again. It is called **before**
> `exit_op_txncmt:`, so the three `k_error()` paths do not pop a level they did
> not commit.
>
> ***MEASURED ON THE 18:36:04 INSTALL, `sd.exe` `4732ECF659E8DB40`.***
> `gplbld/verify-txn.ps1` — **NEW** — reports **9 of 9**:
>
> | | before | after |
> |---|---|---|
> | the outer record's write | `base` — **lost** | **`outer`** |
> | `SYSTEM(1008)` delta over the pair | **+2** | **0** |
> | `SYSTEM(1007)` after the inner commit | **0** — no transaction | parent reinstated |
>
> ***IT IS WIRED INTO `VerifyInstall1` AND WAS MEASURED BEFORE BEING WIRED IN***,
> which is the rule `verify-lineendings` records. **The unelevated half is 14
> steps now, not 13** — expect **14 of 14**. It needs no elevation, no `-Run`
> token and raises no UAC prompt, and it **refuses an elevated shell**, because
> an elevated session lands in SDSYS where its probe is not.
>
> ***ONE ROW FAILED ON ITS FIRST RUN AND THE PRODUCT WAS RIGHT.*** `NEST.LEVEL`
> expected 1 and read 2: the baseline `l0` is taken **outside** the outer
> transaction, so inside the inner one the depth is two above it. **The
> instrument was wrong, not `txn.c`** — corrected in the row rather than by
> moving the baseline, since `NEST.DELTA` needs the same outside-the-pair
> baseline and one of them is one thing to get wrong instead of two.
>
> ***AND ONE THING IS FILED RATHER THAN FIXED — see 11's entry.*** On the three
> `k_error()` commit-failure paths, `process.txn_id` has already been zeroed, so
> `txn_abort()` and `op_txnrbk()` find nothing to roll back and the level stays
> counted. **Pre-existing, not widened by this**, and it needs a decision about
> the records already written rather than a decrement.
>
> ***A CYCLE WAS SPENT: install 29 Aug 18:36:04, `assert-current` exit 0 live.***
> `make sd` ran first (`cycle.ps1` does not build): `txn.o` recompiled, exit 0,
> no warnings. **The next suite run is `b67`.**
>
> # ⇩ GREEN IN BOTH HALVES. PRE_RELEASE 59 IS CLOSED. NOTHING IS OWED. ⇩
>
> ***`-Run b66`, 29 Aug 2026 17:54–18:12 — UNELEVATED 13 OF 13, ELEVATED 19 OF
> 19, 1,106 `[PASS]`, ZERO `[FAIL]`, ZERO TABLE ROWS SCORING FAIL.*** The first
> run to come back green in both halves.
>
> ***THE RE-AIMED ROW MEASURED, IT DID NOT MERELY PASS.*** `verify-batchjob`
> exit 0 with `ELEVATED in SDSYS, no entry: still runs` **True / True / PASS /
> decisive yes**, and **neither `SDSYS-ENTRY-PRESENT` nor `SDSYS-PLANT-FAILED`
> appears anywhere in the transcript** — which matters, because both of those
> also produce exit 0 while measuring nothing. **Check the row and the markers,
> not the exit code.**
>
> ***SDSYS IS CLEAN AFTERWARDS, CHECKED WITH A CONTROL.*** No `ZZBATCHS` in
> `sdsys\bp` or `bp.out`, `batch.jobs` empty, and `zzbatch` **0 hits** in the VOC
> buckets — against a control finding `listf` 6, `count` 18, `who` 15 in the same
> search. ***THE FIRST ATTEMPT AT THAT CHECK WAS WORTHLESS AND SAID SO***: a
> plain `grep` of the dynamic file's `%0`/`%1` buckets found the probe absent
> **and the control absent too**, so it was measuring nothing. `grep -a -F` is
> what reads them.
>
> ***PRE_RELEASE 59 IS CLOSED*** — all five verifiers pass. Two were converted to
> a real non-administrator account, **two needed no change at all** (`lcnames`
> back to 142 of 142, `osusers` 44/0 — both recovered the moment clause 2 was
> reversed), and `batchjob` was re-aimed. **Open count 22 → 21.**
>
> ***USE `b67`; b54–b66 ARE SPENT.*** There is nothing owed and nothing to
> re-run: spend it on a run that carries something new.
>
> *(The box below is the pre-`b66` text, kept for the reasoning that produced
> the re-aim.)*
>
> # ⇩ STEP 2 IS BUILT, CYCLED AND MEASURED. ONE FAILURE, AND IT IS A VERIFIER. ⇩
>
> ***`-Run b65`, 29 Aug 2026 16:35–16:54 — UNELEVATED 12 OF 13, ELEVATED 19 OF
> 19, 1,106 `[PASS]` AND ZERO `[FAIL]` IN EVERY LOG.*** The prediction below was
> two-thirds right and the miss is the informative part.
>
> | predicted to recover | result |
> |---|---|
> | `verify-lcnames` | ***142 of 142*** (was 107 of 128 on `b60`) |
> | `verify-osusers` | **44 / 0** |
> | `verify-batchjob` | ***STILL FAILS — exit 1, 9 of 10 rows*** |
>
> ***THE ONE FAILING ROW IS `ELEVATED with no entry: still runs`, expected True
> and observed False — AND ITS SUBJECT NO LONGER EXISTS.*** That is more than
> the *"check that leg"* warning already on file. `verify-batchjob.ps1:111`
> `Push-Location`s into the account directory and runs `sd` **elevated**,
> expecting to stand in the account with the batch gate bypassed. Under the
> ruled model **an elevated session cannot stand in an ordinary account at
> all**: an elevated login goes to SDSYS (`LOGIN:568`), and a `logto` out of
> SDSYS gives up the flag (`CPROC:2781`). So the state that row measures is
> unreachable, not merely mis-measured.
>
> ***THE PRODUCT RULE IT WAS PROTECTING IS INTACT.*** `LOGIN:901` still bypasses
> the batch gate on `K$ADMINISTRATOR`, so *"elevation passes on its own"* (the
> owner's 22 Aug decision) holds — **in SDSYS**, which is now the only place an
> elevated session can be.
>
> ***RULED 29 Aug 2026 — "re-aim the batchjob row at sdsys". BUILT AND UNRUN; IT
> NEEDS `b66`.*** The elevated child now asserts that `batch.jobs/SDSYS` is
> absent (**refusing out loud rather than deleting a record it did not write**),
> plants the same `COUNT VOC` paragraph in **SDSYS's own VOC** as `zzbatchsyspa`,
> runs it, and cleans up **unconditionally** with `DELETE VOC` plus the BP source
> and object. ***THE ACCOUNT PROBES COULD NOT BE REUSED*** — they are in the
> ACCOUNT's VOC and an elevated session never sees them, which is the whole
> reason the row had to move. **A broken precondition is recorded NON-DECISIVE,
> not as a FAIL**, so it cannot make a claim about the product that the run did
> not make. **This is PRE_RELEASE 59's last of four; no cycle is owed** —
> `verify-batchjob.ps1` is on `$neverShipped`, `assert-current` is exit 0 live,
> and the script parses with **0 errors and all 8 functions found**.
>
> ***USE `b66`. b54–b65 ARE SPENT.*** `b64` bought nothing — an interrupted
> parent stranded `sdtub64`, and `b65`'s sweep removed it exactly as read from
> `sdtestuser-admin.ps1:201-213` (`DELETE.ACCOUNT`, both halves gone, checked
> after). `sdtub65` went in the `finally`.
>
> ***COUNT `[FAIL]` WITH THE BRACKETS.*** A bare `FAIL` also matches
> `verify-fold`'s negative control — *"expected FAIL, observed FAIL, result
> PASS"* — which is a check working correctly, and scoring it as a failure is
> §"anchor on the SUCCESS wording" from the other side. It cost one wrong count
> here before the self-report line was read.
>
> ***FULL CYCLE 29 Aug 2026 15:33:45, `assert-current` EXIT 0 LIVE.*** 184
> programs compiled, **0 errors and 0 of the fatal "is not assigned a value"
> class**; `gpl.bp.out` 186 and `gcat` 127, both unchanged, so nothing was
> added or lost. Verified by reading the installed tree, not the run's output:
> `LOGIN` and `MODIFYA` objects recompiled 15:33:14, messages **10128** and
> **10129** installed at 424 and 308 bytes, and the mirrored file count moved
> 2982 → **2984**, which is exactly the two new messages.
>
> ***NOTHING IS IN FLIGHT AND NOTHING IS HALF-BUILT. THE ONE THING OWED IS A
> RUN.*** Step 2 is built, cycled, installed and measured; the `verify-batchjob`
> row is ruled and re-aimed at SDSYS, and it has never been executed.
>
> ***RUN AND GREEN ON `b66` — see the box at the top.*** The prediction held:
> unelevated 13 of 13, and the re-aimed row passed **decisive**, with neither
> `SDSYS-ENTRY-PRESENT` nor `SDSYS-PLANT-FAILED` firing. **The command form is
> kept here because it is the one to reuse, with a fresh token:**
>
> ```
> C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\VerifyInstall1.ps1 -ThenElevated -Run b67 -ContinueOnFailure
> ```
>
> **ORDINARY, UNELEVATED PowerShell — not elevated** (§4.0.1).
>
> ***AND DO NOT Ctrl-C IT — `b64` IS WHAT THAT COSTS.*** 29 Aug 15:45:56:
> `Create` succeeded in full and **the parent transcript then stopped dead**
> after *"EXPECT A UAC PROMPT NOW"* — no error, no `finally`, 881 bytes. The
> interrupt does not reach the removal, so `sdtub64` was left live and enabled
> and the two reruns correctly refused on it. **If a UAC prompt is missed, let
> the step fail**; the removal still runs on that path.
>
> ***TWO OLDER STRAYS ARE IN `sdusers` AND THE SWEEP WILL NOT TAKE THEM***, by
> design — `sdsshb55` (the `b55` run named in H.1) and `b48adm` do not match
> `sdtu*`. Not urgent; noted so the next reader does not rediscover them.
>
> ***AND THERE IS A PREDICTION TO CHECK IT AGAINST — READ THIS BEFORE SCORING
> THE RUN.*** PRE_RELEASE 59's five unelevated failures were all one cause:
> *"every one assumes an administrator lands in an ordinary account, which
> clause 2 abolishes."* **Clause 2 is now reversed, so that assumption is true
> again**, and `verify-lcnames`, `verify-osusers` and `verify-batchjob` — the
> three still unconverted — are expected to come back. `verify-nocase` and
> `verify-lineendings` were converted to a real non-administrator account and
> are unaffected either way, which is the better shape and stays. ***IF THE
> THREE DO NOT RECOVER, THAT IS THE FINDING***, and 59 needs re-reading rather
> than the verifiers patching.
>
> ***THE OTHER THING THE RUN DECIDES IS WHETHER `don` CAN STILL GET IN AT
> ALL.*** The `sdusers` gate lost its administrator exemption, so an
> administrator with no SD account is now refused with 5009 — deliberately, it
> is the owner's *"if any are built outside of sd they do not have access"*.
> `don` was in `sdusers` and had an account before the cycle, and `adopt` runs
> unconditionally in `sd.iss`, so this should be invisible. **It was not driven
> by hand from here on purpose**: an unelevated `sd` piped by an agent is
> CLAUDE.md's opening trap, and a hung `sd.exe` strands the user-table slot and
> makes the next `cycle.ps1` refuse.
>
> ***THE RECOVERY DOOR WAS CHECKED AND IS OPEN.*** `adopt-account.ps1` goes in
> through `sd -internal`, which is still exempt from the gate by design, so a
> failed adopt is a setback and not a lockout. `sd.iss`'s failure branch no
> longer names a specific refusal, because which one you get now depends on how
> far adopt got.
>
> ***STEP 1 — MEASURED 29 Aug 2026, AND THE ANSWER IS "NO NEW KERNEL KEY".***
> `gplbld/probe-osadmin.ps1`, run twice from the same account, one leg
> unelevated and one elevated:
>
> | | unelevated | elevated |
> |---|---|---|
> | `WindowsPrincipal.IsInRole` (Win32 control) | False | True |
> | `getgrouplist()` holds 544 → **`IsAdmin()`** | **TRUE** | **TRUE** |
> | `getgroups()` holds 544 → **`IsElevated()`** | **FALSE** | **TRUE** |
> | `K$OS.ADMINISTRATOR` (`op_kernel.c:456`) | TRUE | TRUE |
> | `K$ADMINISTRATOR` **as seeded** (`kernel.c:240`) | **FALSE** | **TRUE** |
>
> ***THE CAUTION WAS RIGHT — `IsAdmin()` IS TRUE UNELEVATED***, so
> `K$OS.ADMINISTRATOR` cannot carry 56 clause 2's `:513` branch on its own.
> **`IsElevated()` is the discriminator and SD already exposes it**: read
> `kernel(K$ADMINISTRATOR,-1)` **at `LOGIN`'s `begin case` (`:420`)** and it
> still holds the `kernel.c:240` seed, which is exactly *"is this session
> already elevated"*. Both instruments agreed in both legs.
>
> ***THE SEED SURVIVES TO `:420` — BY EXHAUSTIVE GREP, NOT BY ASSUMPTION.***
> Three live writers of the flag exist in the BASIC layer: `LOGIN:615` and
> `CPROC:2769`/`:2781`, and both `CPROC` sites are in the `LOGTO` path, which
> cannot run before `LOGIN`. `APISRVR:1204`/`:1206` are commented out.
>
> ***DO NOT WRITE THE OBVIOUS BASIC PROBE — IT REPORTS THE OPPOSITE.***
> `LOGIN:615` sets the flag for anybody who reached SDSYS, which today is every
> administrator elevated or not (`:513`), so a program run from an SD prompt
> reads 1 in **both** legs and would be written up as *"no discriminator
> exists"*. That is why the instrument asks `getgroups()`/`getgrouplist()`
> directly, through the MSYS2 runtime `sd.exe` is built against.
>
> **To re-run it — the two legs are the measurement, one alone says nothing:**
>
> ```
> C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\probe-osadmin.ps1
> ```
>
> **once in an ORDINARY, UNELEVATED PowerShell and once in an ELEVATED one.**
> It needs no install, no SD, no account and no `-Run` token, and it refuses out
> loud if the account it runs as is not an administrator — that null case prints
> `IsAdmin() = FALSE`, which is word for word the answer step 1 hoped to see.
>
> ***STEP 2 — BUILT AND CYCLED 29 Aug 2026. THREE CHANGES, ONE CYCLE.***
>
> 1. **`LOGIN:414`, the `sdusers` gate** — the administrator exemption is gone
>    and the gate is uniform across all three tiers. It reads
>    `if not(kernel(K$INTERNAL,-1)) then`; `-INTERNAL` stays exempt, which is
>    the bootstrap and the `adopt` recovery.
> 2. **`LOGIN:568`, the SDSYS case** — now
>    `case kernel(K$ADMINISTRATOR, -1) and kernel(K$OS.ADMINISTRATOR, 0)`.
>    ***THE FIRST IS THE PROCESS-START SEED AND IS THE WHOLE MECHANISM***; the
>    second is belt to its braces, closing the case where a token carries
>    Administrators for an account that is not a member. **Do not "simplify" it
>    back to one key** — `K$OS.ADMINISTRATOR` alone is TRUE for an unelevated
>    administrator, which is the case that must not come here. An unelevated
>    administrator falls through to `case 1` and lands in their own account.
> 3. **`MODIFYA`, 57's promotion report** — `promo.snapshot` before the register
>    write and `promo.report` after it, so *"what did this command void"* is a
>    genuine before-and-after reading of `tier_allows` rather than rank
>    arithmetic copied out of `TIERGATE`. A demotion strands nobody and prints
>    nothing; an unreadable group says so rather than reporting a comfortable
>    zero. Messages **10128** and **10129**.
>
> ***DO NOT DO: the 20-file `adopt-account` removal.*** It is CANCELLED — see
> below. And **do not build "two tiers"**; that ruling was withdrawn.
>
> ***THE SUITE IS AT `b64`*** (`b54`–`b63` spent). Two of PRE_RELEASE 59's four
> verifiers are converted and green; `verify-lcnames` and `verify-batchjob`
> are **not mechanical** — read 59 before starting either.
>
> # ⇩ 56 CLAUSE 2 IS REVERSED: THE ADMINISTRATOR'S PERSONAL ACCOUNT COMES BACK ⇩
>
> ***OWNER'S RULING, 29 Aug 2026 — AND IT CANCELS QUEUED WORK. READ THIS
> BEFORE TOUCHING `LOGIN` OR `sd.iss`.*** *"that is precisely why
> administrators also had a personal account. They got SDSYS in one of two
> ways, by starting SD in an elevated session or by logging to SD after logging
> into their personal account."* And the property applies to every tier: *"if
> any are built outside of sd they do not have access to sd until a matching
> standard or programmer account is created in SD."*
>
> ***IT ALREADY HOLDS FOR STANDARD AND PROGRAMMER, AND THE CODE SAYS WHY IT
> DOES NOT FOR ADMINISTRATORS.*** `LOGIN:399`'s `is_grp_member(lgn.id,
> 'sdusers')` refuses an outside-SD account with **5009**. The exemption at
> `:398` was added by 56 itself and its comment states the causation: *"the
> model gives an administrator no account of their own — so nothing ever puts
> them in sdusers"*. **Restore the account and the exemption's reason is gone.**
>
> ***1. THE `adopt-account` REMOVAL IS CANCELLED — DO NOT DO THE 20 FILES.***
> It was ruled unnecessary on the very clause now reversed. Adopt is how the
> installing administrator gets their personal account. ***NOTHING HAD BEEN
> REMOVED***, because that entry was deliberately kept separate — that caution
> is what saved it. The withdrawn ruling is struck in 56 rather than deleted.
>
> ***2. `LOGIN:398`'s ADMINISTRATOR EXEMPTION GOES***, and the `sdusers` gate
> becomes uniform across all three tiers.
>
> ***3. `LOGIN:513` MUST STOP SENDING EVERY `K$OS.ADMINISTRATOR` TO SDSYS.*** An
> **unelevated** administrator lands in their **personal account**; SDSYS is
> reached by an already-elevated session, or by `logto sdsys` from that
> account. Two explicit routes, not one automatic one.
>
> ***4. AND THE MECHANISM FOR "IS THIS SESSION ALREADY ELEVATED" DOES NOT
> EXIST YET — MEASURE BEFORE DESIGNING.*** `K_ADMINISTRATOR` is a **settable
> `USR_ADMIN` flag** (`op_kernel.c:395` — it takes an argument and can be set
> or cleared), and `K_OS_ADMINISTRATOR` is `IsAdmin() && connection_type !=
> CN_SOCKET` (`op_kernel.c:456`), i.e. *"is the PERSON an administrator"*.
> **What `IsAdmin()` answers for an UNELEVATED administrator is the crux and is
> not established** — this file already records it answering TRUE for every API
> session until the `CN_SOCKET` guard was added, so do not trust it unmeasured.
>
> **The `ADMINISTRATOR` tier stays — three tiers, as below.**
>
> # ⇩ THREE TIERS. THE "TWO TIERS" RULING WAS REVERSED THE SAME HOUR. ⇩
>
> ***DO NOT BUILD "TWO TIERS". IT IS WITHDRAWN.*** Owner, 29 Aug 2026, after
> being shown that `CREATE.ACCOUNT … ADMINISTRATOR` makes a Windows
> administrator: *"we need three tiers because we create accounts in SD not in
> windows except for the installer, and that is correct … That is the better
> approach and one I had forgotten about."* ***SD CREATING THE WINDOWS ACCOUNT
> IS THE DIRECTION THE DESIGN WANTS*** — SD is the authority for who
> administers SD, and the tier is the mechanism. **Nothing was built, so
> nothing had to be undone.**
>
> ***THE TRACE IS KEPT BECAUSE IT IS THE RECORD OF WHAT THE TIER DOES:***
> `CREATEA:813` → `make.admin` → `os_group("ADDMEM", "S-1-5-32-544", …)`, the
> built-in Administrators group; the tier's extra verbs each gate themselves on
> the **person** (`CREATEA:251`, `DELACC:85`, `MODIFYA:167`, `GRANTA:95`,
> `UNLOCK:61`); the tier is **15 literals in 4 files** while the 52
> `K$ADMINISTRATOR` / 5 `K$OS.ADMINISTRATOR` uses are the **kernel key** and a
> different thing; and `accounts\don` carries `ADMINISTRATOR` in field 5 today.
>
> ***ONE PROPERTY IS LEFT TO SETTLE AND THE CODE DOES NOT DO IT — OWNER'S
> CALL.*** He said *"an Administrator account created outside of SD does not
> have access to SD until a matching SD administrator account is created."*
> **Measured, that is not today's behaviour:** `LOGIN:513` sends any
> `K$OS.ADMINISTRATOR` straight to `initial.account = 'SDSYS'` and reads
> **SDSYS's** register record, never one belonging to the person; `LOGIN:398`
> skips the `sdusers` gate for them outright. So any Windows administrator at
> **the console** is in on a UAC consent, with no SD-side account. Over ssh
> they are refused in practice — `elevate('START')` has no desktop (10002).
> ***AND BE HONEST ABOUT THE CEILING***: a Windows administrator can add
> themselves to any group, read the data tree, or run as SYSTEM, so such a
> check is **an explicit act and an audit trail, not a boundary that holds
> against them.** Worth having, perhaps — but chosen knowing that.
>
> ***57 STANDS AND IS NARROWER THAN IT READS***: *"Proceed, and print what it
> voided."* `LOGIN` is not a `tier_allows` caller, so the account's own owner
> is never stranded and a single-member account cannot strand anything.
>
> # ⇩ BOTH OWNER RULINGS OF 29 Aug ARE BUILT AND UNRUN. ⇩
>
> ***HE WAS ASKED TWO QUESTIONS AND ANSWERED BOTH: "1. sweep  2. delete dead
> voc".*** Both are implemented.
>
> ***1. THE SWEEP.*** `sdtestuser-admin.ps1 -Sweep` removes stray `sdtu*`
> accounts from interrupted runs, **inside the elevated child Create already
> raises — no extra UAC prompt.** ***THE CANDIDATE LIST IS BUILT IN THE ELEVATED
> PROCESS AND IS NOT PASSED IN***: this is code that deletes Windows accounts,
> so the parent controls *whether* to sweep, never *what*. Three conditions, all
> required and each printed — name matches `^sdtu[a-z0-9]+$`, is **not** the
> account being created, and **is in `sdusers`**. `DELETE.ACCOUNT`, so record,
> group and Windows user go together; the check is the artefact before and
> after.
>
> ***2. THE DEAD VOC RECORDS — DONE AND VERIFIED. `after: 0`.*** All four
> deleted with `DELETE VOC` (`1 record(s) deleted` each), and an independent
> `LISTF` afterwards found **no `SD*BP.OUT` records at all**. **PRE_RELEASE 60
> is closed.**
>
> ***AND CLEANING THEM UP EXPOSED A PRODUCT DEFECT — NEW, PRE_RELEASE 61, `B`.***
> Once the four dead records went, **`$MAP` was the only `Err 30` left**, on an
> otherwise clean install. `sdsys/newvoc/$MAP` has **no type code**: field 1
> reads `File for MAP output` where every other file record has **`F`** —
> including ***our own `voc_template/$MAP`***, which is the same record shipped
> twice with one copy right. `$map` and `$map.dic` both exist on disk, so it is
> the record and not the file. ***UPSTREAM HAS THE IDENTICAL SPLIT*** —
> `sdb64/NEWVOC/$MAP` broken, `sdb64/VOC_TEMPLATE/$MAP` correct — so it is filed
> in UPSTREAM_FIXES.md as well. ***DO NOT JUST PASTE THE `F` IN***: settle first
> which of the two feeds SDSYS's VOC (`verify-lcnames.ps1:772` says
> `voc_template` does, which the live reading appears to contradict) and whether
> a user account's `$MAP` is sound. **A `map` verb ships, so the file is
> reachable.**
>
> *(The verb was wrong first time and the script said so:)* Run elevated 29 Aug 2026, `DELETE.FILE` answered *"Error deleting DATA
> portion"* + *"DICT part of file does not exist"* on all four and changed
> nothing — **and `clean-deadvoc` reported FAILED**, because its verdict is a
> second `LISTF` rather than SD's wording. ***THE RIGHT VERB IS `DELETE VOC
> <name>`***: `DELETEF` wants to remove a FILE, and the file these records name
> is already gone — which is the definition of the thing being cleaned up. What
> has to go is the **VOC record**. Read from `gpl.bp/DELETE`: with ids named
> explicitly it takes the `num.ids > 0` branch and **neither prompt is
> reachable** (both are in the select-list and `ALL` branches), so `NO.QUERY` is
> not needed. ***AND SD's SUCCESS WORDING IS NOT USABLE AS AN ANCHOR HERE*** —
> sysmsg 3221 `"%1 record(s) deleted"` prints unconditionally, so
> `0 record(s) deleted` appears on the failure path too. Both `clean-deadvoc.ps1`
> and `verify-catgate.ps1` now use `DELETE VOC`, and catgate's is
> **unconditional**: keying it on the directory existing is what let these
> accumulate, since the record outliving the directory *is* the defect.
> **The four are still there — rerun the command below.**
>
> **ELEVATED PowerShell, and `-WhatIf` first if you want to see the list:**
>
> ```
> C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\clean-deadvoc.ps1 -WhatIf
> ```
>
> ```
> C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\clean-deadvoc.ps1
> ```
>
> It is on `$neverShipped` and `assert-current` is **exit 0 live** with it
> listed. Its unelevated refusal was exercised (exit 2).
>
> # ⇩ TWO OF FOUR CONVERTED AND GREEN. UNELEVATED 10 OF 13. ⇩
>
> ***`b63`, 29 Aug 2026 13:03:55 — `verify-lineendings` PASSED 17 OF 17, AND
> `verify-nocase` HELD.*** Elevated **19 of 19**. The two readings that matter
> in lineendings both passed as `sdtub63` over ssh: **the straddle**
> (`line 1 length 2047` — a CRLF exactly on the 2048-byte buffer boundary, the
> case its header says the file exists for) and **the lone-CR control**
> (length 11, one field — a CR survived as data). The account removed cleanly
> and the run left **no `sdtu*` user, record, group or `%TEMP%` residue**.
>
> ***`b63` IS SPENT. USE `b64`.***
>
> ***AND THE CLASSIFICATION IN 59 WAS WRONG — READ THIS BEFORE PICKING UP THE
> REST.*** It said *"four are close to mechanical"*. **Only two were.** The
> remaining three each need a TOKEN SPLIT, not a driver swap:
> **`verify-lcnames`** has 53 `Invoke-SD` calls of which **four are `LOGTO
> SDSYS`**, and those four work today *because* the administrator lands in
> SDSYS — the same fact that breaks the other 49; every call site has to be
> classified, and a mistake either way is a check that passes while measuring
> the wrong session. **`verify-batchjob`** re-invokes itself elevated and its
> child `Push-Location`s into the account to get a session there, which under 56
> it does not get — **check that leg before converting it.**
>
> ***AND ONE INTERRUPTED RUN COST A TOKEN — b62.*** A console **Ctrl-C does NOT
> run the `finally`**, measured: no removal was attempted and `sdtub62` was left
> live. (A `Stop-Job` pipeline stop *does*, which is why the comment claiming it
> was believed.) `VerifyInstall1` now **names any orphan and its remove command
> before it creates anything**; it reports and does not act.
>
> # ⇩ `verify-nocase` IS GREEN. THE PATTERN IS PROVEN. ⇩
>
> ***`b61`, 29 Aug 2026 12:21:40 — `verify-nocase` PASSED 3 OF 3, INCLUDING THE
> `DHFILE=0` CONTROL ITS OWN HEADER CALLS THE POINT OF THE TEST.*** ssh exit 0,
> `DIRFILE=1`, `DHFILE=0`, `ISWIN=1`. ***THE FIRST MEASUREMENT THIS PROJECT HAS
> TAKEN AS A REAL NON-ADMINISTRATOR.*** **Unelevated 9 of 13** (was 8),
> **elevated 19 of 19**, doors 5 of 5.
>
> ***SO `verify-lineendings.ps1` IS CONVERTED TOO AND IS UNRUN.*** The caution
> that said "one first" has been paid off. The refusal tests are a **table**
> now, cross-checked against `VerifyInstall1`'s own `$needsTestUser` read out of
> its source — a verifier converted but unlisted is untested, one listed but
> unwired is skipped, and both are silent. **Units 51 / 0.**
>
> ***`b61` IS SPENT. USE `b62`.***
>
> ***AND ONE THING FILED FROM THE LOG — PRE_RELEASE 60.*** SDSYS's `LISTF` now
> shows `SDCATGB59BP.OUT` **and** `SDCATGB60BP.OUT`, both `Err 30`: one dead VOC
> record per suite run since b59. `verify-catgate.ps1:161` deletes `<ACCT>BP`
> through SD and then removes `<ACCT>BP.OUT` with `Remove-Item` — **the exact
> thing the comment directly above it forbids.**
>
> ***0. `b60` RAN IN FULL. ELEVATED 19 OF 19. THE ACCOUNT MACHINERY WORKS END
> TO END. THE TIER WAS WRONG AND IS FIXED.*** 29 Aug 2026, 11:53:01.
>
> ***THE FOUNDATION IS WITNESSED FOR THE FIRST TIME.*** Create: `before=False
> after=True` on **both** the ACCOUNTS record and the Windows user; the ACE for
> `GITORLI\don` landed; and the **unelevated parent's own write succeeded** —
> `writable by this unelevated process: C:\ProgramData\SD\user_accounts\sdtub60`,
> which is the only token that could answer. Remove: `before=True after=False`
> on both. **`verify-doors-suite` 5 of 5 green in the same run**, so two account
> mechanisms coexisted.
>
> ***WHAT STOPPED `verify-nocase` WAS THE TIER, AND IT SAID SO IN SD's OWN
> WORDS.*** ssh **exit 0**, the session was in `sdtub60`, and then:
> *"BASIC is not in your VOC"*, *"RUN is not in your VOC"*.
> **`sdsys/newvoc/TIER.OMIT.STANDARD` lists `basic` and `run`** among the 42
> verbs a standard account does not get — read from the record, not inferred.
> ***ALL FOUR VERIFIERS COMPILE A PROBE, SO STANDARD CANNOT HOST ANY OF THEM.***
> The account is **PROGRAMMER** now, which is still a real non-administrator —
> ADMINISTRATOR is the tier that lands in SDSYS, and `verify-doors` uses
> PROGRAMMER for this same reason. **The unit test row that said *"does NOT
> grant ADMINISTRATOR or PROGRAMMER"* was itself the bug** — it encoded the
> wrong choice as a rule and would have defended it against correction. Split in
> two, and the tier is now checked against `TIER.OMIT.STANDARD` itself.
>
> ***TWO LEAKS FOUND AND FIXED, BOTH PRE_RELEASE 47's SHAPE.*** The unit test's
> denied fixture survived — `icacls /remove:d` did **not** remove the ACE and
> its output had been sent to `*> $null`, so six undeletable directories were in
> `%TEMP%` before anyone looked. `/reset` does remove it, the exit code is read,
> and the removal is a **checked row** rather than a warning nobody reads.
> `Invoke-SdAsTestUser` never removed its work directory either — `native.in`
> and 609 bytes of `native.out` per verifier per run. **Units 45 / 0**, and a
> run now leaves `%TEMP%` clean.
>
> ***AND THE RUN POLLUTED SDSYS, WHICH IS THE COST OF THE THREE UNCONVERTED
> VERIFIERS.*** `C:\ProgramData\SD\sdsys\BP.OUT` was created **12:07:16**, by
> `verify-lcnames` compiling its probe while landed in SDSYS. Harmless and the
> next cycle clears it — but **two of `lcnames`' 21 failures are about that
> object directory's case**, and those readings are not to be trusted until it
> runs in an account: its premise was broken. `lcnames` scored **107 of 128**.
>
> ***1. FINISH THE CONVERSION — `verify-nocase` HAS STILL NEVER COMPLETED.***
> Session 80 did the runner wiring and `verify-nocase.ps1` ONLY, which is the
> recommendation that stood here, followed. `VerifyInstall1` creates `sdtu<Run>`
> before its step list and removes it in a **`finally`** (the loop `break`s on a
> failing step, which is how `sddrb50a` came to be live on this machine now).
> **`test-sdtestuser-units.ps1` is 34 / 0** and still needs no install, no
> elevation, no account and no ssh — run it first, it costs nothing.
>
> ***NO CYCLE IS NEEDED AND `assert-current` IS EXIT 0 LIVE.*** Everything
> touched is `gplbld` and already on `$neverShipped`. **USE `b60`.**
>
> ***TWO DEFECTS FELL OUT OF THE WIRING AND BOTH WOULD HAVE COST A RUN.***
> (a) ***`assert-current` WAS ALREADY EXITING 1***, naming the three files
> session 79 wrote and never listed on `$neverShipped` — so **the suite could
> not have run at all**, and every verifier that calls it would have refused.
> Listed now; **exit 0 live afterwards.** (b) ***AN ACCOUNT DIRECTORY IS NOT
> REACHABLE BY THE UNELEVATED PARENT***: it grants Modify to SYSTEM,
> Administrators and its own `sdu_` group only, and `ls`/`touch` on `SDACCTB59`
> both answered *"Permission denied"* — while all four verifiers plant probes
> through the **file system**. `-Action Create` now adds one inheritable ACE for
> the invoking user. **A group would not have worked** — membership is fixed at
> logon, PRE_RELEASE 44 exactly.
>
> **Left after the run:** `verify-lcnames`, `verify-lineendings`,
> `verify-batchjob`, then `verify-osusers.ps1` **separately** — 931 lines, 32
> references to `@logname`/`don`, its own elevation dance. **Do not bundle it.**
>
> ***DO NOT TAKE THE SHORTCUT.*** Adding `LOGTO DON` to each verifier passes
> today and breaks the moment `adopt-account` goes — which is ruled and
> pending. It is written into the module's header so nobody re-derives it.
>
> ***AND EXPECT TWO MORE UAC PROMPTS*** — one for Create, one for Remove.
> `verify-doors-suite.ps1` serves three legs from one consent through
> `sd-elevate.ps1`'s helper and would remove both; deliberately not done in the
> same commit as an unproven mechanism.
>
> **THE TWO COMMANDS, IN ORDER. Both in an ORDINARY, UNELEVATED PowerShell —
> §4.0.1: `verify-credacl` and `verify-osusers` are only valid from an ordinary
> token, and `VerifyInstall1` refuses an elevated one outright.**
>
> ```
> C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\test-sdtestuser-units.ps1
> ```
>
> ```
> C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\VerifyInstall1.ps1 -ThenElevated -Run b64 -ContinueOnFailure
> ```
>
> ***`b64`. `b54`–`b63` ARE ALL SPENT*** — every profile directory under
> `C:\Users` from those runs is still there until a restart (PRE_RELEASE 35/36;
> `CREATE.ACCOUNT` refuses rather than hand back a suffixed home).
>
> ***THERE IS NOTHING TO RE-RUN FOR ITS OWN SAKE.*** `b63` is the settled
> reading: **unelevated 10 of 13, elevated 19 of 19**, and the three failures
> are the three unconverted verifiers. Spend the next token on a run that
> carries a conversion, not on repeating this one.
>
> ***DO NOT Ctrl-C IT.*** Measured on `b62`: the interrupt does not reach the
> account removal, so it strands a live enabled account and burns the token. If
> a UAC prompt is missed, **let the step fail** — the removal still runs on that
> path. If one is stranded anyway, the next run names it and gives the command.
>
> ***2. 56's `adopt` REMOVAL*** — ruled unnecessary 29 Aug (*"the installer has
> to be a windows administrator … they can login to sd and is logged into the
> sdsys account"*), **20 files** including `sd.iss`'s `AdoptCode` /
> `PasswordStepWanted` wizard flow, `CREATEA`, `DELACC`, `stage.py` and six
> verifiers. **Deliberately not bundled with the login change** so a broken
> install has one candidate cause. **Harmless meanwhile** — the account is
> simply never entered.
>
> ***3. 57's PROMOTION CASE*** — `modify.account b programmer` silently strands
> every lower-tier grant into `sdu_b`. The gate holds; nothing reports it. Two
> options in 57's "Left to settle", **the owner's call**.
>
> **58 is the documentation and waits for all three.**
>
> ***AND ONE INSTRUMENT TRAP THAT NEARLY PRODUCED A FALSE READING THIS
> SESSION:*** the `SD-verify` logs carry **both encodings at once** — the
> numbered per-step logs are **UTF-16LE**, the verifiers' own transcripts are
> **UTF-8**. A plain `grep` on the first kind reports **0 PASS / 0 FAIL** on a
> full 25KB log, which is indistinguishable from a step that did nothing. **Use
> `Get-Content`, or check the BOM first.**
>
> *(The box below is the pre-cycle text, kept for its commands and its
> reasoning. The cycle it opens with has been run.)*
>
> ***SESSIONS 76 TO 79 TOUCHED NEITHER `gplsrc` NOR `sdsys`, SO THE CYCLE IS
> STILL THE FIRST STEP AND THIS BOX IS STILL CURRENT.*** **19 open**, from the
> checker.
>
> ***BUT THE BIGGEST THING IN THE FILE IS NOW PRE_RELEASE 56, AND IT IS NOT
> STARTED.*** The owner rewrote the administrator access model on 29 Aug 2026
> — elevated **at login** into **SDSYS**, **no account of their own**, and
> **the rights of whatever account they logto**. **It supersedes 15 Aug's
> *"nobody logs in to an account but their own"*, withdraws the 29 Aug ruling
> on 31, and re-opens PRE_RELEASE 2** — a closed **B**. ***READ 56 BEFORE
> TOUCHING `LOGIN`, `CPROC` OR `CREATEA`***, and note it costs administrators
> ssh. Three of its seven clauses are already the code.
>
> **Of the six decisions taken on 29 Aug, two are done** — the 21 headings
> (session 78) and 31's trace (session 79, which produced 56). **54 and 55 are
> still available to pick up cold**, and neither is affected by 56.
>
> ### ⇩ WHAT TO DO FIRST ⇩
>
> **A CYCLE IS OWED — `assert-current` EXITS 1 UNTIL IT RUNS.** ***AND WHAT IT
> NOW CARRIES IS PRE_RELEASE 56, NOT THE OLD COMMENT RENUMBER.*** Session 79
> changed `gplsrc/keys.h`, `gplsrc/op_kernel.c`, `gpl.bp/LOGIN`, `gpl.bp/CPROC`,
> `gpl.bp/ELEVATE` and `gpl.bp/INT$KEYS.H`. **The C is already built** — `make
> sd` ran at 09:36, exit 0, 0 warnings, and `cycle.ps1` does NOT build, so do
> not skip that step if anything else moves. **The BASIC has never been
> compiled.**
>
> ***ONE PIECE OF 56 IS DELIBERATELY UNWRITTEN — `CREATEA`'s `grant.os.access`,
> which needs the `adopt` ruling in 56's "Left to settle".*** If that ruling
> lands first, make the change and spend ONE cycle on the lot; a cycle run now
> is void the moment it is made (§"A CYCLE ENDS AT THE NEXT SOURCE CHANGE").
>
> **ELEVATED PowerShell:**
>
> ```
> C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\cycle.ps1
> ```
>
> **THEN THE SUITE, `b59`** — ordinary UNELEVATED PowerShell, the owner's own
> terminal, not an agent's (§4.0.1). Expect the settled shape: 13 of 13
> unelevated, 18 of 19 elevated, the one failure `verify-apiadmin` **21/23**.
>
> ```
> C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\VerifyInstall1.ps1 -ThenElevated -Run b59 -ContinueOnFailure
> ```
>
> ***NOTHING IS WAITING ON THE OWNER. THE VERIFIER QUESTIONS CAME BACK TO US,
> 29 Aug 2026*** — *"your call on the verification utilities i have no
> opinion"*. All three are decided below; **the third is DONE and 54 and 55 are
> not started**.
>
> | | decided |
> |---|---|
> | wire `verify-profiledir.ps1` into a runner | **yes — `VerifyInstall2`.** Now ***PRE_RELEASE 54*** |
> | the typed-vs-computed figure guard | **yes, and it is smaller than it looked.** Now ***PRE_RELEASE 55*** |
> | the 21 struck-but-silent section headings | ***DONE 29 Aug 2026*** — all 21 carry `DONE <date>`; the checker's NOTE is gone and the tripwire is measured, below |
>
> ***THE 21 HEADINGS WERE WORTH DOING BECAUSE THEY TURNED A NOTE INTO A
> TRIPWIRE — DO NOT REDO THIS, IT IS DONE.*** `test-fixlist-units.ps1`'s rule 4
> is **one-directional by design**: it fails a section that says DONE over an
> **open** row, and it cannot fail the other way because most sections say
> nothing at all. **With DONE in all 21 headings, re-opening an entry is a hard
> FAIL** — the row un-strikes, the heading still says DONE, rule 4 fires. ***THE GUARD EXISTS NOW, AND IT WAS MEASURED IN
> BOTH DIRECTIONS ON THE SAME RE-OPENING*** — row 41 un-struck against the new
> heading FAILS, *"section 41 does not contradict row 41"*, **183 passed / 1
> failed, exit 1**; the identical un-strike against the old silent heading scored
> **184 passed / 0 failed, exit 0**. Both were run and both were restored.
> Entries do get reversed: 32 was partly reversed by 36, and 4 / 52 / 53 were all
> re-validated after being written.
>
> **The obvious objection is answered**: yes, this duplicates status, and *status
> living in more than one place* is the root cause the checker was written for.
> **Duplication is only dangerous when nothing compares the copies** — here the
> checker compares them every run, which is exactly what was missing on 28 Aug.
>
> ***DONE BY HAND, 21 `Edit` CALLS, NO SCRIPT.*** CLAUDE.md's rule about file
> edits applies with full force to a 21-site change in a tracked document, and
> this file has three silent corruptions in its record already. **The bytes were
> checked afterwards rather than assumed**: `git diff --stat` 21 insertions / 21
> deletions, every added line a `## ` heading, no BOM, CR count 0 unchanged, em
> dashes 568 → 589 — **+21, one per new separator, which is the count that would
> move if anything else had been rewritten.**
>
> ***THE THREE OWNER'S-CALL ENTRIES ARE RULED, 29 Aug 2026 — 31, 34 AND 39.***
> Recorded in PRE_RELEASE_FIXES.md, **and no work was started on any of them at
> the owner's instruction.** A ruling closes a question, not an entry, so those
> three did not move the count.
>
> | | ruling | what it now costs |
> |---|---|---|
> | **31** | ***WITHDRAWN THE SAME DAY AND REPLACED BY PRE_RELEASE 56.*** It read *"being an ADMINISTRATOR is the gate"*; shown what that cost, the owner reversed it — *"if they logto another account, they have the rights of that account"* | **back to the verifier-only fix the row first claimed.** Clause 5 is what `CPROC:2735` already does, so the product is right. **Sev back B → S**, and **the assertion at `verify-apiadmin.ps1:610` must not move until 56 lands** |
> | **34** | ***a set may declare itself link-free***; `checklinks.py` grows the declaration and `release.ps1` accepts it | the zero-link refusal stays the default for `User`, `Administrator` and `Testing`. **Not to be settled by adding a link** |
> | **39** | ***a second, separate prompt on uninstall***, and it must **never** take the installing person's own account | `sd.iss:3482` is unchanged; a second question follows it, defaulting to keep. **Sev resolved B? → B.** The exclusion is the hard part — `sd.iss:86` says `{username}` is whoever authenticated UAC, not necessarily who is signed in |
>
> ***AND ONE PREMISE WAS CORRECTED WHILE TAKING 39.*** The owner ruled by analogy
> to an upgrade *"giving the option of retaining accounts and the configuration
> file"*. **There is no upgrade-time prompt** — an upgrade replaces the shipped
> half in place and asks nothing. The prompt is on **uninstall** (`sd.iss:3482`)
> and covers the SD-side records only. He was told, and the ruling stands on the
> corrected premise.
>
> ***AND THE DOCS REPO IS AT `/c/Users/dmont/Projects/SDCoreWindowsDocs`.*** It
> is a sibling of this one and it is a separate git repository.
>
> ***RENAMED BY THE OWNER, 29 Aug 2026, TO MATCH ITS GitHub REPOSITORY — AND
> THIS ENTRY'S WARNING HAS INVERTED, WHICH IS WHY IT IS REWRITTEN RATHER THAN
> PATCHED.*** It used to read *"with spaces in the name … a probe for
> `SDCoreWindowsDocs` finds nothing, which is why two entries sat as 'cannot
> validate here' for a whole session."* **That is now exactly backwards**: the
> directory IS `SDCoreWindowsDocs`, there are no spaces, and a probe for the
> repository name is the thing that works. A stale warning that has flipped is
> worse than no warning, because it sends the reader away from the answer.
>
> ***PRE_RELEASE 4 AND 52 ARE DONE, 28 Aug 2026 — all twelve edits of 52's recipe
> applied in one commit***, `Testing/markdown/05,06,07`, diff 13 insertions / 14
> deletions. **Every figure was re-derived from the tree before it was written**:
> `newvoc` 395 entries / 119 field-1-`V` / `TIER.ADD.ADMINISTRATOR` 21 lines /
> `TIER.OMIT.STANDARD` 43, giving 81 and 416. HTML and PDF re-rendered for the
> three pages and the HTML checked for the corrected figures — `encrypt.field` is
> gone from the whole Testing set.
>
> ***THE INTERPRETER LINE IN §H.2 IS MISLEADING AND COST A WRONG CONCLUSION THIS
> SESSION.*** It records the MSYS2 python as the decision, so a probe of
> `/c/msys64/usr/bin/python` found no `markdown` and this session reported
> rendering as impossible. **The owner corrected it: every PDF on this box was
> made here.** `markdown` **3.10.2** is installed for the **Windows** python
> **3.13.14** (`WindowsApps\PythonSoftwareFoundation.Python.3.13`), which is what
> `mkdoc.py` and `mkpdf.ps1` run on. The MSYS2 gap is real and still unfixed —
> **it is a `setup-devbox.ps1` question, not a "cannot render" one.**
>
> ***PRE_RELEASE 53 IS DONE TOO — OWNER'S RULING, 28 Aug 2026: "move to not in SD
> core".*** The `encrypt.field` section is deleted from `Administrator/01` and the
> fact now lives as `## Field-level encryption` on
> `Testing/markdown/14-not-in-sd-core.md`, naming `sdencrypt()`/`sddecrypt()` as
> the supported route (verified in `gplsrc/sd_encrypt_sodium.c`) and saying
> plainly that nothing replaces the verb.
>
> ***AND IT WAS NOT COSMETIC: BOTH DOC GENERATORS HAD BEEN REFUSING TO RUN, AND
> NOTHING IN THE RECORD KNEW.*** `mktclsyntax.py` exited 1 with `NOT A VERB
> encrypt.field has a shape and is not on the roster`, `tclmap.py` with the same
> verb `claimed by Administrator/01` — so **the TCL syntax card could not be
> regenerated at all.** The roster is computed and had already self-corrected to
> **143**; `tools/tcl-syntax-shapes.txt` and `tclmap.py`'s map are typed and had
> not. **That gap is the whole reason a computed roster is worth having**, and it
> sat undetected because nobody had re-run the generators since PRE_RELEASE 25
> took the verb.
>
> ***BOTH NOW EXIT 0, AND THEY CONFIRM 4 AND 52 INDEPENDENTLY*** — `roster 143
> verbs (standard 81, programmer 42, administrator 20)` and `tclmap 143 of 143, 0
> exempt`, from tools that COMPUTE the figures rather than quote them.
> `checklinks` 0 broken across all three sets (77 / 6 / 185). **`README.md`'s
> three roster citations moved 144 → 143**, and **§H.2 below was corrected to 143
> in the same commit** rather than merely flagged; the "127 of 144" line is a
> record of a past miscount and was left.
>
> ***NOTHING CROSS-CHECKS A TYPED FIGURE AGAINST A COMPUTED ONE, AND THAT IS THE
> GAP BEHIND ALL OF 4, 52 AND 53.*** `mktclsyntax.py` had printed **standard 81**
> in the generated card for a week while the tester set said **77** — the two
> halves of the documentation disagreed and nothing compared them, because the
> generators read the VOC and the hand-written pages do not. **Not filed as an
> entry**: it is a design question about the toolchain, not a defect in a page,
> and it is the owner's call whether a checker should assert prose figures against
> `mktclsyntax`'s roster line. It is the cheapest guard left on the table.
>
> ***THE OPEN COUNT: 17, AND READ IT FROM THE CHECKER, NEVER FROM PROSE.***
> `test-fixlist-units.ps1` — **182 passed, 0 failed** — lists **3, 6, 7, 8, 9,
> 11, 12, 16, 20, 24, 28, 31, 34, 39, 44, 54, 55**. It is unelevated and needs no
> install.
>
> ***IT WENT 15 → 17 ON 29 Aug, AND NOTHING NEW BROKE.*** **54** and **55** are
> the two verifier questions that had been sitting in this box as prose;
> filing them counts them. **That is the point** — the same session that says
> *read it from the checker, never from prose* should not be keeping two of its
> tasks in a paragraph. Nothing was closed and nothing regressed.
>
> *(How it reached 15: `6f5e9a8` ended with **17** open — not 16, which was true
> after 35 and 36 closed but BEFORE 52 was filed, and 52 is one of the two closed
> there. 17 − 4 − 52 = 15; 53 was opened and closed in the same session. An
> intermediate count quoted as a final one is the same error as the 143/144 in
> entry 4, one document up.)*
>
> ### ⇧ END OF WHAT TO DO FIRST ⇧
>
> ***HANDOFF, SEVENTY-FIFTH SESSION, 28 Aug 2026. THE WHOLE LIST RAN, AND 36
> WORKS END TO END.*** Two cycles, `b56` and `b57`, a restart, and the sweep at
> **21:51:50** printed **`5 considered, 5 reclaimed, 0 still pending, 0
> refused`**. Two defects were found and fixed on the way — **PRE_RELEASE 49 and
> 50** (filed as 42/43 and renumbered — see 49), both DONE and both measured on
> the installed tree. **`-List` elevated at
> 21:57:29 then said `0 records`**, and that reading is now worth something:
> since 49, an unelevated run refuses rather than printing the same sentence.
>
> ***36 IS COMPLETE: ALL FOUR RULINGS OBSERVED, 28 Aug 2026.*** The fourth is
> below and was the last one standing. `create.account` refusing a name
> whose profile directory is still there (10124/10125, `gpl.bp/PROFILE_DIR`)
> **had never been exercised** — no b56 or b57 log mentions either message,
> because every other verifier is careful to use a fresh name, so **the one rule
> that had never fired was the one nothing could vouch for.**
>
> ***IT IS MEASURED NOW. `gplbld/verify-profiledir.ps1`, ELEVATED, 28 Aug 22:18:
> 14 of 14*** — `create.account` refused `sdpd2x` over a leftover
> `C:\Users\sdpd2x`, printed 10124 naming both, created no Windows account, no
> `sdu_` group, no `ACCOUNTS` record and no suffixed home; and the control
> `sdpd2y`, identical but for the directory, was created and then deleted
> cleanly. ***SO ALL FOUR OF 36'S RULINGS ARE NOW OBSERVED.***
>
> ***ITS FIRST RUN SCORED 13 OF 14 AND THE PRODUCT WAS ALREADY RIGHT*** — see
> PRE_RELEASE 51. The refusal was in the transcript, complete and correct, and
> the matcher could not see it: message files hold **literal backslash-n**, not
> newlines, and `[regex]::Escape` turned each into a pattern hunting a literal
> backslash. **The same helper made `verify-delaccount.ps1:553` incapable of
> failing and `:568` — in the keep-both branch, which has never run here —
> certain to fail.** Both fixed; three latent copies are named in 45.
>
> ***`gplbld/verify-profiledir.ps1`.*** It makes its own fixture — `!profile_dir` is a `Test-Path`
> on `<ProfilesDirectory>\<name>` (`PROFILE_DIR:99-100`), so a bare directory is
> enough and the test needs no deleted account, no reboot and no reclaim store.
> **It carries its own control**: the same `CREATE.ACCOUNT` for a second name
> with no leftover directory must SUCCEED, so a refusal on its own cannot pass
> the run. 10124 is matched through `Get-SysMsgPattern` with **both**
> placeholders filled — the account name alone appears in the echoed command and
> in every other refusal the verb can print. On `$neverShipped`, and
> `assert-current` is **exit 0 live** after adding it.
>
> ```
> C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\verify-profiledir.ps1 -Prefix sdpd1
> ```
>
> **10125 stays unexercised** — "the check could not run" needs `os.execute` to
> fail, which nothing here can force.
>
> ***AND THE 61 → 56 COUNT IS THE PART A RERUN MUST KEEP.*** The tally line
> cannot see containment: 56 of the 61 directories had no record and had to be
> left alone, and a sweep that deleted more would still have printed
> `5 reclaimed, 0 refused`. **Count the directory before and after, every time.**
>
> ### ⇩ WHAT RAN, IN ORDER — ALL OF IT DONE ⇩
>
> ***STEPS 0 TO 4 ARE DONE. THE INSTALL IS 28 Aug 2026 21:27:34, GREEN, `b57` ON
> IT.*** The 20:48:24 install carried `b56`; the 43 fix then cost a second
> cycle. `assert-current` exit 0 live on both, **`gcat` 126 / `GPL.BP.OUT` 185**
> — up from 125/184, which is `gpl.bp/PROFILE_DIR` arriving and is the evidence
> that 36's BASIC half compiled rather than the report that it did.
>
> ***STEP 0 — `make sd`. DONE 28 Aug 2026 20:44, exit 0, clean.*** **It was
> missing from this list and the omission cost a cycle**: the 20:40:17 install
> staged `bin\sdsvc.exe` from **26 Aug 20:40**, so PRE_RELEASE 36's Windows half
> was installed without ever being compiled. `assert-current` check A2 caught it
> — the exact shape §6 records under *"`cycle.ps1` DOES NOT BUILD"*, found this
> time by the guard rather than by a wasted measurement. **The rebuild is real,
> not a no-op: `sdsvc.exe` 144,301 → 146,089 bytes.** Unelevated, MSYS2 login
> shell; the agent can run it.
>
> **STEP 1 — the cycle. `ELEVATED PowerShell`.** Nothing else can happen first:
> the BASIC has never compiled. ***OWED AGAIN AFTER STEP 0*** — the relink moved
> `sd.exe` `DF77FD6D61DE5184` → `C5834134AF60BBD9`, so check A refuses the
> 20:40:17 install and only a cycle clears it.
>
> ```
> C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\cycle.ps1
> ```
>
> **STEP 2 — the suite. An ORDINARY, UNELEVATED PowerShell, your own terminal,
> not an agent's (§4.0.1).** ***SPENT: b54, b55, b56, b57, b58. `b59` IS
> NEXT.*** `b55` was **burnt against the stale tree at 20:41:43** — see below,
> it is the one that teaches something.
>
> ```
> C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\VerifyInstall1.ps1 -ThenElevated -Run b59 -ContinueOnFailure
> ```
>
> ***THE SUITE'S SETTLED SHAPE, THREE RUNS RUNNING (b56 20:52, b57 21:30, b58
> 22:26): 13 of 13 unelevated, 18 of 19 elevated.*** That includes
> `verify-doors-suite` green, **which b56 did for the first time ever**
> (PRE_RELEASE 44). ***THE ONE FAILURE IS THE SAME ONE EVERY TIME***:
> `verify-apiadmin` **21/23**, the known stale control of **PRE_RELEASE 31**,
> now identical across **five** runs including two from before 36 was
> installed. **Treat a different number there as news; treat 21/23 as the
> baseline.**
>
> **b58 also proved a non-repair left nothing behind** — PRE_RELEASE 51's three
> insurance fixes — because `verify-accountacl` **21/0**, `verify-routes`
> **33/0** and `verify-accountrules` **34/0** are identical in b56, b57 and b58.
> A fix that was not fixing anything visible has to leave the counts alone, and
> "still green" would not have shown that.
>
> ***HOW `b55` WAS BURNT, BECAUSE THE SUITE'S OWN SUMMARY SAYS THE OPPOSITE.***
> Eleven steps exited 2 on `assert-current`'s STALE refusal and the door suite
> reported *"Create left nothing behind"* — so the run reads as having created
> nothing. **It created one thing.** `verify-sshonly.ps1` is deliberately exempt
> from `assert-current` (CLAUDE.md), so it ran, and the elevated batch was then
> **killed** — `post-cycle-elevated exited -1073741510`
> (`STATUS_CONTROL_C_EXIT`), its transcript stopping mid-line after *"Error 5
> getting semaphores"* with no transcript-end marker — **before its teardown**.
> Left on the machine, measured 28 Aug: Windows user `sdsshb55` **enabled**,
> `C:\Users\sdsshb55` created 20:42:44, and a `ProfileList` entry. No `sdu_`
> group. ***THE LESSON IS THE EXEMPTION, NOT THE KILL***: a refused suite is not
> a suite that did nothing, because the two exempt scripts run anyway — so
> **the run number is spent even when every reported step refused.**
>
> **Litter, and PRE_RELEASE 39's tool takes it** — ELEVATED, `-List` first, it
> changes nothing:
>
> ```
> C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\cleanup-devlitter.ps1 -List
> ```
>
> ***PRE_RELEASE 50 IS FIXED IN SOURCE AND OWES A CYCLE — SO STEPS 1 AND 2 RUN
> AGAIN, IN THAT ORDER, BEFORE THE REBOOT IS WORTH SPENDING.*** `-List` elevated,
> 28 Aug 21:15, found **5 genuine records and refused all five**: every one owned
> by `GITORLI\don`, the administrator whose session ran `DELETE.ACCOUNT`, against
> a check accepting only `S-1-5-18` or `S-1-5-32-544`. The owner check is gone
> and the store's ACL is the containment; units **39/39**, control `-Sweep` at
> the pre-43 copy **37/2**, red on those two rows alone.
>
> ***AND THE CYCLE DELETES THE FIXTURE ALONG WITH THE TREE.*** `C:\ProgramData\SD`
> goes, and `b56`'s five records go with it — so **`b56`'s five directories
> become litter with no record** (`sddrb56a`, `sddrb56b`, `sdapiab56`,
> `sdapinb56`, `sdapiidb56`; `cleanup-devlitter.ps1` takes them). **Fresh records
> can only come from a fresh suite run, which is why STEP 2 comes before the
> reboot rather than after the fix.**
>
> ***THE PRE-REBOOT STATE, MEASURED 28 Aug 21:50, SO THE SWEEP'S LOG CAN BE
> JUDGED AGAINST SOMETHING.*** `-List` elevated: **5 considered, 0 reclaimed, 5
> still pending, 0 refused** — `sddrb57a`, `sddrb57b`, `sdapiab57`, `sdapinb57`,
> `sdapiidb57`, all five directories present with their `ProfileList` entries.
> **`C:\Users` holds 61 `sd*` directories and 46 `ProfileList` `sd*` entries; only
> those five are recorded.**
>
> ***A PASS:*** the log ends `5 considered, 5 reclaimed, 0 still pending, 0
> refused`, the five directories and their entries are gone, and `-List`
> elevated then says **0 records**.
>
> ***AND THE LITTER IS A FREE CONTAINMENT CONTROL — USE IT.*** 56 of the 61
> directories have **no record** and the sweep must not touch one of them. `sd*`
> must fall **61 → 56 and by exactly those five**. Any other directory
> disappearing is a containment failure wearing the costume of a success, and
> the tally line alone will not say so.
>
> **STEP 3 — RESTART WINDOWS. This is the step that actually tests 36 and it is
> the one nothing else will remind you of.** The sweep only ever does anything
> on a boot: it is `sdsvc.exe` starting the SD service that runs it, and the
> profile hives it is waiting on come down at shutdown. Step 2 will have left
> profile directories under `C:\Users` — that is what makes the test real.
>
> **STEP 4 — read what the sweep did. UNELEVATED is enough for both.**
>
> ```
> notepad C:\ProgramData\SD\reclaim-profiles.log
> ```
>
> ```
> powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Program Files\SD\reclaim-profiles.ps1" -List
> ```
>
> **What a pass looks like:** the log names each record, prints `before:` and
> `after:` for the directory and the `ProfileList` entry, and ends `N
> considered, N reclaimed, 0 still pending, 0 refused`. The `b55` profile
> directories are gone from `C:\Users`. `-List` then says **0 records**.
> **`refused` on any row is the thing to read closely** — the reason is printed
> in full and each one is a deliberate guard, not a fault in itself.
>
> ### ⇧ END OF THE LIST ⇧
>
> ***WHAT WAS BUILT.*** All four of 36's rulings — `DELETE_USER` takes the
> directory first and keeps both halves otherwise, the pair is recorded under
> `C:\ProgramData\SD\profile-reclaim`, `gplbld/reclaim-profiles.ps1` sweeps it
> from `sdsvc.exe` at every service start, and `create.account` refuses a name
> whose profile directory is still there. **New `gpl.bp/PROFILE_DIR`, new
> statuses 6/7/8, messages 10075 and 10116 rewritten, 10123/10124/10125 new.**
>
> **What HAS been measured, and it is only the Windows half.** `sdsvc.c`
> compiles clean under the UCRT64 toolchain with `-Wall -Wformat=2`, 0
> warnings. `gplbld/test-reclaim-units.ps1` — **39/39, no install, no
> elevation, no store** — drives the sweep's refusal table, and its positive
> control against a copy with the containment check removed **fails 34/5 on
> exactly the five containment rows**. The sweep itself was watched running in
> `-List` mode: absent store says so and exits 0; a planted store's two records
> are both refused by name on the owner control, exit 1; an unelevated sweep
> refuses and exits 2. The five edited/added `.ps1` files parse 0 errors and
> carry no BOM and no CR. `DELETE_USER`'s generated PowerShell is **1944 chars**
> against `MAX_SH_COMMAND_LENGTH` 32000 — worth keeping an eye on, because
> `op_sh.c:216` answers an over-long command by doing **nothing** and setting
> `ER_LENGTH`, which would look exactly like a delete that left no profile.
>
> ***THE FIRST THING THE CYCLE'S OWN `verify-delaccount` WILL EXERCISE IS THE
> RE-SCOPED 32 TEST.*** ***That verifier's own step 3*** — not the RESTART step
> in the list above — now branches: both halves gone, or both halves
> kept **and recorded**. On this machine the hive is normally still up at that
> point, so the keep-both branch is the one that will run — and it reads the
> record back and asserts `10075` present, `10123` absent.
>
> ***TWO SCRIPTS NOW SHIP THAT DID NOT, SO THE DOCS ARE OUT BY TWO.***
> `secure-reclaim.ps1` and `reclaim-profiles.ps1` are in `stage.py`'s
> `ProgramFiles` list and are watched by `assert-current` like the rest;
> `test-reclaim-units.ps1` is on `$neverShipped`. **`Technical/02` in
> `SDCoreWindowsDocs` says *"all 26 that ship"* and it is 28** — nothing in this
> repository asserts that count, so nothing here will catch it. That is H.2's.
>
> ***THE OLD HANDOFF FOLLOWS, AND ITS ITEM 1 IS DONE.***
>
> ***HANDOFF, SEVENTY-THIRD SESSION, 28 Aug 2026.*** The cycle ran, the suite
> ran, **twelve unelevated steps exited 0 and the thirteenth — the new door
> step — failed.** Two faults, one in the wrapper and one in the instrument.
> **The install is current and `assert-current` is exit 0**; nothing is
> half-done.
>
> ***1. THE CLEAN-UP — AND `-Phase Remove` CANNOT DO IT. RUN, MEASURED, AND IT
> FAILED FOR A REAL REASON.*** `sddrb50a` is **STRANDED**: the 15:29:59 cycle
> deleted both trees, so its `ACCOUNTS` record went with the data tree — the
> register now holds only `don` and `sdsys` — while **the Windows account
> survived, enabled, with its own `sdu_` group and its memberships of
> `sdusers`, `sdssh` and `sdapi` intact**, and `sshd_config` still carries
> `AllowGroups sdssh`. **`DELETE.ACCOUNT` cannot reach an account SD has no
> record of**, so the removal is a Windows one. ***THAT IS PRE_RELEASE 39,
> MEASURED RATHER THAN REASONED, AND IN A STRONGER FORM THAN THE ENTRY
> CLAIMED.*** **ELEVATED PowerShell, `-List` first — it changes nothing:**
>
> ```
> C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\cleanup-devlitter.ps1 -List
> ```
>
> ***DONE — RUN TWICE, EITHER SIDE OF A REBOOT, AND READ BACK INDEPENDENTLY.***
> The stranded pair is **gone**: no `sddrb50a` user, no `sdu_sddrb50a` group.
> The `sddrb50a` profile went on the second run once the reboot unloaded its
> hive. ***THE ORPHAN-SID WORRY DID NOT MATERIALISE — MEASURED, NOT ASSUMED:
> `sdusers`, `sdssh` and `sdapi` all carry `0`***, so `Remove-LocalUser` took
> the memberships with it. **Nothing was over-deleted**: all five real SD
> groups (`sdusers`, `sdssh`, `sdapi`, `sdadmins`, `sdsshonly`) are present and
> `sdout` survived the home sweep. **The second run's `exit 1` is the designed
> INCOMPLETE, not a fault** — it refuses to read a sweep of what it could see
> as a sweep of the machine. ***AND THE STALE VM LINE IS WITNESSED FIXED***: it
> printed *"`sshRemoteTest-C1` is NOT registered - nothing to delete"*.
> ***IT COULD NOT HAVE SEEN THESE UNTIL NOW — PRE_RELEASE 45***: `sddr` was
> never in the stem list, so all four door families were invisible to both
> sweep scripts and a run would have reported a clean machine. **Added, both
> self-tests re-run green.** ***AND A REBOOT IS NEEDED BETWEEN THE ACCOUNTS AND
> THE PROFILES*** — a loaded hive cannot be removed, and `sddrb50a`'s is. The
> script says so itself before it deletes anything.
>
> ***THEN THE THREE UNREACHABLE DIRECTORIES, BY HAND, ELEVATED*** — the sweep
> prints the command for the first one and it is the same for each:
>
> ```
> Remove-Item -LiteralPath "C:\Users\sddr1a" -Recurse -Force
> Remove-Item -LiteralPath "C:\Users\sddr2a" -Recurse -Force
> Remove-Item -LiteralPath "C:\Users\sddrb51a" -Recurse -Force
> ```
>
> ***THE ORPHAN-SID CHECK IS DONE AND CLEAN.*** `cleanup-devlitter` calls
> `Remove-LocalUser` **without** stripping the user out of `sdusers`, `sdssh`
> and `sdapi` first — the ordering is section 1's on purpose, *"accounts first,
> so the profile sweep sees orphans"* — so an orphan SID was the thing to look
> for. **All three read 0 before AND after**, so nothing was left. Kept here as
> the check to repeat, not as an open worry:
>
> ```
> foreach ($g in @('sdusers','sdssh','sdapi')) { "$g : " + @(Get-LocalGroupMember $g | Where-Object { $_.Name -match '^S-1-' }).Count }
> ```
>
> ***`verify-doors-admin.ps1 -Prefix sddrb50 -Phase Remove` IS SPENT AND IS NOT
> WORTH RE-RUNNING.*** It now names the case rather than failing bare.
>
> ***`sddrb50a` IS STILL A LIVE, ENABLED, UNSUSPENDED WINDOWS ACCOUNT IN
> `sdusers`, `sdssh` AND `sdapi`*** — re-measured on disk after the `b51` run,
> not assumed. The Suspend and Remove legs never elevated on that run (fault
> 1), so the account the Create leg made is still there with ssh and API access
> and a password of the verifier's own generating. ***`sddrb51a` DOES NOT NEED
> THIS*** — the fixed suite removed it itself. **The profile directory
> `C:\Users\sddrb50a` will stay** — that is PRE_RELEASE 35/36 and only a
> restart releases it.
>
> ***2. THE SUITE RERUN — `-Run b52`, AND IT NOW TESTS SOMETHING NEW.*** In an
> ORDINARY, UNELEVATED PowerShell, his own terminal, not an agent's (§4.0.1):
>
> ```
> C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\VerifyInstall1.ps1 -ThenElevated -Run b53 -ContinueOnFailure
> ```
>
> ***`-ContinueOnFailure` IS ON HIS OWN RULING, 28 Aug 2026***, because the door
> step's failure has twice stopped the hand-over to `VerifyInstall2` and **the
> nineteen elevated steps have never run on this install.** It hands over
> whatever the door step does.
>
> # ⇧ PRE_RELEASE 19 IS CLOSED. `-Run b53`, ALL FIVE DOOR LEGS GREEN. ⇧
>
> ***THE CONDITION WAS THE OWNER'S — "19 stays B until the doors are covered" —
> AND IT IS MET BY A PASSING RUN.*** `Create` 13/13, `Control` 8/8, `Suspend`
> 5/5, `Refused` 5/5, `Remove` 4/4. **All three doors admitted, then all three
> refused, with the suspension the only thing changed in between.** The
> elevated half's only failure is `verify-apiadmin` — PRE_RELEASE 31's known
> control, four runs running — and **step 19 is now green, so 46 is confirmed
> fixed.** **`b53` is spent; `b54` is next.**
>
> ***WHAT IS LEFT ON THE MACHINE IS PROFILE DIRECTORIES AND NOTHING ELSE***: no
> Windows accounts, no `sdu_` groups, no `ACCOUNTS` records, **0 orphan SIDs**
> in `sdusers`, `sdssh` and `sdapi`. **The b52 and b53 suite runs left 24
> directories in `C:\Users`** — that is PRE_RELEASE 35/36 and the reason 36
> matters: two suite runs now cost two dozen of them.
> `cleanup-devlitter.ps1`, elevated, sweeps them after a reboot.
>
> ***`b52` RAN. THE DOOR OPENED; THE CHECK DID NOT.*** `Create` **13/13** —
> helper created, granted, and **Windows agreed** — and door 2's `WHO` answered
> ***`91 SDDRB52A from SDDRB52B`*** with **no 5161**. So 44's cure works and
> the local non-decisive witness failed in the same transcript, exactly as
> designed. **`Remove` 4/4, both accounts gone.** The one failing row was the
> anchor: `WHO` appends `from <ACCOUNT>` only on the success path, and the
> check required the account to be the whole of the second field. **Fixed and
> measured across five paths; `b53` is what closes 19.**
>
> ***THE ELEVATED HALF RAN FOR THE FIRST TIME ON THIS INSTALL — ALL 19 STEPS***,
> on the `-ContinueOnFailure` ruling. **Two failures, both diagnosed:** step 14
> `verify-apiadmin` is **byte-identical to b49's and the three runs before it**
> (PRE_RELEASE 31, open, and its headline hole still passes); step 19
> `verify-tierapi` is **PRE_RELEASE 46, new and now fixed** — it claimed
> ADMINISTRATOR 417 against a tree that says 416.
>
> | leg | result |
> |---|---|
> | `Create` (elevated) | **8/8** — `argv (15)`, password masked |
> | `Control` (ordinary) | ***2 of 7 FAILED, both `logto`*** — ssh and the API admitted in the same leg |
> | `Remove` (elevated) | **2/2** — `argv (13)`, no `-Password`. ***Ran as a suite step for the first time ever*** |
>
> ***THAT RUN IS THE WITNESS FOR BOTH FAULTS AT ONCE.*** Fault 1's fix let the
> two elevated legs launch; fault 2's fix made the Control leg tell the truth;
> and because the suite still ran `Remove` after stopping, **`sddrb51a` left no
> Windows account, no `sdu_` group and no `ACCOUNTS` record** — read from disk
> afterwards, only the 35/36 profile directory remains. **The three-door
> comparison inside one leg is the strong part**: same account, same session,
> ssh and the API in and `logto` out.
>
> ***FAULT 1 — PRE_RELEASE 43, FIXED.*** `verify-doors-suite.ps1` passed
> `'-Password', ''` for Suspend and Remove. **`Start-Process -ArgumentList`
> carries `[ValidateNotNullOrEmpty()]`, and on a COLLECTION that validates
> every ELEMENT** — one `''` rejects the entire list with *"The argument is
> null or empty"* and **nothing launches, so no UAC prompt ever appears.** The
> pair is conditional now (the idiom `sd-elevate.ps1:118` already used), the
> argv and its element count are printed, and an empty element is refused **by
> name**. `gplbld/test-doorsargv-units.ps1` guards it — **35/35, no install, no
> elevation, no account** — and its positive control, `-Suite` pointed at a
> copy carrying the old form, **fails 27/8**.
>
> ***FAULT 2 — PRE_RELEASE 19 IS RE-OPENED ON ONE ROW OF SEVEN.*** The check
> that said *"logto entered the account"* matched the account name **anywhere
> in the transcript**, and the session echoes what it is fed. On the b50
> Control leg **SD printed 5161 *"Unable to change to new directory"* and `WHO`
> answered `91 DON`** — and the row scored PASS. **It scored the same PASS on
> `sddr2`**, which is what the seventy-second session's *"logto ADMITTED"*
> rests on. Anchored on `WHO`'s answer now, with 5161 as a disqualifier.
>
> ***WHAT IS STILL PROVEN, AND WHAT IS NOT.*** **ssh and the API admitted
> genuinely** — both authenticate afresh. **All three REFUSALS still stand**:
> `logto.authorised` is called at `CPROC:2679`, *before* the chdir at `:2691`,
> so a suspended account is refused with 10107 and never reaches 5161. **What
> is unproven is the ADMITTED half, for one door of three.**
>
> ***THE CAUSE IS PRE_RELEASE 44 AND IT IS WINDOWS, NOT SD.*** `don` is in
> `sdu_sddrb50a` **on the machine** and **not in his own token**, because
> Windows fixes group membership at logon — measured both ways, with `sdusers`
> present in the same token as the control. So `logto.authorised` passes on the
> machine's list and the chdir is denied on the token's. ***RULED 28 Aug 2026
> AND BUILT: two accounts, as the door table says*** — *"grant user A into
> account B, suspend B, then ssh as A and `LOGTO B`"*, which
> PRE_RELEASE_FIXES' own door table specified before any of this was written.
> **The local `LOGTO` still runs and is recorded NON-DECISIVE**, so every
> transcript carries the evidence for why the helper exists.
>
> ***THE PRODUCT HALF OF 44 IS STILL OPEN AND IS STILL HIS.*** 5161 says only
> *"Unable to change to new directory"* — no mention that the group is not yet
> in the caller's token and a sign-out would fix it. **A verifier working
> around it is not the same as an administrator being told.**
>
> ***ALREADY ON THE MACHINE: `C:\Users\sddr1a`, `C:\Users\sddr2a` AND
> `C:\Users\sddrb50a`.*** The first two are swept clean otherwise — no Windows
> user, no `sdu_` group, no `ACCOUNTS` record, no orphan SIDs in `sdapi`,
> `sdssh` or `sdusers`. **The third is not**, until command 1 above runs. All
> three directories are **PRE_RELEASE 35/36** and only a restart releases them;
> `clean-test-profiles.ps1` will name them after one. **They block nothing**
> except reuse of those three names.
>
> ***THE FIVE LEGS ON `sddr2`, 28 Aug 2026 — GREEN AS REPORTED, AND THE
> `Control` ROW IS NOW KNOWN TO BE ONE ROW SHORT OF TRUE.***
>
> | leg | shell | result |
> |---|---|---|
> | `Create` | elevated | **8/8** |
> | `Control` | **unelevated, the agent's own** | **6/6 as scored — but the `logto` row was a false positive** (see fault 2). **ssh and the API admitted; `logto` did not** |
> | `Suspend` | elevated | **5/5**, and *still in `sdssh`* — the suspension moved no Windows group |
> | `Refused` | **unelevated, the agent's own** | ***4/4 — ALL THREE REFUSED*** |
> | `Remove` | elevated | **2/2**, fixture gone; profile directory left behind, **expected** |
>
> **ssh and `logto` refused in SD's own words** — 10107, *"Account SDDR2A is
> suspended"* — and **ssh refused AFTER the banner**, so authentication had
> succeeded and the refusal is `LOGIN`'s, not sshd's. **The API cannot identify
> its own refusal by design**, so what proves it is the pair: same account,
> same password, same call, admitted then refused, **the suspension the only
> thing changed in between.**
>
> ***BOTH PREFIXES ARE SPENT. A PREFIX IS SINGLE-USE ONCE ITS ACCOUNT HAS
> REACHED THE CONTROL LEG*** — the ssh login leaves a profile directory that
> `DELETE.ACCOUNT` cannot remove, Windows will not put a new profile where one
> already sits, and a rebuilt account would get a **suffixed home**: an
> unmeasured variable in a test whose whole point is that only the suspension
> changes. **`sddr1`, `sddr2` and `sddrb50` are used; a hand-run attempt takes
> `sddr3` and a suite run takes `b51`, and each measures its name free first**
> (no Windows user, no `sdu_` group, no `ACCOUNTS` record, no profile
> directory) — **which is exactly what stopped the second b50 attempt.**
>
> ***WHAT THE FIRST CONTROL RUN FOUND, AND WHY IT MATTERED.*** On `sddr1` the
> API refused with `QMError(): Invalid username or password` while the account
> was in `sdapi`, `sdssh` **and** `sdusers` — **route granted, credential
> absent.** `CREATE.ACCOUNT` prompts for the **Windows** password, which is
> what sshd checks; the API does SCRAM against a PBKDF2 verifier in
> `sdsys\$cred` that **only `MODIFY.PASSWORD` writes**. `Create` now sets it,
> anchored on `Password set for account` **case-sensitively** (`:153` prints
> *"has no password set"* on a path that has not set one). **SD then confirmed
> the diagnosis in its own words on `sddr2`:** *"Account SDDR2A has no password
> set. Setting the first one."* **The product half is PRE_RELEASE 42 and is the
> owner's call.**
>
> ***WHO RUNS WHICH LEG — MEASURED, NOT ASSUMED.*** The agent shell is
> `GITORLI\don` **UNELEVATED**, a child process reads back a batch file written
> to `TEMP` (so `SSH_ASKPASS` works from here), `ssh.exe` is on PATH and
> `sd-connect.exe` is present. ***So the agent runs the two UNELEVATED legs
> itself*** — `verify-doors.ps1 -Phase Control` and `-Phase Refused` — and the
> owner runs only the three elevated ones. §4.0.1 bars an agent from
> `VerifyInstall1`, not from a standalone verifier.
>
> **THE SEQUENCE IS FIVE PHASES AND EACH ONE PRINTS THE NEXT COMMAND**:
> Create → **Control (agent, unelevated)** → Suspend → **Refused (agent,
> unelevated)** → Remove. ***If the Control leg fails, STOP*** — a door that
> refuses before the suspension makes its later refusal worthless.
>
> ***WHAT THIS CLOSED — AND IT DID NOT, ON ONE ROW.*** *(Corrected by the
> seventy-third session: the `logto` door's ADMITTED half was a false positive,
> so **19 is re-opened on that row**. The owner's ruling that it **stays `B`
> until the doors are covered** is unchanged and is what re-opens it — a
> passing run is coverage only when the run measured the thing it names.)*
> ~~the last row of **PRE_RELEASE 19**, which the owner
> ruled on 28 Aug 2026 **stays `B` until the doors are covered**. A written
> verifier is not coverage; only a passing run is — and there is now a passing
> run, so **19 is struck**.~~ ***WHAT IS LEFT OF PRE_RELEASE 38 IS A DECISION,
> NOT A MEASUREMENT***: the pair is standalone and **not wired into
> `VerifyInstall1`**, deliberately, for the same reason `verify-acctmsgs` is
> not — it creates a real Windows account, and it needs an elevated half and an
> unelevated half. **Wire it into the two runners, or leave it standalone and
> named in the docs? Owner's call.**
>
> ***THE STATE YOU INHERIT.*** Install **28 Aug 15:29:59** — the owner's cycle,
> which shipped PRE_RELEASE 42 — `assert-current` **exit 0 run live after every
> change below**, tree clean. **Do not run a cycle to "get to a clean state";
> you are in one**, and the only changes since are in `gplbld`. *(Earlier text
> here named `67cf316` and the 00:53:34 install; both are superseded.)*
>
> **Spent — do not reuse:** `sdmsga`, `sdmsgb` (next `sdmsgc`), `sdtc1` (next
> `sdtc2`), `sddr1`, `sddr2`, `sddrb50`, `sddrb51`. **`zzprf` is re-runnable as
> it stands.** `b49`, **`b50`** and **`b51`** are spent; the next suite run is
> **`b52`**.
>
> ***ONE THING IS UNRUN AND WILL FIRST BE EXERCISED BY THAT SUITE RUN:*** 23
> verifiers had a dead ANSI strip that is now LIVE (PRE_RELEASE 10), and the two
> runners now close transcripts a step leaks (PRE_RELEASE 40). **If `-Run b50`
> shows a new failure, suspect those two changes before suspecting the product.**
>
> ***THIRTEEN PRE_RELEASE ENTRIES CLOSED ON 28 Aug 2026*** — 5, 10, 13, 14, 15,
> 22, 25, 26, 27, 37, 40, 41, plus six of 19's seven rows. *(**24 struck, 20
> open** as of the seventy-third session — counted from the table, not carried
> forward: 42 and 43 struck, 19 re-opened, 44 added.)*
>
> ***THE FOUR TRAPS THIS SESSION PAID FOR, EACH ONE COSTING A RUN OR NEARLY ONE.***
>
> 1. ***A VERB GIVEN NO ARGUMENT PROMPTS, AND DOWN A PIPE THE PROMPT EATS THE
>    NEXT LINE.*** `LIST.INDEX <file>` with no index name reached `LISTI:117`,
>    swallowed the `OFF` after it and hung to the timeout. `LISTI:117`,
>    `DELETEI:101`, `DELETEF:117` and `DELACC:96` all do this. **Name every
>    optional argument.** The tell is a transcript whose last line is a prompt
>    and whose next command never appears.
> 2. ***A PASSWORD THAT GOES THROUGH `SSH_ASKPASS` MUST USE THE cmd-SAFE
>    ALPHABET.*** `GeneratePassword` produces `^`, which cmd eats. **The fix was
>    already at `verify-createaccount.ps1:403` and was walked past** — the
>    "search the record" rule in its usual shape.
> 3. ***A PREMISE WRITTEN INTO A TEST AS THOUGH MEASURED.*** "127 is a hard SAM
>    limit" was reasoned, written into a header as fact, and false —
>    `Set-LocalUser` accepted a 150-character password and entry 22's refusal arm
>    recorded SKIP. **Measure before writing the comment.**
> 4. **The Bash tool's working directory PERSISTS between calls.** A `cat >>`
>    landed in the wrong directory and a byte-scan silently checked a file that
>    did not exist, reporting a clean result for nothing. **Use absolute paths.**
>
> ## ⇧ THAT IS THE HAND-OVER. EVERYTHING BELOW IS BACKGROUND. ⇧

> ## NOTHING IS BROKEN AND NOTHING IS HALF-DONE.
>
> ## THE DEVELOPMENT PHASE IS CLOSED. THE DOCUMENTATION PHASE IS THE WORK.
>
> ***7.18 AND H.5 BOTH CLOSED 26 Aug 2026, THE SIXTIETH SESSION, AND THE STATED
> 1.0-0 GATE IS EMPTY.*** The task table above is the authority on status, not
> this box. **`H.2` — documentation — is the only open row, and section 7 has
> nothing left in it.**
>
> ### HANDOFF, SEVENTY-FIRST SESSION — THE WITNESSES ARE WRITTEN AND UNRUN
>
> ***NOTHING IS BROKEN AND NOTHING IS HALF-DONE.*** The install of **28 Aug
> 00:53:34 is still current** — `assert-current` **exit 0 run live this
> session, after the three new scripts were added** — so the eight fixes can
> still be witnessed **without spending a cycle**. Nothing in `gplsrc` or
> `sdsys` was touched, deliberately: any edit there would make the tree stale
> and cost the install that is the only thing able to test them.
>
> ***TWO SCRIPTS DO THE EIGHT. THEY ARE YOURS TO RUN; I CANNOT — BOTH NEED AN
> ELEVATED SHELL.*** Both parse 0 errors, carry no BOM, and every refusal path
> in each was exercised unelevated and exits 2.
>
> **1. The five that need no account — entries 5, 13, 14, 15, 26.**
> Leaves nothing behind; creates and removes its own fixtures inside SDSYS.
> ***In your own terminal, ELEVATED PowerShell:***
>
> ```
> C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\verify-vocverbs.ps1
> ```
>
> **2. The three that need real accounts — entries 22, 27, 37.** Creates four
> Windows accounts and deletes all four; refuses up front if any name is taken.
> **`sdmsga` is free — measured this session** (no Windows account, no
> `ACCOUNTS` record, no profile directory for any of the four derived names).
> ***In your own terminal, ELEVATED PowerShell:***
>
> ```
> C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\verify-acctmsgs.ps1 -Prefix sdmsga
> ```
>
> **Neither is wired into `VerifyInstall1`, on purpose** — the second creates
> Windows accounts, and the suite is not the place to decide when that happens.
> They are standalone until you say otherwise.
>
> **`test-vocverbs-units.ps1` needs no install and no elevation** — 40 rows,
> run and green this session. It drives the first script's matchers against
> synthetic transcripts of a fixed build **and of the defect**, and requires
> every pattern to tell them apart.
>
> ***THREE OF THE SEVENTIETH SESSION'S SUGGESTED TESTS DO NOT WORK, AND TWO OF
> THEM WOULD HAVE SCORED A FALSE PASS.*** The table below is left as written
> because the ENTRIES it names are right; these are corrections to the
> *commands*, and each is why the scripts above do something different:
>
> - ***26 — `delete.file zzwork force` CANNOT FAIL.*** `DELETEF` guards both
>   prompts with `if not(force)` (`:250` and `:319`), so `force` suppresses
>   them whether or not the fix is present. The reproduction entry 26 itself
>   describes is the **`no.query`** form, which does *not* suppress them —
>   only the path comparison does. **A run of the `force` form would have
>   measured nothing and reported a pass.**
> - ***22 — the password `a` is ACCEPTED on this machine.*** `net accounts`
>   reports **minimum password length 0**, and complexity is off by default on
>   a client SKU, so that arm creates a real account instead of printing
>   10119. The script drives the two arms separately: the **mismatch** arm is
>   deterministic (`SET_PASSWD:101` compares the pair before Windows is
>   involved), and the **refusal** arm uses a **150-character** password, past
>   the SAM's 127-character limit for a local account. **If this host accepts
>   even that, the arm is recorded SKIP and not PASS**, and the account is
>   removed.
> - **13 — `qselect voc saving 3` needs an ACTIVE select list** or it stops at
>   `3290` (`QSELECT:196`). The script uses `QSELECT VOC * SAVING 3`, which is
>   self-contained; a preceding `SELECT` would print a second *"selected to
>   select list"* line, which is the wording under test.
>
> ***THE FIRST SCRIPT IS RUN AND GREEN — 36 PASS / 0 FAIL, ALL FIVE ENTRIES.***
> `verify-vocverbs.ps1` on the 00:53:34 install, owner's elevated terminal.
> **PRE_RELEASE 5, 13, 14, 15 and 26 are struck.** The evidence that is worth
> keeping, because each is the row a lazy check would have got wrong:
>
> - **5** — `.D ZZPRFD` printed `Delete VOC record 'zzprfd'?`, the lower-case
>   name from an upper-case verb. The defect could not print that line at all.
>   **Exactly one** delete prompt fired in the session, which is the
>   fall-through half.
> - **13** — the message ends in a list number, nothing dangling, and it
>   selected more than zero.
> - **14** — 10117 printed, **6146 never asked**, and `sdsys\messages` still on
>   disk. The absence of the question is the whole check; answering it reaches
>   the same place.
> - **15** — `delete.index zzprfak f1` answered *"Deleted index F1"*, and the
>   control held: an unknown name came back **as typed**, not upcased.
> - **26** — `delete.file zzprfw no.query` fired **neither** prompt. ***Not
>   tested with `force`***, which is what the seventieth session's table asked
>   for and which cannot fail.
>
> ***IT TOOK TWO RUNS, AND THE FIRST FAILURE WAS MINE.*** 21 of 22, failing at
> the entry 15 FIXTURE: `LIST.INDEX <file>` with no index name PROMPTS
> (`LISTI:117`), so it ate the `OFF` after it and the session sat until the
> timeout — while `CREATE.INDEX` had already said *"Added index for F1"*. Fixed
> to `LIST.INDEX <file> ALL`, and the fixture now carries three independent
> instruments instead of the one that could be eaten.
>
> ***THE CLASS, WHICH IS THE PART WORTH KEEPING: anything driven down a pipe
> must NAME every optional argument.*** `LISTI:117`, `DELETEI:101`,
> `DELETEF:117` and `DELACC:96` each prompt when theirs is omitted, and a
> prompt down a pipe answers itself with the next command. **The tell is a
> transcript whose last line is a prompt and whose next command never appears.**
> Same family as §6's *"piping a command into sd hangs the session"*, reached
> from the other end: not a bare command, but a well-formed script with one
> argument left off.
>
> **No stray `sd.exe`** — checked after the timeout; only the normal `sdwind`.
> The aborted run left `ZZPRFSRC` and `zzprfak` behind and the pre-clean
> removed both on the second run, so the script is re-runnable as it stands.
>
> ***THE SECOND SCRIPT IS RUN TOO — `verify-acctmsgs` 26 PASS / 0 FAIL / 1
> SKIP, `-Prefix sdmsga`.*** **27 and 37 are struck. 22 is HALF measured and is
> deliberately NOT struck.**
>
> - **27** — both `MODIFY.ACCOUNT ADD account=… to=…` and `… DELETE account=…
>   from=…` in the bytes the run added to `sdsys/audit`, **with the controls
>   first**: 10018 and 10021 in SD's own output, because the record is written
>   inside `if stat = 0` and a failed edit would otherwise read as a missing
>   audit record.
> - **37** — 10034 *"may reach this computer only over ssh"*, 10078 *"SD routes
>   for …: ssh and the API"*, **and both old wordings absent**. The
>   disqualifier is what carries this one: both lines contain "ssh", so a check
>   anchored there would have passed on the defect.
> - **22, mismatch arm** — 10118 printed, the other three of the four messages
>   absent, and answering `N` unwound the creation with no account and no
>   register record left.
>
> ***22'S "WINDOWS REFUSED" ARM (10119) HAS NEVER RUN, AND THE REASON IS A
> PREMISE OF MINE THAT WAS WRONG.*** The arm sends a **150-character** password
> on the stated grounds that 127 is a hard SAM limit for a local account
> whatever the policy says. ***`Set-LocalUser` ACCEPTED IT*** — so the account
> was created for real, the script said so, removed it, and recorded **SKIP**.
> **This is the "measure before writing the comment" trap**: the limit was
> reasoned, written as fact into the script's header, and is false here. It is
> **corrected in place rather than deleted**, because the next session will
> otherwise reason its way to the same password.
>
> ***THE OWNER RULED: CHANGE THE POLICY FOR THE TEST (28 Aug 2026).*** So the
> password is now **chosen from the policy rather than guessed**.
> `Get-PasswordPolicy` reads `MinimumPasswordLength` and `PasswordComplexity`
> with `secedit /export` — locale-independent, unlike parsing the prose
> `net accounts` prints, which is kept only as the fallback — and
> `Select-RefusedPassword` breaks whichever rule is in force: **one character
> short of the minimum**, or **a single character class** against complexity.
> With no rule in force there is nothing to break, and the arm says so and
> SKIPs. `test-acctmsgs-units.ps1` drives that chooser with policies this host
> does not have: **35 rows, all passing**.
>
> ***THE SCRIPT STILL DOES NOT CHANGE THE POLICY, AND THAT IS DELIBERATE.*** It
> reads it and adapts. Changing a machine's password policy has to be somebody's
> decision, made once, in the open, and **reverted afterwards** — not a side
> effect of running a test.
>
> ***AND IT RAN: 31 PASS / 0 FAIL / 0 SKIP, `-Prefix sdmsgb`.*** The three
> elevated commands were `net accounts /minpwlen:14`, the verifier, then
> `net accounts /minpwlen:0`. **10119 printed naming the account**, with the
> mismatch and unelevated messages absent and the retry still offered, so both
> arms of entry 22 are now measured and it is struck.
>
> ***THE POLICY IS BACK: minimum length 0, read AFTER the run, not assumed.***
> Leaving 14 in force would have changed how every later `create.account` on
> this machine behaves.
>
> ***AND NOTHING WAS LEFT BEHIND BY EITHER PREFIX*** — no Windows account,
> register record or profile directory for any of the eight names across
> `sdmsga` and `sdmsgb`, and `C:\Users` holds only `b48adm`, `dmont` and
> `Public`. Read from disk, not from what the deletes reported.
>
> ***`sdmsga` AND `sdmsgb` ARE SPENT. THE NEXT PREFIX IS `sdmsgc`.***
>
> ### `verify-tierchange.ps1` — ***THIS HEADING WAS WRONG. CORRECTED 31 Aug 2026, PRE_RELEASE 109***
>
> ***IT DID NOT PASS 28 OF 28. IT CANNOT HAVE.*** `-Run b89` ran the same file
> against the same product on 31 Aug and got **27 of 28**, failing the 10115
> check — and `git log -S` puts **the check, `Test-Say`, `tier.os.remove` and
> message 10115 all unchanged since before the 28 Aug run** (`5251a3d` 28 Aug,
> `62217b6` 27 Aug). **No transcript survives to say otherwise**: this was a
> hand-run, and only a runner step writes a numbered log. **The likeliest
> reading is that the verdict line's *"28 decisive checks"* was recorded here as
> *"28 PASS"*** — the instrument-misreading class CLAUDE.md already catalogues.
> **The defect was the verifier's, not the product's** — see PRE_RELEASE 109.
>
> ***FIRST RUN, NO FIXES NEEDED*** — the only one of the three verifiers this
> session that passed on the first attempt. **`sdtc1` is spent; use `sdtc2`.**
> Nothing left behind, read from Windows rather than from what
> `DELETE.ACCOUNT` said.
>
> ***THE ARITHMETIC CONFIRMED ITSELF, WHICH IS THE POINT OF BUILDING IT THAT
> WAY.*** `D = 397` arrived by **two independent routes** — `A + added −
> removed` from what 10113 said, and `P + kept` from what a clean downgrade
> would have been — and they agreed. `added 0, removed 19, kept 1` against 20
> administration verbs: **the edited record is provably still there and provably
> the only difference.** No count is typed anywhere in the file.
>
> ***THE LAST ROW OF 19'S TABLE — THE THREE DOORS — IS NOW COVERED, 28 Aug
> 2026.*** `verify-tierchange` never claimed them: it prints them as NOT tested
> rather than scoring them, which is why the row survived to be closed
> honestly. The `verify-doors` pair covers them, all four legs green on
> `sddr2`. **The ruling *"19 stays B until the doors are covered"* is satisfied
> by that run, so 19 is struck.**
>
> **The table below is kept as written** — it is the analysis of *why* nothing
> reached the doors, and it is what the pair was built from.
>
> ***WHAT EACH DOOR NEEDED, AND WHY NOTHING REACHED IT BEFORE:***
>
> | door | where | why nothing reaches it yet |
> |---|---|---|
> | `LOGIN` (ssh/console) | `LOGIN:477` → **10107** | needs a **real ssh login** as the suspended account. `verify-sshonly.ps1` already has the `SSH_ASKPASS` machinery to borrow |
> | `logto` | `CPROC:3776` → **10107** | needs an **UNELEVATED** session. `verify-tiers` must be elevated to create accounts at all, so its `LOGTO` takes `CPROC:3729`'s bypass — it asserts the bypass rather than working around it |
> | the API | `APISRVR:507` → **10003** | 10003 is **deliberately** what *"no such account"* and *"not granted"* also answer, so wording proves nothing. It needs a **controlled pair on one account**: the same account reachable, then suspended, then reachable again |
>
> **The shape is PRE_RELEASE 38.** The awkward part is not the checks, it is
> that one script must create accounts **elevated** and then measure them
> **unelevated** and **over ssh** — which is why the suite is split into
> `VerifyInstall1` and `VerifyInstall2` in the first place.
>
> ### THE DOOR PAIR HAS MET SD — `verify-doors-admin.ps1` + `verify-doors.ps1`
>
> ***A PAIR, LIKE THE SUITE, BECAUSE THE TWO HALVES NEED OPPOSITE TOKENS.***
> The fixture needs an **elevated** process (`CREATE.ACCOUNT` and
> `MODIFY.ACCOUNT` are `K$ADMINISTRATOR`); the measuring must be **unelevated**,
> because `logto` reaches its suspension test only *after* `CPROC:3729`'s
> elevated bypass. **`verify-doors.ps1` refuses to run elevated** and says why —
> measuring that door from an elevated session would report the design working
> as a fault, which is the mistake `verify-tiers` section 6 declines to make.
>
> ***FIVE COMMANDS, AND EACH PHASE PRINTS THE NEXT ONE.*** ***`sddr1` IS SPENT
> — its profile directory survives the delete and a rebuild under that name
> would get a suffixed home (see the box at the top). `sddr2` is free,
> measured 28 Aug.*** Start ELEVATED:
>
> ```
> C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\verify-doors-admin.ps1 -Prefix sddr2 -Phase Create
> ```
>
> ***A PREFIX IS SINGLE-USE ONCE ITS ACCOUNT HAS SIGNED IN OVER ssh.*** The
> Control leg's ssh login creates a Windows profile, and `DELETE.ACCOUNT`
> cannot remove it while its hive is mounted (PRE_RELEASE 35/36). **Take a
> fresh prefix for every attempt** rather than reusing one that reached the
> Control leg.
>
> It prints the generated password and the exact unelevated command to run
> next. The order is **Create → Control (unelevated) → Suspend → Refused
> (unelevated) → Remove**.
>
> ***THE CONTROL LEG IS NOT A FORMALITY.*** If a door refuses *before* the
> suspension, its refusal after one proves nothing — and the likeliest causes
> are mundane, a wrong password or the caller not in the account's group. The
> script says STOP in those words rather than carrying on.
>
> **Three things it gets right that a first attempt would not:**
>
> - ***The ssh refusal is SD's, not sshd's.*** Suspension moves no Windows
>   group, so ssh authenticates in **both** phases and `ForceCommand` starts SD
>   in both. The anchor is **10107 in the session output**, not an ssh failure —
>   a run where ssh itself failed would be measuring a different defect and
>   scoring it as a pass. The Suspend phase asserts the account is **still in
>   `sdssh`** for that reason.
> - ***The caller is added to the account's group at Create.*** Without it
>   `logto` is refused as *"not allowed in requested account"* in **both** legs,
>   and the refusal proves nothing. Adding them makes the suspension the only
>   thing that changes.
> - ***The API door cannot identify itself and the script says so.*** `10003` is
>   deliberately what *"no such account"* and *"not granted"* also answer. Only
>   the controlled pair distinguishes it, and the file states that instead of
>   pretending the refusal is self-identifying.
>
> **It does not touch `sd.conf`.** `APIPORT=4243` was measured on and listening;
> if it were not, that door records **SKIP**. A verifier that restarts SD to
> measure a refusal has changed the thing it is measuring.
>
> **Parse 0 errors, no BOM, 8 identical `Write-Verdict` copies, 126 of 126
> verdict assertions, every refusal path exercised.**
>
> ***BOTH HALVES HAVE NOW MET SD, 28 Aug 2026.*** `-Phase Remove` 2/2,
> `-Phase Create` 6/6, `-Phase Control` **5 of 6 — ssh and `logto` ADMITTED,
> the API refused for a MISSING CREDENTIAL, not a missing route.** `Create` was
> the thing at fault and now sets the SD password with `MODIFY.PASSWORD`;
> the product half is **PRE_RELEASE 42**. The written-and-unrun claim above
> stands as the record of what pre-flight checking did and did not catch:
> **parse, BOM and refusal paths all passed, and the fixture was still
> unusable, because no static check knows that the API reads a different
> credential store than ssh.**
>
> ### the original hand-over, kept for the reasoning
>
> **PRE_RELEASE 19 is a `B`, and correcting it was worth more than believing
> it.** Three of its claims are false — see the dated block at the top of the
> entry — and the one that mattered was ***"the test cannot be piped"***, which
> was **wrong when written** and had kept a verifier from being attempted at
> all. A password prompt is answered perfectly well by the next LINE of one
> string; `verify-tiers.ps1` had been creating accounts that way for weeks.
>
> **What is genuinely left of 19 is three rows, and this covers them:**
>
> | row | what proves it |
> |---|---|
> | the required keyword | `modify.account X programmer` on an administrator prints **10111** and **nothing moves** — tier, Windows group and `os.users` all still ADMINISTRATOR afterwards |
> | what leaves with ADMINISTRATOR | Windows `Administrators` membership **and** the `os.users` record, both asserted PRESENT after the promote so their removal is a *transition* and not an absence |
> | the "left alone" count | one admin verb's VOC record is made to differ with `.S`, then **`D = P + kept`** — a clean downgrade lands back on `P`, so the kept record is provably there and provably the only difference |
>
> ***NOT ONE COUNT IS TYPED.*** The account's VOC is measured three times — as
> PROGRAMMER, as ADMINISTRATOR, as PROGRAMMER again — and the rows assert the
> relations: `A > P` (the null case), `D = A + added − removed` (10113 agrees
> with the file), and `D = P + kept`. This is the trap that printed *"the 21
> administration verbs … 20 20 PASS"*.
>
> ***ELEVATED, YOUR OWN TERMINAL. `sdtc1` IS FREE — measured.***
>
> ```
> C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\verify-tierchange.ps1 -Prefix sdtc1
> ```
>
> ***THE ACCOUNT IS A WINDOWS ADMINISTRATOR FOR PART OF THE RUN***, which is the
> point of the test. The downgrade is asserted before the delete, and the
> clean-up reads Windows rather than trusting what `DELETE.ACCOUNT` said.
>
> **Parse 0 errors, no BOM, 6 identical `Write-Verdict` copies, 96 of 96 verdict
> assertions, both refusal paths exercised. It has never met SD.**
>
> ***`sdmsga` IS SPENT. THE NEXT PREFIX IS `sdmsgb`.*** The run left nothing
> behind — no Windows account, register record or profile directory for any of
> the four names, read from disk rather than from what the delete reported.
>
> ### HANDOFF, SEVENTIETH SESSION — GREEN, PUSHED, AND EIGHT FIXES AWAIT A WITNESS
>
> ***NOTHING IS BROKEN AND NOTHING IS HALF-DONE.*** Repository pushed and clean
> at `4735957`. **Install 28 Aug 00:53:34, `assert-current` exit 0,
> `verify-tiers` 33 PASS / 0 FAIL.** `sd.exe` `DF77FD6D61DE5184` unmoved —
> everything this session changed is BASIC, messages and one deleted VOC record.
>
> ***START HERE: EIGHT FIXES ARE INSTALLED AND NOBODY HAS RUN THEM.*** They
> compiled and they shipped; that is not the same as working, and the install
> is current **now**. Another cycle only puts them back in this state. Each is
> one command in an ordinary SD session:
>
> | entry | what to type | what proves it |
> |---|---|---|
> | **5** | save a paragraph as `daily`, then `.d DAILY` | it deletes. Then `.d nosuchname` must say **not found in VOC**, not act on a stale record |
> | **13** | `qselect voc saving 3` | the message ends with **a list number**, not a dangling *"select list "* |
> | **14** | `delete.file <a file whose part is in SDSYS> no.query` | it does **not** prompt, prints **10117**, and leaves the system file |
> | **15** | `create.index`, then `delete.index zzak f1` in **lower case** | it deletes. A genuinely unknown name must still echo **as typed** |
> | **22** | `create.account user zztest programmer both`, give a password Windows refuses (`a`) | **10119**, not a bare retry. Mismatched pair gives **10118** |
> | **26** | `create.file zzwork`, then `delete.file zzwork force` in lower case | **neither** DATA nor DICT prompt fires |
> | **27** | `modify.account <acc> add <user>`, then read the audit file | a `MODIFY.ACCOUNT ADD account=… to=…` record exists |
> | **37** | `create.account user zztest2 programmer both` | the two lines name **different subjects** and no longer contradict |
>
> **Then strike them in PRE_RELEASE_FIXES.md** — they are marked *COMPILED AND
> INSTALLED — UNTESTED* on purpose, and only **25** is struck, because
> `verify-tiers` measured it.
>
> ***WHAT IS OPEN: 30 ENTRIES.*** Of the eleven-entry batch, **6 and 12 remain,
> and both entries were WRONG about what they needed** — 6 is an investigation
> (the `C:` directory is remade by every install; no install-time `CREATE.FILE`
> exists and the parser fix predates it), and 12 is a **C** change at
> `gplsrc/op_dio3.c:853`, not the message-only edit its entry claims.
> **PRE_RELEASE 36 is RULED and NOT BUILT** — the entry's first block is the
> spec. **41 is new**: the cleanup sweep reports *"every section reached zero"*
> while orphan directories remain, because its counter and its cleaner share one
> blind `Win32_UserProfile` enumeration.
>
> ***MACHINE STATE, MEASURED AT HANDOFF.*** `C:\Users` holds only `b48adm`
> besides the built-ins — **its Windows account is live and its SD account was
> destroyed by the cycle**, which is the 32/35/36 shape and was predicted before
> the run. SD register: `don`, `sdsys`, `sdtier1/2/3` — the last three are
> `verify-tiers` residue left deliberately. ***`sdtier` AND `sdtierb` ARE SPENT;
> USE `sdtierc`.*** `b48tier`, `b48susp` and `b48adm`'s SD halves are gone.
>
> ***THREE TRAPS THIS SESSION PAID FOR.***
>
> 1. ***NEVER REWRITE A TRACKED FILE WITH POWERSHELL `Set-Content`.*** Used for
>    a two-row table swap, it read the UTF-8 file as CP1252 and wrote it back
>    double-encoded — **all 272 em dashes became `â€"`** — plus a BOM and CRLF
>    throughout. ***THAT QUOTED SEQUENCE IS THE ONLY ONE IN THIS FILE, IT IS
>    EVIDENCE RATHER THAN DAMAGE, AND §0 STATES THE EXPECTED COUNT SO NOBODY HAS
>    TO INVESTIGATE IT AGAIN.*** **The mojibake is silent**; stripping the CRs made the diff
>    *smaller*, which reads like progress. Recovery is `git checkout` and redo
>    with the editing tools.
> 2. ***A CONSTANT TYPED INTO A LABEL DRIFTS FROM THE VALUE BESIDE IT.*** A
>    `verify-tiers` row printed *"the 21 administration verbs are still
>    ABSENT … 20 20 PASS"*. Interpolate the count; never type it.
> 3. **`grep -l '\n'` matches the letter `n`**, so it "found" the escape in
>    nearly every message file. Use `grep -F`.
>
> ### HANDOFF, SIXTY-NINTH SESSION — NOTHING IS BROKEN, NOTHING IS HALF-DONE
>
> ***THE SESSION ENDED ON CREDIT.*** Both repositories **pushed and clean**, the
> install **green and current**, `C:\Users` clean, and every fix in the tree is
> compiled. **What is left is seven decisions and three measurements, all listed
> below.**
>
> ***START BY READING PRE_RELEASE_FIXES.md.*** Seven entries are open and
> **six of them are yours to rule on, not work to be done**: **31** (rewrite
> `verify-apiadmin`'s stale control), **34** (`release.ps1` cannot finish on a
> zero-link set), **36** (***RULED 27 Aug — no longer a decision. It is now
> WORK, and the entry's first block says exactly what to implement***), **37**
> (`create.account` prints two contradictory lines), **38** (the suite tests
> SUSPENDED on no door), **39** (uninstall leaves every account without its ssh
> confinement), **40** (a verifier's transcript records the verifiers after it).
>
> ***THE THREE MEASUREMENTS THEN OWED — TWO ARE NOW DONE.*** ~~item **5.2's API
> door** (`APISRVR:507`, never reached — and it **cannot be tested by its
> wording**, which is deliberate, so it needs a controlled pair)~~ — **DONE
> 28 Aug 2026: the controlled pair ran on `sddr2`, ADMITTED then REFUSED.**
> ~~item **5.5**, `verify-tierchange.ps1`~~ — **DONE 28 Aug, 28 PASS.** **STILL
> OWED: item 5.4**, `tools\sdprobe.ps1 -Source tools\probes\p25-holdtrip.b` in
> the docs repo, 15 cases, compiled clean and **never run**.
>
> ***THE FIXTURES EXIST AND ARE NOT IN THEIR ORIGINAL STATES.*** `b48tier` is
> **STANDARD** now, not PROGRAMMER — item 5.1 downgraded it — and its
> `voc/basic` carries a hand-edited fourth line, which is the record the
> downgrade left alone. `b48susp` is **SUSPENDED**. `b48adm` is **PROGRAMMER,
> `both`**, password known to the owner, and it **has signed in over ssh**, so
> deleting it will leave a profile directory (entry 35/36, expected).
>
> ***`b49` IS SPENT. THE NEXT SUITE RUN IS `b50`.***
>
> ***THREE TRAPS THIS SESSION PAID FOR, WRITTEN ONCE.***
>
> 1. ***COUNT A SUITE RUN FROM THE PER-STEP CAPTURES***,
>    `<time>-NN-verify-*.log`, which are one file per step by construction. A
>    `verify-<name>-*.log` may contain **later** verifiers' output — 15 of 33
>    verifiers never stop their transcript (entry 40). A wrong verdict was
>    issued and withdrawn on exactly this.
> 2. ***A REBOOT CLEANS NOTHING. IT ONLY UNLOCKS.*** `cleanup-devlitter.ps1`
>    needs one **because a mounted hive cannot be removed** — that line was in
>    this file the whole time and four exchanges went on rediscovering it.
>    **When a symptom appears, grep the record; knowing a warning is not the
>    same as reaching for it.**
> 3. ***MEASURE BEFORE WRITING THE COMMENT.*** "Status 6 is harmless" was
>    reasoned, reached the code, a shipped message and the changelog, and was
>    false. It cost three rounds.
>
> ***GREEN AND CURRENT: INSTALL 27 Aug 22:52:21, `assert-current` EXIT 0.***
> `gcat` **125** / `gpl.bp.out` **184**, `sd.exe` `DF77FD6D61DE5184` **unmoved**
> — everything this session changed is BASIC, messages and one shipped comment.
> **Suite `-Run b49`: 30 of 31 steps, 963 `PASS`, 1 `[FAIL]`, 0 `[SKIP]`**, the
> one failure being PRE_RELEASE 31's known stale control.
>
> ***STALE AS OF 28 Aug: `C:\Users` HOLDS 11 DIRECTORIES AGAIN, 10 OF THEM
> ORPHANS, AND 22 HIVES ARE LOADED.*** The sweep below did happen; **the `b49`
> suite refilled it afterwards**, which is the measurement PRE_RELEASE 36 now
> carries. Three of the ten have no `ProfileList` entry at all. **A reboot's
> repair lasts one suite run.**
>
> ***AND `C:\Users` IS CLEAN FOR THE FIRST TIME IN WEEKS*** — the post-reboot
> sweep took **53, failed 0**, and the three `b49`/`b50` directories this
> session made were removed by hand. Only `Default`, `dmont` and `Public`
> remain.
>
> - **PRE_RELEASE 23 is fully closed.** The three docs pages that said
>   `term default` does not restore 120 x 36 are corrected —
>   `SDCoreWindowsDocs` `c41d999`.
> - **The shipped-scripts gap is closed.** `Technical/02` The Installed Scripts,
>   all **26** of them (the recorded 25 was measured wrong), and tester `01` now
>   prints the `install-ssh.ps1` retry command it only promised —
>   `SDCoreWindowsDocs` `7914e60`.
> - **Item 5.3 is closed.** The owner ran `edit bp ZZMARKS` unelevated on the
>   19:37:47 install — **no problems**. Both editors are now witnessed.
> - **Two new pre-release entries, 33 and 34.** ***33 is already fixed*** —
>   `allow-ssh-groups.ps1`'s usage line now names the `-Installed` it requires;
>   comment only, and it rides 32's cycle. **34 is in item 4's table and needs
>   your ruling.**
> - ***PRE_RELEASE 32 IS FIXED AND MEASURED — AND THE MEASUREMENT FOUND 35.***
>   `DELETE_USER`'s `catch { exit 6 }`, which left **both** halves of the
>   profile behind, is `catch { }`, and the `ProfileList` key is removed in its
>   own right. Cycled at **21:58:17** and tested end to end. **The registry
>   half works**: the deleted account's entry was gone. ***AND THE SYMPTOM
>   HAPPENED ANYWAY*** — the recreated account landed at
>   `C:\Users\b49home.GITORLI` because the **directory** survived, and Windows
>   will not put a new profile where a directory already sits either.
> - ***PRE_RELEASE 35: BOTH HALVES CAUSE THE SAME SYMPTOM, AND I HAD WRITTEN
>   THAT STATUS 6 WAS HARMLESS.*** That claim was reasoned, not measured, and
>   it had already reached the code comments, message `10075` and the
>   changelog. All three are corrected. ***AND THE DIRECTORY HALF CANNOT BE
>   FIXED AT DELETE TIME — MEASURED FOUR WAYS.*** `Remove-Item` fails with
>   `IOException` on **`UsrClass.dat`**; the directory is owned by
>   `BUILTIN\Administrators`, so it is not permissions; `reg unload` of both
>   hives is **refused elevated**; and even `Rename-Item` is refused. **The
>   path cannot be freed while the hive is mounted.** `DELETE_USER` still tries
>   — it succeeds for an account that never signed in — and `10075` now names
>   the cause and the restart. ***UNCOMPILED — IT NEEDS ANOTHER CYCLE.***
> - ***PRE_RELEASE 36 IS THE ROOT CAUSE OF ALL OF IT, AND IT IS YOURS.***
>   **22 orphaned SIDs — 44 hives — were mounted on this host**, every one for
>   an account that no longer exists. That is why `Remove-CimInstance` failed
>   in the first place, and it is probably why the 53 stale `ProfileList`
>   entries were never swept: `clean-test-profiles.ps1` uses the same call.
>   **Nothing SD does can unmount them; only a restart.** Two decisions in the
>   entry, neither built.
> - ***AND THE RECORD ALREADY SAID SO.*** The `cleanup-devlitter.ps1` line —
>   *"a loaded hive cannot be removed"* — has been in this file since 26 Aug. I
>   quoted it myself in the runbook earlier in the session, then spent four
>   exchanges rediscovering it. **Knowing a warning is not the same as reaching
>   for it when the symptom turns up.**
> - ***THE TEST THAT FOUND IT IS WORTH KEEPING, AND ITS ONE TRAP IS THE ssh
>   LOGIN.*** A brand new Windows account has **no profile until it signs in
>   once**, so a create/delete/create test without a login leaves nothing
>   behind and passes while proving nothing. Full form in PRE_RELEASE 35.
>
> ***THE FIXTURES WERE ALREADY GONE, AND THIS BOX SAID OTHERWISE FOR HALF A
> SESSION.*** The sequencing note here read *"5.1 and 5.2 go first, before any
> source change, because a fresh install destroys the fixtures"*. **The fresh
> install had already happened**: `b48tier`, `b48susp` and `b48adm` were made
> against **18:58:55** and the **19:37:47** cycle wiped both trees. Item 3
> carries the measurement.
>
> ***THE TELL WAS AVAILABLE AND WAS NOT USED.*** The same box records that the
> 19:37:47 cycle destroyed the `ZZMARKS` fixture and had it rebuilt. A cycle
> does not destroy one fixture. **When a cycle is known to have eaten something,
> the question is what else it ate.**
>
> ***SO THE ORDER INVERTS: nothing is waiting on this install, and PRE_RELEASE
> 32 is free to go first.*** Rebuild the three accounts on the install after
> its cycle, `cleanup-devlitter.ps1` first — the Windows halves outlived the SD
> halves and a same-name rebuild is exactly PRE_RELEASE 32's defect.
>
> ### HANDOFF, SIXTY-EIGHTH SESSION — READ THE FIVE NUMBERED ITEMS FIRST
>
> ***THE SESSION ENDED ON CREDIT, NOT ON A PROBLEM.*** `sd4windows` is **pushed
> and clean**, the install is **green and current**, and **nothing is
> half-written or half-installed**. The docs repository was not touched this
> session and has one correction owed (item 4).
>
> ***WHAT WAS DONE: FOUR PRE_RELEASE ENTRIES CLOSED AND TWO NEW ONES FOUND.***
> 21, 23 and 29 fixed, installed and **measured**; 30 (a stale verifier) fixed
> and passing in-suite; `-Run b48` scored **30 of 31**. New and open: **31**
> (`verify-apiadmin`'s control is stale — needs your ruling) and **32**
> (`delete.account` leaves the `ProfileList` entry, so a recreated account gets
> a different home and loses its ssh keys — a real user-facing defect).
>
> ***THE ONE THING TO PICK UP IS SMALL:*** `edit bp ZZMARKS` unelevated, thirty
> seconds, item 5.3. Everything else outstanding is a decision or another
> repository.
>
> ***AND THE LESSON THIS SESSION KEEPS PAYING FOR, WRITTEN ONCE:*** PRE_RELEASE
> 29 took **three** attempts, and each fix was reported before it was measured
> **in the place it runs**. A console is not `os.execute`; the installed tree is
> not the source tree. **Run it where it runs, and print what the instrument
> actually read.**
>
> ## ***1. PRE_RELEASE 29 IS DONE. THE TREE IS GREEN. NOTHING IS HALF-DONE.***
>
> ***Install 27 Aug 19:37:47, `assert-current` exit 0.*** The owner ran
> `micro bp ZZMARKS` **three times, save and no-save, no message.**
> **`~/.micro/backups/` now exists** — the very write that used to fail, and it
> had never appeared once before. **The mark round trip survived a real save**:
> SD reads the record back as 19 fields, 907 chars, VM 6 / SM 1 / TM 3, no stray
> CR or LF. ***That closes the last of item 5.3.***
>
> ***IT TOOK THREE ATTEMPTS AND THE PATTERN IS THE POINT.*** Each fix was
> reported before it was measured where it runs:
>
> - **`-backup off`** — reasoned from micro's option defaults, fixed nothing.
> - **The helper read `$env:USERPROFILE` and `$env:TEMP`, EMPTY inside
>   `os.execute`.** Tested four ways beforehand — **all four from a console**,
>   the one environment those runs held constant.
> - **`EDIT` split the capture on `char(10)`** where it is `@fm` with trailing
>   `CR` and **no LF at all** (`FM=7 CR=8 LF=0`, measured).
>
> **Also found:** `[System.IO.Path]::GetTempPath()` answers `C:\WINDOWS\` when
> TEMP is unset — elevated, the fallback would have created
> `C:\WINDOWS\sd-micro`. Any candidate under the Windows directory is refused.
>
> ***AND `cycle.ps1` DESTROYS THE `ZZMARKS` FIXTURE*** — it deletes both trees,
> so `don`'s BP goes too, and `EDIT` happily opens a record that does not exist.
> One run was wasted editing an **empty new record** before anyone noticed.
> **Rebuild it after every cycle**: `tools\probes\make-zzmarks.py` (docs repo),
> sha `1D65F19475F3CA5DCC5D594897F6B9CB`. It is rebuilt and canonical now.
>
> **A micro save rewrites the record on disk with `dos` line endings** — 908 →
> 927 over 19 lines. **Benign**: SD's reader normalises them, measured above.
>
> ### The 18:58:55 install, which the suite below scored
>
> ***`assert-current` was exit 0 live on it.*** `sd.exe`
> `DF77FD6D61DE5184` (unmoved — all BASIC), `gcat`/`gpl.bp.out` **125 / 184**.
> **The micro fix is in it, verified by reading the install**: `micro-home.ps1`
> in Program Files, `micro.home` in the installed `EDIT`, `MICROHOME=` compiled
> into the object, and **`-backup off` gone from it**.
>
> ***THE SUITE: 30 of 31 steps exited 0 — 12 unelevated (ALL) + 18 of 19
> elevated. 971 `PASS`, 3 `[FAIL]`, 0 `[SKIP]`***, counted with the UTF-16
> decode and both controls (§6): the 19 elevated logs contributed 505 `PASS`,
> and the known-failing `b43` control still shows its 8 `[FAIL]`, so the zero
> `[SKIP]` is a measurement.
>
> - ***`verify-osusers` PASSES IN-SUITE*** — PRE_RELEASE 30's fix works where it
>   stopped the previous run dead. The unelevated half is 12 of 12.
> - **`verify-apiadmin` exit 1, 21/23** — the known stale control, PRE_RELEASE
>   31. **The headline questions all PASSED**: the API session cannot open or
>   write `$cred` and cannot run `OS.EXECUTE`.
> - **`verify-sshonly` carries 2 `[FAIL]` yet exited 0** — non-decisive rows,
>   and **environmental: PRE_RELEASE 32**. `b48` was spent twice, so Windows
>   made duplicate profiles and ssh key auth broke. *(The instruction to re-run
>   with `b48` was mine and was wrong — the prefix rule is in this box.)*
>
> ***NEXT RUN USES `b49`, AND RUN `cleanup-devlitter.ps1` FIRST*** — 53 stale
> `sd*` `ProfileList` entries have accumulated since `b44`.
>
> ***WHY `verify-apiadmin` FAILS, TRACED AND NOT GUESSED.*** Its *control*
> expects an elevated session `LOGTO`'d into a PROGRAMMER account to lose
> `OS.EXECUTE`. `CPROC:2713` **does** clear `USR_ADMIN` (`op_kernel.c:416`), but
> `os_permitted()` (`op_sh.c:167`) then keys `os.users` on `process.username` —
> `don` — whom **PRE_RELEASE 2 listed**. The gate says yes on the *person*,
> exactly as that feature's changelog says it should. **Product is per design;
> the control was written before `don` had a record.** The rewrite needs the
> owner to frame what it now proves. Not touched.
>
> ***THE THREE PRODUCT FIXES, ALL NOW ON THIS INSTALL.***
>
> 1. **PRE_RELEASE 21** — ***DONE.*** `verify-tiers` PASSED in `b48`.
> 2. **PRE_RELEASE 23** — ***DONE, AND THE DOCS ARE CORRECTED TOO.*** The owner
>    ran `term default` then `term`: **120 x 36**, where it was 20 x 24.
>    `term default` prints nothing, which is what that arm does and is not a
>    defect. The three pages that said the verb does not restore it —
>    *SD TCL - The Terminal and the Session*, tester `13` and `02` — are fixed
>    in `SDCoreWindowsDocs` `c41d999`, 27 Aug 2026 (sixty-ninth session).
> 3. **PRE_RELEASE 29** — ***DONE.*** Witnessed on the 19:37:47 install: three
>    runs, save and no-save, no message.
>
> ***NO CONSOLE CHECK IS OUTSTANDING ON THE EDITORS.*** The `micro` run closed
> on 27 Aug; `edit bp ZZMARKS` unelevated was run by the owner in the
> sixty-ninth session — **no problems**. Both editors are witnessed working on
> the 19:37:47 install. The fixture is in `don`'s BP; it was written at sha
> `1D65F19475F3CA5DCC5D594897F6B9CB` and a `micro` save has rewritten it since
> (`dos` line endings, 908 → 927, benign — SD's reader normalises them).
>
> ## ***2. THE `sd -cleanup` DEBT IS CLEARED — the 17:25:59 cycle wiped both trees.***
>
> It was owed on the *previous* install: two piped batches had hung and been
> killed (Users 12 and 19 stale on 27 Aug), User 19 leaving an `RU` lock on
> `zzlock31` in `don`'s `voc`. The fresh install removed all of it. **Kept
> because the cause recurs:**
>
> - ***`clearinput` in a piped session discards the unread script*** — including
>   a trailing `off` — so the batch hangs. It is now on SD TCL page 29. Scanning
>   a program for `input`/`keyin` is not enough; the question is *does it touch
>   the input stream*. `delete.file` needs `force`, not just `no.query`
>   (PRE_RELEASE 26), which is what hung one of the two.
> - ***`sd -cleanup` never gives back a task lock*** (PRE_RELEASE 24,
>   `clopts.c:300` tests the cleaner's own user number). Neither dead session
>   held one; if a future one does, `unlock tasklock` *n* elevated is the way
>   out.
>
> ## ***3. THE TIER WORK IS MEASURED AND WORKS. THE THREE FIXTURES ARE GONE.***
>
> ***CORRECTED 27 Aug 2026, SIXTY-NINTH SESSION. THIS TABLE SAID THEY WERE
> STILL THERE AND THEY ARE NOT.*** They were made against the **18:58:55**
> install and the **19:37:47** cycle wiped both trees — the same cycle whose
> destruction of the `ZZMARKS` fixture item 1 records and which was rebuilt.
> Nobody re-checked the accounts.
>
> **Measured on the 19:37:47 install rather than argued:** `sdsys/accounts`
> holds **`don` and `sdsys` and nothing else**, `user_accounts` holds only
> `don`, and `group_accounts` is **empty**.
>
> ***THE REFUSAL THAT FOUND IT LOOKS LIKE THE WRONG ONE, AND THAT IS BY
> DESIGN.*** `logto b48tier` from an elevated SDSYS session answered *"User not
> allowed in requested account"*, which reads as a failed group test. It is not:
> `CPROC:2639` prints **the same message** when the account is absent from the
> register, deliberately, so the register cannot be probed for which names
> exist. **A refusal that cannot distinguish the two cases cannot be read as
> either one** — the register is what settles it.
>
> ***THE WINDOWS SIDE OUTLIVED THE SD SIDE***, which a cycle does not touch:
> local user **`b48adm`** and groups **`sdg_b48tier`**, **`sdg_b48susp`**,
> **`sdu_b48adm`** are all still on this host. So rebuilding `b48adm` under the
> same name walks straight into PRE_RELEASE 32. ***Run `cleanup-devlitter.ps1`
> before rebuilding anything***, which the 53 stale `ProfileList` entries
> already wanted.
>
> Full detail below in "THE TIER CHANGE AND SUSPENDED ARE MEASURED AND WORK".
> The short form: `modify.account` moves an account between STANDARD,
> PROGRAMMER, ADMINISTRATOR and SUSPENDED in either direction, the VOC delta
> reported the predicted **42** and **21** every time, and the Windows side was
> diffed from outside SD with `don` as an unchanged control. **None of that is
> in doubt; only the fixtures are gone.**
>
> | account | what it was | what it was for |
> |---|---|---|
> | `b48tier` | PROGRAMMER, group | the **"left alone"** test, item 5.1 |
> | `b48susp` | ***SUSPENDED***, group | the unelevated LOGTO-door fixture |
> | `b48adm` | PROGRAMMER, user | the ssh and API doors, item 5.2 |
>
> **Rebuilding them is scriptable except for one:** `create.account group` does
> not prompt (`CREATEA:517`), `create.account user` prompts for a password and
> `no.query` does not suppress it — so `b48adm` needs a person. And
> **`delete.account` prompts unconditionally** (`DELACC:242`, no `no.query`), so
> never tear them down from a pipe.
>
> ## ***4. THE THREE FIXES ARE ALL DONE AND MEASURED. WHAT IS LEFT IS A DECISION AND TWO COMMITS ELSEWHERE.***
>
> ***OPEN, AND NONE OF IT NEEDS A CYCLE:***
>
> | | |
> |---|---|
> | **PRE_RELEASE 31** | **Yours.** `verify-apiadmin`'s control expects an elevated `LOGTO`'d session to lose `OS.EXECUTE`; `os_permitted()` keys the list on the *person* (`don`), whom PRE_RELEASE 2 listed, so the product is per design and the **control** is stale. Say what it should now prove and it can be rewritten — `$neverShipped`, no cycle |
> | **PRE_RELEASE 32** | ***WRITTEN, AND IT IS THE ONE THING HERE THAT DOES NEED A CYCLE.*** `DELETE_USER` now removes the `ProfileList` entry in its own right; the BASIC is **uncompiled**. **53 stale entries are still on this host** — `cleanup-devlitter.ps1` before the next suite run, and before rebuilding any `b48` fixture |
> | **PRE_RELEASE 34** | **Yours.** `release.ps1` cannot complete on `Technical`: `checklinks.py` rightly refuses a zero-link set and, two pages in, that set still has no honest cross-reference. Either the tool learns to say *this set has no links* or `release.ps1` passes a zero-link set out loud. ***Not to be settled by adding a link*** |
> | **`b49`** | the next suite number. `b48` is spent twice over |
>
> ***DONE THIS SESSION, KEPT FOR THE RECORD:***
>
> | | |
> |---|---|
> | **PRE_RELEASE 21** | the unreachable inner `if old.tier # 'SUSPENDED'` at the field-6 write in `tier.set` is **deleted**; `MODIFYA` banner + equality-guard comment + `SYSCOM/KEYS.H` now say the equality guard is what keeps field 6 write-once. Behaviour unchanged — **`verify-tiers` PASSED in the 27 Aug `b48`, regression check clean.** DONE |
> | **PRE_RELEASE 23 / UPSTREAM 24** | `TERM`'s `KW$DEFAULT` arm now sets `DEFAULT.WIDTH` / `DEFAULT.DEPTH`, not `MIN.WIDTH` and hard-coded 24; the `sdterm` depth-25 case went too. ***MEASURED 27 Aug: `term` reports 120 x 36.*** **DONE.** Left: three docs pages in `SDCoreWindowsDocs` still describe the old behaviour |
> | **PRE_RELEASE 29** | ***DONE, install 19:37:47.*** `MICRO_CONFIG_HOME` is a per-user `~/.micro` (`[Environment]::GetFolderPath`, falling back to local application data then TEMP) via the new shipped `gplbld/micro-home.ps1`; `EDIT`'s `micro.home` reads its `MICROHOME=` line before the working copy is written; the dead `-backup off` and `editor.args` are gone; `stage.py` ships the script and its wrong comment is corrected. **Three runs by the owner, save and no-save, no message** |
>
> ## ***5. WHAT IS STILL NOT MEASURED. 1 AND 2 NEED THEIR FIXTURES REBUILT FIRST.***
>
> ***5.1 AND 5.2 CANNOT BE RUN AS WRITTEN — the accounts they name were
> destroyed by the 19:37:47 cycle, item 3.*** They are written below as they
> stand because the *procedure* is right; only the accounts are missing.
> **Rebuild after the next install, not on this one**, so a cycle does not throw
> them away a second time, and run `cleanup-devlitter.ps1` first — the Windows
> halves of all three survived and a same-name rebuild meets PRE_RELEASE 32.
>
> 1. ***THE "LEFT ALONE" COUNT — DONE, 27 Aug 2026, install 22:52:21. IT FIRED
>    FOR THE FIRST TIME AND THE GUARD HOLDS.*** `b48tier` PROGRAMMER (42
>    added), `ed voc basic` with a fourth field, then
>    `modify.account b48tier standard`: ***`VOC: 0 records added, 41 removed,
>    1 left alone`.*** **And the count was not taken as the answer** — from
>    inside the account, `ct voc basic` returns **four lines** with the edit
>    intact and `ct voc micro` returns **`Record 'micro' not found`**. One kept,
>    one gone; `basic` alone would have been consistent with a downgrade that
>    deleted nothing. Comparison is whole-record equality, `MODIFYA:1144`.
> 2. ***THE ssh DOOR (`LOGIN`) IS DONE — 27 Aug 2026, install 22:52:21.***
>    `ssh b48adm@localhost` suspended: password accepted, **banner shown**, then
>    ***`Account B48ADM is suspended`*** and `Connection terminated`. Restored
>    with `modify.account b48adm programmer both`, the same command **admitted**
>    him. ***The banner is the control*** — it proves authentication succeeded
>    and the refusal came from `LOGIN`'s tier check, not from ssh. **Refusing
>    after authentication is the right order**: checking first would tell anyone
>    who can type a name which accounts exist and which are suspended.
>    ***THE API DOOR (`APISRVR:507`) IS STILL NOT REACHED***, and it cannot be
>    tested the same way: it refuses with `sysmsg(10003)`, **the same text as
>    "no such account" and "not granted"**, deliberately, so the API does not
>    enumerate the register. **Only a controlled pair on one account proves it**
>    — connect unsuspended, suspend, connect again, restore. **The suite does
>    not cover suspension at all**: neither `verify-tiers.ps1` nor
>    `verify-tierapi.ps1` mentions it, so `b49` will not test what was done by
>    hand here.
> 3. ***BOTH EDITORS ARE DONE AND ITEM 5.3 IS CLOSED — 27 Aug, install
>    19:37:47.*** Three runs of `micro bp ZZMARKS` unelevated, save and no-save:
>    **it draws, it highlights, it saves with no message, `$hold` is empty
>    afterwards** (so `EDIT` does clean up, which its history block claimed and
>    nobody had watched), and **the mark round trip survives a real save** — 19
>    fields, 907 chars, VM 6 / SM 1 / TM 3, no stray CR. ***AND `edit` —
>    Microsoft Edit — WAS RETRIED UNELEVATED ON THE SAME INSTALL, sixty-ninth
>    session: the owner ran `edit bp ZZMARKS` and reported no problems.*** It
>    sets no `MICRO_CONFIG_HOME`, which is why it was expected to be unaffected
>    — that is now measured rather than reasoned. **Nothing is left on 5.3.**
> 4. **`tools\sdprobe.ps1 -Source tools\probes\p25-holdtrip.b`**, docs repo —
>    15 cases, compiled clean 27 Aug, **never run**.
> 5. **Then `verify-tierchange.ps1` can be written** — the behaviour is known
>    now, so it can be built against a live install instead of guessed at.
>    PRE_RELEASE 19 lists what it must cover.
>
> ### THE DOCUMENTATION STATE
>
> ***BOTH REFERENCES ARE COMPLETE. FOUR SETS NOW, NOT THREE.***
>
> | | |
> |---|---|
> | `Testing/` | 15 pages, unchanged |
> | `User/` | 33. SD BASIC `01`-`18`, SD TCL `19`-`31`, cards at `94` and `95` |
> | `Administrator/` | **new** — `01` accounts and security, `02` sessions and locks, `03` operating system access |
> | `Technical/` | `01` restricted commands, `02` the installed scripts |
>
> `docmap` **411 of 411**, `tclmap` **144 of 144**, `checklinks` 185/0 on `User`
> and 6/0 on `Administrator`, HTML and PDF current for both.
>
> ***THE ADMINISTRATOR SET IS A SEPARATE DELIVERABLE SO IT CAN BE WITHHELD***
> — owner's ruling. **Sets never link to each other**, and `checklinks`
> enforces that for free because it resolves each set's links against that
> set's own `html` directory. Verified zero cross-links each way. Name a page
> in another set in words, never as a link.
>
> ***THE SYNTAX CARDS LIVE AT `94` ONWARDS*** — owner's ruling, so that adding
> another card never renumbers a subject page. `94` SD BASIC, `95` SD TCL.
>
> ***THE "17 LEFT" IN THE LAST HANDOFF WAS SHORT BY SEVEN, AND THE FIX IS A
> TOOL, NOT A CORRECTION.*** Seven verbs were counted as covered and were on no
> page — `listu` inside a warning, `lock` inside the word "unlock",
> `create.account` inside a keyword table on the editor page — because the
> count was answering *does this string occur* and the question is *is this
> verb explained here*. **`tools\tclmap.py` now asks the second one**: it
> requires evidence on the page, the verb backticked or opening a line inside a
> fenced syntax block, and prose does not count. It found seven problems on its
> first run and `mktclsyntax.py`'s completeness gate found more.
>
> **The tester set carries the tier change** (six pages) **and the 120 × 36
> default** (pages 02 and 13). `06` also gained the four `os.users` keywords,
> which had never been in the tester set at all.
>
> ***THREE TOOL FACTS LEARNT THE HARD WAY THIS SESSION:***
>
> - **`sdtcl.ps1` CANNOT DRIVE `MODIFY.ACCOUNT`.** It opens with `LOGTO don`,
>   and `CPROC:2713` drops `K$ADMINISTRATOR` on any `logto` whose target is not
>   SDSYS. Type those at an elevated `sd` prompt, or `logto sdsys` and stay.
> - **The PDF step is separate and gets forgotten.** Pages 19–27 shipped with no
>   PDF at all until the owner noticed. **Check markdown against PDF, never HTML
>   against PDF** — re-rendering touches every HTML mtime and reports the whole
>   set as stale. The one-liner is in the docs `README.md`.
> - **`CREATE.ACCOUNT USER` prompts for a password** and `NO.QUERY` does not
>   suppress it. A group account does not (`CREATEA:517`), which is what made
>   the tier round trip scriptable.
>
> ### WHAT CHANGED AND WHY — SIXTY-FIFTH SESSION, AND IT IS NOW INSTALLED
>
> *(Kept because the cycle of 27 Aug 12:06 is what installed it, and neither
> screen editor has been run since. Nothing below is outstanding work.)*
>
> ***`micro` REFUSED A SOURCE RECORD, AND `gpl.bp/EDIT` WAS THE ONLY SOURCE
> RECORD IN THE SHIPPED TREE ITS OWN GUARD COULD REFUSE.*** His ruling with it:
> *"the whole purpose of these editors is primarily to edit source code without
> having to use ED... the conversion of field, value and subvalue marks needs to
> be handled seamlessly, just like CRLF or LF."*
>
> **The round-trip guard was doing what it was written to do** — convert `@vm`
> and `@sm` to tokens, convert back, refuse anything that came back different.
> Three kinds of text tripped it: a literal `~~`, a literal `` ~` ``, or a `~`
> immediately before a mark. **`EDIT` carries the token strings as constants.**
> Measured across `sdsys` and `user_accounts`: the only other hits are `gcat`
> and `gpl.bp.out` object records, which nobody edits.
>
> ***THE FIX IS AN ESCAPE CHARACTER, AND IT IS CONDITIONAL ON PURPOSE.*** `~`
> now escapes; a tilde is written `~-` **only where the next character would
> make the pair look like a token** — another `~`, a backtick, a `-`, `@vm` or
> `@sm`. Everywhere else it is left alone, so `a~b` is still `a~b` and ordinary
> source reads normally. **Escaping every tilde would have been simpler and
> would not have been seamless.** `escape.tildes` in `EDIT`; the decode is three
> `change()` calls whose **order is load-bearing in both directions** and the
> code says why.
>
> ***PROVED BEFORE THE CYCLE, NOT AFTER.***
> `gplbld/test-edittokens-units.py` runs the same algorithm over **every string
> up to six characters** built from `~`, `` ` ``, `-`, `@vm`, `@sm` and one
> ordinary letter — **55,987, none lossy** — and over **all 197 shipped
> `gpl.bp` records, 17 of them containing a tilde, none lossy**. It asserts the
> corpus contains tildes: a lossless answer over records with no tilde in them
> would be true and would prove nothing.
>
> ***PRE_RELEASE ITEM 1 WENT IN THE SAME EDIT*** — the malformed refusal he saw
> again in the same paste. Fixed at `end.program`, the **one** print site, by
> splitting `error.text` on `char(10)` and writing one `crt` per line, rather
> than at the eight places that build the text. **Neither fix is verified: both
> are compiled BASIC and want the cycle above.**
>
> ***AND HE ADDED THE TEXT MARK HIMSELF THE SAME DAY, WITH A RULE FOR RUNS.***
> `~!` is a text mark, and **consecutive marks are separated by a comma** —
> *"text mark, text mark, value mark would be `~!,~!,~~`"*. That closed
> pre-release item 18, which was open for about an hour: the old guard never
> detected `@tm` either, so **the changelog's claim that text marks were
> "covered by that same refusal" was never true** and is corrected.
>
> ***HIS FIRST PROPOSAL WAS `` `~ `` AND HE WITHDREW IT HIMSELF, WHICH IS THE
> DESIGN DECISION WORTH KEEPING.*** He asked whether a token led by a backtick
> was a problem *"as it changes the pattern where every mark conversion starts
> with a ~"*. It is, and not cosmetically: it makes the **backtick** a second
> escape-introducing character needing its own escape, and `` ~` `` and
> `` `~ `` are anagrams, so a run of marks comes out as ``~``~`` and only a
> strict left-to-right scanner can read it. With `~!` a backtick is an ordinary
> character again.
>
> **A LITERAL COMMA BETWEEN TWO MARKS IS `~,`, AND THAT ONE IS FORCED** —
> `~~,~~` already means two value marks, so a real comma there has to be
> escaped. It is the only token not in his specification.
>
> ***AND THE DECODE STOPPED BEING `change()` CALLS.*** A run separator is a
> token that exists only by virtue of **where it sits**, and `change()` rewrites
> the whole string with no notion of where it is. `marks.out` and `marks.back`
> are left-to-right scans now. **Proved exhaustively to length 6 in the routine
> test and once to length 7 — 5,380,840 strings, none lost.**
>
> ### AND AN ADMINISTRATOR NO LONGER ELEVATES TO REACH THE OPERATING SYSTEM
>
> Owner, 27 Aug 2026: administrators are to *"have access to os.execute, ssh
> and api by default without escalating"*. **Pre-release item 2, closed.**
>
> ***TWO OF THE THREE ALREADY HELD, AND IT WAS RE-MEASURED RATHER THAN
> QUOTED.*** `Get-LocalGroupMember` on this install, 27 Aug: `don` is in
> **both `sdssh` and `sdapi`**. `CREATEA` has given an ADMINISTRATOR both
> routes since 21 Aug and no keyword can take either away.
>
> **`OS.EXECUTE` was the one that did not**, and `os.users` held **0 records**
> on a fresh install. Both gates that read that list — `CPROC`'s `sh` gate on
> field 1 and `op_sh.c`'s `os_permitted()` on field 2, which is also what
> `EDIT` reads — fall back to *elevation*, and an unelevated administrator is
> an ordinary user by design. That is the whole of why he met *"edit is not
> available to don"*.
>
> **One place: `CREATEA`'s new `grant.os.access`.** An ADMINISTRATOR-tier
> **USER** account is written into `os.users` as it is created — ADOPT
> included — with **both** fields `yes`. `DELACC` removes it again, but only
> where SD is deleting the Windows login itself.
>
> ***AND IT GAINED KEYWORDS THE SAME DAY:*** `sh-on` and `os-on` on
> `CREATE.ACCOUNT`, `sh-on` / `sh-off` / `os-on` / `os-off` on
> `MODIFY.ACCOUNT`. **Four switches over two fields**, not four names for one
> state as `SSH`/`API`/`BOTH`/`NONE` are, so `sh-off` leaves `OS.EXECUTE`
> alone. `MODIFYA`'s new `os.set`.
>
> **The hyphen is his and it parses** — `PARSER`'s simple-token arm splits at a
> space, a comma, a bracket or a quote and at nothing else, so `os-on` is one
> token with `keyword = -1`. *(He settled it mid-task: his first message mixed
> `OS-ON` with `sh.on`, and he chose the hyphen for all four.)*
>
> ***`os.set` DOES NOT REFUSE AN ADMINISTRATOR — AND THE OWNER HAS SINCE RULED
> THAT IT MUST.*** The reasoning committed with it was that ssh and the API are
> a **rule** while operating-system access is a **default**. **He overturned
> that the same afternoon**: *"administrators have full access, there should be
> no way to turn it off."* See the two rulings at the top of this box; **the
> code, both programs' headers and page 26 all still argue the old way.**
>
> ***THE 26 Aug RULING HAD A SECOND HALF AND IT WAS DELIBERATELY NOT DONE:***
> teaching `EDIT`'s `check.permitted` the ADMINISTRATOR tier as well. One list
> already answers *"may this person reach the operating system"*, and a tier
> test beside it makes the answer depend on two things that can disagree —
> `os.users` is keyed by **person**, a tier belongs to an **account**. **The
> cost is stated rather than hidden**: an administrator whose record is deleted
> or set to `no` IS refused, instead of the tier overriding. That is a
> narrowing of his earlier ruling and he has been told so.
>
> **Both fields, not only field 2** — field 1 is `sh` and `!`, field 2 is
> `OS.EXECUTE` and the editors, and granting one without the other leaves an
> administrator able to run `os.execute` from BASIC and refused at the prompt.
> **That half is a judgement call**: he named `os.execute`, not `sh`.
>
> ## ***BOTH RULINGS ARE BUILT, AND SO IS A FOURTH TIER HE ADDED THE NEXT DAY. NONE OF IT HAS COMPILED.***
>
> Sixty-sixth session.  He opened it by naming the outstanding
> `create.account`/`modify.account` work and adding **SUSPENDED**, *"a fourth
> trust level ... so that an account can be temporarily denied access"*.
>
> ***THE TREE OWED A CYCLE BEFORE ANY OF THIS AND NOW OWES A BIGGER ONE.***
> `gpl.bp/EDIT` was already uncompiled; **`MODIFYA`, `CREATEA`, `LOGIN`,
> `CPROC`, `APISRVR` and `SYSCOM/KEYS.H` have all changed since.** `sd.exe`
> has NOT moved — it is still a cycle and not a rebuild. **Nothing below has
> been compiled, let alone run.** *(Historic: that was `b48`, which has since run.)*
>
> ### 1. AN ADMINISTRATOR'S ACCESS CANNOT BE TURNED OFF — BUILT
>
> `MODIFYA`'s `os.set` carries `route.set`'s `S-1-5-32-544` guard, by SID, with
> its own message **10106** (10083 says *"always has both ssh and the API"*,
> which is the wrong text for `os-off`). **Both directions**, as `route.set`
> does. The three places that argued the old way are rewritten: both program
> headers, the changelog entry, and page 26.
>
> **The cost is stated at `os.set` rather than hidden**: an administrator
> ADOPTed over a Windows user whose `os.users` record already said `no` keeps
> it — `grant.os.access` leaves an existing record alone (10103) — and no verb
> can now change it. `ed os.users <name>` from SDSYS is the way out.
>
> ### 2. THE TIER IS SETTABLE, AND SUSPENDED IS THE FOURTH — BUILT
>
> `MODIFY.ACCOUNT <account> STANDARD | PROGRAMMER | ADMINISTRATOR | SUSPENDED`,
> any direction, no intermediate step. **`tier.set` in `MODIFYA`** plus
> `voc.delta` and seven small routines under it.
>
> ***HIS ANSWERS TO THE FIVE QUESTIONS, WHICH ARE RULINGS AND NOT DEDUCTIONS:***
>
> | question | his answer |
> |---|---|
> | where SUSPENDED lives | **field 5**, a fourth value of `ACC$TIER`; the tier it displaced goes to **field 6, `ACC$PRIOR.TIER`** |
> | what a suspension stops | **SD refuses at every door**; nothing is withdrawn on Windows |
> | when the VOC changes | **at once**, not at the next login |
> | what leaves with ADMINISTRATOR | Windows `Administrators` **and** the `os.users` record, automatically |
> | ssh and the API on a downgrade | **the caller names them** — `modify.account don programmer both` — refused with 10111 otherwise |
> | a `resume` keyword | **no** — coming back names the destination tier |
>
> ***HIS OWN QUESTION IS WHAT DECIDED THE SHAPE***: *"does it have to be
> resumed prior to each change or can they just happen naturally"*. No
> intermediate resume, ever. **Field 6 is written ONLY on the transition INTO
> SUSPENDED** — the equality guard at the top of `tier.set` is what enforces
> that (a second suspend returns there), so suspending twice cannot store
> `SUSPENDED` as the prior tier — and it is cleared by any move to a named
> tier. *(The write-once explanation was corrected 27 Aug — see "A CLAIM OF THE
> BUILD SESSION'S IS WRONG" below; PRE_RELEASE 21.)*
>
> **THREE DOORS, AND THEY WERE FOUND BY READING RATHER THAN ASSUMED**:
> `LOGIN` (after the case statement, so both arms), `CPROC`'s
> `logto.authorised`, `APISRVR`'s `vb.account`. The API one **reuses 10003**
> like every other refusal there, so the API does not tell a caller which of
> the three reasons applied.
>
> ***AND `update.voc` HAD TO LEARN SUSPENDED OR A RELEASE UPDATE WOULD STRIP
> IT.*** `LOGIN:268`'s walk visits **every** account, suspended ones included,
> and `update.voc` reads anything not blank/PROGRAMMER/ADMINISTRATOR as *apply
> the standard omit list*. A suspended administrator would have come back
> holding a standard VOC. Fixed at both sites that set `update.voc.tier` from
> a record — the walk and `get.acc.tier`.
>
> **THE VOC IS A DELTA AND NOT A REBUILD, and that is forced.** `CREATEA`
> builds into an empty directory and *then* writes the account's file pointers;
> re-running it on a live account would copy NEWVOC over every `F` pointer.
> The three tiers nest, so the difference between any two is one or both of
> `TIER.OMIT.STANDARD` and `TIER.ADD.ADMINISTRATOR` — **read from NEWVOC, not
> reproduced**, so `voc.delta` holds the arithmetic and no tier data.
>
> ***A DOWNGRADE DELETES ONLY WHAT IT WOULD HAVE WRITTEN.*** Each id is rebuilt
> from the source file with `CREATEA`'s own transformation and compared with
> what the account's VOC holds; anything different is **counted and left**, and
> the count is printed (10113). Deleting by id alone would destroy a user's own
> work under a verb's name.
>
> ### TWO JUDGEMENT CALLS, MARKED AT THEIR SITES AND NOT HIS
>
> 1. **An elevated or internal session can still `LOGTO` a suspended account.**
>    The test sits *after* `logto.authorised`'s two privileged bypasses. He has
>    ruled twice that an administrator's access cannot be turned off, looking at
>    a suspended account is the ordinary reason to have one, and anyone elevated
>    can lift it anyway. **If that is wrong the fix is to move the block above
>    the internal test** — not to add a second one.
> 2. **Nobody may suspend `@logname`'s account or the one they are standing in**
>    (10112). The way back would be `sd -internal`, which is undocumented.
>
> ### WHAT THIS TOUCHED BESIDES THE VERBS
>
> - **`SYSCOM/KEYS.H`** — `ACC$PRIOR.TIER` 6, and `ACC$TIER`'s fourth value.
>   Field 6 is a clean first use; field 4 is the poisoned one.
> - **Messages 10106–10115**, ten of them. 10105 was the previous highest.
> - **`gplbld/FILES_DICTS/accounts.dic^TIER` and `^PRIOR.TIER`**, new, plus a
>   rewritten `^@`. ***`LIST ACCOUNTS` HAS NEVER SHOWN THE TIER*** — the
>   dictionary held `@ID`, `PATH`, `DESCR`, `GROUP` and nothing else, so field 5
>   has been invisible since 17 Aug. **The default listing is
>   `PATH DESCR TIER BY @ID` now**: `GROUP` came out because it is always
>   `sdu_`/`sdg_` plus the account name, and `PATH DESCR GROUP TIER` is 123
>   columns against a 120 default. `WRITE_INSTALL_DICTS` `SSELECT`s the
>   directory, so new files need no manifest entry.
> - **`MODIFYA` has a BCOMP init block at the top**, the same one and the same
>   reason `LOGIN` carries: `rank.out` is read in `voc.delta` and assigned in
>   `tier.rank` forty lines below it, and *"is not assigned a value"* fails the
>   whole bootstrap (`bootstrap.py:229`). `tier.close.template` exists only so
>   that every mention of `tvoctmpl.f` stands below its `openpath`.
>
> ### THE CYCLE RAN. WHAT IT PROVED, AND WHAT IT CANNOT
>
> **Cycle 27 Aug 2026, install `12:06:20`, `sd.exe` `DF77FD6D61DE5184`** —
> unmoved, as it should be for a BASIC-only change. `assert-current` **exit 0,
> run live**, 2969 files across 6 mirrored directories. **`b47`'s accounts went
> with the fresh install: the register holds `don` and `sdsys` and nothing
> else, so `b48` is clean.**
>
> ***IT COMPILES, AND THE CONTROL IS THE PREVIOUS CYCLE'S LOG.*** `MODIFYA`
> **0 error(s)**, `$MODIFYA added to global catalogue`; **189 compile units,
> every one 0 errors**; **zero `is not assigned a value` warnings**. The four
> benign `assigned but never used` warnings appear in *identical counts* in the
> 11:11 log, which predates the commit — so **this work added no warning**.
> `gcat` 125 and `gpl.bp.out` 184, unmoved: no program was added.
>
> **VERIFIED BY READING THE INSTALL, NOT THE RUN'S OUTPUT:**
>
> | | |
> |---|---|
> | messages `10106`–`10115` | all ten present in `C:\ProgramData\SD\sdsys\messages` |
> | `accounts.dic` | `TIER` (field 5, *Tier*, 13L) and `PRIOR.TIER` (field 6, *Was*, 13L) both present; `@` reads `PATH DESCR TIER BY @ID` |
> | ***both dictionary items RESOLVE*** | `list sd.accounts` prints a **`Tier`** column reading `ADMINISTRATOR` for `don`; `list sd.accounts tier prior.tier` prints **`Tier` and `Was`**. That heading has no other source, so it cannot appear on a failure path |
> | `ct sd.accounts don` | field 5 `ADMINISTRATOR`, **field 6 absent** — correct for an unsuspended account |
> | the compiled object | `gcat/$MODIFYA` carries `SUSPENDED` ×7 (HEAD~1 source: **0**), `S-1-5-32-544` ×3 — exactly `route.set`, `os.set`, `tier.set` — and both TIER list names |
> | ***START HERE item 1*** | `os.users/don` holds two `yes` lines. **Closed** |
> | ***START HERE item 3*** | **`sh dir` unelevated returns a real listing.** The recorded refusal wording — *"not permitted to use the operating system shell"* (10053) — is absent. **Closed** |
>
> ***NOTHING BEHAVIOURAL ABOUT THE TIER VERBS IS TESTED, AND THAT IS A HARD
> LIMIT AND NOT AN OMISSION.*** `MODIFY.ACCOUNT` is
> `kernel(K$ADMINISTRATOR,-1)`, seeded from `IsElevated()` at process start, so
> **an unelevated session cannot reach one line of `tier.set`** — it stops at
> 2001 before the parser. Still completely unexercised: **`voc.delta`**, the
> three suspension doors, the write-once rule on field 6, ruling 1's refusal.
>
> ***AND THE ROUND TRIP MUST NOT GO DOWN A PIPE.*** `CREATE.ACCOUNT USER`
> **prompts for a password** — mandatory since 21 Aug, and `NO.QUERY` does not
> suppress it, it covers the confirmation at `CREATEA:501`. A prompt in a piped
> session eats the following lines and waits for ever, and `sdtcl.ps1`'s own
> banner is explicit that the timeout path **costs the install**: the dead
> session keeps its user-table slot and recovery is `sd -cleanup` plus a
> service restart. **Type it at an interactive elevated SD session.**
>
> ### ***THE TIER CHANGE AND SUSPENDED ARE MEASURED AND WORK. 27 Aug 2026.***
>
> The owner ran the elevated half at his own terminal; the unelevated half was
> run by the agent. **Install 27 Aug 12:06:20, `sd.exe` `DF77FD6D61DE5184`,
> `assert-current` exit 0.** Accounts left behind: `b48tier` (PROGRAMMER, group),
> `b48susp` (**SUSPENDED**, group, *keep it — it is the unelevated door
> fixture*), `b48adm` (PROGRAMMER, user, password known to the owner).
>
> ***THE TWO NUMBERS ARE THE EVIDENCE, AND BOTH WERE PREDICTED FROM SOURCE
> BEFORE THE RUN, NOT READ OFF THE OUTPUT.*** `TIER.OMIT.STANDARD` holds **42**
> ids and `TIER.ADD.ADMINISTRATOR` **21**. Every `voc.delta` move reported
> exactly one of those or zero.
>
> | measured | result |
> |---|---|
> | ruling 1 | `modify.account don os-off` → **`don is an administrator and always reaches the operating system`** |
> | STANDARD → PROGRAMMER | **42 added** |
> | PROGRAMMER → SUSPENDED | field 5 `SUSPENDED`, **field 6 `PROGRAMMER`**, VOC 0/0/0 |
> | SUSPENDED → STANDARD | **42 removed**, field 6 cleared |
> | ***SUSPENDED → PROGRAMMER with field 6 = `STANDARD`*** | ***42 added.*** **THE ONE THE DESIGN RESTS ON**: a blank field 6 also ranks 2, so it would have given **0 added**. This is what separates "field 6 was read" from "field 6 defaulted" |
> | the downgrade refusal | bare `modify.account b48adm programmer` → **`Say what remote access B48ADM is to have`** |
> | ADMINISTRATOR → PROGRAMMER `ssh` | **21 removed**, `os.users` record removed, `may sign in over ssh, and may not use the API` |
>
> ***AND THE WINDOWS SIDE WAS DIFFED FROM OUTSIDE SD, BEFORE AND AFTER, WITH A
> CONTROL.*** SD's own message is a claim; this is the check of it.
> `os.users/b48adm` `yes`/`yes` → **gone**; Windows `Administrators` **MEMBER →
> removed**; `sdapi` **MEMBER → removed**; `sdssh` **MEMBER → MEMBER** (kept,
> which is what `ssh` asked for and is the half that would look identical if
> `route.apply` had done nothing); `sdusers` untouched. **Control: `don`'s
> `os.users` record and his `Administrators` and `sdapi` memberships are
> unchanged**, so the removals tracked the account acted on.
>
> ***THE LOGTO DOOR, MEASURED UNELEVATED AND IN A PAIR.*** `logto b48susp`
> (SUSPENDED) → **`Account B48SUSP is suspended`**; `logto b48tier` (STANDARD)
> → `User not allowed in requested account`; `who` reads `8 DON` after both, so
> neither move happened. **Two accounts differing only in tier, two different
> refusals** — either alone is consistent with a check that never ran.
>
> ### ***A CLAIM OF THE BUILD SESSION'S WAS WRONG — CORRECTED 27 Aug***
>
> ***THE WRITE-ONCE RULE NEVER FIRES.*** Four documents — `SYSCOM/KEYS.H`,
> `tier.set`'s banner, this box and HISTORY — said field 6 is safe because
> `MODIFYA` writes it *"only on the transition INTO SUSPENDED"*. The second
> `modify.account b48tier suspended` answered **`B48TIER is already SUSPENDED;
> nothing changed`**, which is the **equality guard** at the top of `tier.set`
> returning early. It never reached the field-6 write.
>
> **It is unreachable, not merely unexercised.** `old.tier` is upcased and
> trimmed and `want.tier` is one of four upper-case literals, so
> `want.tier = 'SUSPENDED'` at that point already implies
> `old.tier # 'SUSPENDED'`. **The behaviour is correct — field 6 IS preserved —
> but by a different guard than the one documented.**
>
> ***FIXED IN SOURCE 27 Aug (uncompiled), FOLDED INTO THE MICRO CYCLE.*** The
> unreachable inner `if old.tier # 'SUSPENDED'` at the field-6 write in
> `tier.set` is deleted; `MODIFYA`'s banner, the equality-guard comment and
> `SYSCOM/KEYS.H`'s note now say the equality guard is what makes field 6
> write-once. Went in with PRE_RELEASE 23 and 29 because the tree was already
> off `assert-current` for 29. `b48` now scores this.
>
> ### WHAT IS STILL NOT MEASURED
>
> 1. ***THE SUITE — DONE.*** `-Run b48` ran 27 Aug against the 18:58:55 install:
>    **30 of 31, 971 `PASS`, 3 `[FAIL]`, 0 `[SKIP]`.** See START HERE item 1.
> 2. ***THE "LEFT ALONE" COUNT — every run so far reported `0 left alone`, which
>    is a rule that has never been exercised, not a rule that passed.*** It needs
>    a VOC record edited by hand before a downgrade. `b48tier` is PROGRAMMER and
>    is the fixture: from an elevated session `logto b48tier` (elevation
>    bypasses the group test), change a record `TIER.OMIT.STANDARD` names — `ed
>    voc basic`, `I` with text, `FI` — then `logto sdsys` and
>    `modify.account b48tier standard`. **Expect `41 removed, 1 left alone`.**
> 3. ***THE ssh/CONSOLE DOOR (`LOGIN`) AND THE API DOOR (`APISRVR`).*** Neither
>    has been reached. `b48adm` is the fixture and the owner has its password:
>    suspend it, `ssh b48adm@localhost` must answer **`Account B48ADM is
>    suspended`**, then `modify.account b48adm programmer ssh` to restore. **Do
>    the unsuspended attempt too** — a refusal that would have happened anyway
>    proves nothing.
> 4. **`micro gpl.bp EDIT`** from an unelevated console; a console, not a pipe.
> 5. **`tools\sdprobe.ps1 -Source tools\probes\p25-holdtrip.b`**, docs repo, 15
>    cases, compiled clean 27 Aug, never run.
>
> **Then `verify-tierchange.ps1` can be written** — the behaviour is known now,
> so it can be built against a live install instead of guessed at.
> PRE_RELEASE_FIXES 19 carries what it must cover.
>
> ### THE TESTER SET IS UPDATED; THE `User` SET IS NOT
>
> **Six pages, docs commit `db1a3d7`, 15 rendered, `checklinks` 76 links 0
> broken.** `05` carries the fourth tier and the rewritten "Changing an account
> afterwards"; `08`, `09` and `12` say what a suspension is **not** — an SD
> control and not a Windows one. `00`'s index line changed with `05`'s subtitle.
>
> ***`06` GAINED THE FOUR `os.users` KEYWORDS, WHICH WERE NEVER IN THE TESTER
> SET AT ALL*** — a gap left by the 27 Aug work rather than by this one. That
> section documented only hand-editing with `ed` and never said an
> ADMINISTRATOR account gets both fields unasked. **The hand-edit route stays**,
> because it is the only way out of the case the keywords refuse.
>
> **The `User` set still has nothing on any of it.** Page `32`, *accounts and
> security*, is where it belongs and is unwritten; page `26` has the `os-off`
> refusal and that is all. The changelog covers it meanwhile.
>
> ### TWO SAFETY NOTES THAT STILL STAND
>
> 1. **Never `Stop-Process` an sd session on a tree you still want to measure.**
>    Recovery is `sd -cleanup` plus a service restart.
> 2. **`delete.account` prompts unconditionally** (`DELACC:242`, no `no.query`),
>    so do not tear the three fixtures down from a pipe — and do not tear
>    `b48susp` down at all until item 3 is done. The next fresh install removes
>    them, which is what happened to `b47`'s fifteen.
>
> ***AND `LOGTO` OUT OF SDSYS DROPS `K$ADMINISTRATOR` (`CPROC:2713`).*** Found
> the hard way is the alternative: `sdtcl.ps1` opens with `LOGTO don`, so **it
> cannot drive `MODIFY.ACCOUNT` at all**, elevated or not. Type those at an
> elevated `sd` prompt, or `logto sdsys` and stay there.
>
> ***THE `SD TCL` REFERENCE IS DONE BAR `33`: `19` TO `32` ARE ALL WRITTEN AND
> COVERAGE IS 144 OF 144.*** `30` processes and phantoms, `31` locks and `32`
> accounts and security were written 27 Aug 2026. It lives in the `User` set on
> the owner's ruling — numbering continues from 19, names are
> `NN-sd-tcl-<topic>.md`. `checklinks` **183 links, 0 broken** across 32 pages,
> HTML and PDF both rendered by `tools\release.ps1 -Set User -NoZip`.
>
> ***`phantom` AND `pdebug` ARE DESCRIBED FROM SOURCE AND WERE DELIBERATELY NOT
> RUN.*** A phantom child inherits the pipe a scripted session is fed down, so
> the job never completes even after the parent exits — HISTORY.md, 24 Aug
> 2026, two `sd.exe` left behind. `pdebug` polls `keyready()`/`keyin()`, so down
> a pipe it eats the commands that have not run yet. **Neither may be added to a
> probe or an `sdtcl` batch.** Page 30 says so on the page.
>
> ***PAGES 26 AND 27 DESCRIBE BEHAVIOUR THAT IS NOW INSTALLED (cycle
> 27 Aug 12:06:20) AND STILL UNWITNESSED — neither screen editor has been run
> since.*** Page 25's `ed` listings are all measured and stand; the two
> screen verbs are described from source, because they cannot be driven down a
> pipe at all. **Re-read 26 and 27 once the cycle lands.**
>
> **Their key tables ARE measured, from the editors themselves**: micro's from
> the default bindings and help text inside the executable SD installs (micro
> **2.0.15**), Microsoft Edit's from `draw_menubar.rs` at tag **v1.2.1**, which
> is the version on this machine. Neither was typed from memory.
>
> ***AND `ed` CAN BE DRIVEN DOWN A PIPE, WHICH IS HOW `25` WAS MEASURED.*** Six
> `sdtcl` runs, no hang. **The rule that made it safe: read every `input` site
> in `ED` before sending anything** — `FD`, `DELETE`, `SAVE`/`FI` to a
> *different* name, `LOAD`, `UNLOAD`, `ed` with no file or record name, and an
> unrecognised command all prompt. `I` **with text**, `FI` with no name, and `Q`
> on an unchanged record do not.
>
> **`sdtcl`'s echo guard warns on an editor session and is right to be ignored
> there** — the lines after `ed` are eaten by `ED`, not echoed by TCL, so the
> count is legitimately short. The transcript reaching `:OFF` is what says the
> run finished.
>
> | | |
> |---|---|
> | ✅ `19` | the command processor |
> | ✅ `20` | files and records |
> | ✅ `21` | the query processor |
> | ✅ `22` | select lists |
> | ✅ `23` | alternate key indexes |
> | ✅ `24` | programs and the catalogue |
> | ✅ `25` | `ed`, the line editor |
> | ✅ `26` | `edit`, the plain screen editor |
> | ✅ `27` | `micro`, the capable one |
> | ✅ `28` | printing and spooling |
> | ✅ `29` | the terminal and the session |
> | ✅ `30` | processes and phantoms |
> | ✅ `31` | locks |
> | ✅ `32` | accounts and security |
> | `33` | **syntax — generated, all 144 verbs** |
>
> ***THE EDITORS TOOK THREE PAGES AND EVERYTHING AFTER THEM MOVED UP BY TWO.***
> Owner, 27 Aug 2026: *"since editor documentation is long, perhaps three
> documents might be better, one each for ed, edit and micro"*. **The generated
> syntax card is `33` now, not `31`.** `26` carries the mechanics both screen
> editors share — the working copy, the marks, the two gates — and `27` links
> to it rather than repeating it.
>
> ***AND TWO THINGS THE FIRST VERSION SAID WERE WRONG, BOTH HIS CORRECTIONS.***
> It offered `ed` as *"the one that always works"* and said `edit` *"needs the
> editor installed"*. **SD's installer installs both editors**, machine-wide, so
> availability is not the difference between them. What is: `ed` runs INSIDE SD
> and needs neither a terminal nor `OS.EXECUTE`, which is why it is the one for
> a phantom, an API session or a script.
>
> ***THE PLAN IS CHECKED, NOT ASSERTED: every one of the 144 verbs is on exactly
> one page, verified in both directions.*** The roster is 144 and not 140
> because four records are a keyword **and** a verb — `break`, `count`,
> `display`, `off` — which `CPROC:1718` re-parses from field 3. **SD's own VOC
> dictionary agrees**: its I-type `DISPATCH` encodes the same rule, and
> `count voc with dispatch # ""` answers 144. `CA` 97, `IN` 45, `OS` 2.
>
> ***FOR `33`, THE SYNTAX COMES FROM EACH VERB'S OWN `START-DESCRIPTION`
> BLOCK*** — 166 of the 178 catalogued verb records have one. The 81 internal
> and OS verbs have no program to read, so they need a hand-kept shapes file the
> way `syntax-shapes.txt` serves the BASIC card.
>
> ***`18` AND `Technical/01` ARE GENERATED, NOT EDITED, AND THEY PARTITION THE
> ROSTER.*** `tools\mksyntax.py` writes both from `BCOMP`'s own tables and
> **refuses unless every name is on exactly one of them** — 372 + 75 = **447**.
> It lifts the argument count for 173 functions straight out of the compiler's
> dispatch table, which is positional against the name list and carries each
> name in a comment it checks against. **Edit `tools\syntax-shapes.txt` and
> regenerate; do not edit either page.**
>
> | | |
> |---|---|
> | `User\markdown\18-sd-basic-syntax.md` | 372 names an application may use, one alphabetical run, syntax only |
> | `Technical\markdown\01-sd-basic-restricted-commands.md` | 75 it may not — 36 restricted statements, 38 internal-only functions, and `errmsg` |
>
> ***ONE QUESTION IS OPEN AND IT IS THE OWNER'S: DOCUMENT 09.*** `09 Alternate
> Key Indexes` is **8 of 8 restricted commands** — `akclear`, `akdelete`,
> `akenable`, `akread`, `akrelease`, `akwrite`, `create.ak`, `delete.ak`, and
> nothing else. The ruling was about the syntax card, so **the page was left
> where it is** rather than moved unasked. If restricted commands belong in
> `Technical`, that whole page belongs there too. `13` and `16` carry a few
> each and are mixed; **`17` is fine** — the one name on it that is not
> restricted, `debug`, is what the page is about.
>
> **`docmap.py` was deliberately not changed** and now says why: it answers
> *"is every name explained somewhere in the `User` set"*, and it still is,
> because the pages that explain them have not moved. Move the names in
> `docmap` only if the pages move.
>
> **`checklinks` on `Technical` refuses today and is right to** — one page, no
> cross-references, so it finds no links at all. Run it there once there is a
> second page.
>
> ***`H.2` IS STILL OPEN AND WHAT IS LEFT IS NAMED.*** The `Technical` set has
> two pages of a set that wants more; questions **7** and **14** in
> `QUESTIONS-2026-08-26.md` are unanswered. *(The shipped-scripts gap was the
> third item here and closed on 27 Aug 2026 — `Technical/02`. The count was 26,
> not the 25 written here.)*
>
> ***DEFECTS FOUND WHILE DOCUMENTING NOW HAVE THEIR OWN LIST:
> [PRE_RELEASE_FIXES.md](PRE_RELEASE_FIXES.md), 28 ENTRIES.*** Read it before
> planning release work; this box does not repeat it.
>
> ***A DEFECT IN BOTH TREES GOES IN BOTH FILES.*** Owner's correction, 26 Aug
> 2026, replacing a "one defect, one file" rule that had stood for one session
> and hid three things. `UPSTREAM_FIXES.md` says *the `sdb64` maintainer should
> know*; `PRE_RELEASE_FIXES.md` says *we would ship this*. **Being fixed
> upstream is not being fixed here** — of the four found last session, #18 and
> #19 are now fixed in this tree and **#17 and #20 are not**, and nothing had
> recorded which was which.
>
> **#17 is still the one that matters** — silent partial data loss inside a
> construct whose entire purpose is that there is no such thing. It is
> pre-release item 11, verified live here: `txn_depth` is `++` at `txn.c:96`,
> `--` at `:592`, and `op_txncmt()` touches neither. ***Do not fix half of it.***
>
> **Three more went upstream this session** — #21 `QSELECT` loses the list
> number from its own message, #22 `DELETE.INDEX` will not match a lower-case
> index name where `LIST.INDEX` will, #23 `DELETE.FILE ... NO.QUERY` still
> prompts when part of the file is in the system account. All three are live
> here too, as pre-release items 13, 15 and 14.
>
> ***THE TOOLING MOVED OUT OF THE SESSION SCRATCHPAD ON PURPOSE, BECAUSE A
> SCRATCHPAD DOES NOT SURVIVE AN ACCOUNT CHANGE.*** Eight instruments are now
> in the docs repository's `tools\`, and every one has been run from there.
> **The probe sources are kept too, in `tools\probes\`, with a README saying
> which runner takes which** — a number with no way to reproduce it is a number
> the next session has to take on trust:
>
> | | |
> |---|---|
> | `tools\sdtcl.ps1` | ***the TCL half of the same idea***, and how the SD TCL pages are measured: run the command, quote what SD said. **Refuses a transcript with fewer command echoes than commands sent.** Defaults to a USER account - `LOGTO SDSYS` asks UAC when the session is not already elevated, so measuring in SDSYS puts a consent prompt in front of whoever is at the machine, once per run |
> | `tools\sdprobe.ps1` | ***how most measured values in the set were produced.*** Writes a BASIC probe into an account's BP, runs it down §6's `Invoke-SD` pipe, and **REFUSES a run that did not print its own START and END markers**. It has refused six real drafts |
> | `tools\sdprobe2.ps1` | ***TWO SESSIONS AT ONCE***, which is the only way any lock can be measured — every `RECORDLOCKED()` code above zero is the self-answer. **It refuses unless the two report different user numbers AND the contender names the holder**; a pair that ran one after the other prints exactly the numbers a reader expects from a working test |
> | `tools\sdcompile.ps1` | compile only. **Half of what a reference has to say is a refusal** — `errmsg`, the internal-only intrinsics, the restricted statements — and `sdprobe`'s guard requires `0 error(s)`, so it can only ever refuse those. `-ExpectErrors` refuses a probe that was meant to fail and compiled |
> | `tools\sddebug.ps1` | compiles with `DEBUGGING` and **drives the debugger from a script**. It works because `TERMINFO('sreg')` is empty on the `windows` terminal type, so `$DEBUG` takes its line-oriented path and a pipe can answer it. Refuses a run with no `>` prompt |
> | `tools\docmap.py` | assigns every name `BCOMP` accepts to exactly one document; exits non-zero on a gap. **411 of 411** today, across all seventeen |
> | `tools\linkup.py` | turns `*SD Basic - X*` into a link **only for pages that exist**, so `checklinks` stays meaningful |
> | `tools\probes\` | the sixteen probe sources, with a README mapping each to its runner |
>
> ***THE METHOD IS THE POINT, NOT THE PAGE COUNT.*** The roster comes from
> `BCOMP`'s own tables, never from `..\sdhelp`, and every example is compiled
> and run before it is written down. That has caught **eight** statements
> drafted as though they worked, three behaviours recorded nowhere else
> (`matbuild ... using`, `errmsg`, `on n goto` clamping), and — this session —
> **three upstream defects and one advice in an already-written page that was
> simply wrong** (page 07 told the reader to convert a POSIX path with
> `kernel(K$WINPATH, ...)`; an ordinary program cannot call `kernel()` at all).
> **Do not relax it to go faster; it is the only reason the set is worth
> anything.**
>
> ***AND TWO PATTERNS ARE WORTH REUSING RATHER THAN REDISCOVERING.***
> **Anything that can block goes AFTER the probe's END marker**, so the
> measurement is banked before the risk is taken — that is how
> `server.addr()`'s resolver hang and `config()`'s abort were both measured
> without losing the rest of the run. And **two contending sessions rendezvous
> through a file, never a timer**: a slow compile turns a staggered pair into a
> measurement of nothing that still prints numbers. When one session holds a
> **file** lock the rendezvous needs a *second* file, or each waits for a write
> the other cannot make.
>
> **Render with** `python tools\mkdoc.py --in User\markdown --out User\html`,
> then `powershell -File tools\mkpdf.ps1 -In User\html -Out User\pdf`, then
> `python tools\checklinks.py User\markdown User\html` — **110 links, 0
> broken** at handoff.
>
> ***THE THREE C FIXES ARE INSTALLED AND EACH WAS RE-MEASURED, 26 Aug 2026.***
> The cycle ran at 21:17:22 and `assert-current` is **exit 0**. Verified with
> the three probes this box used to name, each run through
> `tools\sdprobe.ps1`:
>
> | probe | reads | was |
> |---|---|---|
> | `p16-system.b` | `system(1010)=[Windows]` | `Linux` |
> | `p16c-config.b` | `config(NOSUCHKEY)=[] status=1004`, **`neither aborted`** | aborted the caller |
> | `p15-sockets.b` | `set.keepalive(0)=1`, **`keepalive.now=0`** | `1` / `1` |
>
> ***AND FIXING THEM MADE THREE PUBLISHED PAGES WRONG, WHICH IS THE COST THE
> SEPARATE DOCUMENTATION REPOSITORY WAS ACCEPTED WITH.*** Nothing fails when a
> page goes stale; a person has to notice. Corrected the same session:
> `16` said `system(1010)` answers `Linux` and warned readers off it, and said
> a nine-character `config()` name aborts the caller; `15` said keep-alive
> could not be turned off. **All three were true when written and were false
> the moment the fixes installed.**
>
> **So: after any C fix lands, grep the `User` set for what it claimed.** The
> pages most at risk are the ones whose value is a measured defect, because
> those are exactly the ones a fix invalidates.
>
> ---
>
> ***RUN `python sdb_ai/sd64/gplbld/check-stale-leads.py` BEFORE YOU ANSWER ANY
> "WHAT IS LEFT" QUESTION.*** One second, and it is the difference between the
> table and a guess.
>
> ***THIS BOX WAS PRUNED 26 Aug 2026 AND IT IS MEANT TO STAY THIS SIZE.*** It
> is headed *"IT IS SHORT"* and had reached a quarter of the file, because
> twelve sessions each added a handoff to the top and none removed the one
> below. **Add yours by replacing what it supersedes, not by stacking on it.**
>
> ---
>
> ### THE SUITE IS ONE COMMAND, AND `-Run` ALONE IS A TRAP
>
> From an **ordinary** terminal — two processes with the correct token each is
> the design — about four UAC prompts:
>
> ```
> C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\VerifyInstall1.ps1 -ThenElevated -Run b49
> ```
>
> ***`-Run` ON ITS OWN DOES NOTHING*** — it is *"ignored without
> `-ThenElevated`"*. Without that switch `VerifyInstall1` runs its 12 unelevated
> steps, prints **"every step exited 0"** and stops, which reads exactly like a
> finished suite and is **12 of 31**. ***`b46`, `b47` AND `b48` ARE SPENT — USE `b49`.*** `b48` went twice, which is what PRE_RELEASE 32 cost.
> A `-Run` prefix is spent once.
>
> ***AND THE SAME TRAP RUNS THE OTHER WAY, WHICH IS HOW `b46` GOT WRITTEN DOWN
> WRONG.*** The two halves print **different** summary lines and neither names
> the suite: `VerifyInstall1` prints *"every step exited 0"* with **no number**
> (12), and `VerifyInstall2` prints *"all 19 steps exited 0"* (19). Quoting the
> second on its own — which the 61st session did — records a green 31-step run
> as **"19 of 19"**, and the next reader cannot tell it from a run where the
> unelevated half never happened. **Write down both numbers, or write `31/31`.**
>
> **AND `Start-Process -Verb RunAs -Wait` DOES NOT SET `$LASTEXITCODE`** — use
> `-PassThru` and `.ExitCode`, or a failed `cycle.ps1` reads as success. One run
> exited **1** where `$LASTEXITCODE` read 0.
>
> ### ONE THING IS LEFT ON THE MACHINES AND IT IS NOT A TASK
>
> ***GONE, AND WITH IT THE ONLY MAC COLLISION — MEASURED 2 Sep 2026.***
> `sdStandalone-C1` is **no longer registered**, so the warning below has no
> partner left: `VBoxManage list vms` shows only `Beardog`, `Template` and
> `Test 3`-`Test 6`, and every one has a distinct MAC — `Template`
> `080027AECE7C`, `Beardog` `0800273AF379`, `Test 3` `080027C61086`, `Test 4`
> `0800271DABE7`, `Test 5` `08002734F731`, `Test 6` `080027C3E817`. ***SO ANY OF
> THEM MAY RUN AT THE SAME TIME, TEMPLATE INCLUDED.*** The clash was never a
> property of `Template`: `080027AECE7C` is `Template`'s **own** address, and
> `sdStandalone-C1` was cloned **keeping** it. A default VirtualBox clone
> regenerates the MAC, which is why `Test 3`-`Test 6` all differ — so a new
> clone does not reintroduce this unless somebody deliberately preserves MACs.
> *(Original note follows.)*
>
> Guest `sdStandalone-C1` is still registered, powered off, carrying the
> stand-alone install that closed H.5. ***It shares MAC `080027AECE7C` with
> `Windows 11 - Template` — never run both at once.*** `cleanup-devlitter.ps1`
> does not touch it (its `$VMName` is the older clone), so it goes by hand when
> nobody wants to look at that install again:
>
> ```
> VBoxManage unregistervm sdStandalone-C1 --delete
> ```
>
> ### FIVE STANDING INSTRUMENTS, ALL ON `$neverShipped`, ALL WITH CONTROLS
>
> Do not re-derive them.
>
> | | |
> |---|---|
> | `cleanup-devlitter.ps1` | users, `sdu_` groups, the profile sweep, the home directory, the VM. `-SelfTest` / `-List` / act. ***Needs a REBOOT between the accounts and the profiles*** — a loaded hive cannot be removed, and after a suite run every hive is loaded |
> | `check-stale-leads.py` | **three** phases: an entry whose opening status is contradicted later; the task table against the entries, both directions; and an entry that records a person SEEING something and later denying anyone has. `test-staleleads-units.py` is its control, **13 of 13** |
> | `check-client-sync.py` | the API client across the three trees. 12 checks, 0 failed. `--self-test` 6 of 6 |
> | `probe-sshremote.ps1` | the HOST half of the ssh remote-block test. `-SelfTest` 4 of 4 |
> | `verify-standalone.ps1` | runs **on a guest**, via `-Installer` + `-InstallerSha256` in place of `assert-current`. All four refusal paths exercised |
>
> `verify-upgrade.ps1` is the sixth and it is spent for now: ***do not re-run
> `-Snapshot`***, it would overwrite the pre-upgrade state with the post-upgrade
> one and destroy a measurement that took three sessions to score. The snapshot
> is at `C:\ProgramData\SD-verify\upgrade-snapshot.json`.
>
> ---
>
> ## THE HANDOFF ROWS — H.1 TO H.5
>
> Their conclusions are in the task table. These entries carry what is still
> worth following; the record of how each was reached is in HISTORY.md, entry
> ***"ARCHIVE 26 Aug 2026 — START HERE's closed record, sessions 49 to 60, in
> full"***.
>
> ### 1. DONE — THE MACHINE IS A FULL INSTALL AND THE WHOLE SUITE IS GREEN
>
> | | |
> |---|---|
> | install | **26 Aug 2026, 17:14:03**, a **FULL** install — `cycle-20260826-171313.log`, the cycle that built `$EDIT` |
> | the suite | **31/31 steps, every one exit 0** — **12** unelevated (`VerifyInstall1-20260826-171534.log`) + **19** elevated (`post-cycle-20260826-171706.txt`), run as `-ThenElevated -Run b46`. **991 `PASS`, 0 `[FAIL]`, 0 `[SKIP]`.** Both counters read, because two counters that cannot both be zero is the cheap null-case guard |
> | `sd.exe` | `8E6A6CF45AA6F20A` |
> | `gcat` / `gpl.bp.out` | **125 / 184** |
> | `assert-current` | **exit 0**, run live at the start of the sixty-second session — so every verifier will run |
>
> ***THE `-Run` TOKEN IS PROVEN TO HAVE REACHED THE ELEVATED HALF*** — the
> evidence is the account names its steps created, `sdacctb46`, `sdtiertb46`,
> `sdcatgb46`, `sdaclb46`, `sdrtb46` and the rest, in
> `post-cycle-20260826-171706.txt`. Not the switch having been typed.
>
> **Nothing since has changed anything that ships**, and that is measured
> rather than assumed: `assert-current` exits 0 on this tree today.
>
> ***WHAT THAT RUN DOES NOT COVER, AND EACH GAP WAS CLOSED SEPARATELY.*** The
> **upgrade path** is gated on `DataTreeUpgrade` and that was a first install,
> so none of it ran — see H.3. The suite has **no step that chooses the
> stand-alone install** (H.5) and **no step for VFS** (H.3a); both were checked
> directly on the installed tree instead.
>
> ***AND FAILURE-SHAPED LINES IN A GREEN RUN ARE THE MEASUREMENT, NOT A
> FAILURE.*** `verify-credacl` raises `TerminatingError(Get-Acl): "Attempted to
> perform an unauthorized operation."` — that IS its test, and the next line
> says *"Access is denied - which is the expected answer"*. `verify-osusers`
> prints *"Error 2 executing operating system command"* while scoring
> `elev_piped=refused`. `icacls` reports *"Failed processing 0 files"*, and
> `secure-account-dirs` *"0 failed"*. **Read them before reporting them.**
>
> ### 2. DOCUMENTATION — H.2 IS STILL OPEN. THE TESTER SET IS REVIEWED; THE OTHER TWO SETS ARE NOT WRITTEN
>
> **H.2 stays open**: the `User` set is two pages into seventeen, `Technical`
> is empty, and two review questions are unanswered. What follows is what is
> settled.
>
> ***THE `User` SET IS AN SD BASIC REFERENCE, AND THE MAP IS RULED.*** Owner,
> 26 Aug 2026: seventeen documents, **grouped by function**, each titled
> `SD Basic - <category>`. ***ALL SEVENTEEN ARE WRITTEN: `01` Program
> Structure, `02` Program Control, `03` Math Functions, `04` String Functions,
> `05` Dynamic Arrays, `06` Data Conversion, `07` File Handling, `08` Select
> Lists, `09` Alternate Key Indexes, `10` Sequential Files, `11` CSV Files,
> `12` Terminal Input and Output, `13` Printing, `14` Locks and Transactions,
> `15` Sockets, `16` System and Environment, `17` Debugging*** — all rendered
> to HTML **and PDF**, `docmap` **411 of 411**, `checklinks` **110 links, 0
> broken**. Numbers
> are one flat run for the whole `User` set, **no letter suffixes** — §6's
> hyphen-collation trap.
>
> ***`14` AND `15` NEEDED INSTRUMENTS THAT DID NOT EXIST, AND THE REASON IS
> WORTH KEEPING.*** A lock you hold yourself answers a different question from
> one somebody else holds — every `RECORDLOCKED()` code above zero is the
> self-answer — so `sdprobe2.ps1` runs **two sessions at once** and refuses a
> run in which they did not demonstrably contend. Sockets went the other way:
> `create.server.socket` calls `listen()`, so **one** session can be both ends
> on loopback, and the client waits in the backlog until the same session
> accepts it. `17` needed a third, `sddebug.ps1`, because the debugger is
> line-oriented on this port and can therefore be driven down a pipe.
>
> ***EVERY DOCUMENT NOW OPENS ON A GENERATED TITLE PAGE — OWNER, 26 Aug
> 2026.*** Name, subject, `Copyright © 2026 Donald Montaine`, the release it
> shipped with, and **CC BY-SA 4.0** with a three-paragraph summary and
> `https://creativecommons.org/licenses/by-sa/4.0/`. **It is built by
> `mkdoc.py`, not pasted into each file** — the Markdown supplies only `Title:`
> and `Subtitle:`. `mkdoc.py` **refuses to write a page** that renders without
> the title page, the copyright or the licence URL. ***THIS ALSO CHANGES THE
> `Testing` SET AT ITS NEXT RENDER***, which has not been re-rendered.
>
> ***THE PAGE BREAK WAS VERIFIED WITH A CONTROL, AND THE FIRST INSTRUMENT WAS
> WRONG.*** Comparing page counts on a real document gave 6 with the break and
> 6 without — the content rounded the same either way, so it proved nothing.
> The decisive test is a **one-paragraph document**: 2 pages with the break,
> **1 without**. Both halves were run.
>
> ***COVERAGE IS CHECKED, NOT ASSUMED***: `scratchpad\docmap.py` assigns every
> name `BCOMP` accepts to exactly one document and exits non-zero on a gap —
> **411 of 411 assigned**. Rebuild it in `gplbld` if the set is ever picked up
> on another machine.
>
> ***THE ROSTER COMES FROM `BCOMP`'s OWN TABLES, NOT FROM `..\sdhelp`.*** The
> same extraction `gplbld/mkbasicsyntax.py` uses gives **218 statements, 37
> reserved words, 176 intrinsics** — what this port's compiler actually
> accepts. Diffed against the historic by-type roster: **8 things the old docs
> describe are gone** (`rsd`, `stope`, `stopm`, `encrypt()`, `decrypt()`,
> `ttyget()`, `ttyset`, `connect.port()`) and **59 exist that the old roster
> never listed** — `sdencrypt()`, `sddecrypt()`, `checksum()`, `randomize`,
> `sysmsg()`, `vartype()`, the `ak*` family, the debug family, `printcsv`,
> `sendmail` among them. **Do not take a function list from the help tree.**
>
> ***WHAT MEASURING FOUND THAT NO DOCUMENT RECORDS, AND SOME OF IT IS
> DEFECTS.*** Each was reproduced on the 17:14:03 install.
>
> | | |
> |---|---|
> | ***`matbuild ... using` DOES NOT WORK*** | the keyword compiles as a **variable** and the program aborts with *"Unassigned variable USING"*. Tried in both cases. **`st.matbuild` is byte-identical to `../sdb64`'s, so it is upstream's defect, not ours.** The delimiter is always `@fm` |
> | ***`errmsg` IS IN `BCOMP`'s STATEMENT TABLE AND DOES NOT COMPILE*** | *"Unrecognised statement"*. Its opcode was removed 28 Jul 24 and the name was left behind. **Being in the table is not evidence a statement exists** — the roster needs compiling, not just reading |
> | ***`on n goto` CLAMPS, IT DOES NOT FALL THROUGH*** | with two labels, `on 0` and `on -1` both go to **label 1** and `on 3` goes to **label 2**. So there is no "none of the above", and a zero — what an empty variable evaluates to — silently runs the first branch |
> | ***`locate`'s SUBSCRIPT DEPTH CHOOSES THE LEVEL*** | `arr<f>` searches FIELDS, `arr<f,v>` searches VALUES. One subscript on a value list finds nothing and returns an insertion point, which reads like a working search. The statement form **requires** the brackets |
> | `div()` is not `/` | `div(7,2)` is **3**: the intrinsic compiles to `OP.QUOTIENT` (`BCOMP:476`), not to the `/` opcode of the same name |
> | `idiv()` changes rounding | truncates on two integers, **floors** if either is floating point: `idiv(-7,2)` is `-3`, `idiv(-7.0,2)` is `-4` |
> | `num('')` is **true** | the empty string passes the test people use as a validator |
> | `selectv` is not a dynamic array | `vartype()` **11**; `dcount()` on it fails *"Data cannot be converted to a string"*. Read it with `readnext ... from` |
> | the format qualifier has no keyword | `t '10R2'` works, `t fmt '10R2'` compiles `fmt` as a variable |
> | `getlist`/`savelist` need `then`/`else` | without one the error is *"Expected THEN or ELSE"* reported against the **next** statement |
> | `fileinfo` has no record count | key 6 is minimum modulus. Use `selectinfo(list, 3)` |
> | a trailing `@fm` becomes an id | `formlist` on three ids built with `id : @fm` produced **four** entries, the last empty |
> | ***AN INDEX TAKES THREE STEPS AND EACH REPORTS SUCCESS ALONE*** | `create.index` makes an **empty** index; an **already-open file variable never sees it** (`indices()` empty, `fileinfo(f,13)` 0) until close and reopen; `build.index` needs **exclusive access and your own session counts** — *"Cannot gain exclusive access to file"*, rc **3021**. Only after close, build, reopen did `selectindex` return ids |
> | `selectindex` returns two different things | with a value, the record **ids**; **without one, the distinct index VALUES**. Nothing says which |
> | `selectleft`/`selectright`/`setleft`/`setright` take no `then`/`else` | writing one is *"Unrecognised statement"*. They take `setting` and `to` |
> | `openseq`'s `then`/`else` is not success/failure | `then` = the file existed, `else` = it was **created** (or the open failed) |
> | `csvdq()` is a **de**-quoter | it splits one CSV line into field-mark separated fields. There is no matching function that quotes one |
> | `printer file` takes the unit after `on` | `printer file on 1 'F','R'`; the positional form is a compile error. `printer.setting` takes **three** arguments |
> | sequential writes are **CRLF** | measured byte for byte: `65 66 13 10 67 68 13 10` |
>
> ***AND WHAT DOCUMENTS 14 TO 17 ADDED, 26 Aug 2026.*** Same install. The three
> marked ***upstream*** are in `sdb64` unchanged and **none is fixed**.
>
> | | |
> |---|---|
> | ***inside a transaction, `write` and `delete` need the lock ALREADY HELD*** | `ER_NOLOCK` **3023**, and `messages/1407` renders it *"Error 3023 (o/s 0) writing record (Possible full disk?)"* — a lock error wearing a disk error's message. `op_dio3.c:770` and `:325`, `if (pcfg.must_lock \|\| txn_id)`. The same `write` succeeds outside a transaction |
> | ***reaching `end transaction` with no `commit` discards everything, silently*** | measured: the record still read its pre-transaction value. There is no implicit commit |
> | ***`system(1008)` never decrements on a commit*** — upstream | `txn_depth--` is only in `rollback()` (`txn.c:592`), and BCOMP compiles `commit` as a jump **past** `end transaction`. So the level is permanently wrong after the first committed transaction. **Test `system(1007)`**, which is 0 outside one |
> | ***a `commit` inside a NESTED transaction abandons the outer one*** — upstream | measured: the inner write landed, **the outer write was lost**, `system(1007)` read 0 after the inner commit. `op_txncmt` does not pop `txn_stack` |
> | `recordlocked()` sets `status()` to the **owner's user number** | measured across two sessions on all five refusal paths. It is the only way to find out who holds a record |
> | a plain `readu` waits **250 ms per retry** and does not time out | measured 252 ms, released by the other session. `op_lock.c:515`, `Sleep(250)` |
> | a `lock` with no `else` **retries for ever** | BCOMP generates `sleep 1` + jump back as the default `else` |
> | a **file** lock stops locking, not reading | measured: `readu ... locked` refused on every record, a plain `read` returned normally |
> | ***`read.socket`'s timeout is ignored unless the socket is blocking, and no socket starts blocking*** | measured: flags 0 with a 5000 ms timeout returned in **0 ms**; flag 1 waited 2025 ms. **The bug passes its own tests** — on loopback the data is already there |
> | a closed peer is **7013 or 1008**, depending which end closed | a loop guarded only on 7013 ran all 21 of its iterations |
> | `set.socket.mode` key 6 ignores its argument — ***FIXED 26 Aug 2026, uncycled*** | `set.socket.mode(s, 6, 0)` returned **1** and keep-alive read **1**. `op_skt.c` set `n = TRUE` unconditionally; the line is gone. UPSTREAM_FIXES #19 |
> | `server.addr('localhost')` is **`::1`** while `create.server.socket('127.0.0.1')` is IPv4 | and an unresolvable name **blocks in the OS resolver** — still not back after 45 s, with no way to bound it from BASIC |
> | ***`config()` names are case sensitive and at most 8 characters*** — the abort ***FIXED 26 Aug 2026, uncycled*** | wrong case is `''` + status 1004, and that stands. **Nine characters aborted the caller** with *"Data cannot be converted to a string"* because the early exit jumped over `result`'s initialisation; it now returns `''` + 1004 as well. UPSTREAM_FIXES #18 |
> | `env()` is case sensitive | `env('path')` is 0 characters where `env('PATH')` is 926. Windows is case-insensitive everywhere else |
> | `system(1010)` answered **`Linux`** on Windows — ***FIXED 26 Aug 2026, uncycled*** | `system(1006)` still answers `0` and is an open decision. **`system(91)` was already right** |
> | ***`kernel()` is internal-only, and page 07's advice was wrong*** | it told the reader to convert a POSIX path with `kernel(K$WINPATH, ...)`. An ordinary program cannot call `kernel()` at all — **corrected in the page this session** |
> | an unknown function reads as a **matrix** | `v = testlock(5)` gives *"Matrix TESTLOCK is not referenced in a DIM statement"* at the **last line of the program**. With three arguments it is *"Right bracket not found where expected"* instead |
> | `sdencrypt()` has no usable key from an ordinary account | a passphrase gives status **10204**, a key-length error. The derivation function is `sdext()`, which is internal-only |
> | `os.execute` **aborts** when the account lacks the right | *"don is not permitted to use OS.EXECUTE"*. No `else`, no `on error`, no status to test |
> | the debugger is **line-mode on this port, always** | `full.screen` is `terminfo('sreg') # ''` (`DEBUG:522`), and `sreg` is an SD-client capability the `windows` definition does not carry. Nothing is lost, and it means the debugger **can be driven from a pipe** |
> | `debug` and `pdebug` are on `TIER.OMIT.STANDARD` | a standard account has neither verb; the `debug` **statement** is its only way in |
>
> ***AND EVERY EXAMPLE IS MEASURED, WHICH IS NOT DECORATION — IT CAUGHT FOUR
> WRONG ANSWERS THE REFERENCE WOULD HAVE PRODUCED.*** `div(7,2)` is **3**, not
> `3.5`, because the intrinsic `DIV()` compiles to `OP.QUOTIENT` and not to the
> `/` opcode that shares its name (`BCOMP:476`); `idiv()` truncates on two
> integers and **floors** if either is floating point, so `idiv(-7,2)` is `-3`
> and `idiv(-7.0,2)` is `-4`; `num('')` is **true**; `shift()` right-shifts
> **unsigned**, so `shift(-1,1)` is `2147483647`. The probe route is a program
> written into `C:\ProgramData\SD\user_accounts\don\bp` — **writable without
> elevation, where `sdsys\bp` is not** — then `BASIC`/`RUN` down §6's
> `Invoke-SD` pipe. Runner kept at
> `scratchpad\run-zzmath.ps1`; it refuses a run that did not print its own
> START and END markers.
>
> ***NOTHING ABOUT THE DOCUMENTATION IS IN THIS REPOSITORY ANY MORE.***
> Repository
> [SDCoreWindowsDocs](https://github.com/dmontaine/SDCoreWindowsDocs), working
> tree `C:\Users\dmont\Projects\SDCoreWindowsDocs` — **the owner
> moved it out of `sdhelp` on 26 Aug 2026** — branch `main`,
> **pushed**. The P-drive copy is stale. Three sets, each `markdown` +
> `html` + `pdf`: `Testing` holds the 15-page tester set, `User` holds the
> SD BASIC reference in progress, `Technical` is empty.
>
> ***HE ALSO REVIEWED PAGE 00 AND THE LINEAGE IN IT WAS WRONG.*** SD Core is a
> version of SD carrying elements of the main SD version and of ScarletDME;
> **ScarletDME forked the original GPL release of OpenQM 2.6.6**, which did not
> carry every feature of the commercial 2.6.6 and **for which no documentation
> was ever released**. So *"anything true of stock OpenQM is out of scope"* is
> struck: the OpenQM documents are a **reference, not an authority**. Head
> `076fdd7`.
>
> ***THE OWNER ANSWERED THE 18-QUESTION REVIEW LIST ON 26 Aug 2026. SIXTEEN ARE
> APPLIED; TWO ARE OPEN*** and are at the top of `QUESTIONS-2026-08-26.md` —
> **q7** the `limitssh` default, re-asked with four options because *"not sure
> what you are proposing"*, and **q14**, which he did not answer. The rest of
> the answers and what each changed are in that file; **do not re-derive them
> here.**
>
> ***THE PAGES ARE NUMBERED `00`–`14`, FLAT, AND THAT IS LOAD-BEARING.*** They
> were briefly `01a`/`01b`/`06a` and it put them in a different order in
> Explorer than in the renderer — §6's hyphen-collation trap. **Do not
> reintroduce a letter suffix to avoid a rename.**
>
> ***THE TOOLCHAIN WENT WITH IT (q15) AND `$neverShipped` LOST BOTH NAMES.***
> `mkdoc.py` and `mkpdf.ps1` are `tools\` in the docs repository, along with
> **`release.ps1`**, which renders only what changed, **refuses to zip when any
> generated page is older than its Markdown**, and prints a SHA256.
> `assert-current.ps1` carries a comment where the two entries were saying not
> to re-add them. `setup-devbox.ps1` still installs python-markdown, because the
> pages are rendered on this box.
>
> ```
> tools\release.ps1                 (in the docs repository, not here)
> ```
>
> ***THE CHANGELOG FIX OF 26 Aug DOES NOT MAKE THE TREE STALE.*** Two wrong
> statements in the 21 Aug API entry were silently corrected (`sd.conf`'s path,
> and the `sdapi` wording). Measured after: `assert-current` **exit 0** — it
> prints `EXEMPT: sdsys\changelog is newer than the install`. **So the
> correction reaches an installed system only at the next install**, and no
> verifier is blocked meanwhile.
>
> ***q18 LEAVES A PIECE OF WORK BEHIND AND IT IS NOT A TASK YET.*** The ruling
> is that a **client** installer carries the DLLs, the documentation and the
> related utilities, **no source of any kind**, and creates a `docs`
> subdirectory holding the GitHub references. That is a change to
> `sdclient.iss` / `qmclient.iss` in the client repositories — **not to
> `sd.iss`** — and it has not been made. Page 10 of the tester set says plainly
> that W1.0-0 does not ship it.
>
> **Identity is set per repository, not globally, on this machine** — a new
> clone needs `user.name`/`user.email` set, or commits fail with *"unable to
> auto-detect email address"*. The docs repository's `README.md` carries that
> and the build commands.
>
> ***THE ONE ERROR HE CAUGHT, AND IT IS WORTH NOT REPEATING.*** A first draft
> said accounts SD creates *"sign in over ssh and nothing else"*. **Wrong**: they
> cannot log in to **Windows**, and they reach SD over ssh **or through an API
> client**. A standard-tier account with `api` and no `ssh` is an ordinary thing
> — someone running a custom GUI client — and is probably the commonest shape a
> deployed system has. The API is not a developers-and-administrators feature.
>
> ***WHAT WAS SETTLED BEFORE IT STARTED:*** the format, the audience, where it
> ships, and the topic list, which is his verbatim. All of it is in
> §"DOCUMENTATION DECISIONS" and §"THESE FOUR ARE THE BRIEF" below, and those
> two sections were deliberately left untouched by the 26 Aug prune.
>
> ***THE SAMPLE WAS JUDGED AND PASSED:*** *"I like the format"*, and the
> aggregate-by-function shape was singled out. Sample at
> `docs\sample\file-commands.html`, source
> [docs/sample/file-commands.md](docs/sample/file-commands.md). ***THE RENDERER
> IS NO LONGER IN THIS REPOSITORY*** (q15, 26 Aug 2026) — rebuilding the sample
> now reaches across to the docs repository:
>
> ```
> python "C:\Users\dmont\Projects\SDCoreWindowsDocs\tools\mkdoc.py" --in docs/sample --out docs/sample
> ```
>
> ***THE INTERPRETER DECISION IS ANSWERED — OWNER, 26 Aug 2026: THE MSYS2
> PYTHON.*** `mkdoc.py` is the only thing in the whole build with a third-party
> dependency — `markdown`; every other import across the ten `gplbld/*.py`
> files is stdlib or local. **The gap was bigger than the package**:
> python-markdown 3.10.2 was installed for the **Windows** python (3.13.14),
> not the **MSYS2** python `setup-devbox.ps1` installs (3.12.13), so on a fresh
> box `python mkdoc.py` failed at the *interpreter*, not at the import.
>
> ***`python-markdown` IS NOW IN `setup-devbox.ps1`'s PACKAGE LIST, AND IT IS A
> PACKAGE RATHER THAN A `pip install` FOR A MEASURED REASON.*** The MSYS2
> python has **no pip at all** — *"No module named pip"*, measured 26 Aug 2026
> — so the pip route needs `python-pip` first and then an unpinned download
> outside pacman. **`msys/python-markdown` is 3.10.2-1, the same version the
> sample was rendered with**, so it needs neither. It is in the **msys** repo,
> not only the mingw ones; a `pacman -Ss python-markdown` that looks mingw-only
> has been truncated.
>
> ***MEASURED, NOT ASSUMED:*** `setup-devbox.ps1 -CheckOnly` on this host,
> 26 Aug 2026, reports **`missing: python-markdown`** and hands over
> `pacman -S --needed python-markdown`. **It is the only missing package** —
> every other one was already present — so that line is the change firing and
> nothing else.
>
> ***AND IT IS NOT YET INSTALLED HERE.*** Until it is, `mkdoc.py` runs only
> under the Windows python, which is what has rendered every page so far. It
> exits 2 naming `pip install markdown` if the import is missing, so it fails
> loudly either way.
>
> ***THE `$neverShipped` HALF OF THIS IS SPENT.*** `mkdoc.py` and `mkpdf.ps1`
> left `gplbld` on 26 Aug 2026 (q15) and both entries were removed in the same
> commit; a comment stands where they were. **What still holds is the reason:**
> naming a `.md` in `stage.py` or `sd.iss` puts it under `assert-current`'s
> `$shipsAs` valve, **after which every documentation edit costs a full cycle**.
> Documentation does not ship from this repository, so nothing has to be wired
> up here at all.
>
> ***ONE DEFECT THE PHASE WILL HAVE TO RULE ON.*** `sdsys\changelog` ships into
> the **data tree**, which the installer never overwrites, so a user's changelog
> is frozen at their install date — in the one file whose entire job is telling
> them what changed. It probably wants moving to `{app}` beside the
> documentation. Raised 25 Aug 2026; not decided, and not yet a task.
> ***IT HAS NOW BITTEN ONCE***: the two silent corrections of 26 Aug (q1, q8)
> reach an installed system only at its next install, and `assert-current`
> exempts the file by name rather than reporting the tree stale.
>
> ### 3. THE DATA-TREE UPGRADE PATH — CLOSED 26 Aug 2026, RUN AND MEASURED
>
> `verify-upgrade.ps1 -Compare`, elevated, 21:48:14: **55 PASS, 0 FAIL, 1 SKIP
> of 56 rows, exit 0**, on the install that ran over the top at 21:21 on
> 25 Aug. `RefreshDictionaries` fired on the same install for the first time
> ever — **76 of 76 dictionary records, `COMPLETE`** — which closed the other
> half.
>
> ***THE LESSON IS NOT THE UPGRADE, IT IS THAT NOBODY RE-READ THE TREE.*** The
> install had already happened and been recorded as *"not yet done"*, because
> the scoring failed and the failure was diagnosed without anyone looking at
> the tree it was scoring. ***Do not re-run `-Snapshot`.***
>
> ### 3a. VFS STRIPPED FROM THE C — CLOSED 25 Aug 2026, CYCLED AND VERIFIED
>
> Checked directly on the installed tree, because **the suite has no VFS step**,
> and every check paired with a control: `$define FL$TYPE.VFS` 0 against
> `FL$TYPE.SEQ` 1, `$define ER$VFS.*` 0 against `ER$ENCRYPTED` 1, `$define
> FVAR.NET` 0 against `FVAR.SEQ` 1, `_EXTENDLIST` absent from all three of
> `gpl.bp`, `gpl.bp.out` and `pcode.out` against `_DELLIST` present in all
> three. `UPSTREAM_FIXES.md` entry 15 is written.
>
> ***THE FIRST VERSION OF THAT CHECK WAS WRONG AND IS WORTH THE WARNING.*** It
> grepped for the bare names and reported 1 and 2 hits — **the history comments
> that deliberately name what was removed.** A pattern that matches the removal
> notice as readily as the definition is not a check. Anchoring on `^ *$define`
> and pairing each with a control is what made it decisive.
>
> ### 4. THE REMOTE-BLOCK CONTROL — CLOSED 25 Aug 2026. THE SCOPING BLOCKS A REMOTE MACHINE
>
> The §5.9 claim had been outstanding since 13 Aug and is now measured, with
> the disagreement that makes it decisive: rule `Any` → host dial **CONNECTED
> 23ms**; rule `127.0.0.1` → **dropped 4003ms**, with port 5040 on the same
> guest answering in **23ms** as the witness that the guest was up and the host
> could reach it.
>
> ### 4a. THE ssh REMOTE-BLOCK RUNBOOK — RUN AND PASSED, AND KEPT FOR THE NEXT GUEST
>
> Seven steps, a person at the wizard. ***The `Open` leg must run FIRST***, and
> the precondition is a **Private** network profile on the guest. Kept because
> anything else that needs a machine that never had OpenSSH wants the same rig.
>
> ### 5. THE STAND-ALONE INSTALL — CLOSED 26 Aug 2026. 21 PASS, 0 FAIL, ***0 SKIP***
>
> On guest `sdStandalone-C1` at 01:46:11. The row that had never once been
> measurable, `no ssh server on this machine at all`, fired its **strong form**.
> The owner cycled choosing stand-alone and looked at both pages.
>
> ***WHAT THE PAGES SHOWED IS WRITTEN DOWN, WHICH IS THE STEP THAT WAS MISSED
> LAST TIME RATHER THAN THE LOOKING.*** The mode page and the tasks page are
> correct, with **no `sshremote`/`apiremote` boxes** on a stand-alone run —
> which was unrecorded either way after the 25 Aug run, and is the fault
> `check-stale-leads.py` phase 3 was built for.
>
> ***THE PREFLIGHT QUESTION IS ANSWERED AND NEEDS NO CODE CHANGE.*** Owner,
> 26 Aug 2026: the ssh preflight **still refuses** on a stand-alone install. A
> stand-alone install neither installs nor configures an ssh server, so the
> reason for the refusal does not apply — but relaxing a check verified on three
> guests the same week was his call, and he kept it. ***Do not reopen it as a
> tidiness item***, and note it was never a one-line change either way: the
> preflight runs in `InitializeSetup`
> ([sd.iss:829](sdb_ai/sd64/gplbld/sd.iss:829)), **before the wizard is drawn,
> so before the mode can have been chosen**, which is why "skip it when
> stand-alone" cannot be a `Check:`.
>
> ***FOUR FACTS ESTABLISHED WHILE SCOPING IT, so nobody re-derives them:***
>
> - ***`APIPORT` UNSET MEANS SD OPENS NO PORT AT ALL*** —
>   [sdwind.c:351](sdb_ai/sd64/gplsrc/sdwind.c:351) and `sdwind.c:310`. So "no
>   API" is a real state, not just a firewall rule. A stand-alone `sd.conf`
>   omits `APIPORT`.
> - ***`APILOGIN` IS NOT AN OFF SWITCH.*** It decides whether the API demands a
>   password (`op_kernel.c:848`); `APILOGIN=0` is the WEAKER setting, not the
>   safer one. Do not reach for it here.
> - **The installing user's own account needs no ssh.** `CREATEA` puts only
>   non-administrators in `sdsshonly`, and `LOGIN` admits the console when
>   elevated.
> - **`sd.conf` is `onlyifdoesntexist`**, so a stand-alone variant is written on
>   a first install only — an upgrade will not rewrite it.
>
> ***AND SWITCHING BETWEEN THE TWO ACCOUNTS IS NOT A PROBLEM.*** A stand-alone
> system still has the user's own account and `SDSYS`. `LOGTO SDSYS` asks for no
> password — `LOGTO.STEP.UP` was deleted 14 Aug 2026, `CPROC:2568` calls
> `elevate('START','')` and the gate is elevation — and an already-elevated
> session switches with no prompt at
> [sd-elevate.ps1:105](sdb_ai/sd64/gplbld/sd-elevate.ps1:105). **`CPROC:2566`
> and `sd-elevate.ps1:23` both say `!elevate` *"cannot work over ssh"*, and that
> is true only when a PROMPT is needed** — whether an ssh token is elevated
> depends on `LocalAccountTokenFilterPolicy`, which §5.6.2 records as never
> measured. ***Do not restate either comment as absolute until somebody
> measures it.***
>
> ---
>
> ## DOCUMENTATION DECISIONS, AGREED 25 Aug 2026
>
> ### WHERE THE WORK LIVES: ~~THIS REPOSITORY~~ ***REVERSED 26 Aug 2026 — ITS OWN GitHub REPOSITORY***
>
> ***OWNER'S DECISION, 26 Aug 2026, AND IT OVERRIDES THE 25 Aug RULING BELOW:***
> *"there will be a separate repository on github for all the documentation we
> create. It will not have the no binary bits rule."*
>
> **So the documentation is a project of its own**, and ***the no-binaries rule
> in CLAUDE.md is a `sd4windows` rule only*** — it does not travel to the
> documentation repository, which may therefore track the rendered PDFs
> alongside their Markdown. **Nothing about `sd4windows` changes: no binary
> becomes trackable here.**
>
> ***THE REPOSITORY IS
> [github.com/dmontaine/SDCoreWindowsDocs](https://github.com/dmontaine/SDCoreWindowsDocs)***,
> created 26 Aug 2026 and **created empty**, which is what the first push
> needed. Working tree
> `C:\Users\dmont\Projects\SDCoreWindowsDocs` — the owner moved it
> out of `sdhelp` the same day — `origin` set, **pushed**.
>
> ***THE MARKDOWN IS TRACKED AND THE GENERATED `.html`/`.pdf`/`.zip` ARE NOT.***
> Ruled 26 Aug 2026, question 16: the pages are rendered after a change, only
> the ones that changed, and the two eventual deliverables — a PDF download and
> the pages on a web site — are both built from the Markdown at release time.
> `tools\release.ps1` there does it and refuses on a stale page.
>
> ***WHAT THE OLD RULING WAS FOR, BECAUSE THE RISK IT NAMED IS REAL AND IS NOW
> UNMANAGED.*** It read: *"documentation has to ship with the code, be versioned
> with it and be checkable against source. A separate repository recreates the
> drift this codebase keeps paying for — on 25 Aug alone, four statements in the
> installer dialogs had quietly stopped being true, and a writer working from a
> detached copy would have faithfully documented all four."*
>
> **That was not answered, it was outweighed.** A documentation repository
> cannot be checked against source by anything that runs, so ***drift is now
> caught by a person or not at all***. Two consequences to carry: write from
> source and from this file rather than from a rendered page, and **re-read the
> installer dialogs and the changelog whenever a release moves**, because
> nothing will fail if a page goes stale.
>
> ***THE SIZE PROBLEM IS `PROJECT_STATUS` ONLY.*** It is read every session;
> `HISTORY` is read on demand, so its length costs nothing. Compress the closed
> steps — 0-2 and 4-17 — into `HISTORY`, which this file already does in places
> (*"Detail compressed 21 Aug 2026 under §0.5"*). ***DO NOT REWRITE `HISTORY`***:
> rule 1 is append-only and it has earned its keep repeatedly.
>
> ### WHERE THE DOCUMENTATION SHIPS: `{app}\doc\`, NOT THE USER'S DOCUMENTS FOLDER
>
> Everything under `{app}` is *"replaced on upgrade and removed on uninstall"*,
> which is exactly the lifecycle documentation wants. A Start Menu shortcut goes
> beside the two that exist (`{group}\SD`, `{group}\Check the SD installation`).
> The user's Documents folder is wrong three ways: it is their space, it would
> never be updated, and uninstall would leave it behind.
>
> ***AND THIS EXPOSED A REAL DEFECT, RECORDED HERE BECAUSE IT IS THE SAME FAMILY
> AS THE UPGRADE PATH: `sdsys\changelog` SHIPS INTO THE DATA TREE***, which the
> installer never overwrites. **A user's changelog is therefore frozen at their
> install date and can never be updated** — in the one file whose entire job is
> telling them what changed. It probably wants moving to `{app}` too. Not yet
> decided; not yet raised as a task.
>
> ### THE FORMAT: MARKDOWN IN THE REPOSITORY, SINGLE-FILE HTML AT STAGE TIME
>
> Every Windows machine has a browser, so there is nothing to install and no
> format to explain. **Single file with embedded CSS** — no asset folder to
> break. Works offline, which matters on the machines SD installs on. The user
> can print to PDF from the browser, so **no PDF needs shipping, which the
> no-binaries rule forbids anyway** (it is why `sdhelp` is hand-carried).
>
> ***WHAT ACTUALLY MAKES THEM LOOK GOOD*** — about 100 lines of CSS, written
> once and shared:
>
> | | |
> |---|---|
> | line length capped ~70-75 characters | the single biggest win; full-width text is what makes docs look amateur |
> | a system font stack | no web fonts, so no network dependency and no licence question |
> | real table and code-block styling | technical documentation lives or dies on these |
> | a table of contents with anchors | long reference pages are unusable without one |
> | a print stylesheet | so browser-to-PDF comes out clean |
>
> ***THE CONVERTER: a small pure-Python Markdown library*** (`markdown` or
> `mistune`) called from a `gplbld/` script. It fits the existing Python build,
> and `setup-devbox.ps1` can install it beside the rest of the tooling. Writing
> the documentation in HTML directly avoids the dependency and is much worse to
> write and review; **pandoc is the better converter and is rejected** — a
> binary dependency cuts against building from source.
>
> ***CHM IS REJECTED, AND NOT ONLY FOR THE OBVIOUS REASON.*** It is the classic
> Windows help format with real advantages — F1 integration, built-in search —
> but it is a binary, its toolchain is long abandoned, and **Windows blocks CHM
> files opened from a network path**. That produces a "help does not work"
> support problem which never reproduces on the developer's own machine.
>
> ### RULED 25 Aug 2026 ON SEEING THE SAMPLE. THESE FOUR ARE THE BRIEF
>
> ***1. `..\sdhelp` IS A RESOURCE, NOT A SOURCE TO COPY.*** Owner: *"use the
> documents in `..\sdhelp` as resources but do not copy them verbatim. Always
> make sure to wrap in the changes we have made for our version."* **The sample
> page is closer to a transcription than the brief allows** — it is a format
> demonstration and should not be taken as the model for how much of a help
> page to carry over. Every page is rewritten for this port, with our
> behaviour folded in. §2's sdhelp entry is why that is not pedantry: three
> defects in three pages, in one afternoon.
>
> ***2. AGGREGATE BY FUNCTION.*** Owner singled this out: *"I like the way you
> have aggregated by function 'File commands' rather than the more typical
> 'one command at a time' format."* So a topic page holds the verbs that belong
> together. `..\sdhelp`'s one-file-per-verb shape is not the model.
>
> ***3. THE FIRST DOCUMENT SET IS FOR TESTERS, AND ITS AUDIENCE DECIDES ITS
> CONTENT.*** They *"will already be familiar with Pick-like systems,
> especially openQM, and will only need documentation to tell them how SD Core
> for Windows is different."* **So it documents the DELTA, not the product.**
> Anything true of stock OpenQM is out of scope for this set; comprehensive
> documentation comes later. His topic list, verbatim — *"Things that are
> unique to SD Core"*:
>
> | | |
> |---|---|
> | Installation | |
> | Account types | Standard, Programmer, Administrator, Group |
> | Admin Only Commands | and how to use them |
> | Programmer / Admin Commands | and how to use them |
> | SSH Access | |
> | API Access | |
> | Lower case and case conversion | |
> | Security Improvements | |
> | Other Hardening | |
> | Historical features not available in SD Core | |
>
> ***AND ONE THE OWNER NAMED EXPLICITLY, 25 Aug 2026, BECAUSE A TESTER WILL
> ASSUME OTHERWISE:*** *"note that this version does not support multi-user on
> windows server using rdp"*. **It belongs in the notes, stated plainly.** It is
> not an oversight and not a gap to be filled later — it follows from the access
> model and is already settled:
>
> - `sdsshonly` carries **both** `SeDenyInteractiveLogonRight` **and**
>   `SeDenyRemoteInteractiveLogonRight`
>   ([deny-logon.ps1:29](sdb_ai/sd64/gplbld/deny-logon.ps1:29)), and `CREATEA`
>   joins every non-administrator account to it — so an SD account is denied the
>   physical console and Remote Desktop together.
> - **`RDPACCOUNT` was built to lift exactly this and was deleted after a day**
>   (§"`RDPACCOUNT` was built and then deleted"): one Windows setting covers RDP
>   and the keyboard, so lifting the RDP denial lifted the console denial with
>   it. `CREATEA:683` also records that multi-user RDP means Windows CALs, *"so
>   a site that wants it is buying a commercial product, and it is outside this
>   port's focus."*
> - **The rule that holds without exception:** nobody SD creates can log in to
>   Windows at this machine unless they are already a Windows administrator.
>   Concurrent users reach SD **over ssh**, which is what the ssh path is for.
>
> **Nearly every row already has its answer written down in this file**, which
> is the payoff for keeping it: account types §5.6, admin/programmer verbs and
> the tiers §5.11, ssh §5.9, the API §5.13, case §5.12, the ACL and hardening
> work §7 steps 14-15, and the removed features §"SDNet is gone" and §5.19.
> **Write from source and from here, not from `..\sdhelp`.**
>
> ***4. THE THREE STYLE SUB-CHOICES IN THE SAMPLE WERE NOT CALLED OUT
> INDIVIDUALLY*** — lower-case commands, dark mode following the machine, and
> the sidebar table of contents. *"I like the format"* covers the page as
> rendered, so **they stand as shipped**; none has been separately ruled on and
> any of them is a one-line change.
>
> ---
>
> ### THE CLOSED RECORD THAT USED TO SIT HERE
>
> Items 3, 3a, 4, 4a and 5, the refuse-to-install work, the ssh firewall
> defect, the rig notes and the session-by-session records back to the
> forty-ninth were moved to HISTORY.md on 26 Aug 2026 — entry ***"ARCHIVE
> 26 Aug 2026 — START HERE's closed record, sessions 49 to 60, in full"***.
> The task table at the top of this file carries their conclusions. **Nothing
> was deleted.**


---

### Phase 3, as built — the parts that are not visible in a diff

**THE MARKER IS A WINDOW IN TIME, NOT A SECOND IDENTITY TEST.** `sdsys/$adopt`
is not ACL'd against anyone — the data tree grants `sdusers` Modify, so any SD
user can create it. It buys them nothing: `K$INTERNAL` still means
`sd -internal`, which `sd.c` forces to SDSYS, which `LOGIN` refuses without an
elevated session. **This reverses the 15 Aug position** — that an elevated
administrator typing `ADOPT` by hand is acceptable — on the owner's ruling of
21 Aug.

**AND NO VERIFIER MAY RE-OPEN THE WINDOW - owner's ruling, 21 Aug 2026.**
*"The ADOPT command itself is not supposed to be available after
installation."* Two verifiers were writing the marker themselves and adopting an
account, which made the product read as though it offered a door it does not.
Neither does now: **`verify-delaccount` builds its borrowed subject with
`CREATE.ACCOUNT` and then sets the Windows description**, which is the only
thing `!is_sd_user` reads (`IS_SD_USER:94`), and **`verify-accountrules` takes
its control from the install's own adoption** - `adopt-account.log`,
`accounts/DON`, the spent marker, the route groups - instead of performing a
second one. **ADOPT is now invoked in exactly two places: `adopt-account.ps1`,
and one verifier that requires it to be REFUSED.**

**AND THE STANDARD IS THE PRODUCT AS DELIVERED - owner, 21 Aug 2026.**
*"Since this is an open source project, users can make any changes they want.
The goal is to make the project, as delivered, enforce the idea that SD account
setup happens in SD. If users want to degrade security after the fact, that is
their right."* **This overrules the argument that a gate an elevated
administrator can pass is not worth building** - an administrator who forges a
marker, or writes an `ACCOUNTS` record by hand, is exercising their right and is
not the case the design answers to. What the design owes is that **nothing the
shipped product offers sets up an SD account outside SD.**

**AFTER AN INSTALL THE MARKER IS ABSENT**, so ADOPT is refused as an
unrecognised token on every path the product offers.

**VERIFIED 22 Aug 2026: the marker names the account it authorises.**
`adopt-account.ps1` writes `sdsys/$adopt.<user>` and `CREATEA` tests that path,
so one marker opens the door for **one account** rather than for the verb in
general. **No file parsing** - the name is in the path, and both sides downcase
the same `$User` this script was invoked with, which answers the objection
`adopt-account.ps1` used to carry ("a mismatch on case or a domain prefix would
break the install").

**HOW IT WAS MEASURED, and it is the install itself rather than a verifier
re-opening the door.** On the 08:32:03 install: `adopt-account.log` records
*"don now has an SD account"*, `accounts/DON` exists, `verify-tiers` reads its
tier as `ADMINISTRATOR`, **no `$adopt*` file survives under `sdsys`**, and
`verify-accountrules` §4 pairs the refusal (2018, no marker) with that adoption
as its control. A marker that no longer matched its name would have shown up as
the installing user having **no SD account at all**.

**AND THE TWO SIDES CANNOT DRIFT ON CASE**, which was nearly untrue: see the
header's case-fold note. `adopt-account.ps1` now folds with
`ToLowerInvariant`/`ToUpperInvariant` to match SD's ASCII `lc_chars`/`uc_chars`
maps; the culture-sensitive forms it used before would have disagreed on a
Turkish or Azeri locale.

**IT IS BUILT WHERE THE NAME IS PARSED, NOT IN `more.args`, AND THAT IS THE
WHOLE CARE IN IT.** `more.args` is shared with the GROUP and OTHER arms, which
never assign `acc.uname` - and **`AND` does not short-circuit**, so
`downcase(acc.uname)` in the ADOPT case condition would abort every
`CREATE.ACCOUNT GROUP` with an unassigned variable. That is precisely the defect
§6 records at `CREATEA:1405`, which survived from 10 June to 21 Aug 2026.
`CREATEA:280` sets it in the USER arm, between the name parse and
`gosub more.args`; the bare `$adopt` at `:241` stays as the fallback for the
arms that never adopt, and **nothing writes that name any more.**

**DOWNCASED ON BOTH SIDES DELIBERATELY.** `acc.uname` keeps whatever case was
typed on the ADOPT path: the `downcase` at the `is_user` test runs only in its
**else**, so an account found under its typed spelling is never folded.

**REFUSING ADOPT ONCE ANY ACCOUNT IS REGISTERED WAS CONSIDERED AND REJECTED.** A
second administrator reinstalling over an existing tree has no SD account and no
other supported way to get one, because `CREATE.ACCOUNT USER` refuses a name
whose Windows account already exists (10038). It would have been a real
regression, not a tightening.

**NO CHANGELOG ENTRY, DELIBERATELY.** ADOPT is undocumented on purpose - it is
refused as an unrecognised token so it "tells nobody it exists" - and §7 step 3
records the owner's decision not to document it. Nothing a user can see changed:
the install behaves as before and the verb was already refused afterwards.

**IT IS DELETED IN TWO PLACES.** `CREATEA` deletes it on acceptance, so it
authorises exactly one adoption; `adopt-account.ps1` deletes it in a `finally`,
so a refused verb or a killed process does not leave it behind. **Only an
accepted `ADOPT` can spend it**: the existence test is in the `case` condition
and the delete is inside the branch, written so as not to depend on whether
`AND` short-circuits — which, as `CREATEA:1405` records, it does not.
**It must never be in the source tree**: `stage.py` copies `sdsys` wholesale, so
a committed marker would leave the door open on every install.

**TWO DELIBERATE DEVIATIONS FROM THE APPROVED PLAN, both forced by an ACL, both
confirmed by the `$cred/DON` write at 16:19 on 21 Aug.**

1. **The closing SD session is `[Code]` at ssPostInstall, not a `postinstall`
   `[Run]` checkbox.** The plan chose `[Run]` because setting your *own*
   password needs no elevation in SD's permission model — true, and not the
   binding constraint. `sd.iss`'s own gravestone records that Inno runs such an
   entry as *"Run as: Original user"*, and that token carries neither `sdusers`
   (so it cannot open the data tree until the user signs out) nor
   Administrators (so `!CRED_SET` could not write `$cred`). Setup's token has
   both — and the credential written at 16:19, into a store locked to SYSTEM and
   Administrators, is the proof.
2. **The `LOGIN` rule fires only for an ELEVATED session at a REAL TERMINAL.**
   `secure-cred.ps1` locks `$cred` to SYSTEM and Administrators, so an ordinary
   session can neither read it to ask the question nor write it to answer. And
   **the terminal test is what keeps the suite alive**: `Invoke-SD` pipes a
   script into `sd` in ten verifiers, and a prompt in front of that would eat
   `LOGTO SDSYS` as the first password attempt.

**THE TERMINAL TEST IS `kernel(K$TTY,0) # ''`, AND IT WAS MEASURED.** `K$TTY` is
`ttyname(fileno(stdin))` (`kernel.c:250`). Probe built with the MSYS2 gcc,
21 Aug: piped stdin → `isatty=0`, `ttyname=(NULL)`; a new console window — what
Inno's `Exec` with `SW_SHOW` gives `sd.exe` — → `isatty=1`, `ttyname=/dev/cons0`.
**Do not re-derive this.**

**`require.credential` ASKS BUT DOES NOT AUTHENTICATE.** Login still takes no
password. It is `LOGIN:643`; it fails **open** if `$cred` cannot be opened —
that means a broken install, and refusing every elevated login for it takes away
the session that could repair it — while the API fails **closed** on the same
condition in `!CRED_VERIFY`. **An empty password is the way out of the prompt
loop**, and it has to be one, or a session that cannot write a credential would
loop with no exit but killing the process.

---

### Phase 4, as built

**NO PRODUCT CODE CHANGED** — four `gplbld` files. **Every refusal in
`verify-accountrules` has a control that succeeds**: *"nothing was created"*
passes just as happily on a build where `CREATE.ACCOUNT` never creates anything,
so each leg refuses and then makes **the same account** with the one thing that
was missing — the keyword, a matching password, the marker.

**THE PASSWORD FAILURE IS PROVOKED WITH TWO DIFFERENT PASSWORDS**, not a weak
one: `SET_PASSWD:100` returns false on `pw1 = '' or pw1 # pw2`, which is
deterministic where a policy-rejected password depends on the machine. **The
unwind is measured on all four traces** — register, directory, Windows user,
`sdu_` group — which turns `CREATEA`'s claim that the unwind is complete into a
measurement.

**THE ONE CHECK THAT SEPARATES ABSOLUTE FROM ADDITIVE** is `verify-routes` step
4: after `MODIFY.ACCOUNT x API` on an account created with `SSH`, the routes
must be `api` **alone**. An additive implementation passes everything else in
that file.

**A NEW VERIFIER MUST GO ON `assert-current`'s `$neverShipped` LIST**, or it
reports the tree stale because it exists and then refuses to run on the strength
of its own newness.

---

### The message numbers Phase 2 added

So a refusal naming one is identifiable without a grep. Retired with them:
10063–10072, 6029, 6031.

| | |
|---|---|
| 10076-10079 | the four resulting-access statements — ssh only / API only / both / none. **Shared by `CREATE.ACCOUNT` and `MODIFY.ACCOUNT`** so access reads the same however it was set |
| 10080 | already had that access; nothing changed |
| 10081 | unable to change remote access for %1, status %2 |
| 10082 | **say who may reach this account** — `CREATE.ACCOUNT USER` with no keyword |
| 10083 | %1 is an administrator and always has both |
| 10084 / 10085 | the delete confirmation, with and without a Windows account to name |
| 10086 | an account must have a password; nothing was created |
| 10087 | %1 is a group account and has no remote access |
| 10088-10095 | what `require.credential` says (Phase 3) |

**`set.access` IS A `gosub` SUBROUTINE IN `CREATEA`**, not a verb or a file. It
turns `access.ssh` / `access.api` into `sdssh` / `sdapi` membership and prints
one of 10076–10079. **It is called from the USER arm only, and deliberately from
OUTSIDE the `make.admin` and `adopt` else branches** — that placement is the
whole of the administrators-get-the-API fix, because the join it replaced sat
inside them. `MODIFYA`'s equivalent is `route.set`, which additionally REMOVES
memberships, since it is absolute.

**THE PLAN IS AT `C:\Users\dmont\.claude\plans\zazzy-questing-engelbart.md`** —
approved 21 Aug, and it carries the reasoning for each phase and the
group-account section that shaped the password rule.

---

## THE FILE HALF IS CLOSED (21 Aug 2026). A REMOTE API SESSION STILL RUNS AS LocalSystem

**COMPRESSED 21 Aug 2026 under §0.5**, which says a closed step's material goes
down to its conclusion. This section was ~3,500 lines — a third of the file —
and almost all of it was the record of an exposure that is **fixed**. The record
was **moved, not deleted**: HISTORY.md, *"ARCHIVE: the LocalSystem exposure
record"*, 21 Aug, holds it verbatim, and the session entries around it
(20 Aug *"a remote API session appears to run as LocalSystem"*, *"CONFIRMED …
and can rewrite `$cred`"*, *"Acting on the API finding"*, 21 Aug *"the gate is
built"*) are the narrative. What is below is what is still true.

**THE FILE HALF: CLOSED AND MEASURED.** A remote API session can no longer open
`$cred` (`ER_PERM`, 3035) nor reach `OS.EXECUTE`. The account it stands in is
its root — the containment gate in `op_dio2.c` plus the `USR_ADMIN` fix in
`kernel.c`. Confirmed by `verify-apiadmin` on every install since, most recently
**22/23 on the 17:18:11 install** (the 23rd is the standing N/A). §"THE GATE"
has the six entry points and the read/write axis.

**THE TOKEN HALF: OPEN, AND IT IS THE ONLY LARGE ITEM LEFT.** `sdwind` `fork()`s
the session, so it inherits the LocalSystem service token. Only the session's
REACH was narrowed; its IDENTITY is untouched. §WHAT IS LEFT, cheapest
first carries it.

### What fixing it involves — kept because the reasoning is what dates

**"CAN `sdwind` RUN AS SOMETHING OTHER THAN LocalSystem?" — owner, 20 Aug 2026.
YES, and §5.7 specifies a virtual account, `NT SERVICE\SD`, needing no password
management. Three things qualify it, and the third is the one that matters.**

1. **A BLOCKER IN OUR OWN CODE.** `sd -start` is gated on `IsElevated()`
   (`sd.c` `check_admin()`), true only with `BUILTIN\Administrators` in the
   token. **A virtual service account is not in that group, so the service could
   not start SD.** `install-service.ps1:22` says so outright. Changing the
   account means changing that gate, not just the service definition.
2. **THE ACLs ARE THE REAL WORK: TEN PLACES NAME SYSTEM.** Eight
   `gplbld/secure-*.ps1` (`account-dirs`, `accounts`, `audit`, `cred`, `gcat`,
   `log`, `osusers`, `psdir`), the data-tree root at `sd.iss:291`, and **one
   that is not an ACL at all** — `win32sem.c:112` builds
   `D:(A;;GA;;;SY)(A;;GA;;;BA)(A;;GA;;;<group>)` for the semaphores, so a
   service that was not SYSTEM could not reopen its own objects. Mechanical, but
   ten places and one of them is C.

   **`Global\` IS NOT A BLOCKER, and `win32sem.c`'s comment overstates it.**
   That comment claims creation needs `SeCreateGlobalPrivilege`. Measured
   20 Aug with a scratch program from an ordinary unelevated token — the
   privilege absent, `Administrators` deny-only — and `Global\sd_scratch_probe`
   was **CREATED, err 0** (`ERROR_ALREADY_EXISTS` checked, not assumed; pid in
   the name; run twice). A service logon would hold it anyway via the SERVICE
   SID `S-1-5-6`. *(Tested: a mutex from a filtered-admin token. Not tested: a
   semaphore with a security descriptor from a service token — same namespace
   rule, different security descriptor.)* Correct the comment next time that
   file is touched; it matters because somebody weighing this decision would
   read it as a blocker.
3. **A SERVICE ACCOUNT DOES NOT FIX THIS ON ITS OWN, AND THAT IS THE POINT.**
   §5.7's stage 2 runs session processes under the service identity — the
   identity that owns the tree. Same reach, different name.

**SO THE QUESTION TO SETTLE IS NOT THE SERVICE ACCOUNT.** It is whether a
session may hold a token that exceeds the user's. Either match the user — an
S4U logon and `CreateProcessAsUser`, the only thing that restores §5.7's
premise, and real work — or accept a service identity and gate the paths.

**AND THAT SECOND OPTION IS NO LONGER HYPOTHETICAL, which corrects what this
section said before 21 Aug 2026.** It used to read *"build the path gating SD
has never had"*. **The gate exists now** (`op_dio2.c`, root = the account the
session stands in). So the choice is narrower than it was: S4U for a token that
matches the user, versus the gate that is already holding. What the gate does
not do is make the session's *identity* the user's, which is what every
non-file check still sees.

**A THIRD PLACE IN THE CODE RESTS ON THE FALSE ASSUMPTION**, after
`APISRVR:459` and `:489`, and it is still there. `check_admin()`'s comment:
*"the client, network and API paths use `-C`, `-N` and `-Q`. **Those children
inherit an ORDINARY user's token**"* — true for phantoms and SDLocal, whose
parent is a user's `sd.exe`; **false for the API, whose parent is the service.**
Written 15 Aug 2026, the day the service landed.

**AND SD HAS NO FILE-LEVEL ACCESS CONTROL OF ITS OWN BEYOND THE GATE.**
`op_openpath` calls `open_file()` with no path restriction (`op_dio1.c:368`).
§5.7 states the premise: *"While SD runs as the invoking user, account passwords
organise access; they do not secure it."* **The API path is the first place
where SD stopped running as the invoking user**, and the gate is what replaced
it.

---

## 0. Maintenance rules

Revised 14 Aug 2026, seventh session, on the owner's instruction: **the
documentation was taking more of a session than the work.** The rules below
replace a longer set that caused it.

**Audience: the next AI session. Not the owner — he does not read these.** Write
for a cold agent that will act on this: terse, factual, `file:line` over
description. No emphasis for effect, no narrative, no argument. The `changelog`
is the exception and stays plain English for users.

> ***THE MOJIBAKE SCAN OF THIS FILE HAS AN EXPECTED VALUE, AND IT IS ONE.***
> Owner, 30 Aug 2026: *"every review of PROJECT_STATUS wonders about the
> mojibake"* — so the answer lives here instead of being re-derived. **A
> double-encoding scan** — `grep -a -o` for the CP1252-through-UTF-8 lead bytes
> `\xC3\xA2\xE2\x82\xAC`, which is what an em dash becomes — **must report
> exactly 1 occurrence, on the `Set-Content` trap in the 21 Aug 2026 entry, and
> that one is a deliberate QUOTATION of the corruption it describes.**
>
> ***SO THE READING IS: 1 IS CORRECT, 0 MEANS SOMEBODY "FIXED" THE EVIDENCE, AND
> 2 OR MORE IS REAL DAMAGE.*** A bare *"this is fine"* note would have settled
> the first reading and left the other two unanswerable, which is why it is
> written as a count. **Do not paste the sequence into any new prose here** —
> naming the bytes keeps the expected value at 1, and a second literal copy would
> break the check this paragraph exists to make cheap.
>
> **The same is NOT true of `PRE_RELEASE_FIXES.md`, `HISTORY.md` or any script:
> there the expected count is 0.** Measured 30 Aug 2026 across all three. The
> underlying rule is `CLAUDE.md`'s — a tracked file is edited with `Edit`/`Write`
> and never by a program — and this paragraph only stops its verification from
> costing an investigation each time.

> ***READING THESE FILES IS NOT THE SAME AS SEARCHING THEM, AND THE PROJECT RULE
> IS TO SEARCH.*** Owner's instruction, 23 Aug 2026: **grep PROJECT_STATUS.md
> and HISTORY.md for the verb, script or flag in any command before running it.**
> `CLAUDE.md` §"Search the record before you run anything" is the rule; it is
> there rather than here because it is loaded every session and this section is
> not. **Three or four consecutive sessions lost time to a warning that was
> already on disk** — most recently `echo WHO | sd` on 23 Aug 2026, which made
> an unusable session. ***THAT WARNING WAS ITSELF UNFINDABLE UNTIL 26 Aug
> 2026***: this sentence said §START HERE recorded it and §START HERE never
> did, so the grep the rule mandates returned only this pointer. **It is now a
> §6 trap**, which is where rule 4 says a trap goes.

> ***AND WHEN YOU CLOSE PART OF AN ENTRY, FIX ITS FIRST SENTENCE.*** Owner,
> 26 Aug 2026: *"i have been getting a different list of things left to do each
> time i ask"* — and *"step 14, I thought that decision had already been
> made"*. **He was right.** Four entries that day led with a superseded "still
> open" paragraph and carried their own correction further down; step 14 said
> *"WHAT IS STILL A DECISION, AND IT IS THE OWNER'S"* **338 lines above**
> *"STEP 14 IS CLOSED."* **A reader stops at the first status sentence**, so
> such an entry misleads everyone who does not read all of it — and three
> careful reads in one session each reported a different list because each
> stopped at a different line.
>
> **Run `python sdb_ai/sd64/gplbld/check-stale-leads.py` before answering
> "what is left".** It reports entries whose opening status claim is
> contradicted later in the same entry. It ranks for reading and does not
> decide; a hit can be a verb-phrase "done" in an entry that is genuinely open.
> **An entry may narrate "this was open, then it closed" — but it must say so
> FIRST.**

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
   Refactors, findings and traps do not. **Writing one no longer costs a
   cycle** — it is exempt from `assert-current` since 21 Aug 2026, header
   item 1 — so there is nothing left to weigh against obeying this rule.

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
- **Stage 2 - NOT BEING DONE, owner, 23 Aug 2026.** It read *"move to native
  Win32 and drop the `msys-2.0.dll` dependency"*. **Dropping MSYS2 was an
  assumed route to user isolation, not the objective**, and it is not required
  for it: Win32 calls work from an MSYS2 build and this tree already makes
  them. §7 step 13 has the survey, the four reasons, and what the one
  attempted leg cost. **The outcomes it was for are §7 steps 14 and 15.**

The client library is native Win32 already — see §5.3. **That is a property of
the client, not a staging post the server is travelling towards.**

## 2. Environment

**SETTING A NEW MACHINE UP IS A SCRIPT NOW, NOT THIS SECTION READ CAREFULLY:
`gplbld/setup-devbox.ps1`.** Elevated, idempotent, and safe to re-run — every
step checks before it acts. **`-CheckOnly` surveys a machine and changes
nothing, and needs no elevation**, which makes it the thing to run first on a
strange box.

```powershell
powershell -ExecutionPolicy Bypass -File setup-devbox.ps1 -CheckOnly
```

**IT RUNS BEFORE THIS REPOSITORY EXISTS**, so it reads nothing from the tree it
lives in and clones `sd4windows` itself. Fetch it alone with `curl.exe -fLo`
from the raw GitHub URL in its header.

It does **Git for Windows** and **GitHub CLI (`gh`)**, MSYS2, the pacman list,
**libsodium from source into `/usr/local`**, Inno Setup 6, the **four**
repositories as siblings, `sdb64`'s `origin/dev` fetch, and ends with **`make
sd` — because the build is the only real test of the environment**.

***`gh` IS INSTALLED ON THE OWNER'S INSTRUCTION, 23 Aug 2026, AND IT CUTS
ACROSS THE PARAGRAPH BELOW ABOUT MSYS2'S `git`.*** Both are recorded because
the two look contradictory otherwise. Nothing in the project calls `gh` — no
Makefile, no `gplbld` script — so by the "not a requirement, do not install
it" reasoning it would stay out. **What earns it a place is the one step this
script cannot do for anybody: the SSH key.** That is the step the first real
run died on, `gh ssh-key add` is the shortest way through it, and the script
had been *naming* `gh` in its advice while never installing it — which is the
worst of the three options.

***ONE THING IT DOES NOT DO, AND IT DOES NOT MATTER:*** it does not fetch
**`Projects\GPL.BP`**, which has no remote because it is a **convenience copy of
upstream**, not project material (§2, corrected 23 Aug 2026). A machine it
builds can build and test SD; for the attribution work, clone ScarletDME or
sdb64 rather than copying that tree across by hand.

**IT USED TO BE TWO. SSH KEYS STOPPED BEING A BLOCKER 23 Aug 2026** (owner's
decision, before the first clean-VM run). **All three GitHub repositories are
PUBLIC, so a key was only ever needed to PUSH** — and cloning over `git@` meant
a machine without one skipped `sd4windows` and `sdclilib32`, and skipped
**`make sd`** with them. So a bare machine could be set up to within one step
of the only thing that proves it. **Clones are `https` now**, and the script
sets the `git@` **push URL** afterwards with `git remote set-url --push`, so
nothing about pushing changes and no hand-editing is wanted. A key is now
needed the first time somebody pushes, and git explains that clearly by itself.

***MSYS2'S OWN `git` IS DELIBERATELY NOT IN THE PACKAGE LIST***, and the first
draft had it. `-CheckOnly` on the reference machine reported it missing — on
the machine that builds SD, ships installers and runs the whole suite. So it
was never a requirement: cloning is Windows `git` from PowerShell, and nothing
in the Makefile or `gplbld/*.py` shells out to git at all. **A setup script that
reports a working machine as incomplete teaches the operator to ignore it.**

***RUN ONCE, 23 Aug 2026, ON THE OWNER'S LAPTOP — AND THE LAPTOP WAS NOT A
FRESH MACHINE.*** §setup-devbox HAS BEEN RUN has the four defects it found and
what was done about each. What matters for this section:

- **Executed for the first time: the libsodium build (worked) and the Inno
  Setup install (found four defects between them).**
- **`diffutils` was missing from the package list** and is missing on this
  machine too, so the list is now 10.
- ***"STILL UNEXERCISED ANYWHERE: winget fetching MSYS2, and the pacman run"
  WAS TRUE WHEN WRITTEN AND IS NOT NOW.*** Corrected 24 Aug 2026. The clean-VM
  run later the same day **executed both for the first time and both worked** —
  8 packages including the new `diffutils`, and libsodium's configure printed no
  `cmp`/`diff` errors.

***THE CLEAN-VM RUN FINISHED ON THE THIRD ATTEMPT, 24 Aug 2026 — §7 STEP 17 IS
CLOSED.*** Attempt 1 (`DevInstallTest`, 23 Aug) died at `Step-Clone` on a PATH a
running process cannot see updated; attempts 1 and 2 on `DevEnvInstallTest`
(24 Aug) wedged the guest, which turned out to be the host's Hyper-V/NEM
fallback rather than anything in the script (§6). **Attempt 3 ran end to end,
exit 0, through `make sd`** — the clones, the build and the summary are all
now proven on a bare machine. §7 step 17 has the detail and the rig; §7 step 2
documents the VM. ***Still open there: the owner wants `sdhelp` INSTALLED, not
reported.***

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

**COMPRESSED 21 Aug 2026, thirty-eighth session**, under §0 rule 5 — the two
generation-2 audits and the `sdb64` dev-branch review are in HISTORY,
*"ARCHIVE 21 Aug 2026 - section 2's generation-2 audits and dev-branch
review"*, with what they found. What is below is the rule and what is still
live.

**THERE ARE THREE GENERATIONS, AND KNOWING WHICH ONE A LINE CAME FROM IS OFTEN
THE WHOLE ANSWER** (owner, 15 Aug 2026):

1. **`sdb64`** — <https://codeberg.org/stringdatabase/sdb64>, the unmodified
   Linux version and the active upstream project. **Cloned at `../sdb64`** with
   `main` checked out and `origin/dev` fetched, so both branches are readable
   without the network: `git -C ../sdb64 show origin/dev:sd64/<path>`.
   **Diffing against it is the cheapest way to attribute a surprise** — it is
   what settled §5.13 and §7 step 7.
2. **`sdb_ai`** — an experimental variant the owner produced by putting `sdb64`
   through **five AI cleaning and validation cycles**. This is why the code
   reads more cleanly than its age suggests, and why those cycles also
   introduce problems of their own.
3. **SD for Windows** — this repository, the port, built on top of `sdb_ai`.

**GENERATION 2 IS TAGGED IN THE SOURCE AND IS WORTH GREPPING FOR.** Every change
from the cleaning cycles carries a `Modified by Composer AI - 2026/06/10`
comment: **226 of them across 73 files**, all bearing that one date. **A line
with that marker is neither upstream nor port work**, so when something
surprises you, grep for the marker before treating it as intended, and check the
behaviour against `sdb64`. **Two have already cost real time** — the
`VALID_OS_PATH` trap in §6, and the `SH` administrator gate at
`GPL.BP/CPROC:3321`, which a session mistook for a Ladybridge decision it would
have been wrong to reverse. Several things this port has "found" turned out to
be inherited from generation 1 instead, so the check runs both ways.

**THE VERDICT OF THE TWO AUDITS, in one line each.** BASIC side: **the whole
validation layer is a generation-2 invention** — `!valid_os_name`,
`!valid_shell_cmd` and `!valid_os_path` do not exist upstream on either branch,
and neither do their call sites. C side: 206 markers over 53 files, **mostly
good** static-analyser hardening rather than policy, and **nothing there should
be reverted wholesale** — the BASIC side's verdict does not carry over.

**THE PATTERN TO CARRY FORWARD, which is the reusable half of both audits:**
generation 2's failure mode is **turning a loud failure into a quiet one**, and
once — in `op_openseq` — turning a success into a silent corruption. When a
marker adds a guard, the question is never "is the guard right" but **"what does
it do instead, and who can tell?"**

**WHAT IS STILL LIVE OUT OF THE TWO AUDITS:**

- **`!valid_os_name`'s charset is `A-Za-z0-9._-`, length 32 (`INT$KEYS.H:32`) —
  no backslash and no space**, so it rejects `DOMAIN\user` and any Windows name
  containing one. Benign where the name is one SD is about to *create*;
  **questionable where the name already exists** — `DELACC:240` and
  `MODIFYA:103/127` refuse to clean up or amend an account whose name it
  dislikes, leaving litter nothing can address.
- **AND IT IS STILL ON THE API LOGIN PATH — ANSWERED 21 Aug 2026: A SMELL, NOT
  A DEFECT.** `APISRVR:1180` applies it to the username inside the SCRAM
  exchange, before the credential is read (`goto scram.bad.cred`), and
  `SDCLIENT:279` does the same for remote logins. **A name it refuses can never
  have been an SD account**, for two independent reasons, so no legitimate login
  is lost:

  | | |
  |---|---|
  | nothing derives the name | `SDConnect()`'s `username` argument goes to `scram_login()` and straight into `n=%s` (`sdclilib.c:1049`). **No `GetUserName` anywhere in the client**, so a qualified name appears only if the application author writes one |
  | the client does not filter it | its only check is **length 1..32** (`sdclilib.c:1218`), no charset — so it does reach the server |
  | SD cannot register such a name | `valid_os_name` gates creation too: `CREATE_USER:79`, `CREATEA:537`, `CREATEA:1406` (ADOPT) |
  | SD cannot see domain accounts at all | `IS_USER:62` in its own words — *"LOCAL ACCOUNTS ONLY. Get-LocalUser does not see domain accounts"* — and `CREATE_USER` uses `New-LocalUser` |

  **MEASURED WITH ITS CONTROL — `verify-apiname`, 13/13 then 17/17; §4 has the
  row.** Four spellings refused, including **`name@computer`**, which matters
  because the UPN form is what a domain user is likeliest to type today.

  **WHAT THE REFUSAL COSTS IS DIAGNOSTIC, AND THAT WAS THE REAL FINDING.** To
  the caller it is still **indistinguishable from a wrong password** — same
  branch, byte-identical text — and that is deliberate. **The half that was a
  defect is fixed**: it used to write **nothing** to `audit`, and since 21 Aug
  2026 every refusal is recorded with a distinct `reason=`. §8 has it, closed.

  **A REAL DOMAIN ACCOUNT CANNOT BE PRESENTED ON THIS MACHINE**, and this is a
  trap rather than a task: GITORLI is in `WORKGROUP`, measured
  (`Win32_ComputerSystem.PartOfDomain` False). Same shape as §4's RDP entry —
  the reasoning is sound and the rig is absent. §7 step 2's VM is not a domain
  either, so proving it against a live domain account needs a rig nobody has.
  **The four facts above are what make that acceptable rather than owed:** SD
  cannot register, adopt or even see such an account, so there is no login being
  refused.
- **`!valid_shell_cmd` rejects `;|&$`, backquote and `<>`**, so **even an
  elevated `SH` cannot pipe or redirect** — `SH dir | findstr x` is refused.
  That is message 5240 in §4's `OS.USERS` table, and §7 step 7 lifts the ban for
  a listed account only.
- **FLAGGED, NOT FIXED — `dh_open.c:257`.** On `k_alloc` failure for the trigger
  name it silently opens the file **without its trigger**: `DHF_TRIGGER` never
  set, so writes bypass the trigger's validation. OOM-only, and the right remedy
  — `k_error()` like the ~15 other allocation sites, or failing the open —
  changes open-failure semantics. **Decide it deliberately rather than in
  passing.** The guard still contains a dead `if (p == NULL) { p = NULL; }`,
  re-read 21 Aug 2026.
- **`APISRVR` IS 2,147 CHANGED LINES ON `sdb64`'s DEV BRANCH**, mostly
  reformatting with real error checking inside it. Not taken: ours had already
  diverged and §7 step 6 owned it. **Step 6 is now closed and SCRAM has diverged
  it much further**, so this is a decision somebody can finally make — and the
  reason not to take it wholesale is unchanged, that the reformat would bury the
  port's own changes.

**Release identity was not taken either, and is now RULED.** Owner, 24 Aug 2026:
*"our numbering sequence is different than upstream, hence the W in front of the
number."* **`SD_REV_STAMP` is `W1.0-0` and does not track upstream** - the `W`
marks a separate sequence, so `sdb64` at `1.0-2` and dev at `1.0-3` are not
numbers to follow. Do not "catch up" the trailing digit; it would imply a parity
this port does not claim. (The C side is `MAJOR_REV 1`, `MINOR_REV 0`, `BUILD 2`
in
[gplsrc/revstamp.h:41-44](sdb_ai/sd64/gplsrc/revstamp.h:41); only the stamp
string differs from upstream, and deliberately.)

**The TCL verb surface is written down**, in [docs/TCL_VERBS.md](docs/TCL_VERBS.md)
— SD's commands against OpenQM 2.6.6, supplied by the owner 14 Aug 2026. Read it
before adding or renaming a verb. The structural fact it records: **SD has
accounts, not accounts and users.** `CREATE.USER`, `DELETE.USER`, `ADMIN.USER`
and `LIST.USERS` are all deliberately absent, which is why `CREATE.ACCOUNT`
provisions the operating system account itself.

### The sibling repositories, and what "in sync" means

**THE ARROW TURNED ROUND ON 19 Aug 2026 AND THIS TABLE USED TO HAVE IT
BACKWARDS.** `gplsrc/sdclilib/` is **the source of truth**; `winsdclilib` is a
mirror of it. It was the other way round until the 32-bit client shipped
without SCRAM in it — built from a `winsdclilib` that had not moved since
15 Aug, still sending the password in clear, with nothing in either project
able to report it. **One hop instead of two, so the middle copy cannot lag
again.** `gplsrc/sdclilib/VENDORING.md` was rewritten around the new direction
rather than deleted; read it before syncing anything.

| Path | What it is | Our duty |
|---|---|---|
| `../sdb64` | upstream Linux project, `main` + `origin/dev` | **read-only.** Fixes it needs go in [UPSTREAM_FIXES.md](UPSTREAM_FIXES.md) |
| `../winsdclilib` | **a mirror of `gplsrc/sdclilib/`**, not its source | **push to it** when the client changes here |
| `../sdclilib32` | the 32-bit `qmclilib.dll` for mvDeveloper. **Holds no source** — its `Makefile` `SRCDIR` points into this tree | build and test it after a client change |
| this repository | the port, and the client library's home | — |

**32-bit is a shipping constraint, not a test convenience** — mvDeveloper needs
it, and `qmclilib.dll` must stay a single file that can be copied beside an
application, which is what chose PBKDF2 over Argon2 for SCRAM.

***THE LINUX CLIENT IS REMOVED FROM THE PROJECT — owner, 23 Aug 2026.***
*"This build is windows only and I think the number of users that want to
connect from a linux client to a windows server are very small."* **Not cloned,
not synced, not a duty, and not in the table above.** ***The GitHub repository
is DELETED and the working tree is gone*** — `gh repo view` no longer resolves
it.

***IT IS NOT DISCARDED, THOUGH, AND THE REASON IS FORWARD-LOOKING.*** The owner
may advance **`sdb_ai` itself — the Linux base this port was built on — as its
own line, still separate from upstream `sdb64`** (§2, the three generations). A
Linux client belongs with that work rather than with this one. So it is
archived rather than abandoned:

**`C:\Users\dmont\Projects\linuxsdclilib.zip`, AND IT IS NOW THE ONLY COPY.**
**Verified restorable 23 Aug 2026**, not merely assumed: extracted to a scratch
directory, `git log` reads the full history with HEAD at **`f6ab707`**,
`git fsck` is **clean**, and the commit [UPSTREAM_FIXES.md](UPSTREAM_FIXES.md)
entry #2 cites is present. **84 entries, 61 of them `.git/`** — it is a
repository, not a source dump.

**AND IT IS COPIED TO pCloud** (owner, 23 Aug 2026), so it is not resting on
one disk.

***`Projects\GPL.BP` IS NOT EXPOSED, AND THIS SAID IT WAS.*** Corrected
23 Aug 2026 on the owner's word: it is a **copy he took from upstream so the
material was available locally**, and it is **throw-away - it can always be
fetched again**. The claim *"nothing here can recreate it"* was true only of
this repository and was written as though the tree were unique. §2 has the
detail and the measurement.

**AND THE TWO ENDS CANNOT TALK ANYWAY, measured 23 Aug 2026:** this port's
client sends **request 47** for SCRAM and upstream's dispatch table **ends at
46**; an upstream client sends **request 24**, which `APISRVR` marks *"RETIRED,
always refused"*. **No fallback in either direction, by design.**
[UPSTREAM_FIXES.md](UPSTREAM_FIXES.md) opens with what that costs.

***THE REASON IT WENT UNNOTICED IS THE PART TO KEEP, because the same hole is
still open elsewhere.*** It had stopped at **15 Aug** with **no SCRAM at all**
while this section claimed it was "kept in sync" — **the same date and the same
symptom as the 32-bit client that shipped sending passwords in clear.** That
was fixed by making `gplsrc/sdclilib/` the source of truth, "one hop instead of
two" — but that redirected the **Windows** mirror only. ~~**`sdclilib32` is still
two hops away and nothing compares it.**~~ ***BOTH HALVES ARE STALE, corrected
26 Aug 2026.*** `sdclilib32/Makefile:44` reads
`SRCDIR ?= ../sd4windows/sdb_ai/sd64/gplsrc/sdclilib` and its own comment at
:36 records the change — *"19 Aug 26 - REPOINTED FROM ../winsdclilib TO THE SD
FOR WINDOWS TREE"* — so it has been **one hop since the same day the mirror
was**. And [check-client-sync.py](sdb_ai/sd64/gplbld/check-client-sync.py) now
compares it, including a check that `SRCDIR` has not gone back via the mirror.
**The claim outlived its own fix by a week in the file that recorded the fix.**

**THE SAME CONSTANT LIVES IN A DOZEN PLACES ACROSS THESE TREES**, and that is
not hypothetical: it is how the `SV_EMSG_PAIR`/`SV_ECONTXT` transposition
survived from 5 to 15 Aug 2026 in three repositories at once. **Before changing
any shared constant, grep them all:**

```sh
grep -rn "define SV_" ../sdb64 ../winsdclilib ../sdclilib32 . \
    --include=*.h --include=*.bi --include=*.c
```

**AND THE SAME SWEEP IS WORTH RUNNING FOR A FEATURE, NOT ONLY A CONSTANT** -
`grep -rli scram` over those trees is what found the Linux client three
phases behind, in one second, after eight days of nothing noticing.

**THAT TRANSPOSITION IS SETTLED AND THIS SECTION CARRIED IT AS OPEN FOR SIX
DAYS.** All four trees now read `SV_EMSG_PAIR=6, SV_ECONTXT=7`, `sdb64` was
right all along, and the fault was `winsdclilib` `13e4bf5` introducing the pair
reversed in a commit titled *"Align Windows client error handling with Linux"*.
Fixed in `winsdclilib` `a1987b0` and independently here, both on 15 Aug 2026.
**[UPSTREAM_FIXES.md](UPSTREAM_FIXES.md) #2 is CLOSED — nothing to send** — and
it keeps the method that settled it, which is the part worth re-reading before
anyone re-opens the question. *Three claims struck here 21 Aug 2026: that the
values are still transposed, that `sdsys/syscom/sdclilib.h` "deliberately
defines neither" (it defines both, at `:127`), and that our BASIC therefore
cannot tell a transport failure from a context error.*

***THE COMMAND DOCUMENTATION IS AT `C:\Users\dmont\Projects\sdhelp`, AND THIS
SECTION DID NOT MENTION IT UNTIL 24 Aug 2026.*** 783 HTML files, one per verb,
keyword and BASIC statement. **Read it before inferring a verb's syntax from
its BASIC source** — it settled three questions in one session: `copy.htm` says
outright that `BINARY` *suppresses* the field-mark/newline translation between
a hashed and a directory file, which is what made the `COPY` route in §7 step
14 safe to build; `create_file.htm` says `PATHNAME` names a directory the file
is created **under**; and `csv.htm` claims RFC 4180 conformance, which turned
§7 step 16(b) into a testable gap rather than a preference. Strip the tags to
read it: `sed -e 's/<[^>]*>//g' <file>.htm`.

***IT IS TRUSTWORTHY FOR SYNTAX. THE DELTA IS REMOVED COMMANDS — owner,
24 Aug 2026:*** *"other than some removed commands, the tcl and basic
definitions are right."* It is an OpenQM 2.6.6 base **partly modified for the
Linux SD**, so it is not stock OpenQM documentation — but the definitions
themselves are correct, and the failure mode is a page describing a command
this port no longer has, which announces itself the moment the command is
tried. *An earlier draft of this entry called it untrustworthy page by page;
that was an over-correction and is struck.* **Confirm against source when the
answer decides a cycle** — `COPY:220-229` was checked before `copy.htm` was
relied on — and remember this tree has removed verbs since (§5.19 `SED` and
`UPDATE.RECORD`, SDNet's three `*.SERVER` verbs) and that `CREATEF`'s own doc
comment is stale in a way that cost run `b22`.

***MEASURED 25 Aug 2026 WHILE WRITING THE SAMPLE PAGE: THE DELTA IS NOT ONLY
WHOLE VERBS. IT IS KEYWORDS INSIDE A VERB THAT STILL EXISTS.***
`create_file.htm` documents `ENCRYPT keyname`; `gpl.bp/CREATEF` contains **no
reference to encryption at all** — 0 hits — so the token falls through the
keyword `case` to `CREATEF:251`, `stop sysmsg(2018, token)`, *Unexpected
token*. Its see-also names `CREATE.KEY` and `ENCRYPT.FILE`; neither is in
`sdsys/voc_template`. `KW$ENCRYPT` is defined at `syscom/PARSER.H:226` and used
by nothing, and `voc_template/encrypt` is the type-K record for it. **Not ours
and not a defect** — `../sdb64`'s `CREATEF` has 0 hits too, so encryption went
when OpenQM was GPL'd, and there is nothing for UPSTREAM_FIXES. **It is the
documentation that is stale, and only a page-by-page pass against source finds
the rest.** The reverse also happens, which is why the pass has to go both
ways: `CREATEF`'s own header comment says `DIRECTORY path` where the real
keyword is `PATHNAME` (`CREATEF:183`) — there, the help page is the one that is
right. Two other pieces of the sample checked out against source: the `.dic`
suffix is lower case on a real install (the page says `.DIC`), and `pathname`
requires an existing directory (`CREATEF:191`, sysmsg 6110).

***AND THE COMMAND LISTS THAT SAY WHAT STILL EXISTS ARE IN THE `sdb64` CLONE
ALREADY*** — `../sdb64/sd64/Documentation/`, two files, found 24 Aug 2026:
**`Basic Command List SD 0.8.0.txt`** (520 lines) and **`TCL Command List SD
0.8.0.txt`** (212 lines). Both head with *"usage the same as OpenQM 2.6.6"* and
mark commands **unique to SD with `*`**. **That is the natural companion to
`sdhelp`**: the HTML gives the syntax, these give the roster. Between them they
answer the "removed commands" caveat above without guessing.

***PROVENANCE, CORRECTED 24 Aug 2026: THE `C:` COPY IS A COPY.*** Owner: **the
upstream copy carries all the modifications**, and `C:\Users\dmont\Projects\
sdhelp` is a copy of that — so it is **not** unique material, and an earlier
draft of this entry saying it "carries modifications that exist nowhere else"
was wrong. **It is NOT in the `sdb64` clone**, measured: that repository holds
no `.htm` at all, only the two `Documentation/` lists above. So it cannot be
fetched from the tree we already clone.

**RULED 24 Aug 2026.** Owner: *"we do not care about sdhelp_2-6-6 other than
when it helps us write documentation. However setup devbox should include the
whole `..\sdhelp` tree, as the documentation process may happen on another
computer and I want those resources handy."*
**`setup-devbox.ps1` now has a `Step-SdHelp`**: `-SdHelpSource <path>` copies the
tree to `<Root>\sdhelp` and verifies the file count; without it the tree is
reported as a hand-carry item beside `Projects\GPL.BP` rather than passed over
in silence. **It is not cloned and not vendored** - 30 MB of third-party PDF and
HTML, and this repository takes no binaries.

***THE RULING ABOVE WAS WITHDRAWN BY THE OWNER ON 24 Aug 2026 AND THIS IS THE
CURRENT POSITION.*** Seeing the first end-to-end run he noted `sdhelp` did not
install and said he wanted it installed; hours later he cancelled the request:
*"cancel the sdhelp request - I will just download it from my P drive if
needed."* **So a machine built by this script deliberately does NOT have the
tree, and that is accepted.** The `Step-SdHelp` report is the whole of what is
wanted. `-SdHelpSource` has never been run and does not need to be.

**Do not re-derive the original ruling from the quote above and reopen this.**
The quote is kept because it explains why `Step-SdHelp` exists at all.

**Local shape:** not a repository — no `.git`, no remote — and
`setup-devbox.ps1` does not fetch it, **so a machine built from that script
will not have it**. It is unpacked from `sdhelp_2-6-6 20260221 AM.zip`
(1.87 MB) or the matching `.7z` beside it in `Projects\`. **The backup on
pCloud is that archive, under that name** — `sdhelp_2-6-6 20260221 AM` — which
is the proper name of the set; the `sdhelp\` directory is just the unpacked
convenience. *(An earlier draft said the pCloud name was unknown.)*

***IT HAS A FUTURE ROLE — owner, 24 Aug 2026: it is the material from which SD
for Windows' own documentation will eventually be written.*** That is why it is
kept rather than re-fetched, and it is worth knowing before anyone treats it as
disposable the way §2 records `Projects\GPL.BP`.

Three more local trees, none part of this repository, all absent on a fresh
machine, and nothing in the build depends on any of them:

- **`C:\Users\dmont\Projects\gplsrc`** — original GPL ScarletDME C source.
  Limited value: Ladybridge stripped the Windows code thoroughly. Still useful
  for recovering text mangled by the `qm`→`sd` rename.
- **`C:\Users\dmont\Projects\GPL.BP`** — original ScarletDME BASIC source, 212
  files. **A LOCAL CONVENIENCE COPY OF UPSTREAM, AND THROW-AWAY** — owner,
  23 Aug 2026: he copied it here so the material was available without a
  network round trip, *"it is not a part of this project and ... can always be
  retrieved from other projects"*. **It needs no backup and no remote.**

  ***IT HAS ANSWERED A REAL QUESTION ONCE, WHICH IS THE ARGUMENT FOR KEEPING
  IT TO HAND.*** §7 step 16's resource note: `SETPTR`'s `NEWLINE CR|LF|CRLF`
  keyword is in this tree, and finding it showed that Ladybridge's answer to
  line endings was a per-print-unit setting rather than a compile-time
  constant — and that the mechanism is still in our own tree, unstripped.
  **The C sibling yielded nothing on the same question**, so search the BASIC
  first when the question is about behaviour rather than plumbing.

  **It is still the thing to READ** when the question is what the port removed:
  it retains real Windows code that this repository's `sdsys/gpl.bp` had
  stripped, which is what §7 step 12 worked from. See §5.4.

  ***WHERE IT COMES BACK FROM, MEASURED 23 Aug 2026 RATHER THAN ASSUMED:***
  **`../sdb64` is NOT a superset.** Its `sd64/sdsys/GPL.BP` holds 214 files
  against this tree's 212, **176 names in common and 36 absent** — `_login`,
  `_banner`, `accrst`, `accsve`, the `.SCR` screens. Those 36 come from
  **ScarletDME on GitHub**, the older project sdb64 succeeded. **Re-fetching
  means both, not just the Codeberg clone.**

  **AND IT IS A DIFFERENT TREE FROM `sdsys/gpl.bp`, WHICH IS EASY TO ASSUME IT
  IS NOT:** 212 files against 200, 170 shared names, and **not one of the 170 is
  byte-identical**. 42 exist only here, 30 only in the repository.
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

**COMPRESSED 21 Aug 2026, thirty-eighth session**, under §0 rule 5. The section
as it stood — every measurement with the reasoning that produced it — is in
HISTORY, *"ARCHIVE 21 Aug 2026 - section 4's measurement record"*. Nothing was
deleted, and the three corrections made on the way are noted where they belong.

### 4.0 The verifier inventory — count the directory, and which are actually run

***COUNT CORRECTED 24 Aug 2026: `ls verify-*.ps1 | wc -l` says **30**.*** It
said 28 earlier the same day, where the heading said 27 and the paragraph below
said 26. The additions since are `verify-lineendings` (§7 step 16 (a)) and
**`verify-sysdiracl`** (§7 step 15's second guard, in `VerifyInstall1` beside
`verify-pcodeacl`). The two that were never added here are
**`verify-apiidentity`** (§7 step 14 — measured for the first time on 24 Aug,
run `b28`, and it FAILS on a real product finding) and **`verify-pcodeacl`**
(§7 step 15). All are on `$neverShipped`. **Count the directory rather than
trusting this line** — it has now been wrong three times, in both directions,
which is what the rule below exists to stop. The heading no longer carries a
number for the same reason.

***THERE ARE ALSO TWO NON-VERIFIER TESTS, AND NEITHER IS IN A RUNNER.*** The
second is `gplbld/test-verdict-units.ps1` (24 Aug 2026): it lifts the
`Write-Verdict` function out of **both** `verify-createaccount.ps1` and
`verify-sshonly.ps1` by AST, checks all four cases including the two null ones,
and **asserts the two copies are byte-identical**. Unelevated, no SD, no
account, no install — run it after editing either verifier. The first is
`gplbld/test-apiidentity-units.ps1`. It unit-tests `verify-apiidentity`'s two
helpers by lifting them out of that script **by AST**, so it cannot drift from
what it tests. Unelevated, no SD, no account, no install, touches only
`%TEMP%` — it makes no claim about the installed tree, which is why it is not
named `verify-*` and spends no prefix. **Run it after editing that verifier**:
both cases it covers are bugs that were paid for in real runs (§6's WHO-pattern
and `icacls`-ordering traps).

**WRITTEN 22 Aug 2026 BECAUSE THE SET HAD NEVER BEEN WRITTEN DOWN.** There are
**28** `verify-*.ps1` in `gplbld` — 24 when this was written, plus
`verify-notyet`, `verify-parsertokens` and `verify-batchjob`, less
`verify-editkeys`, removed 23 Aug with the editors it tested. `post-cycle-elevated.ps1` ran **nine** of
them, and the other fifteen were reachable only by remembering they existed.
**Three of the twenty-four — `verify-scramlogin`, `verify-setpw`,
`verify-tierapi` — were not named anywhere in this file at all**, so a session
reading the handoff could not have known to run them. That is exactly what
happened to `verify-delaccount`, which went a whole phase unrun; the difference
is that this list makes the next one visible instead of waiting for it to be
missed again. **Add a row here in the same commit that adds a verifier.**

**ALL 26 ARE ON `assert-current`'s `$neverShipped` LIST** — checked by name,
22 Aug 2026, not by eye: two earlier attempts to audit this by grepping a line
range and by regex both reported files missing that were not. Grep for
`'<name>'` **quoted**, or the answer is wrong.

**Run after a cycle, elevated — `post-cycle-elevated.ps1`, SEVENTEEN steps since
22 Aug 2026**, in this order, which is not arbitrary:

```
fold  nonet  createaccount  tiers  catgate  osusers  accountacl  routes
accountrules  delaccount  sshonly | peerlog | apiadmin  apiname  apiport
scramlogin  tierapi
```

**The two bars are the two ordering constraints.** Everything left of the first
can leave a diagnosis in the SD error log, and `verify-peerlog` **overwrites**
that log with synthetic records to make the trim fire. Everything right of the
second edits `APIPORT` in the installed `sd.conf` and restarts SD, so none of it
is talking to the server the earlier steps measured. `verify-nonet` is first
because it is static and cheap: a tree that is not what the cycle left says so
before twelve throwaway accounts exist.

**Thirteen prefixes, one token: `-Run`.** The header has the invocation and the
collision guard.

**BOTH RUNNERS NOW REFUSE IF SD IS NOT RUNNING, added 22 Aug 2026 after it cost
a run.** `assert-current` **does not answer that question** and cannot: it
compares hashes and mtimes, so a **stopped** server is perfectly "current". The
service had been stopped to clear a stale user table and not started again;
`verify-fold` printed *"assert-current: the installed tree matches source"* and
then died on its first SD command with *"SD has not been started"*. **A green
line immediately above a failure is the worst possible reading order**, and at
seventeen steps each one would have found out separately, leaving accounts
behind on the way. Both runners check the **service and an `sdwind` process** —
not the service alone, because `sdsvc.log` shows it reporting RUNNING while it
waits five seconds to see whether `sdwind` stays up. **Neither starts it**:
`cycle.ps1` owns that, a stopped SD after a cycle is itself diagnostic, and the
unelevated runner could not start a service anyway.

**Run after a cycle, UNELEVATED — `post-cycle-unelevated.ps1`, NEW 22 Aug 2026,
and it spends no prefixes at all:** `verify-credacl`, `verify-nocase`,
`verify-setpw`, `verify-allowgroups`, `verify-keys`, `verify-lcnames`,
`verify-parsertokens`, `verify-batchjob`. Nothing there creates a Windows
account, so unlike the
elevated runner it is free to re-run.

```powershell
C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\post-cycle-unelevated.ps1
```

**IT REFUSES AN ELEVATED SHELL, AND THAT IS LOAD-BEARING.** `verify-credacl`
asks whether an **ordinary** user can read or write `sdsys\$cred`;
`secure-cred.ps1` grants `Administrators` Full, so an elevated run would pass
every check **and prove the opposite of what the file claims**. A test that
passes for the wrong reason is worse than one nobody runs, because it is
believed. `verify-osusers` refuses for the same class of reason — *"CPROC admits
`K$ADMINISTRATOR` whatever `OS.USERS` says"*.

**RUN THIS ONE FIRST, BEFORE THE ELEVATED RUNNER.** Measured 22 Aug 2026 in the
harder direction — *after* the 17-step elevated run had already churned the tree
— and **all 8 exited 0**, so either order works. First is better for two
reasons: it measures the tree closest to what the cycle left, before sixteen
steps of account, `sd.conf` and service churn; and `verify-lcnames`, the file
§8's intermittent has always been about, gets the cleanest tree it can. Nothing
here depends on anything the elevated runner creates — all eight use `$cred`,
`OS.USERS` and the installing user's own account, which the **install** provides.

| step | 22 Aug result |
|---|---|
| `verify-credacl` | PASSED |
| `verify-osusers` | **PASSED** — *"OS.USERS grants a shell, and takes it away again"*. **First result since the 16:38:01 install**, and it only ran at all because it moved out of the elevated runner |
| `verify-nocase` | PASSED |
| `verify-setpw` | PASSED |
| `verify-allowgroups` | all checks passed |
| `verify-keys` | 10/10 |
| `verify-editkeys` | 14/14 |
| `verify-lcnames` | **142/142** — the intermittent did **not** recur |

**IT IS NOT UNATTENDED, AND THE HEADER OF `verify-osusers` UNDERSTATES BY HOW
MUCH.** That file says it *"will prompt for the elevation it needs, twice"*. It
has **one** `-Verb RunAs` call site (`:559`) but **three** phases in its
`ValidateSet` — `Grant`, `GrantOsx`, `Revoke` — and the owner counted the
prompts on the day: about three from it. **Expect to click.** It is second in the
list so the clicking is over early rather than after five silent minutes.

**IN NEITHER RUNNER: NONE, SINCE 22 Aug 2026.** The eight that were out are all
in the elevated runner now, and **none was deleted** — owner's instruction was
*wire it in or delete it*, and each of the eight was read before being judged.
Every one guards a claim no other verifier makes:

| verifier | the claim only it makes | was |
|---|---|---|
| `verify-nonet` | SDNet is gone and its neighbours are not | `gcat` 132 → 129 |
| `verify-catgate` | the **global** catalogue needs administrator rights by every route (UPSTREAM_FIXES 7) | 25/25 |
| `verify-osusers` | the `SH`/`OS.EX` truth table — the middle two rows prove the fields independent | 24/24, **16:38:01 install** |
| `verify-sshonly` | the ssh-only model end to end, incl. a **real ssh login** | 13 checks |
| `verify-apiname` | `!valid_os_name` refuses a qualified name, indistinguishably, **and it is audited** | **17/17**, 22 Aug |
| `verify-apiport` | the two API gates answer **differently** — wrong password vs `ACC$GROUP` | `sdapi4` |
| `verify-scramlogin` | the SCRAM wire exchange against the **RFC**, replay and nonce reuse refused, request 24 refused | *no recorded result* |
| `verify-tierapi` | all three tiers reachable over the API, and one that should not be, refused | *no recorded result* |

**THE TWO SUPERSESSION CLAIMS I EXPECTED TO FIND BOTH FAILED.** `verify-apiport`
looked obsolete — Phase 1 made `APIPORT` ship active and that script turns the
port on and off — but **it was updated for exactly that on 21 Aug** (*"PUT BACK,
NOT REMOVED AGAIN"*), and `verify-apiadmin` measures containment, not the gates.
And `verify-sshonly` overlaps `verify-createaccount`'s three logon measurements
but is five times the size and does the real `ssh`. **Nothing here was dead
code.**

**THEY ALL RAN, 22 Aug 2026, `-Run b1` — 12 of 17 clean, and the five failures
were worth every minute.** `verify-scramlogin` **40/40** and `verify-apiport`
all-checks are **first recorded results ever**; `verify-tierapi` 15/16 and
`verify-catgate` 25/25.

| step | outcome |
|---|---|
| `verify-osusers` | exit 2, **measured nothing** — it *refuses* an elevated window. **My error**: it was classified by grepping for `WindowsBuiltInRole`, which it mentions in a gate that **refuses** rather than requires. Moved to the unelevated runner. **Read the branch, not the symbol.** |
| `verify-nonet` | 16/17 — `CT VOC UNLOCK shows a V type code` wanted `^\s*\d*\s*V\s*$` and SD prints **`1: V`**. **The colon was missing, so it had failed every run since it was written.** `verify-lcnames:767` had it right all along. Fixed |
| `verify-tierapi` | 15/16 — `bound to 127.0.0.1 only` **expected `$false` of an expression that asks "is it 0.0.0.0"**, so it failed *because the server was correct*. **Posture B left behind**, which Phase 1 reversed on 21 Aug. `verify-apiport` asked the same question the right way round two steps earlier and got the opposite answer — **that disagreement is what makes it a test bug and not a finding**. Fixed |
| `verify-fold` | exit 2 — `CREATE.FILE ZZUCFOLD1` met *"DATA part of file already exists"*. **Residue from two interrupted runs**, not a defect. Clear it with `verify-fold.ps1 -Cleanup` |
| `verify-sshonly` | ***exit 0, 15 PASS, 0 FAIL — CORRECTED 24 Aug 2026 on the `b36` run.*** This row said *"exit 1 — OPEN, and the owner's call"*, that every `ssh` attempt was refused **including the control**, and that the test asserted a premise the product no longer had. **It passes**: `ssh-only: LogonUser INTERACTIVE` refused 1385, `NETWORK_CLEARTEXT` and `NETWORK` admitted, ssh admitted with a password **and** with a key, and still admitted with the account also in `Users`. Whatever the 21 Aug failure was, it is gone; the row was never re-checked after it |

**THREE OF THE FIVE WERE FAULTS IN THE TESTS OR IN MY WIRING, NOT IN SD**, and
two of those had been failing silently for as long as they had existed —
which is the argument for the inventory above in one line.

### 4.0.2 The suite CANNOT be run from the installer, and the reason is structural

**ASKED 22 Aug 2026: can `VerifyInstall1` be made part of the install, so the
installer reports a result straight after installing? NO — not this suite, and
not by wiring it in.** The blocker is not effort:

1. **`assert-current.ps1` compares the installed tree against the SOURCE tree**
   — `bin\sd.exe`, `gplsrc`, `sdsys`, all under `sdb_ai\sd64`. **Nearly every
   verifier calls it first.** An end-user machine has no source tree, so it
   exits 2 with *"no bin/sd.exe - run make sd"* before any check runs. The suite
   answers *"does the install match what I just built"*, which is a **developer's**
   question and is meaningless on a machine that built nothing.
2. **13 of the 24 need MSYS2, `gcc`, `make` and the repository Makefile** —
   `verify-apiadmin`, `verify-apiport`, `verify-apiname` and `verify-scramlogin`
   compile C probes at run time. `verify-tierapi` additionally needs
   `sd-connect.exe` from the **separate `sdclilib32` repository**.
3. **None of the verify scripts is shipped.** `stage.py` ships a named list;
   they are not on it, and they are on `$neverShipped` precisely because they
   cannot reach an install.
4. **It is aggressive for a user's machine**: it creates and deletes Windows
   accounts, restarts the SD service, and plants synthetic records in the error
   log. Directly after an install, on somebody else's computer, that is not a
   self-test — it is a second installer.
5. **It needs about four UAC approvals and several minutes**, and the installer
   runs its steps through `Exec` with `SW_HIDE`, where nothing can answer.

**WHAT WOULD ACTUALLY WORK IS A DIFFERENT ARTEFACT**, and it is worth building
when somebody wants it: a small **post-install smoke test** using only the
installed tree — SD starts, a session opens, the installing user's account was
adopted, `$cred` and `gcat` carry the right ACLs, the API port is listening.
**11 of the 24 already need nothing but the installed tree**
(`verify-fold`, `verify-nonet`, `verify-tiers`, `verify-routes`, `verify-setpw`,
`verify-nocase`, `verify-keys`, `verify-editkeys`, `verify-credacl`,
`verify-allowgroups`, `verify-sshonly`) — but each still calls `assert-current`,
so they would need that call made conditional before any of them could ship.
**Not started; recorded so the next session does not rediscover the blocker.**

### 4.0.1 An agent shell can elevate ONLY DIRECTLY — the suite's own elevations are refused

> ***CORRECTED 23 Aug 2026, AND THE SECTION BELOW IS TRUE ONLY OF THE SIMPLE
> CASE.*** Two attempts to run `-Run b16` from an agent shell were lost to
> this, so it is stated before the older text rather than after it.
>
> | what elevates | result |
> |---|---|
> | **`Start-Process -Verb RunAs` issued DIRECTLY by the agent's shell** | **WORKS** — measured 4× on 23 Aug: `probe-s4u` twice, `cycle.ps1`, and killing a hung `sd.exe` |
> | **the same call made by a verifier the agent launched** | ***REFUSED*** — `verify-osusers`: *"elevation for Grant did not happen: The operation was canceled by the user"*, **with no dialog shown to the owner** |
> | the whole suite launched as a BACKGROUND task | ***HANGS FOR EVER*** — `verify-batchjob` printed *"A UAC PROMPT IS COMING"* and stopped; **no `consent.exe` ever existed**, and the run sat 10 minutes with no output |
>
> **SO THE 19 Aug CLAIM WAS RIGHT ABOUT THE SUITE AND WRONG ABOUT THE MECHANISM,
> and the 22 Aug correction below was right about the mechanism and wrong to
> generalise it.** *"The operation was canceled by the user"* with **nobody
> having been asked** is the signature; a nested launch has no desktop to put
> consent on, and the owner sees nothing at all.
>
> ***THE PRACTICAL RULE IS UNCHANGED AND IS THE ONE TO FOLLOW: THE VERIFY SUITE
> IS RUN BY A PERSON, FROM THEIR OWN ORDINARY TERMINAL.*** An agent may run
> `cycle.ps1` and one-off elevated commands; it may not run `VerifyInstall1`.
> **Do not spend a `-Run` token finding this out again.**
>
> **NOTHING IS LEFT BEHIND WHEN IT FAILS THIS WAY** — checked 23 Aug: no `b16`
> user or `sdu_` group, no `os.users` record, `batch.jobs` empty, no stray
> `sd.exe`. `verify-osusers` says so itself: *"Nothing was measured and nothing
> was left behind."* **So the token is NOT spent and can be reused.**

### 4.0.1a The older entry, kept because its measurement was real

**MEASURED 22 Aug 2026, twice, and it contradicts a claim this file has acted on
since 19 Aug.** `post-cycle-elevated.ps1`'s header says an agent shell cannot
raise a UAC prompt — *"`Start-Process -Verb RunAs` returns 'The operation was
canceled by the user' without ever showing one, because a detached process has
no desktop to display consent on"* — and **that is why the elevated verifiers
have to be started by a human.**

From an **unelevated** agent shell, `Start-Process powershell -Verb RunAs -Wait
-PassThru` returned **exit 0**, and the child reported **`user=GITORLI\don
elevated=True`** while the parent reported `elevated=False`. It was then used
for real: `verify-fold.ps1 -Cleanup`, exit 0, which cleared the `ZZ*FOLD*`
residue.

***ANSWERED THE SAME HOUR, BY THE OWNER, AND THE FIRST ANSWER WAS WRONG.*** This
entry said *"either UAC is configured not to prompt for this account, or
something changed since 19 Aug"* and offered no way to tell. The owner supplied
it in four words — **"I got three uac prompts"** — so:

**UAC PROMPTS NORMALLY. IT IS NOT SILENT.** What actually happens is that
`-Verb RunAs` from an agent shell **raises a real consent dialog on the owner's
desktop**, and the elevation succeeds **because a human approves it**. The
19 Aug claim is wrong about the mechanism — the prompt *does* show — but its
practical conclusion survives intact and matters more than the correction:

**AN AGENT CAN START AN ELEVATED CHILD; IT CANNOT DO SO UNATTENDED.** Every
`-Verb RunAs` costs somebody a click. Two were spent before anyone realised —
a probe and `verify-fold.ps1 -Cleanup` — with no warning given that they would
interrupt. **Say so before elevating.** A suite that silently demands consent
five times is worse than one that asks for a command.

**WHAT WAS NEARLY RECORDED INSTEAD is the lesson.** *"UAC must be configured not
to prompt"* was a plausible reading of a true observation, it was about to go
into this file as a hypothesis, and it was wrong. The evidence that settled it
was on the owner's screen the whole time and invisible from here. **When a
measurement has a half that only a human can see, ask before writing the
conclusion.**

**DO NOT COLLAPSE THE TWO RUNNERS.** The unelevated half must keep a genuine
ordinary token whatever happens here — that is why `verify-credacl` and
`verify-osusers` refuse elevation — and `verify-osusers` prompts twice on its
own, which is most of the three.

**ALL SEVEN UNELEVATED VERIFIERS RAN 22 Aug 2026 ON THE 08:32:03 INSTALL**, most
of them for the first time in this file's memory:

| verifier | result |
|---|---|
| `verify-credacl` | PASSED — an ordinary user can neither read the DACL of `sdsys\$cred` nor create a record in it |
| `verify-nocase` | PASSED, 3 decisive — directory file `FL$NOCASE` 1, dynamic file 0, `SYSTEM(91)` 1 |
| `verify-setpw` | PASSED, 4/4 — `MODIFY.PASSWORD DON somethingextra` refused with 5276, and the control without the token reaches the prompt |
| `verify-allowgroups` | all checks passed — apply is idempotent, removal is an exact inverse, four foreign-policy shapes refused |
| `verify-keys` | 10/10 — DEL and Ctrl-H both erase, LEFT/RIGHT both move, with the no-erase and no-arrow controls |
| ~~`verify-editkeys`~~ | **STRUCK 23 Aug 2026 — `SED` and `UPDATE.RECORD` were removed, so this row's subject is gone and the verifier with it (§5.19). It read 14/14. Kept struck rather than deleted because the measurement was real and HISTORY, 19 Aug, explains what it found** |
| `verify-lcnames` | **142/142 at 08:52**, then 135/142 — see §8's intermittent, which this is |

**`verify-lcnames` IS THE ONE TO DISTRUST OF THE SEVEN.** The other six are
short, and each ran once and cleanly. It is the only one long enough to have hit
the intermittent, and it is the verifier the intermittent has always been about.

### Verified by observation

**A row is claim and decisive measurement, and nothing else.** Every one has a
HISTORY entry carrying how it was found and what it cost; go there when a row
looks surprising. The header carries the suite's **current pass counts** and
they are not repeated here (§0 rule 3).

**A ROW IS EVIDENCE ABOUT THE INSTALL IT NAMES AND NOTHING SINCE.** The current
install is **25 Aug 2026, 17:17:57** (`sd.exe` `275CFB03E142AA2C`, unchanged
since 24 Aug because no C has changed — the hash is not evidence that anything
else is, and the mtime comparison is what settles the rest). Dating the tree
before believing a result is §6's most expensive lesson. *(This paragraph named
the 22 Aug 22:50:18 install until 25 Aug 2026; it had gone stale across three
installs, in the section this file calls its most useful.)*

| claim | when | measurement |
|---|---|---|
| **The whole suite passes on everything the fifty-seventh session built** | 25 Aug, 17:17:57 install | `VerifyInstall1 -ThenElevated -Run b41` — **12 unelevated + 19 elevated steps, all exit 0**, **979 `PASS`**, and the eight failure-shaped lines each read and benign. `assert-current` clean on every section: rename walk, B3 over **six** mirrors / 2,951 files, B4 25 checked, nothing newer. Installer `sd-setup-W1.0-0.exe` 4,818,601 bytes. **Does NOT cover the upgrade path** (gated on `DataTreeUpgrade`, this was a first install) **or the stand-alone install** (no suite step chooses it — all 31 ran the full installation) |

**WHY SO MANY ROWS NAME A CONTROL, stated once instead of in each of them.** A
refusal proves nothing on its own: a gate that refuses everything, a filter that
copies nothing, a lookup that matches anything and a check that never ran all
produce the expected answer. Where a row names a control, that control is the
reason the row is evidence — **do not drop it when re-running the measurement.**

#### The account verbs

| claim | install | measurement, and its control |
|---|---|---|
| **`CREATE.ACCOUNT` makes both halves, and its ssh-only branch holds** | 14 Aug `sdacct2`, 16 Aug `sdacct9` | 16 of 16. Windows account, `sdusers`, `sdu_`, `sdsshonly`, not `Administrators`; account directory, VOC, private catalogue, `ACCOUNTS` record. Then three logon measurements **on an account SD created with a password SD set**: `LogonUser` INTERACTIVE **refused 1385**, NETWORK_CLEARTEXT **admitted**, real `ssh` **admitted** |
| **`DELETE.ACCOUNT`, both directions, the profile, and the `$adopt` marker** | 21 Aug, 17:18:11 | `verify-delaccount -Prefix sddel4`, **40 of 40 with 0 N/A — every `Note` in the file fired**, which is the claim the count carries and `sddel1` (37) and `sddel2` (38) could not. SD made it → account, `sdu_`, register record, directory and **both halves of the profile** gone; SD borrowed it → `10036`, Windows account and profile untouched, SD side gone anyway. One Y/N each way, sentinel `5051` proving nothing else ate the input |
| **Which `DELETE.ACCOUNT` branch fired is established by state, not by the message** | 16 Aug `sdacct14` | Only `case sd.made.it` deletes the Windows user; 10036 leaves it, 10037 means it never existed. Directory mtimes land in `DELACC`'s own order with `ACCOUNTS` **last**, which is the ordering that leaves a failed run re-runnable |
| **`MODIFY.ACCOUNT`, and remote access is absolute rather than additive** | 21 Aug, 17:18:11 | `verify-routes -Prefix sdrt6`, six calls. **Step 4 is the only check that separates the two**: `MODIFY.ACCOUNT x API` on an account created `SSH` must leave the routes `api` **alone**. An additive build passes every other check in the file |
| **Every refusal path in `CREATE.ACCOUNT`** | 21 Aug 17:18:11, re-run 22 Aug 08:32:03 | `verify-accountrules`, `sdar3` then `sdar6` at **34/34**. Each leg refuses and then makes **the same account** with the one thing that was missing — the control, because *"nothing was created"* passes just as happily on a build that never creates anything. The password failure is provoked with **two different passwords**, not a weak one (`SET_PASSWD:100`), and the unwind is measured on all four traces |
| **`GRANT`, `REVOKE` and `LIST.GRANTS`** | 15 Aug 16/16, re-run 16 Aug on a fresh install | Every SD-side claim checked against `Get-LocalGroupMember` afterwards, which is the point of the step: SD writes nothing to its own record. The idempotent paths say so rather than implying they acted. `LIST ACCOUNTS` still works with the `Granted to` column gone |
| **`ADOPT`, and the lockout fix** | 15 Aug | `ADOPT sdadopt1` printed *"keeps the Windows sign-in rights it already had"* and left `sdsshonly` unchanged — against `don`, whom the same verb had restricted minutes earlier. **The trap and the rule behind it are §6** |
| **`ADOPT` is refused without a marker, and the marker names ONE account** | 22 Aug, 08:32:03 | `verify-accountrules -Prefix sdar6` §4 is the pair: `sd -internal CREATE.ACCOUNT USER sdar6d ADOPT` with no marker is refused **as an unrecognised token (2018)** — no register record, Windows account untouched — and the control is **the install's own adoption**, not a second one the verifier performs. `adopt-account.ps1` wrote `sdsys\$adopt.don`, `CREATEA` tested `'$adopt.':downcase(acc.uname)`, matched, adopted and deleted it. Four independent traces: `adopt-account.log` *"don now has an SD account"*, `accounts\DON`, `verify-tiers` reading its tier as `ADMINISTRATOR`, and **no `$adopt*` file surviving under `sdsys`** — the last checked directly, unelevated, after the run. A marker bound to the wrong name would leave the installing user with **no SD account at all** |
| **§7 step 1f — the installer gives the installing user an account** | 15 Aug, and every install since | `adopt-account.log`: `don now has an SD account`, `don keeps the Windows sign-in rights it already had`; `ACCOUNTS/DON` present and `sdsshonly` **empty** |

#### Login, elevation and who reaches SDSYS

| claim | install | measurement, and its control |
|---|---|---|
| **The login rule and the command-line gate** | 16 Aug, 22:57:00 | 6 of 6. Bare `sd` → `8 DON`, `sd -ADON` → `9 DON`, `sd -ASDSYS` refused `10051`, `sd LISTF` and `sd -start` refused exit 1 — and **`sd --version` exit 0**, the control |
| **The command line is closed to an unelevated session** | 15 Aug | 19 of 19 against the **installed** `sd.exe`, hash-identical to `bin/sd.exe`. All twelve guarded switches plus `LISTF` and `WHO` refused, exit 1; `--version` exit 0. With `SD_SESSION=1` set, all four forms **including `--version`** answered `SD is already running in this session`, so the guard is before the gate as `comlin()` intends |
| **A Windows administrator is an SD administrator** | 14 Aug | Positive: from an **unelevated** administrator session `sd -start` worked — decisive because **gid 544 is not in `getgroups()`** there, so it can only have been found through `getgrouplist()`. Negative: rebuilt with `-DSD_ADMIN_GID=99999` it refused, exit 1 |
| **Windows does limit who may elevate** | 14 Aug | `EnableLUA=1` with `ConsentPromptBehaviorUser=3` — a standard user is prompted for **somebody else's** administrator credentials on the secure desktop and cannot elevate as itself. **This is the measurement §5.6's reversal rests on.** **The UAC slider moves, so read it rather than remembering it**; only the *prompt* changes, because token filtering is `EnableLUA`'s doing and that read 1 every time |
| **An unelevated administrator's token carries `Administrators` as "Group used for deny only"** | 14 Aug | That string is the whole of the distinction §7 step 0 needs, and it is the same fact as `getgroups()` versus `getgrouplist()` (§5.6.1) |
| **The global catalogue gate, and the two locks** | 18 Aug, 11:35:44 | `verify-catgate` 25/25. `DELETE.CATALOG $LOGIN` refused from a PROGRAMMER account with `$LOGIN` still 6,160 bytes; `CATALOG BP $SDGATE2` refused and `gcat` did not gain it; **private and local cataloguing still accepted in the same account**, and both administrator controls still work. The unprivileged session comes from `LOGTO SDSYS` then `LOGTO <account>` (`CPROC:2657`), not from credentials, which `sdsshonly` would refuse |

**`EnableLUA = 0` WOULD BREAK THE MODEL AND MAKE THE TESTS LIE.** With no split
token every administrator session is elevated, so `IsElevated()` collapses into
`IsAdmin()`, plain `sd` puts any administrator into SDSYS always, **SDSYS becomes
reachable over ssh**, and the refusal half of every gate test can never fire —
recording false passes. **The test machine must have `EnableLUA = 1`.**

#### The shell, and what an ordinary user can reach

| claim | install | measurement, and its control |
|---|---|---|
| **`OS.USERS` refuses an unlisted account** | 17 Aug, 22:43:52 | Unelevated `SH dir` as `don` → *"don is not permitted to use the operating system shell"* (10053). The ACL is checked separately and is the exact split `CPROC` needs: `sdusers:(OI)(CI)(RX)`, a write raises `UnauthorizedAccessException`, a read succeeds — `CPROC` reads the list in the user's own process |
| **The admit path runs — §7 step 7 observed rather than argued** | 18 Aug, 07:00:00 | `verify-osusers` 18 of 18, 13 decisive. The four-row table below. What was scored is **a marker file each probe creates**, not the message: SD echoes the command back, so a message can be present without the command having run |
| **`SH` is restricted by a generation-2 gate — not by Linux, and not by a port decision** | 15 Aug | `GPL.BP/CPROC:3321`, `if not(kernel(K$ADMINISTRATOR,-1))`, dated `2026/06/10` and present at the initial import. The original ScarletDME `CPROC` has no gate there at all, and `SH`/`!` have been in `VOC_TEMPLATE` throughout. **So §7 step 7 was never a search for a Linux block** |
| **An ordinary user's program reaches the OS in the same session where `SH` is refused** | 15 Aug | One unelevated session, control first: `SH echo` → *"Command requires administrator privileges"*; then a program in `don`'s own BP running `OS.EXECUTE ... CAPTURING` → marker captured and printed back. **So the gate does not break programs** — `OS.EXECUTE` compiles to `OP.SHCAP` and neither `K$ADMINISTRATOR` nor `!valid_shell_cmd` is on that path. **The form that does break is `EXECUTE 'SH ...' CAPTURING`**, which goes through TCL |
| **`SH` sets `SD_SESSION`, and `sd` refuses in the shell it hands back** | 15 Aug | `SH Get-ChildItem Env:SD_SESSION` → `SD_SESSION 1`, and the refusal watched on **both** child paths — `sh(TRUE)` and `sh(FALSE)`, the latter being the path the `SH` verb itself takes |

|  | plain `SH` | `SH` with a pipe |
|---|---|---|
| unelevated, unlisted | refused 10053 | refused 10053 |
| **elevated**, unlisted | ran | refused **5240** |
| unelevated, **listed** | **ran** | **ran** |
| unelevated, unlisted again | refused 10053 | — |

**What each row is for.** Row 3 is the reading nobody had ever taken. Row 4 is
what stops it being read into an install that admits everybody — the shell goes
away again when the record does. Row 2 is the "regresses nothing" claim, and its
two cells carry **different messages**: 5240 is `!valid_shell_cmd` refusing the
pipe, 10053 is the gate refusing the person.

#### The data tree, its ACLs and the case work

| claim | install | measurement, and its control |
|---|---|---|
| **`$CRED` is closed to ordinary users** | 17 Aug, 17:36:21 | `verify-credacl`, and **it must run unelevated** — the ACL grants `Administrators` Full, so an elevated run passes however broken it is, and the script refuses to run elevated. The decisive measurement is a **write**: `File::Open(...CreateNew)` inside `$CRED` raises `UnauthorizedAccessException` where the 17:08:32 install printed `sdusers:(I)(OI)(CI)(M)`. **A listing alone would not have been evidence** |
| **The data-tree ACLs are right, checked from the outside** | 14 Aug | Exactly `sdusers:(OI)(CI)(M)`, `Administrators:(OI)(CI)(F)`, `SYSTEM:(OI)(CI)(F)`, no `BUILTIN\Users` — and a session whose token lacks `sdusers` refused on every path inside. **`Test-Path` on the directory itself still answers True** (§6): check the contents, or you will conclude the ACL never applied |
| **Directory files open `DHF_NOCASE`** | 17 Aug, 20:10:31 | `verify-nocase`: directory file `FL$NOCASE` **1**, dynamic file **0**. Both read 0 on the 17:36:21 install, so the flag is being read rather than invented, and `dh_open.c:549` still takes a dynamic file's flags from its own header |
| **Case-insensitive queries against a directory file — the behaviour, not the flag** | 17 Aug, 20:34:04 | `verify-nocase` exit 0 with `SYSTEM(91)` answering 1, then by hand: `SELECT BP WITH @ID = "sue"` finds record `SUE`, **`SELECT VOC WITH @ID = "who"` finds nothing**. The dynamic file is the control and is the only reason the first half means anything. This is `QPROC:499` running for the first time |
| **A scheduled job runs the commands its account is listed for, and nothing else** | 22 Aug, 23:46:31 | `verify-batchjob`, **10 of 10 decisive**, run with an ORDINARY token because an elevated one passes the gate by design. Refused unlisted; **RAN** once the record was written; refused again once it was removed; refused with an argument though listed; refused when the VOC record is not PA/S; **still RAN elevated with no record at all**; and an ordinary token **cannot write** `batch.jobs`. **The two "RAN" rows are what make the five refusals evidence** — a gate that refused everything would pass those five. §7 step 9 |
| **A TCL token is not split at a backslash, and still is at a comma** | 22 Aug, 22:50:18 | `verify-parsertokens`, **7 of 7 decisive**. `CT VOC C:\Temp\zznosuch` comes back whole where the 21:34:25 install answered `Record 'C:'`; **the comma row is the control that makes it evidence** — `CT VOC a,b` still splits into `a`, `,` and `b`, so the parser is demonstrably in the path rather than bypassed. §7 step 12 |
| **The lower-case fold, the renames, and the tiers** | 18–19 Aug, various | `verify-fold`, `verify-lcnames` and `verify-tiers`, each with its own control — §5.12 carries what moved, what was left deliberately, and the four traps for anyone scripting a fold again |

#### The install, the service and the second machine

| claim | install | measurement, and its control |
|---|---|---|
| **A genuine first install works, and the files were counted** | 14 Aug | 3,264 files against a broken run's 16, and a `Compare-Object` of every staged path against every installed one reporting no differences in either direction. **An install test that does not COUNT what was installed proves very little** — `Check: DataTreeAbsent` had been evaluated per file, ~3,260 files were silently skipped, and Setup still exited 0 |
| **The install is whole and a session runs on it** | 16 Aug, 22:57:00 | `gcat` 132, `GPL.BP.OUT` 193, `gcat/$CPROC` 25,208 bytes, 3,477 files — then an **unelevated** `sd` answered `WHO` → `2 DON`. Both halves matter: the counts say the bootstrap finished, the session says the tree works |
| **The installed system runs as an ordinary user** | 14 Aug, after a reboot | Nothing set in the environment: `sd -start`, `COUNT VOC` 431, `WHO`, `sd -stop`. Closes §5.6.1 in the real world, §5.7's ACL model from the user's side, and the sign-out requirement. **What it does not show: `sd -start` had to be typed** — the gap the service later closed |
| **The service works, and an ordinary user reaches it** | 16 Aug | Service `Running`, `sdwind` alive at t+30s, all six `Global\sd_sem_*` openable, `adopt-account.log` reading `don now has an SD account`. Then the half the requirement rests on: from an **unelevated** session-1 process, all six semaphores opened and a bare `sd` answered `2 DON` |
| **The service survives a restart, including one with a leftover segment** | 16 Aug, thirteenth session | It did **not**, and the fix is what this row records: `sd_state()` downgrades `SD_WRECKAGE` to `SD_STOPPED` for a segment whose mtime predates boot. `sd -stop` still leaks the segment at shutdown, so the leak is harmless rather than absent. HISTORY, *"A segment from a previous boot stops meaning wreckage"* |
| **SD will not run under LocalSystem in session 0 on POSIX semaphores** | 16 Aug | `sdwind` dies at ~10s started by the service **and** by a scheduled task as SYSTEM with no service anywhere, and is **alive at 40s** from an interactive elevated session — one install, one sitting. `sem_open` at `sdsem.c:82` blocks ten seconds and times out, errno 116. Both processes in that probe were SYSTEM in session 0, so it is **not** cross-session. **Kept because it is why the Win32 semaphore change exists** |
| **No regression from the Win32 semaphores** | 16 Aug | The IPC change rewrote the layer every session depends on, so that morning's tests were re-run against it on the same install: 11 of 11 on the login rule and grants, 16 of 16 on `CREATE.ACCOUNT` |
| **The service no longer lies or leaves wreckage** | 16 Aug | It reports `STOPPED` with `sdwind.exe has GONE after 5 seconds` rather than `Running` over a dead SD, and `sd -stop` behind a failed start leaves `shm` empty. Before this, a failed service left every later `sd` on the machine broken |
| **The daemon starts on an installed system, and it is called `sdwind`** | 14 Aug | `start_sd()` asks `exe_directory()`, so `sd -start` from `C:\Program Files\SD\usr\bin` left `sdwind.exe` in that directory while `<sysdir>\bin` held only `pcode` — the old path could not possibly have worked. **Why it was silent is the trap in §6** |
| **§7 step 1d — `sd -start` and `sd -stop` over wreckage** | 15 Aug, installed binary | All five branches, run twice, from one unelevated session with every pid accounted for — including the `EPERM` warning, which names a **translated** Windows pid. Corroborated as §4 asks: `Stop-Process` from that same session was refused, and the daemon measured High integrity against the session's Medium |
| **The bootstrap refuses an unelevated window, before doing anything** | 15 Aug | A **nonexistent** `--sysdir` drew the elevation refusal and not `no such sysdir`, so the check is genuinely first. `stage.py --bootstrap` left no staging directory; plain staging stays ungated. The elevated half ran the same morning, 3,291 files staged |
| **The uninstaller removes the service and keeps the data** | 16 Aug | `sc query SD` → 1060, `C:\Program Files\SD` gone, and **`C:\ProgramData\SD` kept, 3,486 files** — which is the other half of the test |
| **The uninstaller runs, and the upgrade path is a different path** | 14 Aug | `/VERYSILENT` exit 0, `C:\ProgramData\SD` completely intact. The PATH entry is removed by `RemoveFromPath` at `usUninstall`, which Inno cannot undo by itself. `sdusers` is left deliberately — a kept data tree is ACL'd to it |
| **An installed system finds its configuration with nothing set in the environment** | 14 Aug | Reads `C:\ProgramData\SD\sd.conf` through `%ProgramData%` |
| **`CREATUSR` is gone from the compiled catalogue, not just from the source** | 16 Aug | Installed `gcat/$CONFIG` is 3,153 bytes and does **not** contain `CREATUSR`, while it does contain `DEADLOCK` — the control, without which the search proves nothing |
| **§7 step 2 on a second machine: the install is self-contained, and RDP is refused** | 15 Aug | VirtualBox guest with **no MSYS2, no `gplsrc`, no development tree**, which is the whole reason the step existed. Install **byte-identical**: `sd.exe` sha256 `81594E79CC2B560C`, the same four counts, and `COUNT VOC` **431**. Then RDP, control then treatment: `VIRTUAL\don` **ADMITTED**, `VIRTUAL\sdacct7` **REFUSED** with *"the user account is not authorized for remote login"* — the wording that is `SeDenyRemoteInteractiveLogonRight` specifically rather than a credentials failure. **`LogonUser` cannot test RDP at all**, so this genuinely required the second machine |

#### ssh, the deny rights and `AllowGroups`

| claim | install | measurement, and its control |
|---|---|---|
| **The ssh-only model works** | 14 Aug | `gplbld/verify-sshonly.ps1`, thirteen checks, **control and treatment on the same account minutes apart with nothing else changed**: the console is closed by the deny rights and ssh is not. `ssh` **ran a shell**, not merely authenticated, and the `OpenSSH/Operational` log agreed at the same moment, so the verdict does not rest on the test's own reporting. **Why there is a control column at all:** the first run refused the key login on *both* sides, and measured alone the treatment side would have read as "the deny rights break ssh" |
| **`ApplyDenyLogon` works — the rights are applied** | 17 Aug, 20:34:04 | `secedit /export /areas USER_RIGHTS`: `SeDenyInteractiveLogonRight` and `SeDenyRemoteInteractiveLogonRight` both **present** for `sdsshonly`, `SeDenyNetworkLogonRight` **absent**. **All three rows are wanted and the third is wanted absent** — setting it would deny the network logon Win32-OpenSSH authenticates with and break ssh outright |
| **`AllowGroups` is applied and enforced, and the administrator is not locked out** | 14 Aug | Control and treatment by real connections, with the **reason read out of the `OpenSSH/Operational` log** rather than the exit code, because the client message is identical either way. A member: `Connection reset by authenticating user`. An **enabled** non-member: *"none of user's groups are listed in AllowGroups"*. A first control was confounded by a **disabled** account and was redone |
| **`allow-ssh-groups.ps1` edits `sshd_config` correctly** | 14 Aug | `verify-allowgroups.ps1`, 20 checks against `sshd_config_default` — world readable, so the test needs no elevation, no `sshd` and no network, and it lifts the functions out of the shipped script by parsing it so it cannot drift. It asks whether add-then-remove reproduces the original **byte for byte**, and found a real defect on its first run (§6) |
| **An ssh session lands inside SD** | 15 Aug | `ssh sdacct6@localhost whoami` answered **SD's banner and a `:` prompt, exit 0 — `whoami` never ran**, which is sshd discarding the client's command and running SD. And **scp is dead, measured**: exit 255, *"Received message too long"* |
| **A brand new Windows account cannot use ssh KEY authentication until it has logged in once** | 14 Aug | Observed in both directions with group membership identical either way. A property of Windows, not of anything here: no prior logon means no profile and no home directory, so `AuthorizedKeysFile` is never read. **Password authentication is unaffected**, and this applies to accounts `CREATE.ACCOUNT` makes |
| **`BUILTIN\Users` membership is not required for an SD account** | 14 Aug | The account logged in over ssh and ran `whoami` **before** `Users` was added, and adding it changed nothing |

**READING THE DENY RIGHTS BACK HAS CAUGHT TWO ATTEMPTS.** `secedit /export`
writes resolvable local groups **by name, not by SID**, so a check grepping for
a SID reports "not present" when it is present — and **the file is UTF-16LE**,
so `Get-Content` without `-Encoding Unicode` can match nothing at all, which
looks identical. On 17 Aug 2026 a hand-rolled check hit **both at once** and
reported all three rights absent on a machine where two were correctly present.
**Use `gplbld/verify-sshonly.ps1`** (`:421-432`), which gets both right and
carries the warning in its own comment. Do not hand-roll it a third time.

#### The API

| claim | install | measurement, and its control |
|---|---|---|
| **The API is reached at its own port** | 21 Aug, 11:50:48 | `verify-apiport -Prefix sdapi4`. `netstat` shows `0.0.0.0:4243 LISTENING` and no loopback binding; the client library carried a real session over it with SCRAM client-first and client-final sent, no cleartext login, and **the password absent from the 286 bytes on the wire**. The installer's half separately: `SD-API-In-TCP` with `RemoteAddress Any`, and `APIPORT=4243` in the shipped `sd.conf`. **A connection from another machine is still unmeasured** |
| **A remote API session cannot open `$cred` or reach `OS.EXECUTE`** | 21 Aug, 17:18:11 | `verify-apiadmin -Prefix sdapia12`. It ships **two** probes: `APIOSEXECPROBE`, whose whole job is to die, alongside one that must survive. The containment gate in `op_dio2.c` roots a session at the account it stands in; the `USR_ADMIN` fix in `kernel.c` is the other half |
| **`SDConnectLocal()` carries a session** | 17 Aug, 12:28:49 | `make check-local` on the installed pair, `assert-current` exit 0, `WHO -> 2 DON`. **`DON` admitted and `SDSYS` refused** with *"User not allowed in requested account"* — `DON` alone would be equally consistent with a check that never executed, which is why the pair is evidence and either half alone is worthless |
| **`errlog` is written per connection, and trimmed** | 21 Aug, 17:18:11 | `verify-peerlog`. `sdwind.c`'s `log_message()` gained the trim the `sd` side always had |
| **`!valid_os_name` refuses a qualified login name, the client cannot tell why, and the trail can** | 22 Aug, 08:32:03 | `verify-apiname -Prefix sdapin2`, **17 of 17**, owner's elevated run; `sdapin1` was 13/13 on 21 Aug, 17:18:11, before the audit half existed. **The control is the same account and password admitted bare**, which is what makes the four refusals evidence rather than four accounts that did not exist: `COMPUTER\name`, `computer\name`, a **spaced** name and **`name@computer`** (the UPN shape) all refused. **All four return the byte-identical text a WRONG PASSWORD returns** — `Invalid username or password`. **THE AUDIT HALF IS THE REVERSAL**: on `sdapin1` the `audit` file *"did not grow at all"* across the five refused attempts, and on `sdapin2` it grows once per refusal with a distinct `reason=`, the name sanitised to `GITORLI?sdapin2`, and no raw backslash anywhere. The 33-character control is refused CLIENT-side with different text (`Invalid user name`, `sdclilib.c:1218`), so the length cap and the charset check are two limits and not one seen twice. §2 has why refusing costs no legitimate login; §8 has the audit record |

| **An API session runs as the user who logged in — files and all** | 24 Aug, 11:15:29 | `verify-apiidentity -Prefix sdapiidb32`, `assert-current` exit 0, `sd.exe` `7DDC68F6595382A6`. **`ZZAPI` owned `GITORLI\sdapiidb32`** where `b28` read `NT AUTHORITY\SYSTEM`; the control `ZZLOCAL`, written by a local elevated session, reads `GITORLI\don`, so the two owners differ and ownership is tracking the writer. **The DENY fixture is now REFUSED (`status 3001`)** — it OPENED on `b27`/`b28` because a LocalSystem session holds `SeBackupPrivilege` and bypasses DACLs outright, so that row flipping is a second, independent instrument saying the session is no longer LocalSystem. **And `API IDENTITY LOST` is absent from the errlog** — the same `check.identity` (`APISRVR:578`, `:921`) that printed it twice on `b31`, unchanged, with both call sites exercised this run (`vb.account` attached, then the write). §7 step 14 |

| **SD writes CRLF to everything externally readable** | 24 Aug, 12:36:09 | `verify-lineendings`, **17/17 decisive**, `assert-current` exit 0, `sd.exe` `070A9C52E293B2FA`. Read as **raw bytes, not through SD** — since the reader now folds CRLF, a round trip through SD would have reported success whatever was on disk. `WRITESEQ` → `ONE␍␊TWO␍␊`; **`WRITECSV` → `A1,B1␍␊A2,B2␍␊`, conformant with the RFC 4180 claim its own documentation makes**; a directory-file record write → `RA␍␊RB␍␊RC␍␊`. **All fourteen (a) checks still pass**, so the write change did not regress the read change. The owner's rule was external readability, and **no DH path uses `Newline` at all**. §7 step 16 (b) |
| **SD reads CRLF files correctly, and a lone CR is still data** | 24 Aug, 12:15:51 | `verify-lineendings`, **14/14 decisive**, `assert-current` exit 0. A directory-file record planted with CRLF from outside SD now reads **identically to the LF control** (fields 5, 5, 6) where it previously kept a `LAST=13` on every terminated field; `READSEQ` and `READCSV` likewise, the latter mattering because a conformant RFC 4180 CSV used to lose its last field per row to a stray CR. **Two controls are on the FIX, not the defect**: a CRLF placed exactly on the 2048-byte `SEQ_BUFFER_SIZE` boundary folds (line 1 reads 2047, not 2048), which is the case no small fixture reaches; and `LEFT<CR>RIGHTZ` stays **one field of 11 bytes**, so the change did not simply strip every CR. §7 step 16 (a) |

#### The foundations, observed 13 Aug 2026

Nothing since has contradicted any of them, and re-verifying them is not worth a
session's time.

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

**The five OS-facing BASIC helpers work, and the shell is PowerShell** — 14 Aug
2026, re-observed after `op_sh.c` was pointed at PowerShell, so `OS.EXECUTE`
reaches it and the exit status carries back through `OS.ERROR()` with bash out
of the loop entirely. `!valid_os_path` 16 of 16, `!is_grp_member` 7 of 7,
`!ps_script` 5 of 5. **One measurement decided the design:**
`Invoke-Expression` propagates a script's `exit` status where `& .\script.ps1`
does not, and it is not subject to the execution policy, so nothing needs
`-ExecutionPolicy Bypass`.

**`sudo.exe` is present and enabled in inline mode** (`Enabled = 3`), enabled by
hand on 14 Aug 2026. **The installer neither installs nor enables it** and does
not need to — "Run as administrator" produces the same elevated token on every
Windows version.

### Not verified — treat as unknown

**SWEPT 21 Aug 2026, AGAIN WHILE COMPRESSING, AND AGAIN 26 Aug 2026.**
**Fourteen** claims here have been struck or narrowed since 21 Aug because the
thing they called unknown had been measured, in several cases **hundreds of
lines above the entry still calling it unknown**. They are in the archive with
what settled each.

**THE 26 Aug SWEEP READ ALL SEVEN LIVE ENTRIES AND FOUND EXACTLY ONE ROTTEN**
— the ssh-options bullet, whose two halves were closed by a ruling and by two
on-screen observations. **The other six were checked and stand**, which is
worth stating: `K$SET.USERNAME`'s non-`$internal` refusal has **no verifier at
all** (grepped `gplbld` for it — no hits, against `CRED_VERIFY` as the control),
and interactive SD **over ssh at a real terminal** appears nowhere but in this
claim and its own archive copy. A sweep that reports only what it struck reads
as if the rest were unexamined.

**THE PATTERN IS WORTH KNOWING BEFORE READING THE REST.** The header was
rewritten every phase and this list was not, so **what rots here is specifically
an entry claiming something has NOT been done** — the dated measurements in the
Verified half held up under checking. **Check §4 against itself before believing
anything here.** Two of the twelve were refuted by the Verified half of this very
section; the twelfth, struck 21 Aug 2026 while compressing, was *"whether
`OS.EXECUTE` works at all on an installed system"*, which the 15 Aug measurement
of an ordinary user's program reaching the OS had already answered on an install.

- ~~**`OS.EXECUTE` is ungated for every *local* session.** `OS.EX` is stored,
  dictionaried and read by nobody, so an unlisted programmer with `BASIC` still
  has full OS access from a program. Gating it needs C.~~ **THAT C WAS WRITTEN
  ON 19 Aug 2026 AND THIS ENTRY WAS THE THIRTEENTH STALE CLAIM IN THIS LIST —
  struck 21 Aug 2026, having survived the compression pass of the same day.**
  `os_permitted()` (`op_sh.c:150`, called at `:209`) gates `OS.EXECUTE` for
  every session, on `HDR_INTERNAL`, elevation, or `OS.USERS` field 2;
  `verify-osusers` **24/24** on the 16:38:01 install, with a four-row truth
  table at §7 step 7 whose middle two rows prove the two fields independent.
  **The lesson is the one this list already states about itself, arriving
  again**: an entry claiming something has NOT been done is the kind that rots,
  and reading it in place is not enough to notice — it took checking §7 step 7
  against HISTORY.

- **What still has to be watched when something calls `vb.login`.** Four things:
  that an account with no `$CRED` entry is refused; that one with an entry is
  admitted; that `@logname` afterwards is the name that was **verified** rather
  than the client's assertion; and that `kernel(K$SET.USERNAME,…)` is **refused
  from a program that is not `$internal`**, which is the gate protecting the
  audit trail.

  ***THIS ENTRY POINTED AT "§7 step 6a, 6b and 6c" UNTIL 22 Aug 2026, AND ALL
  THREE HAD STOPPED EXISTING*** — step 6 was compressed on 21 Aug and its
  sub-steps went with it, so the pointer sent a reader hunting for a
  numbered item no longer in the file. The four claims are written out here
  instead, which is what should have replaced the pointer. **Two more of the
  same dangling pointers survive in §6** (`§7 step 6c` and `§7 step 6a`) and are
  narrative rather than task, so they are left with this note against them.
  Same fault as the `header item N` row in the stale-claims table: **compressing
  a section does not update what points into it.**

- **Which of `AllowGroups`' four patterns actually matched.** It is applied and
  enforced, but `AllowGroups` is a union and all four patterns were written
  deliberately, so the bare and `COMPUTER\` forms cannot be told apart from that
  result. Deliberate — §5.6.2 — and it stays unknown unless somebody narrows the
  list on purpose.

- **The installer's own path through the ssh options.** The reworded closing
  dialog **has** been seen and read on screen (17 Aug, *"looks fine"*).
  ~~What is still unseen is the **`limitssh` task** and **`ApplyAllowGroups`
  reporting any of its three outcomes**.~~ ***BOTH HALVES ARE CLOSED AND THIS
  WAS THE FOURTEENTH STALE CLAIM IN THIS LIST — struck 26 Aug 2026.***

  - **`limitssh` is no longer a task at all**, so there is nothing left to see:
    the refuse-to-install ruling removed it, and `sd.iss` now declares exactly
    three — `addtopath`, `sshremote`, `apiremote` (checked by grepping
    `^Name: "` , which returns those three and nothing else).
  - **`ApplyAllowGroups` reported its outcome on screen, twice.** 24 Aug on
    `Windows 11 - sshRemoteTest`, *"ssh is now limited to members …"*; 25 Aug
    across the three-guest run, *"running with no task gate, confirmed by its
    own outcome box"*. HISTORY.md, fifty-fourth session part 3 and fifty-fifth
    part 4.

  ***THE ENTRY BELOW IT PREDICTED THIS EXACTLY AND STILL DID NOT SAVE IT.*** It
  says both are *"visible on the next ordinary cycle — no VM"*; several ordinary
  cycles then ran, the VM runs saw them too, and **the sentence above it went on
  saying "still unseen"** because nothing sends a reader back to the opening
  line of a bullet whose body they just corrected. **When you withdraw part of
  an entry, re-read its first sentence.**

  ***"NEITHER CAN BE SEEN HERE … IT NEEDS THE VM" IS WITHDRAWN, 24 Aug 2026.***
  It rested on `Check: SshServerAbsent` gating the task. **`limitssh` lost its
  `Check` on 21 Aug 2026** ([sd.iss:210](sdb_ai/sd64/gplbld/sd.iss:210) carries
  none) and is offered on every install, **ticked by default**;
  `ApplyAllowGroups` is gated on `WizardIsTaskSelected('limitssh')`
  (`sd.iss:965`), so it runs here too. **Both are visible on the next ordinary
  cycle — no VM.** `sshremote` is the one that still needs it
  ([sd.iss:139](sdb_ai/sd64/gplbld/sd.iss:139) keeps the `Check`).

  **This is the third claim in this file to survive the change that falsified
  it** — `sd.iss`'s own comment at :2390 recorded the change the day it
  happened, and three sections went on asserting the old shape. Compiling an
  Inno script proves the Pascal parses and nothing more — the two defects
  already recorded in that script both compiled perfectly.

- **That SD works over an ssh session AT A REAL TERMINAL — only the tty half is
  left.** The two separately are done: an ssh session lands inside SD (above),
  and the MSYS2 tty layer was measured at a real Windows console on 19 Aug
  (§5.18). **What has never happened is those two at once** — an interactive
  `sd -ASOMEACCOUNT` at a terminal *reached over ssh*, where the pty is sshd's
  rather than `conhost`'s. §7 step 2's rig is what would answer it.

- **Semaphore locking under contention.** The semaphores have never been
  observed **held** — nothing has watched one block. They are no longer
  exercised only in the uncontended case, though: the record-lock contention
  below runs through `StartExclusive(REC_LOCK_SEM, ...)`
  ([op_lock.c:591](sdb_ai/sd64/gplsrc/op_lock.c:591)) from two sessions at
  once, and it did not misbehave. **What is unmeasured is the blocking path,
  not the code path.**

- ***CONTENTION — THE RECORD-LOCK HALF IS CLOSED, 26 Aug 2026. THE API HALF IS
  NOT.*** Two sessions ran at once on the 17:14:03 install (users 73/74, then
  76/77) and **competed**: `recordlocked()` answered -1, -2 and -3 for another
  session's read, update and file lock, every `locked` clause fired with
  `status()` carrying the holder's user number, a plain `readu` waited 252 ms
  and was released by the other session, and a task lock refused the second
  taker. `tools\sdprobe2.ps1` in the docs repository is the instrument and it
  **refuses a run in which the two did not demonstrably overlap**. ***What is
  still untried is the API server path*** — contention between an API session
  and a local one.

- **Writing and reading application data.** The bootstrap creates and reads
  system files; the scratch accounts hold nothing but a VOC.

- **What the daemon actually does for the system — EXERCISED 22 Aug 2026, AND IT
  DOES NOT CONVERGE.** `check_lost_users()` (`sdwind.c:238`) scans the user table
  every five minutes, and on finding an entry whose process is gone
  (`kill(pid, 0)`) shells out to `sd -cleanup` (`:295`). This entry used to say
  *"that path has never been exercised — no session has been killed and the
  cleanup watched"*. **Both have now happened**, by accident rather than design:
  several `sd` sessions were killed with `Stop-Process` to escape a hang, and
  from **09:13:01 onward every new session was answered `Forced logout`** —
  twelve of them in the error log, user numbers 242 to 253, each a *fresh,
  healthy* session, `sdwind` the only live process. It **did not recover on its
  own** across twenty minutes, and `sd -cleanup` cannot be run by hand to clear
  it because that verb requires elevation.

  **WHAT IS ESTABLISHED IS THE SYMPTOM, NOT THE CAUSE**, and the difference
  matters: killing sessions leaves stale entries, the daemon notices, and the
  remedy it runs ends up forcing out live sessions instead of only dead ones —
  but whether that is `sd -cleanup` misjudging, or `kill(pid, 0)` answering
  wrongly for an MSYS2 pid, was **not** determined. Do not write it up as either
  until somebody looks.

  **THE OPERATIONAL PART: never `Stop-Process` an `sd` session on a tree you
  still want to measure.** It costs the install, not just the session. Recovery
  is elevated — `sd -cleanup`, and a service restart if that does not take.

- **RDP refusal — CLOSED, but the rest of this entry is KEPT AS A TRAP, NOT A
  TASK** (§0 rule 4). It was watched refusing a session on the VirtualBox guest,
  control then treatment, so §5.6.2 has no unobserved claim left. What is still
  true is that **it cannot be tested on this machine**, and this is the record
  that stops the next session rediscovering that.

  **It cannot be automated:** there is no `LogonUser` logon type corresponding
  to RDP's type 10, so only a real Remote Desktop connection exercises the
  right; asking for one returns `87 ERROR_INVALID_PARAMETER`.

  **AND THIS MACHINE CANNOT RDP TO ITSELF. Measured 14 Aug 2026, three
  attempts**, so do not spend more time on it here — `mstsc /v:localhost` with
  the signed-in user's credentials, with the probe account's, and
  `mstsc` to the machine's own Wi-Fi address, all three answering:

  ```
  Your computer could not connect to another console session on the remote
  computer because you already have a console session in progress.
  Error code: 0x708
  ```

  **The refusal comes before any credential prompt**, so which account is
  offered never enters into it. RDP was enabled throughout — `fDenyTSConnections`
  0, `rdp-tcp` listening, inbound rules on for all profiles, all checked the same
  day. That is the whole of what was observed: it is deliberately **not** turned
  into a statement about how many sessions Windows permits, because two such
  statements were derived from this error already and both were wrong
  (HISTORY.md, two `Correction:` entries of 14 Aug 2026).

  **To repeat the test:** `verify-sshonly.ps1 -Keep` on the machine under test,
  then RDP to it from a different one. §6 has the two RDP traps, which between
  them cost most of an hour.

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
   (5 Aug 2026) — `gplsrc/sdclilib/VENDORING.md` is the record.
4. **Their developer then forked `winsdclilib` back**, and changes from it are
   in `sdb64`'s `dev` branch now.
5. **AND THE ARROW TURNED ROUND ON 19 Aug 2026.** This directory is **no longer
   a vendored copy** — it is the source of truth, and `winsdclilib` is its
   mirror. *Corrected 21 Aug 2026: step 3 used to end "the whole directory is a
   vendored copy kept faithful to its source on purpose", which stopped being
   true when the 32-bit client shipped without SCRAM in it.* §2 has the table.

**So for this directory, code has flowed BOTH ways, and "upstream" is
ambiguous** — the reverse of every other file in the port, where `sdb64` is
plainly the source. Two consequences worth acting on:

- **Do not "align with upstream" reflexively here.** A session did exactly that
  with `SV_EMSG_PAIR`/`SV_ECONTXT` and had to revert it — settled in
  UPSTREAM_FIXES.md #2, **which is closed**: `sdb64` was right, the fault was in
  the client libraries, and all four trees have read 6/7 since 15 Aug 2026.
- **An AI completed step 2**, so this directory carries the same risk §2
  describes for generation 2 — plausible-looking decisions nobody made
  deliberately. It has **no `Composer AI` markers**, so that grep does not find
  them here; the tell is absent and the suspicion still applies.

### 5.4 The BASIC layer's platform switch, and why it is not to be revived (owner, 21 Aug 2026)

The C code and the BASIC source in `sdsys/GPL.BP` work together — notably for
compilation — and the BASIC side has a platform abstraction of its own.

**OWNER'S RULING, 21 Aug 2026: THERE SHOULD BE NO WINDOWS BRANCHES IN THIS
VERSION OF SD, BECAUSE IT IS WINDOWS ONLY.** Same rule CLAUDE.md states for the
C code. **The switch is therefore something to remove, not to turn on**, and
§7 step 12 is rewritten accordingly — take the Windows arm, drop the
conditional, delete the Linux arm.

Two SYSTEM keys are the entire bridge:

| Key | Meaning | State, re-read 21 Aug 2026 |
|---|---|---|
| `SYSTEM(91)` | "is this Windows" | **answers `1`** — `op_sys.c:282`, changed 17 Aug 2026 |
| `SYSTEM(1006)` | "is this Windows NT style" | returns `is_nt`, `kernel.h:43` `init(FALSE)`, **never assigned**, and **no BASIC file reads it** |

**THE `SYSTEM(91)` ROW SAID "hardcoded to `0`" UNTIL 21 Aug 2026 AND WAS TWO
DAYS OUT OF DATE WHEN IT WAS WRITTEN.** It was flipped on 17 Aug to fix the
query processor: `QPROC:87` reads it into `is.windows` and `QPROC:508` is the
**only** route by which a directory file's ids are matched case insensitively,
so `SELECT ... WITH @ID = "sue"` never matched record `SUE`. `op_sys.c:259` has
the reasoning. **That single reader is also why flipping it early was safe** —
the branch removal had been thorough enough that nothing else could light up.

This repository's BASIC source has had its Windows branches removed — `LOGIN`,
`CONFIG`, `CPROC`, `CREATEA` and `PARSER` all went to none. The logic still
exists in the external tree at **`C:\Users\dmont\Projects\GPL.BP`** (§2, and
the 13 Aug HISTORY entry *"Surveyed the BASIC layer (GPL.BP)"* — whose closing
pointer to "§5.5" means **this** section, which was §5.5 before the file was
renumbered). **The idiom there is a bare `windows`**, set by
`windows = system(91)`, not `is.windows`.

**THE OLD ORDERING WARNING IS GONE WITH THE RULING.** It said restoring the
branches first was harmless but flipping `SYSTEM(91)` first would turn on paths
that are no longer there. Nothing is being restored and nothing is being
flipped, so neither half applies. §7 step 12 has what replaced it.

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
`LOGTO` is logged.

***CORRECTED 25 Aug 2026 — THIS PARAGRAPH WAS STALE BY ELEVEN DAYS.*** It read:
*"`LOGTO SDSYS` re-prompts — the one exception to 'granted, not prompted' — and
asks for the caller's own password, not an SDSYS one, which is easy to get
backwards and is the whole point: an SDSYS password would be a second shared
secret held by every administrator, which is the OpenQM weakness this exists to
remove."* **`LOGTO SDSYS` asks for no password at all.**
`LOGTO.STEP.UP` was deleted on 14 Aug 2026 — `CPROC:3798` says so in as many
words, *"there is no password to re-ask for now: the gate is elevation and it
is applied at login"* — and §5.6's five rules already recorded the reversal.
**What `CPROC:2568` actually does is call `elevate('START','')`**: 0 when the
session is already elevated, a UAC consent prompt otherwise, and `sysmsg(10002)`
with an audited `LOGTO REFUSED` when that fails. The reasoning about a shared
SDSYS secret still holds and is why there is no SDSYS password to ask for; it
was the *mechanism* that changed.

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

***SUPERSEDED IN ITS ssh CLAUSES — READ PRE_RELEASE 124 BEFORE USING THIS. 2 Sep
2026.*** The decision below stands on who may use the console; **its two ssh
claims are both false now.** The API is an **independent port-4243 listener**,
not a tunnel — `sd.iss:349` records *"the ssh tunnel is no longer part of the
design"* — so accounts do **not** reach the machine over ssh and nothing else,
and the API is **not** piped through ssh. *(The original text is kept below
unaltered; it is the record of what was decided on 14 Aug, not a description of
today's design.)*

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
- **What used to stand here as "the real answer", and it is NOT.** The
  proposal was: `sdwind` becomes a service running as a dedicated account -
  a virtual account, `NT SERVICE\SD`, needing no password management - which
  owns the tree exclusively, with **session processes spawned under the
  SERVICE identity** and the user reaching their session over a named pipe, so
  the user's own token never touches the data. Accounts would become private
  *because* of the password rather than in spite of it. It was called the
  direct Windows equivalent of the Linux original dropping to `sdsys` via
  `EUID_SET` (§5.5).

  **20 Aug 2026 - THAT IS THE BUG THIS PROJECT JUST MEASURED, WRITTEN AS A
  DESIGN.** "Session processes run under an identity that owns the whole tree"
  is exactly what an API session already does by accident, and
  `verify-apiadmin.ps1` showed where it leads: a PROGRAMMER-tier account
  opened and wrote `$cred`. Adopting this deliberately would generalise that
  from the API to every session.

  **WHAT THE PROPOSAL LEFT OUT IS THE PART THAT MAKES IT SAFE.** It works only
  if SD enforces access once the OS no longer can, and **SD has no file-level
  access control**: `op_openpath` calls `open_file()` with no path restriction
  of any kind (`op_dio1.c:368`). The Linux comparison is what hid this - Linux
  `EUID_SET` drops to `sdsys` *and* the Linux original had the same absence,
  so the parallel is exact and inherits the gap rather than answering it.

  **SO IT IS A ROUTE, NOT AN ANSWER, and the missing half is the bulk of the
  work**: path gating inside SD, **which exists as of 21 Aug 2026** — the
  containment gate in `op_dio2.c`, rooted at the account the session stands in.
  So the missing half is no longer missing, and what this section still lacks
  is the identity half. *The claim that stood here — "the named-pipe transport
  is separately blocked, so the transport half cannot be built today either" —
  went with the named pipe: the local transport was rebuilt on anonymous pipes
  the same day and works (§7 step 11).* **Do not reach for this section as the
  fix.** The opening section of this file has the options that were actually
  weighed.

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

***BOTH HALVES OF THIS "Why" ARE NOW FALSE AND SO IS ITS CONCLUSION — 2 Sep
2026, PRE_RELEASE 123 AND 124.*** The API is an independent port-4243 listener
rather than an ssh tunnel (124), so an install without ssh is **usable** — an
API-granted account signs in with no ssh server present — and `install-ssh.ps1`
is no longer unconditional either: the `sshserver` task is **opt-in, default
off** since 1 Sep (123), carrying `Flags: checkablealone unchecked`. *(Original
kept below as the record of the reasoning that was overturned.)*

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
`installssh\allowgroups`) is now top-level.

***"ITS OWN `Check` IS THE ONLY THING LEFT KEEPING IT OFF SOMEBODY ELSE'S
SERVER" IS WRONG AND IS WITHDRAWN, 24 Aug 2026.*** `limitssh` **has no
`Check`** — it lost one on 21 Aug 2026 ([sd.iss:210](sdb_ai/sd64/gplbld/sd.iss:210)),
is offered on every install, and has no `Flags: unchecked`, so it is **ticked by
default**. `sshremote` is the task that still carries `Check: SshServerAbsent`
(`sd.iss:139`).

***AND THE TWO ssh STEPS ARE GATED DIFFERENTLY, WHICH IS THE PART THAT MATTERS
AND WAS NOT WRITTEN DOWN ANYWHERE.*** Measured in the source, 24 Aug 2026:

| step | gate | so on a machine with somebody else's sshd |
|---|---|---|
| `ApplySshFirewall` | ***`if not SshWasAbsent then Exit`*** (`sd.iss`) | **never runs.** The rule is structurally safe |
| `ApplyAllowGroups` | ***only*** `WizardIsTaskSelected('limitssh')` (`sd.iss:965`) | **RUNS, on a default-ticked box** |

**So `sshd_config` is protected by neither a `Check` nor `SshWasAbsent`** — it
is protected by **refusal 2 inside `allow-ssh-groups.ps1`**: an existing
`AllowGroups`, `AllowUsers`, `DenyGroups` or `DenyUsers` line is somebody's
policy and the script exits 2 leaving it alone. That backstop is real and is
tested (`verify-allowgroups`, four foreign-policy shapes refused).

***BUT `allow-ssh-groups.ps1`'s OWN HEADER STATES A PREMISE THAT IS FALSE.***
Lines 30-34 say the §5.9 rule *"is carried by the task being **unticked by
default**"*. **It is ticked by default.** The header names refusal 2 as "the
real backstop" in the same breath, so the script's behaviour is right and only
its stated reasoning is wrong — but the gap it leaves is real: **on a machine
whose `sshd_config` is STOCK — no `AllowGroups` line, which is exactly what
this machine was found with on 21 Aug 2026 — refusal 2 does not fire, and a
default-ticked box edits an ssh server SD did not install.**

***THAT IS A DECISION FOR THE OWNER, NOT A DEFECT TO FIX QUIETLY.*** The
options are to restore `Flags: unchecked` on `limitssh`, to gate
`ApplyAllowGroups` on `SshWasAbsent` the way the firewall step is, or to rule
that a stock config is fair game because the task names what it does. **Not
started, and nothing has been changed on the strength of this reading.**

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
  matter. ***1010 IS FIXED, 26 Aug 2026*** — `PLATFORM_NAME` in `sddefs.h` is
  `"Windows"`, so `SYSTEM(1010)` answers Windows and `BCOMP`'s `$IFDEF` token
  moves from `SD.LINUX` to `SD.WINDOWS`. **Nothing in `gplsrc` or `sdsys`
  tests either token** — checked before the change, not assumed — so no
  shipped program compiles differently. **1006 is still hard-wired 0**:
  `is_nt` is declared `init(FALSE)` at `kernel.h:44`, read once, and assigned
  nowhere. Set it or remove the key; it is a decision, not a fix, and it is
  open. The rest are platform neutral.
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

**FILE NAMES ARE IN SCOPE, INCLUDING THE ONES THAT ALREADY EXIST — `VOC`, `BP`
and the rest. Owner, 18 Aug 2026.** Not only newly created files: the shipped
ones are to be lower case too.

**IT IS TWO DIFFERENT THINGS AND ONLY ONE OF THEM IS HARD.**

a. **The name on disk.** `ACCOUNTS`, `BP`, `BP.OUT`, `DICT.DIC`, `DIR_DICT`,
   `GPL.BP`, `GPL.BP.OUT`, `MESSAGES`, `NEWVOC`, `OS.USERS`, `PCODE.OUT`,
   `PSTMP`, `SD.VOCLIB`, `SYSCOM`, `VOC`, `VOC.DIC`, `VOC_TEMPLATE`, the four
   `$` files, and per account `BP`, `VOC`, `$HOLD`, `$HOLD.DIC`, `$SVLISTS`.
   **Renaming these is cosmetic for resolution** — NTFS matches without being
   asked — but the stored path text is user-visible through `LISTF` and
   `OS_CWD`, which is the point. Note the account directory already mixes the
   two: `cat` and `stacks` are lower case beside `BP` and `VOC`.

b. **The VOC record id, which is what a user types.**

**THE CONVERSION IS DOWNWARD, owner 18 Aug 2026** — `upcase(` towards
`downcase(`. `downcase()` is a compiler intrinsic (`BCOMP:469`, `OP.DNCASE`)
and `CREATEA:517` already uses it to force lower case, so the idiom is
established here.

**BUT THE FOLD IS NOT A PLAIN `upcase(` — IT IS "AS TYPED, THEN UPPER", AND
THAT CHANGES THE PLAN.** Read 18 Aug 2026, and two earlier readings of this
section were wrong about it. Every site tries the token EXACTLY AS TYPED first
and only falls back to upper case:

```
PARSER:151   read voc.rec from @voc, string
PARSER:152     else read voc.rec from @voc, upcase(string)
PARSER:139   open string ... else open upcase(string)          multifile
QPROC:488    open qproc.file.name ... else open upcase(...)    + :494 rewrites the name
CPROC:2176   open run.file.name.out ... else open upcase(...)  RUN, and 2182/2192 likewise
PARSER:251   read voc.rec from @voc, upcase(string)            THE EXCEPTION - no as-typed try
```

**SO THE CHANGE IS ADDITIVE, NOT A FLIP: as typed → down → up.** Adding a
`downcase` attempt to the chain is **purely additive on today's tree** — with
every id upper case, the new attempt can never hit, so it changes no behaviour
and cannot break anything. Replacing the `upcase` attempt instead would break
lower-case typing of every id not yet renamed, and `PARSER:152` serves verbs and
keywords as well as file names, so that blast radius is the whole VOC.

**THE FOLD IS NOT EIGHT SITES. IT IS 76, IN 38 FILES — measured 18 Aug 2026**,
and the list above was only the ones someone had looked at. **DONE AND VERIFIED 18 Aug
2026** on the 16:24:23 install — `gplbld/verify-fold.ps1`, 5 of 5. 63 converted
by a scripted transform over the two regular shapes, 11 by hand, 4 left
deliberately. The first bootstrap FAILED; see the traps below.

- **PLAIN** — `read/open X else read/open upcase(X) else <err> end end`. Insert
  a `downcase` tier; re-indent the inner block.
- **REWRITE** — as PLAIN but followed by `X = upcase(X)` inside the outer block,
  so the `downcase` tier takes the `THEN` form and folds the name itself.
- **BY HAND**: `PARSER` ×3 (multifile `status()` nesting; a single-line
  `else goto`; and the keyword read, which has no as-typed attempt and whose
  body would have to be duplicated — a `fold.found` flag instead), `CATALOG`,
  `CPROC` ×2, `FORMAT`, `SED`, `SHOW` (which folds through `found` flags in
  separate blocks, so a lower-case pair goes before the upper-case pair), `CD`
  (the name opened and the name rewritten are different variables).
- **LEFT DELIBERATELY**: `CPROC:2600` and `LOGIN:690` read `ACCOUNTS` by
  **account name**, which stays upper case — that is the wide half of this
  section and is what makes signing in case insensitive. `QPROC:3848` and
  `UPDREC:2584` have **no as-typed attempt at all**, so there is no fold to
  extend; they are dictionary/token ids and belong with the dictionary half.

**FOUR TRAPS FOR ANYONE SCRIPTING THIS AGAIN. The last two got past a clean
compile and a balance check, and were caught only by running the bootstrap.**

1. **Fold sites nest** — `CPROC`'s RUN block holds three, one inside another —
   so indices taken before the first edit are stale by the second. Batch
   conversion silently skipped the outer sites and would have spliced a `PLAIN`
   site at the wrong line. Recompute after every single conversion.
2. **A converted REWRITE site re-detects itself**, because the inserted
   `end else` becomes the line above the `upcase` attempt, so a one-line
   "already done?" check loops forever.
3. **`if cond then <statement>` followed by `else` / `end` is a block, and its
   opening line does not end in `then`.** Miss it and the matching-end search
   stops one `end` early, so the inserted `end` lands *inside* the wrong block.
   In `BCOMP`'s `open.include.record` that put `return` on the wrong side of a
   branch. **It compiled, and it balanced** — count the bare `else` as an
   opener.
4. **The trailing rewrite is not always `X = upcase(X)`.** `BCOMP`'s
   `get.file.ref` has `token = upcase(token.string)` — different variable each
   side. Rebuilding it from the left-hand side produced
   `token = downcase(token)`, which reads `token` before it is ever assigned:
   **"Unassigned variable in $BCOMP"**, which stopped the bootstrap while it was
   compiling `TERM`. Mirror the existing line, do not regenerate it.

**The balance check is necessary and NOT sufficient**, which trap 3 proves:
every edited file's block-opener minus block-closer count must be unchanged from
its committed version (36 files, 0 unbalanced), but a misplaced `end` balances
just as well as a correct one. **`cycle.ps1 -SkipInstall` is the real check** —
it costs a bootstrap, not an install, and it is what found both of these.

**THE FOLD HAD A SECOND LOOKUP AND IT WAS MISSED — FIXED AND VERIFIED
18 Aug 2026**, `verify-fold.ps1` 10/10 on the 19:46:12 install, section 4.
`_VOC_REF` is `pcode_voc_ref`, which `get_voc_file_reference()`
(`op_dio1.c:481`) recurses into, so it resolves the name for **every BASIC
`OPEN`** (`op_dio1.c:624`) and for `op_seqio.c:193`, `:453`. It was not among
the 36 files the fold commit changed and had **no fold at all** — one
exact-match read, then the `PATH:` / `Account:File` syntax.

**THE 74 SITES WORK BY PASSING EACH OF THREE CASES DOWN TO AN EXACT-MATCH
`_VOC_REF`.** That is why verbs all passed. A **hard-coded literal** got
nothing: `open "$SAVEDLISTS"` at `SAVELST:106`, `GETLIST:97`, `DELLIST:69`,
`LSTMRG:60`, `COPYLST:171`/`:193`, `SAVESTK:89`/`:110`, `CLEANAC:72`,
`UPDREC:77`, `_DELLIST:39`, `_GETLIST:39`, `_SAVELST:47`, plus `ED $SAVEDLISTS`
in `NEWVOC/EDIT.LIST` and `VOC_TEMPLATE/EDIT.LIST`. Every one would have broken
at the first VOC-id rename.

**Measured before the change** on the 18:54:10 install: VOC id `zzprobe1` could
not be opened as `ZZPROBE1` from BASIC while `COUNT ZZPROBE1` found it; VOC id
`ZZPROBE2` could not be opened as `zzprobe2`. **A FLAG AND A `goto`, NOT A
NESTED BLOCK** (`_VOC_REF:102`), so the special syntax keeps its indentation —
the file already jumps to `parse.as.q.pointer` from inside its own case
statement. The Q-pointer target at `:272` takes the PLAIN shape.

**ONLY A BASIC PROGRAM CAN TEST THIS.** No verb reaches it, for the reason
above. `verify-fold.ps1` section 4 writes a probe into `BP` — a directory file,
so a record is a file on disk — compiles it and reads five printed answers.

**(b) HAS STARTED, AND `$SAVEDLISTS` IS THE WORKED EXAMPLE — 18 Aug 2026**,
`verify-lcnames.ps1` 36/36 on the 20:34:25 install. The VOC id is now
`$savedlists`. **What one rename costs, in full**: the hard-coded literals (13
`open` sites plus the `recordlocku`/`write` pairs and COPYLST's name
comparisons), `MESSAGES` 3248/3249/3250/6462, `EDIT.LIST` in both `NEWVOC` and
`VOC_TEMPLATE`, `CREATEA:759`, a `START-HISTORY` line per file, a changelog
entry, and a verifier section for the pre-rename account. The name on disk
(`$svlists`) did NOT move and did not need to — (a) and (b) are independent.

**NO MIGRATION, MEASURED.** An account created before the rename holds
`$SAVEDLISTS`; the code opens the literal `$savedlists`; `_VOC_REF` folds UP as
well as down. `verify-lcnames.ps1` §5 renames the id back with a BASIC toggle
(`ZZSVTOGL` into `bp`), drives `SAVE.LIST`/`GET.LIST` through it, and restores
it — a failure part-way leaves the account in the state the section asserts
works, so the failure mode is benign.

**AND "NOT FOUND" IS THE WRONG INSTRUMENT FOR A VOC-ID RENAME.** Two checks
written that way failed on the 20:21:53 install. **`CT` folds the RECORD id as
well as the file name** — `CT:202`, one of the 74 sites — so
`CT VOC $SAVEDLISTS` still finds the record. **`CT:215` prints the id it
MATCHED, not the one typed**, so the echo is the instrument: type
`$SAVEDLISTS`, be answered `VOC $savedlists`. Control: `CT VOC $hold` must
still answer `VOC $HOLD`. Also measured on the 20:34:25 install, because the
changelog promises it: `COUNT $SAVEDLISTS` finds the file, and
`COPY.LIST x,y FROM $SAVEDLISTS` copies and reads back — COPYLST compares the
name with `=` rather than folding, and reaches the file through its generic
three-case `open` instead.

**`$HOLD` IS DONE TOO — 18 Aug 2026**, `verify-lcnames.ps1` 46/46 on the
21:29:59 install. It was the wider one: `CLEANAC`, `MICRO`, `SPVIEW`,
`_NEXTPTR`, `_PRFILE`, `SETPTR`, `CREATEA:759`, `MESSAGES` 7119/7131/7170,
`NEWVOC/SP.VIEW`'s description text, and — new for this rename —
**`VOC_TEMPLATE/$HOLD` renamed to `$hold`**, because in `VOC_TEMPLATE` the
record id *is* the file name and `BBPROC:181` copies each one into SDSYS's own
VOC. `core.ignorecase` is true here, so a case-only `git mv` needs a temporary
name in between.

**THE `"$HOLD "` PREFIX IS NOT A VOC ID AND STILL MOVED WITH IT.** `SETPTR:334`
puts it in front of a hold-file record name and `to_file.c` reads it back
(`start_file()`); it is never looked up, but it is displayed by `sysmsg(7120)`
and `sysmsg(7171)`. **Both sides fold rather than flip** — `downcase(...)` in
`SETPTR`'s three tests, `MemCompareNoCase` in C — because the BASIC half is
built by the bootstrap and the C half by `make sd`, so neither may assume the
other has moved. `_PRFILE:56`'s guard took `downcase()` for the same reason.

**`BP` AND `$COMMAND.STACK` ARE WHAT IS LEFT OF THE CONTROLS**, asserted in
`verify-lcnames.ps1` §3 by typing them in lower case and requiring an upper-case
echo. Whichever moves next takes its control with it.

**THE TCL COMMANDS ARE DONE — 18 Aug 2026, 792 ids**, `verify-lcnames.ps1`
57/57 and `verify-tiers.ps1` 22/22 on the 22:55:26 install. 384 in `NEWVOC`,
397 in `VOC_TEMPLATE`, 11 in `SD.VOCLIB`, plus field 3 of the 22 R records and
the contents of both tier lists. **Excluded and each for its own reason**: the
14 `$`/`%`/`@` records (their own queued renames), the F/Q **file pointers**
(`VOC`, `BP`, `NEWVOC`, `GPL.BP`, `ACCOUNTS`, `MESSAGES`, `SYSCOM`, `QFILE`,
`DICT.DICT`, `MD`, `SD.ACCOUNTS`, `OS.USERS`, `BP.OUT`, `GPL.BP.OUT`), which
are file names and move with (a); the two `T` tier-list records, which are data
and never VOC entries; and `!`, `#`, `&`, which have no case.

**`git mv` PER FILE IS NOT THE WAY TO DO 792 OF THEM.** `core.ignorecase` is
true here, so a plain `git add -A` after a filesystem rename sees **nothing** —
it reported only the content changes and none of the renames. Rename on disk
through a temporary name, then `git -c core.ignorecase=false add -A .`, which
stages all of them in one call (787 as `R`, 5 as add/delete pairs because their
content changed too).

**THE ORIGINAL SCOPE NOTE, kept because the reasoning is still the rule:** Every command id
in `NEWVOC` and `VOC_TEMPLATE`, not only the `$` files. The audit is in this
file's header; what it comes to is that **dispatch already folds and only
COMPARISONS were at risk**, and the nine that mattered were folded on 18 Aug
2026 before any id moved: `UPDREC`, `QPROC` ×2, `CPROC` ×2, `APISRVR`,
`DELETEF`, `SETFILE`, and the tier filter in `LOGIN` and `CREATEA`.

**THE TIER FILTER IS THE ONE THAT WOULD HAVE FAILED SILENTLY.** `LOGIN:576` and
`CREATEA:640` compare the id from a `READNEXT` against `'TIER.OMIT.STANDARD'`
with `=`, and the omit list holds verb ids compared against that id the same
way. Move one side and nothing is omitted: a STANDARD account gets the whole
VOC, and it looks exactly like a filter that worked. Both sides `upcase()` now,
so the list content and the ids can move independently.

**SCOPE, MEASURED:** 387 command ids in `NEWVOC` and 400 in `VOC_TEMPLATE`
(K 238, V 133/143, R 11, P 3/6, S 2) plus `SD.VOCLIB`'s 11. **Out of scope and
deliberately so**: the 14 `$`/`%`/`@` records and the F/Q **file pointers**,
which are file names rather than commands and belong with (a).

**`bp.OUT` IS FIXED AND `BP`, `BP.OUT`, `GPL.BP`, `GPL.BP.OUT` HAVE MOVED —
19 Aug 2026, NOT YET MEASURED.** `BASIC` built the object file name from the
TOKEN, so `BASIC bp X` asked for `bp.OUT` while `CREATE.FILE` made the
directory `BP.OUT` (`CREATEF:378`, `UPSTREAM_FIXES.md` #6). **No case of the
fold reaches a mixed-case id**, so the next `BASIC BP Y` stopped with
`Data pathname 'BP.OUT' already exists`, permanently.

**THE FIX IS TWO HALVES AND EITHER ALONE STILL GIVES A MIXED NAME.** The name
comes from the VOC record that answered the `open` — the read was already
there and discarded the answer — **and the suffix follows that name's case**,
because `'.OUT'` is a literal and would rebuild `bp.OUT` from a lower-case id.
`out.suffix` is used in the Q-pointer branch too: what creates the object file
in the other account is this same program applying this same rule.

**`MICRO` WAS THE TENTH COMPARISON SITE AND THE AUDIT COULD NOT HAVE FOUND
IT.** `MICRO:134` tested `InfileName[-2,2] = "BP"` to decide whether to offer
*"Compile?"* — a comparison against a **substring of a file name**, not
against a VOC id, which is the shape the 281-site grep looked for. It had been
silently broken since 5.12 (a) made the per-account file `bp`. `upcase()`d now.

**WHAT THE ID MOVE COST:** four `voc_template` record renames (there the id
**is** the file name), the `"BP"` default source file in `BASIC`, `CATALOG` ×3,
`CPROC`, `CREATEA`, `FORMAT` and `GENERATE`; `openseq 'gpl.bp'` in `ERRGEN`,
`OPGEN` and `REVSTAMP`; five `$include GPL.BP` lines across `BBPROC` and
`PROG_INFO`; `first.compile`; `second.compile`; `bootstrap.py`; `docs/TCL_VERBS.md`;
a changelog entry; and `verify-lcnames.ps1` §3 and its new §9.

**`$COMMAND.STACK` IS THE LAST CONTROL.** Whatever moves it must bring a
replacement, or §3 can no longer tell a rename from a sweep.

**(a) IS DONE FOR THE PER-ACCOUNT FILES — 18 Aug 2026**, `verify-lcnames.ps1`
26/26 on the 19:46:12 install. A new account holds `$hold`, `$hold.dic`,
`$svlists`, `bp`; `VOC` is deliberately still upper case and is the control,
`cat` was already lower. `CREATEA:737` onwards (`os.name`, not `fn`),
`create.dir.file`'s `.dic` suffix, the create-if-missing fallbacks in
`SAVELST:114`, `COPYLST:179`, `SAVESTK:97`, and `to_file.c`'s three hold-file
paths. **No migration**: each account's VOC names its own files and NTFS matches
either case, so existing accounts are untouched and need nothing.

**`to_file.c`'s HALF CANNOT BE TESTED ON WINDOWS**, and a check that claimed to
was corrected. The literal is a RELATIVE path resolved against the account
directory, so `$HOLD\P1` and `$hold\P1` reach the same place. It passed on a
binary that never contained the change — §6, `assert-current` check A2.

**THIS OVERTURNS THE "ONE COMMIT" CLAIM THIS SECTION USED TO MAKE.** The
fallback can be added, cycled and tested on its own; the renames can then follow
a file at a time, each independently verifiable. Nothing has to move as a single
all-or-nothing change.

**MEASURED 18 Aug 2026 on the 08:44:51 install, and it is what must still hold
afterwards:** `COUNT BP`, `COUNT bp`, `COUNT VOC` and `COUNT voc` all work.

**AND THE ADDITIVE FALLBACK FIXES A LIVE DEFECT, so step one earns its own
cycle rather than being scaffolding.** `CREATE.FILE testlc` writes the VOC id
**as typed** (`testlc`) while upcasing the file on disk and the paths it stores
in fields 2 and 3 (`TESTLC`, `TESTLC.DIC`). Measured on the 08:44:51 install:

```
CT VOC testlc    ->  F / TESTLC / TESTLC.DIC
CT VOC TESTLC    ->  Record 'TESTLC' not found
COUNT testlc     ->  0 record(s) counted
COUNT TESTLC     ->  File not found
```

**So a file created with a lower-case name is invisible to anyone who types its
name in upper case** — on a system that is case insensitive everywhere else.
That is today's behaviour, nothing to do with the conversion, and the `downcase`
attempt is what closes it. The probe was removed afterwards, VOC record included.

**`DHF_NOCASE` IS NOT NEEDED FOR THIS.** It was worth ruling out, because `VOC`
is a **dynamic** file and takes its flags from its own header
(`dh_open.c:549`), so §7 step 8(a) never covered it and `verify-nocase.ps1`
asserts `DHFILE=0` deliberately. But folding one side is what delivers case
insensitivity here, exactly as it does now — the file's own flag is not
involved either way, and `DHFILE=0` should go on being asserted.

**(a) IS DONE IN FULL — 19 Aug 2026**, `verify-lcnames.ps1` **115/115** on the
**07:41:45** install, `sd.exe` `339AB7157F002679`. Every name in the installed
`sdsys` is lower case, and so is each account's `voc`. The new §2a reads the
`sdsys` listing with `-ceq` and asserts **25 lower-case names present and their
25 upper-case spellings absent**; §3 adds `CT VOC VOC` → `voc` /
`@SDSYS/voc.dic` and `CT VOC SYSCOM` → `@SDSYS/syscom`.

```
$cred $hold $hold.dic $ipc $map $map.dic accounts accounts.dic bin bp bp.out
cat dict.dic dir_dict gcat gpl.bp gpl.bp.out messages newvoc os.users
os.users.dic pcode.out prt pstmp sd.voclib syscom voc voc.dic voc_template
```

**THE FACT THE WHOLE THING TURNS ON, and it is not obvious from the names:**
`create.file <path> DYNAMIC` **in BASIC is a language statement and takes the
path exactly as given.** It is *not* the `CREATE.FILE` verb, which upper-cases
the name on disk (`CREATEF:378`). So `BBPROC`'s `FILES_LIST` — seven names and
the `'.dic'` suffix — decides the case of everything the bootstrap creates, and
`CREATEA:581`/`create.dir.file` decides it for each account. **No `CREATEF`
change was needed and `UPSTREAM_FIXES.md` #6 is untouched.**

**What moved together**, and it really is one change: the on-disk names
(**2,968 files**, 12 SDSYS directories, plus 73 record ids in
`gplbld/FILES_DICTS`); the F-type records in `NEWVOC` and `VOC_TEMPLATE` that
carry the path and their `@SDSYS/VOC.DIC`-style dictionary paths; `BBPROC`;
`CREATEA`; 14 more `GPL.BP` programs that `openpath` an SDSYS file
(`APISRVR`, `CPROC`, `CRED_SET`, `CRED_VERIFY`, `DELACC`, `GRANTA`, `LOADLANG`,
`LOGIN`, `MODIFYA`, `PS_SCRIPT`, `SETACC`, `SETFILE`, `SET_ACC_PASSWORD`,
`_VOC_REF`); `gplsrc/messages.c` (the only C-side literal, and the reason
`make sd` was needed); `gplbld/stage.py`, `bootstrap.py`, `sd.iss`,
`pcode_bld.py`, `gen_includes.py`, `CREATE_INSTALL_DICT_FILE`,
`INSTALL_FILE_INFO`; and the scripts that name these paths as literals —
`verify-osusers.ps1`, `-nocase`, `-tiers`, `-fold`, `-catgate`, `-apiport`,
`-nonet`, `-credacl`, `-createaccount`, `cycle.ps1`, `adopt-account.ps1`,
`secure-gcat.ps1`, `secure-psdir.ps1`, `secure-cred.ps1`, `secure-osusers.ps1`.

**THE VOC IDS DID NOT MOVE**, so `$include GPL.BP x`, `BASIC GPL.BP *`
(`SECOND.COMPILE`), `CD VOC` (`THIRD.COMPILE`) and `bootstrap.py`'s
`RUN GPL.BP …` are unchanged and still resolve. `BBPROC` passes `'gpl.bp'` to
`$bcomp`, which reaches VOC id `GPL.BP` through `_VOC_REF`'s **upward** fold —
the half that has always worked.

**`git mv` DOES NOT WORK FOR A DIRECTORY EITHER**, and it fails differently
from the 792-record case: with `core.ignorecase` true, `git add -A` after the
filesystem rename staged 2,968 **additions** and no deletions, because
`lstat("sdsys/GPL.BP/…")` still succeeds against `sdsys/gpl.bp/`. The old index
entries have to be removed by name:
`git -c core.ignorecase=false rm -r --cached sdb_ai/sd64/sdsys/<OLD>` per
directory, after `git -c core.ignorecase=false add -A`. 2,950 then came out as
`R` and 18 as add/delete pairs — the small records whose content changed too.

**THE CHEAP CHECK BEFORE SPENDING A CYCLE**, because `os.path.exists` cannot
make it on NTFS: import `stage.py` and compare `SDSYS_SHIP`/`SDSYS_EMPTY`
against `os.listdir(sdsys)` as a **set**, case-exactly. A `.ps1` parse sweep
(`[Parser]::ParseFile` over `gplbld\*.ps1`) is the other one. Neither says the
bootstrap works; both catch the typo that would waste the install.

*(Unrelated but found while surveying: the installed `sdsys` contains an empty
directory literally named `C:`. Something builds a path where a bare file name
was expected. Still there after this rename, harmless, and nobody has looked
at it.)*

**`$COMO` IS THE ONE PER-ACCOUNT NAME LEFT UPPER CASE**, deliberately.
`COMO:44` and `PHANTOM:59` define the on-disk name and the VOC id with the same
`$define`, so splitting them is `CREATEA`'s `fn`/`os.name` pattern again — and
nothing in `gplbld` drives `COMO`, so it would ship unmeasured.

### 5.20 `cub1` was empty because NO type had loaded, not because cub1 was missing (22 Aug 2026)

> ## SETTLED ON A CYCLED TREE - install 22 Aug 20:57:34, `assert-current` exit 0.
>
> **THE FIRST LOOKUP DOES FAIL, AND THE FALLBACK IS WHAT SAVES IT.** Measured
> with the probe as the login paragraph's **FIRST SENTENCE**, which is the only
> place that sees the state `$LOGIN` leaves:
>
> ```
> term.type  = [windows]        env.TERM   = [xterm-256color]
> cub1.len   = 1 (byte 8)       kbs.len    = 1      el.len   = 3
> cup.len    = 16               clear.len  = 6      at.cs.len = 6
> ```
>
> ***`term.type` IS `windows` WHILE `env.TERM` IS `xterm-256color`, AND THAT IS
> THE WHOLE PROOF.*** Had the first lookup succeeded, `settermtype()` would have
> stored the name it was given. `windows` can only have come from the fallback,
> so the attempt before it failed. **The defect is real and the fix works.**
>
> **AND THERE IS NO LAUNCH-CHAIN DIFFERENCE** - the suspicion this section
> carried for an hour. PowerShell `Start-Job` and `cmd /c` give **byte-identical
> probe output**.
>
> ***WHY EVERY EARLIER READING WAS WORTHLESS, which is the reusable part:*** they
> were taken at the `:` prompt, which is **always after** the paragraph has run
> `TERM WINDOWS`. A question about `$LOGIN` can only be answered from inside the
> paragraph's first line. The `-Cleanup`-style toggle that puts it there and
> takes it out again is three dozen lines of BASIC and is worth rebuilding rather
> than re-deriving.
>
> **ONE THING IS STILL UNEXPLAINED AND IS NOT CLAIMED AS UNDERSTOOD.** A raw
> byte capture on the **pre-fix** build began with `27 91 72 27 91 74` -
> `ESC[H ESC[J`, once, immediately before the `LOGIN:278` banner. With no
> fallback, `LOGIN:200`'s `@(-1)` should have been empty there, and **nothing in
> C hardcodes that sequence** (grepped). That capture was taken on an already
> stale tree, with a runaway session and two `Stop-Process` kills in flight, so
> it is the least trustworthy datum here - but it is not explained. **What would
> settle it:** capture the same bytes from a build without the fix, on a clean
> tree.

**Answers the open item "WHY `cub1` CAME BACK EMPTY".** Measured on the
22 Aug 19:38:32 install, `assert-current` exit 0.

**THE FIRST `settermtype()` OF THE SESSION FAILS, AND UNTIL ONE SUCCEEDS EVERY
CAPABILITY IS EMPTY** — not just `cub1`. `tsettermtype()` calls
`free_terminfo()` only after the open succeeds (`sdtermlb.c:167` and `:173`), so
a name with no entry leaves `tinfo` NULL on the first call, and `sdtgetstr()`
then returns `""` for every id (`sdtermlb.c:395`). `tio.term_type` is assigned
only on success (`sdtermlb.c:329`).

**THE NAME IS `xterm-256color` AND WINDOWS DID NOT SET IT.** The MSYS2 runtime
supplies it: TERM is empty at Machine, User and Process scope, and `env('TERM')`
inside SD answers `xterm-256color`. `terminfo/x` holds only `xterm`.

**THE PROMPT IS INSIDE `$LOGIN`, THE REPAIR IS AFTER IT.** `require.credential`
is `LOGIN:592`; the VOC `login` paragraph's `TERM WINDOWS` is run by
`CPROC:411`, and `$LOGIN` is called at `CPROC:324`. So the password prompt — and
the clear screen — are the only places in a session that are always in the
unrepaired state.

***THE PIPE WAS NEVER THE DIFFERENCE. THE TIMING WAS.*** Every piped
measurement is taken at the `:` prompt, after the paragraph has run. That is
why `verify-keys` passed while the owner watched backspace fail, and why the
22 Aug note said a piped session "emitted byte 8 correctly".

Measured with `don`'s `login` paragraph lifted out, i.e. the state `$LOGIN`
leaves:

| TERM | `@TERM.TYPE` | cub1 | kbs | el | cup | `@(IT$CUB)` |
|---|---|---|---|---|---|---|
| unset - runtime gives `xterm-256color` | empty | 0 | 0 | 0 | 0 | **0** |
| `zzz` | empty | 0 | 0 | 0 | 0 | **0** |
| `xterm` | `xterm` | 1 (8) | 1 (127) | 3 | 16 | 1 (8) |
| `windows` | `windows` | 1 (8) | 1 (127) | 3 | 16 | 1 (8) |

**`kbs` WAS EMPTY TOO**, so `_INPUT:90`'s lookup returned nothing at that
prompt. The 19 Aug `_KEYCODE` fix and `erase.keys = char(8):char(127)` were both
working around this, and the `char(8)` erase of 22 Aug stands - it is the right
change independently, and this makes the capability correct as well.

**THE FIX, `LOGIN`:** downcase, ask, and check. `kernel(K$TERM.TYPE, s)` returns
the type in force after the attempt and leaves it unchanged on failure
(`op_kernel.c:226-232`), so a mismatch is the failure; fall back to `windows`.
`TERM:245-246` is the same test on the same two calls. **NOT MEASURED ON AN
INSTALL YET** - it is a source change made after this cycle, so it owes a
`cycle.ps1`.

***WHAT THE FIX DOES NOT DO, AND THE FIRST WRITE-UP OF IT SAID OTHERWISE.***
Owner, 22 Aug 2026: *"the installers password prompt was already fixed"*.
Correct, and it makes the obvious test worthless - **it passes either way**:

- `_INPUT:187` erases with `char(8)` and never asks for the capability.
- `_INPUT:117`'s `erase.keys = char(8):char(127)` is additive, so the empty
  `kbs` at `:90` costs nothing either.
- `sd -QUIET off` skips `LOGIN:200`'s clear screen **twice** - `system(1026)`
  is `off`, and `CMD.QUIET` is set.

**So the installer session has no capability-dependent output left, and this
change is a no-op there.** What it fixes is `LOGIN:200` for an ordinary
interactive session - the sign-on clear screen, the only `@()` call left in
`$LOGIN` besides the `sdterm`-only `:205` - and the root cause the two `_INPUT`
changes were working around. **That, not backspace, is what a cycle has to
show.**

*`clear` was not measured empty directly; cub1, kbs, el and cup were. It
follows from the code rather than from the table: `sdtgetstr()` returns
`null_string` at `sdtermlb.c:395` before it ever looks at the name, so with
`tinfo` NULL every id is empty.*

**UPSTREAM HAS IT TOO — `UPSTREAM_FIXES.md` #12.** `LOGIN:79` unchecked,
`terminfo/x/xterm` only, `CPROC:284-285` against `:366`, and its clear screen is
`LOGIN:97` inside the same subroutine.

***AND IT CORRECTS A CLAIM IN §5.18***, which is why this took three sessions to
find: that section says `env('TERM')` "never runs" and that `$TERM` cannot
change the terminal type. Both are wrong, and wrong for the same reason as the
`cub1` question — the measurement behind them was taken at the `:` prompt.

### 5.19 REMOVED WITH ITS SUBJECT: the full-screen editors are gone (23 Aug 2026)

**`SED` and `UPDREC` were removed from the system on 23 Aug 2026** (§7 step 10's
neighbour, and the changelog entry of that date), so the key-table work this
section recorded has nothing left to apply to and `verify-editkeys.ps1` went with
them. Compressed under §0.5; **HISTORY, 19 Aug, holds the measurements** - the
before-and-after tables, `UPDREC`'s arrows typing themselves into the record, and
`SED`'s bindings as the worked example.

**THE PART THAT IS STILL LIVE IS IN §5.17 AND §5.18, NOT HERE**: on this platform
Backspace is `127` and Delete is `ESC [ 3 ~`, measured from three console hosts.
That governs the COMMAND LINE, which still exists, and `verify-keys.ps1` still
measures it.

**AND THE ONE CORRECTION WORTH CARRYING: `ED` WAS NEVER AFFECTED.** §5.17 listed
it and was wrong - `ED` is the LINE editor, reads whole lines with `input`, and
goes through the command-line editor `_KEYCODE` fixed. It is also the editor this
system now uses, so if backspace is ever reported broken in `ED`, that is a new
fault and not this one coming back.

### 5.18 The arrow keys were dead because of the default terminal type (19 Aug 2026)

**Owner, 19 Aug 2026: left arrow, right arrow, backspace and clear screen do
not work in cmd, PowerShell or Windows Terminal.** Root cause found and fixed;
the arrows are measured, clear screen is not a defect (below).

**IT IS A REGRESSION FROM 18 AUG, NOT FROM THE BACKSPACE FIX.** `changelog:305`
changed the `login` paragraph in `voc_template` and `newvoc` from `TERM LINUX`
to `TERM VT100`, reasoning "on Windows the sensible default is VT100". Backwards:
the entry named `linux` is the ANSI/normal-cursor-mode one, and that is what
every Windows console speaks. Measured on the 09:10:45 install, all four cells:

| TERM | `kcub1` | sends `ESC [ D` | sends `ESC O D` |
|---|---|---|---|
| `vt100`, `xterm` | `\EOD` | **dead** | works |
| `linux`, `ansi` | `\E[D` | **works** | dead |

**THE `ESC O` SPELLING CAN NEVER ARRIVE, AND THAT IS THE WHOLE ARGUMENT.** A
terminal sends it only in APPLICATION CURSOR MODE, entered by `smkx`
(`ESC [ ? 1 h`). **SD never sends `smkx`** — the string occurs nowhere in the
tree but `gplsrc/ti_names.h:179-180`, the capability-name table. `settermtype()`
(`op_tio.c:2524`) sends `is1` only, and `is1` is absent from `vt100`, `xterm`,
`ansi` and `linux` alike, so SD sends nothing at all at terminal init. So a
`vt100` default listens for a byte sequence nothing on the platform emits.
`kbs` is the same story one key over — that was §5.17.

**THE FIX, owner's ruling: one type that matches Windows.** `terminfo.src` gains
`windows`, a **byte-exact copy** of `linux` (verified with `cmp` on the extracted
capability lines; the `kbs=\177` literal DEL survives the copy). `login` field 2
in `sdsys/voc_template/login` and `sdsys/newvoc/login` is `TERM WINDOWS`, and
`LOGIN:116`'s fallback is `'windows'`. **The other 61 entries are still shipped**
— the owner asked for a copy and a default, not a cull.

***THE PARAGRAPH-IS-WHAT-DECIDES CLAIM THAT STOOD HERE IS WRONG — §5.20,
22 Aug 2026.*** It said `system(7)` already answers by the time anything can
look, so `LOGIN`'s `env('TERM')` branch never runs, and that neither `$TERM`
nor `sd -TERM` changes the terminal type. **`env('TERM')` decides it for the
whole of `$LOGIN`**, which is where the password prompt and the clear screen
are; the paragraph runs at `CPROC:411`, after `$LOGIN` returns at `:324`, and
only repairs it from the `:` prompt onwards. The measurement behind the old
claim was taken at that prompt. Both places must still name the same type.

**CLEAR SCREEN WAS NEVER BROKEN.** `@(-1)` emits `27 91 72 27 91 74` =
`ESC [ H ESC [ J`, and `@(5,3)` emits `ESC [ 4 ; 6 H` — both correct, measured
with a `seq()` probe. `clear` is identical in `vt100`, `linux` and `windows`,
so the terminal-type change could not have affected it either way.
**Owner confirmed "CS works correctly", 19 Aug 2026**, at a console. Treat it
as collateral in the original report rather than a fifth fault.

**`sd.exe` LINKS `msys-2.0.dll`**, so the terminal layer is Cygwin's console
handler, which is what translates key presses into these byte sequences and
tracks application cursor mode by watching the output stream. That is why the
protocol argument above holds for cmd, PowerShell and Windows Terminal alike.

**A PIPE IS NOT A CONSOLE, AND EVERY INSTRUMENT HERE IS A PIPE.** `verify-keys`
passed 6/6 on backspace while the owner was reporting backspace as broken. The
gap is real and is the reason the clear-screen half is still open.

**`verify-keys.ps1` IS THE GUARD, 6 → 10 CHECKS.** Section 3 types `COUNTVOC`,
LEFT ×4, RIGHT ×1, space: `COUNT VOC` if both arrows moved the cursor,
`COUN is not in your VOC` if only LEFT did, `COUNTVOC is not in your VOC` if
neither — one run, three distinguishable answers. Controls: the `ESC O` spelling
must **not** count, and no arrows at all must be refused.

**AND `sdtic` HAD A DEFECT THAT COST THIS SESSION A BUILD — `UPSTREAM_FIXES.md`
#9, fixed here.** `reset_buffers()` sat inside `if ((errors == 0) && !skip)`, so
a failed entry left `strings[]` and `str_count` to accumulate into the next one;
the full database with one bad entry **segfaulted at 24 files of 100** and, with
stdout block-buffered to a file, printed nothing. `sdtic` also always exited 0.
Both fixed: the reset is unconditional and a failed entry now fails the run.
Found by giving the new entry a description containing a comma — `get_token()`
splits on commas, so `Windows Terminal)` was read as a capability name.

**`gplbld\probe-keys.ps1` IS THE INSTRUMENT, AND IT IS THE ONLY ONE HERE THAT
IS NOT A PIPE.** It compiles `ZZKEYPROBE` into the caller's own `bp`, starts a
plain `sd` in the current console, and prints every byte each key sends, naming
an arrow's spelling as it goes. **Reach for it whenever a keyboard question
comes up** — next step 2, backspace in the full-screen editors, is the same
class of problem and has no instrument of its own yet.

* **The program is LEFT INSTALLED**; `-Cleanup` removes it and stops. It used
  to be removed on exit, and the second console was then told
  `RUN BP ZZKEYPROBE` and answered that it did not exist. `-Cleanup` is exempt
  from the console guard and from `assert-current` — removing a file needs
  neither, and a guard that blocks the undo gets worked around.
* **It refuses if stdin is redirected.** Piping in would measure the pipe and
  answer the wrong question confidently, which is what it exists to prevent.
* **It checks the OBJECT exists in `bp.out`**, not just that the compiler said
  `0 error(s)` — `RUN` needs the object.
* **`@(0,0)` disables pagination.** A cursor POSITIONING call does that; a
  special function like `@(-1)` does not. Without it the pager fires mid-listing
  and **the key pressed to dismiss it is itself a keystroke**.
* **`sd <command>` is elevation-gated** (`sd.c:734`), so it cannot run the
  program for you; the operator types `RUN BP ZZKEYPROBE`. Elevating to avoid
  that would change the session under test. **Elevation does NOT change the
  account** — measured, an elevated `sd` still lands in `DON`, not `SDSYS`.
* **Nothing captures its output.** SD writes to the console directly.

### 5.17 The keyboard: accept both spellings of a key, not the one terminfo names (19 Aug 2026)

**The backspace key did nothing at all in cmd, PowerShell or Windows Terminal**,
and nothing in PuTTY unless its "Backspace key" setting was changed to
Control-H. Reported by the owner, 19 Aug 2026.

**A terminal sends one of two bytes for backspace — Ctrl-H (8) or DEL (127) —
and nothing in the protocol says which.** `_KEYCODE` built its table from
terminfo (`code = K$BACKSPACE ; key.string = tinfo<T$KEY.BACKSPACE>`), so SD
accepted whichever byte `kbs` named and let the other fall through as a literal.
`CPROC:835`/`972` have a `case` for `K$BACKSPACE` and none for 127, so it was
silently discarded.

**MEASURED: every Windows console host sends DEL.** `LOGIN:115` takes
`env('TERM')` and `LOGIN:116` defaults an unset one to `vt100`, whose `kbs` is
`^H` — and `TERM` is unset on this machine. So the platform this port exists for
had a dead backspace out of the box.

**NO CHOICE OF TERMINAL TYPE COULD HAVE FIXED IT, which is the part worth
keeping.** Of the 62 entries in `terminfo.src`, **51 say `^H`** (39 as `^H`,
12 as `\b`), one says `^Y`, eight have no `kbs` at all — and **only `xterm` and
`linux` say DEL**. That is why `vt100-w` looked like it should have helped and
did not: it is the **wide** 132-column variant, `cols#132` and a different
`rs2`, and every key capability is identical to `vt100`. `vt100-at` (AccuTerm,
which genuinely is a Windows emulator) is `kbs=^H` too.

**THE FIX BINDS BOTH BYTES, BEFORE THE TERMINFO BINDS.** `bind` *replaces* an
existing binding, so the two defaults are overridden by anything terminfo
claims: `vt100-at` has `kdch1=` and keeps DEL as its Delete key, while
`vt100` — which has no `kdch1` at all — leaves 127 unclaimed and gains a working
backspace. **Additive in the same sense as the three-case fold**: it turns a
lookup that finds nothing into one that finds something, and changes no lookup
that already succeeds.

**CHANGING THE DEFAULT TERMINAL TYPE WAS THE OTHER CANDIDATE AND WAS REJECTED.**
`LOGIN:116` could default to `xterm`, and the owner confirmed `TERM xterm` fixes
all three consoles. But it would then break every terminal that sends `^H`,
because `xterm`'s `kbs` is DEL and `^H` would be the unbound one — the same bug
pointing the other way. It also changes `cols`, colours and the function keys
for everyone. Binding both is strictly better and touches nothing else.

**IT IS TESTABLE FROM A PIPE, WHICH IS WHY IT HAS A VERIFIER AT ALL.**
`keyin()` reads stdin, so a byte piped in reaches the command-line editor
exactly as a keystroke does — the same property behind the BOM trap in §6. The
instrument is **what SD executes**, not what it echoes: `COUNTX<erase> VOC` runs
`COUNT VOC` and answers "422 record(s) counted" if the erase worked, and
`COUNTX VOC` and answers "not in your VOC" if it did not. `gplbld/verify-keys.ps1`,
unelevated, needs no account and no terminal.

**THE EDITORS WERE THE SAME FAMILY, WERE FIXED ON 19 Aug, AND WERE REMOVED ON
23 Aug — §5.19.** `UPDREC` read raw bytes with `keyin()` and carried its own
table, and `SED` did the same; both bound `char(127)` to Delete, so Backspace
deleted forwards inside them. **Neither exists now**, so what is below applies
to the command line alone.

**TWO THINGS THIS PARAGRAPH USED TO SAY ARE WRONG, and §5.19 has the
measurements.** It listed **`ED`**, which is the LINE editor: it reads with
`input`, so the `_KEYCODE` fix above already covers it and DEL erases backwards
there today. And it said a test "needs a console" — it does not. `keyin()` reads
**standard input**, so a full-screen editor is drivable from a pipe, and the
instrument is the record it saves rather than the screen it paints.
`gplbld/verify-editkeys.ps1` was that test, **until `SED` and `UPDATE.RECORD` were removed on 23 Aug 2026 and it went with them** (§5.19).

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

### 5.14 Administrative logic goes in a subroutine, because the forms are a SEPARATE PROJECT (owner, 23 Aug 2026)

**THE FORMS THEMSELVES ARE OUT OF SCOPE HERE.** Owner's decision, 23 Aug 2026:
they belong to **a set of GUI utilities that will be created**, and they are
**not necessary for a working SD**. §7 step 10 is removed on that ruling. What
was a goal for "after the system runs well" is now somebody else's deliverable,
and this file should stop implying SD owes it.

**THE RULE SURVIVES, AND IT MATTERS MORE THAN IT DID, NOT LESS: new
administrative capability goes in a SUBROUTINE with a verb over it**, not in a
verb that holds the logic. While the forms were going to live here, that was a
convenience — a later form could call the same code instead of reimplementing
it. Now that they live in another project, it is the only way in: **something
outside this repository can call a catalogued subroutine or the API, and can do
nothing whatever with logic buried inside a verb** except drive the verb blind
and scrape what it prints.

`GPL.BP/CRED_SET` and `CRED_VERIFY` with `SET_ACC_PASSWORD` over them are the
pattern to copy, and `SET.PASSWORD` is already prompt-driven, which is the right
precedent.

**WHAT IS STILL SHAPED LIKE A COMMAND LINE, for whoever writes those utilities:**
the grants verb (§7 step 5), edited through `MODIFY ACCOUNTS`; `os.users` (§7
step 7) and `batch.jobs` (§7 step 9), both edited with `ED` from SDSYS. The
batch list is the one with rules a form could enforce at the point of setting up
rather than at 3am — a single name, no arguments, `PA` or `S` only — which §7
step 9 records as the part it could not fully deliver without a verb to edit the
list with.

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
| ~~`PLATFORM_NAME "Linux"`~~ — ***DONE 26 Aug 2026***, it is `"Windows"` and the token is `SD.WINDOWS` | `gplsrc/sddefs.h` | done |
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

### 5.24 The BASIC functions and operators, verified (31 Aug 2026)

***THE SURFACE IS SOUND. 169 VALUE CASES, 0 FAILURES, ON THE 13:33:28 INSTALL***
— `gplbld/verify-basicfuncs.ps1` with `gplbld/basicfuncs.sb`, run unelevated in
`don`'s own bp on PRE_RELEASE 94's probe model and removed again. **This is the
question under §5.23**: the sweeps asked whether a status was discarded; this
asks whether the language returns the right answer at all, which every query in
the system is built out of.

**STRUCTURAL, FIRST, BECAUSE A VALUE TEST CANNOT SEE ANY OF IT.** Four links,
each measured with a control:

| link | result |
|---|---|
| BCOMP's parallel tables `intrinsics` / `intrinsic.opcodes` | **176 = 176**, zero lines assigning one half only |
| compiler include vs runtime header | `gen_includes.py --check` — **all four in sync, byte-for-byte** |
| every intrinsic's `OP.xxx` is defined | **172 used, 172 resolve**, 0 missing; a bogus name IS reported missing |
| opcode number == `dispatch[]` position | **512 entries, 0 mismatches**, both banks; an injected break reports exactly 1 |

***THE DESIGN IS WHY THEY ALL PASS AND IT IS WORTH KNOWING.*** `gplsrc/opcodes.h`
is an X-macro table — `_opc_(0x2A, OP_ABS, "ABS", op_abs, …)` — and
`kernel.c:75` builds `dispatch[]` by `#include`ing it. **One file carries the
number, the C name, the BASIC name and the handler**, `gpl.bp/OPCODES.H` is
generated from it, and a missing handler is a link error. Drift is structurally
impossible rather than merely absent. **Do not re-audit this by hand.**

***BEHAVIOURAL: EVERY ONE OF THE FIRST RUN'S 20 "FAILURES" WAS THE TEST'S
EXPECTATION, NOT THE PRODUCT.*** That is the result, and the traps are worth
more than the tally because each is one a programmer will hit. **They are
recorded at the case in `basicfuncs.sb`, not repeated here** — `MD` inserts a
point rather than rounding; `SHIFT`'s positive count goes **right**;
`CONVERT(from, to, source)`; `SUBSTITUTE` splits its source by **marks** and the
delimiter splits the old/new *lists* (`gpl.bp/_SUBST`); `LOCATE arr<1>` searches
**fields**; `VSLICE` takes value N of each field; `RAISE` promotes @vm to @fm;
`ASCII()` takes EBCDIC in; `DTX` returns **lower case** (`%x`, byte-identical
upstream); `MTH`'s am/pm case is `OptAMPMUpcase`, defaulting lower.
**The documentation was right wherever it says anything** — `CONVERT` and
`SUBSTITUTE`'s signatures both match what was measured.

**WHAT IS NOT COVERED, STATED SO THE CLAIM IS HONEST**: the probe's header lists
every excluded intrinsic and why — terminal-blocking, sockets, file or select
list, session state, printer state, and the ones that change the process.
**169 cases is not 176 functions**: some functions carry several cases and the
excluded ones carry none.

***WIRED INTO `VerifyInstall1` ON THE OWNER'S RULING, 31 Aug 2026*** — beside
`verify-txn.ps1`, which is the same shape. **17 steps now, up from 16.**
***PROVED WITHOUT A RUN TOKEN, BECAUSE §4.0.1 FORBIDS THE AGENT RUNNING THE
RUNNER***: the step list was lifted from the file and driven through
`suite-only.ps1`'s `Select-SuiteSteps` — `-Only verify-basicfuncs` selects
exactly 1 with `Partial` true, two names come back in **runner order**, and a
typo'd name is refused by name. **That is how to check a wiring here; do not
spend a `-Run` on it.**

**Re-deriving the header counts turned up PRE_RELEASE 107**: `verify-tierchange.ps1`
is in neither runner and is the parent of `verify-acctmsgs` and `verify-vocverbs`,
so three never run. **It wants the ELEVATED runner and is filed, not wired** —
that is the owner's command to change.

### 5.23 A query must never answer wrongly (owner, 31 Aug 2026)

*"`LIST ACCOUNTS` must be absolutely accurate. Administrators must never receive
an answer to a query that is wrong — this is a blocking defect."*

***IT IS A PRINCIPLE, NOT A RULING ABOUT ONE VERB, AND IT PROMOTES ANYTHING IT
REACHES TO `B`.*** Said of PRE_RELEASE 93 and quoted here because its scope is
wider than that entry: an administrator acts on what a query tells them, so a
listing that is merely *usually* right is worse than one that refuses — they
cannot tell which rows to trust.

***THE COROLLARY, AND IT IS THE WIDER RULE — OWNER, 31 Aug 2026:*** *"This is a
database application. No failure is more severe than misreported data, not just
to the administrator but for every user."*

***SO THIS IS THE SEVERITY ORDERING FOR THE WHOLE PROJECT, NOT A RULE ABOUT
LISTINGS.*** Storing data and giving it back is what SD is for; returning the
wrong answer is the worst thing it can do, and it outranks a crash — a crash is
visible and a wrong answer is not. **Anything in this class is `B`.**

***THE CORE DATA PATH HAS ONE RECORDED INSTANCE AND IT IS THE ARCHETYPE***:
PRE_RELEASE **11**, the silent transaction data loss — a nested `COMMIT`
abandoned the outer transaction and its writes vanished with **no error, no
warning and nothing in the log**. **Fixed, and it earned a standing verifier**
(`verify-txn`, 9 of 9) precisely because a silent wrong answer is the kind that
comes back unnoticed. **No open entry is on the core data path today** — the two
live ones are metadata.

***CLASSIFIED AGAINST THE COROLLARY, 31 Aug 2026. THE FIRST TWO ARE MEASURED;
THE REST ARE A READING AND WANT THE OWNER'S EYE BEFORE ANY SEVERITY MOVES.***

| | entry | what it tells someone untrue |
|---|---|---|
| **in the class, measured** | **93** | `LIST ACCOUNTS` names accounts that do not exist |
| | **65** | `LIST OS.USERS` names grants for accounts that do not exist |
| | **94** | `CREATE.ACCOUNT` says "%1 is now an SD administrator" on a grant that did not happen |
| | **95** | a failed header flush marks the file clean, so `record_count` on disk can disagree with the data — needs an I/O error, and `dh_close` is where it does not self-heal |
| | **96** | a privilege check that could not complete is reported as "not an administrator" — the audit line states a reason nobody established, and `sd.c:838` tells an elevated administrator to elevate |
| | **97** | `MODIFY.ACCOUNT` says the `os.users` record is removed, and the VOC removal count, from a `delete` whose failure was discarded — 65's symptom by a second route |
| | **98** | the trail says `ELEVATION GRANTED` for a session refused before the rights were given — an event that did not occur, where 96 is a reason never established. The one open entry whose trigger needs no induced fault |
| | **99** | the API session's identity, which stamps every audit line, is set by a call whose refusal is discarded; a checked neighbour thirty lines later is the only thing that catches it |
| | **100** | an AK node allocator answers "could not" with 0, nobody tests it, and node 0 is the index header — a transient write error becomes permanent corruption of what every query on that key is answered from. **The one entry with no self-heal** |
| | **101** | `DELETE` on a directory file inside a transaction cannot fail — the record survives, the commit reports success, and the next query returns it. **Filed B: the only open entry besides 93 and 94 whose trigger is an ordinary state, not an induced fault** |
| | **102** | a commit that fails half way is partly applied, cannot be rolled back, and never releases its locks. **11's leftover, recorded only inside a struck entry until now** |
| | **103** | `WEOFSEQ` and `OPENSEQ … OVERWRITE` report success on a truncate that did not happen, so the file keeps its old tail — and `SetFileSize` is a `bool` that always answers TRUE |
| | **104** | `DELETE.FILE` orphans a relocated alternate-key index and discards the delete. **Not in the class and the row says so** — 6136 and 6141 are true, the index is simply left behind |
| | **105** | a verifier's compile check anchors on the argument it passed in, so only its disqualifier does any work. **Instrument, not product** — the class §5.23 exists to stop being measured badly |
| **candidates, my reading** | **67** | the mode page's caption calls ssh optional; a full install always installs the server |
| | **89**, **88** | a control the user clicks expecting an action, and none follows |
| | **20** | the register says `SUSPENDED` while the person keeps Windows administrator rights |
| **not in the class** | 6, 16, 28, 66, 70, 74, 76 | litter, a missing message, confidentiality, or missing function — none states a falsehood |

**80 is already `B` on its own account** and belongs here too: documentation that
describes a model the product no longer has is the same failure in prose.

***TWO FILES ANSWER WRONGLY TODAY, MEASURED ON THE 13:33:28 INSTALL***, and
both are queryable because `voc_template` gives each an F-pointer and a
dictionary:

| query | records | wrong |
|---|---|---|
| `LIST ACCOUNTS` (and `LIST SD.ACCOUNTS`) | 28 | **26** dead — PRE_RELEASE 93 |
| `LIST OS.USERS` | 6 | **5** dead, each `yes\|yes` — PRE_RELEASE 65 |

**Both hold a row whose subject is an OS object that has gone**, and nothing in
SD reconciles either. `batch.jobs` is the third queryable file of this shape and
is empty, so it is untested rather than clean.

***IT SETTLES 65's OPEN QUESTION AND THE ANSWER IS "NOT ENOUGH".*** 65 asked
whether documenting the recovery — *"remove with `DELETE.ACCOUNT`"* printed at
teardown — was acceptable in place of removing the record. **It is not, and the
reason is this section**: a note in a transcript nobody reads does not make
`LIST OS.USERS` true. ***AND IT DECIDES BETWEEN THE TWO FIXES THAT WERE ON THE
TABLE***: a start-of-run sweep leaves the query wrong *between* runs, so the
removal has to happen when the account goes.

**THE DISTINCTION THAT MAKES THAT SAFE IS ALREADY IN THE FILES** — `os.users`
is *"the one leftover that is a PERMISSION rather than a register entry"*, so
removing it hides nothing about a half-failed `CREATE.ACCOUNT`, which is what
the 30 Aug decision was protecting. The `ACCOUNTS` record is the evidence and
stays.

### 5.22 What an administrator has as themselves, and what needs SDSYS (owner, 31 Aug 2026)

*"Administrators logged in as themselves need to have full access to everything
EXCEPT the ability to issue the restricted administrator commands. They have to
log to sdsys to do that."*

| | as themselves | in SDSYS |
|---|---|---|
| enter any account, **no grant needed** | yes | yes |
| the 41 capabilities (`TIER.OMIT.STANDARD`) | yes | yes |
| the 24 restricted commands (`TIER.ADD.ADMINISTRATOR`) | **no** | yes |

***"ADMINISTRATOR" MEANS BOTH, AND THAT WAS DECIDED EARLIER.*** Owner, 31 Aug
2026: *"an administrator has to be both a windows administrator and an sd
administrator… accounts created outside of sd do not have access to sd unless
they are granted access from within sd."* **This is already built and already
recorded** — do not re-derive it:

- **`LOGIN:573` is the predicate**, and any new test should reuse it rather
  than invent one: `kernel(K$ADMINISTRATOR, -1) and kernel(K$OS.ADMINISTRATOR, 0)`.
- **`LOGIN:417`** refuses a non-`sdusers` Windows user with 5009,
  `reason = 'not a member of sdusers'`.
- **`LOGIN:388-413`** carries the owner's sentence: *"if any are built outside
  of sd they do not have access to sd until a matching standard or programmer
  account is created in SD."*
- **Entry 56** removed the administrator exemption — *"the `sdusers` gate is
  uniform across all three tiers"* — proved by `-Run b66`.
- **It is an explicit act and an audit trail, not a boundary against a Windows
  administrator**, who can add themselves to `sdusers`. `LOGIN`'s own comment
  says the owner was shown that before ruling. **Do not re-argue it** — §5.6.1
  and the 30 Aug *"this is our default setup, not a prevention"* ruling cover
  the same ground.

***ACCESS AND PRIVILEGE ARE DIFFERENT QUESTIONS, AND CONFLATING THEM IS
PRE_RELEASE 91.*** Which accounts a person may ENTER must not be answered with
the flag that says what the session may DO — `CPROC:2823` clears that flag on
every `logto` out of SDSYS, by the 16 Aug ruling, and access must survive it.

### 5.21 No control may be inert (owner, 31 Aug 2026)

*"No option should be available that the user can click thinking that an action
is going to take place, but nothing happens (for example an option that says
install a server when it is already installed and clearing the selection does
nothing)."*

**A tickbox is a promise about what the installer is about to do.** One that
cannot act is a false statement, and the cost is not the wasted click — it is
that the reader believes they have made a choice. This generalises the owner's
earlier rule about the `limitssh` box, already quoted at `sd.iss:338`: *"seeing
a tick box a user just assumes it is an option."*

**Two ways to satisfy it, and the file already contains both.**

- **Do not offer it.** `sshserver` carries `Check: SshServerAbsent`
  (`sd.iss:186`), so the box is absent on a machine that already has a server.
- **Make it act in both directions, and pre-set it from the truth.**
  `sshremoteshut` / `sshremoteopen` are defaulted from the live firewall scope
  (`GetSshRuleIsOpen`), and `ApplySshFirewall` runs `-Open` or `-Restrict` on
  every install — so a deliberate click always moves something and touching
  nothing changes nothing. That is §PRE_RELEASE 76's ruling, and it is the
  better of the two whenever the state is real rather than absent.

***IT APPLIES HARDEST ON AN UPGRADE, WHICH IS WHERE IT IS CURRENTLY BROKEN.***
An upgrade preserves configuration and re-runs little, so a control that acts
on a first install can be inert on the second. **PRE_RELEASE 89 carries the
audit of all seven `[Tasks]` entries**: five clean, and two not — `apiremote`,
because `sd.conf` is `onlyifdoesntexist` and *"an upgrade rewrites nothing
either way"* (`sd.iss:517`), and `addtopath`, because nothing removes SD from
`PATH` outside the uninstaller (`:3810`). **Neither is fixed; the ruling is
recorded so the next control is not built the same way.**

**Check a new control against this before writing it**, and check both
directions: the off direction is the one that fails, because the on direction
is the one anybody thinks to test.

## 6. Traps

Each of these cost real time. Read before debugging anything similar.

- ***A PROCESS-LIST PROBE MATCHES ITSELF, AND REPORTS A STRAY THAT IS THE
  QUESTION.*** Found 28 Aug 2026 checking whether the elevate-once helper had
  been left running after `-Run b54`.

  `Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like
  '*sd-elevate-helper*' }` returned **1**, and the one was **the PowerShell
  process running that very query** — its own command line contains the pattern.
  The verdict *"an elevated helper survived the run"* was wrong, and it was
  wrong in the alarming direction.

  ***THIS PROJECT IS FULL OF THE SHAPE IT BREAKS***: "no stray `sd.exe`" is a
  standard end-of-run check, and any command-line search for a script's name
  will match the searcher whenever the searcher names it.

  **THE FIXES, and the second is the one that survives being copied:**

  1. **Exclude `$PID`.** `Where-Object { $_.ProcessId -ne $PID -and ... }`.
  2. ***PREFER EVIDENCE THAT CANNOT NAME ITSELF.*** For a named-pipe server,
     ask whether the **pipe** is open — `[System.IO.Directory]::GetFiles(
     '\\.\pipe\')` — which no query can create by asking. Matching on
     `Name='sd.exe'` rather than on a command line is the same idea. **The
     helper was confirmed gone by the pipe being absent, not by a corrected
     process list.**

- ***ONE EMPTY STRING IN AN `-ArgumentList` ARRAY REJECTS THE WHOLE ARRAY, AND
  NOTHING LAUNCHES.*** Found 28 Aug 2026 on the `-Run b50` suite run;
  PRE_RELEASE 43.

  `Start-Process -ArgumentList` carries `[ValidateNotNullOrEmpty()]`, and
  PowerShell applies that attribute to **every element of a collection**, not
  just to the collection. So `@('-NoProfile', '-Password', '')` fails binding
  with **"Cannot validate argument on parameter 'ArgumentList'. The argument is
  null or empty"** — a message that names **no element**, and reads like the
  whole parameter was omitted.

  **Measured, with a control:** the same call with no empty element gets past
  `-ArgumentList` and fails on a later parameter instead.

  ***WHAT MAKES IT EXPENSIVE IS THAT IT IS DATA-DEPENDENT.*** The call site is
  one line and looks right; whether it works depends on a variable. In
  `verify-doors-suite.ps1` the **Create** leg carried a password and elevated
  normally, and **Suspend** and **Remove** carried `''` and died **before their
  UAC prompt** — so a suite step failed with no window, no child, and no log
  file for the leg that "ran".

  ***THE FIX IS TO OMIT THE PAIR, NOT TO PASS A PLACEHOLDER***, which is the
  idiom `sd-elevate.ps1:118` already used for its optional `-LogFile`. **And
  the class fix is to print the argv and its element count and refuse an empty
  element by name** — see the `$args` clobber in CLAUDE.md, which is the same
  lesson from the other side: you cannot debug an argument list you never see.

- ***THE SUITE'S `PASS` COUNT WAS GREPPED OUT OF FILES NOTHING COULD READ, AND
  THE `[FAIL]` HALF OF THE NULL-CASE GUARD WAS THE HALF THAT WENT BLIND.***
  Found 26 Aug 2026, the sixty-second session, while checking the `b46` cycle.

  **`VerifyInstall2` writes its 19 per-step logs as UTF-16LE** — they open
  `FF FE` — because they come from `Start-Transcript` in the elevated child.
  Everything else in a run is UTF-8 or UTF-8-with-BOM. ***`grep` reads a
  UTF-16LE file as binary and matches nothing in it***, silently, exit 1.

  **The recipe in the record was *"a plain grep over the run's 47 files"*, and
  it is reproducible: over `b43`'s 47 files it returns `923` — the number this
  file has carried since 25 Aug — while decoding the 20 UTF-16LE files first
  returns `1446`.** So the grep read **27 of 47 files**.

  ***THE PASS UNDERCOUNT IS THE HARMLESS HALF. THE POINT IS THAT `0 [FAIL]` WAS
  NOT A MEASUREMENT OF THE ELEVATED HALF AT ALL*** — every elevated step's
  `[FAIL]` line lives in exactly the files the grep could not read. The counters
  were recorded as *"the cheap null-case guard"*, and for 19 of the 31 steps the
  guard was itself the null case. **Both runs really are clean** — decoded,
  `b43` and `b46` are both `0 [FAIL]`, `0 [SKIP]` — **so the verdict was right
  and the instrument was not.** What actually carried those runs was the step
  exit codes, which `VerifyInstall1`/`2` check themselves.

  ***THE FIX IS TO DECODE, AND TO PROVE THE DECODE REACHED SOMETHING.*** Count
  per encoding and print the UTF-16 subtotal; if it is `0`, the decode did
  nothing and the total is a lie. And control the failure pattern against a run
  that DID fail — `20260823-081128-05-verify-tiers.log` carries 8 `[FAIL]` when
  decoded, so a `[FAIL]` grep that finds none there is broken, not lucky.

  ***AND THE PATTERN IS BARE `PASS`, NOT `[PASS]` — DO NOT "TIDY" IT.*** The
  verifiers do not agree on a format: some print `[PASS] <claim>`, others a
  table row whose last column is `PASS`, others a closing `verify-x: PASSED`.
  Anchoring on `[PASS]` scores `b46` as **601** instead of **991** and drops
  whole verifiers to zero. Every count in this file is bare `PASS`.

  **`991` is `b46` de-duplicated**: the unelevated per-verifier logs are copied
  wholesale into `VerifyInstall1-<stamp>.log`, so a flat sum over all 47 files
  double-counts them (it gives `1485`). The elevated per-step logs are **not**
  duplicated in `post-cycle-elevated-<stamp>.log`, because `VerifyInstall2` is
  invoked `-Quiet` and its Tee holds only the summary.

- ***WINDOWS AND PYTHON DISAGREE ABOUT WHERE A HYPHEN SORTS, SO A FILE CAN BE
  LISTED IN ONE ORDER BY EXPLORER AND ANOTHER BY A BUILD SCRIPT.*** 26 Aug
  2026, the documentation set. **Explorer's collation ignores the hyphen**, so
  `01a-first-run` sorts **before** `01-installation`. **Python's `sorted()`
  compares bytes**, where `-` is `0x2D` and `a` is `0x61`, so it sorts
  **after**.

  **What it cost:** three new pages were rendered by `mkdoc.py` in the intended
  reading order and listed by the folder in a different one — the walkthrough
  above the installation page it was written to follow. The owner looked in the
  folder, did not find them, and reported them missing. **They had been there
  and pushed for an hour.**

  ***THE FIX IS NOT TO PICK A SORT — IT IS TO USE NAMES THAT CANNOT DISAGREE.***
  A flat `00`–`13` with no letter suffixes sorts identically under both rules.
  **Anywhere an ordering is user-visible AND consumed by a script, check it in
  both**: `Get-ChildItem | Sort-Object Name` and the script's own listing.

  **`stage.py` and the mirror walks sort file names too.** Nothing has gone
  wrong there — the names in play are unambiguous — but the same discrepancy is
  latent wherever a name mixes `-` with a letter at the same position.

- ***PIPING A COMMAND INTO `sd` HANGS THE SESSION AND LEAVES A STRAY PROCESS.
  `echo WHO | sd` IS THE ONE THAT KEEPS BEING TYPED, AND IT LOOKS LIKE
  NOTHING.*** Walked into 23 Aug 2026; it hung, and **the stray `sd.exe` cost an
  elevation to clear**.

  ***RECORDED HERE 26 Aug 2026 BECAUSE IT WAS NOWHERE THIS FILE SAID IT WAS.***
  §0 pointed at *"§START HERE already recorded"* it — **START HERE never held
  it**, and §6, which rule 4 says is where traps live, had no entry. CLAUDE.md
  tells every session to grep this file for the command before running it; the
  only hit was the dangling pointer. **This is the trap the grep rule exists
  for, and the grep could not find it.**

  ***THE MECHANISM IS NOT "PIPES DO NOT WORK" — SD IS BLOCKED ON A PROMPT IT
  CAN NEVER BE ANSWERED.*** Diagnosed 23 Aug 2026 on the sibling symptom, an
  elevated `sd <command>` that *"blocks for ever during start-up"*: it had
  reached the account's **`New password:`** prompt and was blocked on a read
  that gets no input. **CPU 0.016s to 0.297s across 26 seconds — blocked, not
  looping.** ***There is no errlog entry, because nothing has gone wrong from
  SD's side***, which is why this reads as a crash and is not one.

  ***AND THE OUTPUT IS NOT MISSING, IT IS SOMEWHERE NOBODY READ.*** The same
  day, `sd` was reported as giving *"no output"* when stdout had been redirected
  to a file; the password prompt was in it the whole time. **That cost a day.**
  If SD is quiet, find its stdout before theorising.

  **THE SHAPE THAT WORKS** — `Invoke-SD` in the verifiers, e.g.
  [probe-catprivate.ps1:144](sdb_ai/sd64/gplbld/probe-catprivate.ps1:144):
  feed a **whole script that ends in `OFF`**, run it under `Start-Job` with a
  **timeout**, and on timeout say so out loud rather than returning empty. Its
  timeout branch names the cleanup, and that part is not decoration: **a
  timed-out session leaves its user-table slot and locks behind, so `sdwind`
  will not shut down and `cycle.ps1` will refuse to start** — `Stop-Process` the
  `sdwind` PID it names.

- ***A VIRTUALBOX GUEST THAT FREEZES UNDER DISK LOAD IS THE HOST'S HYPERVISOR,
  NOT THE GUEST'S WORKLOAD. IT COST TWO WEDGED RUNS AND MOST OF A SESSION,
  AND IT WAS MISDIAGNOSED AS THE WORKLOAD BOTH TIMES.*** 24 Aug 2026, step 17.
  **THE TELL IS ONE LINE IN `VBox.log`:**
  `HM: HMR3Init: Attempting fall back to NEM: AMD-V is not available`. VirtualBox
  is then running on the **Windows Hyper-V platform** (`WinHvPlatform.dll`)
  instead of native AMD-V, which is slow and wedges guests. **Grep that line
  before believing anything a VM tells you.**

  ***THE SYMPTOM LOOKS EXACTLY LIKE AN APPLICATION HANG, WHICH IS THE TRAP.***
  The guest desktop stops repainting — **tray clock frozen** — keystrokes and
  Ctrl+C do not reach it, and it must be powered off. Session 53 read that as
  `pacman` blocking on a file lock; this session hit the identical freeze
  **inside the MSYS2 installer's own extraction, before pacman ran at all**.

  ***HOW TO TELL A WEDGE FROM SLOW WORK, since the screen is useless either
  way*** — both are cheap and neither needs guest credentials:

  | instrument | wedged | alive |
  |---|---|---|
  | differencing `.vdi` size, sampled 60 s apart | **0 bytes** growth | grows |
  | `VBoxManage metrics query <vm> CPU/Load/User` | steady, ~2 cores spinning | varies |
  | guest tray clock across two screenshots | frozen | advances |

  **CLEARING IT TAKES FOUR HOST SWITCHES AND THE OBVIOUS ONE IS NOT ENOUGH.**
  Anything in the Hyper-V family holds AMD-V exclusively. On this host all four
  were needed, each with a reboot: **Memory Integrity** off (Core isolation),
  **Virtual Machine Platform** off, `bcdedit /set hypervisorlaunchtype off`,
  and — the one that actually released it — the
  `HKLM:\SYSTEM\CurrentControlSet\Control\DeviceGuard\Scenarios\WindowsHello`
  `Enabled` value set to **0**. ***TURNING WINDOWS HELLO OFF IN SETTINGS DOES
  NOT CLEAR THAT KEY***; it is the Enhanced Sign-in Security platform flag and
  it survived three reboots. `hypervisorlaunchtype` was **already `Off`** and
  was being overridden by it.

  ***VERIFY ON THE SUCCESS WORDING, NOT THE ERROR'S ABSENCE.*** Host side,
  `(Get-CimInstance Win32_ComputerSystem).HypervisorPresent` must read
  **False**, and `Win32_Processor`'s `SecondLevelAddressTranslationExtensions`
  and `VMMonitorModeExtensions` must flip **False to True** — they read False
  *because* a hypervisor is holding them, so their return is the positive
  proof. Guest side, `VBox.log` must carry `HM: Using AMD-V implementation 2.0`
  and `HM: VT-x/AMD-V enable method: VirtualBox`. **Security note: Memory
  Integrity is a real protection and this lowers it. It is the owner's call,
  it is reversible, and an agent must not make it.**

- **`icacls /inheritance:r /T` BEFORE THE GRANT EMPTIES THE PARENT, LOSES THE
  WALK, AND EXITS 0 HAVING SAID SO. IT COST TWO RUNS AND ALMOST SHIPPED A
  FALSE PRODUCT FINDING.** 24 Aug 2026, `verify-apiidentity` `b25`/`b26`.
  A fixture directory whose ACEs are all inherited has an **empty DACL** after
  `/inheritance:r`, and **owner-implicit rights cover `READ_CONTROL` and
  `WRITE_DAC` but NOT `FILE_TRAVERSE`** - so icacls cannot descend into the
  directory it has just emptied. It prints `<path>\*: Access is denied.` on
  stderr and **exits 0**, because the item named on the command line
  succeeded. The children keep their stale inherited ACEs - here
  `sdusers:(OI)(CI)(M)` from `C:\ProgramData\SD` - while the DIRECTORY reads
  back perfectly clean.

  **THE ORDER IS GRANT FIRST, STRIP SECOND.** The explicit ACE is then already
  in place when the inherited ones go, access is never lost, and the walk
  completes. `Set-FixtureAcl` in `verify-apiidentity.ps1` is the worked form.

  **AND THE EXIT CODE IS NOT THE INSTRUMENT.** Read the output for
  `Access is denied` and for `Failed processing [1-9]`; `Assert-Icacls` does.
  Both `b25` and `b26` were scored on that silence.

  **Measured, not reasoned** - two scratch probes separated the two candidate
  causes: a child locked against its owner is still `Get-Acl`-readable (so
  owner `READ_CONTROL` works), while an untouched child under an emptied
  parent is not (so traversal is what fails).

- **ASSERT THE ACL ON THE OBJECT THAT GETS OPENED, WHICH FOR A DYNAMIC FILE IS
  `%0` AND NOT THE DIRECTORY.** Same session. `op_dio1.c:734` only `stat()`s
  the directory and then tests for `<path>/%0`; with it, `dh_open()` opens the
  subfiles (`dh_open.c:122`), and **without it the file becomes a
  DIRECTORY_FILE and `op_dio1.c:866` opens nothing at all**. So a directory
  whose DACL looks right proves nothing about the file, and a fixture that
  loses its `%0` silently stops being able to deny anything.

- **AN ACL CANNOT GATE A LocalSystem SESSION AT ALL, SO DO NOT BUILD A
  PERMISSION FIXTURE TO TEST ONE.** 24 Aug 2026, `b27`. LocalSystem holds
  `SeBackupPrivilege`, which bypasses DACLs outright - measured indirectly but
  unambiguously: three fixtures with DACLs verified correct at `%0`, one
  granting the account alone and one granting it nothing, **all opened**, which
  no single token can do. **Ownership is the instrument that survives this**,
  because a privilege that lets a token OPEN a file it has no ACE on does not
  change whose name goes on a file it CREATES. §7 step 14.

- **A `^\s*\d+\s+(\S+)` "session and account" PATTERN ALSO MATCHES
  `1 record(s) copied.`** 24 Aug 2026, `b24`. Parsing `WHO` that way turned two
  COPY success lines into two extra WHO reports and failed a step that had
  entirely succeeded. Match an ACCOUNT-SHAPED token to end of line, and
  **do not make it case-insensitive** - under `(?i)` an `[A-Z]` class matches
  the `r` of `record(s)` and the bug returns, which is this section's
  `-match` trap arriving from a new direction. `Get-WhoAccounts` is the form,
  with a unit test that runs the real b24 transcript through it.
- **NAMING A SCRIPT WITH A PATH SEPARATOR IN `stage.py` OR `sd.iss` SILENTLY
  UN-EXCLUDES IT FROM `assert-current`.** Hit 20 Aug 2026. A comment in
  `stage.py`'s `SD_CONF` block said *"Measured 20 Aug 2026
  (`gplbld/verify-apiadmin.ps1`)"*, and `assert-current` began reporting:

  ```
  note: verify-apiadmin.ps1 now appears in stage.py or sd.iss, so it is watched again
  ```

  **`$shipsAs` matches `["'\/]` immediately before the name**, to tell a ship
  list entry from a passing mention - and a mention that happens to carry a
  path separator looks exactly like a ship list entry. **This is the same
  false positive that check was already hardened against**, arriving by the
  one route the hardening does not cover: its own comment records that the
  first version matched the bare name and reinstated `assert-current.ps1`
  because `stage.py` discusses it in a comment.

  **WHY IT MATTERS RATHER THAN BEING COSMETIC:** the file leaves
  `$neverShipped`, so the next edit to it makes the tree report STALE - and
  `verify-apiadmin.ps1` **calls `assert-current` and refuses on a non-zero
  exit**, so it would refuse to run on the strength of its own newness. That
  is the self-blocking shape the `verify-accountacl.ps1` note in
  `assert-current.ps1` describes, reached without anyone touching that list.

  **THE RULE: in `stage.py` and `sd.iss`, name a script WITHOUT a path** -
  *"verify-apiadmin.ps1 in this directory"*, never `gplbld/verify-apiadmin.ps1`.
  **And read `assert-current`'s `note:` lines**; this one is printed on an
  otherwise exit-0 run, so a reader watching only the exit code never sees it.

- **`sdclilib.dll` BUILDS REPRODUCIBLY AND `sd.exe` DOES NOT, AND THE
  ASYMMETRY DECIDES WHAT A NO-OP REBUILD COSTS.** Measured 20 Aug 2026 by
  running `make sd` twice with no source change between:

  ```
  sdclilib.dll  3783A82FCDEBD433 -> 3783A82FCDEBD433   identical
  sd.exe        EBD39CFC091DB1A2 -> B0F8DE2D5F4306E9   different
  ```

  So **rebuilding after touching anything the server links ALWAYS costs a
  cycle**, whether or not the change could affect the binary - the hash moves,
  `assert-current`'s Check A fails, and only an install can clear it. The
  client DLL is free.

  **THE SHAPE THIS ARRIVES IN, because it is not obvious from either end.**
  Editing `gplsrc/sdclilib/Makefile` to add a TEST target - which cannot
  change any shipped byte - left the DLL's mtime older than the Makefile, so
  Check B said *"run `make sd`"*; running it then broke Check A, which only a
  cycle fixes. **One edit to a test-only target, two cycles**, if the rebuild
  is not done before the first one. Do the rebuild first.

- **A TIER RESULT THAT LOOKS LIKE THE SILENT FULL-VOC FAILURE IS MORE LIKELY A
  BROKEN ACCOUNT NAME. 19 Aug 2026.** `verify-tiers.ps1` reported all three
  tiers holding **429** VOC records, **0 of 18** capabilities withheld and all
  **10** administration verbs present in a STANDARD account — which is exactly
  the failure §5.12 says is dangerous because it "looks exactly like a filter
  that worked".

  **It was not the filter. `CREATE.ACCOUNT` had created nothing**, `LOGTO` had
  failed, and every session was still in **SDSYS** — and `voc_template` holds
  429 records. **The discriminator is one line in `sdsys/audit`:**

  ```
  LOGTO REFUSED account=-PREFIX reason=not in the register
  ```

  **CHECK THE ACCOUNT WAS CREATED BEFORE READING ANY TIER NUMBER.** `429`, or
  any figure equal to `voc_template`'s record count, means SDSYS.

  **THE CAUSE WAS POWERSHELL SPLATTING**, in `post-cycle-elevated.ps1`:
  `& $path @($s.Args)`. **`@(...)` is an array subexpression, not splatting.**
  Measured, all three forms, against a probe script:

  ```
  & $p @($a)             ->  Prefix = [-Prefix sdtierg]   the whole array, stringified
  & $p @a   (array)      ->  Prefix = [-Prefix]           elements bind POSITIONALLY
  & $p @h   (hashtable)  ->  Prefix = [sdtierg]           the only one that binds by name
  ```

  **SPLAT A HASHTABLE OR PASS THE PARAMETERS LITERALLY.** Array splatting is
  not a fix.

- **A CHECK THAT CANNOT FAIL IS WORSE THAN NO CHECK, and this one guarded
  account creation.** 19 Aug 2026. `verify-tiers.ps1` section 1 read
  `if ($out -notmatch $t.Name) { exit 2 }` — but **SD echoes the command it is
  given**, so the account name is in the output whether `CREATE.ACCOUNT`
  succeeded or refused. A run that created nothing walked straight past it and
  first surfaced three sections later wearing the disguise above. It now
  asserts the `accounts\<NAME>` record exists — the thing the verb is *for*.

  **The general form: assert the effect, not the transcript.** Anything that
  greps SD's output for a string the input also contains is measuring the echo.

- **AN ELEVATED SCRIPT WITHOUT A TRANSCRIPT REPORTS NOTHING**, because the
  elevated window does not paste its output back into the session that asked
  for it. 19 Aug 2026: `verify-createaccount.ps1` was the only verifier without
  `Start-Transcript`, exited 2 in under a second, and left no record of why —
  the fault had to be reconstructed from `verify-tiers`' audit trail instead.
  Fixed, and closed in the existing `finally` so every `exit` path releases it;
  a transcript left running swallows the *next* verifier's output.

- **`CT` AND `LIST` DISAGREED ABOUT THE SAME RECORD ID, AND THE VERIFIER COULD
  NOT HAVE SEEN IT.** 18 Aug 2026, found while auditing for the TCL rename and
  fixed the same day. On the 22:26:18 install, with the VOC id already renamed:

  ```
  CT VOC $HOLD        ->  VOC $hold                 (CT:202 folds the record id)
  LIST VOC $hold      ->  1 record(s) listed
  LIST VOC $HOLD      ->  0 record(s) listed, '$HOLD' not found
  ```

  `QPROC`'s `check.record` read the record id **exactly** and had no fold at
  all. So the `$hold` rename shipped a live regression the same session that
  made it, and the changelog promised "the old spelling still works when you
  type it" — true of `COUNT`, `CT` and `ED`, false of `LIST`.

  **`verify-lcnames.ps1` TESTED `CT` AND `COUNT` AND NEITHER CAN SHOW THIS**,
  because both fold. A verb that folds cannot be the instrument for a verb that
  does not. It now tests `LIST` both ways, with an absent-id control so the fold
  is distinguishable from a lookup that matches anything.

  **The general lesson: after a rename, test every verb that NAMES the thing,
  not one of them.** The ones that fold all pass together and say nothing about
  the ones that do not.

- **`BASIC bp X` CREATES A `bp.OUT` THAT NOTHING CAN EVER OPEN AGAIN, AND IT
  BREAKS THE NEXT SCRIPT RATHER THAN THE ONE THAT DID IT.** 18 Aug 2026. Two
  verify scripts exited 2 on a fresh, good install with
  `Data pathname 'BP.OUT' already exists / Unable to open newly created output
  file`, which reads like a broken bootstrap.

  `BASIC:132` builds the object file name from the source name **as typed** —
  `bp` gives `bp.OUT`, not `BP.OUT`. `BASIC:135` opens it through the three-case
  fold, finds nothing on a fresh account, and `BASIC:157` runs
  `CREATE.FILE DATA bp.OUT DIRECTORY`. `CREATE.FILE` then writes the VOC id **as
  typed** (`bp.OUT`) and the directory **upper-cased** (`BP.OUT`) —
  `UPSTREAM_FIXES.md` #6.

  **THE FOLD CANNOT REACH A MIXED-CASE ID.** It tries as typed, all lower, all
  upper; `bp.OUT` is none of those from `BP.OUT`. So the next `BASIC BP Y` finds
  no VOC entry, tries to create `BP.OUT`, and the directory is already there.
  **Permanently** — nothing clears it but deleting the file.

  **WHY IT APPEARED ONLY NOW**: 5.12 (a) made the per-account file `bp`, so
  scripts and people type `bp`. Before that everyone typed `BP` and the two
  spellings agreed. The repair is
  `DELETE.FILE bp.OUT FORCE` — `FORCE` because `DELETEF` prompts separately for
  the DATA and DICT parts whenever the stored path differs from the default
  name, which for a lower-case file it always does. `verify-lcnames.ps1`'s
  `Remove-Probes` now does it, and only when that run created the file.

- **`assert-current` CHECK A2 TURNS `make check-local` INTO A PERMANENT FALSE
  STALE.** 18 Aug 2026, fixed the same day. A2 flags any file under `gplsrc`
  newer than the oldest binary in `bin\`, and it did **not** inherit check B's
  `localtest\` exclusion. `make check-local` builds
  `gplsrc\sdclilib\localtest\local-connect-test.exe`, so from then on every
  `assert-current` said STALE and every verify script refused — and reinstalling
  does not help, because the next run of `check-local` recreates the file.

  **The documented post-cycle order is cycle, `check-local`, then the verify
  scripts**, so this fires on the normal sequence rather than on anything
  unusual. Check B's own comment (added 17 Aug for `__pycache__` and
  `localtest`) foresaw exactly this failure and A2, written on 18 Aug, was one
  place short. Both exclusions are now in both checks.

- **ORDER EXEMPT FIXES FIRST, THEN RE-MEASURE, THEN TOUCH `sdsys`.** 18 Aug
  2026, and it cost a cycle. A verify script is in `assert-current`'s
  `$neverShipped` list and cannot make an install stale; a shipped file under
  `sdsys` can. Correcting a verifier and a message file in one go therefore
  voids the install being measured, for the sake of the half that did not need
  to.

  **THE EXAMPLE THIS ENTRY WAS WRITTEN AROUND IS DEAD, THE RULE IS NOT.** It
  said `sdsys/changelog`, which was the commonest case; the changelog has been
  exempt since 21 Aug 2026 (header item 1), so it no longer voids anything.
  Every other shipped file under `sdsys` still does.

- **`cycle.ps1` DOES NOT BUILD. A C CHANGE CAN BE CYCLED, INSTALLED, TESTED AND
  PASSED WITHOUT EVER BEING COMPILED.** 18 Aug 2026, and it cost a whole cycle.
  `cycle.ps1` stages whatever is already in `bin\`; the build is a separate
  `make sd` in an MSYS2 login shell. `to_file.c` was edited at 19:15 and cycled
  at 19:38 against `bin/sd.exe` from **17:17**.

  **BOTH `assert-current` CHECKS PASSED, and neither was wrong to.** Check A
  compares installed `sd.exe` against `bin/sd.exe` — equal, *because both were
  stale*. Check B compares source mtimes against the **install** time, and
  19:15 is older than 19:39. The script's own header reasons carefully about the
  opposite direction ("most changes here are BASIC, so hashing `sd.exe` is not
  enough"); this is the other half and nothing covered it.

  **AND THE TEST FOR THE CHANGE PASSED TOO, which is what made it invisible.**
  The change was `$HOLD` to `$hold` in a **relative** path, and NTFS matches
  either against the `$hold` directory — so the old binary and the new one
  behave identically. `verify-lcnames.ps1` §4 carried a comment claiming it
  measured the C literal; it cannot, on Windows, and the comment is corrected.

  **`assert-current` CHECK A2 NOW CATCHES IT**: any file under `gplsrc` newer
  than the **oldest** binary in `bin\` is stale, and it names the file. Run
  against the tree as it stood it printed `18 Aug 19:15:43 gplsrc	o_file.c`.
  Oldest rather than `sd.exe` alone, so `gplsrc\sdclilib` and `gplsrc\sdsvc`
  count — they ship in the same install.

  **The discriminator, if this is ever in doubt: the `sd.exe` hash.** It moved
  `DA280984D21571B4` to `A6AAAB58AAB676F4` when the C was finally built.

- **A CONFIRMING VERB EATS THE NEXT PIPED LINE AS ITS ANSWER, AND SPINS FOR EVER
  IF THE PIPE RUNS OUT WHILE IT IS STILL ASKING.** 18 Aug 2026. **Corrected the
  same day**: this entry first said piped answers were "not consumed" and that
  such prompts "read the keyboard directly". Both were wrong — measured with a
  throwaway file, `DELETE.FILE` answers perfectly well from the pipe:

  ```
  DELETE.FILE sdtrap  +  Y  Y   ->  OK to delete DATA portion 'SDTRAP'? Y
                                    DATA portion 'SDTRAP' deleted
                                    OK to delete DICT portion 'SDTRAP.DIC'? Y
                                    DICT portion 'SDTRAP.DIC' deleted
                                    VOC entry 'sdtrap' deleted
  ```

  **The real trap has two halves.** A prompt consumes **the next line in the
  pipe**, whatever you meant it to be — so `DELETE.FILE x` followed by `OFF`
  feeds `OFF` to the prompt as the answer, and the line you intended as a
  command is gone. Then, the answer being neither Y nor N, it asks again, the
  pipe is exhausted, and **it re-asks on EOF without end**. Surplus answers are
  harmless: extra `Y` lines just reach the prompt as unknown verbs.

  **So supply every answer, in order, before the next command.** Count the
  prompts — `DELETE.FILE` asks twice, DATA then DICT.

  **AND THE LESSON THAT WAS ACTUALLY MINE:** the "it hangs" reading came from
  sampling a background task's output file a second or two after starting it,
  seeing only the command echo, and killing a run that was working. Three
  `sd.exe` processes died that way. **Give it time and read the output again
  before concluding a hang.**

  If a process does need killing: **they are children of the calling
  `powershell.exe`, so identify them by `ParentProcessId`** — the service is
  session 0 and a real user session must not be caught by a blanket
  `Stop-Process -Name sd.exe`.

  **A BASIC program is still the cleanest route for a record**, and needs no
  answers at all: `OPEN 'VOC' TO F.VOC` then `DELETE F.VOC, 'id'`. That is how
  the `testlc` probe record was removed.

- **POWERSHELL'S `-match` IS CASE INSENSITIVE, SO A SUCCESS TEST CAN MATCH THE
  FAILURE LINE.** 21 Aug 2026, caught while writing `verify-apiname.ps1` and
  **before** it cost an elevated run, which is the only reason it is cheap.
  `remote_connect_test.c` prints `admitted` when the connect succeeds (`:116`)
  and **`ADMITTED`** on the *failure* paths of its wrong-password and SDSYS
  checks (`:139`, `:154`) — so `$out -match 'admitted'` answers true for both,
  and a harness reading it would score a failed refusal as a passing login.
  **Use `-ceq` on the trimmed line, or `-cmatch`.** The `c` prefix is the
  case-sensitive form of every PowerShell comparison operator (`-ceq`,
  `-cmatch`, `-clike`, `-ccontains`) and none of them is the default.

  **The general form is §0 rule 2's, arriving through the harness rather than
  the system:** an instrument you have not checked is not evidence, and a
  comparison that cannot fail is the commonest way to build one. This file has
  now recorded four such instruments — `Measure-Object -Line`, the UAC registry
  reading, `OpenProcess(PROCESS_TERMINATE)`, and a `-notmatch` on SD's own echo
  (§6 above) — and this is the fifth.

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
  after. **Fixed 16 Aug 2026** — `sd_state()` downgrades `SD_WRECKAGE` to
  `SD_STOPPED` for a segment whose mtime predates boot, so the leak is harmless
  rather than absent (§4; HISTORY, *"A segment from a previous boot stops
  meaning wreckage"*). *Pointer corrected 21 Aug 2026: this said "header item 1",
  and that header was archived.* The same applies to anything else that assumes
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
    either stream. `termios` → Console API **was attempted on 23 Aug 2026 and
    reverted** - §7 step 13 - so this stays true and now stays true on purpose.

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

  **AND "CHECKS BOTH" WAS NOT ENOUGH — CORRECTED 18 Aug 2026.** It checked them
  in `CurStepChanged` and `CurUninstallStepChanged` and NOT in
  `CurPageChanged`, which **still fires in silent mode** — the wizard form is
  created and simply not shown. A `-Silent` cycle stopped there with a modal
  box on screen and copied nothing until somebody clicked OK. The guard is now
  the first statement of `CurPageChanged`; verified by a `-Silent` cycle
  running through unattended, 21:03:32.

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

- ***CORRECTED 30 Aug 2026 — THE SENTENCE BELOW IS OUT OF DATE AND WAS FALSE
  FOR FIVE DAYS BEFORE ANYBODY NOTICED. READ THIS FIRST.*** ***THERE IS AN
  UPGRADE PATH***, built 25 Aug 2026 on the owner's ruling *"preserve the
  user's own files, replace all the shipped ones"*. `stage.py`'s
  `write_upgrade_iss()` emits `upgrade.iss`, and `sd.iss:1044` states the
  invariant: *"upgrade.iss is gated on this; the whole-tree entry in [Files] is
  gated on DataTreeAbsent. **One or the other fires on every install, never
  both and never neither.**"* **On an upgrade `gpl.bp`, `gpl.bp.out`,
  `messages`, `newvoc` and `voc_template` ARE replaced**, while `$cred`,
  `accounts`, `cat`, `os.users`, `batch.jobs`, `prt`, `$hold`, `bp` and
  `bp.out` are preserved — **so a BASIC or message fix DOES reach an existing
  install.** ***WHAT STILL DOES NOT IS ANY LIVE VOC***, SDSYS's own included:
  they are built from those templates and are in neither list, and nothing
  re-runs `UPDATE.ACCOUNT` — **PRE_RELEASE 70.** ***THE CYCLE RULE BELOW STILL
  STANDS AND IS NOT WEAKENED BY THIS*** — a test cycle still begins from a
  deleted tree — **but it now rests on "date what you are testing", not on
  "the tree can never move".** *(Reading the old text as current nearly cost a
  wrongly-filed blocker on 30 Aug: PRE_RELEASE 71.)* **The superseded text
  follows, kept because it is what a returning reader remembers:**

- **INSTALLING OVER A LIVE TREE DOES NOT REFRESH EVERYTHING, SO "TEST IT ON THE
  INSTALLED SYSTEM" CAN QUIETLY MEAN "TEST AN OLD BUILD".**

  ***CORRECTED 30 Aug 2026 — PRE_RELEASE_FIXES 71. THE RULE BELOW IS UNCHANGED
  AND THE REASON IT USED TO GIVE WAS FALSE.*** This bullet said *"THE INSTALLED
  DATA TREE IS NEVER UPGRADED"* and *"`sd.iss` skips the entire `sdsys` set when
  `C:\ProgramData\SD\sdsys` already exists"*, and both stopped being true on
  **25 Aug 2026**, when the owner ruled *"preserve the user's own files, replace
  all the shipped ones"* and `upgrade.iss` was built to do it. **`sd.iss:1044`
  states the invariant that replaced them**: *"upgrade.iss is gated on this; the
  whole-tree entry in `[Files]` is gated on `DataTreeAbsent`. One or the other
  fires on every install, never both and never neither."*

  ***WHAT AN UPGRADE ACTUALLY DOES*** is replace the shipped set — `gpl.bp`,
  `syscom`, `newvoc`, `voc_template`, `messages`, `sd.voclib`, the objects and
  the catalogue — and preserve `stage.py`'s `SDSYS_PRESERVE` list: `$cred`,
  `accounts`, `cat`, `os.users`, `batch.jobs`, `prt`, `$hold`, and SDSYS's own
  `bp`/`bp.out`. **`sd.conf` is `onlyifdoesntexist` and is never rewritten.**

  ***SO WHY THE RULE STILL STANDS, AND IT MUST NOT BE WEAKENED ON THE STRENGTH
  OF THIS CORRECTION.*** A cycle still begins from a deleted tree. What an
  upgrade does NOT do is re-run anything — **PRE_RELEASE 70**: no existing
  account, SDSYS included, gains a verb an upgrade adds to `newvoc` or
  `voc_template`. So an upgraded tree is a *different* state from a fresh one,
  and testing on it answers a question you did not ask. **A rule defended by a
  false reason is one the next session argues with**, which is the whole cost
  this correction is paying off: reading the old text as current, a session was
  one step from filing a blocker claiming W1.0-0 could never be patched.

  **CLAUDE.md's Testing section carries the same stale justification and is
  deliberately NOT edited here** — it is the owner's standing-instruction file.

  The consequence nobody had joined up: on
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
  `sdsys/MESSAGES` names the delta exactly. ***AND `assert-current.ps1` IS THE
  REAL ANSWER TO ALL OF THIS***, written after this bullet was: it compares
  source mtimes against the install across six mirrored directories and refuses
  a stale tree, which is a better instrument than any hand-check above.

  **Refreshing for a TEST means uninstall, delete `C:\ProgramData\SD`,
  reinstall** — the procedure at the top of this file, and `cycle.ps1` does it.
  ***THAT IS ABOUT TESTING, NOT ABOUT WHETHER SHIPPING AN UPGRADE IS POSSIBLE***
  — it is, since 25 Aug 2026, and the sentence that used to stand here saying
  *"there is no upgrade path"* is corrected above.

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

- **`AND` DOES NOT SHORT-CIRCUIT, AND BCOMP CANNOT SEE A PER-PATH UNASSIGNED
  VARIABLE. Together they hid a broken verb for two months.** `CREATEA`'s
  `create.group` tested

  ```
  if upcase(acc.type) = 'USER' and not(valid_os_name(acc.uname)) then
  ```

  `acc.uname` is assigned in the USER arm alone, so on the GROUP path it has no
  value — and **both operands are evaluated whatever the first one answers**, so
  `!VALID_OS_NAME` was called anyway and aborted on its first use of the
  argument. **Every `CREATE.ACCOUNT GROUP` died** with `000000EE: Unassigned
  variable at line 30 of !VALID_OS_NAME`, from 10 June until 21 Aug 2026.

  **BCOMP's "is not assigned a value" is per VARIABLE, not per PATH**, and
  `acc.uname` *is* assigned — just not on that one. Clean compile, runtime
  abort, every time. **So the warning above catches a missing include and will
  never catch this.** Nest the test, or assign the variable at the top the way
  `access.given` and `adopt.marker` are. Fixed at `CREATEA:1405`; swept for the
  same shape and it was the only instance.

  **AND NOTHING TESTED THE VERB**, which is the other half of why it survived —
  the Phase 4 plan said "nothing tests `CREATE.ACCOUNT GROUP` today" and was
  right. It is `verify-accountrules.ps1` step 3 now.

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

***SECTION 7 IS EMPTY. EVERY STEP IN IT IS CLOSED.*** The development phase
ended on 26 Aug 2026 with step 18 and H.5. The task table at the top of this
file is the authority on status; the entries below carry each step's conclusion
and the pointers that are still worth following.

***COMPRESSED 26 Aug 2026 under §0 rule 5*** — *"when a §7 step closes,
compress its §4 and §7 material to the conclusion"*, which had never been done
and had let this section grow to about a quarter of the file. **The problem
statements, the surveys, the reasoning that was live while each step was open
and the measurement transcripts are in HISTORY.md**, entry *"ARCHIVE 26 Aug
2026 — section 7's nineteen closed steps, in full"*. Nothing was deleted.

**Steps 4 to 13 keep the numbers they have carried since 13 Aug 2026**, because
the rest of this file refers to them by number. Do not renumber.

0. **CLOSED — 14 Aug 2026, sixth session. The Linux access model is restored,
   installed and verified end to end (§5.6, §4).** All five rules observed,
   both `LOGTO` paths, `CREATE.ACCOUNT` at 16 of 16.

   **`git show f9edab0:sdb_ai/sd64/sdsys/GPL.BP/LOGIN`, lines 185–270, is the
   specification** — this repository's own pre-port source. Read it before
   changing anything about who may enter which account. The one deliberate
   departure: an elevated session skips the `ACC$GROUP` test, because
   `ACCOUNTS/SDSYS` names a Linux group that does not exist on Windows. **And
   `IsElevated()` is not `IsAdmin()`** — a UAC-filtered token carries
   `Administrators` as deny-only, so the two answer different questions and
   both are wanted (`linuxlb.c`).

1. **CLOSED 16 Aug 2026, sixteenth session** — the account-model loose ends the
   port opened. `CREATUSR` is gone.

2. **DONE 15 Aug 2026, tenth session (§4).** A VirtualBox guest served as the
   second machine. ***It is still the rig***: items 4, 5 and H.5 all ran on
   guests, and anything that needs a machine that never had OpenSSH needs one
   built the same way.

3. **CLOSED 25 Aug 2026 — every installer loose end is closed**, the last being
   the remote-block control that became H.4. The closing dialog was read on
   screen by the owner rather than compiled, which is what found the
   `net localgroup sdusers` lines that could not work; they were dropped at
   `sd.iss:493`. **If that is ever re-checked, grep the emitted string, not the
   file** — `sd.iss` still names `net localgroup` at lines 67 and 926, inside
   comments recording why it went, so a plain grep looks alarming and is not.

4. **CLOSED — built and verified 16 Aug 2026, thirteenth session.**

5. **CLOSED 16 Aug 2026, fourteenth session — (f) included.** `GPL.BP/GRANTA`.

6. **CLOSED 17 Aug 2026, nineteenth session — the API works end to end.**

7. **CLOSED 17 Aug 2026 — both halves. `SH` and `OS.EXECUTE` are permitted by a
   list, not by a role.**

8. **CLOSED 22 Aug 2026 — both halves** (§5.12). Lower case everywhere it can
   be: the file-name half and the command half.

9. **CLOSED AND MEASURED, 22–23 Aug 2026.** A scheduled job can log in and run
   a command the administrator has named for its account. **`verify-batchjob`
   10 of 10 decisive on the 23:46:31 install.**

   ***THE THREE ROWS THAT CARRY IT ARE THE POSITIVE ONES*** — *listed: the
   paragraph RAN*, *ELEVATED with no entry: still runs*, *entry removed:
   refused again*. The five refusals prove nothing without them, and ***an
   ordinary token cannot WRITE `batch.jobs`*** is the whole of the control.

10. ***REMOVED FROM THIS PROJECT — owner, 23 Aug 2026.*** It read *"write the
    administrative forms"*. §5.14 has why they are a separate project.

11. **CLOSED — `SDConnectLocal()` carries a session.** Verified on the 12:28:49
    install.

12. ***REWRITTEN ON THE OWNER'S RULING, 21 Aug 2026. DO NOT RESTORE THE
    BRANCHES.*** It used to read *"restore the BASIC layer's Windows branches"*.
    **There are no Windows branches in this version of SD, because it is
    Windows only** — CLAUDE.md's rule for the C code, stated for the BASIC
    layer. A branch implies a non-Windows arm to fall back to and there is
    none. §5.4 has the reasoning and why it is not to be revived.

13. ***DROPPED AS A MIGRATION — owner's decision, 23 Aug 2026.*** It read
    *"Stage 2, native Win32"*. **Steps 14 and 15 are the two outcomes it was
    ever for**, and both are closed. §1 carries the four reasons and what the
    one attempted leg cost.

    **The question that ended it is the right one to ask of any remaining
    Linux-ism:** *"is this conversion really necessary — the system seems to
    work fine with Cygwin dependencies."*

14. ***CLOSED AND VERIFIED 24 Aug 2026 — API session identity, shape (b): the
    session becomes the authenticated user.*** Install 11:15:29,
    `verify-apiidentity` exit 0, the decisive row PASS — `ZZAPI` is owned by
    `GITORLI\sdapiidb32` where `b28` had `NT AUTHORITY\SYSTEM`.

    **This entry is why `check-stale-leads.py` exists.** It opened *"WHAT IS
    STILL A DECISION, AND IT IS THE OWNER'S"* — true for one day — and that
    sentence sat **338 lines above** *"STEP 14 IS CLOSED"* until 26 Aug 2026,
    being reported as outstanding work to an owner who knew better.

15. ***CLOSED 24 Aug 2026 — the data tree is private from SD's own users.***
    The ACL lock, §5.7's service-account model. `verify-sysdiracl` 16/16 on the
    18:03:37 install, `probe-catprivate` 3/3, all four writers measured.

16. ***CLOSED 24 Aug 2026, both halves — SD reads and writes CRLF.***
    (a) verified on install 12:15:51, (b) on install 12:36:09, **17/17
    decisive**. Commits `6120642` (a) and `2a30af1` (b).

    **`2f4c47c` is a separate `writeport` count defect** — `UPSTREAM_FIXES`
    #14, and ***not verifiable here***: it needs a real port device.

17. ***CLOSED 24 Aug 2026, fifty-fourth session — `setup-devbox.ps1` ran end to
    end on a bare VM***, about 17 minutes, **exit 0**, through `make sd`, last
    line `setup-devbox: finished, no problems.`

    ***`sdhelp` WAS RAISED AS AN OPEN REQUIREMENT AND THE OWNER CANCELLED IT
    THE SAME DAY.*** 24 Aug 2026: *"cancel the sdhelp request — I will just
    download it from my P drive if needed."* The script's behaviour is correct
    as it stands: report it, place nothing. **Read §2's `sdhelp` paragraph
    before touching this** — the position arrived by way of a wrong attribution
    and a correction, so the end state looks like the thing that was asked for.

    ***THE ONE KNOWN COVERAGE GAP IS CLOSED, 26 Aug 2026.*** Step 17 proved the
    script *works*; what had never been checked was whether it still installs
    **everything a new machine needs**, and it did not install the `markdown`
    package `mkdoc.py` imports. `python-markdown` is now in `$PacmanPackages`
    and `-CheckOnly` names it. **The general question stands**: verify coverage
    against what the build actually uses, not that the script exits 0.

18. ***CLOSED 26 Aug 2026, sixtieth session — the last task of the development
    phase, and verified on the machine rather than off the transcript.*** Two
    runs of `cleanup-devlitter.ps1` either side of a reboot, by the owner,
    elevated, read back independently: **0 profile directories** (was 30),
    **0 `sd*` `ProfileList` entries** (was 77), **0 local `sd*` users** (was 8),
    **`sdout` and only `sdout`** in the home directory, the clone gone.

    ***NOTHING WAS OVER-DELETED***, which is the control: the five real SD
    groups, `don` and `test1` are all present, and `sdu_don` and `sdu_test1`
    survived a sweep that removed every other `sdu_` group.

    ***`cleanup-devlitter.ps1` IS KEPT*** — the piles come back the moment
    testing resumes — and it ***needs a reboot between the accounts and the
    profiles***: a loaded hive cannot be removed, and after a suite run every
    hive is loaded.

## 8. Open questions

**COMPRESSED 21 Aug 2026, thirty-eighth session**, under §0 rule 5. Closed and
superseded material is in HISTORY, *"ARCHIVE 21 Aug 2026 - section 8's closed
and superseded questions"*. Nothing was deleted.

**ONE WHOLE SECTION WENT AS STALE RATHER THAN CLOSED, and it is the reason to
read this section against the source.** It was headed *"BUILT AND VERIFIED,
20 Aug 2026: `RDPACCOUNT`"* and ran to a hundred lines of design for a keyword
**deleted the following day** — a cold session would have believed it shipped.
See "`RDPACCOUNT` was built and then deleted" below.

The identity question that stood here — admin flag inside SD, or OS group — was
**answered on 13 Aug 2026** and is now §5.6. Neither option was taken.

---

### Open: how many kinds of user does SD have, and what enforces each (16 Aug 2026)

**THE MECHANISM IS BUILT AND VERIFIED** — `verify-tiers`, three tiers chosen by
`CREATE.ACCOUNT` keyword (`PROGRAMMER` beside `ADMINISTRATOR`), the tier
recorded in **`ACCOUNTS` field 5** (`ACC$TIER`, `KEYS.H:281`), and the omit and
add lists held as **data** in `NEWVOC/TIER.OMIT.STANDARD` and
`NEWVOC/TIER.ADD.ADMINISTRATOR` so the shipped posture changes without
recompiling. Owner's approach: **capability by VOC content** — take `BASIC`,
`CATALOG`, `RUN`, `ED` and the rest off accounts that do not need them.
(`SED` was in that list until 23 Aug 2026, when the editor was removed and the
`TIER.OMIT.STANDARD` line went with it.)
Idiomatic MV, and it needs no C.

**CLOSED 24 Aug 2026, session 50.** The full three-tier split is ruled,
on disk, installed at 13:36:51, and **verified end to end by
`verify-tiers.ps1 -Prefix sdtierd` at 14:11:22 — 22 of 22 PASS**. The
subsection below carries the settled split; the START HERE at the top of
this file carries the verify table.

**THREE THINGS THIS QUESTION USED TO BE BLOCKED ON HAVE SINCE LANDED**, which
narrows it considerably:

- **Per-account ACLs are done** (`verify-accountacl`), so a reduced VOC is no
  longer one `COPY` away from being undone by its own user.
- **The global catalogue is gated and `gcat` is read-only to `sdusers`**
  (`verify-catgate`), which is what "catalogued" had to mean before program
  provenance could mean anything.
- **`OS.EXECUTE` is gated on the API path** by the containment gate.

**TWO RESIDUAL HOLES, both real, neither closed by any of that:**

1. **Injection through an application's own `OS.EXECUTE` or `EXECUTE`.** Tier-1
   programs legitimately need OS access, so the capability stays; an app that
   builds a command from user input is an escape, and the user compiles nothing.
   `!valid_shell_cmd`'s ban on `; | & $ < >` guards the `SH` path only. **The
   real fix is program provenance** — a catalogued program written by a
   programmer may `OS.EXECUTE`, an ad-hoc one may not. Setuid-shaped, new
   machinery, and now unblocked by the `gcat` gate above.
2. **A machine whose ssh server SD did not install**, where `ForceCommand` is
   never written (§5.9, structural). The user lands in `cmd.exe` and never meets
   SD's VOC at all.

**AND THE FLOOR UNDER ALL OF IT:** until §5.7's service model, every tier is
enforced by the user's own Windows token. Tier 3 is real because Windows
enforces it; tiers 1 and 2 are only ever as real as the ACLs.

**`LIST` AND `SELECT` MUST STAY IN STANDARD AND READ ANY FILE THE ACCOUNT CAN
OPEN.** So the VOC tier decides what a user may **do** and the per-account ACL
decides what they may **reach**. Neither substitutes for the other.

**THE FILTER FAILS SILENTLY AND ITS FAILURE LOOKS LIKE SUCCESS** — §6 has the
trap. A tier reading equal to `voc_template`'s record count means the session is
in **SDSYS** and the account was never created; check that first, and never read
a tier number without it.

#### THE SPLIT, settled 24 Aug 2026

**The split covers every verb in the current 141-entry `voc_template`.** Nothing
unaccounted for, nothing named that no longer exists — cross-checked 24 Aug
2026. Cumulative: `PROGRAMMER` gets STANDARD plus its own, `ADMINISTRATOR` gets
everything.

**HOW IT GOT HERE.** The first-pass split written 17 Aug is at HISTORY.md line
22086, marked "not reviewed by the owner ... expect entries to move." Session
50 lifted it, adjusted it for three verb changes since (`SED` and
`UPDATE.RECORD` removed session 42, `MODIFY.PASSWORD` added 17 Aug per
`CREATEA:72`), and put four remaining calls to the owner. **Owner ruled them
24 Aug 2026, session 50:** debug family moves to PROGRAMMER; the read-only
inspectors move to STANDARD; `SET.DATE` stays ADMIN; **`UMASK` is removed
entirely** — it is a POSIX file-mode-bits call, essentially inert on Windows
where security is ACL-based (`verify-accountacl`), so the verb is misleading
rather than useful. `op_umask` in `gplsrc/op_misc.c:1503` and `int.umask` in
`CPROC:3301` stay compiled but callerless, as `$MICRO` and `$NLS` are.

**REMOVED FROM EVERY TIER (8) — one new on 24 Aug 2026 (`UMASK`):**
```
micro  nls  set.language  load.language
set.server  delete.server  list.servers  umask
```
The first seven are already gone from both VOCs; UMASK still needs its
`voc_template/umask` and `newvoc/umask` records deleted. **One cycle-worth of
change on disk.**

**ADMINISTRATOR only (21).** These are moved into voc_template-only by adding
to `NEWVOC/TIER.ADD.ADMINISTRATOR` and (for those still in NEWVOC) removing
the record from NEWVOC.

- **A1, account and grant administration (10) — owner-ruled 17 Aug; `encrypt.field`
  removed 28 Aug, PRE_RELEASE 25, because `$CRYPTO` does not exist:**
  ```
  create.account  delete.account  modify.account  update.account  clean.account
  grant  revoke  list.grants  unlock  modify.password
  ```
- **A2, system-wide state (8):** `logout` refuses to log out another user's
  process unless caller is admin (`CPROC:3110`), so the tier is a policy call,
  not a security one. `SET.DATE` confirmed admin 24 Aug even though it only
  sets the SD process date-offset and does not touch the OS clock — SD's own
  clock is a system-wide fact once the daemon holds it.
  ```
  config  listu  list.readu  list.locks  clear.locks  lock  logout  set.date
  ```
- **A3, shell escapes (2) — owner-ruled 16 Aug, "same class as MICRO":**
  ```
  sh  !
  ```

**PROGRAMMER adds (42).**

- **P1, compilers, editors, code catalogue (15) — thirteen owner-ruled 17 Aug**
  (`BASIC`, `CATALOG`, `RUN`, `ED`, `COPY` off standard; `MODIFY`,
  `COMPILE.DICT`, `GENERATE`, `PHANTOM` — 17 Aug rulings; plus aliases
  `CATALOGUE`, `DELETE.CATALOG`, `DELETE.CATALOGUE`, `EDIT`, `CD`). `MAP`
  and `DEBUG` need `BASIC`-produced object.
  ```
  basic  catalog  catalogue  delete.catalog  delete.catalogue
  compile.dict  cd  generate  phantom  run  map  debug
  ed  edit  modify
  ```
- **P2, file and index definition (14):**
  ```
  create.file  delete.file  clear.file  configure.file
  analyse.file  analyze.file  fstat  hsm  set.trigger
  create.index  delete.index  build.index  make.index  list.index
  ```
- **P3, bulk record edit (9)** — cut from the earlier 17 when the read-only
  inspectors moved to STANDARD 24 Aug:
  ```
  copy  copyp  delete  rename  reformat  sreformat
  sort.item  delete.common  cname
  ```
- **P4, process introspection (4) — owner-ruled 24 Aug**, moved from
  ADMINISTRATOR: a programmer needs these to debug their own code.
  ```
  pstat  pdebug  pdump  dump
  ```

**STANDARD (77). The application floor**, owner-ruled 16 Aug that `LIST` and
`SELECT` stay in STANDARD and by extension the query family. Grew by 8 on 24
Aug when the read-only inspectors moved down from PROGRAMMER.

- **S1, query and list processing (10) — application core, owner-ruled floor:**
  ```
  select  sselect  qselect  nselect
  list  sort  sum  list.label  sort.label  list.files
  ```
- **S2, named lists (10):**
  ```
  get.list  save.list  form.list  copy.list  merge.list  delete.list
  list.union  list.inter  clear.select  clearselect
  ```
- **S3, spool and print (7):**
  ```
  setptr  spool  sp.open  sp.close  sp.view  printer  como
  ```
- **S4, session and environment (23):**
  ```
  logto  quit  stop  abort  clear.abort  go  if  set  show  option  alias
  set.exit.status  set.file  term  pterm  date  time  date.format
  who  who.am.i  status  release  autologout
  ```
- **S5, screen and messages (10):**
  ```
  message  logmsg  bell  echo  hush  pause  sleep  clr  cs  ct
  ```
- **S6, prompt and input state (9):**
  ```
  clear.input  clearinput  clear.prompts  clearprompts
  clear.data  cleardata  clear.stack  get.stack  save.stack
  ```
- **S7, read-only inspectors (8) — owner-ruled 24 Aug**, moved from PROGRAMMER:
  they read only, they need no BASIC or catalogue, an application can and does
  invoke them.
  ```
  search  list.diff  list.item  list.common  list.vars
  report.src  report.style  format
  ```

**Total: 21 + 41 + 77 = 139 verbs.** *(Was 21 + 42 + 77 = 140 until MODIFY
was removed from SD Core on 24 Aug 2026 - it was one of the 42 PROGRAMMER
verbs withheld from STANDARD, so only that middle number moves.)* Every verb
accounted for exactly once.

**LANDED ON DISK 24 Aug 2026, and installed at 13:36:51 in the same session:**

1. `sdsys/voc_template/umask` and `sdsys/newvoc/umask` deleted (UMASK
   removal).
2. Eleven verb files deleted from `sdsys/newvoc/`: `config`, `listu`,
   `list.readu`, `list.locks`, `clear.locks`, `lock`, `logout`, `set.date`,
   `sh`, `!`, `clean.account`. Their voc_template records stay and the
   admin tier reaches them via TIER.ADD.ADMINISTRATOR.
3. `sdsys/newvoc/TIER.OMIT.STANDARD` rewritten to 42 P verbs (was 17).
4. `sdsys/newvoc/TIER.ADD.ADMINISTRATOR` rewritten to 21 A verbs (was 10).
5. `gplbld/verify-tiers.ps1` count arithmetic re-derived — STANDARD 354,
   PROGRAMMER 396, ADMINISTRATOR 417; `$Withheld` grew to 42 verbs and
   `$AdminVerbs` to 21, each grouped by rationale.
6. `changelog` entry written for the user-visible change.

**Cycled at 13:36:51 and verified at 14:11:22.** `sd.exe
F53AE8F87BC55326`, `assert-current: the installed tree matches source`.
`verify-tiers.ps1 -Prefix sdtierd` returned **22 of 22 PASS**: COUNT VOC
per tier landed on 354 / 396 / 417 exactly, every between-tier control
row PASSed, and `UPDATE.ACCOUNT` on the standard account did not restore
the 42 withheld verbs. See the START HERE table at the top of this file
for the row-by-row.

### ANSWERED IN CODE 22 Aug 2026, UNMEASURED: what may a scheduled job run?

**§7 step 9 is the answer and carries what was built.** Read that first; what
follows is the design as it was written, kept because the reasoning still holds
and because **two of its specifics were wrong and the corrections are worth
seeing beside them** — `sd <command>` was elevation-gated in C, so "needs no new
C code" was false; and the list could not live in SDSYS's VOC, which grants
`sdusers` Modify. Both measured before anything was changed.

**The login half answers itself under §5.6:** a scheduled task runs as a Windows
user, and if that user has an SD account, `sd` puts it there with nothing asked.
The batch account is a Windows account plus its SD account, and it grants nobody
because nobody else is in its `ACC$GROUP` group. **No credential is involved
anywhere.**

**What is open is the capability list**, and the design is the owner's: an
`X`-type VOC item named `ALLOWED` in **SDSYS's** VOC, holding `ACCOUNT, VOC name`
pairs. Only an administrator can edit it, because it lives in SDSYS; the job
still runs in the named account, so **nothing runs with administrator rights**.
**The mechanism exists and needs no new C code:** `SYSTEM(1026)` returns the
command from the command line (`op_sys.c` case 1026) and `CPROC` does not pick
it up until line 556, so `LOGIN` can read and decide first.

**Constraints to build to**, worked out once so they are not re-derived:

- **One token, no arguments, enforced.** This is what does the security work —
  not "must be in VOC", since every verb is a VOC item and a verb entry with no
  arguments is useless.
- **Accept only `PA` and `S` VOC types**, so a mislisted verb fails when it is
  set up rather than at 3am.
- **Any prompt is fatal in this mode** (§6, the spinning prompt).
- **The name must be unique across the list**, or `-A` must match — never a
  silent override.
- **Set `@logname` explicitly**, since an unattended job has no person behind it.
- **Catalogue batch programs locally**, so they do not become runnable from
  every account.

**Rejected, so it is not proposed again:** a password on the command line
(readable through Task Manager, `Win32_Process` and ETW), a password file, and
hashing the VOC entry — the last on its own merits, because it pins one hop and
no further, and storing the command text rather than a name gets the same
protection for nothing. The reasoning still holds for any future secret: **a
capability list has nothing to leak or rotate, and a stolen credential grants an
interactive session where a list grants a fixed set of commands.**

**What it does not fix.** The account boundary is **not** a data boundary — a
Q-pointer in the batch account's VOC reaches another account's files. And **who
may trigger a job is still open**: the list says what may run, not who may fire
it. The batch account is also the one place per-directory ACLs work in stage 1,
since exactly one principal ever runs there.

### Open, undiagnosed: `BASIC` produced no object in SDSYS on a reused file name

18 Aug 2026, on the 11:35:44 install. `verify-catgate.ps1` created a scratch
directory file in SDSYS, compiled into it and catalogued — fine on a fresh tree,
twice. On the first run to reuse a name an earlier run had `DELETE.FILE`d,
`CREATE.FILE` reported success and `BASIC <file> <prog>` then produced no
`.OUT`. Not reproduced since; the verifier now uses a per-run name and prints
what SD said, so a recurrence will carry its own diagnosis.

**Do not read the first account of this as evidence** — it claimed the VOC entry
was missing, which was an artefact of testing for `sdsys\VOC\<name>` as a file.
**A VOC record is not a file: `VOC` is a DYNAMIC file** (`CREATEA:575`), on disk
a directory of `%0`/`%1` buckets, so it holds two files whatever its record
count. That check could never pass and was removed.

### CLOSED 22 Aug 2026: every refused API login is audited

**THE GAP, WHICH WAS MEASURED BEFORE IT WAS FIXED.** `APISRVR` audited exactly
one refusal reason — `not in sdapi` — and that fires only **after** the SCRAM
proof succeeds. Everything failing earlier reached `scram.bad.cred` and wrote
nothing: a wrong password, an account with no `$cred` record, a version-1
credential, a rejected name. `verify-apiname` watched the `audit` file **not
grow at all** across five consecutive refused logins. Meanwhile §5.6's console
model logs every refused login and refused `LOGTO` (§7 step 4).

**WHAT WAS BUILT.** One writer, at `exit.vb.scram.fail`, driven by a new
`scram.refuse.reason`. **Every path out of both SCRAM handlers passes that
label**, which is the same argument `LOGIN`'s `terminate.connection` rests on —
a refusal added later is recorded whether or not its author thinks about the
trail. Seventeen sites set a reason; the three shared labels supply a default so
a site added without one still cannot be silent.

**THE REPLY TO THE CLIENT IS UNCHANGED**, deliberately: every credential failure
still answers `5017` after the same three-second sleep. The trail gets the
truth, the caller gets what it always got. **That is safe here because
`secure-audit.ps1` grants `sdusers` `(AD,RA,S)` — AppendData, and no
ReadData** — so an ordinary SD user cannot read the reasons back and use them to
enumerate accounts. **Check that ACL still says that before adding any further
detail to a record.**

**THE NAME IS SANITISED, AND THAT IS NOT FUSSINESS.** `audit_message()`
(`k_error.c`) writes its text **verbatim** and ends the record with a newline,
and these names have **not** passed `valid_os_name` — that is the point of
recording them. `scram.clean.name` caps at `MAX.USERNAME.LEN` and maps anything
outside `valid_os_name`'s own set to `?`, so `GITORLI\jim` is recorded as
`GITORLI?jim`. Without it a name containing a newline forges an audit line.

**THE COST, ACCEPTED.** A stranger can now make the server write a record — one
per connection, never faster than the existing `sleep 3`. An unlogged
authentication failure is the worse of the two, and `win32_audit_rotate()`
exists for the file. The changelog says so in as many words.

**VERIFIED 22 Aug 2026 — `verify-apiname.ps1 -Prefix sdapin2`, 17/17**, owner's
elevated run on the 08:32:03 install. Step 6 was **inverted** to the new
contract: the trail grew, `reason=name rejected by valid_os_name` and
`reason=wrong password` both appear and differ, the name appears **sanitised**,
and — the log-injection control — the **raw backslash form never appears**. What
the trail gained, verbatim:

```
API REFUSED user=GITORLI?sdapin2 reason=name rejected by valid_os_name
API REFUSED user=sdapin2 reason=wrong password
API REFUSED user=sdapin2?GITORLI reason=name rejected by valid_os_name
```

**AND THE DISCRIMINATOR STILL HOLDS** (step 5): all five refused spellings read
back to the client as `Invalid username or password`, identical to a wrong
password. The trail separates them; the caller cannot.

### Open, undiagnosed: the first verifier run after a cycle sometimes fails checks the second passes

**RESTORED TO THIS FILE 21 Aug 2026.** It was raised on 19 Aug 2026 and
explicitly *"kept in the file rather than closed"*, and then fell out of it
anyway — found while compressing §2 and §7, by reading the HISTORY entry that
records it (*"OS.EXECUTE is gated: the C half of step 7 is closed"*, and
*"An install spent on the intermittent check: three explanations dead"*).

**What was seen:** 138/142 then 142/142 with nothing changed between, roughly
**2 runs in 10**, cause unknown. Three explanations were spent ruling out and
are all dead: the `$RELEASE` prompt (`LOGIN:444` fires only on a stamp
mismatch, and both sides read `W1.0-0`), the revision cross-check, and the
installer's `ADOPT` step running SD.

**WHY IT IS KEPT RATHER THAN CLOSED, which is the whole point of the entry:**
the discipline here is *cycle, then measure*, and **a check that fails without
meaning it teaches whoever meets it to re-run until green** — which is how a
real failure gets waved through.

**It may already be gone, and that is not the same as knowing.** One later
instance was traced to the test being wrong rather than the tree — four checks
that looked for `voc_template`-only records in an account VOC built from
`newvoc`, where "Record not found" was the correct answer — and the verifier now
asserts the absence too. Whether that was the whole of it was never established.

**IF IT RECURS, CAPTURE THE RUN UNPIPED.** Both original sightings were lost
because the run went through `Select-String`, so `Start-Transcript` recorded the
command and not the answers.

**IT RECURRED 22 Aug 2026, ON THE 08:32:03 INSTALL, AND THIS SIGHTING HAS THE
BREAKDOWN THE OTHER TWO LACK.** Same verifier — the "142" in *138/142* is
`verify-lcnames` — and the same shape: **142/142 at 08:52, then 135/142 at
~09:00 with no source change between** (`assert-current` exit 0 either side).

**ALL SEVEN FAILING CHECKS BEGIN WITH `LOGTO SDSYS`**, and every one of the 135
that passed runs inside the invoking user's own account:

```
SDSYS: typing ACCOUNTS / MESSAGES / QFILE / OS.USERS is answered lower case
CT VOC COPYP shows a bare V type code
COPYP answers differently from an unknown verb
COPYP still reaches $COPYP itself
```

**That is a narrowing, not a diagnosis**: three of the seven are read-only
(`CT VOC COPYP`, `COPYP`, `LIST VOC COPYP`), so nothing was renamed and left
unrestored — what they share is only *entering SDSYS*. Previous sightings
recorded a count and no names, so "some checks" is now "the SDSYS-entering
ones". **The advice above was still not followed** — this run also went through
`Select-String` — but the tool captured the whole summary table anyway, which is
where the seven names came from. **Redirect to a file next time; do not rely on
that.**

**A SECOND, SEPARATE FAULT FOLLOWED AND MUST NOT BE CONFLATED WITH IT.** From
09:13:01 every session was `Forced logout` — but that began *after* sessions
were killed with `Stop-Process`, thirteen minutes after the 135/142 run, and is
§4's `check_lost_users()` entry, not this one. **The 135/142 happened first,
with the tree healthy.**

---

### Settled, kept because the conclusion is still operational

#### `RDPACCOUNT` was built and then deleted (20–21 Aug 2026)

**It is gone, and typing it now stops `CREATE.ACCOUNT` with `Unexpected token
(RDPACCOUNT)` and makes no account.** It existed for one day as a keyword letting
an SD-created account sign in to Windows. **Why it went:** the same Windows
setting covers Remote Desktop and the physical keyboard together, so an account
created with it could also walk up to the machine and log in, which was never
the intention. **The rule that now holds without exception: nobody SD creates can
log in to Windows at this machine unless they are already a Windows
administrator.** Phase 2 replaced it with the four-way route model —
`create.account user <n> ssh|api|both|none`.

**ACCOUNTS ALREADY CREATED WITH IT KEEP THEIR WINDOWS SIGN-IN**, because SD did
not record which they were. The changelog entry of 21 Aug 2026 has the manual
remedy.

**One thing it left behind, and one it resolved.** Left: **`sd LISTF` from a
desktop is refused while `sd` then `LISTF` works** — `check_admin()` gates the
command-line form (`sd.c:585`). Defensible, and only visible to a class of user
that no longer exists. Resolved: the comment at `sd.c:570-573` justifies that
gate with *"whoever is at the console or on Remote Desktop is an administrator,
because SD's own accounts are confined to ssh"* — **true again** now the keyword
is gone.

#### The console path stays exactly as it is (owner, 21 Aug 2026)

Neither dropped nor turned into a client of the service. It stays a privileged
administrator path, and **the behaviour that is there now is the specification**
— which unblocks the token work, because process-creation identity has to be
decided only for the sessions the SERVICE creates.

- **Entry is always your own account.** `sd` with no account named lands in
  `@logname`'s, administrators included.
- **`sd -ASDSYS` is refused, message `10051`.** `LOGIN:334` has **no elevation
  branch**, so an elevated session is refused the same way. `10002` is reachable
  only under `-internal`.
- **`LOGTO SDSYS` is the only door**, and entering SDSYS is what obtains
  privilege (`CPROC:2595`). `!elevate` answers 0 when the session is already
  elevated, so an elevated prompt sees no dialog and an ordinary one sees UAC.
- **Over ssh it fails by construction**: UAC draws on the interactive desktop and
  an ssh session has none. Windows enforces it, not a test here.

**"AN ELEVATED PROMPT PUTS YOU IN SDSYS AUTOMATICALLY" IS ONE STEP OUT**, and
the owner's own elevated session showed which: `who` → `27 DON`, then
`logto sdsys` → `27 SDSYS from DON` **with no UAC dialog**. So elevation buys a
**silent** `LOGTO SDSYS`, not a different destination. The automatic form was
true until 15 Aug 2026 and was deleted that day deliberately (`LOGIN:356`).

**That session is also the only measurement of any of this from a REAL
TERMINAL** — every verifier drives SD through a pipe — so `create.account user
test2` / `delete.account test2` typed at the `:` prompt is independent
corroboration of `verify-delaccount`.

#### The API is reached at its own port; posture B is gone (owner, 21 Aug 2026)

*"api through an ssh tunnel should be removed, it should only be allowed to the
port, normally 4243."* `sdwind.c open_api_listener()` binds `INADDR_ANY`,
`stage.py` ships `APIPORT=4243` **active**, and `gplbld/api-firewall.ps1` owns an
`SD-API-In-TCP` rule the installer creates (task `apiremote`, ***`Flags:
unchecked` since 25 Aug 2026*** — it was ticked by default until then; the owner
made it opt-in on finding that the two remote options defaulted opposite ways)
and the uninstaller removes.

***THAT IS A NARROWING OF POSTURE, NOT A REVERSAL OF THE 21 Aug DECISION.***
`APIPORT=4243` still ships **active** and `sdwind.c` still binds `INADDR_ANY`,
so the API is on and the port is open on the machine. What changed is only the
firewall rule the installer leaves behind: loopback unless asked. The cost is
recorded at the task itself — somebody who wanted a remote client and did not
read the task list now gets *"cannot connect"*.

**WHAT CHANGED IS NOT THE ARGUMENT FOR POSTURE B — IT IS WHAT STANDS IN FRONT OF
THE PORT.** Posture B was settled when the API login was cleartext and a session
that got in could open `$cred` and reach `OS.EXECUTE`. SCRAM-SHA-256 replaced the
login and the containment gate shut both, measured, so the port is no longer a
boundary doing work nothing else does.

**WHAT IS STILL TRUE, so this is a judgement and not a clean bill:** an API
session's TOKEN is still LocalSystem. Binding a network interface widens who may
**attempt** a SCRAM exchange; it does not widen what a session can do once in.

**`apiremote` is ticked while `sshremote` is unchecked, deliberately.** ssh has a
use for somebody who never wants a remote connection — a local user ssh'ing to
localhost, the case that made the ssh server mandatory. The API has no such case
after this change, so a firewalled-off port would ship a feature that does not
work. `sd.iss` says how to flip it in one flag.

**THE LINUX CLIENT CONTRACT CANNOT BE PORTED, AND THE REASON IS NOT ssh —
MEASURED 16 Aug 2026.** The Gambas3 client forwards a local TCP port to a UNIX
domain socket (`ssh -L <port>:/tmp/sdsys/sdclient.socket`). The ssh client
accepts that syntax; **the blocker is that MSYS2's AF_UNIX is not a socket
Windows can see.** A socket bound by MSYS2 is, from native Windows, a **54-byte
regular file** reading `!<socket >52445 s <cookie>` — the Cygwin emulation, a TCP
port plus a shared secret — where a native Windows AF_UNIX socket is a
zero-length reparse point. Demonstrated with a control on one socket at one
moment: MSYS2's own client connected and the server logged the accept; native
`curl.exe --unix-socket` on the same path failed in 0 ms and the server saw
nothing. **So `sshd`, a native Windows program, cannot reach a socket SD creates
through the MSYS2 runtime**, however the rest is built.

**AND THE NAMED PIPE IS NOT THE ANSWER TO PEER IDENTITY, which this section
asserted twice and was wrong both times.** A pipe in the Cygwin descriptor table
is **permanently ready** to `select()`, so `sdpoll()` spins and `sd.exe` never
answers (§7 step 11) — and `CN_PIPE` is not spare, it is SDLocal's own transport
(`sd.c:423`). **The answer is `GetExtendedTcpTable`**, which identifies the peer
of the socket `sdwind` already has and changes no transport; `make
check-peer-probe` proves it, and `verify-peerlog` measures it in place.

#### SDNet is gone (21 Aug 2026), and two residues are deliberate

`gplsrc/netfiles.c` is deleted and builds no object; `DELSRVR`, `SETSRVR` and
`LISTSRVR` are gone from `gpl.bp`; the three `*.SERVER` verbs are gone from
`voc_template`; and the semicolon dispatch in `op_dio1.c` is gone, so a name
containing `;` now falls through to `fullpath()` and fails like any other bad
pathname. Verified by `verify-nonet`, and `gcat` went 132 → 129, which is the
cheapest independent check that the removal reached the installed tree.

- **`gplsrc/sdnet.h` STAYS.** Despite the name it is a portability header —
  termios, netdb, the `SOCKET` typedef, `closesocket`, `NetError` — included by
  `linuxio.c`, `lnxport.c`, `op_skt.c` and the client library. **Deleting it
  would break the client library and terminal I/O.**
- **`NETFILES` is still parsed, stored and displayed, and is tested nowhere.**
  **Leave the parse**, or an `sd.conf` carrying the line stops SD loading —
  exactly as with `CREATUSR`. And leave the `sysseg` field, because removing it
  shifts the shared-segment layout and `SYSSEG_REVSTAMP` does not catch that.

**"A parameter that reads like a gate and gates nothing" is the shape worth
recognising again** — that is the whole of why this entry is kept.

#### The rest, in one line each

- **SDSYS reaches every account without exception, and `LOGTO` takes a
  registered account name only** — both answered by the owner on 13 Aug 2026 and
  written into §5.6. Direct directory access by path is not supported, which
  closes the bypass rather than resolving paths back to accounts.
- **`IsAdmin()` tests Windows `Administrators`; `sdadmins` is gone** (§5.6.1). It
  is referenced by nothing and the installer need not create it. Keeping an OS
  check on it would have inherited §6's sign-out-and-back-in trap, so `sd -start`
  would have failed for the installing user on every fresh install.
- **The binaries were purged from history on 13 Aug 2026**, and force pushed.
  **Any clone taken before that date is incompatible** — re-clone it; do not
  merge or push from one.
- **The LEFT ARROW in a Windows console is closed** — the default terminal type
  was `vt100`, whose arrows are the application-cursor-mode spellings, and SD
  never sends `smkx`. §5.18; `verify-keys` section 3 is the standing guard.
- **`usr/lib/systemd/` and `etc/xinetd.d/` are kept deliberately.** They have no
  function on Windows but they document the service topology — socket
  activation, ports, per-connection instances — that a Windows service must
  reproduce. Remove once that design is captured elsewhere.
- **The client library is LGPL-3.0-or-later with a linking exception** while the
  rest of the tree is GPL-3.0. Compatible and intentional for a client library,
  but a real licensing boundary.
