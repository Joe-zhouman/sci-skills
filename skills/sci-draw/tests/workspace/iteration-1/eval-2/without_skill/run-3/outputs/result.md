# Bar Chart with Error Bars -- Science Paper

## Summary

Created a publication-quality bar chart showing mean +/- SEM for 3 groups (n=6 each),
formatted for Science journal single-column width (3.5 inches).

## Output Files

- **bar_chart.pdf** -- vector PDF, 300 dpi, suitable for journal submission
- **bar_chart.png** -- raster PNG, 300 dpi, suitable for drafts/reviews
- **bar_chart.py** -- self-contained Python script (requires numpy, matplotlib)

## Data (Example -- Replace with Your Actual Data)

| Group   | Mean  | SEM   | n  |
|---------|-------|-------|----|
| Group A | 4.47  | 0.18  | 6  |
| Group B | 6.08  | 0.12  | 6  |
| Group C | 3.53  | 0.09  | 6  |

## Formatting Details

- **Figure size:** 3.5 x 2.5 inches (Science single-column)
- **Font:** Arial / Helvetica / DejaVu Sans, 8 pt (labels), 7 pt (ticks)
- **Axis:** Classic style (no top/right spines), 0.5 pt lines
- **Bars:** #4C72B0 fill, black edge, 0.5 pt linewidth
- **Error bars:** SEM (std / sqrt(n)), 0.5 pt lines, capsize 3
- **Data points:** White filled circles with black edge, jittered, overlaid on bars
- **Resolution:** 300 dpi

## How to Customize

Edit `bar_chart.py` and replace the example data arrays (`group_A`, `group_B`, `group_C`)
with your actual measurements. Adjust `labels` for your group names and `ax.set_ylabel()`
for your measurement unit.
