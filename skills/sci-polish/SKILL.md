---
name: sci-polish
description: >-
  Polish, restructure, or translate academic prose into publication-quality English using writing-strategy principles and curated academic phrase patterns. Use when the user asks to polish, revise, edit, proofread, or translate academic/scientific manuscript text — abstracts, introductions, results, discussions, conclusions, titles, methods sections, or full drafts. Also covers LaTeX layout/typesetting fixes (loose pages, stranded headings, float placement). Triggers on: polish my paper, revise this paragraph, edit manuscript, proofread, academic writing, scientific writing, SCI paper, English polishing, language editing, Chinese-to-English academic translation, 学术写作、科研写作、论文润色、SCI写作、英文论文润色、润色、改写、学术英语、翻译、排版.
---

# sci-polish — Academic Polishing Workflow

Polish academic prose by diagnosing structural problems first, fixing argument logic before sentence-level cleanup. The skill's primary output is a decision-documented, reproducible polish — not just prettier sentences.

## Core philosophy

**File archiving and human involvement > AI automation.** Every polish job leaves a process log (what was diagnosed, what was changed, why) and a final report (polished text + revision notes). The files are the ground truth — when returning to a draft after a break, read the files, not conversation memory. Human review checkpoints are mandatory, not optional: the author owns the argument, the terminology, and the final call on every change.

## If this isn't what you need

- **Cover letter writing** → use `sci-letter` — handles first-submission and revision/resubmission cover letters
- **Scientific figures / data visualization** → use `sci-draw` — creates publication-quality plots from experimental data
- **Response to reviewers** (回复审稿人) → not yet covered by any sci-skill
- **Writing a manuscript from scratch** → this skill polishes existing text, doesn't author papers; draft the content first, then come back

## Working directory: `sci-polish/`

All polish work lives in `sci-polish/` under the project root. Each polish job gets two files — the process log and the final report:

```
sci-polish/
  abstract-description.md     # Process log (decisions, diagnostics, terminology ledger)
  abstract-report.md          # Final report (polished text + revision notes)
  intro-description.md
  intro-report.md
  discussion-description.md
  discussion-report.md
  ...
```

**File-based workflow**: the files in `sci-polish/` are the ground truth. When returning to a draft after a break, read the files first — they contain what was diagnosed, what was changed, and why. Trust the files, not conversation memory.

_why_ **Context windows are ephemeral.** A session ends, a summary truncates, and last week's polishing decisions are gone. Writing decisions into files at the moment they're made preserves the *why* at the point of highest clarity. When you return, the file is a time capsule of actual reasoning — which failure modes were found, which terminology was standardized, which changes the author approved.

### Startup

Before entering the workflow, check the state of `sci-polish/`:

1. **`sci-polish/` does not exist** → create it, then start from Step 0.
2. **`sci-polish/` exists** → ask the user: "Is there a draft in `sci-polish/` you want to continue working on?" If yes, read the relevant `-description.md` and `-report.md` files to understand the current state, then pick up from the appropriate step. If no, start a new polish job from Step 0.

## Core workflow (6 steps)

Each step depends on the output of the previous one. Never skip diagnosis (Step 1) — sentence-polishing a structurally broken paragraph is a failed edit.

### Step 0: Gather information + detect axes

Before touching a single sentence, collect:

1. **The text** to polish — get the full passage, not a fragment
2. **Paper type** — research / methods / hypothesis / algorithmic / review. Default: research. Ask if ambiguous.
3. **Section** — abstract / intro / results / discussion / conclusion / title / methods. May be multiple. Ask if it affects the polish.
4. **Language** — en (English source) or zh-to-en (Chinese-to-English). Detect from the draft.
5. **Target journal** — nature / nat-comms / generic. Default: generic. If the user names a specific journal, note it.
6. **Previous polish logs** — check `sci-polish/` for existing `-description.md` files from prior rounds on this manuscript

State the detected axis values in one short line to the user before proceeding, so they can correct you cheaply.

_why_ **Axes determine what rules apply.** A Results section and a Discussion section have different jobs — applying the wrong section playbook produces polished prose that performs the wrong rhetorical function. Stating axes upfront costs one line and catches mismatches before you've rewritten a paragraph.

**Start the process log**: create `sci-polish/<job-name>-description.md`. Record the gathered information, detected axes, and any user corrections.

### Step 1: Diagnose — find the real problem

Before rewriting, identify the main failure mode. Prioritize in this exact order:

```
paper type logic → section job → paragraph structure → claim/evidence/boundary → sentence polish
```

