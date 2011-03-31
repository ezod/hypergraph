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
    Return the degree matrix of a hypergraph. For directed hypergraphs,
    considers the indegree.

    @param H: The input hypergraph.
    @type H: L{Hypergraph}
    @param weighted: Return the weighted degree matrix if true.
    @type weighted: C{bool}
    @return: The degree matrix.
    @rtype: C{numpy.ndarray}
    """
    return numpy.diag([H.indegree(v, weighted=weighted) \
        for v in sorted(list(H.vertices))])


def adjacency_matrix(G):
    """\
    Return the adjacency matrix of a graph. For directed graphs, considers the
    indegree adjacency (incidence).

    @param G: The input graph.
    @type G: L{Graph}
    @return: The adjacency matrix.
    @rtype: C{numpy.ndarray}
    """
    try:
        assert G.uniform(2)
    except AssertionError:
        raise ValueError('function can only be applied to 2-uniform graphs')
    V = sorted(list(G.vertices))
    adjacency = numpy.zeros((len(V), len(V)))
    for u in range(len(V)):
        for v in range(len(V)):
            adjacency[u][v] = int(G.incident(V[u], V[v]))
    return adjacency


def incidence_matrix(H):
    """\
    Return the incidence matrix of a hypergraph.

    @param H: The input directed hypergraph.
    @type H: L{Hypergraph}
    @return: The adjacency matrix.
    @rtype: C{numpy.ndarray}
    """
    try:
        assert H.directed
    except AssertionError:
        raise ValueError('function can only be applied to directed hypergraphs')
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
