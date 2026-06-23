# Figure Strategy for Nature Paper: Deep Learning Protein Structure Prediction

## Paper Narrative Summary

The paper has four evidence streams that must defend three core claims:
1. **Superiority**: Our model outperforms 4 baselines across 3 datasets
2. **Mechanism**: Each of 3 model components contributes meaningfully to performance
3. **Practicality**: The model trains efficiently and scales well at inference time

I recommend **3 figures** with a clear division of labor -- one figure per claim.

---

## Figure 1 -- Main Benchmark Result (the hero figure)

**Archetype**: `quantitative grid`
**Layout**: Nature double-column (183 mm / 7.2 inch wide)
**Core claim**: Our model outperforms all 4 baseline methods across all 3 datasets.

### Panel composition

| Panel | Content | Chart type | Justification |
|-------|---------|------------|---------------|
| (a) | Benchmark accuracy on Dataset 1: 5 methods | Grouped bar with error bars | Direct method-to-method comparison per dataset; small multiples across datasets for instant cross-dataset pattern reading |
| (b) | Benchmark accuracy on Dataset 2: 5 methods | Grouped bar with error bars | Same structure as (a); shared y-axis scale enables immediate visual comparison |
| (c) | Benchmark accuracy on Dataset 3: 5 methods | Grouped bar with error bars | Completes the cross-dataset picture |
| (d) | Summary heatmap: methods (rows) x datasets (columns), color = accuracy | Heatmap (viridis) | Compact overview showing our method is consistently best; reinforces the per-panel pattern in one glance |

### Figure contract

```
Core conclusion:  Our model achieves the highest accuracy across all 3 benchmark
                  datasets, outperforming all 4 baselines.
Figure archetype: quantitative grid
Target journal:   Nature (English)
Final size:       183 mm x ~140 mm (double-col, 4 panels in 2x2 grid)
Panel map:
  a: Dataset 1 benchmark (grouped bar, 5 methods)
  b: Dataset 2 benchmark (grouped bar, 5 methods)
  c: Dataset 3 benchmark (grouped bar, 5 methods)
  d: Summary heatmap (methods x datasets)
Evidence hierarchy:
  hero evidence:       panels (a-c) showing per-dataset dominance
  validation evidence: panel (d) confirming consistency across datasets
Statistics needed:     mean accuracy + SD/SEM/95% CI per method per dataset,
                       significance tests (paired t-test or Wilcoxon) with
                       Bonferroni correction for 4 pairwise comparisons
Source data needed:    per-fold or per-run accuracy values (to compute error bars)
Reviewer risk:         (1) Are error bars from same evaluation protocol across methods?
                       (2) Are datasets diverse enough to claim generalization?
                       (3) Is the y-axis starting at 0 (or at a meaningful baseline)?
```

### Chart selection rationale

Grouped bar chart is the right choice here because:
- x-axis categories (methods) are discrete and unordered
- We want to compare magnitudes across methods within each dataset
- n=5 methods is within the readable range for grouped bars
- Error bars are essential and natural on bars

**Alternative considered**: A single heatmap without per-dataset panels. Rejected because per-dataset bar charts let readers see error bar magnitude and significance markers, which a heatmap cannot show.

### Pitfall interceptions

- **P1 risk (mean bar hiding distribution)**: If individual fold/run scores are available (e.g., 5-fold cross-validation), overlay stripplot dots on each bar. If only aggregated metrics exist, ensure the legend states "mean +/- SD, n=5 folds" explicitly.
- **P4 risk (y-axis truncation)**: Accuracy values should start from 0 or from a meaningful random baseline (e.g., 25% for 4-class). Do NOT start at 90% just to amplify small differences -- a reviewer will flag this immediately.
- **P9 risk (undeclared error)**: The figure legend must state whether error bars are SD, SEM, or 95% CI, and the number of replicates/folds.

---

## Figure 2 -- Ablation Study

**Archetype**: `quantitative grid`
**Layout**: Nature single-column (89 mm / 3.5 inch wide)
**Core claim**: Each of the 3 model components contributes to the overall performance gain.

### Panel composition

| Panel | Content | Chart type | Justification |
|-------|---------|------------|---------------|
| (a) | Ablation: full model vs. 3 ablated variants (4 conditions) | Horizontal bar chart (sorted by accuracy, descending) | Horizontal bars allow long method names on y-axis; sorting by value makes ranking immediately visible |
| (b) | Per-component delta: accuracy drop when removing each component | Horizontal bar chart (3 bars, descending by delta) | Isolates each component's marginal contribution; the "what do you lose" view |

