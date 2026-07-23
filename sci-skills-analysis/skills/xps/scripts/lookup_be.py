#!/usr/bin/env python3
"""
Look up XPS binding energies from the NIST database.

Data source: NIST X-ray Photoelectron Spectroscopy Database (SRD 20)
via KherveDB archive (2019 snapshot, 55,948 records).

This is a DETERMINISTIC lookup — script reads the database, not LLM memory.

Usage:
  python scripts/lookup_be.py Si                                    # all Si entries
  python scripts/lookup_be.py Si --line 2p                          # Si 2p only
  python scripts/lookup_be.py C --line 1s --range 284 286           # C 1s 284-286 eV
  python scripts/lookup_be.py Si,N,O --line 2p --quality Good       # only Good quality
  python scripts/lookup_be.py Si3N4 --search-formula                # formula search
  python scripts/lookup_be.py Si --line 2p --fwhm                   # FWHM stats for Si 2p
  python scripts/lookup_be.py Si --line 2p --split                  # spin-orbit splitting
"""

import sys
import json
import argparse
import os
import math
from _cli import eprint, write_output, add_format_arg


def load_db() -> "pd.DataFrame":
    """Load the NIST parquet database."""
    try:
        import pandas as pd
    except ImportError:
        eprint({
            "type": "dependency_error", "subtype": "missing_package",
            "param": "pandas",
            "message": "pandas is required to read the NIST database",
            "hint": "conda install pandas pyarrow",
        })
        sys.exit(1)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "..", "assets", "NIST_BE.parquet")

    if not os.path.exists(db_path):
        eprint({
            "type": "io_error", "subtype": "asset_missing",
            "param": "NIST_BE.parquet",
            "message": "NIST database parquet not found in assets/",
            "hint": "the skill ships NIST_BE.parquet in assets/ — reinstall the skill, "
                    "or fetch it from https://github.com/gkerherve/KherveDB and place it there",
            "expected_path": os.path.abspath(db_path),
        })
        sys.exit(1)

    return pd.read_parquet(db_path)


def lookup(df, elements=None, line=None, be_range=None, quality=None,
           formula_search=None, limit=200):
    """Query the NIST database."""
    mask = df['BE (eV)'].notna()

    if quality:
        mask &= df['Quality'].isin(quality if isinstance(quality, list) else [quality])

    if elements:
        elem_mask = df['Element'].str.strip().isin(elements)
        mask &= elem_mask

    if line:
        mask &= df['Line'].str.contains(line, na=False, case=False)

    if formula_search:
        mask &= df['Formula'].str.contains(formula_search, na=False, case=False)

    if be_range:
        mask &= df['BE (eV)'].between(be_range[0], be_range[1])

    result = df[mask].sort_values('BE (eV)')

    if len(result) > limit:
        # For large results, group by formula for summary
        # Include representative citation per group
        summary = result.groupby(['Element', 'Line', 'Formula']).agg(
            be_count=('BE (eV)', 'count'),
            be_mean=('BE (eV)', 'mean'),
            be_std=('BE (eV)', 'std'),
            be_min=('BE (eV)', 'min'),
            be_max=('BE (eV)', 'max'),
            top_quality=('Quality', lambda x: x.mode().iloc[0] if not x.mode().empty else 'N/A'),
            top_author=('Author', lambda x: x.mode().iloc[0] if not x.mode().empty else 'N/A'),
            top_journal=('Journal', lambda x: x.mode().iloc[0] if not x.mode().empty else 'N/A'),
        ).round(3).reset_index().sort_values('be_mean')

        return {
            "summary": True,
            "total_records": len(result),
            "shown_groups": len(summary),
            "grouped_by_formula": summary.to_dict(orient='records'),
        }

    cols = ['Element', 'Line', 'BE (eV)', 'Formula', 'Name', 'Quality',
            'Charge Reference', 'Author', 'Journal',
            'Full Width at Half-maximum Intensity (eV)',
            'Gaussian Width (eV)', 'Lorentzian Width (eV)',
            'Energy Uncertainty', 'Background Subtraction Method',
            'Peak Location Method']
    available = [c for c in cols if c in result.columns]
    return {
        "summary": False,
        "count": len(result),
        "results": result[available].to_dict(orient='records'),
    }


