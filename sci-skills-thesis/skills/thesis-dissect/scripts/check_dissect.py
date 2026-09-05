#!/usr/bin/env python3
r"""check_dissect.py — chapter-map.md coverage + 零丢弃缺席机械门（确定性，纯 stdlib）。

查 coverage（每章 framework-instantiation 非空 + progression-in（ch1 除外）
+ progression-out（末章除外）+ status=written + tex-file 存在于 thesis/tex/），
以及两类"防缺席"检查：
1. 零丢弃缺席：每章 papers 的 paper-X/trace.md 存在，且 SI 清单与讨论素材清单
   每条有去向（→ 实际落点），不允许 `pending` 残留或缺去向（小论文的 SI/discussion
   因篇幅限制被挤出正文，学位论文没有此限制——丢弃必须是显式弃用+理由）。
2. 章形签名：章 tex 的 \section 标题不得是 IMRaD 词（机械拆分 Methods/Results 的
   形态）；"本章讨论"节存在（discussion 是每篇论文的精髓，独立成节）；"本章小结"
   末节存在；章引存在（\chapter 与首个 \section 之间有实质引文段，或首节名"引言"）。
**不查 depth/grounding**（重构好不好、claim 挂不挂证据是人工门/prose eval，非脚本职责）——见 spec §门。
这是 enforcement split 的落地：机械归脚本，判断归作者。

退出码: 0 = 通过; 1 = 有 coverage/缺席问题（打印具体问题）。

用法:
    python check_dissect.py [<path/to/chapter-map.md>] [<tex-dir>]
    默认: ./sci-skills/thesis-dissect/chapter-map.md, ./thesis/tex（相对 cwd，即项目根）
"""
from __future__ import annotations
import re, sys
from pathlib import Path

# status 的 settled 值（其它如 pending/stale 都 fail）
SETTLED_STATUS = "written"
# 视为"空"的 progression 值（ch1 progression-in / 末章 progression-out 允许 none，
# 但非首/末章的 none 视为缺失）
_NONE_TOKENS = {"none", "（none）", "(none)", "无", "—"}


def split_chapters(text: str) -> list[tuple[str, str]]:
    """把 chapter-map.md 按 `## Chapter N` 切成 [(chapter_label, body), ...]，按出现序。
    跳过 ``` 代码块内的标题（aries #2 — code-fence blindness）。"""
    chapters: list[tuple[str, str]] = []
    current_label: str | None = None
    current_lines: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            if current_label is not None:
                current_lines.append(line)
            continue
        if not in_fence:
            m = re.match(r"^##\s+(Chapter\s+\d+)(?:\s+.*)?$", line, re.IGNORECASE)
            if m:
                if current_label is not None:
                    chapters.append((current_label, "\n".join(current_lines)))
                current_label = m.group(1).strip()
                current_lines = []
                continue
        if current_label is not None:
            current_lines.append(line)
    if current_label is not None:
        chapters.append((current_label, "\n".join(current_lines)))
    return chapters


def _field_value(chapter_body: str, field: str) -> str | None:
    """从 chapter body 取字段值。字段形如 `- framework-instantiation: ...`。
    返回值（去首尾空格），找不到返回 None。"""
    m = re.search(rf"^-\s+{re.escape(field)}\s*:\s*(.*)$",
                  chapter_body, re.MULTILINE | re.IGNORECASE)
    return m.group(1).strip() if m else None


def _is_empty(val: str | None) -> bool:
    """字段缺失或值为 none-token → 视为空。"""
    if val is None:
        return True
    v = val.strip().lower()
    return v == "" or v in _NONE_TOKENS


# ---------- 章形签名 + 零丢弃缺席（防缺席层；质量仍归人工门） ----------

# IMRaD 签名词表：**整标题等值**匹配（normalize 后），非包含——
# "XX 的合成与表征"这类模块标题（干什么的名词化）不误伤；裸的"方法/结果"才拦。
_IMRAD_TITLES = {
    "方法", "实验方法", "实验部分", "实验与方法", "材料与方法", "方法与材料",
    "实验材料与方法", "实验部分与方法", "表征方法", "实验与表征", "实验与结果分析",
    "结果", "实验结果", "结果与讨论", "结果与分析", "结果与表征", "结果和讨论",
    "methods", "experimentalmethods", "experimentalsection", "materialsandmethods",
    "methodology", "results", "resultsanddiscussion", "characterization", "experimental",
}

# 章引的等价节名（模板用 \section{引言} 开章时视为有章引）
_INTRO_TITLES = {"引言", "绪论", "本章引言", "引言与概述", "概述"}

# 章引正文的最低实质字符数（启发式阈值；剥离命令与空白后）
_CHAPTER_INTRO_MIN_CHARS = 80


def _norm_title(title: str) -> str:
    """标题归一：去空白/标点、小写——供整标题等值匹配。"""
    return re.sub(r"[^\w\u4e00-\u9fff]+", "", title.lower())


def _strip_tex_comments(text: str) -> str:
    r"""剥离 tex 注释（先保 \% 再砍 % 后内容——naive 但对 gate 足够，文档已声明）。"""
    text = text.replace("\\%", "")
    return "\n".join(re.sub(r"%.*", "", ln) for ln in text.splitlines())


