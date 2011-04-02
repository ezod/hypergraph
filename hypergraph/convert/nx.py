"""\
Hypergraph - NetworkX graph conversions.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: LGPL-3
"""

import networkx


def networkx_export(G):
    """\
    Export a graph to a NetworkX graph object.

    @param G: The graph to export.
    @type G: L{Graph}
    @return: A NetworkX graph object.
    @rtype: C{networkx.Graph} or C{networkx.DiGraph}
    @raise ValueError: Graph is not 2-uniform.
    """
    try:
        assert G.uniform(2)
    except AssertionError:
        raise ValueError('function can only be applied to 2-uniform graphs')
    if not G.directed:
        nxG = networkx.Graph()
        nxG.add_weighted_edges_from([tuple(edge) + (G.weights[edge],) \
            for edge in G.edges])
    else:
        nxG = networkx.DiGraph()
        for edge in G.edges:
            nxG.add_edge(edge.tail.pop(), edge.head, weight=G.weights[edge])
    return nxG
