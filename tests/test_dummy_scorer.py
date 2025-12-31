import numpy as np
from vlfm_repro.vlm.scorers import DummyScorer

def test_dummy_scorer_is_deterministic():
    img = np.zeros((10, 10), dtype=np.float32)
    a = DummyScorer(seed=0).score(img, "chair")
    b = DummyScorer(seed=0).score(img, "chair")
    assert a == b
