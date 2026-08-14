# HISTORY

Append-only record for the SD Windows port. This is the overflow and archive
for [PROJECT_STATUS.md](PROJECT_STATUS.md), which holds only what a new session
needs to act on today.

Read this when you need to know *why* something is the way it is, whether an
approach has already been tried, or whether a claim in PROJECT_STATUS was ever
corrected.

---

## Rules

1. **Append-only. Never delete or rewrite an entry.** If an entry turns out to
   be wrong, add a new entry that says so and references it by date and
   heading. The wrong turn is part of the record; erasing it invites a repeat.
2. **Newest first.** New entries go directly below this rules block.
3. **Every entry carries an absolute date and the commits it covers.** Never
   "today" or "last session".
4. **Entries are written to be read cold**, by someone with no memory of the
   session, possibly on another account. Spell out names and paths.
5. **Corrections get their own entry**, headed `Correction:`. This is how a
   future session learns that a confident earlier claim was wrong.
6. Suggested shape, not mandatory: what changed, why, what it cost, what is
   still open.

---

## Correction: 14 Aug 2026 - RDP denial CAN probably be tested on one machine

Corrects "14 Aug 2026 - The ssh-only model is proven, and three false failures
on the way", immediately below, which said the `0x708` failure meant "no
variation of it will work on one machine" and moved the RDP test to the second
machine on that basis. **The reasoning was wrong**, and it was wrong in the
direction that costs most: it declared a test impossible and parked it.

`0x708` is *"you already have a console session in progress"*. It is the
**same-user** case. `mstsc /v:localhost` had defaulted to the signed-in user's
own credentials, and asking to connect to a console session you are already
sitting in is circular, so RDP refuses before authentication. The error was
read as a statement about how many sessions a Windows client SKU permits, and
it is not one.

What a client SKU actually does: several user sessions may exist at once - that
is Fast User Switching - but only one may be **connected**, and an incoming RDP
logon **takes the console over** rather than being refused for coexisting with
it. So a *different* user, with no session to collide with, has nothing to
trigger `0x708` and should reach the logon check where the deny right is
evaluated.

The attempt is therefore worth making with the **probe account's** credentials.
Outcomes: refused with "the system administrator has restricted the types of
logon ... that you may use" means the right holds and nothing happens to the
console; admitted means the right does not hold, §5.6.2 is half wrong, and the
console session is disconnected - recoverable by signing in again, with
processes in the disconnected session still running.

The second machine remains the definitive test, for a better reason than the
one originally given: it is the configuration a real user is in, and it does
not put the tester's own session at risk.

**The general lesson, which is why this is an entry and not an edit.** An error
message was taken as evidence for a broader claim than it supported, and the
broader claim was then written into three places at once - precisely so that a
future session would not re-attempt the test. Confidence and reach were added
in the same step. Prefer to record what was observed (`0x708`, same user,
before authentication) and keep the conclusion narrow.

---

## 14 Aug 2026 - The ssh-only model is proven, and three false failures on the way

Third session of 14 Aug 2026, covering the commit that carries this entry, on
top of `61b9408`. One subject: §5.6.2, which the previous session left decided,
implemented, shipped in the installer and completely unexercised.

### What was proven

`gplbld/verify-sshonly.ps1`, new and tracked, against a real Windows account:
thirteen checks, all passing. The result in one line — **joining `sdsshonly`
takes away the console and leaves ssh alone.**

| | control, no SD group | in `sdsshonly` |
|---|---|---|
| `LogonUser` INTERACTIVE | admitted | **refused 1385** |
| `LogonUser` NETWORK_CLEARTEXT | admitted | admitted |
| `ssh` with a password | admitted | **admitted** |
| `ssh` with a key | admitted | admitted |

The account did not merely authenticate: the test asserts on `whoami` coming
back, so a shell ran under that token. And the verdict does not rest on the
test's own reporting — the installed sshd, which is the only one that counts,
logged `Accepted password for sdsshprobe` and `Accepted publickey for
sdsshprobe` to `OpenSSH/Operational` at the same moment.

`deny-logon.ps1` ran against a real group for the first time; it had only ever
been tried on a throwaway. `SeDenyNetworkLogonRight` was confirmed untouched,
which is the one thing in the design that had to be got right.

**Still not observed: RDP refusal, and it needs two machines.** There is no
`LogonUser` type for it — RDP is logon type 10 and `LogonUser` cannot produce
one — so only a real Remote Desktop connection exercises the right. The probe
account was left alive to do that by hand, and the attempt on 14 Aug 2026
failed for a reason unrelated to the design: `mstsc /v:localhost` answers
`0x708`, "you already have a console session in progress", refusing **before
authentication** because a Windows client SKU allows one session and the
console holds it. No variation of it will work on one machine. The test moves
to the second machine, with this one as the RDP client.

### Why the script is a file rather than a session

§7 step 2 has to repeat all of this on the second machine, which is being built
precisely because this one has a development tree. A test that exists only as
typed commands would have been retyped from memory, differently.

### The control column earned its place immediately

The first run refused the **key** login on both sides of the experiment. Read
without a control that is "the deny rights break ssh", and §5.6.2 would have
been abandoned on a false result. An equal failure on both sides cannot have
been caused by the thing that differs between them.

The real cause turned out to be worth knowing on its own: **a Windows account
that has never logged on has no user profile**, and Win32-OpenSSH resolves
`AuthorizedKeysFile .ssh/authorized_keys` relative to the home directory — so
the planted key was never read. Shown in both directions across runs: refused
twice with no prior login; accepted after one password login, which creates the
profile. **This applies to accounts `CREATE.ACCOUNT` makes**, and it is in the
product changelog for that reason.

### Three false failures, all now traps in §6

Every one of them reported a failure that had not happened, which is the
expensive kind.

1. **`native.exe 2>&1` under `$ErrorActionPreference = 'Stop'`.** PowerShell
   5.1 wraps native stderr in `ErrorRecord`s and `Stop` makes them throw. `ssh`
   writes `Warning: Permanently added 'localhost' ...` to stderr **on a
   successful login**, so the script died on a success message and printed
   `FAILED` with a stack trace. Fixed by routing every external program through
   one `Invoke-Native` helper built on `Start-Process` with separate stream
   files. There is no inline `2>&1` left in the script.

2. **`sshd -d` from an elevated prompt authenticates nobody.** sshd must run as
   SYSTEM to build a user token; elevation is not enough and there is no flag
   for it. It answers `get_user_token - unable to generate user token ... as i
   am not running as system` and fails at `mm_answer_pwnamallow`, before
   authentication is attempted — so a DEBUG3 log that looks like a total
   authentication failure is really a diagnostic that cannot work. Both rounds
   of a diagnostic script were void. The installed service's reasons are in the
   `OpenSSH/Operational` event log and were enough.

3. **A human retyping a 36-character random password.** Three `Failed password`
   entries in the event log pointed at a design problem that did not exist —
   `LogonUser` had accepted the same string on the same account minutes
   earlier. `ssh` honours `SSH_ASKPASS` with `SSH_ASKPASS_REQUIRE=force`, so
   the password test is now automated; the secret travels in an environment
   variable cleared in a `finally`, never in a file. The generated password now
   also avoids `l I 1 O 0` and every shell metacharacter.

### A question asked and answered by measuring

`New-LocalUser` joins no group at all, and `CREATE_USER` adds none either, so
an SD account is in `sdusers`, `sdu_<name>` and `sdsshonly` and **not
`BUILTIN\Users`**. While the ssh failures were unexplained this looked like a
likely cause, and the tempting fix was to add `Users` defensively in
`CREATEA`. It was measured instead: the account logged in over ssh and ran a
command *before* `Users` was added, and adding it changed nothing. **No code
was changed**, and §4 records the measurement so the question is not reopened.

### What it cost, and what is still open

Three elevated runs, two of which failed for reasons that had nothing to do
with the subject. Open: RDP refusal; `CREATE.ACCOUNT` with `sdsshonly` present,
which has still never executed that branch; `AllowGroups`; and SD itself driven
over an ssh session.

---

## 14 Aug 2026 - SD runs as an ordinary user, and sshd finally starts

The end of the second session of 14 Aug 2026. Both results came from the
repository owner rebooting, which is worth noting on its own: the two things
blocking verification all day were a stale access token and a half-applied
Windows capability, and one restart cleared both.

### SD runs unelevated, which it never had

From a **normal PowerShell window** — no elevation, no MSYS2, nothing set in
the environment:

```
sd -start      SD (64 Bit) has been started     sdwind running: True
COUNT VOC      431 record(s) counted
WHO            2 SDSYS
sd -stop       SD (64 Bit) has been shut down   sdwind gone
```

Three things close together:

- **§5.6.1 in the real world.** `IsAdmin()` admitted an administrator who had
  not elevated. The earlier proof used a probe built with a synthetic gid; this
  is the shipped binary in an ordinary session, which is the case that matters.
- **§5.7's ACL model from the user's side.** The token now carries `sdusers`,
  and that grants the data tree — 3,264 files listed unelevated — **and**
  `/dev/shm`, mapped into `C:\ProgramData\SD\shm`, which is what `sd -start`
  needs in order to allocate semaphores. Before the reboot the same session was
  refused on every path inside `C:\ProgramData\SD`; nothing else changed.
- **The sign-out requirement is real and sufficient.** It is documented in §6
  and in the installer's closing dialog, and this is it being demonstrated
  rather than asserted.

**What it does not show, and is now the most visible gap:** `sd -start` had to
be typed. An installed system does not come up on boot, because there is no
service. After every restart somebody must start SD by hand. That is §5.7's
service model and it is hard to miss now that everything else works.

### sshd runs, and the installer step was still wrong

`Get-WindowsCapability -Online` reported `State : Installed` after the reboot,
so the brace fix earlier in the session was the whole of that bug.

**But the service was left `Stopped`, `StartType=Manual`, with no
`sshd_config`** — and that turned out to be a second defect rather than an
artefact of the terminated run. The capability installs the *files*; the
**service does not exist until after a reboot**. The step ran
`Add-WindowsCapability`, `Set-Service` and `Start-Service` in one breath, so on
a machine that needs the restart, `Set-Service` throws "no such service", hits
the catch, and reports **total failure for what is actually a success needing a
reboot**.

Fixed by moving the whole thing out of the `.iss` into
`gplbld/install-ssh.ps1`, which distinguishes the cases and **exits 2 for
"restart required"**. Being told to reboot is useful; being told it failed is
not. Moving it to a file is also the direct lesson of the brace bug: an inline
`[Run]` parameter cannot be read or parse-checked, and a shipped script can —
both scripts are now parse-checked before they are believed.

Run against the already-installed capability it reported `sshd is Running,
StartType=Automatic`, two listeners on port 22, the firewall rule enabled, and
`sshd_config` created. sshd writes that file on first start, which is the
earliest moment `AllowGroups` (§5.6.2) could be edited into it — worth knowing,
because there was nothing to edit before now.

### Where this leaves the ssh-only model

**Built, and completely untested through ssh** — but the blocker is gone. This
machine has a running `sshd` for the first time, so the ordered test in §4 can
be done here rather than waiting for the second machine. The step that matters
is proving an account in `sdsshonly` **can** still ssh in: if Win32-OpenSSH
needs something the deny rights remove, the model fails closed and nobody
reaches SD at all.

## 14 Aug 2026 - SD accounts become ssh-only, and the API goes through ssh too

**Decision from the repository owner**, 14 Aug 2026: accounts SD creates reach
the machine over ssh and nothing else; local terminal access is for
administrators, who have ordinary Windows accounts; and **the API is piped
through ssh as well**. That last clause settles §8's "how should the API be
exposed" — posture B, which is what the owner had already done to OpenQM.

Asked whether `CREATE.ACCOUNT ... ADMINISTRATOR` should still create the
Windows account, the answer was **yes, unrestricted, keep the keyword**. So the
keyword now decides two things at once:

| | `CREATE.ACCOUNT USER x` | `... x ADMINISTRATOR` |
|---|---|---|
| Windows group | standard user | `Administrators` |
| Administers SD | no | yes |
| Console / RDP | **denied** | allowed |
| ssh | yes | yes |

### The design, and the two things it turns on

**Two rights, and deliberately not a third.**
`SeDenyInteractiveLogonRight` blocks the console and
`SeDenyRemoteInteractiveLogonRight` blocks Remote Desktop.
**`SeDenyNetworkLogonRight` must not be set** — Win32-OpenSSH authenticates
with a network logon, cleartext-network for passwords and S4U for keys, so
denying it would remove the one route the design exists to preserve. That is
the whole risk in one sentence.

**The rights go on a GROUP, applied once by the installer, not per account.**
`CREATE.ACCOUNT` adds every non-administrator account to `sdsshonly`; that
membership is all account creation does. Rejected alternatives, and why:

- There is **no PowerShell cmdlet for user rights** — measured,
  `Get-Command *AccountRight*` returns nothing — so a per-account grant means
  P/Invoke or `secedit` on the hot path of every creation.
- **`secedit` is a read-modify-write of the entire USER_RIGHTS area.** Running
  it per account rewrites unrelated machine policy and races anything else
  editing it.
- A group is **inspectable**: "who is confined to ssh?" is one membership list
  rather than a walk through `secpol.msc`.
- SD already has `!os_group("ADDMEM", ...)`, written and verified.

**It cannot be `sdusers`**, which is the trap worth naming: that group grants
access to the data *files* and administrators are in it too, so denying console
logon there would lock administrators out of their own machine.

### What was built

`gplbld/deny-logon.ps1`, shipped to `C:\Program Files\SD\` by `stage.py` and
run once by the installer. It uses `LsaAddAccountRights` through P/Invoke —
surgical, one SID and one right — rather than `secedit`. It lives in a file
rather than inline in the `.iss` deliberately: an inline `[Run]` parameter is
exactly where the OpenSSH brace bug hid, and a file can be read and
parse-checked on its own.

`CREATEA` gained the `else` branch to the `ADMINISTRATOR` test, plus messages
10034 and 10035. It compiles with 0 errors.

### Verified, and the part that is not

Against a throwaway group:

| Right | Before | After |
|---|---|---|
| `SeDenyInteractiveLogonRight` | `Guest` | `sddenyprobe,Guest` |
| `SeDenyRemoteInteractiveLogonRight` | *absent* | `sddenyprobe` |
| `SeDenyNetworkLogonRight` | `Guest` | `Guest` — untouched |

`Guest` surviving in the first row is the case for LSA over `secedit`
demonstrated rather than argued. Idempotent on a second run; a missing group
exits 1 saying so.

**One trap in reading it back:** `secedit /export` writes resolvable local
groups **by name**, not by SID, so a check that greps the exported policy for a
SID reports "absent" when the right is present. The first attempt at this test
did exactly that and reported a false negative.

**Nothing has been tested through ssh**, because this machine still has no
`sshd` — the install hit the Features-on-Demand delay, was terminated part-way
and left a pending reboot. The untested list is in §4, and item 2 on it is the
one that matters: if Win32-OpenSSH turns out to need something these rights
remove, the model fails **closed** and nobody reaches SD at all. It should be
proven on a machine with `sshd` before anyone relies on it.

`AllowGroups` in `sshd_config` — the owner's second layer — is designed in
§5.6.2 and **not implemented**. It needs care: it means writing to a file SD
does not own, and the list must include administrators or the machine's own
administrator loses ssh.

## 14 Aug 2026 - the OpenSSH option never worked, and never said so

Found by the repository owner ticking the box during a normal interactive
install and then asking why there was no ssh server. There was not, and there
never had been on any install.

`gplbld/sd.iss` had:

```
try {{ Add-WindowsCapability ... ; Start-Service sshd }} catch {{ exit 1 }}
```

**In Inno, `{{` is the escape for a literal `{`, and `}` needs no escape at
all** — so `}}` is not an escape, it is two closing braces. The install log
records `Parameters:` *after* expansion, and shows what PowerShell actually
received:

```
try { Add-WindowsCapability ... ; Start-Service sshd }} catch { exit 1 }}
```

Single opening braces, doubled closing ones. Parsed without running it, that
gives "The Try statement is missing its Catch or Finally block" — so nothing
executed at all.

**It failed in total silence, by design.** The entry carries
`skipifdoesntexist` and checks no exit code, because §5.9 requires that a
failed ssh install must not fail the SD install. Correct rule, but it means a
step that could never run looked identical to one that ran fine: no `sshd.exe`,
no service, nothing on port 22, and not a word anywhere. The only evidence is
the expanded `Parameters:` line in the log.

Fixed by writing `}` singly. The corrected string was parsed before being
believed:

```powershell
[System.Management.Automation.Language.Parser]::ParseInput($s, [ref]$null, [ref]$err)
```

as shipped → parse error; as fixed → OK. That check costs nothing and is worth
doing to any generated PowerShell.

### And then the corrected command exposed a second problem

Running it for real showed the step is **slow**, which §5.9 had not
anticipated — it had planned for failure, not for duration. With the capability
`NotPresent`, `Add-WindowsCapability` fetches from Features on Demand and hands
off to `TiWorker`, which worked for minutes, grew its working set by 16 MB in a
four-second sample, and set **`RebootPending`**.

Because the `[Run]` entry is `runhidden` with no progress, the wizard sits on
"Installing OpenSSH Server..." saying nothing, and it reads as a hang. It was
reported as one during this very session. The run was terminated part-way,
which left the capability unapplied and the reboot pending — the outcome that
argues hardest for the guidance now in §5.9:

- say on the tasks page that it takes minutes;
- never kill `TiWorker`, since interrupting servicing mid-operation is how the
  component store gets corrupted;
- and tell the user about the pending reboot, which SD itself never needs.

**Still unverified:** that `sshd` runs once servicing completes, and everything
downstream of it — which now includes the repository owner's decision that SD
accounts are to be ssh-only.

## 14 Aug 2026 - CREATE.ACCOUNT runs for the first time, and can make an administrator

Carries out §7 step 1 the same day the administrator decision was made. The
verb had **never been executed**, on Windows or otherwise, since the port
began.

### What the repository owner clarified, and why it removed a config option

> `CREATUSR` isn't an active verb in SD, everything is handled by
> `CREATE.ACCOUNT`. We have only accounts, not accounts and users like in QM
> and ScarletDME.

Confirmed by the TCL verb list they supplied the same day, now tracked at
[docs/TCL_VERBS.md](docs/TCL_VERBS.md): `CREATE.USER`, `DELETE.USER`,
`ADMIN.USER`, `LIST.USERS` and `PASSWORD` are all in the "in OpenQM, not in SD"
column. There is no user concept to manage separately.

So the `config('CREATUSR')` gate in `CREATEA` was **removed**. It asked
permission to do the second half of the only thing the verb does, which stops
making sense once account and OS account are the same object. `config.c` still
parses the parameter and `CONFIG` still prints it; `DELACC` still consults it,
which is now an asymmetry and is written up as §7 step 1c.

**Correction to the entry below and to what §7 said.** It claimed `CREATUSR`
"is not in the shipped `sd.conf` and defaults off", and gave that as one of two
things blocking the verb. **That was wrong.** `config.c` line 98 sets
`pcfg.create_user = 1` — it defaulted **on** and blocked nothing. The real
blocker was the pathname validator below, which nobody had looked at because
the verb had never been run far enough to reach it.

### The defect that had been waiting at the end of it

`CREATEA` line 257 calls `ospath(pathname, OS$PATHNAME)`. That is the **C**
validator in `op_dio2.c`, not the BASIC `VALID_OS_PATH` that was fixed on
13 Aug — two validators with similar names, different implementations, and only
the C one on this path. It split the pathname on `/` alone and ran
`valid_name()` over each component, and `valid_name()` rejects everything in
`df_restricted_chars`, which contains **both `:` and `\`**. So
`C:\ProgramData\SD\user_accounts` was a single component holding two forbidden
characters, and no native Windows path could pass.

**The symptom was a half-made account**, which is why it is worth recording.
`CREATE.ACCOUNT` printed `User sdtest1 Created`, prompted for and set the
Windows password — and only then stopped with `Invalid account pathname`. The
Windows account existed, nothing in SD did, and the message named a pathname
while the visible work had apparently succeeded.

Fixed by skipping an optional drive letter and splitting on either separator.
**`df_restricted_chars` was deliberately not widened**: `op_dio3.c` and
`op_dio4.c` use it to map record ids onto filenames and back, which is a
different job, and changing it would change how records are named on disk
without being reversible for files that already exist.

### The `ADMINISTRATOR` keyword

```
CREATE.ACCOUNT USER <name> {ADMINISTRATOR} {NO.QUERY}
```

Keywords already follow the name, so it fits the existing shape. Matched on the
token text rather than by adding a `KW$` constant — `SYSCOM/PARSER.H` is a
positional table of 216 entries shared by every verb, and extending it to serve
one verb is a larger and riskier change than this warranted. The cost is that
`ADMINISTRATOR` cannot be abbreviated, unlike `NO.QUERY`.

The grant goes through `!os_group`, which learned to take a **security
identifier** as well as a name: `Add-LocalGroupMember` has a parameter set that
accepts one, and `BUILTIN\Administrators` is renamed on a localised Windows so
the name cannot be written out. Same reasoning as `icacls` in `sd.iss`. Two new
messages, 10032 and 10033 — note 10030 and 10031 were **already taken** by
`CPROC`'s step-up prompts, which is worth checking before claiming a number.

The grant is deliberately placed **after** the `sdusers` add rather than
instead of it. They answer different questions: `sdusers` grants access to the
database files, `Administrators` decides who administers SD. An administrator
who has not elevated does not carry `Administrators` in their token either, so
they need `sdusers` to reach the data tree exactly as an ordinary user does.

### Verified

Run elevated — `CREATE_USER` needs an elevated token — and driven through a
pipe with the password first, per §6.

| | `CREATE.ACCOUNT USER sdtest1` | `... sdtest2 ADMINISTRATOR` |
|---|---|---|
| Windows local user, enabled | yes | yes |
| member of `sdusers` | yes | yes |
| `sdu_<name>` group created | yes | yes |
| account dir, VOC, `$HOLD`, `$SAVEDLISTS`, BP, private catalogue | yes | yes |
| record in `ACCOUNTS` | yes | yes |
| **member of Administrators** | **no** | **yes** |

So `CREATE_USER`, `SET_PASSWD` and `OS_GROUP` have all now executed against
real Windows accounts, which closes the creation half of "every OS account
operation is unverified". `DELETE.ACCOUNT` and `MODIFY.ACCOUNT` still have not
been run.

**Both test accounts were removed afterwards.** They were real Windows accounts
with a known password and one of them was a local administrator; leaving them
would have been a live hole rather than untidiness. One empty `sdu_sdtest2`
group survived a cancelled elevation prompt and is harmless.

## 14 Aug 2026 - a Windows administrator is an SD administrator

**Decision from the repository owner**, reversing the "SDSYS is the only
administrator" half of §5.6 and settling §8's `IsAdmin()`/`sdadmins` question
on the same day that question was promoted to blocking. In their words: if you
can log in as an administrator to the OS, you are an administrator of SD; the
installer has to be an administrator, so the person who installs SD administers
it. Normal accounts are created as standard local accounts, and an
administrator is made deliberately with a keyword at account creation.

### How it came up, because three problems turned out to be one

It surfaced from a plain interactive install rather than from design work.
Running the wizard as a normal user would:

1. The final dialog told the user to run `net localgroup sdusers <name> /add`,
   which the owner queried — SD has `CREATE.ACCOUNT`, which already does
   exactly that (`CREATEA` line 340, `os_group("ADDMEM", "sdusers", ...)`) and
   creates the Windows user besides. The installer was advertising a manual
   workaround as though it were the design.
2. The "set the SDSYS password now" step ran and never let anyone type.
3. Which raised the question of why there was a second password at all.

And the answer to (3) exposed a drift that had been there since 13 Aug: §5.6
said OS groups were dropped from SD's logic entirely, but `IsAdmin()` was still
the real source of `K$ADMINISTRATOR`, and §5.6 itself carved out "an
administrator running an internal command" as a password-free way in. **So an
OS administrator was already being admitted without the SDSYS password.** The
written decision and the behaviour had come apart; this closes the gap in
favour of the behaviour, and takes option 2 of the three that §8 had listed.

It also kills the `sdadmins` defect found earlier the same day — the installer
created `sdusers` and never `sdadmins`, so a clean machine got an install
nobody could start. There is now no private group to create.

### `getgrouplist()`, not `getgroups()` — and this is the whole of it

Measured with a C probe on 14 Aug 2026, from an **unelevated** session
belonging to a machine administrator:

| Call | Source | Contains Administrators (544)? |
|---|---|---|
| `getgroups()` | the process token | **NO** |
| `getgrouplist()` | the account's groups in the SAM | **YES** |

A UAC-filtered token carries Administrators as "deny only" and Cygwin omits it,
so `getgroups()` really means *is elevated*, not *is an administrator*.
`IsAdmin()` used `getgroups()`. It uses `getgrouplist()` now, which is the
question the owner actually asked.

**And the gid, never the name.** `getgrnam("Administrators")` gives 544 and
`getgrgid(544)` gives it back, because Cygwin maps built-in SIDs to their RID —
the same reason `Users` is 545. **`Administrators` is renamed on a localised
Windows**, so a lookup by name fails on a German or French machine while the
number does not. `sd.iss` had already had to learn this for `icacls`, where it
writes `*S-1-5-32-544`. `SD_ADMIN_GROUP "sdadmins"` in `sddefs.h` becomes
`SD_ADMIN_GID 544`, still `#ifndef`-guarded so the probe trick in §6 works.

