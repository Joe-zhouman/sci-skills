#!/usr/bin/env python3
"""
Compute atom% from fitted XPS peaks using relative sensitivity factors (RSF).

Takes one or more fit.json files (one per element/region) + an RSF source,
and computes atomic percentages.

RSF source resolution (auto-detect or explicit):
  auto          Check state.json for user-provided RSF table, fall back to
                built-in Scofield theoretical RSF.
  scofield      Use built-in Scofield t-RSF (Al Kα, C 1s = 1.000).
  /path/rsf.csv User-provided CSV (columns: Element,Line,RSF).

Usage:
  python scripts/quantify.py -f si2p/fit.json n1s/fit.json o1s/fit.json
  python scripts/quantify.py -f si2p/fit.json n1s/fit.json --assign "Si 2p:N 1s:O 1s"
  python scripts/quantify.py -f si2p/fit.json --rsf-source scofield
  python scripts/quantify.py -f si2p/fit.json --rsf-source /path/to/rsf.csv
"""

import sys
import json
import argparse
import os
import math
from _cli import eprint, die, write_output, add_format_arg, load_json

# ── Built-in Scofield RSF table (Al Kα, 1486.6 eV) ──────────────────────
# Normalized to C 1s = 1.000.
# Source: Scofield, J.H. (1976) J. Electron Spectrosc. Relat. Phenom. 8, 129–137.
# Cross-referenced with R.N. King's compilation (xpsdatabase.com).
# fmt: off
_SCOFIELD_RSF = {
    # s orbitals
    ("Li", "1s"): 0.057,  ("Be", "1s"): 0.172,  ("B",  "1s"): 0.405,
    ("C",  "1s"): 1.000,  ("N",  "1s"): 1.678,  ("O",  "1s"): 2.930,
    ("F",  "1s"): 4.430,  ("Na", "1s"): 8.520,
    ("Mg", "2s"): 1.047,  ("Al", "2s"): 0.935,  ("Si", "2s"): 1.074,
    ("P",  "2s"): 1.332,  ("S",  "2s"): 1.635,
    # p orbitals
    ("Na", "2p"): 2.018,  ("Mg", "2p"): 2.042,  ("Al", "2p"): 1.854,
    ("Si", "2p"): 2.115,  ("P",  "2p"): 2.596,  ("S",  "2p"): 3.153,
    ("Cl", "2p"): 3.661,  ("K",  "2p"): 5.070,  ("Ca", "2p"): 5.070,
    ("Sc", "2p"): 6.02,   ("Ti", "2p"): 7.12,   ("V",  "2p"): 8.28,
    ("Cr", "2p"): 9.51,   ("Mn", "2p"): 10.82,  ("Fe", "2p"): 12.23,
    ("Co", "2p"): 13.71,  ("Ni", "2p"): 15.32,  ("Cu", "2p"): 16.95,
    ("Zn", "2p"): 18.65,  ("Ga", "2p"): 20.50,  ("Ge", "2p"): 22.50,
    ("Ga", "3p"): 1.46,   ("Ge", "3p"): 2.10,   ("As", "3p"): 2.82,
    ("Se", "3p"): 3.60,   ("Br", "3p"): 4.43,
    # d orbitals
    ("Ga", "3d"): 1.89,   ("Ge", "3d"): 2.69,   ("As", "3d"): 3.55,
    ("Se", "3d"): 4.47,   ("Br", "3d"): 5.44,   ("Rb", "3d"): 6.93,
    ("Sr", "3d"): 7.94,   ("Y",  "3d"): 9.05,   ("Zr", "3d"): 10.14,
    ("Nb", "3d"): 11.36,  ("Mo", "3d"): 12.63,  ("Ru", "3d"): 14.29,
    ("Rh", "3d"): 15.82,  ("Pd", "3d"): 17.41,  ("Ag", "3d"): 19.03,
    ("Cd", "3d"): 20.68,  ("In", "3d"): 22.41,  ("Sn", "3d"): 24.12,
    ("Sb", "3d"): 25.96,  ("Te", "3d"): 27.95,  ("I",  "3d"): 29.98,
    ("Cs", "3d"): 33.19,  ("Ba", "3d"): 35.42,  ("La", "3d"): 37.65,
    ("Ce", "3d"): 39.93,  ("Pr", "3d"): 42.24,  ("Nd", "3d"): 44.62,
    # f orbitals
    ("Hf", "4f"): 8.41,   ("Ta", "4f"): 9.39,   ("W",  "4f"): 10.48,
    ("Ir", "4f"): 12.66,  ("Pt", "4f"): 13.98,  ("Au", "4f"): 17.47,
    ("Hg", "4f"): 18.80,  ("Tl", "4f"): 20.03,  ("Pb", "4f"): 21.38,
    ("Bi", "4f"): 22.72,
}
# fmt: on


