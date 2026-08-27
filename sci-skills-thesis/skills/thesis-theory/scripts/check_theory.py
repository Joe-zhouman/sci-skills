#!/usr/bin/env python3
"""check_theory.py — theory-map.md near-trivial CONSISTENCY 门（确定性，纯 stdlib）。

**诚实命名（spec §①/§⑥，aquarius T1/T3/T5）**：这是 near-trivial consistency 门，
**非 depth，非 polish 后的持续不变量（write-time 检查）**。theory-map.md 各段真价值
不同：Shared 段的 confirmed 痕迹是 genuinely new（作者 depth 决策的落盘 footprint，
不可从任何盘上文件派生）+ extraction-outcome: waived-by-author 是 genuinely new
（候选全否决、作者裁最小章的落盘终态——本门识别为合法终态，非 vacuous pass）；
Overlap 段是 genuinely new（作者手解的 work list——**resolver 是作者非 sibling
skill，本门不 enforce resolution**，disposition 可选字段不查）。本门查：**缺席**
（theory-map.md 不存在 / confirmed 但 Shared 段空）+ **官僚 lapse**（编造 Shared/
章号 / 悬空 grounded-in / pending 残留 / 缺 theory-tex 文件 / spine 被重开——
`[pending?` 残留 = mid-write backtrack 窗口，spec §⑥ #5）。**查不出 depth**
（forced/trivial 共用过作者门 / 编造 § 位置 / Overlap 覆盖完整性[提升未记录的
absent 条目]——属 eval + 作者）。polish 改过理论章 prose 后，overlap 位置与 prose
的对齐无人重验（与 summary F6 同理）。见 spec §门与 enforcement。

退出码: 0 = 通过; 1 = 有 consistency 问题（打印具体问题）。

用法:
    python check_theory.py [<theory-map.md>] [<chapter-map.md>] [<thesis-spine.md>] [<tex-dir>]
    默认: ./sci-skills/thesis-theory/theory-map.md, ./sci-skills/thesis-dissect/chapter-map.md,
          ./sci-skills/thesis-spine.md, ./thesis/tex（相对 cwd，即项目根）
"""
from __future__ import annotations
import re, sys
from pathlib import Path, PurePath

# status/outcome 的 settled 值（其它如 pending/proposed 都 fail）
SHARED_SETTLED = "confirmed"
OUTCOME_CONFIRMED = "confirmed"
OUTCOME_WAIVED = "waived-by-author"
# spine 的 pending 标记（mid-write backtrack 复验用——mirror check_spine.py：含问号
# 防 audit-trail 散文误匹配，aries #3）。注意：theory-map.md 自身不用此标记——
# 它自己的候选态用 status 字段表示（mirror summary F3，无死 grep）。
PENDING_MARKER = "[pending?"
# 视为"空"的值（none / 无 / —）
_NONE_TOKENS = {"none", "（none）", "(none)", "无", "—"}


# 任意级别 markdown 标题（`## 备注` / `### 编辑注记` / 异族 entry header 一视同仁）
# 与单独成行的水平分割线（`---` / `***` / `___`）都终止当前 entry——字段窗口被截断，
# 外来区块的字段行不能顶替本 entry 的缺失字段（aries B1 + R1；取代旧的
# _ANY_ENTRY_HEADER——那是本规则的 Shared/Overlap 特例）。hr 须整行只有
# 分割字符（`-{3,}\s*$` 等）——bullet `- shared-ref` 带后续内容，不满足，不会误伤。
_SCOPE_TERMINATOR = re.compile(r"^(?:#{1,6}\s|-{3,}\s*$|\*{3,}\s*$|_{3,}\s*$)")


