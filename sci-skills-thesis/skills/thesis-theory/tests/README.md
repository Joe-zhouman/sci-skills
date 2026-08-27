# thesis-theory tests

Test plan (run via skill-creator-plus eval loop before deployment):

1. **near-trivial consistency gate** — `scripts/check_theory.py` (the gate) +
   `scripts/test_check_theory.py` (35 stdlib cases, run `python3
   test_check_theory.py`). Exit-code contract: 0 = consistency 通过; 1 =
   consistency issues (each printed). Four args: theory-map / chapter-map /
   spine / tex-dir. All 35 cases, checked one-by-one against the on-disk test
   functions:
   - `test_passes_on_settled` — passes on a settled theory-map.md
     (extraction-outcome: confirmed — 2 Shared entries each grounded-in 2
     chapters + 1 Overlap + `theory-tex: chapter1.tex` naming an existing file);
   - `test_passes_on_waived_terminal` — passes on the waived terminal
     (extraction-outcome: waived-by-author + empty Shared/Overlap 段 + theory-tex
     present — the author's 裁最小章 footprint, NOT a vacuous pass; spec §Step 1
     fallback / aquarius T3);
   - `test_fails_on_missing_extraction_outcome` — fails on a missing
     `extraction-outcome` field;
   - `test_fails_on_invalid_extraction_outcome` — fails on an invalid value
     (`maybe` — only confirmed | waived-by-author are legal);
   - `test_fails_on_confirmed_vacuous_shared` — fails on confirmed-but-empty
     Shared 段 (vacuous-pass guard: either ≥1 confirmed component or the
     waived-by-author terminal — no silent third state);
   - `test_fails_on_waived_with_shared_entries` — fails on
     waived-with-Shared-entries (contradiction: waived = 裁最小章, no components);
   - `test_fails_on_missing_component` — fails on a missing `component`
     (Shared 1);
   - `test_fails_on_empty_instantiates_framework` — fails on an empty
     `instantiates-framework` (value = `none`);
   - `test_fails_on_shared_status_pending` — fails on `status=pending` (Shared —
     an AI candidate never author-settled must not pass; pending → confirmed,
     never auto-adopted);
   - `test_fails_on_grounding_single_chapter` — fails on single-chapter
     grounding (both groundings in Chapter 1 — <2 distinct chapters fails the
     共用 definition floor);
   - `test_fails_on_dangling_grounded_in` — fails on a dangling grounded-in
     (Chapter 9 but chapter-map.md only has Chapter 1-2);
   - `test_fails_on_missing_theory_map` — fails on a missing theory-map.md
     (theory not yet run — 缺席);
   - `test_graceful_on_binary_theory_map` — graceful on a binary/non-utf8
     theory-map.md — must not raise, returns a UTF-8 issue string;
   - `test_ignores_utf8_bom_in_theory_map` — ignores a UTF-8 BOM (a BOM-prefixed
     first Shared entry must not drop out of checks; its dangling grounded-in
     Chapter 9 is still caught — with Chapter 1 also present so the ≥2-distinct
     floor passes and the dangling branch is what fires, not the <2
     short-circuit);
   - `test_accepts_entry_headers_with_trailing_title` — accepts entry headers
     with a trailing title (`## Shared 1 (热力学基础)` parses, the entry body
     isn't lost);
   - `test_fails_on_missing_theory_tex_field` — fails on a missing `theory-tex`
     field (template-derived filename, not hardcoded);
   - `test_fails_on_missing_theory_tex_file` — fails on a missing theory-tex
     file (the field names a file absent from thesis/tex/ — theory didn't
     produce its tex);
   - `test_fails_on_theory_tex_path_traversal` — fails on theory-tex path
     traversal (absolute path AND `..` traversal both rejected — the field value
     is file-content-derived, i.e. untrusted);
   - `test_fails_on_missing_shared_ref` — fails on a missing `shared-ref` field
     (Overlap 1);
   - `test_fails_on_dangling_shared_ref` — fails on a dangling shared-ref
     (Shared 9 but the map only has Shared 1-2);
   - `test_fails_on_malformed_shared_ref` — fails on a malformed shared-ref
     (`某个组件` — no parseable Shared number, can't cross-ref);
   - `test_fails_on_overlap_chapter_not_in_chapter_map` — fails on an overlap
     chapter-ref not in chapter-map.md (Chapter 9);
   - `test_fails_on_empty_suggested_disposition` — fails on an empty
     `suggested-disposition` (value = `none` — the author's hand-resolution work
     list needs the suggestion);
   - `test_fails_on_missing_chapter_map` — fails on a missing chapter-map.md
     (dissect not yet run — grounded-in can't cross-ref);
   - `test_fails_on_unreadable_chapter_map` — fails on an unreadable
     chapter-map.md (binary/non-utf8 — reports the cross-ref 跳过, NOT a silent
     swallow);
   - `test_fails_on_chapter_map_without_entries` — fails on a readable-but-entryless
     chapter-map.md (zero `## Chapter N` entries — the grounded-in cross-ref
     would otherwise silently skip on the empty set; no-silent-skip);
   - `test_fails_on_missing_spine` — fails on a missing spine.md (theory's own
     hard dependency — the Unified-framework skeleton);
   - `test_fails_on_unreadable_spine` — fails on an unreadable spine.md
     (binary/non-utf8 — reports spine 复验跳过, NOT a silent swallow);
   - `test_fails_on_spine_pending_residue` — fails on spine `[pending?` residue
     (spine re-opened mid-write → theory-map may be stale — the aquarius T1
     mid-write backtrack window the 4th arg exists to close);
   - `test_fenced_shared_does_not_count` — a fenced `## Shared` does NOT count
     toward confirmed mode's ≥1 requirement → the vacuous-pass guard fires
     (pins fence-aware entry parsing);
   - `test_hr_closes_field_window` — a standalone `---` hr closes the entry's
     field window (fields after the hr belong to a foreign block and must not
     substitute the entry's own missing fields — summary R1 lineage);
   - `test_foreign_block_fields_do_not_substitute` — a `## 备注` block carrying
     Shared-shaped fields after Shared 1 must NOT substitute Shared 1's own
     fields (any markdown heading of ANY level terminates the entry's field
     window — summary B1 lineage);
   - `test_orphan_fence_diagnostic` — odd number of ``` lines → explicit
     orphan-fence diagnostic (fail-noisy on the structural problem itself, not a
     misleading absence issue — summary B4 lineage);
   - `test_ansi_sanitized_in_issue_output` — ANSI/control sequences in field
     values echoed into issue lines are stripped (no terminal-title rewrite /
     log-line forgery surface — summary B5 lineage);
   - `test_bad_theory_tex_value_graceful` — a theory-tex value that breaks stat
     (overlong name → OSError [Errno 36]) → graceful 值无法检验 issue, never a
     crash (stat fallback). NOTE the Python 3.13 finding: pathlib `is_file()`
     internally catches the NUL ValueError (returns False), so a NUL value never
     reaches the stat-fallback branch — the overlong-name pattern is what
     actually triggers it (mirror summary aries B2).

   Parsing/scoping rule (summary aries B1/B3/R1 lineage): fields must live
   directly under their entry header until the next heading of ANY level or a
   standalone `---` hr (both close the field window); fenced content is not
   field material; an unbalanced ``` count emits an explicit orphan-fence
   diagnostic rather than silently swallowing the rest of the file (fail-noisy
   over fail-silent).

2. **the split (spec §⑥, stated honestly)** — check_theory.py is **NEAR-TRIVIAL
   CONSISTENCY, NOT depth, NOT overlap-resolution enforcement, NOT a post-polish
   invariant (a write-time 检查).** The genuinely-new content is the Shared
   confirmed footprint (the author depth gate's on-disk trace — pending →
   confirmed, never auto-adopted) + `extraction-outcome: waived-by-author` (the
   all-candidates-vetoed fallback's on-disk terminal) + the Overlap 清单 itself
   (the author's hand-resolution work list). The Overlap 段's resolver is the
   **AUTHOR**, never a sibling skill — check_theory.py verifies structure only
   (shared-ref not dangling + chapter in chapter-map + suggested-disposition
   non-empty); resolution is NEVER enforced (blocking the skill's completion
   gate on the author's manual work would be wrong, spec §③). The gate catches
   **缺席** (theory-map.md missing / confirmed-but-empty Shared 段 — the
   vacuous-pass guard) + **官僚 lapse** (fabricated Shared/chapter refs /
   dangling grounded-in / pending residue / missing theory-tex file / spine
   re-opened mid-write). It does **NOT** catch: forced/trivial sharing past the
   author gate ("都用了误差分析" surface parallelism — attachment blindness, the
   Load-bearing premise's inherent boundary), fabricated § locations
   (prose-vs-structure), or overlap coverage completeness (absent entries —
   write-then-record discipline + eval territory, aquarius T5). State this
   plainly — do NOT overclaim a "coherence guarantee."

3. **prose is NOT script-tested** — the two-act protocol's judgment is evaluated
   via skill-creator-plus's eval loop later, not here. That judgment includes:
   - **tension-flag behavior** — questions, not verdicts (each flag: the
     tension + specific evidence + a question for the author);
   - **forced/trivial-sharing detection** — "都用了误差分析"-style candidates
     get flagged as surface parallelism, not silently proposed as depth;
   - **framing-gate behavior** — per-section gate echo (structure / component
     allocation / terms) → author aligns → write; runs UNCONDITIONALLY, no
     gate-skip;
   - **theory prose instantiates the framework** — the chapter genuinely
     narrates spine's Unified framework, not a methods-pastiche with the
     framework pasted on top (prose-vs-structure);
   - **method-vs-contribution layering** — theory lifts method/theory-layer
     sharing; no duplication of summary ②'s contribution-layer commonality;
   - **terminology canonicalization** — canonical forms from
     thesis-terminology-ledger.md;
   - **write-then-record discipline** — theory-map.md records what landed
     (Shared/Overlap entries written as prose lands), not what was proposed;
   - **overlap location truthfulness AND completeness** — the recorded
     theory-§/chapter-§ positions genuinely contain the lifted material, and
     lifted positions absent from the 清单 are caught (absent-entry failures —
     aquarius T5, explicitly NOT a mechanical check).

4. **decoupling assertions (programmatic)** —
   - grep: zero sibling-skill calls in thesis-theory source (no `from thesis-` /
     `import thesis-…` in `scripts/` or `SKILL.md` or `references/`; the
     `thesis-internal material` hits are prose, and the
     `thesis-terminology-ledger.md` mentions are file-path reads, not Python
     imports). SKILL.md does **NOT run** a sibling's check script — Step 0 does
     its own lightweight read-checks (hard-stop reads of spine.md +
     chapter-map.md); the `check_summary.py` / `check_spine.py` /
     `check_intro.py` strings in `scripts/` are mirror-lineage comments, never
     an invocation;
   - theory writes `thesis/tex/<theory-tex>` (the template-named theory chapter
     file, per template-spec.md — NOT hardcoded) +
     `sci-skills/thesis-theory/theory-map.md` (its own working dir, NOT into
     `thesis-dissect/` or `thesis-spine/`);
   - theory reads spine's `thesis-spine.md` + dissect's `chapter-map.md` + each
     `thesis/tex/chN.tex` but never writes them, and never reads
     registry/small papers/intro/summary products (spec §⑤ — thesis-internal
     material only).

**Known limitation (honest, mirror summary/spine tests/README practice):** the
eval loop is prose-judgment, non-deterministic — state plainly, don't pretend
the script covers depth. check_theory.py is **near-trivial consistency, not
depth** (spec §① residual) — a forced/trivial shared component the author
confirms anyway passes the gate; that is an attachment failure, caught only by
the author + prose eval, not here. `disposition:` is an **OPTIONAL author-fills
audit-trail field, NOT enforced by check_theory.py** (mirror intro's
anchor-in-intro / summary's anchor-in-synthesis demotion — the author may
resolve overlaps long after this skill hands off). **Overlap coverage
completeness is NOT mechanically checked** (aquarius T5 — absent-entry failures
make the author's work list look complete while a lifted position went
unrecorded; that is write-then-record discipline + eval territory, not a gate
property).

TODO: scaffold evals.json + run the full eval loop per skill-creator-plus
before ship (the prose surface).
