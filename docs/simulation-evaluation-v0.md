# SeekSense AI – Simulation & Evaluation Plan (v0)

## 1. Goals

The goal of this first simulation phase is to:

- Demonstrate an end-to-end **semantic search loop** in a ROS2 + Nav2 environment.
- Compare SeekSense-style behaviour against a simple baseline search.
- Record basic metrics (time-to-find, success rate, path length) that can later be replicated on real robots.

This is not about perfect model performance yet; it is about proving that the architecture and API are practical.

## 2. Target stack

- **ROS2 distribution**: Humble (or Foxy if required by the simulator)
- **Navigation**: Nav2
- **Simulator**: Gazebo or similar
- **Robot model**:
  - Simple differential-drive base
  - RGB or RGB-D camera mounted at a realistic height
  - Standard LiDAR or depth-based navigation (Nav2)

## 3. World and scenario design

### 3.1 Base world

Initial world:

- One main corridor
- 3–4 side bays or rooms
- A few static obstacles (boxes, shelves)
- One **target object** (e.g. trolley or box) placed in one of the bays

Later variations:

- Move the target to a different bay
- Add more clutter
- Slightly alter corridor geometry

### 3.2 Tasks

Single-task scenario for v0:

> “Find the trolley in one of the bays off the main corridor.”

The robot starts at a fixed start pose in the corridor.

## 4. Conditions to compare

### 4.1 Baseline: naive search

A simple search strategy:

- Visit each bay sequentially in a fixed order.
- In each bay, perform a simple sweep or fixed set of viewpoints.
- Stop when the target is detected or all bays are visited.

This represents how many systems behave today when they do not use semantic frontier maps.

### 4.2 SeekSense-style semantic search

Use the SeekSense semantic loop:

- Same start pose and world
- Robot streams pose + camera frames to the SeekSense backend
- SeekSense:
  - Builds a semantic frontier map
  - Selects the next promising waypoint (corridor or bay) based on semantic likelihood + coverage
  - Returns waypoints to the robot via `search_next`
- Once the target is visible, `search_verify` returns a safe approach pose

The key difference: the robot does not just visit bays in a fixed order, it prioritises **semantically promising** areas.

## 5. Metrics

For each run, record:

- **Time-to-find**  
  Time from start to verification of the target.

- **Success rate**  
  Percentage of runs where the target is correctly found within a time limit.

- **Path length**  
  Total distance travelled by the robot (from odometry).

- **Number of waypoints visited**  
  How many waypoints the navigation stack was asked to visit.

- **Qualitative behaviour**  
  - Heatmap or trace of where the robot searched
  - Whether it spent time in obviously irrelevant areas

Early on, even approximate metrics are acceptable as long as they are **consistent and repeatable**.

## 6. Experimental procedure (v0)

1. **Setup**
   - Launch the simulated world with the corridor and bays.
   - Spawn the robot at a fixed start pose.
   - Place the target object in a known bay (but treat its location as unknown to the algorithm).

2. **Baseline runs**
   - Run the naive search strategy N times (e.g. N = 10).
   - Record metrics for each run.
   - Reset the world between runs.

3. **SeekSense runs**
   - Run the SeekSense-style semantic search N times (same N, same starting pose).
   - Use the same target location(s) as the baseline.
   - Record metrics for each run.

4. **Compare**
   - Compute average time-to-find and path length.
   - Note any cases where:
     - Baseline succeeds but SeekSense fails, and why.
     - SeekSense succeeds faster or with less travel.

5. **Report**
   - Summarise results in a simple table or chart.
   - Capture screenshots of:
     - The simulated world
     - Example search traces
     - Qualitative differences between behaviours

These can be reused in pitch decks, technical appendices, and investor materials.

## 7. Implementation notes

- In v0, the “semantic” part can be approximated by:
  - A synthetic heatmap per bay (e.g. one bay has higher likelihood).
  - Simple heuristic rules, rather than full vision–language models.
- The important part is the **shape of the API and loop**:
  - `search_start` → `search_next` (loop) → `search_verify`.
- Once the loop is stable, the underlying scoring can be replaced with real vision–language perception.

## 8. Summary

This simulation and evaluation plan is designed to be:

- Small enough to implement in a short time.
- Realistic enough to demonstrate the core value of SeekSense.
- Repeatable, so later real-world pilots can be compared against the same basic metrics.

It shows that SeekSense is being developed as a measurable, testable system rather than just a concept.