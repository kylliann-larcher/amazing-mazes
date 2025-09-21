# tests/conftest.py
import os
import sys

# Ajoute le dossier "src" au PYTHONPATH pour que "features" soit importable
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)
