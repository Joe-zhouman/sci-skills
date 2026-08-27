# Spec Compliance Review — thesis-summary

**Reviewed**: BASE 503f204 → HEAD 054b7af (7 commits, 7 tasks)
**Spec**: `docs/superpowers/specs/thesis-summary.md`
**Plan**: `docs/superpowers/plans/2026-08-27-thesis-summary.md`
**Reviewer**: scorpio

## Verdict
❌ Issues found — 1 minor (1 missing, 0 extra, 0 misunderstood)

The load-bearing promises all landed and were verified by reading, not by trusting the
report. §⑥ checks 1–6 are implemented in `check_summary.py` exactly as specified (status-field
pending, gap↔Callback bijection with absence+fabricated detection, resolved-how/filled,
grounded-in ≥2 distinct chapters in chapter-map, synthesis-tex existence+path guard, BOM/fence/
unreadable family mirrors) — 26/26 tests pass (run, not assumed). F1–F6 honest naming sits in
all three required places (docstring / SKILL.md / tests/README); the plan's 9 phrase assertions
P1–P9 pass. Workflow Step 0's three hard stops + lightweight self-check (no sibling scripts),
the schema (verbatim inline, `anchor-in-synthesis` optional-unenforced, 展望 no baton entry),
the init placeholder completion (exactly the two invited edits, F5 bases in the commit message),
zero churn to spine/dissect/intro (empty diff), and every scope boundary (no literature-search,
no ch1-theory.tex, no registry/small-paper reads, no sibling-script runs) — all confirmed.
The single finding is one unlanded item from spec §⑧'s mirror list.

## Missing

### M1 (minor) — "targeted revision" (spec §⑧ 直接镜像 item 5, spec 防带病推进 "(targeted)") appears nowhere in the skill

**Spec demands it twice**:
- spec §⑧ line 101, 直接镜像（照搬）list: "per-section confirmation gate（①③段）；fuse-claim-into-opening（…）；verb calibration（…）；real-DOI 纪律（引了才挂 placeholder）；**targeted revision**。" — the fifth of five sci-story mirrors claimed as 照搬.
- spec 防带病推进 line 207: "①段 framing 错回 gate 重对齐（**targeted**）" — the qualifier describes the re-alignment path.

**Implementation**: `grep -c targeted` = 0 in all three prose artifacts —
`sci-skills-thesis/skills/thesis-summary/SKILL.md`, `references/writing-discipline.md`,
`references/synthesis-guide.md`. The other four §⑧ mirror items all landed (confirmation gate:
SKILL.md:234-243 + writing-discipline.md:23-43; fuse-claim-into-opening: SKILL.md:236-238 +
synthesis-guide.md:17-21; verb calibration: writing-discipline.md:108-123; real-DOI 纪律:
writing-discipline.md:93-104 + SKILL.md:271-274). "Targeted revision" — revise the affected
section at the gate on a framing error, not a wholesale rewrite — is stated nowhere.

**Mitigation (why minor)**: the acceptance row's own 验收 ("各 fallback 路径有落盘痕迹
（unfilled / pending）") passes — unfilled at SKILL.md:189/245-247, pending at SKILL.md:258-262;
the plan itself omitted the item from Task 4's prescribed content (plan gap carried through,
not implementer improvisation); §⑧ is attribution-accounting rationale, not a feature list.
But spec-vs-artifact it is a stated mirror that never landed.

**Fix**: one clause in `references/writing-discipline.md` §①③ framing gate (after line 43)
— e.g. "a framing error found at the gate re-aligns the affected section targeted (re-gate +
revise that section), never a wholesale rewrite of the chapter (sci-story targeted revision,
spec §⑧)." Route: capricorn (one line).

## Extra (unrequested)

None. Items that could look extra, verified as in-spec:
- duplicate-Callback + one-Callback-one-gap checks (`check_summary.py:103-109, 163-166`) —
  within spec §⑥-2 "gap↔Callback **一一对应**" (bijection = both directions); tested at
  `test_check_summary.py:268-275, 125-131`.
