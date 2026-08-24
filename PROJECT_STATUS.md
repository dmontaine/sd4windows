# PROJECT STATUS

Living handoff document for the SD Windows port. This project moves between
sessions, machines and accounts; anything not written here is lost. Read this
file first. Read [HISTORY.md](HISTORY.md) only if you need the record of how
something came to be the way it is.

**Last updated:** 24 Aug 2026, fifty-first session (OPGEN loose ends closed; one cycle owed).

---

## NEXT SESSION: START HERE, IT IS SHORT

> ## NEXT: NOTHING IS BLOCKING. §7 IS EMPTY, §8 IS CLOSED — ASK.
>
> ***THE CYCLE RAN AT 15:13:25, THE INSTALL LANDED AT 15:14:28, AND
> `assert-current` EXITS 0.*** `sd.exe` `275CFB03E142AA2C`. Transcript
> `%LOCALAPPDATA%\SD-verify\cycle-20260824-151325.log`, `CYCLE COMPLETE`,
> steps 1-8 all ran, both trees deleted and recreated. Installed counts match
> the staged ones exactly — `gcat` 126 (staged 126), `GPL.BP.OUT` 186 (staged
> 186), `$BCOMP` 88,070 — and the credential register has **1 account with a
> password**, so the suite will not stall at a password prompt.
>
> ### THE INSTALL WAS VERIFIED ON DISK, NOT READ OFF THE CYCLE LOG
>
> | probe | expected | observed |
> |---|---|---|
> | `assert-current` | exit 0 | **exit 0**, "no source file is newer than the install" |
> | installed `GPL.BP/OPGEN` | absent | **absent** |
> | installed `GPL.BP.OUT/OPGEN` | absent | **absent** — the object, a separate fact from the source |
> | installed `GPL.BP/ERRTEXT.H` rows `4100`/`4101`/`-10303` | present | **lines 98, 99, 216** |
> | installed `SYSCOM/ERR.H` `SD$SCRAM.ERR` | present | **line 286** |
> | installed `GPL.BP/BCOMP` naming `gen_includes.py` | present | **lines 22 and 66** |
> | installed `GPL.BP/OPCODES.H` `SDPYOBJ` | **absent** | **0 occurrences** |
> | **compiled `GPL.BP.OUT/ERRTEXT` carries the three new texts** | present | **all three** |
> | **catalogued `gcat/!ERRTEXT` carries them** | present | **all three** |
>
> **THE LAST TWO ROWS ARE THE ONES THAT MATTER**, and they are why this is more
> than "the files copied". `ERRTEXT.H` is `$include`d, so the strings only
> reach a running system by being compiled *into* `!ERRTEXT` — and `gcat/!ERRTEXT`
> is what actually executes. It differs from `GPL.BP.OUT/ERRTEXT` in **126
> bytes, all of them the fixed-width name field** (`!ERRTEXT` against `ERRTEXT`,
> space padding against NUL); same 11,321 bytes, identical thereafter.
>
> **BOTH CONTROLS WERE RUN, so the greps above are not trivially true**: the
> pre-existing row `DLL not found` **is** found in the same object (the search
> can see embedded strings at all), and `SDPYOBJ` is **absent from compiled
> `GPL.BP.OUT/BCOMP`** (the OPCODES.H change propagated through the compile,
> not just onto disk).
>
> ***WHAT WAS NOT DONE: `!ERRTEXT` WAS NEVER CALLED.*** No BASIC was run to
> display `errtext(4100)`. That would need a program compiled into the fresh
> install, and the static chain above was judged to cover it. **If a future
> session wants the behavioural proof, it is still owed.**
>
> ### A DEFECT IN `cycle.ps1` WAS FOUND WHILE CHECKING, AND FIXED
>
> ***`cycle.ps1` STARTED A TRANSCRIPT AND NEVER STOPPED IT.*** PowerShell 5.1
> keeps a transcript **active** until it is stopped or the session ends, and
> supports several at once — every active one receives every line. Two runs in
> **one** elevated window therefore left the first log open and recording the
> second.
>
> **IT HAD ALREADY CORRUPTED THE RECORD.** After the 15:13:25 cycle,
> `cycle-20260824-133558.log` — the log for the **13:36:51 install that this
> file cites** — holds **two** `CYCLE COMPLETE` lines and two step-1 banners,
> and `verify-tiers-20260824-134341.log` has an entire cycle appended after its
> own output. Neither carries a `transcript end` marker, because neither was
> ever stopped. **Treat both as contaminated.** The decisive
> `verify-tiers-20260824-141122.log` (22/22) is **untouched**, as is
> `cycle-20260824-150409.log`.
>
> **WHY IT SURVIVED THIS LONG**: a run launched as its own process
> (`powershell -File`) closes the file at process exit, so its log is clean and
> carries an end marker. The bleed only appears when the documented usage is
> followed literally — typing the script path at an already-open elevated
> prompt.
>
> **FIXED**: `StopCycleTranscript` in `gplbld/cycle.ps1`, called on all four
> exit paths (`Fail`, `-SkipInstall`, the `assert-current` failure, and the
> success tail). Parse-check 0 errors, **6 functions where HEAD had 5** so
> nothing was swallowed, no BOM, LF only. `cycle.ps1` is on `assert-current`'s
> `$neverShipped` list, so **the fix costs no cycle** — confirmed, exit 0 after
> the edit. **Any elevated window still open from before the fix still holds
> those stale transcripts; close it.**
>
> **INSTRUMENT NOTE FOR THE NEXT SESSION THAT ELEVATES BY SCRIPT.**
> `Start-Process -Verb RunAs -Wait` **does not set `$LASTEXITCODE`** — it comes
> back empty and the harness then reports the *launcher's* 0, which reads the
> same whether the cycle completed or aborted at step 2. **Read the
> transcript.** Use `-PassThru` and `.ExitCode` if a code is wanted.
>
> ### BOTH OPGEN LOOSE ENDS ARE CLOSED — session 51
>
> 1. **The two "run OPGEN" comments now name `gplbld/gen_includes.py`** —
>    [BCOMP:64-67](sdb_ai/sd64/sdsys/gpl.bp/BCOMP:64) and
>    [gplsrc/opcodes.h:36-46](sdb_ai/sd64/gplsrc/opcodes.h:36), each with a
>    dated START-HISTORY line. **The control that mattered**: `--check` still
>    reports `OPCODES.H` in sync *after* the `opcodes.h` edit, and that
>    header's own description says its layout "is known to" the generator, so
>    the edit could have moved the output.
> 2. **`ERR.H` and `ERRTEXT.H` regenerated**, all four outputs in sync. The
>    drift was smaller than session 50 read it: `SYSCOM/ERR.H` already carried
>    `ER$SRVRERR 4100` and `ER$INV.NBR 4101` (hand-added 19 Aug) and lacked
>    only `SD$SCRAM.ERR -10303`; `ERRTEXT.H` lacked the text rows for all
>    three. Additive and callerless — nothing in `sdsys/` names any of the
>    three, and [ERRTEXT:50](sdb_ai/sd64/sdsys/gpl.bp/ERRTEXT:50) looks up with
>    `locate errno in err<1> setting pos` over two arrays the generator builds
>    in step, so a mid-table insertion carries no positional dependency.
>
> **BOTH ARE NOW ON THE INSTALL** — the 15:13:25 cycle, verified in the
> table at the top of this block. `assert-current` exit 0 and
> `gen_includes.py --check` still reads four in sync. **There is still no
> verifier for error text**, and `!ERRTEXT` was never called; the proof
> is that the strings are compiled into `gcat/!ERRTEXT`, not that anyone
> watched it print one.
>
> ### §7 STEP 9 VERIFIER, NEVER STARTED
>
> Was the second mechanical item that came out of the "what tasks are
> left" review. Not begun this session.
>
> ### §7 IS EMPTY AND §8 TIER WORK IS CLOSED. ASK BEFORE STARTING ANYTHING.
>
> ***END OF THE FIFTY-FIRST SESSION, 24 Aug 2026.*** Three commits: the
> two OPGEN comments with `ERR.H`/`ERRTEXT.H` regenerated, the changelog
> entry for both and `make sd`; the `-SkipInstall` result; then the
> owner's full cycle at 15:13:25, its verification, and the `cycle.ps1`
> transcript fix. **The install is current and nothing is owed.**
>
> ***END OF THE FIFTIETH SESSION, 24 Aug 2026.*** The owner ruled the split,
> session 50 transcribed it to disk, the cycle at 13:36:51 installed it,
> and **`verify-tiers.ps1 -Prefix sdtierd` at 14:11:22 returned 22 of 22
> PASS** — including the between-tier controls (STANDARD lacks the 42
> withheld and the 21 admin, PROGRAMMER has the 42 and lacks the 21,
> ADMINISTRATOR has both) and the durability check (UPDATE.ACCOUNT does
> not restore what CREATE.ACCOUNT withheld). Section 3's COUNT VOC landed
> on **354 / 396 / 417 exactly**, the arithmetic in the verify-tiers
> header. **The three-tier split is settled, on disk, installed, and
> verified end to end.**
>
> Five commits this session: `82f5c66` handoff docs, `d913eac` disk apply,
> `e8bf060` cycle handoff, `7ca4597` verify-tiers Invoke-SD fix (the LOGIN
> TERM-reset trap; see the block below headed "THE HANG"), and the commit
> carrying this update.
>
> ### CLEAN THE HALF-INSTALLED PREFIXES AT LEISURE
>
> `sdtierc1/2/3` (the hung run before the Invoke-SD fix) and `sdtierd1/2/3`
> (the passing run — Cleanup removed their Windows accounts but leaves the
> SD register records "in place - remove with DELETE.ACCOUNT" by design).
> Nothing blocks on them. Removing with `DELETE.ACCOUNT sdtierc1` etc.
> inside SD when convenient.
>
> ### WHAT WAS MEASURED THIS TURN, WITHOUT ELEVATION
>
> | probe | expected | observed |
> |---|---|---|
> | installed `sd.exe` | matches source | `F53AE8F87BC55326`, 13:36:51 install |
> | installed `TIER.OMIT.STANDARD` vs source | identical, 43 lines | **identical, 43 lines** |
> | installed `TIER.ADD.ADMINISTRATOR` vs source | identical, 22 lines | **identical, 22 lines** |
> | 13 deleted verb files absent from install | none present | **none present** |
> | installed `newvoc/` V-verb count | 119 | **119** (395 total records) |
> | installed `voc_template/` V-verb count | 140 | **140** (425 total records) |
> | `DON` `ACCOUNTS` field 5 | `ADMINISTRATOR` | **`ADMINISTRATOR`** |
> | `DON` `COUNT VOC` | 417 | **417** — the ADMIN arithmetic exactly |
> | admin verbs (`sh`, `!`, `config`, `create.account`, `modify.password`) in DON's VOC | present | **present** |
> | programmer verbs (`basic`, `phantom`, `pstat`, `pdebug`) in DON's VOC | present | **present** |
> | standard-with-move (`search`, `report.src`) in DON's VOC | present (admin gets all) | **present** |
> | `umask` in DON's VOC | absent | **`'umask' not found`** |
> | `TIER.OMIT.STANDARD` / `TIER.ADD.ADMINISTRATOR` as VOC records in DON | absent | **`not found`** for both |
> | `verify-lineendings.ps1` | 17/17 PASS | **17/17 PASS**, all decisive rows PASS |
>
> ### VERIFY-TIERS 22/22 PASS AT 14:11:22 - THE DECISIVE RESULT
>
> Transcript: `%LOCALAPPDATA%\SD-verify\verify-tiers-20260824-141122.log`.
> Every one of the twenty-two rows PASS on the 13:36:51 install:
>
> | section | check | expected | observed |
> |---|---|---|---|
> | 0 | shipped OMIT vs test's `$Withheld` | 0 diffs | **0 diffs** |
> | 0 | shipped ADD vs test's `$AdminVerbs` | 0 diffs | **0 diffs** |
> | 2 | sdtierd1/2/3 `ACC$TIER` | STANDARD / PROGRAMMER / ADMIN | **matches** |
> | 3 | STANDARD `COUNT VOC` | 354 | **354** |
> | 3 | PROGRAMMER `COUNT VOC` | 396 | **396** |
> | 3 | ADMINISTRATOR `COUNT VOC` | 417 | **417** |
> | 4 | STANDARD missing 42 withheld / 21 admin | 42 / 21 | **42 / 21** |
> | 4 | PROGRAMMER missing 42 withheld / 21 admin | 0 / 21 | **0 / 21** |
> | 4 | ADMINISTRATOR missing 42 withheld / 21 admin | 0 / 0 | **0 / 0** |
> | 5 | STANDARD after UPDATE.ACCOUNT | 354, 42 still missing | **354, 42** |
>
> Section 4 is the decisive between-tier control: PROGRAMMER at "0
> withheld missing, 21 admin missing" is the row that stops a broken
> copy loop from passing STANDARD trivially. Section 5 is the durability
> half - UPDATE.ACCOUNT does not restore what CREATE.ACCOUNT withheld,
> which is the whole reason `ACC$TIER` exists.
>
> ### THE HANG: LOGIN RESETS TERM ON EVERY ACCOUNT SWITCH. `verify-tiers` IS FIXED.
>
> ***THIS TRAP IS SHARED BY EVERY VERIFIER THAT HAS AN `Invoke-SD` — TODAY
> ONLY `verify-tiers` PRODUCES ENOUGH OUTPUT TO HIT IT.*** `LOGIN` at
> `gpl.bp/LOGIN:201-209` re-initialises `PU$WIDTH` and `PU$LENGTH` from
> `env('LINES')` and `env('COLUMNS')` every time it runs. An elevated PS
> session usually has neither set, so `terminfo` supplies a default around
> 24 lines. `Invoke-SD` sent `LOGTO SDSYS` then `TERM 200,9999` then the
> caller's commands — so the caller's own `LOGTO sdtierc1` wiped `TERM`,
> and section 3's `LIST VOC` of 65 quoted verbs paginated. The page prompt
> reads the same stdin the script is feeding, and OFF had already been
> written, so no answer ever arrived.
>
> **WHY IT PASSED ON 17 Aug AND NOT ON 24 Aug.** The split moved Section 3's
> `LIST VOC` from ~29 items to 65. Twenty-nine fitted inside the default
> page depth; sixty-five does not. Same code, changed input.
>
> **`verify-tiers.ps1`'s `Invoke-SD` now re-applies `TERM 200,9999` after
> every `LOGTO` in the caller's commands.** Parse-check passes, and the
> reproducer with the fix's exact command sequence returns in one second
> against DON's VOC — the same sequence without the fix hangs indefinitely.
>
> **THE SAME FIX SPREAD TO EVERY OTHER VERIFIER THAT PREPENDED A `TERM`
> BEFORE THE CALLER'S COMMANDS**, so the class is closed rather than left
> latent — session 50 part 6: `verify-accountacl`, `verify-accountrules`,
> `verify-apiport`, `verify-delaccount`, `verify-routes`,
> `verify-scramlogin`, `verify-tierapi` (the seven canonical five-line
> shape); `verify-catgate`, `verify-nonet`, `verify-fold` (Start-Job
> wrappers with the same prefix); `verify-osusers`, `verify-keys`,
> `verify-lcnames`, `verify-setpw` (TERM-only prefix); `verify-apiname`
> (with its `$ESC` variant); and `verify-apiadmin`'s `Invoke-SDIn` (a
> per-account form). Each parse-checks 0 errors and carries no embedded
> BOM. Two verifiers were skipped deliberately: `verify-apiidentity` has
> no TERM prefix by design (the caller supplies it) and `verify-createaccount`
> has no TERM prefix at all — neither can leak a TERM it never set.
>
> ### THE WRITEPORT FIX LANDED IN THIS CYCLE TOO
>
> `gplsrc/op_seqio.c:1762`, `UPSTREAM_FIXES.md` #14, in the same
> `F53AE8F87BC55326` binary. It cannot be verified without a real port
> device, so its landing is announcement rather than proof.
>
> ### WHAT SESSION 49 CLOSED, IN ONE TABLE
>
> | | install | verifier |
> |---|---|---|
> | **§7 step 14** — an API session runs as the caller | 11:15:29 `7DDC68F6595382A6` | `verify-apiidentity -Prefix sdapiidb32`, decisive row PASS |
> | **§7 step 16 (a)** — readers accept CRLF | 12:15:51 `7F587B82B63569C8` | `verify-lineendings` 14/14 |
> | **§7 step 16 (b)** — writers emit CRLF | 12:36:09 `070A9C52E293B2FA` | `verify-lineendings` 17/17 |
>
> **Three defects were found in the instruments and the record while doing it**,
> and each is written up where it happened: `verify-apiidentity` had been
> **leaking an account per run since `b18`** while reporting otherwise; step
> 16's site list named a branch that was **never `READSEQ`**; and the same list
> missed that **every reader is chunked**, where a CRLF on a 2 KB boundary
> would have been wrong once per 2 KB of real data.
>
> ### STEP 14 IS CLOSED — AN API SESSION NOW RUNS AS THE CALLER
>
> Install **11:15:29**, `sd.exe` `7DDC68F6595382A6`, `assert-current` exit 0.
> `verify-apiidentity -Prefix sdapiidb32` exit 0, decisive row PASS.
>
> | instrument | before (`b28`/`b31`) | after (`b32`) |
> |---|---|---|
> | owner of `ZZAPI` | `NT AUTHORITY\SYSTEM` | **`GITORLI\sdapiidb32`** |
> | DENY fixture over the API | OPENED | **REFUSED, `status 3001`** |
> | `API IDENTITY LOST` in errlog | twice | **absent** |
>
> The fix is `CW_SET_EXTERNAL_TOKEN` **plus `seteuid`**, all in
> `gplsrc/win32s4u.c`, **no BASIC change**. `SYSTEM(28)` (`op_sys.c:228`) is
> the only BASIC-visible consequence and **has no caller in `gpl.bp`**, which
> is what chose class over narrow. §7 step 14 has the detail.
>
> ### STEP 16 (a) IS CLOSED TOO — SD NOW READS CRLF FILES CORRECTLY
>
> Install **12:15:51**, `sd.exe` `7F587B82B63569C8`, `assert-current` exit 0.
> `verify-lineendings` exit 0, **14/14 decisive**. A CRLF record now reads
> **identically to the LF control**; `READCSV` no longer leaves a CR on the
> last field of every row. **Two checks are controls on the FIX**: a CRLF on
> the 2048-byte buffer boundary folds, and a lone CR survives as data.
>
> ### STEP 16 (b) IS CLOSED TOO — SD NOW WRITES CRLF WHERE IT CAN BE READ
>
> Install **12:36:09**, `sd.exe` `070A9C52E293B2FA`, `assert-current` exit 0.
> `verify-lineendings` exit 0, **17/17 decisive**, read side and write side.
>
> **The owner's rule decided the scope**, 24 Aug: a **directory** file's records
> are real OS files that external programs read and write, so they get the
> platform's line ending; **dynamic (DH)** files cannot be read from outside and
> do not matter. **Every site `Newline` reaches is on the external side of that
> line, and no DH path uses it at all**, so it resolved to `sddefs.h:65-66` —
> now `"\r\n"` / `2`. `DS` stays `/` (§7 step 12).
>
> `WRITECSV` now emits `A1,B1␍␊`, **conformant with the RFC 4180 claim its own
> documentation has always made**. Verified by reading **raw bytes**, because
> the reader now folds CRLF and a round trip through SD would pass regardless.
>
> ### ONE THING LEFT ON THE FLOOR, AND IT NEEDS A REBOOT
>
> `C:\Users\sdapiidb32` survives as a **stuck hive** — its account is gone, so
> nobody is signed in, but the registry hive was never unloaded and a profile
> cannot be removed while it is loaded. `clean-test-profiles.ps1` names it and
> refuses, correctly. Clear it by rebooting and re-running that script, or
> `reg unload HKU\S-1-5-21-3329101812-2004472801-1855080994-2150` elevated.
>
> ### SUPERSEDED — THIS BLOCK DESCRIBES A TREE THAT WAS INSTALLED ON 24 Aug
>
> ***EVERYTHING BELOW UNTIL THE NEXT `###` IS SESSION 49's STATE AND IS NO
> LONGER TRUE.*** The `writeport` fix it says is uninstalled was installed by
> the **13:36:51** cycle, and the tree has been cycled twice more since
> (15:04:09 `-SkipInstall`, 15:13:25 full). `assert-current` exits **0**.
> Kept for the transcript names only. *Marked 24 Aug 2026, session 51 — it
> was already false when session 50 handed over.*
>
> **`op_seqio.c:1762`, the `writeport` CR-only fix** (§7 step 16, and
> `UPSTREAM_FIXES.md` #14).
>
> | | |
> |---|---|
> | installed `sd.exe` | `070A9C52E293B2FA`, **12:36:09** — the step 16 (b) build |
> | `bin/sd.exe` | `F53AE8F87BC55326`, 12:47:43 — carries the `writeport` fix |
> | last **full** cycle | `cycle-20260824-123527.log`, ended 12:37:08 |
> | last run of any kind | `cycle-20260824-124801.log`, **`-SkipInstall` only**, 12:48:38 |
>
> ***A FULL `cycle.ps1` WAS BELIEVED RUN AND WAS NOT.*** Checked against the
> transcripts, not against the report: **no log after 12:37:08 reaches phase
> 5**, and the installed binary is still dated 12:31:50. Whatever ran either
> stopped at `-SkipInstall` or did not start. **Nothing is broken by this** —
> the installed tree is the fully verified step 16 (b) one — but the
> `writeport` fix is **not in it**, and no measurement taken now describes it.
>
> **It cannot be verified even after a cycle**: exercising `WRITESEQ` to a port
> needs a real port device and no verifier here reaches it. **So consider
> batching it with the next real change rather than spending a cycle on it
> alone** — the owner's call, not a decision already taken. **A cycle ends at the next source change**, so take
> any reading you want from this tree *first*.
> **Prefixes `sdapiidb18`–`b32` are spent; use `b33` or later.**
>
> **`verify-lineendings.ps1` needs no prefix and no elevation**, and cleans up
> after itself — it is the cheapest way to confirm a tree is sane.
>
> ### WHAT IS ALREADY BUILT, SO IT IS NOT BUILT AGAIN
>
> - **`K$IMPERSONATING` (62)** — `<1>` the identity Windows says this thread has,
>   `<2>` whether SD holds a token. **`<1>` empty with `<2>` true IS the defect.**
>   `APISRVR`'s `check.identity` logs it at the group check and at the write,
>   **only when the two disagree** — so a healthy session is silent, and **its
>   going quiet is how you will know a fix worked.**
> - **`gplbld/probe-impfork.c`** — is the runtime governing `open()`, does
>   ownership track the token, and the Q3 bisect of what drops impersonation.
>   `--q3check` and `--ownercheck` self-test without elevation.
> - **`gplbld/probe-sessionfork.ps1`** — watches `Win32_ProcessStartTrace` during
>   a live API session. `-SelfTestOnly` proves it fires without spending a cycle.
>
> ### INSTRUMENTS THAT LIED, 23–24 Aug. ALL ARE FIXED; THE PATTERN IS NOT.
>
> `ImpersonatingUser()` returned SD's belief rather than asking Windows.
> `probe-sessionfork` read a Cygwin `fork`+`exec` — **two** Windows process
> creations — as one, and got the right verdict for the wrong reason.
> `clean-test-profiles` printed *"someone is signed in"* about deleted accounts.
> **24 Aug adds two more.** `q4_report` called a form **"lost"** that a
> `seteuid` fast path had meant never ran — caught only because the row printed
> its real inputs. And **`verify-apiidentity` announced *"account removed"*
> unconditionally for `b18`–`b31` while `DELETE.ACCOUNT` was refusing its
> arguments outright** (below). **Each was a value measured with an explanation
> bolted on that was not.** §6 and §0 carry the rules; the habit they need is
> separating what was read from what it was taken to mean.
>
> ### THE VERIFIER WAS LEAKING AN ACCOUNT PER RUN, AND SAYING IT WAS NOT
>
> `verify-apiidentity.ps1` called `DELETE.ACCOUNT <name> USER`. **The verb takes
> the account name and nothing else** — `DELACC:103` rejects any further token
> with sysmsg 2018 *before deleting anything* — and the next line announced
> success without reading the output or the state. So **every run from `b18` to
> `b32` left its Windows account, SD record and profile behind**; that is the
> backlog `clean-test-profiles.ps1` keeps being asked to clear. Fixed 24 Aug:
> the argument is dropped and the claim now anchors on **the account record and
> the local user actually being gone**, printing the raw output when they are
> not. The corrected form was then run for real and removed both.

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

> ***READING THESE FILES IS NOT THE SAME AS SEARCHING THEM, AND THE PROJECT RULE
> IS TO SEARCH.*** Owner's instruction, 23 Aug 2026: **grep PROJECT_STATUS.md
> and HISTORY.md for the verb, script or flag in any command before running it.**
> `CLAUDE.md` §"Search the record before you run anything" is the rule; it is
> there rather than here because it is loaded every session and this section is
> not. **Three or four consecutive sessions lost time to a warning that was
> already on disk** — most recently `echo WHO | sd` on 23 Aug 2026, which
> §START HERE already recorded as making an unusable session.

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
- ***STILL UNEXERCISED ANYWHERE: winget fetching MSYS2, and the pacman run.***
  Both were skipped because `C:\msys64` and all 9 packages were already there.
  **These are the two steps with the most left to go wrong** and no run so far
  has touched either.
- **`diffutils` was missing from the package list** and is missing on this
  machine too, so the list is now 10.

**THE NEXT RUN WANTS A VM SNAPSHOT OF A CLEAN WINDOWS**, not a developer's
laptop — §7 step 2 documents a reusable rig. Nothing short of a machine with
no MSYS2 will exercise the remaining two paths.

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

**Release identity was not taken either.** Dev bumps to 1.0-3; we are 1.0-2, and
that is not something to change by inference. Owner's call.

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
two" — but that redirected the **Windows** mirror only. **`sdclilib32` is still
two hops away and nothing compares it.**

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
fetched from the tree we already clone; ask the owner.

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

### 4.0 The verifier inventory — all 28, and which are actually run

***COUNT CORRECTED 24 Aug 2026: `ls verify-*.ps1 | wc -l` says **28**, where
the heading said 27 and the paragraph below said 26.*** The two that were never
added here are **`verify-apiidentity`** (§7 step 14 — measured for the first
time on 24 Aug, run `b28`, and it FAILS on a real product finding) and
**`verify-pcodeacl`** (§7 step 15). Both are on `$neverShipped`. **Count the
directory rather than trusting this line** — it has now been wrong twice, in
both directions, which is what the rule below exists to stop.

***THERE IS ALSO ONE NON-VERIFIER TEST, AND IT IS IN NEITHER RUNNER:***
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
| `verify-sshonly` | exit 1 — **OPEN, and the owner's call**. Every `ssh` attempt was refused, **including the control**, because it builds a plain local account in **no SD group** and `sshd`'s `AllowGroups` now names `sdssh`. The test predates §5.6.2's own change. `verify-createaccount` step 3 already proves ssh works on an SD-made account, so nothing is unmeasured — but this file now asserts a premise the product no longer has |

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

**A ROW IS EVIDENCE ABOUT THE INSTALL IT NAMES AND NOTHING SINCE.** Only
22 Aug 2026's **22:50:18** install is current (`sd.exe` `CB9C4E0460B175F5`,
unchanged since 21 Aug because no C has changed — the hash is not evidence
that anything else is, and the mtime comparison is what settles the rest).
Dating the tree before believing a result is §6's most expensive lesson.

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

