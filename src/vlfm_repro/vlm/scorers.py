from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Tuple
import numpy as np


class VLMScorer(Protocol):
    def score(self, image: np.ndarray, prompt: str) -> Tuple[float, float]:
        """
        Returns (score, confidence) in [0, 1].
        score: how likely prompt matches the view
        confidence: reliability of the score
        """
        ...


@dataclass
class DummyScorer:
    """
    Deterministic, lightweight scorer for Stage C ablations.
    Produces stable outputs without any heavy model dependency.
    """
    seed: int = 0

    def score(self, image: np.ndarray, prompt: str) -> Tuple[float, float]:
        # Convert image to a stable scalar feature
        img = np.asarray(image, dtype=np.float32)
        if img.ndim >= 3:
            img = img.mean(axis=-1)
        mean_val = float(np.clip(np.nanmean(img) if img.size else 0.0, 0.0, 1.0))

        # Stable hash based on prompt + seed (no python hash randomness)
        s = (prompt + f"|{self.seed}").encode("utf-8")
        h = 0
        for b in s:
            h = (h * 131 + b) % 1000003

        # Map to [0,1]
        base = (h % 1000) / 999.0
        score = float(np.clip(0.25 * mean_val + 0.75 * base, 0.0, 1.0))
        confidence = float(np.clip(0.6 + 0.3 * (base - 0.5), 0.0, 1.0))
        return score, confidence


class BLIP2Scorer:
    """
    Placeholder for real BLIP-2 integration.
    On Mac, keep optional. We'll implement full model load on Linux/GPU later.
    """
    def __init__(self, *args, **kwargs):
        raise NotImplementedError(
            "BLIP-2 integration is tracked in Issue #2 but is optional on macOS. "
            "Use DummyScorer for now; implement BLIP-2 on Linux/GPU later."
        )
