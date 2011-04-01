"""\
Hypergraph - search algorithms.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: LGPL-3
"""

def breadth_first_search(H, start):
    """\
    Breadth-first search generator. Yields vertices as they are reached, along
    with the path over which it was reached (a list of tuples containing the
    next edge in the path and the destination vertex).

    @param H: The input hypergraph.
    @type H: L{Hypergraph}
    """
    marked = set([start])
    Q = [(start, [])]
    while Q:
        v, path = Q.pop()
        for edge in H.incident(v):
            for w in edge:
                if not w in marked:
                    marked.add(w)
                    Q.append((w, path + [(edge, w)]))
                    yield w, path + [(edge, w)]
