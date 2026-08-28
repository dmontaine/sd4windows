# PRE-RELEASE FIXES

Defects and gaps found **while writing the documentation**, which need deciding
or fixing before W1.0-0 is released. Started 26 Aug 2026.

**This file is maintained, not written once.** Add an entry when the
documentation work turns something up; move it to DONE with a date and the
commit when it is fixed.

***IT LISTS WHAT WE WOULD SHIP, NOT WHOSE FAULT IT IS.*** Owner's correction,
26 Aug 2026. [UPSTREAM_FIXES.md](UPSTREAM_FIXES.md) answers a different
question — *the maintainer of `sdb64` should know about this* — and **a defect
in both trees belongs in both files.** Being upstream's bug has never been a
reason to ship it, and being fixed upstream is not being fixed here. Entries
11 to 13 below are exactly that case and were missed for a day by a rule that
said otherwise.

**Why a separate file.** Writing a reference forces every claim to be checked
against what SD actually does, which is a different exercise from testing that
it works. Most of what follows was found by trying to write a true sentence.

`SEV` is the recommendation, not a ruling: **B** blocks the release, **S**
should be fixed, **M** minor.

| | SEV | what | where |
|---|---|---|---|
| ~~1~~ | **B** | ~~The `edit` / `micro` refusal message is malformed~~ — **DONE 27 Aug 2026** | `sdsys/gpl.bp/EDIT` |
| ~~2~~ | **B** | ~~The installing user gets no `OS.EXECUTE`~~ — **DONE 27 Aug 2026** | `sdsys/gpl.bp/CREATEA` |
| 3 | **S** | The live `SDSYS` VOC does not match `voc_template` | `sdsys/voc_template` |
| 4 | **S** | Tester page 07 says a standard account has 77 verbs; it has 81 | docs repo |
| ~~5~~ | **S** | `.d name` cannot find a lower-case VOC record typed in upper case — **FIXED 28 Aug: folds case like `.L`/`.R`, and reports 5043 instead of falling through with a stale `voc.rec`.** ***DONE 28 Aug 2026, MEASURED*** on the 00:53:34 install by `verify-vocverbs.ps1`: `.D ZZPRFD` printed `Delete VOC record 'zzprfd'?` — the lower-case name from an upper-case verb — the record was gone afterwards, and an unknown name reported 5043 with no second prompt | `CPROC:1119` |
| 6 | **S** | An empty directory called `C:` is created in the data tree by the installer | `gplbld/sd.iss` |
| 7 | **M** | `sort.item` is withheld from a standard account and `list.item` is not | `newvoc/TIER.OMIT.STANDARD` |
| 8 | **M** | `help` is an empty stub and F1 reaches it | `CPROC:2498` |
| 9 | **M** | `umask` is implemented and unreachable | `CPROC:3301` |
| ~~10~~ | **M** | ~~Two verifiers carry a dead ANSI strip~~ — ***IT WAS 23 FILES AND 24 OCCURRENCES, NOT TWO.*** **DONE 28 Aug 2026**: all converted to `([char]27 + '\[[0-9]*[A-Za-z]')`. ***AND IT WAS STILL SPREADING*** — three of the 23 were written the same day, by copying `probe-catprivate.ps1`'s `Invoke-SD` *"unchanged"*. **Guarded by a test, not by 23 comments**: `test-verdict-units.ps1` now scans the whole directory and fails if any script carries the dead form again, **tokenising rather than grepping** so a comment that quotes it (there are two, both correct) is not a false positive | `gplbld` |
| 11 | **B** | ***Nested `commit` silently loses the outer transaction's writes*** — UPSTREAM #17, **unfixed here** | `gplsrc/txn.c` |
| 12 | **S** | Error 3023 tells the user the disk may be full — UPSTREAM #20, **unfixed here**. ***28 Aug: NOT the message-only fix this entry claims — the call site is `gplsrc/op_dio3.c:853`, so it is a C change and a REBUILD, not a data change. Left out of the 28 Aug batch for that reason*** | `sdsys/messages/1407`, `gplsrc/op_dio3.c:853` |
| ~~13~~ | **M** | `qselect` prints its message without the list number — UPSTREAM #21. **FIXED HERE 28 Aug: `tgt.list` passed as the second argument.** ***DONE 28 Aug 2026, MEASURED*** by `verify-vocverbs.ps1`: the message ends in a list number, no dangling `select list `, and it selected more than zero. Still live upstream | `gpl.bp/QSELECT:240` |
| ~~14~~ | **S** | `delete.file ... no.query` still prompts, so it cannot run unattended — UPSTREAM #23. **FIXED HERE 28 Aug: `check.sdsys.file` takes the safe `N` branch under `no.query` and says so — new message 10117.** ***DONE 28 Aug 2026, MEASURED*** by `verify-vocverbs.ps1` on a copy of the `messages` pointer: 10117 printed, **6146 never asked**, the VOC reference gone and `sdsys\messages` still on disk. Still live upstream | `gpl.bp/DELETEF:222` |
| ~~15~~ | **M** | `delete.index` will not match a lower-case index name, though `list.index` will — UPSTREAM #22. **FIXED HERE 28 Aug: supplied names are case-corrected against the real ones, as `LISTI:147` does; an unknown name is still reported as typed.** ***DONE 28 Aug 2026, MEASURED*** by `verify-vocverbs.ps1`: `delete.index zzprfak f1` answered *"Deleted index F1"* and the file read back with no indices; **the control held too** — a genuinely unknown name came back **as typed**, not upcased. Still live upstream | `gpl.bp/DELETEI:155` |
| 16 | **S** | A killed session blocks exclusive access, says nothing about why, and only an administrator can clear it | `gplsrc/sd.c:333` |
| ~~17~~ | **B** | ~~`edit` / `micro` refuse a record whose text looks like a mark token~~ — **DONE 27 Aug 2026** | `sdsys/gpl.bp/EDIT` |
| ~~18~~ | **M** | ~~A text mark reaches the editor as a raw control character~~ — **DONE 27 Aug 2026** | `sdsys/gpl.bp/EDIT` |
| 19 | **B** | ***RE-OPENED 28 Aug 2026, ONE ROW OF SEVEN: THE `logto` DOOR WAS NEVER ADMITTED, AND THE CHECK THAT SAID IT WAS MATCHED THE ECHO OF ITS OWN COMMAND. REPRODUCED ON A SECOND ACCOUNT, `-Run b51` 16:54 — the fixed check FAILS the two `logto` rows while ssh and the API pass in the same leg, so the re-opening is measured twice and on two accounts.*** `verify-doors.ps1:255` was `Test-Say $out $acctU`, and the session echoes what it is fed, so `SDDRB50A` was in the transcript whether the `LOGTO` landed or not. **On the `-Run b50` Control leg SD printed 5161 *"Unable to change to new directory"* and `WHO` answered `91 DON` — the session never left `DON` — and the row scored PASS.** The same check scored the same PASS on `sddr2`, which is what the struck text below rests on. **Anchored on `WHO`'s answer now** (`^<number> <ACCOUNT>$`, the shape nothing typed can produce) **with 5161 as a disqualifier**, and both directions measured against the real transcript. ***THE CAUSE IS 44, AND THE CURE IS ALREADY WRITTEN DOWN IN THIS FILE***: the `logto` row of the door table below says **two** accounts — *"ssh as A and `LOGTO B`"* — and the implementation instead runs `LOGTO` in the caller's own session, whose token predates the `sdu_` group. **ssh and the API are unaffected: both authenticate afresh, and both remain measured.** ***THE REFUSAL HALF STILL STANDS*** — `logto.authorised` is called at `CPROC:2679`, **before** the chdir at `:2691`, so a suspended account is refused with 10107 and never reaches 5161. **What is unproven is the ADMITTED half of the pair, for one door of three.** Owner's to confirm; reversible if he reads it otherwise — ~~**DONE 28 Aug 2026. The owner's ruling was *"19 stays B until the doors are covered"*, and the condition is now met by a passing run rather than by argument.**~~ Six rows closed by `verify-tierchange.ps1` (28 PASS); ~~**the last row — the three doors — is closed by the `verify-doors` pair**, all four legs green on `sddr2`: `Create` 8/8, ***`Control` 6/6 with ssh, `logto` and the API ALL ADMITTED***, `Suspend` 5/5, ***`Refused` 4/4 with ALL THREE REFUSED***.~~ `LOGIN:477` and `CPROC:3776` said it in SD's own words (10107, *"Account SDDR2A is suspended"*) — **ssh after the banner, so authentication had succeeded and the refusal is SD's, with the account still in `sdssh` so no Windows group moved.** The API cannot identify its own refusal by design, so **the controlled pair is what proves it**: same account, same password, same call, admitted then refused, the suspension the only change. **Found and fixed a defect in the verifier on the way — see 42** | `gpl.bp/MODIFYA`, `gplbld/verify-tierchange.ps1`, `verify-doors-admin.ps1`, `verify-doors.ps1` |
| 20 | **S** | A suspended administrator is still a Windows administrator | `gpl.bp/MODIFYA` |
| ~~21~~ | **S** | ~~The write-once rule on `ACC$PRIOR.TIER` is unreachable, and four documents say it is what makes field 6 safe~~ — **dead test deleted, docs corrected 27 Aug; compiled + installed 17:25:59, `b48` is the regression check** | `gpl.bp/MODIFYA`, `syscom/KEYS.H` |
| ~~22~~ | **M** | `create.account` says a password was not set and never says why — **FIXED 28 Aug: `!set_passwd` ALREADY set the reason and the caller discarded it. `status()` is read immediately and 10118-10121 name the four cases; the "not elevated" one says a retry cannot help.** ***DONE 28 Aug 2026, BOTH ARMS MEASURED*** by `verify-acctmsgs.ps1` — **31 PASS / 0 FAIL / 0 SKIP**, `-Prefix sdmsgb`. **Mismatch**: 10118 printed, the other three of the four messages absent, and answering `N` unwound the creation. **Windows refused**: 10119 printed **naming the account**, with the mismatch and unelevated messages absent and the retry still offered. ***THE REFUSAL ARM NEEDED THE MACHINE'S POLICY CHANGED*** — owner's ruling: `net accounts /minpwlen:14`, run, then `/minpwlen:0` to put it back, **and it is back, read after the run**. **The first attempt SKIPped**: it sent a 150-character password on the reasoning that 127 is a hard SAM limit for a local account, and `Set-LocalUser` accepted it. The password is now **chosen from the policy** — `Get-PasswordPolicy` reads it with `secedit`, `Select-RefusedPassword` breaks whichever rule is in force | `gpl.bp/CREATEA:498` |
| ~~23~~ | **S** | ~~`term default` sets 20x24, the MINIMUM width, not SD's 120x36 default~~ — UPSTREAM #24. ***DONE 27 Aug 2026***, installed 17:25:59 and **measured: `term` reports 120 x 36**. **Docs corrected too**, `SDCoreWindowsDocs` `c41d999` | `gpl.bp/TERM:165` |
| 24 | **S** | ***`sd -cleanup` never releases a dead session's task locks*** — UPSTREAM #25, **unfixed here** | `gplsrc/clopts.c:300` |
| ~~25~~ | **S** | ~~`encrypt.field` is in every administrator's VOC and `$CRYPTO` is not in the distribution~~ — UPSTREAM #26. ***DONE 28 Aug 2026, MEASURED on the 00:53:34 install: `verify-tiers` 33 PASS, ADMINISTRATOR 416, STANDARD and PROGRAMMER unmoved.*** **Fixed by taking the entry's recommended option: the `voc_template` record is DELETED and the name removed from `TIER.ADD.ADMINISTRATOR`. ADMINISTRATOR's VOC is 416, re-derived from the directory; STANDARD and PROGRAMMER unmoved. `verify-tiers.ps1` and PROJECT_STATUS §A1 updated with it.** ***UNCOMPILED. Reversible in one commit if you would rather ship a `$CRYPTO`*** | `sdsys/voc_template/encrypt.field`, `newvoc/TIER.ADD.ADMINISTRATOR` |
| ~~26~~ | **S** | `delete.file` *name* `no.query` prompts twice when the name is typed in lower case — UPSTREAM #27. **FIXED HERE 28 Aug: both the DATA and DICT path comparisons are case-insensitive.** ***DONE 28 Aug 2026, MEASURED*** by `verify-vocverbs.ps1`: `delete.file zzprfw no.query` fired **neither** prompt and deleted DATA, DICT and the VOC entry. ***NOT tested with `force`, which is what this entry's summary in START HERE asked for and which CANNOT FAIL*** — `DELETEF:250`/`:319` guard both prompts with `if not(force)`. Still live upstream | `gpl.bp/DELETEF:233` |
| ~~27~~ | **M** | `modify.account` *acc* `add`/`delete` makes the same group change as `grant`/`revoke` and writes no audit record — **FIXED 28 Aug: a `K$AUDIT` record after each successful edit, naming the verb, on the model of `GRANTA:208`/`:233`.** ***DONE 28 Aug 2026, MEASURED*** by `verify-acctmsgs.ps1` on the 00:53:34 install: **both** `MODIFY.ACCOUNT ADD account=… to=…` and `… DELETE account=… from=…` appeared in the bytes the run added to `sdsys/audit`, **with the controls first** — 10018 and 10021 in SD's own output, since the record is written inside `if stat = 0` and a failed edit would otherwise read as a missing audit record | `gpl.bp/MODIFYA:344` |
| 28 | **M** | A process dump is written into the system directory, where every SD user can read it | `gplsrc/pdump.c:97` |
| ~~29~~ | **S** | ~~`micro` reports "Permission denied" on every save~~ — **DONE 27 Aug 2026**, install 19:37:47. `MICRO_CONFIG_HOME` is a per-user `~/.micro` via the new `micro-home.ps1`. Owner: three runs, save and no-save, **no message**. Took three attempts — see the entry | `gpl.bp/EDIT`, `gplbld/micro-home.ps1` |
| ~~30~~ | **S** | ~~`verify-osusers.ps1` refuses on a fresh install: it needs `@LOGNAME` unlisted in `os.users`, but PRE_RELEASE 2 made `adopt-account` list every administrator~~ — **verifier fixed 27 Aug (parks and restores the record); the product is correct** | `gplbld/verify-osusers.ps1` |
| 31 | **S** | ***`verify-apiadmin`'s control is stale*** — it expects an elevated session `LOGTO`'d into a PROGRAMMER account to lose `OS.EXECUTE`, but `os_permitted()` keys the list on `process.username` (`don`), whom PRE_RELEASE 2 listed. Product is per design; **verifier needs a rewrite, owner to confirm the new premise**. Headline hole (API OS.EXECUTE) stays closed | `gplbld/verify-apiadmin.ps1` |
| ~~32~~ | **S** | ~~`delete.account` leaves the `ProfileList` registry entry, so an account recreated under the same name gets a DIFFERENT home directory~~ — **FIXED 27 Aug 2026: the `catch { exit 6 }` that left both halves is now `catch { }`, and the key is removed in its own right; status 6 splits into 6 (directory) and 7 (registry entry).** ***UNCOMPILED — needs a cycle.*** Generated PowerShell parse-checked 0 errors / 203 tokens; the new steps run read-only against a real account | `gpl.bp/DELETE_USER`, `gpl.bp/DELACC`, `messages/10075`, `messages/10116` |
| ~~33~~ | **S** | ~~`allow-ssh-groups.ps1`'s own usage text offers a bare form that **writes nothing**~~ — **DONE 27 Aug 2026**, the usage line names `-Installed` and a dated note says which forms need it. Comment only, parses 0 errors / 1247 tokens | `gplbld/allow-ssh-groups.ps1:4` |
| 34 | **S** | ***`release.ps1` cannot complete on the `Technical` set*** — `checklinks.py` rightly refuses a zero-link set, and two pages in, `Technical` still has no honest cross-reference. A whole set has no working release command. **Owner's call, and not to be settled by adding a link** | docs repo `tools/release.ps1`, `tools/checklinks.py` |
| 35 | **S** | ***A profile DIRECTORY left behind moves the next account's home just as the registry entry does*** — found by running 32's own regression test on the install that fixed 32. `DELETE_USER` now tries to remove it, **and MEASURED: it cannot be deleted OR renamed while the hive is mounted**, so the honest answer is the rewritten `10075`, which names the cause and the restart. **Cure is 36** | `gpl.bp/DELETE_USER`, `gpl.bp/DELACC`, `messages/10075` |
| 36 | **M** | ***Deleted accounts leave their registry hives mounted — 22 orphan SIDs / 44 hives on this host*** — the ROOT CAUSE of 32 and 35. **Mechanism confirmed: `Remove-CimInstance` failed on a mounted hive, then cleared `53 removed, 0 failed` after a restart.** Nothing SD does can unmount them. ***RULED 27 Aug 2026 AND NOT BUILT: keep BOTH halves on failure, directory first, and reclaim the pair from a sweep at SD service start — not the machine-wide Windows per-days policy. `create.account` REFUSES on an existing directory. No restart in the delete path*** | Windows lifecycle; `gplbld/clean-test-profiles.ps1`, `gplbld/install-service.ps1` |
| ~~37~~ | **S** | ***`create.account` prints two lines that contradict each other***: with `both` it says *"may sign in over ssh only"* then *"may sign in over ssh and use the API"*. **Two different gates** — Windows logon rights (`CREATEA:808`) and SD route keywords (`:1612`) — worded so nothing tells the reader that. **FIXED 28 Aug: 10034 now says "may reach this computer only over ssh"; 10076/10077/10078 are recast as "SD routes for %1: ...". Nothing anchors on the old text — checked.** ***DONE 28 Aug 2026, MEASURED*** by `verify-acctmsgs.ps1`: on a real `create.account … programmer both`, 10034 read *"may reach this computer only over ssh"* and 10078 *"SD routes for …: ssh and the API"*, **and both old wordings were absent** — the disqualifier is what carries this one, since both lines contain "ssh" and any check anchored there would have passed on the defect | `messages/10034`, `10076`, `10077`, `10078` |
| ~~38~~ | **M** | ***WIRED IN 28 Aug 2026 ON THE OWNER'S RULING — "wire the pair into VerifyInstall".*** `gplbld/verify-doors-suite.ps1` drives all five phases as **one step** and is the **last step of `VerifyInstall1`**, conditional on `-Run`. ***IT HAD TO GO IN THE UNELEVATED RUNNER, AND THAT IS FORCED, NOT PREFERRED***: the phases need alternating tokens (Create elevated, Control ordinary, Suspend elevated, Refused ordinary, Remove elevated) and **an elevated parent cannot make an ordinary child** — `runas /trustlevel` yields a RESTRICTED token, not the user's own (`VerifyInstall1.ps1:70`) — so the ordinary half must be the parent. It raises the three elevated children itself, **announcing each UAC prompt**, and the child redirects its own output because `-Verb RunAs` cannot be combined with `-RedirectStandardOutput`. **It refuses a prefix with any residue before creating anything** — Windows user, `sdu_` group, `ACCOUNTS` record, **or profile directory** — because a name is single-use once its account has reached the Control leg. ***COSTS: three more UAC prompts, and one permanent profile directory per suite run until 35/36 is built.*** **Unrun as a suite step** — the refusal path was exercised (exit 2, nothing created) and the five phases were run by hand. **The original finding:** ~~The suite tests SUSPENDED on no door at all~~ — neither `verify-tiers.ps1` nor `verify-tierapi.ps1` contains the word. ssh and `logto` are now measured by hand; **the API door has never been reached** and cannot be tested by wording, since `APISRVR:507` refuses with the same `sysmsg(10003)` as every other refusal. **Needs a controlled pair.** ***28 Aug: `verify-tiers.ps1` section 6 written and UNRUN — the record, the write-once guard 21 left unmeasured, and the VOC. It CANNOT test the `logto` door: the check sits after `CPROC:3729`'s elevated bypass and this verifier must be elevated.*** ***THE CONTROLLED PAIR NOW EXISTS AND HAS PASSED, 28 Aug 2026*** — `verify-doors-admin.ps1` + `verify-doors.ps1` on `sddr2`, all four legs green, **all three doors ADMITTED then all three REFUSED**, and ***the API door was reached for the first time***. **WHAT IS LEFT OF THIS ENTRY IS ONE DECISION, NOT A MEASUREMENT: the pair is standalone and is NOT wired into `VerifyInstall1`.** It is deliberately unwired for the same reason `verify-acctmsgs` is — **it creates a real Windows account**, and it needs an elevated half and an unelevated half, which is the split the suite already has. **Owner's call: wire it into the two runners, or leave it standalone and named in the docs.** Note the fixture is single-use — its Control leg's ssh login leaves a profile directory that entries 35/36 cannot yet remove, so each attempt needs a fresh prefix. ***RUN AS A SUITE STEP FOR THE FIRST TIME ON `-Run b50`, 28 Aug 2026, AND IT FAILED TWICE FOR TWO DIFFERENT REASONS.*** First run: `Create` 8/8 and `Control` 6/6, then **Suspend and Remove died before their UAC prompt** — entry 43. Second run, after the same cycle: **refused up front**, because the first run had already spent `sddrb50a` at the Control leg — **the single-use guard working exactly as designed, and nothing was created.** ***THE PRICE IS NOW MEASURED RATHER THAN ESTIMATED***: a failed run leaves a **live, enabled, UNSUSPENDED** account in `sdusers`, `sdssh` and `sdapi` plus its profile directory, because the leg that removes it is the one that did not run. **43 is fixed and unrun; the next attempt needs a fresh `-Run` token** | `gplbld/verify-tiers.ps1`, `verify-tierapi.ps1`, `verify-doors-admin.ps1`, `verify-doors.ps1`, `verify-doors-suite.ps1` |
| 39 | **B?** | ***Uninstalling strips SD's `AllowGroups` and `ForceCommand` and leaves every account SD created*** — so each becomes an ordinary ssh-reachable account with a PowerShell shell. `sd.iss` removes no account anywhere; the closing disclosure does not mention them. **Reasoned from source, not measured — run an uninstall first.** Owner's call | `gplbld/sd.iss:3367`, the closing disclosure |
| ~~40~~ | **M** | ~~A verifier's transcript keeps recording the verifiers that run after it~~ — `verify-sshonly-*.log` carried `verify-apiadmin`'s `[FAIL]` rows and the whole suite's summary. `Start-Transcript` with no matching stop, **15 of 33 verifiers**. **DONE 28 Aug 2026, AND FIXED IN THE TWO RUNNERS RATHER THAN IN FIFTEEN VERIFIERS**: `VerifyInstall1` and `VerifyInstall2` now close every transcript a step left open, **name the step that leaked**, and `VerifyInstall1` restores its own with `-Append`. **One place, it cannot be forgotten by the next verifier somebody writes, and it also covers the case a `try`/`finally` does not — a step that dies outright.** ***Mechanism verified against real nested transcripts*** (none-open, three-leaked, and the runner's close-and-restore shape), **not yet in a suite run** | `gplbld/VerifyInstall1.ps1`, `VerifyInstall2.ps1` |
| 41 | **M** | ***The cleanup sweep reports "every section reached zero" while three orphan directories are still on disk*** — the counter and the cleaner share one `Win32_UserProfile` enumeration, which reads from `ProfileList`, so a directory whose entry is gone is invisible to both. **Measured 28 Aug: `7 -> 0` and "done" with `sdapiab49`, `sdapiidb49`, `sdapinb49` still there.** **DONE 28 Aug 2026** — both scripts now carry a **direct `C:\Users` scan** as a second, independent instrument: `clean-test-profiles.ps1` names them **UNREACHABLE with the reason and exits non-zero** (*before* its "nothing to do" return, which is the path the measured run took), and `cleanup-devlitter.ps1` counts them in **both** BEFORE and AFTER and will no longer say *"every section reached zero"* over them. ***Reported, not deleted*** — the removal decision is 36's. ***AND THE POSITIVE CONTROL FOUND A SAFETY BUG IN THE FIX***: under a permissive pattern the scan returned **`All Users`, a junction to `C:\ProgramData`**, for which the code prints a `Remove-Item -Recurse -Force` line. **Reparse points are now excluded in both copies**, and the guard is exercised by a test. **36's boot sweep must not inherit the blind enumeration** | `gplbld/clean-test-profiles.ps1`, `cleanup-devlitter.ps1` |
| ~~42~~ | **M** | ***FIXED 28 Aug 2026 ON THE OWNER'S RULING — "prompt for password at creation".*** `!set_passwd` now writes SD's own credential through `!CRED_SET` from the **same prompt** that sets the Windows one, so 10078 is true of a new account. **One prompt, both stores; they remain separate credentials and `modify.password` still changes SD's alone.** New status **6** — the half-set case, Windows took it and `$cred` did not — with message **10122**, and `CREATEA` names it rather than falling through to 10121's *"status %1"*. ***THE FIX IS COMPILED-AND-UNRUN UNTIL A CYCLE***: it is the first `sdsys` change since 28 Aug 00:53:34, so the installed tree is stale and nothing can test it until one runs. **The original finding:** ~~`create.account ... both` announces the API as a route, but the account cannot use the API until `modify.password` is run~~ — 10078 prints *"SD routes for %1: ssh and the API."* while the only password the verb prompts for is the **Windows** one (*"New Windows password for %1"*). **The two doors authenticate against different stores and nothing says so**: sshd checks the Windows password, so ssh is admitted; the API does SCRAM against a PBKDF2 verifier in `sdsys\$cred` that **only `MODIFY.PASSWORD` writes**, so it refuses. ***Measured 28 Aug 2026, the first time the API door was ever reached***: `sddr1a`, created `PROGRAMMER BOTH`, was in `sdapi`, `sdssh` **and** `sdusers` — the route was granted and the credential did not exist — and `sd-connect` answered `QMError(): Invalid username or password`. **The refusal is the worst possible one to debug**: `APISRVR:507` deliberately answers `10003` for *"no such account"* and *"not granted"* too, so nothing in it points at a missing password. `SET_ACC_PASSWORD:195-198` already owns the sentence — *"ssh and the SD API will refuse to connect until a password is set"* — but it is printed by the wrong verb and is **wrong about ssh**, which the Windows password admits. **Owner's call: prompt for the SD password at creation, or have 10078 say the API needs one.** `verify-doors-admin.ps1` also runs `MODIFY.PASSWORD` itself, and that stays — it keeps the door pair working against an install predating this fix. ***ONE SENTENCE IS STILL WRONG AND IS LEFT ALONE DELIBERATELY***: `SET_ACC_PASSWORD:195-198` tells someone declining a first password that *"ssh and the SD API will refuse to connect"*, and **ssh does not** — a Windows password admits it, which is exactly what `sddr1a` did. That path is now reachable mainly for SDSYS at install, since creation unwinds without a password; **worth correcting when someone is next in that file** | `gpl.bp/SET_PASSWD`, `gpl.bp/CREATEA`, `sdsys/messages/10122`, `sdsys/messages/10078` |
| ~~43~~ | **S** | ~~***The door suite's Suspend and Remove legs could never elevate, so the suite could never pass***~~ — **DONE AND WITNESSED 28 Aug 2026, `-Run b51` at 16:54.** ***THE FIX IS NOT MERELY WRITTEN: BOTH ELEVATED LEGS LAUNCHED AND THE `Remove` LEG RAN AS A SUITE STEP FOR THE FIRST TIME EVER*** — `Create` **8/8** on `argv (15)` with the password masked, `Remove` **2/2** on `argv (13)` with no `-Password` at all, and the run left **no Windows account, no `sdu_` group and no `ACCOUNTS` record** behind (read from disk afterwards; only the 35/36 profile directory remains). **The printed argv is what makes it checkable at a glance**, and it is in the transcript of every leg now. `Invoke-ElevatedPhase` passed `'-Password', $Password` unconditionally, and Suspend and Remove take no password (`verify-doors-admin.ps1:58` defaults it to `''`). ***`Start-Process -ArgumentList` CARRIES `[ValidateNotNullOrEmpty()]`, AND ON A COLLECTION THAT VALIDATES EVERY ELEMENT***: one `''` rejects the whole list with *"The argument is null or empty"* and **nothing launches**. Measured on `-Run b50`: Create carried a password and ran 8/8, Suspend and Remove died **before their UAC prompt**, so the account was left unsuspended and the Refused leg could not run. **The pair is now built conditionally** — the idiom `sd-elevate.ps1:118` already used for its optional `-LogFile` — with the **argv and its element count printed**, and an **empty element refused by name** rather than by a binding message that identifies none. `gplbld/test-doorsargv-units.ps1` guards it: **35 of 35**, no install, no elevation, no account; ***its positive control is `-Suite <copy carrying the old form>`, run and observed FAILING 27/8***. The live cmdlet's rejection was measured directly, not reasoned | `gplbld/verify-doors-suite.ps1`, `test-doorsargv-units.ps1`, `assert-current.ps1` |
| 44 | **S** | ***CONFIRMED BY THE SUITE ITSELF, `-Run b51`, 28 Aug 2026 16:54, on a SECOND account — this is not a one-off.*** With the instrument honest the Control leg reported **2 of 7 decisive checks failed**, both of them the `logto` rows (*"entered the account"* expected True got **False**; *"did NOT report 5161"* expected False got **True**), while **ssh and the API both admitted** in the same leg — the three-door comparison inside one run, which is stronger evidence than either door alone. The suite then **stopped at the right place** (*"a door refused BEFORE the suspension, so its refusal after one would prove nothing"*) **and still ran `Remove`**, so nothing live was left behind. ***`LOGTO` authorises on the machine's group list and then fails the chdir on the token's, and says only "Unable to change to new directory"*** — an administrator who has just run `create.account` is in the new `sdu_<acct>` group **on the machine** but **not in their own token**, because Windows fixes group membership at logon. So `logto.authorised` (`CPROC:2679`) passes, the chdir at `:2691` is denied, and 5161 is all the user sees. **Measured 28 Aug 2026 with a control**: `Get-LocalGroupMember sdu_sddrb50a` → `GITORLI\don` **present**; the same live unelevated token → `sdu_sddrb50a` **absent** while `sdusers` (granted before a reboot) **present**, so the enumeration works and the absence is real. **The record already knew the mechanism** — PROJECT_STATUS §6 *"group membership is fixed in the token at logon"* — **but nothing connects it to this message.** 5161 is also `SETACC:67`. ***Owner's call, and there are three shapes***: say so in 5161 when the account was reachable but the directory was not; have `create.account` print the sign-out line it already prints elsewhere; or leave it. **It is also why 19's `logto` door cannot be measured from the creating session** — the door table in this file already specifies the cure, *"ssh as A and `LOGTO B`"* | `sdsys/gpl.bp/CPROC:2691`, `SETACC:67`, `sdsys/messages/5161` |

