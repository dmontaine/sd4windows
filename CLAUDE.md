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

**THE TELL IS WHO THE SHORTCUT IS FOR.** If the benefit is *"then nobody has to
be present"* or *"then I don't have to hand this back"*, stop and ask. That is
the whole class:

- **Unattended operation is not a goal of this project.** A cycle needs a person
  at the wizard; the verify suite needs a person's own terminal (§4.0.1); SD
  cannot be installed silently at all (owner, 23 Aug 2026). **An agent
  optimising toward "no human needed" is optimising against the design.**
- **The work does not get better, only more autonomous.** `-Silent` did not make
  that cycle a better test. It made it one nobody watched, and it produced an
  install with no password on any account — handed over as an unexplained hang
  in SD's start-up, and it cost two sessions.

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

## Testing: every cycle runs against a newly installed system

Standing instruction from the repository owner, 15 Aug 2026, after stale
installs caused the same failure repeatedly. **A test cycle begins with a fresh
install. Not a reinstall over the top of the old one.**

**One command, elevated PowerShell** — `gplbld/cycle.ps1` does the whole cycle:
stops the service, stages and bootstraps, checks the staged tree is whole,
builds the installer, uninstalls, deletes both trees, installs, then runs
`assert-current`.

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

Why it is a rule and not a preference: **the installer deliberately never
overwrites an existing `C:\ProgramData\SD\sdsys`**, so "I tested it on the
installed system" silently means "I tested the build that first created that
tree". This has cost whole investigations of bugs already fixed —
PROJECT_STATUS.md §6, "the installed data tree is never upgraded", and the
four-fault run in HISTORY.md.

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

## Conventions

- Match the surrounding code. It is a 2007 Ladybridge codebase with its own
  idioms — `Public`/`Private` macros, `START-HISTORY` blocks, banner comments.
  Add a dated line to a file's `START-HISTORY` block when changing it.
- Nothing binary is tracked — see the constraint above. `bin/` is build output
  and is ignored apart from its README.
- Explain *why* in commit messages, not just what. The reasoning is the part
  that does not survive in the diff.
