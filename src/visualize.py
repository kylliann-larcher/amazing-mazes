# src/visualize.py
from __future__ import annotations
import os, time
from typing import List

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def grid_to_str(grid: List[List[str]]) -> str:
    return "\n".join("".join(row) for row in grid)

def show(grid: List[List[str]], delay_ms: int = 25, title: str = ""):
    clear()
    if title:
        print(title)
    print(grid_to_str(grid))
    time.sleep(max(0, delay_ms) / 1000.0)

class ConsoleAnimator:
    """Petit helper pour passer comme callback à nos algos."""
    def __init__(self, delay_ms: int = 25, title: str = ""):
        self.delay_ms = delay_ms
        self.title = title

    def __call__(self, grid: List[List[str]]):
        show(grid, self.delay_ms, self.title)
