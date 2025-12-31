# VLFM pipeline breakdown (engineering view)

VLFM is not a single model; it is a pipeline:

1) **Geometry / exploration**
   - Build a 2D occupancy grid from depth + pose.
   - Extract **frontiers**: free cells adjacent to unknown.
   - Cluster frontiers and compute candidate waypoints.

2) **Vision-language value map**
   - Score RGB observations against a text prompt (target object).
   - Project per-view scores into a top-down **value map** and maintain a **confidence map**.
   - Update via weighted fusion where observations overlap.

3) **Frontier ranking**
   - Evaluate frontier clusters using value-map statistics near each cluster.
   - Select best frontier waypoint.

4) **Navigation controller**
   - Navigate to the selected waypoint via a PointNav controller / stack.
   - Repeat until target detection triggers final goal.

This repository implements Stage (1) + (3) and the interface for (2).
