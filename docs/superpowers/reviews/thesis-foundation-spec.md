# Spec Compliance Review — thesis-foundation (re-review of capricorn's fixes)

**Reviewed**: BASE 264d898 → HEAD 4f140e7 (fix commit `4f140e7` reconciling SKILL.md with impl)
**Spec**: `docs/superpowers/specs/thesis-skill-family.md`
**Plan**: `docs/superpowers/plans/2026-08-24-thesis-foundation.md`
**Reviewer**: scorpio
**Prior review**: found M1 (degraded-mode spec generation claimed but not impl), U1 (checkup "Reports:"+JSON over-promised + no misplaced-items/git/JSON), E1 (template-spec.md duplicated in tex/). All routed to capricorn.

## Verdict
✅ Spec compliant — all 3 prior findings resolved, 3 defensible deviations acceptable. 1 new minor issue found (stale test-plan doc, introduced by the fix commit). This is Plan 1 of N (foundation); 7 prose skills remain out of scope.

## Prior findings — resolution verification

### M1 (degraded-mode spec generation) — RESOLVED
- **SKILL.md** (`sci-skills-thesis/skills/thesis-init/SKILL.md:133-137`): bullet now reads "If the spec is absent, init weaves the `.cls` but skips `thesis/template-spec.md` — downstream skills have no naming convention until one is added manually. (Generating a spec from a bare `.cls` is not done — it would require parsing the class file; the human writes the spec, same as any other template-pack author.)"
- **Impl** (`init_project.py:386-391`): `spec_src = pack / "template-spec.md" if pack else None; if spec_src and spec_src.is_file() and not spec_dst.exists(): copy`. If spec absent → no copy, no generation. `_weave_template` (`init_project.py:332-355`) copies all non-dotfile, non-spec files (incl. `.cls`); no `.cls` parser anywhere in the module (grep: 0 hits for any cls parsing).
- **Match**: SKILL.md honest ("skips", "not done — would require parsing"), impl does neither generate nor parse. Match.

