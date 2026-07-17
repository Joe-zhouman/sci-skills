---
name: sci-polish
description: >-
  Polish academic manuscript prose by editing manuscript/vN/tex/ directly — git
  commits serve as the audit trail, no separate polish output directory. Reads
  the figure warehouse and writing drafts before editing to preserve
  claim/evidence consistency. Covers polish, restructure, and Chinese-to-English translation of academic/scientific manuscript text —
  abstracts, introductions, results, discussions, conclusions, titles, methods
  sections, or full drafts. Also covers LaTeX layout/typesetting fixes (float
  placement, stranded headings, loose pages). Triggers on: polish my paper,
  revise this paragraph, edit manuscript, proofread, academic writing, scientific
  writing, SCI paper, English polishing, language editing, Chinese-to-English
  academic translation, 学术写作、科研写作、论文润色、SCI写作、英文论文润色、润色、
  改写、学术英语、翻译、排版.
---

# sci-polish

Polish academic manuscript prose directly in `manuscript/vN/tex/`. Git tracks every
change; commit messages carry the diagnosis and revision summary. No separate polish
output directory — the manuscript is both source and output.

## Layout & boundaries

```
<project-root>/
  manuscript/
    v1/tex/                     ← THIS skill reads and edits here (or current round)
    r1/tex/                     ← also works on revision rounds
  sci-skills/
    sci-write/                  ← READ + WRITE on terminology-ledger.md (co-owned);
                                   READ-ONLY: paper-plan.md, results.md, discussion.md,
                                   conclusion.md, method.md, figN-reading.md
    sci-draw/                   ← READ-ONLY: figN-report.md (claims, findings, stats,
                                   terminology)
```

- **Edits `manuscript/` directly.** The manuscript IS the working surface. No
  intermediate files, no `sci-polish/` output directory.
- **Git is the audit trail.** `git diff` shows what changed; the commit message
  records the diagnosis and revision decisions. No separate description/report
  files — the git history is the permanent record.
- **`sci-skills/sci-write/terminology-ledger.md` is co-owned.** Both the writing stage and the polishing stage read and write this file. Content-level decisions are recorded first; form-level constraints discovered during polish extend it.
- **Reads other neighbors — never edits.** Claim files and figure reports are read-only.

## Startup

Every session starts here:

1. **Locate the manuscript.** Check `manuscript/v1/tex/` (default) or the current
   review round (`manuscript/rN/tex/`). If absent, ask the user where the tex files
   are. If no tex files exist anywhere, ask the user to provide the manuscript
   content — this skill works on existing text, not a blank page.

2. **Check git tracking.** If the manuscript directory is not under git, remind
   the user: "Polish without git loses the audit trail. `git init` or `git add`
   the tex files first, then come back." Don't proceed without git — the commit
   history IS the polish record.

3. **Read the neighbors** (skip any that don't exist — the manuscript may not
   have been drafted in the writing stage):

   From `../sci-skills/sci-write/`:
   - `claim.md` — **the canonical claim.** The one-sentence argument, gap, evidence
     baseline, and boundary. This is the non-negotiable anchor——润色可以改措辞，
     但不能改 claim。Read it first.
   - `terminology-ledger.md` — **co-owned file.** The canonical term ledger
     produced by the writing stage (or an earlier polish round). Read it; enforce it.
     Extend it after polish for any new constraints discovered.
   - `paper-plan.md` — figure claims (the "what this paper argues" map) and
     section status
   - `results.md` / `discussion.md` / `conclusion.md` / `method.md` — drafted
     prose with claim/evidence structure
   - `figN-reading.md` — claim corrections from the figure-reading consistency
     check (the corrected claim wins over the original figure report)

   From `../sci-skills/sci-draw/` (*figure warehouse* — read regardless of source):
   - `figN-report.md` — `Core conclusion`, `Key findings`, `Statistical methods`,
     terminology. These are the evidence ground truth.

   **If the writing drafts exist**: the claims recorded there are the non-negotiable
   content baseline. Polish improves expression without altering claim substance,
   evidentiary strength, or boundary. The terminology ledger, if present, provides
   the canonical form for every term — enforce it.

   **If the writing drafts don't exist**: work standalone. Diagnose from the
   manuscript text alone, without family context. The diagnosis hierarchy still
   applies; you just lack the external claim reference and pre-built ledger.

