# src/main.py
from __future__ import annotations
from pathlib import Path
from config import MAZES_DIR, SOLUTIONS_DIR, IMAGES_DIR
from features.gen_backtrack import BacktrackingGenerator
from features.solve_backtrack import BacktrackingSolver
from features.solve_astar import AStarSolver
from features.export_img import AsciiExporter
from utils import Maze
import sys

def ask_input_int(prompt: str, default: int | None = None) -> int:
    raw = input(prompt).strip()
    if raw == "" and default is not None:
        return default
    try:
        return int(raw)
    except ValueError:
        raise

def normalize_output_path(name: str | Path, default_dir: Path, default_name: str) -> Path:
    """
    Retourne un Path complet :
    - si name vide -> default_dir/default_name
    - si name donné et contient dossier -> Path(name)
    - si name donné uniquement comme nom de fichier -> default_dir / name
    """
    if not name:
        return default_dir / default_name
    p = Path(name)
    if p.parent == Path("."):
        return default_dir / p.name
    return p

def cli():
    print("=== Amazing Mazes (POO) ===")
    print("1) Générer un labyrinthe (Backtracking)")
    print("2) Résoudre un labyrinthe (Backtracking)")
    print("3) Résoudre un labyrinthe (A*)")
    print("4) Exporter ASCII -> PNG")
    print("q) Quitter")
    choice = input("Votre choix ? [1/2/3/4/q] ").strip().lower()

    # === Remplacer le bloc "if choice == '1':" existant par ce bloc ===
    if choice == "1":
        # Taille
        try:
            n = ask_input_int("Taille du labyrinthe (n>=1) ? (ENTER=5) ", default=5)
            if n < 1:
                print("⚠️ n doit être >= 1")
                return
        except Exception:
            print("⚠️ Entrée invalide.")
            return

        # Choix de l'algorithme de génération
        print("Algorithme de génération :")
        print("  1) Backtracking (DFS)  (par défaut)")
        print("  2) Kruskal")
        algo = input("Votre choix ? [1/2] (ENTER=1) ").strip() or "1"

        # Choix du nom de sortie
        out_raw = input(f"Fichier de sortie (.txt) ? (ENTER pour data/outputs/mazes/maze_{n}.txt) ").strip()
        out_path = normalize_output_path(out_raw, MAZES_DIR, f"maze_{n}.txt")

        # Sélection de la classe de génération
        if algo == "2":
            try:
                from features.gen_kruskal import KruskalGenerator as GenClass
            except Exception as e:
                print(f"Erreur import KruskalGenerator : {e}")
                print("Vérifie que src/features/gen_kruskal.py existe.")
                return
        else:
            from features.gen_backtrack import BacktrackingGenerator as GenClass

    # Génération
        try:
            gen = GenClass(n)
            maze = gen.generate()
        except Exception as e:
            print(f"Erreur lors de la génération : {e}")
            return

        # Sauvegarde (Maze.save_txt supporte str/Path)
        try:
            saved = maze.save_txt(str(out_path))
        except TypeError:
            maze.save_txt(str(out_path))
            saved = str(out_path)

        print(f"✅ Généré ({'Kruskal' if algo=='2' else 'Backtracking'}): {saved}")
        return
# === fin du bloc à remplacer ===


    if choice == "2":
        src_raw = input(f"Fichier labyrinthe source (.txt) ? (ENTER pour dernier généré) ").strip()
        out_raw = input("Fichier solution (.txt) ? (ENTER pour data/outputs/solutions/solution_backtrack.txt) ").strip()

        # si l'utilisateur n'a pas donné src, on essaye un default (dernier ou maze_5.txt)
        if not src_raw:
            # prefer maze_5.txt as safe default
            src_path = MAZES_DIR / "maze_5.txt"
        else:
            src_path = Path(src_raw)
            if src_path.parent == Path("."):
                src_path = MAZES_DIR / src_path.name

        out_path = normalize_output_path(out_raw, SOLUTIONS_DIR, "solution_backtrack.txt")

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
        return

    if choice == "3":
        src_raw = input(f"Fichier labyrinthe source (.txt) ? (ENTER pour last) ").strip()
        out_raw = input("Fichier solution (.txt) ? (ENTER pour data/outputs/solutions/solution_astar.txt) ").strip()

        if not src_raw:
            src_path = MAZES_DIR / "maze_5.txt"
        else:
            src_path = Path(src_raw)
            if src_path.parent == Path("."):
                src_path = MAZES_DIR / src_path.name

        out_path = normalize_output_path(out_raw, SOLUTIONS_DIR, "solution_astar.txt")

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
        return

    if choice == "4":
        src_raw = input(f"Fichier labyrinthe source (.txt) ? (ENTER pour data/outputs/mazes/maze_5.txt) ").strip()
        out_raw = input("Fichier image sortie (.png) ? (ENTER pour data/outputs/images/maze.png) ").strip()
        cell_size_raw = input("Taille cellule en pixels (ENTER=10) ? ").strip()

        if not src_raw:
            src_path = MAZES_DIR / "maze_5.txt"
        else:
            src_path = Path(src_raw)
            if src_path.parent == Path("."):
                src_path = MAZES_DIR / src_path.name

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
        return

    if choice == "q":
        print("Au revoir 👋")
        sys.exit(0)

    print("Choix invalide.")

if __name__ == "__main__":
    cli()
