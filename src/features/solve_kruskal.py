from __future__ import annotations
import random
from typing import Tuple, List, Optional, Dict, Set
from utils import Maze

Coord = Tuple[int, int]

class DisjointSet:
    def __init__(self, elements: List[Coord]):
        # Initialisation Union-Find
        self.parent = {e: e for e in elements}
        self.rank = {e: 0 for e in elements}

    def find(self, x: Coord) -> Coord:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: Coord, b: Coord) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        # Union by rank
        if self.rank[ra] < self.rank[rb]:
            self.parent[ra] = rb
        elif self.rank[ra] > self.rank[rb]:
            self.parent[rb] = ra
        else:
            self.parent[rb] = ra
            self.rank[ra] += 1
        return True

class KruskalSolver:
    """
    Solveur basé sur Kruskal:
    1) construit un arbre couvrant (Kruskal) sur les cases '.' adjacentes,
    2) cherche un chemin dans cet arbre (DFS),
    - marque 'o' pour le chemin final
    - marque '*' pour les cases explorées mais non retenues
    """

    def __init__(self, seed: Optional[int] = None):
        self.seed = seed

    def solve(self, maze: Maze) -> Maze:
        if self.seed is not None:
            random.seed(self.seed)

        H, W = maze.ascii_height, maze.ascii_width
        start: Coord = (0, 1)
        goal:  Coord = (H - 1, W - 2)

        # Copie de la grille
        grid = [row[:] for row in maze.grid]

        # 1) Construire la liste des noeuds (cases '.') et des arêtes entre voisins '.' (droite/bas)
        nodes: List[Coord] = [(r, c) for r in range(H) for c in range(W) if grid[r][c] == "."]
        node_set: Set[Coord] = set(nodes)

        # Si l'entrée/sortie ne sont pas marquées comme praticables (cas de certains formats), on les ajoute si possible
        if 0 <= start[0] < H and 0 <= start[1] < W and grid[start[0]][start[1]] == ".":
            node_set.add(start)
        if 0 <= goal[0] < H and 0 <= goal[1] < W and grid[goal[0]][goal[1]] == ".":
            node_set.add(goal)

        nodes = list(node_set)

        # Construire la liste des arêtes (poids aléatoires pour Kruskal)
        edges: List[Tuple[float, Coord, Coord]] = []
        for r, c in nodes:
            # voisin droite
            if c + 1 < W and (r, c + 1) in node_set:
                edges.append((random.random(), (r, c), (r, c + 1)))
            # voisin bas
            if r + 1 < H and (r + 1, c) in node_set:
                edges.append((random.random(), (r, c), (r + 1, c)))

        # 2) Kruskal: trier les arêtes par poids et construire l'arbre couvrant (forêt si composantes multiples)
        edges.sort(key=lambda e: e[0])
        ds = DisjointSet(nodes)

        # Adjacence de l'arbre couvrant
        tree_adj: Dict[Coord, List[Coord]] = {v: [] for v in nodes}

        for _, a, b in edges:
            if ds.union(a, b):
                tree_adj[a].append(b)
                tree_adj[b].append(a)

        # 3) DFS dans l'arbre (uniquement via tree_adj), avec marquage '*' pour exploré et 'o' pour le chemin final
        visited: Set[Coord] = set()
        path: List[Coord] = []

        def dfs(r: int, c: int) -> bool:
            visited.add((r, c))
            if (r, c) != start and (r, c) in node_set:
                grid[r][c] = "*"  # marquer exploré (écrasé plus tard par 'o' si sur le chemin)

            if (r, c) == goal:
                path.append((r, c))
                return True

            # Explorer voisins dans un ordre fixe pour la reproductibilité visuelle
            dir_order = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            for dr, dc in dir_order:
                nr, nc = r + dr, c + dc
                nb = (nr, nc)
                if nb in tree_adj.get((r, c), []) and nb not in visited:
                    if dfs(nr, nc):
                        path.append((r, c))
                        return True
            return False

        # Lancer depuis l'entrée si elle est dans le graphe, sinon aucun chemin ne sera trouvé
        if start in tree_adj:
            dfs(*start)
        else:
            # Marquage minimal si l'entrée n'est pas une case praticable '.'
            pass

        # 4) Marquer le chemin final en 'o'
        for r, c in path:
            grid[r][c] = "o"
        # Préserver entrée/sortie praticables
        if 0 <= start[0] < H and 0 <= start[1] < W:
            grid[start[0]][start[1]] = "o"
        if 0 <= goal[0] < H and 0 <= goal[1] < W:
            grid[goal[0]][goal[1]] = "o"

        return Maze(grid)
