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
| 1 | **B** | The `edit` / `micro` refusal message is malformed | `sdsys/gpl.bp/EDIT` |
| 2 | **B** | The installing user gets no `OS.EXECUTE` | `gplbld/adopt-account.ps1` |
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

***UPSTREAM #18 AND #19 ARE FIXED IN THIS TREE*** and are deliberately not
listed above — `op_config.c` and `op_skt.c`, both 26 Aug 2026, each citing its
UPSTREAM_FIXES number in its own history block. **They are the reason 11 to 13
are worth stating separately**: four upstream defects were found while
documenting, two were fixed here and two were not, and nothing recorded which
was which.

---

## 1. The `edit` / `micro` refusal message is malformed — **B**

Reported by the owner, 26 Aug 2026.

`check.permitted` builds a multi-line refusal by concatenating `char(10)` — a
bare LF — and `EDIT:273` prints the whole thing with **one** `crt`. Eight sites
build text this way: `EDIT` lines 236, 362, 374, 397, 426, 432 (which converts
field marks to `char(10)` wholesale), 503 and 557.

***CONFIRMED ON A REAL CONSOLE BY THE OWNER, 26 Aug 2026.*** A bare LF advances
a line without returning to column 0, so every line after the first starts where
the previous one ended:

```
:edit bp test
edit is not available to don.
                            It runs an editor outside SD, so it needs OS.EXECUTE permission: field 2 of your record in
the SD system file os.users, which only an administrator can change.
                                                                    ed, the line editor, needs none of this.
```

**A pipe hides it.** Through `sdtcl`, `edit voc =` returns two clean lines,
because there the LF *is* the separator. **Test this one on a console.**

**The fix is one `crt` per line** rather than one `crt` of an embedded-LF
string. §7.16 established that this port writes CRLF to everything externally
readable; the terminal path was not part of that work.

**Look at the whole family, not just this message.** `char(10)` as a line
separator inside a single write is the class.

## 2. The installing user gets no `OS.EXECUTE` — **B**

Owner's instruction, 26 Aug 2026: the installer should be an administrator and
have ssh, api and `OS.EXECUTE` in his own account automatically.

***TWO OF THE THREE ALREADY HOLD AND SHOULD NOT BE REDONE:***

| | |
|---|---|
| tier | `CREATEA:1320` — `if adopt and tier = 'STANDARD' then tier = 'ADMINISTRATOR'`. The adopted account is already ADMINISTRATOR; `sdsys/accounts/don` field 5 reads `ADMINISTRATOR` on this install |
| ssh + api | `CREATEA:1322` — an administrator always has both routes and no keyword can take either away. Owner's rule, 21 Aug 2026 |
| `OS.EXECUTE` | **missing** |

**Measured 26 Aug 2026: `C:\ProgramData\SD\sdsys\os.users` holds 0 records** on
a freshly installed system, so nobody has `OS.EXECUTE` or `SH` by that route.
`adopt-account.ps1` runs `CREATE.ACCOUNT USER <name> ADOPT` and writes no
`os.users` record.

**This is why item 1 is being seen at all, and the owner's console confirms
it.** `EDIT`'s `check.permitted` admits an administrator through
`kernel(K$ADMINISTRATOR, -1)`, which requires elevation. An unelevated session
belonging to the installing user therefore falls past that test to the
`os.users` lookup, finds no record, and gets the refusal — in the malformed
form above. The message read *"edit is not available to don"*, and `don` **is**
the ADMINISTRATOR-tier adopted account. **So the two items are one symptom:**
fixing 2 stops most people ever seeing 1, and 1 still needs fixing for everyone
who legitimately lacks the permission.

***RULED BY THE OWNER, 26 Aug 2026, AND IT IS BOTH HALVES:***

1. **The installing user gets `OS.EXECUTE` automatically** — an `os.users`
   record with field 2 `yes`, written by `adopt-account.ps1` alongside the
   ADOPT it already runs.
2. **Administrators get `edit` and `micro` automatically.** *"administrators
   should have automatic edit and micro access."* So `EDIT`'s
   `check.permitted` must accept the **ADMINISTRATOR tier**, not only
   `kernel(K$ADMINISTRATOR, -1)`, which is an *elevation* test and is false in
   an ordinary unelevated session.

**The two are not the same change and both are wanted.** (1) grants
`OS.EXECUTE` generally — `sh` and `!` as well as the editors. (2) makes the
editors work for an administrator whatever `os.users` says. **Together they mean
an administrator never meets this refusal**, which is the point.

***THE TIER IS AVAILABLE TO `EDIT` AND IS NOT WHAT IT READS TODAY.*** Field 5
of the account's `accounts` register record is `ADMINISTRATOR`
(`syscom/KEYS.H:282`, `ACC$TIER`); `check.permitted` reads `K$ADMINISTRATOR`
and `os.users` field 2 and never looks at it. **Keep the no-terminal refusal
regardless of tier** — an API session or a piped script still cannot run a
full-screen editor, and that check is right.

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

***WHAT WAS NOT ESTABLISHED, SO DO NOT ASSUME IT.*** `sdwind`'s
`check_lost_users()` sweep is supposed to reap these every five minutes.
**Neither observation ran long enough to test it** — the two stale entries were
watched for about four and about three minutes before being cleared by hand. So
it is still open whether the sweep works here, and PROJECT_STATUS §6 records it
misbehaving on 22 Aug 2026 by forcing out healthy sessions instead. **Time the
next one properly before concluding anything.**

## DONE

*(nothing yet)*