def _load_rsf_table(rsf_source: str) -> dict:
    """Return a dict {(Element, Line): rsf_value} from the given source."""
    if rsf_source == "scofield":
        return dict(_SCOFIELD_RSF)
    # Assume file path: user-provided CSV
    if not os.path.exists(rsf_source):
        die({
            "type": "io_error", "subtype": "file_not_found",
            "param": "--rsf-source",
            "message": f"RSF file not found: {rsf_source}",
            "hint": "check the path, or use --rsf-source scofield for built-in values",
        })
    import pandas as pd
    df = pd.read_csv(rsf_source)
    required = {"Element", "Line", "RSF"}
    missing = required - set(df.columns)
    if missing:
        die({
            "type": "validation_error", "subtype": "missing_columns",
            "param": "--rsf-source",
            "message": f"RSF CSV missing columns: {missing}",
            "hint": "CSV must have columns: Element, Line, RSF",
        })
    table = {}
    for _, row in df.iterrows():
        elem = str(row["Element"]).strip()
        line = str(row["Line"]).strip()
        table[(elem, line)] = float(row["RSF"])
    return table


def _resolve_rsf_source(args_rsf_source: str | None) -> tuple[str, str]:
    """Resolve RSF source: explicit arg > state.json > scofield fallback.

    Returns (source_type, source_path_or_label).
    """
    if args_rsf_source == "scofield":
        return "scofield", "scofield"
    if args_rsf_source and args_rsf_source not in ("auto",):
        return "user-file", args_rsf_source

    # auto: check state.json
    workdir = os.path.join("sci-skills", "sci-analysis", "xps")
    state_file = os.path.join(workdir, "state.json")
    if os.path.exists(state_file):
        try:
            with open(state_file) as f:
                state = json.load(f)
        except Exception:
            state = {}
        rsf = state.get("rsf")
        if rsf and rsf.get("source") == "user" and rsf.get("file"):
            user_file = os.path.join(workdir, rsf["file"])
            if os.path.exists(user_file):
                return "user-file", user_file
    return "scofield", "scofield"


def _parse_region_label(label: str) -> tuple[str, str]:
    """Parse region labels like 'Si 2p', 'N 1s', 'O 1s', 'Sn 3d'.

    Returns (element, line) or (None, None) on failure.
    """
    import re
    m = re.match(r"(\w+)\s+(\d[spdf](?:\d?/\d)?)", label, re.IGNORECASE)
    if m:
        return m.group(1), m.group(2).lower()
    # Try elemental symbol only (e.g., just "Si")
    m = re.match(r"(\w+)$", label.strip(), re.IGNORECASE)
    if m:
        return m.group(1), "auto"
    return None, None


