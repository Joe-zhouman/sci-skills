#!/usr/bin/env python3
"""
Export fitted XPS results to CSV (like your MATLAB output) or structured JSON.

CSV format: x, y_raw, y1, y2, ..., yf
  - x:        Binding Energy
  - y_raw:    original counts
  - yN:       individual peak components (on top of background)
  - yf:       fitted envelope (on top of background)

This is the format your MATLAB script produced and what sci-draw can consume.
"""

import sys
import json
import argparse
import csv
from _cli import eprint, write_output, add_format_arg, load_json


def to_csv(fit_result: dict) -> str:
    """Convert fit result to CSV string matching MATLAB output format."""
    import numpy as np
    import io

    energies = np.array(fit_result["energies"])
    counts_raw = np.array(fit_result["counts_raw"])
    bg = np.array(fit_result["background"]) if fit_result.get("background") else np.zeros_like(energies)
    envelope = np.array(fit_result["envelope"])
    components = fit_result.get("components", {})
    peaks = fit_result["peaks"]

    buf = io.StringIO()
    writer = csv.writer(buf)

    # Header
    header = ["x", "y"]
    for pk in peaks:
        header.append(pk["prefix"].rstrip("_"))
    header.append("yf")
    writer.writerow(header)

    # Data rows
    for i in range(len(energies)):
        row = [f"{energies[i]:.6f}", f"{counts_raw[i]:.6f}"]
        for pk in peaks:
            prefix = pk["prefix"]
            if prefix in components:
                comp_val = float(components[prefix][i]) + float(bg[i])
                row.append(f"{comp_val:.6f}")
            else:
                row.append("")
        env_val = float(envelope[i]) + float(bg[i])
        row.append(f"{env_val:.6f}")
        writer.writerow(row)

    return buf.getvalue()


def to_structured_json(fit_result: dict) -> dict:
    """Export as structured JSON suitable for sci-draw consumption."""
    return {
        "region_label": fit_result.get("region_label", ""),
        "energies": fit_result["energies"],
        "counts_raw": fit_result["counts_raw"],
        "counts_subtracted": fit_result.get("counts_subtracted"),
        "background": fit_result.get("background"),
        "envelope": fit_result["envelope"],
        "residual": fit_result["residual"],
        "peaks": fit_result["peaks"],
        "fit_quality": fit_result["fit_quality"],
        "calibration": fit_result.get("metadata", {}).get("calibration", {}),
        "background_method": fit_result.get("metadata", {}).get("background", {}),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Export XPS fit results to CSV or structured JSON"
    )
    parser.add_argument("--fit", "-f", required=True,
                        help="path to fit result JSON (from fit_peaks.py)")
    parser.add_argument("--out", "-o", required=True,
                        help="output file path")
    parser.add_argument("--export-format", "-F", choices=["csv", "json"], default="csv",
                        help="export format (default: csv)")

    args = parser.parse_args()

    fit_result = load_json(args.fit, "--fit")

    if args.export_format == "csv":
        output = to_csv(fit_result)
        with open(args.out, "w") as f:
            f.write(output)
    else:
        output = to_structured_json(fit_result)
        with open(args.out, "w") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Saved to {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
