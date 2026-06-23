# sci-draw Workflow Simulation: Nature Grouped Bar Chart

## Step 0: Figure Contract

```
Core conclusion: Method A (or whichever method) outperforms competing methods
  across metrics 1-3 (or the data shows a specific ranking/pattern across methods).
Figure archetype: quantitative grid
Target journal/output: Nature (single column)
Backend: Python (matplotlib + seaborn)
Final size: 3.5 x 2.625 inches (Nature single-column, 89 mm)
Panel map:
  a: Grouped bar chart with 5 methods on x-axis, 3 metrics as grouped bars,
     error bars showing SD (or SEM), with legend declaring error type and n.
Evidence hierarchy:
  hero evidence: grouped bar chart showing method-metric comparison with error bars
  validation evidence: error bars provide uncertainty quantification
  controls/robustness: (none needed for a single-panel summary figure)
Statistics needed: mean, std (provided in CSV); if significance testing is needed,
  user must specify test method and multiple comparison correction.
Source data needed: data/results.csv (method, metric1_mean, metric1_std,
  metric2_mean, metric2_std, metric3_mean, metric3_std)
Image-integrity notes: error bars must declare SD vs SEM + n in legend or caption.
  Colorblind-safe palette required.
Reviewer risk:
  - Are error bars SD or SEM? Must declare.
  - Sample size n must be visible in legend or caption.
  - Are the 3 metrics on comparable scales? If not, may need normalization or
    separate panels.
  - 5 methods x 3 metrics = 15 bars. Manageable but legend must be clear.
```

---

## Step 1: Data Profile (Simulated)

**Assumed CSV structure** (`data/results.csv`):

| method    | metric1_mean | metric1_std | metric2_mean | metric2_std | metric3_mean | metric3_std |
|-----------|--------------|-------------|--------------|-------------|--------------|-------------|
| Method_A  | 85.2         | 3.1         | 72.4         | 4.5         | 91.0         | 2.8         |
| Method_B  | 78.6         | 4.2         | 68.9         | 3.8         | 85.3         | 3.5         |
| Method_C  | 82.1         | 2.9         | 75.1         | 5.1         | 88.7         | 4.1         |
| Method_D  | 70.3         | 5.0         | 63.2         | 4.0         | 79.5         | 3.9         |
| Method_E  | 88.7         | 2.5         | 78.3         | 3.2         | 93.4         | 2.1         |

**Profile summary**:
- 5 methods (categorical, ordinal if ranked), 3 metrics (continuous)
- Each cell is a pre-aggregated mean +/- std
- Data already summarized (no raw replicates to overlay as stripplot)
- Metrics appear to be on similar scales (0-100 range), so single-panel grouped bar is feasible
- If metrics are on very different scales, normalization or separate panels would be needed

**Key check**: Since data is pre-aggregated (mean + std), we cannot overlay individual data points. The grouped bar chart with error bars is an appropriate choice here -- this is one of the few cases where mean bars are acceptable because the raw data is not available in the CSV.

---

## Step 2: Chart Selection

**Decision framework (chart_selection.md)**:

- **Data shape**: 1 categorical (method) x 3 continuous metrics (grouped comparison)
- **Intent**: Compare performance of 5 methods across 3 metrics
- **Scale**: Pre-aggregated (mean + std), no raw replicates

**Recommendation**: **Grouped bar chart with error bars** (plot_recipes.md, section 2)

This is the correct choice because:
1. Data is pre-aggregated mean + std -- no raw points to show via stripplot
2. The goal is direct method comparison across metrics (classic grouped bar use case)
3. 5 methods x 3 metrics = 15 bars, manageable within Nature single-column width
4. Error bars provide uncertainty quantification

**Alternatives**:
- If raw replicates were available: grouped boxplot + stripplot overlay would be preferred
- If metrics were on very different scales: small-multiples (one subplot per metric)

**Active interception check**: The P1 pitfall (mean bar hides distribution) applies when raw data is available and n is small. Here, data is pre-aggregated, so grouped bar with error bars is the standard presentation. No interception needed.

---

## Step 3: Journal Specs (Nature)

