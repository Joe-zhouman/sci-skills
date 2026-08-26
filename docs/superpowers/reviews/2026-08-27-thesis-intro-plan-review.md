# Plan Task-Decomposition Review — thesis-intro

**Document**: `docs/superpowers/plans/2026-08-27-thesis-intro.md`
**Reviewer**: libra

## Status
Approved

## Issues (if any, max 3)
None blocking.

## Recommendations (advisory, do not block)
- **Task 2 Step 3 — code placement instruction is ambiguous.** The instruction says "replace the `# Task 2 在此处扩展 cross-ref 检查` line with: [code block]." But the marker sits at function-level (4-space indent, BEFORE the `for label, body in gaps:` loop), while the replacement code's `# 6. filled-by` block uses `body`/`label` (for-loop variables) at 8-space indent — it must go INSIDE the for loop, after the `# 4. status` check. The `# 若 chapter-map.md 缺失` block (4-space indent) correctly goes after the for loop. A literal find-and-replace of the marker line would place the `# 6.` block before the for loop where `body` is undefined, producing a `NameError` at runtime (not a `SyntaxError` — the code parses, but `check()` would crash when `chapter_map_path.is_file()` is True). A competent implementer reading the replacement code's `body` usage and 8-space indent would infer the correct placement, but this costs one debug cycle. Fix: reword the instruction to split the two placements explicitly (e.g., "Add the `# 6. filled-by` block inside the for loop after the status check; add the `# 若 chapter-map.md 缺失` block after the for loop"), or move the marker inside the for loop in Task 1's code.

## Checklist (what was verified)
- [x] Every task has a clear starting point with exact code, file paths, commands, and expected output
- [x] Task boundaries are sensible — each task is one focused unit (Task 1 = core checks, Task 2 = cross-ref, Task 3 = SKILL.md, Task 4 = references, Task 5 = tests/README, Task 6 = init placeholder, Task 7 = verification)
- [x] Dependencies are stated — Task 2 extends Task 1's check_intro.py (stated in Task 2 header); Task 7 depends on all prior (stated in Task 7 header); Task 3 references Tasks 1-2's check_intro.py
- [x] No placeholders or TODOs (the `<BASE>` in Task 7 Step 4 is explicitly addressed: "Replace `<BASE>` with the Pre-flight sha," recorded in Pre-flight Step 0)
- [x] All referenced sibling files exist: `sci-skills-thesis/skills/thesis-spine/` (scripts/check_spine.py + test_check_spine.py), `sci-skills-thesis/skills/thesis-dissect/` (scripts/check_dissect.py + test_check_dissect.py + references/ + tests/README.md), `sci-skills-article/skills/sci-story/` (references/ with writing-discipline.md + literature-search.md + introduction-guide.md), `sci-skills/skills/thesis-init/scripts/init_project.py` + `test_init.py` (placeholder text at lines 191-219 matches the plan's "find" text exactly), parent spec `docs/superpowers/specs/thesis-skill-family.md`
- [x] Test counts match: Task 1 = 11 tests (`ALL CORE TESTS PASS`), Task 2 adds 4 = 15 total (`ALL TESTS PASS`) — matches plan's expected output
- [x] Terminology aligns with glossary — uses "Narrative gap" (settled term), "callback-anchor" (spec term), "data baton" (spec term); no `_Avoid_` aliases used
- [x] init_project.py placeholder text at lines 204-206 matches the plan's Task 6 "find" string verbatim; dissect's CONTRACT.md (init_project.py line 170) names chapter-map.md as "接力棒" — confirms the plan's mirror claim
