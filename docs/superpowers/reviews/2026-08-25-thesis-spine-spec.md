# Spec Compliance Review — thesis-spine

**Reviewed**: BASE 688534e → HEAD 56b323b (branch `thesis-spine`)
**Spec**: `docs/superpowers/specs/thesis-spine.md` (aquarius round-3 + user-approved)
**Plan**: `docs/superpowers/plans/2026-08-25-thesis-spine.md` (7 tasks)
**Reviewer**: scorpio
**Glossary**: `docs/superpowers/glossary.md` (read; no `_Avoid_` aliases found in impl)

## Verdict

✅ **Spec compliant** — no missing requirements, no extra/unrequested work, no misunderstandings. All 7 load-bearing invariants hold, verified by reading code (not the report).

## Load-bearing invariants (each verified by reading the code)

### 1. check_spine.py is COVERAGE ONLY — ✅
- `STRUCTURAL_FIELDS = ["Main line", "Unified framework", "Inter-chapter progression"]` at `sci-skills-thesis/skills/thesis-spine/scripts/check_spine.py:20` — exactly the 3 structural fields; umbrella + boundary excluded.
- No-`pending`: `check_spine.py:62` (`if PENDING_MARKER in text`).
- Sub-coverage (per-paper instantiation): `check_spine.py:75-82` — extracts `paper-[\w-]+` IDs from `## Intake`, checks each appears in `## Unified framework` body.
- Sub-coverage (per-role advance+question): `check_spine.py:84-97` — each `- role N:` line checked for `question` + `advance` substrings.
- **No reference to umbrella or Boundary anywhere in `check()`** (`check_spine.py:54-98`) — confirmed by reading the full function.
- `test_ignores_umbrella_and_boundary` at `scripts/test_check_spine.py:75-84` asserts an EMPTY umbrella + EMPTY boundary still returns `issues == []`. Ran the suite: 8/8 PASS.

### 2. tension-flagging = questions-not-verdicts + depth-INFLUENCE stated failure mode — ✅
- SKILL.md Core discipline #2 (`SKILL.md:35-38`): three-element question form, "AI never asserts 'this framework is shallow' — that is depth-gating, forbidden."
- SKILL.md Core discipline #3 (`SKILL.md:39-43`): "tension-flagging is depth-INFLUENCE, not depth-gating... named as a stated failure mode, not solved."
- SKILL.md Pervasive discipline (`SKILL.md:211-219`): reiterates depth-INFLUENCE + explicitly refutes the figN-reading "fact-check" false equivalence (aquarius round-1 load-bearing finding preserved).
- `references/writing-discipline.md:24-71`: full protocol — (a)/(b)/(c) elements, forbidden verdict forms, author disposition (`fatal → revised | dismissed → reason`), depth-INFLUENCE residual stated, figN-reading false-equivalence section (`writing-discipline.md:64-71`) ends with "**不要把 tension-flagging 写成 fact-check。**"
- **Not weakened** to figN-reading framing — the false equivalence is named and refused in both SKILL.md and the reference. ✅

### 3. umbrella = distinct depth-gated 4th field (NOT collapsed, NOT coverage) — ✅
- `SKILL.md:114` inline schema: `## Thesis-level claim (umbrella) ← one-sentence total contribution (depth-gated, NOT coverage)`.
- `SKILL.md:172-182` Step 4: "umbrella is the depth-gated 4th field, distinct from the 3 coverage-gated structural fields; NOT collapsed into the main line, which would lose its independent depth-gate."
- `references/spine-schema.md:51`: `Thesis-level claim (umbrella) | product | **depth** | ... 独立 depth-gate，不并入主线`.
- `check_spine.py:20` STRUCTURAL_FIELDS excludes umbrella (see invariant 1). ✅

### 4. no allowed-tools field — ✅
- Frontmatter (`SKILL.md:1-13`) contains only `name` + `description`. `grep "allowed-tools"` → not found. Mirrors sci-write/sci-story (prose skills). ✅

### 5. zero churn to merged foundation — ✅
- `git diff --name-only 688534e..56b323b` — all 7 changed files are under `sci-skills-thesis/`. No edits under `sci-skills/skills/thesis-init/` or `templates/thesis/`. ✅
- `thesis-init` and `templates/thesis/` untouched.