4. **Load or build the terminology ledger.**

   **If `sci-skills/sci-write/terminology-ledger.md` exists** → read it, enforce it.

   **If it doesn't exist** → build it from these sources in priority order:
   1. Manuscript glossary (`glossary.tex`, `nomenclature.tex`, etc.) — authoritative
   2. Figure reports (`figN-report.md`)
   3. neighboring writing files
   4. Manuscript text itself

   Write to `sci-skills/sci-write/terminology-ledger.md`:

   ```markdown
   # Terminology Ledger

   | Category | Term / variants | Canonical form | Source | Notes |
   |---|---|---|---|---|
   | Compound | contact thermal resistance / thermal contact resistance | thermal contact resistance | manuscript glossary | |
   | Variable | IL-6 / interleukin-6 | IL-6 | fig1-report | |
   | Stats | SD / SEM / 95% CI | SD | fig1-report | |
   | ... | ... | ... | ... | |
   ```

   Source column: `manuscript glossary`, `figN-report`, `drafting-stage`, `polish-discovered`.
   Conflict resolution: manuscript glossary wins.

   Enforce during polish. Update after polish (with human approval), commit together with tex changes.

5. **If manuscript glossary exists** (`glossary.tex`, `nomenclature.tex`, etc.): read it. Terms defined there are authoritative; ledger conflicts → glossary wins, flag and update ledger.

## Workflow

### Step 0 — Gather axes

Before touching a sentence, collect:

1. **The text** — which tex file(s), which section(s)
2. **Paper type** — research / methods / hypothesis / algorithmic / review.
   Default: research. Ask if ambiguous.
3. **Section context** — what job does this section perform? If neighboring writing files
   exist, cross-reference against the section templates in
   `references/section-guide.md` with the drafted prose as the concrete
   example of that job. If no writing drafts, use `references/section-guide.md`
   alone.
4. **Language** — en (English source) or zh-to-en (Chinese-to-English). Detect
   from the draft.
5. **Target journal** — nature / nat-comms / generic. Default: generic. Affects
   style guardrails.
6. **Claim baseline** — if neighboring writing files exist, extract the claim list:
   - From `paper-plan.md`: which figures, what each claims
   - From `results.md`: which paragraph carries which claim, verb strength used
   - From `discussion.md`: mechanism interpretations, limitation boundaries
   - From `figN-reading.md`: corrected claims (these win over original reports)

   If no writing drafts, the claim baseline is what the manuscript text
   currently states — you'll preserve substance during polish without a separate
   reference.

State the detected axis values in one short line before proceeding. Correct
cheaply — the user sees a one-line summary and can override any axis.

### Step 1 — Diagnose

Identify the main failure mode before editing. Prioritize in this exact order:

```
paper type logic → section job → paragraph structure → claim/evidence/boundary → sentence polish
```

Check each level:

| Level | What to look for | With family context |
|---|---|---|
| Paper type | Wrong architecture for this paper type | Cross-check with `references/paper-types.md` playbook |
| Section job | Section performing wrong rhetorical work | Compare against the section template for this section |
| Paragraph | No controlling idea, stacked claims, missing logic | Cross-check paragraph claim against `paper-plan.md` figure claim |
| Claim/evidence/boundary | Claim without evidence, missing limitation, correlation→causation | Verify verb strength matches `figN-report.md` stats (show vs suggest vs may) |
| Sentence | Wordiness, overloaded sentences (>30 words), inconsistent terminology | Enforce terminology ledger |

**Do not sentence-polish a draft whose section job is wrong.** Surface the
structural problem first, explain it, then polish only after the user confirms.

**If a paragraph's structural problem cannot be fixed without inventing content,
flag it.** Don't paper over missing logic with smooth prose.

**Claim drift detection (when family context exists):** Before editing any
sentence that carries a scientific claim, compare against the claim baseline
(Step 0.6). If the manuscript text already differs from the recorded claim,
flag it — the human needs to decide which version is correct. If the edit
would change what is claimed, how strongly, what evidence supports it, or
where the boundary is → flag for human review rather than silently rewriting.

### Step 2 — Polish

Apply polish in priority order, matching the diagnosis hierarchy:

1. **Paper-type architecture** — load `references/paper-types.md`, apply the
   relevant playbook
2. **Section job** — load `references/section-guide.md`, fix rhetorical function.
   If the writing drafts exist, the section template tells you what job this
   section performs; cross-check that the polished version still does that job.
3. **Paragraph logic** — load `references/writing-strategy.md`, restructure flow
   (hourglass, claim/evidence/boundary)
4. **Language rules** — load `references/language-guide.md`, apply sentence and
   paragraph rules
5. **Style mechanics** — load `references/style-guardrails.md`, check articles,
   register, overclaim

Load only the reference files needed for this job. Don't load everything at once.

**Claim-preservation rule:** every editorial change must be checked against
`claim.md`. If the edit would change what is claimed, verb strength, or
limitation boundary → flag. Allow wording/grammar fixes. When in doubt,
read `claim.md` again and compare.

**For Chinese-to-English (zh-to-en):** extract core propositions first,
reconstruct logical links, then apply English rules. Do not translate
clause-by-clause. See `references/language-guide.md` for the full workflow.

**For LaTeX layout requests:** skip the prose axes and load
`references/latex-layout.md` directly. That file is self-contained — diagnosis
workflow, float patterns, and the "regenerate wide figures taller at the source"
rule. Always compile and visually inspect before and after.

