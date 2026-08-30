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

***THE TABLE BELOW IS THE INDEX. THE SECTIONS UNDER IT ARE DETAIL.*** A struck
number is done; **read the table, never the section headings.** Some entries have
no section at all — a short one needs no essay — so counting `## N.` headings
gives an answer that is wrong and looks authoritative. That is exactly how 28 Aug
2026 reported 36 open when 18 were, and filed three new entries onto numbers the
table had been using for a week.

***NEXT FREE ID: 64.*** Take it from here and increment it; **do not derive it by
scanning.** `gplbld/test-fixlist-units.ps1` enforces this line, the uniqueness of
every id, that a section and its row describe the same defect and agree on
status, and that every `PRE_RELEASE <n>` cited in PROJECT_STATUS.md, HISTORY.md
or a `gplbld` script names an id this table actually has. It needs no install and
no elevation.

| | SEV | what | where |
|---|---|---|---|
| ~~1~~ | **B** | ~~The `edit` / `micro` refusal message is malformed~~ — **DONE 27 Aug 2026** | `sdsys/gpl.bp/EDIT` |
| 2 | **B** | ***RE-OPENED 29 Aug 2026 BY THE OWNER'S NEW ACCESS MODEL — see 56.*** The fix wrote every ADMINISTRATOR-tier account into `os.users`, which is keyed on the **person** and so survives a `LOGTO`; 56 rules that an administrator has the rights of whatever account they move to. **And 56 abolishes the administrator account this attached to.** *(Was: the installing user gets no `OS.EXECUTE` — DONE 27 Aug 2026)* | `sdsys/gpl.bp/CREATEA` |
| 3 | **S** | The live `SDSYS` VOC does not match `voc_template` — ***RE-VALIDATED 28 Aug 2026 against the LIVE VOC, not a directory listing***: `ct voc %L` / `%G` / `%E` all answer `Record not found` while all three are present in `newvoc` AND `voc_template`; `ct voc =` returns `K` / `25` and `=` is in neither source tree. `count voc` says **428** against `voc_template`'s 426. Still open, and the specifics hold | `sdsys/voc_template` |
| ~~52~~ | **S** | ***The tester set documents `encrypt.field`, which no longer ships, and three tier numbers that moved with it*** — measured 28 Aug 2026 while fixing 4. `TIER.ADD.ADMINISTRATOR` is **21 lines − 1 header = 20 names** and `encrypt.field` is gone from it (PRE_RELEASE 25); `verify-tiers.ps1:42` is authoritative — **ADMINISTRATOR 392 + 20 + 4 = 416**, PROGRAMMER 396 and STANDARD 354 unmoved. SD corroborates: `count voc with dispatch # ""` in SDSYS answers **143**, which is 81 + 42 + 20. ***THE RECIPE, ALL IN `Testing/markdown`***: **05** line 18 `\| Verbs \| 81 \| 81 + 42 \| 81 + 42 + 20 \|`, line 19 `417`→`416`, line 29 `77`→`81`, line 55 `392 + 21 + 4 = 417`→`392 + 20 + 4 = 416`, line 69 `**21**`→`**20**`, line 73 `21 more`→`20 more`; **06** subtitle and line 5 `21`→`20`, line 61 heading drop *"and field encryption"*, line 65 delete the `encrypt.field` line, line 267 `of the 21`→`of the 20`, line 271 delete `**\`encrypt.field\`** · `; **07** line 4 `77`→`81`, line 7 `[21 more]`→`[20 more]`. ***Two edits of this were applied and REVERTED*** when the session ended — the docs repo is clean at `7914e60`, and a half-applied table is worse than none. ***DONE 28 Aug 2026 — ALL TWELVE EDITS APPLIED IN ONE COMMIT***, the diff 13 insertions / 14 deletions (the extra deletion is the `encrypt.field` code line). **Every number was re-derived from the tree before it was written, not copied from this row**: `newvoc` 395 entries, 119 field-1-`V` records, `TIER.ADD.ADMINISTRATOR` 21 lines, `TIER.OMIT.STANDARD` 43 | docs repo, `Testing/markdown/05,06,07` |
| ~~4~~ | **S** | Tester page 07 says a standard account has 77 verbs; it has 81 — ***81 CONFIRMED 28 Aug 2026 from the tree***: `newvoc` holds **119** records whose field 1 starts with `V`, plus the four keyword-and-verb records (`break`, `count`, `display`, `off`) = **123**, less `TIER.OMIT.STANDARD`'s **42** names (43 lines, first is a header comment) = **81**. **Fix it together with 52** — the same table carries `417` and `+21`, both stale, and correcting one number while leaving the others is how this page got wrong in the first place. *(The entry below says page 06 repeats the figure; it is page **05**.)* ***DONE 28 Aug 2026 with 52***, in the one commit both entries always needed | docs repo |
| ~~5~~ | **S** | `.d name` cannot find a lower-case VOC record typed in upper case — **FIXED 28 Aug: folds case like `.L`/`.R`, and reports 5043 instead of falling through with a stale `voc.rec`.** ***DONE 28 Aug 2026, MEASURED*** on the 00:53:34 install by `verify-vocverbs.ps1`: `.D ZZPRFD` printed `Delete VOC record 'zzprfd'?` — the lower-case name from an upper-case verb — the record was gone afterwards, and an unknown name reported 5043 with no second prompt | `CPROC:1119` |
| 6 | **S** | An empty directory called `C:` is created in the data tree by the installer | `gplbld/sd.iss` |
| 7 | **M** | `sort.item` is withheld from a standard account and `list.item` is not | `newvoc/TIER.OMIT.STANDARD` |
| 8 | **M** | `help` is an empty stub and F1 reaches it | `CPROC:2498` |
| 9 | **M** | `umask` is implemented and unreachable | `CPROC:3301` |
| ~~10~~ | **M** | ~~Two verifiers carry a dead ANSI strip~~ — ***IT WAS 23 FILES AND 24 OCCURRENCES, NOT TWO.*** **DONE 28 Aug 2026**: all converted to `([char]27 + '\[[0-9]*[A-Za-z]')`. ***AND IT WAS STILL SPREADING*** — three of the 23 were written the same day, by copying `probe-catprivate.ps1`'s `Invoke-SD` *"unchanged"*. **Guarded by a test, not by 23 comments**: `test-verdict-units.ps1` now scans the whole directory and fails if any script carries the dead form again, **tokenising rather than grepping** so a comment that quotes it (there are two, both correct) is not a false positive | `gplbld` |
| ~~11~~ | **B** | ***Nested `commit` silently loses the outer transaction's writes*** — UPSTREAM #17. ***DONE 29 Aug 2026***: the reinstate-and-decrement block is lifted out of `rollback()` into `end_txn_level()` and called from `op_txncmt()` too — **one function, both callers, because having it in one place with one caller is what the defect was.** Placed **before** `exit_op_txncmt:` so the three `k_error` paths do not pop a level they did not commit. **Measured on the 18:36:04 install, `verify-txn.ps1` 9 of 9**: the outer write now reads `outer` where it read `base`, the level delta is `0` where it was `+2`, and the parent transaction is reinstated where the session had been left in none. **Wired into `VerifyInstall1` after being measured, not before** | `gplsrc/txn.c`, `gplbld/verify-txn.ps1` |
| 12 | **S** | Error 3023 tells the user the disk may be full — UPSTREAM #20, **unfixed here**. ***28 Aug: NOT the message-only fix this entry claims — the call site is `gplsrc/op_dio3.c:853`, so it is a C change and a REBUILD, not a data change. Left out of the 28 Aug batch for that reason*** | `sdsys/messages/1407`, `gplsrc/op_dio3.c:853` |
| ~~13~~ | **M** | `qselect` prints its message without the list number — UPSTREAM #21. **FIXED HERE 28 Aug: `tgt.list` passed as the second argument.** ***DONE 28 Aug 2026, MEASURED*** by `verify-vocverbs.ps1`: the message ends in a list number, no dangling `select list `, and it selected more than zero. Still live upstream | `gpl.bp/QSELECT:240` |
| ~~14~~ | **S** | `delete.file ... no.query` still prompts, so it cannot run unattended — UPSTREAM #23. **FIXED HERE 28 Aug: `check.sdsys.file` takes the safe `N` branch under `no.query` and says so — new message 10117.** ***DONE 28 Aug 2026, MEASURED*** by `verify-vocverbs.ps1` on a copy of the `messages` pointer: 10117 printed, **6146 never asked**, the VOC reference gone and `sdsys\messages` still on disk. Still live upstream | `gpl.bp/DELETEF:222` |
| ~~15~~ | **M** | `delete.index` will not match a lower-case index name, though `list.index` will — UPSTREAM #22. **FIXED HERE 28 Aug: supplied names are case-corrected against the real ones, as `LISTI:147` does; an unknown name is still reported as typed.** ***DONE 28 Aug 2026, MEASURED*** by `verify-vocverbs.ps1`: `delete.index zzprfak f1` answered *"Deleted index F1"* and the file read back with no indices; **the control held too** — a genuinely unknown name came back **as typed**, not upcased. Still live upstream | `gpl.bp/DELETEI:155` |
| 16 | **S** | A killed session blocks exclusive access, says nothing about why, and only an administrator can clear it | `gplsrc/sd.c:333` |
| ~~17~~ | **B** | ~~`edit` / `micro` refuse a record whose text looks like a mark token~~ — **DONE 27 Aug 2026** | `sdsys/gpl.bp/EDIT` |
| ~~18~~ | **M** | ~~A text mark reaches the editor as a raw control character~~ — **DONE 27 Aug 2026** | `sdsys/gpl.bp/EDIT` |
| ~~19~~ | **B** | ***CLOSED 28 Aug 2026 BY `-Run b53`: ALL FIVE LEGS GREEN, BOTH TOKENS EXERCISED, AND THE OWNER'S CONDITION — "19 stays B until the doors are covered" — MET BY A PASSING RUN RATHER THAN BY ARGUMENT.*** `Create` **13/13**, `Control` **8/8**, `Suspend` **5/5**, `Refused` **5/5**, `Remove` **4/4**. ***ALL THREE DOORS ADMITTED AND THEN ALL THREE REFUSED, WITH THE SUSPENSION THE ONLY CHANGE***: ssh and `logto` in SD's own words (**10107**), and the API by the controlled pair, since it cannot identify its own refusal. **The `logto` door is genuinely covered at last** — `WHO` answered `91 SDDRB53A from SDDRB53B`, so the session *arrived* rather than started there, and **5161 did not appear**. ***THE REFUSED LEG PROVED THE ORDERING TOO***: *"logto: it was NOT 5161 instead of the suspension"* passed, so the refusal came from `logto.authorised` at `CPROC:2679` and not from the token-dependent chdir at `:2691` — which is why the refusal half was trustworthy even while 44 was unfixed. **Nothing was left behind**: no Windows accounts, no `sdu_` groups, no `ACCOUNTS` records, **0 orphan SIDs** in all three groups, only the two profile directories that are 35/36. *(Was: THE DOOR ITSELF NOW OPENS — `-Run b52`, 17:41. `Create` 13/13 with the helper granted and WINDOWS AGREEING, and the `logto` reached the account: `WHO` answered `91 SDDRB52A from SDDRB52B` and 5161 DID NOT APPEAR.)* 44's two-account cure works, and the non-decisive local witness failed in the same transcript as designed, so both halves are on one page. ***WHAT STILL FAILS IS THE CHECK, NOT THE DOOR***: the anchor required the account to be the whole of the second field, and `WHO` appends `from <ACCOUNT>` **only when the session has logto'd** — so it matched only the case where the door had NOT opened. ***THAT IS THE SAME TRAP AS THE ORIGINAL, FROM THE OPPOSITE SIDE***: the first version matched the name anywhere and passed on the failure path; its replacement matched only at end of line and failed on the success path. **Both were written from a transcript of the path they were not meant to catch.** Now anchored on the shape — a number, then the account as a whole word — with a **second decisive row on the `from <helper>` clause**, which is the stronger evidence because it says the session ARRIVED rather than started there. **Five paths measured against the same two patterns**: real b52 success, real b50 failure, echo-only, started-there, and a logto to a different account. **`-Run b53` is what closes 19.** *(Was: RE-OPENED 28 Aug, one row of seven — the check matched the echo of its own command; reproduced on a second account on `-Run b51`.)* ***WHAT CLOSES IT IS NOW BUILT AND UNRUN: 44's two-account door, and `-Run b52` is the run that decides.*** A written verifier is still not coverage — the owner's ruling has not changed — so **19 stays open until a leg passes**. `verify-doors.ps1:255` was `Test-Say $out $acctU`, and the session echoes what it is fed, so `SDDRB50A` was in the transcript whether the `LOGTO` landed or not. **On the `-Run b50` Control leg SD printed 5161 *"Unable to change to new directory"* and `WHO` answered `91 DON` — the session never left `DON` — and the row scored PASS.** The same check scored the same PASS on `sddr2`, which is what the struck text below rests on. **Anchored on `WHO`'s answer now** (`^<number> <ACCOUNT>$`, the shape nothing typed can produce) **with 5161 as a disqualifier**, and both directions measured against the real transcript. ***THE CAUSE IS 44, AND THE CURE IS ALREADY WRITTEN DOWN IN THIS FILE***: the `logto` row of the door table below says **two** accounts — *"ssh as A and `LOGTO B`"* — and the implementation instead runs `LOGTO` in the caller's own session, whose token predates the `sdu_` group. **ssh and the API are unaffected: both authenticate afresh, and both remain measured.** ***THE REFUSAL HALF STILL STANDS*** — `logto.authorised` is called at `CPROC:2679`, **before** the chdir at `:2691`, so a suspended account is refused with 10107 and never reaches 5161. **What is unproven is the ADMITTED half of the pair, for one door of three.** Owner's to confirm; reversible if he reads it otherwise — ~~**DONE 28 Aug 2026. The owner's ruling was *"19 stays B until the doors are covered"*, and the condition is now met by a passing run rather than by argument.**~~ Six rows closed by `verify-tierchange.ps1` (28 PASS); ~~**the last row — the three doors — is closed by the `verify-doors` pair**, all four legs green on `sddr2`: `Create` 8/8, ***`Control` 6/6 with ssh, `logto` and the API ALL ADMITTED***, `Suspend` 5/5, ***`Refused` 4/4 with ALL THREE REFUSED***.~~ `LOGIN:477` and `CPROC:3776` said it in SD's own words (10107, *"Account SDDR2A is suspended"*) — **ssh after the banner, so authentication had succeeded and the refusal is SD's, with the account still in `sdssh` so no Windows group moved.** The API cannot identify its own refusal by design, so **the controlled pair is what proves it**: same account, same password, same call, admitted then refused, the suspension the only change. **Found and fixed a defect in the verifier on the way — see 42** | `gpl.bp/MODIFYA`, `gplbld/verify-tierchange.ps1`, `verify-doors-admin.ps1`, `verify-doors.ps1` |
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
| ~~31~~ | **S** | ***DONE 29 Aug 2026, MEASURED ON `-Run b59`: `verify-apiadmin` 22 PASS / 0 FAIL / 0 SKIP AND THE CONTROL PASSES*** — `[PASS] control: local elevated session refused OS.EXECUTE: expected False, got False`, after failing on five consecutive runs. ***CLOSED BY 56 WITH NO EDIT TO THE VERIFIER AT ALL***: `CREATEA` stopped writing administrators into `os.users`, so `os_permitted()` falls through to a lookup that finds nothing and refuses — the control's original expectation is simply right again. ***AND THE RECORDED "21/23" WAS WRONG IN THE DENOMINATOR***: b58's own log reads 21 PASS / **1** FAIL, so it was always **22** checks. The figure to carry forward is **22/22**. *(Original entry below.)* ~~`verify-apiadmin`'s control is stale~~ — it expects an elevated session `LOGTO`'d into a PROGRAMMER account to lose `OS.EXECUTE`, but `os_permitted()` keys the list on `process.username` (`don`), whom PRE_RELEASE 2 listed. Headline hole (API OS.EXECUTE) stays closed. ***RULED 29 Aug 2026 — BEING AN ADMINISTRATOR IS THE GATE, SO THIS IS A PRODUCT CHANGE AND NOT THE VERIFIER-ONLY FIX THIS ROW USED TO CLAIM.*** Owner: *"any administrator keeps universal rights, ssh, api, os.execute, no matter which account they logto. Permission belongs to the person, even if they logto an account with fewer priviledges."* **Today an administrator who is NOT in `os.users` is REFUSED after a `LOGTO`** — `CPROC:2713` clears `USR_ADMIN` and `os_permitted()` falls through to the list; `don` passes only because PRE_RELEASE 2 listed him. **Sev raised S → B: the defect is the product, not the instrument.** ***AND THAT RULING IS WITHDRAWN THE SAME DAY — SEE 56.*** Told what it cost, the owner reversed it: *"if they logto another account, they have the rights of that account."* **That is what `CPROC:2735` already does**, so the product is right and this is once more the verifier-only fix it was first filed as. **Sev back B → S**, and the work is one assertion in `verify-apiadmin.ps1`, which must not be changed until 56 lands. Not started | `gplbld/verify-apiadmin.ps1` |
| ~~32~~ | **S** | ~~`delete.account` leaves the `ProfileList` registry entry, so an account recreated under the same name gets a DIFFERENT home directory~~ — **FIXED 27 Aug 2026: the `catch { exit 6 }` that left both halves is now `catch { }`, and the key is removed in its own right; status 6 splits into 6 (directory) and 7 (registry entry).** ***PARTLY REVERSED 28 Aug BY 36, ON THE OWNER'S RULING, AND DELIBERATELY***: removing the entry over a directory that is still there destroys the only handle a sweep has, so the entry is now removed **only if the directory went**, both halves are kept together otherwise, and something comes back for the pair. **The defect this entry names is still fixed** — an entry is never left behind on its own. **Its regression test is re-scoped** from *"the entry is gone"* to *"the entry is gone when the directory went"*. ***BOTH FIXES REMAIN UNCOMPILED — needs a cycle.*** Generated PowerShell parse-checked 0 errors / 203 tokens on 27 Aug, 1944 chars on 28 Aug; the new steps run read-only against a real account | `gpl.bp/DELETE_USER`, `gpl.bp/DELACC`, `messages/10075`, `messages/10116`, `gplbld/verify-delaccount.ps1` |
| ~~33~~ | **S** | ~~`allow-ssh-groups.ps1`'s own usage text offers a bare form that **writes nothing**~~ — **DONE 27 Aug 2026**, the usage line names `-Installed` and a dated note says which forms need it. Comment only, parses 0 errors / 1247 tokens | `gplbld/allow-ssh-groups.ps1:4` |
| 34 | **S** | ***`release.ps1` cannot complete on the `Technical` set*** — `checklinks.py` rightly refuses a zero-link set, and two pages in, `Technical` still has no honest cross-reference. A whole set has no working release command. **Not to be settled by adding a link.** ***RULED 29 Aug 2026 — A SET MAY DECLARE ITSELF LINK-FREE.*** `checklinks.py` gains an explicit per-set way to say *this set legitimately has no links*, and `release.ps1` accepts it; `Technical` opts in. **The zero-link refusal stays the default for `User`, `Administrator` and `Testing`**, so a set that loses its links by accident still fails loudly — the guard is narrowed by declaration, never removed. Not started | docs repo `tools/release.ps1`, `tools/checklinks.py:57` |
| ~~35~~ | **S** | ***DONE 28 Aug 2026, MEASURED*** — `create.account` now refuses the name and prints the directory (10124), witnessed by the new `gplbld/verify-profiledir.ps1` **14/14** on the 21:27:34 install, with a control account created and deleted in the same run. ***A profile DIRECTORY left behind moves the next account's home just as the registry entry does*** — found by running 32's own regression test on the install that fixed 32. `DELETE_USER` now tries to remove it, **and MEASURED: it cannot be deleted OR renamed while the hive is mounted**, so the honest answer is the rewritten `10075`, which names the cause and the restart. **Cure is 36, and 36 IS BUILT AS OF 28 Aug 2026 AND UNRUN**: the boot sweep removes the directory and `create.account` refuses the name until it is gone, so both halves of this symptom are answered — **but nothing has compiled yet, so this stays open until a cycle and a restart have been through it** | `gpl.bp/DELETE_USER`, `gpl.bp/DELACC`, `messages/10075` |
| ~~36~~ | **M** | ***DONE 28 Aug 2026, ALL FOUR RULINGS OBSERVED.*** The sweep reclaimed **5 of 5** after a restart (`5 considered, 5 reclaimed, 0 still pending, 0 refused`), `C:\Users` fell **61 → 56 by exactly those five** with `ProfileList` 46 → 41, the re-scoped 32 test is green in b56–b58, and `create.account` refuses a live directory (`verify-profiledir.ps1` 14/14). Two defects were found on the way and fixed — **49** and **50**. ***BUILT 28 Aug 2026, ALL FOUR RULINGS.*** Directory first and the `ProfileList` entry only if it went (`DELETE_USER`); the pair recorded under `C:\ProgramData\SD\profile-reclaim`; `gplbld/reclaim-profiles.ps1` sweeps it from `sdsvc.exe` at every service start; `create.account` REFUSES on an existing profile directory and names it (`!profile_dir`, 10124/10125). **New statuses 6/7/8 and messages 10075 rewritten, 10116 rewritten, 10123/10124/10125 new.** ***THE SWEEP READS THE RECORD, NOT `ProfileList`***, so it does not inherit the blindness that left `sdapiab49` and two others unfindable. **Its refusal table is a pure function guarded by `gplbld/test-reclaim-units.ps1` — 39/39, and its positive control against a copy with the containment check removed fails 34/5.** **The store gets an ACL of its own** (`gplbld/secure-reclaim.ps1`): inherited, it would be a list of directories every SD user can edit and LocalSystem later deletes. **32's regression test is re-scoped** in `verify-delaccount.ps1` from *"the entry is gone"* to *"the entry is gone when the directory went"*, with the keep-both branch asserting the record. *(Was: RULED 27 Aug 2026 AND NOT BUILT.)* ***Deleted accounts leave their registry hives mounted — 22 orphan SIDs / 44 hives on this host*** — the ROOT CAUSE of 32 and 35. **Mechanism confirmed: `Remove-CimInstance` failed on a mounted hive, then cleared `53 removed, 0 failed` after a restart.** Nothing SD does can unmount them | `gpl.bp/DELETE_USER`, `CREATEA`, `DELACC`, `PROFILE_DIR`; `gplsrc/sdsvc/sdsvc.c`; `gplbld/reclaim-profiles.ps1`, `secure-reclaim.ps1`, `test-reclaim-units.ps1` |
| ~~37~~ | **S** | ***`create.account` prints two lines that contradict each other***: with `both` it says *"may sign in over ssh only"* then *"may sign in over ssh and use the API"*. **Two different gates** — Windows logon rights (`CREATEA:808`) and SD route keywords (`:1612`) — worded so nothing tells the reader that. **FIXED 28 Aug: 10034 now says "may reach this computer only over ssh"; 10076/10077/10078 are recast as "SD routes for %1: ...". Nothing anchors on the old text — checked.** ***DONE 28 Aug 2026, MEASURED*** by `verify-acctmsgs.ps1`: on a real `create.account … programmer both`, 10034 read *"may reach this computer only over ssh"* and 10078 *"SD routes for …: ssh and the API"*, **and both old wordings were absent** — the disqualifier is what carries this one, since both lines contain "ssh" and any check anchored there would have passed on the defect | `messages/10034`, `10076`, `10077`, `10078` |
| ~~38~~ | **M** | ***WIRED IN 28 Aug 2026 ON THE OWNER'S RULING — "wire the pair into VerifyInstall".*** `gplbld/verify-doors-suite.ps1` drives all five phases as **one step** and is the **last step of `VerifyInstall1`**, conditional on `-Run`. ***IT HAD TO GO IN THE UNELEVATED RUNNER, AND THAT IS FORCED, NOT PREFERRED***: the phases need alternating tokens (Create elevated, Control ordinary, Suspend elevated, Refused ordinary, Remove elevated) and **an elevated parent cannot make an ordinary child** — `runas /trustlevel` yields a RESTRICTED token, not the user's own (`VerifyInstall1.ps1:70`) — so the ordinary half must be the parent. It raises the three elevated children itself, **announcing each UAC prompt**, and the child redirects its own output because `-Verb RunAs` cannot be combined with `-RedirectStandardOutput`. **It refuses a prefix with any residue before creating anything** — Windows user, `sdu_` group, `ACCOUNTS` record, **or profile directory** — because a name is single-use once its account has reached the Control leg. ***COSTS: three more UAC prompts, and one permanent profile directory per suite run until 35/36 is built.*** **Unrun as a suite step** — the refusal path was exercised (exit 2, nothing created) and the five phases were run by hand. **The original finding:** ~~The suite tests SUSPENDED on no door at all~~ — neither `verify-tiers.ps1` nor `verify-tierapi.ps1` contains the word. ssh and `logto` are now measured by hand; **the API door has never been reached** and cannot be tested by wording, since `APISRVR:507` refuses with the same `sysmsg(10003)` as every other refusal. **Needs a controlled pair.** ***28 Aug: `verify-tiers.ps1` section 6 written and UNRUN — the record, the write-once guard 21 left unmeasured, and the VOC. It CANNOT test the `logto` door: the check sits after `CPROC:3729`'s elevated bypass and this verifier must be elevated.*** ***THE CONTROLLED PAIR NOW EXISTS AND HAS PASSED, 28 Aug 2026*** — `verify-doors-admin.ps1` + `verify-doors.ps1` on `sddr2`, all four legs green, **all three doors ADMITTED then all three REFUSED**, and ***the API door was reached for the first time***. **WHAT IS LEFT OF THIS ENTRY IS ONE DECISION, NOT A MEASUREMENT: the pair is standalone and is NOT wired into `VerifyInstall1`.** It is deliberately unwired for the same reason `verify-acctmsgs` is — **it creates a real Windows account**, and it needs an elevated half and an unelevated half, which is the split the suite already has. **Owner's call: wire it into the two runners, or leave it standalone and named in the docs.** Note the fixture is single-use — its Control leg's ssh login leaves a profile directory that entries 35/36 cannot yet remove, so each attempt needs a fresh prefix. ***RUN AS A SUITE STEP FOR THE FIRST TIME ON `-Run b50`, 28 Aug 2026, AND IT FAILED TWICE FOR TWO DIFFERENT REASONS.*** First run: `Create` 8/8 and `Control` 6/6, then **Suspend and Remove died before their UAC prompt** — entry 43. Second run, after the same cycle: **refused up front**, because the first run had already spent `sddrb50a` at the Control leg — **the single-use guard working exactly as designed, and nothing was created.** ***THE PRICE IS NOW MEASURED RATHER THAN ESTIMATED***: a failed run leaves a **live, enabled, UNSUSPENDED** account in `sdusers`, `sdssh` and `sdapi` plus its profile directory, because the leg that removes it is the one that did not run. **43 is fixed and unrun; the next attempt needs a fresh `-Run` token** | `gplbld/verify-tiers.ps1`, `verify-tierapi.ps1`, `verify-doors-admin.ps1`, `verify-doors.ps1`, `verify-doors-suite.ps1` |
| 39 | **B** | ***Uninstalling strips SD's `AllowGroups` and `ForceCommand` and leaves every account SD created*** — so each becomes an ordinary ssh-reachable account with a PowerShell shell. `sd.iss` removes no account anywhere; the closing disclosure does not mention them. ***NO LONGER REASONED — MEASURED 28 Aug 2026, AND IT SURVIVES A WHOLE CYCLE.*** `cycle.ps1` uninstalled and deleted **both** trees at 15:29:59, so `sddrb50a`'s `ACCOUNTS` record went with the data tree — the register now holds only `don` and `sdsys`. **The Windows side did not move**: the account is still **enabled**, still has its own `sdu_sddrb50a` group, and is still a member of `sdusers`, `sdssh` **and** `sdapi`, with `sshd_config` still carrying `AllowGroups sdssh`. **So the account outlived the SD installation that made it, keeping every route it was granted.** ***AND IT IS NOW UNREMOVABLE BY SD***: `DELETE.ACCOUNT` cannot reach an account with no `ACCOUNTS` record, so `verify-doors-admin.ps1 -Phase Remove` correctly FAILS on it rather than reporting a tidy pass, and names it STRANDED. **Whether SD would still admit a login is NOT measured** — the password was generated inside an elevated child and never printed, deliberately. **What is measured is that Windows still would.** ***RULED 29 Aug 2026 — A SECOND, SEPARATE PROMPT ON UNINSTALL, AND IT MUST NEVER TAKE THE INSTALLING PERSON'S OWN ACCOUNT.*** Owner: *"a second separate prompt, however deleting the windows accounts should not delete the account of the person doing the installation so that there is at least one remaining account that can log into windows."* So `sd.iss:3482`'s *"Remove the SD database as well?"* stays exactly as it is, and a **second** question follows it about the Windows accounts SD created (with their `sdu_`/`sdg_` groups and profiles), defaulting to keep. **The installing user is excluded from that sweep by construction, not by the operator noticing** — leaving at least one account that can still sign in to Windows. **The closing disclosure is wrong either way and is fixed with it**: it names the database, the ssh server and `sdusers`, and never mentions the accounts. Not started | `gplbld/sd.iss:3367`, `sd.iss:3482`, the closing disclosure |
| ~~40~~ | **M** | ~~A verifier's transcript keeps recording the verifiers that run after it~~ — `verify-sshonly-*.log` carried `verify-apiadmin`'s `[FAIL]` rows and the whole suite's summary. `Start-Transcript` with no matching stop, **15 of 33 verifiers**. **DONE 28 Aug 2026, AND FIXED IN THE TWO RUNNERS RATHER THAN IN FIFTEEN VERIFIERS**: `VerifyInstall1` and `VerifyInstall2` now close every transcript a step left open, **name the step that leaked**, and `VerifyInstall1` restores its own with `-Append`. **One place, it cannot be forgotten by the next verifier somebody writes, and it also covers the case a `try`/`finally` does not — a step that dies outright.** ***Mechanism verified against real nested transcripts*** (none-open, three-leaked, and the runner's close-and-restore shape), **not yet in a suite run** | `gplbld/VerifyInstall1.ps1`, `VerifyInstall2.ps1` |
| ~~41~~ | **M** | ~~***The cleanup sweep reports "every section reached zero" while three orphan directories are still on disk***~~ — the counter and the cleaner share one `Win32_UserProfile` enumeration, which reads from `ProfileList`, so a directory whose entry is gone is invisible to both. **Measured 28 Aug: `7 -> 0` and "done" with `sdapiab49`, `sdapiidb49`, `sdapinb49` still there.** **DONE 28 Aug 2026** — both scripts now carry a **direct `C:\Users` scan** as a second, independent instrument: `clean-test-profiles.ps1` names them **UNREACHABLE with the reason and exits non-zero** (*before* its "nothing to do" return, which is the path the measured run took), and `cleanup-devlitter.ps1` counts them in **both** BEFORE and AFTER and will no longer say *"every section reached zero"* over them. ***Reported, not deleted*** — the removal decision is 36's. ***AND THE POSITIVE CONTROL FOUND A SAFETY BUG IN THE FIX***: under a permissive pattern the scan returned **`All Users`, a junction to `C:\ProgramData`**, for which the code prints a `Remove-Item -Recurse -Force` line. **Reparse points are now excluded in both copies**, and the guard is exercised by a test. **36's boot sweep must not inherit the blind enumeration** | `gplbld/clean-test-profiles.ps1`, `cleanup-devlitter.ps1` |
| ~~42~~ | **M** | ***FIXED 28 Aug 2026 ON THE OWNER'S RULING — "prompt for password at creation".*** `!set_passwd` now writes SD's own credential through `!CRED_SET` from the **same prompt** that sets the Windows one, so 10078 is true of a new account. **One prompt, both stores; they remain separate credentials and `modify.password` still changes SD's alone.** New status **6** — the half-set case, Windows took it and `$cred` did not — with message **10122**, and `CREATEA` names it rather than falling through to 10121's *"status %1"*. ***THE FIX IS COMPILED-AND-UNRUN UNTIL A CYCLE***: it is the first `sdsys` change since 28 Aug 00:53:34, so the installed tree is stale and nothing can test it until one runs. **The original finding:** ~~`create.account ... both` announces the API as a route, but the account cannot use the API until `modify.password` is run~~ — 10078 prints *"SD routes for %1: ssh and the API."* while the only password the verb prompts for is the **Windows** one (*"New Windows password for %1"*). **The two doors authenticate against different stores and nothing says so**: sshd checks the Windows password, so ssh is admitted; the API does SCRAM against a PBKDF2 verifier in `sdsys\$cred` that **only `MODIFY.PASSWORD` writes**, so it refuses. ***Measured 28 Aug 2026, the first time the API door was ever reached***: `sddr1a`, created `PROGRAMMER BOTH`, was in `sdapi`, `sdssh` **and** `sdusers` — the route was granted and the credential did not exist — and `sd-connect` answered `QMError(): Invalid username or password`. **The refusal is the worst possible one to debug**: `APISRVR:507` deliberately answers `10003` for *"no such account"* and *"not granted"* too, so nothing in it points at a missing password. `SET_ACC_PASSWORD:195-198` already owns the sentence — *"ssh and the SD API will refuse to connect until a password is set"* — but it is printed by the wrong verb and is **wrong about ssh**, which the Windows password admits. **Owner's call: prompt for the SD password at creation, or have 10078 say the API needs one.** `verify-doors-admin.ps1` also runs `MODIFY.PASSWORD` itself, and that stays — it keeps the door pair working against an install predating this fix. ***ONE SENTENCE IS STILL WRONG AND IS LEFT ALONE DELIBERATELY***: `SET_ACC_PASSWORD:195-198` tells someone declining a first password that *"ssh and the SD API will refuse to connect"*, and **ssh does not** — a Windows password admits it, which is exactly what `sddr1a` did. That path is now reachable mainly for SDSYS at install, since creation unwinds without a password; **worth correcting when someone is next in that file** | `gpl.bp/SET_PASSWD`, `gpl.bp/CREATEA`, `sdsys/messages/10122`, `sdsys/messages/10078` |
| ~~43~~ | **S** | ~~***The door suite's Suspend and Remove legs could never elevate, so the suite could never pass***~~ — **DONE AND WITNESSED 28 Aug 2026, `-Run b51` at 16:54.** ***THE FIX IS NOT MERELY WRITTEN: BOTH ELEVATED LEGS LAUNCHED AND THE `Remove` LEG RAN AS A SUITE STEP FOR THE FIRST TIME EVER*** — `Create` **8/8** on `argv (15)` with the password masked, `Remove` **2/2** on `argv (13)` with no `-Password` at all, and the run left **no Windows account, no `sdu_` group and no `ACCOUNTS` record** behind (read from disk afterwards; only the 35/36 profile directory remains). **The printed argv is what makes it checkable at a glance**, and it is in the transcript of every leg now. `Invoke-ElevatedPhase` passed `'-Password', $Password` unconditionally, and Suspend and Remove take no password (`verify-doors-admin.ps1:58` defaults it to `''`). ***`Start-Process -ArgumentList` CARRIES `[ValidateNotNullOrEmpty()]`, AND ON A COLLECTION THAT VALIDATES EVERY ELEMENT***: one `''` rejects the whole list with *"The argument is null or empty"* and **nothing launches**. Measured on `-Run b50`: Create carried a password and ran 8/8, Suspend and Remove died **before their UAC prompt**, so the account was left unsuspended and the Refused leg could not run. **The pair is now built conditionally** — the idiom `sd-elevate.ps1:118` already used for its optional `-LogFile` — with the **argv and its element count printed**, and an **empty element refused by name** rather than by a binding message that identifies none. `gplbld/test-doorsargv-units.ps1` guards it: **35 of 35**, no install, no elevation, no account; ***its positive control is `-Suite <copy carrying the old form>`, run and observed FAILING 27/8***. The live cmdlet's rejection was measured directly, not reasoned | `gplbld/verify-doors-suite.ps1`, `test-doorsargv-units.ps1`, `assert-current.ps1` |
| ~~45~~ | **M** | ~~***The litter sweep could not see the door pair's accounts at all — `sddr` was never added to the stem list***~~ — **DONE 28 Aug 2026.** `verify-doors-admin.ps1` invented a name family on 28 Aug and nothing added its stem to `clean-test-profiles.ps1`, which is where `cleanup-devlitter.ps1` reads the pattern from. **So `sddr1a`, `sddr2a`, `sddrb50a` and `sddrb51a/b` were invisible to both scripts**, and a sweep over them would have reported a clean machine — ***PRE_RELEASE 41's lesson with a different blind spot***: 41 was a counter that could not see a directory whose `ProfileList` entry had gone, this was a pattern that could not see the name. **`sddr` added, with the five real names as must-match fixtures** and `sddriver`/`sddrive` added to the must-NOT list, because the stem is short enough to want a word-shaped control. Both self-tests re-run: `clean-test-profiles -SelfTest` **29 of 29 must-match, 20 of 20 correctly rejected**; `cleanup-devlitter -SelfTest` **0 cases failed**, and it reads the pattern out of the sweep rather than duplicating it, so one edit fixed both. ***THE RULE THIS LEAVES: a test that invents a name family adds its stem in the same commit***, or its litter is invisible to the only thing that sweeps it up. ***AND THE SAME `-List` RUN SHOWED A SECOND STALE INSTRUMENT LINE, ALSO FIXED***: the header said *"`sshRemoteTest-C1` left alone (-IncludeVM to delete)"* about a VM the 7.18 cleanup **deleted** — *"left alone"* reads as *"still present"*. It now says whether the VM is registered, measured in **both polarities** (the spent name `known=False`, a real one `known=True`). **The name is deliberately NOT repointed at `sdStandalone-C1`**, which does exist: PROJECT_STATUS records that guest as one to delete **by hand** when nobody needs it, and pointing `-IncludeVM` at it would turn a documented manual decision into a side effect of a sweep | `gplbld/clean-test-profiles.ps1`, `cleanup-devlitter.ps1` |
| ~~47~~ | **M** | ~~***The door suite leaked a temp directory on every refused run, and two runs in one second crashed it***~~ — **DONE 28 Aug 2026**, both found by running the suite twice inside a second while testing 48's helper route. **`$work` was created ABOVE the residue check**, and the refusal path exits before the `try`/`finally` that removes it — **four leaked directories were on disk**, one per refused run. And **`$stamp` is `yyyyMMdd-HHmmss`**, so a second run in the same second hit *"An item with the specified name already exists"* and **died with an unhandled exception — exit 1 from a script whose refusal code is 2**, which would read as a failed measurement rather than a refusal. ***THE LEAK MATTERS MORE UNDER 48***: `$work` now holds the Create launcher and that launcher carries the password. **The four were measured empty, so nothing leaked** — but the property was holding by luck. Now uniquely named and created only once the run is going ahead. **Measured after: two refused runs in the same second, both exit 2, no new directory** | `gplbld/verify-doors-suite.ps1` |
| ~~48~~ | **M** | ***DONE AND WITNESSED — `-Run b54`, 28 Aug 2026 19:28. ALL FIVE LEGS GREEN THROUGH THE HELPER, ONE PROMPT INSTEAD OF THREE.*** `Create`, `Suspend` and `Remove` each printed `via helper:` with the password **masked**, the door step exited **0**, and the run cleaned up completely: **no accounts, 0 orphan SIDs, no stray `sd.exe`, the work directory gone, the helper stopped and its pipe closed.** ***BUILT AND UNRUN 28 Aug 2026, ON THE OWNER'S RULING — the door suite's three UAC prompts become one.*** It routes the three elevated legs through **one resident elevated helper**, reusing the shipped `sd-elevate.ps1` that SD's own `ELEVATE` verb drives rather than growing a second copy of security-sensitive elevation code — *that duplication is the defect class 46 was*. **`-NoHelper` keeps the `Start-Process -Verb RunAs` route that `-Run b53` went green on**, and `test-doorsargv-units.ps1` drives **both** (**51 of 51**). ***A SUITE RUN GOES FROM FOUR PROMPTS TO TWO, NOT TO ONE, AND THE REASON IS A HARD LIMIT***: `sd-elevate.ps1` hard-codes a **300-second per-request timeout**, which every door leg finishes inside and `VerifyInstall1`'s own elevation of `VerifyInstall2` does not — that half runs 19 verifiers. **Taking it to one means editing a shipped file, which makes the tree stale and costs a cycle. Owner's call, not assumed.** ***THE SECRET MOVED FROM A COMMAND LINE INTO A FILE, AND THAT IS A STEP UP RATHER THAN DOWN — MEASURED, NOT ARGUED***: the helper passes no arguments, so the launcher is self-contained and carries the password; but `Win32_Process.CommandLine` returned a marker argument **verbatim to a same-user process**, while a `%TEMP%` file carries **SYSTEM, Administrators and the user and nobody else**. Same three principals, except the file is deleted in the `finally`. **The old comment — *"the launcher carries no secret, the password arrives as its argument"* — had it backwards.** ***UNRUN: the Create leg is elevated, so `-Run b54` is what exercises it***, and if the helper cannot start it falls back to a prompt per leg rather than failing the run | `gplbld/verify-doors-suite.ps1`, `test-doorsargv-units.ps1` |
| ~~46~~ | **S** | ~~***`verify-tierapi.ps1` and `verify-tiers.ps1` disagreed about the ADMINISTRATOR VOC count, and nothing compared them***~~ — **DONE 28 Aug 2026.** PRE_RELEASE 25 deleted `encrypt.field` (a V record pointing at `$CRYPTO`, which is nowhere in the tree), so ADMINISTRATOR went **417 → 416** and the other two tiers did not move. **`verify-tiers.ps1` was re-derived from the directory the same day; `verify-tierapi.ps1` was not**, so the pair disagreed about one fact for a day. ***IT SURFACED AS `-Run b52` STEP 19***, the first suite run to reach `verify-tierapi` against an install carrying 25's change — 22 PASS / 1 FAIL, *"ADMINISTRATOR VOC count: expected 417, got 416"*. **The product was right and the verifier was stale.** Re-derived from `newvoc` rather than copied across: 395 names − 3 = 392 base, `TIER.ADD.ADMINISTRATOR` 21 lines = 20 verbs, so **392 + 20 + 4 = 416**, with PROGRAMMER 396 and STANDARD 354 unmoved as the check on the arithmetic. ***THE CLASS FIX IS `gplbld/test-tiercounts-units.ps1`***, new: it re-derives all three counts from the directory and checks **both files against the TREE**, not against each other — *two files agreeing on a wrong number is exactly as broken as two disagreeing* — and asserts the two differences equal what the two list records add and remove, so a typo in one sum cannot pass. **13 of 13**, no install, no elevation, no run token. ***ITS POSITIVE CONTROL RAN AGAINST THE PRE-FIX PAIR TAKEN FROM `git show`***, not retyped: **12 passed, 1 failed**, naming the file and both numbers | `gplbld/verify-tierapi.ps1`, `test-tiercounts-units.ps1` |
| ~~49~~ | **S** | ***`reclaim-profiles.ps1 -List` reported "0 records" when it was merely not allowed to read the store*** — `-ErrorAction SilentlyContinue` swallowed the access denial and the empty-store branch announced its own reading as fact. The store is granted to SYSTEM and Administrators only, so an unelevated `-List` could never have said anything else. **DONE 28 Aug 2026**, measured on the install: it now refuses and exits 2. *(Filed as "42" on the day and renumbered — 42 was already taken.)* | `gplbld/reclaim-profiles.ps1` |
| ~~50~~ | **B** | ***The reclaim sweep refused every record `DELETE_USER` will ever write*** — the owner check accepted only `S-1-5-18` or `S-1-5-32-544`, and an elevated process owns what it creates by its **own** SID, so the producer could never satisfy the consumer: five genuine records, five refusals, nothing reclaimable on any machine. It shipped past a 39/39 unit suite whose accepted rows all handed in SYSTEM or Administrators. **DONE 28 Aug 2026** on the owner's ruling — the per-file owner check is gone and the store's ACL is the containment; sweep 5/5 after a restart. *(Filed as "43" and renumbered.)* | `gplbld/reclaim-profiles.ps1`, `test-reclaim-units.ps1` |
| ~~51~~ | **M** | ***`Get-SysMsgPattern` could not match any MULTI-LINE message*** — the message files hold literal backslash-n and `[regex]::Escape` turned each into a pattern hunting a literal backslash the rendered output never contains. It cost `verify-profiledir` a FAIL on a correct product, left `verify-delaccount:553` incapable of failing, and left `:568` certain to fail on the first machine whose profile hive is still mounted. **THE THIRD TIME THIS FUNCTION HAS GONE BLIND** (see 45 for the second). **DONE 28 Aug 2026, all five copies**, plus `gplbld/test-sysmsg-units.ps1` — 43/0, control 37/2 on the pre-fix copies. *(Filed as "45" and renumbered.)* | `gplbld/verify-*.ps1` |
| 44 | **S** | ***RE-VALIDATED 28 Aug 2026 FROM THE INSTALLED MESSAGE, not from this entry's own text***: `C:\ProgramData\SD\sdsys\messages\5161` reads exactly `Unable to change to new directory` — nothing about the group, the token, or signing out. Still open. ***THE VERIFIER HALF IS DONE AND WITNESSED — `-Run b53`, all five legs green. THE PRODUCT HALF IS STILL OPEN AND IS STILL THE OWNER'S.*** 5161 says only *"Unable to change to new directory"*, with nothing about the group not yet being in the caller's token or a sign-out fixing it — and that is the sentence a real administrator hits after `create.account`, not a test. **The run carries its own non-decisive witness**: this session's `LOGTO` reports 5161 in the Control leg while the helper's succeeds, in the same transcript. ***RULED AND BUILT 28 Aug 2026 — "two accounts, as the door table says".*** The owner's choice between covering the door properly, dropping it, or fixing only the message. **The door pair now creates a HELPER account `<prefix>b` alongside the account under test, grants it into the account's `sdu_` group, and issues the `LOGTO` from inside the helper's own ssh session** — a fresh logon, so its token carries the group SID this session cannot. `verify-doors.ps1` runs the local `LOGTO` too and records it as a **NON-DECISIVE witness**, so the transcript carries the evidence for why two accounts are needed rather than a comment claiming it. ***UNRUN — it needs an elevated Create leg, so `-Run b52` is what tests it.*** **Costs a second profile directory per run** (35/36), and both names are now checked free before anything is created. **The PRODUCT half of this entry is untouched and still open**: 5161 still says only *"Unable to change to new directory"*, and that is the sentence a real administrator hits. ***CONFIRMED BY THE SUITE ITSELF, `-Run b51`, 28 Aug 2026 16:54, on a SECOND account — this is not a one-off.*** With the instrument honest the Control leg reported **2 of 7 decisive checks failed**, both of them the `logto` rows (*"entered the account"* expected True got **False**; *"did NOT report 5161"* expected False got **True**), while **ssh and the API both admitted** in the same leg — the three-door comparison inside one run, which is stronger evidence than either door alone. The suite then **stopped at the right place** (*"a door refused BEFORE the suspension, so its refusal after one would prove nothing"*) **and still ran `Remove`**, so nothing live was left behind. ***`LOGTO` authorises on the machine's group list and then fails the chdir on the token's, and says only "Unable to change to new directory"*** — an administrator who has just run `create.account` is in the new `sdu_<acct>` group **on the machine** but **not in their own token**, because Windows fixes group membership at logon. So `logto.authorised` (`CPROC:2679`) passes, the chdir at `:2691` is denied, and 5161 is all the user sees. **Measured 28 Aug 2026 with a control**: `Get-LocalGroupMember sdu_sddrb50a` → `GITORLI\don` **present**; the same live unelevated token → `sdu_sddrb50a` **absent** while `sdusers` (granted before a reboot) **present**, so the enumeration works and the absence is real. **The record already knew the mechanism** — PROJECT_STATUS §6 *"group membership is fixed in the token at logon"* — **but nothing connects it to this message.** 5161 is also `SETACC:67`. ***Owner's call, and there are three shapes***: say so in 5161 when the account was reachable but the directory was not; have `create.account` print the sign-out line it already prints elsewhere; or leave it. **It is also why 19's `logto` door cannot be measured from the creating session** — the door table in this file already specifies the cure, *"ssh as A and `LOGTO B`"* | `sdsys/gpl.bp/CPROC:2691`, `SETACC:67`, `sdsys/messages/5161` |
| ~~53~~ | **S** | ***THREE MORE DOCUMENT SETS STILL CARRIED `encrypt.field`, AND THEY WERE WRONG IN A DIFFERENT WAY FROM 52*** — found 28 Aug 2026 while closing 52, which corrected the **Testing** set only. These do not merely miscount it; they tell the reader **the verb is in an administrator's VOC and fails to load**, which stopped being true when PRE_RELEASE 25 removed it. ***CONFIRMED GONE TREE-WIDE***: absent from `newvoc`, from `voc_template` (426 entries — only the `encrypt` **keyword**, `211`, which is in the base 392 and is not a verb) and from `TIER.ADD.ADMINISTRATOR`. **Four places**: `Administrator/markdown/01-accounts-and-security.md:323-333`, a whole `## encrypt.field does not work in this release` section quoting the `$CRYPTO` load error; `User/markdown/95-sd-tcl-syntax.md:92`, a table row tiered **`A`**; and the two toolchain inputs that generate them — `tools/tcl-syntax-shapes.txt:81` and `tools/tclmap.py:128`, the latter mapping the verb onto Administrator/01, so the generator still expects that page to document it. ***ONE DECISION IS NEEDED BEFORE ANY EDIT AND IT IS THE OWNER'S***: `Administrator/markdown/01:333` is the **ONLY line in the entire documentation** that records field-level encryption as absent from W1.0-0 — measured by grepping `encrypt` across all four sets — so **deleting the section loses that fact**, while leaving it states a mechanism that no longer exists. Reword it to "not present, and the verb does not ship", or delete it and put the fact on a *not in SD Core* page. **Do not delete the shapes/tclmap rows without the same answer**: `95-sd-tcl-syntax.md` is generated, so an edit to the page alone is overwritten on the next render. *(`sdencrypt()`/`sddecrypt()` are unaffected and DO ship — this is the verb only.)* ***DONE 28 Aug 2026 ON THE OWNER'S RULING, "move to not in SD core".*** The section is deleted from `Administrator/01` and the fact is now `## Field-level encryption` on `Testing/markdown/14-not-in-sd-core.md`, which names `sdencrypt()`/`sddecrypt()` as the supported route and says plainly that nothing replaces the verb. ***AND IT WAS NOT COSMETIC — BOTH DOC GENERATORS HAD BEEN REFUSING TO RUN.*** `mktclsyntax.py` exited 1 on `NOT A VERB encrypt.field has a shape and is not on the roster` and `tclmap.py` on `NOT A VERB encrypt.field claimed by Administrator/01`, so **the TCL syntax card could not be regenerated at all** while the shapes file and the map still named it. **The roster is computed and had already self-corrected to 143**; the two typed lists had not, which is precisely the failure the computed roster exists to expose. Both now exit 0 — `roster 143 (standard 81, programmer 42, administrator 20)`, `tclmap 143 of 143, 0 exempt` — and that is an INDEPENDENT confirmation of 4 and 52's figures, from a tool that computes rather than quotes. `checklinks` 0 broken on all three sets (77/6/185) | docs repo, `Administrator/markdown/01`, `Testing/markdown/14`, `User/markdown/95`, `tools/` |
| 54 | **M** | ***`verify-profiledir.ps1` is in neither runner, so 36's last leg never fires again*** — the leg that had **never** fired before 28 Aug, which is why it could not be trusted and why the script was written. It scored **14 of 14** and then went nowhere: not in `VerifyInstall1`, not in `VerifyInstall2`. ***DECIDED 29 Aug 2026 — WIRE IT INTO `VerifyInstall2`***, the owner having said the verifier questions are mine. It needs **elevation**, so `VerifyInstall2` is the right runner and `VerifyInstall1` is not. **Its cost is lower than `verify-doors-suite`, which is already a suite step**: it creates one control account and deletes it, and it never logs in, so it leaves **no profile directory** — the thing that makes the doors fixture single-use and expensive. ***THE ONE THING THAT MUST NOT BE GOT WRONG: its `-Prefix` has to come from the `-Run` token***, as `sdacctb48`/`sdtiertb48` already do. It refuses a spent stem by design, so a fixed prefix passes once and fails on every later run on the same machine. Not started — verifier gap, not product | `gplbld/VerifyInstall2.ps1`, `gplbld/verify-profiledir.ps1` |
| ~~63~~ | **M** | ***DONE AND VERIFIED 29 Aug 2026 — `listf` NOW DESCRIBES ALL SIXTEEN, AND `$MAP` STILL READS `DH`, WHICH IS THE CONTROL.*** Measured on the **20:31:49** install with `assert-current` **exit 0 live** (*"no source file is newer than the install"*): the ten rows that printed a bare `F` now read `File - Spooler hold files`, `File - Account register`, `File - BASIC program source`, `File - Compiled BASIC object code`, `File - GPL BASIC program source`, `File - Compiled GPL BASIC object`, `File - System message texts`, `File - VOC given to a new account`, `File - Operating system users` and `File - Session IPC area`. **Zero bare type codes left in the column.** ***AND `-Run b67` IS GREEN IN BOTH HALVES ON THE SAME INSTALL***: `VerifyInstall1` every step exit 0, `VerifyInstall2` **19 of 19**, **655 `[PASS]` and zero `[FAIL]`** across 21 transcripts — so the twelve record changes broke nothing. *(Was: `listf` PRINTS A BARE `F` WHERE A DESCRIPTION BELONGS, ON TEN OF SDSYS'S SIXTEEN FILES.*** Measured 29 Aug 2026 on the live 18:55:20 install, from the `listf` output itself: `$hold`, `accounts`, `bp`, `bp.out`, `gpl.bp`, `gpl.bp.out`, `messages`, `newvoc`, `os.users` and `qfile` all show `F` in the **Description** column, while `$MAP`, `$ACC`, `SD.VOCLIB`, `dict.dict`, `syscom` and `voc` show real text. ***THE CAUSE IS A DELIBERATE FALLBACK MEETING A GAP, NOT A BUG IN EITHER HALF***: `voc.dic`'s `Description` item is `IF @ = '' THEN F1 ELSE @` over **NEWVOC**, so a file with no `newvoc` record falls back to **field 1 of the VOC record** — which in SDSYS's voc_template-derived VOC is the type code `F`. Nine of the ten have **no `newvoc` record at all**, correctly, because they are SDSYS-only files a new account never gets; `newvoc/newvoc` is the tenth and its field 1 is literally `F`. **So the fallback is doing what it says and there is simply nothing to fall back to.** ***COSMETIC, AND IT IS IN THE FIRST OUTPUT A NEW ADMINISTRATOR SEES***, which is why it is worth the ten records rather than nothing. **Two shapes were possible: give the ten a description, or make the fallback print empty instead of the type code.** ***THE FIRST IS BUILT*** — the second hides the gap everywhere it occurs, including in accounts, and a blank column teaches nobody what the file is. ***AND IT IS A LEGITIMATE FORM, NOT A SECOND MALFORMED RECORD — THE RECORD ALREADY SETTLED THAT AND IT WAS NEARLY MISSED A FOURTH TIME.*** `CPROC:1410` says the type code **may be followed by comment text with no intervening space** (the PI / PI-open / UniVerse rule), and HISTORY.md's *"the five malformed VOC_TEMPLATE entries were never broken"* is the correction that established it — after an UPSTREAM entry about those five had itself been **written and withdrawn**. **This session withdrew a second one over `$MAP` before finding that.** ***BUILT AND THEN VERIFIED 29 Aug 2026 — the cycle at 20:31:49, `b67`, and the `listf` above.*** Ten `voc_template` file records now read `File - …`; `edit` and `micro`, the last two of the section-8 five, are reduced to a bare `V`. **The invariant is asserted rather than assumed**: field 1's first character is what every reader takes (`CREATEA:1233`/`:1292`, `BASIC:201`, `FORMAT:79`, `PARSER:178`, `SPVIEW:103`, `CPROC`'s five `[1,1]`), all twelve still yield `F`/`V`, and the 392-of-392 newvoc agreement is unchanged. ***IT NEEDS A FULL CYCLE BEFORE ANYTHING CAN BE MEASURED*** — `assert-current` check B walks `sdsys` and these records are now newer than the install, so every verifier refuses until then. Found while closing 61, whose whole premise was a misreading of this same column.)* | `sdsys/voc_template/{$hold,accounts,bp,bp.out,gpl.bp,gpl.bp.out,messages,newvoc,os.users,qfile,edit,micro}` |
| 55 | **S** | ***`release.ps1` never runs the two doc generators that already refuse on a stale figure*** — measured 29 Aug 2026 by reading it: it calls `mkdoc.py` (:109), `mkpdf.ps1` (:126) and `checklinks.py` (:161), and **neither `mktclsyntax.py` nor `tclmap.py`**. Both of those compute the roster from the VOC and both **exit 1** when the typed lists disagree — which is exactly what they did over `encrypt.field`, undetected for a week, until 53 ran them by hand. ***So the guard already exists and nothing calls it.*** **Part one is nearly free: call both from `release.ps1` and fail the release when either refuses.** **Part two is the actual gap** — the generators check the typed *maps*, not the typed *prose*, so `mktclsyntax.py` printed `standard 81` in the generated card for a week while the tester set said `77` and nothing compared them. Have the generator emit its computed figures as data and assert the handful of labelled tier counts against it. **This is the guard called "the cheapest still available" in `a931c36`, now filed rather than left in prose.** Not started — docs toolchain | docs repo `tools/release.ps1:161`, `tools/mktclsyntax.py`, `tools/tclmap.py` |
| ~~59~~ | **S** | ***FIVE UNELEVATED VERIFIERS ASSUME AN ADMINISTRATOR LANDS IN AN ORDINARY ACCOUNT, WHICH 56 ABOLISHES*** — measured on `-Run b59`, 29 Aug 2026: unelevated **8 of 13**, and all five failures are one cause. `verify-lcnames` names it — *"the session is in the account, not SDSYS … [FAIL] WHO names the account"*. Also `verify-osusers`, `verify-nocase`, `verify-lineendings`, `verify-batchjob`. ***NOT PRODUCT DEFECTS: every one refused the null case out loud rather than scoring a false pass***, which is the instrument rule working on the first run that broke the assumption. **The fix is a real non-administrator test account for that half**, not a tweak to five scripts. ***`verify-nocase` IS GREEN ON `b61`, 3 of 3 — the first measurement this project has taken as a real non-administrator.*** ***DONE 29 Aug 2026 — ALL FIVE PASS ON `-Run b66`: UNELEVATED 13 OF 13, ELEVATED 19 OF 19, 1,106 `[PASS]` AND ZERO `[FAIL]`.*** Two were converted to a real non-administrator account (`nocase`, `lineendings`); **two needed no change at all** — `lcnames` (back to **142 of 142**) and `osusers` recovered the moment 56 clause 2 was reversed and an administrator landed in an ordinary account again; and `batchjob` was **re-aimed at SDSYS** on the owner's ruling, its row now reading `ELEVATED in SDSYS, no entry: still runs` **PASS, decisive** | `gplbld/verify-{lcnames,osusers,nocase,lineendings,batchjob}.ps1` |
| ~~61~~ | **B** | ***DONE 29 Aug 2026 — NOT A DEFECT. THE PREMISE WAS INVERTED, AND `newvoc` FIELD 1 IS A DESCRIPTION BY DESIGN.*** ***THE SYMPTOM DOES NOT REPRODUCE***: an elevated `listf` in SDSYS on the 18:55:20 install shows `$MAP` as **`DH`**, not `Err 30`, with both pathnames resolved. ***THE THREE FILES DO THREE DIFFERENT JOBS AND THE ENTRY COMPARED TWO OF THEM AS IF THEY DID ONE.*** **`voc_template` field 1 is the TYPE CODE and becomes SDSYS's own VOC** (`gplbld/stage.py:119`, `verify-lcnames.ps1:771` — both right; the "live reading appears to contradict" was the misreading). Live bytes agree: SDSYS's VOC holds `$MAP` `F` `@SDSYS/$map` `@SDSYS/$map.dic` (`sdsys/voc/%0`, offset 11280). **`newvoc` field 1 is the DESCRIPTION, AND ITS FIRST CHARACTER IS THE TYPE CODE.** ***`CREATEA:1233` REPLACES THE FIELD WITH ITS OWN FIRST CHARACTER*** — `rec<1> = if upcase(rec[1,1]) = 'P' then rec<1>[1,2] else rec[1,1]`, two characters for a `P` type, repeated at `:1292` for the administrator verbs. **So the description does not survive into an account's VOC, but its first letter is load-bearing**, and ***the invariant is measured: 392 of 392 `newvoc` first characters equal `voc_template`'s type code, 0 mismatches***, installed tree and source alike. *(An earlier pass here cited `CREATEA:1181` and said the field was simply dropped. **Both were wrong**: that comment is about the tier list records — `TIER.OMIT.STANDARD` field 1 reads `This record is not a VOC entry…` — and nothing about it concerns VOC descriptions.)* `don`'s live VOC carries the type code `F` and **zero** newvoc description text, which is question 2 of this entry answered. ***AND THE DESCRIPTION COLUMN IS A LOOKUP, NOT A FIELD READ***: `voc.dic`'s `Description` item is `IF @ = '' THEN F1 ELSE @` over **NEWVOC**, so `listf` shows newvoc's text when there is one and **falls back to field 1** when there is not — which is why ten SDSYS rows print a bare `F` where a description belongs. **That fallback is the only real wart here and it is filed separately as 63, `M`.** ***THE CONTROL THAT SETTLED IT***: neither `File for MAP output` **nor** `File - Vocabulary` appears anywhere in `sdsys/voc/%0` or `%1`, while `listf` displayed both — so the column cannot be reading the VOC record, and the first attempt to explain it from field 1 alone was measuring the wrong thing. **`Err 30` itself came from `FTYPE:54`/`:68` on a failed `openpath` of field 2, and field 2 is byte-identical in both copies, so field 1 was never a candidate cause.** ***WITHDRAWN UPSTREAM TOO*** — [UPSTREAM_FIXES.md](UPSTREAM_FIXES.md) carried the same false claim and was one step from being sent. *(Was: `newvoc/$MAP` HAS NO TYPE CODE, SO SDSYS'S VOC SHIPS ONE BROKEN FILE RECORD ON EVERY INSTALL — Field 1 reads `File for MAP output`, the description, where every other file record has **`F`**. `LISTF` in SDSYS reports it `Err 30` on the live install. Found 29 Aug 2026 while confirming entry 60's cleanup. Do not just paste the `F` in until that is answered.)* | `sdsys/newvoc/$MAP`, `sdsys/voc_template/$MAP`, `gpl.bp/CREATEA:1181` |
| 62 | **B?** | ***TRACED 29 Aug 2026: BOTH ROUTES INTO SDSYS NOW TEST THE PERSON BEFORE ANYTHING PROMPTS — SO THE HOLE IS CLOSED IN CODE, AND NOTHING TESTS IT.*** ***READ BY SOURCE, NOT RUN, AND THAT IS THE WHOLE REMAINING GAP.*** **Route 1, `LOGIN:568`**: `case kernel(K$ADMINISTRATOR, -1) and kernel(K$OS.ADMINISTRATOR, 0)` — the branch needs an **already-elevated session** AND an **administrator person**, and a standard user fails both, so `elevate('START')` at `:578` is unreachable to them; `LOGIN:558` records that it now prompts for nothing, `sd-elevate.ps1:119` short-circuiting when the token is already an administrator's. **Route 2, `CPROC:2634`**: an explicit `if not(kernel(K$OS.ADMINISTRATOR, 0))` refuses with **10002** and audits `LOGTO REFUSED account=SDSYS reason=not an administrator` — ***placed BEFORE `elevate('START')` deliberately***, its own comment saying a refusal after UAC has drawn its dialog *"has already asked a person for a password it was never going to accept"*. **`elevate('START')` has exactly two callers and those are both of them.** ***THE KEY IS THE RIGHT ONE***: `keys.h:201` — `K_OS_ADMINISTRATOR` is *"the PERSON, asked of Windows every time. Nothing in SD can set, clear or forge it, and a LOGTO does not move it"* — implemented at `op_kernel.c:457` as `IsAdmin() && (connection_type != CN_SOCKET)`, carrying `kernel.c:240`'s guard so an API session cannot answer TRUE spuriously. **The audit half follows: a non-administrator can no longer reach the credential prompt on either route, so the helper can no longer run as somebody `@logname` is not.** ***SEV STAYS `B?` AND THE ENTRY STAYS OPEN, BECAUSE COMPILING IS NOT RUNNING***: **no verifier covers this** — `10002`, `not an administrator` and `LOGTO REFUSED` return **zero hits across every `gplbld/verify-*.ps1`** — so the refusal is asserted by reading and by nothing else. **What would close it is a verifier driving a real non-administrator at both routes**, which PRE_RELEASE 59's `sdtestuser` machinery already builds. *(Was: RE-MEASURE WHETHER `elevate('START')` STILL ADMITS SOMEBODY WHO IS NOT AN ADMINISTRATOR — split out of **56** when that closed, so a measured finding is not lost because the code around it moved. As measured before clause 2 was reversed: `elevate('START')` gates on `Start-Process -Verb RunAs` succeeding and tests nobody's identity — that verb gives a standard user a *credential* prompt, so an administrator's password was enough to reach SDSYS, and `@logname` and `audit_message()` then named the standard user who did not consent.)* | `gpl.bp/LOGIN:568`, `gpl.bp/CPROC:2634`, `gplsrc/op_kernel.c:457` |
| ~~60~~ | **S** | ***DONE 29 Aug 2026 — VERIFIED, `after: 0`.*** All four records deleted with `DELETE VOC` (`1 record(s) deleted` each), and an independent `LISTF` afterwards found **no `SD*BP.OUT` records at all**. The original finding, and the verb that was wrong first time: Run elevated, `DELETE.FILE` answered *"Error deleting DATA portion"* + *"DICT part of file does not exist"* on all four and changed nothing; **`clean-deadvoc` reported FAILED**, its verdict being a second `LISTF` rather than SD's wording. ***`DELETE VOC <name>` IS THE VERB***: `DELETEF` removes a FILE and the file these records name is already gone — the very thing being cleaned up. From `gpl.bp/DELETE`: naming ids takes the `num.ids > 0` branch, so **neither prompt is reachable** and `NO.QUERY` is unneeded. **sysmsg 3221 `"%1 record(s) deleted"` prints unconditionally, so it is NOT a usable success anchor** — `0 record(s) deleted` is on the failure path. Both scripts use `DELETE VOC` now, and `verify-catgate`'s is **unconditional**, because the record outliving the directory *is* the defect. ***STILL OPEN: the four records are still there and the rerun is unrun.*** The original finding: ***`verify-catgate` LEAVES A DEAD VOC RECORD IN SDSYS ON EVERY RUN, AND THE CODE DOES THE THING ITS OWN COMMENT FORBIDS.*** `LISTF` in SDSYS now shows `SDCATGB59BP.OUT` **and** `SDCATGB60BP.OUT`, both `Err 30` — SDSYS's VOC naming a file that is not there — one per suite run since b59, and `b61`'s will make three. `Remove-Fixtures` ([verify-catgate.ps1:161](sdb_ai/sd64/gplbld/verify-catgate.ps1:161)) deletes `<ACCT>BP` **through SD** with `DELETE.FILE ... FORCE`, then removes `<ACCT>BP.OUT` with **`Remove-Item`** — while the comment directly above it says to use SD *"because CREATE.FILE also wrote a VOC entry … deleting the directory alone would leave SDSYS's VOC naming a file that is not there"*. The object file made by `BASIC $ctlFile $ctlName` has a VOC entry of its own and nothing deletes it. **Harness, not product** — but it pollutes SDSYS, it accumulates, and `verify-lcnames` reads `LISTF` | `gplbld/verify-catgate.ps1:161` |
| ~~58~~ | **B** | ***DONE 29 Aug 2026 — the `Administrator` set describes the built model (`01-accounts-and-security.md:44-47`): elevation is fixed when SD starts, and SDSYS is reached from an elevated terminal or the UAC prompt `logto sdsys` raises.*** ***THIS ROW WENT STALE WITH EVERY CHECKER GREEN***, because `check-stale-leads.py` compares this file against itself and **cannot see the docs repository** — read that repo before reporting on any row whose work lives there. *(Was: THE DOCUMENTATION DOES NOT DESCRIBE THE ACCESS MODEL THE PRODUCT NOW HAS*** — owner's instruction, 29 Aug 2026, raised as 56 and 57 were written. **Every set is affected**: administrators are elevated at login into SDSYS and have **no account of their own**, they **lose ssh**, a grant may go **down or sideways only**, and **SDSYS is never granted**. Two new messages, **10126** and **10127**. ***DO NOT WRITE IT FROM THIS ENTRY*** — 56 and 57 both have pieces still unsettled, and the docs repo is a **separate git repository** at `C:\Users\dmont\Projects\SDCoreWindowsDocs` *(renamed 29 Aug 2026 to match its GitHub repository — this row used to warn of "spaces in its path", which is no longer true)*. ***THE "BLOCKED" HALF HAS LIFTED, 29 Aug 2026***: 56 clause 2 and 57 are built, cycled and proved by `-Run b66` (unelevated 13 of 13, elevated 19 of 19). **What is left is a scope question, not a blocker** — 56's own remainder is the `elevate('START')` identity hole, which the documentation does not describe anyway. **Do it with 34 and 55, as this entry has always said.** Not started.)* | docs repo `User`, `Administrator`, `Testing`, `Technical` |
| ~~57~~ | **B** | ***DONE 29 Aug 2026 — built, cycled and proved by `-Run b66`, including the promotion report, its last piece.*** "Installed and unrun" was a testing gap, not outstanding work; no verifier covers `modify.account b programmer` stranding grants, which is a gap worth filling one day. *(Was: A GRANT MAY GO DOWN OR SIDEWAYS, NEVER UP — owner's rule, 29 Aug 2026.*** *"Standard accounts can not be given access to programmer accounts, programmer accounts can be given access to standard accounts. Only windows administrators can enter SDSYS, rights to SDSYS can not be granted."* ***THE TIER IS THE ACCOUNT'S AND IT IS BAKED INTO ITS VOC AT CREATION***, so entering a higher-tier account handed over its whole verb set — **+42 verbs** for a standard user entering a programmer account, on the computed roster. **WRITTEN, UNCOMPILED**: new `gpl.bp/TIERGATE` (`!tier_allows`), wired into `CPROC`'s `logto.authorised`, `GRANTA` and `MODIFYA`'s ADD arm; messages 10126 and 10127. ***CPROC's IS THE ONLY GATE THAT HOLDS*** — the grant is a Windows group membership, so `net localgroup` makes one without SD, and a tier can be raised after a legal grant with nothing revisiting the group. ***CYCLED 29 Aug 2026, AND THE LAST PIECE IS IN***: `MODIFYA`'s `promo.snapshot`/`promo.report` name the grants a promotion voided, measured across the register write rather than computed from the ranks; messages 10128 and 10129. **Installed and unrun**.)* | `sdsys/gpl.bp/TIERGATE`, `CPROC` logto.authorised, `GRANTA`, `MODIFYA` |
| ~~56~~ | **B** | ***DONE 29 Aug 2026 — the model as finally ruled is built, cycled and proved by `-Run b66`: the `sdusers` gate is uniform across all three tiers (`LOGIN:414`), the SDSYS case tests **elevation** rather than personhood (`LOGIN:568`), an unelevated administrator lands in their own account, and administrators keep ssh.*** ***ITS ONE REMAINDER IS SPLIT OUT AS ENTRY 62 RATHER THAN DROPPED*** — the `elevate('START')` identity hole was measured **before** clause 2 was reversed, and the reversal plausibly closes it, so it is re-filed to be re-measured rather than carried here as an open claim about a model that has since changed. *(Was: THE ADMINISTRATOR ACCESS MODEL, REWRITTEN — owner's ruling 29 Aug 2026, and it SUPERSEDES THREE RECORDED DECISIONS.*** ***READ CLAUSE 2's REVERSAL FIRST — THE MODEL BELOW IS NOT THE ONE THAT SHIPPED.*** For one morning administrators had **no account of their own** and were elevated **at login** into **SDSYS**; the owner reversed that the same day, and **the built model is the reversed one**: administrators KEEP a personal account, land in it when unelevated, and reach SDSYS by **two explicit routes** — starting SD already elevated, or `logto sdsys` from that account. They may `logto` anywhere and **take the rights of whatever account they move to**. ***THREE OF THE SEVEN CLAUSES WERE ALREADY THE CODE***, which is why PRE_RELEASE **31**'s 29 Aug ruling is withdrawn the same day. **Re-opens PRE_RELEASE 2** (a closed **B**). **Reverses 15 Aug 2026** (*"nobody logs in to an account but their own"*) **for the ELEVATED case only** — an unelevated administrator now lands in their own account, exactly as 15 Aug said. ***AND ADMINISTRATORS KEEP ssh***: the withdrawn model had taken it, and an ssh session is never elevated, so it lands in the personal account like anybody else's. ***A NON-ADMINISTRATOR CAN STILL REACH SDSYS***, measured and NOT yet fixed: `elevate('START')` tests nobody's identity, so an administrator's password is enough. BUILT AND CYCLED 29 Aug 2026; the suite is unrun.)* | `sdsys/gpl.bp/LOGIN:445`, `gpl.bp/CPROC:2597`, `gplsrc/linuxlb.c:88` |

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

