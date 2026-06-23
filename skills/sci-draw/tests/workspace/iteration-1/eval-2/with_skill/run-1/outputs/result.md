# Eval-2 Result: Mean Bar Chart with n=6 (P1 Interception)

## 1. Would the skill intercept this request?

**Yes.** The request triggers **P1: mean bar chart hides distribution and sample size** (see `references/viz_pitfalls.md`).

With n=6 per group, the skill's chart selection table (`references/chart_selection.md`, "Decision Axis 3: Data Scale") states:

- n < 10 per group --> **strongly recommend stripplot / dot plot directly; do not draw statistical bars**
- Mean bar chart is listed as **forbidden** for 1 categorical + 1 continuous with n < 10

The quick-reference in SKILL.md line 176 confirms: "1 cat + 1 cont, n<10/group --> Stripplot / dot plot (show all points) --> Mean bar (forbidden)".

## 2. What alternative would the skill suggest?

**Primary recommendation: boxplot + stripplot overlay.**

Rationale (from viz_pitfalls.md P1):
- n=6 is too small for bar height + error bars to communicate the true data distribution
- A reviewer would likely request "show individual data points"
- Boxplot + stripplot shows all 6 points directly, hiding nothing, and is actually more convincing
- Code is only one extra line compared to a bar chart

**Alternative: stripplot / dot plot only** (since n < 10, even boxplot quartile estimates are less reliable).

## 3. Interception dialogue

The skill would produce dialogue following the pattern in SKILL.md lines 325-335:

> The "mean bar chart with 3 groups of 6 samples" you requested triggers the classic P1 error (see viz_pitfalls.md) -- n=6 is too small, bar height + one error bar cannot tell the reader the true data distribution. A reviewer at Science would likely request "show individual data points."
>
> I suggest **boxplot + stripplot overlay** -- all 6 points per group directly visible, distribution clear at a glance, hiding nothing. Only one extra line of code.
>
> Proceed with original plan, or switch to box+stripplot?

## 4. If user insists on bars -- minimum requirement

Per SKILL.md line 337: "If user insists on bars --> at minimum force stripplot overlay showing each point."

The minimum enforcement:
- Bar chart is allowed **only if** a stripplot overlay shows every individual data point on top of each bar
- Error bars must explicitly declare SD or SEM + n in the legend
- Legend must state: error type, sample size n, and significance test if applicable

## 5. Complete Python script (intercepted solution: boxplot + stripplot)

```python
"""
sci-draw intercepted solution: boxplot + stripplot overlay
Original request: mean bar chart, 3 groups, n=6 each
Interception: P1 -- n<10 mean bar is forbidden; switched to box+stripplot
Target journal: Science (single-col 2.2 in, 1.5-col 4.7 in)
Export: PDF (vector) + PNG (300 DPI)
"""

import sys, os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- Setup style (Science journal preset) ---
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))
from setup_style import setup_style
from export_figure import export_figure

setup_style(journal='science', lang='en')

# --- Colorblind-safe palette ---
PAL = sns.color_palette('colorblind')

# --- Simulate example data: 3 groups, n=6 each ---
rng = np.random.default_rng(42)
groups = ['Control', 'Treatment A', 'Treatment B']
data = pd.DataFrame({
    'group': np.repeat(groups, 6),
    'value': np.concatenate([
        rng.normal(10.0, 1.5, 6),   # Control
        rng.normal(13.5, 2.0, 6),   # Treatment A
        rng.normal(11.8, 1.2, 6),   # Treatment B
    ])
})

# --- Figure contract ---
# Core conclusion: Treatment A increases the measured response vs Control.
# Evidence: direct comparison of individual measurements across 3 groups.
# Chart: boxplot (quartile summary) + stripplot (show all n=6 points per group).

# --- Plot: boxplot + stripplot overlay ---
fig, ax = plt.subplots(figsize=(4.7, 3.5))  # Science 1.5-col width

sns.boxplot(
    data=data, x='group', y='value',
    palette=PAL[:3],
    showfliers=False,       # stripplot shows all points instead
    width=0.5,
    linewidth=0.8,
    ax=ax,
)
sns.stripplot(
    data=data, x='group', y='value',
    color='black',
    size=4,
    alpha=0.7,
    jitter=0.15,
    edgecolor='white',
    linewidth=0.3,
    ax=ax,
)

# --- Axis labels and formatting ---
ax.set_xlabel('')
ax.set_ylabel('Response (a.u.)', fontsize=7)
ax.tick_params(axis='both', labelsize=7)

# --- Legend annotation: error type + n ---
# Boxplot shows IQR (25th-75th percentile) and median line.
# Add a text annotation declaring sample size.
ax.text(
    0.98, 0.02,
    'Box: IQR + median; n = 6 per group',
    transform=ax.transAxes,
    fontsize=6,
    ha='right', va='bottom',
    style='italic',
    color='grey',
)

# --- Tight layout ---
fig.tight_layout()

# --- Export: PDF (vector) + PNG (raster, 300 DPI) ---
os.makedirs('figs', exist_ok=True)
export_figure(
    fig,
    basename='figs/fig1_groups_comparison',
    formats=['pdf', 'png'],
    size_inches=(4.7, 3.5),
    dpi=300,
    grayscale_preview=True,   # colorblind check
)

print('Exported: figs/fig1_groups_comparison.pdf + .png')
```

## 6. Export format

Per the sci-draw workflow (SKILL.md Step 7, Rule 2):
- **PDF** (vector) -- primary format for line/bar/scatter/box figures; journals prefer vector for crisp rendering at any zoom
- **PNG** (raster, 300 DPI) -- fallback for submission systems that require raster; Science requires >= 300 DPI

The `export_figure` call uses `formats=['pdf', 'png']` and `grayscale_preview=True` to auto-generate a grayscale version for colorblind verification (Rule 3).
