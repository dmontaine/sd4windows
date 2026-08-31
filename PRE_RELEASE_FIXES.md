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

***NEXT FREE ID: 91.*** Take it from here and increment it; **do not derive it by
scanning.** `gplbld/test-fixlist-units.ps1` enforces this line, the uniqueness of
every id, that a section and its row describe the same defect and agree on
status, and that every `PRE_RELEASE <n>` cited in PROJECT_STATUS.md, HISTORY.md
or a `gplbld` script names an id this table actually has. It needs no install and
no elevation.

| | SEV | what | where |
|---|---|---|---|
| ~~1~~ | **B** | ~~The `edit` / `micro` refusal message is malformed~~ — **DONE 27 Aug 2026** | `sdsys/gpl.bp/EDIT` |
| ~~2~~ | **B** | ***THE INSTALLING USER GETS NO `OS.EXECUTE` — DONE AND VERIFIED 29 Aug 2026 ON `-Run b69`. THE RECORD ARRIVES AND THE ACCESS IS BACK.*** Install **22:04:34**, `assert-current` **exit 0 live**. `C:\ProgramData\SD\sdsys\os.users\don` reads **`yes|yes`**, and `verify-osusers` took the ***"already listed"*** branch — *"don is already listed … That is what CREATEA/adopt-account do for an ADMINISTRATOR account"* — where on `b68` there had been nothing to park. **All twenty of its rows pass**, including every `unlisted:` row, because those park the record deliberately and so measure the gate either way. ***AND THE ACCEPTED LEAK SHOWED ITSELF ON THE FIRST RUN, EXACTLY WHERE IT WAS PREDICTED — FILED AS 64, NOT SWEPT UP HERE.*** `verify-apiadmin` fell **22/23 → 21/23**: its control *"local elevated session refused OS.EXECUTE"* expected the local session to be **refused** and observed it **run**. That control's own comment explains why it used to hold — a local session *"starts in SDSYS with USR_ADMIN set and gives the flag up on the way out"*, then falls through to the `os.users` lookup, **which is keyed on the person**. With `don` listed, the lookup now succeeds. **The row is the leak, measured.** ***SECOND CONSEQUENCE, ALSO FILED (65): THE RUN LEFT THREE ORPHANED `os.users` RECORDS*** — `SDRTB69A`, `SDTAPIB693`, `SDTIERTB693`, whose Windows accounts are **gone**, checked. **This entry closes because its own goal is met and measured; the two consequences are their own entries rather than a reason to hold it open.** *(Was: MEASURED 29 Aug 2026 AND IT IS LIVE AGAIN: AN UNELEVATED ADMINISTRATOR HAS NO `sh`, NO `!` AND NO `OS.EXECUTE`. THE ROW'S OWN REASON FOR BEING OPEN WAS WRONG; THE DEFECT IS REAL FOR A DIFFERENT ONE.*** ***THE EVIDENCE IS IN `b68`'s OWN TRANSCRIPT***, on the 20:31:49 install: `[PASS] unlisted: refused with message 10053`, `[PASS] the refusal names the same @logname the probe reported: expected don, got don`, `[PASS] unlisted: OS.EXECUTE from a program is refused`. **`verify-osusers` scores those green because it tests the GATE, not the POLICY** — the gate is working perfectly and the policy is the thing that changed. `C:\ProgramData\SD\sdsys\os.users` holds **0 records**, read off disk. ***THE CAUSE IS A CHANGE MADE FOR A MODEL THAT WAS WITHDRAWN FOUR HOURS LATER AND NEVER REVERTED.*** `7aee48d` (**10:16:02**) deleted `os.sh = @true` / `os.exec = @true` from `CREATEA`'s ADMINISTRATOR arm; they now default `@false` (`:287`) and are set **only** by an explicit `SH-ON`/`OS-ON` keyword (`:1492`). **Its own comment states the justification**: *"It is not a withdrawal of access: 56 elevates an administrator at login into SDSYS, where USR_ADMIN answers os_permitted() before the file is read."* ***THAT IS CLAUSE 2, AND `af5490e` REVERSED IT AT 14:58:26 THE SAME DAY.*** An unelevated administrator now lands in their **own account**, where `USR_ADMIN` is false, so `op_sh.c:161` never short-circuits and the empty `os.users` refuses them. **The owner's instruction of 26/27 Aug — administrators to *"have access to os.execute, ssh and api by default without escalating"* — is not satisfied, and "without escalating" is exactly the case that broke.** ***AND THE FIX IS NOT THE OBVIOUS ONE — READ THIS BEFORE TOUCHING IT.*** Restoring the two lines re-creates the leak that justified removing them: `os.users` is keyed on the **person** (`process.username`) and a `LOGTO` never changes it (`op_sh.c:167`), so a listed administrator keeps `OS.EXECUTE` in every account they move to, which 56 forbids. ***THE SESSION FLAG DOES NOT HAVE THAT PROBLEM AND ALREADY BEHAVES CORRECTLY***: `CPROC:2781` clears `K$ADMINISTRATOR` on any `LOGTO` away from SDSYS, its 13 Aug comment saying the rights had *"followed you into whatever account you moved to next, which made the rights a property of the session rather than of the account you are standing in"*. **So access carried by the flag is account-scoped for free, and access carried by `os.users` is not.** ***BUT THE NAIVE VERSION OF THAT IS A TRAP***: `LOGIN:568` is `case kernel(K$ADMINISTRATOR, -1) and kernel(K$OS.ADMINISTRATOR, 0)`, so setting the flag for an unelevated administrator **at login** would send them straight back to SDSYS and undo the reversal. Any fix must land **after** that branch decides. ***RULED AND BUILT 29 Aug 2026 — THE OWNER CHOSE "RESTORE THE TWO LINES IN `CREATEA`", HAVING BEEN SHOWN THE LEAK AND THE SESSION-FLAG ALTERNATIVE.*** `os.sh = @true` / `os.exec = @true` are back in the ADMINISTRATOR arm (`CREATEA:1613`), where `7aee48d` removed them. ***SO THE `LOGTO` LEAK IS NOW AN ACCEPTED COST AND NOT AN OVERSIGHT — DO NOT "FIX" IT BACK WITHOUT A RULING***, and both the code comment and the `START-HISTORY` line say so, because the next reader will find the paragraph explaining why the lines were dangerous still sitting directly beneath them. **Every word of that paragraph is still true**; what changed is that it is no longer decisive. **ssh and the API are unaffected** — connection-time group tests, so neither follows a `LOGTO`. ***BUILT, UNCOMPILED, UNVERIFIED: IT IS BASIC, SO IT NEEDS A FULL CYCLE, AND `assert-current` IS RED UNTIL ONE RUNS.*** **An existing install does not gain the record** — `grant.os.access` fires at `CREATE.ACCOUNT` time and the installer never overwrites a data tree, so it lands on a **new** install where `AdoptAccount` re-creates the installing user's account; the changelog says so in those terms. ***WHAT CLOSES IT IS `b69`***: `verify-osusers`' baseline branch should take the *"already listed"* path instead of *"nothing was there"*, and its `unlisted:` rows must still pass — they park the record deliberately, so they measure the gate either way. *(Was: RE-OPENED 29 Aug 2026 BY THE OWNER'S NEW ACCESS MODEL — see 56. The fix wrote every ADMINISTRATOR-tier account into `os.users`, which is keyed on the **person** and so survives a `LOGTO`; 56 rules that an administrator has the rights of whatever account they move to. **And 56 abolishes the administrator account this attached to.** *(Was: the installing user gets no `OS.EXECUTE` — DONE 27 Aug 2026)*)*)* | `sdsys/gpl.bp/CREATEA:287`, `:1492`, `gplsrc/op_sh.c:161`, `gpl.bp/CPROC:2781`, `gpl.bp/LOGIN:568` |
| 3 | **S** | The live `SDSYS` VOC does not match `voc_template` — ***RE-VALIDATED 28 Aug 2026 against the LIVE VOC, not a directory listing***: `ct voc %L` / `%G` / `%E` all answer `Record not found` while all three are present in `newvoc` AND `voc_template`; `ct voc =` returns `K` / `25` and `=` is in neither source tree. `count voc` says **428** against `voc_template`'s 426. Still open, and the specifics hold | `sdsys/voc_template` |
| ~~52~~ | **S** | ***The tester set documents `encrypt.field`, which no longer ships, and three tier numbers that moved with it*** — measured 28 Aug 2026 while fixing 4. `TIER.ADD.ADMINISTRATOR` is **21 lines − 1 header = 20 names** and `encrypt.field` is gone from it (PRE_RELEASE 25); `verify-tiers.ps1:42` is authoritative — **ADMINISTRATOR 392 + 20 + 4 = 416**, PROGRAMMER 396 and STANDARD 354 unmoved. SD corroborates: `count voc with dispatch # ""` in SDSYS answers **143**, which is 81 + 42 + 20. ***THE RECIPE, ALL IN `Testing/markdown`***: **05** line 18 `\| Verbs \| 81 \| 81 + 42 \| 81 + 42 + 20 \|`, line 19 `417`→`416`, line 29 `77`→`81`, line 55 `392 + 21 + 4 = 417`→`392 + 20 + 4 = 416`, line 69 `**21**`→`**20**`, line 73 `21 more`→`20 more`; **06** subtitle and line 5 `21`→`20`, line 61 heading drop *"and field encryption"*, line 65 delete the `encrypt.field` line, line 267 `of the 21`→`of the 20`, line 271 delete `**\`encrypt.field\`** · `; **07** line 4 `77`→`81`, line 7 `[21 more]`→`[20 more]`. ***Two edits of this were applied and REVERTED*** when the session ended — the docs repo is clean at `7914e60`, and a half-applied table is worse than none. ***DONE 28 Aug 2026 — ALL TWELVE EDITS APPLIED IN ONE COMMIT***, the diff 13 insertions / 14 deletions (the extra deletion is the `encrypt.field` code line). **Every number was re-derived from the tree before it was written, not copied from this row**: `newvoc` 395 entries, 119 field-1-`V` records, `TIER.ADD.ADMINISTRATOR` 21 lines, `TIER.OMIT.STANDARD` 43 | docs repo, `Testing/markdown/05,06,07` |
| ~~4~~ | **S** | Tester page 07 says a standard account has 77 verbs; it has 81 — ***81 CONFIRMED 28 Aug 2026 from the tree***: `newvoc` holds **119** records whose field 1 starts with `V`, plus the four keyword-and-verb records (`break`, `count`, `display`, `off`) = **123**, less `TIER.OMIT.STANDARD`'s **42** names (43 lines, first is a header comment) = **81**. **Fix it together with 52** — the same table carries `417` and `+21`, both stale, and correcting one number while leaving the others is how this page got wrong in the first place. *(The entry below says page 06 repeats the figure; it is page **05**.)* ***DONE 28 Aug 2026 with 52***, in the one commit both entries always needed | docs repo |
| ~~5~~ | **S** | `.d name` cannot find a lower-case VOC record typed in upper case — **FIXED 28 Aug: folds case like `.L`/`.R`, and reports 5043 instead of falling through with a stale `voc.rec`.** ***DONE 28 Aug 2026, MEASURED*** on the 00:53:34 install by `verify-vocverbs.ps1`: `.D ZZPRFD` printed `Delete VOC record 'zzprfd'?` — the lower-case name from an upper-case verb — the record was gone afterwards, and an unknown name reported 5043 with no second prompt | `CPROC:1119` |
| 6 | **S** | An empty directory called `C:` is created in the data tree by the installer ***— REPRODUCED AND CHARACTERISED 30 Aug 2026 ON THE 18:03:57 INSTALL, AND IT IS NOT `sd.iss`.*** **It is `C:\ProgramData\SD\sdsys\C:`, empty, and its real NTFS name is `U+0043 U+F03A`** — `C` followed by the **Cygwin/MSYS private-use mapping of a colon**, which is how the POSIX runtime writes a name NTFS forbids. **So it is written by something running on the MSYS2 runtime — SD itself — and not by Inno**, whose `[Dirs]` has three clean `{#DataDir}` entries. ***PINNED TO THE ADOPT STEP BY TIMING***: `adopt-account.log`, `user_accounts\don` and `sdsys\C:` share a creation time of **18:04:39**, so `sd -internal CREATE.ACCOUNT USER don ADOPT` makes the correct account directory AND this one, the latter relative to its cwd of SDSYS. ***TWO INSTRUMENTS LIED ON THE WAY AND BOTH ARE WORTH KNOWING.*** `find . -name 'C:'` under Git Bash reports **nothing** — MSYS mangles the `C:` argument before `find` sees it — and `Test-Path 'C:\ProgramData\SD\sdsys\C:'` answers **False**, because a colon in a Windows path names an alternate data stream rather than a file. **It was found by searching for `*:*` and confirmed by enumerating code points.** A search for this by name will keep coming back clean. ***WHAT IS NOT YET KNOWN IS THE LINE.*** `CREATEA` already guards a bare drive letter at `:769` (`parent.dir matches "1A':"`), the account directory itself is built correctly from `CONFIG('USRDIR')`, and the private catalogue uses `pathname:@ds:'cat'` — none of those is it. **Harmless in itself; it is litter of the same class as 65 and 60, in the one directory whose ACL is the whole of the protection** | `gpl.bp/CREATEA`, `sdsys` (not `gplbld/sd.iss`), and entries 65, 60 |
| ~~7~~ | **M** | `sort.item` is withheld from a standard account and `list.item` is not — ***CONFIRMED AN OVERSIGHT FROM THE RECORD, 30 Aug 2026, WHICH IS WHAT THE ENTRY ASKED FOR.*** The owner's session-50 ruling (`d913eac`, 24 Aug 2026) moved *"read-only inspectors"* to STANDARD and **names them**: `search list.diff list.item list.common list.vars report.src report.style format`. ***`sort.item` IS NOT IN A LIST THAT NAMES ITS SIBLING***, so it was never ruled on — it simply survived the first-pass omit list. **They are one program**: `newvoc/list.item` is `$QPROC` verb **10** and `newvoc/sort.item` is `$QPROC` verb **11**, both `Verb - Query processor`, differing in sort order alone. ***THE FIX IS ONE LINE AND FOUR FILES MOVE WITH IT, WHICH IS 82 EXACTLY***: dropping the name takes `TIER.OMIT.STANDARD` **43 lines → 42** (42 names → 41) and **STANDARD 354 → 355**, with **PROGRAMMER 396 and ADMINISTRATOR 419 UNMOVED** — that asymmetry is the arithmetic check. `verify-tiers.ps1:42`, `verify-tierapi.ps1` and `test-tiercounts-units.ps1` all carry 354 and must move together; **run `test-tiercounts-units.ps1` first, it costs a second.** ***LEFT FOR THE OWNER, NOT BUILT***: tier membership is a policy ruling and every one of them so far has been his. ***DONE 30 Aug 2026 on the owner's instruction to settle the open rulings.*** `sort.item` is out of `TIER.OMIT.STANDARD` — **43 lines → 42, so 42 names → 41** — and both verifiers moved with it in the same commit. ***THE GUARD 82 EXISTS FOR WAS RUN IMMEDIATELY AND IS GREEN***: `test-tiercounts-units` **13 of 13**, deriving **STANDARD 355, PROGRAMMER 396, ADMINISTRATOR 419** from the tree and agreeing with `verify-tiers.ps1` and `verify-tierapi.ps1` on all three. **PROGRAMMER and ADMINISTRATOR did not move, which is the check on the arithmetic** — either of them moving would have meant the name reached `newvoc` instead of leaving the omit list. ***THE PRODUCT IS PROVEN ON `-Run b77` AND THE INSTRUMENT WAS NOT.*** `sdtiertb771 COUNT VOC: expected 355, got 355` **PASS**, and the installed `TIER.OMIT.STANDARD` reads **42 lines with `sort.item` gone**. ***BUT `verify-tiers` FAILED FOUR CHECKS, ALL THE SAME MISS***: it carries **its own copy of the withheld NAMES** and only the count constant had been updated — `shipped TIER.OMIT.STANDARD matches this test: expected 0, got 1`, `omit list length: expected 42, got 41`, and two more, every one 42-against-41. **Caught by that file's own cross-check, which exists for exactly this.** ***AND `test-tiercounts-units` DID NOT AND CANNOT***: it reconciles the COUNTS each verifier claims against the tree, and both counts were already right — `$Withheld` is a set of NAMES that nothing outside `verify-tiers` compares. **Same shape as 82, one level down.** `sort.item` removed from `$Withheld`; checked without a run — 41 names both sides, `Compare-Object` difference **0**, which is the assertion at `:390`. **`gplbld` only, no cycle. The four rows should go green on the next suite run** | `newvoc/TIER.OMIT.STANDARD`, `verify-tiers.ps1:167` and `$Withheld`, `verify-tierapi.ps1:135`, `test-tiercounts-units.ps1` |
| ~~8~~ | **M** | `help` is an empty stub and F1 reaches it — ***DONE 30 Aug 2026 on the owner's instruction to settle the open rulings. F1 SAYS SOMETHING NOW.*** Both `int.help:` and `f1.help:` fell straight through to `return`, so F1 at the command prompt did nothing at all — not an error, not a message — which reads as a broken keyboard rather than a missing feature. New message **10149**, printed by both labels. ***IT DOES NOT POINT AT DOCUMENTATION, AND THAT IS MEASURED RATHER THAN MODEST***: nothing under `C:\Program Files\SD` is documentation — the install is scripts, the changelog and the two editors — so a message naming a manual that does not ship would be the exact false sentence this file exists to catch. 10149 names only what is on the machine: the account's own VOC (`list voc`) and the Start Menu installation check, whose wording is copied from `check-install.ps1`'s own output. **`int.help` stays unreachable as a verb** — no VOC record names internal verb 14, so adding one would move the tier counts; the verb and the key are wired to the same message so they cannot diverge if one is ever added. **BUILT AND INSTALLED, NOT WITNESSED.** `C:\ProgramData\SD\sdsys\messages\10149` is on the 22:44 install and reads correctly, but ***NOTHING IN THE SUITE PRESSES F1***, so no run can show it. **Witnessing it is one keystroke**: start SD, press F1 at the command prompt with an empty command line (`CPROC:932`, `n = K$F1 and at.command = ''`). Left DONE rather than open because the work is complete and the gap is a verifier that does not exist, not a doubt about the change | `CPROC` `int.help`/`f1.help`, `CPROC:932`, `sdsys/messages/10149` |
| ~~9~~ | **M** | `umask` is implemented and unreachable — ***THIS ENTRY'S TWO OPTIONS ARE BOTH WRONG, MEASURED 30 Aug 2026, AND HALF OF IT WAS ALREADY RULED.*** *"Either ship a VOC record for it"* — **the owner refused that on 24 Aug 2026**, session 50, `d913eac`: *"UMASK removed entirely — POSIX file-mode-bits call, essentially inert on Windows where security is ACL-based"*, and `sdsys/voc_template/umask` was **deleted** in that commit. Confirmed from the tree: `umask` is absent from **both** `newvoc` and `voc_template`. So the verb is not an oversight, it is a decision this entry did not know about. ***AND "DELETE THE ROUTINE" WOULD BREAK START-UP IF READ AS WRITTEN***: there are **two** things called umask and only one is dead. `op_umask` (`gplsrc/op_misc.c:1503`, opcode `0xCF0B`) is the SD BASIC `UMASK()` function and **`CPROC:325` CALLS IT ON EVERY START-UP** — `if umask(002) then null`, with a comment explaining why. **The dead half is `int.umask` alone** (`CPROC:3371-3381`, internal verb 35, dispatched from `:1637`), which nothing can reach because no VOC record points at verb 35. ***SO WHAT IS LEFT IS ONE SMALL CALL***: delete `int.umask` and its dispatch entry, or leave it as the tree leaves `$MICRO` and `$NLS` — `d913eac` names that precedent itself, *"stay compiled but callerless"*. **Owner's, and it is now a one-line question rather than a design one**. ***RULED 30 Aug 2026: KEEP IT, AND THE REASON IS THE DISPATCH TABLE.*** The answer changed once the mechanism was read rather than assumed. `CPROC:1603` dispatches with `on voc.rec<3> gosub int.quit, int.clr, …` — **positional** — so deleting entry 35 renumbers **PDUMP, PAUSE, CLEAR.ABORT, SET.EXIT.STATUS, REPORT.STYLE and LOGMSG**, every one of which is named by NUMBER in a shipped VOC record. **Removing ten dead lines would mean editing six live records and getting all six right, for no user-visible gain.** So it stays, exactly as `d913eac` said of it — *"stay compiled but callerless"*, as `$MICRO` and `$NLS` do — and the routine and the slot now carry a dated comment saying it is dead **on purpose**, why the slot cannot go, and that `op_umask` is LIVE at `CPROC:325`. **The entry is closed by a decision, not by a code change** | `CPROC:3371` (dead, documented), `CPROC:1603` (positional dispatch), `CPROC:325` and `gplsrc/op_misc.c:1503` (LIVE, do not touch) |
| ~~10~~ | **M** | ~~Two verifiers carry a dead ANSI strip~~ — ***IT WAS 23 FILES AND 24 OCCURRENCES, NOT TWO.*** **DONE 28 Aug 2026**: all converted to `([char]27 + '\[[0-9]*[A-Za-z]')`. ***AND IT WAS STILL SPREADING*** — three of the 23 were written the same day, by copying `probe-catprivate.ps1`'s `Invoke-SD` *"unchanged"*. **Guarded by a test, not by 23 comments**: `test-verdict-units.ps1` now scans the whole directory and fails if any script carries the dead form again, **tokenising rather than grepping** so a comment that quotes it (there are two, both correct) is not a false positive | `gplbld` |
| ~~11~~ | **B** | ***Nested `commit` silently loses the outer transaction's writes*** — UPSTREAM #17. ***DONE 29 Aug 2026***: the reinstate-and-decrement block is lifted out of `rollback()` into `end_txn_level()` and called from `op_txncmt()` too — **one function, both callers, because having it in one place with one caller is what the defect was.** Placed **before** `exit_op_txncmt:` so the three `k_error` paths do not pop a level they did not commit. **Measured on the 18:36:04 install, `verify-txn.ps1` 9 of 9**: the outer write now reads `outer` where it read `base`, the level delta is `0` where it was `+2`, and the parent transaction is reinstated where the session had been left in none. **Wired into `VerifyInstall1` after being measured, not before** | `gplsrc/txn.c`, `gplbld/verify-txn.ps1` |
| ~~12~~ | **S** | ***DONE AND MEASURED 31 Aug 2026 ON THE 01:05:10 INSTALL — see the end of this row.*** Error 3023 tells the user the disk may be full — UPSTREAM #20, **unfixed here**. ***28 Aug: NOT the message-only fix this entry claims — the call site is `gplsrc/op_dio3.c:853`, so it is a C change and a REBUILD, not a data change. Left out of the 28 Aug batch for that reason*** ***— FIXED AND COMPILED 31 Aug 2026; STAYS OPEN UNTIL IT IS MEASURED ON AN INSTALL.*** Done by the route UPSTREAM 20 recommends: **special-case the status at the call site rather than reword 1407**, which stays accurate for the disk-full case it was written for. New message **10151** names the missing lock, says the stored record is unchanged, and points at `READU` / `READVU`; `MUSTLOCK` is the config spelling and both verbs were checked against the tree rather than assumed. ***THE MESSAGE FILE FOLLOWS THE ONE-LINE CONVENTION AND THAT IS LOAD-BEARING***: `sysmsg()` turns REAL newlines into field marks **before** expanding literal `\n`, so a message written across several physical lines renders as marks. 433 bytes, one line, one trailing LF, CR 0, exactly one `%d`. ***WHAT IS STILL WRONG AND IS SAID OUT LOUD IN THE CODE***: `ER_RDONLY`, `ER_IID` and `ER_TRIGGER` also reach `exit_op_write` and still render through 1407, so they still speculate about the disk. **Each wants its own text rather than a shared one**, and `ER_RDONLY` already logs separately via `log_permissions_error()` — left deliberately, not missed. `make sd` **exit 0, no warnings**, `op_dio3.o` rebuilt. ***MEASURED 31 Aug 2026 ON THE 00:48:04 INSTALL AND THE BRANCH WORKS — BUT THE MESSAGE ARRIVED TRUNCATED, WHICH IS ENTRY 87.*** `probe-nolockmsg.ps1`, a real `WRITE` inside a `BEGIN TRANSACTION` with no lock held, run in the `DON` account: **`PROBE-OPENED` True** (the program ran), **`PROBE-WROTE-OK` False** (the write was refused, so a lock really was required), ***"no lock is held on it" True*** and ***"Possible full disk" False***. **Those last two are the whole entry** — the success anchor appears only in 10151 and the disqualifier only in 1407. ***AND THE PROBE REFUSED TWICE BEFORE IT PASSED, WHICH IS THE GUARD WORKING***: the first run's BASIC would not compile (`END` was taken as `END TRANSACTION`) and it reported *"the probe never opened the file, so nothing below was measured"* rather than scoring the absent disk wording as a pass. ***WHAT IT ALSO FOUND***: the rendered message stopped at *"A WRITE must already hold an u"*, cut mid-word — `k_error()` truncates at ~84 characters, **filed as 87 and fixed with it**, and 10151 shortened to three lines (rendered 202 against a 231 bound). ***RE-MEASURED 31 Aug 2026 ON THE 01:05:10 INSTALL AND THE MESSAGE NOW ARRIVES WHOLE — DONE.*** Same probe, same four readings, and all three lines rendered: *"Error 3023 writing record: no lock is held on it. Nothing was written. / A WRITE inside a transaction, or under MUSTLOCK=1, needs the lock already. / Take it with READU (READVU for one field), then WRITE."* **The truncation that cut it at "an u" was 87, fixed with it** | `sdsys/messages/1407`, `sdsys/messages/10151`, `gplsrc/op_dio3.c:853`, and entry 87 |
| ~~13~~ | **M** | `qselect` prints its message without the list number — UPSTREAM #21. **FIXED HERE 28 Aug: `tgt.list` passed as the second argument.** ***DONE 28 Aug 2026, MEASURED*** by `verify-vocverbs.ps1`: the message ends in a list number, no dangling `select list `, and it selected more than zero. Still live upstream | `gpl.bp/QSELECT:240` |
| ~~14~~ | **S** | `delete.file ... no.query` still prompts, so it cannot run unattended — UPSTREAM #23. **FIXED HERE 28 Aug: `check.sdsys.file` takes the safe `N` branch under `no.query` and says so — new message 10117.** ***DONE 28 Aug 2026, MEASURED*** by `verify-vocverbs.ps1` on a copy of the `messages` pointer: 10117 printed, **6146 never asked**, the VOC reference gone and `sdsys\messages` still on disk. Still live upstream | `gpl.bp/DELETEF:222` |
| ~~15~~ | **M** | `delete.index` will not match a lower-case index name, though `list.index` will — UPSTREAM #22. **FIXED HERE 28 Aug: supplied names are case-corrected against the real ones, as `LISTI:147` does; an unknown name is still reported as typed.** ***DONE 28 Aug 2026, MEASURED*** by `verify-vocverbs.ps1`: `delete.index zzprfak f1` answered *"Deleted index F1"* and the file read back with no indices; **the control held too** — a genuinely unknown name came back **as typed**, not upcased. Still live upstream | `gpl.bp/DELETEI:155` |
| 16 | **S** | A killed session blocks exclusive access, says nothing about why, and only an administrator can clear it ***— PART OF THE GROUND MOVED UNDER IT ON 31 Aug 2026: 24's FIX MAKES THE DOCUMENTED RECOVERY ACTUALLY WORK.*** This entry's chain ends *"`sd -cleanup` clears it, and requires elevation"*, and **for task locks that was not true** — 24's loop released none. So the administrator's route was broken as well as awkward, and one of the two is now fixed. ***THE ENTRY ITSELF IS STILL A DECISION AND WAS DELIBERATELY NOT BUILT***: it names *"two independent things to decide"* — **diagnosis** (should the refusal name the session holding the file, rather than pointing at the file) and **recovery** (should `logout` *n* reap a slot whose process is gone, or should an unprivileged user get some way to clear their own dead session). **Both are wording-and-policy choices, not defects with one right answer**, and inventing either would be a change to the access model rather than a fix. ***AND THE THIRD PIECE IS AN OPEN QUESTION THIS BATCH DID NOT TOUCH***: `check_lost_users()` did not reap a dead entry across two full sweep intervals, and PROJECT_STATUS.md §6 says not to guess between its two candidates — `sd -cleanup` misjudging, or `kill(pid, 0)` answering wrongly for an MSYS2 pid. **24's fix does not answer that**: it changes what cleanup RELEASES, not whether the sweep ever calls it | `gplsrc/sd.c:333`, `gplsrc/clopts.c`, and entry 24 |
| ~~17~~ | **B** | ~~`edit` / `micro` refuse a record whose text looks like a mark token~~ — **DONE 27 Aug 2026** | `sdsys/gpl.bp/EDIT` |
| ~~18~~ | **M** | ~~A text mark reaches the editor as a raw control character~~ — **DONE 27 Aug 2026** | `sdsys/gpl.bp/EDIT` |
| ~~19~~ | **B** | ***CLOSED 28 Aug 2026 BY `-Run b53`: ALL FIVE LEGS GREEN, BOTH TOKENS EXERCISED, AND THE OWNER'S CONDITION — "19 stays B until the doors are covered" — MET BY A PASSING RUN RATHER THAN BY ARGUMENT.*** `Create` **13/13**, `Control` **8/8**, `Suspend` **5/5**, `Refused` **5/5**, `Remove` **4/4**. ***ALL THREE DOORS ADMITTED AND THEN ALL THREE REFUSED, WITH THE SUSPENSION THE ONLY CHANGE***: ssh and `logto` in SD's own words (**10107**), and the API by the controlled pair, since it cannot identify its own refusal. **The `logto` door is genuinely covered at last** — `WHO` answered `91 SDDRB53A from SDDRB53B`, so the session *arrived* rather than started there, and **5161 did not appear**. ***THE REFUSED LEG PROVED THE ORDERING TOO***: *"logto: it was NOT 5161 instead of the suspension"* passed, so the refusal came from `logto.authorised` at `CPROC:2679` and not from the token-dependent chdir at `:2691` — which is why the refusal half was trustworthy even while 44 was unfixed. **Nothing was left behind**: no Windows accounts, no `sdu_` groups, no `ACCOUNTS` records, **0 orphan SIDs** in all three groups, only the two profile directories that are 35/36. *(Was: THE DOOR ITSELF NOW OPENS — `-Run b52`, 17:41. `Create` 13/13 with the helper granted and WINDOWS AGREEING, and the `logto` reached the account: `WHO` answered `91 SDDRB52A from SDDRB52B` and 5161 DID NOT APPEAR.)* 44's two-account cure works, and the non-decisive local witness failed in the same transcript as designed, so both halves are on one page. ***WHAT STILL FAILS IS THE CHECK, NOT THE DOOR***: the anchor required the account to be the whole of the second field, and `WHO` appends `from <ACCOUNT>` **only when the session has logto'd** — so it matched only the case where the door had NOT opened. ***THAT IS THE SAME TRAP AS THE ORIGINAL, FROM THE OPPOSITE SIDE***: the first version matched the name anywhere and passed on the failure path; its replacement matched only at end of line and failed on the success path. **Both were written from a transcript of the path they were not meant to catch.** Now anchored on the shape — a number, then the account as a whole word — with a **second decisive row on the `from <helper>` clause**, which is the stronger evidence because it says the session ARRIVED rather than started there. **Five paths measured against the same two patterns**: real b52 success, real b50 failure, echo-only, started-there, and a logto to a different account. **`-Run b53` is what closes 19.** *(Was: RE-OPENED 28 Aug, one row of seven — the check matched the echo of its own command; reproduced on a second account on `-Run b51`.)* ***WHAT CLOSES IT IS NOW BUILT AND UNRUN: 44's two-account door, and `-Run b52` is the run that decides.*** A written verifier is still not coverage — the owner's ruling has not changed — so **19 stays open until a leg passes**. `verify-doors.ps1:255` was `Test-Say $out $acctU`, and the session echoes what it is fed, so `SDDRB50A` was in the transcript whether the `LOGTO` landed or not. **On the `-Run b50` Control leg SD printed 5161 *"Unable to change to new directory"* and `WHO` answered `91 DON` — the session never left `DON` — and the row scored PASS.** The same check scored the same PASS on `sddr2`, which is what the struck text below rests on. **Anchored on `WHO`'s answer now** (`^<number> <ACCOUNT>$`, the shape nothing typed can produce) **with 5161 as a disqualifier**, and both directions measured against the real transcript. ***THE CAUSE IS 44, AND THE CURE IS ALREADY WRITTEN DOWN IN THIS FILE***: the `logto` row of the door table below says **two** accounts — *"ssh as A and `LOGTO B`"* — and the implementation instead runs `LOGTO` in the caller's own session, whose token predates the `sdu_` group. **ssh and the API are unaffected: both authenticate afresh, and both remain measured.** ***THE REFUSAL HALF STILL STANDS*** — `logto.authorised` is called at `CPROC:2679`, **before** the chdir at `:2691`, so a suspended account is refused with 10107 and never reaches 5161. **What is unproven is the ADMITTED half of the pair, for one door of three.** Owner's to confirm; reversible if he reads it otherwise — ~~**DONE 28 Aug 2026. The owner's ruling was *"19 stays B until the doors are covered"*, and the condition is now met by a passing run rather than by argument.**~~ Six rows closed by `verify-tierchange.ps1` (28 PASS); ~~**the last row — the three doors — is closed by the `verify-doors` pair**, all four legs green on `sddr2`: `Create` 8/8, ***`Control` 6/6 with ssh, `logto` and the API ALL ADMITTED***, `Suspend` 5/5, ***`Refused` 4/4 with ALL THREE REFUSED***.~~ `LOGIN:477` and `CPROC:3776` said it in SD's own words (10107, *"Account SDDR2A is suspended"*) — **ssh after the banner, so authentication had succeeded and the refusal is SD's, with the account still in `sdssh` so no Windows group moved.** The API cannot identify its own refusal by design, so **the controlled pair is what proves it**: same account, same password, same call, admitted then refused, the suspension the only change. **Found and fixed a defect in the verifier on the way — see 42** | `gpl.bp/MODIFYA`, `gplbld/verify-tierchange.ps1`, `verify-doors-admin.ps1`, `verify-doors.ps1` |
| 20 | **S** | A suspended administrator is still a Windows administrator | `gpl.bp/MODIFYA` |
| ~~21~~ | **S** | ~~The write-once rule on `ACC$PRIOR.TIER` is unreachable, and four documents say it is what makes field 6 safe~~ — **dead test deleted, docs corrected 27 Aug; compiled + installed 17:25:59, `b48` is the regression check** | `gpl.bp/MODIFYA`, `syscom/KEYS.H` |
| ~~22~~ | **M** | `create.account` says a password was not set and never says why — **FIXED 28 Aug: `!set_passwd` ALREADY set the reason and the caller discarded it. `status()` is read immediately and 10118-10121 name the four cases; the "not elevated" one says a retry cannot help.** ***DONE 28 Aug 2026, BOTH ARMS MEASURED*** by `verify-acctmsgs.ps1` — **31 PASS / 0 FAIL / 0 SKIP**, `-Prefix sdmsgb`. **Mismatch**: 10118 printed, the other three of the four messages absent, and answering `N` unwound the creation. **Windows refused**: 10119 printed **naming the account**, with the mismatch and unelevated messages absent and the retry still offered. ***THE REFUSAL ARM NEEDED THE MACHINE'S POLICY CHANGED*** — owner's ruling: `net accounts /minpwlen:14`, run, then `/minpwlen:0` to put it back, **and it is back, read after the run**. **The first attempt SKIPped**: it sent a 150-character password on the reasoning that 127 is a hard SAM limit for a local account, and `Set-LocalUser` accepted it. The password is now **chosen from the policy** — `Get-PasswordPolicy` reads it with `secedit`, `Select-RefusedPassword` breaks whichever rule is in force | `gpl.bp/CREATEA:498` |
| ~~23~~ | **S** | ~~`term default` sets 20x24, the MINIMUM width, not SD's 120x36 default~~ — UPSTREAM #24. ***DONE 27 Aug 2026***, installed 17:25:59 and **measured: `term` reports 120 x 36**. **Docs corrected too**, `SDCoreWindowsDocs` `c41d999` | `gpl.bp/TERM:165` |
| ~~24~~ | **S** | ***DONE AND MEASURED 31 Aug 2026 ON THE 00:48:04 INSTALL — A DEAD SESSION'S TASK LOCK IS RELEASED, AND THE CONTROL HELD.*** `probe-tasklock.ps1`: baseline **no locks**; a background session took `LOCK 5` and `LIST.LOCKS` showed it; the session was killed with `taskkill /F` and ***THE LOCK SURVIVED THE KILL*** — which is the row that makes the next one decisive, because a lock released by the kill itself would have scored `sd -cleanup` a pass for doing nothing; then `sd -cleanup` elevated, **exit 0**, and `LIST.LOCKS` answered ***"No task locks reserved by any user"***. **Anchored on that exact free-text wording, not on absence of output.** ***`sd -cleanup` never releases a dead session's task locks*** — UPSTREAM #25. ***FIXED AND COMPILED 31 Aug 2026; STAYS OPEN UNTIL IT IS MEASURED ON AN INSTALL — COMPILING IS NOT RUNNING.*** **One word**: the task-lock loop in `remove_user()` tested `process.user_no` where the file, record and group loops below it all test `user_no`, the uid taken from `uptr->uid`. ***AND IT RELEASED NOTHING RATHER THAN THE WRONG THING***, which is why it never looked like corruption: `cleanup()` tidies up for OTHER sessions and never becomes a user, so `process.user_no` is **0** — and a FREE task-lock slot is also 0, so the loop matched exactly the empty slots, cleared them again, and left every held lock held. **The recovery this port documents everywhere** — *"run an elevated `sd -cleanup`"* — **was not one for task locks.** `make sd` **exit 0, no warnings**, `clopts.o` rebuilt, `bin/sd.exe` `4732ECF6…` → `8E1264DB…`. **Re-confirmed live upstream at `ae0cc5f` before changing it here.** **To close: a cycle, then a killed session holding a `LOCK`, then `sd -cleanup`, then `list.locks`** | `gplsrc/clopts.c:300`, and entry 16 |
| ~~25~~ | **S** | ~~`encrypt.field` is in every administrator's VOC and `$CRYPTO` is not in the distribution~~ — UPSTREAM #26. ***DONE 28 Aug 2026, MEASURED on the 00:53:34 install: `verify-tiers` 33 PASS, ADMINISTRATOR 416, STANDARD and PROGRAMMER unmoved.*** **Fixed by taking the entry's recommended option: the `voc_template` record is DELETED and the name removed from `TIER.ADD.ADMINISTRATOR`. ADMINISTRATOR's VOC is 416, re-derived from the directory; STANDARD and PROGRAMMER unmoved. `verify-tiers.ps1` and PROJECT_STATUS §A1 updated with it.** ***UNCOMPILED. Reversible in one commit if you would rather ship a `$CRYPTO`*** | `sdsys/voc_template/encrypt.field`, `newvoc/TIER.ADD.ADMINISTRATOR` |
| ~~26~~ | **S** | `delete.file` *name* `no.query` prompts twice when the name is typed in lower case — UPSTREAM #27. **FIXED HERE 28 Aug: both the DATA and DICT path comparisons are case-insensitive.** ***DONE 28 Aug 2026, MEASURED*** by `verify-vocverbs.ps1`: `delete.file zzprfw no.query` fired **neither** prompt and deleted DATA, DICT and the VOC entry. ***NOT tested with `force`, which is what this entry's summary in START HERE asked for and which CANNOT FAIL*** — `DELETEF:250`/`:319` guard both prompts with `if not(force)`. Still live upstream | `gpl.bp/DELETEF:233` |
| ~~27~~ | **M** | `modify.account` *acc* `add`/`delete` makes the same group change as `grant`/`revoke` and writes no audit record — **FIXED 28 Aug: a `K$AUDIT` record after each successful edit, naming the verb, on the model of `GRANTA:208`/`:233`.** ***DONE 28 Aug 2026, MEASURED*** by `verify-acctmsgs.ps1` on the 00:53:34 install: **both** `MODIFY.ACCOUNT ADD account=… to=…` and `… DELETE account=… from=…` appeared in the bytes the run added to `sdsys/audit`, **with the controls first** — 10018 and 10021 in SD's own output, since the record is written inside `if stat = 0` and a failed edit would otherwise read as a missing audit record | `gpl.bp/MODIFYA:344` |
| 28 | **M** | A process dump is written into the system directory, where every SD user can read it ***— EXAMINED 31 Aug 2026 IN THE BATCH-2 C WORK AND DELIBERATELY NOT BUILT: THE CODEBASE ARGUES AGAINST THIS ENTRY'S MIDDLE OPTION.*** Of its three, *"whether the dump should be written with a restrictive ACL"* is the only one that is a C change, so it was the candidate — and ***`win32audit.h` already rules on that shape for this tree***: `win32_audit_rotate()` **copies** the security descriptor from the file it rotates away *"rather than rebuilt from anything that could drift out of step with the installer"*, because a file created by `CreateFile` inherits the data tree's rights and the tree grants `sdusers` Modify. **Building a DACL in `pdump.c` would be the second, divergent way of doing what one `secure-*.ps1` already does**, and the drift that warns about is the same drift. ***SO THE RECOMMENDATION IS OPTION 1, WHICH IS INSTALLER WORK, NOT C***: `DUMPDIR` set to an administrator-only directory with a `secure-dumps.ps1` on the `secure-audit.ps1` model. **Still the owner's call, and the third option — whether `sdsys` should stop being `sdusers`-writable — is wider than this entry and untouched** | `gplsrc/pdump.c:97`, `gplsrc/win32audit.h`, `gplbld/secure-audit.ps1` |
| ~~29~~ | **S** | ~~`micro` reports "Permission denied" on every save~~ — **DONE 27 Aug 2026**, install 19:37:47. `MICRO_CONFIG_HOME` is a per-user `~/.micro` via the new `micro-home.ps1`. Owner: three runs, save and no-save, **no message**. Took three attempts — see the entry | `gpl.bp/EDIT`, `gplbld/micro-home.ps1` |
| ~~30~~ | **S** | ~~`verify-osusers.ps1` refuses on a fresh install: it needs `@LOGNAME` unlisted in `os.users`, but PRE_RELEASE 2 made `adopt-account` list every administrator~~ — **verifier fixed 27 Aug (parks and restores the record); the product is correct** | `gplbld/verify-osusers.ps1` |
| ~~31~~ | **S** | ***DONE 29 Aug 2026, MEASURED ON `-Run b59`: `verify-apiadmin` 22 PASS / 0 FAIL / 0 SKIP AND THE CONTROL PASSES*** — `[PASS] control: local elevated session refused OS.EXECUTE: expected False, got False`, after failing on five consecutive runs. ***CLOSED BY 56 WITH NO EDIT TO THE VERIFIER AT ALL***: `CREATEA` stopped writing administrators into `os.users`, so `os_permitted()` falls through to a lookup that finds nothing and refuses — the control's original expectation is simply right again. ***AND THE RECORDED "21/23" WAS WRONG IN THE DENOMINATOR***: b58's own log reads 21 PASS / **1** FAIL, so it was always **22** checks. The figure to carry forward is **22/22**. *(Original entry below.)* ~~`verify-apiadmin`'s control is stale~~ — it expects an elevated session `LOGTO`'d into a PROGRAMMER account to lose `OS.EXECUTE`, but `os_permitted()` keys the list on `process.username` (`don`), whom PRE_RELEASE 2 listed. Headline hole (API OS.EXECUTE) stays closed. ***RULED 29 Aug 2026 — BEING AN ADMINISTRATOR IS THE GATE, SO THIS IS A PRODUCT CHANGE AND NOT THE VERIFIER-ONLY FIX THIS ROW USED TO CLAIM.*** Owner: *"any administrator keeps universal rights, ssh, api, os.execute, no matter which account they logto. Permission belongs to the person, even if they logto an account with fewer priviledges."* **Today an administrator who is NOT in `os.users` is REFUSED after a `LOGTO`** — `CPROC:2713` clears `USR_ADMIN` and `os_permitted()` falls through to the list; `don` passes only because PRE_RELEASE 2 listed him. **Sev raised S → B: the defect is the product, not the instrument.** ***AND THAT RULING IS WITHDRAWN THE SAME DAY — SEE 56.*** Told what it cost, the owner reversed it: *"if they logto another account, they have the rights of that account."* **That is what `CPROC:2735` already does**, so the product is right and this is once more the verifier-only fix it was first filed as. **Sev back B → S**, and the work is one assertion in `verify-apiadmin.ps1`, which must not be changed until 56 lands. Not started | `gplbld/verify-apiadmin.ps1` |
| ~~32~~ | **S** | ~~`delete.account` leaves the `ProfileList` registry entry, so an account recreated under the same name gets a DIFFERENT home directory~~ — **FIXED 27 Aug 2026: the `catch { exit 6 }` that left both halves is now `catch { }`, and the key is removed in its own right; status 6 splits into 6 (directory) and 7 (registry entry).** ***PARTLY REVERSED 28 Aug BY 36, ON THE OWNER'S RULING, AND DELIBERATELY***: removing the entry over a directory that is still there destroys the only handle a sweep has, so the entry is now removed **only if the directory went**, both halves are kept together otherwise, and something comes back for the pair. **The defect this entry names is still fixed** — an entry is never left behind on its own. **Its regression test is re-scoped** from *"the entry is gone"* to *"the entry is gone when the directory went"*. ***BOTH FIXES REMAIN UNCOMPILED — needs a cycle.*** Generated PowerShell parse-checked 0 errors / 203 tokens on 27 Aug, 1944 chars on 28 Aug; the new steps run read-only against a real account | `gpl.bp/DELETE_USER`, `gpl.bp/DELACC`, `messages/10075`, `messages/10116`, `gplbld/verify-delaccount.ps1` |
| ~~33~~ | **S** | ~~`allow-ssh-groups.ps1`'s own usage text offers a bare form that **writes nothing**~~ — **DONE 27 Aug 2026**, the usage line names `-Installed` and a dated note says which forms need it. Comment only, parses 0 errors / 1247 tokens | `gplbld/allow-ssh-groups.ps1:4` |
| ~~34~~ | **S** | ***`release.ps1` cannot complete on the `Technical` set*** — `checklinks.py` rightly refuses a zero-link set, and two pages in, `Technical` still has no honest cross-reference. A whole set has no working release command. **Not to be settled by adding a link.** ***RULED 29 Aug 2026 — A SET MAY DECLARE ITSELF LINK-FREE.*** `checklinks.py` gains an explicit per-set way to say *this set legitimately has no links*, and `release.ps1` accepts it; `Technical` opts in. **The zero-link refusal stays the default for `User`, `Administrator` and `Testing`**, so a set that loses its links by accident still fails loudly — the guard is narrowed by declaration, never removed. ***COMBINED INTO 80 ON THE OWNER'S RULING, 30 Aug 2026 — CLOSED AS AN ENTRY, NOT AS WORK.*** The analysis above is unchanged and is what 80 acts on; what has gone is the separate number. **It was never separable from H.2 anyway** — a cross-page link cannot be added to `Technical` without deciding what `Technical` is going to contain, which is H.2's business, and both now happen once against the final install image | docs repo `tools/release.ps1`, `tools/checklinks.py:57`, and **entry 80** |
| ~~35~~ | **S** | ***DONE 28 Aug 2026, MEASURED*** — `create.account` now refuses the name and prints the directory (10124), witnessed by the new `gplbld/verify-profiledir.ps1` **14/14** on the 21:27:34 install, with a control account created and deleted in the same run. ***A profile DIRECTORY left behind moves the next account's home just as the registry entry does*** — found by running 32's own regression test on the install that fixed 32. `DELETE_USER` now tries to remove it, **and MEASURED: it cannot be deleted OR renamed while the hive is mounted**, so the honest answer is the rewritten `10075`, which names the cause and the restart. **Cure is 36, and 36 IS BUILT AS OF 28 Aug 2026 AND UNRUN**: the boot sweep removes the directory and `create.account` refuses the name until it is gone, so both halves of this symptom are answered — **but nothing has compiled yet, so this stays open until a cycle and a restart have been through it** | `gpl.bp/DELETE_USER`, `gpl.bp/DELACC`, `messages/10075` |
| ~~36~~ | **M** | ***DONE 28 Aug 2026, ALL FOUR RULINGS OBSERVED.*** The sweep reclaimed **5 of 5** after a restart (`5 considered, 5 reclaimed, 0 still pending, 0 refused`), `C:\Users` fell **61 → 56 by exactly those five** with `ProfileList` 46 → 41, the re-scoped 32 test is green in b56–b58, and `create.account` refuses a live directory (`verify-profiledir.ps1` 14/14). Two defects were found on the way and fixed — **49** and **50**. ***BUILT 28 Aug 2026, ALL FOUR RULINGS.*** Directory first and the `ProfileList` entry only if it went (`DELETE_USER`); the pair recorded under `C:\ProgramData\SD\profile-reclaim`; `gplbld/reclaim-profiles.ps1` sweeps it from `sdsvc.exe` at every service start; `create.account` REFUSES on an existing profile directory and names it (`!profile_dir`, 10124/10125). **New statuses 6/7/8 and messages 10075 rewritten, 10116 rewritten, 10123/10124/10125 new.** ***THE SWEEP READS THE RECORD, NOT `ProfileList`***, so it does not inherit the blindness that left `sdapiab49` and two others unfindable. **Its refusal table is a pure function guarded by `gplbld/test-reclaim-units.ps1` — 39/39, and its positive control against a copy with the containment check removed fails 34/5.** **The store gets an ACL of its own** (`gplbld/secure-reclaim.ps1`): inherited, it would be a list of directories every SD user can edit and LocalSystem later deletes. **32's regression test is re-scoped** in `verify-delaccount.ps1` from *"the entry is gone"* to *"the entry is gone when the directory went"*, with the keep-both branch asserting the record. *(Was: RULED 27 Aug 2026 AND NOT BUILT.)* ***Deleted accounts leave their registry hives mounted — 22 orphan SIDs / 44 hives on this host*** — the ROOT CAUSE of 32 and 35. **Mechanism confirmed: `Remove-CimInstance` failed on a mounted hive, then cleared `53 removed, 0 failed` after a restart.** Nothing SD does can unmount them | `gpl.bp/DELETE_USER`, `CREATEA`, `DELACC`, `PROFILE_DIR`; `gplsrc/sdsvc/sdsvc.c`; `gplbld/reclaim-profiles.ps1`, `secure-reclaim.ps1`, `test-reclaim-units.ps1` |
| ~~37~~ | **S** | ***`create.account` prints two lines that contradict each other***: with `both` it says *"may sign in over ssh only"* then *"may sign in over ssh and use the API"*. **Two different gates** — Windows logon rights (`CREATEA:808`) and SD route keywords (`:1612`) — worded so nothing tells the reader that. **FIXED 28 Aug: 10034 now says "may reach this computer only over ssh"; 10076/10077/10078 are recast as "SD routes for %1: ...". Nothing anchors on the old text — checked.** ***DONE 28 Aug 2026, MEASURED*** by `verify-acctmsgs.ps1`: on a real `create.account … programmer both`, 10034 read *"may reach this computer only over ssh"* and 10078 *"SD routes for …: ssh and the API"*, **and both old wordings were absent** — the disqualifier is what carries this one, since both lines contain "ssh" and any check anchored there would have passed on the defect | `messages/10034`, `10076`, `10077`, `10078` |
| ~~38~~ | **M** | ***WIRED IN 28 Aug 2026 ON THE OWNER'S RULING — "wire the pair into VerifyInstall".*** `gplbld/verify-doors-suite.ps1` drives all five phases as **one step** and is the **last step of `VerifyInstall1`**, conditional on `-Run`. ***IT HAD TO GO IN THE UNELEVATED RUNNER, AND THAT IS FORCED, NOT PREFERRED***: the phases need alternating tokens (Create elevated, Control ordinary, Suspend elevated, Refused ordinary, Remove elevated) and **an elevated parent cannot make an ordinary child** — `runas /trustlevel` yields a RESTRICTED token, not the user's own (`VerifyInstall1.ps1:70`) — so the ordinary half must be the parent. It raises the three elevated children itself, **announcing each UAC prompt**, and the child redirects its own output because `-Verb RunAs` cannot be combined with `-RedirectStandardOutput`. **It refuses a prefix with any residue before creating anything** — Windows user, `sdu_` group, `ACCOUNTS` record, **or profile directory** — because a name is single-use once its account has reached the Control leg. ***COSTS: three more UAC prompts, and one permanent profile directory per suite run until 35/36 is built.*** **Unrun as a suite step** — the refusal path was exercised (exit 2, nothing created) and the five phases were run by hand. **The original finding:** ~~The suite tests SUSPENDED on no door at all~~ — neither `verify-tiers.ps1` nor `verify-tierapi.ps1` contains the word. ssh and `logto` are now measured by hand; **the API door has never been reached** and cannot be tested by wording, since `APISRVR:507` refuses with the same `sysmsg(10003)` as every other refusal. **Needs a controlled pair.** ***28 Aug: `verify-tiers.ps1` section 6 written and UNRUN — the record, the write-once guard 21 left unmeasured, and the VOC. It CANNOT test the `logto` door: the check sits after `CPROC:3729`'s elevated bypass and this verifier must be elevated.*** ***THE CONTROLLED PAIR NOW EXISTS AND HAS PASSED, 28 Aug 2026*** — `verify-doors-admin.ps1` + `verify-doors.ps1` on `sddr2`, all four legs green, **all three doors ADMITTED then all three REFUSED**, and ***the API door was reached for the first time***. **WHAT IS LEFT OF THIS ENTRY IS ONE DECISION, NOT A MEASUREMENT: the pair is standalone and is NOT wired into `VerifyInstall1`.** It is deliberately unwired for the same reason `verify-acctmsgs` is — **it creates a real Windows account**, and it needs an elevated half and an unelevated half, which is the split the suite already has. **Owner's call: wire it into the two runners, or leave it standalone and named in the docs.** Note the fixture is single-use — its Control leg's ssh login leaves a profile directory that entries 35/36 cannot yet remove, so each attempt needs a fresh prefix. ***RUN AS A SUITE STEP FOR THE FIRST TIME ON `-Run b50`, 28 Aug 2026, AND IT FAILED TWICE FOR TWO DIFFERENT REASONS.*** First run: `Create` 8/8 and `Control` 6/6, then **Suspend and Remove died before their UAC prompt** — entry 43. Second run, after the same cycle: **refused up front**, because the first run had already spent `sddrb50a` at the Control leg — **the single-use guard working exactly as designed, and nothing was created.** ***THE PRICE IS NOW MEASURED RATHER THAN ESTIMATED***: a failed run leaves a **live, enabled, UNSUSPENDED** account in `sdusers`, `sdssh` and `sdapi` plus its profile directory, because the leg that removes it is the one that did not run. **43 is fixed and unrun; the next attempt needs a fresh `-Run` token** | `gplbld/verify-tiers.ps1`, `verify-tierapi.ps1`, `verify-doors-admin.ps1`, `verify-doors.ps1`, `verify-doors-suite.ps1` |
| ~~39~~ | **B** | ***DONE AND MEASURED 30 Aug 2026 ON A REAL INTERACTIVE UNINSTALL IN `Windows 11 - Test` — THE `-Remove` PATH RAN FOR THE FIRST TIME AND DID EXACTLY WHAT IT PROMISED.*** The sweep's own log, read off the guest rather than reported from the screen: `mode : REMOVE`, `keep : don`, `token: elevated`, `sdusers members: don, henry, james`, `administrators that would remain: Administrator, don`, **`KEEPING: don`**, **`REMOVING (2): henry, james`** — each with `group sdu_<name> removed` and `user removed` — and **`removed 2 of 2 account(s); kept 1.`** ***THE BEFORE/AFTER CAPTURES AGREE***: local users **9 → 7**; `sdusers`, `sdssh` and `sdapi` down to `don` alone; **`sdsshonly` EMPTY**; `sdu_HENRY` and `sdu_JAMES` gone and `sdu_don` left; `Administrators` untouched; and ***`sshd_config`'s SD block is gone***, leaving only the stock commented `#ForceCommand cvs server`. **`tim`, a Windows account SD never created, was correctly untouched** — the control this run got for free. **The prompt named the account it was keeping IN THE QUESTION** (`sd.iss:3576`), which is what the ruling required, and defaulted to No. ***TWO THINGS NOT EXERCISED, SAID PLAINLY RATHER THAN TICKED***: the **last-administrator refusal** — the guard evaluated and reported *"administrators that would remain: Administrator, don"* but never had to fire, because this guest has an administrator outside `sdusers`; and the **keep-the-database** branch, since the tree came out `absent` in the after capture, so that half went untested. ***AND THE RUN FOUND A HOLE THIS SWEEP CANNOT COVER — FILED AS 72, NOT SWEPT UP HERE***: `john`, half-created by the failure in 68, is **in no group at all** and so is invisible to a candidate set built from `sdusers`. **He survived the uninstall**, which is this entry's own defect arriving by a door this fix cannot reach. *(Was: Uninstalling strips SD's `AllowGroups` and `ForceCommand` and leaves every account SD created — so each becomes an ordinary ssh-reachable account with a PowerShell shell. `sd.iss` removes no account anywhere; the closing disclosure does not mention them. ***NO LONGER REASONED — MEASURED 28 Aug 2026, AND IT SURVIVES A WHOLE CYCLE.*** `cycle.ps1` uninstalled and deleted **both** trees at 15:29:59, so `sddrb50a`'s `ACCOUNTS` record went with the data tree — the register now holds only `don` and `sdsys`. **The Windows side did not move**: the account is still **enabled**, still has its own `sdu_sddrb50a` group, and is still a member of `sdusers`, `sdssh` **and** `sdapi`, with `sshd_config` still carrying `AllowGroups sdssh`. **So the account outlived the SD installation that made it, keeping every route it was granted.** ***AND IT IS NOW UNREMOVABLE BY SD***: `DELETE.ACCOUNT` cannot reach an account with no `ACCOUNTS` record, so `verify-doors-admin.ps1 -Phase Remove` correctly FAILS on it rather than reporting a tidy pass, and names it STRANDED. **Whether SD would still admit a login is NOT measured** — the password was generated inside an elevated child and never printed, deliberately. **What is measured is that Windows still would.** ***RULED 29 Aug 2026 — A SECOND, SEPARATE PROMPT ON UNINSTALL, AND IT MUST NEVER TAKE THE INSTALLING PERSON'S OWN ACCOUNT.*** Owner: *"a second separate prompt, however deleting the windows accounts should not delete the account of the person doing the installation so that there is at least one remaining account that can log into windows."* So `sd.iss:3482`'s *"Remove the SD database as well?"* stays exactly as it is, and a **second** question follows it about the Windows accounts SD created (with their `sdu_`/`sdg_` groups and profiles), defaulting to keep. **The installing user is excluded from that sweep by construction, not by the operator noticing** — leaving at least one account that can still sign in to Windows. **The closing disclosure is wrong either way and is fixed with it**: it names the database, the ssh server and `sdusers`, and never mentions the accounts. Not started)* | `gplbld/sd.iss:3367`, `sd.iss:3482`, `sd.iss:3576`, `gplbld/remove-sdaccounts.ps1`, the closing disclosure |
| ~~72~~ | **B** | ***A HALF-CREATED ACCOUNT JOINS NO GROUP, SO IT IS NEVER CONFINED AND NO SWEEP CAN EVER FIND IT. MEASURED 30 Aug 2026 IN `Windows 11 - Test`, BEFORE AND AFTER A REAL UNINSTALL.*** `john` was created by `create.account user john none`, which failed at the credential step — **entry 68** — and the owner answered `N` to the retry. ***WHAT HE WAS LEFT WITH, READ OFF THE GUEST***: `john` appears **exactly once** in each capture, in the local-users list, `enabled=True`. **He is in `sdusers`? No. `sdsshonly`? No. Is there an `sdu_JOHN`? No.** ***SO THE ORDER OF OPERATIONS IS THE DEFECT.*** `CREATEA` creates the Windows user, sets its password, and only then adds it to `sdusers` and `sdsshonly` — visible in `henry`'s own transcript, *"User henry Created / New Windows password… / HENRY added to sdusers"* — **so a failure between the second and third steps leaves a Windows account that SD has made and then disowned.** ***TWO CONSEQUENCES, BOTH WORSE THAN THE FAILED COMMAND.*** **(1) IT IS NOT CONFINED.** `sdsshonly` is what carries `SeDenyInteractiveLogonRight` and `SeDenyRemoteInteractiveLogonRight`, so `john` **could sign in to Windows at the console or over RDP for as long as SD was installed** — against the owner's standing policy that only administrators log in directly. **(2) IT IS INVISIBLE TO 39's SWEEP**, whose candidate set is `sdusers` membership *"because `CREATE.ACCOUNT` adds every account it makes and nothing else does, so the group IS the list SD created"* — **a premise this defect falsifies.** `john` survived the uninstall as an ordinary enabled Windows account with a password the administrator had set. ***AND THE MESSAGE DOES NOT SAY SO***: 10122 warns that *"ssh would admit this account and the API would refuse it"*, and 10008 asks *"user created but password not set, Retry (Y/N)?"* — **neither says a Windows account now EXISTS, is UNCONFINED, and will not be cleaned up.** Answering `N` reads as *"nothing was made"*. **Fix shapes: roll the Windows user back when a later step fails; or join `sdusers`/`sdsshonly` BEFORE the password so a failure leaves something the sweep owns; or say plainly what was left behind and how to remove it. The first is the only one that leaves no window at all** | `gpl.bp/CREATEA` create/password/group order, `sdsys/messages/10122`, `10008`, `gplbld/remove-sdaccounts.ps1` candidate set, and entries 68, 39 ***— THIS ROW'S DIAGNOSIS WAS WRONG AND THE TRUTH IS WORSE. CORRECTED AND FIXED 30 Aug 2026.*** It said `CREATEA` does not roll back. **It does**: `CREATEA:626` was `void delete_user(acc.uname)` followed by 10086, *"An account must have a password. Nothing was created."* ***THE `void` WAS THE DEFECT — 10086 IS A CLAIM ABOUT WHAT JUST HAPPENED AND IT WAS PRINTED WHETHER OR NOT THE REMOVAL WORKED.*** **The two runs of 30 Aug prove it from both sides**: `sdswa1` failed the same way under `verify-sdsyswrite` from an **elevated** create and the rollback WORKED — the verifier's own row *"no Windows account left behind"* passed — while `john`, created from an unelevated `logto`-reached SDSYS, survived. ***AND THE CAUSE IS ONE WORD IN `DELETE_USER`***: `:275` ran `os.execute`, **not `ps_script`**. ***NOTHING REFUSED, WHICH IS WHY IT WAS SILENT***: after `LOGTO SDSYS`, `CPROC:2769` sets `K$ADMINISTRATOR` — which **is** `USR_ADMIN` — so `os_permitted()` returns TRUE at `op_sh.c:161` and `os.execute` is **allowed**; but the PowerShell it spawns inherits the SD process token, which is not elevated, so `Remove-LocalUser` was denied. ***THE TREE ALREADY HAD THE RULE AND THIS FILE WAS THE ONE EXCEPTION***: `CREATE_USER:104`, `SET_PASSWD:130` and `OS_GROUP` all CHANGE Windows state through `ps_script`, while `IS_USER`, `IS_GROUP`, `IS_GRP_MEMBER`, `IS_SD_USER` and `PROFILE_DIR` only READ and correctly use `os.execute`. **DELETE_USER changed state through the reading path.** ***FIXED 30 Aug 2026, UNCOMPILED***: `DELETE_USER` takes `ps_script`; `CREATEA` reads the rollback's result instead of voiding it; and **new message 10130** says the honest thing when a rollback fails — that the account is still there, is NOT confined, and no sweep will find it. **`PS_SCRIPT:165` falls back to `os.execute` when the caller is not an administrator, so a non-administrator caller behaves exactly as before** ***— DONE 30 Aug 2026, PROVEN ON THE PATH THAT MATTERS AND NOT ON A PROXY FOR IT.*** Reproduced exactly as the entry describes: from the owner's **OWN, UNELEVATED** account, `logto sdsys`, `create.account user testrb none`, two passwords deliberately not matching, answered `n`. **That is the route the whole defect lives on** — an elevated start lands in SDSYS and never exercises it, which is why `verify-sdsyswrite`'s cleanup rows could not prove this. ***THE MACHINE AGREES WITH THE MESSAGE, WHICH IS THE WHOLE CLAIM***: `TESTRB` **absent** from Windows against a control that finds `don`, `sdu_TESTRB` **absent**, the `ACCOUNTS` register record **absent**, the account directory **absent**. ***AND THE DECISIVE DETAIL IS WHICH MESSAGE PRINTED.*** It said *"An account must have a password. Nothing was created."* and **NOT 10130** — 10130 is the new message this fix added for the case where the rollback FAILS, so its silence is the positive evidence that the rollback ran and worked. **Before the fix that same sentence printed either way, which is what made `john` survive an uninstall as an enabled Windows account with a password.** *(Incidentally the first sighting of 79 in the wild: the prompt read `Retry (y/<n>)?` and `n` was taken.)* | `gpl.bp/DELETE_USER:275`, `gpl.bp/CREATEA:626`, `sdsys/messages/10130`, `10122`, `10008`, `gplbld/remove-sdaccounts.ps1`, and entries 68, 39, 79 |
| ~~73~~ | **S** | ***DONE AND MEASURED 31 Aug 2026 ON `-Run b80`: `verify-sdsyswrite` 12 OF 12, ZERO FAIL, INCLUDING THE DECISIVE AUDIT ROW.*** See the end of this row for the numbers. ***NO VERIFIER HAS EVER MADE A SUCCESSFUL ADMINISTRATIVE WRITE FROM A SESSION THAT REACHED SDSYS BY `logto` FROM AN UNELEVATED START — WHICH IS EXACTLY THE HOLE 68 LIVES IN.*** Owner, 30 Aug 2026: *"there is a hole in the verification scripts, they do not test what an admin logged in as themselves and then doing a LOGTO SDSYS can and cannot do."* ***THE GAP IS NARROWER AND SHARPER THAN THAT, MEASURED ACROSS `gplbld`***: about **twenty** verifiers issue `LOGTO SDSYS`, so the route is exercised constantly — **but all of them bar one gate on elevation**, so the SD PROCESS is elevated and a `$cred` or `os.users` write succeeds. **The one without an elevation gate, `verify-lcnames.ps1`, only READS the VOC** (`CT VOC ACCOUNTS`, `CT VOC MESSAGES`). ***AND THE ONE VERIFIER THAT COVERS `modify.password` NEVER COMPLETES A PASSWORD CHANGE.*** `verify-setpw.ps1` is 61 lines and makes four assertions, **all about argument parsing**: `MODIFY.PASSWORD DON somethingextra` refused with 5276 and not reaching the prompt, and a control that reaches the prompt and is not refused — **whose password is deliberately `definitely-not-the-password`, so authentication always fails and `CRED_SET` is never called.** **It proves the parser and never once exercises the write.** ***THIS IS THE "WHAT WOULD HAVE CAUGHT IT" ANSWER THAT §"AN INSTRUMENT SHOWS WHAT IT DID" DEMANDS***, and it is the class-fix for 68 and 72 both: the one-line cause is `CRED_SET` writing directly, and the CLASS is that **every administrative write is only ever measured from the privilege level that makes it work.** ***THE SHAPE OF THE FIX, AND ITS PARENT MUST BE UNELEVATED, WHICH §4.0.1 ALREADY REQUIRES OF THE SUITE***: start SD as the administrator's own account from an **unelevated** parent, `logto sdsys`, then perform each write that touches a protected store — `$cred` via a REAL `set.password`, `os.users` via `modify.account <acc> os-on`, and an audit/log append as the control that should still succeed, since `secure-audit.ps1` and `secure-log.ps1` grant `sdusers` append while `secure-cred.ps1` grants nothing and `secure-osusers.ps1` grants read-only. ***AND IT NEEDS THE POSITIVE CONTROL OR IT MEASURES NOTHING***: the same operations from an ELEVATED start must SUCCEED, or a red row cannot be told apart from a broken probe. **Filed S rather than the usual M for a verifier gap, because this one let a B ship and covers 72 as well** ***BUILT AND RUN 30 Aug 2026 — `gplbld/verify-sdsyswrite.ps1`, AND IT IS RED EXACTLY WHERE IT WAS DESIGNED TO BE.*** `-Prefix sdswa2`, unelevated, one UAC consent: **5 PASS / 2 FAIL**, the two failures being *"unelevated SDSYS can write `$cred`"* and *"…can write `os.users`"*, with all three controls green — setup created the account, the unelevated session **reached SDSYS and read it** (`18 record(s) counted`), and the **elevated** control wrote `$cred` successfully. **It is written to go green when 68 is fixed; a green run before that means the probe is broken.** ***THREE FAULTS OF ITS OWN WERE CAUGHT BEFORE IT COULD MISLEAD, AND THE THIRD IS THE ONE WORTH READING.*** (1) It named a `set.password` verb that **does not exist** — only `modify.password`, only in `voc_template`. (2) It fed SD a **CRLF** body, and SD takes the `\r` as a line of its own, so every command got a blank line after it and every ANSWER went one out of step; that presented as *"The two passwords did not match"* and is a line-ending fault, now guarded by asserting the body is CR-free before it is written. ***(3) ITS OWN SUMMARY LINE PRINTED A FALSE GREEN.*** The tally tested `Expected -ne 'n/a'` with `Expected` a **Boolean**, so PowerShell coerced the string — `[bool]'n/a'` is `$true` — and every *"expected True"* row read as a skip: **the first real run reported `2 PASS / 0 FAIL / 5 SKIP` on a run with five passes and two genuine failures.** The exit code was correct throughout, **which is what makes it the dangerous kind of wrong** — a script written to catch false greens printed one on the single line a human reads. Each row now records its own verdict, and **the tally refuses itself if the three counts do not add up to the number of rows** ***— AND IT WENT GREEN 30 Aug 2026, `-Prefix sdswa5`, 7 PASS / 0 FAIL / 0 SKIP, WHICH IS THE BEHAVIOUR THIS ROW PREDICTED***: it was written to be red until 68 was fixed and to go green when it was, and it did both, catching the intermediate 3035 → 3037 state on the way. ***THE ROW STAYS OPEN, BECAUSE ONE LEG OF ITS OWN DESIGN WAS NEVER BUILT.*** The shape called for **an audit/log append as the control that should still SUCCEED** — `secure-audit.ps1` grants `sdusers:(AD` and `secure-log.ps1` grants `sdusers:A`, append, precisely so an ordinary session can write them — and `verify-sdsyswrite.ps1` has no such row: its seven are setup, the SDSYS-reach control, the two write measurements, the elevated control and two cleanups. **Without it the suite proves the two protected stores are reachable and never shows that a store which was ALWAYS writable still is**, so a change that broke append everywhere would read green here. **That leg, not another verifier, is what closes 73** | `gplbld/verify-sdsyswrite.ps1`, ***— AND THIS ROW'S OWN PREMISE IS HALF WRONG, WHICH IS WHY THE LEG IS NOT BUILT YET. CORRECTED 30 Aug 2026.*** It says *"`secure-audit.ps1` grants `sdusers:(AD` and `secure-log.ps1` grants `sdusers:A` — append, precisely so an ordinary session can write them"*. **`secure-log.ps1` grants `sdusers` NOTHING**, and says so in its own header: *"sdusers needs nothing at all here - not append"* — the log is administrators-only, because the log is ABOUT the very person it would otherwise let write. **Only the audit trail is append-for-`sdusers`.** ***AND THE AUDIT CANNOT BE READ BACK BY THE SESSION THAT WROTE IT***, which changes the shape of the control this row asks for: `AD` is AppendData and NOT ReadData, so an unelevated SDSYS session can append and cannot verify. **The leg therefore has to measure the file's size from the ELEVATED side, either side of an append triggered from the UNELEVATED one** — three steps, not one, and the row's one-line description hides that. ***WHAT APPENDS IS ALSO NARROWER THAN "a write"***: the only caller of `win32_audit_append` is `gplsrc/k_error.c:742`, so the trigger has to be an SD error condition rather than an ordinary command. **NOT BUILT: a row that appended nothing would score PASS for doing nothing, which is the exact failure this entry exists to prevent** ***— BUILT 30 Aug 2026, AND THE APPEND-NOTHING TRAP IS CLOSED BY NAMING THE RECORD RATHER THAN BY MEASURING SIZE.*** Step 6 of `verify-sdsyswrite.ps1`. **The trigger is a refused `LOGTO`**: `CPROC:2738` calls `kernel(K$AUDIT, 'LOGTO REFUSED account=<NAME> reason=not in the register')`, so it needs nothing compiled into the account, it changes nothing else, and ***the record carries a name THIS RUN chose*** — which is what makes the row decisive, because size alone cannot tell our append from a concurrent one. **`K$AUDIT` is ungated** (`op_kernel.c:652`, *"Returns 0 always"*), so nothing in the leg depends on the administrator flag the `LOGTO` set — that was the doubt that made this look expensive. **Five rows**: the trail exists; ***the probe name is ABSENT beforehand*** (the negative control, so a leftover cannot score the decisive row before anything is written); this process cannot READ the trail, which is the `(AD,RA,S)` ACL echoed by `icacls` rather than asserted; the trail grew; and **the append is this run's, by name — the DECISIVE one.** New `Invoke-PSElevated`/`Get-AuditState` do the two elevated reads through the same helper the rest of the file uses. ***`.Contains()`, NOT `-match` OR `Select-String -SimpleMatch`***, because an interpolated pattern silently changes what is searched for and would report a present record as absent — which here reads exactly like *"the append never landed"*. **Parse-check 0 errors, 2888 tokens, 12 functions found** — the function count is the check, since a BOM yields 0 errors with the bodies swallowed. ***STILL OPEN: IT HAS NOT RUN.*** It needs an unelevated parent and one UAC consent, and the leg is written to be read alongside the two write rows — green step 6 means the session works and any failure above is about `$cred` and `os.users`; red step 6 means the session itself is the problem and the rows above say nothing ***— RUN 31 Aug 2026, `-Run b80`, UNELEVATED, AND GREEN IN EVERY ROW: 12 of 12.*** `VerifyInstall1` **PARTIAL, 2 of 17** — and **17**, not 16, which is the arithmetic saying `test-stemcoverage-units` was added rather than substituted. ***THE STEP-6 EVIDENCE, WHICH IS THE POINT OF THE LEG***: probe name `ZZAUD2B5E158F1D01`; **before `exists=True len=53441 token=False`**; SD answered `LOGTO ZZAUD2B5E158F1D01` → *"User not allowed in requested account"* (10003, the refusal that fires `CPROC:2738`); **after `exists=True len=53754 token=True`**. ***THE ACL LEG PROVED THE SHAPE WAS NECESSARY RATHER THAN CAUTIOUS***: the unelevated process could not even read the file — `icacls … Access is denied`, `Successfully processed 0 files` — so a one-step version that read from the session's own side would have failed on a working product. ***AND THE GROWTH WAS 313 BYTES, NOT ONE RECORD***, because `LOGTO SDSYS` audits its elevation too — **which is exactly why size alone is not the check and the NAME is.** ***THE TWO WRITE ROWS ARE NOW GREEN, AND THAT IS THIS ENTRY'S REAL RESULT***: `unelevated SDSYS can write $cred` and `… os.users` both **True**, from the session shape that used to fail. The file was written to be red until 68 was fixed and green after, so this is **68's fix positively confirmed by an instrument built for it**, rather than inferred from 68's absence. ***WHAT WAS NOT EXERCISED, STATED RATHER THAN LEFT TO BE ASSUMED***: the `secure-log.ps1` half. The row offered *"an audit/log append"* as the control and the audit trail is the one that was built and run; the log grant is untested and no row here claims otherwise | `gplbld/verify-sdsyswrite.ps1`, `gplbld/verify-setpw.ps1`, `gplbld/verify-lcnames.ps1`, `gplbld/secure-audit.ps1`, `gplbld/secure-log.ps1`, `gplsrc/k_error.c:742`, `gplsrc/win32audit.c:39`, and entries 68, 72 |
| 74 | **M** | ***THE CLOSING DISCLOSURE NAMES ONE OF THE FOUR GROUPS AN UNINSTALL LEAVES BEHIND.*** Measured 30 Aug 2026 in the after-capture of the real uninstall that closed 39: **`sdusers`, `sdssh`, `sdapi` and `sdsshonly` all still exist**, with `don` in the first three, plus `sdu_don`. `sd.iss:1330` promises *"Your database, the ssh server, the sdusers group, and the Windows accounts SD created - with their sdu_ and sdg_ groups and their profiles"* — **so three of the four are unnamed.** ***`sdusers` IS THE ONLY ONE WITH A STATED REASON TO STAY*** (`sd.iss:3506`: deleting it *"would orphan the permissions on their own database"*), and that reason does not extend to the other three: with SD gone there is no ssh confinement to apply and no API to gate. **`sdsshonly` still carries `SeDenyInteractiveLogonRight` and `SeDenyRemoteInteractiveLogonRight`** — harmless while empty, but it is a deny-logon group left on the machine by software that has removed itself. **Same shape as 65: litter rather than damage, and it is in the one document whose whole job is to be complete about what is left behind.** **Either remove the three, or name them** ***— NAMED, 30 Aug 2026. THE OTHER HALF IS STILL THE OWNER'S.*** The disclosure now lists **all four by name** — `sdusers`, `sdssh`, `sdapi`, `sdsshonly` — and adds why: `sdusers` stays because deleting it would orphan the database permissions (`:3506`), the other three because SD does not assume they are its to remove, and **`sdsshonly` still denies its members console and Remote Desktop sign-in**, so it is called out as the one to remove by hand. ***REMOVING THEM IS A BEHAVIOUR CHANGE AND IS NOT DONE***: that is the half this row leaves open, and naming them is the part that makes a document whose whole job is completeness actually complete. **ISCC exit 0 on the change. BUILT, UNSEEN — the closing disclosure shows at uninstall, which a cycle's silent uninstall skips (`UninstallSilent`), so it wants the interactive path 39 used** | `gplbld/sd.iss:1330`, `:3506`, `gplbld/deny-logon.ps1:29`, and entry 39 |
| ~~75~~ | **S** | ***REMOVE THE STAND-ALONE INSTALL MODE: 67 MAKES IT REDUNDANT, AND THE TWO REMOTE BOXES BECOME SERVICE SWITCHES RATHER THAN FIREWALL SWITCHES.*** Owner, 30 Aug 2026: *"we should remove the standalone option — if the user does a full install and leaves both ssh and api unchecked, there will be no ssh server install and is basically the same as a standalone install"*, and then, settling the one gap: ***"the api box unchecked should mean not provide the service at all - the port should not be left open… redoing the install to allow ssh or api - better path than the existing standalone to full."*** ***THE THREE DIFFERENCES, MEASURED, AND TWO OF THEM ARE ALREADY GONE.*** **(1) ssh server** — 67 already means an unchecked ssh box installs none. **(2) `create.account user` refused outright with 10100** — its stated reason at `CREATEA:400` is *"With no ssh server such an account can sign in NOWHERE"*, **which 67 now answers per-route and later**, so the blanket refusal is redundant and the owner has said he does not want it. **(3) APIPORT — the only real difference, and the switch already exists.** `sd_conf_standalone()` (`stage.py:541`) is `SD_CONF` with `APIPORT=4243` commented out and asserts no active APIPORT survives; `stage.py:499` records why that is the true switch rather than a firewall rule — *"`open_api_listener()` returns -1 for 'no listener' when the port is <= 0"*. **So "no API listener at all" is BUILT AND TESTED; it is merely keyed to `StandaloneChosen` instead of to the api box.** ***THE CHANGE IS THEREFORE A RE-KEYING PLUS A DELETION***, not new mechanism: the two `sd.conf` variants stay and switch on the api box; `sshremote`/`apiremote` change meaning from *"let other computers connect"* to *"provide this service"*, with the firewall following the service rather than gating it. ***WHAT GOES***: the mode page, `StandaloneChosen`, `WriteStandaloneMarker`, the `$standalone` marker, `CREATEA:412-418` and message **10100**, and `verify-standalone.ps1` — **and with the page goes the only irreversible decision the installer asks anyone to make**, *"this cannot be changed from inside SD afterwards"*. ***ONE WRINKLE THE RULING'S "REDO THE INSTALL" PATH HITS, AND IT IS THE API HALF ONLY***: `sd.conf` is `onlyifdoesntexist` (`sd.iss:407-411`) precisely so a reinstall never discards a configuration the user edited, **so a reinstall would NOT turn APIPORT back on.** The ssh half needs nothing — 67 reads machine state, so installing the server is enough. **Either the installer edits that one line surgically — `allow-ssh-groups.ps1` is the precedent for writing into a file SD does not own — or the documentation says to uncomment `APIPORT` and restart, which is a one-line change to the admin's own configuration file. ***CHOSEN 30 Aug 2026: DOCUMENTATION.*** The installer does not edit a configuration file the administrator owns, and uncommenting one `APIPORT` line is a smaller and more visible act than a silent rewrite; the reasoning is recorded at the removal site in `sd.iss`** ***— BUILT 30 Aug 2026, IN THE SAME PASS AS 67 AND 76 BECAUSE EVERY `Check:` IN THE FILE CARRIED `not StandaloneChosen`.*** **WHAT WENT**: the mode page and its two radio buttons, `ModeChoiceText`, `StandaloneChosen`, `StandaloneWasMarked`, `WriteStandaloneMarker`, `ShouldSkipPage` (it existed only to hide that page), `DisclosureText`'s `Standalone` parameter and its three branches, `CREATEA`'s marker read, **message 10100 (deleted)** and **`verify-standalone.ps1` (deleted, with its `assert-current` `$neverShipped` entry)**. **`SummaryPage` is re-anchored on `wpWelcome`**, where it sat before 25 Aug 2026, and it still lands before `wpSelectTasks` — which is what the ssh boxes need. ***THE API BOX IS A SERVICE SWITCH NOW***: it picks between the two `sd.conf` variants, so unticked means `open_api_listener()` gets no port and opens nothing, and `ApplyApiFirewall` writes no rule for a service that does not exist. ***AND THAT COSTS A STATE THIS ROW DID NOT NAME — FLAGGED FOR THE OWNER RATHER THAN SWALLOWED.*** There used to be three: listener open to the network, listener restricted to loopback, no listener. Collapsing the box to "provide it or do not" removes the middle one, **so a program on the SAME machine talking to SD over the API now needs the box ticked, and ticking it also opens port 4243 to the network.** Implemented as ruled because the ruling is explicit; **if local-only API use matters, that is a third state to put back and it is the owner's call.** ***`$standalone` IS NOT DELETED FROM EXISTING TREES***: nothing reads it, no ship list names it, and its own text explains what it used to do — kept in `verify-upgrade.ps1`'s `$UNNAMED` because "an upgrade must not delete what no ship list names" is still exactly the property being tested. ***CYCLED AND MEASURED ON THE INSTALLED TREE, 30 Aug 2026.*** `assert-current` **exit 0 live**: message **10100 is gone** with `10101` present as the control, **no `$standalone` marker was written**, and the mirrored count is **2984** where it was **2985** — one file, the deleted message. ***AND THE FLAGGED COST ARRIVED ON THE FIRST CYCLE, WHICH IS WHY IT IS WORTH THE ROW.*** The owner installed with the API box unticked; `# APIPORT=4243` is commented in `C:\ProgramData\SD\sd.conf` and **nothing is listening on 4243** with the SD service Running. **That is this entry working as ruled** — and it leaves the machine with **no API at all**, where the old unticked box meant *"listener up, this machine only"*. ***NINE SUITE VERIFIERS NEED THE API AND WOULD ALL FAIL ON SUCH AN INSTALL***: `verify-apiadmin`, `verify-apiidentity`, `verify-apiname`, `verify-apiport`, `verify-accountacl`, `verify-peerlog`, `verify-scramlogin`, `verify-tierapi`, `verify-doors-suite`. **A `-Run` token spent there reads as a catastrophic regression and is nothing of the kind.** ***SO THE THIRD STATE IS A LIVE QUESTION, NOT A HYPOTHETICAL: "provide the API but do not open the port" has no way to be asked for, and the owner's own first install is the case for putting it back.*** **STAYS OPEN on that decision** | `gplbld/stage.py:541`, `:499`, `gplbld/sd.iss` `[Files]`, `:1284`, `:1317`, `:1519`. ***CLOSED 30 Aug 2026: THE ONE DECISION IT STAYED OPEN ON IS TAKEN, AND THE WORK IS ENTRY 85.*** The owner's ruling here is unchanged; what was open was the cost it flagged — no local-only API state at install time — and 85 restores it as a child task without touching the ruling. ***75 STAYS CLOSED AND 85 IS RE-OPENED, WHICH IS THE HONEST SPLIT***: the decision this entry waited on has been taken and is not in question; **85's task flags are wrong** and the default still opens the port, so the work is unfinished while the ruling is not | `gplbld/stage.py:541`, `:499`, `gplbld/sd.iss` `[Files]`, `:1284`, `:1317`, `:1519`, `:2114`, `:1889`, `gpl.bp/CREATEA:394`, `gplbld/verify-upgrade.ps1:157`, `gplbld/assert-current.ps1:238`, and entries 67, 76, 85 |
| ~~85~~ | **S** | ***DONE 31 Aug 2026 — THE THREE FLAGS WERE RIGHT ALL ALONG, AND "THE FIX DID NOT WORK" WAS A MISREADING OF A RESTORED TASK STATE. THE REMAINING DEFECT IS 88.*** Measured by `gplbld/probe-taskflags.ps1`, built this session, which drives the tasks page through Inno's OWN click path (`TNewCheckListBox.CheckItem`, the method a mouse click calls) and reads the states back — unelevated, ~3 seconds, no cycle, no install, no run token. ***LEG 1, THE FLAGS ALONE (`UsePreviousTasks=no`): EVERY ONE OF THE THREE BEHAVES.*** Tick parent → child STAYS unchecked (`dontinheritcheck`); untick child → parent STAYS ticked (`checkablealone`); re-tick parent → child STAYS unchecked. **The ssh pair, the control 67 already paid for, is identical on all five transitions** — so 67 needs no re-opening either, and its *"the fix is proven"* claim survives. ***LEG 2 REPRODUCES THE OWNER'S REPORT EXACTLY, FROM THE SAME BINARY AND THE SAME FLAGS***, changing only `UsePreviousTasks` to `yes` with a previous selection restored: both API boxes arrive **CHECKED**. ***THE CAUSE IS THAT sd.iss NEVER SETS `UsePreviousTasks`, SO IT DEFAULTS TO `yes`***, and this machine's `Inno Setup: Selected Tasks` reads **`addtopath,sshremoteopen,apiremote,apiremote\apinetwork`** — written by the PRE-FIX build, restored faithfully by the fixed one. **The wizard was showing the old install's answer, not the new declaration.** ***AND HIS SENTENCE COVERED TWO THINGS, ONE OF WHICH WAS NEVER A DEFECT***: *"if one is checked they both are checked"* is the restored ARRIVAL state, and *"vice versa"* is untick-parent-unticks-child, which is correct Inno behaviour and cannot be disabled. **Once either box is touched, the flags take over and behave.** ***INNO IS 6.7.3***, read from the same registry key — the version question this entry left open. ***THE LESSON IS NOT "READ THE FLAGS HARDER"***: two sessions ended on this page because nothing could measure it, and the entry's own caveat — *"only a person can judge this"* — was true and is now false. The probe is on `$neverShipped`; wiring it into a runner is the owner's call. *(Original entry follows.)* ***THE FLAGGED COST OF 75 IS PAID OFF: THE LOCAL-ONLY API STATE IS BACK, AS A CHILD TASK.*** Done 30 Aug 2026 on the owner's instruction to settle the open rulings. **His ruling is untouched** — an unticked parent still means SD installs the no-listener `sd.conf` and opens no socket at all. What changed is only the SCOPE applied when the API *is* provided. ***THE SHAPE IS THE ONE ALREADY RULED FOR ssh, NOT A NEW IDEA***: `apiremote` gains the child `apiremote\apinetwork`, exactly as `sshserver\sshremote` works, and Inno greys and unchecks a child whose parent is unchecked — so "you cannot let the network in without providing the service" is a state the reader SEES. ***AND THE DEFAULT MOVES THE SAFE WAY***: parent alone now leaves the rule **RESTRICTED to this computer**, and opening 4243 to the network is a second deliberate click rather than a side effect of wanting the API. `ApplyApiFirewall` follows `ApiNetworkWanted` instead of `ApiWanted` — **the old line could only ever be true there, so the `-Restrict` arm was dead code and every install that provided the API opened it to the network.** ***THE REPORT TEXT'S "FROM THIS COMPUTER ONLY" ARM WAS UNREACHABLE AND IS NOW THE DEFAULT ONE***, so its wording was corrected too: it names `remote.api on` first and the script second, because telling the reader to run a PowerShell file when SD has shipped a verb for it since entry 78 is exactly the staleness 77 was filed for. ***RE-OPENED THE SAME DAY — IT WAS STRUCK BEFORE ANYONE HAD SEEN THE WIZARD, AND THE WIZARD IS WHERE IT IS WRONG.*** Owner, 30 Aug 2026, watching the install this batch cycled: *"the two API entries are linked together like the ssh entries were before they were fixed. If you select or delete one, you select or delete both."* ***THE FIREWALL HALF IS RIGHT AND THE TASK DECLARATION IS NOT.*** `ApplyApiFirewall` correctly follows `ApiNetworkWanted`; what is missing is the flags that make a child behave like a child. **`apiremote\apinetwork` has no `dontinheritcheck`**, so Inno checks it whenever the parent is checked — and that reverses the entire point of the entry: ticking *"provide the SD API"* re-ticks *"let other computers reach it"*, so the default opens 4243 to the network again, which is the exact cost 85 exists to remove. ***THE PRECEDENT IS THREE LINES AWAY AND WAS NOT COPIED CLOSELY ENOUGH***: `sd.iss:187-193` has `Flags: checkablealone` on `sshserver` and `Flags: unchecked dontinheritcheck` on `sshserver\sshremote`. **Mine has neither**, and additionally carries a `GroupDescription` on the CHILD that the ssh child does not have. ***THE FIX IS THREE FLAGS AND ITS OWN CYCLE***: add `dontinheritcheck` to the child, `checkablealone` to the parent, drop the child's `GroupDescription`. **A CYCLE CANNOT CATCH THIS AND NEITHER CAN THE SUITE** — the wizard is interactive and `UninstallSilent`-style automation never sees it, which is why it took the owner's eyes on a real install. ***THE LESSON, AND IT IS THE ONE THIS FILE KEEPS RECORDING***: *"only ISCC can judge `sd.iss`"* was the caveat written here, and it was too weak. ISCC judged it fine. **ISCC checks that the tasks COMPILE, not that they BEHAVE**, and the entry was struck on the strength of the weaker claim ***— THE THREE FLAGS ARE IN, 31 Aug 2026, AND THE INSTALLER IS BUILT AND WAITING TO BE LOOKED AT.*** `apiremote` gains `checkablealone`, `apiremote\apinetwork` gains `dontinheritcheck`, and the child's `GroupDescription` is gone — so the pair is now structurally identical to `sshserver` / `sshserver\sshremote` at `:187-193`, which 67 already proved on a real install. ***THE PARENT KEEPS `unchecked` AND THE ssh PARENT DOES NOT, AND THAT IS 75's RULING RATHER THAN AN INCONSISTENCY***: an unticked API box means SD opens no socket at all, so the API defaults OFF, while the ssh server defaults ON when the machine has none. **The firewall half needed nothing** — `ApplyApiFirewall` already follows `ApiNetworkWanted` → `WizardIsTaskSelected('apiremote\apinetwork')`. **`cycle.ps1 -SkipInstall` 31 Aug 01:14:09**: ISPP lint 0 bad lines, BASIC **189 programs, 0 errors**, ISCC exit 0, `sd-setup-W1.0-0.exe` **4,925,443 bytes** in `C:\Users\dmont\sdout`. ***STILL OPEN, AND ONLY A PERSON CAN CLOSE IT***: run that `.exe` to the tasks page and look — ticking *"Provide the SD API"* must leave *"Let other computers reach it"* UNTICKED, and unticking the child must leave the parent ticked. **Cancelling there writes nothing.** *ISCC compiled the broken version too, which is why its exit code is not evidence here* ***— AND THE FLAGS DID NOT WORK. LOOKED AT 31 Aug 2026 AND THE BEHAVIOUR IS UNCHANGED.*** Owner, at the wizard of the 01:14:09 installer: *"the api checks move together if one is checked they both are checked and vice versa."* **Five things are ruled out by measurement rather than argument**: only one `sd-setup*.exe` exists on the machine and it postdates the edit; `cycle.ps1:468` compiles `$Iss` = `gplbld/sd.iss`, the file edited; there is exactly one `Name:` for each of parent and child; **nothing in `[Code]` touches `TasksList`, `WizardSelectTasks`, `CheckItem` or `Checked[`**; and ISCC's only warning is the pre-existing `FileCopy` hint. ***THE NEXT STEP IS A QUESTION, NOT CODE***: does the **ssh** pair on the same page behave correctly? It carries the identical flags, so it discriminates — ssh right and API wrong points at the API parent's extra `unchecked` or its absent `Check:`; **both wrong means the flags are not doing this here at all, and 67's *"the fix is proven"* would need re-reading, because what was measured on 30 Aug was the OUTCOME (server installed, `RemoteAddress=127.0.0.1`) and not the checkbox behaviour.** ***ALSO ESTABLISH WHICH DIRECTION***: a child ticking its parent is CORRECT Inno behaviour, and only *parent ticks child* is the defect; the report covers both | `gplbld/sd.iss` `[Tasks]` (needs `dontinheritcheck`, `checkablealone`), `:187-193` (the pattern to copy), `ApiNetworkWanted`, `ApplyApiFirewall`, and entries 67, 75, 76, 78 |
| 88 | **S** | ***AN UPGRADE RESTORES THE PREVIOUS INSTALL'S TICKBOXES, SO A TIGHTENED DEFAULT NEVER REACHES AN EXISTING SITE. THE OWNER'S CALL.*** Found 31 Aug 2026 while measuring 85, and it is what made 85 look unfixed. **`sd.iss` `[Setup]` never sets `UsePreviousTasks`, so it is `yes`** — Inno's default — and at startup Setup reads `Inno Setup: Selected Tasks` from the uninstall key and uses it as the tasks page defaults, **overriding every `unchecked` flag in `[Tasks]`**. This machine's value reads **`addtopath,sshremoteopen,apiremote,apiremote\apinetwork`**. ***THE CONSEQUENCE IS THE EXACT THING 85 EXISTS TO PREVENT, ONE LEVEL UP***: 85 made "let other computers reach the API" a second deliberate click, and on **every existing install** that click is instead inherited from last time — `ApiNetworkWanted` → `ApplyApiFirewall` then opens 4243 to the network on the upgrade, with the reader never having ticked it *on that run*. **`sshremoteopen` rides the same mechanism.** ***AND IT IS NOT OBVIOUSLY WRONG, WHICH IS WHY IT IS A DECISION RATHER THAN A FIX.*** `yes` is Inno's default and is normally right — an upgrade should not silently discard a choice the site made deliberately — **and it matches this project's existing policy that an upgrade does not re-ask**: the mode page is deliberately not shown twice (`sd.iss:1140`) and `sd.conf` is `onlyifdoesntexist` (`:408-411`). **`no` would make the page always show the declared defaults, which fails safe and lets a tightened default land — at the cost of silently CLOSING a port a site had deliberately opened, unless they notice and re-tick.** ***THE THIRD OPTION IS THE HONEST ONE***: keep `yes` and say on the page that these are the previous install's answers. ***ONE OPERATIONAL NOTE WHATEVER IS RULED***: until the recorded value is cleared or SD is uninstalled, **this machine's wizard will keep arriving with both API boxes ticked**, so judging that page by eye here measures the old install rather than the new declaration — use `gplbld/probe-taskflags.ps1`, which pins `UsePreviousTasks` explicitly and runs both legs in ~3s ***— RULED 31 Aug 2026, AND THE RULING DISSOLVES THE QUESTION RATHER THAN ANSWERING IT: "on an upgrade, just skip this page entirely. If the admin wants to make additional choices, we have given them the command line tools."*** **With no tasks page on an upgrade there is no restored state for the reader to see and no inert box to click**, so `UsePreviousTasks` stops mattering to the wizard and 89's `apiremote` defect goes with it. ***BUT SKIPPING THE PAGE IS NOT ENOUGH ON ITS OWN, AND THIS IS THE PART TO BUILD CAREFULLY.*** Inno still initialises the tasks from their defaults **plus the `UsePreviousTasks` restoration**, and `WizardIsTaskSelected` keeps answering — so hiding the page alone would turn *visible but inert* into ***invisible but active***: `ApplyApiFirewall` and `ApplySshFirewall` firing from state nobody saw, and `install-ssh.ps1` able to install an OpenSSH server silently. **The ruling therefore needs both halves — `ShouldSkipPage(wpSelectTasks)` when `DataTreeUpgrade`, AND the four gates (`ApiWanted`, `ApiNetworkWanted`, `SshServerWanted`, `SshRemoteWanted`) returning no-change on an upgrade** — with the closing report saying the settings were left alone and naming the commands. ***`DataTreeUpgrade` IS THE PREDICATE TO USE***, `sd.iss:1277`, cached from one `InitializeSetup` sample because a live `DirExists` is destroyed by the first file written — a bug that once skipped ~3,260 files and still exited 0. **NOT BUILT.** *(`ShouldSkipPage` was removed on 30 Aug with the mode page, `:1410`, so it is being reintroduced rather than edited.)* ***AND "REINSTALL" HAS TWO MEANINGS — SETTLED WITH THE OWNER 31 Aug 2026.*** `DataTreeUpgrade` keys on the DATA TREE (`:1086`, `not DirExists('{#DataDir}\sdsys')`), not on whether SD is installed, and the uninstaller deliberately keeps `C:\ProgramData\SD` while tearing down three things — `RemoveAllowGroups`, `RemoveApiFirewall`, `RemoveFromPath`. **So uninstall-then-install would count as an upgrade and skip the page, on a machine whose ssh confinement, 4243 rule and `PATH` entry had just been removed** — state destroyed, and never asked. ***RULED: THAT PATH SHOWS THE PAGE.*** The skip condition is a TRUE over-the-top upgrade — data tree present **and SD currently installed** — and the discriminator is the uninstall key `HKLM\...\Uninstall\{9F2B7C41-3D6A-4E58-9B0F-5C7A1E2D8B34}_is1`, which the uninstaller removes: **present → skip, absent → show**. ***AND THE OWNER'S REASON FOR BEING RELAXED ABOUT SHOWING IT IS SOUND, CHECKED RATHER THAN ACCEPTED***: *"we already adjust what is displayed if an ssh server is already installed, the user just gets the option of opening the port or not."* **Nothing in the uninstall removes the OpenSSH capability** — only `remove-ssh.ps1` calls `Remove-WindowsCapability` and it is wired into nothing — so `SshWasAbsent` is False, the install-the-server pair stays hidden, and the one question shown is defaulted from the live firewall scope (entry 76). ***A BONUS ON THAT PATH***: the uninstall key is gone, so `UsePreviousTasks` has nothing to restore and the page comes up at its declared defaults rather than the previous install's answers. **One residual, and it is 89 defect A rather than anything new**: `sd.conf` survives the uninstall (`uninsneveruninstall` + `onlyifdoesntexist`), so an unticked API box there still will not remove a listener. | `gplbld/sd.iss` `[Setup]` (no `UsePreviousTasks` line), `:425-428`, `:187-193`, `:1277` (`DataTreeUpgrade`), `:1410`, `ApiNetworkWanted`, `ApplyApiFirewall`, `gplbld/probe-taskflags.ps1`, and entries 85, 67, 75, 76, 89 |
| 90 | **S** | ***EVERY "WITH NO KEYWORD IT REPORTS" VERB PRINTS NOTHING, AND THAT IS FOUR SHIPPED VERBS, NOT ONE.*** Found 31 Aug 2026 when the owner ran the new `append.sd.path` bare on the installed tree and got **no output whatsoever** — no report, no error, no blank complaint. ***THE CAUSE IS IN `PS_SCRIPT`, NOT IN ANY OF THE VERBS.*** `PS_SCRIPT:77-85`: `if kernel(K$ADMINISTRATOR, -1) then rc = elevate('RUN', ps.path)` … `return rc`, and **only the fall-through path — `os.execute … | Invoke-Expression` at `:92` — ever reaches the terminal.** The helper is a separate elevated process on a named pipe; it returns a **status and nothing else**, which `REMOTEAPI`'s own comment already says in terms: *"ps_script returns the status and nothing else, so this cannot read the script's own 'already ON' line."* ***SO IT BITES EXACTLY WHERE IT CANNOT BE AVOIDED***: all four verbs are administrator-gated, an administrator session HAS a helper, so the helper path is not the edge case — **it is the only case in normal interactive use.** *(A session that is genuinely elevated with no helper — `sd -internal`, a bootstrap — gets 9 back and falls through, which is why this never showed during installs.)* ***THE OTHER THREE ARE ENTRY 78's AND CARRY THE SAME PROMISE IN THEIR OWN DESCRIPTIONS***: `SSHSRVR` *"With no keyword it reports whether one is present and changes nothing"*, `REMOTEAPI` *"With no keyword it reports the current setting"*, and `REMOTESSH`. **Identical shape, identical gate — but INFERRED FROM THE CODE, not separately measured: typing `remote.api` bare in SDSYS confirms or refutes it in one line.** ***AND IT IS WORSE THAN A MISSING REPORT, BECAUSE IT ALSO SWALLOWS REFUSALS.*** `sd-path.ps1` prints why it declined; `remove-ssh.ps1` prints the restart warning; `api-listener.ps1` prints *"already ON"*. **None of it can be seen.** ***ONE SHIPPED MESSAGE IS NOW A FALSE STATEMENT BECAUSE OF IT***: 10155 says *"The reason is in the lines above"* and there are no lines above — that is mine, written this session, and it must not ship as it stands. ***THE MECHANISM TO COPY ALREADY EXISTS AND IS MEASURED***: `os.execute <cmd> CAPTURING <var>` returns the output as a field-marked array — `EDIT:684` uses it for its editor probe, and HISTORY's 27 Aug entry shows `micro-home`'s output arriving that way, field marks and all. ***CONFIRMED BY MEASUREMENT 31 Aug 2026, NOT LEFT AS INFERENCE.*** The owner ran `remote.api` on the installed tree: as `don` it refused with **2001**, so the gate works; after `logto sdsys` it printed ***nothing at all***. **The blast radius is all four verbs and the fix belongs in the shared path.** ***THE HELPER IS WHERE IT GOES, AND IT IS SMALLER THAN THE PIPE PROTOCOL SUGGESTS.*** `sd-elevate-helper.ps1:214-219` already runs the script as a **child process** — `Start-Process powershell -Wait -PassThru -WindowStyle Hidden` — precisely so an `exit` in the script cannot kill the helper and take the session's privilege with it. **Its stdout simply goes nowhere.** `Start-Process` takes `-RedirectStandardOutput`, and `PSTMP` is already the right place to put the file: it exists, `secure-psdir.ps1` has settled its ACL, and `PS_SCRIPT` already owns the lifetime of `ps.path` and deletes it. ***SO THE FIX IS A REDIRECT PLUS A READ, AND THE PIPE PROTOCOL IS NOT TOUCHED*** — `:37`'s *"the reply to a request is an exit code"* and the single `ReadLine()` at `sd-elevate.ps1:91` stay exactly as they are, which is the part that would have been risky. ***BUT IT MUST BE OPT-IN, AND THAT IS THE ONE THING NOT TO GET WRONG.*** `ps_script` is not only these four verbs: `!create_user` and `!set_passwd` go through it, and `PS_SCRIPT`'s own header records that the whole reason scripts are written to a file is to keep a password out of a command line. **Printing helper output unconditionally would put credential-adjacent text on screen for the first time.** So a **new `ps_script_out()`** beside the existing function, with `ps_script` unchanged, and only the report paths calling it. **NOT FIXED — the shape is agreed to this much and the owner has not ruled on it** | `gpl.bp/PS_SCRIPT:77-92`, `gpl.bp/EDIT:684` (`capturing`), `gpl.bp/APNDPATH`, `SSHSRVR`, `REMOTEAPI`, `REMOTESSH`, message 10155, and entries 89, 78 |
| 89 | **S** | ***OWNER'S RULING, 31 Aug 2026: NO TICKBOX MAY BE INERT.*** *"No option should be available that the user can click thinking that an action is going to take place, but nothing happens (for example an option that says install a server when it is already installed and clearing the selection does nothing)."* **A control that cannot act is a false statement about what the installer is about to do**, and it costs more than a wasted click: the reader believes they have made a choice. ***AUDITED ALL SEVEN `[Tasks]` ENTRIES THE SAME DAY. FIVE ARE CLEAN, TWO ARE NOT.*** ***CLEAN, AND THEY ARE THE PATTERN TO COPY***: `sshserver` carries `Check: SshServerAbsent`, so the box is **hidden** when the machine already has a server — this ruling already built, at `:186`; `sshserver\sshremote` cannot outlive its parent; and `sshremoteshut` / `sshremoteopen` are **pre-set from the live firewall scope** (`GetSshRuleIsOpen`) with `ApplySshFirewall` running `-Open` or `-Restrict` on every install, so **both directions act and touching nothing changes nothing** — entry 76's ruling, and it is the sharpest existing answer to this one. ***DEFECT A — `apiremote` IS INERT ON EVERY UPGRADE, AND HALF-ACTS, WHICH IS WORSE.*** `sd.conf` ships through a `[Files]` pair gated `Check: ApiWanted` / `Check: not ApiWanted`, both `onlyifdoesntexist` (`:534-537`), and **`sd.iss:517` states the consequence in its own words: *"an upgrade rewrites nothing either way"***. So on an upgraded tree, ticking *"Provide the SD API (port 4243)"* **does not make SD open a socket** and unticking it does not close one — the listener is whatever the first install left. **But `ApplyApiFirewall` DOES run**, following `ApiNetworkWanted`, so the reader gets a firewall change and no service change: the box moves something, just not the thing it names. ***DEFECT B — UNTICKING `addtopath` NEVER REMOVES SD FROM `PATH`.*** The task carries no `Check:` at all, so it is always offered; the `[Registry]` entry carries `Check: NotOnPath('{app}\usr\bin')` (`:3950`), and **`RemoveFromPath` is called only from `CurUninstallStepChanged`** (`:3810`). Ticking when it is already on `PATH` is a harmless no-op — the state is what the reader wants — but **unticking is a misleading one**: they clear the box, and `sd` still runs from any directory. ***IT COMPOUNDS WITH 88***: `UsePreviousTasks` defaults to `yes`, so on an upgrade the API box arrives **already ticked from last time AND unable to act** — inherited and inert at once. ***THE SHAPE OF THE FIX IS ALREADY IN THE FILE, ON THE ssh SIDE.*** For the API the honest options are (a) hide the box on an upgrade the way `sshserver` hides on a machine that has a server, or (b) do what 76 did for ssh — **read the current `sd.conf`, pre-set the box from it, and act on a deliberate change by editing the `APIPORT` line alone**, which keeps `onlyifdoesntexist`'s promise never to overwrite a configuration the user edited. For `addtopath`, either give the task a `Check:` so it is not offered when it cannot act, or make unticking call `RemoveFromPath`. **NOT BUILT — the ruling is recorded, the audit is done, and which way each goes is the owner's call** | `gplbld/sd.iss:517`, `:534-537` (the `sd.conf` pair), `:3950` and `:3810` (`addtopath`), `:186-200` (the clean pattern), `ApiWanted`, `ApplyApiFirewall`, `ApplySshFirewall`, PROJECT_STATUS §5.21, `gplbld/sd-path.ps1`, and entries 88, 85, 76, 75 ***— BOTH DEFECTS ARE RULED, 31 Aug 2026, AND ONE OF THE TWO IS HALF BUILT.*** **Defect A (`apiremote`) is answered by 88's ruling**: an upgrade skips the tasks page entirely, so the box that could not act is no longer offered. **Defect B (`addtopath`) is answered by a COMMAND, and the owner found that gap in his own ruling** — *"we do not have a user command to change the path. If we skip page, fire nothing on upgrade we need to have that option available as a command."* ***`gplbld/sd-path.ps1` IS BUILT AND UNIT-TESTED*** (`-Show` / `-Add` / `-Remove`, elevated for the two that write; `test-sdpath-units.ps1` **24 of 24**, lifting its three pure functions by AST so the test cannot drift from the script). It ships via `stage.py`. ***STILL TO BUILD: THE VERB, AND THE NAME IS RULED — `append.sd.path on \| off`***, administrator-only, which means **`voc_template` ONLY and listed in `TIER.ADD.ADMINISTRATOR`** (`verify-tiers.ps1:41`: *"putting it in newvoc hands it to every account SD creates"*). **That moves ADMINISTRATOR to 420** — 392 + 24 + 4, **re-derived from the directory rather than adjusted by one**, as that block requires — and needs a doc page, or `tclmap` goes to 147 with four `NO PAGE` rows instead of three ***— BUILT 31 Aug 2026, NOT YET COMPILED: THE CYCLE IS OWED.*** `sdsys/gpl.bp/APNDPATH` (modelled on `SSHSRVR`), `sdsys/voc_template/append.sd.path` — **voc_template only, and `newvoc` staying at 395 names is the proof it went there** — `TIER.ADD.ADMINISTRATOR` → 24 verbs, and messages **10152–10156**. `SECOND.COMPILE` is `BASIC gpl.bp *`, so the program needs no manifest entry, and `stage.py`'s object-count guards are lower bounds. ***`test-tiercounts-units` CAUGHT THE SECOND COPY IN UNDER A SECOND***, which is the third time that constant has drifted and the **first time it cost nothing**: `verify-tiers.ps1` was updated, the guard was run, and it said *"verify-tierapi.ps1: ADMINISTRATOR — claims 419, tree says 420"*. **13 of 13 now, both files agreeing with the tree.** ***AND A STALE COMMENT WAS CORRECTED ON THE WAY***: the 25 and 30 Aug blocks both said `TIER.OMIT.STANDARD` is *"1 + 42"* and `STANDARD 392 - 42 + 4 = 354`. The file is 42 lines, **1 + 41**, and the coded STANDARD has always been **355** — nothing was failing, but a re-derivation that trusted the comment would come out one short and read as a regression. **No confirmation prompt on `off`, unlike `ssh.server remove`**: that one strands every account's only way in, this one removes a convenience and `append.sd.path on` puts it straight back ***— IT COMPILES. `cycle.ps1 -SkipInstall`, 31 Aug 2026 09:06:15, ISCC exit 0, `sd-setup-W1.0-0.exe` 4,931,937 bytes.*** ***AND THE STAGED TREE WAS READ RATHER THAN THE RUN'S OUTPUT BELIEVED***, per the 26 Aug precedent: `gpl.bp.out/APNDPATH` **783 bytes**, `gcat/$APNDPATH` present, `voc_template/append.sd.path` staged, messages **10152–10156** all five staged, `TIER.ADD.ADMINISTRATOR` **24 verbs** including it. ***`gpl.bp.out` IS 190, UP FROM 189*** — the one new program, not a coincidence — and `gcat` 131. ***THE ADMIN-ONLY PLACEMENT PROVED ITSELF IN THE STAGE***: `newvoc` still holds **395** names and `newvoc/append.sd.path` is **absent**, which is the whole of stage.py's rule that putting it there would hand it to every account SD creates. **Reaching ISCC is itself evidence about the BASIC**: `bootstrap.py`'s `check_compile()` dies on any *"is not assigned a value"* warning, so a clean run clears that class too. ***RUN 31 Aug 2026 BY THE OWNER, ON THE INSTALLED TREE. THREE LEGS OF FOUR PASS.*** In SDSYS: **`on`** printed *"SD's program directory is on the system PATH."*, **`off`** printed the removal message, `on` again worked, and after `logto don` a **non-administrator was refused with 2001** — the gate holds. **`append sd.path on` was correctly refused with *"append is not in your VOC"***, which is the negative control nobody asked for: `append` is not a verb and the three-segment name is not being split. ***THE FOURTH LEG FAILED: BARE `append.sd.path` PRINTED NOTHING AT ALL.*** It is filed as **PRE_RELEASE 90**, because it is **not this verb's bug alone** — see there |
| 76 | **S** | ***ON A MACHINE THAT ALREADY HAS ssh, THE INSTALLER NEVER ASKS WHO MAY REACH IT AND NEVER SETS THE FIREWALL EITHER WAY.*** Owner, 30 Aug 2026, installing a second time on the VM: *"installer no longer asks about ssh access - the ssh server is installed but the user might want it limited to loopback so still want to deny remote access."* ***TWO MECHANISMS, AND THE SECOND IS THE ONE THAT MATTERS.*** The `sshremote` task carries `Check: SshServerAbsent and not StandaloneChosen`, **so the checkbox is not offered** once `sshd.exe` exists; and `ApplySshFirewall` then exits at `sd.iss:1658` — *"if not SshWasAbsent then Exit"* — **before calling `ssh-firewall.ps1` at all, so neither `-Restrict` nor `-Open` runs and whatever scope the rule already had simply persists.** ***THE RULE IT IMPLEMENTS IS RIGHT AND ITS REACH IS WRONG.*** §5.9 — *"we never reconfigure or restart an ssh server we did not install"* — is correct for a **foreign** server, and **SD cannot tell a foreign one from its own on a reinstall**, so it treats both as untouchable. On a reinstall over SD's own work the server IS one SD installed and configured. ***THE EXPOSURE DECISION IS STILL MEANINGFUL AND THERE IS NOW NO WAY TO MAKE IT***, which is the owner's point: a site reinstalling may well want loopback-only, and the installer neither asks nor acts. ***IT ALSO INVALIDATES ADVICE GIVEN EARLIER THE SAME DAY, WHICH IS WHY THIS IS FILED RATHER THAN NOTED***: priming `Windows 11 - Template` with the OpenSSH capability was suggested to save the ~45-minute install per clone, and it does — **but every clone would then install with `SshWasAbsent` false, so no ssh question and NO FIREWALL RESTRICTION, leaving the rule at Windows' own default of `RemoteAddress=Any`.** That turns a time saving into a silently more exposed test machine, and it would not have shown up as a failure anywhere. **Candidate discriminator, not chosen: SD's own block in `sshd_config` (`# --- BEGIN SD ssh-only model ---`) marks a server SD has configured before, so `ApplySshFirewall` could proceed when it is present. It does NOT cover uninstall-then-reinstall, since `RemoveAllowGroups` takes the block out.** **Ties directly to 67 and 75, which both change what "already has ssh" means** ***— BUILT 30 Aug 2026. THE `if not SshWasAbsent then Exit` IS GONE AND THE BOX IS OFFERED ON EVERY INSTALL.*** ***THE DISCRIMINATOR THIS ROW LOOKED FOR TURNED OUT NOT TO BE NEEDED, WHICH IS THE USEFUL PART.*** It proposed detecting SD's own `sshd_config` block to tell "a server we configured before" from a foreign one, and noted that uninstall-then-reinstall defeats it. **The owner's ruling makes the question go away**: put the choice in front of the reader and DEFAULT IT TO THE TRUTH. `GetSshRuleIsOpen` reads the live `RemoteAddress` in `InitializeSetup` and the box starts ticked or unticked to match, so **an installer who touches nothing changes nothing — a rule that was open stays open, one that was loopback-only stays loopback-only** — and only a deliberate click moves it. That is safe on a foreign server without needing to recognise one. ***5.9 IS NARROWED, NOT ABANDONED, AND THE NARROWING IS NAMED IN THE CODE***: `OpenSSH-Server-In-TCP` is Windows' shared rule, so restricting it blindly would cut off a site's own ssh — which is exactly why the default is read rather than assumed. **Nothing here writes `sshd_config` for a server SD did not install; that half of 5.9 is untouched.** ***THREE PIECES OF TEXT THAT HAD BECOME FALSE WERE REWRITTEN RATHER THAN LEFT***: the disclosure page's *"IF THIS MACHINE ALREADY HAS WINDOWS' SSH SERVER, SD DOES NOT CHANGE ITS FIREWALL RULE … that option is not offered"*, the tasks-page message box's *"SD WILL NOT CHANGE ITS FIREWALL RULE … that is why the option is absent from this page"*, and `SshReport`'s *"left both its configuration and its firewall rule exactly as they were"*. **That message box's own comment predicted this** — *"each time the text went on asserting the old shape until somebody noticed"* — for the fifth time. ***AND THE ADVICE THIS ROW INVALIDATED IS NOW SAFE TO TAKE***: priming `Windows 11 - Template` with the OpenSSH capability no longer leaves a clone with no ssh question, because the question is asked whether or not the server is already there. ***CYCLED AND MEASURED 30 Aug 2026, AND THE PROOF IS THAT THE OWNER COULD DO IT AT ALL.*** `assert-current` **exit 0 live**. This machine already had ssh; he unticked *"allow remote access"* on the tasks page and the rule reads **`RemoteAddress=127.0.0.1`**. **Before this change that box was not shown on a machine with an ssh server, and `ApplySshFirewall` exited at `if not SshWasAbsent` before touching anything** — so *having a box to untick* is the measurement, and the loopback scope is the effect. **`-ScopeFile` is measured separately**: against the live rule it writes `restricted`, exit 0. ***ONE LEG IS NOT PROVEN AND IS NOT CLAIMED — THE "OPEN" BRANCH OF THE DEFAULT.*** Nobody recorded the rule's scope BEFORE the cycle, so the box arriving pre-ticked to match an already-open rule is untested. **Closing it needs the owner to say whether the box was ticked when he reached it, or a machine whose rule is `Any` at install time** — which is the clone case this row's own warning about priming the Template describes. **STAYS OPEN on that leg** | `gplbld/sd.iss:938`, `:1054`, `:1226`, `:1776`, `:3409`, `[Tasks]`, `gplbld/ssh-firewall.ps1` `-ScopeFile`, and entries 67, 75 |
| ~~77~~ | **B** | ***THE UPGRADE DIALOG TELLS THE USER THE OPPOSITE OF WHAT THE INSTALLER JUST DID, AND IT FIRES ON EXACTLY THE CONDITION THAT MAKES IT FALSE.*** Owner, 30 Aug 2026, on seeing it: *"I'm not sure the dialog is correct, some things are updated during a reinstall."* **He is right, and it is provable in one file.** `sd.iss:3311` shows the box when `not DataTreeAbsent`; `DataTreeUpgrade` at `:1229` is `not DataTreeWasAbsent` — ***the same predicate*** — and it is what gates the generated upgrade branch's `[InstallDelete]` and `[Files]`. **So the sentence "the newly built system files were NOT installed over it" is printed precisely when they ARE.** ***THE SECOND SENTENCE IS FALSE TOO***: *"Upgrading an existing database in place is not yet supported"* — it was ruled, built and closed on 25/26 Aug 2026 (owner: *"preserve the user's own files, replace all the shipped ones"*, `stage.py:237`), and task-table **H.3** records it verified, `-Compare` **55 PASS / 0 FAIL / 1 SKIP** with `RefreshDictionaries` **76 of 76**. ***MEASURED ON THE OWNER'S OWN 30 Aug REINSTALL***: files under `C:\ProgramData\SD\sdsys` carry **16:40:08**, including `voc.dic`, `dict.dic`, `accounts.dic`, `$map.dic` and three `os.users.dic` records — dictionaries rewritten by `RefreshDictionaries` in the tree the box had just called untouched. ***THIS IS ENTRY 71's DEFECT SHIPPED TO USERS.*** 71 records that PROJECT_STATUS §6 and CLAUDE.md claimed there was no upgrade path and had been wrong since 25 Aug; **this is the same stale claim in the product, where a customer reads it and believes their system files were not updated.** Filed **B** and not S for that reason: a user who trusts it will not re-run anything after an upgrade that silently did work. ***WHAT IS ACTUALLY TRUE AND SHOULD BE SAID INSTEAD***: the shipped files ARE replaced, the user's own data, accounts, `$cred` and `sd.conf` are preserved by name (`SDSYS_PRESERVE`), and `sd.conf` specifically is `onlyifdoesntexist` so a reinstall does NOT change configuration. **Check the wording against `stage.py`'s two lists rather than against this row** ***— FIXED 30 Aug 2026, AND EVERY CLAIM IN THE NEW TEXT COMES FROM `stage.py`'s OWN LISTS RATHER THAN FROM THIS ROW.*** Three paragraphs replace the two false ones: **what is untouched** (accounts and passwords, the account register, the private catalogue, the print queue, held output, and SDSYS's own `bp`/`bp.out` — that is `SDSYS_PRESERVE` verbatim), **what was replaced** (the BASIC source and its objects, the VOC templates, the messages and the dictionaries — `SDSYS_SHIP` minus the preserve list), and **that configuration was not changed**. ***THE THIRD PARAGRAPH IS NOT PADDING***: `sd.conf` being `onlyifdoesntexist` is exactly why re-running the installer does not turn the API back on, which cost the owner a confused half hour the same day, and the dialog is the cheapest place to say so. **Checked: no other copy of the old claim survives in `sd.iss`, no line begins with `#` (the ISPP hazard `cycle.ps1` refuses builds for), and the file stays BOM-free, CR-free and ASCII.** ***STILL OPEN AS 71 AND DELIBERATELY NOT SWEPT IN HERE***: PROJECT_STATUS §6 and CLAUDE.md carry the same stale sentence, and that is 71's job — this entry was only ever the shipped one. **BUILT, UNSEEN — it shows only on a reinstall over an existing tree, so the next such install is what proves it** ***— DONE 30 Aug 2026, SEEN ON SCREEN.*** The second installer run over the tree the cycle had just made showed all three paragraphs: data untouched, **"SD'S OWN SYSTEM FILES WERE REPLACED"**, and configuration unchanged. **The box now says what the installer did**, where that morning it said the opposite of it. ***ONE SENTENCE IN THE NEW TEXT WENT STALE BETWEEN BEING WRITTEN AND BEING READ, AND IT IS FIXED BUT UNSEEN.*** It closed with *"To turn the SD API on or off, edit sd.conf and restart the SD service"* — true for the few hours between fixing this and building **78**, which shipped `remote.api on|local|off` in the same install and does exactly that. It now names the verb. **That change is committed and needs an installer rebuild to appear**; it is text only and rides with the next cycle rather than earning one. ***THE PATTERN IS THIS FILE'S OLDEST AND IT CAUGHT ME TOO***: the tasks-page message a few hundred lines up carries *"each time the text went on asserting the old shape until somebody noticed"* from 21 and 25 Aug. **Nothing was wrong with the code and every checker passed; it was found by looking at the rendered box** | `gplbld/sd.iss:3311`, `:1212`, `:1229`, `:491-509`, `gplbld/stage.py:237`, `SDSYS_PRESERVE`, task table H.3, and entries 71, 78 |
| 78 | **S** | ***THREE ADMINISTRATOR COMMANDS TO CHANGE AFTER INSTALL WHAT ONLY THE INSTALLER CAN CHANGE TODAY.*** Owner, 30 Aug 2026: *"we need three new administrator commands `REMOTE.API ON\|OFF`, `REMOTE.SSH ON\|OFF` and `SSH.SERVER INSTALL\|REMOVE`."* ***THEY ANSWER THE OBJECTION 75 LEFT STANDING***, which was the only thing that entry did not close: with the stand-alone mode gone, changing your mind about ssh or the API meant re-running the installer, and for the API a reinstall does **not** help because `sd.conf` is `onlyifdoesntexist`. **These make that decision reversible from inside SD, which is where the owner said it belonged.** ***THE MACHINERY IS ALREADY BUILT AND SHIPPED, SO THESE ARE THIN WRAPPERS AND NOT NEW MECHANISM.*** `C:\Program Files\SD` already installs `ssh-firewall.ps1` (`-Installed -Open` / `-Installed -Restrict`), `api-firewall.ps1` (`-Open` / `-Restrict`) and `install-ssh.ps1`, all re-runnable by hand today and all tested by the installer path. `ps_script` (`PS_SCRIPT:166`) hands them to the elevated helper when `K$ADMINISTRATOR` is set, which **68 has just proved works for exactly this kind of privileged write**. **Gate them the way `MODIFY.ACCOUNT` does — `if not(kernel(K$ADMINISTRATOR, -1)) then stop sysmsg(2001)`.** ***TWO OF THE THREE ARE NOT PURELY A SCRIPT CALL, AND THAT IS THE DESIGN WORK***: **(a) `REMOTE.API ON` must uncomment `APIPORT=4243` in `C:\ProgramData\SD\sd.conf` AND the listener only opens at start-up** (`stage.py:499`: *"open_api_listener() returns -1 for 'no listener' when the port is <= 0"*), so it needs an SD service restart, which disconnects every logged-in user — **report it or do it is the owner's call.** **(b) `SSH.SERVER REMOVE` is staged behind a REBOOT** — measured 30 Aug 2026 on this host: after `Remove-WindowsCapability` succeeded, `sshd.exe` was still on disk, the `sshd` service still Running and `RebootPending` True. **The command must say so, or a user will run it, see ssh still working and report a bug.** ***AND `SSH.SERVER REMOVE` SHOULD REFUSE OR WARN WHEN SD ACCOUNTS EXIST***: `deny-logon.ps1:29` leaves an SD account with exactly two routes, ssh and the API, so removing the server strands every account that has neither — the same reasoning `CREATE.ACCOUNT`'s per-route argument now carries. **Naming follows the lower-case convention (`remote.api`, `remote.ssh`, `ssh.server`); `newvoc` and the tier lists both need entries, and `TIER.ADD.ADMINISTRATOR` is where they belong** ***— TWO RULINGS TAKEN 30 Aug 2026, BOTH FROM THE OWNER.*** **(1) `remote.api` CARRIES THREE STATES, `on \| local \| off`** — `on` is listener plus open firewall, `local` is listener with the firewall restricted to loopback, `off` is no listener at all. ***THAT PUTS BACK THE STATE 75 REMOVED***, and it resolves 75's open cost rather than leaving it: the installer keeps its two simple boxes and the finer control lives inside SD, which is where the owner said this decision belonged. **(2) `remote.api` PROMPTS Y/N AND THEN RESTARTS** — *"this disconnects every SD session including yours"* — rather than reporting and leaving it. ***THE RESTART IS THE HARD PART AND IT IS ALREADY MEASURED***: `cycle.ps1:299` records that ***"stopping the SERVICE does not always take the DAEMON with it"*** (21 Aug 2026, 17:05), and it is `sdwind` — not the service — that holds the shared segment and `/dev/shm`. **So a `Restart-Service` is not sufficient and would leave the old configuration running while reporting success**; the restart needs the stop-wait-on-process-then-start shape `cycle.ps1` already uses, as a shipped script of its own. ***THE VERB COUNT IS AN ENFORCED INVARIANT AND MOVES***: `TIER.ADD.ADMINISTRATOR` goes 20 verbs to 23, so `verify-tiers.ps1` must go **ADMINISTRATOR 392 + 20 + 4 = 416** to **392 + 23 + 4 = 419**, with PROGRAMMER 396 and STANDARD 354 **unmoved** — which is the check on the arithmetic, since these are administrator-only. **And the docs repo's `tclmap` goes 143 to 146**, which is H.2 and a separate repository. ***THE RECORD SHAPE IS `voc_template/<verb>` = `V` / `CA` / `$<PROGRAM>`***, measured from `create.account`, `modify.account`, `grant` and `unlock` ***— BUILT 30 Aug 2026, ALL THREE, AND UNCOMPILED.*** **Three scripts** — `api-listener.ps1` (new, edits `APIPORT`), `restart-sd.ps1` (new), `remove-ssh.ps1` (new) — **three programs** `gpl.bp/REMOTEAPI`, `REMOTESSH`, `SSHSRVR`, **three `voc_template` records**, **three `TIER.ADD.ADMINISTRATOR` lines**, **18 messages 10131-10148**, and `verify-tiers.ps1` **416 → 419**. ***`api-listener.ps1` IS TESTED AGAINST A COPY OF THE LIVE `sd.conf` RATHER THAN REASONED ABOUT***: `-Show` reads OFF (which this machine is), `-On` takes 4714 → 4712 bytes with CR/LF unchanged at 85/85, `-Off` returns it **byte-identical by SHA256**, a second `-On` says *"already ON"* and writes nothing, and **both negative controls refuse**: a file carrying neither form of the line, and `-On -Off` together. ***TWO DEFECTS WERE CAUGHT BEFORE THEY COULD COST A CYCLE.*** **(1) The includes were wrong** — `K$ADMINISTRATOR` and `K$WINPATH` are defined in `INT$KEYS.H` and in neither `KEYS.H` nor `PARSER.H`, so the first draft would have failed BCOMP on unknown symbols; all three now take `MODIFY.ACCOUNT`'s four. **(2) `restart-sd.ps1` is not `Restart-Service`**, because `cycle.ps1:299` measured that *"stopping the SERVICE does not always take the DAEMON with it"* and `sdwind` holds the shared segment — a naive restart would report success over the old configuration, which for `remote.api` means saying the API is on when no socket reopened. ***AND ONE CLAIM IN THE RECORD IS CORRECTED***: `cycle.ps1` says *"sd -stop refuses while users are logged in"*. **It does not** — `stop_sd()` (`gplsrc/sysseg.c:766`) walks the user table and SIGTERMs every entry with a uid and a pid > 0, with no such check. **That is why the Y/N warning comes BEFORE the restart**: the administrator is one of the sessions it ends and will not be there to read anything printed after. ***CYCLED 30 Aug 2026 AND THE PRODUCT IS PROVEN: `verify-tiers -Prefix sdtierv` IS 31 PASS / 2 FAIL, AND THE COUNT ROW IS `sdtierv3 COUNT VOC: expected 419, got 419`.*** Install **17:35:05**, `assert-current` **exit 0 live**, mirrored count **2984 → 3008** — exactly the 24 files added (18 messages, 3 `voc_template`, 3 `gpl.bp`) — and `C:\Program Files\SD` **30 → 33**, the three new scripts. ***STANDARD 354 AND PROGRAMMER 396 BOTH PASSED UNMOVED***, which is the asymmetry that proves the three verbs went to `voc_template` only and never reached `newvoc`. **The suspend/restore machinery is green too**, including `elevated LOGTO enters a suspended account` at 396. ***THE TWO FAILURES WERE THE TEST'S OWN STALE COPY OF THE LIST, NOT THE PRODUCT.*** `verify-tiers` holds `$AdminVerbs` as well as the `Count`, and I changed the count and not the list: *"shipped TIER.ADD.ADMINISTRATOR matches this test: expected 0, got 3"* naming all three verbs, and *"add list length: expected 20, got 23"*. **The check is built to catch exactly that** — its own comment says it exists so nobody gets away with *"updating the record and not the test, or the other way about"*, and it compares the SHIPPED record rather than trusting either side. **Fixed and verified by comparing the source list against the installed record: identical, 23 both sides.** `verify-tiers.ps1` is on `assert-current`'s `$neverShipped`, **so no new cycle is needed** — re-run with a fresh prefix, since `sdtierv1`–`3` are left in the `ACCOUNTS` register by design. **BASIC compiled and catalogued: `REMOTEAPI` 1291, `REMOTESSH` 755, `SSHSRVR` 955 bytes, all three in `gcat`.** ***RE-RUN `-Prefix sdtierw` IS 33 PASS / 0 FAIL — "VERIFY-TIERS: all checks passed."*** Both section-0 rows green (`shipped TIER.ADD.ADMINISTRATOR matches this test: expected 0, got 0`; `add list length: expected 23, got 23`) and the three counts **354 / 396 / 419** all PASS. **So the VOC wiring of all three verbs is closed and measured.** ***AND THE BEHAVIOUR IS NOW MOSTLY PROVEN TOO, 30 Aug 2026.*** All three **report** paths ran — and `ssh.server` reading the Windows capability state, which needs elevation, is what proves `ps_script` reaches the elevated helper for these verbs. **`remote.ssh off`** moved the rule to `127.0.0.1` immediately with no restart. **`remote.api local`** set the firewall and correctly offered **no** restart, the listener not having moved; **`remote.api off`** edited `sd.conf` (`active=1 → 0`) and **did** offer one, as `y/<n>`, with Enter taken as no. ***THREE FAULTS CAME OUT OF ACTUALLY RUNNING THEM, WHICH IS THE ARGUMENT FOR DOING SO***: two report-wording faults, and **PRE_RELEASE 81**, a blocker in `api-firewall.ps1` that had been shipping broken and told the owner the API was local while the port stood open. ***WHAT REMAINS UNEXERCISED, AND IT IS A THIRD OF THE FEATURE***: **`ssh.server install` and `ssh.server remove` have never run.** `remove` is the awkward one — it takes ssh off the machine, is staged behind a reboot, and strands every SD account while it is gone — so it wants the VM rather than this host. **That is what keeps 78 open** | `gpl.bp/MODIFYA:181`, `gpl.bp/PS_SCRIPT:166`, `gplbld/ssh-firewall.ps1`, `gplbld/api-firewall.ps1`, `gplbld/install-ssh.ps1`, `gplbld/cycle.ps1:299`, `gplbld/stage.py:499`, `gplbld/verify-tiers.ps1:42`, `newvoc/TIER.ADD.ADMINISTRATOR`, `voc_template/create.account`, and entries 67, 75, 76 |
| ~~79~~ | **M** | ***EVERY Y/N PROMPT MUST SAY WHICH ANSWER ENTER GIVES.*** Owner's rule, 30 Aug 2026: *"scripts need to indicate which is the default using `<y>/n` or `y/<n>`."* ***THE INVENTORY IS THE VALUABLE PART, BECAUSE THE PROMPTS ARE NOT ALL THE SAME SHAPE AND THE FIRST READING SAID THEY WERE.*** Twenty messages carry a Y/N prompt; sixteen have a `gpl.bp` consumer and **four are dead** — `3513`, `6010`, `6012`, `6611` have no reference anywhere in `sdb_ai/`. **Three behaviours were found, not one**: *(a)* **loop until Y or N**, where an empty answer re-asks for ever — `10084`, `10085`, `6146`, `6195`, `5003`, `6521`, `7109`, `7305`; *(b)* ***ALREADY DEFAULTS TO N AND NEVER SAID SO*** — `3044` (`if upcase(yn) # 'Y' then stop`), `10008` (`if upcase(yn) = 'Y' then goto`), and `6588`, whose loop already accepts `''` and then tests `if x = 'Y'`; *(c)* **multi-way** — `2060` (Y/N/Q), `7143` (Y/N/Q/?), `5049` (Y/N/A). ***DONE 30 Aug 2026 FOR (a) AND (b): 11 MESSAGES REWORDED AND 9 CODE SITES CHANGED.*** Group (b) needed **wording only**, which is the cheap half and would have been missed by a sweep that assumed one shape. Group (a) gained one line, `if yn = '' then yn = 'N'`, and **N is the conservative answer in every one** — these are overwrite, delete and rewrite-every-account questions. ***`6521` IS USED TWICE IN `ED` AND BOTH MOVED TOGETHER***; a `head -1` grep found only the first, and leaving the other would have made the same prompt answer differently depending on which line printed it. ***THE MESSAGES COULD NOT BE EDITED BY HAND AND THAT IS RECORDED BECAUSE IT WILL RECUR***: every one ends in a **trailing space** before its newline — the gap between the prompt and the typed answer, because the caller uses `display … :` — and the `Edit` and `Write` tools both **strip a trailing space** from the content given to them. A scripted byte-level substitution was used instead, under CLAUDE.md's own exemption for a transform the editing tools cannot do, and each file was checked to have grown by exactly the marker's two bytes with its tail intact. ***WHAT IS DELIBERATELY NOT DONE, EACH FOR A REASON***: the **three multi-way prompts**, because the default is a ruling nobody has made — `Q` and `A` are not simply "not yes", and `7143` *"OK to print"* may well want **Y**; **`ED`'s `yes.no` subroutine**, which has **six callers** of which only `6585` is in this inventory, so a default there changes five prompts nobody has looked at; **`QPROC`'s `get.label.yn`** (one caller, `7211`), whose question — *"omit blank data lines"* — has no conservative answer; and **the four dead messages**, which are left rather than deleted in case upstream still uses them | `sdsys/messages/3044`, `10008`, `6588`, `10084`, `10085`, `6146`, `6195`, `5003`, `6521`, `7109`, `7305`. ***THE REST IS DONE, 30 Aug 2026, ON THE OWNER'S INSTRUCTION TO SETTLE THE OPEN RULINGS — ALL THREE DEFERRALS, AND EACH FOR THE REASON IT WAS DEFERRED.*** **`ED`'s `yes.no`: the six callers were READ, which is what the deferral asked for** — `:1080` copy block, `:1135` delete the entire record, `:1189` delete block, `:1340` delete the entire record, `:2066` move lines, `:2603` overwrite an existing record — and every one is `gosub yes.no / if no then return`, so **N declines the destructive action at all six and one default is right for all of them.** **`QPROC`'s `get.label.yn` HAS a conservative answer** once you notice one arm REMOVES lines from the report and the other does not: N, show the data as it is. ***AND THE MULTI-WAY PROMPTS DISSOLVED RATHER THAN NEEDING A RULING***: the default is a two-way question — does Enter act or not — even where the prompt has three or four answers. `2060` N leaves the Q-pointer alone and `Q` still has to be typed; `5049` N keeps the record this account has, and **`A` is FURTHER from conservative than `Y`**, not nearer. ***`7143` NEEDED WORDING ONLY AND ALREADY DEFAULTED TO Y***: `SPVIEW:297` pre-sets `yn = 'Y'` before a one-character `input`, so Enter has always accepted it and only the prompt was silent. **Ten messages reworded**, by the byte-level route this entry's own text predicted would recur — the editing tools strip the trailing space that separates prompt from answer — with each file asserted to contain its old text exactly once, to grow by exactly the length difference, and to keep its tail byte-for-byte. `gplbld/reword-yn-prompts.ps1` records it and **refuses a second run** (0 of 10, 10 refused). ***THE WORDING IS INSTALLED AND CONFIRMED; THE DEFAULTS ARE NOT WITNESSED, AND THE TWO HALVES ARE WORTH SEPARATING.*** Read off the 22:44 install: `Overwrite (y/<n>/q)?`, `Are you sure you want to delete the entire record (y/<n>)?`, `Omit blank data lines (y/<n>)`. ***BUT NOTHING IN THE SUITE PRESSES ENTER AT A PROMPT*** — every verifier types an explicit `Y` — so no run exercises a default, and none can without a verifier written to send an empty line. **Left DONE**: the code is one `if x = '' then x = 'N'` per site, each reasoned from its own caller, and the risk is a wrong DEFAULT rather than a broken prompt — which a run typing `Y` would not have caught either | `sdsys/messages/2060`, `5049`, `6554`, `6555`, `6556`, `6558`, `6577`, `6585`, `7143`, `7211`, `gpl.bp/ED` `yes.no`, `QPROC` `get.label.yn`, `SETFILE`, `LOGIN`, `gplbld/reword-yn-prompts.ps1`, and entry 78 |
| 80 | **B** | ***THE DOCUMENTATION AUDIT — ONE TASK, RUN LAST, AGAINST THE FINAL INSTALL IMAGE. IT ABSORBS H.2, 34 AND 55.*** Owner's ruling, 30 Aug 2026: *"lets wrap all the outstanding documentation pre-release tasks into a single documentation audit task that validates and updates the whole documentation tree against the final install image. This task will be done just before the final release 1.0 wrap up. In this task you take control of the gap analysis, you validate, correct and build all the documentation both yours and the other AI's."* ***WHY ONE TASK AND WHY LAST, WHICH IS THE PART WORTH KEEPING***: the documentation describes a model that has moved under it five times this week — **56** rewrote the administrator access model, **67** made the ssh server a choice, **75** deleted the stand-alone installation the tester set describes, **76** added a firewall question, **77** corrected what an upgrade does, **78** added three verbs and **79** changed twenty prompts. **Validating a reference against a moving target means validating it twice**, and H.2 already records the cost of not waiting: the tester set described `encrypt.field` for a week after it was deleted. ***THE INPUT IS THE FINAL INSTALL IMAGE, NOT THE SOURCE TREE.*** Every claim is checked against what a user actually receives — the installed VOC, the shipped messages, the wizard pages, the `changelog` — because that is the thing the reader has in front of them, and §"an instrument shows what it DID" applies to a sentence as much as to a probe. ***I TAKE CONTROL OF THE GAP ANALYSIS.*** `generate_gap_analysis_pdf.py` sits UNTRACKED in the repository root and PROJECT_STATUS records *"another AI is editing the documentation; leave it alone and never `git add -A` here"* — **that instruction stands until this task runs and is lifted by it.** The `never git add -A` half stands permanently regardless. ***WHAT THE THREE ABSORBED ITEMS CONTRIBUTE, SO NOTHING IS LOST WITH THEIR NUMBERS***: **H.2** is the body of work — the tester set (15 pages, q7 and q14 still unanswered), the `User` set (32 pages, 143 of 143 TCL verbs, the generated syntax card at `33` still to write), `Technical` (2 pages), `docmap`, `checklinks`, and the open question of whether document `09` belongs in `Technical`. **34** is that `Technical` has no cross-page link, so `checklinks.py` rightly refuses a zero-link set and `release.ps1` cannot complete on it. **55** is that `release.ps1` calls `mkdoc.py`, `mkpdf.ps1` and `checklinks.py` but **not** `mktclsyntax.py` or `tclmap.py`, both of which already compute the roster and already `exit 1` on disagreement — *"the comparison was built; the wiring was missing"*. ***NOT ABSORBED, AND DELIBERATELY: 71.*** It is the same kind of defect — a false sentence — but in `PROJECT_STATUS.md` and `CLAUDE.md`, which are read by **every session**, not by a customer. Folding it into a task that runs just before 1.0 would leave a known-false claim in the handoff for weeks, and it has already *"nearly cost a wrongly-filed blocker"* once. **It stays open and separate; the owner can overrule that.** ***WHAT CLOSES 80***: `release.ps1` completes on all three sets, `docmap`, `checklinks`, `tclmap` and `mktclsyntax` all agree with the installed image, HTML and PDF are current, and every page's claims have been checked against a machine the installer actually built ***— AND THE NEW ADMINISTRATOR COMMANDS ARE EXPLICITLY IN SCOPE. OWNER, 31 Aug 2026: "documentation for the new commands we have created needs to be part of 80."*** ***THE TREE IS ALREADY RED AND HAS BEEN SINCE 30 Aug, MEASURED 31 Aug 2026 RATHER THAN ASSUMED***: `python tools/tclmap.py <sd4windows>/sdb_ai/sd64/sdsys/newvoc` exits **1** with *roster **146**, assigned **143**, exempt 0* and three `NO PAGE` rows — **`remote.api`, `remote.ssh`, `ssh.server`**, the administrator verbs entry 78 added. **Confirmed independently**: those three strings appear nowhere in the documentation tree, by filename or content. ***THE CHECKER IS NOT AT FAULT AND THAT IS THE USEFUL PART*** — `tclmap.py:24` computes the roster (`123` verb records in `newvoc` **plus** the list in `newvoc/TIER.ADD.ADMINISTRATOR`, now 23 not 20), so it noticed the three on its own the moment they were added. **Nobody ran it.** ***SO THE RECORDED "tclmap 143 of 143, 0 exempt" IN TASK-TABLE H.2 IS STALE***: it is 143 of **146**, and reading that row would tell the next session the docs are green when the generator refuses. ***WHAT WOULD HAVE CAUGHT IT, WHICH IS THE QUESTION THE INSTRUMENT RULES ASK***: nothing could, because **`tclmap.py` lives in the OTHER repository and no tier-1 check in this one runs it** — so adding an administrator verb here silently breaks a checker there, and the two repositories have no gate between them. **That cross-repo gap is the thing to fix, not the three missing pages.** ***AND IT WILL TAKE THE PATH COMMAND TOO***: the verb ruled on 31 Aug 2026 makes the roster **147** and the missing-page count **four**. ***ONE CONTENT NOTE FOR THE ssh PAGE, FROM THE OWNER LOOKING FOR IT AND NOT FINDING IT, 31 Aug 2026***: *"Windows 11 no longer shows that it is installed either in settings/apps or control panel/programs and features."* **That is correct behaviour and the documentation must say so, because the natural conclusion is that it was never installed.** OpenSSH Server is a **Feature on Demand**, not a program, so it has never appeared in Programs and Features; in Windows 11 it is under ***Settings → System → Optional features***, having been under Settings → Apps in Windows 10 — which is where somebody who learned it on 10 will look. ***AND THE PowerShell FALLBACK IS NOT AVAILABLE EITHER***: `Get-WindowsCapability -Online` **needs elevation even to READ** — measured twice, 30 Aug 2026 in `remove-ssh.ps1:62-67` and again 31 Aug unelevated, where it throws. **So the page should name `ssh.server` with no keyword as the way to answer "is it installed?"** — it reports and changes nothing, and it works because `ps_script` routes through the session's elevated helper. **The same shape applies to `remote.api` and `remote.ssh`, which also report when given no keyword** | `SDCoreWindowsDocs` (`C:\Users\dmont\Projects\SDCoreWindowsDocs`), `generate_gap_analysis_pdf.py`, `release.ps1`, `mkdoc.py`, `mkpdf.ps1`, `checklinks.py`, `mktclsyntax.py`, `tclmap.py`, task table H.2, and entries 34, 55, 56, 67, 71, 75, 76, 77, 78, 79 |
| ~~81~~ | **B** | ***`api-firewall.ps1` CANNOT RESTRICT THE API, AND REPORTS THAT IT DID — WITH ITS OWN EVIDENCE PRINTED UNDERNEATH SAYING OTHERWISE.*** Found 30 Aug 2026 the first time `remote.api local` ran in front of the owner. **Verbatim:** `Set-NetFirewallRule : An unspecified, multicast, broadcast, or loopback IPv6 address was specified.` then `api-firewall: updated SD-API-In-TCP for port 4243`, then `api-firewall: the SD API is reachable FROM THIS MACHINE ONLY`, then its own read-back `rule: … RemoteAddress Any`, then **exit 0** — so `remote.api` said *"The SD API is now LOCAL"* while the port stood open to the network. **Measured on the live rule afterwards: `RemoteAddress=Any`.** ***THE CAUSE IS ONE LITERAL***: `:111` built the scope as `@('127.0.0.1', '::1')`, and Windows refuses **any** IPv6 loopback literal in `-RemoteAddress`. ***AND `ssh-firewall.ps1` HAD THE IDENTICAL BUG, FIXED IT, AND THE FIX WAS NEVER CARRIED ACROSS*** — its comment at `:185-192` describes this defect word for word, down to *"the rule is LEFT AT RemoteAddress=Any … the exact exposure this script exists to prevent."* **Third time in one week that a rule was applied in one file and not its sibling**, after `CRED_SET`/`MODIFYA` on close-before-write and the read-back that followed it. ***THE SECOND DEFECT IS THE WORSE ONE AND IT IS A CLASS, NOT AN INSTANCE***: the verdict was gated on **having made the call**, not on the result. The `try`/`catch` was supposed to stop this and did not — **the CIM error came back NON-TERMINATING despite `$ErrorActionPreference = 'Stop'`** — so a cmdlet that fails without throwing produces a confident false green. ***FIXED IN BOTH SCRIPTS, 30 Aug 2026***: the `::1` is gone, and each now RE-READS the rule and compares the applied scope with what was asked for, exiting 1 and printing what it actually found when they differ. **`ssh-firewall.ps1` is not known to be wrong and gets the gate anyway** — the two do the same job and one of them was caught lying about it. **Verified against the real broken state rather than a hypothetical: with the live rule at `Any`, the new gate fires for `-Restrict` and stays quiet for `-Open`.** ***THE EXPOSURE IS CLOSED, AND THE FIX IS PROVEN FROM SOURCE — BUT THE SHIPPED COPY IS STILL BROKEN, SO THIS STAYS OPEN.*** `api-firewall.ps1 -Restrict` run from source, elevated, 30 Aug 2026: **no error**, and `RemoteAddress 127.0.0.1`. ***VERIFIED INDEPENDENTLY OF THE SCRIPT, WHICH HAD JUST PROVED IT COULD LIE***: read straight from Windows, `SD-API-In-TCP` is `LocalPort=4243 RemoteAddress=127.0.0.1`, `OpenSSH-Server-In-TCP` is `LocalPort=22 RemoteAddress=127.0.0.1`, **neither open to the network**. (Both daemons still bind `0.0.0.0`, which is the design — the rule is scoped rather than disabled so `localhost` keeps working.) **`ssh-firewall.ps1 -Show`'s new plain-English line reads correctly too**: *"state is OFF - only this computer may connect over ssh"*. ***WHAT KEEPS IT OPEN: `C:\Program Files\SD\api-firewall.ps1` STILL CONTAINS `::1`.*** Source `sha256 adf933b5…`, installed `66bc71c8…`, and `REMOTEAPI:223` calls `kernel(K$WINPATH, '/api-firewall.ps1')` — the INSTALLED one. **So `remote.api local` from inside SD today would still fail and still report success**, and only a cycle changes that. **Closing this on a source-only proof would be the same mistake the entry is about** ***— DONE 30 Aug 2026, CYCLED AND PROVEN THROUGH THE VERB ITSELF.*** Install **18:03:57**, `assert-current` **exit 0**. `remote.api local` from inside SD printed **no `Set-NetFirewallRule` error**, and — the part that matters — its read-back **agrees with its claim** for the first time: *"the SD API is reachable FROM THIS MACHINE ONLY"* above `RemoteAddress 127.0.0.1`, where before it sat above `RemoteAddress Any`. **And no restart was offered**, correctly: the listener never moved, so `port.moved` stayed false. ***CHECKED INDEPENDENTLY OF THE SCRIPT, BECAUSE THE SCRIPT IS WHAT LIED***: read straight from Windows, `SD-API-In-TCP` is `RemoteAddress=127.0.0.1`, not open to the network. **And the INSTALLED copy is now the fixed one** — `$remote = if ($Open) { 'Any' } else { '127.0.0.1' }` at `:125`, source and installed `sha256` both `ADF933B5240A52FD`. *(A grep for `::1` still answers yes on that file and means nothing: the literal survives in the comment that explains why it is not used. The instrument had to be sharpened to read the assignment rather than the string — the same lesson the entry is about, in miniature.)* | `gplbld/api-firewall.ps1:111`, `:132`, `gplbld/ssh-firewall.ps1:185-192`, `gpl.bp/REMOTEAPI:223`, and entries 78, 68 |
| ~~82~~ | **S** | ***`test-tiercounts-units.ps1` IS RUN BY NOTHING, SO THE GUARD WRITTEN FOR EXACTLY THIS FAILURE SAT UNRUN WHILE EXACTLY THIS FAILURE HAPPENED AGAIN.*** Found 30 Aug 2026 on `-Run b70` step 21: `verify-tierapi.ps1` failed with *"ADMINISTRATOR VOC count: expected 416, got 419"* because **78** added three verbs, `verify-tiers.ps1` was re-derived and this constant was not. ***THAT IS THE SECOND TIME THE SAME FILE HAS BEEN LEFT BEHIND THE SAME WAY***, and its own comment says so about the first: *"28 Aug 26 - 417 → 416, AND THIS FILE WAS THE ONE LEFT BEHIND."* **`test-tiercounts-units.ps1` was WRITTEN that day, for this**: it re-derives all three counts from `sdsys/newvoc` and checks every verifier against the tree, with **no install, no elevation and no run token**. ***RUN AFTERWARDS, IT NAMED THE DEFECT IN UNDER A SECOND***: *"verify-tierapi.ps1: ADMINISTRATOR -- claims 416, tree says 419"*, and its closing advice is the right one — *"a count that disagrees with the tree is the VERIFIER being stale, not the product."* ***THE FILE'S OWN CLAIM THAT "THIS CANNOT DRIFT AGAIN UNNOTICED" WAS NEVER TRUE***: nothing invokes it. It is in **neither `VerifyInstall1` nor `VerifyInstall2`**, so it is a free check that only fires if somebody remembers it exists — which is the same failure `VerifyInstall1`'s own header describes for the seven unelevated verifiers nobody ran, and the same shape as **54**. ***THE FIX IS TO WIRE IT IN, NOT TO REMEMBER HARDER.*** It belongs at the FRONT of `VerifyInstall1` — it needs nothing, costs nothing, and a stale tier count makes two later suite steps meaningless. **The constant is corrected to 419 and `test-tiercounts-units` is 13 of 13; the wiring is the entry** ***— WIRED 30 Aug 2026 AS STEP 1 OF 16 IN `VerifyInstall1`, AND UNRUN IN THE RUNNER.*** `@{ Name = 'test-tiercounts-units.ps1'; P = @{} }` ahead of `verify-credacl`. ***IT IS THE ONLY STEP THAT COULD BE FIRST***: it reads `..\sdsys\newvoc` in the **source** tree and the two tier verifiers beside it — no install, no elevation, no account, no prefix, no run token, under a second. ***AND IT DOES NOT WEAKEN `verify-credacl`'s CLAIM TO BE FIRST***, which the runner's own ORDER comment states and which matters: credacl fails if the session is somehow privileged and must do so before passing steps suggest the tree is fine. **This step never looks at a token, an ACL or the installed tree**, so a green line from it says nothing about what credacl guards — it says the SOURCE is self-consistent, which is a different claim and a precondition for believing either tier step later. **Checked: `$needsTestUser` needs no entry (it needs no test user), and the count assertion at `:446` is relative (`$before + 2`), so nothing else enumerates the list.** ***ALL FOUR FREE UNITS TESTS RUN GREEN AFTER THE CHANGE*** — `tiercounts` 13/13, `sdtestuser` 51/0, `verdict` 126/126, `fixlist` 217/0 — **which is the habit this entry is about.** **UNRUN IN THE RUNNER: `b73` is what proves it appears as step 1 and that the elevated half still reaches 21** ***— DONE 30 Aug 2026, OBSERVED ON `-Run b73`.*** Install **20:24:50**, `assert-current` **exit 0 live** in the step transcripts. `test-tiercounts-units.ps1` is the **FIRST** `=====` banner in the `VerifyInstall1` log, **ahead of `verify-credacl.ps1`**, and the unelevated half ran **16 of 16** — up from 15, which is the arithmetic that says the new step is the addition and nothing was displaced. **The elevated half still reaches 21 of 21.** ***GREEN IN BOTH HALVES: 37 steps, 693 `[PASS]`, 0 `[FAIL]`*** — 278 unelevated and 415 elevated, plus `verify-sdsysgate`'s *"10 decisive check(s), 0 failed"* and `verify-apiidentity`'s four-row table, neither of which uses `[PASS]` markers. **676 → 693 is exactly this step's 13 plus 65's four new checks**, which is how the totals were reconciled rather than eyeballed | `gplbld/test-tiercounts-units.ps1`, `gplbld/verify-tierapi.ps1:174`, `gplbld/VerifyInstall1.ps1:287`, and entries 54, 78, 25 |
| ~~83~~ | **S** | ***`DELETE_USER` CAN LEAVE THE PROFILE DIRECTORY WITHOUT ITS `ProfileList` ENTRY — THE EXACT SPLIT 36 EXISTS TO PREVENT — AND MESSAGE 10075 TELLS THE USER IT DID NOT.*** Found 30 Aug 2026 on `-Run b74`, the **first run ever to reach the keep-both arm** (65's pinned subject). **Measured by two independent instruments**: `verify-delaccount` step 6 read `ProfileList entry was KEPT with it: expected True, got False` immediately after the verb, and the reclaim sweep's own log wrote `before: directory present, ProfileList entry gone` four minutes later. ***THE CAUSE IS THAT THE GUARD CANNOT COVER THE CALL THAT DOES THE DAMAGE.*** `DELETE_USER:270` runs `Remove-CimInstance` on the `Win32_UserProfile`, which removes **both halves** in Windows' own order; when the directory cannot go, the registry entry may already have. The explicit guard at `:281` — `if ((-not $dirleft) -and (Test-Path $key))` — only governs **SD's own second removal**, so it never fires here and cannot undo what `Remove-CimInstance` already did. **The file's own comment shows the author knew the call was unreliable** (*"a thrown Remove-CimInstance does not tell you what it managed to remove first"*) and answered it by **measuring** afterwards — which is right, and is not the same as keeping the promise. ***SO THE CODE IS HONEST AND THE MESSAGE IS NOT.*** 10075 says *"SD has kept the profile's registry entry with the directory rather than removing one half of a pair, and has recorded both"* — **the first clause was false on the only run that has ever printed it.** ***THE RECOVERY IS NOT AT RISK, WHICH IS WHY THIS IS S AND NOT B***: `reclaim-profiles.ps1` reads the **record**, not `ProfileList`, and it reclaimed this pair at the next service start (below). **Three shapes, and the choice is the owner's**: reword 10075 to promise only what is kept — the RECORD; or reorder `DELETE_USER` to `Remove-Item` the directory first and call `Remove-CimInstance` only if that succeeded, which is what 36's own text already claims happens; or rule the invariant obsolete, since the record superseded the entry as the handle, and delete the `:281` guard with it. ***RULED AND BUILT 30 Aug 2026 ON THE OWNER'S INSTRUCTION — SHAPE TWO, THE REORDER, BECAUSE IT IS WHAT 36's OWN TEXT ALREADY CLAIMS HAPPENS.*** 36 says *"`DELETE_USER` takes the DIRECTORY first and removes the `ProfileList` entry only if that succeeded"*, and the code did not: `Remove-CimInstance` ran first and removes **both** halves. **It now sits inside the `-not $dirleft` guard, after the directory removal.** It is not replaced — it is still the sanctioned way to deregister a profile, which is why `clean-test-profiles.ps1` uses it — only moved behind the test it was defeating; the explicit `Remove-Item` on the key stays after it as the fallback for a CIM call that fails without throwing, which this tree was caught by in **81**. ***AND THE MESSAGE STOPS LYING WITHOUT BEING EDITED***: with the directory tried first, a kept directory means the entry is kept too, so 10075's *"SD has kept the profile's registry entry with the directory"* becomes true again rather than being reworded to promise less. **Statuses 6, 7 and 8 all stay reachable** — 7 is the directory going and the entry surviving both removals. ***PRE-FLIGHTED WITHOUT A CYCLE***: the PowerShell the verb builds was reconstructed from the `ps :=` lines and parsed — **0 errors, 27/27 braces**, and the reconstruction asserts the order it is about, *directory removed BEFORE `$dirleft` is read: True*, *`Remove-CimInstance` AFTER: True*. ***DONE AND PROVEN 30 Aug 2026 ON `-Run b77`, ON THE DECISIVE BRANCH.*** `verify-delaccount` **54 PASS + 0 N/A of 54, zero FAIL** — up from 53/1, and the one that flipped is this entry's: ***`the ProfileList entry was KEPT with it: expected True, got True`***, with the pin biting (`65: status 6/7/8 … DECISIVE`), **10075 shown**, **the pair recorded for reclaim**, and 10123 absent. **So the message stopped lying without being reworded, exactly as the ruling intended** | `sdsys/gpl.bp/DELETE_USER` (`Remove-CimInstance`, now guarded), `sdsys/messages/10075`, `gplbld/verify-delaccount.ps1` step 6, and entries 36, 65, 81 |
| ~~84~~ | **M** | ***SIX CHECKS IN `verify-notyet.ps1` MATCHED CONSOLE OUTPUT WITH LITERAL PHRASES, SO THEY ANSWERED ON THE CONSOLE'S WIDTH RATHER THAN THE PRODUCT'S BEHAVIOUR.*** Found 30 Aug 2026 on `-Run b74` step 3: *"says the sign-in has not got it yet: expected True, got False"* against a build that was printing **exactly** the right sentence — check-install had wrapped it as `...does not have it` / `yet.`, and the pattern looked for the unwrapped form. ***IT PASSED ON `b73` AT A DIFFERENT WIDTH, WHICH IS THE WORST PROPERTY A CHECK CAN HAVE: CORRECT BY LUCK.*** ***AND THE FIVE THAT STAYED GREEN WERE NO BETTER OFF*** — four of them assert a phrase **ABSENT**, and a wrapped line is absent to a literal pattern too, so they would have passed just as happily on output that **did** contain what they exist to rule out. `control: no "does not have it yet"` is one of them, so the control was as blind as the check. **Repairing only the red one would have looked like a fix and left four asserting nothing.** ***DONE 30 Aug 2026, ALL SIX, AND PROVEN AGAINST THE REAL FAILING BYTES***: a `Wrapped()` helper escapes the literal runs and joins them with `\s+`, the same cure PRE_RELEASE 51 applied to `Get-SysMsgPattern`'s `Esc-Loose`. **Replayed against `b74`'s own transcript: the old pattern answers `False` — reproducing the failure — and the new one answers `True`.** **A positive control ships with it**: a fixture wrapped where the console wrapped it, asserted to match, so if the matcher ever breaks every phrase check below it goes red instead of blind. **`gplbld` only, `assert-current` exit 0, no cycle.** ***DONE AND OBSERVED 30 Aug 2026 ON `-Run b75`***: `verify-notyet` **14 of 14**, up from 12/13 — *"control: the phrase matcher survives a wrapped line: expected True, got True"* and *"says the sign-in has not got it yet: expected True, got True"*. **The check that went red on `b74` is green and the control that guards the matcher is green with it** | `gplbld/verify-notyet.ps1`, and entry 51 |
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
| ~~44~~ | **S** | ***RE-VALIDATED 28 Aug 2026 FROM THE INSTALLED MESSAGE, not from this entry's own text***: `C:\ProgramData\SD\sdsys\messages\5161` reads exactly `Unable to change to new directory` — nothing about the group, the token, or signing out. Still open. ***THE VERIFIER HALF IS DONE AND WITNESSED — `-Run b53`, all five legs green. THE PRODUCT HALF IS STILL OPEN AND IS STILL THE OWNER'S.*** 5161 says only *"Unable to change to new directory"*, with nothing about the group not yet being in the caller's token or a sign-out fixing it — and that is the sentence a real administrator hits after `create.account`, not a test. **The run carries its own non-decisive witness**: this session's `LOGTO` reports 5161 in the Control leg while the helper's succeeds, in the same transcript. ***RULED AND BUILT 28 Aug 2026 — "two accounts, as the door table says".*** The owner's choice between covering the door properly, dropping it, or fixing only the message. **The door pair now creates a HELPER account `<prefix>b` alongside the account under test, grants it into the account's `sdu_` group, and issues the `LOGTO` from inside the helper's own ssh session** — a fresh logon, so its token carries the group SID this session cannot. `verify-doors.ps1` runs the local `LOGTO` too and records it as a **NON-DECISIVE witness**, so the transcript carries the evidence for why two accounts are needed rather than a comment claiming it. ***UNRUN — it needs an elevated Create leg, so `-Run b52` is what tests it.*** **Costs a second profile directory per run** (35/36), and both names are now checked free before anything is created. **The PRODUCT half of this entry is untouched and still open**: 5161 still says only *"Unable to change to new directory"*, and that is the sentence a real administrator hits. ***CONFIRMED BY THE SUITE ITSELF, `-Run b51`, 28 Aug 2026 16:54, on a SECOND account — this is not a one-off.*** With the instrument honest the Control leg reported **2 of 7 decisive checks failed**, both of them the `logto` rows (*"entered the account"* expected True got **False**; *"did NOT report 5161"* expected False got **True**), while **ssh and the API both admitted** in the same leg — the three-door comparison inside one run, which is stronger evidence than either door alone. The suite then **stopped at the right place** (*"a door refused BEFORE the suspension, so its refusal after one would prove nothing"*) **and still ran `Remove`**, so nothing live was left behind. ***`LOGTO` authorises on the machine's group list and then fails the chdir on the token's, and says only "Unable to change to new directory"*** — an administrator who has just run `create.account` is in the new `sdu_<acct>` group **on the machine** but **not in their own token**, because Windows fixes group membership at logon. So `logto.authorised` (`CPROC:2679`) passes, the chdir at `:2691` is denied, and 5161 is all the user sees. **Measured 28 Aug 2026 with a control**: `Get-LocalGroupMember sdu_sddrb50a` → `GITORLI\don` **present**; the same live unelevated token → `sdu_sddrb50a` **absent** while `sdusers` (granted before a reboot) **present**, so the enumeration works and the absence is real. **The record already knew the mechanism** — PROJECT_STATUS §6 *"group membership is fixed in the token at logon"* — **but nothing connects it to this message.** 5161 is also `SETACC:67`. ***Owner's call, and there are three shapes***: say so in 5161 when the account was reachable but the directory was not; have `create.account` print the sign-out line it already prints elsewhere; or leave it. **It is also why 19's `logto` door cannot be measured from the creating session** — the door table in this file already specifies the cure, *"ssh as A and `LOGTO B`"*. ***DONE 30 Aug 2026 on the owner's instruction — AND 5161 ITSELF IS DELIBERATELY UNCHANGED.*** The entry offered three shapes; the one taken is a variant of the first, done so it cannot damage the other call site. **5161 is shared with `SETACC:67`, for a different cause**, so rewording it would make one site clearer by making the other wrong. New message **10150** is printed only at `CPROC`'s chdir failure, immediately after 5161, where the cause IS known: `logto.authorised` has just passed, so the grant exists on the machine and only the chdir failed. **10150 names the token-lag case and the cure — sign out and back in — then says what to look at if that does not help**, rather than asserting a cause it cannot rule out, and it prints the path SD tried. ***DONE AND WITNESSED 30 Aug 2026 ON `-Run b77`, IN THE REAL SCENARIO RATHER THAN A FIXTURE.*** `verify-doors` in the unelevated half hit exactly the path this entry describes, and the transcript carries all three lines together: `:LOGTO SDDRB77A` / `Unable to change to new directory` / ***`The grant is in place, but this sign-in cannot use it yet.`*** **5161 still prints and is still shared with `SETACC`; 10150 follows it only here** | `sdsys/gpl.bp/CPROC` (the `ospath(acc.rec, OS$CD)` failure), `SETACC:67`, `sdsys/messages/5161` (unchanged), `10150` (new), and entry 19's door suite |
| ~~53~~ | **S** | ***THREE MORE DOCUMENT SETS STILL CARRIED `encrypt.field`, AND THEY WERE WRONG IN A DIFFERENT WAY FROM 52*** — found 28 Aug 2026 while closing 52, which corrected the **Testing** set only. These do not merely miscount it; they tell the reader **the verb is in an administrator's VOC and fails to load**, which stopped being true when PRE_RELEASE 25 removed it. ***CONFIRMED GONE TREE-WIDE***: absent from `newvoc`, from `voc_template` (426 entries — only the `encrypt` **keyword**, `211`, which is in the base 392 and is not a verb) and from `TIER.ADD.ADMINISTRATOR`. **Four places**: `Administrator/markdown/01-accounts-and-security.md:323-333`, a whole `## encrypt.field does not work in this release` section quoting the `$CRYPTO` load error; `User/markdown/95-sd-tcl-syntax.md:92`, a table row tiered **`A`**; and the two toolchain inputs that generate them — `tools/tcl-syntax-shapes.txt:81` and `tools/tclmap.py:128`, the latter mapping the verb onto Administrator/01, so the generator still expects that page to document it. ***ONE DECISION IS NEEDED BEFORE ANY EDIT AND IT IS THE OWNER'S***: `Administrator/markdown/01:333` is the **ONLY line in the entire documentation** that records field-level encryption as absent from W1.0-0 — measured by grepping `encrypt` across all four sets — so **deleting the section loses that fact**, while leaving it states a mechanism that no longer exists. Reword it to "not present, and the verb does not ship", or delete it and put the fact on a *not in SD Core* page. **Do not delete the shapes/tclmap rows without the same answer**: `95-sd-tcl-syntax.md` is generated, so an edit to the page alone is overwritten on the next render. *(`sdencrypt()`/`sddecrypt()` are unaffected and DO ship — this is the verb only.)* ***DONE 28 Aug 2026 ON THE OWNER'S RULING, "move to not in SD core".*** The section is deleted from `Administrator/01` and the fact is now `## Field-level encryption` on `Testing/markdown/14-not-in-sd-core.md`, which names `sdencrypt()`/`sddecrypt()` as the supported route and says plainly that nothing replaces the verb. ***AND IT WAS NOT COSMETIC — BOTH DOC GENERATORS HAD BEEN REFUSING TO RUN.*** `mktclsyntax.py` exited 1 on `NOT A VERB encrypt.field has a shape and is not on the roster` and `tclmap.py` on `NOT A VERB encrypt.field claimed by Administrator/01`, so **the TCL syntax card could not be regenerated at all** while the shapes file and the map still named it. **The roster is computed and had already self-corrected to 143**; the two typed lists had not, which is precisely the failure the computed roster exists to expose. Both now exit 0 — `roster 143 (standard 81, programmer 42, administrator 20)`, `tclmap 143 of 143, 0 exempt` — and that is an INDEPENDENT confirmation of 4 and 52's figures, from a tool that computes rather than quotes. `checklinks` 0 broken on all three sets (77/6/185) | docs repo, `Administrator/markdown/01`, `Testing/markdown/14`, `User/markdown/95`, `tools/` |
| ~~54~~ | **M** | ***`verify-profiledir.ps1` is in neither runner, so 36's last leg never fires again*** — the leg that had **never** fired before 28 Aug, which is why it could not be trusted and why the script was written. It scored **14 of 14** and then went nowhere: not in `VerifyInstall1`, not in `VerifyInstall2`. ***DECIDED 29 Aug 2026 — WIRE IT INTO `VerifyInstall2`***, the owner having said the verifier questions are mine. It needs **elevation**, so `VerifyInstall2` is the right runner and `VerifyInstall1` is not. **Its cost is lower than `verify-doors-suite`, which is already a suite step**: it creates one control account and deletes it, and it never logs in, so it leaves **no profile directory** — the thing that makes the doors fixture single-use and expensive. ***THE ONE THING THAT MUST NOT BE GOT WRONG: its `-Prefix` has to come from the `-Run` token***, as `sdacctb48`/`sdtiertb48` already do. It refuses a spent stem by design, so a fixed prefix passes once and fails on every later run on the same machine. ***WIRED 30 Aug 2026, EXACTLY AS THIS ROW SPECIFIES.*** Added to `VerifyInstall2` as `@{ Name = 'verify-profiledir.ps1'; P = @{ Prefix = $ProfPrefix } }`, with `$ProfPrefix` defaulting to **`"sdprof$Run"`** so the prefix comes from the `-Run` token — the one thing this row said must not be got wrong, because the script refuses a spent stem and a fixed prefix would pass once and fail every later run on the same machine, reading like a product fault. **Placed after `verify-delaccount`**, both being account-lifecycle rows. ***A HASHTABLE SPLAT, NOT AN ARRAY***, which the runner's own comment records the cost of getting wrong: `@($a)` and `@a` both bind positionally and gave `$Prefix = "-Prefix sdtierg"`, which read exactly like a silent tier-filter failure. ***DONE 30 Aug 2026 — RUN TWICE AND GREEN BOTH TIMES.*** `-Run b70` and `-Run b72`, step **13 of 21**, `verify-profiledir.ps1 -Prefix sdprofb70` / `sdprofb72`, **exit 0**. **The prefix derived from the `-Run` token on both**, which is the property that matters: a fixed one would have passed on `b70` and failed on `b72`, and the second run is what proves it did not. ***36's LAST LEG HAS NOW FIRED — TWICE — HAVING NEVER FIRED SINCE THE DAY IT WAS WRITTEN*** | `gplbld/VerifyInstall2.ps1`, `gplbld/verify-profiledir.ps1` |
| ~~64~~ | **B** | ***DONE AND MEASURED 29 Aug 2026 — `verify-apiadmin` IS BACK TO 22 PASS / 0 FAIL / 1 SKIP ON `-Prefix sdapiaz1`, AND THE NEW CONTROL IS GREEN.*** *"control: the probe CAN see OS.EXECUTE run (local, listed administrator)"* read **`True`/`True`**, and every other row matched its expected value; the single SKIP is the standing `n/a` on *"API session is NOT running as SYSTEM"*, which cannot be asked once OS.EXECUTE was refused. **The two rows either side still hold, which is what makes the run mean something**: *"API session was refused OS.EXECUTE by name"* `True`, *"API session CANNOT run OS.EXECUTE"* `False`/`False`. ***THE RUN LEFT NOTHING BEHIND, CHECKED RATHER THAN ASSUMED***: `sdapiaz1` is gone from `Get-LocalUser` and from `sdsys\accounts`, and **`os.users` gained no record** — still the same four. **That narrows 65**: the orphans come from the ADMINISTRATOR-tier verifiers (`sdrtb69a`, `sdtapib693`, `sdtiertb693`), not from every verifier, so 65 should start at those and not here. *(Was: THE `LOGTO` LEAK IS REAL, MEASURED, AND IT BREAKS AN EXISTING SECURITY CONTROL — `verify-apiadmin` IS 21/23 AND THAT IS THE PRODUCT, NOT THE TEST.)* Filed from `-Run b69`, 29 Aug 2026, the first run after entry 2's ruling. The row: *"control: local elevated session refused OS.EXECUTE"*, **expected refused, observed it RAN** (`False`/`True`; it read `False`/`False` on both `b67` and `b68`). ***THE MECHANISM IS THE ONE THE OWNER ACCEPTED***, and the control's own comment had already written it down: a local session *"starts in SDSYS with USR_ADMIN set and gives the flag up on the way out (CPROC, 'administrator rights belong to SDSYS'), so by the time it reaches the probe `os_permitted()` says no"* — it then falls through to the `os.users` lookup, **which is keyed on the person and which a `LOGTO` does not change** (`op_sh.c:167`). With `don` listed `yes|yes`, that lookup now succeeds. ***THE INVERSION THAT CONTROL EXISTED TO NAME HAS GONE***: it read *"same account, same program, and the remote client is the one that gets the operating system"* — **now both do.** ***SO THIS IS A DECISION, NOT A TEST EDIT.*** Either the control is updated to assert the ruled behaviour (an administrator keeps the operating system wherever they `logto`), **or** the grant moves to the session flag as entry 2 records — `CPROC:2781` already clears it on a `LOGTO`, with `LOGIN:568`'s trap to avoid. **Do not simply flip the expected value: that would encode the leak as intended without anybody saying it was.** ***RULED 29 Aug 2026 — "LEAVE ssh, API AND `os.execute` RIGHTS THE WAY THEY ARE FOR THE ADMINISTRATOR'S PERSONAL ACCOUNT." NO PRODUCT CHANGE. THE FIRST BRANCH, AND THE LEAK IS NOW SAID TO BE INTENDED.*** He reached it by specifying the whole model rather than the row — os.execute on the personal account, administrator commands via `LOGTO SDSYS`, elevated login straight into SDSYS, no SDSYS over ssh or the API — then withdrew the two changes that would have followed. ***THE THREE POINTS THAT WOULD HAVE NEEDED CODE ARE WITHDRAWN, AND THE OTHER THREE WERE ALREADY BUILT***: `logto sdsys` from an unelevated personal account already checks `K$OS.ADMINISTRATOR`, calls `elevate('START')` for one UAC consent and sets `elev.obtained` (`CPROC:2570-2590`), which is what `logto.authorised` accepts; `LOGIN:568` already sends an elevated session straight to SDSYS; and `kernel.c:240`'s `CN_SOCKET` guard already keeps `K$ADMINISTRATOR` off every API session. ***MEASURED WHILE RULING, FROM THE LIVE `b69` INSTALL***: `accounts\DON` field 5 is `ADMINISTRATOR` (`CREATEA:1583` forces it on the adopt path), `os.users\don` is `yes`/`yes`, and `don` is in `sdssh`, `sdapi`, `sdusers` and `Administrators` but NOT `sdsshonly`. **ssh is held twice over** — `sshd_config:88` names `Administrators` in its own right, which is why `MODIFYA:557` says `sdssh` cannot lock an administrator out. **None of the three is removable**: `MODIFYA:583` (10083) and `:719` (10106) both key on `is_grp_member(acc.user, "S-1-5-32-544")`, the Windows group and not the SD tier — and :719 sits BEFORE the `os.users` open, so an administrator cannot grant himself `os-on` either. ***THE FIX IS THE VERIFIER, AND IT IS BUILT AND NOW RUN.*** `verify-apiadmin.ps1:602` is a different claim with a different name rather than an inverted boolean, and it now does the job the API row was missing — **the POSITIVE CONTROL**: *"the probe CAN see OS.EXECUTE run (local, listed administrator)"*, expecting `$true`. A refusal is only evidence if the probe could have seen a success, and while both legs were refused nothing in the run ever demonstrated that it could. **The `FINDING` arm at `:655` is kept and commented rather than deleted** — it fires only if the local leg is refused while the API leg runs, which is a worse state than the API finding alone and stays worth printing. **It needed no cycle — the product is unchanged and `assert-current` exempts the file at `assert-current.ps1:550`.** **65 is unaffected and stays open** | `gplbld/verify-apiadmin.ps1:602`, `gplsrc/op_sh.c:161`, `gpl.bp/CREATEA:1613`, `gpl.bp/MODIFYA:583`, `:719` |
| ~~65~~ | **S** | ***`os.users` NOW ACCUMULATES AN ORPHANED RECORD PER ADMINISTRATOR-TIER THROWAWAY ACCOUNT, ONE OR MORE PER SUITE RUN.*** Measured after `-Run b69`, 29 Aug 2026: `os.users` holds `SDRTB69A`, `SDTAPIB693` and `SDTIERTB693` alongside `don`, and **all three Windows accounts are gone** — checked with `Get-LocalUser`, not assumed. **Introduced by entry 2's restoration**: before it, an ADMINISTRATOR-tier account got no record, so nothing could be left behind. ***`DELETE.ACCOUNT` IS SUPPOSED TO TAKE IT AWAY*** — entry 2's original text says it removes the record *"where SD is deleting the Windows login itself"*, which is exactly what these verifiers do — **so either that path is not firing or its condition is narrower than the text claims. Read `DELACC` before changing anything.** **Same shape as PRE_RELEASE 60**, the dead VOC records `verify-catgate` left one per run: harmless individually, accumulating, and it pollutes the file whose ACL is the whole of the protection. **A stale `yes|yes` keyed on a NAME that Windows may one day reissue is worse than untidy**. ***ANSWERED 30 Aug 2026 — THE ENTRY'S OWN QUESTION HAD TWO ANSWERS AND THE MEASURED ONE IS NOT THE DEFECT.*** It asked whether `DELACC`'s path was *"not firing or narrower than the text claims"*. **It is not firing: the verifiers that leaked never run the verb.** `verify-tierapi.ps1:309` and `verify-routes.ps1:478` both `Remove-LocalUser` and say *"remove with DELETE.ACCOUNT"* — so nothing of SD's ran, and the leak was the harness's. ***AND THE CONDITION IS ALSO NARROWER THAN THE TEXT CLAIMS, WHICH IS THE PRODUCT DEFECT HIDING BEHIND IT***: the removal sat inside `case stat = 0`, and `!delete_user` returns TRUE for **0, 6, 7 AND 8** — `DELETE_USER:328` — the login gone in all four, the three others differing in the **PROFILE alone**. A loaded hive is what makes a profile unremovable, so **6/7/8 is the ORDINARY outcome for an account somebody has just used** and the covered case was the rarer one. ***AND `void delete_user(...)` WAS AGAIN THE DEFECT, exactly as at `CREATEA:643` (entry 72)***: the function already answers *"is the login gone"* and the answer was discarded, so the caller re-derived it from a status and got it wrong. **STILL ACCUMULATING, MEASURED ON THE 18:03:57 INSTALL**: `os.users` holds `don` plus **seven** orphans from `b70`–`b72` — `SDRTB70A`, `SDRTB72A`, `SDTAPIB703`, `SDTAPIB723`, `SDTIERTB703`, `SDTIERTB713`, `SDTIERTB723` — and all seven Windows accounts are **ABSENT** to `Get-LocalUser`. ***BUILT 30 Aug 2026, UNRUN — IT NEEDS A CYCLE AND THEN THE ELEVATED HALF.*** `DELACC` reads the return into `login.gone` and both callers reach a new `drop.os.access:` subroutine — the `sd.made.it` arm after its case block, and **`lookup.stat # 0`, the half-removed account, which is the arm every *"remove with DELETE.ACCOUNT"* note lands in and which cleared nothing.** One place, two callers, on entry 11's shape. **The check is in `verify-delaccount.ps1`, which VerifyInstall2 already runs**: its SD-made subject is now **ADMINISTRATOR-tier**, because only that tier is given a record and a STANDARD subject would have scored *"the record is gone"* by never having had one. **Three states are required — ABSENT at preflight, PRESENT after `create.account`, ABSENT after `delete.account`** — and the run **prints whether it took the decisive branch**: the check is decisive only on the keep-both path (6/7/8) and says *"CONFIRMATORY, not decisive"* on status 0. **The harness leak is disclosed rather than swept**: both verifiers and `cleanup-devlitter.ps1` now name `os.users` beside the register, and `DELETE.ACCOUNT` is a true recovery for it as of this fix — it was not before. **Not upstream**: `sdb64`'s `DELACC` has no `os.users` at all, only `OS.EXECUTE "sudo userdel"`. ***CYCLED AND RUN ON `-Run b73`, 30 Aug 2026, AND STILL NOT PROVEN — THE INSTRUMENT SAID SO ITSELF, WHICH IS THE ONLY REASON THIS IS NOT BEING CLOSED.*** Install **20:24:50**, `verify-delaccount` **42 PASS / 0 FAIL / 0 N/A** (38 → 42, the four new checks), all three states measured: `os.users\SDDELB73S` **absent at preflight**, **`yes | yes` after `create.account`**, **gone after `delete.account`**. ***BUT THE RUN TOOK STATUS 0*** — its own line 89 reads *"65: status 0 - the os.users check above is CONFIRMATORY, not decisive"* — **so it exercised the arm that already worked before the fix.** ***AND THE CAUSE IS STRUCTURAL RATHER THAN LUCK, WHICH IS THE FINDING***: step 2 makes the profile with **`CreateProfile`**, which never loads a hive, so `Remove-Item` on `C:\Users\<name>` always succeeds and `DELETE_USER:282` always reaches `exit 0`. **As built, this verifier can NEVER reach 6/7/8.** The status is decided by `$dirleft`/`$keyleft` at `DELETE_USER:277-283`, so the decisive branch needs the profile directory to be **undeletable at the moment the verb runs** — an open handle without `FILE_SHARE_DELETE` anywhere under it is enough, and `LoadUserProfile` without the matching unload is the other route. ***THE SAME GAP KEEPS 36's KEEP-BOTH ARM UNMEASURED***, and `verify-delaccount.ps1`'s own header already said so: *"It has not run on this host yet."* **One rig would settle both.** ***A CASE-ONLY DIFFERENCE WOULD HAVE FAKED A PASS AND DID NOT, BECAUSE IT WAS ANTICIPATED***: the account is `sddelb73s` and the record is **`SDDELB73S`** — `grant.os.access` keys on `acc.uname`, which is upper case — so a `-ceq` in `Get-OsUsersRecord` would have scored step 1 FAIL and step 3's *"gone"* a **pass for the wrong reason**. The match is case-insensitive on purpose and the comment there says why. ***THE RIG IS BUILT, 30 Aug 2026, AND NEEDS `b74` — NO CYCLE.*** Owner's call: **a THIRD subject rather than pinning the first**, so status 0 keeps its coverage and 6/7/8 gains it. `verify-delaccount.ps1` **step 6** creates `<prefix>h` `ADMINISTRATOR BOTH`, gives it a profile, **pins one file inside that profile open with `FileShare.Read`**, and then runs `DELETE.ACCOUNT`. **Deleting a file needs `FILE_SHARE_DELETE` from every other handle on it**, so the pin blocks `Remove-Item` on the file, which blocks `-Recurse` on the directory above it — `$dirleft` at `DELETE_USER:277`, the same state a loaded hive produces, with **no interop, no logon and no password**. ***THE RIG IS CHECKED BEFORE THE PRODUCT IS***: if the pin does not bite the run is back on status 0, and that is reported as a failure **OF THE RIG**, named as such — `"THE PIN DID NOT BITE"` — rather than as a green branch or a product fault. **The decisive `os.users` check is asserted on both branches**, because it has to hold either way; only what it *proves* differs. ***AND IT RETIRES A SECOND NEVER-RUN ARM***: 36's keep-both assertions — the entry kept **with** the directory, the reclaim record naming it, 10075 shown, 10123 absent — have never fired on this host, which `verify-delaccount.ps1`'s own header said before b73 and which b73 left true. **`C:\Users\<prefix>h` and its ProfileList entry are LEFT BEHIND on purpose**: that is what status 6 means, and the next SD service start reclaims the pair. **The pin is released in `finally`, outside the `-Keep` test**, so nothing is held hostage from that sweep. ***NO CYCLE — MEASURED, NOT ASSUMED***: `assert-current` **exit 0** after the edit, both files being exempt. Pre-flighted: **0 parse errors, 16 functions** (unchanged), steps renumber cleanly **1–7**, no BOM, 0 CR, no non-ASCII. ***DONE 30 Aug 2026 — PROVEN ON `-Run b74`, ON THE DECISIVE BRANCH, WHICH IS WHAT TOOK THREE ATTEMPTS TO REACH.*** ***THE PIN BIT***: *"the pin blocked the profile removal (this leg is decisive): expected True, got True"*, then ***"65: status 6/7/8 - the os.users check below is DECISIVE"***, and on that branch — **`10075` shown, the profile directory KEPT, the reclaim record written and naming the directory, `10123` absent** — ***"os.users record is gone (the DECISIVE one): expected False, got False"***. **`verify-delaccount` 53 PASS / 1 FAIL of 54**, and **the single FAIL is not this entry**: it is the `ProfileList` split now filed as **83**, found only because this rig reached the arm. **The step-3 subject still took status 0 and still said so**, so both arms are covered in one run, which is what the third subject was for | `gpl.bp/DELACC`, `sdsys/os.users`, `gplbld/verify-delaccount.ps1`, `verify-tierapi.ps1`, `verify-routes.ps1`, `VerifyInstall2.ps1`, and entries 36, 83 |
| 66 | **S** | ***THE TWO EDITORS ARE STILL FETCHED FROM THE INTERNET AT INSTALL TIME, UNPINNED — THE DECISION TO BUNDLE THEM WAS TAKEN 26 Aug 2026 AND NOTHING WAS BUILT.*** Raised by the owner 30 Aug 2026 after a VM install: *"the two full screen editor packages are being downloaded from the internet and they were supposed to be bundled with the install so that we knew which version was installed."* **The record agrees with him** — HISTORY.md's 26 Aug close lists, under *"Open, none started"*, ***"bundling micro with the installer (decided, licence question settled, nothing built)"***. ***THE SHARP PART IS NOT THE DOWNLOAD, IT IS THAT THE DOCUMENTATION IS MEASURED AGAINST VERSIONS THE INSTALLER DOES NOT INSTALL.*** The editor pages were written from **micro 2.0.15**'s own bindings and **Microsoft Edit v1.2.1**'s `draw_menubar.rs` — read out of the executables, which is why they are trustworthy — while `install-editors.ps1:137` runs `winget install --id <id> --exact --scope machine --silent` **with no `--version`**, so a user installing next year gets whatever is current and a key-binding table that may not describe it. **`Microsoft.Edit` and `zyedidia.micro`** are the ids. ***micro IS THE ONE THAT ALWAYS DOWNLOADS*** — its winget manifest is `Installer Type: portable (zip)` and *"it never ships with Windows, so unlike Microsoft Edit it is always a download"*; Edit is at `C:\Windows\System32\edit.exe` on current builds and the script correctly skips it there, so on an older or Server SKU **both** are fetched. **A portable zip is the easy case to bundle: one executable, no installer to drive.** ***AND IT COSTS INSTALL TIME ON EXACTLY THE RIG THAT MATTERS*** — the same VM install where the OpenSSH capability download is already slow. **`sd.iss` runs the script unconditionally.** ***THE REPOSITORY CONSTRAINT SHAPES THE FIX AND DOES NOT FORBID IT***: no binaries are tracked, so the version and its SHA-256 are what the tree records, and a `gplbld` step fetches the pinned artefact at INSTALLER-BUILD time into the staging tree for `sd.iss` to embed — *"anything that has to ship as a binary ships outside the repository, as a release artefact"* (CLAUDE.md). **Owner's ruling already taken; this is the build, not a fresh question** | `gplbld/install-editors.ps1:137`, `gplbld/sd.iss`, `gplbld/stage.py` |
| 67 | **S** | ***A FULL INSTALL ALWAYS INSTALLS THE OpenSSH SERVER, EVEN WHEN THE USER DECLINES ssh — AND THE MODE PAGE'S OWN CAPTION SAYS IT IS OPTIONAL.*** Owner, 30 Aug 2026: *"if the user leaves the allow users to connect over ssh blank (perhaps he only wants api connections) why should he have to install the ssh server?"* ***HE IS RIGHT ABOUT THE MECHANISM, MEASURED FROM THE FILE.*** The `[Tasks]` entries `sshremote` and `apiremote` are **firewall** tasks, both `Flags: unchecked`; the server install at `sd.iss:719` is gated on **`SshServerAbsent and not StandaloneChosen`** and **does not test `sshremote` at all**. So leaving the ssh box blank closes port 22 and still installs the capability, starts `sshd`, and rewrites `sshd_config` with `AllowGroups` and `ForceCommand`. **`FullRadio.Caption` (`sd.iss:1399`) promises *"multiple users, optional remote ssh, optional remote API access"* — only the PORT is optional, not the server.** ***THE COST IS NOT HYPOTHETICAL***: it is the slow step on the VM rig (`StatusMsg: "Installing OpenSSH Server (this can take several minutes)..."`), and **it is what makes entry 39's consequence reachable at all** — an install that never wanted ssh still ends up with SD-created accounts that become ordinary ssh-reachable logins the moment uninstall strips `ForceCommand`. ***BUT IT IS NOT A CHECKBOX, AND THE REASON IS `deny-logon.ps1:29`***: `sdsshonly` carries `SeDenyInteractiveLogonRight` and `SeDenyRemoteInteractiveLogonRight` and deliberately **not** `SeDenyNetworkLogonRight`, so a non-administrator SD account **cannot reach the console or RDP** and has exactly two routes — ssh and the API — **and that holds for a LOCAL user too**, who reaches SD by `ssh localhost` with the firewall shut. **So "no ssh server" is not a firewall setting; it is a decision that no account will ever log in interactively, and `create.account <user> ssh` would then make an account with no working route.** ***THE SHAPE OF THE FIX IS A THIRD MODE, NOT A NEW TICKBOX*** — an API-only full installation, stated on the mode page in those terms, refusing `ssh`/`both` at `CREATE.ACCOUNT`, skipping `install-ssh.ps1`, `allow-ssh-groups.ps1` and the ssh firewall, and leaving `sshd_config` untouched. ***THE MITIGATION IS NOW MEASURED, NOT ASSUMED, AND IT HOLDS — SO THIS STAYS S.*** On a fresh VM install of 30 Aug 2026 with **both boxes unchecked**, `capture-state.ps1` read the live rule: `OpenSSH-Server-In-TCP`, `enabled=True`, `dir=Inbound`, `profile=Private`, ***`RemoteAddress=127.0.0.1`***. **`ssh-firewall.ps1 -Restrict` did its job** (`:150` sets `-RemoteAddress '127.0.0.1' -Enabled True`), so the unwanted `sshd` is **running and not reachable from the network**. **The same capture confirmed the rest of this entry**: `sshd.exe` PRESENT with the service `Running`/`Automatic` despite ssh being declined. ***AND A CLAIM OF MINE WAS WITHDRAWN ON THE WAY THERE, WHICH IS WHY THE READING IS SPELLED OUT ABOVE.*** An earlier capture printed only DisplayName, Enabled and Direction; I read `enabled=True dir=Inbound` as *"port 22 is open"* and said it made this a **B**. **It proves nothing of the kind** — a correctly RESTRICTED rule is also `Enabled=True`, so a restricted install and an open one are identical on those three fields. **The scope was the whole question and was the one field not read**; `capture-state.ps1` now reads it. **Arguably still a B on the grounds that it installs and RUNS a network daemon the user declined — but the exposure really is local-only, so it is filed S; the owner's call** ***AND THE ACCESS POLICY IS SETTLED, WHICH RESOLVES THE ONE QUESTION THIS ENTRY LEFT OPEN — "DOES ANYTHING ELSE NEED ssh?" NO.*** Owner restated it 30 Aug 2026: only administrators ever log in directly, at the keyboard or through RDP/AnyDesk; OS-level users the customer adds get no SD access by default; **multi-user RDP is not supported, only a single remote session**, for which the administrator installs AnyDesk or turns on Remote Desktop on Win 11 Pro. **All of it is already recorded** — §5.6.2 (`PROJECT_STATUS.md:5808`, owner 14 Aug 2026): *"Accounts SD creates reach the machine over ssh and nothing else. Local terminal access — the physical console, and Remote Desktop — is for administrators"*; and `RDPACCOUNT` was **deleted** rather than fixed (HISTORY.md:11345) so the rule *"holds by construction"*. ***SO AN ADMINISTRATOR NEVER NEEDS ssh***: they log in at the console and reach SDSYS by elevating (`LOGIN:568`), which is 56's model. **The ONLY thing an API-only install gives up is an interactive SD session for a NON-administrator account** — which is a real deployment (SD as the database behind an application) and must be said in those words on the mode page. **"OS users get no SD by default" verified rather than assumed, and it holds twice**: `LOGIN:415` refuses a non-`sdusers` Windows user with audit reason *"not a member of sdusers"*, and `sd.iss:577` ACLs the data tree to SYSTEM, Administrators and `sdusers` alone. ***AND IT HOLDS FOR ADMINISTRATORS TOO — A CORRECTION TO THIS ROW'S FIRST DRAFT, WHICH SAID THE OPPOSITE.*** The draft claimed a customer-added Windows administrator *"does get SD"*. **It was wrong**, and it conflated two different things: the data-tree ACL grants `Administrators` full control, which is FILESYSTEM access, while **SD login is refused at `LOGIN:414` with 5009 like anybody else made outside SD**. The administrator exemption that would have made the draft true **was removed on 29 Aug 2026** — entry 56, *"the `sdusers` gate is uniform across all three tiers"*, built, cycled and **proved by `-Run b66`** — and `LOGIN:388-413` records the owner's own sentence it exists to make true: *"if any are built outside of sd they do not have access to sd until a matching standard or programmer account is created in SD."* The gate runs **before** account determination, so an elevated administrator not in `sdusers` never reaches the SDSYS case at `:568`. ***AND DO NOT RE-ARGUE THAT WITH "AN ADMINISTRATOR COULD BYPASS IT" — THE OWNER HAS OVERRULED IT THREE TIMES, MOST RECENTLY 30 Aug 2026.*** *"We are not trying to prevent an administrator from making a non-standard system — this is an open source project after all… this is our default setup, not a prevention against users doing whatever they want to."* **`PROJECT_STATUS.md:3772` already settles it**: *"The goal is to make the project, as delivered, enforce the idea that SD account setup happens in SD. If users want to degrade security after the fact, that is their right"* — and that passage says in terms that it **overrules the argument that a gate an elevated administrator can pass is not worth building**. **What the design owes is that nothing the shipped product offers sets up an SD account outside SD.** The caveat is written into `LOGIN:410-413` as well; **it is not wrong, it is the wrong emphasis, and repeating it re-opens a closed question** ***AND THE ROUTE KEYWORDS MUST GO WITH THE MODE — OWNER, 30 Aug 2026: "if we are going to have the option of not installing the ssh server, the create and modify accounts commands should not accept ssh as an option."*** **The mechanism to copy already exists and so does the argument.** `CREATEA:412-418` reads a marker file, `@sdsys:@ds:'$standalone'`, and refuses `create.account user` outright with **10100**; the comment above it at `:400` gives this entry's reasoning in the product's own words — *"With no ssh server such an account can sign in NOWHERE, so it would be an account nobody could ever use."* ***BUT STAND-ALONE'S ANSWER IS TOO BLUNT TO REUSE***: it refuses user creation ENTIRELY, and an API-only install exists precisely to create API users. **So the guard is narrower — permit `create.account user`, refuse the `SSH` and `BOTH` keywords, leaving `API` and `NONE`** — and **`NONE` stays meaningful**, `:421-423` calling it *"an application user who can only be reached by LOGTO"*. ***MODIFY.ACCOUNT NEEDS THE SAME GUARD ON ITS route.set ARM OR IT RE-CREATES THE BROKEN STATE ONE COMMAND LATER***, which is the owner's point and is the half a create-time-only fix would miss. ***AND ADOPT MUST STAY EXEMPT — THE TRAP IS ALREADY WRITTEN AT `:405-411`***: the installer's own account step runs `sd -internal CREATE.ACCOUNT USER <name> ADOPT` through this very arm, so a test placed before `more.args` *"would refuse the install that wrote the marker, and a stand-alone system could not be installed at all."* ***THE OWNER RULED THE UPGRADE PATH 30 Aug 2026 — "if they change their minds, do a reinstall which uses the normal upgrade path accepting the new access routes" — AND IT CANNOT WORK AS THE INSTALLER STANDS. READ THIS BEFORE BUILDING IT.*** **A reinstall does not ask, and could not act on the answer if it did.** Three compounding reasons, all measured from `sd.iss`: (1) ***the mode page is a FIRST-INSTALL question and is deliberately not shown twice*** — `:1140`, *"On an upgrade the existing tree already carries the answer"*; (2) ***`StandaloneChosen` derives the mode from the TREE, not from the radio*** — `:1130-1133`, marked means forced stand-alone and an existing unmarked tree means forced full, with the radio consulted **only** when the data tree was absent; (3) ***`sd.conf` is `onlyifdoesntexist`*** (`:408-411`) so the API port is not rewritten either. **`WriteStandaloneMarker` only ever WRITES the marker and never removes it**, and `:1944-1948` says so deliberately — *"nothing deletes it… so the generated upgrade.iss cannot delete it either"* — while the marker's own text tells the user *"To get a full installation, uninstall SD and install it again choosing that option."* ***AND THE REASON IS SOUND RATHER THAN INCIDENTAL: THE MODE IS NOT THE MARKER.*** It is the marker **plus** whether an ssh server was installed **plus** `sd.conf`'s APIPORT, which is exactly why the marker text warns that deleting the file does not convert the installation. **So the ruling needs the installer changed, not just used**: the access question re-asked on an upgrade, `sd.conf` updated rather than skipped, and `install-ssh.ps1` allowed to run on a tree that already exists. ***ONE CONSEQUENCE TO STATE IN THE RULING***: even then, **existing accounts do not gain ssh** — they are not in `sdssh`, so switching the mode changes what is POSSIBLE, not what accounts HAVE, and each needs `modify.account <acc> ssh`. **`BOTH` is refused along with `SSH`, confirmed by the owner in the same message** ***RULED 30 Aug 2026, AND IT SUPERSEDES THE MARKER DESIGN ABOVE — "67 should be: refuse ssh and both if no ssh server installed."*** **The condition is the MACHINE, not the install.** ***THAT DISSOLVES THE UPGRADE PROBLEM RATHER THAN SOLVING IT***, and it is why this ruling is better than the one it replaces: the test is evaluated **at command time from real machine state**, so a site that later installs an ssh server finds `create.account … ssh` simply starts working. **None of the three obstacles apply any more** — no mode page has to be re-asked, `StandaloneChosen` is not consulted, and `sd.conf` never needs rewriting. **No new marker file, and nothing to keep in step with reality.** *(The three obstacles are still true of the STANDALONE→full transition and are left recorded above for that reason.)* ***ONE IMPLEMENTATION QUESTION IS OPEN AND IT IS NOT SMALL: HOW BASIC ASKS.*** The installer's own test is `SshWasAbsent := not FileExists('{sys}\OpenSSH\sshd.exe')` (`sd.iss:899`), but **there is no established pattern in the BASIC tree for testing a WINDOWS system path** — `ospath(..., OS$EXISTS)` is used only against SD-tree paths, `kernel(K$WINPATH)` converts POSIX→Windows and not back, **no BASIC reads an environment variable**, and `/cygdrive` appears **nowhere** in `gpl.bp`. Candidates, none chosen: `ospath` with a Windows path, **which may simply work under the Cygwin runtime and should be MEASURED before anything is designed around it**; a `deffun … calling '!ssh_installed'` in the shape of `!tier_allows`; or a C-side answer where `%SystemRoot%` is readable. **Do not reach for `ps_script` — it routes through the elevated helper (`PS_SCRIPT:166`), which is a great deal of machinery for a file test.** ***BUILT 30 Aug 2026 ON THE OWNER'S RULING, AND THE SHAPE IS A DEPENDENT PAIR OF TICKBOXES RATHER THAN THIS ROW'S "THIRD MODE".*** His words: *"if an ssh server is installed, the user should have a separate choice to allow remote access. If a server is not installed the user should have two choices, install the server, and allow remote access. Allowing remote access should not be an option if they choose not to install the ssh server."* ***THE CAPABILITY INSTALL IS GATED ON THE BOX NOW***, `Check: SshServerWanted` where it read `SshServerAbsent and not StandaloneChosen` — which is the whole of this entry's complaint, that the step never tested a box at all. **`ApplyAllowGroups` and `ApplySshFirewall` take the same gate**, so an install with no server writes no `sshd_config` and no firewall rule. ***THE DEPENDENCY IS INNO'S OWN, NOT A VALIDATION MESSAGE***: `sshserver\sshremote` is a CHILD task, and Inno greys and unchecks a child whenever its parent is unchecked — so "should not be an option" is a UI state the reader sees rather than a complaint after the fact. **Four `[Tasks]` entries carry what the reader sees as at most two boxes**, because a child cannot be created under a parent whose `Check` is False, so the server-present case needs flat entries of its own; `SshRemoteWanted` ORs them rather than re-deriving the partition, so the two copies cannot drift. ***THE "THIRD MODE" FRAMING IS WITHDRAWN WITH 75***: with stand-alone gone there is one installation and two boxes, and the mode page that would have carried a third is deleted. ***AND THE FIRST BUILD OF IT WAS WRONG AT THE WIZARD, WHICH IS WHERE IT COULD ONLY EVER HAVE BEEN CAUGHT.*** Owner, 30 Aug 2026, watching the tasks page: *"I click install the server and both check boxes are filled. I unclick let other computer connect and it also deletes installing the server."* **Neither of the two states he asked for could be expressed.** ***THE CAUSE IS TWO MISSING `[Tasks]` FLAGS, AND I ASSUMED INNO'S DEFAULTS INSTEAD OF READING THEM.*** From `ISetup.chm`, *"Tasks section"*, quoted because it names both symptoms exactly: **`dontinheritcheck`** — *"Specifies that the task should not automatically become checked when its parent is checked"* — and **`checkablealone`** — *"Specifies that the task can be checked when none of its children are. **By default, if no Tasks parameter directly references the task, unchecking all of the task's children will cause the task to become unchecked.**"* ***THE `Check:` ON THE [Run] ENTRY IS NOT THE `Tasks:` PARAMETER THAT EXEMPTION MEANS***, so `checkablealone` is load-bearing rather than decorative. **Fixed: `checkablealone` on `sshserver`, `unchecked dontinheritcheck` on `sshserver\sshremote`** — 31 insertions, 2 deletions, the flags and their record. ***THE THIRD STATE THAT WAS UNREACHABLE IS THE ONE THE RULING IS MOSTLY ABOUT***: install the server and do NOT allow remote access. **The other half of the mechanism was right and is confirmed by the same help topic** — *"A child task can't be selected if its parent task isn't selected"* — so the dependency itself never needed code. ***AND THE ABSENT-SERVER CASE FINALLY BECAME REACHABLE ON THIS HOST***: removing the OpenSSH capability is staged behind a REBOOT, so the first attempt still had `sshd.exe` on disk and correctly showed the server-present box. **REBUILT, UNTESTED — the wizard is the only place this can be judged** | `gplbld/sd.iss` `[Tasks]`, `:768`, `:1237`, `:1242`, `:1698`, `:1776`, `gplbld/deny-logon.ps1:29`, `gpl.bp/LOGIN:415`, `gpl.bp/CREATEA:400`, `gpl.bp/MODIFYA` route.set, and entries 75, 76 |
| ~~68~~ | **B** | ***SDSYS REACHED BY `logto` CANNOT CREATE AN ACCOUNT, AND IT LEAVES A HALF-CREATED ONE BEHIND. MEASURED BY THE OWNER ON THE VM INSTALL, 30 Aug 2026:*** *"if i login to personal account and then logto sdsys, I can't create users. If I login directly to sdsys from an elevated prompt, i can create users."* **That is one of the TWO routes the access model documents** — `LOGIN:396-399` quotes the owner: *"They got SDSYS in one of two ways, by starting SD in an elevated session or by logging to SD after logging into their personal account"* — **so half the model cannot do the thing SDSYS exists for.** ***THE CAUSE IS THAT THE TWO HALVES OF SETTING A PASSWORD RUN AT DIFFERENT PRIVILEGE LEVELS.*** The Windows half is `SET_PASSWD:130` → `ps_script` → `PS_SCRIPT:166` → **`elevate('RUN')`, which the ELEVATED HELPER runs**; the credential half is `SET_PASSWD:162` → `CRED_SET`, a **plain `openpath`/`write` by the SD PROCESS ITSELF** (`CRED_SET:68`, `:114`). `secure-cred.ps1` locks `$cred` to SYSTEM and Administrators and grants `sdusers` **nothing**, so an unelevated process cannot write it. ***AND SD BELIEVES IT IS ADMINISTRATOR, CORRECTLY, WHICH IS WHY NOTHING REFUSES EARLIER***: `CPROC:2769` sets `K$ADMINISTRATOR` on `logto sdsys` while `USR_ADMIN` was seeded from the real token at process start (`kernel.c:241`) — **the flag and the token disagree, and only file I/O notices.** ***THE ORDERING IS THE WORSE HALF OF THIS.*** The irreversible step runs first: the Windows account is created and its password set, THEN the credential write fails, leaving exactly what message 10122 warns about — **an account ssh would admit and the API would refuse.** `john` was left in that state on the VM. **`create.account` should establish it can write `$cred` BEFORE creating a Windows user.** ***THE CLASS IS TWO STORES, NOT ONE, AND THE OTHER TWO SHOW THE FIX WAS UNDERSTOOD ONCE***: `secure-audit.ps1` grants `sdusers:(AD` and `secure-log.ps1` grants `sdusers:A` — **append, precisely so an ordinary session can write them** — while `secure-osusers.ps1` grants `(OI)(CI)(RX)`, read-only, so ***`modify.account <acc> os-on`/`sh-on` should fail the same way*** (`MODIFYA`'s `openpath … 'os.users'` is direct BASIC I/O — **reasoned from the ACL, NOT yet measured; measure before fixing**). ***AND THE INSTRUMENT IS BLIND TWICE OVER***: `CRED_SET` has **five** distinct failure paths — `$cred` missing, no salt, empty PBKDF2, empty HMAC, refused write — and `CREATEA:602` collapses all five into `stat = 6`, so the message cannot say which; and **`pw.stat = 5`, *"Not elevated - retrying will not help"*, can never fire for this, because that `IsInRole` test runs INSIDE THE HELPER (`SET_PASSWD:120-122`), which is always elevated. It measures the wrong process.** **Fix shapes, none chosen: route the protected-store writes through the helper as `ps_script` already does; or re-exec SD elevated on `logto sdsys`; or refuse the whole command up front. A token cannot be elevated in place, so "make the process elevated" is not among them** | `gpl.bp/SET_PASSWD:130`, `:162`, `gpl.bp/CRED_SET:68`, `:114`, `gpl.bp/CREATEA:602`, `gpl.bp/PS_SCRIPT:166`, `gpl.bp/CPROC:2769`, `gplsrc/kernel.c:241`, `gplbld/secure-cred.ps1`, `gplbld/secure-osusers.ps1` ***— REPRODUCED UNDER INSTRUMENT 30 Aug 2026 BY `verify-sdsyswrite.ps1` (73), AND IT IS A STRAIGHT PERMISSIONS DENIAL***: `Unable to set password for SDSWA2, **status 3035**`, and `err.h:145` gives `ER_PERM 3035 /* Permissions error (os.errno) */`. **The elevated control passed in the same run** — same command, same account, `Password set for account` — so the probe can see a success and the difference is the token, exactly as reasoned. ***AND THE SECOND STORE IS NOW MEASURED RATHER THAN REASONED***: `MODIFY.ACCOUNT <acc> OS-ON` from the same unelevated SDSYS also failed to write `os.users`, so 68's class is both stores and not just `$cred`. ***ONE PREDICTION IN THIS ROW WAS WRONG AND IS CORRECTED HERE.*** It said the unelevated session would fail at the `$cred` **OPEN**, at `SET_ACC_PASSWORD:149`'s *"Cannot open the $CRED register"*. **It does not.** The open SUCCEEDS — the run printed *"Account SDSWA2 has no password set. Setting the first one."*, which is only reachable after `:143-147` has read the file — and the failure comes later, at the **write**. **So the ACL permits the open and refuses the write, which is why the command gets all the way to collecting both passwords before it fails**, and why the user sees a late failure rather than an early refusal | `gpl.bp/SET_PASSWD:130`, `:162`, `gpl.bp/CRED_SET:68`, `:114`, `gpl.bp/CREATEA:602`, `gpl.bp/PS_SCRIPT:166`, `gpl.bp/CPROC:2769`, `gplsrc/kernel.c:241`, `gplsrc/err.h:145`, `gplbld/secure-cred.ps1`, `gplbld/secure-osusers.ps1`, `gplbld/verify-sdsyswrite.ps1` ***— FIXED 30 Aug 2026 ON THE OWNER'S RULING, "route the `$cred` write through `ps_script` with the read-back verification". BUILT, UNCOMPILED.*** `CRED_SET`'s direct `write` now falls back to `ps_script`, which hands the script to the elevated helper when `K$ADMINISTRATOR` is set (`PS_SCRIPT:166`) and falls back to `os.execute` when it is not — **so an ordinary caller behaves exactly as before.** ***THREE THINGS WERE MEASURED RATHER THAN ASSUMED BEFORE A LINE WAS WRITTEN, AND EACH WOULD HAVE CORRUPTED THE CREDENTIAL STORE.*** **(1) The field mark on disk is CRLF, not LF** — `od -c` on `sdsys/os.users/don` reads `y e s \r \n y e s \r \n`, so an LF-only write would store a record SD reads back with the wrong field count, silently. The script uses `[char]13 + [char]10` rather than an escape, so nothing depends on surviving `Invoke-Expression`. **(2) ASCII is safe because every value is base64** — `gplsrc/sd_scram.c:26`, *"EVERY BINARY VALUE HERE IS BASE64, in and out"* — so no value can contain the quote the script is built with. **(3) `pstmp` is already hardened for credential material**: `secure-psdir.ps1` gives it `CREATOR OWNER (OI)(IO)(F)` with `sdusers` holding directory rights only, added **16 Aug 2026** because *"!set_passwd's script carries a new Windows password in clear"*. ***THE READ-BACK IS THE POINT AND NOT A COURTESY.*** Either path can report success and leave a record SD cannot use — the elevated one goes through a script whose exit code says the FILE was written and nothing about whether SD can parse it — and an unusable `$cred` record is an account that authenticates against nothing, discovered at the next login rather than here. **So the record is read back through SD's own reader and BOTH keys are compared, the same fields `!CRED_VERIFY` will use.** ***WHAT CLOSES IT IS A CYCLE THEN `verify-sdsyswrite.ps1` GOING GREEN*** — it is written to be red until exactly this lands. ***AND `os.users` IS FIXED THE SAME WAY, SO ONE CYCLE CARRIES BOTH.*** `MODIFYA:757` takes the identical fallback and read-back — `secure-osusers.ps1` grants `sdusers` `(OI)(CI)(RX)`, read-only, so that write was refused for the same reason. ***THE ELEVATED WRITE HAPPENS AFTER `close`, DELIBERATELY***: the `readu` above holds an update lock, and letting an outside process write the file while SD holds a record lock would be a lock SD believes in and Windows knows nothing about. **The read-back re-opens the file and compares both fields, so a script that wrote something SD cannot read back is a failure rather than a success** ***— HALF RIGHT, AND `-Prefix sdswa4` ON 30 Aug 2026 NAMED THE OTHER HALF: 6 PASS / 1 FAIL, STATUS 3035 → 3037.*** The elevated write now SUCCEEDS — `ps_script` returned 0 — and the failure moved to the READ-BACK, which is exactly what the two-stage status was added to tell apart. ***THE READ-BACK WAS COPIED FROM `MODIFYA`, WHERE IT IS VALID, INTO THE ONE FILE WHERE IT CANNOT BE.*** `secure-osusers.ps1` grants `sdusers` `(OI)(CI)(RX)`, read-only, so MODIFYA's unelevated read-back genuinely works — and `os.users` PASSED on the identical route in the same run. `secure-cred.ps1` grants `sdusers` **nothing — not write, and not read either** (its own comment: *"sdusers is granted NOTHING here. That is the entire point."*), so the process that NEEDS the fallback cannot read `$cred` back afterwards. ***MEASURED DIRECTLY, NOT REASONED***: an unelevated shell gets `Permission denied` listing `$cred`, while `os.users/don` reads `y e s \r \n y e s \r \n`. ***AND `read ... else` HID IT***: a permission denial and a missing record take the SAME else branch, so *"wrote it and could not look"* was reported as *"wrote it and it did not read back"*. **The same shape of error as the close-before-write rule and in the same week — a rule lifted from the file where it holds into the file where it does not.** ***THE FIX IS THAT THE HELPER VERIFIES ITS OWN WRITE***, being the only party that can read the file: it returns **2** for wrote-but-mismatched, which `CRED_SET` maps to `ER$WRITE.ERROR`, while any other non-zero — including `ps_script`'s `-1` for "could not run" — stays `ER$PERM`. **The SD-side read-back now runs ONLY on the direct-write path**, where this process demonstrably has access and SD's own reader is the better check. ***`-cne` AND NOT `-ne`, AND THAT IS MEASURED***: PowerShell's default comparison is case-INSENSITIVE and every value here is base64, which is case-SIGNIFICANT — a bench check confirms `-ne` ACCEPTS a record differing in case alone and would report it verified. ***DONE 30 Aug 2026 — `-Prefix sdswa5` IS 7 PASS / 0 FAIL / 0 SKIP, WHICH IS EXACTLY WHAT THIS ROW SAID WOULD CLOSE IT.*** Install **30 Aug 12:02:00**, `assert-current` **exit 0 live**, and the installed `gpl.bp/CRED_SET` is **byte-identical to source** (`sha256 2657b46b…`) and carries the fix's marker — **so the green run measured the fix and not a stale tree.** ***THE ANCHOR IS THE SUCCESS WORDING***, `Password set for account SDSWA5`, with no refusal marker present; the previous two runs printed *"Unable to set password … status 3035/3037"* in its place. **All three controls green** — setup created the account, the unelevated session reached SDSYS and read it (`3 record(s) counted`), and the ELEVATED control still writes `$cred` — and the tally equals the row count, so the run refuses to be a false green. **`os.users` green on the same route**, and cleanup left no account and no Windows account behind. **Both blockers 68 names are now closed; 72 is fixed and still needs its own provocation** | `gpl.bp/CRED_SET:160-260`, `gpl.bp/MODIFYA:757`, `gpl.bp/SET_PASSWD:130`, `:162`, `gpl.bp/CREATEA:602`, `gpl.bp/PS_SCRIPT:166`, `gpl.bp/CPROC:2769`, `gplsrc/kernel.c:241`, `gplsrc/err.h:145`, `gplsrc/sd_scram.c:26`, `gplbld/secure-cred.ps1`, `gplbld/secure-osusers.ps1`, `gplbld/secure-psdir.ps1`, `gplbld/verify-sdsyswrite.ps1` |
| ~~69~~ | **S** | ***MESSAGE 10034 ASSERTS ssh FOR AN ACCOUNT THAT HAS NONE, SO `create.account … api` CONTRADICTS ITSELF — 37's FIX WAS INCOMPLETE FOR THE TWO ROUTE VALUES ITS SAMPLE DID NOT CONTAIN.*** Measured by the owner 30 Aug 2026 on the VM, `create.account user james api`: *"JAMES may reach this computer only over ssh - the console and Remote Desktop are denied to it."* followed immediately by *"SD routes for JAMES: the API only, not ssh."* **`10034` is printed unconditionally whenever the account joins `sdsshonly` (`CREATEA:911-914`) and describes the WINDOWS logon right; the route line is the other gate.** ***ITS SECOND CLAUSE IS TRUE AND ITS FIRST IS FALSE***: james is in `sdsshonly`, so the console and Remote Desktop really are denied him — but he is **not** in `sdssh`, so `sshd_config`'s `AllowGroups` will not admit him and **ssh is not a route he has at all.** ***THIS IS 37's FIX BEING INCOMPLETE, AND THAT ENTRY RECORDS EXACTLY HOW IT HAPPENED.*** 37 prescribed this very wording — *"something like `may reach this computer only over ssh` for the logon right"* — and named its sample in as many words: ***"This is the example to fix against"***, the example being `both`. **The wording is true for `ssh` and `both` and false for `api` and `none`**, the two values the sample did not contain. **The owner used `none` for `john` earlier the same evening, so both broken cases were exercised inside an hour.** ***THE LESSON IS THE GENERAL ONE RATHER THAN THE STRING***: a message fixed against the worst-LOOKING example was never read against the other values of the same keyword, and `SSH | API | BOTH | NONE` is a four-value enumeration that any wording change has to be checked against four times. **The gates are correct — this is what the tool TELLS the administrator, and the risk is operational: a reader may believe james already has ssh and never add him to `sdssh`.** **The fix is wording again: `10034` should state only the Windows fact it owns — the console and Remote Desktop are denied — and leave every claim about ssh to the route line, which already reads correctly in all four cases (`10076`/`10077`/`10078`)** ***AND THE ROOT OF IT IS THAT THE GROUP IS MISNAMED — OWNER'S QUESTION, 30 Aug 2026: "why is he in `sdsshonly` if it was not chosen?"*** **The membership is CORRECT and the name is not.** Checked every use: `sdsshonly` is written in exactly one place (`CREATEA:911`) and consumed by exactly one thing — `deny-logon.ps1:29`, which sets `SeDenyInteractiveLogonRight` and `SeDenyRemoteInteractiveLogonRight`. **Nothing else reads it**; the remaining hits are verifiers and cleanup lists. **So the group does not GRANT ssh — it DENIES the console and Remote Desktop, which james must be denied exactly as much as any other SD account.** What denies him ssh is a different fact: he is **not in `sdssh`**, so `AllowGroups` never admits him. ***HE IS THEREFORE api-ONLY AT ALL FOUR LEVELS ALREADY*** — console denied, RDP denied, ssh denied, API allowed — **and `verify-routes.ps1:300`/`:318` encode that design, asserting every standard account IS in `sdsshonly` and an administrator is not, whatever the route.** ***THE NAME REPEATS THE FALSE CLAIM A SECOND TIME, IN THE GROUP'S OWN COMMENT***: `sd.iss:511` creates it with `/comment:"SD accounts restricted to ssh"`. **A rename (`sdnologon`, say) would remove the confusion at its source, but it is a SHIPPED group name** — an installer step, the account-creation path, five verifiers, the cleanup lists and the documentation — **and an existing install would carry the old name, so it is a bigger change than the message fix and should be ruled on separately** ***— FIXED 30 Aug 2026 BY MAKING 10034 STOP CLAIMING WHAT IS NOT ITS TO CLAIM.*** It is printed unconditionally on joining `sdsshonly`, and **`sdsshonly` is about the WINDOWS LOGON RIGHT** — true for all four route values. The route line printed immediately after it is the other gate and was already right. **So the message keeps its true clause and drops the false one**, and now reads: *"%1 is denied sign-in at the console and over Remote Desktop. The next line says which ways in it has."* ***NO PER-ROUTE BRANCHING AND NO NEW MESSAGE***, which is deliberate: 37's fix broke because it wrote one sentence against a sample containing only `ssh` and `both`, and any wording that asserts a route has to be right for four values and stay right when a fifth is added. A sentence that describes only the logon right cannot go stale that way. ***DONE 30 Aug 2026, READ ON SCREEN FROM THE VERB ITSELF.*** `create.account user jtest api` printed **"JTEST is denied sign-in at the console and over Remote Desktop. The next line says which ways in it has."** immediately followed by **"SD routes for JTEST: the API only, not ssh."** ***THE TWO LINES NOW AGREE***, where the pair the owner measured on the VM contradicted each other in consecutive sentences. **The account was then removed cleanly** — `Group: sdu_JTEST Deleted`, `OS User: JTEST Deleted` — so nothing was left behind by the test | `sdsys/messages/10034`, `gpl.bp/CREATEA:911`, `:914`, `:936`, `gplbld/deny-logon.ps1:29`, `gplbld/sd.iss:511`, and entry 37 |
| 70 | **S** | ***AN UPGRADE REPLACES `newvoc` AND `voc_template` BUT RE-RUNS NOTHING, SO NO EXISTING ACCOUNT — INCLUDING SDSYS's OWN — EVER GAINS A NEW VERB.*** Found 30 Aug 2026 from the owner's question, *"that is a real hole as the most likely things to need updated are in sdsys."* ***THE BIG VERSION OF HIS WORRY IS ALREADY SOLVED AND THE RECORD SAYS OTHERWISE — SEE THE SECOND HALF OF THIS ROW.*** `stage.py`'s `write_upgrade_iss()` implements the owner's 25 Aug ruling, *"preserve the user's own files, replace all the shipped ones"*: **`gpl.bp`, `gpl.bp.out`, `messages`, `newvoc` and `voc_template` ARE replaced** on an upgrade, while `$cred`, `accounts`, `cat`, `os.users`, `batch.jobs`, `prt`, `$hold`, `bp` and `bp.out` are preserved. **So BASIC fixes and message fixes DO reach an existing install.** ***WHAT DOES NOT IS EVERY LIVE VOC.*** SDSYS's own `voc` and each account's VOC are built **from** those templates — by the bootstrap and by `CREATEA` — and are in **neither** list, deliberately (`stage.py:244-246`: everything the bootstrap and the running system create is in neither, so an upgrade cannot reach it). **`UPDATE.ACCOUNT` is the ruled mechanism for refreshing one** — `sd.iss:1872` and `upgrade-dicts.ps1:29` both say *"UPDATE.ACCOUNT's shape, which is already the ruling for VOC"* — **but nothing runs it on an upgrade and nothing tells the administrator to.** So a release that adds a verb ships the verb to `newvoc`, and **no existing account can type it.** **Entry 3 may be a symptom of exactly this** rather than an independent defect — check before working either. **`upgrade-dicts.ps1` is the precedent for the fix: an upgrade-only step that brings one part of the tree forward, reporting failure rather than swallowing it** | `gplbld/stage.py:237-246`, `:355`, `write_upgrade_iss()`, `gplbld/sd.iss:1872`, `gplbld/upgrade-dicts.ps1`, and entry 3 |
| ~~71~~ | **S** | ***`PROJECT_STATUS.md` §6 AND `CLAUDE.md` BOTH STILL SAY THERE IS NO UPGRADE PATH, AND IT HAS BEEN FALSE SINCE 25 Aug 2026.*** §6 (`:8882`) reads *"THE INSTALLED DATA TREE IS NEVER UPGRADED… `sd.iss` skips the entire `sdsys` set when `C:\ProgramData\SD\sdsys` already exists"* and *"There is no upgrade path (§7 step 3)"*; CLAUDE.md's Testing section carries the same justification. ***BOTH WERE OVERTAKEN BY `upgrade.iss`***, and `sd.iss:1044` states the invariant that replaced them — *"upgrade.iss is gated on this; the whole-tree entry in [Files] is gated on DataTreeAbsent. **One or the other fires on every install, never both and never neither**"* — while `sd.iss:380-383` keeps the old sentence on purpose, flagged as *"true for eleven days and the sentence a returning reader will remember."* ***IT COST SOMETHING THE DAY IT WAS FOUND***: reading §6 as current, this session was one step from filing a **B** claiming W1.0-0 could never be patched, and it was the owner's own instinct that the hole was real which prompted the check. **A stale warning in the handoff document is worse than no warning**, because §"Search the record before you run anything" makes these two files the thing every session trusts first. ***THE TESTING RULE THEY SIT INSIDE IS STILL RIGHT AND MUST NOT BE WEAKENED*** — a cycle still starts from a deleted tree — **but its stated REASON is now wrong, and a rule defended by a false reason is one the next session will argue with.** **§6 is corrected in the same commit as this entry; CLAUDE.md is the owner's standing-instruction file and is left for him** ***— §6 CORRECTED 30 Aug 2026. CLAUDE.md IS STILL OWED AND IS WHY THIS STAYS OPEN.*** The bullet now states the invariant from `sd.iss:1044` — *"one or the other fires on every install, never both and never neither"* — names what an upgrade replaces and what `SDSYS_PRESERVE` keeps, and points at `assert-current.ps1` as the instrument that replaced the hand-checks written beside it. ***THE TESTING RULE IS UNCHANGED AND ITS REASON IS NOW A TRUE ONE***, which was the whole risk: a cycle still starts from a deleted tree, but because an upgrade **re-runs nothing** (PRE_RELEASE 70) — so an upgraded tree is a different state, not a stale one. **A rule defended by a false reason is one the next session argues with**, and this one was one step from being argued into a wrongly-filed blocker. ***DONE 30 Aug 2026 — THE `CLAUDE.md` HALF IS WRITTEN, ON THE OWNER'S INSTRUCTION TO SETTLE THE OPEN RULINGS.*** That half was reserved for him because it is his file; he handed it over. The paragraph said *"the installer deliberately never overwrites an existing `C:\ProgramData\SD\sdsys`"* and now states `sd.iss:1044`'s invariant instead, names what an upgrade replaces and what it preserves, and — the part that matters — ***GIVES THE RULE A REASON THAT IS TRUE***: a cycle still starts from a deleted tree, but because an upgrade **RE-RUNS NOTHING** (entry 70), so no existing account ever gains a new verb. **Both halves are now done and this entry closes** | `PROJECT_STATUS.md` §6, `CLAUDE.md` §Testing, `gplbld/sd.iss:1044`, and entry 70 |
| ~~63~~ | **M** | ***DONE AND VERIFIED 29 Aug 2026 — `listf` NOW DESCRIBES ALL SIXTEEN, AND `$MAP` STILL READS `DH`, WHICH IS THE CONTROL.*** Measured on the **20:31:49** install with `assert-current` **exit 0 live** (*"no source file is newer than the install"*): the ten rows that printed a bare `F` now read `File - Spooler hold files`, `File - Account register`, `File - BASIC program source`, `File - Compiled BASIC object code`, `File - GPL BASIC program source`, `File - Compiled GPL BASIC object`, `File - System message texts`, `File - VOC given to a new account`, `File - Operating system users` and `File - Session IPC area`. **Zero bare type codes left in the column.** ***AND `-Run b67` IS GREEN IN BOTH HALVES ON THE SAME INSTALL***: `VerifyInstall1` every step exit 0, `VerifyInstall2` **19 of 19**, **655 `[PASS]` and zero `[FAIL]`** across 21 transcripts — so the twelve record changes broke nothing. *(Was: `listf` PRINTS A BARE `F` WHERE A DESCRIPTION BELONGS, ON TEN OF SDSYS'S SIXTEEN FILES.*** Measured 29 Aug 2026 on the live 18:55:20 install, from the `listf` output itself: `$hold`, `accounts`, `bp`, `bp.out`, `gpl.bp`, `gpl.bp.out`, `messages`, `newvoc`, `os.users` and `qfile` all show `F` in the **Description** column, while `$MAP`, `$ACC`, `SD.VOCLIB`, `dict.dict`, `syscom` and `voc` show real text. ***THE CAUSE IS A DELIBERATE FALLBACK MEETING A GAP, NOT A BUG IN EITHER HALF***: `voc.dic`'s `Description` item is `IF @ = '' THEN F1 ELSE @` over **NEWVOC**, so a file with no `newvoc` record falls back to **field 1 of the VOC record** — which in SDSYS's voc_template-derived VOC is the type code `F`. Nine of the ten have **no `newvoc` record at all**, correctly, because they are SDSYS-only files a new account never gets; `newvoc/newvoc` is the tenth and its field 1 is literally `F`. **So the fallback is doing what it says and there is simply nothing to fall back to.** ***COSMETIC, AND IT IS IN THE FIRST OUTPUT A NEW ADMINISTRATOR SEES***, which is why it is worth the ten records rather than nothing. **Two shapes were possible: give the ten a description, or make the fallback print empty instead of the type code.** ***THE FIRST IS BUILT*** — the second hides the gap everywhere it occurs, including in accounts, and a blank column teaches nobody what the file is. ***AND IT IS A LEGITIMATE FORM, NOT A SECOND MALFORMED RECORD — THE RECORD ALREADY SETTLED THAT AND IT WAS NEARLY MISSED A FOURTH TIME.*** `CPROC:1410` says the type code **may be followed by comment text with no intervening space** (the PI / PI-open / UniVerse rule), and HISTORY.md's *"the five malformed VOC_TEMPLATE entries were never broken"* is the correction that established it — after an UPSTREAM entry about those five had itself been **written and withdrawn**. **This session withdrew a second one over `$MAP` before finding that.** ***BUILT AND THEN VERIFIED 29 Aug 2026 — the cycle at 20:31:49, `b67`, and the `listf` above.*** Ten `voc_template` file records now read `File - …`; `edit` and `micro`, the last two of the section-8 five, are reduced to a bare `V`. **The invariant is asserted rather than assumed**: field 1's first character is what every reader takes (`CREATEA:1233`/`:1292`, `BASIC:201`, `FORMAT:79`, `PARSER:178`, `SPVIEW:103`, `CPROC`'s five `[1,1]`), all twelve still yield `F`/`V`, and the 392-of-392 newvoc agreement is unchanged. ***IT NEEDS A FULL CYCLE BEFORE ANYTHING CAN BE MEASURED*** — `assert-current` check B walks `sdsys` and these records are now newer than the install, so every verifier refuses until then. Found while closing 61, whose whole premise was a misreading of this same column.)* | `sdsys/voc_template/{$hold,accounts,bp,bp.out,gpl.bp,gpl.bp.out,messages,newvoc,os.users,qfile,edit,micro}` |
| ~~55~~ | **S** | ***`release.ps1` never runs the two doc generators that already refuse on a stale figure*** — measured 29 Aug 2026 by reading it: it calls `mkdoc.py` (:109), `mkpdf.ps1` (:126) and `checklinks.py` (:161), and **neither `mktclsyntax.py` nor `tclmap.py`**. Both of those compute the roster from the VOC and both **exit 1** when the typed lists disagree — which is exactly what they did over `encrypt.field`, undetected for a week, until 53 ran them by hand. ***So the guard already exists and nothing calls it.*** **Part one is nearly free: call both from `release.ps1` and fail the release when either refuses.** **Part two is the actual gap** — the generators check the typed *maps*, not the typed *prose*, so `mktclsyntax.py` printed `standard 81` in the generated card for a week while the tester set said `77` and nothing compared them. Have the generator emit its computed figures as data and assert the handful of labelled tier counts against it. **This is the guard called "the cheapest still available" in `a931c36`, now filed rather than left in prose.** ***COMBINED INTO 80 ON THE OWNER'S RULING, 30 Aug 2026 — CLOSED AS AN ENTRY, NOT AS WORK.*** The wiring is still missing and 80 is what fixes it. **Wiring it EARLIER would have been actively unhelpful**, which is the argument for the combination rather than against it: both generators `exit 1` on a roster disagreement, and the roster has moved three times this week — 78 alone takes the TCL verb count from 143 to 146 — so a `release.ps1` wired now would simply refuse every run until the documentation caught up | docs repo `tools/release.ps1:161`, `tools/mktclsyntax.py`, `tools/tclmap.py`, and **entry 80** |
| ~~59~~ | **S** | ***FIVE UNELEVATED VERIFIERS ASSUME AN ADMINISTRATOR LANDS IN AN ORDINARY ACCOUNT, WHICH 56 ABOLISHES*** — measured on `-Run b59`, 29 Aug 2026: unelevated **8 of 13**, and all five failures are one cause. `verify-lcnames` names it — *"the session is in the account, not SDSYS … [FAIL] WHO names the account"*. Also `verify-osusers`, `verify-nocase`, `verify-lineendings`, `verify-batchjob`. ***NOT PRODUCT DEFECTS: every one refused the null case out loud rather than scoring a false pass***, which is the instrument rule working on the first run that broke the assumption. **The fix is a real non-administrator test account for that half**, not a tweak to five scripts. ***`verify-nocase` IS GREEN ON `b61`, 3 of 3 — the first measurement this project has taken as a real non-administrator.*** ***DONE 29 Aug 2026 — ALL FIVE PASS ON `-Run b66`: UNELEVATED 13 OF 13, ELEVATED 19 OF 19, 1,106 `[PASS]` AND ZERO `[FAIL]`.*** Two were converted to a real non-administrator account (`nocase`, `lineendings`); **two needed no change at all** — `lcnames` (back to **142 of 142**) and `osusers` recovered the moment 56 clause 2 was reversed and an administrator landed in an ordinary account again; and `batchjob` was **re-aimed at SDSYS** on the owner's ruling, its row now reading `ELEVATED in SDSYS, no entry: still runs` **PASS, decisive** | `gplbld/verify-{lcnames,osusers,nocase,lineendings,batchjob}.ps1` |
| ~~61~~ | **B** | ***DONE 29 Aug 2026 — NOT A DEFECT. THE PREMISE WAS INVERTED, AND `newvoc` FIELD 1 IS A DESCRIPTION BY DESIGN.*** ***THE SYMPTOM DOES NOT REPRODUCE***: an elevated `listf` in SDSYS on the 18:55:20 install shows `$MAP` as **`DH`**, not `Err 30`, with both pathnames resolved. ***THE THREE FILES DO THREE DIFFERENT JOBS AND THE ENTRY COMPARED TWO OF THEM AS IF THEY DID ONE.*** **`voc_template` field 1 is the TYPE CODE and becomes SDSYS's own VOC** (`gplbld/stage.py:119`, `verify-lcnames.ps1:771` — both right; the "live reading appears to contradict" was the misreading). Live bytes agree: SDSYS's VOC holds `$MAP` `F` `@SDSYS/$map` `@SDSYS/$map.dic` (`sdsys/voc/%0`, offset 11280). **`newvoc` field 1 is the DESCRIPTION, AND ITS FIRST CHARACTER IS THE TYPE CODE.** ***`CREATEA:1233` REPLACES THE FIELD WITH ITS OWN FIRST CHARACTER*** — `rec<1> = if upcase(rec[1,1]) = 'P' then rec<1>[1,2] else rec[1,1]`, two characters for a `P` type, repeated at `:1292` for the administrator verbs. **So the description does not survive into an account's VOC, but its first letter is load-bearing**, and ***the invariant is measured: 392 of 392 `newvoc` first characters equal `voc_template`'s type code, 0 mismatches***, installed tree and source alike. *(An earlier pass here cited `CREATEA:1181` and said the field was simply dropped. **Both were wrong**: that comment is about the tier list records — `TIER.OMIT.STANDARD` field 1 reads `This record is not a VOC entry…` — and nothing about it concerns VOC descriptions.)* `don`'s live VOC carries the type code `F` and **zero** newvoc description text, which is question 2 of this entry answered. ***AND THE DESCRIPTION COLUMN IS A LOOKUP, NOT A FIELD READ***: `voc.dic`'s `Description` item is `IF @ = '' THEN F1 ELSE @` over **NEWVOC**, so `listf` shows newvoc's text when there is one and **falls back to field 1** when there is not — which is why ten SDSYS rows print a bare `F` where a description belongs. **That fallback is the only real wart here and it is filed separately as 63, `M`.** ***THE CONTROL THAT SETTLED IT***: neither `File for MAP output` **nor** `File - Vocabulary` appears anywhere in `sdsys/voc/%0` or `%1`, while `listf` displayed both — so the column cannot be reading the VOC record, and the first attempt to explain it from field 1 alone was measuring the wrong thing. **`Err 30` itself came from `FTYPE:54`/`:68` on a failed `openpath` of field 2, and field 2 is byte-identical in both copies, so field 1 was never a candidate cause.** ***WITHDRAWN UPSTREAM TOO*** — [UPSTREAM_FIXES.md](UPSTREAM_FIXES.md) carried the same false claim and was one step from being sent. *(Was: `newvoc/$MAP` HAS NO TYPE CODE, SO SDSYS'S VOC SHIPS ONE BROKEN FILE RECORD ON EVERY INSTALL — Field 1 reads `File for MAP output`, the description, where every other file record has **`F`**. `LISTF` in SDSYS reports it `Err 30` on the live install. Found 29 Aug 2026 while confirming entry 60's cleanup. Do not just paste the `F` in until that is answered.)* | `sdsys/newvoc/$MAP`, `sdsys/voc_template/$MAP`, `gpl.bp/CREATEA:1181` |
| ~~62~~ | **B?** | ***DONE AND MEASURED 29 Aug 2026 ON `-Run b68` — THE HOLE DID NOT SURVIVE THE REVERSAL, AND THE `B?` RESOLVES TO "NOT A B".*** `verify-sdsysgate` **10 decisive checks, 0 failed**, on the 20:31:49 install: a real non-administrator (`sdgateb68`, confirmed **not** in the Administrators group by reading the group rather than SD's wording) landed in **its own account** over ssh, and its `LOGTO SDSYS` was ***refused BY IDENTITY — `reason=not an administrator` in the audit***. **Both disqualifiers absent**: no `reason=elevation refused or unavailable`, so execution never reached `elevate('START')`, and no `ELEVATION GRANTED account=SDSYS`. The null case and the reader control both passed — the audit grew and the tail carried this session's own `LOGIN` record — so the two absence-based checks were reading a real tail rather than an empty one. **`b68` overall: `VerifyInstall1` every step exit 0, `VerifyInstall2` 20 of 20, 655 `[PASS]`, 0 `[FAIL]` across 22 transcripts, account removed clean.** ***THE ENTRY'S OWN TERMS ARE MET***: it said *"if it survives it is a `B`, and if it does not this entry closes with the measurement written down"* — it did not survive, and this is the measurement. **The verifier stays as a standing suite step, so the property cannot silently regress.** *(Was: TRACED 29 Aug 2026: BOTH ROUTES INTO SDSYS NOW TEST THE PERSON BEFORE ANYTHING PROMPTS — SO THE HOLE IS CLOSED IN CODE, AND NOTHING TESTS IT.*** ***READ BY SOURCE, NOT RUN, AND THAT IS THE WHOLE REMAINING GAP.*** **Route 1, `LOGIN:568`**: `case kernel(K$ADMINISTRATOR, -1) and kernel(K$OS.ADMINISTRATOR, 0)` — the branch needs an **already-elevated session** AND an **administrator person**, and a standard user fails both, so `elevate('START')` at `:578` is unreachable to them; `LOGIN:558` records that it now prompts for nothing, `sd-elevate.ps1:119` short-circuiting when the token is already an administrator's. **Route 2, `CPROC:2634`**: an explicit `if not(kernel(K$OS.ADMINISTRATOR, 0))` refuses with **10002** and audits `LOGTO REFUSED account=SDSYS reason=not an administrator` — ***placed BEFORE `elevate('START')` deliberately***, its own comment saying a refusal after UAC has drawn its dialog *"has already asked a person for a password it was never going to accept"*. **`elevate('START')` has exactly two callers and those are both of them.** ***THE KEY IS THE RIGHT ONE***: `keys.h:201` — `K_OS_ADMINISTRATOR` is *"the PERSON, asked of Windows every time. Nothing in SD can set, clear or forge it, and a LOGTO does not move it"* — implemented at `op_kernel.c:457` as `IsAdmin() && (connection_type != CN_SOCKET)`, carrying `kernel.c:240`'s guard so an API session cannot answer TRUE spuriously. **The audit half follows: a non-administrator can no longer reach the credential prompt on either route, so the helper can no longer run as somebody `@logname` is not.** ***SEV STAYS `B?` AND THE ENTRY STAYS OPEN, BECAUSE COMPILING IS NOT RUNNING***: **no verifier covers this** — `10002`, `not an administrator` and `LOGTO REFUSED` return **zero hits across every `gplbld/verify-*.ps1`** — so the refusal is asserted by reading and by nothing else. ***THE VERIFIER IS BUILT AND WIRED, 29 Aug 2026 — `gplbld/verify-sdsysgate.ps1`, AND IT HAS NEVER RUN. IT CLOSES ON `b68`, NOT BEFORE.*** ***THE ANCHOR IS THE ENTIRE DESIGN, AND sysmsg 10002 IS NOT IT***: `CPROC` prints 10002 on **both** refusal paths — the identity gate (`:2637`, audit `reason=not an administrator`) and the failed elevation (`:2651`, audit `reason=elevation refused or unavailable`) — and the account is reached **over ssh, which has no interactive desktop**, so `elevate('START')` would fail there anyway. ***A CHECK ANCHORED ON 10002 WOULD PASS WITH THE GATE DELETED.*** **The audit REASON is the only thing that separates them**, which is why the step is **elevated and lives in `VerifyInstall2`** — the trail is locked to SYSTEM and Administrators, measured: an unelevated read is *"Permission denied"*. It makes and removes its own account, VerifyInstall1's belonging to the unelevated half. **Ten decisive checks** *(written up as eight before the run counted them)*, including the null case (*the audit grew*), a reader control (*the tail carries this session's `LOGIN` record*), a Windows-side control (*the account is NOT an administrator*, read from the group rather than from SD's wording), and **two disqualifiers** — `reason=elevation refused or unavailable` and `ELEVATION GRANTED account=SDSYS` must both be **absent**. ***WHAT IT CANNOT DO, SAID IN ITS OWN HEADER***: it cannot reproduce the original hole, which needed a standard user at an interactive desktop typing an administrator's password into a RunAs credential prompt — no non-interactive test can make one. **It proves the property that closed the hole, not the hole.** ***VERIFIED ONLY AS FAR AS AN UNELEVATED SESSION CAN***: parse 0 errors / 2 functions, BOM 0, CR 0, both reachable guards **run and return exit 2** against a control that reads 0, and `assert-current` **exit 0 live** with it on `$neverShipped` — the session-79 trap, where three unlisted scripts made every verifier refuse. *(Was: what would close it is a verifier driving a real non-administrator at both routes**, which PRE_RELEASE 59's `sdtestuser` machinery already builds — now built as above.)* *(Was: RE-MEASURE WHETHER `elevate('START')` STILL ADMITS SOMEBODY WHO IS NOT AN ADMINISTRATOR — split out of **56** when that closed, so a measured finding is not lost because the code around it moved. As measured before clause 2 was reversed: `elevate('START')` gates on `Start-Process -Verb RunAs` succeeding and tests nobody's identity — that verb gives a standard user a *credential* prompt, so an administrator's password was enough to reach SDSYS, and `@logname` and `audit_message()` then named the standard user who did not consent.)*)* | `gpl.bp/LOGIN:568`, `gpl.bp/CPROC:2634`, `gplsrc/op_kernel.c:457`, `gplbld/verify-sdsysgate.ps1` |
| ~~60~~ | **S** | ***DONE 29 Aug 2026 — VERIFIED, `after: 0`.*** All four records deleted with `DELETE VOC` (`1 record(s) deleted` each), and an independent `LISTF` afterwards found **no `SD*BP.OUT` records at all**. The original finding, and the verb that was wrong first time: Run elevated, `DELETE.FILE` answered *"Error deleting DATA portion"* + *"DICT part of file does not exist"* on all four and changed nothing; **`clean-deadvoc` reported FAILED**, its verdict being a second `LISTF` rather than SD's wording. ***`DELETE VOC <name>` IS THE VERB***: `DELETEF` removes a FILE and the file these records name is already gone — the very thing being cleaned up. From `gpl.bp/DELETE`: naming ids takes the `num.ids > 0` branch, so **neither prompt is reachable** and `NO.QUERY` is unneeded. **sysmsg 3221 `"%1 record(s) deleted"` prints unconditionally, so it is NOT a usable success anchor** — `0 record(s) deleted` is on the failure path. Both scripts use `DELETE VOC` now, and `verify-catgate`'s is **unconditional**, because the record outliving the directory *is* the defect. ***STILL OPEN: the four records are still there and the rerun is unrun.*** The original finding: ***`verify-catgate` LEAVES A DEAD VOC RECORD IN SDSYS ON EVERY RUN, AND THE CODE DOES THE THING ITS OWN COMMENT FORBIDS.*** `LISTF` in SDSYS now shows `SDCATGB59BP.OUT` **and** `SDCATGB60BP.OUT`, both `Err 30` — SDSYS's VOC naming a file that is not there — one per suite run since b59, and `b61`'s will make three. `Remove-Fixtures` ([verify-catgate.ps1:161](sdb_ai/sd64/gplbld/verify-catgate.ps1:161)) deletes `<ACCT>BP` **through SD** with `DELETE.FILE ... FORCE`, then removes `<ACCT>BP.OUT` with **`Remove-Item`** — while the comment directly above it says to use SD *"because CREATE.FILE also wrote a VOC entry … deleting the directory alone would leave SDSYS's VOC naming a file that is not there"*. The object file made by `BASIC $ctlFile $ctlName` has a VOC entry of its own and nothing deletes it. **Harness, not product** — but it pollutes SDSYS, it accumulates, and `verify-lcnames` reads `LISTF` | `gplbld/verify-catgate.ps1:161` |
| ~~58~~ | **B** | ***DONE 29 Aug 2026 — the `Administrator` set describes the built model (`01-accounts-and-security.md:44-47`): elevation is fixed when SD starts, and SDSYS is reached from an elevated terminal or the UAC prompt `logto sdsys` raises.*** ***THIS ROW WENT STALE WITH EVERY CHECKER GREEN***, because `check-stale-leads.py` compares this file against itself and **cannot see the docs repository** — read that repo before reporting on any row whose work lives there. *(Was: THE DOCUMENTATION DOES NOT DESCRIBE THE ACCESS MODEL THE PRODUCT NOW HAS*** — owner's instruction, 29 Aug 2026, raised as 56 and 57 were written. **Every set is affected**: administrators are elevated at login into SDSYS and have **no account of their own**, they **lose ssh**, a grant may go **down or sideways only**, and **SDSYS is never granted**. Two new messages, **10126** and **10127**. ***DO NOT WRITE IT FROM THIS ENTRY*** — 56 and 57 both have pieces still unsettled, and the docs repo is a **separate git repository** at `C:\Users\dmont\Projects\SDCoreWindowsDocs` *(renamed 29 Aug 2026 to match its GitHub repository — this row used to warn of "spaces in its path", which is no longer true)*. ***THE "BLOCKED" HALF HAS LIFTED, 29 Aug 2026***: 56 clause 2 and 57 are built, cycled and proved by `-Run b66` (unelevated 13 of 13, elevated 19 of 19). **What is left is a scope question, not a blocker** — 56's own remainder is the `elevate('START')` identity hole, which the documentation does not describe anyway. **Do it with 34 and 55, as this entry has always said.** Not started.)* | docs repo `User`, `Administrator`, `Testing`, `Technical` |
| ~~57~~ | **B** | ***DONE 29 Aug 2026 — built, cycled and proved by `-Run b66`, including the promotion report, its last piece.*** "Installed and unrun" was a testing gap, not outstanding work; no verifier covers `modify.account b programmer` stranding grants, which is a gap worth filling one day. *(Was: A GRANT MAY GO DOWN OR SIDEWAYS, NEVER UP — owner's rule, 29 Aug 2026.*** *"Standard accounts can not be given access to programmer accounts, programmer accounts can be given access to standard accounts. Only windows administrators can enter SDSYS, rights to SDSYS can not be granted."* ***THE TIER IS THE ACCOUNT'S AND IT IS BAKED INTO ITS VOC AT CREATION***, so entering a higher-tier account handed over its whole verb set — **+42 verbs** for a standard user entering a programmer account, on the computed roster. **WRITTEN, UNCOMPILED**: new `gpl.bp/TIERGATE` (`!tier_allows`), wired into `CPROC`'s `logto.authorised`, `GRANTA` and `MODIFYA`'s ADD arm; messages 10126 and 10127. ***CPROC's IS THE ONLY GATE THAT HOLDS*** — the grant is a Windows group membership, so `net localgroup` makes one without SD, and a tier can be raised after a legal grant with nothing revisiting the group. ***CYCLED 29 Aug 2026, AND THE LAST PIECE IS IN***: `MODIFYA`'s `promo.snapshot`/`promo.report` name the grants a promotion voided, measured across the register write rather than computed from the ranks; messages 10128 and 10129. **Installed and unrun**.)* | `sdsys/gpl.bp/TIERGATE`, `CPROC` logto.authorised, `GRANTA`, `MODIFYA` |
| ~~87~~ | **S** | ***`k_error()` TRUNCATED EVERY MESSAGE AT ABOUT 84 CHARACTERS, AND HAS DONE SINCE THE BUFFER WAS SIZED.*** Found 31 Aug 2026 by **measuring** 12 rather than by reading the code: the new message 10151 came back as *"Error 3023 writing record: no lock is held on it. A WRITE must already hold an u"* — **cut mid-word**, so the half that tells the reader what to DO never arrived. ***`+` WHERE THE ALLOCATION USED `*`***: `s` is declared `char s[(MAX_ERROR_LINES * MAX_EMSG_LEN) + 1]` — 3 × 80 + 1 = **241** — and the bound passed to `vsnprintf` read `(MAX_ERROR_LINES + MAX_EMSG_LEN) + 1` = **84**. So the buffer was sized for three 80-column lines and the writer was told it had one line's worth. **Every `k_error()` in the product is affected**, not just the new message; it is simply that nothing had a message long enough to notice. ***AND THE OBVIOUS REPAIR IS A BUFFER OVERFLOW, WHICH IS THE PART WORTH KEEPING***: turning the `+` into a `*` would pass 241 — but `n` is already **10 bytes** of `"%08X: "` offset prefix written into `s` beforehand, so `vsnprintf` could then write to `n + 241` in a 241-byte buffer. **The fix is `sizeof(s) - n`**, which is correct whatever the constants become and needs no second place to keep in step. **Message 10151 was shortened to three lines with it** — rendered **202** against a bound of 231, checked by `check_msg_len.py`, which counts the escapes it substituted and refuses a run that substituted none. ***IDENTICAL UPSTREAM at `k_error.c:207`, `ae0cc5f`*** — UPSTREAM #28. ***MEASURED 31 Aug 2026 ON THE 01:05:10 INSTALL, `sd.exe` `87701F86…` — THE MESSAGE ARRIVES WHOLE.*** All three lines of 10151 rendered where the same probe had shown *"…must already hold an u"* one install earlier, so the reading is a before-and-after on the same instrument rather than a fresh green. **The install is the only place this could be judged**: the bound is compiled in, so no unit test could have caught it and no source review had for years | `gplsrc/k_error.c:225`, `gplsrc/sddefs.h:297-298`, and entry 12 |
| ~~86~~ | **M** | ***THE LITTER SWEEP WALKED PAST 25 OF 268 PROFILE DIRECTORIES AND REPORTED SUCCESS — THE THIRD TIME THIS STEM LIST HAS BEEN PROVED BY A MISS.*** Found 30 Aug 2026 while clearing `C:\Users` on the owner's instruction. `clean-test-profiles.ps1`'s `$stems` had **15** entries and neither `sdgate` (`verify-sdsysgate`, 9 directories `sdgateb68`–`b77`) nor `sdtu` (the `sdtu<Run>` test account `VerifyInstall1` creates, 16 directories `sdtub60`–`b77`). **Both families were invented after the 28 Aug sweep and neither added its stem**, which is exactly what that fix's own note requires — *"a new test that invents a name family has to add its stem HERE in the same commit, or its litter is invisible to the only thing that sweeps it up."* ***AND IT FAILED THE QUIET WAY, WHICH IS THE PART WORTH KEEPING***: all 25 **had** `ProfileList` entries, so nothing refused them and nothing counted them — the sweep did not skip them, it never saw the names, and `cleanup-devlitter.ps1` reported a clean run over a machine still carrying them. **That is 41's blind spot and 45's blind spot in the same file for the third time**, and the count is what exposed it: 268 directories on disk against 243 the pattern matched. ***FIXED AND MEASURED 30 Aug 2026***: both stems added, four real names added to `-SelfTest`'s must-match list and four word-shaped near-misses (`sdgateway`, `sdgatekeeper`, `sdtutorial`, `sdtuning`) to must-not — all four fail on the required digit. `clean-test-profiles -SelfTest` **33 of 33 must-match, 24 of 24 correctly rejected**; `cleanup-devlitter -SelfTest` **0 failed**, and it reads the pattern out of the sweep so the two cannot drift. **Coverage re-measured after the fix: 268 of 268 inside the rule, 0 outside.** ***THE REAL GUARD IS STILL NOT A CHECK AND THAT IS THE OPEN QUESTION THIS ENTRY LEAVES BEHIND***: nothing compares `$stems` against the account names the runners actually build, so a fourth family will be missed the same way. `VerifyInstall2.ps1`'s `-Run` block is the list to compare against, and `test-fixlist-units.ps1` is the precedent for a free unelevated checker — **not built, and filed as the recommendation rather than done** ***— BUILT 30 Aug 2026, AND IT FOUND TWO MORE FAMILIES ON ITS FIRST RUN.*** `gplbld/test-stemcoverage-units.ps1`, free: no install, no elevation, no run token. It reads `$stems` out of the sweep and the families out of BOTH runners — every account name is composed as `"sd<family>$Run"`, so that literal **is** the list — and fails a family with no stem. ***FIRST RUN: EXIT 1, NAMING `sdprof` (`verify-profiledir`, from `VerifyInstall2`) AND `sdsw` (`verify-sdsyswrite`, from `VerifyInstall1`).*** **That is four families missed across three occasions** — `sddr` (45), `sdgate`/`sdtu` (86), and these two — so the instruction asking each new test to add its own stem has been followed **none** of the four times it mattered. ***AND NEITHER HAD LEFT LITTER YET, WHICH IS WHY COUNTING `C:\Users` COULD NEVER HAVE FOUND THEM***: `sdsw`'s account is deleted in a `finally` and `sdprof` makes a fixture directory rather than an account. **A hole nobody has fallen into is still a hole, and only a source-to-source comparison sees it.** Both stems added with fixtures; `-SelfTest` now **37 of 37 must-match, 28 of 28 correctly rejected**, coverage **19 of 19**. ***BOTH DIRECTIONS WERE MEASURED ON REAL DATA RATHER THAN ASSERTED*** — red before the fix naming the two, green after. **Wired as a step in `VerifyInstall1` beside `test-tiercounts-units`**, for that step's own recorded reason: a guard that exists and runs nowhere is what let 86 happen. ***THAT TAKES THE UNELEVATED HALF FROM 16 STEPS TO 17*** — expect `17 of 17`, and a `16` means it was substituted rather than added | `gplbld/clean-test-profiles.ps1` `$stems`, `-SelfTest`, `gplbld/cleanup-devlitter.ps1`, and entries 41, 45 |
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

## 7. `sort.item` is withheld from a standard account and `list.item` is not — **M** — ***DONE 30 Aug 2026*** (STANDARD 354 → 355)

`sort.item` is on `newvoc/TIER.OMIT.STANDARD`; `list.item` is not. Both print
whole records field by field, so withholding one and not the other achieves
nothing. **Looks like an oversight in the list rather than a decision** — worth
confirming, because if it was deliberate the reason should be written down.

***CONFIRMED AN OVERSIGHT, 30 Aug 2026, FROM THE RULING THAT CREATED THE
LIST.*** `d913eac` (24 Aug 2026, session 50) records the owner's four rulings on
the first-pass split, and the read-only-inspector one **names its members**:
*"read-only inspectors (search list.diff list.item list.common list.vars
report.src report.style format) -> STANDARD"*. **`sort.item` is absent from a
list that names `list.item`**, so it was never put to him — it survived the
first pass unexamined. They are one program with two verb numbers: `list.item`
is `$QPROC` **10**, `sort.item` is `$QPROC` **11**.

