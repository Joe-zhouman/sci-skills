## Code Quality Review — thesis-theory (BASE ab5a893..HEAD 53130bb)

Scope reviewed: `sci-skills-thesis/skills/thesis-theory/` in full (SKILL.md 427L, scripts/check_theory.py 290L, scripts/test_check_theory.py 557L/35 cases, references/theory-guide.md 159L, references/writing-discipline.md 179L, tests/README.md 193L) + `sci-skills/skills/thesis-init/scripts/init_project.py` placeholder-completion edit (hunk @231-256). Session-record docs excluded per scope. All 35 tests run green (`python3 scripts/test_check_theory.py` → ALL TESTS PASS, exit 0).

Copy-lineage noted up front: helpers `_split_sections`/`_fences_balanced`/`_field_value`/`_top_level_field`/`_is_empty`/`_header_numbers`/`_single_ref_number`/`_sanitize` are AST-identical to shipped `check_summary.py` (scorpio already verified); this review judges the theory-specific delta (`check_theory.py:184-271`, the whole test file, and the prose artifacts) plus anything the copy propagates.

### Strengths

1. **The honest-boundary statement is consistent across four surfaces** — module docstring (`check_theory.py:2-16`), SKILL.md rule 6 (`SKILL.md:107-119`), writing-discipline §6 (`references/writing-discipline.md:160-179`), tests/README §2 (`tests/README.md:115-134`). Each states what the gate catches (缺席 + 官僚 lapse) AND what it cannot (forced/trivial sharing, fabricated §, coverage completeness) without drifting into overclaim. This is the family's central anti-pattern defense done properly, not boilerplate.
2. **Glossary discipline is exact.** Overlap 清单 semantics follow the glossary entry verbatim: resolver-is-author, no downstream enforcement, disposition optional-audit-trail — enforced in code (`check_theory.py:251-252` declines to check resolution), and the glossary's `_Avoid_` aliases ("overlap resolution gate", "dedup list") are cited as avoided rather than used (`SKILL.md:83-85`).
3. **Tiered degradation is coherent.** Primary-file failure returns early (`check_theory.py:145-152`); dependency files (chapter-map, spine) degrade to explicit `"…跳过"` diagnostics instead of silent skips (`check_theory.py:160-170`, `173-182`) — and each degraded mode has its own pinning test (`test_check_theory.py:369-383`, `401-407`). Every `read_text`/stat call is exception-wrapped; nothing can raise out of `check()` (proven empirically below, probe E).
4. **Path guard is correctly tiered** — absolute/`..` rejection before stat (`check_theory.py:259-263`), OSError/ValueError stat-fallback (`:264-268`), existence check last (`:269-270`). And the test for it is honest about its own fixture history: `test_bad_theory_tex_value_graceful` (`test_check_theory.py:504-519`) documents WHY the NUL-byte fixture pinned nothing on Python 3.13 (pathlib swallows ValueError → returns False) and swaps to an overlong name that actually reaches the fallback branch. A vacuous test was repaired instead of shipped — that is the exact integrity this checkpoint exists for.
5. **Test discrimination is above family average.** Three independent angles on the scope-terminator rule: fenced-Shared-must-not-count (`test_check_theory.py:420-444` — discriminative: with fence handling removed, the vacuous guard stops firing AND the dangling-ref guard is skipped on empty `shared_nums`, so the assertion genuinely fails), hr-closes-window (`:446-460`), foreign-block-no-substitute (`:462-480`). The BOM test engineers its fixture so the *dangling* branch fires rather than the <2 floor short-circuiting, with the reasoning written down (`:264-286`). The ANSI test is two-stage — first proves the grounded-in issue fired, then asserts no `\x1b` anywhere (`:500-501`) — so it cannot pass vacuously.
6. **Foundation edit is consistent with sibling contracts.** The `SKILL_DIR_CONTRACTS["thesis-theory"]` completion (`init_project.py:237-256`) uses the same relative-path convention as every sibling entry (`../../thesis/template-spec.md` @ init_project.py:171, 179, 209, 213, 243, 279), names exactly the fields the gate reads (`extraction-outcome` / Shared / Overlap / `theory-tex`), states resolver-is-author, and lists readers (`init_project.py:251-253`) matching SKILL.md's layout tree (`SKILL.md:141-142`) and the 信息流单向收敛 cut. No drift introduced.

