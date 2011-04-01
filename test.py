#!/usr/bin/env python

"""\
Unit tests for hypergraph.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: LGPL-3
"""

import unittest

from hypergraph import *
from hypergraph.matrix import *
from hypergraph.orientation import *
from hypergraph.path import *


class TestCore(unittest.TestCase):

    def setUp(self):
        V = set(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'])
        self.U = Hypergraph(vertices=V)
        self.U.add_edge(Edge(['A', 'D', 'C', 'I', 'G', 'H', 'B']), weight=9.805444)
        self.U.add_edge(Edge(['E', 'D', 'F', 'A']), weight=7.944848)
        self.U.add_edge(Edge(['F', 'B', 'C']), weight=5.238859)
        self.U.add_edge(Edge(['D', 'E', 'J']), weight=2.182849)
        self.U.add_edge(Edge(['B', 'C', 'E', 'A', 'I', 'G', 'F']), weight=1.700069)
        self.U.add_edge(Edge(['I', 'H', 'G', 'J', 'C', 'D']), weight=7.809860)
        self.U.add_edge(Edge(['G', 'F', 'E']), weight=8.340940)
        self.U.add_edge(Edge(['D', 'G', 'E', 'H', 'F', 'C', 'B', 'A', 'I']), weight=6.847455)
        self.U.add_edge(Edge(['J', 'C', 'H', 'B', 'F', 'D', 'E', 'A']), weight=9.601762)
        self.U.add_edge(Edge(['J', 'D', 'G']), weight=2.771911)
        self.U.add_edge(Edge(['F', 'G', 'I', 'H']), weight=9.884923)
        self.U.add_edge(Edge(['D']), weight=1.910802)
        self.U.add_edge(Edge(['C', 'J', 'H', 'E', 'G', 'F', 'A', 'I', 'D', 'B']), weight=2.443810)
        self.U.add_edge(Edge(['A', 'G']), weight=9.445038)
        self.U.add_edge(Edge(['G', 'H', 'D', 'I', 'A', 'J', 'E', 'B', 'F']), weight=0.320235)
        self.U.add_edge(Edge(['I', 'D']), weight=4.417088)
        self.U.add_edge(Edge(['E', 'G', 'I']), weight=5.241375)
        self.U.add_edge(Edge(['B', 'J', 'A', 'H']), weight=5.715912)
        self.U.add_edge(Edge(['I', 'D', 'E', 'B']), weight=4.940382)
        self.U.add_edge(Edge(['H', 'C', 'I']), weight=2.983528)
        self.D = Hypergraph(vertices=V, directed=True)
        self.D.add_edge(Edge(['A', 'G'], 'A'), weight=9.445038)
        self.D.add_edge(Edge(['A', 'C', 'B', 'E', 'D', 'G', 'F', 'I', 'H', 'J'], 'J'), weight=2.443810)
        self.D.add_edge(Edge(['I', 'H', 'G', 'F'], 'F'), weight=9.884923)
        self.D.add_edge(Edge(['J', 'E', 'D'], 'D'), weight=2.182849)
        self.D.add_edge(Edge(['I', 'B', 'E', 'D'], 'B'), weight=4.940382)
        self.D.add_edge(Edge(['C', 'D', 'G', 'I', 'H', 'J'], 'G'), weight=7.809860)
        self.D.add_edge(Edge(['D'], 'D'), weight=1.910802)
        self.D.add_edge(Edge(['A', 'C', 'B', 'E', 'G', 'F', 'I'], 'E'), weight=1.700069)
        self.D.add_edge(Edge(['J', 'D', 'G'], 'G'), weight=2.771911)
        self.D.add_edge(Edge(['E', 'G', 'F'], 'F'), weight=8.340940)
        self.D.add_edge(Edge(['I', 'H', 'C'], 'C'), weight=2.983528)
        self.D.add_edge(Edge(['C', 'B', 'F'], 'C'), weight=5.238859)
        self.D.add_edge(Edge(['A', 'C', 'B', 'D', 'G', 'I', 'H'], 'I'), weight=9.805444)
        self.D.add_edge(Edge(['A', 'E', 'D', 'F'], 'A'), weight=7.944848)
        self.D.add_edge(Edge(['A', 'H', 'B', 'J'], 'H'), weight=5.715912)
        self.D.add_edge(Edge(['A', 'B', 'E', 'D', 'G', 'F', 'I', 'H', 'J'], 'B'), weight=0.320235)
        self.D.add_edge(Edge(['I', 'E', 'G'], 'I'), weight=5.241375)
        self.D.add_edge(Edge(['I', 'D'], 'I'), weight=4.417088)
        self.D.add_edge(Edge(['A', 'C', 'B', 'E', 'D', 'G', 'F', 'I', 'H'], 'E'), weight=6.847455)
        self.D.add_edge(Edge(['A', 'C', 'B', 'E', 'D', 'F', 'H', 'J'], 'D'), weight=9.601762)

    def test_equal_repr(self):
        self.assertEqual(Hypergraph(), Hypergraph())
        self.assertEqual(Graph(), Graph())
        G = Hypergraph(vertices=self.U.vertices, edges=self.U.edges, weights=self.U.weights, directed=False)
        self.assertEqual(G, self.U)
        H = eval('%s' % self.U)
        self.assertEqual(H, self.U)

    def test_remove_vertex(self):
        self.U.remove_vertex('I')
        self.assertFalse('I' in self.U.vertices)
        self.assertFalse(Edge(['I', 'D']) in self.U.edges)
        self.assertFalse(Edge(['I', 'D']) in self.U.weights.keys())

    def test_add_edge(self):
        self.assertRaises(ValueError, self.U.add_edge, Edge(['A', 'Z']))

    def test_remove_edge(self):
        self.U.remove_edge(Edge(['I', 'D']))
        self.assertFalse(Edge(['I', 'D']) in self.U.edges)
        self.assertFalse(Edge(['I', 'D']) in self.U.weights.keys())

    def test_adjacent(self):
        self.assertTrue(self.U.adjacent('A', 'G'))

    def test_reachable(self):
        self.assertFalse(self.D.reachable('A', 'G'))
        self.assertTrue(self.D.reachable('G', 'A'))
        self.assertTrue(self.D.reachable('E', 'D'))

    def test_neighbors(self):
        self.assertEqual(self.U.neighbors('I'), set(['A', 'C', 'B', 'E', 'D', 'G', 'F', 'H', 'J']))
        self.assertEqual(self.D.neighbors('I'), set(['C', 'B', 'E', 'G', 'F', 'J']))

    def test_degree(self):
        self.assertEqual(self.U.degree('I', weighted=False), 11)
        self.assertEqual(self.D.indegree('I', weighted=False), 3)
        self.assertEqual(self.D.outdegree('I', weighted=False), 8)


class TestMatrix(unittest.TestCase):

    def setUp(self):
        V = set(['A', 'B', 'C', 'D', 'E', 'F', 'G'])
        self.GU = Graph(vertices=V, directed=False)
        self.GU.add_edge(Edge(['A', 'B']))
        self.GU.add_edge(Edge(['A', 'F']))
        self.GU.add_edge(Edge(['B', 'C']))
        self.GU.add_edge(Edge(['B', 'E']))
        self.GU.add_edge(Edge(['B', 'G']))
        self.GU.add_edge(Edge(['C', 'D']))
        self.GU.add_edge(Edge(['C', 'E']))
        self.GU.add_edge(Edge(['D', 'E']))
        self.GU.add_edge(Edge(['E', 'G']))
        self.GU.add_edge(Edge(['F', 'G']))
        self.GD = Graph(vertices=V, directed=True)
        self.GD.add_edge(Edge(['A', 'B'], head='A'))
        self.GD.add_edge(Edge(['A', 'F'], head='F'))
        self.GD.add_edge(Edge(['B', 'C'], head='B'))
        self.GD.add_edge(Edge(['B', 'E'], head='E'))
        self.GD.add_edge(Edge(['B', 'G'], head='G'))
        self.GD.add_edge(Edge(['C', 'D'], head='C'))
        self.GD.add_edge(Edge(['C', 'E'], head='C'))
        self.GD.add_edge(Edge(['D', 'E'], head='D'))
        self.GD.add_edge(Edge(['E', 'G'], head='E'))
        self.GD.add_edge(Edge(['F', 'G'], head='F'))
        self.HU = Hypergraph(vertices=V, directed=False)
        self.HU.add_edge(Edge(['A', 'B']))
        self.HU.add_edge(Edge(['A', 'E', 'F']))
        self.HU.add_edge(Edge(['B', 'C', 'D', 'G']))
        self.HU.add_edge(Edge(['B', 'E']))
        self.HU.add_edge(Edge(['B', 'G']))
        self.HU.add_edge(Edge(['C', 'D', 'F']))
        self.HU.add_edge(Edge(['C', 'E']))
        self.HU.add_edge(Edge(['D']))
        self.HU.add_edge(Edge(['E', 'G']))
        self.HU.add_edge(Edge(['F', 'G']))

    def test_degree_matrix(self):
        self.assertTrue(numpy.all(degree_matrix(self.GU) == numpy.diag([2, 4, 3, 2, 4, 2, 3])))
        self.assertTrue(numpy.all(degree_matrix(self.GD) == numpy.diag([1, 1, 2, 1, 2, 2, 1])))

    def test_laplacian_eigenvalues(self):
        eLGU = laplacian_eigenvalues(laplacian_matrix(self.GU))
        eLHU = laplacian_eigenvalues(laplacian_matrix(self.HU))
        self.assertTrue(abs(eLGU[0]) < 1e-8)
        self.assertTrue(abs(eLHU[0]) < 1e-8)
        self.assertFalse(abs(eLGU[1]) < 1e-8)
        self.assertFalse(abs(eLHU[1]) < 1e-8)
        self.GU.add_vertex('H')
        self.GU.add_vertex('I')
        self.GU.add_edge(Edge(['H', 'I']))
        self.HU.add_vertex('H')
        self.HU.add_vertex('I')
        self.HU.add_edge(Edge(['H', 'I']))
        self.assertTrue(abs(laplacian_eigenvalues(laplacian_matrix(self.GU))[1]) < 1e-8)
        self.assertTrue(abs(laplacian_eigenvalues(laplacian_matrix(self.HU))[1]) < 1e-8)

class TestPath(unittest.TestCase):

    def setUp(self):
        V = set([1, 2, 3, 4, 5])
        self.U = Graph(vertices=V, directed=False)
        self.D = Graph(vertices=V, directed=True)
        for G in [self.U, self.D]:
            G.add_edge(Edge([1, 2], head=(G.directed and 2 or None)), weight=1.25)
            G.add_edge(Edge([2, 3], head=(G.directed and 3 or None)), weight=1)
            G.add_edge(Edge([3, 4], head=(G.directed and 4 or None)), weight=1.11)
            G.add_edge(Edge([4, 5], head=(G.directed and 5 or None)), weight=1.43)
            G.add_edge(Edge([3, 5], head=(G.directed and 5 or None)), weight=10)
            G.add_edge(Edge([5, 2], head=(G.directed and 2 or None)), weight=2)
            G.add_edge(Edge([1, 5], head=(G.directed and 5 or None)), weight=100)

    def test_dijkstra(self):
        exp = {1: None, 2: 1, 3: 2, 4: 3, 5: 2}
        act = dijkstra(self.U, 1)
        self.assertEqual(act, exp)
        exp = {1: None, 2: 1, 3: 2, 4: 3, 5: 4}
        act = dijkstra(self.D, 1)
        self.assertEqual(act, exp)

    def test_shortest_path(self):
        ep = [1, 2, 5]
        el = 3.25
        act = shortest_path(self.U, 1, 5)
        self.assertEqual(act, (ep, el))
        ep = [1, 2, 3, 4, 5]
        el = 4.79
        act = shortest_path(self.D, 1, 5)
        self.assertEqual(act, (ep, el))

    def test_floyd_warshall(self):
        self.assertEqual(floyd_warshall(self.U)[1][5], 3.25)
        self.assertEqual(floyd_warshall(self.D)[1][5], 4.79)


if __name__ == '__main__':
    unittest.main()
