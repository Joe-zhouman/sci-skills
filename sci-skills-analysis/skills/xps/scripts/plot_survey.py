#!/usr/bin/env python3
"""Plot full survey spectrum for data exploration — quick overview before fitting."""

import sys
import json
import argparse
from _cli import eprint, add_format_arg, load_json


def plot_survey(data: dict, out_path: str, title: str | None = None,
                annotations: list[dict] | None = None) -> str:
    """Plot the full survey spectrum."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    energies = np.array(data["energies"])
    counts = np.array(data["counts"])

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(energies, counts, "k-", linewidth=0.8)
    ax.fill_between(energies, 0, counts, alpha=0.15, color="0.3")
    ax.set_xlim(max(energies), min(energies))
    ax.set_xlabel("Binding Energy (eV)")
    ax.set_ylabel("Counts")

    source = data.get("metadata", {}).get("source", "")
    if title:
        ax.set_title(title, fontsize=12)
    else:
        ax.set_title(f"XPS Survey — {source}", fontsize=12)

    # Annotate expected peak positions
    if annotations:
        for ann in annotations:
            pos = ann.get("position", 0)
            label = ann.get("label", "")
            if min(energies) <= pos <= max(energies):
                ax.axvline(x=pos, color="C44E52", linestyle="--",
                           linewidth=0.6, alpha=0.5)
                y_max = max(counts)
                ax.text(pos, y_max * 0.9, label, fontsize=7, rotation=90,
                        va="top", ha="right", color="#C44E52", alpha=0.7)

    fig.tight_layout(pad=0.3)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out_path


def main():
    parser = argparse.ArgumentParser(
        description="Plot XPS survey spectrum for exploration"
    )
    parser.add_argument("--data", "-d", required=True,
                        help="path to data JSON ({energies, counts, metadata})")
    parser.add_argument("--out", "-o", required=True,
                        help="output image path (.png)")
    parser.add_argument("--title", "-t", default=None,
                        help="plot title")
    add_format_arg(parser)

    args = parser.parse_args()

    data = load_json(args.data, "--data")

    path = plot_survey(data, args.out, args.title)
    print(f"Saved to {path}", file=sys.stderr)


if __name__ == "__main__":
    main()