## 4. Tester page 07 says a standard account has 77 verbs — **S** — ***DONE 28 Aug 2026, with 52***

It has **81**. `Testing/markdown/07-programmer-commands.md` opens with the
wrong number, and page **05** repeats it — *not* page 06, which carries the
administrator's `21` instead. Both were corrected in the same commit as 52;
the recipe and the diff are on that row.

**77 is a count of VOC records whose field 1 begins with `V`.** It misses the
four records that are a keyword *and* a verb — `break`, `count`, `display`,
`off` — whose fields 3 onward are a complete verb record. `CPROC:1718`
re-parses from field 3, so all four are typeable, and none is on
`TIER.OMIT.STANDARD`.

**Confirmed three ways.** `CREATEA:961`-`996` copies every `newvoc` record
except the two list records and, for a standard tier, the 42 omitted names —
with no filter on record type, so 123 − 42 = 81. SD's own VOC dictionary
encodes the same rule in its I-type `DISPATCH` field. And the verb total is
**143** — `81 + 42 + 20` — which is what `count voc with dispatch # ""` answers
in `SDSYS`.

***THIS PARAGRAPH SAID 144 AND `CA` 97 / `IN` 45 / `OS` 2 UNTIL 28 Aug 2026,
AND BOTH WERE STALE.*** Re-scanned from the tree that day: `voc_template` — the
source of `SDSYS`'s VOC — holds **139** records whose field 1 starts with `V`
(`CA` **95**, `IN` **42**, `OS` **2**) plus the four keyword-and-verb records =
**143**. `newvoc` holds **119** (`CA` 82, `IN` 37, no `OS`) plus the same four =
**123**. **The old figure was a count of `V` records ONLY, from a tree with five
verbs since removed**, and it was being quoted as the verb total, so it
disagreed with `81 + 42 + 20` by one and nothing noticed. *A number that
corroborates must be re-measured when the thing it corroborates moves.*

