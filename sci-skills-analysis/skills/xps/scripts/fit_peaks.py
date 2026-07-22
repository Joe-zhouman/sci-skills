#!/usr/bin/env python3
"""
XPS peak fitting via lmfit.

This is the narrative engine. The fitting configuration (peaks.json) IS the story:
  - How many peaks? Where? How wide? What constraints?
  - Every constraint range is a dial — tighten to lock in your narrative,
    loosen to let the data speak (or to explore alternatives).

Uses lmfit for all fitting — the de-facto standard in the XPS Python ecosystem
(LG4X, KherveFitting are both built on it).

Config format (peaks.json):
{
  "region_label": "Si 2p",
  "energy_range": [107, 95],
  "peak_function": "pseudo_voigt",
  "peaks": [
    {
      "label": "Si0",
      "center":        99.60,  "center_range":  [99.0,  100.2],
      "sigma":          0.80,  "sigma_range":   [0.5,   1.5],
      "amplitude":   5000.0,   "amplitude_range": [1000, 20000],
      "fraction":       0.5,  "fraction_range": [0.0,   1.0]
    }
  ]
}

peak_function: gaussian | lorentzian | pseudo_voigt | voigt
  - pseudo_voigt: fraction 0.0 = pure Gaussian, 1.0 = pure Lorentzian
  - voigt: true Voigt convolution (slower, most physical)
"""

import sys
import json
import argparse
import os
from _cli import eprint, die, write_output, add_format_arg, load_json


def build_model(peaks_config: list[dict], peak_func: str, x, y):
    """Build an lmfit CompositeModel from peak configs."""
    import numpy as np
    from lmfit.models import (
        GaussianModel, LorentzianModel,
        PseudoVoigtModel, VoigtModel,
    )

    model_map = {
        "gaussian": GaussianModel,
        "lorentzian": LorentzianModel,
        "pseudo_voigt": PseudoVoigtModel,
        "voigt": VoigtModel,
    }

    if peak_func not in model_map:
        eprint({
            "type": "validation_error", "subtype": "unknown_peak_function",
            "param": "peak_function",
            "message": f"unknown peak function: {peak_func}",
            "hint": "use one of: gaussian, lorentzian, pseudo_voigt, voigt"
        })
        sys.exit(1)

    ModelClass = model_map[peak_func]

    # Build composite model
    params = None
    composite = None

    for i, pc in enumerate(peaks_config):
        prefix = f"p{i}_"
        model = ModelClass(prefix=prefix)

        if composite is None:
            composite = model
        else:
            composite += model

        # Set initial values and bounds
        if params is None:
            params = model.make_params()
        else:
            params.update(model.make_params())

        # center
        pkey = f"{prefix}center"
        params[pkey].set(value=pc["center"])
        if "center_range" in pc:
            params[pkey].set(min=pc["center_range"][0], max=pc["center_range"][1])

        # sigma (FWHM ≈ 2.355 * sigma for Gaussian)
        skey = f"{prefix}sigma"
        params[skey].set(value=pc.get("sigma", 1.0), min=0.01)
        if "sigma_range" in pc:
            params[skey].set(min=pc["sigma_range"][0], max=pc["sigma_range"][1])

        # amplitude
        akey = f"{prefix}amplitude"
        params[akey].set(value=pc.get("amplitude", max(y) * 0.5), min=0)
        if "amplitude_range" in pc:
            params[akey].set(min=pc["amplitude_range"][0],
                             max=pc["amplitude_range"][1])

        # fraction (only for pseudo_voigt)
        if peak_func == "pseudo_voigt":
            fkey = f"{prefix}fraction"
            params[fkey].set(value=pc.get("fraction", 0.5), min=0.0, max=1.0)
            if "fraction_range" in pc:
                params[fkey].set(min=pc["fraction_range"][0],
                                 max=pc["fraction_range"][1])

    return composite, params


def evaluate_fit(model, params, x):
    """Evaluate individual peak components and envelope."""
    import numpy as np

    components = model.eval_components(params=params, x=x)
    envelope = model.eval(params=params, x=x)

    peaks_out = []
    for name, y_comp in components.items():
        peaks_out.append({
            "prefix": name,
            "intensity": y_comp.tolist(),
        })

    return envelope, peaks_out


