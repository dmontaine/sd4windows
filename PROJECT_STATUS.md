# PROJECT STATUS

Living handoff document for the SD Windows port. This project moves between
sessions, machines and accounts; anything not written here is lost. Read this
file first. Read [HISTORY.md](HISTORY.md) only if you need the record of how
something came to be the way it is.

**Last updated:** 21 Aug 2026, thirty-seventh session.

---

## NEXT SESSION: START HERE, IT IS SHORT

**ALL FOUR PHASES OF THE 21 Aug 2026 PLAN ARE DONE AND MEASURED.** Cycle 21 Aug,
install **17:18:11**, `sd.exe` **`CB9C4E0460B175F5`**, `assert-current` exit 0
afterwards — so these results describe the tree as it stands.

**NO CYCLE IS OWED. THE THIRTY-SEVENTH SESSION CHANGED NOTHING THAT SHIPS.**
Two commits, both documentation and one build script: the changelog exemption
(item 1 below) and the striking of step 11's *"does not work"* from the five
places that carried it. `assert-current.ps1` is on its own `$neverShipped` list,
so **the 17:18:11 install is still current — re-measured, exit 0, after the
edit** — and the suite below still stands. **Start from it.**

| verifier | prefix | result |
|---|---|---|
| `verify-fold` | — | 10/10 |
| `verify-createaccount` | `sdacct30` | exit 0 |
| `verify-tiers` | `sdtiert6` | exit 0 |
| `verify-accountacl` | `sdacl10` | 21/21 |
| `verify-routes` | `sdrt6` | 33/33 |
| `verify-accountrules` | `sdar3` | 35/35 |
| `verify-peerlog` | — | 21/21 |
| `verify-apiadmin` | `sdapia12` | 22/23, the 23rd a standing N/A |
| `verify-delaccount` | `sddel4` | 40/40, 0 N/A — every `Note` in the file fired |

**WHAT THE FOUR PHASES DID**, in one line each. §8 has the reversals, §"Phase 3,
as built" and §"Phase 4, as built" below have the reasoning, HISTORY has the
narrative.

| | |
|---|---|
| 1 | the API is a network service — binds `INADDR_ANY`, `APIPORT=4243` ships **active**, installer opens a firewall rule |
| 2 | remote access is a create-time property: `create.account user <n> ssh\|api\|both\|none`, same four on `modify.account` and **absolute, not additive**; password mandatory for USER accounts; one delete confirmation; `set.password` → `modify.password` |
| 3 | `ADOPT` is install-only behind a one-shot marker; the install ends in an SD session that takes the installing user's password |
| 4 | `verify-routes` rewritten; `verify-accountrules` written for the refusal paths |

**ONE THING IS LEFT AND IT IS THE OWNER'S.** `verify-delaccount` was one of the
three; it ran on the 17:18:11 install at **40 of 40, 0 N/A** — §4 has it, and
the Phase 3 `$adopt` marker assertion is measured. **The whole suite is now
green on one install**, so the next source change starts from a known tree.

1. **DECIDED AND BUILT 21 Aug 2026 — `sdsys/changelog` IS EXEMPT FROM THE
   STALENESS GUARD.** Owner's decision. It was touched by nearly every commit
   and each touch cost a cycle before the suite would run again.
   `assert-current.ps1:334` carries a second list, `$shippedButExempt`, holding
   that one path. **It could not go on `$neverShipped`**: that list is
   self-policing against `stage.py` and `sd.iss`, and `changelog` is quoted at
   `stage.py:140`, so it would have been reinstated on the next run and the
   exemption would have done nothing.

   **The guard's bias is kept by making it loud rather than silent** — when the
   changelog is newer than the install the script prints an `EXEMPT:` line
   naming it, **through `Write-Output` and not `Note()`, so `-Quiet` does not
   swallow it**. Measured both ways on the 17:18:11 install, and **with the
   control**: `sdsys/MESSAGES/10053` touched still reports STALE and exit 1, so
   the exemption is one path wide. What is accepted is that an install may carry
   a changelog behind source; nothing reads it.

2. **The two that outlive the plan.** The API session's TOKEN is still
   LocalSystem — §WHAT IS OWED, and the only large item left. And **nothing has
   ever crossed the network**: every API measurement has gone to
   `127.0.0.1:4243`. The bind is asserted `0.0.0.0` and the firewall rule exists,
   but the second machine in §7 step 2 is what settles it.

**OWNER'S RULING, 21 Aug 2026 — NO WINDOWS BRANCHES ANYWHERE. THIS IS A
WINDOWS-ONLY PORT.** CLAUDE.md already said it for the C code; it applies to
the BASIC layer too. **§7 step 12 was rewritten because it said the opposite** —
it had asked for the BASIC layer's Windows branches to be *restored* from the
external tree and the platform switches turned on. **They are to be removed
instead:** take the Windows arm, drop the conditional, delete the Linux arm.
§5.4 and §7 step 12 carry the detail, including the two things re-read that day
— `SYSTEM(91)` already answers `1`, and `SYSTEM(1006)`/`is_nt` has no reader at
all — and the one arm that must **not** be taken, `LOGIN`'s forced
administrator rights on console sessions, which §5.6 rejects.

**THE STANDING COMMANDS.** A cycle begins with a fresh install and ends at the
next source change; `-SkipInstall` is the cheap way to find out whether a change
compiles.

```powershell
C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\cycle.ps1 -SkipInstall
C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\cycle.ps1
C:\Users\dmont\Projects\sd4windows\sdb_ai\sd64\gplbld\post-cycle-elevated.ps1 -TierPrefix sdtiert7 -Account sdacct31 -AclPrefix sdacl11 -ApiPrefix sdapia13 -RoutePrefix sdrt7 -RulesPrefix sdar4 -DelPrefix sddel5
```

**`verify-delaccount` IS NOW IN THE RUNNER** — owner's instruction, 21 Aug 2026,
`-DelPrefix`, ninth step, between `verify-accountrules` and `verify-peerlog`.
It was the last verifier that had to be *remembered*: on `assert-current`'s
`$neverShipped` list, so it never reported the tree stale, and nothing else
reported its absence either. It went a whole phase without running, which is how
Phase 3's `$adopt` marker assertion reached the end of the plan unmeasured.
**Nothing is now run by hand**; the two lines above are the whole cycle.

**Every prefix is single-use** and the defaults in `post-cycle-elevated.ps1` are
spent — §6 has the list. **The install now ends in a visible SD session that asks
for a password; close it (`off`) before the next cycle**, or step 1 refuses.

**THIS FILE WAS COMPRESSED ON 21 Aug 2026 AND IS NOT FINISHED.** It was 11,636
lines against §0.5's 3,500 ceiling; it is now ~7,000. Three blocks went, all
**moved to HISTORY, not deleted** — see the three `## ARCHIVE 21 Aug 2026`
entries there: the 3,500-line LocalSystem exposure record, §7's closed steps
0–2 and 4–6, and the 739-line phase-by-phase header. **Still ~2× the ceiling.**
The next targets are §4 (1,185 lines) and §8 (970), both full of closed
material; **§6 is off limits — rule 4, never cut a trap for size**, and §5 is
the reasoning that dates. Two stale claims surfaced while compressing and were
corrected rather than carried: §7 step 6 still said `APIPORT` defaults off and
the transport was posture B, both reversed by Phase 1.

---

### Phase 3, as built — the parts that are not visible in a diff

**THE MARKER IS A WINDOW IN TIME, NOT A SECOND IDENTITY TEST.** `sdsys/$adopt`
is not ACL'd against anyone — the data tree grants `sdusers` Modify, so any SD
user can create it. It buys them nothing: `K$INTERNAL` still means
`sd -internal`, which `sd.c` forces to SDSYS, which `LOGIN` refuses without an
elevated session. **This reverses the 15 Aug position** — that an elevated
administrator typing `ADOPT` by hand is acceptable — on the owner's ruling of
21 Aug.

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
REACH was narrowed; its IDENTITY is untouched. §WHAT IS OWED carries it.

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
- **Stage 2 (not started).** Move to native Win32 and drop the
  `msys-2.0.dll` dependency: `fork` → `CreateProcess`, `termios` → Console API,
  passwd/group → Windows authentication.

The client library is already at stage 2 — see §5.3.

## 2. Environment

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

**THERE ARE THREE GENERATIONS, AND KNOWING WHICH ONE A LINE CAME FROM IS OFTEN
THE WHOLE ANSWER.** Stated by the repository owner, 15 Aug 2026:

1. **`sdb64`** — <https://codeberg.org/stringdatabase/sdb64>, the unmodified
   Linux version and the active upstream project. **Cloned locally at
   `../sdb64` since 15 Aug 2026**, with `main` checked out and `origin/dev`
   fetched, so both branches are readable without the network:
   `git -C ../sdb64 show origin/dev:sd64/<path>`. It is also a network
   resource, so a machine without the clone loses nothing but convenience.
   **Diffing against it is the cheapest way to attribute a surprise** — it is
   what settled §5.13 and §7 step 7.
2. **`sdb_ai`** — an experimental variant the owner produced by putting `sdb64`
   through **five AI cleaning and validation cycles**. This is why the code
   reads more cleanly than its age suggests, and why those cycles also
   introduce problems of their own.
3. **SD for Windows** — this repository, the port, built on top of `sdb_ai`.

**GENERATION 2 IS TAGGED IN THE SOURCE AND IS WORTH GREPPING FOR.** Every
change from the cleaning cycles carries a `Modified by Composer AI - 2026/06/10`
comment: **226 of them across 73 files** — 53 in `gplsrc`, 20 in `sdsys` —
measured 15 Aug 2026, all bearing that one date. **A line with that marker is
neither upstream nor port work**, so when something surprises you, grep for the
marker before treating it as intended and check the behaviour against `sdb64`.

**Two have already cost real time**: the `VALID_OS_PATH` trap in §6, and the
`SH` administrator gate at `GPL.BP/CPROC:3321` (§4, §7 step 7), which a session
mistook for a Ladybridge decision it would have been wrong to reverse. Several
other things this port has "found" turned out to be inherited from generation 1
rather than introduced — so the check runs both ways.

#### The generation-2 audit — BASIC side, done 15 Aug 2026

All 20 `sdsys` markers read against `sdb64`. **The whole validation layer is a
generation-2 invention**: `!valid_os_name`, `!valid_shell_cmd` and
`!valid_os_path` **do not exist upstream on either branch**, and neither do
their call sites. Three groups:

- **`!valid_os_name` — 8 call sites, and one of them is a live problem.**
  Charset is `A-Za-z0-9._-` only, length `MAX.USERNAME.LEN` = 32
  (`INT$KEYS.H:32`). **No backslash and no space**, so it rejects
  `DOMAIN\user` and any Windows name containing a space. Benign where the name
  is one SD is about to *create* (`CREATEA`, `CREATE_USER`, `SET_PASSWD` —
  refusing an awkward name is reasonable), **questionable where the name
  already exists**: `DELACC:240` and `MODIFYA:103/127` refuse to clean up or
  amend an account whose name it dislikes, which leaves litter nothing can
  address. **And `APISRVR:894` applies it to the API login name before
  authenticating** — §1 makes the API the product's front door and §7 step 6
  owns it. `SDCLIENT:249` does the same for remote logins. **NOT YET MEASURED:
  whether a real API login presents a domain-qualified name.** That measurement
  is what decides whether this is a defect or only a smell; make it before
  touching step 6.
- **`!valid_shell_cmd` rejects `;|&$` + backquote + `<>`**, so **even an
  elevated `SH` cannot pipe or redirect** — `SH dir | findstr x` is refused.
  This belongs with §7 step 7's decision: lifting the administrator gate alone
  would still leave shell-out unable to do the thing §5.13 wants it for.
- **The rest are benign or genuinely good.** Empty-input early returns in
  `IS_GROUP`, `IS_GRP_MEMBER`, `IS_USER`, `USERNAME`, `USERNO`, `ABSPATH`;
  fail-closed on empty password/salt in `SD_KEY_FROM_PW`; file-handle open-state
  tracking in `WRITE_INSTALL_DICTS`. **`LOGIN:172` is a cycle repairing itself**
  — it closes an unterminated banner string an earlier cycle left, which had
  caused `Unrecognised statement`.

#### The generation-2 audit — C side, 15 Aug 2026

**Method, stated because it bounds the claim: every marker was grouped by its
own stated intent, and then each group that can CHANGE BEHAVIOUR was read.**
Groups that cannot — analyser annotations, uninitialised-local fixes — were
classified from their comments and not read individually. So "audited" here
means *every behaviour-changing category*, not every one of the 206 lines.

**The C markers are a different animal from the BASIC ones and are mostly
GOOD.** 206 markers over 53 `gplsrc` files, static-analyser hardening rather
than policy. **Nothing here should be reverted wholesale**; the BASIC side's
verdict does not carry over.

| Category | n | Verdict |
|---|---|---|
| `noreturn` / fall-through annotations | ~24 | cosmetic, safe |
| uninitialised locals on switch-default paths | ~15 | genuine fixes |
| allocation guards ending in `k_error("Insufficient memory…")` | ~15 | **right answer** — loud, immediate, matches the codebase |
| `strtok`→`strtok_r` (`messages.c`, `netfiles.c`, `op_dio2.c`, `sdidx.c`) | 5 | correct — `savep` is function-scoped in every case |
| `message` pointed at a string literal (`messages.c`) | 3 | improvement, and dead code either way (`k_error()` longjmps above) |
| NULL-chunk guards in string padding (`op_str5.c`) | 3 | correct — implicit trailing spaces |
| abort an AK node split on `k_alloc` failure (`dh_ak.c`) | 3 | defensible: orphans a node on OOM vs upstream's NULL-deref mid-split |
| `timeout` read uninitialised (`op_seqio.c`) | 2 | genuine fix — `sq_file->timeout` is where it lives |
| free merge buffers on open failure (`op_sort.c`) | 1 | genuine leak fix |
| `w_addr < 0` always false on an unsigned | 1 | genuine bug fix |
| `groups` allocated every call, never freed | 1 | genuine leak fix |
| **`malloc(1)` → static buffer** | 2 | **DEFECT — fixed** |
| **cleanup gated on the ELSE indicator** | 1 | **DEFECT — fixed** |
| **trigger setup skipped on `k_alloc` failure** | 1 | **flagged, NOT fixed** |

**THE SECOND DEFECT IS THE SERIOUS ONE, AND IT WAS LIVE.** `op_seqio.c`'s
`op_openseq()` had `if (status)` where upstream has `if (process.status)`,
"because `process.status` may be cleared for `ER_RNF` before resources are
freed". It is cleared deliberately, and the two mean different things: `status`
goes on the e-stack as the **ELSE indicator**, while `process.status` is what
`STATUS()` returns — line 597's `ER_RNF; /* Transformed to zero later */` is
that transformation arriving. **So every `OPENSEQ` of a not-yet-existing file —
the normal way to create one — ran the failure cleanup on a successful open**:
`k_free(fvar)` while `fvar_descr->data.fvar` already pointed at it, plus
`k_free(sq_file)` and its pathname, and a decremented `ref_ct`. A use-after-free
handed straight to the BASIC programme, and **silent**, because `process.status`
was 0 by then so the `k_error()` at the foot of the block could not fire.
**Not OOM-gated like the others — this fired on ordinary use.** Reverted to
upstream's test; `make sd` clean.

**FLAGGED, NOT FIXED — `dh_open.c:257`.** On `k_alloc` failure for the trigger
name it silently opens the file **without its trigger**: `DHF_TRIGGER` never
set, so writes bypass the trigger's validation. Same loud-to-silent trade as
the `malloc(1)` defect, but OOM-only, and the right remedy — `k_error()` like
the ~15 other allocation sites, or failing the open — changes open-failure
semantics. **Decide it deliberately rather than in passing.** (The guard also
contains a dead `if (p == NULL) { p = NULL; }`.)

**The pattern to carry forward:** generation 2's failure mode is **turning a
loud failure into a quiet one**, and once — in `op_openseq` — turning a success
into a silent corruption. When a marker adds a guard, the question is never
"is the guard right" but **"what does it do instead, and who can tell?"**

**ONE REAL DEFECT, FOUND AND FIXED.** `ctype.c`'s `CNullString()` and
`op_sdext.c`'s `NullString()` both guarded their `malloc(1)` and returned a
**`static char empty[1]`** on failure. Their results are **owned and freed by
the caller** — `op_sdext.c:258` frees every non-NULL entry of `SDMEArgArray`
in a loop, and both functions feed it (`NullString()` at line 170, and
`Extract()`→`CNullString()` at line 184). So an out-of-memory produced
`free()` of static storage: **heap corruption discovered somewhere else
entirely, in place of upstream's immediate NULL dereference.** Strictly worse,
and on the credential path — line 227 hands that array to `sd_KeyFromPW()`.
**Fixed by returning NULL**, which the release loop already tests for.
`make sd` clean afterwards. **Only reachable when a 1-byte `malloc` fails, so
it is latent rather than live** — but it is the shape to look for elsewhere: a
cleaning-cycle guard that changes who owns a pointer.

**WORTH SENDING UPSTREAM.** This is the one case where generation 2 found a
genuine flaw: `sdb64` has `p = malloc(1); *p = '\0';` with no check at all, so
upstream NULL-dereferences on the same out-of-memory. The fix committed here is
better than both and applies to `sdb64` unchanged. **Written up in
[UPSTREAM_FIXES.md](UPSTREAM_FIXES.md), which is maintained from now on** —
CLAUDE.md carries the rule.

#### What `sdb64`'s dev branch has that we want — reviewed 15 Aug 2026

13 commits, 14 files, `main..origin/dev`, heading for 1.0-3.

**TAKEN.** **`ER_SRVRERR 4100`, `ER_INV_NBR 4101`** into `gplsrc/err.h`,
`gplsrc/sdclilib/err.h` and `sdsys/SYSCOM/ERR.H` — purely additive, no conflict.
Clean rebuild after `rm -f gplobj/*.o`, no warnings.

**FOUND AND DELIBERATELY LEFT ALONE: `SV_EMSG_PAIR` AND `SV_ECONTXT` ARE
TRANSPOSED BETWEEN THE TWO PROJECTS.** `sdb64` dev has `EMSG_PAIR=6,
ECONTXT=7`; the vendored `winsdclilib` client here has them the other way
round. A caller compiled against one header talking to a library built from the
other reads each state as the other one.

**This session renumbered ours to match upstream and then reverted it**, on
learning the client library's provenance (§5.3 below): `sdb64` did not
originate this file. **Which numbering is right cannot be determined from this
repository** and is written up in [UPSTREAM_FIXES.md](UPSTREAM_FIXES.md) #2
with what would settle it. Until then the vendored copy keeps `winsdclilib`'s
values, because a vendored copy stays faithful to its source, and
**`sdsys/SYSCOM/sdclilib.h` deliberately defines NEITHER**, so no BASIC commits
to a numbering by accident. The cost is that our BASIC cannot yet tell a
transport failure from a context error.

**Incidental but useful: these constants are duplicated in FOUR files** —
`gplsrc/sdclilib/sdclient.h`, `sdclilib.h`, `sdclilib.bi`, and
`sdsys/SYSCOM/sdclilib.h`. Changing two of four is what surfaced the conflict,
as a redefinition warning. **`grep -rn "define SV_"` before touching them.**

**ALREADY HERE, INDEPENDENTLY.** Dev's `GetResponse()` fix — return TRUE after
re-fetching the error text rather than reporting a server-side error as a
transport failure — **is already in our stage-2 client**, with a fuller comment
and a better fallback path. Nothing to take. Worth knowing the two trees agreed.

**NOT APPLICABLE.** `_XOPEN_SOURCE` Fedora 44 warnings (Linux); `op_sdpyobj.c`
and `sdext_py.c` (embedded Python, dropped — §5.15); `SDConnectUDS` syslog
(Unix domain sockets).

**CORROBORATION FOR §7 STEP 6d, AND IT IS WORTH HAVING.** Dev comments out the
`getpwnam`/`setgid`/`setuid` block in `SDConnectLocal` — independently reaching
the conclusion step 6d already holds, that these calls make no sense when the
local connection is forked from a running SD. **Upstream also gives a reason we
did not have: it breaks an Apache-spawned process** while working from a test C
program. Our client has no such block, so nothing to do, but step 6d is now
backed by somebody else's field experience.

**OWNER'S CALL, NOT TAKEN.** Dev bumps to **1.0-3** (`revstamp.h`, `$RELEASE`,
`sddefs.h`, `sdclient.h`); we are 1.0-2, and release identity is not something
to change by inference. **`APISRVR` is 2,147 changed lines**, mostly
reformatting with real error checking inside it; ours has already diverged and
§7 step 6 owns it — revisit when step 6 is done, not before, or the reformat
will bury the port's own changes.

**The TCL verb surface is written down**, in
[docs/TCL_VERBS.md](docs/TCL_VERBS.md) — SD's commands against OpenQM 2.6.6,
supplied by the repository owner 14 Aug 2026. Read it before adding or renaming
a verb. The important structural fact it records: **SD has accounts, not
accounts and users.** `CREATE.USER`, `DELETE.USER`, `ADMIN.USER` and
`LIST.USERS` are all deliberately absent, which is why `CREATE.ACCOUNT`
provisions the operating system account itself and why the `CREATUSR` gate was
removed (§7 step 1a).

### The sibling repositories, and what "in sync" means

**Four repositories are in play, all cloned beside this one as of
15 Aug 2026**, and three of them are **maintained**, not merely consulted:

| Path | What it is | Our duty |
|---|---|---|
| `../sdb64` | upstream Linux project, `main` + `origin/dev` | **read-only.** Fixes it needs go in [UPSTREAM_FIXES.md](UPSTREAM_FIXES.md) |
| `../winsdclilib` | the Windows client library, vendored into `gplsrc/sdclilib/` (§5.3) | **maintain.** Holds the client documentation and is to be the basis of an eventual **SD for Windows client installer** |
| `../linuxsdclilib` | the Linux client library, imported 5 Aug 2026 | **keep in sync** with the above where the code is shared |
| this repository | the port | — |

**THE SAME CONSTANT LIVES IN A DOZEN PLACES ACROSS THESE FOUR TREES.** That is
not hypothetical — it is how the `SV_EMSG_PAIR`/`SV_ECONTXT` transposition
survived from 5 to 15 Aug 2026 in three repositories at once. **Before changing
any shared constant, grep all four**:

```sh
grep -rn "define SV_" ../sdb64 ../winsdclilib ../linuxsdclilib . --include=*.h --include=*.bi --include=*.c
```

`sdb64` is the authority for anything it defines first; the client repositories
are the authority for the Windows/Linux transport code they own. **Neither is
simply "upstream" for `gplsrc/sdclilib/`** — see §5.3's round trip.

Two local trees, neither part of this repository, both absent on a fresh
machine, and nothing in the build depends on either:

- **`C:\Users\dmont\Projects\gplsrc`** — original GPL ScarletDME C source.
  Limited value: Ladybridge stripped the Windows code thoroughly. Still useful
  for recovering text mangled by the `qm`→`sd` rename.
- **`C:\Users\dmont\Projects\GPL.BP`** — original ScarletDME BASIC source, 212
  files. **This one is genuinely valuable.** It retains real Windows code that
  this repository's `sdsys/GPL.BP` had stripped: 21 files carry Windows logic
  there against 6 here, and every file present in both lost all of it. See
  §5.4.

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

### Verified by observation

**Entries are claim, decisive measurement, and nothing else.** Every one of
them has a HISTORY entry carrying how it was found and what it cost; that is
where to go when a claim here looks surprising.

**THE API IS REACHED AT ITS OWN PORT — 21 Aug 2026, owner's elevated run on the
11:50:48 install.** `gplbld/verify-apiport.ps1 -Prefix sdapi4`, **13 of 13**.
`netstat` shows `0.0.0.0:4243 LISTENING` and no loopback binding; the client
library carried a real session over it (`remote_connect_test` exit 0) with SCRAM
client-first and client-final sent, no cleartext login, and the password absent
from the 286 bytes on the wire. The installer's half was checked separately:
`SD-API-In-TCP` exists with `RemoteAddress Any`, `api-firewall.ps1` is in
`{app}`, and the shipped `sd.conf` carries `APIPORT=4243`. **A connection from
another machine is still unmeasured** — see the header.

**`DELETE.ACCOUNT`, BOTH DIRECTIONS, THE PROFILE AND THE PHASE 3 MARKER —
21 Aug 2026, owner's elevated run on the 17:18:11 install.**
`gplbld/verify-delaccount.ps1 -Prefix sddel4`, **40 of 40, 0 N/A**, exit 0.
`assert-current` green inside the run, so it describes that install.

**40 IS EVERY `Note` IN THE FILE**, so no check was skipped. That is the claim
the count carries and the earlier runs could not: `sddel1` was 37 and `sddel2`
38, both short because checks did not fire.

- **SD made it → it went, unasked.** `10028` and `10025` shown; Windows account,
  `sdu_sddel4s`, register record and account directory all gone, and **both
  halves of the profile with them** — `C:\Users\sddel4s` and its `ProfileList`
  entry. `10075` not shown, so `delete_user` returned 0 and not 6.
- **SD borrowed it → refused.** `10036` shown, `10028` not; **the Windows
  account, its description AND its profile are all still there.** The SD side
  went anyway — group, register record, directory.
- **Exactly one Y/N, both directions.** The sentinel came back as `5051` from
  inside each run, so nothing else consumed the input. The one question is the
  account *directory* (`6031`); `6029` was never reached.
- **`ADOPT` SPENT THE ONE-SHOT MARKER** — `$adopt` gone after the verb, the
  Phase 3 assertion that had never run. It registered the account, made
  `sdu_sddel4b` and left the description alone, which is what keeps step 5's
  refusal meaningful.

**The profile half is real, not vacuous:** both subjects were given a profile
with `userenv!CreateProfile` first, since an account nothing has signed into
has none. The first attempt (`sddel1`) reported **7 N/A** because that setup
failed — see HISTORY; the checks refused to pass on a subject that did not
exist, which is what the third state is for.

**THE GLOBAL CATALOGUE GATE AND THE TWO LOCKS — VERIFIED 18 Aug 2026, elevated,
on the 11:35:44 install.** `gplbld/verify-catgate.ps1`, **25 of 25**, exit 0.
Decisive rows: `DELETE.CATALOG $LOGIN` refused from a PROGRAMMER account with
`$LOGIN` still 6160 bytes; `CATALOG BP $SDGATE2` refused and `gcat` did not gain
it; `gcat` and `GPL.BP.OUT` both `sdusers:(OI)(CI)(RX)` with no `(I)` entries;
private and local cataloguing both still accepted in the same account; and both
administrator controls — global catalogue and global delete — still work from an
elevated SDSYS session. The unprivileged session is obtained by `LOGTO SDSYS`
then `LOGTO <account>` (`CPROC:2657`), not by credentials, which `sdsshonly`
would refuse. The header carries the reasoning.

