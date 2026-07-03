# Worked examples

## Task A: User gives CSV and says "help me plot this for my paper"

**Think-first workflow example:**

1. **Step 0**: Ask "What should this figure convince the reader of?" — group differences? time trends? variable relationships?
2. **Step 1**: Explore the data — run `scripts/profile_data.py` if it's a clean CSV, or inspect directly if the data is more complex. Verify column types manually.
3. **Step 2**: Reason from data shape + claim + sample size to select chart type. **Proactively give recommendation + reason + 1-2 alternatives**
4. **After user confirms** → Steps 3-7: journal style, plot, export, review, finalize.

Don't skip any step.

## Task B: User wants "mean bar chart with 3 groups of 5 samples"

**Active interception example:**

```
The "3 groups of 5 samples mean bar chart" you requested triggers the classic P1 error (see `references/viz_pitfalls.md`) — n=5 is too small, bar height + one error bar can't tell the reader the true data distribution. A reviewer would likely request "show individual data points".

I suggest **boxplot + stripplot overlay** — 5 points directly visible, hiding nothing, actually more convincing. Code is only one extra line.

Proceed with original plan, or switch to box+stripplot?
```

If user insists on bars → at minimum force stripplot overlay showing each point.

## Task C: Multi-panel composite figure

User: "Give me Figure 1: 4 panels — PCA, loss curve, confusion matrix, survival curve."

Flow:
1. Confirm target journal (determines 7.2 in or 7.16 in; Nature `a/b/c` vs IEEE `(a)(b)(c)`)
2. Plot each panel independently, **ensure font size, color palette, axis scales are unified** (same variable = same color across all 4 panels)
3. Combine with `plt.subplots(2, 2, figsize=(7.2, 5.4))`
4. `layout_tools.finalize_figure(fig)` then `add_panel_labels(fig, style='nature')` — **unified figure-coordinate alignment**, don't hand-place `ax.text` (prone to misalignment, see `references/viz_pitfalls.md` P18)
5. Export, then visually review per `references/visual_review.md` checklist.

Recipe in `references/plot_recipes.md` section 9.

## Task D: Statistical figure with significance annotations

User: "3 groups, boxplot with significance bars."

Flow:
1. Explore to confirm n (n<10 → must overlay stripplot)
2. Run statistical test (**user must state** which test, whether multiple comparison correction applied)
3. Plot box + stripplot
4. Use `matplotlib.lines.Line2D` or `statannotations` for significance bridges
5. **Legend must state**: error type / n / test method / correction / symbol definition

Recipe in `references/plot_recipes.md` section 4.
