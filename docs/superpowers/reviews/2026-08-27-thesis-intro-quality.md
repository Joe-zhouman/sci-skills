# Code Quality Review — thesis-intro

Branch: `46b0297..HEAD` (thesis-intro feature branch — 3rd skill in the thesis writing-chain family).
Reviewer: taurus. Scope: code quality (readability, naming, duplication, error handling, separation of concerns, file responsibility, test integrity). Spec compliance is scorpio's (✅ Compliant, M1 fixed); runtime bugs are aries's.
Mirror reference: `sci-skills-thesis/skills/thesis-dissect/` (closest sibling — proven pattern this must match).

---

## Strengths

1. **Honest naming / calibration is the standout quality of this change.** The "near-trivial CONSISTENCY, NOT coverage, NOT depth" caveat is repeated, consistently, wherever the gate is described: `check_intro.py:2-11` (docstring), `SKILL.md` §①/§② (rules 1-2), `tests/README.md:35-52`, and all three references. The implementer refuses to overclaim what the gate catches — `check_intro.py:8-9` explicitly states "查不出 depth（一个 gap 实际没章 genuinely fills 但 agent 填了章号 → 过本门，是 depth failure）". This is exactly the calibration that makes the rest of the code trustworthy. A less disciplined author would have called it a "coverage gate."

2. **Error handling on the primary file is complete and non-raising.** `check()` at `check_intro.py:104-109` covers all three failure modes for gap-map.md (missing → `is_file()` false; `UnicodeDecodeError`; `OSError as e`) and returns issue strings rather than raising. The `test_graceful_on_binary_gap_map` test (`test_check_intro.py:159-175`) verifies the no-raise contract with a `try/except` that fails the test if `check()` raises. Mirrors `check_dissect.py:75-80` faithfully.

