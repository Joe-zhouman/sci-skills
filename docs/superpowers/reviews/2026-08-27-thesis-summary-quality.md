# Code Quality Review — thesis-summary

Branch: `503f204..HEAD` (thesis-summary feature branch — 4th skill in the thesis writing-chain family).
Reviewer: taurus. Scope: code quality (readability, naming, duplication, error handling, separation of concerns, file responsibility, test integrity). Spec compliance is scorpio's (✅ Compliant, M1 fixed); runtime bugs are aries's.
Mirror reference: `sci-skills-thesis/skills/thesis-intro/scripts/check_intro.py` + `test_check_intro.py` (the named quality baseline — same family pattern, now one generation further). Probes cited below were executed against HEAD, not read off the page.

---

## Strengths

1. **Honest naming/calibration carried through unchanged, in all four surfaces.** The near-trivial-consistency caveat and its inverse ("查不出 depth") appear consistently in `check_summary.py:4-15` (docstring — including the genuinely useful attribution split: *what* in each section is genuinely new vs *near-trivial-by-construction*), SKILL.md rules 1/7 (`SKILL.md:43-53`, `87-93`), tests/README.md §2 (`tests/README.md:75-90`) and the known-limitation footer (`tests/README.md:126-133`). The `anchor-in-synthesis` demotion is stated identically in code-relevant prose (`SKILL.md:204-206`) and the README (`tests/README.md:131-133`). Nothing overclaims "coherence guarantee" anywhere.

2. **Error handling on the secondary batons is better than the baseline it mirrors.** Both intro-review findings are closed: gap-map read failure emits `"✗ ... gap↔Callback 对应检查跳过"` (`check_summary.py:133-135`) and chapter-map failure emits `"✗ ... grounded-in cross-ref 跳过"` (`check_summary.py:145-147`) instead of the silent swallow the intro round had — and each has a dedicated test asserting the exact skip message (`test_check_summary.py:294-302`, `312-319`). Primary-file failure modes (missing / non-UTF-8 / OSError) all return issue strings, never raise (`check_summary.py:115-122`), with the no-raise contract enforced by try/except (`test_check_summary.py:188-192`).

3. **The bijection — this gate's reason to exist — is correct and ordered defensively.** Duplicate-callback detection sits *after* the fabricated-ref `elif` but does not depend on `gap_nums` being populated (`check_summary.py:161-166`: `else: seen_gap_refs[n] = label` catches duplicates even when cross-ref data is unavailable). Both directions are tested: absence (`test_fails_on_missing_gap_callback`, `255-266`) and duplication (`268-275`).

4. **The synthesis-tex path guard is a faithful mirror of the intro aries re-test, with both attack vectors covered.** Absolute-path + `..` rejection via `PurePath.parts` (`check_summary.py:208-210`), existence check on the composed path (`211-212`); tests cover `/etc/passwd` and `../../../etc/passwd` separately (`test_check_summary.py:238-253`). `_single_ref_number` correctly rejects 0-match and >1-match values (`check_summary.py:106-109`), mirrored by two distinct tests (`118-123`, `125-131`).

5. **Fence-awareness survived the generalization — and the new test asserts the load-bearing direction.** Generalizing intro's `split_gaps` into parameterized `_split_sections(text, header_word)` (`check_summary.py:35-61`) preserved fence toggling, and `test_ignores_entries_inside_code_fence` (`test_check_summary.py:359-381`) checks the direction that matters for a lock: a fenced fake Callback 3 must NOT count toward covering Gap 3. The trailing-title regex branch also got the dedicated test the intro suite originally lacked (`216-222`).

6. **BOM handling applied uniformly, not just to the primary file.** All three reads use `utf-8-sig` (`check_summary.py:118`, `131`, `143`). `test_ignores_utf8_bom_in_summary_map` (`test_check_summary.py:195-214`) is well-designed: the BOM'd fixture starts with a *fabricated* `gap-ref: Gap 999`, proving stripping actually re-enabled parsing rather than merely passing vacuously.