def _get_j_components(line_base: str) -> tuple:
    """Map an orbital label like '2p' to its two j-components.

    Returns (j_high, j_low, area_ratio_numerator_high, area_ratio_denominator)
    e.g. '2p' -> ('2p3/2', '2p1/2', 2, 1)
         '3d' -> ('3d5/2', '3d3/2', 3, 2)
         '4f' -> ('4f7/2', '4f5/2', 4, 3)
    Returns (None, None, 0, 0) if the line has no spin-orbit splitting (s orbitals).
    """
    import re
    m = re.match(r'(\d+)([spdf])', line_base.strip().lower())
    if not m:
        return None, None, 0, 0
    n_principal = int(m.group(1))
    orbital = m.group(2)
    l_map = {'s': 0, 'p': 1, 'd': 2, 'f': 3}
    l = l_map.get(orbital)
    if l is None or l == 0:
        # s orbitals don't split — but shouldn't be called with --split on s
        return None, None, 0, 0
    # j = l ± 1/2 → degeneracy = 2j+1
    j_high = l + 0.5   # degeneracy: 2*(l+0.5)+1 = 2l+2
    j_low  = l - 0.5   # degeneracy: 2*(l-0.5)+1 = 2l
    area_high = 2 * l + 2
    area_low  = 2 * l
    j_high_str = f"{n_principal}{orbital}{int(j_high*2)}/2"
    j_low_str  = f"{n_principal}{orbital}{int(j_low*2)}/2"
    # Normalize ratio: e.g. d: (2l+2):(2l) = 4:2 = 2:1, f: (2l+2):(2l) = 6:4 = 3:2
    from math import gcd
    g = gcd(area_high, area_low)
    return j_high_str, j_low_str, area_high // g, area_low // g


def spin_orbit_split(df, elements, line, quality=None) -> dict:
    """Compute spin-orbit splitting by querying both j-components.

    First tries to match records where the SAME paper reported both components
    (same Author + Formula + Journal). If < 3 matched pairs found, falls back
    to the global mean difference across all records for each component.
    """
    j_high, j_low, ratio_high, ratio_low = _get_j_components(line)

    if j_high is None:
        return {
            "error": f"Line '{line}' has no spin-orbit splitting (s orbital or unrecognized)",
            "hint": "Use --split only with p, d, or f orbitals (e.g., --line 2p, --line 3d, --line 4f)",
        }

    # Build base mask
    mask = df['BE (eV)'].notna()
    if quality:
        mask &= df['Quality'].isin(quality if isinstance(quality, list) else [quality])
    if elements:
        mask &= df['Element'].str.strip().isin(elements)

    # Get records for each j-component
    high_mask = mask & df['Line'].str.contains(j_high, na=False, case=False) & ~df['Line'].str.contains('sat', na=False, case=False)
    low_mask  = mask & df['Line'].str.contains(j_low, na=False, case=False) & ~df['Line'].str.contains('sat', na=False, case=False)

    df_high = df[high_mask][['BE (eV)', 'Formula', 'Author', 'Journal', 'Quality']].copy()
    df_low  = df[low_mask][['BE (eV)', 'Formula', 'Author', 'Journal', 'Quality']].copy()

    # Try matched-pair approach: same Formula + Author → same paper measured both
    # Convention: splitting = BE(j_low) - BE(j_high), always positive.
    # (higher j → lower BE → higher intensity)
    merged = df_high.merge(df_low, on=['Formula', 'Author'], suffixes=('_high', '_low'))
    if len(merged) >= 3:
        merged['splitting'] = merged['BE (eV)_low'] - merged['BE (eV)_high']
        splitting_mean = merged['splitting'].mean()
        splitting_std  = merged['splitting'].std()
        return {
            "method": "matched_pairs",
            "line": line,
            "j_high": j_high, "j_low": j_low,
            "area_ratio": f"{ratio_high}:{ratio_low}",
            "n_pairs": len(merged),
            "splitting_mean_eV": round(splitting_mean, 3),
            "splitting_std_eV": round(splitting_std, 3) if not (isinstance(splitting_std, float) and math.isnan(splitting_std)) else None,
            f"be_{j_high}_mean_eV": round(merged['BE (eV)_high'].mean(), 2),
            f"be_{j_low}_mean_eV": round(merged['BE (eV)_low'].mean(), 2),
            "notes": "Splitting = BE(j_low) − BE(j_high). Computed from NIST records where same paper reported both components.",
        }

    # Fallback: global mean per component (less reliable but gives a rough number)
    be_high_mean = df_high['BE (eV)'].mean()
    be_low_mean  = df_low['BE (eV)'].mean()
    n_high = len(df_high)
    n_low  = len(df_low)

    if n_high == 0 or n_low == 0:
        return {
            "error": f"Insufficient NIST data: {j_high} n={n_high}, {j_low} n={n_low}",
            "hint": f"Use Handbook of XPS (Moulder 1992) or NIST live search for {j_high}/{j_low} splitting",
        }

    return {
        "method": "global_mean",
        "line": line,
        "j_high": j_high, "j_low": j_low,
        "area_ratio": f"{ratio_high}:{ratio_low}",
        f"n_{j_high}": n_high, f"n_{j_low}": n_low,
        f"be_{j_high}_mean_eV": round(be_high_mean, 2),
        f"be_{j_low}_mean_eV": round(be_low_mean, 2),
        "splitting_mean_eV": round(be_low_mean - be_high_mean, 3),
        "warning": "WARNING: global-mean fallback (insufficient matched pairs in NIST). "
                   "Splitting is a physical constant — prefer Handbook of XPS values.",
    }


