#!/usr/bin/env python3
"""
Manage the XPS analysis working directory + state.json.

The workdir is fixed at <cwd>/sci-skills/sci-analysis/xps/ — created on init,
read by every session thereafter. state.json is the only reliable carrier of
analysis context across sessions (context clears; files don't).

Subcommands:
  init          Create the workdir tree + an empty state.json (idempotent).
  status        Read state.json and report what's done / in-progress / missing.
  add-evidence  Copy an external file into evidence/ and append to state.evidence.
  set-region    Create a region subdir and/or advance its status
                (explored → fitting → done).
  set-rsf       Record RSF source for atom% quantification (user / scofield).

report.md is NOT generated here — that's narrative, the LLM's job per
references/report-template.md. This script only keeps the structured state
honest so the LLM doesn't hand-edit JSON.

All mutations are atomic (write temp, rename) so a crash mid-write can't
corrupt state.json.
"""

import sys
import json
import argparse
import os
import shutil
from datetime import date
from _cli import eprint, die, write_output, add_format_arg


# Fixed workdir relative to the agent's cwd.
WORKDIR = os.path.join("sci-skills", "sci-analysis", "xps")
STATE_FILE = os.path.join(WORKDIR, "state.json")
EVIDENCE_DIR = os.path.join(WORKDIR, "evidence")

# region status state machine — enforced on set-region
STATUS_ORDER = ["explored", "fitting", "done"]


def _empty_state() -> dict:
    return {
        "claim": "",
        "instrument": "",
        "pass_energy": None,
        "created": date.today().isoformat(),
        "updated": date.today().isoformat(),
        "rsf": None,
        "evidence": [],
        "regions": [],
        "comparisons": [],
    }


def _load_state() -> dict:
    """Load state.json or die with a typed envelope."""
    if not os.path.exists(STATE_FILE):
        die({
            "type": "io_error", "subtype": "state_not_initialized",
            "param": "state.json",
            "message": f"workdir not found: {WORKDIR}",
            "hint": f"run `state.py init` first (creates {WORKDIR}/ + state.json)",
        })
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except json.JSONDecodeError as exc:
        die({
            "type": "io_error", "subtype": "parse_failed",
            "param": "state.json",
            "message": f"invalid JSON in {STATE_FILE}: {exc.msg}",
            "hint": "fix state.json by hand or re-init (init is idempotent and "
                    "won't overwrite an existing state.json)",
        })


def _save_state(state: dict) -> None:
    """Atomic write: temp file + rename, so a crash can't corrupt state.json."""
    state["updated"] = date.today().isoformat()
    tmp = STATE_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    os.replace(tmp, STATE_FILE)


# ---------------------------------------------------------------- subcommands

def cmd_init(args) -> dict:
    """Create workdir tree + empty state.json. Idempotent."""
    created = []
    if not os.path.exists(WORKDIR):
        os.makedirs(WORKDIR)
        created.append(WORKDIR)
    if not os.path.exists(EVIDENCE_DIR):
        os.makedirs(EVIDENCE_DIR)
        created.append(EVIDENCE_DIR)

    if os.path.exists(STATE_FILE):
        return {
            "action": "init",
            "workdir": WORKDIR,
            "state_existed": True,
            "created": created,
            "note": "state.json already present — left untouched (init is idempotent)",
        }

    state = _empty_state()
    _save_state(state)
    created.append(STATE_FILE)
    return {
        "action": "init",
        "workdir": WORKDIR,
        "state_existed": False,
        "created": created,
        "state": state,
    }


def cmd_status(args) -> dict:
    """Read state.json and summarize progress."""
    state = _load_state()
    regions = state.get("regions", [])
    by_status = {s: [] for s in STATUS_ORDER}
    for r in regions:
        s = r.get("status", "?")
        by_status.setdefault(s, []).append(r.get("label", "?"))

    return {
        "action": "status",
        "workdir": WORKDIR,
        "claim": state.get("claim", "") or "(not set)",
        "instrument": state.get("instrument", "") or "(not set)",
        "pass_energy": state.get("pass_energy"),
        "rsf": _summarize_rsf(state.get("rsf")),
        "n_evidence": len(state.get("evidence", [])),
        "evidence_techniques": [e.get("technique", "?")
                                 for e in state.get("evidence", [])],
        "regions_by_status": {s: by_status.get(s, []) for s in STATUS_ORDER},
        "comparisons": [c.get("label", "?")
                        for c in state.get("comparisons", [])],
        "next_steps": _suggest_next(state),
    }


