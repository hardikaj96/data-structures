from copy import deepcopy
from priorityQueues.priorityQueue import AdaptableHeapPriorityQueue
from priorityQueues.priorityQueue import HeapPriorityQueue

class Vertex:
    """Lightweight vertex structure for a graph"""
    def __init__(self, x):
        """Do not call constructor directly. Use Graph's insert.vertex(x)"""
        self._element = x

    def element(self):
        """Return element associated with this vertex"""
        return self._element

    def __hash__(self):
        return hash(id(self))

class Edge:
    """Lightweight edge structure for a graph"""
    def __init__(self, u, v, x):
        self.origin = u
        self.destination = v
        self._element = x

    def endpoints(self):
        """Return (u,v) tuple for vertices u and v"""
        return (self.origin, self.destination)

    def opposite(self, v):
        """Return the vertex that is opposite v on this edge"""
        return self.destination if v is self.origin else self.origin

    def element(self):
        """Return element associated with this edge"""
        return self._element

    def __hash__(self):
        return hash((self.origin, self.destination))

class Graph:
    """Representation of a simple graph using an adjacency map"""
    def __init__(self, directed=False):
        """Create an empty graph (undirected)
        Graph is directed if optional parameter is True
        """
        self.outgoing = {}
        self.incoming = {} if directed else self.outgoing

    def is_directed(self):
        """Return True if this is a directed graph, False if undirected"""
        return self.incoming is not self.outgoing

    def vertex_count(self):
        """Return the number of vertices in the graph"""
        return len(self.outgoing)

    def vertices(self):
        """Return an iteration of all vertices of the graph"""
        return self.outgoing.keys()

    def edge_count(self):
        """Return the number of edges in the graph"""
        total = sum(len(self.outgoing[v]) for v in self.outgoing)
        return total if self.is_directed() else total // 2

    def edges(self):
        """Return a set of all edges of the graph"""
        result = set()
        for secondary_map in self.outgoing.values():
            result.update(secondary_map.values())
        return result

    def get_edge(self, u, v):
        """Return the edge from u to v or None if not adjacent"""
        return self.outgoing[u].get(v)

    def degree(self, v, outgoing=True):
        """Return the number of (outgoing) edges incident to vertex v in the graph
        If graph is directed, optional parameter used to count incoming edges
        """
        adj = self.outgoing if outgoing else self.incoming
        return len(adj[v])

    def incident_edges(self, v, outgoing=True):
        """Return all (outgoing) edges incident to vertex v in the graph"""
        adj = self.outgoing if outgoing else self.incoming
        for edge in adj[v].values():
            yield edge

    def insert_vertex(self, x=None):
        """Insert and return a new Vertex with element x"""
        v = self.Vertex(x)
        self.outgoing[v] = {}
        if self.is_directed():
            self.incoming[v] = {}
        return v

    def insert_edge(self, u, v, x=None):
        """Insert and return a new Edge from u to v with auxillary element x"""
        e = self.Edge(u, v, x)
        self.outgoing[u][v] = e
        self.incoming[v][u] = e


def DFS(g, u, discovered):
    """Perform DFS of the undiscovered portion of Graph g starting at Vertex u.

    discovered is a dictionary mapping each vertex to the edge that was used to
    discover it during the DFS.
    Newly discovered vertices will be added to the dictionary as a result
    """
    for e in g.incident_edges(u):
        v = e.opposite(u)
        if v not in discovered:
            discovered[v] = e
            DFS(g, v, discovered)

def construct_path(u, v, discovered):
    path = []
    if v in discovered:
        path.append(v)
        walk = v
        while walk is not u:
            e = discovered[walk]
            parent = e.opposite(walk)
            path.append(parent)
            walk = parent
        path.reverse()
    return path

def DFS_complete(g):
    """Perform DFS for entire graph and return forest as a dictionary
    Result maps each vertex v to the edge that was used to discover it
    """
    forest = {}
    for u in g.vertices():
        if u not in forest:
            forest[u] = None
            DFS(g, u, forest)
    return forest

def BFS(g, s, discovered):
    """Perform BFS of the undiscovered portion of Graph g starting at Vertex s.

    discovered is a dictionary mapping each vertex to the edge that was used to
    discover it during the BFS
    Newly discovered vertices will be added to the dictionary as a result
    """
    level = [s]
    while len(level)>0:
        next_level = []
        for u in level:
            for e in g.incident_edges(u):
                v = e.opposite(u)
                if v not in discovered:
                    discovered[v] = e
                    next_level.append(e)
        level = next_level

