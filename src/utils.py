# src/utils.py
from __future__ import annotations
from typing import List
from pathlib import Path
from config import MAZES_DIR, SOLUTIONS_DIR


class Maze:
    """
    Représentation ASCII d’un labyrinthe.
    Chaque cellule est un caractère dans une matrice (list[list[str]]).
    """

    def __init__(self, grid: List[List[str]]):
        self.grid = grid

    @classmethod
    def empty_from_n(cls, n: int) -> "Maze":
        """
        Construit une grille vide de taille (2n+1)x(2n+1) pleine de murs '#'
        et avec des cellules '.' aux positions impaires.
        """
        H = W = 2 * n + 1
        grid = [["#" for _ in range(W)] for _ in range(H)]
        for r in range(1, H, 2):
            for c in range(1, W, 2):
                grid[r][c] = "."
        return cls(grid)

    @property
    def ascii_height(self) -> int:
        return len(self.grid)

    @property
    def ascii_width(self) -> int:
        return len(self.grid[0]) if self.grid else 0

    def copy(self) -> "Maze":
        return Maze([row[:] for row in self.grid])

    def save_txt(self, filename: str | None = None) -> str:
        """
        Sauvegarde la grille dans un fichier .txt.
        - Si filename est None ou vide : data/outputs/mazes/maze_auto.txt
        - Si filename est juste un nom (sans dossier), on le place dans data/outputs/mazes
        Retourne le chemin complet du fichier sauvegardé.
        """
        if not filename:
            filename = MAZES_DIR / "maze_auto.txt"
        else:
            filename = Path(filename)
            if filename.parent == Path("."):
                filename = MAZES_DIR / filename.name

        # forcer extension .txt si absente
        if filename.suffix.lower() != ".txt":
            filename = filename.with_suffix(".txt")

        filename.parent.mkdir(parents=True, exist_ok=True)
        with open(filename, "w", encoding="utf-8") as f:
            for row in self.grid:
                f.write("".join(row) + "\n")
        return str(filename)

    @classmethod
    def load_txt(cls, filename: str) -> "Maze":
        """
        Charge un fichier .txt représentant un labyrinthe.
        - accepte chemin absolu/relatif complet
        - accepte un nom simple cherché dans data/outputs/mazes puis data/outputs/solutions
        - accepte fichiers sans extension si présents
        """
        path = Path(filename)

        # cas 1 : existe tel quel
        if path.exists():
            real = path
        else:
            # préparer variantes de noms (avec et sans .txt)
            names_to_try = [path.name] if path.suffix else [
                path.with_suffix(".txt").name,
                path.name,
            ]

            found = None
            # chercher dans mazes
            for nm in names_to_try:
                cand = MAZES_DIR / nm
                if cand.exists():
                    found = cand
                    break
            # chercher dans solutions
            if not found:
                for nm in names_to_try:
                    cand = SOLUTIONS_DIR / nm
                    if cand.exists():
                        found = cand
                        break
            # chercher dans cwd
            if not found:
                for nm in names_to_try:
                    cand = Path.cwd() / nm
                    if cand.exists():
                        found = cand
                        break

            if not found:
                raise FileNotFoundError(
                    f"Fichier introuvable: {filename}. "
                    f"Cherché dans {MAZES_DIR} et {SOLUTIONS_DIR}."
                )
            real = found

        with open(real, "r", encoding="utf-8") as f:
            lines = [list(line.rstrip("\n")) for line in f]
        return cls(lines)


# ----------------------------------------------------------------------
# Utilitaire pour résoudre un nom de fichier (maze ou solution)
# ----------------------------------------------------------------------
def resolve_maze_file(name: str | None) -> str | None:
    """
    Résout un nom de fichier donné en recherchant dans MAZES_DIR puis SOLUTIONS_DIR.
    - accepte 'maze_30' ou 'maze_30.txt' ou un chemin absolu/relatif.
    - accepte aussi fichiers sans extension physiquement présents (ex: 'maze_30_s').
    - retourne le chemin complet (string) si trouvé, sinon None.
    """
    if not name:
        return None

    p = Path(name)

    # s'il existe tel quel (avec ou sans extension)
    if p.exists():
        return str(p)

    # variantes de noms
    names_to_try = [p.name] if p.suffix else [
        p.with_suffix(".txt").name,
        p.name,
    ]

    # chercher dans mazes
    for nm in names_to_try:
        cand = MAZES_DIR / nm
        if cand.exists():
            return str(cand)

    # chercher dans solutions
    for nm in names_to_try:
        cand = SOLUTIONS_DIR / nm
        if cand.exists():
            return str(cand)

    # chercher dans cwd
    for nm in names_to_try:
        cand = Path.cwd() / nm
        if cand.exists():
            return str(cand)

    return None
