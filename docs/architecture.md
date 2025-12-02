# SeekSense AI – Technical Architecture & Semantic Search Flow

## 1. Purpose of this document

This document gives a clear, practical overview of how SeekSense AI works from a technical point of view. It explains the main components, how the system integrates with existing robot stacks, and the roadmap from simulation prototype to real-world deployment. It is intended to support the business plan and financial model by showing that the product has a concrete technical foundation.

## 2. Brief context

SeekSense AI is a UK-based deep-tech company building *Seek*, a training-free semantic search API for indoor mobile robots. Seek allows robots to “find things by name” in unfamiliar environments by combining perception, mapping, language understanding and exploration.

The core idea:

- The robot keeps its existing navigation and safety stack (e.g. ROS2 + Nav2).  
- SeekSense AI provides a *semantic search layer* that decides what to look for and where to explore next, based on a natural-language description  
  (e.g. “find the cleaning trolley near ward C”, “locate pallet 18B in aisle 4”).

## 3. High-level system overview

At a high level, the system looks like this:

### Robot side (on board)

Runs ROS2 or a compatible navigation stack (e.g. Nav2) and provides:

- Pose estimates (where the robot is)
- Map / costmap (where it can safely move)
- Camera frames (RGB or RGB-D)

A thin SeekSense client on the robot:

- Subscribes to camera + pose topics
- Sends observations and target queries to SeekSense AI
- Receives waypoints / approach poses and forwards them to the navigation stack

### SeekSense AI side (backend service)

The SeekSense service:

- Receives pose and camera data from the robot
- Builds and updates a *semantic frontier map* conditioned on the target description
- Selects promising frontiers and waypoints for the robot to explore
- Returns waypoints and safe approach poses via a simple API:
  - search_start
  - search_next
  - search_verify
  - checkpoint
- Logs each run for replay, grading and debugging

The result is that the robot behaves as if it has a reusable *“find-by-name” skill*, without the site needing custom semantic waypoints and scripts for every building.

## 4. SeekSense AI architecture

### 4.1 Robot and environment assumptions

SeekSense AI is designed for indoor mobile robots that:

- Can estimate their pose (e.g. via SLAM or AMCL)
- Have a navigation stack capable of:
  - Obstacle avoidance
  - Path planning
  - Safety / speed limits
- Can stream:
  - Camera frames (RGB or RGB-D)
  - Associated pose information (timestamped)

SeekSense AI does *not* replace base-level safety or low-level control. It assumes those functions already exist and focuses on the semantic layer on top.

### 4.2 Integration with ROS2 / Nav2

On the robot side, a typical integration with ROS2 / Nav2 looks like:

- A ROS2 node (Seek client) subscribes to:
  - /camera/image or /camera/image_raw
  - /tf or /odom for pose

The client:

1. Calls search_start with:
   - Target description (text)
   - Current pose
   - Basic camera model / intrinsics
2. Receives a waypoint from SeekSense AI
3. Sends this waypoint to Nav2 as a navigation goal
4. While moving, streams new pose + images and calls search_next repeatedly
5. Once SeekSense AI reports that the target is visible and verified, it receives a *safe approach pose* and passes that to Nav2 as the final goal

This keeps roles clean:

- *Nav2*: avoids walls, handles stairs as obstacles, executes motion safely  
- *SeekSense AI*: decides which regions are promising and where to search next, based on meaning

### 4.3 Core components inside SeekSense AI

#### 4.3.1 Perception & language interface

- Takes raw camera frames and the text query (e.g. “blue trolley in bay 4”)
- Uses vision–language techniques to estimate:
  - Which regions of the image likely contain the described object or area
  - A semantic score for each observation
- Outputs per-frame semantic information that can be mapped into the robot’s coordinate frame

This layer is modular so it can be upgraded over time as models evolve.

#### 4.3.2 Semantic frontier map builder

Maintains an internal map where each cell or region has:

