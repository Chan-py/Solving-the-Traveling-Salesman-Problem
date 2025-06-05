import gzip
import re
import matplotlib.pyplot as plt
import numpy as np

def read_tsp(path):
    """
    .tsp 또는 .tsp.gz 파일을 읽어서
    { idx: (x, y), ... } 형태의 dict로 반환합니다.
    """
    # 파일 열기: .gz면 gzip, 아니면 일반 open
    opener = gzip.open if path.endswith('.gz') else open
    with opener(path, 'rt') as f:
        lines = f.readlines()

    coords = {}
    in_coords = False
    for line in lines:
        line = line.strip()
        if line.startswith('NODE_COORD_SECTION'):
            in_coords = True
            continue

        if in_coords:
            if line == 'EOF' or line == '':
                break
            # ex) "  1   37.619   55.755"
            parts = re.split(r'\s+', line)
            idx = int(parts[0])
            x, y = float(parts[1]), float(parts[2])
            coords[idx] = (x, y)
    return coords


class UnionFind:

    def __init__(self, n):
        # 1-based indexing
        self.parent = [-1] * (n + 1)

    def find(self, x):
        if self.parent[x] < 0:
            return x
        self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def merge(self, a, b):
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return False

        if self.parent[ra] > self.parent[rb]:
            ra, rb = rb, ra

        self.parent[ra] += self.parent[rb]
        self.parent[rb] = ra
        return True

    def size(self, x):
        return -self.parent[self.find(x)]
    

def distance(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return (dx**2 + dy**2) ** 0.5


def visualize_tour(coords, tour, save_path="../result/monalisa/mona_new.png", color='black', lw=0.28, show=True):
    # 좌표 값을 추출해서 x, y 리스트로 만듭니다.
    # coords의 key와 tour에 들어있는 인덱스가 일치한다고 가정합니다.
    xs = []
    ys = []
    for node in tour:
        x, y = coords[node]
        xs.append(x)
        ys.append(y)
    # 마지막에 출발점으로 돌아오도록 한 번 더 추가
    first_node = tour[0]
    x0, y0 = coords[first_node]
    xs.append(x0)
    ys.append(y0)

    # 그림을 그립니다.
    plt.figure(figsize=(6, 6))
    plt.plot(xs, ys, color=color, linewidth=lw, marker='o', markersize=0)
    plt.axis('equal')
    plt.axis('off')
    plt.tight_layout()

    # 저장 경로가 지정되면 파일로 저장
    if save_path is not None:
        plt.savefig(save_path)
    
    # 화면에 보여줄지 여부
    if show:
        plt.show()
    else:
        plt.close()

def plot_clusters(coords, clusters, centers=None, save_path="../result/monalisa/mona_clustering.png"):
    """
    Simple visualization of k-means++ clustering results.

    Args:
        coords (dict): Mapping from node key to (x, y) coordinate.
        clusters (dict): Mapping from cluster label to list of node keys.
        centers (dict, optional): Mapping from cluster label to centroid (x, y).
        save_path (str, optional): If provided, save the figure to this path.
    """
    cmap = plt.get_cmap('tab20')
    plt.figure(figsize=(6, 6))

    for lab, node_list in clusters.items():
        points = np.array([coords[u] for u in node_list])
        color = cmap(lab % 20)
        plt.scatter(points[:, 0], points[:, 1], s=0.1, color=color)

    if centers is not None:
        centroids = np.array([centers[lab] for lab in sorted(centers.keys())])
        plt.scatter(centroids[:, 0], centroids[:, 1], s=50, c='black', marker='X')

    plt.axis('equal')
    plt.axis('off')

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        plt.close()
    else:
        plt.show()