"""
Publication-quality bar chart with error bars for Science paper.
3 groups, n=6 each, showing mean +/- SEM.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# ── Publication formatting (Science journal style) ──────────────────────────
mpl.rcParams.update({
    # Font
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 7,
    'axes.labelsize': 8,
    'axes.titlesize': 8,
    'xtick.labelsize': 7,
    'ytick.labelsize': 7,
    'legend.fontsize': 7,
    # Lines & axes
    'axes.linewidth': 0.6,
    'xtick.major.width': 0.6,
    'ytick.major.width': 0.6,
    'xtick.major.size': 3,
    'ytick.major.size': 3,
    'xtick.direction': 'out',
    'ytick.direction': 'out',
    'axes.spines.top': False,
    'axes.spines.right': False,
    # Figure
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.05,
    # Legend / grid
    'axes.grid': False,
})

# ── Inline data: 3 groups, n=6 each ────────────────────────────────────────
np.random.seed(42)
group_A = np.array([12.3, 14.1, 11.8, 13.5, 15.0, 12.9])   # Control
group_B = np.array([18.7, 20.2, 17.5, 19.8, 21.3, 18.1])   # Treatment 1
group_C = np.array([25.4, 23.8, 27.1, 24.6, 26.0, 25.9])   # Treatment 2

groups = [group_A, group_B, group_C]
labels = ['Control', 'Treatment 1', 'Treatment 2']

# ── Compute mean and SEM ────────────────────────────────────────────────────
means = [np.mean(g) for g in groups]
sems  = [np.std(g, ddof=1) / np.sqrt(len(g)) for g in groups]  # SEM = SD / sqrt(n)

# ── Color palette (colorblind-friendly, muted) ──────────────────────────────
colors = ['#4472C4', '#ED7D31', '#70AD47']  # blue, orange, green

# ── Create figure (single-column Science width ~ 3.5 in) ────────────────────
fig, ax = plt.subplots(figsize=(3.5, 2.8))

x = np.arange(len(groups))
bar_width = 0.55

bars = ax.bar(
    x, means, bar_width,
    yerr=sems,
    color=colors,
    edgecolor='black',
    linewidth=0.6,
    capsize=3,
    error_kw={'elinewidth': 0.8, 'capthick': 0.8},
    zorder=3,
)

# ── Axis labels ─────────────────────────────────────────────────────────────
ax.set_xlabel('Group')
ax.set_ylabel('Measurement (a.u.)')
ax.set_xticks(x)
ax.set_xticklabels(labels)

# ── Y-axis: start at 0, add headroom for error bars ─────────────────────────
ax.set_ylim(0, max(m + s for m, s in zip(means, sems)) * 1.15)

# ── Thin horizontal reference line at y=0 ───────────────────────────────────
ax.axhline(0, color='black', linewidth=0.4, zorder=1)

# ── Add individual data points (jittered) for transparency ──────────────────
for i, (g, color) in enumerate(zip(groups, colors)):
    jitter = np.random.normal(0, 0.04, size=len(g))
    ax.scatter(
        np.full_like(g, i, dtype=float) + jitter, g,
        s=12, color='white', edgecolor='black', linewidth=0.4,
        zorder=4, alpha=0.85,
    )

# ── Save ────────────────────────────────────────────────────────────────────
fig.savefig('bar_chart_mean_errorbar.pdf')
fig.savefig('bar_chart_mean_errorbar.png')
plt.close(fig)

print("Saved: bar_chart_mean_errorbar.pdf")
print("Saved: bar_chart_mean_errorbar.png")
print(f"Means:  {means}")
print(f"SEMs:   {sems}")
