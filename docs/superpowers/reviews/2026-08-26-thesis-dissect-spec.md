# Spec Compliance Review — thesis-dissect

**Reviewed**: BASE 364985c → HEAD f36be85 (branch `thesis-dissect`; 5 commits, 5 files, +760 lines)
**Spec**: `docs/superpowers/specs/thesis-dissect.md` (aquarius round-2, user-approved)
**Plan**: `docs/superpowers/plans/2026-08-26-thesis-dissect.md` (6 tasks)
**Reviewer**: scorpio
**Glossary**: read (`docs/superpowers/glossary.md`) — no `_Avoid_` aliases swapped for canonical terms.

## Verdict
✅ Spec compliant — all 7 load-bearing invariants hold; all 6 tasks match the spec; no missing requirements; no extra/unrequested work; no misunderstandings. 14/14 stdlib tests pass; CLI exit codes correct (0 pass / 1 fail).

## Missing
None. Every spec §（①–⑧）is implemented:

- §① 拆即写 (dissect-by-writing) — SKILL.md:18-23, 35-40, 181-187; restructure-discipline.md:3, 38-54
- §② chapter numbering = ordinal after non-1:1 — SKILL.md:207-213
- §③ chapter-map.md per-chapter schema — SKILL.md:131-148; check_dissect.py:73-114
- §④ non-1:1 + fallback + backtrack cleanup — SKILL.md:170-177
- §⑤ paper-X/trace.md (every paper) + binding.md (non-1:1 only) — SKILL.md:66-68, 82-83
- §⑥ restructure-discipline.md — references/restructure-discipline.md:1-128
- §⑦ terminology-ledger co-write — SKILL.md:98, 114, 190
- §⑧ test split (coverage script + prose eval) — check_dissect.py + test_check_dissect.py (14 tests) + tests/README.md

## Extra (unrequested)
None. The implementation creates exactly the 5 files the plan specified:
- `sci-skills-thesis/skills/thesis-dissect/SKILL.md`
- `sci-skills-thesis/skills/thesis-dissect/scripts/check_dissect.py`
- `sci-skills-thesis/skills/thesis-dissect/scripts/test_check_dissect.py`
- `sci-skills-thesis/skills/thesis-dissect/references/restructure-discipline.md`
- `sci-skills-thesis/skills/thesis-dissect/tests/README.md`

No scope creep into foundation/spine/init (verified: `git diff --name-only 364985c..f36be85 -- sci-skills/skills/thesis-init/ sci-skills-thesis/skills/thesis-spine/` = empty).

## Misunderstood
None.

## Confirmed correct (what I verified by reading code + running tests)

### Load-bearing invariant 1: 拆即写 = dissect-by-writing (spec §①)
- SKILL.md:22, 38 — `**There is no module-map.md file**` stated explicitly in core discipline.
- SKILL.md:181-187 — workflow Step 1.3: "Per-module dissect-by-writing + post-module gate (拆即写, no pre-write outline)... write its tex (dissection IS writing: IMRaD→method-results restructure happens in-write...) → author gates AFTER the module's tex is written (post-module gate)".
- restructure-discipline.md:3 — `**不是 pre-write outline**` (NOT a pre-write outline).
- restructure-discipline.md:53 — `不产 module-map.md 文件` (does not produce module-map.md file).
- restructure-discipline.md:101-111 — "What this reference is NOT" section explicitly forbids pre-write outline.
- All 15 grep hits for "module-map" are in negative/prohibitive context ("no module-map", "not via pre-write module-map", "不产 module-map"). No module-map.md file is produced.
- File contracts (SKILL.md:62-68) list produced files: chN.tex + chapter-map.md + trace.md + binding.md — no module-map.md.
- **No regression to outline-then-fill.** Post-module gate is AFTER tex written, not pre-write.

### Load-bearing invariant 2: check_dissect.py COVERAGE ONLY (spec §门与 enforcement)
- check_dissect.py:2-7 — docstring states `**不查 depth/grounding**` (does NOT check depth/grounding).
- check_dissect.py:81-114 — checks ONLY: framework-instantiation non-empty, progression-in (ch1 excepted), progression-out (last excepted), status=written, tex-file exists. No restructure-quality check, no claim-evidence check, no grounding check.
- SKILL.md:51-54, 198-202 — explicitly states "Depth (restructure quality) and grounding (claim-evidence) are NOT checked".
- tests/README.md:32-40 — states the split honestly: "Prose is NOT script-tested".

