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

    @param G: The input hypergraph.
    @type G: L{Hypergraph}
    @param weighted: Return the weighted degree matrix if true.
    @type weighted: C{bool}
    @return: The degree matrix.
    @rtype: C{numpy.ndarray}
    """
    return numpy.diag([H.degree(v, weighted=weighted) \
        for v in sorted(list(H.vertices))])
