---
name: sci-draw
description: >-
  Scientific data visualization for creating publication-quality plots from experimental data. Use when the user asks to create, revise, or audit data-driven figures: statistical plots, bar/box/scatter charts, heatmaps, dose-response curves, survival curves, volcano plots, and multi-panel data layouts. Handles journal formatting, colorblind-safe palettes, and export requirements. Not for: AI-generated or text-to-image artwork (DALL-E, Stable Diffusion), conceptual diagrams or graphical abstracts without quantitative data, architecture/flowchart/network diagrams, interactive web visualizations or dashboards (Bokeh/Plotly HTML apps), or any figure not based on empirical data. Covers Chinese phrasings like 科研数据绘图、论文数据可视化、统计作图、论文图表、数据可视化.
---

# sci-draw — Scientific Figure Workflow

Publication-grade scientific figures as a visual argument, not isolated pretty plots.
Every figure starts from a conclusion, an evidence hierarchy, and a review-risk check before code or aesthetics.

## Overview

The biggest pain point isn't "I can't use matplotlib" — it's "I have data and don't know what chart best communicates my conclusion." This skill's primary ability is **thinking and judgment**, then **drawing**.

**Always think before drawing:**
1. Understand what the figure must argue — same data, different conclusions = different charts
2. Explore the data first — let facts drive chart selection
3. Actively intercept classic mistakes — don't just comply
4. Too many dimensions → suggest splitting, not cramming

**Scope**: pure data charts only — line, bar, scatter, box/violin, heatmap, error bar, distribution, correlation matrix, multi-panel composites. **Not** diagrams, flowcharts, architecture diagrams, or schematics.

## Boundaries

- **AI text-to-image art** (DALL-E, Stable Diffusion, Midjourney) → not this skill
- **Diagrams / flowcharts / schematics** → not this skill; use dedicated diagram tools
- **Prose / polishing / cover letters / submission** → not this skill; this skill only produces figures and figure reports

## Environment setup (first run only)

Before using this skill, run the environment check:

```bash
python scripts/check_env.py
```

This verifies Python >= 3.11 and all required packages. If the check fails:

1. Try a user-specified Python: `python scripts/check_env.py --python /path/to/python`
2. If no suitable Python is available, the script prints conda and uv commands to create a fresh environment. Guide the user through one of them.
3. Re-run `check_env.py` after setup to confirm.

Do not hardcode a specific environment path — use `check_env.py` each time.

## Two usage modes

**Single figure**: user gives data + asks for a figure → follow Steps 0-7 below.
**Figure set planning**: user describes a research theme or manuscript → plan a complete set of figures (Figure 1-N), each with contract, panel layout, and narrative role. See "Figure set planning" section at the end of this file.

## Working directory: `sci-skills/sci-draw/`

All figure work lives in `sci-skills/sci-draw/` under the project root. Each figure gets its own set of files — the process log, the final report, and the exported graphics:

```
sci-skills/sci-draw/
  fig1.py                 # Plotting script (written at Step 4)
  fig1-description.md     # Process log (created at Step 0, filled through Steps 1-6)
  fig1-report.md          # Final structured report (distilled at Step 7)
  fig1.pdf                # Vector export
  fig1.png                # Raster preview
  fig2.py
  fig2-description.md
  fig2-report.md
  fig2.pdf
  fig2.png
  ...
```

**File-based workflow**: the files in `sci-skills/sci-draw/` are the ground truth. When returning to a figure after a break, read the files first — they contain what was decided and why. Trust the files, not conversation memory.

_why_ **Context windows are ephemeral.** A session ends, a summary truncates, and last week's reasoning is gone. Writing decisions into files at the moment they're made preserves the *why* at the point of highest clarity. When you return, the file is a time capsule of actual reasoning, not a reconstruction from fading memory. The alternative — "I'll remember and write it up at the end" — produces reports that are clean but hollow, missing the trade-offs and dead-ends that shaped the final result.

### Startup

Before entering the workflow, check the state of `sci-skills/sci-draw/`:

1. **`sci-skills/sci-draw/` does not exist** → create it, then start from Step 0.
2. **`sci-skills/sci-draw/` exists** → ask the user: "Is there a figure in `sci-skills/sci-draw/` you want to continue working on?" If yes, read the relevant `-description.md` and `-report.md` files to understand the current state, then pick up from the appropriate step — **don't** restart from scratch. If no, start a new figure from Step 0.

