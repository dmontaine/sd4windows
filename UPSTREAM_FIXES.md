# UPSTREAM FIXES

Defects found while porting SD to Windows that **also affect `sdb64`**, the
upstream Linux project at <https://codeberg.org/stringdatabase/sdb64>.

**Fixes owed to `winsdclilib` do NOT belong here** — it is ours to maintain and
is fixed directly (PROJECT_STATUS.md §2, the sibling repositories). This file is
only for what `sdb64` itself needs. Entry #2 is a closed example of a bug that
looked like upstream's and was not. *(`linuxsdclilib` was removed from the project on 23 Aug 2026 — repository
deleted, tree archived to `Projects\linuxsdclilib.zip` and to pCloud — and is
not a destination for anything. Its history survives in that zip, which is why
entry #2's citation of `f6ab707` still resolves.)*

## Nothing here can be tested across the boundary

**The two projects cannot talk to each other, so no claim in this file has ever
been checked by running one side against the other.** Measured 23 Aug 2026:

- **This port's client cannot log in to an upstream server.** Its only login
  path sends **request 47** (`SrvrScramFirst`); upstream's `APISRVR` dispatch
  table **ends at 46**, so the request falls off the end of it. There is no
  fallback — request 24 was removed here, not deprecated.
- **An upstream client cannot log in to this port's server.** It sends request
  24, which `APISRVR` marks *"RETIRED, always refused"* since 20 Aug 2026:
  SCRAM is the only network login and there is **no fallback, by design**.
- `grep -rli scram ../sdb64` finds **nothing**. Upstream has no SCRAM at all.

**So every entry here rests on READING upstream's source and reasoning about
it — never on observing upstream misbehave.** That is a real limit and it
should show in how an entry is worded: say what the code does and why it is
wrong, and **do not write as though the failure was reproduced** unless it was
reproduced *in this tree*, which is a different claim and worth stating as one.

**It also means the usual safety net is absent.** Elsewhere in this project a
wrong conclusion is caught by a verifier; here there is nothing to run. The
substitute is the generation check below — do it, every time.

**This file has a different audience from the rest of the repository.**
PROJECT_STATUS.md and HISTORY.md are written for the next AI session;
this one is written to be **handed to the upstream maintainer**, so each entry
should stand on its own without knowing anything about the Windows port. Plain
English, the reasoning included, and the patch small enough to read.

## What belongs here

A fix belongs here when **the defect is present in `sdb64` itself**, on `main`
or `dev`. Check before adding — `../sdb64` is cloned locally:

```sh
git -C ../sdb64 show main:sd64/gplsrc/<file>
git -C ../sdb64 show origin/dev:sd64/gplsrc/<file>
```

Three generations exist and only the first is upstream's problem
(PROJECT_STATUS.md §2):

| Generation | What it is | Belongs here? |
|---|---|---|
| `sdb64` | the upstream Linux project | **yes** |
| `sdb_ai` | five AI cleaning cycles; marked `Composer AI - 2026/06/10` | no — ours |
| SD for Windows | this port | no — ours |

So a bug carrying a `Composer AI` marker is **not** upstream's unless the
underlying flaw is there too — which happens, and #1 below is exactly that
case: the cleaning cycle correctly spotted an upstream flaw and then fixed it
badly. **Windows-specific changes never belong here.**

## Status key

***DO NOT MAINTAIN PER-ENTRY STATUS. THE WHOLE FILE GOES AT THE END.*** Owner,
2 Sep 2026: *"don't worry about the status of each report. I just will send him
the whole file when we are done."* **This file IS the deliverable** — it is
emailed to the upstream developer, who is a former colleague of the owner's on
upstream SD, as one document when the work is done. So the markers below are
history rather than a workflow: **leave them where they are, do not add them to
new entries, and do not spend a session reconciling them.** What an entry needs
is to be true and self-contained; what it does not need is a status line.

*(The original key, kept because sixteen entries still carry its markers:
`PROPOSED` — written up, not sent. `SENT` — reported upstream, with where.
`ACCEPTED` / `DECLINED` — upstream has ruled. Keep declined entries, with the
reason.)*

---

## 1. `NullString()` and `CNullString()` return static storage that the caller frees

**Status:** PROPOSED, 15 Aug 2026
**Affects:** `sd64/gplsrc/op_sdext.c`, `sd64/gplsrc/ctype.c` — `main` and `dev`
**Severity:** latent. Only reachable when a 1-byte `malloc` fails, so it will
not be seen in normal running — but the failure mode is heap corruption, and
the code sits on the credential path.

**Upstream today** does not check the allocation at all:

```c
char* NullString() {
  char* p;
  p = malloc(1);
  *p = '\0';        /* NULL dereference if malloc failed */
  return p;
}
```

`ctype.c`'s `CNullString()` is the same, and `Extract()` returns it.

**Why it matters.** Both results are owned and freed by the caller.
`op_sdext.c` puts them into `SDMEArgArray` — `NullString()` directly, and
`Extract()`'s result in the loop just below — and then frees every non-NULL
entry of that array before returning. On out-of-memory the current code
dereferences NULL and crashes immediately.

**The fix.** Return NULL on failure. The release loop already tests for it:

```c
char* NullString() {
  char* p;
  p = malloc(1);
  if (p == NULL)
    return NULL;
  *p = '\0';
  return p;
}
```

**A warning about the obvious alternative**, because this project tried it and
it is worse. Returning a `static char empty[1]` on failure removes the NULL
dereference and replaces it with `free()` of static storage — undefined
behaviour, and unlike the crash it is silent, delayed, and discovered far from
its cause. If upstream would rather treat a failed 1-byte allocation as fatal,
that is also defensible; what must not happen is handing back a pointer the
caller will free.

---

## 2. `SV_EMSG_PAIR` and `SV_ECONTXT` were transposed — RESOLVED, and it was NOT upstream's bug

**Status:** **CLOSED 15 Aug 2026. Nothing to send.** `sdb64` was right and had
been all along; the transposition was in the client libraries and is fixed in
all three of them. Kept because the *method* that settled it is the reusable
part, and because a future session comparing the two will otherwise re-open it.

**What it was.** `sdb64` `dev` commit `d0647b9`, **19 Jul 2026**, defined
`SV_EMSG_PAIR=6, SV_ECONTXT=7`. `winsdclilib` commit `13e4bf5`, **5 Aug 2026**,
titled *"Align Windows client error handling with Linux"*, introduced the same
two names as `ECONTXT=6, EMSG_PAIR=7` — **the opposite of the thing it was
aligning to**, seventeen days later. The same 5 Aug work seeded
`linuxsdclilib` at its initial import (`3a3e02a`), so the swap propagated to
both client repositories while `sdb64` stayed correct.

**How it was settled**, and this is the part worth keeping: `sdb64` **`main`
does not carry these constants at all** — only `dev` does. So neither client
repository can have taken them from `sdb64`'s released branch, which is what
made the direction of travel unambiguous once `winsdclilib`'s own history was
available. **Dates alone were not enough and pointed the wrong way**: the
vendored snapshot is 5 Aug and `sdb64`'s commit is 19 Jul, but a snapshot date
says nothing about when a line was written. A session here renumbered on that
reasoning, reverted it, and only got it right once all three histories were
readable.

**Fixed and pushed, 15 Aug 2026:** `winsdclilib` `a1987b0` (headers, `.bi`,
`USER_GUIDE.md` — `make check` passes with the new values) and
`linuxsdclilib` `f6ab707` (headers, `.bi`, the `#ifndef` fallbacks in
`sdclilib.c`, `USER_GUIDE.md` — **not built**, the change was made from a
Windows machine and the commit message says so). This port's vendored copy is
corrected to match, and `sdsys/SYSCOM/sdclilib.h` gained both names for the
first time, so BASIC can now tell a transport failure from a context error.

**One thing left undone, and it is upstream-facing in the other direction:**
`sdb64`'s `dev` branch is the only place these constants live upstream — `main`
does not have them. When `dev` merges to `main` they arrive; until then anyone
building the client against `sdb64` `main` has neither.

---

## 3. `start_sd()` treats a failed `fork()` as success, and the daemon dies silently

**Status:** PROPOSED, 16 Aug 2026
**Affects:** `sd64/gplsrc/sysseg.c` (`start_sd()`) and `sd64/gplsrc/sdlnxd.c` —
both present on `main` and `dev`
**Severity:** `sd -start` reports that SD has started when it has not, and
leaves a shared memory segment and semaphore set behind. Every later session
then fails on the orphaned semaphores with a message that does not describe the
problem. Recovery needs `sd -stop`, which is not what the message suggests.

**The fork is not checked.** `sysseg.c` around line 351:

```c
  cpid = fork();
  if (cpid == 0) { /* Child process */
    ...
    execl(path, path, NULL);
    ...
  } else /* Parent process */
```

`fork()` returns `-1` on failure, and `-1` is not `0`, so a failure takes the
*parent* branch. The daemon is never started, nothing is reported, and
`start_sd()` carries on to tell the user SD has started. On Linux this is
reachable whenever `fork()` hits `EAGAIN` or `ENOMEM` — process limits, cgroup
pressure, a loaded machine.

It matters more than a missed error usually would because of *where* it sits:
`bind_sysseg(TRUE, ...)` has already created the shared segment and the
semaphores by this point. So the failure leaves a half-built system that looks
started, and the next `sd` session finds semaphores with no daemon behind them.

**Suggested fix** — report it and let the existing `sd -stop` path clean up,
rather than trying to unwind `bind_sysseg()` here:

```c
  cpid = fork();

  if (cpid < 0) {
    fprintf(stderr, "Cannot start %s - fork() failed: %s\n", SDWIND_NAME,
            strerror(errno));
    fprintf(stderr, "Run sd -stop to clear what this left behind.\n");
    return FALSE;
  }

  if (cpid == 0) { /* Child process */
```

