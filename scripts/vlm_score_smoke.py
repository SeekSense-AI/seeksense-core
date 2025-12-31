from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from vlfm_repro.vlm.value_map import ValueMap
from vlfm_repro.vlm.scorers import DummyScorer
from vlfm_repro.vlm.observation_updater import Observation, apply_observation


def load_image(path: str | None) -> np.ndarray:
    if path is None:
        return np.random.default_rng(0).random((224, 224)).astype(np.float32)
    arr = mpimg.imread(path)
    arr = np.asarray(arr, dtype=np.float32)
    if arr.max() > 1.0:
        arr = arr / 255.0
    return arr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image", type=str, default=None, help="Optional path to an image")
    ap.add_argument("--prompt", type=str, default="chair", help="Text prompt")
    ap.add_argument("--seed", type=int, default=0, help="Dummy scorer seed")
    ap.add_argument("--out", type=str, default="results/vlm_smoke", help="Output folder")
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    img = load_image(args.image)
    scorer = DummyScorer(seed=args.seed)
    score, conf = scorer.score(img, args.prompt)

    vm = ValueMap.zeros(120, 160)
    apply_observation(vm, Observation(center_rc=(55, 80), score=score, confidence=conf, radius_cells=14))

    (out_dir / "vlm_score.json").write_text(
        json.dumps({"prompt": args.prompt, "seed": args.seed, "score": float(score), "confidence": float(conf)}, indent=2),
        encoding="utf-8",
    )

    plt.figure()
    plt.imshow(vm.value, origin="lower")
    plt.title(f"ValueMap (score={score:.2f}, conf={conf:.2f})")
    plt.axis("off")
    plt.savefig(out_dir / "value_map.png", dpi=220, bbox_inches="tight")
    plt.close()

    print(f"[OK] Wrote: {out_dir / 'vlm_score.json'}")
    print(f"[OK] Wrote: {out_dir / 'value_map.png'}")


if __name__ == "__main__":
    main()
