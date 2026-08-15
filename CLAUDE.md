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

## You must maintain these files

This is a standing instruction from the repository owner, not a nicety.

- **Update PROJECT_STATUS.md in the same commit as the work it describes**, not
  afterwards. If a commit changes what builds, what runs, what is decided, or
  what is next, it changes PROJECT_STATUS.md too.
- **Never move anything into "Verified" without observing it yourself in that
  session.** Compiling is not running. Running once is not tested. If a
  previous session claimed something and you did not confirm it, it stays
  unverified.
- **Append to HISTORY.md** when work completes, when PROJECT_STATUS.md needs to
  shed settled material, and — especially — when an earlier claim turns out to
  be wrong. Corrections get their own entry. HISTORY.md is append-only; never
  delete or rewrite an entry.
- **Keep PROJECT_STATUS.md readable**, which is three budgets rather than one
  (§0 rule 5): **header ≤ 200 lines**, **§7 Next steps ≤ 300**, whole file
  ≤ 3,500. The first two are what a session reads front to back before doing
  anything, so they are the ones that matter; the rest is read by searching.
  **§6 Traps is meant to grow** — never cut a trap to meet a number.
  **The file self-cleans when a §7 step closes**: in that same commit, compress
  its §4 tables to their conclusions and move its §5 weighing to HISTORY.md.
  Do that and the rollover never becomes an event. Never a reason to omit a
  finding. Measure with `.Count`, not `Measure-Object -Line`, which ignores
  blank lines and undercounts by ~15%.
- **Record anything a user would notice in `sdb_ai/sd64/sdsys/changelog`**, in
  the same commit as the work. That is the product changelog and it ships with
  the system; the two files above are the state of the work and the reasoning
  behind it, and neither substitutes for it.

The full rules are in §0 of PROJECT_STATUS.md and at the top of HISTORY.md.
Follow those; this file only points at them.

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

## Conventions

- Match the surrounding code. It is a 2007 Ladybridge codebase with its own
  idioms — `Public`/`Private` macros, `START-HISTORY` blocks, banner comments.
  Add a dated line to a file's `START-HISTORY` block when changing it.
- Nothing binary is tracked — see the constraint above. `bin/` is build output
  and is ignored apart from its README.
- Explain *why* in commit messages, not just what. The reasoning is the part
  that does not survive in the diff.
