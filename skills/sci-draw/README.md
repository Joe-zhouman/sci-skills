# sci-draw

Submission-grade scientific figure workflow. Produces not just a chart but a documented, reproducible, publication-ready deliverable: a plotting script, a decision log, a structured report, and the exported figure files.

## Two outputs, not one

The skill's other core function is turning the figure-making process into reusable documents. Every figure produces five files in `sci-draw/`:

```
sci-draw/
  fig1.py                 # Reproducible plotting script
  fig1-description.md     # Process log — every decision and its rationale
  fig1-report.md          # Structured report for manuscript writing and revision
  fig1.pdf                # Vector export
  fig1.png                # Raster preview
```

- **Process log** (`-description.md`): created at Step 0, filled through every step. Decisions aren't reconstructed from memory at the end — they're written down as they happen.
- **Report** (`-report.md`): distilled from the log at the final step. Clean, structured, machine-readable. Serves manuscript writing, reviewer responses, and cross-figure consistency checks.
- **Script** (`fig1.py`): anyone (including future you) can re-run it to regenerate the figure.

When returning to a figure after a break, read the files in `sci-draw/` first — not conversation memory.

## Human-in-the-loop

The workflow is designed for human judgment, not full automation. The agent advises on chart selection and catches common mistakes, but the human verifies data semantics, confirms chart choices, and does the final visual review. No script can judge whether a figure communicates its argument — that takes human eyes.

## Structure

```
sci-draw/
├── SKILL.md
├── README.md
├── requirements.txt
├── scripts/
│   ├── check_env.py          # Environment verification
│   ├── profile_data.py       # Data profiling
│   ├── setup_style.py        # Journal style configuration
│   ├── export_figure.py      # PDF + PNG export
│   ├── check_figure.py       # File compliance audit
│   ├── visual_qa.py          # Layout audit (library)
│   └── layout_tools.py       # Panel label alignment (library)
├── references/
│   ├── figure-contract.md    # Step 0 — establish what the figure must prove
│   ├── nature-2026-observations.md  # Step 0 — archetype examples from published papers
│   ├── data_profiling.md     # Step 1 — interpreting profile_data.py output
│   ├── chart_selection.md    # Step 2 — deeper examples and edge cases
│   ├── journal_specs.md      # Step 3 — detailed dimensions per journal
│   ├── plot_recipes.md       # Step 4 — chart-specific code recipes
│   ├── design-theory.md      # Step 4 — color semantics, typography, layout
│   ├── api.md                # Step 4 — palette constants and helper signatures
│   ├── chart-types.md        # Step 4 — specialized chart type patterns
│   ├── common-patterns.md    # Step 4 — reusable plotting patterns
│   ├── tutorials.md          # Step 4 — tutorial-style walkthroughs
│   ├── visual_review.md      # Step 6 — human-eye review checklist
│   ├── publication_checklist.md  # Step 7 — submission compliance checklist
│   ├── viz_pitfalls.md       # Active interception — 18 common mistakes
│   └── task-examples.md      # Worked examples of common scenarios
├── assets/
│   ├── gallery/              # Rich multi-panel figure examples
│   ├── chart-atlas/          # Chart type reference images
│   └── figures4papers/       # Demo figures with plotting scripts
└── tests/
    ├── evals.json
    └── workspace/             # Test run outputs and benchmarks
```
