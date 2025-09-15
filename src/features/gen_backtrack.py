# src/features/gen_backtrack.py
from __future__ import annotations
import random
from typing import List, Tuple, Callable, Optional
from utils import Maze

Cell = Tuple[int, int]
OnStep = Optional[Callable[[List[List[str]]], None]]

def _neighbors(cell: Cell, n: int) -> List[Cell]:
    r, c = cell
    neigh = []
    if r > 0: neigh.append((r - 1, c))
    if r < n - 1: neigh.append((r + 1, c))
    if c > 0: neigh.append((r, c - 1))
    if c < n - 1: neigh.append((r, c + 1))
    random.shuffle(neigh)
    return neigh

def _to_ascii(cell: Cell) -> Cell:
    r, c = cell
    return 2 * r + 1, 2 * c + 1

class BacktrackingGenerator:
    """DFS backtracking itératif (pile) — avec callback on_step facultatif."""
    def __init__(self, n: int, seed: int | None = None):
        if n < 1:
            raise ValueError("n doit être >= 1")
        self.n = n
        self.seed = seed

    def generate(self, on_step: OnStep = None) -> Maze:
        if self.seed is not None:
            random.seed(self.seed)

        n = self.n
        maze = Maze.empty_from_n(n)
        visited = [[False] * n for _ in range(n)]

        start = (0, 0)
        stack: List[Cell] = [start]
        visited[start[0]][start[1]] = True

        while stack:
            curr = stack[-1]
            unvisited = [nb for nb in _neighbors(curr, n) if not visited[nb[0]][nb[1]]]
            if unvisited:
                nb = unvisited[0]
                cr, cc = _to_ascii(curr)
                nr, nc = _to_ascii(nb)
                wall_r = (cr + nr) // 2
                wall_c = (cc + nc) // 2
                maze.grid[wall_r][wall_c] = "."
                if on_step: on_step(maze.grid)  # <-- callback visuel
                visited[nb[0]][nb[1]] = True
                stack.append(nb)
            else:
                stack.pop()

        maze.grid[0][1] = "."
        maze.grid[2 * n][2 * n - 1] = "."
        if on_step: on_step(maze.grid)
        return maze
