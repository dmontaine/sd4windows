# CLAUDE.md

## Read this first

**[PROJECT_STATUS.md](PROJECT_STATUS.md) is the handoff document. Read it
before doing anything else in this repository.** It holds the current state,
the decisions already made and why, the traps that have already cost time, and
the ordered next steps. [HISTORY.md](HISTORY.md) is the append-only archive —
read it when you need to know why something is the way it is, or whether an
approach has already been tried.

This project moves between sessions, machines and accounts. Nothing carries
over except what is written in those two files.

## Search the record before you run anything

Standing instruction from the repository owner, 23 Aug 2026, after three or
four consecutive sessions where the thing that went wrong **was already written
down before the session started.** Sessions are not being lost to unknowns.
They are being lost to warnings that were on disk and unread.

**Before running a command, grep both documents for what you are about to
run** — the **verb, script, path or flag you are about to type**, most
distinctive token first. From the repository root:

```sh
grep -n -i -E 'echo WHO \| sd' PROJECT_STATUS.md HISTORY.md
```

Read every hit. A hit is normally a session that has already paid for it.

**A broad term returns dozens of hits. Narrow it, do not skip it** — add a
second stage for warning language, which reliably cuts it to a readable
handful:

```sh
grep -n -i -E 'cycle\.ps1' PROJECT_STATUS.md HISTORY.md |
  grep -i -E 'NEVER|DO NOT|CANNOT|MUST|trap|hung|hang|cost|refus|wrong|stale'
```

**Everything needs the check except this list:** reading a file, `grep`/`find`,
and read-only `git` (`log`, `show`, `status`, `diff`). If you are deciding
whether something is harmless enough to skip, that is the moment the rule is
for — run the grep.

**It applies to the first attempt, not just a retry**, and to commands that
look trivial. What was walked into on 23 Aug 2026 was `echo WHO | sd`, which
§START HERE already recorded as making an unusable session; it hung, and the
stray `sd.exe` cost an elevation to clear. **Some warnings are in the memory
file rather than these two** — the `MEMORY.md` index is loaded every session,
so read it as part of the same check.

**Finding a warning does not forbid the command.** Overriding a stale one is
legitimate — say which warning, and why it does not apply, before you run.
Overriding one you never saw is what this rule exists to stop.

## Run standing procedures exactly as written

Standing instruction from the repository owner, 23 Aug 2026, after a session
ran `cycle.ps1 -Silent` instead of the documented `cycle.ps1`. His words: *"If I
had been asked I would have asked for clarification and said no."*

**The standing commands are written with their arguments** — in this file and in
PROJECT_STATUS.md's "START HERE". **Anything you add to one is a change to the
owner's procedure, and it needs his yes first.** A flag that exists, is
documented, and is off by default is not thereby approved: `-Silent` was all
three.

***THE OLD TELL — "WHO IS THE SHORTCUT FOR" — IS WITHDRAWN. CORRECTED BY THE
OWNER, 28 Aug 2026: he PREFERS unattended operation wherever it is possible.***
This section used to forbid the direction outright. It now governs the manner
only. **Reducing the number of times a person has to be present is a GOAL, not
a smell** — but every guardrail below survives the change, because none of them
was ever really about keeping a human in the loop.

- **PURSUE IT BY REMOVING THE NEED FOR A PROMPT, NOT BY SKIPPING THE STEP.**
  `gplbld/sd-elevate.ps1` is the shape to copy: **one** UAC consent at
  `-Start`, then a resident elevated helper serves the whole session over a
  named pipe, with a `PING` that answers `ELEVATED` so a reply from something
  unelevated cannot be mistaken for success. That turns four prompts into one
  **and measures exactly what it measured before**. `-Silent` turned a watched
  install into an unwatched one and measured **less**. The first is the goal;
  the second is the thing this section still stops.
- ***A FLAG YOU ADD IS STILL A CHANGE TO HIS PROCEDURE AND STILL NEEDS HIS
  YES.*** Unchanged, and it is the part that caught `-Silent`. A flag that
  exists, is documented, and is off by default is not thereby approved:
  `-Silent` was all three, and it produced an install with **no password on any
  account**, handed over as an unexplained hang in SD's start-up. Two sessions.