**SWEPT 21 Aug 2026 AND SWEPT AGAIN WHILE COMPRESSING.** Twelve claims here
have been struck or narrowed since 21 Aug because the thing they called unknown
had been measured, in several cases **hundreds of lines above the entry still
calling it unknown**. They are in the archive with what settled each.

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
  dialog **has** been seen and read on screen (17 Aug, *"looks fine"*). What is
  still unseen is the **`limitssh` task** and **`ApplyAllowGroups` reporting any
  of its three outcomes**, and neither can be seen here: `Check: SshServerAbsent`
  is false on a machine that already has OpenSSH, so the tick box never appears.
  **It needs the VM from §7 step 2.** Compiling an Inno script proves the Pascal
  parses and nothing more — the two defects already recorded in that script both
  compiled perfectly.

- **That SD works over an ssh session AT A REAL TERMINAL — only the tty half is
  left.** The two separately are done: an ssh session lands inside SD (above),
  and the MSYS2 tty layer was measured at a real Windows console on 19 Aug
  (§5.18). **What has never happened is those two at once** — an interactive
  `sd -ASOMEACCOUNT` at a terminal *reached over ssh*, where the pty is sshd's
  rather than `conhost`'s. §7 step 2's rig is what would answer it.

- **Semaphore locking under contention.** The semaphores have never been
  observed held, so the `sdsem.c` port is exercised only in the uncontended
  case.

- **Contention.** Two sessions have coexisted and `LISTU` listed both, so
  multi-user attach works. What is untried is two sessions *competing*: record
  locking between real users, and the API server path.

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

In the order they should be taken. **Steps 4 to 13 keep the numbers they have
carried since 13 Aug 2026**, because the rest of this file refers to them by
number; steps 1 to 3 were renumbered on 14 Aug 2026 when the install layout,
the staging script and the Inno installer were all finished and removed.

0. **CLOSED — 14 Aug 2026, sixth session. THE LINUX ACCESS MODEL IS RESTORED,
   INSTALLED AND VERIFIED END TO END (§5.6, §4).** All five rules observed, both
   `LOGTO` paths, `CREATE.ACCOUNT` at 16 of 16.

   **`git show f9edab0:sdb_ai/sd64/sdsys/GPL.BP/LOGIN`, lines 185–270, is the
   specification** — this repository's own pre-port source. The five rules in
   §5.6 are transcribed from it, not designed here. Read it before changing
   anything about who may enter which account.

   **The one deliberate departure from `f9edab0`: an elevated session skips the
   `ACC$GROUP` test**, because `ACCOUNTS/SDSYS` names a Linux group that does
   not exist on Windows. **And `IsElevated()` is not `IsAdmin()`** — a
   UAC-filtered token carries `Administrators` as deny-only, so the two answer
   different questions and both are wanted (`linuxlb.c`).

   *(Detail compressed 21 Aug 2026 under §0.5.)*

1. **CLOSED 16 Aug 2026, sixteenth session — the loose ends the account model
   left are all tied off.** a and c went that session, b was superseded by
   step 0b, and d, e and f were already done.

   **The one thing worth carrying forward: `CREATUSR` is gone**, including the
   `struct PCFG` field. Removing a `config.h` field means
   **`rm -f gplobj/*.o` before `make sd`** — the Makefile tracks no header
   dependencies, so every field after the removed one shifts and stale objects
   read the wrong offsets. §6 carries that trap.

   *(Detail compressed 21 Aug 2026 under §0.5.)*