### 6. staged gates + backtrack + single rich baton + roles + default 1:1 — ✅
- **Staged gates**: `SKILL.md:96-203` (Steps 0–5, each structural stage "Stop. Author gates depth"). Steps run in dependency order: main line → framework → progression → umbrella (`SKILL.md:98-99`).
- **Backtrack**: `SKILL.md:198-203` — "revise the earlier component and re-propose downstream. Re-mark downstream candidates `pending`." Cites spec §①.
- **Single rich baton (no working-notes dir)**: `SKILL.md:72-75` — "No working-notes directory (spec §② — spine is directory-less; a single rich baton holds product + Intake + Cracks + Alternatives)". File inventory confirms: only `SKILL.md`, `references/`, `scripts/`, `tests/` — no notes dir.
- **roles + default 1:1, paper-agnostic**: `SKILL.md:162-166` — "research-chapter roles in sequence (default 1:1 with N papers)... Paper-agnostic — roles, NOT paper→chapter bindings (binding is dissect's job, 拆即写; spec §④). Dissect binds papers to roles in `chapter-map.md` (supports merge / split); bind-miss falls back to spine." ✅

### 7. no sibling-skill calls — ✅
- `grep -rnE "from thesis-(dissect|intro|theory|summary)|import thesis-(dissect|intro|theory|summary)|thesis-(dissect|intro|theory|summary)\("` over `SKILL.md` + `references/` + `scripts/` → **(none in skill source)**. The only match in the skill tree is inside `tests/README.md:33` which *documents* the decoupling rule ("no `from thesis-dissect` / `import thesis-…`") — that's the rule's prose, not an actual call. ✅
- Handoff points to thesis-dissect as a file the author reads (`SKILL.md:195-196`): "Point the author to thesis-dissect... Do NOT auto-run it — read neighbors, don't orchestrate." ✅

## Spec schema fidelity

- `references/spine-schema.md:7-42` is **verbatim** from spec L133-168 — confirmed by `diff` (VERBATIM MATCH). All 8 sections present with correct gate labels (3 coverage-gated structural / umbrella depth-gated / boundary depth-gated / Intake evidence / Cracks audit / Alternatives audit).
- SKILL.md condensed inline schema (`SKILL.md:111-118`) lists all 8 sections with correct gate tags; points to `references/spine-schema.md` for the full template.

## Workflow fidelity (spec §工作流, 6 steps)

| Spec step | SKILL.md location | Verified |
|---|---|---|
| Step 0 — Read the room (startup/resume) | `SKILL.md:125-139` | thesis-sources.md hard-stop ✓; per-paper high-level intake → `## Intake` ✓; Tex→Read, PDF→`mcp__extract__analyze_doc` ✓; template-spec.md read ✓; terminology-ledger seeded `source: thesis-spine` ✓; resume skip-to-unsettled ✓ |
| Step 1 — Main line | `SKILL.md:141-148` | pending candidate grounded in Intake ✓; tension-flags ✓; depth gate ✓ |
| Step 2 — Unified framework | `SKILL.md:150-158` | builds on confirmed main line ✓; per-paper instantiation coverage check ✓ |
| Step 3 — Inter-chapter progression | `SKILL.md:160-170` | roles default 1:1 paper-agnostic ✓; per-role advance+question coverage check ✓ |
| Step 4 — Umbrella + Boundary | `SKILL.md:172-182` | three fields settled first ✓; umbrella distinct depth-gate ✓; Boundary defined ✓ |
| Step 5 — Handoff | `SKILL.md:184-196` | runs check_spine.py ✓; umbrella NOT checked ✓; points to thesis-dissect ✓; no auto-run ✓ |
| Backtrack | `SKILL.md:198-203` | re-marks downstream pending ✓ |

## Enforcement split (spec §门)

- **Coverage (mechanical, check_spine.py)**: 3 structural fields non-empty + sub-coverage + no `[pending`. Verified at `check_spine.py:54-98`. Umbrella explicitly NOT in this layer.
- **Depth (human only)**: main line sharp? framework hollow? progression insightful? umbrella overclaim? — `SKILL.md:44-46`, `references/writing-discipline.md:14-18`. AI "cannot honestly check these" — stated at `SKILL.md:44-46`.
- **tension-flagging residual**: depth-INFLUENCE named as stated failure mode at `SKILL.md:39-43`, `writing-discipline.md:52-57`, `SKILL.md:211-219`.
- **Honest boundary (Load-bearing premise)**: decoupling prevents ABSENT not HOLLOW — `SKILL.md:224-228`, `writing-discipline.md:93-100`.

