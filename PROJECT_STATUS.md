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
OPEN TASKS wins and this block is the stale one.

***22 Sep 2026 — Bundle A CLOSED: 71, 69, 73, 76's remaining witnesses, `verify-routes`' seat conversion.***
Detail: HISTORY.md, 22 Sep 2026 (search `RELEASE_1.1 71`, `69`, `73`, `76`, `verify-routes`). `-Run`
tokens spent through `b228`; next is `b229`.

***22 Sep 2026, overnight — §5/§6 TRIMMED*** to the owner's instruction, with retained entries
shortened to their essential issues as well. PROJECT_STATUS.md: **329,082 → 142,944 bytes**
(`wc -c`, 57% smaller). Full pre-trim text is `git show 375c611:PROJECT_STATUS.md`. HISTORY.md
carries one entry naming what moved. §0's 350,000-byte cap and its maintenance rules are
otherwise unchanged; no decision, rule, open task or distinct §6 trap lesson was dropped —
only the narrated measurement trails, superseded corrections-of-corrections, and repeated
restatement around them.

**Next, in order:** 76's falsification check (`verify-apiadmin`/`verify-privundetermined`, elevated,
SDSYS signed in, *without* the planted `os.users\SDSYS` fixture); 97's suite-speedup proposals; the
47 → 48 → 49 gates (parity audit → docs → staging/zips), none started.

***Open, not filed:*** `voc_template` has no `~` record; SDSYS's VOC never gets one. Ask before building.

***Tooling:*** `agent-elevate.ps1 -Start` = one UAC click, then
`-Run -Script <name>.ps1 -ScriptArgs '-Run','bNNN','-Only','<step>'` (comma-list args as an array, not a
joined string). `bbcmp` compiles `set_acc_password`/`createa`, not `login`. `ISCC` needs a staged tree.
`cycle.ps1`'s "handle on it" message is a guess — check ownership (`takeown`) before assuming a lock.

> §5.29: *"we are responsible for the transport and the default unmodified system, after that it is the
> wild west."* Read before filing a security finding — an admin's own grant is not our defect.

---

## OPEN TASKS — RELEASE 1.1 (W1.1-0)

**5 open (ids across 3 entries): validated against the tree by the 27th pass,
21 Sep 2026, plus 97; 59, 69, 71, 73, 75, 77, 84, 100–104, 64, 95, 96 and 99 all closed 22 Sep, and 61 folded into gate 48; 53 is deferred to W1.2 (its own section, below the gates).** Every call
that was the owner's has been ruled — he delegated them, 21 Sep 2026 — and each ruling
is in its entry. `B` blocks
the release, `S` should be fixed, `M` is minor. Each entry says what is open and
what is owed; **the row it came from, with every earlier status layered under it,
is in HISTORY.md under *"ARCHIVE 21 Sep 2026 — RELEASE_1.1_FIXES.md as it stood"*
— grep `| 64 |`** for the full text of an id. Release 1.1's two objectives
(owner, 11 Sep 2026) were the defects SD Core for Linux found in this tree and
embedded Python installed rather than shipped; the Python route is built and
witnessed (`verify-pyapi`, `verify-pygate`, §5.27).

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
add a row there whenever a line a verifier matches on is reworded. `verify-lcnames` AND
`sdtestuser-admin` **WITNESSED 22 Sep 2026**, unelevated (`-Run b224` for the account pair):
`verify-lcnames` 165/165; `sdtestuser-admin` Create/Remove both instrumented before/after,
driving `verify-nocase` (5/5) and `verify-lineendings` (17/17). ***THE FULL SUITE RAN 22 Sep 2026,
`-Run b223`, elevated: 31 of 35 clean.*** Two were stale verifiers (`verify-elevdoor`,
`verify-sdsysgate` — both asserted `RELEASE_1.1 45`'s withdrawn model; fixed and re-witnessed
clean, `-Run b225`). Two could not run on `b223`: `verify-routes` demanded the genuine SDSYS
Windows session (predated the seat); `verify-print` could not set its throwaway default printer
in the helper's non-interactive session (cleaned up correctly, untested interactively).
***`verify-routes.ps1` CONVERTED TO THE SDSYS SEAT AND RE-WITNESSED SAME DAY, `-Run b226`:
35 of 35, no account switch*** — see HISTORY.md, 22 Sep 2026. **Still owed:** the falsification
check below (a local control run *without* the planted record was not done).

Owner's ruling, 21 Sep 2026. **All four were converted in source:**
`sdtestuser-admin.ps1` and `verify-lcnames.ps1` earlier that day, and
`verify-apiadmin.ps1` and `verify-privundetermined.ps1` unattended overnight.
`test-logtoreaim-units.ps1` now reports **0 files still sending the refused prefix**
and `test-sdsysseat-units` passes; both verifiers parse with the function counts they had
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

