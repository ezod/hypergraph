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
    all other vertices in graphs with nonnegative weights.

        - E. W. Dijkstra, "A Note on Two Problems in Connexion with Graphs,"
          Numerische Mathematik, vol. 1, pp. 269-271, 1959.

    @param G: The graph.
    @type G: L{Graph}
    @param start: The start vertex.
    @type start: C{object}
    @return: The "previous" array of Dijkstra's algoritm.
    @rtype: C{dict}
    @raise ValueError: Graph is not 2-uniform or has negative edge weights.
    """
    try:
        assert G.uniform(2)
        assert all([weight >= 0 for weight in G.weights.values()])
    except AssertionError:
        raise ValueError(('function can only be applied to 2-uniform graphs '
                          'with nonnegative edge weights'))
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


def bellman_ford(G, start):
    """\
    Bellman-Ford algorithm for finding the shortest paths from the start vertex
    to all other vertices in directed graphs.

        - R. Bellman, "On a Routing Problem," Quarterly of Applied Mathematics,
          vol. 16, no. 1, pp. 87-90, 1958.

        - L. R. Ford Jr. and D. R. Fulkerson, "Flows in Networks," Princeton
          University Press, 1962.

    @param G: The directed graph.
    @type G: L{Graph}
    @param start: The start vertex.
    @type start: C{object}
    @return:
    @rtype: C{dict}
    @raise ValueError: Graph is not 2-uniform or is not directed.
    @raise RuntimeError: Graph contains a negative-weight cycle.
    """
    try:
        assert G.directed
        assert G.uniform(2)
    except AssertionError:
        raise ValueError('function can only be applied to 2-uniform digraphs')
    dist = dict.fromkeys(G.vertices, float('inf'))
    prev = dict.fromkeys(G.vertices, None)
    dist[start] = 0.0
    for i in range(1, len(G.vertices) - 1):
        for edge in G.edges:
            u, v = edge.tail.pop(), edge.head
            if dist[u] + G.weights[edge] < dist[v]:
                dist[v] = dist[u] + G.weights[edge]
                prev[v] = u
    for edge in G.edges:
        u, v = edge.tail.pop(), edge.head
        if dist[u] + G.weights[edge] < dist[v]:
            raise RuntimeError('graph contains a negative-weight cycle')
    return prev


def shortest_path(G, start, end):
    """\
    Find the shortest path from the start vertex to the end vertex. Attempt to
    use Dijkstra's algorithm first, then Bellman-Ford algorithm.

    @param start: The start vertex.
    @type start: C{object}
    @param end: The end vertex.
    @type end: C{object}
    @return: Shortest path vertex list and total distance.
    @rtype: C{list}, C{float}
    """
    try:
        prev = dijkstra(G, start)
    except ValueError:
        prev = bellman_ford(G, start)
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

        - R. W. Floyd, "Algorithm 97: Shortest Path," Comm. of the ACM, vol. 5,
          no. 6, p. 345, 1962.

        - S. Warshall, "A Theorem on Boolean Matrices," J. of the ACM, vol. 9,
          no. 1, pp. 11-12, 1962.

    @param G: The input graph.
    @type G: L{Graph}
    @return: A two-dimensional dictionary of pairwise shortest path lengths.
    @rtype: C{dict} of C{dict} of C{float}
    @raise ValueError: Graph is not 2-uniform.
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
