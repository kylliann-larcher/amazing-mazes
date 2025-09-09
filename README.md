#  Amazing Mazes

Projet 2 B2 IA  : génération et résolution de labyrinthes parfaits en Python.  
Le but est de créer un générateur de labyrinthes (Backtracking, Kruskal) et des solveurs (Backtracking, A*), puis de visualiser le résultat en ASCII ou en image.

---

##  Installation

Cloner le repo puis installer les dépendances dans un environnement virtuel :

```bash
git clone https://github.com/votre-compte/amazing-mazes.git
cd amazing-mazes

python -m venv .venv
# Linux/Mac
source .venv/bin/activate
# Windows
.venv\Scripts\activate

pip install -r requirements.txt 
```

## Utilisation

Lancer le programme principal :

```bash
python src/main.py
```

## Arborescence

```bash
amazing-mazes/
├─ src/
│  ├─ main.py           # Point d’entrée du programme (CLI: générer / résoudre)
│  ├─ utils.py          # Fonctions utilitaires (I/O fichiers, affichage ASCII)
│  └─ features/         # Modules par fonctionnalité
│     ├─ gen_backtrack.py   # Générateur Backtracking
│     ├─ gen_kruskal.py     # Générateur Kruskal (bonus)
│     ├─ solve_backtrack.py # Solveur Backtracking
│     ├─ solve_astar.py     # Solveur A*
│     └─ export_img.py      # Conversion ASCII → PNG (bonus)
├─ tests/               # Tests unitaires avec pytest
├─ data/
│  ├─ samples/          # Labyrinthes d’exemple
│  └─ outputs/          # Labyrinthes générés par le programme
├─ .gitignore           # Fichiers à ignorer par Git
├─ requirements.txt     # Dépendances Python
└─ README.md            # Documentation projet
```