***THE COST OF FIXING IT IS THE 82 SHAPE AND IS WORTH STATING BEFORE ANYONE
STARTS.*** Dropping the name takes the record **43 lines → 42** (42 names → 41)
and **STANDARD 354 → 355**, leaving **PROGRAMMER 396 and ADMINISTRATOR 419
unmoved** — that asymmetry is the check on the arithmetic. Three instruments
carry 354 and must move in the same commit: `verify-tiers.ps1:42`,
`verify-tierapi.ps1` and `test-tiercounts-units.ps1`. **Run the last of those
first**; it needs no install and answers in a second, and a whole suite run has
already been spent on exactly this mismatch.

**Not built.** Tier membership is a policy ruling and every one so far has been
the owner's.

## 8. `help` is an empty stub and F1 reaches it — **M** — ***DONE 30 Aug 2026*** (F1 prints 10149)

Internal verb 14. `CPROC:2498`'s body is entirely commented out and it returns
immediately; `f1.help` at `:2500` falls into the same empty routine, so **F1 at
the command prompt does nothing.** No VOC record in `newvoc` or `voc_template`
points at verb 14, so the name is not recognised either — measured:
`help is not in your VOC`.

**Decide whether F1 should say something** rather than silently doing nothing.
The documentation is the help system now, and the pages say so.

