# src/features/gen_kruskal.py
from __future__ import annotations
import random
from typing import Tuple, List, Callable, Optional
from utils import Maze

Cell = Tuple[int, int]
OnStep = Optional[Callable[[List[List[str]]], None]]

class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb: return False
        if self.rank[ra] < self.rank[rb]:
            self.parent[ra] = rb
        elif self.rank[ra] > self.rank[rb]:
            self.parent[rb] = ra
        else:
            self.parent[rb] = ra
            self.rank[ra] += 1
        return True

class KruskalGenerator:
    def __init__(self, n: int, seed: int | None = None):
        if n < 1:
            raise ValueError("n doit être >= 1")
        self.n = n
        self.seed = seed

    def _cell_index(self, r: int, c: int) -> int:
        return r * self.n + c

    def generate(self, on_step: OnStep = None) -> Maze:
        if self.seed is not None:
            random.seed(self.seed)
        n = self.n
        maze = Maze.empty_from_n(n)

        edges: List[Tuple[Tuple[int,int], Tuple[int,int]]] = []
        for r in range(n):
            for c in range(n):
                if r + 1 < n: edges.append(((r, c), (r + 1, c)))
                if c + 1 < n: edges.append(((r, c), (r, c + 1)))
        random.shuffle(edges)
        uf = UnionFind(n * n)

        for a, b in edges:
            ai = self._cell_index(a[0], a[1])
            bi = self._cell_index(b[0], b[1])
            if uf.union(ai, bi):
                ar, ac = 2 * a[0] + 1, 2 * a[1] + 1
                br, bc = 2 * b[0] + 1, 2 * b[1] + 1
                wall_r, wall_c = (ar + br) // 2, (ac + bc) // 2
                maze.grid[wall_r][wall_c] = "."
                if on_step: on_step(maze.grid)  # <-- callback visuel

        maze.grid[0][1] = "."
        maze.grid[2 * n][2 * n - 1] = "."
        if on_step: on_step(maze.grid)
        return maze