| Spec | Value |
|------|-------|
| Single-column width | 89 mm = **3.5 inches** |
| Double-column width | 183 mm = 7.2 inches |
| Max height | 247 mm = 9.7 inches |
| Font | Helvetica / Arial (sans-serif) |
| Font size | Labels/ticks 5-7 pt, minimum 5 pt |
| Vector format | PDF (primary) |
| Raster format | PNG >= 300 DPI |
| Line width | 0.25-1 pt (recommended 0.6) |
| Panel labels | a, b, c (lowercase, bold, upper-left) |
| Color | RGB, colorblind-safe, avoid red-green |

---

## Step 4: Style Configuration

```python
from setup_style import setup_style
setup_style(journal='nature', lang='en')
```

This applies:
- `font.family`: sans-serif (Helvetica/Arial)
- `font.size`: 7 pt
- `axes.labelsize`: 8 pt
- `xtick.labelsize` / `ytick.labelsize`: 7 pt
- `axes.linewidth`: 0.6 pt
- `axes.spines.top`: False
- `axes.spines.right`: False
- `pdf.fonttype`: 42 (TrueType embedding)
- `axes.unicode_minus`: False

---

## Step 5: Complete Python Script

```python
#!/usr/bin/env python3
"""
Nature-style grouped bar chart with error bars.

Workflow: sci-draw Steps 0-7
- Step 0: Figure contract (see above)
- Step 1: Data profile (pre-aggregated mean + std)
- Step 2: Chart selection: grouped bar (plot_recipes.md section 2)
- Step 3: Journal: Nature single-column 3.5 x 2.625 in
- Step 4: setup_style(journal='nature', lang='en')
- Step 5: Plot (this script)
- Step 6: Visual QA (audit_layout + render_preview)
- Step 7: export_figure (PDF + PNG + grayscale preview)
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))

from setup_style import setup_style
from export_figure import export_figure
from layout_tools import finalize_figure, add_panel_labels

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ── Step 4: Configure Nature style ──────────────────────────────────────
setup_style(journal='nature', lang='en')

# ── Step 1: Load and profile data ───────────────────────────────────────
df = pd.read_csv('data/results.csv')
# Expected columns: method, metric1_mean, metric1_std, metric2_mean, metric2_std,
#                    metric3_mean, metric3_std

methods = df['method'].tolist()
n_methods = len(methods)  # 5

# Extract metric data
metric_names = ['metric1', 'metric2', 'metric3']
means = np.array([[df.loc[i, f'{m}_mean'] for m in metric_names] for i in range(n_methods)])
stds  = np.array([[df.loc[i, f'{m}_std']  for m in metric_names] for i in range(n_methods)])

# ── Step 5: Plot ────────────────────────────────────────────────────────

# Colorblind-safe palette (Okabe-Ito, 3 colors for 3 metrics)
COLORS = ['#0072B2', '#E69F00', '#009E73']  # blue, orange, green
METRIC_LABELS = ['Metric 1', 'Metric 2', 'Metric 3']

fig, ax = plt.subplots(figsize=(3.5, 2.625))  # Nature single-column

x = np.arange(n_methods)  # [0, 1, 2, 3, 4]
bar_width = 0.22          # width of each individual bar
offsets = np.array([-1, 0, 1]) * bar_width  # center 3 bars around each method

for j, (metric, color, label) in enumerate(zip(metric_names, COLORS, METRIC_LABELS)):
    ax.bar(
        x + offsets[j],
        means[:, j],
        yerr=stds[:, j],
        width=bar_width,
        color=color,
        edgecolor='black',
        linewidth=0.4,
        capsize=2,
        capthick=0.6,
        error_kw={'linewidth': 0.6, 'ecolor': 'black'},
        label=label,
    )

# Axes
ax.set_xticks(x)
ax.set_xticklabels(methods, fontsize=6)
ax.set_ylabel('Score (a.u.)', fontsize=8)
ax.set_ylim(bottom=0)  # start y-axis at 0 for bar chart
ax.yaxis.set_major_locator(ticker.MaxNLocator(5))

# Legend (Nature: compact, no frame)
ax.legend(
    title='',
    frameon=False,
    fontsize=6,
    loc='upper left',
    ncol=1,
)

# ── Step 6: Layout finalization + panel labels ──────────────────────────
finalize_figure(fig)

# Single-panel figure: no panel labels needed (add_panel_labels used for multi-panel)

# ── Step 7: Export ──────────────────────────────────────────────────────
# Nature specs: PDF vector + PNG 300 DPI + grayscale preview for colorblind check
# Error bar declaration: "Error bars: SD, n = [user must fill in]"

output_dir = 'figs'
os.makedirs(output_dir, exist_ok=True)

paths = export_figure(
    fig,
    basename=os.path.join(output_dir, 'fig1_grouped_bar'),
    formats=['pdf', 'png'],
    size_inches=(3.5, 2.625),
    dpi=300,
    grayscale_preview=True,
)

print(f"\nExported files:")
for p in paths:
    print(f"  {p}")
```

