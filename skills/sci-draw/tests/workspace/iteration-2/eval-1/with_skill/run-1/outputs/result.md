# Figure 1 Plan — Nanoparticle Drug Delivery System

---

## Figure Contract

```
Core conclusion:
  Optimized nanoparticle formulation X achieves sustained drug release over 72 hours
  while maintaining biocompatibility at therapeutic concentrations, validating it as a
  viable drug delivery platform.

Figure archetype:
  asymmetric mixed-modality figure

Target journal/output:
  Nature Materials

Backend:
  Python (matplotlib + seaborn)

Final size:
  Double-column: 183 mm x 140 mm (7.2 inch x 5.5 inch)

Panel map:
  a: Nanoparticle size (hydrodynamic diameter) across 4 formulations
  b: Zeta potential across 4 formulations
  c: In vitro cumulative drug release curves over 72 hours (4 formulations)
  d: Cell viability at 3 concentrations (per formulation or lead formulation)

Evidence hierarchy:
  hero evidence:     panel c — release kinetics (directly defends sustained release claim)
  validation:        panels a, b — physicochemical characterization (establishes system identity)
  controls/robustness: panel d — cell viability (addresses biocompatibility concern)

Statistics needed:
  - Size & zeta: mean +/- SD, n >= 3 independent batches
  - Release: mean +/- SD, n >= 3 replicates per timepoint
  - Viability: mean +/- SD, n >= 6 wells; one-way ANOVA + Tukey post-hoc or Dunnett's test vs. control

Source data needed:
  - Formulation ID, hydrodynamic diameter (nm), PDI
  - Zeta potential (mV) per formulation
  - Cumulative release (%) at each timepoint (0, 1, 2, 4, 8, 12, 24, 48, 72 h) per formulation
  - Cell viability (%) at 3 concentrations per formulation, with untreated control

Image-integrity notes:
  - No image adjustments apply (all quantitative data plots)
  - All data points must be visible (overlay stripplot where n < 10)

Reviewer risk:
  - "Which formulation is the lead?" -- must be clear from visual hierarchy or annotation
  - "Is the release sustained or is it burst release?" -- curve shape must be legible, not compressed
  - "Is viability dose-dependent?" -- 3 concentrations must be clearly distinguishable
  - "What is n?" -- legend or caption must declare sample size and error type
```

---

## Panel Layout

### Architecture: 2 x 2 grid, hero panel allocated more visual weight

```
+-----------------------------------+-----------------------------------+
|                                   |                                   |
|   Panel a                         |   Panel b                         |
|   Nanoparticle size               |   Zeta potential                  |
|   (grouped bar, 4 formulations)   |   (grouped bar, 4 formulations)   |
|   --- validation ---              |   --- validation ---              |
|                                   |                                   |
+-----------------------------------+-----------------------------------+
|                                                             |
|   Panel c (HERO -- spans full width or dominant area)       |
|   In vitro release curves, 72 h                            |
|   (line + error band, 4 formulations)                       |
|   --- hero evidence ---                                     |
|                                                             |
+-------------------------------------------------------------+
|                                   |                           |
|   Panel d                         |   (shared legend /        |
|   Cell viability                  |    annotation area)       |
|   (grouped bar, 3 concentrations) |                           |
|   --- robustness ---              |                           |
+-----------------------------------+---------------------------+
```

**Layout rationale**: Panel c (release kinetics) is the hero -- it directly defends the sustained release claim. It gets the most horizontal space (full width of the figure) so the time axis is legible and the 4 curves are clearly distinguishable. Panels a and b are narrow validation panels stacked side-by-side above the hero. Panel d sits bottom-left with a compact legend area to its right.

**Alternative layout** (if hero panel is better served by 2x2 with enlarged bottom-right):

```
+------------------------+------------------------+
|  Panel a               |  Panel b               |
|  Size (nm)             |  Zeta potential (mV)   |
|  grouped bar            |  grouped bar            |
+------------------------+------------------------+
|  Panel d               |  Panel c               |
|  Cell viability        |  Release curves (HERO)  |
|  grouped bar            |  line + error band      |
+------------------------+------------------------+
```

This keeps all 4 panels in a clean grid but gives panel c the bottom-right position (natural reading endpoint, strongest visual weight in left-to-right/top-to-bottom scanning).

---

## Panel-by-Panel Specification

### Panel a: Nanoparticle Hydrodynamic Diameter

| Property | Value |
|----------|-------|
| Chart type | Grouped vertical bar + stripplot overlay |
| X-axis | Formulation (F1, F2, F3, F4) -- categorical |
| Y-axis | Hydrodynamic diameter (nm) |
| Error bars | SD, n = 3 independent batches |
| Color | Blue family (4 shades, light to dark across formulations) |
| Unique claim | "Formulations differ in particle size; the lead formulation is in the target range (e.g., 100-200 nm)" |
| Evidence role | Validation -- establishes physicochemical identity |
| Interception check | n=3 per group triggers P1 warning. Must overlay stripplot showing all 3 data points per bar. Mean bar alone is forbidden at n<10. |