### Figure contract

```
Core conclusion:  Removing any single component degrades performance, confirming
                  all three components are necessary.
Figure archetype: quantitative grid
Target journal:   Nature (English)
Final size:       89 mm x ~120 mm (single-col, 2 stacked panels)
Panel map:
  a: Full model vs ablated variants (horizontal bar, 4 conditions)
  b: Per-component accuracy delta (horizontal bar, 3 components)
Evidence hierarchy:
  hero evidence:       panel (a) showing full model beats all ablated variants
  validation evidence: panel (b) showing each component has non-trivial contribution
Statistics needed:     mean accuracy + SD per ablation condition; significance
                       of each removal vs full model (paired test)
Source data needed:    per-fold accuracy for each ablation variant
Reviewer risk:         (1) Are the 3 components truly independent (no interaction)?
                       (2) Is the ablation fair (only one component removed at a time)?
                       (3) Could reviewer ask for all 2-way ablation combinations?
```

### Chart selection rationale

Horizontal bar is preferred over vertical bar here because:
- Ablation variant names can be long and descriptive
- Horizontal layout avoids rotated x-axis labels
- Sorting by value creates a natural ranking visual

**Alternative considered**: A table of numbers. Rejected because a chart makes the magnitude of each component's contribution instantly readable; a table requires mental arithmetic.

### Pitfall interceptions

- **P1 risk**: If n folds is small (e.g., 3-5), overlay individual data points on each bar. Do not show only mean +/- error bar.
- **P6 risk (connecting discrete categories with lines)**: The 3 components are categorical, not ordered. Do NOT connect them with a line. Use separate bars.
- **P12 risk (one figure, multiple claims)**: This figure has one claim ("all components matter"). The two panels are two views of the same evidence, not two separate claims. This is acceptable.

---

## Figure 3 -- Training Dynamics and Inference Efficiency

**Archetype**: `quantitative grid`
**Layout**: Nature double-column (183 mm / 7.2 inch wide)
**Core claim**: Our model converges as fast as the baseline during training and scales efficiently at inference time.

### Panel composition

| Panel | Content | Chart type | Justification |
|-------|---------|------------|---------------|
| (a) | Training loss over 200 epochs: our model vs baseline | Line plot + error band (shaded 95% CI or SD) | x is continuous (epochs); line is the correct representation; error band shows run-to-run variability |
| (b) | Validation accuracy over 200 epochs: our model vs baseline | Line plot + error band | Same structure as (a) but on the validation metric; shows generalization, not just training fit |
| (c) | Inference time vs input size: our model vs baselines | Scatter + line (log-log scale if input sizes span >1 order of magnitude) | x is continuous (input size); log-log reveals scaling exponent; scatter shows actual measurements, line connects them |
| (d) | Inference time bar chart at one representative input size | Grouped bar (methods compared) | Concrete "here is the actual number" anchor; complements the scaling curve in (c) |

### Figure contract

```
Core conclusion:  Our model trains efficiently (comparable convergence) and has
                  competitive or better inference scaling across input sizes.
Figure archetype: quantitative grid
Target journal:   Nature (English)
Final size:       183 mm x ~140 mm (double-col, 4 panels in 2x2 grid)
Panel map:
  a: Training loss curves (line + error band, 2 methods x 200 epochs)
  b: Validation accuracy curves (line + error band, 2 methods x 200 epochs)
  c: Inference time vs input size (scatter + line, log-log if needed)
  d: Inference time at representative size (grouped bar, 5 methods)
Evidence hierarchy:
  hero evidence:       panels (a-b) showing convergence; panel (c) showing scaling
  validation evidence: panel (d) providing a concrete efficiency number
Statistics needed:     mean +/- SD over N independent training runs (ideally >=3)
                       for loss/accuracy curves; mean +/- SD over K runs for
                       inference time
Source data needed:    per-epoch loss/accuracy from multiple runs; per-input-size
                       inference timing from multiple runs
Reviewer risk:         (1) Were the baselines trained with the same compute budget?
                       (2) Is inference time measured on the same hardware?
                       (3) Are the input sizes representative of real protein lengths?
```

### Chart selection rationale

- **Line plot for training curves**: Epochs are a true continuous sequence; lines are the correct visual metaphor. Error bands (not error bars at sampled points) show the full trajectory of variability.
- **Scatter + line for inference time**: Input sizes may not be evenly spaced, so scatter shows the actual measurement points. Connecting with a line reveals the scaling trend. If sizes span 100 to 100,000 residues, use log-log axes -- the slope then directly shows the computational complexity exponent (O(n), O(n log n), O(n^2)).
- **Bar chart anchor in (d)**: Reviewers often want one concrete number ("at 500 residues, your model takes X ms vs Y ms for baseline"). Panel (d) provides this.

