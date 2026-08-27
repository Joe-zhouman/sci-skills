# Plan Task-Decomposition Review — thesis-dissect

**Document**: `docs/superpowers/plans/2026-08-26-thesis-dissect.md`
**Reviewer**: libra
**Spec (context)**: `docs/superpowers/specs/thesis-dissect.md` (aquarius round-2 "Lean. Ship." — design logic not re-checked)

## Status
Approved

## Decomposition check (all pass)

- **Startability**: Every task has exact file paths + real code in every code-step + expected outputs stated.
  - Tasks 1–2 (TDD): full verbatim Python source for both `test_check_dissect.py` and `check_dissect.py`; run commands + expected pass/fail lines given.
  - Tasks 3–5 (prose): detailed content outlines with spec §references (§①–⑧, §跨 skill 文件交接, §工作流, §门与 enforcement) + named mirror files to follow (spine SKILL.md, sci-write section-templates.md, spine tests/README.md). Task 3 adds a runnable `assert`-based verify script verbatim.
  - Task 6 (verification): all grep/run/diff commands given verbatim with expected output strings.
- **Boundaries**: One artifact/concern per task. No grab-bag. Task 1 = core coverage; Task 2 = tex-file extension (clean TDD continuation); Tasks 3/4/5 = one file each; Task 6 = verification only (no new files).
- **Dependencies stated + correctly ordered**:
  - Task 2 → Task 1: extends `check()`, replaces the `# 5. tex-file ... (Task 2 在此扩展)` marker Task 1 deliberately leaves.
  - Task 3 → Tasks 1–2: "check_dissect.py (Tasks 1–2) already exists for SKILL.md to reference" — explicit.
  - Task 4 → Task 3: "The load-on-demand reference SKILL.md indexes (Task 3)" — explicit.
  - Task 5 → Tasks 1–2: references the test cases by name.
  - Task 6 → all + Pre-flight BASE sha.
- **Placeholders**: None that are plan defects.
  - The `# 5. ... (Task 2 在此扩展)` marker in Task 1's check_dissect.py is an intentional TDD handoff point — Task 2 Step 3 replaces it with real code.
  - `<BASE>` in Task 6 is a documented substitution (Pre-flight Step 0 records it; Task 6 Step 4 says "Replace `<BASE>` with the Pre-flight sha").
  - The "TODO" in Task 5's tests/README.md §4 is content of the README being written (intentional output), not a plan gap.
- **Referenced files exist** (verified on disk):
  - Mirrors: `sci-skills-thesis/skills/thesis-spine/{SKILL.md, scripts/check_spine.py, scripts/test_check_spine.py, tests/README.md, references/}` ✓; `sci-skills-article/skills/sci-write/references/section-templates.md` ✓.
  - Plugin root `sci-skills-thesis/` exists (`.claude-plugin/` + `skills/`) ✓. `thesis-dissect/` does not exist yet — Task 1 Step 1 creates it via `mkdir -p` ✓.
  - Parent specs `thesis-skill-family.md` + `thesis-spine.md` exist ✓.
  - Task 6 Step 4 diff paths both match reality: `sci-skills/skills/thesis-init/` (shared plugin, deliberate per recent commits) + `sci-skills-thesis/skills/thesis-spine/` ✓.
- **Spec §numbers valid**: §①–⑧ all present in spec; §跨 skill 文件交接 / §工作流 / §门与 enforcement / §Implementation Notes all present. (§Load-bearing premise is parent-spec territory — Task 3 cites it as "spec §Load-bearing premise" slightly imprecisely, but the dissect spec references it inline and the concept is unambiguous; not a blocker.)
- **chapter-map.md schema**: the spec's schema block fields (framework-instantiation, progression-in/out, tex-file, status, `## Chapter N`) match exactly what check_dissect.py parses and what the test fixtures assert on.

## Recommendations (advisory, do not block)

- Task 3 Step 1 could note that `references/restructure-discipline.md` (created in Task 4) won't exist until Task 4 runs — a transient dangling reference between Tasks 3 and 4. The implementer can see this from the task order, so it's not blocking; an explicit one-liner would just remove all doubt.
