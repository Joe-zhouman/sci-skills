# Figure Plan -- CRISPR Guide RNA Editing Efficiency

**Target journal**: Science
**Manuscript claim**: Systematic evaluation of five guide RNAs reveals that guide design determines on-target editing efficiency, off-target risk, and functional outcomes in CRISPR-Cas9 gene editing.

---

## Science Journal Specifications

| Parameter | Value |
|---|---|
| Single column | 55 mm / 2.2 inch |
| 1.5 column | 120 mm / 4.7 inch |
| Double column | 183 mm / 7.2 inch |
| Font | Helvetica / Arial, 5-7 pt |
| Panel labels | A, B, C (uppercase, bold, upper-left) |
| Vector format | PDF / EPS |
| Bitmap DPI | >= 300 (line art >= 600) |

---

## Core Narrative

The manuscript argues that guide RNA design is the primary determinant of CRISPR editing success. The four figures build a sequential argument:

1. **Figure 1** establishes the experimental system and validates it (the reader trusts the platform).
2. **Figure 2** delivers the main comparison: five guides differ dramatically in on-target efficiency (the central claim).
3. **Figure 3** addresses the reviewer's first objection -- off-target effects differ by guide and must be evaluated alongside efficiency (the safety argument).
4. **Figure 4** closes the loop: editing efficiency translates to measurable functional outcomes, not just molecular events (the biological significance argument).

---

## Visual Vocabulary (Established in Figure 1, Reused Throughout)

### Color palette (colorblind-safe)

| Element | Color | Hex | Usage |
|---|---|---|---|
| Guide RNA 1 (gRNA-1) | Deep blue | #0F4D92 | All figures |
| Guide RNA 2 (gRNA-2) | Teal | #2B9086 | All figures |
| Guide RNA 3 (gRNA-3) | Gold/amber | #D4A017 | All figures |
| Guide RNA 4 (gRNA-4) | Coral/orange | #E8714A | All figures |
| Guide RNA 5 (gRNA-5) | Muted red | #B64342 | All figures |
| Control / Untreated | Gray | #8C8C8C | Figures 2, 4 |
| Negative / Off-target | Light gray | #C0C0C0 | Figure 3 background |

Each guide also gets a unique marker shape (circle, square, triangle-up, diamond, triangle-down) and line style (solid, dashed, dotted, dash-dot, long-dash) for redundant encoding. This is critical for Science's grayscale printing requirements.

### Font and annotation conventions

- Font: Helvetica / Arial, 6 pt for labels, 5.5 pt for tick labels
- Panel labels: uppercase bold (A, B, C, D), positioned upper-left
- Error bars: SEM, with n and statistical test declared in legend or caption
- Significance: * p < 0.05, ** p < 0.01 (Mann-Whitney U with Bonferroni correction)
- Scale bars: on all microscopy/image panels with unit annotation

---

## Figure 1: Experimental Design and Validation

- **Core conclusion**: The CRISPR editing platform is technically sound and reproducible, establishing the experimental framework for the subsequent efficiency comparisons.
- **Archetype**: Schematic-led composite
- **Journal size**: 1.5 column (120 mm / 4.7 inch wide) -- the schematic needs horizontal space
- **Estimated height**: ~4.0 inch (to accommodate schematic + validation row)

### Panel map

| Panel | Content | Evidence role | Chart type | Size allocation |
|---|---|---|---|---|
| A | Experimental design schematic: Cas9 protein, target gene locus, five guide RNA binding sites marked with color-coded arrows on the genomic locus | Hero -- establishes the system | Schematic diagram (non-data panel, drawn in matplotlib or imported SVG) | ~50% of figure width |
| B | Cas9 protein expression validation (Western blot quantification or RT-qPCR of Cas9 mRNA across cell lines) | Validation -- platform works | Strip plot (n = 3-4 biological replicates per condition) | ~25% of width |
| C | Transfection efficiency control (flow cytometry % GFP+ cells across all conditions) | Validation -- delivery is consistent | Strip plot with connecting line across conditions (paired samples) | ~25% of width |

### Evidence hierarchy

- **Hero**: Panel A -- the schematic defines the visual vocabulary for the entire manuscript. Guide RNA colors, genomic locus representation, and Cas9 icon are reused in Figures 2-4.
- **Validation**: Panels B and C confirm the platform works. These are visually quieter (smaller, fewer annotations) but must pass reviewer scrutiny.

