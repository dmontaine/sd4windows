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

| | SEV | what | where |
|---|---|---|---|
| ~~1~~ | **B** | ~~The `edit` / `micro` refusal message is malformed~~ — **DONE 27 Aug 2026** | `sdsys/gpl.bp/EDIT` |
| ~~2~~ | **B** | ~~The installing user gets no `OS.EXECUTE`~~ — **DONE 27 Aug 2026** | `sdsys/gpl.bp/CREATEA` |
| 3 | **S** | The live `SDSYS` VOC does not match `voc_template` | `sdsys/voc_template` |
| 4 | **S** | Tester page 07 says a standard account has 77 verbs; it has 81 | docs repo |
| 5 | **S** | `.d name` cannot find a lower-case VOC record typed in upper case | `CPROC:1119` |
| 6 | **S** | An empty directory called `C:` is created in the data tree by the installer | `gplbld/sd.iss` |
| 7 | **M** | `sort.item` is withheld from a standard account and `list.item` is not | `newvoc/TIER.OMIT.STANDARD` |
| 8 | **M** | `help` is an empty stub and F1 reaches it | `CPROC:2498` |
| 9 | **M** | `umask` is implemented and unreachable | `CPROC:3301` |
| 10 | **M** | Two verifiers carry a dead ANSI strip | `gplbld` |
| 11 | **B** | ***Nested `commit` silently loses the outer transaction's writes*** — UPSTREAM #17, **unfixed here** | `gplsrc/txn.c` |
| 12 | **S** | Error 3023 tells the user the disk may be full — UPSTREAM #20, **unfixed here** | `sdsys/messages/1407` |
| 13 | **M** | `qselect` prints its message without the list number — UPSTREAM #21, **unfixed here** | `gpl.bp/QSELECT:240` |
| 14 | **S** | `delete.file ... no.query` still prompts, so it cannot run unattended — UPSTREAM #23, **unfixed here** | `gpl.bp/DELETEF:222` |
| 15 | **M** | `delete.index` will not match a lower-case index name, though `list.index` will — UPSTREAM #22, **unfixed here** | `gpl.bp/DELETEI:155` |
| 16 | **S** | A killed session blocks exclusive access, says nothing about why, and only an administrator can clear it | `gplsrc/sd.c:333` |
| ~~17~~ | **B** | ~~`edit` / `micro` refuse a record whose text looks like a mark token~~ — **DONE 27 Aug 2026** | `sdsys/gpl.bp/EDIT` |
| ~~18~~ | **M** | ~~A text mark reaches the editor as a raw control character~~ — **DONE 27 Aug 2026** | `sdsys/gpl.bp/EDIT` |
| 19 | **B** | ***The tier change and `SUSPENDED` compile but have never RUN, and there is no verifier*** | `gpl.bp/MODIFYA` |
| 20 | **S** | A suspended administrator is still a Windows administrator | `gpl.bp/MODIFYA` |
| 21 | **S** | ~~The write-once rule on `ACC$PRIOR.TIER` is unreachable, and four documents say it is what makes field 6 safe~~ — **dead test deleted, docs corrected 27 Aug; compiled + installed 17:25:59, `b48` is the regression check** | `gpl.bp/MODIFYA`, `syscom/KEYS.H` |
| 22 | **M** | `create.account` says a password was not set and never says why | `gpl.bp/CREATEA:498` |
| ~~23~~ | **S** | ~~`term default` sets 20x24, the MINIMUM width, not SD's 120x36 default~~ — UPSTREAM #24. ***DONE 27 Aug 2026***, installed 17:25:59 and **measured: `term` reports 120 x 36**. Left: three docs pages still describe the old behaviour (docs repo) | `gpl.bp/TERM:165` |
| 24 | **S** | ***`sd -cleanup` never releases a dead session's task locks*** — UPSTREAM #25, **unfixed here** | `gplsrc/clopts.c:300` |
| 25 | **S** | `encrypt.field` is in every administrator's VOC and `$CRYPTO` is not in the distribution — UPSTREAM #26, **unfixed here** | `sdsys/voc_template/encrypt.field` |
| 26 | **S** | `delete.file` *name* `no.query` prompts twice when the name is typed in lower case — UPSTREAM #27, **unfixed here** | `gpl.bp/DELETEF:233` |
| 27 | **M** | `modify.account` *acc* `add`/`delete` makes the same group change as `grant`/`revoke` and writes no audit record | `gpl.bp/MODIFYA:344` |
| 28 | **M** | A process dump is written into the system directory, where every SD user can read it | `gplsrc/pdump.c:97` |
| 29 | **S** | `micro` reports "Permission denied" on every save — **the file IS saved**, so a false alarm, not data loss (downgraded from **B**). Fix is `MICRO_CONFIG_HOME` = a per-user `~/.micro` via the new `micro-home.ps1`. ***THREE ATTEMPTS: `-backup off` fixed nothing; the helper read env vars that are empty inside `os.execute`; `EDIT` split the capture on `char(10)` where it is `@fm`.*** All three now corrected and **measured end to end — uncompiled, needs a cycle** | `gpl.bp/EDIT`, `gplbld/micro-home.ps1` |
| 30 | **S** | ~~`verify-osusers.ps1` refuses on a fresh install: it needs `@LOGNAME` unlisted in `os.users`, but PRE_RELEASE 2 made `adopt-account` list every administrator~~ — **verifier fixed 27 Aug (parks and restores the record); the product is correct** | `gplbld/verify-osusers.ps1` |
| 31 | **S** | ***`verify-apiadmin`'s control is stale*** — it expects an elevated session `LOGTO`'d into a PROGRAMMER account to lose `OS.EXECUTE`, but `os_permitted()` keys the list on `process.username` (`don`), whom PRE_RELEASE 2 listed. Product is per design; **verifier needs a rewrite, owner to confirm the new premise**. Headline hole (API OS.EXECUTE) stays closed | `gplbld/verify-apiadmin.ps1` |
| 32 | **S** | ***`delete.account` leaves the `ProfileList` registry entry, so an account recreated under the same name gets a DIFFERENT home directory*** — `C:\Users\<name>.<DOMAIN>` — and anything keyed to the old path breaks. **Measured: ssh public-key auth refused.** 53 stale entries on this host | `gpl.bp/DELACC` |

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

