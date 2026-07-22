"""
Shared CLI boilerplate for XPS scripts.

Agent-friendly conventions (#5):
  - --format json|pretty (json default when stdout is not a TTY)
  - Structured error envelope on stderr
  - stdout = data only
"""

import sys
import json
import argparse
import os
from typing import Any

# A downstream consumer closing the pipe (e.g. `... | head`) is normal —
# exit silently on SIGPIPE/BrokenPipeError instead of dumping a traceback.
try:
    import signal
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
except (AttributeError, ValueError):
    # Windows has no SIGPIPE; fine.
    pass


def eprint(obj: dict) -> None:
    """Write a structured error envelope to stderr."""
    json.dump(obj, sys.stderr, ensure_ascii=False)
    sys.stderr.write("\n")


def die(obj: dict) -> None:
    """Write a structured error envelope to stderr and exit(1)."""
    eprint(obj)
    sys.exit(1)


def load_json(path: str, param: str = "--data") -> Any:
    """Load JSON from path with a structured error envelope on failure.

    Guards the hottest failure path (missing/unreadable input) so agents get a
    typed envelope instead of a raw Python traceback.
    """
    if not os.path.exists(path):
        die({
            "type": "io_error", "subtype": "file_not_found",
            "param": param, "message": f"file not found: {path}",
            "hint": "check the path, or run an earlier stage of the pipeline first",
        })
    try:
        with open(path) as f:
            return json.load(f)
    except json.JSONDecodeError as exc:
        die({
            "type": "io_error", "subtype": "parse_failed",
            "param": param, "message": f"invalid JSON in {path}: {exc.msg}",
            "hint": "re-run the pipeline stage that produced this file",
        })


def write_output(data: Any, fmt: str) -> None:
    """Write output to stdout in the requested format."""
    try:
        if fmt == "json":
            json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
            sys.stdout.write("\n")
        elif fmt == "pretty":
            if isinstance(data, dict):
                _pretty_dict(data)
            elif isinstance(data, list):
                for item in data:
                    print(item)
            else:
                print(data)
        else:
            eprint({
                "type": "cli_error",
                "subtype": "invalid_format",
                "param": "--format",
                "message": f"unsupported format: {fmt}",
                "hint": "use --format json or --format pretty"
            })
            sys.exit(1)
    except BrokenPipeError:
        # Downstream consumer closed the pipe (e.g. `| head`); exit quietly.
        sys.exit(0)


def _pretty_dict(d: dict, indent: int = 0) -> None:
    prefix = "  " * indent
    for k, v in d.items():
        if isinstance(v, dict):
            print(f"{prefix}{k}:")
            _pretty_dict(v, indent + 1)
        elif isinstance(v, list) and len(v) > 20:
            print(f"{prefix}{k}: [{len(v)} items]")
        elif isinstance(v, float):
            print(f"{prefix}{k}: {v:.6g}")
        else:
            print(f"{prefix}{k}: {v}")


def add_format_arg(parser: argparse.ArgumentParser) -> None:
    is_tty = sys.stdout.isatty()
    parser.add_argument(
        "--format", choices=["json", "pretty"],
        default="pretty" if is_tty else "json",
        help="output format (default: pretty for TTY, json for pipe)"
    )
