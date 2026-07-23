#!/usr/bin/env python3
"""
Stack multiple fitted regions into one exploration figure.

Fixed template: vertical stack, shared x-axis (Binding Energy, high→low).
Useful for: Si 2p + N 1s + Li 1s side by side, or before/after comparisons.
"""

import sys
import json
import argparse
from _cli import eprint, add_format_arg, load_json
from _plot import draw_spectrum, save_both


def plot_multi_region(regions: list[dict], out_path: str,
                      title: str | None = None) -> str:
    """Render a vertical stack of fitted regions."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    n = len(regions)
    fig = plt.figure(figsize=(8, 2.5 * n))
    gs = fig.add_gridspec(n, 1, hspace=0.3)

    for idx, fit_result in enumerate(regions):
        ax = fig.add_subplot(gs[idx])

        energies = np.array(fit_result["energies"])
        counts_raw = np.array(fit_result.get("counts_raw", fit_result.get("counts_subtracted", [])))
        bg = np.array(fit_result["background"]) if fit_result.get("background") else None
        envelope = np.array(fit_result["envelope"])
        peaks = fit_result["peaks"]
        components = fit_result.get("components", {})

        draw_spectrum(ax, energies, counts_raw, bg, envelope, peaks, components)

        ax.set_xlim(max(energies), min(energies))
        ax.set_ylabel("Intensity")

        region_label = fit_result.get("region_label", f"Region {idx+1}")
        r2 = fit_result["fit_quality"]["r_squared"]
        ax.set_title(f"{region_label}  (R²={r2:.3f})", fontsize=10, loc="left")
        ax.tick_params(labelsize=8)

        # Only bottom panel gets x-label
        if idx == n - 1:
            ax.set_xlabel("Binding Energy (eV)")

    if title:
        fig.suptitle(title, fontsize=12, y=0.995)

    fig.tight_layout(pad=0.8)
    if title:
        fig.subplots_adjust(top=0.95)

    base = out_path.rsplit(".", 1)[0] if "." in out_path else out_path
    return save_both(fig, base)


def main():
    parser = argparse.ArgumentParser(
        description="Stack multiple fitted XPS regions vertically"
    )
    parser.add_argument("--regions", "-r", nargs="+", required=True,
                        help="paths to fit result JSON files")
    parser.add_argument("--out", "-o", required=True,
                        help="output image path (.png)")
    parser.add_argument("--title", "-t", default=None,
                        help="figure title")
    add_format_arg(parser)

    args = parser.parse_args()

    regions = []
    for path in args.regions:
        # Each file might contain one region or a merged result
        data = load_json(path, "-r")
        if "regions" in data:
            regions.extend(data["regions"])
        else:
            regions.append(data)

    path = plot_multi_region(regions, args.out, args.title)
    print(f"Saved to {path}", file=sys.stderr)


if __name__ == "__main__":
    main()
