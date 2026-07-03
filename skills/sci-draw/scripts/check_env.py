"""
sci-draw :: check_env.py
=========================
Verify Python version and required packages for sci-draw.

Checks Python >= 3.11 and all required packages. On failure, prints
conda/uv environment creation commands.

Usage
-----
    python scripts/check_env.py                    # check current Python
    python scripts/check_env.py --python /usr/bin/python3.12
    python scripts/check_env.py --format json      # machine-readable output
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from importlib.metadata import version as pkg_version


def _version_ok(actual: str, minimum: str) -> bool:
    """Compare two version strings without third-party libraries."""
    a = tuple(int(x) for x in actual.split("."))
    b = tuple(int(x) for x in minimum.split("."))
    return a >= b


REQUIRED = {
    "matplotlib": "3.7",
    "seaborn": "0.13",
    "Pillow": "10.0",
    "numpy": "1.24",
    "pandas": "2.0",
    "scipy": "1.10",
}
MIN_PYTHON = "3.11"


def _python_version(python_path: str) -> str:
    """Get Python version string from a given interpreter."""
    r = subprocess.run(
        [python_path, "-c", "import sys; print(sys.version)"],
        capture_output=True, text=True, timeout=15,
    )
    if r.returncode != 0:
        raise RuntimeError(f"Failed to run {python_path}: {r.stderr.strip()}")
    return r.stdout.strip().split()[0]


def _check_package(name: str, min_version: str) -> dict:
    try:
        v = pkg_version(name)
        ok = _version_ok(v, min_version)
        return {"name": name, "version": v, "required": min_version, "ok": ok}
    except Exception:
        return {"name": name, "version": None, "required": min_version, "ok": False}


def check(python_path: str | None = None) -> dict:
    """
    Check a Python interpreter and its installed packages.

    Returns a dict with keys: python_path, python_version, python_ok,
    packages, all_ok, fix_hint.
    """
    py = python_path or sys.executable

    try:
        pv = _python_version(py)
        py_ok = _version_ok(pv, MIN_PYTHON)
    except RuntimeError as e:
        return {
            "python_path": py,
            "python_version": None,
            "python_ok": False,
            "packages": [],
            "all_ok": False,
            "error": str(e),
            "fix_hint": f"The Python at {py} could not be run. Check the path.",
        }

    pkgs = [_check_package(n, v) for n, v in REQUIRED.items()]
    all_ok = py_ok and all(p["ok"] for p in pkgs)

    result = {
        "python_path": py,
        "python_version": pv,
        "python_ok": py_ok,
        "packages": pkgs,
        "all_ok": all_ok,
    }

    if not all_ok:
        missing = [p["name"] for p in pkgs if not p["ok"]]
        result["fix_hint"] = _build_fix_hint(py_ok, missing)

    return result


def _build_fix_hint(py_ok: bool, missing: list[str]) -> str:
    """Build environment creation commands."""
    pkgs = " ".join(missing)
    lines = []
    lines.append(f"Missing or outdated packages: {', '.join(missing)}")
    lines.append("")
    lines.append("Create a new environment (choose one):")
    lines.append("")
    lines.append("  # conda:")
    lines.append(f"  conda create -n sci-draw python={MIN_PYTHON} {pkgs} -y")
    lines.append("  conda activate sci-draw")
    lines.append("")
    lines.append("  # uv:")
    lines.append("  uv venv --python 3.11")
    lines.append("  source .venv/bin/activate")
    lines.append(f"  uv pip install {pkgs}")
    return "\n".join(lines)


def format_pretty(result: dict) -> str:
    lines = []
    lines.append(f"Python: {result.get('python_path', '?')}")
    lines.append(f"  version: {result.get('python_version', 'unknown')} "
                 f"({'OK' if result.get('python_ok') else 'FAIL — need >= ' + MIN_PYTHON})")
    lines.append("")
    for p in result.get("packages", []):
        status = "OK" if p["ok"] else "FAIL"
        ver = p["version"] or "missing"
        lines.append(f"  {p['name']}: {ver} (need >= {p['required']}) {status}")
    lines.append("")
    if result.get("all_ok"):
        lines.append("All checks passed.")
    else:
        lines.append(result.get("fix_hint", "Some checks failed."))
    lines.append("")
    return "\n".join(lines)


def _cli() -> int:
    p = argparse.ArgumentParser(description="sci-draw environment checker")
    p.add_argument("--python", help="Path to Python interpreter (default: current)")
    p.add_argument("--format", choices=["pretty", "json"], default="pretty")
    args = p.parse_args()

    result = check(args.python)
    if args.format == "json":
        json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        print(format_pretty(result))
    return 0 if result["all_ok"] else 1


if __name__ == "__main__":
    sys.exit(_cli())
