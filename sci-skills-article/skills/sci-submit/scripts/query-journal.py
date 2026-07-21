#!/usr/bin/env python3
"""Query a single journal via EasyScholar API.

Usage:
  python3 query-journal.py "Nature Energy"
  python3 query-journal.py "Advanced Materials" --json

Output (default): human-readable one-liner
Output (--json): machine-readable JSON object

Requires: EASY_SCHOLAR_API_KEY environment variable (already set in ~/.bashrc)
Rate limit: max 2 requests/second. This script makes 1 call — batch scripts handle delays.
"""

import json, os, sys, urllib.request, urllib.parse
from typing import Optional


def query(name: str) -> Optional[dict]:
    key = os.environ.get("EASY_SCHOLAR_API_KEY", "")
    if not key:
        sys.exit("EASY_SCHOLAR_API_KEY not set. Check ~/.bashrc or run: export EASY_SCHOLAR_API_KEY='your-key'")

    q = urllib.parse.quote(name)
    url = f"https://www.easyscholar.cc/open/getPublicationRank?secretKey={key}&publicationName={q}"
    try:
        d = json.loads(urllib.request.urlopen(url, timeout=10).read())
    except Exception as e:
        sys.exit(f"Request failed: {e}")

    if d.get("code") != 200:
        sys.exit(f"API error: {d.get('msg', 'unknown')} (code {d.get('code')})")

    return d["data"]["officialRank"]["all"]


def main():
    if len(sys.argv) < 2:
        sys.exit(f"Usage: {sys.argv[0]} <journal-name> [--json]")

    name = sys.argv[1]
    as_json = "--json" in sys.argv

    data = query(name)

    if as_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(f"{name}")
        print(f"  SCI升级版: {data.get('sciUp', '?')} | 基础版: {data.get('sciBase', '?')} | JCR: {data.get('sci', '?')}")
        print(f"  IF: {data.get('sciif', '?')} | 5年IF: {data.get('sciif5', '?')}")
        print(f"  小类: {data.get('sciUpSmall', '?')} | Top: {data.get('sciUpTop', '无')}")
        print(f"  预警: {data.get('sciwarn', '无')} | EI: {data.get('eii', '无')} | 北大核心: {data.get('pku', '无')}")


if __name__ == "__main__":
    main()
