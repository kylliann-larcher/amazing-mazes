# Générateur de labyrinthe avec Kruskal (bonus)
from __future__ import annotations
import random
from typing import Tuple, List
from utils import Maze

Cell = Tuple[int, int]

class DisjointSet:
    def __init__(self, n: int):
        self.parent = {(r, c): (r, c) for r in range(n) for c in range(n)}

    def find(self, cell: Cell) -> Cell:
        if self.parent[cell] != cell:
            self.parent[cell] = self.find(self.parent[cell])
        return self.parent[cell]

    def union(self, a: Cell, b: Cell):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra

def _to_ascii(cell: Cell) -> Cell:
    r, c = cell
    return 2 * r + 1, 2 * c + 1

class KruskalGenerator:
    """Génère un labyrinthe parfait par l’algorithme de Kruskal."""

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
        ds = DisjointSet(n)

        # Liste des murs entre cellules adjacentes
        walls = []
        for r in range(n):
            for c in range(n):
                if r < n - 1:
                    walls.append(((r, c), (r + 1, c)))
                if c < n - 1:
                    walls.append(((r, c), (r, c + 1)))
        random.shuffle(walls)

        for cell1, cell2 in walls:
            if ds.find(cell1) != ds.find(cell2):
                # Enlève le mur entre cell1 et cell2
                cr1, cc1 = _to_ascii(cell1)
                cr2, cc2 = _to_ascii(cell2)
                wall_r, wall_c = (cr1 + cr2) // 2, (cc1 + cc2) // 2
                maze.grid[wall_r][wall_c] = "."
                ds.union(cell1, cell2)

        return maze
