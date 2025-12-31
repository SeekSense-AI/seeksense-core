from __future__ import annotations

from dataclasses import dataclass
import numpy as np

# Convention:
#   -1 = unknown
#    0 = free
#    1 = occupied

@dataclass
class OccupancyGrid:
    """Simple 2D occupancy grid.

    Attributes:
        grid: int8 array of shape (H, W) with values in {-1,0,1}.
        resolution: meters per cell.
        origin_xy: world (x,y) of grid cell (0,0) lower-left corner.
    """
    grid: np.ndarray
    resolution: float = 0.05
    origin_xy: tuple[float, float] = (0.0, 0.0)

    def __post_init__(self) -> None:
        if not isinstance(self.grid, np.ndarray):
            raise TypeError("grid must be a numpy array")
        if self.grid.ndim != 2:
            raise ValueError("grid must be 2D (H,W)")
        if self.grid.dtype != np.int8:
            self.grid = self.grid.astype(np.int8, copy=False)

    @property
    def shape(self) -> tuple[int, int]:
        return self.grid.shape

    def in_bounds(self, r: int, c: int) -> bool:
        h, w = self.grid.shape
        return 0 <= r < h and 0 <= c < w

    def neighbors(self, r: int, c: int, connectivity: int = 4) -> list[tuple[int, int]]:
        if connectivity not in (4, 8):
            raise ValueError("connectivity must be 4 or 8")
        deltas = [(-1,0),(1,0),(0,-1),(0,1)]
        if connectivity == 8:
            deltas += [(-1,-1),(-1,1),(1,-1),(1,1)]
        out = []
        for dr, dc in deltas:
            rr, cc = r + dr, c + dc
            if self.in_bounds(rr, cc):
                out.append((rr, cc))
        return out

    def world_xy(self, r: int, c: int) -> tuple[float, float]:
        """World (x,y) at the center of cell (r,c)."""
        ox, oy = self.origin_xy
        x = ox + (c + 0.5) * self.resolution
        y = oy + (r + 0.5) * self.resolution
        return (x, y)
