#!/usr/bin/env python3
"""check_polish.py — 一致性机械门（确定性，纯 stdlib）。

两项纯机械检查（spec §④）：
1. ledger enforce——thesis-terminology-ledger.md 的 markdown 表格（normative 五列
   `| Category | Term / variants | Canonical form | Source | Notes |`，按 header 名
   匹配：Term/variants + Canonical form 两列必需，其余列容忍，aquarius P6）解析出
   变体→规范形映射，grep 全部章 tex 查变体残留。LaTeX 注释（% 整行/行内）不计；
   ASCII 变体词边界匹配（防 columnum 内误报 um），CJK 变体子串匹配。
2. 交叉引用悬空（单向）——\\ref/\\eqref/\\autoref/\\cref/\\Cref{X}（含逗号多 key）
   指向不存在的 \\label{X}。**不查未用 label**（aquarius P5：ch:/sec:/eq: label
   合法地永不被引用，按 issue 报是系统性噪声）。

**诚实命名**：本门只查机械一致性。**不查**散文质量（depth——人工审+eval）、
**不重跑写作链门**（写作链各 check 脚本是 write-time check
非 post-polish invariant——glossary Intro↔Summary coherence lock；polish 改写 prose
后 baton 位置漂移是已知且接受的）、**不查 AIGC 分数**（只有再检测知道）。
ledger 缺失 → issue + 降级（交叉引用照查——polish 向前兼容半成品，spec §④）。
输出有界：MAX_ISSUES 截断 + 显式截断行（no silent cap）。

退出码: 0 = 通过; 1 = 有 issue（逐条打印）。
用法:
    python check_polish.py [<tex-dir>] [<ledger.md>]
    默认: ./thesis/tex, ./sci-skills/thesis-terminology-ledger.md（相对 cwd，即项目根）
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

MAX_ISSUES = 200          # bounded output——超出截断 + 显式行
VARIANT_MIN_LEN = 2       # 单字符变体太噪，跳过
# 视为 "空变体" 的值
_NONE_TOKENS = {"none", "（none）", "(none)", "无", "—", "-"}


def _fences_balanced(text: str) -> bool:
    """数 ``` 开头行——奇数 = 存在未闭合 code fence（fail-noisy：孤 fence 会让
    其后表格被整体吞掉，须显式诊断。与 _ledger_tables 用同一 fence 判定）。
    【继承自家族最硬化 check 脚本——verbatim，docstring 已本地化】"""
    n = sum(1 for line in text.splitlines() if line.lstrip().startswith("```"))
    return n % 2 == 0


# ANSI/控制序列消毒（aries B5 lineage）——\t 与 \n 留。
_CTRL_RE = re.compile(r"[\x00-\x08\x0b-\x1f\x7f]")


def _sanitize(val: str) -> str:
    """剥离 ANSI/控制序列——issue 行只承载可读文本（原始 ledger/报告值不可直接
    进输出，防终端 title 改写/日志行伪造）。【继承自家族最硬化 check 脚本——verbatim】"""
    return _CTRL_RE.sub("", val)


def _strip_comment(line: str) -> str:
    """去掉 LaTeX 注释：% 起注释，\\% 是字面百分号，\\\\% 是换行命令后接注释。
    状态机逐字消费：反斜杠+下一字符原子吞（正确处理 \\\\ 与 \\% 的一切偶/奇
    反斜杠串），裸 % 截断（F3——lookbehind 正则对 \\\\% 判反，状态机无此洞）。"""
    out: list[str] = []
    i = 0
    while i < len(line):
        c = line[i]
        if c == "\\":
            out.append(line[i:i + 2])
            i += 2
            continue
        if c == "%":
            break
        out.append(c)
        i += 1
    return "".join(out)


def _ledger_tables(text: str) -> list[list[str]]:
    """fence-aware markdown 表格抽取：返回表格行块（连续 | 行为一块）。
    fence 内的表格不计（示例块不是 ledger 数据）。"""
    blocks: list[list[str]] = []
    cur: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.lstrip().startswith("|"):
            cur.append(line.strip())
        elif cur:
            blocks.append(cur)
            cur = []
    if cur:
        blocks.append(cur)
    return blocks


def _parse_ledger_pairs(text: str) -> tuple[list[tuple[str, str]], int]:
    """按 header 名匹配解析 (变体→规范形) 对（aquarius P6）。

    header 行须同时含 variant/term 列与 canonical 列（大小写不敏感，子串匹配
    ——'Term / variants' 命中 'term' 也命中 'variant'）；分隔行（---）跳过；
    变体按 / 与中英逗号切分；与 canonical 同形（忽略大小写）**或包含于
    canonical** 的变体跳过（F2：变体 ⊂ 自身规范形 = 永远无法 enforce——正确
    文本必含规范形即自啮，跳过是语义正确非掩盖）。
    返回 (pairs, 可解析表格数)——非术语表格（header 名不匹配）跳过不计数。
    """
    pairs: list[tuple[str, str]] = []
    n_tables = 0
    for block in _ledger_tables(text):
        header = [c.strip().lower() for c in block[0].strip("|").split("|")]

        def _col(names: tuple[str, ...]) -> int | None:
            for i, h in enumerate(header):
                if any(n in h for n in names):
                    return i
            return None

        vi = _col(("variant", "term"))
        ci = _col(("canonical",))
        if vi is None or ci is None:
            continue  # 非术语表格（笔记表/单位表无 variants 列等）——header 名不匹配则跳过
        n_tables += 1
        for row in block[1:]:
            cells = [c.strip() for c in row.strip("|").split("|")]
            if len(cells) != len(header):
                continue
            if all(re.fullmatch(r":?-+:?", c or "-") for c in cells):
                continue  # 分隔行 |---|---|
            if vi >= len(cells) or ci >= len(cells):
                continue
            canon = cells[ci]
            variants = [v.strip() for v in re.split(r"[/,，]", cells[vi])
                        if len(v.strip()) >= VARIANT_MIN_LEN
                        and v.strip().lower() not in _NONE_TOKENS]
            if canon and len(canon) >= VARIANT_MIN_LEN:
                for v in variants:
                    if v.lower() != canon.lower() and v.lower() not in canon.lower():
                        pairs.append((v, canon))
    return pairs, n_tables


