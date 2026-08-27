#!/usr/bin/env python3
"""check_summary.py — summary-map.md near-trivial CONSISTENCY 门（确定性，纯 stdlib）。

**诚实命名（spec §①，aquarius F1/F6）**：这是 near-trivial consistency 门，**非 depth，
非 polish 后的持续不变量（write-time 检查）**。summary-map.md 各段真价值不同：
Commonality 段的 confirmed 痕迹是 genuinely new（作者 depth 决策的落盘 footprint，
不可从任何盘上文件派生）+ unfilled 状态是 genuinely new（callback 失败的 surface）；
Callback 段的 gap↔Callback 一一对应是 near-trivial-by-construction（gaps ~1:1 derived
from chapters——镜像 check_intro.py 的诚实归属），真价值是**缺席检测**（agent 跳过某
gap 没写收束 → 缺 entry → 拦）；resolved-how 是 write-time self-record（从刚写的 prose
可派生，非独立证据）。本门查：**缺席**（summary-map.md 不存在 / gap 无 Callback）+
**官僚 lapse**（编造不存在的 Gap 号 / 悬空章号 / pending 残留 / 缺 synthesis-tex 文件）。
**查不出 depth**（agent 编一条 resolved-how 而正文没真收束 → 过本门，是 prose-vs-promise
failure，属 eval + 作者）。polish 改过 synthesis prose 后，resolved-how 记录与 prose 的
对齐无人重验（与 intro 的 anchor-in-intro 降级同理）。见 spec §门与 enforcement。

退出码: 0 = 通过; 1 = 有 consistency 问题（打印具体问题）。

用法:
    python check_summary.py [<summary-map.md>] [<gap-map.md>] [<chapter-map.md>] [<tex-dir>]
    默认: ./sci-skills/thesis-summary/summary-map.md, ./sci-skills/thesis-intro/gap-map.md,
          ./sci-skills/thesis-dissect/chapter-map.md, ./thesis/tex（相对 cwd，即项目根）
"""
from __future__ import annotations
import re, sys
from pathlib import Path, PurePath

# status 的 settled 值（其它如 pending/unfilled/proposed 都 fail）
CALLBACK_SETTLED = "filled"
COMMONALITY_SETTLED = "confirmed"
# 视为"空"的值（none / 无 / —）
_NONE_TOKENS = {"none", "（none）", "(none)", "无", "—"}


def _split_sections(text: str, header_word: str) -> list[tuple[str, str]]:
    """把 baton 按 `## <header_word> N` 切成 [(label, body), ...]，按出现序。
    跳过 ``` 代码块内的标题（mirror check_intro.py aries #2——fence 内的条目不算）。"""
    sections: list[tuple[str, str]] = []
    current_label: str | None = None
    current_lines: list[str] = []
    in_fence = False
    pat = re.compile(rf"^##\s+{header_word}\s+(\d+)(?:\s+.*)?$", re.IGNORECASE)
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            if current_label is not None:
                current_lines.append(line)
            continue
        if not in_fence:
            m = pat.match(line)
            if m:
                if current_label is not None:
                    sections.append((current_label, "\n".join(current_lines)))
                current_label = f"{header_word} {m.group(1)}"
                current_lines = []
                continue
        if current_label is not None:
            current_lines.append(line)
    if current_label is not None:
        sections.append((current_label, "\n".join(current_lines)))
    return sections


def _field_value(body: str, field: str) -> str | None:
    """从 entry body 取字段值。字段形如 `- gap-ref: ...`。找不到返回 None。"""
    m = re.search(rf"^-\s+{re.escape(field)}\s*:\s*(.*)$",
                  body, re.MULTILINE | re.IGNORECASE)
    return m.group(1).strip() if m else None


def _top_level_field(text: str, field: str) -> str | None:
    """从 summary-map.md 全文取 top-level 字段值（`synthesis-tex: ...`，无 `- ` 前缀）。"""
    m = re.search(rf"^{re.escape(field)}\s*:\s*(.*)$",
                  text, re.MULTILINE | re.IGNORECASE)
    return m.group(1).strip() if m else None


