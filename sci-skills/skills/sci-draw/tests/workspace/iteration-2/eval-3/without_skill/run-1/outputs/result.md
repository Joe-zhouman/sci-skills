# Figure Plan: CRISPR Gene Editing Efficiency Manuscript (Science)

## General Formatting Guidelines (Science Requirements)

- **Figure width**: Single column = 3.5 in; 1.5 column = 5.5 in; Full width = 7 in
- **Font**: Arial or Helvetica, 6-8 pt in final figures
- **Color palette**: Colorblind-friendly (e.g., Okabe-Ito or viridis). Avoid red-green contrasts.
- **Resolution**: 300 DPI minimum for raster; prefer vector (SVG/PDF/EPS)
- **Labels**: Lowercase bold letters (a, b, c...) for sub-panels, top-left corner
- **Statistical reporting**: Error bars = SD or SEM (define in legend); exact p-values on plots; n values in legends
- **Scale bars**: Required on all microscopy images

---

## Figure 1: Experimental Design Schematic and Validation

**Purpose**: Establish the experimental system, demonstrate that the CRISPR components are functional, and set up the rationale for the gRNA comparison.

**Layout**: 4 panels, full-width figure (7 x 5 in)

### Panel 1a -- Experimental Workflow Schematic
- **Content**: Schematic diagram of the overall experimental pipeline
  - Target gene locus with exon/intron structure and the target site highlighted
  - CRISPR-Cas9 RNP or plasmid delivery method depicted (e.g., electroporation, lipofection)
  - Cell type / model organism used
  - Downstream readouts: indel quantification (NGS), functional assays, off-target analysis
- **Style**: Clean vector illustration; use color-coded arrows for workflow steps
- **Dimensions**: 3.5 x 3.5 in (left half of figure)

### Panel 1b -- Cas9 Expression / Activity Validation
- **Content**: Western blot or flow cytometry confirming Cas9 protein expression at relevant timepoints post-delivery
- **Data type**: Representative blot image with quantification bar graph below, or FACS histograms
- **Controls**: Non-transfected (NT), transfection reagent only, Cas9-only (no gRNA)
- **Statistics**: n >= 3 biological replicates; paired test if appropriate
- **Dimensions**: 1.75 x 2.5 in

### Panel 1c -- gRNA Target Site Sequencing Validation
- **Content**: Sanger sequencing or targeted amplicon NGS confirming on-target cutting at the intended locus
  - T7E1 or Surveyor assay gel image showing cleavage bands, OR
  - Amplicon sequencing reads aligned to reference with indel spectrum plot
- **Controls**: Untreated (wild-type) sample
- **Dimensions**: 1.75 x 2.5 in

### Panel 1d -- Cell Viability Post-Transfection
- **Content**: Bar graph showing cell viability (e.g., MTT, CellTiter-Glo, or trypan blue exclusion) at 24-72 h post-delivery
- **Purpose**: Rule out cytotoxicity as a confounding variable for editing efficiency
- **Dimensions**: 1.75 x 2.5 in

### Design Rationale
The validation figure is essential for Science reviewers to confirm that any observed differences in editing efficiency across gRNAs are attributable to gRNA sequence properties, not delivery artifacts or cytotoxicity. Including cell viability data pre-empts a common reviewer concern.

---

## Figure 2: Editing Efficiency Comparison Across 5 Guide RNAs

**Purpose**: Present the core comparative dataset -- on-target editing efficiency for all 5 gRNAs, with sufficient depth to support mechanistic interpretation.

**Layout**: 6 panels, full-width figure (7 x 6 in)

### Panel 2a -- Indel Frequency Overview
- **Content**: Grouped bar graph comparing indel frequency (%) for all 5 gRNAs at the target locus
  - X-axis: gRNA identifiers (gRNA-1 through gRNA-5)
  - Y-axis: Indel frequency (%)
  - Sub-bars if multiple timepoints (e.g., 48 h, 72 h, 7 d)
- **Statistics**: One-way ANOVA with Tukey post-hoc; show exact p-values for pairwise comparisons
- **Dimensions**: 3.5 x 2.5 in