## 5. `.d name` cannot find a lower-case VOC record typed in upper case — **S** — ***DONE 28 Aug 2026***

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

## 10. Two verifiers carry a dead ANSI strip — **M** — ***DONE 28 Aug 2026***

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

## 11. Nested `commit` silently loses the outer transaction's writes — **B** — **DONE 29 Aug 2026**

***FIXED 29 Aug 2026 ON THE OWNER'S SEQUENCING.*** `end_txn_level()` is lifted
out of `rollback()` and called from `op_txncmt()` as well, so a commit leaves
the level it committed and a nested commit reinstates the parent instead of
abandoning it. **Both halves of the caution below are honoured**: `txn_depth`
and the `txn_stack` pop move together, so `system(1008)` did not become
trustworthy while the data-loss path stayed.

**Measured, not assumed** — `gplbld/verify-txn.ps1` on the 18:36:04 install,
**9 of 9**, `sd.exe` `4732ECF659E8DB40`:

| | before | after |
|---|---|---|
| the outer record's write | `base` — **lost** | **`outer`** |
| the inner record's write | `inner` | `inner` |
| `SYSTEM(1008)` delta over the pair | **+2** | **0** |
| `SYSTEM(1007)` after the inner commit | **0** — no transaction | **non-zero** — parent reinstated |

