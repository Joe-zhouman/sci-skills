# sci-draw Skill Evaluation: P1 Interception Case

## Task

User request: "I have 3 groups with n=6 each. I want a bar chart showing the mean with error bars for my Science paper."

---

## Step 0: Figure Contract (Abbreviated)

```
Core conclusion:  [User must specify] e.g., "Group X shows higher response than Groups Y and Z"
Figure archetype: quantitative grid
Target journal:   Science
Backend:          Python (matplotlib + seaborn)
Final size:       1.5-col = 4.7 inch (120 mm); or single-col = 2.2 inch (55 mm)
Panel map:
  a: group comparison (1 categorical x 1 continuous)
Evidence hierarchy:
  hero evidence: group differences in measured response
Statistics needed: user must declare test + correction
Source data needed: 3 groups x 6 replicates
Reviewer risk: P1 — mean bar with n=6 hides distribution
```

---

## Step 1: Data Profile Summary

- **Structure**: 1 categorical variable (3 groups) x 1 continuous variable (response)
- **Sample size**: n = 6 per group (total N = 18)
- **Per-group n < 10**: triggers small-sample interception

Key finding: n=6 per group is firmly in the "n < 10" zone where the chart selection
framework and P1 pitfall rule both forbid a bare mean bar chart.

---

## Step 2: Active Interception Dialogue

> **P1 Interception -- Mean Bar Chart with n < 10 per Group**
>
> The "mean bar chart with error bars" you requested triggers the classic P1 error
> (mean bar hides distribution): with only n = 6 per group, a bar's height plus one
> error bar cannot communicate the true data distribution to the reader. A reviewer
> at Science would likely request "show individual data points" -- and in 2020+,
> multiple journals (PLoS Biology, Nature Methods) have publicly called for an end
> to bare mean bars with small samples.
>
> **Why this matters for n = 6:**
> - n = 6 and n = 600 look identical as bare bars -- no way to judge evidence strength
> - A bimodal distribution, severe skew, or a single outlier driving the mean is invisible
> - Science's figure guidelines emphasize showing data, not just summaries
>
> **Recommended alternative: boxplot + stripplot overlay**
> - The boxplot shows median, IQR, and range at a glance
> - The stripplot overlay shows all 6 individual data points per group -- hiding nothing
> - This is actually more convincing to a reviewer than a bare bar
> - The code is only ~3 extra lines compared to a bar chart
>
> If you need to show means explicitly, I can add a mean marker (diamond or horizontal
> line) inside each boxplot so the mean is still visible alongside the full distribution.
>
> **Proceed with the recommended boxplot + stripplot, or stick with the original bar chart?**

---

## Step 3: Journal Specs (Science)

| Spec | Value |
|---|---|
| Single-column width | 55 mm = 2.2 inch |
| 1.5-column width | 120 mm = 4.7 inch |
| Double-column width | 183 mm = 7.2 inch |
| Font | Helvetica / Arial (sans-serif) |
| Font size | 5-7 pt labels and ticks |
| Vector format | PDF / EPS |
| Raster DPI | >= 300 (600 for line art) |
| Panel labels | A, B, C (uppercase, bold, top-left) |

Given 3 groups with a simple comparison, a single-column (2.2 inch) figure may be
too narrow for a boxplot + stripplot to be legible. **Recommend 1.5-column (4.7 inch)
or at minimum 3.5 inch** to give each group enough horizontal space.

---

## Step 4-7: Intercepted Solution Script (Boxplot + Stripplot)

The following script produces a publication-ready boxplot + stripplot for Science,
replacing the requested mean bar chart. All 6 data points per group are visible.

