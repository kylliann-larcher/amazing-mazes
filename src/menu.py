# src/menu.py
from __future__ import annotations
from pathlib import Path
import sys

# --- Imports projet (tous en haut) ---
from config import MAZES_DIR, SOLUTIONS_DIR, IMAGES_DIR
from utils import Maze, resolve_maze_file
from features.gen_backtrack import BacktrackingGenerator
from features.gen_kruskal import KruskalGenerator
from features.solve_backtrack import BacktrackingSolver
from features.solve_astar import AStarSolver
from features.export_img import AsciiExporter
from visualize import ConsoleAnimator

# ---------------- Helpers ----------------
def ask_input_int(prompt: str, default: int | None = None) -> int:
    raw = input(prompt).strip()
    if raw == "" and default is not None:
        return default
    return int(raw)

def normalize_output_path(name: str | Path | None, default_dir: Path, default_name: str,
                          force_ext: str | None = None) -> Path:
    """
    - name vide -> default_dir/default_name
    - name simple -> default_dir/name
    - name avec dossier -> Path(name)
    - force_ext : si fourni (ex ".txt"), on force l'extension
    """
    if not name:
        res = default_dir / default_name
    else:
        p = Path(name)
        if p.parent == Path("."):
            res = default_dir / p.name
        else:
            res = p
    if force_ext and res.suffix.lower() != force_ext.lower():
        res = res.with_suffix(force_ext)
    return res

def strip_solution_marks(maze: Maze) -> Maze:
    """Remet un maze 'solution' en état brut en remplaçant 'o'/'*' par '.' pour visualiser la résolution."""
    g = [row[:] for row in maze.grid]
    h = len(g)
    w = len(g[0]) if h else 0
    for r in range(h):
        for c in range(w):
            if g[r][c] in ("o", "*"):
                g[r][c] = "."
    return Maze(g)

# ---------------- Handlers ----------------
def handle_generate():
    try:
        n = ask_input_int("Taille du labyrinthe (n>=1) ? (ENTER=5) ", default=5)
        if n < 1:
            print("⚠️ n doit être >= 1")
            return
    except Exception:
        print("⚠️ Entrée invalide.")
        return

    print("Algorithme de génération :")
    print("  1) Backtracking (DFS)  (par défaut)")
    print("  2) Kruskal")
    algo = input("Votre choix ? [1/2] (ENTER=1) ").strip() or "1"

    out_raw = input(f"Fichier de sortie (.txt) ? (ENTER pour data/outputs/mazes/maze_{n}.txt) ").strip()
    out_path = normalize_output_path(out_raw, MAZES_DIR, f"maze_{n}.txt", force_ext=".txt")

    try:
        if algo == "2":
            maze = KruskalGenerator(n).generate()
            algo_name = "Kruskal"
        else:
            maze = BacktrackingGenerator(n).generate()
            algo_name = "Backtracking"
    except Exception as e:
        print(f"Erreur lors de la génération : {e}")
        return

    try:
        saved = maze.save_txt(str(out_path))
    except TypeError:
        maze.save_txt(str(out_path))
        saved = str(out_path)
    print(f"✅ Généré ({algo_name}): {saved}")

def handle_solve_backtrack():
    src_raw = input("Fichier labyrinthe source (.txt) ? (ENTER pour data/outputs/mazes/maze_5.txt) ").strip()
    out_raw = input("Fichier solution (.txt) ? (ENTER pour data/outputs/solutions/solution_backtrack.txt) ").strip()

    if not src_raw:
        src_path = str(MAZES_DIR / "maze_5.txt")
    else:
        resolved = resolve_maze_file(src_raw)
        if resolved is None:
            print(f"⚠️ Fichier '{src_raw}' non trouvé.")
            return
        src_path = resolved

    out_path = normalize_output_path(out_raw, SOLUTIONS_DIR, "solution_backtrack.txt", force_ext=".txt")

    try:
        maze = Maze.load_txt(str(src_path))
    except FileNotFoundError as e:
        print(f"⚠️ {e}")
        return

    solver = BacktrackingSolver()
    solved = solver.solve(maze)

    try:
        saved = solved.save_txt(str(out_path))
    except TypeError:
        solved.save_txt(str(out_path))
        saved = str(out_path)
    print(f"✅ Solution Backtracking écrite: {saved}")

def handle_solve_astar():
    src_raw = input("Fichier labyrinthe source (.txt) ? (ENTER pour data/outputs/mazes/maze_5.txt) ").strip()
    out_raw = input("Fichier solution (.txt) ? (ENTER pour data/outputs/solutions/solution_astar.txt) ").strip()

    if not src_raw:
        src_path = str(MAZES_DIR / "maze_5.txt")
    else:
        resolved = resolve_maze_file(src_raw)
        if resolved is None:
            print(f"⚠️ Fichier '{src_raw}' non trouvé.")
            return
        src_path = resolved

    out_path = normalize_output_path(out_raw, SOLUTIONS_DIR, "solution_astar.txt", force_ext=".txt")

    try:
        maze = Maze.load_txt(str(src_path))
    except FileNotFoundError as e:
        print(f"⚠️ {e}")
        return

    solver = AStarSolver()
    solved = solver.solve(maze)

    try:
        saved = solved.save_txt(str(out_path))
    except TypeError:
        solved.save_txt(str(out_path))
        saved = str(out_path)
    print(f"✅ Solution A* écrite: {saved}")