def fwhm_stats(df, elements, line, be_range, quality, formula_search) -> dict:
    """Aggregate FWHM statistics for matching records that have FWHM data."""
    mask = df['Full Width at Half-maximum Intensity (eV)'].notna()

    if quality:
        mask &= df['Quality'].isin(quality if isinstance(quality, list) else [quality])
    if elements:
        mask &= df['Element'].str.strip().isin(elements)
    if line:
        mask &= df['Line'].str.contains(line, na=False, case=False)
    if be_range:
        mask &= df['BE (eV)'].between(be_range[0], be_range[1])
    if formula_search:
        mask &= df['Formula'].str.contains(formula_search, na=False, case=False)

    fwhm_col = 'Full Width at Half-maximum Intensity (eV)'
    gauss_col = 'Gaussian Width (eV)'
    loren_col = 'Lorentzian Width (eV)'

    subset = df[mask]
    n_fwhm = len(subset)

    if n_fwhm == 0:
        return {"error": "No FWHM data found for these query parameters",
                "hint": "Only 12.6% of NIST records include FWHM. Try broadening the query, "
                        "or use the reference table in peak-fitting.md for guidance."}

    stats = {
        "n_records": n_fwhm,
        "fwhm_mean_eV": round(subset[fwhm_col].mean(), 2),
        "fwhm_std_eV": round(subset[fwhm_col].std(), 2),
        "fwhm_min_eV": round(subset[fwhm_col].min(), 2),
        "fwhm_max_eV": round(subset[fwhm_col].max(), 2),
        "fwhm_median_eV": round(subset[fwhm_col].median(), 2),
    }

    # Gaussian/Lorentzian widths if available
    if subset[gauss_col].notna().any():
        stats["gaussian_width_mean_eV"] = round(subset[gauss_col].dropna().mean(), 2)
    if subset[loren_col].notna().any():
        stats["lorentzian_width_mean_eV"] = round(subset[loren_col].dropna().mean(), 2)

    # Per-formula breakdown: show top 15 (by record count) if any found
    formulas_with_fwhm = subset.groupby('Formula')[fwhm_col].agg(['count', 'mean', 'std']).dropna()
    formulas_with_fwhm = formulas_with_fwhm[formulas_with_fwhm['count'] >= 2].round(2)
    formulas_with_fwhm = formulas_with_fwhm.sort_values('count', ascending=False)
    if len(formulas_with_fwhm) > 0:
        top_n = formulas_with_fwhm.head(15)
        stats["by_formula"] = top_n.reset_index().rename(
            columns={'count': 'n', 'mean': 'fwhm_mean', 'std': 'fwhm_std'}
        ).to_dict(orient='records')
        if len(formulas_with_fwhm) > 15:
            stats["by_formula_truncated"] = True
            stats["by_formula_total_groups"] = len(formulas_with_fwhm)

    # Material-class hint based on formula keywords
    materials = [str(f) for f in subset['Formula'].dropna().unique()]
    stats["material_class_hint"] = _guess_material_class(materials)

    return stats


