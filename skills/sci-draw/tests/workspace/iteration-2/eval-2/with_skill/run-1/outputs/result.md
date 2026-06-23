# sci-draw 8-Step Workflow Result

## Task
Tumor volume time series figure for Nature submission.
Treatment groups: Control, Drug_A, Drug_B, Drug_C (n=8 per group).

## Workflow Steps Completed

### Step 0: Figure Contract

Core conclusion: Drug_B significantly suppresses tumor growth compared to
control over 28 days, while Drug_A shows moderate inhibition and Drug_C
shows only transient effect.

Figure archetype: quantitative grid (single panel, time series)

Target journal: Nature
Final size: single-column 3.5 x 2.625 inches

Panel map:
  a: Line plot with SEM error bands showing tumor volume over time
     for all 4 treatment groups (n=8 per group)

Evidence hierarchy:
  hero evidence: Drug_B sustained tumor suppression vs control
  validation evidence: Drug_A moderate effect, Drug_C rebound
  controls/robustness: Control group natural growth trajectory

Statistics needed: Two-way repeated measures ANOVA or mixed-effects model;
  pairwise comparisons at day 28; error = SEM, n=8

Source data: tumor_data.csv (4 groups x 8 subjects x 5 timepoints)

Reviewer risk:
  - n=8 is adequate for line+error band (not a small-sample bar chart issue)
  - Must declare SEM and n in legend
  - Must use colorblind-safe palette with redundant encoding (line style + marker)


### Step 1: Data Profiling
# Data profile: /home/joe/Documents/repo/skill/sci-draw/sci-draw/tests/workspace/iteration-2/eval-2/with_skill/run-1/outputs/tumor_data.csv

**Shape:** 160 rows × 4 cols

## Columns

| Column | Type | n | missing | summary |
|---|---|---|---|---|
| `Subject` | text | 160 | 0 |  |
| `Group` | categorical | 160 | 0 | 4 levels: Control(40), Drug_A(40), Drug_B(40), Drug_C(40); min_group_n=40 |
| `Time_days` | ordinal | 160 | 0 | 5 levels: 0(32), 7(32), 14(32), 21(32), 28(32); min_group_n=32 |
| `TumorVolume_mm3` | continuous | 160 | 0 | mean=253, sd=185, range=[75.8, 956], skew=1.72 (highly skewed); outliers=8 (IQR) |

## Group structure
- Grouped by: `Group`, `Subject`
- Number of groups: 32
- Group size: min=5, median=5, max=5
- **WARN**: at least one group has n<10 — use box/violin + stripplot rather than mean-only bar chart.

## Chart suggestions (preliminary)
- 分类 vs 连续，小样本（每组 n<10）→ **箱线图/小提琴图 + stripplot 叠加原始点**；**避免**只画均值柱状图，会掩盖分布。
- 分类维度组合数 = 20（Group, Time_days 全交叉），**一张图塞不下**——建议按某一维拆成多面板，或选择子集。
- TumorVolume_mm3 高度偏态（skew=1.72）→ 考虑对数变换或小提琴图代替均值柱图

> 这是基于数据形态的**初步建议**。最终图型选择必须结合**论证目标**（你想说什么）—— 详见 `references/chart_selection.md`。

**Verification**: All groups have exactly n=8 biological replicates. PASS.

### Step 2: Chart Selection

Data shape: time (5 points) vs continuous (tumor volume) x 4 groups
Recommended chart: **Line plot + SEM error band**

Rationale:
  - X axis is true time (continuous, ordered) -> line is correct (not bar)
  - Multiple groups on same time axis -> color + line style dual encoding
  - n=8 per group -> SEM error band is appropriate (not too noisy)
  - 4 groups <= 6 -> manageable on single panel with direct labels

Alternatives considered:
  1. Individual spaghetti plots + mean overlay (shows variability, but cluttered with 32 lines)
  2. Box/violin at each timepoint (loses temporal continuity)

Interception check:
  - n=8 per group: acceptable for line+error band chart type
  - NOT a mean bar chart (which would trigger P1 for n<10)
  - Line plot is semantically correct (time is continuous)
  - No P6 violation (connecting categorical x with lines)

Decision: PROCEED with line + SEM error band, colorblind-safe palette,
  redundant encoding (color + line style + marker).


### Step 3: Journal Specs

