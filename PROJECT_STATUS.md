# PROJECT STATUS

**The one file for what is open and what to know before working on it.** This
project moves between sessions, machines and accounts; anything not written here
is lost. Read this file first.

**One source of truth (owner, 21 Sep 2026: *"there should be only one, focused on
the tasks currently at hand"*).** Before this date open work was tracked in six
places — a task table, a stack of handoff blocks, `RELEASE_1.1_FIXES.md`,
`PRE_RELEASE_FIXES.md`, `BUGS_FROM_LINUX_PORT.md` and this file's §7 and §8 — and
two checkers existed only to compare them. **They are gone.** What remains:

| where | what it holds |
|---|---|
| **CURRENT PICKUP** | the newest handoff — where to start, in order |
| **OPEN TASKS** | every task that is open now, one short entry each, in the register's ids |
| **§0** | how to maintain this file |
| **§4.0.1, §4.0.2** | two elevation facts CLAUDE.md cites |
| **§5** | decisions and why — do not reopen without the owner |
| **§6** | traps that already cost time |
| **§8** | open questions nobody has diagnosed |

**Everything closed goes to [HISTORY.md](HISTORY.md), and nothing else does.** A
task that finishes is deleted from OPEN TASKS in the same commit and, if its
story is worth keeping, appended to HISTORY. **Do not strike a row, do not keep a
"done" list, do not add a second status anywhere.** New tasks continue
`RELEASE_1.1`'s id space: the highest id issued is **104**, so **the next is 105** —
take it here and cite it as `RELEASE_1.1 97`, never as a bare number (the old
`PRE_RELEASE` space overlaps it). A citation such as
`RELEASE_1.1 64` or `PRE_RELEASE 96` in a source comment names an entry that is
now in HISTORY.md under the heading *"ARCHIVE 21 Sep 2026 — RELEASE_1.1_FIXES.md"*
or *"— PRE_RELEASE_FIXES.md"*; grep the number there.

---

## CURRENT PICKUP

**This is the newest handoff and the only one. A session that ends replaces it
(delete the old, write the new); it does not stack a second block on top.** What
it lists as owed is also an entry under OPEN TASKS — if the two ever disagree,
OPEN TASKS wins and this block is the stale one. The 26th pass's handoff and
every older one are in HISTORY.md under *"ARCHIVE 21 Sep 2026 — PROJECT_STATUS.md
before consolidation"*; what they still owed was carried into OPEN TASKS.

***21 Sep 2026, ~13:10 — THE TREE IS CURRENT (12:26 cycle, upgraded over the top at 12:32); 64, 95, 96
AND 99 ARE CLOSED; 76 IS HALF WITNESSED.*** This stretch, all elevated through the agent helper with SDSYS
signed in: `verify-apiadmin` and `verify-privundetermined` green on `b211` after eight stale success
anchors were fixed (`test-verifieranchors-units.py` guards the class); `verify-accountmodel` rewritten and
green on `b213`/`b214` (no `newvoc` id missing from a new account; the four extras pinned), which found **100**.
`verify-upgrade.ps1` was fixed and self-tested; `probe-filespeed.ps1` and `probe-sdsysvoc.ps1` are kept.
The elevated helper stops after 60 idle minutes, or `agent-elevate.ps1 -Stop`.

***CALL `agent-elevate.ps1` DIRECTLY FROM A POWERSHELL SESSION*** — `& <path>\agent-elevate.ps1 -Run
-Script <gplbld>\VerifyInstall2.ps1 -ScriptArgs '-Run','bNNN','-Only','<step>'`. Through `powershell -File`,
or from bash, the comma list collapses into ONE argument and the runner answers *"-Run was not given"*
before running anything. `-Run` tokens `b206`–`b214` are spent.

***22 Sep 2026 — 101 IS DONE AND WITNESSED AND IS IN HISTORY.md.*** SDSYS is reached at the console and over
`SDConnectLocal`, and by nothing else: `verify-sdsyslocal` exit 0 from an elevated Windows SDSYS session
(admitted, `WHO -> 3 SDSYS`, and the administrator verb ran — so `IsInteractive()` answers true for a
ConnectLocal child), `verify-routes` **35/35** on `b218`, `verify-localconnect` exit 0, `assert-current` clean
against the 19:20:42 install. **It threw off two findings, 102 and 103, and the owner closed both the same
day** — 103 because requiring an SD password at the console is correct (the defect was a comment), 102 because
its subject was the installer-attached account, which he rules out of scope, and **the question he actually
cares about — is a STANDARD user restricted — was already witnessed green on `b211`** by `verify-apiadmin`
(*"API session was refused OS.EXECUTE by name"*, plus `$cred` refused both ways, on a real API connection).
Both are in HISTORY.md; 102's documentation half moved to **61**. `-Run` tokens `b206`–`b218` are spent.

***100 IS FIXED IN SOURCE AND NEEDS THE NEXT CYCLE*** (`newvoc/%t` → `%T`, `$KnownUnlisted` 1 → 0), then
`verify-accountmodel`.

***NEXT, IN ORDER.*** (1) **Owner, one UAC click:** 76's remainder, `verify-lcnames`, is in `VerifyInstall1`,
whose elevated legs start SD's own resident helper (the agent's helper cannot serve them) —
`powershell -ExecutionPolicy Bypass -File C:\Users\Don\SDCoreProject\sd4windows\sdb_ai\sd64\gplbld\VerifyInstall1.ps1
-Only verify-lcnames` from an **ordinary unelevated** prompt (it refuses an elevated one); its new
"voc_template absent" row has never run. `sdtestuser-admin` is exercised by the full suite's door pair.
Then a full suite by the owner — none has run since 18 Sep 10:30. (2) The ruled builds, which want one
cycle together: 59's reader hardening (C), 71's SDSYS-only cross-account password rule, 77's retired-ids
list (BASIC), and 100's rename if it is wanted. (3) 84's rewrite and 97's proposals.

---

## OPEN TASKS — RELEASE 1.1 (W1.1-0)

**15 open: 12 validated against the tree by the 27th pass, 21 Sep 2026, and 97, 100 and 104
added since (101, 102 and 103 closed 22 Sep) (64, 95, 96 and 99 closed the same day); 53 is deferred to W1.2 (its own section, below the gates).** Every call
that was the owner's has been ruled — he delegated them, 21 Sep 2026 — and each ruling
is in its entry. `B` blocks
the release, `S` should be fixed, `M` is minor. Each entry says what is open and
what is owed; **the row it came from, with every earlier status layered under it,
is in HISTORY.md under *"ARCHIVE 21 Sep 2026 — RELEASE_1.1_FIXES.md as it stood"*
— grep `| 64 |`** for the full text of an id. Release 1.1's two objectives
(owner, 11 Sep 2026) were the defects SD Core for Linux found in this tree and
embedded Python installed rather than shipped; the Python route is built and
witnessed (`verify-pyapi`, `verify-pygate`, §5.27).

### 104 · S — `sdsys\voc` and `sdsys\gpl.bp` are writable by every SD user, and the installer's hardening list does not name them

**Measured 22 Sep 2026, unelevated, on the 19:20:42 install.** `C:\ProgramData\SD\sdsys\voc` and
`…\sdsys\gpl.bp` both carry **`ace\sdusers = Modify, Synchronize`**, inherited. So does `…\shm` (that is 59)
and the `sdsys` and `SD` directories themselves. ***WHAT IS CORRECTLY LOCKED, AND IT IS MOST OF IT:***
`gcat`, `newvoc`, `messages`, `accounts`, `cat` and `os.users` all read **no ordinary-user write**, `$cred`'s
ACL is not even readable unelevated, and `C:\Program Files\SD` is clean. **The designed hardening works; these
two are the gap.**

***IT LOOKS LIKE AN OMISSION RATHER THAN A DECISION.*** `sd.iss:3444-3451` hands `secure-sysdirs.ps1` exactly
**seven** paths — `accounts`, `$map`, `messages`, `newvoc`, `bp`, `cat`, `sd.conf` — and that script's own
criterion is *"take Modify off the SDSYS system directories that nothing writes"*. `voc` and `gpl.bp` fit that
criterion and are simply not on the list. **Both look safe to add**: SDSYS's own VOC is rewritten by
`UPDATE.ACCOUNT` / `$LOGIN` mode 2 run **in SDSYS**, an administrator, and Administrators keep access through
the same grant; recompiling `GPL.BP` is already documented as an elevated window (`secure-gcat.ps1`).
***NOT VERIFIED — the `$ipc` precedent in `secure-sysdirs.ps1`'s header is exactly the trap*** ($ipc looks
lockable and is written by every session), so each one needs `probe-syswrites.ps1`-style evidence before it is
locked, and `verify-sysdiracl.ps1` is where a new row would go.

**WHY IT MATTERS ON ONE TRANSPORT ONLY.** `net_path_permitted()` returns TRUE for every path unless the
session is `CN_SOCKET` (`op_dio1.c:704`), and an ssh session is `CN_CONSOLE` — so from ssh, ordinary BASIC
(`OSWRITE`, `OPENSEQ`) reaches any path NTFS allows. **On that transport the containment is the NTFS ACL, not
SD.** An API session is contained and does not have this reach.

***THE ADMINISTRATOR ALREADY HAS TWO ANSWERS, AND THE OWNER NAMED BOTH, 22 Sep 2026: "the admin can remove the
ability to issue BASIC and RUN to any account, leaving them with only access to cataloged programs", and
"they can also lock them into an application and remove the break key."*** Both are real and standard
practice, and an account that never reaches TCL cannot reach any of this. ***THE OPEN QUESTION IS WHETHER
REMOVING `BASIC`/`RUN` IS A BOUNDARY OR A SPEED BUMP, AND IT IS NOT ANSWERED HERE***: an account's own VOC is
writable by that account (it must be), and `newvoc` is READABLE to it — so whether any remaining catalogued
verb can copy a VOC record back, or write a file by path, decides it. **Read the verb set before relying on
it.** That is a question about SD's shipped verbs, not about these ACLs, and the two fixes are independent:
locking the two directories costs nothing and does not depend on how any site configures its accounts.

### 100 · M — `newvoc/%t` is a mis-cased escape: FIXED IN SOURCE 22 Sep 2026, witness owed

***THE OWNER APPROVED THE FIX, 22 Sep 2026 ("a cycle is fine, it takes 90 seconds"), AND IT IS DONE IN
SOURCE: `git mv newvoc/%t` → `newvoc/%T`***, a case-only rename through a temporary name because
`core.ignorecase` is true and NTFS resolves the two to one file. `verify-accountmodel`'s `$KnownUnlisted` is
**1 → 0**, which is what that constant was built to announce, and its two count rows now require
`COUNT NEWVOC` and `LIST NEWVOC` to agree exactly. **Owed: a cycle, then `verify-accountmodel`.**

