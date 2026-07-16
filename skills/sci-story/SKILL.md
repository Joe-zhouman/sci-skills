---
name: sci-story
description: >-
  Narrative academic writing — draft Introduction, Discussion, Abstract,
  and Keywords from completed Results and figure reports. Anchored to the
  four-question spine and Introduction-Discussion coherence. Writes intro.md,
  discussion.md, abstract.md. 写引言、写讨论、写摘要、write introduction, write
  discussion, write abstract. Does not do data-driven Method/Results/Conclusion,
  does not polish prose, does not draw figures.
---

# sci-story

Write Introduction / Discussion / Abstract / Keywords from completed Results and
the figure warehouse. Every section serves the four-question spine;
Introduction and Discussion are coherent by construction — they're drafted together
with the same spine, not independently.

## Layout & boundaries

```
<project-root>/
  manuscript/v1/tex/             ← the OFFICIAL manuscript (user owns; this skill does NOT touch it)
  sci-skills/
    sci-draw/                    ← figure warehouse — READ-ONLY: figN-report.md
    sci-write/                   ← THIS skill reads and writes here
      paper-plan.md              ← READ: figure list + section progress
      results.md                 ← READ: completed Results (evidence baseline for Discussion)
      method.md                  ← READ: data/sample context for Introduction
      conclusion.md              ← READ: contribution statement
      figN-reading.md            ← READ: figure claim corrections
      terminology-ledger.md      ← READ + WRITE (co-owned with the writing and polishing stages)
      intro.md                   ← WRITE: this skill's output
      discussion.md              ← WRITE: this skill's output
      abstract.md                ← WRITE: this skill's output
```

- **Does NOT touch `manuscript/`.** MD drafts go to `sci-skills/sci-write/`.
  Moving content into `manuscript/v1/tex/` is the human's job.
- **Does NOT write to `../sci-draw/`.** Read-only on the figure warehouse.
- **Output is always MD.** Don't ask "md or tex" — tex is a different skill's concern.
- **Reads writing drafts from disk; never imports code.**

## File contracts

| File | Produced by | Read by | Schema |
|---|---|---|---|
| `paper-plan.md` | drafting stage | this skill | fig entries + section status |
| `results.md` | drafting stage | this skill | data-driven prose (evidence baseline) |
| `conclusion.md` | drafting stage | this skill | contribution statement |
| `method.md` | drafting stage | this skill | data/sample context |
| `figN-reading.md` | drafting stage | this skill | corrected claim (wins over report) |
| `../sci-draw/figN-report.md` | any figure-maker | this skill | Core conclusion, Key findings |
| `terminology-ledger.md` | drafting + polishing + this skill | this skill | canonical term forms |
| `intro.md` | this skill | human, polishing stage | Introduction draft |
| `discussion.md` | this skill | human, polishing stage | Discussion draft |
| `abstract.md` | this skill | human, polishing stage | Abstract draft |

## Startup

Every session starts here:

1. **Locate `sci-skills/sci-write/`.** Must exist — the figure reports and data-driven
   drafts this skill reads live here. If `results.md` isn't there yet, tell the user:
   "Results need to be drafted first — narrative sections are drafted AFTER completed
   results exist. Draft the results, then come back."

2. **Read the neighbors** (skip any that don't exist; flag missing but don't block):

   From `sci-skills/sci-write/`:
   - `paper-plan.md` — figure claims, section status
   - `results.md` — completed Results (the evidence baseline Discussion interprets)
   - `conclusion.md` — the contribution statement
   - `method.md` — data/sample context for Introduction background
   - `figN-reading.md` — claim corrections (corrected claim wins over report)

   From `../sci-draw/` (*figure warehouse* — read regardless of source):
   - `figN-report.md` — `Core conclusion`, `Key findings`, `Statistical methods`.
     These are the evidence ground truth.

3. **Load or build the terminology ledger.**

   If `terminology-ledger.md` exists → read it, enforce it. Extend with new terms.

   If it doesn't exist → build from figure reports + writing drafts + manuscript
   text. Write to `sci-skills/sci-write/terminology-ledger.md`. Mark new entries
   with source `sci-story`.

## Workflow

### Step 0 — Gather axes + read inputs

1. **Paper type** — research / methods / hypothesis / algorithmic / review.
   Default: research. Ask if ambiguous.
2. **Target journal** — nature / nat-comms / generic. Default: generic.
3. **Language** — en. Default.
4. Read all neighbor files thoroughly. Build a mental model: key claims, figure
   support, contribution statement, evidence boundary.
5. **Infer the gap** from context. Introduction hasn't been written yet, so infer
   from what Results claim vs what Conclusion states as contribution. If gap is
   unclear, ask the human.

State the detected axes in one short line before proceeding.

### Step 1 — Write the four-question spine (human intervention point)

Draft the spine that every section will serve:

> (1) What problem do we solve, and why is there no well-established solution?
> (2) What is our contribution?
> (3) Why can our method work in essence?
> (4) What advantage and new insight do we provide?

**Stop. Show the human.** Ask: "Does this spine capture the paper's argument?
Introduction and Discussion will both be built from this — get it right now."

Write the spine to `sci-skills/sci-write/story-spine.md` after human confirms.

### Step 2 — Draft Discussion first

Discussion anchors interpretation. Write it first so Introduction knows exactly
what narrative arc it must set up.

