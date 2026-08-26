# Existence Audit — thesis-intro plan

> 审查日期：2026-08-27 | lens: design (aquarius)
> target: `docs/superpowers/plans/2026-08-27-thesis-intro.md`
> authority: `docs/superpowers/specs/thesis-intro.md` (settled — aquarius round-1 6 findings absorbed with honest residual naming)
> bar: do the 6 honest-naming premises survive the implementation details? + existence (ceremony / dead code / overclaim / causal gap)

**net: -9 lines deletable + 4 shrink fixes** | not Lean — 6 premises faithfully inherited on the explicit surface (no blatant regression), but the implementation details leak: one reference doc sneaks back chapter-coverage framing, the docstring contradicts its own honest-naming in-paragraph, the cross-ref parser has an aries #2 hole, test 15 is redundant, and the assertion block covers only 4 of 6 premises.

---

## Premise inheritance — faithful on the explicit surface

All 6 round-1 premises are faithfully inherited in the plan's explicit constraints (Architecture L7, Decision-ladder L34, Load-bearing constraints L41-48, docstring L291-307, SKILL.md body L612-618, tests/README L762-770, Execution context L958-961). No sneak-back of "genuinely new value" / "framing vs coverage" / "B3 clean split" / "narrative craft enforcement" / "coherence lock" / "anchor-in-intro enforced" in those sections. The plan is honest on the load-bearing surface.

The findings below are in the IMPLEMENTATION DETAILS — reference doc, test fixture, parser, assertion block — where the honest-naming is weaker or the code contradicts the prose.

## Tagged findings

**L296 (check_intro.py docstring): shrink:** the docstring says "这是 near-trivial consistency 门，**非 coverage gate**" then two lines later refers to "非本 **coverage 门**" — internal contradiction. The docstring is where the honest-naming invariant LIVES (shipped code, read by aries/scorpio); it violates its own assertion in the same paragraph. Fix: "非本 consistency 门" or "非 check_intro.py 的 near-trivial consistency." The honest-naming is load-bearing; the slip undercuts it at the source.

**L503-508 (test_passes_when_all_filled_by_resolve): delete:** redundant with test 1 (test_passes_on_settled L161-165). Same fixture (GAP_MAP_SETTLED + CHAPTER_MAP_SETTLED); test 1 asserts `issues == []` (strictly stronger — no issues at all), test 15 asserts `not any("filled-by" in i and "不在" in i)` (weaker subset — only no cross-ref issues). If test 1 passes, test 15 trivially passes. 14 tests, not 15. Update the 3 count claims (L568, L862, L939 all say "15").

**L143 + L156-157 (_write_project `ch_tex_files` parameter + default `{"ch1.tex": "x", "ch2.tex": "x"}`): yagni:** check_intro.py only verifies `ch0-intro.tex` (L419-421); the chN.tex files are decorative — no check inspects them, no test customizes `ch_tex_files`. Simplify: drop the parameter + the `for name, body in ...` loop, create only ch0-intro.tex. The sibling files are fixture-realism cargo.

**L736 (introduction-guide.md §5 "every chapter fills at least one gap; must collectively cover"): shrink:** overclaims the spec's "typically one per body chapter" (spec L49 — a ~1:1 tendency) into an unenforced chapter→gap coverage *requirement*. check_intro.py checks gap→chapter (each gap has a filled-by), NOT chapter→gap (each chapter fills a gap). Stating "must" for an unchecked direction sneaks back the "coverage gate" framing round-1 rejected — spec §①: "非 spine/dissect 那种 'required 结构元素在不在' 的 coverage 门." "Every chapter fills at least one gap" IS "required structural element presence" (chapter→gap), the exact coverage-type the spec disclaimed. Reframe as narrative goal ("a chapter with no gap is unmotivated — author should address at the gate"), not enforced "must."

