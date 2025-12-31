from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from vlfm_repro.frontier.frontier_extractor import FrontierCluster
from vlfm_repro.vlm.value_map import ValueMap

@dataclass(frozen=True)
class RankedFrontier:
    cluster: FrontierCluster
    score: float

def score_cluster(
    value_map: ValueMap,
    cluster: FrontierCluster,
    radius_cells: int = 3,
    mode: str = "mean",
) -> float:
    """Score a frontier cluster using value-map statistics near its centroid."""
    h, w = value_map.value.shape
    cr, cc = cluster.centroid_rc
    r = int(round(cr))
    c = int(round(cc))
    r0 = max(0, r - radius_cells)
    r1 = min(h, r + radius_cells + 1)
    c0 = max(0, c - radius_cells)
    c1 = min(w, c + radius_cells + 1)

    window = value_map.value[r0:r1, c0:c1]
    if window.size == 0:
        return 0.0

    if mode == "mean":
        return float(window.mean())
    if mode == "max":
        return float(window.max())
    raise ValueError("mode must be 'mean' or 'max'")

def rank_frontiers(
    value_map: ValueMap,
    clusters: list[FrontierCluster],
    radius_cells: int = 3,
    mode: str = "mean",
) -> list[RankedFrontier]:
    ranked = [RankedFrontier(cluster=cl, score=score_cluster(value_map, cl, radius_cells, mode)) for cl in clusters]
    ranked.sort(key=lambda rf: rf.score, reverse=True)
    return ranked