***THE CALL SITE IS BEFORE `exit_op_txncmt:`, DELIBERATELY.*** The three
`goto`s above it are write and delete failures that have already called
`k_error()`; the transaction is broken there and the level must not be popped
as though it had committed. **That leaves a separate, pre-existing gap which
this does not widen and does not fix**: on those error paths `process.txn_id`
was already zeroed at the top of the function, so `txn_abort()` and
`op_txnrbk()` both find nothing to roll back and the level stays counted. A
commit that failed half way needs a decision about the records already written,
not a decrement — **filed here rather than guessed at.**

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

## 13. `qselect` prints its message without the list number — **M** — ***DONE 28 Aug 2026***

**UPSTREAM_FIXES #21. Live in this tree, measured 26 Aug 2026** —
`gpl.bp/QSELECT:240` passes one argument to a two-parameter message, so every
successful `qselect` ends with a dangling *"select list "*. `NSELECT:112` two
files away supplies both and is the model. One line, and `tgt.list` is already
in hand on the line above.

Documented as a known blemish in the select-lists page so a reader does not go
looking for a list that is there.

## 14. `delete.file ... no.query` still prompts — **S** — ***DONE 28 Aug 2026***

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

## 15. `delete.index` will not match a lower-case index name — **M** — ***DONE 28 Aug 2026***

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

## 2. The installing user gets no `OS.EXECUTE` — **B** — ***RE-OPENED 29 Aug 2026, see 56***

***THE 26/27 Aug RULING IS SUPERSEDED BY THE OWNER'S ACCESS MODEL OF 29 Aug
2026 (entry 56), AND THE FIX BELOW IS NOW THE WRONG SHAPE — NOT MERELY
STALE.*** Two reasons, both structural:

1. `os.users` is keyed on **`process.username`**, the Windows login, which
   `LOGTO` never changes (`op_sh.c:167`). A listed administrator therefore
   keeps `OS.EXECUTE` in **every account they move to** — exactly what 56 says
   they must lose.
2. `grant.os.access` fires when an **ADMINISTRATOR-tier account** is created,
   ADOPT included. **56 abolishes the administrator's own account**, so there
   is nothing left for it to attach to.

**`os.users` itself is not dead** and must not be removed with this: it is
still how a *non-administrator* is granted the operating system, and the ACL
`gplbld/secure-osusers.ps1` puts on it is still the whole of the protection.
What is withdrawn is writing administrators into it. **The original entry
follows, unchanged.**

---

*(original, DONE 27 Aug 2026, kept for its measurements)*

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

## 19. The tier change and `SUSPENDED` compile but have never run — **B** — ***DONE 28 Aug 2026***

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

## 21. The write-once rule on `ACC$PRIOR.TIER` is unreachable — **S** — ***DONE 27 Aug 2026***

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

## 22. `create.account` says a password was not set and never says why — **M** — ***DONE 28 Aug 2026***

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

## 23. `term default` sets the minimum width, not the default — **S** — ***DONE 27 Aug 2026***

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

## 25. `encrypt.field` is in every administrator's VOC and `$CRYPTO` does not exist — **S** — ***DONE 28 Aug 2026***

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

## 26. `delete.file` *name* `no.query` prompts twice when the name is typed in lower case — **S** — ***DONE 28 Aug 2026***

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

## 27. `modify.account` *acc* `add`/`delete` writes no audit record — **M** — ***DONE 28 Aug 2026***

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

## 30. `verify-osusers.ps1` refuses on a fresh install — **S** (verifier, not product) — ***DONE 27 Aug 2026***

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

## 31. An elevated local session keeps OS.EXECUTE after LOGTO — **S** — ***DONE 29 Aug 2026***

> ***CLOSED BY `-Run b59`, 29 Aug 2026, AND THE TRANSCRIPT WAS READ RATHER THAN
> THE STEP'S EXIT CODE BELIEVED.*** `verify-apiadmin` **22 PASS / 0 FAIL /
> 0 SKIP**, and the line that matters:
>
> ```
> [PASS] control: local elevated session refused OS.EXECUTE: expected False, got False
> ```
>
> ***IT CLOSED WITH NO EDIT TO `verify-apiadmin.ps1` AT ALL.*** 56 stopped
> `CREATEA` writing administrators into `os.users`, so `os_permitted()` falls
> through to a lookup that finds nothing and refuses. The control was never
> wrong about what it wanted — the product had drifted from it.
>
> ***THE RECORDED "21/23" WAS WRONG IN THE DENOMINATOR, AND THAT IS MEASURED
> RATHER THAN ARGUED.*** b58's own log reads **21 PASS / 1 FAIL** — 22 checks,
> not 23, the single failing one being this control. Both runs have 22. **Carry
> 22/22 forward and treat any other number as news**; the old figure is
> probably PRE_RELEASE 40's wrapped-line double count.
>
> ***THE INSTRUMENT ALMOST FOOLED THE READING, TOO.*** These transcripts are
> **UTF-16**, so an ordinary `grep` for `[PASS]` matches nothing and reports
> **0 PASS / 0 FAIL** on a full log — which reads exactly like a step that did
> nothing. Convert first (`iconv -f UTF-16LE`) or read with `Get-Content`.

> ***READ THIS BEFORE THE REST OF THE SECTION. THE 29 Aug RULING BELOW IS
> WITHDRAWN*** — see entry **56**, taken hours later once the owner was shown
> what it cost. His replacement: *"if they logto another account, they have the
> rights of that account."* **`CPROC:2735` already does exactly that**, so the
> product is correct and the whole of this entry is one stale assertion in
> `verify-apiadmin.ps1:610`. **Sev B → S.**
>
> **DO NOT CHANGE THAT ASSERTION UNTIL 56 LANDS.** 56 moves `LOGIN`, and a
> control moved ahead of the product turns the suite green over a gate that is
> still in flight.
>
> ***WHAT SURVIVES THE WITHDRAWAL IS THE TRACE***, which was done for the old
> ruling and is what 56 is built on: the ssh and API doors are gated at
> connection time and a `LOGTO` cannot reach either; `sh` (`CPROC:3519`) is a
> **second** gate on the same flag that this entry never named; and `IsAdmin()`
> cannot be called without the `CN_SOCKET` guard. All of it is below and none
> of it depended on the ruling.

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
is stale** — same class as PRE_RELEASE 30. The API-side behaviour (refused) is
not in question and the headline hole stays closed.

### ***RULED 29 Aug 2026 — BEING AN ADMINISTRATOR IS THE GATE. IT IS A PRODUCT CHANGE.***

Put to the owner as a choice between *the `os.users` list is the gate* (making
this verifier-only) and *administrator status is the gate*. He took the second:

> *"Any administrator keeps universal rights, ssh, api, os.execute, no matter
> which account they logto. Permission belongs to the person, even if they logto
> an account with fewer priviledges."*

***THE CODE IS NARROWER THAN THAT TODAY, AND THAT GAP IS THE DEFECT.***
`os_permitted()` (`op_sh.c:150`) returns TRUE on `USR_ADMIN`, but `CPROC:2713`
**clears `USR_ADMIN`** on a `LOGTO` away from SDSYS, so the call falls through to
the `os.users` lookup keyed on the Windows login. **An administrator with no
`os.users` record is therefore REFUSED after a `LOGTO`.** `don` is admitted only
because PRE_RELEASE 2 listed him — the passing case is an accident of that
entry, not the rule the owner has now stated.

| what the ruling requires | where |
|---|---|
| administrator status survives a `LOGTO` for `OS.EXECUTE` | `gplsrc/op_sh.c:150` — check administrator status directly, **or** stop `CPROC:2713` clearing `USR_ADMIN` |
| the same for the ssh and API routes | ***TRACED 29 Aug 2026 — NEITHER IS REACHABLE AFTER A `LOGTO`, SO NEITHER NEEDS A CHANGE.*** See the trace below |
| ***and the same for `sh`, which this entry did not name*** | `CPROC:3519` — a **second** gate on the same flag. Found by the trace below |
| the control in `verify-apiadmin` follows the product | `gplbld/verify-apiadmin.ps1` — it must assert the new rule, not the old one |

### ***THE SSH AND API ROUTES, TRACED 29 Aug 2026 — READ THIS BEFORE WRITING THE FIX***

The entry required this before choosing where the fix goes. **Both doors are
gated at CONNECTION time, on the Windows account, before any `LOGTO` exists —
so a `LOGTO` cannot take either away and the ruling's ssh and API halves are
already satisfied by the product.** Traced from source, not run:

| door | the gate | keyed on | does `LOGTO` reach it? |
|---|---|---|---|
| **ssh** | `sshd_config AllowGroups sdssh`, then `LOGIN:427` *(own account only)* and `LOGIN:477` *(not SUSPENDED)* | the Windows login, at connection | **No.** Every ssh connection re-runs `LOGIN` from scratch |
| **API** | `APISRVR:1463` `is_grp_member(scram.user,'sdapi')`, inside the SCRAM handshake | the SCRAM-authenticated **account** | **No.** The gate is spent before `vb.account` can move anywhere |
| **`os.execute`** | `op_sh.c:161` `USR_ADMIN`, else `os.users/<process.username>` field 2 | the session flag | ***Yes — this is the defect*** |
| **`sh`** | `CPROC:3519` `K$ADMINISTRATOR`, else `os.users` field 1 | the same session flag | ***Yes — and the entry did not name it*** |

***SO THE PREFERENCE IN POINT 1 BELOW STANDS, BUT IT IS TWO SITES AND NOT
ONE.*** `sh` and `OS.EXECUTE` are separate gates reading the same flag:
`os_permitted()` returns TRUE on `HDR_INTERNAL` (`op_sh.c:158`), and CPROC is
`$internal`, so the `sh` verb never reaches the C test — `CPROC:3519` is its
whole gate. Fixing `op_sh.c` alone leaves `sh` refused after a `LOGTO`.

***`IsAdmin()` CANNOT BE CALLED HERE WITHOUT THE `CN_SOCKET` GUARD, AND THAT IS
THE REGRESSION THIS ENTRY'S OWN TEST EXISTS TO CATCH.*** `IsAdmin()`
(`linuxlb.c:88`) asks `getpwuid(getuid())` — the **real** uid. An API session is
`fork()`ed by the LocalSystem service, and `AssumeUserIdentity()`
(`win32s4u.c:178`) changes only the **effective** uid, so `getuid()` stays
SYSTEM and `IsAdmin()` answers TRUE for every remote client. **That is the
identical shape of the 21 Aug hole `kernel.c:240` fixed** — `IsElevated()` was
true for every API session for the same reason — and its guard,
`connection_type != CN_SOCKET`, is what any new test has to carry too.

***AND THERE IS A THIRD CONSEQUENCE THE RULING DOES NOT NAME: THE ONWARD
`LOGTO` IS REFUSED.*** `logto.authorised` (`CPROC:3752`) passes on
`K$ADMINISTRATOR`, which `CPROC:2735` has just cleared — so the hop after the
first one falls through to the `sdu_` group test on `@logname` and is refused
unless the administrator was granted. Recoverable by `LOGTO SDSYS` again, at the
cost of a second UAC prompt per hop. **Not filed as a change**: the ruling names
ssh, api and os.execute, and this is none of them. Flagged because the fix's
shape decides it either way.

***THE BLAST RADIUS OF *NOT* CLEARING THE FLAG, COUNTED.*** Five more readers,
all of which would change meaning: `op_sys.c:480` (`system(1050)`),
`CPROC:2410` (`break on user`), `CPROC:3107` (`logout all`), `CPROC:3133`
(`logout` another user's process), `CPROC:3351` (`pdump` another user's
process). **That is the argument for point 1 below, and it is now measured
rather than asserted.**

***TWO THINGS TO SETTLE BEFORE WRITING THE FIX, AND NEITHER IS RULED.***

1. ***`USR_ADMIN` GATES MORE THAN `OS.EXECUTE`, SO THE BLAST RADIUS IS NOT
   `op_sh.c`.*** `CPROC:2713` clears it on the stated principle that
   *"administrator rights belong to SDSYS"*, and PRE_RELEASE 20 (a suspended
   administrator) and the door work both stand on that line. **Not clearing it
   is the smaller diff and the larger change.** Checking administrator status
   inside `os_permitted()` touches one gate and leaves the principle intact —
   **prefer that unless the ssh/API halves say otherwise.**
2. ***`os.users` DOES NOT BECOME DEAD.*** The ruling adds administrators; it
   removes nothing. A non-administrator listed in `os.users` keeps
   `OS.EXECUTE`, and the ACL that `gplbld/secure-osusers.ps1` puts on that file
   is still the whole of the protection (`op_sh.c:145`).
3. ***ADDED 29 Aug 2026 BY THE TRACE ABOVE, AND IT IS THE OWNER'S — WHERE DOES
   ADMINISTRATOR STATUS COME FROM?*** The two answers are not the same change
   and one of them widens the product well past a `LOGTO`:
   - ***(a) STICKY ON ELEVATION — RECOMMENDED.*** A companion flag set beside
     `USR_ADMIN` at `CPROC:2723` (entering SDSYS, which is the only thing that
     obtains privilege) and **not** cleared at `CPROC:2735`. It means *"this
     session proved administrator status"*, so the rule becomes **you do not
     lose `OS.EXECUTE` by moving** — which is what the ruling says in the words
     it says it in: *"keeps ... no matter which account they logto"*.
     **It widens nothing at login.**
   - **(b) Seeded at login** from `IsAdmin() && connection_type != CN_SOCKET`.
     ***This grants every Windows administrator `OS.EXECUTE` OVER ssh WITHOUT
     ELEVATING, which they cannot get today*** — `CPROC:2598` refuses `LOGTO
     SDSYS` on ssh by design, because UAC has no desktop there (5.6.2). It is a
     bigger change than the defect, and it is not what "keeps" means.

   **Under (a) an administrator who never entered SDSYS is still refused — and
   that is correct, because they were refused before the `LOGTO` too, so
   nothing was lost.**

***AND THE API SIDE IS UNAFFECTED — CHECK THIS HOLDS WHEN THE FIX IS WRITTEN.***
A remote API session is refused because its `process.username` is the *account*
(`sdapiab48`), and an account is not a person and is not an administrator. **The
ruling is about administrators, so it must not reopen the hole `verify-apiadmin`
exists to catch.** That is the regression test for this entry.

***AND THE CONTROL'S NEW WORDING DOES NOT DEPEND ON WHICH OPTION IN 3 IS
TAKEN*** — traced 29 Aug 2026, so it is settled ahead of the ruling. The
control's session reaches the account **through SDSYS**, so it has proved
administrator status under (a) and under (b) alike:
`verify-apiadmin.ps1:610` inverts from `expected False` to **expected True**,
and its comment at `:602` — *"gives the flag up on the way out"* — becomes the
description of the defect rather than of the design. ***DO NOT CHANGE IT
FIRST.*** A control moved ahead of the product turns the suite green over a
gate that is still wrong, which is the false verdict §"An instrument shows what
it DID" exists to stop.

**Left behind by that run** (normal — the next `cycle.ps1` clears them): the
`b48` verifier accounts `sdacctb48`, `sdtiertb48*`, `sdrtb48*`, `sdtapib48*` and
three `os.users` records for the ADMINISTRATOR-tier ones the tier verifiers make.

---

## 32. `delete.account` leaves the ProfileList entry, so a recreated account gets a different home — **S** — ***DONE 27 Aug 2026***

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

## 33. `allow-ssh-groups.ps1`'s own usage text omits the switch it requires — **S** — ***DONE 27 Aug 2026***

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
the docs `README` are the only route. **Do not settle it by adding a link.**

### ***RULED 29 Aug 2026 — A SET MAY DECLARE ITSELF LINK-FREE***

Put to the owner as three ways out: a per-set declaration, `release.ps1`
passing every zero-link set, or leaving `Technical` on its two hand steps. He
took the first.

***THE GUARD IS NARROWED BY DECLARATION, NOT REMOVED.*** `checklinks.py` gains
an explicit way for one set to say *this set legitimately has no links*, and
`release.ps1` accepts it. `Technical` opts in. **`User` (33 pages),
`Administrator` (3) and `Testing` (15) keep the zero-link refusal**, so a set
that loses its links to a bad edit still fails loudly — which is the whole
value of `checklinks.py:57` and the reason the second option was not taken.

**Shape notes for whoever builds it**, none of them ruled:

- **The declaration belongs to the SET, not to the invocation.** A
  `-AllowNoLinks` switch on `release.ps1` would be typed by whoever is running
  it, which is the person least placed to know — and it would silence the guard
  on any set they aimed it at. Put it where the set is described.
- **It must be visible in the output.** `checklinks.py` should say it read the
  declaration and is passing a zero-link set *because of it*, per the instrument
  rule — a set that goes quiet is indistinguishable from a set that broke.
- **Keep it honest against its own reason for existing.** If `Technical` ever
  gains a real cross-reference, the declaration should not then hide a broken
  one: a declared set with links found should check them normally.

