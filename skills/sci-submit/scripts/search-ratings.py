#!/usr/bin/env python3
"""Search journal-ratings.json — China CSTEE T1/T2/T3 directory.

Usage:
  python3 search-ratings.py "Nature Communications"           # exact match (case-insensitive)
  python3 search-ratings.py "Nature Communications" --fuzzy   # fuzzy (substring match)
  python3 search-ratings.py "nano research"                   # exact first, fallback to fuzzy
  python3 search-ratings.py --field "材料"                     # list all journals in a field

The script tries exact match first. If no results, falls back to fuzzy (substring).
A journal may appear in multiple fields — that's expected, all results are shown.
"""

import json, sys
from pathlib import Path

RATINGS = Path(__file__).resolve().parent.parent / "data" / "journal-ratings.json"


def load() -> list:
    return json.loads(RATINGS.read_text(encoding="utf-8"))


def exact(query: str, records: list) -> list:
    q = query.strip().lower()
    return [r for r in records if r["journal"].strip().lower() == q]


def fuzzy(query: str, records: list) -> list:
    q = query.strip().lower()
    return [r for r in records if q in r["journal"].lower()]


def by_field(query: str, records: list) -> list:
    q = query.strip().lower()
    return [r for r in records if q in r["field"].lower()]


def normalize_journal_name(name: str) -> str:
    """Normalize ALL CAPS names to Title Case for display."""
    name = name.strip()
    if name == name.upper() and name.isascii() and len(name) > 10:
        # Likely all-caps: title-case it, preserving common mixed-case patterns
        return name.title()
    return name


def show(records: list):
    for r in records:
        name = normalize_journal_name(r["journal"])
        tier = r.get("tier", "?")
        if_val = r.get("if_val")
        if_str = f"IF {if_val}" if if_val and if_val != "None" else ""
        parts = [f"Tier {tier}", name, r["field"]]
        if if_str:
            parts.append(if_str)
        print(" | ".join(parts))


def main():
    if len(sys.argv) < 2:
        sys.exit(f"Usage: {sys.argv[0]} <journal-name> [--fuzzy]\n"
                 f"       {sys.argv[0]} --field <name>")

    records = load()

    if sys.argv[1] == "--field":
        if len(sys.argv) < 3:
            sys.exit("--field requires a field name fragment")
        results = by_field(sys.argv[2], records)
        print(f"Field '{sys.argv[2]}': {len(results)} journals")
        show(results)
        return

    fuzzy_mode = "--fuzzy" in sys.argv
    query = " ".join(a for a in sys.argv[1:] if not a.startswith("--"))

    # Try exact first
    results = exact(query, records)
    if results:
        print(f"{query}: {len(results)} match(es)")
        show(results)
        return

    # Fuzzy fallback
    if not fuzzy_mode:
        print(f"No exact match for '{query}'. Trying fuzzy...", file=sys.stderr)

    results = fuzzy(query, records)
    if results:
        print(f"{query} (fuzzy): {len(results)} match(es)")
        show(results)
    else:
        print(f"No match for '{query}' in {len(records)} records.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
