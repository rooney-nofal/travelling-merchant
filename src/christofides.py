"""Implémentation pédagogique de l'algorithme de Christofides pour un TSP métrique."""

from dataclasses import dataclass
import networkx as nx


@dataclass
class ChristofidesResult:
    """
    Regroupe tous les résultats utiles de l'algorithme.

    Cela évite de retourner plusieurs variables séparées.
    """

    route: list[int]
    total_distance: float
    mst_weight: float
    odd_vertices: list[int]
    matching: list[tuple[int, int]]
    matching_weight: float
    eulerian_edge_count: int


def route_distance(graph, route):
    """Calcule la distance totale d'une tournée fermée."""

    # Si la tournée contient moins de 2 villes, il n'y a pas de distance à calculer.
    if len(route) < 2:
        return 0.0

    total = 0.0

    # On parcourt chaque ville de la tournée.
    for i in range(len(route)):

        # Ville actuelle.
        current_city = route[i]

        # Ville suivante.
        # Le modulo permet de revenir automatiquement à la première ville
        # quand on atteint la fin de la liste.
        next_city = route[(i + 1) % len(route)]

        # On ajoute la distance entre les deux villes au total.
        total += graph[current_city][next_city]["weight"]

    return total


def build_mst(graph):
    """
    ÉTAPE 1 — Construire le MST.

    MST = Minimum Spanning Tree = arbre couvrant minimum.

    L'idée :
    relier toutes les villes avec le moins de kilomètres possible,
    sans créer de cycle à cette étape.
    """

    # NetworkX construit ici le MST avec l'algorithme de Prim.
    mst = nx.minimum_spanning_tree(
        graph,
        weight="weight",
        algorithm="prim",
    )

    return mst


def find_odd_vertices(mst):
    """
    ÉTAPE 2 — Trouver les sommets de degré impair.

    Le degré d'un sommet = nombre d'arêtes qui touchent ce sommet.

    Christofides doit ensuite "corriger" ces sommets impairs
    pour pouvoir construire un circuit eulérien.
    """

    odd_vertices = []

    # mst.degree() renvoie chaque sommet avec son degré.
    for node, degree in mst.degree():

        # Si le reste de la division par 2 vaut 1,
        # alors le degré est impair.
        if degree % 2 == 1:
            odd_vertices.append(node)

    return odd_vertices


def build_minimum_matching(graph, odd_vertices):
    """
    ÉTAPE 3 — Relier les sommets impairs deux par deux.

    On crée d'abord un sous-graphe contenant uniquement
    les sommets impairs.

    Ensuite on cherche le matching parfait de poids minimum :
    chaque sommet impair est associé à un autre,
    tout en ajoutant le moins de distance possible.
    """

    # On récupère uniquement les sommets impairs
    # et les distances qui existent entre eux.
    odd_graph = graph.subgraph(odd_vertices).copy()

    # NetworkX cherche le couplage de poids minimum.
    matching = nx.algorithms.matching.min_weight_matching(
        odd_graph,
        weight="weight",
    )

    # On transforme le résultat en liste pour faciliter la lecture.
    return list(matching)


def build_eulerian_multigraph(graph, mst, matching):
    """
    ÉTAPE 4 — Construire un multigraphe eulérien.

    On part du MST puis on ajoute les arêtes du matching.

    Après cet ajout, tous les sommets ont un degré pair.
    Cela permet d'obtenir un circuit eulérien.
    """

    # MultiGraph est utilisé car plusieurs arêtes
    # peuvent éventuellement relier les mêmes sommets.
    eulerian_graph = nx.MultiGraph(mst)

    # On ajoute toutes les paires obtenues lors du matching.
    for u, v in matching:
        eulerian_graph.add_edge(
            u,
            v,
            weight=graph[u][v]["weight"],
        )

    return eulerian_graph


def euler_to_hamiltonian(eulerian_graph, start=0):
    """
    ÉTAPE 5 — Transformer le circuit eulérien en tournée TSP.

    Le circuit eulérien peut repasser plusieurs fois par une même ville.

    Pour obtenir une tournée du voyageur de commerce,
    on garde uniquement la première visite de chaque ville.
    """

    # On calcule le circuit eulérien à partir du sommet de départ.
    euler_circuit = list(
        nx.eulerian_circuit(
            eulerian_graph,
            source=start,
        )
    )

    # On reconstruit la suite des sommets parcourus.
    sequence = [start]

    for _, destination in euler_circuit:
        sequence.append(destination)

    # Cette liste contiendra la tournée finale sans doublons.
    route = []

    # Ce set permet de mémoriser les villes déjà visitées.
    visited = set()

    # On garde une ville uniquement lors de sa première apparition.
    for city in sequence:
        if city not in visited:
            route.append(city)
            visited.add(city)

    return route, euler_circuit


def christofides(graph, start=0):
    """
    Lance l'algorithme complet de Christofides.

    HISTOIRE COMPLÈTE :

    graphe complet
        ↓
    MST
        ↓
    sommets impairs
        ↓
    matching minimum
        ↓
    multigraphe eulérien
        ↓
    circuit eulérien
        ↓
    suppression des passages répétés
        ↓
    tournée finale
    """

    # Sécurité : le graphe doit contenir des villes.
    if graph.number_of_nodes() == 0:
        raise ValueError("Le graphe est vide.")

    # Sécurité : la ville de départ doit exister.
    if start not in graph:
        raise ValueError(
            f"Le sommet de départ {start} n'existe pas."
        )

    # ---------------------------------------------------------
    # ÉTAPE 1 : construire l'arbre couvrant minimum.
    # ---------------------------------------------------------
    mst = build_mst(graph)

    # ---------------------------------------------------------
    # ÉTAPE 2 : récupérer les sommets de degré impair.
    # ---------------------------------------------------------
    odd_vertices = find_odd_vertices(mst)

    # ---------------------------------------------------------
    # ÉTAPE 3 : relier ces sommets impairs deux par deux
    # en minimisant la distance ajoutée.
    # ---------------------------------------------------------
    matching = build_minimum_matching(
        graph,
        odd_vertices,
    )

    # ---------------------------------------------------------
    # ÉTAPE 4 : fusionner MST + matching.
    # Le graphe devient eulérien.
    # ---------------------------------------------------------
    eulerian_graph = build_eulerian_multigraph(
        graph,
        mst,
        matching,
    )

    # Vérification de sécurité :
    # tous les sommets doivent avoir un degré pair.
    if not nx.is_eulerian(eulerian_graph):
        raise RuntimeError(
            "Le multigraphe obtenu n'est pas eulérien."
        )

    # ---------------------------------------------------------
    # ÉTAPE 5 : construire le circuit eulérien puis
    # supprimer les villes déjà visitées.
    # ---------------------------------------------------------
    route, euler_circuit = euler_to_hamiltonian(
        eulerian_graph,
        start=start,
    )

    # ---------------------------------------------------------
    # ÉTAPE 6 : calculer la distance de la tournée finale.
    # ---------------------------------------------------------
    total_distance = route_distance(
        graph,
        route,
    )

    # Poids total de l'arbre couvrant minimum.
    mst_weight = mst.size(
        weight="weight",
    )

    # Somme des distances ajoutées par le matching.
    matching_weight = sum(
        graph[u][v]["weight"]
        for u, v in matching
    )

    # On rassemble tous les résultats dans un seul objet.
    return ChristofidesResult(
        route=route,
        total_distance=total_distance,
        mst_weight=mst_weight,
        odd_vertices=odd_vertices,
        matching=matching,
        matching_weight=matching_weight,
        eulerian_edge_count=len(euler_circuit),
    )