***THE EIGHT "COMPILED AND INSTALLED — UNTESTED" ENTRIES NOW HAVE VERIFIERS,
AND ALL EIGHT ARE STRUCK.*** 28 Aug 2026. Entries **5, 13, 14, 15, 26** are
`gplbld/verify-vocverbs.ps1` — ***36 PASS / 0 FAIL***; **22, 27, 37** are
`gplbld/verify-acctmsgs.ps1` — ***31 PASS / 0 FAIL / 0 SKIP***. Both need an
**elevated** shell, and both ran against the 00:53:34 install, so no cycle was
spent. **Neither passed first time, and neither first failure was the
product**: `verify-vocverbs` stopped at 21 of 22 because `LIST.INDEX` prompts
when given no index name, and `verify-acctmsgs` SKIPped entry 22's refusal arm
because the password it guessed was accepted. **Nothing moves to DONE on the
strength of a script existing** — strike an entry only when a run has printed
its rows. PROJECT_STATUS.md START HERE carries both commands
and the three corrections to the tests those entries' own summaries suggested:
**26 cannot be tested with `force`** (both prompts are already guarded by
`not(force)`, so that form passes on the defect), **22's `a` is accepted on a
machine whose minimum password length is 0**, and **13's bare `qselect` form
stops at 3290** for want of an active select list.

***UPSTREAM #18 AND #19 ARE FIXED IN THIS TREE*** and are deliberately not
listed above — `op_config.c` and `op_skt.c`, both 26 Aug 2026, each citing its
UPSTREAM_FIXES number in its own history block. **They are the reason 11 to 13
are worth stating separately**: four upstream defects were found while
documenting, two were fixed here and two were not, and nothing recorded which
was which.

---

## 3. The live `SDSYS` VOC does not match `voc_template` — **S**

Measured 26 Aug 2026 while writing the query-processor page.

| | |
|---|---|
| `%L` `%G` `%E` and the two-character forms | **ship in `voc_template` and in `newvoc`, and are ABSENT from the live `SDSYS` voc.** `ct voc %L` answers *Record '%L' not found* |
| `=` | **is in the live `SDSYS` voc** as `K` / `25`, and is in **neither** `newvoc` nor `voc_template` |

So the `%`-form comparison operators do not work in `SDSYS`:
`count voc with dispatch %L "I"` returns `0 record(s) counted` and two *not
found* complaints, where `lt`, `<` and `before` all return 381.

**`<` and `>` cannot be VOC records on this port at all** — they are illegal
NTFS file names, and `newvoc` and `voc_template` are directory files. They work
anyway, so the parser is not taking them from the VOC. That is worth
understanding before changing anything here.

***UNTESTED AND IT MATTERS: a user account is built from `newvoc` by `CREATEA`,
which copies every record, so a user account probably DOES get the `%` forms and
`SDSYS` does not.*** No standard account survived the suite teardown, so this
was not measured. The published operator table lists only spellings that were
run.

## 4. Tester page 07 says a standard account has 77 verbs — **S**

It has **81**. `Testing/markdown/07-programmer-commands.md` opens with the
wrong number, and page 06 repeats it.

**77 is a count of VOC records whose field 1 begins with `V`.** It misses the
four records that are a keyword *and* a verb — `break`, `count`, `display`,
`off` — whose fields 3 onward are a complete verb record. `CPROC:1718`
re-parses from field 3, so all four are typeable, and none is on
`TIER.OMIT.STANDARD`.

**Confirmed three ways.** `CREATEA:961`-`996` copies every `newvoc` record
except the two list records and, for a standard tier, the 42 omitted names —
with no filter on record type, so 123 − 42 = 81. SD's own VOC dictionary
encodes the same rule in its I-type `DISPATCH` field. And
`count voc with dispatch # ""` answers **144** in `SDSYS`, matching a file scan
of the shipped tree exactly (`CA` 97, `IN` 45, `OS` 2).

## 5. `.d name` cannot find a lower-case VOC record typed in upper case — **S**

`CPROC:1119` tries the name as typed and then `upcase` only. `.l` (`CPROC:1176`)
and `.r` (`CPROC:1204`) try as typed, then `downcase`, then `upcase`.

