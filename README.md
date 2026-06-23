# sci-draw

Submission-grade scientific figure workflow for high-impact journals.

## Design Decisions

### QA Strategy: Draft-First, User-Driven Iteration

The workflow produces a working draft, not a self-correcting final version. Pre-export checks (font clipping, tick overlap, missing glyphs) are one-shot — fix what's found, then export. The model is not trusted to self-diagnose and iterate to perfection.

**Why:** LLMs don't reliably self-correct. A "QA loop" that asks the model to find its own mistakes and fix them is performative, not effective. The user reviewing the output and requesting changes is faster and more reliable than the model pretending to audit itself.

**What this means in practice:**
- `audit_layout()` catches deterministic issues (missing glyphs, text clipping, tick overlap) before export
- Everything else is user-driven: the user sees the output, says what to change, and the agent makes those changes
- No "fix → re-export → re-check until clean" loop
- Fine-tuning happens outside this skill's workflow

### Description: Trigger-Focused, Not Tutorial

The YAML description lists concrete trigger scenarios (including Chinese phrasings) and exclusions. It does not summarize the workflow — that's what SKILL.md body is for.

## Structure

```
sci-draw/
├── SKILL.md              # Core workflow (9 steps)
├── references/           # Loaded on demand
│   ├── chart_selection.md
│   ├── viz_pitfalls.md
│   ├── plot_recipes.md
│   ├── journal_specs.md
│   └── ...
├── scripts/              # Deterministic tools
│   ├── profile_data.py
│   ├── setup_style.py
│   ├── export_figure.py
│   ├── check_figure.py
│   ├── visual_qa.py
│   └── layout_tools.py
├── assets/               # Demo figures and reference plots
└── tests/
```
