#!/usr/bin/env python3
"""
Single XPS spectrum plot — flat, exploration / group-meeting quality.

Single panel only: raw data (dots) + background (dashed) + component peaks
(filled) + envelope (solid) + species labels. No residual — flat means error
is harder to scrutinize, which is exactly what you want for a narrative plot.

Use during the fitting loop and for group meetings.
For comparison (two samples stacked), use plot_compare.py.
"""

import sys, json, argparse, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from _cli import eprint, add_format_arg, load_json

PEAK_COLORS = [
    "#C44E52", "#4C72B0", "#55A868", "#C48A3F",
    "#8172B2", "#64B4CD", "#CCB974", "#8C8C8C",
]


def plot_region(fit_result: dict, out_path: str, title: str | None = None):
    energies = np.array(fit_result["energies"])
    counts_raw = np.array(fit_result["counts_raw"])
    bg = np.array(fit_result["background"]) if fit_result.get("background") else None
    envelope = np.array(fit_result["envelope"])
    peaks = fit_result["peaks"]
    components = fit_result.get("components", {})

    # Flat single panel — wide, not tall
    fig, ax = plt.subplots(figsize=(7, 2.8))

    # Raw data
    ax.plot(energies, counts_raw, ".",
            color="0.35", markersize=2.5, alpha=0.6, zorder=1)

    # Background
    if bg is not None:
        ax.plot(energies, bg, "--", color="0.45", linewidth=0.7, zorder=2)

    # Component peaks (filled)
    for i, pk in enumerate(peaks):
        prefix = pk["prefix"]
        color = PEAK_COLORS[i % len(PEAK_COLORS)]
        if prefix in components:
            comp_y = np.array(components[prefix])
            if bg is not None:
                comp_y = comp_y + bg
            baseline = bg if bg is not None else np.zeros_like(energies)
            ax.fill_between(energies, baseline, comp_y,
                            alpha=0.25, color=color, linewidth=0, zorder=3)
            ax.plot(energies, comp_y, color=color, linewidth=0.7, zorder=4)

    # Envelope
    env_plot = envelope + bg if bg is not None else envelope
    ax.plot(energies, env_plot, "k-", linewidth=1.0, zorder=5)

    # Species labels at peak maxima
    env_max = np.max(env_plot)
    for i, pk in enumerate(peaks):
        prefix = pk["prefix"]
        color = PEAK_COLORS[i % len(PEAK_COLORS)]
        if prefix in components:
            comp_y = np.array(components[prefix])
            if bg is not None:
                comp_y = comp_y + bg
            if np.max(comp_y - (bg if bg is not None else 0)) < 0.08 * env_max:
                continue
            center_idx = np.argmax(comp_y)
            cx, cy = energies[center_idx], comp_y[center_idx]
            ax.annotate(
                pk["label"],
                xy=(cx, cy), fontsize=9, color=color, fontweight="bold",
                ha="center", va="bottom",
                xytext=(0, 5), textcoords="offset points",
            )

    ax.set_ylabel("Intensity (counts)", fontsize=9)
    ax.set_xlabel("Binding Energy (eV)", fontsize=9)
    ax.set_xlim(max(energies), min(energies))
    ax.tick_params(labelsize=8)

    # Title with region + R²
    region = fit_result.get("region_label", "")
    r2 = fit_result["fit_quality"]["r_squared"]
    label = f"{region}  (R² = {r2:.4f})" if region else f"R² = {r2:.4f}"
    ax.set_title(label, fontsize=11, loc="left")

    fig.tight_layout(pad=0.3)

    base = out_path.rsplit(".", 1)[0] if "." in out_path else out_path
    fig.savefig(f"{base}.pdf", dpi=150, bbox_inches="tight")
    fig.savefig(f"{base}.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # Return fit summary for printing separately (not on the figure)
    return {
        "pdf": f"{base}.pdf",
        "png": f"{base}.png",
        "r_squared": fit_result["fit_quality"]["r_squared"],
        "peaks": [{
            "label": pk["label"],
            "center": pk["center"],
            "stderr": pk["center_stderr"],
            "fwhm": pk["fwhm_approx"],
            "amplitude": pk.get("amplitude", 0),
        } for pk in peaks],
    }


def main():
    parser = argparse.ArgumentParser(description="Single XPS region plot — flat, no residual")
    parser.add_argument("--data", "-d", help="background-subtracted JSON")
    parser.add_argument("--fit", "-f", required=True, help="fit result JSON")
    parser.add_argument("--out", "-o", required=True, help="output path (.png)")
    parser.add_argument("--title", "-t", default=None)
    add_format_arg(parser)
    args = parser.parse_args()

    fit_result = load_json(args.fit, "--fit")
    if args.data:
        d = load_json(args.data, "--data")
        fit_result.setdefault("counts_raw", d.get("counts"))
        fit_result.setdefault("background", d.get("background"))

    summary = plot_region(fit_result, args.out, args.title)

    if args.format == "json":
        # Structured output — agent reads this and presents to user
        json.dump(summary, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        # Human-readable fallback
        print(f"R² = {summary['r_squared']:.4f}")
        print(f"{'Species':<10} {'BE (eV)':<12} {'FWHM':<8} {'Amplitude':<10} {'±stderr'}")
        print("-" * 55)
        for p in summary["peaks"]:
            print(f"{p['label']:<10} {p['center']:<12.2f} {p['fwhm']:<8.2f} {p['amplitude']:<10.0f} {p['stderr']:<.2f}")
        print(f"\nFigure: {summary['pdf']}")


if __name__ == "__main__":
    main()