**`ApplyDenyLogon` WORKS — VERIFIED 17 Aug 2026, elevated, on the 20:34:04
install.** `sd.iss` `[Run]` entry → `[Code]`, exit code checked. The rights
read back from `secedit /export /areas USER_RIGHTS`:

```
SeDenyInteractiveLogonRight       = *S-1-...-1016,sdsshonly,Guest   PRESENT
SeDenyRemoteInteractiveLogonRight = *S-1-...-1016,sdsshonly         PRESENT
SeDenyNetworkLogonRight           = Guest                           ABSENT
```

**All three rows are wanted, and the third is wanted ABSENT** — setting it
would deny the network logon Win32-OpenSSH authenticates with and break ssh
outright, which is the one thing §5.6.2 exists to preserve.

**The first reading of this said all three were absent, and that was the
CHECK being wrong, not the machine.** See the `deny-logon.ps1` caveat above:
by-name not by-SID, and UTF-16LE. Both were already documented and a
hand-rolled check hit both anyway.

**17 Aug 2026 - `OS.USERS` REFUSES AN UNLISTED ACCOUNT, twentieth session.** On
the 22:43:52 install, unelevated, `SH dir` piped into `sd.exe` as `don`:

```
don is not permitted to use the operating system shell
```

That is the new message 10053 with `@logname` substituted, from `CPROC`'s
rewritten `os.command` gate. **The ACL is verified with it and separately**:
`icacls` shows `sdusers:(OI)(CI)(RX)` with no inherited entries, a write into
`OS.USERS` raises `UnauthorizedAccessException`, and a read succeeds - which is
the exact split `CPROC` needs, since it reads the list in the user's own
process. `secure-osusers.ps1` worked on its first install.

**18 Aug 2026 - THE ADMIT PATH RUNS. `gplbld/verify-osusers.ps1`, 18 of 18
checks, 13 of them decisive, exit 0 on the 07:00:00 install**, twenty-first
session. The whole of §7 step 7 is now observed rather than argued:

| | plain `SH` | `SH` with a pipe |
|---|---|---|
| unelevated, unlisted | refused 10053 | refused 10053 |
| **elevated**, unlisted | ran | refused **5240** |
| unelevated, **listed** | **ran** | **ran** |
| unelevated, unlisted again | refused 10053 | — |

**What each row is for.** Row 3 is the reading nobody had ever taken. Row 4 is
what stops it being read into an install that admits everybody — the shell goes
away again when the record does. Row 2 is the "regresses nothing" claim, and
its two cells carry **different messages**: 5240 is `!valid_shell_cmd` refusing
the pipe, 10053 is the gate refusing the person, so the ban is intact for an
elevated session that is not listed.

**What was scored is a marker FILE each probe creates**, not the message — SD
echoes the command back, so a message can be present without the command having
run. `@LOGNAME` is **`don`, lower case**, and the record is keyed by it.
Unelevated `OPENPATH` of a file that is (RX) to `sdusers` **succeeds**, which is
what makes the design work at all. Transcript in `%LOCALAPPDATA%\SD-verify`;
`OS.USERS` was empty again afterwards, checked directly.

**17 Aug 2026 — CASE INSENSITIVE QUERIES AGAINST A DIRECTORY FILE WORK, and
this is the BEHAVIOUR rather than the flag.** On the 20:34:04 install,
`verify-nocase.ps1` exit 0 with `SYSTEM(91)` answering 1, and then by hand,
treatment and control in one session:

```
SELECT BP  WITH @ID = "sue"   directory file, record is SUE  ->  1 record(s)
SELECT VOC WITH @ID = "who"   dynamic file,   record is WHO  ->  0 record(s)
```

**THE CONTROL IS THE DYNAMIC FILE AND IT IS WHY THIS MEANS ANYTHING** — a
directory file matching across case proves nothing if everything matches. `VOC`
is dynamic with `NOCASE` off and stays case sensitive, so `"who"` finds nothing
while `"sue"` finds `SUE`.

**This is `QPROC:499` running for the first time.** It is gated on
`SYSTEM(91)`, which answered 0 on Windows until this session.

**17 Aug 2026 — DIRECTORY FILES OPEN `DHF_NOCASE`, twentieth session.** On the
20:10:31 install, `gplbld/verify-nocase.ps1` unelevated as SD account `DON`,
exit 0, `assert-current` clean:

```
directory file (BP) reports FL$NOCASE   expected 1   observed 1   PASS
dynamic file (VOC) reports FL$NOCASE    expected 0   observed 0   PASS
```

**BOTH ROWS ARE DECISIVE AND THE SECOND IS WHY THE FIRST MEANS ANYTHING.** Both
read 0 before the change (17:36:21 install), so the directory file moved and
the dynamic file did not — the flag is being read rather than invented, and
`dh_open.c:549` still takes a dynamic file's flags from its own header.

**This is the flag being SET, not the lock collision.** `op_lock.c` has honoured
`DHF_NOCASE` since long before the port; what this port changed is whether a
directory file gets it. A two-session `READU` test would exercise `op_lock.c`,
which is not what changed.

**17 Aug 2026 — `$CRED` IS CLOSED TO ORDINARY USERS, twentieth session.** On the
17:36:21 install, `gplbld/verify-credacl.ps1` unelevated as `GITORLI\don`, exit
0, `assert-current` clean. **The decisive measurement is a write, not a
listing**: `[System.IO.File]::Open(...CreateNew)` on a record inside
`C:\ProgramData\SD\sdsys\$CRED` raises `UnauthorizedAccessException`, and
`icacls` on the same path answers **Access is denied** where the 17:08:32
install printed `GITORLI\sdusers:(I)(OI)(CI)(M)`.

**A listing alone would not have been evidence** — inherited entries, deny ACEs,
group nesting and token filtering all change what one means — which is why the
script asks the filesystem the question an attacker would ask. **And it must be
run UNELEVATED**: the ACL grants `Administrators` Full, so an elevated run
passes however broken the ACL is. The script refuses to run elevated.

**16 Aug 2026 — §7 STEP 1c IS CLOSED: `DELETE.ACCOUNT`'s "SD CREATED IT" BRANCH
HAS RUN, sixteenth session.** `sdacct14` made by `verify-createaccount.ps1
-Keep` from an **unelevated** session at 23:34 — and it **authenticated over
ssh and ran `whoami`**, answering `gitorli\sdacct14`, so the account was real
and carried a password SD set. Fifteen seconds later `DELETE.ACCOUNT sdacct14`
from an unelevated session that had entered SDSYS removed **all four halves**:
Windows user, `sdu_sdacct14`, the account directory, and the `ACCOUNTS` record.

**Which branch fired is established by state, not by reading the message.**
`DELACC`'s three cases are distinguishable by what they leave behind, and only
`case sd.made.it` (`sysmsg(10028)`) deletes the Windows user — 10036 leaves it
and 10037 means it never existed. It existed, and it is gone. Corroborated by
the directory mtimes, which land in DELACC's own order: `user_accounts`
23:34:29, `PSTMP` 23:34:31 (the privileged half going through `!ps_script`),
**`ACCOUNTS` last at 23:34:32**, which is the deliberate ordering that leaves a
failed run re-runnable. **The `10028` line itself was not read by this
session** — it went to the operator's screen.

**16 Aug 2026 — THE LOGIN RULE AND THE COMMAND-LINE GATE, 6 of 6 WITH THE
CONTROL, on the fresh install, sixteenth session.** Unelevated: bare `sd` →
`8 DON` and `sd -ADON` → `9 DON` admitted; `sd -ASDSYS` refused `You can only
log in to your own account - use LOGTO to reach another`; `sd LISTF` and
`sd -start` refused `This command needs an elevated session`, **exit 1**; and
`sd --version` **exit 0**, the control without which a gate that refuses
everything would look correct.

**16 Aug 2026 — `CONFIG` NO LONGER LISTS `CREATUSR`.** 56 lines, running
`CMDSTACK` → `DEADLOCK` straight past where it sat. The user-visible half of
§7 step 1a; the compiled-object check is separate, below.

**16 Aug 2026 — THE INSTALL IS WHOLE AND A SESSION RUNS ON IT, sixteenth
session.** On the install of **22:57:00**, `assert-current` exit 0, `sd.exe`
`7A383F487235134B`: `gcat` **132**, `GPL.BP.OUT` **193**, `gcat/$CPROC`
**25,208**, `$LOGIN` 5,615, `$QPROC` 54,073, `VOC` present, 3,477 files,
`ACCOUNTS/DON` present. Then the part the previous install could not do at all:
an **unelevated** `sd` answered `WHO` → **`2 DON`** and `OFF` → exit 0.
**Both halves matter** — the counts say the bootstrap finished, the session
says the tree works, and the 17:51:35 install passed nothing but a file copy.

**16 Aug 2026 — `CREATUSR` IS GONE FROM THE COMPILED CATALOGUE, not just from
the source.** Installed `gcat/$CONFIG` is 3,153 bytes and does **not** contain
the string `CREATUSR`, while it does contain `DEADLOCK` — the control, without
which the search proves nothing.

**16 Aug 2026 — THE LOGIN RULE, 5 of 5, eleventh session, on the fresh
install.** Written 15 Aug and never run until now. `sd -internal` → `12 SDSYS`,
so the bootstrap and install door still reaches SDSYS — the one to check before
anything else, because nothing can be installed without it. A bare elevated
`sd` → `13 DON`. `LOGTO SDSYS` from there → **`14 SDSYS from DON`**, which names
where it came from and is the decisive form. `sd -ASDSYS` → **`You can only log
in to your own account - use LOGTO to reach another`**, sysmsg(10051), and it did
not reach SDSYS.

**16 Aug 2026 — `LIST.GRANTS` ON A FRESH INSTALL, eleventh session.** The CR fix
had only ever been seen on a hand-recompiled `OS_GROUP`. `LIST.GRANTS SDACCT9`
with two members printed `'   don'` and `'   sdacct9'` **adjacent, neither
carrying a CR and no blank line between them**, read back with control
characters made visible rather than by eye. `GRANT`/`REVOKE` round-tripped
against `Get-LocalGroupMember` both ways, each printing the sign-out line.

**16 Aug 2026 — `CREATE.ACCOUNT`, 16 of 16 on a fresh install, eleventh
session.** `verify-createaccount.ps1 -Account sdacct9` exit 0: both halves of
what it makes, the ssh-only branch, and all three logon measurements —
`LogonUser` INTERACTIVE **refused 1385**, NETWORK_CLEARTEXT **admitted**, ssh
**admitted**. `sdacct9` is left in place, password `Sd-Test-1`.

**16 Aug 2026 — THE UNINSTALLER REMOVES THE SERVICE, test (e), eleventh
session.** Service gone (`sc query SD` → 1060), `C:\Program Files\SD` gone, and
**`C:\ProgramData\SD` kept, 3,486 files** — which is the other half of the test:
the user's database is `uninsneveruninstall` and must survive.

**16 Aug 2026 — NO REGRESSION FROM THE Win32 SEMAPHORES, eleventh session.**
The IPC change rewrote the layer every SD session depends on, so the morning's
tests were re-run against it on the same install: **11 of 11** on the login
rule, `GRANT`/`REVOKE` and `LIST.GRANTS` (still no CR, still no blank line),
and **16 of 16** on `CREATE.ACCOUNT` for `sdacct10`, ssh-only branch and all
three logon measurements included.

**16 Aug 2026 — THE SERVICE WORKS, AND AN ORDINARY USER REACHES IT, eleventh
session, on a fresh install.** The whole chain, one install: the service
`Running`, `sdwind` **alive at t+30s** — past the ten-second mark that had
killed it every previous time — all six `Global\sd_sem_716d0302_*` openable,
and `adopt-account.log` reading **`don now has an SD account`** with
`ACCOUNTS/DON` present, which closes §7 step 1f.

**Then the half that had never been tested, and it is the one the requirement
rests on.** From an **unelevated** session-1 process (`GITORLI\don`, elevated
`False`, session `1`): all six semaphores opened, and a bare `sd` answered
**`2 DON`** — an ordinary user logged in to an SD started by a LocalSystem
service in session 0, with nobody having typed anything. **The restart has now
been measured and it fails — see the entry below; this one still stands for
everything short of a reboot.**

**16 Aug 2026 — THE SERVICE DOES NOT SURVIVE A RESTART, AND WHY, twelfth
session, on the same install.** Machine rebooted 10:31:21; `Get-Service SD`
`Stopped`/Automatic, no `sdwind`, SCM event 7024. From
`C:\ProgramData\SD\sdsvc.log`: shutdown 10:31:05 `sd -stop` **exit 1**, boot
10:31:30 `sd -start` **exit 1 one second later**, then the service's own
recovery `sd -stop` **exit 0** at 10:31:41.

**The segment survived the reboot, and the decisive measurement is a directory
mtime.** `C:\ProgramData\SD\shm` has LastWriteTime **10:31:41.396** — the
recovery `sd -stop`. A directory mtime moves only when an entry is added or
removed; nothing was added, because `sd -start` exited one second in, before
`bind_sysseg()`, which unlinks after itself on failure (`sysseg.c:332`,
`:343`). So an entry was **removed at 10:31:41**, and was therefore present at
boot. One second also excludes both ten-second waits — the daemon poll and
`sem_open`.

The rest is single-code-path rather than observed, because `sdsvc-sd.log`
captured nothing: `sd -stop` exit 1 can only be `shm_unlink()` failing with
errno ≠ ENOENT (`sysseg.c:785`, the one `return FALSE` in `stop_sd()`), and a
one-second `sd -start` failure over a present segment with no daemon is
`SD_WRECKAGE` (`sysseg.c:506`). Header item 1 has the fix options; §6 has the
trap.

**16 Aug 2026 — §7 STEP 1f, BY THE INSTALLER RATHER THAN BY HAND, twelfth
session.** `adopt-account.log` on the 10:23 install reads `don now has an SD
account` and `don keeps the Windows sign-in rights it already had`, and
`ACCOUNTS/DON` exists. Read off the installed tree, not re-run.

**16 Aug 2026 — SD WILL NOT RUN UNDER LocalSystem IN SESSION 0 ON POSIX
SEMAPHORES, test (a), eleventh session. Fixed by the entry above; kept because
it is why the Win32 change exists.** Header item 1 carries the reasoning and what is left to
decide. The measurements: `sdwind` dies at **~10s** started by the service and
**~10s** started by a scheduled task as SYSTEM with no service anywhere, and is
**alive at 40s** started from an interactive elevated session — one install,
one sitting. It dies saying **`sdwind: Error 116 getting semaphores`**, errno
116 = `ETIMEDOUT`, because the probe `sem_open` at `sdsem.c:82` **blocks about
ten seconds and times out**. Both processes in that probe were SYSTEM in
session 0, so it is **not** a cross-session problem.

**16 Aug 2026 — AND THE SERVICE NO LONGER LIES OR LEAVES WRECKAGE, eleventh
session.** Same install. It reports `STOPPED` with `sdwind.exe has GONE after 5
seconds` rather than `Running` over a dead SD, and `sd -stop` behind the failed
start leaves **`shm` empty** — after which `adopt-account` reports the honest
`SD has not been started` instead of `Error 116 getting semaphores`. Before
this, a failed service left every later `sd` on the machine broken.

**15 Aug 2026 — §7 STEP 5: GRANT, REVOKE AND LIST.GRANTS WORK, 16 of 16 on a
fresh install, tenth session.** Every SD-side claim checked against
`Get-LocalGroupMember` afterwards, because the point of the step is that SD
writes nothing to its own record: `GRANT SDACCT8 TO don` → `don may now use
account SDACCT8` **and don in `sdu_sdacct8`**; `REVOKE` → out of it again.
Both print the sign-out line (5c). The idempotent paths say so rather than
implying they acted — a second `GRANT` answers `already a member`, a second
`REVOKE` answers `has not been granted`. Refusals: unknown account →
`Account not registered in ACCOUNTS file`; unknown user → `There is no Windows
account named nosuchuser`, **and it did not add them**. **`LIST ACCOUNTS`
still works** with the `Granted to` column gone, which is what 5d's ordering
was for.

**Two defects found by running it that compiling could not have shown.**
`LIST.GRANTS` printed a blank line after every member: PowerShell ends lines
CRLF, the capture splits on the LF, and `trim()` removes spaces but **not the
carriage return**. It reads as untidiness and is not — a name carrying a CR
fails `!valid_os_name`, so `OS_GROUP`'s own promise that a `LISTMEM` name can
go straight back to `DELMEM` was false. Fixed by `convert char(13):char(10)`
before the trim, **verified on a hand-recompiled `OS_GROUP` rather than a
fresh install** — re-check it on the next one, it is one command.

**And the installer failed to give the installing user an account**, reporting
`code 3` — the `adopt-account.ps1` race now in §6. It had never fired before
because the machine had never been loaded enough to lose it.

**15 Aug 2026 — §7 STEP 2 RAN ON A SECOND MACHINE, tenth session. THE INSTALL
IS SELF-CONTAINED AND THE RDP REFUSAL IS MEASURED.** VirtualBox guest
`VIRTUAL`, Windows 11 Pro, bridged at 10.0.0.143, from snapshot `Before SD
install`. **No MSYS2, no `gplsrc`, no development tree** — which is the whole
reason the step existed, because an accidental dependency on any of them can
only show up here.

**The install is byte-identical to the build machine's**: `sd.exe` sha256
`81594E79CC2B560C`, and **19 / 3,456 / `gcat` 130 / `GPL.BP.OUT` 191** — the
same four counts. `sd -start` exit 0, `sdwind` up, and **`COUNT VOC` answered
`431 record(s) counted`**, which is the number that says the database is whole
rather than merely present. `adopt-account.log` shows the installer's account
step ran there too: `don now has an SD account`, `don keeps the Windows sign-in
rights it already had` — the lockout fix on a machine that never had the bug.

**RDP, control then treatment, which is the half one machine cannot do.**
`CREATE.ACCOUNT USER sdacct7` on the guest put it in `sdusers`, `sdu_sdacct7`
and `sdsshonly`, not `Administrators`, saying `sdacct7 may sign in over ssh
only`. Then from the host, same target, same port, same firewall rules,
differing only by `sdsshonly` membership:

- **control — `VIRTUAL\don` → ADMITTED.** Without it a refusal is
  indistinguishable from RDP being off, which is not hypothetical: three
  earlier attempts failed for rig reasons alone.
- **treatment — `VIRTUAL\sdacct7` → REFUSED, `The connection was denied because
  the user account is not authorized for remote login`.** That wording is
  `SeDenyRemoteInteractiveLogonRight` specifically, **not** a credentials
  failure, which is the distinction that makes it evidence.

`LogonUser` locally on the guest agreed on the two types it can test —
INTERACTIVE **refused 1385**, NETWORK_CLEARTEXT **admitted**. **It cannot test
the RDP path at all**: there is no logon type 10 for `LogonUser`
(`RemoteInteractive` is an LSA audit value), and asking for one returns
`87 ERROR_INVALID_PARAMETER`. A tenth-session probe row claimed otherwise and
was wrong. **So RDP genuinely required the second machine** — the step was right
to insist.

**15 Aug 2026 — AN ssh SESSION LANDS INSIDE SD (header 2b), tenth session.**
`ssh sdacct6@localhost whoami` against the fresh install answered **SD's banner
and a `:` prompt, exit 0 — `whoami` never ran**. That is the decisive form:
sshd discards the client's command and runs SD. `verify-createaccount.ps1`
deliberately accepts *either* proof of admission, because it must run either
side of `allow-ssh-groups.ps1`, so it cannot make this measurement — it was made
separately. `CREATE.ACCOUNT USER sdacct6` was **16 of 16** on the way past,
including the ssh-only branch and the three logon measurements: `LogonUser`
INTERACTIVE **refused 1385**, NETWORK_CLEARTEXT **admitted**, ssh **admitted**.

**And scp is dead, measured rather than asserted.** `scp` to that account
**exit 255**, `Received message too long` / `Ensure the remote shell produces no
output for non-interactive sessions` — which is what forcing a command that
prints a banner does. The `changelog` already said so; now it is observed.

**15 Aug 2026 — `SH` SETS `SD_SESSION` AND `sd` REFUSES IN THE SHELL IT HANDS
BACK (header 2c), tenth session.** Elevated live session on the install:
`SH Get-ChildItem Env:SD_SESSION` printed **`SD_SESSION 1`**, so `op_sh.c:312`
is observed and not just `sd.c`'s half. The refusal was then watched on **both**
child paths — `OS.EXECUTE 'sd --version' CAPTURING` (`sh(TRUE)`) and
`OS.EXECUTE 'sd --version'` with no CAPTURING (**`sh(FALSE)`, the identical path
the `SH` verb takes**) — each answering `SD is already running in this session -
type EXIT to return to it.`

**Why it took three runs, and it is a testing trap not a defect:**
`SH sd --version` in the piped elevated session produced **no output at all**.
The refusal is `fprintf(stderr, ...)` at `sd.c:301`, and the capture took only
stdout. `Get-Command sd` inside the same child resolved to
`C:\Program Files\SD\usr\bin\sd.exe`, so it was never a PATH failure.
**`CAPTURING` sees it because `op_sh.c:281-282` dup2s the pipe onto BOTH 1 and
2**; a bare `2>` on the `sd` invocation does the same for the uncaptured form.

