"""
sci-draw eval-2: Boxplot + stripplot for 3 groups, n=6 each.

Intercepted from user's original request for mean bar chart.
Reason: n=6 per group is too small for mean bars -- bars hide the distribution
and individual data points. Boxplot + stripplot overlay shows all 6 points per
group, the median, IQR, and range, giving reviewers full transparency.
"""

import sys
import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Add the skill's scripts directory to path
SKILL_SCRIPTS = "/home/joe/Documents/repo/skill/sci-draw/sci-draw/scripts"
sys.path.insert(0, SKILL_SCRIPTS)

from setup_style import setup_style
from export_figure import export_figure

# --- Step 1: Apply publication style (Science journal, English) ---
info = setup_style(journal="science", lang="en")
print(f"Style applied: {info}")

# --- Step 2: Inline data -- 3 groups, n=6 each ---
np.random.seed(42)
data = {
    "Group": (["Control"] * 6 + ["Treatment A"] * 6 + ["Treatment B"] * 6),
    "Value": [
        # Control: moderate values
        12.3, 14.1, 11.8, 13.5, 12.9, 15.2,
        # Treatment A: higher values
        18.7, 20.1, 17.4, 19.8, 21.3, 18.2,
        # Treatment B: moderate-high with more spread
        16.5, 22.1, 14.8, 19.3, 17.9, 23.6,
    ],
}
df = pd.DataFrame(data)

print(f"\nData summary:")
print(df.groupby("Group")["Value"].describe())

# --- Step 3: Create figure -- boxplot + stripplot overlay ---
fig, ax = plt.subplots(figsize=(4.7, 3.0))

# Colorblind-safe palette
palette = sns.color_palette("colorblind", 3)

# Boxplot: shows median, IQR, whiskers (1.5*IQR)
sns.boxplot(
    data=df,
    x="Group",
    y="Value",
    palette=palette,
    width=0.5,
    linewidth=0.8,
    fliersize=0,  # hide outlier points (stripplot will show them)
    ax=ax,
)

# Stripplot overlay: show ALL individual data points (n=6 per group)
sns.stripplot(
    data=df,
    x="Group",
    y="Value",
    color="black",
    size=4,
    jitter=0.15,
    alpha=0.7,
    edgecolor="white",
    linewidth=0.3,
    ax=ax,
)

# Labels
ax.set_xlabel("")
ax.set_ylabel("Measurement (a.u.)")

# Add legend annotation: error type + n (mandatory for Science)
ax.text(
    0.5, -0.15,
    "Box: median + IQR; dots: individual replicates; n = 6 per group.",
    transform=ax.transAxes, fontsize=6, ha="center", va="top",
    style="italic",
)

# --- Step 4: Export ---
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
basename = os.path.join(OUTPUT_DIR, "fig_boxplot_stripplot")

paths = export_figure(
    fig,
    basename=basename,
    formats=["pdf", "png"],
    size_inches=(4.7, 3.0),
    dpi=300,
    grayscale_preview=True,
)

print(f"\nExported files:")
for p in paths:
    print(f"  {p}")

plt.close(fig)
print("\nDone.")