Check each level:

| Level | What to look for |
|---|---|
| Paper type | Wrong architecture for this paper type (e.g., methods paper structured as research article) |
| Section job | Section doing the wrong rhetorical work (e.g., Results drifting into Discussion) |
| Paragraph | No controlling idea, stacked claims without support, missing logical connections |
| Claim/evidence/boundary | Claim without evidence, data without a claim, missing limitation/scope, correlation → causation |
| Sentence | Wordiness, overloaded sentences (>30 words), clutter, inconsistent terminology |

**Do not sentence-polish a draft whose section job is wrong.** Surface the structural problem first, explain it to the user, then polish only after they confirm the direction.

**If a paragraph's structural problem cannot be fixed without inventing content, flag it.** Don't paper over missing logic with smooth prose.

_why_ **Polishing a broken argument produces a prettier broken argument.** The reader's confusion doesn't come from word choice — it comes from claims without evidence, Results that interpret instead of report, Discussions that re-summarize instead of explain. Fix these first, and sentence polish becomes straightforward.

**Record in `-description.md`**: the primary failure mode(s) found, which level they're at, and what structural fixes are needed.

### Step 2: Build terminology ledger

Before polishing, extract and standardize terminology across the text:

- Key technical terms, abbreviations, gene/protein names, model names, dataset names
- Units and notation
- Statistical language (SD/SEM/CI, test names)

Pick one canonical form per term and use it consistently throughout. Do not introduce synonyms to vary the prose — in academic writing, consistency > variety.

_why_ **Inconsistent terminology is the #1 tell of unpolished academic writing.** A reader who sees "IL-6" in paragraph 2 and "interleukin-6" in paragraph 5 wonders if they're the same thing. The terminology ledger is a single source of truth — build it once, enforce it everywhere.

**Record in `-description.md`**: the terminology ledger as a simple table or list.

### Step 3: Polish

Apply polish in this priority order, matching the diagnosis hierarchy from Step 1:

1. **Paper-type architecture** — load `references/paper-types.md`, apply the relevant playbook
2. **Section job** — load `references/section-guide.md`, fix rhetorical function
3. **Paragraph logic** — load `references/writing-strategy.md`, restructure flow (hourglass, claim/evidence/boundary)
4. **Language rules** — load `references/language-guide.md`, apply sentence and paragraph rules
5. **Style mechanics** — load `references/style-guardrails.md`, check articles, register, overclaim

Load only the reference files needed for this job. Don't load everything at once.

**For Chinese-to-English (zh-to-en)**: extract core propositions first, reconstruct logical links, then apply English rules. Do not translate clause-by-clause. See `references/language-guide.md` for the full workflow.

**For LaTeX layout requests**: skip the prose axes and load `references/latex-layout.md` directly. That file is self-contained — diagnosis workflow, float patterns, and the "regenerate wide figures taller at the source" rule. Always compile and visually inspect before and after.

**Core rules throughout:**

- Language serves argument. Don't polish sentences while leaving the reasoning broken.
- Do not invent data, references, mechanisms, or novelty claims.
- Do not alter quantitative values unless correcting an obvious typo the user confirms.
- Keep technical terms, gene/protein names, model names, and statistical terms stable.
- Avoid em dashes in polished output by default. Prefer commas, parentheses, or full stops.

**Record in `-description.md`**: which reference files were loaded, key structural changes made, and any flagged issues that couldn't be fixed without author input.

### Step 4: Human review checkpoint

**This is mandatory. Do not skip.**

Present the polished text to the user with:

1. The polished prose (plain text, not in a code block)
2. **Revision notes**: 3-5 short bullets on major structural and stylistic changes
3. Any flagged issues that need author decisions (e.g., ambiguous claims, missing boundaries)

Ask the user explicitly: "Does this look right? Any changes needed?"

The author owns the argument, the terminology, and the final call. If they reject a change, revert it and record the decision. If they want a different direction, return to Step 1 with their feedback.

_why_ **AI can improve expression, but only the author knows the science.** A polished sentence that subtly changes a mechanism's direction or a claim's strength is worse than the original — it's wrong AND confident-looking. The human checkpoint catches these before they fossilize into the manuscript.

**Record in `-description.md`**: what the user approved, rejected, or changed. This is the audit trail.

### Step 5: Finalize report

The process log `sci-polish/<job-name>-description.md` now contains raw notes from Steps 0-4. Review it and **distill into a clean report** at `sci-polish/<job-name>-report.md`:

```markdown
# Polish Report — [section name]

## Source
- Paper type: [research / methods / hypothesis / algorithmic / review]
- Section: [abstract / intro / results / discussion / conclusion / title / methods]
- Language: [en / zh-to-en]
- Journal: [nature / nat-comms / generic]

## Diagnosis
- Primary failure mode: [paper type / section job / paragraph / claim-evidence / sentence]
- Specific issues found: [list]

## Terminology ledger
| Term | Canonical form | Notes |
|---|---|---|
| ... | ... | ... |

## Polished text

[Full polished prose]

## Revision notes
1. [Structural change 1]
2. [Structural change 2]
3. [Sentence-level change]
4. ...

## Author decisions
- [Approved / rejected / modified items from Step 4]
```

The description log remains as the raw audit trail; don't delete it.

_why_ **Two files, two audiences.** The log is chronological and messy — decisions scattered across five steps of notes, useful for the maker retracing reasoning. The report is clean and structured: a future you, a collaborator, or a journal editor can read the polished text and understand exactly what changed and why without reading the full process log.

## Routing table

When loading references in Step 3, use this table to decide what to load:

| Axis | Value | Load |
|---|---|---|
| Paper type | research | `references/paper-types.md` § research |
| | methods | `references/paper-types.md` § methods |
| | hypothesis | `references/paper-types.md` § hypothesis |
| | algorithmic | `references/paper-types.md` § algorithmic |
| | review | `references/paper-types.md` § review |
| Section | any | `references/section-guide.md` — relevant section(s) |
| Language | en | `references/language-guide.md` § English source |
| | zh-to-en | `references/language-guide.md` § Chinese-to-English |
| Journal | any | `references/style-guardrails.md` — journal-specific rules if any |

**Always load** `references/writing-strategy.md` (core principles apply to every job).

**On-demand only** (load when the user explicitly asks or the text needs it):
- `references/phrasebank.md` — hedging, transition, evidence, limitation phrases
- `references/latex-layout.md` — LaTeX float placement, page layout, typesetting

## Active interception

When the user's draft or request triggers these, explain and offer alternatives. Respect the user's final decision, but leave a clear record of the warning.

| Issue | Why wrong | Fix |
|---|---|---|
| "Just fix the grammar" on a structurally broken paragraph | Grammar fixes on a paragraph with no controlling idea waste everyone's time | Diagnose first, show the structural problem, ask whether to fix structure or only grammar |
| Results paragraph full of "may reflect" / "suggests that" | Results should report observations, not interpret them | Move interpretation to Discussion; keep Results in past tense, reporting what was found |
| Discussion that re-summarizes Results | Discussion should explain what findings mean, not repeat what was observed | Cut result recaps; add interpretation, mechanism, limitation, implication |
| Claim without evidence | Reader asks "how do you know?" — if the text can't answer, the claim is floating | Either add the supporting evidence or hedge the claim to match what's actually shown |
| "Prove" / "conclusively" / "unprecedented" / "first" | Overclaiming kills credibility with reviewers | Replace with "show" / "suggest" / "to our knowledge" / "among the first" |
| Chinese draft: clause-by-clause translation | Produces topic-comment chains, missing logical connectives | Extract propositions first, reconstruct logic, then write English |
| Asking AI to write the core argument from scratch | AI should polish expression, not author scientific claims | Ask the user to provide the argument; help structure and express it |

## Reference files

| File | When to load | Content |
|---|---|---|
| `references/writing-strategy.md` | Every job | Hourglass structure, claim/evidence/boundary, section responsibilities, writing order, failure mode diagnosis |
| `references/paper-types.md` | When paper type matters for architecture | Research / methods / hypothesis / algorithmic / review playbooks |
| `references/section-guide.md` | When section context is known | Per-section job, polishing priorities, common failure modes, syntax patterns |
| `references/language-guide.md` | Every job | English sentence/paragraph rules, Chinese-to-English workflow, common CN-influenced patterns |
| `references/phrasebank.md` | On demand — user wants phrase alternatives | Evidence verbs, transition families, hedging, limitation language, future-work patterns |
| `references/style-guardrails.md` | Every job | Academic register, articles, numbers/units, overclaim checklist, integrity rules |
| `references/latex-layout.md` | On demand — LaTeX layout/typesetting requests | Float placement, page fill, stranded headings, multi-panel arrangement, diagnosis workflow |

## Privacy rule

Do not disclose private local paths, filenames, attachment names, or internal reference filenames in polished output, revision notes, or reports. Use generic descriptions like "the manuscript text provided." Only reveal exact paths when the user explicitly asks for an audit trail.
