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


def _ensure_uv_env() -> None:
    """Transparent env launcher.

    The skill scripts run in the repo-root uv env (.venv/). An agent invoking
    `python scripts/foo.py` with any interpreter is silently re-execed under
    .venv/bin/python so imports (lmfitxps etc.) resolve — no `uv run` needed,
    no path assumptions (works via symlink or real path). Idempotent via the
    SCI_SKILLS_VENV marker so it never re-exec loops.

    Walks up from this file to find a pyproject.toml; the .venv lives next to
    it. If no .venv exists, falls through silently (dev/CI may use another env
    or have deps on PATH).
    """
    if os.environ.get("SCI_SKILLS_VENV") == "1":
        return  # already in the managed env (or chose not to); don't loop

    here = os.path.dirname(os.path.abspath(__file__))
    root = None
    cur = here
    for _ in range(10):  # scripts/ is a few levels under repo root
        if os.path.exists(os.path.join(cur, "pyproject.toml")):
            root = cur
            break
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        cur = parent

    if root is None:
        return  # not running from a checkout; trust whatever env invoked us

    venv_python = os.path.join(root, ".venv", "bin", "python")
    if not os.path.exists(venv_python):
        return  # no managed env; trust the caller's interpreter

    if os.path.abspath(sys.executable) == os.path.abspath(venv_python):
        return  # already the right interpreter

    # Only re-exec for the realistic form: `python <script.py> [args]`. The
    # `-c`/`-m`/stdin forms can't be reconstructed for execv without re-parsing
    # CPython's own argv handling, so skip them — agents invoke scripts as
    # files, and dev tests can use `uv run` or the .venv python directly.
    if not sys.argv or not os.path.exists(sys.argv[0]):
        return

    # Re-exec under the managed env. Preserve argv and cwd.
    os.environ["SCI_SKILLS_VENV"] = "1"
    os.execv(venv_python, [venv_python] + sys.argv)


_ensure_uv_env()

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
