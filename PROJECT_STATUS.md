# PROJECT STATUS

Living handoff document for the SD Windows port. This project moves between
sessions, machines and accounts; anything not written here is lost. Read this
file first. Read [HISTORY.md](HISTORY.md) only if you need the record of how
something came to be the way it is.

**Last updated:** 14 Aug 2026, fourth session of the day, at commit `9b44d4b`
plus the commit that carries this line. **This session had no elevated
window** — the permission layer refused to launch one — so everything below is
what could be done and proven without one, and **step 0 is unchanged and still
first**. What landed:

- **`AllowGroups` is implemented** (§5.6.2's second layer, previously "not
  implemented at all"): `gplbld/allow-ssh-groups.ps1`, offered by the installer
  as a subtask of the OpenSSH one, and taken back out again on uninstall.
- **Its file editing is verified, its effect is not.** `verify-allowgroups.ps1`
  is tracked, needs no elevation and no `sshd`, and passes 20 checks — but
  nothing has yet pointed the script at a live `sshd_config`, and **whether the
  group patterns match the right people is the lockout risk** and is unknown.
  §4 Unverified spells out the three parts of that.
- **The installer's closing dialog leads with `CREATE.ACCOUNT`** (§7 step 1b),
  instead of telling the user to run `net localgroup sdusers <name> /add` for a
  Windows account the verb would have created for them.
- **Two traps** in §6: the Inno brace-comment trap caught a second time, and
  the general one behind it — an installer edit to a file SD does not own has to
  be an *exact* inverse, which a blank line quietly broke.

The previous session's summary, kept because it is what the state above rests
on. It had one subject: the ssh-only model (§5.6.2), left built and entirely
unproven by the session before it.

- **THE SSH-ONLY MODEL IS PROVEN** (§4, §5.6.2), by a control-and-treatment
  experiment on a real Windows account. The console closes, ssh stays open,
  and the account logs in and runs a shell. The one part still unobserved is
  RDP refusal, which has no way to be automated.
- **The test is a tracked script, `gplbld/verify-sshonly.ps1`**, because §7
  step 2 has to repeat it on the second machine.
- **`deny-logon.ps1` has now run against a real group**, not a throwaway.
- Three traps found and recorded in §6, all of which produced **false
  failures** — a passing test that reported FAILED, and a diagnostic that
  reported total authentication failure for every account on the machine.
- **A new SD account cannot use key authentication until somebody has logged
  in with a password once** (§4, §6). This is a property of Windows, it
  applies to accounts `CREATE.ACCOUNT` makes, and it was found by accident.
- **`BUILTIN\Users` membership is not needed** — asked because `CREATE_USER`
  never adds it, answered by measuring rather than by adding it defensively.

- **RDP refusal cannot be tested from one machine** — measured, three attempts,
  after two wrong inferences about it that are corrected in HISTORY.md. It
  moves to the second machine.
- **`gplbld/verify-createaccount.ps1` is written but HAS NOT RUN.** It needs an
  elevated window. Everything in `CREATE.ACCOUNT` up to the elevation gate is
  confirmed (§4); the privileged half is untested and is step 0.
- **Scripting SD from PowerShell has two traps** (§6), both of which produce a
  failure that looks like SD's fault and is not.

**Where it stopped:** §5.6.2 is verified except RDP. The `CREATE.ACCOUNT` test
is written and **still unrun** — that is step 0, and it is one command in an
elevated window. `AllowGroups` is now written, and unrun in the same way and
for the same reason.

**Both of the things at the top of the list now need the same thing: a window
somebody has elevated.** Neither is hard and neither is long. If you are
reading this with an elevated prompt available, do step 0 and step 0a before
anything else, because everything written since 14 Aug 2026's third session is
waiting on them.

**STATE OF THIS MACHINE, 14 Aug 2026 - READ FIRST.** There is a **working SD
install** on it, from the fixed installer:

| Thing | State |
|---|---|
| **THE WHOLE INSTALL IS STALE** | **Built 08:32/08:34 on 14 Aug 2026 and never refreshed. It predates commit `2fd0aff`, which is the commit that made `CREATE.ACCOUNT` work.** Anything tested against it is testing 08:32's code — that is the trap in §6, and it is what made step 0 fail. A current installer is waiting at `C:\Users\dmont\sdout\`; installing it needs elevation and means removing the data tree first, since an upgrade will not replace it |
| `C:\Program Files\SD` | 15 files, correct, binaries in `usr\bin` including `sdwind.exe`. `sd.exe` is 08:32:44 and carries the **pre-fix `op_dio2.c`** |
| `C:\ProgramData\SD\sdsys` | **3,264 files - a working database**, `COUNT VOC` reports 431. The compiled `gcat/$CREATEA` is 08:34 and has **no ssh-only branch**; `MESSAGES/10032`–`10035` are absent |
| The daemon | **runs**, as `C:\Program Files\SD\usr\bin\sdwind.exe`, and `sd -stop` takes it down |
| SDSYS password | **not set.** `LOGIN` warns and admits an administrator, which is the correct state for an install nobody has finished |
| `sdusers` group | exists, with `GITORLI\don` in it |
| `sdadmins` group | exists, **created by hand on 13 Aug, not by the installer** — see below |
| System PATH and the Settings > Apps entry | both present |
| `C:\ProgramData\SD` ACL | locked to sdusers/Administrators/SYSTEM. An unelevated session **cannot read inside it** until `don` signs out and back in; `Test-Path` on the directory itself still says True, so look at the contents |
| MSYS2 dev tree at `/usr/local/sdsys` | still reachable with `SD_CONFIG=/etc/sd.conf`. Its `bin/` was refreshed with the `sdwind` build on 14 Aug 2026 and the stale `sdlnxd.exe` removed; `pcode`/`pcode.old` are still beside them, since the dev tree keeps the old unsplit layout |
| **The machine was rebooted** on 14 Aug 2026 | `don`'s token now carries `sdusers`, so **an ordinary unelevated session runs SD** — verified, §4. The sign-out trap in §6 is cleared *on this machine only*; it applies afresh to every new user added to the group |
| **OpenSSH Server** | **installed, `sshd` Running / Automatic**, listening on 22, firewall rule enabled, `C:\ProgramData\ssh\sshd_config` created with defaults. So the ssh-only model (§5.6.2) can now be tested **here**, which was not true earlier in the day |
| `sdsshonly` group | **exists now**, created 14 Aug 2026 by `verify-sshonly.ps1`, with both deny rights applied to it. So `CREATE.ACCOUNT` for a non-administrator will work here. It is left in place deliberately — it is what the installer would have created |
| Test accounts | **none. Cleaned up 14 Aug 2026** — `sdsshprobe` and its transcript are gone, confirmed. `sdsshonly` is empty and that is correct; the group is the installer's, the membership is not |
| SD | **running as this session ended**, started 14 Aug 2026 from `C:\Program Files\SD\usr\bin\sd.exe` and left up. `sd -stop` takes it down |
| SD at boot | **does not start.** There is no service (§5.7), so `sd -start` must be typed after every restart |

Nothing needs cleaning off before the next piece of work. To start over anyway,
elevated: `C:\Program Files\SD\unins000.exe /VERYSILENT`, delete
`C:\Program Files\SD` and `C:\ProgramData\SD`, then `Remove-LocalGroup sdusers`
— but leave `sdadmins` alone, for the reason in §8.

**THE STAGED TREE AND THE INSTALLER WERE BOTH REBUILT AT THE END OF
14 Aug 2026's FOURTH SESSION, AND THEY ARE CURRENT.** This is the fix for the
staleness that made step 0 fail; all that is left is to install it, which needs
elevation.

| | |
|---|---|
| `C:\Users\dmont\stagetest` | rebuilt 16:15, `make sd` + `stage.py --force --bootstrap`, **3,285 files**, 10.4 MB, bootstrap clean, four MSYS2 DLLs |
| `C:\Users\dmont\sdout\sd-setup-1.0-2.exe` | rebuilt 16:17 from the tracked `sd.iss`, ISCC exit 0, 4,771,110 bytes (was 4,761,838 at 08:35) |

Checked in the rebuilt stage rather than assumed: `MESSAGES/10032`–`10035` all
present; `allow-ssh-groups.ps1`, `deny-logon.ps1` and `install-ssh.ps1` all in
`ProgramFiles`; and the compiled `gcat/$CREATEA` **contains the string
`sdsshonly`**, where the installed one from 08:34 does not. That last one is
the ssh-only branch shown present in pcode rather than inferred from a source
file.

**Not verified: that this installer installs.** It compiled; nobody has run it.
Neither artefact survives a rebuild of the machine, and both are reproduced by
the commands at the top of `gplbld/sd.iss`. Evidence from the earlier
first-install run is in `C:\Users\dmont\`: `sdverify-transcript.txt` (the
counts) and `sdfirstinstall.innolog` (16,507 lines, against 145 for the broken
run).

**Where to start next.**

0. **RUN `gplbld/verify-createaccount.ps1` FROM AN ELEVATED WINDOW.** This is
   the first thing to do and it is one command. `CREATE.ACCOUNT`'s ssh-only
   branch has still never executed — the group did not exist when the verb was
   last run, and it does now. Everything up to the elevation gate is already
   confirmed (§4 Verified), so this is the privileged half and nothing else:

   ```powershell
   powershell -File C:\Users\dmont\Projects\sdb_ai_windows\sdb_ai\sd64\gplbld\verify-createaccount.ps1
   ```

   **The path is absolute on purpose.** An elevated window opens in
   `C:\WINDOWS\system32`, never in the repository, so a relative path fails
   with "the argument ... does not exist" — which reads like a missing script
   rather than a wrong working directory. Every elevated command in this file
   is written out in full for that reason. Adjust the prefix if the repository
   is somewhere else.

   A pass closes the chain end to end — SD creates the account, SD restricts
   it, and the restriction is then shown to hold by the same three
   measurements that proved §5.6.2. Read §4 Unverified for what its cleanup
   deliberately does *not* remove.

   **IT RAN ON 14 Aug 2026, FOURTH SESSION, AND IT FAILED — BUT NOT BECAUSE
   `CREATE.ACCOUNT` IS BROKEN. THE INSTALLED SYSTEM ON THIS MACHINE PREDATES
   THE COMMIT THAT MADE `CREATE.ACCOUNT` WORK.** Do not chase the failure; fix
   the install and run it again. The evidence is decisive:

   | | |
   |---|---|
   | `C:\Program Files\SD\usr\bin\sd.exe` built | 14 Aug 2026 **08:32:44** |
   | commit `2fd0aff`, "Make CREATE.ACCOUNT work" | 14 Aug 2026 **09:50:56** |
   | `MESSAGES/10032`–`10035` in the installed tree | **absent**, all four |

   So the installed `sd.exe` carries the **pre-fix `op_dio2.c`**, whose
   `OS_PATHNAME` case split on `/` alone and therefore rejected every native
   Windows path — and the installed `CREATEA` is the pre-fix one, with no
   `ADMINISTRATOR` keyword and **no ssh-only branch at all**. Six of the
   failures are that one fact:

   - `Invalid account pathname` is the exact symptom the comment at
     `op_dio2.c:650` was written to describe, down to it happening *after* the
     Windows user was created.
   - `message 10034 (ssh only) shown: no` — the message does not exist in the
     installed tree and neither does the code that prints it.
   - no `sdusers`, no `sdu_` group, no account directory, no `ACCOUNTS` record:
     `CREATEA` `stop`s at the pathname check before reaching any of them.

   **What the run did establish, and it is worth having:** `CREATE_USER`
   reached the OS from an elevated session and **made a real Windows account**
   — `the Windows account exists: PASS`. It was left disabled and without a
   password, which is correct rather than a fault: `SET_PASSWD` line 120 runs
   `Enable-LocalUser` *inside* the password script, so an account whose
   password was never set stays inert. `LogonUser` answering **1326** for both
   logon types is consistent with exactly that and is not evidence about the
   deny rights.

   Cleanup worked and **the machine is clean** — no `sdacct1`, no `sdu_sdacct1`,
   `sdsshonly` empty, no account directory, no `C:\Users\sdacct1`.

   **SECOND RUN, AGAINST THE REBUILT INSTALL: THE SSH-ONLY BRANCH EXECUTED FOR
   THE FIRST TIME.** 9 of 13 structural checks passed, including every one that
   step 0 existed to answer — `sdacct1 may sign in over ssh only` was printed
   from message 10034, and membership of `sdusers`, `sdu_sdacct1` and
   `sdsshonly` was confirmed, with `Administrators` correctly absent. The
   account directory, `VOC`, `$HOLD`, `BP`, the private catalogue and the
   `ACCOUNTS` record were all made. **`CREATEA` line 400 has now run.**

   Of the four remaining failures, **two were the test's own fault** and are
   fixed: it asserted `$SAVEDLISTS` where `CREATEA` creates `$SVLISTS` (the
   message carries the VOC name, the directory carries the DH file name), and
   the file count expected 16 program files where a real install has 18 —
   `unins000.exe` and `unins000.dat` are the installer's, not the stage's.

   **The other two are one cause, now measured**: the PowerShell pipeline's
   CRLF phantom line, first trap in §6. `SET_PASSWD`'s first `input` ate a
   phantom, so the password was never set, so the account stayed disabled and
   all three logon measurements failed for want of a password. `Invoke-SD` now
   sends one string with LF separators. **This was the thing the previous entry
   declined to conclude from a lossy echo; it was then established by
   experiment rather than by reading the transcript harder.**

   **So step 0 has a prerequisite, and the unelevated half of it is DONE.**
   `make sd` and `stage.py --force --bootstrap` were re-run at 16:15 and the
   installer rebuilt at 16:17 — see the table above the numbered steps, which
   records what was checked in the result. **What is left is one elevated
   sequence, and it must remove the data tree**, because the installer will not
   replace an `sdsys` that already exists (§5.9) — which is precisely how this
   install came to be four commits behind its own repository:

   ```powershell
   & "C:\Program Files\SD\usr\bin\sd.exe" -stop
   Get-Process sdwind -ErrorAction SilentlyContinue | Stop-Process -Force
   & "C:\Program Files\SD\unins000.exe" /VERYSILENT
   Remove-Item -Recurse -Force "C:\Program Files\SD", "C:\ProgramData\SD"
   & "C:\Users\dmont\sdout\sd-setup-1.0-2.exe"
   ```

   The `Stop-Process` line is not belt and braces — it is the §6 trap two
   entries down, and this daemon really was started by an elevated session.
   Leave `sdusers`, `sdadmins` and `sdsshonly` alone; the installer recreates
   the two it owns, and §8 explains `sdadmins`.

   **DONE 14 Aug 2026, fourth session.** The install was refreshed and is
   current: 18 files in `C:\Program Files\SD`, 3,268 under `sdsys`,
   `MESSAGES/10034` present. No sign-out was needed, because `sdusers` was left
   alone and the token already carried it.

   **What remains is to run the test once more**, with the CRLF fix in place
   and **a fresh account name**, because the previous run left the SD side of
   `sdacct1` behind deliberately and `CREATE.ACCOUNT` will refuse the name:

   ```powershell
   powershell -File C:\Users\dmont\Projects\sdb_ai_windows\sdb_ai\sd64\gplbld\verify-createaccount.ps1 -Account sdacct2
   ```

   The script now checks for that leftover up front and says this, rather than
   letting SD refuse the name after it has already made a Windows account.

0a. **THEN APPLY `AllowGroups` ONCE, IN THE SAME ELEVATED WINDOW**, and keep
   that window open while you do it. Written 14 Aug 2026 and never pointed at
   a real `sshd_config`:

   ```powershell
   powershell -File C:\Users\dmont\Projects\sdb_ai_windows\sdb_ai\sd64\gplbld\allow-ssh-groups.ps1 -Installed
   ```

   **Read this before running it.** It restricts who may ssh into this
   machine. It is safe to try *here* because this machine's administrator has
   console access and does not depend on ssh — that is not true everywhere.

   - Exit **0** wrote the block and restarted `sshd`. **Immediately open a
     second terminal and ssh in as an account in `sdusers`**, before closing
     anything. That is the measurement §4 Unverified is asking for.
   - Exit **2** refused, and says why. On this machine the likely reason is
     that `sshd_config` already exists but restricts nobody, which is *not* a
     refusal case — so exit 2 here more likely means the `-Installed` switch
     was omitted.
   - Anything else failed and put the original back.

   To undo: the same command with `-Remove` instead of `-Installed`, or copy
   `C:\ProgramData\ssh\sshd_config.before-sd` back over it.

   The file editing itself is already proven and does not need re-testing —
   `verify-allowgroups.ps1` beside it passes 20 checks with no elevation, and
   can be run anywhere, from any directory, to confirm nothing has regressed.

1. **Finish the loose ends the ssh-only work left.** The model itself is
   proven (§4); what is below is small and should not be left to drift.

   a. **RDP refusal has moved to step 2, and it is measured rather than
      assumed this time.** Three attempts on 14 Aug 2026 — `localhost` and the
      machine's own LAN address, with two different accounts — all answered
      `0x708` before reaching a credential prompt. **Nothing further to try
      here**; the table is in §4 Unverified. It needs a separate client
      machine.

   b. **Done 14 Aug 2026 — the probe account and its transcript are deleted**,
      confirmed. `sdsshonly` was deliberately left, because it is what the
      installer creates and `CREATE.ACCOUNT` needs it.

   d. **Make `sd -stop` tell the truth about `sdwind`** — found 14 Aug 2026,
      fourth session, the trap is in §6 and this is the fix for it.
      `sysseg.c` line 503 discards `kill()`'s return value, so an unelevated
      `sd -stop` against a daemon an elevated session started gets `EPERM`,
      leaves it running, and prints "SD (64 Bit) has been shut down" anyway.
      The liveness poll underneath walks the user table only and never waits
      for the daemon.

      Small and self-contained: check the return, and if it is `EPERM` say so
      — "sdwind (pid n) could not be stopped: it was started by a more
      privileged session" is the whole of what the user needs. Do **not** make
      it fatal; the segment teardown that follows is still correct and still
      wanted.

      It needs `make sd` and a re-run of the start/stop cycle at both
      elevations, so it is a build session rather than a documentation one.

   c. **`AllowGroups` is written — done 14 Aug 2026, fourth session** — and is
      §7 step 0a above until somebody has watched it work. What exists:
      `gplbld/allow-ssh-groups.ps1`, an `installssh\allowgroups` subtask in
      `sd.iss` that is unreachable unless SD is installing OpenSSH itself,
      removal on uninstall, and `gplbld/verify-allowgroups.ps1`.

      Both cautions from §5.6.2 are honoured, and how matters if you change
      any of it: the administrators group is resolved from **`S-1-5-32-544`**
      rather than written as a name, because the name is localised; and the
      offer is a **child task** of the OpenSSH one, which is what makes it
      structurally impossible to reach on a machine whose ssh server SD did
      not install.

   `CREATE.ACCOUNT` with `sdsshonly` present is **step 0 above**, which is
   where it belongs now that the test for it is written.

1. **Finish the account model now that administration is the OS's** (§5.6.1,
   decided 14 Aug 2026). `IsAdmin()` is done and verified; what is left is the
   account-creation half.

   a. **DONE 14 Aug 2026 and verified — `CREATE.ACCOUNT` works.** The
      `ADMINISTRATOR` keyword is in, the `config('CREATUSR')` gate is gone, and
      the verb has now been run for the first time. See §4.

   b. **DONE 14 Aug 2026, fourth session — the installer's closing dialog
      leads with the verb.** It now gives `sd -start`, `sd -ASDSYS`,
      `CREATE.ACCOUNT USER <name>`, says that an elevated window is needed and
      why, says that accounts made this way are ssh-only, and gives the
      `ADMINISTRATOR` keyword. `net localgroup sdusers <name> /add` stays as
      what it always was — the way to give SD to somebody who already has a
      Windows account.

      **Nobody has seen it on screen** (§4 Unverified). The script compiles;
      that is a different claim.

   c. **Decide what `DELETE.ACCOUNT` should do**, which is now the asymmetry.
      `DELACC` still consults `config('CREATUSR')` before offering to remove
      the OS user (line 211), and that gate no longer exists on the creating
      side. It also has not been run. Removing an account should probably
      remove the Windows user it created, but that is a destructive default
      and wants deciding rather than assuming.

   d. **`CREATUSR` is now dead config.** Nothing consults it on the create
      side; `config.c` still parses it, `op_config.c` still answers it and
      `CONFIG` still prints it. Remove all three once `DELACC` stops using it.

      **Correction, 14 Aug 2026:** this file previously said `CREATUSR` "is not
      in the shipped `sd.conf` and defaults off", and gave that as a blocker.
      **That was wrong** — `config.c` line 98 sets `pcfg.create_user = 1`, so
      it defaulted **on** and never blocked anything. The real blocker was the
      pathname validator in §6.

2. **Install on a genuinely clean machine.** Still the test that matters, and
   still not done: this machine has a development tree, so an accidental
   dependency could survive. **The repository owner is building a second
   machine for this** (14 Aug 2026), which is what it has been waiting for.

   **The `sdadmins` gap that would have made this fail is closed** — §5.6.1
   means `IsAdmin()` now tests Windows `Administrators`, which always exists,
   so there is no group for the installer to forget to create and `sd -start`
   should work on a fresh machine. That was the predicted failure and it is
   gone.

   **Rebuild the installer first — the one at `C:\Users\dmont\sdout\` is
   stale.** It was built at 08:35 on 14 Aug and predates everything after it:
   the `IsAdmin()` change, the OpenSSH brace fix, the removal of the SDSYS
   password step, `sdsshonly` and `deny-logon.ps1`, the `CREATE.ACCOUNT` work,
   and — added 14 Aug 2026, fourth session — the reworded closing dialog and
   the whole of `AllowGroups`. Full sequence at the top of `gplbld/sd.iss`; the
   `--bootstrap` stage is the slow part.

   **`stage.py` must be re-run, not just `ISCC`.** `allow-ssh-groups.ps1` is a
   new file that `stage.py` copies into `ProgramFiles`, so compiling against
   the existing `C:\Users\dmont\stagetest` produces an installer whose
   `AllowGroups` step cannot find its own script. `stage.py` raises rather than
   warning if the source is missing, so a full rebuild cannot get this wrong —
   only a shortcut can.

   What to check there, in order: **count the files** (3,264 under
   `sdsys`, not 16 — do not trust Setup's exit code); `sd -start` and
   `COUNT VOC` reporting 431; that `sdwind` is running; and then the whole
   ssh-only model in §4 Unverified, which is the reason a second machine is
   worth having — it is the only place `sshd` can be exercised without the
   half-applied capability this machine is carrying.

3. **Run the account commands once.** They compile and have never executed
   (§4). Needs an elevated session; the `sdusers` group now exists, so that
   half of the blocker is gone. Until then this is code nobody has seen work.

4. **Waiting on the repository owner:** `sdadmins` above; how the API should be
   exposed (§8); and whether the `sdusers` login gate comes back, which the
   owner wants "if it is possible" and now is — but which pulls against §5.6
   (see the correction there before acting on it).

5. **This file is overdue a rollover** (§0 rule 5): **3,844 lines against a
   ~2,000 limit**, and it grew again on 14 Aug 2026's fourth session rather
   than shrinking — §0 rule 5 says a finding is never left out to hit the
   number, and `AllowGroups` produced findings. **That makes the rollover the
   most overdue item in this list, and it is a job for a session that starts
   with it rather than one that reaches it.**

   Superseded installer material was compressed on 14 Aug 2026, which is not
   enough. The candidates, in order of how much they would shed
   and how little would be lost: §4's older entries on the staged tree and the
   probe builds, most of which are now covered by the installer working
   end to end; §3's "This machine as the session ended (13 Aug 2026)", which
   describes a development tree that is no longer how the system is reached;
   and §5.6, which is the longest section in the file and largely settled. Move
   them to HISTORY.md, newest first. Not done here because it is a
   restructuring job rather than a trim, and it should not be bolted onto a
   session that was testing something else.

**Read first if anything to do with compilation misbehaves:** the `ERRGEN` trap
in §6. An undefined `$define` in SD is a *warning* at compile time and an abort
at run time, in a program that may not run until much later.

---

## 0. Maintenance rules

These are binding. A stale status file is worse than none, because the next
session will act on it.

1. **Update this file in the same commit as the work it describes.** Not
   afterwards, not "at the end". If a commit changes what builds, what runs,
   what is decided, or what is next, it changes this file too.
2. **Never promote anything into Verified without evidence in that session.**
   "It compiles" is not "it runs". "It ran once" is not "it is tested". If you
   did not observe it yourself, it belongs in §4 Unverified, whatever a
   previous session claimed.
3. **Record corrections, do not quietly overwrite.** If something here turns
   out to be wrong, fix it *and* note the correction in HISTORY.md. A future
   session that reads only the corrected text cannot tell it was ever wrong,
   which is how the same wrong turn gets taken twice.
4. **Traps in §6 are the highest value part of this file.** Anything that cost
   more than about fifteen minutes to work out goes there, phrased as what
   happens and what to do.
5. **Roll over when this file exceeds ~2000 lines**, or when any section is
   mostly historical. Move the settled material to HISTORY.md, newest first,
   and leave behind only what a new session needs to act today. §1–§7 are
   permanent sections; keep them, shorten them.

   **Understand what the limit is for.** It exists to stop this file sprawling
   to the point where nobody reads it — a handoff document that has grown to
   several thousand lines has stopped being a handoff document. It is not a
   target to sit near, and it is never a reason to leave a finding out. If
   something is worth recording, record it and trim elsewhere; detail that also
   exists in HISTORY.md is the first thing to cut, since nothing is lost by it.

   Prune when a section has gone stale, not when a number is approached. The
   best moment is just after work lands: instructions that have been carried
   out become history, and shed easily.
6. **HISTORY.md is append-only.** Never delete or rewrite an entry. Correct it
   with a new entry that references the old one.
7. **State the date as an absolute date.** Never "today", "last week", "the
   previous session".
8. **Anything a user would notice goes in `sdb_ai/sd64/sdsys/changelog`**, in
   the same commit. That is the product changelog, it ships with the system,
   and the port had added nothing to it for its first several sessions while
   these two files carried everything. They are not a substitute: this file is
   the state of the work, HISTORY.md is why it was done, the changelog is what
   changed for someone using SD. New verbs, new or moved files, changed
   behaviour at login, new messages and new configuration all belong there;
   refactors, findings and traps do not.

Checklist before you end a session:

- [ ] §3 Current state matches what is actually in the tree
- [ ] §4 Verified / Unverified is honest, and nothing was promoted without evidence
- [ ] §6 Traps gained anything that cost you real time
- [ ] §7 Next steps reordered, with anything finished removed
- [ ] Anything user visible added to `sdb_ai/sd64/sdsys/changelog`
- [ ] Any correction to earlier claims noted in HISTORY.md
- [ ] Header date and commit above updated

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
mingw-w64-ucrt-x86_64-gcc`.

**`python-devel` and `gettext-devel` are no longer needed** (13 Aug 2026), both
dropped with embedded Python (§5.15). `gettext-devel` was only ever there
because `python3-config --ldflags --embed` emits `-lintl` and the runtime
`libintl` package does not carry the link library — so removing the interpreter
took a second, unrelated-looking dependency with it.

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

**The unmodified Linux version is at
<https://codeberg.org/stringdatabase/sdb64>** (given by the repository owner,
14 Aug 2026). `sdb64` is the active project; this tree is the experimental
variant. Use it to check what the original does before assuming a difference is
deliberate — several things this port has "found" turned out to be inherited
rather than introduced. It is a network resource, not a local tree, so it is
available on any machine.