**Annotation**: Dashed horizontal line at target size range boundary if clinically relevant. PDI values as secondary annotation below each bar if space permits, or in supplementary.

### Panel b: Zeta Potential

| Property | Value |
|----------|-------|
| Chart type | Grouped vertical bar + stripplot overlay |
| X-axis | Formulation (F1, F2, F3, F4) -- categorical |
| Y-axis | Zeta potential (mV) |
| Error bars | SD, n = 3 independent batches |
| Color | Same blue family as panel a (unified formulation identity) |
| Unique claim | "Surface charge is formulation-dependent and supports colloidal stability / cellular uptake" |
| Evidence role | Validation -- confirms surface chemistry design |
| Interception check | Same n=3 stripplot requirement. Y-axis should include 0 mV reference line. |

**Annotation**: Dashed horizontal line at 0 mV. If stability threshold is known (e.g., |zeta| > 30 mV), add a shaded region or reference line.

### Panel c: In Vitro Drug Release (HERO)

| Property | Value |
|----------|-------|
| Chart type | Line plot + error band (fill_between) |
| X-axis | Time (h) -- continuous, 0-72 h |
| Y-axis | Cumulative release (%) |
| Lines | 4 formulations, color + marker dual encoding |
| Error bands | SD or 95% CI (shade, alpha=0.15), n >= 3 replicates |
| Color | Same blue family as panels a, b (unified formulation identity) |
| Unique claim | "The lead formulation achieves sustained release over 72 h without burst release, outperforming other formulations" |
| Evidence role | HERO -- directly defends the core claim |
| Line styling | Linewidth 1.5-2 pt; markers at data timepoints (circle, square, triangle, diamond); marker size 6-8 pt |

**Annotation**:
- Direct-label each curve at the right edge (formulation name) rather than a separate legend -- saves space and avoids lookup.
- If burst release is a concern, annotate the 0-4 h region with a shaded box or arrow.
- Y-axis should start at 0%, end at 100% (or auto-tighten if max is well below 100%).

**Reviewer-risk mitigation**: The curve shape must clearly show sustained vs. burst release. If all 4 curves are similar, the figure's argument weakens -- in that case, highlight the lead formulation with a thicker line or distinct marker.

### Panel d: Cell Viability

| Property | Value |
|----------|-------|
| Chart type | Grouped vertical bar + stripplot overlay |
| X-axis | Concentration (3 levels: low, medium, high) -- categorical |
| Y-axis | Cell viability (%) |
| Bars | Grouped by formulation or single lead formulation at 3 concentrations |
| Error bars | SD, n >= 6 wells |
| Color | If grouped by formulation: same blue family. If single formulation: green (positive signal) |
| Unique claim | "The lead formulation maintains high cell viability (>80%) across therapeutic concentrations" |
| Evidence role | Robustness -- addresses biocompatibility / safety concern |

**Annotation**:
- Dashed horizontal line at 80% viability threshold (common acceptance cutoff).
- Significance brackets between groups if ANOVA is significant (* p<0.05, ** p<0.01).
- Untreated control bar included for reference.

**Interception check**: n=6+ per group. If n < 10, stripplot overlay is mandatory. If viability is near 100% for all groups, y-axis should be tightened (e.g., 70-110%) to show differences -- never compress 0-100%.

---

## Evidence Hierarchy Summary

| Panel | Claim defended | Role | Visual weight | Size allocation |
|-------|---------------|------|---------------|-----------------|
| c | Sustained release over 72 h | HERO | Highest | Full width or 2x area |
| a | Size tunability across formulations | Validation | Medium | Standard |
| b | Surface charge design | Validation | Medium | Standard |
| d | Biocompatibility at therapeutic doses | Robustness | Medium-low | Standard |

---

## Color and Style Strategy

**Unified visual vocabulary across all panels**:
- Formulations F1-F4 mapped to a single blue family (light to dark):
  - F1: `#B4C0E4` (baseline_soft)
  - F2: `#7884B4` (baseline_mid)
  - F3: `#484878` (baseline_dark)
  - F4: `#0F4D92` (blue_main)
- This ensures the same formulation has the same color in every panel -- reader never has to re-learn the mapping.
- For panel d (viability), if a single lead formulation is shown, use green (`#2E9E44`) to signal positive/biocompatible outcome.

**Redundant encoding** (colorblind safety):
- Line styles: solid, dashed, dash-dot, dotted for the 4 curves in panel c
- Markers: circle, square, triangle-up, diamond for the 4 curves
- In bar charts (panels a, b, d): hatch patterns as grayscale fallback

---

