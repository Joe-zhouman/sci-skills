# Nature-Style Grouped Bar Chart with Error Bars

## 1. Approach

The task is to produce a publication-quality grouped bar chart for a Nature journal paper, using data from a CSV with 5 methods and 3 metrics (each with mean and standard deviation columns).

**Workflow:**

1. Load and validate the CSV structure (method, metric1_mean, metric1_std, metric2_mean, metric2_std, metric3_mean, metric3_std).
2. Use matplotlib for full control over layout, tick labels, error bars, and export. Seaborn is avoided here because grouped bar charts with explicit error bars are cleaner to implement with raw matplotlib.
3. Apply Nature journal formatting conventions: single-column width (~89 mm / 3.5 in), Arial/Helvetica font, 5-7 pt axis labels, minimal axes (no top/right spines), and a restrained color palette.
4. Export as both vector PDF (for submission) and high-DPI PNG (for preview).

**Design choices:**

- Grouped bars: 3 metrics side-by-side within each method group, with thin black error bars (capsize 3 pt).
- Colors: A colorblind-safe palette (e.g., Nature's typical muted blues/oranges/greens).
- Legend: placed above the plot or to the right, outside the plotting area, to avoid occluding data.
- No gridlines on the y-axis behind bars (Nature style is clean); optional light horizontal gridlines behind bars if the editor prefers.

---

## 2. Python Script

```python
#!/usr/bin/env python3
"""
Nature-style grouped bar chart with error bars.

Expected CSV format:
    method, metric1_mean, metric1_std, metric2_mean, metric2_std, metric3_mean, metric3_std
    MethodA, 0.85, 0.03, 0.72, 0.04, 0.91, 0.02
    MethodB, 0.78, 0.05, 0.68, 0.03, 0.88, 0.04
    ...

Output:
    - grouped_bar_chart.pdf  (vector, submission-ready)
    - grouped_bar_chart.png  (300 DPI preview)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from pathlib import Path

# ---------------------------------------------------------------------------
# 1. Nature journal formatting
# ---------------------------------------------------------------------------

def apply_nature_style():
    """Configure matplotlib rcParams for Nature publication standards."""
    mpl.rcParams.update({
        # Font: Nature uses Helvetica/Arial; fall back to DejaVu Sans if unavailable
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 7,                    # base font size in pt
        "axes.labelsize": 7,               # axis labels
        "axes.titlesize": 8,               # subplot title
        "xtick.labelsize": 6,              # x-axis tick labels
        "ytick.labelsize": 6,              # y-axis tick labels
        "legend.fontsize": 6,              # legend text

        # Axes
        "axes.linewidth": 0.6,             # spine thickness
        "axes.spines.top": False,          # remove top spine
        "axes.spines.right": False,        # remove right spine
        "axes.edgecolor": "black",
        "axes.labelcolor": "black",

        # Ticks
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "xtick.major.size": 3,
        "ytick.major.size": 3,
        "xtick.direction": "out",
        "ytick.direction": "out",
        "xtick.color": "black",
        "ytick.color": "black",

        # Legend
        "legend.frameon": False,
        "legend.borderaxespad": 0.5,

        # Figure
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.05,

        # Grid (off by default for Nature)
        "axes.grid": False,
    })


# ---------------------------------------------------------------------------
# 2. Load and validate data
# ---------------------------------------------------------------------------

def load_data(csv_path: str) -> pd.DataFrame:
    """Load CSV and validate expected columns."""
    df = pd.read_csv(csv_path)

    # Derive metric names from columns
    metric_names = []
    for col in df.columns:
        if col.endswith("_mean"):
            metric_names.append(col.replace("_mean", ""))

    if len(metric_names) != 3:
        raise ValueError(
            f"Expected 3 metrics (mean columns), found {len(metric_names)}: {metric_names}"
        )

    # Validate that corresponding _std columns exist
    for m in metric_names:
        if f"{m}_std" not in df.columns:
            raise ValueError(f"Missing std column for metric '{m}': expected '{m}_std'")

    return df, metric_names


# ---------------------------------------------------------------------------
# 3. Color palette (colorblind-safe, Nature-compatible)
# ---------------------------------------------------------------------------

# Muted palette inspired by Nature/Science figures
NATURE_COLORS = [
    "#4C72B0",   # steel blue
    "#DD8452",   # muted orange
    "#55A868",   # sage green
    "#C44E52",   # muted red (unused here, but available)
    "#8172B3",   # muted purple (unused here)
]


# ---------------------------------------------------------------------------
# 4. Create the grouped bar chart
# ---------------------------------------------------------------------------

def create_grouped_bar_chart(
    df: pd.DataFrame,
    metric_names: list,
    output_dir: str = ".",
    figure_width_mm: float = 89,   # Nature single-column width
    figure_height_mm: float = 75,  # reasonable aspect ratio
):
    """
    Generate a Nature-style grouped bar chart.

    Parameters
    ----------
    df : DataFrame with columns [method, <metric>_mean, <metric>_std, ...]
    metric_names : list of metric name strings (without _mean/_std suffix)
    output_dir : directory for saved figures
    figure_width_mm : figure width in mm (Nature single column = 89 mm)
    figure_height_mm : figure height in mm
    """
    methods = df["method"].tolist()
    n_methods = len(methods)
    n_metrics = len(metric_names)

    # Convert mm to inches for matplotlib
    width_in = figure_width_mm / 25.4
    height_in = figure_height_mm / 25.4

    # Bar layout parameters
    bar_width = 0.22          # width of each individual bar
    group_gap = 0.15          # extra gap between method groups
    group_width = n_metrics * bar_width + group_gap

    # X positions for each method group
    x_group = np.arange(n_methods) * group_width

    # Create figure and axes
    fig, ax = plt.subplots(figsize=(width_in, height_in))

    # Plot each metric as a set of grouped bars
    for i, metric in enumerate(metric_names):
        means = df[f"{metric}_mean"].values
        stds = df[f"{metric}_std"].values

        # Offset bars within each group
        x_bars = x_group + i * bar_width

        ax.bar(
            x_bars,
            means,
            width=bar_width,
            yerr=stds,
            capsize=3,                    # error bar cap width (pt)
            error_kw={
                "linewidth": 0.6,
                "ecolor": "black",
                "capthick": 0.6,
            },
            color=NATURE_COLORS[i % len(NATURE_COLORS)],
            edgecolor="black",
            linewidth=0.4,
            label=metric.replace("_", " ").title(),
            zorder=3,                     # bars above gridlines
        )

    # X-axis: method labels centered under each group
    x_tick_positions = x_group + (n_metrics - 1) * bar_width / 2
    ax.set_xticks(x_tick_positions)
    ax.set_xticklabels(methods, rotation=0, ha="center")

    # Y-axis
    ax.set_ylabel("Score")
    ax.set_ylim(bottom=0)

    # Add light horizontal gridlines behind bars (optional, some Nature papers use this)
    ax.yaxis.grid(True, linewidth=0.3, color="#CCCCCC", zorder=0)
    ax.set_axisbelow(True)

    # Legend above the plot
    ax.legend(
        loc="upper center",
        bbox_to_anchor=(0.5, 1.12),
        ncol=n_metrics,
        handlelength=1.5,
        handletextpad=0.4,
        columnspacing=1.0,
    )

    # Tight layout with padding
    plt.tight_layout()

    # Save outputs
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    pdf_path = out / "grouped_bar_chart.pdf"
    png_path = out / "grouped_bar_chart.png"

    fig.savefig(pdf_path, format="pdf")
    fig.savefig(png_path, format="png", dpi=300)
    plt.close(fig)

    print(f"Saved: {pdf_path}")
    print(f"Saved: {png_path}")

    return pdf_path, png_path


# ---------------------------------------------------------------------------
# 5. Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Nature-style grouped bar chart")
    parser.add_argument(
        "--csv",
        type=str,
        default="data/results.csv",
        help="Path to input CSV file",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="output",
        help="Directory for output figures",
    )
    args = parser.parse_args()

    # Apply Nature formatting
    apply_nature_style()

    # Load data
    df, metric_names = load_data(args.csv)
    print(f"Loaded {len(df)} methods, {len(metric_names)} metrics: {metric_names}")

    # Generate chart
    create_grouped_bar_chart(df, metric_names, output_dir=args.output_dir)
```

---

## 3. Journal Formatting Applied

| Element | Specification |
|---|---|
| **Figure width** | 89 mm (Nature single-column) or 183 mm (full-page, if needed) |
| **Font family** | Helvetica / Arial (sans-serif) |
| **Font size** | 7 pt base; 6 pt tick labels; 8 pt subplot title |
| **Axes** | Bottom and left spines only; no top/right spines |
| **Spine/tick width** | 0.6 pt |
| **Error bars** | Black, 0.6 pt line, capsize 3 pt |
| **Bar edges** | Black, 0.4 pt |
| **Color palette** | Colorblind-safe muted tones (steel blue, muted orange, sage green) |
| **Legend** | Above plot, no frame, horizontally arranged |
| **Grid** | Light horizontal gridlines (0.3 pt, #CCC) behind bars |
| **Resolution** | 300 DPI for raster; vector PDF for submission |

These settings match Nature's artwork guidelines (https://www.nature.com/nature/for-authors/final-submission) for line weight, font, and figure dimensions.

---

## 4. Export Format

| Format | Use Case | Details |
|---|---|---|
| **PDF** (vector) | Journal submission | Primary deliverable; scalable, editable in Illustrator |
| **PNG** (300 DPI) | Manuscript preview / supplementary | High-resolution raster for Word/LaTeX drafts |

The script produces both. PDF is the submission-ready format; PNG is for quick review and embedding in draft documents. If the journal requests TIFF, the script can be extended with `fig.savefig("output.tiff", format="tiff", dpi=300)`.
