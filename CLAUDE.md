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

## You must maintain these files, cheaply

Standing instruction from the repository owner, 14 Aug 2026: **the ratio of
time spent on the project to time spent documenting it was too high.**
PROJECT_STATUS.md and HISTORY.md are **written for the next AI session, not for
him** — he does not read them. So:

- **Terse and factual.** `file:line` over description. No narrative, no
  emphasis for effect, no restating a finding in several sections. One fact,
  one place, with pointers.
- **Documentation is a small fraction of a session.** If it approaches half,
  stop and cut. Do not print line counts in the files or re-measure to keep
  them true.
- **Update PROJECT_STATUS.md in the same commit as the work**, and never move
  anything into "Verified" without observing it yourself that session.
  Compiling is not running.
- **Append to HISTORY.md** when work completes or an earlier claim proves
  wrong. Append-only. Keep entries short.
- **`sdb_ai/sd64/sdsys/changelog` is the exception**: it ships to users, stays
  plain English, and gets anything a user would notice, in the same commit.

Full rules in §0 of PROJECT_STATUS.md. Follow those; this file only points.

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
