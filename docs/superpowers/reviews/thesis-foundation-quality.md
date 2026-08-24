# Code Quality Re-Review — thesis-foundation slice (post-taurus-fixes)

> Reviewer: taurus (code quality), re-review after fixes
> Prior review: this file, v1 (PASS with 1 Important + 6 Minor)
> Range: `git diff 264d898..cd1dacf -- sci-skills-thesis/` (full slice); fix commit `cd1dacf`
> Spec: `docs/superpowers/specs/thesis-skill-family.md` (approved)
> Glossary read: `docs/superpowers/glossary.md` — no `_Avoid_` aliases in the new/changed code. Terms (Thesis / Family namespace / Compass file / Read neighbors don't orchestrate / 拆即写) all match settled definitions.
> Test run: `cd sci-skills-thesis/skills/thesis-init/scripts && python3 test_init.py` → **10/10 PASS** (ran myself, output verified)

---

## What changed (fix commit cd1dacf)

Three files touched, +85/-9 lines:
- `init_project.py` — cmd_checkup extended (main.tex verify + tex/ integrity + .cls informational); git init two-arm; comment fixed
- `test_init.py` — 2 new tests (missing main.tex, missing tex/ dir)
- `SKILL.md` — line 154 rewritten to match impl

---

## Fix verification (prior issues, each confirmed landed)

### Important #1 — SKILL.md:154 doc/code mismatch → RESOLVED

The fix took the "extend the check" path (the more useful long-term option), not the cheaper doc-tighten. Verified end to end:

- **main.tex presence verified, flagged as issue when missing.** `init_project.py:525` (`main_tex = tex_dir / "main.tex"`), `:529` (`"main_tex": main_tex.is_file()` in JSON), `:539-542` (`if not main_tex.is_file(): issues.append(...)`). This is the universal compile entry point — its absence is a real weave-integrity break, correctly raised to `issues` (not just reported).
- **.cls is informational only, never required.** `init_project.py:524` (`cls_files = sorted(...)` with `# informational only` comment), `:530` (list in JSON), `:532` (`cls_note` for human report), `:535` (shown in report line). No `issues.append` for empty `cls_files`. This matches the shipped reality: generic-test uses `\documentclass{report}` (templates/thesis/generic-test/main.tex:1) with no `.cls` at all — the prior review's core finding.
- **tex/ dir missing flagged** (this was prior Minor #4, folded into this fix). `init_project.py:516-521`: `if not tex_dir.is_dir()` → report + issue + `info["thesis"]["tex_dir"] = False`. No more silent `tex 文件: 0`.
- **SKILL.md:154 now matches impl exactly.** Doc claims, left to right: `thesis/ present?` (init_project.py:510), `tex/ present?` (:516), `main.tex present?` (:539), `how many .tex files?` (:528), `template-spec.md present?` (:543), `.cls reported informationally — not required` (:524/:532, no issue path). Every claim maps to a code line. No phantom claims remain.
- **2 new tests pass and assert the right thing.** `test_init.py:175` (`test_checkup_flags_missing_main_tex`): deletes main.tex, asserts `rc != 0` and `"main.tex 缺失" in out`. `:197` (`test_checkup_flags_missing_tex_dir`): rmtree's tex/, asserts `rc != 0` and `"tex/ 缺失" in out`. Both capture stdout via `contextlib.redirect_stdout` (consistent with the file's existing test style). Both verified PASS in my run.

### Minor #1 — git init two-arm → RESOLVED

`init_project.py:450-453`:
```python
except FileNotFoundError:
    report.append("⚠ git 未安装，跳过 git init（请手动 git init）")
except subprocess.CalledProcessError as e:
    report.append(f"⚠ git init 失败: {e.stderr.strip()}")
```
Splits "git not installed" from "git init refused" — the article-init pattern (article-init:426-429 per prior review). `e.stderr.strip()` is safe: the `subprocess.run` call at `:448` sets `capture_output=True, text=True`, guaranteeing `e.stderr` is a string (never None). ✓

### Minor #2 — cryptic comment → RESOLVED

`init_project.py:378`: `# write CONTRACT.md (article-init:371 mirror)`. Parses cleanly now — names what it writes and points to the mirror. The old `# <-- the write article-init's mirror has` (which read as a note-to-self left by mistake) is gone. ✓

### Minor #3 — JSON key drift → DEFERRED WITH TODO (as agreed)

`init_project.py:498`: `# TODO: align JSON key with article-init's "family_root_exists" for cross-family consumers`. The TODO sits directly above the `info` dict (the exact line a future fixer would touch) and states both the action and the reason. This is the right shape for a deferred item — it doesn't pretend parity is faithful, and it leaves a marker at the seam. ✓ (Deferred Minor #5 dual-source-of-truth and #6 unconditional-rc=0 likewise untouched, as agreed.)

---

## New issues introduced by the checkup extension?

Checked specifically for: .cls informational reporting bolted on cleanly? report line cluttered? JSON shape consistent?

### None found.

- **Report line reads clean, not cluttered.** Healthy case (`init_project.py:533-536`):
  `thesis/   ✓  tex 文件: 1  main.tex: ✓  .cls: (无 — 原生 report 类)`. Each field is labeled and meaningful: tex count (chapter files), main.tex (entry point), .cls (template class file, informational). For a real pack like thuthesis it'd render `.cls: thuthesis.cls` — short. The `(无 — 原生 report 类)` parenthetical only appears for packs without .cls and is accurate for the only shipped pack (generic-test's main.tex:1 uses `\documentclass{report}`). Not clutter — information-dense with clear delimiters.