### Verified

Built clean. Then, from an **unelevated administrator session** — the case the
old test would have got wrong:

- **Positive:** the shipped build ran `sd -start`, the daemon came up, `sd
  -stop` took it down. This is decisive rather than incidental: gid 544 is
  **not** in `getgroups()` here, so it can only have been found through
  `getgrouplist()`.
- **Negative:** `sd.c` and `linuxlb.c` rebuilt with `-DSD_ADMIN_GID=99999`
  refused with "Command requires administrator privileges", exit 1 — so the gid
  really is what is tested, and §6's override still works.

### Also changed

The installer's postinstall "Set the SDSYS administrator password now" step is
**removed**, not fixed. It is unnecessary under this model, and it was broken
twice over: `sd -internal` needs a running server and the installer never runs
`sd -start`, so it died with "SD has not been started"; and Inno logged it as
`Run as: Original user`, so it ran unelevated with a token that does not carry
`sdusers` and could not have opened the database either. `nowait` meant the
console vanished before either message could be read. All three would have to
be fixed together if a password step is ever wanted back.

`sdusers` is untouched and still needed: it grants access to the data tree,
which is an ACL question rather than an authorisation one. Worth keeping
straight — an administrator who has not elevated does not carry Administrators
in their token either, so they need `sdusers` to reach the files exactly as an
ordinary user does.

### Still to do

`CREATE.ACCOUNT USER <name> {ADMINISTRATOR}` — the keyword that makes an
administrator rather than a standard local account. The existing syntax puts
keywords after the name (`{NO.QUERY}`), so it fits without disturbing anything.
Not built in this commit. Note `CREATE.ACCOUNT` has still never been run at
all, and `CREATUSR` is not in the shipped `sd.conf` so OS user creation is
disabled out of the box — both have to be dealt with before the verb works.

The installer's closing dialog still points at `net localgroup`, which is the
thing that started this. It should lead with `CREATE.ACCOUNT` and keep the
manual command as the fallback for someone who already has a Windows account —
deliberately **not** reworded yet, because pointing users at a verb that
currently errors would be worse than the present text.

## 14 Aug 2026 - the daemon is fixed and renamed `sdwind`, and it starts

Closes the entry below, which found that `sd -start` could never launch the
daemon on an installed system, and carries out the rename the repository owner
asked for. Both in one change because they are the same lines.

### The fix

Two call sites built a path to an executable from `sysseg->sysdir`:

- `gplsrc/sysseg.c`, `start_sd()`, `"%s/bin/sdlnxd"`
- `gplsrc/sdlnxd.c`, `check_lost_users()`, `"'%s/bin/sd' -cleanup"` — the
  cleanup session fired when a user's process has vanished

Both resolved to `C:\ProgramData\SD\sdsys\bin`, which holds `pcode` and
`pcode.old` and no executables at all. The second one had not been noticed when
the entry below was written; it was found by reading the file while renaming
it, which is an argument for doing the rename rather than deferring it.

**Both now resolve against the running executable**, through a new
`gplsrc/exepath.c`:

```c
bool exe_directory(char* buff, int buff_len);   /* readlink("/proc/self/exe") */
```

That was chosen over hardcoding the new location deliberately: the launcher and
the launched then stay together **by construction**, so the next layout change
cannot reintroduce this. It is also the same rule the MSYS2 runtime itself uses
to find its POSIX root, which is why `sd.exe` and its DLLs must share a
directory. `/proc/self/exe` is a Linux interface that the MSYS2 runtime
implements; measured 14 Aug 2026, it resolves correctly through a path
containing spaces and reports the name **without** the `.exe` extension, which
is what is wanted since `execl()` and `system()` both append it — and is how
the code it replaces named `sdlnxd` and `sd`.

`exepath.o` is added to `gpl.src` and to the daemon's own link line, which is
short (`sdwind.o sdsem.o exepath.o`) and cannot reach `linuxlb.c`.

**And the forked child now `_exit()`s instead of returning.** This is the half
that made the bug invisible: on a failed `execl`, or a `snprintf` overflow,
control fell back into the caller's code inside a child that had already
`daemon()`ed, so a missing daemon produced no message and no failed exit
status. It now prints what it could not start and why, and leaves. The general
lesson is in §6 — a forked child that fails must `_exit()`, never `return`.

### The rename

`sdlnxd` means "SD Linux daemon", which is the wrong name in a Windows-only
repository. `gplsrc/sdlnxd.c` → `gplsrc/sdwind.c` (via `git mv`, so the history
follows), the `sdlnxd_pid` field in the shared segment struct, `sysdump.c`'s
report line, the `Makefile` target and its entry in the `sd:` prerequisites, two
ship-list entries in `gplbld/stage.py`, and one comment in
`gplbld/bootstrap.py`.

The name itself now lives in **one place**, `SDWIND_NAME` in `sddefs.h`, used
both by `start_sd()` to launch it and by the daemon's own errlog prefix, so the
two cannot drift apart and a further rename is a single line.

**A correction to the caution in the entry below**, which said renaming
`sdlnxd_pid` "changes the layout of the shared segment struct". It does not —
renaming a field of the same type at the same offset changes no layout, so
`revstamp.h` and the segment version needed no thought after all. What *does*
change across this commit is the daemon's **file name**, which matters only to
an existing install: an old tree has `sdlnxd.exe` and a new `sd.exe` will look
for `sdwind`. Upgrading an existing install is unsolved anyway (§5.9.1).

`gplbld/sd.iss` needed no change, as predicted — the daemon ships under the
`ProgramFiles\*` glob and is not named anywhere in the installer.

### Verified

Built clean (`make sd`, exit 0, `Linking sdwind`, `Linking sd`); the four
changed or new C files compile with no warnings under `-Wall -Wextra`, the only
one reported being a pre-existing unused parameter in `create_shared_segment`.

Then, on the **development** tree, `sd -start` left
`bin/sdwind` running and `sd -stop` removed it. That proves the mechanism but
not the bug, since `<sysdir>/bin` holds executables there — so the staged tree
was rebuilt with a full bootstrap, the installer recompiled, and the machine
cleaned and installed from scratch:

- `sdwind.exe` **running as pid 9740 out of `C:\Program Files\SD\usr\bin\`**,
  while `<sysdir>\bin` held only `pcode, pcode.old`. The old path could not
  have worked; this is the case that had never once succeeded.
- `COUNT VOC` 431 records, `WHO` `2 SDSYS`, and `sd -stop` took the daemon down.
- The install re-counted at **3,264 of 3,264** files, which also confirms the
  installer still works after `stage.py` changed.

Not verified: what the daemon *does*. `check_lost_users()` runs every five
minutes and shells out to `sd -cleanup` only when it finds a user table entry
whose process has gone. Nothing has made a session go missing, so that path —
including the second fixed call site — has still never executed. It was
unreachable before today, the daemon never having run.

`errlog` stayed empty through the whole cycle, as it did before the fix, so
that open question is not explained by the daemon and remains in §4.

## 14 Aug 2026 - `sd -start` cannot start the daemon on an installed system

Found immediately after the entry below, while scoping the `sdlnxd` → `sdwind`
rename the repository owner asked for. The rename turned up a defect, which is
the more useful half of this entry.

**`gplsrc/sysseg.c` line 405** builds the daemon's path as `"%s/bin/sdlnxd"`
from `sysseg->sysdir`, so on an installed system it execs
`C:\ProgramData\SD\sdsys\bin\sdlnxd`. That directory holds `pcode` and
`pcode.old` and nothing else. The daemon ships to
`C:\Program Files\SD\usr\bin\sdlnxd.exe`.

**Why it was there and why it is now wrong.** The Linux install put the
executables and the pcode composite library in the same
`/usr/local/sdsys/bin`, so `sysdir` was a correct base. §5.8 split them —
binaries to `C:\Program Files\SD\usr\bin`, `pcode`/`pcode.old` staying with
SDSYS because `BCOMP` addresses them relative to `@sdsys` — and this call site
was not moved with them. The split itself is recorded in §6 as "two unrelated
things in one directory"; what was missed is that a C runtime string also
depended on them being one thing.

**It fails silently and the symptom is an absence.** The `execl` is in a forked
child that has already called `daemon(1, 1)`, so nothing is printed anywhere
and `sd -start` still reports success. `sysseg->sdlnxd_pid` stays at -1, which
is exactly the value meaning "failed to start", and `sd -stop` then correctly
skips the kill. SD works completely — shared segment, `COUNT VOC` reporting
431, `WHO`, `LIST ACCOUNTS` — because none of that needs the daemon. The only
thing that shows it is `Get-Process sdlnxd` returning nothing, which is what
the entry below logged as an unexplained observation before this was chased.

**It works in development**, where `<sysdir>/bin` genuinely does hold the
executables, which is why 13 Aug 2026 recorded the daemon starting and staying
up and why nothing had contradicted that until an install existed to test. Same
family as the `/bin/bash` trap in §6: correct in the development tree, wrong in
the installed one, and invisible until the two differ. The generalisation is
now in §6 — **when anything moves between the trees, grep the C for the old
location**, because the compiler cannot see a runtime string.

Not fixed here. It is §7 step 1a together with the rename, since they are the
same lines, and the fix should resolve against the executable's own directory
rather than hardcode the new path — otherwise the next layout change repeats
it.

**The rename scope, recorded so it need not be re-derived.** Tracked source
only: `gplsrc/sdlnxd.c` (rename the file too), `gplsrc/sysseg.c`,
`gplsrc/sysseg.h` (`int sdlnxd_pid` in the shared segment struct),
`gplsrc/sysdump.c`, `Makefile` (target plus the `sd:` prerequisite list),
`gplbld/stage.py` (two ship-list entries) and one comment in
`gplbld/bootstrap.py`. `gplbld/sd.iss` does **not** name it — it ships under
the `ProgramFiles\*` glob — and `gpl.src` does not list it either, since it
links separately from `sdlnxd.o` and `sdsem.o`. `bin/` and `gplobj/` are build
output; `AI_Modification_Notes/` is a historical record and should keep the old
name, as should this file's earlier entries.

## 14 Aug 2026 - the installer fix is verified: a first install lays down 3,264 files

Closes the correction below, "the installer was NOT verified for a first
install". The fix committed in `5748a51` was run for the first time and it
works. This entry is the evidence, because the previous round of testing was
green against a database the installer had never written and the lesson taken
from that was to **count what was installed**.

**Method, and it matters that the machine was cleaned first.** The broken
install left by the previous session was removed in one elevated pass:
`C:\Program Files\SD\unins000.exe /VERYSILENT`, then `C:\Program Files\SD` and
`C:\ProgramData\SD` deleted outright, then the `sdusers` group removed. The
data tree was copied to `C:\Users\dmont\sd-preclean-backup` first; only
`sdsys/$HOLD` and `sd.conf` survived the copy, which is of no consequence
because the tree being discarded was the 16-file broken one, but it is recorded
rather than glossed.

**The installer under test was rebuilt from the tracked source**, not taken on
trust from the previous session's output directory:

```sh
cd sdb_ai/sd64
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" /DStage=C:\Users\dmont\stagetest \
    /O"C:\Users\dmont\sdout" gplbld\sd.iss