### Issues

#### Critical (Must Fix)
None. No logic error visible in the shipped code path; every field/ref combination I probed produces the documented verdict (see probes under Important 1 and Minor 1).

#### Important (Should Fix)

1. **`check_theory.py:226-228` — the Overlap-under-waived branch is load-bearing but has ZERO test coverage, and the load is real.** The 35-case dictated set (plan Task 5, `docs/superpowers/plans/2026-08-27-thesis-theory.md:1073-1080`) covers waived+Shared but never waived+Overlap. Mutation simulation (branch deleted, same fixture):
   - shipped code: `✗ Overlap 1 存在于 waived-by-author 终态（waived = Shared/Overlap 段须空）` — correct;
   - branch deleted: **zero issues, exit 0**. A waived map carrying Overlap entries passes silently, because the dangling-shared-ref guard is skipped on empty `shared_nums` (`check_theory.py:237`: `elif shared_nums and n not in shared_nums`) and the vacuous-pass guard only arms under `OUTCOME_CONFIRMED` (`:222`).
   That is a silent pass, not just a coarser diagnostic — the exact class the family hardened against (summary aries / taurus I2 no-silent-skip lineage). Fix: add one test mirroring `test_fails_on_waived_with_shared_entries` (`test_check_theory.py:183-198`) with an Overlap entry injected into `THEORY_MAP_WAIVED`; asserting on `"waived" in i.lower() and "Overlap 1" in i`.
2. **`check_theory.py:102-106` — `_top_level_field` is fence-blind; a fenced example block above the real fields can both produce false failures and mask deletions.** Inherited verbatim from `check_summary.py:96-106`, so not introduced here — but the new copy ships the hole, and the family's own B4 ruling (`check_theory.py:87-92`) treats fence-swallowed content producing misleading output as a must-fix. Empirically confirmed (probe B):
   ```
   > baton. 模板示例（勿照抄）:
   ```
   theory-tex: chapter9.tex
   extraction-outcome: pending
   ```
   theory-tex: chapter1.tex
   extraction-outcome: confirmed
   …(valid Shared 1)
   ```
   → emits BOTH `✗ extraction-outcome \`pending\` 非法…` and `✗ theory-tex \`chapter9.tex\` 不存在…` despite the real values being legal (leftmost `re.search` match wins, fence lines included). Inverted variant: delete the real `extraction-outcome` line, leave the example fence → the fence's `confirmed` satisfies the legality check and the map passes with the real field absent — a silent pass. Fix: scan fences out exactly like `_split_sections` does (skip `lstrip().startswith("```")` toggles) before applying the field regex; carry the same fix back to `check_summary.py`.
3. **`check_theory.py:195-197` — `shared_nums` is built inline, duplicating `_header_numbers` and reopening the dual-parser risk the helper exists to close.** `_header_numbers` (`:116-120`) was extracted specifically so header parsing has a single site — its own docstring cites taurus I1: "单一 parser，无脱钩可能". Yet `check()` re-derives the same `{int(label.split()[1])}` expression by hand at `:197`. Today the sites agree; the first future change to label format that touches one and not the other reintroduces the I1 bug through a door the fix bricked up. Behaviorally safe to hoist (Overlap validation runs after the Shared loop completes, so precomputation is order-equivalent). Fix: `shared_nums = _header_numbers(text, "Shared")` before the loop at `:196`; delete `:195` and `:197`.

#### Minor (Nice to Have)

