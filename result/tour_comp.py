import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Ground-truth optimal tour costs
ground_truth = {
    'a280': 2579,
    'xql662': 2513,
    'kz9976': 1061882,
    'mona-lisa100K': 5757191
}

# Measured tour costs for MST (Prim-Array) and New algorithm
results = {
    'a280': {
        'MST': 3484.853377045222,
        'New': 3684.6132423254444
    },
    'xql662': {
        'MST': 3526.5415918369845,
        'New': 3723.078253554498
    },
    'kz9976': {
        'MST': 1457223.5174078138,
        'New': 1513519.9624601793
    },
    'mona-lisa100K': {
        'MST': 8395215.018901309,
        'New': 8424637.005932804
    }
}

dataset_names = ['a280', 'xql662', 'kz9976', 'mona-lisa100K']
methods = ['Optimal', 'MST', 'New']

# Colors for each method
method_colors = {
    'Optimal': 'steelblue',
    'MST': 'chocolate',
    'New': 'seagreen'
}

# Bar width and spacing
bar_width = 0.15
gap = bar_width + 0.1  # gap between groups
step = bar_width * len(methods) + gap  # horizontal distance between group starts

positions = []
heights = []
colors = []

# Compute positions, heights, and colors for each bar
for i, name in enumerate(dataset_names):
    opt = ground_truth[name]
    mst_cost = results[name]['MST']
    new_cost = results[name]['New']
    ratios = {
        'Optimal': 1.0,
        'MST': mst_cost / opt,
        'New': new_cost / opt
    }
    for j, method in enumerate(methods):
        x = i * step + j * bar_width
        positions.append(x)
        heights.append(ratios[method])
        colors.append(method_colors[method])

# Set up figure
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(positions, heights, width=bar_width, color='white', edgecolor=colors, linewidth=0.8)

# Apply hatching and line width
for bar in bars:
    bar.set_hatch('///')
    bar.set_linewidth(1)
    
# Horizontal grid lines
ax.yaxis.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
ax.set_axisbelow(True)

# X-axis ticks at the center of each group
group_centers = [i * step + bar_width for i in range(len(dataset_names))]
ax.set_xticks(group_centers)
ax.set_xticklabels(dataset_names, rotation=0, fontsize=19)

# Labels and title
# ax.set_title('Tour Cost Ratio Across All Datasets', fontsize=18)
ax.set_xlabel('Dataset', fontsize=20)
ax.set_ylabel('Cost / Optimal', fontsize=20)

# Y-axis starts at 0
max_height = max(heights)
ax.set_ylim(0, max_height * 1.1)

# Annotate each bar with its ratio value
for bar, h in zip(bars, heights):
    x_center = bar.get_x() + bar.get_width() / 2
    ax.text(
        x_center,
        h + 0.02 * max_height,
        f'{h:.2f}',
        ha='center',
        va='bottom',
        fontsize=11
    )

# Legend for the three methods
patches = [
    mpatches.Patch(facecolor='white', edgecolor=method_colors[m], hatch='///', label=m)
    for m in methods
]
ax.legend(handles=patches, loc='upper left', fontsize=14)

plt.tight_layout()
plt.savefig('tour_comp/exp2.pdf')
plt.show()