Load `references/discussion-guide.md`. Structure:

1. **Opening** — restate the main finding as a contribution, not an observation.
   "Our results show [contribution]. This means [interpretation]."
2. **Mechanism** — why this result? Plausible mechanism, hedged. Address rival
   explanations.
3. **Literature comparison** — align/contrast with prior work. Use real-DOI
   placeholders from search MCP.
4. **Limitations** — evidence boundaries. Specific, not generic.
5. **Implications** — bounded significance statement.

Before writing full prose, run the **confirmation gate** (see `references/writing-discipline.md`):
echo the Discussion's one-paragraph argument + key interpretations + assumptions.
Get human confirmation.

Write `discussion.md`.

### Step 3 — Draft Introduction

Load `references/introduction-guide.md`. Funnel structure:

1. **Field stake** — why this field matters.
2. **Bottleneck** — state of the art and its limitation.
3. **Prior work** — key attempts, what they left unsolved.
4. **Gap** — the specific unsolved problem. This must match what Discussion addresses.
5. **Present study** — what we did, what we found, how it fills the gap.

**Introduction-Discussion coherence check (mandatory before writing full prose):**

Run the check from `references/writing-discipline.md`: for every gap/bottleneck
in the Introduction outline, confirm Discussion has a corresponding response.
If mismatch, fix before drafting.

Before writing full prose, run the **confirmation gate**: echo the funnel structure
+ gap statement + coherence check results. Get human confirmation.

Write `intro.md`.

### Step 4 — Draft Abstract

Load `references/abstract-guide.md`. Abstract is a mini-paper, written last when
Discussion and Introduction are stable.

1. Compress the spine into one tight paragraph.
2. Choose template variant (A/B/C) based on the paper's argument structure.
3. No new content — everything must already appear in Introduction, Results,
   or Discussion.

Run the confirmation gate: echo the compressed spine. Get human confirmation.

Write `abstract.md`.

### Step 5 — Human review

**Mandatory. Do not skip.**

Show changes with `git diff` across `sci-skills/sci-write/`.

Ask explicitly: "Do intro/discussion/abstract look right? Any coherence issues?"

The author owns the argument. Revisions are targeted, not full rewrites.

### Step 6 — Commit

After the human approves:

```bash
git add sci-skills/sci-write/intro.md sci-skills/sci-write/discussion.md \
        sci-skills/sci-write/abstract.md sci-skills/sci-write/terminology-ledger.md
git commit -m "story(intro,discussion,abstract): <one-line spine>

- Introduction: funnel from [field stake] to gap [gap]
- Discussion: interprets [main finding], addresses [rival], limited by [boundary]
- Abstract: mini-paper, compressed spine
- Terminology ledger: [new/updated entries if any]"
```

Update `paper-plan.md`: set Introduction, Discussion, Abstract, Keywords to
`story-drafted`.

## Pervasive discipline (Steps 2-4)

Runs around every section draft. Detail in `references/writing-discipline.md`:

- **Four-question spine first.** Every section serves the spine. Can't write the
  spine → don't draft.
- **Confirmation gate** before each section's full prose.
- **Introduction-Discussion coherence.** Intro gap → Discussion must respond.
  Run the consistency check after every Intro draft.
- **Targeted revision** — change only what the human flags, never full rewrite.
- **Verb calibration** — Introduction states contributions with strong verbs
  (we showed/demonstrated); Discussion interprets with weaker verbs (may reflect,
  suggests). Mechanism speculation → weak verbs + boundary statement.
- **Real-DOI citation placeholders.** Search MCP → real DOI → placeholder.
  Human does final Zotero insertion.
- **Sweep unsupported novelty/universal claims.**

## Reference index

| File | Open when |
|---|---|
| `references/writing-discipline.md` | Before drafting any section — confirmation gate, coherence rules, verb calibration, citation protocol |
| `references/literature-search.md` | At Steps 2-3 (Discussion and Introduction) — academic search tool priority, journal quality, layer-by-layer citation requirements |
| `references/discussion-guide.md` | At Step 2 — default structure, coherence check, syntax, failure modes |
| `references/introduction-guide.md` | At Step 3 — funnel structure, paragraph jobs, drafting rules, Intro-Discussion lock chain |
| `references/abstract-guide.md` | At Step 4 — mini-paper structure, template variants, drafting discipline |

## Boundaries

| Need | Where |
|---|---|
| Write Method/Results/Conclusion from data | data-driven drafting — reports observations, not narrative |
| Polish/revise prose | prose polishing — edits manuscript tex directly |
| Create scientific figures | figure creation — produces plots and figure reports |
| Submit manuscript / cover letter | submission management |
| Full systematic lit review | This skill does targeted search for positioning and comparison; a different mode |

## Decoupling self-check

Run after any change to this skill:

```bash
grep -rn "from sci-write\|import sci-write\|sci_write\." skills/sci-story/   # must be empty
grep -rn "from sci-draw\|import sci-draw\|sci_draw\." skills/sci-story/     # must be empty
grep -rni "nature-writing\|nature_writing" skills/sci-story/                # must be empty
```

Reading files is allowed; importing code or assuming co-presence is a leak.

## Privacy

Don't disclose private paths, filenames, or unpublished manuscript content in
user-facing output, generated prose, or commit messages. Use generic descriptions
("the provided data file"). Reveal exact paths only when the user explicitly asks
for an audit trail.