def handle_export_image():
    src_raw = input(f"Fichier labyrinthe source (.txt) ? (ENTER pour data/outputs/mazes/maze_5.txt) ").strip()
    out_raw = input("Fichier image sortie (.png) ? (ENTER pour data/outputs/images/maze.png) ").strip()
    cell_size_raw = input("Taille cellule en pixels (ENTER=10) ? ").strip()

    if not src_raw:
        src_path = str(MAZES_DIR / "maze_5.txt")
    else:
        resolved = resolve_maze_file(src_raw)
        if resolved is None:
            print(f"⚠️ Fichier '{src_raw}' non trouvé dans {MAZES_DIR} ni dans {SOLUTIONS_DIR}.")
            print("    → Vérifie le nom, ou génère/solve d'abord le labyrinthe.")
            return
        src_path = resolved

    out_path = normalize_output_path(out_raw, IMAGES_DIR, "maze.png")
    try:
        cell_size = int(cell_size_raw) if cell_size_raw else 10
    except ValueError:
        print("⚠️ Taille cellule invalide, valeur par défaut 10 utilisée.")
        cell_size = 10

    try:
        maze = Maze.load_txt(str(src_path))
    except FileNotFoundError as e:
        print(f"⚠️ {e}")
        return

    exporter = AsciiExporter(cell_size=cell_size)
    try:
        saved = exporter.export(maze, str(out_path))
    except Exception as e:
        print(f"Erreur lors de l'export image: {e}")
        return
    print(f"✅ Image exportée: {saved}")

def handle_visual_generate():
    try:
        n = ask_input_int("Taille du labyrinthe (ENTER=20) ? ", default=20)
    except Exception:
        print("Entrée invalide."); return

    print("Algo génération : 1) Backtracking  2) Kruskal")
    algo = (input("Votre choix ? (ENTER=1) ").strip() or "1")
    speed = input("Vitesse (ms par frame, ENTER=25) ? ").strip()
    delay = int(speed) if speed else 25
    anim = ConsoleAnimator(delay_ms=delay, title="Génération (ASCII)")

    if algo == "2":
        KruskalGenerator(n).generate(on_step=anim)
    else:
        BacktrackingGenerator(n).generate(on_step=anim)

    print("\n✅ Terminé. (Appuie ENTER pour revenir au menu)")
    input()

def handle_visual_solve():
    src = input("Fichier labyrinthe source (.txt, mazes/ ou solutions/) ? ").strip()
    resolved = resolve_maze_file(src)
    if not resolved:
        print("⚠️ Fichier introuvable.")
        return
    maze = Maze.load_txt(resolved)

    # Nettoyage facultatif si c'est déjà une solution
    has_marks = any(ch in ("o", "*") for row in maze.grid for ch in row)
    if has_marks:
        ans = input("Le fichier semble déjà résolu (contient 'o' ou '*'). Nettoyer pour visualiser ? [Y/n] ").strip().lower()
        if ans in ("", "y", "yes", "o", "oui"):
            maze = strip_solution_marks(maze)

    print("Algo résolution : 1) Backtracking  2) A*")
    algo = (input("Votre choix ? (ENTER=1) ").strip() or "1")
    speed = input("Vitesse (ms par frame, ENTER=15) ? ").strip()
    delay = int(speed) if speed else 15

    visit_anim = ConsoleAnimator(delay_ms=delay, title="Résolution - Exploration (*)")
    path_anim  = ConsoleAnimator(delay_ms=delay, title="Résolution - Chemin (o)")

    if algo == "2":
        AStarSolver().solve(maze, on_visit=visit_anim, on_path=path_anim)
    else:
        BacktrackingSolver().solve(maze, on_visit=visit_anim, on_path=path_anim)

    print("\n✅ Terminé. (Appuie ENTER pour revenir au menu)")
    input()

# ---------------- Menu loop ----------------
def run():
    """Boucle interactive : affiche le menu, exécute l'action, puis revient au menu."""
    try:
        while True:
            print("\n=== Amazing Mazes (POO) ===")
            print("1) Générer un labyrinthe (Backtracking / Kruskal)")
            print("2) Résoudre un labyrinthe (Backtracking)")
            print("3) Résoudre un labyrinthe (A*)")
            print("4) Exporter ASCII -> PNG")
            print("5) [Visuel] Générer un labyrinthe (Backtracking / Kruskal)")
            print("6) [Visuel] Résoudre un labyrinthe (Backtracking / A*)")
            print("q) Quitter")
            choice = input("Votre choix ? [1/2/3/4/5/6/q] ").strip().lower()

            if choice == "1": handle_generate()
            elif choice == "2": handle_solve_backtrack()
            elif choice == "3": handle_solve_astar()
            elif choice == "4": handle_export_image()
            elif choice == "5": handle_visual_generate()
            elif choice == "6": handle_visual_solve()
            elif choice == "q":
                print("Au revoir 👋")
                break
            else:
                print("Choix invalide. Réessaie.")

    except KeyboardInterrupt:
        print("\nInterrompu par l'utilisateur. Au revoir 👋")
    except Exception as e:
        print(f"\nUne erreur inattendue est survenue : {e}")
        print("Tu peux relancer le programme. Si l'erreur persiste, copie-colle le message ici.")
