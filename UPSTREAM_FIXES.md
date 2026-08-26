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

`PROPOSED` — written up, not sent. `SENT` — reported upstream, with where.
`ACCEPTED` / `DECLINED` — upstream has ruled. Keep declined entries, with the
reason.

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

**What this port did with it, for whatever it is worth to upstream.** `MICRO`
was removed here on 17 Aug 2026 on a containment argument — an external editor
is a way out of SD — and brought back on 26 Aug 2026 as `EDIT`, rewritten with
all three fixed and gated on the account tier rather than on the `OS.USERS`
shell list. The rewrite is `sdsys/gpl.bp/EDIT` and its header records what
changed and why, line by line, so the three fixes can be lifted without taking
the Windows-specific parts.

**Not reproduced against upstream, per this file's standing caveat.** Fault 1
was reasoned from the source and from the absence of any `micro` check;
faults 2 and 3 are structural and readable in the same file.
