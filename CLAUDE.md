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
- **Roll over** when PROJECT_STATUS.md exceeds roughly 2000 lines: move settled
  material into HISTORY.md and leave only what is needed to act today. The
  limit exists to stop the file sprawling to the point where nobody reads it —
  it is not a target to sit near, and never a reason to omit a finding.

The full rules are in §0 of PROJECT_STATUS.md and at the top of HISTORY.md.
Follow those; this file only points at them.

## Project constraints

- **Windows only.** Linux development lives in a separate repository. Do not
  add `#ifdef` branches to keep Linux building — replace Linux code outright.
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
- Linked binaries in `bin/` are tracked, because the install scripts deploy
  them from the repository. Build intermediates are not.
- Explain *why* in commit messages, not just what. The reasoning is the part
  that does not survive in the diff.