```

The staged tree at `C:\Users\dmont\stagetest` was reused unchanged. That is
worth being explicit about: the `.exe` provably corresponds to the committed
`sd.iss`, and only the packaging step was redone.

**What a genuine first install produced.** Counted, not inferred:

| Measure | Broken (before fix) | Now | Staged source |
|---|---|---|---|
| files under `C:\ProgramData\SD\sdsys` | 16 | **3,264** | 3,264 |
| directories under it | - | 44 | 44 |
| `gcat` entries | 0 | 129 | 129 |
| `GPL.BP.OUT` entries | 0 | 11 | 11 |
| `Installing the file` lines in the Inno log | 15 | 3,279 | - |
| Inno log length | 145 lines | 16,507 lines | - |

A `Compare-Object` of every staged path against every installed path reported
**no differences in either direction** - nothing skipped and nothing extra. The
install log line count is the cheapest possible check of this class and is
worth keeping in mind for next time: 145 lines against 16,507 is not a
difference anyone has to squint at.

**And the installed system runs**, observed twice in two separate elevated
passes:

- `sd -start` from `C:\Program Files\SD\usr\bin\sd.exe`
- `COUNT VOC` reporting **431 records**
- `LIST ACCOUNTS` reporting `Pathname: C:\ProgramData\SD\sdsys`
- `WHO` reporting `3 SDSYS`
- `sd -stop`

each preceded by `Warning: account SDSYS has no password set`, which is the
correct state for a tree whose installation has not been finished by setting
one, and which confirms the ordering decision in §5.9: every internal command
works while SDSYS has no credential.

**The rest of the installer's job, all confirmed on the same run.** The ACLs
are exactly `GITORLI\sdusers:(OI)(CI)(M)`, `BUILTIN\Administrators:(OI)(CI)(F)`
and `NT AUTHORITY\SYSTEM:(OI)(CI)(F)`, with no `BUILTIN\Users` - and this time
that was also confirmed **from the outside**, which the previous round did not
do: an ordinary unelevated session, whose token does not yet carry `sdusers`,
is refused on every path inside `C:\ProgramData\SD`. `Test-Path` on the
directory itself still answers True, because listing the parent is permitted;
only the contents are denied. Anyone checking this should look inside rather
than at the directory entry. Also present: `sdusers` created with `GITORLI\don`
in it, `user_accounts`, `group_accounts` and `shm` created, exactly one
`C:\Program Files\SD\usr\bin` entry on the system PATH, 15 files in
`C:\Program Files\SD`, and no `gplbld` anywhere in the data tree.

### The finding this run produced: the installer creates `sdusers`, never `sdadmins`

**Not observed, deduced - and it predicts that a clean-machine install produces
a system nobody can start.** Recorded here because it is the same shape as the
bug just fixed: invisible on this machine because of state left over from
earlier work.

`IsAdmin()` in `gplsrc/linuxlb.c` line 75 is `getgrnam(SD_ADMIN_GROUP)`, and
returns FALSE if the group does not exist - deliberately failing closed.
`SD_ADMIN_GROUP` is `"sdadmins"` (`gplsrc/sddefs.h` line 131). `gplsrc/sd.c`
line 613 refuses `sd -start` with "Command requires administrator privileges"
when `IsAdmin()` is false.

`gplbld/sd.iss` creates **`sdusers`** - for the ACL - and nothing in `gplbld/`
mentions `sdadmins` at all. So on a machine that has never had SD development
on it, `getgrnam("sdadmins")` returns NULL, nobody is an SD administrator, and
`sd -start` refuses. The postinstall `SET.PASSWORD SDSYS` step would fail the
same way, since `sd -internal` is gated identically.

Everything above ran here only because `sdadmins` was created by hand on
13 Aug 2026 and this account's token carries it. §4 already records, from an
earlier session, that `sd -start` refuses while the group is absent and
succeeds once built against a group the token holds - so the behaviour is
verified even though this particular consequence was not exercised.

**This is deliberately not fixed in this commit**, because the obvious fix
prejudges an open question. §8's "what happens to `IsAdmin()` and `sdadmins`?"
asks whether `sd -start` keeps an OS-level check at all, and if it does,
whether the right group is `sdadmins` or Windows `Administrators`. Adding two
`net localgroup sdadmins` lines to the `.iss` would settle that by accident.
The question now has a forcing function it did not have before: without an
answer the installer cannot produce a working system on a clean machine.

### Two smaller observations, neither chased down

- **`Get-Process sdlnxd` reported nothing immediately after `sd -start`**, in
  both passes, while `COUNT VOC` then worked and reported 431 records. §4
  records from 13 Aug 2026 that `sd -start` "spawned `sdlnxd`, which stayed
  running". SD itself is plainly fine - the shared segment is created and
  answered - so this is about the daemon's lifetime, not the server's. It may
  be that `sdlnxd` exits promptly when nothing needs the network layer, or that
  it was not yet visible at the moment of the check. Not investigated, and
  stated as an observation rather than a conclusion.
- **`errlog` was empty** after a full start/command/stop cycle on the fresh
  tree, where earlier sessions saw "User n (pid, don)" lines written to it.
  Also not chased.

### A note on the harness, not on SD

The first elevated pass ran everything correctly but died before writing its
own summary log, showing a burst of PowerShell errors as the window closed. The
suspicion at the time was the `sd -stop` process-group trap in §6, since that
trap's signature is exactly "the shell above it vanished with exit status
zero". **It was not that.** A second pass under `Start-Transcript`, with marker
files bracketing every `sd -stop`, reached all nine markers and ran to
completion - so `sd -stop` is behaving, and the fix recorded in §6 holds. The
fault was in the throwaway script's own logging helper, which called
`.TrimEnd()` on the result of piping an empty result set through `Out-String`.
Worth one line here only so that nobody re-opens the `sd -stop` question on the
strength of the first observation.

## Correction: 14 Aug 2026 - the installer was NOT verified for a first install

Corrects the entry "The staged tree is bootstrapped" and the §4 claim added
with it, both of which said the installer worked. **It works on the upgrade
path. A first install produced a broken database.**

`gplbld/sd.iss` gated the data tree with `Check: DataTreeAbsent`, which tested
`DirExists` directly. A Check function is evaluated **per file**. The first
file of the sdsys set created `C:\ProgramData\SD\sdsys`, every later evaluation
therefore answered False, and the remaining ~3,260 files were silently skipped.
The result: 16 files installed, no `gcat`, no `GPL.BP.OUT`, no working
database - and Setup exited 0.

**Why the first round of testing missed it, which is the part worth learning
from.** The machine already had a data tree, put there by hand earlier in the
day while testing install-by-copy. So the only path exercised was the upgrade
one, which skips the whole set consistently and looks identical whether the
Check is right or wrong. Every observable was green: exit 0, files in Program
Files, correct ACLs, SD starting and reporting 431 records - because SD was
reading the hand-made tree, not anything the installer had laid down. The test
that would have caught it is the one that had been deferred all along, and the
reason for deferring it was that the machine was not clean.

The lesson is not "test on a clean machine", which was already written down. It
is that **an install test which does not COUNT what was installed proves very
little**: every high-level check passed against a database the installer had
not written. §7 step 1 now says to count the files and not trust the exit code.

**Fixed but NOT verified.** `InitializeSetup` caches the answer once, before
any file is copied, and `DataTreeAbsent` returns the cached value. The
installer was rebuilt with the fix. It has never been run - the session ended
first, and the machine is left carrying the broken install. The state block at
the top of PROJECT_STATUS.md says what is there and how to clear it.

Two smaller findings from the same round, both real:

- **The uninstaller left a dead directory on the system PATH.** Inno cannot
  undo an appended `[Registry]` value, because the `olddata` constant means it
  cannot know which part it contributed. `RemoveFromPath` now strips it by
  name at `usUninstall`. The uninstaller otherwise did the important thing
  correctly: `C:\ProgramData\SD` survived untouched, which is what a silent
  uninstall must do.
- **A brace comment in an Inno `[Code]` section cannot mention a
  brace-delimited constant.** The comment ends at the first closing brace and
  the prose after it is parsed as code, so the error points at English several
  lines from any statement. The `(* *)` form works - and must not mention
  itself either, which ended the comment the same way and cost a second
  compile.

---

## 14 Aug 2026 - The configuration file finds itself, and the last Inno blocker goes

Instruction from the repository owner: fix the configuration lookup so it does
not need `SCARLET_CONFIG`, and if a variable is still needed, rename it to
`SD_CONFIG`. Both done. This was the last of the four things §5.16 listed as
standing between the staged tree and an Inno package.

**What it was.** The server read `SCARLET_CONFIG` and fell back to
`/etc/sd.conf`; the client library read `SD_CONFIG` and fell back to `sd.ini`
in the Windows directory, with a comment claiming the two matched. They did
not, so setting the variable you would expect configured exactly one of them.
Worse for an install: once the binaries ship with `msys-2.0.dll` beside them
the POSIX root moves to `C:\Program Files\SD\`, so `/etc/sd.conf` resolves
*inside* Program Files — read-only to ordinary users, and separated from the
data it describes. The install test on this day had to set the variable by
hand, which is not an install.

**What it is now.** Both read `SD_CONFIG`; both fall back to
`%ProgramData%\SD\sd.conf`, with the literal `C:\ProgramData\SD\sd.conf` only
as a last resort. `%ProgramData%` rather than the literal because that folder
can be relocated and the variable holds where it actually is — the same
reasoning as deriving PowerShell's path from `%SystemRoot%` earlier in the day.
`SCARLET_CONFIG` is no longer read at all: it named a project this is not part
of, and §5.16's standing rule is to convert rather than tolerate. The
`sd.ini`-in-`C:\Windows` fallback is gone too.

The two values are `SD_CONFIG_ENV` and `SD_CONFIG_DEFAULT` in `gplsrc/sddefs.h`
and are **duplicated** in `sdclilib.c`, because the client is a separate
toolchain that must not include the server's headers (§5.2). Both files say so;
change them together.

Also fixed while here: one caller of `GetConfigPath()` in `sdfix.c` passed a
201-byte buffer where every other passes `MAX_PATHNAME_LEN + 1`, so the
function's contract was whatever the smallest caller happened to be.

**Verified** with `SD_CONFIG` and `SCARLET_CONFIG` both explicitly unset: the
staged tree, installed by copying to `C:\ProgramData\SD\`, started and reported
431 records from `COUNT VOC` and `Pathname: C:\ProgramData\SD\sdsys` from
`LIST ACCOUNTS`.

**Two traps found on the way, and the second one cost the most time in this
session.**

The UCRT64 compiler needs its own `bin` directory on PATH even when invoked by
absolute path. `gcc.exe` finds its DLLs beside itself; the `cc1.exe` it spawns
does not, and resolves them through PATH. Without it, `gcc --version` works and
compiling a one-line program **exits 1 with completely empty stdout and
stderr** — which reads as a broken compiler, not a search path. The Makefile
now sets it from `$(dir $(UCRT_CC))`, so the build no longer depends on the
developer's shell.

And `make sd` lists `sdclilib` as a *prerequisite*, so when the client failed
to build, make stopped before linking `sd` — and left `bin/sd.exe` at its
previous contents. Every test after that measured a binary that did not contain
the change being tested, including a password prompt that was blamed in turn on
`$CRED`, on the CRLF fix, and on `LOGIN`, none of which had anything to do with
it. **After a build failure, check the timestamp on `bin/sd.exe` before
believing any test result.**

**Where this leaves the installer.** All four blockers in §5.16 are cleared. The
remaining work is the `.iss` itself, the `icacls` step, prompting for the SDSYS
password last, and the uninstaller's policy for `C:\ProgramData\SD\`. Two things
are still untested and both need something this session did not have: an install
onto a machine with **no development tree**, and `C:\Program Files\SD\`, which
needs elevation to create.

**State left on this machine.** `C:\ProgramData\SD\sdsys` is a freshly
bootstrapped install with **no SDSYS password and no ACLs**, and it is what SD
now reads by default. The development tree at `/usr/local/sdsys` is unchanged
but is reachable only with `SD_CONFIG=/etc/sd.conf`.

---

## 14 Aug 2026 - The staged tree is bootstrapped, and installing it found four bugs

Instruction from the repository owner: fix the staging gap and pre-bootstrap
the tree. Both done, and the tree has now been **installed and run**, which
had never happened — §4's "the installer is the least tested part of the
system" was accurate, and this is what testing it cost.

**What was built.** `gplbld/bootstrap.py` encodes the sequence that
PROJECT_STATUS §3 carried only as prose and `installsdai.sh` as line numbers.
`gplbld/stage.py --bootstrap` runs it against the staged tree, then retargets
the SDSYS account record to the production path and **checks that nothing else
in the tree embeds the build path** rather than trusting the sweep somebody did
once. `gplbld/pcode_bld.py` takes the sysdir as an argument instead of having
`/usr/local/sdsys` hardcoded.

**The staging gap was worse than "Python is required".** `gplbld/` was not
staged at all, so `bbcmp.py`, `pcode_bld.py` and the `FILES_DICTS` that
`WRITE_INSTALL_DICTS` reads were simply absent — the tree could not have been
installed on any machine, with or without Python. `FILES_DICTS` is now copied
in for the bootstrap and removed afterwards: it is a build input, not data.

**Four bugs, all found by running the thing rather than reading it.**

1. **`sd -stop` killed its own caller.** `stop_sd()` did
   `kill(uptr->pid, SIGTERM)` guarded only by `uptr->uid`, and `kill(0, ...)`
   signals the whole process group. A build script called `sd -stop` and the
   Python process driving it and the shell above that both vanished, silently,
   with exit status zero. It took three attempts to see, because every symptom
   said "the script stopped half way" rather than "something killed me". The
   liveness poll twenty lines below always tested `pid > 0`; this loop did not.
2. **An over-long `SH1` corrupted the parameter after it.** `config.c` used a
   plain `strcpy` into an 80-byte buffer and `sortmem`/`sortmrg` are next in
   the struct, so the 93-character PowerShell value overran and SD refused to
   start with "Invalid value for SORTMRG configuration parameter" — naming a
   parameter the file does not contain. `MAX_SH_CMD_LEN` is 255 now and both
   copies are checked. The other `strcpy` calls in that parser have the same
   shape and are **not** audited.
3. **A CRLF `sd.conf` corrupted every string parameter.** Only `'\n'` was
   stripped, so the carriage return stayed on the value and `SDSYS` became
   `C:\ProgramData\SD\sdsys\r`. Numeric parameters were fine because `sscanf`
   stops at the `\r`, which is what made it look like a path fault. It could
   only ever appear in the *shipped* configuration, never the developer's own
   hand-written LF one - the worst place for a bug to hide.
4. **`ACCOUNTS` records are newline-delimited, not `\xfe`-delimited**, being a
   directory-type file. Rewriting field 1 with the DH field mark flattened the
   record and discarded the account name and the grant list. Caught by looking
   at the bytes, not by any check.

**And three corrections to the recorded bootstrap sequence**, which had rotted
without anyone knowing:

- The last three steps need `-internal`. Written as plain `sd RUN ...` and
  `sd THIRD.COMPILE`, they now sit at the `Account:` prompt that §5.6
  introduced on 13 Aug 2026 and the connection is terminated. Nobody had
  re-run the bootstrap in between.
- `sd -i` completes its work and then dies on signal 6, so its exit status is
  meaningless and the step is judged on what it created.
  `installsdai.sh` had commented the line out, which is why this never showed.
- `THIRD.COMPILE` compiles dictionary I-types and prints no "n error(s)"
  summary, so a build check that demands one fails on a healthy system.

**Verified.** The full bootstrap ran against the staged tree, `SECOND.COMPILE`
compiling 190 programs with no errors. The tree was then installed by copying
to `C:\ProgramData\SD\` and run from the staged binaries: `COUNT VOC` reported
431 records, `WHO` reported `2 SDSYS`, and `LIST ACCOUNTS` showed the
production pathname with the account name and grant list intact. **No Python
and no compiler were used at install time.**

Not proved: the machine still has a development tree, so an accidental
dependency could still be hiding; and `C:\Program Files\SD\` was not used,
since creating it needs elevation. The install also had to be told where its
configuration was, because the compiled fallback `/etc/sd.conf` resolves inside
`C:\Program Files\SD\` once the POSIX root moves. That is the last Inno
blocker and it is now the top of §7.

---

## 14 Aug 2026 - PowerShell becomes the shell, and two standing rules

Follows directly from the entry below, which found that `OS.EXECUTE` ran
`/bin/bash -c` while an installed SD ships no shell. Instruction from the
repository owner: point `SH1` at PowerShell and update the `OS.EXECUTE`
strings.

**It simplified the code rather than complicating it.** The five programs
written earlier the same day each built a PowerShell script and then wrapped it
in bash single quotes to protect it. With PowerShell as the shell the command
*is* the script, so the wrapper and the `>/dev/null 2>&1` came out of all of
them. `!ps_script` changed most: it used to `cat` its temporary file into
PowerShell's stdin, and now names the file **relative to the working
directory** — which removes the need for a Windows pathname that BASIC has no
way to produce, and makes it work whether SDSYS sits at a POSIX path or a
Windows one.

`op_sh.c` derives the PowerShell path from `%SystemRoot%` rather than writing
`C:\Windows`, because the system drive is not guaranteed. It must contain no
spaces: `clparse()` splits on them and does not honour quotes, which rules out
naming PowerShell through anything in Program Files.

**Two measurements decided the design, rather than assumption.**
`Invoke-Expression` propagates a script's exit status and `& .\script.ps1`
does not — a script ending `exit 7` gave 7 through the first and 1 through the
second. `Invoke-Expression` also runs text rather than a file, so the execution
policy does not apply and nothing needs `-ExecutionPolicy Bypass`. Both probes
were re-run afterwards with bash out of the loop: `is_grp_member` 7 of 7,
`ps_script` 5 of 5.

**Two standing rules were given at the same time and are now §5.16.** Every
remaining Linux-ism is to be converted to its Windows equivalent where one
exists, rather than wrapped or tolerated — `/bin/bash` is the cautionary case,
since it looked like an inert default and silently broke every installed
system. And where Linux parity conflicts with the Inno installer, the installer
wins. That second rule settles the pre-bootstrap question in the installer's
favour: the staged tree ships `gcat`, `GPL.BP.OUT` and `PCODE.OUT` empty today,
which would make an end user run the BASIC bootstrap with Python and a
compiler, and that is not something an installer should do.

§5.16 carries the working list of Linux-isms still in the tree and what
"Inno compatible" requires, in dependency order.

---

## 14 Aug 2026 - OS accounts come back, and the shell they need is missing

Covers the working tree at the time of writing; committed in the same change as
this entry.

**A decision was reversed by the repository owner.** PROJECT_STATUS §5.6 said
"Create no OS users and no OS groups at all", on the reasoning that OS account
creation was Linux baggage that did not transfer. The owner's position, stated
on 14 Aug 2026: the *linkage* between an SD account and an OS user is worth
keeping, and Windows offers the same thing through `net user` and
`net localgroup`. The original reasoning was wrong about what was Linux
specific — the mechanism was, the intent was not.

**Read the reversal narrowly.** Provisioning came back; authorisation did not.
Every account still carries its own password, SDSYS is still the only
administrator, and `LOGIN` was not touched. The owner asked for the `sdusers`
login gate back "if it is possible", and it now is — but restoring it is a
separate act, and it pulls against §5.6's "administration is a matter of knowing
the SDSYS password" in a way that is not yet resolved. That tension is recorded
rather than silently decided.

**What was built.** `GPL.BP/CREATE_USER` (`New-LocalUser`),
`GPL.BP/DELETE_USER` (`Remove-LocalUser`), `GPL.BP/SET_PASSWD` (`Set-LocalUser`,
prompting inside SD), `GPL.BP/OS_GROUP` (the four group operations behind one
subroutine, per §5.14), `GPL.BP/PS_SCRIPT` (run a script carrying a secret), and
`GPL.BP/IS_GRP_MEMBER` rewritten. Call sites in `CREATEA`, `DELACC` and
`MODIFYA` swapped. All ten compile clean.

**Three findings, in the order they matter.**

1. **`OS.EXECUTE` needs a shell an installed system does not have, and this is
   not new.** `op_sh.c` defaults to `/bin/bash -c`; `gplbld/stage.py` ships no
   shell. On an installed tree `/bin/bash` resolves inside `C:\Program
   Files\SD\` and is not there. So every `OS.EXECUTE` in the system fails once
   installed, while working perfectly in development. It was found by asking
   whether the new work would survive the Inno installer — a question worth
   asking earlier than it was. Now a trap in §6, with three options and no
   decision.
2. **Elevation is a hard constraint, not a detail.** An ordinary SD session has
   a UAC-filtered token — `BUILTIN\Administrators` present as "Group used for
   deny only" — and `net localgroup ... /add` answers "System error 5. Access is
   denied." Measured, not assumed. Every helper tests for elevation explicitly
   and returns status 5, rather than parsing a localised message.
3. **Windows `sudo` is not Linux `sudo`.** `sudo.exe` ships on build 26200 but
   is disabled by default and enabled from Developer Settings. There is no
   sudoers file and no per-command policy: it asks UAC to elevate your own
   token. "Only the sdsys user can `sudo sd`" holds, but through Administrators
   membership and UAC, not policy. Worth writing down because the Linux
   intuition is misleading here.

**Passwords stay off the command line.** `net user <name> <password> /add` would
expose the password to any local user through Task Manager, `Get-CimInstance
Win32_Process` or ETW — the pattern §8 already rejected for batch login. The
owner chose a temporary script file instead. `!ps_script` writes it inside the
SDSYS directory, where §5.7's ACL inheritance protects it with no permission
call of its own; that is the first practical use of the "noacl breaks chmod but
not inheritance" finding.

**Correction to an earlier instruction.** §6 said the fix for `is_grp_member`
was "to delete these calls, not repair them". That was written when SD was
expected to stop touching OS groups. The routine was repaired instead: it asks
`Get-LocalGroupMember` and distinguishes member, not-a-member and no-such-group
by exit code, which parsing `net localgroup` output cannot do without depending
on the language Windows is installed in. Seven cases verified from inside SD.
Note it costs a bash plus a PowerShell start on a path that runs at every login;
the fast answer is `getgrnam()` behind a KERNEL key, which is known to work but
is new C code.

**Also done, and it was §7 step 2.** `!valid_os_path` accepts backslashes and
spaces, so `C:\Program Files\SD\usr\bin` passes and the binaries can move. 16
cases verified. The protection moved to the call site, which single-quotes:
single rather than double, because bash still reads a backslash as an escape
inside double quotes, so a path ending in a separator would escape the closing
quote.

**What was deliberately not done.** No Windows account was created or deleted —
`sudo` is disabled here, and throwaway OS accounts were not made without the
owner's say-so — so none of the account operations have ever run. `CREATEA`
still carries `sudo chmod g+s`, which is meaningless on Windows and will warn on
every account creation; it goes with §5.7's `icacls` step, whose inheritable
ACEs are its real equivalent.

---

## 13 Aug 2026 — Second prune of PROJECT_STATUS, and the §5.6 reasoning moved here

Rollover, not new work, at the end of the session. PROJECT_STATUS had reached
2123 lines against the ~2000 in §0 rule 5. Trimmed: §4's `LOGTO` case-by-case
table and the escalation program listing (both duplicated entries already in
this file), §5.1, §5.5, §5.8's `sdrealpath` correction, §5.11's purge account
and §5.15's itemised removal list — all of which describe finished work whose
detail is here. §5.6's "what is still missing" list was split, since several of
its bullets described work that was subsequently done.

The one piece that was **moved rather than trimmed** is below: §5.6's reasoning
was not recorded anywhere else, so it is set out here in full before being
reduced to conclusions in PROJECT_STATUS. §5.6 had grown to 255 lines, most of
it the *why* behind decisions that are now built and verified. Nothing was
dropped.

### Why the identity model has the shape it does

### You log in as yourself, then move; the login identity follows you

This is how shared access works and it is what makes it attributable:

- A person logs in with **their own account name and password**. That
  establishes the session identity.
- Access to other accounts is **granted, not shared**. Once in, a person may
  `LOGTO` any account they have been given access to. There is no second
  password to know and none to share.
- **`@logname` does not change on `LOGTO`.** The login identity persists for
  the life of the session, which is the whole mechanism — everything
  downstream attributes to the person who authenticated, not to the account
  they are standing in.
- **Every login and every `LOGTO` is written to an audit log**, in the form
  "SUE logged to JANE at *date/time*".

So the holiday and assistant case is not a shared password. If Sue covers for
Jane, Sue is granted access to JANE; she logs in as SUE, does `LOGTO JANE`, and
the log records that she did. Withdrawing it removes one grant and changes
nobody's password. Nothing is ever shared, so nothing has to be rotated.

This is what raises the bar above OpenQM, where an account password is a single
shared secret with no record of who used it. It also puts administration under
audit for free: SDSYS is reached by `LOGTO SDSYS` from your own identity, and
that entry is logged like any other.

### Why the step-up asks for your own password, not an SDSYS one

`LOGTO SDSYS` requires a password again — the one exception to "granted, not
prompted" — on the grounds that entering administration deserves a deliberate
act rather than an unguarded session becoming an administrative one.

**The password it asks for is the person's own.** This matters and is easy to
get backwards. Re-entering your own credential is re-authentication: it
confirms the person at the keyboard is still the one who logged in, changes
nothing about attribution, and introduces no new secret. An SDSYS password
would be a second shared secret held by every administrator, which is precisely
the OpenQM weakness this model exists to remove — the audit log would still
name the person, but the credential behind the most privileged account in the
system would be shared, and unrotatable without telling everyone.

Log the step-up separately from the `LOGTO` itself, both when it succeeds and
when it fails; a failed step-up is the single most interesting line in the
audit trail.

### Why the credential register is a separate file

`$CRED` is not part of the ACCOUNTS record and must stay that way. `LOGIN`
opens `ACCOUNTS` at line 175, in the user's own process, **before** any
authentication — it must, to know the account exists — and eleven other
programs open it too, including `_VOC_REF` for routine resolution. Verifiers
stored there would let any user pull every account's Argon2 hash and attack it
offline.

In stage 1 `$CRED` is still readable by everyone, since Windows has no setuid
and there is no privileged helper short of §5.7's service, so this does not fix
the exposure. It makes the boundary **exist**, so that §5.7 can later lock one
file to the service account without restructuring ACCOUNTS or migrating data.

## 13 Aug 2026 — Correction: the API server does have a credential check, and it cannot work

Investigation, no code. Prompted by the repository owner's background on
OpenQM: it was very insecure, remote access worst of all, telnet was replaced
with ssh only, and the API never got the same treatment. Since §1 now makes the
API the front door, the question moved to the top.

### Correction

§5.6 and §7 step 6 both said the API server "has no credential check of its
own". **That is wrong.** `APISRVR` line 921 calls `login(username, password)`,
which reaches `op_login()` and then `login_user()` in `linuxio.c`. There are
two paths and the port breaks each in an opposite direction:

- `APILOGIN=1`, which is what `sd.conf` ships, reads `PASSWD_FILE_NAME` —
  `/etc/shadow`. **MSYS2 has neither `/etc/shadow` nor `/etc/passwd`**, the
  same NSS change behind the `is_grp_member` trap. `fopen` returns NULL and it
  returns FALSE, so every API login is refused. The API is **closed, not
  open** — which is the good version of broken, but it means the interface the
  product now exists for does not function at all.
- `APILOGIN=0` skips passwords entirely and trusts `getpeereid()` on an AF_UNIX
  socket — mab's Feb 2024 hardening, and the right model. But **MSYS2 emulates
  AF_UNIX over a TCP loopback socket with a handshake file**, so it is not a
  filesystem object with permissions and "local socket" means much less than
  it does on Linux.

What is genuinely missing, as opposed to broken, is authorisation *after*
connect: `SrvrAccount` reaches any account by name and `@logname` comes from
the client. Both now written into §7 step 6 as ordered work.

### The exposure question, recorded as an open question rather than a decision

The repository owner raised a web front end as a way to make all API access
local — SD behind it, never on the network. Recorded in §8 with three postures
(SD's socket exposed; ssh tunnel; web front end) and, deliberately, with the
argument **against** the web front end given equal weight, because it is the
repository owner's own and it is a serious one: web servers invite attack,
every attacker knows how, scanning is constant and automated, and a custom
protocol on a non-standard port does not attract the same volume. Obscurity is
not security but it is a real reduction in opportunistic traffic.

The counter recorded alongside it is that a web tier does not add network
exposure, it moves it — the comparison is IIS exposed versus `APISRVR` exposed,
and `APISRVR` is 2007 code with fixed 32-byte credential buffers that nobody
has fuzzed. But that argument only beats the status quo, not the ssh tunnel,
which exposes nothing either.

The observation that may settle it: **§1 points at the tunnel.** If the target
user is a Windows developer using SD as a back end, their application is the
front end. SD does not need a web tier to be secure, it needs to stop listening
on the network. Whether SD offers a browser UI is then a product question, and
separating the two is probably what makes either decidable.

Two constraints recorded for whichever posture wins: attribution has to survive
the extra hop, with the front end asserting identity and SD still enforcing the
grant list; and connection pooling breaks `@logname` regardless of `NUMUSERS`,
which is only a default — the repository owner notes OpenQM systems run several
hundred users.

### The network-layer argument, added the same day

The repository owner's second point for the API posture: with a private API you
keep VPN, IP restriction and similar controls that a public web server forfeits
by definition. Recorded in §8, with the structural form of it — a public web
application must accept anonymous connections as far as the login page, so its
TLS stack, HTTP parser, router, session handling and password reset are all
reachable pre-authentication by everyone, while an IP-restricted API has a
pre-authentication surface reachable by nobody. That is a difference in kind
rather than obscurity.

Recorded alongside it, so the record is not misread later: the axis is *public
versus private*, not web versus API. A web front end on an internal network
keeps the same controls, so C's security cost over B is a second codebase to
patch rather than an exposed one.

**And the finding that makes this actionable: SD never binds a listening
socket.** `sd -N` runs per connection with the socket as stdin and stdout —
**xinetd** bound port 4243, spawned per connection and supplied `only_from`.
xinetd does not exist on Windows, so the service replacing it inherits the bind
address, the port, per-connection spawning and access control, and none of it
is implemented. The recommendation recorded is to **bind loopback by default**,
so posture B is what a default install gets without anyone deciding, and to
settle whether `only_from` is reimplemented or replaced by a Windows Firewall
rule written at install time. This also explains why §8's note about keeping
`etc/xinetd.d/` as documentation of the service topology was worth following.

## 13 Aug 2026 — Embedded Python removed; SD is a back end for the API

Decision from the repository owner on 13 Aug 2026, prompted by the staging
script's warning about the 195 MB Python standard library. The answer was not
"ship it" or "trim it" but that embedded Python was never what this is for:
**SD for Windows is a back end data store for Windows developers, reached
through the API.** Recorded as §5.15, and as a scope statement in §1 because it
is the tie-breaker for anything else that asks whether a feature earns its
place.

### Why it was a removal, not a flag

`-DEMBED_PYTHON` looked like a one-line change on `Makefile:73`. It is not:
`gplsrc/sdext_py.c` and `gplsrc/op_sdpyobj.c` carry **no `EMBED_PYTHON` guards
at all** and are listed in `gpl.src`, so they cannot compile without the Python
headers however the flag is set. Removing the flag alone would have broken the
build. And CLAUDE.md's rule against `#ifdef` branches for dead platform code
applies in spirit, so the whole thing went:

