from __future__ import annotations

from dataclasses import dataclass
import numpy as np
from typing import Iterable

from vlfm_repro.mapping.occupancy_grid import OccupancyGrid

@dataclass(frozen=True)
class FrontierCluster:
    cells: list[tuple[int, int]]          # (r,c)
    centroid_rc: tuple[float, float]      # float centroid in grid coords
    centroid_xy: tuple[float, float]      # world coords centroid

def find_frontier_cells(
    og: OccupancyGrid,
    connectivity: int = 4,
    require_free: bool = True,
) -> list[tuple[int, int]]:
    """Return frontier cells: free (or non-occupied) cells adjacent to unknown.

    A frontier cell is typically defined as:
    - a free cell (0)
    - with at least one neighbor that is unknown (-1)
    """
    g = og.grid
    h, w = g.shape
    frontier = []
    for r in range(h):
        for c in range(w):
            v = int(g[r, c])
            if require_free and v != 0:
                continue
            if not require_free and v == 1:
                continue
            for rr, cc in og.neighbors(r, c, connectivity=connectivity):
                if int(g[rr, cc]) == -1:
                    frontier.append((r, c))
                    break
    return frontier

def _bfs_components(
    cells: set[tuple[int, int]],
    og: OccupancyGrid,
    connectivity: int = 8
) -> list[list[tuple[int, int]]]:
    comps: list[list[tuple[int, int]]] = []
    visited: set[tuple[int, int]] = set()
    for cell in cells:
        if cell in visited:
            continue
        q = [cell]
        visited.add(cell)
        comp = []
        while q:
            cur = q.pop()
            comp.append(cur)
            for nb in og.neighbors(cur[0], cur[1], connectivity=connectivity):
                if nb in cells and nb not in visited:
                    visited.add(nb)
                    q.append(nb)
        comps.append(comp)
    return comps

def cluster_frontiers(
    og: OccupancyGrid,
    frontier_cells: Iterable[tuple[int, int]],
    connectivity: int = 8,
    min_cluster_size: int = 5
) -> list[FrontierCluster]:
    """Cluster frontier cells into connected components and compute centroids."""
    cell_set = set(frontier_cells)
    comps = _bfs_components(cell_set, og, connectivity=connectivity)
    clusters: list[FrontierCluster] = []
    for comp in comps:
        if len(comp) < min_cluster_size:
            continue
        rs = np.array([p[0] for p in comp], dtype=np.float32)
        cs = np.array([p[1] for p in comp], dtype=np.float32)
        cr = float(rs.mean())
        cc = float(cs.mean())
        rr = int(round(cr))
        rc = int(round(cc))
        rr = max(0, min(rr, og.shape[0] - 1))
        rc = max(0, min(rc, og.shape[1] - 1))
        cx, cy = og.world_xy(rr, rc)
        clusters.append(FrontierCluster(cells=list(comp), centroid_rc=(cr, cc), centroid_xy=(cx, cy)))
    clusters.sort(key=lambda cl: len(cl.cells), reverse=True)
    return clusters
