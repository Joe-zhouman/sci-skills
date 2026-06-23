---
name: sci-draw
description: >-
  Scientific data visualization for creating publication-quality plots from
  experimental data. Use when the user asks to create, revise, or audit
  data-driven figures: statistical plots, bar/box/scatter charts, heatmaps,
  dose-response curves, survival curves, volcano plots, and multi-panel data
  layouts. Handles journal formatting, colorblind-safe palettes, and export
  requirements. Not for: AI-generated or text-to-image artwork (DALL-E, Stable
  Diffusion), conceptual diagrams or graphical abstracts without quantitative
  data, architecture/flowchart/network diagrams, interactive web visualizations
  or dashboards (Bokeh/Plotly HTML apps), or any figure not based on empirical
  data. Covers Chinese phrasings like 科研数据绘图、论文数据可视化、
  统计作图、论文图表、数据可视化.
---

# sci-draw — Scientific Figure Workflow

Publication-grade scientific figures as a visual argument, not isolated pretty plots.
Every figure starts from a claim, an evidence hierarchy, and a review-risk check
before code or aesthetics.

## Overview

The biggest pain point isn't "I can't use matplotlib" — it's "I have data and don't
know what chart best communicates my conclusion." This skill's primary ability is
**thinking and judgment**, then **drawing**.

**Always think before drawing:**
1. Understand what the figure must argue — same data, different claims = different charts
2. Profile the data first — let facts drive chart selection
3. Actively intercept classic mistakes — don't just comply
4. Too many dimensions → suggest splitting, not cramming

**Scope**: pure data charts only — line, bar, scatter, box/violin, heatmap, error bar,
distribution, correlation matrix, multi-panel composites. **Not** diagrams, flowcharts,
architecture diagrams, or schematics.

## When to use

- User gives CSV/Excel/DataFrame and says "plot this" or "what chart should I use"
- User is writing a paper and needs data figures
- User has a draft figure that "doesn't look publication-ready"
- User mentions Nature/Science/IEEE or any journal
- User asks about error bars, significance, colorblind safety, vector export, multi-panel
- User asks "how to fix Chinese matplotlib square boxes"

## When NOT to use

- AI text-to-image generation (DALL-E, Stable Diffusion, Midjourney, etc.)
- Mechanism diagrams, workflow/flowcharts, architecture diagrams, schematics
- Conceptual illustrations or graphical abstracts without data axes
- Plotly/Altair/Bokeh interactive or web-first charts (unless Plotly recipe requested)
- EDA-only plots without a publication target
- 3D, GIS, or non-scientific illustration
- Illustrator/Figma-first layout

## Environment setup (first run only)

Before using this skill, verify Python environment has the required packages:

```bash
python3 -c "import matplotlib, seaborn, numpy, pandas, scipy; from PIL import Image; print('OK')"
```

If this fails, the user needs to set up a Python environment with the dependencies
listed at the bottom of this file. Guide them — do not hardcode a specific environment
path in scripts or instructions.

## Two usage modes

**Single figure**: user gives data + asks for a figure → follow Steps 0-7 below.
**Figure set planning**: user describes a research theme or manuscript → plan a complete
set of figures (Figure 1-N), each with contract, panel layout, and narrative role.
See "Figure set planning" section at the end of this file.

## Core workflow (9 steps)

**This is what distinguishes the skill from a plotting tool — never start by plotting.**
Each step depends on the output of the previous one.

### Step 0: Figure contract

Before generating any code, establish the contract (`references/figure-contract.md`):

1. **Core conclusion**: one-sentence claim the figure must defend
2. **Evidence chain**: map each planned panel to the claim; drop panels that don't carry
   a unique piece of evidence
3. **Archetype**: classify as `quantitative grid`, `schematic-led composite`,
   `image plate + quant`, or `asymmetric mixed-modality figure`
4. **Journal/export constraints**: final dimensions, DPI, source data traceability

The highest-priority rule: **the chart serves the scientific logic**. Aesthetic polish,
template matching, and complex layout are subordinate to making the core conclusion clear.

If the user hasn't stated the claim, ask: "What should this figure convince the reader
of?" or infer from manuscript context and state your assumption.

### Step 1: Profile data

Run `scripts/profile_data.py`:

```bash
python scripts/profile_data.py data.csv --group group --group condition
```

Output: column types, sample sizes, missing rates, distributions, outliers, correlations,
preliminary chart suggestions. See `references/data_profiling.md` for interpretation.

**Key checks:**
- Column type detection correct? (numeric ID misclassified as ordinal is common)
- Per-group n? Small-sample warning?
- Highly skewed? Need log axis?

### Step 2: Select chart

**This is the advisor's core responsibility.** Based on Steps 0-1, consult
`references/chart_selection.md` for the decision framework.