_why_ **Restarting discards prior decisions.** Starting from Step 0 every time forces the user to re-explain their data and goals. Reading the files first means you already know the conclusion, the chart choice, the journal, and the statistical methods — the user picks up where they left off, not where you assume they are.

## Core workflow (8 steps)

**This is what distinguishes the skill from a plotting tool — never start by plotting.**
Each step depends on the output of the previous one.

### Step 0: Figure contract

Before generating any code, establish the contract (`references/figure-contract.md`):

1. **Core conclusion**: one-sentence conclusion the figure must prove
2. **Evidence chain**: what evidence types are needed to defend this conclusion? Each type = a candidate panel. Think in terms of the argument, not the data columns:
   - **System/overview** — what is the experimental system, cohort, or design?
   - **Main effect** — what is the primary comparison or discovery?
   - **Mechanism/localization** — how or where does the effect operate?
   - **Quantification** — how large is the effect? Representative image quantified?
   - **Robustness/controls** — does the effect hold under alternative conditions?
   - **Subgroup/sensitivity** — any nuance worth showing (optional)?
3. **Archetype**: classify as `quantitative grid`, `schematic-led composite`, `image plate + quant`, or `asymmetric mixed-modality figure`. The archetype sets the panel count expectation — see `references/figure-contract.md`.
4. **Journal/export constraints**: final dimensions, DPI, source data traceability

_why_ **Evidence chain before panels.** Starting from data columns ("I have group, treatment, value") produces 2-3 panels that mirror the input. Starting from evidence types ("I need to show the system, the main effect, and that it's robust") produces 5-7 panels that mirror the argument. Data tells you what's possible; the evidence chain tells you what's necessary.

If the user hasn't stated the conclusion, ask: "What should this figure convince the reader of?" or read from paper-plan's `conclusion` field.

**Start the process log**: create `sci-skills/sci-draw/<fig-name>-description.md` as a scratch file. Write down the contract decisions (conclusion, archetype, journal constraints). This file accumulates raw notes through Steps 1-6 — decisions, data findings, rationale, issues encountered. At Step 7, it gets distilled into a clean report at `sci-skills/sci-draw/<fig-name>-report.md`.

### Step 1: Explore data + plan panels

Understand the data first. Then build the evidence chain — panels come from the argument, not from the data columns.

1. **Profile the data** — column semantics, sample sizes, distributions, dimensionality. Run `profile_data.py` or ask the user.

2. **Build the evidence chain from the conclusion.** For each evidence type from Step 0, ask: can the data support this? What specific variable/comparison would serve as the evidence? Be exhaustive — the goal is to find all defensible evidence vectors, not the minimum.

   ```
   Evidence chain for: [core conclusion]
   - System/overview — [specific variable or view that establishes the system]
   - Main effect — [primary comparison that shows the effect]
   - Mechanism — [how/where does it work?]
   - Quantification — [how large? representative image quantified?]
   - Robustness — [alternative condition, control group, sensitivity check]
   - Subgroup/sensitivity — [optional: any nuance worth showing?]
   ```

   Each evidence type that the data can support becomes a panel. If the data can't support a type (e.g., no mechanism data), skip it — but note the gap so the user can decide.

   _why_ **Argument-first, not data-first.** Starting from data columns ("I have group, treatment, value") produces 2-3 panels that mirror the input file. Starting from the evidence chain ("I need to prove this claim, what evidence does that require?") produces 5-7 panels that mirror the argument. A reviewer evaluates the argument, not the data schema.

3. **Draft a panel plan.** Assign each evidence type to a panel. Mark the hero panel. Use the archetype from Step 0 to guide the layout. For archetype-specific panel counts, see `references/figure-contract.md`. For concrete multi-panel layout templates (clinical cascade, comparison grid, longitudinal, dose-response, genomics, multi-group) with exact panel arrangements, see `references/nature-observations.md`.

   **Stop. Ask the human:** "Here's the evidence chain and proposed panel layout. Any evidence missing that you'd want a reviewer to see?" The question frames toward completeness — the default answer should be "looks good," not "remove panel c."

   _why_ **Ask about gaps, not excess.** Asking "Too many?" signals that panels are costly and should be pruned. Asking "Any missing evidence?" signals that completeness is the goal. The human can still say "drop panel d, it's a distraction" — but they won't prune by default.

### Step 2: Select chart