***22 Sep 2026 — BOTH VERIFIERS NOW TAKE `-NoFixture`***, so the check no longer needs a
manual edit: it skips planting `os.users\SDSYS` for the local control and reports the
result under a differently-named check (`falsification: ...`), not a flipped expected
value on the existing one. Not yet run — needs the same elevated-agent-helper + SDSYS-
signed-in setup as the witnessed runs, and reaches SDSYS through the seat's own scheduled
task (`sdsys-seat.ps1`), so the operator does not switch sessions to run it.

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
lines) — the tri-state's logging *"has never been executed by anything"*, and this step
makes it non-zero on purpose three times, the only thing proving the path fires. Its
unit guard `test-privundetermined-units` goes with it if it is ever retired.
`verify-lcnames` (1,093 lines) — already converted in source; the lower-case standard
is stable and this is its widest net, and the churn was the 5.12 conversion rather
than steady-state; one witness run is owed (now done, see 76). `verify-apiidentity` —
the only witness of 55's session-as-the-user property; 84's rewrite onto the real
`sdclilib` and its SDSYS-seat conversion are DONE AND WITNESSED (22 Sep, `sdapiidb222`),
and `scram-probe.py` stays. **What would reverse these:** a verifier failing for an
*instrument* reason more than twice. **Examined and kept — do not retire on a second
pass:** `probe-akwrite` (only witness of the alternate-key write path), `verify-nonet`
(5 s), the eight case verifiers (each a distinct mechanism, 5–7 s), `verify-notyet`,
`verify-cmdaudit`, `verify-elevdoor`. 32 of 65 steps have never failed in 8–31 runs, but
a clean record is what a regression guard looks like; the run summaries do not say
whether a failure was the product or the instrument.

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
  on more than a dozen pages, which 64 made false. **Absorbs 61** (owner, 22 Sep,
  moved here): at `Administrator/markdown/01-accounts-and-security.md:85`, `:88`,
  `:165`; `03-operating-system-access.md:189`; `05a-managing-accounts.md:101`,
  `:153`, *"Administrators have API access and `OS.EXECUTE` access automatically"*
  is false since 58 removed it; and add the two facts — **only SDSYS administers**,
  and an **ssh session's reach is bounded by NTFS, not by SD**. `SDCoreWindowsDocs`
  was clean at `de44f8e`, matching its remote (22 Sep). 61's in-repo half is
  already DONE (§5.25's correction box, §5.28's API-token and ssh rows); only the
  shipped docs, in the other repository, remain — check every factual claim before
  it ships (§5.29 and the "not isolated" line that was false). **Add a
  security-posture section** (owner, 22 Sep): describe how the system is **secured
  at delivery** — SD accounts tied to standard Windows accounts (no privileged
  token), ssh users `ForceCommand`'d into SD with no `sh`/`OS.EXECUTE`, `os.users`
  empty, `APIPORT` off until asked, `sdsshonly` denying the console, `BASIC`/`RUN`
  removable and app-lock-at-login with the break key disabled available — **and
  that the administrator can choose to open it up** (grant `os-on`, `sdapi`,
  `sdssh`, leave `BASIC`/`RUN`) **based on their environment, which is their choice
  and responsibility** (§5.29). **Absorbs old 18:**
  rebuild the sets with `tools\release.ps1` and copy the corrected bound PDFs from
  `<Set>\book\` into the release's `documentation\` before zipping, so the 29
  `-ExecutionPolicy Bypass` fixes in `SDCoreWindowsDocs 76e1dce` reach the shipped
  PDFs (assembly is a hand step with no script). Linux starts its documentation
  from the finished Windows docs, so name the shape early.
- **49 — the W1.1 staging directories and zips**, one Windows and one Linux.
  **Settle first, and before 48 documents an install procedure:** is a release
  zip a source snapshot (the installer would have to clone a *tag*) or an artefact
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
broker — so it goes with it to W1.2 (59 itself is now closed by ruling, §5.29, and its
hardening is no longer a 1.1 item). **Until the deciding experiment is run, no document
may say a local user *cannot influence* the service through this section** — the claim
is unmeasured, and saying less is the honest wording for 1.1.

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

***THIS FILE IS CAPPED AT 350,000 BYTES (`wc -c`), NO EXCEPTIONS.*** Owner,
22 Sep 2026, after a session spent more of itself narrating findings — long
prose entries, quoted transcripts, restated context — than doing the work:
*"we are spending more time documenting and verifying than moving the project
forward."* A line-count cap rewards cramming long lines instead, so this one
is bytes. **If a commit would push the file over the cap, cut or move content
to HISTORY.md in the SAME commit** — "next session will clean it up" is not a
plan. Check before committing: `wc -c PROJECT_STATUS.md`. A CURRENT PICKUP
entry states the outcome and points at HISTORY.md for detail; it does not
carry the detail itself. An OPEN TASKS entry is what is owed, not a log of
every step taken to find out.

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
> 2 OR MORE IS REAL DAMAGE.*** Do not paste the sequence into any new prose in
> either file — naming the bytes keeps the expected value at 1.
>
> **This file expects 0** (its own copy moved to HISTORY.md on 5 Sep 2026, along
> with the count); **HISTORY.md expects 1**, and since 21 Sep 2026 also holds the
> archived `PRE_RELEASE_FIXES.md`, still measured exactly 1 after that move. The
> underlying rule is `CLAUDE.md`'s — a tracked file is edited with `Edit`/`Write`
> and never by a program.

> ***READING THESE FILES IS NOT THE SAME AS SEARCHING THEM, AND THE PROJECT RULE
> IS TO SEARCH.*** Owner's instruction, 23 Aug 2026: **grep PROJECT_STATUS.md
> and HISTORY.md for the verb, script or flag in any command before running it.**
> `CLAUDE.md` §"Search the record before you run anything" is the rule; it is
> there rather than here because it is loaded every session and this section is
> not. Three or four consecutive sessions lost time to a warning that was
> already on disk — most recently `echo WHO | sd` on 23 Aug 2026 (§6), which made
> an unusable session.

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
4. **§6 traps: anything that cost real time. Never cut a trap for size — tighten
   the prose, do not drop the lesson.** What happens, what to do. This section
   is meant to grow.
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
   they are not on it, and `assert-current` exempts them precisely because they
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
**11 of the 24 already need nothing but the installed tree** — but each still
calls `assert-current`, so that call would need to be made conditional before
any of them could ship. **Not started, recorded so the next session does not
rediscover the blocker.**

### 4.0.1 An agent shell can elevate ONLY DIRECTLY — the suite's own elevations are refused

***MEASURED, and this is the current reading:*** a `Start-Process -Verb RunAs`
issued **directly** by the agent's own shell works; the same call made **by a
script the agent launched** (nested) is refused — *"The operation was canceled
by the user"*, **with no dialog ever shown to the owner** — because UAC renders
on the secure desktop and a nested elevation has no desktop to render on
(§4.0.1). The whole suite launched as a background task hangs forever the same
way, silently. **So: the verify suite is run by a person, from their own
ordinary terminal.** An agent may run `cycle.ps1` and one-off elevated commands
directly; it may not run `VerifyInstall1`, and must not spend a `-Run` token
re-discovering this. **12 Sep 2026, once, on this machine:** even a direct
`Start-Process -Verb RunAs` was refused the same way; not repeated, and it is
unknown whether a dialog rendered and was declined or never rendered — ask the
owner rather than re-testing. **Nothing is left behind by a refusal this way**
(checked both times: no stray account, group, `os.users` record, or process) —
**the token is not spent and can be reused.**

***21 Sep 2026 — THERE IS NOW A ROUTE AROUND "ONLY DIRECTLY", AND IT COSTS ONE CLICK PER
SESSION.*** `.claude/tools/agent-elevate.ps1 -Start`, run by the owner from an ordinary
prompt, launches a resident elevated helper (one UAC click). After that the agent runs
`agent-elevate.ps1 -Run -Script <repo>\sdb_ai\sd64\gplbld\<name>.ps1 -ScriptArgs <words>` and
gets the script's real exit code plus its captured output (in
`%LOCALAPPDATA%\SD-verify\agent-elevate\`, printed by the client). ***CALL THE CLIENT
DIRECTLY FROM A POWERSHELL SESSION, WITH `-ScriptArgs '-Run','b210','-Only','x'` AS A REAL ARRAY***
— through `powershell -File`, or from bash, a comma list arrives as one string and the
runner refuses *"-Run was not given"* without running anything. `-Stop` ends it and it
stops itself after 60 idle minutes. **Limits:** only a `.ps1` directly in `gplbld`, with
plain arguments; a run is killed at 30 minutes (exit 124); **it cannot run `cycle.ps1`**
— the installer's finish page asks for passwords in a hidden, non-interactive process
that cannot answer — **and it does not lift the rule above**: the full suite's parent
must stay unelevated and nested elevation is still refused. **The intended use, not yet
tried:** an elevated verifier step, `VerifyInstall2.ps1 -Run bNNN -Only <step>`.
**The allow-list stops accidents, not an agent that writes a script into `gplbld`.** Free
guard: `test-agentelevate-units.ps1`.

---

## 5. Decisions and why

Do not undo these without reading the reasoning.

### 5.29 SECURE THE TRANSPORT; WHAT THE ADMINISTRATOR DOES AFTER THAT IS THEIRS (owner, 22 Sep 2026)

> ***"We are responsible for the transport and the default unmodified system, after that it is the wild
> west."*** — the owner's own one-line form, 22 Sep 2026. **If you read nothing else in this section, read
> that. It is the whole triage rule, and the two halves are the test: is this the TRANSPORT, or is this the
> DEFAULT UNMODIFIED SYSTEM? If neither, it is not ours.**

**The longer form, why:** *"Pick systems have always had the attitude that security was possible, but it
was up to the admin to enforce it... My desire is to only make the transport tunnel secure. What the admin
decides after the user arrives is his responsibility. By default we turn a lot of things off, leaving the
default system locked out of the OS. If the admin changes that, then that is their concern."*

**In scope:** the tunnel (TLS and SCRAM, 41/42), the `sdapi`/`sdssh` grants, sshd's `AllowGroups`,
`ForceCommand` and `DisableForwarding`, the API's containment gate, `$cred`'s ACL, and the shipped
DEFAULTS being closed (`os.users` empty, `APIPORT` off until asked, `sdsshonly` denying the console).
**Out of scope:** hardening a site against its own administrator's later choices. An administrator who
grants `os-on`, `sdapi` or `sdssh` has decided.

**It settles a class of argument, not one case.** *"An account at TCL with `BASIC` and `RUN` can write
any path NTFS allows on an ssh session"* is TRUE and is **not a defect** under this ruling — the
administrator can remove `BASIC`/`RUN` or lock the account into an app with the break key removed.
**Do not file, or re-file, a finding whose whole content is "a user left at TCL can do X."**

**The line to triage on: a default we ship is ours; a grant an administrator makes is theirs.** **104**
was ours — two `sdsys` directories kept `sdusers:Modify` while their six siblings were locked, an
inconsistency in our own default — fixed and closed. **59 is the administrator's** (ruled 22 Sep,
reversing last session's carve-out): every SD account is tied to a standard Windows account so its
token cannot escalate, an ssh user is `ForceCommand`'d with no `sh`/`OS.EXECUTE`, `BASIC`/`RUN` can be
removed, and the account can be app-locked at login. Reaching the shm-segment path (§5.28 row 1) takes
several deliberate admin steps — the same class as "a user left at TCL can do X." The reader-hardening
remedy remains a legitimate W1.2 improvement but is not a 1.1 blocker.

### 5.28 The security model after RELEASE_1.1 64, evaluated (21 Sep 2026)

64's decision made this part of itself: *"Once everything is removed, we will evaluate
the resulting security model."* **What survives 64 and must not be swept up:** 60 (bounded
copies in `clopts.c`), the TLS/SCRAM tunnel (41, 42), 55's session-as-the-user handover
and its SID-ACL'd pipe, and the `secure-*.ps1` ACL hardening. **Method: read from source
(`op_sh.c`, `login`, `cproc`, `createa`), joined to measurements already in the record
(55, 59, 53, 60). Nothing was run; every runtime claim is marked as reasoned.**

| principal | what it holds | enforced by |
|---|---|---|
| SDSYS, the Windows account of that name, elevated | the **only** SD administrator: the session flag is granted at login after `elevate('START')` | LOGIN; `LOGTO SDSYS` refused outright (10002); `sd -internal` forced to SDSYS and needs LOGIN's one-shot marker (82) |
| any other Windows administrator | an ordinary SD account like everybody else; refused SDSYS | LOGIN |
| every ordinary SD account, USER and GROUP | the whole of `newvoc` (former PROGRAMMER level; no tiers); ssh and the API **by default** (`createa:611-615`) | `createa`; `sdssh`/`sdapi` Windows groups |
| OS.EXECUTE, `SH` and Python, for that account | **default deny**: `os_user_permitted` allows only an internal program, the administrator flag, or `os.users\<login>` field 2 = `yes`; ships empty | `op_sh.c`; the Python gate calls the same function (23) |
| an API session | TLS + SCRAM; runs **as** the authenticated user (55); confined to its account root, nine read-only SDSYS entries and `NETDIRS`; **never holds the SD administrator flag**; its Windows token is whatever LSA returns for that account, unfiltered | `apisrvr`; the containment gate in `op_dio2.c`; `kernel.c:296` |
| an **ssh** session | **NOT path-confined**: `net_path_permitted()` is TRUE for every path once the session is `CN_CONSOLE`, which ssh is — the containment on this transport is the ACL, not SD (59, 104) | sshd's `AllowGroups`/`ForceCommand`/`DisableForwarding`; NTFS |
| the data tree | `$cred` readable only by SYSTEM and Administrators; the rest per the `secure-*.ps1` scripts | Windows ACLs |

**Findings, worst first:**

1. **59 (CLOSED by ruling, 22 Sep — §5.29)** — the LocalSystem daemon `sdwind` reads a
   segment every SD user can write; the owner ruled it the administrator's side of the line.
2. **53 (deferred to W1.2)** — an ordinary local user can open the daemon's MSYS2 shared
   section for write; whether that can influence the service is **unmeasured**, so no
   document may claim it cannot.
3. **The decision text and the build disagree about OS-level access, and the build is the
   safer one.** 64's text says *"the only limit... is imposed by Windows"*; what is built
   is default-deny per account. **Ruled 21 Sep 2026: default-deny stays** — 59 and 53 are
   why a remote interpreter is worth more to an attacker than it looks, and an admin can
   still grant it per account. Docs must say *no OS access until an administrator grants
   it*, not *Windows' limits*. **The grant is the administrator's decision, not SD's**
   (owner, 22 Sep: *"if the admin chooses to give a user api access and os.execute access
   that should be respected as their choice"*, same for ssh) — a transport test that
   refuses `OS.EXECUTE` on `CN_SOCKET` even when `os.users` says yes is **REFUSED, not
   deferred.** What is owed instead is **disclosure** (gate 48).
4. **Every account has the remote doors by default but no credential until an elevated
   interactive sign-in (69).** Fails closed; the message now says so.
5. **A Windows administrator can grant themselves anything by hand.** Out of scope by the
   owner's 21 Aug ruling (*"if users want to degrade security after the fact, that is their
   right"*); 95's fix keeps the installer from doing it for them.
6. **What 64 removed is what it gained:** no tier boundary, no administrator-as-themselves
   bypass, no promotion/demotion, no second administrator identity.

**Carried forward, not re-measured:** an application's own `OS.EXECUTE`/`EXECUTE` built
from user input is an escape (less reachable now); a machine where SD did not install the
ssh server never writes `ForceCommand`, so a user reaches `cmd.exe` directly.
**Not examined, worth doing in 47/48:** the phantom/background-process path, `ForceCommand`
on a real second machine. **What would change these rulings:** the 53 experiment showing
influence is possible; a bypass of the `os.users` default-deny by an unprivileged account.

### 5.1 POSIX IPC replaces System V

System V IPC compiles and links on MSYS2 then fails at runtime with ENOSYS
(§6); native Windows has none at all. POSIX named shared memory and semaphores
work on both and are the right direction for stage 2, since POSIX shared
memory is backed by `CreateFileMapping`. `sysseg.c`, `sdidx.c` and `sdwind.c`
use `shm_open`/`ftruncate`/`mmap`/`munmap`; `sdsem.c` uses
`sem_open`/`sem_trywait`/`sem_post`; names come from `SD_POSIX_SHM_NAME` and
`SD_POSIX_SEM_FMT` in `sddefs.h`. Two spots needed more than substitution —
`munmap` must be told the mapping length that `shmdt` derived from the
address, recorded at attach; `stop_sd()` polls the user table with
`kill(pid, 0)` since POSIX exposes no System V attach count. Full reasoning:
HISTORY, "First native Windows build".

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

Owner, 15 Aug 2026. `gplsrc/sdclilib/` did not come from the usual three
generations (§2): `sdb64`'s own C developer started a partial Windows API
library, an AI completed it into `github.com/dmontaine/winsdclilib`, it was
vendored here 13 Aug 2026 (`b6624565`), and their developer then forked it
back — changes from it are now in `sdb64`'s `dev` branch. **As of 19 Aug 2026
this directory is no longer a vendored copy — it is the source of truth**, and
`winsdclilib` is its mirror. So "upstream" is ambiguous here, the reverse of
every other file in the port. **Do not "align with upstream" reflexively** —
a session did exactly that with `SV_EMSG_PAIR`/`SV_ECONTXT` and had to revert
(UPSTREAM_FIXES.md #2, closed: `sdb64` was right). And since an AI completed
step 2, this directory carries §2's generation-2 risk despite having no
`Composer AI` markers to flag it.

### 5.4 The BASIC layer's platform switch, and why it is not to be revived (owner, 21 Aug 2026)

**OWNER'S RULING: NO WINDOWS BRANCHES IN THIS VERSION OF SD, BECAUSE IT IS
WINDOWS ONLY.** Same rule CLAUDE.md states for the C code — take the Windows
arm, drop the conditional, delete the Linux arm.

Two SYSTEM keys bridge the BASIC and C sides: `SYSTEM(91)` ("is this
Windows") answers `1` (`op_sys.c:282`, flipped 17 Aug 2026 to fix
case-insensitive directory-file matching in `QPROC:508` — its only reader,
which is also why flipping it early was safe); `SYSTEM(1006)` ("is this NT
style") is hard-wired 0, `is_nt` never assigned, and no BASIC file reads it —
open, set it or remove the key. This repository's BASIC has had its Windows
branches removed (`LOGIN`, `CONFIG`, `CPROC`, `CREATEA`, `PARSER`); the
external tree at `C:\Users\dmont\Projects\GPL.BP` still has them, keyed on a
bare `windows = system(91)`, not `is.windows`.

### 5.5 The Linux privilege model does not survive the move

Background for §5.6. `IsAdmin()` was `getuid() == 0` and `SYSTEM(27)` returns
`getuid()`, which is 197609 under MSYS2 — never zero, so every privilege test
answered the same way permanently and the symptom was a refusal from code
that looks correct (§6). `EUID_SET`/`EUID_RESTORE` were the mechanism the root
branch used, reaching `sdext_eguid.c` through `SDEXT`; Windows has no
equivalent short of `LogonUser` plus `ImpersonateLoggedOnUser`, which is the
shape §5.7's service model needs. Full site-by-site table: HISTORY, "Surveyed
every BASIC to C linkage".

### 5.6 Identity model: accounts with passwords (13 Aug 2026), and administration is the OS's (14 Aug 2026)

**REVERSED 14 AUG 2026. Mimic the Linux version:** SD login takes no password;
the OS has already authenticated you, and SD asks it who you are (verified
against a Debian VM and this repository's own pre-port `LOGIN` at `f9edab0`).

The model, in five rules:

| | |
|---|---|
| `sd`, no account named | you land in **the SD account with your own name** |
| no SD account of that name | refused — `sysmsg(5018)` |
| not in `sdusers` | refused at the door — `sysmsg(5009)` |
| **`sudo sd`, or any elevated session** | **your own account, like everybody else.** `LOGTO SDSYS` afterwards |
| `sd -Aname` | **refused unless `name` is your own account** — `sysmsg(10051)`. `-INTERNAL` is exempt and forces SDSYS, needing elevation — `sysmsg(10002)` |
| **an elevated session, in `LOGTO`** | **passes without the group check** — `ACCOUNTS/SDSYS` names a group Windows does not have, so the check would refuse administration to everybody (§6). Linux root does not pass it either |

**What makes it work on Windows:** `ACC$GROUP` is written as `sdu_<name>` on
every account (`CREATEA 455`), the group is created by `CREATE.ACCOUNT` and
`sdusers` joined at `CREATEA 345`, `!is_grp_member` works, and the sudoers
list is `Administrators`.

**The credential machinery is NOT deleted** (owner, 14 Aug 2026). `$CRED`,
`!CRED_SET`, `!CRED_VERIFY` and `SET.PASSWORD` all stay: the API is a
separate door and does require an account password.

**The security position rests on OS group membership, not a secret checked
at login** — not a weakening: every SD process opens the database under the
invoking user's own token (§5.7), so account passwords organise access, they
do not secure it. `Administrators` is machine-wide, so anyone in it for an
unrelated reason gets SDSYS — parity with Linux sudoers, but a decision to
hold deliberately.

**The superseded 13 Aug 2026 decision, in three lines:** SD had no concept of
users, only accounts, each with its own password (reversed for login,
retained for the API); SDSYS was the only administrator (reversed — an
*elevated* Windows administrator); OS groups were dropped from SD's logic
entirely (reversed — they are now the whole model). Full reasoning: HISTORY,
"Moved from PROJECT_STATUS §5.6".

### 5.6.1 A Windows administrator is an SD administrator (decided 14 Aug 2026)

**Decision, 14 Aug 2026**, reversing "SDSYS is the only administrator": if you
can log in as a Windows administrator, you are an SD administrator; the
installer runs elevated, so the installing user is one without any further
step.

**What "administrator" tests, and it is not elevation.** `getgroups()` (the
process token) does **not** carry `Administrators` when UAC-filtered (deny
only) and Cygwin drops it; `getgrouplist()` (the account's SAM groups) does.
`IsAdmin()` uses `getgrouplist()` now. **Both answers are wanted, for
different questions:** `IsAdmin()`/`getgrouplist()` still gates `sd -start`
(should not demand elevation of somebody already an administrator);
`K$ADMINISTRATOR`, which decides who reaches SDSYS, needs the **elevated**
answer — hence a separate `IsElevated()`.

**Test gid 544, never the name** — `Administrators` is renamed on a localised
Windows, `*S-1-5-32-544` is portable. `gplbld/sd.iss` and `CREATEA` both use
the SID form.

**Consequences:** actions needing an elevated token still fail unelevated
(creating a Windows account among them) — an SD administrator can *administer
SD*, not do every administrative thing (§5.7 is the service-model answer).
`sdusers` is unaffected — an ACL question, not authorisation; an elevated
administrator reaches the tree via `Administrators` without it, everyone else
needs the group and a sign-out/in after being added (§6). Normal accounts are
standard local accounts; administrators are made deliberately, with a keyword.

**SD creates and deletes OS accounts** (reversing "create none"), through
`*-LocalUser`/`*-LocalGroup`: `!create_user`, `!delete_user`, `!set_passwd`,
`!os_group`, `!ps_script`, `!is_grp_member` — all in `GPL.BP`. **Elevation is
not optional** for any of it, so it works from the installer and an elevated
terminal, not from a normal session; each helper tests for elevation
explicitly rather than guessing from an error message. **`OS.EXECUTE` needed
a shell an installed system does not have** — resolved by making `SH`/`SH1`
PowerShell (§6). **`sudo` on Windows is a convenience, elevation is the
prerequisite** — the control is the `Administrators` group, not a sudoers
file; a normal account attempting elevation is prompted for *somebody else's*
administrator credentials and cannot elevate as themselves. `sudo.exe` itself
is not installed or enabled by the installer (Windows 11 24H2+ only, would
exclude Windows 10/Server) — "Run as administrator" gives the identical
elevated token on every version. **One real risk, fails closed:**
`LocalAccountTokenFilterPolicy` unset means a local account logging on **over
the network** gets a filtered token, so a remote administrator over ssh may be
unable to elevate at all — nobody gets extra access, an administrator gets
less. (Superseded by §5.25's measurement that this is not actually what
happens for ssh — see there.)

**Passwords never go on a command line** (owner, 14 Aug 2026) — `!ps_script`
writes the script to a file inside the SDSYS directory, runs it, deletes it.

**Access:** SDSYS reaches every account without exception, tested on the
account you are **standing in** (`who`), not the one logged in as — stepping
*out* of SDSYS loses the exception. `LOGTO` takes an account name only, never
a pathname — closed by removing the capability rather than resolving paths
back to accounts. **The API server's `login(username, password)` check
cannot succeed on Windows** (reads `/etc/shadow`, which MSYS2 lacks) — the API
is closed rather than open until §7 step 6/§8 build a real mechanism.

**How the administrator flag is held.** `LOGIN` sets `USR_ADMIN` on entry to
SDSYS and clears it entering anything else; `CPROC` does the same on every
`LOGTO`. Only an `$internal` program may set the flag and only SDSYS may
compile one. `kernel.c` seeds the flag from `IsAdmin()` at process start.

**`LOGTO SDSYS` asks for no password at all** — `LOGTO.STEP.UP` was deleted
14 Aug 2026 (`CPROC:3798`); `CPROC:2568` calls `elevate('START','')`: 0 when
already elevated, a UAC prompt otherwise, `sysmsg(10002)` on refusal.

**Audit — BUILT AND VERIFIED 16 Aug 2026** (§7 step 4). Login, refused login,
`LOGTO`, refused `LOGTO` and `GRANT`/`REVOKE` all write to `<sysdir>/audit`,
identity stamped from `my_uptr`. **Not `errlog`** — `log_message()` discards
the oldest half at the configured size, correct for diagnostics, wrong for an
audit trail. **What is still missing:** no verb for managing grants (`GRANT`/
`REVOKE`, §7 step 5); `ACC$GROUP` is dead but still populated and shown by
`LIST ACCOUNTS`; the tier-filter comparisons in `LOGIN`/`CREATEA` and the
`is_grp_member` calls guarding Linux account shell-outs in `CREATEA`/`MODIFYA`
go with the eventual removal of the Linux account commands.

**Understand the security consequence before relying on any of this.** A
password gate inside SD is not a file security boundary — see §5.7.

### 5.6.2 SD accounts are ssh-only; the console belongs to administrators (decided 14 Aug 2026)

**VERIFIED 14 Aug 2026 at both ends except RDP** (`gplbld/verify-sshonly.ps1`,
and the `CREATE.ACCOUNT` branch that drives it). RDP is the only part
nobody has watched.

***SUPERSEDED IN ITS ssh CLAUSES, 2 Sep 2026 (PRE_RELEASE 124).*** The API is
an **independent port-4243 listener**, not an ssh tunnel — SD accounts do
**not** reach the machine over ssh and nothing else. ***SUPERSEDED AGAIN ON
THE ADMINISTRATOR SIDE, 5 Sep 2026 — READ §5.25.*** An administrator is now
refused any session that did not start on this machine, over ssh and the API
alike; what was "should" is now enforced.

**Decision (original, 14 Aug 2026):** accounts SD creates reach the machine
over ssh only; console and RDP are for administrators (ordinary Windows
accounts). This sits on top of §5.6.1: `CREATE.ACCOUNT USER x ADMINISTRATOR`
creates an unrestricted Windows account (console + RDP + SD admin); without
the keyword, confined to ssh.

**Mechanism: `SeDenyInteractiveLogonRight` and `SeDenyRemoteInteractiveLogonRight`,
applied to a GROUP (`sdsshonly`) by the installer once — not per account
(no PowerShell cmdlet for account rights).** **Never deny network logon** —
Win32-OpenSSH authenticates via network logon, so denying it would lock out
ssh itself; this is the one thing to get right. **Cannot be `sdusers`** —
that grants file access and administrators are in it too. `AllowGroups` in
`sshd_config` is the second layer, an installer offer rather than something a
verb does silently (writes to a file SD does not own).

**Verified 14 Aug 2026 by control and treatment: the lockout did not happen.**
Implementation notes: it is a **child** task of OpenSSH's install (absent when
a server pre-exists); the administrators group is resolved from
`S-1-5-32-544`, never the name; four `AllowGroups` patterns cover bare and
`COMPUTER\`-qualified forms; the block is inserted **before** the first
`Match` line (the shipped config ends with `Match Group administrators`,
so appending would scope it wrongly); removed on uninstall, original kept as
`sshd_config.before-sd`.

**What ssh-only does not mean:** the deny rights control *where* an account
may log in, not *what it may run* — an ssh session lands in `cmd.exe` by
default; confining a user to SD is a separate control (not part of this
decision).

### 5.7 Where the OS still has to be involved: protecting the data tree

Dropping OS groups from SD's logic (§5.6) does not remove the need for OS
file permissions, and the two do not compose the way one would hope.

**The tension.** Every SD process opens the database directly, in its own
process, under the invoking user's own token — there is no data server. So
any ACL strong enough to stop a user reading the files in Explorer also stops
SD reading them on that user's behalf. **While SD runs as the invoking user,
account passwords organise access; they do not secure it.** This decides
whether accounts are private from each other: to enter account B a user's
token must have read/write on B's directory, because their own process does
the I/O — stage 1 therefore offers only two unwanted options (grant everyone
everything, or duplicate the password gate as per-user ACLs).

**What is achievable in stage 1:** lock the tree to `sdusers` +
`Administrators`, blocking everyone not an SD user; it does not stop one SD
user reading another's account files directly.

**A "run sessions as a dedicated service identity" proposal was raised and
rejected, 20 Aug 2026** — it is exactly what an API session already does by
accident (`verify-apiadmin.ps1` showed a PROGRAMMER-tier account opening and
writing `$cred`), and it is safe only if SD enforces access once the OS
cannot — which it did not, at the time (`op_openpath`/`open_file()` had no
path restriction). **The missing half is no longer missing as of 21 Aug
2026** — the containment gate in `op_dio2.c`, rooted at the session's account.
What still lacks is the *identity* half.

**Mechanics, verified 13 Aug 2026.** `C:\ProgramData` grants
`BUILTIN\Users:(I)(OI)(CI)(RX)` by inheritance (world readable by default).
Breaking inheritance and granting narrowly needs no elevation for an owned
directory:

```sh
icacls <dir> /inheritance:r /grant "*S-1-5-18:(OI)(CI)F" \
    /grant "*S-1-5-32-544:(OI)(CI)F" /grant "<principal>:(OI)(CI)M"
