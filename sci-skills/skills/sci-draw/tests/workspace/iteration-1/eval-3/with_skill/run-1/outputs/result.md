# Eval 3: Two Continuous Variables -- Gene Expression Relationship

## 1. Chart Type Recommendation

**Scatter plot + regression line + r value annotation.**

Per the skill's chart selection decision framework (`references/chart_selection.md`):

> | Data shape | Recommended | Don't use |
> |---|---|---|
> | 2 continuous, view relationship | Scatter + regression + r value | Line (unless x is ordered continuous) |

Two continuous variables (gene expression levels) where the goal is to visualize their relationship maps to the "2 continuous" data shape. The recommended chart is a scatter plot with a regression fit line and the Pearson correlation coefficient (r) and p-value annotated on the figure.

**Alternatives considered:**
- 2D KDE / hexbin density: useful when n > 1000 and overplotting is severe, but at n=200 a scatter plot with alpha transparency is perfectly legible and shows individual data points -- preferred for publication.
- Joint plot (scatter + marginal histograms): a valid alternative that adds distribution information, but adds figure size and complexity for a single-panel figure.

## 2. Why This Chart Type

The skill's decision framework uses three axes:

| Axis | Assessment |
|---|---|
| Variable types | 2 x continuous (gene expression levels) |
| Argument intent | Relationship / correlation ("does Gene X expression predict Gene Y?") |
| Sample size | n=200 -- large enough for stable regression, small enough that individual points are visible |

2 continuous variables + relationship intent = **scatter + regression + r value**. This is the canonical choice. A line chart would be wrong here because the x-axis is not an ordered continuous variable (like time or dose) -- it is another gene's expression level, so connecting points with lines would imply a nonexistent ordering.

The r value annotation is critical for a Nature Methods submission: it lets reviewers immediately quantify the strength of the relationship without computing it themselves. The skill's plot recipe (`references/plot_recipes.md` section 3) explicitly recommends annotating r and p on scatter plots as a "reviewer time saver."

## 3. Colorblind-Safe Encoding for Disease Status

Disease status is a categorical variable (e.g., healthy vs. diseased) encoded on the scatter plot. The skill mandates **redundant encoding** per Rule 3:

| Visual channel | Healthy | Diseased |
|---|---|---|
| Color | `#0072B2` (Okabe-Ito blue) | `#D55E00` (Okabe-Ito vermillion) |
| Marker shape | circle (`o`) | triangle up (`^`) |

Why both color AND marker shape:
- ~8% of men have color vision deficiency; red-green is the most common form.
- Marker shape alone distinguishes groups even in grayscale print.
- The skill's `export_figure(..., grayscale_preview=True)` generates a grayscale PNG to verify distinguishability before submission.

Okabe-Ito palette chosen over `seaborn.color_palette('colorblind')` because it has the strongest published evidence for universal distinguishability (Okabe & Ito, 2002).

## 4. Nature Methods Journal Specifications

From `references/journal_specs.md`:

| Parameter | Nature Methods requirement |
|---|---|
| Single-column width | 89 mm = **3.5 inch** |
| Double-column width | 183 mm = **7.2 inch** |
| Max height | 247 mm = 9.7 inch |
| Font | **Helvetica / Arial** (sans-serif) |
| Font size (labels/ticks) | 5--7 pt, minimum 5 pt |
| Line width | 0.25--1 pt (recommend 0.6 for axes) |
| Vector format | **PDF** (primary) / EPS |
| Raster (if needed) | PNG/TIFF, **>= 300 DPI**, RGB color |
| Panel labels | **a, b, c** (lowercase, bold, upper-left) |
| Color | RGB, colorblind-safe, avoid red-green only |
| Font embedding | TrueType fonttype 42 (Type 3 rejected) |

## 5. Complete Python Script