(Upstream's daemon is `sdlnxd`; this port renamed it, hence the macro.)

**And the daemon cannot say why it failed to start.** `sdlnxd.c` ends its
startup with:

```c
  if (!get_semaphores(FALSE, errmsg))
    exit(2);
```

`errmsg` has just been filled in with the reason and is then discarded, and the
`shm_open`/`fstat`/`mmap` failures above it are bare `exit(1)`s. When the daemon
will not start there is nothing to read anywhere — `log_message()` is not usable
this early, because it takes `ERRLOG_SEM` and the semaphores are precisely what
has failed. Printing `errmsg` to `stderr` before each exit costs nothing and is
the difference between a diagnosis and a guess:

```c
  if (!get_semaphores(FALSE, errmsg)) {
    fprintf(stderr, "sdlnxd: %s\n", errmsg);
    exit(2);
  }
```

**How it was found.** Porting to Windows, SD was run from a Windows service.
`sd -start` printed "SD has been started", no daemon existed, and every
subsequent session failed on the semaphores. Nothing in the two programs
reported anything, so the cause had to be reconstructed from file ownership and
exit codes. The Windows-specific part of that is ours; these two are not.

---

## 4. `SDConnectLocal()` and `sd -C` disagree about what `-C` takes, so a local client connection cannot work

`PROPOSED`

**The two halves of the local-connection mechanism have never matched.** The
client library builds a command line naming a **pipe**, and the server parses
`-C` as a pair of **file descriptors** and rejects anything else.

`sdclient.c`, in `SDConnectLocal()`:

```c
sprintf(command, "%s\BIN\SD.EXE -Q -C %s", sysdir(), pipe_name);
```

`sd.c`, handling that argument:

```c
case 'C': /* SDLocal client connection */
  connection_type = CN_PIPE;
  if (sscanf(argv[arg], "-C%d!%d", &TxPipe, &RxPipe) != 2) {
    exit(1);
  }
  dup2(RxPipe, 0);
  dup2(TxPipe, 1);
  break;
```

The client passes `-C` and the pipe name as **two separate arguments**, so
`argv[arg]` is exactly `"-C"`. `sscanf` matches no integers, returns 0, and the
process calls `exit(1)` immediately. The client then blocks in
`ConnectNamedPipe()` waiting for a child that has already gone, or fails there.

**So `SDConnectLocal()` cannot succeed as the two files stand.** There is no
ordering or timing to it — the server exits during argument parsing, before it
does anything at all.

**A second fault sits behind the first**, and it matters because fixing only
the parse leaves the call still failing: the executable is looked for at
`<sysdir>\BIN\SD.EXE`, and `sysdir()` returns the **SDSYS data directory**.
The server executable does not live in the database.

**Suggested fix.** Accept both forms rather than replacing one with the other,
since the descriptor form is what a Unix parent doing fork-then-exec would
send:

```c
case 'C': /* SDLocal client connection */
  connection_type = CN_PIPE;
  if (sscanf(argv[arg], "-C%d!%d", &TxPipe, &RxPipe) == 2) {
    dup2(RxPipe, 0);
    dup2(TxPipe, 1);
  } else {
    if (++arg >= argc)
      exit(1);
    /* argv[arg] is the pipe name - open it and make it 0 and 1 */
  }
  break;
```

**Note the argument must be consumed here.** The option loop above stops at the
first argument that does not begin with `-`, and a pipe name does not, so
leaving it would end option parsing and the name would then be taken for a
command to execute. `-TERM` already consumes its argument this way.

Opening the pipe is platform work: on Windows it is `CreateFile` on the pipe
name, and on a Unix host the equivalent local transport would be a socket or
FIFO path. That part is not proposed here, only the argument handling and the
executable location, which are wrong independently of platform.

**How it was found.** Porting to Windows. `SDConnectLocal()` had never been
called on this platform, and reading the two sides against each other to find
out what it expected showed they had never agreed. Both files are byte-identical
to `sdb64` in the lines quoted, which is why this is here rather than in our own
notes.

---

## 5. `LOGIN`'s VOC update decides whether to write a record by comparing it against a different record

**Status:** PROPOSED, 17 Aug 2026
**Affects:** `sd64/sdsys/GPL.BP/LOGIN`, the `update.voc` subroutine — `main` and
`dev`
**Severity:** low but real, and silent. Some VOC entries are never added to an
account by `UPDATE.ACCOUNT` or by the "Update VOC to new release?" prompt, with
no error and nothing in the output to show it.

`update.voc` walks `SDSYS NEWVOC` and copies each record into the target
account's VOC. For each id it does:

```
      read rec from sdsys.file,id then
         new.type = upcase(rec[1,1])
         if new.type = 'P' then new.type = upcase(rec[1,2])

         readu old.rec from update.voc.f, id then
            ...
         end

accept.without.query:
         rec<1> = new.type   ;* Remove comment text
         ...
         if compare(old.rec, rec) then
            write rec to update.voc.f, id
            display '.' :
         end else
            release update.voc.f, id
         end
      end
   repeat
```

**`old.rec` is never initialised, and the `READU` has no `ELSE`.** A failed
`READ` leaves its target variable untouched — `op_dio3.c` takes the ELSE clause
without writing the string descriptor — so when the account's VOC does not yet
hold the id, `old.rec` still contains **the record read on a previous iteration
of the loop**. The `compare()` that decides whether to write is then made
against an unrelated record.

Most of the time the two differ and the record is written, which is the right
outcome for the wrong reason. It goes wrong when a missing id and an id already
present normalise to byte-identical records, because then `compare()` says
"same" and the missing one is silently skipped.

**`NEWVOC` contains several such pairs.** `CATALOG` and `CATALOGUE` are both
`V` / `CA` / `$CATALOG`; `CD` and `COMPILE.DICT` are both `V` / `CA` / `$CD`;
`GRANT`, `REVOKE` and `LIST.GRANTS` all point at `$GRANTA`. Note that `rec<1>`
is normalised to the bare type letter just above the comparison, so records
whose descriptions differ still end up identical. Whether the pair actually
arrives adjacent depends on the order a directory select returns ids, which is
filesystem-dependent — so this reproduces on some hosts and not others, which is
the worst property a bug of this kind can have.

**The fix is one line** — clear the variable so a failed read is distinguishable
from a successful one:

```
         old.rec = ''
         readu old.rec from update.voc.f, id then
```

An `ELSE old.rec = ''` on the `READU` would do the same thing and is arguably
clearer about intent; either works.

**How it was found.** Reading `update.voc` while adding a filter to it for the
Windows port. The stale variable was noticed on the way past, and the C side was
then checked to confirm that a failed `READ` really does leave the target alone
rather than emptying it.

---

## 6. `CREATE.FILE` names the file one way on disk and another way in the VOC, so the name it reports back does not work

**Status:** PROPOSED, 18 Aug 2026
**Affects:** `sd64/sdsys/GPL.BP/CREATEF` — `main` and `dev`, identical line
numbers in both
**Severity:** low, self-inflicted by the user's choice of case, but confusing in
a way that is hard to diagnose: the confirmation message names something that
then cannot be used.

Create a file with a lower-case name and `CREATE.FILE` reports:

```
:CREATE.FILE testlc
Created DICT part as TESTLC.DIC
Created DATA part as TESTLC
```

It has upper-cased the name, and says so. But the name it just printed does not
work, while the one that was typed does:

```
:COUNT testlc
0 record(s) counted
:COUNT TESTLC
File not found
```

Nor can the entry be examined under the reported name:

```
:CT VOC testlc     ->  F / TESTLC / TESTLC.DIC
:CT VOC TESTLC     ->  Record 'TESTLC' not found
```

**One command applies two different case policies.** `file.name` is taken from
the command exactly as typed and never folded:

```
108:   file.name = field(token, ',', 1)
```

The VOC record is written under that as-typed name:

```
460:   write voc.rec to voc.f, file.name
```

but the name used on disk — and therefore the paths stored in fields 2 and 3 —
is upper-cased:

```
301:                  os.name = ospath(upcase(file.name), OS$MAPPED.NAME)
374:      os.name = ospath(upcase(file.name), OS$MAPPED.NAME)
```

So the VOC id keeps the user's case while everything else is folded up, and the
two halves disagree. Lookup then hides it: a name is tried as typed and only
then as `upcase()`, which is why the typed form still resolves and the reported
form never can.

**This is not Windows-specific.** The mismatch is between the VOC id and the
stored path, not between the path and the filesystem, so a case-sensitive host
behaves the same way. It was found on a Windows port, but `CREATEF` there is
byte-identical to `main`.

**No fix is proposed, because the right one depends on a policy decision this
project should make rather than a port.** The two halves need to agree, and
either direction does that: write the VOC entry under `upcase(file.name)` so the
entry matches the message and the disk, which is the smaller change; or stop
upper-casing the path so the file is named what the user asked for, which is the
less surprising behaviour. What should not stay is the current split, where the
message reports a name that does not resolve.

**How it was found.** Measuring what `CREATE.FILE` does with a lower-case name,
while scoping a lower-case conversion for the Windows port. The probe file and
its VOC entry were removed afterwards.

## 7. The global catalogue can be written and deleted by any user, because only the spelled-out `GLOBAL` keyword is checked

**Status:** PROPOSED, 18 Aug 2026
**Affects:** `sd64/sdsys/GPL.BP/CATALOG` and `sd64/sdsys/GPL.BP/DELCAT` — checked
on `main`
**Severity:** high. The global catalogue holds the object code SD runs for every
session, `$LOGIN` among them, so writing it is code execution in other users'
sessions and deleting from it stops everybody signing in.

`CATALOG` decides it is working on the global catalogue in two different ways,
and only one of them is checked.

The keyword is checked. `CATALOG` at the `GLOBAL` keyword:

```
case keyword = KW$GLOBAL
   ...
   mode = CAT_GLOBAL
   if system(27) # 0 then stop sysmsg(2001)   ;* requires administrator
```

The name prefix is not. A call name beginning with one of `*`, `!`, `_` or `$`
selects the same mode, in three places (`CATALOG` lines 153, 167 and 178 on
`main`), none of which tests anything:

```
if mode # CAT_PCODE and index(prefix.chars, call.name[1,1], 1) then
   program.name = program.name[2,999]
   if mode and mode # CAT_GLOBAL then stop sysmsg(3021)
   mode = CAT_GLOBAL
end
```

So `CATALOG BP MYPROG GLOBAL` is refused and `CATALOG BP $MYPROG` is allowed,
though they do the same thing. There is no later test: `catalogue.program`
reaches `case mode = CAT_GLOBAL` and writes `gcat` unconditionally.

**`DELETE.CATALOG` tests nothing at all**, by either route — `DELCAT` has no
privilege test anywhere in it, and the same prefix characters route a name to
the global catalogue:

```
case global or index(prefix.chars, cat.name[1,1], 1)
   readvu obj.rec from gcat.f, cat.name, 0 then
      delete gcat.f, cat.name
```

`DELETE.CATALOG $LOGIN` therefore removes the program every session runs.

**Why it is reachable.** On Linux the tree is owned `sdsys:sdusers` with group
write, so an ordinary SD user's own process can write `gcat`; SD does its file
I/O as the invoking user, so no privilege is needed for the write itself. The
BASIC test is the only gate, and for these routes there is none. An account
needs `CATALOG` or `DELETE.CATALOG` in its VOC, which any account doing
development has.

**Suggested fix**, which is what this port did: test once where the mode is
finally known rather than at each place that sets it, so a further route to
`CAT_GLOBAL` inherits the check. In `CATALOG`, after the `begin case no.names`
block and before the object file is opened:

```
if mode = CAT_GLOBAL and system(27) # 0 then
   stop sysmsg(2001)  ;* Command requires administrator privileges
end
```

In `DELCAT`, before the delete loop rather than inside it, so a list mixing
private and global names deletes nothing rather than stopping part way through:

```
if system(27) # 0 then
   gbl.count = dcount(name.list, @fm)
   for gbl.i = 1 to gbl.count
      gbl.name = name.list<gbl.i>
      if global or index(prefix.chars, gbl.name[1,1], 1) then
         stop sysmsg(2001)
      end
   next gbl.i
end
```

`sysmsg(2001)` already exists and is the message `CATALOG` uses for this today.
Local and private cataloguing are untouched by both changes: they write the
account's own `VOC` and `cat`, not `gcat`.

---

## 8. `start_file()` reads six bytes of a print file name that may be shorter than that

**Status:** PROPOSED, 18 Aug 2026
**Affects:** `sd64/gplsrc/to_file.c`, `start_file()` — checked on `main` and
`origin/dev`
**Severity:** low. An out-of-bounds read of at most five bytes, off the heap,
whose result is discarded. It will not normally be noticed; it will be noticed
by a sanitiser or a hardened allocator.

`start_file()` decides whether a print unit is aimed at the account's hold file
by testing the first six characters of the name for `"$HOLD "`:

```c
} else if (memcmp(pu->file_name, "$HOLD ", 6) == 0) {
```

`pu->file_name` is allocated by `alloc_c_string()` at exactly `string_len + 1`
bytes (`strings.c`), and it is set from whatever name the user gave. The
`AS PATHNAME` form of `SETPTR` stores that name unchanged, so

```
SETPTR 1,132,60,0,0,3,AS PATHNAME /tmp
```

leaves a five-byte allocation, and `memcmp` is then given a length of six.
`memcmp` is entitled to read all `n` bytes — implementations commonly compare a
machine word at a time — so this is a read past the end of the allocation, not
merely a redundant comparison. The shortest name a user can supply makes it a
five-byte overread.

**Suggested fix.** Compare only as far as the string actually goes:

```c
} else if (strncmp(pu->file_name, "$HOLD ", 6) == 0) {
```

`strncmp` stops at the terminating NUL, so a shorter name simply does not match.
Nothing else changes: the two agree on every input that is at least six bytes
long, which is every input that could have matched.

This port arrived at the same place from a different direction — it made the
test case-insensitive using SD's own `MemCompareNoCase()`, which compares byte
by byte and returns at the first difference, so the overread went with it. The
one-word `strncmp` change above is the whole fix for upstream and carries no
behaviour change at all.

## 9. `sdtic` carries a failed entry's buffers into the next one, and always exits 0

**Status:** PROPOSED, 19 Aug 2026
**Affects:** `sd64/gplsrc/sdtic.c`, `process_file()` — the terminfo compiler.
Checked against `../sdb64`: the two files differ only in an `O_BINARY` guard, an
`atoi`/`strtol` change and a `strtok`/`strtok_r` change, none of which touch
this.
**Severity:** medium. The visible outcome is a **truncated terminfo database
that the build reports as successful**. A user then meets it as "my terminal
does not work", a long way from the cause.

`process_file()` compiles one entry per iteration. The whole of the "build and
write it out" step is guarded:

```c
    if ((errors == 0) && !skip) {
      ...build the entry, write it out...
      errors = 0;
      reset_buffers();
    }
  }
```

`reset_buffers()` is **inside** that guard. So an entry that produced an error —
or one that `skip` passed over for selective compilation — leaves `strings[]`,
`string_offsets[]` and `str_count` holding its own half-built data, and the next
entry accumulates on top of it. Given enough following entries this runs past
the end of `strings[4096]`.

**Reproduced** by giving one entry a description containing a comma:

```
windows|Windows console (cmd, PowerShell, Windows Terminal),
```

That is malformed source — `get_token()` splits on commas, so `PowerShell` and
`Windows Terminal)` are read as capability names and `lookup()` rejects them —
but the handling is the defect, not the input. Compiling a 62-entry database
with that one entry in it **segfaulted part way through**, leaving 24 of the
100 expected files. Because stdout is block buffered when redirected, not one
of the diagnostics already printed reached the file either, so the operator saw
a bare "Segmentation fault" and a directory that looked plausible.

**Suggested fix.** Move the reset out of the guard, so it runs for every entry:

```c
    if ((errors == 0) && !skip) {
      ...build the entry, write it out...
      errors = 0;
    }

    errors = 0;
    reset_buffers();
  }
```

**A second, separable point.** `errors` is reset per entry, so nothing records
whether the run as a whole succeeded, and `main()` returns 0 regardless. A
makefile cannot tell a complete database from a partial one. Adding a counter
that is never reset, and returning non-zero when it is not zero, turns the
silent case into a build failure:

```
sdtic: 1 terminal definition(s) did not compile - see above.
```

With both changes the same malformed database compiles the other 61 entries
correctly, names the bad one with its line number, and exits 1.


---

## 10. `sdrealpath()` stops resolving at the first component that does not exist, and returns the rest of the path unprocessed

**Status: PROPOSED**

`sdrealpath()` in `gplsrc/linuxlb.c` walks a pathname component by component,
collapsing `.` and `..` and following symlinks as it goes. When `lstat()` on a
component answers `ENOENT` it stops, copies **the remainder of the input string
verbatim** onto what it has resolved so far, and returns:

```c
      if (lstat(outpath, &st) < 0) {
        if (errno != ENOENT)
          return NULL;

        /* Simply glue unrecognised component(s) on the end so that we
          return a fully resolved path of what we might be trying to
          create.                                                      */
        ...
          *(tgt++) = '/';
          strcpy(tgt, p);
        }
        return outpath;
      }
```

Returning something for a path that does not exist yet is deliberate and is
right - a caller creating a file needs it. The defect is that the remainder is
copied **without being processed**, so any `.` or `..` in it survives, and the
returned path is not the absolute form the function's own comment promises.

**How to see it.** Both calls below name the same file, and only the first has
every component present:

```
in   /data/accounts/live/../../sdsys
out  /data/sdsys                                  <- resolved

in   /data/accounts/live/nofile/../../../sdsys
out  /data/accounts/live/nofile/../../../sdsys    <- returned unchanged
```

One non-existent component anywhere in the path is enough, and it does not have
to be the last one.

**Why it matters.** `fullpath()` is the only path-canonicalising function SD
has, and `OSPATH(name, OS$FULLPATH)` is how BASIC reaches it. Two consequences:

1. **Comparing two results is unsound.** Two spellings of the same file can
   come back different, so code that caches, deduplicates or compares resolved
   pathnames can treat one file as two.
2. **Anything using it as a security check is defeated by one made-up name.**
   This is how we found it: we were adding a rule confining a class of session
   to a directory, implemented as "resolve the path, then check it is under the
   permitted root". A path containing a component that does not exist keeps its
   `..` segments, still begins with the permitted root, passes the check, and is
   then resolved by the operating system to somewhere else entirely. The check
   reads as protection and does not protect.

We do not know of a place in `sdb64` today where point 2 is exploitable - the
containment rule is ours and upstream has no equivalent. Point 1 stands on its
own, and point 2 is worth knowing before anyone builds such a check.

**Suggested fix.** Process the remainder through the same loop instead of
copying it. The minimal change is to note that the component was missing and
carry on rather than return - keeping the existing behaviour of producing a
path for something that does not exist, while still collapsing `.` and `..`:

```c
      if (lstat(outpath, &st) < 0) {
        if (errno != ENOENT)
          return NULL;

        /* The component does not exist.  Keep going so that "." and ".."
          later in the path are still collapsed - a caller creating a file
          needs a path back, but it has to be a RESOLVED one.  There is
          nothing to follow, so only the symlink handling is skipped.     */
        continue;
      }
```

with the loop's `p = q + 1` advance moved so that `continue` cannot skip it.

**A caller that wants the old behaviour has a better option anyway**: resolve
the parent directory, which does exist, and append the final component itself.

**If the unresolved form is kept deliberately**, the comment should say so and
say that the result may still contain `..`, because the current one says the
opposite - "a fully resolved path".

**Reported against** `origin/dev`, `sd64/gplsrc/linuxlb.c`, the `ENOENT` branch
of `sdrealpath()`.

---

## 11. `CREATE.ACCOUNT` reports a failure as a positive `@SYSTEM.RETURN.CODE`, which is the range that means success

**Status:** PROPOSED, 21 Aug 2026
**Affects:** `sd64/sdsys/GPL.BP/CREATEA` line 158, and `sd64/sdsys/GPL.BP/ED`
line 57 — `main` and `dev`, identical on both
**Severity:** low but silent, and it fails in the unsafe direction: a caller
that checks whether `CREATE.ACCOUNT` worked is told it did when it did not.

When `CREATE.ACCOUNT USER` cannot create the operating system account, it sets
the return code without negating it:

```
         if not(create_user(acc.uname)) then
           * create user failed
           @system.return.code = ER$NOT.CREATED
           stop sysmsg(10006,STATUS()) ;* Create User Failed, OS Error: %1
```

`gplsrc/err.h` states the convention at the top of the file:

> Commands that set negative error codes into `@SYSTEM.RETURN.CODE` use the
> arithmetic inverse of the values listed below.

`ER$NOT.CREATED` is 6, so this leaves **6** where every other error exit in the
same program leaves **-6**. `CREATEA` assigns `@SYSTEM.RETURN.CODE` in
twenty-five places: twenty-three negate, one is `= 0` on the success path at
line 377, and this is the twenty-fifth.

**The positive range is not unused — it means "this many things were done".**
That is what makes this more than a cosmetic sign error. Across `GPL.BP` a
positive value is a count of work completed:

| Where | What it sets |
|---|---|
| `COPY:271`, `COPYP:160` | `records.copied` |
| `DELETE:162`, `NSELECT:105` | `record.count` |
| `GETLIST:113`, `FORMLST:98`, `MRGLIST:161`, `LSTMRG:160` | a `dcount()` |
| `BASIC:246` | `num.programs` |

So a `CREATE.ACCOUNT` that has just refused to create anything leaves behind a
value indistinguishable from "six records copied".

**And the readers test the sign, not the value.** Two places in the shipped
source ask only whether the number is negative:

```
PROC:677     if.arg1 = if @system.return.code < 0 then 1 else ''
PDEBUG:61    if @system.return.code < 0 then goto abort.pdebug.startup
```

`PROC:677` is how a PROC finds out whether the command it just ran failed. A
PROC that creates accounts and tests for an error after each one is told that a
failed creation succeeded, and carries on. Nothing hides the failure from a
person — message 10006 is printed — but the machine-readable answer contradicts
what the screen says.

**The fix is one character:**

```
           @system.return.code = -ER$NOT.CREATED
```

**The same fault is in `ED`, at line 57:**

```
   @system.return.code = ER$ARGS   ;* Preset for command errors
```

`CREATEA:86` and `DELACC:55` write that identical preset as `-ER$ARGS`, and
`ED` itself clears it to `0` at line 168 on the path that succeeds — so it is
meant as an error value and wants the same minus. It is listed here rather than
as a separate entry because it is one defect with two instances.

**How it was found.** Reading `CREATEA` line by line while making an unrelated
change to the account verbs in a Windows port of SD, and noticing that one
error exit in a file of twenty-five did not look like its neighbours. The
convention was then confirmed from `err.h` rather than assumed, and the meaning
of the positive range from the commands that set it.

**Not verified by running it.** The change is one character on a path that
needs `create_user()` to fail, which is awkward to provoke deliberately; it is
offered on the strength of the convention in `err.h` and of the other
twenty-three sites in the same file.

---

## 12. A login whose `TERM` has no terminfo entry gets no terminal capabilities at all, for the whole of `$LOGIN`

**Status:** PROPOSED, 22 Aug 2026
**Affects:** `sd64/sdsys/GPL.BP/LOGIN` — `main` and `dev`. The mechanism it
relies on is in `sd64/gplsrc/sdtermlb.c`, which needs no change.
**Severity:** cosmetic in effect, but it fires on almost every modern login.
The screen is not cleared at sign-on and any prompt inside the login sequence
has no cursor control — so backspace at such a prompt erases nothing.

### What happens

`LOGIN:79` sets the terminal type and does not check the result:

```
            s = env('TERM')
            if s = '' then s = 'vt100'
      end

      void kernel(K$TERM.TYPE, s)
```

If `$TERM` names a terminal that has no entry in the shipped `terminfo`
directory, that call **fails**, and the failure is silent.

**The consequence is bigger than one missing capability.** `tsettermtype()`
opens the terminfo file first and calls `free_terminfo()` only afterwards
(`sdtermlb.c:169` and `:173`), so a lookup that fails leaves whatever was
loaded before still in place. On the **first** call of a session there is
nothing loaded, so `tinfo` stays `NULL` — and `sdtgetstr()` then returns an
empty string for **every** capability id (`sdtermlb.c:372`), not just for the
one that was asked for. `tio.term_type` is only assigned on success
(`sdtermlb.c:308`), so `@TERM.TYPE` is empty as well.

Everything `$LOGIN` does after that point runs with no terminal capabilities:

* `LOGIN:97`, `display @(-1) :` — the clear screen at sign-on emits nothing.
* `LOGIN:118`, `:348`, `:441` — prompts. Cursor motion, and therefore
  destructive backspace, does not work at any of them.

### Why it has gone unnoticed

The account's VOC `login` paragraph sets the type again — `VOC_TEMPLATE/LOGIN`
field 2 is `TERM LINUX` — and that call succeeds, so from the `:` prompt
onwards everything is correct.

But the paragraph runs **after** the login sequence: `CPROC:284-285` calls
`$LOGIN`, and `CPROC:366` is where the paragraph is read and run. So the
repair always arrives too late for the things listed above, and any test run
from a command prompt sees a session that has already been repaired.

### How likely is it

The shipped `terminfo` directory has `linux`, `ansi`, `vt100` and `xterm`, and
no entry for any of the values a current desktop or terminal multiplexer sets:

| `TERM` | typical source | entry shipped? |
|---|---|---|
| `xterm-256color` | GNOME Terminal, Konsole, most X terminals, most ssh clients | no |
| `screen`, `screen-256color` | GNU screen | no |
| `tmux-256color` | tmux | no |
| `linux` | the kernel virtual console | yes |

So the console is the case that works, and a graphical terminal or an ssh
session from one is the case that does not.

### The fix

Ask for the type, then check it loaded, and fall back to a type that is
shipped. `KERNEL(K$TERM.TYPE, ...)` returns the type in force **after** the
attempt and leaves it unchanged when the attempt fails (`op_kernel.c:220-227`),
so a mismatch is the failure. `settermtype()` lowercases the name it stores
(`sdtermlb.c:153`, `:308`), so the name has to be lowercased before comparing
or an upper-case `$TERM` will not match itself.

Replacing `LOGIN:79`:

```
      s = downcase(s)
      if (kernel(K$TERM.TYPE, s) # s) and (s # 'linux') then
         s = 'linux'
         void kernel(K$TERM.TYPE, s)
      end
```

`linux` to match `VOC_TEMPLATE/LOGIN`, so that the two places that name a
default name the same one. `TERM:245-246` already performs this same test on
these same two calls, for the `TERM` verb — this only brings the login path
into line with it.

**A second fix is possible and is not proposed here:** shipping the missing
terminfo entries, or teaching the lookup to strip a `-256color` suffix and
retry. Either would reduce how often the fallback is needed, but neither
removes the need to check that a lookup succeeded.

### How it was found

Backspace did nothing at a password prompt during installation in a Windows
port of SD, while the same key measured correctly from a command prompt on the
same installation. The difference turned out not to be the terminal but the
moment: the prompt is inside `$LOGIN` and the measurement was taken after it.
Confirmed by lifting the account's `login` paragraph out of the way and reading
the capabilities back: with a `$TERM` that has no entry, `cub1`, `kbs`, `el`
and `cup` all came back zero-length; with one that has an entry, all four were
correct.

---

## 13. `READCSV` leaves a carriage return on the last field of every row of an RFC 4180 CSV

**Status:** PROPOSED, 24 Aug 2026
**Affects:** `sd64/gplsrc/op_seqio.c` — the `memchr(p, '\x0A', bytes)` line in
`op_readseq()`'s normal-file branch (`1147` on `main` at the time of writing)
**Severity:** low, and **the platform caveat belongs at the top**: `sdb64` is
Linux-only, where LF is the norm, so files written locally are unaffected and
most users will never see this. It is an **interop** defect, not a general
reading defect, and that is why this entry is scoped to CSV rather than
written up as "SD reads CRLF files wrongly".

**Why CSV is different from the rest.** RFC 4180 §2.1 specifies **CRLF** as the
record separator, on every platform. So a *conformant* CSV is CRLF even when it
was produced on Linux, and a CSV that arrives from Excel or any Windows tool
certainly is. `qmb_writecsv.htm` and `csv.htm` both state conformance in as
many words — *"QM adheres to the CSV standard (RFC 4180)"* — so this is a claim
the documentation already makes.

**What happens.** `READCSV` compiles to `OP.READSEQ` (`BCOMP`'s `st.readcsv:`
emits `OP.READSEQ` and then parses), and `op_readseq()` searches only for LF:

```c
q = memchr(p, '\x0A', bytes);
if (q != NULL) /* Found a LF.  Copy to but not including LF */
{
  n = q - p;
  ts_copy(p, n);          /* the CR before the LF is still in here */
```

The line therefore keeps the CR, and the CSV parser then splits it on commas.
**Only the last field is affected**, because a comma terminates all the others
and the line terminator terminates only the last — which is what makes it
awkward to notice: `A1,B1<CR><LF>` yields `A1` and `B1<CR>`.

**A suggested fix, and the trap in it.** The obvious patch is to look at the
byte before the LF:

```c
  n = q - p;
  if ((n > 0) && (p[n - 1] == '\x0D'))
    ts_copy(p, n - 1);
  else
    ts_copy(p, n);
```

**That alone is not correct, and this is the part worth reading.** This loop is
fed from a buffer of `SEQ_BUFFER_SIZE`, which is **2048**, and it accumulates
across refills. A CRLF can therefore land with the CR as the last byte of one
buffer and the LF as the first byte of the next, in which case the CR has
already been copied and `p[n - 1]` is not it. At 2 KB that is not a rare edge
case — over a large CSV it is close to certain. A correct fix has to **hold a
trailing CR back** rather than look behind the LF, decide when the next buffer
arrives, and emit it as data if no LF follows (including at end of file, where
a deferred CR would otherwise be dropped).

**Leave a lone CR alone.** A CR that is not followed by LF is data, not a
terminator; stripping every CR would pass a naive test and corrupt records.
`BCOMP`'s own source reader already takes this view — it strips a *trailing*
CR from each line and nothing else.

**Not reproduced against upstream.** Per this file's standing caveat, the
reading above is from upstream's source. It *was* reproduced in the Windows
port, whose code at these lines was byte-identical before the fix: a CSV
planted with CRLF read back with the last field one byte long and ending in
character 13, against an LF control that did not.

---

## 14. `WRITESEQ` to a port sends a bare CR: the byte count is 1 on a two-character literal

**Status:** PROPOSED, 24 Aug 2026
**Affects:** `sd64/gplsrc/op_seqio.c` — `op_writeseq()`'s `SQ_PORT` branch
(`1590` on `main` at the time of writing)
**Severity:** low reach, unambiguous defect. It only affects `WRITESEQ` to a
**port**, so most installations will never execute it — but where it does run,
the line terminator has always been wrong and nothing reports it.

**Unlike entry #13 there is no platform argument here.** This is not about
which line ending a platform prefers; it is a call that does not do what it was
written to do, on Linux exactly as much as anywhere else.

**Upstream today:**

```c
    if (!writeport(fu, "\r\n", 1))
      goto exit_op_writeseq;
```

`writeport()`'s third argument is a **byte count** — `bool writeport(int hPort,
char* str, int16_t bytes)` in `lnxport.c`. So the call passes a two-character
literal and asks for **one** byte: every `WRITESEQ` to a port terminates its
line with a bare **CR**, and the LF is never sent.

**The literal is the statement of intent, and the count contradicts it.** If CR
alone were wanted the string would be `"\r"`. Nothing else in the file
disagrees: `onewline` (`tio.h`) is initialised to `"\r\n"` for character-device
output, which is the conventional terminator for a serial device.

**The fix:**

```c
    if (!writeport(fu, "\r\n", 2))