***THE RECORDED OBJECTION IS ANSWERED BY MEASUREMENT RATHER THAN OVERRULED.*** It was that the decoder's
case-handling had not been read. It has now: **`op_dio4.c:1135` decodes the `~` escape by testing
`*(p + 1) == 'T'`, upper case and first character only**, so a lower-case `%t` falls through to the generic
loop where PRE_RELEASE 128 keeps an unknown escape **literal** — the id reads back as `%t` and never as `~`.
The `UpperCaseString()` at `:1119` does not rescue it: it sits under `CASE_INSENSITIVE_FILE_SYSTEM`, which
`dh_open.c:581` records as *"a macro this tree never defines"*. So `%T` is what the decoder expects, and an
escape letter is not a name, which is why this one file is exempt from the lower-case rule.

**Still open underneath it, and NOT part of the approved fix:** `voc_template` has no `~` record at all
(re-checked 22 Sep — it holds `%E`, `%G`, `%L`, `%P` and their pairs, no `%T`), so **SDSYS's own VOC still
lacks it** even after this. That is a second change to a different file and was never ruled on. **And still
not measured:** whether `~` works as a keyword without the record at all — HISTORY notes that `<` and `>`
*"cannot be VOC records on this port"* yet work, which suggests the parser may not read them from the VOC,
and would make the whole thing cosmetic.

The original finding follows.

### 100 (as found) — `newvoc/%t` is a mis-cased escape: the record for `~` is undecodable and never reaches an account

Found 21 Sep 2026 by `verify-accountmodel` (its first passing run, `b213`). `COUNT NEWVOC` says
**395** and `LIST NEWVOC` prints and reports **394**; ten of the eleven names the listing does
not print are the `%`-encoded operator ids it prints decoded (`%E` `=`, `%G` `>`, `%L` `<`,
`%P` `%`), and the eleventh is **`sdsys/newvoc/%t`**, whose content is `Keyword to test
soundex code` / `33`. `op_dio3.c:42` says the directory-file mapping stores `~` as **`%T`**;
the 19 Aug 2026 commit `e1095ab` (*"Every SDSYS file name is lower case on disk"*) turned it
into `%t`, an escape the decoder does not know. **Observed:** a fresh account's VOC holds 398
records = the 394 listed `newvoc` ids + `$command.stack`, `$hold`, `$savedlists`, `bp`, so
**the `~` record reaches no account**; `voc_template` has no `~` record at all; `%t` is the
only lower-cased escape in `sdsys` (swept 21 Sep). **Not measured — and it decides how much
this matters:** whether `~` works as a keyword without the record (HISTORY.md carries a note that `<`
and `>` "cannot be VOC records on this port" yet work, which says the parser may not read
them from the VOC). **The fix, if wanted:** a case-only `git mv` of `newvoc/%t` to
`newvoc/%T` (mind NTFS: it is a rename through a temporary name), then a cycle, then
`verify-accountmodel`'s `$KnownUnlisted` goes 1 → 0 and its count rows go red until it is
changed, which is intended. **Objection to the fix, so it is not lost:** the lower-case rule
was made for record and file NAMES; an escape letter is not a name, but the decoder's
case-handling was not read, so whether it would accept `%T` is inferred from the comment.

### 76 · B (harness) — the four verifiers are converted to the SDSYS seat; two are witnessed

**Witnessed 21 Sep 2026, elevated through the agent helper, SDSYS signed in:** `verify-apiadmin`
and `verify-privundetermined` on `b211` — both exit 0; `verify-apiadmin` every row PASS with
its one designed N/A (the "not SYSTEM" row, unmeasurable once `OS.EXECUTE` is refused),
`verify-privundetermined` **27 of 27**; the `os.users\SDSYS` fixture was planted and removed
in both and the tree was left clean. **The first run, `b210`, failed at "credential set" in
both — an instrument fault, not the product:** `SET_ACC_PASSWORD` was reworded that day to
print `Password accepted.` and **eight** verifiers still matched `Password set for account`
(`verify-apiadmin`, `-apiname`, `-apiport`, `-apiwire`, `-doors-admin`, `-privundetermined`,
`-scramlogin`, `-vocwrite`); all eight are fixed and `test-verifieranchors-units.py` (free
tier, four mutants red) fails when a `verify-*` anchors on a phrase in its RETIRED table —
add a row there whenever a line a verifier matches on is reworded. **Still owed:**
`verify-lcnames` and `sdtestuser-admin` (the unelevated tier, `VerifyInstall1`), the
falsification check below (a local control run *without* the planted record was not done),
and the full suite.

Owner's ruling, 21 Sep 2026. **All four were converted in source:**
`sdtestuser-admin.ps1` and `verify-lcnames.ps1` earlier that day, and
`verify-apiadmin.ps1` and `verify-privundetermined.ps1` unattended overnight.
`test-logtoreaim-units.ps1` now reports **0 files still sending the refused prefix**
(its two rows for the last pair left the table in the same change) and
`test-sdsysseat-units` passes; both verifiers parse with the function counts they had
at HEAD. **What the last two do:** `Invoke-SDSys` is a plain seat call; `Invoke-SDIn
<personal account>` is `Invoke-SdSeatText -Commands (@("LOGTO $account") + ...) -Internal`
and refuses `SDSYS`; `Assert-SdSeat` runs twice (plain, then `-Internal`) before anything
is created. **The local `OS.EXECUTE` control** plants `os.users\SDSYS` immediately before
it and removes it immediately after, refuses to start if one already exists, and has a
`finally` backstop (`Set-SeatOsUsersRecord`/`Remove-SeatOsUsersRecord`, never overwrite,
never remove one they did not write); it adds two fixture rows to each verifier's tally.

**Owed:** one elevated run with SDSYS signed in, then a full suite (none since
18 Sep 10:30). **What would falsify the `os.users` fixture:** the local control passing
*without* the record, meaning `USR_ADMIN` survives the LOGTO under `-Internal` and the
record is unneeded; and **read the first red as a finding about the seat or the door
before reverting anything** — the `-Internal` door itself was witnessed on 20 Sep for
`verify-apiwire` and `verify-vocwrite`, which is the evidence it works, not for these two.

### 97 · S (harness) — the validation suites: upkeep cut, runtime still to do

***21 Sep 2026, overnight and unattended (owner asleep, judgement delegated; nothing
committed).*** **Done and verified:** `assert-current.ps1`'s 1,450-line hand-kept
`$neverShipped` list is derived — every `verify-/test-/probe-/check-/clean-*` file in
`gplbld` that `stage.py` and `sd.iss` do not name, plus a 40-name residual that
should not grow (equivalence proved over all three watched trees; a new `verify-*`
stays exempt and a non-family file still raises STALE, both run); `check-free-tier.ps1`
takes the free list from the directory (52 guards, 57 s, no registration and no
count); 14 unreferenced probes deleted; CLAUDE.md's 43 KB free-tier block archived
to HISTORY. **Not done, and it needs an attended session** because every change to
the elevated suite needs the owner's elevation to prove: **runtime**.

**Measured:** a complete set is cycle 3–12 min + free 1 + unelevated ~4.6 (26 steps,
no per-step logs exist) + elevated **15.4 (32 timed steps, 18 Sep)**. 30% of all
commits touch the 192 validation scripts (69,873 lines); `assert-current.ps1` (205
commits) and the two runners (46, 37) are the most-edited files in `gplbld` because
each new script was registered by hand in up to four places. **Where elevated time
goes:** literal `Start-Sleep` is only 32 s; it is account creation and deletion
(`delaccount` 14 creates/10 deletes, 65 s; `accountrules` 16 creates, 47 s) and
**service stop/start — each of the seven API-cluster steps (`apiremote`, `apiadmin`,
`apiname`, `apiport`, `scramlogin`, `relayidentity`, `peerlog`) contains about six**,
592 s together with `routes`, `sshadmin` and the account cluster.

**Proposals, by payoff, each unproven until run:** (a) one shared *API on* window —
the runner enables the API once, runs the cluster, disables it — with `verify-apiport`
(whose subject is the toggling) left standalone; (b) one shared account fixture for
`routes`, `accountrules`, `sshadmin`, `apiremote`, `createaccount`, `sshonly`,
`profiledir`; (c) log per-step durations in `VerifyInstall1` (the unelevated half has
none); (d) derive `VerifyInstall2`'s 20 hand-plumbed `*Prefix` parameters and their
`-Run` derivation from the step declarations. **Not built tonight: (a)-(d) all edit
the runners or the elevated verifiers, which cannot be run without him.**

