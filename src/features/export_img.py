# src/features/export_img.py
from __future__ import annotations
from typing import List
from PIL import Image
from pathlib import Path
import os
from config import IMAGES_DIR
from utils import Maze

# mapping char -> RGB
COLOR_MAP = {
    "#": (0, 0, 0),        # wall -> black
    ".": (255, 255, 255),  # corridor -> white
    "o": (220, 20, 60),    # path -> crimson/red
    "*": (200, 200, 200),  # explored -> light gray
}

class AsciiExporter:
    """
    Convertit une grille ASCII Maze en image PNG.
    - cell_size: taille en pixels d'une cellule (ex: 8, 10)
    - background_color: couleur de fond si caractère inconnu
    """

    def __init__(self, cell_size: int = 10, background_color: tuple[int,int,int] | None = None):
        self.cell_size = max(1, int(cell_size))
        self.background_color = background_color or (255, 0, 255)  # magenta for unknown

    def export(self, maze: Maze, filename: str | Path | None = None) -> str:
        """
        Exporte la grille Maze en PNG.
        - filename: chemin souhaité (str ou Path). Si None ou vide, on utilisera IMAGES_DIR/maze_auto.png
        - Si l'extension est manquante, on ajoute automatiquement .png
        - Retourne le chemin du fichier exporté (string)
        """
        # Prépare le nom de fichier
        if not filename:
            dest = IMAGES_DIR / "maze_auto.png"
        else:
            dest = Path(filename)
            # si l'utilisateur a donné juste un nom (pas de dossier), placer dans IMAGES_DIR
            if dest.parent == Path("."):
                dest = IMAGES_DIR / dest.name

        # Si aucune extension, forcer .png
        if not dest.suffix:
            dest = dest.with_suffix(".png")
        # Si l'extension n'est pas reconnue par Pillow, normaliser vers .png
        if dest.suffix.lower() not in (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff"):
            dest = dest.with_suffix(".png")

        # Créer dossier si besoin
        dest.parent.mkdir(parents=True, exist_ok=True)

        grid: List[List[str]] = maze.grid
        h = len(grid)
        w = len(grid[0]) if h > 0 else 0
        if h == 0 or w == 0:
            raise ValueError("La grille est vide, impossible d'exporter l'image.")

        img_h = h * self.cell_size
        img_w = w * self.cell_size

        # Crée l'image
        img = Image.new("RGB", (img_w, img_h), (0, 0, 0))
        pixels = img.load()

        for r in range(h):
            for c in range(w):
                ch = grid[r][c]
                color = COLOR_MAP.get(ch, self.background_color)
                top = r * self.cell_size
                left = c * self.cell_size
                for y in range(top, top + self.cell_size):
                    for x in range(left, left + self.cell_size):
                        pixels[x, y] = color

        # Sauvegarde en PNG (on force format PNG via suffix)
        img.save(str(dest))
        return str(dest)
