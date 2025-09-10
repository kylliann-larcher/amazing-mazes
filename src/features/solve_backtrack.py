# Solveur de labyrinthe avec Backtracking
from __future__ import annotations
from typing import Tuple, List, Optional
from utils import Maze

Coord = Tuple[int, int]

class BacktrackingSolver:
    """
    Solveur DFS (backtracking).
    - marque 'o' pour le chemin final
    - marque '*' pour les cases explorées mais non retenues
    """

    def __init__(self):
        pass

    def solve(self, maze: Maze) -> Maze:
        H, W = maze.ascii_height, maze.ascii_width
        start = (0, 1)              # entrée
        goal  = (H - 1, W - 2)      # sortie

        grid = [row[:] for row in maze.grid]  # travail sur une copie

        def neighbors(r: int, c: int):
            for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < H and 0 <= nc < W and grid[nr][nc] in (".",):
                    yield nr, nc

        visited = [[False]*W for _ in range(H)]
        path: List[Coord] = []

        def dfs(r: int, c: int) -> bool:
            if (r, c) == goal:
                path.append((r, c))
                return True
            visited[r][c] = True
            # Marquer exploré sauf si c'est l'entrée
            if (r, c) != start:
                grid[r][c] = "*"
            for nr, nc in neighbors(r, c):
                if not visited[nr][nc]:
                    if dfs(nr, nc):
                        path.append((r, c))
                        return True
            return False

        dfs(*start)

        # Marquer le chemin final en 'o'
        for r, c in path:
            grid[r][c] = "o"
        # Garder entrée/sortie praticables
        grid[start[0]][start[1]] = "o"
        grid[goal[0]][goal[1]] = "o"

        return Maze(grid)
