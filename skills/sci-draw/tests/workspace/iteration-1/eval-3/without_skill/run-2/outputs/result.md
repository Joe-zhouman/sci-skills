# Scatter Plot for Gene Expression Relationship - Nature Methods Submission

## Best Visualization Approach

For two continuous variables (gene expression levels) from 200 samples colored by disease status, a **scatter plot** is the optimal choice:

- **Scatter plots** reveal the joint distribution, correlation, and group separation
- **Color coding** by disease status enables immediate visual comparison
- **Different markers** (circle vs triangle) provide redundancy for colorblind accessibility

## Nature Methods Formatting Requirements

| Element | Specification |
|---------|---------------|
| Single column width | 89 mm (3.5 in) |
| Double column width | 183 mm (7.2 in) |
| Font | Arial or Helvetica, 5-7 pt |
| Line width | 0.25-1 pt |
| Resolution | 300 DPI (print), 1000+ DPI (line art) |
| Color palette | Colorblind-friendly |

## Python Script

```python
#!/usr/bin/env python3
"""
Scatter plot of gene expression levels for Nature Methods submission.
200 samples, 2 groups (healthy vs disease), 2 continuous variables.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# ============================================================
# Nature Methods formatting guidelines
# ============================================================
# - Single column: 89 mm (3.5 in), Double column: 183 mm (7.2 in)
# - Font: Arial or Helvetica, 5-7 pt in print
# - Line width: 0.25-1 pt
# - DPI: 300 for print, 1000+ for line art
# - Color: use colorblind-friendly palettes
# ============================================================

# --- Set up Nature Methods style ---
mpl.rcParams.update({
    # Font
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 7,
    'axes.labelsize': 7,
    'axes.titlesize': 7,
    'xtick.labelsize': 6,
    'ytick.labelsize': 6,
    'legend.fontsize': 6,

    # Axes
    'axes.linewidth': 0.5,
    'axes.spines.top': False,
    'axes.spines.right': False,

    # Ticks
    'xtick.major.width': 0.5,
    'ytick.major.width': 0.5,
    'xtick.major.size': 3,
    'ytick.major.size': 3,
    'xtick.direction': 'in',
    'ytick.direction': 'in',

    # Lines
    'lines.linewidth': 0.5,

    # Legend
    'legend.frameon': False,
    'legend.borderaxespad': 0,

    # Figure
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.05,
})

# --- Generate synthetic data (200 samples) ---
np.random.seed(42)

# Gene A expression (continuous, arbitrary units)
# Healthy: lower expression, Disease: higher expression
n_samples = 200
n_healthy = 100
n_disease = 100

# Gene A (x-axis): Healthy ~ N(5, 1.5), Disease ~ N(8, 1.8)
gene_a_healthy = np.random.normal(loc=5.0, scale=1.5, size=n_healthy)
gene_a_disease = np.random.normal(loc=8.0, scale=1.8, size=n_disease)

# Gene B (y-axis): correlated with Gene A + noise
# Healthy: ~ N(4, 1.2), Disease: ~ N(7, 1.5)
gene_b_healthy = 0.6 * gene_a_healthy + np.random.normal(loc=1.0, scale=1.0, size=n_healthy)
gene_b_disease = 0.5 * gene_a_disease + np.random.normal(loc=1.5, scale=1.2, size=n_disease)

# Combine
gene_a = np.concatenate([gene_a_healthy, gene_a_disease])
gene_b = np.concatenate([gene_b_healthy, gene_b_disease])
status = np.array(['Healthy'] * n_healthy + ['Disease'] * n_disease)

# --- Color palette (colorblind-friendly, Nature-style) ---
# Using a palette similar to Nature Methods publications
color_healthy = '#377EB8'   # Blue
color_disease = '#E41A1C'   # Red

# --- Create figure (single column width: 89 mm ≈ 3.5 inches) ---
fig, ax = plt.subplots(figsize=(3.5, 3.0))

# Plot scatter for each group
for label, color, marker in [('Healthy', color_healthy, 'o'),
                               ('Disease', color_disease, '^')]:
    mask = status == label
    ax.scatter(gene_a[mask], gene_b[mask],
               c=color,
               marker=marker,
               s=20,           # marker size
               alpha=0.7,
               edgecolors='white',
               linewidths=0.3,
               label=label,
               zorder=3)

# --- Labels ---
ax.set_xlabel('Gene A expression (a.u.)')
ax.set_ylabel('Gene B expression (a.u.)')

# --- Legend ---
ax.legend(loc='upper left', frameon=False, fontsize=6)

# --- Grid (optional, subtle) ---
ax.grid(True, alpha=0.2, linewidth=0.3)

# --- Tight layout ---
fig.tight_layout()

# --- Save outputs ---
output_dir = '/home/joe/Documents/repo/skill/sci-draw/sci-draw/tests/workspace/iteration-1/eval-3/without_skill/run-2/outputs'

# PDF (vector, for submission)
fig.savefig(f'{output_dir}/scatter_gene_expression.pdf',
            format='pdf', dpi=300, bbox_inches='tight')

# PNG (raster, for preview)
fig.savefig(f'{output_dir}/scatter_gene_expression.png',
            format='png', dpi=300, bbox_inches='tight')

plt.close()

print("Figures saved successfully:")
print(f"  PDF: {output_dir}/scatter_gene_expression.pdf")
print(f"  PNG: {output_dir}/scatter_gene_expression.png")
```

## Output Files

- `scatter_gene_expression.pdf` - Vector format for journal submission
- `scatter_gene_expression.png` - Raster format for preview/manuscript draft

## Key Design Decisions

1. **Colorblind-friendly palette**: Blue (#377EB8) for Healthy, Red (#E41A1C) for Disease
2. **Redundant encoding**: Different markers (circle vs triangle) supplement color
3. **Single column figure**: 3.5 inches wide, appropriate for Nature Methods
4. **Minimal chart junk**: Removed top/right spines, subtle grid
5. **Inward ticks**: Standard for scientific publications
6. **White edge colors**: Distinguishes overlapping points
