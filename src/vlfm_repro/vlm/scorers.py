from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Tuple
import numpy as np


class VLMScorer(Protocol):
    def score(self, image: np.ndarray, prompt: str) -> Tuple[float, float]:
        """Return (score, confidence) in [0, 1]."""
        ...


@dataclass
class DummyScorer:
    """
    Deterministic, lightweight scorer for Stage C smoke runs.
    Produces stable outputs without any heavy ML dependencies.
    """
    seed: int = 0

    def score(self, image: np.ndarray, prompt: str) -> Tuple[float, float]:
        img = np.asarray(image, dtype=np.float32)
        if img.ndim >= 3:
            img = img.mean(axis=-1)
        mean_val = float(np.clip(np.nanmean(img) if img.size else 0.0, 0.0, 1.0))

        s = (prompt + f"|{self.seed}").encode("utf-8")
        h = 0
        for b in s:
            h = (h * 131 + b) % 1000003

        base = (h % 1000) / 999.0
        score = float(np.clip(0.25 * mean_val + 0.75 * base, 0.0, 1.0))
        confidence = float(np.clip(0.65 + 0.25 * (base - 0.5), 0.0, 1.0))
        return score, confidence


class BLIP2Scorer:
    """
    Placeholder for Phase 2 (Linux/GPU).
    We'll implement real BLIP-2 loading + scoring later.
    """
    def __init__(self, *args, **kwargs):
        raise NotImplementedError(
            "BLIP-2 integration is Phase 2 (Linux/GPU). Use DummyScorer for now."
        )
