"""\
Hypergraph - Dot language support for Graphviz.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: LGPL-3
"""

import pydot


def dot_export(G):
    """\
    Export a graph to PyDot.

    @param G: The graph to export.
    @type G: L{Graph}
    @return: List of PyDot nodes.
    @rtype: C{list} of C{pydot.Node}
    """
    assert G.uniform(2)
    D = pydot.Dot(graph_type=(G.directed and 'digraph' or 'graph'))
    for v in G.vertices:
        D.add_node(pydot.Node(name=str(v), label=str(v)))
    weighted = not all([weight == 1.0 for weight in G.weights.values()])
    for e in G.edges:
        if G.directed:
            tail, head = e.tail.pop(), e.head
        else:
            tail, head = tuple(e)
        if weighted:
            D.add_edge(pydot.Edge(src=str(tail), dst=str(head),
                weight=str(G.weights[e])))
        else:
            D.add_edge(pydot.Edge(src=str(tail), dst=str(head)))
    return D.to_string()