def _suggest_next(state: dict) -> list[str]:
    """Heuristic: what's missing? Non-prescriptive — the LLM decides."""
    steps = []
    if not state.get("claim"):
        steps.append("claim not set — ask the user what XPS should prove (Step 0)")
    if not state.get("instrument"):
        steps.append("instrument not set — ask: what instrument model, what X-ray source (Al/Mg), what pass energy? (Step 0)")
    if not state.get("rsf"):
        steps.append("RSF not set — ask the user if they have instrument RSF table; if not, fall back to Scofield (Step 0)")
    regions = state.get("regions", [])
    if not regions:
        steps.append("no regions loaded — load data + run find_peaks (Phase 1)")
    for r in regions:
        if r.get("status") == "explored":
            steps.append(f"{r.get('label','?')}: ready to fit (set-region <label> fitting)")
        if r.get("status") == "fitting":
            steps.append(f"{r.get('label','?')}: fitting in progress — finalize or iterate")
    if regions and all(r.get("status") == "done" for r in regions):
        steps.append("all regions done — generate report.md (Phase 3)")
    return steps


def _summarize_rsf(rsf: dict | None) -> dict:
    if not rsf:
        return {"status": "not_set"}
    return {
        "status": rsf.get("source", "?"),
        "source": rsf.get("source", "?"),
        "file": rsf.get("file"),
        "notes": rsf.get("notes", ""),
    }


def cmd_set_rsf(args) -> dict:
    """Record RSF source in state.json."""
    state = _load_state()
    rsf = {"source": args.source, "file": None, "notes": args.notes or ""}

    if args.file:
        src = args.file
        if not os.path.exists(src):
            die({
                "type": "io_error", "subtype": "file_not_found",
                "param": "file",
                "message": f"RSF file not found: {src}",
                "hint": "check the path",
            })
        # copy RSF file into workdir for persistence
        rsf_dir = os.path.join(WORKDIR, "user_rsf")
        if not os.path.exists(rsf_dir):
            os.makedirs(rsf_dir)
        name = os.path.basename(src)
        dest = os.path.join(rsf_dir, name)
        if os.path.abspath(src) != os.path.abspath(dest):
            shutil.copy2(src, dest)
        rsf["file"] = os.path.relpath(dest, WORKDIR)

    state["rsf"] = rsf
    _save_state(state)
    return {"action": "set-rsf", "rsf": state["rsf"]}


def cmd_set_meta(args) -> dict:
    """Record instrument metadata in state.json."""
    state = _load_state()
    if args.instrument is not None:
        state["instrument"] = args.instrument
    if args.pass_energy is not None:
        state["pass_energy"] = args.pass_energy
    _save_state(state)
    return {
        "action": "set-meta",
        "instrument": state.get("instrument", ""),
        "pass_energy": state.get("pass_energy"),
    }


def cmd_add_evidence(args) -> dict:
    """Copy a file into evidence/ and append to state.evidence."""
    state = _load_state()
    src = args.file
    if not os.path.exists(src):
        die({
            "type": "io_error", "subtype": "file_not_found",
            "param": "file",
            "message": f"evidence file not found: {src}",
            "hint": "check the path — the file is copied into evidence/, "
                    "the original path won't be relied on later",
        })

    # meaningful name: prefer --name, else use the file's basename (never IMG_001
    # if the user gave a good name; if they didn't, that's on them)
    name = args.name or os.path.basename(src)
    dest = os.path.join(EVIDENCE_DIR, name)
    if os.path.abspath(src) != os.path.abspath(dest):
        shutil.copy2(src, dest)

    entry = {
        "technique": args.technique or "",
        "description": args.description or "",
        "source_file": os.path.join("evidence", name),
        "added": date.today().isoformat(),
    }
    state.setdefault("evidence", []).append(entry)
    _save_state(state)

    return {
        "action": "add-evidence",
        "copied_to": dest,
        "entry": entry,
        "n_evidence": len(state["evidence"]),
    }


