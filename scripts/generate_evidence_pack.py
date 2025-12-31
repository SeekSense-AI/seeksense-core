from __future__ import annotations

from datetime import datetime
from pathlib import Path
import json

import numpy as np
import matplotlib.pyplot as plt

from vlfm_repro.mapping.occupancy_grid import OccupancyGrid
from vlfm_repro.frontier.frontier_extractor import find_frontier_cells, cluster_frontiers
from vlfm_repro.vlm.value_map import ValueMap
from vlfm_repro.nav.frontier_ranker import rank_frontiers


def make_synthetic_grid(h: int = 120, w: int = 160) -> OccupancyGrid:
    grid = -1 * np.ones((h, w), dtype=np.int8)
    grid[20:95, 20:130] = 0
    grid[55:65, 130:150] = 0
    grid[35:40, 40:110] = 1
    grid[25:85, 95:98] = 1
    grid[70:75, 35:80] = 1
    return OccupancyGrid(grid=grid, resolution=0.05, origin_xy=(0.0, 0.0))


def save_png(path: Path, title: str, base: np.ndarray, overlays: list[tuple[np.ndarray, dict]] | None = None):
    plt.figure(figsize=(10, 6))
    plt.imshow(base, origin="lower")
    if overlays:
        for pts, kw in overlays:
            plt.scatter(pts[:, 1], pts[:, 0], **kw)
    plt.title(title)
    plt.axis("off")
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, dpi=220, bbox_inches="tight")
    plt.close()


def main():
    run_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    out_dir = Path("results/habitat_runs") / run_id
    frames = out_dir / "frames"
    frames.mkdir(parents=True, exist_ok=True)

    og = make_synthetic_grid()

    # Visualization base map: unknown=0.2, free=0.8, occupied=0.0
    g = og.grid.astype(np.int16)
    base = np.zeros_like(g, dtype=np.float32)
    base[g == -1] = 0.2
    base[g == 0] = 0.8
    base[g == 1] = 0.0

    frontier_cells = find_frontier_cells(og, connectivity=4, require_free=True)
    clusters = cluster_frontiers(og, frontier_cells, connectivity=8, min_cluster_size=20)

    # Dummy semantic map: simple gaussian hotspot
    h, w = og.shape
    vm = ValueMap.zeros(h, w)
    rr, cc = np.ogrid[:h, :w]
    hotspot = np.exp(-((rr - 55) ** 2 + (cc - 85) ** 2) / (2 * 20.0 ** 2)).astype(np.float32)
    conf = (0.85 * np.ones_like(hotspot)).astype(np.float32)
    vm.update_patch(0, 0, hotspot, conf)

    ranked = rank_frontiers(vm, clusters, radius_cells=6, mode="mean")
    best = ranked[0] if ranked else None

    # Save 3 frames
    if len(frontier_cells) > 0:
        fpts = np.array(frontier_cells, dtype=int)
    else:
        fpts = np.zeros((0, 2), dtype=int)

    save_png(frames / "01_occupancy.png", "Occupancy map (synthetic)", base)

    save_png(
        frames / "02_frontiers.png",
        f"Frontiers (cells={len(frontier_cells)}, clusters={len(clusters)})",
        base,
        overlays=[(fpts, {"s": 2})],
    )

    overlays = [(fpts, {"s": 2})]
    if best is not None:
        cr, cc_ = best.cluster.centroid_rc
        overlays.append((np.array([[cr, cc_]]), {"s": 110, "marker": "o"}))

    save_png(
        frames / "03_chosen_frontier.png",
        "Chosen frontier (rank-1) + frontiers",
        base,
        overlays=overlays,
    )

    # Write evidence + metadata
    meta = {
        "run_id": run_id,
        "num_frontier_cells": int(len(frontier_cells)),
        "num_clusters": int(len(clusters)),
        "ranked_top5": [
            {
                "score": float(r.score),
                "centroid_rc": [float(r.cluster.centroid_rc[0]), float(r.cluster.centroid_rc[1])],
                "cluster_size": int(len(r.cluster.cells)),
            }
            for r in ranked[:5]
        ],
    }
    (out_dir / "metrics.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    evidence = out_dir / "EVIDENCE.md"
    evidence.write_text(
        "\n".join(
            [
                "# Evidence pack (Stage D scaffolding)",
                "",
                f"Run ID: `{run_id}`",
                "",
                "This run is a **synthetic** (non-Habitat) evidence pack to demonstrate the logging + artefact pipeline used in Stage D:",
                "- Occupancy map creation",
                "- Frontier extraction + clustering",
                "- Semantic value map scoring (dummy hotspot)",
                "- Frontier ranking and chosen frontier visualization",
                "",
                "## Outputs",
                "- `frames/01_occupancy.png` — occupancy grid",
                "- `frames/02_frontiers.png` — extracted frontiers",
                "- `frames/03_chosen_frontier.png` — chosen frontier highlighted",
                "- `metrics.json` — summary metadata",
                "",
                "Next step: swap synthetic grid for Habitat observations (Issue #4).",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(f"[OK] Evidence pack written to: {out_dir}")


if __name__ == "__main__":
    main()