**The TCL verb surface is written down**, in
[docs/TCL_VERBS.md](docs/TCL_VERBS.md) — SD's commands against OpenQM 2.6.6,
supplied by the repository owner 14 Aug 2026. Read it before adding or renaming
a verb. The important structural fact it records: **SD has accounts, not
accounts and users.** `CREATE.USER`, `DELETE.USER`, `ADMIN.USER` and
`LIST.USERS` are all deliberately absent, which is why `CREATE.ACCOUNT`
provisions the operating system account itself and why the `CREATUSR` gate was
removed (§7 step 1).

Neither of the two local trees below is part of this repository, both will be
absent on a fresh machine, and nothing in the build depends on either.

**`C:\Users\dmont\Projects\gplsrc`** — original GPL ScarletDME C source. Value
is limited; Ladybridge stripped the Windows code thoroughly and only
`qmclient.c` holds any, which `gplsrc/sdclilib/` has since superseded. Still
useful for recovering text mangled by the `qm`→`sd` rename, which is how the
corrupted `#include` in `sdclient.c` was confirmed.

**`C:\Users\dmont\Projects\GPL.BP`** — original ScarletDME BASIC source, 212
files. **This one is genuinely valuable**, unlike the C tree. It retains real
Windows code that this repository's `sdsys/GPL.BP` had stripped: 21 files carry
Windows logic there against 6 here, and every file present in both lost all of
it. See §5.4.

### Relationship to sdb64

`sdb64` is the active project. This tree, `sdb_ai`, is an experimental variant
that has been through five major AI cleaning and validation cycles, which is
why the code reads more cleanly than its age suggests. Those cycles are also
capable of introducing new problems — see the `VALID_OS_PATH` trap in §6.

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

**SD runs.** The sequence below completed on 13 Aug 2026 and the system answers
commands (§4). It is the order `installsdai.sh` uses, with that script's line
numbers, and it is what an installer has to reproduce:

**It is a script now, not prose: `gplbld/bootstrap.py`.** Run it through
`gplbld/stage.py --bootstrap`, which is how an install is built (§5.16). The
sequence it runs, corrected on 14 Aug 2026 by running it:

```sh
python3 gplbld/bbcmp.py <sysdir> GPL.BP/BBPROC  GPL.BP.OUT/BBPROC
python3 gplbld/bbcmp.py <sysdir> GPL.BP/BCOMP   GPL.BP.OUT/BCOMP
python3 gplbld/bbcmp.py <sysdir> GPL.BP/PATHTKN GPL.BP.OUT/PATHTKN
python3 gplbld/pcode_bld.py <sysdir>          # takes the path now, see below
touch <sysdir>/gcat/'$CPROC'                  # empty placeholder, required
sd -start                                     # before -i, not after
sd -i                                         # pass 1; DIES ON SIGNAL 6, see below
sd -internal SECOND.COMPILE
sd -internal RUN GPL.BP WRITE_INSTALL_DICTS NO.PAGE
sd -internal THIRD.COMPILE
sd -internal BASIC GPL.BP CPROC               # writes the real gcat/$CPROC
```

**Three corrections to what this file used to say**, all found by running it:

- **The last three steps need `-internal`.** They were written as plain
  `sd RUN ...` and `sd THIRD.COMPILE`. That stopped working on 13 Aug 2026,
  when plain `sd` with no account named began asking `Account:` instead of
  putting an administrator into SDSYS (§5.6). They sat at the prompt and the
  connection was terminated. Nobody noticed because nobody re-ran the
  bootstrap between the change and 14 Aug.
- **`sd -i` finishes its work and then dies on signal 6.** Its exit status
  says nothing, so judge it on what it created — `VOC`, `VOC.DIC`,
  `ACCOUNTS.DIC`, `$MAP`, `DICT.DIC`. `installsdai.sh` sidestepped this by
  commenting the line out (line 603), which is why it never surfaced.
- **`pcode_bld.py` takes the sysdir as an argument.** It had
  `/usr/local/sdsys` hardcoded, which cannot work when building an install at
  another path.

`gplbld/FILES_DICTS` is copied into `<sysdir>/gplbld/` for the bootstrap and
removed afterwards — `WRITE_INSTALL_DICTS` reads it as
`@sdsys:"/gplbld/FILES_DICTS"`. It is a build input, not data, so it must not
still be there when the tree ships.

Two steps look wrong and are not. The `touch` is what lets `sd -start` run
before anything is catalogued — `read_config()` only does `access(path, 0)` on
`<sysdir>/gcat/$CPROC`, so an empty file satisfies it and the last step
overwrites it. There is no ordering deadlock; if it looks like one, read the
HISTORY entry "SD runs. Full bootstrap completes" before re-deriving it.

Three things worth knowing before running it:

- **`gplsrc`, `gplobj` and `gplbld` do not belong in `<sysdir>`** (13 Aug 2026).
  `APISRVR` and `ERRTEXT` each carried a `$execute` that ran a build tool
  against `./gplsrc`; both are commented out and `gplbld/gen_includes.py` does
  that work at build time. `SECOND.COMPILE` compiled 207 programs with no
  errors without them (§4). `installsdai.sh` still copies them and should stop.
- **An aborted run leaves record locks behind**, so `sd -stop` and `sd -start`
  before retrying, or the next run waits forever at no CPU (§6).
- **Every catalogue write prints `Unable change ownership of directory error
  <path> err: 1000`.** That is `CATALOG` doing the Linux `chown` to
  `sdsys:sdusers`, which has no Windows meaning. Non-fatal, and it goes with
  the rest of the OS-account work in §5.6.

### This machine as the session ended (13 Aug 2026)

None of this is in the repository. The layout is the pre-§5.8 one, under `/etc`
and `/usr/local`; there is no reason to redo it by hand, but **the installer
must not reproduce it**.

