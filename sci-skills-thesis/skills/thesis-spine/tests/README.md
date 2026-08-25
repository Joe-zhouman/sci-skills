# thesis-spine tests

Test plan (run via skill-creator-plus eval loop before deployment):

1. **deterministic coverage gate** — `scripts/check_spine.py` (the gate) +
   `scripts/test_check_spine.py` (8 stdlib cases, run `python3 test_check_spine.py`).
   Exit-code contract: 0 = coverage through; 1 = coverage issues (each printed).
   Cases covered:
   - passes on a settled spine (no `[pending`, all 3 structural fields filled,
     per-paper instantiations present, every role has `question` + `advance`);
   - fails on a `[pending` marker (unsettled candidate — dissect can't build on it);
   - fails on an empty structural field (`## Main line` body blank);
   - fails on a missing structural section (`## Unified framework` gone);
   - **passes on empty umbrella + empty boundary** — load-bearing: those are
     depth (human-gated), NOT coverage. The script must not gate them
     (`test_ignores_umbrella_and_boundary` is the proof);
   - fails on a missing per-paper instantiation (paper listed in `## Intake`
     but no `per-paper:` line in `## Unified framework` → contract gap);
   - fails on a progression role missing `question`;
   - fails on a progression role missing `advance`.

2. **the split (spec §⑥, stated honestly)** — coverage is deterministic
   (grep-able: `[pending` markers, structural-field emptiness, per-paper lines,
   per-role `question`/`advance` keywords), so it earns a runnable stdlib test —
   mirroring thesis-init's justified deviation (deterministic code + verifiable
   outputs). Prose is NOT script-tested: the workflow's judgment — candidate
   grounding in real evidence, tension-as-question-not-verdict, depth-influence
   naming, gate-fires-on-empty behavior — is evaluated via skill-creator-plus's
   eval loop later, not here.

3. **decoupling assertions (programmatic)** —
   - grep: zero sibling-skill calls in thesis-spine source
     (no `from thesis-dissect` / `import thesis-…`);
   - spine writes `thesis-spine.md` to `sci-skills/` (top-level shared workspace,
     NOT a spine working-notes dir);
   - spine reads neighbors' files (`thesis-sources.md`, `template-spec.md`) but
     never writes to them.

TODO: scaffold evals.json + run the full eval loop per skill-creator-plus before ship.
