# Code Quality Review — thesis-spine

> Reviewer: taurus (code quality) | Range: `688534e..56b323b` (branch `thesis-spine`)
> Jurisdiction: HOW the code is built (static read). Spec compliance = scorpio (0 issues, prior).
> Files reviewed: plugin.json, SKILL.md, check_spine.py, test_check_spine.py,
> writing-discipline.md, spine-schema.md, tests/README.md.
> Glossary loaded: `docs/superpowers/glossary.md` (6 thesis terms).

## Strengths

- **Clean separation of concerns in `check_spine.py`.** `check()` (check_spine.py:54-98)
  returns a list of issues and never throws; `main()` (check_spine.py:101-110) handles
  printing + exit code. Tests call `check()` directly (test_check_spine.py:49, 56, 63, ...)
  — they verify **behavior** (pass/fail conditions), not implementation. No test reaches into
  `split_sections` or `_find_section`. Good test integrity.

- **The enforcement split is empirically proven, not just asserted.**
  `test_ignores_umbrella_and_boundary` (test_check_spine.py:75-84) is load-bearing: it
  empties both `## Thesis-level claim` and `## Boundary` and asserts `issues == []`. The
  comment explains *why* — they are depth (human-gated), NOT coverage. This is the test
  that would catch a future regression if someone added umbrella to `STRUCTURAL_FIELDS`.
  `STRUCTURAL_FIELDS` (check_spine.py:20) excludes umbrella by listing only the 3.

- **Terminology discipline is excellent — zero `_Avoid_` aliases.** Every glossary term is
  used canonically: "coverage mechanical gate" / "depth human-gate" always specify the layer
  (glossary: "must always specify which layer"); "Compass-file coupling (罗盘文件)"
  (SKILL.md:61); "read neighbors, don't orchestrate" (SKILL.md:25, 196); "contract gap"
  (SKILL.md:158); "拆即写" (SKILL.md:77, 165, 195). No "manuscript" for thesis, no
  "validation error" for gap, no "outline" for plan.