## Nature Materials Journal Specifications

| Spec | Value |
|------|-------|
| Journal | Nature Materials |
| Single-column width | 89 mm (3.5 inch) |
| Double-column width | 183 mm (7.2 inch) |
| Max height | 247 mm (9.7 inch) |
| Chosen size | 7.2 inch x 5.5 inch (double-column, fits 4 panels comfortably) |
| Font | Helvetica / Arial (sans-serif) |
| Font size (labels/ticks) | 7-9 pt (minimum 5 pt) |
| Font size (panel labels) | 9-10 pt, bold |
| Vector format | PDF (primary) + EPS |
| Raster format | PNG, 300 DPI (for preview) |
| Line width | 0.6 pt (data lines), 0.8 pt (axes/spines) |
| Color space | RGB, colorblind-safe |
| Panel labels | a, b, c, d (lowercase, bold, top-left) |
| DPI (raster) | 300 minimum; 600 for dense line plots |
| Font embedding | pdf.fonttype = 42 (TrueType, not Type 3) |

**Export command** (when plotting):
```python
from scripts.export_figure import export_figure
export_figure(
    fig,
    basename='figs/fig1',
    formats=['pdf', 'png'],
    size_inches=(7.2, 5.5),
    dpi=300,
    grayscale_preview=True,
)
```

---

## Reviewer Risk Assessment

| Risk | Mitigation |
|------|------------|
| "Show individual data points" (n=3-6 per group) | Stripplot overlay on all bar charts |
| "Is this burst or sustained release?" | Hero panel (c) with full 72 h time axis; annotate early timepoints |
| "What is the lead formulation?" | Thicker line / distinct marker in panel c; direct labels |
| "Viability threshold?" | Dashed line at 80% with clear legend annotation |
| "Statistical test and n?" | Declare in legend: error type, n, test, correction, symbol definitions |
| "Grayscale readability?" | export_figure with grayscale_preview=True; hatch patterns on bars |

---

## Figure Description (fig_description.md)

```markdown
# Figure 1 -- Nanoparticle characterization, release kinetics, and biocompatibility

## Core conclusion
The optimized nanoparticle formulation achieves sustained drug release over 72 hours
while maintaining cell viability above 80% at therapeutic concentrations, validating
it as a viable drug delivery platform.

## Data source
- File: [nanoparticle characterization data, release study data, cell viability data]
- Samples: 4 formulations, n >= 3 independent batches (characterization), n >= 3
  replicates per timepoint (release), n >= 6 wells (viability)
- Variables: hydrodynamic diameter (nm), zeta potential (mV), cumulative release (%),
  cell viability (%)

## Chart type & rationale
- Panel a: Grouped bar + stripplot -- categorical comparison of 4 formulations on
  continuous size variable; stripplot mandatory at n < 10
- Panel b: Grouped bar + stripplot -- same rationale for zeta potential
- Panel c: Line + error band -- time-series data (0-72 h); line appropriate because
  x-axis is continuous time
- Panel d: Grouped bar + stripplot -- categorical comparison of 3 concentration levels
  on continuous viability variable

## Statistical methods
- Test: one-way ANOVA with Tukey's post-hoc (or Dunnett's vs. control for viability)
- Correction: Tukey HSD for pairwise comparisons; Dunnett's for many-to-one
- Error bars: SD, n = 3 (characterization), n = 3 (release), n = 6 (viability)
- Significance: * p < 0.05, ** p < 0.01

## Key findings
- Formulations differ in hydrodynamic diameter (target: 100-200 nm range)
- Zeta potential indicates colloidal stability across formulations
- Lead formulation shows sustained release profile over 72 h without burst release
- Cell viability remains above 80% across all tested concentrations

## Journal specs
- Target: Nature Materials
- Size: double-column 7.2 inch x 5.5 inch
- Format: PDF (vector) + PNG (300 DPI preview)
- Font: Helvetica/Arial, 7-9 pt
```

---

## Execution Notes

When the user confirms this plan and provides actual data:

1. **Step 1** -- Profile data with `profile_data.py` to confirm column types, n per group, distributions, outliers.
2. **Step 2** -- Finalize chart selection based on data shape (confirm grouped bar is appropriate; if distributions are bimodal, switch to violin + stripplot).
3. **Step 3** -- Nature Materials specs are documented above.
4. **Step 4** -- `setup_style(journal='nature', lang='en')`.
5. **Step 5** -- Plot each panel independently, then combine with `GridSpec(2, 2, ...)`. Use `layout_tools.add_panel_labels(fig, style='nature')` for consistent label placement.
6. **Step 6** -- Visual QA: `audit_layout(fig)` + `render_preview(fig, ...)` + human-eye check.
7. **Step 7** -- Export PDF + PNG with grayscale preview.
8. **Step 8** -- Write `fig1_description.md` using the template above.
