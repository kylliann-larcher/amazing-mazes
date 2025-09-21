# Tests unitaires pour les solveurs
from features.gen_backtrack import BacktrackingGenerator
from features.solve_backtrack import BacktrackingSolver

def test_solver_marks_path():
    n = 5
    maze = BacktrackingGenerator(n, seed=42).generate()
    solved = BacktrackingSolver().solve(maze)
    # Entrée/sortie doivent être marquées 'o'
    assert solved.grid[0][1] == "o"
    assert solved.grid[2*n][2*n-1] == "o"
    # Il doit exister au moins un 'o' entre les deux
    inner_o = sum(ch == "o" for row in solved.grid for ch in row)
    assert inner_o >= 2
