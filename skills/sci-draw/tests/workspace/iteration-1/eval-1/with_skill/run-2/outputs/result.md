# sci-draw Workflow Simulation: Nature Grouped Bar Chart

## Step 0: Figure Contract

```
Core conclusion:
  Method X outperforms competing approaches across all three evaluation metrics.

Figure archetype:
  quantitative grid

Target journal/output:
  Nature (single-column)

Backend:
  Python (matplotlib + seaborn)

Final size:
  3.5 in x 2.625 in (89 mm x 66.7 mm, Nature single-column, 4:3 ratio)

Panel map:
  a: Grouped bar chart — 5 methods x 3 metrics with error bars (mean +/- SD)

Evidence hierarchy:
  hero evidence:  metric1 differences across methods
  validation evidence: metric2, metric3 confirm consistent ranking
  controls/robustness: error bars show within-method variability

Statistics needed:
  Mean and SD already pre-computed per method per metric

Source data needed:
  data/results.csv (method, metric1_mean, metric1_std, metric2_mean, metric2_std, metric3_mean, metric3_std)

Image-integrity notes:
  N/A (no microscopy or imaging)

Reviewer risk:
  - Are error bars SD or SEM? Must declare in legend/caption.
  - Sample size n not visible in the figure itself — must state in caption.
  - 5 methods x 3 metrics = 15 bars; ensure x-axis labels are readable at 7pt.
  - Colorblind safety: 3 metric groups must use redundant encoding.
```

## Step 1: Data Profile (Simulated)

The CSV has this structure:

| Column | Type | Notes |
|--------|------|-------|
| method | Categorical (5 levels) | x-axis grouping |
| metric1_mean, metric1_std | Continuous | First performance metric |
| metric2_mean, metric2_std | Continuous | Second performance metric |
| metric3_mean, metric3_std | Continuous | Third performance metric |

**Key observations:**
- 5 methods x 3 metrics = 15 data points (grouped bar chart: 5 groups, 3 bars each)
- Each bar has an associated SD error bar
- No raw replicates in the file — only pre-computed mean +/- SD
- No missing values expected (summary table format)

## Step 2: Chart Selection

**Recommendation: Grouped bar chart with error bars**

**Rationale:**
- Data is pre-computed summary statistics (mean + SD), not raw observations. A grouped bar chart is the standard visual for comparing k methods across m metrics when only summaries are available.
- 5 groups x 3 bars = 15 bars total — within the readable range for a single-column figure.
- The claim is "method ranking across metrics" — bars side-by-side make direct comparison trivial.

**Alternatives considered and rejected:**
1. **Radar/spider chart**: Poor perceptual accuracy for comparing areas; Nature does not publish them.
2. **Grouped dot plot with error bars**: Valid alternative, but bars are conventional for this data shape in Nature-style papers.
3. **Heatmap (methods x metrics)**: Loses the visual impact of magnitude differences; error bars cannot be shown.

**Active interception check:**
- P1 (mean bar hides distribution): NOT triggered here because the data IS pre-computed summaries, not raw observations. The user has no individual data points to show. The error bars (SD) are the appropriate uncertainty representation.
- P6 (connecting categorical x with lines): NOT triggered — we use bars, not lines.

## Step 3: Journal Specifications (Nature)

| Specification | Value |
|---------------|-------|
| Journal | Nature |
| Layout | Single-column |
| Figure width | 3.5 in (89 mm) |
| Figure height | 2.625 in (66.7 mm, 4:3 ratio) |
| Font family | Helvetica / Arial (sans-serif) |
| Font size (labels) | 7-8 pt |
| Font size (ticks) | 7 pt |
| Font size (minimum) | >= 6 pt |
| DPI (raster) | 300 |
| Vector format | PDF (primary), EPS accepted |
| Line width | 0.6-1.0 pt |
| Spine style | Top and right spines OFF |
| Sub-panel labels | a, b, c (lowercase, bold, upper-left) |
| Color policy | Colorblind-safe; avoid red-green |
| Font embedding | TrueType (fonttype 42) |

## Step 4-7: Complete Python Script