2. **DONE 15 Aug 2026, tenth session (§4).** A VirtualBox guest served as the
   second machine: install byte-identical, all four counts matching, `COUNT VOC`
   431, and **the RDP refusal measured with a control**. §5.6.2 is complete.

   **THE RIG IS REUSABLE AND IS THE REASON THIS STEP IS NOT CUT TO ONE LINE.**
   VM `Windows 11 Clone`, snapshot `Before SD install`, NIC **bridged** — NAT
   cannot be used, since the host must open a connection *to* the guest.
   Bridging over the WiFi adapter worked here, which is not guaranteed; the host
   ARP entry carrying the VM's own MAC is how to tell it is working before
   blaming anything else. Files reach the guest through
   `VBoxManage sharedfolder add --transient --automount`, which needs no guest
   credentials — **do not drive the guest with `guestcontrol`**, which does.
   Read §6's two RDP traps first; between them they cost most of an hour.

   **AND IT IS THE RIG THE ONE REMAINING NETWORK CLAIM NEEDS.** Nothing has ever
   crossed the network to the API port — every measurement has gone to
   `127.0.0.1:4243`. This is how that gets settled.
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
     hidden by `Check: SshServerAbsent` on this machine (§4 Not verified). **It
     is no longer a subtask**: renamed `limitssh` and promoted on 16 Aug 2026
     when its parent went (§5.9). *Pointer corrected 21 Aug 2026: this said
     "header item 1", and that header was archived.*
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
4. **CLOSED — BUILT AND VERIFIED 16 Aug 2026, thirteenth session**, on the
   12:18:42 install. The audit trail: `audit_message()` in `k_error.c`, reached
   from BASIC as `kernel(K$AUDIT, text)` (key 57, `keys.h` and `INT$KEYS.H`).
   Every login, refused login, `LOGTO` and refused `LOGTO` is recorded with
   user, uid, pid and reason. `LOGIN` writes its record at the single point a
   login has succeeded, and `terminate.connection` writes every refusal, so a
   refusal added later is recorded whether or not its author thinks about the
   trail. The file is `sdsys/audit`, ACL'd append-only for `sdusers` by
   `secure-audit.ps1` — that ACL is the whole of the protection.

   *(Detail compressed 21 Aug 2026 under §0.5; the record is in HISTORY,
   16 Aug, and in the archive entry of 21 Aug.)*

5. **CLOSED 16 Aug 2026, fourteenth session — (f) included.** `GPL.BP/GRANTA`
   serves **`GRANT <account> TO <user>`**, **`REVOKE <account> FROM <user>`**
   and **`LIST.GRANTS <account>`** from one program behind three
   `VOC_TEMPLATE` entries; bare `GRANT <account>` lists too. `!os_group` gained
   `LISTMEM`. Watched reaching the audit trail at 14:48 from an unelevated
   session that had entered SDSYS, with the Windows group edited and correctly
   reverted.

   **`ACC$USERS` is gone and field 4 is NOT REUSED** — records written 13–14 Aug
   still carry a grant list there, and an installed tree is never upgraded.
   That is the one thing here that constrains future work.

   *(Detail compressed 21 Aug 2026 under §0.5.)*

6. **CLOSED 17 Aug 2026, nineteenth session — THE API WORKS END TO END**, and
   **Phase 1 on 21 Aug 2026 changed what it exposes**. Verified originally by
   `verify-apiport.ps1 -Prefix sdapi2` against the 16:5x install: a remote
   session opened over the port, **the wrong password refused by `!CRED_VERIFY`
   and SDSYS refused by the `ACC$GROUP` test**, with different messages — which
   is what makes the admitted case mean anything.

   **TWO CLAIMS THIS STEP CARRIED ARE NOW FALSE, and they are corrected rather
   than left to mislead.** It said the transport was *"loopback TCP with ssh
   carrying it (posture B)"* and that *"`APIPORT` defaults off"*. Phase 1
   reversed both on the owner's decision of 21 Aug 2026: the listener binds
   `INADDR_ANY`, `APIPORT=4243` ships **active**, and the installer opens a
   firewall rule. §8 has the reversal; the header has the measurements.

   **What still holds from this step:** the listener lives in `sdwind`; an
   account needs `$cred` **and** `sdapi` membership; `!CRED_VERIFY` and the
   `ACC$GROUP` test are the two gates, and they answer differently on purpose.

   *(Detail compressed 21 Aug 2026 under §0.5; SCRAM superseded the cleartext
   login on 20 Aug and the containment gate landed on 21 Aug — both have their
   own HISTORY entries.)*
7. **CLOSED — BOTH HALVES. `SH` AND `OS.EXECUTE` ARE PERMITTED BY A LIST, NOT BY
   ELEVATION.** The BASIC half landed 17 Aug 2026 and the C half on 19 Aug;
   `verify-osusers.ps1` **24/24** on the 16:38:01 install. §4 has the four-row
   `SH` table and what each row is for.

   ***"WHAT IS NOT DONE, AND IT IS HALF THE FEATURE" STOOD HERE UNTIL
   21 Aug 2026 AND WAS TWO DAYS STALE WHEN THE PHASES BEGAN.*** It said field 2
   `OS.EX` was "stored, dictionaried and read by nobody" and that gating it
   needed C. **That C was written on 19 Aug** — `os_permitted()`, `op_sh.c:150`,
   called at `:209`. The same claim had propagated into §4 and §8 and is struck
   in all three places.

   **THE PROBLEM IT SOLVED (§8).** The gate at `CPROC`'s `os.command:` label
   admitted only `K$ADMINISTRATOR`, which is `IsElevated()`, and an ssh session
   can never be elevated — so programmers, the one group that needs a shell,
   were the one group that could never have one, while `OS.EXECUTE` stayed
   ungated for everybody. The visible control was denied to the people who
   needed it and the capability it guards was open to those who did not.

   **WHAT WAS BUILT:** `@SDSYS/OS.USERS`, a directory file, **one record per
   account**, keyed by account name. Field 1 `SH`, field 2 `OS.EX`, each `yes`
   or anything else. Dictionary `OS.USERS.DIC` shipped as source in
   `gplbld/FILES_DICTS` and written at bootstrap by `WRITE_INSTALL_DICTS`.
   **Both files are staged empty by `stage.py`, and that is load-bearing** —
   `WRITE_INSTALL_DICTS` `OPENPATH`s the dictionary rather than creating it, so
   an unstaged file would ship with no dictionary. Admin edits with `ED` from
   SDSYS. Message 10053.

   **THE C GATE HAS THREE WAYS IN, and the first is what keeps `SH` working.**
   `HDR_INTERNAL`: the `SH` verb reaches the OS by `CPROC` itself calling
   `os.execute`, so in C the verb and the statement are the same code and cannot
   be told apart. `CPROC` is `$internal` and has already applied the finer rule,
   so trusting the marker leaves `SH` unchanged — **and it cannot be forged**,
   because `BCOMP:2864` honours `$INTERNAL` only for a session that is itself
   internal **and** elevated. Then an elevated session, and `OS.USERS` field 2.
   Checked rather than assumed: all 13 programs in the shipped tree that call
   `os.execute` are `$internal`.

   **THE TRUTH TABLE IS WHAT MAKES IT EVIDENCE** — a gate that refused
   everything, or read field 1 by mistake, could not produce it:

   ```
   unlisted            SH refused    OS.EXECUTE refused
   SH=yes OS.EX=no     SH RUNS       OS.EXECUTE refused
   SH=no  OS.EX=yes    SH refused    OS.EXECUTE RUNS
   elevated            SH runs       OS.EXECUTE RUNS
   ```

   **The middle two rows are one record each, read in one session, and they are
   the whole proof that the two fields are independent.** Note `SH` implies
   `OS.EX` and cannot not (`CPROC:3465`); the useful combination is the third
   row — programs may shell out, the person at the prompt may not.

   **THE ACL IS THE ENTIRE CONTROL.** `gplbld/secure-osusers.ps1` grants
   `sdusers` **(RX) — read, not modify**, which is the difference from
   `secure-cred.ps1`: `CPROC` reads the list from the user's own process, so
   they must read it and must never write it. Called from `[Code]` as
   `SecureOsUsers`, **exit code checked**. Without it any SD user adds their own
   name and the file is decoration — exactly what happened to `$CRED`.

   **ELEVATION STILL PASSES ON ITS OWN**, deliberately: an empty `OS.USERS` must
   not lock the machine's own administrator out of `SH`. **The metacharacter ban
   is lifted for a listed account only**, so an elevated session that is not
   listed keeps `!valid_shell_cmd` exactly as before.

   **NOT IN `NEWVOC`, and that was reconsidered mid-design.** Everything in
   `NEWVOC` is copied into every account's VOC unless excluded in **two** places,
   and the tier lists' fail-safe is *permissive* — a missing record means the
   full VOC. **A permission list needs the opposite default** and must not
   inherit that convention.

   **TWO THINGS FOR WHOEVER TOUCHES THE VERIFIER.** It runs unelevated and
   **prompts for UAC twice itself**: the measurement must not be elevated or
   `CPROC:3448` admits it on `K$ADMINISTRATOR` and `OS.USERS` is never consulted,
   while writing the record and removing it again must be. And **a new verifier
   must go on `assert-current`'s `$neverShipped` list**, or it reports the tree
   stale because it exists and then refuses to run on the strength of its own
   newness.

   **A form for account setup with these privileges belongs to the GUI
   utilities, which are a SEPARATE PROJECT** - owner, 23 Aug 2026, §5.14 and
   §7 step 10. `ED` from SDSYS is the editor here and is not an interim
   measure any more.

