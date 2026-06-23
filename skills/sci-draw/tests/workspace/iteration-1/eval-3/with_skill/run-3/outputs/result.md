# Scatter + Regression for Two Continuous Gene Expression Variables

## Figure Contract

```
Core conclusion:    Gene expression levels of X and Y are correlated, and this
                    relationship differs by disease status.
Figure archetype:   quantitative grid (single-panel scatter with regression)
Target journal:     Nature Methods
Final size:         3.5 x 2.625 inches (Nature single-column, 89 mm)
Panel map:
  a: Scatter plot with per-group regression lines + 95% CI bands,
     Pearson r and p annotated, colorblind-safe dual encoding
Evidence hierarchy:
  hero evidence:     scatter + regression showing correlation structure
  validation:        r/p values annotated directly on plot
Statistics needed:   Pearson r, two-sided p per group
Source data needed:  CSV with columns: sample_id, gene_x, gene_y, disease_status
Image-integrity notes: synthetic demo data; replace with real measurements
Reviewer risk:       ensure colorblind safety (dual encoding: color + marker);
                     alpha for n=200 to avoid overplotting; declare n in legend
```

## Recommendation

**Chart choice: Scatter + regression + 95% CI + annotated r/p** -- this is the canonical
visualization for two continuous variables examining a relationship, with a third categorical
dimension (disease status) mapped via color and marker shape (dual encoding).

Per the chart selection framework:
- Two continuous variables --> scatter + regression line + 95% CI band
- Third dimension is categorical --> `hue` (color) + `style` (marker) dual encoding
- n=200 total --> use `alpha=0.7` to prevent overplotting while preserving density information
- Nature Methods --> 3.5 in single-column, Helvetica/Arial, 5-7 pt labels, 300 DPI, PDF vector

**Why not alternatives:**
- Line plot: x is not ordered continuous (P6 violation)
- Hexbin/2D KDE: n=200 is moderate, scatter is still readable; hexbin hides individual samples
- Heatmap: only 2 variables, not a correlation matrix

**Colorblind safety:** Okabe-Ito palette (seaborn `colorblind`) + distinct marker shapes
(circle, square, triangle) ensures distinguishability even in grayscale.

## Complete Python Script

```python
"""
sci-draw :: Scatter + regression for two continuous gene expression variables
Target: Nature Methods, single-column (3.5 x 2.625 in)
Features: colorblind-safe dual encoding (color + marker), per-group regression
          with 95% CI, annotated Pearson r/p, grayscale preview.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'scripts'))

from setup_style import setup_style
from export_figure import export_figure

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

# ============================================================
# Step 4: Configure Nature Methods style
# ============================================================
setup_style(journal='nature', lang='en')

# Okabe-Ito colorblind-safe palette
PAL = sns.color_palette('colorblind')

# ============================================================
# Step 1: Simulate data (replace with real CSV load)
# ============================================================
rng = np.random.default_rng(42)
n_per_group = 100
groups = ['Healthy', 'Disease']
markers = ['o', 's']  # circle vs square for dual encoding

dfs = []
for i, g in enumerate(groups):
    x = rng.normal(loc=5 + i * 1.5, scale=1.2, size=n_per_group)
    y = 0.6 * x + rng.normal(loc=i * 0.8, scale=0.8, size=n_per_group)
    dfs.append(pd.DataFrame({'Gene_X': x, 'Gene_Y': y, 'Disease_Status': g}))
df = pd.concat(dfs, ignore_index=True)

# ============================================================
# Step 5: Plot -- scatter + regression + r/p annotation
# ============================================================
fig, ax = plt.subplots(figsize=(3.5, 2.625))

for i, (group, color, marker) in enumerate(zip(groups, PAL[:2], markers)):
    sub = df[df['Disease_Status'] == group]

    # Scatter with dual encoding: color + marker shape
    ax.scatter(
        sub['Gene_X'], sub['Gene_Y'],
        c=[color], marker=marker,
        s=20, alpha=0.7, edgecolor='black', linewidth=0.3,
        label=f'{group} (n={len(sub)})',
    )

    # Regression line + 95% CI band
    sns.regplot(
        data=sub, x='Gene_X', y='Gene_Y',
        scatter=False, color=color,
        line_kws={'lw': 1.0, 'ls': '-' if i == 0 else '--'},
        ci=95,
        ax=ax,
    )

    # Annotate Pearson r and p
    r, p = pearsonr(sub['Gene_X'], sub['Gene_Y'])
    ax.text(
        0.05, 0.95 - i * 0.10,
        f'{group}: r = {r:.2f}, p = {p:.1e}',
        transform=ax.transAxes, fontsize=6, color=color,
        va='top', ha='left',
        bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=1),
    )

ax.set_xlabel('Gene X expression (a.u.)')
ax.set_ylabel('Gene Y expression (a.u.)')
ax.legend(
    title='Disease status', frameon=False,
    loc='lower right', fontsize=6, title_fontsize=7,
)

# ============================================================
# Step 7: Export at Nature Methods final size
# ============================================================
output_dir = os.path.join(os.path.dirname(__file__), 'outputs')
os.makedirs(output_dir, exist_ok=True)

export_figure(
    fig,
    basename=os.path.join(output_dir, 'fig_scatter_gene_expression'),
    formats=['pdf', 'png'],
    size_inches=(3.5, 2.625),
    dpi=300,
    grayscale_preview=True,
)

plt.close(fig)
print('Done. Check outputs/ for PDF, PNG, and grayscale preview.')
```

## Visual QA Checklist (Pre-Export)

### Layer 1 -- Deterministic Checks

| Check | Status | Notes |
|---|---|---|
| Figsize = 3.5 x 2.625 in | PASS | Nature single-column |
| Font: Helvetica/Arial, 6-8 pt | PASS | setup_style('nature') |
| PDF fonttype 42 (TrueType) | PASS | setup_style sets pdf.fonttype=42 |
| Colorblind palette (Okabe-Ito) | PASS | seaborn 'colorblind' |
| Dual encoding (color + marker) | PASS | circles vs squares |
| Regression line + 95% CI | PASS | sns.regplot with ci=95 |
| Pearson r/p annotated | PASS | ax.text on plot |
| n declared in legend | PASS | 'Healthy (n=100)', 'Disease (n=100)' |
| No pie/3D/rainbow/jet | PASS | clean scatter |
| No dual Y-axis | PASS | single axis |
| No P1-P15 pitfalls triggered | PASS | scatter is correct chart type |
| Grayscale preview generated | PASS | export_figure(grayscale_preview=True) |

### Layer 2 -- Visual Review Notes

After rendering, verify:
1. Legend does not occlude data points (placed in lower-right empty region)
2. Regression CI bands are distinguishable between groups
3. Grayscale preview: circles vs squares still distinguishable
4. Panel label alignment (single panel, no label needed)
5. Axis labels readable at 3.5 in final size

## Legend/Caption Text (for manuscript)

> **Fig. X | Relationship between Gene X and Gene Y expression by disease status.**
> Scatter plot showing expression levels of Gene X (x-axis) and Gene Y (y-axis) in
> Healthy (n = 100, circles) and Disease (n = 100, squares) samples. Solid and dashed
> lines indicate per-group linear regression fits; shaded bands represent 95% confidence
> intervals. Pearson correlation coefficients and two-sided p-values are annotated.
> Colors follow the Okabe-Ito colorblind-safe palette. a.u., arbitrary units.