- Explored / unexplored state
- A semantic likelihood of containing the target, based on past observations

It:

- Updates this map as new frames and pose data arrive from the robot
- Identifies *frontiers* (boundaries between explored and unexplored cells)
- Annotates them with their current semantic likelihood

This is where SeekSense AI turns raw vision–language output into a spatial structure the robot can use.

#### 4.3.3 Scoring, selection and waypoint generation

Evaluates candidate frontiers and regions using a combination of:

- Semantic likelihood
- Distance / travel cost
- Coverage (how much new area will be explored)
- Safety margins and navigation constraints

Produces:

- The next waypoint to visit (for search_next)
- A safe approach pose once the target is detected and verified (for search_verify)

These scoring functions and heuristics are a key part of the IP and will be tuned using real pilot data.

#### 4.3.4 Session and state management

Each search is handled as a *session*, with:

- A unique session ID
- Stored semantic map and logs
- Termination conditions (found / not found / timeout)

The API surface:

- search_start – creates a new session
- search_next – advances the search and returns the next waypoint
- search_verify – confirms whether the target is present and returns an approach pose
- checkpoint – saves state for replay or resuming later

This makes SeekSense AI usable as a well-defined service that can run multiple searches in parallel across different robots or sites.

#### 4.3.5 Logging, replay and grading tools

To help robotics teams adopt SeekSense AI, the system will provide tools for:

- Logging each search run (poses, waypoints, semantic scores, results)
- Replaying runs to understand:
  - Where the robot searched
  - Why certain waypoints were chosen
- Grading different configurations or versions of the service

These tools support internal tuning and give customers clear visibility into system behaviour.

## 5. Data flows and API behaviour

A typical data flow for a single semantic search looks like this:

### 5.1 Search start

Robot sends:

- Target description (e.g. “cleaning trolley for ward C”)
- Current pose
- Camera model and an initial frame

SeekSense AI:

- Creates a new session
- Initialises a semantic frontier map around the robot’s current area
- Returns the first waypoint

### 5.2 Search loop

Robot:

- Navigates to the waypoint using its own stack
- Streams new pose + images
- Calls search_next periodically

SeekSense AI:

- Updates the semantic frontier map with new observations
- Chooses the next promising waypoint (or decides the current waypoint is still best)
- Returns updated waypoints until termination conditions are met

### 5.3 Verification and approach

Once the system is confident the target is visible:

- search_verify is called
- SeekSense AI confirms the match and computes a safe approach pose (e.g. stop 1–2 metres away, with a good viewing angle)
- Robot navigates to that pose

### 5.4 Checkpoint and logging

Session data is stored for:

- Debugging
- Performance analysis
- Future features (e.g. semantic memory / “where was it last seen?”)

---

## 6. Semantic search session lifecycle (pseudocode)

The core loop that a robot runs against SeekSense AI can be expressed as:

```python
# Pseudocode for a single semantic search task

# 1) Start a new semantic search session
session = seek.search_start({
    "target": "cleaning trolley near ward C",
    "pose": robot.pose(),
    "camera": rgbd.frame(),          # or RGB + camera model
})

# 2) Main search loop
while not session.done:
    # Ask SeekSense where to go next
    waypoint = seek.search_next(session)

    # Send waypoint to navigation stack (e.g. Nav2)
    nav.go_to(waypoint)

    # While the robot is moving, stream observations back to SeekSense
    while nav.is_moving():
        seek.update_observation(session, {
            "pose": robot.pose(),
            "camera": rgbd.frame(),
        })

        if seek.target_visible(session):
            break

    # If target is visible / likely found, break and verify
    if seek.target_visible(session):
        break

# 3) Verification and safe approach
result = seek.search_verify(session)
if result.found:
    nav.go_to(result.approach_pose)
else:
    # Optional: handle “not found” case with clear explanation
    log.info("Target not found after semantic search.")
