import math
import sys
sys.setrecursionlimit(10000)

from utils import distance

INF = int(1e9)

def run(coords):

    def dfs(x, visited):
        full_mask = (1 << n) - 1
        if visited == full_mask:
            return graph[x][0] if graph[x][0] > 0 else INF

        if dp[x][visited] != INF:
            return dp[x][visited]

        best_cost = INF
        best_next = -1
        for i in range(n):
            bit_i = 1 << i
            if (visited & bit_i):
                continue

            temp = dfs(i, visited | bit_i) + graph[x][i]
            if temp < best_cost:
                best_cost = temp
                best_next = i

        dp[x][visited] = best_cost
        parent[x][visited] = best_next
        return best_cost
    
    ############## START ################
    nodes = list(coords.keys())
    n = len(nodes)

    graph = [[0]*n for _ in range(n)]
    for i in range(n):
        u = coords[nodes[i]]
        for j in range(n):
            if i == j:
                continue
            v = coords[nodes[j]]
            graph[i][j] = distance(u, v)

    subset_count = 1 << n

    dp = [[INF] * subset_count for _ in range(n)]
    parent = [[-1] * subset_count for _ in range(n)]
    
    start = 0
    init_mask = 1 << start
    total_cost = dfs(start, init_mask)


    tour = [nodes[start]]
    cur = start
    mask = init_mask
    while True:
        nxt = parent[cur][mask]
        if nxt == -1:
            break
        tour.append(nodes[nxt])
        mask |= (1 << nxt)
        cur = nxt
    tour.append(nodes[start])

    return tour, total_cost