def _variant_pattern(variant: str) -> re.Pattern[str]:
    """ASCII 词（字母数字连字符）→ 词边界匹配（防 columnum 内误报 um）；
    含 CJK/其他字符 → 纯子串匹配（\\b 对 CJK 无效）。"""
    if re.fullmatch(r"[A-Za-z0-9\-]+", variant):
        return re.compile(rf"(?<![A-Za-z0-9\-]){re.escape(variant)}(?![A-Za-z0-9\-])")
    return re.compile(re.escape(variant))


_REF_RE = re.compile(r"\\(?:ref|eqref|autoref|cref|Cref)\{([^}]+)\}")
_LABEL_RE = re.compile(r"\\label\{([^}]+)\}")


def check(tex_dir: Path, ledger: Path) -> list[str]:
    """返回 issue 列表（空 = 通过）。不抛异常——问题进列表。"""
    issues: list[str] = []

    # --- tex 收集 ---
    tex_files: list[Path] = []
    if not tex_dir.is_dir():
        issues.append(f"✗ {tex_dir} 不存在或非目录（thesis/tex 未建？先跑写作链）")
    else:
        tex_files = sorted(p for p in tex_dir.glob("*.tex") if p.is_file())
        if not tex_files:
            issues.append(f"✗ {tex_dir} 无 .tex 文件（写作链未产正文？）")

    # --- ledger 解析（缺失→issue+降级，非终止——spec §④）---
    pairs: list[tuple[str, str]] = []
    if not ledger.is_file():
        issues.append(f"✗ {ledger} 不存在——一致性检查降级（只查交叉引用）；"
                      "spine 建 ledger 是写作链前提，缺失请先跑 thesis-spine")
    else:
        try:
            text = ledger.read_text(encoding="utf-8-sig")
            if not _fences_balanced(text):
                issues.append(f"✗ {ledger} 存在未闭合 code fence——表格解析可能不完整（检查 ``` 配对）")
            pairs, n_tables = _parse_ledger_pairs(text)
            if not n_tables:
                issues.append(f"✗ {ledger} 无可解析术语表格（normative 五列 "
                              "| Category | Term / variants | Canonical form | Source | Notes |，按 header 名匹配）")
        except UnicodeDecodeError:
            issues.append(f"✗ {ledger} 不是有效的 UTF-8 文本（二进制？）——一致性检查降级")
        except OSError as e:
            issues.append(f"✗ {ledger} 无法读取：{e}——一致性检查降级")

    # --- 检查 1：变体残留（LaTeX 注释不计）---
    for v, canon in pairs:
        pat = _variant_pattern(v)
        for tf in tex_files:
            try:
                lines = tf.read_text(encoding="utf-8-sig", errors="replace").splitlines()
            except OSError as e:
                issues.append(f"✗ {tf} 无法读取：{e}")
                continue
            for ln, line in enumerate(lines, 1):
                if pat.search(_strip_comment(line)):
                    issues.append(f"✗ {tf.name}:{ln} 变体 `{_sanitize(v)}` → 应为 "
                                  f"`{_sanitize(canon)}`（thesis-terminology-ledger.md）")

    # --- 检查 2：交叉引用悬空（单向——未用 label 不查，aquarius P5）---
    labels: set[str] = set()
    refs: list[tuple[str, int, str]] = []
    for tf in tex_files:
        try:
            lines = tf.read_text(encoding="utf-8-sig", errors="replace").splitlines()
        except OSError:
            continue  # 读取失败已在检查 1 记 issue
        for ln, line in enumerate(lines, 1):
            code = _strip_comment(line)
            labels.update(_LABEL_RE.findall(code))
            for m in _REF_RE.finditer(code):
                for key in m.group(1).split(","):
                    key = key.strip()
                    if key:
                        refs.append((tf.name, ln, key))
    for fname, ln, key in refs:
        if key not in labels:
            issues.append(f"✗ {fname}:{ln} \\ref{{{key}}} 悬空——\\label{{{key}}} 不存在于任何章 tex")

    # --- bounded output（no silent cap）---
    if len(issues) > MAX_ISSUES:
        kept = issues[:MAX_ISSUES]
        kept.append(f"✗ …… 另有 {len(issues) - MAX_ISSUES} 个 issue 截断（共 {len(issues)}）——"
                    f"修完前 {MAX_ISSUES} 个再跑")
        return kept
    return issues


def main(argv: list[str]) -> int:
    tex_dir = Path(argv[1]) if len(argv) > 1 else Path("thesis") / "tex"
    ledger = Path(argv[2]) if len(argv) > 2 else Path("sci-skills") / "thesis-terminology-ledger.md"
    issues = check(tex_dir, ledger)
    if issues:
        print(f"check_polish: {len(issues)} 个一致性问题 @ {tex_dir} + {ledger}:")
        for it in issues:
            print(f"  {it}")
        return 1
    print(f"check_polish: ✓ 一致性通过 @ {tex_dir}（ledger enforce + 交叉引用）")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
