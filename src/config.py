# src/config.py
from pathlib import Path

# racine du projet (le dossier qui contient src/)
ROOT = Path(__file__).resolve().parent.parent

# dossier data central
DATA_DIR = ROOT / "data"

# sorties catégorisées
MAZES_DIR = DATA_DIR / "outputs" / "mazes"
SOLUTIONS_DIR = DATA_DIR / "outputs" / "solutions"
IMAGES_DIR = DATA_DIR / "outputs" / "images"

# s'assurer que les dossiers existent
for p in (MAZES_DIR, SOLUTIONS_DIR, IMAGES_DIR):
    p.mkdir(parents=True, exist_ok=True)