```python
#!/usr/bin/env python3
"""
Intercepted solution: boxplot + stripplot for 3 groups, n=6 each.
Original request was mean bar chart -- intercepted per P1 (n<10 mean bar forbidden).
Target: Science journal, 1.5-column (4.7 inch) or single-column (3.5 inch).
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from setup_style import setup_style
from export_figure import export_figure

# --- Step 4: Configure style for Science ---
setup_style(journal='science', lang='en')

# Okabe-Ito colorblind-safe palette (3 groups)
PAL = ['#0072B2', '#E69F00', '#009E73']

# --- Demo data (replace with your actual data) ---
rng = np.random.default_rng(42)
groups = ['Group A', 'Group B', 'Group C']
n_per_group = 6

df = pd.DataFrame({
    'group': np.repeat(groups, n_per_group),
    'value': np.concatenate([
        rng.normal(loc=5.0, scale=1.2, size=n_per_group),
        rng.normal(loc=7.5, scale=1.5, size=n_per_group),
        rng.normal(loc=6.0, scale=0.9, size=n_per_group),
    ]),
})

# --- Step 5: Plot boxplot + stripplot ---
# Science 1.5-col = 4.7 inch; height chosen for readable aspect ratio
fig, ax = plt.subplots(figsize=(4.7, 3.0))

# Boxplot: show median + IQR, hide outlier markers (stripplot shows all points)
sns.boxplot(
    data=df, x='group', y='value',
    palette=PAL,
    showfliers=False,       # do not duplicate outlier markers
    width=0.5,
    linewidth=0.8,
    boxprops=dict(edgecolor='black', linewidth=0.8),
    medianprops=dict(color='black', linewidth=1.0),
    whiskerprops=dict(color='black', linewidth=0.8),
    capprops=dict(color='black', linewidth=0.8),
    ax=ax,
)

# Stripplot overlay: show every individual data point
sns.stripplot(
    data=df, x='group', y='value',
    color='black',
    size=4,                 # visible at 4.7 inch figure width
    alpha=0.7,
    jitter=0.15,            # slight jitter to reduce overlap
    edgecolor='white',
    linewidth=0.3,
    ax=ax,
)

# --- Axis labels (Science: 5-7 pt) ---
ax.set_xlabel('')
ax.set_ylabel('Response (a.u.)', fontsize=7)
ax.tick_params(axis='both', labelsize=6)

# Remove top and right spines for cleaner look
sns.despine(ax=ax)

# --- Step 6-7: Legend / caption info ---
# Science requires error type + n declaration in the figure caption.
# Place a small note inside the figure or rely on the figure legend text.
ax.text(
    0.98, 0.02,
    'Boxes: median + IQR\nDots: individual values (n=6/group)',
    transform=ax.transAxes,
    fontsize=5,
    ha='right', va='bottom',
    style='italic',
    color='gray',
)

plt.tight_layout()

# --- Step 7: Export ---
export_figure(
    fig,
    basename='figs/fig1_group_comparison',
    formats=['pdf', 'png'],
    size_inches=(4.7, 3.0),
    dpi=300,
    grayscale_preview=True,   # colorblind check
)

print("Exported: figs/fig1_group_comparison.pdf + .png")
print("Visual QA: run render_preview + audit_layout before submission.")
```

---

## Caption Template (for Science submission)

> **Fig. 1.** [Title describing the comparison]. Boxplots show median and
> interquartile range (IQR); individual data points are overlaid as filled
> circles (n = 6 per group). [State statistical test, e.g., "One-way ANOVA
> with Tukey's HSD post hoc correction; *p < 0.05, **p < 0.01."]

---

## Summary of Interception

| Aspect | User requested | Skill recommended | Rationale |
|---|---|---|---|
| Chart type | Mean bar + error bars | Boxplot + stripplot overlay | P1: n=6 too small for bars; bars hide distribution |
| Evidence shown | Mean + error bar only | All 6 raw points + median + IQR | Reviewer can judge data quality directly |
| Journal specs | Science | 1.5-col (4.7 in), Helvetica 6-7 pt, PDF vector | Science single-col (2.2 in) too narrow for 3 boxplots |
| Color palette | (not specified) | Okabe-Ito / seaborn colorblind | Rule 3: colorblind-safe mandatory |
| Error declaration | (not specified) | In-figure note + caption | Rule 5: SD/SEM/n/test must be declared |
| Grayscale check | (not specified) | grayscale_preview=True | Rule 3: redundant encoding for B&W printing |
