"""\
Hypergraph - path algorithms.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: LGPL-3
"""

from .core import Edge


def floyd_warshall(G):
    """\
    Floyd-Warshall algorithm for finding the shortest path lengths between all
    pairs of vertices in a graph.

    @param G: The input graph.
    @type G: L{Graph}
    @return: A two-dimensional dictionary of pairwise shortest path lengths.
    @rtype: C{dict} of C{dict} of C{float}
    """
    path = {}
    for u in G.vertices:
        path[u] = {}
        for v in G.vertices:
            if u == v:
                path[u][v] = 0.0
                continue
            try:
                path[u][v] = G.weights[Edge([u, v])]
            except KeyError:
                path[u][v] = float('inf')
    for w in G.vertices:
        for u in G.vertices:
            for v in G.vertices:
                path[u][v] = min(path[u][v], path[u][w] + path[w][v])
    return path