def fit_peaks(data: dict, config: dict, peak_func: str = "pseudo_voigt") -> dict:
    """Run peak fitting and return structured results.

    peak_func is a METHOD choice (gaussian|lorentzian|pseudo_voigt|voigt), passed
    in from the command line — it does NOT belong in peaks.json, which is pure
    data (peak positions, initial values, constraints). Method vs data separation.
    """
    import numpy as np

    energies = np.array(data["energies"])
    counts_sub = np.array(data.get("counts_subtracted", data["counts"]))

    # Restrict to fitting region
    region = config.get("energy_range")
    if region:
        r0, r1 = max(region), min(region)  # high BE → low BE
        mask = (energies <= r0) & (energies >= r1)
        x_fit = energies[mask]
        y_fit = counts_sub[mask]
    else:
        x_fit = energies
        y_fit = counts_sub

    # Pre-flight data check: NaN/inf in the fitting region propagates into the
    # optimizer and surfaces as an opaque traceback. Fail early with a typed envelope.
    if not np.all(np.isfinite(y_fit)):
        die({
            "type": "data_error", "subtype": "non_finite",
            "param": "--data",
            "message": "fitting region contains NaN or inf values",
            "hint": "check the background-subtraction step — Tougaard/polynomial can "
                    "produce inf at edges if the region is too narrow"
        })

    peaks_config = config.get("peaks", [])

    if not peaks_config:
        eprint({
            "type": "validation_error", "subtype": "no_peaks",
            "param": "peaks",
            "message": "peaks list is empty",
            "hint": "add at least one peak definition to peaks.json"
        })
        sys.exit(1)

    model, params = build_model(peaks_config, peak_func, x_fit, y_fit)

    # Fit — wrap the optimizer: non-convergence / singular Jacobian / NaN propagation
    # surface as raw lmfit tracebacks otherwise. Give the agent a typed envelope.
    from lmfit import fit_report
    try:
        result = model.fit(y_fit, params, x=x_fit, method="leastsq")
    except Exception as exc:
        die({
            "type": "fit_error", "subtype": "optimizer_failed",
            "param": "--config",
            "message": f"lmfit did not produce a result: {type(exc).__name__}: {exc}",
            "hint": "common fixes: widen *_range constraints, reduce peak count, "
                    "or check initial values aren't wildly off the data"
        })

    # Evaluate on full energy range
    envelope_full = model.eval(params=result.params, x=energies)
    components = model.eval_components(params=result.params, x=energies)

    # Build peak summary
    peaks_summary = []
    for i, pc in enumerate(peaks_config):
        prefix = f"p{i}_"
        pk = {
            "label": pc["label"],
            "prefix": prefix,
            "center": round(float(result.params[f"{prefix}center"].value), 4),
            "center_stderr": round(float(result.params[f"{prefix}center"].stderr or 0), 4),
            "sigma": round(float(result.params[f"{prefix}sigma"].value), 4),
            "sigma_stderr": round(float(result.params[f"{prefix}sigma"].stderr or 0), 4),
            "amplitude": round(float(result.params[f"{prefix}amplitude"].value), 2),
            "amplitude_stderr": round(float(result.params[f"{prefix}amplitude"].stderr or 0), 2),
        }
        # fwhm ≈ 2.355 * sigma for Gaussian component
        pk["fwhm_approx"] = round(pk["sigma"] * 2.355, 4)

        if peak_func == "pseudo_voigt":
            pk["fraction"] = round(float(result.params[f"{prefix}fraction"].value), 4)
            pk["fraction_stderr"] = round(float(result.params[f"{prefix}fraction"].stderr or 0), 4)

        peaks_summary.append(pk)

    # Component intensities
    comp_dict = {}
    for name, y_comp in components.items():
        comp_dict[name] = y_comp.tolist()

    # Fit quality
    r_squared = 1 - np.sum(result.residual**2) / np.sum(
        (y_fit - np.mean(y_fit))**2
    )

    # Warning signs
    warnings = []
    for pk in peaks_summary:
        # Check if parameters hit bounds
        pc_config = peaks_config[peaks_summary.index(pk)]
        center_range = pc_config.get("center_range")
        if center_range:
            if abs(pk["center"] - center_range[0]) < 0.01:
                warnings.append(f"{pk['label']}: center at lower bound ({center_range[0]})")
            if abs(pk["center"] - center_range[1]) < 0.01:
                warnings.append(f"{pk['label']}: center at upper bound ({center_range[1]})")
        if pk["fwhm_approx"] < 0.3:
            warnings.append(f"{pk['label']}: FWHM unreasonably narrow ({pk['fwhm_approx']:.2f} eV)")
        if r_squared < 0.8:
            warnings.append(f"R² = {r_squared:.3f} — poor fit, consider adjusting peaks or constraints")

    return {
        "energies": energies.tolist(),
        "counts_raw": data["counts"],
        "counts_subtracted": counts_sub.tolist(),
        "background": data.get("background"),
        "region_label": config.get("region_label", ""),
        "peak_function": peak_func,
        "peaks": peaks_summary,
        "components": comp_dict,
        "envelope": envelope_full.tolist(),
        "residual": (counts_sub - envelope_full).tolist(),
        "fit_quality": {
            "r_squared": round(float(r_squared), 4),
            "n_peaks": len(peaks_config),
            "n_data_points": len(x_fit),
        },
        "warnings": warnings,
        "config_snapshot": config,
        "metadata": dict(data.get("metadata", {})),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Fit XPS peaks using lmfit — every constraint is a narrative dial"
    )
    parser.add_argument("--data", "-d", required=True,
                        help="path to input JSON (from subtract_background.py)")
    parser.add_argument("--config", "-c", required=True,
                        help="path to peaks config JSON (pure data: peak positions + constraints)")
    parser.add_argument("--peak-function", default="pseudo_voigt",
                        choices=["gaussian", "lorentzian", "pseudo_voigt", "voigt"],
                        help="fit method (default: pseudo_voigt)")
    parser.add_argument("--out", "-o", default=None,
                        help="write fit result to file instead of stdout")
    add_format_arg(parser)

    args = parser.parse_args()

    data = load_json(args.data, "--data")
    config = load_json(args.config, "--config")

    result = fit_peaks(data, config, peak_func=args.peak_function)

    # Print warnings to stderr
    if result["warnings"]:
        for w in result["warnings"]:
            eprint({"type": "fit_warning", "message": w})

    if args.out:
        with open(args.out, "w") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Saved to {args.out}", file=sys.stderr)
    else:
        write_output(result, args.format)


if __name__ == "__main__":
    main()
