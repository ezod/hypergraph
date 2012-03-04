"""\
Hypergraph - search algorithms.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: LGPL-3
"""

def breadth_first_search(H, start):
    """\
    Breadth-first search generator. Yields vertices as they are reached.

    @param H: The input hypergraph.
    @type H: L{Hypergraph}
    @param start: The start vertex.
    @type start: C{object}
    """
    yield start
    marked = set([start])
    Q = [start]
    while Q:
        v = Q.pop(0)
        for edge in H.incident(v, forward=False):
            for w in ([edge.head] if H.directed else edge):
                if not w in marked:
                    marked.add(w)
                    Q.append(w)
                    yield w


def depth_first_search(H, start, marked=None):
    """\
    Depth-first search generator. Yields vertices as they are reached, along
    with the path over which each was reached (a list of tuples containing the
    next edge in the path and the destination vertex).

    @param H: The input hypergraph.
    @type H: L{Hypergraph}
    @param marked: The initial set of marked vertices (for internal use).
    @type marked: C{set}
    @param start: The start vertex.
    @type start: C{object}
    """
    if marked is None:
        yield start
        marked = set()
    marked.add(start)
    for edge in H.incident(start, forward=False):
        if not edge in marked:
            for w in ([edge.head] if H.directed else edge):
                if not w in marked:
                    yield w
                    for y in depth_first_search(H, w, marked=marked):
                        yield y
