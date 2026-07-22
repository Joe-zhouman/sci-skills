#!/usr/bin/env python3
"""
Automatic peak detection in XPS spectra — two-pass method.

Phase 1: peak detection on background-subtracted data
  - scipy.signal.find_peaks for automatic peak finding
  - scipy.signal.argrelextrema for local maxima

Phase 2: initial lmfit fit (like MATLAB's "first fit" in XPSFindPeaks.mlx)
  - Runs a fit with the detected peaks as starting points
  - Returns refined parameters as initial guesses for manual tuning

Phase 3 (optional): refined fit using Phase 2 results as starting points

This mirrors the MATLAB workflow: detect → first fit → use results as seeds → second fit.
BUT: this only provides CANDIDATES. The user must still decide which peaks to keep
and what constraints to apply — that's the narrative part.

Output: a peaks.json template ready for fit_peaks.py, with NIST annotations.
"""

import sys, json, argparse, os
import numpy as np
from _cli import eprint, write_output, add_format_arg, load_json


def _detect_peaks(energies: np.ndarray, counts_sub: np.ndarray,
                  prominence: float, distance: float,
                  min_fwhm: float, max_fwhm: float,
                  max_peaks: int) -> list[dict]:
    """Find peaks via local maxima detection."""
    from scipy.signal import find_peaks

    # Normalize for peak detection
    y = counts_sub - counts_sub.min()
    y = y / y.max()

    # prominence: fraction of full range
    prom = prominence
    dist = max(1, int(distance / np.median(np.abs(np.diff(energies)))))

    peaks_idx, props = find_peaks(y, prominence=prom, distance=dist)
    if len(peaks_idx) == 0:
        # Relax prominence
        peaks_idx, props = find_peaks(y, prominence=prom / 2, distance=dist)

    # If still nothing, try argrelextrema
    if len(peaks_idx) == 0:
        from scipy.signal import argrelextrema
        order = max(3, int(dist))
        peaks_idx = argrelextrema(y, np.greater, order=order)[0]

    # Sort by peak height descending, take top N
    peak_heights = y[peaks_idx]
    sort_idx = np.argsort(peak_heights)[::-1]
    peaks_idx = peaks_idx[sort_idx][:max_peaks]

    # Re-sort by energy for output
    peaks_idx = np.sort(peaks_idx)

    candidates = []
    # counts_sub is the raw background-subtracted intensity; use it for FWHM
    # (scipy.signal.find_peaks ran on the normalized y only to LOCATE peaks).
    cs = counts_sub
    base = cs.min()
    prominence_arr = props.get('prominences', [])

    for k, idx in enumerate(peaks_idx):
        center = float(energies[idx])
        amplitude = float(cs[idx])

        # FWHM via half-max crossings on the raw (un-normalized) counts, so
        # the height and threshold are in the same units.
        half = base + (cs[idx] - base) * 0.5
        left = idx
        while left > 0 and cs[left] > half:
            left -= 1
        right = idx
        while right < len(cs) - 1 and cs[right] > half:
            right += 1
        fwhm_est = abs(energies[right] - energies[left])
        sigma = max(0.2, min(fwhm_est / 2.355, max_fwhm / 2.355))

        prom = float(prominence_arr[k]) if k < len(prominence_arr) else 0.0

        candidates.append({
            "center": center,
            "sigma": round(sigma, 3),
            "amplitude": round(amplitude, 1),
            "prominence": round(prom, 4),
        })

    return candidates


