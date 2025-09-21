#  Amazing Mazes

Projet éducatif et expérimental autour de la **génération** et de la **résolution** de labyrinthes.  
L’objectif est double :  
1. Construire un outil complet (génération, résolution, export, visualisation).  
2. Comparer expérimentalement différents algorithmes pour **mesurer leurs limites, performances et comportements structurels**.

---

## 🎯 Objectifs pédagogiques

- Comprendre et implémenter plusieurs algorithmes classiques :
  - **Génération** : Backtracking (DFS), Kruskal.
  - **Résolution** : Backtracking (DFS), A*.
- Illustrer les différences entre algorithmes :
  - Temps d’exécution, consommation mémoire, scalabilité.
  - Qualité du chemin trouvé (optimal ou non).
  - Exploration (brute vs heuristique).
- Démontrer les **limites de la récursion** en pratique (RecursionError).
- Fournir un cadre reproductible avec :
  - Benchmarks internes (`internal_bench.py` → CSV),
  - Notebook d’analyse (`bench_report.ipynb` → graphes + conclusion),
  - Visualisation ASCII animée.

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

# PowerShell
.\.venv\Scripts\Activate.ps1


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
├─ src/ # code principal
│ ├─ features/ # algorithmes (générateurs et solveurs)
│ ├─ utils.py # classe Maze + helpers
│ ├─ menu.py # menu interactif
│ └─ main.py # point d’entrée
├─ data/outputs/ # labyrinthes générés, solutions, images, benchmarks
├─ scripts/ # outils internes (benchmarks)
├─ notebooks/ # analyse et rapport
└─ tests/ # tests unitaires (pytest)
```

---

## ⚙️ Fonctionnalités

### Génération
- **Backtracking (DFS)** : exploration en profondeur, labyrinthes sinueux.  
- **Kruskal** : approche par graphe (union-find), plus équilibrée et stable.

### Résolution
- **Backtracking Solver** : DFS récursif, chemin valide mais pas toujours optimal.  
- **A*** : heuristique (Manhattan), trouve toujours le plus court chemin.  

### Export & Visualisation
- Sauvegarde `.txt` et export `.png` (Pillow).  
- Animation ASCII pour visualiser :
  - la génération (mur par mur),
  - la résolution (`*` exploration, `o` chemin).

### Benchmarks
- Script `internal_bench.py` :
  - mesures de temps et mémoire,
  - détection des erreurs (ex. RecursionError),
  - statistiques structurelles (corridors, chemin, exploration).

### Rapport
- Notebook `bench_report.ipynb` :
  - description des colonnes du CSV,
  - graphes (temps, mémoire, exploration, longueur de chemin),
  - analyses et conclusion.

---

## 🔎 Résultats expérimentaux

### 1. Générateurs
- **Backtracking** : rapide, mais limité par la récursion.  
- **Kruskal** : plus stable, adapté aux grandes tailles.

### 2. Solveurs
- **Backtracking Solver (DFS)** :
  - explore presque tout le labyrinthe (exploration inefficace),
  - peut échouer par RecursionError,
  - chemin valide mais non optimal.
- **A\*** :
  - explore sélectivement,
  - toujours optimal,
  - plus scalable.

### 3. Analyses
- Temps et mémoire en **O(n²)**, cohérents avec la taille du labyrinthe.  
- **DFS récursif** échoue au-delà de ~100–150 cellules de côté (recursionlimit=1000).  
- **A\*** explore beaucoup moins de cases que DFS.  
- **Qualité des solutions** : A\* > Backtracking.  

---
### Menu interactif:

1) Générer un labyrinthe (Backtracking / Kruskal)
2) Résoudre un labyrinthe (Backtracking)
3) Résoudre un labyrinthe (A*)
4) Exporter ASCII -> PNG
5) [Visuel] Générer un labyrinthe (ASCII animé)
6) [Visuel] Résoudre un labyrinthe (ASCII animé)
q) Quitter

### Benchmarks

```bash
python scripts/internal_bench.py
```
### Rapport

Ouvrir notebooks/bench_report.ipynb dans Jupyter/VSCode.

# Conclusion

#### Ce projet illustre :

- Les différences pédagogiques entre algorithmes récursifs et itératifs.

- L’importance de la scalabilité : ce qui marche en petit échoue en grand.

- La puissance d’algorithmes heuristiques comme A* pour l’optimisation de chemin.

#### En résumé :

- DFS (Backtracking) est un excellent support pédagogique, mais limité.

- Kruskal et A* sont plus robustes et adaptés aux grandes tailles.

- Le projet démontre par l’expérience ce que disent la théorie et la complexité.

---
Projet réalisé dans le cadre de ma formation en IA & Data.
Objectif : combiner programmation Python, algorithmique, analyse expérimentale et bonnes pratiques de projet (tests, visualisation, benchmark, rapport).

---
