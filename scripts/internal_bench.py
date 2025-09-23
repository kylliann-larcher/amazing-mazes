r"""
Benchmark interne des ALGO EXISTANTS (aucun nouveau fichier d'algo) :
- Générateurs : Backtracking, Kruskal
- Solveurs    : Backtracking (récursif si ton fichier l'est), A*
- Mesures : temps (ns), mémoire (tracemalloc + optionnel psutil RSS)
- Résilience : capture RecursionError / autres exceptions -> pas de crash
- Paramètres : --min/--max (ou --sizes), --repeats, --reclimit, --verbose

Exemples (PowerShell) :
  .venv\Scripts\activate
  python scripts\internal_bench.py --min 1 --max 200 --repeats 5 --reclimit 5000 --verbose --out data/outputs/internal_bench_1_200_r5.csv
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
import time
import tracemalloc
import csv
import statistics
import argparse
import gc

try:
    import psutil
except Exception:
    psutil = None

from features.gen_backtrack import BacktrackingGenerator
from features.gen_kruskal import KruskalGenerator
from features.solve_backtrack import BacktrackingSolver
from features.solve_astar import AStarSolver
from utils import Maze

OUT_CSV = Path("data/outputs/internal_bench.csv")
OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

# -----------------------
# Mesures
# -----------------------
def measure_fn(fn):
    import time, tracemalloc, gc
    gc.collect()
    tracemalloc.start()

    t0 = time.perf_counter_ns()
    ok, err, result = 1, None, None
    try:
        result = fn()
    except RecursionError:
        ok, err = 0, "RecursionError"
    except Exception as e:
        ok, err = 0, f"{type(e).__name__}: {e}"
    t1 = time.perf_counter_ns()

    # même si exception, on récupère le pic alloc Python
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "result": result,
        "ok": ok,
        "error": err,                       # None si OK, sinon message clair
        "time_ns": int(t1 - t0),            # temps haute résolution
        "tracemalloc_peak_bytes": int(peak),
        "rss_delta_bytes": None,            # pas de psutil ici
    }


# -----------------------
# Métriques grille
# -----------------------
def extract_maze_metrics(maze: Maze | None):
    """
    Renvoie des métriques de la grille si maze est non-null, sinon des 0.
    """
    if maze is None:
        return {
            "ascii_h": 0, "ascii_w": 0,
            "wall_count": 0, "corridor_count": 0,
            "path_length": 0, "explored_count": 0,
            "visited_count": 0, "other_count": 0,
        }
    grid = maze.grid
    h = len(grid)
    w = len(grid[0]) if h else 0
    counts = {"#": 0, ".": 0, "o": 0, "*": 0, "other": 0}
    for row in grid:
        for ch in row:
            if ch in counts:
                counts[ch] += 1
            else:
                counts["other"] += 1
    corridor_count = counts["."] + counts["o"] + counts["*"]
    return {
        "ascii_h": h,
        "ascii_w": w,
        "wall_count": counts["#"],
        "corridor_count": corridor_count,
        "path_length": counts["o"],
        "explored_count": counts["*"],
        "visited_count": counts["o"] + counts["*"],
        "other_count": counts["other"],
    }


# -----------------------
# Wrappers (utilisent les ALGO existants)
# -----------------------
def gen_backtrack_run(n: int, seed: int | None = None) -> Maze:
    return BacktrackingGenerator(n, seed=seed).generate()

def gen_kruskal_run(n: int, seed: int | None = None) -> Maze:
    return KruskalGenerator(n, seed=seed).generate()

def solve_backtrack_run(maze: Maze) -> Maze:
    return BacktrackingSolver().solve(maze)

def solve_astar_run(maze: Maze) -> Maze:
    return AStarSolver().solve(maze)


# -----------------------
# Orchestration
# -----------------------
def run_one(size: int, seed: int, repeats: int, verbose: bool = False):
    """
    Pour une taille donnée :
      - Génère 'repeats' mazes via Backtracking ET 'repeats' mazes via Kruskal
      - Résout chaque maze généré (de chaque source) avec BacktrackingSolver & A*
    Renvoie une liste de lignes (dict) pour CSV.
    """
    rows = []

    # ----- Génération : on collecte TOUTES les instances pour chaque générateur -----
    gen_sets = {
        "Backtracking": [],  # liste de Maze (ou None si fail)
        "Kruskal": []
    }

    for gen_key, gen_name, gen_fn in [
        ("backtrack", "Backtracking", gen_backtrack_run),
        ("kruskal",   "Kruskal",     gen_kruskal_run),
    ]:
        for r in range(repeats):
            if verbose:
                print(f"  [n={size} r={r+1}] Génération {gen_name} ...")
            m = measure_fn(lambda: gen_fn(size, seed + r))
            maze = m["result"] if m["ok"] else None
            metrics = extract_maze_metrics(maze)

            # Ligne "generator"
            rows.append({
                "size": size, "seed": seed + r, "role": "generator", "algo": gen_name,
                "repeat": r + 1, "ok": m["ok"], "error": m["error"],
                "time_ns": m["time_ns"],
                "tracemalloc_peak_bytes": m["tracemalloc_peak_bytes"],
                "rss_delta_bytes": m["rss_delta_bytes"],
                # Pour les lignes générateurs, on peut renseigner gen_source=algo pour cohérence/filtrage
                "gen_source": gen_name,
                **metrics,
            })

            gen_sets[gen_name].append(maze if m["ok"] else None)

    # ----- Résolution : pour chaque source de génération, chaque solveur, chaque run -----
    for gen_source_name, maze_list in gen_sets.items():
        # S'il n'y a aucune instance OK dans cette source, on passe (rien à résoudre)
        any_ok = any(mz is not None for mz in maze_list)
        if not any_ok:
            if verbose:
                print(f"  [n={size}] Pas de maze valide pour gen_source={gen_source_name} -> skip solveurs.")
            continue

        for solver_name, solver_fn in [("Backtracking", solve_backtrack_run), ("AStar", solve_astar_run)]:
            for r in range(repeats):
                if verbose:
                    print(f"  [n={size} r={r+1}] Résolution {solver_name} sur gen_source={gen_source_name} ...")

                base_maze = maze_list[r] if r < len(maze_list) else None
                if base_maze is None:
                    # run de génération a échoué → ligne solver en échec explicite
                    m = {"ok": 0, "error": "NoMazeToSolve", "time_ns": 0,
                         "tracemalloc_peak_bytes": 0, "rss_delta_bytes": None, "result": None}
                    metrics = extract_maze_metrics(None)
                else:
                    # important: .copy() pour ne pas réutiliser une grille déjà marquée
                    m = measure_fn(lambda: solver_fn(base_maze.copy()))
                    metrics = extract_maze_metrics(m["result"] if m["ok"] else None)

                rows.append({
                    "size": size, "seed": seed + r, "role": "solver", "algo": solver_name,
                    "repeat": r + 1, "ok": m["ok"], "error": m["error"],
                    "time_ns": m["time_ns"],
                    "tracemalloc_peak_bytes": m["tracemalloc_peak_bytes"],
                    "rss_delta_bytes": m["rss_delta_bytes"],
                    "gen_source": gen_source_name,   # <- NOUVELLE COLONNE CLEF
                    **metrics,
                })

    return rows



# -----------------------
# CLI & driver
# -----------------------
def parse_args():
    p = argparse.ArgumentParser(description="Internal benchmark for amazing-mazes (existing algos only)")
    # soit --sizes explicites...
    p.add_argument("--sizes", nargs="+", type=int,
                   help="Explicit sizes n to test (n x n). If omitted, uses --min..--max.")
    # ... soit un intervalle continu
    p.add_argument("--min", type=int, default=1, help="Min size n (inclusive) if --sizes not provided")
    p.add_argument("--max", type=int, default=200, help="Max size n (inclusive) if --sizes not provided")

    p.add_argument("--repeats", type=int, default=5, help="Repeats per test (default 5)")
    p.add_argument("--seed", type=int, default=1, help="Seed for RNG (base, increment per repeat)")
    p.add_argument("--reclimit", type=int, default=1000, help="sys.setrecursionlimit value")
    p.add_argument("--out", type=str, default=str(OUT_CSV), help="Output CSV path")
    p.add_argument("--verbose", action="store_true", help="Print detailed progress")
    return p.parse_args()

def main():
    args = parse_args()
    # Fixe la limite de récursion pour les ALGO récursifs existants (ex: BacktrackingSolver)
    sys.setrecursionlimit(args.reclimit)

    # Construire la liste des tailles
    sizes = args.sizes if args.sizes else list(range(args.min, args.max + 1))

    all_rows = []
    for n in sizes:
        if args.verbose:
            print(f"Running size={n} (repeats={args.repeats}) ...")
        rows = run_one(n, args.seed, args.repeats, verbose=args.verbose)
        all_rows.extend(rows)

    # write CSV
    fieldnames = [
        "size","seed","role","algo","repeat","ok","error",
        "time_ns","tracemalloc_peak_bytes","rss_delta_bytes",
        "ascii_h","ascii_w","wall_count","corridor_count",
        "path_length","explored_count","visited_count","other_count",
        "gen_source"
    ]
    outp = Path(args.out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    with outp.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in all_rows:
            writer.writerow({k: r.get(k, "") for k in fieldnames})

    # print summary per (size, role, algo) with OK/Fail counts
    print("\nSummary:")
    grouped = {}
    for r in all_rows:
        key = (r["size"], r["role"], r["algo"])
        grouped.setdefault(key, []).append(r)
    for key, vals in grouped.items():
        size, role, algo = key
        oks = [v for v in vals if v["ok"] == 1]
        fails = [v for v in vals if v["ok"] == 0]
        times = [v["time_ns"] for v in oks]
        if times:
            median_ms = statistics.median(times) / 1e6
            mean_ms = statistics.mean(times) / 1e6
            stdev_ms = statistics.stdev(times) / 1e6 if len(times) > 1 else 0.0
            print(f" size={size:3d} role={role:9s} algo={algo:12s} "
                  f"OK={len(oks):2d} FAIL={len(fails):2d} "
                  f"mean={mean_ms:.3f}ms median={median_ms:.3f}ms std={stdev_ms:.3f}ms")
        else:
            print(f" size={size:3d} role={role:9s} algo={algo:12s} OK=0 FAIL={len(fails):2d} (no timing)")
    print(f"\nCSV saved to {outp}")

if __name__ == "__main__":
    main()