- missing/unreadable gap-map/chapter-map issue strings (`check_summary.py:127-149`) — required
  by §⑥-6 "不可读文件处理" and preconditioned by §⑥-2/§⑥-4; tested at
  `test_check_summary.py:286-319`.
- `_NONE_TOKENS` (`check_summary.py:32`) — verbatim mirror of `check_intro.py:27` (family
  convention for "非空").
- 7a2e042's message-format fix (`check_summary.py:193`, list-repr → joined numbers) — minimal
  fix required for `test_fails_on_dangling_grounded_in` to pass; disclosed in the commit body.

## Misunderstood

None found.

## Confirmed correct (what I verified by reading / running)

**§⑥ 检查项 1–6 vs `check_summary.py`**:
1. pending via status field only — `CALLBACK_SETTLED`/`COMMONALITY_SETTLED` per-entry checks at
   `check_summary.py:29-30, 169-173, 195-199`; `grep 'pending?'` over script+SKILL.md = 0 hits
   (F3: no marker grep).
2. gap↔Callback bijection both directions — absence (`check_summary.py:176-179`, the lock's
   core 缺席检测), fabricated Gap ref (`:161-162`), duplicate (`:163-166`).
3. resolved-how non-empty + status=filled; unfilled fails (`:167-173`).
4. commonality non-empty + grounded-in ≥2 distinct chapters (`:189-191`, set-dedup) + all in
   chapter-map (`:192-194`) + status=confirmed, pending fails (`:195-199`).
5. synthesis-tex top-level field + file exists in thesis/tex + absolute/`..` rejection
   (`:202-212`).
6. BOM `utf-8-sig` (`:118, 131, 143`), fence-aware splitting (`:35-61`) and fence-aware header
   numbers (`:85-100`), graceful unreadable handling (`:119-122, 133-135, 145-147`).
- Tests: 26/26 PASS (run at HEAD). README's 26-case list is set-identical to the 26 `test_*`
  functions (diffed programmatically).

**F1–F6 honest naming, all three landing sites**:
- docstring F1+F6 (`check_summary.py:2-15`): near-trivial/非 depth/write-time/genuinely-new
  accounting/near-trivial-by-construction/缺席检测/resolved-how self-record — all present.
- SKILL.md: plan Task 3 Step 2's needle list + P1–P9 assertions — **run at HEAD, all pass**
  (enforce/provides-data, near-trivial+absence, unconditional+no-gate-skip, never-auto-adopt+
  tension-flags, write-time, ≥2 floor, no cross-skill edit, no replay, real-DOI). `gate-skip`
  appears only inside the F2 rejection (SKILL.md:63-67, 299; writing-discipline.md:39-43).
- tests/README: the near-trivial/write-time split (§2, lines 75-90) + known limitation incl.
  eval non-determinism and `anchor-in-synthesis` optional-unenforced (lines 126-133).

**Workflow Step 0–4 vs SKILL.md:163-293**:
- Three hard stops: spine missing/empty/pending-field (SKILL.md:210-213); chapter-map missing /
  any status≠written incl. stale (:214-216); gap-map missing = "enforce side has no data baton"
  (:217-218).
- Lightweight gap-map self-check, explicitly NOT running check_intro.py (:219-222); the only
  `check_intro.py` strings in the skill are the "does NOT run" statements (SKILL.md:220;
  tests/README.md:116-119) — no invocation anywhere.
- tex→Read / PDF→`mcp__extract__analyze_doc` (:227-229); resume = section boundary
  (:165-169, 230-232).
- Step 1 gate echo (a)(b)(c) + unconditional + unfilled fallback (:234-247); Step 2 pending
  candidates + tension-flags questions-not-verdicts + author settle + never auto-adopt
  (:249-262); Step 3 Boundary/limitation grounding + F4 DOI boundary (:264-274); Step 4 runs
  the 4-arg check, points to thesis-theory, does NOT auto-run (:276-293).

**Schema (SKILL.md:171-206) vs spec §summary-map.md schema (spec lines 123-149)**: verbatim —
synthesis-tex / gap-ref / resolved-how / status / anchor-in-synthesis (OPTIONAL, not enforced —
no check for it in the script) / commonality / grounded-in / confirmed; 展望 has no baton entry
(SKILL.md:203-204).