### U1 (checkup over-promise + missing parity features) — RESOLVED
- **misplaced-items scan**: `list_root_candidates` (`init_project.py:460-479`) + surfaced in `cmd_checkup` (`init_project.py:541-551`), added to `issues` and `info["root_candidates"]`.
- **git status**: reported (`init_project.py:553-556`) + `info["git"]`. Deliberately NOT an issue (see deviation #2).
- **JSON block**: `print("\n--- JSON ---\n" + json.dumps(info, ...))` (`init_project.py:568`).
- **SKILL.md "filled vs placeholder" trimmed** (`SKILL.md:155-156`): "each shared file present? (...) — the agent or human judges 'filled' by reading it". Impl checks presence only (`init_project.py:519-523`); "filled" judgment explicitly delegated to human/agent. Match.
- **article-init parity verified** by reading article-init's `cmd_checkup` (`sci-skills/skills/article-init/scripts/init_project.py:479-583`): same shape — `list_root_candidates` mirror, `info` dict, `--- JSON ---` block, root-candidates as issues. One deliberate deviation (git), assessed below.
- **2 new tests** (`test_init.py:131-176`): `test_checkup_prints_json` (asserts `--- JSON ---`, `"project_root"`, `"thesis"`, `"sci-skills"` in output + rc==0) and `test_checkup_reports_misplaced_items` (drops `stray.tex`, asserts rc!=0, `"stray.tex"` and `"root_candidates"` in output). Both pass. Quality acceptable — the JSON test is string-presence rather than parsing the JSON, but it's a parity-shape test, sufficient.

### E1 (template-spec.md duplicated in tex/) — RESOLVED
- **`_weave_template` skips it** (`init_project.py:337-341`): `if src.name.startswith(".") or src.name == "template-spec.md": continue` with comment citing E1.
- **`cmd_init` copies to canonical home** (`init_project.py:386-391`): copies `pack/template-spec.md` → `thesis/template-spec.md` (only if not already exists).
- **Test asserts no dup** (`test_init.py:76-79`): `assert not (tex / "template-spec.md").is_file()` + asserts spec at `thesis/template-spec.md` carries `chapterN.tex`.
- **No leftover `tex/template-spec.md` references** in code/contracts (grep: all references resolve to `thesis/template-spec.md` or the "beside tex/" phrasing which is correct — `thesis/template-spec.md` is sibling of `thesis/tex/`).

## Defensible deviations — assessment

### Deviation 1: dropped "(and warns)" from M1 SKILL.md bullet — ACCEPTABLE
- Impl does NOT warn when spec absent (`cmd_init` silently skips the copy). SKILL.md does NOT claim a warning. Honest.
- Whether init *should* warn is a quality/spec question (taurus/libra), not a compliance gap. The impl-doc match holds.

### Deviation 2: git-status reported but NOT an issue — ACCEPTABLE & NECESSARY
- Article-init treats git-absence as an issue (`article-init/init_project.py:566-567`: `issues.append("⚠ 项目未 git init...")`).
- Thesis checkup deviates: reports git status (`init_project.py:553-556`) but never appends to `issues`.
- **Necessary**: `test_checkup_healthy` (`test_init.py`) runs `init --no-git` then asserts `checkup` rc==0. If git-absence were an issue, this test would break — the fix preserves it.
- **Justified** (docstring `init_project.py:487-491`): "`--no-git` 是一等选项，且 thesis 家族常与 article 共存于已 git 化的仓库；只报告、不报警." Honest, documented deviation from parity. Acceptable.

### Deviation 3: E1 scope-expanded to THESIS_CONTRACT prose + SKILL.md Reports bullet — ACCEPTABLE
- Moving template-spec.md's canonical location (tex/ → thesis/) required updating all references to the old path. The scope expansion is logical consistency, not gold-plating.
- **THESIS_CONTRACT** (`init_project.py:112-118`): "init 把 ... 织入 `tex/`（main.tex + 章骨架），并把 `template-spec.md` 复制到 `thesis/`" + "看 `template-spec.md`（本目录）和织入 `tex/` 的 `.cls`". Previously pointed at `tex/template-spec.md`. Correctly reconciled.
- **SKILL.md Reports bullet** (`SKILL.md:154`): split `template-spec.md` out to "`thesis/template-spec.md` present?". Correct.
- All `SKILL_DIR_CONTRACTS` already referenced `../../thesis/template-spec.md` (correct relative path from `sci-skills/<skill>/`), never `tex/template-spec.md` — no change needed there. Verified.
- Within the logical scope of E1. Acceptable.

## New issues found

### N1 (minor, NEW — introduced by the fix commit): `tests/README.md` is now stale and contradicts the test
- `sci-skills-thesis/skills/thesis-init/tests/README.md` was last touched at `c5d2cec` (before the fix); the fix commit `4f140e7` modified `test_init.py` but did NOT update `tests/README.md`.
- **(a) Stale count** (`tests/README.md:7`): "The six cases in `scripts/test_init.py`" — but there are now **8** tests (the fix added `test_checkup_prints_json` + `test_checkup_reports_misplaced_items`; `grep -cE '^def test_'` = 8). The 2 new U1 tests are undocumented in the test plan.
- **(b) Contradicts the E1 fix** (`tests/README.md:23-25`): "the test asserts those [`main.tex`, `template-spec.md`] land in `tex/`" — but after E1 the test asserts the opposite: `assert not (tex / "template-spec.md").is_file()` (`test_init.py:77`). The README now misdescribes what the test guarantees.
- **Risk**: next agent reading the test plan is misled about both the count and what `test_init_weaves_template` asserts (could "fix" the test thinking the README is the spec).
- **Fix**: update `tests/README.md` — bump count to 8, add the 2 U1 test descriptions, correct the weaves-template line to say main.tex lands in tex/ and template-spec.md lands at `thesis/` (not tex/).

## Confirmed correct (verified by reading code, not the report)

- All 8 tests pass (`python3 test_init.py`): constants, skeleton, weaves-template, idempotent, checkup-healthy, checkup-missing, checkup-json, checkup-misplaced.
- `_weave_template` recursion for real multi-file packs (`shutil.copytree` on subdirs) preserved (`init_project.py:343-348`) — the E1 skip only excludes the flat `template-spec.md`, not subdir handling.
- Idempotency holds on the E1 change: `spec_dst` copy is `if not spec_dst.exists()` (`init_project.py:389`); `_weave_template` skip-existing preserved (`init_project.py:344-354`). `test_init_idempotent` confirms.
- Glossary thesis terms present (`docs/superpowers/glossary.md:18,74,78,82,86,90` — 6 terms). No `_Avoid_` alias drift in thesis code: "manuscript" used only to contrast against the article artifact (correct), "dissertation"/"outline-then-fill"/"coordinate skills"/"dispatch skills" = 0 hits.
- Template-spec canonical location consistently `thesis/template-spec.md` across SKILL.md layout block (`SKILL.md:66`), THESIS_CONTRACT (`init_project.py:98,116-118`), all 4 SKILL_DIR_CONTRACTS (`init_project.py:171,179,210,239,268`), checkup issue text (`init_project.py:513`), family-layout reference (`references/family-layout.md:111,169`).

## Pre-existing (NOT introduced by the fix, not a regression — flagging only)

### P1 (minor, pre-existing): SKILL.md checkup Reports bullet over-specifies vs impl
- `SKILL.md:154`: "`thesis/` present? `tex/` has `.cls` + `main.tex`? which chapter files exist?"
- Impl (`init_project.py:509-511`): reports `tex_file_count` (counts `*.tex`) only; does NOT verify or report `.cls` or `main.tex` presence specifically.
- Pre-dates the fix (the `.cls + main.tex` phrasing was preserved across the reword). Not a regression. Low priority — the SKILL is describing what checkup *addresses*; the impl answers a subset. Route to taurus if tightened.

## Routing recommendation
- **N1** (stale `tests/README.md`): back to **capricorn** — doc update to match the test it describes. Small, mechanical.
- **P1** (checkup Reports bullet vs impl): **taurus** — quality/doc-impl drift, not spec compliance.