def floyd_warshall(g):
    """Return a new graph that is the transitive closure of g"""
    closure = deepcopy(g)
    verts = list(closure.vertices())
    n = len(verts)
    for k in range(n):
        for i in range(n):
            if i != k and closure.get_edge(verts[i],verts[k]) is not None:
                for j in range(n):
                    if i != j != k and closure.get_edge(verts[k],verts[j]) is not None:
                        if closure.get_edge(verts[i],verts[j]) is None:
                            closure.insert_edge(verts[i],verts[j])
    return closure

def topological_sort(g):
    """Return a list of vertices of directed acyclic graph g in topological order
    If graph g has a cycle, the result will be incomplete
    """
    topo = []
    ready = []
    incount = []
    for u in g.vertices():
        incount[u] = g.degree(u, False)
        if incount[u] == 0:
            ready.append(u)
    while len(ready) > 0:
        u = ready.pop()
        topo.append(u)
        for e in g.incident_edges(u):
            v = e.opposite(u)
            incount[v] -= 1
            if incount[v] == 0:
                ready.append(v)
    return topo

#Dijkstra
def shortest_path_lengths(g, src):
    """Compute shortest-path distances from src to reachable vertices of g
    Graph g can be undirected or directed, but must be weighted such that
    e.element() returns a numeric weight for each edge e.
    Return dictionary mapping each reachable vertex to its distance from src
    """
    d = {}
    cloud = {}
    pq = AdaptableHeapPriorityQueue()
    pqlocator = {}
    # for each vertex v of the graph, add an entry to the priority, with
    # the source having distance 0 and all others having infinte distance
    for v in g.vertices():
        if v in src:
            d[v] = 0
        else:
            d[v] = float('inf')
        pqlocator[v] = pq.add(d[v], v)

    while not pq.is_empty():
        key, u = pq.remove_min()
        cloud[u] = key
        del pqlocator[u]
        for e in g.incident_edges(u):
            v = e.opposite(u)
            if v not in cloud:
                wgt = e.element()
                if d[u] + wgt < d[v]:
                    d[v] = d[u] + wgt
                    pq.update(pqlocator[v], d[v], v)
    return cloud

def shortest_path_tree(g, s, d):
    """Reconstruct shortest-path tree rooted at vertex s, given distance map d

    Return tree as a map from each reachable vertex v to the
    edge e=(u,v) that is used to reach v from its parent u in the tree
    """
    tree = {}
    for v in d:
        if v is not s:
            for e in g.incident_edges(v, False):
                u = e.opposite(v)
                wgt = e.element()
                if d[v] == d[u] + wgt:
                    tree[v] = e
    return tree

def MST_PrimJarnik(g):
    """Compute a minimum spanning tree of weighted graph g
    Return a list of edges that comprise the MST
    """
    d = {}
    tree = []
    pq = AdaptableHeapPriorityQueue()
    pqlocator = {}

    for v in g.vertices():
        if len(d) == 0:
            d[v] = 0
        else:
            d[v] = float('inf')
        pqlocator[v] = pq.add(d[v], (v, None))
    while not pq.is_empty():
        key, value = pq.remove_min()
        u, edge = value
        del pqlocator[u]
        if edge is not None:
            tree.append(edge)
        for link in g.incident_edges(u):
            v = link.opposite(u)
            if v in pqlocator:
                wgt = link.element()
                if wgt < d[v]:
                    d[v] = wgt
                    pq.update(pqlocator[v], d[v], (v, link))

def MST_Kruskal(g):
    """Compute a minimum spanning tree of a graph using Kruskal's algorithm.

    Return a list of edges that comprise the MST

    The elements of the graph's edges are assumed to be weights.
    """
    tree = []
    pq = HeapPriorityQueue()
    forest = Partition()
    position = {}
    for v in g.vertices():
        position[v] = forest.make_group(v)

    for e in g.edges():
        pq.add(e.element(), e)

    size = g.vertex_count()
    while len(tree) != size - 1 and not pq.is_empty():
        weight, edge = pq.remove_min()
        u, v = edge.endpoints()
        a = forest.find(position[u])
        b = forest.find(position[v])
        if a != b:
            tree.append(edge)
            forest.union(a, b)
    return tree

class Partition:
    """Union-find structure for maintaining disjoint sets"""

    class Position:

        def __init__(self, container, e):
            """Create a new position that is the leader of its own group"""
            self.container = container
            self._element = e
            self.size = 1
            self.parent = self
        def element(self):
            """Return element stored at this position"""
            return self._element

    def make_group(self, e):
        """Makes a new group containing element e, and returns its Position"""
        return self.Position(self, e)

    def find(self, p):
        """Finds the group containing p and return the position of its leader"""
        if p.parent != p:
            p.parent = self.find(p.parent)
        return p.parent

    def union(self, p, q):
        """Merges the groups containing elements p and q"""
        a = self.find(p)
        b = self.find(q)
        if a is not b:
            if a.size > b.size:
                b.parent = a
                a.size += b.size
            else:
                a.parent = b
                b.size += a.size