1. **`check_theory.py:198-200` vs `:226-229` — duplicated waived-contradiction branches, already textually drifted.** Shared's copy appends `（waived = 作者裁了最小章——Shared/Overlap 段须空，spec §Step 1 fallback）`, Overlap's copy `（waived = Shared/Overlap 段须空）` — half the rationale dropped. Hoist a single pre-loop check (`if outcome == OUTCOME_WAIVED and (shareds or overlaps): issues.append(...)` then gate both loops) so the two copies cannot drift further.
2. **`check_theory.py:44-45` — stale dead-name archaeology.** The comment explains the current regex by reference to `_ANY_ENTRY_HEADER`, "那是本规则的 Shared/Overlap 特例" — an identifier that no longer exists anywhere in the repo (grep-verified). Future readers never saw it; state the current rule, drop the tombstone.
3. **`test_check_theory.py:232` — weak assertion pin in `test_fails_on_grounding_single_chapter`.** `("2" in i or "两" in i)` matches nearly any digit. Regression analysis says the test still detects its target (drop the `<2` floor and neither the floor nor the dangling branch fires — `{1} ⊆ {1,2}` — so `"grounded-in" in i` fails), but a message rewrite to pure Chinese numerals without 两 would false-green. Pin the actual discriminating token instead: `"解析出" in i` or `"不同章" in i`.
4. **`test_check_theory.py:521-556` — manual runner with no sync guard.** Verified in-sync today (35 defined test functions, 35 called; only helper names excluded), but adding `test_*` N+1 without appending to `__main__` is a silent-never-runs failure. Same pattern in `test_check_summary.py:541+` (37/37) — family-wide. Cheap hardening: derive `called` from a declared list and assert `set == {n.__name__ for n in globals() if n.__name__.startswith("test_")}`, or assert a count constant. Sibling-carry recommendation.
5. **`check_theory.py:154` — `shareds` is the odd plural.** Sibling lineage names its section lists naturally (`callbacks`, `commonalities` in `check_summary.py:148-149`); `components` (the semantic object, per `SKILL.md:185` "one Shared per confirmed component") reads better than `shareds`.
6. **Check numbering (#2/#3/#5) is anchored only in spec prose.** SKILL.md schema comments (`SKILL.md:221`, `:234`) and Step 3 (`:339`) cite "check #2/#3/#5"; the definition lives at `docs/superpowers/specs/thesis-theory.md:177`, and the script itself carries no numbers. Recoverable, but consider numbering the check stages in the script's comments (`# --- check #2: extraction-outcome ---`) so citation and target share a file.
7. **Duplicate `## Shared N` headers are undetected** — a verbatim-duplicated entry validates cleanly twice (probe C showed per-entry checking works, `shared_nums` dedupes). Structurally ambiguous baton passes. Same absence exists in summary (its only bijection was domain-specific gap↔Callback), so this is a family-design question, not a defect of this port — record it as known limitation in tests/README if not worth a gate.

### Recommendations
- **Carry two fixes back to the shipped sibling**: the fence-blind `_top_level_field` (Issue 2) applies byte-identically to `check_summary.py:96-106`, and the runner-count guard (Minor 4) to `test_check_summary.py`. One edit, two gates hardened.
- **Probes run for this review** (evidence for Important 1-2, E disproving a suspected hole): `python3 /tmp/probe_theory.py` — keep or delete; the relevant outputs are transcribed above.
- **A suspected hole investigated and cleared**: interpolating raw `OSError` text into the stat-fallback message (`check_theory.py:268`, mirror `check_summary.py:244`) looked like an ANSI-injection route around `_sanitize` — it is not; Python's OSError formatting renders the filename via `repr()`, which escapes ESC bytes to literal `\x1b` text (probe E: output clean). Recording this so nobody re-files it.
- **SKILL.md is the family's largest at 427L** (siblings 263-359). Nothing is unearned, but the honest-boundary paragraph alone appears in ~5 near-synonymous variants across the artifact set (docstring / rule 6 / pervasive-discipline bullet / writing-discipline §6 / README §2), and rules 2/5/6 (`SKILL.md:71-78`, `99-106`, `107-119`) substantially preview what writing-discipline §1/§5/§6 then say in full. Watch this growth pattern before the next sibling copies it.
- Plan-conformance side note for scorpio: delivered suite matches the dictated 35-case set one-for-one (names and behaviors verified against `tests/README.md:11-106`, which maps every function to its intent accurately); the single addition recommended (Important 1) is *beyond* the dictated minimum, closing a hole the dictation didn't see.

### Assessment
**Verdict**: CHANGES REQUESTED
**Reasoning**: No shipped-path defect — the gate behaves correctly on everything reachable through happy-path input, and the hardening inheritance is faithfully tested. But three cheap, concretely-evidenced gaps should seal before merge: an executable branch whose removal turns a contradiction into exit 0 with nothing to catch it (Important 1), a fence-blind top-field parser that can both falsely reject and mask deletions (Important 2), and a second hand-rolled parser site contradicting the module's own single-parser invariant (Important 3). Each is a few lines.

---

## Re-review — fix commit 0c16917b (range ab5a893..0c16917)

Re-reviewed the three touched files (`scripts/check_theory.py`, `scripts/test_check_theory.py`, `tests/README.md`) plus empirical re-probes. Suite: ALL TESTS PASS (38 tests). Zero churn to `check_summary.py` confirmed (diff stat touches only the three thesis-theory files).

### Fix verification (original findings)

| Original finding | Status | Evidence |
|---|---|---|
| I-1 Overlap-under-waived untested branch | **Fixed** | New `test_fails_on_waived_with_overlap_entries` (`test_check_theory.py:200-217`) per prescription; branch replaced by hoisted pre-loop guard (`check_theory.py:204-208`) that emits ONE aggregated contradiction (`✗ Shared 9, Overlap 1 存在于 waived-by-author 终态…` — re-probe A') and gates both loops by emptying the lists. Mutation argument holds: delete the hoisted guard → waived+Overlap produces zero issues → the new assertion fails. Caught. |
| I-2 fence-blind `_top_level_field` | **Fixed** | Fence-aware line-scan with the same toggle rule as `_split_sections` (`check_theory.py:102-117`). Re-probes both variants against fixed code: poison variant → **0 issues** on a legal map (was 2 false failures); mask variant (real `extraction-outcome` deleted, fence remains) → missing-field issue fires (was silent pass). Both variants pinned as tests: `test_top_level_fields_ignore_fenced_examples` (`test_check_theory.py:521-534`) and `test_fenced_example_does_not_mask_missing_field` (`:537-551`). Summary carry booked to family hardening queue with an in-code pointer (`check_theory.py:106-107`) so the known hole isn't lost — acceptable routing, carry still owed to `check_summary.py`. |
| I-3 inline `shared_nums` duplication | **Fixed** | `shared_nums = _header_numbers(text, "Shared")` (`check_theory.py:212`), hand-rolled parse site gone; grep confirms no `shareds` leftover anywhere. Single-parser invariant restored. |
| M1 drifted waived messages | **Fixed** | Two copies collapsed into one guard with full rationale + spec ref (`check_theory.py:205-207`). |
| M2 dead-name tombstone `_ANY_ENTRY_HEADER` | **Fixed** | Removed from the `_SCOPE_TERMINATOR` comment (`check_theory.py:41-44`). |
| M3 weak `"2" in i` pin | **Fixed** | Assertion now pins `"解析出" or "不同章"` (`test_check_theory.py:253`) — the actual discriminating tokens. |
| M4 runner drift risk | **Fixed** | Auto-discovery runner over sorted `globals()` with count print (`test_check_theory.py:562-566`): 38 = number of defined `test_` functions (helpers `_new_root`/`_write_project` correctly excluded by prefix). A defined-but-uncalled test is structurally impossible; order-independence holds since every test builds its own project. Sibling `test_check_summary.py` still on manual list — same queue. |
| M5 `shareds` naming | **Fixed** | Renamed to `components` throughout (`check_theory.py:162ff`). |
| M6 check-numbering only in spec | **Fixed** | Script comments now cite spec §⑥ #1–#4 at their stages (`check_theory.py:211, 228, 239, 265`) and #5 for spine re-verify (`:183`), matching `SKILL.md` citations. |
| M7 duplicate-header nondetection | **Resolved as designed** | Recorded honestly as a known non-gated limitation with rationale in `tests/README.md:207-210` — right call for a family-design question rather than a unilateral gate. |

New code quality of the fixes themselves: hoisted-guard aggregation changes waived mode from N issues to 1 — strictly better diagnostics and simpler pins; `_top_level_field` rewrite preserves first-match semantics minus fence lines (CRLF-safe via `splitlines`; `.strip()` retained); runner discovery has no tuple-comparison hazard (keys unique strings). Nothing introduced by the fixes needs fixing.

### Assessment
**Verdict**: Approved
**Reasoning**: All three Important findings fixed with discriminating tests (verified by re-probing the exact scenarios that failed before: `got: []` mask variant now fails loudly, poison variant now green), all seven Minors either fixed or resolved-as-designed with the decision recorded on disk, and the two out-of-scope sibling carries are documented in-code pending the hardening queue rather than silently dropped.
