# Issue ledger — r1

round: r1
status: checkpoint
strategies_locked: no

## Solution order
1. R1-Q02 [foundational] surface roughness definition → decides wording everywhere
2. R1-Q03 [derived, depends_on R1-Q02] theoretical model explanation
3. R1-Q01 [terminal] nomenclature

## R1-Q01
- reviewer: R1
- surface_comment: "Please provide nomenclature for the symbols and abbreviations used."
- underlying_concern: clarity; readers need a symbol key
- stance: agree&revise
- evidence_anchors: REVIEW:R1:Q01
- safe_claim_boundary: n/a — additive, no claim at stake
- manuscript_action: add Nomenclature section
- manuscript_location: manuscript/r1/tex/sections/method.tex, top
- revision_kind: surgical
- solution_order: 3
- depends_on: none
- safety: approved
- status: analyzed

## R1-Q02
- reviewer: R1
- surface_comment: "What is this roughness: RMS, Ra, or Rz? Unit?"
- underlying_concern: ambiguous quantity; readers can't reproduce
- stance: clarify
- evidence_anchors: REVIEW:R1:Q02 PAPER:sections/results.tex#roughness
- safe_claim_boundary: state the fact (Ra, μm); don't claim one metric is superior
- manuscript_action: change "surface roughness" → "Ra" and add "μm"
- manuscript_location: manuscript/r1/tex/sections/results.tex
- revision_kind: surgical
- solution_order: 1
- depends_on: none
- safety: approved
- status: analyzed
