# src/menu.py
from __future__ import annotations
from pathlib import Path
import sys

from config import MAZES_DIR, SOLUTIONS_DIR, IMAGES_DIR
from utils import Maze, resolve_maze_file

# helpers -------------------------------------------------------------------
def ask_input_int(prompt: str, default: int | None = None) -> int:
    raw = input(prompt).strip()
    if raw == "" and default is not None:
        return default
    return int(raw)

def normalize_output_path(name: str | Path | None, default_dir: Path, default_name: str,
                          force_ext: str | None = None) -> Path:
    """
    Normalise les chemins de sortie :
      - name vide -> default_dir/default_name
      - name simple -> default_dir/name
      - name avec dossier -> Path(name)
      - force_ext : forcer l'extension (ex ".txt")
    """
    if not name:
        res = default_dir / default_name
    else:
        p = Path(name)
        if p.parent == Path("."):
            res = default_dir / p.name
        else:
            res = p
    if force_ext:
        if res.suffix.lower() != force_ext.lower():
            res = res.with_suffix(force_ext)
    return res

# Handlers ------------------------------------------------------------------
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

    # Choix de la classe génératrice
    if algo == "2":
        try:
            from features.gen_kruskal import KruskalGenerator as GenClass
        except Exception as e:
            print(f"Erreur import KruskalGenerator : {e}")
            print("Vérifie que src/features/gen_kruskal.py existe.")
            return
    else:
        from features.gen_backtrack import BacktrackingGenerator as GenClass

    try:
        gen = GenClass(n)
        maze = gen.generate()
    except Exception as e:
        print(f"Erreur lors de la génération : {e}")
        return

    try:
        saved = maze.save_txt(str(out_path))
    except TypeError:
        maze.save_txt(str(out_path))
        saved = str(out_path)
    print(f"✅ Généré ({'Kruskal' if algo=='2' else 'Backtracking'}): {saved}")


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

    from features.solve_backtrack import BacktrackingSolver
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

    from features.solve_astar import AStarSolver
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

    # resolve source file across mazes/solutions
    if not src_raw:
        src_path = str(MAZES_DIR / "maze_5.txt")
    else:
        resolved = resolve_maze_file(src_raw)
        if resolved is None:
            print(f"⚠️ Fichier '{src_raw}' non trouvé dans {MAZES_DIR} ni dans {SOLUTIONS_DIR}.")
            print("    → Vérifie le nom, ou génère/solve d'abord le labyrinthe.")
            # propose de générer ? non pour garder handler simple
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

    # importer AsciiExporter dynamiquement pour éviter crash si Pillow absent
    try:
        from features.export_img import AsciiExporter
    except Exception as e:
        print(f"Erreur import AsciiExporter (Pillow peut manquer): {e}")
        return

    exporter = AsciiExporter(cell_size=cell_size)
    try:
        saved = exporter.export(maze, str(out_path))
    except Exception as e:
        print(f"Erreur lors de l'export image: {e}")
        return
    print(f"✅ Image exportée: {saved}")


# Main loop -----------------------------------------------------------------
# Main loop (remplacer l'ancienne fonction run par celle-ci)
def run():
    """Boucle interactive : affiche le menu, exécute l'action demandée, revient au menu."""
    try:
        while True:
            print("\n=== Amazing Mazes (POO) ===")
            print("1) Générer un labyrinthe (Backtracking / Kruskal)")
            print("2) Résoudre un labyrinthe (Backtracking)")
            print("3) Résoudre un labyrinthe (A*)")
            print("4) Exporter ASCII -> PNG")
            print("q) Quitter")
            choice = input("Votre choix ? [1/2/3/4/q] ").strip().lower()

            if choice == "1":
                handle_generate()
            elif choice == "2":
                handle_solve_backtrack()
            elif choice == "3":
                handle_solve_astar()
            elif choice == "4":
                handle_export_image()
            elif choice == "q":
                print("Au revoir 👋")
                break
            else:
                print("Choix invalide. Réessaie.")

    except KeyboardInterrupt:
        # Ctrl+C friendly exit
        print("\nInterrompu par l'utilisateur. Au revoir 👋")
    except Exception as e:
        # On attrape les erreurs non prévues pour ne pas quitter sans explication
        print(f"\nUne erreur inattendue est survenue : {e}")
        print("Tu peux relancer le programme. Si l'erreur persiste, copie-colle le message ici.")
