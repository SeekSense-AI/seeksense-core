from __future__ import annotations

from dataclasses import dataclass
import numpy as np

@dataclass
class ValueMap:
    """Top-down value map + confidence map.

    Model-agnostic container. In a full VLFM reproduction, value updates
    would come from a VLM scoring (image, prompt).

    - value: float32 (H,W) in [0,1] (suggested)
    - conf:  float32 (H,W) in [0,1]
    """
    value: np.ndarray
    conf: np.ndarray

    @classmethod
    def zeros(cls, h: int, w: int) -> "ValueMap":
        return cls(
            value=np.zeros((h, w), dtype=np.float32),
            conf=np.zeros((h, w), dtype=np.float32),
        )

    def update_patch(
        self,
        r0: int, c0: int,
        patch_value: np.ndarray,
        patch_conf: np.ndarray,
    ) -> None:
        """Fuse a patch into the global map via confidence-weighted averaging."""
        ph, pw = patch_value.shape
        r1, c1 = r0 + ph, c0 + pw
        v_old = self.value[r0:r1, c0:c1]
        c_old = self.conf[r0:r1, c0:c1]

        c_new = np.clip(patch_conf, 0.0, 1.0).astype(np.float32)
        v_new = np.clip(patch_value, 0.0, 1.0).astype(np.float32)

        denom = (c_old + c_new)
        out = np.where(denom > 1e-6, (c_old * v_old + c_new * v_new) / denom, v_old)

        self.value[r0:r1, c0:c1] = out
        self.conf[r0:r1, c0:c1] = np.clip(denom, 0.0, 1.0)