8. **CLOSED 22 Aug 2026 - BOTH HALVES.** (§5.12) The file-name half was done
   and measured earlier; **the account-name half landed 22 Aug** - `CREATEA`
   downcases the register key, `adopt-account.ps1` follows, and the shipped
   `accounts/SDSYS` record is renamed `accounts/sdsys`. Confirmed on the
   19:38:32 install: `LIST ACCOUNTS` shows `don` and `sdsys`, matching
   `user_accounts\don` and `sdu_don`. `verify-createaccount` every row and
   `verify-accountrules` 34/34. **It was three lines, not the five-program
   refactor this step feared** - the lookup is case-insensitive on NTFS and
   displayed names upcase at the point of use, both measured. See
   §WHAT THE FORTIETH SESSION LEAVES item 2. §5.12 carries what
   moved, what was left deliberately, the four traps for anyone scripting a fold
   again, and the two instruments that are not obvious — read it before the next
   rename rather than re-deriving any of it here.

   *(Working detail compressed 21 Aug 2026 under §0 rule 5 — the
   `CASE_INSENSITIVE_FILE_SYSTEM` analysis, the case-inversion investigation and
   its eight eliminated candidates are in HISTORY, "ARCHIVE 21 Aug 2026 -
   section 7's closed steps 7, 8 and 11".)*

   **DONE AND VERIFIED**, each on the install named in §5.12:

   - **The three-case fold — as typed, then down, then up** — at the 74 parser
     sites **and in `_VOC_REF`**, which every BASIC `OPEN` goes through and which
     had no fold at all. `verify-fold` 10/10. **It is additive**: with every id
     upper case the new attempt can never hit, so it changed no behaviour and
     could not break anything.
   - **Every name in the installed `sdsys` is lower case on disk**, and so is
     each account's `voc` — `verify-lcnames` 115/115. 2,968 files, 12 SDSYS
     directories, 73 record ids in `gplbld/FILES_DICTS`.
   - **792 TCL command ids**, plus `$savedlists`, `$hold`, and
     `bp`/`bp.out`/`gpl.bp`/`gpl.bp.out`.
   - **The tiers came through it unaffected** — `verify-tiers` 22/22.

   **THE TERMINAL HALF NEEDS NO WORK AT ALL**, which took a session to establish
   and is easy to re-open by mistake. Case inversion is **off** for every session
   a real user gets, and not because the C setters are dead: `LOGIN:266` does set
   it, and the VOC `login` paragraph — run at session start and again on every
   `LOGTO` — turns it off afterwards and wins. **The authoritative place to
   change this behaviour is the paragraph**, in `newvoc/login` and
   `voc_template/login`, not C and not `$LOGIN`.

   **WHAT IS LEFT, in the order it should be taken:**

   - **The account-name half**, which is the wide one: `LOGIN` 281, 321, 339,
     383, 690 and `CPROC` 2531, 2577, 2579, plus the audit lines 2601, 2619,
     3686 — about **11 sites**. Removing those `upcase()` calls is what makes
     `sue` and `SUE` one account, and the `$CRED` register is keyed the same way.
     **Sequencing matters**: case-insensitive *comparison* is what makes today's
     upcasing harmless, so removing the upcasing first would make them two
     accounts. **707 `upcase(` calls in `gpl.bp` are NOT all in scope** — most
     are VOC verb lookup, `Y`/`N` answers and record types, which must stay.
   - **The dictionary and VOC ids** that have not moved. `$COMMAND.STACK` is the
     **last control** `verify-lcnames` §3 owns — whatever moves it must bring a
     replacement, or §3 can no longer tell a rename from a sweep.
   - **`$COMO` is deliberately still upper case**: `COMO:44` and `PHANTOM:59`
     define the on-disk name and the VOC id with the same `$define`, so splitting
     them is `CREATEA`'s `fn`/`os.name` pattern again — and nothing in `gplbld`
     drives `COMO`, so it would ship unmeasured.

   **A SEPARATE REAL DEFECT, FOUND ON THE WAY AND NOT FIXED: `SET_PASSWD`'s
   case-inversion save/restore can never restore On.** `op_pterm` returns the
   **new** value, and a **negative** argument is what reports without setting, so
   `SET_PASSWD:88` `was.inverted = pterm(PT$INVERT, @false)` saves the *off* it
   just wrote and `:98` restores that. The fix is to read with
   `pterm(PT$INVERT, -1)` first, then set. **Harmless today only because
   inversion is already off everywhere** — latent, and ours (the lines carry a
   `14 Aug 26 Windows port` marker), so no `UPSTREAM_FIXES.md` entry.
9. **CLOSED AND MEASURED, 22–23 Aug 2026.** A scheduled job can log in and run
   a command the administrator has named for its account. **`verify-batchjob`
   10 of 10 decisive on the 23:46:31 install**, and the three rows that carry it
   are *listed: the paragraph RAN*, *ELEVATED with no entry: still runs* and
   *entry removed: refused again* — the five refusals prove nothing without
   them. ***An ordinary token cannot WRITE `batch.jobs`*** is the whole of the
   control, and it is a row too.

   **TWO THINGS §8 SPECIFIED TURNED OUT TO BE WRONG, both measured before
   changing anything, and both are the reason this was not a half-hour job.**

   a. ***"IT NEEDS NO NEW C CODE" WAS FALSE.*** `sd <command>` was gated on
      `check_admin()` (`sd.c`), and **a scheduled task is not elevated**, so it
      never reached `LOGIN` at all. Measured: `sd COUNT VOC` from an ordinary
      shell answered *"This command needs an elevated session"*, exit 1.
      **Owner's decision, 22 Aug 2026, from three offered: the gate moves to
      `LOGIN` and becomes a list — step 7's shape.** Elevation still passes on
      its own, so nothing an administrator does today changes; an account with
      the command on its list passes too; everyone else is refused as before,
      by `LOGIN`, with a message saying which.
   b. ***THE LIST CANNOT LIVE IN SDSYS's VOC***, which is where §8 put it.
      **`sdsys\voc` grants `sdusers` Modify** — measured 22 Aug by writing a
      file into it from an ordinary token — and **a VOC record cannot carry an
      ACL of its own**, so the list would have been decoration, which is
      exactly what happened to `$CRED`. It is **`@SDSYS/batch.jobs`**, a
      directory file, **one record per account**, one command name per line
      (value marks are read too, because the dictionary describes `COMMAND` as
      multivalued and `ED` invites one per line). **Locked read-only to
      `sdusers` by `secure-osusers.ps1`** — the same script, which takes
      `-Path` and was never os.users-specific — called from `[Code]` as
      `SecureBatchJobs` with the exit code checked.

   **WHERE THE GATE IS:** `LOGIN`'s `batch.permitted`, reached from the block
   immediately before the success audit, so **a refusal leaves through
   `terminate.connection` and is written to the audit trail with a reason**
   without a second call site. The audit record now names the command when
   there is one. `CPROC` does not pick the command up until its single-command
   branch, which is after the whole login paragraph — **nothing has run when
   the gate decides.**

   **THE CONSTRAINTS FROM §8, AND WHAT EACH BECAME:** one token and no
   arguments — enforced, and it is the line doing the security work; `PA` and
   `S` VOC types only — enforced on the leading characters of field 1, because
   a type code may be followed by prose (`File for BASIC programs` is how
   `CREATEA` writes a file pointer); unique across the list, or `-A` must match
   — **free by construction**, since the record is keyed by `initial.account`,
   which is already what `-A` set; `@logname` — **not touched, and that needs
   checking on the cycle**: a batch logon has a real Windows user behind it, so
   the "no person" case §8 anticipated may not arise.

   **STILL OPEN, and it is §8's own "any prompt is fatal":** nothing here stops
   the *command itself* prompting. A paragraph that asks a question will sit
   there. The list limits what may run, not what what-may-run does.

   **THE INTERACTIVE PATH IS UNTOUCHED** — only `SYSTEM(1026)` is gated — and
   that is load-bearing rather than incidental: `verify-batchjob.ps1` plants
   and removes its own VOC probes through a piped session, because doing it
   with `sd DELETE VOC x` is the very thing being measured.
10. **REMOVED FROM THIS PROJECT — owner, 23 Aug 2026.** It read *"write the
    admin helpers (§5.14) — forms over the administrative work that is command
    lines and hand-edited records today"*. **The forms will be part of a set of
    GUI utilities that will be created, and they are not necessary for a working
    SD**, so they are not this repository's to build and their absence is not a
    gap in it.

    **THE SEQUENCING RULE IS NOT REMOVED WITH THEM — §5.14 keeps it, and it is
    now load-bearing rather than convenient.** Administrative logic goes in a
    subroutine with a verb over it, because a utility outside this repository
    can call a catalogued subroutine or the API and can do nothing with logic
    buried inside a verb. **The step went; the constraint on how everything else
    here is written did not.**

    **ONE DANGLING POINTER IS LEFT ON PURPOSE.** `gpl.bp/LOGIN:890` still says
    *"until there is a verb to edit the list with (step 10)"*. It is a comment,
    and correcting it means a source change, which makes the installed tree
    stale and costs a whole cycle — on a tree that had just gone 27 of 27.
    **Fix it the next time `LOGIN` is edited for a real reason**, and read it
    meanwhile as "until the GUI utilities exist".
11. **CLOSED — `SDConnectLocal()` CARRIES A SESSION.** Verified on the 12:28:49
    install of 17 Aug 2026: `make check-local` on the installed pair,
    `assert-current` exit 0, `WHO -> 2 DON`. Five runs in all, four in
    development and one on the install, exit 0 each time.

    *(Compressed 21 Aug 2026 under §0 rule 5. The named-pipe attempt, the
    transport options as they were framed, and the diagnosis in the order it
    happened are in HISTORY, "ARCHIVE 21 Aug 2026 - section 7's closed steps 7,
    8 and 11". Two stale headings — "AND NOT RUN", then "CALLED, AND IT DOES NOT
    WORK" — were struck from this step on 21 Aug; both had been refuted by this
    step's own body.)*

    **`SDConnectLocal()` AS ORIGINALLY WRITTEN COULD NEVER HAVE WORKED**, on
    this platform or any other, and it took three independent faults with it.
    **All three still matter to any successor:**

    a. **The client and the server disagreed about `-C`.** The client built
       `sd.exe -Q -C <pipename>` with the name as a SEPARATE argument, while
       `sd.c` parsed `sscanf(argv[arg], "-C%d!%d", …)` and `exit(1)`ed on
       anything else. **The same mismatch is in `sdb64`, byte for byte** —
       `UPSTREAM_FIXES.md` #4. `sd.c` now takes either form and **consumes the
       name argument**, which it must: the option loop stops at the first
       argument not beginning with `-`, so the name would otherwise be taken for
       a command to execute.
    b. **The client looked for `sd.exe` inside the DATA tree.** It is now found
       **beside the DLL** through `GetModuleHandleEx(FROM_ADDRESS)`, which needs
       no configuration and follows the install wherever `{app}` puts it.
       **The path is quoted too**: it is under `C:\Program Files`, and an
       unquoted spaced path in `CreateProcessA` with a NULL application name
       makes Windows try `C:\Program.exe` first — a hijack, not just a bug.
    c. **The access argument to `cygwin_attach_handle_to_fd()` must MATCH THE
       HANDLE**, not describe what the descriptor is for. Passing `GENERIC_READ`
       for descriptor 0 — the obvious thing to write — **succeeds**, and the
       descriptor then fails `read()` with `EBADF`.

    **WHAT THE TRANSPORT IS NOW: two anonymous pipes handed to the child as its
    STANDARD HANDLES**, so Cygwin builds descriptors 0 and 1 itself and its
    `PeekNamedPipe`-based `select()` answers honestly. **The command line is
    `-Q -C1!0`, and the order matters** — `sd.c` does `dup2(RxPipe, 0);
    dup2(TxPipe, 1)`, so rx must be 0 and tx must be 1. An earlier note in this
    file said `-C0!1`; it was wrong. **Inheritance is restricted to exactly
    those two handles** with `PROC_THREAD_ATTRIBUTE_HANDLE_LIST`, because plain
    `bInheritHandles = TRUE` copies every inheritable handle the process owns
    into a long-lived `sd.exe`, and this library is loaded into somebody else's
    application.

    **WHY THE NAMED PIPE WENT, and it is not a bug left to find:** a descriptor
    made by `cygwin_attach_handle_to_fd()` is reported **permanently ready** by
    `select()`, so `sdpoll()` spins and `sd.exe` never answers — §6 has it.
    **Do not spend another cycle looking for a flag**; six combinations of the
    name and access arguments, `O_NONBLOCK` and `F_SETOWN` were all measured.
    `gplsrc/win32pipe.c` stays but has left the hot path, and `sd.c`'s
    `-C <pipename>` branch now **refuses with a diagnostic** rather than hanging,
    because silent-and-never-answering is the worst thing to leave callable.

    **THE FRAMING THAT WAS WRONG, kept because it is the reusable part:** the
    peer identity never came from the pipe. `SDConnectLocal()` gets identity
    because it **spawns `sd.exe` with `CreateProcessA`**, so the server is a
    child running under the caller's own token. The pipe only carries bytes —
    which is why the socket option's stated cost and the named pipe's stated
    benefit were both illusory. §8 has where peer identity actually comes from
    (`GetExtendedTcpTable`).

    **RE-RUN IT AFTER ANY CYCLE, UNELEVATED:**

    ```sh
    cd sdb_ai/sd64 && make check-local
    ```

    **It carries its own control, and that is the reason to trust it:** `DON`
    admitted, `SDSYS` **refused** with *"User not allowed in requested account"*
    — the `ACC$GROUP` grant check running. `DON` succeeding alone would prove
    nothing, since a check that never ran would admit it too. Exit codes say
    which happened: 1 `DON` refused, 2 `SDSYS` admitted (so the check did not
    run and the first result is worthless), 3 the session opened but `WHO`
    failed. **It is deliberately NOT in `make check`** — everything there runs
    without a server; this measures the installed tree and is subject to the
    cycle rule.

    **`strace` IS THE TOOL FOR ANYTHING THAT PRINTS NOTHING AND EXITS NOTHING.**
    `/c/msys64/usr/bin/strace.exe`, works on any Cygwin binary including
    `sd.exe`, and it answered in one run what three cycles could not. There is no
    `gdb` in this MSYS2 install.

    **The vendored client's own docs were wrong and are corrected**: both
    `README.md` and `USER_GUIDE.md` said the Windows DLL does not provide
    `SDConnectLocal` and that it is "Linux-specific". It is exported — ordinal 6,
    checked with `objdump -p`.
12. **REWRITTEN ON THE OWNER'S RULING, 21 Aug 2026. DO NOT RESTORE THE
    BRANCHES.** This step used to read *"Restore the BASIC layer's Windows
    branches from the external `GPL.BP` tree, then set `SYSTEM(91)` to 1 and
    assign `is_nt`"*. **There should be no Windows branches in this version of
    SD, because it is Windows only** — the same rule CLAUDE.md already states
    for the C code (*"do not add `#ifdef` branches to keep Linux building —
    replace Linux code outright"*), now stated for the BASIC layer.

    **A branch implies a non-Windows arm to fall back to, and there is none.**
    So the work is: **take the Windows arm from the external tree, drop the
    conditional, and delete the Linux arm.** `if windows then '\' else '/'`
    becomes whichever separator this port actually wants — decided on its
    merits, not by a platform test.

    **THE SWITCHES ARE DEAD WEIGHT UNDER THIS RULING, not a thing to turn on.**
    `SYSTEM(91)` already answers **1** (`op_sys.c:282`, 17 Aug 2026, flipped to
    fix case-insensitive `@ID` matching — §5.4). `SYSTEM(1006)`/`is_nt` has
    **no reader at all** in the shipped BASIC tree. A constant that is always
    true does not need testing.

    **SURVEYED AND ACTED ON, 22 Aug 2026, forty-second session. THE SOURCE IS
    `C:\Users\dmont\Projects\GPL.BP`** — 212 files, **25 carry platform
    references**, and **10 of those do not ship here at all** (`VBSRVR`,
    `ADMSRVR`, `SETQ`, `LGNPORT`, `PASSWD`, `QMPKG`, `CREATEU`, `ADMUSER`,
    `ACCRST`, `DELUSER`). **The idiom is a bare `windows`**, set by
    `windows = system(91)` (`CPROC:251`, `LOGIN:91`) — *not* `is.windows`,
    which is why grepping for that finds nothing and looks like the logic is
    gone.

    **ONE LIVE DEFECT, AND IT WAS THE WRONG ARM RATHER THAN A MISSING ONE.**
    `PARSER` split every TCL token at the first backslash: upstream guards that
    line with `if not(is.windows)`, and the port **kept the Linux body and
    dropped the guard**. **Measured, not read** — `RUN BP C:\Temp\zznosuch`
    answered *"Program BP.OUT **C:** not found"*, while `C:/Temp/zznosuch` and a
    bare name came through whole. `RUN` is the instrument because message 5073
    echoes both names it was given; `COUNT` does not, and `@parser` cannot be
    called from a probe program because `!PARSER` is `$internal`. **The
    reachable case is `CREATE.ACCOUNT OTHER <name> <path>`**, which takes its
    pathname through the parser at `CREATEA:466`. Fixed by deleting the split.
    **`sdb64` has the same unguarded line** (`sd64/sdsys/GPL.BP/PARSER:116`)
    **and it is correct there** — that tree is Linux-only, so no
    `UPSTREAM_FIXES.md` entry.

    **MEASURED ON THE INSTALLED TREE, 22 Aug 22:50:18, and guarded from now
    on.** `gplbld/verify-parsertokens.ps1` is new, **7 of 7 decisive**, and it
    is in `VerifyInstall1` because it needs no elevation and spends no prefix.
    **It asks two questions, not one:** the backslash path must come back whole
    **and** `CT VOC a,b` must still split into `a`, `,`, `b` - without the
    second, a `CT` that never reached the parser would pass just as happily with
    the defect restored. **`CT` and not `RUN`, and that is not a preference:**
    `RUN` echoes both names only once the account has an object part to look in,
    and on a freshly made account nothing has been compiled, so it answers
    *"Cannot find item to run"* and echoes nothing. That is how the original
    instrument stopped working between two installs on the same day.

    **ALSO DONE:** `QPROC`'s `is.windows` is gone — `system(91)` is a constant
    1, so `if is.windows and is.dir` tested something that could not vary; and
    `CREATEA`'s `USRDIR`/`GRPDIR` fallbacks were `/home/sd/...`, replaced with
    the paths `config.c` already defaults to.

    **WHAT WAS DELIBERATELY NOT TAKEN, each judged against this port's own
    decisions rather than by platform test:**

    - **Every `upcase()` Windows arm** — `LOGIN` 305, 433, 445, `CREATEA` 128,
      169, `CPROC` 2222. §5.12 went the other way on purpose, and `CPROC`'s is
      superseded outright by the three-case fold at `CPROC:2253`–`2255`.
    - **`CPROC`'s `dir.separator` stays `/`** (`CPROC:290`; upstream
      `= if windows then '\' else '/'` at `:323`). `@ds` is SYSCOM slot 57 and
      compilation depends on it — `BCOMP` opens `@sdsys:@ds:'bin'` — and `/` is
      what works on the MSYS2 runtime, so the burden is on changing it.
    - **`CONFIG` keeps printing `SH`, `SH1` and `SPOOLER`** (upstream hides them
      on Windows, `CONFIG` 136, 143). **This port has a real `SH`** — step 7 —
      and all three are live in `config.h`/`op_config.c`, so the upstream arm
      would hide settings that work here. **Do not "restore" it.**
    - **`CREATEA`'s `@DRIVE` flash-drive branch** (`CREATEA:218`). The installer
      pins `C:\Program Files\SD` and no longer offers a location at all, so a
      relocatable install is not a thing this port has.
    - **`LOGIN`'s forced administrator rights** on any console session, which
      **§5.6 rejects on purpose**.
13. **DROPPED AS A MIGRATION — owner's decision, 23 Aug 2026.** It read
    *"Stage 2, native Win32"* and it is not being done. **What replaces it is
    steps 14 and 15 below**, which are the two outcomes it was ever for.

    **THE QUESTION THAT ENDED IT, and it is the right one to ask of any
    remaining Linux-ism:** *"is this conversion really necessary — the system
    seems to work fine with Cygwin dependencies."*

    ### Why it went, in the order the reasons matter

    **1. IT WAS NEVER ABOUT REMOVING CYGWIN.** Read what this step actually
    claimed for itself: *"the service-account model in §5.7 belongs here, and
    until it lands the data tree is not genuinely private from SD's own
    users"*; §8's tiers entry, *"until §5.7's service model, every tier is
    enforced by the user's own Windows token"*; and the installer's own first
    page, *"SD users are not isolated from each other"*. **The objective was
    user isolation and a private data tree. Dropping MSYS2 was an assumed
    route to it, never the goal** — and the route was never checked against
    the goal until it was queried.

    **2. IT IS NOT REQUIRED FOR EITHER OUTCOME.** Win32 calls work from an
    MSYS2 build and **this tree already makes them** — `win32sem.c`,
    `win32peer.c`, `win32pipe.c`, `win32audit.c`, `linuxlb.c`. The API
    session's LocalSystem token was never blocked by the runtime: it is
    blocked by **SCRAM authenticating in the CHILD, after `execl`**, so
    `sdwind` does not know the caller at spawn time. That is an architecture
    question. §5.7's service model likewise needs `CreateProcessAsUser` **at
    particular sites**, not a runtime swap.

    **3. WHAT MSYS2 COSTS IS REAL, KNOWN, AND ALREADY PAID.** The `/dev/shm`
    `etc/fstab` mapping (§6); AF_UNIX invisible to native Windows (§8, which
    killed the Linux client contract); Cygwin pid ≠ Windows pid (`K_WINPID`);
    the dual `C:/` and `/c/` namespace (`K_WINPATH`, `net_normalise`);
    `select()` permanently ready on an attached handle (§7 step 11); shipping
    `msys-2.0.dll` under the two-components rule (§5.8); and the tty layer,
    which is what leg 1 hit. **Every one is documented and worked around, and
    none of them is breaking the product.**

    **4. AND THE RISK PROFILE IS THE WRONG SHAPE.** The legs land on the
    console, the terminal, shared memory and process creation — ***precisely
    the paths the 26-verifier suite structurally CANNOT test***, because every
    verifier drives SD down a pipe. **High blast radius, no automated
    coverage.** Leg 1 was the mild version of that and it still shipped a
    cleartext password prompt; SYSSEG would not have been mild.

    ### What leg 1 cost, kept because it is the evidence for the decision

    `linuxio.c`'s six termios calls were converted to the Console API on
    23 Aug 2026 and **reverted the same day**. The installer's post-install
    prompt **echoed the password in cleartext**, printed its stars afterwards
    a whole line at a time, and froze without asking for the confirmation.

    ***`SetConsoleMode` IS AVAILABLE UNDER MSYS2, NOT SUFFICIENT.*** Cygwin's
    tty layer sits in front of the console and implements termios **in
    userspace** — canonical line buffering and echo are **Cygwin's**, not the
    console driver's. Removing `tcsetattr` left Cygwin echoing and
    line-buffering.

    ***AND THE INSTRUMENT COULD NOT HAVE CAUGHT IT, BECAUSE ITS CONTROL WAS
    CONTAMINATED.*** `probe-console.c` calls `tcsetattr(raw)` at step 3 and
    never undoes it, so every later reading was taken with **Cygwin already in
    raw mode**. It proved `SetConsoleMode` sticks and does not disturb key
    delivery — both true — and never observed what `SetConsoleMode` **alone**
    does, which was the question that decided the leg. **"Can I set this?"
    answered in place of "is this sufficient?"** The caveat is now the first
    thing in that file, above its own verdict logic.

    **TWO MEASUREMENTS SURVIVE AND ARE WORTH KEEPING** if a flip is ever
    forced for some other reason:

    - **The console mode SD actually wants is `0x2e8`** — line input off, echo
      off, **processed input off**, virtual-terminal input on. It is what the
      console is already in and what Cygwin's `tcsetattr(raw)` leaves it at.
    - ***Processed input must be OFF, and that is a fact about SD rather than
      about Cygwin.*** `linuxio.c` sets `ISIG`, so the obvious conversion turns
      it on and breaks the break key: **SD handles break in software**,
      comparing the incoming byte against `tio.break_char` and calling
      `break_key()`. The byte has to reach SD. `set_term()`'s `trap_break` has
      always been a software flag; only the termios call made it look
      otherwise.

    ### The survey, kept because it is what the successor needs

    **Counts are code lines with comment lines excluded** — the first pass of
    this table said `sys/cygwin.h` was 14 calls and it is **6**, the rest being
    the comments explaining them. **A raw `grep -c` is not a measurement here.**

    | leg | measured |
    |---|---|
    | `fork` → `CreateProcess` | **5 sites**, `op_kernel.c:701`, `op_sh.c:379`, `sdwind.c:491`, `sysseg.c:643`, `sysseg.c:745` — **every one fork+exec**, none needs copy-on-write |
    | `termios` | **11 sites, 2 files** — `linuxio.c` 6 (session terminal), `lnxport.c` 5 (**serial ports**, a different Win32 API and no verifier drives it) |
    | passwd/group | **22 sites, 5 files** — `linuxlb.c` 14, `ingroup.c` 3, `op_dio2.c` 3, `linuxio.c` 1, `sdext_eguid.c` 1 |
    | `sys/cygwin.h` | **6 sites, 3 files** — `cygwin_conv_path` ×2, `cygwin_internal` ×2, `cygwin_attach_handle_to_fd` ×2 |
    | POSIX shm + semaphores | **17 sites, 6 files** — `sysseg.c` 6, `sdsem.c` 3, `sdidx.c` 2, `sdwind.c` 2, `win32sem.c`/`.h` 4. **This is SYSSEG** |
    | `select()`/poll semantics | §7 step 11 measured the difference |

    ***THE `sys/cygwin.h` SIX WOULD DELETE THEMSELVES AT A FLIP RATHER THAN
    NEEDING CONVERSION*** — `K_WINPID` becomes `getpid()`, `K_WINPATH` becomes
    the identity function, and `net_normalise()` folds a dual namespace that
    does not exist natively. **Do not "convert" them early**: `net_normalise()`
    is inside the API containment gate, the only thing in front of a
    LocalSystem session, and hand-rolling a native fold while `getcwd()` still
    answers `/c/...` would either duplicate the runtime or break the gate.

    **The toolchain flip itself was never the hard part** — `UCRT_CC` is wired
    in the Makefile and `sdclilib`, `sdsvc` and the check probes already build
    native.

14. **The API session's identity.** `sdwind.c:491` `fork()`s the session, so it
    inherits the service's LocalSystem token. **What 22 Aug measured was REACH,
    not identity** — the `op_dio2.c` containment gate holds over the network.
    §THE FILE HALF IS CLOSED, and §What fixing it involves.

    ***IT CANNOT BE FIXED AT THE FORK, and that is the thing to know before
    planning it.*** The SCRAM exchange happens **in the child, in `APISRVR`,
    after the `execl`**, so at spawn time `sdwind` does not yet know who the
    caller is. Two shapes, and it is a decision rather than a discovery:

    a. **Authenticate in `sdwind` first, then spawn as the user.** Moves SCRAM
       out of BASIC into C — the larger change, and it relocates the one piece
       of security logic currently readable as BASIC.
    b. **Let the session take the token after it authenticates.** SCRAM means
       **the server never holds the password**, so `LogonUser` is not
       available; only **S4U**.

    ***THE PROBE IS RUN, 23 Aug 2026, AND SHAPE (b) IS AVAILABLE.***
    `gplbld/probe-s4u.c`, driven by `probe-s4u.ps1`; §S4U IS MEASURED has the
    table and the three corrections. From **LocalSystem** the S4U token comes
    back at **Impersonation** level and `CreateProcessAsUser` **works** — the
    child's own `whoami` read `gitorli\test1`. From `don`, elevated or not, it
    is Identification and refused. **`SeTcbPrivilege` is the discriminator**:
    it gates `LsaRegisterLogonProcess`, and the trusted LSA connection is what
    raises the level.

    **TWO SHAPES OF (b), AND THE PROBE MEASURED BOTH.** The session can be
    **re-spawned** with `CreateProcessAsUser`, or — much smaller — it can
    **impersonate in place**: `ImpersonateLoggedOnUser` on the S4U token
    worked and could open a file. ***BUT IMPERSONATION IS PER-THREAD AND DOES
    NOT REACH BACKWARDS***: handles already open keep the access they were
    opened with, and any thread that did not impersonate is unaffected. In
    `sdwind`'s child that is most of the process.

    **WHAT IS STILL A DECISION, AND IT IS THE OWNER'S:** (a) moves SCRAM into
    C and spawns as the user; (b) keeps SCRAM in BASIC and takes the token
    afterwards, at the cost of a window between `execl` and the token change
    during which the session is LocalSystem. **The probe removed the unknown,
    not the choice.**

    ***THE SECOND UNKNOWN IS NOW MEASURED TOO, 23 Aug 2026, AND SHAPE (b)
    SURVIVES IT.*** `gplbld/probe-impersonate.c` + `.ps1`, as LocalSystem via
    `schtasks`, target `test1`. **`ImpersonateLoggedOnUser` DOES govern the
    MSYS2 runtime's `open()`** — which is how SD opens every data file
    (`dh_file.c:815` `OpenFile()` calls POSIX `open()`), and the thing nobody
    had tested. It was the last thing that could have killed (b) outright.

    | leg | result |
    |---|---|
    | control A, as LocalSystem | both files **OPENED** |
    | while impersonating `test1` | allowed **OPENED**, forbidden **refused, errno 13** |
    | control B, after `RevertToSelf` | forbidden **OPENED** again |

    **Identity by readback** — the thread token was queried and read
    `GITORLI\test1`. **And the control that matters is that `test1` is NOT an
    Administrator**, which `probe-impersonate.ps1` refuses to run without: the
    forbidden fixture grants Administrators, so an admin target would have read
    it anyway and the run would have reported a false negative.

    ***THE RECOMMENDATION, AND THE REASON IS NOT THE CRYPTO.*** Shape **(b)**.
    Shape (a) must replace `fork` + `dup2(conn,0/1)` + `execl` (`sdwind.c:491`)
    with `CreateProcessAsUser` **while handing a socket to an MSYS2 child as
    POSIX fd 0** — the least-charted part of the whole step, and unprobed.
    (b) does not touch the spawn path at all and has **one hook point**:
    `logged.in = @true` at `APISRVR:1442`, the single place SCRAM succeeds.

    **THE WINDOW IS NARROWER THAN THIS ENTRY IMPLIED.** Before `logged.in` the
    dispatcher admits **only requests 24, 25, 47 and 48** — 24 is retired and
    answers 5275, and 47/48 are the two halves of SCRAM. So the LocalSystem
    window contains **server-controlled code only**, not attacker-steered work.
    And a window is inherent either way: **SCRAM must read `$cred`, which is
    closed to everyone but SYSTEM and Administrators**, so the reader cannot
    already be the user.

    ***KNOWN LIMIT, UNCHANGED AND NOT MEASURED AWAY:*** impersonation is
    per-thread and **does not reach backwards**. Handles opened before the
    switch — the shared segment, `$cred` — keep LocalSystem access. What makes
    (b) work is that the account files are opened at `LOGTO`, which is *after*.

    **NEITHER NEEDS THE RUNTIME CHANGED.** That was step 13's assumption and it
    did not survive examination.

    ***SHAPE (b) IS CHOSEN AND BUILT - OWNER, 23 Aug 2026. BUILT IS NOT
    VERIFIED (§0 rule 2): IT HAS COMPILED AND NOTHING HAS RUN IT.***

    | part | where |
    |---|---|
    | S4U logon + impersonate | `gplsrc/win32s4u.c`, `.h` - new |
    | kernel key **61** | `keys.h` `K_ASSUME_USER`, `INT$KEYS.H` `K$ASSUME.USER` |
    | dispatcher, `$internal` only | `op_kernel.c`, beside `K_SET_USERNAME` |
    | the hook | `APISRVR` `vb.scram.final`, **before `logged.in = @true`** |
    | refusal | message **5277** |
    | link | `-lsecur32` in `L_FLAGS`; `win32s4u` in `gpl.src` |

    ***IT FAILS CLOSED, AND THAT IS THE WHOLE CONTROL.*** The call sits before
    `logged.in` is set, so a refusal leaves the caller authenticated into
    nothing - the dispatcher goes on admitting only 24, 25, 47 and 48. Setting
    `logged.in` first would leave a session that believes it is the user while
    holding the service's token, **which is worse than one that never started.**

    **`win32*.c` FILES NEVER INCLUDE `sd.h`**, and this cost a build: `sd.h`
    defines `Private`, `STRING`, `Sleep` and `GetCurrentProcessId` as macros and
    every one collides with `windows.h`, giving *"expected identifier or ( before
    static"* pointing at the project's own header. They take `windows.h` and
    their own header only, and use `malloc` rather than `k_alloc`.

    ***CYCLED AND RUN, 23 Aug 2026: INSTALL 21:25:18, `-Run b17` GREEN AT 10 AND
    17.*** All five API verifiers passed and **message 5277 appears nowhere in
    the log**. Because the hook fails closed that is a POSITIVE result:
    `AssumeUserIdentity` returned 1 on every live API login, so the S4U logon
    and `ImpersonateLoggedOnUser` both work in the real session.

    **THE RISK NAMED BEFOREHAND DID NOT MATERIALISE.** Nothing the session must
    write - `errlog`, `pstmp`, the audit trail - refused. Watched for, not
    merely absent. *Corrected 24 Aug 2026: this said "the session writes as the
    user after the switch", which `b28` disproved - it writes as
    `NT AUTHORITY\SYSTEM`. The absence of refusals is explained by that, not by
    the switch working.*

    ***MEASURED 24 Aug 2026 ON THE 23 Aug 21:25:18 INSTALL, AND THE EFFECT IS
    ABSENT.*** `gplbld/verify-apiidentity.ps1 -Prefix sdapiidb28`, run `b28`,
    `assert-current` exit 0. The call was already proven by `b17`; this is the
    consequence, and it is negative.

    ```
    ZZLOCAL (written by the local elevated session): GITORLI\don
    ZZAPI   (written by the API session)           : NT AUTHORITY\SYSTEM
    ```

    **The instrument is OWNERSHIP, not access.** A directory-type file stores
    each record as a real file, so the owner of a record is the OS identity
    that wrote it. `vb.write` (request 16, `APISRVR:900`) writes one from the
    API session; `COPY` writes the other from a local elevated session.
    **The two owners differing is the control** - it is what makes the API
    reading evidence rather than a statement about who owns the tree.

    **So `K$ASSUME.USER` fires, succeeds, and does not govern the file layer.**
    The hook is unconditional at `APISRVR:1472` and a false return jumps to
    `exit.vb.scram.fail` before `logged.in`, so a session that logged in ran it
    and it returned true. `win32s4u.c:184` refuses an Identification-level
    token rather than impersonating with one, and **nothing calls
    `RevertUserIdentity()` anywhere in the tree.**

    ***RE-TESTED FROM A FORKED CHILD, 24 Aug 2026, AND SHAPE (b) SURVIVES IT.***
    `gplbld/probe-impfork.c` + `.ps1`, as LocalSystem via `schtasks`, target
    `test1`. This section used to say the evidence was weaker than it read,
    because `probe-impersonate` was a **standalone** program started by
    `schtasks` while an API session is `fork()`ed and `exec()`d. **The two
    configurations behave identically** — both legs exit 11:

    | leg | forbidden while impersonating | created while impersonating |
    |---|---|---|
    | fork()ed and exec()d Cygwin child | refused, errno 13 | owned `GITORLI\test1` |
    | direct, started by cmd.exe (control) | refused, errno 13 | owned `GITORLI\test1` |

    Both legs run from one binary against one set of fixtures, so the only
    difference between the rows is how the process started. **The fork is not
    the explanation for b28.**

    ***AND THE SAME RUN CLEARED b28's OWN INSTRUMENT, WHICH IS WHY IT CARRIED A
    SECOND LEG.*** b28's control — a record written by the local session owned
    `GITORLI\don`, one written by the API session owned SYSTEM — is equally
    consistent with the runtime stamping a new file from its **own cached
    user**, which `fork()` carried in from the service and which the thread
    token does not touch. That would have made ownership the wrong instrument.
    **It was tested directly and it is wrong**: the Cygwin `uid` read **18
    (SYSTEM) throughout both legs** while the file created in the same breath
    came out owned by `test1`. **The POSIX uid does not decide the owner; the
    thread token does.** Ownership means what b28 took it to mean.

    ***SO THE FINDING SHARPENS WITHOUT A FURTHER MEASUREMENT.***
    `AssumeUserIdentity` succeeds at login (b17) and **the thread is no longer
    impersonating by the time the session writes** (b28 + this probe). The
    other branch — `ZZAPI` already existing, so the write changed no owner —
    is closed: fresh record name, and `verify-apiidentity.ps1:938` refuses the
    null case by requiring the file on disk.

    **NOTHING IN OUR TREE DROPS IT**, checked 24 Aug: `RevertUserIdentity()`
    has no caller (`op_kernel.c:284` withholds it from BASIC on purpose), there
    are **no threads** anywhere in `gplsrc`, and `sdext_eguid.c`'s `seteuid` is
    reachable only from `op_sdext.c:343`, an explicit extension call that is
    not on the login or write path.

    ***THE BISECT IS DONE, 24 Aug 2026, AND ONLY `fork()` DROPS IT.***
    `probe-impfork`'s Q3 leg performs, one at a time, what APISRVR does between
    the hook and the write, reading back the thread token **and** creating a
    file after **every** step. Both legs identical on all 14 rows.

    | step | token after | owner of file made after |
    |---|---|---|
    | `usleep`, `stat`, `open`/`read`/`close`, `opendir`, **`chdir`**, `getcwd`, `getpwuid`, `getpwnam`, **socket `send`/`recv`**, `select`, signal delivery, **`LsaDeregisterLogonProcess`** | `target` | `GITORLI\test1` |
    | **`fork()` + `waitpid`** | **NONE** | **`NT AUTHORITY\SYSTEM`** |

    **`LsaDeregisterLogonProcess` WAS TESTED BECAUSE THE PRODUCT DOES IT AND
    NEITHER PROBE DID** — `win32s4u.c:208`'s `exit_assume:` runs on the success
    path too (`ok = 1` falls into it), while both probes leak `hlsa`. It
    returns `STATUS_SUCCESS` and **the impersonation survives it**, so that
    difference is not the explanation either.

    ***THE `fork()` RESULT MATTERS BEYOND b28.*** It reverts the thread to the
    process token **silently**, so **any `PHANTOM` (`op_kernel.c:735`) or `SH`
    (`op_sh.c:379`) taken by an impersonated session drops it back to
    LocalSystem with no error**, and nothing in `win32s4u.c` can notice. Shape
    (b) owes an answer to this whatever fixes b28.

    ***RESOLVED BY (a2), 24 Aug 2026: THE SESSION FORKS, AND THE CALL SITE IS
    THE LOGTO GROUP CHECK.*** The earlier reading of this — "nothing on the API
    login-to-write path forks" — was wrong because it looked only for literal
    `fork()` in C. `is_grp_member` is BASIC calling `!ps_script`, which reaches
    `op_sh.c:379` and forks there; grepping the C tree for `fork(` never showed
    it, because the call comes from `APISRVR:566`.

    `probe-sessionfork.ps1 -Prefix sdapiidb30`, on the 09:53:11 install:
    sdwind made **1** fork clone (`sdwind.exe` 15812) whose exec target was the
    session (`sd.exe` 4448); **the session then made 2 fork clones of its own,
    both exec'ing `powershell.exe`** (14612→29948, 34624→27640).

    | step | what happens |
    |---|---|
    | `APISRVR:1472` | `K$ASSUME.USER` impersonates the caller. Works (`b17`) |
    | `APISRVR:439` `vb.account` | the account switch, a **post-login** request |
    | `APISRVR:566` | `is_grp_member(kernel(K$USERNAME,0), acc.group)` |
    | `!ps_script` → `op_sh.c:379` | `cpid = fork()`, then execs `powershell.exe` (`:308`) |
    | → | the impersonation is silently gone |
    | `vb.open` / `vb.write` | run as LocalSystem → `b28`'s SYSTEM-owned record |

    **`APISRVR:1470`'s own comment names its killer**: the account's files "are
    opened at LOGTO, which is after, and that is what makes this worth doing".
    LOGTO is where the group check forks the identity away.

    **MEASURED vs INFERRED.** *Measured*: the session forks twice into
    PowerShell; `fork()` drops impersonation; the record is SYSTEM-owned.
    *Inferred*: that **this** fork is the one that drops it in the live session.
    **(b) is now a confirmation rather than a search.**

    ***THE FIX IS WIDER THAN THIS CALL.*** `PHANTOM` (`op_kernel.c:735`) and
    `SH` (`op_sh.c:379`, the same site) fork too, so any of them taken by an
    impersonated session drops it. Moving `is_grp_member` alone leaves the class
    open. `cygwin_internal(CW_SET_EXTERNAL_TOKEN)` addresses the class;
    re-impersonating after each fork is the narrow fix. Either lands on
    `sd.exe`.

    **THE INSTRUMENT FAULT THAT CAME WITH IT, so it is not repeated.** `b29`
    reported "the session does fork" **for the wrong reason**: a Cygwin
    `fork()`+`exec()` is **two** Windows process creations — the clone carries
    the *parent's* image name, then the exec target starts as a new process —
    and the first version read that pair as "session forks child". It was
    calling `sdwind`'s own spawn a fork by the session. Corrected to resolve
    clone→target pairs, and re-run as `b30`; the corrected run also **names the
    exec target**, which is what identifies the call site at all.

    **(a2) IS BUILT AND PRE-FLIGHTED — `gplbld/probe-sessionfork.ps1`, 24 Aug
    2026.** It watches `Win32_ProcessStartTrace` while a live
    `verify-apiidentity` run logs in and writes, and asks whether the session
    creates any child at all. **An event trace rather than polling**, because a
    fork that exits in milliseconds would be missed by polling and the miss
    would read as "did not fork". **It filters on `ParentProcessID` and never on
    `CommandLine`** (§6's self-match trap), which also separates the two kinds
    of `sd.exe` for free: sessions are children of `sdwind`, the verifier's own
    `Invoke-SD` calls are children of the verifier. It refuses three null cases
    — the trace not firing (self-tested first, measured working), no starts at
    all during a run that demonstrably happened, and no child of `sdwind` seen,
    since without identifying the session "it did not fork" is not a claim it
    may make. **No switch skips `assert-current`, deliberately.**

    ***IT NEEDS A CURRENT TREE.*** `verify-apiidentity.ps1:409` gates on
    `assert-current`, and the 24 Aug banner change made the tree stale, so **a
    `cycle.ps1` is owed before (a2) runs**. `-SelfTestOnly` proves the
    instrument fires without spending one. Prefix **b29 or later**.

    **(b) Costs a cycle**: `ImpersonatingUser()` (`win32s4u.c:230`) exists and
    has no caller; reporting it at write time is decisive.

    ***AN ACL FIXTURE CANNOT ANSWER THIS AND MUST NOT BE RE-TRIED.*** `b27` and
    `b28` both opened all three ACL fixtures - including one whose `%0` grants
    the account alone, and one that grants it nothing - with every DACL
    verified correct at `%0` in the same run. No single token does both.
    **A LocalSystem session holds `SeBackupPrivilege`, which bypasses DACLs
    outright**, so no arrangement of grants gates it. Those three rows are kept
    in the verifier as readings, marked non-decisive, and do not set the exit
    code. Ownership works precisely because a privilege that lets a token OPEN
    what it has no ACE on does not change whose name goes on a file it CREATES.

    **HOW THE FIXTURES GET INTO VOC, because two obvious routes are dead.**
    `SET.FILE` is a CROSS-ACCOUNT verb (`SETFILE.b:29`) and refuses with 2201;
    `CREATE.FILE ... DYNAMIC PATHNAME` half-succeeds, writing the VOC entry and
    then stopping at 6128 before adding `@ID` (`CREATEF:471-486`), which is a
    product bug and still open. What works, and is what the verifier does:
    **create the file plainly, move it, then write the VOC F-pointer as text
    into a DIRECTORY-type scratch file and `COPY` it into VOC.** COPY maps
    newlines to field marks whenever exactly one side is a directory file
    (`COPY:220-229`); `BINARY` is what SUPPRESSES that and is implied only when
    both sides are directory files. **The record must be LF-only** - §6.

    ***THE CLASS OPTION IS MEASURED AND IT WORKS — 24 Aug 2026. BUT NOT AS THE
    ONE CALL THIS ENTRY NAMED: IT IS A PAIR.*** `probe-impfork.c` gained a
    **Q4** leg. It costs **no cycle** — the file is on `assert-current`'s
    `$neverShipped` list — and it needed no edit to `sd.exe`.
    `probe-impfork.ps1 -Account test1`, elevated, `assert-current` exit 0
    either side, install 24 Aug 10:34:44 unchanged. **Exit 15 on both legs.**

    | form | result |
    |---|---|
    | 1 — `CW_SET_EXTERNAL_TOKEN`, then `fork` | **LOST.** Returned 0, `errno` 0, thread token `NONE`, file owned by SYSTEM |
    | 2 — register, then `seteuid(target)`, then `fork` | ***CARRIED.*** Thread token `target` **and** file owned `GITORLI\test1` |

    **THE BARE CALL IS NOT THE FIX, AND THAT IS THE FINDING.** It only
    *registers* a token; **`seteuid()` is what makes the runtime adopt it**,
    which is why Cygwin's own callers do the pair. Row 4 and row 6 differ by
    nothing else.

    **Both instruments agree, in both legs** — the `fork()`ed and `exec()`d
    child (the API session's shape) and the direct control, identical rows.
    **Row 1 is the control and it reproduced the defect first**: a plain
    `fork()` gave token `NONE` and a SYSTEM-owned file, so the run demonstrated
    the fault before testing the cure.

    ***THE NULL CASE WAS REAL AND WAS CAUGHT BEFORE IT LIED.*** The unelevated
    `--q4check` mode necessarily targets its own uid, and `seteuid()` to the
    uid you already hold returns 0 from a fast path without touching the user
    context — the first `q4_report` printed that as form 2 **"lost"**, a
    verdict on something that never ran. `q4_report` now separates **three**
    non-results (never attempted, refused, target uid already the euid) from a
    loss, and the elevated run shows `seteuid(197957) from euid 18`, so the
    guard confirms it was genuinely exercised rather than assumed.

    ***WHAT THE CLASS FIX WOULD CHANGE BESIDES THE TOKEN — SURVEYED, 13 SITES.***
    `seteuid` moves the **effective** uid only; **the real uid stays 18
    (SYSTEM)**, which the probe shows directly (`uid 18 euid 197957`). So:

    | site | effect |
    |---|---|
    | `linuxlb.c:95`, `:213` `getpwuid(getuid())` | **unaffected** — real uid |
    | `sdfix.c:1548` `getuid()` in a dump name | **unaffected** — real uid |
    | `op_sys.c:228` `geteuid()` exposed to BASIC | **CHANGES** — the one visible behavioural difference |
    | `ingroup.c:76` `getegid()` | unaffected by `seteuid` alone; **would change if the fix also calls `setegid`** |
    | `sdext_eguid.c:67` | already does this pair; off the login/write path |

    **So the decision is now between two WORKING options**, and the class one
    costs a `seteuid` whose blast radius is the single `op_sys.c:228` reading.

    ***THE CLASS FIX IS BUILT — 24 Aug 2026. BUILT IS NOT VERIFIED (§0 rule 2):
    IT HAS COMPILED AND NOTHING HAS RUN IT.***

    | part | where |
    |---|---|
    | `adopt_in_runtime()` — the pair, register then `seteuid` | `gplsrc/win32s4u.c`, new static |
    | called on success, **fails closed** | `win32s4u.c`, after `ImpersonateLoggedOnUser` |
    | euid restored on revert | `RevertUserIdentity()` |
    | includes | `<unistd.h>`, `<pwd.h>`, `<sys/cygwin.h>`, **after `windows.h`** |

    **NO BASIC CHANGE AND NO NEW ENTRY POINT.** `K$ASSUME.USER` already routes
    to `AssumeUserIdentity()` (`op_kernel.c:289`), so extending that one
    function covers the hook; callers need not know it now takes two calls.

    **IT REFUSES THE NULL CASE INTERNALLY.** `seteuid()` to the uid already
    held returns 0 from a fast path *without* adopting the token, so
    `adopt_in_runtime` refuses when the euid already equals the target rather
    than reporting a success whose identity would die at the first fork. It
    also **reads the euid back** rather than trusting `seteuid`'s return.

    **`setegid` IS DELIBERATELY NOT CALLED.** `ingroup.c:76` reads `getegid()`
    and *does* have callers; the measurement did not need it.

    **Compiled clean:** `make sd` (`win32s4u.o`, `sd` linked, `bin/sd.exe`
    11:08:43 — newer than source, checked, because **`cycle.ps1` contains no
    `make`** and a C change can otherwise be cycled against a stale binary).
    Then `cycle.ps1 -SkipInstall` 11:10:08 — **198 BASIC programs, zero
    non-zero error counts**, staged tree whole, installer built 4,801,598 bytes.

    ***VERIFIED — 24 Aug 2026, install 11:15:29, `sd.exe` `7DDC68F6595382A6`,
    `assert-current` exit 0.*** `verify-apiidentity -Prefix sdapiidb32`, exit 0,
    the decisive row PASS. **STEP 14 IS CLOSED.**

    | instrument | `b28` (before) | `b32` (after) |
    |---|---|---|
    | owner of `ZZAPI` | `NT AUTHORITY\SYSTEM` | **`GITORLI\sdapiidb32`** |
    | control `ZZLOCAL` | `GITORLI\don` | `GITORLI\don` |
    | DENY fixture over the API | OPENED | **REFUSED, `status 3001`** |
    | `API IDENTITY LOST` in errlog | twice (`b31`) | **absent** |

    **THREE INSTRUMENTS, AND THE SECOND TWO WERE NOT AVAILABLE BEFORE.** The
    DENY fixture *could not* gate a LocalSystem session — `SeBackupPrivilege`
    bypasses DACLs outright, which is why §7 recorded those rows as
    non-decisive. **Its flipping to REFUSED is therefore evidence in its own
    right**, not a repeat of the ownership reading. And the errlog alarm is the
    *same* `check.identity` (`APISRVR:578`, `:921`) that fired twice on `b31`,
    unchanged since, with **both call sites exercised this run** — the account
    attach and the write. Its silence is a pass, not a removed check.

    **The changelog entry written ahead of verification now stands** and needs
    no revision.

15. **A data tree private from SD's own users** — §5.7's service-account model.

    ***SURVEYED 23 Aug 2026, AND THIS STEP IS MUCH SMALLER THAN IT READS.***
    Measured on the 10:01:45 install, `assert-current` exit 0. What follows
    replaces the old opening claim, which was that *"anyone who can use SD on
    this machine can read another account's files from outside SD"*.

    ***THAT IS NO LONGER TRUE, AND §8's "B WORK" IS WHY.*** Account privacy is
    **already enforced by the OS**, and it shipped without this step being
    updated to say so:

    | path | DACL as installed |
    |---|---|
    | `user_accounts\don` | `sdu_don:(OI)(CI)(M)`, Administrators, SYSTEM — **no `sdusers`** |
    | `user_accounts` container | locked; refuses even its own user's DACL read |
    | `sdsys\$cred`, `pstmp`, `audit` | no `sdusers` at all |
    | `gcat`, `os.users`, `batch.jobs`, `gpl.bp.out` | `sdusers:(OI)(CI)(RX)` — read-only |

    `sdu_don` contains only `don`; `test1` is an `sdusers` member and is not in
    it. `secure-account-dirs.ps1` stamps existing accounts, `CREATEA` stamps new
    ones, and `verify-accountacl` guards that the two agree. **So the
    service-account model is not needed for account-to-account privacy** — the
    per-account group already does it, and §5.7's objection that it *"adds a
    Windows-user-to-account mapping to maintain"* is stale: the group is
    **derived** from the directory name (`sdu_<name>`) and `GRANT` maintains it.

    ***WHAT IS ACTUALLY LEFT IS AN INTEGRITY HOLE, NOT A CONFIDENTIALITY ONE,
    AND IT IS WORSE THAN THE ONE THE STEP WAS WRITTEN ABOUT.*** Everything under
    `C:\ProgramData\SD` that nothing stamped still inherits `sdusers:(OI)(CI)(M)`
    — **Modify, not read** — including `sdsys\bin`, `accounts`, `$map`, `$ipc`,
    `messages`, `newvoc`, `bp`, `cat` and `sd.conf`.

    **`sdsys\bin\pcode` IS THE ONE THAT MATTERS.** `sysseg.c:189` builds
    `<sysdir>/bin/pcode`, `:193` opens it and `:279` reads it into the shared
    segment; every session then executes it through `load_pcode()`
    (`sd.c:847`). **So any `sdusers` member can replace the pcode every
    session runs, including SDSYS's and an administrator's**, taking effect at
    the next SD start.

    ***PROVED BY WRITING, NOT BY READING THE ACL***: as `GITORLI\don`,
    **unelevated** — so the `Administrators` ACE is deny-only and cannot be the
    grant — a file was created in `C:\ProgramData\SD\sdsys\bin` and removed
    again. The grant is `sdusers:(M)`.

    **THE INSTALLER DISCLOSES THE OTHER THING.** `sd.iss:778` and `:1407` say a
    user can *"read and rewrite any other account's files"* — confidentiality,
    between accounts. **Neither says the interpreter itself is writable**, and a
    reader would not take it from those words.

    ***THAT HALF IS DONE AND VERIFIED, 23 Aug 2026, install 17:47:55.***
    `secure-pcode.ps1` grants `sdusers:(OI)(CI)(RX)` — **read, not write** —
    called from `sd.iss`'s `SecurePcode` beside `SecureGcat` and staged by
    `stage.py`. `verify-pcodeacl.ps1` guards it, 4 of 4, and the suite is
    **27** (10 unelevated). §STEP 15 SURVEYED has the readings and why `(RX)`
    rather than removing `sdusers`.

    ***WHAT REMAINS OF THIS STEP AFTER THAT.*** The rest of the inherited
    `sdusers:(M)` list is untouched — `accounts`, `$map`, `$ipc`, `messages`,
    `newvoc`, `bp`, `cat`, `sd.conf`. **Each needs its own judgement, not a
    sweep**: sessions genuinely write some of them, so the `gcat`/`pcode`
    answer of "read-only to `sdusers`" does not transfer. `accounts` is the
    obvious next one to weigh. **None of this is the service-account model,
    which the survey above shows account privacy no longer needs.**

    **This is what makes tiers 1 and 2 real.** §8: tier 3 is real because
    Windows enforces it; the other two are only ever as real as the ACLs.

    ***"IT NEEDS `CreateProcessAsUser` AT THE SITES THAT CREATE SESSIONS" IS
    NOT ENOUGH, AND THE SURVEY IS WHY.*** There are only three such sites —
    `sdwind.c:491` (API, parent is the service), `op_kernel.c:701` (PHANTOM),
    and `sdclilib.c:1597` (`SDConnectLocal`). ***THE PATH SD USERS ACTUALLY
    TAKE HAS NO SITE AT ALL***: §5.6.2 makes accounts **ssh-only**, sshd
    creates that session as the user, and `sd.exe` is then simply the user's
    own process. Nothing inside SD spawns it, so no call placed inside SD can
    change its token. Making *that* run as a service identity means `sd.exe`
    becoming a thin client of `sdwind` — a far larger change than this step's
    one sentence implies, and the transport for it already exists (§7 step 11).

    **THE CALL ITSELF IS MEASURED WORKING, 23 Aug 2026** — step 14's probe,
    from LocalSystem, with an S4U token and no password. Note it points the
    *opposite* way to this step: S4U makes a session run **as the user**, while
    §5.7's model makes it run **as the service**. Both are coherent; they are
    different architectures and only one can be built.

16. **LINE ENDINGS: SD READS ONLY LF AND WRITES ONLY LF, ON A WINDOWS-ONLY
    PRODUCT.** Raised by the repository owner, 24 Aug 2026. **Not started, and
    it is two pieces of work.** His reasoning, which is the part that dates:
    **directory files exist so that EXTERNAL EDITORS can edit BASIC programs**;
    OpenQM was originally a Windows product and is believed to have used CRLF
    then; the Linux version moved to LF, ScarletDME and `sdb64` inherit that,
    and this port inherited it from them **without the reversal ever being
    weighed**.

    ***AND THE WRITE SIDE IS THE HALF WITH THE STRONGER CASE - owner,
    24 Aug 2026:*** *"if a user wants to create a csv file to be read by Excel,
    or a document to be loaded into notepad or imported into word, i'm sure the
    crlf standard would be expected."* **That is a requirement about what SD
    PRODUCES, not merely tolerance of what it is given**, and RFC 4180 does
    specify CRLF for CSV. A `WRITESEQ` that emits LF is not wrong on Linux and
    is a defect on a Windows-only product whose intended user (§1) is a Windows
    developer using SD as a back end data store.

    ***AND SD HAS DEDICATED CSV STATEMENTS, SO THIS IS A CONFORMANCE CLAIM SD
    ALREADY MAKES AND DOES NOT MEET — owner, 24 Aug 2026.*** `WRITECSV`,
    `READCSV`, `MATREADCSV`, `INPUTCSV` and `PRINTCSV` are shipped statements,
    with `OP_FORMCSV` and `OP_CSVDQ` in `op_str5.c` and a `CSV` report keyword
    in the query processor. **`sdhelp/csv.htm` says the output *"conforms to
    the CSV format specification (RFC 4180)"* in as many words, and RFC 4180
    specifies CRLF as the record separator.**

    **`WRITECSV` EMITS LF.** `BCOMP:11366` `st.writecsv:` assembles the line
    and then sets `opcode = OP.WRITESEQ`, so it inherits `op_seqio.c:1712`'s
    global `Newline`. `sdhelp/sdb_writecsv.htm` describes it only as *"written
    to the file with a newline appended"* — it does not say which. **So the
    owner's Excel case is not hypothetical: it is a named verb, documented as
    RFC 4180, that is not RFC 4180 on the platform this port exists for.**
    That gives (b) a concrete acceptance test instead of a matter of taste.

    ***AND THE TWO CSV OUTPUT PATHS MAY ALREADY DISAGREE — MEASURE BEFORE
    ASSUMING.*** The query processor's `CSV` keyword produces a REPORT, which
    goes through a print unit and therefore through `pu->newline`; `WRITECSV`
    goes through `WRITESEQ` and the global. If `SETPTR … NEWLINE CRLF` works
    (see the resource note), then `LIST … CSV` can already be made conformant
    while `WRITECSV` cannot — an inconsistency worth knowing before choosing
    where to fix it.

    **THE COMPILER IS ALREADY SAFE, WHICH IS WHY THIS HAS NOT BITTEN YET.**
    `BCOMP:1672`, in `get.line:` - the main source-line reader - is
    `if src[1] = char(13) then src = src[1,len(src)-1]` under the comment
    *"Remove trailing CR for cross-platform compatibility"*. (`src[1]` is the
    RIGHTMOST character in this dialect, as the `~` continuation test two lines
    below confirms.) **So editing a BASIC program externally works, which is
    the one case the feature exists for.** Nothing else is protected.

    **NEITHER RECORD READ PATH HAS ANY CR HANDLING** - checked 24 Aug 2026.
    CR literals do exist elsewhere in the C tree (twelve, in seven files; see
    the correction in the resource note below), but none of them is on the
    path that turns a file's bytes into a record.

    | direction | site | today |
    |---|---|---|
    | directory-file record READ | `op_dio3.c:1180` | maps `\n` to a field mark, leaves `\r` - **every field gains a trailing CR** |
    | `READSEQ` | `op_seqio.c:1152` | splits on `'\n'` only - every line gains a trailing CR |
    | directory-file record WRITE | `op_dio3.c:1385`, `:1399` | field mark to `Newline` |
    | `WRITESEQ` | `op_seqio.c:1712`, `:1726` | `Newline` |
    | `COMO` | `op_tio.c:2986` | `Newline` |
    | hold files | `to_file.c:129`, `:340` | `Newline` |

    `Newline` is `sddefs.h:65`, `"\n"`, `NewlineBytes 1`, sitting under
    *"Derived items"* beside `DS '/'`. **Upstream `sdb64` is byte-identical**,
    so changing it is a deliberate divergence rather than a fix.

    ***THE WRITERS ARE PARAMETERISED AND THE READERS ARE NOT. THAT ASYMMETRY IS
    THE SHAPE OF THE WORK, AND IT IS WHY (b) ALONE CORRUPTS THE TREE.*** All
    **eight** write sites go through `Newline`/`NewlineBytes`, including the
    file-position arithmetic at `op_seqio.c:1717` — so the write half really is
    close to a two-line change at `sddefs.h:65-66`. The read half is **four
    hardcoded sites**: `op_dio3.c:1172` (the trailing-newline drop),
    `op_dio3.c:1182` (the mapping loop), `op_seqio.c:1152` (the terminator
    search) and `op_seqio.c:1153` (**a hardcoded `posn += 1`** past a
    terminator that would become two bytes). **Change the constant on its own
    and SD writes `\r\n`, maps the `\n` to a field mark, leaves the `\r` on the
    end of every field, and desyncs every `READSEQ` position.** So (a) is a
    PREREQUISITE for (b), not an alternative to it.

    *And note what that asymmetry implies: a two-byte-capable newline constant,
    with every write site routed through it, is not what a Linux-only codebase
    would carry — it would inline `"\n"`. It is consistent with the owner's
    account that the write side was built for CRLF and later pointed at LF,
    which makes (b) closer to restoring an intended capability than to adding
    one. **Do not read that as permission to skip (a).***

    ***SCOPE, MEASURED, AND IT IS NARROWER THAN IT LOOKS: DH FILES ARE NOT
    AFFECTED.*** `Newline` reaches only the four write sites above. A DH file
    stores field marks in its own format, so `gcat`, `VOC`, `$CRED`, `ACCOUNTS`
    and every byte count this file quotes for them (`gcat/$CPROC` 25,208;
    `$LOGIN` 6,160) are untouched by either change.

    ***STARTED 24 Aug 2026. THREE THINGS ARE NOW MEASURED OR DOCUMENTED, AND
    TWO OF THEM CHANGE THE SHAPE OF THE WORK.*** All three cost **no cycle** —
    they read the docs and the 11:15:29 install, which `assert-current` says
    matches source.

    **1. THE DOCUMENTATION SAYS CRLF-ON-WINDOWS IS THE DESIGN, SO (b) IS A
    CONFORMANCE FIX RATHER THAN A PRODUCT DECISION.** From the owner's
    `..\sdhelp` collection, 24 Aug 2026:

    | source | words |
    |---|---|
    | `qmhelp_2-6-6/directoryfiles.htm` | field marks are converted to *"the **operating system dependent** representation of a newline"*, and on read *"the newlines are translated to field marks"* |
    | `qmhelp_2-6-6/qmb_writecsv.htm` | *"QM adheres to the CSV standard (RFC 4180)."* |
    | `qmhelp_2-6-6/csv.htm` | mode 1 *"produces output that conforms to the CSV format specification (RFC 4180)"* |

    **"Operating system dependent" is the whole argument.** On Windows that is
    CRLF, so SD emitting LF is a deviation from its own documented design, not
    a preference this port would be imposing. RFC 4180 §2.1 specifies CRLF, and
    **both** CSV paths claim conformance.

    ***2. `SETPTR … NEWLINE CRLF` REACHES THE DISK. MEASURED — AND IT SHRINKS
    (b).*** The resource note called this the first thing to test. Two legs,
    one report, differing in one token; hold files read back as bytes:

    | leg | size | CR | LF | CRLF pairs |
    |---|---|---|---|---|
    | `NEWLINE CRLF` | 133 | 3 | 3 | **3** |
    | `NEWLINE LF` (control) | 130 | 0 | 3 | 0 |

    Exactly three bytes apart — the three added CRs. **So everything that goes
    through a print unit can already emit CRLF today**, including
    `LIST … CSV LPTR n`. **The two CSV paths therefore DO disagree**, which
    step 16 predicted and left open: the report path is reachable-conformant
    now, `WRITECSV` is not.

    ***CORRECTION IN THE SAME BREATH:*** an earlier reading of this step took
    `to_file.c:128`'s `case NL: emit(pu, Newline, NewlineBytes)` as proof the
    global wins on the hold-file path. **The measurement says otherwise.** That
    `case NL:` handles an embedded newline as PRINT CONTROL — the same
    distinction the resource note already draws for `to_file.c:107` and CR —
    and the line terminator is emitted from `pu->newline` before it gets there.

    ***3. THE (a) DEFECT IS CONFIRMED END TO END, NOT INFERRED.*** A record
    planted into a directory file from outside SD with CRLF, which is exactly
    what an external editor does, read back through `READ`:

    | record | bytes | field 1 | field 2 | field 3 |
    |---|---|---|---|---|
    | CRLF | 18 | LEN=6 **LASTCHAR=13** | LEN=5 **LASTCHAR=13** | LEN=5 LASTCHAR=65 |
    | LF (control) | 16 | LEN=5 LASTCHAR=65 | LEN=4 LASTCHAR=65 | LEN=5 LASTCHAR=65 |

    **Every CRLF-terminated field keeps a trailing CR.** The third field is
    unterminated in both records and comes back clean either way, which pins it
    to terminator handling rather than to content. Instruments and fixtures are
    `scratchpad/measure-newline.ps1` and `measure-read.ps1`; both plant, read
    and then remove their own fixtures.

    ***4. ALL FOUR SEQUENTIAL STATEMENTS MEASURED, 24 Aug 2026 — AND `READCSV`
    IS A DATA-CORRUPTION DEFECT ON THE DOCUMENTED INTEROP PATH.*** Read
    fixtures were planted with **CRLF from outside SD**, which is what Excel
    and an external editor produce; write output was read back as raw bytes.

    | statement | today | evidence |
    |---|---|---|
    | `WRITESEQ` | **LF only** | `41 4C 50 48 41 0A 42 45 54 41 0A` |
    | `WRITECSV` | **LF only** | `41 31 2C 42 31 0A 41 32 2C 42 32 0A` — **so the RFC 4180 claim is false today** |
    | `READSEQ` | **keeps the CR on every line** | `LEN=6 LASTCHAR=13`, `LEN=5 LASTCHAR=13`; the unterminated third line reads `LASTCHAR=65` — the built-in control |
    | `READCSV` | **keeps the CR on the LAST FIELD of every row** | row 1 `P LEN=2 LAST=49`, **`Q LEN=3 LAST=13`**; row 2 the same |

    ***`READCSV` IS THE ONE TO LEAD WITH.*** The first field is clean because a
    comma terminates it; the last field inherits the line terminator's CR. So
    **reading a conformant CSV silently appends a CR to one field per row** —
    not an aesthetic issue but wrong data, on the exact path `csv.htm` and
    `qmb_writecsv.htm` claim RFC 4180 conformance for. It makes (a) a
    correctness fix rather than tolerance.

    ***5. THE `bp.out` QUESTION THAT BLOCKED (b) IS ANSWERED. OBJECT CODE IS
    NOT AT RISK.*** ***`sdsys/gpl.bp/BASIC:239` is `mark.mapping out.f, off`***
    — the `BASIC` verb disables mapping on the object file before writing it.
    Confirmed independently by a byte census of the shipped tree:

    | file | 0x0A LF | 0x0D CR | 0xFE FM | 0xFD SVM |
    |---|---|---|---|---|
    | `gpl.bp/SETPTR` (source, 32,799 b) | 929 | 0 | **0** | 0 |
    | `gpl.bp.out/SETPTR` (object, 7,702 b) | 82 | 53 | **5** | 62 |

    The source record has **no field marks** — every one became an LF, so
    mapping ran. The object keeps its field marks *and* carries raw LF and CR
    as data, so mapping did not run. **Changing `Newline` therefore cannot
    corrupt object code**, and the failure this step feared — "a corrupt
    catalogue rather than a line-ending change" — is off the table.

    ***CORRECTION: THE CLAIM THAT NOTHING CALLS IT WAS A GREP FOR THE WRONG
    TOKEN.*** This step said *"No shipped BASIC program calls `MAPMARKS` — the
    only hit is `BCOMP:9073`"*. `MAPMARKS` is the **opcode**; the **statement**
    is `MARK.MAPPING`, and it appears **27 times in 13 shipped programs** —
    `BASIC`, `CATALOG`, `COPY`, `COPYP`, `MAPCAT`, `APISRVR`, `CT`, `CNAME`,
    `CONFIGF`, `BBPROC`, `PROG_INFO`, `SDCLIENT`, `BCOMP`. The write path was
    never missing; it was never grepped for under its own name.

    ***(a) IS WRITTEN, 24 Aug 2026. IT HAS COMPILED AND NOTHING HAS RUN IT
    (§0 rule 2).*** `bin/sd.exe` 12:05:15, `make sd` clean, both changed files
    clean on their own under `-Wall -Wformat=2`. **`cycle.ps1 -SkipInstall` is
    NOT yet run** — the elevation was declined — so the tree is STALE and
    nothing has been staged.

    | part | where |
    |---|---|
    | directory-record read: CRLF folds to ONE field mark | `op_dio3.c`, the mapping loop, rewritten as a compactor |
    | trailing terminator at EOF drops `\r\n`, not just `\n` | `op_dio3.c`, the `remaining_bytes == 0` block |
    | `READSEQ` (and so `READCSV`) strips a CR before the LF | `op_seqio.c`, the normal-file branch |

    ***TWO CORRECTIONS TO THIS STEP'S OWN SITE LIST, BOTH FOUND BY OPENING THE
    FILES.*** They are why "four hardcoded sites" understated the work:

    1. ***`op_seqio.c:1152`/`:1153` IS THE PORT/FIFO BRANCH, NOT `READSEQ` ON A
       FILE.*** The branch that reads an ordinary record is
       **`op_seqio.c:1244`**, which this step never listed. Fixing only the
       listed lines would have changed nothing that `READSEQ` on a directory
       file actually executes. **The port/FIFO branch is deliberately LEFT
       ALONE** — a CRLF arriving on a port or socket may be protocol rather
       than a text line ending, and §5's `inewline`/`onewline` pair is the
       per-channel setting that already governs that. Named here so the
       omission is a decision and not an oversight.
    2. ***EVERY ONE OF THESE READERS IS CHUNKED, SO A CRLF CAN STRADDLE A
       BUFFER BOUNDARY.*** `SEQ_BUFFER_SIZE` is **2048** and
       `MAX_T1_BUFFER_SIZE` is **31744**. At 2 KB this is not an edge case: in
       a large CSV a terminator landing across a boundary is close to certain.
       Both fixes therefore **hold the CR back** rather than looking at the
       byte before the LF, and both emit it as data if no LF follows —
       including at end of file, where a deferred CR would otherwise be
       swallowed.

    **A LONE CR IS LEFT ALONE THROUGHOUT**, which is the rule this step set and
    what `BCOMP:1672` already assumes. **Image mode is untouched**, so no
    binary read can be affected — mark mapping is the discriminator, exactly as
    the step said.

    ***(a) IS VERIFIED — 24 Aug 2026, install 12:15:51, `sd.exe`
    `7F587B82B63569C8`, `assert-current` exit 0.***
    `verify-lineendings.ps1` exit 0, **14 of 14 decisive checks PASS.**

    | reading | before (11:15:29) | after (12:15:51) |
    |---|---|---|
    | CRLF record, field lengths | 6, 5, 5 — `LAST=13` on 1 and 2 | **5, 5, 6 — `LAST=65, 88, 89`** |
    | LF control | 5, 4, 5 | **5, 5, 6 — identical to the CRLF record** |
    | `READSEQ` line 1 | `LEN=6 LAST=13` | **`LEN=4 LAST=65`** |
    | `READCSV` last field | `QLEN=3 QLAST=13` | **`QLEN=2 QLAST=49`** |
    | **straddle, line 1** | *never tested* | **`LEN=2047 LAST=80`** — folded across the boundary |
    | **lone CR record** | *never tested* | **1 field, `LEN=11 LAST=90`** — CR preserved as data |

    **The two rows that were never tested before are the ones that matter.**
    The straddle proves the CR is carried across a 2048-byte buffer boundary
    rather than found by looking behind the LF; the lone-CR row proves the fix
    did not simply strip every CR. Fixture words end in **different letters**
    (`A/X/Y`, `A/B/C`, `P/Q`, `Z`), so no last-character reading is right by
    coincidence. No residue left in `bp`, `BP.OUT` or `cat`.

    ***THE VERIFIER IS WRITTEN AND IS NOT A ONE-LINER, FOR ONE REASON:***
    `gplbld/verify-lineendings.ps1`, on `$neverShipped` in the same commit.
    Six checks, and **two of them are controls on the FIX rather than on the
    defect** — which is what stops it scoring green on a change that is wrong:

    | check | why it exists |
    |---|---|
    | CRLF record reads with no trailing CR | the defect |
    | LF control reads identically to it | proves the two spellings now agree |
    | `READSEQ` lines carry no CR | the defect on the sequential path |
    | ***CRLF straddling the 2048-byte buffer boundary*** | **the case no small fixture reaches**; line 1 must read 2047, not 2048 |
    | ***a LONE CR survives as data*** | **a fix that stripped every CR would pass everything above** |
    | `READCSV` last field is clean | the RFC 4180 round trip |

    It **refuses the null case out loud**: if the instrument produces no
    readings the run is VOID, not a pass, because every "carrying a CR: 0"
    check would otherwise be satisfied by absence. Fixture words end in
    different letters so a last-character reading cannot be right by accident.

    ### (a) MAKE THE READERS TOLERANT - a defect fix, do this first

    Treat `\r\n` as the terminator at the two read sites; **leave a lone `\r`
    alone**, because it is data. This is exactly what `BCOMP` already does.
    Two details that are easy to miss:

    - The existing trailing-newline handling at `op_dio3.c:1169` drops a final
      `\n`; it must drop a final `\r\n` too, or the last field keeps its CR.
    - **Mark mapping is the discriminator.** It is off in image mode, which is
      the binary path, so folding CRLF in non-image mode cannot touch a
      binary read.

    **(a) STANDS ON ITS OWN AND IS WHAT MAKES (b) SAFE TO CONSIDER**, because a
    tolerant reader accepts the LF records already shipped in `voc_template`,
    `newvoc`, `messages` and `bp` whichever way (b) goes, and accepts a tree
    holding both spellings during a transition.

    ***(b) IS DECIDED AND WRITTEN, 24 Aug 2026. COMPILED AND CYCLED TO
    `-SkipInstall`; NOTHING HAS RUN IT.***

    ***THE OWNER'S RULE, AND IT IS BETTER THAN THE THREE OPTIONS IT WAS ASKED
    TO CHOOSE BETWEEN:*** *"everything including record writes to files that
    are directory as they may be read and written by external programs.
    anything involving dynamic files, it doesn't matter as they can't be
    directly read through external programs."* **The discriminator is EXTERNAL
    READABILITY, not the statement.** It is also the documented purpose of
    directory files (`directoryfiles.htm`: data *"to be processed from outside
    of QM"*).

    ***THAT RULE RESOLVES TO THE CONSTANT, WHICH IS WHY THIS OVERRIDES THIS
    STEP'S OWN "DO NOT FLIP THE GLOBAL" ADVICE.*** Surveyed 24 Aug: **every
    site `Newline` reaches is on the external side of the owner's line** —
    directory-record writes, `WRITESEQ`/`WRITECSV`, `COMO`, hold files, errlog
    — and **no DH path uses the macro at all**. `sddefs.h:65-66` is now
    `"\r\n"` / `2`. The three objections that made "flip it" wrong before are
    all now answered: object code is safe (`gpl.bp/BASIC:239`), the readers are
    tolerant ((a), verified), and the internal-files cost is what the owner
    just ruled on.

    ***IT IS A RESTORATION, NOT AN INVENTION — `k_error.c:605-611` SAYS SO.***
    It uses this macro *"instead of the more obvious use of `\n`"* precisely so
    it can *"do our own handling of the CRLF newline pair on Windows"*. That
    comment was written when `Newline` was `"\r\n"`. `tio.h:111`'s
    per-print-unit `char newline[2+1]` is the same tell.

    ***TWO THINGS THE EIGHT-SITE SURVEY IN THIS STEP MISSED.***

    1. **`Newline` has EIGHT MORE uses that write the ERRLOG** — `k_error.c`
       ×6, `sdwind.c` ×2. They move with it, which on Windows is wanted (the
       log opens in Notepad) but was never listed as a consequence.
    2. **Ports and FIFOs do NOT use it.** `op_seqio.c` writes its own
       terminator, so no socket or port was affected by (b). **That call was
       `writeport(fu, "\r\n", 1)` — a two-character literal with length 1, so
       it emitted CR only.** ***FIXED separately, 24 Aug 2026 — count is now
       2 (`op_seqio.c:1762`), on the owner's instruction.*** It is **not** part
       of (b) and does not use `Newline`: a port is not a directory file, so
       the external-readability rule never reached it. `writeport()`'s third
       argument is a byte count (`lnxport.c:88`), the literal is the statement
       of intent, and `onewline` (`tio.h:162`) is init `"\r\n"` for
       character-device output. **Upstream `sdb64` has the identical line —
       `UPSTREAM_FIXES.md` #14.** The neighbouring `WRITEBLK` port write
       correctly appends nothing and was left alone.
       ***IT IS COMPILED AND CYCLED TO `-SkipInstall` (12:48:38) BUT CANNOT BE
       TESTED HERE*** — exercising it needs a real port device, and no verifier
       in this project can reach it. That is weaker evidence than everything
       else in this step and is stated rather than glossed.

    **`DS` STAYS `/`.** §7 step 12's ruling is unaffected — the two "derived
    items" are not one decision.

    ***(b) IS VERIFIED — 24 Aug 2026, install 12:36:09, `sd.exe`
    `070A9C52E293B2FA`, `assert-current` exit 0. `verify-lineendings` exit 0,
    **17/17 decisive**. STEP 16 IS CLOSED, BOTH HALVES.***

    | what SD wrote | bytes on disk |
    |---|---|
    | `WRITESEQ` | `4F 4E 45 **0D 0A** 54 57 4F **0D 0A**` |
    | `WRITECSV` | `41 31 2C 42 31 **0D 0A** 41 32 2C 42 32 **0D 0A**` — **RFC 4180 at last** |
    | directory-file record write | `52 41 **0D 0A** 52 42 **0D 0A** 52 43 **0D 0A**` |

    **Read as RAW BYTES, not through SD** — the fix to (a) means a round trip
    through SD would report success whatever is on disk, so reading it back
    through SD would have been no check at all. **And all fourteen (a) checks
    still pass**, straddle and lone-CR controls included, so (b) did not
    regress (a).

    ***CYCLED TO `-SkipInstall`, 12:33:07, AND ONE NUMBER IS THE CONTROL.***
    198 programs, no non-zero error counts, installer 4,802,959 bytes. **Phase
    3 is byte-identical to the pre-change run** — `gcat` 126, `gpl.bp.out` 187,
    `$CPROC` **25418**, `$BCOMP` **88079**. Those byte counts not moving is
    positive evidence that the object and catalogue paths do not go through
    `Newline`, which until now was an inference from `mark.mapping out.f, off`.

    **`verify-lineendings.ps1` gained three write checks** — `WRITESEQ`,
    `WRITECSV` and a directory-record write, each read back as **raw bytes**.
    That last part matters: SD now folds CRLF on the way in, so a round trip
    through SD would report success whatever is on disk. **Owed: a full
    `cycle.ps1`, then the verifier.**

    ### (b) WRITE CRLF - a product decision, and it needs one thing settled first

    ***ANSWERED 24 Aug 2026 — `gpl.bp/BASIC:239`, `mark.mapping out.f, off`,
    corroborated by a byte census. THIS NO LONGER BLOCKS (b); the paragraph is
    kept because its reasoning is why the question mattered.***

    ***THE OPEN QUESTION THAT BLOCKS IT: HOW DOES BINARY OBJECT CODE IN
    `bp.out` SURVIVE THE FIELD-MARK/NEWLINE MAPPING TODAY?*** `bp.out` and
    `gpl.bp.out` are DIRECTORY files (§5.12) holding object code, and
    `op_dio1.c:867` sets `mark_mapping = TRUE` unconditionally on every
    directory-file open. **No shipped BASIC program calls `MAPMARKS`** - the
    only hit is `BCOMP:9073`, which is the compiler EMITTING the opcode - and
    `BCOMP` writes no object record with a plain `write`, so the write happens
    somewhere not yet located. **Find that path before changing `Newline`**: if
    object code goes through the mapping, a two-byte newline changes every
    object file on disk, and the failure would look like a corrupt catalogue
    rather than a line-ending change.

    **THE ARGUMENT FOR (b) IS A STANDING INSTRUCTION, NOT JUST TASTE.** §5.16
    rule 1: *"Every Linux-ism that remains is to be converted to its Windows
    equivalent where one exists"* - and `Newline "\n"` is precisely that.
    **The counter-precedent is its own sibling**: §7 step 12 deliberately left
    `dir.separator` as `/` because `@ds` is load-bearing for compilation. So
    the two constants under *"Derived items"* are not one decision, and
    `Newline` needs its own judgement rather than automatic conversion.

    **What (b) would cost, so it is weighed rather than discovered:** shipped
    directory-file records stay LF while newly written ones become CRLF, so a
    tree holds both - harmless given (a), untidy, and worth deciding whether
    `stage.py` normalises. Anything asserting exact byte counts on a directory
    file or on `COMO`/hold output moves. And the mapping is already lossy in
    one direction - data containing a literal newline round-trips as a field
    mark today - so (b) changes the shape of that edge case without creating
    it.

    ### RESOURCE NOTE: THE REFERENCE TREES WERE SEARCHED 24 Aug 2026

    Owner's suggestion — ScarletDME kept `if windows` blocks that Ladybridge
    stripped from the GPL version and that SD stripped again, so they might
    record how line endings were handled. **They do, and the answer is a
    DESIGN rather than a constant.** Recorded here so nobody searches twice.

    ***`C:\Users\dmont\Projects\gplsrc` (original ScarletDME C): NOTHING.***
    `qmdefs.h:84-85` is already `Newline "\n"` / `NewlineBytes 1`, identical to
    ours, with the same eight parameterised write sites. **No `#ifdef WIN32`,
    `WINDOWS` or `MSDOS` conditional survives anywhere in that tree** — §2's
    "Ladybridge stripped the Windows code thoroughly" is exactly right for C.

    ***`C:\Users\dmont\Projects\GPL.BP` (original ScarletDME BASIC): THE
    ANSWER.*** `SETPTR` takes a **`NEWLINE CR|LF|CRLF`** keyword, per PRINT
    UNIT — `newline = char(13)` / `char(10)` / `char(13):char(10)` — and
    reports it back in its own listing. **Ladybridge's answer to this question
    was to let the caller say what it wants, per output channel.**

    ***AND IT IS STILL IN THIS TREE, UNSTRIPPED. THIS IS THE MOST USEFUL THING
    IN THIS STEP.***

    | piece | where |
    |---|---|
    | `NEWLINE CR/LF/CRLF` keyword, documented and parsed | `gpl.bp/SETPTR:57`, `:423-434`, reported back at `:702-704` |
    | per-print-unit storage | `tio.h:111` `char newline[2+1]` |
    | set / read from BASIC | `op_tio.c:1575-1577`, `:1783`, default `"\n"` at `:3408` |
    | emitted at end of line | `op_tio.c:2147`, `:2651`, `:2667` — `pu->newline`, **not** the global |

    **SO THE CSV-FOR-EXCEL CASE MAY ALREADY BE REACHABLE TODAY**, with
    `SETPTR` … `NEWLINE CRLF` and `PRINT ON`. ***UNMEASURED, AND IT IS THE
    FIRST THING TO TEST BECAUSE IT COULD SHRINK (b) DRAMATICALLY:***
    `to_file.c:128`'s `case NL:` still emits the **global** `Newline`, so
    whether `pu->newline` actually reaches the disk in a hold file is not
    established. Write a hold file both ways and read the bytes.

    **THE TERMINAL ALREADY HAS ITS OWN PAIR, AND IT IS ALREADY CRLF** —
    `tio.h:162-163`, `onewline` init `"\r\n"` and `inewline` init `13`,
    settable from BASIC (`op_tio.c:2304`, `:2312`) and used for console and
    socket output (`:3296`-`:3303`). **The codebase's habit is a newline
    setting PER CHANNEL, and only file I/O was left on the global.**

    ***THAT REFRAMES (b): IT IS NOT "FLIP THE CONSTANT", IT IS "EXTEND THE
    PER-CHANNEL MODEL THAT ALREADY EXISTS TO `WRITESEQ` AND THE
    DIRECTORY-FILE WRITE".*** More work than two lines, far safer, idiomatic
    for this codebase, and it leaves SD's own internal files alone unless the
    caller asks otherwise — which removes most of the cost listed above.

    ***CORRECTION, 24 Aug 2026: an earlier draft of this step said "there is no
    `'\r'` char literal anywhere in the C tree". That was a malformed grep and
    it is false*** — there are twelve, in seven files. **None is on the record
    read path, which is the claim that matters and still stands.** Two are
    worth copying rather than re-deriving: **`config.c:172` is
    `while ((p > rec) && ((p[-1] == '\r') || (p[-1] == '\n')))`** — the §6 CRLF
    fix, already implemented, and the worked precedent for (a) — and
    `op_sh.c:188` scans for either terminator the same way. `to_file.c:107` and
    `op_tio.c:3865` handle CR as PRINT CONTROL (column reset), which is a
    different thing and must not be confused with line-ending translation.
    ### HOW TO MEASURE EITHER, because no existing verifier can

    Every verifier writes its fixtures with LF and drives SD down a pipe. The
    test for (a) is to plant a record file with **CRLF** into a directory file
    from OUTSIDE SD - which is what an editor does - then read it back through
    SD and compare the field against the intended value.
    `verify-apiidentity`'s ZZIDSRC mechanism is the worked example of planting
    a directory-file record from PowerShell, and its byte readback
    (`$bytes -contains 13`) is the assertion inverted. The test for (b) is the
    same fixture in reverse: have SD write, and read the bytes.

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

- **A1, account and grant administration (11) — owner-ruled 17 Aug, in the
  installed tree today:**
  ```
  create.account  delete.account  modify.account  update.account  clean.account
  grant  revoke  list.grants  unlock  modify.password  encrypt.field
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

**Total: 21 + 42 + 77 = 140 verbs.** Matches the 141 in today's `voc_template`
less UMASK, which is being removed. Every verb accounted for exactly once.

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
`SD-API-In-TCP` rule the installer creates (task `apiremote`, **ticked by
default**) and the uninstaller removes.

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