So a paragraph saved as `daily` can be listed and recalled by typing `DAILY`
and **cannot be deleted** by typing `DAILY`.

**Ours, not upstream's** — upstream `CPROC` has **0** `downcase` calls and this
port's has 15, so §5.12's fold missed a site. It is not among the four the
section records as left deliberately.

**Second, smaller fault at the same place:** if both reads fail, `voc.rec` keeps
its previous value and is then tested for `S`/`PA`, and there is no *not found*
message on this path — `.l` has one (sysmsg 5043) and `.d` does not.

## 6. An empty directory called `C:` is created in the data tree — **S**

`C:\ProgramData\SD\sdsys\C:` exists, is empty, and is stamped **26 Aug 2026
21:17:46 — twenty-four seconds into the 21:17:22 install**. So the installer
makes it, not a running session.

Consistent with the POSIX-versus-Windows path confusion that stopped the editors
working: something built a path from a drive-letter fragment and created it
relative to the data tree. **Chase it in `sd.iss` / `finish-install.ps1`, not in
the interpreter.**

***28 Aug 2026: STILL REPRODUCED, AND THE ADVICE ABOVE IS NOT WHERE IT WAS
FOUND.*** `C:\ProgramData\SD\sdsys\C:` exists on the 27 Aug 22:52:21 install,
empty, stamped **22:52:43 — 21 seconds in**, so every install makes one.
**What was ruled out**: no `CREATE.FILE` is issued by anything under `gplbld`
at install time (`finish-install.ps1` and `adopt-account.ps1` issue none), and
`sd.iss` names no such path.

**The shape that matches is `verify-parsertokens.ps1`'s subject** — a TCL token
truncated at the first backslash, leaving `C:` as a record id. **But that
parser defect was fixed on 22 Aug and this directory postdates the fix**, so
either a second site still splits, or something builds the path without going
through `PARSER` at all. **Not chased further; it needs a session with a cycle
to bisect.** Left out of the 28 Aug batch because it is an investigation rather
than an edit.

## 7. `sort.item` is withheld from a standard account and `list.item` is not — **M**

`sort.item` is on `newvoc/TIER.OMIT.STANDARD`; `list.item` is not. Both print
whole records field by field, so withholding one and not the other achieves
nothing. **Looks like an oversight in the list rather than a decision** — worth
confirming, because if it was deliberate the reason should be written down.

## 8. `help` is an empty stub and F1 reaches it — **M**

Internal verb 14. `CPROC:2498`'s body is entirely commented out and it returns
immediately; `f1.help` at `:2500` falls into the same empty routine, so **F1 at
the command prompt does nothing.** No VOC record in `newvoc` or `voc_template`
points at verb 14, so the name is not recognised either — measured:
`help is not in your VOC`.

**Decide whether F1 should say something** rather than silently doing nothing.
The documentation is the help system now, and the pages say so.

## 9. `umask` is implemented and unreachable — **M**

Internal verb 35. `CPROC:3301` is a working routine that reports or sets the
file-creation mask, and **no VOC record points at it**, so it cannot be typed —
measured: `umask is not in your VOC`. `umask()` from SD BASIC still works.

Either ship a VOC record for it or delete the routine; a working verb nobody can
reach is the kind of thing that reads as a missing feature.

## 10. Two verifiers carry a dead ANSI strip — **M**

`gplbld/probe-catprivate.ps1:165` and `gplbld/verify-catgate.ps1:133` both hold
``$out -replace "`e\[[0-9]*[A-Za-z]"``. **`` `e `` is not an escape in Windows
PowerShell 5.1**, so the pattern is the literal letter `e` and strips nothing.

**Already recorded** — PROJECT_STATUS.md §6 says every ANSI strip in `gplbld` is
dead code and names `verify-nocase.ps1` and `verify-tiers.ps1` as carrying it
harmlessly; these two were not on that list. `verify-osusers.ps1` does it
correctly with `[char]27`.

Not shipped, so it costs nothing at release — but it silently mis-scores any
check whose anchor spans an escape sequence, and it did exactly that on
26 Aug 2026 before the raw output was read.

---

# UPSTREAM DEFECTS WE STILL SHIP

**The analysis is in [UPSTREAM_FIXES.md](UPSTREAM_FIXES.md) and is not repeated
here.** What these entries add is the only thing that file does not say:
***whether our own tree still carries it.*** Checked against the source, not
remembered.

## 11. Nested `commit` silently loses the outer transaction's writes — **B**

**UPSTREAM_FIXES #17. Live in this tree, verified 26 Aug 2026:** `txn_depth` is
incremented at `gplsrc/txn.c:96` and decremented at `:592`, and `op_txncmt()`
does **neither** — it touches neither `txn_depth` nor the transaction stack.

***THIS IS THE ONE THAT MATTERS ON THE WHOLE LIST.*** It is silent partial data
loss inside the one construct whose entire purpose is that there is no such
thing, and `system(1008)` climbs for ever so nothing reports it.

***DO NOT FIX HALF OF IT.*** Decrementing `txn_depth` in `op_txncmt()` would
make `system(1008)` trustworthy while the data-loss path stayed, which is worse
than both being visibly wrong. The owner has it in front of him and the
sequencing is his.

## 12. Error 3023 tells the user the disk may be full — **S**

**UPSTREAM_FIXES #20. Live in this tree, verified 26 Aug 2026** — our
`sdsys/messages/1407` still reads:

```
Error %d (o/s %d) writing record (Possible full disk?)
```

Error **3023** is *"write/delete with no lock"*, so the first application to
wrap a working `WRITE` in a transaction without locking first is sent to check
disk space. **Ships in the message file, so it costs no rebuild** — the fix is
a second message id special-cased at the call site, leaving 1407 accurate for
the disk-full case it was written for.

## 13. `qselect` prints its message without the list number — **M**

**UPSTREAM_FIXES #21. Live in this tree, measured 26 Aug 2026** —
`gpl.bp/QSELECT:240` passes one argument to a two-parameter message, so every
successful `qselect` ends with a dangling *"select list "*. `NSELECT:112` two
files away supplies both and is the model. One line, and `tgt.list` is already
in hand on the line above.

Documented as a known blemish in the select-lists page so a reader does not go
looking for a list that is there.

## 14. `delete.file ... no.query` still prompts — **S**

**UPSTREAM_FIXES #23. Live in this tree, measured 26 Aug 2026** —
`gpl.bp/DELETEF:222` and `:297` call `check.sdsys.file` with no `no.query`
guard, and that subroutine prompts unconditionally.

***IT COST A SESSION THE DAY IT WAS FOUND.*** `delete.file zzak force no.query`
was issued down a pipe on the strength of `no.query`, hit the system-account
prompt, ate the following commands as answers and hung; killing it left a
user-table slot that needed an elevated `sd -cleanup` to clear. **Anything that
drives SD non-interactively is exposed** — a build script, a test harness, the
verify suite.

The safe branch already exists: `N` deletes the VOC reference and leaves the
system file alone. Honouring `no.query` by taking it, or refusing the
combination up front, both beat a prompt nobody can answer.

## 15. `delete.index` will not match a lower-case index name — **M**

**UPSTREAM_FIXES #22. Live in this tree, measured 26 Aug 2026** —
`gpl.bp/DELETEI:155` compares with an exact `locate` against names held upper
case, where `gpl.bp/LISTI:147` upcases both sides first. So `list.index zzak f1`
finds the index and `delete.index zzak f1` answers *"Unrecognised index name
(f1)"*.

**Worth a look alongside item 5**, `.d name` in `CPROC` — different files,
different authors, same shape: two commands that should agree about a name and
one of them folds case. Whatever policy is settled for one should settle the
other.

## 16. A killed session blocks exclusive access, explains nothing, and only an administrator can clear it — **S**

***THIS ONE IS OURS, AND IT FOLLOWS FROM OUR OWN HARDENING.*** Upstream's
`-CLEANUP` runs unguarded (`sdb64 gplsrc/sd.c:297`); ours calls `check_admin()`
first (`gplsrc/sd.c:333`), which asks `IsElevated()`. That was the 15 Aug 2026
decision to gate every administrative switch, and **the reasoning still looks
right** — `cleanup()` acts on everybody's sessions. What was not considered is
what an ordinary user does afterwards.

**The chain, all of it measured on 26 Aug 2026:**

| | |
|---|---|
| a session dies without logging out | its user-table slot survives; `listu` still lists it |
| `build.index` on a file it had open | *"Cannot gain exclusive access to file"* — **in a session that never opened the file** |
| `logout` *n* | *"Force logout initiated"*, then the entry reads **`(logout pending)` for ever** — logout signals a process that no longer exists |
| `sd -cleanup` | clears it, and **requires elevation** |
| `logout` itself | is an **administrator** verb, so it is not a programmer's route either |

***THE MESSAGE IS THE WORST PART.*** *"Cannot gain exclusive access to file"*
points at the file. Nothing points at a dead session, and the user has no reason
to run `listu` — which is administrator-only anyway. **A programmer whose ssh
connection drops cannot fix their own `build.index`, and cannot find out why.**
Dropped connections are routine over ssh, which is the access route this port is
built around.

**Two independent things to decide, and they are separable:**

1. **Diagnosis.** The refusal could name the session holding the file, the way
   `sdprobe2.ps1` requires a contender to name the holder before a lock
   measurement counts. That is useful even when the holder is alive.
2. **Recovery.** Either let `logout` *n* reap a slot whose process is gone
   instead of marking it pending for ever, or give an unprivileged user some
   way to clear their own dead session. `-CLEANUP` acting on everybody is a
   fair reason to keep its gate; it is not a reason to leave the user stuck.

***AND THE AUTOMATIC SWEEP DOES NOT RECOVER IT. MEASURED 26 Aug 2026.***
`sdwind`'s `check_lost_users()` is supposed to find an entry whose process is
gone — `kill(pid, 0)` — every five minutes and shell out to `sd -cleanup`.

**User 58, pid 363, logged in 22:57, was still listed by `listu` at 23:07** with
`sdwind` running throughout. **Ten minutes is at least two full sweep
intervals**, so this is not a case of not having waited: the entry outlived the
mechanism meant to remove it, and was cleared only by an elevated `sd -cleanup`
run by hand.

*(An earlier draft of this entry said the sweep had not been given long enough
to judge, which was true of the first stale entry — watched about four minutes
— and is not true of this one.)*

**So there is no automatic recovery, not merely an awkward manual one.** That
raises the cost of everything above: the user cannot fix it, cannot diagnose it,
and waiting does not help either.

**What is still open is WHY**, and PROJECT_STATUS §6 already says not to guess
between the two candidates — `sd -cleanup` misjudging, or `kill(pid, 0)`
answering wrongly for an MSYS2 pid. **That question is now worth answering**,
because the same §6 entry records the sweep on 22 Aug 2026 doing the opposite
and forcing out healthy sessions for twenty minutes. A sweep that misses dead
entries and evicts live ones is one bug or two, and nobody has looked.

---

## DONE

## 1. The `edit` / `micro` refusal message is malformed — **B** — DONE 27 Aug 2026

Reported by the owner, 26 Aug 2026; seen again by him on 27 Aug in the refusal
that raised item 17.

`check.permitted` built a multi-line refusal by concatenating `char(10)` — a
bare LF — and `EDIT` printed the whole thing with **one** `crt`. Eight sites
built text that way. A bare LF advances a line without returning to column 0,
so every line after the first started where the previous one ended:

```
:edit bp test
edit is not available to don.
                            It runs an editor outside SD, so it needs OS.EXECUTE permission: field 2 of your record in
the SD system file os.users, which only an administrator can change.
                                                                    ed, the line editor, needs none of this.
```

**A pipe hides it**, which is why it survived: down a pipe the LF *is* the
separator and the same message reads perfectly.

***FIXED AT THE ONE PRINT SITE, NOT THE EIGHT BUILDERS.*** `end.program` now
splits `error.text` on `char(10)` and writes one `crt` per line. That is the
fix for the class rather than for the message: a message written next year
cannot reintroduce it.

**Not verified on a console yet** — it is compiled BASIC and wants a cycle.

## 17. `edit` / `micro` refuse a record whose text looks like a mark token — **B** — DONE 27 Aug 2026

Reported by the owner, 27 Aug 2026, editing a source record in `SDSYS`:

```
This record cannot be edited with micro.
Its text and the ~~ and ~` marks cannot be told apart, so saving it would
change data you did not edit.
ed, the line editor, handles it without any of this.
```

His ruling with it: ***"the whole purpose of these editors is primarily to edit
source code without having to use ED... the conversion of field, value and
subvalue marks needs to be handled seamlessly, just like CRLF or LF."***

**The guard was doing what it was written to do.** `process.record` converted
`@vm` to `~~` and `@sm` to `` ~` ``, converted back, and refused any record
where the two differed. Three kinds of text tripped it: a literal `~~`, a
literal `` ~` ``, or a `~` immediately before a mark.

***AND `sdsys/gpl.bp/EDIT` WAS THE ONLY SOURCE RECORD IN THE SHIPPED TREE THAT
IT REFUSED.*** Measured across `sdsys` and `user_accounts`: the only other hits
are `gcat` and `gpl.bp.out` object records, which nobody edits. **The program
refused itself, because it carries the token strings as constants.**

**The fix is an escape character.** `~` now escapes, and a tilde is written
`~-` **only where the next character would make the pair look like a token** —
another `~`, a backtick, a `-`, `@vm` or `@sm`. Everywhere else it is left
alone, so `a~b` is still `a~b` in the editor and ordinary source reads
normally. `marks.out` in `EDIT`. *(It was
`escape.tildes` and three `change()` calls for about an hour; item 18 added a
third mark and the run separator the same day, and the decode had to become a
left-to-right scan — a separator is a token that exists only by virtue of where
it sits, and `change()` has no notion of where it is.)*

**The round-trip check stays** and is now expected never to fire; if it does,
that is a defect in `EDIT` rather than a property of the record, and its
message says so.

***PROVED BEFORE THE CYCLE, NOT AFTER.*** `gplbld/test-edittokens-units.py`
runs the same algorithm over **every string up to six characters** drawn from
`~`, `` ` ``, `-`, `@vm`, `@sm` and one ordinary letter — **55,987 of them, 0
lossy** — and over **all 197 shipped `gpl.bp` records, 17 of which contain a
tilde, 0 lossy**. It asserts the corpus contains tildes, because a lossless
answer over records with no tilde in them would be true and would prove
nothing.

**Not upstream.** `sdb64`'s `GPL.BP/MICRO` does no mark conversion at all —
see UPSTREAM_FIXES #16, fault 4, added the same day.

**Not verified on a console yet** — it is compiled BASIC and wants a cycle.

## 18. A text mark reaches the editor as a raw control character — **M** — DONE 27 Aug 2026

Found 27 Aug 2026 while correcting the changelog for item 17, and **the entry it
corrected was itself wrong**: the changelog said text marks were *"covered by
that same refusal rather than being left to surprise you"*, and they never were.
The round trip only converted `@vm` and `@sm`, so a record containing `@tm`
converted to itself, compared equal, and passed the guard untouched. It then
went to the editor as `x'FB'`.

***THE OWNER ADDED THE MARK THE SAME DAY.*** `~!` is a text mark, and it is
`~!` rather than his first proposal `` `~ `` because he spotted that a token led
by a backtick breaks the rule that every token starts with `~` — which would
make the backtick a second escape-introducing character needing its own escape.

**And with three marks the runs needed separating.** Consecutive marks are now
written with a comma between their tokens — `~!,~!,~~` — because token against
token they cannot be read. A literal comma standing in exactly that position is
written `~,`.

Proved the same way as item 17, over an alphabet that now includes `!`, `,` and
`@tm`: exhaustive to length 6 in the routine test and **once to length 7,
5,380,840 strings, none lost.**

## 2. The installing user gets no `OS.EXECUTE` — **B** — DONE 27 Aug 2026

Owner's instruction, 26 Aug 2026 and again on the 27th: administrators are to
*"have access to os.execute, ssh and api by default without escalating"*.

***TWO OF THE THREE ALREADY HELD, AND THAT WAS RE-MEASURED RATHER THAN
QUOTED.*** `CREATEA` gives an ADMINISTRATOR both routes and no keyword can take
either away (21 Aug 2026); `MODIFY.ACCOUNT` refuses to remove them for the same
reason (10083). Checked live on this install, 27 Aug: `Get-LocalGroupMember`
shows `don` — the ADMINISTRATOR-tier account the installer adopted — in **both
`sdssh` and `sdapi`**.

