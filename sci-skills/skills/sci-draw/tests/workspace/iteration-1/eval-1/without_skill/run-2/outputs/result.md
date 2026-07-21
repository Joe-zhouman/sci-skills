# Nature-Style Grouped Bar Chart - Result

## Task
Create a Nature-style grouped bar chart with error bars from CSV data containing 5 methods and 3 metrics (each with mean and std).

## Files Created

### 1. Data File: `data/results.csv`
CSV with columns: `method`, `metric1_mean`, `metric1_std`, `metric2_mean`, `metric2_std`, `metric3_mean`, `metric3_std`

| method   | metric1_mean | metric1_std | metric2_mean | metric2_std | metric3_mean | metric3_std |
|----------|-------------|-------------|-------------|-------------|-------------|-------------|
| Method_A | 0.85        | 0.03        | 0.82        | 0.04        | 0.90        | 0.02        |
| Method_B | 0.78        | 0.05        | 0.75        | 0.06        | 0.84        | 0.04        |
| Method_C | 0.92        | 0.02        | 0.89        | 0.03        | 0.95        | 0.01        |
| Method_D | 0.80        | 0.04        | 0.77        | 0.05        | 0.86        | 0.03        |
| Method_E | 0.88        | 0.03        | 0.85        | 0.04        | 0.92        | 0.02        |

### 2. Python Script: `create_nature_bar_chart.py`
Reads from `data/results.csv` and generates the chart. Key Nature formatting applied:

- **Font**: Arial / Helvetica, 7pt (Nature single-column standard)
- **Figure size**: 3.5 x 2.5 inches (Nature single column width)
- **Spines**: Top and right removed
- **Linewidth**: 0.5pt axes and ticks
- **Colors**: Nature-friendly palette (`#E64B35` red, `#4DBBD5` teal, `#00A087` green)
- **Error bars**: capsize=1.5, 0.5pt linewidth
- **Legend**: frameless, 3-column, positioned at top-left
- **Gridlines**: light horizontal only, below bars
- **PDF font type**: 42 (TrueType, editable in Illustrator)

### 3. Output Files
- `nature_grouped_bar_chart.pdf` - Vector format for publication
- `nature_grouped_bar_chart.png` - 300 DPI raster for review

## How to Run
```bash
python create_nature_bar_chart.py
```

Output will be saved to the `outputs/` directory alongside this script.
