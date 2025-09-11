# Fonctions utilitaires (I/O fichiers, affichage ASCII)
from __future__ import annotations
from typing import List
import os
from pathlib import Path
from config import MAZES_DIR

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

    def save_txt(self, filename: str | None = None) -> str:
        """
        Sauvegarde la grille en .txt.
        Si filename est None ou vide, on crée un fichier dans data/outputs/mazes.
        Retourne le chemin complet du fichier sauvegardé (string).
        """
        # filename par défaut
        if not filename:
            filename = MAZES_DIR / "maze_auto.txt"
        filename = Path(filename)
        # si le chemin est relatif et n'a pas de dossier, l'interpréter dans MAZES_DIR
        if filename.parent == Path("."):
            filename = MAZES_DIR / filename.name

        # créer dossier parent si besoin
        filename.parent.mkdir(parents=True, exist_ok=True)
        with open(filename, "w", encoding="utf-8") as f:
            for row in self.grid:
                f.write("".join(row) + "\n")
        return str(filename)

    @classmethod
    
    def load_txt(cls, filename: str) -> "Maze":
        path = Path(filename)
        # accepter les chemins simples (nom de fichier) en cherchant dans MAZES_DIR
        if not path.exists():
            alt = MAZES_DIR / path.name
            if alt.exists():
                path = alt
        if not path.exists():
            raise FileNotFoundError(f"Fichier introuvable: {filename}")
        with open(path, "r", encoding="utf-8") as f:
            lines = [list(line.rstrip("\n")) for line in f]
        return cls(lines)

    def copy(self) -> "Maze":
        return Maze([row[:] for row in self.grid])
