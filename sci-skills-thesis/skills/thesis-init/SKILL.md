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

# thesis-init

Manual scaffold + template-weave + audit tool. Run once, exit. It builds `thesis/` — the
first-class artifact organized by chapter (not review-round) — plus the `sci-skills/` shared
workspace (thesis-prefixed files, so it coexists with the article family in the same dir) and
each skill's `CONTRACT.md`, and weaves a selected university template pack into `thesis/tex/`.
It does not stay running and does not advance the writing chain (the human does, by invoking
each writing skill). It does not draw figures or write prose.

**This is the only skill in the family that knows about all sibling skills.** Every other skill
is decoupled — it only knows files. thesis-init is the entry node carrying the routing table
(on-disk compass file: `BROTHER_SKILLS` in `init_project.py` + each dir's `CONTRACT.md`); when
the user wants to spine / dissect / write a chapter / typeset / polish, check the table below
and invoke the right skill via the Skill tool. Don't try to do the work without the skill — each
one has procedures, references, and guardrails that prevent specific failures.

## Sibling skills

| When the user says | Invoke |
|---|---|
| 提主线 / 统一框架 / 章间递进 / thesis spine / 主线 | `thesis-spine` |
| 拆小论文 / 写正文章 / 模块化重构 / dissect / 拆即写 | `thesis-dissect` |
| 写绪论 / 研究现状 / gap / write introduction | `thesis-intro` |
| 写共用理论方法 / 第二章 / theory | `thesis-theory` |
| 写总结 / 共性提炼 / callback / 展望 / write summary | `thesis-summary` |
| 排版 / 编译 / .cls 合规 / 盲审格式 / typeset | `thesis-typeset` |
| 润色 / 术语统一 / AIGC 降率 / 去 AI 味 / polish | `thesis-polish` |
| 初始化 / init / 建目录 / scaffold / checkup | (this skill) |

## Division of labor

The core philosophy: **确定性归脚本，判断性归 agent.**

- **Deterministic → the script** (`scripts/init_project.py`): build the directory skeleton, write
  each dir's `CONTRACT.md`, weave the selected template pack into `thesis/tex/`, create the
  shared-file placeholders. Idempotent, no judgment — re-running skips existing files, never
  overwrites.
- **Judgment / interactive → the agent** (this skill's prose, not a script): interactively
  collect the source registry (which small papers, where their data lives — scattered across
  folders), decide which template pack to use, confirm the project root. The agent writes the
  registry as simple markdown per the schema (§ The source registry) — there is no script for it,
  because the registry is plain markdown the agent fills by asking the user.

The script never writes registry content; the agent never writes skeleton/contracts. The script
is reproducible and audit-safe; the agent keeps the user in control of placement decisions.

## Layout it builds

```
<project-root>/
  thesis/                          ← 一等产物（正文 tex，working notes 绝不落这）
    CONTRACT.md                    ← thesis/ 接口契约（章制、模板已织好、谁读写；不重复模板要求）
    tex/                            ← init 织入所选大学 .cls（main.tex/章文件/前置后置/refs.bib 按模板要求名）
    template-spec.md               ← 从模板包复制（该模板文件命名约定，各 skill 读它对齐）
  sci-skills/                      ← 共享家族工作区（article + thesis 共用）
    thesis-README.md               ← thesis 家族自述 + routing table（thesis- 前缀避免与 article 的 README.md 碰撞）
    thesis-sources.md              ← 来源 registry（init 交互生成，所有 thesis skill 导航真相）
    thesis-spine.md                ← 主线+统一框架+章间递进+thesis级claim（spine 产，全家族读）★ thesis- 前缀避碰
    thesis-terminology-ledger.md   ← 术语表（spine 建，各章/polish 共写）★ thesis- 前缀避碰
    thesis-dissect/                ← 拆+写正文章（带每篇小论文第3级子文件夹）
      paper-A/                     ← 该篇拆解笔记（章映射/模块重构/question→claim）
      paper-B/
    thesis-intro/                  ← 绪论章 working notes
    thesis-theory/                 ← 第二章 working notes
    thesis-summary/                ← 总结章 working notes
```

Three things to internalize about this layout:

- **`thesis/` is the product; `sci-skills/` is the shared workspace.** `thesis/` is a first-class
  artifact at the project root, organized by chapter (not review round), and the template is
  woven into `tex/` at init — before any prose is written (unlike the article family, which moves
  templates at submission). Working notes never land in `thesis/`; they live in `sci-skills/`.
- **Each dir's `CONTRACT.md` is a directory-level contract, not a help file.** Any agent/skill
  producing into a dir follows that contract (schema, naming, who reads it) without needing to
  know which skill consumes it. This is how the family decouples. init generates these contracts;
  if the user just `mkdir`s, the contracts are missing and downstream skills can't mesh.
- **Shared files are `thesis-` prefixed** (`thesis-sources.md` / `thesis-spine.md` /
  `thesis-terminology-ledger.md` / `thesis-README.md`) so the thesis family coexists with the
  article family in the same `sci-skills/` dir without collision. thesis-init is the only node
  that knows all siblings; every other skill reads these files (compass-file coupling, no skill
  imports another).

Full layout rationale (why the fixed name, product-vs-workspace split, naming-collision rules,
decoupling self-check) is in `references/family-layout.md` — read it when modifying the layout or
contracts or adding a sibling skill, not on every run.

## init

Two subcommands: `init` (below) and `checkup` (audit). Builds the skeleton above in the current
directory and weaves the selected template pack into `thesis/tex/`.

```bash
python scripts/init_project.py init                          # skeleton + contracts + template weave + placeholders
python scripts/init_project.py init --template tsinghua      # select a template pack by name
python scripts/init_project.py init --template-dir <path>    # user-supplied .cls + spec (degraded mode)
python scripts/init_project.py init --no-git                 # skip git init
```

For exact args, `python scripts/init_project.py --help`. Template selection (`--template` /
`--template-dir`) is detailed in § Template selection.

Idempotent — re-running skips existing dirs/files, never overwrites. Builds `thesis/` (with
`tex/` + `CONTRACT.md` + `template-spec.md`), the `sci-skills/` shared-file placeholders
(`thesis-README.md`, `thesis-sources.md`, `thesis-spine.md`, `thesis-terminology-ledger.md`),
and each writing skill's working-notes dir + `CONTRACT.md`. It does **not** generate registry
content (the agent fills `thesis-sources.md` interactively) and does **not** generate spine or
terminology content (those are `thesis-spine`'s job).

If `thesis/` or `sci-skills/` already exists, init still fills in any missing `CONTRACT.md`
contracts and placeholders (so an existing project that predates the contracts gets them
retroactively without clobbering content).

## Template selection

init takes `--template <pack-name>` to select a university template pack from `templates/thesis/`
(shipped inside the plugin, so it's self-contained on standalone install).

- **One pack** in `templates/thesis/`: default to it; `--template` optional.
- **Many packs**: the agent asks the user which school and passes `--template <name>`.
- **User's school not packaged yet**: `--template-dir <path>` points at a user-supplied directory
  containing the `.cls` + a `template-spec.md`. If the spec is absent, init weaves the `.cls` but
  skips `thesis/template-spec.md` — downstream skills have no naming convention until one is added
  manually. (Generating a spec from a bare `.cls` is not done — it would require parsing the class
  file; the human writes the spec, same as any other template-pack author.)

A template pack = `templates/thesis/<school>/`: the `.cls` + a blueprint (`main.tex` + front/back
-matter skeleton) + `template-spec.md` (file-naming convention, `refs.bib` name, chapter
organization, front/back-matter checklist, compile requirements). Adding a school = adding a
pack directory, no skill code changes.

## checkup

Audit the current layout. Read-only, never modifies anything.

```bash
python scripts/init_project.py checkup
```

Reports:

- `thesis/` present? `tex/` has `.cls` + `main.tex`? which chapter files exist? `thesis/template-spec.md` present?
- `sci-skills/` present? each shared file present? (`thesis-sources.md` / `thesis-spine.md` /
  `thesis-terminology-ledger.md` / `thesis-README.md`) — the agent or human judges "filled" by reading it
- each writing skill's working-notes dir + `CONTRACT.md` state
- **misplaced items** — anything in the project root that isn't under `thesis/` or `sci-skills/`
- git status

Exit code is non-zero if there are issues; the JSON block (printed after the human-readable table)
is for programmatic consumption.

## The source registry (`thesis-sources.md`)

The agent's interactive job — there is no script for it. The registry is plain markdown the agent
fills by asking the user, then every thesis skill reads it to locate scattered sources. **Never
hardcode source dirs in any skill.**

For each small paper that will become a thesis chapter, ask the user:

- **paper_id** — stable identifier (e.g. `paper-A`); used as the `thesis-dissect/paper-A/` dir name
  and the chapter-map key
- **path(s)** — the paper's manuscript folder(s); may be multiple (a paper split across folders)
- **data_path(s)** — where its data lives; may be scattered across folders
- **slug** — chapter-name token per the template's convention (e.g. `ch3` → `ch3.tex`)
- **claim** — optional at init; filled later by `thesis-dissect`

Write entries to `sci-skills/thesis-sources.md` per its `CONTRACT.md` schema. This file is the
single navigation truth — every thesis skill reads it to locate scattered sources. The registry
may be extended later (add a paper, fix a path) by editing the file directly; re-running `init`
won't clobber it (idempotent — skips existing).

Collect the registry as part of running init: the agent asks the user paper-by-paper, the script
has already created the placeholder, the agent fills it in.

## After init

Point the user at **`thesis-spine`** — the next skill, which establishes the main line + unified
framework + chapter progression + thesis-level claim. Do **not** auto-run it. thesis-init
scaffolds and exits; the human advances the pipeline by invoking each writing skill. (Read
neighbors, don't orchestrate — a skill may read another's on-disk outputs to sense what's ready,
but must not trigger another skill to run.)

## Constraints

- **Manual trigger, run once, exit.** No daemon, no watching, no auto-advancing the pipeline.
- **Idempotent.** Existing dirs/files are skipped, never overwritten.
- **Determinism to the script, judgment to the agent.** init / checkup / template-weave are
  mechanical (script); collecting the source registry, choosing the template pack, and confirming
  the project root are the agent's job (asking the user). The script never writes registry content;
  the agent never writes skeleton or contracts.
- **Only the output side, never the source side.** It manages the project's `thesis/` and
  `sci-skills/`; it never touches the plugin's `skills/` or `templates/`.
- **Does not produce prose, figures, spine, or submissions** — those are other skills. It only
  scaffolds the workspace and weaves the template.

## Sibling dirs

Have working-notes dirs (created by init, with `CONTRACT.md`): `thesis-dissect` (with a `paper-X/`
subdir per source paper), `thesis-intro`, `thesis-theory`, `thesis-summary`. No own dir (produce
top-level shared files / edit tex in place / entry-exit): `thesis-spine` (produces
`thesis-spine.md` + builds `thesis-terminology-ledger.md`), `thesis-polish` (git trail on
`thesis/tex/`), `thesis-typeset` (git trail on `thesis/tex/`), `thesis-init` (entry, exits).

## Privacy

Don't leak private paths or unpublished content in generated contracts (`CONTRACT.md`), the
registry, or audit reports. The paths shown in a checkup report or collected into the registry are
the user's own project paths (visible to them, not exfiltrated).
