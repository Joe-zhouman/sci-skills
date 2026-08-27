# thesis-summary tests

Test plan (run via skill-creator-plus eval loop before deployment):

1. **near-trivial consistency gate** — `scripts/check_summary.py` (the gate) +
   `scripts/test_check_summary.py` (26 stdlib cases, run `python3 test_check_summary.py`).
   Exit-code contract: 0 = consistency through; 1 = consistency issues (each printed).
   Four args: summary-map / gap-map / chapter-map / tex-dir. All 26 cases, checked
   one-by-one against the on-disk test functions:
   - `test_passes_on_settled` — passes on a settled summary-map.md (2 Callbacks
     bijection-complete against gap-map.md + 1 Commonality grounded-in 2 chapters +
     `synthesis-tex: chapter5.tex` naming an existing file);
   - `test_fails_on_missing_gap_ref` — fails on a missing `gap-ref` field;
   - `test_fails_on_malformed_gap_ref` — fails on a malformed gap-ref (`some gap` — no
     parseable Gap number, can't cross-ref);
   - `test_fails_on_multi_gap_ref` — fails on a multi-token gap-ref (`Gap 1 Gap 2` —
     two numbers; one Callback→one gap; mirror intro aries #5);
   - `test_fails_on_empty_resolved_how` — fails on an empty `resolved-how` (value =
     `none`);
   - `test_fails_on_status_pending_callback` — fails on `status=pending` (unsettled —
     gap not yet closed);
   - `test_fails_on_status_unfilled_callback` — fails on `status=unfilled` (fallback
     trace — a callback that couldn't be made, surface to the author);
   - `test_fails_on_missing_summary_map` — fails on a missing summary-map.md (summary
     not yet run — 缺席);
   - `test_graceful_on_binary_summary_map` — graceful on a binary/non-utf8
     summary-map.md — must not raise, returns a UTF-8 issue string;
   - `test_ignores_utf8_bom_in_summary_map` — ignores a UTF-8 BOM (a summary-map.md
     starting directly with `## Callback 1` + a BOM must not drop Callback 1 from
     checks; its fabricated Gap 999 is still caught — mirror intro aries #1: both reads
     use `utf-8-sig`);
   - `test_accepts_entry_headers_with_trailing_title` — accepts entry headers with a
     trailing title (`## Callback 1 (高温)` parses, the entry body isn't lost — mirror
     intro/dissect trailing-title test);
   - `test_fails_on_missing_synthesis_tex_field` — fails on a missing `synthesis-tex`
     field (template-derived filename, not hardcoded — mirror intro aries #2);
   - `test_fails_on_missing_synthesis_tex_file` — fails on a missing synthesis-tex
     file (the field names a file absent from thesis/tex/ — summary didn't produce its
     tex);
   - `test_fails_on_synthesis_tex_path_traversal` — fails on synthesis-tex path
     traversal (absolute path AND `..` traversal both rejected — the field value is
     file-content-derived, i.e. untrusted; mirror intro aries re-test);
   - `test_fails_on_missing_gap_callback` — fails on a gap without a Callback
     (bijection ABSENCE — the lock's core check: every Gap in gap-map.md must have a
     Callback entry; a skipped closure leaves a missing entry → the gate stops it);
   - `test_fails_on_duplicate_callback_for_same_gap` — fails on duplicate Callbacks for
     the same gap (two Callbacks both referencing Gap 1 — 一一对应 broken);
   - `test_fails_on_fabricated_gap_ref` — fails on a fabricated gap-ref (Gap 9 but
     gap-map.md only has Gap 1-2);
   - `test_fails_on_missing_gap_map` — fails on a missing gap-map.md (intro not yet
     run — the lock's enforce side has no data baton);
   - `test_fails_on_unreadable_gap_map` — fails on an unreadable gap-map.md
     (binary/non-utf8 — the gate reports that the gap↔Callback correspondence check is
     skipped, NOT a silent swallow; aquarius A2: sm/cm unreadable branches both had
     tests, this one didn't);
   - `test_fails_on_missing_chapter_map` — fails on a missing chapter-map.md (dissect
     not yet run — grounded-in can't cross-ref);
   - `test_fails_on_unreadable_chapter_map` — fails on an unreadable chapter-map.md
     (binary/non-utf8 — reports the grounded-in cross-ref skip, NOT a silent swallow;
     mirror intro taurus fix);
   - `test_fails_on_empty_commonality` — fails on an empty `commonality` (value =
     `none`);
   - `test_fails_on_commonality_single_chapter_grounding` — fails on single-chapter
     grounding (both groundings in Chapter 1 — <2 distinct chapters fails the
     cross-chapter floor);
   - `test_fails_on_commonality_status_pending` — fails on `status=pending`
     (Commonality — an AI candidate never author-settled must not pass; never
     auto-adopted);
   - `test_fails_on_dangling_grounded_in` — fails on a dangling grounded-in (Chapter 9
     but chapter-map.md only has ch1-2);
   - `test_ignores_entries_inside_code_fence` — **passes-ignore on entries inside a
     code fence**: a fenced `## Callback 3` does NOT count as covering Gap 3, so the
     bijection still flags Gap 3 as absent (mirror intro/dissect fence-aware parsing).

2. **the split (spec §⑥, stated honestly)** — check_summary.py is **NEAR-TRIVIAL
   CONSISTENCY, NOT a coverage gate, NOT depth, NOT a post-polish invariant (a
   write-time check).** The genuinely-new content is the Commonality confirmed
   footprint (the author depth-gate's on-disk trace — not derivable from any existing
   file) + the unfilled state (a failed callback surfaced). The gap↔Callback bijection
   is near-trivial-by-construction (gaps are ~1:1 derived from chapters — mirroring
   intro §①'s honest attribution): its real value is **absence detection** (an agent
   that quietly drops a closure leaves a missing entry → the gate stops it), NOT
   guaranteeing prose quality. `resolved-how` is a write-time self-record (derivable
   from the prose just written, not independent evidence). The gate catches **缺席**
   (summary-map.md missing / gap without a Callback) + **官僚 lapse** (fabricated Gap
   refs / dangling chapter numbers / pending residue / missing synthesis-tex file). It
   does **NOT** catch: an agent writing resolved-how with no real closure in the prose
   (prose-vs-promise — author + eval), nor a hollow 似是而非 commonality the author
   confirms anyway (attachment blindness — the Load-bearing premise's inherent
   boundary). State this plainly — do NOT overclaim a "coherence guarantee."

3. **prose is NOT script-tested** — the three-section funnel's judgment is evaluated
   via skill-creator-plus's eval loop later, not here. That judgment includes:
   - **callback-really-resolves-anchor** — does the closure prose genuinely resolve the
     gap's promise (gap wording from the intro tex vs the closure prose), NOT
     check_summary.py's near-trivial gap-ref bijection (the bijection only checks the
     Gap number matches and a resolved-how string exists, not that the prose closes
     what intro promised);
   - **commonality depth (似是而非 detection)** — is a confirmed commonality a genuine
     cross-chapter stratum, not a similarity label the author waved through;
   - **tension-flag behavior** — questions, not verdicts (each flag: the tension +
     specific evidence + a question for the author);
   - **framing-gate behavior** — ①③ gate echo → author aligns → write; runs
     UNCONDITIONALLY, no gate-skip (F2);
   - **outlook grounded in Boundary** — every ③ item hooks a spine Boundary or chapter
     limitation, no free-floating future-work boilerplate;
   - **terminology enforcement** — canonical forms from thesis-terminology-ledger.md;
   - **write-then-record discipline** — summary-map.md records what landed, not what
     was proposed.

4. **decoupling assertions (programmatic)** —
   - grep: zero sibling-skill calls in thesis-summary source (no `from thesis-` /
     `import thesis-…` in `scripts/` or `SKILL.md` or `references/`; the
     `thesis-internal material` hits are prose, and the `thesis-spine.md` /
     `chapter-map.md` / `gap-map.md` mentions are file-path reads, not Python
     imports). SKILL.md does **NOT run** intro's check_intro.py — Step 0's lightweight
     self-check on gap-map.md replaces it (avoids cross-skill script coupling; the
     `check_intro.py` strings in source are mirror-lineage comments + the explicit
     "does NOT run" statement, never an invocation);
   - summary writes `thesis/tex/<synthesis-tex>` (the template-named synthesis file,
     per template-spec.md — NOT hardcoded) + `sci-skills/thesis-summary/summary-map.md`
     (its own working dir, NOT into `thesis-intro/` or `thesis-dissect/`);
   - summary reads spine's `thesis-spine.md` + dissect's `chapter-map.md` + intro's
     `gap-map.md` + the intro tex + each `thesis/tex/chN.tex` but never writes them.

**Known limitation (honest, mirror intro's tests/README practice):** the eval loop is
prose-judgment, non-deterministic — state plainly, don't pretend the script covers
depth. check_summary.py is **near-trivial consistency, not depth coverage** (spec §①
residual) — a fabricated resolved-how with no real closure passes the gate; that is a
prose-vs-promise failure, caught only by the author + prose eval, not here.
`anchor-in-synthesis` is an **OPTIONAL audit-trail field, NOT enforced by
check_summary.py** (mirror intro's anchor-in-intro demotion — prose drifts under
polish; enforcing it would be fragile ceremony).

TODO: scaffold evals.json + run the full eval loop per skill-creator-plus before ship
(the prose surface).