**Core rules:** language serves argument. Don't invent data, references, or claims. Don't alter quantitative values. Enforce the terminology ledger. Avoid em dashes.

### Step 3 — Human review

**Mandatory. Do not skip.**

Present the polished changes with `git diff`. The diff is the review surface —
the user sees exactly what changed, line by line.

Ask explicitly: "Does this look right? Any changes needed?"

The author owns the argument, the terminology, and the final call on every
change. If they reject a change, revert it. If they want a different direction,
return to Step 1 with their feedback.

### Step 4 — Commit

After the human approves:

```bash
git add manuscript/vN/tex/<changed-files> sci-skills/sci-write/terminology-ledger.md
git commit -m "polish(<section>): <one-line diagnosis>

- <structural change>
- <claim/evidence adjustment, if any>
- <terminology ledger: new/updated entries with source>
- <sentence-level summary>"
```

Each polish round is one commit. `git log -- manuscript/vN/tex/` is the polish history.

## Routing table

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
| Journal | any | `references/style-guardrails.md` — journal-specific rules if applicable |

**Always load** `references/writing-strategy.md` (core principles apply to every job).

**On-demand only** (load when the user explicitly asks or the text needs it):
- `references/phrasebank.md` — hedging, transition, evidence, limitation phrases
- `references/latex-layout.md` — LaTeX float placement, page layout, typesetting

## Active interception

When the user's draft or request triggers these, explain and offer alternatives.
Respect the user's final decision, but leave a clear record of the warning.

| Issue | Why wrong | Fix |
|---|---|---|
| "Just fix the grammar" on a structurally broken paragraph | Grammar fixes on a paragraph with no controlling idea waste everyone's time | Diagnose first, show the structural problem, ask whether to fix structure or only grammar |
| Results paragraph full of "may reflect" / "suggests that" | Results should report observations, not interpret them | Move interpretation to Discussion; keep Results in past tense, reporting what was found |
| Discussion that re-summarizes Results | Discussion should explain what findings mean, not repeat what was observed | Cut result recaps; add interpretation, mechanism, limitation, implication |
| Claim without evidence | Reader asks "how do you know?" — if the text can't answer, the claim is floating | Either add the supporting evidence or hedge the claim to match what's actually shown |
| "Prove" / "conclusively" / "unprecedented" / "first" | Overclaiming kills credibility with reviewers | Replace with "show" / "suggest" / "to our knowledge" / "among the first" |
| Chinese draft: clause-by-clause translation | Produces topic-comment chains, missing logical connectives | Extract propositions first, reconstruct logic, then write English |
| Asking AI to write the core argument from scratch | AI should polish expression, not author scientific claims | Ask the user to provide the argument; help structure and express it |
| Silently rewriting a claim recorded in neighboring writing files | The claim was calibrated to figure evidence in the figure-reading step | Flag the discrepancy; let the human decide which version is correct |
| New terminology constraint discovered during polish (word order, convention) not written back to ledger | Next sci-write or sci-polish round starts from scratch, same mistakes recur | Add the constraint to `sci-skills/sci-write/terminology-ledger.md`; mark source `polish-discovered`; commit together with the tex changes |
| Ledger entry conflicts with manuscript glossary | Manuscript glossary is the authoritative source for terms it defines | Flag the discrepancy; manuscript glossary wins; update ledger to match

## Reference index

| File | Open when |
|---|---|
| `references/writing-strategy.md` | Every job — hourglass structure, claim/evidence/boundary, section responsibilities, failure mode diagnosis |
| `references/section-guide.md` | Section context known — per-section job, polishing priorities, common failure modes, syntax patterns |
| `references/language-guide.md` | Every job — English sentence/paragraph rules, Chinese-to-English workflow, common CN-influenced patterns |
| `references/paper-types.md` | Paper type matters for architecture — research/methods/hypothesis/algorithmic/review playbooks |
| `references/style-guardrails.md` | Every job — academic register, articles, numbers/units, overclaim checklist, integrity rules |
| `references/phrasebank.md` | On demand — evidence verbs, transition families, hedging, limitation language, future-work patterns |
| `references/latex-layout.md` | On demand — float placement, page fill, stranded headings, multi-panel arrangement, SI structure, diagnosis workflow |

## Boundaries

This skill does not do these things:

| Need | Where |
|---|---|
| Write a manuscript from scratch | Draft content first (data-driven or manual), then come back to polish |
| Write a cover letter | submission stage — handles cover letters for submission and revision |
| Create scientific figures | figure creation — produces publication-quality plots from experimental data |
| Response to reviewers | Not yet covered |
| Literature search / Introduction drafting | narrative writing stage; polish here after drafting |

## Privacy

Do not disclose private paths, filenames, or unpublished manuscript content in
user-facing output, commit messages, or `git diff` commentary. Use generic
descriptions ("the manuscript tex file"). Reveal exact paths only when the user
explicitly asks for an audit trail.