## Scope boundaries (spec §scope 边界)

- **No deep read / no tex / no chapter-map**: `SKILL.md:22-24`, `SKILL.md:76-78`. spine produces only `thesis-spine.md` + seeds `thesis-terminology-ledger.md`. ✅
- **No paper→chapter binding**: `SKILL.md:162-166` (roles, not bindings). ✅
- **Terminology ledger independence**: spine seeds `thesis-terminology-ledger.md` (thesis-prefixed), does NOT touch article's `sci-skills/sci-write/terminology-ledger.md` — `SKILL.md:55,90`. ✅

## Test acceptance (spec §测试验收)

- `check_spine.py` + `test_check_spine.py`: 8 stdlib cases — passes on settled; fails on pending / empty field / missing section / missing per-paper instantiation / role missing question / role missing advance; **passes on empty umbrella + empty boundary** (load-bearing). Ran suite: 8/8 PASS.
- CLI exit codes: pass→0, fail→1. Verified by running both cases.
- eval loop (prose) explicitly **out of scope for this plan** (plan L680) — documented as TODO in `tests/README.md:39`. Not a missing requirement. ✅

## Glossary audit

Read `docs/superpowers/glossary.md` (6 thesis terms + family principles). Checked thesis-spine source for `_Avoid_` aliases:
- `dissertation` (avoid for Thesis) → none.
- `manuscript` (avoid for Thesis) → none in source.
- `the paper` / `the dissertation` → none.
- `coordinate skills` / `dispatch skills` (avoid for read-neighbors) → none.
- `orchestrate` appears only in the canonical phrase "read neighbors, don't orchestrate" (`SKILL.md:26,196`) — this IS the glossary's canonical term (entry title "Read neighbors, don't orchestrate"), not the avoid alias. ✅
- `config` / `index file` (avoid for Compass file) → none; uses "Compass-file coupling (罗盘文件)" (`SKILL.md:61`). ✅
- `beginner-friendly` / `general-purpose` (avoid for serves-author-first) → none. ✅

## Extra / unrequested work

**None found.** Every element in the implementation traces to a spec or plan requirement:
- "Core discipline (state upfront)" section → plan Task 4 Step 1 item 2 (required).
- Inline baton schema snippet in SKILL.md → condensed reference pointing to `references/spine-schema.md` (reasonable aid, not new behavior).
- "各节职责" table in spine-schema.md → plan Task 5 Step 2 (required: "a short 'what each section is for' table").
- Verb-calibration section in writing-discipline.md → plan Task 5 Step 1 item 4 (required).
- `__pycache__/` generated by running tests — NOT tracked (`git ls-files` confirms 7 tracked files only), gitignored at repo level. Not committed churn.

## Confirmed correct (what I verified by reading)

- `check_spine.py` full source (114 lines) — coverage-only, no depth leakage.
- `test_check_spine.py` full source (118 lines) — 8 cases including the load-bearing `test_ignores_umbrella_and_boundary`.
- `SKILL.md` full source (241 lines) — all 6 workflow steps + backtrack + pervasive discipline + no allowed-tools.
- `references/writing-discipline.md` full source (100 lines) — tension protocol + depth-INFLUENCE residual + figN-reading false-equivalence refusal + pending protocol + verb calibration + honest boundary.
- `references/spine-schema.md` full source (59 lines) — verbatim spec schema + section-responsibility table.
- `tests/README.md` full source (39 lines) — coverage/eval split stated honestly; eval loop TODO is plan-sanctioned out-of-scope.
- `plugin.json` — valid JSON, name `sci-skills-thesis`, sibling to `sci-skills-article` + `sci-skills`.
- Test suite ran: 8/8 PASS. CLI exit codes: 0 pass / 1 fail.
- Decoupling grep clean on skill source (the tests/README.md match is the rule's own prose).
- Foundation churn: zero (no edits under `sci-skills/skills/thesis-init/` or `templates/thesis/`).
- Glossary aliases: none used.

## Observation (routed to aries, NOT a spec finding)

The `PENDING_MARKER = "[pending"` substring match (`check_spine.py:24,62`) is a conservative gate — it would also flag author-written content like a markdown link `[pending tasks](url)`. This is **more strict** than spec requires (fails toward catching unsettled candidates), so it is NOT a spec drift — but aries should line-by-line the script for this and other edge cases (this is surface-5 execution code per the plan's review-flow note).
