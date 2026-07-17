---
name: sci-skills-init
description: >-
  科研项目初始化 / Research project init — scaffold manuscript/ + sci-skills/ skeleton,
  write directory contracts, audit layout, migrate legacy files. 纯手动，不自动触发。
  Manual only. 不画图不写文不投稿 / Does not draw, write, or submit.
---

# sci-skills-init

Manual scaffold + audit tool. Run once, exit. It builds the directory skeleton
and the directory contracts; it does not stay running and does not advance the
figure→prose pipeline (the human does, by using each skill).

**This is the only skill in the family that knows about all sibling skills.**
Every other skill is decoupled — it only knows files. When the user wants to
draw / write / polish / submit, check the table below and invoke the right skill
via the Skill tool. Don't try to do the work without the skill — each one has
procedures, references, and guardrails that prevent specific failures.

## Sibling skills

| When the user says | Invoke |
|---|---|
| 画图 / plot / figure / chart / 数据可视化 / revise figure | `sci-draw` |
| 写论文 / write results / method / conclusion / 从数据写正文 | `sci-write` |
| 写引言 / 写讨论 / 写摘要 / write introduction / discussion / abstract | `sci-story` |
| 润色 / polish / revise paragraph / proofread / 翻译 / 排版 / LaTeX layout | `sci-polish` |
| 投稿 / submit / cover letter / 选期刊 / 被拒转投 / 投稿追踪 | `sci-submit` |
| 导出 / export / md转tex / tex转Word / md→tex / tex→docx | `sci-export` |
| 初始化 / init / 建目录 / scaffold / checkup / 迁移老项目 | (this skill) |

## Layout it builds

```
<project-root>/
  manuscript/                      ← the official manuscript (first-class citizen, at root)
    CONTRACT.md                    ← directory contract (v/r round scheme)
    v1/                            ← original draft (empty; user picks the tex template)
  sci-skills/                      ← skill-output region (family namespace, fixed name)
    README.md                      ← family self-description (generated)
    sci-draw/    + CONTRACT.md     ← figure warehouse (contract)
    sci-write/   + CONTRACT.md     ← writing intermediate products (contract)
    sci-submit/  + CONTRACT.md     ← submission products (contract)
  .gitignore                       ← common research-project ignores
  .git/                            ← git init (unless --no-git)
```

Two things to internalize about this layout:

- **`manuscript/` is the product; `sci-skills/` is tool output.** The manuscript is a first-class citizen at the project root because it often arrives from outside (Word / Overleaf / a collaborator's project) and is bigger than any one skill. Skills serve it; none owns it.
- **Each subdirectory's `CONTRACT.md` is a directory-level contract, not a help file.** Any agent/skill producing into a directory follows that contract — schema, field names, naming, who reads it — without needing to know which skill consumes it. This is how the family decouples. `init` generates these contracts; if the user just `mkdir`s, the contracts are missing and downstream skills can't mesh.

The manuscript is organized by review round (single dimension): `v1` = original draft (one v1 can submit to many journals — most are your-paper-your-way); `rN` = Nth revision package (revised tex + Response + reviews + revision cover letter). Which journal a v/r went to lives in `sci-skills/sci-submit/submit-history.md`, not in the directory structure. `init` builds only `v1/`; `r1`/`r2` are created when revision actually happens.

Full layout rationale (why the fixed name, source-vs-output split, evolution rules, decoupling self-check) is in `references/family-layout.md` — read it when modifying the layout or contracts, not on every run.

## init

Builds the skeleton above in the current directory.

```bash
python scripts/init_project.py init           # skeleton + contracts + .gitignore + git init
python scripts/init_project.py init --no-git  # skip git init
```

Idempotent — re-running skips existing dirs/files, never overwrites. Only builds empty `v1/` and the contracts; it does **not** generate any tex template content (templates are highly customized — the user decides; repo `templates/main/` is a reference blueprint). `r1`/`r2` are not pre-built.

If `manuscript/` or `sci-skills/` already exists, init still fills in any missing `CONTRACT.md` contracts (so an existing project that predates the contracts gets them retroactively without clobbering content).

## checkup

Audit the current layout. Read-only, never modifies anything.

```bash
python scripts/init_project.py checkup
```

Reports:
- `manuscript/` present? which rounds exist (`v1`/`r1`/`r2`)? does `v1/` have content?
- `sci-skills/` present? each sibling dir's state
- **misplaced items** — anything in the project root that isn't under `manuscript/` or `sci-skills/`. This is the signal to migrate (see below).
- git status

Exit code is non-zero if there are issues; the JSON block (printed after the human-readable table) is for programmatic consumption.

## Migrate a legacy project (agent flow, not a script subcommand)

There is no `migrate` subcommand. Old-project structures vary wildly (Word docs, Overleaf zips, a collaborator's weird layout); hardcoded rules misjudge user files (treating a `.md` note as the manuscript is a disaster). Migration is an agent flow:

1. Run `checkup`. It reports misplaced items in the project root.
2. Dispatch **Explore** to read those items' contents and judge where each belongs (script sees only filenames; Explore can tell "this is the manuscript" vs "this is an old figure warehouse" vs "this is a scratch note").
3. Confirm each proposed destination with the user (manuscript → `manuscript/v1/`, old figures → `sci-skills/sci-draw/`, etc.).
4. Issue `mv` commands yourself, after the user confirms.

The script never moves user files. Determinism belongs to the script (init/checkup); judgment belongs to Explore; moving files belongs to the agent + human.

## Constraints

- **Manual trigger, run once, exit.** No daemon, no watching, no auto-advancing the pipeline.
- **Idempotent.** Existing dirs/files are skipped, never overwritten.
- **Determinism to the script, judgment to the agent.** init/checkup are mechanical (script); reading content to judge placement is Explore's job; moving user files is agent + human.
- **Only the output side, never the source side.** It manages the project's `manuscript/` and `sci-skills/`; it never touches the repo's `skills/`.
- **Does not produce figures, prose, or submissions** — those are other skills. It only scaffolds and audits the workspace.

## Sibling dirs

Pre-built (design settled): `sci-draw`, `sci-write`, `sci-submit`. `sci-polish` is not pre-built (zero output dir — it edits manuscript tex directly).

## Privacy

Don't leak private paths or unpublished content in generated contracts (`CONTRACT.md`) or audit reports. The paths shown in a checkup report are the user's own project paths (visible to them, not exfiltrated).
