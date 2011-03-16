"""\
Hypergraph - orientation algorithms.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: LGPL-3
"""

from .core import Hypergraph, Edge


def minimum_maximum_indegree_orientation(H):
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
                    elif D[w] < D[u] - 1:
                        return path + [(edge, w)]
                    elif D[w] <= D[u]:
                        marked.add(w)
                        Q.append((w, path + [(edge, w)]))
        return None

    from random import sample
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

    N. Piersma and W. Van Dijk, "A Local Search Heuristic for Unrelated Parallel
    Machine Scheduling with Efficient Neighborhood Search," Mathematical and
    Computer Modelling, vol. 24, no. 9, pp. 11-19, 1996.

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
        mmax = max([(L.indegree(v), v) for v in L.vertices])[1]
        Jmax = set([edge for edge in L.edges if edge.head is mmax])
        Emax = set([(i, j) for i in L.vertices - set([mmax]) \
            for j in Jmax if i in j])
        while Emax:
            vertex, edge = Emax.pop()
            if L.indegree(vertex) + 1e-4 < L.indegree(mmax) \
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
        M = [vertex for vertex in L.vertices]
        M.sort(cmp=lambda a, b: L.indegree(a) < L.indegree(b) and -1 \
            or L.indegree(a) > L.indegree(b) and 1 or 0)
        try:
            for m1 in reversed(M):
                for m2 in M:
                    if m2 is m1:
                        break
                    for j in [edge for edge in L.edges \
                    if edge.head is m1 and m2 in edge]:
                        for k in [edge for edge in L.edges \
                        if edge.head is m2 and m1 in edge]:
                            if max(L.indegree(m1) - H.weights[Edge(j)] \
                                + H.weights[Edge(k)], L.indegree(m2) \
                                - H.weights[Edge(k)] + H.weights[Edge(j)]) \
                                + 1e-4 < max(L.indegree(m1), L.indegree(m2)):
                                L.remove_edge(j)
                                L.remove_edge(k)
                                L.add_edge(Edge(j, head=m2),
                                    weight=H.weights[Edge(j)])
                                L.add_edge(Edge(k, head=m1),
                                    weight=H.weights[Edge(k)])
                                accepted = True
                                raise Break
        except Break:
            pass
    return L