def _guess_material_class(formulas: list) -> str:
    """Heuristic material class from formula names."""
    has_oxide = any('O' in str(f) and any(c.isdigit() for c in str(f)) for f in formulas)
    has_metal = any(str(f).strip() in {
        'Ag','Au','Cu','Ni','Pt','Pd','Fe','Co','Cr','Mo','W','Al','Ti','Zn','Sn','Pb','Mn','V'
    } for f in formulas)
    has_polymer = any('C' in str(f) and 'H' in str(f) for f in formulas)

    if has_polymer:
        return "polymer/organic — expected FWHM 0.8–1.4 eV"
    if has_metal and not has_oxide:
        return "pure metal — expected FWHM 0.3–0.6 eV (single crystal) to 0.6–1.0 eV (polycrystalline)"
    if has_oxide:
        return "oxide/inorganic — expected FWHM 0.9–1.8 eV"
    return "unknown — see FWHM table in peak-fitting.md"


def main():
    parser = argparse.ArgumentParser(
        description="Look up XPS binding energies from NIST database (SRD 20)"
    )
    parser.add_argument("query", nargs="?", default=None,
                        help="element symbol (e.g. Si) or comma-separated list (e.g. Si,N,O)")
    parser.add_argument("--line", "-l", default=None,
                        help="filter by spectral line (e.g. 1s, 2p, 2p3/2)")
    parser.add_argument("--range", "-r", nargs=2, type=float, default=None,
                        metavar=("LOW", "HIGH"),
                        help="filter by binding energy range (eV)")
    parser.add_argument("--quality", "-q", choices=["Good", "Adequate", "Good,Adequate"],
                        default="Good,Adequate",
                        help="minimum data quality (default: Good,Adequate)")
    parser.add_argument("--search-formula", "-s", default=None,
                        help="search by formula substring (e.g. Si3N4)")
    parser.add_argument("--limit", type=int, default=200,
                        help="max raw results before grouping (default: 200)")
    # table is a human-readable column format; json/pretty follow the shared CLI contract
    parser.add_argument("--format", choices=["json", "pretty", "table"],
                        default="pretty" if sys.stdout.isatty() else "json",
                        help="output format (default: pretty for TTY, json for pipe; "
                             "table = column-aligned human view)")
    parser.add_argument("--show-all-columns", action="store_true",
                        help="include all columns in JSON output (honored by --split and --fwhm)")
    parser.add_argument("--split", action="store_true",
                        help="compute spin-orbit splitting for the given --line (p/d/f orbitals)")
    parser.add_argument("--fwhm", action="store_true",
                        help="aggregate FWHM statistics for matching records (instead of BE lookup)")

    args = parser.parse_args()

    df = load_db()

    # Parse quality
    qualities = args.quality.split(",") if args.quality else None

    # Parse elements from query or formula search
    elements = None
    if args.query:
        parts = [e.strip() for e in args.query.split(",")]
        # Check if these look like element symbols (1-2 letters, optional whitespace)
        if all(len(p.split()[-1]) <= 3 for p in parts):
            elements = parts
        else:
            # Treat as formula search
            args.search_formula = args.search_formula or args.query

    # --- Mode dispatch ---
    if args.fwhm:
        # FWHM aggregation mode
        result = fwhm_stats(df, elements=elements, line=args.line,
                            be_range=args.range and tuple(args.range),
                            quality=qualities, formula_search=args.search_formula)
        output = {
            "source": "NIST X-ray Photoelectron Spectroscopy Database (SRD 20)",
            "source_url": "https://srdata.nist.gov/xps/",
            "archive": "KherveDB 2019 snapshot (55,948 records)",
            "mode": "fwhm_stats",
            **result,
        }
        write_output(output, args.format)
        msg = (
            "---\n"
            "Only 12.6% of NIST records include FWHM. Data may be sparse.\n"
            "For a complete reference, see the FWHM table in peak-fitting.md.\n"
            "NIST live: https://srdata.nist.gov/xps/"
        )
        print(msg, file=sys.stderr)
        return

    if args.split:
        if not args.line:
            print("Error: --split requires --line (e.g., --line 2p, --line 3d, --line 4f)", file=sys.stderr)
            sys.exit(1)
        result = spin_orbit_split(df, elements=elements, line=args.line,
                                  quality=qualities)
        output = {
            "source": "NIST X-ray Photoelectron Spectroscopy Database (SRD 20)",
            "source_url": "https://srdata.nist.gov/xps/",
            "archive": "KherveDB 2019 snapshot (55,948 records)",
            "mode": "spin_orbit_split",
            **result,
        }
        write_output(output, args.format)
        msg = (
            "---\n"
            "WARNING: NIST records for spin-orbit splitting are sparse and imbalanced.\n"
            "Preferred source: Moulder et al., Handbook of XPS (Physical Electronics, 1992).\n"
            "See peak-fitting.md for a pre-computed table of common elements.\n"
            "NIST live: https://srdata.nist.gov/xps/"
        )
        print(msg, file=sys.stderr)
        return

    # --- Default: BE lookup mode ---
    result = lookup(df, elements=elements, line=args.line,
                    be_range=args.range and tuple(args.range),
                    quality=qualities, formula_search=args.search_formula,
                    limit=args.limit)

    if args.format == "table":
        _print_table(result)
    else:
        output = {
            "source": "NIST X-ray Photoelectron Spectroscopy Database (SRD 20), Version 5.0",
            "source_url": "https://srdata.nist.gov/xps/",
            "nist_doi": "https://dx.doi.org/10.18434/T4T88K",
            "archive": "KherveDB 2019 snapshot (55,948 records)",
            "archive_doi": "https://github.com/gkerherve/KherveDB",
            "quality_filter": args.quality,
            **result,
        }
        write_output(output, args.format)

    # Always remind about NIST verification for publication
    msg = (
        "---\n"
        "Source: NIST SRD 20 (DOI: 10.18434/T4T88K), via KherveDB 2019 archive.\n"
        "<HARD-GATE> For publication, verify against live NIST database: https://srdata.nist.gov/xps/ </HARD-GATE>"
    )
    print(msg, file=sys.stderr)


