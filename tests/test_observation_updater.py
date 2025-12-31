import numpy as np
from vlfm_repro.vlm.value_map import ValueMap
from vlfm_repro.vlm.observation_updater import Observation, apply_observation

def test_apply_observation_changes_map():
    vm = ValueMap.zeros(50, 60)
    before = vm.value.copy()
    apply_observation(vm, Observation(center_rc=(25, 30), score=1.0, confidence=1.0, radius_cells=6))
    assert np.sum(np.abs(vm.value - before)) > 0.0
    assert vm.value.max() <= 1.0 + 1e-6