```

**Note the neighbouring call is correct and should not be changed.**
`op_writeblk()`'s port branch writes `src_str->bytes` and appends no terminator
at all, which is right — `WRITEBLK` is a block write and must not add one.

**Not reproduced, and this one cannot easily be.** Per this file's standing
caveat the reading is from source. It was **not** reproduced even in the
Windows port, because exercising it needs a real port device; the defect is
asserted from the signature of `writeport()` and the length of the literal,
both of which are in the code above. That is weaker evidence than this file's
other entries and is stated rather than glossed.

---

## 15. The BASIC advertises a virtual file system the C has never implemented, so a `VFS:` file pointer is reported as valid and then fails to open

**Status:** PROPOSED, 25 Aug 2026
**Affects:** `sd64/gplsrc/descr.h`, `dh.h`, `err.h`, `kernel.c`, `kernel.h`,
`keys.h`, `op_dio3.c`, `pdump.c`; `sd64/sdsys/GPL.BP/FTYPE`, `_VOC_REF`,
`_EXTENDLIST`; `sd64/sdsys/BP/VFS.CLS` — `main` and `dev`
**Severity:** low, and it is a documentation-and-dead-code problem rather than
a crash. But it misleads: SD tells an administrator that a file pointer is a
valid virtual file system and then refuses to open it with an unrelated error.

**What is there today.** The BASIC half of SD knows about virtual file
systems. The C half does not.

| Where | What it says |
|---|---|
| `GPL.BP/FTYPE:50` | `if upcase(path[1,4]) = 'VFS:' then return ('VFS')` |
| `GPL.BP/_VOC_REF` | a branch that skips absolutising a `VFS:` pathname |
| `SYSCOM/KEYS.H` | `FL$TYPE.VFS 6`, a FILEINFO file type |
| `SYSCOM/ERR.H` | `ER$VFS.NAME` 3038, `ER$VFS.CLASS` 3039, `ER$VFS.NGLBL` 3040 |
| `sdsys/BP/VFS.CLS` | a template VFS class module, shipped to every installation |
| the C open path | ***nothing recognises a `VFS:` pathname at all*** |

`grep -rn 'VFS:' sd64/gplsrc` returns **nothing**. There is no code anywhere in
the C that looks at the first four characters of a pathname for `VFS:`, no
handler is ever loaded, and errors 3038-3040 are defined and **never raised** —
`grep -rn 'ER_VFS_' sd64/gplsrc` finds only the three `#define` lines in
`err.h`.

**So this is what an administrator sees.** Write a VOC F-pointer whose
pathname is `VFS:something`, and:

