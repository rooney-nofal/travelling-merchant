# Travelling Merchant — Christofides

Projet de résolution du **Travelling Salesman Problem (TSP)** sur **20 villes françaises**.

Cette partie du projet implémente l'algorithme de **Christofides** avec des distances géographiques calculées à partir des coordonnées GPS.

## Objectif

Trouver une tournée passant une fois par chacune des 20 villes puis revenant au point de départ, en limitant la distance totale.

## Pipeline

```text
CSV des villes
    ↓
Distances Haversine
    ↓
Matrice 20 × 20
    ↓
Graphe complet pondéré — 190 arêtes
    ↓
MST avec Prim
    ↓
Sommets de degré impair
    ↓
Matching minimum
    ↓
Multigraphe eulérien
    ↓
Circuit eulérien
    ↓
Raccourci des sommets déjà visités
    ↓
Tournée Christofides
```

## Structure du projet

```text
travelling-merchant/
│
├── data/
│   └── villes_france_lat_long.csv
│
├── outputs/
│   └── .gitkeep
│
├── src/
│   ├── __init__.py
│   ├── cities.py
│   ├── distances.py
│   ├── graph.py
│   ├── christofides.py
│   └── visualization.py
│
├── tests/
│   ├── __init__.py
│   └── test_christofides.py
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation sous Windows / VS Code

Dans le terminal ouvert à la racine du projet :

```powershell
py -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## Exécuter Christofides

```powershell
python main.py
```

Le programme affiche les métriques dans le terminal et crée :

```text
outputs/christofides_route.html
outputs/christofides_result.json
```

## Résultats attendus avec les données fournies

| Mesure | Résultat |
|---|---:|
| Villes | 20 |
| Arêtes du graphe complet | 190 |
| Arêtes du MST | 19 |
| Poids du MST | 2 665,05 km |
| Sommets impairs | 12 |
| Paires du matching | 6 |
| Poids du matching | 1 142,03 km |
| Tournée Christofides | 3 445,60 km |

## Tester le projet

```powershell
python -m unittest discover -s tests -v
```

## Publier sur GitHub

Ne jamais envoyer `.venv` sur GitHub.

```powershell
git status
git add .
git commit -m "Add Christofides TSP implementation"
git push origin main
```


## Lisibilité du code

Le code est volontairement commenté de manière pédagogique.

Les étapes principales sont numérotées directement dans `main.py`
et `src/christofides.py` afin de pouvoir suivre facilement le raisonnement :

```text
1. Charger les villes
2. Calculer les distances
3. Construire le graphe
4. Construire le MST
5. Trouver les sommets impairs
6. Faire le matching
7. Construire le circuit eulérien
8. Obtenir la tournée finale
9. Afficher et sauvegarder les résultats
```
