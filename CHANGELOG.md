# Changelog

## [Unreleased]

### sci-draw: Argument-driven panel planning (2026-07-19)

**Core shift: data-columns → evidence-chain.** The figure workflow now builds panels from the scientific argument, not the data schema.

- **Step 0** now requires an **evidence chain** before archetype selection: system/overview → main effect → mechanism/localization → quantification → robustness/controls → subgroup/sensitivity. Each evidence type becomes a candidate panel.
- **Step 1** rewritten: panels come from the argument ("I need to prove this claim, what evidence does that require?"), not from listing data columns ("I have group, treatment, value"). Produces 5-7 panels by default instead of 2-3.
- **Human gate question** changed from "Too many? Too few?" to "Any evidence missing that you'd want a reviewer to see?" — frames toward completeness, not pruning.
- **"Split" rule** replaced with "compose, don't split": complexity should be digested within one multi-panel figure, not sharded into separate figures. Only true split case: two independent conclusions.
- **Archetype table** expanded with `Typical panels` column (4-8 for quantitative grid, 4-7 for schematic-led composite, 5-8 for image plate + quant and asymmetric mixed-modality).
- **Reviewer-risk checklist** now includes: "Could a reviewer ask for evidence that's missing from the figure?"
- **Figure set planning** template updated with evidence chain field and 5-panel default (was 3).

### sci-draw: New reference — nature-observations.md (2026-07-19)

Added `references/nature-observations.md` (195 lines, 6 concrete layout patterns) as a pattern library for multi-panel figure layout:

| Pattern | Panels | Use case |
|---|---|---|
| Clinical/Translational Cascade | 6-8 | Trials, gene therapy, vaccines |
| Multi-Metric Comparison Grid | 4-8 | Benchmarks, method comparisons |
| Time/Longitudinal Evidence Chain | 5-7 | Disease progression, treatment response |
| Dose-Response / Concentration Series | 4-6 | Pharmacology, toxicology |
| Genomics / High-Throughput Panel | 5-8 | RNA-seq, ChIP-seq, single-cell |
| Comparative Anatomy / Multi-Group | 4-7 | Multi-species, tissue panels, cell atlases |

Each pattern includes: concrete row/col layout, panel roles and visual weights, color mapping rules, inter-panel relationships. Cross-pattern rules establish "3 panels is a figure fragment, not a complete argument" as the floor.

**Wired into**: SKILL.md Step 1 (panel planning) and Step 4 (layout reference).

### contract: Backend simplified to Python-only

Removed R backend references from `figure-contract.md` — sci-draw is Python/matplotlib only (nature-figure handles both backends).

---

## [v1.0.0] — 2026-07-18

### Initial release
- Claim-driven architecture across all skills
- Scene-based skill family (`sci-skills/`)
- Human-in-the-loop gates at key decision points
- Skills: sci-draw, sci-write, sci-polish, sci-export, sci-submit, sci-story
