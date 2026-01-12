from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass
class SmokeConfig:
    scene: str = "example_scene"
    episodes: int = 1
    max_steps: int = 50
    prompt: str = "chair"
    out_root: str = "results/habitat_runs"


def utc_run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def try_import_habitat() -> Optional[str]:
    try:
        import habitat  # type: ignore
        return getattr(habitat, "__version__", "importable")
    except Exception:
        return None


def main() -> None:
    cfg = SmokeConfig(
        scene=os.environ.get("SCENE", "example_scene"),
        episodes=int(os.environ.get("EPISODES", "1")),
        max_steps=int(os.environ.get("MAX_STEPS", "50")),
        prompt=os.environ.get("PROMPT", "chair"),
        out_root=os.environ.get("OUT_ROOT", "results/habitat_runs"),
    )

    run_id = utc_run_id()
    out_dir = Path(cfg.out_root) / run_id
    (out_dir / "frames").mkdir(parents=True, exist_ok=True)

    habitat_marker = try_import_habitat()

    metrics: Dict[str, Any] = {
        "run_id": run_id,
        "mode": "habitat" if habitat_marker else "stub",
        "scene": cfg.scene,
        "episodes": cfg.episodes,
        "max_steps": cfg.max_steps,
        "prompt": cfg.prompt,
        "habitat": {"available": bool(habitat_marker), "marker": habitat_marker},
        "results": {"success_rate": None, "spl": None, "path_length": None, "num_steps": None},
        "notes": [],
    }

    if not habitat_marker:
        metrics["notes"].append(
            "Habitat not available on this machine. This is a stub run to prove pipeline + schema."
        )
        write_json(out_dir / "metrics.json", metrics)
        write_text(
            out_dir / "EVIDENCE.md",
            "\n".join(
                [
                    "# Stage D — Habitat smoke run (stub)",
                    "",
                    f"Run ID: {run_id}",
                    "",
                    "Habitat is not installed/available on this machine.",
                    "This run proves the Stage D output pipeline and schema.",
                    "",
                    "Outputs:",
                    "- metrics.json",
                    "- EVIDENCE.md",
                    "- frames/ (reserved)",
                    "",
                    "Next step: run on Linux with Habitat-Sim/Habitat-Lab installed, then wire env + metrics.",
                    "",
                ]
            ),
        )
        print(f"[OK] Stub run written to: {out_dir}")
        return

    metrics["notes"].append(
        "Habitat import succeeded, but full env wiring is not implemented in this scaffold yet."
    )
    write_json(out_dir / "metrics.json", metrics)
    write_text(
        out_dir / "EVIDENCE.md",
        "\n".join(
            [
                "# Stage D — Habitat smoke run (scaffold)",
                "",
                f"Run ID: {run_id}",
                "",
                "Habitat import succeeded. Full environment setup + episode loop will be added next.",
                "",
            ]
        ),
    )
    print(f"[OK] Scaffold run written to: {out_dir}")


if __name__ == "__main__":
    main()