**This is the advisor's core responsibility.** Reason from Steps 0-1: data characteristics + conclusion determine the chart, not user preference or habit.

**Decision = data shape + conclusion + sample size:**

| Data shape | Default | Small-n rule |
|---|---|---|
| 1 continuous, distribution | Histogram + KDE | n<5: list points directly |
| 1 cat + 1 cont, comparison | Box/violin + stripplot | n<10: stripplot only, no bars |
| 2 continuous, relationship | Scatter + regression + r | — |
| Time/dose vs continuous | Line + error band | 2 timepoints only → paired dot plot |
| Multi-variable (>3 cols) | Correlation heatmap / pairplot | — |
| Matrix data | Heatmap (viridis/RdBu_r) | — |

**Same data, different conclusions = different charts.** Example: 30 subjects × 2 drugs × 5 timepoints. "Drug A is faster than B overall" → boxplot pooling all timepoints. "A and B diverge most at t=3" → line chart with error bands over time. "Subject variability is large" → spaghetti plot with individual lines. The data is identical; the chart changes because the argument changes.

**Complexity → compose, don't split:**
- Grouping combinations > 12 → use multiple panels, each showing a coherent subset
- x-axis labels > 8 → use faceted multi-panel layout instead of angled labels
- Legend items > 6 → use direct labels or one shared legend strip across panels
- y-axis spans multiple orders of magnitude → use separate panels with different scales
- The figure wants to make two independent conclusions → **two figures** (this is the only true split case)

_why_ **Complexity is why multi-panel figures exist.** A 6-panel figure that exhaustively proves one conclusion is stronger than two 3-panel figures that each feel incomplete. The point of panels is to digest complexity within one argument, not to avoid it. Split only when the conclusions diverge — not when the data is rich.

**Give**: recommendation + brief reason + 1-2 alternatives. If the user's choice doesn't fit the data (e.g., n=5 mean bar), explain why and offer the better option (see "Active interception" below). For deeper examples and edge cases, see `references/chart_selection.md`.

**Record**: chosen chart type, rationale (why this, not alternatives), and any interception warnings you gave to the user.

### Step 3: Apply journal style

If no target journal was specified in Step 0, ask now: "Thesis / Chinese core / English SCI / NeurIPS" all have different specs. See `references/journal_specs.md` for detailed dimensions and requirements per journal.

```python
from scripts.setup_style import setup_style
setup_style(journal='nature', lang='en')             # English Nature
setup_style(journal='general', lang='zh', serif_for_zh=True)  # Chinese serif mixed
```

Applies figsize, font sizes, DPI, font family, spine visibility, and CJK font detection in one call.

_why_ **Matplotlib renders text in absolute points.** If you plot at default size then resize the figure, all font sizes shift unpredictably. Setting journal style first guarantees every label is at the correct size from the first `ax.text()`. CJK font detection must also happen before any text is drawn — fixing square boxes after rendering means redoing everything.

**Record**: journal, language, CJK settings (serif/sans).

### Step 4: Plot

Write the plotting script and save it as `sci-skills/sci-draw/<fig-name>.py`. This is the reproducible source — anyone (including your future self) should be able to run it and regenerate the figure.

Follow `references/plot_recipes.md` for chart-specific recipes. For design rationale (color semantics, typography, multi-panel architecture) see `references/design-theory.md`. For palette constants and helper signatures see `references/api.md`. For specialized chart types see `references/chart-types.md`. For real journal page layout patterns see `references/nature-observations.md`. Additional patterns in `references/common-patterns.md` and `references/tutorials.md`.

Mandatory while plotting:
- `figsize=(target_width, target_height)` in inches — set final size directly
- Use `seaborn.color_palette('colorblind')` or Okabe-Ito + redundant encoding (different line styles / markers)
- Error bars / shadows must declare SD / SEM / 95% CI + n in legend

_why_ **Three rejection causes, three hard rules.** (1) Scaling a figure in Word after export shrinks 9pt fonts to 4.5pt — the #1 journal desk-rejection cause. (2) Red-green-only encoding has zero meaning for ~8% of male readers; redundant encoding (color + marker + line style) costs one line of code and loses no one. (3) SD and SEM differ by √n — omitting the error bar type in the legend invites the reviewer to assume the wrong one, which can reverse a conclusion.

**Record**: statistical test used, correction method, error bar type (SD/SEM/CI), n, significance annotations (*, **, *** definitions).

