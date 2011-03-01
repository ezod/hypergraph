"""\
Python module for graphs and hypergraphs.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: GPL-3
"""

class Edge(frozenset):
    """\
    Edge class.
    """
    def __new__(cls, edge):
        """\
        Constructor. Verifies the immutability of the vertices.
        """
        try:
            assert all([vertex.__hash__ for vertex in edge])
        except (AttributeError, AssertionError):
            raise TypeError('vertices must be immutable')
        if not edge:
            raise ValueError('edge must contain at least one vertex')
        return frozenset.__new__(cls, edge)

    @property
    def head(self):
        """\
        The head vertex of this edge (if any).
        """
        try:
            return self._head
        except AttributeError:
            self._head = None
            return self._head

    @head.setter
    def head(self, vertex):
        """\
        Set the head vertex of this edge.
        """
        if not vertex in self:
            raise ValueError('edge has no vertex \'%s\'' % vertex)
        self._head = vertex


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