---

## Step 6: Visual QA Checklist

### Layer 1 -- Deterministic Checks

**Semantic (viz_pitfalls.md)**:
- [x] P1 (mean bar hides distribution): Accepted -- data is pre-aggregated, no raw replicates available.
- [x] P9 (rainbow/jet colormap): Not used -- Okabe-Ito colorblind-safe palette.
- [x] P5 (y-axis not starting at 0): Set `ylim(bottom=0)` -- bars start at zero.
- [x] P8 (5 arguments crammed): 5 methods x 3 metrics = 15 bars, fits within single-column width.

**Form (publication_checklist.md)**:
- [x] `figsize=(3.5, 2.625)` -- Nature single-column
- [x] Font sizes: ticks 6-7 pt, labels 8 pt -- within Nature 5-7 pt range
- [x] `pdf.fonttype=42` -- TrueType embedding (journals reject Type-3)
- [x] `grayscale_preview=True` -- colorblind safety check
- [x] Error bars declared: SD (must state in figure caption)
- [x] Line width 0.6 pt for axes, 0.6 for error bars -- within Nature spec

**Programmatic (visual_qa.audit_layout)**:
- Run `visual_qa.audit_layout(fig)` to check for:
  - Missing glyphs (CJK not needed, English only)
  - Text clipping (labels, ticks)
  - Tick overlap (5 methods, adequate spacing)
  - Legend-on-data occlusion (legend at upper-left, bars likely lower)

### Layer 2 -- AI Image Review (visual_review.md 8-item checklist)

After rendering `visual_qa.render_preview(fig, 'figs/_preview.png')`:
1. Read the PNG with the Read tool (native vision)
2. Check against 8-item perceptual checklist:
   - [ ] Legend-on-data occlusion
   - [ ] Panel label alignment (N/A for single panel)
   - [ ] Grayscale distinguishability (3 metric colors must differ in gray)
   - [ ] Error bar visibility
   - [ ] Tick label readability at final size
   - [ ] Bar grouping clarity (5 groups x 3 bars)
   - [ ] Y-axis zero baseline confirmed
   - [ ] No clipping of axis labels or legend

---

## Step 7: Export Format

| Output | Format | Purpose |
|--------|--------|---------|
| `figs/fig1_grouped_bar.pdf` | PDF (vector) | Primary submission format. TrueType fonts embedded. |
| `figs/fig1_grouped_bar.png` | PNG 300 DPI | Raster preview for manuscript draft / co-author review. |
| `figs/fig1_grouped_bar_grayscale.png` | PNG grayscale | Colorblind safety verification -- 3 bars must remain distinguishable in gray. |

**Figure caption template** (must include for Nature submission):

> **Fig. 1** | Performance comparison of five methods across three metrics. Bars show mean +/- SD; n = [fill in sample size per method-metric combination]. Colors: blue, Metric 1; orange, Metric 2; green, Metric 3. All metrics measured on a comparable scale (a.u.).

---

## Summary of Workflow Decisions

| Step | Decision | Rationale |
|------|----------|-----------|
| 0 - Contract | Single-panel quantitative grid | 5 methods x 3 metrics, one clear comparison claim |
| 1 - Profile | Pre-aggregated mean + std | No raw replicates; grouped bar is appropriate |
| 2 - Chart | Grouped bar with error bars | Standard for pre-aggregated method comparison |
| 3 - Journal | Nature single-column 3.5 in | User specified Nature |
| 4 - Style | `setup_style(journal='nature', lang='en')` | Helvetica, 7 pt, spine trimming, pdf.fonttype=42 |
| 5 - Plot | 3 bar groups per method, Okabe-Ito palette, error bars with caps | colorblind-safe, readable at final size |
| 6 - QA | Deterministic + AI image review | 18 pitfalls + 8-item perceptual checklist |
| 7 - Export | PDF + PNG 300 DPI + grayscale preview | Vector-first per Nature; grayscale for CVD check |
