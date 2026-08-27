# Code Quality Review — thesis-dissect (branch `thesis-dissect`, `364985c..f36be85`)

Scope: `check_dissect.py` + `test_check_dissect.py` + `SKILL.md` + `references/restructure-discipline.md` + `tests/README.md`. Spine sibling (`check_spine.py` / `test_check_spine.py`) read for consistency. scorpio confirmed spec compliance (0 issues) — this review judges how the code is built.

All 14 stdlib tests pass (`python3 test_check_dissect.py` → ALL TESTS PASS, exit 0).

## Strengths

- **`check_dissect.py:61-62` — `check()` returns an issues list, never raises.** Documented contract ("不抛异常——问题进列表"). File-missing (`:64-65`), UTF-8 decode (`:68-69`), and `OSError` (`:70-71`) all handled separately with actionable messages. Mirrors `check_spine.py:56-66`.
- **`check_dissect.py:26-42` — `split_chapters` returns an ordered `list[tuple]`, not a `dict` like spine's `split_sections` (`check_spine.py:29-45`).** Justified divergence: chapter order is load-bearing for the ch1/last-chapter exemption logic (`:87`, `:93`), which section-name lookups don't need. The right data structure for the right job.
- **`check_dissect.py:53-58` — `_is_empty` + `_NONE_TOKENS` correctly carve out the ch1/last-chapter `none` exemption.** Tests `test_ch1_progression_in_none_ok` (`test:66-72`) and `test_last_chapter_progression_out_none_ok` (`test:83-89`) prove this load-bearing behavior. Without these, `none` on ch1/last would false-fail.
- **`check_dissect.py:85-86` — comment explains a non-obvious decision** ("用 _is_empty（统一处理 None/空/none-token），不内联 — 内联版会漏空白值"). Prevents a future reader from "simplifying" to an inline check that would let `"progression-in:   "` (whitespace-only) pass. Exactly the kind of comment that earns its keep.
- **`check_dissect.py:32` — `^##\s+(Chapter\s+\d+)\s*$` correctly rejects `###` subsections** (verified: `### Subsection` is absorbed into the chapter body, not mistaken for a chapter boundary). The `\s+` after `##` is what guards it.
- **`check_dissect.py:48` — `_field_value` uses `re.escape(field)` + `re.MULTILINE`**, robust to extra whitespace (`-   framework-instantiation:    x` → `'x'`) and case (`Framework-Instantiation` matches via `re.IGNORECASE`). Verified.
- **Tests test behavior, not implementation.** All 14 call the public `check(cm, tex_dir)` and assert on returned issues — no poking at `split_chapters` / `_field_value` directly. The `SETTLED.replace(...)` fixture-mutation pattern is safe: a broken replace target produces a loud assertion failure, not a silent no-op.
- **Terminology is consistent with `docs/superpowers/glossary.md`.** 拆即写 (glossary:78-80), `outline-then-fill` `_Avoid_` (glossary:80), compass file (glossary:74-76), read-neighbors-don't-orchestrate (glossary:41-43), contract gap (glossary:45-47), real-DOI placeholder (glossary:49-51), serves-the-author-first (glossary:90-92) — all used verbatim, no invented aliases.
- **`references/restructure-discipline.md:53,70,110` — explicitly disowns `module-map.md` as the anti-pattern**, consistent with the glossary's `_Avoid_: outline-then-fill`. Three separate passes reinforce the discipline without contradiction.

## Issues

### Critical (Must Fix)
None.

### Important (Should Fix)