def _first_fit(energies: np.ndarray, counts_sub: np.ndarray,
               candidates: list[dict], peak_func: str) -> list[dict]:
    """
    Run an initial fit using detected peaks as starting points.
    Returns refined parameters — like MATLAB's 'first fit' step.
    """
    try:
        from lmfit.models import GaussianModel, PseudoVoigtModel, VoigtModel
    except ImportError:
        eprint({"type": "dependency_error", "message": "lmfit required", "hint": "conda install lmfit"})
        return candidates  # fallback to raw detection

    ModelClass = {"gaussian": GaussianModel, "pseudo_voigt": PseudoVoigtModel,
                  "voigt": VoigtModel}.get(peak_func, GaussianModel)

    # Build composite model
    params = None
    composite = None
    for i, c in enumerate(candidates):
        prefix = f"p{i}_"
        model = ModelClass(prefix=prefix)
        composite = model if composite is None else composite + model
        p = model.make_params()
        p[f"{prefix}center"].set(value=c["center"], min=c["center"] - 1.0, max=c["center"] + 1.0)
        p[f"{prefix}sigma"].set(value=c["sigma"], min=0.1, max=5.0)
        p[f"{prefix}amplitude"].set(value=c["amplitude"], min=0)
        if peak_func == "pseudo_voigt":
            p[f"{prefix}fraction"].set(value=0.5, min=0, max=1)
        params = p if params is None else params
        if params is not p:
            params.update(p)

    try:
        result = composite.fit(counts_sub, params, x=energies, method="leastsq")
    except Exception:
        return candidates

    refined = []
    for i, c in enumerate(candidates):
        prefix = f"p{i}_"
        refined.append({
            "center": round(float(result.params[f"{prefix}center"].value), 3),
            "sigma": round(float(result.params[f"{prefix}sigma"].value), 3),
            "amplitude": round(float(result.params[f"{prefix}amplitude"].value), 1),
        })
    return refined


def _place_evenly(x: np.ndarray, y: np.ndarray, n_peaks: int) -> list[dict]:
    """Place N peaks evenly across the data range (fallback when auto-detect fails)."""
    x_min, x_max = min(x), max(x)
    spacing = (x_max - x_min) / (n_peaks + 1)
    y_max = max(y)
    peaks = []
    for i in range(n_peaks):
        center = x_max - spacing * (i + 1)  # high BE first (left side)
        idx = np.argmin(np.abs(x - center))
        amplitude = float(y[idx])
        peaks.append({
            "center": round(float(center), 2),
            "sigma": round(spacing / 3.5, 3),
            "amplitude": round(amplitude, 1),
            "prominence": 0.0,
        })
    return peaks


def _place_from_nist(x: np.ndarray, y: np.ndarray, nist_positions: list[float]) -> list[dict]:
    """Place peaks at NIST-expected positions, estimating amplitude from data."""
    peaks = []
    for pos in nist_positions:
        idx = np.argmin(np.abs(x - pos))
        amplitude = float(y[idx]) if idx < len(y) else max(y) * 0.5
        peaks.append({
            "center": round(float(pos), 2),
            "sigma": 0.8,
            "amplitude": round(amplitude, 1),
            "prominence": 0.0,
        })
    return peaks