## 4. Tester page 07 says a standard account has 77 verbs — **S**

It has **81**. `Testing/markdown/07-programmer-commands.md` opens with the
wrong number, and page 06 repeats it.

**77 is a count of VOC records whose field 1 begins with `V`.** It misses the
four records that are a keyword *and* a verb — `break`, `count`, `display`,
`off` — whose fields 3 onward are a complete verb record. `CPROC:1718`
re-parses from field 3, so all four are typeable, and none is on
`TIER.OMIT.STANDARD`.

**Confirmed three ways.** `CREATEA:961`-`996` copies every `newvoc` record
except the two list records and, for a standard tier, the 42 omitted names —
with no filter on record type, so 123 − 42 = 81. SD's own VOC dictionary
encodes the same rule in its I-type `DISPATCH` field. And
`count voc with dispatch # ""` answers **144** in `SDSYS`, matching a file scan
of the shipped tree exactly (`CA` 97, `IN` 45, `OS` 2).

## 5. `.d name` cannot find a lower-case VOC record typed in upper case — **S**

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

## 10. Two verifiers carry a dead ANSI strip — **M**

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

## 11. Nested `commit` silently loses the outer transaction's writes — **B**

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

## 13. `qselect` prints its message without the list number — **M**

**UPSTREAM_FIXES #21. Live in this tree, measured 26 Aug 2026** —
`gpl.bp/QSELECT:240` passes one argument to a two-parameter message, so every
successful `qselect` ends with a dangling *"select list "*. `NSELECT:112` two
files away supplies both and is the model. One line, and `tgt.list` is already
in hand on the line above.

