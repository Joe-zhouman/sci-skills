# thesis-spine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `thesis-spine` — the writing-chain entry skill of the sci-skills-thesis family (establishes main line + unified framework + inter-chapter progression + thesis-level claim umbrella from N small papers, before any chapter is dissected) — plus create the `sci-skills-thesis` plugin it lives in.

**Architecture:** Mirror the article family's compass-file coupling. thesis-spine lives in a NEW plugin `sci-skills-thesis/` (sibling to `sci-skills-article/`, created by this plan — the foundation only built the shared `sci-skills` plugin with thesis-init). It is a PROSE skill (judgment-heavy workflow): the SKILL.md is the primary artifact, the script is a helper. It produces the top-level `thesis-spine.md` baton (read by dissect/intro/summary/theory) + seeds `thesis-terminology-ledger.md`, reading `thesis-sources.md` + `template-spec.md` + the N small papers. **No working-notes dir** (respects spec §② + the merged foundation layout — zero churn to thesis-init). The coverage gate (`scripts/check_spine.py`) is COVERAGE ONLY (3 structural fields + sub-coverage + no-pending); umbrella + boundary are depth (human-gated), NOT checked by the script — this split is load-bearing (spec §⑥ + §门, aquarius-verified).

**Tech Stack:** Python 3.11+ stdlib (pathlib, re, sys, argparse) for check_spine.py; stdlib `assert` test script (no pytest — mirrors thesis-init's justified deviation); Claude Code plugin manifest; markdown for SKILL.md + references.

**Spec:** `docs/superpowers/specs/thesis-spine.md` (aquarius round-3 "Lean. Ship.", user-approved — the authority; read it in full before implementing).
**Parent spec:** `docs/superpowers/specs/thesis-skill-family.md` (family source-of-truth).
**Glossary:** `docs/superpowers/glossary.md` (6 thesis terms — use verbatim).
**Mirror patterns:** `sci-skills-article/.claude-plugin/plugin.json` (manifest), `sci-skills-article/skills/sci-write/SKILL.md` (prose-skill structure + references/ + tests/README.md), `sci-skills/skills/thesis-init/scripts/init_project.py` + `test_init.py` (stdlib test shape + justified deviation).

---

## File Structure

This plan creates:

- `sci-skills-thesis/.claude-plugin/plugin.json` — NEW plugin manifest (mirrors sci-skills-article's)
- `sci-skills-thesis/skills/thesis-spine/SKILL.md` — the prose workflow (primary artifact)
- `sci-skills-thesis/skills/thesis-spine/scripts/check_spine.py` — coverage mechanical gate (deterministic, stdlib)
- `sci-skills-thesis/skills/thesis-spine/scripts/test_check_spine.py` — stdlib assert tests
- `sci-skills-thesis/skills/thesis-spine/references/writing-discipline.md` — tension-flagging protocol + confirmation gate + pending protocol (load-on-demand)
- `sci-skills-thesis/skills/thesis-spine/references/spine-schema.md` — full thesis-spine.md template (load-on-demand)
- `sci-skills-thesis/skills/thesis-spine/tests/README.md` — test plan doc (script + eval split)

**Decision-ladder outcomes baked in:**
- plugin.json → Rung 4 (mirror sci-skills-article's existing manifest exactly; only name/description/keywords differ)
- check_spine.py → Rung 7 (must write; deterministic coverage gate with verifiable outputs — the case skill-creator-plus/testing.md says earns a runnable test). Stdlib only (Rung 3: `re`, `pathlib`, `sys`, `argparse`).
- SKILL.md / references / tests/README → prose (the skill's value is the workflow + gates + tension-flagging discipline, not code)
- No `allowed-tools` frontmatter field → mirror sci-write/sci-story (prose skills omit it; use runtime tools). Spine uses Read (tex/sources) + `mcp__extract__analyze_doc` (PDF — global rule, never Read on PDF) + Write + Bash. No WebFetch (tension evidence is in the papers, not external search; literature search is intro's job). No vision (intake is text claim+structure, not image analysis).

---

## Pre-flight: open feature branch

> thesis-spine work happens on a feature branch, NOT master (foundation is merged on master; don't build on it directly). Do this before Task 1.

- [ ] **Step 0: Create the feature branch**

```bash
cd /home/joe/Documents/repo/skill/sci-skills
git checkout -b thesis-spine
```

Expected: `Switched to a new branch 'thesis-spine'`.

---

## Task 1: Plugin scaffold

**Files:**
- Create: `sci-skills-thesis/.claude-plugin/plugin.json`
- Create: `sci-skills-thesis/skills/thesis-spine/.gitkeep` (tracks the dir until SKILL.md lands in Task 4)

- [ ] **Step 1: Create the plugin manifest**

Write `sci-skills-thesis/.claude-plugin/plugin.json` (mirror `sci-skills-article/.claude-plugin/plugin.json` exactly — only name/description/version/keywords differ; author/homepage/repo/license identical):

```json
{
  "name": "sci-skills-thesis",
  "description": "sci-skills thesis family — turn N published papers into a degree thesis (重组延伸, not from-scratch). The writing chain: spine, dissect, intro, theory, summary, typeset, polish. thesis-init (shared infra) lives in the sci-skills plugin. Claude Code only.",
  "version": "0.1.0",
  "author": {
    "name": "Joe-zhouman",
    "email": "joe_zm@foxmail.com"
  },
  "homepage": "https://github.com/Joe-zhouman/sci-skills",
  "repository": "https://github.com/Joe-zhouman/sci-skills",
  "license": "MIT",
  "keywords": ["skills", "research", "thesis", "dissertation", "academic-writing", "sci-skills"]
}
```

- [ ] **Step 2: Create the skill dir placeholder**

```bash
mkdir -p sci-skills-thesis/skills/thesis-spine/scripts
mkdir -p sci-skills-thesis/skills/thesis-spine/references
mkdir -p sci-skills-thesis/skills/thesis-spine/tests
touch sci-skills-thesis/skills/thesis-spine/.gitkeep
```

- [ ] **Step 3: Verify manifest is valid JSON + plugin is a sibling**

Run:
```bash
python3 -c "import json; d=json.load(open('sci-skills-thesis/.claude-plugin/plugin.json')); assert d['name']=='sci-skills-thesis'; print('ok')"
ls -d sci-skills-thesis sci-skills-article sci-skills
```
Expected: `ok` then the three plugin dirs listed (sci-skills-thesis is a new sibling, NOT inside sci-skills/).

- [ ] **Step 4: Commit**

```bash
git add sci-skills-thesis/
git commit -m "thesis-spine: scaffold sci-skills-thesis plugin + thesis-spine skill dirs"
```

---

## Task 2: check_spine.py — core coverage (no-pending + 3 structural fields non-empty)

> TDD. check_spine.py is deterministic code with verifiable outputs → earns a runnable stdlib test (mirror thesis-init's justified deviation). This task builds the core coverage checks; Task 3 adds sub-coverage (per-paper instantiation + per-role advance/question).

**Files:**
- Create: `sci-skills-thesis/skills/thesis-spine/scripts/test_check_spine.py`
- Create: `sci-skills-thesis/skills/thesis-spine/scripts/check_spine.py`

- [ ] **Step 1: Write the failing tests for core coverage**

Create `sci-skills-thesis/skills/thesis-spine/scripts/test_check_spine.py`:

```python
"""stdlib tests for check_spine.py — run: python3 test_check_spine.py"""
import importlib.util, pathlib, sys, tempfile, os
HERE = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("check_spine", HERE / "check_spine.py")
check_spine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_spine)

# --- fixtures ---
SETTLED = """# thesis-spine.md
> Baton. `pending` = AI candidate, NOT author-adopted.

## Main line (主线)
N 篇小论文统一于 X 框架，共同贡献了 Y。

## Unified framework (统一框架)
the X framework
per-paper: how paper-A instantiates it = 侧视角1
per-paper: how paper-B instantiates it = 侧视角2

## Inter-chapter progression (章间递进)
ordered:
- role 1: question = X 怎么起作用?; advances the main line by 建立 baseline
- role 2: question = X 在 B 条件下?; advances the main line by 拓展 boundary

## Thesis-level claim (umbrella)
本 thesis establish 了 Y（三结构字段 collectively argue 它）。

## Boundary
本 thesis 不 establish Z。

## Intake (per-paper evidence base)
- paper-A: claim = …; structure = IMRaD; how it could fit a main line = 侧视角1
- paper-B: claim = …; structure = IMRaD; how it could fit a main line = 侧视角2

## Cracks flagged (tension-flagging, §⑤)
- [stage 1 / main line] (a) tension: … (b) evidence: … (c) question: …?
  disposition: [dismissed → reason: …]

## Alternatives considered
- main line: considered <alt>, rejected because <reason>
"""

def _write_fixture(content: str) -> pathlib.Path:
    p = pathlib.Path(tempfile.mkdtemp()) / "thesis-spine.md"
    p.write_text(content, encoding="utf-8")
    return p

def test_passes_on_settled_spine():
    issues = check_spine.check(_write_fixture(SETTLED))
    assert issues == [], f"expected pass, got: {issues}"
    print("test_passes_on_settled_spine: PASS")

def test_fails_on_pending_marker():
    bad = SETTLED.replace("## Main line (主线)\nN 篇",
                          "## Main line (主线)\n[pending? ] N 篇")
    issues = check_spine.check(_write_fixture(bad))
    assert any("pending" in i.lower() for i in issues), f"expected pending issue, got: {issues}"
    print("test_fails_on_pending_marker: PASS")

def test_fails_on_empty_structural_field():
    bad = SETTLED.replace("## Main line (主线)\nN 篇小论文统一于 X 框架，共同贡献了 Y。",
                          "## Main line (主线)\n")
    issues = check_spine.check(_write_fixture(bad))
    assert any("main line" in i.lower() and ("空" in i or "empt" in i.lower()) for i in issues), \
           f"expected empty-main-line issue, got: {issues}"
    print("test_fails_on_empty_structural_field: PASS")

def test_fails_on_missing_structural_section():
    bad = SETTLED.replace("## Unified framework (统一框架)\nthe X framework\nper-paper: how paper-A instantiates it = 侧视角1\nper-paper: how paper-B instantiates it = 侧视角2\n",
                          "")
    issues = check_spine.check(_write_fixture(bad))
    assert any("unified framework" in i.lower() for i in issues), f"expected missing-section issue, got: {issues}"
    print("test_fails_on_missing_structural_section: PASS")

def test_ignores_umbrella_and_boundary():
    """Load-bearing: an EMPTY umbrella + EMPTY boundary still passes coverage —
    they are depth (human-gated), NOT coverage. check_spine must not check them."""
    bad = SETTLED.replace("## Thesis-level claim (umbrella)\n本 thesis establish 了 Y（三结构字段 collectively argue 它）。",
                          "## Thesis-level claim (umbrella)\n")  # empty umbrella
    bad = bad.replace("## Boundary\n本 thesis 不 establish Z。",
                      "## Boundary\n")  # empty boundary
    issues = check_spine.check(_write_fixture(bad))
    assert issues == [], f"empty umbrella/boundary must NOT fail coverage (they're depth): {issues}"
    print("test_ignores_umbrella_and_boundary: PASS")

if __name__ == "__main__":
    test_passes_on_settled_spine()
    test_fails_on_pending_marker()
    test_fails_on_empty_structural_field()
    test_fails_on_missing_structural_section()
    test_ignores_umbrella_and_boundary()
    print("ALL CORE TESTS PASS")
```

- [ ] **Step 2: Run tests — verify they fail (module not found)**

```bash
cd sci-skills-thesis/skills/thesis-spine/scripts && python3 test_check_spine.py
```
Expected: `ModuleNotFoundError` / `FileNotFoundError` (check_spine.py doesn't exist yet).

- [ ] **Step 3: Implement check_spine.py core**

Create `sci-skills-thesis/skills/thesis-spine/scripts/check_spine.py`:

```python
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
PENDING_MARKER = "[pending"


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
    text = spine_path.read_text(encoding="utf-8")

    # 1. 无 pending 残留（settled 后作者删 [pending? ] 标记）
    if PENDING_MARKER in text:
        issues.append("✗ 仍有 `[pending` 标记——有未 settle 的候选，dissect 不可建在 unsettled 字段上")

    sections = split_sections(text)

    # 2. 3 结构字段存在且非空
    for field in STRUCTURAL_FIELDS:
        body = _find_section(sections, field)
        if body is None:
            issues.append(f"✗ 结构字段 `## {field}` 缺失")
        elif not body.strip():
            issues.append(f"✗ 结构字段 `## {field}` 为空")

    # sub-coverage（Task 3 在此扩展：framework 每篇实例化 + progression 每角色 advance/question）
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
```

- [ ] **Step 4: Run tests — verify the 4 core tests pass (sub-coverage test from Task 3 not yet present)**

```bash
cd sci-skills-thesis/skills/thesis-spine/scripts && python3 test_check_spine.py
```
Expected: `test_passes_on_settled_spine: PASS` ... `test_ignores_umbrella_and_boundary: PASS` then `ALL CORE TESTS PASS`. (`test_ignores_umbrella_and_boundary` is the load-bearing one — confirms the script does NOT gate depth.)

- [ ] **Step 5: Commit**

```bash
git add sci-skills-thesis/skills/thesis-spine/scripts/
git commit -m "thesis-spine: check_spine.py core coverage (no-pending + 3 structural fields; depth NOT checked)"
```

---

## Task 3: check_spine.py — sub-coverage (per-paper instantiation + per-role advance/question)

> TDD. Extends check() with the two sub-coverage checks from spec §门: framework has per-paper instantiation for each Intake paper; progression has per-role question + advance.

**Files:**
- Modify: `sci-skills-thesis/skills/thesis-spine/scripts/test_check_spine.py`
- Modify: `sci-skills-thesis/skills/thesis-spine/scripts/check_spine.py`

- [ ] **Step 1: Append failing tests for sub-coverage**

Append to `test_check_spine.py` (before the `if __name__` block — and update `__main__` per Step 4):

```python
def test_fails_on_missing_per_paper_instantiation():
    """Intake 列了 paper-B 但 Unified framework 无其实例化 → contract gap。"""
    bad = SETTLED.replace("per-paper: how paper-B instantiates it = 侧视角2\n",
                          "")  # paper-B instantiation gone, but still in Intake
    issues = check_spine.check(_write_fixture(bad))
    assert any("paper-B" in i for i in issues), f"expected missing-instantiation issue for paper-B, got: {issues}"
    print("test_fails_on_missing_per_paper_instantiation: PASS")

def test_fails_on_role_missing_advance():
    """progression role 缺 advance → coverage 问题。"""
    bad = SETTLED.replace("advances the main line by 拓展 boundary",
                          "")  # role 2 now has question but no advance
    issues = check_spine.check(_write_fixture(bad))
    assert any("advance" in i.lower() for i in issues), f"expected missing-advance issue, got: {issues}"
    print("test_fails_on_role_missing_advance: PASS")

def test_fails_on_role_missing_question():
    """progression role 缺 question → coverage 问题。"""
    bad = SETTLED.replace("question = X 怎么起作用?;", "")
    issues = check_spine.check(_write_fixture(bad))
    assert any("question" in i.lower() for i in issues), f"expected missing-question issue, got: {issues}"
    print("test_fails_on_role_missing_question: PASS")
```

- [ ] **Step 2: Run — verify the 3 new tests fail**

```bash
cd sci-skills-thesis/skills/thesis-spine/scripts && python3 test_check_spine.py
```
Expected: the 3 new tests fail (sub-coverage not implemented — no issue raised where one is expected). The Task-2 core tests still pass.

- [ ] **Step 3: Implement sub-coverage in check()**

In `check_spine.py`, replace the `# sub-coverage（Task 3 ...）` placeholder line with:

```python
    # 3. Unified framework: 每篇 Intake 论文都有实例化行（contract gap 否则）
    intake = _find_section(sections, "Intake") or ""
    framework = _find_section(sections, "Unified framework") or ""
    if framework:
        paper_ids = re.findall(r"^-\s+(paper-[\w-]+)", intake, re.MULTILINE)
        for pid in paper_ids:
            if pid not in framework:
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
```

- [ ] **Step 4: Update `__main__` to run all tests + verify all pass**

Replace the `__main__` block in `test_check_spine.py` with:

```python
if __name__ == "__main__":
    test_passes_on_settled_spine()
    test_fails_on_pending_marker()
    test_fails_on_empty_structural_field()
    test_fails_on_missing_structural_section()
    test_ignores_umbrella_and_boundary()
    test_fails_on_missing_per_paper_instantiation()
    test_fails_on_role_missing_advance()
    test_fails_on_role_missing_question()
    print("ALL TESTS PASS")
```

Run:
```bash
cd sci-skills-thesis/skills/thesis-spine/scripts && python3 test_check_spine.py
```
Expected: 8 `: PASS` lines then `ALL TESTS PASS`.

- [ ] **Step 5: Commit**

```bash
git add sci-skills-thesis/skills/thesis-spine/scripts/
git commit -m "thesis-spine: check_spine.py sub-coverage (per-paper instantiation + per-role advance/question)"
```

---

## Task 4: SKILL.md (the prose workflow — primary artifact)

> Prose, not TDD. The SKILL.md IS the skill's value (workflow + gates + tension-flagging discipline). check_spine.py (Tasks 2–3) already exists for SKILL.md to reference. Mirror `sci-skills-article/skills/sci-write/SKILL.md`'s structure (frontmatter → Layout & boundaries → File contracts → Workflow → Pervasive discipline → Reference index → Privacy).

**Files:**
- Create: `sci-skills-thesis/skills/thesis-spine/SKILL.md`
- Delete: `sci-skills-thesis/skills/thesis-spine/.gitkeep` (SKILL.md replaces it as the dir tracker)

- [ ] **Step 1: Write the SKILL.md**

Write `sci-skills-thesis/skills/thesis-spine/SKILL.md` with this frontmatter (NO `allowed-tools` field — mirror sci-write/sci-story; spine is a prose skill using runtime tools: Read for tex/sources, `mcp__extract__analyze_doc` for PDFs (global rule — never Read on PDF), Write, Bash):

```markdown
---
name: thesis-spine
description: >-
  Thesis writing-chain entry — establish the main line (主线) + unified framework (统一框架)
  + inter-chapter progression (章间递进) + thesis-level claim (umbrella) from N small papers,
  BEFORE any chapter is dissected. Staged depth-gates with backtrack; AI proposes candidates
  marked `pending` (never auto-adopted) and tension-flags (questions, not verdicts); the author
  gates architecture depth (AI cannot honestly audit depth — it generates the shallowness it
  checks). Produces thesis-spine.md (the baton dissect/intro/summary/theory read) + seeds
  thesis-terminology-ledger.md. Reads thesis-sources.md + template-spec.md + the small papers
  (high-level intake only — no deep reading, no tex, no paper→chapter binding; those are
  dissect's job). Triggers: 提主线, 统一框架, 章间递进, thesis spine, 主线框架, thesis-level claim.
---
```

Body must cover (mirror sci-write's section structure; pull exact content from `docs/superpowers/specs/thesis-spine.md` — the spec is the authority, cite its §numbers):

1. **One-line positioning** (after the `# thesis-spine` H1): thesis-spine establishes the architecture-level baton before any chapter is dissected; it does NOT deep-read papers, write tex, or bind paper→chapter (those are dissect). Run before dissect, after init. The author advances the pipeline by invoking each writing skill (read neighbors, don't orchestrate).

2. **The core discipline (state upfront — this is the family's anti-pattern defense):**
   - **AI proposes candidates marked `pending`, never auto-adopts.** A field still marked `pending` is unsettled — dissect must not build on it.
   - **AI tension-flags = questions to the author, never verdicts.** Each tension: (a) the tension, (b) specific evidence (paper/figure/§), (c) a question for the author. AI never asserts "this framework is shallow" — that's depth-gating, forbidden. (Detail in `references/writing-discipline.md`.)
   - **The honest residual (state it, don't hide it):** tension-flagging is depth-INFLUENCE, not depth-gating. AI deciding which tensions to raise biases the author's attention — attachment-blind authors may be led by the framing. This is an irreducible residual, named as a stated failure mode, not solved. AI's one real edge over the author is the absence of attachment; tension-flagging preserves it without crossing into depth-gating.
   - **Depth is human-gated only.** Is the main line sharp? framework high-level or hollow? progression insightful? umbrella overclaim? AI cannot honestly check these — checking "is this framework deep" produces the shallowness it checks. The author gates depth; AI assists.

3. **Layout & boundaries** (paste the spec's file-contract table from §跨 skill 文件交接; state: spine produces top-level `thesis-spine.md` + seeds `thesis-terminology-ledger.md`; NO working-notes dir; reads `thesis-sources.md` + `template-spec.md` + small papers; check_spine.py is spine's own helper at `scripts/check_spine.py`).

4. **File contracts** — table of: `thesis-spine.md` (spine produces; dissect/intro/summary/theory read; schema in `references/spine-schema.md`), `thesis-terminology-ledger.md` (spine seeds; chapters/polish co-write), `thesis-sources.md` (init produces; spine reads), `template-spec.md` (init produces; spine reads), small papers (external; spine reads), `scripts/check_spine.py` (spine's own; Step 5 runs it).

5. **Workflow** — the 6 steps from spec §工作流, each as an H3:
   - **Step 0 — Read the room (startup/resume)**: read `thesis-sources.md` (hard stop if missing/empty → "run thesis-init and fill the registry first"); read each small paper per registry `paths` for HIGH-LEVEL INTAKE ONLY (claim + IMRaD structure + how it could fit a main line → write `## Intake` in spine.md). **Tex → Read; PDF → `mcp__extract__analyze_doc` (never Read on PDF — global rule).** read `template-spec.md` (chapter-naming so progression roles align); seed `thesis-terminology-ledger.md` from cross-paper terms (mark `source: thesis-spine`). On resume: if spine.md has settled sections (no `pending`), skip to the first unsettled stage; Intake persists so no re-reading papers.
   - **Step 1 — Main line (主线 thread)** (depth human-gate): AI proposes main-line candidates (`pending`, one-sentence thread connecting the N papers, grounded in intake). AI tension-flags. **Stop. Author gates depth** (is the thread sharp?). Settled → `## Main line`.
   - **Step 2 — Unified framework (统一框架)** (depth human-gate): AI proposes framework candidates (`pending`, builds on the confirmed main line — the framework + how each paper instantiates it). AI tension-flags. **Stop. Author gates depth.** Settled → `## Unified framework`. **Coverage check (mechanical)**: each paper declares instantiation — a paper lacking it is a contract gap, ask the author.
   - **Step 3 — Inter-chapter progression (章间递进)** (depth human-gate): AI proposes progression candidates (`pending` — research-chapter ROLES in sequence, default 1:1 with N papers; each role: its question + how it advances the main line; paper-agnostic, NOT paper→chapter bindings). AI tension-flags. **Stop. Author gates depth.** Settled → `## Inter-chapter progression`. **Coverage check**: each role declares advance + question.
   - **Step 4 — Thesis-level claim (umbrella) + Boundary** (depth human-gate): now the 3 structural fields are settled, AI proposes the umbrella candidate (`pending` — one-sentence total contribution that the 3 fields collectively argue). AI tension-flags (overclaim beyond what the 3 fields establish? hollow?). Define `## Boundary` (what the umbrella does NOT establish; mirror sci-write's claim.md boundary). **Stop. Author gates depth.** Settled → `## Thesis-level claim` + `## Boundary`.
   - **Step 5 — Handoff**: run `python scripts/check_spine.py <project>/sci-skills/thesis-spine.md` (coverage mechanical gate: no `pending` + 3 structural fields non-empty + sub-coverage; **umbrella + boundary are NOT checked — they're depth**). If it passes, spine.md is the settled baton. Point the author to **thesis-dissect** (binds papers to the progression roles, 拆即写). Do NOT auto-run it.
   - **Backtrack**: at any depth-gate, if the author finds an earlier component wrong (e.g. framework won't propose cleanly → main line is wrong), revise the earlier component and re-propose downstream. Re-mark downstream candidates `pending`.

6. **Pervasive discipline** (runs around every stage; detail in `references/writing-discipline.md`): confirmation gate before each stage settles; tension-flagging is questions-not-verdicts + the depth-influence stated failure mode; `pending` protocol (never auto-adopt); verb calibration (state contributions with strong verbs, hedge interpretations); the honest boundary (decoupling prevents ABSENT spines, not HOLLOW ones — spec §Load-bearing premise).

7. **Reference index** — table: `references/writing-discipline.md` (before any stage — tension-flagging protocol, confirmation gate, pending protocol, depth-influence failure mode, verb calibration) | `references/spine-schema.md` (the full thesis-spine.md template — what each section holds).

8. **Privacy**: don't leak private paths, filenames, or unpublished paper content in spine.md's Intake/Cracks, user-facing replies, or commit messages. Use generic descriptions ("paper-C §4.2"); reveal exact paths only when the author asks for an audit trail.

Write the full body following sci-write's tone and structure. Use the spec (`docs/superpowers/specs/thesis-spine.md`) §Implementation Notes for exact schema/workflow/gates; cite spec §numbers where the reader should look for rationale.

- [ ] **Step 2: Verify it parses as a skill + key invariants are present**

Run:
```bash
python3 -c "
t = open('sci-skills-thesis/skills/thesis-spine/SKILL.md').read()
assert t.startswith('---'), 'missing frontmatter'
fm = t.split('---')[1]
assert 'name: thesis-spine' in fm, 'missing name'
assert 'allowed-tools' not in fm, 'spine is prose — must NOT declare allowed-tools (mirror sci-write)'
body = t.split('---',2)[2]
for needle in ['Step 0', 'Step 4', 'depth-INFLUENCE', 'never auto-adopt', 'check_spine.py', 'dissect', 'mcp__extract__analyze_doc']:
    assert needle in body, f'missing: {needle}'
# depth must NOT be checkable by the script — state it
assert 'umbrella' in body.lower() and 'depth' in body.lower()
print('ok')
"
```
Expected: `ok`. (The `allowed-tools` assertion is the load-bearing one — spine is prose, mirrors sci-write.)

- [ ] **Step 3: Remove the .gitkeep (SKILL.md now tracks the dir) + commit**

```bash
git rm sci-skills-thesis/skills/thesis-spine/.gitkeep
git add sci-skills-thesis/skills/thesis-spine/SKILL.md
git commit -m "thesis-spine: SKILL.md — staged-gate workflow, tension-flagging (questions not verdicts), depth human-gate"
```

---

## Task 5: references/ (prose depth refs, load-on-demand)

> Prose. Two reference files SKILL.md indexes (Task 4). Mirror `sci-skills-article/skills/sci-write/references/` structure (each file is opened on demand by a trigger, not every run).

**Files:**
- Create: `sci-skills-thesis/skills/thesis-spine/references/writing-discipline.md`
- Create: `sci-skills-thesis/skills/thesis-spine/references/spine-schema.md`

- [ ] **Step 1: Write references/writing-discipline.md**

The depth reference, opened before any stage. Must cover (mirror sci-write's `writing-discipline.md` shape; pull exact protocol from spec §⑤ + §门):

1. **Confirmation gate** — before each stage settles, echo the candidate + the tension(s) + the depth question for the author. The author confirms/rewrites/rejects before the next stage builds on it. (Mirror sci-write's confirmation gate.)
2. **Tension-flagging protocol (the core — spec §⑤)**:
   - Form: a **question** to the author, with three elements: (a) the tension, (b) specific evidence anchored to a paper/figure/§, (c) a question for the author.
   - **Never a verdict.** Forbidden forms: "this framework is shallow," "the main line isn't sharp enough," "this progression is weak." Those are depth-gating — AI generates the shallowness it checks.
   - Author dispositions: `fatal → revised` (the candidate is revised) or `dismissed → reason: …` (the author judges the tension doesn't hold, with a reason). Disposition is recorded in `## Cracks flagged` — dissect/summary inherit the record that the author knew and disposed, NOT an AI verdict.
   - **The honest residual (state it explicitly — aquarius round-1 load-bearing finding):** tension-flagging is depth-INFLUENCE, not depth-gating. AI choosing which tensions to raise biases the author's attention; attachment-blind authors may be led by the framing (see only what AI raised, miss what it didn't). This is irreducible — any AI participation in raising tensions has framing influence. The skill accepts and names this residual; it does not pretend to eliminate it. AI's one real edge over the author is the absence of attachment (the author has feeling for their own work; AI doesn't) — tension-flagging preserves this edge without crossing into depth-gating.
   - **Why not drop it / restrict to fact-checks:** dropping it abandons AI's only edge, leaving the author alone against their own attachment blind spot. Restricting to verifiable fact-checks makes it redundant with the coverage/grounding mechanical layer (which already checks cross-consistency). The unique value IS the attachment-blind tension — which IS the depth-influence, accepted+bounded. (Spec §⑤ rejected the figN-reading "fact-check" analogy as false equivalence.)
3. **`pending` protocol** — every AI candidate is marked `pending`; the author adopts by removing the marker. A field still marked `pending` is unsettled — dissect must not build on it. check_spine.py fails on any `[pending` marker. Never auto-adopt.
4. **Verb calibration** — state contributions with strong verbs (establishes / shows / demonstrates); hedge interpretations (may / suggests / indicates). Mirror sci-write's verb discipline.
5. **The honest boundary (spec §Load-bearing premise)** — file handoff (dissect can't proceed without spine.md) prevents ABSENT spines, not HOLLOW ones. A hollow spine can pass coverage + author confirmation if the author's judgment is insufficient (attachment + tension framing bias compound). No structural mechanism replaces author judgment. Named honestly, not overclaimed.

- [ ] **Step 2: Write references/spine-schema.md**

The full `thesis-spine.md` template (copy verbatim from spec §thesis-spine.md schema — the code block at spec lines 133–168). Add a one-line header: "The baton's schema. spine writes this; check_spine.py gates the 3 structural fields (coverage); umbrella + boundary are depth (human-gated, NOT checked by the script)." Then the template block. Then a short "what each section is for" table (product sections vs evidence/audit sections — mirror claim.md's product+evidence co-location).

- [ ] **Step 3: Commit**

```bash
git add sci-skills-thesis/skills/thesis-spine/references/
git commit -m "thesis-spine: references/ — writing-discipline (tension-flagging protocol + depth-influence failure mode) + spine-schema template"
```

---

## Task 6: tests/README.md (test plan doc)

> Prose. Mirror `sci-skills-article/skills/sci-write/tests/README.md` shape — a prose test plan doc, NOT a runnable script. State the coverage/eval split honestly (spec §⑥).

**Files:**
- Create: `sci-skills-thesis/skills/thesis-spine/tests/README.md`

- [ ] **Step 1: Write the test plan README**

Cover (mirror sci-write's tests/README.md structure):

1. **Deterministic coverage gate** — `scripts/check_spine.py` + `scripts/test_check_spine.py` (run `python3 test_check_spine.py`). The cases it covers: passes on settled spine; fails on `[pending` marker; fails on empty/missing structural field; fails on missing per-paper instantiation; fails on role missing question/advance; **passes on empty umbrella + empty boundary (they're depth, NOT coverage — load-bearing)**. Note the exit-code contract (0 pass / 1 fail).
2. **The split (state honestly, spec §⑥)** — coverage is deterministic (grep-able: pending markers, field emptiness, per-paper lines, per-role keywords) → earns a runnable stdlib test, mirroring thesis-init's justified deviation (deterministic code + verifiable outputs). **Prose is NOT script-tested** — the workflow's judgment (candidate grounding, tension-as-question-not-verdict, depth-influence naming, gate-fires-on-empty behavior) is evaluated via skill-creator-plus's eval loop later, not here.
3. **Decoupling assertions (programmatic)** — grep: zero sibling-skill calls in thesis-spine source (no `from thesis-dissect` / `import thesis-...`); spine writes `thesis-spine.md` to `sci-skills/` (top-level, NOT a spine working-notes dir); spine reads neighbors' files (thesis-sources.md, template-spec.md) but never writes to them.
4. **TODO** — scaffold evals.json + run the full eval loop per skill-creator-plus before ship (the prose surface). Mirror sci-write's tests/README.md TODO line.

- [ ] **Step 2: Commit**

```bash
git add sci-skills-thesis/skills/thesis-spine/tests/README.md
git commit -m "thesis-spine: tests/README.md test plan (coverage=script+stdlib; prose=eval; split stated honestly)"
```

---

## Task 7: End-to-end verification + decoupling grep

> No new files — verification only. Confirms the deterministic surface works end-to-end and the decoupling invariants hold.

**Files:**
- No new files — verification only.

- [ ] **Step 1: Run the full test suite**

```bash
cd sci-skills-thesis/skills/thesis-spine/scripts && python3 test_check_spine.py
```
Expected: 8 `: PASS` lines then `ALL TESTS PASS`.

- [ ] **Step 2: Run check_spine.py as the skill would (CLI, on a fixture), confirm exit codes**

```bash
cd sci-skills-thesis/skills/thesis-spine/scripts
# pass case
tmp_pass=$(mktemp -d)
cat > "$tmp_pass/spine.md" <<'EOF'
## Main line (主线)
thread connecting N papers.
## Unified framework (统一框架)
the X framework
per-paper: how paper-A instantiates it = 侧视角1
## Inter-chapter progression (章间递进)
- role 1: question = X?; advances the main line by baseline
## Thesis-level claim (umbrella)
EOF
python3 check_spine.py "$tmp_pass/spine.md"; echo "exit=$?"
# fail case (pending marker)
cat > "$tmp_pass/spine_bad.md" <<'EOF'
## Main line (主线)
[pending? ] a thread.
## Unified framework (统一框架)
fw
## Inter-chapter progression (章间递进)
- role 1: question = X?; advances the main line by y
EOF
python3 check_spine.py "$tmp_pass/spine_bad.md"; echo "exit=$?"
rm -rf "$tmp_pass"
```
Expected: pass case prints `✓ coverage 通过` + `exit=0`; fail case prints the pending issue + `exit=1`. (Note: the pass case has an empty umbrella section — it still passes, because umbrella is depth, not coverage.)

- [ ] **Step 3: Decoupling grep — no sibling-skill calls**

```bash
echo "=== sibling-skill imports/calls in thesis-spine source (must be empty) ==="
grep -rnE "from thesis-(dissect|intro|theory|summary)|import thesis-(dissect|intro|theory|summary)|thesis-(dissect|intro|theory|summary)\(" sci-skills-thesis/skills/thesis-spine/ || echo "(none — decoupling holds)"
```
Expected: `(none — decoupling holds)`.

- [ ] **Step 4: Confirm SKILL.md + plugin shape invariants**

```bash
# no allowed-tools (spine is prose, mirrors sci-write)
grep -q "allowed-tools" sci-skills-thesis/skills/thesis-spine/SKILL.md && echo "FAIL: spine must not declare allowed-tools" || echo "ok: no allowed-tools (prose skill)"
# spine has no working-notes dir (spec §② — no churn to foundation)
ls -d sci-skills-thesis/skills/thesis-spine/scripts sci-skills-thesis/skills/thesis-spine/references sci-skills-thesis/skills/thesis-spine/tests
# plugin is a sibling, NOT inside sci-skills/
test -d sci-skills-thesis/.claude-plugin && echo "ok: sci-skills-thesis plugin exists as sibling"
```
Expected: `ok: no allowed-tools` / the three subdirs / `ok: sci-skills-thesis plugin exists as sibling`.

- [ ] **Step 5: Commit any final fixes (if Steps 1–4 revealed gaps)**

If verification revealed gaps, fix and commit:
```bash
git add -A && git commit -m "thesis-spine: end-to-end verification fixes"
```
If no gaps, this step is a no-op (nothing to commit) — note that in your task report.

---

## Acceptance (this plan, against the spec)

- [ ] `sci-skills-thesis/` is a valid Claude Code plugin (plugin.json parses; skills/thesis-spine/ present) — Task 1.
- [ ] `check_spine.py` gates COVERAGE only: no `[pending` + 3 structural fields non-empty + per-paper instantiation + per-role advance/question; **does NOT check umbrella or boundary** (they're depth) — verified by `test_ignores_umbrella_and_boundary` (load-bearing) — Tasks 2–3.
- [ ] 8 stdlib tests pass; CLI exit codes correct (0 pass / 1 fail) — Task 7.
- [ ] SKILL.md has the staged-gate workflow (Steps 0–5) + backtrack; tension-flagging = questions-not-verdicts + depth-influence stated failure mode; `pending` never auto-adopted; **no `allowed-tools` field** (prose skill, mirrors sci-write) — Task 4.
- [ ] references/ holds writing-discipline.md (tension protocol + failure mode) + spine-schema.md (template) — Task 5.
- [ ] tests/README.md states the coverage/eval split honestly — Task 6.
- [ ] spine has NO working-notes dir; plugin is a sibling (not inside sci-skills/); zero churn to the merged foundation — Task 7.
- [ ] No sibling-skill calls (decoupling grep clean) — Task 7.
- [ ] umbrella is a distinct depth-gated 4th field (NOT collapsed into main line, NOT under coverage) — Task 4 SKILL.md + Task 2 `test_ignores_umbrella_and_boundary`.

**Out of scope for this plan (named follow-ups):**
- The eval loop for the prose surface (candidate grounding, tension-as-question, gate-fires-on-empty) — run via skill-creator-plus's eval later; documented in tests/README.md, not implemented here.
- The 6 remaining writing-chain skills (dissect/intro/theory/summary/typeset/polish) — each its own plan.
- Real university template packs — foundation's `generic-test` proved the mechanism; a real school pack is a separate data task.

---

## Execution context (for the implementer + reviewers)

- **Branch**: `thesis-spine` (opened in Pre-flight; do NOT work on master — foundation is merged there).
- **Review flow during execution** (subagent-driven-development): capricorn implements each task (TDD for the script, prose for SKILL.md/references); after each task or at end, **scorpio** (spec compliance — does the code match the spec?) + **taurus** (quality — readability, naming, duplication) + **aries** (adversarial — **MUST run**: SKILL.md instructs Bash execution of `check_spine.py` + the script itself is execution code, surface 5; aries line-by-lines the script for shell/python footguns + prompt-injection on SKILL.md).
- **Spec is the authority**: when SKILL.md/references wording is ambiguous, read `docs/superpowers/specs/thesis-spine.md` §the-relevant-section — cite spec §numbers in the prose so the reader can find rationale.
