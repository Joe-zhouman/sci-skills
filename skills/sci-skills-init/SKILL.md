---
name: sci-skills-init
description: >-
  Scaffold and audit the sci-skills family workspace for a research project. Run
  when the user explicitly asks to initialize a project, set up the manuscript/
  and sci-skills/ layout, or check that on-disk outputs are in the right place.
  Manual only — does not auto-trigger; the user invokes it on purpose. Creates
  the directory skeleton + directory contracts (.README.md) + git init, and runs
  a placement audit. It does not draw figures, write prose, or submit — those are
  other skills. Triggers: 初始化科研项目, 建sci-skills目录, 检查落盘位置,
  init research project, scaffold sci-skills.
disable-model-invocation: true
---

# sci-skills-init

Manual scaffold + audit tool. Run once, exit. It builds the directory skeleton
and the directory contracts; it does not stay running and does not advance the
figure→prose pipeline (the human does, by using each skill).

## Layout it builds

```
<project-root>/
  manuscript/                      ← the official manuscript (first-class citizen, at root)
    .README.md                     ← directory contract (v/r round scheme)
    v1/                            ← original draft (empty; user picks the tex template)
  sci-skills/                      ← skill-output region (family namespace, fixed name)
    README.md                      ← family self-description (generated)
    sci-draw/    + .README.md      ← figure warehouse (contract)
    sci-write/   + .README.md      ← writing intermediate products (contract)
    sci-submit/  + .README.md      ← submission products (contract)
  .gitignore                       ← common research-project ignores
  .git/                            ← git init (unless --no-git)
```

Two things to internalize about this layout:

- **`manuscript/` is the product; `sci-skills/` is tool output.** The manuscript is a first-class citizen at the project root because it often arrives from outside (Word / Overleaf / a collaborator's project) and is bigger than any one skill. Skills serve it; none owns it.
- **Each subdirectory's `.README.md` is a directory-level contract, not a help file.** Any agent/skill producing into a directory follows that contract — schema, field names, naming, who reads it — without needing to know which skill consumes it. This is how the family decouples. `init` generates these contracts; if the user just `mkdir`s, the contracts are missing and downstream skills can't mesh.

The manuscript is organized by review round (single dimension): `v1` = original draft (one v1 can submit to many journals — most are your-paper-your-way); `rN` = Nth revision package (revised tex + Response + reviews + revision cover letter). Which journal a v/r went to lives in `sci-skills/sci-submit/submit-history.md`, not in the directory structure. `init` builds only `v1/`; `r1`/`r2` are created when revision actually happens.

Full layout rationale (why the fixed name, source-vs-output split, evolution rules, decoupling self-check) is in `references/family-layout.md` — read it when modifying the layout or contracts, not on every run.

## init

Builds the skeleton above in the current directory.

```bash
python scripts/init_project.py init           # skeleton + contracts + .gitignore + git init
python scripts/init_project.py init --no-git  # skip git init
```

Idempotent — re-running skips existing dirs/files, never overwrites. Only builds empty `v1/` and the contracts; it does **not** generate any tex template content (templates are highly customized — the user decides; repo `templates/main/` is a reference blueprint). `r1`/`r2` are not pre-built.

If `manuscript/` or `sci-skills/` already exists, init still fills in any missing `.README.md` contracts (so an existing project that predates the contracts gets them retroactively without clobbering content).

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

Currently pre-built (design settled): `sci-draw`, `sci-write`, `sci-submit`. `sci-polish` is deferred (strategy TBD); it gets added to `BROTHER_SKILLS` + `SKILL_DIR_GUIDES` in `scripts/init_project.py` once decided. Only pre-build skills whose design is settled — don't pre-build what isn't thought through.

## Privacy

Don't leak private paths or unpublished content in generated contracts (`.README.md`) or audit reports. The paths shown in a checkup report are the user's own project paths (visible to them, not exfiltrated).
