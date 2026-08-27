# Plan Task-Decomposition Review — thesis-theory

**Document**: docs/superpowers/plans/2026-08-27-thesis-theory.md
**Spec read for context**: docs/superpowers/specs/thesis-theory.md (+ glossary checked)
**Reviewer**: libra
**Scope**: task decomposition only — startability / boundaries / dependencies / placeholders / file existence. Design logic NOT re-judged (aquarius already approved; its 4 precision fixes verified applied to the plan text).

## Status
Approved

## Issues
None blocking.

## Verification evidence (what was checked on disk, not assumed)

1. **Startability** — every task has a concrete entry point:
   - Task 1: verbatim `cp` command, full test file inline (18 cases), exact replacement docstring/constants/check()/main() provided; the keep-verbatim helper list (`_split_sections`/`_SCOPE_TERMINATOR`, `_fences_balanced`, `_field_value`, `_top_level_field`, `_is_empty`, `_header_numbers`, `_single_ref_number`, `_sanitize`, `_CTRL_RE`, `_NONE_TOKENS`) **matches actual definitions in shipped `check_summary.py` byte-for-byte** (verified lines 32–136). `PurePath` is already imported there (`from pathlib import Path, PurePath`), so 4c's traversal guard needs no import edit.
   - Task 2: append block + runner extension listed line-by-line (17 cases); 18+17=35 matches every "35 tests" claim in Tasks 5 and 7 — internally consistent.
   - Task 3: frontmatter verbatim; nine numbered body requirements each pinned to a spec §; verification script inline.
   - Task 4: six content bullets per reference file with target lengths.
   - Task 6: all four before/after replace blocks match `init_project.py` lines 224–252 **exactly as they sit on disk today** (有什么用 line 233 / 文件清单 line 237 / 产物怎么进来 line 245 / 谁读它 line 250); anchors are text-matched so line drift cannot break them; `init --no-git` confirmed a real first-class flag.
   - Task 7: commands concrete; base-sha dependency wired back to Pre-flight Step 0.

2. **Task boundaries** — clean one-artifact-per-task slicing: gate+tests → pinning tests → SKILL.md → references → tests README → init edit → verification. No task mixes unrelated subsystems. Task 6 is the sole foundation touch and states its four sub-edits with per-edit justification booked.

3. **Dependencies** — all stated: Tasks 1–2 feed Task 3 (SKILL.md references check_theory.py — said in Task 3's preamble); Task 3→Task 4 forward reference explicitly acknowledged with the transient-inconsistency note; Pre-flight sha feeds Task 7 Step 3; spec authority named "read in full before Task 1".

4. **Placeholders** — none. No TBD/TODO/"similar to Task N". Red-state expectation in Task 1 Step 3 is framed as falsifiable prediction with a fallback rule ("any erroring out counts as red") — implementer-safe.

5. **Referenced files exist**: `thesis-theory.md` spec ✓, parent family spec ✓, mirror `thesis-summary/SKILL.md` + `scripts/check_summary.py` + `tests/README.md` ✓, `thesis-spine/scripts/check_spine.py` ✓ (its `PENDING_MARKER` usage confirms the "[pending?" convention the spine re-verify reuses) ✓, `sci-skills/skills/thesis-init/scripts/{init_project.py,test_init.py}` ✓, aquarius review file referenced by Task 7's commit allowance ✓.

6. **Glossary alignment** — no `_Avoid_` alias used ("overlap resolution gate"/"dedup list": 0 occurrences in the plan); settled term "Overlap 清单" used throughout.

## Recommendations (advisory, do not block)
- The init CONTRACT block sits at lines 224–252 today; if master moves before execution, the text-matched anchors still hold — no action needed, noted only because Task 6's header says "~line 224".
- Task 6 Step 2's expected message assumes `test_init.py` prints an ALL-tests-pass line on success; whatever the script actually prints, the rc=0 path is what matters — implementer should not be surprised by cosmetic wording differences.

## Verdict
Seven tasks, each independently startable by an implementer with zero prior context; spec cited as authority at every ambiguity point; zero-churn enforcement wired through a recorded base sha. Ready for capricorn.
