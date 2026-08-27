# Plan Task-Decomposition Review — thesis-summary

**Document**: `docs/superpowers/plans/2026-08-27-thesis-summary.md`
**Reviewer**: libra
**Spec (context)**: `docs/superpowers/specs/thesis-summary.md` (aquarius round-1 "Lean. Ship." — findings A1-A4/F1-F6 dissolved; plan fidelity not re-checked)

## Status
Approved

## Decomposition check (all pass)

- **Startability**: Every task has exact file paths, complete code, runnable commands, and stated expected outputs.
  - Tasks 1–2: full verbatim Python source for both `test_check_summary.py` (14 core tests) and `check_summary.py`; red-state expected error named (ModuleNotFoundError/FileNotFoundError); every step has its command + expected string (`ALL TESTS PASS (14 tests)` / `(26 tests)`).
  - Task 3: frontmatter verbatim + nine-section body spec with per-section prescribed content pulled from spec §s, plus a complete runnable `python3 -c` verify script (needle list + P1-P9 honest-naming assertions).
  - Tasks 4–5 (prose): section-by-section content outlines keyed to spec §①–⑥/§工作流/§门与 enforcement (~120-180 line guidance) + named mirror (`thesis-intro/tests/README.md`, verified on disk). Task 5 enumerates all 26 cases individually.
  - Task 6: exact replace-with blocks + verification commands.
  - Task 7: all commands verbatim with expected outputs (`DECOUPLING-OK`, `NO-SIBLING-SCRIPT-OK`, zero-churn diff scope).
- **Boundaries**: One artifact per task. T1 gate core + failing tests / T2 cross-baton pinning tests (no production-code churn) / T3 SKILL.md / T4 references (2 prose files) / T5 tests/README / T6 the single foundation edit / T7 verification only. No grab-bag.
- **Dependencies stated**:
  - Task 2 → Task 1: explicit "green-first pinning... implementation landed in Task 1".
  - Task 3 → Tasks 1–2: "check_summary.py (Tasks 1–2) already exists for SKILL.md to reference" — explicit.
  - Task 4 → Task 3: "The load-on-demand references SKILL.md indexes (Task 3)" — explicit.
  - Task 5 → Tasks 1–2: documents the gate and enumerates its 26 cases by behavior.
  - Task 7 → Pre-flight: base-sha substitution documented twice (Pre-flight Step 0 records it; Task 7 Step 3 diffs against it, with rationale — aquarius A3).
- **Fixture consistency (Task 1 ↔ Task 2)**: no drift — Task 2's 12 appended tests reuse the same module-level constants `SUMMARY_MAP_SETTLED` / `GAP_MAP_SETTLED` / `CHAPTER_MAP_SETTLED` and `_write_project()` helper defined in Task 1; no second fixture definition exists. The Task 2 `__main__` extension lists exactly the 12 appended functions, in order.
- **Number consistency**: 14 (Task 1) + 12 (Task 2) = **26** appears consistently in File Structure, Task 2 Step 2, Task 5 body ("26 stdlib cases", 26 bullets enumerated), and Task 7 Step 1. The one exception is Task 5's **commit message** ("25 cases") — see Recommendations. Task 3 Step 2 has exactly 9 numbered honest-naming assertion groups (P1-P9), matching its claim.
- **Placeholders**: none. All code complete; no TBD/TODO. `<base-sha>` in Task 7 is a documented substitution tied to Pre-flight.
- **Referenced files exist** (verified on disk):
  - Mirrors: `sci-skills-thesis/skills/thesis-intro/{SKILL.md, scripts/check_intro.py, scripts/test_check_intro.py, references/writing-discipline.md, tests/README.md}` ✓; `sci-skills-thesis/skills/thesis-spine/SKILL.md` ✓; `sci-skills-article/skills/sci-story/SKILL.md` ✓.
  - Parent spec `docs/superpowers/specs/thesis-skill-family.md` ✓; glossary `docs/superpowers/glossary.md` ✓.
  - Target dirs do not exist yet — Task 1 Step 1 creates them via `mkdir -p` (scripts/references/tests) ✓.
  - `sci-skills/skills/thesis-init/scripts/init_project.py` + `test_init.py` exist ✓; argparse confirms `init --no-git` subcommand (L660-661) ✓.
- **Task 6 replace-text vs disk (verbatim, fixed-string)**: all three anchors match EXACTLY ONCE — 文件清单 placeholder at L267; read-list lines at L276/L277/L278. Deterministic `str.replace` targets.
- **Task 6 Step 3 sanity-check command (executed live)**:
  - Ran the exact one-liner against the current tree: clean end-to-end execution; printed count `0` with no WOVEN-OK — the correct PRE-edit outcome (placeholder names no files; registry line still present), proving the chain mechanics work.
  - Simulated POST-edit state on a properly nested copy of the patched script: `grep -c` returned **3** (≥2 as stated) and `WOVEN-OK` printed — the plan's expected post-edit output reproduces exactly, including absence of `thesis-sources.md`.
  - Step 2's premise holds: `test_init.py` passes pre-edit and contains zero assertions on contract CONTENT (no reference to summary-map/placeholder text) — the edit cannot break it.

## Recommendations (advisory, do not block)

- Task 5 Step 2's commit message says "**25 cases**"; the README being committed and all four other locations say **26**. Fix the digit when committing (one-character edit, zero risk).
- Task 6's cited range "~lines 253-274" is slightly stale at the tail: the entry starts at L253 (correct) but the second replacement block sits at L276-278, outside `sed -n '253,274p'`. Harmless — the edit anchors are verbatim quoted text, not line numbers, and the plan itself instructs verifying against disk first — but `sed -n '250,282p'` would cover the whole entry.
- Transient forward reference (same shape as the dissect-plan note): Task 3's SKILL.md indexes `references/writing-discipline.md` + `references/synthesis-guide.md`, which don't exist until Task 4. Visible from task order; a one-liner would remove all doubt. Task 3's own verify script deliberately doesn't probe for them, so nothing fails in between.
- Implementation detail worth knowing (not a plan change): `init_project.py` resolves `REPO_TEMPLATES_DIR` from `__file__`'s four-level repo nesting at import time — so Task 6 Step 3 must invoke the script via its canonical repo path (as the plan correctly does), never a copied-out instance.