### Pitfall interceptions

- **P2 risk (dual y-axis)**: Training loss and validation accuracy have different scales and units. Do NOT put them on the same axes with dual y-axis. Use separate panels (a) and (b). This is a classic trap -- a dual y-axis would fabricate visual convergence/divergence patterns.
- **P6 risk**: Do NOT connect inference time data points if input sizes are categorical (e.g., "small/medium/large"). Only connect if input size is truly continuous. If categorical, use grouped bars instead.
- **P9 risk**: Error bands must be labeled. State in the legend: "shaded band = SD across 3 independent training runs" (or 95% CI, whichever you use).
- **P14 risk (rainbow/jet colormap)**: Not applicable here since we are using categorical color assignment for methods, not a continuous colormap. But ensure the 2-5 method colors are from the colorblind-safe palette.

---

## Cross-Figure Design System

### Unified color palette

Assign one consistent color to each method across all three figures:

```
Our model:    #0072B2  (blue)       -- always the "signal" color, most prominent
Baseline 1:   #E69F00  (orange)
Baseline 2:   #009E73  (teal/green)
Baseline 3:   #CC79A7  (pink/mauve)
Baseline 4:   #999999  (grey)
```

This is the Okabe-Ito-derived palette, which is colorblind-safe and prints well in grayscale. Redundant encoding: our model uses a thicker line or filled marker; baselines use thinner lines or open markers.

### Shared style settings

- Font: Helvetica (Nature's recommended sans-serif), 7 pt for labels, 6 pt for tick labels
- Line width: 0.6 pt (Nature recommends thinner than matplotlib default)
- Panel labels: lowercase bold **a**, **b**, **c**, **d** in top-left corner (Nature convention)
- Legend: placed outside data area (`bbox_to_anchor`), `frameon=False`
- Background: white, no grid or minimal horizontal grid only
- Despine: remove top and right spines

### Export specifications

| Figure | Size (inches) | Format | DPI |
|--------|---------------|--------|-----|
| Fig 1  | 7.2 x 5.5    | PDF (vector) + PNG 300 | 300 |
| Fig 2  | 3.5 x 4.5    | PDF (vector) + PNG 300 | 300 |
| Fig 3  | 7.2 x 5.5    | PDF (vector) + PNG 300 | 300 |

All exported at final size -- never rescale in LaTeX/Word after export (Rule 1).

---

## Recommended Execution Order

1. **Figure 1 first** -- it is the hero figure and sets the visual vocabulary (colors, method names, style). Every subsequent figure reuses this palette.
2. **Figure 2 second** -- the ablation supports the main result and uses the same style system.
3. **Figure 3 third** -- efficiency analysis is the weakest claim (contributes least to novelty) and should be polished last.

For each figure, the workflow is:
Step 1 (contract, above) -> Step 2 (profile data) -> Step 3 (select chart) -> Step 4 (journal specs) -> Step 5 (setup style) -> Step 6 (plot) -> Step 7 (visual QA loop) -> Step 8 (export).

---

## Supplementary Figures (optional)

If the paper has space or the journal requires supplementary material:

- **Supplementary Fig S1**: Full confusion matrices per dataset (heatmap) -- shows per-class performance, not just aggregate accuracy.
- **Supplementary Fig S2**: Learning rate sensitivity / hyperparameter sweep (line plots).
- **Supplementary Fig S3**: Per-residue accuracy or GDT-TS distribution (box + stripplot) -- shows performance at finer granularity than global metrics.

These are not part of the main narrative but preemptively answer reviewer questions.

---

## Pre-submission Checklist Summary

Before export, verify each figure against these rules:

- [ ] All error bars/ bands declare SD/SEM/CI + n in legend (Rule 5)
- [ ] Font size >= 6 pt at final printed size (Rule 4)
- [ ] Colorblind-safe palette with redundant encoding (Rule 3)
- [ ] Vector PDF for data charts, PNG only if raster needed (Rule 2)
- [ ] Plotted at final Nature size, never rescaled (Rule 1)
- [ ] No dual y-axes (P2), no pie charts (P3), no rainbow colormap (P14)
- [ ] y-axis starts at 0 or meaningful baseline for accuracy (P4)
- [ ] Grayscale preview generated and distinguishable (P13)
- [ ] Panel labels aligned, no text clipping, no legend-on-data (P17, P18)