### Load-bearing invariant 3: ch1/last progression exceptions (spec §门与 enforcement)
- check_dissect.py:87 — `if ch_num > 1:` skips progression-in check for ch1 (first chapter by position).
- check_dissect.py:93 — `if ch_num < total:` skips progression-out check for last chapter.
- `_is_empty()` (check_dissect.py:53-58) treats None/""/none-tokens as empty — so non-ch1 with `progression-in: none` correctly fails.
- test_check_dissect.py:66-72 — `test_ch1_progression_in_none_ok` proves ch1 none is OK.
- test_check_dissect.py:83-89 — `test_last_chapter_progression_out_none_ok` proves last none is OK.
- test_check_dissect.py:74-81 — `test_fails_on_non_ch1_missing_progression_in` proves ch2 none fails.
- test_check_dissect.py:91-98 — `test_fails_on_non_last_missing_progression_out` proves ch1 (non-last) none fails.
- All 4 edge-case tests pass.

### Load-bearing invariant 4: No allowed-tools field
- SKILL.md frontmatter (1-14): only `name` + `description`. No `allowed-tools`.
- grep confirmed: 0 matches for "allowed-tools".

### Load-bearing invariant 5: Zero churn to foundation + spine
- `git diff --name-only 364985c..f36be85 -- sci-skills/skills/thesis-init/ sci-skills-thesis/skills/thesis-spine/` = empty.
- All 5 new files are under `sci-skills-thesis/skills/thesis-dissect/`.

### Load-bearing invariant 6: Chapter numbering = ordinal after non-1:1 (spec §②)
- SKILL.md:209-212 — "chN = chapter ordinal AFTER merges/splits are applied (not spine role position — non-1:1 breaks role-position: merge role 1+2 → ch1, role 3 → ch2 not ch3; split role 1 → ch1+ch2, role 2 → ch3). dissect traverses papers in spine progression-role order, but chapter numbers increment by actual output."

### Load-bearing invariant 7: No sibling-skill calls
- grep `from thesis-(spine|intro|theory|summary)|import thesis-(spine|intro|theory|summary)` across SKILL.md + scripts/ + references/ = 0 matches.
- SKILL.md:76 — "Compass-file coupling (罗盘文件) — no skill calls a sibling skill; handoff is via on-disk files."
- SKILL.md:204 — "Do NOT auto-run — read neighbors, don't orchestrate."

### Test suite execution
- `python3 test_check_dissect.py` → 14 `: PASS` lines + `ALL TESTS PASS`, exit=0.
- CLI pass case: `✓ coverage 通过`, exit=0.
- CLI fail case (status=pending): prints `✗ Chapter 1 status=pending`, exit=1.

### Spec acceptance criteria (all met)
1. IMRaD→modular restructure + in-write (§Acceptance 1) — restructure-discipline.md covers method-results pairing + question→method→results triple.
2. 拆即写 no two steps (§Acceptance 2) — no module-map.md; post-module gate after act.
3. Inter-chapter progression (§Acceptance 3) — progression-in/out checked.
4. Framework instantiation (§Acceptance 4) — framework-instantiation non-empty checked.
5. non-1:1 handling (§Acceptance 5) — binding.md only for non-1:1; backtrack marks stale.

### Spec scope boundaries (all respected)
- No `ch0-intro.tex` / `chN-synthesis.tex` / `ch1-theory.tex` produced.
- No new figure files.
- No edits to article-family `sci-skills/sci-write/terminology-ledger.md` — only `thesis-terminology-ledger.md` co-write.

### Glossary compliance
- 拆即写 (dissect-is-write) — used as canonical term throughout; `outline-then-fill` correctly flagged as `_Avoid_` (SKILL.md:20, 37).
- Compass file (罗盘文件) — used correctly (SKILL.md:76).
- Contract gap — used correctly (restructure-discipline.md:77-99); `_Avoid_: validation error, schema violation` not used.
- Real-DOI placeholder — used correctly (SKILL.md:187, 228).
- Architecture-level claim — concept respected (depth = human-gated; coverage = mechanical).
- Read neighbors, don't orchestrate — used correctly (SKILL.md:27, 204).
- No `_Avoid_` aliases substituted for canonical terms.