- `gplsrc/sdext_py.c`, `gplsrc/op_sdpyobj.c`, `gplsrc/sdext_python_inc.h`, and
  their two entries in `gpl.src`
- the `EMBED_PYTHON` blocks in `op_sdext.c` and `sd.c`
- `PY_HDRS`, `PY_LDFLAGS` and `-DEMBED_PYTHON` in the Makefile
- 20 `GPL.BP/PY_*` programs, `SYSCOM/SDPYFUNC.H`, 4 `sdsys/BP/PY_*` tests
- the `SD_Py*` error codes in `gplsrc/err.h` and the `SD_Py*`/`SD_Obj_*` SDEXT
  keys in `SYSCOM/KEYS.H`

`gplbld/gen_includes.py` regenerated `SYSCOM/ERR.H` and `GPL.BP/ERRTEXT.H` from
the edited `err.h` without being asked twice, which is the first real use of
the tool written earlier the same day.

### Two things that bit, both now traps in §6

**The opcode table is positional.** `kernel.c` builds its dispatch table from
`opcodes.h`, so deleting `op_sdpyobj` broke the link. Deleting the `_opc_` line
would have been far worse — it renumbers every opcode after `0xCFFE` and
invalidates all compiled pcode everywhere. The file's own convention is to
retire an opcode in place by pointing it at `op_illegal` with a generic name,
as `OP_09`, `OP_9E` and `OP_BB` already do; `OP_CFFE` is now one of them.

**And `BCOMP` has a parallel positional list.** It registers intrinsics in
`int.intrinsics` and dispatches through an `on i goto` whose entries are
matched **by position**. Removing `SDPYOBJ` from one without the other would
have silently misrouted every intrinsic after it — a fault that compiles
cleanly and produces wrong code. Both were removed in the same edit.

Also met: the Makefile does not track header dependencies, so editing
`opcodes.h` left a stale `kernel.o` and the link failed pointing at
`kernel.c`, a file that had not been touched.

### Verified

- `make sd` from clean links with no Python, and `objdump -p bin/sd.exe` no
  longer names `msys-python3.12.dll`.
- `SECOND.COMPILE` compiled **187 programs with no errors** — 207 less the 20
  `PY_*` programs, exactly as expected — after recompiling `BCOMP` first,
  since the intrinsic table changed.
- `COUNT VOC` still reports 432 records, `WHO` reports `SDSYS`, and
  `COUNT NOSUCHFILE` still expands to "File not found".
- The staged tree fell from **16.2 MB to 9.6 MB**, and the DLL closure from
  seven to four. `msys-intl-8` and `msys-iconv-2` went too: they were only ever
  present because Python pulled them in.

### What else it took with it

`python-devel` and `gettext-devel` leave the build dependencies (§2).
`gettext-devel` was only ever there because `python3-config --ldflags --embed`
emits `-lintl`, so an unrelated-looking dependency disappeared with the
interpreter. Plain `python` stays: `gplbld/bbcmp.py` is the only thing that can
compile BASIC before a BASIC compiler exists. It is a developer dependency —
an installed system needs no Python at all.

### Consequence to weigh

If the API is the primary interface, §7 step 6 — bringing `APISRVR` under the
identity model — matters more than its position suggests. `APISRVR` has **no
credential check of its own** and its `logname` comes from the client, so any
session it accepts reaches any account by name. That was tolerable as a side
entrance. As the main door it is not. Flagged, not reordered; that is the
repository owner's call.

## 13 Aug 2026 — Staging script written, and it immediately found an install blocker

First cut of `gplbld/stage.py`, §7 step 3a. It assembles both install roots
from an explicit whitelist, computes the MSYS2 DLL closure, writes `sd.conf`
and `etc\fstab`, and emits a `MANIFEST.txt` outside both roots so two builds
can be diffed. 3087 files, 16 MB.

### The whitelist justified itself on the first run

Within minutes of the first staged tree existing, running `sd.exe` from it with
MSYS2 off PATH surfaced something that no amount of reading would have found:

> Warning: '/dev/shm' does not exists or is not a directory.

**Shipping `msys-2.0.dll` beside the executable relocates the entire POSIX
namespace.** The runtime derives its root from the DLL's own directory by
stripping **two** path components — matching MSYS2's `<root>\usr\bin`. This was
guessed wrong twice (parent-of-DLL-directory, then DLL-directory) before being
measured directly with `cygpath -w /` against the staged tree:

| `msys-2.0.dll` at | `/` becomes |
|---|---|
| `<X>\SD\usr\bin\` | `<X>\SD\` |
| `<X>\SD\bin\` | `<X>\` |
| `<X>\SD\` | the parent of `<X>` |

So `/dev/shm`, `/etc/sd.conf` and `/tmp` all move with the DLL. §5.8 said
"binaries and the MSYS2 DLLs beside them in `C:\Program Files\SD\`", which
would have put the POSIX root at `C:\Program Files\` and required creating
`C:\Program Files\dev`. The layout table now says `C:\Program Files\SD\usr\bin`
and the reason is recorded in §6, because it looks like gratuitous Unix-ism
and will otherwise get "tidied up" by a future session.

**Second problem, following from the first.** `/dev/shm` cannot live under
Program Files at all: `shm_open()` creates files in it, so every SD user needs
write access, and Program Files is read-only to ordinary users by design.
Cygwin reads `<root>\etc\fstab`, and a bind entry moves it — verified working:

```
C:/ProgramData/SD/shm /dev/shm ntfs binary 0 0
```

With that in place the staged `sd.exe` ran on a `PATH` of
`C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem` — no `msys64`, no Git
for Windows — and answered `SD is not active.` with no warnings and exit 0.
That is the correct answer, not a failure: the running server's shared segment
belongs to the `msys64` POSIX root and the staged process has its own, which is
the §6 PATH trap behaving exactly as documented.

### What the closure turned out to be

Seven MSYS2 DLLs for the server — `msys-2.0`, `msys-crypt-2`,
`msys-python3.12`, `msys-intl-8`, `msys-iconv-2`, `msys-gcc_s-seh-1`, and
`libsodium-26` from `/usr/local/bin` because it is built from source. Only
`kernel32` and `ntdll` come from Windows. Three of the seven are reachable only
transitively, so direct imports would not have been enough — `objdump -p`
walked recursively, rather than `ldd`, so the answer does not depend on the
loader's search order and would be the same on a machine that could not run the
binary.

`sdclilib.dll` needs **nothing** but Windows system DLLs, which confirms §5.3's
claim about the two toolchains by measurement rather than by assertion.

### Left open

- **The embedded Python standard library is not staged.**
  `msys-python3.12.dll` is in the closure so `sd.exe` loads, but
  `usr/lib/python3.12` is 195 MB and the `PY_*` family will fail without it.
  Ship it, ship a subset, or make `EMBED_PYTHON` optional — undecided, and the
  script prints a warning saying so rather than quietly omitting it.
- `sdsys/BP` ships and contains test programs. The Linux install did the same.
- Nothing sets ACLs yet; that is installer work, not staging.
- **No install has been done from the staged tree.** The run above proves the
  binaries load, not that an install works. Step 3b is still ahead.

## 13 Aug 2026 — Installer: the shell script port is dropped

Decision from the repository owner on 13 Aug 2026, **reversing** the revision
made earlier the same day and recorded in §5.9 as "Two installers, in order:
build-from-source now, Inno Setup later". No code; §5.9 and §7 step 3 rewritten.

### What changed

`installsdai.sh` and `deletesdai.sh` will **not** be ported to Windows. Two
scripts replace them: one that builds a **staging directory** containing
exactly what an install consists of, and one that turns that directory into an
**Inno Setup installer**. The pattern is one the repository owner has used on
another project.

The position has now moved three times, which is worth setting out so a future
session can see it was deliberate rather than drifting:

1. Go straight to Inno Setup, `installsdai.sh` being apt/dnf/zypper, systemd,
   xinetd and `/etc` throughout.
2. No — do the Linux method on Windows first: download, install dependencies,
   compile, install, as a development tool.
3. No — skip it. What that would produce is a *developer* setup script, and §2
   and §3 already serve that reader. The bootstrap sequence, which is the part
   with real value, has to be driven by whichever installer gets written, so
   it is written once either way.

### Why the Linux script existed — the point that settles it

From the repository owner, and this is the part that should stop the question
being reopened. `installsdai.sh` was **not** a developer convenience on Linux;
it was load-bearing. ScarletDME targeted Fedora, Debian, Arch and OpenSUSE
across several versions each, every one with a different compiler, libc and set
of package names. No single binary works across that spread, so **the end user
had to compile**, and the script existed to abstract apt from dnf from pacman
from zypper and drive a build on the user's own machine.

None of that holds on Windows. There is one target, one ABI, and SD ships its
own runtime beside `sd.exe` (§5.8), so there is nothing to adapt to and the
user needs no compiler. Strip the distro handling out of `installsdai.sh` and
what remains is a developer setup tool covered by §2 and §3 already. The
requirement that justified the script is a Linux-specific one that the port
does not inherit — so this is a case where the Windows install ends up
genuinely simpler than the Linux original, which is not true of much else here.

### Why the staging script is the valuable half

Not mainly packaging. Three reasons, and the middle one is the strongest:

- It makes §5.8 executable. The install layout is prose in PROJECT_STATUS; a
  staging script is that layout in a form that either runs or does not, and it
  forces the `<sysdir>/bin` split to be decided rather than remembered.
- **It is a whitelist, and whitelists find accidental dependencies.** `gplsrc`
  sat in the data tree for as long as it did because `installsdai.sh` copied it
  wholesale and nobody asked why — a fault that cost most of a session earlier
  the same day. A script that copies only what is on an explicit list,
  installed onto a machine with no development tree, surfaces that class of
  problem immediately. The installer is the least tested part of the system;
  making it cheap to rerun is what changes that.
- It is where the MSYS2 DLL closure gets **computed by walking the imports**
  rather than guessed. Missing one gives exit code 53 and no message at all.

### Corrections to §5.9 as it stood

- It said the Inno Setup compiler was **not installed**. It is installed on
  this machine.
- It framed the shell-script port as what was wanted first. That is reversed.

### Kept from the old scripts

`deletesdai.sh` is not ported but should be **read** before an uninstaller is
written. Inno supplies an uninstaller; it does not answer what happens to
`C:\ProgramData\SD\`, which holds the user's database. Removing it on uninstall
is a catastrophe and leaving it makes reinstall awkward, because accounts and
`$CRED` are already there. The old script is where the current answer is
recorded.

### Numbering

§7 step 3 is now the staging script and Inno pair, absorbing what was step 9;
steps 9 to 13 shifted down by one. Steps 1, 2 and 4 to 8 are unchanged. The
staging script still cannot jump the queue — step 1 has to settle the layout
for it to have something to stage, and step 2 has to fix `VALID_OS_PATH`,
which rejects both the space and the backslash in `C:\Program Files`.

## 13 Aug 2026 — §3 of PROJECT_STATUS pruned

Housekeeping, recorded so a future session knows the section was shortened
deliberately rather than left incomplete. §3 went from 175 lines to 113, and
the file from 1814 to about 1750.

**Nothing was moved, because everything cut was already here.** What went was
the narrative of a completed bring-up: the `gcat/$CPROC` placeholder
investigation and the `is_bootstrap` red herring (this file, "SD runs. Full
bootstrap completes", and the entry above it), the step-by-step account of what
each bootstrap command produced, the correction of the earlier "`sd -i` blocks
silently" report, and the note that the `/etc/group` blocker had gone. §3 also
still opened with "SD still does not start", three paragraphs above the text
saying it does — stale wording that had survived two sessions.

What was kept is what a session needs to act: the build commands, the bootstrap
sequence itself with the two counter-intuitive steps flagged and a pointer here
rather than an explanation, the state of this machine including every password
and scratch account, and the scripted-session pattern. The "laid down already"
and "machine as this session ended" tables were merged, since the second had
overtaken the first.

The trigger was rule 5 in §0 — the file was at 1814 lines against a ~2000
rollover — but the reason to do it now rather than at 2000 is the rest of that
rule: work had just landed, so the instructions that had been carried out were
the easiest thing in the file to shed.

## 13 Aug 2026 — Batch login raised and designed; admin helpers set as a goal

No code. Two things from the repository owner, both recorded in
PROJECT_STATUS.md rather than here because both are still ahead of the work:
the full reasoning for the first is in §8 under "how does a scheduled job log
in", and the second is §5.14.

**Batch login.** Every account now carries a password (§5.6), which breaks the
`sd -internal SECOND.COMPILE` shape the install script uses and the cron jobs MV
users expect. The design chosen is the repository owner's: an `ALLOWED` item in
SDSYS's VOC listing `ACCOUNT, VOC name` pairs, so that only an administrator can
authorise unattended work, paired with a batch account that grants nobody so
that only an administrator can maintain what runs. It needs no new C code —
`SYSTEM(1026)` already exposes the command line to `LOGIN`.

Recorded here mainly so the alternatives are not proposed again: a password on
the command line is readable by any local user; a password file works and could
be made defensible but a capability list beats a stored credential; and hashing
the VOC entry to detect tampering pins one hop only, because a transitive
closure discovered at run time cannot be hashed. §8 carries the reasoning and
the constraints that came out of working it through.

The install half of the problem turned out not to be a problem: `LOGIN` admits
an administrator to an account with no verifier yet, so an installer that sets
the SDSYS password **last** needs no credential during the bootstrap. That is
now an ordering requirement on §7 step 3.

**Admin helpers.** A goal for after the system runs well: forms in place of
remembered command lines and hand-edited records. The part that matters before
then is the sequencing rule it implies — put administrative logic in
subroutines with a verb over it, so a form can call the same code later. §7 was
renumbered to add both; steps 1 to 9 are unchanged.

## 13 Aug 2026 — The data tree no longer holds C source, and `ERRGEN` turned out to be booby-trapped

Carries out §7 step 1, parts a, b and c. The data tree can now be built and
compiled with `gplsrc`, `gplobj` and `gplbld` absent, which was the blocker on
moving SDSYS to `C:\ProgramData\SD\`.

### What changed

- `GPL.BP/APISRVR` lines 64-65, the `$execute 'BASIC GPL.BP REVSTAMP'` and
  `$execute 'RUN GPL.BP REVSTAMP'` pair, are commented out, exactly as
  `GPL.BP/CPROC` 139-140 already were. `$include revstamp.h` stays.
- `GPL.BP/ERRTEXT` line 33, `$execute 'RUN GPL.BP ERRGEN'`, is commented out
  for the same reason. **This one was not known about** — see below.
- New `gplbld/gen_includes.py` replaces both generators at build time. It
  regenerates `GPL.BP/REVSTAMP.H` from `gplsrc/revstamp.h`, and `SYSCOM/ERR.H`
  and `GPL.BP/ERRTEXT.H` from `gplsrc/err.h`. `--check` reports drift without
  writing, ignoring the generation timestamp.
- The three generated files are regenerated in the repository, which is what
  the drift below made necessary.

### The second `$execute`, which cost the session most of its time

Running `SECOND.COMPILE` with `gplsrc` absent did not simply succeed. It failed
several programs in, with `Unassigned variable ER$ARGS at line 60 of $CATALOG`
— a **run time** abort in a program that had just compiled with no errors.

The cause was `GPL.BP/ERRTEXT`, which carries `$execute 'RUN GPL.BP ERRGEN'`.
`ERRGEN` is a build tool of the same family as `REVSTAMP`: it reads
`./gplsrc/err.h` and writes `SYSCOM/ERR.H` and `GPL.BP/ERRTEXT.H`. Its
statement order is the problem:

```
   openseq 'GPL.BP', 'ERRTEXT.H' to out.f ...
   weofseq out.f                                  <- truncates output 1
   openseq 'SYSCOM', 'ERR.H' to syscom.f ...
   weofseq syscom.f                               <- truncates output 2
   ... writes three header lines to out.f ...
   openseq "./gplsrc/err.h" to in.f else abort    <- only now reads its input
