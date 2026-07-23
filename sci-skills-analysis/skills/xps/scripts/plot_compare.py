#!/usr/bin/env python3
"""
XPS comparison plot — the narrative tool.

Stack two (or more) fitted spectra vertically with offset, matching the style
of publication XPS comparison figures. Same element, different samples/conditions.

Design (matches the user's reference image):
  - Spectra stacked vertically, offset in y for visual separation
  - Raw data: dotted points
  - Component peaks: filled with alpha, consistent colors across panels
  - Envelope: solid dark line
  - Species labels: colored text + arrow pointing to peak
  - No y-axis ticks (offset comparison — absolute intensity doesn't matter, ratios do)
  - Shared x-axis, BE high→low
  - Sample labels on the right side of each panel

This is THE narrative output. The eye immediately sees which component dominates
in which sample — the whole point of the comparison.
"""

import sys, json, argparse
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from _cli import eprint, add_format_arg, load_json
from _plot import draw_spectrum, build_color_map, save_both


def plot_compare(spectra: list[dict], out_path: str,
                 title: str | None = None, xlabel: str = "Binding Energy (eV)"):
    """
    spectra: list of dicts, each with:
      - fit_result: path to fit JSON, or the loaded dict
      - label: sample name (e.g. "Si-MO", "Bare Si")
      - data: (optional) path to bg JSON for raw counts
    """
    # Load all
    loaded = []
    all_species = []
    for i, spec in enumerate(spectra):
        fit = spec["fit_result"]
        if isinstance(fit, str):
            fit = load_json(fit, "-f")
        data = spec.get("data")
        if isinstance(data, str):
            data = load_json(data, "-d")

        result = {
            "label": spec.get("label", f"Sample {i+1}"),
            "energies": np.array(fit["energies"]),
            "envelope": np.array(fit["envelope"]),
            "peaks": fit["peaks"],
            "components": fit.get("components", {}),
            "bg": np.array(fit["background"]) if fit.get("background") else None,
        }
        # Load raw data: prefer data JSON, fallback to fit JSON
        if data:
            result["counts_raw"] = np.array(data.get("counts", data.get("counts_raw", [])))
            if data.get("background") and result.get("bg") is None:
                result["bg"] = np.array(data["background"])
        if "counts_raw" not in result and "counts_raw" in fit:
            result["counts_raw"] = np.array(fit["counts_raw"])

        for pk in result["peaks"]:
            if pk["label"] not in all_species:
                all_species.append(pk["label"])

        loaded.append(result)

    color_map = build_color_map(all_species)
    n = len(loaded)

    fig = plt.figure(figsize=(7, 2.2 * n))
    gs = fig.add_gridspec(n, 1, hspace=0.15)

    for idx, spec in enumerate(loaded):
        ax = fig.add_subplot(gs[idx])

        # Shared spectrum stack — color_map keeps species colors consistent across panels.
        draw_spectrum(ax, spec["energies"], spec.get("counts_raw"), spec["bg"],
                      spec["envelope"], spec["peaks"], spec["components"],
                      color_map=color_map)

        # Sample label on the right
        ax.text(0.98, 0.92, spec["label"], transform=ax.transAxes,
                fontsize=10, fontweight="bold", ha="right", va="top",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                          edgecolor="0.7", alpha=0.85))

        ax.set_xlim(max(spec["energies"]), min(spec["energies"]))
        ax.set_ylabel("Intensity", fontsize=8)
        ax.tick_params(labelsize=7)
        # Remove y ticks for offset comparison
        ax.set_yticks([])

        if idx < n - 1:
            ax.tick_params(labelbottom=False)
        else:
            ax.set_xlabel(xlabel, fontsize=9)

    if title:
        fig.suptitle(title, fontsize=12, y=0.995, fontweight="bold")

    fig.tight_layout(pad=0.5)
    base = out_path.rsplit(".", 1)[0] if "." in out_path else out_path
    save_both(fig, base)
    plt.close(fig)

    # Return fit summaries for terminal printing
    summaries = []
    for spec in loaded:
        summaries.append({
            "label": spec["label"],
            "peaks": [{
                "label": pk["label"],
                "center": pk["center"],
                "stderr": pk["center_stderr"],
                "fwhm": pk["fwhm_approx"],
            } for pk in spec["peaks"]],
        })
    return {"pdf": f"{base}.pdf", "png": f"{base}.png", "spectra": summaries}


def main():
    parser = argparse.ArgumentParser(
        description="XPS comparison plot — stacked spectra, offset, species labels"
    )
    parser.add_argument("--fit", "-f", nargs="+", required=True,
                        help="paths to fit result JSONs (one per spectrum)")
    parser.add_argument("--labels", "-l", nargs="+", default=None,
                        help="sample labels (one per fit, matching order)")
    parser.add_argument("--data", "-d", nargs="*", default=None,
                        help="paths to background JSONs (one per fit, matching order)")
    parser.add_argument("--out", "-o", required=True, help="output path (.png)")
    parser.add_argument("--title", "-t", default=None, help="figure title")
    parser.add_argument("--xlabel", default="Binding Energy (eV)")
    add_format_arg(parser)
    args = parser.parse_args()

    labels = args.labels or [f"Sample {i+1}" for i in range(len(args.fit))]
    data_paths = args.data or [None] * len(args.fit)

    if len(labels) != len(args.fit):
        eprint({"type": "cli_error", "message": "--labels count must match --fit count"})
        sys.exit(1)

    spectra = []
    for i, fp in enumerate(args.fit):
        spectra.append({
            "fit_result": fp,
            "label": labels[i],
            "data": data_paths[i] if i < len(data_paths) else None,
        })

    result = plot_compare(spectra, args.out, args.title, args.xlabel)

    if args.format == "json":
        json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        for s in result["spectra"]:
            print(f"\n--- {s['label']} ---")
            print(f"{'Species':<10} {'BE (eV)':<12} {'FWHM':<8} {'±stderr'}")
            print("-" * 42)
            for p in s["peaks"]:
                print(f"{p['label']:<10} {p['center']:<12.2f} {p['fwhm']:<8.2f} {p['stderr']:<.2f}")
        print(f"\nFigure: {result['pdf']}")


if __name__ == "__main__":
    main()
