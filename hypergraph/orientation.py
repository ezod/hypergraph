"""\
Hypergraph - orientation algorithms.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: LGPL-3
"""

from random import sample
from copy import copy

from .core import Hypergraph, Edge
from .search import breadth_first_search


def random_orientation(H):
    """\
    Return a random orientation of a hypergraph.

    @param H: The input hypergraph.
    @type H: L{Hypergraph}
    @return: A random orientation of the hypergraph.
    @rtype: L{Hypergraph}
    """
    L = Hypergraph(vertices=H.vertices, directed=True)
    for edge in H.edges:
        L.add_edge(Edge(edge, head=sample(edge, 1)[0]))
    L.weights = copy(H.weights)
    return L


def minimum_maximum_indegree_orientation(H):
    """\
    Find a minimum maximum indegree orientation of an unweighted hypergraph.
    Adapted from a graph algorithm by Asahiro et al. for finding a minimum
    maximum outdegree orientation.

        - Y. Asahiro, E. Miyano, H. Ono, and K. Zenmyo, "Graph Orientation
          Algorithms To Minimize the Maximum Outdegree," Int. J. Foundations of
          Computer Science, vol. 18, pp. 197-215, 2007.
    
    @param H: The input unweighted hypergraph.
    @type H: L{Hypergraph}
    @return: A minimum maximum indegree orientation of the hypergraph.
    @rtype: L{Hypergraph}
    """
    def find_reducing_path(L, D, u):
        for w, path in breadth_first_search(L, u):
            if D[w] < D[u] - 1:
                return path
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


def minimum_maximum_weighted_indegree_orientation(H):
    """\
    Approximate a minimum maximum weighted indegree orientation of a weighted
    hypergraph using a local search heuristic. Adapted from an algorithm by
    Piersma and Van Dijk for the R||Cmax scheduling problem (which is a superset
    of the P|Mj|Cmax problem, equivalent to MIO).

        - N. Piersma and W. Van Dijk, "A Local Search Heuristic for Unrelated
          Parallel Machine Scheduling with Efficient Neighborhood Search,"
          Mathematical and Computer Modelling, vol. 24, no. 9, pp. 11-19, 1996.

    @param H: The input hypergraph.
    @type H: L{Hypergraph}
    @return: Approximation of minimum MIO of the hypergraph.
    @rtype: L{Hypergraph}
    """
    class Break(Exception): pass
    L = Hypergraph(vertices=H.vertices, directed=True)
    # starting point
    for edge in H.edges:
        L.add_edge(Edge(edge, head=min([(L.indegree(v), v) for v in edge])[1]),
            weight=H.weights[edge])
    # search NR
    accepted = True
    while accepted:
        accepted = False
        vmax = max([(L.indegree(v), v) for v in L.vertices])[1]
        Emax = set([edge for edge in L.edges if edge.head is vmax])
        R = set([(v, emax) for v in L.vertices - set([vmax]) \
            for emax in Emax if v in emax])
        while R:
            vertex, edge = R.pop()
            if L.indegree(vertex) + 1e-4 < L.indegree(vmax) \
                - H.weights[Edge(edge)]:
                L.remove_edge(edge)
                L.add_edge(Edge(edge, head=vertex),
                    weight=H.weights[Edge(edge)])
                accepted = True
                break
    # search NI
    accepted = True
    while accepted:
        accepted = False
        V = [vertex for vertex in L.vertices]
        V.sort(cmp=lambda a, b: L.indegree(a) < L.indegree(b) and -1 \
            or L.indegree(a) > L.indegree(b) and 1 or 0)
        try:
            for v1 in reversed(V):
                for v2 in V:
                    if v2 is v1:
                        break
                    for e1 in [edge for edge in L.edges \
                    if edge.head is v1 and v2 in edge]:
                        for e2 in [edge for edge in L.edges \
                        if edge.head is v2 and v1 in edge]:
                            if max(L.indegree(v1) - H.weights[Edge(e1)] \
                                + H.weights[Edge(e2)], L.indegree(v2) \
                                - H.weights[Edge(e2)] + H.weights[Edge(e1)]) \
                                + 1e-4 < max(L.indegree(v1), L.indegree(v2)):
                                L.remove_edge(e1)
                                L.remove_edge(e2)
                                L.add_edge(Edge(e1, head=v2),
                                    weight=H.weights[Edge(e1)])
                                L.add_edge(Edge(e2, head=v1),
                                    weight=H.weights[Edge(e2)])
                                accepted = True
                                raise Break
        except Break:
            pass
    return L
