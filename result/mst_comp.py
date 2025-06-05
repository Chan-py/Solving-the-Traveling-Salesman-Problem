import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# (1) 원본 데이터에 'INF' 표기를 위한 표시를 추가합니다.
#     float('inf') 자체를 times 에 넣으면 그래프가 깨지므로, 
#     내부적으로는 None/np.nan 으로 처리하고 나중에 텍스트만 표시할 것입니다.
datasets = {
    'a280': {
        'methods': ['Kruskal', 'Prim-Heap', 'Prim-Array'],
        'times': [0.035499331951141355, 0.029944710731506348, 0.021352784633636476]
    },
    'xql662': {
        'methods': ['Kruskal', 'Prim-Heap', 'Prim-Array'],
        'times': [0.3182134866714478, 0.22367448806762696, 0.13137211799621581]
    },
    'kz9976': {
        'methods': ['Kruskal', 'Prim-Heap', 'Prim-Array'],
        'times': [130.94633769989014, 47.86716842651367, 26.961471557617188]
    },
    'mona-lisa100K': {
        # Kruskal, Prim-Heap 은 메모리 오류 → None 으로, Prim-Array 만 실제 시간
        'methods': ['Kruskal', 'Prim-Heap', 'Prim-Array'],
        'times': [None, None, 1900.2236614227295]
    }
}

for name, data in datasets.items():
    methods = data['methods']
    times = data['times']
    
    # (2) 유한한(finite) 값들 중 최대값을 구해서, INF 표시용 높이를 계산
    finite_times = [t for t in times if (t is not None)]
    if len(finite_times) == 0:
        # 예외 처리: 모든 값이 None 이면 기본 높이를 1 로 둡니다.
        max_finite = 1.0
    else:
        max_finite = max(finite_times)
    inf_height = max_finite * 1.3  # INF 표시용 높이 (예: 최대값의 10% 위)
    
    # (3) 실제 그래프용 데이터 배열: None 은 '바를 그리지 않음'으로 해석
    plot_heights = []
    for t in times:
        if t is None:
            plot_heights.append(inf_height)  # 바를 그리지만, 텍스트로는 INF 라벨만 붙일 예정
        else:
            plot_heights.append(t)
    
    fig, ax = plt.subplots(figsize=(6, 4))
    facecolors = ['white', 'white', 'white']
    edgecolors = ['chocolate', 'steelblue', 'seagreen']
    #    ※ 첫 번째 막대 테두리만 choco로, 나머지는 facecolor와 동일하게 설정
    
    bars = ax.bar(methods, plot_heights, width=0.5,
                  color=facecolors,     # facecolor를 리스트로 지정
                  edgecolor=edgecolors) # edgecolor도 리스트로 지정
    # bars = ax.bar(methods, plot_heights, width=0.5, color='white', edgecolor='chocolate')
    
    # (4) 해칭 처리 및 테두리 두께
    for bar in bars:
        bar.set_hatch('///')
        bar.set_linewidth(1)
    
    # (5) Y축 그리드
    ax.yaxis.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
    ax.set_axisbelow(True)
    
    # (6) 제목 및 축 레이블
    # ax.set_title(f'{name}', fontsize=16)
    ax.set_xlabel('MST Algorithm', fontsize=18)
    ax.set_ylabel('Time (seconds)', fontsize=18)
    ax.tick_params(axis='x', labelsize=18)
    ax.tick_params(axis='y', labelsize=18)
    
    # (7) 각 바 위에 숫자 또는 “INF” 텍스트 표시
    for bar, t in zip(bars, times):
        height = bar.get_height()
        x_center = bar.get_x() + bar.get_width() / 2
        if t is None:
            # 메모리 오류인 경우, inf_height 로 그려진 바 위에 'INF' 라벨만 붙임
            ax.text(x_center, 
                    height * 0.9,            # 막대 중앙 정도에 붙이거나, 
                    'INF',                  # INF 라벨
                    ha='center', va='bottom',
                    fontsize=10, fontweight='bold', color='red')
    
    # (8) 범례 (Runtime → 해칭된 패턴에 대한 설명)
    patch = mpatches.Patch(
        facecolor='white',
        edgecolor='black',
        hatch='///',
        label='Runtime'
    )
    ax.legend(handles=[patch], loc='upper right', fontsize=14)
    
    plt.tight_layout()
    plt.savefig(f'mst_comp/ex1_{name}.pdf')
    plt.show()
