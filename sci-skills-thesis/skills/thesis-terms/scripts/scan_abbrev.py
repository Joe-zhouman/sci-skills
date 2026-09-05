#!/usr/bin/env python3
r"""scan_abbrev.py — 缩写候选提取器（确定性，纯 stdlib）。

**候选器，不是结论器。** 输出的每行都是"待 AI 核验的候选"：全称要逐字回原文锁定、
误报要滤（材料式 Ti3C2Tx、期刊名、图表标签）、脚本漏扫的要 AI 补——翻译另有作者门。
本脚本只负责把"人眼扫 N 篇论文找缩写"的机械部分变便宜。

三类模式：
1. `全称 (ABBR)`   — 论文最常见的定义形："thermal contact resistance (TCR)"。
2. 定义动词句     — "TCR denotes/stands for/refers to/means 全称"、
                    "TCR: thermal contact resistance"（高精度、低召回——兜底形）。
3. 缩写节行       — Abbreviations / Nomenclature / Acronyms / Notation 标题下的
                    `ABBR␣␣全称` 或 `ABBR - 全称` 行。

ABBR 判定：≥2 字符、首字符字母、含 ≥2 个大写字母、允许 `-`/`/` 连接子词且每个子词
以字母开头。数字开头拒（"(3a)"）；全小写拒（"(fig)"）。**已声明的误报类**：大写数字
混合的材料式（Ti3C2Tx）会过判定成为候选——AI 核验滤掉，这是候选器分工的一部分。

同名多全称**不去重**（保留为潜在冲突信号——同缩写异义必须交作者裁决）；同名同全称
（忽略大小写/尾点）去重留首见。

输出: --format md（默认，人读表）| json（agent 用，对象数组）。
退出码: 0 = 成功（含零候选）; 1 = 输入错误（路径不存在/不可读/格式不支持）。

用法:
    python scan_abbrev.py <file-or-dir> [more...] [--format md|json]
    目录则递归收集 .tex/.md/.txt。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# ABBR 最短长度（固定常量，不做 CLI 参数——候选器的判定口径要稳定）
_MIN_ABBR_LEN = 2
# 全称候选的最大词数/长度（防把整句话吞成"全称"）
_MAX_FULL_LEN = 120

# 定义动词锚（模式 2）——只认显式定义动词/冒号，不猜散文续写
_DEFINE_VERBS = r"(?:denotes?|stands?\s+for|refers?\s+to|means?|is\s+defined\s+as|:)"

_TEXT_SUFFIXES = {".tex", ".md", ".txt"}
# 缩写节标题（模式 3）——中英常见写法
_SECTION_HEAD = re.compile(
    r"^(?:#+\s*)?(?:abbreviations?|nomenclature|acronyms?|notation|abbreviation list)"
    r"\s*:?\s*$", re.IGNORECASE)
# 缩写节条目行：`ABBR  全称`（≥2 空格）或 `ABBR - 全称` / `ABBR: 全称`
_SECTION_ENTRY = re.compile(
    r"^\s*([A-Za-z][A-Za-z0-9]*(?:[-/][A-Za-z0-9]+)*)\s*(?:\s{2,}|\s+[-–—:]\s*)(\S.{1,120}?)\s*$")
# 模式 1：全称 (ABBR)——字符类不含换行（prepare 已句切行，全称窗口不出句）
_FULL_PAREN = re.compile(r"([A-Za-z][A-Za-z0-9\-,; \t]{1,%d}?)\s*\(([^()\s][^()]*)\)"
                         % _MAX_FULL_LEN)
# 模式 2：ABBR <定义动词> 全称
_ABBR_DEF = re.compile(r"\b([A-Za-z][A-Za-z0-9]*(?:[-/][A-Za-z0-9]+)*)\s*%s\s+([A-Za-z][A-Za-z0-9\-,; \t]{1,%d})"
                       % (_DEFINE_VERBS, _MAX_FULL_LEN))


def is_acronym(s: str) -> bool:
    """ABBR 判定——口径见模块 docstring（候选器口径，宁滥勿缺，AI 核验兜底）。"""
    s = s.strip()
    if not (_MIN_ABBR_LEN <= len(s) <= 12):
        return False
    if not s[0].isalpha():
        return False
    parts = re.split(r"[-/]", s)
    if not all(parts):
        return False
    if sum(1 for c in s if c.isupper()) < 2:
        return False
    return all(p[0].isalpha() and any(c.isalpha() for c in p) for p in parts)


def prepare(text: str) -> str:
    """剥 LaTeX 注释/行内数学/无参命令，花括号与 ~ 透明化为空格，按句切行
    （句子边界 = 全称捕获的硬边界，防跨句吞成大全称）——让三类模式只看正文。"""
    text = text.replace("\\%", "")
    text = "\n".join(re.sub(r"%.*", "", ln) for ln in text.splitlines())
    text = re.sub(r"\$[^$\n]*\$", " ", text)          # 行内数学
    text = re.sub(r"\\\([^)\n]*\\?\)", " ", text)      # \( ... \)
    text = re.sub(r"\\[a-zA-Z]+\*?", " ", text)        # 无参命令（\label 等）
    text = text.replace("{", " ").replace("}", " ")
    text = text.replace("~", " ").replace("\\\\", " ")
    text = re.sub(r"([.!?])\s+", r"\1\n", text)        # 句切行（e.g./Fig. 之类缩写点也切——只影响候选窗口，无害）
    return text


def _clean_full(raw: str) -> str:
    """全称候选清理：去首尾连接符/标点、剥前导冠词、压空白——只做无损修饰，不改词。"""
    s = re.sub(r"\s+", " ", raw).strip()
    s = s.strip(" ,;:-–—").strip()
    s = re.sub(r"^(?:The|A|An|the|a|an)\s+", "", s)
    return s.strip(" ,;:-–—").strip()


def _ctx(lines: list[str], lineno: int, col: int, span: int = 60) -> str:
    """匹配点的上下文（同行前后各 span 字符，压空白）。"""
    line = lines[lineno]
    lo, hi = max(0, col - span), min(len(line), col + span)
    return re.sub(r"\s+", " ", line[lo:hi]).strip()


def scan_text(text: str, source: str) -> list[dict]:
    """单文件扫描 → 候选列表 [{abbr, full, context, source}]。同名同全称去重留首见。"""
    prepared = prepare(text)
    lines = prepared.splitlines()
    found: list[dict] = []
    seen: set[tuple[str, str]] = set()

    def add(abbr: str, full: str, lineno: int, col: int) -> None:
        abbr, full = abbr.strip(), _clean_full(full)
        if not is_acronym(abbr) or not full:
            return
        key = (abbr.lower(), full.lower().rstrip("."))
        if key in seen:
            return
        seen.add(key)
        found.append({"abbr": abbr, "full": full,
                      "context": _ctx(lines, lineno, col), "source": source})

    # 模式 1：全称 (ABBR)
    for m in _FULL_PAREN.finditer(prepared):
        lineno = prepared.count("\n", 0, m.start())
        col = m.start() - (prepared.rfind("\n", 0, m.start()) + 1)
        add(m.group(2), m.group(1), lineno, col)

    # 模式 2：ABBR <定义动词> 全称
    for m in _ABBR_DEF.finditer(prepared):
        lineno = prepared.count("\n", 0, m.start())
        col = m.start() - (prepared.rfind("\n", 0, m.start()) + 1)
        add(m.group(1), m.group(2), lineno, col)

    # 模式 3：缩写节行（标题行后连续的条目行；连续 2 个非条目非空行即出节）
    in_section = False
    misses = 0
    for lineno, line in enumerate(lines):
        stripped = line.strip()
        if _SECTION_HEAD.match(stripped):
            in_section, misses = True, 0
            continue
        if not in_section:
            continue
        if not stripped:
            continue
        m = _SECTION_ENTRY.match(line)
        if m and is_acronym(m.group(1)):
            add(m.group(1), m.group(2), lineno, 0)
            misses = 0
        else:
            misses += 1
            if misses >= 2:
                in_section = False
    return found


def collect_paths(inputs: list[str]) -> list[Path]:
    """展开输入：文件直收；目录递归收 .tex/.md/.txt。"""
    paths: list[Path] = []
    for raw in inputs:
        p = Path(raw)
        if p.is_dir():
            paths.extend(sorted(q for q in p.rglob("*")
                                if q.is_file() and q.suffix.lower() in _TEXT_SUFFIXES))
        else:
            paths.append(p)
    return paths


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="缩写候选提取器（候选非结论，AI 核验+作者门兜底）")
    ap.add_argument("inputs", nargs="+", help="tex/md/txt 文件或目录（目录递归）")
    ap.add_argument("--format", choices=["md", "json"], default="md", help="输出格式（默认 md）")
    args = ap.parse_args(argv[1:])

    paths = collect_paths(args.inputs)
    if not paths:
        print("scan_abbrev: ✗ 输入不含任何 .tex/.md/.txt 文件（目录为空或后缀不符）", file=sys.stderr)
        return 1
    candidates: list[dict] = []
    for p in paths:
        if not p.is_file():
            print(f"scan_abbrev: ✗ 文件不存在: {p}", file=sys.stderr)
            return 1
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            print(f"scan_abbrev: ✗ 非 UTF-8 文本: {p}", file=sys.stderr)
            return 1
        except OSError as e:
            print(f"scan_abbrev: ✗ 无法读取 {p}: {e}", file=sys.stderr)
            return 1
        candidates.extend(scan_text(text, str(p)))

    if args.format == "json":
        print(json.dumps(candidates, ensure_ascii=False, indent=2))
        return 0

    if not candidates:
        print("scan_abbrev: 无候选（脚本三模式未命中——不等于论文无缩写，AI 补扫兜底后再下结论）")
        return 0
    print("# 缩写候选（scan_abbrev.py）")
    print("> 候选非结论：AI 核验全称逐字 + 滤误报 + 补扫；译名另有作者门。")
    print("> 同缩写多全称 = 潜在冲突（同缩写异义），须交作者裁决。")
    print()
    print("| 缩写 | 候选全称 | 出处 | 上下文 |")
    print("|---|---|---|---|")
    for c in candidates:
        print(f"| {c['abbr']} | {c['full']} | {c['source']} | {c['context']} |")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
