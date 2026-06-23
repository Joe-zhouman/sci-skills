#!/usr/bin/env python3
"""
Scatter plot of two gene expression variables colored by disease status.
Formatted for Nature Methods submission.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

# ── Nature Methods formatting ─────────────────────────────────────────
# Single column: 89 mm (3.5 in), Double column: 183 mm (7.2 in)
FIG_WIDTH = 3.5   # inches (single column)
FIG_HEIGHT = 3.2  # inches

rcParams.update({
    # Font
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 7,
    'axes.labelsize': 8,
    'axes.titlesize': 8,
    'xtick.labelsize': 6,
    'ytick.labelsize': 6,
    'legend.fontsize': 6,

    # Lines & markers
    'axes.linewidth': 0.6,
    'lines.linewidth': 0.5,
    'xtick.major.width': 0.6,
    'ytick.major.width': 0.6,
    'xtick.major.size': 3,
    'ytick.major.size': 3,

    # Axes
    'axes.spines.top': False,
    'axes.spines.right': False,

    # Figure
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.05,

    # Legend
    'legend.frameon': False,
    'legend.borderpad': 0.3,
    'legend.handlelength': 1.0,
})

# ── Simulate data ─────────────────────────────────────────────────────
np.random.seed(42)
n = 200

# Two gene expression variables with a moderate correlation
mean_expr = [6.5, 8.0]
cov = [[1.0, 0.55],
       [0.55, 1.2]]
data = np.random.multivariate_normal(mean_expr, cov, size=n)

# Disease status: 0 = Healthy, 1 = Disease
disease_status = np.random.binomial(1, 0.45, size=n)

gene_x = data[:, 0]
gene_y = data[:, 1]

# ── Color palette (color-blind friendly) ───────────────────────────────
colors = {0: '#4472C4', 1: '#C00000'}   # blue / red
labels = {0: 'Healthy', 1: 'Disease'}

# ── Plot ───────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(FIG_WIDTH, FIG_HEIGHT))

for status in [0, 1]:
    mask = disease_status == status
    ax.scatter(gene_x[mask], gene_y[mask],
               c=colors[status],
               s=12,               # marker size (pt^2)
               alpha=0.7,
               edgecolors='none',
               label=labels[status],
               zorder=3)

# Regression line (overall)
z = np.polyfit(gene_x, gene_y, 1)
x_line = np.linspace(gene_x.min(), gene_x.max(), 100)
ax.plot(x_line, np.polyval(z, x_line),
        color='#555555', linewidth=0.8, linestyle='--', zorder=2)

# Labels
ax.set_xlabel('Gene A expression (log₂)')
ax.set_ylabel('Gene B expression (log₂)')

# Legend
ax.legend(loc='upper left', markerscale=1.5)

# ── Pearson r annotation ──────────────────────────────────────────────
from scipy import stats
r, p = stats.pearsonr(gene_x, gene_y)
ax.text(0.97, 0.03,
        f'r = {r:.2f}, P = {p:.1e}',
        transform=ax.transAxes,
        ha='right', va='bottom',
        fontsize=6, color='#333333')

# ── Export ─────────────────────────────────────────────────────────────
output_dir = '/home/joe/Documents/repo/skill/sci-draw/sci-draw/tests/workspace/iteration-1/eval-3/without_skill/run-3/outputs'

fig.savefig(f'{output_dir}/scatter_expression.pdf')
fig.savefig(f'{output_dir}/scatter_expression.png')

plt.close(fig)
print('Saved: scatter_expression.pdf  scatter_expression.png')