Until then, `Technical` renders with:

```
python tools\mkdoc.py --in Technical\markdown --out Technical\html --product "SD Core for Windows" --version W1.0-0
powershell -File tools\mkpdf.ps1 -In Technical\html -Out Technical\pdf
```

and the `README`'s markdown-against-PDF loop is what proves nothing is stale.

## 35. A profile DIRECTORY left behind moves the next account's home, exactly as the registry entry does — **S** — ***DONE 28 Aug 2026***

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

## 36. Deleted accounts leave their registry hives mounted, and nothing SD does can unmount them — **M** (owner's call) — ***DONE 28 Aug 2026***

***BUILT 28 Aug 2026. ALL FOUR RULINGS, AND NOT ONE OF THEM HAS BEEN RUN —
NO CYCLE HAS COMPILED THE BASIC AND NO SERVICE HAS STARTED THE SWEEP.*** It is
recorded as built rather than done for exactly the reason §0 gives: compiling
is not running, and none of this has even compiled.

| ruling | where it landed |
|---|---|
| keep BOTH halves, directory first | `gpl.bp/DELETE_USER` — `$dirleft` decides whether the `ProfileList` entry is touched at all |
| record the SID as SD's to reclaim | same file — one file per SID under `C:\ProgramData\SD\profile-reclaim`, naming the SID, the account and the DIRECTORY |
| SD's own sweep at service start | `gplbld/reclaim-profiles.ps1`, run by `gplsrc/sdsvc/sdsvc.c` before `sd -start`. Best effort, bounded wait, its own log |
| `create.account` REFUSES and names the directory | `gpl.bp/CREATEA` via the new `gpl.bp/PROFILE_DIR`, messages 10124 and 10125 |
| no restart in the delete path | nothing was added; 10075 now says the next restart clears it rather than asking for one |

**Statuses and messages.** `!delete_user` gains **8** — *left behind AND not
recorded* — beside 6 and 7, because 6's new message promises a reclaim and that
promise must never be printed about a pair nothing is coming back for.
**10075 rewritten** (a third time, as this entry predicted), **10116
rewritten**, **10123 / 10124 / 10125 new**.

***THE SWEEP READS THE RECORD, NOT `ProfileList`***, which is what this entry's
own 28 Aug measurement demanded. It also refuses a record it cannot vouch for,
and the refusal table is a **pure function** so it can be tested without a
store, a reboot or an elevated token: `gplbld/test-reclaim-units.ps1`, **39
passed / 0 failed**, and its **positive control** — the same test against a copy
with the containment check deleted — **fails 34/5 on exactly the five
containment rows**. The sweep was also watched running in `-List` mode against
a planted store: two records, both refused by name on the owner control, exit 1;
an absent store says so and exits 0; an unelevated sweep refuses and exits 2.

***THE STORE HAS AN ACL OF ITS OWN AND THAT IS NOT TIDINESS.***
`C:\ProgramData\SD` grants `sdusers:(OI)(CI)M` to everything underneath, so a
reclaim store left to inherit would be **a list of directories every SD user
can edit and LocalSystem later deletes** — the same shape as the SDSYS\PSTMP
escalation in `PS_SCRIPT`'s header. `gplbld/secure-reclaim.ps1` creates it with
inheritance broken at install time (so no SD user can create it first and own
it), `DELETE_USER` does the same if it is missing on an older tree, and the
sweep re-asserts it every boot **and** skips any record not owned by SYSTEM or
Administrators.

***AND 32'S REGRESSION TEST IS RE-SCOPED, AS THIS ENTRY SAID IT WOULD HAVE TO
BE.*** `verify-delaccount.ps1` step 3 asserted *"the ProfileList entry is
gone"*, which now scores the correct keep-both behaviour as a failure. It
branches on the state actually reached: both halves gone, or both halves kept
**and recorded**, with the record's `directory=` line read back and 10075
asserted present / 10123 asserted absent. **10123 is on `$needMsgs`**, because
it is asserted absent and an unreadable message would have scored that as a
pass.

**What is NOT built, and is not in the ruling either:** nothing sweeps a
directory that was orphaned before this existed — the three `sdapi*b49` folders
and the two dozen the b52/b53 suite runs left. Those are still
`cleanup-devlitter.ps1`'s job, and PRE_RELEASE 41 is the entry about that
script's own blindness.

***AND IT PUTS THE DOCS OUT BY TWO.*** `Technical/02` The Installed Scripts
covers *"all 26 that ship"*; `secure-reclaim.ps1` and `reclaim-profiles.ps1`
make it **28**. Nothing in this repository asserts that count, so nothing here
will catch it — it is H.2's, in `SDCoreWindowsDocs`.

*(The ruling table and the evidence below are unchanged, and are what the above
was implemented against.)*

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

## 37. `create.account` says "may sign in over ssh" twice, about two different things — **S** — ***DONE 28 Aug 2026***

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

## 38. The suite does not test SUSPENDED on any door — **M** (verifier gap, not product) — ***DONE 28 Aug 2026***

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

## 39. Uninstalling strips SD's ssh confinement and leaves every account it created — **B** (ruled 29 Aug 2026)

Found 27 Aug 2026 from the question *"will the released system leave litter
behind?"*.

***THIS SECTION SAID "REASONED FROM SOURCE, NOT MEASURED" FOR A DAY AFTER IT WAS
MEASURED*** — corrected 29 Aug 2026. The row has carried the measurement since
28 Aug: `cycle.ps1` uninstalled and deleted both trees at 15:29:59, `sddrb50a`'s
`ACCOUNTS` record went with the data tree, and **the Windows side did not
move** — still enabled, still in `sdusers`, `sdssh` and `sdapi`, with
`sshd_config` still carrying `AllowGroups sdssh`. **The account outlived the SD
installation that made it and is now unremovable by SD**, because
`DELETE.ACCOUNT` cannot reach an account with no `ACCOUNTS` record. Read the
row; the analysis below is the original reasoning and the measurement confirmed
it.

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

### ***RULED 29 Aug 2026 — OPTIONS 1 AND 2 TOGETHER, AS A SECOND SEPARATE PROMPT***

> *"A second separate prompt, however deleting the windows accounts should not
> delete the account of the person doing the installation so that there is at
> least one remaining account that can log into windows."*

***FIRST, A CORRECTION TO THE PREMISE THE RULING WAS ASKED ON.*** The owner
described the choice as one an **upgrade** already offers — *"deletion happens
before the re-install phase and the user is given the option of retaining
accounts and the configuration file or deleting them"*. **There is no such
upgrade-time prompt.** An upgrade replaces the shipped half of the data tree in
place and asks nothing (`sd.iss:374`, the generated `upgrade.iss`). The prompt
he is describing is on **uninstall** — `sd.iss:3482`, *"Remove the SD database
as well?"*, defaulting to No — and its wording *"EVERY SD account, every
password ... and your configuration file"* means the SD-side records under
`C:\ProgramData\SD`. **It deletes no Windows account**, which is exactly this
entry. The ruling stands on the corrected premise: he wants that same shape of
choice extended to the Windows accounts.

| | |
|---|---|
| **`sd.iss:3482` is unchanged** | *"Remove the SD database as well?"*, still defaulting to No |
| **A second question follows it** | about the Windows accounts SD created, with their `sdu_`/`sdg_` groups and profiles. Also defaults to keep |
| ***The installing user is excluded BY CONSTRUCTION*** | not by the operator noticing, and not by a warning. **At least one account must still be able to sign in to Windows** |
| **The closing disclosure is fixed with it** | it names the database, the ssh server and `sdusers`, and never mentions the accounts — wrong whichever way the prompt is answered |

***THE EXCLUSION IS THE PART TO GET RIGHT, AND IT IS NOT MERELY "SKIP
`{username}`".*** `sd.iss:86` already records that `{username}` is whoever
authenticated the UAC prompt, which need not be the person signed in. **Decide
what "the installing person" resolves to before writing the sweep**, and make
the uninstaller **say which account it is keeping**, so a wrong answer is
visible rather than discovered at the next sign-in. The instrument rule applies
to an uninstaller too: it must print what it removed and what it kept.

***AND IT MUST REFUSE THE NULL CASE.*** If the sweep would remove every account
that can sign in to Windows, it must stop and say so rather than proceed —
that is the failure the ruling exists to prevent, and it is the one case where
the prompt's answer is overridden.

**Sev resolved `B?` → `B`**: the ruling requires a change to the uninstaller, so
it is work that must land before W1.0-0 rather than a question about whether to
do any.

### ***BUILT 29 Aug 2026 — AND THE `-Remove` PATH IS UNEXERCISED. READ THAT BEFORE TICKING IT.***

**New shipped script `gplbld/remove-sdaccounts.ps1`** (in `stage.py`'s list, so
**NOT** on `$neverShipped`), a second prompt in `sd.iss`, and the closing
disclosure fixed with it.

***WHAT "THE INSTALLING PERSON" RESOLVES TO — SETTLED, AS THE ENTRY ASKED.***
It resolves to **`{username}` at UNINSTALL time**, passed as `-Keep`. The
installer's identity is **not** persisted and deliberately so: an uninstall may
happen years later, run by a different administrator, and an account recorded at
install time may not exist any more — an exclusion naming a deleted account
protects nobody. **The owner's purpose clause is the real requirement** —
*"so that there is at least one remaining account that can log into windows"* —
so that is implemented as a property to check rather than an identity to trust.

| guard | behaviour |
|---|---|
| candidate set | **`sdusers` membership only.** `CREATE.ACCOUNT` adds every account it makes and nothing else does, so the group *is* the list SD created — structural, not a name test |
| `-Keep` missing or unmatched | **refuses, exit 2.** The exclusion is meant to hold by construction, so an unnamed keeper means the construction did not happen |
| would remove the last local administrator | ***refuses the whole sweep, exit 2 — and this overrides a Yes at the prompt*** |
| not elevated | refuses at the act step |
| the prompt | names the account it is keeping **in the question**, so a wrong answer is visible before it acts |
| the report | logged to a file, named back to the user, listing removed and kept |

***MEASURED — THE READ-ONLY HALF ONLY.*** Report mode on this machine:
candidates `b48adm`, `sdsshb55`, `test1`; `don` kept by `-Keep`; administrators
that would remain `Administrator`, `bkupuser`, `don`. All three refusals fired
(`-Remove` with no `-Keep`; `-Keep nosuchuser`; and the elevation gate). **The
gate ordering was checked statically** — every refusal precedes every write, the
first write being 20 lines below the last gate. The `cmd /c` quoting and log
redirection were exercised for real in report mode.

***WHAT HAS NOT BEEN RUN, AND CANNOT BE HERE:***
- **the `-Remove` path.** Nothing has actually been deleted.
- **the last-administrator refusal**, which cannot be provoked on a machine
  with administrators outside `sdusers`.
- ***the prompt itself. `cycle.ps1` uninstalls `/VERYSILENT`, so `UninstallSilent`
  short-circuits before it*** — and `cycle.ps1:486` records the harder half:
  **"an uninstaller fix cannot be verified in the cycle that ships it"**, because
  `unins000.exe` is generated at INSTALL time. This change reaches an uninstaller
  only at the *next* install.

***SO IT WANTS THE VirtualBox RIG (task 7.2), NOT THIS MACHINE.*** A real
interactive uninstall that deletes accounts should not be exercised where the
accounts matter. **Do not tick this entry until it has been.**

**One trap paid for**: `sd.iss` grew a line starting with `#13#10`, which ISPP
reads as a preprocessor directive — the exact thing that file's own comments
warn about twice. `cycle.ps1`'s guard caught it and named the line.

## 40. A verifier's transcript swallows the verifiers that run after it — **M** (verifier, not product) — ***DONE 28 Aug 2026***

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

## 41. The cleanup sweep reports "every section reached zero" on a machine that still has orphan directories — **M** (dev tooling, not product) — ***DONE 28 Aug 2026***

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

---

## 49. `reclaim-profiles.ps1 -List` reports "0 records" when it is merely not allowed to read the store — **S** — ***DONE 28 Aug 2026***

***RENUMBERED FROM 42, 28 Aug 2026.*** It was filed as 42 on the day, and 42 was
already taken: the index table has carried rows to **48** since before this
session while the detail sections stopped at 41, so a new entry written from the
sections alone collided with a table row describing a different defect. 43 and
45 went the same way and are now 50 and 51. **Read the table, not the section
headings — it is the index.**

***FIXED AND MEASURED ON THE INSTALLED TREE, same command, same machine, ninety
minutes apart.*** `-ErrorAction SilentlyContinue` replaced by a `try/catch` that
refuses and exits 2. Unelevated `-List`, 21:48:22:

```
reclaim-profiles: CANNOT READ the store at C:\ProgramData\SD\profile-reclaim - Access to the path ... is denied.
reclaim-profiles: this is NOT an empty store - nothing was measured and nothing was changed.
```

against the same command's earlier *"0 records in the store - nothing was left
behind to reclaim"* on a store that held five. **Left open by this fix:**
`reclaim-profiles.ps1:119` still states the intent that `-List` needs no
privileged token, and the store's ACL still makes that impossible. Granting
`Users` **read** would honour the comment and keep write to Administrators; it
would also expose deleted account names. Not filed as its own entry pending the
owner's view.

*(Sits outside the `## DONE` block above; move it there at the next tidy.)*

Found 28 Aug 2026 running the documented STEP 4 command from §START HERE
unelevated, as that step says to, immediately after a `-Run b56` suite that had
left thirteen profile directories on the machine. The tool said the store was
empty. It is not — `DELETE.ACCOUNT` had printed 10075 for both door accounts
minutes earlier.

***THE MEASUREMENT THAT SHOWS IT IS NOT AN EMPTY STORE.***
`verify-doors-admin-remove-20260828-205440.log`:

```
| Note: the Windows profile for SDDRB56B could not be removed yet, and SD has kept it.
| Note: the Windows profile for SDDRB56A could not be removed yet, and SD has kept it.
```

So the keep-both path fired twice and the pairs should be recorded. `-List`
unelevated:

```
reclaim-profiles: 0 records in the store - nothing was left behind to reclaim.
Nothing was measured and nothing was changed.
```

***THE CAUSE, AND IT IS ONE FLAG.*** `reclaim-profiles.ps1:271`:

```powershell
$records = @(Get-ChildItem -LiteralPath $Path -File -ErrorAction SilentlyContinue)
```

`secure-reclaim.ps1` grants the store to SYSTEM and Administrators **only** —
that is the whole point of it, and it is right. So an unelevated enumeration
throws `UnauthorizedAccessException`, `SilentlyContinue` swallows it, `$records`
is empty, and line 276 announces the **empty-store** interpretation as fact:
*"nothing was left behind to reclaim"*. **An unelevated `-List` cannot ever
report anything else**, on any machine, however full the store is.

***THE NULL-CASE GUARD IS PRESENT AND STILL DID NOT CATCH IT.*** The comment
above line 275 says the empty case must not read as *"swept everything"*, and
it does refuse out loud. **It refuses the case it can see.** Two different
states — nothing recorded, and not allowed to look — arrive at line 271 as the
same empty array, and the message picks one of them. This is the instrument
rule's rule 3 in the shape where the check exists and is aimed at the wrong
question: not *"did I find nothing?"* but *"could I have found anything?"*

**THE FIX IS THE CLASS, NOT THE FLAG.** Drop `SilentlyContinue`, catch the
enumeration, and **refuse** — exit non-zero with the reason — rather than
report a count. The sweep path at line 123 already knows how to say *"NOT
ELEVATED ... Nothing was attempted"*; `-List` needs the same sentence for the
same reason. A readability probe before the count would also do it.

**AND THE DOCUMENTATION IS WRONG WHEREVER THIS IS DESCRIBED.** §START HERE's
STEP 4 says *"UNELEVATED is enough for both"*. It is enough for the log; it is
never enough for `-List`, and following it as written scores a false pass on
the one step that was supposed to prove PRE_RELEASE 36 works. Correct that in
the same commit as the fix.

**Not fixed on the spot, deliberately.** The script ships, so editing it would
have voided the 20:48:24 install before the reboot that tests the sweep could
be spent. Measure first, then fix, then cycle.

---

## 50. The reclaim sweep refuses every record `DELETE_USER` will ever write — **B** — ***DONE 28 Aug 2026*** *(renumbered from 43; see 49)*

***FIXED ON THE OWNER'S RULING (option 2: drop the per-file owner check, rely on
the store's ACL) AND MEASURED END TO END.*** `Get-RefusalReason` lost the
`$ownerSid` parameter; the owner is still read and logged as evidence. The ACL
is asserted by the sweep itself at every boot — `/inheritance:r`, SYSTEM and
Administrators only — before a record is read.

| | |
|---|---|
| units | **39/39** |
| control, `-Sweep` at the pre-43 copy | **37/2**, red on the two new rows alone |
| `-List` elevated, before the reboot | `5 considered, 0 reclaimed, 5 still pending, **0 refused**` (was `5 refused`) |
| sweeps at 21:41–21:45, hives still up | `still pending - the record is kept for the next start`, `UsrClass.dat ... used by another process` |
| **sweep after the restart, 21:51:50** | **`5 considered, 5 reclaimed, 0 still pending, 0 refused`** |
| containment | `C:\Users` `sd*` **61 → 56**, `ProfileList` `sd*` **46 → 41**, and by exactly those five |

**The pre-reboot rows are the part worth keeping**: they drove the *keep and
retry* path, which no unit test can reach and which only exists because the
hive is still mounted. Kept, retried, reclaimed — the whole design, observed.

**The containment number is not in the tally line.** 56 of the 61 directories
had no record and had to be untouched; only counting the directory before and
after says so. A sweep that deleted more would still have printed
`5 reclaimed, 0 refused`.

*(Sits outside the `## DONE` block above; move it there at the next tidy.)*

Found 28 Aug 2026 by running `-List` **elevated** after entry 49 showed the
unelevated form could not see the store. **This is the whole of 36's sweep, not
an edge case: as built it can never reclaim anything.**

***THE MEASUREMENT.*** `C:\Program Files\SD\reclaim-profiles.ps1 -List`,
elevated, 21:15:00, on the 20:48:24 install after `-Run b56`:

```
reclaim-profiles: 5 record(s) to consider
    sid=...-2989 account=SDDRB56A  directory=C:\Users\sddrb56a  owner=...-1001
    REFUSED: owned by ...-1001, not SYSTEM or Administrators.
    [ and identically for SDDRB56B, SDAPIAB56, SDAPINB56, SDAPIIDB56 ]
reclaim-profiles: 5 considered, 0 reclaimed, 0 still pending, 5 refused
```

**Five genuine records, written by `DELETE_USER` itself, and five refusals.**
`...-1001` resolves to **`GITORLI\don`** — a member of `Administrators`, and
the very administrator whose elevated session issued `DELETE.ACCOUNT`.

***THE CAUSE IS A WINDOWS OWNERSHIP FACT, NOT A BUG IN THE RECORDS.***
`reclaim-profiles.ps1:176`:

```powershell
if ($ownerSid -ne 'S-1-5-18' -and $ownerSid -ne 'S-1-5-32-544') {
```

Its comment reads *"An ordinary user wrote it."* **He is not an ordinary
user.** A file created by an elevated process is owned by **the creator's own
SID**, not by `BUILTIN\Administrators` — that has been the default since the
`System objects: Default owner for objects created by members of the
Administrators group` policy began defaulting to *Object creator*. And
`DELETE_USER` runs in whatever session ran `DELETE.ACCOUNT`, which is an
administrator's session. **So the producer can never satisfy the consumer's
check**, on any machine, in the ordinary case.

***WHY 39/39 AND A POSITIVE CONTROL DID NOT CATCH IT, WHICH IS THE PART WORTH
KEEPING.*** `test-reclaim-units.ps1` drives the **refusal table** and proves a
*planted* record is refused by the owner control. Its positive control removes
the **containment** check — a different check — and correctly fails 34/5. **No
test ever asserted that a record `DELETE_USER` actually wrote is ACCEPTED**,
because until 21:15 today no such record had ever existed. The suite tested
every way in which the guard says no, and never the one path where it must say
yes. *A test that only exercises the refusals is a test that passes when the
feature does nothing.*

***AND THE END-TO-END TEST WOULD HAVE SCORED IT GREEN.*** §START HERE's pass
wording is *"ends `N considered, N reclaimed, 0 still pending, 0 refused`"*.
The run above ends `5 considered, 0 reclaimed, 0 still pending, 5 refused` —
which a skim reads as a clean tally with a number in every column. Only
`refused` being non-zero distinguishes it, and that is the one column the
handoff tells the reader to check *"closely"*. **The reboot was not spent**:
`-List` is the same code path and answered the question for free.

***THE FIX IS THE OWNER'S CALL, BECAUSE IT IS A SECURITY GUARD.*** Three
shapes, cheapest last:

1. **Accept a SID that is currently a member of `BUILTIN\Administrators`**, as
   well as SYSTEM and the group itself. Keeps a backstop; costs a group lookup
   per record; a former administrator's old record stays honoured.
2. **Drop the per-file owner check and rely on the store's ACL.**
   `secure-reclaim.ps1` already grants the store to SYSTEM and Administrators
   **only**, so an ordinary user cannot create a file there at all — which is
   the containment the owner check was standing in for. The check's own comment
   admits this: *"The store's ACL is what should have made this impossible."*
3. **Have `DELETE_USER` set the record's owner to `BUILTIN\Administrators`**
   explicitly on creation. Leaves the consumer untouched, but every record
   written by an older build stays refused for ever.

**Whichever is chosen, the unit test needs the missing row**: a record written
the way `DELETE_USER` writes it, asserted **accepted**. That is the case whose
absence made 39/39 meaningless here.

**Do not reboot to confirm this.** The sweep at boot runs the same
`Get-RefusalReason`; it will refuse the same five and change nothing.

---

## 51. `Get-SysMsgPattern` cannot match any MULTI-LINE message, so three checks could not do their job — **M** — ***DONE 28 Aug 2026, all five copies*** *(renumbered from 45; see 49)*

***CONFIRMED ON THE INSTALL, 22:18: `verify-profiledir` 14 of 14***, the same
run that had reported 13 of 14 eight minutes earlier against the same product
and the same message. Nothing about `CREATE.ACCOUNT` changed between the two
runs — only the matcher did.

Found 28 Aug 2026 by the first run of `verify-profiledir.ps1`, which reported
`[FAIL] message 10124 shown` on a transcript containing 10124, printed
correctly and in full. **The product was right and the instrument was wrong.**

***THE CAUSE.*** The message FILES hold **literal backslash-n**, not newlines -
`grep -o -F` counts **16** in 10124, **14** in 10075, **16** in 10123 - and SD
turns each into a line break when it prints. `Get-SysMsgPattern` runs the file
text through `[regex]::Escape`, which renders `\n` as `\\n`: a pattern looking
for a literal backslash followed by `n`, which the rendered output never
contains. **A single-line message matches; a multi-line one cannot, ever.**

***THE THREE CHECKS, AND THEY FAIL IN OPPOSITE DIRECTIONS.***

| where | check | what it actually did |
|---|---|---|
| `verify-profiledir.ps1` | `10124 shown` — expects `$true` | **failed on a correct product** |
| `verify-delaccount.ps1:553` | `10075 NOT shown` — expects `$false` | **passed whatever was printed** — it cannot fail |
| `verify-delaccount.ps1:568` | `10075 shown` — expects `$true` | **would fail every time it ran** |

