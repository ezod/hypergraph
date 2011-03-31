"""\
Hypergraph - matrix functions.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: LGPL-3
"""

import numpy


def degree_matrix(H, weighted=True):
    """\
    Return the degree matrix of a hypergraph.

    @param H: The input hypergraph.
    @type H: L{Hypergraph}
    @param weighted: Return the weighted degree matrix if true.
    @type weighted: C{bool}
    @return: The degree matrix.
    @rtype: C{numpy.ndarray}
    """
    return numpy.diag([H.degree(v, weighted=weighted) \
        for v in sorted(list(H.vertices))])


def adjacency_matrix(G):
    """\
    Return the adjacency matrix of a graph.

    @param G: The input graph.
    @type G: L{Graph}
    @return: The adjacency matrix.
    @rtype: C{numpy.ndarray}
    """
    assert G.uniform(2)
    V = sorted(list(G.vertices))
    adjacency = numpy.zeros((len(V), len(V)))
    for u in range(len(V)):
        for v in range(len(V)):
            adjacency[u][v] = int(G.adjacent(V[u], V[v]))
    return adjacency
