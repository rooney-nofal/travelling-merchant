"""Point d'entrée principal du projet Christofides."""

import json
from pathlib import Path

from src.christofides import christofides
from src.cities import load_cities
from src.distances import build_distance_matrix
from src.graph import build_graph
from src.visualization import plot_route


# Dossier dans lequel on enregistre les résultats générés.
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"


def main():
    """
    Lance tout le projet dans l'ordre.

    On peut lire ce fichier comme une histoire :
    villes -> distances -> graphe -> Christofides -> résultats -> carte.
    """

    # =========================================================
    # ÉTAPE 1 — Charger les villes
    # =========================================================
    # On lit le CSV contenant :
    # nom de la ville, latitude et longitude.
    cities = load_cities()

    # =========================================================
    # ÉTAPE 2 — Calculer les distances
    # =========================================================
    # À partir des coordonnées GPS,
    # on calcule une distance Haversine entre chaque paire de villes.
    #
    # Avec 20 villes, on obtient une matrice 20 x 20.
    distance_matrix = build_distance_matrix(cities)

    # =========================================================
    # ÉTAPE 3 — Construire le graphe complet
    # =========================================================
    # Chaque ville devient un sommet.
    # Chaque liaison entre deux villes devient une arête.
    # Le poids de l'arête correspond à la distance.
    graph = build_graph(
        cities,
        distance_matrix,
    )

    # =========================================================
    # ÉTAPE 4 — Lancer Christofides
    # =========================================================
    # L'indice 0 correspond à Paris dans notre fichier CSV.
    result = christofides(
        graph,
        start=0,
    )

    # =========================================================
    # ÉTAPE 5 — Transformer les indices en noms de villes
    # =========================================================
    # L'algorithme travaille avec des indices : 0, 1, 2...
    # Ici on récupère les vrais noms pour l'affichage.
    route_names = [
        cities[index][0]
        for index in result.route
    ]

    # =========================================================
    # ÉTAPE 6 — Afficher les métriques dans le terminal
    # =========================================================
    print("=" * 60)
    print("CHRISTOFIDES — TSP SUR 20 VILLES FRANÇAISES")
    print("=" * 60)

    print(f"Villes                : {len(cities)}")
    print(f"Arêtes du graphe      : {graph.number_of_edges()}")
    print(f"Poids du MST          : {result.mst_weight:.2f} km")
    print(f"Sommets impairs       : {len(result.odd_vertices)}")
    print(f"Paires du matching    : {len(result.matching)}")
    print(f"Poids du matching     : {result.matching_weight:.2f} km")
    print(f"Distance de la tournée: {result.total_distance:.2f} km")

    print()
    print("Tournée :")

    # On rajoute la première ville à la fin uniquement pour l'affichage,
    # afin de montrer que la tournée revient à son point de départ.
    print(
        " -> ".join(
            route_names + [route_names[0]]
        )
    )

    # =========================================================
    # ÉTAPE 7 — Générer la carte interactive
    # =========================================================
    # Folium crée un fichier HTML ouvrable dans un navigateur.
    map_path = plot_route(
        result.route,
        cities,
        result.total_distance,
        filename="christofides_route.html",
    )

    # =========================================================
    # ÉTAPE 8 — Enregistrer les résultats en JSON
    # =========================================================
    # Cela permet de réutiliser facilement les chiffres
    # dans une autre partie du projet.
    OUTPUT_DIR.mkdir(exist_ok=True)

    json_path = (
        OUTPUT_DIR
        / "christofides_result.json"
    )

    with open(
        json_path,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            {
                "route_indices": result.route,
                "route_names": route_names,
                "total_distance_km": round(
                    result.total_distance,
                    2,
                ),
                "mst_weight_km": round(
                    result.mst_weight,
                    2,
                ),
                "odd_vertices_count": len(
                    result.odd_vertices
                ),
                "matching_pairs_count": len(
                    result.matching
                ),
                "matching_weight_km": round(
                    result.matching_weight,
                    2,
                ),
            },
            file,
            ensure_ascii=False,
            indent=2,
        )

    # =========================================================
    # ÉTAPE 9 — Indiquer où se trouvent les fichiers générés
    # =========================================================
    print()
    print(f"Carte HTML : {map_path}")
    print(f"Résultats  : {json_path}")


# Ce bloc signifie :
# exécuter main() uniquement si on lance directement ce fichier.
if __name__ == "__main__":
    main()
