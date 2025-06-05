import matplotlib.pyplot as plt
import numpy as np

# 데이터셋 크기 (노드 개수) - U16, U20 제외
sizes = np.array([280, 662, 9976, 100000])

# MST (Prim-Array) 실행 시간
mst_times = np.array([
    0.021352784633636476,    # a280
    0.13137211799621581,     # xql662
    26.961471557617188,      # kz9976
    1900.2236614227295       # mona-lisa100K
])

# New Method 실행 시간
new_times = np.array([
    0.023940925598144532,    # a280
    0.07620892524719239,     # xql662
    4.7084972858428955,      # kz9976
    374.12327456474304       # mona-lisa100K
])

# DP 선을 INF처럼 표시하기 위한 높이 계산
max_time = max(np.nanmax(mst_times), np.nanmax(new_times))
inf_height = max_time * 1.3  # 로그 스케일 상단에 약간 여유를 둠

# DP 값을 모두 inf_height로 설정
dp_times = np.array([inf_height] * len(sizes))

# 플롯
plt.figure(figsize=(6, 4))
plt.loglog(
    sizes, dp_times,
    marker='o', markersize=6, linestyle='--',
    color='#d62728', markerfacecolor='white', markeredgecolor='#d62728',
    linewidth=1.5, label='DP (infeasible → INF)'
)
plt.loglog(
    sizes, mst_times,
    marker='s', markersize=6, linestyle='-',
    color='#ff7f0e', markerfacecolor='white',
    markeredgecolor='#ff7f0e', linewidth=1.5, label='MST (Prim-Array)'
)
plt.loglog(
    sizes, new_times,
    marker='^', markersize=6, linestyle='-',
    color='#2ca02c', markerfacecolor='white',
    markeredgecolor='#2ca02c', linewidth=1.5, label='New Method'
)

# 레이블 및 축 설정
plt.xlabel('Number of nodes (log scale)', fontsize=15)
plt.ylabel('Runtime (s, log scale)', fontsize=15)
# plt.title('Runtime Comparison: MST vs. New Method (DP shown as INF)', fontsize=14)
plt.grid(which='major', linestyle='--', linewidth=0.5, alpha=0.7)

# 범례
plt.legend(frameon=False, fontsize=10)

plt.tight_layout()
plt.savefig('time_comp/exp3.pdf')
plt.show()