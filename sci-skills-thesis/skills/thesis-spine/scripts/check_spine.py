#!/usr/bin/env python3
"""check_spine.py — thesis-spine.md coverage 机械门（确定性，纯 stdlib）。

只查 coverage（3 结构字段非空 + 无 pending 残留 + sub-coverage）。
**不查 depth**（umbrella + boundary 是人工门，非脚本职责）——见 spec §门。
这是 enforcement split 的落地：机械归脚本，判断归作者。

退出码: 0 = 通过; 1 = 有 coverage 问题（打印具体问题）。

用法:
    python check_spine.py [<path/to/thesis-spine.md>]
    默认: ./sci-skills/thesis-spine.md（相对 cwd，即项目根）
"""
from __future__ import annotations
import re, sys
from pathlib import Path

# 3 结构字段（coverage-gated）。section 名含括号注释（如 "Main line (主线)"），
# 用 startswith 匹配。umbrella/boundary 不在此——depth 人工门。
STRUCTURAL_FIELDS = ["Main line", "Unified framework", "Inter-chapter progression"]

# pending 标记：字段以 `[pending? ]` 开头表示 AI 候选未 settle。
# header 注释用 backtick-`pending`（不含 `[`），不撞此标记。
# 用 `[pending?`（含问号）而非 `[pending`——后者会误匹配 audit-trail 散文
# 如 `[pending replication by third party]`（aries #3）。
PENDING_MARKER = "[pending?"


def split_sections(text: str) -> dict[str, str]:
    """把 markdown 按 `## ` 标题切成 {section_name: body}（body 不含标题行）。"""
    sections: dict[str, str] = {}
    current_name: str | None = None
    current_lines: list[str] = []
    for line in text.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            if current_name is not None:
                sections[current_name] = "\n".join(current_lines)
            current_name = m.group(1).strip()
            current_lines = []
        elif current_name is not None:
            current_lines.append(line)
    if current_name is not None:
        sections[current_name] = "\n".join(current_lines)
    return sections


def _find_section(sections: dict[str, str], prefix: str) -> str | None:
    """按前缀找 section body（section 名如 'Main line (主线)'）。找不到返回 None。"""
    for name, body in sections.items():
        if name.startswith(prefix):
            return body
    return None


def check(spine_path: Path) -> list[str]:
    """返回 coverage 问题列表（空 = 通过）。不抛异常——问题进列表。"""
    issues: list[str] = []
    if not spine_path.is_file():
        return [f"✗ {spine_path} 不存在（spine 未产？跑 thesis-spine）"]
    try:
        text = spine_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return [f"✗ {spine_path} 不是有效的 UTF-8 文本（二进制？）"]
    except OSError as e:
        return [f"✗ {spine_path} 无法读取：{e}"]

    # 1. 无 pending 残留（settled 后作者删 [pending? ] 标记）
    if PENDING_MARKER in text:
        issues.append("✗ 仍有 `[pending?` 标记——有未 settle 的候选，dissect 不可建在 unsettled 字段上")

    sections = split_sections(text)

    # 2. 3 结构字段存在且非空
    for field in STRUCTURAL_FIELDS:
        body = _find_section(sections, field)
        if body is None:
            issues.append(f"✗ 结构字段 `## {field}` 缺失")
        elif not body.strip():
            issues.append(f"✗ 结构字段 `## {field}` 为空")

    # 3. Unified framework: 每篇 Intake 论文都有实例化行（contract gap 否则）
    intake = _find_section(sections, "Intake") or ""
    framework = _find_section(sections, "Unified framework") or ""
    if framework:
        paper_ids = re.findall(r"^-\s+(paper-[\w-]+)", intake, re.MULTILINE)
        for pid in paper_ids:
            # anchor the id as a distinct token, not a bare substring —
            # paper-A must not match inside paper-AB's instantiation line.
            if not re.search(rf"\b{re.escape(pid)}(?![\w-])", framework):
                issues.append(f"✗ `{pid}` 在 Intake 列出但 Unified framework 无实例化（contract gap）")

    # 4. Inter-chapter progression: 每个角色声明 question + advance
    progression = _find_section(sections, "Inter-chapter progression") or ""
    if progression:
        # 角色条目形如 "- role 1: question = …; advances the main line by …"
        role_lines = [ln for ln in progression.splitlines()
                      if re.match(r"^\s*-\s+role\s+\d+", ln, re.IGNORECASE)]
        if not role_lines:
            issues.append("✗ Inter-chapter progression 无 role 条目")
        for role_line in role_lines:
            low = role_line.lower()
            if "question" not in low:
                issues.append(f"✗ progression role 缺 question：{role_line.strip()}")
            if "advance" not in low:
                issues.append(f"✗ progression role 缺 advance：{role_line.strip()}")
    return issues


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else Path("sci-skills") / "thesis-spine.md"
    issues = check(path)
    if issues:
        print(f"check_spine: {len(issues)} 个 coverage 问题 @ {path}:")
        for it in issues:
            print(f"  {it}")
        return 1
    print(f"check_spine: ✓ coverage 通过 @ {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
