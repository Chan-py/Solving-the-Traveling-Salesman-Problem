import matplotlib.pyplot as plt

# Data provided by the user
k_values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
times = [
    28.44275484085083, 13.392850828170776, 14.969853067398072, 12.111027050018311,
    10.491463994979858, 9.148713541030883, 5.0354572296142575, 4.444639730453491,
    4.392868852615356, 8.066244888305665, 8.60598292350769, 7.184525680541992,
    5.730402135848999, 5.422050094604492, 9.075379037857056, 12.606296157836914,
    18.96487078666687, 24.930718421936035, 30.816745710372924
]

plt.figure(figsize=(8, 5))
plt.plot(k_values, times, marker='o', linewidth=2)
plt.xlabel('k Value', fontsize=15)
plt.ylabel('Execution Time (seconds)', fontsize=15)
# plt.title('Execution Time vs. k Value')

# Set x‐axis ticks to avoid decimals (every other k)
xticks = k_values[::2]  # [2, 4, 6, ..., 20]
plt.xticks(xticks, fontsize=13)
plt.yticks(fontsize=13)

plt.grid(True, linestyle='--', alpha=0.6)

plt.savefig('k_comp/exp4.pdf', bbox_inches='tight', dpi=300)
plt.show()