3. **The `callback-anchor` field check is the right thing to enforce, and the comment says why.** `check_intro.py:135-137` enforces `callback-anchor` presence, with the inline comment noting "gap-map.md 唯一 genuinely new 内容——§①；presence 是机械 field-check 非 depth." This is the field that earns gap-map.md its existence (per SKILL.md §①: chapter-map.md doesn't carry it, ch0-intro.tex is prose not a structured promise). Enforcing presence without pretending to check depth is the correct split.

4. **Code-fence blindness fix is mirrored correctly in both places it's needed.** `split_gaps` (`check_intro.py:40-44`) and `_chapter_numbers_in` (`check_intro.py:81-84`) both toggle `in_fence` on ``` markers, preventing a `## Gap 99` or `## Chapter 99` inside a code block from being parsed as real. Verified by `test_ignores_chapter_headers_inside_code_fence` (`test_check_intro.py:208-219`), which constructs a `## Chapter 99` inside a fence in chapter-map.md and confirms a `filled-by: Chapter 99` still fails cross-ref. Mirrors `check_dissect.py`'s aries #2 fix.

5. **Test integrity: tests verify real behavior, and redundancy was considered deliberately.** `test_passes_on_settled` (`test_check_intro.py:75-79`) asserts `issues == []` (strictly stronger than "no specific issue type"). The omitted `test_passes_when_all_filled_by_resolve` is documented at `test_check_intro.py:221-222` with the reasoning "redundant with test_passes_on_settled, which asserts the strictly stronger `issues == []`." Good — the author thought about test redundancy rather than mechanically mirroring the sibling.

6. **`PENDING_MARKER` mirror is verbatim against the original source.** `check_intro.py:29` (`PENDING_MARKER = "[pending?"`) matches `check_spine.py:26` exactly, including the subtle choice of `[pending?` (with `?`) over `[pending` to avoid matching audit-trail prose like `[pending replication by third party]` (per `check_spine.py:24-25`). The claim "镜像 check_spine" is accurate.

7. **The `init_project.py` placeholder completion is clean and contract-consistent.** The edit (`init_project.py:198-209, 222`) completes the thesis-intro CONTRACT.md block: names `gap-map.md` as the data baton, describes its schema (gap → filled-by + callback-anchor + status), and adds `thesis-summary` to the "谁读它" reader list. Uses glossary terms correctly (narrative gap / data baton / callback-anchor). Sits in the same fenced-contract format as the sibling blocks above and below it.

---

## Issues

### Critical (Must Fix)

None. No logic errors visible by reading, no broken existing functionality, no swallowed critical errors on the primary path, no secrets.

### Important (Should Fix)

1. **`check_intro.py:121-126, 150` — chapter-map.md read errors are silently swallowed, and the gate can overclaim "consistency 通过."**

   The chapter-map read has its own handler:
   ```python
   # check_intro.py:121-126
   if chapter_map_path.is_file():
       try:
           cm_text = chapter_map_path.read_text(encoding="utf-8")
           chapter_nums = _chapter_numbers_in(cm_text)
       except (UnicodeDecodeError, OSError):
           chapter_nums = set()  # chapter-map 不可读 → cross-ref 查不出，但 core 查继续
   ```
   Compare the gap-map read at `check_intro.py:104-109`, which *returns an issue* for both `UnicodeDecodeError` and `OSError`. The asymmetry is: primary file unreadable → reported (fatal); secondary file unreadable → silently swallowed, `chapter_nums = set()`.

   The silent swallow combines with the truthiness guard at `check_intro.py:150`:
   ```python
   elif chapter_nums and ch_num not in chapter_nums:
   ```
   When `chapter_nums` is an empty set (from the swallowed except, OR from an empty-but-readable chapter-map), `chapter_nums and ...` short-circuits — cross-ref is skipped for *every* gap. No issue is appended. `main()` then prints `check_intro: ✓ consistency 通过` (`check_intro.py:172`) even though the cross-ref check — one of the gate's named responsibilities — silently did not run.

   Why it matters: the gate's pass message overclaims. "consistency 通过" implies cross-ref ran; it didn't. The comment at line 125-126 ("cross-ref 查不出，但 core 查继续") documents the *intent* (core checks continue), but the implementation also suppresses the *signal* that cross-ref was skipped. A user running check_intro.py gets no indication that the one cross-skill consistency check was disabled.

   Scope is narrow: in the normal flow, dissect produced chapter-map.md and `check_dissect.py` already verified it's readable + non-empty, and intro's Step 0 (`SKILL.md:188-191`) hard-stops if dissect isn't complete. So an exists-but-unreadable chapter-map requires manual corruption between dissect and intro. But error-handling consistency is a code-quality concern regardless of hit-rate, and the overclaim is real.

   Fix: append an issue when the except fires, e.g. `f"✗ {chapter_map_path} 不可读（二进制/权限）— cross-ref 跳过"`. This preserves the "core checks continue" intent (don't `return`) while making the gate's output honest. Optionally also report when `_chapter_numbers_in` returns an empty set from a readable-but-empty chapter-map (same overclaim risk via the `and` guard).

   Also untested: there is no equivalent of `check_dissect.py`'s `test_graceful_on_unreadable_file` (`test_check_dissect.py:176-198`, the chmod-000 case) for *either* file in the intro suite. The `except OSError` handler at `check_intro.py:108` (gap-map) and the `except (UnicodeDecodeError, OSError)` at `check_intro.py:125` (chapter-map) are both uncovered by a permission-denied test. The binary test only exercises `UnicodeDecodeError`.

### Minor (Nice to Have)

1. **`test_check_intro.py:179` — dead `_write_project()` call; return values immediately shadowed.**
   ```python
   def test_fails_on_dangling_filled_by():
       gm, cm, tex_dir = _write_project()          # line 179: assigned but UNUSED
       bad = GAP_MAP_SETTLED.replace(...)
       gm, cm, tex_dir = _write_project(gap_map=bad)  # line 182: reassigned, actually used
   ```
   Line 179 builds a complete temp project (gap-map + chapter-map + tex) that is never read — its outputs are overwritten on line 182. A reader has to pause to confirm the first call is dead. Delete line 179.

2. **`test_check_intro.py` — no test for trailing-title gap headers (`## Gap 1 (note)`).**
   The regex at `check_intro.py:46` allows trailing titles via `(?:\s+.*)?$`, mirroring `check_dissect.py:40`. But the dissect suite has a dedicated `test_chapter_headers_with_trailing_title_accepted` (`test_check_dissect.py:163-174`) that constructs `## Chapter 1 (绪论)` and verifies it parses; the intro suite has no `## Gap N (title)` equivalent. The trailing-title branch is untested — if someone simplified the regex to `^##\s+(Gap\s+\d+)$`, all 17 tests would still pass. Add a mirror test.

3. **`check_intro.py:111-155` — inline comment numbering out of order: 1, 2, 3, 2b, 4, 6, 5.**
   The `2b` (`check_intro.py:135`) reflects the callback-anchor check being inserted later (the M1 scorpio fix). The sequence then jumps 4 → 6 (`check_intro.py:144`) → 5 (`check_intro.py:155`). A reader expects sequential order. Renumber 1-6 cleanly, or drop the numbers (the code is linear enough to read without them).

4. **`check_intro.py:40-44` vs `81-84` — intra-file code-fence toggle duplication (3 lines).**
   Both `split_gaps` and `_chapter_numbers_in` implement the same `if line.lstrip().startswith("```"): in_fence = not in_fence; continue` toggle. The functions differ in body handling (`split_gaps` preserves fence lines in the gap body; `_chapter_numbers_in` skips them), so they're not fully unifiable, but a small `_iter_unfenced_lines(text)` yielding `(line, in_fence)` tuples would remove the duplicated toggle. Borderline worth it for 3 lines — judge by whether a 4th consumer appears. (Note: the *cross-skill* duplication of `_field_value` / `_is_empty` / `split_*` with `check_dissect.py` and `check_spine.py` is **by-design** — the glossary's "Contracts over imports" principle forbids cross-skill code imports as the cost of decoupling-as-survival-strategy. Not flagged as an issue.)

---

## Recommendations

- **Cross-skill triplication is now worth watching.** `_field_value` (`check_intro.py:60-64` ↔ `check_dissect.py:54-59`), `_is_empty` (`check_intro.py:67-72` ↔ `check_dissect.py:62-67`), and `split_*` (near-identical save the regex) now exist in three siblings (spine, dissect, intro). This is the accepted cost of the decoupling principle and is correct for now. If a 4th writing-chain sibling arrives, reconsider whether a shared `thesis_checks` utility module (imported within the *plugin*, which is one replaceable unit, not a cross-skill import) is worth breaking the pure-copy pattern. Architectural call, not a code-quality defect — flagged for the record.

- **Gate-message honesty is worth a standing rule.** The Important finding is a instance of a general pattern: a gate that silently skips one of its named checks and then reports "通过." If more `check_*.py` siblings are added, consider a convention: any skipped check must emit a non-fatal informational issue, so "通过" always means "all named checks ran and passed," never "some checks ran and the rest were silently disabled."

---

## Assessment

**Verdict**: PASS

**Reasoning**: The code is a faithful, well-calibrated mirror of the proven dissect pattern. Tests verify real behavior (17/17 pass, strict `issues == []` assertion on the happy path, deliberate omission of redundant cases). Honest naming is the standout — the "near-trivial consistency, NOT depth" caveat is repeated everywhere and the implementer refuses to overclaim. The one Important issue (chapter-map read errors silently swallowed, letting the gate report "consistency 通过" while cross-ref was skipped) is a real error-handling inconsistency worth fixing, but it is narrow — precondition-guarded by dissect's own gate + intro's Step 0 hard-stop, so it only triggers on manual corruption between skills. No Critical issues; no logic errors; no broken functionality. Recommend addressing the Important finding and the two test-mirror gaps (trailing-title test, unreadable-file test) before relying on the cross-ref signal, but none block merge.
