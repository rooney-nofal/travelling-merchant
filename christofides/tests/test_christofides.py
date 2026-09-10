"""Tests simples de non-régression du projet Christofides."""
import unittest

from src.christofides import christofides
from src.cities import load_cities
from src.distances import build_distance_matrix
from src.graph import build_graph


class ChristofidesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cities = load_cities()
        cls.matrix = build_distance_matrix(cls.cities)
        cls.graph = build_graph(cls.cities, cls.matrix)
        cls.result = christofides(cls.graph, start=0)

    def test_dataset_contains_20_cities(self):
        self.assertEqual(len(self.cities), 20)

    def test_complete_graph_has_190_edges(self):
        self.assertEqual(self.graph.number_of_edges(), 190)

    def test_route_visits_each_city_once(self):
        self.assertEqual(len(self.result.route), 20)
        self.assertEqual(len(set(self.result.route)), 20)

    def test_mst_has_19_edges(self):
        # Un arbre couvrant sur 20 sommets possède 19 arêtes.
        import networkx as nx
        mst = nx.minimum_spanning_tree(
            self.graph,
            weight="weight",
            algorithm="prim",
        )
        self.assertEqual(mst.number_of_edges(), 19)

    def test_expected_project_metrics(self):
        self.assertAlmostEqual(
            self.result.mst_weight,
            2665.05,
            places=2,
        )
        self.assertEqual(
            len(self.result.odd_vertices),
            12,
        )
        self.assertAlmostEqual(
            self.result.matching_weight,
            1142.03,
            places=2,
        )
        self.assertAlmostEqual(
            self.result.total_distance,
            3445.60,
            places=2,
        )


if __name__ == "__main__":
    unittest.main()
