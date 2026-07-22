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
"""

import sys
import json
import argparse
import os
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
            'Charge Reference', 'Author', 'Journal']
    available = [c for c in cols if c in result.columns]
    return {
        "summary": False,
        "count": len(result),
        "results": result[available].to_dict(orient='records'),
    }


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
                        help="include all columns in JSON output")

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