### Step 5: Export

```python
from scripts.export_figure import export_figure
export_figure(
    fig, basename='sci-skills/sci-draw/fig1',
    formats=['pdf', 'png'],
    size_inches=(3.5, 2.625),
    dpi=300,
    grayscale_preview=True,    # auto grayscale for colorblind check
)
```

Then run `scripts/check_figure.py --strict` for machine audit.

_why_ **Vector text stays sharp; raster doesn't.** Journal PDF checkers reject figures with rasterized text — PDF keeps fonts as text at any zoom, while PNG text at 300 DPI is fuzzy. The grayscale preview is a one-click colorblind audit: if categories blend together in gray, they'll blend for colorblind readers too. Catch it here, not in peer review.

**Record**: output file paths, formats, final dimensions, DPI.

### Step 6: Visually review

Open the exported PNG and PDF. Go through the checklist in `references/visual_review.md`
item by item — don't skim. The checklist covers glyphs, font sizes, clipping, panel
alignment, colors, data integrity, cross-panel consistency, and argument clarity.

**Loop discipline:**
- Fix issues one at a time, re-export, re-check. Max 3 review rounds.
- If it still doesn't pass after 3 rounds, the problem is likely upstream: wrong chart type (revisit Step 2) or too many dimensions (split the figure).

_why_ **Perceptual judgment needs human eyes.** No script can judge whether a figure communicates its argument or "looks right." Font readability at print scale, color harmony, and argument clarity are perceptual — only a person can verify them. The
next check after this is peer review — catch what you can before that.

**Record** in description log: each round's findings, what was fixed in code, and what was deferred to manual touch-up.

### Step 7: Finalize report

The process log `sci-skills/sci-draw/<fig-name>-description.md` now contains raw notes accumulated through Steps 0-7: decisions, data findings, rationale, issues. Review it and **distill into a clean report** at `sci-skills/sci-draw/<fig-name>-report.md`.

The report is NOT the figure legend — it's a machine-readable record for downstream workflows (manuscript writing, revision, cross-referencing). The description log remains as the raw audit trail; don't delete it.

Before considering the figure done, run through the compliance checklist in `references/publication_checklist.md` — dimensions, DPI, font embedding, colorblind safety, error-bar declaration, and data provenance.

_why_ **Two files, two audiences.** The log is chronological and messy — decisions are scattered across seven steps of notes, useful for the maker who needs to retrace reasoning. The report is structured for downstream consumers: writing the manuscript legend, answering reviewer questions ("what was n again?"), checking cross-figure consistency, and giving future you a fast entry point. Log = maker, report = reader.