1. `LISTF` reports its type as `VFS`, because `FTYPE` says so.
2. `_VOC_REF` resolves the name and deliberately leaves the pathname relative,
   because it believes a VFS handler will interpret it.
3. `OPEN` then fails in the C with whatever error a directory named `VFS:`
   produces on the platform — on Linux, a path-not-found.

The first two steps confirm the thing exists. The third denies it. Nothing in
between says "virtual file systems are not supported", because no code
believes that.

**The four internal values, and which of them reach disk.** This is the
question that decides whether the definitions can simply be deleted, and it has
a different answer for each:

| Value | Where | Persisted? |
|---|---|---|
| `VFS_FILE` 5 (`descr.h:318`) | `fvar->type`, the runtime `FILE_VAR` | **No.** And never assigned — `fvar->type` only ever receives `INITIAL_FVAR`, `DIRECTORY_FILE`, `DYNAMIC_FILE`, `SEQ_FILE` or `NET_FILE`. It is read once, at `op_dio3.c:493`, in a guard that cannot fire |
| `SEL_VFS` 2 (`dh.h:154`) | indexes `select_ftype[]`, an in-memory array | **No.** Never assigned and never compared; the `#define` is its only occurrence in the tree |
| `DHF_VFS` 0x40 (`dh.h:105`) | **a file-header bit** — `dh.h:98`, *"LS 16 bits come from file header"* | **Yes, in format** — but never set, and excluded from `DHF_CREATE` (0xB8), so no SD build has ever created a file carrying it |
| `PF_IS_VFS` 0x00200000 (`kernel.h:101`) | **a compiled-object header flag** (`pgm->flags`) | **Yes, in format** — tested at `kernel.c:591`, printed at `pdump.c:227`, and never set: BCOMP has no directive that would set it |

**The fix, and the one rule that goes with it.** Remove the definitions and
their three uses. The uses are all no-ops:

```c
/* op_dio3.c - fvar->type is never VFS_FILE, so the last test is always true */
-  if ((field_no != 0) && (fvar->type != NET_FILE) && (fvar->type != VFS_FILE)) {
+  if ((field_no != 0) && (fvar->type != NET_FILE)) {

/* kernel.c - PF_IS_VFS is never set, so it never selects this branch */
-      || (process.program.flags & (PF_IS_TRIGGER | PF_IS_VFS | HDR_IS_CLASS))) {
+      || (process.program.flags & (PF_IS_TRIGGER | HDR_IS_CLASS))) {

/* pdump.c - drop the two lines that print "VFS handler" */
```

and in the BASIC, drop `FTYPE`'s `VFS:` case and `_VOC_REF`'s branch, so every
pathname is absolutised — which is what the C has always required.

***RETIRE `DHF_VFS`'s 0x40 AND `PF_IS_VFS`'s 0x00200000. DO NOT RECYCLE
THEM.*** Both live in a persisted header format. No SD build ever wrote either,
but a file or an object produced by another MultiValue implementation could
carry the bit, and a future feature that reused the value would then read it as
its own. Leaving a comment where the `#define` was costs nothing:

```c
/* 0x00000040 is RETIRED - do not recycle.  It was DHF_VFS, and it is a
   file-header bit, so a file from another MultiValue implementation could
   carry it.  No SD build ever set it: it is not in DHF_CREATE. */
```

Error numbers 3038-3040 are worth retiring for a second reason: `gplsrc/sdclilib/err.h`
carries its own copy of them, and that is the client library's **public** error
header. Removing codes there is an API change to a shipped library rather than
an internal tidy-up, so this port left that file alone and the numbers stay
claimed.

**Two other pieces of the same feature.** `sdsys/BP/VFS.CLS` is a template
class module for writing a VFS handler — it is shipped to every installation
and describes an interface nothing calls. And `GPL.BP/_EXTENDLIST`, whose own
description says *"Used by the VFS on actions that require a partial list to be
completed"*, is a pcode program that is loaded by name at start-up and never
invoked: `pcode.h` declares `Pcode(extendlist)` and no C source calls
`pcode_extendlist`. (Control for that grep: `pcode_dellist` is called at
`op_dio4.c:137`, so call sites are written literally and the search does find
them.)

**This port has deleted `_EXTENDLIST`, and the two things that made it safe are
worth stating because neither is obvious.** First, `load_pcode()`
(`sd.c:847`) walks the pcode library and matches on
`obj->ext_hdr.prog.program_name` — entries are found **by name**, not by
ordinal — so removing one shifts nothing. `pcode.h`'s own history block already
records the precedent: *"15 Jun 24 mab - remove banner, login, pickmsg, ttyset,
ttyget from pcode"*. Second, the removal has to touch all four places or SD will
not start at all: the `Pcode()` line in `pcode.h`, the name in the pcode build
list, the name in `COMP_PCODE`, and the source record. A `Pcode()` entry with no
library object makes `load_pcode()` print *"Pcode item EXTENDLIST not found"*
and refuse to start, which is at least a loud failure.

**Not reproduced against upstream, per this file's standing caveat.** The
reading is from `sdb64` source. What *was* run is the removal itself, in the
Windows port: with all of the above gone, `make sd` compiles clean with
`-Wall -Wformat=2` and no warning, which is the evidence that nothing depended
on any of it.

**Why upstream might reasonably decline this.** If a VFS implementation is
planned, the right fix is the opposite one — implement the C side, or make
`FTYPE` and `_VOC_REF` say plainly that the feature is not available in this
build. What should not stay is the present state, where two of the three layers
report success and the third fails for an unrelated reason.

## 16. `MICRO` reports "Record is unchanged" when the editor is not installed, and leaves its working copy behind on every exit but one

`GPL.BP/MICRO` runs an external editor on a copy of the record and reads the
copy back. Three faults, all still in `sdb64` as of the clone at
`sdb64/sd64/sdsys/GPL.BP/MICRO`.

**1. Nothing checks that the editor exists.** `Editor = "micro"` is hard-coded
and reached through `execute "!" : editor : ...`. On a machine with no `micro`
the shell escape fails, the working copy is read back unchanged, and the
program prints ***"Record is unchanged"*** and offers `<E>xit or <R>e-edit`.
**That is a confident wrong answer**: the user is told their edit made no
difference when in fact no editor ever ran. Nothing in the output names the
cause, and `micro` is not installed by default on any of the four
distributions ScarletDME targeted.

**2. The working copy is deleted on one exit path out of six.** `delete
TempFile,TempRecordName` is inside `if Response = "E"`. Every other way out —
an empty record, a write error, `<N>o` at the save prompt, a failed read-back,
a missing record name — reaches `End_Program` with the copy still in `$HOLD`.
So a session that goes wrong leaves `<record>.editing` in the user's hold file
permanently, and the next `MICRO` on the same record silently starts from
whatever that stale copy contains rather than from the record.

**3. The editor is given a relative path.** `"'" : TempFileName : "/" :
TempRecordName : "'"` is `$HOLD/name`, which resolves only because the process
happens to be sitting in the account directory. `fileinfo(fvar, FL$PATH)` is
what actually knows where a directory file lives, and it costs one line.

**4. Value and subvalue marks are handed to the editor raw.** Added 27 Aug
2026. `Write TempRecord to Tempfile,TempRecordName` (`MICRO:194`) writes the
record to `$HOLD` exactly as it stands, and `MICRO:184` reads it back the same
way. A **field** mark is fine — a directory file writes one field per line and
the editor sees lines. A **value** mark and a **subvalue** mark are not: they
are `x'FD'` and `x'FC'`, control characters in the middle of a line, and what
becomes of them is entirely up to the editor. Nothing in `MICRO` converts,
escapes, checks or warns.

So `MICRO` on a multivalued record is a silent data risk rather than an error:
an editor that drops the character loses the value boundary, one that
"corrects" it changes the record, and either way the user is asked *"Save?"*
about a record something other than their own editing has already altered.
**The obvious case is a dictionary record**, which is the kind of record
`MICRO` exists to edit and the kind most likely to be multivalued.

**What this port did with it.** Marks are converted to typeable tokens on the
way out and back on the way in — `~~` for a value mark, `` ~` `` for a
subvalue mark, `~-` for a literal tilde where one would otherwise be misread —
and the conversion is lossless for every record, proved over every arrangement
of those characters and over all 197 shipped source records before it was
built. `sdsys/gpl.bp/EDIT`, `escape.tildes` and `process.record`. A **text**
mark is still passed through raw and that is stated rather than hidden.

**What this port did with the rest of it, for whatever it is worth to
upstream.** `MICRO`
was removed here on 17 Aug 2026 on a containment argument — an external editor
is a way out of SD — and brought back on 26 Aug 2026 as `EDIT`, rewritten with
all three fixed and gated on the account tier rather than on the `OS.USERS`
shell list. The rewrite is `sdsys/gpl.bp/EDIT` and its header records what
changed and why, line by line, so the three fixes can be lifted without taking
the Windows-specific parts.

**Not reproduced against upstream, per this file's standing caveat.** Fault 1
was reasoned from the source and from the absence of any `micro` check;
faults 2 and 3 are structural and readable in the same file.

---

## 17. `COMMIT` never ends the transaction it commits: the level counter only ever climbs, and a nested `COMMIT` silently loses the outer transaction's writes

Two symptoms, one cause. Both measured in this port, and the code is identical
in `sdb64` — `main` and `dev` both have `txn_depth++` at `txn.c:96` and
`txn_depth--` only at `txn.c:592`, inside `rollback()`.

**`op_txncmt()` does not undo what `op_txnbgn()` did.** `op_txnbgn()` does two
things: it increments `txn_depth`, and — if a transaction is already running —
it pushes the running one onto `txn_stack`. `op_txncmt()` writes the cache out,
clears `process.txn_id` and releases the locks, and then returns. **It does not
decrement `txn_depth` and it does not pop `txn_stack`.** The only place either
happens is `rollback()`, which `op_txnend()` calls.

**And `COMMIT` is compiled as a jump past `END TRANSACTION`.** `BCOMP`'s
`st.commit` emits `OP.TXNCMT` and then jumps to the transaction's exit label,
which is after the `OP.TXNEND` that `BEGIN TRANSACTION` emitted at the end
label. So on the committed path `op_txnend()` never runs, and nothing ever
reverses the two effects.

**Symptom 1 — `SYSTEM(1008)` is wrong for the rest of the session.** Key 1008
returns `txn_depth` (`op_sys.c`). Measured, four transactions in one program,
**none of them nested**:

| | |
|---|---|
| first transaction, inside | `SYSTEM(1008)` = **1** |
| after its `COMMIT` | **1** — not 0 |
| fourth transaction, inside | **2** |
| after a `ROLLBACK` | back to the value before it — rollback is balanced |

So a program cannot ask "am I in a transaction?" with key 1008. `SYSTEM(1007)`
is correct — it is `process.txn_id`, and `op_txncmt()` does clear that.

**Symptom 2 — a nested `COMMIT` abandons the outer transaction, and its writes
are lost with no message.** Measured: an outer transaction wrote `R2`, an inner
one wrote `R3` and committed, then the outer one committed.

| | |
|---|---|
| the inner record `R3` | `inner` — landed |
| the outer record `R2` | ***unchanged — the write vanished*** |
| `SYSTEM(1007)` after the inner `COMMIT` | **0** — the session is in no transaction at all |
| `SYSTEM(1008)` delta over the pair | **+2** |

The inner `COMMIT` sets `process.txn_id = 0` and leaves the outer transaction's
cache on `txn_stack`, orphaned. The outer `COMMIT` then commits an empty cache.
**The all-or-nothing guarantee is not merely weakened here, it is inverted**:
part of the transaction lands and part does not, which is the one outcome a
transaction exists to prevent.

**A fix has to cover both, and the second is the dangerous one.** Decrementing
`txn_depth` in `op_txncmt()` fixes symptom 1 on its own; symptom 2 needs the
`txn_stack` pop as well, so that a nested `COMMIT` reinstates the parent
transaction rather than ending all of them. Either `op_txncmt()` takes over
that bookkeeping, or `st.commit` stops jumping past `OP.TXNEND` — but note that
`op_txnend()` as written calls `rollback()` unconditionally, so it cannot
simply be allowed to run after a commit.

**Reproduced in this tree, not against upstream**, per this file's standing
caveat. Probe: `tools/probes/p14c-txn.b` in the `SDCoreWindowsDocs` repository.

***FIXED IN THIS PORT, 29 Aug 2026, AND THE SHAPE MAY BE USEFUL TO YOU.*** The
reinstate-and-decrement block at the foot of `rollback()` is lifted into a
`Private void end_txn_level(void)` and called from `op_txncmt()` as well, so
both halves of `op_txnbgn()` are undone on the committed path. **One function
with two callers rather than a second copy** — the defect was precisely that
this bookkeeping existed in one place with one caller.

**The call is placed BEFORE `op_txncmt()`'s `exit_op_txncmt:` label**, so the
three `k_error()` paths do not pop a level they did not commit. Note that this
leaves a separate pre-existing gap in `sdb64` as well: on those error paths
`process.txn_id` has already been zeroed at the top of `op_txncmt()`, so
`txn_abort()` and `op_txnrbk()` find nothing to roll back and the level stays
counted. That one is not addressed here.

**`st.commit` is untouched** — the BASIC compiler still jumps past
`OP.TXNEND`, which stays correct, because `op_txnend()` calls `rollback()`
unconditionally and must not run after a commit.

Measured on the fixed build: the outer record's write lands where it was
previously lost, `SYSTEM(1008)` is balanced across the pair where it climbed by
2, and `SYSTEM(1007)` names the parent transaction after the inner commit where
it read 0.

`FIXED HERE — PROPOSED UPSTREAM`

---

## 18. `CONFIG()` with a name longer than eight characters returns an uninitialised descriptor, and the caller aborts on a value that was never written

`op_config.c`, identical on `sdb64` `main` and `dev`:

```c
  char param[8 + 1];
  DESCRIPTOR result;
  ...
  descr = e_stack - 1;
  if (k_get_c_string(descr, param, 8) < 1)
    goto exit_op_config;

  InitDescr(&result, INTEGER);      /* <-- skipped by the goto above */
  result.data.value = 0;
  ...
exit_op_config:
  k_dismiss();
  *(e_stack++) = result;            /* <-- pushes whatever was on the stack */
