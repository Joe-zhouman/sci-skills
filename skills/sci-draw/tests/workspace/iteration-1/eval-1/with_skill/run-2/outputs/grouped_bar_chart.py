#!/usr/bin/env python3
"""
Nature-style grouped bar chart with error bars.
================================================

Figure Contract
---------------
Core conclusion: Compare the performance of 5 methods across 3 evaluation
metrics, showing both central tendency and variability.

Chart type: Grouped bar chart (categorical x = methods, grouped by metrics).
This is appropriate because:
  - x is categorical (5 methods), not continuous
  - We compare means across groups with known variability
  - n per cell is moderate (simulated as n=10 replicates per method-metric)

Journal: Nature single-column (89 mm = 3.5 in width)
Error bars: SD (standard deviation), n = 10 replicates per cell
Palette: seaborn colorblind (colorblind-safe)
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Add skill scripts to path
SKILL_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', '..', 'scripts')
)
sys.path.insert(0, SKILL_DIR)

from setup_style import setup_style
from export_figure import export_figure

# ============================================================
# Step 0: Figure contract (documented above in docstring)
# ============================================================

# ============================================================
# Step 1: Generate simulated data
# ============================================================
rng = np.random.default_rng(42)

methods = ['Method A', 'Method B', 'Method C', 'Method D', 'Method E']
metrics = ['Accuracy', 'F1 Score', 'AUC-ROC']
n_reps = 10  # replicates per cell

# Ground-truth means (each row = method, each col = metric)
true_means = np.array([
    [0.82, 0.78, 0.85],   # Method A
    [0.91, 0.88, 0.93],   # Method B (best)
    [0.76, 0.72, 0.80],   # Method C
    [0.87, 0.84, 0.90],   # Method D
    [0.79, 0.75, 0.82],   # Method E
])

# Ground-truth standard deviations
true_stds = np.array([
    [0.04, 0.05, 0.03],   # Method A
    [0.03, 0.04, 0.02],   # Method B
    [0.06, 0.07, 0.05],   # Method C
    [0.03, 0.04, 0.03],   # Method D
    [0.05, 0.06, 0.04],   # Method E
])

# Generate raw replicates and compute sample mean / std
raw_data = rng.normal(
    loc=true_means[:, :, np.newaxis],
    scale=true_stds[:, :, np.newaxis],
    size=(5, 3, n_reps),
)
raw_data = np.clip(raw_data, 0, 1)  # bounded to [0, 1]

sample_mean = raw_data.mean(axis=2)
sample_std = raw_data.std(axis=2, ddof=1)

# ============================================================
# Step 2: Chart selection rationale
# ============================================================
# Grouped bar chart is correct here:
#   - x is categorical (methods), not ordered continuous
#   - 3 metrics per method is manageable (not >12 combinations)
#   - Error bars with declared SD + n are appropriate
# P1 note: since these are aggregate metrics (not raw observations),
# a bar chart with error bars is the standard convention in ML papers.

# ============================================================
# Step 4: Configure Nature style
# ============================================================
setup_style(journal='nature', lang='en')

# Colorblind-safe palette (seaborn 'colorblind')
PALETTE = ['#0072B2', '#E69F00', '#009E73']  # blue, orange, green

# ============================================================
# Step 5: Plot
# ============================================================
fig, ax = plt.subplots(figsize=(3.5, 2.625))

n_methods = len(methods)
n_metrics = len(metrics)
bar_width = 0.22
gap = 0.08  # extra gap between method groups

x_base = np.arange(n_methods) * (n_metrics * bar_width + gap)

for j, (metric, color) in enumerate(zip(metrics, PALETTE)):
    offset = (j - (n_metrics - 1) / 2) * bar_width
    x_pos = x_base + offset

    bars = ax.bar(
        x_pos,
        sample_mean[:, j],
        width=bar_width,
        yerr=sample_std[:, j],
        label=f'{metric} (mean ± SD, n={n_reps})',
        color=color,
        edgecolor='black',
        linewidth=0.4,
        capsize=2,
        error_kw={'linewidth': 0.7, 'capthick': 0.7},
    )

ax.set_xticks(x_base)
ax.set_xticklabels(methods, fontsize=7)
ax.set_ylabel('Score', fontsize=8)
ax.set_ylim(0, 1.05)
ax.yaxis.set_major_locator(ticker.MultipleLocator(0.2))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))

# Legend: frameon=False for clean Nature look
ax.legend(
    frameon=False,
    fontsize=5.5,
    loc='upper left',
    bbox_to_anchor=(0.0, 1.0),
    handlelength=1.2,
    handletextpad=0.4,
    labelspacing=0.3,
)

# ============================================================
# Step 7: Export
# ============================================================
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
basename = os.path.join(OUTPUT_DIR, 'grouped_bar_chart')

paths = export_figure(
    fig,
    basename=basename,
    formats=['pdf', 'png'],
    size_inches=(3.5, 2.625),
    dpi=300,
    grayscale_preview=True,
)

print()
print('Exported files:')
for p in paths:
    print(f'  {p}')
    assert os.path.exists(p), f'File not found: {p}'
    size_kb = os.path.getsize(p) / 1024
    print(f'    ({size_kb:.1f} KB)')
