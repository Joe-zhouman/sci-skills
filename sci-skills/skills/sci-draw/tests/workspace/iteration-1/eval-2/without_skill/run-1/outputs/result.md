# Mean Bar Chart with Error Bars — Approach and Output

## 1. Approach

For a bar chart showing means with error bars for 3 groups (n=6 each) suitable for a Science paper, I would:

1. Use **matplotlib** as the plotting library — it is the standard Python tool for publication-quality figures.
2. Compute the **mean** and **standard error of the mean (SEM)** for each group. SEM is the appropriate error bar metric for displaying precision of the mean estimate (SEM = std / sqrt(n)).
3. Create a clean, minimal bar chart with error bars (caps on the error bars).
4. Apply publication-quality formatting: no top/right spines, clear axis labels, appropriate font sizes, and tight layout.
5. Export as **PDF** (vector format, required by most journals including Science) at 300+ DPI equivalent quality.

## 2. Full Python Script

```python
"""
Bar chart with mean +/- SEM error bars for 3 groups (n=6 each).
Publication-quality figure for Science paper.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# ── Publication-style defaults ────────────────────────────────────────
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 8,
    "axes.labelsize": 9,
    "axes.titlesize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "axes.linewidth": 0.8,
    "xtick.major.width": 0.8,
    "ytick.major.width": 0.8,
    "xtick.major.size": 3,
    "ytick.major.size": 3,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
})

# ── Sample data (replace with your actual measurements) ──────────────
# Each group has n = 6 observations
np.random.seed(42)
group_A = np.array([4.2, 4.5, 4.1, 4.8, 4.3, 4.6])   # Group A
group_B = np.array([5.1, 5.4, 5.0, 5.7, 5.2, 5.5])   # Group B
group_C = np.array([6.0, 6.3, 5.9, 6.6, 6.1, 6.4])   # Group C

groups = [group_A, group_B, group_C]
group_names = ["Group A", "Group B", "Group C"]

# ── Compute mean and SEM ─────────────────────────────────────────────
n = 6
means = [np.mean(g) for g in groups]
sems  = [np.std(g, ddof=1) / np.sqrt(n) for g in groups]   # SEM = s / sqrt(n)

# ── Create figure ────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(3.5, 2.8))   # single-column width for Science

x_pos = np.arange(len(groups))
bar_width = 0.55

bars = ax.bar(
    x_pos,
    means,
    width=bar_width,
    color="#4C72B0",          # muted blue — prints well in greyscale
    edgecolor="black",
    linewidth=0.8,
    yerr=sems,
    error_kw={
        "ecolor": "black",
        "capsize": 4,
        "capthick": 0.8,
        "elinewidth": 0.8,
    },
    zorder=3,
)

# ── Axis formatting ──────────────────────────────────────────────────
ax.set_xticks(x_pos)
ax.set_xticklabels(group_names)
ax.set_ylabel("Measurement (units)")

# Remove top and right spines (publication standard)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# Y-axis starts at 0
ax.set_ylim(bottom=0)

# Light horizontal grid for readability
ax.yaxis.grid(True, linestyle="--", alpha=0.4, zorder=0)
ax.set_axisbelow(True)

plt.tight_layout()

# ── Save outputs ─────────────────────────────────────────────────────
fig.savefig("bar_chart_mean_sem.pdf")       # vector PDF (primary, for submission)
fig.savefig("bar_chart_mean_sem.png", dpi=300)  # raster PNG (for preview)
plt.close(fig)

print("Saved: bar_chart_mean_sem.pdf")
print("Saved: bar_chart_mean_sem.png")
```

## 3. Formatting Applied

| Element               | Choice                                   | Rationale                                      |
|-----------------------|------------------------------------------|------------------------------------------------|
| Font                  | Arial / Helvetica, 8-9 pt               | Science journal standard sans-serif            |
| Figure size           | 3.5 x 2.8 inches                        | Single-column width for Science (3.5 in max)   |
| Spines                | Top and right removed                    | Standard publication style, reduces clutter     |
| Error bars            | SEM (std/sqrt(n)), caps, black           | SEM is standard for showing mean precision      |
| Bar color             | Muted blue (#4C72B0) with black edges    | Reproduces well in both color and greyscale     |
| Grid                  | Light horizontal dashed lines            | Aids reading values without visual noise        |
| DPI                   | 300                                      | Meets journal print requirements                |
| Y-axis                | Starts at zero                           | Avoids misleading visual distortion of bars     |
| Layout                | tight_layout with minimal padding        | Maximizes figure area within allowed dimensions |

## 4. Export Format

- **Primary**: PDF (vector) — required for journal submission; scales without quality loss.
- **Secondary**: PNG at 300 DPI — for manuscript preview and supplementary use.

Both files are saved to the working directory when the script is run.
