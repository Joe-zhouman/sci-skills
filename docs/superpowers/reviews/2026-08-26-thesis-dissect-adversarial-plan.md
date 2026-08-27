# Existence Audit — thesis-dissect plan (2026-08-26)

**Target:** `docs/superpowers/plans/2026-08-26-thesis-dissect.md`
**Authority:** `docs/superpowers/specs/thesis-dissect.md` (aquarius round-2, user-approved)
**Lens:** design (plan executing an approved spec)
**Date:** 2026-08-26

---

## Verdict

**net: -4 lines deletable.**

Not "Lean. Ship." The plan faithfully executes the approved spec on every load-bearing axis the orchestrator named (verified below), but Task 1's check_dissect.py has one real hole: the progression-in/out coverage gate reimplements `_is_empty` inline and drops the empty-string case the spec requires gated.

---

## Findings

Task 1 Step 3, check_dissect.py progression-in + progression-out blocks: shrink: inline `pi is None / elif pi in _NONE_TOKENS` (5 lines × 2 fields) reimplements `_is_empty` (defined 30 lines above, already used by framework-instantiation in the same loop). The inline version drops the empty-string case — `progression-in:` or `progression-in:   ` (blank/whitespace value) passes coverage for non-ch1, but spec §门与 enforcement requires `progression-in（ch1 除外）非空` / `progression-out（末章除外）非空`. Verified: `_is_empty("")` → True (correctly fails); the inline `elif "".strip().lower() in _NONE_TOKENS` → False (passes, bug). Replacement: `if _is_empty(pi): issues.append(...)` — 3 lines/field, consistent with the framework-instantiation check 4 lines above, closes the gap.

---

## What was verified (no findings — recorded because the orchestrator asked)

1. **拆即写 in the plan (spec §①, load-bearing).** check_dissect.py (Tasks 1–2) gates chapter-map.md fields + tex-file existence only — no module-map.md anywhere, no pre-write-outline check. SKILL.md (Task 3) body instructions state "dissection IS writing… no pre-write module-map outline" + pervasive discipline "no pre-write outline" + references (Task 4) "it is NOT a pre-write outline (no module-map)". Task 3 Step 2's grep assertion (`'module-map.md' not in body or 'no pre-write' in body.lower() or …`) is load-bearing-correct as a prose grep proxy — it matches the exact negation phrases Task 3 tells the author to write. No regression to outline-then-fill.

2. **check_dissect.py coverage-only (spec §门).** The script checks exactly the 5 spec-mandated coverage fields (framework-instantiation non-empty + progression-in ch1-excepted + progression-out last-excepted + status=written + tex-file exists in thesis/tex/) and nothing depth-like — no restructure-quality, no claim-grounding, no binding judgment. Matches spec §门 "depth 不在此层" + §测试验收 "只查 coverage".

3. **ch1 / last-chapter progression exceptions.** Logic is correct: `ch_num = idx+1`, `total = len(chapters)`; progression-in skipped when `ch_num > 1` is False (ch1); progression-out skipped when `ch_num < total` is False (last). Single-chapter case (total=1) correctly skips both (ch1 is also last). Tests test_ch1_progression_in_none_ok + test_last_chapter_progression_out_none_ok assert the exceptions hold; test_fails_on_non_ch1_missing_progression_in + test_fails_on_non_last_missing_progression_out assert non-ch1/non-last `none` fails. No off-by-one. (Naming nit: the two "fails on … missing" tests actually set `none`, not a missing field — untested branch, but that's completeness, not existence.)

4. **Two-arg design (vs spine's one-arg).** Sound. Spine's check_spine.py takes one arg because it gates one baton file's own fields. Dissect's gate spans two locations: `sci-skills/thesis-dissect/chapter-map.md` (the baton) + `thesis/tex/<chN.tex>` (the produced prose). Two args is the minimum to express that. Defaults are cwd-relative (`Path("sci-skills")/"thesis-dissect"/"chapter-map.md"` + `Path("thesis")/"tex"`) matching how the skill runs from project root — mirrors spine's default pattern exactly. Not a shrink candidate; the two locations are not derivable from one another without assuming the project root.

5. **YAGNI / decision ladder.** Every task maps to a spec acceptance criterion (Task 1→§门 Coverage + §测试验收; Task 2→§门 tex-file; Task 3→§工作流 + §Implementation Notes; Task 4→§⑥; Task 5→§⑧; Task 6→§防带病推进 decoupling grep + §"无 init/spine 变更"). No task adds scope the spec doesn't require. The decision-ladder outcomes section, Pre-flight branch, and Task 6 E2E are plan-format scaffolding (superpowers convention), not scope-creep.

6. **Zero churn to foundation + spine.** No task writes under `sci-skills/skills/thesis-init/` or `sci-skills-thesis/skills/thesis-spine/`. Task 6 Step 4 enforces this with `git diff --name-only <BASE>..HEAD -- sci-skills/skills/thesis-init/ sci-skills-thesis/skills/thesis-spine/`. Both target dirs verified to exist (so the check is real, not a no-op on a typo'd path).

7. **Completeness for a fresh implementer.** Exact paths, real code (full check_dissect.py + 14 tests inline), expected outputs ("14 `: PASS` lines then `ALL TESTS PASS`"). All mirror references verified to exist on disk: sci-write SKILL.md + section-templates.md, spine SKILL.md + check_spine.py + test_check_spine.py + tests/README.md + references/, all three specs. SETTLED fixture traced against check_dissect.py by hand — passes (2 chapters, ch1 progression-in=none skipped, ch2 progression-out=none skipped, both tex files exist, both status=written). The one `<project>` placeholder in Task 3 Step 2 is self-explanatory and the no-arg default makes it unnecessary. The tests/README.md "TODO — scaffold evals.json" is an honestly-named out-of-scope follow-up (spec §⑧ defers prose eval), not a plan gap.

---

## Round 2 — re-audit (2026-08-26)

**Verdict: Lean. Ship.**

Round-1 sole finding (Task 1 Step 3 progression-in/out inline check dropping the empty-string case) is closed. The blocks now call `_is_empty(pi)` / `_is_empty(po)`, consistent with the framework-instantiation check 4 lines above.

Verified:
1. `_is_empty("")` → True; `_is_empty("   ")` → True (v="" via strip). Blank `progression-in: ` / `progression-in:   ` now fails for non-ch1/non-last. Bug closed.
2. ch1 / last exceptions intact: `if ch_num > 1` / `if ch_num < total` gate the whole block, so `_is_empty` is never called for excepted cases — ch1 progression-in=none and last progression-out=none still pass.
3. The four progression tests trace clean: test_ch1_progression_in_none_ok + test_last_chapter_progression_out_none_ok (skip → no issue); test_fails_on_non_ch1_missing_progression_in + test_fails_on_non_last_missing_progression_out (`_is_empty("none")` → True → issue). The unified call does not break the none-fails tests — it's the mechanism that satisfies them.
4. No new load-bearing issue. Inline comment on the `_is_empty` call (lines 323-324) is regression-prevention context, not bloat. All 14 tests hand-traced against the settled fixture + mutations → pass.

net: 0. The round-1 shrink finding is resolved; nothing else deletable.
