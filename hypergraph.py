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
    def __new__(cls, edge, head=None):
        """\
        Constructor. Verifies the immutability of the vertices.

        @param edge: Initializing iterable.
        @type edge: C{object}
        @param head: Head vertex (optional).
        @type head: C{object}
        """
        try:
            assert all([vertex.__hash__ for vertex in edge])
        except (AttributeError, AssertionError):
            raise TypeError('vertices must be immutable')
        if not edge:
            raise ValueError('edge must contain at least one vertex')
        return frozenset.__new__(cls, edge)

    def __init__(self, edge, head=None):
        """\
        Constructor. Verifies and sets the head vertex if applicable.

        @param edge: Initializing iterable.
        @type edge: C{object}
        @param head: Head vertex (optional).
        @type head: C{object}
        """
        try:
            assert not head or head in self
        except AssertionError:
            raise ValueError('edge has no vertex %s' % head)
        self._head = head

    def __hash__(self):
        """\
        Hash function.
        """
        return super(Edge, self).__hash__() + \
            (self.head and self.head.__hash__() or 0)

    def __repr__(self):
        """\
        Canonical string representation.
        """
        if self.head:
            return '%s(%s, %s)' % \
                (self.__class__.__name__, list(self), self.head)
        else:
            return super(Edge, self).__repr__()

    __str__ = __repr__

    @property
    def head(self):
        return self._head


class Hypergraph(object):
    """\
    Hypergraph class.
    """
    def __init__(self, vertices=set(), edges=set(), weights={}, directed=False):
        """\
        Constructor.
        """
        self._directed = directed
        try:
            assert all([vertex.__hash__ for vertex in vertices])
        except (AttributeError, AssertionError):
            raise TypeError('vertices must be immutable')
        self._vertices = vertices
        self._weights = {}
        try:
            for edge in edges:
                assert isinstance(edge, Edge)
                assert all([vertex in vertices for vertex in edge])
                assert (not directed and not edge.head) \
                    or (directed and edge.head)
                try:
                    self._weights[edge] = float(weights[edge])
                except KeyError:
                    self._weights[edge] = 1.0
        except AssertionError:
            raise ValueError('invalid edge %s' % edge)
        self._edges = edges

    @property
    def directed(self):
        return self._directed

    @property
    def vertices(self):
        return self._vertices

    @property
    def edges(self):
        return self._edges

    def weight(self, edge):
        """\
        Return the weight of a given edge.

        @param edge: The edge.
        @type edge: L{Edge}
        """
        return self._weights[edge]


class Graph(Hypergraph):
    """\
    Graph (2-uniform hypergraph) class.
    """
    def __init__(self, vertices=set(), edges=set(), weights={}, directed=False):
        """\
        Constructor.
        """
        try:
            assert all([len(edge) == 2 for edge in edges])
        except AssertionError:
            raise ValueError('edges must have exactly two vertices')
        super(Graph, self).__init__(vertices, edges, weights, directed)
