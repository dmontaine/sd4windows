# UPSTREAM FIXES

Defects found while porting SD to Windows that **also affect `sdb64`**, the
upstream Linux project at <https://codeberg.org/stringdatabase/sdb64>.

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

## 2. `SV_EMSG_PAIR` and `SV_ECONTXT` are transposed between the two projects

**Status:** NEEDS A DECISION FROM THE OWNER BEFORE IT IS SENT, 15 Aug 2026
**Affects:** `sd64/gplsrc/sdclient.h`, `sd64/sdsys/SYSCOM/sdclilib.h` on `dev`,
against `github.com/dmontaine/winsdclilib`
**Severity:** wrong-value, not crash. Only bites where the two projects meet —
which is the case this whole client exists for, a Windows client against an SD
server.

The same two names carry **opposite values** in the two projects:

| | `SV_EMSG_PAIR` | `SV_ECONTXT` |
|---|---|---|
| `sdb64` `dev` (commit `d0647b9`, 19 Jul 2026) | 6 | 7 |
| `winsdclilib`, vendored here from `b6624565` | 7 | 6 |

So a caller compiled against one header, talking to a library built from the
other, reads each state as the other one.

**WHO IS RIGHT IS NOT DETERMINED, AND SHOULD NOT BE GUESSED.** This file has a
round-trip history (PROJECT_STATUS.md §5.3): `sdb64`'s own C developer started
a partial Windows library, the repository owner had AI complete it into
`winsdclilib`, that was vendored into the Windows port, and their developer then
forked `winsdclilib` back into `sdb64`'s `dev`. **Code has flowed both ways, so
neither project is simply "upstream" for these two constants.**

Dates do not settle it either: `sdb64`'s commit is 19 Jul 2026 and the snapshot
vendored here is 5 Aug 2026, but that is only when the snapshot was cut and says
nothing about when the constants were written in `winsdclilib`.

**Three candidate origins, and all are live:** the developer's original partial
Visual Studio library; the AI completion that produced `winsdclilib`, which
could well have assigned the numbers itself; or their fork, transposing on the
way back. **`winsdclilib`'s own history is what settles it, and it is not in
this repository.**

**What this project did in the meantime: nothing.** The vendored copy keeps
`winsdclilib`'s values because it is a vendored copy and must stay faithful to
its source, and `sdsys/SYSCOM/sdclilib.h` deliberately defines **neither**, so
that no BASIC code commits to a numbering that may have to change. A session
here did renumber to match upstream and then reverted it on discovering the
provenance — do not redo that without settling the question first.

**To settle it**, in order — the first answer wins:

1. **Did the developer's original partial Visual Studio library define them?**
   If so those values are the origin and both projects should match them.
2. **Otherwise, when did they first appear in `github.com/dmontaine/winsdclilib`?**
   Before 19 Jul 2026 means `sdb64` transposed them on the fork and should
   change. After, means `sdb64`'s numbering came first, this project should
   adopt it, and `sdsys/SYSCOM/sdclilib.h` should gain both.
3. **If it was the AI completion that assigned them**, nobody chose either
   numbering and the tidiest answer wins — take `sdb64`'s, since it is the
   published one.

Whichever way it goes, the fix is to make the two agree and say so in both
projects' history, because the names are identical and the values are not —
which is the worst kind of disagreement to leave in place.

