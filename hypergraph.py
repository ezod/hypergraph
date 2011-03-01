"""\
Python module for graphs and hypergraphs.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: GPL-3
"""

class GraphEdge(tuple):
    """\
    Graph edge class.
    """
    def __new__(cls, edge):
        """\
        Constructor. Verifies the immutability of the vertices.
        """
        try:
            assert all([vertex.__hash__ for vertex in edge])
        except (AttributeError, AssertionError):
            raise TypeError('vertices must be immutable')
        return tuple.__new__(cls, edge)


class Hypergraph(object):
    """\
    Hypergraph class.
    """
    pass


class Graph(Hypergraph):
    """\
    Graph (2-uniform hypergraph) class.
    """
    pass