- Give recommendation + brief reason + 1-2 alternatives
- If grouping combinations > 12 → **suggest splitting**, not cramming
- If user's choice doesn't fit data (e.g., n=5 mean bar) → **gently explain and offer
  better option** (see "Active interception" below)
- If data has special characteristics (bimodal, severe outliers,跨量级) → mention in
  the recommendation

### Step 3: Check journal specs

Once target journal is known, consult `references/journal_specs.md` for:
single/double column width (mm and inches), font size, recommended font, DPI,
vector format preference.

If no target journal specified, ask. "Thesis / Chinese core / English SCI / NeurIPS"
all have different specs.

### Step 4: Configure style

```python
from scripts.setup_style import setup_style
setup_style(journal='nature', lang='en')             # English Nature
setup_style(journal='general', lang='zh', serif_for_zh=True)  # Chinese serif mixed
```

SciencePlots is used automatically if installed; falls back gracefully if not.

### Step 5: Plot

Follow `references/plot_recipes.md` for chart-specific recipes. Additional patterns
in `references/common-patterns.md` and `references/tutorials.md`.

Mandatory while plotting:
- `figsize=(target_width, target_height)` in inches — set final size directly
- Use `seaborn.color_palette('colorblind')` or Okabe-Ito + redundant encoding
  (different line styles / markers)
- Error bars / shadows must declare SD / SEM / 95% CI + n in legend

### Step 6: Pre-export check

Run `visual_qa.audit_layout(fig)` to catch missing glyphs, text clipping, and tick
overlap. Fix any WARN/FAIL before export. This is a one-shot check — if issues
remain, export anyway and let the user review the output.

Subsequent fine-tuning happens outside this workflow (user-driven iteration).

### Step 7: Export

```python
from scripts.export_figure import export_figure
export_figure(
    fig, basename='figs/fig1',
    formats=['pdf', 'png'],
    size_inches=(3.5, 2.625),
    dpi=300,
    grayscale_preview=True,    # auto grayscale for colorblind check
)
```

Then run `scripts/check_figure.py --strict` for machine audit.

### Step 8: Write figure description

After export, generate a structured description file alongside the figure:
`figs/fig1_description.md`. This is NOT the figure legend — it's a machine-readable
summary for downstream workflows (manuscript writing, revision, cross-referencing).

```markdown
# Figure 1 — [short title]

## Core conclusion
[One-sentence claim this figure defends]

## Data source
- File: [path or description]
- Samples: [n per group, total N]
- Variables: [list]

## Chart type & rationale
- Type: [grouped bar / scatter / boxplot / etc.]
- Why: [brief reason based on data shape and argument]

## Statistical methods
- Test: [t-test / ANOVA / Mann-Whitney / etc.]
- Correction: [Bonferroni / FDR / none]
- Error bars: [SD / SEM / 95% CI / IQR], n=[X]
- Significance: [* p<0.05, ** p<0.01]

## Key findings
- [Finding 1]
- [Finding 2]

## Journal specs
- Target: [Nature / Science / IEEE / etc.]
- Size: [single-col 3.5in / double-col 7.2in]
- Format: PDF + PNG
```

This file serves multiple purposes:
- Writing the manuscript figure legend (expand the core conclusion + findings)
- Revision rounds (reviewer asks "what was n?" → check description)
- Cross-figure consistency (ensure all figures use the same statistical conventions)
- Automated manuscript generation workflows

## Chart quick-reference (detailed decisions in chart_selection.md)

| Data shape | Recommended | **Don't use** |
|---|---|---|
| 1 continuous, view distribution | Histogram + KDE / boxplot | Pie chart |
| 1 categorical, view proportions | Horizontal bar (sorted by value) | Pie chart, 3D pie |
| 1 cat + 1 cont, n<10/group | **Stripplot / dot plot** (show all points) | Mean bar (**forbidden**) |
| 1 cat + 1 cont, n≥10/group | **Box/violin + stripplot overlay** | Mean bar only |
| 2 continuous, view relationship | Scatter + regression + r value | Line (unless x is ordered continuous) |
| Time/dose vs continuous | Line + error band | Bar |
| Multi-variable correlation (>3 cols) | Correlation heatmap / pairplot | Parallel coordinates |
| Matrix data | Heatmap (viridis/RdBu_r) | 3D surface, rainbow colormap |
| Composition/stacking | Stacked bar / treemap | **Pie chart** |

Full decision tree and "same data different claim" examples in `chart_selection.md`.

## Five hard rules

### Rule 1: Plot at final size, never rescale

`figsize` must be the actual paper size (Nature single-col 3.5 in, double-col 7.2 in;
IEEE single-col 3.5 in, double-col 7.16 in). **Never** rescale in Word/LaTeX after export.