```

**The early exit jumps over the only initialisation of `result`.** A name that
does not fit the nine-byte buffer takes that path, and the automatic
`DESCRIPTOR` is pushed onto the e-stack with whatever type byte happened to be
in that stack slot.

Measured in this port: `CONFIG('NOSUCHKEY')` — nine characters — aborted the
program with ***"Data cannot be converted to a string"***. The same call with
eight characters is well behaved: an unknown eight-character name falls through
to the final `else` and returns an empty string with `ER_NOT_FOUND`, and that
is what a long name should do too.

**It is a two-line fix**: move the `InitDescr` pair above the
`k_get_c_string()` test, or set `process.status = ER_NOT_FOUND` and initialise
before the `goto`. `op_pconfig()` has the same `char param[8 + 1]` at the same
offset and is worth reading at the same time.

**Not a security issue, but not a tidy one either** — what is pushed is
whatever the previous e-stack user left, so the failure is not reproducible
from the source alone and will differ between builds.

**Reproduced in this tree, not against upstream.** Probe:
`tools/probes/p16c-config.b`.

***FIXED IN THIS PORT, 26 Aug 2026, and the fix is three lines.*** The
`InitDescr` pair moved above the `k_get_c_string()` test so no path can reach
the tail with `result` unwritten, and the early exit now returns **the same
shape as the final else** — an empty `STRING` with `ER_NOT_FOUND` — rather than
the integer zero the initialisation sets. A name that is too long is a name
that does not exist, and a caller should not be able to tell those two apart.
`gplsrc/op_config.c`; the comment at the site says the same thing. **The same
`char param[8 + 1]` is in `op_pconfig()` and was left alone** — it is a
different function with a different tail and nobody has measured it.

`PROPOSED`

---

## 19. `SET.SOCKET.MODE(s, SKT$INFO.KEEP.ALIVE, 0)` reports success and enables keep-alive

`op_skt.c`, `op_setskt()`, unchanged on `sdb64` `main`:

```c
    case SKT_INFO_KEEP_ALIVE:
      GetInt(descr);
      n = (descr->data.value != 0);
      n = TRUE;                       /* <-- the argument is discarded */
      setsockopt(sockvar->socket_handle, SOL_SOCKET, SO_KEEPALIVE, ...);
