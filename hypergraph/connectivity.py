"""\
Hypergraph - connectivity properties.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: LGPL-3
"""

from itertools import combinations

from .matrix import laplacian_matrix, laplacian_eigenvalues


def connected(H):
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


def edge_cut(H, X):
    """\
    Return the edge cut (coboundary) of a set with respect to a hypergraph.

    @param H: The hypergraph.
    @type H: L{Hypergraph}
    @param X: The vertex subset.
    @type X: C{set}
    @return: The edge cut of X with respect to H.
    @rtype: C{set}
    @raise ValueError: X is not a subset of the vertices of H.
    """
    try:
        assert X.issubset(H.vertices)
    except AssertionError:
        raise ValueError('set is not a subset of the hypergraph vertices')
    Y = H.vertices - X
    EX = set()
    for edge in H.edges:
        for u, v in combinations(edge, 2):
            if u in X and not u in Y and v in Y and not v in X:
                EX.add(edge)
                break
    return EX


def isoperimetric_number(H):
    """\
    Return the isoperimetric number (Cheeger constant) of a hypergraph.

        - J. A. Rodriguez, "Laplacian Eigenvalues and Partition Problems in
          Hypergraphs," Applied Mathematics Letters, vol. 22, no. 6, pp.
          916-921, 2009.

    @param H: The hypergraph.
    @type H: L{Hypergraph}
    @return: The isoperimetric number of H.
    @rtype: C{float}
    """
    i = float('inf')
    for n in range(1, int(len(H.vertices) / 2) + 1):
        for X in combinations(H.vertices, n):
            ex = len(edge_cut(H, set(X)))
            if ex / n < i:
                i = ex / n
    return i