**Init placeholder completion (the ONE foundation edit)**: `git diff 503f204..HEAD --
sci-skills/skills/thesis-init/scripts/init_project.py` shows exactly the two prescribed edits —
文件清单 names `summary-map.md` (placeholder "随设计定" line deleted) and the 读清单 rewrite
(thesis-sources.md line removed, gap-map.md line added). `test_init.py` exits 0; woven-CONTRACT
temp-dir check returns WOVEN-OK (summary-map+gap-map present, registry line gone). Commit
054b7af's subject (245 chars, verified via Python — the "..." seen in log display is a display
artifact) states both F5 bases: "name summary-map.md (literal invitation) + read-list rewrite
(add gap-map.md baton, drop registry — invited-by-design; resolves family-spec
交接表-vs-summary-row conflict, take the narrow side)".

**Zero churn**: `git diff 503f204..HEAD -- thesis-spine/ thesis-dissect/ thesis-intro/` = empty.
Range touches only `thesis-summary/**` + `init_project.py` + `docs/superpowers/**` design
records.

**Scope boundaries**: no `literature-search`/`ch1-theory` strings anywhere in the skill
(grep = 0); `references/` contains exactly the 2 prescribed files; registry/small-papers appear
only in "does NOT read" statements (SKILL.md:32, 138-140); scripts import only stdlib
(`re, sys, pathlib, importlib`).

**Glossary**: no `_Avoid_` aliases (`research gap`, `outline-then-fill`, `coordinate/dispatch
skills` — grep = 0). Narrative gap / architecture-level claim / compass-file / real-DOI
placeholder all used canonically.

**Design records**: spec + plan + 3 review docs committed (da6b0b1) in house style (dated
headers, lens/reviewer attribution), matching the `*-spec.md` review lineage format.

## Watch item (not a violation)
SKILL.md:201-202 and :289-290 call the Callback 段 "the lock's enforcement record". F1's ban
(plan line 41) is on labeling the **summary-map.md file** "LOCK-ENFORCEMENT RECORD"; the file
is labeled "写后 baton (DATA)" (SKILL.md:175), the near-trivial accounting precedes both uses
(SKILL.md:43-53), and "coherence guarantee" is explicitly disclaimed (SKILL.md:318).
Segment-level naming after honest accounting = compliant; recorded so the next reviewer
doesn't re-litigate it.

---

## Addendum — M1 re-verification (post-fix)

**Fix commit**: 94c4121 (HEAD at re-check) — `thesis-summary: scorpio M1 fix — targeted-revision discipline added to ①③ framing-gate section (spec §⑧ mirror item 5)`
**Scope of fix**: 1 file, +6 lines (`references/writing-discipline.md` only; `git diff 94c4121..HEAD` = empty — nothing else changed).

**M1 closed — verified by reading the diff and the on-disk file**:
- `references/writing-discipline.md:44-49` adds "**Targeted revision after the gate.**" —
  exactly where prescribed (end of the ①③ framing-gate section, after the UNCONDITIONAL
  paragraph at :39-43, before `### ② spine depth gate` at :51).
- Content carries both spec anchors M1 cited: spec §⑧ 直接镜像 item 5 ("direct mirror from
  sci-story's targeted-revision discipline") + spec Acceptance 防带病推进 ("framing 错回 gate
  重对齐, targeted 不全文重写"), and states the behavior itself (fix what was flagged at the
  gate — a wrong closure ① / a bad hook ③ — do not rewrite wholesale; the echo-aligned rest
  stands). Scope matches the ①③ gate section it lives in.
- M1's grep evidence reversed: `targeted` 0→3 hits in `writing-discipline.md` (SKILL.md /
  synthesis-guide.md remain 0 — correct; the discipline is write-time gate behavior, this
  reference is its home).
- No new issues introduced: no extra behavior, no gate-skip implication (post-gate revision
  discipline, not a skip condition), no glossary drift.

## Final Verdict
✅ Spec compliant — M1 fixed and verified at `references/writing-discipline.md:44-49` (commit 94c4121). All other findings unchanged from the original review (0 missing, 0 extra, 0 misunderstood; watch item stands as recorded, non-violation).