**L364-366 (`_chapter_numbers_in`): shrink:** lacks the `in_fence` toggle that `split_gaps` has (L327-334 — the aries #2 fix the plan explicitly claims to mirror at L323 "跳过 ``` 代码块内的标题（mirror check_dissect aries #2）"). A `## Chapter 99` inside a code block in chapter-map.md → included in the valid set → a gap's `filled-by: Chapter 99` passes cross-ref → false positive in the very check that catches fabrication. Two parsing functions for chapter-map.md (dissect's `split_chapters` with `in_fence` vs intro's `_chapter_numbers_in` without) is inconsistent + has a hole. Extract a shared `_split_headers(text, pattern)` helper with `in_fence` (DRY, ~same lines, one fix point), or add the `in_fence` toggle. Note: dissect ships `test_ignores_chapter_headers_inside_code_fence` for its parser; intro drops both the fix and the test for the chapter-map direction.

**L644-664 (Task 3 Step 2 assertion block): shrink:** claims to "verify key invariants incl. honest-naming assertions" but covers only 4 of 6 premises. Missing premise 4 (B3 gray-zone) — the `'heuristic'` needle (L652) is too generic; a regression that drops gray-zone framing but keeps "heuristic" anywhere passes. Missing premise 6 (anchor-in-intro optional) — not asserted at all; a regression re-enforcing it isn't caught. Assertion 8 (L662) has weak `or` logic: `'pre-write gap-map' not in body.lower() or 'NOT a pre-write' in body` passes if the qualification exists *anywhere*, even if "pre-write gap-map" coexists unqualified elsewhere — should be `and`-style or assert the bad phrase absent. Tighten: assert all 6 premises with correct logic, or shrink the claim that the block verifies honest-naming.

## Holds (vote-of-confidence)

- **6 premises inherited** on the explicit surface — no blatant regression. The user's primary concern is met; the leaks are in implementation details.
- **Task 6 (init placeholder)**: 3 section edits (文件清单 + 这个文件夹是什么 + 谁读它) — exceeds spec's "~1-string edit" wording (spec L209) but is the *minimum* faithful mirror of dissect's CONTRACT.md (which names chapter-map.md in all 3 sections: 文件夹是什么 L197, 文件清单 L201, 谁读它 L211). Not over-reach; the spec's "~1-string" was an under-estimate, the plan corrects it toward the stated mirror intent. (Minor: L817 "may add thesis-summary" is too conditional — dissect definitively lists it; mirror should too. Wording, not existence.)
- **7 tasks well-decomposed**: no grab-bag, no missing task, no task needing a split. Task 1+2 (core vs cross-ref, 2 TDD passes with a commit between) is reasonable, not over-split.
- **Cross-ref check (#3) earns existence**: catches AI fabrication of chapter numbers (real LLM failure mode), cheap (set lookup), honestly named near-trivial consistency (not "genuinely new value" — spec §⑥ round-2). Not ceremony.
- **3 references** (writing-discipline + literature-search + introduction-guide): distinct topics, load-on-demand, mirror sci-story's structure. Not duplicates of each other or of SKILL.md (SKILL.md summarizes; references elaborate).
- **Task 7 zero-churn + decoupling grep**: real family invariants ("read neighbors, don't orchestrate"), cheap. Not ceremony.
- **test 15 redundancy** aside, the 14 behavioral tests verify the check's catch/pass surface correctly; honest-naming prose claims are correctly split to docstring + SKILL.md + tests/README (not testable by assert).

## Score rationale

Not "Lean. Ship." The plan faithfully inherits the 6 honest-naming premises on the explicit surface (the user's primary concern) — no sneak-back of round-1 overclaims in the constraints, docstring intent, SKILL.md body, or tests/README. But the implementation details have 6 findings: the docstring contradicts its own honest-naming in-paragraph (L296), test 15 is redundant with test 1 (L503), the test fixture carries decorative chN.tex files no check reads (L143), the introduction-guide sneaks back chapter-coverage framing as an unenforced "must" (L736), `_chapter_numbers_in` has the aries #2 hole that `split_gaps` explicitly mirrors the fix for (L364), and the assertion block that claims to verify honest-naming covers only 4 of 6 premises with one weak `or` (L644). ~9 lines deletable (test 15 ~6 + ch_tex_files ~3) + 4 shrink fixes (docstring wording, intro-guide reframe, `_chapter_numbers_in` in_fence, assertion block tighten). None negate the plan's existence — fix and ship.
