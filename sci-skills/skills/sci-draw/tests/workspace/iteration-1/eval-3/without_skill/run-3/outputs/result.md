# Gene Expression Scatter Plot — Nature Methods Format

## Overview

This script generates a publication-ready scatter plot comparing two continuous gene expression variables (200 samples), colored by disease status (Healthy vs Disease). It follows Nature Methods formatting guidelines.

## Files

- `scatter_plot.py` — Python script (matplotlib + scipy)
- `scatter_expression.pdf` — Vector output for publication
- `scatter_expression.png` — Raster output (300 DPI) for review

## Nature Methods Formatting Applied

| Setting | Value | Rationale |
|---|---|---|
| Figure width | 89 mm (3.5 in) | Single-column width |
| Font family | Arial / Helvetica | Required sans-serif |
| Axis label size | 8 pt | Nature Methods spec |
| Tick label size | 6 pt | Nature Methods spec |
| Spine removal | Top & right off | Reduce chartjunk |
| Line width | 0.6 pt | Clean, thin lines |
| Export DPI | 300 | Print quality |
| Marker size | 12 pt² | Readable without overlap |
| Alpha | 0.7 | Show overlap regions |

## How to Run

```bash
pip install matplotlib numpy scipy
python scatter_plot.py
```

## Script Design Decisions

1. **Color palette** — Blue (#4472C4) for Healthy, Red (#C00000) for Disease. Color-blind friendly and high contrast on white background.

2. **Regression line** — Dashed gray overall trend line to show correlation direction without implying causation.

3. **Pearson r annotation** — Placed in bottom-right corner with r and P values, using 6 pt font per Nature Methods style.

4. **Legend** — Top-left, frameless, with slightly enlarged markers (scale 1.5x) for clarity.

5. **Simulated data** — 200 samples drawn from a bivariate normal distribution with moderate positive correlation (r ~ 0.45) to mimic typical gene co-expression patterns.

## Output

The script writes two files to the same directory:

- `scatter_expression.pdf` — Use this for submission (vector, scalable)
- `scatter_expression.png` — Use this for quick review or supplementary upload
