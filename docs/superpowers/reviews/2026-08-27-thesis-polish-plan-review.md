# Plan Task-Decomposition Review — thesis-polish

**Document**: /home/joe/Documents/repo/skill/sci-skills/docs/superpowers/plans/2026-08-27-thesis-polish.md
**Reviewer**: libra
**Scope**: task decomposition only (design already cleared by aquarius; Tasks 1-3 code empirically green 42/42)

## Status
Issues Found (2)

## Issues

1. **Task 8 Step 3 grep-1 self-fires on Task 1's own mandated artifact — the stated expectation is unreachable as written.** Task 1 Step 4 requires `check_polish.py` verbatim, including its docstring prose ("check_summary/check_intro/check_theory 等是 write-time check") and the two provenance docstrings the same step mandates ("【继承自 check_theory.py——verbatim】" on `_fences_balanced` and `_sanitize`). Task 8 Step 3 then greps `scripts/*.py` for exactly those literals and declares any hit a FAIL. Empirically confirmed: extracting Task 1's code block verbatim and running the plan's own grep yields 3 matches → "FAIL: script references a sibling's script", not the expected "SCRIPT-DECOUPLING-OK". The plan's rephrase remedy is written only for the second grep (references/SKILL.md), so a fresh-context implementer hits a contradiction at the final gate with no sanctioned resolution. **Fix (docstring-only, zero test impact):** in Task 1's code block, rephrase line-15 prose to not name sibling scripts (e.g. "写作链各 check 脚本是 write-time check 非 post-polish invariant"), and rephrase the two provenance docstrings to name the lineage without the literal filename (e.g. "【继承自理论章家族 check 硬化——verbatim】"). Alternatively reshape grep-1 — but scrubbing matches the plan's own stated remedy style.

2. **Stale test counts in two verbatim-executed spots.** Task 7's commit message says "22+8+9 cases" and Task 8 Step 5 says "39 tests green"; Task 8 Step 1 and Task 7 content §1 both say 25 + 8 + 9 = 42 (matching the empirically green run). Capricorn executes commit messages and report text verbatim, so the branch would carry a commit message that misstates the artifact it commits and a final report contradicting the plan's own Step 1. **Fix:** 22 → 25 and 39 → 42 (residue from pre-adversarial-round counts; three check tests were added with F1-F8).

## What checked out (no action needed)

- **Startability**: every task has exact file paths; Tasks 1-3 carry full code + full test files; Tasks 4-7 carry section-level content specs with named source files to read; Task 8 has exact commands. No guessing required anywhere.
- **Task boundaries**: 8 tasks, one artifact family each (gate / parser / parser / SKILL.md / new references / mirrored references / test README / verification). No grab-bags.
- **Dependencies**: stated where load-bearing — Tasks 1-3 before Task 4 ("Scripts already exist for it to reference"); wenqu parsers read before Tasks 2/3; check_theory.py opened and copied before Task 1; Pre-flight base sha feeds Task 8's zero-churn diff; Task 4→6 reference-index transience explicitly acknowledged.
- **No placeholders**: zero TODO/TBD in task bodies (line 7's "placeholder" is the init-precedent fact, not a gap).
- **Referenced files exist**: sci-polish SKILL.md + four named references; check_theory.py (helpers present); wenqu parse_paperyy.py / parse_paperpass.py; humanizer-zh SKILL.md; prose-pattern-abuse.md; thesis-dissect restructure-discipline.md; thesis-theory tests/README.md; both specs; glossary. `init_project.py` lives at `sci-skills/skills/thesis-init/scripts/init_project.py` and confirms polish 不预建 (BROTHER_SKILLS excludes it) — Task 8 Step 4's expected-diff path is correct.
- **Glossary**: AIGC 降率 / 去 AI 味 / 缝合 used verbatim; 缝合's `_Avoid_: 重构` respected (Task 4 assertion even pins it).
- **Task 4's assertion suite passes against its own body spec** (checked needle-by-needle, including S1 scope strings and the P3/P5/P8 pins).

## Recommendations (advisory, do not block)

- Task 8 Step 2 is labeled "(Task 4's script, re-run)" but embeds only the frontmatter subset of Task 4's suite. Label it as the subset, or restate the full suite, so a fresh-context implementer doesn't have to decide which is meant.
- After Issue 1's fix, Task 1 Step 4's phrase "keep their docstrings with the theory-family artifact names updated to polish's" should state the exact replacement string — it is currently ambiguous, and that ambiguity is what let the literal `check_theory.py` survive into the mandated docstrings.

## Routing
Back to **writing-plans** for the two fixes (both one-line edits to already-written blocks); then straight to **capricorn** — no re-review of unchanged tasks needed beyond the edited lines.
