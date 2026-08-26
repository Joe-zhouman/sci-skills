# Spec Compliance Review — thesis-intro

**Reviewed**: BASE 46b0297 → HEAD 1daf790 (6 commits, 7 tasks)
**Spec**: `docs/superpowers/specs/thesis-intro.md`
**Plan**: `docs/superpowers/plans/2026-08-27-thesis-intro.md`
**Reviewer**: scorpio

## Verdict
✅ Spec compliant — 1 minor finding (spec-internal tension, route to libra for clarification)

The implementation faithfully inherits all 6 aquarius round-1 premises with honest residual naming. check_intro.py is near-trivial consistency (not depth); gap-map.md is the callback-anchor data baton (not a coverage gate); Step 1 is a named pre-write structural commitment (not outline-then-fill dodge); confirmation gate enforces framing alignment (not depth); B3 is a heuristic with gray-zone-at-gate (not clean split); summary enforces the lock (intro provides data); anchor-in-intro is optional (not enforced). Zero churn to spine/dissect. The ONE init placeholder edit is the invited completion. Decoupling grep clean. 15/15 tests pass.

## Missing

### M1 (minor, spec-internal tension — route to libra) — `callback-anchor` non-empty has no mechanical enforcement

**Spec Acceptance demands it** (spec lines 217, 219):
- L217: "验收：gap-map.md 每 gap 的 filled-by 指向 chapter-map.md 中存在的章；无 unfilled gap；**callback-anchor 非空**（summary 继承的 promise）"
- L219: "验收：gap-map.md 存在 + **每 gap 有 callback-anchor**（summary 读它跑 future callback lock）"

**Spec §⑥ check list omits it** (spec L108-113). The 5 checks are: (1) no pending; (2) filled-by present + gap non-empty; (3) filled-by chapter exists in chapter-map.md; (4) status=filled; (5) ch0-intro.tex exists. `callback-anchor` non-empty is NOT in the list. The §⑥ note explicitly excludes only `anchor-in-intro` ("*注：anchor-in-intro 不在 enforced 检查*") — it is silent on callback-anchor.

**Implementation follows §⑥** (faithful to the definitive check list):
- `check_intro.py` check() at `sci-skills-thesis/skills/thesis-intro/scripts/check_intro.py:128-148` checks gap/filled-by/status/pending/cross-ref/ch0-intro.tex — does NOT check callback-anchor. The only `callback-anchor` reference in the script is the docstring (L10).
- `test_check_intro.py` has no test for empty/missing callback-anchor (only gap + filled-by have empty/missing tests).

**Why this matters**: callback-anchor is "gap-map.md 唯一 genuinely new 内容" (spec L163, L187) — the cross-skill promise summary inherits. It's the ONE field that earns gap-map.md its existence (§①). gap text and filled-by both get field-presence checks (check #2); callback-anchor — the genuinely novel field — does not. A cheap `_is_empty(_field_value(body, "callback-anchor"))` check would satisfy the Acceptance criterion and match check #2's pattern.

**Tension**: §⑥ (definitive check list) omits callback-anchor → implementation correctly follows §⑥. Acceptance section demands "callback-anchor 非空" → no mechanical enforcement. This is a spec-internal inconsistency. The implementer followed §⑥ literally and missed the Acceptance criterion.