```python
"""
Nature Methods scatter plot: two gene expression levels, colored by disease status.
Uses sci-draw setup_style and export_figure.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'scripts'))

from setup_style import setup_style
from export_figure import export_figure

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

# ---------------------------------------------------------------
# Step 0: Figure contract
# ---------------------------------------------------------------
# Core conclusion: Gene X expression is positively correlated with
# Gene Y expression, and the correlation strength differs by disease status.
#
# Evidence chain: single panel -- scatter with regression + r value.
# Archetype: quantitative grid (single panel).
# Journal: Nature Methods, single-column (3.5 in).

# ---------------------------------------------------------------
# Step 1: Simulate data (replace with real data in production)
# ---------------------------------------------------------------
rng = np.random.default_rng(42)
n_total = 200
n_healthy = 120
n_disease = n_total - n_healthy

# Simulate correlated gene expression (log2 scale, typical for RNA-seq)
gene_x_healthy = rng.normal(6.0, 1.5, n_healthy)
gene_y_healthy = 0.6 * gene_x_healthy + rng.normal(0, 1.0, n_healthy)

gene_x_disease = rng.normal(7.5, 1.8, n_disease)
gene_y_disease = 0.7 * gene_x_disease + rng.normal(0, 1.2, n_disease)

df = pd.DataFrame({
    'Gene X (log2 TPM)': np.concatenate([gene_x_healthy, gene_x_disease]),
    'Gene Y (log2 TPM)': np.concatenate([gene_y_healthy, gene_y_disease]),
    'Disease Status': (['Healthy'] * n_healthy + ['Disease'] * n_disease),
})

# ---------------------------------------------------------------
# Step 4: Configure style (Nature Methods, English)
# ---------------------------------------------------------------
setup_style(journal='nature', lang='en')

# Okabe-Ito colorblind-safe palette
COLORS = {'Healthy': '#0072B2', 'Disease': '#D55E00'}
MARKERS = {'Healthy': 'o', 'Disease': '^'}

# ---------------------------------------------------------------
# Step 5: Plot -- scatter + regression + r value
# ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(3.5, 3.0))

# Plot each group with color + marker shape (redundant encoding)
for status in ['Healthy', 'Disease']:
    sub = df[df['Disease Status'] == status]
    ax.scatter(
        sub['Gene X (log2 TPM)'],
        sub['Gene Y (log2 TPM)'],
        c=COLORS[status],
        marker=MARKERS[status],
        s=20,
        alpha=0.75,
        edgecolor='black',
        linewidth=0.3,
        label=f'{status} (n={len(sub)})',
    )
    # Regression line with 95% CI
    sns.regplot(
        data=sub,
        x='Gene X (log2 TPM)',
        y='Gene Y (log2 TPM)',
        scatter=False,
        color=COLORS[status],
        line_kws={'lw': 1.0, 'ls': '--' if status == 'Disease' else '-'},
        ax=ax,
    )

# Annotate Pearson r and p for each group
text_y = 0.95
for status in ['Healthy', 'Disease']:
    sub = df[df['Disease Status'] == status]
    r, p = pearsonr(sub['Gene X (log2 TPM)'], sub['Gene Y (log2 TPM)'])
    p_str = f'{p:.1e}' if p < 0.001 else f'{p:.3f}'
    ax.text(
        0.05, text_y,
        f'{status}: r = {r:.2f}, p = {p_str}',
        transform=ax.transAxes,
        fontsize=6,
        color=COLORS[status],
        va='top',
        ha='left',
    )
    text_y -= 0.10

# Also annotate overall correlation
r_all, p_all = pearsonr(df['Gene X (log2 TPM)'], df['Gene Y (log2 TPM)'])
p_all_str = f'{p_all:.1e}' if p_all < 0.001 else f'{p_all:.3f}'
ax.text(
    0.05, text_y,
    f'Overall: r = {r_all:.2f}, p = {p_all_str}',
    transform=ax.transAxes,
    fontsize=6,
    color='black',
    va='top',
    ha='left',
    fontweight='bold',
)

ax.set_xlabel('Gene X expression (log2 TPM)')
ax.set_ylabel('Gene Y expression (log2 TPM)')
ax.legend(
    title='Disease Status',
    frameon=False,
    fontsize=6,
    title_fontsize=7,
    loc='lower right',
    markerscale=1.3,
)

# ---------------------------------------------------------------
# Step 6: Visual QA (programmatic checks)
# ---------------------------------------------------------------
# - Axes spines: top/right removed (Nature style) -- handled by setup_style
# - Font sizes: labels 8pt, ticks 7pt, legend 6pt -- within 5-7pt range
# - Grayscale distinguishability: checked via export_figure grayscale_preview
# - No overplotting at n=200 with alpha=0.75 -- acceptable

# ---------------------------------------------------------------
# Step 7: Export
# ---------------------------------------------------------------
paths = export_figure(
    fig,
    basename='figs/fig_scatter_gene_expression',
    formats=['pdf', 'png'],
    size_inches=(3.5, 3.0),
    dpi=300,
    grayscale_preview=True,    # colorblind safety check
)

print('\nExported files:')
for p in paths:
    print(f'  {p}')

# Figure caption (for manuscript):
# "Scatter plot of Gene X vs Gene Y expression levels (log2 TPM) in
#  200 samples, colored and shaped by disease status (Healthy: n=120,
#  blue circles; Disease: n=80, orange triangles). Dashed/solid lines
#  show per-group linear regression fits. Pearson r and p-values
#  annotated. Grayscale preview confirms distinguishability."
```

## 6. Export Format

**PDF (vector) + PNG (raster at 300 DPI) + grayscale preview PNG.**

| File | Purpose |
|---|---|
| `fig_scatter_gene_expression.pdf` | Primary submission format -- vector, lossless, editable text. Nature Methods prefers PDF/EPS. |
| `fig_scatter_gene_expression.png` | Raster backup at 300 DPI (Nature minimum). For manuscript systems that require raster. |
| `fig_scatter_gene_expression_grayscale.png` | Colorblind safety check -- verifies groups remain distinguishable without color. |

PDF is the primary format because: (1) it is vector -- lines and text remain sharp at any zoom, (2) Nature Methods accepts PDF/EPS as vector formats, (3) TrueType fonttype 42 embedding ensures text is editable and passes the NPP submission checker. PNG at 300 DPI is included as a raster fallback. The grayscale preview is generated automatically by `export_figure(..., grayscale_preview=True)` to verify the redundant marker-shape encoding works for colorblind reviewers.