| Thing | State |
|---|---|
| `/etc/sd.conf` | `SDSYS=/usr/local/sdsys`; `USRDIR`/`GRPDIR` point at `C:\ProgramData\SD\` |
| `/usr/local/sdsys` | fully bootstrapped, SD answers commands |
| SD server | started, `sdlnxd` running |
| Binary used | `/usr/local/sdsys/bin/sd.exe`, the shipped build — the probe is no longer needed here, since the token now carries `sdadmins` |
| `sdadmins` local group | created, `GITORLI\don` enrolled — **unnecessary under §5.6**, but do not delete it yet (§8) |
| **SDSYS password** | **`hunter2`** — set during testing, change it |
| Scratch accounts | `JANE`, `SUE`, `KIM` under `/home/sd/user_accounts`; `PAT` under `C:\ProgramData\SD\user_accounts`. Passwords **`correcthorse`** (SUE) and **`batterystaple`** (PAT). Delete all of them before this machine is used for anything real |
| Grants recorded | `JANE` grants `SUE`; `SDSYS` grants `SUE`; `KIM` and `PAT` grant nobody, which is what makes them useful |
| `gplsrc`, `gplobj`, `gplbld` | **moved out of `<sysdir>`** into a session scratchpad. Do not put them back |
| `<sysdir>/C:` | an empty directory left by the `sdrealpath()` bug before it was fixed (§5.8). Harmless, and not evidence of anything |

**Scratch test programs in `<sysdir>/BP`**, none of them in the repository:
`CREDTEST`, `CREDRT`, `SETPW`, `INTEST`, `VTEST`, `MKACC`, `GRANT`, `WHOAMI`,
`MKDICT`, `MKBP`, `PROBE`, plus `SUE/BP/ESCALATE` (§4), which no longer
compiles. `SETPW` and `MKACC` hold passwords in plain text and go with the
scratch accounts. Two are worth keeping until there are real verbs for the job:
`WHOAMI` prints `@LOGNAME`, `@WHO`, `@PATH` and `SYSTEM(1050)`, and is
catalogued **globally** so it runs from an account with no `BP` file; `MKACC`
skips an account already in ACCOUNTS rather than rewriting it, so re-running it
does not wipe the grant lists.

A **non-administrator probe** sits at `/tmp/nonadmin/sd_nonadmin.exe`, built
per §6 with `SD_ADMIN_GROUP` naming a group nobody holds. It is the only way to
see this system as an ordinary user, since every session here is otherwise an
SD administrator. `/tmp` does not survive a rebuild; the recipe in §6 does.

### Picking it up again

**Note the default configuration moved on 14 Aug 2026.** With nothing set,
SD now reads `C:\ProgramData\SD\sd.conf` and therefore the installed tree at
`C:\ProgramData\SD\sdsys`. That tree has **no SDSYS password**, so `LOGIN`
warns and admits an administrator; it **does** have the ACLs, applied by the
installer, so an unelevated session that has not signed out since being added
to `sdusers` cannot read it at all (§6). The development tree below is reachable
only by setting `SD_CONFIG=/etc/sd.conf`.

`echo hunter2 | sd -internal COUNT VOC` should report 432 records and
`echo hunter2 | sd -ASDSYS WHO` should report `SDSYS`. **Both need the password
now** — the internal no-password path is gone (§5.6). If they fail, SD is not
started: `bin/sd.exe -stop` then `bin/sd.exe -start`, redirecting output to a
file (§6).

**A scripted session must be piped from an MSYS2 shell** and cannot use a `<`
redirect (§6):

```sh
cat commands.txt | /usr/local/sdsys/bin/sd.exe -ASDSYS 2>&1 | tr -d '\r'
```

with the password as the first line of `commands.txt` and `OFF` as the last.
Leave a prompt unanswered at end of input and SD spins at full CPU (§6).

## 4. Verified vs unverified

Keep this split honest. It is the single most useful thing in the file.

### Verified by observation

- All six binaries compile, link and run. `sd.exe` prints `SD has not been
  started`, which specifically exercises the new `sem_open` probe path.
- `sdtic.exe` compiled `terminfo.src` into 99 terminfo files — real work, not
  just a banner.
- Client DLL compiles with **zero warnings** under `-Wall -Wextra -Wpedantic`,
  both bundled test suites pass, and it exports 51 `SD*` symbols including
  `SDConnectLocal`.
- MSYS2 runtime behaviour, tested by compiling and running probes:
  `fork`/`waitpid`, `termios`, `getpwuid`, `shm_open`+`mmap`, `sem_open`,
  `mmap(MAP_SHARED|MAP_ANONYMOUS)` all work. `shmget` and `semget` **fail at
  runtime with ENOSYS**.
- `terminfo` regenerates byte identically with and without the `O_BINARY`
  correction, confirming that change is protective rather than a repair.
- The group-based `IsAdmin()` logic, against member, non-member, absent group
  and primary group. `getgrnam()` resolves Windows local groups on the MSYS2
  runtime and reports membership accurately. (Superseded as the identity model
  by §5.6, but the observation stands and `IsAdmin()` still gates `sd -start`.)
- **`IsAdmin()` in the linked binary.** `sd -start` refused with "Command
  requires administrator privileges" while the group was absent, and got past
  that check once built against a group the token holds. So `check_admin()`
  and `IsAdmin()` work in the real executable, in both directions.
- **The whole shared segment lifecycle**, exercised at 3 MB in the shape
  `sysseg.c` uses: create, size, map, attach from a second mapping, confirm the
  attach sees the right size and content, write through one mapping and read it
  through the other, create six semaphores, confirm one excludes while held and
  can be reacquired after posting, unmap, unlink, and confirm a later attach
  gives ENOENT. All as intended. This was the largest single unknown in the
  port; it has since been exercised by SD itself as well — see below.
- `gplbld/bbcmp.py` and `gplbld/pcode_bld.py` both run on Windows and produce
  `gcat` entries and `PCODE.OUT`.
- **SD has started.** `sd -start` (probe build, §6) created the shared segment
  and all six semaphores *itself* — `/dev/shm/sd_shm_716d0301` at 100 KB and
  `sd_sem_716d0302_0` through `_5` — and spawned `sdlnxd` (renamed `sdwind` on
  14 Aug 2026), which stayed
  running. This is the `shm_open`/`ftruncate`/`mmap` **creation** path in
  `sysseg.c` executing for the first time; it had never run before, and it was
  the largest remaining unknown after the standalone lifecycle test. Observed
  13 Aug 2026.
- The `gcat/$CPROC` placeholder satisfies `read_config()`. An empty file is
  enough, as the check is only `access(path, 0)`.
- **Multi-process attach works.** A second process (`sd -i`) attached to the
  segment created by `sd -start`, was allocated a user table slot, and wrote to
  `<sysdir>/errlog` — "User 2 (pid 1931, don)", "User 5 (pid 2050, don)". This
  was listed as unverified until now.
- SD writes `<sysdir>/errlog` correctly, including on receipt of SIGTERM.
- **`sd -stop` works, including the new liveness poll.** It reported "SD (64
  Bit) has been shut down", and `/dev/shm` was left completely empty — the
  segment and all six semaphores unlinked. `sd -start` then brought the system
  up again from nothing. So the full start/stop/restart cycle runs, which
  closes the `stop_sd()` item that was listed as unverified.
- **Account passwords work end to end.** `!SD_GET_SALT` returns a fresh
  24-character salt per call and `!SD_KEY_FROM_PW` a reproducible 44-character
  Argon2 key that changes with either password or salt — libsodium works on
  Windows, and neither routine had a caller before. Round trip through
  `!CRED_SET` / `!CRED_VERIFY`: the right password verifies, the wrong one does
  not, account names are case insensitive, an unknown account and an empty
  password both fail closed, and re-setting the same password yields a new salt
  and verifier that still verifies. The stored record holds salt and key only,
  with no trace of the password.
- **Login authenticates.** `echo hunter2 | sd -ASDSYS WHO` reports `SDSYS`; a
  wrong password is refused three times and terminates the connection; and
  `sd -internal COUNT VOC` still returns 432 records through the administrator
  install path. Observed 13 Aug 2026.
- **The complete bootstrap runs, and SD answers commands.** Every step from
  `sd -start` through `BASIC GPL.BP CPROC` completed on 13 Aug 2026;
  `SECOND.COMPILE` alone compiled 204 programs with no errors. `WHO` reports
  `7 SDSYS`, `COUNT VOC` reports 431 records and `SELECT VOC` selects them. So
  the compiler chain (`BCOMP`, `@ds` path resolution, the pcode loader), DH
  file creation, and reading records back all work.
- **`@ds` is correct for stage 1.** 204 programs compiled with
  `dir.separator` hardcoded to `/`, which settles the open question in §6 for
  the MSYS2 runtime. It remains live for stage 2.
- **`K$ADMINISTRATOR` answers truthfully.** With `USR_ADMIN` seeded from
  `IsAdmin()`, the rewritten test in `BBPROC` granted access under the probe
  build (group `Users`, which the token holds). It had refused everybody before.
- **The six semaphores are not a bottleneck under normal running.** Sampled
  with a `sem_getvalue()` probe both at idle and while another process was
  waiting on a record lock: all six read 1 (free) throughout.
- **The shipped binary does everything the probe did.** Once the token carried
  `sdadmins`, `/usr/local/sdsys/bin/sd.exe` ran `-stop`, `-start`, `-internal`
  commands and a password login, all of which call `check_admin()` or
  `IsAdmin()`. The probe build is no longer needed on this machine. Observed
  13 Aug 2026.
- **The whole `LOGTO` suite behaves, in both directions.** Observed 13 Aug 2026
  as SUE: refused without a grant, admitted with one, admitted into her own
  account, refused for an account granting nobody, refused for SDSYS without a
  grant, admitted to SDSYS with a grant **and her own password** (three wrong
  tries refused without dropping the connection), refused for a pathname, and
  refused for an unknown account in wording identical to an ungranted one.
  SDSYS reaches every account without a grant, and the exception belongs to the
  account you are standing in — so SDSYS→KIM→JANE is refused at the second
  move. The exception carries through a step-up: SUE→SDSYS→KIM was admitted,
  reporting `LOGNAME=SUE WHO=KIM`. `@logname` survived every hop. The full
  case-by-case table is in the HISTORY entry "LOGTO is gated by grants, and the
  shipped binary is verified".
- **The install path still bypasses everything.** `sd -internal` entered SDSYS
  with no password, moved to JANE with no grant and back with no step-up, and
  `COUNT VOC` still reports 432 records. The bootstrap is unaffected by any of
  this; re-observed after the pathname removal.
- **Drive-letter paths work, after the `sdrealpath()` fix (§5.8).** A probe
  opened the same file through `C:\ProgramData\SD\user_accounts\PAT\VOC`,
  `C:/...`, `/c/...`, a lower-case drive letter and a mixed
  `C:\ProgramData/SD/...`. Before the fix every drive-letter form failed with
  ER_FNF and only `/c/...` worked. The MSYS2 runtime was never the problem —
  a C probe confirmed `stat()` accepts all of them.
- **Accounts under `C:\ProgramData\SD` work end to end.** `sd -APAT` run from
  `C:\Windows`, with `USRDIR=C:\ProgramData\SD\user_accounts` in `sd.conf`,
  prompted for PAT's password and landed in the account directory. The full
  bootstrap still answers (`COUNT VOC` reports 432) and the whole LOGTO suite
  above still passes against the rebuilt binary — worth stating, because
  `sdrealpath()` is on the path of every file open in the system.
- **SD does not need the MSYS2 *shell*, only its DLLs.** `sd.exe` run straight
  from a PowerShell prompt, with `C:\msys64\usr\bin` and
  `C:\msys64\usr\local\bin` on PATH, answered `COUNT VOC` with 432 records.
  POSIX paths still resolve — `/usr/local/sdsys`, `/etc/sd.conf` — because the
  translation is done by `msys-2.0.dll`, not by bash. So the shell dependency
  is already gone; what remains is the runtime dependency, which is stage 2.
- **SD no longer needs an operating system group to use.** Observed with a
  probe whose `SD_ADMIN_GROUP` names a group nobody holds (§6), which is the
  only way to be a non-administrator on this machine. `sd -ASUE` prompted for
  the account name's password and entered SUE with `SYSTEM(1050)` reporting
  **0** — not an administrator, and nothing about the Windows account
  mattered. That is the whole point of §5.6, and it had never been shown from
  the outside.
- **The SDSYS password alone makes you an SD administrator.** The same
  non-administrator probe ran `sd -ASDSYS`, was prompted, gave `hunter2`, and
  arrived with `SYSTEM(1050)` reporting **1**. `LOGIN` sets the flag on entry
  to SDSYS, so administration is now genuinely a matter of knowing the SDSYS
  password rather than of Windows group membership.
- **Administrator rights follow you out of SDSYS.** In that same session,
  `LOGTO KIM` left `SYSTEM(1050)` at 1 while standing in KIM. **Fixed later
  the same day** — see the privilege-escalation entry below.
- **Privilege escalation was demonstrated, then closed.** Before the fix, the
  account SUE compiled a three-line `$internal` program calling
  `kernel(26, 1)` — `K$ADMINISTRATOR`, written as a literal — in her own `BP`
  and ran it from an ordinary session. It printed `before: 0` / `after: 1` and
  `SYSTEM(1050)` then reported 1: a plain user account making itself an
  administrator. After the fix the same program will not compile, `$internal`
  being refused, and `sd -internal -ASUE` is refused by `sd.c`. Listing in the
  HISTORY entry "Administrator rights become the SDSYS account's".
- **The rest of the account model still behaves after all of that.** `sd`
  with no account named now prompts `Account:` even for a member of
  `sdadmins`; `sd -internal` prompts for the SDSYS password and refuses three
  wrong ones; the whole `LOGTO` suite above still passes; and
  `BASIC GPL.BP CPROC` still compiles a system program, which is the one that
  matters, since `BCOMP` itself changed.
- **The data tree needs no C source.** `SECOND.COMPILE` compiled **207
  programs with no errors** against a `<sysdir>` with `gplsrc`, `gplobj` and
  `gplbld` moved away — run twice, once with the original include files and
  again after regenerating them, both clean. Afterwards `COUNT VOC` still
  reports 432 records, `WHO` still reports `SDSYS`, and `COUNT NOSUCHFILE`
  still expands to "File not found", which exercises `!ERRTEXT` and therefore
  the regenerated `ERRTEXT.H`. 207 rather than the 204 recorded earlier
  because the credential programs were added since. Observed 13 Aug 2026.
- **The staged tree runs with MSYS2 entirely off PATH.** `gplbld/stage.py`
  built the tree; `sd.exe` from
  `<stage>\ProgramFiles\usr\bin\` then ran with `PATH` cut down to
  `C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem` — no `msys64`, no
  Git for Windows — and answered `SD is not active.` cleanly, with no warnings
  and exit 0. That proves the computed DLL closure is complete — only
  `kernel32` and `ntdll` come from Windows — and that the `usr\bin` plus
  `etc\fstab` arrangement resolves `/dev/shm` correctly. "SD is not active" is
  the right answer, not a failure: the running server's segment belongs to the
  `msys64` POSIX root and this process has its own. Observed 13 Aug 2026 at
  3087 files and 16 MB with embedded Python, and **3059 files and 9.6 MB after
  §5.15 removed it**, the closure dropping from seven DLLs to four —
  `msys-intl-8` and `msys-iconv-2` turned out to be there only because Python
  was.
- **`gplbld/gen_includes.py` reproduces the generators it replaces.** Its
  output matched the tracked files byte for byte on everything that had
  genuinely been generated from the current C headers — all 199 entries of
  `GPL.BP/ERRTEXT.H` and 199 of the 241 `$define` lines in `SYSCOM/ERR.H` —
  and the differences it reported were all real drift, described in the
  HISTORY entry. `--check` reports the three files in sync after regeneration
  and reported each of them stale before it.

- **`!valid_os_path` accepts native Windows paths and still rejects
  metacharacters.** Observed 14 Aug 2026 from inside SD, 16 cases, all as
  intended: `C:\Program Files\SD\usr\bin`, `C:\ProgramData\SD\sdsys`,
  `/usr/local/sdsys` and a mixed `C:/ProgramData/...` all pass; empty, over
  255 characters, and each of `;` `&` `|` `$` backtick, both quote characters,
  `>` `*` and a tab are all refused. This is §7 step 2, and it was blocking the
  binaries moving under `C:\Program Files`.
- **`!is_grp_member` works on Windows.** Observed 14 Aug 2026 from inside SD,
  7 cases: `don`/`sdadmins` and `don`/`Administrators` report member with
  status 0; `don`/`Guests` reports not-a-member with status 0; `sdusers`,
  `nosuchgroup` and an empty user name each report status 1; and a name equal
  to the group name still reports member, which is the rev 0.9.0 "own group
  account" case. This closes the trap in §6 that had it answering "no" for
  everyone, and it is what makes the login gate possible again. **Note
  `sdusers` does not exist on this machine** — only `sdadmins` — so status 1
  there is the true answer, not a failure.
- **`!ps_script` runs a PowerShell script with a secret in it, off the command
  line.** Observed 14 Aug 2026 from inside SD: `exit 42` came back as 42, a
  `throw` as 1, an empty script as -1 with status 1, the body genuinely ran
  (it wrote a marker file that was read back afterwards), and the temporary
  script was removed. So the write, the pipe through bash into PowerShell, the
  exit status and the cleanup all work.
- All ten changed or new `GPL.BP` programs compile with 0 errors and no
  "not assigned a value" warnings: `VALID_OS_PATH`, `IS_GRP_MEMBER`,
  `PS_SCRIPT`, `OS_GROUP`, `CREATE_USER`, `DELETE_USER`, `SET_PASSWD`,
  `CREATEA`, `DELACC`, `MODIFYA`.

- **The shell is PowerShell now, and bash is out of the loop.** After
  rebuilding `sd.exe` with the new `op_sh.c` defaults and putting `SH`/`SH1`
  in `sd.conf`, both probes above were re-run and every case still passed —
  `is_grp_member` 7 of 7, `ps_script` 5 of 5. So `OS.EXECUTE` reaches
  PowerShell, the exit status still carries back through `OS.ERROR()`, and
  `!ps_script` still finds its own temporary file by a relative name.
  Measured beforehand, and it decided the design: `Invoke-Expression`
  propagates a script's `exit` status where `& .\script.ps1` does not — a
  script ending `exit 7` gave 7 through the first and 1 through the second —
  and it is not subject to the execution policy, so nothing needs
  `-ExecutionPolicy Bypass`.

- **THE STAGED TREE INSTALLS AND RUNS, and this is the first time.** Built
  with `python3 gplbld/stage.py --stage <dir> --force --bootstrap` on
  14 Aug 2026: the full bootstrap ran against the staged tree —
  `SECOND.COMPILE` compiled **190 programs with no errors** — the SDSYS
  account record was retargeted to `C:\ProgramData\SD\sdsys`, and the
  build's own check confirmed nothing else in the tree embeds the build path.
  3278 files, 10.4 MB, four MSYS2 DLLs, and only `kernel32` and `ntdll` from
  Windows.

  It was then **installed by copying** `ProgramData\sdsys` and `sd.conf` to
  `C:\ProgramData\SD\` and run from the staged binaries: `sd -start`
  succeeded, `COUNT VOC` reported **431 records**, `WHO` reported `2 SDSYS`,
  and `LIST ACCOUNTS` showed `Pathname: C:\ProgramData\SD\sdsys` with the
  account name and grant list intact. **No Python and no compiler were used
  at install time.** This is §7 step 3b, which had never been done, and it
  closes "nothing has ever been installed from a staged tree".

  Two things it does *not* prove: the machine still has a development tree, so
  an accidental dependency on it could still be hiding; and `C:\Program
  Files\SD\` was not used, because creating it needs elevation — the
  binaries were run from the staging directory, which exercises the same POSIX
  root rule but not the final location.

- **A GENUINE FIRST INSTALL WORKS, AND THE FILES WERE COUNTED.** Observed
  14 Aug 2026, second session, and this closes the correction below. The
  machine was cleaned first — uninstall, both trees deleted, `sdusers` removed
  — and the installer **rebuilt from the tracked `gplbld/sd.iss`** rather than
  taken on trust, so the `.exe` under test provably matches the committed fix.

  | Measure | Broken | Now | Staged source |
  |---|---|---|---|
  | files under `C:\ProgramData\SD\sdsys` | 16 | **3,264** | 3,264 |
  | directories under it | — | 44 | 44 |
  | `gcat` entries | 0 | 129 | 129 |
  | `GPL.BP.OUT` entries | 0 | 11 | 11 |
  | `Installing the file` lines in the Inno log | 15 | 3,279 | — |
  | Inno log length | 145 lines | 16,507 lines | — |

  A `Compare-Object` of every staged path against every installed path reported
  **no differences in either direction** — nothing skipped, nothing extra.

  **And the installed system runs**, observed twice in two separate elevated
  passes: `sd -start` from `C:\Program Files\SD\usr\bin\sd.exe`, `COUNT VOC`
  reporting **431 records**, `LIST ACCOUNTS` reporting `Pathname:
  C:\ProgramData\SD\sdsys`, `WHO` reporting `3 SDSYS`, `sd -stop`. Each was
  preceded by `Warning: account SDSYS has no password set`, which is correct
  for an install nobody has finished — and is §5.9's password-ordering
  decision working as intended.

  Everything else the installer is responsible for, confirmed on the same run:
  `sdusers` created with `GITORLI\don` in it; `user_accounts`, `group_accounts`
  and `shm` created; exactly one `C:\Program Files\SD\usr\bin` entry on the
  system PATH; 15 files in `C:\Program Files\SD`; no `gplbld` anywhere in the
  data tree; and `sd.conf` present.

- **THE INSTALLED SYSTEM RUNS AS AN ORDINARY USER.** Observed 14 Aug 2026 after
  the repository owner rebooted, from a **normal unelevated PowerShell window**
  — no `runas`, no MSYS2, nothing set in the environment:

  ```
  sd -start          SD (64 Bit) has been started      sdwind running: True
  COUNT VOC          431 record(s) counted
  WHO                2 SDSYS
  sd -stop           SD (64 Bit) has been shut down    sdwind gone
  ```

  This is the first time SD has been used the way a user would actually use
  it, and it closes three things at once:

  - **§5.6.1 in the real world.** `IsAdmin()` admitted an administrator who had
    not elevated. The earlier proof was a probe with a synthetic gid; this is
    the shipped binary in an ordinary session.
  - **§5.7's ACL model, from the user's side.** The token now carries
    `sdusers`, and that grants both the data tree — 3,264 files listed from the
    unelevated session — **and** `/dev/shm`, which is mapped into
    `C:\ProgramData\SD\shm` and is what `sd -start` needs to allocate
    semaphores. The "Error 13" trap in §6 is what this looks like when the
    token is stale, and it is now shown clearing.
  - **The sign-out requirement is real and is sufficient.** Before the reboot
    this same session was refused on every path inside `C:\ProgramData\SD`.
    Nothing else changed.

  **What it does not show:** `sd -start` had to be typed. An installed system
  does **not** come up on boot — there is no service — so after every restart
  someone must start SD by hand. That is §5.7's service model, and it is now
  the most visible gap in a system that otherwise installs and runs.

- **OpenSSH Server installs, and `sshd` runs.** Observed 14 Aug 2026. After the
  reboot, `Get-WindowsCapability -Online` reported
  `OpenSSH.Server~~~~0.0.1.0  State : Installed`, so the corrected
  `Add-WindowsCapability` line works and the brace bug was the whole of it.
  `gplbld/install-ssh.ps1` then reported `sshd is Running,
  StartType=Automatic`, with 2 listeners on port 22, the
  `OpenSSH SSH Server (sshd)` firewall rule enabled, and
  `C:\ProgramData\ssh\sshd_config` created — sshd writes that on first start,
  which is the earliest point at which `AllowGroups` (§5.6.2) could be edited
  into it.

  **And it exposed an installer defect that is now fixed.** The capability
  installed but the **service did not exist until after a reboot**. The old
  step ran `Add-WindowsCapability`, `Set-Service` and `Start-Service` in one
  breath, so on such a machine `Set-Service` threw "no such service", hit the
  catch, and reported total failure for what was actually a success needing a
  restart. `install-ssh.ps1` now distinguishes them and **exits 2 for "restart
  required"**. Being told to reboot is useful; being told it failed is not.

- **The deny-logon rights are applied correctly, and nothing else is
  disturbed.** Observed 14 Aug 2026 against a throwaway group, running
  `gplbld/deny-logon.ps1` exactly as the installer invokes it:

  | Right | Before | After |
  |---|---|---|
  | `SeDenyInteractiveLogonRight` | `Guest` | `sddenyprobe,Guest` |
  | `SeDenyRemoteInteractiveLogonRight` | *absent* | `sddenyprobe` |
  | `SeDenyNetworkLogonRight` | `Guest` | `Guest` — **untouched** |

  The last row is the one that matters: ssh authenticates with a network
  logon, so leaving that right alone is what keeps ssh working (§5.6.2). The
  first row is the argument for `LsaAddAccountRights` over `secedit` shown
  working — the existing `Guest` entry survived, where a policy rewrite would
  have had to reproduce it. Running it twice succeeds (idempotent), and naming
  a group that does not exist exits 1 with "Group sdnosuchgroup was not found"
  rather than failing quietly.

  **A caveat on reading this back.** `secedit /export` writes resolvable local
  groups **by name**, not by SID, so a verification that greps the policy for a
  SID reports "not present" when it is. That is what the first attempt at this
  test did. Compare against the name, or read the whole policy line.

  **Not verified:** that an account in the group can still ssh in while being
  refused at the console. That needs a running `sshd`, which this machine does
  not yet have — see the OpenSSH entry in §4 Unverified.

- **`CREATE.ACCOUNT` RUNS, AND IT HAD NEVER BEEN RUN BEFORE.** Observed
  14 Aug 2026 from an elevated session, driven through a pipe with the
  password first. Both halves of the account are made, and the
  `ADMINISTRATOR` keyword does exactly what §5.6.1 decided:

  | | `CREATE.ACCOUNT USER sdtest1` | `... sdtest2 ADMINISTRATOR` |
  |---|---|---|
  | Windows local user, enabled | yes | yes |
  | member of `sdusers` | yes | yes |
  | `sdu_<name>` group created | yes | yes |
  | account dir, VOC, `$HOLD`, `$SAVEDLISTS`, BP, private catalogue | yes | yes |
  | record in `ACCOUNTS` | yes | yes |
  | **member of Administrators** | **no** | **yes** |

  So a standard local account is the default and an administrator is made
  deliberately, which is the decision. `sdtest2 is now an SD administrator`
  came from the new message 10032, and the Administrators add went in **by
  SID** — `!os_group` now accepts `S-1-5-32-544` and uses
  `Add-LocalGroupMember -SID`, because the name is localised.

  It also closes "**Every OS account operation**" as far as creation goes:
  `CREATE_USER`, `SET_PASSWD` and `OS_GROUP` have all now executed against real
  Windows accounts. `DELETE.ACCOUNT` and `MODIFY.ACCOUNT` still have not.

  **Both test accounts were deleted afterwards** — they were real Windows
  accounts with a known password and one was an administrator. One empty
  `sdu_sdtest2` group survives, harmless; `Remove-LocalGroup sdu_sdtest2`
  clears it.

- **A Windows administrator is an SD administrator, tested two ways.** Observed
  14 Aug 2026 from an **unelevated** session belonging to a machine
  administrator — the case the previous test would have got wrong. Positive:
  the shipped build ran `sd -start`, the daemon came up, `sd -stop` took it
  down. That is decisive rather than incidental, because gid 544 is **not** in
  `getgroups()` in that session, so it can only have been found through
  `getgrouplist()`. Negative: `sd.c` and `linuxlb.c` rebuilt with
  `-DSD_ADMIN_GID=99999` refused with "Command requires administrator
  privileges", exit 1 — so the gid really is the test, and §6's probe override
  still works. See §5.6.1.

- **The daemon starts on an installed system, and it is called `sdwind`.**
  Observed 14 Aug 2026 after the fix. It had **never** started from an install:
  `sysseg.c` execed `"%s/bin/sdlnxd"` built from `sysseg->sysdir`, and
  `<sysdir>/bin` holds `pcode` and `pcode.old` and no executables at all (the
  §5.8 split). `start_sd()` now asks `exe_directory()` — `/proc/self/exe`,
  which the MSYS2 runtime implements — and launches the daemon from beside the
  running executable, so the two cannot drift apart again.

  Verified end to end on a clean first install: `sd -start` from
  `C:\Program Files\SD\usr\bin\sd.exe` left
  **`sdwind.exe` running as pid 9740 out of `C:\Program Files\SD\usr\bin\`**,
  while `<sysdir>\bin` held only `pcode, pcode.old` — so the old path could not
  possibly have worked. `COUNT VOC` then reported **431 records**, `WHO`
  reported `2 SDSYS`, and `sd -stop` took the daemon down again. The same run
  re-counted the install at **3,264 of 3,264** files, which also confirms the
  installer still works after `stage.py` changed.

  **The silence is the part worth remembering.** The `execl` is in a forked
  child that has already called `daemon()`, so a failure printed nothing and
  `sd -start` still reported success. The child now `_exit()`s with a message
  instead of falling back into the caller's code, which is what it did before —
  so a future failure will at least say so. Trap in §6.

  A second call site had the same defect and is fixed with it: the daemon's own
  `check_lost_users()` built `'<sysdir>/bin/sd' -cleanup` to launch a cleanup
  session. Not separately verified, since nothing has yet made a session go
  missing.

- **The ACLs are right, and this time that was checked from the outside.** The
  data tree carries exactly `GITORLI\sdusers:(OI)(CI)(M)`,
  `BUILTIN\Administrators:(OI)(CI)(F)` and `NT AUTHORITY\SYSTEM:(OI)(CI)(F)`,
  with no `BUILTIN\Users`. New on 14 Aug 2026: an ordinary **unelevated**
  session, whose token does not yet carry `sdusers`, was refused on every path
  inside `C:\ProgramData\SD` — so the lockout is real and not just a listing.
  **`Test-Path` on the directory itself still answers True**, because listing
  the parent is permitted; only the contents are denied. Check inside, or you
  will conclude the ACL never applied.

- **CORRECTED 14 Aug 2026, and now fixed and verified — kept because the
  diagnosis is the lesson.** An earlier claim that the installer worked was
  true of the **upgrade** path only. A genuine first install
  **produced a broken database**: `Check: DataTreeAbsent` is evaluated *per
  file*, so the first file created `C:\ProgramData\SD\sdsys`, every later
  evaluation answered False, and the remaining ~3,260 files were silently
  skipped. 16 files installed, no `gcat`, no `GPL.BP.OUT` — and Setup still
  exited 0. The upgrade path hid it, because it skips the whole set
  consistently and looks identical either way. `InitializeSetup` now caches the
  answer once, before any file is copied; the entry above is that fix running.
  **The lesson stands whatever the installer does next: an install test that
  does not COUNT what was installed proves very little.**

- **The upgrade path works too, and it is a different path.** Observed 14 Aug
  2026, before the first-install run above; trimmed here to what that run does
  not already cover. Over an existing data tree, elevated and `/VERYSILENT`:
  `sd.conf` was logged "Skipping due to onlyifdoesntexist flag", the `sdsys`
  tree **does not appear in the install log at all** — `DataTreeAbsent`
  correctly skipping it — and the existing database was left untouched. Also
  confirmed on that run and not repeated since: all four MSYS2 DLLs land in
  `usr\bin` with `etc\fstab` beside them, and an entry appears under the
  `Uninstall` key so SD shows in Settings > Apps pointing at
  `C:\Program Files\SD\unins000.exe`. SD ran from `C:\Program Files\SD\usr\bin`
  for the first time there, so the `usr\bin` POSIX-root rule and the `etc\fstab`
  mapping hold at the real install location and not only in a staging
  directory.

- **An installed system finds its configuration with nothing set in the
  environment.** Observed 14 Aug 2026 with `SD_CONFIG` and `SCARLET_CONFIG`
  both explicitly unset: `sd -start` succeeded, `COUNT VOC` reported **431
  records** and `LIST ACCOUNTS` reported `Pathname: C:\ProgramData\SD\sdsys`,
  reading `C:\ProgramData\SD\sd.conf` found through `%ProgramData%`. It also
  warned "account SDSYS has no password set", which is the correct state for a
  tree the installer has not finished. This was the last thing standing between
  the staged tree and an Inno package (§5.16).

- **The uninstaller runs, and keeps the data.** Run `/VERYSILENT` on
  14 Aug 2026, exit 0: `C:\Program Files\SD` and the Settings > Apps entry
  were removed, and **`C:\ProgramData\SD` was left completely intact** — the
  database, the accounts and `sd.conf` all survived, which is what the
  repository owner asked for and what `UninstallSilent` guarantees for an
  unattended removal.

  It left two things behind, one of them a defect:

  - **The PATH entry, and Inno cannot undo it by itself.** The `[Registry]`
    entry appends with the `olddata` constant, so the uninstaller has no way to
    know which part it contributed and by default leaves a dead directory on
    the system PATH for ever. **Fixed** — `RemoveFromPath` in `sd.iss` strips
    it by name at `usUninstall`.
  - **The `sdusers` group**, deliberately. Every SD user is added to it and a
    kept data tree is ACL'd to it, so removing the group would orphan the
    permissions on a database the user just chose to keep. Now commented as
    intentional rather than left looking like an oversight.

- **THE SSH-ONLY MODEL WORKS.** Observed 14 Aug 2026 by
  `gplbld/verify-sshonly.ps1`, against a real Windows account on this machine.
  This is §5.6.2, which had been decided, built, shipped in the installer and
  never once exercised. Thirteen checks, all passing:

  | | control, in no SD group | after joining `sdsshonly` |
  |---|---|---|
  | `LogonUser` INTERACTIVE — the console | admitted | **refused 1385** |
  | `LogonUser` NETWORK_CLEARTEXT — ssh password auth | admitted | admitted |
  | `LogonUser` NETWORK | — | admitted |
  | **`ssh` with a password** | admitted | **admitted** |
  | `ssh` with a key | admitted | admitted |

  **The bottom row of the middle column is the whole design.** The console is
  closed by the deny rights and ssh is not, measured on the same account
  minutes apart with nothing else changed. `1385` is
  `ERROR_LOGON_TYPE_NOT_GRANTED`.

  **`ssh` was admitted and ran a shell**, not merely authenticated: the test
  asserts on `whoami` returning the account name, so `cmd.exe` started under
  that token. And the verdict does not rest on the test's own reporting —
  the `OpenSSH/Operational` event log recorded `Accepted password for
  sdsshprobe` and `Accepted publickey for sdsshprobe ... ED25519` from the
  installed service at the same moment.

  Also confirmed on the same run: the two deny rights are in machine policy
  against the group and `SeDenyNetworkLogonRight` is **not** — checked by
  reading `secedit /export` back and comparing **by name**, per the caveat
  already in this section. And `deny-logon.ps1` ran against a real group for
  the first time, having previously only been tried on a throwaway.

  **Why there is a control column at all.** The first run refused the key
  login on *both* sides. Had the treatment side been measured alone, that
  would have read as "the deny rights break ssh" and §5.6.2 would have been
  abandoned on a false result. An equal failure on both sides cannot have
  been caused by the thing that differs between them. Keep the control.

  **Not covered:** RDP. See §4 Unverified.

- **A brand new Windows account cannot use ssh key authentication until it has
  logged in once.** Found 14 Aug 2026 while chasing the failure above, and it
  is a property of Windows rather than of anything here. An account that has
  never logged on has no user profile and no home directory, and
  Win32-OpenSSH resolves `AuthorizedKeysFile .ssh/authorized_keys` relative to
  the home directory — so a key planted for a new account is never read.

  Observed in both directions across runs: with no prior login of any kind the
  key was refused twice; after one password login — which creates the profile,
  confirmed by the `ProfileList` registry entry and `C:\Users\<name>`
  appearing — the same key on the same account was accepted. Group membership
  was identical either way, so the prior login is the difference.

  **It applies to accounts `CREATE.ACCOUNT` makes**, which have also never
  logged on. Key-only access to a new SD account cannot work until somebody
  has authenticated with a password once. Nothing in the code has to change,
  but anyone documenting key-based access has to know it.

- **`BUILTIN\Users` membership is not required for an SD account.** Asked
  because `New-LocalUser` joins no group at all and `CREATE_USER` adds none
  either, so an SD account is in `sdusers`, `sdu_<name>` and `sdsshonly` and
  nothing else — an unusual state that looked like a likely cause while the
  ssh failures were unexplained. Measured 14 Aug 2026 rather than assumed: the
  account logged in over ssh and ran `whoami` **before** `Users` was added,
  and adding `Users` afterwards changed nothing. So `CREATE.ACCOUNT` does not
  need to add it, and a defensive `Add-LocalGroupMember` was not written.

- **SD can be driven from PowerShell, and `CREATE.ACCOUNT` reaches the OS.**
  Observed 14 Aug 2026 on the installed tree, unelevated, with SD started from
  `C:\Program Files\SD\usr\bin\sd.exe`: piped commands through `sd -ASDSYS`
  with no password — SDSYS has none set, so `LOGIN` warns and admits an
  administrator — and got `431 record(s) counted` from `COUNT VOC` and `SDSYS`
  from `WHO`.

  `CREATE.ACCOUNT USER sdacct1` then parsed, ran, and stopped at
  **`Create User Failed, OS Error: 5`** — `ERROR_ACCESS_DENIED`, the elevation
  gate in `CREATE_USER` — with **nothing created**: no Windows user and no
  account directory, both checked afterwards. So the VOC entry, the verb, the
  argument parsing and the failure path are all confirmed on the installed
  system, and the only untested part of `CREATE.ACCOUNT` is what happens once
  the token is elevated.

  Getting there cost two traps, both now in §6: SD exits with "Process
  terminated" when handed a redirected stdin, and a PowerShell pipe puts a BOM
  on the first line.

- **`allow-ssh-groups.ps1` edits `sshd_config` correctly.** Observed
  14 Aug 2026, fourth session, by `gplbld/verify-allowgroups.ps1` — 20 checks,
  all passed — against
  `C:\Windows\System32\OpenSSH\sshd_config_default`, which is the template
  `sshd` copies to `C:\ProgramData\ssh\sshd_config` on its first start. **The
  test needs no elevation, no `sshd` and no network**, because that template is
  world readable, so this half can be re-run on any machine at any time. It
  lifts the functions out of the shipped script by parsing it, so it cannot
  drift from the code it checks.

  What passed, and what each one is for:

  | Check | Why it is there |
  |---|---|
  | the block lands **before** the first `Match` | the shipped config's last line is `Match Group administrators`; appending would put `AllowGroups` **inside** that block, applying it to administrators only — which reads as working |
  | exactly one `AllowGroups` after three applies | re-running must replace SD's block, not stack another |
  | remove is an exact inverse of add, after one apply and after three | see the trap below |
  | `AllowUsers` / `DenyUsers` / `AllowGroups` / `DenyGroups` already present is detected | §5.9: do not merge into somebody else's policy |
  | `AllowAgentForwarding` and `#AllowGroups` are **not** detected as policy | a prefix match and a comment would each make the script refuse for no reason |
  | SD's own block is not mistaken for somebody else's | otherwise it refuses to update what it wrote itself |

  **It found a real defect on the first run.** The block ended with a blank
  line for readability, which falls *outside* the markers — so removal left it
  behind and every apply/remove cycle grew the file by a line. Add and remove
  have to be exact inverses; the blank line is gone.