**Why**: matplotlib font size is in absolute units (pt). Rescale 50% in Word → 9pt
becomes 4.5pt — submission check rejects immediately.

### Rule 2: Vector first (PDF)

Line / bar / scatter / heatmap (data grid) / error bar → PDF. Only micrographs and
photos use PNG (300-600 DPI). **Never use JPEG**.

**Why**: JPEG compression artifacts on data figures; journal PDF checker rejects.

### Rule 3: Colorblind-safe palette

Default to `seaborn.color_palette('colorblind')` or Okabe-Ito. **Same figure, different
categories must use redundant encoding** (line style / marker). Before export,
`export_figure(..., grayscale_preview=True)` to verify grayscale distinguishability.

**Why**: ~8% of men, ~0.5% of women have color vision deficiency. Reviewers include
these people. Red-green-only encoding has zero communication power for them.

### Rule 4: Font size readable at final size

Body labels and tick numbers 7-9 pt, minimum font **>= 6 pt**.

**Why**: Review editors print at mm scale and check font size; < 6 pt is unreadable.

### Rule 5: Error declaration mandatory

Any error bar / shadow interval / boxplot — **legend must state**:
- Error type (SD / SEM / 95% CI / IQR)
- Sample size n
- Significance test + correction (e.g., Bonferroni)
- Symbol definition (`* p<0.05` etc.)

**Why**: SD and SEM differ by sqrt(n). Confusion = reversed conclusion = rejection.

## Active interception (advisor responsibility)

When the user's request triggers these errors, **explain first, offer alternatives,
don't silently comply**. Full 18 items in `references/viz_pitfalls.md`.

| Error | Consequence | Alternative |
|---|---|---|
| Mean bar with n<10/group | Hides distribution, hides n, reviewer suspicion | Box + stripplot; or stripplot only |
| Dual Y-axis for unrelated variables | Visual correlation/divergence is fabricated | Split into stacked subplots sharing x |
| Pie chart for proportions | 3x worse angle/length judgment | Horizontal bar (sorted by value) |
| Rainbow / jet colormap | Perceptually non-uniform, fabricates peaks | viridis / magma / RdBu_r |

**Interception dialogue example**:

> The "mean bar chart with 3 groups of 5 samples" you requested triggers P1 (mean bar
> hides distribution): n=5 is too small, bars make reviewers suspect you're hiding
> something. I suggest **box + stripplot overlay** — all 5 points visible, distribution
> clear at a glance. Only one extra line of code. Want to proceed with original plan?

Respect the user's final decision, but **leave a clear record of the warning**.

## CJK support

The root cause of Chinese square boxes in matplotlib: default fonts (DejaVu Sans etc.)
don't contain CJK glyphs. `setup_style(lang='zh')` automatically:

1. Searches for CJK fonts by priority: `Noto Sans CJK SC` > `Source Han Sans SC` >
   `SimHei` > `Microsoft YaHei`
2. Fixes minus sign rendering: `plt.rcParams['axes.unicode_minus'] = False`

If no CJK font found, raises a clear install message (not silent square boxes).

**Chinese journal "Song + Times New Roman mixed"**: pass `serif_for_zh=True` to
use Noto Serif CJK / Source Han Serif / SimSun.

See `references/journal_specs.md` end section for font installation.

## Script reference

| Script | Purpose | Main entry |
|---|---|---|
| `profile_data.py` | EDA: column types / samples / distribution / outliers / correlations / chart suggestions | `profile_data(source, group_cols)` |
| `setup_style.py` | Journal preset + CJK font config + SciencePlots wrapper | `setup_style(journal, lang, use_sciplots, serif_for_zh)` |
| `export_figure.py` | PDF + PNG at exact final size + grayscale preview | `export_figure(fig, basename, formats, dpi, size_inches, grayscale_preview)` |
| `check_figure.py` | File compliance audit (format / DPI / font embedding) | `check_figure(path, min_dpi, target_inches)` |
| `layout_tools.py` | Panel label alignment + constrained/tight layout fallback | `add_panel_labels(fig, style)` / `finalize_figure(fig)` |
| `visual_qa.py` | PNG preview + programmatic check (missing glyphs / clipping / tick overlap) | `render_preview(fig, out)` / `audit_layout(fig)` |

## Reference files

`references/` — **load on demand, don't read all at once**. Each has a TOC at the top.

**Core workflow**: `figure-contract.md` · `chart_selection.md` · `data_profiling.md` · `plot_recipes.md` · `journal_specs.md`
**QA**: `viz_pitfalls.md` (18 pitfalls) · `publication_checklist.md` · `visual_review.md`
**Design**: `design-theory.md` · `common-patterns.md` (16 patterns) · `nature-2026-observations.md`
**Reference**: `api.md` (palettes + helpers) · `tutorials.md` · `chart-types.md` · `demos.md`

## Common task examples

