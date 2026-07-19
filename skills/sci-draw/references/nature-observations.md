# High-Impact Journal Figure Observations

Concrete multi-panel patterns observed in Nature, Science, Cell, and top field journals.
Each entry describes a real figure layout with panel count, arrangement, and what makes it work.
Use these as templates when mapping evidence chains to panel layouts.

---

## Pattern 1: Clinical/Translational Cascade (6-8 panels)

**Seen in**: gene therapy trials, immunotherapy cohorts, vaccine studies.

**Layout**: 3 rows × 2-3 columns, reading top-to-bottom.

```
Row 1 (system):     [a] Cohort CONSORT/design  [b] Baseline characteristics table/heatmap
Row 2 (main):       [c] Primary endpoint (line/bar + individual points)
Row 3 (mechanism):   [d] Biomarker waterfall      [e] Responder vs non-responder
Row 4 (robustness):  [f] Subgroup forest plot     [g] Safety/adverse events summary
```

**Actionable rules**:
- Panel c (primary endpoint) gets the largest area — this is the hero
- Panel f (forest plot) shares the same y-axis labels across subgroups; use one vertical reference line at 1.0 or 0
- Panel d (waterfall) sorts by effect size, colors by response category
- Baseline table (b) can be a heatmap or compact bar grid — it's reference, not argument
- Use one shared color mapping: responders = warm, non-responders = cool, across all panels
- Legend sits above the primary endpoint row, not repeated per panel

**Panel count**: 6-8. Never fewer than 5 — the cascade collapses without mechanism AND robustness.

---

## Pattern 2: Multi-Metric Comparison Grid (4-8 panels)

**Seen in**: method benchmarks, model comparisons, multi-tissue expression panels.

**Layout**: 2-4 rows × 2 columns, shared axes within each row.

```
Row 1 (overview):   [a] PCA / UMAP embedding       [b] Variance explained / scree
Row 2 (main):        [c] Primary metric bar/box     [d] Pairwise comparison heatmap
Row 3 (detail):      [e] Per-category breakdown     [f] Top-N ranked features
Row 4 (robustness):  [g] Sensitivity to parameters  [h] Independent validation cohort
```

**Actionable rules**:
- Each row answers one question. Row 1 = "What's the landscape?", Row 2 = "What's different?", Row 3 = "How big and where?", Row 4 = "Does it hold?"
- Shared x-axis or y-axis within each row — aligned scales invite comparison
- Use one consistent color mapping: method A = blue family, method B = green family, baseline = grey
- Panel labels in top-left of each panel, small bold lowercase
- When a row has only one panel, let it span both columns

**Panel count**: 4-8. Start with 4 rows × 2 cols = 8, then drop rows the data can't support. Never drop both mechanism AND robustness — keep at least one.

---

## Pattern 3: Time/Longitudinal Evidence Chain (5-7 panels)

**Seen in**: disease progression, treatment response over time, developmental series.

**Layout**: mixed — hero panel spans full width, supporting panels flank below.

```
Top (main):         [a] Spaghetti plot — all subjects over time, colored by group (FULL WIDTH)
Bottom row:         [b] Endpoint bar/box           [c] Δ-from-baseline waterfall
                    [d] Time-to-event KM curve     [e] Landmark analysis at key timepoint
Optional:           [f] Correlation: Δ at t1 vs Δ at t2
```

**Actionable rules**:
- Panel a is the hero — it shows individual trajectories, not just group means. This is what separates a publication figure from a conference slide
- Panel b shows the collapsed endpoint (loses time resolution, gains statistical clarity)
- Panel c shows who changed and by how much — sort by magnitude
- Panel d (KM curve) adds the clinical/biological meaning: not just "did it change?" but "did it matter?"
- Panels b-e answer different questions, never re-display the same data slice
- One legend for the group-color mapping, placed above or to the right of the hero panel

**Panel count**: 5-7. Panel a alone already has more information than a bar chart, but panels b-e are what make the conclusion review-proof.

---

## Pattern 4: Dose-Response / Concentration Series (4-6 panels)

**Seen in**: pharmacology, toxicology, dose-escalation, concentration-gradient experiments.

**Layout**: 2-3 rows, left-to-right increasing complexity.

```
Row 1 (main):       [a] Dose-response curve (sigmoid fit + individual points)
Row 2 (detail):     [b] IC50/EC50 bar comparison   [c] Hill slope / efficacy max bar
Row 3 (mechanism):  [d] Representative traces at selected doses
                    [e] Time course at EC50 concentration
```

