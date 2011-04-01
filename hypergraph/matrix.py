"""\
Hypergraph - matrix functions, algebraic and spectral graph theory.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: LGPL-3
"""

import numpy


def degree_matrix(H):
    """\
    Return the degree matrix of a hypergraph. For directed hypergraphs,
    considers the indegree.

    @param H: The input hypergraph.
    @type H: L{Hypergraph}
    @return: The degree matrix.
    @rtype: C{numpy.ndarray}
    """
    return numpy.diag([H.indegree(v) for v in sorted(list(H.vertices))])


def adjacency_matrix(H):
    """\
    Return the adjacency matrix of a hypergraph. For directed hypergraphs,
    considers the indegree adjacency (the column index is associated with the
    head vertex).

    @param H: The input graph.
    @type H: L{Hypergraph}
    @return: The adjacency matrix.
    @rtype: C{numpy.ndarray}
    """
    V = sorted(list(H.vertices))
    adjacency = numpy.zeros((len(V), len(V)))
    for u in range(len(V)):
        for v in range(len(V)):
            adjacency[u][v] = sum([H.weights[edge] \
                for edge in H.reachable(V[u], V[v])])
    return adjacency


def incidence_matrix(H):
    """\
    Return the incidence matrix of a hypergraph.

    @param H: The input hypergraph.
    @type H: L{Hypergraph}
    @return: The adjacency matrix.
    @rtype: C{numpy.ndarray}
    """
    V = sorted(list(H.vertices))
    E = sorted(list(H.edges))
    dV = {}
    for i in range(len(V)):
        dV[V[i]] = i
    incidence = numpy.zeros((len(V), len(E)))
    if H.directed:
        for e in range(len(E)):
            incidence[dV[E[e].head]][e] = 1
            for v in E[e].tail:
                incidence[dV[v]][e] = -1
    else:
        for e in range(len(E)):
            for v in E[e]:
                incidence[dV[v]][e] = 1
    return incidence


def laplacian_matrix(H):
    """\
    Return the Laplacian matrix of a hypergraph.

        - J. A. Rodriguez, "On the Laplacian Eigenvalues and Metric Parameters
          of Hypergraphs," Linear and Multilinear Algebra, vol. 50, no. 1, pp.
          1-14, 2002.

        - J. A. Rodriguez, "On the Laplacian Spectrum and Walk-Regular
          Hypergraphs," Linear and Multilinear Algebra, vol. 51, no. 3, pp.
          285-297, 2003.

    @param H: The input hypergraph.
    @type H: L{Hypergraph}
    @return: The Laplacian matrix.
    @rtype: C{numpy.ndarray}
    """
    A = adjacency_matrix(H)
    return numpy.diag(numpy.sum(A, axis=0)) - A


def laplacian_eigenvalues(L):
    """\
    Return the eigenvalues of a hypergraph Laplacian in ascending order.

    @param L: The hypergraph Laplacian.
    @type L: C{numpy.ndarray}
    @return: The eigenvalues of L.
    @rtype: C{list} of C{float}
    """
    return sorted(numpy.linalg.eigvalsh(L))


def connected_by_laplacian(H):
    """\
    Return whether an undirected hypergraph is connected using the eigenvalues
    of its Laplacian matrix.

    @param H: The input undirected hypergraph.
    @type H: L{Hypergraph}
    @return: Connectivity.
    @rtype: C{bool}
    @raise ValueError: The hypergraph is not undirected.
    """
    try:
        assert not H.directed
    except AssertionError:
        raise ValueError('function only applies to undirected hypergraphs')
    return laplacian_eigenvalues(laplacian_matrix(H))[1] > 0