- **The PENDING_MARKER design is deliberate, and documented.** check_spine.py:22-23
  explains why the baton header uses backtick-\`pending\` (no `[`): so the `[pending`
  substring catches actual markers, not the protocol explanation in the header comment.
  The schema template (spine-schema.md:9-11) follows this convention. Self-consistent.

- **Decoupling holds — verified.** `grep` for `from thesis-` / `import thesis-` in the
  spine source: zero hits. The only `thesis-dissect` mentions (SKILL.md:195, tests/README.md:33)
  are prose handoff ("Point the author to thesis-dissect") and the decoupling *assertion*
  itself. No skill calls a sibling skill. thesis-init confirmed at
  `sci-skills/skills/thesis-init/` — matches plugin.json:3's claim.

- **writing-discipline.md is zero-dependency and says so** (L3: "零依赖——这里是全部内容，
  不引用任何外部 skill 的文件"). The "forbidden forms" (L36-39) and "honest residual"
  (L52-63) sections are concrete — specific banned phrases, not abstract guidance.

- **File sizes appropriate to responsibility.** SKILL.md 241 lines for a writing-chain
  entry with this much discipline; references 100/59 lines; check_spine.py 114 lines;
  test_check_spine.py 118 lines. Nothing in this change created an oversized file or
  grew one significantly.

## Issues

### Critical (Must Fix)

None. The code is correct (8/8 tests pass), the enforcement split is empirically proven,
decoupling holds, no swallowed errors, no logic errors visible by reading.

### Important (Should Fix)

1. **SKILL.md:24 — duplicated glossary term.** `"...those are dissect's job (拆即写,
   拆即写)."` — "拆即写" appears twice in one parenthetical. L77, L165, L195 each use it
   once; L24 is the only double. Typo. → Delete one `拆即写`.

2. **SKILL.md:70 — stale "pytest-tested" claim, contradicts the implementation.** The
   "Layout & boundaries" table says `check_spine.py` is "pytest-tested", but:
   - test_check_spine.py:1 docstring: "stdlib tests for check_spine.py"
   - tests/README.md:6: "8 stdlib cases, run `python3 test_check_spine.py`"
   - tests/README.md:24: "runnable stdlib test"
   - The implementation uses plain `assert` + `print` + `if __name__ == "__main__"`
     (test_check_spine.py:109-118), no pytest fixtures, no `import pytest`.

   The spec §⑥ said "stdlib pytest" (self-contradictory — pytest isn't stdlib); the
   implementation resolved this correctly by going stdlib-only, but SKILL.md:70 inherited
   the "pytest" word and wasn't reconciled. Note: SKILL.md:94 (the "File contracts"
   table) omits the test-runner claim entirely — so SKILL.md is also internally
   inconsistent (L70 says pytest, L94 doesn't). → Replace "pytest-tested" with
   "stdlib-tested" (or drop the qualifier; tests/README.md is the canonical runner doc).

### Minor (Nice to Have)

1. **check_spine.py:62 (`PENDING_MARKER = "[pending"` substring on whole text) —
   empirically false-positives on `[pending` in prose.** Confirmed by running the script
   on a fixture where a Cracks evidence line quotes `paper-C §4.2 notes "[pending review]"`
   — the check flags it as an unsettled candidate. *This is the right asymmetry for a
   coverage gate* (false-positive cost = one author review; false-negative cost = dissect
   building on an unsettled field), so conservative is acceptable — answering the
   orchestrator's question directly. If tightening later, `re.search(r"\[pending\??\s*\]",
   text)` matches the actual marker formats (`[pending]` / `[pending?]` / `[pending? ]`)
   while skipping prose quotes. Not needed now; the tradeoff is worth a one-line note in
   the comment at check_spine.py:22-23 (which currently documents only the backtick-
   \`pending\` avoidance, not the prose-quote risk).

2. **check_spine.py:81 (`if pid not in framework`) — substring match is false-negative
   prone, asymmetric with PENDING_MARKER.** If `paper-B` appears in framework prose
   without being an instantiation line (e.g. "note: paper-B's view differs"), the check
   passes despite no instantiation. This is conservative in the *wrong* direction for a
   coverage gate (misses a gap, vs. PENDING_MARKER's flag-too-much). Tighter:
   `re.search(r"per-paper:.*" + re.escape(pid), framework)`. Low risk — the schema
   (spine-schema.md:17-18) controls the `per-paper: how paper-X instantiates it` format,
   so in practice `paper-B` in framework prose without an instantiation line is unlikely.

3. **check_spine.py:49 (`_find_section` uses `startswith(prefix)`)** — if two sections
   share a prefix (e.g. "Main line" and "Main line of reasoning"), returns the first match.
   The schema controls section names so unlikely, but a tighter anchor would be
   `name == prefix or name.startswith(prefix + " (")` (matching the `(主线)` suffix).

4. **test_check_spine.py:44 (`tempfile.mkdtemp()`) — temp dirs never cleaned up.** For a
   stdlib test run once per eval, negligible; under frequent CI it leaks. Switching to
   `tempfile.TemporaryDirectory()` + `with` would clean up but requires restructuring
   `_write_fixture` to return the dir handle. Minor.

5. **No tests for regex robustness edges.** The 8 tests cover the documented schema
   cases (good), but not: `_find_section` prefix collision, `split_sections` with `###`
   sub-headers, non-`paper-` Intake entry formats, `[pending` in prose. Add only if the
   schema is expected to evolve; the current schema is controlled and the tests cover it.

## Recommendations

- **The PENDING_MARKER substring match is fine for coverage-only.** Conservative
  (false-positive > false-negative) is the correct asymmetry here. The orchestrator's
  framing — "coverage-only and conservative is acceptable" — is right. The one-line
  comment at check_spine.py:22-23 should add the prose-quote tradeoff to its existing
  backtick-\`pending\` note, so a future maintainer knows the conservative choice is
  deliberate on both fronts.

- **Reconcile "pytest" vs "stdlib" family-wide.** The spec §⑥ "stdlib pytest" was the
  source of the stale claim. A `grep -rn "pytest" sci-skills-thesis/` would catch any
  other inherited instances. The repo's justified deviation (init precedent) is
  stdlib-only tests; the terminology should follow.

- **Process note:** the duplicated `拆即写` at SKILL.md:24 and the stale "pytest" at
  SKILL.md:70 are both signs of late-edit drift — the spec evolved (round 3 moved
  umbrella to depth; §⑥ settled on stdlib) but SKILL.md prose wasn't re-scanned. A
  pre-commit grep pass on SKILL.md against tests/README.md + the spec would catch this
  class of drift.

## Assessment

**Verdict**: PASS

**Reasoning**: The implementation is well-built — clean separation of `check()`/`main()`,
load-bearing tests that verify behavior not implementation, excellent glossary
discipline, sound decoupling, and a deliberately conservative coverage gate with the
right asymmetry. The two Important issues (duplicated `拆即写` at SKILL.md:24, stale
"pytest-tested" at SKILL.md:70) are prose-accuracy nits that don't affect functionality
or the enforcement split — fix them, but they don't block merge. The PENDING_MARKER
substring match, the focus question, is the correct tradeoff for a coverage-only gate.