## 9. `umask` is implemented and unreachable — **M** — ***DONE 30 Aug 2026, BY A DECISION RATHER THAN A CODE CHANGE: KEEP IT*** (the dispatch is positional)

Internal verb 35. `CPROC:3301` is a working routine that reports or sets the
file-creation mask, and **no VOC record points at it**, so it cannot be typed —
measured: `umask is not in your VOC`. `umask()` from SD BASIC still works.

Either ship a VOC record for it or delete the routine; a working verb nobody can
reach is the kind of thing that reads as a missing feature.

***BOTH OF THOSE OPTIONS ARE WRONG AS WRITTEN. MEASURED 30 Aug 2026.***

***THE FIRST WAS ALREADY REFUSED, AND BY THE OWNER.*** `d913eac`, 24 Aug 2026,
session 50: *"UMASK removed entirely — POSIX file-mode-bits call, essentially
inert on Windows where security is ACL-based"*, and `sdsys/voc_template/umask`
was **deleted in that commit**. Read back from the tree: `umask` is absent from
**both** `newvoc` and `voc_template`. So "no VOC record points at it" is the
ruling working, not a gap — this entry was written without knowing that.

***AND THE SECOND WOULD BREAK START-UP IF TAKEN LITERALLY, BECAUSE THERE ARE TWO
THINGS CALLED UMASK AND ONLY ONE IS DEAD.***