def cmd_set_region(args) -> dict:
    """Create a region subdir and/or advance its status."""
    state = _load_state()
    label = args.label
    region_dir = os.path.join(WORKDIR, args.dir) if args.dir else os.path.join(WORKDIR, label)
    created_dir = False

    # find or create the region record
    regions = state.setdefault("regions", [])
    rec = next((r for r in regions if r.get("label") == label), None)

    if args.status:
        if args.status not in STATUS_ORDER:
            die({
                "type": "validation_error", "subtype": "invalid_status",
                "param": "--status",
                "message": f"status must be one of {STATUS_ORDER}, got {args.status!r}",
                "hint": f"status machine: {' → '.join(STATUS_ORDER)}",
            })
        # enforce ordering: can't go backwards unless --force
        if rec and rec.get("status"):
            cur = STATUS_ORDER.index(rec["status"])
            new = STATUS_ORDER.index(args.status)
            if new < cur and not args.force:
                die({
                    "type": "validation_error", "subtype": "status_regression",
                    "param": "--status",
                    "message": f"{label}: {rec['status']} → {args.status} is backwards",
                    "hint": "status only advances (explored→fitting→done); "
                            "use --force to override (e.g. re-open a done region)",
                })

    if rec is None:
        rec = {"label": label, "status": "explored", "dir": os.path.relpath(region_dir, WORKDIR)}
        regions.append(rec)

    # create the subdir
    if not os.path.exists(region_dir):
        os.makedirs(region_dir)
        created_dir = True

    if args.sub_claim:
        rec["sub_claim"] = args.sub_claim
    if args.data_source:
        rec["data_source"] = args.data_source
    if args.status:
        rec["status"] = args.status
    rec["dir"] = os.path.relpath(region_dir, WORKDIR)

    _save_state(state)

    return {
        "action": "set-region",
        "label": label,
        "region_dir": region_dir,
        "created_dir": created_dir,
        "status": rec["status"],
        "record": rec,
    }


# ---------------------------------------------------------------- main

def main():
    parser = argparse.ArgumentParser(
        description="Manage the XPS workdir + state.json (init/status/add-evidence/set-region)"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="create workdir + empty state.json")
    p_init.set_defaults(func=cmd_init)
    add_format_arg(p_init)

    p_status = sub.add_parser("status", help="report current progress")
    p_status.set_defaults(func=cmd_status)
    add_format_arg(p_status)

    p_ev = sub.add_parser("add-evidence", help="copy a file into evidence/ + append to state")
    p_ev.add_argument("file", help="path to the evidence file (image, spectrum, etc.)")
    p_ev.add_argument("--technique", "-t", default=None,
                      help="e.g. XRD, TEM, Raman, EDS")
    p_ev.add_argument("--description", "-d", default=None,
                      help="what this evidence shows")
    p_ev.add_argument("--name", "-n", default=None,
                      help="meaningful filename in evidence/ (default: original basename)")
    p_ev.set_defaults(func=cmd_add_evidence)
    add_format_arg(p_ev)

    p_reg = sub.add_parser("set-region", help="create/advance a region subdir + status")
    p_reg.add_argument("label", help="region label, e.g. 'Si 2p'")
    p_reg.add_argument("--status", "-s", default=None, choices=STATUS_ORDER,
                       help="set status (explored→fitting→done)")
    p_reg.add_argument("--dir", default=None,
                       help="subdir name (default: derived from label)")
    p_reg.add_argument("--sub-claim", default=None, help="what this region proves")
    p_reg.add_argument("--data-source", default=None, help="origin of the raw data")
    p_reg.add_argument("--force", action="store_true",
                       help="allow status regression (e.g. re-open a done region)")
    p_reg.set_defaults(func=cmd_set_region)
    add_format_arg(p_reg)

    p_rsf = sub.add_parser("set-rsf", help="record RSF source for atom% quantification")
    p_rsf.add_argument("--source", "-s", required=True,
                       choices=["user", "scofield"],
                       help="RSF source: 'user' for instrument-provided, 'scofield' for theoretical fallback")
    p_rsf.add_argument("--file", "-f", default=None,
                       help="path to user-provided RSF table (copied into workdir)")
    p_rsf.add_argument("--notes", default=None,
                       help="e.g. 'Thermo Avantage default RSF for K-Alpha'")
    p_rsf.set_defaults(func=cmd_set_rsf)
    add_format_arg(p_rsf)

    p_meta = sub.add_parser("set-meta", help="record instrument metadata")
    p_meta.add_argument("--instrument", default=None,
                        help="instrument model + X-ray source, e.g. 'Thermo K-Alpha, Al Kα (mono)'")
    p_meta.add_argument("--pass-energy", type=float, default=None,
                        help="analyzer pass energy in eV, e.g. 50")
    p_meta.set_defaults(func=cmd_set_meta)
    add_format_arg(p_meta)

    args = parser.parse_args()
    result = args.func(args)
    write_output(result, args.format)


if __name__ == "__main__":
    main()