**15 Aug 2026 — AN ORDINARY USER'S PROGRAM REACHES THE OS, IN THE SAME SESSION
WHERE `SH` IS REFUSED. Owner's question, tenth session.** One **unelevated**
session on the install, with the control first: `SH echo ...` at the `:` prompt
→ **`Command requires administrator privileges`**; then a program compiled `0
error(s)` in `don`'s own BP running `OS.EXECUTE 'echo SDMARKER-OK' CAPTURING
CAP` → **`SDMARKER-OK` captured and printed back**. The control is what makes it
mean anything: same session, same user, one route refused and the other open.

**So the gate does not break programs, and §7 step 7's premise was wrong** —
see the correction there. `OS.EXECUTE ... CAPTURING` is its own BASIC statement,
`BCOMP:9647` → `OP.SHCAP` (`0xCF99`, `opcodes.h:505`) → `op_shcap()` →
`sh(TRUE)`, and **neither `kernel(K$ADMINISTRATOR,-1)` nor `!valid_shell_cmd`
is anywhere on that path**. Both live only in `CPROC`'s `os.command:` handler.
**The form that does break is `EXECUTE 'SH ...' CAPTURING`**, which goes through
TCL and therefore through the gate; the statement used directly does not.

**15 Aug 2026 — THE COMMAND LINE IS CLOSED TO AN UNELEVATED SESSION, AND SD
WILL NOT START INSIDE ITSELF. CONFIRMED ON THE INSTALLED BINARY, ninth
session.** 19 of 19, unelevated, against `C:\Program Files\SD\usr\bin\sd.exe`
**dated 09:58 and hash-identical to `bin/sd.exe`** — the fresh install, so this
is the shipped gate and not only the build's. All twelve guarded switches
(`-start -stop -restart -cleanup -d -l -m -u -suspend -resume -internal
-k ALL`) and the bare commands `LISTF` and `WHO` refused with `This command
needs an elevated session`, **exit 1**; `--version` answered `String Database
(sd) Version 1.0-2 64 Bit`, **exit 0**, which is the control — a gate that
refuses everything proves nothing. With `SD_SESSION=1` set, all four forms
tried including `--version` answered `SD is already running in this session`,
so the guard is genuinely before the gate as `comlin()` intends.

**Still not watched: the marker being set by a real `SH`**, which needs an
**elevated** live session for the reason in the next entry; only `sd.c`'s half
of that pair has run.

**15 Aug 2026 — `SH` IS ALREADY RESTRICTED, AND IT REFUSES AN ORDINARY SD
USER.** Observed while trying to close item 2c: from an unelevated session
standing in `DON` on the installed system, `SH cmd /c echo ...` answered
**`Command requires administrator privileges`** (`sysmsg(2001)`) and the
session carried on to `OFF`. The gate is **`GPL.BP/CPROC:3321`**, in the
`os.command:` handler — `if not(kernel(K$ADMINISTRATOR, -1))`, added by
"Composer AI - 2026/06/10" together with `valid_shell_cmd`. `K$ADMINISTRATOR`
is seeded from `IsElevated()` (§7 step 0), so **`SH` needs an elevated session,
not merely an administrator's account.**

**Two things follow, and the second is a correction.**

- **WHAT REFUSES TODAY IS AN AI CLEANING-CYCLE ADDITION, NOT THE LINUX
  PREVENTION AND NOT A PORT DECISION.** Established 15 Aug 2026 after the owner
  said the Linux block had been reversed early on: **the original ScarletDME
  `CPROC` has no gate here at all** — `C:\Users\dmont\Projects\GPL.BP\CPROC`'s
  `os.command:` goes straight to `os.execute`, no `kernel(K$ADMINISTRATOR,-1)`
  and no `valid_shell_cmd`. The gate's own comment dates it **2026/06/10**,
  months before the port, and `git log -S` puts it in this repository at the
  **initial import** (`f9edab0`). **`SH` and `!` have been in `VOC_TEMPLATE` as
  `V`/`OS` since that same import** and were never removed here. So this is §2's
  warning firing exactly as written — check `sdb64` before assuming a difference
  is deliberate — and it is the second instance after `VALID_OS_PATH`.
  **§7 step 7 is therefore NOT a search for a Linux block**: whatever Linux did,
  what stands in the way on Windows is one AI-authored `if`.
- **CORRECTION to 15 Aug's "an SD account DOES have a shell".** True only of an
  **elevated** session. An ssh session cannot be elevated (§4, local-only by
  design), so **an ssh user can never reach `SH`, and `ForceCommand` does keep
  them inside SD** — the hole that correction described is not reachable by the
  people it was worried about. Whoever can use `SH` is at an elevated console
  and could run anything anyway.

**Not watched, and it is what item 2c still needs:** `SH` succeeding from an
**elevated** session, and `SD_SESSION` being set in the shell it returns
(`op_sh.c:312`).

The matrix is `verify-gate.ps1`, written this session and **not tracked** — it
lives in the session scratchpad. Two things in it are the reusable part:
`--version` as the control, and **stderr redirected to a file rather than
`2>&1`**, because PowerShell 5.1 wraps a native exe's stderr in an ErrorRecord
and `$ErrorActionPreference = 'Stop'` then aborts on the first refusal — the
exact line the test exists to observe (§6, the PowerShell traps).

**15 Aug 2026 — §7 STEP 1f IS CLOSED ON A REAL INSTALL.** The installer's
`[Code]` step made the account: `ACCOUNTS` holds `DON` and `SDSYS`,
`user_accounts\don` exists, `sdu_don` has him, `sdsshonly` is **empty** — the
lockout fix holding on the installer's own path — and `adopt-account.log`
records `AppDir=C:\Program Files\SD`, `don keeps the Windows sign-in rights it
already had`, and the daemon put back as it was found. The install underneath
it is the corrected one: **3,455 files, `gcat` 130, and the installed
`gcat/$LOGIN` carries the new banner** — the first time the repository's own
catalogue has been on this machine.

**15 Aug 2026 — `ADOPT` RAN FOR THE FIRST TIME, AND IT LOCKED THE OWNER OUT OF
HIS OWN CONSOLE.** `adopt-account.ps1` against the install, elevated:
`don now has an SD account` — `ACCOUNTS/DON` written, `sdu_don` created, VOC,
`$HOLD`, `$SAVEDLISTS`, BP and private catalogue made. **And `don may sign in
over ssh only`**: the verb put him in `sdsshonly`, which carries both deny-logon
rights, so the next sign-out would have shut him out of the console and RDP.
Membership confirmed with `Get-LocalGroupMember` and removed by hand. §6 has the
fix and the rule behind it. Unelevated first, as a control: the same script was
refused with `sysmsg(10002)` and changed nothing.

**AND THE FIX IS VERIFIED, BY THE SAME VERB MINUTES APART.** `IS_GRP_MEMBER`
and `CREATEA` recompiled on the install, `0 error(s)` each, then
`ADOPT sdadopt1` — a throwaway Windows account — printed **`sdadopt1 keeps the
Windows sign-in rights it already had`** and `Get-LocalGroupMember sdsshonly`
now lists only `sdacct4`, `sdacct5`: **`don` restricted before the fix,
`sdadopt1` not after it**, nothing else changed. `sdusers`, `sdu_sdadopt1`,
`ACCOUNTS/SDADOPT1` and `user_accounts\sdadopt1` all correct. Two more things
fell out: `ADOPT` on a name with no Windows account refused with
`Invalid user name`, which is its other untested branch, and **`sd` typed
unelevated put `don` in his own account — `WHO` answered `5 DON`**, so the
`sdusers` gate still admits him through the rewritten `IS_GRP_MEMBER`.

**15 Aug 2026 — §7 STEP 1d HOLDS ON THE INSTALLED BINARY, NOT JUST THE BUILD.**
All four branches against `C:\Program Files\SD\usr\bin\sd.exe`, **run twice**:
the first pass had a daemon restarted by hand in the middle of it, so it was
redone start to finish from one unelevated session with every pid accounted
for. Second pass: `sd -start` on a live daemon → exit 1, `SD is already started
- sdwind is running as pid 7388`, `Get-Process` agreeing on **7388**, so the pid
translation works in the install too; daemon killed with the segment left →
exit 1, `SD did not shut down cleanly ... Run sd -stop`, and the seven `shm`
files **still there**, since clearing them is the user's decision; `sd -stop` →
exit 0, `shm` empty, no spurious warning; `sd -start` → up as pid 5500. The
14 Aug binary answered `SD is already started` to the killed-daemon case and did
nothing.

**The fifth branch too — the `EPERM` warning, on the install, with the daemon
started elevated by the owner and `sd -stop` run from an ordinary session.**
`sd -stop` exited 0, emptied `shm`, and printed `Warning: sdwind (pid 4620) is
still running.` with the privilege reason and the `Stop-Process -Id 4620 -Force`
command; `sdwind` was indeed still there afterwards. Corroborated the way §4
asks: `Stop-Process` from that same unelevated session was **refused, Access is
denied**, and the daemon measured **High integrity** (`S-1-16-12288`) against
the session's Medium (`S-1-16-8192`). **So the seventh session's claim stands
and the doubt raised against it was mine, not the file's** — the daemon killed
unelevated earlier that morning cannot have been the elevated one.

**15 Aug 2026 — THE BOOTSTRAP REFUSES AN UNELEVATED WINDOW, BEFORE DOING
ANYTHING.** Four unelevated runs: a **nonexistent** `--sysdir` drew the
elevation refusal and not `no such sysdir`, so the check is genuinely first;
`stage.py --bootstrap` left no staging directory; `--help` works on both;
`stage.py` without `--bootstrap` reached its `objdump` check, so plain staging
stays ungated. `os.getgroups()` here carries no 544 (§5.6.1). **The elevated
half ran too**, 06:31: both gates passed in an elevated window and the whole
bootstrap ran behind them — `SECOND.COMPILE` 0 errors throughout, 3,291 files
staged. What that run also exposed is the `ACCOUNTS/SDSYS` trap in §6.

**14 Aug 2026, seventh session — the same §7 step 1d branches on the repository
build, against wreckage the machine supplied itself.** Superseded by the entry
above, which re-ran all of it on the installed binary; compressed on close to
the two things that entry does not carry.

- **The control is why the fix works at all.** The old binary answered
  `SD is already started` against a dead daemon — `sdsem.c:86`, **not** the
  `bind_sysseg` string §7 step 1d named, because `get_semaphores(TRUE)` runs
  first. A fix confined to the two places the step named would have changed
  nothing the user sees. §7 step 1d records the lesson.
- **A defect the fix cannot reach:** with the segment unlinked under a live
  daemon, `sd -stop` reports success, exit 0, and leaves `sdwind` running. §6.

**§7 STEP 1c RUNS — 14 Aug 2026, seventh session, elevated console.** All five
programs compiled `0 error(s)`, catalogued, no `is not assigned a value` (so
`K$INTERNAL` and messages 10036–10039 resolve).

- `CREATE.ACCOUNT USER don` → `Windows account don already exists.  SD accounts
  create their own OS account`. The explicit refusal, on the account it exists
  to protect. Was `Create User Failed, OS Error: 1`.
- `DELETE.ACCOUNT sdacct1` → directory prompt, then `Windows account sdacct1
  does not exist, nothing to delete`; no group warning, `sdu_sdacct1` having
  already gone. **First run of `DELETE.ACCOUNT` in this codebase.**
- Checked after, not assumed: `user_accounts\sdacct1` gone, `ACCOUNTS` down to
  4 accounts + SDSYS, and `sdacct4`/`sdacct5` users and `sdu_` groups
  untouched.

**Measurements behind step 1c**, PowerShell rather than BASIC:

- **`/etc/passwd` and `/etc/group` are absent under both roots** the MSYS2
  runtime can use, while `getent passwd` returned `don` with his SID and
  `Get-LocalGroup` returned `sdu_sdacct5` with its SID, from the same machine.
  That is the whole basis of the three-helper trap in §6.
- **The `SD account` marker is real, and SD wrote it.** `Get-LocalUser sdacct5`
  returns a description of exactly `SD account`, 10 characters, stamped by
  `CREATE_USER` on 14 Aug 2026; `don`'s is empty. **This also proves a quoted
  value containing a space survives SD's `os.execute` path**, which is what
  `!is_sd_user` depends on and what nothing had previously shown.
- **The three answers `!is_sd_user` needs are distinct on real accounts**, run
  as PowerShell against this machine: `sdacct5` → 0 (SD's), `don` → 1 (**not**
  SD's, so `DELETE.ACCOUNT` would refuse to touch the machine
  administrator's login), `sdacct1` → 2 (absent — the half-removed case).
  `is_user`: `don` → yes, `sdacct1` → no. `is_group`: `sdu_sdacct5` → yes,
  `sdu_sdacct1` → no.

**14 Aug 2026, SIXTH SESSION — STEP 0, COMPRESSED TO ITS CONCLUSIONS** under §0
rule 5. HISTORY carries the working detail; these are the claims and what
decided them.

- **`LOGIN` and `CPROC` both compile, `0 error(s)` each, and are catalogued.**
  `gcat/$LOGIN` moved to 18:54:15 and 5,319 bytes — the pcode checked as
  written rather than as reported. Neither had been through a compiler before.
- **The new `LOGIN` is what runs**, dated exactly: the `LOGIN` compile printed
  `Warning: account SDSYS has no password set.` and the `CPROC` compile one
  command later did not, that line living in the deleted
  `authenticate.account`. `CPROC` then compiled *through* the new `LOGIN`, so
  the `sdusers` gate admits a member and `K$FORCED.ACCOUNT` reaches SDSYS.
  Only one warning, structural and not from the edit (§6, `IS_INSTALL`), and no
  `is not assigned a value` lines, so both pass the ERRGEN gate.
- **THE REFUSALS, which are the part that proves it.** From an **unelevated**
  session against the newly installed binaries: `sd` refused with
  `Account DON not in register` (`sysmsg(5018)`), `sd -ASDSYS` refused with
  `SDSYS Account access is restricted to privileged users` (`sysmsg(10002)`),
  while `sd -internal BASIC ...` **elevated** worked twice. An hour earlier the
  first of those put a machine administrator straight into SDSYS. **And
  `sysmsg(10002)` fired for the first time in this codebase's history.**
  **Both were then reproduced by the repository owner in a plain `cmd`
  console**, which mattered because the runs above went through a pipe and §6
  records a piped session as not equivalent to a real one. Incidental and worth
  keeping: extra words on those command lines were **ignored**, so a user
  refused at the door cannot smuggle a command in as an argument.
- **§5.6 IS COMPLETE — ALL FIVE RULES, BOTH `LOGTO` PATHS**, over ssh as
  `sdacct5`, a normal non-administrator account: `sd` gave a `:` prompt with
  nothing asked, `who` confirmed `3 SDACCT5`, `LOGTO SDSYS` was refused by the
  elevation gate (**an ssh session cannot be elevated** — the local-only
  property, tested rather than argued) and `LOGTO SDACCT1` by the restored
  `ACC$GROUP` test. **The two refusals come from different code**, which is why
  both were run; between them they cover every branch the session changed.
- **`CREATE.ACCOUNT` still passes 16 of 16** under the elevated-only gate,
  re-run as `sdacct3`. Its ssh-only restriction holds by the three decisive
  measurements: `LogonUser INTERACTIVE` refused 1385, `NETWORK_CLEARTEXT`
  admitted, ssh with the password SD set admitted. **That run does not test SD
  login and is easy to read as if it does** — all sixteen checks are
  Windows-side. Ignore `Command not found` in its section 1; the script's own
  header records it as a stray stderr artefact of how passwords are fed in.

**The foundations, observed 13 Aug 2026.** Nothing since has contradicted any
of them, and re-verifying them is not worth a session's time.

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

**`IsAdmin()` works in the linked binary, in both directions**, and that is
worth restating rather than filing: `sd -start` refused with "Command requires
administrator privileges" while the group was absent and got past the check
once built against a group the token holds. The probe recipe in §6 is the only
way to see this system as a non-administrator on a machine whose account is one.

#### The installed system

- **A GENUINE FIRST INSTALL WORKS, AND THE FILES WERE COUNTED** — 14 Aug 2026,
  on a machine cleaned first, with the installer rebuilt from the tracked
  `gplbld/sd.iss`. **3,264 files** under `C:\ProgramData\SD\sdsys` against a
  broken run's 16, 129 `gcat` entries, 11 `GPL.BP.OUT`, and a `Compare-Object`
  of every staged path against every installed one reporting **no differences
  in either direction**. It then ran: `COUNT VOC` **431**, `LIST ACCOUNTS`
  giving `Pathname: C:\ProgramData\SD\sdsys`, `WHO` `3 SDSYS`. Everything else
  the installer owns was confirmed on the same run — `sdusers` with
  `GITORLI\don` in it, `user_accounts`/`group_accounts`/`shm`, exactly one PATH
  entry, no `gplbld` in the data tree, `sd.conf` present.

- **CORRECTED 14 Aug 2026, and the lesson outlives the fix.** An earlier claim
  that the installer worked was true of the **upgrade** path only. A genuine
  first install **produced a broken database**: `Check: DataTreeAbsent` is
  evaluated *per file*, so the first file created the directory, every later
  evaluation answered False, ~3,260 files were silently skipped — and **Setup
  still exited 0**. `InitializeSetup` now caches the answer once. **An install
  test that does not COUNT what was installed proves very little.**

- **THE INSTALLED SYSTEM RUNS AS AN ORDINARY USER** — 14 Aug 2026 after a
  reboot, from a normal unelevated window with nothing set in the environment:
  `sd -start`, `COUNT VOC` 431, `WHO`, `sd -stop`, `sdwind` appearing and
  going. The first time SD was used the way a user would use it, and it closes
  three things: **§5.6.1 in the real world**, `IsAdmin()` having admitted an
  administrator who had not elevated; **§5.7's ACL model from the user's
  side**, the token now carrying `sdusers`; and **the sign-out requirement**,
  which is real and sufficient — the same session had been refused on every
  path inside `C:\ProgramData\SD` before the reboot, and nothing else changed.

  **What it does not show:** `sd -start` had to be typed. An installed system
  does **not** come up on boot — there is no service (§5.7) — so after every
  restart someone must start SD by hand. That is now the most visible gap in a
  system that otherwise installs and runs.

- **The upgrade path works too, and it is a different path.** Over an existing
  data tree, `/VERYSILENT`: the `sdsys` tree **does not appear in the install
  log at all** and the database was untouched; the four MSYS2 DLLs and
  `etc\fstab` land in `usr\bin`, and an `Uninstall` key puts SD in Settings.

- **An installed system finds its configuration with nothing set in the
  environment** — reading `C:\ProgramData\SD\sd.conf` through `%ProgramData%`.

- **The uninstaller runs, and keeps the data.** `/VERYSILENT`, exit 0:
  `C:\Program Files\SD` and the Settings > Apps entry removed,
  **`C:\ProgramData\SD` left completely intact**. It used to leave the PATH
  entry behind, which Inno cannot undo by itself because `[Registry]` appends
  with `olddata`; **fixed** by `RemoveFromPath` at `usUninstall`. It leaves the
  `sdusers` group deliberately — a kept data tree is ACL'd to it.

- **The daemon starts on an installed system, and it is called `sdwind`.** It
  had **never** started from an install. `start_sd()` asks `exe_directory()`
  and launches it from beside the running executable, so the two cannot drift
  apart: `sd -start` from `C:\Program Files\SD\usr\bin\sd.exe` left
  `sdwind.exe` running out of that directory, while `<sysdir>\bin` held only
  `pcode, pcode.old` — the old path could not possibly have worked. The
  daemon's own `check_lost_users()` had the same defect and is fixed with it,
  not separately verified. **Why it was silent is the trap in §6.**

- **The ACLs are right, and this time that was checked from the outside.** The
  data tree carries exactly `GITORLI\sdusers:(OI)(CI)(M)`,
  `BUILTIN\Administrators:(OI)(CI)(F)` and `NT AUTHORITY\SYSTEM:(OI)(CI)(F)`,
  with no `BUILTIN\Users` — and an unelevated session whose token does not carry
  `sdusers` was refused on every path inside `C:\ProgramData\SD`, so the lockout
  is real and not just a listing. **`Test-Path` on the directory itself still
  answers True** (§6). Check the contents, or you will conclude the ACL never
  applied.

- **OpenSSH Server installs, and `sshd` runs** — `Installed` after a reboot, so
  the corrected `Add-WindowsCapability` line works and the brace bug (§6) was
  the whole of it. `install-ssh.ps1` then reported `sshd is Running,
  StartType=Automatic`, 2 listeners on port 22, the firewall rule enabled, and
  `C:\ProgramData\ssh\sshd_config` created — which sshd writes on first start,
  and is the earliest point at which `AllowGroups` could be edited into it.

  **And it exposed an installer defect that is now fixed.** The capability
  installed but the **service did not exist until after a reboot**, so a step
  running `Add-WindowsCapability`, `Set-Service` and `Start-Service` in one
  breath reported total failure for a success needing a restart.
  `install-ssh.ps1` now **exits 2 for "restart required"**.

- **`sd.iss` compiles with all of the above in it** — `ISCC.exe` exit 0. That is
  the *only* claim: see §4 Unverified for what compiling does not show.

#### Elevation, and who may reach SDSYS

- **WINDOWS DOES LIMIT WHO MAY ELEVATE, AND `Administrators` IS THE SUDOERS
  FILE.** Measured 14 Aug 2026, fifth session, on this machine's live policy.
  **This is the measurement §5.6's reversal rests on**, and it contradicts the
  belief that sent the port down the password route:

  | Setting | Value | What it means |
  |---|---|---|
  | `EnableLUA` | 1 | UAC on, tokens filtered |
  | `ConsentPromptBehaviorUser` | 3 | **a standard user is prompted for an ADMINISTRATOR's credentials** on the secure desktop — it cannot elevate as itself |
  | `ConsentPromptBehaviorAdmin` | 5 → **now 0**, see below | an administrator gets a consent prompt only |
  | `LocalAccountTokenFilterPolicy` | **not set** | the default remote restriction applies — see below |
  | `FilterAdministratorToken` | not set | — |

  **The UAC slider moves, so read it rather than remembering it.** The sixth
  session recorded `ConsentPromptBehaviorAdmin` at **0** and
  `PromptOnSecureDesktop` at **0**, the owner having moved the slider to "Never
  notify"; the seventh session read **5 and 1** — back at the Windows default,
  so **elevating raises a consent prompt on the secure desktop again**, which
  is what makes the elevated half of a test something a person has to be asked
  for rather than something a session can arrange. **THE ACCESS MODEL IS
  UNAFFECTED EITHER WAY AND THAT WAS MEASURED, NOT ASSUMED:** token filtering
  is `EnableLUA`'s doing and `EnableLUA` is 1 in both readings. In an ordinary
  session belonging to `don`, an administrator, `S-1-5-32-544` is **absent from
  the process token** and `id -G` returns no 544, so `IsElevated()` answers
  false where it should. Only the *prompt* changes.

  **`EnableLUA = 0` WOULD BREAK IT, AND WOULD ALSO MAKE §7 STEP 0e MEANINGLESS.**
  With no split token every administrator session is elevated, so `IsElevated()`
  collapses into `IsAdmin()`, plain `sd` puts any administrator into SDSYS
  always, and **SDSYS becomes reachable over ssh**, contradicting the local-only
  decision in §5.6. Worse for the work: **the refusal half of step 0e could
  never fire**, because no session would be unelevated, and the tests would
  record false passes. **The test machine must have `EnableLUA = 1`.**

  So a normal SD account, which `CREATE.ACCOUNT USER x` deliberately leaves out
  of `Administrators` (§4 above), **cannot elevate and therefore cannot reach
  SDSYS**. That is the Linux rule, enforced by the OS.

- **AN UNELEVATED ADMINISTRATOR'S TOKEN CARRIES `Administrators` AS "GROUP USED
  FOR DENY ONLY".** Observed the same session, in an ordinary PowerShell window
  belonging to `don`, who is in `Administrators` in the SAM:

  ```
  Elevated now: False
  BUILTIN\Administrators   Alias   S-1-5-32-544   Group used for deny only
  ```

  **That string is the whole of the distinction §7 step 0 needs.** It is the
  same fact §5.6.1 measured on 14 Aug with a C probe and read the other way:
  `getgrouplist()` answers "is an administrator", the token answers "is elevated
  right now", and the new model wants both — see §5.6.1's correction.

- **`sudo.exe` is present on this build and enabled in inline mode**
  (`Enabled = 3`). It was enabled by hand on 14 Aug 2026; **the installer does
  not install or enable it** — `gplbld/sd.iss` does not mention `sudo` anywhere,
  checked the same session. It is not needed: "Run as administrator" produces
  the same elevated token on every Windows version.

#### The account model and the ssh-only model

- **The five new OS-facing BASIC helpers work, and the shell is PowerShell.**
  Observed 14 Aug 2026 from inside SD, then re-observed after `op_sh.c` was
  changed to default `SH`/`SH1` to PowerShell — every case still passed, so
  `OS.EXECUTE` reaches PowerShell and the exit status carries back through
  `OS.ERROR()` with bash out of the loop entirely.

  **`!valid_os_path`** 16 of 16 — Windows, POSIX and mixed paths pass; empty,
  over 255 characters, and every shell metacharacter refused. **`!is_grp_member`**
  7 of 7, including the rev 0.9.0 "own group account" case, closing the §6 trap
  that had it answering no for everyone. **`!ps_script`** 5 of 5, carrying a
  secret off the command line and returning `exit 42` as 42, a `throw` as 1, an
  empty script as -1.

  All ten changed or new `GPL.BP` programs compiled with 0 errors and no "not
  assigned a value" warnings. **One measurement decided the design:**
  `Invoke-Expression` propagates a script's `exit` status where
  `& .\script.ps1` does not — 7 through the first, 1 through the second — and
  it is not subject to the execution policy, so nothing needs
  `-ExecutionPolicy Bypass`.

- **A Windows administrator is an SD administrator, tested two ways.** From an
  **unelevated** session belonging to a machine administrator — the case the
  previous test would have got wrong. Positive: the shipped build ran
  `sd -start`, the daemon came up, `sd -stop` took it down. That is decisive
  rather than incidental, because **gid 544 is not in `getgroups()` in that
  session**, so it can only have been found through `getgrouplist()`. Negative:
  `sd.c` and `linuxlb.c` rebuilt with `-DSD_ADMIN_GID=99999` refused with
  "Command requires administrator privileges", exit 1. See §5.6.1.

- **`CREATE.ACCOUNT` RUNS, AND IT HAD NEVER BEEN RUN BEFORE.** From an elevated
  session, both halves of the account are made — Windows user enabled, in
  `sdusers` with its `sdu_` group, account directory, VOC, `$HOLD`,
  `$SAVEDLISTS`, BP, private catalogue, `ACCOUNTS` record — and the
  `ADMINISTRATOR` keyword does exactly what §5.6.1 decided: **without it the
  account is not in `Administrators`, with it it is.** The add went in **by
  SID**, `!os_group` accepting `S-1-5-32-544`, because the name is localised.
  `CREATE_USER`, `SET_PASSWD` and `OS_GROUP` have executed against real Windows
  accounts. **`DELETE.ACCOUNT` and `MODIFY.ACCOUNT` still have not.**

- **The deny-logon rights are applied correctly, and nothing else is
  disturbed.** `gplbld/deny-logon.ps1` as the installer invokes it:
  `SeDenyInteractiveLogonRight` went from `Guest` to `sddenyprobe,Guest`,
  `SeDenyRemoteInteractiveLogonRight` from absent to `sddenyprobe`, and
  **`SeDenyNetworkLogonRight` was left untouched** — the row that matters, ssh
  authenticating with a network logon (§5.6.2). The surviving `Guest` entry is
  the argument for `LsaAddAccountRights` over `secedit` shown working.
  Idempotent; a missing group exits 1 saying so.

  **A caveat on reading this back, AND IT HAS NOW CAUGHT TWO ATTEMPTS.**
  `secedit /export` writes resolvable local groups **by name**, not by SID, so
  a verification that greps for a SID reports "not present" when it is.
  **There is a second half: the file is UTF-16LE** (`FF FE`), so
  `Get-Content` without `-Encoding Unicode` can match nothing at all — which
  looks identical. On 17 Aug 2026 a hand-rolled check hit **both** at once and
  reported all three rights absent on a machine where two were correctly
  present. **Use `gplbld/verify-sshonly.ps1`**, which gets both right
  (`:421-432`) and carries this warning in its own comment. Do not hand-roll
  it a third time.

- **THE SSH-ONLY MODEL WORKS.** Observed by `gplbld/verify-sshonly.ps1` against
  a real Windows account. This is §5.6.2, which had been decided, built,
  shipped in the installer and never once exercised. Thirteen checks, all
  passing:

  | | control, in no SD group | after joining `sdsshonly` |
  |---|---|---|
  | `LogonUser` INTERACTIVE — the console | admitted | **refused 1385** |
  | `LogonUser` NETWORK_CLEARTEXT — ssh password auth | admitted | admitted |
  | **`ssh` with a password** | admitted | **admitted** |
  | `ssh` with a key | admitted | admitted |

  **The bottom two rows of the middle column are the whole design.** The console
  is closed by the deny rights and ssh is not, measured on the same account
  minutes apart with nothing else changed. `1385` is
  `ERROR_LOGON_TYPE_NOT_GRANTED`. `ssh` **ran a shell**, not merely
  authenticated — the test asserts on `whoami` — and the `OpenSSH/Operational`
  log recorded `Accepted password` and `Accepted publickey ... ED25519` from the
  installed service at the same moment, so the verdict does not rest on the
  test's own reporting.

  **Why there is a control column at all.** The first run refused the key login
  on *both* sides. Measured alone, the treatment side would have read as "the
  deny rights break ssh" and §5.6.2 would have been abandoned on a false
  result. An equal failure on both sides cannot have been caused by the thing
  that differs between them. **Keep the control.**

- **A brand new Windows account cannot use ssh KEY authentication until it has
  logged in once.** A property of Windows, not of anything here: an account that
  has never logged on has no profile and no home directory, and Win32-OpenSSH
  resolves `AuthorizedKeysFile .ssh/authorized_keys` relative to the home
  directory, so a planted key is never read. Observed in both directions — the
  key refused twice with no prior login, then accepted after one password login
  created the profile, with group membership identical either way. **It applies
  to accounts `CREATE.ACCOUNT` makes.** Password authentication is unaffected
  and works immediately; only keys wait.

- **`BUILTIN\Users` membership is not required for an SD account.** Asked
  because `New-LocalUser` joins no group and `CREATE_USER` adds none, so an SD
  account is in `sdusers`, `sdu_<name>` and `sdsshonly` and nothing else.
  Measured rather than assumed: the account logged in over ssh and ran `whoami`
  **before** `Users` was added, and adding it changed nothing.

- **`CREATE.ACCOUNT`'S SSH-ONLY BRANCH WORKS, AND THE RESTRICTION IT APPLIES
  HOLDS. 16 of 16, END TO END.** Observed 14 Aug 2026 by
  `gplbld/verify-createaccount.ps1 -Account sdacct2` from an elevated window,
  against the install rebuilt the same session. `CREATEA` line 400 had never
  executed before — `sdsshonly` did not exist the first time the verb ran.

  What SD made: an **enabled** Windows account, in `sdusers`, `sdu_sdacct2` and
  `sdsshonly` and **not** in `Administrators`; message 10034, `sdacct2 may sign
  in over ssh only`; the account directory with `VOC`, `$HOLD`, `$SVLISTS`, `BP`
  and a private catalogue; and the `ACCOUNTS` record. Then the same three
  measurements that proved §5.6.2, on an account **SD created** with a password
  **SD set**:

  | Measurement | Result |
  |---|---|
  | `LogonUser` INTERACTIVE (console) | **refused 1385** |
  | `LogonUser` NETWORK_CLEARTEXT | **admitted** |
  | real `ssh sdacct2@localhost whoami` | **admitted** |

  **So the chain is closed:** SD creates the account, SD restricts it, and the
  restriction holds when tested from outside. That is the whole of the ssh-only
  model except RDP, demonstrated on an account created by the verb rather than
  by a test harness. It also settled `SET_PASSWD` end to end — the password SD
  generated and set was the one ssh accepted.

  **`Warning unable to setgid bit on Group Folder, status: 1` prints on every
  account creation.** Expected and harmless — the `sudo chmod g+s` Linux-ism in
  `CREATEA` (§5.16, §7 step 1e), now observed rather than predicted.

- **`AllowGroups` IS APPLIED AND ENFORCED, AND THE ADMINISTRATOR IS NOT LOCKED
  OUT.** Observed on this machine's live `C:\ProgramData\ssh\sshd_config`.
  **This was the lockout risk, and it is now measured rather than reasoned
  about.** `allow-ssh-groups.ps1 -Installed` exited 0 and wrote
  `AllowGroups sdusers GITORLI\sdusers Administrators GITORLI\Administrators`
  between its markers **immediately before the `Match` block** — the placement
  `verify-allowgroups.ps1` exists to guarantee, confirmed in the live file. The
  original is at `sshd_config.before-sd`; `sshd` restarted and came back
  Running.

  Then control and treatment, by real ssh connections with no password handled,
  so the **reason** is read out of the `OpenSSH/Operational` log rather than the
  exit code:

  | account | groups | sshd logged |
  |---|---|---|
  | `don` | `sdusers` + `Administrators` | `Connection reset by **authenticating user** don` |
  | `CodexSandboxOffline` | neither, **and enabled** | `**not allowed because none of user's groups are listed in AllowGroups**` |

  **The client message is identical in both cases** —
  `Permission denied (publickey,password,keyboard-interactive)`. That is the
  trap, and it is why this was done through the log: only the log distinguishes
  refused-by-group from failed-to-authenticate, marking a group-refused account
  `invalid user` against `authenticating user` for an allowed one.

  So the patterns match a real member, a non-member is refused for exactly the
  intended reason, and the machine's own administrator kept ssh. An `sdsshonly`
  account is in `sdusers` too, so ssh-only accounts are allowed by construction.

  **A first control was confounded and is recorded because it nearly passed for
  evidence.** `WDAGUtilityAccount` is **disabled**, and produced a bare
  `Connection reset` with no log line — a different-looking failure that could
  as easily have been the disabled account as the group check. It was redone
  with an **enabled** non-member, which is the one in the table.