```markdown
# Figure 1 — [short title]

## Core conclusion
[One-sentence conclusion this figure proves]

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

## Chart quick-reference

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

See Step 2 for the full decision framework, "same data different conclusion" examples, and split criteria.

## Five hard rules

### Rule 1: Plot at final size, never rescale

`figsize` must be the actual paper size (Nature single-col 3.5 in, double-col 7.2 in; IEEE single-col 3.5 in, double-col 7.16 in). **Never** rescale in Word/LaTeX after export.

_why_ **Matplotlib font sizes are in absolute points.** Rescale 50% in Word → 9pt becomes 4.5pt — submission check rejects immediately.

### Rule 2: Vector first (PDF)

Line / bar / scatter / heatmap (data grid) / error bar → PDF. Only micrographs and photos use PNG (300-600 DPI). **Never use JPEG**.

_why_ **JPEG compression creates artifacts on data figures.** Journal PDF checkers reject them. Vector PDF for data charts; PNG only for micrographs and photos.

### Rule 3: Colorblind-safe palette

Default to `seaborn.color_palette('colorblind')` or Okabe-Ito. **Same figure, different categories must use redundant encoding** (line style / marker). Before export, `export_figure(..., grayscale_preview=True)` to verify grayscale distinguishability.

_why_ **~8% of men, ~0.5% of women have color vision deficiency.** Reviewers include these people. Red-green-only encoding has zero communication power for them.

### Rule 4: Font size readable at final size

Body labels and tick numbers 7-9 pt, minimum font **>= 6 pt**.

_why_ **Review editors print at mm scale and check font size.** < 6 pt is unreadable in print — the submission check catches this immediately.

### Rule 5: Error declaration mandatory

Any error bar / shadow interval / boxplot — **legend must state**:
- Error type (SD / SEM / 95% CI / IQR)
- Sample size n
- Significance test + correction (e.g., Bonferroni)
- Symbol definition (`* p<0.05` etc.)

_why_ **SD and SEM differ by √n.** Confusing them can reverse a conclusion. Declaring the error type in the legend removes the ambiguity.

## Active interception (advisor responsibility)

When the user's request triggers these errors, **explain first, offer alternatives, don't silently comply**. Full 18 items in `references/viz_pitfalls.md`.

| Error | Consequence | Alternative |
|---|---|---|
| Mean bar with n<10/group | Hides distribution, hides n, reviewer suspicion | Box + stripplot; or stripplot only |
| Dual Y-axis for unrelated variables | Visual correlation/divergence is fabricated | Split into stacked subplots sharing x |
| Pie chart for proportions | 3x worse angle/length judgment | Horizontal bar (sorted by value) |
| Rainbow / jet colormap | Perceptually non-uniform, fabricates peaks | viridis / magma / RdBu_r |

**Interception dialogue example**:

> The "mean bar chart with 3 groups of 5 samples" you requested triggers P1 (mean bar hides distribution): n=5 is too small, bars make reviewers suspect you're hiding something. I suggest **box + stripplot overlay** — all 5 points visible, distribution clear at a glance. Only one extra line of code. Want to proceed with original plan?

Respect the user's final decision, but **leave a clear record of the warning**.

## CJK support

The root cause of Chinese square boxes in matplotlib: default fonts (DejaVu Sans etc.) don't contain CJK glyphs. `setup_style(lang='zh')` automatically:

1. Searches for CJK fonts by priority: `Noto Sans CJK SC` > `Source Han Sans SC` > `SimHei` > `Microsoft YaHei`
2. Fixes minus sign rendering: `plt.rcParams['axes.unicode_minus'] = False`

If no CJK font found, raises a clear install message (not silent square boxes).

**Chinese journal "Song + Times New Roman mixed"**: pass `serif_for_zh=True` to use Noto Serif CJK / Source Han Serif / SimSun.

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

## Common task examples

See `references/task-examples.md` for worked examples of the four most common scenarios: CSV-to-figure, active interception, multi-panel composite, and statistical annotations.

## Privacy rule

Do not disclose private local paths, private filenames, attachment names, internal reference filenames, template identifiers, or provenance of private working materials in user-facing replies, generated code comments, figure legends, reports, or manuscript text. Use generic descriptions like "the provided data file" or "the internal figure contract". Only reveal exact paths when user explicitly asks for audit trail.

## Figure set planning

When the user describes a research theme, manuscript, or dataset and asks to "plan the figures" or "design Figure 1-4", use this process instead of jumping to individual figure creation.

### Input

User provides:
- Research question or manuscript title
- Key findings / conclusions (or data to derive them from)
- Target journal (optional but helpful)

### Output

A figure plan document with one entry per figure:

```
## Figure Plan — [manuscript title]

### Figure 1: [short title]
- **Core conclusion**: [one-sentence conclusion]
- **Archetype**: [quantitative grid / schematic-led / image plate / asymmetric]
- **Evidence chain**:
  - System/overview → panel a
  - Main effect → panel b
  - Mechanism → panel c
  - Quantification → panel d
  - Robustness → panel e
- **Panels**:
  - a: [content] — evidence role: [hero / validation / control]
  - b: [content] — evidence role: [...]
  - c: [content] — evidence role: [...]
  - d: [content] — evidence role: [...]
  - e: [content] — evidence role: [...]
- **Data source**: [file/description]
- **Statistics**: [test, n, error type]
- **Journal spec**: [size, format]

### Figure 2: [short title]
- ...
```

### Planning rules (from figure-contract.md)

1. **One figure, one conclusion**. If a panel doesn't defend the conclusion, drop it.
2. **Panel ordering**: system → main effect → mechanism → quant → robustness.
3. **Visual vocabulary**: Figure 1 establishes colors, symbols, scale. Reuse throughout.
4. **Evidence hierarchy**: hero panel gets the most space; controls are visually quieter.
5. **Reviewer risk**: what would a skeptic challenge? Address it in the plan.
6. **Shared elements**: note which figures share legends, color mappings, or data sources.

### After plan approval

For each figure in the plan, execute the full 8-step workflow (contract → explore → select → style → plot → export → review → finalize). Maintain cross-figure consistency: same variable = same color, same error convention, same font size.