7. **The `init_project.py` placeholder completion is contract-consistent and removes the stale promise.** `init_project.py:267-274` names `summary-map.md` with its full schema (Callback/gap ↔ gap-map `Gap N` 一一对应, Commonality confirmed 痕迹, `synthesis-tex` 按 template-spec 非硬编码) and names `check_summary.py` as reader; `281-284` updates the read-lists and replaces the old "读 sources registry" bullet with the honest 信息流单向收敛 statement. The relative depth `../../thesis/template-spec.md` is correct against the actual scaffold location (`init_project.py:98`, `116` — copied to `thesis/`). The obsolete "该 skill 后续计划补" line is deleted, replaced by the completed fact.

8. **Test inventory claims verify.** 26 `def test_` functions, 26 entries in the runner (`test_check_summary.py:384-409`), matching the README count (`tests/README.md:6-8`); the whole suite passes (`ALL TESTS PASS`, executed at review time). Fixtures use the module-level constants + `str.replace` mutation shape per the known design decision.

---

## Issues

### Critical (Must Fix)

None. No logic errors on the documented paths, no secrets, no broken existing functionality in the `init_project.py` diff.

### Important (Should Fix)

1. **`check_summary.py:85-100` vs `42` — the same header grammar is parsed by two regexes that provably disagree; one parser is redundant and the divergence reaches verdict logic.**

   `_split_sections` anchors fully: `^##\s+{word}\s+(\d+)(?:\s+.*)?$` (`:42`). `_header_numbers` anchors nowhere: `^##\s+{word}\s+(\d+)` (`:90`). Executed probe on `## Gap 2x\n- gap: y`:

   ```
   A1 header_numbers: {2}
   A2 split_sections: []
   ```

   Consequence beyond taste: for `## Gap 2x`, `_header_numbers` puts 2 into the bijection set (`:132`), demanding a `Gap 2` Callback — while `_split_sections` did *not* treat that line as a boundary, so `2`'s actual fields stay glued to the preceding entry's body and are never checked as their own entry. Numbering and field-scoping come from different parsers that disagree on which lines start an entry; a single stray suffix character desyncs them. Since labels are constructed as `f"{header_word} {n}"` (`:54`), `_header_numbers` is fully derivable from `_split_sections`:

   ```python
   {int(label.split()[1]) for label, _ in _split_sections(text, word)}
   ```

   Executed parity check including the fenced-header case: identical result (`C: {2} | from labels: {2}`). Fix deletes ~16 lines and removes the class of drift entirely.

   Family note: intro has the same-shaped pair (`check_intro.py:32-57` vs `83-98`) and was reviewed as Minor there because the bodies differed enough that they weren't unifiable. This generalization step removed that excuse — hence upgraded here.

