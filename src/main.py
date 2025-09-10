from __future__ import annotations
from features.gen_backtrack import BacktrackingGenerator
from features.solve_backtrack import BacktrackingSolver
from utils import Maze

def cli():
    print("=== Amazing Mazes (POO) ===")
    print("1) Générer un labyrinthe (Backtracking)")
    print("2) Résoudre un labyrinthe (Backtracking)")
    choice = input("Votre choix ? [1/2] ").strip()

    if choice == "1":
        try:
            n = int(input("Taille du labyrinthe (n>=1) ? ").strip())
            if n < 1:
                raise ValueError
        except ValueError:
            print("⚠️  Merci de saisir un entier >= 1.")
            return

        out = input("Fichier de sortie (.txt) ? ").strip() or f"data/outputs/maze_{n}.txt"
        gen = BacktrackingGenerator(n)
        maze = gen.generate()
        maze.save_txt(out)
        print(f"✅ Généré: {out}")
        print("👉 Tu peux maintenant choisir l'option 2 pour le résoudre.")

    elif choice == "2":
        src = input("Fichier labyrinthe source (.txt) ? ").strip() or "data/outputs/maze_5.txt"
        out = input("Fichier solution (.txt) ? ").strip() or "data/outputs/solution.txt"
        try:
            maze = Maze.load_txt(src)
        except FileNotFoundError as e:
            print(f"⚠️  {e}")
            print("Astuce: commence par générer un labyrinthe avec l'option 1.")
            return

        solver = BacktrackingSolver()
        solved = solver.solve(maze)
        solved.save_txt(out)
        print(f"✅ Solution écrite: {out}")

    else:
        print("Choix invalide.")

if __name__ == "__main__":
    cli()
