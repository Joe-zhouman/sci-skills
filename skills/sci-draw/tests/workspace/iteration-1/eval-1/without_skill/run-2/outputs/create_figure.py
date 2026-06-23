#!/usr/bin/env python3
"""
Create a Nature-style grouped bar chart with error bars.
5 methods x 3 metrics, each with mean and std.
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from pathlib import Path

# ---------- Nature journal style parameters ----------
mpl.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 7,
    'axes.labelsize': 7,
    'axes.titlesize': 7,
    'xtick.labelsize': 7,
    'ytick.labelsize': 7,
    'legend.fontsize': 6,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'axes.linewidth': 0.5,
    'xtick.major.width': 0.5,
    'ytick.major.width': 0.5,
    'xtick.major.size': 2,
    'ytick.major.size': 2,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'figure.figsize': (3.5, 2.5),  # 3.5 inches wide, Nature single column
    'pdf.fonttype': 42,  # TrueType fonts for editable PDF
    'ps.fonttype': 42,
})

# ---------- Simulated data ----------
methods = ['Method A', 'Method B', 'Method C', 'Method D', 'Method E']
metrics = ['Accuracy', 'F1 Score', 'AUC']

# Mean values: shape (5 methods, 3 metrics)
np.random.seed(42)
means = np.array([
    [0.85, 0.82, 0.90],
    [0.78, 0.75, 0.84],
    [0.92, 0.89, 0.95],
    [0.80, 0.77, 0.86],
    [0.88, 0.85, 0.92],
])

# Standard deviations: shape (5 methods, 3 metrics)
stds = np.array([
    [0.03, 0.04, 0.02],
    [0.05, 0.06, 0.04],
    [0.02, 0.03, 0.01],
    [0.04, 0.05, 0.03],
    [0.03, 0.04, 0.02],
])

# ---------- Colors (Nature-friendly palette) ----------
colors = ['#E64B35', '#4DBBD5', '#00A087']  # Red, Teal, Green

# ---------- Create figure ----------
fig, ax = plt.subplots()

x = np.arange(len(methods))  # [0, 1, 2, 3, 4]
width = 0.22  # Bar width
offsets = [-width, 0, width]  # Center 3 bars around each x position

for i, (metric, color) in enumerate(zip(metrics, colors)):
    bars = ax.bar(
        x + offsets[i],
        means[:, i],
        width,
        yerr=stds[:, i],
        label=metric,
        color=color,
        edgecolor='white',
        linewidth=0.3,
        capsize=1.5,
        error_kw={'linewidth': 0.5, 'capthick': 0.5},
    )

# ---------- Axis formatting ----------
ax.set_xlabel('Method', labelpad=4)
ax.set_ylabel('Score', labelpad=4)
ax.set_xticks(x)
ax.set_xticklabels(methods, rotation=0)
ax.set_ylim(0, 1.05)
ax.set_yticks(np.arange(0, 1.1, 0.2))

# Legend outside plot area
ax.legend(
    frameon=False,
    loc='upper left',
    bbox_to_anchor=(0.0, 1.0),
    ncol=3,
    handlelength=1.2,
    handletextpad=0.4,
    columnspacing=0.8,
)

# Light horizontal gridlines
ax.yaxis.grid(True, linewidth=0.3, alpha=0.5, linestyle='-')
ax.set_axisbelow(True)

plt.tight_layout()

# ---------- Export ----------
output_dir = Path(__file__).parent

pdf_path = output_dir / 'nature_grouped_bar_chart.pdf'
png_path = output_dir / 'nature_grouped_bar_chart.png'

fig.savefig(pdf_path, bbox_inches='tight', pad_inches=0.05)
fig.savefig(png_path, bbox_inches='tight', pad_inches=0.05, facecolor='white')

plt.close(fig)

print(f"PDF saved: {pdf_path}")
print(f"PNG saved: {png_path}")
print("Done!")
