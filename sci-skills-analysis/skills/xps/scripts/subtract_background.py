#!/usr/bin/env python3
"""
Background subtraction for XPS spectra.

Methods:
  shirley    — Iterative Shirley-Sherwood background (default for XPS; good general-purpose)
  tougaard   — Tougaard universal cross-section background (most physical, needs cross-section data)
  linear     — Straight line between region endpoints (fast, for polymers/large-bandgap)
  polynomial — Polynomial fit to endpoints + exterior regions (your MATLAB method)

<HARD-GATE>The same background method MUST be used across all regions in one dataset.
Mixing methods makes quantitative comparisons across elements invalid.</HARD-GATE>
"""

import sys
import json
import argparse
import os
from _cli import eprint, die, write_output, add_format_arg, load_json


def _shirley(energies: list[float], counts: list[float],
             e_start: float, e_end: float) -> list[float]:
    """Shirley background via lmfitxps.

    Iterative S-curve anchored at both region endpoints. Computed only on the
    region slice; outside it the background is held constant at the high-BE
    endpoint value (fitting is region-bounded). XPS data is high→low BE
    (descending), which is exactly the axis orientation lmfitxps expects.
    """
    import numpy as np
    from lmfitxps.backgrounds import shirley_calculate

    x = np.array(energies, dtype=float)
    y = np.array(counts, dtype=float)

    if e_start < e_end:
        e_start, e_end = e_end, e_start

    mask = (x <= e_start) & (x >= e_end)
    indices = np.where(mask)[0]
    if len(indices) < 3:
        eprint({
            "type": "validation_error", "subtype": "region_too_small",
            "param": "--region",
            "message": f"only {len(indices)} points in region [{e_start}, {e_end}]",
            "hint": "widen the background region to include more data points on both sides"
        })
        sys.exit(1)

    i0, i1 = indices[0], indices[-1]
    xr = x[i0:i1 + 1]
    yr = y[i0:i1 + 1]

    # lmfitxps default maxit=10 is too low for many spectra; raise it.
    bg_reg = shirley_calculate(xr, yr, maxit=100)

    # Full-length: Shirley inside region, constant (high-BE value) outside.
    bg = np.full(len(x), float(yr[0]))
    bg[i0:i1 + 1] = bg_reg
    return bg.tolist()


def _tougaard(energies: list[float], counts: list[float],
              e_start: float, e_end: float) -> list[float]:
    """Tougaard background via lmfitxps (textbook 4-PIESCS, universal params).

    Anchors at the high-BE endpoint (index 0 of the descending region) by
    iteratively varying the B scaling parameter; the low-BE endpoint floats
    to whatever the cross-section convolution produces — this is the correct
    physical Tougaard, NOT a both-endpoint-anchored Shirley lookalike. B<0 in
    the result means the data is outside Tougaard's applicability (report it).
    """
    import numpy as np
    from lmfitxps.backgrounds import tougaard_calculate

    x = np.array(energies, dtype=float)
    y = np.array(counts, dtype=float)

    if e_start < e_end:
        e_start, e_end = e_end, e_start

    mask = (x <= e_start) & (x >= e_end)
    indices = np.where(mask)[0]
    if len(indices) < 3:
        eprint({
            "type": "validation_error", "subtype": "region_too_small",
            "param": "--region",
            "message": f"only {len(indices)} points in region [{e_start}, {e_end}]"
        })
        sys.exit(1)

    i0, i1 = indices[0], indices[-1]
    xr = x[i0:i1 + 1]
    yr = y[i0:i1 + 1]

    # tougaard_calculate returns (background_array, optimized_B).
    bg_reg, b_scale = tougaard_calculate(xr, yr, maxit=100)

    if b_scale < 0:
        eprint({
            "type": "fit_warning", "subtype": "tougaard_nonphysical_b",
            "message": f"Tougaard B = {b_scale:.1f} is negative — the data is "
                       f"outside Tougaard's applicability (rising low-BE tail, "
                       f"or region endpoints not in a true background). "
                       f"Result is unphysical; try Shirley or linear."
        })

    bg = np.full(len(x), float(yr[0]))
    bg[i0:i1 + 1] = bg_reg
    return bg.tolist()