- ***NO VERDICT MAY COME FROM A RUN NOBODY COULD HAVE OBSERVED.*** This is the
  guard that replaces the old blanket ban, and it is the one to reach for when
  automating. **Removing the need for a person to be PRESENT is allowed;
  removing the evidence that would have let one disagree is not.** A run whose
  output nobody can read afterwards is not a result — see the instrument rules
  below, which are now doing the work this section used to do.
- **SOME OF IT IS NOT REACHABLE, AND THAT IS MEASUREMENT RATHER THAN
  PREFERENCE.** UAC renders consent on the secure desktop, so a **nested**
  elevation has no desktop to render on: it fails with *"The operation was
  canceled by the user"* while showing nobody anything (§4.0.1). And the verify
  suite's parent **must stay unelevated** — several measurements are only valid
  there, and an elevated parent cannot make an ordinary child, because
  `runas /trustlevel` yields a RESTRICTED token rather than the user's own.
  **Do not spend a run rediscovering either.**
- **ONE DEVELOPER, ONE MACHINE, A LAPTOP LATER — AND BOTH HAVE `sudo`.** Owner,
  28 Aug 2026. So *"it would not work on another machine"* is no longer an
  objection to using a 24H2-only tool **in `gplbld` tooling**. It remains an
  objection for anything that **ships**: `sd.iss` neither installs nor enables
  `sudo`, deliberately, because Windows 10 and Server have none.

**Asking is cheap and he answers in a sentence.** The cost of not asking is
carried by whoever picks the session up.

**This is about deviating, not about doing.** Running the documented command as
documented needs no permission, and neither does ordinary reading, searching or
building.

## Never inline a script that contains a backslash

Owner, 23 Aug 2026: this trap *"has caused many many redos"*. It is a hard rule
now, not a caution.

