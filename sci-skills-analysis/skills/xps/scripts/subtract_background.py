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
    """
    Iterative Shirley background.

    Anchored at both region endpoints (S = I at E_high and E_low); curves
    based on the integrated peak area above the current background:

      S(E) = I(E_high) + (I(E_low) - I(E_high)) · ∫_{E_high}^{E} (I - S) dE'
                                              / ∫_{E_high}^{E_low} (I - S) dE'

    so S(E_high) = I(E_high) and S(E_low) = I(E_low). The integral runs from
    the high-BE end toward the low-BE end — i.e. along increasing index, since
    XPS data is stored high BE → low BE (i0 < i1 in index space).
    """
    import numpy as np

    x = np.array(energies, dtype=float)
    y = np.array(counts, dtype=float)

    # XPS data goes high BE → low BE; e_start should be the higher BE endpoint.
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

    i0, i1 = indices[0], indices[-1]  # i0 = high-BE end, i1 = low-BE end

    xr = x[i0:i1 + 1]
    yr = y[i0:i1 + 1]
    dx = np.abs(np.diff(xr))
    bg_reg = np.full_like(yr, yr[0])  # init at high-BE endpoint value

    for _ in range(100):
        above = np.maximum(yr - bg_reg, 0.0)
        # Cumulative trapezoidal integral from the high-BE end (index 0,
        # integral = 0) toward the low-BE end (integral = total peak area).
        trap = 0.5 * (above[:-1] + above[1:]) * dx
        integral = np.concatenate(([0.0], np.cumsum(trap)))
        total = integral[-1]
        if abs(total) < 1e-15:
            break  # nothing above background — peak absent, keep flat init

        new_bg = yr[0] + (yr[-1] - yr[0]) * integral / total
        delta = np.max(np.abs(new_bg - bg_reg))
        bg_reg = new_bg
        if delta < 1e-6:
            break

    # Full-length background: Shirley curve inside the region, held constant
    # at the high-BE endpoint value outside it (fitting is region-bounded).
    bg = np.full(len(x), yr[0])
    bg[i0:i1 + 1] = bg_reg
    return bg.tolist()


def _tougaard(energies: list[float], counts: list[float],
              e_start: float, e_end: float) -> list[float]:
    """
    Tougaard background via FFT convolution with universal cross-section.

    The Tougaard background is:

      B(E) ∝ ∫_{E}^{∞} I(E') · K(E' - E) dE'

    where the universal cross-section kernel is:

      K(T) = B·T / (C + T²)²

    Uses B=2866 eV², C=1643 eV² (Tougaard universal parameters).
    Convolution via FFT for O(N log N) performance; scaling to endpoints.
    """
    import numpy as np
    from scipy.signal import fftconvolve

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

    B, C = 2866.0, 1643.0

    # Build energy loss grid for convolution
    # XPS convention: x is binding energy, high→low
    # Kinetic energy loss T = E' - E where E' > E (lower BE = higher KE)
    # On our reversed x-axis: T = x[j] - x[i] for j > i (x[j] < x[i], meaning higher KE)
    # We work on the kinetic energy scale: KE = hν - BE
    # T = KE' - KE = (hν - x') - (hν - x) = x - x' for higher KE (x' < x)
    # So T = x[higher_ke] - x[lower_ke] is positive when we think of x reversed

    dx = np.median(np.abs(np.diff(x)))  # uniform step size

    # Energy loss grid: 0 to full range, at data step size
    T_max = abs(max(x) - min(x))
    n_T = len(x)
    T = np.linspace(0, T_max, n_T)

    # Universal cross-section kernel
    kernel = B * T / (C + T**2)**2
    kernel[0] = 0.0  # K(0) = 0

    # Convolve spectrum (reversed so high KE = low BE is first) with kernel
    # We need ∫ I(E+T) · K(T) dT  for fixed E, integrating T from 0 to ∞
    # In practice: reverse energy axis, convolve, reverse back
    y_rev = y[i0:i1+1][::-1]  # now in KE order (low→high)
    bg_rev = fftconvolve(y_rev, kernel[:len(y_rev)], mode='full')[:len(y_rev)] * dx

    # Normalize: scale so B(E₀) = I(E₀) at high-BE endpoint
    bg_region = bg_rev[::-1]  # back to BE order (high→low)

    # Match the high-BE endpoint
    if abs(bg_region[0]) > 1e-15:
        bg_region = bg_region * (y[i0] / bg_region[0])

    # Fill into full array
    bg = np.full(len(x), y[i0])
    bg[i0:i1+1] = bg_region

    # Linear taper outside fitting region to data values
    if i1 + 1 < len(x):
        bg[i1+1:] = y[i1+1:]
    if i0 > 0:
        bg[:i0] = y[:i0]

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

    bg = np.interp(x, [x[i_start], x[i_end]], [y[i_start], y[i_end]])
    # Outside the region, hold constant
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
