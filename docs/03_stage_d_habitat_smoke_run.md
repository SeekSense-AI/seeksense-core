# Stage D — Habitat smoke run (evidence artefacts)

This stage is optional and is treated as an **evidence collection run**, not a demo.

## Goal
Produce artefacts that demonstrate the pipeline can be wired into a simulator run:
- per-episode logs
- saved top-down maps / screenshots
- a small metrics JSON
- pinned environment versions

## Artefact checklist
Save outputs to:
`results/habitat_runs/<YYYYMMDD_run01>/`

Include:
- env_versions.txt (python, pytorch, habitat-lab, cuda)
- command.txt (exact command executed)
- episode_0001.log
- episode_0001_maps/ (pngs)
- metrics.json

## Notes
Keep this repo clean-room. Do not copy third-party source into `src/`.
Link external repos/datasets in documentation and record commands + outputs.