def _section_titles(tex_text: str) -> list[str]:
    """按出现序取 \\section{...} 标题（\\section* 也算；\\subsection 不算——模块内部细分会
    合法存在，签名只看章的顶层骨架）。"""
    return [m.group(1).strip()
            for m in re.finditer(r"\\section\*?\{([^}]*)\}", tex_text)]


def _tex_shape_issues(tex_path: Path, label: str) -> list[str]:
    """章 tex 的章形签名检查（IMRaD 词 / 本章讨论 / 本章小结 / 章引）。文件不存在不在此查
    （coverage 层已查）。启发式口径见 tests/README 已知局限。"""
    issues: list[str] = []
    try:
        text = _strip_tex_comments(tex_path.read_text(encoding="utf-8"))
    except UnicodeDecodeError:
        return [f"✗ {label} tex-file `{tex_path.name}` 不是有效的 UTF-8 文本"]
    except OSError as e:
        return [f"✗ {label} tex-file `{tex_path.name}` 无法读取：{e}"]

    sections = _section_titles(text)

    # 1. IMRaD 签名——机械拆分 Methods/Results 的形态，直接拦
    for sec in sections:
        if _norm_title(sec) in _IMRAD_TITLES:
            issues.append(
                f"✗ {label} \\section{{{sec}}} 是 IMRaD 词——这是机械拆分 Methods/Results 的"
                f"形态；模块标题应是'干什么的名词化'（见 restructure-discipline.md 章形）")

    # 2. 本章讨论节——discussion 是每篇论文的精髓，必须独立成节
    if not any("讨论" in s for s in sections):
        issues.append(f"✗ {label} 缺'本章讨论'节——小论文 discussion 的机制/文献对比/局限"
                      f"必须存活且独立成节，不按模块切块")

    # 3. 本章小结——末节收束章问题 + 递进
    if not sections:
        issues.append(f"✗ {label} 无任何 \\section——章形不完整（章引→模块链→本章讨论→本章小结）")
    else:
        last = sections[-1]
        if "小结" not in last and "总结" not in last:
            issues.append(f"✗ {label} 末节应为'本章小结'（实为'{last}'）——收束章引问题+递进下一章")

    # 4. 章引——\chapter 与首个 \section 之间有实质引文段，或首节名"引言"
    ch = re.search(r"\\chapter\*?\{[^}]*\}", text)
    if ch is not None:
        after = text[ch.end():]
        first_sec = re.search(r"\\section\*?\{", after)
        intro_body = after[:first_sec.start()] if first_sec else after
        # 剥常见无内容命令与其参数（一级），再数实质字符
        intro_body = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?(\{[^{}]*\})?", "", intro_body)
        if len(re.sub(r"\s+", "", intro_body)) < _CHAPTER_INTRO_MIN_CHARS:
            first_title = sections[0] if sections else ""
            if _norm_title(first_title) not in _INTRO_TITLES:
                issues.append(
                    f"✗ {label} 缺章引——\\chapter 与首个 \\section 之间无实质引文段"
                    f"（或首节名'引言'）；引言的职责是提本章问题")
    return issues


def _parse_papers(chapter_body: str) -> list[str]:
    """从 `- papers: [paper-A, paper-C]` 取 slug 列表。"""
    m = re.search(r"^-\s+papers\s*:\s*\[([^\]]*)\]", chapter_body, re.MULTILINE | re.IGNORECASE)
    if m is None:
        return []
    return [p.strip() for p in m.group(1).split(",") if p.strip()]


def _inventory_issues(trace_text: str, slug: str) -> list[str]:
    """SI 清单 / 讨论素材清单：节存在（或显式'无 SI'/'无讨论'声明）+ 每条有去向且非 pending。"""
    issues: list[str] = []
    for header_re, name, decl_display in (
            (r"^##\s*SI", "SI 清单", "无 SI"),
            (r"^##\s*讨论", "讨论素材清单", "无讨论")):
        none_decl = re.compile(decl_display.replace(" ", r"\s*"))
        has_section = re.search(header_re, trace_text, re.MULTILINE) is not None
        has_decl = none_decl.search(trace_text) is not None
        if not has_section and not has_decl:
            issues.append(f"✗ paper {slug}/trace.md 缺'{name}'节（或'{decl_display}'声明）"
                          f"——素材未清点，零丢弃无法审计")
            continue
        # 节内清单行：`- 条目 → 去向`；去向 pending 或缺 → 都算未落位
        m = re.search(header_re + r"[^\n]*\n", trace_text, re.MULTILINE)
        if m is None:
            continue
        rest = trace_text[m.end():]
        body = re.split(r"^##\s", rest, maxsplit=1, flags=re.MULTILINE)[0]  # 到下一个 ## 节为止
        for ln in body.splitlines():
            if not re.match(r"^\s*-\s+\S", ln):
                continue
            if "→" not in ln and "->" not in ln:
                issues.append(f"✗ paper {slug}/trace.md {name}条目缺去向（→ 落点/弃用+理由）："
                              f"{ln.strip()[:40]}")
            elif re.search(r"(→|->)\s*pending\b", ln, re.IGNORECASE):
                issues.append(f"✗ paper {slug}/trace.md {name}条目去向仍为 pending（章收尾后"
                              f"不允许残留）：{ln.strip()[:40]}")
    return issues