- **`allow-ssh-groups.ps1` edits `sshd_config` correctly** — 20 checks by
  `gplbld/verify-allowgroups.ps1` against
  `C:\Windows\System32\OpenSSH\sshd_config_default`, the template `sshd` copies
  on first start. **The test needs no elevation, no `sshd` and no network**,
  because that template is world readable, so it re-runs on any machine; it
  lifts the functions out of the shipped script by parsing it, so it cannot
  drift from the code it checks. The checks cover: the block lands **before**
  the first `Match`; exactly one `AllowGroups` survives three applies; remove is
  an exact inverse of add; a foreign `AllowUsers`/`DenyUsers`/`AllowGroups`/
  `DenyGroups` is detected and not merged into (§5.9), while
  `AllowAgentForwarding` and `#AllowGroups` are correctly *not* taken for
  policy, and SD's own block is not mistaken for a foreign one.

  **It found a real defect on the first run** — a readability blank line falling
  outside the markers, so every apply/remove cycle grew the file by a line (§6).
  Also observed unelevated: **`-Check` resolves the administrators group from
  `S-1-5-32-544`**, which is the half that is wrong on a localised Windows if
  written as a literal.

### Not verified — treat as unknown

**SWEPT 21 Aug 2026 AGAINST THE VERIFIERS THAT NOW EXIST, and it was overdue.
Eight entries here were wrong: four are struck through — §7 step 6, the RDP
refusal, typing at a real console, and the no-development-tree install — and
four narrowed, where part of the claim still stands.** `MODIFY.ACCOUNT` was a
ninth, struck earlier the same session, and **§7 step 11's own heading was a
tenth** — it said *"AND NOT RUN"* directly above a body describing what
running it did. Each carries what settled it.

**AN ELEVENTH WENT THE SAME DAY, AND IT IS THE ONE THE SWEEP ITSELF MISSED.**
Step 11's entry below said the local transport *"DOES NOT WORK"*; it was
replaced hours after that measurement and the step's own body reports the
replacement passing on an install. **The sweep had rewritten that heading's
"NOT RUN" half and left its "does not work" half**, so a half-corrected
sentence read as a checked one. **A correction that touches part of a claim is
the easiest kind to mistake for a whole one** — the striking below now covers
all three places step 11 carried it. The pattern is worth knowing before reading the
rest: **the header was rewritten every phase and this list was not**, so what
rots here is specifically the entries claiming something has NOT been done —
the dated measurements elsewhere in §4 held up under checking. Nothing was
deleted; a closed entry keeps its body where that body is a trap (§0 rule 4),
notably the RDP one.

**Two of them had already been answered by measurements recorded in this very
section**, hundreds of lines above the entry still calling them unknown — the
RDP refusal and the no-development-tree install, both settled by the 15 Aug VM
run. **Check §4 against itself before believing anything here.**

- **`OS.EXECUTE` IS UNGATED FOR EVERY *LOCAL* SESSION, and `OS.USERS` field 2
  does not change that.** §7 step 7. The `SH` half is verified (§4); `OS.EX` is
  stored, dictionaried and read by nobody, so an unlisted programmer with
  `BASIC` still has full OS access from a program. Gating it needs C.

  **"FOR EVERYBODY" WAS TRUE UNTIL 21 Aug 2026 AND IS NOT NOW.** The API path
  is gated — the containment gate in `op_dio2.c` — and it is *measured*, not
  argued: `verify-apiadmin` ships a second probe, `APIOSEXECPROBE`, whose whole
  job is to die (`verify-apiadmin.ps1:281-296`), alongside one that must
  survive. **The narrowing is the API path only**; a local or ssh session is
  exactly as open as this entry always said.

- ~~**§7 STEP 11 HAS BEEN CALLED AND DOES NOT WORK — 17 Aug 2026, on the
  08:03:49 install.** `SDConnectLocal("DON")` never returns; `sd.exe` spins
  silently because `select()` calls the attached descriptor permanently ready.
  So it is NOT currently a route to evidence for §7 step 6c.~~ **THE TRANSPORT
  WAS REPLACED LATER THE SAME DAY AND IT WORKS. Struck 21 Aug 2026, and it is
  the ELEVENTH stale claim of the sweep** — which corrected §7 step 11's
  heading from *"AND NOT RUN"* to *"CALLED, AND IT DOES NOT WORK"*, fixing one
  half of a sentence the body had already refuted twice. **Both halves are now
  struck, here and at §7 step 11.**

  **`SDConnectLocal()` CARRIES A SESSION** — four runs, unelevated,
  `local_connect_test` exit **0** each time, `DON` admitted and `SDSYS`
  **refused** with *"User not allowed in requested account"*. **And on a real
  install**: `make check-local` passed on the installed pair, `assert-current`
  exit 0, **12:28:49 install**, `WHO -> 2 DON`.

  **The always-ready `select()` finding is not withdrawn** — it is why the named
  pipe went. Two anonymous pipes handed to the child as its standard handles
  replaced it, so Cygwin builds descriptors 0 and 1 itself and its
  `PeekNamedPipe`-based `select()` answers honestly. §7 step 11 has the
  measurement, with the control in the same process.

  **AND IT DID DELIVER THE §7 STEP 6c EVIDENCE THIS ENTRY SAID IT COULD NOT.**
  The `SDSYS` refusal is the `ACC$GROUP` grant check running; `DON` admitted
  alone would be equally consistent with a check that never executed, which is
  what makes the pair evidence and either half alone worthless. 6c also has an
  independent measurement over the port — `verify-apiport.ps1 -Prefix sdapi2`.

- ~~**§7 STEP 6 IS BUILT IN FULL AND HAS NEVER RUN — 17 Aug 2026.**~~ **IT RAN
  THE SAME DAY THIS WAS WRITTEN.** §7 step 6 is **CLOSED 17 Aug 2026,
  nineteenth session — the API works end to end**, measured by
  `verify-apiport.ps1 -Prefix sdapi2`: a session opened over the port, **the
  wrong password refused by `!CRED_VERIFY`** (that is 6a) **and SDSYS refused by
  the `ACC$GROUP` test** (that is 6c), with *different* messages, which is what
  makes the admitted case mean anything. Re-measured 21 Aug at `sdapi4`, 13/13.
  **What is left of this entry is 6b and the "what to watch" list below**, kept
  because it is the specification for anything that touches `vb.login` next.

  The API authenticates against `$CRED`, `login_user()` is deleted,
  `K_SET_USERNAME` carries the verified identity, and `vb.account` applies the
  `ACC$GROUP` grant check.

  **6a and 6d ARE COMPILED; 6c IS NOT.** It went in after the 06:07:30 install
  and the next `stage.py --bootstrap` is its first compiler — the same position
  6a was in a few hours earlier, and the same place a mistake will surface.
  **What to check when it compiles:** that `is_grp_member` resolves, and that
  the inline `deffun` beside the call does not upset `SECOND.COMPILE` the way
  `DEFFUN` upsets `bbcmp.py` (`APISRVR` already had one at line 898, so it
  should not, and that is the reason to expect it rather than a measurement).

  **THE COMPILE HALF IS NOW VERIFIED and the risk it carried is spent.**
  Seventeenth session: `SECOND.COMPILE` during the 06:07:30 bootstrap was
  `APISRVR`'s first compiler of any kind and it passed — `bootstrap.py` dies on
  any error or `is not assigned a value` warning, and did not. The evidence is
  `gcat/$APISRVR` **9,129 bytes, md5 `84f7d949…`**, against **9,056 /
  `49c28f05…`** in the previous stage; `gcat` 132 and `GPL.BP.OUT` 193 say the
  bootstrap finished rather than stopping at the seed. So `call !CRED_VERIFY(…)`
  and `void kernel(K$SET.USERNAME, …)` are both accepted BASIC. **Nothing about
  what they DO is verified by this** — a compile proves syntax.

  **THE TRANSPORT DOES NOT BLOCK ALL OF IT, WHICH THIS FILE SAID UNTIL 17 Aug
  2026 AND WAS TOO STRONG.** The two halves have different prerequisites:

  - **6c IS TESTABLE WITHOUT ssh**, through `SDConnectLocal()` (step 11, now
    built). A local session reaches `vb.account`, which is exactly what 6c
    guards. **`vb.local.login` authenticates nothing, deliberately** — a local
    client already runs as the user, so `logname` stays as
    `kernel(K$USERNAME,0)`, which is the identity 6c tests. **That makes step
    11 the cheapest route to the first evidence step 6 has ever had.**
  - **6a and 6b are NOT**, and there the old reasoning stands: they live in
    `vb.login`, the remote path, which needs a client and a transport that is
    **measured unportable** (§8).

  **What to watch when something can finally call `vb.login`:** that an account
  with no `$CRED` entry is refused; that an account with one is admitted; that
  `@logname` afterwards is the name that was verified and not the client's
  assertion; and that `kernel(K$SET.USERNAME,…)` is **refused from a program
  that is not `$internal`**, which is the gate protecting the audit trail.

  **What to watch for 6c, which is reachable sooner:** that a member of an
  account's `sdu_` group is admitted; that a non-member is refused with
  `sysmsg(10003)`; that an account with an empty `ACC$GROUP` is refused rather
  than admitted; and that SDSYS is refused.

- ~~**THE LOGIN RULE IS BUILT AND HAS NEVER RUN**~~ — **VERIFIED TWICE SINCE**,
  and this entry was left standing wrongly for a week: 5 of 5 on 16 Aug 2026
  (eleventh session) and 6 of 6 with the control on the 22:57:00 install
  (sixteenth). §4 Verified has both. The original text asked for exactly the
  checks that were then made — an elevated `sd` landing in `DON`,
  `LOGTO SDSYS` working from there, `sd -ASDSYS` refused, `sd -internal` still
  reaching SDSYS, and `verify-createaccount.ps1` still passing 16 of
  16.
- ~~**THE SERVICE IS BUILT AND HAS NEVER RUN**~~ — **CLOSED AND VERIFIED**,
  header item 2: it runs, an ordinary user reaches it, and it survives a
  restart including one with a leftover segment. Every question this entry
  raised was answered — the SCM reaches Running, `sdwind` appears, `sd -start`
  does work under LocalSystem, ordinary sessions attach to a SYSTEM-created
  segment, and the uninstaller removes the service. `sdsvc.c` is still native
  UCRT64 for the reason recorded there: a service must call
  `StartServiceCtrlDispatcher` and `sd.exe` is MSYS2-POSIX.

  §5.7 still reserves *the identity half* — a service account owning the tree,
  sessions over a named pipe — for stage 2. **What is done is the lifecycle
  half only**, and it changes nothing about who owns the files. **The named
  pipe is no longer optional**, though: §8's transport measurement forces it.