### Data sources

- Panel A: Illustration (no raw data)
- Panel B: Western blot densitometry or qPCR Ct values, n = 3-4 per cell line
- Panel C: Flow cytometry data, n = 3-4 per condition

### Statistics

- Panel B: Descriptive only (mean +/- SEM); no inter-group test needed (validation)
- Panel C: One-way ANOVA across conditions to confirm no significant batch effects; declare n and SEM

### Reviewer risk

- "Is transfection efficiency equivalent across all guide conditions?" -- Panel C directly addresses this.
- "Is Cas9 expression stable?" -- Panel B addresses this.

---

## Figure 2: Editing Efficiency Comparison Across Five Guide RNAs

- **Core conclusion**: Guide RNAs differ significantly in on-target editing efficiency, with gRNA-X achieving the highest indel frequency and gRNA-Y the lowest, demonstrating that guide design is the primary variable.
- **Archetype**: Quantitative grid
- **Journal size**: 1.5 column (120 mm / 4.7 inch wide)
- **Estimated height**: ~3.5 inch

### Panel map

| Panel | Content | Evidence role | Chart type | Size allocation |
|---|---|---|---|---|
| A | Indel frequency (%) at the target locus for all five guides + untreated control, measured by next-generation sequencing (NGS) amplicon sequencing | Hero -- the main efficiency comparison | Box plot + strip plot overlay (n >= 8 biological replicates per guide; show all data points) | ~50% of width |
| B | Editing efficiency over time (0, 24, 48, 72, 96 h post-transfection) for the top 3 guides | Supporting -- shows kinetics | Line plot with error bands (mean +/- SEM), one line per guide (color-coded), time on x-axis | ~50% of width |
| C | Insertion-to-deletion (ins/del) ratio for each guide | Supporting -- shows edit type distribution | Stacked horizontal bar (100% stacked, one bar per guide, ins vs del) | ~33% of width |
| D | Allele frequency distribution for the top-performing guide | Supporting -- shows editing precision | Histogram of allele frequencies at target site | ~33% of width |

### Evidence hierarchy

- **Hero**: Panel A -- the central comparison. This panel must be immediately readable. Box + strip plot because n >= 8 (box is reliable) and all points must be visible (strip overlay). Mean bars are forbidden here.
- **Supporting**: Panel B adds temporal context. Panels C and D add mechanistic detail about edit quality, not just quantity.

### Data sources

- Panel A: NGS amplicon sequencing indel quantification, n >= 8 per guide
- Panel B: Time-course NGS data, n = 3-4 per time point per guide
- Panel C: Derived from Panel A data (ins/del classification)
- Panel D: Subset of Panel A data (single guide, all replicates)

### Statistics

- Panel A: Kruskal-Wallis test across guides; pairwise Mann-Whitney U with Bonferroni correction; declare test, correction, n, error type (SEM) in legend
- Panel B: Repeated-measures ANOVA or mixed-effects model; error bands = SEM
- Panel C: Descriptive (proportions)
- Panel D: Descriptive (distribution)

### Shared elements

- Guide RNA colors from Figure 1 legend are reused exactly
- Control (untreated) uses the gray established in the visual vocabulary

### Reviewer risk

- "Is the difference between guides biologically meaningful or just statistically significant?" -- Panel B (time course) and Panel D (allele precision) address biological relevance.
- "Are individual data points visible?" -- Box + strip overlay addresses this.

---

## Figure 3: Off-Target Analysis

- **Core conclusion**: Guide RNAs with the highest on-target efficiency do not necessarily have the highest off-target risk, and off-target profiling is essential for guide selection.
- **Archetype**: Quantitative grid (with one heatmap panel)
- **Journal size**: 1.5 column (120 mm / 4.7 inch wide)
- **Estimated height**: ~4.0 inch

### Panel map