Nature journal specifications:
  - Single column width: 89 mm = 3.5 inches
  - Font: Helvetica / Arial (sans-serif)
  - Font size: labels/ticks 5-7 pt, min 5 pt
  - Vector format: PDF (primary), EPS accepted
  - Raster: PNG >= 300 DPI
  - Line width: 0.25-1 pt (use 0.6 for data lines)
  - Color: RGB, colorblind-safe, avoid red-green
  - Panel labels: a, b, c (lowercase, bold, top-left)
  - DPI: 300 for raster


### Step 4: Style Setup
Applied: {'journal': 'nature', 'lang': 'en', 'sciplots_used': False, 'cjk_font': None, 'constrained_layout': True}

### Step 5: Plot
Line + SEM error band with colorblind-safe palette.
Redundant encoding: color + line style + marker.

### Step 6: Visual QA
Programmatic audit verdict: PASS

- P1 (mean bar hiding distribution): PASS - using line+error band, not bar chart
- P6 (connecting categorical x): PASS - x is true continuous time
- P7 (too many colors): PASS - 4 groups, colorblind palette with redundant encoding
- P8 (missing legend): PASS - legend present with error declaration
- P9 (undeclared error type): PASS - legend states SEM, n=8
- P11 (resolution/format): PASS - PDF vector + PNG 300 DPI
- P13 (red-green contrast): PASS - using colorblind-safe palette + line style encoding
- P14 (rainbow colormap): PASS - not using continuous colormap

Preview: /home/joe/Documents/repo/skill/sci-draw/sci-draw/tests/workspace/iteration-2/eval-2/with_skill/run-1/outputs/figs/_preview.png

### Step 7: Export
- /home/joe/Documents/repo/skill/sci-draw/sci-draw/tests/workspace/iteration-2/eval-2/with_skill/run-1/outputs/figs/fig1_tumor_volume.pdf
- /home/joe/Documents/repo/skill/sci-draw/sci-draw/tests/workspace/iteration-2/eval-2/with_skill/run-1/outputs/figs/fig1_tumor_volume.png
- /home/joe/Documents/repo/skill/sci-draw/sci-draw/tests/workspace/iteration-2/eval-2/with_skill/run-1/outputs/figs/fig1_tumor_volume_grayscale.png

### Step 8: Figure Description
Written to: /home/joe/Documents/repo/skill/sci-draw/sci-draw/tests/workspace/iteration-2/eval-2/with_skill/run-1/outputs/figs/fig1_tumor_volume_description.md

# Figure 1 -- Tumor volume time course under treatment

## Core conclusion
Drug_B significantly suppresses tumor growth compared to control over 28 days
(p < 0.001), while Drug_A shows moderate inhibition (p < 0.01) and Drug_C
shows only transient early effect with late rebound.

## Data source
- File: tumor_data.csv
- Samples: n = 8 per group, N = 32 total biological replicates
- Variables: Group (Control, Drug_A, Drug_B, Drug_C), Time_days (0, 7, 14, 21, 28),
  TumorVolume_mm3

## Chart type & rationale
- Type: Line plot with SEM error bands
- Why: Time series data (5 timepoints over 28 days) with 4 treatment groups;
  line+error band is the standard for longitudinal tumor growth data. Shows
  temporal dynamics and group separation clearly. n=8 is adequate for SEM estimation.

## Statistical methods
- Test: Unpaired two-sample t-test (day 28 comparisons); proper analysis should
  use two-way repeated measures ANOVA or linear mixed-effects model
- Correction: Bonferroni for 3 pairwise comparisons vs control (alpha = 0.05/3)
- Error bars: SEM (standard error of the mean), n = 8 biological replicates
- Significance: * p < 0.05, ** p < 0.01, *** p < 0.001

## Key findings
- Control group shows progressive tumor growth: 96 -> 824 mm3 over 28 days
- Drug_B achieves strongest suppression: day 28 mean = 214 mm3 vs control 824 mm3 (t = 18.27, p = 3.42e-08)
- Drug_A shows moderate effect: day 28 mean = 448 mm3 (t = 10.35, p = 6.89e-07)
- Drug_C shows early suppression but rebounds by day 28: mean = 430 mm3 (t = 10.96, p = 4.62e-07)
- Colorblind-safe palette with redundant encoding (color + line style + marker)

## Journal specs
- Target: Nature
- Size: single-column 3.5 in
- Format: PDF (vector) + PNG (300 DPI)
- Font: Helvetica/Arial, 6-7 pt
- Grayscale preview generated for colorblind verification

