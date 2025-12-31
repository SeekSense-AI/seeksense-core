# Evidence pack (Stage D scaffolding)

Run ID: `20251231_172032`

This run is a **synthetic** (non-Habitat) evidence pack to demonstrate the logging + artefact pipeline used in Stage D:
- Occupancy map creation
- Frontier extraction + clustering
- Semantic value map scoring (dummy hotspot)
- Frontier ranking and chosen frontier visualization

## Outputs
- `frames/01_occupancy.png` — occupancy grid
- `frames/02_frontiers.png` — extracted frontiers
- `frames/03_chosen_frontier.png` — chosen frontier highlighted
- `metrics.json` — summary metadata

Next step: swap synthetic grid for Habitat observations (Issue #4).
