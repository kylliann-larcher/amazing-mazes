# Générateur de labyrinthe avec Backtracking
from __future__ import annotations
import random
from typing import Tuple, List
from utils import Maze
import sys
sys.setrecursionlimit(10000)  # ou 20000 selon la taille ; attention aux risques

Cell = Tuple[int, int]

def _neighbors(cell: Cell, n: int) -> List[Cell]:
    r, c = cell
    cand = []
    if r > 0:       cand.append((r - 1, c))
    if r < n - 1:   cand.append((r + 1, c))
    if c > 0:       cand.append((r, c - 1))
    if c < n - 1:   cand.append((r, c + 1))
    random.shuffle(cand)
    return cand

def _to_ascii(cell: Cell) -> Cell:
    r, c = cell
    return 2 * r + 1, 2 * c + 1

class BacktrackingGenerator:
    """Génère un labyrinthe parfait par DFS backtracking."""

    def __init__(self, n: int, seed: int | None = None):
        if n < 1:
            raise ValueError("n doit être >= 1")
        self.n = n
        self.seed = seed

    def generate(self) -> Maze:
        if self.seed is not None:
            random.seed(self.seed)

        n = self.n
        maze = Maze.empty_from_n(n)
        visited = [[False] * n for _ in range(n)]

        def carve(curr: Cell):
            visited[curr[0]][curr[1]] = True
            for nb in _neighbors(curr, n):
                if not visited[nb[0]][nb[1]]:
                    cr, cc = _to_ascii(curr)
                    nr, nc = _to_ascii(nb)
                    wall_r, wall_c = (cr + nr) // 2, (cc + nc) // 2
                    maze.grid[wall_r][wall_c] = "."
                    carve(nb)

        carve((0, 0))
        return maze