**Ruled 21 Sep 2026 by the agent, on the owner's delegation (*"i have no opinion, you
make the call"*): all three verifiers stay.** `verify-privundetermined` (69 s, 1,035
lines) — the first reading here, *"two free guards cover its tables"*, was wrong: those
guards check strings, and the step's own header says the tri-state's logging *"has
never been executed by anything"* and that a zero looks identical whether the logging
works or was never reached; this step makes it non-zero on purpose three times and is
the only thing that proves the path fires, so 76's conversion of it stands. Its
unit guard `test-privundetermined-units` exists for that verifier's leg table and
goes with it if it is ever retired. `verify-lcnames` (1,093 lines) — already
converted in source; the lower-case standard is stable and this is its widest net, and
the churn was the 5.12 conversion rather than steady-state; one witness run is owed.
`verify-apiidentity` (failed 15 of 42 recorded runs) — it is the only witness of 55's
session-as-the-user property, so do 84's rewrite rather than retire it, in a session
that can watch it run, and keep `scram-probe.py` (`verify-scramlogin` uses it too)
until the rewrite is witnessed. **What would reverse these:** after its conversion is
witnessed, a verifier failing for an *instrument* reason more than twice.
**Examined and kept — do not retire on a second pass:** `probe-akwrite` (the only
witness of the alternate-key write path; `VerifyInstall2`'s own comment says so),
`verify-nonet` (5 s), the eight case verifiers (each a distinct mechanism, 5–7 s),
`verify-notyet`, `verify-cmdaudit`, `verify-elevdoor`. 32 of 65 steps have never failed
in 8–31 runs, but a clean record is what a regression guard looks like; the run
summaries do not say whether a failure was the product or the instrument.

### 84 · M (harness) — `verify-apiidentity.ps1` still drives `scram-probe.py`, not the real client library

64's slice 5a deleted `verify-tierapi.ps1` and left a debt: `verify-apiremote.ps1`
and `verify-apiidentity.ps1` were both owed the real-client-library reading it
held. **Half is paid:** `verify-apiremote.ps1` was rewritten 20 Sep 2026
(`5d435f9`) to drive `gplsrc/sdclilib/tests/api_admin_probe.c`
(`SDConnect`/`SDExecute`/`SDError`). **`verify-apiidentity.ps1` is untouched** and
still drives `scram-probe.py` (`f92e07a`, 42), a hand-written Python
reimplementation of SCRAM+TLS built because .NET's `SslStream` could not export
the RFC 9266 channel binding. **Built since (25th pass):**
`gplsrc/sdclilib/tests/api_identity_probe.c` on `SDOpen()` alone — compiles clean,
its connect half ran live against the real `sdwind` (wrong credentials refused,
wording captured), and a `check-api-identity` Makefile target exists. **Not
done: wiring it into `verify-apiidentity.ps1`.** It is not a drop-in swap:
`SDStatus()` does not reflect `SDOpen`'s failure the way the wire-level
`server_error` does, so it is a rewrite of a working file's core mechanism, and
needs elevation and/or real credentials in a session that can watch it run.
**Ruled 21 Sep 2026 (agent, on the owner's delegation): keep `verify-apiidentity` and
do this rewrite; it is not retired** — it is the only witness of 55's
session-as-the-user property (see 97).

### 77 · M — an upgrade never removes a VOC record

Reported by the Linux port 19 Sep 2026 and checked here. `login`'s `update.voc`
opens `@sdsys/newvoc`, selects it and writes each record into the account's VOC;
**it never walks the account's VOC**, so a verb deleted from `newvoc` stays in
every existing account for ever (the routine's one `delete` is the case-rename
arm). Reached by `UPDATE.ACCOUNTS`, the `$RELEASE` prompt and `upgrade-voc.ps1`'s
installer walk. **No retired-ids list exists beside `newvoc`.** **Inert today,
by measurement:** `v1.0-0` is `a2e04e4`, and exactly one `newvoc` deletion has
landed since (`a47526f`, 13 Sep, which moved `TIER.ADD.ADMINISTRATOR` and
`TIER.OMIT.STANDARD` to `tier.policy`; 64 then deleted `tier.policy`) — two dead
records in an upgraded VOC that nothing reads.

**Ruled 21 Sep 2026 (agent, on the owner's delegation), and the owner's one question
is answered: a withdrawn VERB record is removed even if it carries `[locked]`; any
other withdrawn record honours the lock.** Reasoning: his own ruling is that verbs are
not the user's to modify (*"every verb (119) because users should not be modifying
them"*), a withdrawn `V`/`IN` record's field 3 is a number that may now dispatch
somewhere else entirely, and overruling a lock on a removal hands the site nothing
where overruling it on a replacement hands them the new record. **To build, in the
conditional:** a retired-ids list shipped beside `newvoc`, named in the commit that
deletes a verb (the discipline `test-retired-wording-units`' `$RETIRED` table already
runs); `update.voc` visits only those ids, so 10166's promise (*"only ever visits
records SD ships"*) still holds; a walk of the account's VOC that deletes whatever
`newvoc` lacks would break it and is not to be built. `login` cannot be compiled by
`bbcmp`, so it needs a cycle and a witness: an account holding a retired verb loses it
across `UPDATE.ACCOUNTS`, and a locked non-verb record survives. **Not built.**

### 75 · S — SD requires a complex password even where the OS does not

Built 19 Sep 2026 (the owner found it running the cycle: Linux demanded a strong
password, ours took anything — both ports had been deferring to the OS, and
Windows' machine policy here is minimum length 0, complexity off). **Two of the
four prompts have been seen refusing a weak password and taking a strong one on
real cycles:** the finish page's SDSYS prompt (the PowerShell copy of the rule;
89 was found there) and its `MODIFY.PASSWORD` prompt (`set_acc_password` →
`pw_complex`; 91 was found there), 20–21 Sep. **Still owed:** a weak password at
`CREATE.ACCOUNT` (10920, then the retry) and at the elevated first login
(`require.credential`) — since 70 sets a password at install, the second needs an
account made without a `$cred`.

### 73 · S — `DELETE.ACCOUNT` says when files could not be removed; installed, never witnessed

Reported by Linux 19 Sep 2026. `delacc:307` discarded the result of the OS delete
(it assigned it to the confirmation variable), so a failed delete looked like a
successful one right after *"this cannot be undone"*. The fix tests the state
(`OS$EXISTS`), not the return code, and the deletion carries on. It is in the
installed tree (`delacc:333-335`, message 10919; `assert-current` exit 0 on the
21 Sep 01:16 install), and **10919 has never appeared in any transcript under
`SD-verify`.** **Witness owed:** a file held open in an account's directory during
`DELETE.ACCOUNT`.

### 71 · S — every account gains `modify.password`; installed, neither witness has run

Owner chose (a), 19 Sep 2026: *"as long the user can only modify their own
password, but the admin can change any password"*. `sdsys/newvoc/modify.password`
added; the split was already enforced (`set_acc_password:87-92`, `:123-126`), so
no code beyond the vocabulary entry. **Owed:** `MODIFY.PASSWORD` typed alone in
`don` (asks for the current password, succeeds) and `MODIFY.PASSWORD sdsys` from
`don` **unelevated**, refused with 2001. The false comment the row names now sits
at `set_acc_password:172-175`, unchanged.

**Ruled 21 Sep 2026 (agent, on the owner's delegation), on the nuance: an elevated
ordinary session must NOT be able to set another account's password — only SDSYS may.**
Today `K$ADMINISTRATOR` means *an elevated session*, so an elevated `don` can (checked:
`set_acc_password:147` tests only that flag). That is the reading of §5.6.1 (*"a Windows
administrator is an SD administrator"*), but 64 is newer and says there is one
administrator, SDSYS, and every other Windows administrator is refused; the wider rule
also buys no security, since an elevated Windows administrator can already rewrite
`$cred` by hand, so it only muddies which identity is accountable. Owner-chosen (a)
stands: everyone changes their own password (current one required). **To build, in
the conditional:** the cross-account branch additionally requires the session's
account to be SDSYS; install-time password setting runs as SDSYS through `sd -internal`
and so is unaffected — **which is the thing to check first, because it is the one
condition that would break the finish page** (does `@logname` read `SDSYS`, and in what
case, inside an internal session?). Compile-check with `bbcmp`, then a cycle, then the
two witnesses above plus `MODIFY.PASSWORD sdsys` from an **elevated** `don`, refused
with 2001. **Not built** — a shipped-BASIC change would make the installed tree stale
and force a cycle before the witnesses already owed can run.

### 69 · S — first-login credential wording fixed in four copies; witness owed

Fixed 19 Sep 2026 in `messages/10089`, `messages/10101`, `sd.iss`'s `/SILENT`
refusal and the hard-coded `crt` block at `set_acc_password:241-245` (the last is
why the wording lint now reads `gpl.bp`), with the stale comments. It said SD
asks for a credential every time; it asks only in an **elevated** session
(`login:1080-1089`), and what a missing credential costs is the *remote* doors.
Installed (`assert-current` exit 0, 21 Sep 01:16). **Witness owed:** an elevated
first login into an account with no `$cred`; since 70 no normal install produces
one, so make it by hand. **Ruled 21 Sep 2026 (agent, on the owner's delegation):
severity stays S, not B** — the wrong sentence is fixed and installed, nothing is
functionally broken, and what is owed is a witness, not a fix; the gap it exposed
(ssh and the API by default, no credential until an elevated login) is now stated
in the message. It becomes B only if the witness shows the message still wrong.

### 61 · B — the shipped documentation says things that are false

In `SDCoreWindowsDocs` (a separate repository, `de44f8e`, matching its remote):
`Administrator/markdown/01-accounts-and-security.md:85`, `:88`, `:165`;
`03-operating-system-access.md:189`; `05a-managing-accounts.md:101`, `:153` —
58 removed the administrator's API access, so *"Administrators have API access
and `OS.EXECUTE` access automatically"* is half false. **This is a pointer, not a
fix here.** Folded into 48's documentation task in practice.

**Added 22 Sep 2026 from RELEASE_1.1 102, which closed into this one.** §5.25 (*"administration requires an
interactive desktop"*) and §5.28 row 3 do not describe what an API session's Windows token actually is: for an
account that holds administrator rights it comes back **High integrity with `BUILTIN\Administrators` enabled**
(measured on SDSYS, 21 Sep 2026). **SD asks for no elevation** — `win32s4u.c:294` is `LsaLogonUser` with logon
type `Network` and nothing requests `TokenLinkedToken` — so that is what LSA returns, and **for a standard
account, which is every account `CREATE.ACCOUNT` makes, there is no admin half to return.** The documentation
should say what is true rather than what was assumed, in this repository's §5.25/§5.28 and in the shipped
pages this entry already lists.

### 59 · B — SD's own system segment is writable by every SD user, and a LocalSystem process reads it

Re-measured 21 Sep on the 01:16 install:
`C:\ProgramData\SD\shm\sd_shm_716d0301` still grants `ace\sdusers:(RX,W)`,
`sysseg.c:326` still creates it `0666`, `sdwind` still calls `check_lost_users()`;
**nothing of the remedy is built.** Measured 18 Sep unelevated with a control: an
ordinary Medium account opened it for write, the control (`sd.exe`) was refused,
the mtime did not move. **The privileged reader is real:** `sdwind.exe` imports
`msys-2.0.dll` and runs under the LocalSystem service; `check_lost_users()` walks
the user table in that segment, `kill(pid,0)`s a pid out of it and fork/execs
`sd -cleanup` as LocalSystem (`sdwind.c:257-290`). Reachable by an ordinary
account over ssh (an ssh session is `CN_CONSOLE`, and `net_path_permitted()`
returns TRUE for every path unless `CN_SOCKET`). **Not claimed: code execution
from it.** The remedy is a design, in the conditional, in the archived row.
Linux's copy is broader (`shmget(… 0666)`); reported to the Linux agent
18 Sep 2026.

***IT NEEDS NO `SH` AND NO `OS.EXECUTE`, AND THAT IS THE THING TO BE CLEAR ABOUT.*** Asked
22 Sep 2026 whether this and 53 are reachable only by an account holding OS access: **53 yes,
this one no.** The segment is an ordinary FILE (`C:\ProgramData\SD\shm\sd_shm_*`) whose ACL
grants `ace\sdusers:(RX,W)`, and `net_path_permitted()` returns TRUE for every path on a
session that is not `CN_SOCKET` (`op_dio1.c:704`). An ssh session is `CN_CONSOLE`. **So plain
BASIC file I/O — `OSWRITE`, `OPENSEQ` — reaches it from an ordinary account over ssh, with no
OS grant of any kind.** Over the API it is blocked, that being the one transport the gate
covers. **53 is different**: it was measured with a compiled program run as a local Windows
user, which an SD-created account cannot become (`sdsshonly` denies console and RDP, ssh gives
a `ForceCommand`'d SD session) — so for an SD account 53 does need `SH`/`OS.EXECUTE`, while its
real population is any local Windows user, who needs no SD grant at all.

**Ruled 21 Sep 2026 (agent, on the owner's delegation): it stays B and 1.1 does not ship
without a hardening of the privileged reader; the broker re-architecture is deferred
to W1.2.** The archived row's remedy — move the privileged surface into a small native
broker so `sdwind` can drop to an unprivileged account — is the right end state and
would also dissolve 53, but it is a redesign of the service on a release that still has
its parity audit, documentation and packaging gates to pass (47→48→49), and 64's own
instruction is to *remove* framework, not build new. The segment cannot be fixed by a
DACL (every session writes it, `stage.py:600`), so **the reader must trust nothing in
it.** **To build, in the conditional:** in `check_lost_users()` (`sdwind.c:257-290`)
and `cleanup()` (`clopts.c:295`, `:359`) take the table's base, stride and count from
the daemon's own constants, never from the segment's header (`UPtr` in
`sysseg.h:227` takes all three from the writable segment, which is why 60's string
bounds were not the fix for the class); read one integer `pid` per slot into a local
and validate it; never hand a string from the segment to `fork/exec` — `sd -cleanup`
gets a slot number only. **What would falsify it:** `sd -cleanup` turning out to need
a per-user string from the segment, in which case that string must be re-derived from
a trusted source (the account register). **Witness, in the conditional:** with the
service running, an ordinary account writes hostile values into the segment (huge
count, negative stride, `pid` 1, a 200-character string) and the daemon stays up and
starts no `sd -cleanup` for the forged slot. Reading the C and compile-checking it
with MSYS2 gcc are possible unattended; **running it is not** — it needs a cycle. **Not
built.**

### 47 → 48 → 49 · B — the release gates, in order, none started

Owner via the Linux mailbox, 15 Sep 2026 18:12. **47 is gated on every other 1.1
task above; 48 on 47; 49 on 48.**

- **47 — Windows↔Linux parity audit.** Audit feature and behaviour parity and
  resolve what it finds. Linux's matching task waits on our "1.1 done" call, so
  this is the shared critical path. *Done when* a written comparison exists and
  its findings are resolved or filed. No parity document exists in either
  repository.
- **48 — documentation current with 1.1.** Bring `SDCoreWindowsDocs` up to date
  with every W1.1 change (API TLS, the SDSYS elevation gate, `delete.account`'s
  skip, the VOC-write fix, prompt defaults, …) — it still describes account tiers
  on more than a dozen pages, which 64 made false. **Absorbs old 18:** rebuild the
  sets with `tools\release.ps1` and copy the corrected bound PDFs from
  `<Set>\book\` into the release's `documentation\` before zipping, so the 29
  `-ExecutionPolicy Bypass` fixes in `SDCoreWindowsDocs 76e1dce` reach the shipped
  PDFs (assembly is a hand step with no script). Linux starts its documentation
  from the finished Windows docs, so name the shape early.
- **49 — the W1.1 staging directories and zips**, one Windows and one Linux.
  **Settle first, and before 48 documents an install procedure:** is a release
  zip a source snapshot (the installer would have to clone a *tag*) or an artifact
  the installer builds from? The Windows installer is an Inno `.iss` build of a
  staged tree (`sd.iss`, `stage.py`), not a git clone, so the clone-a-tag hazard
  may not apply here — but the choice must be pinned and compared with Linux. No
  W1.1 staging directory or zip exists (only `SDCore-W1.0-0.zip` and the cycle's
  `sd-setup-W1.1-0.exe`).

---

## DEFERRED TO W1.2

Not open for 1.1 and not done: **out of the open count above**, not struck (that reads
as done) and not left as an open 1.1 row (owner's rule, 16 Sep 2026). Each entry says
what would bring it back.

### 53 · S — an ordinary local user can open the SD service's MSYS2 shared section for write

***Deferred to W1.2, ruled 21 Sep 2026 by the agent on the owner's delegation.*** It
is the MSYS2 runtime's own design rather than SD code, the only remedy is to take the
runtime out of the LocalSystem daemon, and that is the same re-architecture as 59's
broker — so it goes with it, and 1.1 ships 59's hardening instead. **Until the
deciding experiment is run, no document may say a local user *cannot influence* the
service through this section** — the claim is unmeasured, and saying less is the
honest wording for 1.1.

Measured 16 Sep unelevated (`probe-cygshared.c`): in `msys-2.0S5-11f4a83b0f193bff`
(inferred to be SD's runtime — it holds LocalSystem's `S-1-5-18.1`), `shared.5` opened
**READ and WRITE** as `ace\Don` at Medium integrity; at **Low** integrity, WRITE no on
every section (0 of 8). Re-measured 21 Sep: the installed `sdwind.exe` (20 Sep 22:38
build) still names `msys-2.0.dll`; `sdsvc.exe` and `sdtlsrelay.exe` do not. **The first
task when it returns:** the deciding experiment — whether a write into `shared.5` can
influence a LocalSystem MSYS2 process — before any remedy is chosen. 59 rules out the
cheap option of a separately-pathed `msys-2.0.dll` copy, since SD's segment and
semaphores live in that namespace. **What brings it back into 1.1:** the experiment
showing influence is possible, or the broker work in 59 being pulled forward.

---

## 0. Maintenance rules

Revised 14 Aug 2026, seventh session, on the owner's instruction: **the
documentation was taking more of a session than the work.** The rules below
replace a longer set that caused it.

**Audience: the next AI session. Not the owner — he does not read these.** Write
for a cold agent that will act on this: terse, factual, `file:line` over
description. No emphasis for effect, no narrative, no argument. The `changelog`
is the exception and stays plain English for users.

> ***THE MOJIBAKE SCAN HAS AN EXPECTED VALUE OF ONE, AND SINCE 5 Sep 2026 THE
> FILE IT APPLIES TO IS [HISTORY.md](HISTORY.md), NOT THIS ONE.***
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
> written as a count. **Do not paste the sequence into any new prose in either
> file** — naming the bytes keeps the expected value at 1, and a second literal
> copy would break the check this paragraph exists to make cheap.
>
> ***THE COUNT MOVED BECAUSE THE ENTRY DID, AND THE TOTAL IS UNCHANGED.*** The
> 21 Aug 2026 entry sat inside START HERE's superseded handoff stack, which was
> archived into HISTORY.md on 5 Sep 2026. **Measured either side of the move:
> `PROJECT_STATUS.md` 1 → 0, `HISTORY.md` 0 → 1.** So **this file now expects
> 0**, like every other tracked file, and HISTORY.md is the one with the
> exception. **A paragraph stating an expected value is itself something that
> goes stale when the thing it counts is moved** — this one did, in the same
> session, and was caught only because the move's own encoding check read it.
>
> **The same is NOT true of any script or any other tracked file: there the
> expected count is 0.** Measured 30 Aug 2026, and `HISTORY.md` — which since
> 21 Sep 2026 also holds the archived `PRE_RELEASE_FIXES.md` — still measured
> exactly 1 after that move. The underlying rule is `CLAUDE.md`'s — a tracked
> file is edited with `Edit`/`Write` and never by a program — and this paragraph
> only stops its verification from costing an investigation each time.

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

> ***A TASK THAT FINISHES IS DELETED, NOT STRUCK — AND A NEWER STATUS REPLACES
> AN OLDER ONE, IT DOES NOT SIT ON TOP OF IT.*** Owner, 26 Aug 2026: *"i have
> been getting a different list of things left to do each time i ask"*; and
> 21 Sep 2026: *"there should be only one [source of truth], focused on the tasks
> currently at hand"* and *"the goal here is to reduce bookkeeping by at least
> 75%"*. **A reader stops at the first status sentence**, so an entry that leads
> with a superseded "still open" paragraph and corrects itself further down
> misleads everyone who does not read all of it; a struck row still reads as
> evidence; and a status prepended each session is how two register rows reached
> 50 KB each. So: **each OPEN TASKS entry opens with its current status; when the
> task closes, delete the entry** (append its story to HISTORY.md if worth
> keeping); **when part of it closes, rewrite its first sentence** to say what is
> left. The checker that compared copies of a status (`check-stale-leads.py`) was
> retired the same day, because there is one copy.

1. **Same commit as the work.** If a commit changes what builds, runs, is
   decided, or is next, it changes this file.
2. **Verified means you watched it, this session.** Compiling is not running.
   Otherwise the task stays open and its entry says what is unwitnessed,
   whatever an earlier session claimed.
3. **One fact, one place.** Do not restate a finding in OPEN TASKS, §5, §6 and
   HISTORY. Put it where it belongs and point at it. Duplication is the main way
   this file got large.
4. **§6 traps: anything that cost real time.** What happens, what to do. This
   section is meant to grow; never cut a trap for size.
5. **Size follows from the rules above, not from a ceiling.** OPEN TASKS holds
   only what is open, each entry states its current status in its first
   sentence, and anything that is history goes to HISTORY.md in the same commit.
   Do not print line counts in the text and do not re-measure to keep a printed
   number true — that loop cost a dozen tool calls on 14 Aug 2026.
6. **Corrections: fix the text, say so in one line, move on.** No separate
   ceremony. HISTORY stays append-only, except that everything dated before
   1 Sep 2026 was cut on 21 Sep 2026 (owner) — see its rule 1 for where it is.
7. **Absolute dates.** Never "today" or "last session".
8. **User-visible changes go in `sdb_ai/sd64/sdsys/changelog`**, same commit.
   New or changed verbs, messages, files, login behaviour, configuration.
   Refactors, findings and traps do not. **Writing one no longer costs a
   cycle** — it is exempt from `assert-current` since 21 Aug 2026, header
   item 1 — so there is nothing left to weigh against obeying this rule.

**Time budget: documentation is a small fraction of a session.** If it is
approaching half, stop and cut.

---

## 4. Verified vs unverified

**Only the two elevation facts CLAUDE.md cites stay here.** The verifier inventory
(§4.0), *Verified by observation* and *Not verified — treat as unknown* moved to
HISTORY.md, *"ARCHIVE 21 Sep 2026 — PROJECT_STATUS.md before consolidation"*: they
are state that goes stale, and the suite's own output is the current record.

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
   they are not on it, and `assert-current` exempts them (every `verify-`,
   `test-`, `probe-`, `check-` or `clean-` file in `gplbld` that `stage.py` and
   `sd.iss` do not name) precisely because they cannot reach an install.
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
> ***12 Sep 2026, ON THIS MACHINE (`C:\Users\Don\SDCoreProject`): THE FIRST ROW
> OF THAT TABLE DID NOT HOLD.*** A **direct** `Start-Process -Verb RunAs` from
> the agent's shell — the case measured 4× on 23 Aug as **WORKS** — was refused
> with *"The operation was canceled by the user"*, launching
> `probe-pysystem.ps1` through a wrapper. **One attempt, not repeated.**
>
> ***WHAT IS NOT KNOWN IS WHICH OF TWO THINGS IT WAS***, and the two are
> indistinguishable from inside: the owner may have seen a consent dialog and
> declined it, or no dialog may have rendered at all — that second case is
> §4.0.1's nested-elevation signature, and *"canceled by the user"* with nobody
> asked is exactly how it reads. **The 23 Aug measurement was taken on the other
> machine and under a different harness**, so this is not evidence that it was
> wrong then. ***DO NOT SPEND A SECOND ATTEMPT RESOLVING IT BY GUESSING***: ask
> the owner whether a prompt appeared. If none did, the practical rule is
> unchanged and wider than the suite — **hand elevated commands over**.
>
> **NOTHING WAS LEFT BEHIND**, checked immediately: no `SDProbePySystem`
> scheduled task, no transcript, `0` payload files in `%SystemRoot%\Temp`. The
> refusal happens before the script starts, so it costs nothing but the attempt.
>
> **NOTHING IS LEFT BEHIND WHEN IT FAILS THIS WAY** — checked 23 Aug: no `b16`
> user or `sdu_` group, no `os.users` record, `batch.jobs` empty, no stray
> `sd.exe`. `verify-osusers` says so itself: *"Nothing was measured and nothing
> was left behind."* **So the token is NOT spent and can be reused.**

***21 Sep 2026 — THERE IS NOW A ROUTE AROUND "ONLY DIRECTLY", AND IT COSTS ONE CLICK PER
SESSION.*** `.claude/tools/agent-elevate.ps1 -Start`, run by the owner from an ordinary
prompt, launches a resident elevated helper (one UAC click). After that the agent runs
`agent-elevate.ps1 -Run -Script <repo>\sdb_ai\sd64\gplbld\<name>.ps1 -ScriptArgs <words>` and
gets the script's real exit code plus its captured output (in
`%LOCALAPPDATA%\SD-verify\agent-elevate\`, printed by the client). ***CALL THE CLIENT
DIRECTLY FROM A POWERSHELL SESSION, WITH `-ScriptArgs '-Run','b210','-Only','x'` AS A REAL ARRAY***
— measured 21 Sep: through `powershell -File`, or from bash, the comma list arrives as one
string and the runner refuses *"-Run was not given"* without running anything. `-Stop` ends it and it
stops itself after 60 idle minutes. **Proved live, 21 Sep 2026:** exit 0 and exit 1 both
arrive with their output, and the *server* refuses a script outside `gplbld`, a `..` path,
an unsafe argument and a raw path. **Limits, so it is not over-read:** only a `.ps1` directly
in `gplbld`, with plain arguments; a run is killed at 30 minutes (exit 124); **it cannot
run `cycle.ps1`** — the installer's finish page asks for passwords in windows a hidden,
non-interactive process cannot answer — **and it does not lift the rule above**: the full
suite's parent must stay unelevated and nested elevation is still refused. **The intended
use, not yet tried:** an elevated verifier step, `VerifyInstall2.ps1 -Run bNNN -Only <step>`.
**The allow-list stops accidents, not an agent that writes a script into `gplbld`.** Free
guard: `test-agentelevate-units.ps1`.

## 5. Decisions and why

Do not undo these without reading the reasoning.

### 5.28 The security model after RELEASE_1.1 64, evaluated (21 Sep 2026)

64's decision made this part of itself: *"Once everything is removed, we will evaluate
the resulting security model."* (The decision is verbatim in HISTORY.md, RELEASE_1.1 64's
archived row and its closing entry of 21 Sep 2026.) **What survives 64 and must not be swept
up:** 60 (bounded copies in `clopts.c`), the TLS/SCRAM tunnel (41, 42), 55's
session-as-the-user handover and its SID-ACL'd pipe, and the `secure-*.ps1` ACL
hardening. **Method and limit: read from source this session
(`op_sh.c`, `login`, `cproc`, `createa`) and joined to measurements already in the
record (55, 59, 53, 60). Nothing was run, and this is not a penetration test** — every
runtime claim is marked as reasoned.

| principal | what it holds | enforced by |
|---|---|---|
| SDSYS, the Windows account of that name, elevated | the **only** SD administrator: the session flag is granted at login after `elevate('START')` (`login`: `admin.granted = kernel(K$ADMINISTRATOR, 1)`) | LOGIN; `LOGTO SDSYS` is refused outright (`cproc`, 10002); `sd -internal` is forced to SDSYS by `sd.c` and needs LOGIN's one-shot marker (82) |
| any other Windows administrator | an ordinary SD account like everybody else; refused SDSYS | LOGIN |
| every ordinary SD account, USER and GROUP | the whole of `newvoc` (the former PROGRAMMER level; no tiers); ssh and the API **by default** — silence means both (`createa:611-615`) | `createa`; the `sdssh` and `sdapi` Windows groups |
| OS.EXECUTE, `SH` and Python, for that account | **default deny**: `os_user_permitted` (`op_sh.c`) allows only an internal program, the administrator flag, or `os.users\<login>` field 2 = `yes`; `os.users` ships empty and `CREATE.ACCOUNT` no longer writes a record | `op_sh.c`; the Python gate calls the same function (RELEASE_1.1 23) |
| an API session | TLS + SCRAM; runs **as** the authenticated user (55); confined to its account root, nine read-only SDSYS entries and `NETDIRS` | `apisrvr`; the containment gate in `op_dio2.c` |
| the data tree | `$cred` readable only by SYSTEM and Administrators; the rest per the `secure-*.ps1` scripts | Windows ACLs |

**Findings, worst first:**

1. **59 (B)** — the LocalSystem daemon `sdwind` reads a segment every SD user can write.
   Ruled in its entry: 1.1 hardens the reader so it trusts nothing in the segment; the
   native-broker redesign is W1.2.
2. **53 (deferred to W1.2)** — an ordinary local user can open the daemon's MSYS2 shared
   section for write; whether that can influence the service is **unmeasured**, so no
   document may claim it cannot.
3. **The decision text and the build disagree about OS-level access, and the build is the
   safer one.** 64 says *"the only limit on what they can do at the OS level is that
   imposed by Windows on its standard accounts"*; what is built is default-deny per
   account (table above). The worry recorded in row 64 — that if `os.users` retired,
   every account, remote ones included, could start an interpreter — **does not apply,
   because `os.users` did not retire.** **Ruled 21 Sep 2026 (agent, on the owner's
   delegation): default-deny stays.** 59 and 53 are why a remote interpreter is worth
   more to an attacker than it looks, and an administrator can still grant it per
   account. The documentation must say *no OS access until an administrator grants
   it*, not *Windows' limits*.

   ***AND THE GRANT IS THE ADMINISTRATOR'S DECISION, NOT SD's — OWNER, 22 Sep 2026:
   "if the admin chooses to give a user api access and os.execute access that should be
   respected as their choice", and "same thing with remote ssh."*** This closes a question
   RELEASE_1.1 102 opened and is recorded here because it is the kind of thing a later
   session re-proposes: **a transport test on `os_permitted()` — refusing `OS.EXECUTE` on a
   `CN_SOCKET` session even when `os.users` field 2 says yes — is REFUSED, not deferred.**
   Default-deny and this ruling are not in tension: the fields stay off until somebody sets
   them, and once set the product honours them on every route. **What is owed instead is
   disclosure** — an administrator turning `os-on` for an account that also holds `sdapi` or
   `sdssh` should be able to find out what that combination means (61, 48).
4. **Every account has the remote doors by default but no credential until an elevated
   interactive sign-in (69).** That fails closed — an account with no `$cred` cannot
   authenticate remotely — and the message now says so.
5. **A Windows administrator can grant themselves anything by hand** (`os.users`,
   `sdssh`, `sdapi`, `$cred`). By the owner's 21 Aug 2026 ruling this is out of scope
   (*"if users want to degrade security after the fact, that is their right"*): the
   model defends the product **as delivered**, and 95's fix keeps the installer from
   doing it for them.
6. **What 64 removed is what it gained:** no tier boundary to cross, no
   administrator-as-themselves bypass, no promotion or demotion paths, no second
   administrator identity — fewer places for a boundary bug to sit.

**Carried forward from the 24 Aug record, still true and not re-measured:** an
application's own `OS.EXECUTE`/`EXECUTE` built from user input is an escape (less
reachable now that OS.EXECUTE is default-deny); and on a machine where SD did not
install the ssh server, `ForceCommand` is never written, so a user reaches `cmd.exe`
and never meets SD (`git show 07b0e49:PROJECT_STATUS.md`, §8 *how many kinds of user*).

**Not examined, and worth doing in 47's parity audit or 48's documentation pass:** the
phantom and background-process path, and ssh's `ForceCommand` on a real second machine.
**What would change these rulings:** the 53 experiment showing influence is possible;
a measurement showing the `os.users` default-deny can be bypassed by an unprivileged
account.

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

***AND SUPERSEDED AGAIN ON THE ADMINISTRATOR SIDE, 5 Sep 2026 — READ §5.25.***
This section's "the console belongs to administrators" half is now the *whole*
of an administrator's remote story rather than a preference: an administrator is
refused any session that did not start on this machine, over ssh and over the
API alike (PRE_RELEASE 167 and 170, witnessed on `b122` and `b126`). What was a
statement about who *should* use the console is now enforced.

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

**Reopened as a plan for the release after W1.0-0, 10 Sep 2026 — not decided in
detail, not started.** The owner intends to bring Python back installed on the
machine rather than shipped in the installer. §8 "Python after W1.0-0" holds the
plan, its constraints and what would falsify it. This section still describes
the tree and W1.0-0.

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
| ~~`EUID_SET`/`EUID_RESTORE`~~ — ***CODE REMOVED 5 Sep 2026***, whole chain: `sdext_eguid.c`, both `GPL.BP` wrappers, `define_install.h`, the two `$ifndef IS_INSTALL` blocks and `privileged_commands` in `CPROC`, plus the SDEXT keys 102/103 and errors -10400 to -10403. PRE_RELEASE_FIXES 168 | gone | the service model (§5.7); no direct equivalent, and none wanted |
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

### 5.27 Python runs in a helper process, not inside `sd.exe` (owner, 11 Sep 2026)

***RULED.*** Owner, 11 Sep 2026, opening W1.1-0 and choosing between the two
shapes §8 had put to him. **Python comes back as a separate native process that
SD talks to, not as a library loaded into `sd.exe`.**

***NOTHING IS BUILT. THE PARAGRAPHS BELOW ARE A DESIGN AND A REASON, NOT A
RESULT*** — no helper exists, no protocol is written, and no Python has been
loaded by anything in this tree since `489b18e` removed it on 13 Aug 2026.

**The shape.** A native UCRT64 `sdpy.exe`, built the way the client DLLs are
(§5.3), started per session and spoken to over a pipe; the `PY_*` BASIC
subroutines become requests to it.

**Why, and the first reason is the only one that is measured.** §5.3's rule —
the MSYS2 and native runtimes never meet in one process — is the project's, and
it was paid for. Everything after it is reasoning:

- `python.org`'s Python is a **native** build and `sd.exe` is MSYS2, so loading
  one into the other mixes the runtimes. `long` is 8 bytes on one side and 4 on
  the other.
- The removed code passed a C `FILE*` straight into `PyRun_File`
  (`sdext_py.c:207` at `489b18e^`), which does not survive two C runtimes.
- A crash in the helper kills the helper rather than the SD session.
- It is a natural place for the `os_permitted()` gate §8 constraint 4 requires,
  since Python's `os.system` never reaches `op_sh.c:156`.

***THE REJECTED ALTERNATIVE IS WORTH KEEPING, BECAUSE IT IS THE ONE THAT LOOKS
CHEAPER.*** A native shim DLL loaded by `sd.exe` exposing only fixed-width types
would work in principle and needs no protocol — **and it breaks §5.3
deliberately.** It was put to the owner with that cost stated and he chose the
helper.

**What would falsify the ruling**, and it is one measurement rather than an
argument: a native `python314.dll` loaded into `sd.exe` through a fixed-width
shim, exercised, and run clean. **Nobody has attempted it.** If it worked, the
helper and its protocol are unnecessary.

#### ✅ BUILT AND DRIVEN, 12 Sep 2026 — `gplbld/sdpy.c`, **27 of 27 over a real pipe**

***THE HELPER EXISTS AND WORKS.*** Owner: *"build it - and feel free to improve
the embedded python system if you can."* `build-sdpy.ps1` → **150,788 bytes, 0
warnings at `-Wall -Wextra`**, UCRT64 gcc 16.1.0, linked `-lpython3` at a 3.13
floor and running **3.14.7**. `test-sdpy-units.ps1` drives the **real binary
over a real pipe** — not a model of it — **27 of 27, exit 0**. No install, no
elevation, no run token, no SD.

**Implemented**: `HELLO`, `PING`, `INIT`, `ISINIT`, `FIN`, `QUIT`, `RUNSTR`,
`STRSET`, `STRGET`, `OBJTYPE`, `OBJLEN`, `DELOBJ`, and ***the dict and list
families*** — `DICTCRTE`, `DICTCLR`, `DICTKEYS`, `DICTVALUES`, `DICTVSET`,
`DICTVGET`, `DICTIDEL`, `LISTCRTE`, `LISTAPPD`, `LISTCLR`, `LISTGET`
`RUNFILE` and `GETATTR` (**53 of 53**, 12 Sep 2026).

***THE VERB SURFACE IS COMPLETE: ALL TWENTY `PY_*` NOW HAVE A HELPER VERB
BEHIND THEM***, checked one at a time against the inventory rather than
counted.

#### ✅ ***THE TWO RUNTIMES CAN TALK — MEASURED 12 Sep 2026, 9 of 9***

***THIS IS THE ASSUMPTION THE WHOLE RULING RESTS ON AND NOTHING HAD EVER TESTED
IT.*** §5.3 says the MSYS2 and native runtimes never meet in one process, and
§5.27 chose the helper over a shim DLL on that ground — **but "they must not
share a process" is not "they can talk", and no line in this tree had shown the
second.**

`gplbld/sdpy_client.c` is SD's side of the pipe: **MSYS2 code, compiled with
`/usr/bin/gcc` — the compiler `sd.exe` is built with (`Makefile:48`)** — driving
the **native UCRT64** `sdpy.exe`. `build-sdpyclient.ps1` builds and runs it.
**Nothing of Python appears in that file**; no Python header, no link line, only
bytes on a pipe.

| | |
|---|---|
| start + handshake | an MSYS2 process starts the native child and `HELLO` agrees |
| `PING`, `INIT` | the child runs **3.14.7** behind the stable ABI |
| ***marks and NUL*** | a value carrying `@fm`/`@vm`/`@sm`, a **NUL** and a newline round-trips ***byte for byte*** across the boundary |
| failure | a raising script returns its traceback rather than a broken pipe, **and the pipe is still in step afterwards** |
| shutdown | `sdpy_stop()` sends `QUIT`, closes and reaps without hanging |

**Win32 `CreatePipe`/`CreateProcess`, not `fork()`/`exec()`**: MSYS2 emulates
fork at cost and with its own failure modes, and the child is a native program
that knows nothing about the emulation.

*(The compile met the trap `Makefile:150` already records for the UCRT64
compiler — `gcc.exe` finds its own DLLs, the `cc1.exe` it spawns resolves
through `PATH`, and without it the compile dies with "cannot open shared object
file" and writes nothing. The build script sets it and says why.)*

#### ✅ ***THE OPCODES ARE WIRED — 12 Sep 2026. `sd.exe` LINKS CLEAN AND THE TREE IS STALE ON PURPOSE***

**The C half of the integration is done and compiles.** `sd.exe` links at
**2,004,386 bytes** against 1,969,871 for the 11 Sep build, **0 warnings** on
every new file.

| | |
|---|---|
| `gplsrc/sdpy/sdpy.c` | the helper, **its own directory** for `sdsvc`'s reason — `TEMPSRCS` is a wildcard over `gplsrc/*.c` and would compile a native source with POSIX flags |
| `gplsrc/sdpy_client.c`, `sdpy_session.c` | MSYS2, **inside `sd.exe`**, named in `gpl.src` |
| `gplsrc/op_sdpyobj.c` | the 14 object verbs |
| `op_sdext.c` | the 6 lifecycle and run keys, added to the switch that already carries SCRAM |
| `opcodes.h` | ***`0xCFFE` UN-RETIRED AT THE SAME NUMBER*** — which is exactly why it was retired in place rather than deleted |
| `err.h` | the `-12001`…`-12034` codes restored **unchanged**, plus one new |
| `Makefile`, `gpl.src` | an `sdpy` target calling `build-sdpy.ps1`, and three new objects |

***THE GATE IS BUILT, AND IT IS WHERE CONSTRAINT 4 SAYS IT MUST BE.***
`sdpy_session.c` decides **once per session, at the moment the process is
started** — not per call, because the process *is* the privilege. It calls
`sd_os_permitted()`, a new **wrapper** round `op_sh.c`'s `Private
os_permitted()`: ***a wrapper and not a copy***, because Python's `os.system`
never reaches `op_sh.c:156`, so a session that may not use the shell must not
get an interpreter, and two implementations of that rule would drift silently
in the permissive direction. **`PRIV_WHY` is carried, not flattened** — "not
permitted" and "could not determine" both refuse and say different things.

***CORRECTED 13 Sep 2026 — RELEASE_1.1 23. THE WRAPPER AS BUILT CALLED ALL
THREE TESTS, AND THE FIRST ADMITTED EVERY USER.*** The opcode that starts the
helper runs inside `!PY_INITIALIZE`, whose flags word is `0x22`
(`HDR_INTERNAL`), so `os_permitted()`'s first test answered TRUE before the
username was read; the `os.users` branch was unreachable and every elevated
run agreed, on `USR_ADMIN`. `os_permitted()` is now split — test 1 stays, tests
2 and 3 are `os_user_permitted()`, and `sd_os_permitted()` calls that — which
is the shape constraint 4 specified. Still one body. `verify-pygate` is the
witness, unrun at the time of writing.

***AND ONE NEW ERROR NUMBER, `-12040`, BECAUSE THE HELPER IS A PROCESS.*** It
can fail in a way an in-process interpreter never could: not be there. Every
other code describes something Python said; this one describes not having
reached Python at all, and a caller deciding whether to retry needs them apart.

***THE OPCODE LAYER IS NUL-LIMITED AND THE PIPE IS NOT — SAY SO RATHER THAN
IMPLY OTHERWISE.*** `getarg()` and `SDEXT` hand up **NUL-terminated C
strings**, so a value containing NUL is truncated *before* it reaches the pipe.
Marks pass through perfectly well. `sdpy.exe` and `sdpy_client.c` both carry
explicit lengths and move any byte; **the end-to-end contract is "any byte
except NUL"**, and the limit is this layer's, not the protocol's. The same
sentence is already true of SCRAM — see the note in `keys.h`.

***WHAT IS NOT DONE: THE BASIC HALF.*** `syscom/KEYS.H` has **zero** Python
keys (the C `keys.h` kept all of them, which is why this step was small),
`SYSCOM/ERR.H` needs regenerating with `gen_includes.py`, `BCOMP`'s intrinsics
table and its **positional** `on i gosub` list need `SDPYOBJ` back, and the 20
`PY_*` programs do not exist. **Nothing has been run against an install.**

***THE TREE IS STALE, WHICH IS THIS STEP PAYING THE CYCLE IT PROMISED TO PAY
ONCE.*** `assert-current` refuses, naming `gplsrc\err.h`, `sdpy_client.*` and
`sdpy\sdpy.c`.

***`GETATTR` DOES NO getattr, AND THE NAME IS THE ONLY THING THAT SAYS IT
DOES.*** `SD_PyGetAtt` at `489b18e^` is `PyMapping_GetItemString(global_dict,
Arg)` — fetch a name out of the namespace and `str()` it. **So it is the
GENERAL reader** and `STRGET` is the str-only one. That division is now
enforced: `STRGET` on an integer answers **-12019** *"not a String"* rather than
blaming the encoding, which is the old contract restored; `GETATTR` reads the
same object as `42`.

***`RUNFILE` IS WHERE THE HELPER SHAPE PAYS FOR ITSELF.*** The removed code did
`fopen()` inside `sd.exe` and passed the `FILE*` into `PyRun_File`
(`sdext_py.c:207`) — a stdio handle crossing from the MSYS2 runtime into the
native one, which §5.3 says does not survive and which this section cites as a
reason for the helper. **Here SD sends a path, which is just a string, and the
file is opened on the side that reads it.** Compiling with the real filename
makes a traceback name the script and its line — driven, and the `-12006` for a
missing file **names the path it tried**.

***THE LIST SEPARATOR IS `@fm`, AND EVERY `PY_*` HEADER SAID OTHERWISE.***
`PY_DICTGETKEYS` and its neighbours all document *"tab separated list"*; the C
beside them joined with `PyUnicode_FromString("þ")` — **U+00FE, which IS
`@fm`** — with the tab version commented out one line above. **The code was
right and the headers were stale**, the same shape as the `CREATE.ACCOUNT`
grammar SD Core for Linux filed as bug 4. Measured at `489b18e^`; the rows hold
the code's answer.

**Two deliberate divergences from the removed behaviour, recorded because they
are decisions and not drift:**

- ***AN EMPTY COLLECTION IS NO LONGER AN ERROR.*** The old code returned
  `SD_PyErr_NoItems` (**-12030**) for an empty dict or list, so every caller had
  to special-case a perfectly normal state. It is now status **0** with an empty
  payload, which `DCOUNT` reads as 0 with no special casing.
- ***`LISTCRTE` IS NEW, AND ITS ABSENCE LOOKED LIKE A GAP RATHER THAN A
  DECISION.*** The removed API could append to a list, clear one and read one —
  but could only **create** one by running a script that said `x = []`.

***A LIMIT WORTH KNOWING RATHER THAN HIDING: a key or value that itself
contains `@fm` makes an ambiguous list.*** It is inherent to a mark-joined
string and not fixable inside that format. **The removed code had the same hole
and nothing said so**; `DCOUNT` on the result is where a caller would meet it.

***FIVE THINGS IT DOES THAT THE REMOVED VERSION COULD NOT***, and three are
corrections rather than features:

1. ***IT RETURNS THE TRACEBACK.*** The old surface returned an `int`, so a
   failing script gave the caller `-12004` and nothing else. `sys.stderr` is
   captured, so `PyErr_Print()` writes the real traceback into the buffer and
   it comes back as the payload — driven: `ValueError: deliberate` with its
   file and line, and a `SyntaxError` reported as one.
2. ***IT CAPTURES `print()`, AND THAT IS A CORRECTNESS REQUIREMENT OF THE
   SHAPE.*** **stdout IS the protocol channel**, so an unredirected `print()`
   would desynchronise every frame after it — and would look like a protocol
   bug anywhere except where it was caused. There is a row for exactly that:
   a `PING` immediately after a printing script must still answer `PONG`.
3. **One namespace, shared both ways.** SD's named objects and the scripts'
   globals are the same dict, so `STRSET greeting` then `print(greeting)`
   works, and what a script creates is readable by SD.
4. **A versioned handshake.** `HELLO` must come first and must agree, so a
   stale helper cannot quietly answer a newer SD.
5. **The flag is gone** — `@FALSE` at all six `SDEXT` call sites and never TRUE
   anywhere.

***THE PAYLOAD ENCODING IS LATIN-1, AND GETTING THAT WRONG WOULD HAVE BROKEN IT
ON THE FIRST DYNAMIC ARRAY.*** The first version used `PyUnicode_FromString`.
**An SD string is bytes**: `@fm`/`@vm`/`@sm` are `0xFE`/`0xFD`/`0xFC`, which are
not valid UTF-8, and a NUL would have truncated the value. Latin-1 maps
`0x00`-`0xFF` one for one, and the length is carried explicitly. ***The removed
code already knew this and its error names are the evidence*** —
`SD_PyErr_EnLatin`, `SD_PyErr_UniToStr`. **Driven**: a value carrying all three
marks, a NUL and a newline round-trips **byte for byte**, and `OBJLEN` counts
every one of them.

***WHAT IT DELIBERATELY DOES NOT DO IS THE PERMISSION GATE.*** §8 constraint 4:
the gate belongs where the helper is **started**, on SD's side, and faking one
here would be the decoration that constraint already names. The process refuses
to run on a terminal, and that is the whole of its own claim.

**Not in the free tier, deliberately**: `test-sdpy-units.ps1` needs a built
binary, and a test that passed because nothing was there to drive would be the
vacuous pass §0 forbids. It exits **2** when `sdpy.exe` is missing. Build then
test, the same standing as `probe-pylimited.c`.

**Next, in order**: the dict and list families and `RUNFILE`/`GETATTR`; then the
SD side — `sdpy.c` moves to `gplsrc` with a Makefile target, `SDEXT`/`SDPYOBJ`
become pipe calls, and the 20 `PY_*` come back. ***The first of those is what
turns this from a standalone binary into part of SD, and it is the point at
which a cycle starts being needed.***

#### The protocol, 12 Sep 2026 — ***AS PROPOSED BELOW, AND NOW BUILT TO IT***

**The surface was inventoried first, and it is measured.** All 20 `PY_*` at
`489b18e^` were read; the table below is what they call, not what the removed C
looked like. ***THE FINDING THAT SHAPES EVERYTHING: THE BASIC SURFACE IS ALREADY
A REMOTE CALL.*** It is two opcodes taking strings and returning one value —
which is a pipe message with the framing missing, so the protocol does not have
to be invented, only framed.

| | verbs | shape |
|---|---|---|
| `SDEXT(arg, flag, key)` | **6** — `PY_INITIALIZE`, `PY_FINALIZE`, `PY_IS_INITIALIZED`, `PY_RUNSTRING`, `PY_RUNFILE`, `PY_GETATTR` | one string, one flag |
| `SDPYOBJ(a1, a2, a3, key)` | **14** — the dict, list, str and obj families | three strings |

**Every argument is a string.** The only non-string is `SDEXT`'s flag, and
***it is `@FALSE` at all six call sites*** — so a field nobody has ever set to
TRUE would be carried into a new protocol out of politeness. **Say why it is
kept or drop it; do not copy it silently.**

***OBJECTS ARE NAMED, NOT HANDLED, AND THAT IS THE LOAD-BEARING FACT.***
`PY_CREATEDICT(dictname)` creates a dict *called* `dictname`; every later verb
names it again. There is no handle table and no id to leak. **The names are
per-session state**, which is an independent argument for the per-session helper
this section already rules — two sessions sharing one helper would share a
namespace and collide on a name the user chose.

**Three things a design would have to settle, and only the first is a decision
this project has not already made:**

1. ***FRAMING MUST BE LENGTH-PREFIXED, NOT LINE-BASED.*** The payloads are
   arbitrary SD strings — `PY_RUNSTRING` carries a whole Python program, and
   dict values carry `@fm`/`@vm` marks and can carry NUL. **A line protocol
   would corrupt exactly the values it is built to move, and silently.** This is
   cheap now and expensive after the first verb works.
2. **The response carries a status as well as a value**, because `process.status`
   is part of the existing contract — every one of the 20 documents
   *"status() - 0 on success, error code as defined in ERR.H"*. The error
   numbers already exist (`-12001` to `-12036`), so they travel rather than
   being re-invented.
3. **The value is an int for most verbs and a string for seven** —
   `PY_DICTGETKEYS`, `PY_DICTGETVALUES`, `PY_DICTVALGETS`, `PY_LISTGETS`,
   `PY_OBJTYPE`, `PY_STRGET`, `PY_GETATTR`. The BASIC side already knows which,
   so one payload field serves both.

**What would falsify it**: a verb needing to pass something that is not a
string — a file handle, a matrix, a select list. ***None of the 20 does***,
which is measured and is the reason a three-string frame is proposed at all.
`PY_RUNFILE` takes a **path**, not an open file, so `489b18e^`'s
`FILE*`-across-runtimes problem (`sdext_py.c:207`) does not exist in this shape.

*(Two instrument slips while measuring this, both corrected before anything was
written down. A `grep … | head -1` took its answer from each verb's
`START-DESCRIPTION` block and reported `PY_RUNSTRING` and `PY_RUNFILE` as having
their calls **commented out** — they do not; the comment is the documentation
above the code. And a truncating `grep -o 'PY_[A-Z]*'` invented a verb called
`PY_` and hid `PY_IS_INITIALIZED`. The inventory above is from
`git ls-tree` and from the files with comment lines excluded.)*

***ALSO RULED 11 Sep 2026, AND IT IS A SCOPE RULING RATHER THAN A TECHNICAL
ONE: THE UniVerse SHAPE IS DECLINED.*** Owner: *"drop the server idea — let's
just stay with the original."* **The scope of objective 2 is this section plus
§8, and nothing else.**

A tester running UniVerse on Windows observed that it ships Python **and** a
package set — FastAPI and Uvicorn among them — so an integration server can be
started from a TCL session, and asked whether SD should do the same. **It was
put to the owner the same day, with the split below, and declined.** Three
separable things were on the table and **only the first is in 1.1-0**:

1. Python present and callable from a session — *this is objective 2 already*.
2. A curated third-party package set installed with SD. **Not adopted.** It
   reverses the 10 Sep ruling (installed, not embedded), and `pydantic-core`,
   `httptools` and `uvloop` are compiled wheels pinned to one CPython ABI,
   which re-raises §8 constraint 5. *A middle option — `pip install` of a short
   pinned list during the optional Python step — was offered and is not adopted
   either.*
3. A long-lived HTTP listener started from TCL. **Declined.**

***THE REASON 3 WAS NOT A SMALL ADDITION IS WORTH KEEPING, BECAUSE IT WILL BE
ASKED AGAIN AND IT DOES NOT LOOK LIKE A SECURITY QUESTION.*** It is barely a
Python question at all:

- **Lifetime.** An SD session is request/response and dies with its connection;
  a listener must outlive it. That is a detached, service-shaped process, not
  the per-session helper this section rules.
- **Every existing gate is at connection time** — ssh at `sshd_config` then
  `LOGIN`, the API inside the SCRAM handshake (`APISRVR:1463`), §5.25's
  interactive-desktop rule. **A listener started inside a session is covered by
  none of them**, and it would be a second front door with its own rights.
- **API sessions run as LocalSystem**, so a process spawned from one inherits
  that unless it is deliberately dropped. §8 constraint 4 already records that
  Python's `os.system` never reaches `os_permitted()` (`op_sh.c:156`).
- **Ports are not generalised.** §5.26 measured it: `api-listener.ps1:55`
  matches only the literal `APIPORT=4243` and `api-firewall.ps1:58` defaults to
  4243 with neither caller passing `-Port`.

**None of that is an argument that it cannot be done** — it is the reason it
would need an access ruling before any code, which is what made it a separate
objective rather than an extension of this one. **Reasoning, not measurement.**

### 5.26 The API port stays 4243, on Windows and Linux (owner, 10 Sep 2026)

**Ruled.** Owner, 10 Sep 2026: *"I think we will just stay with 4243 on both
windows and Linux."* `APIPORT=4243` stays the shipped value
(`gplbld/stage.py:602`). Linux is a separate repository; nothing here changes
it.

**Upstream `sdb64` uses 4245**, and moved there so SD does not collide with
OpenQM on 4243 (`sdsys/changelog:5586`; `etc/xinetd.d/services:3`,
`sdclient 4245/tcp`). SD Core and upstream SD therefore differ on this port, and
a client written for upstream has to be given 4243. The comments calling 4243
"the number the Linux build uses" (`gplsrc/config.h:73`, `gplbld/stage.py:564`,
`gplbld/verify-apiport.ps1:35`, `gplbld/verify-scramlogin.ps1:43`) describe the
owner's Linux build, not upstream's.

**What the ruling accepts.** Where OpenQM already holds 4243, SD starts with no
API and says so only in its log — `API listener not started: cannot bind port
4243` (`gplsrc/sdwind.c:367`). The remedy, a different `APIPORT` in `sd.conf`,
is not supported end to end today, read from the code and not run:
`gplbld/api-listener.ps1:55-56` matches only the literal `APIPORT=4243`, so
`remote.api` refuses any other port (exit 2, message 10133); and
`gplbld/api-firewall.ps1:58` defaults to 4243 with neither caller passing
`-Port` (`gplbld/sd.iss:2545`, `gpl.bp/REMOTEAPI:285`), so the rule would name
the wrong port.

**How it was reached, 10 Sep 2026.** A switch to 4245 was ruled for the next
version and withdrawn the same day, before any commit, once the upgrade
consequence was put: `sd.conf` is written `onlyifdoesntexist`
(`gplbld/sd.iss:1708`), so after W1.0-0 ships an upgraded machine keeps
`APIPORT=4243`, and a switch means either rewriting it on upgrade — which stops
every W1.0-0 client connecting on 4243 — or making the tooling accept any port.
Also weighed: a port choice at install (about 2–3 sessions), listening on both
(a second shared-segment field, and the 4243 half still fails where OpenQM
runs), and `APIPORT` as a free setting with 4243 the default (about 1 session).
If revisited, `grep -rn 4243` re-surveys it; `test-retired-wording-units` is the
guard for a reworded port.

**Found in the same survey, independent of the port, not filed** (offered to the
owner for PRE_RELEASE_FIXES on 10 Sep 2026):
- `gplsrc/sdclilib/USER_GUIDE.md` examples connect on **4242** (lines 98, 126,
  164, 167, 521) — OpenQM's telnet port, not the API.
- `APIPORT` is `int16_t` (`gplsrc/config.h:74`, `gplsrc/sysseg.h:97`) with no
  range check (`gplsrc/config.c:305`), and the client's `OpenSocket` takes
  `int16_t` (`gplsrc/sdclilib/sdclilib.c:3994`) though `SDConnect` takes `int`.
  A hand-set port above 32767 gives no listener and no log line (negative, so
  `sdwind.c:350` reads it as unset) or a wrapped port, and the client silently
  connects to 4243. Read from the code, not run.

### 5.25 Administration requires an interactive desktop (owner, 5 Sep 2026)

***THE RULE.*** Administrative work happens **at the console, or through a
remote-control product or single-user remote desktop**. **Not from another
machine.** Owner, 5 Sep 2026: *"Remote admin through api or ssh is just a
security nightmare waiting to happen."*

***REFINED THE SAME DAY, AND THE REFINEMENT IS THE OPERATIVE RULE.*** The first
build read "not over ssh, and not over the API" literally and refused **local**
ssh too — `verify-sshadmin` ssh'd to localhost, was refused, and scored 10/0 on
it. That was the gate working *as specified*, and the specification was narrower
than the ruling. Owner, 5 Sep 2026: *"my lockout from remote API and SSH is
fine. However, local API and SSH should continue to work — if I am at the
console, everything works, only remote access is denied."*

> **Admit an administrator's session when it has a desktop (`K$INTERACTIVE`)
> OR its peer is provably this machine. Refuse otherwise.**

**REMOTE is what is denied, not a transport.** ssh and the API both keep working
for an administrator *on* the machine; both are refused *from* another one.
***THE RULE LIVES IN ONE PLACE AND IS CALLED FROM TWO — `gpl.bp/PEER_LOCAL`,
catalogued as `!peer_local`***, reading `ENV('SSH_CLIENT')` for ssh and
`system(42)` for the API. ***IT PROVES LOCAL RATHER THAN DISPROVING REMOTE***: a
session whose origin cannot be established stays refused, which is what keeps an
unattended scheduled task out. **"Local" means LOOPBACK** — `127.*`, `::1`,
`::ffff:127.0.0.1` — so a connection to this machine's own LAN address is
remote, which is what `b122` and `b126` both measured.

> ***THIS PARAGRAPH USED TO SAY "`LOGIN`'s `peer.local.test` is the decision …
> and `system(42)` for the API", AND THE API HALF OF THAT WAS FALSE.***
> PRE_RELEASE 170: `APISRVR` is the top-level program for an API connection
> (`K$CPROC.LEVEL 0`), so `CPROC` never runs, `CPROC`'s `call '$LOGIN'` never
> happens, and **LOGIN's peer test never saw an API session at all** — the
> `system(42)` branch was dead code written on the assumption that it did. The
> ssh half was witnessed while the API half had never run. The gate is now in
> `APISRVR`'s `vb.scram.final`, after the SCRAM proof and beside the `sdapi`
> test, and the shared routine is what stops the two doors drifting apart.
> Witnessed on `b126`, 15/0, with a PROGRAMMER admitted over the same remote
> address as the control.

***THE PRINCIPLE BEHIND IT, WHICH IS WHAT MAKES IT MECHANICAL.*** Administration
requires a session where **UAC can render** — a real interactive desktop. That
is what makes an elevation *consented to by a person* rather than merely
granted. ssh and the API have no desktop, so any elevation they obtain is
unconsented.

***IT WAS RULED ON A MEASUREMENT, NOT A PREFERENCE, AND THE MEASUREMENT
REVERSED WHAT THIS FILE BELIEVED.*** §5.6.1 and q14 said the risk was that an
administrator over ssh would get a **filtered** token and be unable to reach
SDSYS — *"nobody gets extra access, the failure is that an administrator gets
less"*. **The opposite is true.** On 5 Sep 2026 an administrator ssh'd in,
`WHO` answered `3 SDSYS`, `LIST ACCOUNTS` listed the register, and `sh` gave an
**elevated PowerShell** — `S-1-16-12288` High, `BUILTIN\Administrators`
**enabled rather than deny-only**, and `NT AUTHORITY\NETWORK` in the same
token. sshd runs as LocalSystem and builds the logon token itself, so
`LocalAccountTokenFilterPolicy` never applies to it. **PRE_RELEASE 167 carries
the full measurement and the roadmap.**

***WHAT IT SUPERSEDES.*** §5.6.2 said the console belongs to administrators and
ssh to everyone else, and treated that as enforced by Windows —
`sd-elevate.ps1:29-35` and `LOGIN:630` say so in as many words. **Windows was
not enforcing it.** This decision keeps §5.6.2's intent and moves the
enforcement into SD, where it can be tested.

***AND IT REINSTATES A MODEL THAT WAS WITHDRAWN ON A FALSE PREMISE.*** PRE_RELEASE
56's morning model of 29 Aug 2026 took ssh from administrators; clause 2 reversed
it the same day, and `LOGIN:60` records the reason — *"Administrators keep ssh,
which the morning's model had taken"*, on the grounds that the cost was one *"which
UAC decides rather than a test here"*. **UAC decides nothing here.** So this is
not overturning a considered decision; it makes true what `LOGIN` has claimed
since 29 August.

***THE PART SD CANNOT ENFORCE, AND IT BELONGS IN THE DOCUMENTATION.*** The
owner's *"remote desktop (single user), not RDP Server on Windows Server"* is an
SKU and deployment choice. A token distinguishes an interactive logon from a
network one; it does not distinguish how many people may hold one. **And a
remote-control product only qualifies if it is installed as a SERVICE** — a
per-user install cannot render the secure desktop and the operator sees a frozen
screen (`sd-elevate.ps1:33-35`).

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

- ***AT (5) OF THE REAL-UPGRADE SEQUENCE THE COMMAND IS THE INSTALLER, NEVER
  `cycle.ps1`.*** 17 Sep 2026, RELEASE_1.1 40. A cycle uninstalls and deletes
  both trees, so run in place of `sd-setup-W1.1-0.exe` it destroys the W1.0-0
  tree that (2)–(4) built and snapshotted — one attempt lost. The hand-over had
  put (5)'s command below a numbered list of captions, and it read as missing.
  **In a hand-over, each step's command goes directly under its heading, and a
  step with a destructive look-alike says what not to run.**

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
  `assert-current`'s exemption (a name `stage.py` or `sd.iss` quotes is watched
  again), so the next edit to it makes the tree report STALE - and
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
  2026, and it cost a cycle. A verify script is exempt in `assert-current` (the
  harness name family) and cannot make an install stale; a shipped file under
  `sdsys` can. Correcting a verifier and a message file in one go therefore
  voids the install being measured, for the sake of the half that did not need
  to.

  **THE EXAMPLE THIS ENTRY WAS WRITTEN AROUND IS DEAD, THE RULE IS NOT.** It
  said `sdsys/changelog`, which was the commonest case; the changelog has been
  exempt since 21 Aug 2026 (header item 1), so it no longer voids anything.
  Every other shipped file under `sdsys` still does.

- **`cycle.ps1` DOES NOT RUN `make`. A C CHANGE CAN BE CYCLED, INSTALLED, TESTED
  AND PASSED WITHOUT EVER BEING COMPILED.** 18 Aug 2026, and it cost a whole
  cycle. `cycle.ps1` stages whatever is already in `bin\`; the build is a
  separate `make sd` in an MSYS2 login shell. `to_file.c` was edited at 19:15
  and cycled at 19:38 against `bin/sd.exe` from **17:17**.

  ***THIS HEADING USED TO READ "`cycle.ps1` DOES NOT BUILD" AND THAT IS FALSE
  AS WRITTEN — CORRECTED BY THE OWNER, 3 Sep 2026.*** **It does build**: step 2
  is `stage.py --bootstrap`, and the bootstrap compiles `gpl.bp.out` from
  SECOND.COMPILE, `gcat` and `pcode.out` — which is *most* changes on this
  project, and is why CLAUDE.md calls `-SkipInstall` the cheap way to find out
  whether a BASIC change compiles. **The pages of `0 error(s)` in a cycle log
  are that build.** The bullet below was always right about what it measured;
  only its first four words over-claimed, and they had been copied into a
  handoff by 3 Sep. **The C half is the whole of the gap, and `stage.py` checks
  the binaries are PRESENT, not CURRENT** (`stage.py:991`), so a stale `bin\`
  stages and installs without a word.

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

## 8. Open questions

**Only open questions stay.** Two nobody has diagnosed. The rest of this section —
the Python plan (built and witnessed; §5.27 has the decision), the settled items
and the closed questions — is in HISTORY.md, *"ARCHIVE 21 Sep 2026 —
PROJECT_STATUS.md before consolidation"*.

---

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
