# Visualizing Two Continuous Gene Expression Variables by Disease Status

## 1. Approach

For two continuous gene expression variables from 200 samples, colored by disease status, a **scatter plot** is the most appropriate visualization. Each point represents one sample, with the x-axis showing one gene's expression, the y-axis showing the other, and color encoding disease status (e.g., healthy vs. diseased).

Additional considerations:
- If disease status has only 2 categories, use two distinct, colorblind-safe colors.
- Add a legend to map colors to disease groups.
- Include axis labels with gene names and units (e.g., log2 TPM).
- Add a subtle grid for readability.
- Use a clean, minimal style suitable for a high-impact journal like Nature Methods.

## 2. Python Script

```python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# --- Simulated data (replace with your actual data) ---
np.random.seed(42)
n_samples = 200
n_healthy = 120
n_diseased = n_samples - n_healthy

# Simulated log2 expression values
gene_a_healthy = np.random.normal(loc=6.0, scale=1.5, size=n_healthy)
gene_b_healthy = np.random.normal(loc=5.5, scale=1.2, size=n_healthy)
gene_a_diseased = np.random.normal(loc=8.5, scale=1.8, size=n_diseased)
gene_b_diseased = np.random.normal(loc=7.0, scale=1.5, size=n_diseased)

gene_a = np.concatenate([gene_a_healthy, gene_a_diseased])
gene_b = np.concatenate([gene_b_healthy, gene_b_diseased])
status = np.array(["Healthy"] * n_healthy + ["Diseased"] * n_diseased)

# --- Color palette (colorblind-safe) ---
colors = {"Healthy": "#4472C4", "Diseased": "#ED7D31"}

# --- Figure setup ---
fig, ax = plt.subplots(figsize=(4.5, 4.0), dpi=300)

# --- Plot each group separately for proper legend ---
for group_name in ["Healthy", "Diseased"]:
    mask = status == group_name
    ax.scatter(
        gene_a[mask],
        gene_b[mask],
        c=colors[group_name],
        label=group_name,
        s=30,
        alpha=0.7,
        edgecolors="white",
        linewidths=0.4,
    )

# --- Axis labels ---
ax.set_xlabel("Gene A expression (log2 TPM)", fontsize=10, fontweight="bold")
ax.set_ylabel("Gene B expression (log2 TPM)", fontsize=10, fontweight="bold")

# --- Title (optional for Nature Methods, often omitted; included here for completeness) ---
# ax.set_title("Gene A vs Gene B Expression", fontsize=11, fontweight="bold")

# --- Legend ---
legend = ax.legend(
    title="Disease Status",
    fontsize=8,
    title_fontsize=9,
    frameon=True,
    fancybox=False,
    edgecolor="black",
    linewidth=0.6,
    loc="upper left",
)

# --- Tick formatting ---
ax.tick_params(axis="both", labelsize=9, direction="out", length=4, width=0.8)
ax.xaxis.set_major_locator(ticker.MaxNLocator(5))
ax.yaxis.set_major_locator(ticker.MaxNLocator(5))

# --- Spine styling (Nature Methods style: keep top and right spines, but lighter) ---
for spine in ax.spines.values():
    spine.set_linewidth(0.8)
    spine.set_color("black")

# --- Grid ---
ax.grid(True, linestyle="--", linewidth=0.4, alpha=0.4)
ax.set_axisbelow(True)

# --- Layout ---
fig.tight_layout()

# --- Save ---
# Vector format (PDF) for print; PNG for initial review
fig.savefig("gene_expression_scatter.pdf", format="pdf", bbox_inches="tight", dpi=300)
fig.savefig("gene_expression_scatter.png", format="png", bbox_inches="tight", dpi=300)

plt.show()
```

## 3. Formatting Applied

| Element | Setting |
|---|---|
| Figure size | 4.5 x 4.0 inches (single-column width for Nature Methods) |
| Resolution | 300 DPI |
| Color palette | Colorblind-safe blue (#4472C4) and orange (#ED7D31) |
| Point style | Size 30, 70% opacity, white edge for separation |
| Font sizes | Axis labels 10pt bold, tick labels 9pt, legend 8/9pt |
| Legend | Bordered frame, upper left position |
| Spines | All four kept, black, 0.8pt linewidth |
| Grid | Dashed, light, placed behind data |
| Tick marks | Outward, 4pt length, MaxNLocator(5) |

## 4. Export Format

- **Primary (for submission):** PDF -- vector format, scalable, preferred by Nature Methods for figures.
- **Secondary (for review):** PNG at 300 DPI -- convenient for sharing drafts and quick review.
- Nature Methods requires figures at a minimum of 300 DPI for raster formats and vector formats (PDF/EPS) for line art and plots.
