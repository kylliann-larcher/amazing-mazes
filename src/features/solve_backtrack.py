# src/features/solve_backtrack.py
from __future__ import annotations
from typing import Tuple, List, Dict, Optional, Callable
from utils import Maze

Coord = Tuple[int, int]
OnStep = Optional[Callable[[List[List[str]]], None]]

class BacktrackingSolver:
    """DFS itératif – callbacks on_visit/on_path pour l'animation."""
    def __init__(self):
        pass

    def solve(self, maze: Maze,
              on_visit: OnStep = None,
              on_path: OnStep = None) -> Maze:
        H, W = maze.ascii_height, maze.ascii_width
        start: Coord = (0, 1)
        goal:  Coord = (H - 1, W - 2)
        grid = [row[:] for row in maze.grid]

        def neighbors(r: int, c: int):
            for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < H and 0 <= nc < W and grid[nr][nc] == ".":
                    yield nr, nc

        visited = [[False]*W for _ in range(H)]
        parent: Dict[Coord, Optional[Coord]] = {start: None}
        stack: List[Coord] = [start]
        visited[start[0]][start[1]] = True

        found = False
        while stack:
            r, c = stack.pop()
            if (r, c) == goal:
                found = True
                break
            if (r, c) != start and grid[r][c] == ".":
                grid[r][c] = "*"
                if on_visit: on_visit(grid)  # <-- animation exploration

            for nr, nc in neighbors(r, c):
                if not visited[nr][nc]:
                    visited[nr][nc] = True
                    parent[(nr, nc)] = (r, c)
                    stack.append((nr, nc))

        if not found:
            return Maze(grid)

        node: Optional[Coord] = goal
        while node is not None:
            rr, cc = node
            grid[rr][cc] = "o"
            if on_path: on_path(grid)       # <-- animation “chemin final”
            node = parent.get(node)

        grid[start[0]][start[1]] = "o"
        grid[goal[0]][goal[1]] = "o"
        if on_path: on_path(grid)
        return Maze(grid)