def _split_sections(text: str, header_word: str) -> list[tuple[str, str]]:
    """把 baton 按 `## <header_word> N` 切成 [(label, body), ...]，按出现序。
    entry scoping（aries B1/B3/R1 收紧）：字段窗口 = entry header 起，到**任意级别**
    的下一个 markdown 标题或单独成行的水平分割线为止——`## 备注`/`### 编辑注记`/
    `---` 都截断，后续行丢弃到下一个本族 header，scoping 与段序无关（taurus
    Minor 6 的推广）。fence 内的行（含 ``` 标记行本身）不进 body——fenced 示例块
    不是 field material，fence 内的标题也不开 entry（mirror check_intro.py
    aries #2——fence 内的条目不算）。"""
    sections: list[tuple[str, str]] = []
    current_label: str | None = None
    current_lines: list[str] = []
    in_fence = False
    pat = re.compile(rf"^##\s+{header_word}\s+(\d+)(?:\s+.*)?$", re.IGNORECASE)
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue  # fence 标记行不进 body（aries B3）
        if in_fence:
            continue  # fence 内容行不进 body（aries B3）
        m = pat.match(line)
        if m:
            if current_label is not None:
                sections.append((current_label, "\n".join(current_lines)))
            current_label = f"{header_word} {m.group(1)}"
            current_lines = []
            continue
        if _SCOPE_TERMINATOR.match(line):
            if current_label is not None:
                sections.append((current_label, "\n".join(current_lines)))
                current_label = None
            continue
        if current_label is not None:
            current_lines.append(line)
    if current_label is not None:
        sections.append((current_label, "\n".join(current_lines)))
    return sections


def _fences_balanced(text: str) -> bool:
    """数 ``` 开头行——奇数 = 存在未闭合 code fence（aries B4：孤 fence 会让后续
    条目被整体吞掉，须显式诊断而非只留误导性的缺席 issue——fail-noisy 好过
    fail-silent）。与 _split_sections 用同一 fence 判定（lstrip 后 ``` 前缀）。"""
    n = sum(1 for line in text.splitlines() if line.lstrip().startswith("```"))
    return n % 2 == 0


def _field_value(body: str, field: str) -> str | None:
    """从 entry body 取字段值。字段形如 `- shared-ref: ...`。找不到返回 None。"""
    m = re.search(rf"^-\s+{re.escape(field)}\s*:\s*(.*)$",
                  body, re.MULTILINE | re.IGNORECASE)
    return m.group(1).strip() if m else None


def _top_level_field(text: str, field: str) -> str | None:
    """从 theory-map.md 全文取 top-level 字段值（`theory-tex: ...`，无 `- ` 前缀）。"""
    m = re.search(rf"^{re.escape(field)}\s*:\s*(.*)$",
                  text, re.MULTILINE | re.IGNORECASE)
    return m.group(1).strip() if m else None


def _is_empty(val: str | None) -> bool:
    if val is None:
        return True
    v = val.strip().lower()
    return v == "" or v in _NONE_TOKENS


def _header_numbers(text: str, word: str) -> set[int]:
    """从 baton 的条目标题提取编号（Shared/Chapter→theory-map/chapter-map）。
    派生自 _split_sections 的 labels——单一 parser，无脱钩可能（taurus I1：
    旧实现的无锚正则与 _split_sections 的全锚正则对 `## Shared 2x` 类行分歧）。"""
    return {int(label.split()[1]) for label, _ in _split_sections(text, word)}


def _single_ref_number(val: str, word: str) -> int | None:
    """从引用值（如 'Shared 1'）提取单个编号。匹配不上或含多个 token 返回 None
    （mirror intro aries #5：一 Overlap→一 Shared/Chapter）。"""
    matches = re.findall(rf"{word}\s+(\d+)", val, re.IGNORECASE)
    if len(matches) != 1:
        return None  # 0 matches (unparseable) OR >1 matches (malformed multi-ref)
    return int(matches[0])


# ANSI/控制序列消毒（aries B5）——\t 与 \n 留（值内合法，且 issue 行本身按行打印）。
_CTRL_RE = re.compile(r"[\x00-\x08\x0b-\x1f\x7f]")


def _sanitize(val: str) -> str:
    """剥离 ANSI/控制序列——issue 行只承载可读文本（aries B5：原始字段值不可
    直接进输出，防终端 title 改写/日志行伪造）。"""
    return _CTRL_RE.sub("", val)


