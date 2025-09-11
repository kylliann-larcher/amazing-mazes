# tests/test_kruskal.py
from features.gen_kruskal import KruskalGenerator

def test_kruskal_basic():
    n = 5
    gen = KruskalGenerator(n, seed=42)
    maze = gen.generate()
    H = W = 2 * n + 1
    assert len(maze.grid) == H
    assert all(len(row) == W for row in maze.grid)
    # Entrée/sortie ouvertes
    assert maze.grid[0][1] == "."
    assert maze.grid[2*n][2*n-1] == "."
    # chaque cellule logique doit être un couloir
    for r in range(n):
        for c in range(n):
            ar, ac = 2*r + 1, 2*c + 1
            assert maze.grid[ar][ac] == "."
