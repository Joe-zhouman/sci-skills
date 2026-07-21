#!/usr/bin/env python3
"""Batch query multiple journals via EasyScholar API, output JSON.

Usage:
  python3 query-journals.py "Nature Energy" "Advanced Materials" "ACS Nano"
  python3 query-journals.py --file journals.txt
  python3 query-journals.py "Nature Energy" "Nano Research" --compact

Output: JSON object keyed by journal name.
  --compact: one key per journal, only sciUp + sciif + sciUpTop + sciwarn

Requires: EASY_SCHOLAR_API_KEY environment variable.
Rate limit: sleeps 0.6s between requests (<2/sec).
"""

import json, os, sys, time, urllib.request, urllib.parse


def query(name: str, key: str) -> dict:
    q = urllib.parse.quote(name)
    url = f"https://www.easyscholar.cc/open/getPublicationRank?secretKey={key}&publicationName={q}"
    try:
        d = json.loads(urllib.request.urlopen(url, timeout=10).read())
    except Exception as e:
        return {"error": str(e)}

    if d.get("code") != 200:
        return {"error": d.get("msg", "unknown")}

    return d["data"]["officialRank"]["all"]


def main():
    key = os.environ.get("EASY_SCHOLAR_API_KEY", "")
    if not key:
        sys.exit("EASY_SCHOLAR_API_KEY not set.")

    compact = "--compact" in sys.argv
    file_mode = "--file" in sys.argv

    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    journals = []

    if file_mode:
        if not args:
            sys.exit("--file requires a path: python3 query-journals.py --file journals.txt")
        journals = [line.strip() for line in open(args[0]) if line.strip()]
    else:
        journals = args

    if not journals:
        sys.exit("No journal names provided.")

    result = {}
    for name in journals:
        data = query(name, key)
        if compact and "error" not in data:
            result[name] = {
                "sci_up": data.get("sciUp"),
                "if": data.get("sciif"),
                "top": data.get("sciUpTop"),
                "warn": data.get("sciwarn"),
            }
        else:
            result[name] = data
        time.sleep(0.6)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