**If a Python or PowerShell snippet contains `\` — and on Windows that means any
path — write it to a file with the Write tool and run the file.** Do not pipe it
through a heredoc, `-c`, or `-Command`. Checking is mechanical: *does my inline
script contain a backslash?* Then it does not go inline.

**THERE ARE TWO FAILURE MODES AND KNOWING ONLY THE FIRST IS WHY THIS KEEPS
HAPPENING:**

1. **Unquoted heredoc (`<<EOF`)** — the *shell* eats `\` and expands `$`.
   Widely known, and the reason people reach for `<<'EOF'`.
2. **Quoted heredoc (`<<'EOF'`) feeding Python** — the shell is now innocent and
   **Python's own string literals** still interpret the escapes. `"C:\Users\..."`
   in Python source is `\U`, a truncated `\UXXXXXXXX` escape, and it fails at
   *parse* time. `"C:\temp"` is worse: `\t` is a tab and it fails **silently**.

**Quoting the heredoc fixes 1 and does nothing for 2.** That is the whole trap,
and believing `<<'EOF'` is safe is what walked into it again on 23 Aug 2026.

**If something truly must be inline**, use a raw string (`r'C:\Users\...'`) or
build the separator with `chr(92)` — but prefer the file. A file is also
re-runnable, diffable, and can be parse-checked before it is run.

## Never reach for Python to edit a file

Standing instruction from the repository owner, 28 Aug 2026, immediately after
a session used a Python heredoc to change three table rows in
PRE_RELEASE_FIXES.md. **Use the Edit and Write tools.**

**The rule is about the FIRST reach, and that is where it keeps going wrong.**
The edit always looks mechanical enough to script — three rows, one regex — and
that is exactly the case the editing tools handle with **no encoding,
line-ending or escape surface at all**. What went wrong on 28 Aug was not the
code; it was the decision to write code. The snippet emitted
`SyntaxWarning: invalid escape sequence` and was correct only by luck, and
proving it had not corrupted the file cost a byte-level check that the Edit tool
would not have needed.

**THIS FILE ALREADY SAID SO IN THREE OTHER PLACES AND IT WAS STILL DONE.** The
backslash rule above, the CRLF trap and the `Set-Content` trap are all the same
lesson from different angles, and each is written as advice about *how* to write
the snippet. **They were followed and the file was still edited by a program.**
So it is now a rule about the tool, not about the snippet:

- ***A FILE EDIT GOES THROUGH `Edit` OR `Write`.*** Not `python`, not `sed -i`,
  not `Set-Content`, not a heredoc.
- **If a transform is genuinely too large to do by hand** — a bulk rename across
  hundreds of files — **say so before writing it**, put it in a script file
  rather than inline, and check the result the way the `Set-Content` rule below
  requires: BOM, CR count, mojibake, and `git diff --stat`.
- **`grep`, `find` and read-only inspection are unaffected.** This governs
  *writing*.

**Three separate corruptions of tracked documents are already in the record** —
PROJECT_STATUS.md rewritten wholesale by Python text mode on 21 Aug 2026 (10,998
insertions for a four-line edit), PRE_RELEASE_FIXES.md double-encoded by
`Set-Content` on 28 Aug 2026 (272 em dashes), and the near miss the same day.
**Every one was silent**, and `.gitattributes` (`* -text`) means nothing
normalises the damage.

## Verify a script loads before you submit it for execution

Owner, 23 Aug 2026: too many broken scripts have been **submitted for
execution** — handed to him to run, or fed to a cycle or the verify suite — and
each costs a wasted run or an investigation before anyone learns it never
started. **A script you have not watched load is not ready to submit.**

**The trigger is the handoff, not the typing.** The moment a script goes to the
owner's terminal, into `cycle.ps1`, or into `VerifyInstall1`, its failure lands
away from you. Load it first with the tooling that will run it and **watch the
result — do not hand it over `unrun`.** §START HERE's `verify-apiidentity` was
handed over `unrun, deliberately`; it carried an embedded BOM, died on load as
step 17 of `b18`, and the empty step scored a false green.

**Use the check that CATCHES THE BREAK — a parse-check alone is not it, and this
is measured, not assumed.** The BOM'd file parsed with **0 errors**: `ParseFile`
on the broken bytes returned no error and 18 functions instead of 19, because
`New-SdConnection` had parsed as a command call that swallowed its own body. So
run both, and both cost no cycle:

1. **Parse or compile, for syntax** — PowerShell
   `[System.Management.Automation.Language.Parser]::ParseFile($p,[ref]$t,[ref]$e)`
   with `$p` a **forward-slash** path (so the call carries no backslash, per the
   rule above), then assert `$e.Count -eq 0`; it does not execute the script.
   Python: `python -m py_compile file.py`.
2. **Byte-scan for the encoding gremlins the parser waves through** —
   `grep -a -b -o $'\xEF\xBB\xBF' file`; any hit past offset 0 is an embedded
   BOM. A stray `\t`-as-tab hides from `py_compile` the same way, so a script
   with a backslash still takes the file route above, never a heredoc.

**The check itself obeys the instrument rule:** echo the resolved path and the
counts — 0 parse errors on a file the parser found none of your functions in is
not a pass. **The one exemption is the inline one-liner whose failure you see at
once**; you are already watching it, so there is nothing to pre-check.

## Every command you hand over carries a full path and an elevation verdict

Standing instruction from the repository owner, 28 Aug 2026: *"whenever I am
given something to run, I need the complete path and whether or not to run it
elevated."* Said after a session gave `verify-tiers.ps1` correctly the first
time — absolute path, *"in your own terminal, elevated"* — and then handed over
the `-Prefix sdtierb` rerun as a bare command with no elevation stated.

**Both parts, every time, in the same block:**

1. ***THE ABSOLUTE PATH, WITH EVERY VARIABLE ALREADY EXPANDED.***
   `C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\cycle.ps1`, never
   `cycle.ps1`, never `gplbld\cycle.ps1`, and never `$env:TEMP\…` or `%TEMP%\…`
   — **his elevated shell opens in `C:\WINDOWS\system32`**, and he moves between
   cmd and PowerShell without saying which he is in, so shell-specific syntax is
   a coin flip. A script that finds its own location internally does not change
   this: that makes it cwd-independent *once found*, which is the part a bare
   name breaks.
2. ***ELEVATED OR NOT, SAID OUT LOUD — INCLUDING WHEN IT IS NOT.*** **Silence
   is not "probably fine".** Say *"elevated PowerShell"* or *"an ordinary
   unelevated prompt"*. Some of this project's measurements are only valid
   unelevated — §4.0.1's suite, `edit bp ZZMARKS` in item 5.3, the `logto`
   suspension door — so the wrong shell does not merely fail, **it can produce
   a clean-looking wrong answer.**

**The trigger is the hand-over, not the first mention.** A rerun, a retry with
a different flag, a command repeated from earlier in the same message — each is
a fresh hand-over and carries both parts again. It is two lines; he is the one
who pays when either is missing.

## An instrument shows what it DID, not just what it concluded

Owner's instruction, 23 Aug 2026, after three false verdicts in one session.
**Every one of them was a confident conclusion drawn from an instrument that
never reached the condition it claimed to measure.**

**A verdict with no evidence of what was actually measured is not a result.**
Any probe, test or verifier must print, in its own output:

1. ***THE REAL INPUTS IT USED*** — the exact command line and arguments passed,
   the resolved paths, the target account. Not what it intended to pass.
2. **The state it compared — BEFORE and AFTER**, not just the conclusion drawn
   from them.
3. ***AND IT MUST REFUSE THE NULL CASE OUT LOUD.*** If the measurement could
   have run against nothing, test for that and say so. **A test that passes
   because it did nothing must fail, not pass.**

**WHAT THIS COST ON 23 Aug 2026, three times:**

- **`sd` reported "no output"** — stdout had been redirected to a file nobody
  read. The password prompt was in it the whole time. *One day.*
- **A probe's parameter was named `$args`**, a PowerShell **automatic**
  variable, so it was clobbered and `Start-Process` received **no switches**.
  Setup ran non-silently, the gate correctly did not fire, and the verdict logic
  passed *trivially*. Caught only because the echoed line read `setup ` with
  nothing after it — **rule 1 above is what caught it.**
- **A suite row was called "the one failing check"** on a suite that had never
  run a step.

**THE FIX IS NEVER THE ONE-LINE CAUSE.** Renaming `$args` fixes that probe;
echoing the arguments and refusing an empty list fixes the *class*. **Ask what
would have caught it, not what caused it.**

## A check must anchor on the SUCCESS wording, not on any string the failure also carries

Owner's rule, 23 Aug 2026, after `verify-apiidentity` was reported "confirmed"
on a Step 3 that had actually been refused. A tightening of the instrument
rule; it sits here because it is a specific trap that keeps recurring.

**A verification is a claim about a specific outcome.** Its match text has to
be one that appears **only when that outcome happened**, and cannot appear when
the tool refused, printed a "not found" message, or merely echoed its own
input. **A pattern shared by the success and failure outputs is not a check —
it is a false positive with a check's name on it.**

***THE TRAP ON 23 Aug 2026, and what a real check would have looked like.***
Step 3 was `Invoke-SD ... "SET.FILE $allowDir ZZIDALLOW" ...` and the guard
was `$out -match 'ZZIDALLOW'`. SD **refused** with *"Account name '...' is not
in register"* and later *"Record 'ZZIDALLOW' not found"*. `ZZIDALLOW` appeared
in **the echoed command**, **the refusal**, **the CT VOC error** — three
places on the failure path — so the match reported success. Three runs (`b19`,
`b20`, `b21`) VOIDed downstream before anyone read Step 3's raw output.

**Two mechanical fixes for the class:**

1. ***MATCH THE SUCCESS WORDING THE TOOL PRINTS ON THE POSITIVE PATH.*** Not
   the argument you passed in and not the id you asked about — those are
   already in the failure output. Look at the tool's success output once
   (`Password set`, `File created`, `Record 'x' is a file pointer to ...`) and
   anchor there. For SD verbs the source in `sdsys/gpl.bp/<VERB>` names the
   `display sysmsg(...)` calls; either the success text or the sysmsg id
   itself is a safe anchor.
2. ***CONTROL: MATCH THE FAILURE WORDING TOO, AND REFUSE IF IT APPEARS.***
   `not in register`, `not found`, `syntax error`, and the tool's own error
   framing (`ER_`, `sysmsg 2201`) are all disqualifiers. A step where the
   positive pattern matches AND a disqualifier matches is not a pass either.

**The rule also demands the output stays visible.** Rule 1 of the instrument
section says to print what the tool actually did; **echoing the output when it
looked wrong** is not enough here. Print Step 3's raw output every time. A
subtle refusal that only becomes obvious in retrospect is one no *conditional*
print will catch, because the condition is the thing that was wrong.

## You must maintain these files, cheaply

Standing instruction from the repository owner, 14 Aug 2026: **the ratio of
time spent on the project to time spent documenting it was too high.**
PROJECT_STATUS.md and HISTORY.md are **written for the next AI session, not for
him** — he does not read them. So:

- **Terse and factual.** `file:line` over description. No narrative, no
  emphasis for effect, no restating a finding in several sections. One fact,
  one place, with pointers.
- **Documentation is a small fraction of a session.** If it approaches half,
  stop and cut. Do not print line counts in the files or re-measure to keep
  them true.
- **Update PROJECT_STATUS.md in the same commit as the work**, and never move
  anything into "Verified" without observing it yourself that session.
  Compiling is not running.
- **Append to HISTORY.md** when work completes or an earlier claim proves
  wrong. Append-only. Keep entries short.
- **`sdb_ai/sd64/sdsys/changelog` is the exception**: it ships to users, stays
  plain English, and gets anything a user would notice, in the same commit.
- **[UPSTREAM_FIXES.md](UPSTREAM_FIXES.md) is the other exception**, and it is
  **maintained, not written once**: when you find a defect that is also in
  `sdb64`, add an entry in the same commit as the fix. Check first — the clone
  is at `../sdb64`, and a bug carrying a `Composer AI - 2026/06/10` marker is
  ours rather than upstream's unless the underlying flaw is there too. It is
  written for the upstream maintainer, so plain English and self-contained.
- **[PRE_RELEASE_FIXES.md](PRE_RELEASE_FIXES.md) is the third**: everything that
  needs deciding or fixing before W1.0-0 ships. Add an entry in the same commit
  as the finding and move it to DONE with a date when it is fixed. Most of it
  comes from writing the documentation, because making a sentence true checks
  something that testing that it works does not.

  ***THE TWO FIX FILES ANSWER DIFFERENT QUESTIONS, AND A DEFECT IN BOTH TREES
  GOES IN BOTH.*** Owner, 26 Aug 2026, correcting the "one defect, one file"
  rule that stood here for one session and was wrong. **UPSTREAM_FIXES.md says
  *"the maintainer of `sdb64` should know about this"*; PRE_RELEASE_FIXES.md
  says *"we would ship this"*** — and being upstream's bug has never been a
  reason to ship it. So: file it upstream if `sdb64` has it too, **and** list it
  here for as long as our own tree still carries it, pointing at the upstream
  entry rather than repeating the analysis. **Being fixed upstream is not being
  fixed here.** Three entries were found this way the day the rule was
  corrected, one of them silent data loss.

Full rules in §0 of PROJECT_STATUS.md. Follow those; this file only points.

## Project constraints

- **Windows only.** Linux development lives in a separate repository. Do not
  add `#ifdef` branches to keep Linux building — replace Linux code outright.