Line 568 is in the **keep-both** branch, which has never run on this host — step
3 has always taken the both-gone branch — so a guaranteed red has been sitting
in the verifier that guards PRE_RELEASE 36's central case, waiting for the first
machine whose hive is still up. **Every other `Shown` call across the five
verifiers that carry this helper is on a single-line message and is unaffected**
(checked by counting `\n` in each message the calls name).

***FIXED IN THE TWO FILES THAT HAVE AFFECTED CHECKS.*** `Esc-Loose` turns every
run of whitespace — literal `\n`, real newline, spaces — into `\s+`, so the
pattern survives rendering and wrapping. It cannot loosen a check into a false
positive: the words and their order must still be there.

**Driven with controls before either verifier was re-run** (scratch harness
lifting the two functions out of the shipped file, not a copy): rendered 10124
matches; a **different directory** does not; a **different account** does not;
**the echoed command plus both values alone** does not; 10075 and 10123 now
match; single-line 10084 and 10036 still match. **9 of 9.**

***AND THE THREE LATENT COPIES ARE FIXED TOO, ON THE OWNER'S INSTRUCTION, 28 Aug
2026.*** `verify-accountacl.ps1` and `verify-routes.ps1` carried a simpler
variant (no `$vals`, parts joined with `.*`); `verify-accountrules.ps1` one
differing only in its path base. None of their checks was affected — every
message they name is single-line — so the fix is insurance, and the point of
applying it was that this function has now gone blind **three times in three
different ways**, each found by a run rather than a test.

***SO THE THIRD TIME IT IS A TEST: `gplbld/test-sysmsg-units.ps1`, NEW.*** It
lifts `Get-SysMsgPattern` (and `Esc-Loose` where present) out of each verifier's
**AST rather than copying them**, and drives every message that verifier names
against a reconstruction of SD's rendering. No elevation, no run number, no
accounts — it needs an install only to read the messages from.

| | |
|---|---|
| the tree as it stands | **43 passed, 0 failed** — 5 verifiers, 28 messages |
| control, `-Gplbld` at the pre-45 copies from git | **37 passed, 2 failed** |

**The control is the part that makes the test worth having.** Its two failures
are 10075 and 10123 — the only multi-line messages in that tree — while all 35
single-line rows still pass, so it discriminates the defect itself rather than
the presence of a function. Getting there took a correction: insisting both
functions be liftable made a pre-45 copy fail at the lift, reporting *"the fix
is missing"* instead of running the old matcher and letting it miss. `Esc-Loose`
is optional to the harness for that reason.

**What it still cannot see:** that a verifier asked the right question. Line 553
expects the message NOT to be shown and would pass on a broken matcher and a
working one alike. Direction is the reader's job.

**The duplication remains the underlying problem** — one helper, five copies, so
this fix had to be made five times. The test at least fails all five together
the next time one drifts.

***THE THREE INSURANCE FIXES ARE MEASURED, NOT ASSUMED — `-Run b58`, 28 Aug
22:26.*** 13 of 13 unelevated, 18 of 19 elevated, and the three touched
verifiers are **identical to the two runs before them**, which is the check that
mattered: a repair that was not repairing anything must leave the counts alone.

| verifier | b56 | b57 | b58 |
|---|---|---|---|
| `verify-accountacl` | 21/0 | 21/0 | 21/0 |
| `verify-routes` | 33/0 | 33/0 | 33/0 |
| `verify-accountrules` | 34/0 | 34/0 | 34/0 |

No cycle was needed or spent: only `gplbld` verifiers changed, nothing under
`gplsrc` or `sdsys`, and `assert-current` was exit 0 before and after.

---

## 54. `verify-profiledir.ps1` is in neither runner, so 36's last leg never fires again — **M** (verifier gap, not product)

Carried as an open question to the owner since 28 Aug; **he handed the verifier
questions back on 29 Aug 2026** — *"your call on the verification utilities i
have no opinion"* — so this is decided here rather than asked again.

***THE PART THAT MAKES IT WORTH DOING.*** This leg *"had never been
exercised — no b56 or b57 log mentions either message, because every other
verifier is careful to use a fresh name, so the one rule that had never fired
was the one nothing could vouch for."* That was the whole argument for writing
`verify-profiledir.ps1`. It ran **14 of 14** on 28 Aug at 22:18 and went into
neither runner, **which puts the leg straight back into the state that made it
untrustworthy** — fired exactly once, by hand, by somebody who had to remember.

### ***DECIDED: WIRE IT INTO `VerifyInstall2`***

| | |
|---|---|
| **`VerifyInstall2`, not `VerifyInstall1`** | it needs **elevation**. `VerifyInstall1` is the unelevated parent, and that is forced rather than preferred — an elevated parent cannot make an ordinary child (`VerifyInstall1.ps1:70`, PRE_RELEASE 38) |
| **The cost is lower than a suite step already accepted** | `verify-doors-suite` runs in the suite and leaves **one permanent profile directory per run**, because its Control leg does a real ssh login. This one creates a control account and deletes it and **never logs in**, so Windows makes no profile — nothing is left behind |
| **It needs no cycle of its own** | it makes its own fixture with `New-Item`, needs no deleted account, no reboot and no reclaim store (`PROFILE_DIR:99-100`) |

***THE ONE THING THAT MUST NOT BE GOT WRONG: THE PREFIX COMES FROM THE `-Run`
TOKEN.*** The script refuses a spent stem on purpose — *"use a stem nobody has
used"* — so a **fixed** prefix passes on the first machine that runs it and
fails on every run after. `sdacctb48`, `sdtiertb48*` and `sdrtb48*` show the
convention: derive it, as `sdpd<run>`. **A hard-coded stem here would turn a
green suite red on its second run, which is the noisiest possible way to be
wrong and would probably get the step removed rather than fixed.**

**Also record the spent stems** — `sdpd1`, `sdpd2` are used (PROJECT_STATUS
§verify-profiledir) — and note that **10125 stays unexercised** either way:
*"the check could not run"* needs `os.execute` to fail, which nothing here can
force. Wiring this in does not close that.

---

## 55. `release.ps1` never runs the two doc generators that already refuse on a stale figure — **S** (docs toolchain)

Filed 29 Aug 2026 on the owner's *"your call on the verification utilities"*.
**This is the guard `a931c36` called *"the cheapest guard still available"* and
deliberately left unfiled** as a design question. It is a design question no
longer, so it goes on the list — and it belongs here by this file's own test,
because a doc set with a stale figure in it is a thing we would ship.

***MEASURED, NOT ASSUMED.*** `tools/release.ps1` is 180 lines and calls exactly
three things: `mkdoc.py` (`:109`), `mkpdf.ps1` (`:126`) and `checklinks.py`
(`:161`). **It calls neither `mktclsyntax.py` nor `tclmap.py`.**

***AND THOSE TWO ARE ALREADY THE CHECK.*** Both compute the verb roster from the
VOC, and both **exit 1** when the typed lists disagree with it — which is
precisely what they did over `encrypt.field`:

```
NOT A VERB  encrypt.field has a shape and is not on the roster
NOT A VERB  encrypt.field claimed by Administrator/01
```

**They had been refusing for a week and nothing knew**, because nothing runs
them. PRE_RELEASE 53 found it by running them by hand while fixing something
else. **A generator that refuses is only a guard if something runs it** — the
same failure as 54 one entry up, and the same failure the instrument rules in
CLAUDE.md are about.

### ***DECIDED, IN TWO PARTS, AND THE FIRST IS NEARLY FREE***

1. ***CALL BOTH GENERATORS FROM `release.ps1` AND FAIL THE RELEASE WHEN EITHER
   REFUSES.*** No new logic — the comparison already exists and already exits
   non-zero. This alone would have caught 53 a week earlier. Follow the shape
   `release.ps1` already uses for `checklinks.py` at `:161`, including the
   `$LASTEXITCODE` check, and echo the command per the instrument rule.
2. ***THEN CLOSE THE GAP THE GENERATORS DO NOT COVER: TYPED PROSE.*** They check
   the typed **maps** (`tcl-syntax-shapes.txt`, `tclmap.py`'s map), not the
   typed **sentences**. `mktclsyntax.py` printed `standard 81` in the generated
   card for a week while `Testing/markdown/07` said `77`; the two halves of the
   documentation disagreed and nothing compared them. **Have the generator write
   its computed figures out as data** — roster total and the three tier counts —
   **and assert the handful of labelled counts in the prose against that file.**

***DO NOT TRY TO CHECK EVERY NUMBER IN THE PROSE.*** That is why this sat
unfiled: as *"cross-check typed figures against computed ones"* it is unbounded.
Bounded, it is four numbers with names, and those four are the ones that have
actually gone wrong — PRE_RELEASE **4**, **52** and **53**, all three of them.

**Note it interacts with 34.** Both change `release.ps1`, and 34's ruling adds a
per-set link-free declaration to `checklinks.py`. **Do 34 first or do them
together**; two separate passes over the same 180-line script for related
reasons is how one of them ends up reverted.

---

## 59. Five unelevated verifiers assume an administrator has an ordinary account — **S** (harness, not product) — **DONE 29 Aug 2026**

Measured on `-Run b59`, 29 Aug 2026. **Elevated: 19 of 19, 397 PASS, 0 FAIL,
0 SKIP. Unelevated: 8 of 13**, and all five failures are the same thing.

| | what it said |
|---|---|
| `verify-lcnames` | *"=== 1. the session is in the account, not SDSYS"* → `[FAIL] WHO names the account: expected True, got False` |
| `verify-osusers` | `BASIC BP SDOSUSER` → *"Cannot read source record"*; then *"the probe did not run — no LOGNAME line above"* |
| `verify-nocase` | *"probing as SD account don"* → *"the probe did not run — no DIRFILE line"* |
| `verify-lineendings` | works against `C:\ProgramData\SD\user_accounts\don\bp` |
| `verify-batchjob` | *"the VOC probes could not be planted — nothing below would mean anything"* |

***THIS IS 56 WORKING, NOT 56 BREAKING SOMETHING.*** `don` is an administrator,
so LOGIN now elevates him into SDSYS; these five write a probe into the account
they expect to land in, and `BP` in SDSYS is a different file. `verify-lcnames`
is the clearest case because it **asserts the pre-56 rule as a requirement.**

***AND EVERY ONE OF THEM REFUSED THE NULL CASE OUT LOUD.*** Not one scored a
false pass on a probe that never ran — the instrument rule holding on the first
run that broke its premise, which is the whole reason that rule is written down.

**The fix is not five script tweaks.** Those verifiers mean *"run `sd` as an
ordinary user"*, and that only ever worked because the owner was an
administrator **with an ordinary account** — the combination clause 2 abolishes.
**They need a real non-administrator account to run as**, created and torn down
like the other prefixed test accounts. Until then this half of the suite cannot
speak for the product.

### ***THE FOUNDATION IS BUILT AND TESTED, 29 Aug 2026. THE WIRING IS NOT.***

| | |
|---|---|
| `gplbld/sdtestuser.ps1` | the module: password generation, `Invoke-SdAsTestUser` over ssh, and the SD line-builders. **Dot-sourced, not run** |
| `gplbld/sdtestuser-admin.ps1` | the **elevated** half that creates and removes the account, raised by the unelevated parent — the shape `verify-doors-admin.ps1` uses, and for the reason §4.0.1 gives |
| `gplbld/test-sdtestuser-units.ps1` | ***21 passed / 0 failed***, and it needs **no install, no elevation, no account, no ssh** |

***THE SHORTCUT IS A TRAP AND IS WRITTEN INTO THE MODULE.*** Adding `LOGTO DON`
to each verifier passes today and breaks the moment `adopt-account` goes —
which is ruled and pending, 56's last piece. **Five tests must not stand on an
account that exists only because the installer adopted the installing user.**

***ssh IS THE ROUTE BECAUSE `runas` CANNOT BE.*** Accounts SD creates are in
`sdsshonly`, which carries `SeDenyInteractiveLogonRight` (§5.6.2) — an
interactive logon as one is refused **by Windows**, and that refusal is the
product working correctly.

***ONE ACCOUNT FOR THE WHOLE HALF***, created once by the runner: five
verifiers each making their own would cost five UAC prompts, and CLAUDE.md's
rule is to remove the need for a prompt rather than the step.

***THREE REAL DEFECTS WERE CAUGHT BY WRITING THE TEST, NOT BY RUNNING THE
SUITE.***

1. ***`DELETE.ACCOUNT` HAS NO `NO.QUERY`.*** Checked in `DELACC` rather than
   assumed. The line first written would have passed an unrecognised token
   **and still hit the prompt** — PRE_RELEASE 14 exactly, where a piped
   `no.query` ate the following commands as answers and hung, costing a session
   and an elevated `sd -cleanup`. The confirmation is `input yn` looping *until
   Y or N* (`DELACC:249`), so a blank does not escape it — it spins.
2. ***`STANDARD` IS NOT A KEYWORD***, it is the default (`CREATEA:272`).
   Naming it passes an unrecognised token.
3. ***THE NULL-CASE GUARD WAS DEAD CODE AND THE TEST PASSED ON THE PARAMETER
   BINDER.*** `[Parameter(Mandatory)]` rejects an empty array before the body
   runs, so the module's own refusal never fired and the assertion was
   measuring PowerShell. **Found because the test printed the refusal it got.**
   The parameter is no longer `Mandatory`, and the test now anchors on wording
   only the guard emits, with a control proving the binder's wording would fail
   that check.

***AND THE SUCCESS CHECK WAS REWRITTEN AFTER BEING GOT WRONG TWICE.*** It first
matched SD's output for *"created"* — but message **6011 is "Account NOT
created"**, so the pattern matched the failure; and the wording guessed at
(`6055`/`6056`) **is not printed by `CREATEA` at all**, which is worse than no
anchor. It now checks the **artefact**, as `verify-doors-admin.ps1` does and as
the instrument rule asks: the ACCOUNTS record and the Windows user, **before
and after**, both halves required. A `Create` onto an existing name is refused
outright, because the name is single-use — an ssh sign-in leaves a profile
Windows will not reuse (PRE_RELEASE 35/36).

### ***THE WIRING IS BUILT, 29 Aug 2026. IT HAS NEVER RUN.***

`VerifyInstall1.ps1` creates the account before its step list and removes it
after; `verify-nocase.ps1` is converted. **`verify-lcnames`, `verify-lineendings`
and `verify-batchjob` are NOT** — that is the recommendation above, followed:
prove the pattern on the smallest one first. `verify-osusers.ps1` stays out of
the group entirely.

| | |
|---|---|
| create / remove | `VerifyInstall1.ps1`, conditional on `-Run`, name `sdtu<Run>`. **Removal is in a `finally`** — the loop `break`s on a failing step, so a removal written after it would be skipped by the case it is most needed in. That is `sddrb50a`, live on this machine now |
| the account | passed to the step as `-TestUser` / `-TestPassword`; without `-Run` the step is **SKIPPED** and said so, never run against the invoking user |
| `verify-nocase.ps1` | probe planted in the test account's `BP`, session driven by `Invoke-SdAsTestUser` over ssh. Refuses without the account, **before `assert-current`**, so the refusal is testable with no install |
| `test-sdtestuser-units.ps1` | **34 passed / 0 failed** (was 21). Still no install, no elevation, no account, no ssh |

***TWO DEFECTS WERE FOUND BY WIRING IT, AND BOTH WOULD HAVE COST A RUN.***

1. ***`assert-current` WAS ALREADY EXITING 1, AND HAD BEEN SINCE THE MOMENT THE
   MODULE WAS WRITTEN.*** The three new scripts were not on `$neverShipped`, so
   it named all three under *"STALE: 3 source file(s) are newer than the
   install"* and refused — **and every verifier that calls it refuses too**.
   The suite could not have run at all. Measured by running it, not predicted;
   listed now, and **exit 0 live afterwards**. This is the trap that list
   carries six dated warnings about, sprung by the commit that wrote the fix
   for something else.
2. ***`Get-SdTestUserHome` NAMED A DIRECTORY THE UNELEVATED PARENT CANNOT
   REACH.*** An account directory is protected and grants Modify to SYSTEM,
   Administrators and **its own `sdu_<account>` group only** — an unelevated
   token has none of the three, Administrators being deny-only in a filtered
   one. `ls` and `touch` on `SDACCTB59` both answered *"Permission denied"*.
   **All four verifiers plant their probes through the file system**
   (`verify-lcnames` in nine places), so the module's central helper named a
   path none of them could use. `-Action Create` now adds one inheritable ACE
   for the invoking user. ***A GROUP WOULD NOT HAVE WORKED***: membership is
   fixed at logon, which is PRE_RELEASE 44 exactly — *"don is in `sdu_sddrb50a`
   on the machine and not in his token"* — and is why the door pair needed a
   helper account. An ACE on the **user's** SID needs no new token.

***AND ONE THE WIRING ITSELF INTRODUCED, CAUGHT BEFORE IT SHIPPED.***
`sdtestuser.ps1` carried `Set-StrictMode -Version Latest` at file scope, and
**dot-sourcing runs in the CALLER's scope** — so wiring it into
`VerifyInstall1.ps1` silently turned strict mode on there. Measured with a lax
probe: *"undefined variable: allowed"* before the dot-source, *"THREW —
RuntimeException"* after. **Not theoretical** — `VerifyInstall1`'s missing-
`sd.exe` fallback reads uninstall keys with `$_.DisplayName`/`$_.InstallLocation`
and most carry neither, which under strict mode is terminating, in the branch
whose job is to explain a broken install in one line. Each function now sets it
for itself; a unit row drives both halves **in a separate lax process**, because
the test file is itself strict and a check made in it would have passed whatever
the module did.

### ***FIRST RUN, `b60`, 29 Aug 2026 11:45:30 — IT STOPPED AT THE CREATE STEP***

SD printed its banner and then `:Process terminated`, and made nothing.
`before=False after=False` for both the ACCOUNTS record and the Windows user,
so **the check refused rather than scoring a pass** — the artefact test earning
its place on its first real run.

***THE MESSAGE IS sysmsg 5020 AT `CPROC:473`, THE `K$LOGOUT` ARM.*** A **forced
logout**, not a refusal of the command — which is why nothing echoed
`CREATE.ACCOUNT` at all, and why reading it as "SD said no to the account" would
have sent the next session looking in `CREATEA`.

***AND THE CAUSE WAS ON DISK, DATED 14 Aug 2026, IN A FILE THE ENTRY ALREADY
NAMES.*** `verify-createaccount.ps1`'s header, and PROJECT_STATUS.md §6:

> *"Input must be PIPED. `Start-Process -RedirectStandardInput` hands SD a file
> handle and SD answers 'Process terminated' and exits, the same way the `<`
> redirect does."*

A run was spent rediscovering it. **`sdtestuser-admin.ps1` now pipes** —
`$text | & $exe` inside a `Start-Job`, the shape `verify-doors-admin.ps1` and
`verify-tiers.ps1` both use — with `LOGTO SDSYS` first as every elevated script
here carries, and a **120 s timeout**, which matters more here than in the file
it was copied from: this runs in an elevated window the unelevated parent is
`-Wait`ing on, so an unanswered prompt would hang both with the reason on a
console the parent cannot read.

***`sdtestuser.ps1` STILL USES THE FILE FORM AND IS RIGHT TO.*** The rule is
about handing **sd.exe** its own stdin. `Invoke-SdTestNative` drives `ssh.exe`,
which takes a file handle happily, and SD is at the **far end** of the
connection where it sees the ssh channel rather than a file. That distinction is
now the unit test's **control**: the module must still use it, or the guard has
stopped being able to see the thing it looks for.

**The guard is tokenised, not grepped**, because the fix wrote a comment block
that correctly quotes `-RedirectStandardInput` to explain why it is wrong —
`test-verdict-units.ps1` hit exactly that on 28 Aug. **Units 41 / 0.**

**Nothing was left behind**, measured: no `*b60*` Windows user, ACCOUNTS record
or account directory, no leftover temp work directory, and the only `sdwind` is
the service's own. ***`b60` IS NOT SPENT — REUSE IT.***

### ***SECOND RUN, `b60` AGAIN, 29 Aug 2026 11:53:01 — IT RAN IN FULL, AND THE FOUNDATION IS WITNESSED***

**Elevated 19 of 19. Unelevated 8 of 13.** The account machinery worked end to
end for the first time:

| | |
|---|---|
| Create | `before=False after=True` on **both** the ACCOUNTS record and the Windows user |
| the ACE | granted to `GITORLI\don`, and the **unelevated parent's own write succeeded** — the only token that could answer the question |
| Remove | `before=True after=False` on both, no residue |
| alongside | `verify-doors-suite` **5 of 5 green** in the same run, so two account mechanisms coexisted |

***AND THE TIER WAS WRONG. SD SAID SO IN ITS OWN WORDS.*** ssh **exit 0**, the
session was in `sdtub60`, and then *"BASIC is not in your VOC"* and *"RUN is not
in your VOC"*. `sdsys/newvoc/TIER.OMIT.STANDARD` lists **`basic` and `run`**
among the 42 verbs withheld from a standard account — along with `ed`, `edit`,
`micro`, `create.file`, `copy`, `delete` and `rename`. ***ALL FOUR VERIFIERS
COMPILE AND RUN A BASIC PROBE, SO STANDARD CANNOT HOST ANY OF THEM.***

The account is **PROGRAMMER** now. **Still a real non-administrator**, which is
all 59 ever needed: ADMINISTRATOR is the tier `LOGIN` elevates into SDSYS under
56, and `verify-doors` creates its accounts PROGRAMMER for exactly this reason.

***THE UNIT TEST ROW WAS ITSELF THE BUG.*** It read *"create: does NOT grant
ADMINISTRATOR or PROGRAMMER"* — encoding the STANDARD choice as a rule, so the
test would have **defended the mistake against a correction**. It is split in
two now (ADMINISTRATOR is the one that must never appear), and the tier is
checked against `TIER.OMIT.STANDARD` itself, so a future change that gives
standard accounts `basic` back says the tier can drop again.

***TWO LEAKS, BOTH PRE_RELEASE 47's SHAPE, BOTH FIXED.***

1. **The unit test's denied fixture survived every run.** `icacls /remove:d`
   did not remove the ACE, and its output had been sent to `*> $null` — so six
   undeletable directories were in `%TEMP%` before anyone looked, each still
   carrying `(OI)(CI)(DENY)(WD,AD,WEA,WA)`, with `Remove-Item` answering
   *"Access to the path is denied"*. `/reset` removes it, the exit code is read
   rather than silenced, and **the removal is a checked row** — the warning line
   it replaced is how six accumulated unnoticed.
2. **`Invoke-SdAsTestUser` never removed its work directory** — `native.in` and
   609 bytes of `native.out`, once per verifier per run. Removed now, but only
   when the function made it: a caller that passes `-WorkDir` owns the evidence.

**Units 45 / 0**, and a run leaves `%TEMP%` clean.

***THE RUN POLLUTED SDSYS, AND THAT IS THE COST OF THE UNCONVERTED THREE.***
`C:\ProgramData\SD\sdsys\BP.OUT` was created **12:07:16** by `verify-lcnames`
compiling its probe while landed in SDSYS. Harmless, and the next cycle clears
it. **But two of `lcnames`' 21 failures are about that object directory's
case** (`sdsys bp.out present` → 0, `sdsys BP.OUT absent` → 1), and ***those
readings are not to be trusted until it runs in an account*** — its premise was
broken, which is exactly what the instrument rule says to distrust. `lcnames`
scored **107 of 128**. Re-read them after the conversion, not before.

***`b60` IS SPENT*** — `C:\Users\sdtub60` exists, so the name is taken until a
restart. **Use `b61`.**

### ***THIRD RUN, `b61`, 29 Aug 2026 12:21:40 — `verify-nocase` IS GREEN***

***3 OF 3 DECISIVE CHECKS, INCLUDING THE CONTROL.***

```
verify-nocase: probing as SD account sdtub61 (a throwaway non-administrator)
  ssh exit 0, 656 characters of output
directory file (BP) reports FL$NOCASE  1  1  PASS  yes
dynamic file (VOC) reports FL$NOCASE   0  0  PASS  yes
SYSTEM(91) answers Windows             1  1  PASS  yes
```

**`DHFILE=0` is the row that matters** — it is the control the file's own header
calls *"the point of the test"*: a directory file answering 1 proves nothing
unless a dynamic file still answers 0. ***THIS IS THE FIRST MEASUREMENT THIS
PROJECT HAS TAKEN AS A REAL NON-ADMINISTRATOR.***

**Unelevated 9 of 13** (was 8), **elevated 19 of 19**. The Create/Remove pair
repeated cleanly, and `verify-doors-suite` was 5 of 5 alongside it again.

***SO THE CAUTION IS PAID OFF AND `verify-lineendings.ps1` FOLLOWS.*** The
recommendation was to prove the pattern on the smallest verifier before
replicating it; it is proven. lineendings is converted the same way — probe
planted through the file system, session driven by `Invoke-SdAsTestUser`, refusal
before `assert-current` so it is testable with no install — and is **UNRUN**.

**The refusal tests are a TABLE now, not a copy per script.** Four
near-identical conversions are four chances for one to be subtly wrong; a check
written once cannot drift. And ***the table is compared against
`VerifyInstall1`'s own `$needsTestUser`, read out of its source*** — a verifier
converted but not listed would be untested, one listed but not wired would be
skipped, and both are silent. **Units 51 / 0.**

### ***FOURTH RUN, `b63`, 29 Aug 2026 13:03:55 — `verify-lineendings` IS GREEN TOO. UNELEVATED 10 OF 13.***

**17 checks, all PASS, on real readings** (`REC ZZLECRLF FIELDS=3 LEN=18`), run
as `sdtub63` over ssh. **The two that matter both passed:**

| | |
|---|---|
| the straddle | `line 1 length expected 2047, got 2047` — a CRLF landing exactly on the 2048-byte `SEQ_BUFFER_SIZE` boundary. The file's header calls this the reason it exists rather than a one-liner: a fix that inspects *"the byte before the LF"* is right on every small fixture and wrong once per 2 KB of real data |
| the lone-CR control | length **11 unchanged**, one field — a CR survived **as data**. A fix that stripped every CR would pass checks 1–4 and silently corrupt text; this is the control on the fix rather than on the defect |

**Elevated 19 of 19. The account removed cleanly** (`before=True after=False`
on both halves), and the run left **no `sdtu*` user, no `SDTU*` record, no
`sdu_sdtu*` group and no `%TEMP%` residue.**

### ***AND THE REMAINING TWO ARE NOT MECHANICAL. THE CLASSIFICATION WAS WRONG.***

This entry said *"four are close to mechanical; `verify-osusers.ps1` is not"*.
**Measured against the source, only two were.** `verify-nocase` (211 lines) and
`verify-lineendings` (330) each plant a probe and drive one session, and both
converted in a few edits. The other two do not:

- ***`verify-lcnames.ps1` NEEDS BOTH TOKENS, PER CALL SITE.*** 53 `Invoke-SD`
  calls, **four of them `LOGTO SDSYS`** (`:342`, `:774`, `:782`, `:783`) for
  checks only an administrator may make. Under 56 those four work *today*
  precisely because the invoking administrator already lands in SDSYS — which
  is the same fact that breaks the other 49. So the conversion is not "swap the
  driver": it is **classifying 53 call sites into account-side and SDSYS-side**,
  and a mistake in either direction is a check that passes while measuring the
  wrong session. That is the failure this entry exists to stop.
- ***`verify-batchjob.ps1` RE-INVOKES ITSELF ELEVATED*** (`:287`–`:291`,
  `-Phase setup`) to write SDSYS's `batch.jobs`, and its elevated leg does
  `Push-Location` into the account directory (`:111`) to get a session *in that
  account*. **Under 56 an elevated administrator lands in SDSYS whatever the
  cwd**, so whether that leg still measures what it claims has to be **checked
  rather than assumed** before anything is converted.

  ***CHECKED ON `b65`, 29 Aug 2026, AND IT IS WORSE THAN THE WARNING SAID: THE
  ROW'S SUBJECT IS UNREACHABLE, NOT MERELY MIS-MEASURED.*** `verify-batchjob`
  exits **1** with **9 of its 10 rows passing**; the failure is
  `ELEVATED with no entry: still runs`, expected True and observed **False**.
  **An elevated session cannot stand in an ordinary account at all** under the
  ruled model: an elevated login goes to SDSYS (`LOGIN:568`), and a `logto` out
  of SDSYS gives up the flag (`CPROC:2781`). So there is no state in which the
  thing that row measures can be observed.

  ***THE PRODUCT RULE IT PROTECTS IS INTACT AND WAS CHECKED SEPARATELY.***
  `LOGIN:901` still bypasses the batch gate on `K$ADMINISTRATOR`, so the
  owner's 22 Aug decision — *"elevation passes on its own"* — holds **in
  SDSYS**, which is now the only place an elevated session can be. **Nothing is
  broken; the check is aimed at a place that no longer exists.**

  ***RULED 29 Aug 2026 — "re-aim the batchjob row at sdsys". BUILT, UNRUN.***
  The elevated child no longer `Push-Location`s into the account. It now:

  1. **asserts the "no entry" precondition** — refuses out loud with
     `SDSYS-ENTRY-PRESENT` if `batch.jobs/SDSYS` exists, and **does not delete a
     record it did not write**. Without this the row could pass because SDSYS
     was listed rather than because elevation bypassed the gate;
  2. **plants the same `COUNT VOC` paragraph in SDSYS's own VOC** (`zzbatchsyspa`,
     through a piped `sd`, since a VOC is a dynamic file), because the account
     probes live in the ACCOUNT's VOC and an elevated session never sees them —
     which is the whole reason the row had to move;
  3. runs it from the command line and keeps the proven `record(s) counted`
     anchor;
  4. **cleans up unconditionally** — `DELETE VOC` plus the BP source and object,
     on every path out including both failures. PRE_RELEASE 60 and 61: a VOC
     record outliving what it names *is* the defect those entries are about.

  ***IT IS DECISIVE FOR A REASON THAT GOT STRONGER, NOT WEAKER.*** `LOGIN:901`
  bypasses **the whole of `batch.permitted`** on `K$ADMINISTRATOR` — the
  no-arguments check, the `batch.jobs` listing check **and** the PA/S type
  check. So a command that runs with no SDSYS record cannot have passed the
  listing check, and the bypass is the only thing left that explains it.

  ***AND "COULD NOT BE MEASURED" IS NOT SCORED AS "FAILED".*** Both refusal
  markers record the row **non-decisive** and print the child's own text, so a
  broken precondition cannot turn the script red or make a claim about the
  product that the run did not make.

  **Checked before hand-over**: parses with **0 errors and all 8 functions
  found**, no BOM, CR 0; `assert-current` exit 0 (it is on `$neverShipped`, so
  **no cycle is owed**), `test-verdict-units` 126/126, `test-sysmsg-units` 43/0.
  ***UNRUN — it needs `b66`.***