def find_peaks(data: dict, config: dict) -> dict:
    """
    Main entry: detect peaks → first fit → generate peaks.json template.

    config:
      - energy_range: [low, high] (eV)
      - max_peaks: max number of peaks to detect (default 8)
      - n_peaks: explicit peak count (overrides auto-detect; use for overlapping peaks)
      - nist_positions: list of BE values from NIST database to seed peak positions
      - prominence: peak prominence threshold, fraction of max (default 0.05)
      - distance: minimum distance between peaks in eV (default 0.5)
      - peak_function: gaussian / pseudo_voigt / voigt
      - region_label: string label
    """
    energies = np.array(data["energies"])
    counts_sub = np.array(data.get("counts_subtracted", data["counts"]))

    # Restrict to region
    region = config.get("energy_range")
    if region:
        r0, r1 = max(region), min(region)
        mask = (energies <= r0) & (energies >= r1)
    else:
        mask = np.ones(len(energies), dtype=bool)

    x = energies[mask]
    y = counts_sub[mask]

    max_peaks = config.get("max_peaks", 8)
    n_peaks = config.get("n_peaks")
    nist_positions = config.get("nist_positions")
    prominence = config.get("prominence", 0.05)
    distance = config.get("distance", 0.5)
    peak_func = config.get("peak_function", "gaussian")

    # Choose peak placement strategy
    if nist_positions:
        # User provided NIST positions — place peaks there
        candidates = _place_from_nist(x, y, nist_positions)
        detection_mode = "nist"
    elif n_peaks:
        # User specified peak count — place evenly, then let first fit adjust
        candidates = _place_evenly(x, y, n_peaks)
        detection_mode = "manual_count"
    else:
        # Auto-detect via find_peaks
        candidates = _detect_peaks(x, y, prominence, distance,
                                   min_fwhm=0.3, max_fwhm=5.0, max_peaks=max_peaks)
        detection_mode = "auto"

    # If auto-detect found only 1 peak but data looks like a multi-peak envelope,
    # suggest the user specify n_peaks manually
    if detection_mode == "auto" and len(candidates) <= 1 and max(y) > 100:
        # Warn but still try the first fit with the single peak
        pass

    # First fit
    if config.get("run_first_fit", True) and len(candidates) > 0:
        refined = _first_fit(x, y, candidates, peak_func)
    else:
        refined = candidates

    # Build peaks.json template
    peaks = []
    for c in refined:
        center = c["center"]
        sigma = c["sigma"]
        amplitude = c["amplitude"]
        peaks.append({
            "label": f"Peak@{center:.1f}",
            "center": round(center, 2),
            "center_range": [round(center - 0.8, 2), round(center + 0.8, 2)],
            "sigma": round(sigma, 3),
            "sigma_range": [max(0.1, round(sigma * 0.3, 3)), round(sigma * 2.5, 3)],
            "amplitude": round(amplitude, 1),
            "amplitude_range": [max(0, round(amplitude * 0.1, 1)), round(amplitude * 5, 1)],
        })

    return {
        "region_label": config.get("region_label", ""),
        "energy_range": region or [float(energies[0]), float(energies[-1])],
        "detection_mode": detection_mode,
        "peaks": peaks,
        "candidates_raw": [{
            "center": c["center"],
            "sigma": c["sigma"],
            "amplitude": c["amplitude"],
        } for c in candidates],
        "candidates_refined": refined != candidates,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Automatic XPS peak detection — find peaks, output peaks.json template"
    )
    parser.add_argument("--data", "-d", required=True,
                        help="path to background-subtracted JSON")
    parser.add_argument("--region", "-r", nargs=2, type=float, default=None,
                        metavar=("LOW", "HIGH"),
                        help="energy range to search (eV)")
    parser.add_argument("--max-peaks", type=int, default=8,
                        help="maximum number of peaks for auto-detect (default: 8)")
    parser.add_argument("--n-peaks", "-n", type=int, default=None,
                        help="explicit number of peaks — evenly spaced + first-fit adjust (for overlapping peaks)")
    parser.add_argument("--nist-positions", nargs="+", type=float, default=None,
                        help="NIST BE positions to seed peaks (from lookup_be.py results)")
    parser.add_argument("--prominence", type=float, default=0.05,
                        help="peak prominence threshold, fraction of max (default: 0.05)")
    parser.add_argument("--distance", type=float, default=0.5,
                        help="minimum peak spacing in eV (default: 0.5)")
    parser.add_argument("--peak-function", default="gaussian",
                        choices=["gaussian", "pseudo_voigt", "voigt"])
    parser.add_argument("--no-first-fit", action="store_true",
                        help="skip initial fitting pass, just detect")
    parser.add_argument("--region-label", default="", help="label for the region")
    parser.add_argument("--out", "-o", default=None,
                        help="write peaks.json to file")
    add_format_arg(parser)
    args = parser.parse_args()

    data = load_json(args.data, "--data")

    energies = data["energies"]
    config = {
        "energy_range": args.region or [float(min(energies)), float(max(energies))],
        "max_peaks": args.max_peaks,
        "n_peaks": args.n_peaks,
        "nist_positions": args.nist_positions,
        "prominence": args.prominence,
        "distance": args.distance,
        "peak_function": args.peak_function,
        "region_label": args.region_label,
        "run_first_fit": not args.no_first_fit,
    }

    result = find_peaks(data, config)

    print(f"Detected {len(result['peaks'])} peaks (first fit: {result['candidates_refined']})",
          file=sys.stderr)
    for p in result["peaks"]:
        print(f"  {p['label']}: {p['center']:.2f} eV  σ≈{p['sigma']:.2f}  A≈{p['amplitude']:.0f}",
              file=sys.stderr)

    if args.out:
        with open(args.out, "w") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Saved peaks.json to {args.out}", file=sys.stderr)
    else:
        # Output just the peaks template (not the raw candidates)
        out = {k: v for k, v in result.items() if k != "candidates_raw"}
        write_output(out, args.format)


if __name__ == "__main__":
    main()