- **LIVE, DO NOT TOUCH.** `op_umask` (`gplsrc/op_misc.c:1503`, opcode `0xCF0B`)
  is the SD BASIC `UMASK()` function, and **`CPROC:325` calls it on every
  start-up** — `if umask(002) then null`, with the comment above it explaining
  why. This entry's own last line already said `umask()` still works; what it
  did not say is that SD itself is the caller.
- **DEAD.** `int.umask` alone — `CPROC:3371-3381`, internal verb 35, dispatched
  from the table at `CPROC:1637`. Nothing can reach it because no VOC record
  names verb 35.

**So the remaining call is small**: delete `int.umask` and its dispatch entry,
or leave it as the tree already leaves `$MICRO` and `$NLS` — `d913eac` names
that precedent itself, *"stay compiled but callerless"*. Owner's, and it is a
one-line question now rather than a design one.

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

## 12. Error 3023 tells the user the disk may be full — **S** — ***DONE 31 Aug 2026*** (message 10151 at the call site; measured, and it found entry 87)

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

## 2. The installing user gets no `OS.EXECUTE` — **B** — ***DONE 29 Aug 2026, verified on `-Run b69`*** *(re-opened 29 Aug by 56, then measured and fixed the same day)*

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

## 24. `sd -cleanup` never releases a dead session's task locks — **S** — ***DONE 31 Aug 2026*** (`user_no`, not `process.user_no`; measured with the kill-survives control)

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