### Panel 2b -- Indel Size Distribution
- **Content**: Histogram or ridgeline plot showing the distribution of indel sizes (bp) for each gRNA
- **Insight**: Reveal whether certain gRNAs produce predominantly small indels (1-5 bp) vs. large deletions
- **Dimensions**: 3.5 x 2.5 in

### Panel 2c -- Representative Sequencing Traces
- **Content**: Sanger sequencing chromatograms or IGV screenshots for the top-performing and lowest-performing gRNA
- **Purpose**: Visual evidence of editing; show frameshift vs. in-frame indels
- **Dimensions**: 3.5 x 2 in

### Panel 2d -- Allele Frequency Spectrum
- **Content**: Stacked bar or pie charts showing the proportion of:
  - Wild-type (unedited) alleles
  - Frameshift indels (likely knockout)
  - In-frame indels (may retain partial function)
  - Large deletions / complex rearrangements
- **Dimensions**: 3.5 x 2 in

### Panel 2e -- Editing Efficiency vs. gRNA Design Parameters
- **Content**: Scatter plots correlating editing efficiency with:
  - GC content (%)
  - Predicted off-target score (e.g., MIT score, CFD score)
  - Chromatin accessibility (ATAC-seq signal at target site, if available)
- **Dimensions**: 3.5 x 2 in

### Panel 2f -- Dose-Response for Top gRNA
- **Content**: Dose-response curve for the best-performing gRNA, varying Cas9:gRNA ratio or total RNP amount
- **Purpose**: Demonstrate saturation and identify optimal conditions
- **Dimensions**: 3.5 x 2 in

### Design Rationale
Science expects mechanistic depth, not just a single bar chart. The indel spectrum and allele frequency data provide insight into the biological consequences of each gRNA, while the correlation with design parameters adds predictive value that elevates the work beyond a simple screen.

---

## Figure 3: Off-Target Analysis

**Purpose**: Demonstrate specificity of editing and assess the risk profile of each gRNA -- a critical concern for therapeutic and research applications.

**Layout**: 5 panels, full-width figure (7 x 6 in)

### Panel 3a -- Predicted Off-Target Sites Overview
- **Content**: Genome browser-style view or table showing:
  - Top 10-20 predicted off-target sites (from Cas-OFFinder, CRISPOR, or GUIDE-seq data)
  - Number of mismatches and bulges relative to the on-target site
  - Genomic context (intergenic, intronic, exonic)
- **Dimensions**: 3.5 x 2 in

### Panel 3b -- Off-Target Editing Quantification (Amplicon Sequencing)
- **Content**: Heatmap showing indel frequencies at each predicted off-target site for all 5 gRNAs
  - Rows: Off-target sites (ranked by predicted score)
  - Columns: gRNA-1 through gRNA-5
  - Color scale: Indel frequency (log scale)
- **Controls**: Include on-target site for reference; untreated genomic DNA
- **Dimensions**: 3.5 x 3 in

### Panel 3c -- Specificity Index
- **Content**: Bar graph or dot plot showing the ratio of on-target to off-target editing (specificity index) for each gRNA
- **Metric**: On-target indel% / sum(top 5 off-target indel%)
- **Dimensions**: 1.75 x 2.5 in

### Panel 3d -- GUIDE-seq or DISCOVER-seq Genome-Wide Off-Target Map (if available)
- **Content**: Circos plot or Manhattan-style genome-wide view of off-target cleavage sites identified by unbiased methods
- **Purpose**: Unbiased detection of off-target sites not captured by prediction algorithms
- **Dimensions**: 3.5 x 3 in

### Panel 3e -- Off-Target Indel Characterization
- **Content**: For the top 3 most-abundant off-target sites:
  - Sequencing reads showing the nature of the off-target edit
  - Assessment of whether off-target edits are in-coding regions and could cause functional disruption
- **Dimensions**: 3.5 x 2 in

### Design Rationale
Off-target analysis is a make-or-break section for Science-level CRISPR studies. Combining predicted (computational) and empirical (GUIDE-seq/amplicon-seq) approaches demonstrates rigor. The specificity index provides a single interpretable metric for comparing gRNA safety profiles.

