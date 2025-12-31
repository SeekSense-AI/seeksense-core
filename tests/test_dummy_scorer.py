import numpy as np
from vlfm_repro.vlm.scorers import DummyScorer

def test_dummy_scorer_deterministic():
    img = np.zeros((10, 10), dtype=np.float32)
    s1 = DummyScorer(seed=0).score(img, "chair")
    s2 = DummyScorer(seed=0).score(img, "chair")
    assert s1 == s2
