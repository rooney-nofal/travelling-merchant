# Le marchand ambulant — TSP sur 20 villes françaises

Projet La Plateforme — résolution du **Problème du Voyageur de Commerce** (TSP) :
trouver la tournée la plus courte permettant à Théobald, marchand ambulant, de
visiter 20 villes françaises une seule fois chacune avant de revenir à son point
de départ. Avec 20 villes, il existe 19!/2 ≈ 6,08 × 10¹⁶ tournées possibles :
la force brute est exclue, on optimise.

**Réalisé par : Rooney Nofal & Yanis Founas**

## Structure du projet

| Chemin | Rôle |
|---|---|
| `data/villes_france_lat_long.csv` | Les 20 villes (nom, latitude, longitude) |
| `src/cities.py` | Chargement des villes depuis le CSV |
| `src/distances.py` | Distance de Haversine + matrice 20×20 |
| `src/graph.py` | Graphe complet pondéré NetworkX (20 sommets, 190 arêtes) |
| `src/visualization.py` | Cartes interactives Folium (villes, tournées) |
| `src/christofides.py` | Algorithme de Christofides |
| `src/genetic_algorithm.py` | Algorithme génétique |
| `src/comparison.py` | Étude comparative complète (temps, robustesse, configurations) |
| `tests/` | Tests unitaires |
| `main.py` | Point d'entrée : pipeline Christofides complet |

## Installation et exécution

```bash
git clone https://github.com/rooney-nofal/travelling-merchant.git
cd travelling-merchant
python -m venv .venv
.venv\Scripts\activate        # Windows (Linux/macOS : source .venv/bin/activate)
pip install -r requirements.txt

python main.py                    # Christofides + carte + résultats JSON
python src/genetic_algorithm.py   # Algorithme génétique (démo, seed=42)
python src/comparison.py          # Étude comparative complète (~4 min)
python -m unittest discover tests # Tests
```

Les cartes et résultats sont générés dans `outputs/`.

## Modélisation

Les villes sont les **sommets** d'un graphe complet non orienté ; chaque paire de
villes est reliée par une **arête** dont le poids est la distance de **Haversine**
(distance du grand cercle sur la sphère terrestre, en km). La matrice 20×20 des
distances est précalculée une fois et partagée par les deux algorithmes.

## Algorithme 1 — Christofides

Construction déterministe en cinq étapes : arbre couvrant minimal (MST, 19 arêtes),
sommets de degré impair (12), couplage parfait de poids minimal (6 paires),
circuit eulérien, raccourci en tournée hamiltonienne. **Garantie théorique :
tournée ≤ 1,5 × l'optimum** pour un TSP métrique.

- **Résultat : 3 445,60 km** en ~5 ms (MST 2 665,05 km + couplage 1 142,03 km)
- Déterministe : le même résultat à chaque exécution.

## Algorithme 2 — Génétique

Une population de tournées aléatoires évolue par **sélection par tournoi**,
**croisement ordonné (OX)** — qui préserve la validité des permutations —,
**mutation par inversion** de segment et **élitisme**, pendant plusieurs
centaines de générations.

Paramètres par défaut (configuration B) : population 300, 800 générations,
tournoi 5, mutation 0,25, élitisme 5.

- **Meilleur résultat : 3 157,12 km** en ~7 s — soit **−288,48 km (−8,4 %)**
  par rapport à Christofides.
- Non déterministe : sur 10 exécutions (graines différentes) —
  meilleur 3 157, moyenne 3 196, pire 3 367, écart-type ±82 km.
  **Même la pire exécution reste meilleure que Christofides.**

### Configurations testées

| Configuration | Population | Générations | Mutation | Meilleur | Moyenne | Temps/run |
|---|---|---|---|---|---|---|
| A (rapide)     | 100 | 300   | 0,15 | 3 157,12 km | 3 303,69 km | ~1 s  |
| B (équilibrée) | 300 | 800   | 0,25 | 3 157,12 km | 3 227,12 km | ~8 s  |
| C (intensive)  | 600 | 1 500 | 0,30 | 3 157,12 km | 3 157,12 km | ~33 s |

Plus on investit de calcul, plus on atteint l'optimum de façon fiable : la
configuration C l'a trouvé à chaque essai. Le fait que des exécutions
indépendantes convergent vers 3 157,12 km suggère fortement que cette valeur
est l'optimum global du problème.

## Analyse comparative

| Critère | Christofides | Algorithme génétique |
|---|---|---|
| Distance | 3 445,60 km | **3 157,12 km** (−8,4 %) |
| Temps d'exécution | **~5 ms** | ~7 s (config B) à ~33 s (config C) |
| Robustesse | Déterministe, garantie ≤ 1,5 × opt | Aléatoire, ±82 km sur 10 runs |
| Facilité d'implémentation | Complexe (couplage parfait minimal) | Concepts simples, mais réglage des paramètres nécessaire |

## Conclusion et recommandation

Pour Théobald, chaque kilomètre économisé réduit les coûts, les délais et
l'exposition aux dangers de la route. **Nous recommandons l'algorithme
génétique (configuration C)** : quelques dizaines de secondes de calcul avant
le départ sont négligeables à l'échelle d'une tournée, et le gain de 288 km
par tour de France est considérable et reproductible. Christofides reste
précieux comme **référence de sécurité** : instantané, déterministe et
mathématiquement garanti — idéal pour valider que la solution génétique ne
dérive jamais. En perspective, une approche hybride (initialiser la population
génétique avec la tournée de Christofides) combinerait la garantie de l'un et
la performance de l'autre.