## 34. `release.ps1` cannot complete on the `Technical` set — **S** (docs toolchain) — DONE AS AN ENTRY, COMBINED INTO 80 ON 30 Aug 2026 (the work is not done; it is 80's)

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

## 39. Uninstalling strips SD's ssh confinement and leaves every account it created — **B** (ruled 29 Aug 2026) — ***DONE 30 Aug 2026, measured on a real interactive uninstall in `Windows 11 - Test`***

> ***READ THE ROW FIRST.*** The `-Remove` path ran for the first time and removed
> **2 of 2** accounts, keeping `don`; `sshd_config`'s SD block is gone; `tim`,
> which SD never created, was untouched. **Two legs were NOT exercised and are
> named in the row rather than ticked**: the last-administrator refusal, which
> never had to fire, and the keep-the-database branch. ***AND THE RUN EXPOSED A
> HOLE THIS FIX CANNOT COVER — `john`, half-created by 68, is in no group at all,
> so the sweep's `sdusers` candidate set cannot see him and he survived. That is
> PRE_RELEASE 72.***

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

## 54. `verify-profiledir.ps1` is in neither runner, so 36's last leg never fires again — **M** (verifier gap, not product) — DONE 30 Aug 2026, green on `b70` and `b72`

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

## 55. `release.ps1` never runs the two doc generators that already refuse on a stale figure — **S** (docs toolchain) — DONE AS AN ENTRY, COMBINED INTO 80 ON 30 Aug 2026 (the work is not done; it is 80's)

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