2. **`check_summary.py:161`, `176`, `192` — a *readable but header-less* secondary baton silently disables this gate's named checks, and `main()` still reports 通过.**

   All three checks are guarded by truthiness on the number sets: `elif gap_nums and n not in gap_nums` (`:161`), `if gap_nums:` bijection loop (`:176`), `elif chapter_nums and not nums <= chapter_nums` (`:192`). An unreadable baton now emits an issue (#2 above — good), but a UTF-8-valid baton whose entries are gone yields `set()` and skips everything quietly. Executed probe — gap-map.md present, valid UTF-8, zero `## Gap N` headers, while summary-map references `Gap 1`:

   ```
   B issues: []
   ```

   Zero issues, including no fabricated-ref flag for `Gap 1` — and `main()` would print `✓ consistency 通过` (`:227`). For *this* gate specifically that stings more than in intro: 缺席检测 against gap-map.md is the gate's stated lock core (`check_summary.py:175` comment), and "lock passed with zero callbacks checked against anything" is printed as success. Reach is narrow — check_intro rejects such a file outright (`check_intro.py:127-128`) and Step 0 self-checks entries exist (`SKILL.md:219-222`) — which keeps this Important, not Critical. Fix: when the file is present/readable but yielded nothing, say so:

   ```python
   elif gm_path.is_file() and not gap_nums:
       issues.append(f"✗ {gm_path} 可读但无任何 ## Gap N 条目 — gap↔Callback 对应检查跳过")
   ```

   (chapter-map analog optional, lower stakes.)

3. **`test_check_summary.py:158-172`, `174-193`, `195-214` — three hand-rolled rebuilds of scaffolding the file's own helper already builds (~45 avoidable lines).**

   Each constructs the same six-step mkdir/write chain that `_write_project()` (`83-102`) produces, because the mutation needed happens to hit `summary-map.md` itself. No signature change is required — build normally, then mutate the returned handle:

   - `test_fails_on_missing_summary_map`: `_write_project()` then `sm.unlink()`
   - `test_graceful_on_binary_summary_map`: `_write_project()` then `sm.write_bytes(...)`
   - `test_ignores_utf8_bom_in_summary_map`: same with `codecs.BOM_UTF8 + b"## Callback 1..."`

   Nine duplicated blocks of directory plumbing is nine chances for one copy to drift from the settled fixture (e.g. these three hand copies already create a *different* project shape than the helper's). Collapse to helper + mutation.

### Minor (Nice to Have)

1. **`SKILL.md:113` — `template-spec.md` is drawn inside the `sci-skills/` layout tree, but init scaffolds it at `thesis/template-spec.md`.** Cross-checked against `init_project.py:98` and `116` (复制到 `thesis/`). One-line fix: move it under `thesis/` in the tree or annotate `thesis/template-spec.md`. Worth checking whether intro/dissect trees carry the same slip.

2. **OSError arms are untested everywhere** — `check_summary.py:121-122` (primary), `133-134` (gm), `145-146` (cm). All "binary" fixtures go through `write_bytes(b"\xff\xfe...")`, which triggers `UnicodeDecodeError` only. The dissect suite has the chmod-denied precedent for exactly this arm; one permission-denied test (or unittest.mock raising PermissionError) closes it for all three files at once.

3. **`test_fails_on_malformed_gap_ref` (`test_check_summary.py:118-123`) cannot distinguish its message from the missing-field case.** Its assertion predicate (`"gap-ref" in i and "Callback 1" in i`) is identical to `test_fails_on_missing_gap_ref`'s (`111-116`). If `:160`'s message regressed to reuse the missing-field string, this test would never notice. Assert the distinguishing fragment: `"无法解析"`.

4. **`import codecs` is function-local (`test_check_summary.py:198`).** Move to the top-level stdlib imports (`:12`).

5. **`tests/README.md:7` — "0 = consistency through" is a translation artifact of 通过.** "0 = consistency check passes" reads as intended.

6. **Foreign-type headers fold into the previous entry's body (`check_summary.py:49-58`).** Splitting on `Callback` terminates an entry only at the next `Callback` header, so Commonality lines append into the last Callback's body (and vice versa when splitting on `Commonality`). Today this is benign: field names are disjoint except `status`, and re-first-match semantics favor the owning entry as long as sections follow the template order (SKILL.md schema, `SKILL.md:186-198`, Callback 段 before Commonality 段). Low priority — but treating any `^##\s+(Callback|Commonality)\s+\d+$` line as an entry terminator would make scoping order-independent for 3 lines.

---

## Recommendations

- **Finish the "no silent skip" convention.** The intro review proposed it; this branch implemented half (unreadable → issue emitted) and left the other half (empty-but-readable → silent skip, Important #2) open. Two siblings now show both halves of the pattern; settle it once so the fifth `check_*.py` doesn't re-litigate: *every conditionally-skipped named check emits an informational issue; 通过 always means all named checks ran.*

- **Cross-skill copy count now stands at four.** `_field_value` / `_is_empty` / `_top_level_field` / `_NONE_TOKENS` / the PurePath path-guard exist independently in spine, dissect, intro, and now summary — the accepted cost of contracts-over-imports, still correct at four. Thesis-theory is the fifth writing-chain member; that is the trigger point to reconsider a plugin-local `thesis_checks` utility (one replaceable unit, unlike a cross-skill import).

- **Glossary candidate: "Intro↔Summary coherence lock."** It carries the branch — SKILL.md front matter (`SKILL.md:4-6`), rule 1 (`43-53`), the init CONTRACT block (`init_project.py:267-274`), throughout the README. The glossary currently covers `Narrative gap` (its data side) but not the lock itself; defining the term (enforce-side semantics: structured-vs-structured, baton-vs-baton, not prose-vs-promise) would keep the fifth skill from drifting into calling it a "coherence guarantee."

---

## Assessment

**Verdict**: PASS

**Reasoning**: The gate is a faithful, well-calibrated extension of the proven intro/dissect pattern, and visibly *better* than its baseline on error handling (both secondary-baton failures now emit, each with a dedicated test). The 26-test suite verifies real behavior and runs green. The three Important findings — dual parser divergence with an observed disagreement (`## Gap 2x` → `{2}` vs `[]`), the readable-but-headerless silent-pass probe returning `[]`, and the tripled test scaffolding — are cheap, localized fixes that harden honesty and maintainability without touching the happy path, and none breaks existing functionality. Recommend landing them before thesis-theory forks from this mirror lineage.

---

## Re-review — fix commit `48a032b` (+ glossary `9a0120a`, prose-only)

Scope of this pass: verify each finding's fix quality, re-run the full suite and the original probes, and settle the weak-pin question on `test_parses_sections_in_any_order`. All claims below were executed against HEAD = `48a032b`, not read off the diff.

### Fix verification (all executed)

| Finding | Status | Evidence |
|---|---|---|
| I1 dual parser | **closed** | `_header_numbers` now derives from `_split_sections` labels (`check_summary.py:94-98`); old unanchored regex deleted. Re-run of probe A (`## Gap 2x`): both surfaces now return `set()` / `[]` — single parser, no divergence possible by construction. |
| I2 headerless silent-pass | **closed** | Read blocks inverted to not-is-file/else-try (`check_summary.py:128-139`, `142-152`); readable-but-headerless gm/cm each emit an issue. Probe B re-run returned exactly one issue: `✗ ...可读但无任何 ## Gap N 条目 — gap↔Callback 对应检查跳过`. Both paths covered by `test_fails_on_headerless_gap_map` / `_chapter_map`. |
| I3 scaffold triplication | **closed** | All three tests collapsed to `_write_project()` + `sm.unlink()` / `sm.write_bytes(...)`; directory plumbing exists once. |
| M1 tree placement | **closed** | `template-spec.md` moved under `thesis/` in the SKILL.md layout tree (48a032b SKILL.md hunk). |
| M2 OSError arm | **closed** | `test_graceful_on_permission_denied_summary_map` chmods 000, asserts graceful 无法读取, restores mode in `finally`. |
| M3 weak malformed assertion | **closed** | Now asserts `"无法解析"` (`test_check_summary.py`, 48a032b hunk) — distinguishes from the missing-field case. |
| M4 local import | **closed** | `codecs` moved to top-level imports. |
| M5 README wording | **closed** | "consistency check passes"; no-silent-skip convention recorded in §2 (`tests/README.md`, 48a032b hunk). |
| M6 foreign-header folding | **closed in code** | `_ANY_ENTRY_HEADER` terminator (`check_summary.py:35-37`, `64-67`) makes scoping order-independent — but see Important 4 below: its failure branch has zero test coverage. |

Suite: **30/30 PASS** at HEAD. Glossary commit `9a0120a` adds the coherence-lock term as recommended; prose-consistent, no code.

### Weak-pin ruling: encode the strong pin — do NOT leave it to adversarial validation

The suspicion was correct, now proven by execution. The committed fixture (Commonality section moved before Callbacks, all fields complete) returns `[]` under **both** the old code (reconstructed via `git show HEAD~1`) and the new code:

```
W(weak pin) OLD: []
W(weak pin) NEW: []
```

So `test_parses_sections_in_any_order` documents the positive property but cannot detect reversion of `check_summary.py:64-67`. That branch is *new code introduced by this very fix* — its fold-in failure mode is entirely untested; deleting those four lines keeps all 30 tests green.

Why manual probes aren't enough here: this family's convention — enforced across three aries rounds — is that every claimed mechanical property lands as a test. The README already asserts order-independence as a checked case; as committed, only half the property is checked (the direction the old code also satisfied). Silent mis-scoping is precisely the defect class this suite exists for.

The discriminating fixture is cheap and verified. Construction: Callback 2 carries **no** `status`; a trailing foreign Commonality carries `status: confirmed`.

```
S2(Cb2 no status + Co confirmed tail) OLD: ✗ Callback 2 status=confirmed（应为 filled；pending=未写完，…）
S2(strong pin)                       NEW: ✗ Callback 2 缺 status
```

Old misattributes the foreign `confirmed` into Callback 2; new reports the honest 缺 status. One assertion string separates the implementations. Drop-in form (mirrors the existing mutation idiom):

```python
def test_fails_on_status_bleed_from_foreign_entry():
    """Callback 2 lacks status; trailing Commonality carries one → 缺 status must be
    attributed to Callback 2 itself. Old fold-in reported 'status=confirmed' (wrong
    attribution); revert-detection oracle for _ANY_ENTRY_HEADER termination."""
    bad = (SUMMARY_MAP_SETTLED
           .replace("""## Callback 2
- gap-ref: Gap 2
- resolved-how: 第 5 章回顾可解释性贡献，收束 Gap 2
- status: filled

""", """## Callback 2
- gap-ref: Gap 2
- resolved-how: 第 5 章回顾可解释性贡献，收束 Gap 2

"""))
    sm, gm, cm, tex_dir = _write_project(summary_map=bad)
    issues = check_summary.check(sm, gm, cm, tex_dir)
    assert any("Callback 2" in i and "缺 status" in i for i in issues), \
        f"foreign-status bleed mis-attributed, got: {issues}"
```

(Verified behaviorally above; adapt the exact `replace` target to the settled fixture text.)

### New findings

#### Important (Should Fix)

4. **`check_summary.py:64-67` — the entry-terminator branch added by this fix is untested; the committed any-order pin does not discriminate (proven green under pre-fix code).** → Encode the strong pin per the fixture above so reverting the terminator fails the suite. This is regression armor for glue added minutes ago, not a behavior bug — new code answers correctly on every construction probed (`缺 status` attributed to the right entry in both no-status variants).

#### Minor (Nice to Have)

7. **`check_summary.py:136`, `149` — review-tag leakage into operator-facing gate output.** The strings print `（taurus I2）` as part of the issue line users read; sibling messages carry no such tags, and tags rot once the review is forgotten. Comments at `:36`, `:44`, `:98` are the right home for provenance — strip the suffix from the two f-strings.

### Final Assessment

**Verdict**: PASS

**Reasoning**: All three Importants and Minors 1-5 are verifiably closed — single parser (probes agree), no-silent-skip wired end-to-end with tests and README convention, scaffolding collapsed; suite 30/30 green; original probes return clean results. Two items carry forward, neither a shipped-behavior defect: encode the discriminative strong pin for the new terminator branch (fixture provided, ~10 lines), and strip the review tag from the two gate messages. The weak-pin question is answered definitively: manual probes already proved the point — now spend the ten lines to keep it proven forever.