def quantify(fit_paths: list[str], rsf_source: str = "auto",
             assignments: dict[str, str] | None = None) -> dict:
    """Compute atom% from fit.json files.

    assignments: optional dict {region_label: rsf_key_label}
                 e.g. {"Si 2p": "Si 2p", "N 1s": "N 1s"}
    """
    source_type, source_path = _resolve_rsf_source(rsf_source)
    rsf_table = _load_rsf_table(source_path)

    elements = []
    unmatched = []

    for path in fit_paths:
        data = load_json(path, "--fit")
        label = data.get("region_label", "")
        element, line = _parse_region_label(label)
        explicit = (assignments or {}).get(label)

        # Resolve RSF: try explicit assignment → parsed label → guess by searching fit peaks
        rsf = None
        if element and line and line != "auto":
            rsf = rsf_table.get((element, line))
            if rsf is None:
                # Try without spin-orbit suffix: '2p' from '2p3/2' etc
                import re
                base = re.sub(r'\d/\d', '', line)
                rsf = rsf_table.get((element, base))
        elif element and line == "auto":
            # Element only — need to guess line from peak config
            pass

        if rsf is None and element:
            # Fallback: try scanning the peak config for line hints
            for pk in data.get("config_snapshot", {}).get("peaks", []):
                # peaks have labels like "Si3N4", "Si0" — extract element
                pass

        if rsf is None:
            # Last resort: search rsf_table for any entry matching the element
            candidates = [(e, l, v) for (e, l), v in rsf_table.items() if e == element]
            if len(candidates) == 1:
                rsf = candidates[0][2]
                line = candidates[0][1]
            elif len(candidates) > 1:
                # Pick the one with the largest RSF (usually the main line)
                rsf = max(candidates, key=lambda x: x[2])[2]
                line = max(candidates, key=lambda x: x[2])[1]

        if rsf is None:
            unmatched.append(label)
            continue

        # Sum all peak amplitudes for this region (raw area proxy)
        total_area = 0.0
        for pk in data.get("peaks", []):
            total_area += pk.get("amplitude", 0.0) * pk.get("sigma", 1.0) * math.sqrt(2 * math.pi)

        # If peaks lack amplitude*sigma integration, fall back to envelope area
        if total_area < 1e-6:
            import numpy as np
            total_area = float(np.trapz(data.get("envelope", [])))

        elements.append({
            "label": label,
            "element": element,
            "line": line,
            "area": round(total_area, 2),
            "rsf": rsf,
            "area_over_rsf": round(total_area / rsf, 2),
            "rsf_source": "user" if source_type == "user-file" else "scofield",
        })

    if unmatched:
        eprint({
            "type": "quantify_warning", "subtype": "unmatched_region",
            "message": f"could not match RSF for: {', '.join(unmatched)}",
            "hint": "use --assign to explicitly map region labels to (Element,Line) pairs "
                    "e.g. --assign 'My Peak:Si 2p:Si 2p'",
        })

    if not elements:
        die({
            "type": "quantify_error", "subtype": "no_elements",
            "message": "no regions matched to any RSF value",
            "hint": "check region labels — they should contain element+line like 'Si 2p'",
        })

    # Normalize to 100%
    total_aor = sum(e["area_over_rsf"] for e in elements)
    for e in elements:
        e["atom_percent"] = round(e["area_over_rsf"] / total_aor * 100, 2)

    return {
        "method": "rsf_corrected",
        "rsf_source": source_type,
        "rsf_source_detail": source_path if source_type == "user-file" else "Scofield (1976), Al Kα, C 1s = 1.000",
        "imfp_corrected": False,
        "note": "atom% computed without IMFP correction. For strict quantification, "
                "divide by IMFP ~ E_kin^0.6 before normalization.",
        "elements": elements,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Compute atom% from fitted XPS peaks using RSF"
    )
    parser.add_argument("--fits", "-f", nargs="+", required=True,
                        help="one or more fit.json files (via fit_peaks.py)")
    parser.add_argument("--rsf-source", default="auto",
                        help="'auto' (check state.json), 'scofield' (built-in), "
                             "or path to user CSV (Element,Line,RSF)")
    parser.add_argument("--assign", nargs="+", default=None,
                        help="explicit region→(Element,Line) mappings: "
                             "'Si 2p:Si 2p' 'N 1s:N 1s'")
    parser.add_argument("--out", "-o", default=None,
                        help="write result to file")
    add_format_arg(parser)

    args = parser.parse_args()

    # Parse --assign: "Label:Element Line" pairs
    assignments = {}
    if args.assign:
        for a in args.assign:
            if ":" not in a:
                continue
            label, spec = a.split(":", 1)
            assignments[label.strip()] = spec.strip()

    result = quantify(args.fits, rsf_source=args.rsf_source, assignments=assignments)

    if args.out:
        with open(args.out, "w") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Saved to {args.out}", file=sys.stderr)
    else:
        write_output(result, args.format)


if __name__ == "__main__":
    main()
