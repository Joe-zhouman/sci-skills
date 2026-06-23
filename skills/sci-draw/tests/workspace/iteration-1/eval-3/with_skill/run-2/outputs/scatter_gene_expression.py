"""
Scatter plot: Gene expression levels (200 samples, 2 groups)
- Continuous X: Gene A expression
- Continuous Y: Gene B expression
- Color: Disease status (Healthy vs Disease)
- Dual encoding: different markers per group
- Regression line + r value annotation
- Nature Methods submission quality
"""
import sys
sys.path.insert(0, "/home/joe/Documents/repo/skill/sci-draw/sci-draw/scripts")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

from setup_style import setup_style
from export_figure import export_figure

# --- Step 0: Setup style for Nature ---
setup_style(journal="nature", lang="en")

# --- Generate inline data (200 samples, 2 groups) ---
rng = np.random.default_rng(42)

n_healthy = 100
n_disease = 100

# Gene A expression (continuous)
gene_a_healthy = rng.normal(loc=5.0, scale=1.5, size=n_healthy)
gene_a_disease = rng.normal(loc=7.0, scale=1.8, size=n_disease)

# Gene B expression correlated with Gene A (continuous), different for groups
gene_b_healthy = 0.6 * gene_a_healthy + rng.normal(loc=2.0, scale=1.0, size=n_healthy)
gene_b_disease = 0.8 * gene_a_disease + rng.normal(loc=1.0, scale=1.2, size=n_disease)

gene_a = np.concatenate([gene_a_healthy, gene_a_disease])
gene_b = np.concatenate([gene_b_healthy, gene_b_disease])
status = ["Healthy"] * n_healthy + ["Disease"] * n_disease

df = pd.DataFrame({
    "Gene A expression (log2 TPM)": gene_a,
    "Gene B expression (log2 TPM)": gene_b,
    "Disease status": status,
})

# --- Compute overall regression ---
slope, intercept, r_value, p_value, std_err = stats.linregress(
    df["Gene A expression (log2 TPM)"],
    df["Gene B expression (log2 TPM)"],
)

# --- Plot ---
palette = sns.color_palette("colorblind")
color_map = {"Healthy": palette[0], "Disease": palette[1]}
marker_map = {"Healthy": "o", "Disease": "^"}

fig, ax = plt.subplots(figsize=(3.5, 2.625))

for group in ["Healthy", "Disease"]:
    subset = df[df["Disease status"] == group]
    ax.scatter(
        subset["Gene A expression (log2 TPM)"],
        subset["Gene B expression (log2 TPM)"],
        c=[color_map[group]],
        marker=marker_map[group],
        s=18,
        alpha=0.7,
        edgecolors="white",
        linewidths=0.3,
        label=group,
    )

# Regression line (overall)
x_range = np.linspace(df["Gene A expression (log2 TPM)"].min(),
                       df["Gene A expression (log2 TPM)"].max(), 200)
ax.plot(x_range, intercept + slope * x_range, color="gray", linewidth=1.0,
        linestyle="--", label=f"r = {r_value:.2f}")

# r value annotation on plot
p_str = f"p < 0.001" if p_value < 0.001 else f"p = {p_value:.3f}"
ax.annotate(
    f"r = {r_value:.2f}\n{p_str}",
    xy=(0.05, 0.95), xycoords="axes fraction",
    ha="left", va="top",
    fontsize=7,
    bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="gray", alpha=0.8),
)

ax.set_xlabel("Gene A expression (log2 TPM)")
ax.set_ylabel("Gene B expression (log2 TPM)")

ax.legend(frameon=False, loc="lower right", fontsize=7)

# --- Export ---
OUT_DIR = "/home/joe/Documents/repo/skill/sci-draw/sci-draw/tests/workspace/iteration-1/eval-3/with_skill/run-2/outputs"

paths = export_figure(
    fig,
    basename=f"{OUT_DIR}/scatter_gene_expression",
    formats=["pdf", "png"],
    size_inches=(3.5, 2.625),
    dpi=300,
    grayscale_preview=True,
)

print("\nDone. Exported files:")
for p in paths:
    print(f"  {p}")