**`OS.EXECUTE` was the one that did not**, and `C:\ProgramData\SD\sdsys\os.users`
held **0 records** on a fresh install, so nobody had it. Both gates that read
that list — `CPROC`'s `sh` gate on field 1, and `op_sh.c`'s `os_permitted()` on
field 2, which is also what `EDIT`'s `check.permitted` reads — fall back to
*elevation*, and an unelevated administrator is an ordinary user by design
(`kernel.c`: *"An administrator who has not elevated is an ordinary SD user,
exactly as on Linux"*). That is why he met *"edit is not available to don"*.

**The fix is one place: `CREATEA`'s new `grant.os.access`.** An
ADMINISTRATOR-tier **USER** account is written into `os.users` as it is created
— ADOPT included, so the installing user gets it — with **both** fields `yes`.

***IT IS DATA, NOT A SECOND GATE, AND THAT IS THE PART WORTH KEEPING.*** The
26 Aug ruling had a second half: teach `EDIT`'s `check.permitted` the
ADMINISTRATOR tier as well. **That was deliberately not done.** One list already
answers *"may this person reach the operating system"*; it is readable and
editable; a tier test beside it would make the answer depend on two things that
can disagree, and `os.users` is keyed by **person** while a tier belongs to an
**account**, so the two do not even ask the same question. The cost of the
narrower choice: an administrator whose record is deleted or set to `no` **is**
refused, rather than the tier overriding. That reads as correct — a default that
can be edited — but it is a narrowing of the earlier ruling and is flagged as
one.

**Both fields, not only field 2.** They are the two halves of one capability —
field 1 is the `sh` verb and `!`, field 2 is `OS.EXECUTE` from a program and the
editors. Granting one and not the other would leave an administrator able to run
`os.execute` from BASIC and refused at the prompt.

**And `DELETE.ACCOUNT` takes it away again**, but only where SD is deleting the
Windows login itself: the record is keyed by the person, so removing it for a
login that survives would take a permission from somebody who still has a reason
to hold it. Without that, the verify suite would leave one behind every run.

***AND IT GAINED KEYWORDS THE SAME DAY.*** Owner, 27 Aug 2026: `sh-on` and
`os-on` on `CREATE.ACCOUNT`, and `sh-on`, `sh-off`, `os-on`, `os-off` on
`MODIFY.ACCOUNT`. **Four switches over two fields**, not four names for one
state as `SSH`/`API`/`BOTH`/`NONE` are — `sh-off` leaves `OS.EXECUTE` alone.
`MODIFYA`'s new `os.set`, and `CREATEA`'s `grant.os.access` now reads the two
flags rather than testing the tier itself.

**The hyphen is his** (`os-on`, not `os.on`) and it parses: `PARSER`'s
simple-token arm splits at a space, a comma, a bracket or a quote and at
nothing else, so `os-on` arrives as one token with `keyword = -1`.

***AN ADMINISTRATOR IS NOW REFUSED BY `os.set`, BUILT 27 Aug 2026.*** The
version first committed treated ssh and the API as a **rule** and
operating-system access as a **default**, so `os-off` worked on an
administrator. **He overturned that the same afternoon**: *"administrators have
full access, there should be no way to turn it off."* `os.set` carries
`route.set`'s `S-1-5-32-544` guard now, with its own message **10106**, and the
three places that argued the old way — both program headers, the changelog
entry, and page 26 — are rewritten.

**Not verified** — it is compiled BASIC and wants a cycle. After one, `os.users`
should hold a `don` record with two `yes` fields, and `modify.account don
os-off` should print *"don is an administrator and always reaches the operating
system"*.

---

## 19. The tier change and `SUSPENDED` compile but have never run — **B**

***28 Aug 2026 — THREE OF THIS ENTRY'S CLAIMS ARE NOW FALSE, AND TWO OF THEM
WERE FALSE WHEN WRITTEN.*** Read this block before the original below it; the
original is kept because its table is still the specification.

- ***"NOT ONE LINE OF `tier.set` HAS EXECUTED" — no longer true.***
  `verify-tiers.ps1` section 6 ran on the 00:53:34 install, **33 PASS / 0
  FAIL**: suspend, a second suspend, the restore, and the VOC across
  `UPDATE.ACCOUNT`.
- ***"AND THE TEST CANNOT BE PIPED" — WRONG WHEN WRITTEN.*** The reasoning was
  that `CREATE.ACCOUNT USER` prompts for a password and a prompt down a pipe
  eats the following lines. **It does not, when the whole script is sent as ONE
  string with LF separators** — that is PROJECT_STATUS §6's fix for the phantom
  blank line, and `verify-tiers.ps1` had been creating accounts that way for
  weeks. Confirmed again 28 Aug: `verify-acctmsgs.ps1` piped **four**
  `CREATE.ACCOUNT USER … PROGRAMMER BOTH` with passwords, twice over.
  **The trap is real but it is about verbs given no argument, not about
  passwords** — see START HERE's `LIST.INDEX` finding.
- **"AND THERE IS NO VERIFIER" — half true.** `verify-tiers.ps1` section 6
  covers **the round trip, the write-once rule, the VOC across a release
  update, and the null case**. It deliberately does **not** cover the three
  doors, and says so in its own output rather than scoring them.

***WHAT IS ACTUALLY LEFT, THEREFORE, IS THREE ROWS OF THE TABLE BELOW*** — the
required keyword (10111), what leaves with ADMINISTRATOR, and the "left alone"
count (10113's third number) — **all three testable from an elevated piped
session**, plus **the three doors, which are not, and are PRE_RELEASE 38.**

***AND THOSE THREE ARE NOW MEASURED.*** `gplbld/verify-tierchange.ps1`,
**28 PASS / 0 FAIL**, `-Prefix sdtc1`, on the 00:53:34 install:

- **the required keyword** — 10111 named the account, the success wording was
  **absent**, and tier, Windows group and `os.users` were **all unchanged
  afterwards**. A refusal that had already done half the work would have passed
  the first two rows alone.
- **what leaves with ADMINISTRATOR** — Windows `Administrators` membership and
  the `os.users` record, both asserted **present** after the promote, so their
  removal is a transition and not an absence. 10115 said so as well.
- **the "left alone" count** — `added 0, removed 19, kept 1` against 20
  administration verbs, and ***`D = 397` by two independent routes***:
  `A + added − removed` and `P + kept`. The edited record is provably still
  there and provably the only difference. **No count is typed.**

***ONE ROW IS LEFT — THE THREE DOORS — AND IT IS ENTRY 38's.***

***RULED BY THE OWNER, 28 Aug 2026: "19 stays B until the doors are covered."***
So this entry is **OPEN**, **`B`**, and **not to be struck, folded into 38, or
downgraded** on the strength of the other six rows being measured. Everything
remaining in it lives in 38, which is an `M` — striking this one and pointing
there would be tidy and would move a release blocker onto a minor entry.

***WHAT CLOSES IT IS COVERAGE, NOT ARGUMENT.*** The three doors are
`LOGIN:477`, `CPROC:3776` and `APISRVR:507`, each answering **10107** except the
API, which answers 10003 and must stay indistinguishable from *"no such
account"*. Until something exercises all three against a genuinely suspended
account, this is a blocker.

***THE VERIFIER FOR THEM IS WRITTEN AND UNRUN, 28 Aug 2026*** —
`gplbld/verify-doors-admin.ps1` (elevated fixture) and `gplbld/verify-doors.ps1`
(unelevated measurement). **A pair, because the halves need opposite tokens**,
and the measuring half **refuses to run elevated**: `logto` reaches its
suspension test only after `CPROC:3729`'s bypass, so an elevated session enters
a suspended account correctly and a door test written there would report the
design as a fault. Five phases — **Create → Control → Suspend → Refused →
Remove** — with the control leg mandatory, because a door that refuses *before*
the suspension makes its later refusal worthless. **`-Prefix sddr1` is free.**
***THIS ENTRY STAYS `B` UNTIL THAT PAIR HAS RUN AND PASSED*** — a written
verifier is not coverage.

Built 27 Aug 2026, sixty-sixth session. `MODIFY.ACCOUNT` gained four tier
keywords, `SUSPENDED` became a fourth `ACC$TIER` value with `ACC$PRIOR.TIER`
(field 6) beside it, and three doors learnt to refuse a suspended account.

***THE CYCLE OF 27 Aug 12:05 SETTLED THE COMPILE AND NOTHING ELSE.*** `MODIFYA`
0 errors, 189 units all clean, **zero `is not assigned a value` warnings**, and
the four benign warnings appear in identical counts in the 11:11 log that
predates the commit. The messages and both dictionary items are in the install
and **both dictionary items resolve** — `list sd.accounts` prints a `Tier`
column and `list sd.accounts tier prior.tier` prints `Tier` and `Was`.

***NOT ONE LINE OF `tier.set` HAS EXECUTED.*** `MODIFY.ACCOUNT` is
`kernel(K$ADMINISTRATOR,-1)`, seeded from `IsElevated()` at process start, so
an unelevated session stops at 2001 before the parser. `voc.delta`, the three
doors, the write-once rule on field 6 and ruling 1's refusal are all
unexercised.

***AND THE TEST CANNOT BE PIPED.*** `CREATE.ACCOUNT USER` prompts for a
password — mandatory since 21 Aug 2026, and `NO.QUERY` does not suppress it; it
covers the confirmation at `CREATEA:501`. A prompt in a piped session eats the
following lines and waits, and `sdtcl.ps1`'s banner is explicit that the
timeout path **costs the install**, not just the run. It has to be typed at an
interactive elevated session.

***AND THERE IS NO VERIFIER.*** `verify-tierchange.ps1` does not exist, because
§"Verify a script loads before you submit it for execution" forbids handing
over one that has never been loaded against a live install — and it cannot be,
until the cycle runs. **What it has to cover, so the next session does not
re-derive it:**

| | |
|---|---|
| the round trip | PROGRAMMER → SUSPENDED → PROGRAMMER leaves field 5 back at PROGRAMMER, field 6 empty, and the VOC record count unchanged |
| the write-once rule | SUSPENDED twice must leave field 6 holding the ORIGINAL tier, not `SUSPENDED`. **This is the one a naive test passes by accident** — it only fails on the second suspension |
| the three doors | ssh/console (`LOGIN`), `logto` from an unelevated account (`CPROC`), and the API (`APISRVR`, which answers 10003 and must NOT be distinguishable from "no such account") |
| the required keyword | `modify.account x programmer` on an administrator is REFUSED with 10111; with `both` it succeeds |
| what leaves with ADMINISTRATOR | out of Windows `Administrators`, and the `os.users` record gone |
| **the "left alone" count** | edit one VOC record in the account first, then downgrade. It must be **counted and kept**, not deleted. Nothing else tests that rule |
| the null case | a tier change that matched nothing must FAIL, not pass: assert the VOC record count actually MOVED before believing a green |

**Anchor on the success wording, not the account name.** `Account %1 is now %2`
is 10109 and appears only on the positive path; the account name appears in
every refusal too.

---

## 20. A suspended administrator is still a Windows administrator — **S**

Owner's ruling of 27 Aug 2026 is that a suspension is enforced at SD's doors
and withdraws **nothing** on Windows, which is what makes lifting one free —
there is no prior state to record and restore. The consequence, stated rather
than discovered later:

- The account's user stays in Windows `Administrators`, so they can still
  elevate **on the machine**. SD refuses them; Windows does not.
- Their `os.users` record survives, so `OS.EXECUTE` and the screen editors are
  still permitted **to that person** from any account they can still reach.
- The ssh connection is still accepted and `sd` still starts. The refusal comes
  from `LOGIN`, not from `sshd`.

**None of this lets them back into the suspended account** — all three doors
test field 5. It matters where a suspension is being used to contain somebody
rather than to park an account, and that distinction is worth a sentence in
page 32 when it is written.


---

## 21. The write-once rule on `ACC$PRIOR.TIER` is unreachable — **S**

Measured 27 Aug 2026 by running it. `SYSCOM/KEYS.H`, `tier.set`'s banner,
PROJECT_STATUS.md's START HERE and HISTORY.md all state that field 6 is safe
because `MODIFY.ACCOUNT` writes it **only on the transition into SUSPENDED**.

A second `modify.account <acct> suspended` answered ***"B48TIER is already
SUSPENDED; nothing changed"*** — sysmsg 10110, the **equality guard** at the
top of `tier.set`, returning before the field-6 write is reached.

**It is unreachable rather than merely unexercised.** `old.tier` is upcased and
trimmed and `want.tier` is one of four upper-case literals, so reaching the
write with `want.tier = 'SUSPENDED'` already implies `old.tier # 'SUSPENDED'`.

***AND THE GUARD NOW HAS A REGRESSION CHECK, 28 Aug 2026.*** Deleting the inner
test left the equality guard as the whole write-once mechanism, on an argument
that nothing measured. `verify-tiers.ps1` section 6 suspends a **PROGRAMMER**
account, suspends it again, and asserts `ACC$PRIOR.TIER` still reads
`PROGRAMMER` — if the guard ever stops returning, `SUSPENDED` overwrites it and
the only record of what the account was is gone for good. **PASSED in the
00:07:29 run.** See PRE_RELEASE 38.

***THE BEHAVIOUR IS CORRECT AND ONLY THE EXPLANATION IS WRONG*** — field 6 is
preserved, and the round trip was measured lossless (SUSPENDED with field 6
`STANDARD` → PROGRAMMER gave **42 added**, where a lost field 6 would have
given 0). So this is not a defect in what SD does; it is four documents
describing the wrong guard, which is the kind of thing that survives until
somebody deletes the equality guard and believes the other one is holding.

**The fix**: delete the unreachable inner test, and say at the equality guard
that it is also what protects field 6.

***DONE IN SOURCE 27 Aug 2026, UNCOMPILED.*** The inner
`if old.tier # 'SUSPENDED'` at the field-6 write in `tier.set` is deleted;
`MODIFYA`'s banner, a new comment at the equality guard, and `syscom/KEYS.H`'s
field-6 note all now say the equality guard (sysmsg 10110) is what keeps
field 6 write-once. **Behaviour is unchanged** — it was already correct. Rode
in with PRE_RELEASE 23 and 29 once 29 had taken the tree off `assert-current`;
the owed `cycle.ps1` compiles it. PROJECT_STATUS.md START HERE item 4.

---

## 22. `create.account` says a password was not set and never says why — **M**

Seen 27 Aug 2026 while making a test account. `CREATEA:498` calls
`set_passwd()`, and on failure prints sysmsg 10008 — *"Warning, user created
but password not set, Retry (Y/N)"* — with **no reason**.

The two candidates a caller cannot tell apart are the two most likely ones:
**the two entries did not match**, and **Windows rejected the password** on
length or complexity policy. The retry loop is friendly, but somebody who hits
the second case can retype a matching pair for ever.

`!set_passwd` knows which it was. Passing that back, or printing the two cases
distinctly, is the fix.

---

## 23. `term default` sets the minimum width, not the default — **S**

Found 27 Aug 2026 while writing *SD TCL - The Terminal and the Session*, by
running the verb rather than by reading it. `term default` then `term`:

```
Page width: 20
Page depth: 24
```

**SD's default terminal size is 120 x 36.** `gpl.bp/INT$KEYS.H` defines
`DEFAULT.WIDTH 120` and `DEFAULT.DEPTH 36`, and `LOGIN:213-221` uses both as
the fallback when `LINES`/`COLUMNS` and terminfo say nothing. `TERM:165` sets
`width = MIN.WIDTH` — 20 — and hard-codes depth 24.

***THIS IS NOT COSMETIC.*** The shipped `@` dictionary records and the default
`LIST` layouts are formatted for 120 columns; the changelog records that work.
At 20 columns every standard report wraps. **A user who types `term default` to
put things back makes the display worse**, and has no reason to suspect the
verb they just used.

**Also upstream's** — `sdb64`'s `GPL.BP/TERM` carries the identical lines
164-166 and the identical constants — so it is filed as UPSTREAM_FIXES #24 as
well. Being upstream's is not a reason to ship it.

**The fix is two lines** and is written out in the upstream entry.

***DONE — FIXED, INSTALLED AND MEASURED, 27 Aug 2026.*** `gpl.bp/TERM`'s
`KW$DEFAULT` arm now sets `DEFAULT.WIDTH` / `DEFAULT.DEPTH` (120 x 36). The
`sdterm` depth-25 special case was removed, not kept — see UPSTREAM #24 for why.
Shipped in the owner's `cycle.ps1` of 27 Aug (install 17:25:59) alongside
PRE_RELEASE 21 and 29.

**The owner ran it at his own prompt:** `term default` prints nothing — it sets
and returns, which is what that arm does and is not a defect — and the bare
`term` after it reported **120 x 36**. Against the recorded `20` / `24` before
the fix, that is the whole claim, measured on the installed tree.

***THE THREE DOCUMENTS THAT DESCRIBED THE OLD BEHAVIOUR ARE CORRECTED — NOTHING
IS LEFT ON THIS ENTRY.*** `SDCoreWindowsDocs` `c41d999`, 27 Aug 2026. *SD TCL -
The Terminal and the Session*, tester page 13 and page 02 all told the reader
**not** to use the verb and to type `term 120,36` instead; each now states what
`term default` does, and keeps the one fact that surprises people — **it prints
nothing**, so a bare `term` after it is how you see the result. Tester 13 also
keeps one line saying it used to set 20 x 24, because a tester may hold notes
from an earlier build. Re-rendered with `tools\release.ps1`: Testing 15 pages /
77 links / 0 broken, User 33 / 185 / 0, and markdown-against-PDF checked
separately per the docs `README` — 48 pages, 0 stale, 0 missing.

It was the exact case that `README` warns about: **a page whose value is a
measured defect is the page a fix invalidates.**

## 24. `sd -cleanup` never releases a dead session's task locks — **S**

**UPSTREAM_FIXES #25. Live in this tree**, read at `gplsrc/clopts.c:299-302`
and confirmed identical on upstream `main`.

`remove_user()` takes the dead user's number into `user_no` and then uses
`process.user_no` in the **task-lock** loop, where the three loops below it —
file locks, record locks, group locks — all use `user_no`. `cleanup()` never
becomes a user, so `process.user_no` is **zero**, a free slot is also zero, and
the loop clears free slots and nothing else. **No task lock is released by
cleanup at all.**

***IT MATTERS HERE MORE THAN THE ONE-WORD FIX SUGGESTS.*** `sd -cleanup` is
this project's standard recovery from a killed session and appears in
PROJECT_STATUS.md, in `sdtcl.ps1`'s and `sdprobe.ps1`'s timeout banners, and in
the tester documentation. **All of it promises a recovery that is incomplete**,
and the gap is invisible until something takes a task lock. Nothing in the
shipped tree does, so this has never been hit; an application that guards a
nightly job with `lock 3` would hit it the first time it was killed.

**The remaining ways out are `unlock tasklock` *n*, elevated, or restarting
SD.** Both are documented on *SD TCL - Locks*, which states the defect rather
than leaving it to be discovered.

**The fix is one word**, in C, so it costs a full cycle rather than a
`-SkipInstall`.

## 25. `encrypt.field` is in every administrator's VOC and `$CRYPTO` does not exist — **S**

**UPSTREAM_FIXES #26. Live in this tree**, measured 27 Aug 2026 on the
12:06:20 install:

```
:encrypt.field
00001FCB: Unable to load '$CRYPTO' object code at line 1550 of $CPROC
```

`sdsys/voc_template/encrypt.field` is `CA $CRYPTO 6`; the name is in
`newvoc/TIER.ADD.ADMINISTRATOR`, so **every administrator account gets it**.
There is no `$CRYPTO` in `sdsys/gpl.bp`, none in the installed `gcat`, and
nothing of that name anywhere under `C:\ProgramData\SD`.

***THIS IS A SHIPPED VERB THAT CANNOT WORK***, and the message it produces
names `$CPROC` and an internal line number rather than what the user typed.
**Removing the VOC record is the smaller and more honest fix** — *Verb not
found* is a better answer than a loader error — and nothing in the
documentation or the tester set refers to the verb.

**Decide before release**: ship a `$CRYPTO`, or drop the record from
`voc_template` and from `TIER.ADD.ADMINISTRATOR`. Either is a data change, so a
cycle, not a rebuild.

***DONE 28 Aug 2026 — the record is deleted and the name is out of the list.***
Written before the cycle that will test it, so the run is a check rather than an
observation:

| `verify-tiers` row | expected |
|---|---|
| `add list length` | **20**, not 21 — and it is derived from `$AdminVerbs.Count`, so a mismatch here means the shipped record and the test disagree |
| `shipped TIER.ADD.ADMINISTRATOR matches this test` | **0 differences** |
| `sdtierN3 COUNT VOC` | ***416*** |
| `sdtierN1` / `sdtierN2 COUNT VOC` | **354** / **396**, ***unmoved*** |

***THE TWO THAT DO NOT MOVE ARE THE CHECK.*** The verb was only ever
ADMINISTRATOR's, so it leaves one of the three sums and not the other two. If
STANDARD or PROGRAMMER also moves, the removal took something it should not
have and the count is not the thing to adjust.

***THE PREDICTION HELD ON ALL FOUR ROWS.*** Cycle installed **28 Aug 00:53:34**,
`assert-current` clean, `verify-tiers` **33 PASS / 0 FAIL**: `add list length`
20, 0 differences against the shipped record, ADMINISTRATOR **416**, STANDARD
354 and PROGRAMMER 396 unmoved. **`encrypt.field` is gone from an administrator's
VOC and nothing else moved with it.** ***This entry is DONE.***

**An unpredicted corroboration:** `assert-current` counts **2974** files across
the six mirrored directories against **2970** on the previous install — exactly
the five new messages less the one deleted VOC record. The file census and the
VOC arithmetic agree without being told about each other.

## 26. `delete.file` *name* `no.query` prompts twice when the name is typed in lower case — **S**

**UPSTREAM_FIXES #27, and separate from #14** — that one is
`check.sdsys.file`, on the system-account path. This one is on the ordinary
path, in the caller's own account, and **it fires on every file created and
deleted using the project's own house style.**

`DELETEF:233` guards message 6135, *OK to delete DATA portion*, on `force`
alone; `no.query` is not tested there or at the matching test for the
dictionary part. And `CREATEF`'s *Form operating system file name from VOC
record name* block upper-cases the name before storing it, while `DELETEF`
compares against the name **as the caller typed it**. So the two differ
whenever the verb was typed in lower case, and both prompts fire.

***MEASURED, AND IT COST A RUN BEFORE IT WAS UNDERSTOOD.***
`tools\probes\p31-locks.b` in the docs repository first hung on exactly this
and left a user-table entry and an `RU` lock on a `voc` record. It now stacks
`data 'Y'` answers and captures the output, which is where the evidence comes
from:

```
OK to delete DATA portion 'ZZLK31A'? Y | DATA portion 'ZZLK31A' deleted |
OK to delete DICT portion 'ZZLK31A.DIC'? Y | DICT portion 'ZZLK31A.DIC' deleted |
VOC entry 'zzlk31a' deleted
```

***THE LOWER-CASE HOUSE STYLE IS WHAT MAKES THIS OURS TO WORRY ABOUT.*** Step
7.8 made lower case the way commands are written here and the documentation
teaches it. Upstream's convention hides the same code. **Anything that drives
SD non-interactively and deletes a work file is exposed** — the verify suite,
build scripts, and every probe in the docs repository.

Comparing case-insensitively, or honouring `no.query` beside `force`, both fix
it; the upstream entry argues for the first. BASIC, so `-SkipInstall` will tell
you it compiles and a full cycle is needed to test it.

## 27. `modify.account` *acc* `add`/`delete` writes no audit record — **M**

`GRANTA` writes `kernel(K$AUDIT, 'GRANT account=... to=...')` after every
successful group edit, and the same for `REVOKE`. **`MODIFYA:344`'s `add` and
`delete` arms make the identical `os_group('ADDMEM'/'DELMEM', ...)` call and
write nothing.**

So *who may enter this account* can be changed by two different verbs and only
one of them leaves a trail. **The audit file is the answer to "who granted
this", and it is silently incomplete.** Windows' own security log still records
the group change, which is the reason this is **M** and not **S** — but the
whole point of having SD's own trail is not having to correlate the two.

Either add the two `K$AUDIT` calls, or **retire `add`/`delete` in favour of
`grant`/`revoke`**, which say what they mean and are what the documentation
teaches. *SD TCL - Accounts and Security* recommends `grant`/`revoke` and says
why meanwhile.

## 28. A process dump is written where every SD user can read it — **M**

`pdump.c:97` writes `sddump.`*n* into the directory named by `DUMPDIR`, or into
`sysseg->sysdir` when `DUMPDIR` is empty — which is how SD ships. Measured
27 Aug 2026: an ordinary account's `pdump` of its own session produced a
21,567-byte `C:\ProgramData\SD\sdsys\sddump.27`, and `icacls` on it reports
`GITORLI\sdusers:(I)(M)` — **every SD user has Modify on it.**

**The file holds application data**: `@`-variables, `@SENTENCE` and
`@COMMAND`, the call stack, open files and their locks, and named and unnamed
common. A dump taken to investigate a fault in one account is readable by every
other.

***THE EXISTING CONTROL GUARDS THE WRONG HALF.*** `PDUMP=1` in the
configuration stops an unelevated session **dumping** a process running under
another username. Nothing stops it **reading** a dump that is already there.

**Three things to decide**, none of them large: whether the installer should
set `DUMPDIR` to somewhere administrator-only; whether the dump should be
written with a restrictive ACL; and whether `sdsys` itself should stop being
`sdusers`-writable, which is a wider question than this entry. Raised while
writing *SD TCL - Processes and Phantoms*, which tells the reader to treat a
dump as the data of the program that produced it.

## 29. `micro` reports "Permission denied" on every save — **S** — ***DONE 27 Aug 2026***

> ***CLOSED ON THE INSTALL OF 19:37:47.*** The owner ran `micro bp ZZMARKS`
> **three times, with and without saving, and got no message at all.** The
> mechanism is witnessed rather than inferred: **`~/.micro/backups/` now
> exists** — that directory is created by the very write that failed under
> `Program Files`, and it had never appeared once in the defect's whole life.
> `bindings.json` and `buffers/history` were written beside it.
>
> ***AND THE MARK ROUND TRIP SURVIVED A REAL SAVE***, which is the last piece of
> START HERE item 5.3. After a save, SD reads the record back as **19 fields,
> 907 characters, VM 6 / SM 1 / TM 3, zero stray CR or LF, no field ending in
> CR** — content-identical to the fixture.
>
> ***ONE HARMLESS DIFFERENCE, MEASURED SO NOBODY CHASES IT.*** The record ON
> DISK grows by exactly one byte per line after a micro save (908 → 927 over 19
> lines): micro writes `dos` line endings, and its status bar says so. **SD's
> reader normalises them** — hence the clean read above — so this is the
> directory-file representation changing, not the data. It is item 7.16
> ("SD reads and writes CRLF, both halves") doing its job.
>
> ***IT TOOK THREE ATTEMPTS AND THE FIRST TWO ARE LEFT BELOW ON PURPOSE.*** Each
> failed for a different reason and each was reported as fixed before it was
> measured in the place it runs.

***THE FILE IS SAVED. THE MESSAGE IS FALSE, AND THAT IS THE DEFECT.*** Rewritten
27 Aug 2026 after measuring it four ways; **everything the first version of this
entry blamed was wrong**, and it is left described below because the wrong
diagnosis shipped a code change that does not fix anything.

Found by the owner running the one test only a person can run — `micro bp
ZZMARKS` from an unelevated console. micro drew correctly, the SD BASIC
highlighting worked, every mark token converted exactly as specified, and
**Ctrl-S** produced, in red, on the status line:

```
Permission denied. Save with sudo not supported on Windows
```

***AND THEN IT SAVED THE FILE ANYWAY.*** That is the whole shape of it: a user is
told their work was refused, in the wording of a permission failure, when it was
written. Nothing is lost. It is not a **B**.

***THE MEASUREMENT, 27 Aug 2026 — FOUR RUNS, ONE VARIABLE.*** All of them
unelevated as `don`, all editing the same file in a writable directory, **with
no SD involved at all** — `C:\Users\dmont\microtest\sample.sdbasic`, launched
straight from PowerShell. That is what makes the config home the subject rather
than anything about SD, `$hold`, or the working copy:

| | `MICRO_CONFIG_HOME` | flags | result |
|---|---|---|---|
| A | `C:\Program Files\SD\micro` (`Users:(I)(RX)`) | none | **error**, file saved |
| B | a writable directory | none | ***clean*** |
| C | `C:\Program Files\SD\micro` | `-backup off` | **error**, file saved |
| D | `C:\Program Files\SD\micro` | `-backup false -savehistory false` | **error**, file saved |

**B is the control and it is what makes the rest mean something**: same micro,
same file, same account, same minute — only the config home differs, and only B
is clean. **B also created `backups/`, `bindings.json` and `buffers/history`**
in its writable home, so micro really does write there.

***NO FLAG SUPPRESSES IT, WHICH IS WHAT DECIDES THE FIX.*** `backup` and
`savehistory` are both eliminated by C and D. `savecursor` and `saveundo` are
`false` by default (`micro -options`, installed 2.0.15), so `Serialize()` is not
it either. **The flag values are genuinely being parsed** — the control is
`micro -backup bogusvalue`, which answers `Invalid value` and stops, where
`-backup off` and `-backup false` are both accepted silently. So micro writes
something to its config home on save that no documented option turns off, and
**`MICRO_CONFIG_HOME` must be a directory the running account can write.**

> ***THE `-backup off` NOW IN `gpl.bp/EDIT` DOES NOT FIX THIS AND ITS COMMENT
> BLOCK IS WRONG.*** It was committed on the reasoning in the paragraph the
> table above replaces — that an empty `backupdir` sends the backup to
> `<config-home>/backups/` and that its `MkdirAll` is what aborts the save. The
> mechanism is real (B created `backups/`) but it is **not** what fails the
> save. `EDIT:227` and its twelve-line justification have to be reverted or
> rewritten in whatever cycle carries the real fix. **Do not leave the comment
> standing**: it tells the next reader the defect is closed.

***WHY 26 Aug's "BOTH EDITORS WORK" DID NOT CATCH IT.*** `don` is a member of
Windows `Administrators`, so an **elevated** session writes Program Files
without trouble; an unelevated one gets `Administrators` deny-only in its token
and falls back to `Users:(RX)`. The editors were tested from an elevated
session. **START HERE item 5.3 said "an unelevated console" precisely because
that is the case that had never been run**, and it was right to.

***THE FIX IS A WRITABLE CONFIG HOME, AND ITS SHAPE IS THE OWNER'S CALL.***
micro takes one `-config-dir` for both its read-only configuration and its
writable state, so they cannot be split. **The constraint that rules out the
obvious answer**: micro loads and executes Lua plugins from its config home, so
**one machine-wide writable directory would let any SD user drop code that runs
inside every other user's editor session, with that user's rights** — a
privilege escalation traded for a cosmetic message. ***DO NOT SIMPLY GRANT WRITE
ON `C:\Program Files\SD\micro`.***

**A PER-USER config home has no such problem** — a directory only its owner can
write is one where the only code they can run is their own. The Program Files
copy stays as the **read-only master** of `sdbasic.yaml` and `EDIT` copies it
into the per-user directory; see the owner's shape below.

***`edit` — Microsoft Edit — SETS NO `MICRO_CONFIG_HOME` AND IS NOT AFFECTED***,
but it has still not been retried unelevated, so do not read that as tested.

***TWO OF ITEM 5.3's OPEN QUESTIONS CLOSED AS A SIDE EFFECT, 27 Aug 2026.***
Measured on the install after the owner's real `micro bp ZZMARKS` session, not
reasoned: **`$hold` is empty** — so `EDIT` does clean its working copy up on
this path, which the history block claimed and nobody had watched — and
**`ZZMARKS` came back byte-identical**, 908 bytes, sha `1D65F19475F3CA5DCC5D594897F6B9CB`,
so the mark round trip survives a real editor session. `tools\probes\make-zzmarks.py`
rebuilds the fixture.

***THE OWNER'S SHAPE, 27 Aug 2026: A DIRECTORY UNDER THE USER'S HOME.*** His
suggestion when the four runs above were reported, and it is better than the
`%LOCALAPPDATA%` one it replaces for a reason worth writing down: **it is where
micro itself looks.** micro reads `$MICRO_CONFIG_HOME`, then
`$XDG_CONFIG_HOME/micro`, then `~/.config/micro`, so a home-directory config is
the native arrangement rather than something SD invents, and a user who already
knows micro finds their settings where they expect them.

***AND IT DISPOSES OF THE REASONING THAT PUT THE DIRECTORY IN PROGRAM FILES IN
THE FIRST PLACE.*** `EDIT`'s header and `stage.py:1123` both say the per-profile
routes are useless here because *"accounts SD creates cannot log in to Windows,
so a syntax file in a profile is one they could never be given"*. **That is only
true of a file nobody puts there.** `EDIT` copying `sdbasic.yaml` in at launch —
5,450 bytes from the Program Files master — gives the profile exactly what it
could not be given, and the master stays read-only and single-sourced. **Both
comments have to be corrected in the same commit as the fix; they are the reason
the next reader would undo it.**

**Both open questions are settled, one by ruling and one by design:**

1. ***`~/.micro`, not micro's own `~/.config/micro`*** — the owner's, and this
   host is the argument for it: `C:\Users\dmont\.config\micro` **already exists**
   with a personal `bindings.json` in it, made outside SD. Using micro's native
   path would mean SD writing `sdbasic.yaml` into a directory that is the user's
   own, and their personal settings silently changing SD's editor. `~/.micro` is
   SD's and collides with neither direction.
2. ***The ssh-profile question is no longer a gate.*** It was going to be:
   `C:\Users` holds `sdacctb48`, `sdsshb48` and eight more from the `b48` run,
   which looks like proof that SD accounts get profiles — but every one is an
   **empty stub** with no `NTUSER.DAT`, left by `delete.account`, so it proves
   nothing. **`micro-home.ps1` falls back to `%TEMP%\sd-micro` instead**, and
   both candidates are per-user and private, so the plugin question is answered
   whichever wins. Worth measuring on a live `sdu_` ssh session out of interest;
   nothing waits on it.

***AND A TRAP FOR WHOEVER IMPLEMENTS IT: THE PROFILE DIRECTORY IS NOT THE
ACCOUNT NAME.*** Measured on this host, 27 Aug 2026:

```
USERNAME    = don
USERPROFILE = C:\Users\dmont
```

**`C:\Users\` plus the login name is wrong here and would be wrong silently** —
it would create a second, unused directory and micro would still have nowhere
writable. Use `%USERPROFILE%`, which Windows resolves correctly, and never build
the path from `@logname` or `$env:USERNAME`. `micro-home.ps1` uses
`%USERPROFILE%`.

---

### ***IMPLEMENTED 27 Aug 2026 — UNCOMPILED IN THE SHIPPED TREE, AWAITING A CYCLE***

| | |
|---|---|
| **`gplbld/micro-home.ps1`** | **new, and it ships.** Resolves `%USERPROFILE%\.micro`, falls back to `%TEMP%\sd-micro`, **proves the directory writable by writing a probe file to it** rather than trusting `Test-Path`, copies `sdbasic.yaml` from the Program Files master and refreshes it when the master is newer, and prints one line: `MICROHOME=<path>`. Exit 1 with no such line when there is nowhere to write |
| **`sdsys/gpl.bp/EDIT`** | `-backup off` and its twelve-line justification **deleted**; `editor.args` gone. New `micro.home` subroutine runs the script and reads the `MICROHOME=` line, called **before the working copy is written**, beside the other two gates. The old `editor.cfg = kernel(K$WINPATH, '/micro')` is gone |
| **`gplbld/stage.py`** | ships `micro-home.ps1`; the `microcfg` comment rewritten — it is the **read-only master** now, and the claim that a profile "could never be given" the syntax file is corrected in place |
| **`sdsys/changelog`** | rewritten. The first version described the auto-backup mechanism and said the save failed; both were wrong |

***THE ANCHOR IS THE SUCCESS WORDING, PER THE STANDING RULE.*** `MICROHOME=` is
printed on one path only — after the directory has been proved writable **by
writing to it** — and every diagnostic line begins `micro-home:` instead, so
`EDIT` cannot match its own input or an error message. On failure `EDIT` prints
the script's own output, which names each candidate it tried.

***WHAT WAS MEASURED BEFORE HANDING IT OVER, AND WHAT WAS NOT.*** `micro-home.ps1`
was **parse-checked** (0 errors, 2 functions), byte-scanned (no BOM, LF), and
**run four ways as unelevated `don`**: first run created
`C:\Users\dmont\.micro\syntax\sdbasic.yaml`, sha-identical to the master; second
run said `already current`; with `USERPROFILE` pointed at a read-only directory
it fell through to `...\Temp\sd-micro`; with neither variable set it refused,
exit 1, no `MICROHOME=` line. **`gpl.bp/EDIT` was compiled** — a scratch copy in
`don`'s own BP with `$catalog` and `$internal` stripped, 967 lines, and the only
error is `Matrix KERNEL is not referenced in a DIM statement`, which is what
stripping `$internal` does to the four `kernel()` calls. **Not measured: the
whole thing running.** That needs the cycle.

> ***A FALSE GREEN WAS CAUGHT IN THE MIDDLE OF THAT AND IS WORTH THE LINE.*** The
> first compile was run against `C:\ProgramData\SD\sdsys\gpl.bp\EDIT` — the
> **installed** copy, which no cycle had touched — and it compiled with only the
> expected artefact. It was testing the code this entry replaces. The tell was
> in the evidence and not in the verdict: `micro.home:` did not appear in the
> file, and line 237 still read `kernel(K$WINPATH, '/micro')`. **Print what the
> instrument actually read, not just what it concluded.**

### ***AND IT STILL DID NOT WORK. TWO MORE DEFECTS, BOTH MEASURED 27 Aug 2026***

The owner ran `micro bp ZZMARKS` on the 18:58:55 install and the verb refused —
**quoting the helper's own SUCCESSFUL output underneath the refusal**, which is
what gave both faults away at once:

```
micro could not be given a configuration directory it can write to ...
micro-home: configuration home: C:\Users\dmont\.micro□micro-home: syntax file
already current□MICROHOME=C:\Users\dmont\.micro
```

***1. `EDIT` SPLIT THE CAPTURE ON THE WRONG SEPARATOR.*** `os.execute ...
capturing` returns **@fm-separated** lines each ending in **CR**, and **no LF at
all** — measured with a probe that counted characters rather than assuming:
two lines of output came back `FM=7 VM=0 CR=8 LF=0`, the bytes reading
`... 13 254 ...` between them. `micro.home` split on `char(10)`, so the whole
capture was one field and `MICROHOME=` was never seen. It now normalises `@fm`
and `CR` to one separator before scanning. *(`find.editor` gets away with the
same class of assumption only because its answer is a single line.)*

***2. AND THE HELPER ITSELF WAS READING ENVIRONMENT VARIABLES THAT DO NOT EXIST
THERE.*** The child SD launches gets no user environment block. Measured from
inside `os.execute`, which is the only place this script ever runs:

| | |
|---|---|
| `$env:USERPROFILE` | **empty** |
| `$env:TEMP` | **empty** |
| `$HOME` | **empty** |
| `[Environment]::GetFolderPath('UserProfile')` | `C:\Users\dmont` |
| `[Environment]::GetFolderPath('LocalApplicationData')` | `C:\Users\dmont\AppData\Local` |

So the first version refused **every time it was called the way it is actually
called**, and appeared to work only when run by hand from a console, where
those variables exist. ***That is exactly how it was tested — four ways, from a
console — and the environment was the one variable those four runs held
constant.*** It now asks the shell API and falls back to local application data,
then TEMP.

> ***`[System.IO.Path]::GetTempPath()` IS NOT A FALLBACK, IT IS A TRAP.*** With
> TMP and TEMP both unset it answers **`C:\WINDOWS\`** — measured. Unelevated
> that fails; **elevated it would quietly create `C:\WINDOWS\sd-micro`**, a
> configuration home ordinary users cannot write and administrators share, which
> is both of the things this entry exists to avoid. The script refuses any
> candidate under the Windows directory.

***MEASURED END TO END THIS TIME, IN THE ENVIRONMENT THAT MATTERS.*** A scratch
program in `don`'s own BP ran the rewritten helper through `os.execute` and
applied `micro.home`'s parse verbatim:

```
RAW.LEN=215 FM=3 CR=4 LF=0
  | micro-home: candidates: C:\Users\dmont\.micro | C:\Users\dmont\AppData\Local\SD\micro
  | micro-home: configuration home: C:\Users\dmont\.micro
  | MICROHOME=C:\Users\dmont\.micro
PARSED=[C:\Users\dmont\.micro]
PASS - MICROHOME= parsed from the real capture
```

**Cycled and installed 27 Aug 19:37:47**, and that is the install the closure at
the top of this entry was measured on.

***AND THE FIXTURE DOES NOT SURVIVE A CYCLE — KEEP THIS, IT WILL RECUR.***
`cycle.ps1` deletes both trees, so `don`'s BP — `ZZMARKS` included — goes with
it, and `EDIT` will happily open a record that does not exist. **One test run
was wasted editing an empty new record before anyone noticed.** Rebuild it after
every cycle with `tools\probes\make-zzmarks.py` in the docs repository; sha
`1D65F19475F3CA5DCC5D594897F6B9CB`, 908 bytes.

***WHAT IS ALREADY THERE, WHICH ARGUES FOR THE OWNER'S `.micro` OVER micro's OWN
PATH.*** `C:\Users\dmont\.config\micro` **already exists** on this host with
`bindings.json` and `buffers/` in it — a personal micro configuration, made
outside SD. Using micro's native `~/.config/micro` would mean SD writing
`sdbasic.yaml` into a directory that is the user's own, and the user's personal
settings silently changing how SD's editor behaves. **`~/.micro` is SD's,
collides with neither, and that is the case for it.**

**Whatever is chosen, `EDIT:227`'s `-backup off` and its comment block go in the
same edit** — see the blockquote above.

---

## 30. `verify-osusers.ps1` refuses on a fresh install — **S** (verifier, not product)

Found 27 Aug 2026 running `-Run b48` against the 17:25:59 install — the first
suite run since PRE_RELEASE 2 (previous session) shipped. `verify-osusers`
stopped at its step-0 precondition:

```
[FAIL] record present before the test: expected (none), got yes
verify-osusers: refusing - don is ALREADY on the list.
```

**The product is behaving correctly.** PRE_RELEASE 2 gave `CREATEA` /
`adopt-account` a `grant.os.access` step that writes an `os.users` record
(`yes`,`yes`) for every ADMINISTRATOR-tier account as it is created. The account
the installer adopts is always ADMINISTRATOR, so `adopt-account.log` shows
*"os.users: don has SH yes, OS.EXECUTE yes"* and `C:\ProgramData\SD\sdsys\os.users\don`
is present from first boot. That is the documented, intended design (changelog,
27 Aug: *"IT APPLIES TO THE ACCOUNT THE INSTALLER MAKES FOR YOU"*).

**The verifier predates it.** `verify-osusers` measures the OS.USERS *admit
path* — put `@LOGNAME` on the list, watch a shell appear; take it off, watch it
go — and needs `@LOGNAME` **absent** at the start. Its guard refused a
pre-existing record because, when it was written, one could only be a person's
manual grant that the test must not destroy. The previous session closed
PRE_RELEASE 2 without updating this verifier.

***FIXED 27 Aug 2026 — the verifier now parks and restores.*** When step 0 finds
`@LOGNAME` already listed it copies the record's bytes to a save file, has a new
elevated `Unlist` phase remove it for the baseline, runs the whole transition,
and the `Revoke` phase writes the saved bytes back — so the tree is left exactly
as found, automatic record included. One extra UAC prompt (three, not two) in
that case. `Restore-SavedRecord` and the `finally` that wraps step 0a onward
guarantee the record goes back even on an early `Stop-Here` (`exit` inside
`try` still runs `finally` in PS 5.1 — measured). Parse-checked: 0 errors,
16 functions. **Not yet run** — needs an unelevated console and the three
prompts; it is on `assert-current`'s `$neverShipped`, so no cycle.

**Sibling risk, not chased here:** other verifiers may carry the same "starts
unlisted / starts empty" assumption about `os.users`. `verify-createaccount`
and the tier verifiers touch account creation; worth a sweep when `b48` next
runs clean.

**Update 27 Aug, standalone run:** the fixed verifier **PASSED** — every one of
22 checks, including `baseline: the automatic record is now gone` and
`the parked record was restored`. `os.users\don` came back byte- and
mtime-identical (`yes\nyes\n`, 10 bytes, 17:26). The remaining `b48` question is
PRE_RELEASE 31, below.

---

## 31. An elevated local session keeps OS.EXECUTE after LOGTO — **B?** (owner's call)

Found 27 Aug 2026 by `-Run b48 -ContinueOnFailure` (the run that skipped past
the then-unfixed `verify-osusers`). Elevated half: **18 of 19**, the one failure
`verify-apiadmin`:

```
[FAIL] control: local elevated session refused OS.EXECUTE: expected False, got True
```

***THE HEADLINE FINDING DID NOT FIRE — that part is good.*** `verify-apiadmin`
exists to catch a **remote API session** running `OS.EXECUTE`. This run:
`API session was refused OS.EXECUTE by name` **PASS**, `API session CANNOT run
OS.EXECUTE` **PASS**. The API hole is closed.

***WHAT FAILED IS THE CONTROL.*** The verifier creates a PROGRAMMER account
(`CREATE.ACCOUNT USER ... PROGRAMMER NONE`, so **no** automatic `os.users`
record), then from a **local elevated** PowerShell session does `LOGTO
<acct>` and runs an `OS.EXECUTE` probe. Its comment (written ~21 Aug):

> a LOCAL ELEVATED session ... starts in SDSYS with USR_ADMIN set and gives the
> flag up on the way out (CPROC, "administrator rights belong to SDSYS"), so by
> the time it reaches the probe `os_permitted()` says no.

**It did not say no.** `PROBE.OSEXEC.TRIED=YES` then `PROBE.WHOAMI=gitorli_don`
— `OS.EXECUTE` ran and returned the identity, so `$localRanOsExec` is true where
the control expects false.

***TRACED, AND IT IS A PRE_RELEASE 2 INTERACTION — LIKELY A STALE CONTROL, BUT
THE OWNER SHOULD CONFIRM.*** `os_permitted()` (`op_sh.c:150`):

```c
  if (my_uptr->flags & USR_ADMIN) return TRUE;          /* line 161 */
  ...
  snprintf(path, ..., "os.users%c%s", DS, process.username);  /* line 167 */
  ...  return (stricmp(field2, "yes") == 0);
```

`CPROC:2713` **does** clear `USR_ADMIN` on `LOGTO` away from SDSYS
(`kernel(K$ADMINISTRATOR,0)` → `op_kernel.c:416` `my_uptr->flags &= ~USR_ADMIN`),
and the `elevate('STOP')` beside it releases the OS token — that half works. But
`os_permitted()` then falls through to the list, keyed on **`process.username`**
— the Windows login, `don`, which `LOGTO` never changes. **PRE_RELEASE 2 put
`don` in `os.users`.** So the gate now says yes on the *person*, exactly as its
own changelog intends: *"the name is the WINDOWS login name ... the permission
belongs to the person and does not change when they LOGTO somewhere else."* The
API session is refused only because its `process.username` is the account
(`sdapiab48`), which is not listed.

So the product is doing what PRE_RELEASE 2 designed. **The control in
`verify-apiadmin` (written ~21 Aug, before `don` had an `os.users` record)
is stale** — same class as PRE_RELEASE 30. **Left for the owner** because it is
the verifier's *only* contrast and rewriting it means deciding what the test now
proves: probably "a session whose `process.username` is not listed is refused,
elevated-then-LOGTO'd or not", with a non-`don` Windows identity or an
unlisted-account probe. The API-side behaviour (refused) is not in question and
the headline hole stays closed.

**Left behind by that run** (normal — the next `cycle.ps1` clears them): the
`b48` verifier accounts `sdacctb48`, `sdtiertb48*`, `sdrtb48*`, `sdtapib48*` and
three `os.users` records for the ADMINISTRATOR-tier ones the tier verifiers make.

---

## 32. `delete.account` leaves the ProfileList entry, so a recreated account gets a different home — **S**

Found 27 Aug 2026 by the `b48` suite failing two rows that had passed in every
run since 26 Aug, and traced rather than guessed.

***THE SYMPTOM WAS ssh KEY AUTHENTICATION.*** `verify-sshonly` reported

```
[FAIL] control:  ssh with a key: expected admitted, got refused: Permission denied (publickey,...)
[FAIL] ssh-only: ssh with a key: expected admitted, got refused: Permission denied (publickey,...)
```

Both rows are **non-decisive**, so the step still exited 0 and the verifier
still printed *"12 of 12 decisive checks passed"* — which is why this needed the
`[FAIL]` count to surface at all. **The same two rows passed in the four
previous runs** (`20260826-145346`, `171706`, `212033`, `20260827-173821`) and
failed only in `20260827-190248`.

***THE CHAIN, MEASURED.***

| | |
|---|---|
| `delete.account` deletes the Windows user | but prints *"Warning: the Windows profile for `<name>` was left behind"* — and leaves the **`ProfileList` registry entry** with it |
| an account of the same name is created again | it gets a **new SID** |
| Windows finds the old `ProfileList` entry pointing at `C:\Users\<name>` under a dead SID | so it makes a **second** profile: `C:\Users\<name>.<DOMAIN>` |
| anything holding the old path is now wrong | here, `authorized_keys` — sshd looks under the profile Windows assigns and the key is under the other one |

**On this host:** `C:\Users\sdsshb48` *and* `C:\Users\sdsshb48.GITORLI`, plus
`.000` variants for eight more; **53 stale `sd*` `ProfileList` entries** for
accounts `Get-LocalUser` says do not exist, going back to `b44`.

***IT IS A USER-FACING DEFECT AND NOT ONLY TEST LITTER.*** An administrator who
deletes an SD account and recreates it under the same name — a completely
ordinary thing to do — silently gets a different home directory, and that
account's ssh keys stop working with a message that says nothing about why.

**The fix is `DELACC` removing the `ProfileList` entry when it removes the
Windows user**, in the same branch that already deletes the profile directory
and warns when it cannot. The warning text is the place to say so if the
registry entry cannot be removed either.

***AND IT IS WHY THE `b48` RUN HAD THESE TWO FAILURES AT ALL: THE `-Run` PREFIX
WAS SPENT TWICE.*** `b48` was used by the `-ContinueOnFailure` run at 17:36 and
again at 19:01. The rule *"a `-Run` prefix is spent once"* is in START HERE for
exactly this, and the second run is what created the duplicate profiles. **That
was a mistake in the instructions given to the owner, not by him.** The suite
verdict stands — both rows are non-decisive and the failure is environmental —
but the next run needs `b49`, and `cleanup-devlitter.ps1` should clear the 53
entries first.

***FIXED 27 Aug 2026 — WRITTEN AND CHECKED, NOT YET COMPILED.*** `DELETE_USER`
now names the `ProfileList` key from the SID it already holds, reads
`ProfileImagePath` **before** anything is removed (it is the only record of
where the directory is), and removes the key **in its own right after** the
`Remove-CimInstance` call rather than instead of it.

***THE FIX IS ONE WORD, AND IT IS THE `exit` THAT IS GONE.*** The old catch
read `catch { exit 6 }`, so a failed CIM removal ended the script and **left
both halves**. It is `catch { }` now, and the registry entry is dealt with
below it either way. `Remove-CimInstance` is still tried first and is still the
right tool; its failure no longer decides anything.

**Status 6 splits into 6 and 7**, saying which half could not be removed:

| | |
|---|---|
| **6** | the profile **directory** is left |
| **7** | the **`ProfileList` entry** is left |

***THIS TABLE FIRST SAID 6 WAS HARMLESS — "costs disk, the registry entry went,
so a recreated account still gets its proper home". THAT IS MEASURED FALSE; SEE
ENTRY 35.*** Either half pushes the next account of the same name to a suffixed
home.

**Both halves are tested for after the attempt, not inferred from which call
threw** — a thrown `Remove-CimInstance` does not say what it removed first.
`DELACC` gains a `case stat = 7`; message `10075` is reworded to mean the
directory only and **`10116` is new** for the registry case, naming the
consequence and how to clear it.

***WHAT IS MEASURED AND WHAT IS NOT.*** The generated PowerShell was rebuilt
from the BASIC source and parse-checked: **0 errors, 203 tokens** (not a
zero-token pass), no embedded BOM, and the two genuinely new steps were run
read-only against a real account — `Join-Path` produced the right key, the key
exists, and `ProfileImagePath` read back `C:\Users\dmont` for `don`.
***THE BASIC IS UNCOMPILED*** and `cycle.ps1` is what compiles it.

***AND `messages.c:335` WAS READ BEFORE THE MESSAGE WAS WRITTEN.*** Only `\n`
and `\t` are expanded and there is no default branch, so a literal
`C:\Users\%1` in message text survives intact — but `C:\temp` would not, and
that is worth knowing before writing the next one.

## 33. `allow-ssh-groups.ps1`'s own usage text omits the switch it requires — **S**

Found 27 Aug 2026 while writing *Technical - The Installed Scripts*, by reading
the `param` block instead of the header comment.

The script ships in `C:\Program Files\SD` and its header offers three forms:

```
powershell -File allow-ssh-groups.ps1            write the block and restart sshd
powershell -File allow-ssh-groups.ps1 -Check     print what it would write, touch nothing
powershell -File allow-ssh-groups.ps1 -Remove    take SD's block back out
```

***THE FIRST ONE DOES NOT WRITE ANYTHING.*** `allow-ssh-groups.ps1:248` tests
`-not $Installed` and exits **2** with *"-Installed not given - this rewrites
sshd_config and restarts sshd, so it has to be asked for"*. `-Check` and
`-Remove` return before that test, so **only the documented form that matters
is wrong.**

The switch is right and the guard is right — `-Installed` means *an
administrator asked for this*, and the script is otherwise able to rewrite
`sshd_config` merely by being run. **It is the usage text that is stale**: the
line predates the 21 Aug 2026 change of what `-Installed` asserts, recorded in
the script's own "WHEN IT REFUSES" note fifteen lines below it.

***FIXED 27 Aug 2026, SAME DAY.*** The first usage line now reads
`powershell -File allow-ssh-groups.ps1 -Installed`, with a dated note under the
exit codes saying which forms need the switch and which return before the test.
**Nothing in the code changed**, and the file still parses — **0 errors, 1247
tokens**. It rides PRE_RELEASE 32's cycle; it is a comment, so nothing waits on
that.

*Technical/02* already documents the correct form, so a reader of the
documentation was never caught by this. A reader of the script was.

## 34. `release.ps1` cannot complete on the `Technical` set — **S** (docs toolchain)

Found 27 Aug 2026 by adding the second `Technical` page and running the
documented release command against it.

`tools\release.ps1 -Set Technical` renders both pages, passes its own staleness
gate, and then **exits 1**:

```
checklinks: 2 rendered page(s) read
checklinks: 0 link(s) checked, 0 broken
checklinks: no links found at all - that cannot be right
```

***THE GUARD IS CORRECT AND IS THE INSTRUMENT RULE WORKING.*** A link checker
that passes because it checked nothing is exactly the failure `checklinks.py`
refuses. The record already predicted this — *"`checklinks` on `Technical`
refuses today and is right to; run it there once there is a second page"* — but
**the prediction assumed a second page would bring cross-references, and it has
not.** There is no honest link between restricted BASIC commands and the
Windows installer scripts, and writing one to satisfy a tool would put a false
sentence in a document to make a check go green.

**So a whole set has no working release command**, and the two hand steps in
the docs `README` are the only route. That is the thing to decide, and it is
the owner's: either `checklinks.py` grows a way to say *this set legitimately
has no links* and `release.ps1` passes it, or `release.ps1` treats a
zero-link set as a pass in its own right and says so out loud in its output.
**Do not settle it by adding a link.**

Until then, `Technical` renders with:

```
python tools\mkdoc.py --in Technical\markdown --out Technical\html --product "SD Core for Windows" --version W1.0-0
powershell -File tools\mkpdf.ps1 -In Technical\html -Out Technical\pdf
```

and the `README`'s markdown-against-PDF loop is what proves nothing is stale.

## 35. A profile DIRECTORY left behind moves the next account's home, exactly as the registry entry does — **S**

Found 27 Aug 2026 **by running the regression test for entry 32 on the install
that fixed it**, which is the only reason it was found at all: the registry
half was measured working and the symptom happened anyway.

***THE TEST, AND IT IS WORTH KEEPING.*** `create.account user b49home
programmer ssh`, then `ssh b49home@localhost` **once** — a brand new Windows
account has no profile until it signs in, so without that step there is nothing
to leave behind and the test proves nothing — then `delete.account b49home`,
then create and sign in again.

***WHAT WAS MEASURED AFTERWARDS.***

| | |
|---|---|
| old SID `…-2740`, `ProfileList` entry | **gone** — entry 32's fix worked |
| `C:\Users\b49home` | **still there**, empty to an ordinary reader, ACL still naming the dead SID |
| new SID `…-2742`, live account `b49home` | profile at **`C:\Users\b49home.GITORLI`** |

**Exactly one `ProfileList` entry mentions the name**, and it is the live one.
So the suffix was not caused by a stale registry entry this time. ***Windows
will not put a new profile where a directory already sits either***, and it
takes the same way out — a suffixed home — with the same consequence: anything
keyed to the old path, `authorized_keys` included, is not found.

***SO "REMOVE THE ProfileList ENTRY" WAS HALF A FIX, AND THE COMMENT THAT
CALLED STATUS 6 HARMLESS WAS WRONG WHEN IT WAS WRITTEN.*** It reasoned from
what the registry entry does rather than from what Windows does with an
occupied path, and it went into the code, the message text and the changelog
before anything ran.

**Fixed the same day**: `DELETE_USER` now removes the **directory** in its own
right as well, after the registry key, in the same shape — try it, then test
for it, and report which half survived. `Remove-CimInstance` remains the first
attempt and still does the bookkeeping when it works. **Message `10075` is
rewritten**: it said the directory "was left behind" and implied that was
tidiness; it now says a later account of the same name will not get that
directory back until it is deleted.

***UNCOMPILED — IT NEEDS THE NEXT CYCLE.*** The regenerated PowerShell parses,
**0 errors and 233 tokens** against 203 before the change.

***WHY `Remove-CimInstance` FAILED IS NOT ESTABLISHED*** and the fix does not
depend on it — the hive was not loaded by the time it was checked, so the
likely cause is that it still was when `delete.account` ran, moments after an
ssh session. **If the directory removal fails too, status 6 still fires and now
says something true.**

***MEASURED TO THE END, 27 Aug 2026, AND THE DIRECTORY HALF CANNOT BE FIXED AT
DELETE TIME.*** The `Remove-Item` added above failed on the very next run, and
the four experiments that followed say why:

| what was tried, elevated | answer |
|---|---|
| `Remove-Item -Recurse -Force` | `IOException` — ***`UsrClass.dat` is being used by another process*** |
| `Get-Acl` on the directory | owner is `BUILTIN\Administrators`, so it is **not** a permissions problem |
| `reg unload` of the SID's two hives | **`ERROR: Access is denied`**, elevated |
| `Rename-Item` to move the path aside | **`Access to the path is denied`** |

***THE PATH CANNOT BE FREED AT ALL WHILE THE HIVE IS MOUNTED*** — not deleted,
not even renamed. **And no process owns the orphaned SIDs**: a `Win32_Process`
sweep for processes whose owner has no local account returned **nothing**, so
this is not a lingering ssh session. The holder is something running as SYSTEM.

***THE RECORD ALREADY SAID THIS AND IT WAS NOT READ.*** PROJECT_STATUS's
`cleanup-devlitter.ps1` line: *"Needs a REBOOT between the accounts and the
profiles — a loaded hive cannot be removed, and after a suite run every hive is
loaded."* Four exchanges went on rediscovering it.

**So the code stays as it is and the shape is right:** the `Remove-Item`
attempt succeeds for an account that never signed in (no hive was ever
mounted), fails harmlessly otherwise, and **message `10075` now names the
cause, says a restart is what releases it, and says what happens if it is left**.
That is the honest product answer. **The cure is entry 36.**

## 36. Deleted accounts leave their registry hives mounted, and nothing SD does can unmount them — **M** (owner's call)

***RULED 27 Aug 2026 BY THE OWNER. ALL THREE DECISIONS BELOW ARE ANSWERED AND
NONE IS BUILT.*** The evidence that follows is unchanged; this block is what to
implement against.

| decision | ruling |
|---|---|
| what `DELETE_USER` leaves on failure | ***Keep BOTH halves, and record the SID as SD's to reclaim.*** Try the DIRECTORY first; remove the `ProfileList` entry only if that succeeded. The pair stays consistent and the profile stays visible to `Win32_UserProfile` |
| who reclaims it | ***SD's OWN sweep at service start*** — not the Windows per-days policy. `sdsvc.exe` runs as LocalSystem at every boot (`gplbld/install-service.ps1:33`), by which time the previous boot's hives are down. It takes **both** halves together |
| `create.account` on an existing `C:\Users\<name>` | ***REFUSE.*** Name the directory and say what has to happen. It cannot clear the path itself — the hive is still up |
| a restart in the delete path | ***No.*** Unchanged; the reclaim rides the next boot that happens anyway |

***WHY NOT THE BUILT-IN "DELETE PROFILES OLDER THAN N DAYS ON RESTART" POLICY***,
which was the owner's first instinct and was argued down on three counts:

1. **It is machine-wide and not scoped to SD.** It would age off the customer's
   own admins and service accounts too. SD would be changing a system policy on
   someone else's server to clean up after itself — the opposite of how
   `deny-logon.ps1` and `allow-ssh-groups.ps1` were built.
2. **Its granularity is days, so it does not cure the symptom.** The symptom is
   that the next same-name account gets a suffixed home, and that recurs on any
   recreate inside the age window. It cures the accumulation only.
3. ***AND IT AGES PROFILES OFF THE RECORDED UNLOAD TIME, WHICH IS EXACTLY WHERE
   OUR CASE IS WEAKEST.*** The profiles wanted swept are the ones whose hives
   never unloaded cleanly. **Whether they carry a usable timestamp at all is
   UNMEASURED** and would have to be tested before the policy could be trusted.
   *(Documented Windows behaviour, not measured here.)*

***AND THE TWO OBVIOUS ANSWERS CANCEL OUT UNLESS THE SWEEP TAKES BOTH HALVES.***
"Keep both halves" leaves the `ProfileList` entry so a sweep can find the
profile; a boot-time *file* deletion then removes the directory and leaves that
entry pointing at nothing — inconsistent in the other direction, and
`Win32_UserProfile` reports a profile with no folder as *"Account unknown"*.
**This is why `PendingFileRenameOperations` is not the mechanism**: it deletes
files and cannot touch the registry.

***THE "SERVERS NEVER REBOOT" OBJECTION IS WEAKER THAN IT LOOKS.*** Owner, 27
Aug 2026, from managing Windows servers: *"I always restarted Windows servers
once a week to avoid Windows crud buildup."* On a server run that way the sweep
reclaims within a week rather than never — which is what makes a boot-time
reclaim a real cure and not a theoretical one.

***AND THIS RE-OPENS PART OF 32, DELIBERATELY.*** Keeping the `ProfileList`
entry on failure is the state 32 was filed against. The entry is the only handle
a sweep has, so it is the right trade — but **message `10075` needs rewriting a
third time**, the changelog with it, and **32's regression test re-scoped** from
*"the entry is gone"* to *"the entry is gone when the directory went"*.

Found 27 Aug 2026 while measuring 35. ***TWENTY-TWO ORPHANED SIDs — FORTY-FOUR
HIVES — WERE LOADED ON THIS HOST***, every one for an account `Get-LocalUser`
says does not exist, going back weeks. `2740` in that list is a `b49home` from
an hour earlier.

***THIS IS THE ROOT CAUSE OF 32 AND 35, NOT A SIDE ISSUE.*** A mounted hive is
why `Remove-CimInstance` failed in the first place, which is why **both** halves
of the profile survived, which is the defect 32 described. Removing the registry
entry (32) works because that half needs no file unlocked. The directory (35)
needs the hive down, and only a restart puts it down.

***AND IT PROBABLY EXPLAINS THE 53 STALE `ProfileList` ENTRIES.***
`clean-test-profiles.ps1` sweeps with `Remove-CimInstance` — the same call that
fails on a mounted hive. The sweep may have been failing on every locked profile
rather than never having been run.

***AND A REBOOT CLEANS NOTHING — IT ONLY MAKES THE DIRECTORY DELETABLE.***
Asked by the owner, 27 Aug 2026: *"for a server in normal use, every time it is
rebooted does it clean the directories left behind, or do they sit there
forever?"* **They sit there forever.** Unmounting the hive removes the lock and
that is all; no SD component and nothing in Windows returns for the directory.

***THIRD DECISION, AND IT POINTS THE OPPOSITE WAY FROM WHAT WAS BUILT.***
Removing the `ProfileList` entry — entry 32's fix — **is what every cleanup tool
uses to find the profile**:

| | |
|---|---|
| `Win32_UserProfile` | enumerates from `ProfileList`. No entry, no object |
| `clean-test-profiles.ps1` | sweeps with `Remove-CimInstance`, so it inherits that blindness — the 53 it cleared all still had entries |
| Windows' *"delete profiles older than N days on restart"* policy | operates on profiles, not on folders |

**So the state `delete.account` now leaves on failure is harder to clean up
than the state it used to leave** — an anonymous folder under `C:\Users` that
nothing tracks. It is **not worse for the symptom**, because either half causes
a suffixed home on its own, but it removes the only handle a later sweep had.

***THE OPTION IS TO KEEP BOTH HALVES WHEN THE DIRECTORY CANNOT GO.*** If the
removal fails, leave the registry entry too: the pair stays consistent, the
profile remains visible to `Win32_UserProfile` and to the sweep, and a later
run — or a reboot-time policy — can clear both. **The cost is that the account
name stays blocked either way, which it already is.** *(Reasoned, not measured.
It also argues for removing the directory FIRST and the entry only on success,
which is the reverse of the current order.)*

**Two more things to decide, and neither is mine:**

1. ***Should `create.account` look before it leaps?*** At creation the name is
   known and `C:\Users\<name>` can be tested for. Today a leftover directory
   silently produces a suffixed home; **refusing, or saying plainly what will
   happen, converts a silent wrong answer into an explained one.** It cannot
   delete the directory either — the hive is still up — but it can stop the
   user being surprised.
2. ***Is a restart acceptable in the delete path?*** Almost certainly not, and
   that is why this is written down rather than built.

**Nothing here is a regression**; it is how Windows has always behaved and how
this project has always run. It became visible because 32's fix removed the
half that was masking it.

***MEASURED AFTER A RESTART, 27 Aug 2026 — THE SWEEP CLEARED ALL 53.***
`cleanup-devlitter.ps1` on a freshly rebooted machine: **`removed 53, failed 0`,
profiles matching `53 -> 0`**, users and groups already at 0, `sdout` untouched.

**A prediction was written before the run and it held**: the **20** names still
on disk as directories were all in the list — `sdacctb48` and its `.GITORLI`,
the five `.000` pairs, the three `sdtapib48*` pairs — and **nothing outside the
pattern appeared**: not `b49home`, `b50home`, `dmont`, `Default` or `Public`.
The other **33** were `b44`, `b46`, `b47` and three of `b45`: **registry entries
whose directories were already gone.** 20 + 33 = 53.

***AND THERE IS A CONTROLLED BEFORE-AND-AFTER, ON ONE OBJECT.***
`C:\Users\b50home` refused **both** `Remove-Item` (`IOException`,
`UsrClass.dat` in use) **and** `Rename-Item` (`Access denied`) before the
restart; **the identical `Remove-Item` removed it silently afterwards.** Same
path, same command, nothing between them but the reboot. ***That is the
mechanism proven, not merely consistent.***

*(This paragraph first said no controlled before-and-after existed. That was
written thinking of the 53-profile sweep, and it overlooked the one object that
had been measured failing by hand an hour earlier.)*

**The 53-profile sweep is corroboration rather than proof**: no failing sweep
run is on record, only the accumulation, so it is consistent with the cause
rather than a watched repair. The `b50home` pair is what carries the claim.

***OBSERVED IN THE WILD 28 Aug 2026, AND THE UNTRACKABLE STATE IS REAL.*** A
read-back after a `verify-tiers` run, on the 27 Aug 22:52:21 install:

| | |
|---|---|
| `C:\Users` | **11 non-standard directories**, not the three the 69th-session handoff claims. That claim was true at the sweep; the `b49` suite refilled it |
| of those | **10 are orphans** — `Get-LocalUser` says the account is gone. Only `b48adm` is live |
| loaded hives | **11 SIDs, 22 hives** (`…2750, 2753, 2780, 2781, 2783, 2785, 2787, 2789, 2791, 2793, 2795`). ***The reboot's repair lasted one suite run*** |
| ***`sdapiab49`, `sdapiidb49`, `sdapinb49`*** | ***directory present, NO `ProfileList` entry.*** `Win32_UserProfile` cannot enumerate them, so `clean-test-profiles.ps1` cannot either |

***THOSE THREE ARE THE UNTRACKABLE STATE THIS ENTRY ARGUED ABOUT, MEASURED
RATHER THAN REASONED.*** The ruling above chose "keep both halves" on the
argument that removing the entry destroys the only handle a sweep has. **Three
folders on this machine are now in exactly that condition** and nothing on the
box can find them by profile.

*(NOT ASSERTED: that 32's fix produced them. It landed at 21:58:17 and the
suite ran after, so the timeline fits a `DELETE_USER` whose registry half
succeeded and directory half failed — but the delete transcripts were not read,
and consistent-with is not measured.)*

**A note on the instrument:** enumerating `HKEY_USERS` unelevated **fails per
key**, and the failed enumeration still returns a count — `1` — which is a
confident wrong answer of the kind this project keeps paying for. The 22 above
were read from the names in the access-denied errors, not from that count.

***PREDICTION WRITTEN BEFORE THE 28 Aug REBOOT AND SWEEP, so the run is a test
rather than an observation.*** `clean-test-profiles.ps1:223` enumerates
`Get-CimInstance Win32_UserProfile`, which reads from `ProfileList`:

| | expected |
|---|---|
| the **7** orphans WITH an entry — `sdacctb49`, `sdapib49`, `sdscramb49`, `sdsshb49`, `sdtapib491/2/3` | **removed** |
| ***`sdapiab49`, `sdapiidb49`, `sdapinb49`*** | ***SURVIVE.*** No entry, so the sweep never enumerates them. **They must then be deleted by hand, which is the cost of the untrackable state in one sentence** |
| `b48adm` | **untouched** — its Windows account is live, and the sweep refuses a profile whose SID still has one |

The reported count may exceed 7: `ProfileList` entries outlive their
directories, and 33 of the 53 cleared on 27 Aug were exactly that.

***THE PREDICTION HELD ON EVERY ROW, 28 Aug 2026.*** Reboot, then
`cleanup-devlitter.ps1` elevated: **`removed 7, failed 0`**, and the seven
named are the seven predicted. `b48adm` untouched. ***And `sdapiab49`,
`sdapiidb49` and `sdapinb49` are still on disk***, read back independently
after the run.

**So the untrackable state is demonstrated end to end**: created by a delete,
invisible to the tool built to clean it, removable only by hand. That is the
cost of removing the `ProfileList` entry when the directory cannot go, and it
is what the ruling above avoids. ***The boot sweep specified in the ruling must
enumerate the DIRECTORY, not `ProfileList`, or it inherits this exact hole*** —
see PRE_RELEASE 41.

***THE OPERATIONAL RULE IS THEREFORE UNCHANGED AND NOW HAS ITS REASON:*** the
reboot in the middle of `cleanup-devlitter.ps1` is not about the accounts pass
at all. **It is what makes the profile pass possible**, and running the sweep
without it is what leaves work behind.

## 37. `create.account` says "may sign in over ssh" twice, about two different things — **S**

Seen 27 Aug 2026 in the transcript of a routine `create.account user b49test
programmer ssh`. Two consecutive lines:

```
b49test may sign in over ssh only
b49test may sign in over ssh, and may not use the API
```

***THEY ARE ABOUT DIFFERENT GATES AND THE WORDING HIDES IT.***

| | |
|---|---|
| `CREATEA:808` → `10034` | **Windows logon rights.** The console and Remote Desktop are denied, so ssh is the only way *in to the machine* |
| `CREATEA:1612` → `10076` | **SD's route keywords.** Of SD's two remote routes the account has ssh and not the API |

**Both are worth saying** — they are the two halves of the access model the
project has been careful to keep separate, and `PROJECT_STATUS` calls them two
gates in as many words. **But a reader sees one fact stated twice**, and the
natural conclusion is that the second line is a stutter rather than a different
subject.

***AND WITH `both` IT IS NOT A REPETITION, IT IS A FLAT CONTRADICTION.***
Measured the same evening, `create.account user b48adm programmer both`:

```
b48adm may sign in over ssh only
b48adm may sign in over ssh and use the API
```

`10034` says **only** ssh; `10078` then says ssh **and** the API. Both are true
of their own gate and they cannot both be true of the same one, so a reader has
no way to tell that two subjects are in play rather than one bug. **This is the
example to fix against** — the `ssh`-keyword case merely looks redundant, and
this one looks broken.

**The fix is wording, not logic.** Name the subject in each: something like
*"may reach this computer only over ssh"* for the logon right and *"SD routes:
ssh, not the API"* for the keyword. Nothing in `CREATEA` changes.

**Not upstream's** — both messages and both gates are Windows-port work.

## 38. The suite does not test SUSPENDED on any door — **M** (verifier gap, not product)

Found 27 Aug 2026 after items 5.1 and 5.2 were taken by hand on the 22:52:21
install. **Neither `verify-tiers.ps1` nor `verify-tierapi.ps1` contains the
word `suspend`**, so a suite run exercises none of the three doors the
SUSPENDED tier closes.

***THE PRODUCT IS FINE — ALL THREE DOORS EXIST AND TWO ARE NOW MEASURED.***

| door | where | state |
|---|---|---|
| `LOGIN` — ssh and console | `LOGIN` | ***measured 27 Aug***: banner shown, then `Account B48ADM is suspended`, then admitted again after restore |
| `logto` | `CPROC:3708` `logto.authorised` | measured earlier: `Account B48SUSP is suspended` |
| API | `APISRVR:507` | ***measured 28 Aug 2026 by the controlled pair*** — `sddr2a` connected (`ok connected to account SDDR2A`), was suspended, and the same call was then refused. Nothing in the refusal names the cause, by design; **the pair is what proves it** |

***THE API DOOR CANNOT BE TESTED BY ITS WORDING, AND THAT IS BY DESIGN.*** It
refuses with `sysmsg(10003)` — **the same text as "no such account" and "not
granted"** — so a caller cannot tell which of the three applied and the API does
not enumerate the register's state for an attacker. **A check that anchors on
the message would therefore be a false positive**, matching a refusal that had
nothing to do with suspension. ***The only valid shape is a controlled pair on
one account***: connect while unsuspended and succeed, suspend, connect again
and fail, restore. Either half alone proves nothing — a refusal that would have
happened anyway, or a success that never tested the gate.

**`verify-tiers.ps1` is where the ssh and `logto` cases belong** and
`verify-tierapi.ps1` the API one. This is `$neverShipped` work and needs no
cycle. It is also what PRE_RELEASE 19 asks for: it lists what
`verify-tierchange.ps1` must cover, and the behaviour is known now rather than
guessed at.

***CORRECTED 28 Aug 2026, AND THE SENTENCE ABOVE NAMING `verify-tiers.ps1` FOR
THE ssh AND `logto` CASES IS WRONG.*** ***`verify-tiers.ps1` CANNOT TEST THE
`logto` DOOR AT ALL.*** `logto.authorised` puts the suspension test **after**
two privileged bypasses — `CPROC:3729` (already elevated) and `CPROC:3755`
(elevation just obtained) — which is a judgement call recorded at `CPROC:3765`,
not an oversight. `verify-tiers.ps1` **refuses to run unelevated** because
`CREATE.ACCOUNT` is gated on `K$ADMINISTRATOR`, so every `LOGTO` it issues takes
that bypass. **A door check written there would enter a suspended account and
report the design working as a product fault.**

***WHAT THE DOOR TESTS ACTUALLY NEED IS AN UNELEVATED SESSION AS A USER THE
SUSPENSION DENIES***, which is the group test at `CPROC:3781`:

| door | the shape that works |
|---|---|
| `LOGIN` | ssh in as the suspended account itself. `verify-sshonly.ps1` already has the `SSH_ASKPASS` machinery for an automated password login; `verify-tiers.ps1` has none |
| `logto` | **two** accounts: `grant` user A into account B, suspend B, then ssh as A and `LOGTO B`. A's own session is unelevated, so the bypass does not apply |
| API | the controlled pair already described above |

***AND SECTION 6 OF `verify-tiers.ps1` IS WRITTEN, 28 Aug 2026 — the half an
elevated session CAN reach.*** Parse-checked 0 errors / 2857 tokens, 9 functions
by both the parser and `grep`, no embedded BOM. ***RUN BY THE OWNER 28 Aug
2026, 00:07:29, on the 27 Aug 22:52:21 install — `assert-current` clean, 33
PASS, 0 FAIL***, of which section 6 contributed 11. Transcript
`SD-verify\verify-tiers-20260828-000729.log`. **Repeated at 00:13:03 with
`-Prefix sdtierb`: 33 PASS, 0 FAIL again**, so the section is reproducible
against fresh accounts rather than passing off one set's state. It covers:

- **the record** — `ACC$TIER` becomes `SUSPENDED` and `ACC$PRIOR.TIER` keeps the
  tier it displaced. The **PROGRAMMER** account is used deliberately: restoring
  to `PROGRAMMER` proves field 6 was read, where a STANDARD account would be
  restored to the value a defaulting bug also produces.
- ***the write-once guard, WHICH PRE_RELEASE 21 LEFT UNMEASURED.*** A second
  suspend must stop at the equality test (`10110`) and never reach the field-6
  write — if it did, `SUSPENDED` would overwrite `PROGRAMMER` and the only
  record of what the account was would be gone permanently. 21 deleted the
  unreachable inner test on the argument that the equality guard is the whole
  mechanism; **nothing had ever checked that.**
- **the VOC across `UPDATE.ACCOUNT`** — section 5's question asked of the harder
  tier, since `SUSPENDED` is not a VOC tier and `update.voc` must resolve it to
  field 6 (`LOGIN:283`, `:1212`).
- **the elevated bypass itself**, asserted rather than worked around, so a
  change to `CPROC:3765` is caught. It doubles as the null-case refusal: a
  refused `LOGTO` leaves the session in `SDSYS` and `COUNT VOC` answers with
  SDSYS's VOC, not 396, so a check that measured nothing fails.

**The section prints the three doors as NOT tested and scores none of them.**
That is what keeps this entry open.

## 39. Uninstalling strips SD's ssh confinement and leaves every account it created — **B?** (owner's call)

Found 27 Aug 2026 from the question *"will the released system leave litter
behind?"*. ***REASONED FROM SOURCE, NOT MEASURED*** — no uninstall was run to
watch it happen, and that should be done before this is acted on.

***THE THREE FACTS, EACH CHECKED.***

| | |
|---|---|
| **Uninstall removes no Windows account** | `sd.iss` contains no `Remove-LocalUser` and no call to `!delete_user` anywhere — grep, zero hits. `[UninstallRun]` removes the service and stops SD |
| **Uninstall strips SD's `sshd_config` block** | `RemoveAllowGroups` (`sd.iss:3367`) runs `allow-ssh-groups.ps1 -Remove`, which takes out **`AllowGroups` and `ForceCommand` together** |
| **`sdsshonly` denies the console and Remote Desktop, not ssh** | that is the whole design: SD accounts reach the machine over ssh and nothing else |

***PUT TOGETHER, UNINSTALLING CONVERTS EVERY SD ACCOUNT INTO AN ORDINARY
ssh-REACHABLE ACCOUNT WITH A SHELL.*** The accounts stay, with their passwords
and their group memberships. The ssh server stays — deliberately, and the
disclosure says so. What goes is the `ForceCommand` that put an ssh session
into SD instead of a PowerShell prompt, and the `AllowGroups` that said who
could connect at all.

***THE INSTALLER ALREADY NAMES THIS EXACT CONSEQUENCE, IN ANOTHER CONTEXT.***
`sd.iss:206`, about the task having been a one-shot: *"THE ForceCommand HALF IS
THE SHARP ONE: without it an ssh session lands at a PowerShell prompt instead of
in SD, so an account confined to sdsshonly gets a shell on the server - the
thing the confinement exists to prevent, arriving by the far door."* **It was a
defect there and it is the documented behaviour here.**

***AND THE CLOSING DISCLOSURE DOES NOT SAY SO.*** It lists what uninstalling
keeps as *"Your database, the ssh server, and the sdusers group"* — accurate as
far as it goes, and it **does not mention the accounts SD created, their
`sdu_`/`sdg_` groups, or their profiles**. An administrator reading it has no
reason to think there is anything to clean up.

***WHY THIS IS THE OWNER'S CALL AND NOT AN OBVIOUS FIX.*** Each option costs
something real:

1. **Say it in the disclosure and leave the behaviour.** Cheapest, honest, and
   the administrator does the work. **It also matches the database decision** —
   SD does not destroy the user's data on the way out, and an account is closer
   to data than to installation.
2. **Offer to remove the accounts**, the way removing the database is offered.
   Consistent with 1, and an uninstaller that deletes user accounts by default
   would be worse than the problem.
3. **Leave `AllowGroups` and `ForceCommand` in place.** *No* — an uninstaller
   must not leave configuration behind pointing at an `sd.exe` it has deleted,
   and 5.9 says SD does not keep hold of an ssh server it did not install.

**Option 1 is the smallest true fix and options 1 and 2 combine.** Nothing here
is urgent for a stand-alone install, which has no ssh server and no accounts but
the installing user's.

## 40. A verifier's transcript swallows the verifiers that run after it — **M** (verifier, not product)

Found 27 Aug 2026 while counting the `b49` run, and it **nearly produced a wrong
verdict in the same minute it was found**.

`SD-verify\verify-sshonly-20260827-232336.log` contains **two `[FAIL]` rows**.
They are not sshonly's. They read *"control: local elevated session refused
OS.EXECUTE"* — **`verify-apiadmin`'s** failing control, PRE_RELEASE 31, counted
twice because a transcript records a wrapped line and its continuation. The
file's tail is the **whole suite's** summary at 23:29:59, six verifiers after
sshonly finished.

***THE CAUSE: `Start-Transcript` WITH NO MATCHING STOP.*** `verify-sshonly.ps1`
calls `Start-Transcript` at `:161`; its only `Stop-Transcript` (`:156`) is in the
loop that closes **stale** transcripts at start-up. The verifiers run **in the
runner's own process** — the transcript header names
`VerifyInstall2.ps1 -Run b49` as the host application — so the transcript stays
open on the runner's session and records everything that follows.

***IT IS 15 OF 33 VERIFIERS, NOT ONE.*** Only 18 carry a `Stop-Transcript`
beyond the stale-closing one. The others are masked by luck: the *next*
verifier's stale-closing loop shuts the runaway, so the damage is bounded by
ordering, and the transcripts that look normal are 970 bytes because something
closed them quickly.

***WHY IT MATTERS MORE THAN A TIDINESS BUG.*** It is §6's *"the PASS count was
grepped out of files nothing could read"* in a new form: here the file reads
perfectly and **belongs to the wrong step**. Anyone counting `[FAIL]` per
verifier from `verify-<name>-*.log` attributes a later verifier's failures to an
earlier one. **The safe source is the runner's per-step captures**,
`20260827-<time>-NN-verify-*.log`, which are one file per step by construction —
totalled that way the run is **963 PASS, 1 `[FAIL]`, 0 `[SKIP]`**, and sshonly's
own capture is PASS 20, `[FAIL]` 0.

**The fix is a `try`/`finally` around each verifier's body**, or a
`Stop-Transcript` at every exit path. `$neverShipped`, no cycle.

## 41. The cleanup sweep reports "every section reached zero" on a machine that still has orphan directories — **M** (dev tooling, not product)

Found 28 Aug 2026 by writing a prediction before the run and reading `C:\Users`
back afterwards, which is the only reason it was found at all: the tool's own
output said the machine was clean.

***MEASURED, ONE RUN.*** `cleanup-devlitter.ps1` elevated, after a reboot:

```
  profiles matching    : 7 -> 0
cleanup-devlitter: done - every section reached zero.
```

***AND THREE ORPHAN DIRECTORIES WERE STILL THERE*** — `sdapiab49`,
`sdapiidb49`, `sdapinb49`, read back independently, the Windows account gone
for all three.

***THE CAUSE IS THAT THE COUNTER AND THE CLEANER SHARE ONE BLIND
ENUMERATION.*** `clean-test-profiles.ps1:223` builds its work list from
`Get-CimInstance Win32_UserProfile`, which enumerates from the `ProfileList`
registry key. A directory whose entry has been removed is not a
`Win32_UserProfile` object, so it is invisible **twice**: the sweep cannot clean
it, and the BEFORE/AFTER block cannot count it. **The AFTER figure is not a
measurement of the machine — it is a measurement of the same list the cleaner
has just emptied**, and it can only ever read zero.

***THE NAMES WERE NEVER THE PROBLEM.*** `sdapia`, `sdapiid` and `sdapin` are
all in the script's own pattern, printed at the top of its own run. The filter
would have matched them. Only the source of the list missed them.

**This is the instrument rule's named failure**: a test that passes because it
did nothing must fail, not pass. Here it reported zero because it could not
reach the thing it was reporting on.

***THE FIX IS CHEAP AND IT IS NOT "ALSO DELETE THEM".*** Scan `C:\Users`
directly with the pattern the script already reads out of
`clean-test-profiles.ps1`, subtract the paths `Win32_UserProfile` yielded, and
**report the difference as UNREACHABLE with the reason** — no `ProfileList`
entry, so nothing that enumerates profiles will ever see it. Whether it then
deletes them is a separate decision; **what it must not do is report zero.**

***AND PRE_RELEASE 36'S BOOT SWEEP MUST NOT INHERIT THIS.*** The ruling there
keeps both halves precisely so the profile stays enumerable — but a sweep built
on `Win32_UserProfile` would still be blind to every directory already in this
state on a customer's machine. **It has to enumerate the directory.**

`$neverShipped`, no cycle. Neither script is installed — checked against
`assert-current.ps1:471` and the 26 shipped scripts under `C:\Program Files\SD`.
