# thesis-intro tests

Test plan (run via skill-creator-plus eval loop before deployment):

1. **near-trivial consistency gate** — `scripts/check_intro.py` (the gate) +
   `scripts/test_check_intro.py` (17 stdlib cases, run `python3 test_check_intro.py`).
   Exit-code contract: 0 = consistency through; 1 = consistency issues (each printed).
   Cases covered:
   - passes on a settled gap-map.md + its chapter-map.md + ch0-intro.tex (2 gaps,
     all fields filled, status=filled, filled-by chapters resolve);
   - fails on a missing `gap` field (field absent);
   - fails on an empty `gap` (value = `none`);
   - fails on a missing `filled-by` (field absent);
   - fails on an empty `filled-by` (value = `none`);
   - fails on a missing `callback-anchor` (field absent — the field that earns
     gap-map.md its existence per §①; presence is mechanical, not depth);
   - fails on an empty `callback-anchor` (value = `none`);
   - fails on `status=pending` (unsettled — gap not yet filled);
   - fails on `status=unfilled` (contract gap — no chapter fills this gap);
   - fails on a pending residual (`[pending?` marker anywhere — unsettled candidate,
     mirror check_spine/check_dissect);
   - fails on a missing gap-map.md (intro not yet run — 缺席);
   - fails on a missing ch0-intro.tex (intro didn't produce its tex);
   - graceful on a binary/non-utf8 gap-map.md — must not raise, returns a UTF-8
     issue string;
   - fails on a dangling filled-by (gap references Chapter 9; chapter-map.md only
     has ch1-2 — fabricated/dangling chapter number);
   - fails on a missing chapter-map.md (dissect not yet run — intro can't cross-ref);
   - fails on a malformed filled-by (`some chapter` — no parseable chapter number,
     can't cross-ref);
   - **passes-ignore on chapter headers inside a code fence** — a `## Chapter 99`
     inside a ``` fence in chapter-map.md is NOT counted as a valid chapter, so a
     gap `filled-by: Chapter 99` still fails cross-ref (mirror check_dissect aries #2).

2. **the split (spec §⑥, stated honestly)** — check_intro.py is **NEAR-TRIVIAL
   CONSISTENCY, NOT a coverage gate, NOT depth.** gaps ~1:1 derived from chapters
   by construction (glossary Narrative gap "typically one per body chapter") →
   coverage near-trivial. The gate catches **缺席** (gap-map.md missing) + **官僚
   lapse** (fabricated chapter numbers / dangling filled-by / pending residual /
   missing ch0-intro.tex). It does **NOT** catch depth — a gap no chapter genuinely
   fills but with a valid chapter number written in passes the gate, is a depth
   failure (author-judged, prose eval). gap-map.md's real value is the
   `callback-anchor` data baton for summary (summary inherits the promise), NOT
   the coverage check. State this plainly — do NOT overclaim "genuinely new value"
   for the coverage check (the round-1 overclaim aquarius rejected: a dangling
   filled-by can only arise from an agent fabricating a chapter number, since intro's
   gaps are by construction derived from chapter-map.md's chapters). The
   consistency check earns a runnable stdlib test (deterministic + grep-able:
   `gap`/`filled-by` field presence + value, `status` keyword, `filled-by` chapter
   number ∈ chapter-map.md's `## Chapter N` set, `ch0-intro.tex` file existence) —
   mirroring spine/init/dissect's justified deviation (deterministic code +
   verifiable outputs).

3. **prose is NOT script-tested** — the hybrid workflow's judgment is evaluated via
   skill-creator-plus's eval loop later, not here. That judgment includes:
   - **gap 断层-not-空白** — is the gap a genuine discontinuity between chapters,
     not a cosmetic blank (author + AI judgment, not grep-able);
   - **B3 heuristic gray-zone callback-vs-search** — when a gap could callback an
     existing chapter vs. demand a real-DOI literature search (gray zone has no
     clean two-way split — round-2 修 aquarius);
   - **confirmation-gate framing-alignment behavior** — propose narrative framing
     → author aligns → write prose; the gate enforces framing alignment, NOT depth
     (depth is author-judged residual, softer than spine's tiered depth-gate);
   - **gap→章 depth grounding** — is the chapter genuinely filling the gap, NOT
     check_intro.py's near-trivial cross-ref (cross-ref only checks the chapter
     number exists in chapter-map.md, not that the chapter substantively fills the
     gap);
   - **real-DOI discipline** — `[DOI: ...]` placeholders for real citations, not
     fabricated;
   - **write-then-record gap-map.md** — gap-map.md is recorded from settled tex,
     not a pre-write outline (mirror dissect's write-then-record baton).

4. **decoupling assertions (programmatic)** —
   - grep: zero sibling-skill calls in thesis-intro source
     (no `from thesis-spine` / `from thesis-dissect` / `import thesis-…` in
     `scripts/` or `SKILL.md` or `references/`; the `thesis-spine.md` /
     `chapter-map.md` mentions are file-path reads, not Python imports);
   - intro writes `thesis/tex/ch0-intro.tex` + `sci-skills/thesis-intro/gap-map.md`
     (its own working dir, NOT into `thesis-spine/` or `thesis-dissect/`);
   - intro reads spine's `thesis-spine.md` (the baton — narrate, not re-gate) +
     dissect's `chapter-map.md` (locate body chapters + gap→fill basis) but never
     writes them.

**Known limitation (honest, mirror dissect's tests/README practice):** the eval
loop is prose-judgment, non-deterministic — state plainly, don't pretend the
script covers depth. check_intro.py is **near-trivial consistency, not depth
coverage** (spec §① residual) — a gap that no chapter genuinely fills but carries
a valid chapter number passes the gate; that is a depth failure, caught only by
the author + prose eval, not here. `anchor-in-intro` is an **optional audit-trail
field, NOT enforced by check_intro.py** (demoted per aquarius — a non-enforced
pointer is ceremony; check_intro.py verifies `gap` + `filled-by` + `callback-anchor` +
`status` + `filled-by` cross-ref + `ch0-intro.tex` existence, not `anchor-in-intro`).

TODO: scaffold evals.json + run the full eval loop per skill-creator-plus before
ship (the prose surface).