### Task A: User gives CSV and says "help me plot this for my paper"

**Think-first workflow example:**

1. **Step 0**: Ask "What should this figure convince the reader of?" — group differences?
   time trends? variable relationships?
2. **Step 1**: Run `python scripts/profile_data.py data.csv` for profiling report
3. **Step 2**: Read report's "column types + sample sizes + grouping structure", consult
   `chart_selection.md`. **Proactively give recommendation + reason + 1-2 alternatives**
4. **After user confirms** → Steps 3-7: journal specs, style, plot, QA, export

Don't skip any step.

### Task B: User wants "mean bar chart with 3 groups of 5 samples"

**Active interception example:**

```
The "3 groups of 5 samples mean bar chart" you requested triggers the classic P1 error
(see viz_pitfalls.md) — n=5 is too small, bar height + one error bar can't tell the
reader the true data distribution. A reviewer would likely request "show individual
data points".

I suggest **boxplot + stripplot overlay** — 5 points directly visible, hiding nothing,
actually more convincing. Code is only one extra line.

Proceed with original plan, or switch to box+stripplot?
```

If user insists on bars → at minimum force stripplot overlay showing each point.

### Task C: Multi-panel composite figure

User: "Give me Figure 1: 4 panels — PCA, loss curve, confusion matrix, survival curve."

Flow:
1. Confirm target journal (determines 7.2 in or 7.16 in; Nature `a/b/c` vs IEEE `(a)(b)(c)`)
2. Plot each panel independently, **ensure font size, color palette, axis scales are
   unified** (same variable = same color across all 4 panels)
3. Combine with `plt.subplots(2, 2, figsize=(7.2, 5.4))`
4. `layout_tools.finalize_figure(fig)` then `add_panel_labels(fig, style='nature')` —
   **unified figure-coordinate alignment**, don't hand-place `ax.text` (prone to
   misalignment, see viz_pitfalls P18)
5. **Pre-export check**: `audit_layout(fig)` to catch clipping/overlap → export

Recipe in `plot_recipes.md` section 9.

### Task D: Statistical figure with significance annotations

User: "3 groups, boxplot with significance bars."

Flow:
1. Profile to confirm n (n<10 → must overlay stripplot)
2. Run statistical test (**user must state** which test, whether multiple comparison
   correction applied)
3. Plot box + stripplot
4. Use `matplotlib.lines.Line2D` or `statannotations` for significance bridges
5. **Legend must state**: error type / n / test method / correction / symbol definition

Recipe in `plot_recipes.md` section 4.

## Privacy rule

Do not disclose private local paths, private filenames, attachment names, internal
reference filenames, template identifiers, or provenance of private working materials
in user-facing replies, generated code comments, figure legends, reports, or manuscript
text. Use generic descriptions like "the provided data file" or "the internal figure
contract". Only reveal exact paths when user explicitly asks for audit trail.

## Figure set planning

When the user describes a research theme, manuscript, or dataset and asks to "plan
the figures" or "design Figure 1-4", use this process instead of jumping to individual
figure creation.

### Input

User provides:
- Research question or manuscript title
- Key findings / claims (or data to derive them from)
- Target journal (optional but helpful)

### Output

A figure plan document with one entry per figure:

```
## Figure Plan — [manuscript title]

### Figure 1: [short title]
- **Core conclusion**: [one-sentence claim]
- **Archetype**: [quantitative grid / schematic-led / image plate / asymmetric]
- **Panels**:
  - a: [content] — evidence role: [hero / validation / control]
  - b: [content] — evidence role: [...]
  - c: [content] — evidence role: [...]
- **Data source**: [file/description]
- **Statistics**: [test, n, error type]
- **Journal spec**: [size, format]

### Figure 2: [short title]
- ...
```

### Planning rules (from figure-contract.md)

1. **One figure, one claim**. If a panel doesn't defend the claim, drop it.
2. **Panel ordering**: system → main effect → mechanism → quant → robustness.
3. **Visual vocabulary**: Figure 1 establishes colors, symbols, scale. Reuse throughout.
4. **Evidence hierarchy**: hero panel gets the most space; controls are visually quieter.
5. **Reviewer risk**: what would a skeptic challenge? Address it in the plan.
6. **Shared elements**: note which figures share legends, color mappings, or data sources.

### After plan approval

For each figure in the plan, execute the full 8-step workflow (contract → profile →
select → style → plot → QA → export → description). Maintain cross-figure consistency:
same variable = same color, same error convention, same font size.

## Dependencies

```
matplotlib>=3.7
seaborn>=0.13
Pillow>=10.0
numpy>=1.24
pandas>=2.0
scipy>=1.10
```

Optional (skill degrades gracefully if missing):
```
SciencePlots>=2.1
pypdf>=4.0
PyMuPDF>=1.23
```
