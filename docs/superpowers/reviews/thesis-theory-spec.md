# Spec Compliance Review — thesis-theory

**Reviewed**: BASE ab5a893 → HEAD 53130bb (branch `thesis-theory`)
**Spec**: `docs/superpowers/specs/thesis-theory.md` (+ lineage: `reviews/thesis-theory-adversarial-plan.md` T1-T6, `reviews/thesis-theory-plan-adversarial.md` A1-A4)
**Plan**: `docs/superpowers/plans/2026-08-27-thesis-theory.md`
**Reviewer**: scorpio
**Method**: read spec + lineage in full; read every shipped artifact (`check_theory.py`, `test_check_theory.py`, `SKILL.md`, references ×2, `tests/README.md`, init diff); ran the 35-test suite, init tests, the plan's P1-P10 assertion script, the decoupling greps, the zero-churn assertion, and a woven-CONTRACT sanity init; AST-diffed the shipped check against `check_summary.py`; programmatically diffed the plan's 15 embedded code/text blocks against the shipped files and the spec schema against SKILL.md.

## Verdict
✅ **Spec compliant.** 0 missing, 0 extra, 0 misunderstood. All three as-executed deviations verified acceptable (each was mandatory for correctness, each plan-sync-backed). One cosmetic plan↔shipped line difference (functionally equivalent, noted below).

## Acceptance rows — verified against code/tests, not the report

