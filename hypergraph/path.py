"""\
Hypergraph - path algorithms.

@author: Aaron Mavrinac
@organization: University of Windsor
@contact: mavrin1@uwindsor.ca
@license: LGPL-3
"""

from copy import deepcopy

from .core import Edge


def dijkstra(G, start):
    """\
    Dijkstra's algorithm for finding the shortest paths from the start vertex to
    all other vertices.

    @param start: The start vertex.
    @type start: C{object}
    @return: The "previous" array of Dijkstra's algoritm.
    @rtype: C{dict}
    """
    try:
        assert G.uniform(2)
    except AssertionError:
        raise ValueError('function can only be applied to 2-uniform graphs')
    dist = dict.fromkeys(G.vertices, float('inf'))
    prev = dict.fromkeys(G.vertices, None)
    Q = set(G.vertices)
    dist[start] = 0.0
    while Q:
        u = None
        for vertex in Q:
            if not u or dist[vertex] < dist[u]:
                u = vertex
        Q.remove(u)
        for vertex in G.neighbors(u):
            alt = dist[u] + G.weights[Edge([u, vertex],
                head=(G.directed and vertex or None))]
            if alt < dist[vertex]:
                dist[vertex] = alt
                prev[vertex] = u
    return prev


def shortest_path(G, start, end):
    """\
    Find the shortest path from the start vertex to the end vertex using
    Dijkstra's algorithm.

    @param start: The start vertex.
    @type start: C{object}
    @param end: The end vertex.
    @type end: C{object}
    @return: Shortest path vertex list and total distance.
    @rtype: C{list}, C{float}
    """
    prev = dijkstra(G, start)
    path = []
    u = end
    dist = 0.0
    while u in prev.keys():
        path.insert(0, u)
        if prev[u]:
            dist += G.weights[Edge([prev[u], u],
                head=(G.directed and u or None))]
        u = prev[u]
    return path, dist


def floyd_warshall(G):
    """\
    Floyd-Warshall algorithm for finding the shortest path lengths between all
    pairs of vertices in a graph.

    @param G: The input graph.
    @type G: L{Graph}
    @return: A two-dimensional dictionary of pairwise shortest path lengths.
    @rtype: C{dict} of C{dict} of C{float}
    """
    try:
        assert G.uniform(2)
    except AssertionError:
        raise ValueError('function can only be applied to 2-uniform graphs')
    path = {}
    for u in G.vertices:
        path[u] = {}
        for v in G.vertices:
            if u == v:
                path[u][v] = 0.0
                continue
            try:
                path[u][v] = G.weights[Edge([u, v],
                    head=(G.directed and v or None))]
            except KeyError:
                path[u][v] = float('inf')
    for w in G.vertices:
        for u in G.vertices:
            for v in G.vertices:
                path[u][v] = min(path[u][v], path[u][w] + path[w][v])
    return path


def shortest_path_subgraph(G):
    """\
    Return the shortest path subgraph of a graph, which contains only strong
    edges (edges which form part of a shortest path between some pair of
    vertices).

    @param G: The input graph.
    @type G: L{Graph}
    @return: The shortest path subgraph.
    @rtype: L{Graph}
    """
    S = deepcopy(G)
    path = floyd_warshall(S)
    for edge in S.edges:
        if S.weights[edge] > path[edge.tail.pop()][edge.head]:
            S.remove_edge(edge)
    return S