def _print_table(result: dict) -> None:
    """Column-aligned human-readable view (stdout = data)."""
    if result.get("summary"):
        records = result["grouped_by_formula"]
        print(f"{'BE mean':<12} {'Quality':<10} {'n':<5} {'Element':<6} {'Line':<8} {'Formula':<25} {'Citation'}")
        print("-" * 120)
        for r in records:
            be_str = f"{r['be_mean']:.2f}±{r['be_std']:.1f}" if r.get('be_std', 0) > 0 else f"{r['be_mean']:.2f}"
            qual = r.get('top_quality', 'N/A')
            author = r.get('top_author', '')
            journal = r.get('top_journal', '')
            cite = f"{author}; {journal}" if author and author != 'N/A' else ''
            print(f"{be_str:<12} {qual:<10} {r['be_count']:<5} {r['Element']:<6} {r['Line']:<8} {r['Formula']:<25} {cite[:50]}")
    else:
        records = result["results"]
        print(f"{'BE (eV)':<10} {'Q':<6} {'Element':<6} {'Line':<8} {'Formula':<22} {'Journal'}")
        print("-" * 110)
        for r in records:
            be = r.get('BE (eV)', '')
            elem = r.get('Element', '')
            line = r.get('Line', '')
            qual = str(r.get('Quality', ''))[:5]
            formula = r.get('Formula', '')[:22]
            journal = str(r.get('Journal', ''))[:60]
            print(f"{be!s:<10} {qual:<6} {elem:<6} {line:<8} {formula:<22} {journal}")


if __name__ == "__main__":
    main()
