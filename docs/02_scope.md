# Scope & milestones (Stage A → D)

## Stage A — Repo + reproducibility pack
- README + reproducibility
- clean module layout
- test harness

## Stage B — Frontier mapping module (core first step)
- Occupancy grid representation
- Frontier extraction (4-connected or 8-connected configurable)
- Frontier clustering + waypoint extraction
- Unit tests + synthetic example output

## Stage C — Value-map interface + frontier ranking
- Value-map / confidence-map update interface (model-agnostic)
- Frontier scoring using the value map (mean / max near frontier)
- Unit tests

## Stage D — Habitat smoke run (optional)
Goal: produce evidence artefacts (not a demo video)
- Install Habitat & datasets (ObjectNav)
- Run 1–5 short episodes (smoke)
- Save:
  - maps / screenshots
  - per-episode logs
  - a small `metrics.json` summary
  - environment versions file

Suggested folder:
- `results/habitat_runs/<YYYYMMDD_run01>/`
