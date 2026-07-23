"""Shared XPS plotting primitive for plot_region / plot_compare / plot_multi_region.

All three plot scripts draw the same stack on an axis:
  raw data (dots) -> background (dashed) -> component peaks (filled) ->
  envelope (solid) -> species labels.

One style, hardcoded. Per-script layout (panel count, figsize, titles,
sample labels, legends) stays in the caller.
"""

import numpy as np

# Morandi palette (saturated base + alpha at fill time).
PEAK_COLORS = [
    "#C44E52", "#4C72B0", "#55A868", "#C48A3F",
    "#8172B2", "#64B4CD", "#CCB974", "#8C8C8C",
]

# Components below this fraction of the envelope max are not labeled.
_LABEL_THRESHOLD = 0.08


def draw_spectrum(ax, energies, counts_raw, bg, envelope, peaks, components,
                  color_map=None):
    """Draw the full XPS spectrum stack onto a single matplotlib Axes.

    color_map: optional {label: color} dict. If None, colors are assigned by
               peak index (positional). Pass one for cross-panel species
               consistency (plot_compare).
    """
    energies = np.asarray(energies)
    counts_raw = np.asarray(counts_raw)
    envelope = np.asarray(envelope)
    bg = np.asarray(bg) if bg is not None else None

    # Raw data
    if counts_raw is not None and len(counts_raw):
        ax.plot(energies, counts_raw, ".",
                color="0.35", markersize=2.5, alpha=0.6, zorder=1)

    # Background
    if bg is not None:
        ax.plot(energies, bg, "--", color="0.45", linewidth=0.7, zorder=2)

    # Component peaks (filled)
    for i, pk in enumerate(peaks):
        prefix = pk["prefix"]
        color = color_map[pk["label"]] if color_map else \
            PEAK_COLORS[i % len(PEAK_COLORS)]
        if prefix in components:
            comp_y = np.asarray(components[prefix])
            if bg is not None:
                comp_y = comp_y + bg
            baseline = bg if bg is not None else np.zeros_like(energies)
            ax.fill_between(energies, baseline, comp_y,
                            alpha=0.25, color=color, linewidth=0, zorder=3)
            ax.plot(energies, comp_y, color=color, linewidth=0.7, zorder=4)

    # Envelope
    env_plot = envelope + bg if bg is not None else envelope
    ax.plot(energies, env_plot, "-", color="k", linewidth=1.0, zorder=5)

    # Species labels at peak maxima
    env_max = np.max(env_plot)
    for i, pk in enumerate(peaks):
        prefix = pk["prefix"]
        color = color_map[pk["label"]] if color_map else \
            PEAK_COLORS[i % len(PEAK_COLORS)]
        if prefix not in components:
            continue
        comp_y = np.asarray(components[prefix])
        if bg is not None:
            comp_y = comp_y + bg
        above = comp_y - (bg if bg is not None else 0)
        if np.max(above) < _LABEL_THRESHOLD * env_max:
            continue
        center_idx = np.argmax(comp_y)
        cx, cy = energies[center_idx], comp_y[center_idx]
        ax.annotate(
            pk["label"],
            xy=(cx, cy), fontsize=9, color=color, fontweight="bold",
            ha="center", va="bottom",
            xytext=(0, 5), textcoords="offset points",
        )

    return env_plot


def build_color_map(all_labels: list[str]) -> dict[str, str]:
    """Assign consistent colors to species across panels (preserve order, dedupe)."""
    unique = list(dict.fromkeys(all_labels))
    return {s: PEAK_COLORS[i % len(PEAK_COLORS)] for i, s in enumerate(unique)}


def save_both(fig, out_path: str) -> str:
    """Save a figure to both PDF (vector) and PNG (bitmap), shared base name."""
    base = out_path.rsplit(".", 1)[0] if "." in out_path else out_path
    fig.savefig(f"{base}.pdf", dpi=150, bbox_inches="tight")
    fig.savefig(f"{base}.png", dpi=150, bbox_inches="tight")
    return f"{base}.pdf"
