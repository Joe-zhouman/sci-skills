#!/usr/bin/env python3
"""check_intro.py — gap-map.md near-trivial CONSISTENCY 门（确定性，纯 stdlib）。

**诚实命名（aquarius round-1 load-bearing）**：这是 near-trivial consistency 门，
**非 coverage gate，非 depth**。gaps ~1:1 derived from chapters by construction
（glossary Narrative gap "typically one per body chapter"）→ coverage near-trivial。
本门查的是：缺席（gap-map.md 不存在）+ 官僚 lapse（编造不存在的章号 / filled-by 悬空 /
pending 残留 / 缺 ch0-intro.tex）。**查不出 depth**（一个 gap 实际没章 genuinely fills
但 agent 填了章号 → 过本门，是 depth failure，属人工门/prose eval）。
gap-map.md 的 real value 是 `callback-anchor` data baton（summary 继承的 promise），
非本 consistency 门。见 spec §门与 enforcement + §① residual。

退出码: 0 = 通过; 1 = 有 consistency 问题（打印具体问题）。

用法:
    python check_intro.py [<gap-map.md>] [<chapter-map.md>] [<tex-dir>]
    默认: ./sci-skills/thesis-intro/gap-map.md, ./sci-skills/thesis-dissect/chapter-map.md,
          ./thesis/tex（相对 cwd，即项目根）
"""
from __future__ import annotations
import re, sys
from pathlib import Path

# status 的 settled 值（其它如 pending/unfilled 都 fail）
SETTLED_STATUS = "filled"
# 视为"空"的值（none / 无 / —）
_NONE_TOKENS = {"none", "（none）", "(none)", "无", "—"}
# pending 标记：字段以 `[pending? ]` 开头表示 AI 候选未 settle（镜像 check_spine）。
PENDING_MARKER = "[pending?"


def split_gaps(text: str) -> list[tuple[str, str]]:
    """把 gap-map.md 按 `## Gap N` 切成 [(gap_label, body), ...]，按出现序。
    跳过 ``` 代码块内的标题（mirror check_dissect aries #2）。"""
    gaps: list[tuple[str, str]] = []
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
            m = re.match(r"^##\s+(Gap\s+\d+)(?:\s+.*)?$", line, re.IGNORECASE)
            if m:
                if current_label is not None:
                    gaps.append((current_label, "\n".join(current_lines)))
                current_label = m.group(1).strip()
                current_lines = []
                continue
        if current_label is not None:
            current_lines.append(line)
    if current_label is not None:
        gaps.append((current_label, "\n".join(current_lines)))
    return gaps


def _field_value(body: str, field: str) -> str | None:
    """从 gap body 取字段值。字段形如 `- filled-by: ...`。返回值（去首尾空格），找不到返回 None。"""
    m = re.search(rf"^-\s+{re.escape(field)}\s*:\s*(.*)$",
                  body, re.MULTILINE | re.IGNORECASE)
    return m.group(1).strip() if m else None


def _is_empty(val: str | None) -> bool:
    """字段缺失或值为 none-token → 视为空。"""
    if val is None:
        return True
    v = val.strip().lower()
    return v == "" or v in _NONE_TOKENS


def _chapter_numbers_in(text: str) -> set[int]:
    """从 chapter-map.md 提取所有 `## Chapter N` 的章号（用于 cross-ref check #3，Task 2 扩展）。
    跳过 ``` 代码块内的标题（mirror split_gaps 的 aries #2 fix——否则 code-fence 内的
    `## Chapter 99` 会被当有效章，让 fabricated filled-by: Chapter 99 误过 cross-ref）。"""
    nums: set[int] = set()
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r"^##\s+Chapter\s+(\d+)", line, re.IGNORECASE)
        if m:
            nums.add(int(m.group(1)))
    return nums


def _filled_by_chapter_num(val: str) -> int | None:
    """从 filled-by 值（如 'Chapter 1'）提取章号。匹配不上返回 None。"""
    m = re.search(r"chapter\s+(\d+)", val, re.IGNORECASE)
    return int(m.group(1)) if m else None