**Actionable rules**:
- Panel a: show individual data points, not just the fitted curve — n matters for dose-response
- Panels b-c: derived parameters from the fit, with error (confidence interval of the fit)
- Panel d: raw traces at key concentrations (vehicle, EC50, max) — this is the "trust me" panel
- Use a sequential colormap (light to dark) to encode dose across all panels
- If multiple compounds: one hue per compound, saturation = dose

**Panel count**: 4-6. Panel d (raw traces) is the most commonly cut panel — and the one reviewers most commonly request. Include it.

---

## Pattern 5: Genomics / High-Throughput Panel (5-8 panels)

**Seen in**: RNA-seq, ChIP-seq, proteomics, single-cell studies.

**Layout**: asymmetric — one large overview panel + grid of targeted follow-ups.

```
Top left (overview):  [a] Volcano plot or MA plot (FULL HEIGHT, 40% width)
Top right (detail):   [b] Top DEG heatmap (z-score, 60% width)
Bottom row:           [c] GO/KEGG enrichment bar   [d] GSEA enrichment curve
                      [e] Representative genome browser tracks
                      [f] qPCR validation of top hits
```

**Actionable rules**:
- Panel a: label top N hits by gene name directly on the plot — no legend needed
- Panel b: z-score heatmap, not absolute expression — shows what's atypical per gene
- Panel c (GO bars): horizontal bars, sorted by -log10(p), colored by ontology (BP/CC/MF)
- Panel d (GSEA): one curve per comparison, leading edge marked
- Panel e: tracks at key loci — the "visual proof" panel
- Panel f: wet-lab validation — small, compact, visually subordinate
- Use RdBu_r for heatmaps, viridis for continuous, Okabe-Ito for categorical

**Panel count**: 5-8. Enrichment (c-d) and validation (f) are the panels that distinguish a publication figure from a supplemental figure.

---

## Pattern 6: Comparative Anatomy / Multi-Group Panel (4-7 panels)

**Seen in**: multi-species comparisons, tissue panels, cell-type atlases.

**Layout**: grid with one dominant row.

```
Row 1 (overview):   [a] Representative images / schematics of groups (FULL WIDTH)
Row 2 (quant):      [b] Primary metric comparison   [c] Secondary metric
Row 3 (detail):     [d] Correlation: metric1 vs metric2, colored by group
                    [e] Distribution / histogram overlay by group
Optional:           [f] Phylogenetic or clustering context
```

**Actionable rules**:
- Panel a establishes the visual vocabulary for what follows — group colors are born here
- Panel b: box/violin + stripplot overlay — every data point visible, not hidden behind bars
- Panel d: scatter colored by group, with regression lines per group or overall r value
- Panel e: histogram/ridge plot overlays — transparent fills, direct group labels on ridges
- Group color mapping invented in panel a, reused identically in panels b-e

**Panel count**: 4-7. Panel a is essential — without it, the reader doesn't know what's being compared.

---

## Cross-Pattern Rules

These apply regardless of which pattern you're using:

### Panel count heuristics
- **3 panels is a figure fragment, not a complete argument.** You can show a main effect but not the system, mechanism, or robustness. 3-panel figures should prompt the question: "What evidence is missing?"
- **4-5 panels is the minimum for a complete evidence chain.** System + main effect + mechanism/quantification + one layer of robustness.
- **6-8 panels is standard for high-impact journal main figures.** The additional panels are not decoration — they preempt reviewer questions.
- **8+ panels only when the archetype demands it** (genomics multi-omics, clinical cascade with multiple endpoints).

### Panel labels
- Lowercase bold letters (a, b, c…) in top-left corner of each panel
- Font size: 1.2-1.5× the body label size
- Never use uppercase, never use numbers alone, never place at bottom

### Color consistency
- One variable = one color across ALL panels in the figure
- Hero group gets the most saturated color; controls are muted
- Direct labels over legends whenever categories are spatially fixed
- Shared legend strip above a row, not repeated per panel

### Evidence density
- Each panel should contain exactly one insight. If a panel needs a paragraph to explain, split it
- Bar charts with >8 bars → horizontal layout or split into two panels
- Heatmaps with >50 rows → cluster and show dendrogram, or focus on top-N

### What to protect from pruning
When the user asks to simplify, protect these panels (in order):
1. System/overview — without it, the figure floats in a vacuum
2. Main effect — the figure's reason for existing
3. One robustness/control — at least one check that the effect isn't noise
4. Individual data points — aggregate bars without raw points are the #1 reviewer complaint

Panels that can usually be moved to supplementary:
- Extended subgroup analyses beyond the primary stratification
- Per-sample breakdowns when N > 50
- Alternative normalization or parameter choices (can be a supp figure showing consistency)
