#!/usr/bin/env python3
"""check_dissect.py — chapter-map.md coverage 机械门（确定性，纯 stdlib）。

只查 coverage（每章 framework-instantiation 非空 + progression-in（ch1 除外）
+ progression-out（末章除外）+ status=written + tex-file 存在于 thesis/tex/）。
**不查 depth/grounding**（重构好不好、claim 挂不挂证据是人工门/prose eval，非脚本职责）——见 spec §门。
这是 enforcement split 的落地：机械归脚本，判断归作者。

退出码: 0 = 通过; 1 = 有 coverage 问题（打印具体问题）。

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