| Panel | Content | Evidence role | Chart type | Size allocation |
|---|---|---|---|---|
| A | Genome-wide off-target sites identified by GUIDE-seq or CIRCLE-seq for each guide, ranked by read count | Hero -- shows off-target landscape | Heatmap (guides on x-axis, top off-target sites on y-axis, color = read count or cleavage score), viridis colormap | ~45% of width |
| B | Off-target cleavage frequency at top 5 predicted off-target sites per guide | Supporting -- quantifies risk at specific sites | Grouped bar chart (guide x off-target site), with threshold line at detection limit | ~35% of width |
| C | On-target vs. off-target ratio (specificity score) for each guide | Supporting -- synthesizes Panels A and B into a single decision metric | Scatter plot (x = on-target efficiency from Fig 2A, y = specificity score), one point per guide, labeled | ~30% of width |
| D | Sequence mismatch analysis: number of mismatches vs. off-target cleavage probability | Supporting -- shows the relationship between guide-target mismatch and off-target risk | Scatter + logistic regression curve with 95% CI band | ~30% of width |

### Evidence hierarchy

- **Hero**: Panel A -- the heatmap is the most information-dense panel and establishes whether off-targets are clustered or dispersed. This is the reviewer's primary target.
- **Supporting**: Panel B quantifies the top hits from Panel A. Panel C synthesizes efficiency and safety into one plot (the decision-relevant metric). Panel D provides the mechanistic explanation.

### Data sources

- Panels A, B: GUIDE-seq or CIRCLE-seq sequencing data, n = 2-3 biological replicates per guide
- Panel C: Derived (on-target from Figure 2A, off-target from Panel A/B)
- Panel D: In vitro cleavage assay data across mismatched oligonucleotide targets

### Statistics

- Panel A: No inferential test (heatmaps are descriptive); normalize read counts per million
- Panel B: Fisher's exact test or chi-squared for detection above background; declare detection threshold
- Panel C: Spearman correlation between on-target efficiency and specificity score
- Panel D: Logistic regression; report pseudo-R-squared and p-value

### Shared elements

- Guide RNA colors from visual vocabulary (but Panel A uses a sequential colormap for read counts -- the guide color appears as the column annotation bar above the heatmap)
- Figure 2A on-target values are directly referenced in Panel C

### Reviewer risk

- "Did you check off-targets genome-wide or only at predicted sites?" -- Panel A (GUIDE-seq/CIRCLE-seq is unbiased) addresses this.
- "Is off-target detection sensitive enough?" -- Declare detection limit as a threshold line in Panel B.

---

## Figure 4: Functional Outcomes

- **Core conclusion**: Differences in editing efficiency translate to differential functional outcomes, validating that guide RNA selection has downstream biological consequences.
- **Archetype**: Asymmetric mixed-modality figure
- **Journal size**: 1.5 column (120 mm / 4.7 inch wide)
- **Estimated height**: ~4.5 inch (five panels, needs vertical space)

### Panel map

| Panel | Content | Evidence role | Chart type | Size allocation |
|---|---|---|---|---|
| A | Target gene expression (mRNA level by RT-qPCR) for each guide vs. untreated control | Hero -- confirms gene knockdown correlates with editing efficiency | Box + strip plot (n >= 6 per guide), guides on x-axis, relative expression on y-axis, significance brackets vs. control | ~35% of width |
| B | Target protein level (Western blot quantification or flow cytometry MFI) for each guide | Supporting -- confirms protein-level effect | Strip plot with mean line and SEM error bars (n = 3-4) | ~30% of width |
| C | Correlation between editing efficiency (Fig 2A) and gene expression reduction (Panel A) | Supporting -- links molecular editing to functional outcome | Scatter plot with regression line and r/p values, one point per biological replicate, colored by guide | ~30% of width |
| D | Cell viability or proliferation assay for each guide (if relevant to the gene target) | Supporting -- shows phenotypic consequence | Bar chart with SEM error bars, guides on x-axis, viability % on y-axis, reference line at 100% | ~30% of width |
| E | Representative microscopy images (immunofluorescence or phenotype) for top guide vs. control | Validation -- visual confirmation of phenotype | Image panel pair (2 images side by side), with scale bar and merge/channel labels | ~25% of width |

### Evidence hierarchy

- **Hero**: Panel A -- gene expression reduction is the most direct functional readout and should correlate with Figure 2A editing efficiency. This is the panel that closes the argument loop.
- **Supporting**: Panel B confirms protein-level knockdown. Panel C is the mechanistic bridge (does editing efficiency predict functional outcome?). Panel D shows the phenotypic consequence. Panel E provides visual confirmation.
- **Visually quietest**: Panel E (images) -- small, minimal annotation, serves as qualitative confirmation.