**Neither is a reason to stop; both are a reason not to do them in a hurry.**
The two that were mechanical are done and green, which is the whole value of
having split them.

***WHAT IS LEFT.*** **Two of four are done and green. All three remaining need
a token split rather than a driver swap, so none of them is an afternoon's
copy-and-paste.**

- ***`verify-lcnames.ps1`*** (1049 lines, 53 `Invoke-SD` calls). **Classify
  every call site as account-side or SDSYS-side**, then give it two drivers.
  The four `LOGTO SDSYS` sites are the SDSYS ones and must keep the LOCAL pipe:
  under 56 the invoking administrator is already in SDSYS, so those are exactly
  the checks that still work. Its **21 failures include two `sdsys BP.OUT` rows
  that are NOT to be read as product defects until this is done** — its premise
  is broken and the instrument rule says so.
- ***`verify-batchjob.ps1`*** (368). **Check the elevated leg first, before
  converting anything.** It re-invokes itself elevated (`:287`) and its child
  does `Push-Location` into the account directory (`:111`) to get a session *in
  that account* — and under 56 an elevated administrator lands in SDSYS
  whatever the cwd. Whether that leg still measures "an elevated session passes
  the gate on its own" is a question, not an assumption.
- **`verify-osusers.ps1` separately** — 931 lines with **32** references to
  `@logname`/`don`, and it is *about* the person's identity in `os.users`, with
  its own elevation dance. **Do not bundle it.**
- ***DONE — THE SWEEP. OWNER'S RULING, 29 Aug 2026, asked and answered:
  "sweep".*** A console Ctrl-C does not run `VerifyInstall1`'s `finally`
  (measured on `b62`), so an interrupted run strands its account live and
  enabled. `sdtestuser-admin.ps1 -Sweep` removes strays **inside the elevated
  child Create already raises**, so it costs no extra prompt. ***THE CANDIDATE
  LIST IS BUILT IN THE ELEVATED PROCESS AND IS NOT PASSED IN*** — this is code
  that deletes Windows accounts, so the only thing the parent controls is
  whether to sweep, not what. Three conditions, all required and each printed:
  the name matches `^sdtu[a-z0-9]+$`, it is **not** the account being created
  (a reused token must still hit the single-use refusal, because the profile is
  what burns the name), and it is **in `sdusers`**, which ties it to an account
  SD made. Removal is `DELETE.ACCOUNT`, so record, group and Windows user go
  together, and the check is the artefact before and after rather than SD's
  wording. **UNRUN.**
- **The two UAC prompts.** Create and Remove each raise one through
  `Start-Process -Verb RunAs`. `verify-doors-suite.ps1` serves its three
  elevated legs from **one** consent through `sd-elevate.ps1`'s resident helper
  and would take this to zero extra. Not done here on purpose: it is ~150 lines
  of machinery in that file, and layering a second unproven mechanism on a
  first is how the box's own warning gets ignored. **Do it once this has run.**

**No UAC storm, which was the other risk and did not happen.** The helper
widening in 56 held: every step logged in, and `assert-current` passed in each.

---

## 58. The documentation does not describe the access model the product now has — **B** — **DONE 29 Aug 2026**

***DONE — OWNER, 29 Aug 2026, AND THIS ROW HAD GONE STALE WITHOUT ANY GUARD
NOTICING.*** The docs repository has an `Administrator` set now, and
`Administrator/markdown/01-accounts-and-security.md:44-47` describes the built
model in its own words: what counts as elevated is fixed when SD starts, and
SDSYS is reached from **an elevated terminal or the UAC prompt `logto sdsys`
raises** — the owner's two explicit routes.

***WHY IT DRIFTED, AND IT IS STRUCTURAL RATHER THAN CARELESS.***
`check-stale-leads.py` compares this file's table against this file's entries.
**It cannot see the docs repository at all**, so a row whose work lives there
can go stale with every checker in this tree still exiting 0. Any future entry
whose `where` column names the docs repo has the same hole — **read that repo
before reporting on such a row.**

Owner's instruction, 29 Aug 2026, given while 56 and 57 were being written:
*"remember to enter a task to update documentation with these changes."*

***IT IS FILED NOW AND DELIBERATELY NOT STARTED.*** Both entries it documents
have pieces still unsettled — 56's `adopt` half and 57's promotion case — and
writing a reference against a model still in motion is how the tester set came
to describe `encrypt.field` for a week after it was deleted (PRE_RELEASE 52 and
53). **Start it when 56 and 57 have landed and one cycle has proved them.**

***THE DOCS ARE A SEPARATE GIT REPOSITORY***, at
`C:\Users\dmont\Projects\SDCoreWindowsDocs`.

***RENAMED BY THE OWNER, 29 Aug 2026, TO MATCH THE GitHub REPOSITORY.*** This
paragraph used to warn that the path *"has spaces in it"* and that *"a probe for
`SDCoreWindowsDocs` finds nothing — that cost a whole session once."* **Both
halves are now false and the second is actively misleading**: the directory name
IS the repository name, and probing for it is what works. Rewritten rather than
patched, because a warning that has inverted sends the reader away from the
answer.

### What changed that a reader would notice

| | from |
|---|---|
| an administrator is **elevated at login** and lands in **SDSYS** | 56 |
| an administrator has **no account of their own**; a personal one is created and granted like anyone else's | 56 |
| ***an administrator can no longer reach SD over ssh*** — UAC has no desktop there | 56 |
| `logto sdsys` is refused unless the **person** is an administrator | 56 |
| a grant may go **down or sideways, never up** | 57 |
| **SDSYS is never granted to anybody** | 57 |
| `revoke` / `modify.account … delete` unaffected — removing access is always allowed | 57 |
| new messages **10126**, **10127** | 57 |

### Where it lands

**Derive the page list in the docs repo rather than trusting this one** — H.2
in PROJECT_STATUS.md has the set inventory. The verbs with pages that certainly
move are `grant`, `revoke`, `list.grants`, `logto`, `modify.account` and
`create.account`; beyond those, the tier and restricted-command topic pages,
`Administrator/01`, and any tester page that tells somebody how to sign in —
**that instruction is now different for an administrator.**

***AND IT WILL COLLIDE WITH 34 AND 55, WHICH IS AN ARGUMENT FOR DOING THEM
TOGETHER.*** Regenerating anything runs `mktclsyntax.py` and `tclmap.py`, which
compute the roster and `exit 1` on disagreement — 55 is that they are not wired
into `release.ps1` at all — and `release.ps1` still cannot complete on the
`Technical` set until 34's link-free declaration exists.

---

## 57. A grant may go down or sideways, never up — **B** (owner's rule, 29 Aug 2026) — **DONE 29 Aug 2026**

***DONE — OWNER, 29 Aug 2026.*** `TIERGATE` and its four callers were built and
cycled, and the last piece — the promotion report — was built, cycled and
installed on the same day. **"Installed and unrun" was a testing gap, not
outstanding work**, and it is not a reason to hold the entry open: no verifier
covers `modify.account b programmer` stranding grants, which is a gap worth
filling one day rather than a thing left undone.

> ***IT COMPILES — MEASURED 29 Aug 2026 10:22, NOT REPORTED.*** `cycle.ps1
> -SkipInstall`, and **the staged tree was read rather than the run's output
> believed**, as the 26 Aug precedent requires. `gpl.bp.out/TIERGATE` **and**
> `gcat/!TIER_ALLOWS` both exist; `CPROC`, `LOGIN`, `ELEVATE`, `GRANTA`,
> `MODIFYA`, `APISRVR` and `CREATEA` all recompiled at 10:22; messages
> **10126** and **10127** staged.
>
> ***AND THE WARNING CLASS IS CLEARED, WHICH IS THE PART A GREEN BUILD DOES NOT
> NORMALLY PROVE.*** `bootstrap.py`'s `check_compile()` **dies** on any *"is
> not assigned a value"* warning — the ERRGEN trap, an abort at run time in a
> program that may not run for weeks — as well as on a missing summary and any
> non-zero `n error(s)`. Reaching ISCC means all three passed, so `admin.login`,
> `tg.why`, `ma.why` and TIERGATE's locals are genuinely assigned.
>
> ***THE COUNTS ARE 127 / 186, AND THE 125 / 184 IN §"THE MACHINE" IS A STALE
> BASELINE RATHER THAN A DISAGREEMENT.*** +2, not +1: `PROFILE_DIR` arrived
> with PRE_RELEASE 36 on 28 Aug, after that line was written, and `TIERGATE` is
> the second. **Checked rather than assumed** — both are present.
>
> **Still unrun.** Compiling is not running; `-SkipInstall` never touches
> `C:\ProgramData\SD`.

> *"Standard accounts can not be given access to programmer accounts,
> programmer accounts can be given access to standard accounts. Only windows
> administrators can enter SDSYS, rights to SDSYS can not be granted to
> programmers or standard accounts."*

### ***WHAT IT WAS FIXING, MEASURED FIRST***

Asked what a standard user A gets after `logto b` into a PROGRAMMER account B,
the answer split in a way nothing had written down:

| | follows | because |
|---|---|---|
| **the verb set** | ***the ACCOUNT*** | the tier is applied to the account's own physical VOC **at creation** (`CREATEA:1184`), so A stands in B's directory using B's VOC — **+42 verbs** on the computed roster |
| `sh` / `os.execute` | the **PERSON** | `os.users` keyed on `@logname` / `process.username`, which a `LOGTO` never changes (`CPROC:3548` says so outright) |

**So a grant handed over a whole tier's verbs.** That is the hole the rule
closes. The `os.users` half is untouched by this entry and is PRE_RELEASE 2/56.

### The ordering, and what an unknown tier does

`STANDARD` 1, `PROGRAMMER` 2, `ADMINISTRATOR` 3; entry is permitted when the
person's rank is **at least** the account's. **Equal ranks pass** — two people
sharing a standard account is the ordinary case and not what the rule is aimed
at. `SUSPENDED` resolves through `ACC$PRIOR.TIER`, which exists precisely so
the displaced tier is not lost, so a grant made while somebody is suspended is
still the right one when it lifts. ***An empty or unknown tier is REFUSED, not
defaulted*** — `GRANTA`'s existing rule for an empty `ACC$GROUP`, and the
opposite of NEWVOC's tier lists where a missing record means the full VOC.

### ***FOUR CALLERS. TWO ARE GATES AND TWO ARE COURTESY.***

| | | |
|---|---|---|
| `CPROC` `logto.authorised` | ***GATE*** | placed **after** the group test, so only somebody actually granted learns anything; a stranger still gets the undifferentiated 10003 |
| `APISRVR` `vb.account` | ***GATE*** | ***the fourth door, and it would have been the way round the whole rule*** — see below |
| `GRANTA` | courtesy | the administrator granting finds out at once instead of the user finding out at `logto` |
| `MODIFYA` ADD arm | courtesy | it makes the **identical** `os_group('ADDMEM',…)` call — which is why PRE_RELEASE 27 had to give it the same audit record — so omitting it would make the verb the way round the rule |

***THE API HALF WAS NEARLY MISSED, AND IT IS THE SAME OMISSION PRE_RELEASE 19
AND 38 KEEP FINDING.*** An API session reaches an account through **neither**
`LOGIN` **nor** `logto.authorised` — which is exactly why the `ACC$GROUP` check
had to be added to `vb.account` separately on 17 Aug — so a rule enforced only
in CPROC does not bind it, and a granted standard user could have taken a
programmer account's whole verb set over the API. **It reuses `sysmsg(10003)`
like every other refusal in that routine**, so the API still cannot be used to
enumerate the register; CPROC says more because a local caller has already
proved who they are.

***AND IT IS WHY `!tier_allows` IS `$internal`.*** It reads `@sdsys/accounts`,
and `net_path_permitted()`'s allow-list does **not** include that file — so
from an API session an ordinary program could not read it at all. `HDR_INTERNAL`
is what makes the check possible on the one route that most needs it.

***A CHECK ONLY AT GRANT TIME WOULD BE UNSOUND, AND THAT IS THE REASONING TO
KEEP.*** The grant **is** Windows group membership, so `net localgroup` makes
one without SD ever seeing it; and `modify.account b programmer` can raise a
tier long after a legal grant, with nothing revisiting the group. Both bypass
grant time. Neither bypasses `logto`.

**`REVOKE` and `MODIFY.ACCOUNT … DELETE` are deliberately unguarded.** Taking
access away is always allowed, and refusing a revoke would strand exactly the
memberships this rule wants removed.

### SDSYS is refused by name as well as by tier

Two things already stop it and **both are accidents rather than statements of
the rule**: the shipped `accounts/sdsys` record carries **three fields** —
path, description, group — and **no `ACC$TIER` at all**, so the rank test
refuses it; and `ACC$GROUP` is `sdsys`, which is not a Windows group, so
`is_grp_member` can never pass. Either would evaporate if somebody gave SDSYS
a tier or created a Windows group of that name. The rule is absolute, so
`!tier_allows` refuses the name outright. **The actual enforcement of *"only
Windows administrators enter SDSYS"* is 56's gate in `int.logto`**, which
refuses a non-administrator before the register is read.

### Left to settle

***PROMOTING AN ACCOUNT CAN STRAND AN EXISTING GRANT, AND NOTHING REPORTS
IT.*** `modify.account b programmer` turns every standard-tier member of
`sdu_b` into somebody `logto` will now refuse. **The gate holds** — that is the
whole point of putting it there — but the membership sits in Windows looking
valid and simply stops working. **Not fixed here, and not ruled**: the options
are to refuse the promotion while lower-tier members remain, or to let it
proceed and have `modify.account` *print* the memberships it has just voided.
**The second is the smaller change and the honest one**; it is the owner's
call, and it is the last piece of this entry.

***RULED 29 Aug 2026: "Proceed, and print what it voided."*** `MODIFY.ACCOUNT`
does the promotion and then lists the grantees whose access it has just made
useless.

***BUILT AND CYCLED 29 Aug 2026.*** `MODIFYA`'s `promo.snapshot` runs
immediately before the register write and `promo.report` after it, so the
report is a **before-and-after reading of `tier_allows`** rather than rank
arithmetic copied out of `TIERGATE` — the same call answers differently either
side of the write, and one place still decides. Messages **10128** and
**10129**.

**Three properties that fall out rather than being special-cased:** a demotion
strands nobody, so the comparison is empty and nothing prints, and no code
tests the direction of the move; a membership that was **already** refused
before the command ran — made with `net localgroup`, or left by an earlier
promotion — is not claimed as this command's doing; and an unreadable group
**says so** (10129) instead of reporting a comfortable zero, because "nobody
was affected" and "nothing could be checked" are otherwise the same silence.
***UNRUN — the behaviour is installed and no run has exercised it.***

***AND THE SCOPE IS NARROWER THAN THE PARAGRAPH ABOVE READS — ASKED AND
ANSWERED FROM THE SOURCE.*** The owner asked whether this only applies to
accounts with more than one member. It does. `TIERGATE`'s own description is
the evidence: `!tier_allows(user, account)` compares **the person's own account
tier** with the target's, and its three callers are `CPROC`'s
`logto.authorised`, `GRANTA` and `MODIFY.ACCOUNT` — ***`LOGIN` is not one of
them***. So:

- **the account's own owner is never stranded** — they arrive by `LOGIN`, which
  never consults the gate, and their rank equals the account's in any case;
- **only users granted in by somebody else can be**, and only those whose own
  account is a lower tier;
- **a single-member account cannot strand anything**, so on a typical install
  the printed list is empty.

**Note it now interacts with 56's "two tiers" ruling**: both change `MODIFYA`,
and `MODIFYA:1102`'s rank table is common to them. **Do them in one cycle.**

---

## 56. The administrator access model, rewritten — **B** (owner's ruling, 29 Aug 2026) — **DONE 29 Aug 2026**

***DONE — OWNER, 29 Aug 2026.*** The model as finally ruled is built, cycled and
proved by `-Run b66`: the `sdusers` gate is uniform across all three tiers
(`LOGIN:414`), the SDSYS case tests **elevation** rather than personhood
(`LOGIN:568`), an unelevated administrator lands in their own account, and
administrators keep ssh.

