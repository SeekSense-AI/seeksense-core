# Stage C: Confidence fusion + frontier ranking ablation

This note documents the Stage C ablation that supports Issue #3.

## Goal
Demonstrate a reproducible frontier ranking flow:
1) create a synthetic occupancy grid (explored/free + obstacles + unknown)
2) extract frontier cells and cluster them
3) build semantic value patches with different confidence levels
4) fuse patches via confidence-weighted update
5) rank frontiers and export evidence artefacts

## How to run
pip install -e .
python scripts/frontier_ranking_ablation.py

## Outputs
- results/ablation/frontier_rankings.json
- results/ablation/frontier_ranking_ablation.png