- ~~**The lockout fix is compiled and run on THIS machine only.**~~ It has
  since gone out through the installer on two machines and on every fresh
  install here — `adopt-account.log`'s `keeps the Windows sign-in rights it
  already had` line is the tell, and it appeared again on 22:57:00.
- ~~**No staged tree has yet been built with the `ACCOUNTS/SDSYS` fix.**~~ Many
  have; `check_no_stage_paths` is clean on every stage since, and
  `retarget_sdsys_account()` is now a normal part of `stage.py --bootstrap`.
- ~~**`MODIFY.ACCOUNT` has never been run.**~~ **RUN AND VERIFIED 21 Aug 2026**,
  on the 17:18:11 install: `verify-routes` **33/33**, which calls it six times —
  `API`, `API` again for the "already had that access" path, `BOTH`, `NONE`,
  `SSH`, and `NONE` against an administrator (`verify-routes.ps1:320-361`).
  Step 4 is the one that separates absolute from additive; the header carries
  why. `CREATE.ACCOUNT` and `DELETE.ACCOUNT` had already been run (§4 Verified).
- ~~**`DELETE.ACCOUNT`'s "SD created it" branch is untested**.~~ **RUN AND
  VERIFIED 16 Aug 2026**, sixteenth session, on `sdacct14` — §4 Verified. All
  three of `DELACC`'s cases have now executed at some point.
- ~~**`CREATE.ACCOUNT ... ADOPT` is untested**, and nothing calls it.~~ **The
  installer calls it on every install** and `adopt-account.log` records it —
  §7 step 1f, closed 15 Aug 2026.
- ~~**RDP refusal, and it CANNOT BE TESTED ON THIS MACHINE.** The last
  unobserved claim in §5.6.2. `SeDenyRemoteInteractiveLogonRight` is confirmed
  **applied** to `sdsshonly` in machine policy, but nothing has watched it
  refuse a session.~~ **WATCHED REFUSING A SESSION — 15 Aug 2026, tenth
  session, on the VirtualBox guest, control then treatment** (§4 Verified,
  *"§7 STEP 2 RAN ON A SECOND MACHINE"*): `VIRTUAL\don` ADMITTED, then
  `VIRTUAL\sdacct7` REFUSED with *"the user account is not authorized for
  remote login"* — the wording that is
  `SeDenyRemoteInteractiveLogonRight` specifically rather than a credentials
  failure, which is what makes it evidence. **§5.6.2 has no unobserved claim
  left.**

  **THE REST OF THIS ENTRY IS KEPT AS A TRAP, NOT A TASK** (§0 rule 4): it is
  still true that this cannot be tested here, and the record below is what
  stops the next session spending an hour rediscovering that.

  It cannot be automated — there is no `LogonUser` logon type corresponding to
  RDP's logon type 10, so only a real Remote Desktop connection exercises the
  right.

  **THIS MACHINE CANNOT RDP TO ITSELF. Measured 14 Aug 2026, three attempts**,
  so do not spend more time on it here. All three answered:

  ```
  Your computer could not connect to another console session on the remote
  computer because you already have a console session in progress.
  Error code: 0x708
  ```

  | attempt | credentials offered | result |
  |---|---|---|
  | `mstsc /v:localhost` | the signed-in user's own | `0x708` |
  | `mstsc /v:localhost` | the probe account's | `0x708` |
  | `mstsc /v:10.0.0.3` (own Wi-Fi address) | the probe account's | `0x708` |

  **The refusal comes before any credential prompt**, so which account is
  offered never enters into it, and addressing the machine by its LAN address
  rather than `localhost` makes no difference either. RDP was enabled
  throughout — `fDenyTSConnections` 0, `rdp-tcp` listening, inbound firewall
  rules on for all profiles, all checked the same day.

  That is the whole of what was observed. It is deliberately not turned into a
  statement about how many sessions Windows permits: two such statements were
  derived from this error already and both were wrong (HISTORY.md, two
  `Correction:` entries of 14 Aug 2026).

  **So the test needed a separate client machine** — §7 step 2, and that is
  how it was done on 15 Aug. To repeat it: `verify-sshonly.ps1 -Keep` on the
  machine under test, then RDP to it from a different one.

- **That SD works over an ssh session AT A REAL TERMINAL — narrowed twice, and
  what is left is only the tty half.** *"Not the two together"* is no longer
  true: on 15 Aug 2026 `ssh sdacct6@localhost whoami` answered **SD's banner
  and a `:` prompt, exit 0, with `whoami` never running** (§4 Verified) — sshd
  discarding the client's command and running SD is the two together. And the
  MSYS2 tty layer is no longer unknown either; it was measured at a real
  Windows console on 19 Aug (§5.18, and the entry above).

  **What has still never happened is those two at once**: an interactive
  `sd -ASOMEACCOUNT` at a real terminal *reached over ssh*, where the pty is
  sshd's rather than `conhost`'s. That is a narrower question than this entry
  used to ask, and §7 step 2's rig is what would answer it.

- **Which of `AllowGroups`' four patterns actually matched.** It is applied and
  enforced (§4 Verified), but `AllowGroups` is a union and all four patterns
  were written deliberately, so the bare and `COMPUTER\` forms cannot be told
  apart from that result. Deliberate — see §5.6.2 — and it stays unknown unless
  somebody narrows the list on purpose. **Also unknown: what the installer's
  own path through it does**, since the measurement ran the script by hand on a
  machine that already had OpenSSH and so never sees the tick box.

- **The installer's own behaviour with the new options — NARROWED, 21 Aug 2026,
  and the closing dialog is off this list.** **The reworded closing dialog HAS
  been seen**: screenshotted by the owner before 15 Aug, and read on screen
  again 17 Aug on the 13:43:00 install — *"looks fine"* (§7 step 3, where the
  reading found a defect that compiling never would). **What is still unseen is
  the `limitssh` task** — no longer a subtask since 16 Aug — **and
  `ApplyAllowGroups` reporting any of its three outcomes**, and neither can be
  seen here: `Check: SshServerAbsent` is false on a machine that already has
  OpenSSH, so the tick box never appears.

  Compiling an Inno script proves the Pascal parses, nothing more — and the two
  defects this file has already recorded in that script (the brace bug, the
  per-file `Check`) both compiled perfectly.

- **Whether `OS.EXECUTE` works at all on an installed system.** It almost
  certainly does not — see the shell trap in §6.

- ~~**Typing at SD from a real Windows console.** ... how the MSYS2 tty layer
  behaves in `conhost` or Windows Terminal — echo, masked input, arrow keys,
  terminfo — is unknown. This is the one question that has to be answered by a
  person at a keyboard.~~ **ANSWERED BY A PERSON AT A KEYBOARD, 19 Aug 2026,
  and it produced three §5 decisions rather than a yes.** The owner typed at SD
  in cmd, PowerShell and Windows Terminal and found **the arrow keys, backspace
  and clear screen dead** — root-caused to the default terminal type and fixed,
  with all four `TERM` cells measured on the 09:10:45 install (§5.18). §5.17 —
  accept both spellings of a key — and §5.19 — the full-screen editors carry
  their own key tables — came out of the same sitting, and `verify-keys` and
  `verify-editkeys` exist because of it.

  **What this did NOT answer is the question the entry said it turned on:**
  whether SD needs MSYS2. It does, and not for terminfo — SD generates its own
  `terminfo/` from `terminfo.src` and ships it (§3 Building). The dependency is
  that `sd.exe` is built against the MSYS2 POSIX runtime, which is **§5.3's
  deliberate decision, not an unknown**, and the tty behaviour measured on
  19 Aug is that runtime's, working.
- Semaphore locking under contention. The semaphores have never been observed
  held, so the `sdsem.c` port is exercised only in the uncontended case.
- ~~`SDConnectLocal()` at runtime. It needs a running server and a
  configuration file (§5.8).~~ **RUN, AND ON AN INSTALLED TREE** — see the
  struck entry above and §7 step 11. **Both prerequisites still hold and an
  install satisfies them**: `SDConnectLocal()` calls `sysdir()` and returns
  FALSE if the configuration file is absent (`sdclilib.c:1507`). What changed is
  that the file is no longer how `sd.exe` is LOCATED — that is `sd_exe_path()`,
  `GetModuleHandleEx(FROM_ADDRESS)` beside the DLL — and the comment at
  `sdclilib.c:1502` says the check is kept deliberately, ahead of spawning
  anything.
- **Contention.** Two sessions have now coexisted — an interactive one sitting
  at a password prompt on `/dev/pty0` and a second running `LISTU`, which
  listed both (users 8 and 9, 13 Aug 2026). So multi-user attach works. What
  is still untried is two sessions *competing*: record locking between real
  users, and the API server path.
- Writing and reading application data. The bootstrap creates and reads system
  files, and the scratch accounts hold nothing but a VOC.
- ~~**The installer on a machine with no development tree.** ... the
  accidental-dependency question is untouched, and it is precisely how
  `gplsrc` stayed in the data tree.~~ **ANSWERED 15 Aug 2026, and by the
  measurement recorded 650 lines above this one.** The VirtualBox guest had
  **no MSYS2, no `gplsrc`, no development tree** — *"which is the whole reason
  the step existed, because an accidental dependency on any of them can only
  show up here"* — and the install came out **byte-identical**: `sd.exe`
  sha256 `81594E79CC2B560C`, the same four counts (19 / 3,456 / `gcat` 130 /
  `GPL.BP.OUT` 191), `sd -start` exit 0 and `COUNT VOC` **431**. There is no
  accidental dependency on the development tree.
  `installsdai.sh` is entirely Linux and is not being ported (§5.9).

  **The `sdadmins` prediction that used to sit here is gone**, and not by being
  tested: §5.6.1 made `IsAdmin()` gate on Windows `Administrators`, which
  always exists, so there is no longer a group a clean machine could be missing.

- **What the daemon actually does for the system.** Fixed and verified
  14 Aug 2026 (see §4 Verified), so what remains unknown is only its *effect*:
  `check_lost_users()` shells out to `sd -cleanup` every five minutes when it
  finds a user table entry whose process is gone. That path has never been
  exercised — no session has been killed and the cleanup watched — and it was
  unreachable until today, since the daemon was never running. It matters for
  the API (§7 step 6), which is the daemon's other reason to exist.

- **Why `errlog` stayed empty** through a full start / command / stop cycle on
  the freshly installed tree, 14 Aug 2026, where earlier sessions saw
  "User n (pid, don)" lines written to it. Still empty after the daemon was
  fixed, so it is not explained by that. Not chased.

  **THE PREMISE NO LONGER DESCRIBES THE SYSTEM, 21 Aug 2026.** `errlog` is
  written per connection now — `sdwind.c`'s `log_message()` gained the trim the
  `sd` side always had — and `verify-peerlog` measures both the writing and the
  trim, 21/21 on the 17:18:11 install. So this is a question about **14 Aug's
  tree**, not about anything installed since, and it is not worth chasing on a
  current one.

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
   (5 Aug 2026) — `gplsrc/sdclilib/VENDORING.md` is the record, and the whole
   directory is a vendored copy kept faithful to its source on purpose.
4. **Their developer then forked `winsdclilib` back**, and changes from it are
   in `sdb64`'s `dev` branch now.

**So for this directory, code has flowed BOTH ways, and "upstream" is
ambiguous** — the reverse of every other file in the port, where `sdb64` is
plainly the source. Two consequences worth acting on:

- **Do not "align with upstream" reflexively here.** A session did exactly that
  with `SV_EMSG_PAIR`/`SV_ECONTXT` and had to revert it (§2's dev-branch review,
  UPSTREAM_FIXES.md #2).
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

### 5.19 The full-screen editors carry their own key tables (19 Aug 2026)

**Owner, 19 Aug 2026: "fix backspace in ED and UPDATE.RECORD".** §5.17 had
recorded this as owed and said the work was "a test that drives a full-screen
editor, and nothing here does that yet". **That test now exists** —
`gplbld/verify-editkeys.ps1`, 14 checks.

**ED WAS NEVER AFFECTED, AND §5.17 WAS WRONG TO LIST IT.** `ED` is the LINE
editor: it reads whole lines with `input`, so it goes through the command-line
editor that `_KEYCODE` fixed on 19 Aug. **Measured: DEL erases backwards in ED
already.** It cannot reach the screen editor either — `ED:3436` passes
*"Not full screen editor"* and there is no path from one to the other.

**THE TWO THAT WERE AFFECTED ARE `SED` AND `UPDREC`**, and the fault is the same
in both: their key tables are hard-coded and know nothing of terminfo, so they
bound `char(127)` — the byte every Windows console sends for **Backspace** — to
**Delete**. Measured before the change, on the 10:06:08 install:

| | Backspace, DEL 127 | Ctrl-H 8 |
|---|---|---|
| `SED`, type `AB` DEL `C` | **`ABC`** — deleted forwards | `AC` — correct |
| `UPDREC`, field `AB`, type `X` DEL | **`XB`** — deleted forwards | `AB` — correct |

**AND `UPDREC` WAS WORSE THAN A DEAD KEY: ITS ARROWS TYPED THEMSELVES INTO THE
RECORD.** Its only cursor-key bindings were `char(203)`–`char(212)`
(`UPDREC:2427`), an 8-bit terminal convention nothing on this platform emits. No
escape sequence was bound at all, so `get.key` walked the multi-character table,
failed to match, and the bytes fell through as ordinary text. **Measured: field
`AB`, press Right, type `X`, save — the record became `CXAB`.** That is silent
data corruption in a data-entry screen, and it is why the arrows were fixed here
as well as the erase keys.

**`SED`'s ARROWS WERE ALREADY RIGHT** and are the worked example the `UPDREC`
change copies: `SED:4489` binds `@B`, `@[[D`, `@[OD` and `char(203)` to
`F.LEFT` — Ctrl-B, both escape spellings, and the 8-bit code. Measured: all
three spellings move the cursor. Only its erase keys were wrong.

**THE TWO KEYS ARE DISTINCT BYTES ON THIS PLATFORM, so nothing is shared and
neither key loses its function** — Backspace is `127`, Delete is `ESC [ 3 ~`
(`kdch1`), both measured from three console hosts in §5.18. `SED`'s `F.DELETE`
and `UPDREC`'s `K$DELETE` now take the escape sequence and `127` goes to
backspace. **A terminal that genuinely sends DEL for its Delete key gets
Backspace instead**; these are shipped defaults, and `SED` reads its bindings
from a file a site can edit.

**`UPDREC` ALSO GAINED THE KEYPAD BLOCK** — `khome`, `kend`, `kdch1`, `kich1`,
`kpp`, `knp` — because every one of them was unbound and would have typed itself
into the record in exactly the same way. `kich1` goes to `K$OVERLAY`, which is
what the 8-bit Insert code `char(211)` was already bound to.

**THE INSTRUMENT IS THE SAVED RECORD, AND THAT IS WHAT MAKES THIS TESTABLE AT
ALL.** `SED` and `UPDREC` read the keyboard with `keyin()`, which reads standard
input — so **a full-screen editor is drivable from a pipe** exactly as the
command-line editor is. The screen is not drivable and does not need to be: type,
save, quit, then read the record back with `CT`. §5.17 assumed a console was
required and it is not.

**MEASURED AFTER THE CHANGE — `verify-editkeys.ps1` 14/14, 14:54:36 install.**
`SED` `AB`+DEL+`C` gives `AC`; `UPDREC` field `AB`, `X`+DEL gives `AB`; and
`UPDREC` Right-then-`X` gives `AXB` where it used to give `CXAB`. **The controls
are what make it evidence**: with no erase byte at all the same runs give `ABC`
and `XAB`, so the erase is what changed them; and the Delete key still deletes
FORWARDS in both editors, so the two keys were fixed rather than swapped.
**That last check has to be taken with the cursor NOT at the end of the line** —
at the end, deleting forwards does nothing, and the check would pass on a Delete
key that had stopped working altogether.

**A ONE-LINE `if ... then ... end else ... end` COMPILES CLEAN AND FAILS AT RUN
TIME**, and it cost this session a full verifier run. Written inline —
`open 'F' to f then write .. ; print 'OK' end else print 'FAIL'` — SDBasic
reports `0 error(s)` and then stops with **"Unassigned variable END"**, because
the inline `THEN` takes statements to the end of the line and the `END` is read
as a variable. Use the block form. **CLAUDE.md's "compiling is not running" has
a second edge here**: it is usually about testing a stale install, and this is
the same lesson one layer down.

**A TIMED-OUT RUN LEAVES A RECORD LOCK, AND IT OUTLIVES THE PROCESS.** This cost
an hour. `Stop-Job` kills SD mid-edit; `LIST.READU` then shows an `RU` lock owned
by a dead user; `UNLOCK USER n` and `UNLOCK FILE ...` will not take it from an
ordinary account session; and every later run on that record id stops on
*"Wait for lock to be released? Y or N only"*. **`verify-editkeys.ps1` uses a
fresh random record id for every case** so one timeout cannot poison the rest,
and reports any stale locks it finds rather than failing on them. They clear
with `sd -CLEANUP` (elevated — it removes only users whose process is gone,
`clopts.c:242`) or at the next cycle, which rebuilds the shared memory segment.

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

**THE VOC `login` PARAGRAPH IS WHAT DECIDES THIS, AND `LOGIN:116` IS NEARLY DEAD
CODE.** Measured: `system(7)` already answers `vt100` by the time anything can
look, so `LOGIN:115`'s `env('TERM')` branch never runs — **neither `$TERM` nor
`sd -TERM <type>` changes the terminal type**, only typing `TERM x`. The
paragraph runs after the subroutine and sets it unconditionally. Both were
changed so they cannot disagree, but the paragraph is the one that acts.

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

**THE EDITORS ARE THE SAME FAMILY AND ARE NOW FIXED — §5.19, 19 Aug 2026.**
`UPDREC` reads raw bytes with `keyin()` and carries its own table, and `SED`
does the same; both bound `char(127)` to Delete, so Backspace deleted forwards
inside them.

**TWO THINGS THIS PARAGRAPH USED TO SAY ARE WRONG, and §5.19 has the
measurements.** It listed **`ED`**, which is the LINE editor: it reads with
`input`, so the `_KEYCODE` fix above already covers it and DEL erases backwards
there today. And it said a test "needs a console" — it does not. `keyin()` reads
**standard input**, so a full-screen editor is drivable from a pipe, and the
instrument is the record it saves rather than the screen it paints.
`gplbld/verify-editkeys.ps1` is that test.

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

### 5.14 Administration should be forms, not remembered command lines (goal, 13 Aug 2026)

Goal from the repository owner on 13 Aug 2026, for **after the system runs
well** — not now, and not a reason to hold anything else up. Much of what
administration currently requires is a command line somebody has to remember,
or a record edited by hand in `MODIFY`. The intent is a set of admin helpers
that put a form in front of the same work.

Recorded here because it changes how several things on the §7 list should be
built, and that is cheaper to know before writing them than after. **The rule
that follows: new administrative capability goes in a subroutine with a verb
over it**, not in a verb that holds the logic, so a form added later calls the
same subroutine instead of reimplementing it or shelling out to the verb.
`GPL.BP/CRED_SET` and `CRED_VERIFY` with `SET_ACC_PASSWORD` over them are the
pattern to copy, and `SET.PASSWORD` is already prompt-driven, which is the
right precedent.

The two clearest cases are **the grants verb** (§7 step 5), edited through
`MODIFY ACCOUNTS` today, and **the batch allowlist** (§8), where `ED VOC
ALLOWED` is workable and a form is better — particularly as it is the one place
that has to enforce the no-arguments and VOC-type rules recorded there.

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
  after (header item 1). The same applies to anything else that assumes
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
    either stream. `termios` → Console API is §7 step 13, unported.

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
     hidden by `Check: SshServerAbsent` on this machine (header item 1). **It is
     no longer a subtask**: renamed `limitssh` and promoted on 16 Aug 2026 when
     its parent went (§5.9).
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
7. **BUILT, INSTALLED, AND HALF VERIFIED — 17 Aug 2026, twentieth session.
   `SH` is permitted by a list, not by elevation.** On the 22:43:52 install
   `CPROC` compiled, `WRITE_INSTALL_DICTS` wrote all five `OS.USERS.DIC`
   records, the ACL took, and an unlisted account is refused with message
   10053 (§4).

   **THE ADMIT PATH IS VERIFIED — `gplbld/verify-osusers.ps1`, 18 of 18, exit 0
   on the 07:00:00 install of 18 Aug 2026.** §4 has the table and what each row
   is for. The `changelog` entry it was waiting on is written.

   **THE SCRIPT RUNS UNELEVATED AND PROMPTS FOR UAC TWICE ITSELF.** The
   measurement must not be elevated or `CPROC:3448` admits it on
   `K$ADMINISTRATOR` and `OS.USERS` is never consulted; writing the record and
   removing it again must be, because that ACL is the whole protection. The two
   halves cannot share a token, and elevating is the easy direction.

   **IT IS EXEMPT FROM `assert-current`'s STALENESS GUARD** — added to
   `$neverShipped` (`assert-current.ps1:88`) with the other verifiers, or
   editing the test would demand a reinstall to re-run the test. That list is
   self-policing: a name that turns up quoted in `stage.py` or `sd.iss` is put
   back under the guard.

   **THE PROBLEM IT SOLVES (§8).** The gate at `CPROC`'s `os.command:` label
   admitted only `K$ADMINISTRATOR`, which is `IsElevated()`, and an ssh session
   can never be elevated — so programmers, the one group that needs a shell,
   were the one group that could never have one. Meanwhile `OS.EXECUTE` stayed
   ungated for everybody. The visible control was denied to the people who
   needed it and the capability it guards was open to those who did not.

   **WHAT WAS BUILT:** `@SDSYS/OS.USERS`, a directory file, **one record per
   account**, keyed by account name. Field 1 `SH`, field 2 `OS.EX`, each `yes`
   or anything else. Dictionary `OS.USERS.DIC` with `Name` (D 0), `SH` (D 1),
   `OS.EX` (D 2), plus `@ID` and an `@` default listing, shipped as source in
   `gplbld/FILES_DICTS` and written at bootstrap by `WRITE_INSTALL_DICTS`.
   Both files are staged empty by `stage.py` — **`WRITE_INSTALL_DICTS`
   `OPENPATH`s the dictionary rather than creating it**, so if it were not
   staged the entries would be skipped and the file would ship with no
   dictionary. Admin edits with `ED` from SDSYS. New message 10053.

   **NOT IN `NEWVOC`, and that was reconsidered mid-design.** The tier lists
   live there because `CREATEA` already has it open (`CREATEA:593`); `CPROC`
   does not, so the saving vanishes. Worse, everything in `NEWVOC` is copied
   into every account's VOC unless excluded in **two** places, and the tier
   lists' fail-safe is *permissive* — a missing record means the FULL VOC.
   A permission list needs the opposite default and must not inherit that
   convention.

   **THE ACL IS THE ENTIRE CONTROL.** `gplbld/secure-osusers.ps1` grants
   `sdusers` **(RX) — read, not modify**, which is the difference from
   `secure-cred.ps1`: `CPROC` reads the list from the user's own process, so
   they must read it and must never write it. Called from `[Code]` as
   `SecureOsUsers`, **exit code checked**, failure named in the closing box.
   Without it any SD user adds their own name and the file is decoration —
   exactly what happened to `$CRED`.

   **ELEVATION STILL PASSES ON ITS OWN**, deliberately: an empty `OS.USERS`
   must not lock the machine's own administrator out of `SH`, which is the
   lockout `ADOPT` caused with `sdsshonly` on 15 Aug 2026.

   **The metacharacter ban is lifted for a listed account only** (owner). An
   elevated session that is not listed keeps `!valid_shell_cmd` exactly as
   before, so this adds capability and regresses nothing.

   **WHAT IS NOT DONE, AND IT IS HALF THE FEATURE.** **Field 2 `OS.EX` is
   stored, dictionaried and read by nobody.** `OS.EXECUTE` is a BASIC
   statement compiling straight to `OP.SH`/`OP.SHCAP` into `op_sh.c`, never
   touching `CPROC`, so gating it needs **C**: two bits beside `USR_ADMIN`
   (`sysseg.h`, `0x0100` and `0x0200` are free), a kernel key gated on
   `HDR_INTERNAL` as `K$ADMINISTRATOR` is — or a programmer sets the bit
   themselves — `LOGIN` seeding them, and a check in `sh()`. Until then an
   unlisted programmer with `BASIC` still has full OS access from a program,
   so **this is an auditable permission record, not yet a boundary**.

   **Note `SH` implies `OS.EX` and cannot not**: `CPROC:3465` runs the verb by
   calling `os.execute`, so the two flags are not independent in that
   direction. The useful combination is `OS.EX` yes with `SH` no — programs may
   shell out, the person at the prompt may not.

   **Owner wants a form for account setup with these privileges** eventually
   (§5.14); `ED` is the interim editor.

   *(A "NOT COMPILED" paragraph stood here and was wrong by the time it was
   written — the 22:43:52 cycle compiled `CPROC`, as this step's own first line
   says. Removed 18 Aug 2026.)*

8. **Make everything lower case that can be** (§5.12). **STARTED 17 Aug 2026,
   twentieth session: the file-name half is done in source and NOT VERIFIED.**

   **`CASE_INSENSITIVE_FILE_SYSTEM` IS NOT ONE THING, AND THAT IS THE FINDING.**
   9 sites, defined nowhere — **and never defined in `../sdb64` either**, so it
   is dead in both trees and there is no upstream defect (on a case-sensitive
   Linux filesystem, off is correct). The 9 split into two **competing
   strategies** for the same problem, and only one can be right:

   a. **`dh_open.c:529` — make the COMPARISON case insensitive.** One site.
      Sets `DHF_NOCASE` on directory files. **This is the one that was taken.**
   b. **The other 8 — normalise every path and id to UPPER case** so that
      case-sensitive comparisons agree with the filesystem: `dh_misc.c:143`,
      `op_dio2.c` at 634 (`!OSPATH` input), 726 (`OS_CWD` output), 788
      (directory listings), 916 and 928 (both `OSRENAME` paths), `op_dio4.c`
      1154 and 1285 (`SELECT` over a directory file). **Left off, because
      §5.12 chose lower case** — upper-casing every path is the opposite of
      the goal, and it is user-visible: `OS_CWD` would start answering
      `C:\PROGRAMDATA\SD`. It also buys nothing on Windows, where the
      filesystem already matches case-insensitively without being asked.

   **DEFINING THE MACRO WOULD THEREFORE HAVE BEEN WRONG** — it would have taken
   (a) and (b) together. (a) is now unconditional instead, per CLAUDE.md's rule
   against `#ifdef` branches, and the macro name now governs only (b).
   `op_dio4.c:1155` already guards on `Option(OptSelectKeepCase)` and
   `op_dio4.c:1285` does not, so (b) is not even internally consistent.

   **WHY (a) MATTERS:** a directory file's record ids **are** file names, and
   NTFS resolves `SUE` and `sue` to one file — so without it SD takes **two
   record locks** (`op_lock.c:996`) and **two transaction cache entries**
   (`txn.c:302`) on what is one file. It does **not** change reads or writes:
   `dir_read`/`dir_write` open by name and NTFS was already case insensitive.

   **Nothing is persisted by it.** Directory files have no header, so the flag
   lives only in the shared `FILE_ENTRY`; dynamic files still take theirs from
   disk (`dh_open.c:549`). No format change, nothing to migrate, and it cannot
   corrupt an existing database.

   **VERIFIED 17 Aug 2026 on the 20:10:31 install — `DIRFILE=1`, `DHFILE=0`,
   `gplbld/verify-nocase.ps1` exit 0, unelevated.** §4 has it. The measurement
   is one command, no account creation, nothing to clean up by hand.

   **CORRECTION, same session:** this entry first said the decisive observable
   was a lock on `sue` colliding with one on `SUE` and so "needs two concurrent
   sessions". **That was wrong, and it confused the change with its
   consequence.** What this port changed is whether `DHF_NOCASE` is *set*;
   `op_lock.c` has honoured the flag since long before the port. So the
   decisive reading is `FILEINFO(f, FL$NOCASE)` — one session, one account.

   **THE DYNAMIC FILE IS THE CONTROL.** A directory file answering 1 proves
   nothing alone; `VOC` takes its flags from its own header (`dh_open.c:549`),
   untouched here, so it must still answer 0. One moves, one does not.

   **BEFORE, measured by hand on the 17:36:21 install** (pre-change binary):

   ```
   DIRFILE=0     BP,  a directory file      -> must become 1
   DHFILE=0      VOC, a dynamic file        -> must stay   0
   ```

   **The probe is placed by writing a file, not by driving `ED` through a
   pipe** — `BP` *is* a directory file, so a record is just a file on disk.
   That trick is what makes this cheap, and it is worth remembering for any
   future test that needs BASIC on an installed system.

   **`changelog` ENTRY WRITTEN 17 Aug 2026, once the flag was observed.**

   **IT DESCRIBES THE LOCK COLLISION, WHICH IS INFERRED AND NOT OBSERVED — be
   straight about that if it is ever queried.** What was measured is that the
   flag is SET. That locks then collide follows from `op_lock.c:996`, which
   case-folds the id with `memucpy` when the flag is on, so two sessions
   locking `sue` and `SUE` produce one folded id and one lock entry. Sound, and
   still a reading of source rather than a measurement. A two-session `READU`
   test is the thing that would close it.

   **THE BASIC LAYER HAD THE SAME DEFECT AND IT IS NOW FIXED AND VERIFIED —
   17 Aug 2026, 20:34:04 install, behaviour as well as flag (§4).** `op_sys.c` `case 91` (`SYSTEM(91)`, "Windows?") answered
   **0**, inherited from `sdb64` where it is correct, so every BASIC program
   asking whether it is on Windows was told no — on Windows. Now 1.

   **What that actually broke:** `QPROC:82` reads it into `is.windows` and
   `QPROC:499` is `if is.windows and is.dir then is.case.insensitive = @true`
   — **the only route** by which the query processor treats a directory file's
   ids as case insensitive. `FL$FLAGS` cannot supply it: `op_dio2.c:439`
   answers `FL_FLAGS` only when `(dynamic && internal)`, and a directory file
   is neither, so `QPROC:498` reads 0 for one however the flag is set. **So
   `SELECT ... WITH @ID = "sue"` never matched record `SUE`**, and the code to
   make it match has sat there unreachable.

   **Same shape as `CASE_INSENSITIVE_FILE_SYSTEM`**: correct code, already
   written, never switched on. `is.case.insensitive` upper-cases both sides of
   a comparison only (`QPROC` 4034, 4447, 7059, 7198) and stores nothing, so it
   is the same strategy as (a) and not the upper-casing §5.12 rejected. The
   only other reader, `APISRVR:954`, is commented out. **`ISWIN` moved 0 → 1
   across the two installs and the `SELECT` behaviour was measured with its
   control; `verify-nocase.ps1` carries the row.** `changelog` entry written.

   **THE TERMINAL HALF IS NOT STARTED, AND THE EVIDENCE CONTRADICTS THE
   SOURCE. DO NOT CHANGE IT UNTIL THAT IS RESOLVED.** `case_inversion` is XOR
   `0x20` — true inversion, not force-upper (`op_tio.c:1133`) — and **three**
   places set it TRUE, not the one §5.12 implies: `linuxio.c:240`
   (`start_connection`), `linuxio.c:313` (`init_console`) and `LOGIN:266`.
   `LOGIN:266` is **unconditional** — the `if/else` opened at 233 closes at
   264 — and LOGIN demonstrably runs, because `WHO` answers `2 DON`.

   **Yet `SYSTEM(1001)` reads 0.** Measured repeatedly, 17 Aug 2026, on the
   20:34:04 install. Something either does not run or resets it, and which is
   not known. **A change made on top of this would be a change made on top of
   a contradiction.**

   **18 Aug 2026 — THE THING THIS STEP SAID TO ESTABLISH FIRST IS ESTABLISHED:
   INVERSION IS OFF FOR THE SESSIONS REAL USERS GET, AND THAT IS WHAT §5.12
   WANTS.** On the 07:28:34 install, three independent readings agree:

   ```
   SYSTEM(1001)                      0          op_sys.c case 1001
   PTERM DISPLAY                     Off        op_pterm, a different opcode
   SH New-Item -ItemType File ...    ran        mixed case reached PowerShell
   ```

   **The third is the one that settles it.** The `verify-osusers.ps1` probes
   send a mixed-case command through the input path; with inversion on it would
   have arrived as `nEW-iTEM -iTEMtYPE fILE`, and instead it created its marker.
   That is behaviour, not a flag reading, and it cannot be an instrument fault.

   **So the terminal half is a DEAD-SETTER cleanup, not a behaviour change.**
   SD accounts are ssh-only and ssh gives SD piped stdin, so 0 is the reading
   for every account that can log in. Nothing has to change for §5.12; removing
   the three setters is tidying.

   **RESOLVED, 18 Aug 2026, AND IT IS CONFIGURATION RATHER THAN A DEFECT: THE
   VOC `LOGIN` PARAGRAPH TURNS IT OFF AFTERWARDS.** `NEWVOC/LOGIN` is a `PA`
   record, copied into every account VOC, and it reads:

   ```
   PA
   TERM LINUX
   TERM 120,36
   PTERM CASE NOINVERT      <- this line
   ```

   `CPROC:397` runs it at session start and **`CPROC:2701` runs it again on
   every `LOGTO`**. So `LOGIN:266` does execute and does set the flag TRUE;
   the paragraph runs later and wins. Confirmed live with `CT VOC LOGIN`.

   **SO THE SETTERS ARE NOT DEAD, THEY ARE OVERRIDDEN — and the previous
   entry's "dead-setter cleanup" was wrong.** Nothing in C or in `$LOGIN`
   needs removing, and **the authoritative place to change this behaviour is
   the paragraph**, in `NEWVOC/LOGIN` and `VOC_TEMPLATE/LOGIN`. Inversion
   being off is deliberate and shipped, which is what §5.12 wants, so **§7
   step 8's terminal half needs no work at all.**

   **THE VISIBLE PROOF, worth keeping because it is how this was cracked:**
   with inversion on, an upper-case command echoes back lower case.
   `PTERM CASE INVERT` then `LOGTO DON` echoed as `logto don`, and the command
   after it echoed upper case again — so the flag was on, `LOGTO` turned it
   off, and no banner appeared, meaning `$LOGIN` had not re-run.

   **LINE 2 IS NOW `TERM VT100`, owner's decision 18 Aug 2026** — it said
   `TERM LINUX`, inherited from the Linux original, and `TERM` confirmed the
   session device really was `linux`. Changed in `NEWVOC/LOGIN` and
   `VOC_TEMPLATE/LOGIN`, **byte-for-byte** (`TERM LINUX` and `TERM VT100` are
   both 10 characters, so no record framing moved — and the two files differ,
   `NEWVOC/LOGIN` having no trailing newline where `VOC_TEMPLATE/LOGIN` has
   one). `vt100` is shipped in SD's own terminfo and `TERM VT100` was checked
   on the 07:28:34 install before the edit: `Device : vt100`, no error.
   **NOT YET INSTALLED — needs a cycle.**

   **An existing account keeps `linux` until its VOC is updated**, and then
   picks it up silently: `update.voc` only prompts when the record TYPE
   changes (`LOGIN:613`) and both are `PA`, so `LOGIN:657` just writes it.

   **EIGHT CANDIDATES WERE ELIMINATED GETTING HERE, kept so nobody re-walks
   them.** 18 Aug 2026: (1) `PT$INVERT` and
   `PT_INVERT` disagreeing — both 2, `INT$KEYS.H:146` and `keys.h:181`;
   (2) `LOGIN` not including `int$keys.h` — it does, line 73; (3) two copies of
   `case_inversion` — `Public` is `extern` (`sddefs.h:261`) everywhere but
   `sd.c`, so there is one; (4) the instrument — two opcodes and behaviour
   agree; (5) the early `return` at `LOGIN:198` skipping line 266 — that is the
   `mode = 2 or 3` VOC-upgrade path, and the banner at `LOGIN:209` proves it
   was not taken; (6) `@TRUE` being negative and so meaning "report only" —
   it is 1, measured; (7) the setter being broken — `PTERM CASE INVERT` turns
   it On in the same session and it stays On; (8) `SET_PASSWD` resetting it at
   login — it is called from `CREATEA` and `PS_SCRIPT`, not `LOGIN`.

   **A SEPARATE REAL DEFECT, FOUND ON THE WAY AND NOT FIXED: `SET_PASSWD`'s
   case-inversion save/restore can never restore On.** `op_pterm`'s own stack
   diagram says the value returned is the **NEW** value, and a **negative**
   argument is what reports without setting. So `SET_PASSWD:88`
   `was.inverted = pterm(PT$INVERT, @false)` sets it off and saves the *off* it
   just wrote, and `SET_PASSWD:98` restores that. The fix is to read with
   `pterm(PT$INVERT, -1)` first, then set. **Harmless today only because
   inversion is already off everywhere**; it is latent, and it is ours — the
   lines carry a `14 Aug 26 Windows port` marker — so no `UPSTREAM_FIXES.md`
   entry.

   **WHAT WAS NARROWED, 17 Aug 2026, so the next attempt starts further on:**

   - `connection_type` **defaults to `CN_CONSOLE`** (`kernel.h:54`); only
     `-pipe`-style and socket invocations move it (`sd.c` 407, 423, 471). So a
     plain `sd.exe` is `CN_CONSOLE` and `op_tio.c:3258` should reach
     `init_console()`.
   - **The console path refuses an ordinary user**, measured: `sd.exe RUN BP X`
     with no pipe answers *"This command needs an elevated session"*. That is
     §5.6.2 working as designed, and it is why the console reading cannot be
     taken unelevated.
   - **The piped path is the one that matters anyway.** SD accounts are
     ssh-only, and ssh gives SD piped stdin — so the 0 above is the reading for
     the sessions real users get. **If it is 0 there, §5.12's terminal concern
     may already be satisfied for every account that can actually log in**, and
     the work would be removing three dead setters rather than changing
     behaviour. That is the thing to establish first.
   - `pterm()` **cannot be called from a user account** — internal only, and
     compiles as *"Matrix PTERM is not referenced in a DIM statement"*.
     `SYSTEM(1001)` is the route from a probe.

   **AND 707 `upcase(` CALLS IN `GPL.BP` ARE NOT ALL IN SCOPE.** Most are VOC
   verb lookup, `Y`/`N` answers and record types, which must stay — CPROC
   upcases verbs so lower-case typing still finds `LISTF`. The account-name
   subset is about 11 sites: `LOGIN` 281, 321, 339, 383, 690 and `CPROC` 2531,
   2577, 2579, plus the audit lines 2601, 2619, 3686.

   **WHAT IS LEFT of step 8** is the wide half §5.12 describes: account names
   (`LOGIN`, `CPROC`, the `$CRED` register), dictionary and VOC ids, and — added
   by the owner 18 Aug 2026 — **the file names themselves, `VOC` and `BP`
   included**. (a) is the enabling change for the account half — `$CRED` and
   `ACCOUNTS` are directory files — but removing the `upcase()` calls is still
   what makes `sue` and `SUE` one account, and that is untouched. **The
   terminal's `PT$INVERT` is NO LONGER on this list**: it is off already and
   deliberately, see above.

   **18 Aug 2026, TWENTY-THIRD SESSION — THE FALLBACK IS FINISHED AND THE FIRST
   RENAMES ARE IN.** The fold reached only the parser; `_VOC_REF`, which every
   BASIC `OPEN` goes through, had no fold and is now converted
   (`verify-fold.ps1` 10/10). §5.12 (a) is done for the per-account files —
   `$hold`, `$hold.dic`, `$svlists`, `bp` (`verify-lcnames.ps1` 26/26). **What
   is left of the file-name half is (b), the VOC ids, and the shipped system
   files**, which need `stage.py`, `sd.iss` and four verify scripts to move with
   them. The account-name half is untouched.

   **18 Aug 2026, TWENTY-FOURTH SESSION — THE FIRST VOC ID HAS MOVED.**
   `$SAVEDLISTS` is `$savedlists` (`verify-lcnames.ps1` 36/36, 20:34:25
   install), and §5.12 (b) now has a worked example to copy: what moves with a
   rename, and the verifier section that proves an account created before it
   still works. **`$HOLD` next, then `$COMMAND.STACK` and `BP`**; the shipped
   system files stay the wide half. The account-name half is still untouched.

   **THE FALLBACK IS DONE, SO A RENAME NO LONGER NEEDS ONE.** The fold was "as
   typed, then upper"; it is now as typed, then down, then up, at the 74 parser
   sites and in `_VOC_REF`. **Read §5.12 before the next rename** — it has the
   sites, the measurements, and the two instruments that are not obvious:
   `CT` echoes the id it matched (so "not found" cannot test a rename), and the
   pre-rename account has to be simulated rather than assumed.
9. **Let a scheduled job log in** (§8). The allowlist and the batch account
   that grants nobody. Not urgent — the install half of the problem is solved
   by ordering (step 3) — but it is what MV users expect and it needs no new
   C code. Build it against the constraints written into §8, particularly the
   no-arguments rule, which is the part doing the security work.
10. **Write the admin helpers** (§5.14). Forms over the administrative work
    that is command lines and hand-edited records today, once the system runs
    well enough to be worth using. The sequencing note matters more than the
    step: put administrative logic in subroutines from now on, so a form can
    call it later without reimplementing it.
11. **BUILT AND WORKING — 17 Aug 2026, seventeenth session. VERIFIED ON THE
    12:28:49 INSTALL**, `make check-local` on the installed pair,
    `assert-current` exit 0, `WHO -> 2 DON`. The measurements are in this step's
    body and in §4.

    ***"AND NOT RUN" stood here until 21 Aug 2026; "CALLED, AND IT DOES NOT
    WORK" replaced it that day and was stale too** — both were refuted by this
    entry's own body, which reports the transport being replaced and the test
    passing. The half-correction is why it survived a sweep. Struck 21 Aug 2026
    in both places.*

    **The heading it carried is still the right way to read what follows**:
    `SDConnectLocal()` as originally written **could never have worked**, on
    this platform or any other, and it took three independent faults with it.
    Two were in the shipping path and are fixed; the third was in dead code.
    **A fourth thing was not a defect and is what forced the transport
    change** — the always-ready `select()`, below.

    a. **The client and the server disagreed about `-C`.** `SDConnectLocal()`
       builds `sd.exe -Q -C \\.\pipe\~SDPipe<pid>-<n>` — the pipe name as a
       SEPARATE argument — while `sd.c` parsed `sscanf(argv[arg],
       "-C%d!%d", …)` and `exit(1)`ed on anything else. `argv[arg]` is exactly
       `"-C"`, so it matched nothing and the child died during argument
       parsing. **The same mismatch is in `sdb64`**, byte for byte —
       UPSTREAM_FIXES.md #4. `sd.c` now takes either form, and **consumes the
       name argument**, which it must: the option loop stops at the first
       argument not beginning with `-`, so the pipe name would otherwise be
       taken for a command to execute.
    b. **The client looked for `sd.exe` inside the DATA tree** —
       `<sysdir>\bin\sd.exe`, i.e. `C:\ProgramData\SD\sdsys\bin`, which exists
       and holds the pcode file. It is now found **beside the DLL** through
       `GetModuleHandleEx(FROM_ADDRESS)` + `GetModuleFileName`, which needs no
       configuration and follows the install wherever `{app}` puts it, since
       `stage.py` ships both in `usr\bin`. **The path is now quoted too**: it
       is under `C:\Program Files`, and an unquoted spaced path in
       `CreateProcessA` with a NULL application name makes Windows try
       `C:\Program.exe` first — a hijack, not just a bug.
    c. **`gplsrc/sdclient.c` had a fourth fault and does not matter**: it reads
       `C:\Windows\sd.ini`, which nothing creates. **That file is excluded
       from the build** (`Makefile:66`, `SRCS := $(TEMPSRCS:sdclient.c=)`) —
       the shipping client is `gplsrc/sdclilib/sdclilib.c`, whose `sysdir()`
       was already corrected on 14 Aug. **Read the right file**: an earlier
       hour of this session was spent analysing the dead one.

    **`gplsrc/win32pipe.c` is new, and is the THIRD `windows.h` file** after
    `win32sem.c` and `win32audit.c`. The pipe is a native object created by the
    UCRT64 client and `sd.exe` is MSYS2, so `open()` cannot reach it — the
    Cygwin runtime does not map `\\.\pipe\` names at all. It is opened with
    `CreateFile` and pushed into the Cygwin descriptor table with
    `cygwin_attach_handle_to_fd()`, exported by `msys-2.0.dll` (ordinal 379,
    checked), so everything above it reads and writes 0 and 1 unchanged.

    **It must not include `sd.h`, and neither do the other two.** `sd.h`
    reaches `linuxlb.h`, which declares `GetUserNameA()` and `Sleep()` with
    types that conflict with the real Windows ones — two "conflicting types"
    errors, measured. That is why it returns `int` rather than `bool`, as
    `win32audit.h` does.

    **THE NAMED PIPE DOES NOT WORK, AND THE REASON IS ARCHITECTURAL RATHER THAN
    A BUG LEFT TO FIND. 17 Aug 2026, measured on the 08:03:49 install** — the
    transport this describes is the one that was REPLACED, later the same day,
    and the replacement is what the top of this step reports working. **Three
    real defects
    were fixed on the way and all three were worth fixing; a fourth thing is
    not a defect at all and stops this approach.

    **THE STOPPER: a descriptor made by `cygwin_attach_handle_to_fd()` is
    reported PERMANENTLY READY by `select()`** — `sel.always_ready 1` in
    `strace`, §6. SD decides whether input is waiting by asking `sdpoll()`
    (`linuxio.c:535`, `:383`, `:456`). Told "yes" unconditionally, it spins
    reading one byte at a time for ever: **`sd.exe` alive, silent, and never
    answering.** `make check-local` hung, and `SDConnectLocal("DON")` never
    returned. **Fixed by replacing the transport, not by repairing this** — see
    the top of this step; only the `-C <pipename>` convention still reaches the
    always-ready path, and `sd.c` now refuses it rather than hanging.

    **The three fixes are still right and still needed by any successor**: the
    `-C` argument mismatch, the `sd.exe` location, and the access argument
    below. None of them is undone by this.

    **BUILT AND WORKING — 17 Aug 2026. `SDConnectLocal()` CARRIES A SESSION.**
    Four runs, unelevated, `local_connect_test` exit **0** each time:

    ```
    connecting to DON ...
      admitted
      WHO -> 19 DON
    connecting to SDSYS (this MUST be refused) ...
      refused: User not allowed in requested account
    PASS: DON admitted, SDSYS refused.
    ```

    **AND THAT IS ALSO THE FIRST EVIDENCE OF ANY KIND FOR §7 STEP 6c** — the
    `ACC$GROUP` grant check in `APISRVR`, built 17 Aug and never run. **The
    control is what makes it evidence**: `DON` admitted alone would be equally
    consistent with a check that never executed, and `SDSYS` refused with
    "User not allowed in requested account" is that check running.
    **No orphaned `sd.exe` survives a run**, which is the EOF path working:
    closing our copies of the child's ends is what lets it see stdin close.

    **AND IT IS NOW VERIFIED ON A REAL INSTALL.** The first measurement was a
    development smoke test — the new DLL paired in a scratch directory with the
    installed `sd.exe`. **The cycle then ran and `make check-local` passed on
    the installed pair**, `assert-current` exit 0, 12:28:49 install,
    `WHO -> 2 DON`. Both runs agree; the header has the figures.

    **`make sd` clean, no warnings, both toolchains:** `sd.exe`
    **`81D0856F5493385E`**, `sdclilib.dll` **`8D1517D1CD2B83AB`**.

    **WHAT CHANGED.** All of it client-side except one refusal:

    - `SDConnectLocal()` makes **two anonymous pipes** and hands them to the
      child as its **standard handles**; `session[].hPipe` became `hPipeRd` /
      `hPipeWr`, because an anonymous pipe is one-way and the pair is what the
      duplex named pipe used to be alone.
    - The command line is now **`-Q -C1!0`**. **Note the order** — `sd.c`
      parses `-C<tx>!<rx>` and answers with `dup2(RxPipe, 0); dup2(TxPipe, 1)`,
      so rx must be 0 and tx must be 1. `-C0!1` would cross the streams, and an
      earlier note in this file said exactly that; it was wrong.
    - **Inheritance is restricted to exactly those two handles** with
      `PROC_THREAD_ATTRIBUTE_HANDLE_LIST`. Plain `bInheritHandles = TRUE`
      inherits **every** inheritable handle the process owns, and this library
      is loaded into somebody else's application — a handle it happens to hold
      to a file or a socket would be copied into a long-lived `sd.exe` and kept
      alive for the whole session, with nothing to show why.
    - `sd.c`'s **`-C <pipename>` branch now refuses with a diagnostic** instead
      of hanging. The code behind it is correct and the flaw is not in it, so
      `win32pipe.c` stays; but silent-and-never-answering is the worst thing to
      leave callable.
    - `ConnectNamedPipe` and `DisconnectNamedPipe` are gone: an anonymous pipe
      is connected the moment it exists.

    **The reasoning that got here, kept because the framing was the error:**

    **FIRST, THE FRAMING WAS WRONG: THE PEER IDENTITY NEVER CAME FROM THE
    PIPE.** There is no `ImpersonateNamedPipeClient` and no
    `GetNamedPipeClientProcessId` anywhere in `gplsrc` — checked.
    `SDConnectLocal()` gets identity because it **spawns `sd.exe` with
    `CreateProcessA`**, so the server is a CHILD running under the caller's own
    token and `GetUserNameA()`/`IsElevated()` inside it report the calling user.
    The named pipe only carries bytes. **So the socket option's stated cost is
    illusory — and so is the named pipe's stated benefit.**

    **THE THIRD OPTION: hand the child inherited pipe handles as its STANDARD
    HANDLES** — `CreatePipe` twice, `STARTUPINFO.hStdInput`/`hStdOutput`,
    `bInheritHandles = TRUE` — instead of opening a named pipe after the fact.
    Cygwin then builds descriptors 0 and 1 itself at startup, sees
    `FILE_TYPE_PIPE`, and installs its pipe handler, whose `select()` is
    `PeekNamedPipe`-based and answers honestly.

    **MEASURED, with the control in the same process and the same run** —
    `make check-select-probe`, `gplsrc/sdclilib/tests/select_probe_*.c`,
    identical on four runs:

    ```
    inherited(fd 0)  empty=0  data=1     <- select() tells the truth
    attached(fd 4)   empty=1  data=1     <- always ready: the stopper
    inherited read: [HELLO-INHERITED]    <- and it reads
    ```

    **The control is what makes it mean anything**: both descriptors were
    measured by the same `select()` call with the same timeout, milliseconds
    apart, in one Cygwin child spawned by one native parent. The only
    difference is how the descriptor was made. **`empty=0` is the whole
    finding** — always-ready is a property of injecting a RAW HANDLE, not of
    pipes.

    **IT NEEDS NOTHING IN THE SERVER.** `sd.c:441` already accepts
    `-C<tx>!<rx>` and does `dup2(RxPipe, 0); dup2(TxPipe, 1);`, so with the
    handles arriving on 0 and 1, **`-C0!1` is a no-op `dup2` that just sets
    `CN_PIPE`**. `win32pipe.c` leaves the hot path. The change is client-side
    only and REMOVES code rather than adding a `CN_PIPE` branch through the
    input layer.

    **NOT YET CHECKED:** how `-Q` / `is_sdApiSrvr` behaves with stdin and
    stdout as the protocol channel rather than a terminal. Read that before
    writing code.

    **The two options as originally framed, kept because they are the fallback
    if the above meets something:**

    - **Give `CN_PIPE` its own I/O.** Read and write the HANDLE with
      `ReadFile`/`WriteFile` and answer readiness with `PeekNamedPipe`, instead
      of borrowing descriptors 0 and 1 and `sdpoll()`. Contained — `CN_PIPE`
      is in only TWO places in the server (`sd.c:423`, `op_tio.c:3902`) against
      a dozen for `CN_SOCKET` — but it means a `CN_PIPE` path through the input
      layer. **Prefer this over the socket** if the third option fails.
    - **Use a loopback socket instead**, where Cygwin's `select` genuinely
      works and `CN_SOCKET` is already exercised. Cheaper, but reachable by any
      local process, so it needs authentication invented for it — new security
      surface in the one path that currently has a clean answer.

    **Do not spend another cycle looking for a flag.** Six combinations of the
    name and access arguments, `O_NONBLOCK`, and `F_SETOWN` were all measured;
    the always-ready behaviour is a property of the Cygwin file handler for a
    raw HANDLE, not a setting.

    **The failure and its diagnosis, in the order they were found:**

    - **Observed:** `SDConnectLocal("DON")` → `Connection closed by server`,
      test exit 1.
    - **The pipe was fine.** A probe standing in for the client showed
      `sd.exe` opening the pipe and then exiting **0** — not a crash, not
      `exit(1)`, and **silent on both streams**.
    - **THE PREDICTION IN THIS STEP WAS WRONG.** It said the likely fault was
      `cygwin_attach_handle_to_fd()` not honouring a requested descriptor
      number. It honours it exactly, measured.
    - **The real fault: its access argument must MATCH THE HANDLE**, not
      describe what the descriptor is for. The handle is opened
      `GENERIC_READ | GENERIC_WRITE`, so **both** calls must pass that.
      Passing `GENERIC_READ` for descriptor 0 — the obvious thing to write —
      **succeeds**, and the descriptor then fails `read()` with `EBADF`.

    - **After that fix `sd.exe` STOPPED EXITING and started hanging**, which
      was progress and was also the next symptom. `strace` then showed the
      always-ready loop above, which is the stopper.

    **HOW IT WAS FOUND, AND THIS IS THE REUSABLE PART. Two tools, neither of
    them an install cycle:**

    - **A standalone probe** — twenty lines of C built with MSYS2 gcc outside
      the repository, driven by a PowerShell harness acting as the pipe
      server — settled the access argument by trying six combinations against
      a real pipe with real data. **When the unknown is one library call,
      isolate the call.**
    - **`strace`, which is in MSYS2 at `/c/msys64/usr/bin/strace.exe`** and
      works on any Cygwin binary, `sd.exe` included:

      ```sh
      strace -o log.txt -- "C:\Program Files\SD\usr\bin\sd.exe" -Q -C \\.\pipe\NAME
      ```

      **It answered in one run what three cycles could not**, because the
      failing path prints nothing, exits nothing, and lies through `poll()`.
      There is no `gdb` in this MSYS2 install; `strace` is the tool to reach
      for. Both harnesses are worth rebuilding if this is picked up again.

    **`make sd` clean, no warnings**, both toolchains, `sd.exe`
    **`04CA97C138ADB148`** as installed at 08:03:49.

    **The vendored client's own docs were wrong and are corrected**: both
    `README.md` and `USER_GUIDE.md` said the Windows DLL does not provide
    `SDConnectLocal` and that it is "Linux-specific". It is exported —
    ordinal 6, checked with `objdump -p` — and its transport is a **named
    pipe**, which has no Linux equivalent in that library at all.

    ~~**THE TEST IS WRITTEN AND COMPILES; IT HAS NOT BEEN RUN.**~~ **IT HAS
    RUN, FIVE TIMES** — four development runs and once on the installed pair at
    12:28:49, all exit 0. Struck 21 Aug 2026 with the other two claims of the
    same kind in this step. `gplsrc/sdclilib/tests/local_connect_test.c`, clean
    under `-Wall -Wextra -Wpedantic`. **Re-run it after any cycle, UNELEVATED:**

    ```sh
    cd sdb_ai/sd64 && make check-local
    ```

    **It carries its own control, and the control is the reason to trust it:**

    | account | expected | why |
    |---|---|---|
    | `DON` | admitted | `ACC$GROUP` is `sdu_don` and `GITORLI\don` is a member — both checked on the installed tree |
    | `SDSYS` | **refused** | `ACC$GROUP` is `sdsys`, which is not a Windows group |

    **`DON` succeeding on its own would prove nothing** — a grant check that
    never ran would admit it too. Exit codes say which happened: 1 `DON`
    refused, 2 `SDSYS` admitted (so the check did not run and the first result
    is worthless), 3 the session opened but `WHO` failed.

    **It is deliberately NOT in `make check`.** Everything there runs without a
    server; this measures the INSTALLED tree and is therefore subject to the
    cycle rule.
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

    **WHAT TO ACTUALLY DO**, and it is smaller than the old wording suggested:

    - Source is `C:\Users\dmont\Projects\GPL.BP` — 212 files, 25 with platform
      references. **The idiom is a bare `windows`**, set by
      `windows = system(91)` (`CPROC:251`, `LOGIN:91`) — *not* `is.windows`,
      which is why grepping for that finds nothing and looks like the logic is
      gone. Uses in the five stripped files: `LOGIN` 4, `CONFIG` 3, `CPROC` 3,
      `CREATEA` 4, `PARSER` 2.
    - Start at `CPROC`'s `dir.separator` — shipped `= '/'` (`CPROC:290`),
      original `= if windows then '\' else '/'` (`CPROC:323`) — because `@ds`
      is SYSCOM slot 57 and compilation depends on it: `BCOMP` opens
      `@sdsys:@ds:'bin'`. **`/` is what works today on the MSYS2 runtime**, so
      the burden is on changing it, not on keeping it.
    - **DO NOT TAKE EVERY WINDOWS ARM BLIND.** `LOGIN`'s forced administrator
      rights on any console session, which **§5.6 rejects on purpose**. Judge
      each arm against the port's own decisions.
13. **Stage 2, native Win32.** `fork` → `CreateProcess` (all five call sites
    are fork+exec, none need copy-on-write, so this is tractable), `termios` →
    Console API, passwd/group → Windows authentication. **The service-account
    model in §5.7 belongs here**, and until it lands the data tree is not
    genuinely private from SD's own users.

## 8. Open questions

The identity question that stood here — admin flag inside SD, or OS group — was
**answered on 13 Aug 2026** and is now §5.6. Neither option was taken. See the
HISTORY entry "Identity, install layout and data protection decided" for the
reasoning and for the corrections to the evidence that was recorded here.

### BUILT AND VERIFIED, 20 Aug 2026: `RDPACCOUNT` (decided 18 Aug, owner)

**IT SHIPPED AS `RDPACCOUNT`, NOT `RDPUSER`** - owner, 20 Aug: *"we don't
have users just accounts"*. Everything below this line was written before
that rename and before it was built, and uses the old spelling; it is kept
as the record of how the decision was reached. **The header of this file
has what was actually built, and what it measured.**

**THE BLOCKER NAMED IN THIS SECTION IS GONE** - the per-account ACLs are
done and verified (`verify-accountacl.ps1`). **Difficulty 1 was decided by
deriving rather than recording**, difficulty 2 was built (`MODIFY.ACCOUNT`
gained `RDPACCOUNT`/`NO.RDPACCOUNT`), and difficulty 4 is closed - the
`sd.c` comment is rewritten. **Difficulties 3, 5 and 6 remain open**:
`sd LISTF` from a desktop, user counting across RDP sessions, and §5.6.2's
rewrite into a three-way rule.

**Owner's decision, 18 Aug 2026.** A new `CREATE.ACCOUNT` keyword, orthogonal
to the tier rather than a fourth one:

```
CREATE.ACCOUNT USER jim RDPUSER              standard tier, may sign in to Windows
CREATE.ACCOUNT USER jim PROGRAMMER RDPUSER   programmer tier, may sign in to Windows
```

They hold an ordinary Windows account, may run other Windows programs, reach the
API **without an ssh tunnel**, and reach a terminal session directly.

**MECHANICALLY IT IS SMALL, AND TWO OF THE THREE CAPABILITIES NEED NO CODE.**

- **Skip the `sdsshonly` add.** That group is what carries
  `SeDenyInteractiveLogonRight` and `SeDenyRemoteInteractiveLogonRight`
  (`deny-logon.ps1:29`), and `CREATEA:491` already branches for exactly this
  (`if adopt or is_grp_member(... "S-1-5-32-544")`). The keyword is a third case
  on a test that exists.
- **The terminal works already.** `sd.c:582`: *"Plain `sd` with nothing after it
  is untouched: that is how a user reaches their own account."* `check_admin()`
  gates a command **on the command line** (`sd LISTF`), not an interactive
  session. So "without ssh" needs nothing built.
- **The API works already.** The listener is on 127.0.0.1; `ssh -L` only ever
  existed to carry that across a network, and a client in an RDP session is
  already on the loopback. `$CRED` + `ACC$GROUP` still gate it.

**THE BLOCKER, AND IT IS MEASURED, NOT ARGUED — §8's "B work" IS NOW A
PREREQUISITE.** Every path in the data tree except four inherits
`sdusers:(OI)(CI)(M)`. Measured unelevated, 18 Aug 2026:

```
sdsys                     sdusers:(I)(OI)(CI)(M)
sdsys\gcat                sdusers:(I)(OI)(CI)(M)     <- the compiled system programs
sdsys\GPL.BP.OUT          sdusers:(I)(OI)(CI)(M)
sdsys\NEWVOC              sdusers:(I)(OI)(CI)(M)
user_accounts             sdusers:(I)(OI)(CI)(M)     <- and every account inside it
user_accounts\don         sdusers:(I)(OI)(CI)(M)     <- inherited, NOT per-account
audit, $CRED, PSTMP       Access is denied           <- these four do hold
OS.USERS                  sdusers:(OI)(CI)(RX)
```

**`gcat` is the sharp one.** It holds `$LOGIN` and `$CPROC` as object code, and
`CPROC:315` calls `$LOGIN` for every session. Modify on it means overwriting
`$LOGIN` and **running your code in everybody's session, administrators
included.** Any SD user also has Modify on every other user's account directory.

**What keeps that shut today is precisely what `RDPUSER` removes.** A standard
account cannot reach a filesystem at all: no console and no RDP (`sdsshonly`),
and ssh lands it inside SD through `ForceCommand`. `RDPUSER`'s whole purpose is
to hand it a desktop, and from a desktop this is Explorer, not an exploit.
**So the per-account ACLs (§5.7, §8 "the B work") stop being the thing the tier
work is blocked on and become the thing `RDPUSER` is blocked on.**

*(Partly reachable already: `OS.EXECUTE` is ungated for everybody (§4), so a
PROGRAMMER with `BASIC` can do this today without a desktop. `RDPUSER` widens it
to STANDARD accounts and makes it trivial. That is an argument for fixing the
ACLs, not for treating the new keyword as harmless.)*

**LOCAL ssh DOES NOT MITIGATE IT, and is not worth the complexity.** The owner
offered it as a fallback if direct terminal access is too risky. It would restore
`ForceCommand`, but a desktop user can run `C:\Program Files\SD\usr\bin\sd.exe`
directly and Program Files is read-and-execute to `Users` — so it adds an
authentication step and no containment. **The risk above is filesystem access,
which local ssh does not touch.**

**SMALLER DIFFICULTIES, none of them blocking:**

1. **Where "may RDP" is recorded.** The tier lives in `ACCOUNTS` field 5, inside
   SD; RDP-ness would live in a Windows group's *absence*, outside it. So SD
   cannot report it, `LIST.ACCOUNTS` cannot show it, and the two can drift if
   somebody edits the group by hand. Either mirror it into `ACCOUNTS` and accept
   the drift, or have SD ask the group. **Decide before building.**
2. **`MODIFY.ACCOUNT` needs the same keyword**, or the class is create-time only.
3. **`sd LISTF` from an RDP desktop is refused while `sd` then `LISTF` works** —
   `check_admin()` at `sd.c:585` gates the command-line form. Defensible, but the
   inconsistency only becomes visible with this class of user.
4. **The comment at `sd.c:570-573` becomes false.** It justifies that gate with
   *"whoever is at the console or on Remote Desktop is an administrator, because
   SD's own accounts are confined to ssh"*. The gate can stay; the reasoning
   beside it must be rewritten or it will mislead the next reader.
5. **User counting** — several RDP sessions each running clients
   (`MESSAGES/1000`, "User limit reached") is unexamined.
6. **§5.6.2 needs rewriting** from "the console belongs to administrators" into a
   three-way rule.

**RECOMMENDATION, for the owner to overrule if he wants it sooner:** take the
per-account ACLs first, then add the keyword. The keyword is perhaps an hour;
shipping it before the ACLs converts a documented weakness into a reachable
privilege escalation for the least trusted class of account.

### Superseded background: the same question as first raised (18 Aug 2026)

Owner's question, 18 Aug 2026: SD on Windows Server, a remote user arrives by
**RDP**, and runs an SD API application **without an ssh tunnel**; ordinary
users stay standard accounts. Is it possible? **Yes, and most of it is already
true — but it changes one security property, and that is the part to decide.**

**1. THE TUNNEL WAS NEVER ABOUT THE API, SO THERE IS NOTHING TO REMOVE.** The
listener binds to **127.0.0.1** (§7 step 6, asserted in the same run that proved
the transport). `ssh -L` exists to carry that loopback port **across the
network**; a client running INSIDE an RDP session is already on the machine's
loopback. The API's own gate is untouched and still applies — `$CRED` password
plus the `ACC$GROUP` account test, with two distinct refusal messages (§4). So
"no ssh tunnel" is a consequence of where the listener binds, not a change.
Note `APIPORT` is **not** in `sd.conf` by default; turning it on is deliberate.

**2. THE BLOCKER IS ONE LOGON RIGHT, AND IT IS ALREADY GROUP-SCOPED.**
`deny-logon.ps1` sets `SeDenyInteractiveLogonRight` **and
`SeDenyRemoteInteractiveLogonRight`** — the second one *is* Remote Desktop — so
an SD account cannot RDP in today, by design. But it is applied to
**`sdsshonly`**, which is a *different group* from `sdusers` (`sd.iss:701`). The
fourth user type is therefore **"in `sdusers`, not in `sdsshonly`"** and needs
no new enforcement mechanism.

**`CREATEA` ALREADY HAS THE EXEMPTION AND ANTICIPATED THIS.** `CREATEA:491` is
`if adopt or is_grp_member(acc.uname, "S-1-5-32-544")` — skip the `sdsshonly`
add — and its comment says the test sits there "so the next route inherits the
protection instead of rediscovering the lockout". This is that next route. What
it needs is a **`CREATE.ACCOUNT` keyword** naming the class, not new plumbing.

**3. WHAT IT COSTS, AND IT IS THE ONLY REAL DECISION HERE.** Today *"anyone who
can be local is an administrator"* is true **by construction** — everyone else
is denied both interactive and remote interactive logon. **Binding the API to
loopback is safe because of that, not on its own.** Admit non-administrator
desktop users and "local" becomes a much larger set, so the entire boundary
becomes `$CRED` + `ACC$GROUP`. §8's posture-B note already says the quiet part:
*binding to loopback is not the same as authenticating the peer*, and names the
Windows answer — a **named pipe** with `GetNamedPipeClientProcessId`, for which
`connection_type` already has `CN_PIPE`. **This proposal is what makes that
work worth doing rather than theoretical.**

**Not decided, and not started.** Also unexamined: several concurrent RDP
sessions each running a client is a user-count question (`MESSAGES/1000`, "User
limit reached"), and §5.6.2 would need rewriting from "the console belongs to
administrators" to a three-way rule.

### CLOSED: the LEFT ARROW in a Windows console (raised and settled 19 Aug 2026)

**Cause found, fixed and measured — §5.18.** It was not the `_KEYCODE` change
and it was not a mystery about what the console sends: the default terminal
type was `vt100`, whose arrows are the application-cursor-mode spellings, and
**SD never sends `smkx`, so that mode is never entered**. Every arrow was dead,
not only Left. The default is now the new `windows` type. `verify-keys.ps1`
section 3 is the standing guard, 10/10 on the 10:06:08 install.

**The hypothesis recorded here was right and the proposed probe was not needed**
— the question "what does the console send?" was answered from the protocol
instead: `\EOD` is *by definition* only sent in a mode nothing turns on.

### Open: how many kinds of user does SD have, and what enforces each (raised 16 Aug 2026)

Owner's model, three tiers: **application users** dumped into a menu, never
seeing `:`, holding object code and no source; **programmers**, at the prompt,
with read/write/catalog/execute/create/delete in their own account and any
`GRANT`ed account including a shared-program one, needing *some* `SH`;
**db administrators**, everything. In Pick the last two were the same because
Pick *was* the OS. §5.6.1 already split them here, so deviating is not new.

**THE TWO TIERS THAT EXIST TODAY ARE ENFORCED BACKWARDS**, and this is the
finding to act on before designing more of them:

- `SH` at the prompt is gated on `IsElevated()`, and an ssh session **can never
  be elevated** — so no ssh user ever gets `SH`, including the programmers who
  need it.
- `OS.EXECUTE ... CAPTURING` is **ungated** (§7 step 7, measured with a
  control) — so anyone who can write and run a program has full OS execution
  under their own token.

So the visible control is denied to the people who need it and the capability
it guards is open to everyone who does not. **Tiers 1 and 2 have identical
actual power.**

**No privilege concept exists to hang tiers on.** Only `USR_ADMIN`
(`sysseg.h:158`), one session flag seeded from `IsElevated()` at process start.
Nothing in `SYSCOM`; `PRIVILEGED_COMMANDS` is a local in `IS_INSTALL`, not a
mechanism.

**Owner's approach, 16 Aug 2026: capability by VOC content.** Take **`BASIC`,
`CATALOG`, `RUN`, `ED` and `SED`** off accounts that do not need them — no
compiler, no way to catalogue, no way to run an imported object, no editor to
put any of them back with. Idiomatic MV, needs no C. Plus break off
(`OPT.NO.USER.ABORTS` exists) and `ForceCommand` on by default.

**`COPY` belongs on the list too** — it writes a record into VOC as effectively
as `ED` does. **`EXECUTE`/`PERFORM` do NOT and cannot**: corrected 16 Aug 2026,
they are BASIC statements, not VOC verbs, so they are not in the 434 and cannot
be removed. What they run still resolves through VOC, so removing `BASIC` denies
it to programs as well as to the prompt — which is what makes the whole approach
work with one mechanism.

**THREE TIERS, AND A NEW `PROGRAMMER` KEYWORD ON `CREATE.ACCOUNT`** (owner,
16 Aug 2026) beside the existing `ADMINISTRATOR`. Standard gets a reduced VOC,
`PROGRAMMER` a full one plus limited shell, `ADMINISTRATOR` everything.
**An admin can add anything back to any account**, so the reduced VOC is a
starting posture the site curates, not a wall.

**The decision space is 144 verbs, not 434** — the other 248 are `K` keywords
(query syntax) plus 15 `F`, 11 `R`, 4 `PA`, 2 `S`, 2 `Q`, 2 `PH`, 1 `X`.
First-pass split is roughly 30 admin / 45 programmer / 65 standard, so
**`PROGRAMMER` sits much closer to `ADMINISTRATOR` than to standard**: the real
line is between running an application and building one.

**Owner's rulings, 16 Aug 2026:** `MICRO` **removed** — it launches an external
editor, so it is a containment escape of the same class as `SH`. Language verbs
**removed**, SD is English only: `LOAD.LANGUAGE`, `SET.LANGUAGE`, `NLS`.

**DONE 17 Aug 2026, seventeenth session — all four are out of both VOCs.**
`VOC_TEMPLATE` 434 → **430**, `NEWVOC` 411 → **408** (`LOAD.LANGUAGE` was
already admin-only). **The four programs are KEPT and are now callerless**, as
`$CRED` and its friends are (§7 step 0): `GPL.BP/MICRO`, `NLS`, `SETLANG` and
`LOADLANG` still compile and still catalogue, and nothing can reach them.
**Checked before removing** — nothing anywhere calls `$MICRO`, `$NLS`,
`$SETLANG` or `$LOADLANG`, and `K$SET.LANGUAGE` in `INT$KEYS.H` is kernel key
38, unrelated to the verb and untouched.

**THE INVENTORY, MEASURED 17 Aug 2026, because the numbers here were slightly
wrong.** By the **first character** of field 1, which is what SD reads
(`voc.rec[1,1]`, `CPROC:3376`):

| | `VOC_TEMPLATE` | `NEWVOC` |
|---|---|---|
| **V verbs** | **149** | **136** |
| K keywords | 248 | 249 |
| F / R / P / S / Q / X | 37 | 26 |

**So the decision space is 149 verbs, not the 144 recorded above** — that count
matched the literal string `V` and missed five records whose type field is
descriptive text beginning with V. **`NEWVOC` deliberately carries descriptions
where `VOC_TEMPLATE` carries bare letters**, and `CREATEA:530` normalises them
down to the type letter on the way in, which is why both forms work.

**AND THE GAP BETWEEN THE TWO TIERS TODAY IS ADMINISTRATION, NOT CAPABILITY** —
this is §8's finding, counted. Only **23 records** are in `VOC_TEMPLATE` and not
`NEWVOC` (24 before `LOAD.LANGUAGE` went): **9 administration verbs**
(`CREATE.ACCOUNT`, `DELETE.ACCOUNT`, `MODIFY.ACCOUNT`, `UPDATE.ACCOUNT`,
`GRANT`, `REVOKE`, `LIST.GRANTS`, `UNLOCK`, `ENCRYPT.FIELD`), the 3 `*.SERVER`
verbs, and **11 SDSYS plumbing records** — `$HOLD` `ACCOUNTS` `BP` `BP.OUT`
`GPL.BP` `GPL.BP.OUT` `MESSAGES` `QFILE` and `FIRST/SECOND/THIRD.COMPILE`.
**A standard account still gets `BASIC`, `CATALOG`, `RUN`, `ED`, `SED`, `COPY`,
`SH`, `!` and `DELETE.CATALOG`** — every capability on the removal list.

**THE 9 ARE NOW THE ADMINISTRATOR TIER.** Owner's ruling, 17 Aug 2026:
"administrators get the whole voc". It was never a no-op — an SD administrator
had to `LOGTO SDSYS` to administer anything. Safe because the programs gate
themselves: `CREATEA:109`, `DELACC:60`, `MODIFYA:48`, `GRANTA:86`, `UNLOCK:61`
each open `if not(kernel(K$ADMINISTRATOR, -1)) then stop sysmsg(2001)`.
**Two do not and are on the list anyway** — `UPDATE.ACCOUNT` is `V|IN|15`,
`CPROC:1521`, ungated; `ENCRYPT.FIELD` points at **`$CRYPTO`, which is not in
this tree at all** and is as broken in SDSYS's VOC as it will be in an admin's.

**The 11 plumbing records are NOT copied**, and that is a decision, not an
oversight: `ACCOUNTS`, `BP.OUT`, `GPL.BP`, `GPL.BP.OUT` and `QFILE` are
**relative** pointers (`F|ACCOUNTS|ACCOUNTS.DIC`), so in a user account they
name files that are not there and `LIST ACCOUNTS` fails to open rather than
lists; the `*.COMPILE` records are bootstrap paragraphs; `$HOLD` and `BP` are
already made per-account by `CREATEA`'s `create.dir.file`.

**THE MECHANISM IS BUILT — 17 Aug 2026 — AND HAS NOT BEEN COMPILED OR RUN.**
A cycle is owed; `make sd` is NOT needed (only BASIC and data changed since the
08:03:49 install, `sd.exe` `04CA97C138ADB148`). **`stage.py --bootstrap` is
`CREATEA`'s and `LOGIN`'s first compiler for this change**, and that is where a
mistake will surface. Files: `CREATEA`, `LOGIN`, `SYSCOM/KEYS.H`,
`NEWVOC/TIER.OMIT.STANDARD`, `NEWVOC/TIER.ADD.ADMINISTRATOR`, `MESSAGES/10052`,
`gplbld/stage.py` (comment only).

**A BAD `$LOGIN` LOCKS YOU OUT OF SD** — §7 step 0 says back `gcat` up before
recompiling one on an installed system, and this change touches `LOGIN`. The
cycle route does not have that hazard (the bootstrap builds a fresh tree), but
the recovery route does.

**What was avoided, and why the list matters more than usual here** — none of
this compiles until the cycle: `CONTINUE` is used in `LOGIN` **because that
file demonstrates it** and not in `CREATEA`, which does not; both loops use an
explicit id comparison rather than `LOCATE`; `update.voc.tier` and
`tier.acc.name` are initialised at the top of `LOGIN` because BCOMP's
**"is not assigned a value"** is what `bootstrap.py:229` fails the bootstrap
on, and both are read textually above the `get.acc.tier` that sets them.

- **`PROGRAMMER` keyword** at `CREATEA`, beside `ADMINISTRATOR`, matched on
  token text for the same reason (the `KW$` table is positional and shared).
- **`tier`** — `STANDARD` / `PROGRAMMER` / `ADMINISTRATOR`, a string not a flag,
  because it is written to the register and read back. It replaced a boolean
  `full.voc` that could not tell the top two apart. `PROGRAMMER` **cannot
  downgrade** `ADMINISTRATOR`; both keywords are accepted in either order.
- **`NEWVOC/TIER.OMIT.STANDARD`** lists what a standard account does not get —
  **18 ids** since 17 Aug. **`NEWVOC/TIER.ADD.ADMINISTRATOR`** lists the 9 an
  administrator gets on top, read out of `VOC_TEMPLATE`. Field 1 is a
  description; fields 2+ are ids. **Held as data so the shipped posture changes
  without recompiling**, and in `NEWVOC` because that file is already open in
  the loop and already shipped.
- **READ OUT OF `VOC_TEMPLATE` RATHER THAN MOVED INTO `NEWVOC`, and that is the
  whole design.** The fallbacks only point the safe way while `NEWVOC` holds
  nothing administrative: a lost omit list means "no policy" and gives the full
  VOC, so `CREATE.ACCOUNT` in `NEWVOC` would let one missing record hand every
  account the power to make more. The add list fails the other way — lost, an
  administrator gets a programmer's VOC and finds out at once. `stage.py:117`
  says the same and is amended to say why it survives the tiers.
- **A missing or empty list gives every account the full VOC** — the old
  behaviour exactly, which is the safe way round for a lost record.
- **Both list records' descriptions start with "T"**, not a VOC type letter, so
  if a skip ever broke they would land inert rather than as fake verbs.
- **`ADOPT` defaults to `ADMINISTRATOR`** (`CREATEA`, end of `more.args`).
  Without it the installing user lands STANDARD with no `BASIC`, no `ED` and no
  `CATALOG` — `adopt-account.ps1:195` passes no tier keyword and never had one
  to pass. **A regression the tier work itself would have introduced**, and it
  would have read as "SD is broken after installing it". A default, not an
  override: an explicit keyword still wins, and `make.admin` is untouched.

**WHAT IS ON THE LIST AND WHY.** Owner's rulings, 16–17 Aug: `BASIC`,
`CATALOG`, `RUN`, `ED`, `SED`, `COPY`, `DELETE.CATALOG`, `SH`, `!`. **Plus four
exact aliases, because leaving them would void the ruling** — measured, not
guessed: `CATALOGUE`→`$CATALOG`, `DELETE.CATALOGUE`→`$DELCAT`, `EDIT`→`$ED`,
and `COPYP` (`$COPYP`, "Pick style COPY", the same capability by another
program). **Thirteen ids.**

**RULED 17 Aug 2026 — all four are PROGRAMMER AND ABOVE**, so all four are on
the omit list: **`MODIFY`** (`$MODIFY`, a record editor, the same class as
`ED`), **`COMPILE.DICT`** (`$CD`) and **`GENERATE`** (`$GENERAT`), the
dictionary compilers, and **`PHANTOM`**, which runs a catalogued program in the
background. **This moves `PHANTOM` out of ADMINISTRATOR-only** in the split
below. **Plus a fifth id: `CD` is an exact alias of `COMPILE.DICT`** — both
`Verb to compile dictionaries|CA|$CD`, and `THIRD.COMPILE` uses it that way.
**Eighteen ids.** Reading the records found it; the name alone would not have,
and this is the second time — see the four aliases above.

**NOT DONE:** the 30/45/65 split of the 149 verbs. What exists is the
capability cut, not the full three-tier curation.

**THE HOLE THAT MADE THE TIERS TEMPORARY, FOUND AND FIXED 17 Aug 2026.**
`LOGIN:501 update.voc` re-copied **the whole of `NEWVOC` with no tier filter**,
handing a standard account back `BASIC`, `CATALOG`, `RUN`, `ED`, `SED`, `COPY`
and `DELETE.CATALOG` — and writing `TIER.OMIT.STANDARD` into its VOC as a
record. **Reached two ways, neither needing privilege:** `UPDATE.ACCOUNT`
(`CPROC:1521`, internal verb 15, ungated), and — worse, because it needs no
verb — the `$RELEASE` test at **`LOGIN:419`**, which asks **any** user "Update
VOC to new release?" whenever the account's release level differs from
`SD.REV.STAMP`. One `Y`. **So the tiers survived exactly until the next release
stamp moved**, which is not a boundary anyone would notice.

**The fix needs the tier RECORDED, because it was a create-time decision with
nothing persisting it.** `ACC$TIER` = **`ACCOUNTS` field 5**, `KEYS.H:281` —
the first use of the "start at field 5" that the `ACC$USERS` note reserved
(field 4 is poisoned). `CREATEA` writes it on **every** path including `ADOPT`;
`LOGIN` reads it at all three `update.voc` call sites and applies the same omit
list. **A blank field means the full VOC**, the pre-tier behaviour: blank can
only occur on an account created before this, which already holds a full VOC,
and an update only ever writes — it never deletes.

**And a correction to yesterday's comment:** `CREATEA` says `CONTINUE`'s
behaviour inside `LOOP ... REPEAT` "is not demonstrated anywhere here" and used
a flag instead. **It is demonstrated — `LOGIN`, in `update.voc` itself**, where
a declined type change skips the write. `LOGIN` uses `CONTINUE`; `CREATEA`
keeps its flag, and the wrong note is left standing there rather than corrected
by a second uncompiled change.

**DONE AND PASSED — 17 Aug 2026, 11:31:38, 22 of 22.** `gplbld/verify-tiers.ps1`
is this recipe as one elevated command, and the header has the table. What
follows is what it checks and why each part is there.

**HOW TO TEST IT** — no elevation needed beyond `CREATE.ACCOUNT` itself, and it
carries its own controls. Three accounts, not
one: `CREATE.ACCOUNT USER <a>`, `USER <b> PROGRAMMER`, `USER <c> ADMINISTRATOR`.

- `<a>`'s VOC lacks all **eighteen**; `<b>`'s has them. **Checking only `<a>`
  proves nothing** — a copy loop that skipped everything would also pass it.
- `<c>` has the eighteen **and** the nine, `<b>` has the eighteen and **not**
  the nine. That second half is the control for the add list.
- No account's VOC holds `TIER.OMIT.STANDARD` or `TIER.ADD.ADMINISTRATOR`.
- `ACCOUNTS` field 5 reads `STANDARD` / `PROGRAMMER` / `ADMINISTRATOR`, and
  **`DON`'s reads `ADMINISTRATOR`** — that is the `ADOPT` default, and the
  installing user's own account is the one a broken default breaks.
- **Then the durability half, which is the point of recording the tier:**
  `UPDATE.ACCOUNT` in `<a>` must leave it without the eighteen. Before this
  change it restored every one of them.
`SET.TRIGGER`, `UPDATE.RECORD`, `MODIFY`, `HSM`, `GENERATE` are **PROGRAMMER**.
`SET.SERVER`, `DELETE.SERVER`, `LIST.SERVERS` **removed** — SDNet server details
were not held securely in this version.

**THE SPLIT ITSELF, first pass, rulings above already applied.** Tiers are
cumulative: `PROGRAMMER` gets standard plus its own, `ADMINISTRATOR` gets
everything. **Not reviewed by the owner yet** — expect entries to move.

REMOVED from every tier (7):
`MICRO` `LOAD.LANGUAGE` `SET.LANGUAGE` `NLS` `SET.SERVER` `DELETE.SERVER`
`LIST.SERVERS`

ADMINISTRATOR only (25) — `PHANTOM` moved to PROGRAMMER, owner 17 Aug 2026:
`CREATE.ACCOUNT` `DELETE.ACCOUNT` `MODIFY.ACCOUNT` `UPDATE.ACCOUNT`
`CLEAN.ACCOUNT` `GRANT` `REVOKE` `LIST.GRANTS` `CONFIG` `LISTU` `LIST.READU`
`LIST.LOCKS` `CLEAR.LOCKS` `LOCK` `UNLOCK` `LOGOUT` `SET.DATE`
`UMASK` `PSTAT` `PDEBUG` `PDUMP` `DUMP` `ENCRYPT.FIELD` `SH` `!`

PROGRAMMER adds (47):
`BASIC` `CATALOG` `CATALOGUE` `DELETE.CATALOG` `DELETE.CATALOGUE`
`COMPILE.DICT` `PHANTOM` `RUN` `MAP` `DEBUG` `ED` `EDIT` `SED` `MODIFY` `UPDATE.RECORD`
`SET.TRIGGER` `HSM` `GENERATE` `CREATE.FILE` `DELETE.FILE` `CLEAR.FILE`
`CONFIGURE.FILE` `ANALYSE.FILE` `ANALYZE.FILE` `FSTAT` `CREATE.INDEX`
`DELETE.INDEX` `BUILD.INDEX` `MAKE.INDEX` `LIST.INDEX` `COPY` `COPYP` `DELETE`
`RENAME` `REFORMAT` `SREFORMAT` `SEARCH` `LIST.DIFF` `LIST.ITEM` `SORT.ITEM`
`LIST.COMMON` `DELETE.COMMON` `LIST.VARS` `CD` `CNAME` `REPORT.SRC`
`REPORT.STYLE` `FORMAT`

STANDARD — what an application needs (70):
`SELECT` `SSELECT` `QSELECT` `NSELECT` `GET.LIST` `SAVE.LIST` `FORM.LIST`
`COPY.LIST` `MERGE.LIST` `DELETE.LIST` `LIST.UNION` `LIST.INTER` `CLEAR.SELECT`
`CLEARSELECT` `LIST` `SORT` `SUM` `LIST.LABEL` `SORT.LABEL` `LIST.FILES`
`SETPTR` `SPOOL` `SP.OPEN` `SP.CLOSE` `SP.VIEW` `PRINTER` `COMO` `LOGTO`
`QUIT` `STOP` `ABORT` `CLEAR.ABORT` `GO` `IF` `SET` `SHOW` `OPTION` `ALIAS`
`SET.EXIT.STATUS` `SET.FILE` `TERM` `PTERM` `DATE` `TIME` `DATE.FORMAT` `WHO`
`WHO.AM.I` `STATUS` `MESSAGE` `LOGMSG` `BELL` `ECHO` `HUSH` `PAUSE` `SLEEP`
`CLR` `CS` `CT` `CLEAR.INPUT` `CLEARINPUT` `CLEAR.PROMPTS` `CLEARPROMPTS`
`CLEAR.DATA` `CLEARDATA` `CLEAR.STACK` `GET.STACK` `SAVE.STACK` `RELEASE`
`AUTOLOGOUT` `CLEAR.STACK`

**Two notes on the lists.** `COPYP` is in PROGRAMMER but is one of the five
malformed entries above, so it does not work today either way. And `LIST` and
`SELECT` must stay in STANDARD, yet they read **any** file the account can open
— so the VOC tier decides what a user may DO and the per-account ACL decides
what they may REACH. Neither substitutes for the other.

**How it would be built:** a second, reduced `VOC_TEMPLATE` plus the
`PROGRAMMER` keyword in `CREATEA` beside `ADMINISTRATOR`, so the tier is chosen
where `sdsshonly` and `Administrators` are already chosen. It wants the
per-account ACL under it first, or an administrator's reduced VOC is one `COPY`
away from being undone by its own user.

**FIVE VOC_TEMPLATE ENTRIES ARE INCONSISTENT. THEY ARE NOT BROKEN, AND THE
"CANNOT WORK" CLAIM THIS SECTION MADE FROM 16 Aug 2026 IS WITHDRAWN — measured
18 Aug 2026,** `verify-lcnames.ps1` section 6 on the 19:46:12 install. Field 1
holds a description where a bare type code is usual: `COPYP`, `DELETE.SERVER`,
`LOAD.LANGUAGE`, `SET.SERVER`, `UNLOCK`. Compare `LIST.SERVERS` — `V` / `CA` /
`$LSTSRVR`. **The record is NOT shifted**; fields 2 and 3 are correct in both.

**SD ALLOWS THE DESCRIPTION ON PURPOSE.** `CPROC:1410`, in the source, beside
the test: *"The type code may be followed by comment text with no intervening
space"* — the PI / PI-open / UniVerse rule — and `CPROC:1433` tests
`voc.entry.type[1,1]`. So `Verb to unlock records` is a `V` with a comment and
dispatches. The measurement builds such a record from scratch, in an account
VOC, pointing at `$COPYP`, and it answers `File name required` — which only a
dispatched verb produces.

**SO `UNLOCK` WAS NEVER REPAIRED**, and neither was `COPYP`; both were working.
The `changelog` entry shipped 18 Aug 2026 saying `UNLOCK` "never worked" is
wrong and carries a correction in the same file. **Both records are still bare
`V`** — every other verb is written that way and the inconsistency is what
produced the misreading — but that is tidying, not a fix. **No
`UPSTREAM_FIXES.md` entry**: one was written against `../sdb64`, which has all
five, and withdrawn when `CPROC:1410` was read. **`LOAD.LANGUAGE` no longer
exists** — removed with the language verbs in `ecd62b2`, 17 Aug 2026, not the
zero-byte file this section used to claim.

**ALL FIVE ARE NOW SETTLED, THREE OF THEM BY DELETION.** `UNLOCK` and `COPYP`
carry a bare `V` as of the 18:54:10 and 19:46:12 installs respectively.
**`DELETE.SERVER` and `SET.SERVER` no longer exist** — deleted with SDNet rather
than repaired, on purpose: fixing them would have restored the management verbs
for a subsystem that was being removed. **`LOAD.LANGUAGE` no longer exists**
either, deleted with the language verbs. Nothing here is outstanding.

**`UNLOCK` lives only in `VOC_TEMPLATE`, not `NEWVOC`**, so SDSYS gets it from
the bootstrap and administrator accounts get it through
`TIER.ADD.ADMINISTRATOR`. Note that `CREATEA`'s copy loop reads `rec[1,1]` — the
first CHARACTER of the record — so an administrator account was silently given
`V` from the `V` of "Verb", and the entry may therefore have worked there while
being broken in SDSYS. Worth knowing before concluding the fix changed nothing.
Three are being removed anyway; **`COPYP` and `UNLOCK` have the `V` line** —
re-read 21 Aug 2026, see the end of this section — and `UNLOCK` is what an
administrator reaches for to clear a stuck record lock.

**AND IT HAS NOW COST TIME — 18 Aug 2026, so this is live rather than noted.**
A `verify-fold.ps1 -Cleanup` run was killed at a `DELETE.FILE` prompt while
holding the update lock `DELETEF:145` takes on the VOC record (`readu`). Every
later attempt on that name **blocked silently** — SD echoed the command and
printed nothing at all, indefinitely, which is what a lock wait looks like and
is easily mistaken for another prompt. Two attempts were spent guessing at
prompts before a timeout in the harness showed the empty output that identified
it.

**`UNLOCK` IS THE COMMAND FOR THIS — try it first**; restarting SD
(`sd -stop`, `sd -start`, elevated) rebuilds the shared segment and drops every
lock, but it disconnects everybody and is the fallback, not the procedure.
**The restart was used on 18 Aug 2026 in the belief that `UNLOCK` was one of the
malformed entries and could not run. That belief was wrong** — it dispatched
then as it does now, §8 above — so the restart was never necessary.

**AND THE SAME KILLED SESSION BLOCKS THE NEXT CYCLE.** `cycle.ps1` stopped with
*"SD is still running after 45s: sdwind(8792)"* at 17:21 on 18 Aug 2026 with the
**service already Stopped** — an orphaned `sdwind` holding the segment, because
it will not shut down while a user-table slot is still occupied. Same cause as
the lock: the session was killed without deregistering. `Stop-Process` the PID
`cycle.ps1` names, then run it again. **Any hard kill of an SD session leaves
both a lock and a slot**, so expect the pair together.
**`UNLOCK` IS ALREADY FIXED — READ BACK 21 Aug 2026, SOURCE AND INSTALL.**
This section used to end *"Fixing `UNLOCK` is one line in `VOC_TEMPLATE/UNLOCK`:
field 1 must be `V`, not the description. It needs a cycle"*, and that had been
stale since the 18:54:10 install — the paragraph above records the fix. Both
`sdb_ai/sd64/sdsys/VOC_TEMPLATE/UNLOCK` and
`C:\ProgramData\SD\sdsys\VOC_TEMPLATE\UNLOCK` read `V` / `CA` / `$UNLOCK`,
which is the shape of the control verb `LIST` (`V` / `CA` / `$QPROC`). `COPYP`
is the same. **No cycle is owed by anything in this section.**

**ANSWERED 16 Aug 2026, sixteenth session: A `CA` VERB'S PROGRAM LIVES IN
`gcat`, EXACTLY WHERE IT LOOKS AS THOUGH IT SHOULD.** `$QPROC` is there at
**54,073 bytes** in a healthy tree, alongside 131 others. Nothing needs tracing
and there is no gap in the model.

**The question was manufactured by measuring a broken install**, and the
reasoning is kept because the mistake is the instructive part. What stood here
was: *"The installed system has 4 entries in `gcat` (`!PATHTKN`, `$BBPROC`,
`$BCOMP`, `$CPROC`), 3 objects in `GPL.BP.OUT`, and an empty `cat` — against 144
verbs ... **This is a gap in the model, NOT evidence of a broken tree**, because
`COUNT VOC` returning 431 is recorded repeatedly on real installs."* It was
evidence of a broken tree. Those four are `bbcmp.py`'s **bootstrap seed**, and
`COUNT VOC` 431 was measured on *earlier, working* installs — the one in front
of it had never run at all. **The tell was there and was read past:
`gcat/$CPROC` was 0 bytes**, which is the placeholder `bootstrap.py` touches.

**The general form, and this file has now recorded it twice:** a number read off
the installed tree describes whatever that tree is, and "SD demonstrably works,
so this must be a subtlety I have not traced" is the reasoning to distrust.
**Date the tree first.** Scoping the `gcat` lock is therefore unblocked — 132
entries is the real figure, not 4.

**Not related:** PROC, the pre-BASIC language, was removed from sd-ai and
remains upstream (owner, 16 Aug 2026). `QPROC` and `BBPROC` are not PROC despite
the names.

**It is only durable with per-account ACLs (§7 step 3 / the B work).** A VOC
the user can write is a VOC they can put `BASIC` back into, and SD object code
is portable pcode, so without `DC` withheld they can drop an object into
another account. Locking `<account>\VOC` read-only to `sdu_<name>` is what makes
the reduced VOC stay reduced. **So the tier work is blocked on B, not the other
way round.**

**Two residual holes, both real, neither closed by any of the above:**

1. **Injection through the application's own `OS.EXECUTE` or `EXECUTE`.** Tier-1
   programs legitimately need OS access, so the capability stays; an app that
   builds a command from user input is an escape and the user compiles nothing.
   `!valid_shell_cmd`'s ban on `; | & $ < >` guards the `SH` path only.
2. **A machine whose ssh server SD did not install**, where `ForceCommand` is
   never written (§5.9, structural). The user lands in `cmd.exe` and never meets
   SD's VOC at all.

**The real fix for (1) is program provenance** — a catalogued program written by
a programmer may `OS.EXECUTE`, an ad-hoc one may not. Setuid-shaped, new
machinery, and it depends on the `gcat` ACL work: "catalogued" means nothing
until users cannot rewrite each other's entries. Left open deliberately.

**And the floor under all of it:** until §5.7's service model, every tier is
enforced by the user's own Windows token. Tier 3 is real because Windows
enforces it. Tiers 1 and 2 are only ever as real as the ACLs.

### Settled: SDSYS is the exception, and LOGTO takes names only

Both questions raised by the grant check on 13 Aug 2026 were **answered the
same day by the repository owner** and are now written into §5.6. SDSYS reaches
every account without exception, and `LOGTO` accepts a registered account name
only — direct directory access by path is not supported, which closes the
bypass rather than trying to resolve paths back to accounts.

### CLOSED 21 Aug 2026: SDNet is gone. What follows is the record of the find

**CHECKED FILE BY FILE ON 21 Aug AND EVERY ITEM BELOW IS NOW UNTRUE.**
`gplsrc/netfiles.c` is deleted and builds no object; `DELSRVR`, `SETSRVR` and
`LISTSRVR` are gone from `gpl.bp`; `DELETE.SERVER`, `SET.SERVER` and
`LIST.SERVERS` are gone from `voc_template`; and the semicolon dispatch in
`op_dio1.c` is gone, replaced by a comment saying a name containing `;` now
falls through to `fullpath()` and fails like any other bad pathname.

**TWO RESIDUES, BOTH DELIBERATE, NEITHER A TASK.** `gplsrc/sdnet.h` STAYS and
is still included by `linuxio.c`, `lnxport.c` and `op_skt.c` — it carries
socket declarations that have nothing to do with SDNet, and `sd.h:273` says so
in place. And `NETFILES` is still parsed, stored and displayed while being
tested nowhere: **leave the parse**, or an `sd.conf` carrying it stops loading.

**The original entry is kept below because the reasoning is what dates**, and
because "a parameter that reads like a gate and gates nothing" is the shape
worth recognising again.

---

The repository owner believed the network file capability had gone with telnet,
for the same reason — the client protocol is inherently insecure. **It was still
here, compiled, and reachable when this was written on 18 Aug.**

- `gplsrc/netfiles.c`, 1,227 lines, and `gplsrc/sdnet.h`. **Built**, because
  `Makefile:65` is `TEMPSRCS := $(wildcard *.c)` and excludes only `sdclient.c`.
- `GPL.BP/DELSRVR`, `SETSRVR`, `LISTSRVR`; `VOC_TEMPLATE/DELETE.SERVER`,
  `SET.SERVER`, `LIST.SERVERS`.
- **Reachable from `OPEN`**: `op_dio1.c:635` treats any VOC file reference
  containing `;` as `server;remote_file` and calls `net_open()`.

**`NETFILES` IS NOT A GATE.** It is parsed (`config.c:251`), copied to the
shared segment (`sysseg.c:237`) and displayed (`op_config.c:119`,
`sysdump.c:92`) — and **tested nowhere**. Grep for the field: those four sites
are all of them. There is no way to turn this off in configuration.

**The protocol is what the owner remembered.** `net_open()` reads host, user and
password from `sd.conf` (`netfiles.c:424`), connects on port **4245**, and
recovers the password with a rolling substitution over a fixed 64-character
alphabet — `netfiles.c:564` calls it "a very simple encryption" in its own
comment.

**IT IS LATENT, NOT LIVE, AND THE DISTINCTION MATTERS.** A server must be named
in an `[sdnet]` section of `sd.conf` (`netfiles.c:446`); with none defined, every
remote open fails `ER_SERVER` (`:459`). Neither the shipped nor the installed
`sd.conf` has such a section or a `NETFILES` line — checked 18 Aug 2026. So
nothing is reachable across the network today. What is wrong is that the code
ships and is compiled, that the credentials for any server added later sit in
`sd.conf` under a substitution cipher, and that **there is no switch to refuse
the feature** — a `;` in a VOC entry is the whole trigger, and a user who can
write their own VOC can supply one.

**CONSEQUENCE FOR THE MALFORMED VOC ENTRIES (§8 above).** `DELETE.SERVER` and
`SET.SERVER` do not work *because* they are malformed. Repairing them would
restore the management verbs for a subsystem that is to be removed, and would
add no containment — the open path needs a VOC entry with a `;`, not the verbs.
**Leave them broken; remove them with the rest.**

**OWNER'S DECISION, 18 Aug 2026: REMOVE IT.** `qmclient` stays — the API needs
it, and it is mitigated by requiring an ssh tunnel — but `qmnet` goes.

**IT IS SEPARABLE FROM THE API, CHECKED BEFORE ANY CODE WAS TOUCHED.**
**`sdnet.h` IS NOT SDNet AND MUST STAY** — despite the name it is a portability
header (termios, netdb, the `SOCKET` typedef, `closesocket`, `NetError`), and its
own description says it "extracts commonly used platform dependencies from
networking and terminal i/o modules". That is why `sdclilib/sdclilib.c` includes
it, along with `linuxio.c`, `lnxport.c` and `op_skt.c`. **Deleting it would break
the client library and terminal I/O.** The API's dependency is on the shims, not
on remote files.

**REMOVED AND VERIFIED 18 Aug 2026** — `gplbld/verify-nonet.ps1`, **16 of 16**,
exit 0, on the **18:54:10** install, `sd.exe` **`DA280984D21571B4`**. Builds
clean, zero errors and zero warnings; `sd.exe` 1,914,621 bytes, was 1,955,243.
**`gcat` went 132 → 129 entries**, which is the three removed programs and is
the cheapest independent check that the removal reached the installed tree.
What follows is what was taken out and the three things that bit while doing it.

**THREE TRAPS, ALL FOUND BY THE COMPILER:**

1. **`gpl.src` IS THE BUILD LIST, NOT THE `*.c` WILDCARD.** `Makefile:61` is
   `SDSRCS := $(shell cat $(GPLDOTSRC))` — deleting `netfiles.c` gave
   "No rule to make target 'netfiles.o'" until the name came out of `gpl.src`
   too. The wildcard at `:65` is a different list and misled the first reading.
2. **`sd.h` changed, and the Makefile tracks no header dependencies** — so
   `rm -f gplobj/*.o` first, exactly as §7 step 1a records for `config.h`.
3. **Removing a branch orphans its locals.** `dh_ak.c` and `op_dio4.c` were left
   with unused `index_name`, `akname`, `list_descr`, `count_descr`. One of those
   declarations was still needed by the surviving `else` branch, so a blanket
   delete broke the build — read each warning rather than trusting a pattern.

**SCOPE, MEASURED:**

- `gplsrc/netfiles.c` — delete, 1,227 lines. It is the whole of the feature.
- **30 `NET_FILE` references** (`descr.h:317`, a `FILE_VAR` type) in
  `op_dio3.c` (12), `dh_ak.c` (6), `op_lock.c` (5), `op_dio4.c` (2),
  `op_dio1.c` (2), `op_dio2.c` (1). Every one is a clean `fvar->type == NET_FILE`
  test or a `case NET_FILE:`, so each is a branch deletion rather than surgery.
- The `;` dispatch at `op_dio1.c:635`, which is what reaches `net_open()` at all.
- `GPL.BP/DELSRVR`, `SETSRVR`, `LISTSRVR`; `VOC_TEMPLATE/DELETE.SERVER`,
  `SET.SERVER`, `LIST.SERVERS`. **Do not repair the malformed two first** — see
  above.
- **`NETFILES` NEEDS NO CODE CHANGE AND SHOULD GET NONE.** It is already inert:
  parsed at `config.c:251`, stored at `sysseg.c:237`, reported at
  `op_config.c:119` — and tested nowhere. **Leave the parse**, or an `sd.conf`
  carrying the line stops SD starting, exactly as with `CREATUSR` (§7 step 1a);
  and **leave the `sysseg` field**, because removing it shifts the shared-segment
  layout and `SYSSEG_REVSTAMP` does not catch that.
- It is a C change, so it needs `make sd` and a full cycle, not just a bootstrap.

### Open: what may a scheduled job run? (the login half is now answered)

**REWRITTEN 14 Aug 2026, seventh session, because its premise died.** This was
"how does a scheduled job log in, now that every account has a password?",
raised by the repository owner on 13 Aug 2026 and built on the password model,
`ACC$USERS` and `authenticate.account` — none of which exist now. **The login
half answers itself under §5.6:** a scheduled task runs as a Windows user, and
if that user has an SD account, `sd` puts it there with nothing asked. The
batch account is a Windows account plus its SD account, and it grants nobody
because nobody else is in its `ACC$GROUP` group. **No credential is involved
anywhere**, which is what the whole of the rejected reasoning below was for.

**What is still open is the capability list**, and the design is the owner's:
an `X`-type VOC item named `ALLOWED` in **SDSYS's** VOC, holding
`ACCOUNT, VOC name` pairs. Only an administrator can edit it, because it lives
in SDSYS; the job still runs in the named account, so **nothing runs with
administrator rights**. **The mechanism exists and needs no new C code:**
`SYSTEM(1026)` returns the command from the command line (`op_sys.c` case 1026,
from `single_command` in `sd.c`) and `CPROC` does not pick it up until line
556, so `LOGIN` can read and decide first.

**Constraints to build to**, worked out once and recorded so they are not
re-derived: **one token, no arguments, enforced** — this is what does the
security work, not "must be in VOC", since every verb is a VOC item and with no
arguments a verb entry is useless; **accept only `PA` and `S` VOC types**, so a
mislisted verb fails when it is set up rather than at 3am; **any prompt is
fatal in this mode** (§6, the spinning prompt); **the name must be unique
across the list** or `-A` must match, never a silent override; **set `@logname`
explicitly**, since an unattended job has no person behind it; and **catalogue
batch programs locally**, so they do not become runnable from every account.

**Rejected, so it is not proposed again:** a password on the command line
(readable through Task Manager, `Win32_Process` and ETW) and a password file —
both moot now that login takes no password, but the reasoning that killed them
still holds for any future secret: a capability list has nothing to leak or
rotate, and a stolen credential grants an *interactive session* where a list
grants a fixed set of commands. **Hashing the VOC entry** was rejected on its
own merits and still is: it pins one hop and no further, and storing the
command text rather than a name gets the same protection for nothing.

**What it does not fix.** The account boundary is **not** a data boundary — a
Q-pointer in the batch account's VOC reaches another account's files, so "runs
without administrator rights" is worth having but is not a sandbox. And **who
may trigger a job is still open**: the list says what may run, not who may fire
it. The batch account is also the one place per-directory ACLs work in stage 1,
since exactly one principal ever runs there; fold that `icacls` into §5.9.

### REVERSED 21 Aug 2026: the API is reached AT THE PORT. Posture B is gone

**Owner's decision, 21 Aug 2026:** *"api through an ssh tunnel should be
removed, it should only be allowed to the port, normally 4243."*

`sdwind.c open_api_listener()` binds `INADDR_ANY`; `stage.py`'s `SD_CONF` ships
`APIPORT=4243` **active**; `gplbld/api-firewall.ps1` owns an `SD-API-In-TCP`
rule that the installer creates (task `apiremote`, **ticked by default**) and
the uninstaller removes.

**WHAT CHANGED IS NOT THE ARGUMENT BELOW — IT IS WHAT STANDS IN FRONT OF THE
PORT.** Posture B was settled when the API login was cleartext and a session
that got in could open `$cred` and reach `OS.EXECUTE`. Since then SCRAM-SHA-256
replaced the login (19–20 Aug) and the containment gate shut both (21 Aug,
measured). So the port is no longer a boundary doing work nothing else does.

**WHAT IS STILL TRUE, so this is a judgement and not a clean bill:** an API
session's TOKEN is still LocalSystem. Binding a network interface widens who
may **attempt** a SCRAM exchange, from every local process to everything the
firewall admits. It does not widen what a session can do once in — that is the
gate's job — and the token work is what closes the other half.

**The `apiremote` task is ticked while `sshremote` is unchecked, deliberately.**
ssh has a use for somebody who never wants a remote connection (a local user
ssh'ing to localhost, the case that made the ssh server mandatory). The API has
no such case after this change, so a firewalled-off port ships a feature that
does not work. `sd.iss` says how to flip it in one flag.

**What follows is the superseded record**, kept because the reasoning is still
what has to be argued against if anyone wants the tunnel back.

### SUPERSEDED 21 Aug 2026 — SETTLED 14 Aug 2026: the API is piped through ssh — posture B

**Answered by the repository owner**, in the same instruction that made SD
accounts ssh-only (§5.6.2): *"Even the API is piped through ssh."* **Posture B
below was taken** — SD listens locally, ssh carries the traffic, and nothing of
SD's own faces the network.

What that settles, beyond the choice itself:

- **CORRECTED 14 Aug 2026, fifth session — THE API STILL NEEDS AN ACCOUNT
  PASSWORD.** This bullet used to say the API "stops needing a network
  credential model of its own", reasoning that ssh had already authenticated
  the user so peer identity would do. **The repository owner corrected it: in
  the Linux version the ssh tunnel is only the first gate, and the API has no
  access to the server without an account password.** Two gates, not one.

  **This is what saves the credential machinery.** §5.6's reversal takes
  passwords off the console login, which left `$CRED`, `!CRED_SET`,
  `!CRED_VERIFY` and `SET.PASSWORD` with no caller. They are the API's gate
  instead, and are **not to be deleted** (§7 step 0d).

  **What is not settled is which password.** On Linux the API check is
  `login_user()` reading `/etc/shadow`, so it is the *operating system*
  account's password. MSYS2 has no `/etc/shadow` (§6), so the Windows options
  are `$CRED`, which exists and is verified working, or `LogonUser` against the
  Windows account, which would match Linux more closely at the cost of handling
  a Windows credential inside SD. **Decide it with §7 step 6a**, and note the
  no-password-on-a-command-line rule in §5.6.1 applies to whichever is chosen.
- **The AF_UNIX weakness in §6 matters less, but does not vanish.** Binding to
  loopback is not the same as authenticating the peer.

  **CORRECTED 20 Aug 2026 — this bullet used to say a named pipe with
  `GetNamedPipeClientProcessId` was the right Windows answer "and
  `connection_type` already has `CN_PIPE`". BOTH HALVES ARE WRONG and were
  already wrong three days after it was written.** The named-pipe transport was
  built and abandoned on 17 Aug (§7 step 11): a pipe in the Cygwin descriptor
  table is PERMANENTLY READY to `select()`, so `sdpoll()` spins and `sd.exe`
  never answers. And `CN_PIPE` is not spare — it is SDLocal's own transport
  (`sd.c:423`). **The answer is `GetExtendedTcpTable`**, which identifies the
  peer of the socket `sdwind` already has and changes no transport;
  `make check-peer-probe` proves it. The header of this file has the detail and
  the open policy question.
- **It makes the ssh install path load-bearing**, which is why the silent
  failure fixed on 14 Aug 2026 mattered more than an optional extra.

**The client side, as it actually works today.** Supplied by the repository
owner, 14 Aug 2026 — the command their Gambas3 client runs on Linux:

```sh
sshpass -p <password> ssh -L <port>:/tmp/sdsys/sdclient.socket -N <user>@<host> &
```

The contract is: **ssh forwards a local TCP port to a UNIX domain socket on the
server**, and the client library connects to `localhost:<port>`. Four things
about it do not survive the move to Windows, and together they are larger than
the `login_user()` work in §7 step 6:

1. **Nothing on Windows creates that socket.** `start_connection()`
   (`linuxio.c` 130-131) reads `sun_path` from a socket it has *already been
   given* — the server does not listen, it is spawned per connection with the
   socket on its stdin, by xinetd or systemd socket activation. **Windows has
   neither**, so the listener and the per-connection spawn have to be built.
   That is what the retained `etc/xinetd.d/` and `usr/lib/systemd/` document,
   and it belongs with §5.7's service model.
2. **`/tmp/sdsys/sdclient.socket` resolves inside `C:\Program Files\SD\`** by
   the two-component POSIX-root rule in §6 — and Program Files is read-only to
   ordinary users. It needs the same `etc/fstab` bind `/dev/shm` already got.
   The same trap, one directory along.
3. **MSYS2's AF_UNIX is emulated over a TCP loopback socket** with a handshake
   file (§6), not a filesystem object with permissions, so the Linux reasoning
   — local socket, therefore local users only, therefore `getpeereid()` is
   meaningful — **does not carry**. Strongest argument for the named pipe.
4. **`sshpass` does not exist on Windows**, and a password on a command line is
   visible in the process list anyway. A Windows client wants key-based
   authentication, which removes the need to hold a password at all.

**MEASURED 16 Aug 2026, sixteenth session — THE LINUX CLIENT CONTRACT CANNOT BE
PORTED, AND THE REASON IS NOT ssh.** This was the "untested and load-bearing"
item here; it is now settled, and it settles the transport with it.

- **The ssh client accepts the syntax.** `-L 9999:/tmp/sdclient.socket` on
  OpenSSH_for_Windows_9.5p2 reaches host-key verification, i.e. it parsed —
  against a malformed control that is rejected outright with `Bad local
  forwarding specification`. So `-L port:/unix/socket` is **not** the blocker.
- **The blocker is that MSYS2's AF_UNIX is not a socket Windows can see.** A
  socket bound by MSYS2 at `/tmp/x.sock` is, from native Windows, a **54-byte
  regular file** reading `!<socket >52445 s <cookie>` — the Cygwin emulation,
  a TCP port plus a shared secret. A native Windows AF_UNIX socket is a
  zero-length reparse point.
- **Demonstrated, not inferred**, with a control on one socket at one moment:
  MSYS2's own client **connected** and the server logged the accept; native
  `curl.exe --unix-socket` on the same path failed in 0 ms and the server saw
  nothing.

**So `sshd`, a native Windows program, cannot reach a socket SD creates through
the MSYS2 runtime**, and `ssh -L <port>:/tmp/sdsys/sdclient.socket` cannot work
here however the rest is built. **This decides the named pipe** — already
called "the strongest argument" below, now a measurement rather than an
argument — or a loopback TCP socket with authentication of its own.

**A note on the rig, because the first attempt produced a confident wrong
answer.** MSYS2's emulation needs the server to actively `accept()` for a
client's cookie handshake to complete, so a `listen()`-then-sleep server times
out *every* client. That run had the control failing too, which is the only
reason it was not written up as proof.

**The original question and all three postures** — A, SD's own socket faces the
network; B, ssh or VPN carries it and SD is local only; C, a web front end in
front of a local-only SD — were moved to HISTORY.md on 14 Aug 2026, under
"PROJECT_STATUS rolled over from 4,112 lines". Read it before proposing A or C
again: the case for and against each was worked through at length, and the two
arguments that decide it are that **§1 already points at B** (if the target user
is a Windows developer, their application is the front end) and that C's cost
over B is a second codebase to patch while its benefit — a browser UI — is a
product question rather than a security one.

### Settled: the binaries were purged from history on 13 Aug 2026

Done, and force pushed. See §5.11 and the HISTORY entry. **Any clone taken
before that date is incompatible** and must be re-cloned; do not merge or push
from one. The only remaining copy of the pre-rewrite history is a bundle in a
session scratchpad, which will not survive the machine — see the HISTORY entry
if it is wanted.

### SETTLED 14 Aug 2026: `IsAdmin()` tests Windows `Administrators`, and `sdadmins` is gone

A Windows administrator is an SD administrator; the decision and its measured
basis are in **§5.6.1**. `sdadmins` is referenced by nothing, the installer
need not create it, and it may be deleted from this machine. The two options
not taken are in HISTORY under "PROJECT_STATUS rolled over from 4,112 lines";
one reason is worth carrying: keeping an OS check on `sdadmins` inherits the
sign-out-and-back-in trap in §6, so `sd -start` would have failed for the
installing user on every fresh install.

### CLOSED 21 Aug 2026: the console path stays exactly as it is

**Owner's decision, 21 Aug 2026.** The console entry point is neither dropped
nor turned into a client of the service. It stays a privileged administrator
path, and **the behaviour that is there now is the specification.** That
unblocks the token work: process-creation identity has to be decided only for
the sessions the SERVICE creates, not for a console session, which goes on
opening the database as the invoking user.

**WHAT THAT BEHAVIOUR IS, MEASURED 21 Aug RATHER THAN DESCRIBED.**

- **Entry is always your own account.** `sd` with no account named lands in
  `@logname`'s (`LOGIN`, `case 1`). Owner's rule of 15 Aug 2026, and it covers
  administrators.
- **`sd -ASDSYS` is refused — message `10051`**, *"You can only log in to your
  own account - use LOGTO to reach another"*, observed unelevated. The gate at
  `LOGIN:334` has **no elevation branch**, so an elevated session is refused
  the same way. `10002` is reachable only under `-internal`.
- **`LOGTO SDSYS` is the only door, and entering SDSYS is what obtains
  privilege** (`CPROC:2595`, owner's design 16 Aug). `!elevate` asks UAC and
  answers 0 when the session is already elevated — so from an elevated prompt
  nothing prompts, and from an ordinary one the consent dialog appears.
- **Over ssh it fails by construction**: UAC draws on the interactive desktop
  and an ssh session has none (§5.6.2). Windows enforces it, not a test here.

**"AN ELEVATED PROMPT PUTS YOU IN SDSYS AUTOMATICALLY" IS ONE STEP OUT, AND THE
OWNER'S OWN SESSION SHOWED WHICH.** From an elevated PowerShell, 21 Aug:

```
:who              -> 27 DON               <- own account, NOT SDSYS
:logto sdsys
:who              -> 27 SDSYS from DON    <- and no UAC dialog
```

So an elevated session lands in its own account like any other, and what
elevation buys is a **silent** `LOGTO SDSYS` rather than a consent prompt — the
same destination, reached one step later, which is why it reads as automatic.
The automatic form was true until 15 Aug 2026 and was deleted that day
deliberately (`LOGIN:356`, one of two ways somebody could stand in an account
without ever standing in their own).

**THAT SESSION IS ALSO THE ONLY MEASUREMENT OF ANY OF THIS FROM A REAL
TERMINAL.** Every verifier drives SD through a PIPE, so `create.account user
test2` / `delete.account test2` typed at the `:` prompt is independent
corroboration of the 38 of 38 above — one Y/N for the directory, `Group:
sdu_test2 Deleted`, `OS User: test2 Deleted`.

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
a directory of `%0`/`%1` buckets — `sdsys\VOC` holds two files whatever its
record count. That check could never pass and was removed.

### Other

- `usr/lib/systemd/` and `etc/xinetd.d/` are kept deliberately. They have no
  function on Windows but they document the service topology — socket
  activation, ports, per-connection instances — that a Windows service must
  reproduce. Remove once that design is captured elsewhere.
- The client library is LGPL-3.0-or-later with a linking exception, while the
  rest of the tree is GPL-3.0. That is compatible and intentional for a client
  library, but it is a real licensing boundary worth being aware of.
