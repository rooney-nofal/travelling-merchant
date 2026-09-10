"""Construction du graphe complet pondéré des villes."""

import networkx as nx


def build_graph(cities, distance_matrix):
    """
    Transforme nos données en graphe.

    Chaque ville = un sommet.
    Chaque liaison entre deux villes = une arête.
    Le poids de l'arête = distance Haversine.
    """

    # On crée un graphe vide.
    graph = nx.Graph()

    # =========================================================
    # ÉTAPE 1 — Ajouter les villes comme sommets
    # =========================================================
    #
    # enumerate(cities) donne :
    # - index : numéro associé à la ville
    # - (name, lat, lon) : données de cette ville
    #
    # Exemple :
    # index = 0
    # name = "Paris"
    # lat = 48.8566
    # lon = 2.3522
    for index, (name, lat, lon) in enumerate(cities):

        # On ajoute le sommet au graphe.
        # L'indice devient l'identifiant du sommet.
        graph.add_node(
            index,
            name=name,
            lat=lat,
            lon=lon,
        )

    # =========================================================
    # ÉTAPE 2 — Relier toutes les villes entre elles
    # =========================================================
    #
    # i représente la première ville.
    for i in range(len(cities)):

        # j représente la deuxième ville.
        #
        # On commence à i + 1 pour éviter :
        # - de relier une ville à elle-même
        # - de créer deux fois Paris-Lyon et Lyon-Paris.
        for j in range(i + 1, len(cities)):

            # On récupère dans la matrice la distance entre i et j
            # et on la stocke comme poids de l'arête.
            graph.add_edge(
                i,
                j,
                weight=float(
                    distance_matrix[i][j]
                ),
            )

    # Le graphe complet est maintenant construit.
    return graph
