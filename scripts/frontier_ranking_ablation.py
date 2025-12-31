from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from vlfm_repro.mapping.occupancy_grid import OccupancyGrid
from vlfm_repro.frontier.frontier_extractor import find_frontier_cells, cluster_frontiers
from vlfm_repro.vlm.value_map import ValueMap
from vlfm_repro.nav.frontier_ranker import rank_frontiers


OUT_DIR = "results/ablation"


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


def gaussian_blob(h: int, w: int, center_r: int, center_c: int, sigma: float) -> np.ndarray:
    rr, cc = np.ogrid[:h, :w]
    dist2 = (rr - center_r) ** 2 + (cc - center_c) ** 2
    return np.exp(-dist2 / (2 * (sigma ** 2))).astype(np.float32)


def apply_full_patch(vm: ValueMap, value: np.ndarray, conf: np.ndarray) -> None:
    # Fuse entire-map patch at (0,0)
    vm.update_patch(0, 0, value, conf)


def summarize_ranked(ranked, top_k: int = 10):
    out = []
    for rf in ranked[:top_k]:
        out.append(
            {
                "score": float(rf.score),
                "centroid_rc": [float(rf.cluster.centroid_rc[0]), float(rf.cluster.centroid_rc[1])],
                "centroid_xy": [float(rf.cluster.centroid_xy[0]), float(rf.cluster.centroid_xy[1])],
                "cluster_size": int(len(rf.cluster.cells)),
            }
        )
    return out


def plot_ablation(og: OccupancyGrid, frontier_cells, modes_ranked, out_png: str) -> None:
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

    # Mark top-3 for each mode with different markers
    markers = {"low_conf_patch": "x", "high_conf_patch": "^", "fused": "o"}
    for mode_name, ranked in modes_ranked.items():
        for i, rf in enumerate(ranked[:3]):
            cr, cc = rf.cluster.centroid_rc
            plt.scatter([cc], [cr], s=90, marker=markers.get(mode_name, "o"))
            plt.text(cc + 2, cr + 2, f"{mode_name}#{i+1}:{rf.score:.2f}", fontsize=8)

    plt.title("Stage C ablation: confidence fusion affects frontier ranking")
    plt.axis("off")
    os.makedirs(os.path.dirname(out_png), exist_ok=True)
    plt.tight_layout()
    plt.savefig(out_png, dpi=220)
    plt.close(fig)


def main() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)

    seed = int(os.environ.get("SEED", "0"))
    rng = np.random.default_rng(seed)

    og = make_synthetic_grid()
    frontier = find_frontier_cells(og, connectivity=4, require_free=True)
    clusters = cluster_frontiers(og, frontier, connectivity=8, min_cluster_size=20)

    h, w = og.shape

    # Patch A: high value but low confidence (weak influence when fused later)
    val_a = gaussian_blob(h, w, center_r=50, center_c=145, sigma=18.0)
    conf_a = (0.20 + 0.05 * rng.random((h, w))).astype(np.float32)

    # Patch B: moderate value but high confidence (stronger influence)
    val_b = 0.75 * gaussian_blob(h, w, center_r=55, center_c=80, sigma=22.0)
    conf_b = (0.90 + 0.05 * rng.random((h, w))).clip(0.0, 1.0).astype(np.float32)

    # Mode 1: only low-conf patch
    vm_low = ValueMap.zeros(h, w)
    apply_full_patch(vm_low, val_a, conf_a)
    ranked_low = rank_frontiers(vm_low, clusters, radius_cells=6, mode="mean")

    # Mode 2: only high-conf patch
    vm_high = ValueMap.zeros(h, w)
    apply_full_patch(vm_high, val_b, conf_b)
    ranked_high = rank_frontiers(vm_high, clusters, radius_cells=6, mode="mean")

    # Mode 3: fused (confidence-weighted)
    vm_fused = ValueMap.zeros(h, w)
    apply_full_patch(vm_fused, val_a, conf_a)
    apply_full_patch(vm_fused, val_b, conf_b)
    ranked_fused = rank_frontiers(vm_fused, clusters, radius_cells=6, mode="mean")

    modes_ranked = {
        "low_conf_patch": ranked_low,
        "high_conf_patch": ranked_high,
        "fused": ranked_fused,
    }

    out_json = Path(OUT_DIR) / "frontier_rankings.json"
    payload = {
        "seed": seed,
        "num_frontier_cells": int(len(frontier)),
        "num_clusters": int(len(clusters)),
        "modes": {
            k: summarize_ranked(v, top_k=10) for k, v in modes_ranked.items()
        },
    }
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    out_png = str(Path(OUT_DIR) / "frontier_ranking_ablation.png")
    plot_ablation(og, frontier, modes_ranked, out_png)

    print(f"[OK] Wrote: {out_json}")
    print(f"[OK] Wrote: {out_png}")


if __name__ == "__main__":
    main()