```

Use SIDs, not names. **`/inheritance:r` first is essential** — `/grant` alone
leaves the inherited `Users:(RX)` in place. **`noacl` breaks `chmod` but not
ACL inheritance** — the MSYS2 mount is `noacl` so `chmod` is a no-op, but
files created *through MSYS2* inside a locked directory still inherit the
restricted ACL correctly (NTFS applies inheritance at creation, below the
runtime) — confirmed by writing through MSYS2 into a locked directory. This is
what makes the installer's one-time `icacls` sufficient.

### 5.8 Install layout follows Windows standards (decided 13 Aug 2026)

Windows conventions, not Unix ones (`/etc`, `/usr/local` were stage-1
expedients).

| What | Where | Replaces |
|---|---|---|
| Binaries, and the MSYS2 DLLs beside them | `C:\Program Files\SD\usr\bin\` | `/usr/local/bin` |
| Mount table, mapping `/dev/shm` out to writable space | `C:\Program Files\SD\etc\fstab` | — |
| Configuration | `C:\ProgramData\SD\sd.conf` | `/etc/sd.conf` |
| The SDSYS account | `C:\ProgramData\SD\sdsys\` | `/usr/local/sdsys` |
| User accounts | `C:\ProgramData\SD\user_accounts\` | `/home/sd/user_accounts` |
| Group accounts | `C:\ProgramData\SD\group_accounts\` | `/home/sd/group_accounts` |
| POSIX shared memory | `C:\ProgramData\SD\shm\` | `/dev/shm` |

**`usr\bin` is load-bearing, not tidiness.** Shipping `msys-2.0.dll` beside
the executable puts the POSIX root at the DLL's directory minus **two**
components — see §6 for the measurements and traps. **Three siblings under
one root**, not SDSYS with accounts nested inside it — what makes §5.7's
single `icacls` sufficient.

**Three requirements, all met:** SD's home is under `C:\Program Files`;
login works from any starting directory (`sd.exe` finds its DLLs beside
itself); on login the current directory is the account's own.

**MSYS2 DLLs ship beside `sd.exe`** — Windows searches the executable's own
directory before PATH, which removes both the exit-53-silent-failure and
the Git-for-Windows `msys-2.0.dll` collision (§6).

**Configuration settled 14 Aug 2026:** server and client both read
`SD_CONFIG`, fall back to `%ProgramData%\SD\sd.conf`. `SD_CONFIG_ENV`/
`SD_CONFIG_DEFAULT` in `gplsrc/sddefs.h`, duplicated in `sdclilib.c` (§5.2) —
**change both together**.

**`sdrealpath()` fixed 13 Aug 2026** — it now folds backslashes and treats a
leading drive letter as the root; all five spellings of a Windows path open
the same file.

### 5.9 One installer: a staging script, then Inno Setup (decided 13 Aug 2026)

The `installsdai.sh` Linux port is **dropped** — Windows has one target, one
ABI, and ships its own runtime (§5.8), so nothing to abstract across distros.
Two scripts replace it: `stage.py` builds a staging directory holding exactly
what an install consists of; Inno Setup packages it. Neither the shell
installer nor `deletesdai.sh` is ported, though the latter is worth reading
before touching the uninstaller (records the Linux "what happens to the
database" answer).

**The staging script is the valuable half**, not mainly for packaging: it
makes §5.8 executable; it is a whitelist that finds accidental dependencies
(`gplsrc` sat in the data tree unasked-why until this caught it); it computes
the DLL closure by walking imports rather than guessing (missing one gives
exit 53, no message).

**What the installer does:** lay down both roots; **set the ACLs on the data
tree with `icacls`, breaking inheritance first** (§5.7); create `sdusers` and
`sdsshonly`; run the §3 bootstrap; register the service (§5.7).

**OpenSSH Server is ALWAYS INSTALLED, network exposure is opt-in** (owner,
16 Aug 2026 — reversing an earlier unconditional-off stance). ***BOTH HALVES
OF THE ORIGINAL "WHY" ARE FALSE, 2 Sep 2026 (PRE_RELEASE 123/124)*** — the API
is an independent listener, not an ssh tunnel, so an install without ssh is
usable; `install-ssh.ps1` runs under `Check: SshServerAbsent` and the
`sshserver` task is opt-in, default off. *(Kept as the record of superseded
reasoning: it used to be argued that SD accounts sign in over ssh and nothing
else, so a no-ssh install serves nobody but the installing user — no longer
true.)*

**`sshremote`, off by default, is stricter than what it replaces** — it
scopes the firewall rule to loopback unless ticked (`ssh-firewall.ps1`),
because the plain "enable OpenSSH" capability opens port 22 to any remote
address as a side effect. **`limitssh` (was `installssh\allowgroups`) is
top-level, has no `Check`, and is ticked by default** — protected only by
refusal 2 inside `allow-ssh-groups.ps1` (an existing `AllowGroups`/
`AllowUsers`/`DenyGroups`/`DenyUsers` line is somebody's policy and the
script exits 2, leaving it alone). ***ON A MACHINE WITH A STOCK `sshd_config`
(no such line), refusal 2 does not fire, and the default-ticked box edits an
ssh server SD did not install. This is a decision for the owner, not fixed
quietly — not started.*** Options: unchecked by default, gate on
`SshWasAbsent`, or rule a stock config fair game. **The uninstaller does not
widen the rule back** (no `RemoveAllowGroups` restoring the opened port).

**Requirements, each already cost something:** detect a pre-existing server
**without elevation** (`sshd.exe` on disk or `sshd` service registered —
`Get-WindowsCapability -Online` needs elevation) and never reconfigure or
restart it; a failure to install must not fail the SD install (report and
carry on — Features on Demand can be blocked by policy/WSUS/metered/offline,
and no account but the installing user's can sign in anywhere until it
succeeds); **it is SLOW** — `Add-WindowsCapability` can leave `RebootPending`
for minutes with no wizard progress (it reads as a hang) — never kill it,
say it will take minutes, say the reboot is real; the uninstaller must not
remove it.

**Be honest about the "ten users over ssh, one machine" case:** each needs a
Windows account, which §5.6's OS provisioning makes manageable — but it does
**not** give them isolation from each other's data until §5.7's service model
lands (every process opens under the invoking user's token). Anyone
deploying this way should be told plainly.

### 5.9.1 What the uninstaller does (decided 14 Aug 2026)

**Standard Windows uninstall** — Inno registers under `Uninstall`, removes
only files it installed, from its own log, and only empties directories.
**The default must not touch accounts, the database or the configuration.**
`sd.conf` is `uninsneveruninstall` + `onlyifdoesntexist` (an upgrade must not
overwrite edits). The pre-bootstrapped `gcat`/`GPL.BP.OUT` are shipped files
and Inno removes them correctly (program, not data) — the shipped/user's-own
boundary runs through the middle of `sdsys`, so anything new added to the
ship list needs the uninstaller kept in mind.

**Removing the data is a separate, opt-in choice**, asked from `[Code]`,
defaulting to keeping it. The prompt must say exactly what it destroys and
where; **a silent uninstall must never delete it** (`/SUPPRESSMSGBOXES` does
not do what you'd expect here — §6).

### 5.10 Other BASIC to C linkages, surveyed

Full findings: HISTORY, 13 Aug 2026, "Surveyed every BASIC to C linkage."
Still open: `SYSTEM(n)` — only 27 (§5.5), 91/1006 (§5.4) and 1010 matter;
1010 is fixed (`PLATFORM_NAME` is `"Windows"`, token `SD.WINDOWS`); 1006
(`is_nt`) is still hard-wired 0 and undecided. `OSPATH`/`KERNEL` — enumerated,
not reviewed. `SDEXT` — used by `EUID_*` and the libsodium wrappers; the
`PY_*` family is gone (§5.15, §5.27). `OS.EXECUTE` — shell-outs in 10 files;
account commands are §5.6. Compiler chain carries no platform branches beyond
`@ds` (§6) and `SYSTEM(91)`.

### 5.11 No binaries in the repository (decided 13 Aug 2026)

**Reversing** the earlier position that tracked `bin/` binaries for the
install scripts. **Nothing binary is tracked; everything must be auditable
from source** — the same reason `gplbld/` is Python, not a shipped binary.
`.gitignore` excludes `bin/` and every `.exe`/`.dll`/`.a`/`.o`/`.so`/`.lib`/
`.obj`. Anything that must ship as a binary ships outside the repository as a
release artefact — no convenience exception. **Installing means building**,
but only for whoever runs the staging script; the end user's Inno installer
needs neither a clone nor a toolchain. **History was rewritten 13 Aug 2026
to purge every binary**, past and present; every commit hash changed
(mapping: HISTORY, "History rewritten to purge every binary"). The install
recompiles I-types, so dictionary items carry source and checksum only.

### 5.12 Lower case everywhere it can be (decided 13 Aug 2026)

**Goal: everything that can be lower case should be lower case.** Forced up
today by three things: **account names** (`upcase()`d throughout, which is
why login is case-insensitive), **the terminal** (`PT$INVERT` case-inverts
typed input — the visible half of the password-upcasing trap in §6), and
dictionary/VOC item ids. Sequencing: comparison must stay case-insensitive
while upcasing is removed, or `sue` and `SUE` become different accounts.

**Two independent halves: (a) the name on disk, (b) the VOC record id.** The
conversion direction is downward (`upcase(` → `downcase(`), and it is
**additive, not a flip** — every lookup site tries the token as typed, then
falls back to upper case (`PARSER`, `QPROC`, `CPROC`/RUN); adding a
`downcase` attempt in front changes no existing behaviour, since with every
id currently upper case the new attempt can never hit. Replacing the
`upcase` attempt instead would have broken every not-yet-renamed id.

**(a) IS DONE — 19 Aug 2026**, `verify-lcnames.ps1` 115/115. Every SDSYS
file name and each account's own files (`$hold`, `bp`, etc.) are lower case;
`VOC` deliberately stays upper case as the control. **The fact the whole
thing turns on:** `create.file <path> DYNAMIC` in BASIC is a language
statement taking the path exactly as given — it is *not* the `CREATE.FILE`
verb, which upper-cases on disk. So `BBPROC`'s file list and `CREATEA`
decide the case of everything created, with no `CREATEF` change needed.
**No migration needed** — each account's VOC names its own files and NTFS
matches either case. `$COMO` is the one deliberate holdout (its on-disk name
and VOC id share one `$define`; nothing in `gplbld` exercises it).

**(b), the VOC-id fold, measured 76 sites in 38 files (18 Aug 2026), DONE AND
VERIFIED.** Four traps for anyone doing this again: fold sites **nest**, so
indices go stale mid-batch — recompute after every single edit; a converted
site can re-detect itself as unconverted; `if cond then <stmt> else/end` is a
block whose opener doesn't end in `then` — miss it and an inserted `end`
lands inside the wrong block (compiles and balances cleanly, wrong anyway);
the trailing rewrite variable isn't always the same name as the read (mirror
the existing line, don't regenerate it from the read). **The balance check
(openers − closers unchanged) is necessary and not sufficient — `cycle.ps1
-SkipInstall` is the real check**, and it is what caught the last two.

`_VOC_REF` (`pcode_voc_ref`) needed a **second, separate fold** — it resolves
every BASIC `OPEN`, was missed by the 38-file sweep, and reaches it through a
flag-and-`goto`, not a nested block. **A hard-coded literal VOC id bypasses
the fold entirely** — 13+ sites (`$SAVEDLISTS`, `EDIT.LIST`, etc.) would have
broken at the first VOC-id rename; each rename must sweep for its own
literals. **"Not found" is the wrong instrument for a VOC-id rename** — `CT`
and `COUNT` both fold the id themselves, so they cannot show a fold failure;
`LIST` does not fold, and is now the test.

**`BASIC bp X` creates `bp.OUT`, permanently unreachable** — object file
names come from the source name **as typed**, not upcased, so `bp` gives
`bp.OUT` and the fold (as-typed/lower/upper) can never match a mixed-case id.
Fixed by reading the name from the VOC record that answered the open (not
discarding it) and letting the `.OUT` suffix follow that name's case.
`DELETE.FILE bp.OUT FORCE` recovers a poisoned one.

**Renamed so far, each with its own cost inventory (see HISTORY for detail if
ever repeated): `$SAVEDLISTS`→`$savedlists`, `$HOLD`→`$hold` (including
`voc_template`'s own record, and the `"$HOLD "` file-content prefix, which
folds rather than flips on both the BASIC and C sides since they build at
different times), all 792 TCL command ids across `NEWVOC`/`VOC_TEMPLATE`/
`SD.VOCLIB`** (excluding the `$`/`%`/`@` records and F/Q file pointers, which
move with (a)), **`BP`/`BP.OUT`/`GPL.BP`/`GPL.BP.OUT`** (cost: four
`voc_template` record renames since there the id *is* the filename, plus
`MICRO`'s undetectable tenth comparison site — a substring test against a
filename, not a VOC-id comparison, invisible to the id-based audit).
**`git mv` does not work for 792 records or for a directory rename under
`core.ignorecase=true`** — rename on disk through a temporary name, then
`git -c core.ignorecase=false add -A` (plus `rm -r --cached` per directory
for the directory case). **`$COMMAND.STACK` and `BP`/`$COMMAND.STACK` are
what remain of the case-controls in `verify-lcnames.ps1`** — whatever moves
next must bring a replacement control with it.

### 5.20 `cub1` was empty because NO type had loaded, not because cub1 was missing (22 Aug 2026)

**Answers the open item "why `cub1` came back empty".** `tsettermtype()`
calls `free_terminfo()` only after the open succeeds, so a terminal-type
name with no entry leaves `tinfo` NULL and `sdtgetstr()` returns `""` for
**every** capability, not just `cub1` — until one `settermtype()` succeeds.
**The name is `xterm-256color`, supplied by the MSYS2 runtime**, and
`terminfo/x` holds only `xterm`. **The prompt is inside `$LOGIN`, the repair
is after it** — `TERM WINDOWS` (the `login` paragraph) runs at `CPROC:411`,
after `$LOGIN` returns at `:324`, so the password prompt and the sign-on
clear screen are the only places in a session always in the unrepaired
state. **Every earlier reading of this was taken at the `:` prompt**, which
is always *after* the paragraph has run — that is why `verify-keys` passed
while backspace was reported broken live.

**The fix, in `LOGIN`:** downcase, ask, check — `kernel(K$TERM.TYPE, s)`
returns the type actually in force and leaves it unchanged on failure, so a
mismatch is the failure signal; fall back to `windows`. **What the fix does
NOT do:** the installer's own scripted session has no capability-dependent
output left (`_INPUT` already erases with a literal `char(8)`, and
`sd -QUIET off` skips the clear screen), so the obvious install-log test is
a no-op either way — what changes is `LOGIN:200`'s clear screen in an
ordinary interactive session. **This also corrects §5.18**, which claimed
`env('TERM')` never runs and cannot change the terminal type — both wrong,
for the same "measured at the `:` prompt" reason. **Upstream has the same
bug** — UPSTREAM_FIXES.md #12.

### 5.19 REMOVED WITH ITS SUBJECT: the full-screen editors are gone (23 Aug 2026)

`SED` and `UPDREC` were removed 23 Aug 2026; the key-table work §5.17/§5.18
recorded for them has nothing left to apply to, and `verify-editkeys.ps1`
went with them (measurements: HISTORY, 19 Aug). **What is still live is in
§5.17/§5.18**: on this platform Backspace is `127` and Delete is
`ESC [ 3 ~`, and that governs the command line, which still exists
(`verify-keys.ps1`). **`ED` was never affected** — it is the LINE editor,
reads with `input`, and goes through the command-line fix; if backspace is
ever reported broken in `ED`, that is a new fault.

### 5.18 The arrow keys were dead because of the default terminal type (19 Aug 2026)

**Owner, 19 Aug 2026: left/right arrow, backspace, clear screen dead in cmd,
PowerShell, Windows Terminal.** Root cause: a regression from 18 Aug, not
from the backspace fix — `login` was changed from `TERM LINUX` to
`TERM VT100`, backwards, since `linux`/`ansi` are the ANSI/normal-cursor-mode
entries every Windows console actually speaks (`ESC [ D`), while
`vt100`/`xterm` expect **application cursor mode** (`ESC O D`), which SD
never enters (`smkx` is never sent).

**The fix: one type that matches Windows.** `terminfo.src` gained
`windows`, a byte-exact copy of `linux`; `login`'s default and `LOGIN:116`'s
fallback both use it. The other 61 entries are still shipped. **This
section's original "the paragraph decides it" claim is wrong — see §5.20.**
**Clear screen was never broken** — measured with a `seq()` probe, and the
owner confirmed it at a console; treat it as collateral in the original
report, not a fifth fault.

`sd.exe` links `msys-2.0.dll`, so Cygwin's console handler is what turns key
presses into these byte sequences — the same argument holds for cmd,
PowerShell and Windows Terminal alike. **A pipe is not a console, and every
early instrument here was a pipe** — `verify-keys` passed 6/6 while the
owner watched backspace fail live; it is now 10 checks (§5.17) and
distinguishes both-arrows/one-arrow/neither.

**`sdtic` had its own defect, fixed here (`UPSTREAM_FIXES.md` #9):** a failed
terminfo entry left `reset_buffers()` un-run, so one bad entry corrupted
every entry after it and segfaulted partway through, with stdout
block-buffered so nothing printed; `sdtic` also always exited 0. Both fixed.
**`gplbld\probe-keys.ps1`** is the only non-piped instrument here — compiles
a probe into the caller's own `bp`, starts `sd` in the current console, and
prints every byte each key sends. **Reach for it for any keyboard question.**

### 5.17 The keyboard: accept both spellings of a key, not the one terminfo names (19 Aug 2026)

**Backspace did nothing in cmd, PowerShell, Windows Terminal**, and in PuTTY
unless reconfigured. **A terminal sends Ctrl-H (8) or DEL (127) for
backspace and the protocol does not say which** — `_KEYCODE` built its table
from terminfo alone, so SD accepted whichever byte the active type named and
silently discarded the other. **Every Windows console host sends DEL**, and
`TERM` was unset, defaulting to `vt100`, whose `kbs` is `^H`. **No choice of
terminal type could have fixed it** — of 62 `terminfo.src` entries, only
`xterm` and `linux` say DEL; 51 say `^H`.

**The fix binds both bytes, before terminfo binds** — `bind` replaces an
existing binding, so anything terminfo claims still wins, and the two
defaults only fill what nothing else claimed. Changing the default terminal
type instead was rejected — it would just point the same bug the other way,
breaking every terminal that sends `^H`. **Testable from a pipe**:
`COUNTX<erase> VOC` runs `COUNT VOC` if the erase worked, `verify-keys.ps1`.
**The full-screen editors carried their own key table and were removed 23
Aug 2026 — §5.19 — so this applies to the command line alone.**

### 5.13.1 The ForceCommand scp cost has a workaround: pull, do not push (17 Aug 2026)

**The global `ForceCommand` stays global** (owner, 17 Aug 2026) — a
`Match Group sdsshonly` alternative was rejected again, since it would hand
remote administrators a PowerShell prompt. **The cost — scp/sftp stop
working machine-wide — is INBOUND only.** `ForceCommand` applies where this
machine is the ssh **server**; outward connections (this machine as client)
never consult `sshd_config`. **So an administrator copies files by
PULLING them**, from console or RDP (never in `sdsshonly`); outbound is not
firewalled. **What genuinely cannot be done: pushing a file TO this machine
over ssh** — nobody can, administrators included, and that is the accepted
cost. **Do not "fix" this with a `Match Group administrators` exemption
without reading this first** — `sshd_config` takes the FIRST obtained value
per keyword, and the block is inserted before the first `Match`, so a later
override is not guaranteed to win; unresolved, and pulling avoids the
question entirely.

### 5.13 Shell access is restored, not blocked (decided 13 Aug 2026)

Disabling `SH`/`!` in the Linux version was a mistake; Windows makes it a
worse one (many programs must reach Windows utilities). **Measured against
`sdb64` itself, 15 Aug 2026: neither `main` nor `dev` blocks anything** —
`CPROC`'s `os.command:` runs straight into `os.execute`, `K$SECURE` is a
login flag, not this. So there is nothing upstream to restore; the only
block ever in this lineage was the generation-2 gate at `CPROC:3321`.
Whether the gate should stay is §7 step 7's question, unaffected either way.
Shell-out runs as the invoking user and grants no access beyond a command
prompt — §5.7's service model, not a block on `SH`, is what makes the data
tree private.

### 5.14 Administrative logic goes in a subroutine, because the forms are a SEPARATE PROJECT (owner, 23 Aug 2026)

**The forms are out of scope here** — they belong to a separate set of GUI
utilities, not necessary for a working SD (§7 step 10 removed on this
ruling). **The rule survives and matters more: new administrative capability
goes in a SUBROUTINE with a verb over it**, never logic buried inside a verb
— it is now the only way something outside this repository can reach it at
all (a catalogued subroutine or the API, nothing else). `CRED_SET`/
`CRED_VERIFY` under `SET_ACC_PASSWORD` is the pattern to copy. **Still
shaped like a command line, for whoever writes those utilities:** the grants
verb (§7 step 5), `os.users` and `batch.jobs` (both edited with `ED` from
SDSYS today).

### 5.15 Embedded Python is dropped; the API is the point (decided 13 Aug 2026)

**A statement about what SD for Windows is for**, not packaging: the
intended user reaches SD as a back-end data store, through the API —
embedded Python was not part of that. Removed outright (C sources, Makefile
flags, 20 `GPL.BP/PY_*` programs, `SYSCOM/SDPYFUNC.H`, `SD_Py*` error codes,
SDEXT keys — itemised in HISTORY, "Embedded Python removed"). Took two build
dependencies with it (`python-devel`, `gettext-devel`); plain `python` is
still needed by `gplbld/` for the developer. **Reopened 10 Sep 2026 as a plan
for after W1.0-0** — Python installed on the machine, not shipped in the
installer; see §5.27, RULED and BUILT.

### 5.16 Convert every remaining Linux-ism, and the installer outranks Linux parity (decided 14 Aug 2026)

Two ordering rules, owner, 14 Aug 2026: **(1)** every remaining Linux-ism is
converted to its Windows equivalent where one exists — not wrapped, not
flag-guarded, not left because it looks harmless (`/bin/bash` looked inert
and silently broke every installed system, §6). **(2)** where Linux parity
and the Inno installer conflict, **the installer wins** — drop the Linux
behaviour rather than complicate the install.

**Known remaining Linux-isms** (working list): `PASSWD_FILE_NAME
"/etc/shadow"` (`sdnet.h`, §7 step 6); `SYSTEM(91)`/`is_nt` (§5.4); the
`usr/lib/systemd/`/`etc/xinetd.d/` tree, kept deliberately as topology
documentation; `@ds` hardcoded `/`, live for stage 2 only (§6). Done: `sudo
chmod g+s` → inheritable ACEs (§5.7); `PLATFORM_NAME` → `"Windows"`;
`setuid`/`setgid` in `login_user()` → nothing, SD accounts are not OS users
(§5.6); `EUID_SET`/`EUID_RESTORE` chain removed entirely, 5 Sep 2026
(PRE_RELEASE 168); `installsdai.sh`/`deletesdai.sh` not ported (§5.9).

**What "Inno compatible" required, all seven decided and all but service
registration done:** no dependency on a shell Windows lacks (done, §6); the
layout move (§5.8, done); one config file with no env var needed (done);
**pre-bootstrap the staged tree** — `stage.py --bootstrap` runs the
bootstrap on the build machine at the production path, so **installing is a
file copy** and the end user needs neither Python nor a compiler (before
this, `gplbld/` was absent from the ship list and the staged tree was not
installable at all); `icacls` on the data tree (§5.7); set the SDSYS
password last, after the bootstrap; decide the uninstaller's data handling
(§5.9.1, settled). **Elevation is a point in the installer's favour** — Inno
runs elevated, which is exactly what the OS account commands need (§5.6).

### 5.27 Python runs in a helper process, not inside `sd.exe` (owner, 11 Sep 2026)

**RULED, 11 Sep 2026.** Python comes back as a separate native process SD
talks to over a pipe, not a library loaded into `sd.exe` — because the MSYS2
and native runtimes must never meet in one process (§5.3: `long` is 8 bytes
on one side, 4 on the other; the removed code's `FILE*`-across-runtimes
crossing could not survive it). A native shim DLL was the rejected
alternative — cheaper in principle, breaks §5.3 deliberately; put to the
owner with that cost stated, and he chose the helper. **What would falsify
the ruling:** a native `python314.dll` loaded through a fixed-width shim,
exercised and run clean — nobody has attempted it.

**BUILT AND WORKING, 12 Sep 2026.** `gplbld/sdpy.c` — native UCRT64,
**27 then 53 of 53** over a real pipe, all twenty `PY_*` verbs backed. The
MSYS2↔native pipe itself is proven (`sdpy_client.c`, 9/9: handshake, marks
and NUL round-trip byte for byte, tracebacks on failure without desyncing
the pipe, clean shutdown) — `CreatePipe`/`CreateProcess`, not
`fork()`/`exec()`. **The C integration into `sd.exe` is done and compiles**
(`sdpy.c` in its own directory so `TEMPSRCS`' wildcard doesn't compile it
with POSIX flags; `sdpy_client.c`/`sdpy_session.c` inside `sd.exe`;
`op_sdpyobj.c`; `opcodes.h`'s `0xCFFE` un-retired at the same number; err
codes `-12001..-12034` restored unchanged plus `-12040`, for the helper not
being there at all — a failure mode an in-process interpreter never had).

**The permission gate is per-session, at start, not per call** — the
process *is* the privilege. `sdpy_session.c` calls `sd_os_permitted()`, a
wrapper (not a copy) around `op_sh.c`'s `os_permitted()`, since Python's
`os.system` never reaches it directly and two implementations would drift
permissive. ***CORRECTED 13 Sep 2026 (RELEASE_1.1 23): the wrapper as first
built ran inside `!PY_INITIALIZE`, whose `HDR_INTERNAL` flag made the first
of three tests answer TRUE before the username was even read, admitting
everyone.*** `os_permitted()` is now split — test 1 stays, tests 2/3 became
`os_user_permitted()`, called by `sd_os_permitted()` — the shape the design
required. **The payload is Latin-1** (marks/NUL are not valid UTF-8) and
**framing is length-prefixed, not line-based** (payloads can contain NUL and
marks) — both decided from measuring the removed code's own error names.
**Objects are named, not handled** — no id to leak, and names are
per-session state, an independent argument for the per-session helper.
**Five things the new version does that the old could not:** returns the
real traceback (old surface returned only an int); captures `print()`
(stdout IS the protocol channel — an unredirected print would desynchronise
every frame after it); one shared namespace between SD and script globals; a
versioned `HELLO` handshake; the always-`@FALSE` flag argument is gone
entirely rather than carried forward unused.

**Not built yet:** the BASIC half — `syscom/KEYS.H`, `SYSCOM/ERR.H`
regeneration, `BCOMP`'s intrinsics table, the 20 `PY_*` programs. **Tree is
deliberately stale**, paying the cycle this step always owed.

***DECLINED, 11 Sep 2026, scope ruling: no UniVerse-style HTTP server from
TCL.*** A tester noted UniVerse ships Python plus FastAPI/Uvicorn and asked
whether SD should. Three separable asks, only the first is in 1.1: (1)
Python present and callable — this section. (2) a curated third-party
package set — **not adopted** (compiled wheels re-raise the ABI-pinning
problem §8 flags). (3) a long-lived HTTP listener started from TCL —
**declined** — it is barely a Python question: an SD session is
request/response and a listener must outlive it (a detached, service-shaped
process); every existing gate is at connection time and a session-started
listener is covered by none of them; API sessions run as LocalSystem, so a
spawned process inherits that unless deliberately dropped; ports are not
generalised today (§5.26). Not an argument it cannot be done — an access
ruling would be needed before any code.

### 5.26 The API port stays 4243, on Windows and Linux (owner, 10 Sep 2026)

**Ruled.** `APIPORT=4243` stays shipped on both ports; Linux is a separate
repository. **Upstream `sdb64` uses 4245** to avoid colliding with OpenQM,
so a client written for upstream needs 4243 explicitly — comments calling
4243 "the Linux build's port" describe the owner's Linux build, not
upstream. **What the ruling accepts:** where OpenQM already holds 4243, SD
starts with no API and logs it, and there is no supported end-to-end way to
choose a different port today (`api-listener.ps1`/`api-firewall.ps1` both
hardcode 4243). **Reached after a same-day switch to 4245 was proposed and
withdrawn** once the upgrade consequence was seen: `sd.conf` is
`onlyifdoesntexist`, so an upgraded machine would keep 4243 regardless, and
reconciling that costs more than it's worth for W1.1. **Found in the same
survey, not filed:** `sdclilib/USER_GUIDE.md` examples use port 4242
(OpenQM's telnet port, not the API); `APIPORT` is `int16_t` with no range
check, so a hand-set port above 32767 silently misbehaves.

### 5.25 Administration requires an interactive desktop (owner, 5 Sep 2026)

> ***READ THIS BOX FIRST. The rule holds; the mechanism this section
> describes was deleted by RELEASE_1.1 64, and this box corrects the section
> below to say so — correction added 22 Sep 2026, from RELEASE_1.1 102's
> measurement and 61.***
> `PEER_LOCAL`/`!peer_local`, the `system(42)` API half, `vb.scram.final`'s
> gate and `sd_admin_tier` are gone (`login:527-534`, `apisrvr:1712-1717`).
> **What enforces the rule now:** there is only ONE SD administrator, SDSYS
> (64), and **SDSYS has no remote route at all** — no ssh (`MODIFY.ACCOUNT
> SDSYS SSH` refuses, 12001), no socket API (only `SDConnectLocal`, which
> opens no socket — 101). Every other account has no administrator flag to
> obtain. `kernel.c:296` seeds `USR_ADMIN` only when elevated **and**
> `connection_type # CN_SOCKET` **and** interactive — the desktop requirement
> is satisfied by construction, nothing needs rebuilding. **SD asks for no
> elevation anywhere**, so an unfiltered administrator token is reachable
> only by an account that already holds administrator rights (the
> installer's own account, and SDSYS) — see §5.29 for whose problem that is.

**The rule.** Administration happens at the console, or through a
remote-control product or single-user remote desktop — **not from another
machine.** Owner, 5 Sep 2026: *"Remote admin through api or ssh is just a
security nightmare waiting to happen."* **Refined the same day** after the
first build refused *local* ssh too: *"local API and SSH should continue to
work — if I am at the console, everything works, only remote access is
denied."* **REMOTE is what is denied, not a transport** — "local" means
LOOPBACK, not LAN (measured: a connection to the machine's own LAN address
is remote).

***THE MEASUREMENT THAT DROVE IT, AND IT REVERSED WHAT THIS FILE BELIEVED.***
§5.6.1 predicted a remote ssh administrator would get a **filtered** token
and be *unable* to reach SDSYS — the opposite happened: sshd runs as
LocalSystem and builds the logon token itself, so
`LocalAccountTokenFilterPolicy` never applies to it, and an ssh'd-in
administrator got a fully **elevated**, unfiltered token. §5.6.2's "console
belongs to administrators, ssh to everyone else" was Windows-enforced only
in belief — this moved the enforcement into SD, where it is testable.
**The part SD cannot enforce, belongs in documentation:** "remote desktop
(single-user), not RDP Server on Windows Server" is a deployment choice a
token cannot see, and a remote-control product only qualifies if installed
as a **service** (a per-user install cannot render the secure desktop).

### 5.24 The BASIC functions and operators, verified (31 Aug 2026)

***THE SURFACE IS SOUND. 169 value cases, 0 failures*** —
`gplbld/verify-basicfuncs.ps1`. Structural links all hold by design, not by
audit: `opcodes.h` is an X-macro table (`_opc_(0x2A, OP_ABS, "ABS", op_abs,
…)`) that generates `dispatch[]`, the compiler's intrinsics table and
`gpl.bp/OPCODES.H` all from one source — drift is structurally impossible.
**All 20 "failures" on the first run were the test's wrong expectation, not
the product** (`MD` inserts rather than rounds, `SHIFT`'s positive count
goes right, `SUBSTITUTE` splits by marks, `LOCATE arr<1>` searches fields,
`DTX` returns lower case, etc. — recorded at the case in `basicfuncs.sb`).
**Wired into `VerifyInstall1`, 17 steps.** Same pass found PRE_RELEASE 107:
`verify-tierchange.ps1` (parent of `-acctmsgs`/`-vocverbs`) is in neither
runner and wants the elevated one — filed, not fixed.

### 5.23 A query must never answer wrongly (owner, 31 Aug 2026)

*"`LIST ACCOUNTS` must be absolutely accurate... this is a blocking
defect."* **The corollary, wider than one verb:** *"This is a database
application. No failure is more severe than misreported data... not just to
the administrator but for every user."* **So this is the project's severity
ordering, not a rule about listings** — a wrong answer outranks a crash
(visible vs. invisible), and anything in this class is `B`.

**The archetype, on the core data path:** PRE_RELEASE 11, a nested `COMMIT`
silently abandoning the outer transaction — fixed, with a standing verifier
(`verify-txn`, 9/9) precisely because a silent wrong answer is the kind that
comes back unnoticed. No open entry is on the core data path today.

**Classified against the corollary** (measured unless noted): 93 (`LIST
ACCOUNTS` names dead accounts), 65 (`LIST OS.USERS` names dead grants), 94
(false success message on a grant that didn't happen), 95 (a failed header
flush marks the file clean), 96 (an incomplete privilege check reported as
"not an administrator"), 97 (65's symptom by a second route), 98 (an audit
line for an event that never occurred), 99 (an unchecked identity-setting
call), 100 (an AK allocator's "could not" answers 0, corrupting the index
header — **no self-heal**), 101 (`DELETE` inside a transaction on a
directory file cannot fail, so the commit lies), 102 (a half-applied commit
never rolls back and never releases its locks — 11's leftover), 103
(`WEOFSEQ`/`OPENSEQ OVERWRITE` report a truncate that didn't happen), 105
(a verifier anchored on its own echoed input — instrument, not product).
**80 is `B` on its own account too** — documentation describing a model the
product no longer has is the same failure in prose. **Candidates needing
the owner's eye:** 67, 88, 89, 20.

**Measured 31 Aug 2026: two files answer wrongly today** — `LIST ACCOUNTS`
(26 of 28 dead), `LIST OS.USERS` (5 of 6 dead). **Settles 65's open
question**: documenting the recovery step in a transcript nobody reads is
not enough — the record must actually be removed when the account goes, not
swept at start-of-run (which leaves the query wrong *between* runs). The
`ACCOUNTS` record itself stays, since it is the evidence of what happened.

### 5.22 What an administrator has as themselves, and what needs SDSYS (owner, 31 Aug 2026)

*"Administrators logged in as themselves need to have full access to
everything EXCEPT the ability to issue the restricted administrator
commands. They have to log to sdsys to do that."*

| | as themselves | in SDSYS |
|---|---|---|
| enter any account, **no grant needed** | yes | yes |
| the 41 capabilities (`TIER.OMIT.STANDARD`) | yes | yes |
| the 24 restricted commands (`TIER.ADD.ADMINISTRATOR`) | **no** | yes |

**"Administrator" means both, decided earlier and already built — do not
re-derive it:** `LOGIN:573` is the predicate
(`kernel(K$ADMINISTRATOR,-1) and kernel(K$OS.ADMINISTRATOR,0)`);
`LOGIN:417` refuses a non-`sdusers` Windows user (5009); an account made
outside SD has no SD access until a matching account is created inside SD
(56 removed the old administrator exemption from the `sdusers` gate). **Not
a boundary against a Windows administrator** — they can add themselves to
`sdusers`; this is an explicit act and an audit trail, not a barrier.
**Access and privilege are different questions** (PRE_RELEASE 91 was
conflating them) — which accounts a person may ENTER must not be answered
by the flag that says what the session may DO.

### 5.21 No control may be inert (owner, 31 Aug 2026)

*"No option should be available that the user can click thinking that an
action is going to take place, but nothing happens."* **A tickbox is a
promise; one that can't act is a false statement.** Two ways to satisfy it:
don't offer it (`sshserver`'s `Check: SshServerAbsent`), or make it act in
both directions and default from the live truth
(`sshremoteshut`/`sshremoteopen` default from `GetSshRuleIsOpen`, and
`ApplySshFirewall` runs `-Open`/`-Restrict` on every install regardless of
whether the box was touched). **It applies hardest on an upgrade, where it
is currently broken** — PRE_RELEASE 89 found `apiremote` (config is
`onlyifdoesntexist`, an upgrade rewrites nothing either way) and `addtopath`
(nothing removes SD from PATH outside the uninstaller) both inert on a
second install; neither fixed, recorded so the next control isn't built the
same way. **Check a new control's OFF direction** — the ON direction is the
one anybody thinks to test.

## 6. Traps

Each of these cost real time. Read before debugging anything similar.
**Never cut one for size** (§0 rule 4) — trim the telling, keep the lesson.

- ***AT (5) OF THE REAL-UPGRADE SEQUENCE THE COMMAND IS THE INSTALLER, NEVER
  `cycle.ps1`.*** 17 Sep 2026, RELEASE_1.1 40. A cycle uninstalls and deletes
  both trees — run in place of `sd-setup-W1.1-0.exe` it destroys the W1.0-0
  tree the earlier steps built and snapshotted. **In a hand-over, each
  step's command goes directly under its heading, and a step with a
  destructive look-alike says what not to run.**

- ***A PROCESS-LIST PROBE MATCHES ITSELF.*** 28 Aug 2026. A `CommandLine
  -like '*sd-elevate-helper*'` search returned 1 — the PowerShell process
  running the query itself, since its own command line names the pattern —
  and read as "a helper survived" when nothing had. **Exclude `$PID`**, and
  **prefer evidence that cannot name itself** — a named pipe's presence
  (`[System.IO.Directory]::GetFiles('\\.\pipe\')`) rather than a process
  name or command-line match.

- ***ONE EMPTY STRING IN A `-ArgumentList` ARRAY REJECTS THE WHOLE ARRAY,
  SILENTLY.*** 28 Aug 2026, PRE_RELEASE 43. `Start-Process -ArgumentList`
  carries `[ValidateNotNullOrEmpty()]` on **every element**, so
  `@('-NoProfile','-Password','')` fails binding with a message naming no
  element — reads like the whole parameter was omitted. **Data-dependent**:
  `verify-doors-suite.ps1`'s Create leg (password present) worked, Suspend
  and Remove (password `''`) died before their UAC prompt — no window, no
  child, no log. **Fix: omit the pair, don't pass a placeholder.** Print the
  argv and its element count, and refuse an empty element by name.

- ***THE SUITE'S PASS COUNT WAS GREPPED OUT OF FILES NOTHING COULD READ.***
  26 Aug 2026. `VerifyInstall2` writes its 19 per-step logs as **UTF-16LE**
  (from `Start-Transcript` in the elevated child); everything else is UTF-8.
  **`grep` reads UTF-16LE as binary and matches nothing, silently, exit 1** —
  a plain grep over `b43`'s 47 files read only 27 of them and undercounted
  PASS by over a third. **The dangerous half wasn't the undercount — it's
  that `0 [FAIL]` measured nothing at all for 19 of 31 elevated steps**,
  since every `[FAIL]` line lived in exactly the files the grep couldn't
  read. Both runs really were clean (decoded and confirmed), so the verdict
  was right and the instrument wasn't — what actually carried those runs
  was the step exit codes. **Fix: decode, print the per-encoding subtotal
  (a 0 UTF-16 subtotal means the decode did nothing), and control against a
  run that DID fail.** **The pattern is bare `PASS`, not `[PASS]`** —
  verifiers don't agree on a format, and anchoring on `[PASS]` drops whole
  verifiers to zero. Unelevated per-verifier logs are copied wholesale into
  the combined log, so a flat sum double-counts them; elevated per-step logs
  are not duplicated.

- ***WINDOWS AND PYTHON DISAGREE ABOUT WHERE A HYPHEN SORTS.*** 26 Aug 2026.
  Explorer's collation ignores the hyphen (`01a-first-run` sorts before
  `01-installation`); Python's `sorted()` compares bytes (`-` is `0x2D`,
  `a` is `0x61`, so it sorts after). Three new doc pages rendered in the
  intended order by `mkdoc.py` and listed in a different one by the folder —
  the owner reported them missing; they'd been there an hour. **Use names
  that cannot disagree** (`00`–`13`, no letter suffixes) anywhere an
  ordering is both user-visible and script-consumed.

- ***PIPING A COMMAND INTO `sd` HANGS THE SESSION AND LEAVES A STRAY
  PROCESS. `echo WHO | sd` IS THE ONE THAT KEEPS BEING TYPED.*** 23 Aug 2026;
  it hung, and the stray `sd.exe` cost an elevation to clear. **The
  mechanism is not "pipes do not work" — SD is blocked on a prompt (the
  account's `New password:`) it can never be answered**, from a read that
  gets no input; CPU cycles between 0 and 0.3s across 26 seconds — blocked,
  not looping, and no errlog entry because nothing has gone wrong from SD's
  side. **If SD looks quiet, find its stdout before theorising** — the same
  day, "no output" turned out to be a redirect nobody had read, with the
  password prompt in it the whole time. **The shape that works:** feed a
  whole script ending in `OFF`, via `Start-Job` with a timeout, and on
  timeout say so and `Stop-Process` the named `sdwind` PID — a timed-out
  session leaves its user-table slot and locks behind, so `sdwind` won't
  shut down and `cycle.ps1` refuses to start.

- ***A VIRTUALBOX GUEST THAT FREEZES UNDER DISK LOAD IS THE HOST'S
  HYPERVISOR, NOT THE GUEST'S WORKLOAD.*** 24 Aug 2026; cost two wedged runs,
  misdiagnosed both times as the workload (a `pacman` lock, then the MSYS2
  installer). **The tell:** `VBox.log` — `HM: HMR3Init: Attempting fall back
  to NEM: AMD-V is not available` — VirtualBox is running on the Hyper-V
  platform instead of native AMD-V. **Symptom looks exactly like an app
  hang**: guest tray clock frozen, no keystrokes reach it. **Distinguish
  wedged from slow, cheaply:** differencing `.vdi` size 60s apart (0 growth
  = wedged), `VBoxManage metrics query CPU/Load/User` (steady = wedged),
  guest tray clock across two screenshots. **Clearing it needed four host
  switches, all four, each with a reboot** — Memory Integrity off, Virtual
  Machine Platform off, `bcdedit hypervisorlaunchtype off`, and the one that
  actually released it: `DeviceGuard\Scenarios\WindowsHello\Enabled = 0` in
  the registry (turning Windows Hello off in Settings does **not** clear
  this key). **Verify on the success wording**: host
  `HypervisorPresent` must read False; guest `VBox.log` must carry
  `HM: Using AMD-V implementation 2.0`. **Security note: Memory Integrity is
  a real protection and this lowers it — the owner's call, reversible, an
  agent must not make it unasked.**

- ***`icacls /inheritance:r /T` BEFORE THE GRANT EMPTIES THE PARENT, LOSES
  THE WALK, AND EXITS 0 HAVING SAID SO.*** 24 Aug 2026, cost two runs and
  nearly shipped a false product finding. A directory whose ACEs are all
  inherited gets an **empty DACL** after `/inheritance:r`, and
  owner-implicit rights cover `READ_CONTROL`/`WRITE_DAC` but **not
  `FILE_TRAVERSE`** — so `icacls` cannot descend into what it just emptied.
  It prints `Access is denied` on stderr and **exits 0** (the named item
  succeeded); children keep their stale inherited ACEs while the directory
  itself reads back clean. **Fix: grant first, strip second** — the explicit
  ACE is already in place before the inherited ones go. **The exit code is
  not the instrument** — read the output for `Access is denied` and `Failed
  processing`.

- ***ASSERT THE ACL ON WHAT ACTUALLY OPENS — FOR A DYNAMIC FILE THAT'S `%0`,
  NOT THE DIRECTORY.*** Same session. `dh_open()` opens the subfile; without
  `%0` the "file" becomes a bare directory and nothing opens at all. A
  fixture that loses its `%0` silently stops being able to deny anything,
  while the directory's DACL still looks correct.

- ***AN ACL CANNOT GATE A LocalSystem SESSION AT ALL.*** 24 Aug 2026.
  LocalSystem holds `SeBackupPrivilege`, bypassing DACLs outright — measured
  indirectly: three fixtures with different DACLs (correct, all-granted,
  all-denied) all opened, which no single token can do. **Ownership**
  survives this as the instrument, since a privilege that lets a token OPEN
  a file doesn't change whose name goes on a file it CREATES (§7 step 14).

- ***A `^\s*\d+\s+(\S+)` "session and account" PATTERN ALSO MATCHES
  `1 record(s) copied.`*** 24 Aug 2026. Parsing `WHO` that way turned two
  COPY success lines into two fake WHO reports and failed a step that had
  succeeded. **Match an account-shaped token to end of line, and do not make
  it case-insensitive** — `(?i)` lets `[A-Z]` match the `r` of `record(s)`,
  reintroducing the same bug from a new direction.

- ***NAMING A SCRIPT WITH A PATH SEPARATOR IN `stage.py` OR `sd.iss`
  SILENTLY UN-EXCLUDES IT FROM `assert-current`.*** 20 Aug 2026. `$shipsAs`
  matches `["'\/]` immediately before a name to tell a ship-list entry from
  a passing mention — and a **comment** that happens to carry a path
  separator (e.g. quoting a filename with its directory) looks exactly like
  one. Puts the file back under `assert-current`'s watch, so its next edit
  reports STALE — and if that script itself calls `assert-current` and
  refuses on non-zero, it refuses to run on the strength of its own
  newness. **Rule: name a script WITHOUT a path in `stage.py`/`sd.iss`
  comments and code alike.** Read `assert-current`'s `note:` lines — they
  print on an otherwise exit-0 run.

- ***`sdclilib.dll` BUILDS REPRODUCIBLY, `sd.exe` DOES NOT — A NO-OP REBUILD
  OF THE SERVER ALWAYS COSTS A CYCLE.*** 20 Aug 2026: `make sd` twice with
  no source change gave the DLL an identical hash and the server a
  different one. So touching anything the server links always fails
  `assert-current` Check A regardless of effect, and only an install clears
  it. **Do the rebuild before any test-only Makefile edit**, or one edit
  costs two cycles (mtime trips Check B, then running `make` trips Check A).

- ***A TIER RESULT THAT LOOKS LIKE THE SILENT FULL-VOC FAILURE IS MORE
  LIKELY A BROKEN ACCOUNT NAME.*** 19 Aug 2026. `verify-tiers.ps1` reported
  0 of 18 capabilities withheld in a STANDARD account — looked exactly like
  the dangerous "filter did nothing" failure §5.12 warns about. **It
  wasn't** — `CREATE.ACCOUNT` had silently failed and every session was
  still in SDSYS. **Check the account was created before reading any tier
  number** — a count equal to `voc_template`'s own record count means
  SDSYS. **Cause: PowerShell splatting.** `& $path @($s.Args)` is an array
  **subexpression**, not splatting — it stringifies the whole array as one
  argument. `& $p @a` (array) binds positionally; only `& $p @h`
  (hashtable) binds by name. **Splat a hashtable or pass parameters
  literally.**

- ***A CHECK THAT CANNOT FAIL IS WORSE THAN NO CHECK.*** 19 Aug 2026.
  `if ($out -notmatch $t.Name) { exit 2 }` passed because **SD echoes the
  command it was given**, so the account name is in the output whether
  `CREATE.ACCOUNT` succeeded or refused. **Assert the effect** (the
  `accounts\<NAME>` record exists), not the transcript — anything that greps
  SD's output for a string the input also contains is measuring the echo.

- ***AN ELEVATED SCRIPT WITHOUT A TRANSCRIPT REPORTS NOTHING.*** 19 Aug
  2026 — the elevated window's output never pastes back into the session
  that asked for it. `verify-createaccount.ps1` was the only verifier
  without `Start-Transcript`, exited 2 in under a second, and left no
  record. Fixed, closed in a `finally` so every exit path releases it (a
  transcript left running swallows the *next* verifier's output).

- ***`CT` AND `LIST` DISAGREED ABOUT THE SAME RECORD ID.*** 18 Aug 2026,
  found and fixed the same day. `CT` folds the record id it matched and
  echoes what it matched, not what was typed; `QPROC`'s `LIST` reads the id
  **exactly**, no fold — so a rename shipped a live regression the same
  session it was made, and `CT`/`COUNT` (both folding) could not have shown
  it. **After any rename, test every verb that NAMES the thing, not one of
  them** — the folding ones all pass together and say nothing about the
  ones that don't.

- ***`BASIC bp X` CREATES A `bp.OUT` THAT NOTHING CAN EVER OPEN AGAIN.***
  18 Aug 2026. `BASIC` builds the object name from the source name **as
  typed** (`bp` → `bp.OUT`), then `CREATE.FILE` writes the VOC id as typed
  but the directory **upper-cased** (`BP.OUT`) — mixed case, which the
  three-case fold (as-typed/lower/upper) can never match. **Permanent**
  until `DELETE.FILE bp.OUT FORCE` (needed because `DELETEF` prompts
  separately for DATA/DICT whenever the stored path differs from the
  default). Appeared only once 5.12(a) made the per-account file `bp` —
  before that everyone typed `BP` and the spellings agreed.

- ***`assert-current` CHECK A2 TURNED `make check-local` INTO A PERMANENT
  FALSE STALE.*** 18 Aug 2026, fixed same day. A2 flags anything under
  `gplsrc` newer than the oldest `bin\` binary and hadn't inherited Check
  B's `localtest\`/`__pycache__` exclusion — `make check-local` builds a
  test binary there, so every later `assert-current` said STALE forever
  (reinstalling doesn't help; the next `check-local` recreates the file).
  Both exclusions are now in both checks.

- ***ORDER: EXEMPT FIXES FIRST, THEN RE-MEASURE, THEN TOUCH `sdsys`.***
  18 Aug 2026, cost a cycle. A verify script is `assert-current`-exempt and
  cannot make an install stale; a shipped `sdsys` file can. Fixing both in
  one commit voids the install being measured for the sake of the half that
  didn't need to. (The changelog, the commonest offender here, has been
  exempt since 21 Aug 2026 — every other shipped `sdsys` file still voids.)

- ***`cycle.ps1` DOES NOT RUN `make` — A C CHANGE CAN BE CYCLED, INSTALLED,
  TESTED AND PASSED WITHOUT EVER BEING COMPILED.*** 18 Aug 2026, cost a
  cycle. `cycle.ps1` stages whatever is already in `bin\`; `make sd` is
  separate. ***Correction, owner, 3 Sep 2026: step 2 (`stage.py
  --bootstrap`) DOES compile the BASIC half — that's most changes on this
  project — so only the C half is the gap.*** `stage.py` checks the
  binaries are PRESENT, not CURRENT. Both `assert-current` checks can pass
  over a stale binary in the specific case where the change is a relative
  path literal NTFS matches either way (`$HOLD`→`$hold`) — Check A2 (newest
  source vs. oldest `bin\` binary) is what actually catches a stale C build;
  the `sd.exe` hash moving is the tell if ever in doubt.

- ***A CONFIRMING VERB EATS THE NEXT PIPED LINE AS ITS ANSWER, AND SPINS
  FOREVER IF THE PIPE RUNS OUT WHILE STILL ASKING.*** 18 Aug 2026. A prompt
  consumes **the next line in the pipe**, whatever it was meant to be — so
  `DELETE.FILE x` followed by `OFF` feeds `OFF` to the prompt and the
  intended command is gone; the answer being neither Y nor N, it re-asks on
  EOF without end. **Supply every answer, in order, before the next
  command** — `DELETE.FILE` asks twice (DATA then DICT); surplus `Y`
  answers are harmless. **Give background output time before concluding a
  hang** — three `sd.exe` were killed live by sampling output too early.
  Kill by `ParentProcessId` if needed (the service is session 0). A BASIC
  program (`OPEN`/`DELETE`) needs no prompt handling at all for a record
  delete.

- ***POWERSHELL'S `-match` IS CASE INSENSITIVE, SO A SUCCESS TEST CAN MATCH
  THE FAILURE LINE.*** 21 Aug 2026, caught before it cost a run.
  `remote_connect_test.c` prints `admitted` on success and **`ADMITTED`** on
  two *failure* paths — `$out -match 'admitted'` scores both true. **Use
  `-ceq`/`-cmatch`** (the `c`-prefixed operators are case sensitive; none is
  the default). Fifth instrument in this file found wrong this way.

- ***`` `e `` IS NOT AN ESCAPE IN WINDOWS POWERSHELL 5.1, SO EVERY ANSI
  STRIP USING IT IS DEAD CODE.*** 18 Aug 2026. ``e` `` arrived in PowerShell
  6; the literal letter `e` matches nothing SD emits. **Use `[char]27`.**
  Some scripts still carry the dead form and have never been hurt by it
  only because they match substrings no escape sequence sits inside.

- ***`struct PCFG` IS IN THE SHARED SEGMENT DESPITE ITS HEADER COMMENT, AND
  `SYSSEG_REVSTAMP` WILL NOT CATCH A CHANGE TO IT.*** 16 Aug 2026. Every
  attaching session `memcpy`s the whole struct from the segment; the only
  compatibility check is the release-number revstamp, and two builds of the
  same release are not required to share a `PCFG` layout. **The failure is
  silent and looks like a PowerShell bug** (fields after the change come
  out shifted). A full install cycle replaces every binary at once and is
  what makes it safe — never copy a freshly built `sd.exe` over an installed
  one while SD is running after touching `config.h`.

- ***`read_config()` RUNS ONLY WHEN THE SEGMENT IS CREATED — A
  CONFIGURATION CHANGE CANNOT BE TESTED FROM AN ORDINARY SESSION.*** Same
  session. An attaching session takes `pcfg` from the segment and never
  opens the file; `sd --version` returns even earlier. Three tests of a
  parser change were blind, controls included. **The only route in is
  `sd -start`** (elevated, service stopped) with `SD_CONFIG` naming the
  file under test.

- ***A STAGE WHOSE BOOTSTRAP DIED AFTER THE SEED PHASE PACKAGES AND
  INSTALLS IN SILENCE.*** 16 Aug 2026, cost a whole session's SD-side
  results. `assert-current` is blind to it by construction (compares
  install against source; `gcat`/`GPL.BP.OUT` are build products with no
  source counterpart). Symptom on the installed system: every `sd`
  invocation dies loading `$CPROC`, `0xC0000005` — reads as a corrupt
  binary, is a missing catalogue. **One-second check:**
  `(Get-Item '...\gcat\$CPROC').Length` — never 0. **Enforced now, not
  remembered:** `stage.py`'s `check_bootstrap_complete()` judges the tree on
  five such facts, not the exit code, and refuses to stage a failed one.

- ***`/dev/shm` IS A REAL DIRECTORY HERE, SO POSIX SHARED MEMORY OUTLIVES
  THE MACHINE.*** 16 Aug 2026. `etc/fstab` binds it to NTFS storage (Program
  Files is read-only to ordinary users), so **"a segment exists → a system
  that might be live" is wrong on this port** unlike Linux tmpfs. Broke the
  service across a restart: an unclean `sd -stop` left the segment, it
  survived reboot, and `sd -start` refused it as `SD_WRECKAGE` forever
  after. **Fixed** — `sd_state()` downgrades `SD_WRECKAGE` to `SD_STOPPED`
  for a segment whose mtime predates boot. Win32 semaphores are **not**
  affected (kernel objects, do vanish), so the two now behave differently
  across a reboot.

- ***A NON-CRASHING SERVICE NEVER GETS ITS RECOVERY ACTIONS.*** 16 Aug
  2026. `sc failure` actions are ignored unless the process **crashes**; a
  service that exits `SERVICE_STOPPED` with an error code needs
  `sc failureflag <name> 1` too. Had never fired. Cuts both ways: had it
  fired, the retry would have found a freshly cleaned `shm` and hidden the
  bug above.

- ***A LINE OF `sd.iss` STARTING WITH `#13#10` IS READ AS A PREPROCESSOR
  DIRECTIVE.*** 16 Aug 2026. ISPP treats any line whose first non-blank
  character is `#` as a directive; mid-line `#13#10` is fine. **Keep
  `#13#10` off the start of a line.**

- ***THE CLAUDE CODE `Bash` TOOL IS NOT MSYS2, AND `make ... | tail`
  REPORTS EXIT 0 HAVING BUILT NOTHING.*** 16 Aug 2026. `make` isn't on that
  shell's PATH; `make: command not found` on stdout, piped through `tail`,
  reports `tail`'s exit code. **Build through
  `C:\msys64\usr\bin\bash.exe -lc "make -C <abs path> sd"`** and read the
  linker lines, not the exit code.

- ***`cygwin_attach_handle_to_fd()` GIVES A DESCRIPTOR `select()` CALLS
  PERMANENTLY READY, DEFEATING SD's INPUT LAYER.*** 17 Aug 2026, §7 step 11.
  A descriptor from a raw Windows HANDLE has no real `select` support in
  Cygwin — `sel.always_ready 1` forever, so SD spins reading one byte at a
  time and never frames a packet. Symptom: `sd.exe` alive, silent, high
  CPU, client waits forever. **The access argument must match how the
  HANDLE was opened** — `GENERIC_READ|GENERIC_WRITE` open with a
  `GENERIC_READ`-only attach succeeds the attach and fails `read()` with
  `EBADF`.

- ***THERE ARE TWO "INTERNAL"S AND THEY ARE NOT THE SAME FLAG.*** 17 Aug
  2026, caught before a commit. `$internal` in a header is `HDR_INTERNAL`,
  a property of the PROGRAM (gates `KERNEL`). `K$INTERNAL` reads
  `internal_mode`, a property of the SESSION, set only by `sd -internal`/
  `-I` (already behind `check_admin()`). **A program can be `$internal` in
  a session that is not `internal_mode`** — `APISRVR` is exactly that.
  Reading the header flag as the session one makes a permanently-shut gate
  look permanently open.

- ***AN ORDINARY SD SESSION CANNOT BE READ WITHOUT A CONSOLE, AND THREE
  WRONG WAYS EACH FAIL DIFFERENTLY.*** 17 Aug 2026. `sd WHO` unelevated is
  refused **by design**, not a defect (owner's rule: a command is a
  parameter too). The installed `sd.exe` launched from an MSYS2 shell (not
  a native one) answers "SD has not been started" while running fine — two
  Cygwin universes, launch from a native shell instead. Launched natively
  with stdin/stdout redirected, it blocks in terminal setup and writes
  nothing (the `termios`→Console API attempt was reverted, §7 step 13, and
  stays that way on purpose). **A `WHO` measurement needs a person at a
  terminal.** What CAN be read without one: `adopt-account.log`.

- ***ENABLING REMOTE DESKTOP DOES NOTHING UNTIL THE MACHINE REBOOTS, AND
  THE SETTINGS TOGGLE REPORTS SUCCESS EITHER WAY.*** 15 Aug 2026.
  `TermService` creates its listener only at service start and cannot be
  restarted while running — flipping RDP on under a running service leaves
  it off until a reboot, while the registry, service state and UI toggle
  all read correct. **`netstat -an | findstr 3389` is the only honest
  check.** Costs three rounds of unrelated firewall changes if missed
  (guest network classified Public also genuinely blocks RDP — a plausible
  wrong answer sitting in the way).

- ***`mstsc` PREFILLS THE USERNAME FROM THE HOST, RUINING AN RDP
  CONTROL/TREATMENT TEST SILENTLY.*** Same session. Qualify the account
  explicitly (`GUEST\account`, "Use a different account"), leave "Remember
  me" unticked. A wrong-account credential error reads much like a
  deny-rights refusal; only the wording tells them apart.

- ***A TEST THAT CAPTURES ONLY stdout SEES SD's REFUSALS AS SILENCE.***
  15 Aug 2026. `SH sd --version` piped gave no output at all — it had run
  and refused, on stderr. **A gate under test is exactly the output most
  likely to be on stderr.** Use `OS.EXECUTE ... CAPTURING` (dup2s both
  streams), or redirect stderr to a **file**, never `2>&1` (below).

- ***IN POWERSHELL 5.1, `native.exe 2>&1` TURNS EVERY STDERR LINE INTO A
  TERMINATING ERROR UNDER `$ErrorActionPreference = 'Stop'`.*** 14 Aug 2026.
  PowerShell wraps native stderr in `ErrorRecord`s; under `Stop` that
  throws — **including on success**: `ssh`'s own "Warning: Permanently
  added..." after a working login scored `verify-sshonly.ps1` a hard
  failure. **Never redirect native stderr inline** — `Start-Process` to
  separate files and read `.ExitCode`; feed stdin from an empty file too,
  so a surprise prompt gets EOF instead of hanging.

- ***`sshd -d` STARTED FROM AN ELEVATED ADMINISTRATOR PROMPT CANNOT
  AUTHENTICATE ANY ACCOUNT.*** sshd must run as **SYSTEM** to build a user
  token; elevation is not enough and there is no flag for it — it fails
  before authentication is even attempted, reading exactly like total auth
  failure. **Read the installed service's own event log instead**
  (`OpenSSH/Operational`), which distinguishes failed password / accepted /
  not-allowed at the default level.

- **Do not make a person retype a random password into a test.** 14 Aug
  2026. A 36-char ambiguous-glyph password typed by hand three times logged
  three false `Failed password` entries pointing at a nonexistent design
  problem. `SSH_ASKPASS`/`SSH_ASKPASS_REQUIRE=force` automates it; pass the
  secret via an environment variable, clear it in `finally`; generate any
  human-typed password from an unambiguous alphabet.

- ***IN AN INNO `[Run]` PARAMETER, `{{` ESCAPES A LITERAL `{` BUT `}` MUST
  BE WRITTEN SINGLY — `}}` GIVES YOU TWO.*** 14 Aug 2026. `try {{ ... }}
  catch {{ exit 1 }}` expanded to doubled closing braces and PowerShell
  refused to parse it — **silently**, since the step has
  `skipifdoesntexist` by design (§5.9). **Check the install LOG's
  `Parameters:` line (post-expansion), not the `.iss`**; or parse-check any
  generated PowerShell without running it
  (`[Parser]::ParseInput`). Distinct from the next trap; they share only the
  character.

- **A brace comment in an Inno `[Code]` section cannot mention a
  brace-delimited constant.** `{ ... {app} ... }` ends at the FIRST closing
  brace; everything after parses as code, with the error pointing at prose
  several lines away. Use `(* ... *)`, and don't write `(*`/`*)` inside that
  either. Cost two compile failures 14 Aug 2026, hit twice the same day.

- **An installer edit to a file SD does not own must be an exact inverse.**
  `allow-ssh-groups.ps1` left a trailing blank line outside its own fence,
  so every apply/remove cycle grew `sshd_config` by one line forever. Found
  by a test that applies-then-removes repeatedly and diffs against the
  original **byte for byte** — "it removed the line" is not the check,
  "the file is the file it was" is.

- **A test for a config edit does not need the real config.**
  `sshd_config_default` (the world-readable template `sshd` copies on first
  start) makes the whole of `AllowGroups`' file handling testable
  unelevated, with no `sshd` running at all.

- **The `<sysdir>/bin` split left two C call sites pointing at the old
  location, both failing silently.** 14 Aug 2026, fixed, kept for the
  shape. `sysseg.c`'s daemon exec and `check_lost_users()`'s cleanup exec
  both built paths assuming executables and the pcode library shared one
  directory (true only in development); the daemon simply never started, no
  message, `sd -start` still reported success (`sdwind_pid` stayed -1,
  which also happens to be "never started", so even that looked normal).
  **Grep the C for the old location whenever a path splits between dev and
  installed trees** (the compiler can't help — these are runtime strings).
  **A forked child that fails must `_exit()`, not `return`** — returning put
  it back in the caller's code as a duplicate process.

- **`Test-Path` says True for a directory you cannot read.** It asks about
  the *parent's* listability, not the target's readability. **Check the
  contents** (`Get-ChildItem`/`icacls`, which fail honestly) to test an ACL.

- **The ACL lockout's symptom is "Error 13 allocating semaphores", which
  names nothing useful.** Windows fixes group membership in the token at
  **logon** — the installing user is added to `sdusers` but can't use it
  until sign-out/in, and `/dev/shm` (mapped under the locked tree) is the
  first thing to fail. The installer says so in a dialog for exactly this
  reason.

- **`/SUPPRESSMSGBOXES` does not suppress `MsgBox` calls from `[Code]`.**
  14 Aug 2026; an unattended `/VERYSILENT` install still hung on an OK
  click. **Check `WizardSilent`/`UninstallSilent`, not the switch** — and
  check them in `CurPageChanged` too (still fires in silent mode, form just
  isn't shown) — corrected 18 Aug 2026 after a `-Silent` cycle hung there.

- **The UCRT64 compiler needs its own `bin` on PATH even invoked by
  absolute path — and fails with NO message at all.** `gcc.exe` finds its
  own DLLs; the `cc1.exe` it spawns does not, and a plain
  `int main(void){return 0;}` exits 1 with empty stdout/stderr. Fixed at
  source in the Makefile and in both of `sdclilib`'s other two build routes
  (`make` from inside the directory, `build.cmd`), derived from `$(CC)`/
  `%GCC%` so overriding the compiler moves it too.

- **`NoDefaultCurrentDirectoryInExePath` blocks `cmd` from running an exe
  in the current directory** — reads as a build failure, is a lookup rule.
  Use `.\`.

- **`make sd` lists `sdclilib` as a prerequisite — a client build failure
  silently leaves `sd.exe` unrelinked**, and testing continues against the
  old binary. **Check `bin/sd.exe`'s timestamp after any build failure.**

- **`sd -stop` used to kill its own caller and its whole process group.**
  `stop_sd()` guarded only on `uptr->uid`; `kill(0,...)` or a negative pid
  signals the whole **group**, and an unfilled or half-dead user-table entry
  produced one. Fixed — test is `uptr->pid > 0`. **Never pass an unvalidated
  pid to `kill()`.**

- **An over-long `SH`/`SH1` in `sd.conf` silently corrupted the parameters
  after them.** `strcpy` into `char[80]`; a 93-char PowerShell path
  overran into `sortmem`/`sortmrg`, and SD refused to start naming a
  parameter the file didn't even contain. Fixed: 255-byte buffer,
  length-checked. Other `strcpy`s in that parser share the shape and are
  unaudited.

- **`config.c` stripped `\n` but not `\r`, so a CRLF `sd.conf` corrupted
  every string parameter** (numeric ones were fine — `sscanf` stops at
  `\r`, which hid it as a path bug). Only ever hit the shipped config (LF
  by hand, CRLF from `stage.py`/Notepad). Fixed.

- **`ACCOUNTS` is a directory-type file — its records are text files whose
  field marks are NEWLINES, not `\xfe`.** Splitting on the DH-file field
  mark finds nothing and flattens the record. **Check the file type before
  assuming a delimiter.**

- **`OS.EXECUTE` ran `/bin/bash -c` on a runtime that ships no bash.**
  14 Aug 2026, true of *every* `OS.EXECUTE`, not just the account commands
  that exposed it — worked in development (MSYS2's own bash present),
  would have failed silently on every installed system. **Fixed by pointing
  `SH`/`SH1` at PowerShell** (owner's instruction) — the five OS-facing
  programs are PowerShell already, and it removes a quoting layer. Path
  must contain **no spaces** (`clparse()` splits on them, ignores quotes).

- **MSYS2 declares System V IPC but does not implement it** — headers
  compile and link, `shmget`/`semget` return ENOSYS at runtime, no
  `cygserver`. Test primitives by *running* them.

- **The Makefile does not track header dependencies.** Editing `opcodes.h`
  left `kernel.o` stale and the link failed pointing at an unedited file.
  `rm -f gplobj/*.o` after touching any header.

- **Retire an opcode in place; never delete the line** — `opcodes.h` is
  positional and removing an entry renumbers everything after it,
  invalidating all compiled pcode. Point the slot at `op_illegal` instead
  (`OP_09`, `OP_9E`, `OP_BB`, `OP_CFFE`). **The BASIC side must move with
  it** — `BCOMP`'s intrinsics table and its `on i goto` dispatch are matched
  by **position**.

- **`make` must run from `sd64`** (`MAIN := $(shell pwd)/`). **Link order
  matters** — PE/COFF resolves strictly left to right; libraries must
  follow the objects that use them (ELF's `--no-as-needed` masked this and
  is gone). **`.PHONY` is required for `sdclilib` and `terminfo`** — neither
  names a file and `VPATH` covers `gplsrc`, so make finds the directories
  and calls the target already satisfied.

- **Do not let the client's headers displace the server's** (`revstamp.h`,
  §5.2). **`O_BINARY`/`O_TEXT`** — both hardcoded to zero in two files,
  correct on Linux, now `#ifndef`-guarded (matters for a future native CRT,
  not MSYS2 today).

- **`ssh -T git@github.com` hangs non-interactively on the first
  connection.** Use `-o BatchMode=yes -o StrictHostKeyChecking=accept-new`.
  **Rebuild from clean when switching toolchains** — stale objects from
  another compiler link into nonsense (`rm -f gplobj/*.o`).

- **`@ds` is load-bearing for compilation** — `BCOMP`/`BASIC` build source
  paths with it; SYSCOM slot 57, `CPROC` hardcodes it to `'/'`, correct on
  MSYS2. If compilation starts failing on path resolution, look here first.

- **`whoami /groups` lists `Administrators` in a session that cannot use
  it** — an unelevated administrator's token carries it "Group used for deny
  only". Read the qualifier, not just the group name — misreading this once
  sent the port down the account-password route in §5.6 before §5.6.1
  corrected it. **Before concluding a platform lacks a capability, find
  where that platform puts it.**

- **Adding yourself to a Windows group does not take effect in the session
  you add it from** — fixed in the access token at logon. **Sign out and
  back in, or reboot.**

- **To see what an ordinary user sees, build a probe with a gid nobody
  holds** (`SD_ADMIN_GID`, `#ifndef`-guarded) — rebuild **both** `sd.c` and
  `linuxlb.c` (the latter holds `IsAdmin()`); build the object list from
  `gpl.src`, not `gplobj/*.o` (which has multiple `main`s).

- **A second `msys-2.0.dll` earlier on PATH makes SD lie about being
  started** — "SD has not been started" while the server runs fine. Git for
  Windows ships its own MSYS2 runtime and is on nearly every developer
  machine. The runtime's POSIX root follows the DLL that loaded it. Ship the
  DLLs beside `sd.exe` (Windows searches the exe's own directory first);
  never rely on PATH order.

- **Shipping `msys-2.0.dll` beside `sd.exe` moves the whole POSIX
  namespace — strip exactly TWO path components to find `/`.** Measured:
  `<X>\SD\usr\bin\` → `/` is `<X>\SD\`; one level off in either direction
  moves `/dev/shm` and every POSIX call with it. `C:\Program Files\SD\usr\bin\`
  is the placement that lands `/` on `C:\Program Files\SD\`. `/dev/shm`
  then has to be bound back out to writable space via `etc\fstab`
  (`C:/ProgramData/SD/shm /dev/shm ntfs binary 0 0`), since Program Files is
  read-only to ordinary users.

- **Running `sd.exe` outside the MSYS2 shell needs TWO directories on
  PATH** — the runtime, and `usr\local\bin` for `libsodium-26.dll` (built
  from source into `/usr/local`). Missing either: exit 53, **no message at
  all** (the loader fails before `main`).

- **`sd -A` with no account name does nothing** — `CMD_QUERY_ACCOUNT` is set
  and read by nothing. Either wire it up or drop it.

- **Case inversion makes the account prompt echo in lower case**
  (`PT$INVERT`) — cosmetic only, `LOGIN` upcases the real answer, but reads
  like input corruption. Same mechanism as the password trap below, which is
  not cosmetic at all.

- **Editing BASIC source changes nothing on its own — there are two
  copies.** A repository edit must be copied to `<sysdir>/GPL.BP/` and
  compiled before it has any effect; forgetting the copy is a silent no-op.

- **Privilege tests do not fail, they answer wrongly** — `IsAdmin()`/
  `SYSTEM(27)` under MSYS2 never see uid 0, so a branch always takes one
  side and the symptom is a permission complaint from code that looks
  correct (§5.5).

- **FIXED 14 Aug 2026, kept for the diagnosis: `IS_GRP_MEMBER` read
  `/etc/group` as a text file, which MSYS2/Cygwin do not have** — set
  status 1 and answered false for everyone, refusing every login with "not
  registered for SD use". Not the same as the `getgrnam()` NSS path, which
  works. Fixed by asking `Get-LocalGroupMember`. **Three helpers shared this
  defect and only one was caught with it** — `!is_user`/`!is_group` had the
  identical shape and were found a session later, each looking like a
  different bug entirely (`DELETE.ACCOUNT` silently orphaning `sdu_`
  groups; `CREATEA` misreporting a refusal as "OS Error: 1"). **When a fix
  makes a helper answer correctly, check what its callers were relying on
  it getting wrong** — repairing `!is_user` alone would have turned a
  correct refusal into a silent adoption of somebody's existing Windows
  login; caught before shipping.

- **The API's two security mechanisms both break, in opposite directions.**
  `APILOGIN=1` (shipped default) reads `/etc/shadow`, which doesn't exist —
  fails closed, API unusable. `APILOGIN=0` trusts `getpeereid()` on
  AF_UNIX, which MSYS2 emulates over a TCP loopback socket with a handshake
  file — not a filesystem object with permissions, so "local socket" is a
  far weaker statement than on Linux. **The Windows equivalent of
  `SO_PEERCRED` is a named pipe with `GetNamedPipeClientProcessId`** and a
  security descriptor you control (`connection_type` already has `CN_PIPE`).

- **`chmod` is a no-op on the MSYS2 runtime — the mount is `noacl`.** Real
  permissions stay whatever was inherited. Use `icacls`,
  `/inheritance:r` first (§5.7). ACL *inheritance* itself is unaffected by
  `noacl` and does work.

- **The two configuration paths are duplicated in two toolchains**
  (`sddefs.h` and `sdclilib.c`, §5.2) — change one without the other and
  the client silently looks somewhere else.

- **`sd -start` looks like it hangs, but it has succeeded — `sdwind`
  inherits stdout/stderr, and anything that waits on those streams (a
  pipe, `Start-Process -Wait` with redirection, the Inno installer's own
  `[Code]` step) blocks on the *daemon*, which never exits, not on
  `sd -start` itself, which already has.** Check `Get-Process sdwind`
  rather than waiting. **The remedy that actually works: start it, then
  poll for the daemon process** — never wait on the launcher's own process
  handle, and never look **once** (an idle machine always wins the race, a
  loaded one loses it — cost an install with a race that gave the
  installing user no SD account and just `code 3`). Interrupting a wait
  leaves the daemon holding the script's redirected scratch files, which
  then fail the *next* run with a misleading "file in use".

- **A PowerShell pipeline puts a phantom empty line after every command,
  and an `input` statement eats it.** PowerShell writes CRLF between
  pipeline objects and SD treats CR and LF **each** as a line terminator, so
  `@('A','B') | sd.exe` arrives as `A`, empty, `B`, empty — invisible at the
  `:` prompt (an empty command just reprints), **fatal at an `input`
  statement**. Cost `verify-createaccount.ps1` a silently-disabled account
  (the phantom ate the password, the real password went to the confirm
  prompt, and the retry prompt got the next phantom instead of `Y`) with the
  only visible symptom a stray stderr line. **Fix: send one joined string
  with LF separators, with a leading blank line to also absorb the pipe's
  BOM** (below), not an array. Don't try to verify by reading the echo back
  — SD's erase sequences can render one line twice or truncate a copy.

- **Scripting SD from PowerShell: input must be a real PIPE (`<` redirect
  stops dead after the password prompt), and the pipe prepends a UTF-8 BOM
  to the first line** (`$OutputEncoding` does not fix it). **Send a blank
  sacrificial first line** — the BOM lands on it, SD complains about an
  empty command, and the real commands run untouched.

- ***THERE IS AN UPGRADE PATH*** (built 25 Aug 2026, owner: *"preserve the
  user's own files, replace all the shipped ones"*) — `sd.iss:1044`:
  `upgrade.iss` is gated on `DataTreeAbsent`'s opposite; one or the other
  fires on every install, never both, never neither. **On an upgrade,
  `gpl.bp`, `gpl.bp.out`, `messages`, `newvoc`, `voc_template` ARE
  replaced**; `$cred`, `accounts`, `cat`, `os.users`, `batch.jobs`, `prt`,
  `$hold`, `bp`/`bp.out` are preserved; `sd.conf` is never rewritten
  (`onlyifdoesntexist`). **What still does not update: any LIVE VOC,
  SDSYS's own included** — they're built from those templates and nothing
  re-runs `UPDATE.ACCOUNT` (PRE_RELEASE 70), so no existing account gains a
  verb an upgrade adds. **The cycle rule (fresh install, every time) still
  stands, but now rests on "date what you are testing", not "the tree can
  never move".** Before trusting any result from `C:\Program Files\SD`,
  date it — `LastWriteTime` against `git log` for the binary,
  `Test-Path '...\MESSAGES\10034'`-style probe for whether the data tree
  has caught up. **`assert-current.ps1` is the real instrument** — compares
  source mtimes against the install across six mirrored directories.

- **`sd -stop` leaves `sdwind` running when the stopping session is less
  elevated than the starting one — it now SAYS so, it still cannot stop
  it.** An unelevated process may not signal an elevated one. **Kill it by
  Windows pid** (translated, see below) from an elevated window; a second
  `sd -stop` cannot help, because the segment holding `sdwind_pid` is
  already gone. **Watch for two live daemons** — starting SD again creates a
  fresh segment while the orphan keeps running against the unlinked one.
  **And separately: if the segment is ALREADY gone when `sd -stop` runs, it
  reports success with the daemon still alive and there is nothing left to
  signal or detect** — not fixable the way the above is; the eventual
  answer is a pid file beside the segment, not a field inside it.

- **SD prints MSYS2 process ids, and Windows has never heard of them.**
  `getpid()` under MSYS2 uses the runtime's own numbering (measured: daemon
  called itself 87, `Get-Process` called it 14712) — every pid SD holds
  (user table, `sysdump`, warnings) is this kind. `Stop-Process -Id 87`
  silently acts on an unrelated Windows process. **Translate with
  `cygwin_internal(CW_CYGWIN_PID_TO_WINPID, pid)`** (`sysseg.c`'s
  `win_pid()`); it returns 0 when it cannot translate, so callers can print
  no number rather than a wrong one. `sysdump.c` still prints untranslated.

- **A piped SD session cannot answer "Press RETURN to continue", so any
  `LIST` that outgrows one page hangs forever.** Grew silently from green to
  hung as a register grew past four rows, no code change. **Append
  `NO.PAGE` to every scripted `LIST`.** A stuck `sd.exe` started by an
  elevated session refuses an unelevated `Stop-Process` — kill it from the
  window that started it.

- **Anything `LOGIN` calls becomes a bootstrap dependency**, because
  `SECOND.COMPILE` logs in. Restoring the `sdusers` gate made the bootstrap
  die on a missing `!VALID_OS_NAME` before compiling anything. **If you add
  a call to `LOGIN`/`CPROC`, add its whole call chain to `BBPROC`'s pass-1
  list.** (And the same change made the bootstrap need `sdusers`, which
  only the installer creates — resolved by exempting internal mode from the
  gate, since `-INTERNAL` already requires elevation, §5.6.)

- **`IS_INSTALL` is still defined on every installed system**, so every
  `$ifndef IS_INSTALL` block in `CPROC` compiles out there despite a header
  comment promising the install strips it — it never did. Dead twice over
  (preprocessor here, platform anyway — `!EUID_SET` has no Windows
  equivalent, §5.5). **A comment describing what the install *will* do is
  not evidence that it does** — third time this file has recorded that
  shape.

- **`gplbld/bbcmp.py` cannot compile `LOGIN`** ("VOID statement not
  coded", reproduced against unmodified HEAD as a control) — it builds only
  the bootstrap seed; SD's own `BCOMP` compiles the rest. **A change to
  `LOGIN`/`CPROC` cannot be syntax-checked without a working installed
  system.**

- **`IS_GRP_MEMBER` reading `/etc/passwd`/`/etc/group` directly (not
  through NSS) is a family, not a one-off** — see above; `grep -rn
  'openpath "/etc"' GPL.BP` after both fixes found no more.

- **A blank `Path` from `Get-Process` does not mean "elevated"** — a
  correlation over four samples, not a check; a fifth daemon had a blank
  `Path` *and* granted `OpenProcess(PROCESS_TERMINATE)` to an ordinary
  session, which an elevated process cannot do. **Ask for the right you
  care about directly**
  (`OpenProcess(PROCESS_TERMINATE)`, `IntPtr.Zero` = refused), not a field
  that merely correlates with it.

- **`OpenProcess(PROCESS_TERMINATE)` returning a handle does not mean you
  can terminate** — it returned one for a High-integrity `sdwind` from
  Medium integrity, and `Stop-Process` on the same pid seconds later was
  refused. **Trust the operation, not the probe.**

- **A yes/no prompt with no input spins forever at full CPU**, not idle —
  half a megabyte of repeated prompt in two minutes, and killing it left
  record locks behind (below). Applies to **any** confirmation prompt a
  script can reach. If something hangs at 100% CPU rather than idling, look
  for a prompt, not a lock.

- **Drive a scripted SD session through a pipe, not a `<` redirect** —
  `< commands` stops dead after the password prompt, exit 0, as though
  closed cleanly. **And pipe from an MSYS2 shell, not a Windows one** — both
  Windows shells corrupt the first (password) line: PowerShell 5.1 adds a
  3-byte BOM, `cmd.exe` adds a phantom empty line that eats a retry.
  Measured by counting the echoed asterisks. Reads as "Invalid
  username/password" and sends you looking in the wrong place.

- **`OSPATH()` is only available to `$internal` programs** — in an
  ordinary one the compiler takes it for an unassigned matrix, not
  "unknown function". **`KERNEL` is the same shape** — use
  `SYSTEM(1050)` for the administrator flag without the restriction.
  **`$internal` itself is only accepted under `sd -internal`** — the
  resulting errors point at the internal-only statements below the
  directive, not at the directive itself, several lines above the first
  complaint.

- **`$catalog NAME` in source catalogues *privately*** — invisible from
  every other account until `CATALOG BP NAME GLOBAL` or a `$`/`!`/`*`
  prefix.

- **`fullpath()` ignores the failure it is told about.** `open_file()`
  calls it without checking the result, so an unresolvable path produces an
  arbitrary string and the later `stat()` reports "file not found" about
  something nobody passed in — what made the drive-letter problem (§5.8) so
  hard to see. Resolver now accepts drive letters; the swallowed return
  value is still there.

- **Killing an SD process leaves its record locks behind — the next run
  waits on them forever, with no timeout and almost no CPU, reading exactly
  like a deadlock.** The lock table lives in the shared segment. `sd -stop`
  then `sd -start` clears it (segment unlinked and recreated). Semaphores
  are *not* involved (all read 1 while this happens) — diagnose with
  `strace`, which shows the path being re-stat'ed every 250ms.

- **`sd -SUSPEND` is sticky and survives the process** (`SSF_SUSPEND` in
  the shared segment) — every later invocation refuses with no hint why.
  `sd -RESUME` clears it. Neither call checks `check_admin()`, so any user
  can suspend a running system — worth revisiting under §5.6.

- **Grep the BASIC case-insensitively.** Free-form source is inconsistent
  about case; a case-sensitive sweep for `system(27)` missed the one
  spelled `SYSTEM(27)` and the survivor stopped the bootstrap two steps
  later.

- **`pterm(PT$INVERT, @true)` silently upcases input, including
  passwords.** `hunter2` arrives as `HUNTER2` — verifies fine typed by
  hand, fails at login with nothing visibly wrong (record found, salt/key
  right lengths, status 0). **Save/clear `PT$INVERT` around any password
  read and restore it after.** Would otherwise have shipped.

- **`WRITE ... THEN` is not valid** — bare `write`, or
  `write rec to file, id on error ... end`. The unmatched `end` throws
  every subsequent error off by one, pointing far from the real line.

- **`<sysdir>/bin` is two unrelated things sharing one directory** — the
  installed executables, and the SD pcode composite library `BCOMP` reads
  as `@sdsys:@ds:'bin'` for recursive compilation. When the binaries moved
  to `C:\Program Files\SD\` (§5.8), the pcode library had to stay behind
  with SDSYS (it's data, addressed relative to `@sdsys`) — moving the whole
  directory breaks recursive compilation at a distance, silently.

- **`SECOND.COMPILE` aborting at APISRVR with "Cannot open gplsrc
  revstamp.h" is not a missing directory — it's two compile-time
  `$execute`/`$include` lines in `APISRVR` that run `REVSTAMP` against a
  relative `./gplsrc` path that doesn't exist outside development.** Both
  commented out; `gen_includes.py` does the translation at build time
  instead. **A second, more dangerous instance: `ERRTEXT` running `ERRGEN`,
  which `weofseq`-truncates `SYSCOM/ERR.H` and `ERRTEXT.H` *before* opening
  its own input** — so a missing `gplsrc` destroys both files and then
  aborts, leaving `ERR.H` at zero bytes. **An undefined `$define` in SD is
  NOT a compile error** — the compiler treats the name as a variable,
  prints `WARNING: ER$ARGS is not assigned a value`, reports `0 error(s)`,
  and ships the broken object; the real failure arrives later at runtime as
  "Unassigned variable" in a program that compiled clean. **Read every such
  WARNING as a probable missing include.** Recovery from a poisoned
  catalogue: restore `SYSCOM/ERR.H` from the repository, recompile
  `CATALOG` and hand-copy its object into `gcat` (the old broken `$CATALOG`
  can't catalogue it), then `BCOMP`, then `SECOND.COMPILE` repairs the rest.

- **`AND` does not short-circuit, and BCOMP cannot see a per-path
  unassigned variable — together they hid a broken verb for over two
  months.** `CREATEA`'s GROUP path tested
  `acc.type = 'USER' and not(valid_os_name(acc.uname))` where `acc.uname`
  is only assigned on the USER path — **both operands are evaluated
  regardless**, so `!VALID_OS_NAME` aborted on every `CREATE.ACCOUNT
  GROUP` from 10 June until 21 Aug 2026, with a clean compile every time
  (BCOMP's "not assigned" warning is per-**variable**, not per-path — it
  cannot catch this class). **Nest the test, or assign the variable
  unconditionally at the top.** Also: nothing had ever tested `CREATE.ACCOUNT
  GROUP` — now `verify-accountrules.ps1` step 3.

- **`SECOND.COMPILE` must run under `sd -internal`, not `sd -ASDSYS`** —
  `BCOMP` gates `$internal` on `K$INTERNAL` **and** `K$ADMINISTRATOR`
  together; being in SDSYS alone gives a cascade of misleading parse
  errors (right bracket not found, matrix not in DIM) far from the real
  cause.

- **`errlog` throws away its own history** — `log_message()` discards the
  oldest half at the configured size. Fine for diagnostics, do not put
  audit records there (§5.6).

- **`VALID_OS_NAME` rejects spaces in user names**, undoing a change the
  original made *for* Windows compatibility. Called from `CREATEA`/`APISRVR`.

- **Two different path validators, similar names, different bugs, and
  fixing one says nothing about the other.** `OSPATH(path, OS$PATHNAME)`
  (C, `op_dio2.c`) split on `/` alone and refused any component containing
  `:` or `\` — so `CREATE.ACCOUNT` created the Windows user and set its
  password, THEN failed with "Invalid account pathname", leaving a
  half-made account with a message that named the wrong kind of problem.
  Fixed: optional drive letter skipped, split accepts either separator —
  `df_restricted_chars` deliberately NOT widened (it does a different job,
  mapping record ids to filenames). `VALID_OS_PATH` (BASIC,
  `CREATEA`/`PY_RUNFILE`) rejects backslash and space outright — not in the
  external GPL.BP tree, added by an AI cleaning cycle, nothing upstream to
  copy.

## 8. Open questions

**Only open questions stay.** Two nobody has diagnosed. The rest of this
section — the Python plan (built and witnessed; §5.27 has the decision), the
settled items and the closed questions — is in HISTORY.md, *"ARCHIVE 21 Sep
2026 — PROJECT_STATUS.md before consolidation"*.

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

**RESTORED TO THIS FILE 21 Aug 2026**, raised 19 Aug 2026. **What was seen:**
138/142 then 142/142 with nothing changed between, roughly **2 runs in 10**,
cause unknown. Three explanations were spent ruling out and are all dead: the
`$RELEASE` prompt, the revision cross-check, the installer's `ADOPT` step
running SD.

**Why it stays open rather than closed:** the discipline here is *cycle, then
measure*, and **a check that fails without meaning it teaches whoever meets it
to re-run until green** — which is how a real failure gets waved through.

**One later instance was traced to the test being wrong, not the tree** — four
checks expected `voc_template`-only records absent from an account VOC built
from `newvoc`, where "Record not found" was correct; the verifier now asserts
the absence too. Whether that was the whole of it was never established.

**IF IT RECURS, CAPTURE THE RUN UNPIPED** — both original sightings were lost
to `Select-String` eating the answers.

**IT RECURRED 22 Aug 2026, 08:32:03 install, and this sighting has the
breakdown the others lacked.** Same verifier (`verify-lcnames`), same shape:
142/142 at 08:52, then 135/142 at ~09:00, no source change between
(`assert-current` exit 0 either side). **All seven failing checks begin with
`LOGTO SDSYS`**, and every one of the 135 that passed runs inside the invoking
user's own account — a narrowing (what they share is *entering SDSYS*), not a
diagnosis; three of the seven are read-only, so nothing was renamed and left
unrestored. **A second, separate fault followed 13 minutes later** (`Forced
logout` from `Stop-Process` killing sessions) and must not be conflated with
this one — the 135/142 happened first, with the tree healthy.

---