Documented as a known blemish in the select-lists page so a reader does not go
looking for a list that is there.

## 14. `delete.file ... no.query` still prompts — **S**

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

## 15. `delete.index` will not match a lower-case index name — **M**

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

## 2. The installing user gets no `OS.EXECUTE` — **B** — DONE 27 Aug 2026

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

## 19. The tier change and `SUSPENDED` compile but have never run — **B**

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

## 21. The write-once rule on `ACC$PRIOR.TIER` is unreachable — **S**

Measured 27 Aug 2026 by running it. `SYSCOM/KEYS.H`, `tier.set`'s banner,
PROJECT_STATUS.md's START HERE and HISTORY.md all state that field 6 is safe
because `MODIFY.ACCOUNT` writes it **only on the transition into SUSPENDED**.

A second `modify.account <acct> suspended` answered ***"B48TIER is already
SUSPENDED; nothing changed"*** — sysmsg 10110, the **equality guard** at the
top of `tier.set`, returning before the field-6 write is reached.

**It is unreachable rather than merely unexercised.** `old.tier` is upcased and
trimmed and `want.tier` is one of four upper-case literals, so reaching the
write with `want.tier = 'SUSPENDED'` already implies `old.tier # 'SUSPENDED'`.

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

## 22. `create.account` says a password was not set and never says why — **M**

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

## 23. `term default` sets the minimum width, not the default — **S**

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

***THE THREE DOCUMENTS THAT DESCRIBE THE OLD BEHAVIOUR ARE NOW WRONG AND ARE THE
REMAINING WORK ON THIS ENTRY.*** *SD TCL - The Terminal and the Session*, tester
page 13 and page 02 all state that `term default` does **not** restore 120 x 36
and give `term 120,36` as the way to do it. That was true when written and is
false as of this install. **They live in `SDCoreWindowsDocs`, so the correction
is a separate commit in that repository** — and it is the exact case the docs
`README` warns about: a page whose value is a measured defect is the page a fix
invalidates.

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

## 25. `encrypt.field` is in every administrator's VOC and `$CRYPTO` does not exist — **S**

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

## 26. `delete.file` *name* `no.query` prompts twice when the name is typed in lower case — **S**

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

## 27. `modify.account` *acc* `add`/`delete` writes no audit record — **M**

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

## 29. `micro` reports "Permission denied" on every save — **S**

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

**Still uncompiled in the shipped tree** — `assert-current` names
`gplbld\micro-home.ps1` and `sdsys\gpl.bp\EDIT`. Another cycle is owed.

***AND THE FIXTURE DOES NOT SURVIVE A CYCLE.*** `cycle.ps1` deletes both trees,
so `don`'s BP — `ZZMARKS` included — goes with it, and `EDIT` will happily open
a record that does not exist. The owner's run was therefore editing an **empty
new record**, not the mark fixture. **Rebuild it after every cycle** with
`tools\probes\make-zzmarks.py` in the docs repository; sha
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

## 30. `verify-osusers.ps1` refuses on a fresh install — **S** (verifier, not product)

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

## 31. An elevated local session keeps OS.EXECUTE after LOGTO — **B?** (owner's call)

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
is stale** — same class as PRE_RELEASE 30. **Left for the owner** because it is
the verifier's *only* contrast and rewriting it means deciding what the test now
proves: probably "a session whose `process.username` is not listed is refused,
elevated-then-LOGTO'd or not", with a non-`don` Windows identity or an
unlisted-account probe. The API-side behaviour (refused) is not in question and
the headline hole stays closed.

**Left behind by that run** (normal — the next `cycle.ps1` clears them): the
`b48` verifier accounts `sdacctb48`, `sdtiertb48*`, `sdrtb48*`, `sdtapib48*` and
three `os.users` records for the ADMINISTRATOR-tier ones the tier verifiers make.

---

## 32. `delete.account` leaves the ProfileList entry, so a recreated account gets a different home — **S**

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
