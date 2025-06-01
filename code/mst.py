import heapq
from tqdm import tqdm
import sys
sys.setrecursionlimit(int(1e6))

from utils import UnionFind, distance

def Kruskal(coords):
    nodes = list(coords.keys())
    edges = []
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            u, v = nodes[i], nodes[j]
            w = distance(coords[u], coords[v])
            edges.append((w, u, v))

    edges.sort()
    
    UF = UnionFind(len(nodes))
    graph = [[] for _ in range(len(nodes) + 1)]
    cnt = 0

    for w, u, v in edges:
        if UF.merge(u, v):
            graph[u].append((v, w))
            graph[v].append((u, w))
            cnt += 1
        if cnt == len(nodes) - 1:
            break
    return graph


def Prim(coords):
    nodes = list(coords.keys())

    start = nodes[0]
    visited = {start}

    graph = [[] for _ in range(len(nodes) + 1)]
    cnt = 0
    heap = []

    # 초기: start에서 다른 모든 노드로의 간선 추가
    for v in nodes:
        if v != start:
            w = distance(coords[start], coords[v])
            heapq.heappush(heap, (w, start, v))

    # Prim's algorithm
    while heap and cnt < len(nodes) - 1:
        w, u, v = heapq.heappop(heap)
        if v in visited:
            continue
        visited.add(v)
        graph[u].append((v, w))
        graph[v].append((u, w))
        cnt += 1

        # 새로 방문한 v에서 아직 방문하지 않은 노드로의 간선 추가
        for nxt in nodes:
            if nxt not in visited:
                w2 = distance(coords[v], coords[nxt])
                heapq.heappush(heap, (w2, v, nxt))

    return graph

def Prim_v2(coords):
    nodes = list(coords.keys())
    n = len(nodes)

    key = [1e9] * (n + 1)
    parent = {u: None for u in nodes}
    visited = set()
    
    start = 1
    key[start] = 0

    for i in tqdm(range(n), desc="progress"):
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

    graph = [[] for _ in range(n + 1)]
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
    
    start = 1
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