| Row | Evidence (read, not trusted) |
|---|---|
| ① Shared not AI-destroyable | pending interception `check_theory.py:215-219` (status≠confirmed → issue) pinned by `test_check_theory.py:217-223`; grounded-in ≥2 distinct `check_theory.py:209-211` + test 225-234; dangling chapters `check_theory.py:212-214` + test 236-244; SKILL.md spine protocol (pending + tension-flags + author settle, never auto-adopt) `SKILL.md:60-70,277-300` |
| ② Overlaps managed | shared-ref `check_theory.py:230-238` + chapter-ref `:239-247`, pinned by tests 328-357; surface checklist at handoff `SKILL.md:353-356`; coverage completeness explicitly NOT mechanical — `check_theory.py:252` comment, docstring `:14-15`, `tests/README.md:186-190`, no count-matching code anywhere (T5真落地) |
| ③ Writing chain closes | theory-tex field + file-exists + abs/`..` path guard `check_theory.py:254-270`, tests 295-326 |
| ④ fallback on-disk terminal | waived legal terminal: outcome==waived skips per-field checks `check_theory.py:198,227`; waived-with-entries contradiction `:198-199,227-228` (tests 183-198); confirmed-vacuous guard `:221-223` (test 155-181); waived-terminal pass test 133-139. Backtrack fork leaves pending residue → check honestly fails (non-terminal) — consistent with spec §Step 1 |
| ⑤ spine re-verification | `check_theory.py:172-182` (missing/unreadable/`[pending?` residue → issues), tests 392-418; marker `[pending?` mirrors `check_spine.py:22-24` (aries #3 question-mark form); theory-map itself uses status field only — `PENDING_MARKER` never grepped against tm text (F3 discipline held) |
| ⑥ honest naming | check docstring `check_theory.py:2-16`; SKILL.md P1-P10 all pass (re-ran the plan's assertion script verbatim — `ALL P1-P10 PASS`); `tests/README.md` §2 + known limitation 178-190 |
| ⑦ zero churn + sole foundation edit | `git diff --name-only ab5a893..53130bb` = 13 files, **13/13 whitelisted** (6 docs session records + 6 thesis-theory new + 1 init_project.py); sibling dirs (spine/dissect/intro/summary) = 0 changed files; dissect CONTRACT reader line (`init_project.py:188`) untouched — T2 ripple booked-not-fixed, verified |
| ⑧ no skill calls skill | py-import grep DECOUPLING-OK; SKILL.md no sibling check script (NO-SIBLING-SCRIPT-OK); Step 0 does its own read-checks `SKILL.md:255-265`; the `check_summary.py`/`check_spine.py` strings in tests/README:166-167 are self-describing documentation of the grep's own exceptions, not invocations |

## Review lineage — T1-T6 / A1-A4 genuinely landed (not name-dropped)

- **T1** (4th arg dead surface): spine re-verify is real code + 3 dedicated tests + SKILL.md:336-340 names the duty. Landed.
- **T2** (bookkeeping symmetry): spec §偏离 carries the chapter-map-widening entry (spec:243); dissect ripple booked (plan:45) and confirmed untouched on disk. Landed.
- **T3** (fallback terminal): `extraction-outcome` confirmed/waived machinery + 5 tests (terminal pass, missing, invalid, confirmed-vacuous, waived-with-entries). Landed.
- **T4** (false "不交叉"): spec:76 rewritten to the true proposition; SKILL.md:37-40 uses "no file dependency on intro/summary products" — the false premise did not migrate. Landed.
- **T5** (coverage completeness not mechanical): four locations name it; no such check exists in code. Landed.
- **T6** (test path): test lives at `scripts/test_check_theory.py`; `tests/` holds only README.md. Landed.
- **A1**: docstring whitelist is in the plan (plan:83); AST-diff confirms the 4 swapped helpers differ from `check_summary.py` **docstrings only** — bodies byte-equivalent after docstring strip (verified function-by-function: `_field_value`, `_header_numbers`, `_single_ref_number`, `_top_level_field`; the other 4 helpers + 3 regex constants fully identical).
- **A2**: BOM fixture is `[Chapter 1 §2, Chapter 9 §3]` — two chapters, one dangling; the dangling branch genuinely fires (test docstring 264-268 states the rationale). Landed.
- **A3**: init-edit commit dd7eb54's full message (via `git cat-file`) names all three stale lines (registry-read / dissect-reader / 小论文→正文章). Landed.
- **A4**: plan:440 RED-expectation corrected (no phantom extraction-outcome messages). Landed (plan-text level; no implementation surface).

## Confirmed correct (verified by reading/running)

- **35/35 tests pass** (`python3 test_check_theory.py` → `ALL TESTS PASS`, RC=0). The spec's 测试验收 fail-list maps case-for-case onto the 35 tests — all 23+ fail cases + both pass cases present; I traced each.
- **Hardening genuinely inherited**: utf-8-sig BOM (`:148,165,177`), heading/hr scope terminator (`:46`, `_split_sections`), fence-aware splitting + orphan-fence diagnostic (`:87-92,156-157`), stat fallback `(OSError, ValueError)` (`:264-268`), ANSI sanitize (`_sanitize` on every echoed value), tmpdir atexit (test:20-26). Family fossil discipline held — `check_intro.py` etc. untouched.
- **SKILL.md**: all 9 plan-mandated sections present, nothing extra; frontmatter has NO `allowed-tools`; the embedded theory-map.md schema is **byte-identical** to spec §Implementation Notes (programmatic diff); tex→Read / PDF→`mcp__extract__analyze_doc` rule present (`:270-271`); untrusted guard covers all five read surfaces **including theory-map.md itself** (B7) + tez-atif-dogrulama rule #7 (`:401-427`); read cut (no registry/small papers/intro/summary products) holds in Layout, File contracts, and Step 0 — I checked each list.
- **references ×2**: writing-discipline.md = the 6 dictated protocol sections; theory-guide.md = the 6 dictated craft sections (incl. waived minimal-chapter mode + template-derived naming + "ask the author, don't guess"). No content beyond the dictated scope.
- **tests/README.md**: 4-section shape; all 35 cases individually listed and accurate vs the on-disk test functions; T5/known-limitation honesty present; the `TODO: scaffold evals.json` line mirrors summary/spine practice (precedent on disk at both siblings' tests/README) — not extra.
- **init edit** = exactly the 4 sub-edits (文件清单/读清单/谁读它/有什么用), replacement texts verbatim per plan blocks 8/10/12/14; `test_init.py` RC=0 (14 PASS); woven-CONTRACT sanity in temp dir: theory-map + chapter-map present, registry line gone, stale dissect-reader line gone.
- **Glossary**: new **Overlap 清单** term (+4 lines, allowed session record) matches spec §③ verbatim; `_Avoid_` aliases ("overlap resolution gate"/"dedup list") used nowhere in the skill — only hit is SKILL.md:84 quoting the avoid list itself.
- **No summary remnants in CODE**: the only "summary" tokens in check_theory.py are lineage citations (F6/F3 lessons) at `:16,35` — legitimate attribution, not artifacts.

## As-executed deviations — assessed

1. **Task 1 fixture: bytes-literal non-ASCII → `.encode("utf-8")`** (test:272-275): the dictated `b"...§..."` is a Python **SyntaxError** (non-ASCII in bytes literal) — the fix was mandatory for the file to parse. Plan sync-backed (plan:361-363). **Acceptable — required.**
2. **Task 1 fixture: no-op replace corrected** (test:296-299): dictated pattern `"theory-tex: chapter1.tex\n\n## Shared 1"` never matched (extraction-outcome sits between) → the field line itself is removed instead. Without the fix the test could never exercise its red path honestly. Plan sync-backed (plan:384 shows the fixed pattern). **Acceptable — required.**
3. **Task 2 fixture: NUL-byte → overlong-name** (test:504-519): on Python 3.13 pathlib's `is_file()` swallows the NUL ValueError internally (returns False), so a NUL value produces the "不存在" branch, never the stat fallback — the dictated test would pin nothing. Overlong name genuinely raises OSError; mirrors summary's `test_graceful_on_overlong_synthesis_tex` (verified present in summary's test file at :576). Plan sync-backed (plan:842-855). **Acceptable — required.**
4. **Helper docstring token swaps**: verified AST-level docstring-only (see A1 above). **Acceptable — whitelisted by plan:83.**

**Cosmetic note (no action)**: plan:363 vs shipped test:275 differ in surface (`"...".encode("utf-8")` vs `b"..."`) — the shipped form uses a plain bytes literal for the pure-ASCII tail, equivalent bytes. The plan sync-back is thus one cosmetic line off from shipped; functionally identical, zero behavioral surface.

## Missing
None. Every spec §⑥ check item, workflow step, gate, boundary, and acceptance row traced to code or prose at file:line.

## Extra (unrequested)
None. The diff contains exactly: 6 new skill files + 1 init placeholder completion + 7 session records (spec/plan/3 reviews/glossary — all in the allowed docs set). No sibling-skill edits, no bonus hardening, no scope creep.

## Misunderstood
None. The two-act protocol, the resolver-is-author overlap contract, the read cut, the waived terminal, and the near-trivial/write-time honesty all match the spec's semantics as written.