def check(gap_map_path: Path, chapter_map_path: Path, tex_dir: Path) -> list[str]:
    """返回 consistency 问题列表（空 = 通过）。不抛异常——问题进列表。"""
    issues: list[str] = []
    if not gap_map_path.is_file():
        return [f"✗ {gap_map_path} 不存在（intro 未产？跑 thesis-intro）"]
    try:
        text = gap_map_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return [f"✗ {gap_map_path} 不是有效的 UTF-8 文本（二进制？）"]
    except OSError as e:
        return [f"✗ {gap_map_path} 无法读取：{e}"]

    # 1. 无 pending 残留（settled 后作者删 [pending? ] 标记）
    if PENDING_MARKER in text:
        issues.append("✗ 仍有 `[pending?` 标记——有未 settle 的候选，summary 不可建在 unsettled gap 上")

    gaps = split_gaps(text)
    if not gaps:
        return ["✗ gap-map.md 无 `## Gap N` 条目"]

    # 预读 chapter-map.md 的章号集合（用于 Task 2 cross-ref；此处先加载，Task 2 加检查）
    chapter_nums: set[int] = set()
    if chapter_map_path.is_file():
        try:
            cm_text = chapter_map_path.read_text(encoding="utf-8")
            chapter_nums = _chapter_numbers_in(cm_text)
        except (UnicodeDecodeError, OSError):
            chapter_nums = set()  # chapter-map 不可读 → cross-ref 查不出，但 core 查继续

    for label, body in gaps:
        # 2. gap 非空
        if _is_empty(_field_value(body, "gap")):
            issues.append(f"✗ {label} gap 缺失或为空")
        # 3. filled-by 非空
        if _is_empty(_field_value(body, "filled-by")):
            issues.append(f"✗ {label} filled-by 缺失或为空")
        # 4. status = filled（不是 pending / unfilled）
        st = _field_value(body, "status")
        if st is None:
            issues.append(f"✗ {label} 缺 status")
        elif st.lower() != SETTLED_STATUS:
            issues.append(f"✗ {label} status={st}（应为 filled；pending=未写完，unfilled=无章填此 gap）")
        # 6. filled-by 章存在于 chapter-map.md（near-trivial consistency：防 agent 编造不存在的章号）
        fb = _field_value(body, "filled-by")
        if not _is_empty(fb):
            ch_num = _filled_by_chapter_num(fb)
            if ch_num is None:
                issues.append(f"✗ {label} filled-by `{fb}` 无法解析章号（应为 'Chapter N' 格式）")
            elif chapter_nums and ch_num not in chapter_nums:
                issues.append(f"✗ {label} filled-by Chapter {ch_num} 不在 chapter-map.md 的章列表中（悬空/编造）")
    # 若 chapter-map.md 缺失（dissect 未跑），报 issue（intro 需 dissect 的 baton 才能 cross-ref）
    if not chapter_map_path.is_file():
        issues.append(f"✗ {chapter_map_path} 不存在（dissect 未产？intro 需 chapter-map.md 做 cross-ref）")
    # 5. ch0-intro.tex 存在于 thesis/tex/
    intro_tex = tex_dir / "ch0-intro.tex"
    if not intro_tex.is_file():
        issues.append(f"✗ ch0-intro.tex 不存在于 {tex_dir}（intro 未写绪论 tex？）")
    return issues


def main(argv: list[str]) -> int:
    gm_path = Path(argv[1]) if len(argv) > 1 else Path("sci-skills") / "thesis-intro" / "gap-map.md"
    cm_path = Path(argv[2]) if len(argv) > 2 else Path("sci-skills") / "thesis-dissect" / "chapter-map.md"
    tex_dir = Path(argv[3]) if len(argv) > 3 else Path("thesis") / "tex"
    issues = check(gm_path, cm_path, tex_dir)
    if issues:
        print(f"check_intro: {len(issues)} 个 consistency 问题 @ {gm_path}:")
        for it in issues:
            print(f"  {it}")
        return 1
    print(f"check_intro: ✓ consistency 通过 @ {gm_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