- **`allow-ssh-groups.ps1 -Check` resolves the administrators group by SID.**
  Observed the same session, unelevated: `S-1-5-32-544` resolved to
  `Administrators` on this machine and the script printed the four patterns it
  would write. That is the half that is wrong on a localised Windows if it is
  written as a literal, and it is checkable without touching anything.

- **`sd.iss` compiles with all of the above in it** — `ISCC.exe` exit 0, a
  complete installer built from the tracked script and the existing staged
  tree. That is the *only* claim being made: see §4 Unverified for everything
  about the installer that compiling does not show.

### Not verified — treat as unknown

- **Every OS account operation.** `CREATE.ACCOUNT`, `DELETE.ACCOUNT` and
  `MODIFY.ACCOUNT` have not been run against a real Windows account, and
  cannot be from a normal session (§5.6, elevation). No throwaway OS accounts
  were created. Compiling is not running, and this is the largest untested
  thing added on 14 Aug 2026.
- **RDP refusal, and it CANNOT BE TESTED ON THIS MACHINE.** The last unobserved
  claim in §5.6.2 (§4 Verified covers the rest).
  `SeDenyRemoteInteractiveLogonRight` is confirmed **applied** to `sdsshonly`
  in machine policy, but nothing has watched it refuse a session.

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

  **So the test needs a separate client machine** — §7 step 2. Run
  `verify-sshonly.ps1 -Keep` on the machine under test and RDP to it from a
  different one.

- **`CREATE.ACCOUNT` with `sdsshonly` present.** The verb was run on 14 Aug
  2026 (§4 Verified) but the group did not exist then, so the ssh-only branch
  at `CREATEA` line 400 has still never executed. The group exists now, and
  everything up to the elevation gate is confirmed (§4 Verified) — what
  remains untested is only the privileged half.

  **The test is written and ready: `gplbld/verify-createaccount.ps1`.** It
  needs an elevated window, which is the whole reason it has not run. It
  checks both halves of the account, and then puts the account SD created
  through the same three measurements that proved §5.6.2 — `LogonUser`
  INTERACTIVE refused `1385`, `NETWORK_CLEARTEXT` admitted, and a real ssh
  login with the password SD itself set — so a pass would close the chain end
  to end rather than checking group membership and assuming the rest.

  Note that the branch `stop`s on failure *after* the Windows account and the
  account directory have been created, so a failure there leaves a half-made
  account. The script's cleanup removes the **Windows** half only and leaves
  the `ACCOUNTS` record and the account directory deliberately, because
  removing those is `DELETE.ACCOUNT`'s job and §7 step 1c has not decided what
  that should do.

- **That SD itself works over an ssh session** — `sd -ASOMEACCOUNT` typed at a
  real terminal reached over ssh. The ssh transport is proven and SD is proven,
  but not the two together, and it is also the oldest open question in this
  section: how the MSYS2 tty layer behaves at a real console rather than with
  redirected stdin.

