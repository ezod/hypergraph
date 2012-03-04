"""\
Hypergraph - core classes.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: LGPL-3
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
        @raise TypeError: One or more vertices are not immutable.
        @raise ValueError: No vertices given.
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
        @raise ValueError: Specified head vertex not in edge.
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
            (self.head.__hash__() if self.head else 0)

    def __eq__(self, other):
        """\
        Equality operator.
        """
        return frozenset.__eq__(self, other) and self.head is other.head

    def __repr__(self):
        """\
        Canonical string representation.
        """
        if self.head:
            return '%s(%s, \'%s\')' % \
                (type(self).__name__, list(self), self.head)
        else:
            return super(Edge, self).__repr__()

    @property
    def head(self):
        """\
        Edge head.

        @rtype: C{object}
        """
        return self._head

    @property
    def tail(self):
        """\
        Edge tail set.

        @rtype: C{set}
        """
        return set(self) - set([self._head])


class Hypergraph(object):
    """\
    Hypergraph class.
    """
    def __init__(self, vertices=None, edges=None, weights=None, directed=False):
        """\
        Constructor.

        @param vertices: Initial set of vertices.
        @type vertices: C{set}
        @param edges: Initial set of edges.
        @type edges: C{set}
        @param weights: Initial weight relation.
        @type weights: C{dict}
        @param directed: Directedness of this hypergraph.
        @type directed: C{bool}
        @raise TypeError: One or more vertices are not immutable.
        @raise ValueError: One or more edges are not valid for this hypergraph.
        """
        vertices = set(vertices) if vertices else set()
        edges = set(edges) if edges else set()
        self._directed = directed
        try:
            assert all([vertex.__hash__ for vertex in vertices])
        except (AttributeError, AssertionError):
            raise TypeError('vertices must be immutable')
        self._vertices = vertices
        self.weights = {}
        try:
            for edge in edges:
                assert isinstance(edge, Edge)
                assert (not directed and not edge.head) \
                    or (directed and edge.head)
                try:
                    self.weights[edge] = float(weights[edge])
                except (KeyError, TypeError):
                    self.weights[edge] = 1.0
        except AssertionError:
            raise ValueError('invalid edge %s' % edge)
        except TypeError:
            pass
        self._vertices.update(*edges)
        self._edges = edges

    def __eq__(self, other):
        """\
        Equality operator.

        @rtype: C{bool}
        """
        return self.vertices == other.vertices and self.edges == other.edges \
            and all([abs(self.weights[edge] - other.weights[edge]) < 1e-4 \
            for edge in self.edges])

    def __repr__(self):
        """\
        Canonical string representation.

        @rtype: C{str}
        """
        return '%s(vertices=%s, edges=%s, weights=%s, directed=%s)' % \
            (type(self).__name__, self.vertices, self.edges, self.weights,
             self.directed)

    def add_vertex(self, vertex):
        """\
        Add a vertex to this hypergraph.

        @param vertex: The vertex object to add.
        @type vertex: C{object}
        @raise TypeError: Vertex object is not immutable.
        """
        try:
            assert vertex.__hash__
        except (AttributeError, AssertionError):
            raise TypeError('vertex must be immutable')
        self._vertices.add(vertex)

    def remove_vertex(self, vertex):
        """\
        Remove a vertex and all incident edges from this hypergraph.

        @param vertex: The vertex object to remove.
        @type vertex: C{object}
        """
        edges = set(self.edges)
        for edge in edges:
            if vertex in edge:
                self.remove_edge(edge)
        self._vertices.remove(vertex)

    def add_edge(self, edge, weight=1.0):
        """\
        Add an edge to this hypergraph.

        @param edge: The edge to add.
        @type edge: L{Edge}
        @param weight: The weight of the edge.
        @type weight: C{float}
        @raise ValueError: Edge is not valid for this hypergraph.
        """
        try:
            assert isinstance(edge, Edge)
            assert (not self.directed and not edge.head) \
                or (self.directed and edge.head)
        except AssertionError:
            raise ValueError('invalid edge %s' % edge)
        self._vertices.update(edge)
        self._edges.add(edge)
        self.weights[edge] = weight

    def remove_edge(self, edge):
        """\
        Remove an edge from this hypergraph.

        @param edge: The edge to add.
        @type edge: L{Edge}
        """
        del self.weights[edge]
        self._edges.remove(edge)

    @property
    def directed(self):
        """\
        Directedness of the hypergraph.

        @rtype: C{bool}
        """
        return self._directed

    @property
    def vertices(self):
        """\
        Vertex set of the hypergraph.

        @rtype: C{set}
        """
        return self._vertices

    @property
    def edges(self):
        """\
        Edge set of the hypergraph.

        @rtype: C{set}
        """
        return self._edges

    def uniform(self, k=None):
        """\
        Return whether this is a k-uniform hypergraph.

        @param k: The value of k (optional).
        @type k: C{int}
        @return: Uniformity.
        @rtype: C{bool}
        """
        if k is None:
            k = len(iter(self.edges).next())
        return all([len(edge) == k for edge in self.edges])

    def regular(self, d=None):
        """\
        Return whether this is a d-regular hypergraph.

        @param d: The value of d (optional).
        @type d: C{int}
        @return: Regularity.
        @rtype: C{bool}
        """
        if d is None:
            d = self.degree(iter(self.vertices).next())
        return all([self.degree(vertex) == d for vertex in self.vertices])

    def adjacent(self, u, v):
        """\

        @param u: The first vertex.
        @type u: C{object}
        @param v: The second vertex.
        @type v: C{object}
        @return: A set of 
        @rtype: C{set} of L{Edge}
        """
        if u == v:
            return set()
        return set([edge for edge in self.edges if u in edge and v in edge])

    def incident(self, v, forward=True):
        """\
        Return a set of edges incident on a vertex. In an undirected hypergraph,
        this returns every edge containing the specified vertex (and the
        forward parameter has no effect). In a directed hypergraph, by default,
        this returns edges with the specified head vertex; if the forward
        parameter is set to False, it returns edges for which the specified
        vertex is a tail vertex.

        @param v: The vertex.
        @type v: C{object}
        @param forward: Direction of incidence.
        @type forward: C{bool}
        @return: A set of incident edges.
        @rtype: C{set} of L{Edge}
        """
        if forward and self.directed:
            return set([edge for edge in self.edges if edge.head == v])
        else:
            return set([edge for edge in self.edges \
                if v in edge and edge.head != v])

    def reachable(self, tail, head):
        """\
        Return a set of edges which contain the tail vertex and are directed
        into the head vertex.

        @param tail: The tail vertex.
        @type tail: C{object}
        @param head: The head vertex.
        @type head: C{object}
        @return: A set of edges from tail to head.
        @rtype: C{set} of L{Edge}
        """
        if self.directed:
            return self.adjacent(tail, head) & self.incident(head)
        else:
            return self.adjacent(tail, head)

    def neighbors(self, vertex):
        """\
        Return the set of vertices which are adjacent (in an undirected
        hypergraph) or incident (in a directed hypergraph) to a given vertex.

        @param vertex: The vertex.
        @type vertex: C{object}
        @return: The set of vertices adjacent to the vertex.
        @rtype: C{set}
        """
        return set([v for v in self.vertices if self.reachable(vertex, v)])

    def degree(self, vertex, weighted=True):
        """\
        Return the (weighted) degree of the given vertex.

        @param vertex: The vertex.
        @type vertex: C{object}
        @param weighted: Return the weighted degree if true.
        @type weighted: C{bool}
        @return: Degree of the vertex.
        @rtype: C{float}
        """
        return sum([self.weights[edge] if weighted else 1 for edge \
            in self.edges if vertex in edge])

    def indegree(self, vertex, weighted=True):
        """\
        Return the (weighted) indegree of the given vertex.

        @param vertex: The vertex.
        @type vertex: C{object}
        @param weighted: Return the weighted indegree if true.
        @type weighted: C{bool}
        @return: Indegree of the vertex.
        @rtype: C{float}
        """
        if not self.directed:
            return self.degree(vertex, weighted)
        return sum([self.weights[edge] if weighted else 1 for edge \
            in self.edges if edge.head == vertex])
        
    def outdegree(self, vertex, weighted=True):
        """\
        Return the (weighted) outdegree of the given vertex.

        @param vertex: The vertex.
        @type vertex: C{object}
        @param weighted: Return the weighted outdegree if true.
        @type weighted: C{bool}
        @return: Outdegree of the vertex.
        @rtype: C{float}
        """
        if not self.directed:
            return self.degree(vertex, weighted)
        return sum([self.weights[edge] if weighted else 1 for edge \
            in self.edges if vertex in edge and edge.head != vertex])
        

class Graph(Hypergraph):
    """\
    Graph (2-uniform hypergraph) class.
    """
    def __init__(self, vertices=None, edges=None, weights=None, directed=False):
        """\
        Constructor.

        @param vertices: Initial set of vertices.
        @type vertices: C{set}
        @param edges: Initial set of edges.
        @type edges: C{set}
        @param weights: Initial weight relation.
        @type weights: C{dict}
        @param directed: Directedness of this graph.
        @type directed: C{bool}
        @raise ValueError: Initial edges are not 2-uniform.
        """
        try:
            assert all([len(edge) == 2 for edge in edges])
        except AssertionError:
            raise ValueError('edges must have exactly two vertices')
        except TypeError:
            pass
        super(Graph, self).__init__(vertices, edges, weights, directed)

    def uniform(self, k=None):
        """\
        Return whether this is a k-uniform hypergraph.

        @param k: The value of k (optional).
        @type k: C{int}
        @return: Uniformity.
        @rtype: C{bool}
        """
        return k is None or k == 2
