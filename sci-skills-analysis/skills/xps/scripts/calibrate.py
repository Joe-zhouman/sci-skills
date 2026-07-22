#!/usr/bin/env python3
"""Calibrate XPS binding energy scale by applying a reference-based shift."""

import sys
import json
import argparse
import os
from _cli import eprint, write_output, add_format_arg, load_json


# Standard reference peaks (eV)
REFERENCES = {
    "C1s": 284.8,
    "Au4f7": 83.96,
    "Ag3d5": 368.21,
    "Cu2p3": 932.62,
}

# Known issues per reference
CAVEATS = {
    "C1s": (
        "C 1s adventitious carbon @ 284.8 eV is unreliable — "
        "shifts of ±0.5 eV or more are common (Gengenbach 2022, Appl. Surf. Sci. 606:154855). "
        "Prefer an internal standard (Au 4f, known chemical state) when available."
    ),
    "Au4f7": "Au 4f₇/₂ @ 83.96 eV — reliable internal standard for samples with gold.",
}


def calibrate(data: dict, reference: str | None, position: float | None,
              shift: float | None) -> dict:
    """Apply energy calibration and return updated data with metadata."""
    import numpy as np

    energies = np.array(data["energies"])
    counts = np.array(data["counts"])
    meta = dict(data.get("metadata", {}))

    if shift is not None:
        applied_shift = shift
        method = "manual"
        ref_info = f"manual shift of {shift:+.3f} eV"
    elif reference and position is not None:
        expected = REFERENCES.get(reference, position)
        applied_shift = expected - position
        method = "reference"
        ref_info = f"{reference} @ {position:.3f} eV → shifted to {expected:.3f} eV"
    else:
        eprint({
            "type": "validation_error", "subtype": "missing_args",
            "message": "provide either --shift or both --reference and --position"
        })
        sys.exit(1)

    calibrated_energies = energies + applied_shift

    meta["calibration"] = {
        "method": method,
        "reference": reference,
        "measured_position": position,
        "expected_position": REFERENCES.get(reference) if reference else None,
        "shift_applied": round(applied_shift, 4),
        "description": ref_info,
    }
    if reference in CAVEATS:
        meta["calibration"]["caveat"] = CAVEATS[reference]

    result = {
        "energies": calibrated_energies.tolist(),
        "counts": counts.tolist(),
        "metadata": meta,
    }

    # Warn about C1s
    if reference == "C1s":
        eprint({
            "type": "warning",
            "subtype": "unreliable_reference",
            "message": CAVEATS["C1s"]
        })

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Calibrate XPS binding energy by applying a reference-based shift"
    )
    parser.add_argument("--data", "-d", required=True, help="path to input JSON ({energies, counts, metadata})")
    parser.add_argument("--reference", "-r", choices=list(REFERENCES.keys()),
                        help="reference peak name (C1s, Au4f7, Ag3d5, Cu2p3)")
    parser.add_argument("--position", "-p", type=float,
                        help="measured position of reference peak (eV)")
    parser.add_argument("--shift", "-s", type=float,
                        help="manual energy shift in eV (overrides --reference)")
    parser.add_argument("--out", "-o", default=None,
                        help="write result to file instead of stdout")
    add_format_arg(parser)

    args = parser.parse_args()

    data = load_json(args.data, "--data")

    if args.shift is not None:
        result = calibrate(data, None, None, args.shift)
    elif args.reference and args.position is not None:
        result = calibrate(data, args.reference, args.position, None)
    else:
        eprint({
            "type": "cli_error", "subtype": "missing_args",
            "message": "provide either --shift or both --reference and --position",
            "hint": "example: --reference C1s --position 284.2  or  --shift 0.6"
        })
        sys.exit(1)

    if args.out:
        with open(args.out, "w") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Saved to {args.out}", file=sys.stderr)
    else:
        write_output(result, args.format)


if __name__ == "__main__":
    main()