- **`AllowGroups` ACTUALLY APPLIED TO A LIVE `sshd_config`.** Written on
  14 Aug 2026 and its file editing is verified (§4 Verified,
  "`allow-ssh-groups.ps1` edits `sshd_config` correctly"), but the script has
  **never been pointed at `C:\ProgramData\ssh\sshd_config`** — that needs
  elevation, which this session could not obtain. Three things are therefore
  unknown, in descending order of how much they matter:

  1. **Whether the patterns match the right people.** `AllowGroups sdusers
     GITORLI\sdusers Administrators GITORLI\Administrators` is written on the
     reasoning in the script's header; nothing offline can tell you whether
     Win32-OpenSSH's group lookup matches any of those four against a real
     account. **This is the lockout risk**, and it is why the script writes
     both the bare and `COMPUTER\` forms of each group rather than choosing.
  2. Whether `sshd -T` accepts the result on a real config, and whether
     `Restart-Service sshd` comes back.
  3. Whether an `sdsshonly` account — which is in `sdusers`, so it should be
     allowed — can still ssh in afterwards, and whether an account in neither
     group is refused.

  **Test it on the second machine (§7 step 2), not this one**, and keep a
  console session open while you do. `verify-sshonly.ps1 -Keep` leaves an
  account to try it with.

- **The installer's own behaviour with the new options.** `sd.iss` compiles
  (§4 Verified) and that is all. Nobody has seen the reworded closing dialog,
  the `installssh\allowgroups` subtask appear under its parent, or
  `ApplyAllowGroups` report any of its three outcomes. Compiling an Inno script
  proves the Pascal parses, nothing more — and the two defects this file has
  already recorded in that script (the brace bug, the per-file `Check`) both
  compiled perfectly.

- **Whether `OS.EXECUTE` works at all on an installed system.** It almost
  certainly does not — see the shell trap in §6.

- **Typing at SD from a real Windows console.** Everything above was driven
  with redirected stdin, never an actual console, so how the MSYS2 tty layer
  behaves in `conhost` or Windows Terminal — echo, masked input, arrow keys,
  terminfo — is unknown. The scripted-input corruption in §6 says nothing about
  it either way: those are artefacts of how the shells write to a pipe. This is
  the one question that has to be answered by a person at a keyboard, and it
  matters, because it is what "does SD need MSYS2" really turns on.
- Semaphore locking under contention. The semaphores have never been observed
  held, so the `sdsem.c` port is exercised only in the uncontended case.
- `SDConnectLocal()` at runtime. It needs a running server and a configuration
  file (§5.8).
- **Contention.** Two sessions have now coexisted — an interactive one sitting
  at a password prompt on `/dev/pty0` and a second running `LISTU`, which
  listed both (users 8 and 9, 13 Aug 2026). So multi-user attach works. What
  is still untried is two sessions *competing*: record locking between real
  users, and the API server path.
- Writing and reading application data. The bootstrap creates and reads system
  files, and the scratch accounts hold nothing but a VOC.
- **`CREATE.ACCOUNT` on Windows.** JANE and SUE were built by a scratch program
  (§3) precisely because `CREATEA` shells out to `sudo usermod` and `groupadd`.
  The verb itself has never been run here.
- **The installer on a machine with no development tree.** The first-install
  path itself is now verified here (§4 above), so this is no longer "the least
  tested part of the system" — but the accidental-dependency question is
  untouched, and it is precisely how `gplsrc` stayed in the data tree.
  `installsdai.sh` is entirely Linux and is not being ported (§5.9).

  **There is now a specific prediction to test:** a clean machine has no
  `sdadmins` group, so `IsAdmin()` fails closed and `sd -start` should refuse
  with "Command requires administrator privileges". See §8, first item. That is
  deduced from `linuxlb.c` line 75, `sddefs.h` line 131 and `sd.c` line 613
  plus the `IsAdmin()` observation already recorded above — **it has not been
  observed**, because this machine's token carries `sdadmins`.

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

### 5.4 The BASIC layer has its own platform switch (not yet touched)

The C code and the BASIC source in `sdsys/GPL.BP` work together — notably for
compilation — and the BASIC side has a platform abstraction of its own that
nothing has yet been done about.

Two SYSTEM keys are the entire bridge:

| Key | Meaning | State |
|---|---|---|
| `SYSTEM(91)` | "is this Windows" | hardcoded to `0` in `op_sys.c` |
| `SYSTEM(1006)` | "is this Windows NT style" | returns `is_nt`, declared `init(FALSE)` in `kernel.h` and **never assigned anywhere** |

Both say "not Windows", so every Windows path in the BASIC layer is dead code.
`is_nt` is dormant in exactly the way `CASE_INSENSITIVE_FILE_SYSTEM` is.

Flipping them is not a one line change, because this repository's BASIC source
has had its Windows branches removed. Files present in both trees lost all of
it — `LOGIN` 16 references to none, `CONFIG` 5 to none, `CPROC` 5 to none,
`CREATEA` 4 to none, `PARSER` 3 to none. The logic still exists in the external
`GPL.BP` tree and can be recovered from there; what each file did is listed in
the HISTORY entry for 13 Aug 2026, "Surveyed the BASIC layer (GPL.BP)". The one
to start with is `CPROC`'s `dir.separator`, because compilation depends on it
(§6). Note that `LOGIN`'s Windows branch forced administrator rights on any
console session, which §5.6 deliberately does not adopt.

Order matters: restoring the BASIC branches while `SYSTEM(91)` still returns
zero is harmless, but flipping `SYSTEM(91)` first turns on paths that are no
longer there.

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

**SUPERSEDED IN PART ON 14 AUG 2026 — READ 5.6.1 FIRST.** The "SDSYS is the
only administrator" half of this section was reversed by the repository owner
the next day. **A Windows administrator is an SD administrator.** Everything
below about accounts, passwords and the grant list still stands; only the
question of who is an administrator changed. The correction is in 5.6.1 and in
the HISTORY entry for 14 Aug 2026.

Decision from the repository owner on 13 Aug 2026, superseding the `sdadmins`
group model committed earlier the same day in `f56de86`. **SD has no concept of
users, only accounts** — user accounts intended for one person, and group
accounts reachable by many. Authorisation is entirely internal:

- **Every account carries its own password.** Entry is by password prompt,
  whether from `sd -ASDSYS` at the shell or `LOGTO SDSYS` inside SD. This is
  the PICK / UniVerse / OpenQM model. **Still true.**
- **SDSYS is the only administrator.** There is no separate administrator
  account, group or flag. If you know the SDSYS password, you are in.
  **REVERSED — see 5.6.1.**
- **OS groups are dropped from SD's logic entirely.** No `sdadmins`, no
  `sdusers` login gate, no `ACC$GROUP` membership test. **Partly reversed:**
  `sdadmins` is gone for good, but administration is now Windows
  `Administrators`, and `sdusers` remains as the ACL group that grants access
  to the data tree — which was always a file-permission matter rather than an
  SD authorisation one.

This resolved the open question that stood in §8 (should admin status live
inside SD or in an OS group). §5.5 records the Linux privilege model this
replaces, and is retained for background only.

### 5.6.1 A Windows administrator is an SD administrator (decided 14 Aug 2026)

**Decision from the repository owner, 14 Aug 2026**, reversing "SDSYS is the
only administrator" above and settling §8's `IsAdmin()`/`sdadmins` question,
which had become blocking. In the owner's words: if you can log in as an
administrator to the OS, you are an administrator of SD; the installer has to
be an administrator, so the person who installs SD is an SD administrator
without any further step.

**What forced it.** Three separate problems turned out to be one:

1. The installer creates `sdusers` and never `sdadmins`, so a clean machine got
   an install nobody could start (`IsAdmin()` fails closed).
2. The postinstall "set the SDSYS password" step could not work — see the
   defects recorded in §4 — and on this model it is not needed at all.
3. `IsAdmin()` was still the real source of `K$ADMINISTRATOR` despite §5.6
   saying OS groups were gone, so an OS administrator running `sd -internal`
   was already being admitted without a password. The behaviour and the written
   decision had drifted apart; this closes the gap in favour of the behaviour.

**What "administrator" tests, and it is not elevation.** Measured 14 Aug 2026
with a C probe, from an unelevated session belonging to a machine
administrator:

| Call | Source | Contains Administrators? |
|---|---|---|
| `getgroups()` | the process token | **NO** — a UAC-filtered token carries it "deny only", and Cygwin drops it |
| `getgrouplist()` | the account's groups in the SAM | **YES** |

`IsAdmin()` used `getgroups()`, which would have meant "elevated", not
"administrator". It uses `getgrouplist()` now, so an administrator is an SD
administrator in any session, elevated or not — which is what was asked for.

**Test gid 544, never the name.** `getgrnam("Administrators")` resolves to gid
544 and `getgrgid(544)` back to `Administrators`, because Cygwin maps built-in
SIDs to their RID — the same reason `Users` is 545. **`Administrators` is
renamed on a localised Windows**, so the name is not portable and the number
is. `gplbld/sd.iss` already had to learn this for `icacls`, where it writes
`*S-1-5-32-544`.

**Consequences to know.**

- Actions needing an elevated token still fail when unelevated — creating a
  Windows account among them (`CREATE_USER` returns status 5). So an SD
  administrator is not automatically able to do every administrative thing;
  they are able to *administer SD*. §5.7's service model is the real answer.
- **`sdusers` is unaffected and still needed.** It grants file access to
  `C:\ProgramData\SD`, which is an ACL question, not an authorisation one. An
  elevated administrator reaches the tree through the `Administrators` ACE
  without it; everyone else needs the group, and still needs to sign out and
  back in after being added (§6).
- **Normal accounts are standard local accounts.** `CREATE.ACCOUNT USER <name>`
  creates a standard Windows user. Administrators are made deliberately, with
  a keyword — see §7.
- The SDSYS password stops being what confers administration. It still exists
  and still guards the SDSYS *account*, and every account still carries its own
  password; what changes is that knowing it is no longer the definition of
  being an administrator.

**What already exists and can be reused.** The password machinery is present
and wired:

| Piece | Where |
|---|---|
| Salt generation, `SD_SALT` (100) | `op_sdext.c` → `sd_encrypt_sodium.c` |
| Argon2 key derivation, `SD_KEYFROMPW` (101) | `crypto_pwhash`, same file |
| Masked prompt, `IN$PASSWORD` | `_INPUT` |

So salt, derive and compare is available today without new C code.

**Built and working as of 13 Aug 2026** — see §4 for what was observed:

| Piece | Where |
|---|---|
| `$CRED` register, keyed by account, `CRED$SALT` + `CRED$VERIFIER` | `<sysdir>/$CRED`, defines in `INT$KEYS.H` |
| `!CRED_SET(account, password, ok)` | `GPL.BP/CRED_SET` |
| `!CRED_VERIFY(account, password, ok)` | `GPL.BP/CRED_VERIFY` |
| `SET.PASSWORD [account]` verb | `GPL.BP/SET_ACC_PASSWORD` |
| Password prompt at login, 3 attempts | `LOGIN`, `authenticate.account` |
| `ACC$USERS`, the grant list, field 4 of ACCOUNTS | `SYSCOM/KEYS.H`, dictionary item in `gplbld/FILES_DICTS` |
| `LOGTO` grant check | `CPROC`, `logto.authorised` |
| `LOGTO SDSYS` step-up, 3 attempts | `CPROC`, `logto.step.up` |

`LOGIN` sets `@logname` to the authenticated account and sets
`K$ADMINISTRATOR` on entry to SDSYS. Two deliberate ways in without a password,
both gated on `K$ADMINISTRATOR` (which comes from the OS group via `IsAdmin()`
and cannot be self-granted): an administrator running an internal command,
which is the install path since the bootstrap cannot type a password; and an
account with no password yet, with a warning. So a half-configured system is
not an open one.

**How `LOGTO` decides, as built on 13 Aug 2026.** `CPROC`'s `logto.authorised`
runs where the deleted `ACC$GROUP` test used to sit, immediately after the
ACCOUNTS read, and the early `K$ADMINISTRATOR` test at the top of `int.logto`
is gone — it asked whether the caller was already privileged, which is the
wrong question when entering SDSYS is what confers privilege. In order:

0. **The target must be a registered account name.** Anything not in ACCOUNTS
   is refused before authorisation is even considered — see the pathname
   decision below.
1. An administrator running an internal command is admitted, as at `LOGIN`.
   The bootstrap has no terminal to type a password at.
2. **A session standing in SDSYS may enter any account**, no grant needed.
3. Otherwise you may enter your own account, or one whose `ACC$USERS` names
   you. Refusal is `sysmsg(10003)`, "User not allowed in requested account",
   and the session stays where it was.
4. Entering SDSYS additionally runs `logto.step.up`: three tries at **your own**
   password through `!CRED_VERIFY(@logname, ...)`, with `PT$INVERT` and the
   input prompt character cleared around the read (§6). If you have no
   credential of your own, an administrator is warned and admitted, exactly as
   `LOGIN` treats an account with no password.

`@logname` is untouched by any of it. The only assignments to it anywhere are
`LOGIN` 235, `CPROC` 250 and 282 (both initialisation, the second in a branch
that never runs on Windows), and `APISRVR`. Confirmed by observation as well as
by reading — see §4.

**SDSYS reaches every account, without exception (decided 13 Aug 2026).**
Decision from the repository owner, settling the question this raised when the
grant check was first built. Administration that cannot enter an account cannot
repair one, so SDSYS is not subject to the grant list.

The test is **the account you are standing in** (`who`), not the one you logged
in as, so it holds whether you entered SDSYS directly or stepped up into it
from your own identity — and `@logname` still names the person either way, so
what accounts for the access is the audit record, not a refusal. The
consequence to know: stepping *out* of SDSYS into another account puts you in
that account, and you no longer carry the exception. Going from SDSYS to KIM to
JANE is refused at the second move; return to SDSYS first. Getting back in is
never blocked, because SDSYS is your own account by name if you logged in as
it, and a grant plus your own password if you did not.

**`LOGTO` takes an account name and nothing else (decided 13 Aug 2026).**
Decision from the repository owner. It used to treat anything absent from
ACCOUNTS as a pathname to change directory to, which reached an account's
directory without ever consulting its grant list — the hole recorded in §8 when
the grant check landed, now closed by removing the capability rather than by
resolving paths back to accounts. An unregistered directory is not an account.

An unknown account name gives the same refusal as an account that has not
granted you, so the register cannot be probed to discover which names exist.
That does mean a typo reads as "User not allowed in requested account", which
is the same trade `LOGIN` already makes with "Invalid username or password".

`APISRVR`'s `SrvrAccount` took a name **or** a path in the same way and now
takes a name only. Note that nothing else there is gated: once a session is
accepted it reaches any account by name, because the `LOGTO` grant check does
not cover that path.

**Correction (13 Aug 2026): this section used to say the API server "has no
credential model yet".** That is wrong. `APISRVR` line 921 calls
`login(username, password)`, which is a real connect-time check — it simply
**cannot succeed on Windows**, because it reads `/etc/shadow`, which MSYS2 does
not have (§6). So the API is currently closed rather than open. What is
genuinely missing is authorisation *after* connect, and an authentication
mechanism that can work at all. See §7 step 6 and the open question in §8.

**Correction (14 Aug 2026): SD creates and deletes OS accounts after all.**
Decision from the repository owner, reversing "Create no OS users and no OS
groups at all" above and in §5.9. The reasoning was that OS account creation
was Linux baggage; the owner's position is that the *linkage* between an SD
account and an OS user is worth keeping, and that Windows offers the same
thing — `net user`, `net localgroup`, or the PowerShell `*-LocalUser` and
`*-LocalGroup` cmdlets used in the end.

**Read the two halves apart, because conflating them is the easy mistake.**

- **Provisioning is back.** Creating an SD account creates a Windows user;
  deleting one deletes it. Built and compiling, 14 Aug 2026 — see below.
- **Authorisation is still §5.6's.** Every account carries its own password,
  SDSYS is the only administrator, and nothing consults a Windows group to
  decide who may log in. The owner asked for the login gate back "if it is
  possible"; it is now possible, because `IS_GRP_MEMBER` works (below), but
  **it has not been restored** and `LOGIN` is untouched. It is a separate,
  deliberate act — see §7.

The owner's intended shape: the OS-level `sdsys` user is a Windows
administrator, other SD users are standard users, and only `sdsys` can elevate
SD. **Note this pulls against §5.6's "administration is a matter of knowing the
SDSYS password"** — it would make SD administration depend on an OS identity
again, which §5.6 deliberately removed. Not resolved; flagged because the two
statements cannot both be the whole truth.

**What was built, 14 Aug 2026.** All compile clean; none of the account
operations have been *run*, because they cannot be (elevation, below).

| Piece | Where |
|---|---|
| `!create_user` — `New-LocalUser`, created disabled | `GPL.BP/CREATE_USER` |
| `!delete_user` — `Remove-LocalUser`, profile left alone | `GPL.BP/DELETE_USER` |
| `!set_passwd` — prompts in SD, `Set-LocalUser`, enables | `GPL.BP/SET_PASSWD` |
| `!os_group(action, group, member)` — the four group operations | `GPL.BP/OS_GROUP` |
| `!ps_script` — runs a script carrying a secret | `GPL.BP/PS_SCRIPT` |
| `!is_grp_member` — asks Windows, not `/etc/group` | `GPL.BP/IS_GRP_MEMBER` |

**Three things that decide whether any of it works.**

1. **Elevation, and it is not optional.** Creating a local user or changing a
   local group needs an elevated token. An ordinary SD session has a
   UAC-filtered one — measured 14 Aug 2026, `BUILTIN\Administrators` present
   as *"Group used for deny only"*, and `net localgroup sdusers <name> /add`
   answering "System error 5 has occurred. Access is denied." Every one of
   these helpers therefore tests for elevation explicitly and returns status 5
   rather than guessing from a localised error message. **So account creation
   works from the installer, which Inno runs elevated, and not from a normal
   session.** §5.7's service model is the real answer.
2. **`sudo` on Windows is not `sudo` on Linux, and nothing should require
   it.** It is Windows 11 24H2 and later only, so depending on it would
   exclude Windows 10 and Server. It is not needed to install — Inno requests
   elevation through UAC itself — and not needed afterwards either, since
   "Run as administrator" on a terminal gives the same elevated SD session.
   Treat it as a convenience to document, never a prerequisite. `sudo.exe`
   ships on this build (26200), is **disabled by default**, and is enabled
   from Developer Settings; **it was enabled on this machine on 14 Aug 2026
   in inline mode** (`Enabled=3` under
   `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Sudo`). Inline matters:
   the default when enabled is "in a new window", which would break an
   interactive `sudo sd` because the session needs the same console. It has no sudoers file and no per-command policy: it asks UAC to
   elevate *your own* token, so an administrator gets a consent prompt and a
   standard user gets a prompt for administrator credentials. "Only the sdsys
   user can `sudo sd`" is true, but the mechanism is Administrators membership
   and UAC, not a policy file.
3. **`OS.EXECUTE` needs a shell that an installed system does not have** —
   see §6. This is the one that would have bitten silently.

**Passwords never go on a command line.** Decision from the repository owner,
14 Aug 2026, consistent with the reasoning in §8: `net user <name> <password>
/add` exposes the password to any local user through Task Manager,
`Get-CimInstance Win32_Process` or ETW. `!ps_script` writes the script to a
file inside the SDSYS directory instead, runs it and deletes it. The file is
protected by §5.7's ACL inheritance rather than by a permission call of its
own, which is the first practical use of that finding.

**Still to do on this, and the `is_grp_member` note above is now wrong** — it
said the fix was to delete these calls. It is not; they stay:

- **`GPL.BP/CREATEA` still runs `sudo chmod g+s` on the account directory.**
  Guarded, non-fatal, and meaningless on Windows, so it will warn on every
  account creation. Its real equivalent is the inheritable ACE the installer
  sets (§5.7) — remove it with the ACL step, not before.
- **Nothing has been run.** No Windows account has been created, no group
  changed. `sudo` is disabled on this machine and no throwaway OS accounts
  were made without the owner's say-so.

**What is still missing.**

- **The audit records.** Nothing is written yet for a login, a `LOGTO` or a
  failed step-up, which is the remaining half of this model and now the first
  item in §7. Until it lands, the grant check controls access but leaves no
  trace of who used it — and attribution, not access control, is what this
  model is for.
- **There is no verb for managing grants.** `ACC$USERS` has a dictionary entry
  so `LIST ACCOUNTS` shows it and `MODIFY ACCOUNTS` can edit it, which is what
  the 0.6.4 changelog assumed, but nothing offers `GRANT`/`REVOKE`. The scratch
  `BP/GRANT` on this machine is a stand-in, not a design.

- **`$CRED` must stay a separate file from ACCOUNTS**, which eleven programs
  open before any authentication. Reasoning in HISTORY, as above.
- `ACC$GROUP` is dead but still populated on old records, and `LIST ACCOUNTS`
  still shows it. Remove it with the OS account commands, as one change.
**Built and verified, listed here only because the detail still matters.**
Administrator rights are the SDSYS account's alone — `LOGIN` sets `USR_ADMIN`
on entry to SDSYS and clears it entering anything else, `CPROC` does the same
on every `LOGTO`. Only an `$internal` program may set the flag and only SDSYS
may compile one; `sd -INTERNAL` means SDSYS and asks for its password. Privilege
tests ask the flag, not the uid: use `kernel(K$ADMINISTRATOR, -1)` in an
`$internal` program and `SYSTEM(1050)` anywhere else (§6). `kernel.c` still
seeds the flag from `IsAdmin()` at process start, which now decides only
whether a credential-less account can be entered during a fresh install (§8).

**Still to do, and these are the ones that bite.**

- The `is_grp_member` calls in `CREATEA` (line 323) and `MODIFYA` (96, 99, 125)
  were left where the others were deleted: they guard `OS.EXECUTE` calls to
  `useradd`, `usermod` and `groupadd`, and removing only the guard would let
  those shell-outs run unconditionally. They go when the OS account commands
  go, as one change — together with the `OS.EXECUTE` account commands in
  `CREATE_USER`, `SET_PASSWD`, `CREATEA`, `DELACC` and `MODIFYA`, which under
  this model manage SD accounts and touch no OS account at all.
- `CPROC`'s `system(27) = 0` "entered as root?" branch at line 272 was left
  alone. It guards `EUID_SET`, which has no Windows equivalent (§5.5), and its
  `kernel(K$ADMINISTRATOR, 1)` is now redundant.

**The model in one paragraph.** A person logs in as **themselves**, then moves.
Access to other accounts is **granted, not shared**, so there is no second
password to know and none to rotate; `@logname` does not change on `LOGTO`, so
everything downstream attributes to whoever authenticated; and every login and
`LOGTO` is logged. `LOGTO SDSYS` re-prompts — the one exception to "granted,
not prompted" — and **asks for the caller's own password, not an SDSYS one**,
which is easy to get backwards and is the whole point: an SDSYS password would
be a second shared secret held by every administrator, which is the OpenQM
weakness this exists to remove. The full reasoning, including why the
credential register is a separate file from ACCOUNTS, was moved to HISTORY on
13 Aug 2026 — "Moved from PROJECT_STATUS §5.6".


Attribution is SD-internal and does **not** depend on the service model in
§5.7, so it lands with the password work. It records who authenticated, not who
is at the keyboard — accountability, not proof of identity.

**The audit log must not be the existing `errlog`.** The `LOGMSG` verb reaches
`log_message()` in `k_error.c`, which writes to `<sysdir>/errlog` and, when the
file reaches the `ERRLOG` configured size, **discards the oldest half**. That is
correct for a diagnostic log and disqualifying for an audit trail, which must
not lose records silently. Write the audit trail to its own file, append-only,
and rotate rather than truncate.

`ACCOUNTS` needs the grants. Record them **on the target account** — JANE lists
who may enter JANE — rather than as a list of destinations on the source. It
answers the question administration actually asks ("who can get into JANE?"),
and revocation happens in one place. Note `$LOGINS` chose the other direction,
`LGN$VALID.ACCOUNTS` and `LGN$BANNED.ACCOUNTS` on each user; that register is
gone (§6) and there is no reason to inherit its shape.

Watch that `CPROC` currently reassigns `logname` when it drops to `sdsys`
(around line 278). Under this model nothing may overwrite the login identity.

**Understand the security consequence before relying on this.** A password
gate inside SD is not a file security boundary — see §5.7.

### 5.6.2 SD accounts are ssh-only; the console belongs to administrators (decided 14 Aug 2026)

**VERIFIED 14 Aug 2026, except RDP** — see §4 Verified, "THE SSH-ONLY MODEL
WORKS", and re-run it with `gplbld/verify-sshonly.ps1`. The risk named below,
that denying the wrong right locks everybody out, was the thing tested and it
did not happen. Everything else in this section is reasoning that still stands
on its own; read it before changing any of it.

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
non-administrator account it creates to a dedicated group, and the deny rights
are applied to that group a single time by the installer. The alternative —
granting the rights per account as it is created — was rejected:

- There is **no PowerShell cmdlet for account rights** (measured 14 Aug 2026:
  `Get-Command *AccountRight*` returns nothing), so each grant means either
  `LsaAddAccountRights` through P/Invoke or a `secedit` export-edit-import.
  Doing that per account puts a fiddly, elevation-dependent step on the hot
  path of every account creation.
- `secedit` is a **read-modify-write of the entire USER_RIGHTS area**, so
  running it per account rewrites machine policy repeatedly and races anything
  else editing it.
- A group is **inspectable**. "Who is confined to ssh?" is answered by looking
  at one group's membership, rather than by reading policy through `secpol.msc`
  one right at a time.
- And SD already knows how to do it: `!os_group("ADDMEM", ...)` is written,
  tested and used (§4).

**It cannot be `sdusers`.** That group grants access to the data *files* and
administrators are in it too, so denying console logon to `sdusers` would lock
administrators out of their own console. The two groups answer different
questions and must stay separate — the same distinction §5.6.1 draws between
`sdusers` and `Administrators`.

**`AllowGroups` in `sshd_config` is the second layer**, suggested by the
repository owner. The deny rights stop local logon; `AllowGroups` decides who
may ssh at all. Two independent controls rather than one. Two cautions: it
means writing to `C:\ProgramData\ssh\sshd_config`, a file SD does not own and
which may be managed by policy — §5.9 already forbids reconfiguring an ssh
server SD did not install — and the list **must include administrators**, or
the machine's own administrator loses ssh. That makes it an installer offer,
not something a verb should do silently.

**Written 14 Aug 2026, fourth session, and not yet applied to a live config**
— §7 step 0a, and §4 Unverified for what that leaves open. How the two cautions
are answered, since changing either one re-opens them:

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
`connection_type` (`CN_CONSOLE`, `CN_SOCKET`, `CN_PIPE`) describes only the
terminal transport; there is no data server. So any ACL strong enough to stop a
user reading the files in Explorer also stops SD reading them on that user's
behalf. **While SD runs as the invoking user, account passwords organise
access; they do not secure it.**

**This is what decides whether accounts are private from each other.** For a
user to enter account B, their Windows token must have read and write on B's
directory, because their own process does the I/O. The OS cannot distinguish
"entered with the right password" from "opened in Explorer" — it is the same
token either way. So in stage 1 there are only two options, and neither is what
was wanted: grant every SD user access to every account directory, which gives
no protection between accounts at all; or set per-user ACLs per account
directory, which is OS-level authorisation duplicating the password gate,
reintroducing exactly what §5.6 removed and adding a Windows-user-to-account
mapping to maintain.

Under the service model the question dissolves: no end user holds any file
access, SD is the only reader, and SD checks the password. Accounts become
private from each other *because* of the password rather than in spite of it,
and shared accounts still work, because the OS never sees individual people at
the file layer.

What is achievable now, and what is not:

- **Achievable in stage 1.** Lock the tree to a single identity plus
  `Administrators`, so no other account on the machine can browse it. This
  blocks everyone who is not an SD user. It does not stop an SD user reading
  another account's files directly, since SD runs as them.
- **The real answer, and it is stage 2.** `sdwind` becomes a Windows service
  running as a dedicated service account — a virtual account, `NT SERVICE\SD`,
  needs no password management — which owns the tree exclusively. Session
  processes are spawned under the *service* identity, not the user's, and the
  user reaches their session over the named pipe. The user's own token never
  touches the data. This is the direct Windows equivalent of the Linux original
  dropping to the `sdsys` user via `EUID_SET` (§5.5); it is not a Windows
  novelty. It requires console `sd.exe` to become a client of the service
  rather than doing its own file I/O, which is the substantial part.

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

**What this has to deliver, from the repository owner (13 Aug 2026).** Three
requirements, and two of them already hold:

1. **SD's home is under `C:\Program Files`.** Not done.
2. **The user can start the SD login from any directory.** Already true —
   `sd -ASUE` run from `C:\Windows` logged in normally. What it needs is for
   `sd.exe` to be found and to load the right DLLs, which is why they ship
   beside it (below) rather than being hunted for on PATH.
3. **On login the current directory is the account's directory**, as on Linux.
   Already true: `LOGIN` does `ospath(acc.path, OS$CD)` and sets `@PATH` from
   the result. Logging in as SUE from `C:\Windows` reported
   `PATH=/home/sd/user_accounts/SUE`. Nothing to build, but do not break it —
   it is what makes an account feel like a place rather than a setting.

`ProgramData` is the correct home for machine-wide mutable state, and it has no
space in its name, which sidesteps the `VALID_OS_PATH` trap (§6) for a default
install. `Program Files` does contain a space, so binaries are on the wrong
side of that trap and it must be fixed regardless.

**Ship the MSYS2 DLLs beside `sd.exe` in `C:\Program Files\SD\`.** Windows
searches the executable's own directory before PATH, so this removes both PATH
problems found on 13 Aug 2026 (§6): the exit-53-with-no-message when
`libsodium-26.dll` is missing, and — much worse — Git for Windows's rival
`msys-2.0.dll` being picked up, which makes SD report "SD has not been started"
while it is running. Relying on PATH order is not a supportable install.

Moving off `/usr/local/sdsys` matters on its own merits: it currently resolves
to `C:\msys64\usr\local\sdsys`, inside the MSYS2 install tree, so reinstalling
MSYS2 destroys the database.

**Current state is worse than just the Unix paths — the server and client do
not agree on how to find the configuration:**

**Settled 14 Aug 2026.** Both now read `SD_CONFIG` and both fall back to
`%ProgramData%\SD\sd.conf`, with `C:\ProgramData\SD\sd.conf` as the last
resort if the variable is missing. `SCARLET_CONFIG` is gone — it named a
project this is no longer part of — and so is the `sd.ini`-in-`C:\Windows`
fallback. The two values live in `SD_CONFIG_ENV` and `SD_CONFIG_DEFAULT` in
`gplsrc/sddefs.h`, and are duplicated in `sdclilib.c` because the client is a
separate toolchain that must not include the server's headers (§5.2); change
both together. What it used to be:

| | Environment variable | Fallback |
|---|---|---|
| Server, `GetConfigPath()` in `inipath.c` | `SCARLET_CONFIG` | `/etc/sd.conf` |
| Client, `sysdir()` in `sdclilib/sdclilib.c` | `SD_CONFIG` | `sd.ini` in the Windows directory |

The client's comment claims `SD_CONFIG` matches the server. It does not — the
server reads `SCARLET_CONFIG`. Unify on one variable and one file. Also drop
the `sd.ini`-in-`C:\Windows` fallback: writing there has required
administrator rights since Vista and it is 16-bit-era practice.
`sdnet.h` additionally hardcodes `PASSWD_FILE_NAME "/etc/shadow"`.

**The accounts moved on 13 Aug 2026, and drive letters work now.** Decision
from the repository owner: SD accounts live under `C:\ProgramData\SD\`, beside
the rest of the data. `/home/sd` was the right place while an SD account was an
operating system user; under §5.6 it is not one, so the Linux location decided
nothing. `USRDIR` and `GRPDIR` in `sd.conf` carry it, and the compiled defaults
in `config.c` match.

**`sdrealpath()` was the blocker, and it is fixed** (13 Aug 2026). It treated
anything not starting with `/` as *relative* and glued the working directory in
front, and never treated `\` as a separator, so `C:\ProgramData\SD` became
`/usr/local/sdsys/C:\ProgramData\SD` and every open failed with ER_FNF naming
nothing near the cause. It now folds backslashes and treats a leading drive
letter as the root; all five spellings open the same file (§4). `DS` is still
`/` — this changed what SD **accepts**, not what it produces. The earlier claim
that stage 1 could simply keep forward slashes was wrong; see the HISTORY entry
"Accounts move to ProgramData, and SD learns to read a Windows path".

Two consequences worth carrying forward:

- **The rest of the move is now much less risky.** `SDSYS=C:\ProgramData\SD\sdsys`
  and binaries under `C:\Program Files\SD\` were blocked by exactly this, and
  are not any more.
- **Stored and displayed paths still come out half POSIX.** `CREATEA` joins
  `CONFIG('USRDIR')` to the account name with `@ds`, which is `/`, so the
  ACCOUNTS record reads `C:\ProgramData\SD\user_accounts/PAT`; and `@PATH`
  comes from `ospath("", OS$CWD)`, which is `getcwd()` and always POSIX, so it
  reports `/c/ProgramData/SD/user_accounts/PAT`. Both work. Both are tidied by
  the `@ds` / `dir.separator` question (§6), which is now **testable** for the
  first time, since a `\` separator no longer breaks path resolution.

### 5.9 One installer: a staging script, then Inno Setup (decided 13 Aug 2026)

**Revised twice on 13 Aug 2026; this is the current decision and it reverses
the middle one.** The `installsdai.sh` port is **dropped**. Two scripts replace
it: one that builds a **staging directory** holding exactly what an install
consists of, and one that turns that directory into an **Inno Setup
installer**. Neither the shell installer nor `deletesdai.sh` gets ported.

The three positions in order, so the change is legible: go straight to Inno →
no, do the Linux method on Windows first, since `installsdai.sh` is
apt/dnf/zypper, systemd, xinetd and `/etc` throughout → no, skip it. The
reasoning is in the HISTORY entry for 13 Aug 2026, "Installer: the shell script
port is dropped".

**Why the Linux script existed, and why that reason does not transfer.** This
is the part worth understanding before anyone proposes porting it again.
`installsdai.sh` was not a developer convenience — it was load-bearing.
ScarletDME targeted Fedora, Debian, Arch and OpenSUSE across several versions
each, every one with its own compiler, libc and package names. No single binary
works across that, so **the end user had to compile**, and the script existed to
abstract apt from dnf from pacman from zypper and drive a build on the user's
own machine.

Windows has none of that. One target, one ABI, and SD ships its own runtime
beside `sd.exe` (§5.8), so there is nothing to adapt to and the user needs no
compiler at all. The requirement that made the script necessary on Linux simply
does not exist here — which is why what is left of it, once the distro handling
is stripped out, is a developer setup tool that §2 and §3 already cover. Note
this makes the Windows install genuinely *simpler* than the Linux original,
which is not true of much else in this port.

**The staging script is the valuable half**, and not mainly because of
packaging:

- **It makes §5.8 executable.** The install layout is prose here; a staging
  script is that layout in a form that either runs or does not. It is what
  forces the `<sysdir>/bin` split (§6) to be decided rather than remembered.
- **It is a whitelist, and whitelists find accidental dependencies.** This is
  the strongest argument for it. `gplsrc` sat in the data tree for as long as
  it did because `installsdai.sh` copied it wholesale and nobody asked why —
  a fault that cost most of a session on 13 Aug 2026. A script that copies
  only what is on a list, installed on a machine with no development tree,
  surfaces that class of thing at once. The installer is the least tested part
  of this system (§4); making it cheap to rerun is what changes that.
- **It is where the DLL closure is computed, not guessed.** §5.8 requires the
  MSYS2 DLLs beside `sd.exe`. Which ones — `msys-2.0.dll`, `libsodium-26.dll`,
  and whatever python, intl, bsd and crypt pull in — must be **derived by
  walking the imports**, because missing one gives exit code 53 and no message
  at all (§6). Python in `gplbld/`, beside `bbcmp.py`, `pcode_bld.py` and
  `gen_includes.py`, is the natural home.

**Inno Setup then packages the staged directory.** It stages *pre-compiled*
artefacts rather than building on the target, which is what an end user should
get, and it collides with §5.11 only in appearance: the staged artefacts are
release artefacts built elsewhere, not tracked files. The `.iss` script does
belong in this repository. **Correction to what this section said before: the
Inno Setup compiler is installed on this machine** — it was recorded as absent.

**`deletesdai.sh` is not ported, but read it before writing the uninstaller.**
Inno gives you an uninstaller for free; it does not answer the question that
matters. `C:\ProgramData\SD\` holds the user's database. Removing it on
uninstall is a catastrophe, and leaving it makes reinstall awkward because
accounts and `$CRED` are already there. Decide deliberately; the old script is
where the current answer is written down.

What the installer is responsible for, given §5.6 to §5.8:

- Lay down `C:\Program Files\SD\` and `C:\ProgramData\SD\`.
- Set the ACLs on the data tree with `icacls`, breaking inheritance first
  (§5.7). This is the step that makes the data private, and nothing SD does at
  runtime can substitute for it.
- Prompt for the initial SDSYS password and write the salt and verifier into
  the ACCOUNTS record.
- Create no OS users and no OS groups at all (§5.6).
- Register the service, once §5.7's service model exists.
- Run the BASIC bootstrap sequence in §3.

Inno Setup is a separate toolchain and is not part of `make`. **The compiler
is installed on this machine**, at `C:\Program Files (x86)\Inno Setup 6\nISCC.exe`, confirmed 14 Aug 2026. Still to decide: whether CI produces the
installer. What the uninstaller does is settled below.

**Optional OpenSSH Server, opt in and off by default (decided 14 Aug 2026).**
Decision from the repository owner. The case for offering it at all: SD will
often be installed by someone with little administrative knowledge who wants
the ten people on their local network to reach it. Good security is the
default; the easy path exists but has to be chosen.

Note the Linux script did this unconditionally — `installsdai.sh` installs
`openssh`/`openssh-server` on all four distributions and, on Arch, runs
`systemctl start sshd` and `systemctl enable sshd` (lines 254-295). It sat in
the same package list as `git`, `gcc` and `python3-dev`, because the Linux end
user had to compile. That reason is gone on Windows, so the behaviour is not
inherited — it is re-decided, and the standing rule that the installer outranks
Linux parity is what permits the difference.

Requirements:

- **Unchecked by default**, and clearly worded: it starts a service listening
  on port 22 and adds a firewall rule, which grants remote shell access to the
  whole machine, not just to SD.
- **If OpenSSH Server is already present, say so and do not offer the option.**
  Detect it without needing elevation — `%SystemRoot%\System32\OpenSSH\sshd.exe`
  on disk, or an `sshd` service registered. Note
  `Get-WindowsCapability -Online` **requires elevation** (measured
  14 Aug 2026), which Inno has and a plain query does not, so prefer the file
  or service test. Never silently reconfigure or restart an ssh server the
  machine already has: it may be there for something else and may be managed
  by policy.
- **A failure to install it must not fail the SD install.** It is a Windows
  optional capability fetched from Features on Demand, and that can be blocked
  by policy, by a metered connection or by an offline machine. Report it and
  carry on.

  **And it is SLOW, which was not anticipated and is worse than a failure.**
  Measured 14 Aug 2026: with the capability `NotPresent`, `Add-WindowsCapability`
  downloads and hands off to `TiWorker`, which worked for minutes, grew its
  working set by 16 MB in a 4-second sample, and left **`RebootPending` set to
  True**. The `[Run]` entry is `runhidden` with no progress, so the wizard sits
  on "Installing OpenSSH Server..." saying nothing, and it reads as a hang —
  it was reported as one during testing. Three consequences to design around
  before this ships:

  - **Say it will take minutes** on the tasks page, next to the checkbox.
  - **Never kill it.** Interrupting `TiWorker` mid-servicing is how the
    component store gets corrupted. A terminated run leaves the capability
    half-applied and a reboot pending, which is what happened here.
  - **The reboot is real.** SD itself needs none, so an installer that quietly
    creates a pending reboot because of an optional extra should say so.
- **The uninstaller must not remove it**, for the same reason it must not
  remove the database: it may predate SD or be in use by something else.

**Two consequences of the ten-users-over-ssh case worth being honest about.**

- Each of those people needs a **Windows account on the machine** to ssh in
  and run `sd`. That is precisely what the OS account provisioning restored on
  14 Aug 2026 makes manageable (§5.6) — `CREATE.ACCOUNT` makes the Windows user
  alongside the SD account. The two decisions fit together, which was not
  planned.
- **It does not give those ten people isolation from each other's data**, and
  will not until §5.7's service model lands. Every SD process opens the
  database under the invoking user's own token, so all ten need file access to
  the tree and can read each other's account directories outside SD. The
  account passwords organise access; they do not secure it. Anyone deploying
  this way for casual use should be told that plainly.

### 5.9.1 What the uninstaller does (decided 14 Aug 2026)

Decision from the repository owner, settling the question §5.9 raised.

**Yes, it is the standard Windows uninstall.** Inno registers under
`HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall`, so SD appears in
Settings > Apps and in Control Panel > Programs and Features, and `unins000.exe`
is what both of them run. Nothing has to be built for that.

**The default must not touch accounts, the database or the configuration.**
Most of this comes free and one part does not:

- **The data is safe by default without doing anything.** Inno removes only
  the files it installed, from its own log, and removes a directory only if it
  is empty. Everything the bootstrap and the running system create afterwards —
  `VOC`, `ACCOUNTS`, `$CRED`, the accounts under `user_accounts`, `errlog` — is
  invisible to it.
- **`sd.conf` is the exception and needs handling**, because the installer
  *does* install it, so Inno would remove it like any other installed file.
  Mark it `uninsneveruninstall`, and `onlyifdoesntexist` as well so that
  reinstalling or upgrading does not overwrite settings the user has edited.
- **Pre-bootstrapping widens this.** The staged tree now ships a populated
  `gcat`, `GPL.BP.OUT` and so on, so those *are* installed files and Inno will
  remove them. That is correct — they are program, not data — but it means the
  boundary between "shipped" and "user's" now runs through the middle of
  `C:\ProgramData\SD\sdsys`, and anything added to the ship list has to be
  looked at with the uninstaller in mind.

**Removing the data is a separate, opt-in choice.** Inno can ask during
uninstall from `[Code]`, and the answer must default to keeping the data. Two
conditions: the prompt must say exactly what it destroys and where
(`C:\ProgramData\SD\`, every account and every password), and a **silent
uninstall must never delete it** — an unattended removal that takes the
database with it is the worst possible default.

`deletesdai.sh` is still worth reading before writing this, as §5.9 says, but
it is not the model: it is a Linux script for a Linux layout and the decision
above is not the one it made.


**This is a hobby project with no release schedule and no architecture
document to satisfy.** That is context worth having when weighing "do it
properly" against "do it now": the answer here is usually to do the thing that
keeps development moving and record honestly what it does not yet do. The two
handoff files and the changelog are the only process there is.

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

Consequences to carry into the installer work (§5.9):

- **Installing now means building** — but only for whoever runs the staging
  script, which is the point of it (§5.9). `installsdai.sh` does `cp -R bin
  "$sdsysdir"` and tests for `bin/sd`, both of which assumed a clone already
  contained the binaries; that is one of the reasons it is not being ported.
  The end user gets the Inno Setup installer and needs neither a clone nor a
  toolchain.
- The eight files removed from tracking — `sd.exe`, `sdconv.exe`, `sdfix.exe`,
  `sdidx.exe`, `sdwind.exe`, `sdtic.exe`, `sdclilib.dll`, `libsdclilib.dll.a` —
  are still produced by `make sd` and still needed at runtime. They were
  untracked, not deleted.
- **History was rewritten on 13 Aug 2026 to purge them**, so nothing binary
  exists anywhere in the repository, past or present — verified by walking
  every object for NUL bytes. **Every commit hash changed**; the mapping and
  what else it removed are in the HISTORY entry "History rewritten to purge
  every binary". The install recompiles I-types, so dictionary items carry
  source and checksum only; if a `FILES_DICTS` item ever regains a compiled
  tail, strip it.

### 5.12 Lower case everywhere it can be (decided 13 Aug 2026)

Goal from the repository owner on 13 Aug 2026. **Everything that can be lower
case should be lower case.** SD is inconsistent about it today — BASIC source
is free-form and usually written in lower case, while file names, field names
and account names are forced up. The end state is lower case throughout, with
existing upper-case code converted rather than tolerated.

Not started, and it is a wide change rather than a deep one. What is known to
force case up today, from work already done:

- **Account names.** `KEYS.H` says "Id = account name (forced to uppercase)",
  and `LOGIN`, `CPROC` and the credential helpers all `upcase()` on the way in.
  The `$CRED` register is keyed the same way, which is why account names are
  case insensitive at login.
- **The terminal itself.** `LOGIN` sets `pterm(PT$INVERT, @true)`, so typed
  input is case-inverted: type `SUE` and the prompt echoes `sue`. This is the
  visible half of the trap in §6 that silently upcased a password.
- Dictionary and VOC item ids, which are conventionally upper case throughout
  `NEWVOC` and `FILES_DICTS`.

Sequencing matters. Case insensitivity of *comparison* is what makes the
current upcasing harmless; removing the upcasing without making the
comparisons case insensitive would make `sue` and `SUE` different accounts.
`CASE_INSENSITIVE_FILE_SYSTEM` (§7) is the file-name half of the same problem
and is already written but never defined, so the two belong together.

### 5.13 Shell access is restored, not blocked (decided 13 Aug 2026)

Correction from the repository owner on 13 Aug 2026: disabling the user's
ability to shell out with `SH` or `!` in the Linux version **was a mistake**,
and Windows makes it a worse one. Many programs have to reach Windows
utilities, and there is no way to do that with shell access blocked.

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

Recording it here because it changes how several things on the §7 list should
be built, and it is cheaper to know that before writing them than after:

- **The grants verb** (§7 step 5) is the clearest case. `ACC$USERS` is edited
  through `MODIFY ACCOUNTS` today. Whatever shape it takes — `GRANT`/`REVOKE`
  or a `SET.ACCESS` screen — a form is the destination, so put the work in a
  subroutine the form can call rather than in the verb itself.
- **The batch allowlist** (§8) is the same: `ED VOC ALLOWED` is workable and a
  form is better, particularly as it is the one place that has to enforce the
  no-arguments and VOC-type rules recorded there.
- **`SET.PASSWORD`** already exists and is prompt-driven, which is the right
  precedent.

The general rule that follows: **new administrative capability goes in a
subroutine with a verb over it**, not in a verb that holds the logic. A form
added later then calls the same subroutine instead of reimplementing it or
shelling out to the verb. `GPL.BP/CRED_SET` and `CRED_VERIFY` with
`SET_ACC_PASSWORD` over them are the pattern to copy.

### 5.15 Embedded Python is dropped; the API is the point (decided 13 Aug 2026)

Decision from the repository owner on 13 Aug 2026, and it is a **statement
about what SD for Windows is for**, not just a packaging choice: the intended
user is a Windows developer using SD as a **back end data store, reached
through the API**. Embedded Python was not part of that, so it is gone rather
than shipped unused.

Removed outright rather than left behind an `#ifdef`, the same reasoning as the
Linux code in §1 — and two of the files could not have stayed anyway, being
unguarded and listed in `gpl.src`. The C sources, the Makefile flags, 20
`GPL.BP/PY_*` programs, `SYSCOM/SDPYFUNC.H`, the `SD_Py*` error codes and the
SDEXT keys all went; the itemised list is in the HISTORY entry "Embedded Python
removed".

