# Existence Audit — thesis-foundation plan

**net: -6 lines deletable** (plus 2 plan-breaking causal gaps — must-fix, not deletable: the plan fails as-written if executed)

Tagged against `docs/superpowers/plans/2026-08-24-thesis-foundation.md`, read through the design lens (`~/.claude/agents/refs/aquarius-lens-design.md`) + glossary + spec (`docs/superpowers/specs/thesis-skill-family.md`) + article-family source (`sci-skills/skills/article-init/`).

---

Task 5 Step 3 (cmd_init, `thesis/CONTRACT.md`): causal: `th_contract = th / "CONTRACT.md"` is assigned and never written. The else-branch does `th.mkdir(parents=True); (th/"tex").mkdir()` but no `th_contract.write_text(THESIS_CONTRACT)`. Article-init's mirror writes `ms_contract.write_text(MANUSCRIPT_CONTRACT)` — the write was dropped in translation. Task 5 Step 1 test asserts `(cwd/"thesis"/"CONTRACT.md").is_file()` → fails. Task 7 `test_init_idempotent` does `(cwd/"thesis"/"CONTRACT.md").read_text()` → FileNotFoundError before the idempotency assertion. Two tests break from one missing write. Add `th_contract.write_text(THESIS_CONTRACT, encoding="utf-8")` (idempotent-guarded, both branches).

Task 4 Step 1 vs Step 3 (`SHARED_FILES`): causal: `test_constants` asserts `init_project.SHARED_FILES` (3 asserts); the impl defines `SHARED_FILES_PLACEHOLDERS` — the name `SHARED_FILES` is never bound. AttributeError on the first constant test. The impl consistently uses `SHARED_FILES_PLACEHOLDERS` (cmd_checkup iterates it correctly), only the test uses the wrong name. Alias `SHARED_FILES = SHARED_FILES_PLACEHOLDERS` or fix the test to use the real name.

Decision-ladder (line 35) + Architecture para 3 ("Tests are a stdlib assert script... matching the repo convention"): framing: "article-init uses stdlib + README" is false. Verified at `sci-skills/skills/article-init/`: it has `tests/README.md` (a prose test PLAN — "to be run via skill-creator-plus Test loop", "TODO: scaffold evals.json + run the full Test loop (gen-eval → init-workspace → spawn → grade → aggregate)") and **no** `test_*.py`. The article convention is README + skill-creator-plus evals, not a stdlib assert script. `test_init.py` is net-new, not a mirror — and its two bugs above confirm it was never run. Either drop it and follow the eval convention (article-init's deliberate choice), or justify the deviation honestly. The "matching the repo convention" claim is the camouflage.

Task 6 Step 4 (`_weave_template`): causal: `if src.is_dir(): continue` silently drops every subdir in a pack. `generic-test` is flat (2 files), so the weave mechanism is proven only for flat packs. The plan's own follow-up (Task 11 Step 5) names thuthesis — a multi-file template *system* with config/figures subdirs. The decision-ladder line "no custom .cls needed to prove the weave mechanism" overclaims: the mechanism does not handle real packs. Either recurse into subdirs (`shutil.copytree` per subdir), or scope the contract to flat-only packs explicitly and gate the real-pack weave as a v2 task. As written, a thuthesis pack would weave its .cls + main.tex and silently lose the rest.

Task 6 Step 4 (`REPO_TEMPLATES_DIR`) + Task 6 Step 2 (test `repo_root`): hidden assumption: `Path(__file__).resolve().parents[4]` hardcodes the plugin at exactly 4 dirs deep inside the repo, so template resolution works only in-tree. Article's `templates/main/` is referenced solely in CONTRACT prose ("仓库 templates/main/ 有成熟蓝本可复制") — article-init's code never touches it. Thesis makes `templates/thesis/` a runtime path dependency read at module-load. Same repo-root location, different coupling: article's is a manual-copy pointer; thesis's is a hard path traversal. On standalone plugin install (the eventual Claude Code distribution path), `parents[4]/templates/thesis/` does not resolve. Put packs inside the plugin (`sci-skills-thesis/templates/thesis/`, resolve via `parents[3]`) so the plugin ships self-contained; repo-root `templates/` stays an article-family convenience.

Task 5 Step 3 (README.md + .gitignore) vs spec §命名避碰 (coexistence): negative-space: README.md and .gitignore are unprefixed shared files with first-writer-wins (`if not readme.exists()` / `if not gi.exists()`). thesis-* prefixed files avoid name collision, but these two don't. In a coexist project (spec acceptance: "article+thesis 共用工作区"), whichever family inits second silently loses its README content (thesis routing table + thesis-* file listing) and its .gitignore lines (thesis adds `*.aux`/`*.log`/`*.toc` that article's GITIGNORE_LINES lacks). Coexistence is asserted for 3 files, unhandled for 2. Either append-merge (not skip-if-exists) for these two, or move the routing table into a thesis-owned file (`thesis-README.md`) and drop the .gitignore write (article already covers shared lines; LaTeX products are thesis-specific and belong in a thesis-scoped ignore).

Task 5 Step 1 (`_run_init`): delete: helper defined (`def _run_init(root, *args)...`), never called — all three init tests call `init_project.main(...)` directly. 2 dead lines.

---

## Context-question check (the 5 the orchestrator asked)

1. **Collision/non-clobber?** Partially handled. thesis-* prefix on the 3 shared files + thesis-* brother dir names → no collision there. BUT README.md and .gitignore are unprefixed, first-writer-wins → coexistence gap (tagged above).
2. **stdlib tests vs repo convention?** Faithful to "no pytest" (pyproject has no pytest config), but NOT a mirror — article-init has no test script, uses README + skill-creator-plus evals. The "matching repo convention" justification is false (tagged above).
3. **Source registry by agent, not script?** Sound. init_project.py writes a schema-hint placeholder; SKILL.md assigns the interactive fill to the agent. Matches spec §⑥ and the family's "contracts over imports" (a contract gap is caught at read time). Not a finding.
4. **Native `report` class — proves the weave?** No. It proves the pack compiles and files copy, but hides two flaws the context anticipated: (a) `_weave_template` skips subdirs, so the mechanism is unproven for real multi-file packs; (b) `report` needs no external .cls resolution, so woven-file inter-dependencies (.cls found by main.tex) are never exercised (tagged above).
5. **BROTHER_SKILLS = [dissect, intro, theory, summary], spine/polish/typeset/init no dir?** Correct per spec §skill 文件夹策略. The "有文件夹" set is exactly these four; the test explicitly asserts spine/polish absence. Not a finding.

## What the plan got right

- Scope is honest: foundation-only (scaffold + init + test pack), 7 prose skills explicitly deferred.
- Division of labor (deterministic = script, judgment = agent) faithfully mirrors article-init's philosophy.
- `parents[4]` arithmetic is correct in-tree (verified).
- BROTHER_SKILLS set matches spec layout exactly.
- Idempotency intent (skip-if-exists) mirrors article-init — sound in principle (the bugs are in execution, not intent).
