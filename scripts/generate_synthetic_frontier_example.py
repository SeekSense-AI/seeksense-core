from __future__ import annotations

import json
import os
import numpy as np
import matplotlib.pyplot as plt

from vlfm_repro.mapping.occupancy_grid import OccupancyGrid
from vlfm_repro.frontier.frontier_extractor import find_frontier_cells, cluster_frontiers
from vlfm_repro.vlm.value_map import ValueMap
from vlfm_repro.nav.frontier_ranker import rank_frontiers

OUT_DIR = "results"

def make_synthetic_grid(h: int = 120, w: int = 160) -> OccupancyGrid:
    grid = -1 * np.ones((h, w), dtype=np.int8)

    # Explored free area (room + corridor)
    grid[20:90, 20:120] = 0
    grid[45:55, 120:150] = 0

    # Obstacles
    grid[35:40, 40:95] = 1
    grid[60:65, 30:80] = 1
    grid[25:80, 100:103] = 1

    return OccupancyGrid(grid=grid, resolution=0.05, origin_xy=(0.0, 0.0))

def make_synthetic_value_map(h: int, w: int) -> ValueMap:
    vm = ValueMap.zeros(h, w)
    rr, cc = np.ogrid[:h, :w]
    center_r, center_c = 50, 145
    dist2 = (rr - center_r) ** 2 + (cc - center_c) ** 2
    blob = np.exp(-dist2 / (2 * (18 ** 2))).astype(np.float32)
    vm.value = blob
    vm.conf[:] = 0.8
    return vm

def plot_maps(og: OccupancyGrid, frontier_cells, ranked, out_png: str) -> None:
    g = og.grid.astype(np.int16)
    disp = np.zeros_like(g, dtype=np.float32)
    disp[g == -1] = 0.2  # unknown
    disp[g == 0] = 0.8   # free
    disp[g == 1] = 0.0   # occupied

    fig = plt.figure(figsize=(10, 6))
    plt.imshow(disp, origin="lower")

    if frontier_cells:
        fr = np.array([p[0] for p in frontier_cells])
        fc = np.array([p[1] for p in frontier_cells])
        plt.scatter(fc, fr, s=2)

    for i, rf in enumerate(ranked[:3]):
        cr, cc = rf.cluster.centroid_rc
        plt.scatter([cc], [cr], s=80, marker="x")
        plt.text(cc + 2, cr + 2, f"#{i+1}:{rf.score:.2f}", fontsize=9)

    plt.title("Synthetic Occupancy + Frontiers + Ranked Waypoints")
    plt.axis("off")
    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    plt.tight_layout()
    plt.savefig(out_png, dpi=220)
    plt.close(fig)

def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)

    og = make_synthetic_grid()
    frontier = find_frontier_cells(og, connectivity=4, require_free=True)
    clusters = cluster_frontiers(og, frontier, connectivity=8, min_cluster_size=20)

    vm = make_synthetic_value_map(*og.shape)
    ranked = rank_frontiers(vm, clusters, radius_cells=6, mode="mean")

    out_png = os.path.join(OUT_DIR, "frontier_map_example.png")
    plot_maps(og, frontier, ranked, out_png)

    waypoints = []
    for rf in ranked[:10]:
        waypoints.append({
            "score": rf.score,
            "centroid_rc": [rf.cluster.centroid_rc[0], rf.cluster.centroid_rc[1]],
            "centroid_xy": [rf.cluster.centroid_xy[0], rf.cluster.centroid_xy[1]],
            "cluster_size": len(rf.cluster.cells),
        })

    out_json = os.path.join(OUT_DIR, "frontier_waypoints.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump({"top_waypoints": waypoints}, f, indent=2)

    print(f"Wrote: {out_png}")
    print(f"Wrote: {out_json}")

if __name__ == "__main__":
    main()
