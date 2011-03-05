"""\
Python module for graphs and hypergraphs.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: GPL-3
"""

from copy import copy
from random import sample


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

        @param vertices: Initial set of vertices.
        @type vertices: C{set}
        @param edges: Initial set of edges.
        @type edges: C{set}
        @param weights: Initial weight relation.
        @type weights: C{dict}
        @param directed: Directedness of this hypergraph.
        @type directed: C{bool}
        """
        self._directed = directed
        try:
            assert all([vertex.__hash__ for vertex in vertices])
        except (AttributeError, AssertionError):
            raise TypeError('vertices must be immutable')
        self._vertices = copy(vertices)
        self.weights = {}
        try:
            for edge in edges:
                assert isinstance(edge, Edge)
                assert all([vertex in vertices for vertex in edge])
                assert (not directed and not edge.head) \
                    or (directed and edge.head)
                try:
                    self.weights[edge] = float(weights[edge])
                except KeyError:
                    self.weights[edge] = 1.0
        except AssertionError:
            raise ValueError('invalid edge %s' % edge)
        self._edges = copy(edges)

    def __repr__(self):
        """\
        Canonical string representation.
        """
        return '%s(vertices=%s, edges=%s, weights=%s, directed=%s)' % \
            (self.__class__.__name__, self.vertices, self.edges, self.weights,
             self.directed)

    def add_vertex(self, vertex):
        """\
        Add a vertex to this hypergraph.

        @param vertex: The vertex object to add.
        @type vertex: C{object}
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
        for edge in self.edges():
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
        """
        try:
            assert isinstance(edge, Edge)
            assert all([vertex in self.vertices for vertex in edge])
            assert (not self.directed and not edge.head) \
                or (self.directed and edge.head)
        except AssertionError:
            raise ValueError('invalid edge %s' % edge)
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
        return self._directed

    @property
    def vertices(self):
        return self._vertices

    @property
    def edges(self):
        return self._edges

    def uniform(self, k):
        """\
        Return whether this is a k-uniform hypergraph.

        @param k: The value of k.
        @type k: C{int}
        @return: Uniformity.
        @rtype: C{bool}
        """
        return all([len(edge) == k for edge in self.edges])

    def adjacent(self, u, v):
        """\
        Return whether two vertices are adjacent (directly connected by an
        edge).

        @param u: The first vertex.
        @type u: C{object}
        @param v: The second vertex.
        @type v: C{object}
        @return: Adjacency.
        @rtype: C{bool}
        """
        # TODO: should this check for edge direction?
        return any([(u in edge and v in edge) for edge in self.edges])

    def neighbors(self, vertex):
        """\
        Return the set of vertices which are adjacent to a given vertex.

        @param vertex: The vertex.
        @type vertex: C{object}
        @return: The set of vertices adjacent to the vertex.
        @rtype: C{set}
        """
        return set([v for v in self.vertices if self.adjacent(vertex, v)]) \
            - set([vertex])

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
        return sum([weighted and self.weights[edge] or 1 for edge \
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
        return sum([weighted and self.weights[edge] or 1 for edge \
            in self.edges if edge.head is vertex])
        
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
        return sum([weighted and self.weights[edge] or 1 for edge \
            in self.edges if vertex in edge and edge.head is not vertex])
        

class Graph(Hypergraph):
    """\
    Graph (2-uniform hypergraph) class.
    """
    def __init__(self, vertices=set(), edges=set(), weights={}, directed=False):
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
        """
        try:
            assert all([len(edge) == 2 for edge in edges])
        except AssertionError:
            raise ValueError('edges must have exactly two vertices')
        super(Graph, self).__init__(vertices, edges, weights, directed)

    def uniform(self, k):
        """\
        Return whether this is a k-uniform hypergraph.

        @param k: The value of k.
        @type k: C{int}
        """
        return k == 2


def minimum_maximum_indegree(H):
    """\
    Find a minimum maximum indegree orientation of an unweighted hypergraph.
    Adapted from a graph algorithm by Asahiro et al. for finding a minimum
    maximum outdegree orientation.

    Y. Asahiro, E. Miyano, H. Ono, and K. Zenmyo, "Graph Orientation Algorithms
    To Minimize the Maximum Outdegree," Int. J. Foundations of Computer Science,
    vol. 18, pp. 197-215, 2007.
    
    @param H: The input unweighted hypergraph.
    @type H: L{Hypergraph}
    @return: A minimum maximum indegree orientation of the hypergraph.
    @rtype: L{Hypergraph}
    """
    def find_reducing_path(L, D, u):
        """\
        Find a directed hyperpath which, if reversed, reduces the indegree of
        the specified vertex. This replaces Step 3 of Asahiro et al.'s Reverse
        algorithm.

        @param L: The input directed hypergraph.
        @type L: L{Hypergraph}
        @param D: A dictionary relating vertices to their indegrees.
        @type D: C{dict}
        @param u: The vertex.
        @type u: C{object}
        """
        # generate a set of possible endpoints for the path
        targets = [v for v in D.keys() if D[v] < D[u] - 1]
        # initialize the breadth-first search
        marked = set([u])
        Q = [(u, [])]
        # breadth-first search for a directed path to an endpoint
        while Q:
            v, path = Q.pop()
            for edge in [edge for edge in L.edges if edge.head is v]:
                for w in edge:
                    if w in marked:
                        continue
                    elif w in targets:
                        path.append((edge, w))
                        return path
                    else:
                        marked.add(w)
                        Q.append((w, path + [(edge, w)]))
        return None

    # generate L, an arbitrary orientation of H
    L = Hypergraph(vertices=H.vertices, directed=True)
    for edge in H.edges:
        L.add_edge(Edge(edge, head=sample(edge, 1)[0]))
    while True:
        # compute the indegree of each vertex in L
        degrees = dict((v, L.indegree(v, weighted=False)) for v in L.vertices)
        # find the vertex with maximum indegree
        degrees_rev = dict(map(lambda v: (v[1], v[0]), degrees.items()))
        vmax = degrees_rev[max(degrees_rev.keys())]
        # find a directed path which can reduce the degree of vmax
        path = find_reducing_path(L, degrees, vmax)
        # if no such path exists, return L
        if not path:
            break
        # otherwise, reverse the directed path and continue
        for edge, vertex in path:
            L.remove_edge(edge)
            L.add_edge(Edge(edge, head=vertex))
    return L
