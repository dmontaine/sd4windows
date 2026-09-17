# muse-audit-1

Date: 2026-09-17
Workspace: C:\Users\Don\SDCoreProject\sd4windows
Target copy: <Documents>\muse-audit-1.md

## Result: partial / inconclusive

Workflow `generated.model-chosen` completed with `complete:false`.

No scoped evidence was carried — all 5 scopes returned empty evidence:
- primary-0 structure
- primary-1 impl-risk
- primary-2 tests
- primary-3 docs-status
- primary-4 security

## Claims noted (ungrounded, discovery pointers only)

- Repo is sd4windows port tree (docs/, sdb_ai/sd64/, PROJECT_STATUS.md, README.md)
- Counts cited without file lists: 52 verify-*, 21 test-units, 146 C files / 225 verbs
- Only bodies carried: install-service.ps1, probe-relaydrop.ps1, partial cred_verify / sd_scram / op_sh / elevate / login / cproc
- Line refs cited without bodies carried

## Unresolved (preserved)

- primary-0..4: missing complete evidence result
- full bodies for truncated remainders of prior results 1,2,4,5
- carried file lists / bodies backing counts + runner mapping
- live re-run of check-stale-leads.py and test-fixlist-units.ps1 (sandbox blocked in workflow)

## Next

Re-run narrow: one scope at a time, or inline sampled audit.