def _trace_issues(trace_path: Path, label: str, slug: str) -> list[str]:
    """每章 papers 的 trace.md 存在 + 清单去向检查（防丢弃缺席）。"""
    if not trace_path.is_file():
        return [f"✗ {label} paper {slug} 缺 trace.md（应为 {trace_path}）——深读未做或"
                f"paper-X/ 目录名与 chapter-map 的 papers 不符"]
    try:
        text = trace_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return [f"✗ paper {slug}/trace.md 不是有效的 UTF-8 文本"]
    except OSError as e:
        return [f"✗ paper {slug}/trace.md 无法读取：{e}"]
    return _inventory_issues(text, slug)


def check(chapter_map_path: Path, tex_dir: Path) -> list[str]:
    """返回 coverage 问题列表（空 = 通过）。不抛异常——问题进列表。"""
    issues: list[str] = []
    if not chapter_map_path.is_file():
        return [f"✗ {chapter_map_path} 不存在（dissect 未产？跑 thesis-dissect）"]
    try:
        text = chapter_map_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return [f"✗ {chapter_map_path} 不是有效的 UTF-8 文本（二进制？）"]
    except OSError as e:
        return [f"✗ {chapter_map_path} 无法读取：{e}"]

    chapters = split_chapters(text)
    if not chapters:
        return ["✗ chapter-map.md 无 `## Chapter N` 条目"]

    total = len(chapters)
    checked_traces: set[str] = set()  # merge 章可能重复引用同一 paper——trace 只查一次
    for idx, (label, body) in enumerate(chapters):
        ch_num = idx + 1  # 章序（首章=1, 末章=total）

        # 1. framework-instantiation 非空（每章都要）
        if _is_empty(_field_value(body, "framework-instantiation")):
            issues.append(f"✗ {label} framework-instantiation 缺失或为空")

        # 2. progression-in 非空（ch1 除外）。用 _is_empty（统一处理 None/空/none-token），
        # 不内联 — 内联版会漏空白值（"progression-in:   " 应 fail 但内联 elif 过）。
        if ch_num > 1:
            pi = _field_value(body, "progression-in")
            if _is_empty(pi):
                issues.append(f"✗ {label} progression-in 缺失/为空/为 none（首章除外，本章非首章）")

        # 3. progression-out 非空（末章除外）。同样用 _is_empty。
        if ch_num < total:
            po = _field_value(body, "progression-out")
            if _is_empty(po):
                issues.append(f"✗ {label} progression-out 缺失/为空/为 none（末章除外，本章非末章）")

        # 4. status = written（不是 pending / stale）
        st = _field_value(body, "status")
        if st is None:
            issues.append(f"✗ {label} 缺 status")
        elif st.lower() != SETTLED_STATUS:
            issues.append(f"✗ {label} status={st}（应为 written；pending=未写完，stale=backtrack 后失效）")

        # 5. tex-file 存在于 thesis/tex/
        tf = _field_value(body, "tex-file")
        if tf is None:
            issues.append(f"✗ {label} 缺 tex-file")
        elif not tf.strip():
            issues.append(f"✗ {label} tex-file 为空")
        else:
            tf_name = tf.strip()
            tf_path = Path(tf_name)
            # aries #1: reject absolute paths + `..` traversal — tex-file must live under thesis/tex/
            if tf_path.is_absolute() or ".." in tf_path.parts:
                issues.append(f"✗ {label} tex-file `{tf_name}` 在 thesis/tex/ 之外（绝对路径或 `..` 遍历，禁止）")
            else:
                tex_path = tex_dir / tf_name
                if not tex_path.is_file():
                    issues.append(f"✗ {label} tex-file `{tf_name}` 不存在于 {tex_dir}")
                else:
                    issues.extend(_tex_shape_issues(tex_path, label))

        # 6. 零丢弃缺席：每章 papers 的 trace.md 存在 + SI/讨论清单去向落位
        for slug in _parse_papers(body):
            if slug in checked_traces:
                continue
            checked_traces.add(slug)
            trace_path = chapter_map_path.parent / slug / "trace.md"
            issues.extend(_trace_issues(trace_path, label, slug))
    return issues


def main(argv: list[str]) -> int:
    cm_path = Path(argv[1]) if len(argv) > 1 else Path("sci-skills") / "thesis-dissect" / "chapter-map.md"
    tex_dir = Path(argv[2]) if len(argv) > 2 else Path("thesis") / "tex"
    issues = check(cm_path, tex_dir)
    if issues:
        print(f"check_dissect: {len(issues)} 个 coverage 问题 @ {cm_path}:")
        for it in issues:
            print(f"  {it}")
        return 1
    print(f"check_dissect: ✓ coverage 通过 @ {cm_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
