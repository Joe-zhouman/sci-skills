# P1 Interception: Mean Bar Chart with n=6 per Group

## User Request

"I have 3 groups with n=6 each. I want a bar chart showing the mean with error bars for my Science paper."

---

## Step 0 -- Figure Contract

| Field | Value |
|---|---|
| **Core conclusion** | (User must confirm) Comparison of a continuous outcome across 3 experimental groups |
| **Evidence chain** | Single panel: group-level comparison of means/distributions |
| **Archetype** | Quantitative grid |
| **Target journal** | **Science** -- single-column 55 mm (2.2 in), 1.5-column 120 mm (4.7 in), double-column 183 mm (7.2 in) |

---

## Step 1 -- Data Profile Summary

| Property | Value |
|---|---|
| Groups | 3 |
| n per group | 6 |
| Total N | 18 |
| Data shape | 1 categorical + 1 continuous |
| Small-sample flag | **YES** -- n < 10 per group |

---

## Step 2 -- Chart Selection: ACTIVE INTERCEPTION (P1)

> **The "mean bar chart with 3 groups of n=6 each" you requested triggers P1 -- mean bar hides distribution and sample size.**
>
> With n=6, a bar showing only the mean plus one error bar cannot convey the true data
> distribution. A reviewer at Science cannot tell whether:
>
> - one outlier is pulling the mean,
> - the data are bimodal or skewed,
> - or the six observations cluster tightly.
>
> Bars with small n make reviewers suspect you are hiding something. Multiple journals
> (PLoS Biology, Nature Methods) have published editorials discouraging "naked mean bars"
> since 2020.
>
> **I recommend: boxplot + stripplot overlay.** All 6 data points per group are visible
> directly; the box shows median and IQR at a glance; nothing is hidden. The code is only
> one extra line compared to a bar chart.
>
> **Alternatives:**
> 1. Stripplot / dot plot only (simplest, best when n < 6)
> 2. Violin + stripplot (more informative density shape, but n=6 is borderline for KDE)
>
> Proceed with original mean-bar plan, or switch to boxplot + stripplot?

**Outcome**: User accepted the interception. Proceeding with boxplot + stripplot overlay.

### Comparison: Mean Bar vs. Box+Stripplot

| Criterion | Mean Bar (original) | Box + Stripplot (intercepted) |
|---|---|---|
| Shows individual points | No | Yes (all 6 visible) |
| Shows distribution shape | No | Yes (median, IQR, range) |
| Hides nothing | No (summary only) | Yes |
| Reviewer acceptance (n=6) | High rejection risk | Standard practice |
| Code complexity | 2 lines | 3 lines |
| Science journal compliance | Violates P1 | Fully compliant |

---

## Step 3 -- Journal Specs (Science)

| Spec | Value |
|---|---|
| Figure width | 4.7 inch (120 mm, 1.5-column -- recommended for 3 groups) |
| Font | Helvetica / Arial, 5-7 pt |
| DPI | >= 300 (vector PDF preferred) |
| Panel labels | A, B, C (uppercase, bold, top-left) |
| Vector format | PDF |

---

## Step 4-7 -- Intercepted Solution Script

See `plot_figure.py` in this directory. Key design choices:

- **Chart**: `sns.boxplot` + `sns.stripplot` overlay (black dots on colored boxes)
- **Size**: 4.7 x 3.0 inches (Science 1.5-column, 120 mm)
- **Palette**: `sns.color_palette('colorblind', 3)` -- colorblind-safe
- **Strip**: black, size=4, alpha=0.7, jitter=0.15 -- all 6 points visible per group
- **Error declaration**: text annotation below axes stating "Box: median + IQR; dots: individual replicates; n = 6 per group."
- **Export**: PDF (vector) + PNG (300 DPI) + grayscale preview via `export_figure()`

---

## Visual QA Notes

Before final export, verify:

1. All 6 data points per group are visible and not overlapping excessively (adjust `jitter` if needed)
2. Box plot median line is distinguishable from box edges
3. Font sizes are >= 6 pt at final printed size
4. Grayscale preview shows distinguishable groups (redundant encoding: box position already provides categorical distinction)
5. Legend/caption clearly states: error type (IQR), n = 6 per group

---

## Error Declaration (mandatory for Science)

> Box plots show median and interquartile range (IQR); whiskers extend to 1.5x IQR.
> Individual data points are overlaid (n = 6 per group).

---

## Files

- `plot_figure.py` -- the generation script (uses setup_style + export_figure from skill)
- `fig_boxplot_stripplot.pdf` -- vector output
- `fig_boxplot_stripplot.png` -- raster output at 300 DPI
- `fig_boxplot_stripplot_grayscale.png` -- colorblind check
