# Reproducibility

This project is designed to be reproducible in two modes:

## Mode 1 — Lightweight (Stage A–C)
Runs entirely on CPU and produces:
- unit tests passing
- synthetic frontier-map outputs (png + json)

Suggested environment:
- Python 3.10+
- macOS / Linux / Windows
- No GPU required

## Mode 2 — Simulator (Stage D)
Habitat + ObjectNav evaluation can be added as a smoke run.
This is hardware and driver dependent.

Recommended:
- Ubuntu 22.04
- NVIDIA GPU (optional but helps)
- Pin CUDA + PyTorch versions as per Habitat docs

## Version pinning
Stage A–C pins lightweight versions in `requirements.txt`.

For Stage D, record exact versions used in:
- `results/habitat_runs/<run_id>/env_versions.txt`
- `results/habitat_runs/<run_id>/command.txt`