- **Degraded-path report line is appropriately shorter.** tex/-missing case (`:519`): `thesis/   ✓  tex/ ✗ 缺失` — doesn't report main.tex/.cls because they can't exist without tex/. Correct: no fabricated "0" counts, no cascading phantom checks on a precondition that failed.
- **JSON shape is consistent where it matters, variance is defensible.** When `tex_dir` is False, the keys `tex_file_count`/`main_tex`/`cls_files` are absent (`:521` only sets `tex_dir: False`). A consumer using `.get()` is fine; direct-access would KeyError — but omitting keys that weren't checked (because the precondition failed) is the honest signal vs. fabricating `main_tex: false` (which implies it was checked and is absent). No consumer exists in this slice anyway (no orchestrator). Defensible, not an issue.
- **template-spec.md check is correctly placed outside the tex/ branch** (`:543-544`). It lives at `thesis/template-spec.md` (not `thesis/tex/`), so it's checked whenever `thesis/` exists regardless of tex/ state — a missing tex/ doesn't suppress a real template-spec.md gap.
- **No over-claim in the .cls informational note.** The fallback `(无 — 原生 report 类)` asserts a reason, but the checkup doesn't verify the pack uses the native report class. For generic-test this is true (main.tex:1), and the note is explicitly informational (not an issue/risk). When a real pack lands, it'll have a .cls and this branch won't fire. Not worth flagging — it's context, not a claim.
- **New tests follow the file's established convention** — self-contained imports inside each function body (`:179`, `:201`), matching `test_checkup_reports_misplaced_items` (`:156`). Consistent.

---

## Strengths (carried forward, still hold)

- **Compass-file factoring intact.** `BROTHER_SKILLS` (`:49`), `SKILL_DIR_CONTRACTS` (`:153`), `THESIS_CONTRACT` (`:83`), `SHARED_FILES_PLACEHOLDERS` (`:54`) remain module-level constants consumed by both `cmd_init` and `cmd_checkup`. The checkup extension added new checks against the same source of truth (main.tex is a convention every pack ships, verified against the pack dir, not a new constant) — no new duplicated logic introduced.
- **Tests verify behavior via public entry point.** Both new tests call `init_project.main([...])` and assert on return code + captured stdout + filesystem state — not internals. `test_checkup_flags_missing_main_tex` simulates a real failure mode (delete the file, run checkup, confirm it's caught). This is the right shape: it would catch a regression where the main.tex check is silently removed.
- **Pure stdlib confirmed (unchanged).** The checkup extension uses only `Path.glob` / `Path.is_file` / `Path.is_dir` / `sorted` / `", ".join` — no new imports, no non-stdlib.
- **Exec-free template handling intact.** `_weave_template` (`:332-355`) still uses only `shutil.copytree`/`copyfile`. The new checkup checks are read-only `glob`/`is_file` — no new attack surface.

---

## Issues

### Critical (Must Fix)

None.

### Important (Should Fix)

None. The prior Important #1 is resolved; no new Important issues introduced.

### Minor (Nice to Have)

1. `init_project.py:498` — the TODO for JSON key alignment (deferred Minor #3) is correctly marked, but a future fixer touching the `info` dict should note the shape also changed in this fix: `thesis` now conditionally carries `tex_dir`/`tex_file_count`/`main_tex`/`cls_files` (`:526-531`) vs article-init's flat `manuscript` shape. When aligning the `sci-skills`→`family_root_exists` key, also decide whether the `thesis` sub-dict's conditional-key pattern should match article's `manuscript` sub-dict shape. Low priority — no consumer today.

---

## Recommendations

- **No blockers for the next slice.** The foundation is sealed: checkup now honors every claim SKILL.md:154 makes, the degraded paths (missing tex/, missing main.tex) surface real issues instead of silent zeros, and the git error path gives the user the actual stderr. Downstream skills (thesis-typeset) inherit an honest audit.
- **Test coverage gap (carried, not blocking):** the `.cls` informational reporting path has no dedicated test (e.g., asserting a pack with a .cls shows its name in the report). Low value — it's informational, not an issue path — but the first real pack (thuthesis) should add one alongside the subdir-recursion test noted in tests/README.md.
- **Routing:** No runtime/concurrency/input bugs needing execution — all findings static. No security concerns (no secrets, no untrusted-input exec, `e.stderr` is safe per `:448`). No spec-compliance concerns — the checkup extension is within thesis-init's scoped role (audit only, read-only).

---

## Assessment

**Verdict**: PASS

**Reasoning**: All four landed fixes (Important #1 + Minor #1/#2/#3) are correct and verified by reading + by running the 10-test suite (10/10 PASS). The checkup extension — the riskiest change, adding main.tex verification, .cls informational reporting, and tex/-missing detection — is bolted on cleanly: the report line is information-dense but readable, the JSON shape is consistent with defensible conditional-key variance, and the degraded paths surface real issues instead of silent zeros. SKILL.md:154 now maps claim-by-claim to code lines. No new quality issues introduced. The foundation is sealed.