def _linear(energies: list[float], counts: list[float],
            e_start: float, e_end: float) -> list[float]:
    """Linear background between two endpoints."""
    import numpy as np

    x = np.array(energies, dtype=float)
    y = np.array(counts, dtype=float)

    # Find closest points to endpoints
    i_start = np.argmin(np.abs(x - e_start))
    i_end = np.argmin(np.abs(x - e_end))

    # np.interp requires xp ascending. XPS data is high→low BE (descending),
    # so sort the two anchor points by energy before interpolating.
    xp = [x[i_start], x[i_end]]
    fp = [y[i_start], y[i_end]]
    order = np.argsort(xp)
    bg = np.interp(x, np.array(xp)[order], np.array(fp)[order])

    # Outside the region, hold constant at the nearer endpoint value
    if i_start < i_end:
        bg[:i_start] = y[i_start]
        bg[i_end:] = y[i_end]
    else:
        bg[:i_end] = y[i_end]
        bg[i_start:] = y[i_start]

    return bg.tolist()


def _polynomial(energies: list[float], counts: list[float],
                e_start: float, e_end: float, degree: int = 3) -> list[float]:
    """
    Polynomial baseline: fit a polynomial to the exterior regions
    (outside [e_start, e_end]) and interpolate across the peak region.

    This is the method from your MATLAB template.
    """
    import numpy as np

    x = np.array(energies, dtype=float)
    y = np.array(counts, dtype=float)

    if e_start < e_end:
        e_start, e_end = e_end, e_start

    # Exterior regions: x > e_start (high BE side) and x < e_end (low BE side)
    exterior = (x >= e_start) | (x <= e_end)
    x_ext = x[exterior]
    y_ext = y[exterior]

    if len(x_ext) < degree + 1:
        eprint({
            "type": "validation_error", "subtype": "too_few_exterior_points",
            "param": "--region",
            "message": f"only {len(x_ext)} exterior points for degree-{degree} polynomial",
            "hint": "widen the region or reduce --poly-degree"
        })
        sys.exit(1)

    try:
        coeffs = np.polyfit(x_ext, y_ext, degree)
    except np.linalg.LinAlgError as exc:
        die({
            "type": "numeric_error", "subtype": "polyfit_failed",
            "param": "--region",
            "message": f"polynomial fit failed: {exc}",
            "hint": "exterior points may be degenerate (duplicate x or collinear) — "
                    "widen --region or reduce --poly-degree"
        })
    bg = np.polyval(coeffs, x)

    return bg.tolist()


def main():
    parser = argparse.ArgumentParser(
        description="Subtract background from XPS spectrum"
    )
    parser.add_argument("--data", "-d", required=True,
                        help="path to input JSON ({energies, counts, metadata}, from calibrate.py or hand-written)")
    parser.add_argument("--method", "-m",
                        choices=["shirley", "tougaard", "linear", "polynomial"],
                        default="shirley",
                        help="background method (default: shirley)")
    parser.add_argument("--region", "-r", nargs=2, type=float, required=True,
                        metavar=("START", "END"),
                        help="energy range for background endpoints (eV)")
    parser.add_argument("--poly-degree", type=int, default=3,
                        help="polynomial degree for --method polynomial (default: 3)")
    parser.add_argument("--out", "-o", default=None,
                        help="write result to file instead of stdout")
    add_format_arg(parser)

    args = parser.parse_args()

    data = load_json(args.data, "--data")

    energies = data["energies"]
    counts = data["counts"]

    if args.method == "shirley":
        bg = _shirley(energies, counts, args.region[0], args.region[1])
    elif args.method == "tougaard":
        bg = _tougaard(energies, counts, args.region[0], args.region[1])
    elif args.method == "linear":
        bg = _linear(energies, counts, args.region[0], args.region[1])
    elif args.method == "polynomial":
        bg = _polynomial(energies, counts, args.region[0], args.region[1],
                         args.poly_degree)

    bg_array = __import__("numpy").array(bg)
    counts_array = __import__("numpy").array(counts)
    subtracted = (counts_array - bg_array).tolist()

    meta = dict(data.get("metadata", {}))
    meta["background"] = {
        "method": args.method,
        "region": [args.region[0], args.region[1]],
    }
    if args.method == "polynomial":
        meta["background"]["poly_degree"] = args.poly_degree

    result = {
        "energies": energies,
        "counts": counts,
        "counts_subtracted": subtracted,
        "background": bg,
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
