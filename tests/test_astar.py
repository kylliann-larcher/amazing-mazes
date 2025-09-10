from features.gen_backtrack import BacktrackingGenerator
from features.solve_astar import AStarSolver

def test_astar_finds_path():
    n = 5
    maze = BacktrackingGenerator(n, seed=123).generate()
    solved = AStarSolver().solve(maze)
    # Entrée et sortie doivent être marquées 'o'
    assert solved.grid[0][1] == "o"
    assert solved.grid[2*n][2*n-1] == "o"
    # Chemin trouvé
    assert any("o" in row for row in solved.grid)
