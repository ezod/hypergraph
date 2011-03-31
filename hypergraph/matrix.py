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


def incidence_matrix(H):
    """\
    Return the incidence matrix of a graph.

    @param H: The input directed hypergraph.
    @type H: L{Hypergraph}
    @return: The adjacency matrix.
    @rtype: C{numpy.ndarray}
    """
    assert H.directed
    V = sorted(list(H.vertices))
    E = sorted(list(H.edges))
    dV = {}
    for i in range(len(V)):
        dV[V[i]] = i
    incidence = numpy.zeros((len(V), len(E)))
    for e in range(len(E)):
        incidence[dV[E[e].head]][e] = 1
        for v in E[e].tail:
            incidence[dV[v]][e] = -1
    return incidence
