from __future__ import annotations

from dataclasses import dataclass
import numpy as np
from vlfm_repro.vlm.value_map import ValueMap


@dataclass
class Observation:
    center_rc: tuple[int, int]
    score: float
    confidence: float
    radius_cells: int = 10


def apply_observation(vm: ValueMap, obs: Observation) -> None:
    """
    Applies a gaussian patch to the ValueMap using the existing vm.update_patch(...)
    without modifying ValueMap internals.
    """
    h, w = vm.value.shape
    cr, cc = obs.center_rc
    r = int(obs.radius_cells)

    r0 = max(0, cr - r)
    r1 = min(h, cr + r + 1)
    c0 = max(0, cc - r)
    c1 = min(w, cc + r + 1)

    yy, xx = np.mgrid[r0:r1, c0:c1]
    dist2 = (yy - cr) ** 2 + (xx - cc) ** 2
    sigma2 = max(1.0, (r * 0.6) ** 2)
    kernel = np.exp(-dist2 / (2.0 * sigma2)).astype(np.float32)

    value_patch = (obs.score * kernel).astype(np.float32)
    conf_patch = (obs.confidence * np.ones_like(kernel, dtype=np.float32))

    vm.update_patch(r0, c0, value_patch, conf_patch)