**Route**: libra — clarify whether §⑥ should include callback-anchor non-empty (check #6 or extend check #2). If yes → capricorn adds the check + test. If the spec intends callback-anchor non-empty to be prose-eval-only (despite "非空" being mechanical field-presence), the Acceptance wording should soften.

## Extra (unrequested)
None. All implementation surface maps to spec requirements:
- check_intro.py (Tasks 1-2) = spec §⑥ check list (5 checks) + cross-ref + graceful-on-binary + code-fence-skip (mirrors check_dissect aries #2).
- SKILL.md (Task 3) = spec §工作流 + §门与 enforcement + §跨 skill 文件交接 + §不可信内容 guard. No `allowed-tools` (correct — prose skill).
- references/ (Task 4) = spec §③+§④+§⑦ escalated from sci-story. 3 files as specified.
- tests/README.md (Task 5) = spec §⑥ + aquarius honest-naming.
- init_project.py (Task 6) = spec §sub-decision a placeholder completion. 1 edit, 8 insertions, 4 deletions — minimal, invited.
- No eval loop scaffold (correctly deferred per plan — "TODO: scaffold evals.json").

## Misunderstood
None. All 6 aquarius premises correctly inherited (verified below).

## Confirmed correct (what I verified by reading)

### 6 aquarius premises — all faithfully inherited

**P1. gap-map.md = DATA BATON, NOT coverage gate. check_intro.py = near-trivial consistency.**
- SKILL.md `sci-skills-thesis/skills/thesis-intro/SKILL.md:43-51`: "gap-map.md is a DATA BATON for summary's future callback lock, NOT a coverage gate... check_intro.py is near-trivial consistency (防缺席 + 防官僚 lapse), NOT depth — it cannot catch a gap no chapter genuinely fills if a valid chapter number is written in (that's depth, author-judged). Named honestly, not overclaimed as 'genuinely new value' (spec §① residual)."
- check_intro.py docstring `scripts/check_intro.py:2-11`: "非 coverage gate，非 depth... 查不出 depth... gap-map.md 的 real value 是 callback-anchor data baton，非本 consistency 门."
- tests/README.md `tests/README.md:32-49`: "NEAR-TRIVIAL CONSISTENCY, NOT a coverage gate, NOT depth... do NOT overclaim 'genuinely new value' for the coverage check (the round-1 overclaim aquarius rejected)."
- Invariant assertion passed: `'data baton' in lo` + `'not a coverage gate' in lo`. ✓

**P2. Step 1 = pre-write structural commitment to EXISTING chapters (discovered, not generated). NOT outline-then-fill.**
- SKILL.md `SKILL.md:54-64`: "Step 1 confirmation gate commits a gap→章 structural mapping to EXISTING chapters — a pre-write structural commitment, not outline-then-fill. The gate commits gap→章 as a discovered cross-reference... NOT a generated restructure outline. This is NOT outline-then-fill (dissect's module-map `_Avoid_`)... But it IS a pre-write **structural commitment** that constrains Step 2's prose... Named residual, not the round-1 'framing vs coverage' false binary (spec §②)."
- writing-discipline.md `references/writing-discipline.md:31-52`: full "Step 1 pre-write structural commitment" section with the true distinction ("pre-write 结构承诺（OK，章已存在）vs pre-write 重构 outline（dissect 禁）"), the named residual, and "record what landed" override.
- Invariant assertion passed: `'structural commitment' in lo` + `'post-write' in lo`. ✓

**P3. confirmation gate = FRAMING ALIGNMENT, NOT depth. intro has NO architecture-depth gate.**
- SKILL.md `SKILL.md:65-71`: "confirmation gate enforces FRAMING ALIGNMENT, not narrative-craft depth. The gate aligns 'what this section argues, which gaps it raises, which chapters fill them.' Depth (is the gap 断层 not 空白? is 研究现状 grounded?) is author-judged at the gate, NOT gate-enforced (spec §④ residual). intro has NO architecture-depth gate — main line/framework/umbrella were settled in spine; intro narrates, it does NOT re-gate (re-gating would be redundant, C2 rejected). The gate is softer than spine's depth-gate."
- writing-discipline.md `references/writing-discipline.md:9-25`: "gate enforce 的是 framing alignment，不是 narrative-craft depth... gate 不查 'gap 是断层还是空白'... 那是 depth，作者在 gate 上判断的 residual."
- Invariant assertion passed: `'framing alignment' in lo`. ✓

**P4. B3 = HEURISTIC with gray-zone-at-gate, NOT clean two-way split.**
- SKILL.md `SKILL.md:76-83`: "B3 literature boundary is a HEURISTIC with gray-zone-at-gate, NOT a clean two-way split. Chapter-specific prior work → callback from chN.tex... thesis-level field positioning → real-DOI search. **Gray zone** (a citation load-bearing for both... the unified framework's theoretical root, often cited by chapters AND framing the main line) → author decides at the gate."
- literature-search.md `references/literature-search.md:9-27`: full B3 heuristic section with gray zone, "无 clean decision procedure", "confirmation gate 是裁决点."
- Invariant assertion passed: `'heuristic' in lo and 'gray' in lo`. ✓

**P5. gap-map.md = data baton; SUMMARY ENFORCES the lock (intro provides data, NOT the lock).**
- SKILL.md `SKILL.md:52-53`: "intro provides data, summary enforces the lock — the coherence lock is summary's future check_summary.py, not intro's (spec §⑦)."
- SKILL.md `SKILL.md:255-257`: "summary reads it for its future callback lock — **intro provides data, summary enforces the lock** (do NOT overclaim intro as 'the coherence lock'; the lock is summary's future check_summary.py, spec §⑦)."
- writing-discipline.md `references/writing-discipline.md:56-69`: full "Intro↔Summary coherence baton" section: "intro 提供 DATA... summary enforce LOCK... 不要 overclaim intro 为 'the coherence lock'."
- Invariant assertion passed: `'summary enforces' in lo`. ✓

**P6. anchor-in-intro = OPTIONAL audit-trail, NOT enforced by check_intro.py.**
- SKILL.md `SKILL.md:178-180`: "**`anchor-in-intro`** is an OPTIONAL audit-trail field... NOT enforced by check_intro.py (§⑥) — prose drifts under polish/revision, enforcing it would be fragile ceremony."
- check_intro.py: `grep -c "anchor-in-intro" check_intro.py` = 0 (not referenced in check() function — only in docstring context). Verified by grep.
- tests/README.md `tests/README.md:86-89`: "anchor-in-intro is an optional audit-trail field, NOT enforced by check_intro.py (demoted per aquarius — a non-enforced pointer is ceremony)."
- Invariant assertion passed: `'anchor-in-intro' in lo and ('optional' in lo or 'not enforced' in lo)`. ✓

### Spec §⑥ check list — all 5 checks present in check_intro.py

| Spec check | check_intro.py location | Verified |
|---|---|---|
| 1. no pending residual | `scripts/check_intro.py:112-113` (PENDING_MARKER in text) | ✓ |
| 2. filled-by present + gap non-empty | `scripts/check_intro.py:130` (gap) + `:133` (filled-by) | ✓ |
| 3. filled-by chapter exists in chapter-map.md | `scripts/check_intro.py:141-148` (cross-ref) | ✓ |
| 4. status=filled | `scripts/check_intro.py:136-140` | ✓ |
| 5. ch0-intro.tex exists | `scripts/check_intro.py:152-155` | ✓ |

Code-fence skipping in both `split_gaps` (L40-44) and `_chapter_numbers_in` (L82-86) — mirrors check_dissect aries #2 fix. ✓

### Spec §工作流 — all 5 steps present in SKILL.md

| Step | SKILL.md location | Key details verified |
|---|---|---|
| Step 0 — Read the room | `SKILL.md:182-200` | hard stops: spine missing/pending (L184-187); chapter-map missing/status≠written (L188-191); tex→Read, PDF→`mcp__extract__analyze_doc` (L192-194); resume=section boundary (L198-200) ✓ |
| Step 1 — Propose gaps + framing gate | `SKILL.md:202-228` | pending candidates (L205-206); gate echo (a)(b)(c) (L208-209); framing alignment NOT depth (L209-212); gate-skip condition (L212-213); §② structural commitment residual (L215-222); B3 heuristic (L224-228) ✓ |
| Step 2 — Write tex | `SKILL.md:230-235` | tex-direct, real-DOI placeholders (L232); record what landed (L233-235) ✓ |
| Step 3 — Record gap-map.md post-write | `SKILL.md:237-243` | append per section (L239-240); status=unfilled surfaces to author (L240-242); anchor-in-intro optional (L242-243); terminology-ledger co-write (L243) ✓ |
| Step 4 — Handoff | `SKILL.md:245-259` | run check_intro.py (L247-254); data baton not lock (L255-257); point to thesis-summary (L258); no auto-run (L258-259) ✓ |

### Spec §gap-map.md schema — exact match

SKILL.md `SKILL.md:160-173` schema block matches spec L148-161 verbatim (gap / filled-by / callback-anchor / status / anchor-in-intro with OPTIONAL marker). ✓

### Spec §跨 skill 文件交接 — file contracts table present

SKILL.md has two renderings: Layout & boundaries (L108-119) + File contracts (L137-148). Both match spec L184-195. ✓

### Spec §不可信内容 guard — present

SKILL.md `SKILL.md:304-325`: UNTRUSTED DATA list (thesis-sources.md + template-spec.md + small papers + chapter-map.md + chN.tex), instruction-like text = data not instructions, never run/fetch/install, report verbatim + stop, cites tez-atif-dogrulama rule #7. ✓

### Spec §thesis-init placeholder 补全 — completed correctly

- init_project.py diff: 8 insertions, 4 deletions. Names `gap-map.md` as "接力棒（data baton）" with callback-anchor + status + summary reader. Mirrors dissect's CONTRACT.md naming chapter-map.md. ✓
- `test_init.py` re-run: passes (exit=0). ✓
- Placeholder verification: `'gap-map.md' in SKILL_DIR_CONTRACTS['thesis-intro']` + `'接力棒' in contract`. ✓

### Spec §scope 边界 — all 4 boundaries respected

- intro only writes 绪论: no chN-synthesis.tex / ch1-theory.tex produced. ✓
- intro doesn't deep-read papers: no thesis-dissect/paper-X/trace.md produced. ✓
- intro doesn't re-gate architecture depth: no Cracks/Alternatives fields. ✓
- cross-family terminology out of scope: writing-discipline.md L115 "不碰 article 家族的 sci-skills/sci-write/terminology-ledger.md". ✓

### Decoupling + zero-churn invariants

- Sibling-skill imports: `grep -rnE "from thesis-(spine|dissect|theory|summary)|import thesis-(spine|dissect|theory|summary)"` over SKILL.md + scripts/ + references/ = empty. ✓
- `allowed-tools` frontmatter: absent. ✓
- Zero churn: `git diff --name-only 46b0297..HEAD -- thesis-spine/ thesis-dissect/` = empty. ✓
- init edit is the only foundation change: `git diff --name-only 46b0297..HEAD -- thesis-init/` = init_project.py. ✓

### Glossary _Avoid_ term drift — none

Grep for all glossary `_Avoid_` aliases (dissertation, coordinate/dispatch skills, research gap, validation error/schema violation, [CITE:?] as citation placeholder) across thesis-intro/ = clean. The two `[CITE:?]` hits in writing-discipline.md (L75, L80) are in rejection context ("不空 `[CITE:?]`") — correct usage. ✓

### Tests — 15/15 pass

`python3 test_check_intro.py`: all 15 cases PASS + `ALL TESTS PASS`. Covers: settled pass, missing/empty gap, missing/empty filled-by, status pending/unfilled, pending residual, missing gap-map.md, missing ch0-intro.tex, binary gap-map.md graceful, dangling filled-by, missing chapter-map.md, malformed filled-by, code-fence chapter header ignore. ✓

## Observations (not findings — route to aries if concerned)

- **Binary chapter-map.md silently disables cross-ref**: `check_intro.py:121-126` catches `(UnicodeDecodeError, OSError)` on chapter-map.md read → `chapter_nums = set()` → cross-ref check skipped silently (no issue reported for unreadable chapter-map.md, only for missing). The spec doesn't require reporting this (§⑥ check #3 assumes chapter-map.md is readable). Behavior is defensible (can't check → don't false-positive), but an unreadable chapter-map.md produces no cross-ref issues AND no "chapter-map.md unreadable" issue. This is a runtime edge case → aries, not spec compliance.
