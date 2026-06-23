"""
sci-draw :: check_figure.py
============================
Pre-submission figure compliance audit.

Per-file checks: format (PDF vector / PNG raster), pixel size/DPI,
PDF font embedding type (must be TrueType/Type 42). Outputs issue list.
Non-destructive — read-only, never modifies files.

Usage
-----
    from check_figure import check_figure, print_report
    issues, info = check_figure("figs/fig1.pdf", min_dpi=300, target_inches=(3.5, 2.625))
    print_report("figs/fig1.pdf", issues, info)

CLI:
    python check_figure.py figs/fig1.pdf figs/fig2.png --min-dpi 300
    python check_figure.py figs/*.pdf --strict   # any FAIL → exit 2
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from typing import Any

SUPPORTED_FORMATS = {"pdf", "png"}

SEVERITY = {"INFO": 0, "WARN": 1, "FAIL": 2}


def _ext(path: str) -> str:
    return os.path.splitext(path)[1].lower().lstrip(".")


def _check_raster(
    path: str, ext: str, min_dpi: int,
    target_inches: tuple[float, float] | None,
) -> tuple[list, dict]:
    """Raster (PNG) compliance check."""
    issues: list[tuple[str, str]] = []
    info: dict[str, Any] = {"category": "raster", "ext": ext}

    try:
        from PIL import Image
    except ImportError:
        issues.append((
            "INFO",
            "Pillow not installed, skipping pixel/DPI check: pip install Pillow",
        ))
        return issues, info

    try:
        img = Image.open(path)
        info["size_px"] = img.size  # (w, h)
        dpi = img.info.get("dpi")
        info["dpi"] = dpi
    except Exception as e:
        issues.append(("FAIL", f"Cannot read image: {e}"))
        return issues, info

    if dpi is None:
        issues.append((
            "WARN",
            "No DPI metadata embedded. Journals compute final size from DPI; "
            "use fig.savefig(dpi=300) to set explicitly.",
        ))
    else:
        dx = dpi[0] if isinstance(dpi, tuple) else dpi
        # PIL roundtrips DPI as float; round to absorb 299.9994 ≈ 300.
        dx_rounded = round(float(dx))
        if dx_rounded < min_dpi:
            issues.append((
                "FAIL",
                f"DPI = {dx_rounded} below required {min_dpi}. "
                "Re-save with fig.savefig(dpi=...).",
            ))
        if target_inches is not None:
            tw, th = target_inches
            actual_w_in = info["size_px"][0] / float(dx)
            actual_h_in = info["size_px"][1] / float(dx)
            tol = 0.1  # inch tolerance
            if abs(actual_w_in - tw) > tol or abs(actual_h_in - th) > tol:
                issues.append((
                    "WARN",
                    f"Actual size ~ {actual_w_in:.2f}x{actual_h_in:.2f} in, "
                    f"target {tw}x{th} in. Set figsize=({tw}, {th}) in code; "
                    "do not rescale in Word/LaTeX.",
                ))
    return issues, info


def _check_pdf_fonts(path: str) -> list[tuple[str, str]]:
    """Check PDF font embedding — journals reject Type 3 (CFF outlines)."""
    issues: list[tuple[str, str]] = []
    try:
        from pypdf import PdfReader
    except ImportError:
        try:
            from PyPDF2 import PdfReader  # noqa: F401
        except ImportError:
            issues.append((
                "INFO",
                "pypdf/PyPDF2 not installed, skipping font embedding check: "
                "pip install pypdf",
            ))
            return issues

    try:
        reader = PdfReader(path)
    except Exception as e:
        issues.append(("WARN", f"Cannot parse PDF for font check: {e}"))
        return issues

    bad_fonts: list[str] = []
    not_embedded: list[str] = []
    for page in reader.pages:
        try:
            resources = page.get("/Resources")
            if not resources:
                continue
            fonts = resources.get("/Font")
            if not fonts:
                continue
            for fname, fobj in fonts.items():
                font = fobj.get_object()
                subtype = str(font.get("/Subtype", ""))
                base = str(font.get("/BaseFont", "?"))
                descriptor = font.get("/FontDescriptor")
                if descriptor:
                    descriptor = descriptor.get_object()
                    embedded = any(
                        k in descriptor
                        for k in ("/FontFile", "/FontFile2", "/FontFile3")
                    )
                else:
                    embedded = False
                if "Type3" in subtype:
                    bad_fonts.append(f"{base} ({subtype})")
                elif not embedded and "Type1" not in subtype:
                    not_embedded.append(base)
        except Exception:
            continue
    if bad_fonts:
        issues.append((
            "FAIL",
            f"PDF contains Type 3 fonts: {', '.join(set(bad_fonts))[:200]}. "
            "Type 3 fonts blur on zoom; many journals reject them. "
            "Set rcParams['pdf.fonttype'] = 42 and re-export.",
        ))
    if not_embedded:
        issues.append((
            "WARN",
            f"Fonts possibly not embedded: {', '.join(set(not_embedded))[:200]}. "
            "Others may see substitute fonts when opening.",
        ))
    return issues


def check_figure(
    path: str,
    min_dpi: int = 300,
    target_inches: tuple[float, float] | None = None,
) -> tuple[list[tuple[str, str]], dict]:
    """
    Audit one figure file. Returns (issues, info).
    issues: [(severity, message), ...]; severity in {INFO, WARN, FAIL}
    info: metadata dict (format, pixels, DPI, etc.)
    """
    issues: list[tuple[str, str]] = []
    info: dict[str, Any] = {"path": path}

    if not os.path.exists(path):
        return [("FAIL", f"File not found: {path}")], info

    ext = _ext(path)
    info["ext"] = ext
    info["size_bytes"] = os.path.getsize(path)

    if ext == "pdf":
        info["category"] = "vector"
        issues.extend(_check_pdf_fonts(path))
    elif ext == "png":
        sub_issues, sub_info = _check_raster(path, ext, min_dpi, target_inches)
        issues.extend(sub_issues)
        info.update(sub_info)
    else:
        issues.append(("WARN", f"Unsupported format: .{ext}. Expected PDF or PNG."))

    return issues, info


def print_report(path: str, issues: list, info: dict) -> str:
    """Print audit results in human-readable format; return overall verdict."""
    print(f"\n--- {path} ---")
    if "category" in info:
        print(
            f"  category: {info['category']}  ext: {info['ext']}  "
            f"size: {info.get('size_bytes', '?')} B"
        )
    if info.get("size_px"):
        print(
            f"  pixels: {info['size_px'][0]}x{info['size_px'][1]}  "
            f"dpi: {info.get('dpi')}"
        )

    if not issues:
        print("  [PASS] No issues found.")
        return "PASS"

    max_sev = max(SEVERITY[s] for s, _ in issues)
    verdict = {2: "FAIL", 1: "WARN", 0: "INFO"}[max_sev]
    for severity, msg in sorted(issues, key=lambda x: -SEVERITY[x[0]]):
        print(f"  [{severity}] {msg}")
    print(f"  >>> verdict: {verdict}")
    return verdict


def _cli() -> int:
    p = argparse.ArgumentParser(description="sci-draw compliance checker")
    p.add_argument("paths", nargs="+", help="figure file paths, glob supported")
    p.add_argument("--min-dpi", type=int, default=300)
    p.add_argument("--width-in", type=float, help="target width (inches)")
    p.add_argument("--height-in", type=float, help="target height (inches)")
    p.add_argument(
        "--strict", action="store_true", help="any FAIL → exit code 2"
    )
    p.add_argument("--format", choices=["pretty", "json"], default="pretty",
                   help="输出格式 (default: pretty)")
    args = p.parse_args()

    target = None
    if args.width_in and args.height_in:
        target = (args.width_in, args.height_in)

    expanded: list[str] = []
    for pat in args.paths:
        m = glob.glob(pat)
        expanded.extend(m if m else [pat])

    any_fail = False
    results = []
    for path in expanded:
        issues, info = check_figure(
            path, min_dpi=args.min_dpi, target_inches=target
        )
        if args.format == "json":
            max_sev = max((SEVERITY[s] for s, _ in issues), default=0)
            results.append({
                "path": path,
                "verdict": {2: "FAIL", 1: "WARN", 0: "INFO"}.get(max_sev, "PASS"),
                "issues": [{"severity": s, "message": m} for s, m in issues],
                "info": {k: v for k, v in info.items() if k != "path"},
            })
            if max_sev >= 2:
                any_fail = True
        else:
            verdict = print_report(path, issues, info)
            if verdict == "FAIL":
                any_fail = True

    if args.format == "json":
        json.dump({"results": results, "any_fail": any_fail},
                  sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
    else:
        print()
        if args.strict and any_fail:
            print("[sci-draw] strict mode: at least one FAIL — exit 2",
                  file=sys.stderr)
    if args.strict and any_fail:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
