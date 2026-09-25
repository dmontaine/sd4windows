# Note from SD Core Solo, 25 Sep 2026

Left by the SD Core Solo session at the owner's request, for whoever works in this
repository next. It is information, not a task list: nothing here was changed in
this tree, and nothing was committed. Solo (`C:\Users\Don\SDCoreProject\SDCore4WindowsSolo`)
started from this repository at `36109e8e`, so it shares this code.

## Three code defects, all present here (checked by reading this tree at `36109e8e`)

**1. `RUN` fails for any runfile path over 128 characters.**
`gplsrc/op_jumps.c`, `op_run()`: `char runfile_name[MAX_PROGRAM_NAME_LEN + 1]` and
`k_get_c_string(descr, runfile_name, MAX_PROGRAM_NAME_LEN)`. CPROC builds the path as
`fileinfo(run.file, fl$path) : @ds : run.record.name`, so any `RUN` from a directory
deeper than about 128 characters prints `Invalid runfile pathname` however valid the
file is. **Measured in Solo:** from a folder about 120 characters deep, `RUN gpl.bp
write_install_dicts` failed this way. Here the install path
(`C:\ProgramData\SD\sdsys\gpl.bp.out\...`, about 50 characters) keeps a normal
install clear of it.

**2. The limit in (1) is guarding an unbounded copy.**
`gplsrc/object.c:274`: `strcpy(obj->code.ext_hdr.prog.program_name, name);` into
`program_name[MAX_PROGRAM_NAME_LEN+1]` (`header.h:75`, part of the object format).
Do not simply enlarge (1)'s buffer. Solo's fix: `op_run()` takes up to
`MAX_PATHNAME_LEN`, and `load_object()` copies at most `MAX_PROGRAM_NAME_LEN`
characters, keeping the TAIL of an over-long path. A truncated name can never equal
the full path on the next call, so the object cache cannot return the wrong program;
the file is just reloaded.

**3. `k_error()` can write past its buffer.**
`gplsrc/k_error.c:258`, `:263`, `:266`: three plain `sprintf(s + n, ...)` append
"at line N of <program>" after the `vsnprintf` at `:244` may already have filled most
of the 241-byte `s`. A long message plus a program name of up to 128 characters
overruns it. Fix: `snprintf(s + n, sizeof(s) - n, ...)` on all three.

## One build gap, present here

**4. The bootstrap does not check that the dictionaries were written.**
`gplbld/bootstrap.py:316` runs `-internal RUN gpl.bp write_install_dicts NO.PAGE`
and ignores the output. `sd` exits 0 even when the program never ran, so in Solo a
tree was staged, "successfully", with no dictionaries. Solo's fix: require the
program's own last line, `COMPLETE`, and refuse on `Invalid runfile`,
`ERROR OPENING`, `PROCESS ABORTED` or `READLIST EMPTY`.

## Where the fixes are

In `SDCore4WindowsSolo`, task **SOLO 12** in its `PROJECT_STATUS.md` (built and
measured on 25 Sep 2026, commit pending). Upstream write-ups for 1-3:
`SDCore4WindowsSolo\UPSTREAM_FIXES.md` entries **40** and **41** — the same defects
are in `sdb64` at `ae0cc5f`.

Not relevant here: Solo also changed the semaphore ACL (`win32sem.c`) and removed
the elevation requirements, but those are deliberate multi-user design in this tree,
not defects.
