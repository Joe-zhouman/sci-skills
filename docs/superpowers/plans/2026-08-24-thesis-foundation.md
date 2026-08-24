# thesis-skill-family Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the foundation of the `sci-skills-thesis` plugin family — the plugin scaffold, the `thesis-init` entry skill (its `init_project.py` + contracts + template-pack mechanism), and a minimal test template pack — so the workspace skeleton, source registry, and template weaving work end-to-end. This is Plan 1 of N; the 7 prose skills (spine/dissect/intro/theory/summary/typeset/polish) are subsequent plans built on these contracts.

**Architecture:** Mirror the article family's compass-file coupling. thesis-init lives in the SHARED `sci-skills` plugin (alongside `article-init`); the `sci-skills-thesis` plugin (sibling to `sci-skills-article`, future) holds the writing chain (created when `thesis-spine` lands). Both share the on-disk workspace name `sci-skills/`. `thesis-init` is the only entry node that knows all sibling skills; it scaffolds `thesis/` (the first-class artifact, organized by chapter) + `sci-skills/` shared files (thesis-prefixed to avoid colliding with article family) + per-skill `CONTRACT.md` contracts, and weaves a selected university template pack into `thesis/tex/`. init_project.py is pure stdlib, deterministic (mechanical writing); the interactive source-registry collection is the agent's job (documented in SKILL.md), writing simple markdown per a schema — not a script. Template packs ship at **repo-root** `templates/thesis/` (matching article's `templates/main/` convention; the repo is cloned wholesale, so repo-root templates ship with it) — thesis-init weaves from there via `parents[4]` (`REPO_TEMPLATES_DIR`). thesis makes the pack a runtime path dependency (init reads it to weave); the repo-root convention (same as article) ships it.

**Tests:** A stdlib `assert` script (`test_init.py`), no pytest. **This is a deliberate, justified deviation from the article family** — not "matching repo convention." The article family's article-init has no test script (its `tests/README.md` is a prose plan that admits "TODO: run the full Test loop" — i.e. its deterministic init_project.py is currently untested). For thesis-init's init_project.py — deterministic code with objectively-verifiable file outputs (files exist/don't, content matches, idempotency holds) — a runnable test script earns its place: that is exactly the case skill-creator-plus/testing.md describes ("skills with objectively verifiable outputs"). The article family inherits an untested gap; thesis-init fixes it rather than carrying it forward. (Prose skills later use the eval loop, not a script — that's the right tool for subjective outputs.)

**Tech Stack:** Python 3.11+ stdlib (pathlib, argparse, json, subprocess, shutil); LaTeX (native `report` class for the test pack); Claude Code plugin manifest format.

**Spec:** `docs/superpowers/specs/thesis-skill-family.md`
**Glossary terms already on disk** (verify, don't recreate): Thesis, Compass file, 拆即写, Architecture-level claim, Citation-vs-architecture enforcement split, Serves-the-author-first — in `docs/superpowers/glossary.md`.

---

## File Structure

This plan creates/touches:

- `sci-skills/.claude-plugin/plugin.json` — SHARED plugin manifest (updated: add thesis-init to description + keywords; article-init + sci-draw already present)
- `sci-skills/skills/thesis-init/SKILL.md` — init skill definition (prose workflow)
- `sci-skills/skills/thesis-init/scripts/init_project.py` — the deterministic engine (real code)
- `sci-skills/skills/thesis-init/scripts/test_init.py` — stdlib test script
- `sci-skills/skills/thesis-init/references/family-layout.md` — family layout depth reference (prose)
- `sci-skills/skills/thesis-init/tests/README.md` — test plan doc
- `templates/thesis/generic-test/template-spec.md` — minimal test template pack spec (repo-root, matching article's templates/main/)
- `templates/thesis/generic-test/main.tex` — minimal test template blueprint (native `report` class)
- `docs/superpowers/glossary.md` — verify thesis terms present (already written this session)

**Decision-ladder outcomes baked in:**
- plugin.json → Rung 4 (shared `sci-skills` plugin manifest updated — add thesis-init; no separate `sci-skills-thesis` plugin created in this foundation)
- init_project.py → Rung 7 (must write; mirrors article-init's proven init_project.py). Stdlib only (Rung 3).
- test pack .cls → Rung 4 (native `report` document class; proves the flat-file weave + that a woven pack compiles; real multi-file .cls packs are a named follow-up, not proven here)
- No source-registry script → Rung 1 (agent writes simple markdown directly; a script is scaffolding-for-later)
- Tests → stdlib `assert` script (Rung 3), no pytest (justified deviation above — deterministic code with verifiable outputs earns a runnable test; article family's untested init is a gap, not a convention)

---

## Task 1: Plugin scaffold

> **CORRECTION (user review post-implementation):** thesis-init is SHARED infrastructure
> (scaffolds the same `sci-skills/` workspace for both families), so it lives in the SHARED
> `sci-skills` plugin at `sci-skills/skills/thesis-init/` (alongside `article-init`), NOT in
> `sci-skills-thesis/skills/`. The `sci-skills-thesis` plugin is NOT created in this foundation
> — it has no skills yet (writing chain is future); it is created when `thesis-spine` (the
> first writing skill) lands in the next plan. The steps below show the original pre-correction
> `sci-skills-thesis/` paths; the implemented result uses the shared-plugin paths (see File
> Structure above). Template packs moved to repo-root `templates/thesis/` (matching article's
> `templates/main/`); `init_project.py` resolves them via `REPO_TEMPLATES_DIR = parents[4]`.

**Files:**
- Create: `sci-skills-thesis/.claude-plugin/plugin.json`
- Create: `sci-skills-thesis/skills/thesis-init/.gitkeep` (so the dir tracks until SKILL.md lands in Task 3)

- [ ] **Step 1: Create the plugin manifest**

Write `sci-skills-thesis/.claude-plugin/plugin.json` (mirror `sci-skills-article/.claude-plugin/plugin.json`):

```json
{
  "name": "sci-skills-thesis",
  "description": "sci-skills thesis family — turn N published papers into a degree thesis (重组延伸, not from-scratch). thesis-init + the writing chain: spine, dissect, intro, theory, summary, typeset, polish. Claude Code only.",
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

- [ ] **Step 2: Create the skills dir placeholder**

```bash
mkdir -p sci-skills-thesis/skills/thesis-init/scripts
mkdir -p sci-skills-thesis/skills/thesis-init/references
mkdir -p sci-skills-thesis/skills/thesis-init/tests
touch sci-skills-thesis/skills/thesis-init/.gitkeep
```

- [ ] **Step 3: Verify manifest is valid JSON**

Run: `python3 -c "import json; json.load(open('sci-skills-thesis/.claude-plugin/plugin.json'))"`
Expected: no output, exit 0.

- [ ] **Step 4: Commit**

```bash
git add sci-skills-thesis/
git commit -m "thesis: scaffold sci-skills-thesis plugin + thesis-init skill dirs"
```

---

## Task 2: Verify glossary thesis terms present

**Files:**
- Read-only: `docs/superpowers/glossary.md`

- [ ] **Step 1: Confirm the six thesis terms exist**

Run:
```bash
grep -cE '\*\*(Thesis \(|Compass file|拆即写|Architecture-level claim|Citation-level vs architecture-level|Serves-the-author-first)' docs/superpowers/glossary.md
```
Expected: `6` (all six term headings present, written this session during brainstorming).

If any missing: stop — the brainstorming glossary writes were lost; re-add from the spec's glossary references before proceeding.

- [ ] **Step 2: No commit (read-only verification)**

---

## Task 3: thesis-init SKILL.md (the workflow + agent's role)

**Files:**
- Create: `sci-skills-thesis/skills/thesis-init/SKILL.md`

- [ ] **Step 1: Write the SKILL.md**

Write `sci-skills-thesis/skills/thesis-init/SKILL.md` with this frontmatter and body. This defines what init does and the **division of labor** (deterministic = script; judgment/interactive = agent). Key content it must state:

```markdown
---
name: thesis-init
description: >-
  学位论文项目初始化 / thesis project init — scaffold thesis/ (一等产物, by chapter) + sci-skills/
  shared workspace (thesis-prefixed files, coexists with article family) + per-skill CONTRACT.md,
  and weave a selected university template pack into thesis/tex/. Manual only, runs once and exits.
  thesis-init 是唯一知道所有兄弟 skill 的 entry 节点（路由表）；其他 skill 只认文件。
  不画图不写正文 / does not draw figures or write prose. Triggers: 初始化学位论文, init thesis,
  thesis init, 学位论文开个新项目.
allowed-tools: Read, Write, Bash
---
```

Body must cover (mirror article-init's SKILL.md structure):

1. **One-line positioning**: thesis-init scaffolds the workspace; it does not write prose or draw figures. It runs once and exits — the human advances the pipeline by invoking each writing skill.

2. **Division of labor (the core philosophy)**:
   - **确定性归脚本** (`init_project.py`): build skeleton, write CONTRACT.md files, weave template pack, create shared-file placeholders. Idempotent, no judgment.
   - **判断性归 agent** (this skill's prose): interactively collect the source registry (which small papers, where their data lives — scattered across folders), decide which template pack to use, confirm the project root. The agent writes the registry as simple markdown per the schema (no script for it — the registry is plain markdown the agent fills).

3. **Two subcommands**: `init` (build skeleton + weave template) and `checkup` (audit layout). Reference `init_project.py --help` for exact args.

4. **The source registry (`thesis-sources.md`)** — the agent's interactive job:
   - For each small paper that will become a thesis chapter, ask the user: paper_id, path(s) (may be multiple folders), data path(s) (may be scattered), slug (for chapter naming per template), claim (optional, filled by dissect later).
   - Write entries to `sci-skills/thesis-sources.md` per its CONTRACT.md schema. This file is the single navigation truth — every thesis skill reads it to locate scattered sources. Never hardcode source dirs in any skill.
   - The registry may be extended later (add a paper, fix a path) by editing the file directly.

5. **Template selection**: init takes `--template <pack-name>`. If `templates/thesis/` has one pack, default to it; if many, the agent asks the user and passes `--template`. If the user's school isn't packaged yet, `--template-dir <path>` points at a user-supplied .cls + spec (degraded mode, generates a temporary template-spec.md).

6. **Layout it builds** — the full tree (paste the spec's layout block, with the thesis- prefixed shared files).

7. **After init**: point the user at `thesis-spine` (the next skill — establish main line + unified framework). Do NOT auto-run it (read neighbors, don't orchestrate).

8. **Reference index**: `references/family-layout.md` (when modifying layout/contracts/adding a sibling skill).

Write the full body following article-init/SKILL.md's tone and structure. Use the spec (`docs/superpowers/specs/thesis-skill-family.md`) §Implementation Notes for the exact layout and shared-file list.

- [ ] **Step 2: Verify it parses as a skill (frontmatter + body)**

Run:
```bash
python3 -c "
import re
t = open('sci-skills-thesis/skills/thesis-init/SKILL.md').read()
assert t.startswith('---'), 'missing frontmatter'
assert 'name: thesis-init' in t.split('---')[1], 'missing name'
assert '## ' in t, 'missing body headings'
print('ok')
"
```
Expected: `ok`

- [ ] **Step 3: Commit**

```bash
git add sci-skills-thesis/skills/thesis-init/SKILL.md
git commit -m "thesis-init: SKILL.md — workflow, agent/script labor division, registry role"
```

---

## Task 4: init_project.py — constants + contracts

**Files:**
- Create: `sci-skills-thesis/skills/thesis-init/scripts/init_project.py`
- Create: `sci-skills-thesis/skills/thesis-init/scripts/test_init.py` (the test script, built up across tasks)

- [ ] **Step 1: Write the failing test for constants**

Create `sci-skills-thesis/skills/thesis-init/scripts/test_init.py`:

```python
"""stdlib tests for init_project.py — run: python3 test_init.py"""
import importlib.util, pathlib, sys
HERE = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("init_project", HERE / "init_project.py")
init_project = importlib.util.module_from_spec(spec)
spec.loader.exec_module(init_project)

def test_constants():
    # workspace name shared with article family (coexist in same sci-skills/)
    assert init_project.FAMILY_ROOT_NAME == "sci-skills"
    assert init_project.THESIS_DIR_NAME == "thesis"
    # only the skills that get their own output dir are pre-built
    assert init_project.BROTHER_SKILLS == [
        "thesis-dissect", "thesis-intro", "thesis-theory", "thesis-summary",
    ]
    # spine/polish/typeset/init have NO dir (they write top-level shared files
    # or edit tex in place); verify none of them leaked in
    assert "thesis-spine" not in init_project.BROTHER_SKILLS
    assert "thesis-polish" not in init_project.BROTHER_SKILLS
    # top-level shared files (thesis- prefixed to avoid article-family collision)
    assert "thesis-sources.md" in init_project.SHARED_FILES_PLACEHOLDERS
    assert "thesis-spine.md" in init_project.SHARED_FILES_PLACEHOLDERS
    assert "thesis-terminology-ledger.md" in init_project.SHARED_FILES_PLACEHOLDERS

if __name__ == "__main__":
    test_constants()
    print("test_constants: PASS")
```

- [ ] **Step 2: Run test — verify it fails (module/file not found)**

```bash
cd sci-skills-thesis/skills/thesis-init/scripts && python3 test_init.py
```
Expected: `ModuleNotFoundError` / `FileNotFoundError` (init_project.py doesn't exist yet).

- [ ] **Step 3: Write init_project.py constants + contract text**

Create `sci-skills-thesis/skills/thesis-init/scripts/init_project.py`. Start with module docstring (mirror article-init's: manual-entry thick-orchestration, runs once and exits; deterministic = script, judgment = agent; idempotent; stdlib only) and these constants:

```python
from __future__ import annotations
import argparse, json, os, subprocess, sys
from pathlib import Path

# 家族顶层目录名 — 与 article 家族共享（同一工作区 sci-skills/，二者共存）
FAMILY_ROOT_NAME = "sci-skills"

# 学位论文一等产物目录（在项目根，按章组织，非审稿轮次）
THESIS_DIR_NAME = "thesis"

# 预建的兄弟 skill 子目录（需要自己输出目录的才预建）。
# thesis-spine / thesis-polish / thesis-typeset 不预建：
#   spine 产顶层共享文件 thesis-spine.md + thesis-terminology-ledger.md（无自己的目录）；
#   polish/typeset 直接在 thesis/tex/ 上原地改 tex，git 留痕（无自己的目录）。
# thesis-init 自己也不预建（entry，scaffold 完即退）。
BROTHER_SKILLS = ["thesis-dissect", "thesis-intro", "thesis-theory", "thesis-summary"]

# 顶层共享文件（放在 sci-skills/ 根，thesis- 前缀避免与 article 家族碰撞）。
# thesis-sources.md 是来源 registry（agent 交互填充，全家族导航真相）。
# thesis-spine.md / thesis-terminology-ledger.md 是占位骨架（spine skill 后续填充）。
SHARED_FILES_PLACEHOLDERS = {
    "thesis-sources.md": "<!-- 来源 registry — thesis-init 交互填充。每篇小论文一条：\n"
        "## paper-A\n- slug: chapter-a\n- paths: [../paper-A/, ../shared-data/]\n"
        "- data_paths: [../paper-A/data/]\n- claim: (dissect 回填)\n-->\n",
    "thesis-spine.md": "<!-- 主线+统一框架+章间递进+thesis级claim — thesis-spine skill 产。占位。 -->\n",
    "thesis-terminology-ledger.md": "<!-- 跨章术语表 — thesis-spine 建，各章/polish 共写。占位。 -->\n",
}

# sci-skills/thesis-README.md 内容（thesis 家族自述 + routing table — thesis- 前缀避免与
# article 家族的 sci-skills/README.md 在共存项目里碰撞）
def _readme_text() -> str:
    lines = [f"# {FAMILY_ROOT_NAME}/\n",
             "The sci-skills family on-disk workspace. Article + thesis families coexist here.\n",
             "## Thesis-family shared files (top-level, thesis- prefixed)\n",
             "- `thesis-sources.md` — source registry (thesis-init fills; all thesis skills read)\n",
             "- `thesis-spine.md` — main line + unified framework (thesis-spine produces)\n",
             "- `thesis-terminology-ledger.md` — cross-chapter terminology\n",
             "## Sibling skill dirs\n"]
    for s in BROTHER_SKILLS:
        lines.append(f"- `{s}/`\n")
    lines.append("\n## Convention\n- Skills read neighbors' on-disk outputs; never import each other.\n"
                 "- thesis-init is the only node that knows all siblings; every other skill knows only files.\n")
    return "".join(lines)
```

Then add the contract text constants. Define `THESIS_CONTRACT` (the `thesis/CONTRACT.md` content — state: this is the thesis first-class artifact, organized by chapter not review-round; template woven at init; file naming follows the chosen template's `template-spec.md` — this contract does NOT prescribe filenames; who writes what; working notes never land here). And `SKILL_DIR_CONTRACTS: dict[str,str]` — one entry per brother skill (each a `CONTRACT.md` stating what that dir holds: working notes only, tex goes to `../../thesis/tex/`, who reads it). Model these on article-init's `SKILL_DIR_CONTRACTS` and `MANUSCRIPT_CONTRACT` exactly in shape (three sections: what is this folder / what's it for / how files land here + who reads it).

For the brother-skill contracts, use placeholder content that names the skill's role per the spec §Implementation Notes:
- `thesis-dissect`: working notes per small paper (paper-X/ subdirs: chapter mapping, module restructure, question→claim records). Tex → `../../thesis/tex/`. Produces `chapter-map.md`.
- `thesis-intro`: intro-chapter working notes. Tex → `../../thesis/tex/`.
- `thesis-theory`: ch2 shared-theory working notes. Tex → `../../thesis/tex/`.
- `thesis-summary`: synthesis-chapter working notes. Tex → `../../thesis/tex/`.

- [ ] **Step 4: Run test — verify constants pass**

```bash
cd sci-skills-thesis/skills/thesis-init/scripts && python3 test_init.py
```
Expected: `test_constants: PASS`

- [ ] **Step 5: Commit**

```bash
git add sci-skills-thesis/skills/thesis-init/scripts/
git commit -m "thesis-init: init_project.py constants + CONTRACT.md text (mirror article-init)"
```

---

## Task 5: init_project.py — cmd_init skeleton (scaffold + shared files + skill dirs)

**Files:**
- Modify: `sci-skills-thesis/skills/thesis-init/scripts/init_project.py`
- Modify: `sci-skills-thesis/skills/thesis-init/scripts/test_init.py`

- [ ] **Step 1: Write failing tests for cmd_init**

Append to `test_init.py` (before the `if __name__` block):

```python
import tempfile, shutil

def test_init_builds_skeleton():
    cwd = pathlib.Path(tempfile.mkdtemp())
    orig = pathlib.Path.cwd()
    os.chdir(cwd)
    try:
        rc = init_project.main(["init", "--no-git"])
        assert rc == 0
        # thesis/ first-class artifact — CONTRACT.md MUST be written (the bug aquarius caught)
        assert (cwd / "thesis" / "CONTRACT.md").is_file(), "thesis/CONTRACT.md not written"
        assert (cwd / "thesis" / "tex").is_dir()
        assert (cwd / "thesis" / ".gitignore").is_file(), "thesis/.gitignore not written"
        # shared workspace + thesis- prefixed shared files
        fam = cwd / "sci-skills"
        assert fam.is_dir()
        assert (fam / "thesis-sources.md").is_file()
        assert (fam / "thesis-spine.md").is_file()
        assert (fam / "thesis-terminology-ledger.md").is_file()
        # thesis-README.md (thesis-owned routing table; NOT README.md, which the article
        # family may own in a coexist project — the collision aquarius flagged)
        assert (fam / "thesis-README.md").is_file(), "thesis-README.md not written"
        # init must NOT write a root .gitignore (collides with article family / human's)
        assert not (cwd / ".gitignore").is_file(), "init must not write root .gitignore"
        # brother skill dirs each with a CONTRACT.md
        for s in init_project.BROTHER_SKILLS:
            assert (fam / s / "CONTRACT.md").is_file(), f"missing {s}/CONTRACT.md"
        # spine/polish/typeset do NOT get dirs
        assert not (fam / "thesis-spine").is_dir()
        assert not (fam / "thesis-polish").is_dir()
    finally:
        os.chdir(orig)
        shutil.rmtree(cwd, ignore_errors=True)
    print("test_init_builds_skeleton: PASS")
```

Add `import os` at top of test file if not present. Update the `__main__` block to call both `test_constants()` and `test_init_builds_skeleton()`.

- [ ] **Step 2: Run — verify it fails**

```bash
cd sci-skills-thesis/skills/thesis-init/scripts && python3 test_init.py
```
Expected: failure — `cmd_init` / `main` not defined yet.

- [ ] **Step 3: Implement cmd_init (scaffold, no template weave yet)**

Add to `init_project.py` (mirror article-init's `cmd_init` structure: build thesis/ first, then family root, then shared files, then brother dirs, then .gitignore, then git init unless `--no-git`):

```python
def find_project_root(start: Path | None = None) -> Path:
    return Path(start) if start else Path.cwd()

def family_root(project_root: Path) -> Path:
    return project_root / FAMILY_ROOT_NAME

def cmd_init(args: argparse.Namespace) -> int:
    root = find_project_root()
    report: list[str] = [f"init @ {root}"]

    # 0. thesis/ — first-class artifact. Build thesis/ + CONTRACT.md + tex/ (empty for now).
    #    CONTRACT.md written in BOTH branches (idempotent: skip if exists, write if new).
    th = root / THESIS_DIR_NAME
    th_contract = th / "CONTRACT.md"
    if th.exists():
        if not th_contract.exists():
            th_contract.write_text(THESIS_CONTRACT, encoding="utf-8")
            report.append(f"✓ {THESIS_DIR_NAME}/ 已存在，补 CONTRACT.md")
        else:
            report.append(f"✓ {THESIS_DIR_NAME}/ 已存在（跳过）")
    else:
        th.mkdir(parents=True)
        (th / "tex").mkdir()
        th_contract.write_text(THESIS_CONTRACT, encoding="utf-8")  # <-- the write article-init's mirror has
        report.append(f"✓ 创建 {THESIS_DIR_NAME}/ + tex/ + CONTRACT.md")

    # 1. family root (shared with article family — create if absent, never clobber existing article files)
    fam = family_root(root)
    if not fam.exists():
        fam.mkdir(parents=True)
        report.append(f"✓ 创建 {FAMILY_ROOT_NAME}/")

    # 2. top-level shared files (thesis- prefixed). Skip if exists; never overwrite.
    for name, content in SHARED_FILES_PLACEHOLDERS.items():
        p = fam / name
        if p.exists():
            report.append(f"  - {name} 已存在（跳过）")
        else:
            p.write_text(content, encoding="utf-8")
            report.append(f"  - 创建 {name}")

    # 3. thesis-README.md (thesis-owned routing table — NOT README.md, which the article
    #    family may own in a coexist project; thesis- prefix avoids the collision).
    readme = fam / "thesis-README.md"
    if not readme.exists():
        readme.write_text(_readme_text(), encoding="utf-8")
        report.append("  - 创建 thesis-README.md")

    # 4. brother skill dirs + CONTRACT.md
    for skill in BROTHER_SKILLS:
        sd = fam / skill
        c = sd / "CONTRACT.md"
        if sd.exists():
            if not c.exists() and skill in SKILL_DIR_CONTRACTS:
                c.write_text(SKILL_DIR_CONTRACTS[skill], encoding="utf-8")
                report.append(f"  - {skill}/ 已存在，补 CONTRACT.md")
            else:
                report.append(f"  - {skill}/ 已存在（跳过）")
        else:
            sd.mkdir()
            c.write_text(SKILL_DIR_CONTRACTS.get(skill, f"# {skill}/\n\nReserved.\n"), encoding="utf-8")
            report.append(f"  - 创建 {skill}/ + CONTRACT.md")

    # 5. thesis/.gitignore (thesis-scoped — LaTeX build products). Written INSIDE thesis/,
    #    not at project root, so it never collides with an article-family .gitignore.
    #    Root .gitignore is the human's/article's concern; init does not touch it.
    gi = th / ".gitignore"
    if not gi.exists():
        gi.write_text("\n".join([
            "# LaTeX build products", "*.aux", "*.log", "*.out", "*.toc", "*.bbl", "*.blg",
            "*.fls", "*.fdb_latexmk", "*.synctex.gz", "",
        ]) + "\n", encoding="utf-8")
        report.append("  - 创建 thesis/.gitignore")

    # 6. git init (unless --no-git) — mirror article-init
    if (root / ".git").is_dir():
        report.append("✓ .git/ 已存在（跳过）")
    elif args.no_git:
        report.append("· 跳过 git init（--no-git）")
    else:
        try:
            subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True, text=True)
            report.append("✓ git init")
        except (FileNotFoundError, subprocess.CalledProcessError):
            report.append("⚠ git init 跳过")

    print("\n".join(report))
    return 0
```

Also add `main()` and the argparse setup (mirror article-init — `init` and `checkup` subcommands; `init` takes `--no-git`, `--template`, `--template-dir`):

```python
def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="sci-skills-thesis 家族项目初始化 / 体检。手动触发，跑一次就退。")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_init = sub.add_parser("init", help="建 thesis/ + sci-skills/ 骨架 + 织入模板")
    p_init.add_argument("--no-git", action="store_true")
    p_init.add_argument("--template", default=None, help="模板包名 (templates/thesis/<name>)")
    p_init.add_argument("--template-dir", default=None, help="用户自带 .cls+spec 目录（degraded）")
    p_init.set_defaults(func=cmd_init)
    p_chk = sub.add_parser("checkup", help="体检落盘位置")
    p_chk.set_defaults(func=cmd_checkup)
    args = parser.parse_args(argv[1:])
    return args.func(args)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
```

- [ ] **Step 4: Run — verify skeleton test passes**

```bash
cd sci-skills-thesis/skills/thesis-init/scripts && python3 test_init.py
```
Expected: `test_constants: PASS` then `test_init_builds_skeleton: PASS`.

- [ ] **Step 5: Commit**

```bash
git add sci-skills-thesis/skills/thesis-init/scripts/
git commit -m "thesis-init: cmd_init scaffolds thesis/ + sci-skills/ shared files + brother dirs"
```

---

## Task 6: init_project.py — template-pack weave

**Files:**
- Modify: `sci-skills-thesis/skills/thesis-init/scripts/init_project.py`
- Modify: `sci-skills-thesis/skills/thesis-init/scripts/test_init.py`
- Create: `templates/thesis/generic-test/template-spec.md` (repo-root, matching article's templates/main/)
- Create: `templates/thesis/generic-test/main.tex`

- [ ] **Step 1: Create the minimal test template pack (repo-root)**

Create `templates/thesis/generic-test/template-spec.md`:

```markdown
# template-spec — generic-test (minimal test pack)

> 这份文件是契约（contract）。thesis-init 读它把模板织进 thesis/tex/；各 thesis skill
> 读它对齐文件命名。真实大学模板包（清华 thuthesis 等）按同一 schema 后续收集。

## 这个模板是什么
最小可编译的学位论文模板，用于验证 init 的模板织入机制。用原生 `report` 文档类，
不依赖任何大学 .cls。真实投稿应换成本校模板包（templates/thesis/<school>/）。

## 文件命名约定（各 skill 读这条对齐）
- 章文件：`chapterN.tex`（N 从 0 起：chapter0=绪论，chapter1=理论方法，chapter2+=正文，末章=总结）
- 参考文献：`refs.bib`
- 主文件：`main.tex`（含 preamble + `\input{chapterN}` 织入各章）

## 编译
xelatex main.tex → bibtex main → xelatex main.tex ×2

## 前置/后置页（typeset skill 读这条组织）
- 前置：封面、原创性声明、中英文摘要、目录（本最小包省略，真实包按校规）
- 后置：致谢、攻读成果、作者简介（占位，作者手填）
```

Create `templates/thesis/generic-test/main.tex` (native `report` class — Rung 4, no custom .cls):

```latex
\documentclass[12pt,a4paper]{report}
\usepackage[utf8]{inputenc}
\usepackage{geometry}
\geometry{margin=2.5cm}
\usepackage{hyperref}
\usepackage{graphicx}
\bibliographystyle{plain}

\title{<thesis title — fill in>}
\author{<author — fill in>}

\begin{document}
\maketitle
% 前置页（真实包按校规；此最小包仅占位）
\input{chapter0}   % 绪论
\input{chapter1}   % 共用理论方法
% \input{chapter2} ... 各正文章（dissect 产）
\input{chapter_last}  % 总结展望
\bibliography{refs}
\end{document}
```

- [ ] **Step 2: Write failing test for template weave**

Append to `test_init.py`:

```python
def test_init_weaves_template():
    import tempfile, shutil
    cwd = pathlib.Path(tempfile.mkdtemp())
    orig = pathlib.Path.cwd()
    # locate the generic-test pack at repo root: test_init.py is at
    # sci-skills/skills/thesis-init/scripts/ → parents[4] = repo root (where templates/ lives)
    # templates/thesis/ ships at repo root, matching article's templates/main/ convention.
    repo_root = pathlib.Path(__file__).resolve().parents[4]
    pack = plugin_root / "templates" / "thesis" / "generic-test"
    assert pack.is_dir(), f"test pack missing at {pack}"
    os.chdir(cwd)
    try:
        rc = init_project.main(["init", "--no-git", "--template", "generic-test"])
        assert rc == 0
        tex = cwd / "thesis" / "tex"
        assert (tex / "main.tex").is_file(), "main.tex not woven"
        assert (tex / "template-spec.md").is_file(), "template-spec.md not copied"
        # the chosen template-spec's naming convention is copied into thesis/
        spec = (cwd / "thesis" / "template-spec.md").read_text()
        assert "chapterN.tex" in spec, "naming convention not in woven spec"
    finally:
        os.chdir(orig)
        shutil.rmtree(cwd, ignore_errors=True)
    print("test_init_weaves_template: PASS")
```

(`parents[4]`: `scripts` → `thesis-init` → `skills` → `sci-skills` (plugin) → repo root. Verify: `python3 -c "from pathlib import Path; print(Path('sci-skills/skills/thesis-init/scripts/test_init.py').resolve().parents[4])"` — must resolve to the dir containing `templates/thesis/`.)

Add `test_init_weaves_template()` to the `__main__` calls.

- [ ] **Step 3: Run — verify it fails**

```bash
cd sci-skills-thesis/skills/thesis-init/scripts && python3 test_init.py
```
Expected: `test_init_weaves_template` fails (no template weave logic / pack not found).

- [ ] **Step 4: Implement template weave in cmd_init**

Add helpers + call in `cmd_init` (after creating `thesis/tex/`, weave into it). Template packs resolve relative to the repo root (`templates/thesis/`), shipped with the repo (matching article's `templates/main/`):

```python
# templates/ live at repo root (templates/thesis/), matching article's templates/main/
# convention — the repo is cloned wholesale, so repo-root templates ship with it. Resolved
# from this script: scripts → thesis-init → skills → sci-skills (plugin) → repo root (parents[4]).
REPO_TEMPLATES_DIR = Path(__file__).resolve().parents[4] / "templates" / "thesis"

def _resolve_template_pack(args) -> Path | None:
    """Find the template pack dir to weave. Returns None if user opted out."""
    if args.template_dir:
        d = Path(args.template_dir)
        if not d.is_dir():
            print(f"⚠ --template-dir 不存在: {d}")
            return None
        return d
    if args.template:
        d = REPO_TEMPLATES_DIR / args.template
        if not d.is_dir():
            print(f"⚠ 模板包不存在: {d}（可用: {', '.join(_available_packs())}）")
            return None
        return d
    packs = _available_packs()
    if len(packs) == 1:
        return REPO_TEMPLATES_DIR / packs[0]
    if not packs:
        print("⚠ 无模板包（templates/thesis/ 为空）。thesis/tex/ 留空，待手动织入。")
        return None
    print(f"⚠ 多个模板包: {', '.join(packs)}。用 --template <name> 指定；本次跳过织入。")
    return None

def _available_packs() -> list[str]:
    if not REPO_TEMPLATES_DIR.is_dir():
        return []
    return sorted(p.name for p in REPO_TEMPLATES_DIR.iterdir() if p.is_dir())

def _weave_template(thesis_tex: Path, pack: Path) -> list[str]:
    """Copy pack contents into thesis/tex/, recursing into subdirs (real packs like
    thuthesis have config/figures subdirs). Idempotent: skip existing files/dirs."""
    report = []
    for src in pack.iterdir():
        if src.name.startswith("."):
            continue
        dst = thesis_tex / src.name
        if src.is_dir():
            if dst.exists():
                report.append(f"  - tex/{src.name}/ 已存在（跳过）")
            else:
                shutil.copytree(src, dst)
                report.append(f"  - 织入 tex/{src.name}/")
        else:
            if dst.exists():
                report.append(f"  - tex/{src.name} 已存在（跳过）")
            else:
                shutil.copyfile(src, dst)
                report.append(f"  - 织入 tex/{src.name}")
    return report
```

In `cmd_init`, after creating `thesis/tex/`, add:
```python
    pack = _resolve_template_pack(args)
    if pack:
        report.extend(_weave_template(th / "tex", pack))
    # copy template-spec.md to thesis/ (top of thesis/, the skill-facing contract)
    spec_src = pack / "template-spec.md" if pack else None
    spec_dst = th / "template-spec.md"
    if spec_src and spec_src.is_file() and not spec_dst.exists():
        shutil.copyfile(spec_src, spec_dst)
        report.append("  - 织入 thesis/template-spec.md")
```

Add `import shutil` to the imports at top of init_project.py.

- [ ] **Step 5: Run — verify weave test passes**

```bash
cd sci-skills-thesis/skills/thesis-init/scripts && python3 test_init.py
```
Expected: all three tests PASS.

- [ ] **Step 6: Commit**

```bash
git add sci-skills-thesis/skills/thesis-init/scripts/init_project.py sci-skills-thesis/skills/thesis-init/scripts/test_init.py sci-skills-thesis/templates/thesis/generic-test/
git commit -m "thesis-init: template-pack weave mechanism + minimal generic-test pack"
```

---

## Task 7: init_project.py — idempotency test

**Files:**
- Modify: `sci-skills-thesis/skills/thesis-init/scripts/test_init.py`

- [ ] **Step 1: Write failing idempotency test**

Append to `test_init.py`:

```python
def test_init_idempotent():
    import tempfile, shutil
    cwd = pathlib.Path(tempfile.mkdtemp())
    orig = pathlib.Path.cwd()
    repo_root = pathlib.Path(__file__).resolve().parents[4]  # repo root (same index as test_init_weaves_template)
    os.chdir(cwd)
    try:
        init_project.main(["init", "--no-git", "--template", "generic-test"])
        # snapshot: capture content of a woven file + a contract
        main_tex = (cwd / "thesis" / "tex" / "main.tex").read_text()
        contract = (cwd / "thesis" / "CONTRACT.md").read_text()
        # second run — must not error, must not overwrite existing files
        rc = init_project.main(["init", "--no-git", "--template", "generic-test"])
        assert rc == 0
        # idempotent: existing files unchanged
        assert (cwd / "thesis" / "tex" / "main.tex").read_text() == main_tex
        assert (cwd / "thesis" / "CONTRACT.md").read_text() == contract
    finally:
        os.chdir(orig)
        shutil.rmtree(cwd, ignore_errors=True)
    print("test_init_idempotent: PASS")
```

Add `test_init_idempotent()` to `__main__`.

- [ ] **Step 2: Run — verify it passes (idempotency is already baked into cmd_init's skip-if-exists logic)**

```bash
cd sci-skills-thesis/skills/thesis-init/scripts && python3 test_init.py
```
Expected: all four tests PASS. (If it fails: the skip-if-exists logic has a gap — fix `cmd_init`/`_weave_template` to never overwrite existing files, then re-run.)

- [ ] **Step 3: Commit**

```bash
git add sci-skills-thesis/skills/thesis-init/scripts/test_init.py
git commit -m "thesis-init: idempotency test (re-run does not overwrite)"
```

---

## Task 8: init_project.py — cmd_checkup

**Files:**
- Modify: `sci-skills-thesis/skills/thesis-init/scripts/init_project.py`
- Modify: `sci-skills-thesis/skills/thesis-init/scripts/test_init.py`

- [ ] **Step 1: Write failing checkup tests**

Append to `test_init.py`:

```python
def test_checkup_healthy():
    import tempfile, shutil
    cwd = pathlib.Path(tempfile.mkdtemp())
    orig = pathlib.Path.cwd()
    os.chdir(cwd)
    try:
        init_project.main(["init", "--no-git", "--template", "generic-test"])
        rc = init_project.main(["checkup"])
        assert rc == 0, "healthy layout should exit 0"
    finally:
        os.chdir(orig); shutil.rmtree(cwd, ignore_errors=True)
    print("test_checkup_healthy: PASS")

def test_checkup_missing_workspace():
    import tempfile, shutil
    cwd = pathlib.Path(tempfile.mkdtemp())
    orig = pathlib.Path.cwd()
    os.chdir(cwd)
    try:
        rc = init_project.main(["checkup"])  # never init'd
        assert rc != 0, "uninit'd project should exit non-zero"
    finally:
        os.chdir(orig); shutil.rmtree(cwd, ignore_errors=True)
    print("test_checkup_missing_workspace: PASS")
```

Add both to `__main__`.

- [ ] **Step 2: Run — verify they fail (cmd_checkup not defined)**

```bash
cd sci-skills-thesis/skills/thesis-init/scripts && python3 test_init.py
```
Expected: failure on `test_checkup_healthy` (`cmd_checkup` / `main` AttributeError).

- [ ] **Step 3: Implement cmd_checkup**

Add to `init_project.py` (mirror article-init's `cmd_checkup` — scan thesis/ + sci-skills/, report what's present, list issues, return 0 if healthy else 1):

```python
def cmd_checkup(args: argparse.Namespace) -> int:
    root = find_project_root()
    fam = family_root(root)
    report: list[str] = [f"checkup @ {root}"]
    issues: list[str] = []

    th = root / THESIS_DIR_NAME
    if not th.is_dir():
        issues.append(f"✗ {THESIS_DIR_NAME}/ 不存在。跑 `init` 建它。")
    else:
        tex_files = list((th / "tex").glob("*.tex")) if (th / "tex").is_dir() else []
        report.append(f"thesis/   ✓  tex 文件: {len(tex_files)}")
        if not (th / "template-spec.md").is_file():
            issues.append("⚠ thesis/template-spec.md 缺失（模板未织入？）")

    if not fam.is_dir():
        issues.append(f"✗ {FAMILY_ROOT_NAME}/ 不存在。跑 `init` 建它。")
    else:
        for name in SHARED_FILES_PLACEHOLDERS:
            if not (fam / name).is_file():
                issues.append(f"⚠ {FAMILY_ROOT_NAME}/{name} 缺失")
        for s in BROTHER_SKILLS:
            if not (fam / s / "CONTRACT.md").is_file():
                issues.append(f"⚠ {FAMILY_ROOT_NAME}/{s}/CONTRACT.md 缺失")

    report.append("")
    if issues:
        report.append("问题:")
        for it in issues:
            report.append(f"  {it}")
    else:
        report.append("✓ 布局健康。")
    print("\n".join(report))
    return 1 if issues else 0
```

- [ ] **Step 4: Run — verify checkup tests pass**

```bash
cd sci-skills-thesis/skills/thesis-init/scripts && python3 test_init.py
```
Expected: all six tests PASS.

- [ ] **Step 5: Commit**

```bash
git add sci-skills-thesis/skills/thesis-init/scripts/
git commit -m "thesis-init: cmd_checkup audits thesis/ + sci-skills/ layout"
```

---

## Task 9: references/family-layout.md (depth reference)

**Files:**
- Create: `sci-skills-thesis/skills/thesis-init/references/family-layout.md`

- [ ] **Step 1: Write the family-layout depth reference**

Mirror article-init's `references/family-layout.md` structure (Why the shared name `sci-skills/`; Source vs output split; Directory-contract principle; Per-directory contract overview; Cross-directory data flow; Naming conventions; Evolution rules; Decoupling self-check). Adapt to thesis family:

- **Why shared `sci-skills/`**: thesis and article families coexist in one workspace (a project may have both its small papers under `manuscript/` and its thesis under `thesis/`). thesis- prefixed shared files avoid collision.
- **Per-directory contract overview**: table of `thesis/` (first-class, by chapter), `sci-skills/thesis-sources.md` (registry), `sci-skills/thesis-spine.md` (接力棒), `sci-skills/thesis-terminology-ledger.md` (术语), `sci-skills/thesis-dissect|intro|theory|summary/` (working notes). Note: spine/polish/typeset/init have no dir (rationale).
- **Cross-directory data flow**: the writing-chain read relationships (spine→dissect→intro→summary→theory via files; no skill calls skill). The four shared files + `chapter-map.md` (dissect→summary). tex always lands in `thesis/tex/` (per `template-spec.md` naming), never in working-note dirs.
- **Naming conventions**: thesis- prefix for shared files; chapter filenames follow `template-spec.md` (not hardcoded); `chapter-map.md` fixed name.
- **Evolution rules**: add a sibling skill = add to `BROTHER_SKILLS` + write its `CONTRACT.md` (only skills needing an output dir); add a university template pack = add `templates/thesis/<school>/` + `template-spec.md`, no skill code change.
- **Decoupling self-check**: the checklist (files match CONTRACT.md; reading neighbors stays within contract; no skill assumes a specific sibling produced its input).

Write the full doc. Pull exact file relationships from the spec §Implementation Notes "跨 skill 文件交接" table.

- [ ] **Step 2: Commit**

```bash
git add sci-skills-thesis/skills/thesis-init/references/family-layout.md
git commit -m "thesis-init: references/family-layout.md (depth reference, mirror article-init)"
```

---

## Task 10: tests/README.md (test plan doc)

**Files:**
- Create: `sci-skills-thesis/skills/thesis-init/tests/README.md`

- [ ] **Step 1: Write the test plan README**

Mirror article-init's `tests/README.md` in shape (a prose test plan doc), but document the **stdlib test script** (`scripts/test_init.py`, run `python3 test_init.py`) and the cases it covers: init builds skeleton (incl. thesis/CONTRACT.md + thesis/.gitignore + thesis-README.md, NOT root .gitignore); init weaves template (flat files now; subdir recursion implemented for future multi-file packs); init idempotent; checkup healthy exits 0; checkup missing exits non-zero. Note that the source-registry interactive collection (the agent's job) is NOT script-tested — it's evaluated via skill-creator-plus's eval loop later. **State the test deviation honestly**: thesis-init adds a runnable stdlib test script where article-init has none (article-init's deterministic init_project.py is currently untested — its README admits the TODO); this is a deliberate fix, and the justification is that init_project.py is deterministic code with objectively-verifiable file outputs (the case skill-creator-plus/testing.md says earns a runnable test).

- [ ] **Step 2: Commit**

```bash
git add sci-skills-thesis/skills/thesis-init/tests/README.md
git commit -m "thesis-init: tests/README.md test plan (stdlib, no pytest)"
```

---

## Task 11: End-to-end verification + follow-up task note

**Files:**
- No new files — verification only.

- [ ] **Step 1: Run the full test suite**

```bash
cd sci-skills-thesis/skills/thesis-init/scripts && python3 test_init.py
```
Expected: all six tests PASS (`test_constants`, `test_init_builds_skeleton`, `test_init_weaves_template`, `test_init_idempotent`, `test_checkup_healthy`, `test_checkup_missing_workspace`).

- [ ] **Step 2: Run init in a real temp project, inspect the tree**

```bash
tmp=$(mktemp -d) && cd "$tmp"
python3 /home/joe/Documents/repo/skill/sci-skills/sci-skills-thesis/skills/thesis-init/scripts/init_project.py init --no-git --template generic-test
echo "=== tree ===" && find . -not -path '*/.git/*' | sort
cd / && rm -rf "$tmp"
```
Expected: `thesis/` (CONTRACT.md + tex/{main.tex,template-spec.md} + .gitignore) + `sci-skills/` (thesis-README.md + thesis-sources.md + thesis-spine.md + thesis-terminology-ledger.md + thesis-{dissect,intro,theory,summary}/CONTRACT.md). No root `.gitignore` (init does not write it — avoids article-family collision).

- [ ] **Step 3: Confirm the woven template compiles (proves the test pack is real, not a stub)**

```bash
tmp=$(mktemp -d) && cd "$tmp"
python3 <repo>/sci-skills-thesis/skills/thesis-init/scripts/init_project.py init --no-git --template generic-test
# create minimal chapter stubs so main.tex \input resolves
printf '\\chapter{绪论}\n占位。\n' > thesis/tex/chapter0.tex
printf '\\chapter{理论}\n占位。\n' > thesis/tex/chapter1.tex
printf '\\chapter{总结}\n占位。\n' > thesis/tex/chapter_last.tex
touch thesis/tex/refs.bib
cd thesis/tex && xelatex -interaction=nonstopmode main.tex 2>&1 | tail -5
ls main.pdf 2>/dev/null && echo "PDF OK" || echo "PDF FAILED"
cd / && rm -rf "$tmp"
```
Expected: `main.pdf` created, `PDF OK`. (If xelatex missing, note as env limitation — the weave mechanism is still proven by the file copy; compilation is a bonus check.)

- [ ] **Step 4: Commit any final test/script fixes**

If Steps 1-3 revealed gaps, fix and commit:
```bash
git add -A && git commit -m "thesis-init: end-to-end verification fixes"
```

- [ ] **Step 5: Record the named follow-up (not a task in this plan)**

In the commit message or a note, record that the **real thuthesis (Tsinghua) template pack** is the next data-gathering task: `thuthesis.cls` is installed locally (TeX Live 2026) but is a full template *system* needing its own pack assembly (config + `template-spec.md` for Tsinghua's naming/structure). That is a separate plan, not part of this foundation. The `generic-test` pack proves the mechanism; a real school pack replaces it for actual use.

---

## Acceptance (this plan, against the spec's foundation slice)

- [ ] `sci-skills-thesis/` is a valid Claude Code plugin (plugin.json parses; skills/ dir present).
- [ ] `thesis-init` scaffolds `thesis/` (CONTRACT.md + tex/) + `sci-skills/` shared files (thesis-sources.md / thesis-spine.md / thesis-terminology-ledger.md, thesis- prefixed) + brother skill dirs (dissect/intro/theory/summary) each with CONTRACT.md — verified by `test_init_builds_skeleton`.
- [ ] Template weave works: `--template generic-test` copies `main.tex` + `template-spec.md` into `thesis/tex/`, and the woven `template-spec.md` carries the naming convention — verified by `test_init_weaves_template`.
- [ ] init is idempotent (re-run doesn't overwrite) — `test_init_idempotent`.
- [ ] `checkup` exits 0 on a healthy layout, non-zero when missing — `test_checkup_healthy` / `test_checkup_missing_workspace`.
- [ ] The woven minimal template compiles to PDF (proves the test pack is real, not a stub).
- [ ] No pytest dependency; tests are stdlib `python3 test_init.py`.
- [ ] glossary thesis terms present (6 terms).
- [ ] spine/polish/typeset/init correctly have NO output dir.
- [ ] No skill calls a sibling skill (init only writes files + contracts; the writing-chain read-relationships are documented in family-layout.md, not coded).

**Out of scope for this plan (named follow-ups):**
- The 7 prose skills (spine/dissect/intro/theory/summary/typeset/polish) — each its own plan.
- Real university template packs (thuthesis for Tsinghua, etc.) — data/assembly task; `generic-test` proves the mechanism.
- Cheap-model orchestration entry (`using-thesis-skills`) — v1 cut per spec §⑦.
- Cross-family terminology-ledger unification (thesis vs article) — v1 cut per spec.
