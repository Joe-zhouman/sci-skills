#!/usr/bin/env python3
"""scan_neighbor.py — 感知一轮修回的 grounding 文件,报告就绪状态。

哲学(同 sci-write/scan_neighbor.py):读邻居、不编排邻居、不假设文件从哪来。
本脚本扫一轮 revision 用到的全部 grounding 来源,报告每个文件在不在、
契约字段齐不齐。纯只读、无副作用——不改任何文件(改由 SKILL.md 流程
在人确认后做)。

grounding 来源(解耦:只看文件存在 + 契约字段,不问谁产的):
  - manuscript/rN/reviews/     审稿意见原文
  - manuscript/rN/tex/         被修回的稿(及 v1/r1/... 轮次识别)
  - sci-skills/sci-write/      写作笔记(claim/paper-plan/figN-reading/terminology-ledger)
  - sci-skills/sci-draw/       figN-report.md(图证据 + 统计)
  - sci-skills/sci-revise/     issue-ledger.md / change-log.md(过程状态)

用法:
    python scripts/scan_neighbor.py              # 默认从 cwd 推断项目根
    python scripts/scan_neighbor.py /abs/project # 给项目根绝对路径(便于测试)

项目根推断:从 cwd 往上找,第一个同时含 manuscript/ 和 sci-skills/ 的目录。
找不到则把 cwd 当项目根(后续扫描会报告文件不存在)。

退出码:0 总是(报告型工具,不因"有缺"而失败)。
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


# ---- 项目根推断 ----

def find_project_root(start: Path | None = None) -> Path:
    """从 start(默认 cwd)往上找,第一个同时含 manuscript/ 和 sci-skills/ 的目录。
    找不到返回 start / cwd 本身(让后续扫描自然报告"不存在")。
    """
    p = (start or Path.cwd()).resolve()
    for cand in [p, *p.parents]:
        if (cand / "manuscript").is_dir() and (cand / "sci-skills").is_dir():
            return cand
    return p


# ---- 当前修回轮次识别 ----

def current_round(root: Path) -> dict:
    """识别当前是哪一轮修回。优先最新的 rN,没有 rN 则提示 v1(首投后等意见)。
    返回 {round, path, exists, available_rounds}。
    """
    ms = root / "manuscript"
    rounds: list[str] = []
    if ms.exists():
        rounds = sorted(
            d.name for d in ms.iterdir()
            if d.is_dir() and re.match(r"^r\d+$", d.name)
        )
    v1 = ms / "v1"
    if rounds:
        latest = rounds[-1]  # r1 < r2 < ... 字典序对 rN 成立
        rp = ms / latest
        return {
            "round": latest,
            "path": str(rp),
            "exists": True,
            "available_rounds": rounds,
            "v1_exists": v1.exists(),
        }
    return {
        "round": None,
        "path": None,
        "exists": False,
        "available_rounds": [],
        "v1_exists": v1.exists(),
    }


# ---- 各来源扫描 ----

def _check_file(path: Path) -> dict:
    """单文件就绪状态。"""
    return {
        "path": str(path),
        "exists": path.exists(),
        "size": path.stat().st_size if path.exists() else 0,
    }


def scan_reviews(root: Path, rnd: dict) -> dict:
    """扫 manuscript/<round>/reviews/ 下的审稿意见文件。"""
    if not rnd["exists"]:
        return {"dir": None, "files": [], "note": "no revision round yet"}
    rdir = Path(rnd["path"]) / "reviews"
    files = []
    if rdir.exists():
        for p in sorted(rdir.iterdir()):
            if p.is_file():
                info = _check_file(p)
                info["name"] = p.name
                files.append(info)
    return {
        "dir": str(rdir),
        "exists": rdir.exists(),
        "files": files,
        "note": "" if files else "reviews/ empty or missing — ask the author for the reviewer comments",
    }


def scan_manuscript_tex(root: Path, rnd: dict) -> dict:
    """扫 manuscript/<round>/tex/(被修回的稿)。rN 不存在则 fallback 到 v1。"""
    target = Path(rnd["path"]) / "tex" if rnd["exists"] else root / "manuscript" / "v1" / "tex"
    sections = target / "sections"
    main_tex = target / "main.tex"
    return {
        "tex_dir": str(target),
        "exists": target.exists(),
        "main_tex": _check_file(main_tex),
        "sections_dir": {
            "path": str(sections),
            "exists": sections.exists(),
            "files": sorted(p.name for p in sections.iterdir() if p.is_file())
                     if sections.exists() else [],
        },
        "note": "" if target.exists() else "manuscript tex not found — confirm the round directory",
    }


# sci-write 笔记契约:这些文件记录原稿思路,revision 时读它们理解 claim/证据
SCI_WRITE_NOTES = ["claim.md", "paper-plan.md", "terminology-ledger.md"]


def scan_sci_write(root: Path) -> dict:
    """扫 sci-skills/sci-write/ 的写作笔记 + figN-reading.md。"""
    wdir = root / "sci-skills" / "sci-write"
    notes = {name: _check_file(wdir / name) for name in SCI_WRITE_NOTES}
    # figN-reading.md 是动态命名
    readings = []
    if wdir.exists():
        readings = sorted(p.name for p in wdir.glob("fig*-reading.md"))
    return {
        "dir": str(wdir),
        "exists": wdir.exists(),
        "notes": notes,
        "fig_readings": readings,
        "note": "" if wdir.exists() else
                "sci-skills/sci-write/ not found — paper may not have been drafted through sci-write; "
                "claim boundary must then be inferred from the manuscript (weaker)",
    }


def scan_sci_draw(root: Path) -> dict:
    """扫 sci-skills/sci-draw/ 的 figN-report.md(图证据 + 统计)。"""
    ddir = root / "sci-skills" / "sci-draw"
    reports = []
    if ddir.exists():
        reports = sorted(p.name for p in ddir.glob("*-report.md"))
    return {
        "dir": str(ddir),
        "exists": ddir.exists(),
        "reports": reports,
        "note": "" if reports else
                "no figN-report.md — no figure evidence available for data-backed defenses",
    }


def scan_sci_revise(root: Path) -> dict:
    """扫 sci-skills/sci-revise/ 的过程状态(issue-ledger / change-log)。"""
    rdir = root / "sci-skills" / "sci-revise"
    return {
        "dir": str(rdir),
        "exists": rdir.exists(),
        "issue_ledger": _check_file(rdir / "issue-ledger.md"),
        "change_log": _check_file(rdir / "change-log.md"),
        "polish_todo": _check_file(rdir / "polish-todo.md"),
        "note": "" if rdir.exists() else
                "sci-skills/sci-revise/ not found — first run of this round; "
                "issue-ledger.md will be created during intake",
    }


# ---- issue-ledger 契约字段检查(轻量) ----

LEDGER_REQUIRED_FIELDS = [
    "reviewer", "surface_comment", "underlying_concern", "stance",
    "evidence_anchors", "safe_claim_boundary", "revision_kind",
]


def check_issue_ledger(root: Path) -> dict:
    """解析 issue-ledger.md,报告每条 issue 的必填字段齐不齐 + solution_order 依赖一致性。
    轻量正则解析,不追求完整 markdown AST。
    """
    ledger = root / "sci-skills" / "sci-revise" / "issue-ledger.md"
    if not ledger.exists():
        return {"exists": False, "issues": [], "note": "no issue-ledger.md yet"}

    text = ledger.read_text(encoding="utf-8")
    # 每个 issue block: ## R1-Q03
    blocks = re.split(r"^##\s+(\S+)\s*$", text, flags=re.MULTILINE)
    issues = []
    for i in range(1, len(blocks), 2):
        issue_id = blocks[i].strip()
        body = blocks[i + 1] if i + 1 < len(blocks) else ""
        present = {f: bool(re.search(rf"^- {re.escape(f)}:\s*\S", body, re.MULTILINE))
                   for f in LEDGER_REQUIRED_FIELDS}
        missing = [f for f, ok in present.items() if not ok]
        # depends_on / solution_order
        dep_m = re.search(r"^- depends_on:\s*(\S+)", body, re.MULTILINE)
        order_m = re.search(r"^- solution_order:\s*(\d+)", body, re.MULTILINE)
        issues.append({
            "id": issue_id,
            "missing_fields": missing,
            "depends_on": dep_m.group(1) if dep_m else None,
            "solution_order": int(order_m.group(1)) if order_m else None,
        })
    return {
        "exists": True,
        "issues": issues,
        "count": len(issues),
        "incomplete": sum(1 for x in issues if x["missing_fields"]),
        "note": "" if issues else "ledger exists but no issue blocks yet",
    }


# ---- 主扫描 ----

def scan_neighbor(root: Path | str | None = None) -> dict:
    root = Path(root) if root else find_project_root()
    rnd = current_round(root)
    return {
        "project_root": str(root),
        "round": rnd,
        "reviews": scan_reviews(root, rnd),
        "manuscript_tex": scan_manuscript_tex(root, rnd),
        "sci_write": scan_sci_write(root),
        "sci_draw": scan_sci_draw(root),
        "sci_revise": scan_sci_revise(root),
        "issue_ledger_detail": check_issue_ledger(root),
    }


# ---- 渲染 ----

def _mark(ok: bool) -> str:
    return "✓" if ok else "—"


def render_report(result: dict) -> str:
    root = result["project_root"]
    rnd = result["round"]
    lines = [f"# Neighbor scan — {root}"]

    # 轮次
    if rnd["exists"]:
        lines.append(f"Round: **{rnd['round']}** ({rnd['path']})")
        if rnd["available_rounds"] != [rnd["round"]]:
            lines.append(f"  (other rounds present: {', '.join(rnd['available_rounds'])})")
    else:
        lines.append("Round: **none yet** — no rN directory under manuscript/. "
                     + ("v1 exists (post-submission, awaiting reviews)."
                        if rnd["v1_exists"] else
                        "no v1 either — confirm this is a revision project."))
    lines.append("")

    # reviews
    rv = result["reviews"]
    lines.append("## Reviews (the reviewer comments)")
    if rv["files"]:
        for f in rv["files"]:
            lines.append(f"  {_mark(f['exists'])} {f['name']} ({f['size']} bytes)")
    else:
        lines.append(f"  — {rv['note']}")
    lines.append("")

    # manuscript tex
    mt = result["manuscript_tex"]
    lines.append("## Manuscript tex (the version under revision)")
    lines.append(f"  {_mark(mt['exists'])} {mt['tex_dir']}")
    if mt["sections_dir"]["exists"]:
        secs = mt["sections_dir"]["files"]
        lines.append(f"    sections/: {', '.join(secs) if secs else '(empty)'}")
    if mt["note"]:
        lines.append(f"  ⚠ {mt['note']}")
    lines.append("")

    # sci-write notes (the paper's thinking — often more useful than the manuscript)
    sw = result["sci_write"]
    lines.append("## Writing-stage notes (sci-skills/sci-write/) — the paper's thinking")
    if sw["exists"]:
        for name, info in sw["notes"].items():
            lines.append(f"  {_mark(info['exists'])} {name}"
                         + (f" ({info['size']} bytes)" if info['exists'] else ""))
        if sw["fig_readings"]:
            lines.append(f"  fig-readings: {', '.join(sw['fig_readings'])}")
    else:
        lines.append(f"  — {sw['note']}")
    lines.append("")

    # sci-draw
    sd = result["sci_draw"]
    lines.append("## Figure reports (sci-skills/sci-draw/) — figure evidence + stats")
    if sd["reports"]:
        for r in sd["reports"]:
            lines.append(f"  ✓ {r}")
    else:
        lines.append(f"  — {sd['note']}")
    lines.append("")

    # sci-revise (process state)
    sr = result["sci_revise"]
    lines.append("## Revision-round state (sci-skills/sci-revise/)")
    if sr["exists"]:
        for label, key in [("issue-ledger.md", "issue_ledger"),
                           ("change-log.md", "change_log"),
                           ("polish-todo.md", "polish_todo")]:
            info = sr[key]
            lines.append(f"  {_mark(info['exists'])} {label}"
                         + (f" ({info['size']} bytes)" if info['exists'] else ""))
    else:
        lines.append(f"  — {sr['note']}")
    lines.append("")

    # issue-ledger 字段完整性
    ild = result["issue_ledger_detail"]
    if ild["exists"] and ild["issues"]:
        lines.append("## Issue-ledger field completeness")
        lines.append(f"  {ild['count']} issues, {ild['incomplete']} with missing required fields.")
        for iss in ild["issues"]:
            tag = "⚠ " if iss["missing_fields"] else "✓ "
            extra = f" (missing: {', '.join(iss['missing_fields'])})" if iss["missing_fields"] else ""
            dep = f" depends_on={iss['depends_on']}" if iss["depends_on"] else ""
            lines.append(f"  {tag}{iss['id']}{extra}{dep}")

    return "\n".join(lines)


def main(argv: list[str]) -> int:
    root = argv[1] if len(argv) > 1 else None
    result = scan_neighbor(root)
    print(render_report(result))
    print("\n--- JSON ---")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