def _is_empty(val: str | None) -> bool:
    if val is None:
        return True
    v = val.strip().lower()
    return v == "" or v in _NONE_TOKENS


def _header_numbers(text: str, word: str) -> set[int]:
    """从 baton 提取所有 `## <word> N` 的编号（Gap→gap-map；Chapter→chapter-map）。
    跳过 ``` 代码块内的标题（fence 内不算有效——mirror check_intro.py）。"""
    nums: set[int] = set()
    in_fence = False
    pat = re.compile(rf"^##\s+{word}\s+(\d+)", re.IGNORECASE)
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = pat.match(line)
        if m:
            nums.add(int(m.group(1)))
    return nums


def _single_ref_number(val: str, word: str) -> int | None:
    """从引用值（如 'Gap 1'）提取单个编号。匹配不上或含多个 token 返回 None
    （mirror intro aries #5：一 Callback→一 gap）。"""
    matches = re.findall(rf"{word}\s+(\d+)", val, re.IGNORECASE)
    if len(matches) != 1:
        return None  # 0 matches (unparseable) OR >1 matches (malformed multi-ref)
    return int(matches[0])


def check(sm_path: Path, gm_path: Path, cm_path: Path, tex_dir: Path) -> list[str]:
    """返回 consistency 问题列表（空 = 通过）。不抛异常——问题进列表。"""
    issues: list[str] = []
    if not sm_path.is_file():
        return [f"✗ {sm_path} 不存在（summary 未产？跑 thesis-summary）"]
    try:
        text = sm_path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        return [f"✗ {sm_path} 不是有效的 UTF-8 文本（二进制？）"]
    except OSError as e:
        return [f"✗ {sm_path} 无法读取：{e}"]

    callbacks = _split_sections(text, "Callback")
    commonalities = _split_sections(text, "Commonality")

    # 读 gap-map.md 的 Gap 编号集合（bijection + fabricated-ref 用）
    gap_nums: set[int] = set()
    if gm_path.is_file():
        try:
            gm_text = gm_path.read_text(encoding="utf-8-sig")
            gap_nums = _header_numbers(gm_text, "Gap")
        except (UnicodeDecodeError, OSError):
            gap_nums = set()
            issues.append(f"✗ {gm_path} 不可读（二进制/权限）— gap↔Callback 对应检查跳过")
    else:
        issues.append(f"✗ {gm_path} 不存在（intro 未产？summary 需 gap-map.md 做 callback lock）")

    # 读 chapter-map.md 的章号集合（grounded-in cross-ref 用）
    chapter_nums: set[int] = set()
    if cm_path.is_file():
        try:
            cm_text = cm_path.read_text(encoding="utf-8-sig")
            chapter_nums = _header_numbers(cm_text, "Chapter")
        except (UnicodeDecodeError, OSError):
            chapter_nums = set()
            issues.append(f"✗ {cm_path} 不可读（二进制/权限）— grounded-in cross-ref 跳过")
    else:
        issues.append(f"✗ {cm_path} 不存在（dissect 未产？summary 需 chapter-map.md 做 cross-ref）")

    # --- Callback 条目检查 ---
    seen_gap_refs: dict[int, str] = {}  # gap号 → 首个引用它的 Callback label
    for label, body in callbacks:
        gr = _field_value(body, "gap-ref")
        if _is_empty(gr):
            issues.append(f"✗ {label} gap-ref 缺失或为空")
        else:
            n = _single_ref_number(gr, "Gap")
            if n is None:
                issues.append(f"✗ {label} gap-ref `{gr}` 无法解析单个 Gap 号（应为 'Gap N' 格式，一 Callback→一 gap）")
            elif gap_nums and n not in gap_nums:
                issues.append(f"✗ {label} gap-ref Gap {n} 不在 gap-map.md 的 Gap 列表中（编造/悬空）")
            elif n in seen_gap_refs:
                issues.append(f"✗ {label} 与 {seen_gap_refs[n]} 都引用 Gap {n}（一一对应被破坏——一个 gap 一个 Callback）")
            else:
                seen_gap_refs[n] = label
        if _is_empty(_field_value(body, "resolved-how")):
            issues.append(f"✗ {label} resolved-how 缺失或为空")
        st = _field_value(body, "status")
        if st is None:
            issues.append(f"✗ {label} 缺 status")
        elif st.lower() != CALLBACK_SETTLED:
            issues.append(f"✗ {label} status={st}（应为 filled；pending=未写完，unfilled=callback 不起来→交作者裁）")

    # --- bijection：gap-map 每 Gap 有且仅有一个 Callback（缺席检测——本门的 lock 核心）---
    if gap_nums:
        for n in sorted(gap_nums):
            if n not in seen_gap_refs:
                issues.append(f"✗ Gap {n} 无对应 Callback（缺席——gap-map 的每个 gap 须被 summary 兑付，spec §①）")

    # --- Commonality 条目检查 ---
    for label, body in commonalities:
        if _is_empty(_field_value(body, "commonality")):
            issues.append(f"✗ {label} commonality 缺失或为空")
        gi = _field_value(body, "grounded-in")
        if _is_empty(gi):
            issues.append(f"✗ {label} grounded-in 缺失或为空")
        else:
            nums = {int(x) for x in re.findall(r"chapter\s+(\d+)", gi, re.IGNORECASE)}
            if len(nums) < 2:
                issues.append(f"✗ {label} grounded-in `{gi}` 解析出 <2 个不同章（跨章共性的定义下限：≥2 章）")
            elif chapter_nums and not nums <= chapter_nums:
                bad = sorted(nums - chapter_nums)
                issues.append(f"✗ {label} grounded-in 引用 Chapter {bad} 不在 chapter-map.md 的章列表中（悬空/编造）")
        st = _field_value(body, "status")
        if st is None:
            issues.append(f"✗ {label} 缺 status")
        elif st.lower() != COMMONALITY_SETTLED:
            issues.append(f"✗ {label} status={st}（应为 confirmed——作者 depth gate 痕迹；pending=AI 候选未 settle，never auto-adopted）")

    # --- synthesis-tex top-level 字段（template-derived，非硬编码；含路径守卫）---
    syn_name = _top_level_field(text, "synthesis-tex")
    if syn_name is None or not syn_name.strip():
        issues.append("✗ summary-map.md 缺 top-level `synthesis-tex` 字段（总结章文件名，按 template-spec.md）")
    else:
        syn_name = syn_name.strip()
        syn_path = tex_dir / syn_name
        syn_pure = PurePath(syn_name)
        if syn_pure.is_absolute() or ".." in syn_pure.parts:
            issues.append(f"✗ synthesis-tex `{syn_name}` 在 thesis/tex/ 之外（绝对路径或 `..` 遍历，禁止）")
        elif not syn_path.is_file():
            issues.append(f"✗ synthesis-tex `{syn_name}` 不存在于 {tex_dir}（summary 未写总结章 tex？）")
    return issues


def main(argv: list[str]) -> int:
    sm_path = Path(argv[1]) if len(argv) > 1 else Path("sci-skills") / "thesis-summary" / "summary-map.md"
    gm_path = Path(argv[2]) if len(argv) > 2 else Path("sci-skills") / "thesis-intro" / "gap-map.md"
    cm_path = Path(argv[3]) if len(argv) > 3 else Path("sci-skills") / "thesis-dissect" / "chapter-map.md"
    tex_dir = Path(argv[4]) if len(argv) > 4 else Path("thesis") / "tex"
    issues = check(sm_path, gm_path, cm_path, tex_dir)
    if issues:
        print(f"check_summary: {len(issues)} 个 consistency 问题 @ {sm_path}:")
        for it in issues:
            print(f"  {it}")
        return 1
    print(f"check_summary: ✓ consistency 通过 @ {sm_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
