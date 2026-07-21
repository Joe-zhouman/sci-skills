# Figure Organization for Nature Paper: Deep Learning Protein Structure Prediction

Nature papers typically have 4-6 main figures, each potentially composed of multiple panels (a, b, c...). Here is a recommended layout for your four data categories.

---

## Figure 1: Benchmark Accuracy Comparison (Main Figure)

This is your headline result and should come first. It directly answers "does the method work?"

**Panel a -- Bar chart or grouped bar chart** showing your model vs. 4 baselines across the 3 datasets. Use grouped bars (one group per dataset, bars within each group for methods). This gives readers the big picture at a glance.

**Panel b -- Per-dataset detail plots.** For each dataset, show a more granular metric breakdown (e.g., per-target accuracy or GDT-TS distribution as box plots or violin plots). This handles cases where aggregate metrics hide variability.

**Panel c -- Statistical significance table or heatmap.** A small matrix showing p-values or win/tie/loss counts between your method and each baseline on each dataset. Reviewers will want to see this.

**Tips:**
- Use consistent color coding for each method across all panels.
- Report standard deviations or confidence intervals as error bars.
- If your metric is something like TM-score or GDT-TS, include a horizontal reference line at commonly accepted thresholds.

---

## Figure 2: Ablation Study (Main Figure)

This shows your model is not just a black box -- each component contributes.

**Panel a -- Grouped bar chart** showing performance with the full model and with each component removed (3 ablation conditions + full model = 4 bars per dataset). Display this across the 3 datasets for consistency with Figure 1.

**Panel b -- Component interaction or contribution chart.** A stacked bar or radar/spider chart showing the relative contribution (delta in accuracy) of each component. Alternatively, a simple table inset works well here.

**Panel c -- Qualitative examples.** If possible, show 1-2 structural prediction examples (e.g., protein backbone overlays) comparing the full model vs. ablated variants. Visual structural comparisons are very compelling in the protein folding field.

**Tips:**
- Clearly label what is removed in each ablation (e.g., "w/o attention module", "w/o coevolution features").
- Show the delta (difference) from full model, not just absolute values, so the contribution is immediately obvious.

---

## Figure 3: Training Dynamics (Supplementary or Main Figure)

Training loss curves convey optimization behavior and convergence.

**Panel a -- Training loss curves.** Plot your model and the baseline on the same axes over 200 epochs. Use a log scale on the y-axis if the loss spans orders of magnitude. Shade the standard deviation if you ran multiple seeds.

**Panel b -- Validation loss curves.** Same as above but on validation data. This is where overfitting becomes visible.

**Panel c -- Learning rate schedule or gradient norm (optional).** If you used a non-trivial learning rate schedule (cosine annealing, warm-up, etc.), showing it helps explain the loss curve shape.

**Tips:**
- Smooth the curves with a moving average (window of 5-10 epochs) for readability, but show the raw curves as a faint background.
- Highlight key inflection points (e.g., where your model overtakes the baseline).
- If wall-clock time is more relevant than epoch count (e.g., if per-epoch cost differs), consider plotting against GPU hours instead.

---

## Figure 4: Inference Time / Computational Efficiency (Main or Supplementary Figure)

This addresses the practical deployment question.

**Panel a -- Line plot or log-log plot** of inference time vs. input size (e.g., sequence length or number of residues) for your model and baselines. Log-log axes are standard for scaling analysis.

**Panel b -- Speed-accuracy trade-off scatter plot.** Plot each method as a point (or set of points across datasets) with inference time on the x-axis and accuracy on the y-axis. This is one of the most informative single plots you can make -- it shows Pareto dominance.

**Panel c -- Bar chart of speedup ratios.** Show the fold-speedup of your model over each baseline at a representative input size. This is easy for readers to quote.

**Tips:**
- Report inference time on a single GPU for fair comparison.
- Include a table in the figure caption or as a supplementary table with exact numbers.
- If your model has a different complexity class (e.g., O(n) vs O(n^2)), emphasize the scaling advantage at large input sizes.

---

## Suggested Placement

| Figure | Content | Placement |
|--------|---------|-----------|
| Figure 1 | Benchmark accuracy | Main text |
| Figure 2 | Ablation study | Main text |
| Figure 3 | Training curves | Main text or supplement |
| Figure 4 | Inference time | Main text or supplement |

For a Nature paper, Figures 1 and 2 are almost certainly main-text figures. Figures 3 and 4 could go either way depending on space and how central efficiency is to your story. If speed is a key selling point, keep Figure 4 in the main text and move training curves to supplementary.

---

## General Nature Figure Guidelines

- **Resolution:** 300 DPI minimum for print; use vector formats (PDF, SVG) where possible.
- **Font size:** At least 6 pt after scaling to final print size (single column = 89 mm, double column = 183 mm).
- **Color:** Use colorblind-friendly palettes (e.g., Okabe-Ito, viridis). Nature requires figures to be accessible.
- **Panel labels:** Use lowercase bold letters (a, b, c) in the top-left corner of each panel.
- **Consistent styling:** Same colors, fonts, and axis conventions across all figures.
- **Caption quality:** Each figure caption should be self-contained -- a reader should understand the figure without reading the main text.

---

## Additional Recommendations

1. **Supplementary figures:** Consider adding per-dataset training curves, additional ablation variants, and per-residue accuracy heatmaps as supplementary figures.
2. **Table for exact numbers:** Pair Figure 1 with a supplementary table reporting exact accuracy values, standard deviations, and p-values.
3. **Figure ordering in the paper:** Figures should tell a story in order -- problem context (if needed), main results (Fig 1), why it works (Fig 2), training behavior (Fig 3), practical efficiency (Fig 4).