```

With `gplsrc` absent it truncated both outputs and then aborted. `SYSCOM/ERR.H`
was left at **zero bytes**, so every `ER$` constant in the system became
undefined. That does not fail a compile — it produces
`WARNING: ER$ARGS is not assigned a value` and a `0 error(s)` result — so the
compile reported success and wrote broken objects into the global catalogue.
`$CATALOG` and `$BCOMP` were among them, which meant the compiler chain had to
be repaired before anything else could be recompiled. Recovery is in §6 of
PROJECT_STATUS.md.

The lesson is not about `gplsrc`. It is that **a missing `$define` in SD is a
warning at compile time and an abort at run time**, in a program that may not
run until much later.

### The generated files had drifted, and `ERRGEN` would have destroyed the drift

Porting `ERRGEN` and `REVSTAMP` to Python and diffing the output against the
tracked files showed how far they had come apart:

- `GPL.BP/ERRTEXT.H` was generated on 1 Jul 2024 and matched byte for byte for
  all 199 of its entries — and was missing the 42 error codes added to
  `gplsrc/err.h` since. Those errors had no text at all.
- `SYSCOM/ERR.H` matched byte for byte for 199 of its 241 `$define` lines. The
  other 42, the `SD_*` crypto, SDEXT and embedded-Python codes, had been
  **hand-edited**: they kept the C spelling (`SD_Mem_Err` rather than
  `SD$Mem.Err`) and, more seriously, carried the **opposite sign** to the C
  header. `gplsrc/err.h` says `-10100`; the BASIC copy said `10100`.
- `GPL.BP/REVSTAMP.H` was missing one history line. The `$define`s agreed.

Nothing in the BASIC layer references any of the 42 names — the `SD_EUID_SET`
and `SD_EUID_RESTORE` used by `GPL.BP/EUID_SET` and `EUID_RESTORE` are SDEXT
function keys from `SYSCOM/KEYS.H`, values 102 and 103, not error codes — so
regenerating was safe, and it makes the BASIC copy agree with the C.

Note what this means about the `$execute` that was removed: it ran `ERRGEN` on
**every compile of `ERRTEXT`**, so any such compile on a tree that still had
`gplsrc` would have silently overwritten those hand edits. The directive was a
hazard quite apart from the data-tree question.

### Verified this session

- `SECOND.COMPILE` compiled **207 programs with no errors** against a
  `<sysdir>` with `gplsrc`, `gplobj` and `gplbld` moved away — twice: once with
  the original headers and again after regenerating them. (207 rather than the
  204 recorded earlier because the credential programs were added since.)
- `COUNT VOC` still reports 432 records, `WHO` still reports `SDSYS`, and
  `COUNT NOSUCHFILE` still expands to "File not found", which exercises
  `!ERRTEXT` and so the regenerated `ERRTEXT.H`.
- `gen_includes.py --check` reports all three files in sync after the
  regeneration, and reported each of them stale before it.

### Still open

- **`GPL.BP/OPGEN` is not ported.** It generates `GPL.BP/OPCODES.H` from
  `gplsrc/opcodes.h` and reads `./gplsrc` the same way, but **nothing ever
  `$execute`d it** — it is a manual tool, so it did not block this work and
  removing `gplsrc` does not break any compile. It cannot be run on an
  installed system any more, so it must be ported before opcodes can be
  regenerated. It was left alone deliberately rather than ported badly: its
  hex formatting has behaviour that reading the source does not settle
  (`OP.STOP` is commented `;* 00` while `OP.ABORT` is `;* 1`, from the same
  `oconv(value, 'MX')`), and a wrong opcode table is not a failure that
  announces itself.
- **`WRITE_INSTALL_DICTS` still reads `@sdsys:"/gplbld/FILES_DICTS"`.** It is
  an install-time step rather than part of `SECOND.COMPILE`, so it did not
  affect the test above, but it is the last thing that wants `gplbld` in the
  data tree and the installer work has to deal with it.
- The move itself — `SDSYS` to `C:\ProgramData\SD\` and the binaries to
  `C:\Program Files\SD\` — is unblocked but not done.

## 13 Aug 2026 — Correction: `gplsrc` in the data tree was a misdiagnosis. Session ended on credits

**Session ended here, mid-investigation but at a clean stopping point.** The
next session's first move is §7 step 1a, which is a two-line edit. Everything
below is what was learned; nothing was changed in the code for it.

### The decision

The repository owner chose the **data-only** option for
`C:\ProgramData\SD\`: no `gplsrc`, no `gplobj`, no `gplbld` in the database.
So `REVSTAMP`'s dependency on `./gplsrc/revstamp.h` had to be removed rather
than relocated — and investigating how showed the dependency is much smaller
than this file claimed.

### Correction to §6

§6 said "the runtime tree needs `gplsrc`, `gplobj` and `gplbld/FILES_DICTS`",
on the evidence that `installsdai.sh` copies all three and that
`SECOND.COMPILE` aborts at APISRVR without them. The symptom was real; **the
diagnosis was wrong**. What actually happens:

- `SECOND.COMPILE` is a paragraph: `TERM 120,9999` then `BASIC GPL.BP *`. It
  compiles everything and runs nothing.
- `APISRVR` lines 64-66 are `$execute 'BASIC GPL.BP REVSTAMP'`,
  `$execute 'RUN GPL.BP REVSTAMP'`, `$include revstamp.h`. The second is a
  compile-time directive that **runs** REVSTAMP, which opens
  `./gplsrc/revstamp.h`. That is the whole of it — one file, two lines.
- `CPROC` carries the identical pair **already commented out** (139-140),
  with mab's note that the build should compile and run REVSTAMP to sync the
  headers. The fix was already sitting one file away.
- `REVSTAMP` is a build tool that translates the C header into the BASIC
  include `GPL.BP/REVSTAMP.H`. That include is **tracked in the repository and
  already in sync** — both say 1.0-2 — and the C header's own comment says the
  BASIC copy is normally edited by hand.

No consumer was found for `gplobj` in the data tree at all.
`gplbld/FILES_DICTS` is an install-time input, which the installer should read
from the source tree rather than from the database.

### Also settled this session

`C:\ProgramData\SD\` holds three siblings — `sdsys`, `user_accounts`,
`group_accounts` — not SDSYS with the accounts nested inside it. One root is
what makes §5.7 a single `icacls` rather than a grant per location.

And `<sysdir>/bin` turned out to be two unrelated things sharing a directory:
the executables, and the SD file `BCOMP` opens as `@sdsys:@ds:'bin'` for the
pcode composite library. The move must split them, not relocate the directory.

### State of the machine

SD is running from `/usr/local/sdsys` with the current binaries. Passwords:
SDSYS `hunter2`, SUE `correcthorse`, PAT `batterystaple`; JANE and KIM have
none. PAT lives under `C:\ProgramData\SD\user_accounts`, the other three are
still under `/home/sd/user_accounts`. The scratch programs in `<sysdir>/BP`
are listed in §3 — note `SUE/BP/ESCALATE`, the privilege-escalation proof,
which is now harmless but should go with the rest.

---

## 13 Aug 2026 — Administrator rights become the SDSYS account's, and an escalation is closed

§7 item 2, and it grew a third part when the fix turned out not to be one.

### The two ends it started as

`K_ADMINISTRATOR` in `op_kernel.c` was open at both ends. Any positive
argument set the flag, so a BASIC program could grant itself administrator
rights; and `|| IsAdmin()` meant an argument of zero *re-granted* rather than
cleared whenever the caller was in the OS group, so the flag could not be
given up. Nothing cleared it on leaving SDSYS either, so rights followed a
session into whatever account it moved to next.

Fixed by gating the set on `process.program.flags & HDR_INTERNAL` — the
established "this program was compiled `$internal`" test, already used in
`op_jumps.c` and `op_lock.c` — and by having `LOGIN` and `CPROC` set the flag
on entry to SDSYS and clear it on entry to anything else. `sd -ASUE` on a
machine whose token holds `sdadmins` now reports 0 where it reported 1.

### Why that was not enough, demonstrated

The `HDR_INTERNAL` gate only asks whether the *program* is internal, and
anyone could make one: `sd -internal` was not gated, and `BCOMP` accepted the
`$internal` directive on the strength of internal mode alone. The account SUE
compiled this in her own `BP` and ran it:

```
$internal
      program escalate
      crt 'before: ' : kernel(26, -1)
      void kernel(26, 1)
      crt 'after:  ' : kernel(26, -1)
      end
