from features.gen_backtrack import BacktrackingGenerator
from features.solve_astar import AStarSolver

def test_astar_finds_path():
    n = 5
    maze = BacktrackingGenerator(n, seed=123).generate()
    solved = AStarSolver().solve(maze)
    assert solved.grid[0][1] == "o"
    assert solved.grid[2*n][2*n-1] == "o"
    # Il doit exister au moins un 'o'
    assert any(ch == "o" for row in solved.grid for ch in row)
