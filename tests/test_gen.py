# Tests unitaires pour les générateurs
from features.gen_backtrack import BacktrackingGenerator

def test_ascii_size_and_cells():
    n = 5
    gen = BacktrackingGenerator(n, seed=123)
    maze = gen.generate()
    H = W = 2*n + 1
    assert maze.ascii_height == H
    assert maze.ascii_width == W
    allowed = {"#", ".", "o", "*"}
    assert all(ch in allowed for row in maze.grid for ch in row)
    # Entrée/Sortie ouvertes
    assert maze.grid[0][1] == "."
    assert maze.grid[2*n][2*n-1] == "."

