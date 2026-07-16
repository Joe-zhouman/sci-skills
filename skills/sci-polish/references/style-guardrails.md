# Style Guardrails

Mechanical and stylistic checks applied after the main rewrite. These refine prose and correctness, not override the writing strategy.

## Academic style

- Prefer cautious, precise prose over conversational confidence
- Avoid contractions (don't → do not)
- Avoid rhetorical questions in polished manuscript prose
- Define abbreviations on first use
- Use British spelling by default if the target is Nature-style prose
- Keep figure legends concise (≤ 300 words for Nature-style)
- Keep titles ≤ 75 characters including spaces (Nature-style)

## Articles

Common checks:

- First mention of a singular count noun: "a" or "an"
- Later mention of the same item: "the"
- Generic plural: usually no article
- Unique entity: often "the"
- Abstract nouns used generally: often no article

Typical repair: "The hypoxia induces ..." → "Hypoxia induces ..."

## Numbers and units

### LaTeX: use `siunitx`

All quantities with units must use `siunitx` — never raw text.

```latex
\usepackage{siunitx}
\sisetup{
  mode = text,
  detect-all,
  input-decimal-markers = {.},
  group-digits = integer,
  group-four-digits = true,
  inter-unit-product = \,,         % thin space, not \cdot
  per-mode = reciprocal,           % m·s⁻¹, not fraction
  exponent-product = \times,
  input-exponent-markers = {e},
  uncertainty-mode = separate,
  range-units = single,
}

% OK:
\qty{25}{\cm}
\qty{3.2e5}{\J\per\mol\per\K}   % → J·mol⁻¹·K⁻¹
\qty{37.0 +- 0.5}{\celsius}
\ang{90}

% Wrong:
25 cm, 3.2 s, 90°, 25cm
```

**Key rules**: per-mode = reciprocal (negative exponent), inter-unit-product = thin space (no `\cdot`), scientific notation with `\times`.

### Markdown outputs (drafting stage, etc.): terminology ledger

When working in markdown (not LaTeX), `siunitx` is not available. Record every unit-form convention in `sci-skills/sci-write/terminology-ledger.md`:

| Category | Term / variants | Canonical form | Source | Notes |
|---|---|---|---|---|
| Unit | cm / cm. / centimeter | cm | polish-discovered | space before unit: `25 cm` |
| Unit | °C / deg C / celsius | °C | polish-discovered | |
| Unit | s / sec / second | s | polish-discovered | |

Same unit, same form, every section. Next time the tex is compiled, convert to `siunitx`.

## Academic register

- Avoid spoken fillers and weak evaluative language
- Use "we" only when it suits the discipline and document type
- Keep nominalisation useful, not excessive
- Keep prose impersonal where appropriate, but do not force lifelessness

## Sentence and paragraph mechanics

- Each sentence should express one main proposition
- Dependent clauses must stay attached to a main clause
- Do not join two independent clauses with only a comma
- Each paragraph needs a controlling idea and supporting material
- Avoid sentence fragments introduced by "although" or "whereas"

## AI-prose anti-patterns

These are good-writing rules that happen to be disproportionately violated in AI-generated text. Apply them during polish — silently fix, don't lecture the user.

### Throat-clearing openers

Delete on sight. Cut to the point.

| Pattern | Fix |
|---|---|
| "It is important to note that..." | Delete. If it's important, the content speaks for itself. |
| "It is worth mentioning that..." | Delete. Same. |
| "In order to..." | "To..." |
| "It should be noted that..." | Delete. Just note it. |
| "In today's rapidly evolving..." | Delete. Timestamped cliché. |
| "This serves as a testament to..." | "This demonstrates..." or state the evidence directly. |
| "When it comes to..." | Start with the subject: "X shows..." |
| "With that being said..." | "However" if contrast is intended, else delete. |

Also: sentences that announce what the paper is doing instead of doing it — "This section will discuss...", "We now turn our attention to..." → just do it. Exception: roadmap sentences in the Introduction ("Section 2 reviews...") are standard academic practice, keep them.

### Monotonous sentence rhythm (burstiness)

If 5+ consecutive sentences all fall within a narrow word-count range (e.g., all 20-25 words): **vary the rhythm.**

- Insert a short sentence (≤10 words) to break a run of long ones.
- Combine two short sentences if the pattern is uniformly choppy.
- Read the paragraph aloud — if it feels metronomic, it is.

Target variation by section:
- Introduction: highest variation (hook with short sentences, build with long ones)
- Results: moderate (short for key findings, longer for detail)
- Discussion: highest variation (short for emphasis, long for interpretation)
- Methods: low variation acceptable (procedural sections are naturally uniform)

### Rule-of-three compulsion

Not every argument decomposes into exactly 3 sub-points. If a paragraph always has 3 items, scan harder — two strong points beat three padded ones. Four is fine. Five is fine. Don't pad to 3.

### Uniform paragraph length

All paragraphs ~same length (150-200 words each) → templated feel. Vary it: a 2-sentence paragraph after a 10-sentence one creates rhythm. Methods can be uniform; Introduction and Discussion should not be.

### Synonym cycling

"Students → learners → participants → subjects" within one paragraph. Don't vary terms to avoid repetition — in academic writing, **consistent terminology is clarity, not weakness.** Enforce the terminology ledger. One term per concept per section. Repeat it.

## Overclaim checklist

Flag and soften these words unless the evidence is unusually strong and the scope is tightly defined:

| Overclaim | Safer replacement |
|---|---|
| prove | show |
| conclusively | — (remove) |
| unprecedented | — (remove or qualify) |
| best | among the strongest |
| superior | — (state the specific advantage) |
| first | to our knowledge |
| revolutionary | — (remove) |

## Integrity rules

- Do not invent references
- Do not alter quantitative values unless correcting an obvious typo the user confirms
- Do not upgrade association to causation
- Do not imply broader generalisability than the study supports

## AI boundary

AI may help with language control, not scientific fabrication.

**Allowed**: grammar and clarity, restructuring and hedging, translation with terminology checking

**Not allowed**: fabricated citations or datasets, invented mechanisms presented as fact, unsupported claims of novelty
