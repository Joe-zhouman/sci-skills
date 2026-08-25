# thesis-dissect tests

Test plan (run via skill-creator-plus eval loop before deployment):

1. **deterministic coverage gate** — `scripts/check_dissect.py` (the gate) +
   `scripts/test_check_dissect.py` (14 stdlib cases, run `python3 test_check_dissect.py`).
   Exit-code contract: 0 = coverage through; 1 = coverage issues (each printed).
   Cases covered:
   - passes on a settled chapter-map.md + its tex files (2 chapters, all fields
     filled, status=written);
   - fails on a missing `framework-instantiation` (field absent);
   - fails on an empty `framework-instantiation` (value = `none`);
   - **passes when ch1 `progression-in=none`** — load-bearing: ch1 has no prior
     chapter, so `none` is the settled value, not a gap
     (`test_ch1_progression_in_none_ok` is the proof);
   - fails on a non-ch1 chapter missing `progression-in` (ch2 set to `none`);
   - **passes when last chapter `progression-out=none`** — load-bearing: the last
     chapter has no next chapter, so `none` is settled, not a gap
     (`test_last_chapter_progression_out_none_ok` is the proof);
   - fails on a non-last chapter missing `progression-out` (ch1 set to `none`);
   - fails on `status=pending` (unsettled — chapter not yet written);
   - fails on `status=stale` (backtrack-spine marked it — coverage must fail,
     dissect can't hand off a stale chapter);
   - fails on a missing tex-file (chapter references `ch1.tex` but it's absent
     from `thesis/tex/`);
   - fails on a missing `tex-file` field (no `- tex-file:` line at all);
   - passes when all referenced tex files exist (no tex-file issues);
   - fails on a missing `chapter-map.md` (dissect not yet run);
   - graceful on a binary/non-utf8 `chapter-map.md` — must not raise, returns
     a UTF-8 issue string.

2. **the split (spec §⑧, stated honestly)** — coverage is deterministic
   (grep-able: `framework-instantiation` field presence + value, `progression-in`/
   `progression-out` per chapter position, `status` keyword, `tex-file` field +
   file existence on disk), so it earns a runnable stdlib test — mirroring
   spine's justified deviation (deterministic code + verifiable outputs).
   Prose is NOT script-tested: the 拆即写 (dissect-is-write) workflow's judgment
   — in-write restructure grounding (claim-evidence hanging, IMRaD→method-results
   reorder), post-module gate behavior, fallback-spine trigger, backtrack
   cleanup — is evaluated via skill-creator-plus's eval loop later, not here.

3. **decoupling assertions (programmatic)** —
   - grep: zero sibling-skill calls in thesis-dissect source
     (no `from thesis-spine` / `import thesis-…` in `scripts/` or `SKILL.md`;
     the `thesis-spine.md` / `thesis-sources.md` mentions are file-path reads,
     not Python imports);
   - dissect writes `thesis/tex/chN.tex` + `sci-skills/thesis-dissect/chapter-map.md`
     + `sci-skills/thesis-dissect/paper-X/` notes (its own working dir,
     NOT into `thesis-spine/`);
   - dissect reads spine's `thesis-spine.md` (the baton) but never writes it;
     same for `thesis-sources.md` + `template-spec.md` (thesis-init's, read-only).

**Known limitation (markdown code-fence handling, aries round-2):** `check_dissect.py`'s
`split_chapters` skips `## Chapter N` headers inside ``` fences (so a phantom chapter in a
quoted block isn't parsed), but two CommonMark edge cases are NOT handled: `~~~` tilde fences
(treated as prose, so a `## Chapter N` inside `~~~` leaks as a phantom chapter) and nested
4-tick fences closed by an inner 3-tick. These only fire on **out-of-schema input** — the
chapter-map.md schema (above) is flat field-list markdown with no code blocks, and dissect
never produces one with code blocks. Conservative direction: fails only on malformed
out-of-schema maps, never false-blocks a valid settled map. Documented, not fixed —
elevating to full CommonMark fence handling is scope creep for a coverage gate reading flat
fields. Fix if a real chapter-map.md ever carries code blocks.

TODO: scaffold evals.json + run the full eval loop per skill-creator-plus before ship.
