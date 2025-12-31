import numpy as np

from vlfm_repro.mapping.occupancy_grid import OccupancyGrid
from vlfm_repro.frontier.frontier_extractor import find_frontier_cells, cluster_frontiers

def test_frontier_cells_simple_boundary():
    g = -1 * np.ones((10, 10), dtype=np.int8)
    g[:, :5] = 0
    og = OccupancyGrid(g)

    frontier = find_frontier_cells(og, connectivity=4, require_free=True)
    expected = {(r, 4) for r in range(10)}
    assert expected.issubset(set(frontier))

def test_cluster_frontiers_returns_centroids():
    g = -1 * np.ones((30, 30), dtype=np.int8)
    g[5:25, 5:25] = 0
    og = OccupancyGrid(g)

    frontier = find_frontier_cells(og, connectivity=4, require_free=True)
    clusters = cluster_frontiers(og, frontier, connectivity=8, min_cluster_size=10)

    assert len(clusters) >= 1
    cl = clusters[0]
    assert len(cl.cells) >= 10
    assert isinstance(cl.centroid_rc[0], float)
    assert isinstance(cl.centroid_xy[0], float)
