#!/usr/bin/env python3
"""
Publication-quality bar chart with error bars for Science paper.
3 groups, n=6 each, showing mean +/- SEM.
Outputs: bar_chart.pdf and bar_chart.png
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import rcParams

# --- Science journal formatting (single column = 3.5 in, ~89 mm) ---
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
rcParams['font.size'] = 8
rcParams['axes.linewidth'] = 0.5
rcParams['axes.labelsize'] = 8
rcParams['axes.titlesize'] = 8
rcParams['xtick.labelsize'] = 7
rcParams['ytick.labelsize'] = 7
rcParams['xtick.major.width'] = 0.5
rcParams['ytick.major.width'] = 0.5
rcParams['xtick.major.size'] = 3
rcParams['ytick.major.size'] = 3
rcParams['lines.linewidth'] = 0.5
rcParams['lines.markersize'] = 4
rcParams['legend.fontsize'] = 7
rcParams['figure.dpi'] = 300
rcParams['savefig.dpi'] = 300
rcParams['savefig.bbox'] = 'tight'
rcParams['savefig.pad_inches'] = 0.05

# --- Example data: 3 groups, n=6 each ---
# Replace these arrays with your actual data
np.random.seed(42)
group_A = np.array([4.2, 4.8, 3.9, 5.1, 4.5, 4.3])
group_B = np.array([6.1, 5.7, 6.5, 5.9, 6.3, 6.0])
group_C = np.array([3.5, 3.8, 3.2, 3.6, 3.4, 3.7])

groups = [group_A, group_B, group_C]
labels = ['Group A', 'Group B', 'Group C']

# --- Compute mean and SEM (standard error of the mean) ---
means = [np.mean(g) for g in groups]
sems = [np.std(g, ddof=1) / np.sqrt(len(g)) for g in groups]

# --- Create figure ---
fig, ax = plt.subplots(figsize=(3.5, 2.5))

x = np.arange(len(labels))
bar_width = 0.5

# Bars with error bars (SEM)
bars = ax.bar(
    x, means,
    width=bar_width,
    yerr=sems,
    capsize=3,
    color='#4C72B0',
    edgecolor='black',
    linewidth=0.5,
    error_kw={'elinewidth': 0.5, 'capthick': 0.5},
    zorder=3
)

# Overlay individual data points (jittered)
for i, g in enumerate(groups):
    jitter = np.random.normal(0, 0.04, size=len(g))
    ax.scatter(
        x[i] + jitter, g,
        s=12,
        color='white',
        edgecolors='black',
        linewidth=0.4,
        zorder=4
    )

# --- Axes formatting ---
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_ylabel('Measurement (units)')
ax.set_xlabel('')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xlim(-0.6, len(labels) - 0.4)
ax.set_ylim(0, max(m + s for m, s in zip(means, sems)) * 1.2)

# --- Export PDF and PNG ---
import os
out_dir = os.path.dirname(os.path.abspath(__file__))
fig.savefig(os.path.join(out_dir, 'bar_chart.pdf'), format='pdf', bbox_inches='tight')
fig.savefig(os.path.join(out_dir, 'bar_chart.png'), format='png', dpi=300, bbox_inches='tight')

plt.close(fig)

print("Saved: bar_chart.pdf")
print("Saved: bar_chart.png")
print(f"\nGroup A: mean = {means[0]:.2f}, SEM = {sems[0]:.2f}, n = {len(group_A)}")
print(f"Group B: mean = {means[1]:.2f}, SEM = {sems[1]:.2f}, n = {len(group_B)}")
print(f"Group C: mean = {means[2]:.2f}, SEM = {sems[2]:.2f}, n = {len(group_C)}")
