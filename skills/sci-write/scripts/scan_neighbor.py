#!/usr/bin/env python3
"""scan_neighbor.py — 感知图仓库的落盘产物，报告图状态。

哲学：读邻居、不编排邻居、不假设图从哪来。本脚本只扫约定的图仓库目录
（默认 ../sci-draw/）下已存在的 *-report.md，对照本 skill 的 paper-plan.md，
报告每张图的状态。图仓库里的图可来自任何来源（画图 skill / 手工 / 复制），
本脚本只看文件在不在、契约字段齐不齐。纯只读、无副作用——不改 paper-plan
（改 plan 由 SKILL.md 流程在人确认后做）。

用法:
    python scan_neighbor.py                 # 默认相对路径（从 sci-skills/sci-write/ 看）
    python scan_neighbor.py /abs/sci-skills # 给绝对路径，便于测试

退出码: 0 总是（报告型工具，不因"有 pending"而失败）。
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def _here_sci_skills_root() -> Path:
    """默认推断：本脚本在 skills/sci-write/scripts/ 下，
    工作时的 sci-skills/ 在项目根，即 scripts 往上三级再下到 sci-skills/。
    但运行时 cwd 才是关键——约定从 sci-skills/sci-write/ 调用，邻居在 ../sci-draw/。
    """
    return Path.cwd().parent  # cwd=.../sci-skills/sci-write → parent=.../sci-skills


def parse_paper_plan(plan_path: Path) -> dict[str, dict]:
    """解析 paper-plan.md 的图条目。

    约定每个图条目是一个二级标题下的 bullet 列表：
        ## Figure fig1
        - topic: ...
        - claim: ...
        - status: pending | drawn | written
        - report-ref: ...

    返回 {fig_id: {topic, claim, status, report-ref}}。
    缺失字段给空字符串/None。plan 不存在返回 {}。
    """
    if not plan_path.exists():
        return {}

    text = plan_path.read_text(encoding="utf-8")
    entries: dict[str, dict] = {}
    # 匹配 "## Figure <id>" 块
    blocks = re.split(r"^##\s+Figure\s+(\S+)\s*$", text, flags=re.MULTILINE)
    # split 后: [前缀, id1, 块1, id2, 块2, ...]
    for i in range(1, len(blocks), 2):
        fig_id = blocks[i].strip()
        body = blocks[i + 1] if i + 1 < len(blocks) else ""
        entry: dict[str, str | None] = {
            "topic": None,
            "claim": None,
            "status": None,
            "report-ref": None,
        }
        for key in entry:
            m = re.search(rf"^- {re.escape(key)}:\s*(.+?)\s*$", body, flags=re.MULTILINE)
            if m:
                entry[key] = m.group(1).strip()
        entries[fig_id] = entry
    return entries


def scan_neighbor(sci_skills_root: Path | str | None = None) -> dict:
    """扫 <root>/sci-draw/*-report.md，对照 <root>/sci-write/paper-plan.md。

    返回:
        {
          "sci_skills_root": "<路径>",
          "plan_exists": bool,
          "figures": {
            fig_id: {
              "plan_status": "pending|drawn|written|<空>",
              "report_exists": bool,
              "report_path": "<路径或null>",
              "discrepancy": bool   # plan 说 drawn 但 report 不在，或反之
            }
          },
          "unclaimed_reports": [<fig_id>, ...]  # report 存在但 plan 没有该图
        }
    """
    root = Path(sci_skills_root) if sci_skills_root else _here_sci_skills_root()
    draw_dir = root / "sci-draw"
    plan_path = root / "sci-write" / "paper-plan.md"

    plan = parse_paper_plan(plan_path)

    # 扫邻居的 *-report.md，提取 fig_id（文件名形如 fig1-report.md）
    neighbor_reports: dict[str, Path] = {}
    if draw_dir.exists():
        for p in sorted(draw_dir.glob("*-report.md")):
            # fig1-report.md → fig1
            m = re.match(r"^(.+)-report\.md$", p.name)
            if m:
                neighbor_reports[m.group(1)] = p

    figures: dict[str, dict] = {}
    for fig_id, entry in plan.items():
        status = entry.get("status") or ""
        report_path = neighbor_reports.get(fig_id)
        report_exists = report_path is not None
        # discrepancy: plan 说 drawn/written 但 report 不在；或 plan 说 pending 但 report 已在
        discrepancy = False
        if status in ("drawn", "written") and not report_exists:
            discrepancy = True
        if status == "pending" and report_exists:
            discrepancy = True
        figures[fig_id] = {
            "plan_status": status,
            "report_exists": report_exists,
            "report_path": str(report_path) if report_path else None,
            "discrepancy": discrepancy,
        }

    unclaimed = [fid for fid in neighbor_reports if fid not in plan]

    return {
        "sci_skills_root": str(root),
        "plan_exists": plan_path.exists(),
        "figures": figures,
        "unclaimed_reports": unclaimed,
    }


def render_report(result: dict) -> str:
    """把 scan 结果渲染成人读的报告。"""
    lines = []
    root = result["sci_skills_root"]
    lines.append(f"# Neighbor scan — {root}")
    if not result["plan_exists"]:
        lines.append("- paper-plan.md 不存在。先跑 sci-write Step 1 起草 plan。")
        return "\n".join(lines)

    figures = result["figures"]
    if not figures:
        lines.append("- paper-plan.md 里没有图条目。")
    else:
        lines.append("")
        lines.append("| fig | plan_status | report | 备注 |")
        lines.append("|---|---|---|---|")
        for fid, info in figures.items():
            report_mark = "✓ 就绪" if info["report_exists"] else "— 未画"
            note = ""
            if info["discrepancy"]:
                if info["plan_status"] in ("drawn", "written"):
                    note = f"⚠ plan={info['plan_status']} 但 report 不在"
                elif info["plan_status"] == "pending":
                    note = "→ report 已就绪，建议改 status=drawn（人确认）"
            lines.append(
                f"| {fid} | {info['plan_status'] or '?'} | {report_mark} | {note} |"
            )

    if result["unclaimed_reports"]:
        lines.append("")
        lines.append(
            "未登记的图（report 存在但 plan 没有条目）: "
            + ", ".join(result["unclaimed_reports"])
        )
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
