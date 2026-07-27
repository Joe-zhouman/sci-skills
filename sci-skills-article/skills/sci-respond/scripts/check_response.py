#!/usr/bin/env python3
r"""check_response.py — 扫写好的 response.tex,做 self-check 的确定性部分。

哲学(joe #3):self-check 里"搜这 7 项"是确定性的(正则/grep),该是脚本,
不该让 agent 手工搜 7 遍(又慢又易漏)。语义判断(underlying concern 对不对、
tone 是否得体)仍由 agent 做——本脚本只做能机械验证的。

扫描项:
  1. 每条 \revcomment 有没有配 \revresponse(point-by-point 完整性)
  2. 残留占位:[TBD] / TODO / FIXME / INSERT / <...> / "will add later"
  3. changes 块外的裸 \textcolor(应该用 \added/\deleted 宏)
  4. acknowledgement 计数 lint(thank/apolog 出现在 typo/clarify 类的 changes 块附近 = 过度致谢)
  5. banned qualifiers 无证据统计(improves/significant/robust/SOTA/superior 出现次数,提示复核)
  6. 裸 [htbp]/[t]/[p] float 说明符(Response Figure 应非浮动)
  7. cover page 必备字段(Response Letter # / for / title / manu id)

用法:
    python scripts/check_response.py manuscript/r1/response/response-r1.tex
    python scripts/check_response.py /abs/response.tex

退出码:0 总是(报告型工具;有 warning 不算失败,由人/agent 决定怎么处理)。
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def read_tex(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"response tex not found: {path}")
    return path.read_text(encoding="utf-8")


# ---- 1. revcomment / revresponse 配对 ----

def check_comment_response_pairs(text: str) -> dict:
    """每条 \revcomment 应跟一个 \revresponse。统计两边数量 + 找孤儿。"""
    # reviewresponse.sty 的环境:\begin{revcomment}...\end{revcomment}
    comments = re.findall(r"\\begin\{revcomment\}", text)
    responses = re.findall(r"\\begin\{revresponse\}", text)
    return {
        "revcomment_count": len(comments),
        "revresponse_count": len(responses),
        "balanced": len(comments) == len(responses),
        "note": "ok" if len(comments) == len(responses)
                else f"mismatch: {len(comments)} comments vs {len(responses)} responses — "
                     f"a comment without a response (or vice versa)",
    }


# ---- 2. 残留占位 ----

PLACEHOLDER_PATTERNS = [
    (r"\[TBD\]", "TBD", "missing value not filled — author must supply before submission"),
    (r"\[\?\?\?\]|\[XXX\]|\[TBA\]", "placeholder bracket", "leftover placeholder bracket"),
    (r"<[^>\n]{0,40}>", "angle placeholder", "angle-bracket placeholder (<...>)"),
    (r"\bTODO\b|\bFIXME\b", "TODO/FIXME", "leftover planning marker"),
    (r"INSERT[^.\n]{0,40}", "INSERT", "leftover template instruction"),
    (r"will add (?:later|shortly)|to be added", "will-add-later",
     "conditional promise — only ok if venue allows promised revisions"),
]


def check_placeholders(text: str) -> dict:
    findings = []
    for pat, label, note in PLACEHOLDER_PATTERNS:
        hits = re.findall(pat, text, flags=re.IGNORECASE)
        if hits:
            findings.append({"pattern": label, "count": len(hits),
                             "samples": hits[:3], "note": note})
    clean = not findings
    return {
        "clean": clean,
        "findings": findings,
        "note": "ok" if clean else f"{len(findings)} placeholder/planning patterns left — clean before submission",
    }


# ---- 3. changes 块外的裸 \textcolor ----

def check_bare_textcolor(text: str) -> dict:
    r"""\textcolor 应该包在 \added/\deleted 宏里,或用在 caption/quoteRevision。
    changes 块外的裸 \textcolor{...}{...} 是手写的颜色,该改成宏。
    """
    # 先把 changes 块的内容抠掉,在剩余文本里找裸 textcolor
    without_changes = re.sub(r"\\begin\{changes\}.*?\\end\{changes\}",
                             "", text, flags=re.DOTALL)
    # 排除 caption 里的 \textcolor(图注标色是允许的)和 quoteRevision 宏
    without_caption = re.sub(r"\\caption\{[^}]*\}", "", without_changes)
    bare = re.findall(r"\\textcolor\{[^}]+\}\{", without_caption)
    return {
        "bare_textcolor_count": len(bare),
        "note": "ok" if not bare
                else f"{len(bare)} bare \\textcolor outside changes/caption — "
                     f"should use \\added/\\deleted macros or \\quoteRevision",
    }


# ---- 4. acknowledgement 计数 lint ----

ACK_PATTERNS = [
    r"\bthank\b", r"\bappreciate\b", r"\bgrateful\b", r"\bapologize\b",
    r"\binsightful comment", r"\bmeticulous", r"\bvaluable feedback",
]


def check_acknowledgement_restraint(text: str) -> dict:
    """统计致谢类词出现次数。绝对数 + 提示。
    语义判断(哪条 response 该不该有致谢)由 agent 做——本脚本只报数。
    """
    lower = text.lower()
    total = 0
    per = {}
    for pat in ACK_PATTERNS:
        n = len(re.findall(pat, lower))
        if n:
            per[pat] = n
            total += n
    # 计算 changes 块(typo/clarify 类 response)的数量——这类不该有致谢
    changes_blocks = len(re.findall(r"\\begin\{changes\}", text))
    return {
        "ack_hits": total,
        "by_pattern": per,
        "changes_blocks": changes_blocks,
        "note": "ok" if total <= max(3, changes_blocks == 0 and 3 or 3)
                else f"{total} acknowledgement-ish phrases — review for restraint "
                     f"(typo/clarify changes-blocks should have none; heavy responses ≤1 line each)",
    }


# ---- 5. banned qualifiers 无证据 ----

BANNED_QUALIFIERS = ["improves", "outperforms", "significant", "robust", "SOTA",
                     "superior", "state-of-the-art", "remarkable"]


def check_banned_qualifiers(text: str) -> dict:
    """统计 banned qualifiers 出现次数。每个都该有对应 metric 支撑——本脚本只数,agent 复核。"""
    lower = text.lower()
    hits = {}
    for q in BANNED_QUALIFIERS:
        n = len(re.findall(r"\b" + re.escape(q) + r"\b", lower))
        if n:
            hits[q] = n
    return {
        "total": sum(hits.values()),
        "by_qualifier": hits,
        "note": "ok" if not hits
                else f"{sum(hits.values())} banned-qualifier hits — each must be backed "
                     f"by a metric in the same response, else rephrase",
    }


# ---- 6. 裸 float 说明符 ----

def check_float_specifiers(text: str) -> dict:
    r"""Response Figure 应非浮动(\captionof 或 [H])。裸 [htbp]/[t]/[p]/[h] 是 manuscript 惯用法。"""
    # \begin{figure}[htbp] / \begin{table}[t] 等
    bad = re.findall(r"\\begin\{(?:figure|table)\}\s*\[([htbp]+)\]", text)
    return {
        "bad_float_specifiers": bad,
        "count": len(bad),
        "note": "ok" if not bad
                else f"{len(bad)} float env with [{','.join(set(bad))}] — Response Figures must be "
                     f"non-floating: \\captionof or [H], never [htbp]/[t]/[p]",
    }


# ---- 7. cover page 必备字段 ----

COVER_REQUIRED = [
    (r"Response\s+Letter\s*\\?#", "Response Letter #<rN>"),
    (r"\bfor\b", "for (transition word)"),
    (r"[Mm]anuscript\s*(?:ID|id)?", "manuscript id"),
]


def check_cover(text: str) -> dict:
    """cover page 三字段。粗略——只确认关键词出现,不验排版(agent 视觉检查 PDF)。"""
    # 只在 titlepage 块里找(如果有)
    tp = re.search(r"\\begin\{titlepage\}(.*?)\\end\{titlepage\}", text, re.DOTALL)
    scope = tp.group(1) if tp else text[:1500]  # fallback 到开头
    missing = []
    for pat, label in COVER_REQUIRED:
        if not re.search(pat, scope):
            missing.append(label)
    return {
        "has_titlepage": bool(tp),
        "missing_fields": missing,
        "note": "ok" if not missing
                else f"cover page missing: {', '.join(missing)}",
    }


# ---- 主检查 ----

def check_response(path: Path | str) -> dict:
    p = Path(path)
    text = read_tex(p)
    return {
        "file": str(p),
        "size_bytes": p.stat().st_size,
        "checks": {
            "comment_response_pairs": check_comment_response_pairs(text),
            "placeholders": check_placeholders(text),
            "bare_textcolor": check_bare_textcolor(text),
            "acknowledgement": check_acknowledgement_restraint(text),
            "banned_qualifiers": check_banned_qualifiers(text),
            "float_specifiers": check_float_specifiers(text),
            "cover_page": check_cover(text),
        },
    }


def render_report(result: dict) -> str:
    lines = [f"# Response check — {result['file']} ({result['size_bytes']} bytes)", ""]
    checks = result["checks"]
    # 顶层 ok/warn 汇总
    labels = {
        "comment_response_pairs": "Comment/response pairing",
        "placeholders": "Placeholders & planning language",
        "bare_textcolor": "Bare \\textcolor (should be macros)",
        "acknowledgement": "Acknowledgement restraint",
        "banned_qualifiers": "Banned qualifiers (need metric)",
        "float_specifiers": "Float specifiers (must be non-floating)",
        "cover_page": "Cover page fields",
    }
    for key, label in labels.items():
        c = checks[key]
        ok = c.get("note") == "ok" or c.get("balanced") is True or c.get("clean") is True
        mark = "✓" if ok else "⚠"
        lines.append(f"{mark} {label}: {c['note']}")
        # 明细
        if key == "placeholders" and not c["clean"]:
            for f in c["findings"]:
                lines.append(f"    - {f['pattern']} ×{f['count']} {f['samples']}")
        if key == "banned_qualifiers" and c["total"]:
            lines.append(f"    - {c['by_qualifier']}")
        if key == "acknowledgement" and c["ack_hits"]:
            lines.append(f"    - by pattern: {c['by_pattern']}")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("usage: check_response.py <response.tex>", file=sys.stderr)
        return 2
    try:
        result = check_response(argv[1])
    except FileNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    print(render_report(result))
    print("\n--- JSON ---")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
