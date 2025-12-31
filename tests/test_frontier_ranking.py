import numpy as np

from vlfm_repro.mapping.occupancy_grid import OccupancyGrid
from vlfm_repro.frontier.frontier_extractor import find_frontier_cells, cluster_frontiers
from vlfm_repro.vlm.value_map import ValueMap
from vlfm_repro.nav.frontier_ranker import rank_frontiers

def test_ranking_prefers_high_value_area():
    g = -1 * np.ones((40, 60), dtype=np.int8)
    g[10:30, 10:50] = 0
    og = OccupancyGrid(g)

    frontier = find_frontier_cells(og)
    clusters = cluster_frontiers(og, frontier, min_cluster_size=20)

    vm = ValueMap.zeros(*og.shape)
    vm.value[:, :] = 0.1
    vm.value[15:25, 48:58] = 0.9
    vm.conf[:, :] = 0.8

    ranked = rank_frontiers(vm, clusters, radius_cells=4, mode="mean")
    assert len(ranked) >= 1
    assert ranked[0].score >= ranked[-1].score
