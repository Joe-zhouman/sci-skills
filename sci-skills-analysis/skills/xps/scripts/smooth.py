#!/usr/bin/env python3
"""
Optional smoothing of XPS data before fitting.

Smoothing is a narrative choice — it suppresses noise that might otherwise
produce spurious "peaks," but over-smoothing can erase real features.
The window size determines how aggressive the smoothing is.

Methods:
  savgol  — Savitzky-Golay filter (default; preserves peak shapes well)
  moving  — Simple moving average
"""

import sys
import json
import argparse
from _cli import eprint, write_output, add_format_arg, load_json


def smooth_savgol(y: list[float], window: int, order: int) -> list[float]:
    """Savitzky-Golay smoothing filter."""
    from scipy.signal import savgol_filter
    # Window must be odd
    if window % 2 == 0:
        window += 1
    if window < order + 1:
        eprint({
            "type": "validation_error", "subtype": "invalid_params",
            "param": "--window",
            "message": f"window ({window}) must be > order ({order})",
            "hint": "increase --window or reduce --order"
        })
        sys.exit(1)
    return savgol_filter(y, window, order).tolist()


def smooth_moving(y: list[float], window: int) -> list[float]:
    """Simple moving average smoothing."""
    import numpy as np
    arr = np.array(y)
    kernel = np.ones(window) / window
    smoothed = np.convolve(arr, kernel, mode="same")
    # Fix edges: keep original values at boundaries
    half = window // 2
    smoothed[:half] = arr[:half]
    smoothed[-half:] = arr[-half:]
    return smoothed.tolist()


def main():
    parser = argparse.ArgumentParser(
        description="Optional XPS data smoothing before fitting"
    )
    parser.add_argument("--data", "-d", required=True,
                        help="path to input JSON")
    parser.add_argument("--method", "-m", choices=["savgol", "moving"],
                        default="savgol",
                        help="smoothing method (default: savgol)")
    parser.add_argument("--window", "-w", type=int, default=5,
                        help="window size — larger = more aggressive (default: 5)")
    parser.add_argument("--order", type=int, default=2,
                        help="polynomial order for savgol (default: 2)")
    parser.add_argument("--out", "-o", default=None,
                        help="write result to file instead of stdout")
    add_format_arg(parser)

    args = parser.parse_args()

    data = load_json(args.data, "--data")

    counts = data["counts"]

    if args.method == "savgol":
        smoothed = smooth_savgol(counts, args.window, args.order)
    else:
        smoothed = smooth_moving(counts, args.window)

    meta = dict(data.get("metadata", {}))
    meta["smoothing"] = {
        "method": args.method,
        "window": args.window,
    }
    if args.method == "savgol":
        meta["smoothing"]["order"] = args.order

    result = {
        "energies": data["energies"],
        "counts": smoothed,
        "counts_raw": counts,
        "metadata": meta,
    }

    if args.out:
        with open(args.out, "w") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Saved to {args.out}", file=sys.stderr)
    else:
        write_output(result, args.format)


if __name__ == "__main__":
    main()
