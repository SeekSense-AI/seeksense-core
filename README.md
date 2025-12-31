# SeekSense Core — VLFM Reproduction Track (Stage A→D)

This repository is a **reproducible engineering track** to build the core components described in the VLFM pipeline:
**occupancy + frontier mapping → frontier scoring interface → (optional) Habitat smoke-run outputs**.

**Important note (credit / attribution):**
- Research inspiration: *VLFM (Vision-Language Frontier Maps)*, arXiv:2312.03275.
- This repo implements a **clean-room re-implementation** of the *mapping + frontier extraction + scoring interfaces* needed to reproduce the method.
- Where external code is used (e.g., Habitat baselines / official VLFM repo), we link and document it in `docs/` and do not copy proprietary code.

## What’s implemented right now (Stage A–C)
- ✅ **Occupancy grid + frontier extraction** (unit-tested)
- ✅ **Frontier clustering + centroid waypoints**
- ✅ **Value-map + confidence-map interfaces** (model-agnostic; BLIP-2 integration later)
- ✅ **Frontier ranking logic** (uses value map around each frontier cluster)
- ✅ **Synthetic example generator** that outputs `results/frontier_map_example.png`

## Repository structure
```
.
├─ docs/
│  ├─ 01_paper_breakdown.md
│  ├─ 02_scope.md
│  └─ 03_stage_d_habitat_smoke_run.md
├─ src/vlfm_repro/
│  ├─ mapping/occupancy_grid.py
│  ├─ frontier/frontier_extractor.py
│  ├─ vlm/value_map.py
│  └─ nav/frontier_ranker.py
├─ scripts/
│  └─ generate_synthetic_frontier_example.py
├─ tests/
│  ├─ test_frontier_extraction.py
│  └─ test_frontier_ranking.py
├─ results/              # generated artefacts (png/json logs)
├─ REPRODUCIBILITY.md
├─ pyproject.toml
└─ requirements.txt
```

## Quickstart
### 1) Install
```bash
python -m venv .venv
source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
```

### 2) Run tests
```bash
pytest -q
```

### 3) Generate a real output artefact (no simulator needed)
```bash
python scripts/generate_synthetic_frontier_example.py
```
This will create:
- `results/frontier_map_example.png`
- `results/frontier_waypoints.json`

## Stage D (optional): Habitat smoke run
Stage D is intentionally separated because Habitat installation is heavy and hardware-dependent.

See:
- `docs/03_stage_d_habitat_smoke_run.md`
- Add your run artefacts under `results/habitat_runs/` (logs + maps + metrics)

## License
MIT (see `LICENSE`).
