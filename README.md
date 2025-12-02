# SeekSense AI – Training-Free Semantic Search for Robots

This repository contains the early R&D work for **SeekSense AI** – a semantic search layer for indoor mobile robots.

SeekSense provides a **training-free “find-by-name” API** that lets robots search for objects and locations in unfamiliar environments using natural language (e.g. _“find the cleaning trolley near ward C”_, _“locate pallet 18B in aisle 4”_). The API sits on top of existing navigation stacks (e.g. ROS2 + Nav2) and focuses on semantic frontier mapping, waypoint selection and safe approach poses.

## Repository layout

- `docs/`
  - **`architecture.md`** – Technical architecture & semantic search flow.
  - **`simulation-evaluation-v0.md`** – Simulation & evaluation plan for the first prototype (v0).
- `sim/`
  - `seeksense_sim/` – Placeholder ROS2 package for integrating SeekSense with a Nav2-based robot stack.

## Current focus (v0.1 – Simulation prototype)

- Run a full **semantic search loop** in ROS2 + Nav2 simulation (Gazebo or similar):
  - Subscribe to `/camera/image_raw` and pose (`/odom` or `/tf`).
  - Implement a basic semantic frontier map and scoring loop (placeholder initially).
  - Generate waypoints and verify a target object in a simple world (corridor + bays + trolley).
- Capture metrics for:
  - Time-to-find vs a simple baseline (e.g. naïve sweep).
  - Success rate.
  - Qualitative behaviour (search trace, coverage).

## Tech stack (planned)

- **Robot side**
  - ROS2 Humble
  - Nav2 for navigation and safety
  - RGB / RGB-D camera

- **SeekSense side**
  - Python-based backend (prototype)
  - Semantic frontier mapping
  - Session API:
    - `search_start`
    - `search_next`
    - `search_verify`
    - `checkpoint`

    ## Roadmap

This repository is the R&D core for SeekSense AI – a training-free semantic search layer for indoor mobile robots. The focus is to move in small, testable steps:

### v0.1 – Simulation prototype (0–3 months)
- ROS2 + Nav2 simulation (Gazebo or similar).
- Single-robot corridor + bays world.
- End-to-end semantic search loop:
  - `search_start` → `search_next` → `search_verify`.
- Baseline vs SeekSense-style search comparison:
  - time-to-find,
  - path length,
  - success rate.

### v0.2 – Single-robot MVP in a real environment (3–9 months)
- Expose SeekSense as a documented API.
- Integrate with one real indoor robot (e.g. lab platform / AMR).
- Run “find-by-name” tasks (e.g. trolleys, pallets, equipment).
- Capture metrics:
  - reduction in custom engineering effort per site,
  - time saved versus naïve scripts.

### v0.3 – Multi-site robustness & partner pilots (9–18 months)
- Support 2–3 different environments (warehouse / hospital / campus).
- Harden logging, replay, and grading tools for partner teams.
- Add early features on top of the same loop:
  - better failure modes (“likely upstairs / blocked area”),
  - multi-target search,
  - simple semantic memory (“where was it last seen?”).

The repo is intentionally small at this stage: the goal is to show clear, iterative progress from prototype → MVP → multi-site pilots.

## Status

This repo is currently an **early R&D scaffold**:
- Documentation first (`docs/`).
- ROS2 simulation package skeleton in `sim/`.
- Algorithms and API implementation to be added iteratively based on pilots and experiments.
