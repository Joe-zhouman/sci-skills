# thesis-init tests

Test plan — run via the stdlib test script (no pytest; the repo has no pytest config):

    cd scripts && python3 test_init.py

The eight cases in `scripts/test_init.py`:

1. **test_constants** — module constants pin the workspace layout:
   `FAMILY_ROOT_NAME="sci-skills"` (shared with the article family for coexistence),
   `THESIS_DIR_NAME="thesis"`, the four brother skills that get their own output dir
   (`thesis-dissect`, `thesis-intro`, `thesis-theory`, `thesis-summary`), and the top-level
   `thesis-*` shared placeholders. Asserts `thesis-spine`/`thesis-polish` do NOT get dirs
   (they write top-level shared files or edit tex in place).
2. **test_init_builds_skeleton** — `init --no-git` in a clean cwd produces the full
   skeleton: `thesis/` first-class artifact with `CONTRACT.md` + `tex/` + `.gitignore`;
   `sci-skills/` shared workspace with `thesis-sources.md`, `thesis-spine.md`,
   `thesis-terminology-ledger.md`, and `thesis-README.md` (thesis-prefixed to avoid the
   `README.md` collision the article family may own); one `CONTRACT.md` per brother-skill
   dir. Critically: init does NOT write a root `.gitignore` (collides with the article
   family's / human's).
3. **test_init_weaves_template** — `init --template generic-test` weaves the template pack
   into `thesis/tex/`. The generic-test pack ships flat files only (`main.tex`,
   `template-spec.md`); the test asserts `main.tex` lands in `tex/` AND `template-spec.md`
   lands at `thesis/template-spec.md` (NOT in `tex/` — `_weave_template` skips it there to
   avoid duplication, since `thesis/template-spec.md` is the canonical spot). The chosen
   template-spec's naming convention (`chapterN.tex`) is preserved in the woven spec.
   Subdir recursion is implemented in `_weave_template` via `shutil.copytree` for real
   multi-file packs (e.g. thuthesis with `config/`/`figures/` subdirs), but is not
   exercised by this test.
4. **test_init_idempotent** — re-running `init` with identical args exits 0 and does NOT
   overwrite existing files (content-snapshot equality on `tex/main.tex` and
   `thesis/CONTRACT.md`).
5. **test_checkup_healthy** — on a freshly-init'd layout, `checkup` exits 0.
6. **test_checkup_missing_workspace** — on an uninit'd cwd, `checkup` exits non-zero
   (reports missing `thesis/` and `sci-skills/`).
7. **test_checkup_prints_json** — U1: `checkup` prints a `--- JSON ---` block for
   programmatic consumption (mirrors article-init), including `project_root`, `thesis`,
   and `sci-skills` state. Exercises the JSON-output path on a healthy layout (exit 0).
8. **test_checkup_reports_misplaced_items** — U1: a stray file dropped in the project
   root (not under `thesis/` or `sci-skills/`) is named in the checkup report AND
   surfaces in the JSON under `root_candidates`; checkup exits non-zero. Exercises the
   misplaced-items scan added in the U1 round.

Each `CONTRACT.md` is verified by string match on key sections (`thesis/CONTRACT.md`
first-class-artifact framing; brother-skill contracts per their role).

## What is NOT script-tested

The source-registry interactive collection — the agent's job inside the skill — is
subjective and interactive, so it is NOT exercised by `test_init.py`. It is evaluated via
skill-creator-plus's eval loop later (subject to the skill triggering correctly). That
matches skill-creator-plus/testing.md: subjective/interactive outputs get the eval loop,
not a deterministic script.

## Why a runnable test here (honest deviation from article-init)

Thesis-init adds a runnable stdlib test script where article-init has none.
article-init's deterministic `init_project.py` is currently untested — its `tests/README.md`
admits "TODO: run the full Test loop". This is a deliberate fix, not a
matching-repo-convention carry-forward. The justification (per skill-creator-plus/testing.md):
`init_project.py` is deterministic code with objectively-verifiable file outputs (files
exist/don't, content matches, idempotency holds) — exactly the case that earns a runnable
test. The article family inherits an untested gap; thesis-init fixes it rather than
carrying it forward. Prose skills later use the eval loop, not a script — that's the right
tool for subjective outputs.
