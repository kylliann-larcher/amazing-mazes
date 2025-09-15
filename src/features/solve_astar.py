# src/features/solve_astar.py
from __future__ import annotations
from typing import Tuple, List, Dict, Optional, Callable
import heapq
from utils import Maze

Coord = Tuple[int, int]
OnStep = Optional[Callable[[List[List[str]]], None]]

class AStarSolver:
    """
    Solveur A* (A-star) pour trouver le chemin le plus court.
    - Marque 'o' = chemin final
    - Marque '*' = cases explorées
    """

    def __init__(self):
        pass

    def heuristic(self, a: Coord, b: Coord) -> int:
        """Heuristique de Manhattan"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

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

        open_set: List[Tuple[int, Coord]] = []
        heapq.heappush(open_set, (0, start))

        came_from: Dict[Coord, Optional[Coord]] = {start: None}
        g_score: Dict[Coord, int] = {start: 0}

        visited = set()

        while open_set:
            _, current = heapq.heappop(open_set)
            if current in visited:
                continue
            visited.add(current)

            r, c = current
            if current == goal:
                # reconstruire le chemin
                node: Optional[Coord] = goal
                while node is not None:
                    rr, cc = node
                    grid[rr][cc] = "o"
                    if on_path: on_path(grid)
                    node = came_from[node]
                grid[start[0]][start[1]] = "o"
                grid[goal[0]][goal[1]] = "o"
                if on_path: on_path(grid)
                return Maze(grid)

            # marquer comme exploré
            if current != start and grid[r][c] == ".":
                grid[r][c] = "*"
                if on_visit: on_visit(grid)

            for nb in neighbors(r, c):
                tentative_g = g_score[current] + 1
                if tentative_g < g_score.get(nb, 1e9):
                    came_from[nb] = current
                    g_score[nb] = tentative_g
                    f = tentative_g + self.heuristic(nb, goal)
                    heapq.heappush(open_set, (f, nb))

        # si pas de chemin trouvé
        return Maze(grid)