### Data sources

- Panel A: RT-qPCR data, n >= 6 per guide, 2^-ddCt method
- Panel B: Western blot densitometry or flow cytometry, n = 3-4 per guide
- Panel C: Derived (Fig 2A indel % vs. Panel A relative expression)
- Panel D: MTT/CCK-8 or resazurin assay, n = 4-6 per guide
- Panel E: Representative IF or brightfield images, 1 per condition

### Statistics

- Panel A: One-way ANOVA with Dunnett's correction (each guide vs. untreated control); declare n, error type (SEM), test, correction
- Panel B: Descriptive (strip + mean); same test if formal comparison needed
- Panel C: Pearson correlation; report r and p-value
- Panel D: One-way ANOVA with Dunnett's correction vs. control
- Panel E: No inferential test (qualitative)

### Shared elements

- Guide RNA colors from visual vocabulary (consistent with Figures 1-3)
- Untreated control in gray (consistent with Figure 2)
- Figure 2A values directly used in Panel C

### Reviewer risk

- "Does editing efficiency actually matter for the phenotype?" -- Panel C (correlation) and Panel D (viability) directly address this.
- "Are you showing representative images or cherry-picked fields?" -- Declare "representative of n = 3 experiments" in caption.

---

## Cross-Figure Consistency Checklist

| Element | Convention | Figures affected |
|---|---|---|
| Guide RNA colors | gRNA-1 blue, gRNA-2 teal, gRNA-3 gold, gRNA-4 coral, gRNA-5 red | 1, 2, 3, 4 |
| Guide RNA markers | circle, square, triangle-up, diamond, triangle-down | 2, 3, 4 |
| Control color | Gray #8C8C8C | 2, 4 |
| Error type | SEM throughout | 2, 3, 4 |
| Sample size | Declared in legend or caption for every panel | 2, 3, 4 |
| Significance notation | * p < 0.05, ** p < 0.01 | 2, 4 |
| Statistical test | Mann-Whitney U with Bonferroni (pairwise); Kruskal-Wallis (overall); ANOVA with Dunnett's (vs. control) | 2, 3, 4 |
| Font | Helvetica / Arial, 6 pt labels, 5.5 pt ticks | 1, 2, 3, 4 |
| Panel label style | Uppercase bold A, B, C, D -- upper-left | 1, 2, 3, 4 |
| Spine style | Left + bottom only, no top/right spines | 2, 3, 4 |
| Legend style | Frameless, outside data area or in dedicated legend space | 2, 3, 4 |

---

## Figure Sizing Summary (Science Specifications)

| Figure | Width | Height | Rationale |
|---|---|---|---|
| Fig 1 | 4.7 inch (1.5 col) | ~4.0 inch | Schematic needs horizontal space; validation panels below |
| Fig 2 | 4.7 inch (1.5 col) | ~3.5 inch | Quantitative grid; box+strip is the widest panel |
| Fig 3 | 4.7 inch (1.5 col) | ~4.0 inch | Heatmap needs vertical space for off-target site labels |
| Fig 4 | 4.7 inch (1.5 col) | ~4.5 inch | Five panels, mixed modalities; tallest figure |

All figures use 1.5-column width (120 mm / 4.7 inch) because Science's single column (2.2 inch) is too narrow for the data density required. The 1.5-column format is standard for primary Science figures with multiple panels.

---

## Execution Sequence

After plan approval, execute figures in this order:

1. **Figure 1** first -- establishes visual vocabulary (colors, fonts, panel labels, marker shapes). All subsequent figures reference this.
2. **Figure 2** second -- the hero figure of the manuscript; depends on Figure 1's visual vocabulary.
3. **Figure 3** third -- references Figure 2A on-target values in Panel C.
4. **Figure 4** last -- references both Figure 2A (editing efficiency) and Figure 3 (specificity); closes the argument loop.

Each figure follows the full 8-step workflow: contract -> profile data -> select chart -> configure style (Science preset) -> plot -> visual QA -> export (PDF + PNG at 300 DPI) -> write figure description.
