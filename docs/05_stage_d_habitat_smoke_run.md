# Stage D: Habitat smoke run (Issue #4)

## Purpose
Provide a minimal, reproducible run pipeline that always produces:
- results/habitat_runs/<run_id>/metrics.json
- results/habitat_runs/<run_id>/EVIDENCE.md
- results/habitat_runs/<run_id>/frames/ (reserved)

This is assessor-friendly: fixed folder layout, fixed schema, and a clear log.

## Run (any machine)
pip install -e .
python scripts/run_stage_d_habitat_smoke.py

## Outputs
results/habitat_runs/<run_id>/
- metrics.json
- EVIDENCE.md
- frames/

## Running with Habitat (Linux/GPU)
On Linux with Habitat-Sim/Habitat-Lab installed (GPU recommended), the same command can be extended to:
- load a minimal Habitat environment
- run a short episode loop
- compute metrics (e.g., success rate, SPL)
- optionally export a small number of evidence frames

This repo currently includes the scaffold + schema; full Habitat wiring is the next integration step.