```python
"""
Nature-style grouped bar chart with error bars.
5 methods x 3 metrics, mean +/- SD.

Uses: setup_style, export_figure, finalize_figure, add_panel_labels
"""

import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# --- Import sci-draw tools ---
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from setup_style import setup_style
from export_figure import export_figure
from layout_tools import finalize_figure, add_panel_labels

# ============================================================
# Step 4: Configure Nature style
# ============================================================
info = setup_style(journal='nature', lang='en')
# -> Helvetica/Arial, 7pt, constrained_layout ON, top/right spines OFF,
#    pdf.fonttype=42, axes.unicode_minus=False

# ============================================================
# Load data
# ============================================================
df = pd.read_csv('data/results.csv')
# Expected columns: method, metric1_mean, metric1_std,
#                    metric2_mean, metric2_std, metric3_mean, metric3_std

methods = df['method'].tolist()               # 5 methods
metric_names = ['metric1', 'metric2', 'metric3']

# Build arrays for grouped bars
n_methods = len(methods)                       # 5
n_metrics = len(metric_names)                  # 3

means = np.array([
    [df[f'{m}_mean'].iloc[i] for m in metric_names]
    for i in range(n_methods)
])  # shape (5, 3)

stds = np.array([
    [df[f'{m}_std'].iloc[i] for m in metric_names]
    for i in range(n_methods)
])  # shape (5, 3)

# ============================================================
# Color palette: colorblind-safe, 3 distinct metrics
# ============================================================
# Okabe-Ito subset: blue, orange, green (distinguishable in grayscale)
METRIC_COLORS = ['#0072B2', '#E69F00', '#009E73']
METRIC_HATCHES = ['', '///', '...']  # redundant encoding for grayscale

# ============================================================
# Step 5: Plot grouped bar chart
# ============================================================
fig, ax = plt.subplots(figsize=(3.5, 2.625))  # Nature single-column

bar_width = 0.22
x = np.arange(n_methods)

for j, (metric, color, hatch) in enumerate(
    zip(metric_names, METRIC_COLORS, METRIC_HATCHES)
):
    offset = (j - (n_metrics - 1) / 2) * bar_width
    bars = ax.bar(
        x + offset,
        means[:, j],
        width=bar_width,
        yerr=stds[:, j],
        label=metric,
        color=color,
        edgecolor='black',
        linewidth=0.4,
        errorbar_kw={
            'linewidth': 0.8,
            'capsize': 2,
            'capthick': 0.8,
            'elinewidth': 0.8,
        },
        hatch=hatch,
        alpha=0.9,
    )

# X-axis
ax.set_xticks(x)
ax.set_xticklabels(methods, fontsize=7, rotation=0)
ax.set_xlabel('Method', fontsize=8)

# Y-axis
ax.set_ylabel('Score', fontsize=8)
ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.1f'))

# Legend: upper-left, no frame, small font
ax.legend(
    title='',
    frameon=False,
    fontsize=6,
    loc='upper left',
    bbox_to_anchor=(0.0, 1.0),
    ncol=1,
)

# ============================================================
# Step 6: Layout finalization + panel labels
# ============================================================
finalize_figure(fig)                    # constrained_layout fallback
# Single panel — no panel label needed for a standalone figure.
# If this were part of a multi-panel figure, uncomment:
# add_panel_labels(fig, style='nature')

# ============================================================
# Step 7: Export
# ============================================================
output_dir = 'figs'
os.makedirs(output_dir, exist_ok=True)

paths = export_figure(
    fig,
    basename=os.path.join(output_dir, 'fig1_method_comparison'),
    formats=['pdf', 'png'],
    size_inches=(3.5, 2.625),
    dpi=300,
    grayscale_preview=True,    # colorblind safety check
)

print(f"\nExported files:")
for p in paths:
    print(f"  {p}")

# ============================================================
# Figure caption (for manuscript)
# ============================================================
caption = (
    "Fig. 1 | Performance comparison of five methods across three evaluation "
    "metrics. Bars represent mean +/- SD; n = [STATE SAMPLE SIZE] per method. "
    "Metric definitions: [DEFINE metric1, metric2, metric3]. "
    "Statistical tests: [STATE TEST AND CORRECTION IF APPLICABLE]."
)
print(f"\nCaption:\n{caption}")
```

## Design Decisions Summary

### Chart Type
**Grouped bar chart** — the data is pre-computed summary statistics (mean + SD per method per metric). This is the standard form for method-comparison tables in Nature papers. No raw data points are available, so stripplot overlay is not applicable.

### Error Bars
- **Type**: SD (standard deviation) — declared in figure caption
- **Cap size**: 2 pt, cap thickness 0.8 pt
- **Line width**: 0.8 pt (Nature standard: 0.25-1.0 pt range)
- **Caption must state**: "Bars represent mean +/- SD; n = [X] per method"

### Color Strategy
- **Palette**: Okabe-Ito subset (blue #0072B2, orange #E69F00, green #009E73)
- **Redundant encoding**: Different hatch patterns (none, diagonal, dotted) for grayscale distinguishability
- **Grayscale preview**: `export_figure(grayscale_preview=True)` generates a `_grayscale.png` for colorblind safety verification
- **Avoided**: Red-green contrast (P13 violation)

### Typography
- **Font**: Helvetica (Nature specification)
- **Axis labels**: 8 pt
- **Tick labels**: 7 pt
- **Legend**: 6 pt (minimum readable at 3.5 in width)
- **Font embedding**: TrueType fonttype 42 (PDF)

### Layout
- **figsize**: (3.5, 2.625) — Nature single-column, 4:3 ratio
- **Spines**: Top and right OFF (Nature convention)
- **constrained_layout**: ON (via `setup_style` + `finalize_figure`)
- **Export**: `bbox_inches='tight'` with 0.05 in padding

### Pitfalls Avoided
| Pitfall | Status | Notes |
|---------|--------|-------|
| P1 (mean bar hides distribution) | NOT triggered | Data is pre-computed summaries, not raw observations |
| P6 (categorical x with lines) | NOT triggered | Using bars, not lines |
| P9 (error type undeclared) | Addressed | SD declared in caption |
| P13 (red-green contrast) | Avoided | Okabe-Ito blue/orange/green |
| P17 (text clipping) | Addressed | constrained_layout + tight bbox |

### Export Format
- **PDF** (vector, primary): For manuscript submission — lossless, editable text, fonttype 42
- **PNG** (raster, 300 DPI): For visual QA review and supplementary
- **PNG grayscale** (auto-generated): For colorblind safety check
- **No JPEG**: Prohibited for data figures (P11)
