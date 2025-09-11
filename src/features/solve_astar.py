# Solveur de labyrinthe avec A* (AStar)
from __future__ import annotations
import heapq
from typing import Tuple, List, Dict, Optional
from utils import Maze

Coord = Tuple[int, int]

class AStarSolver:
    """
    Solveur A* (AStar) avec heuristique de Manhattan.
    - 'o' = chemin solution
    - '*' = explorations non retenues
    """

    def __init__(self):
        pass

    def heuristic(self, a: Coord, b: Coord) -> int:
        # Distance de Manhattan
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def solve(self, maze: Maze) -> Maze:
        H, W = maze.ascii_height, maze.ascii_width
        start = (0, 1)
        goal = (H - 1, W - 2)

        grid = [row[:] for row in maze.grid]

        # file de priorité (f, g, coord)
        open_set: List[Tuple[int, int, Coord]] = []
        heapq.heappush(open_set, (0, 0, start))

        came_from: Dict[Coord, Optional[Coord]] = {start: None}
        g_score: Dict[Coord, int] = {start: 0}

        while open_set:
            _, g, current = heapq.heappop(open_set)

            if current == goal:
                break

            r, c = current
            for dr, dc in [(1,0),(-1,0),(0,1),(0,-1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < H and 0 <= nc < W and grid[nr][nc] == ".":
                    tentative_g = g + 1
                    if tentative_g < g_score.get((nr, nc), float("inf")):
                        g_score[(nr, nc)] = tentative_g
                        f = tentative_g + self.heuristic((nr, nc), goal)
                        heapq.heappush(open_set, (f, tentative_g, (nr, nc)))
                        came_from[(nr, nc)] = current
                        # Marquer exploré
                        if (nr, nc) != goal:
                            grid[nr][nc] = "*"

        # Reconstruire chemin
        node = goal
        while node in came_from and node is not None:
            r, c = node
            grid[r][c] = "o"
            node = came_from[node]

        # Remettre entrée/sortie praticables
        grid[start[0]][start[1]] = "o"
        grid[goal[0]][goal[1]] = "o"

        return Maze(grid)
