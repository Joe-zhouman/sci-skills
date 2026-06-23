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