```

The value the caller passed is read, converted, and then overwritten
unconditionally. The function returns 1 — success — because `process.status`
is untouched.

Measured in this port on an accepted connection:

| | |
|---|---|
| `SET.SOCKET.MODE(s, 6, 0)` | returned **1** |
| `SOCKET.INFO(s, 6)` afterwards | **1** — keep-alive is on |

`SOCKET.INFO` reads the real socket option with `getsockopt()`, so the two
disagree and the enquiry is the one telling the truth. The other two keys in
the same `switch` — blocking and `TCP_NODELAY` — both honour their argument,
so this reads as a debugging line left behind rather than a decision.

**The fix is to delete the `n = TRUE;` line.** Anything that relies on turning
keep-alive off — a short-lived connection through a NAT with a low idle
timeout, a test — is silently getting the opposite today, and being told it
worked.

**Reproduced in this tree, not against upstream.** Probe:
`tools/probes/p15-sockets.b`.

***FIXED IN THIS PORT, 26 Aug 2026, by deleting the line.*** `gplsrc/op_skt.c`;
the comment left in its place records what the measurement was, so the next
reader does not have to wonder whether the line was load-bearing.

`PROPOSED`

---

## 20. Message 1407 tells a user the disk may be full when the real fault is a missing lock

`sdsys/MESSAGES/1407` is, in `sdb64` as here:

```
1407:1:Error %d (o/s %d) writing record (Possible full disk?)
```

It is used for every failure of a `WRITE`, and one of those failures has
nothing to do with the disk. `op_dio3.c` refuses a write or a delete with
`ER_NOLOCK` (**3023**, *"attempt to write/delete record with no lock"*)
whenever the caller is inside a transaction or `MUSTLOCK` is configured:

```c
  if (pcfg.must_lock || (txn_id != 0)) {
    if (!check_lock(fvar, lock_id, id_len)) {
      process.status = -ER_NOLOCK;
```

So the first time an application wraps an existing, working `WRITE` in a
transaction without taking the lock first, the program aborts with:

```
Error 3023 (o/s 0) writing record (Possible full disk?)
```

**The number is right and the sentence is misleading**, and it is misleading in
the direction that costs the most time: it sends the reader to check disk
space, on a machine where the same write succeeded a moment earlier outside the
transaction. The o/s error is `0`, which is the tell, but only for somebody who
already suspects the message.

**The cheapest fix is to special-case 3023 at the call site** — the status is
in hand there — rather than to reword 1407, which is accurate for the
disk-full case it was written for. A second message id costs nothing.

Worth saying plainly because it is the rule as much as the message: **inside a
transaction every record written or deleted must already be locked by the
session**, and outside one no lock is needed at all. That difference is what
makes this failure appear late, in production, in code that has been tested.

**Reproduced in this tree, not against upstream.** Probe:
`tools/probes/p14c-txn.b`, section 6.

**Fixed here on 31 Aug 2026, by the route this entry recommends** — the call
site special-cases the status rather than rewording 1407, which stays accurate
for the disk-full case it was written for. `op_dio3.c`'s `exit_op_write` now
reads:

```c
    if (process.status == -ER_NOLOCK)
      k_error(sysmsg(10151), -process.status);
    else
      k_error(sysmsg(1407), -process.status, process.os_error);
```

New message **10151** names the missing lock, says nothing was written, and
points at `READU` / `READVU`. Re-confirmed live on upstream `main` at `ae0cc5f`
— same call site, same message text — immediately before the change here.

**One caveat for whoever takes this upstream**: only `ER_NOLOCK` is split out.
`ER_RDONLY`, `ER_IID` and `ER_TRIGGER` still render through 1407 and are still
wrong about the disk; each wants its own text rather than a shared one.

`FIXED HERE — PROPOSED UPSTREAM`

## 21. `QSELECT` prints its completion message with the list number missing

`sdsys/MESSAGES/3261` takes two parameters, in `sdb64` as here:

```
%1 record(s) selected to select list %2
```

`NSELECT` supplies both. `QSELECT` supplies only the first:

```
NSELECT:108   display sysmsg(3261, record.count, to.list)   ;* correct
QSELECT:231   display sysmsg(3261, @system.return.code)     ;* %2 never supplied
```

So every successful `QSELECT` ends its line with a dangling *"select list "*
and no number:

```
:qselect voc saving 3
14 record(s) selected to select list
```

**It matters more than a cosmetic blemish because the list number is the one
piece of information the user needs next.** `QSELECT` takes `TO n`, so the
result may be in any list from 0 to 10, and the message whose job is to say
which one is silent about it. The value is in hand at the call site — `tgt.list`
is what the line above it passes to `FORMLIST`:

```
   formlist list to tgt.list
   @system.return.code = selectinfo(tgt.list, SL$COUNT)
   display sysmsg(3261, @system.return.code)
```

**The fix is one line**, and `NSELECT` two files away is the model:

```
   display sysmsg(3261, @system.return.code, tgt.list)
```

**Measured on SD Core for Windows W1.0-0**, both with the default target and
with an explicit `TO 2`; the number is absent either way, while `SELECT` and
`NSELECT` print theirs correctly in the same session. Line numbers above are
`sdb64`'s (`QSELECT:231`); this tree has the same statement at `QSELECT:240`.

`PROPOSED`

## 22. `DELETE.INDEX` will not match an index name typed in lower case, though `LIST.INDEX` will

Index names are held in upper case — `indices()` returns `F1` for an index
created as `create.index zzak f1`, and `CREATE.INDEX` says so when it makes one:
*"Added index for F1"*.

`LIST.INDEX` upcases both sides before comparing:

```
LISTI:138   u.ak.names = upcase(ak.names)
```

`DELETE.INDEX` compares what the user typed against the stored names with an
exact `LOCATE`, and does not:

```
DELETEI:149   locate ak.names<i> in ak.list<1> setting pos else continue
```

So on the same file, in the same session:

```
:list.index zzak f1
Alternate key indices for file zzak
Number of indices = 1
Index name...... En Type Nulls S/M Fmt Field/Expression
F1                Y  D    Yes   S   L  1

:delete.index zzak f1
Unrecognised index name (f1)
```

**The two commands disagree about what the index is called**, and the one that
finds it is not the one that can remove it. `ALL` works either way, which is
what makes this easy to miss — the failure only shows up when somebody names an
index individually.

**The fix is the line `LIST.INDEX` already has.** Upcase `ak.list` where it is
gathered, or compare against `upcase(ak.names<i>)`; either matches the existing
behaviour of the sibling command.

**Measured on SD Core for Windows W1.0-0.** Line numbers are `sdb64`'s; this
tree has the same `LOCATE` at `DELETEI:155` and the same `upcase` at
`LISTI:147`.

`PROPOSED`

## 23. `DELETE.FILE ... NO.QUERY` still prompts when part of the file is in the system account

`DELETE.FILE` accepts `NO.QUERY` and honours it for its own confirmations. It
does not reach the one prompt a script is most likely to hit unattended:

```
DELETEF:208   gosub check.sdsys.file
DELETEF:283   gosub check.sdsys.file
```

Neither call is guarded, and `check.sdsys.file` prompts unconditionally:

```
WARNING: The dictionary part of this file is in the system account
Enter Y to delete this file. This may affect other accounts.
Enter N to delete VOC reference but leave the file in the system account.
Delete the file from the system account (Y/N)?
```

**A file created with `USING DICT` on a system file reaches this every time**,
so `DELETE.FILE name FORCE NO.QUERY` blocks for ever in any non-interactive
session — a build script, a test harness, or anything driving SD down a pipe.

***THE QUESTION ITSELF IS WORTH ASKING AND THAT IS NOT WHAT IS BEING
REPORTED.*** Deleting a file out of the system account can affect other
accounts and deserves a human. The defect is that **`NO.QUERY` says it has
already answered the questions and has not**, so the caller has no way to say
*"do not touch the system account"* other than by not calling the verb.

**Either honour `NO.QUERY` here by taking the safe branch** — delete the VOC
reference and leave the system file alone, which is the `N` answer and the
conservative one — **or reject the combination up front** with a message saying
this file cannot be deleted non-interactively. Both are better than a prompt
nobody can answer.

**Measured on SD Core for Windows W1.0-0.** Line numbers are `sdb64`'s; this
tree has the same two unguarded calls at `DELETEF:222` and `DELETEF:297`.

`PROPOSED`

---

## 24. `TERM DEFAULT` sets the MINIMUM width, not the default width

`GPL.BP/TERM`, the `KW$DEFAULT` arm:

```
      case keyword = KW$DEFAULT                  ;* TERM DEFAULT
         width = MIN.WIDTH
         depth = if @term.type = 'sdterm' then 25 else 24
```

`GPL.BP/INT$KEYS.H` defines six constants, six lines apart:

```
      $define MIN.WIDTH           20
      $define DEFAULT.WIDTH      120
      $define MAX.WIDTH        32767
      $define MIN.DEPTH           10
      $define DEFAULT.DEPTH       36
      $define MAX.DEPTH        32767
```

***THE VERB CALLED `DEFAULT` USES `MIN.WIDTH` WHERE `DEFAULT.WIDTH` IS PLAINLY
MEANT***, and hard-codes 24 rather than `DEFAULT.DEPTH`. The result is that
`TERM DEFAULT` sets the page to **20 x 24** — the narrowest SD will accept.

**`LOGIN` uses the right pair**, which is what makes this a slip rather than a
disagreement about what the default is:

```
      s = env('LINES');
      if not(s matches '1N0N') then s = terminfo('lines')
      if s <= 0 then s = DEFAULT.DEPTH
      setpu PU$LENGTH, -1, max(s, MIN.DEPTH)

      s = env('COLUMNS');
      if not(s matches '1N0N') then s = terminfo('cols')
      if s <= 0 then s = DEFAULT.WIDTH
      setpu PU$WIDTH, -1, max(s, MIN.WIDTH)
```

So a session that starts with nothing to go on gets 120 x 36, and typing
`TERM DEFAULT` in that same session narrows it to 20 x 24.

***IT MATTERS MORE THAN A COSMETIC DEFAULT WOULD.*** SD's shipped `@` dictionary
records and default `LIST` layouts are formatted for 120 columns - the changelog
records that work explicitly - so a page of 20 columns wraps every standard
report. A user who runs `TERM DEFAULT` to "put things back" makes the display
worse and has no reason to suspect the verb.

**The fix is two lines**: `width = DEFAULT.WIDTH` and `depth = DEFAULT.DEPTH`.

**Measured on SD Core for Windows W1.0-0** - `term default` then `term`
reported `Page width: 20`, `Page depth: 24`. Upstream `sd64/sdsys/GPL.BP/TERM`
carries the identical three lines at 164-166 and the identical constants at
`INT$KEYS.H:37-42`, so this is not a port artefact.

***FIXED IN THIS PORT, 27 Aug 2026 — AND MEASURED.*** `gpl.bp/TERM`'s
`KW$DEFAULT` arm now sets `DEFAULT.WIDTH` / `DEFAULT.DEPTH`. The `sdterm`
depth-25 special case was removed rather than kept: a default that depends on
the terminal type is not a default, and it paired with the same `MIN.WIDTH`
slip. **Built and installed the same day; `term default` then `term` now reports
`Page width: 120`, `Page depth: 36`** where the same pair of commands reported
`20` / `24` before. Two lines, and the whole of the fix.
PRE_RELEASE_FIXES #23.

`PROPOSED`

## 25. `sd -cleanup` never releases a dead process's task locks

`remove_user()` in `gplsrc/clopts.c` gives back everything a lost process was
holding. It takes the dead user's number from the user table entry it was
handed:

```c
Private void remove_user(USER_ENTRY* uptr) {
  ...
  user_no = uptr->uid;
```

and then uses `user_no` for the file locks, the record locks and the group
locks. **The task-lock loop, which comes first, uses a different variable:**

```c
  /* Give away process locks */

  for (i = 0; i < 64; i++) {
    if (sysseg->task_locks[i] == process.user_no)
      sysseg->task_locks[i] = 0;
  }
```

`process.user_no` is **the cleaning process's own** user number, not the dead
one's. So the loop clears the wrong process's task locks, and the dead
process's stay set.

***IT IS WORSE THAN "CLEARS THE WRONG ONES", BECAUSE OF WHERE IT RUNS.***
`cleanup()` attaches to the shared segment and walks the user table; it never
becomes a user, so `process.user_no` is zero. A free task lock slot is also
zero. The loop therefore matches every **free** slot and sets it to zero again
— a complete no-op — and **no task lock is ever released by cleanup at all.**

**The consequence is a lock that outlives every recovery an administrator has.**
`LIST.LOCKS` shows the number owned by a user number nothing is behind;
`CLEAR.LOCKS` refuses it because it is not the caller's; the process it belongs
to cannot release it because it is dead. The only ways out are
`UNLOCK TASKLOCK n`, which is the forced form and needs administrator rights,
or restarting SD. A program that guards a nightly job with `LOCK 3` and is
killed while holding it will not run again.

**The fix is one word**: `process.user_no` → `user_no`, matching the three
loops below it in the same function.

`kill_process()` in `gplsrc/kernel.c` does the equivalent thing correctly for a
process that ends normally — there `process.user_no` **is** the right variable,
because the process is releasing its own. That is very likely where the line
was copied from.

**Read in this port's tree and confirmed identical on upstream `main`** at
`sd64/gplsrc/clopts.c:299-302`. Not reproduced against upstream — see the note
at the head of this file — but the reasoning needs nothing outside the twelve
lines quoted.

**Fixed here on 31 Aug 2026**, exactly as described above — `process.user_no`
becomes `user_no`, one word, in the task-lock loop of `remove_user()`. Nothing
else in the function changed. Re-confirmed live on upstream `main` at commit
`ae0cc5f` immediately before the change was made here.

`FIXED HERE — PROPOSED UPSTREAM`

## 26. `ENCRYPT.FIELD` is in every administrator's VOC and the program behind it does not exist

`sdsys/VOC_TEMPLATE/ENCRYPT.FIELD` is a catalogued verb pointing at `$CRYPTO`:

```
V
CA
$CRYPTO
6
```

***THERE IS NO `$CRYPTO` ANYWHERE IN THE DISTRIBUTION.*** No source in
`sdsys/GPL.BP`, nothing tracked under that name at all — checked with
`git ls-tree -r --name-only main`, which finds no file whose name contains
`CRYPTO` on either side.

Typing the verb produces a loader error rather than anything a user can act on.
Measured on this port, where the VOC record and the missing program are the
same ones:

```
:encrypt.field
00001FCB: Unable to load '$CRYPTO' object code at line 1550 of $CPROC
```

**It fails at the point of loading, so no argument form behaves any better**,
and the message names `$CPROC` and an internal line number rather than the verb
that was typed.

**Two ways to close it**, and the choice is upstream's: ship the program, or
remove the VOC record. **Removing it is the smaller change and the honest one**
— a name that is not recognised is a better answer than a loader error, and
`ENCRYPT.FIELD` is not documented anywhere in the distribution, so nothing
would break.

`PROPOSED`

## 27. `DELETE.FILE ... NO.QUERY` also prompts whenever the stored path differs from the name as typed, which `CREATE.FILE` guarantees for a lower-case name

**Separate from #23, which is the system-account prompt.** This one is on the
ordinary path and fires for a file in the caller's own account.

`GPL.BP/DELETEF` compares the pathname held in the VOC record against the file
name the caller typed, and asks about the difference:

```
            default.path = file.name

            if data.path # default.path then
               if not(force) then
                  loop
                     display sysmsg(6135, data.path) :  ;* OK to delete DATA portion 'xx'?
                     input yn
```

***THE GUARD IS `FORCE` ALONE. `NO.QUERY` IS NOT TESTED*** — here, or at the
matching test for the dictionary part a little further down. Both prompt.

***AND `CREATE.FILE` MAKES THE TWO DIFFER BY DEFAULT.*** Unless the
`CREATE.FILE.CASE` option is set, `GPL.BP/CREATEF` upper-cases the operating
system name before storing it in VOC field 2:

```
   if option(OPT.CREATE.FILE.CASE) then
      os.name = ospath(file.name, OS$MAPPED.NAME)
   end else
      os.name = ospath(upcase(file.name), OS$MAPPED.NAME)
   end
```

while `DELETEF` keeps `file.name` exactly as the caller typed it whenever the
VOC read at the top of `delete.file` succeeded. **So `CREATE.FILE mydata`
followed by `DELETE.FILE mydata NO.QUERY` prompts twice** — once for the data
part, once for the dictionary — where `CREATE.FILE MYDATA` and
`DELETE.FILE MYDATA NO.QUERY` prompt not at all. The only difference is the
case the user typed.

**Measured on this port**, where the two prompts were captured rather than
answered from a terminal:

```
OK to delete DATA portion 'ZZLK31A'? Y | DATA portion 'ZZLK31A' deleted |
OK to delete DICT portion 'ZZLK31A.DIC'? Y | DICT portion 'ZZLK31A.DIC' deleted |
VOC entry 'zzlk31a' deleted
```

The last line is the tell: the VOC id is `zzlk31a` and the paths are
`ZZLK31A`. **An earlier run without the stacked answers hung**, ate the
commands that followed, and left a user-table entry that needed an elevated
`sd -cleanup`.

**The point of the test is worth keeping** — a file whose data lives somewhere
other than the default place is worth confirming before deleting. **Comparing
case-insensitively is what makes it mean that**, since a name that differs only
in case is the default place. Honouring `NO.QUERY` as well as `FORCE` would be
the smaller fix and would leave interactive behaviour unchanged.

**Confirmed identical on upstream `main`**: `sd64/sdsys/GPL.BP/DELETEF:219-225`
and `sd64/sdsys/GPL.BP/CREATEF:371-375`, the block commented *Form operating
system file name from VOC record name*. Upstream is upper-case-first by
convention, so the case is rarer there than here, and the code is the same.

`PROPOSED`

---

## `NEWVOC/$MAP` has no file type code, so SDSYS's VOC ships a broken record — WITHDRAWN, and the premise was measured false

**Status:** **CLOSED 29 Aug 2026. Nothing to send, and this one must NOT go
upstream as it was written.** Measured against a live install of this port
rather than reasoned about. Three things below are wrong:

- ***`VOC_TEMPLATE`, NOT `NEWVOC`, IS WHAT BECOMES SDSYS's OWN VOC***, so SDSYS
  ships `$MAP` **with** its `F`. Read out of the live VOC at byte level, and
  stated outright in this port's `gplbld/stage.py:119`.
- ***`NEWVOC` CARRYING THE DESCRIPTION IN FIELD 1 IS A CONVENTION ACROSS THE
  WHOLE DIRECTORY***, not a defect in one record. `NEWVOC/basic` reads
  `Verb to compile SDBasic program` where `VOC_TEMPLATE/basic` reads `V`.
- ***AND THE DESCRIPTION'S FIRST CHARACTER IS THE TYPE CODE — THAT IS THE WHOLE
  CONVENTION.*** `GPL.BP/CREATEA` replaces field 1 with its own first character
  as it writes the account's VOC record — `rec<1> = if upcase(rec[1,1]) = 'P'
  then rec<1>[1,2] else rec[1,1]`, two characters for a `P` type. So
  `File for MAP output` becomes `F` and `Verb to compile SDBasic program`
  becomes `V`. Confirmed on a live account: its `$MAP` holds `F`, with **zero**
  occurrences of the description text anywhere in its VOC. **Measured across the
  directory: 392 of 392 `NEWVOC` first characters equal `VOC_TEMPLATE`'s type
  code, 0 mismatches** — the invariant holds, and it is the reason the file can
  carry a description in a type-code field at all.
- ***THE `LISTF` DESCRIPTION COLUMN IS A LOOKUP INTO `NEWVOC`, NOT A FIELD OF
  THE RECORD.*** `VOC.DIC`'s `Description` item is `IF @ = '' THEN F1 ELSE @`
  over `NEWVOC`. **The control that proves it**: neither `File for MAP output`
  nor `File - Vocabulary` appears anywhere in SDSYS's VOC file, while `LISTF`
  displayed both. So the column showing `File for MAP output` was `NEWVOC`
  being read exactly as intended — **the reported symptom was the feature.**

Kept because the *method* is the reusable part: ***"the same record shipped
twice and only one copy is right" is what a directory-wide convention looks
like when exactly one record is examined.*** The entry as originally written
follows, unaltered.

`sd64/sdsys/NEWVOC/$MAP` reads:

```
File for MAP output
@SDSYS/$MAP
@SDSYS/$MAP.DIC
```

Field 1 of a VOC file record is the **type code**, and every other file record
has `F` there. This one has the description instead, and there is no `F`
anywhere in the record.

**Your own tree contains the corrected version of the same record.**
`sd64/sdsys/VOC_TEMPLATE/$MAP` is:

```
F
@SDSYS/$MAP
@SDSYS/$MAP.DIC
```

— identical but for the missing first field. So the record ships twice and only
one copy is right.

**What it looks like on a running system.** `LISTF` reports the record as an
error rather than as a file:

```
$MAP                 Err 30   File for MAP output   @SDSYS/$map   @SDSYS/$map.dic
                     01
```

The description column is showing field 1, which is the symptom: the reader has
taken `File for MAP output` as the type code, failed to recognise it, and
reported an error. The `$MAP` and `$MAP.DIC` directories both exist on disk, so
this is the VOC record and not a missing file.

**Found** while cleaning unrelated dead VOC records out of SDSYS: once those
were gone, `$MAP` was the only error record left, on an otherwise clean install.

**The fix is to put `F` in field 1 of `NEWVOC/$MAP`**, matching
`VOC_TEMPLATE/$MAP`. Worth checking at the same time which of the two files
feeds SDSYS's own VOC, since only one of them is producing this.

***— END OF THE ORIGINAL ENTRY. THE FIX IT PROPOSES WOULD HAVE BROKEN A WORKING
FILE.*** The check it asked for in its own last sentence is the one that killed
it: `VOC_TEMPLATE` feeds SDSYS, `NEWVOC` field 1 is the description, and pasting
`F` over it would have deleted `$MAP`'s description and left it the single
inconsistent record in the directory.

**And the `Err 30` does not reproduce.** Re-run on a rebuilt install, `LISTF`
shows `$MAP` as **`DH`** with both pathnames resolved. `Err 30` came from a
failed `openpath` on **field 2** — byte-identical in both copies — so field 1
was never a candidate cause; the original reading took the description column
for the type code and reasoned from there.

***THE METHOD FAILURE WORTH KEEPING.*** Three files were compared as though
they did one job. `VOC_TEMPLATE` field 1 is a **type code**, `NEWVOC` field 1 is
a **description**, and the `LISTF` column is a **lookup into the latter**.
Reading one record out of one of them, against one record out of another, made
a deliberate design look like a shipped defect — and every sentence of the
report above is individually accurate.

---

## 28. `k_error()` truncates every message to about 84 characters, on a buffer sized for 241

`gplsrc/k_error.c` builds the error text in a buffer sized from the **product**
of the two constants, and then bounds the write with their **sum**:

```c
  char s[(MAX_ERROR_LINES * MAX_EMSG_LEN) + 1];   /* 3 * 80 + 1 = 241 */
  ...
  vsnprintf(&(s[n]), (MAX_ERROR_LINES + MAX_EMSG_LEN) + 1,  message, arg_ptr);
                   /* 3 + 80 + 1 = 84 */
```

`MAX_ERROR_LINES` is 3 and `MAX_EMSG_LEN` is 80 (`gplsrc/sddefs.h`), and the
comment beside the declaration says *"Max 3 lines"*. So the buffer is deliberately
sized for three 80-column lines, and the writer is told it has room for one.

**Every message that goes through `k_error()` is cut at roughly 84 characters.**
Nothing in the shipped message set is long enough for it to be obvious, which is
presumably why it has survived: it looks like the messages are simply short.

It came to light here while adding a longer one. The rendered result was:

```
000000E5: Error 3023 writing record: no lock is held on it.
A WRITE must already hold an u
```

cut mid-word, losing the sentence that told the reader what to do about it.

**The fix is not to correct the typo.** Changing the `+` to a `*` would pass 241
— but `n` already holds the length of a `"%08X: "` offset prefix written into
`s` a few lines earlier, so `vsnprintf` would then be free to write to `n + 241`
in a 241-byte buffer. That converts a truncation into a buffer overflow.

**Use the buffer's own size instead**, which stays correct if either constant
ever changes:

```c
  vsnprintf(&(s[n]), sizeof(s) - n,  message, arg_ptr);
```

Note `n` is 0 on the branch that writes no prefix, so the expression is right on
both paths.

**Fixed here on 31 Aug 2026** exactly as above. Confirmed identical on upstream
`main` at commit `ae0cc5f`, `sd64/gplsrc/k_error.c:207`.

`FIXED HERE — PROPOSED UPSTREAM`

## 29. A failed header flush marks the file clean, so the retry never happens

`dh_flush_header()` in `gplsrc/dh_file.c` clears the "this file has unsaved
changes" flag **before** doing the work that can fail, and every failure path
returns before the flag is restored.

```c
bool dh_flush_header(DH_FILE* dh_file) {
  ...
  if (((dh_file->flags & FILE_UPDATED) || fptr->stats.reset) && ...) {
    dh_file->flags &= ~FILE_UPDATED;          /* :501  cleared up front */

    ...
        return FALSE;                          /* :507  FDS open failed  */
    ...
    if (!read_at(...))  return FALSE;          /* :517                   */
    ...
    if (!write_at(...)) return FALSE;          /* :538                   */
  }

  dh_file->flags |= FILE_UPDATED;              /* :547  success only     */
  return TRUE;
}
```

The two outcomes end up the wrong way round. A flush that **succeeds** leaves
the file marked dirty, so the next flush repeats work that is already done —
harmless. A flush that **fails** leaves it marked clean, so the guard at the top
of the function will not fire next time and the header is simply never written.

Three things that would each have caught this are missing on the same path:

1. **The caller is not told.** The function returns `bool`, and six of its seven
   callers discard it — `dh_clear.c:81`, `dh_file.c:453`, `dh_file.c:738`,
   `dh_split.c:240`, `dh_split.c:459` and `dh_write.c:622`. Only
   `dh_close.c:45` casts it to `(void)`, which at least reads as deliberate.
2. **The failure is not logged.** The FDS-open path calls `log_printf` before
   returning, but the `read_at` and `write_at` paths return silently.
3. **The retry is foreclosed**, by the cleared flag described above.

What the header carries is the reason this matters: `record_count` and
`free_chain` are written at `:531`-`:532`. A stale header means the file's
recorded count disagrees with the data it describes, and the free-space chain
on disk points somewhere other than where the in-memory copy believes.

In most cases it recovers by accident. Every write path sets `FILE_UPDATED`
again (`dh_write.c:121`, `:444`, `:700`, `dh_del.c:94`, `:308`), so the next
update to the same file re-flushes the header. The case that does not recover
is `dh_close.c:45`, where there is no next write: the file closes with a stale
header and nothing anywhere records that it happened.

The trigger is a real I/O error, so this is not reachable on a healthy disk.
It is filed because the failure is silent in all three respects at once rather
than because it is likely.

A minimal fix is to restore the flag on the failure paths — or better, to clear
it only after the `write_at` has succeeded — and to log the two silent returns
the way the first one already does.

`gplsrc/dh_file.c:501`, `:507`, `:517`, `:538`, `:547`. Confirmed identical on
upstream `main` at commit `ae0cc5f`, where the function occupies the same lines.

`PROPOSED`

## 30. `get_ak_node()` returns 0 to mean "I could not get a node", and none of its seven callers test it — node 0 is the AK header

`get_ak_node()` in `gplsrc/dh_ak.c` allocates a node in an alternate key
subfile. It returns the node number, and **0 is its way of saying it failed** —
that is not an inference, it is written explicitly on one path:

```c
Private int32_t get_ak_node(DH_FILE *dh_file, int16_t subfile) {
  int32_t new_node_num = 0;
  ...
  if (!dh_read_group(dh_file, subfile, 0, (char *)ak_header, DH_AK_HEADER_SIZE)) {
    goto exit_get_ak_node;                  /* returns the 0 initialiser */
  }

  if (ak_header->free_chain == 0) {
    file_bytes = filelength64(dh_file->sf[subfile].fu);
    new_node_num = (int32_t)((file_bytes - dh_file->ak_header_bytes) / DH_AK_NODE_SIZE + 1);
    chsize64(dh_file->sf[subfile].fu, file_bytes + DH_AK_NODE_SIZE);   /* discarded */
  } else {
    ...
    if (!dh_write_group(dh_file, subfile, 0, (char *)ak_header, DH_AK_HEADER_SIZE)) {
      new_node_num = 0;                     /* explicitly: 0 means failure */
      goto exit_get_ak_node;
    }
  }
  ...
  return new_node_num;
}
```

**All seven call sites use the result immediately, without testing it**:
`dh_ak.c:2216`, `:2237` and `:2365` in `ak_write()`'s node-split paths,
`:3407` and `:3460` in `update_internal_node()`, and `:3831` and `:3865` in
`write_ak_big_rec()`.

What makes that costly rather than merely untidy is where node 0 lives.
`dh_write_group()` maps it to the start of the subfile:

```c
  if (group) {
    if (subfile < AK_BASE_SUBFILE) {
      offset = GroupOffset(dh_file, group);
    } else {
      offset = ((int64)group - 1) * DH_AK_NODE_SIZE + dh_file->ak_header_bytes;
    }
  } else
    offset = 0;
```

Byte 0 of an AK subfile is the AK header — the same block `get_ak_node()` reads
at the top of itself, holding `free_chain` and `itype_ptr`. So on the failure
path the caller writes a terminal, internal or big-record node **over the index
header**. `write_ak_big_rec()` shows the shape most clearly, because it handles
its other two failures and not this one:

```c
  buff = (DH_BIG_NODE *)k_alloc(48, DH_AK_NODE_SIZE);
  if (buff == NULL) { dh_err = DHE_NO_MEM; head = 0; goto exit_write_ak_big_rec; }

  head = get_ak_node(dh_file, subfile);     /* not checked */
  node_num = head;                          /* 0 */
  ...
  if (!dh_write_group(dh_file, subfile, node_num, (char *)buff, DH_AK_NODE_SIZE)) {
    head = 0; goto exit_write_ak_big_rec;   /* this failure IS handled */
  }
```

The `k_alloc` failure and the `dh_write_group` failure are both caught. The one
allocation that is not memory is the one that is not checked. At `:3865` the
same unchecked value is also stored as a forward link,
`buff->next = SetAKFwdLink(dh_file, next_node_num)`, so a chain can be left
pointing at node 0 as well.

The error does reach the caller eventually — `dh_read_group` and
`dh_write_group` set `dh_err`, and `op_akwrite`/`op_akdelete` copy it into
`process.status` — but only after the header has been overwritten. The report
arrives, and the index is already gone.

Two smaller discards sit alongside it and are worth fixing in the same pass,
though both leak space rather than give wrong answers:

- `dh_ak.c:2702`, above — `chsize64()`'s return is dropped, and it is the call
  that actually extends the subfile for the node number just computed. On
  failure a non-zero node number is returned for space that was never made.
  `filelength64()` (`gplsrc/linuxlb.c`) also discards `fstat()`'s return and
  will hand back an uninitialised `st_size` if it fails, which feeds straight
  into that arithmetic.
- `dh_ak.c:3707` in `ak_clear()` — every other step in that function aborts to
  `exit_ak_clear` on failure, but the `chsize64()` that discards the old index
  content is unchecked, and the function still returns `TRUE`. `dh_clear.c:121`
  tests that result and is told the index was cleared.
- `dh_ak.c:3913` in `free_ak_big_rec()` — `free_ak_node()` returns `bool` and
  is discarded in the loop, so the function reports `TRUE` having failed to
  free any of the chain.

The trigger throughout is a real I/O error on the AK subfile, so none of this is
reachable on a healthy disk. It is filed because the first one converts a
transient write error into permanent corruption of the structure every query on
that key depends on, which is a worse outcome than the failure that caused it.

**And testing for 0 at the call sites is not sufficient on its own, because one
of the three failure paths does not return 0.** Found 1 Sep 2026 while making
that fix; the excerpt above elides it behind the `...`, and it is the middle
branch:

```c
  } else {
    new_node_num = GetAKFwdLink(dh_file, ak_header->free_chain);
    if (!dh_read_group(dh_file, subfile, new_node_num,
                       (char *)&ak_node, DH_FREE_NODE_SIZE)) {
      goto exit_get_ak_node;          /* returns new_node_num, which is NOT 0 */
    }
```

`new_node_num` is already set from the forward link when that read is
attempted, so the failure exit returns the head of the free chain as though it
were a freshly allocated node — and `ak_header->free_chain` has not been
advanced, so the file still believes that node is free. The caller writes a
node the allocator will hand out again. It is a different fault from the header
overwrite and is invisible to a caller-side test for 0, so the fix has to make
the failure convention total in the function rather than guard it at the seven
sites.

A minimal fix is to set `new_node_num = 0` on that path so 0 means failure on
all three, then test `get_ak_node()`'s return at all seven sites and abort the
operation on 0, exactly as the neighbouring `k_alloc` and `dh_write_group`
failures already do; and to take the return of the two `chsize64()` calls.

Note that `update_internal_node()` at `:3460` assigns the result straight into
`node_ptr->node_num`, so it needs a temporary — testing after the store would
mean testing a value already committed to the node structure.

`gplsrc/dh_ak.c:2686`, `:2702`, `:2716`, `:2216`, `:2237`, `:2365`, `:3407`,
`:3460`, `:3707`, `:3831`, `:3865`, `:3913`; `gplsrc/dh_file.c:331`;
`gplsrc/linuxlb.c:46`. Confirmed identical on upstream `main` at commit
`ae0cc5f` — `get_ak_node()` at `:2750`, its `chsize64` at `:2766`, the explicit
`new_node_num = 0` at `:2775`, `ak_clear`'s `chsize64` at `:3748`,
`write_ak_big_rec`'s unchecked call at `:3872`, and `dh_file.c:331` at `:331`.

`PROPOSED`

## 31. Deleting a directory-file record inside a transaction cannot fail; the same statement outside a transaction reports a permission error

`op_delete()` in `gplsrc/op_dio3.c` has two paths for a directory file. Inside a
transaction it defers to the cache, and the work is done later by `op_txncmt()`
in `gplsrc/txn.c`. Outside one it does the delete itself.

The two do not behave the same way, and the transactional one is the weaker.

Outside a transaction (`op_dio3.c:401`-`:414`):

```c
        /* 0408 Check that this really is a file, not CON, COMn, LPTn */

        if (!stat(subfilename, &statbuf) && !(statbuf.st_mode & S_IFREG)) {
          process.status = -ER_IID;
          goto exit_op_delete;
        }

        if (remove(subfilename) < 0) /* 0427 */
        {
          process.os_error = errno;
          if (process.os_error != ENOENT) {
            process.status = -ER_PERM;
            log_permissions_error(fvar);
            goto exit_op_delete;
          }
        }
```

Inside one, the whole of the delete at commit is `txn.c:197`:

```c
            } else
              remove(path);
```

The return is discarded. So a delete that fails — a read-only file, an ACL
denial, or a file another process is holding open — is committed as though it
had happened. `clear_parent()` runs on the next line, the cache entry is freed,
`unlock_txn()` releases the locks, the transaction level is left, and the record
is still on disk. The next `READ`, `SELECT` or `LIST` returns a record the
program was told it had deleted. There is no error, no log entry and no
`process.status`.

The `stat`/`S_IFREG` guard is missing too, so the device-name check that the
`0408` comment describes does not apply inside a transaction.

Within `op_txncmt()` itself the inconsistency is one `switch` wide. Three of the
four arms test their operation:

- `TXN_WRITE` / `DYNAMIC_FILE` — `if (!dh_write(...))`, raises 1422 (`:150`)
- `TXN_WRITE` / `DIRECTORY_FILE` — `if (!dir_write(...))`, raises 1422 (`:158`)
- `TXN_DELETE` / `DYNAMIC_FILE` — `if (!dh_delete(...))`, raises 1423 (`:175`)
- `TXN_DELETE` / `DIRECTORY_FILE` — bare `remove()` (`:197`)

Unlike most of the failure paths in this area, this one does not need a disk
error to reach. A read-only record file is enough, and on Windows a file held
open by another process is routine.

A minimal fix is to give the fourth arm what the other three have: test
`remove()`, treat any `errno` other than `ENOENT` as a failure, log it, and
raise 1423 the way the `dh_delete` arm directly above it does. Copying the
`stat`/`S_IFREG` guard from `op_dio3.c` at the same time would close the
device-name gap.

`gplsrc/txn.c:197`, `:150`, `:158`, `:175`, `:201`; `gplsrc/op_dio3.c:380`,
`:401`, `:407`. Confirmed identical on upstream `main` at commit `ae0cc5f` —
the bare `remove(path)` at `txn.c:187`, and the checked non-transactional path
at `op_dio3.c:386`.

`PROPOSED`

## 32. A commit that fails half way cannot be rolled back and never releases its locks

`op_txncmt()` in `gplsrc/txn.c` clears the transaction id before it starts
committing, so that closing a file during the commit does not recurse:

```c
  commit_txn_id = process.txn_id;
  process.txn_id = 0;
```

It then walks the cache, writing and deleting. A failure raises an error and
jumps to the end of the function:

```c
            if (!dh_write(dh_file, txn->id, txn->id_len, txn->str)) {
              k_error(sysmsg(1422));
              goto exit_op_txncmt;
            }
```

`k_error()` does not return here. `gplsrc/k_error.c:31` sets
`fatal = (*message != '!')`, and messages 1422 and 1423 do not begin with `!`,
so `:289` reaches `longjmp(k_exit, K_ABORT)`. The `goto` below each `k_error()`
is unreachable.

Everything after the commit loop is therefore skipped, not just the exit:

```c
  txn_head = NULL;                    /* :215 - cache never cleared      */
  txn_tail = NULL;
  ...
  unlock_txn(commit_txn_id);          /* :233 - locks never released     */
```

Three things outlive the abort:

1. **The commit is partly applied.** Records handled before the failure are
   written; the rest are not. Nothing records which is which.
2. **Every record lock taken during the transaction is still held.** The only
   two calls to `unlock_txn()` are the one above and the one in `rollback()`,
   and neither is reached. The locks stay until the process ends.
3. **The cache is orphaned** and the transaction level stays counted.

Nothing can undo any of it, because the recovery paths test the id that was
zeroed at the top. `txn_abort()` (`:288`) and `op_txnrbk()` (`:275`) both guard
on `process.txn_id`, so the abort, logout and terminate handlers at
`gplsrc/kernel.c:399`, `:410` and `:423` roll nothing back and report nothing.

The trigger is a genuine write failure at commit time, so this is not reachable
on a healthy disk — with the exception of the directory-file delete described in
entry 31 above, which fails silently and so does not reach this path at all.

The lock release is the separable half and does not need a design decision: the
`unlock_txn()` call could be moved above the failure paths, or repeated on them.
What to do about the records already written is a larger question, since a
partially applied commit cannot simply be forgotten.

Both halves have since been fixed in the Windows port, and the shapes may be
useful even though the code will not transplant directly.

The lock release went into `txn_abort()` rather than to the `k_error()` call
sites. `k_error()` longjmps, so every `goto exit_op_txncmt` after one is dead
code and no label below them can run — the fix has to be on the far side of the
jump, and `txn_abort()` is where the jump lands. Putting it there also covers
any error path added to that loop later, and covers logout and terminate, which
reach the same function. `op_txncmt()` saves `process.txn_id` into a file-scope
`commit_txn_id` before zeroing it, and clears that on the success path so a
later unrelated abort cannot unlock an id the allocator has since reissued.

The records already written are now restored to what they held before. The
before image is captured at commit time, immediately before each action is
applied — not when the write is cached, because only at that moment is the
image certainly the one about to be overwritten, and `TXN_CACHE` holds only the
new data. The images go on a stack, so walking it is already reverse order, and
it is replayed from `txn_abort()` before the locks are released: the records
being rewritten are exactly the ones the transaction still holds locks on, and
they are ours to write only until `unlock_txn()` gives them up. An entry is
either the prior record, or a marker that there was none — in which case the
undo deletes what the commit was creating — or a marker that the image could
not be read, which is logged by file and id rather than passed over. The undo
never raises: the disk is already misbehaving by then, and a `k_error()` there
would longjmp out of the abort handler itself.

Two things about that were not obvious until it was built. The capture reads a
record, so it sets `process.status`, `process.os_error` and `dh_err` on its way
past, and the caller is about to report its own failure through exactly those —
all three have to be saved and restored or the commit's error ends up described
by the capture's last read. And the record the commit *failed* on has to be
captured and restored like any other, because a write that fails part way
leaves it in a state nothing can describe; "the action failed" is not the same
claim as "the record is untouched".

One piece of groundwork was needed first, and upstream would need it too: the
directory-file code has a write API and no read API. `dir_write()` has always
been callable, but the only reader is `read_record()`, which takes its file
variable, id and target off the VM's e-stack and can only be reached by
executing a READ opcode — and a commit cannot execute one. The port added
`dir_read()`, shaped like `dir_write()`, and lifted the CRLF-and-LF to
field-mark conversion into one function shared by both readers rather than
copying it. That sharing is not tidiness: a capture that reversed the mark
mapping even slightly differently from an ordinary read would restore a record
that is not the one it captured, silently, on the failure path.

`gplsrc/txn.c:136`, `:151`, `:159`, `:177`, `:215`, `:233`, `:275`, `:288`,
`:607`; `gplsrc/k_error.c:31`, `:289`; `gplsrc/kernel.c:399`, `:410`, `:423`.
Confirmed present on upstream `main` at commit `ae0cc5f`, where `op_txncmt()`
has the same `process.txn_id = 0`, the same three `k_error()` and `goto` pairs,
and `unlock_txn()` after the loop.

`PROPOSED`

## 33. `SetFileSize()` cannot fail, and two sequential-file opcodes report success on a truncate that did not happen

`chsize64()` is called seven times in `gplsrc`. Six discard the return. The
seventh, `sdfix.c:2493`, tests it:

```c
    if (chsize64(fu[PRIMARY_SUBFILE], n)) {
```

so the return is meaningful and is used elsewhere in the same tree.

The clearest of the six is `dh_file.c:831`, which is the whole function:

```c
bool SetFileSize(OSFILE fu, int64 bytes) {
  chsize64(fu, bytes);
  return TRUE;
}
```

It is declared to return a status and always returns success. A caller cannot
check it even if it wants to, because there is nothing to check.

Its two callers are in `dh_clear.c`, which is `CLEAR.FILE`:

```c
  if (Seek(dh_file->sf[PRIMARY_SUBFILE].fu, ...) < 0) {   /* :89  checked  */
    dh_err = DHE_SEEK_ERROR;
    goto exit_dh_clear;
  }

  for (group = 1; group <= new_modulus; group++) {
    if (Write(dh_file->sf[PRIMARY_SUBFILE].fu, ...) < 0) { /* :97  checked */
      dh_err = DHE_INIT_DATA_ERROR;
      goto exit_dh_clear;
    }
  }

  SetFileSize(dh_file->sf[PRIMARY_SUBFILE].fu, ...);       /* :107 cannot be */

  FDS_open(dh_file, OVERFLOW_SUBFILE);                     /* :113 discarded */
  SetFileSize(dh_file->sf[OVERFLOW_SUBFILE].fu, ...);      /* :114 cannot be */

  for (akno = 0; akno < MAX_INDICES; akno++) {
    if ((ak_map >> akno) & 1) {
      if (!ak_clear(dh_file, AK_BASE_SUBFILE + akno))      /* :121 checked  */
        goto exit_dh_clear;
    }
  }
```

The seek, the write and the index clear are all tested; the two truncates are
the only steps that are not, and they are the only ones that could not be. In
this function the consequence is mild — the primary is rewritten with empty
groups first, and that write is checked, so a failed truncate only fails to
reclaim excess space. `FDS_open()`'s discarded return is worth taking at the
same time, since an invalid handle otherwise reaches the second call.

The two sequential-file sites matter more, because there the truncate is the
entire meaning of the statement.

`op_seqio.c:1542`, the body of `op_weofseq()`:

```c
  Seek(fu, sq_file->posn, SEEK_SET);
  chsize64(fu, sq_file->posn);
  sq_file->base = -1;

exit_op_weofseq:
  InitDescr(e_stack, INTEGER);
  (e_stack++)->data.value = process.status;

  if ((process.status < 0) && !(op_flags & P_ON_ERROR)) {
    k_error(sysmsg(1420), -process.status);
  }
```

`WEOFSEQ` is nothing but that truncate. `process.status` is never set from it,
so the status pushed on the stack is 0 and the `k_error()` two lines later
cannot fire. The opcode aborts loudly on every failure it detects, and this is
the one it does not detect: the file keeps everything past the intended end and
the program is told the truncate succeeded.

`op_seqio.c:803`, in `openseq()` under the overwrite flag, has the same shape,
so `OPENSEQ ... OVERWRITE` can leave the previous contents in place. Later
writes then overwrite only the front of the file and the old tail survives past
the new end.

A minimal fix is to return the result from `SetFileSize()`:

```c
bool SetFileSize(OSFILE fu, int64 bytes) {
  return chsize64(fu, bytes) == 0;
}
```

and, in the two sequential opcodes, to set `process.status` when the truncate
fails so that the `k_error()` each already carries does its job.

`gplsrc/dh_file.c:831`, `:832`; `gplsrc/op_seqio.c:803`, `:1542`;
`gplsrc/dh_clear.c:89`, `:97`, `:107`, `:113`, `:114`, `:121`; the checked
control at `gplsrc/sdfix.c:2493`. Confirmed identical on upstream `main` at
commit `ae0cc5f` — `SetFileSize()` the same four lines at `dh_file.c:831`, and
the two `op_seqio.c` calls at `:724` and `:1392`. The two further discards in
`dh_ak.c` are covered by entry 30 above.

`PROPOSED`

## 34. `DELETE.FILE` orphans a relocated alternate-key index, and discards the delete that would have removed it

`DELETEF` removes the DATA and DICT portions of a file, and tests each one:

```c
            if ospath(data.path, OS$DELETE) then
               if akpath # '' then dummy = ospath(akpath, OS$DELETE)

               display sysmsg(6136, data.path) ;* DATA portion 'xx' deleted
               ...
            end else
               display sysmsg(6138, data.path) ;* Error deleting DATA portion 'xx'
               @system.return.code = -status()
            end
```

The same shape appears again for the dictionary at `DELETEF:350`, with 6141 and
6142.

Both portion deletes are tested and reported. The index delete on the line
between them is not: its result goes into `dummy` and nothing looks at it.
`akpath` comes from `fileinfo(data.f, FL$AKPATH)` a few lines earlier, so this
only applies to a file whose indices were relocated — but when it does apply,
the whole index directory is left on disk with nothing said about it.

The messages are not wrong. 6136 and 6141 name the DATA and DICT portions, and
those really were deleted. Nothing claims anything about the index, so this is
an orphan on disk rather than a false report.

It is worth fixing because this is the verb whose whole job is to remove a file,
and it is the only step in it that neither tests nor reports. The rest is
careful: it refuses when either portion is open (6198, 6199), tests both
deletes, and sets `@system.return.code` from `status()` on failure.

Taking the result and reporting a failure the way the two portions beside it
already do would be enough.

`sdsys/gpl.bp/DELETEF:275`, `:350`, and the tested neighbours at `:277` and
`:353`. Confirmed identical on upstream `main` at commit `ae0cc5f`, at
`DELETEF:245` and `:317`.

Separately, and much smaller: messages **6055** *"User %1 created with no
password"*, **6056** *"User %1 created"*, **6057** *"User is not in register"*
and **6058** *"User %1 deleted"* have no caller anywhere in `gpl.bp` or
`gplsrc` in either tree, so they appear to be left over from a verb that no
longer exists.

`PROPOSED`

## 35. A directory-file record whose filename ends in `%` makes `readnext` walk past the end of a stack buffer

`dir_select()` decodes a directory file's escaped filenames back into record
ids. Its loop is at `sd64/gplsrc/op_dio4.c:1178-1187` on upstream `main` at
commit `ae0cc5f`, and at `:1140-1147` in the Windows port, where the two copies
are byte for byte the same. The buffer it decodes into is `name`, declared at
`op_dio4.c:1118`, and the two substitution tables are at `sd64/gplsrc/sd.h:113-114`
— `df_restricted_chars` `*,=><%/+:;?\"` against `df_substitute_chars`
`ACEGLPSVXYZBQ`, position for position. ***`%` IS ITSELF ON THE RESTRICTED
LIST***, encoding to `%P`, which is what makes the trailing case below
reachable at all:

```c
while ((c = *(p++)) != '\0') {
  if (c == '%') {
    r = strchr(df_substitute_chars, *(p++));
    if (r != NULL) {
      *(q++) = df_restricted_chars[r - df_substitute_chars];
    }
  } else {
    *(q++) = c;
  }
}
```

There are two problems, and the second is a memory-safety one.

**An unknown escape silently discards two characters.** When the letter after
`%` is not in `df_substitute_chars`, `r` is NULL and nothing is written — but
`p` has already stepped over that letter. So a file named `draft%1` decodes to
the id `draft`. Two different files can therefore produce the same id, and the
id `readnext` hands back does not open. `map_t1_id()` never emits such a name
itself, but a directory file is exactly where files created outside SD arrive.

**A trailing `%` runs off the end of the buffer.** `*(p++)` consumes the
string's own terminator, and `strchr(df_substitute_chars, '\0')` returns a
pointer to that table's terminating NUL rather than NULL — so the `r != NULL`
guard passes. `r - df_substitute_chars` is then 13, and `df_restricted_chars[13]`
is that array's own NUL, so the byte written is harmless. The pointer is not:
`p` now points past the end of `name`, and the `while` keeps consuming adjacent
stack memory while `q` writes it back into `name` until a zero byte happens to
turn up. `name` is `char name[MAX_PATHNAME_LEN + 1]` (`op_dio4.c:1118`), a
fixed stack buffer, so this can overflow it rather than merely over-read.

A file called `draft%` in any directory file reproduces it; `%` is a legal
filename character on both Linux and Windows, and no privilege is needed
because a user's own `bp` is a directory file.

Testing the character before consuming it fixes both, and makes the decode
total rather than partial:

```c
if (c == '%') {
  if (p[0] && (r = strchr(df_substitute_chars, p[0])) != NULL) {
    *(q++) = df_restricted_chars[r - df_substitute_chars];
    p++;
  } else {
    *(q++) = c;          /* unknown escape: keep it literal */
  }
}
```

The `if (strlen(name) > 0)` guard just below the loop contains the empty-name
case only; neither fault above produces an empty name in general.

Found by reading, not by running: the Windows port reached this code while
investigating a suspected VOC mismatch that turned out to be the encoding
working correctly.

The suggested fix above is not only proposed — it is the one the Windows port
took, and it has been built, installed and driven since this entry was written.
Four fixtures in a user's `BP`: an ordinary name; `%E`, which is the legitimate
encoding of the id `=` and must still decode; `draft%1`; and `draft%`. `SELECT`
reports all four, `%E` still decodes to `=`, and `draft%1` comes back whole
instead of as `draft`. Nothing there exercises sdb64 itself, so for that side
this remains a reading of identical code — but the patch is known to compile
and to behave as described.

`SENT` — by email to the upstream developer, 2 Sep 2026.

## 36. A directory-file record written inside a transaction goes to the unmapped filename, and one deleted inside a transaction is not deleted

Directory files store each record as a file whose name is the record id put
through `map_t1_id()` (`sd64/gplsrc/op_dio3.c:1296` upstream, `:1346` in the
Windows port). The substitution tables are at `sd64/gplsrc/sd.h:113-114` —
`df_restricted_chars` `*,=><%/+:;?\"` against `df_substitute_chars`
`ACEGLPSVXYZBQ`, position for position — plus a leading `.` to `%D` and a
leading `~` to `%T`. So the id `=` is the file `%E` and the id `,` is the file
`%C`. `map_dir_ids` defaults to `TRUE` (`sd64/gplsrc/kernel.h:80`), and the
encoding is in ordinary use: a stock `SDSYS` VOC contains `%E`, `%G` and `%L`.

`dir_write()` takes that mapped id and uses it verbatim as the filename — the
parameter is even spelled `mapped_id` (`op_dio3.c:1340` upstream). The
non-transactional write passes it correctly:

```c
      if (!map_t1_id(id, id_len, mapped_id)) {     /* op_dio3.c:824 */
        ...
      }

      if (txn_id != 0) {
        if (!txn_write(fvar, id, id_len, str))     /* :832  - the RAW id */
          goto exit_op_write;
      } else {
        if (!dir_write(fvar, mapped_id, str))      /* :835  - the mapped one */
          goto exit_op_write;
      }
```

The mapping is computed and then discarded whenever a transaction is open:
`txn_write()` is handed `id`, not `mapped_id`. `op_delete()` has the identical
split at `:353` and `:359`. The transaction cache is right to hold the raw id —
`txn_read()`, `txn_write()`, `txn_delete()` and `clear_parent()` all match it
against the id the BASIC statement used — but nothing maps it later, and
`op_txncmt()` then applies the cache straight to the disk:

```c
          case DIRECTORY_FILE:                     /* txn.c:148 */
            if (!dir_write(fvar, txn->id, txn->str)) {
```

and, for the delete arm:

```c
            if (snprintf(path, MAX_PATHNAME_LEN + 1, "%s%c%s", fptr->pathname,
                         DS, txn->id) >= (MAX_PATHNAME_LEN + 1)) {   /* :183 */
```

Both consequences are silent, and neither needs anything to go wrong: the
commits succeed.

**A write inside a transaction lands where the matching read cannot find it.**
`WRITE rec ON f, ','` inside a transaction creates the file `,`. A later
`READ ... FROM f, ','` maps the id as it always has, looks for `%C`, and
returns not-found. The record is on disk under a name nothing will ask for.

**A delete inside a transaction removes nothing and reports success.** The path
is built from the raw id, so it names a file that never existed. `remove()`
fails with `ENOENT`, which this code deliberately tolerates — the record being
already gone is what was asked for — so the commit completes normally while the
real record is still there and still readable.

Measured in the Windows port on 4 Sep 2026, on a build with no other change, by
one BASIC program whose commits all succeeded: `=` written outside a
transaction landed as `%E` and read back; `,` written inside one landed as `,`
and read back as not-found; `;` written outside and then deleted inside one
left `%Y` on disk with its contents intact. The directory listing and the
program's own reads were taken as two independent instruments and agreed.
The control matters — without the `%E` row, a build with `map_dir_ids` off
would make the raw and mapped names the same string and the comparison would
pass for the wrong reason.

The fix is to map at the point of contact with the disk, which is where the
non-transactional path already does it: call `map_t1_id(txn->id, txn->id_len,
mapped_id)` at the top of each of `op_txncmt()`'s two `DIRECTORY_FILE` arms and
use its output for `dir_write()` and for the `snprintf()`. Leave the cache
holding the raw id. The failure return cannot fire there — both entry points
validate before anything is cached — but it should still raise the arm's own
error (1422 for write, 1423 for delete) rather than skip silently. In the
delete arm the mapping is worth doing before the statistics counters, which are
incremented first today: an id that could not be mapped would otherwise count a
delete that never happened.

Reported here from reading upstream's source at `ae0cc5f`, where all five
sites are present and match the Windows port's pre-fix state line for line.
The fix above is the one the port took; it compiles, and the behaviour
described was reproduced in that tree, not in `sdb64`.

## 37. `INT.UPDATE.ACCOUNT`'s banner comment names internal verb 30, and the dispatch table two hundred lines above says 15

This is a comment, not code, so nothing misbehaves. It is here because the
comment is the only place a reader can look up what an internal verb number
means, and this one sends them to the wrong routine.

In `sd64/sdsys/GPL.BP/CPROC` the dispatch table reads

```
                     int.update.account,         ;* 15  UPDATE.ACCOUNT
```

and the routine's own banner, some 1,440 lines further down, reads

```
* INT.UPDATE.ACCOUNT    -  UPDATE.ACCOUNT (Internal verb 30)
```

**30 belongs to `INT.STOP`, which is the next banner in the file and where the
number is correct.** So the two banners agree with each other and only one of
them agrees with the table, which is the shape that makes a copied heading hard
to notice.

It matters because field 3 of a `V`/`IN` VOC record *is* that number — `OFF` is
`V / IN / 1`, `WHO` is `V / IN / 16` — so somebody holding a VOC record and
asking "which routine runs this?" reads the banners, not the table. Anyone
tracing `UPDATE.ACCOUNT` that way lands on `INT.STOP`.

The fix is one character: make the banner say 15.

Found while adding an optional keyword to that routine in the Windows port on
4 Sep 2026, where the same wrong number is present and has now been corrected.
Read from upstream's source; there is no behaviour to reproduce.