***ITS ONE REMAINDER IS SPLIT OUT AS ENTRY 62 RATHER THAN DROPPED.*** This entry
carried a **measured** finding — `elevate('START')` tests nobody's identity, so
an administrator's password was enough to reach SDSYS and the trail then named
the person who did **not** consent. That was measured **before** clause 2 was
reversed, and the reversal plausibly changes it: reaching the SDSYS case at
login now requires the session to be **already elevated**, and such a session
runs as the administrator whose credentials were typed, so `@logname` should
name the right person. ***PLAUSIBLY IS NOT MEASURED***, and a security finding
must not evaporate because the code around it moved — so it is re-filed as 62
to be re-measured, not carried here as an open claim about a model that has
since changed.

***THIS SUPERSEDES THREE RECORDED DECISIONS AND THE OWNER TOOK ALL THREE
KNOWINGLY*** — he was shown each one and what it cost before ruling. It is not
drift and it is not a session inventing a model.

### The model, in his words, 29 Aug 2026

> *"Administrators get an elevation prompt at login and are logged in as SDSYS.
> Administrators do not have a regular account of their own. If they want a
> personal account they have to create it and give it specific rights like any
> other account. An administrator can logto any account. If they logto another
> account, they have the rights of that account. If they want administrator
> rights back they have to logout and log back in. However, a person who has
> logged in as a non-administrator only has the ability to move to accounts
> that they have been given access to."*

**And on the way back in, asked whether `logto sdsys` must be refused once you
have left:** *"I like still works"* — so it keeps its present behaviour and
asks UAC again. Logging out is one route back, not the only one.

### ***THREE OF THE SEVEN CLAUSES ARE ALREADY THE CODE. MEASURED, NOT ASSUMED.***

| clause | already true at |
|---|---|
| an administrator can `logto` any account | `CPROC:3752`, passes on `K$ADMINISTRATOR` |
| `logto` elsewhere → you have that account's rights | `CPROC:2735` clears `USR_ADMIN`, `:2738` stops the helper |
| a non-administrator moves only where granted | `CPROC:3803`, `is_grp_member(@logname, ACC$GROUP)` |

***SO THE FIRST CONSEQUENCE IS THAT PRE_RELEASE 31's 29 Aug RULING IS
WITHDRAWN*** — it said the opposite, and clause 5 is the code as written.

### What actually has to be built

| | where | state, 29 Aug 2026 |
|---|---|---|
| `K$OS.ADMINISTRATOR` (63) — *is the signed-in **person** an administrator* | `keys.h`, `INT$KEYS.H`, `op_kernel.c` | ***WRITTEN.*** Carries `kernel.c:240`'s `CN_SOCKET` guard. `make sd` **exit 0, 0 warnings**, `op_kernel.o` mtime moved, `bin/sd.exe` relinked |
| an administrator is elevated at login and lands in **SDSYS** | `LOGIN`, new case before `case 1` | ***WRITTEN, UNCOMPILED.*** Reverses 15 Aug 2026 |
| ***the `sdusers` gate exempts an administrator*** | `LOGIN:380` | ***WRITTEN, UNCOMPILED.*** **Not in the ruling — see below. Without it the model is dead at the door** |
| `logto sdsys` refused unless the **person** is an administrator | `CPROC`, before `elevate('START')` | ***WRITTEN, UNCOMPILED*** |
| `ELEVATE`'s "only one caller" note | `ELEVATE` header | ***WRITTEN.*** LOGIN is the second caller; the owner's 16 Aug rule is untouched and the note says why |
| administrators no longer written into `os.users` | `CREATEA`, the `tier = 'ADMINISTRATOR'` block | ***WRITTEN, UNCOMPILED.*** The two `os.sh`/`os.exec` lines are gone; only the explicit `sh-on`/`os-on` keywords now grant it |
| ***one helper per USER, not per session*** | `ELEVATE`, `sd-elevate.ps1`, `sd-elevate-helper.ps1` | ***WRITTEN.*** Both scripts **parse 0 errors with functions found**, no BOM, CR 0 — see below |
| the control follows the product | `verify-apiadmin.ps1:610` | **PRE_RELEASE 31 — nothing to do, it should now pass unchanged** |

### ***THE HELPER IS ONE PER USER NOW, BECAUSE 56 TURNED ONE PROMPT INTO ONE PER COMMAND***

***THE COST WAS FOUND BEFORE IT WAS PAID.*** With an administrator elevated at
**login**, `sd-elevate.ps1 -Start` runs on every `sd.exe`; its `exit 0`
shortcut needs `IsInRole(Administrator)` on the **process** token, which is
False for an *unelevated* administrator because UAC hands out a filtered token
with Administrators deny-only. So it fell through to `Start-Process -Verb
RunAs` and **prompted every time** — and 13 of the suite's unelevated
verifiers pipe straight into `sd.exe` with no `LOGTO` at all.

**`sudo` does not help and was measured, not assumed**: its own help says it
*"will prompt for confirmation with a User Accounts Control dialog"* on every
invocation — no cache, no ticket, unlike Unix. It also **ships**, and `sd.iss`
deliberately neither installs nor enables it because Windows 10 and Server have
none. PROJECT_STATUS.md:4811 reached this on 14 Aug: *"`sudo sd` is the
convenient spelling, not the mechanism."*

***THE FIX IS THE SHAPE CLAUDE.md ALREADY NAMES*** — *"remove the need for a
prompt, not the step"*. The pipe was `sd-elev-<logname>-<userno>`; dropping
`@userno` lets a second session find the first one's helper through `PING` and
ask for nothing.

| | |
|---|---|
| **the lifetime rule is generalised, not deleted** | the helper still dies with its sessions — it just has more than one. `PING <pid>` registers, `STOP <pid>` deregisters, and it exits when the **last** owner goes |
| ***`-Run` carries the pid too, and that is not tidiness*** | a session reaching SDSYS while a helper already runs never calls `-Start`, because START short-circuits — so `-Run` is the only place it ever announces itself |
| ***`STOP` had to stop meaning "stop"*** | CPROC calls `elevate('STOP')` every time a session leaves SDSYS; with one helper per user that would take the privilege from everyone else. A **bare** `STOP` still stops it outright, for a cleanup |
| **a hashtable, not an array** | PowerShell's `+` on an array splits or folds an element depending on which side the literal is; keying by pid cannot do either, and a duplicate `STOP` is silently fine |
| ***the NAME widened and the ACL did not*** | the pipe DACL still grants exactly one SID, this user's — so no other account can reach it to register a pid or send it a script |

***WHAT THIS DOES NOT FIX, AND IT IS THE LARGER HALF.*** Those 13 verifiers
mean *"run `sd` as an ordinary user"*, which works today only because the owner
is an administrator **with an ordinary account** — a combination clause 2
abolishes. **The suite needs a real non-administrator account for that half**,
whatever the prompt count. Harness work, separable, not started.

### ***THE `sdusers` GATE WOULD HAVE KILLED THIS ON THE FIRST INSTALL***

Found 29 Aug 2026 by reading, before any cycle was spent. `LOGIN:380` refuses
anyone not in `sdusers`, and **it runs before the account is chosen** — while
clause 2 gives an administrator no account, so nothing ever adds them to that
group. **An administrator would have been refused at the door, before the case
that sends them to SDSYS.**

**The exemption is the fix and its argument is the one already in the file**:
internal mode is exempt there because SDSYS *"requires an elevated session …
a strictly harder test than sdusers membership"*. An exempted administrator can
reach exactly one place — SDSYS, which asks UAC — and `sd -Aname` is refused
for any account that is not your own (10051), which an administrator with no
account cannot name.

***AND IT IS THE RIGHT SHAPE RATHER THAN "ADD ADMINISTRATORS TO `sdusers` AT
INSTALL"***, which would cover only the administrators who existed when the
installer ran; one promoted afterwards would be refused for a reason nobody
would think to look for.

### ***31 PROBABLY CLOSES WITH THIS AND NEEDS NO EDIT OF ITS OWN***

`verify-apiadmin`'s control fails because `os_permitted()` falls through to
`os.users/don`, and `don` is listed only because `adopt` makes him an
ADMINISTRATOR-tier account and `grant.os.access` fires. **Stop adopting and the
record is never written, so the control's original `expected False` becomes
right again** — 31 closes for free. **Keep adopting and 31 needs its assertion
inverted after all.** The `adopt` ruling below therefore decides 31 as well.

### ***REVERSAL 1 — 15 Aug 2026, "NOBODY LOGS IN TO AN ACCOUNT BUT THEIR OWN"***

`LOGIN:400-420` carries the rule and names what it deleted: *"'sd' elevated
with no account named went to SDSYS. **The second case is deleted outright.**"*
**This restores precisely that.** The 15 Aug reasoning was *"an administrator
has access to all accounts, once they have logged into SD, not before"*; the
new model answers it differently — an administrator's login **is** the
elevation, so there is no "before" to protect.

### ***REVERSAL 2 — ADMINISTRATORS LOSE ssh, AND THAT IS A CONSEQUENCE RATHER THAN A CHOICE***

UAC draws its consent dialog on the interactive desktop and an ssh session has
none, so `!elevate` fails there (`ELEVATE`'s header, `CPROC:2598`, §5.6.2).
Under this model an administrator has no account of their own to fall back to,
so **SD refuses an administrator over ssh entirely.** Today `don` can ssh in
and after this he cannot. **Clause 3 is the answer** — an administrator who
wants ssh creates a personal account like anyone else — and it is consistent
with §5.6.2, *"local terminal access is for administrators"*. Stated because it
is a behaviour change nobody would predict from the ruling's words.

### ***REVERSAL 3 — PRE_RELEASE 2, A CLOSED B, IS RE-OPENED***

See entry 2. `os.users` is keyed on the **person** and survives a `LOGTO`, so
listing administrators there grants in every account the thing clause 5 takes
away; and the ADMINISTRATOR-tier account it attaches to is abolished by clause
2. **`os.users` survives for non-administrators** — only the administrator
grant is withdrawn.

### ***THE NEW GATE, AND WHY IT IS NOT REDUNDANT — MEASURED 29 Aug 2026***

The owner asked: *"a non administrative user is never allowed into SDSYS?"*
**Today they are.** `elevate('START')` gates on `Start-Process -Verb RunAs`
succeeding (`gplbld/sd-elevate.ps1:120`) and **nothing tests who is signed
in**. That verb gives an administrator a *consent* prompt and a standard user a
*credential* prompt — so a non-administrator holding an administrator's
password reaches SDSYS. The `IsInRole(Administrator)` at `:103` is the
"already elevated, nothing to launch" shortcut, **not a gate**.

***AND THE TRAIL RECORDS THE WRONG PERSON WHEN THAT HAPPENS***: the helper runs
as the administrator whose credentials were typed, while `@logname` and
`audit_message()` still say the standard user, so `ELEVATION GRANTED` is
attributed to somebody who did not consent.

**`IsAdmin()` (`gplsrc/linuxlb.c:88`) is the test, and it already exists with
NO CALLERS AT ALL** — defined, declared at `op_kernel.c:54`, called nowhere.
It asks `getgrouplist` (*is this ACCOUNT an administrator*) rather than
`getgroups` (*is this PROCESS elevated*), which is the question this gate needs;
the two were measured against each other on 14 Aug 2026 in one unelevated
administrator session — `getgroups` no, `getgrouplist` yes.

***IT MUST CARRY THE `CN_SOCKET` GUARD, AND THAT IS NOT OPTIONAL.*** `IsAdmin()`
reads `getpwuid(getuid())` — the **real** uid. An API session is `fork()`ed by
the LocalSystem service and `AssumeUserIdentity()` (`win32s4u.c:178`) changes
only the **effective** uid, so `getuid()` stays SYSTEM and `IsAdmin()` answers
TRUE for every remote client. **That is the identical shape of the hole
`kernel.c:240` closed on 21 Aug**, where `IsElevated()` was true for every API
session for the same reason, and its guard is the one to copy.

### Left to settle

- **`IsAdmin()` is C and both gates are BASIC**, so it needs exposing — a new
  kernel key beside `K$ADMINISTRATOR` (26), which is `keys.h:137` and
  `INT$KEYS.H:101`.
- ***RULED AND THEN REVERSED THE SAME HOUR, 29 Aug 2026. THE ANSWER IS THREE
  TIERS: THE ADMINISTRATOR TIER STAYS.*** *"we need three tiers because we
  create accounts in SD not in windows except for the installer, and that is
  correct. If an Administrator account is created outside of SD it does not
  have access to SD until a matching SD administrator account is created. That
  is the better approach and one I had forgotten about."*

  ***THE FIRST ANSWER WAS "Two tiers", AND THE FINDING BELOW IS WHAT REVERSED
  IT.*** `CREATE.ACCOUNT … ADMINISTRATOR` making a Windows administrator was
  put to him as a contradiction with 56; he read it the other way round, and he
  is right: ***SD CREATING THE WINDOWS ACCOUNT IS THE DIRECTION THE DESIGN
  WANTS.*** SD is the authority for who administers SD, and the tier is the
  mechanism. **Nothing was built, so nothing had to be undone** — the trace
  below stands as the record of what the tier does and is kept for that.

  ***AND IT LEAVES ONE PROPERTY TO SETTLE, BECAUSE THE CODE DOES NOT DO WHAT
  THE SECOND SENTENCE SAYS.*** *"an Administrator account created outside of SD
  does not have access to SD until a matching SD administrator account is
  created"* — **measured, that is not today's behaviour**:
  - `LOGIN:513` — `case kernel(K$OS.ADMINISTRATOR, 0)` sets
    `initial.account = 'SDSYS'` and reads **SDSYS's** register record. It never
    looks for a record belonging to the person.
  - `LOGIN:398` — the `sdusers` gate is skipped outright when
    `K$OS.ADMINISTRATOR` is true.

  So **any** Windows administrator reaching `sd.exe` gets SDSYS on a UAC
  consent, with no SD-side account anywhere. Over **ssh** they are refused in
  practice, because `elevate('START')` cannot raise UAC without a desktop
  (10002) — but **at the console they are in.**

  ***BE HONEST ABOUT WHAT SUCH A CHECK COULD BUY.*** A Windows administrator
  can add themselves to any group, read the data tree directly, or run as
  SYSTEM, so a matching-account requirement is **an explicit act and an audit
  trail, not a boundary that holds against them**. That is still worth
  something and may be exactly what is wanted — but it should be chosen knowing
  it is a speed bump.

  ***RULED 29 Aug 2026: RESTORE THE PERSONAL ACCOUNT. THIS REVERSES 56's
  CLAUSE 2.*** The owner's own words are the design, and they explain the
  mechanism: *"that is precisely why administrators also had a personal
  account. They got SDSYS in one of two ways, by starting SD in an elevated
  session or by logging to SD after logging into their personal account."*
  He also extends the property to every tier: *"if any are built outside of sd
  they do not have access to sd until a matching standard or programmer account
  is created in SD."*

  ***THE PROPERTY ALREADY HOLDS FOR STANDARD AND PROGRAMMER, AND THE CODE SAYS
  WHY IT DOES NOT FOR ADMINISTRATORS.*** `LOGIN:399`'s
  `is_grp_member(lgn.id,'sdusers')` refuses a Windows account made outside SD
  with **5009, *"This user is not registered for SD use"***. The exemption at
  `:398` was added by 56 itself, and its own comment states the causation:
  *"the model gives an administrator no account of their own — so nothing ever
  puts them in sdusers, and they would be refused here"*. **Restoring the
  account removes the reason for the exemption.**

  ***FOUR CONSEQUENCES, AND THE FIRST CANCELS QUEUED WORK.***
  1. ***THE `adopt-account` REMOVAL IS CANCELLED.*** It is ruled unnecessary
     further down this list on the reasoning that an administrator *"can login
     to sd and is logged into the sdsys account"* — **which is exactly the
     clause now reversed.** Adopt is how the installing administrator gets the
     personal account, so it is NECESSARY. ***DO NOT DO THE 20-FILE
     REMOVAL***, and strike that ruling rather than leaving two live rulings
     that contradict each other.
  2. ***BUILT AND CYCLED 29 Aug 2026 — `LOGIN`'s administrator exemption is
     gone*** and the `sdusers` gate is uniform across all three tiers
     (`LOGIN:414`, `if not(kernel(K$INTERNAL,-1)) then`). `-INTERNAL` stays
     exempt: it is the bootstrap, and it is the door `adopt-account.ps1` uses,
     so a failed adopt is a setback and not a lockout.
  3. ***BUILT AND CYCLED 29 Aug 2026 — the SDSYS case tests ELEVATION, not
     personhood.*** `LOGIN:568` reads
     `case kernel(K$ADMINISTRATOR, -1) and kernel(K$OS.ADMINISTRATOR, 0)`, and
     an unelevated administrator falls through to `case 1` and lands in their
     own account. Two explicit routes, as ruled. **The first key is the
     process-start seed and is the mechanism; the second is belt to its
     braces** — see the measurement below, and do not reduce it to one key,
     because `K$OS.ADMINISTRATOR` alone is TRUE for the very case that must not
     come here. ***A SIDE EFFECT WORTH NAMING: ADMINISTRATORS KEEP ssh***,
     which the morning's model had taken — an ssh session is never elevated, so
     it lands in the personal account like anybody else.
  4. **The `ADMINISTRATOR` tier stays** (three tiers), and `CREATEA:1571`'s
     adopt default keeps giving the installer that tier.

  ***MEASURED 29 Aug 2026 — THE MECHANISM EXISTS AND NO NEW KEY IS NEEDED.***
  `gplbld/probe-osadmin.ps1`, run twice from the same account:

  | | unelevated | elevated |
  |---|---|---|
  | `WindowsPrincipal.IsInRole` (Win32 control) | False | True |
  | `getgrouplist()` holds 544 → **`IsAdmin()`** | **TRUE** | **TRUE** |
  | `getgroups()` holds 544 → **`IsElevated()`** | **FALSE** | **TRUE** |
  | `K$OS.ADMINISTRATOR` (`op_kernel.c:456`) | TRUE | TRUE |
  | `K$ADMINISTRATOR` **as seeded** (`kernel.c:240`) | **FALSE** | **TRUE** |

  ***THE WARNING WAS RIGHT: `IsAdmin()` IS TRUE UNELEVATED***, so it cannot
  carry clause 3 on its own. **`IsElevated()` is the discriminator**, and SD
  already exposes it: `K$ADMINISTRATOR` is seeded from it at process start, so
  reading `kernel(K$ADMINISTRATOR,-1)` **at `LOGIN`'s `begin case` (`:420`)**
  answers *"is this session already elevated"*. The two keys differ there and
  only there — after `LOGIN:615` they are both TRUE.

  ***THE SEED SURVIVES TO `:420`, ESTABLISHED BY GREP RATHER THAN ASSUMED.***
  The BASIC layer has exactly three live writers of the flag — `LOGIN:615` and
  `CPROC:2769`/`:2781` — and both `CPROC` sites are in the `LOGTO` path, which
  cannot run before `LOGIN`. (`APISRVR:1204`/`:1206` are commented out.)

  ***SO A BASIC PROBE IN AN ACCOUNT CANNOT ANSWER THIS AND WOULD SAY THE
  OPPOSITE.*** `LOGIN:615` sets the flag for anybody who reached SDSYS, which
  today is every administrator elevated or not (`:513`) — such a probe reads 1
  in both legs and reports *"no discriminator exists"*. That is why the
  instrument measures `getgroups()`/`getgrouplist()` directly, through the MSYS2
  runtime `sd.exe` is built against; `probe-osadmin.c`'s header has the rest.

  ***`CREATE.ACCOUNT … ADMINISTRATOR` MAKES THE USER A WINDOWS ADMINISTRATOR.***
  `CREATEA:813` → `make.admin` → `os_group("ADDMEM", "S-1-5-32-544", acc.uname)`,
  which is the **built-in Administrators group**. So under 56 that one command
  produces: a Windows administrator, who is elevated at login into SDSYS and
  therefore **never enters the account just created for them**; an account
  nobody will use; and `sdssh`/`sdapi` membership (`CREATEA:1588`) that 56 says
  they cannot use, having lost ssh. **It is not dead weight, it is a
  contradiction — and it is an SD verb that grants Windows administrator.**

  ***AND THE TIER'S EXTRA VERBS ARE ALREADY UNUSABLE WITHOUT THAT.*** Every one
  gates itself on the **person** being a Windows administrator —
  `CREATEA:251`, `DELACC:85`, `MODIFYA:167`, `GRANTA:95`, `UNLOCK:61` — so the
  tier can only ever be exercised by someone who, under 56, does not use
  accounts at all.

  ***THE FOOTPRINT: 15 TIER LITERALS IN FOUR BASIC FILES.*** `CREATEA` (6),
  `MODIFYA` (6), `LOGIN` (1), `TIERGATE` (1), plus `MODIFYA:1102`'s rank table
  and `newvoc/TIER.ADD.ADMINISTRATOR`. **The 52 `K$ADMINISTRATOR` and 5
  `K$OS.ADMINISTRATOR` uses are a DIFFERENT THING and must not be touched** —
  they ask whether the *person* is a Windows administrator, which is exactly
  what 56 keeps.

  ***AND IT MUST STAY READABLE EVEN AS IT STOPS BEING OFFERED — MEASURED.***
  `C:\ProgramData\SD\sdsys\accounts\don` carries **`ADMINISTRATOR` in field 5**
  today, because `CREATEA:1571` gives the adopted account that tier. The
  installed data tree is never upgraded (§6), so removing `ADMINISTRATOR` from
  `TIERGATE:132`'s `tg.tiers` would make `tier_allows` answer *"no usable
  tier"* for an existing account and break its `logto`. **So: stop OFFERING it
  in `CREATEA` and `MODIFYA`; keep RECOGNISING it in `TIERGATE`.**

  **Sequencing:** `CREATEA:1571` is the only remaining producer once the
  keyword goes, and it dies with the `adopt` removal below. Not bundled, for
  that entry's own reason — an install that breaks must have one candidate
  cause.
- **`verify-tiers.ps1` measures the tier** and will need the same treatment.
  Not yet touched.
- **The installer adopts the installing user as an account** (`adopt-account`).
  ***THAT RULING IS WITHDRAWN — 29 Aug 2026, LATER THE SAME DAY. `adopt` IS
  NECESSARY AND THE REMOVAL MUST NOT HAPPEN.*** It rested on the clause the
  owner has since reversed (*"they can login to sd and is logged into the sdsys
  account"*); with the personal account restored, adopt is **how the installing
  administrator gets one**. ***NOTHING WAS REMOVED, so there is nothing to put
  back*** — the entry above records why it was kept separate, and that caution
  is what saved it. **The struck text below is the withdrawn ruling, kept so
  nobody re-derives it:** ~~*"the installer has to be a windows administrator
  to install sd. Since they are an administrator they can login to sd and is
  logged into the sdsys account."*~~ It was the 20-file change — `sd.iss`'s post-install step and its
  `AdoptCode`/`PasswordStepWanted` wizard flow, `CREATEA`, `DELACC`,
  `stage.py`, and six verifiers. **Deliberately separated from the login
  change**: an install that breaks must have one candidate cause, not two.
  **Harmless meanwhile** — the account is simply never entered, because LOGIN
  now sends its owner to SDSYS.
- ***`MODIFY.ACCOUNT` still refuses `os-off`/`sh-off` for an ADMINISTRATOR with
  10106***, on the 27 Aug reasoning that the access cannot be taken away. With
  the `CREATEA` change there is now normally **nothing there to take away**, so
  the refusal answers a question nobody asked. **Not changed — it is a
  confusing message rather than a defect**, and it is one line either way.