---

## Figure 4: Functional Outcomes of Editing

**Purpose**: Connect the molecular editing data to biological consequences -- the ultimate validation that editing efficiency translates to functional impact.

**Layout**: 5 panels, full-width figure (7 x 6 in)

### Panel 4a -- Target Protein Expression
- **Content**: Western blot or quantitative proteomics showing target protein levels for each gRNA
  - Include loading control and quantification bar graph
  - Show correlation with indel frequency from Figure 2
- **Dimensions**: 3.5 x 2.5 in

### Panel 4b -- mRNA Expression Analysis
- **Content**: RT-qPCR showing target mRNA levels, normalized to housekeeping genes
  - May reveal nonsense-mediated decay (NMD) for frameshift alleles
  - Include splice-site gRNAs if applicable
- **Dimensions**: 1.75 x 2.5 in

### Panel 4c -- Phenotypic Readout (Cell-Based Assay)
- **Content**: Functional assay appropriate to the target gene, e.g.:
  - Cell proliferation/viability assay if targeting an oncogene
  - Reporter gene assay if targeting a transcription factor
  - Electrophysiology if targeting an ion channel
  - Flow cytometry for surface markers
- **Dimensions**: 3.5 x 2.5 in

### Panel 4d -- Editing Efficiency vs. Functional Outcome Correlation
- **Content**: Scatter plot with regression line showing the relationship between indel frequency (x-axis) and functional readout (y-axis) across all 5 gRNAs
- **Statistics**: R-squared, Pearson or Spearman correlation
- **Purpose**: Demonstrate whether higher editing efficiency reliably translates to stronger functional effects
- **Dimensions**: 1.75 x 2.5 in

### Panel 4e -- Clonal Analysis (Optional, High Impact)
- **Content**: If clonal lines were derived:
  - Sequencing of individual alleles in clonal populations
  - Functional comparison of homozygous knockout vs. heterozygous vs. compound heterozygous clones
- **Dimensions**: 3.5 x 2.5 in

### Design Rationale
Science requires that editing data be connected to meaningful biology. The protein expression and phenotypic data close the loop between CRISPR cutting and functional consequence. The correlation plot (4d) is particularly valuable -- it tests whether editing efficiency is actually a useful predictor of experimental outcome, which has broad implications for the CRISPR field.

---

## Summary Table

| Figure | Panels | Key Message | Width |
|--------|--------|-------------|-------|
| Fig 1 | 4 (a-d) | System is validated; CRISPR components delivered and active | Full (7 in) |
| Fig 2 | 6 (a-f) | 5 gRNAs compared; indel spectra, design correlations | Full (7 in) |
| Fig 3 | 5 (a-e) | Off-target profiled by prediction + empirical methods | Full (7 in) |
| Fig 4 | 5 (a-e) | Editing translates to protein loss and functional change | Full (7 in) |

**Total panels**: 20 across 4 figures

---

## Supplementary Figures (Recommended)

- **Figure S1**: gRNA sequences, target coordinates, and predicted scores for all 5 gRNAs
- **Figure S2**: Full off-target amplicon sequencing data for all predicted sites
- **Figure S3**: Time-course editing kinetics for all 5 gRNAs
- **Figure S4**: Additional phenotypic assays or in vivo data (if applicable)

---

## Notes on Science-Specific Expectations

1. **Conciseness**: Science limits main text to 4-6 figures. This plan uses 4 figures with 20 panels, which is on the upper end. Consider moving panels 2e, 2f, 3d, and 4e to supplementary if space is tight.
2. **Impact**: The combination of systematic gRNA comparison + off-target profiling + functional validation tells a complete story suitable for Science's broad audience.
3. **Statistics**: Science requires transparent statistical reporting. Every comparison must have defined n, test name, and exact p-value.
4. **Data availability**: Raw sequencing data should be deposited (SRA/NCBI) and cited in the methods.
5. **Visual style**: Science prefers clean, minimalist figures. Avoid 3D effects, excessive gridlines, and decorative elements.