def check(tm_path: Path, cm_path: Path, spine_path: Path, tex_dir: Path) -> list[str]:
    """返回 consistency 问题列表（空 = 通过）。不抛异常——问题进列表。"""
    issues: list[str] = []
    if not tm_path.is_file():
        return [f"✗ {tm_path} 不存在（theory 未产？跑 thesis-theory）"]
    try:
        text = tm_path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        return [f"✗ {tm_path} 不是有效的 UTF-8 文本（二进制？）"]
    except OSError as e:
        return [f"✗ {tm_path} 无法读取：{e}"]

    shareds = _split_sections(text, "Shared")
    overlaps = _split_sections(text, "Overlap")
    if not _fences_balanced(text):
        issues.append(f"✗ {tm_path} 存在未闭合 code fence——其后条目可能被整体跳过（检查 ``` 标记配对）")

    # 读 chapter-map.md 的章号集合（Shared grounded-in + Overlap chapter-ref 用）
    chapter_nums: set[int] = set()
    if not cm_path.is_file():
        issues.append(f"✗ {cm_path} 不存在（dissect 未产？theory 需 chapter-map.md 做 cross-ref）")
    else:
        try:
            cm_text = cm_path.read_text(encoding="utf-8-sig")
            chapter_nums = _header_numbers(cm_text, "Chapter")
            if not chapter_nums:
                issues.append(f"✗ {cm_path} 可读但无任何 ## Chapter N 条目 — grounded-in/chapter-ref cross-ref 跳过")
        except (UnicodeDecodeError, OSError):
            issues.append(f"✗ {cm_path} 不可读（二进制/权限）— grounded-in/chapter-ref cross-ref 跳过")

    # --- spine 复验（第 4 参数的职责——handoff 时关掉 mid-write backtrack 窗口，spec §⑥ #5 / T1）---
    if not spine_path.is_file():
        issues.append(f"✗ {spine_path} 不存在（spine 未产？theory 需 thesis-spine.md）")
    else:
        try:
            spine_text = spine_path.read_text(encoding="utf-8-sig")
            if PENDING_MARKER in spine_text:
                issues.append(f"✗ {spine_path} 含 {PENDING_MARKER} 残留——spine 被重开（mid-write backtrack？），"
                              "theory-map 的 instantiates-framework 可能陈旧（spec §⑥ #5）")
        except (UnicodeDecodeError, OSError):
            issues.append(f"✗ {spine_path} 不可读（二进制/权限）— spine 复验跳过")

    # --- extraction-outcome top-level 字段（T3 终态）---
    outcome = _top_level_field(text, "extraction-outcome")
    if outcome is None:
        issues.append("✗ theory-map.md 缺 top-level `extraction-outcome` 字段"
                      "（confirmed / waived-by-author——候选全否决的落盘终态，spec §Step 1 fallback）")
        outcome = ""
    outcome = outcome.strip().lower()
    if outcome not in (OUTCOME_CONFIRMED, OUTCOME_WAIVED) and outcome != "":
        issues.append(f"✗ extraction-outcome `{_sanitize(outcome)}` 非法（应为 confirmed 或 waived-by-author）")

    # --- Shared 条目检查（waived 模式下存在即矛盾；confirmed 模式逐字段）---
    shared_nums: set[int] = set()
    for label, body in shareds:
        shared_nums.add(int(label.split()[1]))
        if outcome == OUTCOME_WAIVED:
            issues.append(f"✗ {label} 存在于 waived-by-author 终态（waived = 作者裁了最小章——Shared/Overlap 段须空，spec §Step 1 fallback）")
            continue
        if _is_empty(_field_value(body, "component")):
            issues.append(f"✗ {label} component 缺失或为空")
        if _is_empty(_field_value(body, "instantiates-framework")):
            issues.append(f"✗ {label} instantiates-framework 缺失或为空（门「共用理论 grounded 在主线框架」的机械面——非空即查，好坏归 eval+作者）")
        gi = _field_value(body, "grounded-in")
        if _is_empty(gi):
            issues.append(f"✗ {label} grounded-in 缺失或为空")
        else:
            nums = {int(x) for x in re.findall(r"chapter\s+(\d+)", gi, re.IGNORECASE)}
            if len(nums) < 2:
                issues.append(f"✗ {label} grounded-in `{_sanitize(gi)}` 解析出 <2 个不同章（共用组件的定义下限：≥2 章）")
            elif chapter_nums and not nums <= chapter_nums:
                bad = ", ".join(str(x) for x in sorted(nums - chapter_nums))
                issues.append(f"✗ {label} grounded-in 引用 Chapter {bad} 不在 chapter-map.md 的章列表中（悬空/编造）")
        st = _field_value(body, "status")
        if st is None:
            issues.append(f"✗ {label} 缺 status")
        elif st.lower() != SHARED_SETTLED:
            issues.append(f"✗ {label} status={st}（应为 confirmed——作者 depth gate 痕迹；pending=AI 候选未 settle，never auto-adopted）")

    # --- vacuous-pass guard：confirmed 但 Shared 段空（T3——缺席拦截）---
    if outcome == OUTCOME_CONFIRMED and not shareds:
        issues.append("✗ extraction-outcome=confirmed 但 Shared 段为空（要么 ≥1 条 confirmed 组件，要么落 waived-by-author 终态——无静默第三态，spec §⑥ #2）")

    # --- Overlap 条目检查（不 enforce resolution——resolver 是作者，glossary Overlap 清单）---
    for label, body in overlaps:
        if outcome == OUTCOME_WAIVED:
            issues.append(f"✗ {label} 存在于 waived-by-author 终态（waived = Shared/Overlap 段须空）")
            continue
        sr = _field_value(body, "shared-ref")
        if _is_empty(sr):
            issues.append(f"✗ {label} shared-ref 缺失或为空")
        else:
            n = _single_ref_number(sr, "Shared")
            if n is None:
                issues.append(f"✗ {label} shared-ref `{_sanitize(sr)}` 无法解析单个 Shared 号（应为 'Shared N' 格式）")
            elif shared_nums and n not in shared_nums:
                issues.append(f"✗ {label} shared-ref Shared {n} 不在 theory-map.md 的 Shared 列表中（悬空/编造）")
        cr = _field_value(body, "chapter-ref")
        if _is_empty(cr):
            issues.append(f"✗ {label} chapter-ref 缺失或为空")
        else:
            cn = _single_ref_number(cr, "Chapter")
            if cn is None:
                issues.append(f"✗ {label} chapter-ref `{_sanitize(cr)}` 无法解析单个 Chapter 号（应为 'Chapter N' 格式）")
            elif chapter_nums and cn not in chapter_nums:
                issues.append(f"✗ {label} chapter-ref Chapter {cn} 不在 chapter-map.md 的章列表中（悬空/编造）")
        for fld in ("theory-§", "chapter-§", "suggested-disposition"):
            if _is_empty(_field_value(body, fld)):
                issues.append(f"✗ {label} {fld} 缺失或为空")
        # 注意：disposition（作者事后填）不查——resolver 是作者，无下游 enforce（§③）；
        # 也不查"每条提升位置都有 Overlap"——覆盖完整性是 absent 类，eval + 写后纪律（T5）。

    # --- theory-tex top-level 字段（template-derived，非硬编码；含路径守卫 + stat 兜底）---
    tex_name = _top_level_field(text, "theory-tex")
    if tex_name is None or not tex_name.strip():
        issues.append("✗ theory-map.md 缺 top-level `theory-tex` 字段（理论章文件名，按 template-spec.md——init 预留的 chapter1 槽位）")
    else:
        tex_name = tex_name.strip()
        tex_pure = PurePath(tex_name)
        if tex_pure.is_absolute() or ".." in tex_pure.parts:
            issues.append(f"✗ theory-tex `{_sanitize(tex_name)}` 在 thesis/tex/ 之外（绝对路径或 `..` 遍历，禁止）")
        else:
            try:
                tex_exists = (tex_dir / tex_name).is_file()
            except (OSError, ValueError) as e:
                tex_exists = None
                issues.append(f"✗ theory-tex 值无法检验（{e}）——路径超长/非法")
            if tex_exists is False:
                issues.append(f"✗ theory-tex `{_sanitize(tex_name)}` 不存在于 {tex_dir}（theory 未写理论章 tex？）")
    return issues


def main(argv: list[str]) -> int:
    tm_path = Path(argv[1]) if len(argv) > 1 else Path("sci-skills") / "thesis-theory" / "theory-map.md"
    cm_path = Path(argv[2]) if len(argv) > 2 else Path("sci-skills") / "thesis-dissect" / "chapter-map.md"
    spine_path = Path(argv[3]) if len(argv) > 3 else Path("sci-skills") / "thesis-spine.md"
    tex_dir = Path(argv[4]) if len(argv) > 4 else Path("thesis") / "tex"
    issues = check(tm_path, cm_path, spine_path, tex_dir)
    if issues:
        print(f"check_theory: {len(issues)} 个 consistency 问题 @ {tm_path}:")
        for it in issues:
            print(f"  {it}")
        return 1
    print(f"check_theory: ✓ consistency 通过 @ {tm_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
