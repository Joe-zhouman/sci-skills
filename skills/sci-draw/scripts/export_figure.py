"""
sci-draw :: export_figure.py
=============================
Unified figure export — PDF (vector) + PNG (raster) at exact final size.

- PDF: vector, lossless, editable text (TrueType fonttype 42). Primary format.
- PNG: raster at user-specified DPI (default 300). For manuscripts that require
  raster or for AI visual review.
- Optional grayscale preview to sanity-check colorblind safety.

Usage
-----
    from export_figure import export_figure
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.plot([0,1,2],[3,1,4])

    paths = export_figure(
        fig,
        basename="figs/fig1_main",
        formats=["pdf", "png"],
        size_inches=(3.5, 2.625),   # Nature single-column
        dpi=300,
        grayscale_preview=True,
    )
    # -> ['figs/fig1_main.pdf', 'figs/fig1_main.png', 'figs/fig1_main_grayscale.png']

CLI: ``python export_figure.py demo``  generate a demo figure and export.
"""
from __future__ import annotations

import argparse
import os
import sys
from typing import Iterable

import matplotlib.pyplot as plt


SUPPORTED_FORMATS = {"pdf", "png"}


def _ensure_parent(path: str) -> None:
    parent = os.path.dirname(os.path.abspath(path))
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)


def export_figure(
    fig,
    basename: str,
    formats: Iterable[str] | None = None,
    dpi: int = 300,
    size_inches: tuple[float, float] | None = None,
    grayscale_preview: bool = False,
    tight: bool = True,
    pad_inches: float = 0.05,
    transparent: bool = False,
) -> list[str]:
    """
    Export a matplotlib Figure to PDF and/or PNG at exact final size.

    Args:
        fig: matplotlib Figure object.
        basename: output path prefix (no extension); subdirectories created automatically.
        formats: list of extensions, e.g. ['pdf', 'png']. Default: ['pdf', 'png'].
        dpi: raster resolution for PNG; 300 (standard) or 600 (IEEE/high-res).
        size_inches: (width, height) in inches. If given, forces fig.set_size_inches()
            before saving — strongly recommended to avoid post-export rescaling.
        grayscale_preview: also generate a _grayscale.png for colorblind safety check.
        tight: use bbox_inches='tight' (trim whitespace).
        pad_inches: padding when tight=True.
        transparent: transparent background (useful for slides/posters).

    Returns:
        List of file paths actually written.
    """
    if formats is None:
        formats = ("pdf", "png")
    formats = [f.lower().lstrip(".") for f in formats]
    unknown = [f for f in formats if f not in SUPPORTED_FORMATS]
    if unknown:
        raise ValueError(
            f"Unsupported formats: {unknown}. Supported: {sorted(SUPPORTED_FORMATS)}"
        )

    if size_inches is not None:
        if len(size_inches) != 2:
            raise ValueError("size_inches must be (width, height)")
        fig.set_size_inches(*size_inches)

    # Embed TrueType fonts (fonttype 42); journals reject Type-3 PDFs.
    plt.rcParams["pdf.fonttype"] = 42
    plt.rcParams["ps.fonttype"] = 42
    plt.rcParams["svg.fonttype"] = "none"

    saved: list[str] = []
    for fmt in formats:
        path = f"{basename}.{fmt}"
        _ensure_parent(path)
        kwargs: dict = {
            "bbox_inches": "tight" if tight else None,
            "pad_inches": pad_inches,
            "transparent": transparent,
        }
        if fmt == "png":
            kwargs["dpi"] = dpi
        fig.savefig(path, **kwargs)
        saved.append(path)
        print(f"[sci-draw] wrote {path}", file=sys.stderr)

    if grayscale_preview:
        gray_path = _grayscale_from(fig, basename, dpi=dpi)
        if gray_path:
            saved.append(gray_path)
    return saved


def _grayscale_from(fig, basename: str, dpi: int) -> str | None:
    """
    Export a grayscale preview for colorblind safety check.
    Uses PIL if available; otherwise skips with a message.
    """
    try:
        from PIL import Image
    except ImportError:
        print(
            "[sci-draw] Pillow not available; grayscale preview skipped.",
            file=sys.stderr,
        )
        return None

    png_path = f"{basename}.png"
    _ensure_parent(png_path)
    fig.savefig(png_path, dpi=dpi, bbox_inches="tight")

    gray_path = f"{basename}_grayscale.png"
    Image.open(png_path).convert("L").save(gray_path)
    print(f"[sci-draw] wrote {gray_path} (grayscale preview)", file=sys.stderr)
    return gray_path


def _demo(out_basename: str) -> None:
    """Generate a small demo figure for quick smoke testing."""
    import numpy as np

    rng = np.random.default_rng(7)
    x = np.linspace(0, 10, 50)
    y1 = np.sin(x) + rng.normal(0, 0.1, x.size)
    y2 = np.cos(x) + rng.normal(0, 0.1, x.size)

    fig, ax = plt.subplots(figsize=(3.5, 2.625))
    ax.plot(x, y1, label="sin", marker="o", markersize=3)
    ax.plot(x, y2, label="cos", marker="s", markersize=3, linestyle="--")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend(frameon=False)

    paths = export_figure(
        fig,
        out_basename,
        formats=["pdf", "png"],
        size_inches=(3.5, 2.625),
        dpi=300,
        grayscale_preview=True,
    )
    print("\nDemo done. Files:", file=sys.stderr)
    for p in paths:
        print(f"  {p}", file=sys.stderr)


def _cli() -> int:
    p = argparse.ArgumentParser(description="sci-draw figure exporter")
    p.add_argument(
        "cmd", choices=["demo"], help="`demo`: generate a demo figure and export"
    )
    p.add_argument(
        "--out", default="./sci_draw_demo", help="output basename (default ./sci_draw_demo)"
    )
    args = p.parse_args()
    if args.cmd == "demo":
        _demo(args.out)
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
