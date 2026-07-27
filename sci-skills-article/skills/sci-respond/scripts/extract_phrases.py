#!/usr/bin/env python3
r"""extract_phrases.py — 从 samples/ 的公开回复信里抽候选框定话术,丢进 phrasebank Inbox。

飞轮(script):作者公开的每一份审稿回复都是 phrasebank 的素材。本脚本扫
assets/samples/<letter>/response.md(从 PDF 提取的 text 版),按一张"框定信号词表"
粗筛出候选句子——那些带重新定位色彩的措辞(does not undermine / manageable /
beyond the scope / we are happy to / for completeness / inherent / future work ...),
不是诚实话术(we agree / we have added 那种谁都会的)。

输出格式直接是 phrasebank.md 的 Inbox 条目格式,复制粘贴即用。vet(A-G 分类、
去留)由人做——本脚本只做能机械做的事(扫文件 + 匹配 + 抽整句 + 标出处)。

用法:
    python scripts/extract_phrases.py                     # 扫所有 samples/*/response.md
    python scripts/extract_phrases.py path/to/letter/    # 扫指定的一封信目录

退出码:0 总是(报告型工具)。
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


# ---- 框定信号词表 ----
# 每条:正则 + 猜测的 tactic(A-G)。命中即把所在整句抽出。
# 这张表是活的——vet 时发现新的框定信号,往这里加,script 下次就能抓到。
FRAMING_SIGNALS = [
    # A. reframe claim scope —— 把弱点框定在 claim 范围之外
    (r"\bdoes not undermine\b", "A-reframe"),
    (r"\bdoes not affect\b", "A-reframe"),
    (r"\bnot (?:a |the )?flaw\b", "A-reframe"),
    (r"\barises not from\b", "A-reframe"),
    (r"\brather from\b", "A-reframe"),
    (r"\bour claim is (?:scoped|limited) to\b", "A-reframe"),
    (r"\bshould be interpreted as\b", "A-reframe"),
    # B. minimize limitation —— 承认但缩小影响
    (r"\bmanageable\b", "B-minimize"),
    (r"\b(inherent|a known characteristic) to\b", "B-minimize"),
    (r"\bnot fully covered\b", "B-minimize"),
    (r"\bvalid limitation\b", "B-minimize"),
    (r"\bcosts? (?:associated )?(?:are|is) (?:manageable|practical|feasible)\b", "B-minimize"),
    (r"\bpractical and feasible\b", "B-minimize"),
    (r"\bmodular design\b", "B-minimize"),
    (r"\ballows? for systematic extension\b", "B-minimize"),
    (r"\b(?:approximate|rough) estimates?\b", "B-minimize"),
    # C. selective emphasis —— 量化有利(这个信号弱,只标强量化词)
    (r"\b\d{2,}[,-]fold\b", "C-emphasis"),
    (r"\borders of magnitude\b", "C-emphasis"),
    # D. divert to SI —— 转移到补充材料
    (r"\b(?:relocated|moved) (?:to|into) (?:the )?Supplementary\b", "D-divert"),
    (r"\bfor completeness\b", "D-divert"),
    (r"\bstrategically relocated\b", "D-divert"),
    # E. fill gap with external ref —— 引文献/预印本填空
    (r"\bto (?:the )?best of our knowledge\b", "E-fill"),
    (r"\bthere are no existing\b", "E-fill"),
    (r"\bto address this gap\b", "E-fill"),
    (r"\bshared as a preprint\b", "E-fill"),
    (r"\bongoing research\b", "E-fill"),
    # F. offer exit —— 给台阶,主动 offer 删除/转移
    (r"\bwe are happy to\b", "F-exit"),
    (r"\bwe are willing to\b", "F-exit"),
    (r"\bif the reviewer (?:believes|prefers)\b", "F-exit"),
    (r"\bwould be discussed in the supplementary\b", "F-exit"),
    # G. exploit misunderstanding —— (通常沉默,无信号词,不扫)
]


def split_sentences(text: str) -> list[str]:
    """粗略分句。保留带小数点的数字(不切错)。剥掉 markdown 标题和孤立题号。"""
    # 先剥 markdown 标题行(## Xxx)——它们不是句子,混进来会污染
    t = re.sub(r"^#{1,6}\s+.*$", "", text, flags=re.MULTILINE)
    # 把句号/问号/感叹号后跟空格或换行作为分句点,但不切小数(数字.数字)
    placeholder = "\x00DOT\x00"
    t = re.sub(r"(\d)\.(\d)", rf"\1{placeholder}\2", t)
    parts = re.split(r"(?<=[.!?])\s+", t)
    out = []
    for p in parts:
        s = p.replace(placeholder, ".").strip()
        # 剥掉句尾的孤立题号(如 "...paper.** 5." → "...paper.**")
        s = re.sub(r"\s+\d{1,3}\.?\s*$", "", s)
        # 剥掉 markdown 加粗/斜体标记(phrasebank 不需要)
        s = s.replace("**", "").replace("__", "")
        if s:
            out.append(s)
    return out


def extract_from_text(text: str, source_label: str) -> list[dict]:
    """扫一份 text,返回命中的候选话术。"""
    sentences = split_sentences(text)
    hits = []
    seen_sentences = set()  # 同一句被多个信号命中,只记一次,tactic 合并
    for sent in sentences:
        # 跳过太短/太长的(整段表格、章节标题)
        if not (20 <= len(sent) <= 400):
            continue
        matched_tactics = []
        matched_signals = []
        for pat, tactic in FRAMING_SIGNALS:
            if re.search(pat, sent, re.IGNORECASE):
                matched_tactics.append(tactic)
                matched_signals.append(pat.replace("\\b", ""))
        if matched_tactics:
            key = sent[:80]  # 去重 key
            if key in seen_sentences:
                # 找已有条目,合并 tactic
                for h in hits:
                    if h["sentence"][:80] == key:
                        for tc in matched_tactics:
                            if tc not in h["tactics"]:
                                h["tactics"].append(tc)
                        break
                continue
            seen_sentences.add(key)
            hits.append({
                "source": source_label,
                "sentence": sent,
                "tactics": matched_tactics,
                "guess": matched_tactics[0] if len(matched_tactics) == 1
                         else " / ".join(sorted(set(matched_tactics))),
            })
    return hits


def find_sample_dirs(skill_root: Path) -> list[Path]:
    """找 assets/samples/*/ 含 response.md 的目录。"""
    samples = skill_root / "assets" / "samples"
    if not samples.exists():
        return []
    return sorted(d for d in samples.iterdir()
                  if d.is_dir() and (d / "response.md").exists())


def render_inbox(hits: list[dict]) -> str:
    """渲染成 phrasebank.md Inbox 可贴的格式。"""
    if not hits:
        return "(no framing phrases found — either the samples have none, or the signal table needs expanding.)"
    lines = []
    for h in hits:
        # 清理句子里的换行(成单行,方便贴)
        sent = re.sub(r"\s+", " ", h["sentence"])
        lines.append(f"- from: {h['source']}")
        lines.append(f"  original: \"{sent}\"")
        lines.append(f"  guess: {h['guess']}")
        lines.append("")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    # skill root = scripts/ 的上两级
    skill_root = Path(__file__).resolve().parent.parent

    if len(argv) > 1:
        # 扫指定目录
        target = Path(argv[1])
        md = target / "response.md" if target.is_dir() else target
        if not md.exists():
            print(f"error: {md} not found", file=sys.stderr)
            return 2
        label = md.parent.name
        hits = extract_from_text(md.read_text(encoding="utf-8"), f"(sample) {label}")
    else:
        # 扫所有 samples
        dirs = find_sample_dirs(skill_root)
        if not dirs:
            print(f"no samples found under {skill_root / 'assets' / 'samples'}",
                  file=sys.stderr)
            return 0
        hits = []
        for d in dirs:
            label = d.name
            text = (d / "response.md").read_text(encoding="utf-8")
            hits.extend(extract_from_text(text, f"(sample) {label}"))

    # 人读报告
    print(f"# Extracted {len(hits)} candidate framing phrase(s) from samples")
    print()
    print("## Inbox-format (paste into phrasebank.md Inbox):")
    print()
    print(render_inbox(hits))
    print()
    print("--- JSON ---")
    print(json.dumps({"count": len(hits), "hits": hits}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
