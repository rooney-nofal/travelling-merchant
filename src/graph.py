"""Build the complete weighted graph of cities (nodes) and roads (edges)."""
import networkx as nx




def build_graph(cities, distance_matrix):
    """Return a complete NetworkX graph: nodes carry city data, edges carry distances in km."""
    graph = nx.Graph()
    for index, (name, lat, lon) in enumerate(cities):
        graph.add_node(index, name=name, lat=lat, lon=lon)
    n = len(cities)
    for i in range(n):
        for j in range(i + 1, n):
            graph.add_edge(i, j, weight=float(distance_matrix[i][j]))
    return graph


if __name__ == "__main__":
    from cities import load_cities
    from distances import build_distance_matrix

    all_cities = load_cities()
    matrix = build_distance_matrix(all_cities)
    g = build_graph(all_cities, matrix)
    print(f"Nodes: {g.number_of_nodes()}")
    print(f"Edges: {g.number_of_edges()}")
    print(f"Paris node: {g.nodes[0]}")
    print(f"Paris-Marseille edge: {g.edges[0, 1]}") 