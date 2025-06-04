import heapq
from tqdm import tqdm
import sys
sys.setrecursionlimit(int(1e6))

from utils import UnionFind, distance

def Kruskal(coords):
    nodes = list(coords.keys())
    n = len(nodes)

    # Build all edges in terms of indices
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            u_label = nodes[i]
            v_label = nodes[j]
            w = distance(coords[u_label], coords[v_label])
            edges.append((w, i, j))
    edges.sort()

    # Kruskal on indices 0..n-1
    UF = UnionFind(n)
    # Prepare graph as label → list[(neighbor_label, weight)]
    graph = {u: [] for u in nodes}
    cnt = 0

    for w, i, j in edges:
        if UF.merge(i, j):
            u_label = nodes[i]
            v_label = nodes[j]
            graph[u_label].append((v_label, w))
            graph[v_label].append((u_label, w))
            cnt += 1
            if cnt == n - 1:
                break

    return graph


def Prim(coords):
    nodes = list(coords.keys())
    start = nodes[0]
    visited = {start}
    graph = {u: [] for u in nodes}
    cnt = 0
    heap = []

    # Push all edges from 'start' into the heap
    for v in nodes:
        if v != start:
            w = distance(coords[start], coords[v])
            heapq.heappush(heap, (w, start, v))

    # Standard Prim’s loop
    while heap and cnt < len(nodes) - 1:
        w, u, v = heapq.heappop(heap)
        if v in visited:
            continue
        visited.add(v)
        graph[u].append((v, w))
        graph[v].append((u, w))
        cnt += 1

        # Add edges from newly added node 'v' to all unvisited nodes
        for nxt in nodes:
            if nxt not in visited:
                w2 = distance(coords[v], coords[nxt])
                heapq.heappush(heap, (w2, v, nxt))

    return graph

def Prim_v2(coords):
    nodes = list(coords.keys())
    n = len(nodes)

    # key = [1e9] * (n + 1)
    key = {u: 1e9 for u in nodes}
    parent = {u: None for u in nodes}
    visited = set()
    
    start = nodes[0]
    key[start] = 0

    # for i in tqdm(range(n), desc="progress"):
    for i in range(n):
        u = None
        min_key = 1e9
        for v in nodes:
            if v not in visited and key[v] < min_key:
                min_key = key[v]
                u = v
        if u is None:
            break
        visited.add(u)

        for v in nodes:
            if v not in visited:
                w = distance(coords[u], coords[v])
                if w < key[v]:
                    key[v] = w
                    parent[v] = u

    # graph = [[] for _ in range(n + 1)]
    graph = {u: [] for u in nodes}
    for v in nodes:
        u = parent[v]
        if u is not None:
            w = distance(coords[u], coords[v])
            graph[u].append((v, w))
            graph[v].append((u, w))

    return graph


def _preorder_traversal(tree, node, visited, tour):
    visited.add(node)
    tour.append(node)
    for nbr, _ in tree[node]:
        if nbr not in visited:
            _preorder_traversal(tree, nbr, visited, tour)

def run(coords):

    graph = Prim_v2(coords)
    # print(graph)
    
    start = list(coords.keys())[0]
    tour = []
    _preorder_traversal(graph, start, set(), tour)
    
    visited = set()
    final = []

    for u in tour:
        if u not in visited:
            visited.add(u)
            final.append(u)
    
    final.append(final[0])

    total_cost = 0
    for i in range(len(final) - 1):
        total_cost += distance(coords[final[i]], coords[final[i+1]])
    return final, total_cost