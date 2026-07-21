#!/home/joe/Documents/repo/skill/sci-draw/sci-draw/.venv/bin/python3
"""
Generate a Nature-formatted line plot with error bands for tumor volume data.
Treatment groups: Control, Drug_A, Drug_B, Drug_C (n=8 biological replicates each).
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from pathlib import Path

# ── Nature formatting constants ──────────────────────────────────────────────
NATURE_WIDTH_MM = 183          # double-column width in mm
NATURE_WIDTH_IN = NATURE_WIDTH_MM / 25.4
NATURE_DPI = 300
FONT_SIZE_PT = 7               # Nature recommends 5-7 pt
AXIS_LABEL_PT = 8
TICK_LABEL_PT = 7
LINE_WIDTH_PT = 0.75
CAP_SIZE_PT = 3
MARKER_SIZE_PT = 4

OUTPUT_DIR = Path(__file__).parent
np.random.seed(42)

# ── Generate synthetic tumor volume data ─────────────────────────────────────
time_points = np.array([0, 3, 7, 10, 14, 17, 21])  # days
n_replicates = 8

# Baseline tumor volume ~ 100 mm3, exponential-ish growth with treatment effects
growth_rate = {
    "Control": 0.12,
    "Drug_A": 0.07,
    "Drug_B": 0.04,
    "Drug_C": 0.09,
}
noise_sd = {
    "Control": 8,
    "Drug_A": 7,
    "Drug_B": 6,
    "Drug_C": 7,
}
baseline = 100

groups = list(growth_rate.keys())
group_data = {}  # {group: array shape (n_replicates, n_timepoints)}

for group in groups:
    rate = growth_rate[group]
    sd = noise_sd[group]
    data = np.zeros((n_replicates, len(time_points)))
    for rep in range(n_replicates):
        trajectory_noise = np.random.normal(0, sd)
        for i, t in enumerate(time_points):
            vol = baseline * np.exp(rate * t) + trajectory_noise + np.random.normal(0, 3)
            data[rep, i] = max(vol, 0)
    group_data[group] = data

# ── Compute group statistics (mean +/- SEM) ──────────────────────────────────
group_means = {}
group_sems = {}
for group in groups:
    group_means[group] = group_data[group].mean(axis=0)
    group_sems[group] = group_data[group].std(axis=0, ddof=1) / np.sqrt(n_replicates)

# ── Colour palette (colour-blind friendly, Nature-compatible) ────────────────
COLORS = {
    "Control": "#444444",
    "Drug_A": "#E69F00",
    "Drug_B": "#0072B2",
    "Drug_C": "#CC79A7",
}
MARKERS = {
    "Control": "o",
    "Drug_A": "s",
    "Drug_B": "^",
    "Drug_C": "D",
}

# ── Configure matplotlib for Nature style ────────────────────────────────────
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": FONT_SIZE_PT,
    "axes.labelsize": AXIS_LABEL_PT,
    "axes.titlesize": AXIS_LABEL_PT,
    "xtick.labelsize": TICK_LABEL_PT,
    "ytick.labelsize": TICK_LABEL_PT,
    "legend.fontsize": TICK_LABEL_PT,
    "lines.linewidth": LINE_WIDTH_PT,
    "lines.markersize": MARKER_SIZE_PT,
    "axes.linewidth": 0.6,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "xtick.major.size": 3,
    "ytick.major.size": 3,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.dpi": NATURE_DPI,
    "savefig.dpi": NATURE_DPI,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
    "pdf.fonttype": 42,        # editable text in Illustrator
    "ps.fonttype": 42,
    "svg.fonttype": "none",
})

# ── Create figure ────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(NATURE_WIDTH_IN, NATURE_WIDTH_IN * 0.72))

for group in groups:
    color = COLORS[group]
    marker = MARKERS[group]
    mean = group_means[group]
    sem = group_sems[group]

    # Error band (SEM)
    ax.fill_between(
        time_points,
        mean - sem,
        mean + sem,
        alpha=0.18,
        color=color,
        linewidth=0,
    )
    # Mean line with markers
    ax.plot(
        time_points,
        mean,
        color=color,
        marker=marker,
        markersize=MARKER_SIZE_PT,
        markerfacecolor="white",
        markeredgewidth=0.6,
        markeredgecolor=color,
        linewidth=LINE_WIDTH_PT,
        label=group.replace("_", " "),
        zorder=3,
    )

# ── Axis labels and limits ───────────────────────────────────────────────────
ax.set_xlabel("Days post-treatment")
ax.set_ylabel("Tumor volume (mm³)")
ax.set_xlim(time_points[0] - 0.5, time_points[-1] + 0.5)
ax.set_ylim(bottom=0)
ax.set_xticks(time_points)

# Legend outside plot area, no frame
ax.legend(
    frameon=False,
    loc="upper left",
    handlelength=1.5,
    handletextpad=0.5,
    columnspacing=0.8,
    borderaxespad=0.3,
)

# ── Save outputs ─────────────────────────────────────────────────────────────
pdf_path = OUTPUT_DIR / "tumor_volume_nature.pdf"
png_path = OUTPUT_DIR / "tumor_volume_nature.png"

fig.savefig(pdf_path, format="pdf")
fig.savefig(png_path, format="png")
plt.close(fig)

print(f"PDF saved: {pdf_path}")
print(f"PNG saved: {png_path}")
print(f"Groups: {groups}")
print(f"Time points: {time_points.tolist()}")
print(f"Replicates per group: {n_replicates}")
print(f"Total data points: {len(groups) * n_replicates * len(time_points)}")