**Three consequences worth carrying forward.**

- **Two build dependencies disappear, not one.** `python-devel` obviously, and
  `gettext-devel` because it was only ever needed to satisfy the `-lintl` that
  `python3-config --ldflags --embed` emits (§2). Plain `python` is still
  needed by `gplbld/`, for the developer only.
- **The install gets much smaller and one open question closes.**
  `msys-python3.12.dll` leaves the DLL closure, and with it the unresolved
  question of whether to ship the 195 MB Python standard library — which
  `gplbld/stage.py` was warning about. There is nothing to decide any more.
- **It reorders §7.** If the API is the primary interface then step 6, bringing
  `APISRVR` under the identity model, and exercising `SDConnectLocal()` are
  more important than their positions suggest. `APISRVR` currently has **no
  credential check of its own** (§5.6), which matters a great deal more for a
  product whose main door is the API than for one where it is a side entrance.
  Not reordered yet — flagged, because it is the repository owner's call.

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

**What "Inno compatible" actually requires.** In dependency order, and most of
it is already decided rather than done:

1. **No dependency on a shell that Windows does not ship.** **Done**,
   14 Aug 2026 — see §6. This was the one that would have shipped broken.
2. **The layout move** (§5.8, §7 step 1). Inno installs to
   `C:\Program Files\SD\usr\bin\` and `C:\ProgramData\SD\`; `gplbld/stage.py`
   already builds exactly that. Not done in the live tree.
3. **One configuration file, found without an environment variable — DONE,
   14 Aug 2026.** Both server and client read `SD_CONFIG` and fall back to
   `%ProgramData%\SD\sd.conf`. Verified with nothing set in the environment
   (§4). See §5.8.
4. **Pre-bootstrap the staged tree — DONE, 14 Aug 2026.**
   `gplbld/stage.py --bootstrap` runs `gplbld/bootstrap.py` against the staged
   tree and ships the result, so installing is a file copy. Verified end to
   end (§4). The rest of this item is the reasoning, kept because it is why
   the shape is what it is.

   The staged tree was **not installable at all** before this.

   **What the end user needs, and this is the question worth being exact
   about.** A C compiler: **never**. The installer ships pre-built binaries
   and SD carries its own runtime DLLs beside `sd.exe` (§5.9, §5.11) — that is
   the whole difference from Linux, where `installsdai.sh` compiled on the
   user's machine because ScarletDME targeted many distributions. Python:
   **yes as things stand, and that is a defect rather than a requirement.**
   `SDSYS_EMPTY` stages `gcat`, `cat`, `GPL.BP.OUT`, `BP.OUT` and `PCODE.OUT`
   empty, so the target must run the bootstrap in §3, and two of its steps are
   `gplbld/bbcmp.py` and `gplbld/pcode_bld.py`.

   **And it could not run even then, because `gplbld/` is not staged at all.**
   It is absent from `SDSYS_SHIP`, so `bbcmp.py`, `pcode_bld.py` and the
   `FILES_DICTS` that `WRITE_INSTALL_DICTS` reads as
   `@sdsys:"/gplbld/FILES_DICTS"` are all missing from the staged tree. So an
   install from it fails today whatever is installed on the target. This is
   precisely the class of thing §5.9 predicted the whitelist would expose, and
   §4's "the installer is the least tested part of the system" is why it was
   not noticed sooner.

   Rule 2 above decides the fix: run the bootstrap on the build machine at the
   production path and ship the filled directories, so installing is a file
   copy and the end user needs **neither Python nor a compiler**. The cost is
   that the data tree's location becomes fixed, and only `ACCOUNTS/SDSYS`
   embeds it. The alternative — staging `gplbld/` and requiring Python on
   every target — is worse on both counts and contradicts §7 step 1's
   "the data tree holds data only".
5. **`icacls` on `C:\ProgramData\SD\`**, breaking inheritance first (§5.7).
   This is the step that makes the data private; nothing at runtime
   substitutes for it.
6. **Prompt for the SDSYS password and set it last** (§7 step 3), after the
   bootstrap, since `LOGIN` admits an administrator to an account with no
   verifier yet.
7. **Decide what the uninstaller does with `C:\ProgramData\SD\`** before
   shipping one (§5.9). It holds the user's database.

**Elevation is a point in the installer's favour, not against it.** Inno runs
elevated, which is exactly what the OS account commands need (§5.6). So
creating the initial accounts is something the installer can do and a normal
session cannot.

## 6. Traps

Each of these cost real time. Read before debugging anything similar.

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
  authenticate ANY account.** Found 14 Aug 2026, while trying to find out why
  a login was refused. sshd must run as **SYSTEM** to build a user token:

  ```
  debug1: get_user_token - unable to generate user token for <name>
          as i am not running as system
  ga_init, unable to resolve user <name>
  ```

  It fails at `mm_answer_pwnamallow`, before authentication is attempted, and
  the DEBUG3 log therefore looks exactly like a total authentication failure
  that has nothing to do with what is being tested. Elevation is not enough
  and there is no flag for it.

  **Read the installed service's reasons instead** — it runs as SYSTEM, and it
  logs to the `OpenSSH/Operational` event log:

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

  **It failed in complete silence and had done so on every install.** The entry
  has `skipifdoesntexist` and checks no exit code, deliberately, because §5.9
  says a failed ssh install must not fail the SD install. So ticking the box
  produced no `sshd.exe`, no service, nothing on port 22, and no message
  anywhere. Only reading the *expanded* parameters in the install log shows it.

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
  silently.** `sysseg.c` execed `"%s/bin/sdlnxd"` built from
  `sysseg->sysdir`, and the daemon's own `check_lost_users()` built
  `'<sysdir>/bin/sd' -cleanup` the same way. Both were right while the Linux
  install kept executables and the pcode library in one
  `/usr/local/sdsys/bin`. §5.8 split them — binaries to
  `C:\Program Files\SD\usr\bin`, `pcode` and `pcode.old` staying with SDSYS
  (see "two unrelated things in one directory" below) — and neither call site
  moved. **So the daemon never started on an installed system**, and nothing
  said so: the `execl` sits in a forked child that has already `daemon()`ed, so
  there was no message anywhere and `sd -start` still reported success.
  `sdwind_pid` stayed at -1, which is exactly the value meaning "failed to
  start", so `sd -stop` correctly skipped it and even that looked normal.

  **The symptom is an absence**, which is the hard kind to notice: SD works
  completely — shared segment, `COUNT VOC`, `WHO`, everything — because none of
  it needs the daemon. Only looking for the process shows it.

  It **worked perfectly in development**, where `<sysdir>/bin` really does hold
  the executables, which is why 13 Aug 2026 recorded the daemon starting and
  staying up and why nothing contradicted that until there was an install to
  test. Same family as the `/bin/bash` trap above.

  **Two lessons, both general.** When anything moves between the development
  and installed trees, **grep the C for the old location** — the compiler
  cannot help, because these are runtime strings. And **a forked child that
  fails must `_exit()`, not `return`**: returning put it back into the
  caller's code as a duplicate process, which is what made this produce no
  symptom at all. Both call sites now resolve against `exe_directory()`
  (`exepath.c`), so the launcher and the launched stay together by
  construction.

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
  `etcstab` maps `/dev/shm` there, the first thing to fail is semaphore
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
  `OS.EXECUTE` ran `/bin/bash -c`, and an installed system has no bash.
  Found while porting the OS account commands, and it was not
  caused by them — it is true of every `OS.EXECUTE` in the system today.
  `op_sh.c` line 179 defaults to `/bin/bash -c`; `gplbld/stage.py` ships the
  six SD executables, the client DLL and the computed MSYS2 DLL closure, and
  **no shell at all**. On an installed tree the POSIX root is
  `C:\Program Files\SD\` (the two-component rule below), so `/bin/bash`
  resolves to `C:\Program Files\SD\bin\bash.exe`, which does not exist. Every
  `OS.EXECUTE` fails, and it will fail on the *installed* system while working
  perfectly in development, where MSYS2's own bash is present.

  This matters beyond the account commands: it is also the whole of §7 step 7,
  restoring `SH` and `!`. Three ways out, and the choice has not been made:

  - **Ship `bash.exe` and its DLL closure** in the staged tree. Straightforward
    and it gives back the shell §4 was pleased to have shed — "SD does not need
    the MSYS2 *shell*, only its DLLs" stops being true of an installed system.
  - **Point `SH1=` in `sd.conf` at a Windows shell**, which `config.c` already
    supports (`SH1`, and `SH` for the interactive form). Then `OS.EXECUTE`
    strings must be written in that shell's syntax, not bash's — which would
    change every command built in `GPL.BP/OS_GROUP`, `CREATE_USER`,
    `DELETE_USER`, `IS_GRP_MEMBER` and `PS_SCRIPT`, all of which currently rely
    on bash single-quoting to protect their PowerShell scripts.
  - **Point `SH1=` straight at `powershell.exe -Command`**, which would suit
    those five programs best of all and remove a quoting layer, at the cost of
    making every other `OS.EXECUTE` in the system PowerShell.

  **The third was taken**, on the repository owner's instruction, 14 Aug 2026.
  `op_sh.c` now defaults both `SH` and `SH1` to PowerShell, at a path derived
  from `%SystemRoot%` rather than written as `C:\Windows`, and `sd.conf` and
  `gplbld/stage.py` carry the same values so they are visible and overridable.
  The path must contain no spaces: `clparse()` splits on them and does not
  honour quotes, which is why PowerShell is named by its real location.

  **What that changed, and it simplified rather than complicated.** Every
  `OS.EXECUTE` string in the five new programs lost its bash quoting layer -
  the command now *is* the PowerShell script. `!ps_script` changed more: it
  used to `cat` the file into PowerShell's stdin, and now names the file
  **relative to the working directory**, which removes the need for a Windows
  pathname that BASIC cannot produce. Both probes still pass with bash out of
  the loop entirely (§4).

  PowerShell ships with Windows, so **SD no longer depends on a shell it would
  have to install**, which is what made this an installer problem.

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

  So `/dev/shm`, `/etc/sd.conf` and `/tmp` all move with it. The first symptom
  is a warning that `/dev/shm` does not exist, followed by every POSIX shared
  memory call failing — which is the entire IPC layer (§5.1). **Put the
  binaries in `C:\Program Files\SD\usr\bin\`**, so the root lands on
  `C:\Program Files\SD\` and everything POSIX stays inside SD's own directory.
  One level up and the root is `C:\Program Files\` itself, which would mean
  creating `C:\Program Files\dev`.

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
  under MSYS2, so `is_grp_member` failed for everyone. MSYS2 and Cygwin dropped `/etc/passwd` and `/etc/group` in favour
  of direct SAM/AD lookups, but `IS_GRP_MEMBER` reads `/etc/group` as a text
  file. It sets status 1 and returns false always, which fails the `sdusers`
  test at `LOGIN` 193 and terminates every connection with "This user is not
  registered for SD use". **This sits one step past where runtime bring-up
  stopped (§3) and would otherwise be met head-on.** Note this is *not* the
  `getgrnam()` path verified in §4 — that goes through the NSS layer and works
  correctly; reading the file directly does not. **The fix was to repair the
  routine, not to delete its callers** — `GPL.BP/IS_GRP_MEMBER` now asks
  `Get-LocalGroupMember` and distinguishes member / not-a-member / no-such-group
  (§4). The earlier instruction here to delete these calls was written under
  the superseded assumption that SD would stop touching OS groups entirely;
  see the correction in §5.6.
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
  `ImpersonateNamedPipeClient` or `GetNamedPipeClientProcessId`, on a pipe
  whose security descriptor you control. `connection_type` already has
  `CN_PIPE`, so the concept is present in the code.
- **`chmod` is a no-op on the MSYS2 runtime — the mount is `noacl`.** `chmod
  0770` leaves a directory `drwxr-xr-x` and changes no ACE; the real permissions
  stay whatever was inherited, which under `C:\ProgramData` includes
  `BUILTIN\Users:(OI)(CI)(RX)`. Nothing in SD can secure a directory by mode
  bits. Use `icacls` from the installer, `/inheritance:r` first (§5.7).
  Inheritance itself is unaffected by `noacl` and does work — see §5.7.
- **The server and client disagree about the configuration file.** The server
  reads `SCARLET_CONFIG` (`inipath.c`), the client reads `SD_CONFIG`
  (`sdclilib/sdclilib.c`), and the client's comment wrongly claims they match.
  Setting the variable you would expect fixes one and not the other. See §5.8.
- **`sd -start` looks like it hangs, but it has succeeded.** It spawns
  `sdwind`, which inherits stdout and stderr. Any shell that captures output —
  a pipe, command substitution, a tool that reads the process's output — then
  blocks until the *daemon* exits, not until `sd -start` exits. The parent has
  already returned. Check with `Get-Process sdwind` rather than waiting. **This
  became live again on 14 Aug 2026**: while the daemon was never starting,
  there was nothing to block on and a piped `sd -start` returned immediately.

  **Correction, 14 Aug 2026, fourth session — "redirect to a file when starting
  from a script" WAS THE ADVICE HERE AND IT IS NOT ENOUGH.** It hung
  `verify-createaccount.ps1` completely, on its first ever run, in a helper
  that was redirecting to files exactly as instructed. `Start-Process -Wait`
  with `-RedirectStandardOutput`/`-RedirectStandardError` does not return until
  the redirected **handles** are released, and `sdwind` holds them — so the
  destination being a file rather than a pipe changes nothing. The wait is on
  the handle.

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

  Measured, not deduced: piping `AAA` and `BBB` both ways and counting prompts.
  The array form shows an empty command between each pair; the single-string
  form shows none. Do that measurement before trusting any transcript — **the
  echo cannot be read directly**, because SD's `[K` erase-line sequences make
  every line appear twice and can truncate one of the copies (this transcript
  rendered `CREATE.ACCOUNT USER sdacct1` as `CREATE.ACCOUSER sdacct1` on a line
  that executed correctly).

  The BOM sink in the same trap below is still needed; the leading newline
  provides it.

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
  binary's `LastWriteTime` against `git log` for whatever the test exercises is
  usually enough; the data tree is harder, because BASIC ships compiled — the
  quick tell is whether a message the new code prints exists at all:

  ```powershell
  Get-Item 'C:\Program Files\SD\usr\bin\sd.exe' | Select-Object LastWriteTime
  Test-Path 'C:\ProgramData\SD\sdsys\MESSAGES\10034'
  ```

  A `find <tree> -newer <stage>/MANIFEST.txt` over `sdsys/GPL.BP` and
  `sdsys/MESSAGES` names the delta exactly, and did here: `CREATEA`,
  `OS_GROUP` and four messages, which is commit `2fd0aff` and nothing else.

  **Refreshing it means uninstall, delete `C:\ProgramData\SD`, reinstall** —
  the procedure at the top of this file. There is no upgrade path and §5.9
  records that as unsolved; this is the first time its absence has cost
  anything, and it will cost more once there is real data in the tree.

- **`sd -stop` REPORTS SUCCESS WHILE LEAVING `sdwind` RUNNING, when the
  stopping session is less elevated than the starting one.** Observed
  14 Aug 2026, fourth session, and it invalidates nothing in §4 — the earlier
  verification started and stopped SD at the same elevation, which is the case
  that works.

  What was seen: `sdwind` had been started by an **elevated** script.
  `sd -stop` from an ordinary session printed `SD (64 Bit) has been shut down`,
  the shared segment and all six semaphores were unlinked — `C:\ProgramData\SD\shm`
  was empty afterwards — and **the daemon was still running**, idle, minutes
  later. `Stop-Process` on it from the same ordinary session was refused with
  `Access is denied`, which is the same permission boundary `kill()` runs into.

  **`sysseg.c` line 503 does not check the result:**

  ```c
  if (sysseg->sdwind_pid > 0)
    kill(sysseg->sdwind_pid, SIGTERM);
  ```

  An unelevated process signalling an elevated one gets `EPERM`, the return
  value is discarded, and the liveness poll below it walks the **user table**
  only — it never waits for `sdwind` — so nothing anywhere notices. The
  shutdown message is printed unconditionally.

  **What to do now:** kill it by Windows pid from an elevated window,
  `Stop-Process -Id <pid> -Force`. `sd -stop` will not help a second time,
  because the segment it reads `sdwind_pid` from has already gone.

  **What to watch for:** an orphaned `sdwind` holds a mapping of an unlinked
  segment and will keep running `check_lost_users()` against it. Starting SD
  again creates a *fresh* segment, so the machine ends up with two daemons and
  one of them is working on memory nothing else can see. Check
  `Get-Process sdwind` after any `sd -stop` that spanned an elevation boundary.

  **The fix is in `sysseg.c` and is not written** — see §7 step 1d.
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
  the symptom go away. **That diagnosis was wrong** (13 Aug 2026).
  `APISRVR` lines 64-66 are:

  ```
  $execute 'BASIC GPL.BP REVSTAMP'
  $execute 'RUN GPL.BP REVSTAMP'
  $include revstamp.h
  ```

  Compile-time directives that *run* `REVSTAMP`, which opens
  `./gplsrc/revstamp.h` relative to the account directory. `SECOND.COMPILE` is
  only the paragraph `TERM 120,9999` then `BASIC GPL.BP *`, so it aborts when
  it reaches APISRVR and nowhere else. **`CPROC` carries the identical two
  lines already commented out** (139-140), with a note that the build should
  compile and run REVSTAMP to sync the two headers — so the intended fix is
  already demonstrated one file away.

  `REVSTAMP` is a build tool: it translates the C header into the BASIC
  include `GPL.BP/REVSTAMP.H`, which is tracked in the repository. **Both
  `$execute` lines are now commented out** (13 Aug 2026) and
  `gplbld/gen_includes.py` does the translation at build time.

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
  "Invalid account pathname" (`CREATEA` line 257) *after* it had created the
  Windows user and set its password — so the operating system account existed,
  nothing in SD did, and the message named a pathname problem in a verb whose
  visible work had apparently succeeded. Found on the first ever run of that
  verb.

  Now: an optional drive letter is skipped, and the split accepts `/` or `\`,
  whichever comes first. **`df_restricted_chars` was deliberately NOT
  widened** — `op_dio3.c` and `op_dio4.c` use it to map record ids onto
  filenames and back, which is a different job, and changing it would change
  how records are named on disk without being reversible for existing files.

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

In the order they should be taken.

Reordered 13 Aug 2026 to the repository owner's stated priorities: finish the
install layout, then make installing work end to end, and only then go back to
the identity model.

1. **Finish the move to the Windows install layout** (§5.8). The accounts are
   done. What remains is `SDSYS` itself to `C:\ProgramData\SD\`, binaries to
   `C:\Program Files\SD\` **with the MSYS2 DLLs beside them** — the exe's own
   directory is searched first, which is the only reliable answer to the PATH
   traps in §6 — unifying the server and client configuration variable, and
   dropping the `sd.ini`-in-`C:\Windows` fallback. The `sdrealpath()` fix
   removed what was blocking all of it.

   **The data tree holds data only, and that part is done** (decided by the
   repository owner, 13 Aug 2026; carried out the same day). No `gplsrc`, no
   `gplobj`, no `gplbld` under `C:\ProgramData\SD\`. The `$execute` pairs in
   `APISRVR` and `ERRTEXT` are commented out, `gplbld/gen_includes.py`
   regenerates the three derived include files at build time, and
   `SECOND.COMPILE` has been run clean with all three directories absent (§4).
   Two loose ends it left, neither blocking:

   - **`GPL.BP/OPGEN` is not ported** to `gen_includes.py`. It generates
     `GPL.BP/OPCODES.H` from `gplsrc/opcodes.h` and reads `./gplsrc` the same
     way the others did, but nothing ever `$execute`d it, so it breaks no
     compile — it simply cannot be run on an installed system any more. Port
     it before opcodes ever need regenerating, and verify byte for byte
     against the tracked `OPCODES.H`; its hex formatting is not obvious from
     the source (`OP.STOP` is commented `;* 00`, `OP.ABORT` `;* 1`).
   - **`WRITE_INSTALL_DICTS` reads `@sdsys:"/gplbld/FILES_DICTS"`.** It is an
     install step rather than part of a compile, so it did not affect the
     test, but it is the last thing wanting `gplbld` in the data tree and step
     3 has to deal with it.

   **Now the move itself**, which is what remains of this step.
   `<sysdir>/bin` holds the pcode library as well as the executables and must
   be **split, not moved** (§6): binaries to `C:\Program Files\SD\`,
   `pcode`/`pcode.old` stay with SDSYS.
2. **Finish the OS account work** (§5.6), in this order. The shell question
   that stood here was **answered on 14 Aug 2026** — `SH` and `SH1` are
   PowerShell, so nothing depends on a shell Windows does not ship (§6).

   a. Enable `sudo` from Developer Settings, or start SD from an elevated
      prompt, and **run `CREATE.ACCOUNT USER` against a throwaway name**. It
      has never been run on Windows at all (§4). Create the `sdusers` local
      group first — it does not exist on this machine.
   b. **Restore the login gate**, which the owner asked for and which is now
      possible: `LOGIN` 193's `sdusers` test was removed when the routine
      behind it could not work. Restoring it makes the group real again, so
      settle first what it means for §5.6's "SDSYS is the only administrator",
      which it pulls against.
   c. **Remove `sudo chmod g+s` from `CREATEA`** as part of §5.7's `icacls`
      step, since inheritable ACEs are its Windows equivalent.

   `VALID_OS_PATH` — **done, 14 Aug 2026** (§4). It accepts backslashes and
   spaces, so `C:\Program Files` passes, and the caller single-quotes.
3. **Build the staging script, then the Inno Setup installer** (§5.9). The
   `installsdai.sh` port is dropped; these two replace it, and this step
   absorbs what used to be step 9.

   a. **The staging script — first cut done**, `gplbld/stage.py`. It builds
      both install roots from an explicit whitelist, computes the MSYS2 DLL
      closure with `objdump -p` walked transitively, writes `sd.conf` and
      `etc\fstab`, and emits `MANIFEST.txt` so two builds can be diffed. The
      staged `sd.exe` runs with MSYS2 off PATH (§4). What it left open:

      - **The `ACCOUNTS/SDSYS` record ships `/usr/local/sdsys`** as the
        account path — a Linux path, which the staging script copies
        verbatim. It has to become the production path, and that decision is
        tied to whether the staged tree is pre-bootstrapped (below).
      - **`sdsys/BP` ships and holds test programs** (`sdTests`,
        `BIGSTR_TEST` and the like). Harmless, and the Linux install did the
        same, but decide whether an end user should get them. The `PY_*` ones
        went with §5.15.
      - **Consider pre-bootstrapping.** §5.9 says the installer stages
        pre-compiled artefacts, but the script stages `gcat`, `GPL.BP.OUT` and
        `PCODE.OUT` **empty**, which means the target still has to run the
        bootstrap. Running it on the build machine at the production path and
        staging the result would make the install a file copy — no Python, no
        compiler, nothing to fail half way — at the cost of fixing the data
        tree's location. Only `ACCOUNTS/SDSYS` embeds it, so the cost is
        small; a sweep of the live tree found nothing else.
      - **Nothing sets the ACLs yet**, and that is the step that makes the
        data private (§5.7). It belongs in the installer, not the staging.
   b. **Install from the staged tree onto a machine with no development
      tree.** This is the point of the exercise and it has **not** been done:
      the run above proves the binaries load, not that an install works. It is
      what finds anything depended on by accident, which is how `gplsrc`
      survived in the data tree for as long as it did.
   c. **The Inno Setup script — written, and verified on a first install**
      (14 Aug 2026, §4). `gplbld/sd.iss` is tracked here; the compiler is on
      this machine at `C:\Program Files (x86)\Inno Setup 6\ISCC.exe`. The
      `icacls` step works and is confirmed from an unprivileged session. What
      is left on the installer itself is **`sdadmins`** — it creates `sdusers`
      and not the group `IsAdmin()` actually gates on, so a clean machine gets
      a system that cannot be started. Blocked on §8's first item, deliberately.
   d. **Settled 14 Aug 2026, §5.9.1.** The uninstaller keeps accounts, the
      database and `sd.conf`, and offers to remove them with the answer
      defaulting to no; a silent uninstall never deletes them. Verified for the
      keep path (§4).

   **Set the SDSYS password last**, after the whole bootstrap has run. `LOGIN`
   admits an administrator to an account with no verifier yet, so every
   internal command in the sequence works while SDSYS has no credential, and
   nothing has to carry a password through the build. This is the whole of the
   install half of the batch-login question in §8; get the ordering wrong and
   it becomes a real problem instead of a non-problem.
4. **Add the audit log** (§5.6). The missing half of the identity model:
   access is controlled, nothing records who used it. Its own append-only file
   that rotates rather than truncates — *not* `<sysdir>/errlog`, which discards
   its oldest half on reaching the `ERRLOG` size. Records every login, every
   `LOGTO`, and every failed step-up, attributed to `@logname`. A failed
   step-up is the single most interesting line in the trail.
5. **Give grants a verb.** `ACC$USERS` can only be edited through
   `MODIFY ACCOUNTS` today. Decide the shape — `GRANT account TO account` and
   `REVOKE`, or a `SET.ACCESS` screen — and write the audit record from it.
6. **Bring the API server under the same model** — and it is more pressing
   than this position suggests, because §1 now says the API is the product's
   front door. **The API does not work on Windows at all**: `APISRVR` line 921
   calls `login(username, password)` → `login_user()` in `linuxio.c`, which
   with `APILOGIN=1` reads `/etc/shadow`, which MSYS2 does not have. It fails
   closed, which is the good version of broken, but it is broken. The shape of
   the work, in value order:

   a. **Authenticate against `$CRED` instead of the OS**, or drop the password
      check entirely in favour of peer identity — which of those depends on
      the exposure decision in §8. `!CRED_VERIFY` exists and is verified
      working (§4), so this is small.
   b. **Set `@logname` from what was verified**, not from the client. It comes
      from the client today (lines 900 and 963), which is what stops the grant
      check being copied across from `LOGTO`.
   c. **Apply the grant check to `SrvrAccount`** once (b) makes it meaningful.
   d. **Delete the `setuid`/`setgid` calls in `login_user()`.** SD accounts are
      not OS users under §5.6, and they are largely no-ops on MSYS2 anyway.
      They go with the rest of the OS-account work.

   `sdnet.h` still hardcodes `PASSWD_FILE_NAME "/etc/shadow"`, which is what
   that authentication used to be, and goes with (a).
7. **Put `SH` and `!` back** (§5.13). Shell access was disabled on Linux and
   that was a mistake; on Windows it stops programs reaching the utilities
   they need. Find what disabled it — a config option, a `K$SECURE` test, or a
   removed verb — and restore it deliberately.
8. **Make everything lower case that can be** (§5.12), folding in
   **`CASE_INSENSITIVE_FILE_SYSTEM`**, which is referenced at 9 sites in
   `dh_misc.c`, `dh_open.c`, `op_dio2.c` and `op_dio4.c` and defined nowhere.
   Windows filesystems *are* case insensitive, so that half is a correctness
   gap with the code already written. Do the case-insensitive comparisons
   first, or `sue` and `SUE` become different accounts.
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
11. **Exercise `SDConnectLocal()`** once a server runs. Needs the configuration
    file from §5.8, or `SD_CONFIG` set.
12. **Restore the BASIC layer's Windows branches** from the external `GPL.BP`
    tree (§5.4), then set `SYSTEM(91)` to 1 and assign `is_nt`. In that order:
    flipping the switches first would enable paths that are no longer present.
    Start with `CPROC`'s `dir.separator`, since compilation depends on it —
    and note that is now testable, since `sdrealpath()` accepts `\` (§5.8).
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

### Settled: SDSYS is the exception, and LOGTO takes names only

Both questions raised by the grant check on 13 Aug 2026 were **answered the
same day by the repository owner** and are now written into §5.6. SDSYS reaches
every account without exception, and `LOGTO` accepts a registered account name
only — direct directory access by path is not supported, which closes the
bypass rather than trying to resolve paths back to accounts.

### Open: how does a scheduled job log in, now that every account has a password?

Raised by the repository owner on 13 Aug 2026. Every account carries a password
(§5.6), and MV users expect to run work unattended — cron jobs, scheduled
tasks, and the `sd -internal SECOND.COMPILE` shape the install script uses. The
design below is the repository owner's; the constraints under it came out of
working through it and are recorded so they are not re-derived.

**The install case is not part of this and is already solved.** `LOGIN`'s
`authenticate.account` checks `$CRED` first and admits an administrator, with a
warning, to an account that has no verifier yet; `sd -i` never reaches `LOGIN`
at all. So an installer that runs the whole bootstrap and calls `SET.PASSWORD`
as its **last** step needs no credential during the build. That is an ordering
requirement on §7 step 3, not an open question.

**The design.** An `X`-type VOC item named `ALLOWED` in **SDSYS's** VOC, whose
lines are `ACCOUNT, VOC name` pairs. `LOGIN` consults it: the account to enter
comes from the list, and so does the command that may run. Because the item
lives in SDSYS, only an administrator can add to it — but the job runs in the
named account, so **nothing runs with administrator rights**; SDSYS is the
storage location for the policy, not the context it executes in.

Paired with it: **a dedicated batch account that grants nobody.** An account
with an empty `ACC$USERS` is already refused to everyone, and SDSYS already
reaches every account without a grant, so only the administrator can enter it
to edit its VOC or recompile its BP programs. Both halves of that are existing,
observed behaviour (§4) — this is a deployment convention, not a new mechanism,
which is its main virtue. `KIM` on the current test machine is already this
shape.

**The mechanism exists.** `SYSTEM(1026)` returns the command from the command
line (`op_sys.c`, case 1026, from `single_command` in `sd.c`), and `CPROC` does
not pick it up until line 556, so `LOGIN` can read it and decide before
authenticating. No new C code is needed.

**Constraints to build to.**

- **One token, no arguments, and enforce it.** This is what does the actual
  security work, not "must be in VOC" — every verb is a VOC item (`COPY` is a
  `CA` entry for `$COPY`, `LIST` is `CA` for `$QPROC`), so requiring VOC
  membership excludes almost nothing. With no arguments a verb entry is
  useless and only a paragraph is worth listing. Reject a command with
  anything after the first word.
- **Accept only `PA` and `S` VOC types** when the list is consulted, so a
  mislisted verb fails when the administrator sets it up rather than spinning
  on a prompt at 3am.
- **Any prompt must be fatal in this mode.** A scripted session that reaches an
  unanswered prompt spins at full CPU (§6).
- **The name must be unique across the list**, or `-A` must be present and
  match. `-A` naming a different account is a refusal, never a silent override.
- **Set `@logname` explicitly** so the audit record reads as an allowlist entry
  rather than as a login. Attribution is the point of §5.6 and an unattended
  job has no person behind it.
- **Catalogue batch programs locally**, not globally, so they do not appear in
  `gcat` and become runnable from every account.

**What was rejected, and why, so it is not proposed again.**

- **A password on the command line.** Command lines are readable by any local
  user through Task Manager, `Get-CimInstance Win32_Process` and ETW.
- **A password file** works today — `cat pw | sd -ABATCH CMD`, and note `<`
  redirection does not (§6) — and an ssh-style refusal to use a file with a
  loose ACL would make it defensible. It was passed over because a capability
  list is better than a stored credential in two ways: there is no secret to
  leak or rotate, and a stolen credential grants an *interactive session*
  while a list grants only a fixed set of commands.
- **Hashing the VOC entry to detect tampering** pins one hop and no further: a
  paragraph reading `RUN BP NIGHTLY` can be pinned, but `BP NIGHTLY` cannot,
  and a transitive closure discovered at run time cannot be hashed at all.
  Storing the command text in the list rather than a name to look up gets the
  same protection for nothing — the approved thing and the executed thing
  become the same object. Whether the list holds a name or the command text is
  still to decide.

**What this depends on, and what it does not fix.**

- **The batch account is the one account where per-directory ACLs work in
  stage 1.** §5.7's dilemma — grant every SD user access to every account, or
  duplicate the password gate in ACLs — exists because a user's own process
  must read the files of any account they enter. No ordinary user is ever
  meant to run in the batch account, so there is exactly one principal to
  grant: whatever the scheduled task runs as, plus `Administrators`. An
  `icacls` on that directory closes the tampering gap properly, today, with no
  stage 2 dependency. Fold it into §5.9's ACL step.
- **The account boundary is not a data boundary.** `ACC$USERS` gates `LOGTO`,
  not file opens, so a Q-pointer in the batch account's VOC reaches another
  account's files with no grant at all. "Runs without administrator rights" is
  true and worth having; it is not a sandbox. Every grant added to let a job
  reach real data widens what a compromised batch account reaches.
- **Still open: who may trigger it.** The list says what may run unattended,
  not who may fire it, so any local user who can run `sd.exe` can start a
  listed job. With the batch account ACL'd away from them that is a matter of
  causing a job to run at the wrong time rather than of reading or altering
  anything — tolerable, but it argues for listing only work that is safe to
  trigger and ideally idempotent. An optional third column naming an OS
  principal is the escape hatch if that is not enough.

### SETTLED 14 Aug 2026: the API is piped through ssh — posture B

**Answered by the repository owner**, in the same instruction that made SD
accounts ssh-only (§5.6.2): *"Even the API is piped through ssh."* **Posture B
below was taken** — SD listens locally, ssh carries the traffic, and nothing of
SD's own faces the network.

What that settles, beyond the choice itself:

- **The API stops needing a network credential model of its own.** §7 step 6a
  asked whether to authenticate against `$CRED` or to trust peer identity. Over
  a local-only transport reached through ssh, ssh has already authenticated the
  user before SD sees a connection, so the answer leans hard towards peer
  identity — and `login_user()` reading `/etc/shadow`, which cannot work on
  Windows anyway, can go rather than be ported.
- **The AF_UNIX weakness in §6 matters less, but does not vanish.** MSYS2
  emulates AF_UNIX over a TCP loopback socket, so "local socket" is a weaker
  statement here than on Linux and any local process can still reach the port.
  Binding to loopback is not the same as authenticating the peer. A **named
  pipe** with `GetNamedPipeClientProcessId` remains the right Windows answer,
  and `connection_type` already has `CN_PIPE`.
- **It makes the ssh install path load-bearing**, which is why the silent
  failure fixed on 14 Aug 2026 mattered more than an optional extra: if ssh is
  how the API is reached, an ssh option that quietly does nothing is not a
  cosmetic bug.

**The client side, as it actually works today.** Supplied by the repository
owner, 14 Aug 2026 — this is the command their Gambas3 client runs on Linux:

```sh
sshpass -p <password> ssh -L <port>:/tmp/sdsys/sdclient.socket -N <user>@<host> &
```

So the contract is: **ssh forwards a local TCP port to a UNIX domain socket on
the server**, `-N` because no remote command is wanted, and the client library
then connects to `localhost:<port>`. That is worth having written down, because
four things about it do not survive the move to Windows, and together they are
larger than the `login_user()` work in §7 step 6.

1. **Nothing on Windows creates that socket.** `start_connection()`
   (`linuxio.c` 130-131) reads `sun_path` from a socket it has *already been
   given* — the server does not listen, it is spawned per connection with the
   socket on its stdin. On Linux that is xinetd or systemd socket activation.
   **Windows has neither**, so the listener and the per-connection spawn have
   to be built. This is what the retained `etc/xinetd.d/` and
   `usr/lib/systemd/` are documenting, and it belongs with §5.7's service
   model rather than with the API's credential check.
2. **`/tmp/sdsys/sdclient.socket` resolves inside `C:\Program Files\SD\`** on an
   installed system, by the two-component POSIX-root rule in §6 — and Program
   Files is read-only to ordinary users. It needs the same treatment
   `/dev/shm` already got: an `etc/fstab` bind out to `C:\ProgramData\SD\`.
   Exactly the same trap, one directory along.
3. **MSYS2's AF_UNIX is emulated over a TCP loopback socket** with a handshake
   file (§6). It is not a filesystem object with permissions, so the Linux
   reasoning — "a local socket, therefore only local users, therefore
   `getpeereid()` is meaningful" — **does not carry**. Any local process can
   reach the port. This is the strongest argument for the named-pipe route.
4. **`sshpass` does not exist on Windows**, and putting a password on a command
   line is visible in the process list anyway. A Windows client wants key-based
   authentication, which also removes the need for the client to hold a
   password at all.

**Untested and load-bearing:** whether Win32-OpenSSH supports `-L
port:/path/to/socket` — forwarding to a UNIX domain socket rather than a
host:port. OpenSSH has done so since 6.7 on Unix; whether the Windows port does
it, and whether it can reach an MSYS2-emulated socket, has not been measured.
If it cannot, the transport needs rethinking rather than porting.

The original question and the three postures are kept below, because the
reasoning for the two not taken is still the record of what was weighed.

<details>
<summary>The question as it stood</summary>

Background from the repository owner: OpenQM was very insecure and **remote
access was the worst of it**. Telnet was removed and replaced with ssh only;
the API never got the same treatment. §1 now makes the API the product's front
door, so this is the security question that matters most.

**Where it actually stands** — see the trap in §6 and the correction in §5.6.
The API has a connect-time credential check that cannot succeed on Windows, so
it is closed rather than open. That buys time; it does not buy a design.

**Three postures, and they are not ranked.**

| | What faces the network | SD's own network exposure |
|---|---|---|
| **A** | SD's own socket, as shipped | full, and it is 2007 code |
| **B** | ssh tunnel or VPN; SD is local only | none |
| **C** | a web front end; SD is local only behind it | none |

**B is what the repository owner already did to OpenQM**, and it carries to
Windows unchanged — OpenSSH ships as a Windows optional feature and port
forwarding works. It is the conservative answer and costs nothing new.

**The installer now offers B as a checkbox** (decided 14 Aug 2026, §5.9):
opt-in, off by default, withheld with an explanation if the machine already
has an ssh server. That does not decide the posture question — it makes B
reachable by someone who would not otherwise know how, which is the case the
repository owner raised: ten people on a local network, installed by someone
with little administrative knowledge. Read §5.9's two caveats before
recommending it, particularly that ssh gives those ten people **no isolation
from each other's data** until §5.7's service model exists.

**C was the repository owner's idea**, and its merit is that it makes the
*simplest* API authentication the correct one rather than forcing a bigger one.
If the only client is one local process, a **named pipe whose ACL admits
exactly one principal** — an IIS app pool virtual account, or a Kestrel service
account — is a stronger statement than any credential that client could
present. No `$CRED` check in the API path, no TLS in SD, no certificate story.
That is less code, not more. It is also the one case where Windows ACLs work
cleanly, for the same reason as the batch account above: one principal to
grant, so §5.7's dilemma never arises.

**The argument against C, and it is a serious one** (repository owner,
13 Aug 2026): web servers invite attack. Every hacker knows how to attack one,
scanning is constant and automated, and a custom protocol on a non-standard
port simply does not attract the same volume. Obscurity is not security, but it
is a real reduction in *opportunistic* attack traffic, and a web tier is a
whole additional codebase and patching burden. **This is recorded as an option
to be convinced of, not a decision.**

The honest counter is that C does not *add* network exposure, it *moves* it:
the comparison is not "web server versus nothing" but "IIS exposed versus
`APISRVR` exposed", and `APISRVR` is 2007 Ladybridge code with fixed 32-byte
credential buffers that nobody has ever fuzzed. Obscurity cuts both ways —
fewer people attack it, and fewer people have found its bugs. But that argument
favours C only over **A**. Against **B** it has no force at all, because B
exposes nothing either.

**Which is worth noticing: §1 points at B.** If the target user is a Windows
developer using SD as a back end, *their* application is the front end, and it
sits on the same machine or reaches SD over a tunnel. SD does not need to ship
a web tier to be secure — it needs to stop listening on the network. A web
front end is then a **product** decision, about whether SD offers a browser UI,
rather than a security mechanism. Keeping those two questions apart is probably
what makes this decidable.

**The network-layer argument, and it is the strongest one for B** (repository
owner, 13 Aug 2026). A private API can be put behind controls that run *before
a byte reaches SD* — VPN, a Windows Firewall rule scoped by remote address or
interface, or IPsec Connection Security Rules, which can require the peer to be
an authenticated domain machine without a line of application code. A public
web server forfeits all of it by definition: if it is public, anyone may reach
it.

The sharper form of that, which is structural rather than obscurity: **a public
web application must accept anonymous connections as far as the login page.**
Its TLS termination, HTTP parser, router, session handling, login form,
password reset and static file serving are all reachable pre-authentication, by
everyone, by design. An IP-restricted API has a pre-authentication surface
reachable by nobody. That is a real difference in kind.

**The refinement that keeps this honest, so it is not read as "web is
insecure":** the axis is *public versus private*, not web versus API. A web
front end on an internal network behind the same VPN keeps every one of those
controls. Deployed privately, C's security cost over B is a second codebase to
patch, and its benefit is a browser UI — which is the product question again,
not a security one.

**Where these controls have to live, and nothing does it yet.** SD never binds
a listening socket. `sd -N` runs per connection with the socket as stdin and
stdout; **xinetd** bound port 4243, spawned an instance per connection and
supplied `only_from`. xinetd does not exist on Windows, so the service that
replaces it inherits all four responsibilities, and none of them are
implemented. Two consequences:

- **Make it bind to loopback by default**, so posture B is what you get without
  anyone deciding anything, and listening more widely takes a deliberate act.
- `only_from` has no Windows equivalent unless the replacement implements it or
  the install writes a Windows Firewall rule. Decide which; a firewall rule is
  less code and easier to audit.

These are the deployer's controls rather than SD's, so they are reasons to
permit a posture, not a substitute for SD's own authentication (§7 step 6).
Both, not either.

**Two things that apply to B and C alike.**

- **Attribution has to survive the extra hop.** If a front end is the only
  client, every SD session carries *its* identity and `@logname` stops naming a
  person — which destroys what §5.6 is for. The workable split is that the
  front end **asserts identity** (trusted because of the pipe ACL) and SD still
  **enforces authorisation**, checking the target account's `ACC$USERS` itself.
  The grant list stays where it can be audited, and the front end never becomes
  the authorisation authority. Same shape as the batch-login conclusion above:
  an asserted capability, not a shared secret. The cost to accept consciously
  is that compromising the front end compromises attribution entirely.
- **Connection pooling breaks identity, and this is not about `NUMUSERS`.**
  A pooled connection reused across users breaks both `@logname` and account
  isolation, so it needs a session per user or a `LOGTO` with the identity
  reset per request. Note `NUMUSERS=20` in `sd.conf` is only a default —
  OpenQM systems run several hundred users — so the ceiling is a tuning
  question, but the identity problem is not, and retrofitting it is painful.

**What this makes more valuable than its position suggests.**
`SDConnectLocal()` becomes the production entry point under either B or C
rather than a curiosity, and it has never been run (§4). The client DLL is
already the right shape for it: native UCRT64, and confirmed this session to
depend on nothing but Windows system DLLs, so a .NET or native client can use
it with no MSYS2 runtime anywhere in the client tier. That separation was made
for a different reason (§5.3) and happens to be exactly what this needs.

</details>

### Settled: the binaries were purged from history on 13 Aug 2026

Done, and force pushed. See §5.11 and the HISTORY entry. **Any clone taken
before that date is incompatible** and must be re-cloned; do not merge or push
from one. The only remaining copy of the pre-rewrite history is a bundle in a
session scratchpad, which will not survive the machine — see the HISTORY entry
if it is wanted.

### SETTLED 14 Aug 2026: `IsAdmin()` tests Windows `Administrators`, and `sdadmins` is gone

**Answered by the repository owner the same day it was promoted here.** Option
2 below was taken: a Windows administrator is an SD administrator. The decision
and its measured basis are written up in **§5.6.1**, which is the place to
read; what follows is the question as it stood, kept because the reasoning for
the other two options is still the record of what was weighed.

The `sdadmins` group is no longer referenced by anything. It may be deleted
from this machine once a build without it has been run, and it is no longer a
thing the installer has to create.

<details>
<summary>The question as it stood</summary>

**Promoted to the top of this section on 14 Aug 2026.** This was a tidy-up
question with no deadline. It is now the one thing standing between the
installer and a machine that has never had SD on it, so it needs an answer
before the installer can ship.

**What forces it.** `IsAdmin()` (`gplsrc/linuxlb.c` line 75) is
`getgrnam(SD_ADMIN_GROUP)` and returns FALSE when the group is absent, failing
closed by design. `SD_ADMIN_GROUP` is `"sdadmins"` (`gplsrc/sddefs.h` line
131). `sd.c` line 613 refuses `sd -start` with "Command requires administrator
privileges" when it is false. **`gplbld/sd.iss` creates `sdusers` — for the
ACL — and never `sdadmins`.** Nothing in `gplbld/` mentions it. So a clean
machine gets an install in which nobody is an SD administrator, `sd -start`
refuses, and the postinstall `SET.PASSWORD SDSYS` step fails identically. It
works on this machine only because `sdadmins` was created by hand on 13 Aug
2026 and this account's token carries it — the same "leftover state hides the
bug" shape as the `DataTreeAbsent` defect (§4).

**The three answers, and none has been taken.** Adding two `net localgroup
sdadmins` lines to the `.iss` would work, but it decides this question by
accident, which is why it was not done:

1. **Keep an OS-level check on `sdadmins`**, and have the installer create it
   and enrol the installing user, exactly as it already does for `sdusers`.
   Cheapest, and consistent with what the code says today. Note it inherits the
   sign-out-and-back-in trap in §6, so `sd -start` would not work for the
   installing user until they log in again — which for the postinstall
   `SET.PASSWORD` step means it fails on a fresh install every time.
2. **Gate on Windows `Administrators` instead.** Starting a server is an
   administrative act, the group always exists, and it needs no installer step
   at all. It also sidesteps (1)'s re-logon problem, since an elevated token
   carries it immediately. Against it: §5.6 deliberately separated SD
   administration from Windows administration.
3. **Drop the OS check**, and let `sd -start` be gated by file permissions on
   the data tree alone — which the ACLs now genuinely enforce (§4). Most in
   keeping with §5.6, and the largest change.

§5.6 removes the *need* for the group as an identity mechanism, but both it and
`IsAdmin()` are committed (`f56de86`, `9c00730`) and the check runs before any
account exists or any password can be prompted for, so it cannot simply be
deleted: that would leave `sd -start` ungated. Until this is settled, leave
`IsAdmin()` in place.

**Do not delete the `sdadmins` group from this machine** while the question is
open: the token carries it, which is what allows the shipped `sd.exe` to run
`-start` and `-stop` here without the probe build of §6, and it is for the
moment the source of `K$ADMINISTRATOR` for every session (§5.6). Deleting and
recreating it is worse than leaving it — a recreated group has a new SID, which
this token would not carry until the next logon.

</details>

### Open: does the console path survive the service model?

§5.7's service-account model is what makes the data tree genuinely private, but
it requires SD session processes to run as the service rather than as the
invoking user. `sd -ASDSYS` typed at a shell currently runs as that user and
opens the database itself. Decide whether the console entry point becomes a
client of the service, is dropped in favour of a client tool, or stays as a
privileged path used only by administrators. This shapes stage 2 and should be
settled before the `fork` → `CreateProcess` work starts, since that is where
the process creation identity is decided.

### Other

- `usr/lib/systemd/` and `etc/xinetd.d/` are kept deliberately. They have no
  function on Windows but they document the service topology — socket
  activation, ports, per-connection instances — that a Windows service must
  reproduce. Remove once that design is captured elsewhere.
- The client library is LGPL-3.0-or-later with a linking exception, while the
  rest of the tree is GPL-3.0. That is compatible and intentional for a client
  library, but it is a real licensing boundary worth being aware of.
