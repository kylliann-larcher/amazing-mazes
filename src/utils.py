# Fonctions utilitaires (I/O fichiers, affichage ASCII)
from __future__ import annotations
from typing import List
import os

class Maze:
    """
    Représente un labyrinthe ASCII :
      - '#' = mur
      - '.' = couloir
      - 'o' = chemin solution
      - '*' = exploré mais non retenu
    Taille logique n => grille ASCII (2*n+1) x (2*n+1)
    Entrée = (0,1), Sortie = (2*n, 2*n-1)
    """
    def __init__(self, grid: List[List[str]]):
        self.grid = grid

    @classmethod
    def empty_from_n(cls, n: int) -> "Maze":
        H = W = 2 * n + 1
        grid = [["#" for _ in range(W)] for _ in range(H)]
        # Place les cellules (couloirs) aux coordonnées impaires
        for r in range(n):
            for c in range(n):
                ar, ac = 2 * r + 1, 2 * c + 1
                grid[ar][ac] = "."
        # Entrée/Sortie
        grid[0][1] = "."
        grid[2 * n][2 * n - 1] = "."
        return cls(grid)

    @property
    def ascii_height(self) -> int:
        return len(self.grid)

    @property
    def ascii_width(self) -> int:
        return len(self.grid[0]) if self.grid else 0

    def save_txt(self, filename: str) -> None:
        #créer dossier si nécessaire
        os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
        with open(filename, "w", encoding="utf-8") as f:
            for row in self.grid:
                f.write("".join(row) + "\n")

    @classmethod
    def load_txt(cls, filename: str) -> "Maze":
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Fichier introuvable: {filename}. "
                "Assure-toi d'avoir généré un labyrinthe (option 1) ou de donner un chemin valide.")
        with open(filename, "r", encoding="utf-8") as f:
            lines = [list(line.rstrip("\n")) for line in f]
        return cls(lines)

    def copy(self) -> "Maze":
        return Maze([row[:] for row in self.grid])