```

`before: 0`, `after: 1`. Key 26 is `K$ADMINISTRATOR`, written as a literal
because an ordinary account cannot reach SDSYS's `INT$KEYS.H` — no obstacle
whatever. **This was run before the fix, not reasoned about**, which is the
only reason the fix is known to be a fix: the same program now fails to
compile, and SUE stays at 0.

`BCOMP` now requires `kernel(K$ADMINISTRATOR, -1)` as well as internal mode
before accepting `$internal`. Building a system program is an administrative
act, so it needs SDSYS.

### And the rule that ties it together

Decision from the repository owner, arriving mid-fix: **`-internal` may only
enter SDSYS, and must know its password.** Implemented in `sd.c` — any other
account with `-INTERNAL` is refused rather than quietly redirected — and by
deleting the internal-mode bypass from `LOGIN`'s `authenticate.account`, which
was the last route into administration that did not involve the SDSYS
password. `LOGIN`'s "administrator with no account named lands in SDSYS" case
went with it, so plain `sd` now asks which account.

**The install is unaffected, and the reason is worth recording**: `sd -i` runs
`$BBPROC`, which never calls `$LOGIN` — it only compiles it. Checked before
the bypass was removed, because removing it blind would have broken the
bootstrap. And on a fresh install SDSYS has no credential yet, so the
"no password set" branch admits an administrator with a warning.

### Verified

`sd -internal -ASUE` refused; `sd -internal` prompts and admits on `hunter2`,
refuses three wrong ones; plain `sd` prompts for the account; SUE reports 0,
SDSYS 1, and SUE stepping up to SDSYS and out again goes 0 → 1 → 0;
escalation fails to compile; `BASIC GPL.BP CPROC` still builds a system
program, which is the regression that matters since `BCOMP` itself changed;
`COUNT VOC` still reports 432; the whole `LOGTO` suite still passes.

### Left standing, deliberately

`kernel.c` still seeds the flag from `IsAdmin()` at process start. It now
decides one thing only — whether a credential-less account can be entered
during a fresh install — and confers no standing privilege, since `LOGIN`
clears it a moment later for any account that is not SDSYS. Removing it
entirely would take the fresh-install path with it.

---

## 13 Aug 2026 — Accounts move to ProgramData, and SD learns to read a Windows path

Decision from the repository owner: SD accounts live under
`C:\ProgramData\SD\user_accounts` and `C:\ProgramData\SD\group_accounts`.
Settles the question opened earlier the same day. `/home/sd` was the right
place while an SD account was an operating system user; under §5.6 it is not
one, so nothing about the Linux location carried over.

### What that turned out to require

Writing the location into `sd.conf` did not work, and the reason was not the
location. Creating the account succeeded and then `openpath` on it failed with
ER_FNF, "file not found", against a path that plainly existed. Measured with a
probe over five spellings:

| Spelling | Before | After |
|---|---|---|
| `C:\ProgramData\SD\user_accounts\PAT\VOC` | FAIL 3003 | OK |
| `C:/ProgramData/SD/user_accounts/PAT/VOC` | FAIL 3003 | OK |
| `/c/ProgramData/SD/user_accounts/PAT/VOC` | OK | OK |
| `c:\ProgramData\...` (lower-case drive) | FAIL 3003 | OK |
| `C:\ProgramData/SD/...` (mixed) | FAIL 3003 | OK |

**The MSYS2 runtime was never the problem.** A five-line C probe confirmed
`stat()` accepts every one of those spellings. The fault was `sdrealpath()` in
`linuxlb.c`, SD's own hand-rolled `realpath()`, which every `openpath` reaches
through `fullpath()`. Its opening `switch` treats anything not starting with
`/` as a *relative* path and prepends the working directory, and its scanner
only ever splits on `/`. So `C:\ProgramData\SD` resolved to
`/usr/local/sdsys/C:\ProgramData\SD`.

It now folds backslashes to `/` and treats a leading drive letter as the root,
with `root_len` replacing the three hardcoded `outpath + 1` root tests. `DS`
stays `/`: this changed what SD accepts, not what it emits.

**Why it was hard to see, and this is the part worth keeping.**
`open_file()` calls `fullpath()` without checking the result, and `fullpath()`
copies its scratch buffer out whether `sdrealpath()` succeeded or not. An
unresolvable path therefore does not fail at the resolver — it produces an
arbitrary string, and the `stat()` a few lines later reports "file not found"
about something nobody passed in. The swallowed return value is still there;
it is in §6 now.

### Corrections to §5.8

That section claimed MSYS2 "accepts `C:/ProgramData/SD/sdsys` with forward
slashes throughout, so stage 1 can move to the correct location while keeping
`/` as the separator". Half right in a way that misleads: the runtime does,
SD did not, and the sentence would have sent the next session looking at mount
tables. Corrected in place, with this entry as the record.

The same claim's consequence was also wrong. Moving `SDSYS` and the binaries
was described as decoupled from the `@ds` question; in fact it was blocked by
the resolver, and now genuinely is decoupled. Flipping `dir.separator` to `\`
has also become testable for the first time, since a backslash no longer
breaks path resolution.

### Verified

`sd -APAT` run from `C:\Windows`, with `USRDIR=C:\ProgramData\SD\user_accounts`
in `sd.conf`, prompted for the password and landed in the account directory.
`COUNT VOC` still reports 432 and the whole LOGTO suite still passes against
the rebuilt binary — stated explicitly because `sdrealpath()` sits on the path
of every file open in the system.

Two cosmetic leftovers, both tied to `@ds` being `/`: the stored path reads
`C:\ProgramData\SD\user_accounts/PAT`, because `CREATEA` joins with `@ds`; and
`@PATH` reports `/c/ProgramData/SD/user_accounts/PAT`, because it comes from
`getcwd()`, which is always POSIX under MSYS2.

### Also recorded, not built

Two goals from the repository owner, now §5.12 and §5.13. **Everything that can
be lower case should be** — account names, file and field names, and the case
inversion at login — with the warning that the comparisons have to become case
insensitive first, or `sue` and `SUE` become different accounts. And
**disabling `SH` and `!` on Linux was a mistake**: programs need Windows
utilities, and shell-out grants nothing the user does not already have at a
command prompt.

### The changelog gap

`sdb_ai/sd64/sdsys/changelog` is the product changelog, ships with the system,
and **the port had added nothing to it** — 841 lines ending at upstream's
Version 1.0-2, while PROJECT_STATUS.md and HISTORY.md carried everything. That
is the wrong division: those two are the state of the work and the reasoning,
and neither is what a user reads. A "Windows port - unreleased" section now
heads the file, covering the identity model, the account move, Windows paths,
the POSIX IPC switch and the no-binaries rule. Maintaining it is now rule 8 in
§0 and a line in CLAUDE.md.

---

## 13 Aug 2026 — SD outside the MSYS2 shell: it works, and one PATH trap is nasty

No code changed. Prompted by the question of whether logging in will one day be
"global and not require MSYS2". Half of that is already true and had never been
tested, so it was.

**The shell dependency is already gone.** `sd.exe` run from a plain PowerShell
prompt answered `COUNT VOC` with 432 records. POSIX paths still resolve —
`/usr/local/sdsys`, `/etc/sd.conf` — because the translation lives in
`msys-2.0.dll`, not in bash. What remains is the *runtime* dependency, which is
stage 2 and unchanged.

It needs two directories on PATH, not one: `C:\msys64\usr\bin` for the runtime
and `C:\msys64\usr\local\bin` for `libsodium-26.dll`, which sits there because
libsodium is built from source into `/usr/local`. Miss either and the loader
fails before `main` with exit code 53 and **no message at all**.

**The trap worth the entry.** Put `C:\Program Files\Git\usr\bin` ahead of
MSYS2 on PATH — Git for Windows ships its own MSYS2 runtime, and it is on
nearly every developer machine — and `sd.exe` starts, runs, and reports
**"SD has not been started"** while the server is running perfectly. The
runtime derives its POSIX root from the location of the DLL that loaded it, so
`/dev/shm` resolves inside Git's installation, where no shared segment exists.
The message names the wrong problem completely.

Both are arguments for shipping the DLLs beside `sd.exe` under
`C:\Program Files\SD\` (§5.8), since Windows searches the executable's own
directory before PATH. §5.8 now says so.

**Where it is still not shell-agnostic: reading a password.** Scripted stdin
from either Windows shell corrupts the first line, which is the password.
PowerShell 5.1 puts a UTF-8 BOM on the stream, so `abc` arrives as six
characters and `abcdef` as nine — measured by counting the asterisks SD echoes,
and `$OutputEncoding` does not suppress it. `cmd.exe` adds a character per line
and an extra empty line that eats one of the three tries. A pipe from bash is
correct, with LF or CRLF. These are artefacts of the sending shell rather than
SD faults, but they surface as "Invalid username or password", which sends you
looking in the wrong place. Also confirmed from `cmd.exe`: a `<` redirect from
a regular file cannot be read at all, so that earlier finding is SD's input
layer and not something about bash.

**What was not tested, and cannot be from here.** Nobody has typed at SD from a
real Windows console. Every test above used redirected stdin, so how the MSYS2
tty layer behaves in `conhost` or Windows Terminal — echo, masked input, arrow
keys, terminfo — is unknown, and the scripted corruption above says nothing
about it. That is now in §4 as the unverified item that "does SD need MSYS2"
actually turns on, and it needs a person at a keyboard.

---

## 13 Aug 2026 — What logging in actually looks like, seen as an ordinary user

No code changed. This entry records what was observed when the question "how
does one log into SD from the command line" was asked, because most of it had
never been seen from outside the administrator's seat.

Every session on this machine is an SD administrator: the token carries
`sdadmins` and `kernel.c` seeds `USR_ADMIN` from `IsAdmin()`. So the ordinary
user's experience was invisible here. A **non-administrator probe** — the §6
recipe with `SD_ADMIN_GROUP` naming a group nobody holds, the inverse of the
probe built when the group work landed — made it visible. The recipe is now in
§6 next to the original.

| Entered as | What happens |
|---|---|
| `sd` or `sd -A`, administrator | straight into SDSYS, prompts for the SDSYS password |
| `sd`, ordinary user | prompts `Account:` then `Password:` |
| `sd -ASUE` | prompts for SUE's password |
| `sd -ASUE WHO` | same, runs the one command, exits |
| `sd -internal` | SDSYS with no password; administrators only |

Three things worth knowing came out of it:

**SD no longer needs an operating system group to use.** The probe logged into
SUE with the account's own password and `SYSTEM(1050)` reported 0. Nothing
about the Windows account mattered. That is what §5.6 was for, and it had never
been shown from the outside.

**The SDSYS password alone makes you an SD administrator.** The same probe ran
`sd -ASDSYS`, gave `hunter2`, and arrived with `SYSTEM(1050)` at 1, because
`LOGIN` sets the flag on entry to SDSYS. Administration is now a matter of
knowing that password rather than of Windows group membership.

**Administrator rights follow you out of SDSYS.** `LOGTO KIM` from there left
the flag at 1 while standing in KIM. This was known to be true while
`IsAdmin()` is true, and blamed on the `op_kernel.c` set hole; here `IsAdmin()`
was false and the flag still persisted, because **no code attempts to clear
it**. §7 item 2 now names both ends of the problem rather than one.

Two smaller findings, both in §6. `sd -A` with no account name sets
`CMD_QUERY_ACCOUNT` and nothing anywhere reads that flag, so bare `-A` is
identical to plain `sd` — for an administrator, going straight into SDSYS
instead of asking which account, the opposite of the option's name. And the
`Account:` prompt echoes in lower case, because `LOGIN` turns `PT$INVERT` on
before it; harmless, but it is the visible face of the case-inversion trap that
cost real time on the password read.

---

## 13 Aug 2026 — SDSYS is the exception; LOGTO takes account names only

Decisions from the repository owner, answering both questions the entry below
raised, and the code that carries them out. Made and built the same day.

### SDSYS reaches every account, without exception

The grant check as first built tested `@logname` and nothing else, so an SDSYS
login could not enter an account that had not granted it — recorded as an open
question because §5.6 did not say. The answer is that SDSYS is the exception:
administration that cannot enter an account cannot repair one.

**The test is the account you are standing in, `who`, not the one you logged in
as.** That reading was chosen deliberately and is worth understanding, because
the alternative is defensible and one line away. Keying on `@logname` would
have meant that the model's own recommended route into administration — log in
as yourself, `LOGTO SDSYS` with your own password — did *not* carry the
exception, while a direct SDSYS login did. The account would be an exception
only for people who knew the shared SDSYS password, which is the arrangement
§5.6 exists to get away from. Keying on `who` gives the exception to whoever is
standing in SDSYS however they got there, and `@logname` still names them.

Observed both ways: logged in as SDSYS, `LOGTO JANE` and `LOGTO KIM` were
admitted although neither grants SDSYS; logged in as SUE, `LOGTO KIM` was
refused, `LOGTO SDSYS` with SUE's own password was admitted, and `LOGTO KIM`
from there was admitted as `LOGNAME=SUE WHO=KIM`.

The one edge to know: stepping *out* of SDSYS puts you in an ordinary account
and you no longer carry the exception. SDSYS → KIM → JANE is refused at the
second move. Returning to SDSYS is never blocked, since it is your own account
by name if you logged in as it, and a grant plus your own password if not.

### LOGTO takes an account name and nothing else

`int.logto` treated anything absent from ACCOUNTS as a pathname to change
directory to. That was the hole the entry below recorded: it reached an
account's directory without ever consulting the grant list, and it was open to
anyone the OS group made an administrator, which on a machine with `sdadmins`
is every session. Rather than resolve paths back to accounts — which needs the
resolved directory, so it means moving before authorising and unwinding on
refusal — the capability is gone. An unregistered directory is not an account.

An unknown name now gives the same refusal as an ungranted one, so the register
cannot be probed for which account names exist. The cost is that a typo reads
as "User not allowed in requested account"; `LOGIN` already makes the same
trade with "Invalid username or password".

`APISRVR`'s `SrvrAccount` took "account name or path" in the same way and now
takes a name only. **Nothing else there was gated and nothing was added**: the
API server has no credential model, its `logname` arrives from the client, and
putting a grant check on top of that would look like a control without being
one. It is now §7 item 4, with the authentication named as the part that has to
come first.

Found while making that change: `revert.to.old.account` put the *directory*
back after a refused account switch but not `account.path`, so `@PATH` was left
holding the path the session had failed to reach. Pre-existing, and made more
visible by the new refusal, which reaches revert with `account.path` empty. It
now restores both.

### What this changed in the record

PROJECT_STATUS §4 had recorded, under Verified, "An SDSYS login cannot `LOGTO`
an account that has not granted it". That observation was correct when made and
is now false by decision, not by error — the behaviour changed the same day.
The bullet has been replaced by what was observed after the change. §8's two
open questions are marked settled rather than deleted.

---

## 13 Aug 2026 — LOGTO is gated by grants, and the shipped binary is verified

Continues the entry below, "Account credentials: register, helpers and login",
which stopped with `LOGTO` untouched. Covers the commit carrying this entry.

### What was built

The second half of §5.6. Entry to an account is now authorised, not assumed.

| Piece | Where |
|---|---|
| `ACC$USERS`, field 4 of ACCOUNTS, the grant list | `sdsys/SYSCOM/KEYS.H` |
| Its dictionary item, and `USERS` added to the default listing | `gplbld/FILES_DICTS/ACCOUNTS.DIC^USERS`, `…^@` |
| `logto.authorised`, the grant check | `sdsys/GPL.BP/CPROC` |
| `logto.step.up`, re-authentication for SDSYS | `sdsys/GPL.BP/CPROC` |
| Messages 10030 and 10031 | `sdsys/MESSAGES` |

The early "is the caller privileged" test at the top of `int.logto` is gone.
It had been `system(27) = 0` and then `K$ADMINISTRATOR`, and both ask the wrong
question: entering SDSYS is what confers administrator rights, so requiring
them to get in is backwards. Authorisation now happens in one place, below the
ACCOUNTS read, where the target account is known — the spot the deleted
`ACC$GROUP` test used to occupy, and it fails the same way that test did.

The step-up asks for **the caller's own** password, not an SDSYS one. This is
the easy thing to get backwards and the whole point of the model: re-entering
your own credential proves the person at the keyboard is still the one who
logged in, and introduces no shared secret. An SDSYS password would be a second
secret held by every administrator, unrotatable without telling all of them.

`KEYS.H` already carried the history line "20240330 mab add ACC$USERS" for a
define that was not in the file. The 0.6.4 changelog describes the same design
— "A list of allowed users is found in ACCOUNTS record, field <ACC$USERS>" — so
field 4 restores what upstream intended rather than inventing a layout.

### What was observed

Two scratch accounts, JANE and SUE, driven from a real login as SUE. The grant
check refused `LOGTO JANE` before the grant and admitted it after; refused
`LOGTO SDSYS` before the grant; and after granting, refused three wrong
passwords and admitted the right one. `LOGTO SUE` into her own account needs no
grant, as it must. A refused `LOGTO` leaves the session where it was and does
not drop the connection.

`@logname` survives all of it — `LOGNAME=SUE WHO=JANE`, and `LOGNAME=SUE
WHO=SDSYS` after stepping up. Administration is reached from a personal
identity, which is what makes the audit log (now §7 item 1) worth writing.

`sd -internal` still enters SDSYS with no password and moves with no grant, so
the bootstrap is untouched. Full table in PROJECT_STATUS §4.

**The shipped `bin/sd.exe` was exercised for the first time.** The token now
carries `sdadmins` — the re-logon that group membership needs had happened
between sessions — so `-stop`, `-start`, `-internal` and a password login all
ran against the real binary rather than the probe build. That closes two
entries that had stood in §4 as unverified since the group work landed.

### Traps found, all of them cheap to hit again

**A confirmation prompt reached by a script spins for ever at full CPU.**
`CATALOG BP WHOAMI GLOBAL` asks "Program is also in private catalogue.
Remove?". The piped input had already run out, the read returned end of file,
and the prompt loop asked again — half a megabyte of repeated prompt in about
two minutes. It reads like a hang; it is the opposite of the lock-wait hang
already in §6, which idles. This one matters beyond testing: §5.9's installer
will drive SD from a script.

**A scripted session must be piped, not redirected.** `cat cmds | sd -AACCOUNT`
works; `sd -AACCOUNT < cmds` stops after the password prompt and exits 0. Both
are non-tty stdin. Not investigated further.

**`OSPATH()` is `$internal`-only**, and fails like `KERNEL` does: the compiler
decides it is an array and complains that it is not in a `DIM` statement.

**`$catalog NAME` in the source catalogues privately**, so the program is
invisible from other accounts. `CATALOG BP NAME GLOBAL`, or a `$`/`!`/`*`
prefix, is what makes it global.

### What is still open

The audit log, which is the remaining half of §5.6 and is now the first item in
§7. Two questions for the repository owner went into §8: whether an
administrator should be able to enter an account that has not granted them —
as built, SDSYS cannot — and the bare-pathname branch of `LOGTO`, which reaches
an account directory without a grant check and is open to anyone the OS group
makes an administrator. Neither is a regression; both are consequences of §5.6
as written, and closing the second means restructuring `int.logto` rather than
inserting a test.

`CREATE.ACCOUNT` was not used to build the test accounts, because `CREATEA`
still shells out to `sudo usermod` and `groupadd`. A scratch program made them
instead. The verb has still never run on Windows.

### Stale entry removed from PROJECT_STATUS §4

§4 still listed "Bootstrap pass 1 has never completed — `sd -i` attaches and
then blocks silently" under *Not verified*, while the *Verified* list directly
above it recorded the complete bootstrap running and 204 programs compiling.
Both were written in the same session; the second superseded the first and the
first was never taken out. The claim itself was corrected on 13 Aug 2026 in
"Correction: `sd -i` was not deadlocked, and not on a semaphore" — the cause
was a stale record lock left by a killed run. The bullet is now removed.

---

## 13 Aug 2026 — Account credentials: register, helpers and login. Session ended on credits

**Session ended mid-task, with LOGTO still to do.** Resume at PROJECT_STATUS
§5.6, which lists the exact insertion points, and read the machine state at the
end of §3 before touching anything.

### What was built

The first half of the identity model in §5.6. Accounts now have their own
passwords, stored as an Argon2 verifier.

| Piece | Where |
|---|---|
| `$CRED` register keyed by account | `<sysdir>/$CRED`, fields in `INT$KEYS.H` |
| `!CRED_SET`, `!CRED_VERIFY` | `GPL.BP/CRED_SET`, `GPL.BP/CRED_VERIFY` |
| `SET.PASSWORD [account]` | `GPL.BP/SET_ACC_PASSWORD` |
| Login password prompt | `LOGIN`, `authenticate.account` |

`$CRED` is a separate file from `ACCOUNTS` on purpose: `LOGIN` opens `ACCOUNTS`
before authenticating anything and eleven other programs open it too, so a
verifier stored there would be readable by every user.

The libsodium primitives were verified before anything was built on them —
neither `!SD_GET_SALT` nor `!SD_KEY_FROM_PW` had ever had a caller. Both work
on Windows.

`LOGIN`'s three account-determination cases collapsed into one, since entry no
longer varies by how you arrived. Two deliberate ways in without a password,
both gated on `K$ADMINISTRATOR` — which now comes from OS group membership via
`IsAdmin()` and cannot be self-granted: an administrator running an internal
command, because the bootstrap runs through `LOGIN` and cannot type a password;
and an account with no password yet, with a warning. Note `-internal` alone is
unguarded in `sd.c`, so the administrator test is the gate, not internal mode.

### Two traps, one of which would have shipped

**`pterm(PT$INVERT, @true)` silently upcases input.** `LOGIN` turns case
inversion on before prompting, so `hunter2` arrived as `HUNTER2`. The password
verified correctly by hand and failed at login with nothing visibly wrong — the
record was found, the salt and derived key were the right lengths, `STATUS()`
was zero. Every intermediate check passed because the only fault was the case of
the bytes. Found by dumping `seq()` of each character. Inversion is now saved,
cleared around the password read, and restored.

**`$internal` is only accepted under `sd -internal`**, gated by `BCOMP` on
`kernel(K$INTERNAL, -1)`. From an ordinary session the directive is rejected and
then every internal-only statement it enables reports "Unrecognised statement",
so the reported lines are all several lines below the actual cause.

Also `WRITE ... THEN` is not valid BASIC here; it produces an unrecognised
statement plus a spurious complaint about text after the final `end`.

### What is not done

`LOGTO` is untouched, so **any authenticated session can still enter any
account** — the login prompt is the only real control at the moment. Still to
write: the grant check on the target account, the step-up password on
`LOGTO SDSYS` against the person's own credential, and confirming `@logname`
survives the move. The `op_kernel.c` set hole is also still open, which is why
administrator rights cannot currently be cleared once `IsAdmin()` is true.

Everything this session was run against the probe build with `SD_ADMIN_GROUP`
overridden to `Users`. `bin/sd.exe` is current but has never been run.

---

## 13 Aug 2026 — History rewritten to purge every binary. All earlier hashes are stale

**Read this before following any commit hash quoted in an entry below.** The
repository history was rewritten on 13 Aug 2026 with `git filter-repo`, so
every hash recorded in earlier entries refers to the pre-rewrite history and no
longer resolves. Mapping for the commits those entries name:

| Subject | Old | New |
|---|---|---|
| Remove superseded Linux artifacts and untrack generated files | `3b4600e` | `b234541` |
| Replace the client library with the enhanced winsdclilib port | `202b965` | `df4202a` |
| Add PROJECT_STATUS, HISTORY and CLAUDE.md for cross-session handoff | `139cdfd` | `af5c9ab` |
| Record the BASIC layer survey in the handoff documents | `4e525d6` | `edd941f` |
| Survey every BASIC to C linkage; record the privilege model finding | `a70520a` | `2416abd` |
| Base SD administrator rights on group membership, not uid zero | `f56de86` | `5509ce9` |
| Raise the PROJECT_STATUS rollover limit to 800 lines | `3248b72` | `2b85a87` |
| Start runtime bring-up; verify the IPC port; unify the admin check | `9c00730` | `016756c` |
| Decide the identity model, install layout, data protection and audit | `59c1de7` | `4b6353b` |
| Require the password again on LOGTO SDSYS | `c1fd5b9` | `d40c068` |
| Raise the PROJECT_STATUS rollover limit to 2000 lines | `a054dbb` | `9d2338b` |
| Start SD for the first time; correct the bootstrap sequence | `fcfce5f` | `4fed1f7` |
| Rule out a semaphore deadlock; find the real bootstrap blocker | `ff0d239` | `a43de38` |
| Base the BASIC privilege tests on K$ADMINISTRATOR | `5c09f0f` | `13c2fcd` |
| Remove the OS group tests; SD now runs | `91c63d8` | `a35d20f` |

Subjects did not change, so matching by subject is reliable where this table is
not enough. Commit count is unchanged at 17.

### What was removed

The previous entry untracked the binaries going forward but left them in
history, where a clone still fetched them. This finishes the job.

- **Windows build output**: `sd.exe`, `sdconv.exe`, `sdfix.exe`, `sdidx.exe`,
  `sdlnxd.exe`, `sdtic.exe`, `sdclilib.dll`, `libsdclilib.dll.a`, and the whole
  `gplobj/*.o` set — about 90 object files.
- **Linux build output that a extension-based sweep missed entirely**:
  `bin/sd`, `bin/sdconv`, `bin/sdfix`, `bin/sdidx`, `bin/sdlnxd`, `bin/sdtic`.
  These are ELF binaries with **no file extension**, left from before the port,
  along with `libsdcli.so`, `sdclilib.so` and `libsdcli.dll.a`. Finding them
  needed a scan of every blob in history for NUL bytes rather than a glob —
  worth remembering the next time something claims to be binary-free.
- **62 compiled `terminfo/` files**, generated by `sdtic` from `terminfo.src`
  and already ignored going forward.
- **Compiled I-type object code inside two install dictionary items**,
  `DICT.DIC^TYPE.CODE` and `DICT.DIC^FORMAT.CODE` in `gplbld/FILES_DICTS`. The
  repository owner pointed out that the install recompiles every I-type, so the
  object code is not needed. Verified rather than assumed: after stripping,
  `THIRD.COMPILE` prints "Compiling TYPE.CODE", which it had not before because
  the compiled form was already present, and `LIST DICT VOC` then resolves the
  I-types normally (`IS.REMOTE I 1L`, `TYPE I 2L`). Field 15 is the source
  checksum and was kept; only the trailing object code fields were blanked,
  which is the shape `DICT.DIC^SMV` already had. This was applied across all
  history by a blob callback, so the object code never existed here — which is
  why there is no separate commit for it, the one that made the change became
  empty and was pruned.

Result: **zero blobs containing NUL bytes anywhere in history**, verified by
walking every object. `.git` fell from about 5.7 MB to 2.3 MB. The four largest
remaining blobs are all legitimate text source — `BCOMP`, `bbcmp.py`, `SED` and
`QPROC`.

`bin/README` was deliberately kept, so the directory is still documented.

### Method, and the safety net

`git filter-repo` was downloaded for this (with permission) since MSYS2 has no
pip and `filter-branch` is deprecated. It needs Git for Windows on `PATH` when
run from the MSYS2 shell, which is not the default. It also removes the
`origin` remote as a safety measure, so that had to be re-added before pushing.

**A full bundle of the pre-rewrite repository was taken first** and is at
`pre-rewrite-backup.bundle` in this session's scratchpad. That is outside the
repository and will not survive the machine; if the old history matters, copy
it somewhere durable now. Recovery is `git clone pre-rewrite-backup.bundle`.

---

## 13 Aug 2026 — SD runs. Full bootstrap completes; no binaries in the repository

Two changes, one of them a reversal of policy set earlier the same day.

### The OS group membership tests are gone

`is_grp_member` calls removed from `LOGIN` (the `sdusers` login gate and the
`ACC$GROUP` account gate), `CPROC` (`LOGTO`) and `APISRVR` (three sites), along
with the `deffun` declarations, which had no callers left. This is §5.6: SD
consults no operating system group.

**It also means nothing currently restricts entry to any account.** That is the
intended interim state — account credentials replace the groups — but the
system is open until that is built, and should not be exposed to anything
meanwhile. §7 step 1 is now the credential model, and it is urgent rather than
merely next.

The calls in `CREATEA` and `MODIFYA` were left deliberately. They guard
`OS.EXECUTE` calls to `useradd`, `usermod` and `groupadd`; removing the guard
alone would let those shell-outs run unconditionally, which is worse than
leaving them in place. They go when the OS account commands go, as one change.

### The bootstrap now runs to completion, and SD answers commands

| Step | Result |
|---|---|
| `sd -i` | 9 programs compiled, `VOC` and dictionaries created |
| `SECOND.COMPILE` | **204 programs compiled with no errors** |
| `WRITE_INSTALL_DICTS` | dictionary entries written, "COMPLETE" |
| `THIRD.COMPILE` | I-types compiled |
| `BASIC GPL.BP CPROC` | real 24 KB `gcat/$CPROC`, replacing the placeholder |

```
sd -ASDSYS WHO          -> 7 SDSYS
sd -ASDSYS COUNT VOC    -> 431 record(s) counted
sd -ASDSYS SELECT VOC   -> 431 record(s) selected to list 0
```

Reading records back works. `@ds` hardcoded to `/` compiled 204 programs, which
settles that question for stage 1.

Three things were learned getting there, all recorded as traps.

**Grep the BASIC case-insensitively.** There were five `system(27)` privilege
tests, not four: `WRITE_INSTALL_DICTS` spells it `SYSTEM(27)`. A case-sensitive
sweep found four, and the survivor stopped the bootstrap two steps later. This
directly caused a wasted cycle.

**`KERNEL` is only available to `$internal` programs.** `WRITE_INSTALL_DICTS`
is not one, and `KERNEL(K$ADMINISTRATOR, -1)` there produced "WARNING: KERNEL is
not assigned a value" — the compiler treating it as a variable, not an unknown
function. `SYSTEM(1050)` returns the same `USR_ADMIN` flag (`op_sys.c` case
1050) with no such restriction, and is the right call for non-internal code.

**The runtime tree needs `gplsrc`, `gplobj` and `gplbld/FILES_DICTS`.**
`installsdai.sh` copies all three into `<sysdir>`, and the list recorded in §3
had omitted them. `REVSTAMP` opens `./gplsrc/revstamp.h` relative to the account
directory, so `SECOND.COMPILE` aborted at APISRVR with "Cannot open gplsrc
revstamp.h", which reads like a compiler fault and is a missing directory.

The stale-lock trap recorded in the entry below proved itself twice more: an
aborted `SECOND.COMPILE` left a lock on the sequential file `REVSTAMP` writes,
and the retry sat at 0.47 s of CPU over 78 s until SD was restarted. The
documented fix — stop and start — worked both times.

Still outstanding: every catalogue write prints "Unable change ownership of
directory error ... err: 1000", which is `CATALOG` doing the Linux `chown` to
`sdsys:sdusers`. Non-fatal, and it belongs with the rest of the OS account work.
Also `LOGIN` carried a mangled banner, `END-HISTORYPTION:`, where the AI cleaning
cycles had merged `END-HISTORY` and `START-DESCRIPTION:`; repaired in passing.

### No binaries in the repository

Decision from the repository owner, **reversing** the position recorded earlier
the same day that linked binaries in `bin/` were tracked so the install scripts
could deploy them from a clone. Everything must be auditable from source — the
same reason the pcode build is Python rather than a shipped binary.

Eight files untracked: `sd.exe`, `sdconv.exe`, `sdfix.exe`, `sdidx.exe`,
`sdlnxd.exe`, `sdtic.exe`, `sdclilib.dll`, `libsdclilib.dll.a`. They are still
built by `make sd` and still needed at runtime; they were untracked, not
deleted. `.gitignore` now excludes `bin/` and every `.exe`, `.dll`, `.a`, `.o`,
`.so`, `.lib` and `.obj` anywhere in the tree, and CLAUDE.md carries the
constraint so it is read before anything is added back.

The consequence for §5.9 is that installing means building: `installsdai.sh`
does `cp -R bin "$sdsysdir"` and tests for `bin/sd`, both of which assumed a
clone already held the binaries.

**The binaries remain in git history**, so a clone still fetches them and the
audit goal is only half met. Purging needs a history rewrite and a force push,
which is destructive to existing clones and breaks the commit hashes this
archive quotes. Not done without asking; recorded as an open question in §8.

---

## 13 Aug 2026 — Privilege tests moved to K$ADMINISTRATOR; bootstrap pass 1 completes

**SD compiled BASIC and created database files on Windows for the first time.**

### The change

Three privilege tests in the BASIC layer asked `SYSTEM(27)`, which is
`getuid()`. There is no uid zero on Windows, so each answered the same way
permanently (§5.5). They now ask `KERNEL(K$ADMINISTRATOR, -1)`:

| File | Was | Effect on Windows |
|---|---|---|
| `BBPROC` (~line 129) | `system(27) # 0` | bootstrap always refused |
| `CATALOG` (~line 105) | `system(27) # 0` | `CATALOG GLOBAL` always refused |
| `CPROC` `int.logto` (~line 2461) | `system(27) > 0` | `LOGTO SDSYS` always refused |

`LOGIN:217` already used `K$ADMINISTRATOR` and needed no change.

**The tests alone would have achieved nothing**, because nothing set the flag.
`CPROC` was the only thing that ever called `kernel(K$ADMINISTRATOR, 1)`, and
only inside its `system(27) = 0` branch, which never runs here — so
`K$ADMINISTRATOR` answered "no" for everybody and swapping one always-false
test for another would have changed the message and not the outcome. So
`kernel.c` now seeds `USR_ADMIN` from `IsAdmin()` where the user table entry is
initialised, next to the existing `USR_PHANTOM` and `USR_SDAPISRVR` flags.

That keeps the OS group as the source of administrator status for now, which is
the interim position: when the credential model in §5.6 lands, entry to SDSYS
becomes what sets the flag. It also means the seeding is the single place to
change, rather than scattered tests.

`CPROC`'s `system(27) = 0` "entered as root?" branch at line 272 was left as
found. It guards `EUID_SET`, which has no Windows equivalent, and its
`kernel(K$ADMINISTRATOR, 1)` is now redundant.

### Result

`sd -i` exits 0. It compiled `CPROC`, `LOGIN`, `BASIC`, `BCOMP`, `PTERM`,
`CATALOG`, `PARSER`, `IS_GRP_MEMBER` and `TERM` with zero errors each, and
created `VOC`, `ACCOUNTS.DIC`, `$HOLD.DIC`, `$MAP`, `$MAP.DIC`, `$IPC`,
`DICT.DIC`, `DIR_DICT` and `VOC.DIC`. `GPL.BP.OUT` went from 4 objects to 11.

So the compiler chain works — `BCOMP`, `@ds` path resolution, the pcode loader
— and so does DH file creation. Both were unverified. The `@ds` question raised
in §6 is answered for stage 1: hardcoded `/` is correct on the MSYS2 runtime.

### Where it stops now

`SECOND.COMPILE` fails with "This user is not registered for String Database
(sd) use" — `LOGIN:193`, `is_grp_member(lgn.id,'sdusers')`, failing because
`IS_GRP_MEMBER` parses `/etc/group` and MSYS2 has no such file. Predicted in
the entry below and hit exactly where predicted. Pass 1 escaped it only because
`-i` runs `$BBPROC` instead of `LOGIN`. Under §5.6 the calls get deleted.

### Method note worth keeping

Testing a BASIC edit needs three steps, not one: edit the repository copy, copy
it to `<sysdir>/GPL.BP/`, then compile it. `$BBPROC` is compiled by
`gplbld/bbcmp.py`. Skipping the copy leaves the running system on the old code
with no indication anything was missed. Recorded as a trap.

All of this still runs against the probe build with `SD_ADMIN_GROUP` overridden
to `Users`, since the token has yet to pick up `sdadmins`.

---

## 13 Aug 2026 — Correction: `sd -i` was not deadlocked, and not on a semaphore

Corrects the entry below, "SD started for the first time; the bootstrap
deadlock was not one", which recorded `sd -i` as blocking silently and named a
semaphore deadlock as the first thing to eliminate. It is neither.

### It is not a semaphore deadlock

Established two independent ways.

A `sem_getvalue()` probe against all six named semaphores read **1 (free) on
every one**, both at idle and while a process was blocked. And `LockSemaphore`
in `sdsem.c` is a spin loop — `while (sem_trywait(...) != 0) RelinquishTimeslice;`
where `RelinquishTimeslice` is `sched_yield()` — so a process stuck there would
burn CPU continuously. The blocked process used 0.36 s over 95 s of wall clock.
Whatever it was waiting on, it was sleeping, not spinning.

### What it actually was: a stale record lock, self-inflicted

`strace` (MSYS2's, which launches rather than attaches) showed the process
stat'ing `/tmp/bbproc.log` and then `clock_nanosleep(0.250000000)`, over and
over. That is the record-lock wait path in `op_dio3.c` around line 1065:
conflicting lock held by another user → `Sleep(250)` → re-execute the opcode →
repeat, with no timeout and no message. `BBPROC:118` opens `/tmp/bbproc.log`
with `openseq ... overwrite`, which is what wanted the lock.

The lock was left behind by earlier `sd -i` runs that this session killed. The
lock table lives in the shared segment, so a process killed with SIGTERM or
SIGKILL never releases what it held, and every later run waits on it forever.
`sd -stop` followed by `sd -start` clears it, because the segment is unlinked
and recreated empty. Recorded as a trap in §6 — the symptom (no output, no
return, no CPU) reads exactly like a deadlock and is not one.

### What is really blocking bootstrap pass 1

On a clean lock table `sd -i` does not hang at all. It returns immediately with

```
Command requires administrator privileges
```

and aborts. That message is **not** `check_admin()` in `sd.c` — it is
`BBPROC:133`, `if system(27) # 0`, which is always true on Windows because
`SYSTEM(27)` is `getuid()` and there is no uid zero. It is the §5.5 trap hit
for real, and it is the same message from a different place, which is what made
it confusing earlier in the session.

**So runtime bring-up and the identity work have converged.** Pass 1 cannot
proceed until the privilege tests move to `KERNEL(K$ADMINISTRATOR, -1)` per
§5.6. The probe build's `SD_ADMIN_GROUP` override cannot help, because BBPROC
tests `SYSTEM(27)` directly and never consults `K$ADMINISTRATOR`. §7 has been
reordered accordingly.

### Also confirmed while investigating

`sd -stop` works, including the new liveness poll that replaced the System V
attach count. It reported a clean shutdown and left `/dev/shm` completely
empty — segment and all six semaphores unlinked — after which `sd -start`
brought the system up again. The full start/stop/restart cycle runs. That
closes an item listed as unverified.

Also: `sd -start` does not hang when its output goes to a file rather than a
pipe, confirming the diagnosis in the entry below that the apparent hang is
`sdlnxd` inheriting stdout and stderr.

---

## 13 Aug 2026 — SD started for the first time; the bootstrap deadlock was not one

Covers the documentation commit after `a054dbb`. No code changed. **SD created
its shared segment and ran, which it had never done before.**

### Correction: the recorded bootstrap sequence was wrong

PROJECT_STATUS §3 described a deadlock — `sd -i` reporting "SD has not been
started" while `sd -start` could not run because `config.c` demands
`<sysdir>/gcat/$CPROC`, which only the last bootstrap step creates. It suggested
reading the `is_bootstrap` flag in `sd.c` to resolve the ordering.

There is no deadlock. The sequence as recorded omitted two steps that
`installsdai.sh` performs. The installer creates an **empty placeholder** at
line 468:

```sh
# Fool sd's vm into thinking gcat is populated
sudo touch /usr/local/sdsys/gcat/\$CPROC
```

then runs `sd -start` at line 590, *before* `sd -i` at line 604. `read_config()`
only calls `access(path, 0)`, so an empty file satisfies it; the real catalogue
overwrites the placeholder at the end. Confirmed by creating the placeholder by
hand, after which `-start` proceeded.

Two things worth recording about the investigation. The `$CPROC` check exists in
the original Ladybridge source as well — `gplsrc/config.c` in the external
reference tree — so it is not something the AI cleaning cycles introduced, which
was the first suspicion. And `is_bootstrap` is a red herring: it is set at
`sd.c:321` and never consulted by `bind_sysseg`.

### SD started

With the placeholder in place and a probe binary built per §6 (both `sd.c` and
`linuxlb.c` recompiled with `-DSD_ADMIN_GROUP='"Users"'`, since the token still
lacks `sdadmins`), `sd -start` created `/dev/shm/sd_shm_716d0301` at 100 KB and
six semaphores `sd_sem_716d0302_0` through `_5`, and spawned `sdlnxd`, which
stayed up. That is the `shm_open`/`ftruncate`/`mmap` creation path in
`sysseg.c` executing for the first time. The standalone lifecycle test recorded
earlier had exercised the same calls, but never from within SD.

Multi-process attach followed for free: `sd -i` attached to the existing
segment, was allocated a user table slot, and wrote to `<sysdir>/errlog` —
"User 2 (pid 1931, don)". Both were listed as unverified.

### Where it stops now

`sd -i` blocks silently. No output at all, and it never returns. It is blocked
rather than looping — 0.36 s of CPU over 95 s of wall clock — and behaves
identically whether given `/dev/null` or a real pty via `script`. The suspicion
worth eliminating first is a semaphore deadlock, because that would mean a
defect in the `sdsem.c` port rather than another missing install step. Reading
`$BBPROC` is the other thread to pull, since `-i` installs it as the command
processor and it is the only thing running at that point.

### Two traps found the hard way

`sd -start` appears to hang. It has not: it spawns `sdlnxd`, which inherits
stdout and stderr, so any shell capturing output blocks until the *daemon*
exits rather than until `sd -start` does. The parent returned long before.

`sd -SUSPEND` is sticky and survives the process, because the flag lives in the
shared segment. Every later invocation dies with "SD is suspended" and no hint
of why. This was self-inflicted here — a diagnostic loop ran `-SUSPEND` and the
next twenty minutes of "SD is suspended" looked like a new failure. `sd -RESUME`
clears it. Neither verb calls `check_admin()`, so any user can suspend a running
system; worth revisiting under §5.6.

---

## 13 Aug 2026 — PROJECT_STATUS rollover limit raised to 2000 lines

Supersedes the entry below, "PROJECT_STATUS rollover limit raised to 800 lines",
on the figure only. Its reasoning still holds; the number was still too small.

800 was set earlier the same day, after 400 proved too tight, and was binding
again within hours — the identity, install layout, data protection and audit
decisions took the file to 826. Raising it twice in one day is the signal: the
figure was being chosen to feel tidy rather than to serve a purpose.

**The purpose, stated by the repository owner: stop the file growing to several
thousand lines, as happened on another project, where it stops being something
anyone reads.** It is not there to keep the document at a convenient size, and
approaching it is not a problem. 2000 leaves real headroom — roughly two and a
half times the current content, and far enough below the failure case that this
should not need revisiting.

The wording in both PROJECT_STATUS §0 and CLAUDE.md now carries that intent, so
a later session does not read the number as a budget and start compressing live
material to stay under it. Added a note on *when* to prune: just after work
lands, when instructions that have been carried out turn into history and shed
easily — not when a line count is approached.

---

## 13 Aug 2026 — Step-up authentication on LOGTO SDSYS

Follows the entry below, which this refines rather than corrects. Covers the
documentation commit after `59c1de7`. No code changed.

That entry recorded `LOGTO` as needing no password, access being by grant. The
repository owner added one exception: **`LOGTO SDSYS` prompts for the password
again.** Entering administration should be a deliberate act, not something an
unguarded session drifts into.

**The password asked for is the person's own, not an SDSYS password**, and the
distinction is the whole value of the change. Re-entering your own credential
is re-authentication — it confirms the person at the keyboard is still the one
who logged in, keeps attribution intact, and creates no new secret. An SDSYS
password would be a second shared secret held by every administrator, which is
exactly the OpenQM weakness this model was built to remove: the audit log would
still name a person, but the credential guarding the most privileged account in
the system would be shared, and unrotatable without telling everybody.

The step-up is logged separately from the `LOGTO`, on success and on failure. A
failed step-up is the most interesting single line the audit trail can carry.

---

## 13 Aug 2026 — Identity, install layout and data protection decided

Covers the documentation commit that follows `9c00730`. No code changed. Four
decisions from the repository owner, and the investigation that informed them.

### The decisions

1. **Every SD account carries its own password; OS groups are dropped from SD
   entirely.** SD has no users, only accounts — user accounts for one person,
   group accounts reachable by many. **SDSYS is the only administrator**,
   entered by password prompt from `sd -ASDSYS` or `LOGTO SDSYS`. This is the
   PICK / UniVerse / OpenQM model. Now PROJECT_STATUS §5.6.
2. **The install layout follows Windows standards**, not Unix: binaries under
   `C:\Program Files\SD\`, data and configuration under `C:\ProgramData\SD\`.
   Now §5.8.
3. **The installer becomes an Inno Setup binary** (preferred) or a PowerShell
   script, replacing `installsdai.sh`. Now §5.9.
4. **The data tree must be protected from snooping.** Now §5.7.

### This supersedes a decision made the same day

`f56de86` and `9c00730` had just committed the opposite model: SD administrator
rights from membership of an `sdadmins` local group, with `IsAdmin()` resolving
it through `getgrnam()`. That work is not wasted — `IsAdmin()` still gates
`sd -start`, which happens before any account or password exists — but it is no
longer the identity model. See §8 for what remains to decide about it.

### Corrections to what §8 recorded as evidence

The open question in §8 listed evidence favouring an internal administrator
flag. Two of the three points were wrong, and are corrected here.

**Wrong: "SD already has the machinery — login records carry `LGN$ADMIN`."**
The `$LOGINS` register was removed on 12 Jun 2024. There is no `$LOGINS` file
in `sdsys/`; every read and write of it is commented out in `LOGIN` and
`APISRVR`, including both `kernel(K$ADMINISTRATOR, lgn.rec<LGN$ADMIN>)` calls,
which were the only consumers of the flag. `LGN$ADMIN` survives in
`INT$KEYS.H` as a `$define` pointing at a file that no longer exists. An
internal flag would therefore have meant reintroducing a retired register, not
reusing existing machinery. `ACCOUNTS` cannot substitute directly — it is keyed
per account, not per user — though under the decision actually taken that turns
out to be exactly the right granularity.

**Overstated: "on the current design the OS is still the authority."** It is
not, inside the BASIC layer. `op_kernel.c` grants `USR_ADMIN` unconditionally
for any positive argument, so any user who can run BASIC can call
`kernel(K$ADMINISTRATOR, 1)` and become an SD administrator — which is exactly
what `CPROC` does. `IsAdmin()` is consulted only when the argument is zero,
which also reads backwards: passing "clear" *grants* admin to a group member.
The OS was genuinely authoritative only at `sd -start`. This hole must be
closed under the new model too, or the SDSYS password gate is decorative.

**Refined, not wrong: the re-logon delay.** It was recorded that an OS group
cannot make the installing user an administrator immediately, because Windows
fixes group membership in the token at logon. That is correct for `IsAdmin()`,
which reads the token via `getgroups()`. It is *not* correct for the BASIC
layer's `is_grp_member`, which reads the group's member list and so sees a new
member at once. The two would have disagreed for one logon — SD granting access
the OS would still refuse — which is worse than failing closed. Moot under the
decision taken, but worth not rediscovering.

### `/etc/group` does not exist under MSYS2 — a blocker, found before it bit

`IS_GRP_MEMBER` reads `/etc/group` as a text file. MSYS2 and Cygwin dropped
`/etc/passwd` and `/etc/group` years ago in favour of direct SAM/AD lookups, and
neither file is present on this machine. So `is_grp_member` sets status 1 and
returns false for every caller, which fails the `sdusers` test at `LOGIN` 193
and terminates every connection with "This user is not registered for SD use".

This sits one step past where runtime bring-up stopped, so it would have been
met head-on in the next session. It is *not* the `getgrnam()` path verified in
§4 — that goes through the NSS layer and works correctly. Under decision 1 the
`is_grp_member` calls are deleted rather than repaired, which disposes of the
blocker as a side effect.

### Data protection: what was found, and why it is stage 2

The premise behind decision 4 was that OS directory permissions keep an
account's contents private. Two findings, both verified on this machine.

**`chmod` cannot secure anything here.** The MSYS2 mount is `noacl`
(`none / cygdrive binary,posix=0,noacl,user`). `chmod 0770` on a test directory
left it `drwxr-xr-x` and changed no ACE. `C:\ProgramData` grants
`BUILTIN\Users:(I)(OI)(CI)(RX)` by inheritance, so a directory created there is
world readable and snooping requires no privilege at all.

**But ACL inheritance is unaffected by `noacl`, which makes the fix
practical.** Breaking inheritance and granting narrowly works, needs no
elevation for a directory you own, and — the useful part — files subsequently
created *through the MSYS2 shell* inside that directory inherit the restricted
ACL correctly, because NTFS applies inheritance in the kernel at creation time,
below the runtime. Verified by writing through MSYS2 into a locked directory
and reading back the resulting ACE. So the installer sets permissions once with
`icacls` and everything SD creates afterwards is protected automatically. This
also answers the `chmod g+s` problem left open earlier: the setgid directory
behaviour *is* inheritable ACEs.

Use SIDs rather than names in the installer — `*S-1-5-18` for SYSTEM,
`*S-1-5-32-544` for `BUILTIN\Administrators` — so a localised Windows does not
break it. `/inheritance:r` must come first; `/grant` alone leaves the inherited
`Users:(RX)` in place and the tree stays readable.

**The limit, and it is architectural.** Every SD process opens the database
directly — `dh_open()` → `dio_open()` → `open()` — in its own process, under the
invoking user's token. `connection_type` (`CN_CONSOLE`, `CN_SOCKET`, `CN_PIPE`)
describes only the terminal transport; there is no data server. So any ACL
strong enough to stop a user reading the files in Explorer also stops SD reading
them on that user's behalf. **While SD runs as the invoking user, account
passwords organise access but do not secure it.**

Real protection needs `sdlnxd` to become a Windows service under a dedicated
service account that owns the tree, with session processes spawned under the
*service* identity and users reaching them over the named pipe. That is the
direct Windows equivalent of the Linux original dropping to the `sdsys` user via
`EUID_SET`, not a Windows novelty. It requires console `sd.exe` to become a
client rather than doing its own file I/O, which is the substantial part, and it
belongs with the stage 2 `fork` → `CreateProcess` work. Until then the
achievable goal is blocking everyone who is not an SD user, which is worth
having and is not the same as privacy between accounts.

### Also found

The server and client disagree about the configuration file. `GetConfigPath()`
in `inipath.c` reads `SCARLET_CONFIG`, falling back to `/etc/sd.conf`;
`sysdir()` in `sdclilib/sdclilib.c` reads `SD_CONFIG`, falling back to `sd.ini`
in the Windows directory — and its comment claims the two match. They do not.
`sdnet.h` also hardcodes `PASSWD_FILE_NAME "/etc/shadow"`. Folded into §5.8.

The password machinery decision 1 needs already exists and is wired: `SD_SALT`
(100) and `SD_KEYFROMPW` (101) reach `crypto_pwhash` (Argon2) through SDEXT, and
`_INPUT` already supports masked entry via `IN$PASSWORD`. No new C code is
needed for salt, derive and compare.

### Where the verifiers must not go

The first draft of §5.6 said to add salt and verifier as ACCOUNTS fields 4 and
5, appended for backward compatibility. That is wrong and was corrected before
this entry was committed. `LOGIN` opens `ACCOUNTS` at line 175 in the user's own
process *before* authenticating — it has to, in order to know the account exists
— and eleven other programs open it as well, `_VOC_REF` among them for routine
resolution. Every SD user's process can therefore read it, and verifiers stored
there would let any user harvest every account's Argon2 hash for offline attack.

They go in a separate register keyed by account name. In stage 1 that file is
still readable by everyone, since Windows has no setuid and there is no
privileged helper short of the service model, so the split does not fix the
exposure. Its value is that the boundary exists from the start, so the service
model can lock one file down without restructuring ACCOUNTS or migrating data.

### Several people per account, and why one password each is not enough

Noted by the repository owner: a user account is sometimes reached by more than
one person — cover during holidays, assistants. A per-account password supports
that with no mechanism at all, which is a genuine advantage over the OS group
model where each person had to be enrolled and removed.

The first draft of §5.6 stopped there and listed the consequences — no
attribution, and rotation for everyone when one person's access is withdrawn —
as costs inherent to shared credentials, to be stated rather than engineered
away. **The repository owner rejected that**, and correctly: a single password
shared between people is a classic weakness, and raising the security level
above OpenQM was one of the motives for this whole change. A model that cannot
name who logged in fails the goal that prompted it.

An intermediate draft proposed a credential list per account — one name, salt
and verifier per person permitted into it. The repository owner replaced that
with something simpler and better, which is what §5.6 now records: **you log in
as your own account, and the login identity follows you.** Access to other
accounts is granted rather than shared, `LOGTO` needs no second password,
`@logname` never changes, and every login and every `LOGTO` is written to an
audit log as "SUE logged to JANE at *date/time*".

Sue covering for Jane is therefore not a shared password at all. Sue is granted
access to JANE, logs in as SUE, does `LOGTO JANE`, and the log records it.
Withdrawing the cover removes one grant; nobody's password changes, because
nothing was ever shared. Administration comes under audit for free, since SDSYS
is reached by `LOGTO SDSYS` from a named identity.

Grants are recorded on the target account — JANE lists who may enter JANE —
because that answers the question administration actually asks and puts
revocation in one place. `$LOGINS` chose the opposite direction with
`LGN$VALID.ACCOUNTS` and `LGN$BANNED.ACCOUNTS` per user; that register is gone
and there is no reason to inherit its shape. Worth recording that this session
earlier argued against reviving `$LOGINS` on the grounds that it was retired
deliberately — that argument survives, and the model arrived at needs no global
user register at all.

Attribution is SD-internal and does not depend on the service model, so it can
land with the password work. It records who authenticated, not who is at the
keyboard — accountability, not proof of identity.

**The audit log cannot be the existing one.** `LOGMSG` reaches `log_message()`
in `k_error.c`, which writes `<sysdir>/errlog` and, on reaching the configured
`ERRLOG` size, discards the oldest half of the file. Correct for a diagnostic
log, disqualifying for an audit trail. The trail needs its own append-only file
that rotates rather than truncates. Also note `CPROC` reassigns `logname` when
it drops to `sdsys` (around line 278); under this model nothing may overwrite
the login identity.

Separately, none of this makes accounts *private* from each other in stage 1.
Entering an account requires the user's own token to hold read and write on that
account's directory, and the OS cannot tell that token apart from the same
person browsing the directory in Explorer. Privacy between accounts waits for
§5.7.

### Still open

Recorded in §8: whether `sd -start` keeps an OS-level check now that
`IsAdmin()` has no other purpose, and whether the console entry point survives
the service model. Both shape stage 2.

---

## 13 Aug 2026 — Runtime bring-up started; IPC verified; session ended on credits

**Session ended mid-task.** Handing off to another account. Resume at
PROJECT_STATUS §3, "Runtime bring-up", and answer the question at the top of §8
before doing further identity work.

Built the runtime environment for the first time: `/etc/sd.conf` pointing at
`/usr/local/sdsys`, that tree populated from `sd64/sdsys` plus `bin` and
`terminfo`, and the account directories under `/home/sd`. None of this is in
the repository; it exists only on this machine.

**The IPC port is now largely de-risked.** `sd -start` was blocked behind the
administrator check, so rather than leave the shared memory work unexercised,
the create/attach/detach/unlink cycle was run standalone at 3 MB in the shape
`sysseg.c` uses: create, size, map, attach from a second mapping, verify size
and content, verify writes are visible through both mappings, create six
semaphores, verify exclusion while held and reacquisition after posting, unmap,
unlink, and verify a later attach gives ENOENT. Everything behaved. That was
the largest single unknown in the port.

**`IsAdmin()` was proved in the linked binary, in both directions.** `sd -start`
refused while `sdadmins` did not exist, and got past the check once built
against a group the token holds. On the way, `check_admin()` in `sd.c` turned
out to be a third privilege path that the earlier survey missed: it tested
`geteuid() != 0` and `in_group("admin")` rather than `IsAdmin()`. It now defers
to `IsAdmin()`, so there is one definition of an SD administrator.
`SD_ADMIN_GROUP` was made `#ifndef`-guarded so a site, or a probe build, can
override it.

**A correction worth recording.** When `sd -start` first printed "Command
requires administrator privileges", that was reported as the new `IsAdmin()`
working. It was not — it was `check_admin()`, which at that point did not call
`IsAdmin()` at all. The conclusion happened to be right in the end, but it was
asserted before being checked.

**The friction that matters for the design.** The `sdadmins` group was created
and `GITORLI\don` enrolled, and it still did not take effect: Windows fixes
group membership in the access token at logon, so the group resolved by name
while `getgroups` did not list it. Elevation does not help. That directly
contradicts the requirement that the installing user become an administrator
automatically, and is the strongest argument for the internal-flag alternative
raised the same day. Recorded as the open question at the top of PROJECT_STATUS
§8, unanswered.

**Bootstrap progress.** `gplbld/bbcmp.py` and `gplbld/pcode_bld.py` both run on
Windows unmodified — `gcat` now holds `$BBPROC`, `$BCOMP` and `!PATHTKN`, and
`PCODE.OUT` is populated. The sequence stops at `sd -i`, which reports "SD has
not been started" while `sd -start` refuses because `config.c` requires
`gcat/$CPROC`, which only the last bootstrap step produces. That ordering is
the immediate puzzle and is written up in §3. Given the isolation testing
above, suspect the bootstrap sequence rather than the IPC port.

---

## 13 Aug 2026 — PROJECT_STATUS rollover limit raised to 800 lines

**Commit:** documentation only.

The limit was ~400 and was raised to ~800 on the repository owner's
instruction. Earlier entries below refer to the old figure; they are left as
written, per the append-only rule, and this entry supersedes them on that
point.

400 proved too tight for the size of this port. The file crossed it twice in a
single day of work and both crossings forced a compression pass, which is
attention spent on housekeeping rather than on the port. The material was
genuinely needed — the privilege model, the BASIC layer survey and the identity
decision are all things a new session has to know before touching anything.

A note was added alongside the rule making the intent explicit: the limit is a
prompt to prune, never a reason to leave a finding out. Where something must
go, detail duplicated in HISTORY.md goes first, since nothing is lost by it.

An alternative was considered and not taken: splitting the §5 decisions into a
separate ARCHITECTURE file. Raising the limit keeps one document to read first,
which is the property that makes the handoff work across accounts.

---

## 13 Aug 2026 — Windows identity model decided; IsAdmin() reimplemented

**Commit:** see below. Code change is confined to `IsAdmin()` in `linuxlb.c`
and `SD_ADMIN_GROUP` in `sddefs.h`.

Context from the repository owner: on Linux, SD itself creates OS user
accounts, and administrator access is obtained by running `sudo sd`. Both
needed rethinking for Windows.

**What SD does today.** Every account operation shells out through `sudo`:
`useradd -m` in `CREATE_USER`, `passwd` in `SET_PASSWD`, `usermod -aG` in
`CREATEA` and `MODIFYA`, `groupadd` in `CREATEA`, `userdel` and `groupdel` in
`DELACC`, and `chmod g+s` in `CREATEA`. The installer creates the `sdusers`
group and the `sdsys` system user. SD's security model is therefore delegated
to the operating system: its accounts are real OS users and file access is
enforced by group ownership plus setgid directories.

**Three things established before deciding.**

`sudo sd` can survive as a command form: `sudo.exe` is present at
`C:\WINDOWS\system32\sudo.exe` on this machine, though disabled. But it does
not restore the mechanism — an elevated MSYS2 process still reports
`uid=197609`, because Cygwin derives the uid from the security identifier and
elevation does not change it. What elevation changes is group membership and
integrity level.

The original had a Windows answer and it should not be copied. `LOGIN` in the
external GPL.BP tree sets `lgn.id = 'Console'` and forces
`lgn.rec<LGN$ADMIN> = @true` for any console session, with a neighbouring
comment explaining that authentication was "alien" to Windows 95/98/ME. On a
modern system that would make anyone able to run `sd.exe` an SD administrator.

`chmod g+s` is the one command with no equivalent. Everything else maps to
`New-LocalUser`, `New-LocalGroup`, `Add-LocalGroupMember` and so on; the setgid
directory behaviour is inheritable ACEs, `icacls <dir> /grant "<g>:(OI)(CI)M"`.

**Decisions taken.** SD no longer creates or deletes OS accounts; it maps onto
Windows users and groups that already exist. This keeps OS-enforced file
security without SD holding standing administrative rights, and does not break
on a domain-joined machine. Administrator rights come from membership of the
`sdadmins` local group rather than from elevation, which separates SD
administration from Windows administration, needs no UAC prompt, and works for
a service.

**Implemented.** `IsAdmin()` was `getuid() == 0`. It now resolves
`SD_ADMIN_GROUP` with `getgrnam()` and tests the primary group and the
supplementary list, failing closed when the group does not exist. Verified
first that the mechanism works at all: `getgrnam()` resolves Windows local
groups on the MSYS2 runtime (`Users` 545, `Administrators` 544) and reports
membership accurately. The function body was then exercised as a standalone
copy against member, non-member, absent-group and primary-group cases, all four
as intended. The linked `sd.exe` path remains unexercised because SD does not
start.

**Deliberately not done, and why.** The BASIC side is untouched.
`sdsys/GPL.BP.OUT` contains only a README — there are no compiled objects in
the tree — and the installer compiles the BASIC with
`bin/sd -internal BASIC GPL.BP CPROC` after `gplbld/pcode_bld.py`. A BASIC edit
is therefore inert until SD runs and can compile it, so writing those changes
now would produce source that cannot be tested and does not match anything
executable. Recorded as a trap.

Note that the new `IsAdmin()` does **not** by itself unblock SDSYS or
`CATALOG GLOBAL`: those sites test `SYSTEM(27)` directly rather than
`K$ADMINISTRATOR`, so they still always deny. That is part of the pending
BASIC work, not an oversight.

---

## 13 Aug 2026 — Surveyed every BASIC to C linkage

**Commits:** documentation only; no code changed. Follows the GPL.BP survey
below, which covered platform detection only.

Interfaces enumerated and checked: `SYSTEM(n)` (19 keys in use), `OSPATH()`
(15 keys), `KERNEL()` (around 120 keys), `SDEXT`, `OS.EXECUTE` (10 files), and
the compiler chain.

**The privilege model is the serious finding, and it is not a detection
problem.** `IsAdmin()` in `linuxlb.c` is `return (getuid() == 0)`, and
`SYSTEM(27)` returns `getuid()` unchanged. `getuid()` under MSYS2 was measured
at 197609, and Windows has no uid 0 at all — administrator there is a token
privilege. So every privilege test answers the same way permanently, and
nothing errors:

- `CPROC` — `new.account = "SDSYS" and system(27) > 0` is always true, so
  **SDSYS access is always denied**
- `CATALOG` — `system(27) # 0` guarding `CATALOG GLOBAL` is always true, so
  **global cataloguing is always denied**, which reaches into the compile
  workflow and not just administration
- `CPROC` — the `system(27) = 0` "entered as root?" branch never runs, so the
  drop to `sdsys` via `EUID_SET` never happens
- `K$ADMINISTRATOR` in `op_kernel.c` consults `IsAdmin()` and so is never
  granted implicitly

`EUID_SET`/`EUID_RESTORE` reach `sdext_eguid.c` through `SDEXT` and call
`getpwnam`, `setegid` and `seteuid`. Native Windows has no equivalent;
impersonation is `LogonUser` plus `ImpersonateLoggedOnUser`.

The useful part is that this concentrates: everything routes through
`IsAdmin()` or `SYSTEM(27)`, so one decision about what "administrator" means
on Windows and one function body covers it. Recorded as next step 4.

**`VALID_OS_NAME` undoes a documented Windows fix.** It rejects spaces in user
names, and both `ADMUSER` and `CREATEU` in the external tree carry the line
"15 Apr 05 2.1-12 Allow spaces in user names for Windows compatibility". A
2005 change made deliberately for Windows was removed by the cleaning cycles
twenty-one years later. Called from `CREATEA` and `APISRVR`. This is the second
instance of that pattern after `VALID_OS_PATH`, which is enough to treat it as
a class rather than a coincidence.

**`PLATFORM_NAME` reaches the compiler.** It is `"Linux"` in `sddefs.h`,
returned by `SYSTEM(1010)`, and `BCOMP` does
`add 'SD.':upcase(system(1010)) to defined.tokens` — so the BASIC compiler
defines the token `SD.LINUX`. The external tree does the same with `QM.`.
Nothing tests the token in either tree, so it is latent rather than broken, but
any BASIC source asking `SYSTEM(1010)` is told "Linux".

Surveyed but not yet examined in detail: the 15 `OSPATH` keys in `op_dio2.c`
(all path semantics, including `OS$FULLPATH`, documented as "Return full DOS
file name"), and the platform sensitive `KERNEL` keys (`K$SETUID`, `K$SETGID`,
`K$USERS.UID`, `K$IN.GROUP`, `K$TTY`, `K$RUNEXE`, `K$INIPATH`). `OS_CHOWN` is
an SD addition called from `CATALOG` with no Windows meaning.

Everything else checked is platform neutral: terminal type, endianness,
version, times, queue and select state, and the compiler chain apart from `@ds`
and the token above.

PROJECT_STATUS passed 400 lines during this update and was rolled over per its
own rule: §5.1 and §5.2 were merged and shortened, since the full reasoning
already lives in the entry below, and §5 was renumbered.

---

## 13 Aug 2026 — Surveyed the BASIC layer (GPL.BP) for platform code

**Commits:** documentation only; no code changed.

Context supplied by the repository owner: `sdb64` is the active project, and
this tree is an experimental variant that has been through five major AI
cleaning and validation cycles — which is why the code reads more cleanly than
its age suggests. The original ScarletDME BASIC source was made available at
`C:\Users\dmont\Projects\GPL.BP` for comparison, on the basis that the C code
and the BASIC code work together for things like compilation.

**The BASIC layer has a platform switch that nothing had looked at.** Two
SYSTEM keys are the whole bridge between the C code and the BASIC source:
`SYSTEM(91)` ("is this Windows") is hardcoded to zero in `op_sys.c`, and
`SYSTEM(1006)` ("Windows NT style") returns `is_nt`, which `kernel.h` declares
`init(FALSE)` and which is never assigned anywhere. Both answer "not Windows",
so every Windows path in the BASIC layer is dead code. `is_nt` is dormant in
exactly the way `CASE_INSENSITIVE_FILE_SYSTEM` is.

**Unlike the C reference tree, the external GPL.BP is a real asset.** It holds
Windows logic in 21 files against 6 here, and every file present in both trees
lost all of it: `LOGIN` went from 16 references to none, `CONFIG` 5 to none,
`CPROC` 5 to none, `CREATEA` 4 to none, `PARSER` 3 to none. Details of what
each did are in PROJECT_STATUS §5.5. This is the opposite of the finding for
the C tree, where the Windows code was genuinely gone and only comments
remained.

**`@ds` turned out to be load-bearing for compilation**, which is the
connection the owner pointed at. `BCOMP` opens `@sdsys:@ds:'bin'` and builds
source paths with it; `BASIC` builds its source and output paths the same way.
It is SYSCOM slot 57, fed from `dir.separator`, which the original set as
`if windows then '\' else '/'` and which `CPROC` here hardcodes to `'/'`.
Correct on the MSYS2 runtime, and a live question for stage 2.

**One Windows blocker was introduced by the cleaning cycles, not inherited.**
`VALID_OS_PATH` does not exist in the external tree; it is dated 2026/06/10 in
this one. Its permitted character set omits the backslash and it rejects spaces
as shell metacharacters, so it rejects `C:\SD\accounts` and everything under
`C:\Program Files`. It guards `CREATEA` (account creation) and `PY_RUNFILE`.
Worth recording as a caution: the cleaning cycles can introduce Windows
problems as readily as they remove clutter, so "the original did not have this"
is not a safe assumption in either direction.

Smaller Linux remnants: `/tmp/api_srvr.log` and `/tmp/bbproc.log` in `APISRVR`
and `BBPROC`, and `sudo chmod g+s` in `CREATEA`. `OS_CHOWN` is implemented in
`op_dio2.c` and called from `CATALOG` via `ospath()`; it has no meaning on
Windows. The BASIC compiler itself (`BCOMP`, `ACOMP`) carries no platform
branches in either tree beyond the `@ds` use above.

Nothing was changed. The ordering constraint is recorded in PROJECT_STATUS §7:
restore the BASIC branches first, flip the SYSTEM keys second, because doing it
the other way enables paths that are no longer there.

---

## 13 Aug 2026 — Client library replaced with the vendored winsdclilib port

**Commit:** `202b965`

Vendored `github.com/dmontaine/winsdclilib` at `b6624565cacb365d0a2788545495a7fa3ba3f743`
(5 Aug 2026) into `gplsrc/sdclilib/`, replacing `gplsrc/sdclilib.c`.

**Why it was safe.** `sdclilib` is not listed in `gpl.src`, so it was never
linked into the server — it only ever produced the shared library. Replacing it
could not destabilise the server work.

**Why it is better.** No longer the partial Visual Studio port described by the
stale snapshot that used to sit in `examples/windows.c/winsdclilib/`. It
combines the complete Linux client behaviour with a Winsock transport and
carries fixes the old code lacks: an index-buffer overflow, `realloc` ordering
on a failed grow, short sends, malformed response lengths, and abandoning a
connection whose stream can no longer be trusted. Verified by building rather
than trusting the README — zero warnings under `-Wall -Wextra -Wpedantic`, both
bundled test suites pass.

**Why its own directory.** Its `sdclient.h`, `err.h` and `revstamp.h` are
different files from the ones in `gplsrc`. `revstamp.h` feeds
`MAJOR_REV`/`MINOR_REV`/`BUILD` into `SYSSEG_REVSTAMP` in `sysseg.c`, which
stamps the shared memory segment. Flattening the layout would have displaced
the server's copy.

**`SDConnectLocal` restored.** Absent upstream because that project targets a
Windows client talking to a *remote Linux* server, where a local connection has
no meaning — the user identified this, and it is correct. It matters again now
the server runs on Windows, and the Python wrapper binds it. Modelled on
`gplsrc/sdclient.c:666`: named pipe, `CreateProcess` of `sd.exe -Q -C <pipe>`,
`ConnectNamedPipe`, then `SrvrLocalLogin` and `SrvrAccount`. Two deliberate
improvements on that original — `ERROR_PIPE_CONNECTED` treated as success
rather than failure, and the process handle closed as well as the thread handle
(the original leaked it). Supporting it needed `sysdir()` and a transport layer
(`transport_recv`/`transport_send`/`transport_live`/`transport_error`) so
packet I/O works over socket or pipe. Upstream's error handling and connection
abandonment were left untouched; only byte moving is dispatched.

**Also fixed.** `sdclilib` and `terminfo` both needed `.PHONY`: neither names a
file and `VPATH` covers `gplsrc`, so make found the directories and considered
the targets satisfied. This is why an earlier session saw `terminfo` report "is
up to date" for something it had never built.

**Removed.** The stale `examples/windows.c/winsdclilib/` snapshot, and the
`sdclilib.so`/`libsdcli.so` pair built from the old client.

**Still open.** `SDConnectLocal` has never run. It needs a live server and an
`sd.ini`.

---

## 13 Aug 2026 — Correction: the `O_BINARY` override was not corrupting data

**Commit:** `202b965`

An earlier claim in this session's reporting — that hardcoding `O_BINARY` to
zero meant SD was writing binary files in text mode and corrupting them — was
**wrong**, and was stated with more confidence than the evidence supported.

On finding the same override a second time in `sdtic.c` (which does not include
`sddefs.h` and so carries its own copy), the prediction was that the 99
generated terminfo files were corrupted. Tested by regenerating
them with and without the correction: **byte identical**. The MSYS2 runtime
opens files in binary mode by default, so discarding the flag changes nothing
there.

The `#ifndef` guards in `sddefs.h` and `sdtic.c` are kept because they are
correct and will matter for stage 2, where the native Windows CRT defaults to
text mode. Both source comments were rewritten to say this plainly instead of
implying an active bug.

**Lesson worth keeping:** the compiler warning was real and worth chasing; the
conclusion drawn from it was not verified before being asserted. Regenerating
the artifact and comparing bytes took under a minute.

---

## 13 Aug 2026 — Removed superseded Linux artifacts

**Commit:** `3b4600e`

Deleted the six Linux ELF binaries in `bin/` (superseded by the `.exe` builds),
and `pcode_bld.log`, `pass1`, `pass2` — pcode build scratch. `pass1` and
`pass2` are byte identical and are written by the `pass1()`/`pass2()` stages of
`gplbld/bbcmp.py`.

Untracked but kept on disk: `terminfo/`, all 99 files of which are generated by
the `terminfo` make target. Verified by deleting the directory and rebuilding
before committing to the change.

Tracked files went from 3,446 to 3,255.

**Kept deliberately**, despite having no function on Windows: `usr/lib/systemd/`
and `etc/xinetd.d/`. They document the service topology a Windows service must
reproduce. Also kept: `installsdai.sh` and `deletesdai.sh`, which are the
targets of the port rather than obsolete output.

---

## 13 Aug 2026 — First native Windows build

**Commit:** `143c959`

All six binaries compile, link and run as native PE32+ executables for the
first time.

**The central problem.** MSYS2 ships the genuine Cygwin `sys/shm.h`, so SD's
System V IPC code compiled and linked without a warning and would have failed
at runtime with ENOSYS. Found by compiling and *running* probe programs rather
than checking for headers — which is the only reason it surfaced in minutes
instead of during a confusing debugging session later. MSYS2 has no
`cygserver`, so there is no way to enable System V IPC.

POSIX named shared memory and named semaphores do work, so:

- `sysseg.c` — `shmget`/`shmat`/`shmdt` → `shm_open`/`ftruncate`/`mmap`/`munmap`
- `sdsem.c` — `semget`/`semop`/`semctl` → `sem_open`/`sem_trywait`/`sem_post`
- `sdidx.c`, `sdlnxd.c` — their own copies of the attach code

Two places needed more than substitution: `munmap` must be told the mapping
length that `shmdt` derived from the address, and `stop_sd()` waited on the
System V attach count, which POSIX shared memory does not expose. It now polls
the user table with `kill(pid, 0)`, which also catches a process that died
without clearing its own entry.

**Other platform fixes.** `O_ASYNC` has no equivalent — verified first that
`keyin()` and `keyboard_pending()` test stdin with `sdpoll()` independently, so
input still works without SIGIO. `environ` was remapped to glibc's internal
`__environ`. `linux/limits.h` → `limits.h` in four files. `sdclient.c:127` read
`SDnclude <io.h>`, corrupted by the `qm`→`sd` rename; the upstream GPL source
has a clean `#include`.

**Build.** Libraries had to move after the objects that reference them, since
the PE/COFF linker resolves strictly left to right; ELF had masked this with
`-Wl,--no-as-needed`. Dropped `-DLINUX` (never tested for anywhere in the
source), `-fPIE` (the default here) and `-soname` (no PE equivalent — replaced
by an import library). libsodium is not packaged for the MSYS2 runtime and is
built from source into `/usr/local`.

**Two premises that turned out to be wrong**, both worth recording:

- *"gcc is on this computer under C:\msys64."* MSYS2 was installed but
  contained no toolchain at all — `mingw64/bin` was empty and there was no
  `gcc.exe` or `make.exe` anywhere. It had never been run; pacman performed
  first-time setup on first invocation. Everything in PROJECT_STATUS §2 was
  installed during this work.
- *"Many files in gplsrc still contain Windows code."* They do not. Of ten
  files matching Windows API idioms, nine matched only on comments or on
  `BOOL`/`SOCKET`, which are the project's own typedefs. Only `qmclient.c`
  holds real Windows code, and it includes `windows.h` unconditionally — it was
  always the Windows client, not stripped server code. The reference tree's
  value is archaeology: in `op_kernel.c`, both there and in this repository, a
  `/* Construct command for CreateProcess */` comment sits directly above a
  `fork()` call in `op_phantom()`, marking where Windows code used to be.

  The reference tree is a separate checkout at `C:\Users\dmont\Projects\gplsrc`
  and is not part of this repository.

**The finding that most de-risked the port:** all five `fork()` call sites are
fork+exec, none rely on copy-on-write semantics. The usual "cannot port this to
Windows because of `fork`" obstacle does not apply.

---

## 13 Aug 2026 — Repository created

**Commit:** `1285c13`

Initial import of the working tree and push to
`github.com/dmontaine/sdb_ai_windows`.

`.gitattributes` sets `* -text`: the tree is a Linux-targeted package stored on
a Windows host, and a clone on a machine with `core.autocrlf=true` would inject
CRLF into the shell installers. The executable bit was restored on
`installsdai.sh` and `deletesdai.sh`, which Windows had dropped
(`core.filemode=false` staged everything as `100644`). The ELF binaries in
`bin/` were deliberately left non-executable, since `installsdai.sh:514` does
`chmod -R 755` on the installed directory itself.

Git identity was set repo-locally rather than globally, to avoid changing
machine-wide state.
