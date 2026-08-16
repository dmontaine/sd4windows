# UPSTREAM FIXES

Defects found while porting SD to Windows that **also affect `sdb64`**, the
upstream Linux project at <https://codeberg.org/stringdatabase/sdb64>.

**Fixes owed to `winsdclilib` and `linuxsdclilib` do NOT belong here** — those
two are ours to maintain and are fixed directly (PROJECT_STATUS.md §2, the
sibling repositories). This file is only for what `sdb64` itself needs. Entry
#2 is a closed example of a bug that looked like upstream's and was not.

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