- **No binaries in this repository.** Everything must be auditable from source.
  That is why the pcode build is Python (`gplbld/`) rather than a shipped
  binary, and why no `.exe`, `.dll` or object file is tracked. Anything that
  has to ship as a binary ships outside the repository, as a release artefact.
  Do not add a convenience exception; installing means building.
- Two toolchains, deliberately: the server builds against the MSYS2 POSIX
  runtime, the client DLL is native UCRT64. See PROJECT_STATUS.md §5.4.

## Building

```sh
cd sdb_ai/sd64 && make sd
```

`make` must run from `sdb_ai/sd64` — the Makefile uses `MAIN := $(shell pwd)/`.
`make sdclilib` builds only the client library. After switching toolchains,
clear stale objects with `rm -f gplobj/*.o`.

***YOU NORMALLY DO NOT HAVE TO RUN THIS AT ALL — `cycle.ps1` STEP 0 DOES IT.***
Owner's instruction, 3 Sep 2026: *"seems like there should be one script that
can do all three, compile c if necessary, compile basic if necessary and run
the installer if necessary."* The cycle now rebuilds the C when source has
moved past `bin\`, compiles the BASIC as it always did (`stage.py --bootstrap`,
step 2), and installs. **The install stays unconditional** — a test cycle
begins with a *fresh* one.

**Run `make sd` by hand only to compile without cycling** — the equivalent of
`cycle.ps1 -SkipInstall` for the C half.

***AND "IF NECESSARY" IS NOT WHAT `make` MEANS BY IT, WHICH IS WHY STEP 0 IS
MORE THAN A CALL TO `make`.*** `make` relinks only what changed, while
`assert-current` compares source against the **oldest** binary in `bin\` — so
editing one C file and running `make sd` leaves the tree STALE and every verify
script refusing. Step 0 therefore **deletes the binaries and relinks all of
them**, then asks the guard again rather than trusting `make`'s exit code.
`gplbld/stale-binaries.ps1` holds the rule, one copy for both callers.

## Testing: every cycle runs against a newly installed system

Standing instruction from the repository owner, 15 Aug 2026, after stale
installs caused the same failure repeatedly. **A test cycle begins with a fresh
install. Not a reinstall over the top of the old one.**

**One command, elevated PowerShell** — `gplbld/cycle.ps1` does the whole cycle:
***rebuilds the C if source has moved past `bin\` (step 0, added 3 Sep 2026)***,
stops the service, stages and bootstraps, checks the staged tree is whole,
builds the installer, uninstalls, deletes both trees, installs, then runs
`assert-current`. **So a C change no longer needs `make sd` first** — see
"Building" above for why that step deletes the binaries rather than just
calling `make`.

```powershell
C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\cycle.ps1
```

`-SkipInstall` stops after building the installer, which is the cheap way to
find out whether a BASIC change compiles without spending an install.

**Do not hand-run the steps.** Owner's instruction, 17 Aug 2026, after the
sequence had grown to four commands across three shells; the two faults that
prompted it — a still-running SD service, and `ISCC` run from a directory where
`gplbld\sd.iss` does not resolve — are now structurally impossible rather than
merely written down. PROJECT_STATUS.md §"START HERE" has both.

Why it is a rule and not a preference, ***CORRECTED 30 Aug 2026 —
PRE_RELEASE_FIXES 71. THE RULE IS UNCHANGED AND THE REASON IT USED TO GIVE WAS
FALSE.*** This paragraph said **the installer deliberately never overwrites an
existing `C:\ProgramData\SD\sdsys`**, and that stopped being true on **25 Aug
2026**, when the owner ruled *"preserve the user's own files, replace all the
shipped ones"* and `upgrade.iss` was built to do it. `sd.iss:1044` states the
invariant that replaced it: *"upgrade.iss is gated on this; the whole-tree entry
in `[Files]` is gated on `DataTreeAbsent`. One or the other fires on every
install, never both and never neither."*

**The real reason is worse, not weaker: AN UPGRADE REPLACES FILES AND RE-RUNS
NOTHING** (PRE_RELEASE_FIXES 70). `gpl.bp`, `syscom`, `newvoc`, `voc_template`,
`messages` and `sd.voclib` are replaced, while `$cred`, `accounts`, `cat`,
`os.users`, `batch.jobs`, `prt`, `$hold`, `bp` and `bp.out` are preserved — so a
BASIC or message fix *does* reach an existing tree, but **no existing account,
including SDSYS's own, ever gains a new verb.** "I tested it on the installed
system" therefore still means "I tested a tree whose per-account state is
whatever the first install left". This has cost whole investigations of bugs
already fixed — PROJECT_STATUS.md §6 and the four-fault run in HISTORY.md.

**A rule defended by a false reason is one the next session argues with**, and
this one was a step away from being argued into a wrongly-filed blocker.
`gplbld/assert-current.ps1` is the instrument that replaced the hand-checks.

**Do not reason your way out of it.** Hashing a few files that look current is
not evidence the tree is: the files you would think to check are the ones you
already believe changed, and `gcat` — the catalogue that actually runs — is not
readable as source. A ninth-session attempt to do exactly this is recorded in
PROJECT_STATUS.md header item 1.

**Then date what you are testing before believing any result from it**, and
state the full path of the binary under test — `C:\Program Files\SD\...` is the
installed one and is current only just after an install.

**A CYCLE ENDS AT THE NEXT SOURCE CHANGE.** Added 15 Aug 2026 because the rule
above says when a cycle *begins* and said nothing about what ends one, and that
gap was enough to break it twice in one session — both times by editing source
while a test was in flight and carrying on reading the results. **Any result
taken from the tree after a source change is void, not "probably still valid".**
Finish every source change first, then run one cycle, then measure.

**This is enforced, not remembered:** `gplbld/assert-current.ps1` exits non-zero
unless the installed tree matches source, and `verify-createaccount.ps1` refuses
to run without it. Call it first from anything new that tests the install.
**Hashing `sd.exe` is not sufficient on its own** — most changes here are BASIC,
messages, dictionaries and the installer script, none of which touch the binary,
so it also compares source mtimes against the install. The scripts that test
Windows-side behaviour rather than SD (`verify-sshonly.ps1`,
`verify-allowgroups.ps1`) are deliberately exempt.

## The full verify suite runs at milestones, not after every change

Standing instruction from the repository owner, 30 Aug 2026, after `b73`, `b74`
and `b75` each cost about twenty minutes: *"add `-Only`, and drop the full run
to milestones."* A full run is **~20 minutes** — 4.6 unelevated, 15 elevated —
and the single step that decides a change is usually **30 to 90 seconds** of it.

**Three tiers. Use the cheapest one that can answer the question.**

1. **The free unit tests and `assert-current`** — seconds, no install, no
   elevation, no run token: `test-tiercounts-units`, `test-fixlist-units`,
   `test-verdict-units`, `test-sdtestuser-units`, `test-suiteonly-units`,
   `test-retired-wording-units`, `test-stemcoverage-units`,
   `test-dirscoverage-units`, `test-stripcomments-units`,
   `test-diffcapture-units`, `test-transcriptwhole-units`,
   `test-apigate-units`, `check-stale-leads.py`,
   `test-staleleads-units.py`, `test-edittokens-units.py`,
   `test-upgradeiss-units.py`, `test-acctmsgs-units`,
   `test-apiidentity-units`, `test-deletioncheck-units`,
   `test-doorsargv-units`, `test-reclaim-units`, `test-sdpath-units`,
   `test-sysmsg-units`, `test-vocverbs-units`, `test-reconcile-units`,
   `test-stalebin-units`. ***ALL TWENTY-SIX. Run these on
   every change*** — **about 30 s for the whole set**, measured 3 Sep 2026, each
   in its own process. A whole suite run has already been spent twice discovering
   what one
   of them names in a second. **`test-retired-wording-units` is the wording
   lint**: it scans every message file and shipped script for phrases that were
   deliberately reworded, so a fix that lands in one copy and misses another
   (PRE_RELEASE 121, a ~19-minute find on a screen) fails here in a second
   instead. When you retire wording, register the old phrase and its
   replacement in that script's `$RETIRED` table, in the same commit.

   ***THE LAST TWO WERE MISSING FROM THIS LIST UNTIL 2 Sep 2026, WHICH IS THE
   DEFECT THEY BOTH EXIST TO CATCH.*** `test-stemcoverage-units` shipped 31 Aug
   and `test-dirscoverage-units` on 2 Sep; neither was named here, so "run the
   free tests" meant a list that did not include them. **Both are guards over
   two files that describe one fact and are kept in step by hand** — the litter
   sweep's stems against the runners, and `sd.iss`'s `[Dirs]` block against
   `stage.py`'s directory lists — and *this list is a third instance of exactly
   that shape.* **A new free guard goes in this sentence in the commit that
   creates it**, the same rule as `assert-current`'s `$neverShipped`.

   ***`test-diffcapture-units` JOINED IT 3 Sep 2026, ONE COMMIT LATE, WHICH IS
   WORTH THE SENTENCE.*** It guards `gplbld/diff-capture.ps1`, the manifest
   comparison PRE_RELEASE 134 needs. It was written and committed with the
   script, and this list was updated in the NEXT commit rather than that one —
   so for one commit the guard existed and "run these on every change" did not
   name it. **That is the exact gap the paragraph above describes**, arrived at
   by an author who had just read it.

   ***`test-transcriptwhole-units` JOINED IT 3 Sep 2026 IN THE COMMIT THAT
   CREATED IT***, which is the rule above working and needs no paragraph of its
   own. It guards `gplbld/transcript-whole.ps1`, PRE_RELEASE 137's check that a
   cycle log actually received ISCC's output.

   ***`test-stripcomments-units` WAS ADDED HERE IN ITS OWN COMMIT, 2 Sep 2026,
   WHICH IS THE RULE ABOVE WORKING RATHER THAN A TENTH ENTRY WORTH NOTING.***
   It guards `gplbld/strip-comments.ps1`, the comment stripper that
   `assert-current` and `test-retired-wording-units` now share
   (PRE_RELEASE_FIXES 143). **And the same commit found `$neverShipped`'s one
   real gap**: `test-retired-wording-units.ps1` had never been listed, so
   editing the wording lint turned the tree STALE for a file that ships nowhere
   and offered a whole cycle as the cure. **The directory was swept rather than
   the one name added** — every other gplbld script missing from that list
   genuinely is named in `stage.py` or `sd.iss`, so it was one omission and not
   a rotted list.

   ***`test-staleleads-units.py` JOINED THE LIST 2 Sep 2026 AND IT HAD BEEN RED
   FOR DAYS, WHICH IS WHAT NOT BEING ON THE LIST COSTS.*** 12 of 13, and nobody
   ran it. **`check-stale-leads.py` itself exited 0 throughout**, because the
   failing case guards phase 1, which ranks and deliberately does not decide —
   so the listed check passed while its own units test failed.
   ***THE TEN THAT WERE STILL MISSING JOINED THE LIST ABOVE ON 3 Sep 2026***,
   the owner delegating the call — *"what tests are needed in the verification
   cycle are totally your call"*: `test-edittokens`, `test-upgradeiss`,
   `test-acctmsgs`, `test-apiidentity`, `test-deletioncheck`, `test-doorsargv`,
   `test-reclaim`, `test-sdpath`, `test-sysmsg`, `test-vocverbs`. ***IT WAS
   DECIDED ON A MEASUREMENT RATHER THAN A PREFERENCE***: the ten cost **7.1 s**
   against the fourteen's **21.8 s**, all twenty-four green, none needing an
   install, elevation or a run token. **So the sentence now asks 29 s of a
   session instead of 22, and that is not a price worth a second guard going
   red for days unread.** *(The superseded wording listed `test-staleleads`
   among the ten. It was already on the list and there is no separate script of
   that name — the count of ten was right, one of the names was not.)*

   ***`test-reconcile-units` JOINED IT 3 Sep 2026 IN THE COMMIT THAT CREATED
   IT***, which is the rule above working and needs no paragraph of its own. It
   guards `gplbld/reconcile-accounts.ps1`'s decision table, PRE_RELEASE 93 and
   65's sweep — the one that deletes account directories as LocalSystem at
   every service start.

   ***`test-stalebin-units` JOINED IT 3 Sep 2026 IN THE COMMIT THAT CREATED
   IT.*** It guards `gplbld/stale-binaries.ps1` — this script's own check A2,
   lifted into a file so that **`cycle.ps1`'s step 0 and `assert-current` decide
   "does the C need rebuilding" with the same code**. Its exclusions each cost a
   session when they were missing, and none of them can be exercised by running
   the thing on a healthy tree.
2. **`-Only <step[,step]>`** — the step that decides your change. Both runners
   take it; names may omit `.ps1` and are case-insensitive. **Two names work
   either way — `-Only a,b` and `-Only 'a,b'` are equivalent since 31 Aug
   2026**, when both runners went `[string[]]`. *Before that the unquoted form
   died on parameter binding without running anything, and every example here
   was single-name, so nothing said so.*
3. **The full suite** — **before a release, and before a handoff.** That is
   where regressions in things you did not touch get caught: `b75`'s second
   failure was `verify-notyet`, unrelated to anything changed that day.

**`-Only` and `-ThenElevated` do not combine**, so a targeted elevated step is
run against `VerifyInstall2` directly:

```powershell
C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\VerifyInstall1.ps1 -Only verify-lcnames
C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\VerifyInstall2.ps1 -Run b76 -Only verify-delaccount
```

The first is an **ordinary unelevated** prompt, the second an **elevated** one.
***`-Run` is still required for a targeted elevated step and still derives every
prefix*** — that is the reason to go through the runner rather than call the
verifier by hand, because a fixed prefix passes once and fails every later run
(PRE_RELEASE 54).

***A PARTIAL RUN IS NEVER REPORTABLE AS A PASSING SUITE.*** The banner, the
summary heading and the closing line all carry `PARTIAL`, and the closing line
never reads *"every step exited 0"*. **A mistyped step name is refused by name
and exits 2** rather than selecting nothing and reporting success — the null
case the instrument rules above forbid. `gplbld/suite-only.ps1` holds the
filter, one copy for both runners, and `test-suiteonly-units.ps1` drives it.

## Conventions

- Match the surrounding code. It is a 2007 Ladybridge codebase with its own
  idioms — `Public`/`Private` macros, `START-HISTORY` blocks, banner comments.
  Add a dated line to a file's `START-HISTORY` block when changing it.
- Nothing binary is tracked — see the constraint above. `bin/` is build output
  and is ignored apart from its README.
- Explain *why* in commit messages, not just what. The reasoning is the part
  that does not survive in the diff.
