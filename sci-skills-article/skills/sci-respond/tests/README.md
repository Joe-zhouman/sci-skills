# sci-respond tests

## Script unit tests (deterministic, run directly)

The two scripts have deterministic output and can be exercised without the full
skill flow. Run them against the fixtures in `fixtures/`:

```bash
# scan_neighbor: graceful on an empty/nonexistent project root
python scripts/scan_neighbor.py tests/fixtures/empty-project

# scan_neighbor: full grounding present
python scripts/scan_neighbor.py tests/fixtures/full-grounding

# check_response: a clean response → all ✓
python scripts/check_response.py tests/fixtures/response-clean.tex

# check_response: a response with intentional defects → flags each
python scripts/check_response.py tests/fixtures/response-dirty.tex
```

Verify:
- `scan_neighbor` on `empty-project`: reports every source missing, exit 0,
  does NOT crash on absent directories.
- `scan_neighbor` on `full-grounding`: reports all sources present, finds the
  r1 round, parses issue-ledger with complete fields.
- `check_response` on `response-clean.tex`: all checks `✓` (balanced pairs,
  no placeholders, macros used, cover fields present, non-floating figures).
- `check_response` on `response-dirty.tex`: each defect flagged — mismatched
  comment/response, a `[TBD]`, a bare `\textcolor`, an over-thank on a typo
  block, a banned qualifier, a `[htbp]` float, missing cover field.

## Skill acceptance checklist (subjective, run one real round end-to-end)

Run the skill against a real revision package (e.g. `assets/Response Letter#1.pdf`
as the target shape). Walk this checklist:

1. **Intake senses grounding.** `scan_neighbor.py` runs first; the skill reads
   its report before reading any individual file. Missing sources are surfaced,
   not silently assumed.
2. **Issue decomposition.** Each reviewer comment → a stable ID (`R1-Q03`) with
   surface_comment, underlying_concern, stance, safe-claim-boundary, evidence
   anchors in `issue-ledger.md`.
3. **Checkpoint stops.** The skill does NOT draft before the author locks
   strategies. Class-B issues (defend/concede/experiment/ambiguous) get a menu;
   Class-A decisions (template, tex, layout) are not asked.
4. **Solution order respects logic.** Foundational issues (claim-narrowing,
   experiment) processed before derived ones (explanation built on the new
   footing); typo/format batched last. Work order ≠ presentation order
   (presentation stays point-by-point per reviewer).
5. **Cross-reviewer overlap answered in full.** Duplicated concerns are NOT
   cross-referenced ("see R1's response") — each reviewer's section answers
   fully (systems may not show reviewers each other's sections).
6. **Self-contained responses.** Every response carries its own evidence (figure
   / data / quoted original / precise location). The independent-reviewer read
   (a fresh skeptic with only the response letter) finds nothing unclear.
7. **Acknowledgement restraint.** Typo/clarify responses have no acknowledgement
   (the redline block IS the answer). Heavy responses have ≤1 short line at the
   end. `check_response.py` acknowledgement count is low.
8. **Response Figures non-floating.** `\captionof` or `[H]`, never `[htbp]`.
   `check_response.py` float-specifier check clean.
9. **Cover page.** Three fields only (`#<rN>` / for / title / manu id),
   double-blind safe, no identity leakage.
10. **Compiles.** `pdflatex -interaction=nonstopmode -halt-on-error` produces a
    PDF in the current session; visually inspected before "done."

## Decoupling assertions (programmatic)

- grep: zero `from sci-revise`/`import sci-revise`/`from sci-write`/`from sci-draw`
  in sci-respond source — the skill reads neighbor artifacts via files/CONTRACT,
  never via code import.
- skill writes the response product into `manuscript/rN/response/` (NOT into
  `sci-skills/sci-respond/` — it has no own output dir).
- skill writes process state into the shared `sci-skills/sci-revise/` (ledger,
  change-log), NOT into `manuscript/`.
- skill never edits `manuscript/rN/tex/` (that is sci-revise's job).

TODO: scaffold evals.json + run full skill-creator-plus Test loop before ship.
