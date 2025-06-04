import random

from utils import distance
import mst
import dp


def kmeans_plus_plus(coords, K, max_iter=100):
    if K <= 0 or K > len(coords):
        raise ValueError("K must be between 1 and number of nodes")

    nodes = list(coords.keys())
    points = [coords[u] for u in nodes]
    N = len(nodes)

    # --- K-Means++ initialization ---
    centers = []
    # pick first center randomly
    first_idx = random.randrange(N)
    centers.append(points[first_idx])

    # pick the remaining K-1 centers
    for _ in range(1, K):
        # For each point, compute squared distance to nearest existing center
        dist_sq = []
        for p in points:
            d2 = min((p[0] - c[0])**2 + (p[1] - c[1])**2 for c in centers)
            dist_sq.append(d2)
        total = sum(dist_sq)    # total sum of distances

        if total == 0:
            # All points coincide with centers; pick any uncovered point
            next_idx = random.choice(range(N))
            centers.append(points[next_idx])
            continue

        # Pick next center with probability proportional to dist_sq[i]
        r = random.random() * total
        cum = 0.0
        for i, d2 in enumerate(dist_sq):
            cum += d2
            if cum >= r:
                centers.append(points[i])
                break

    # Convert centers list to dict for easy updates: {label: (x,y)}
    centers = {i: centers[i] for i in range(K)}

    # --- K-Means iterations ---
    for iteration in range(max_iter):
        # Assign each node to the nearest center
        labels = [None] * N
        for i, p in enumerate(points):
            best_label = None
            best_dist = 1e9
            for lab, c in centers.items():
                d = (p[0] - c[0])**2 + (p[1] - c[1])**2
                if d < best_dist:
                    best_dist = d
                    best_label = lab
            labels[i] = best_label

        # Compute new centers as mean of assigned points
        new_centers = {i: (0.0, 0.0) for i in range(K)}
        counts = {i: 0 for i in range(K)}
        for idx, lab in enumerate(labels):
            x, y = points[idx]
            sx, sy = new_centers[lab]
            new_centers[lab] = (sx + x, sy + y)
            counts[lab] += 1

        for lab in range(K):
            if counts[lab] == 0:
                # If a cluster lost all points, reinitialize center randomly
                rand_idx = random.randrange(N)
                new_centers[lab] = coords[nodes[rand_idx]]
            else:
                sx, sy = new_centers[lab]
                new_centers[lab] = (sx / counts[lab], sy / counts[lab])

        # Check for convergence (centers do not move)
        converged = True
        for lab in range(K):
            old = centers[lab]
            new = new_centers[lab]
            if (old[0] - new[0])**2 + (old[1] - new[1])**2 > 1e-8:
                converged = False
                break
        centers = new_centers
        if converged:
            break

    # Build final clusters
    clusters = {i: [] for i in range(K)}
    for idx, lab in enumerate(labels):
        u = nodes[idx]
        clusters[lab].append(u)

    return clusters, centers


def get_cluster_internal_tours(clusters, coords):
    cluster_tours = {}
    for lab, node_list in clusters.items():
        sub_coords = {u: coords[u] for u in node_list}
        tour, _ = mst.run(sub_coords)  # mst.run returns (tour, cost)
        cluster_tours[lab] = tour
    return cluster_tours


def dp_cluster_order(centroids):
    seq, cost = dp.run(centroids)
    return seq[:-1], cost


def rotate_cycle(cycle, start_node):
    if not cycle:
        return []
    # Remove the final repeated node if present
    if cycle[0] == cycle[-1]:
        base = cycle[:-1]
    else:
        base = list(cycle)
    n = len(base)
    try:
        idx = base.index(start_node)
    except ValueError:
        idx = 0
    rotated = base[idx:] + base[:idx]
    return rotated


def merge_cluster_tours(coords, cluster_tours, seq, centroids):
    K = len(seq)

    # 1) “open” 형태(마지막 중복 제거)로 클러스터 내부 투어를 미리 만들어 둡니다.
    open_tours = {}
    for lab, tour in cluster_tours.items():
        if tour and tour[0] == tour[-1]:
            open_tours[lab] = tour[:-1]
        else:
            open_tours[lab] = list(tour)

    # 2) seq 순서대로, 각 클러스터마다 start/end를 결정하고 rotate된 “open” 경로를 계산
    rotated = {}
    for idx, lab in enumerate(seq):
        # 2a) 이전(prev) 클러스터 레이블과 다음(next) 클러스터 레이블 구하기 (wrap-around)
        if idx > 0:
            prev_lab = seq[idx - 1]
        else:
            prev_lab = seq[-1]
        if idx < K - 1:
            next_lab = seq[idx + 1]
        else:
            next_lab = seq[0]

        prev_cent = centroids[prev_lab]
        next_cent = centroids[next_lab]

        # 이 클러스터의 “open cycle” 노드 리스트
        base = open_tours[lab]  # e.g. [n0, n1, ..., n(m-1)]

        # “best split 인덱스(best_i)”를 찾기
        best_i = None
        best_cost = 1e9
        m = len(base)
        if m == 0:
            # 해당 클러스터에 노드가 없으면 건너뜁니다 (매우 드문 경우).
            rotated[lab] = []
            continue

        # m>=1일 때, 순환을 한 바퀴 돌 수 있으므로
        # 각 i in [0..m-1]: start_node = base[i], end_node = base[i-1] (wrap)
        for i in range(m):
            start_node = base[i]
            end_node = base[i - 1]  # i-1이 -1이 되면 base[-1] = base[m-1]

            d_prev = distance(coords[start_node], prev_cent)
            d_next = distance(coords[end_node], next_cent)
            cost = d_prev + d_next

            if cost < best_cost:
                best_cost = cost
                best_i = i

        start_node = base[best_i]  # 베스트 split의 시작 노드

        rotated[lab] = rotate_cycle(cluster_tours[lab], start_node)

    # 3) 모든 클러스터의 “open path”를 seq 순서대로 이어 붙이기
    final_tour = []
    for idx, lab in enumerate(seq):
        tour = rotated[lab]
        if idx == 0:
            final_tour.extend(tour)
        else:
            # 새로운 클러스터 path를 이어 붙일 때 앞 노드가
            # 이전 cluster의 end_node와 같다면 중복 방지 위함
            final_tour.extend(tour)

    # 4) 마지막에 다시 출발 노드를 붙여 닫힌 순환 완성
    if final_tour:
        final_tour.append(final_tour[0])

    return final_tour


def compute_total_cost(coords, tour):
    total = 0.0
    for i in range(len(tour) - 1):
        u = tour[i]
        v = tour[i + 1]
        total += distance(coords[u], coords[v])
    return total


def run(coords, K=10, max_iter=100):
    # 1. Cluster nodes
    clusters, centers = kmeans_plus_plus(coords, K, max_iter=max_iter)

    # 2. Solve each cluster's TSP via MST-based 2-approx
    cluster_tours = get_cluster_internal_tours(clusters, coords)

    # 3. DP to find cluster sequence
    seq, _ = dp_cluster_order(centers)

    # 4. Merge cluster tours
    final_tour = merge_cluster_tours(coords, cluster_tours, seq, centers)

    # 5. Compute total cost
    total_cost = compute_total_cost(coords, final_tour)

    return final_tour, total_cost