1. **`check_dissect.py:32` — `split_chapters` regex silently rejects chapter headers with trailing title text.** The pattern `^##\s+(Chapter\s+\d+)\s*$` requires the line to END after the digits. A header like `## Chapter 1 (绪论)` or `## Chapter 1 — 绪论` produces zero chapters → the gate returns `"✗ chapter-map.md 无 `## Chapter N` 条目"` (`:75`) even though chapters are visibly present. The glossary itself annotates chapters ("Ch1 绪论 / Ch2 共用理论方法"), making trailing title text a natural authoring pattern in this domain. The failure is total and the message is confusing (author sees chapters; gate says none). The schema in `SKILL.md:137-148` does show bare `## Chapter 1`, so the code is consistent with the documented contract — but the cliff is one trailing word away. → Either widen to `^##\s+(Chapter\s+\d+)\b.*$` (capture the label, ignore any trailing title) or sharpen the error to name the deviation ("found `## Chapter 1 (绪论)` — schema requires bare `## Chapter N`").

2. **`test_check_dissect.py` (whole file) — no test exercises the `except OSError` handler at `check_dissect.py:70-71`.** The spine sibling has `test_graceful_on_unreadable_file` (`test_check_spine.py:122-139`, chmod-000 with root-skip guard) for the identical handler. The handler was mirrored but its test wasn't ported. → Add the chmod-000 test mirroring `test_check_spine.py:122-139` (including the `os.geteuid() == 0` skip and the `finally: os.chmod(p, 0o644)` restore).

### Minor (Nice to Have)

1. **`test_check_dissect.py` — no test for `main()` exit-code contract.** `tests/README.md:7` documents "Exit-code contract: 0 = coverage through; 1 = coverage issues," but no test calls `main(argv)` and asserts the return value. `main()` is load-bearing for CI/eval integration. A two-line test (`assert main([cm]) == 0` on settled, `== 1` on broken) would close the gap.

2. **`test_check_dissect.py:62` — `"empt" in i.lower()` is a dead assertion branch.** Issue messages use Chinese "空" (`check_dissect.py:83`), never "empty"/"empt" in English. The `"empt"` check can never fire. Harmless over-broad assertion, but misleading to a reader trying to understand what the test verifies.

3. **`check_dissect.py:23` — `_NONE_TOKENS` includes em-dash `—` but not hyphen `-` or en-dash `–`.** An author writing `progression-in: -` as a placeholder gets a non-empty pass. Low risk (schema uses `none`), but the set is slightly inconsistent across dash variants.

4. **`SKILL.md:58-119` — "Layout & boundaries" (directory tree + table at `:78-89` + bullets at `:91-104`) and "File contracts" (table at `:108-119`) enumerate the same files twice.** Three passes over the same producer/reader/role list. Could consolidate to one table + the tree; the detail bullets could move under the table they elaborate.

5. **`tests/README.md:42-52` — section 3 "decoupling assertions (programmatic)" describes grep checks that aren't implemented as runnable code.** No `evals.json` exists yet (TODO at `:53`). The "(programmatic)" label oversells what's on disk vs. what's described. Either implement the grep checks as a tiny script or re-label as "(intended, pending evals.json)".

## Recommendations

- The `split_chapters` regex (Important #1) is the only item I'd fix before the eval loop — it's a one-line change that closes a total-failure mode on a domain-natural input. The OSError test (Important #2) is a quick port from the sibling. Both are under 15 minutes of work.
- The gate trusts appearance order over label numbers (`idx`-based, `:78`): if the AI ever emits chapters out of numeric order, ch1/last exemptions apply to the wrong chapters. This is a producer-contract issue (the schema says ordered), not a gate bug, but worth a one-line comment at `:77-79` noting the appearance-order assumption so a future maintainer doesn't "fix" it to parse label numbers.

## Assessment

**Verdict**: PASS

**Reasoning**: Solid implementation — correct coverage logic with no off-by-ones (verified single-chapter and multi-chapter cases), robust error handling that never raises, tests that verify behavior rather than internals, and justified divergences from the spine sibling (ordered list for chapter semantics, `_is_empty` for none-token handling). Terminology is consistent with the glossary; no invented terms. The two Important issues are a regex robustness cliff and a missing ported test — both fixable without restructuring, neither a correctness bug for spec-compliant input. No Critical issues, no swallowed errors, no duplication, no file-size concerns.
