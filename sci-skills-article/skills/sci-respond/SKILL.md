---
name: sci-respond
description: >-
  Write the Response-to-Reviewers letter as a standalone LaTeX document, compiled
  to PDF. Point-by-point responses grounded in the manuscript, the reviews, and
  the writing-stage notes (claim, paper-plan, figure reports) — every response
  self-contained so the reviewer never has to flip back to the manuscript. Drives
  a revision round on manuscript/rN/: intakes the reviews, decomposes them into a
  stable issue ledger, stops at a checkpoint for the author to lock the
  per-issue strategy decisions that only they can make, then drafts the response
  tex and runs the final self-check. Writes tex directly (tex is the better
  format — precise layout; Word via pandoc only if the author insists, and the
  author fixes what pandoc cannot place precisely). Uses inline redline
  (\added/\deleted) for typo/clarification responses, keeps Response Figures
  non-floating (as-is), and compiles its own PDF from its bundled template.
  Triggers on: response letter, response to reviewers, rebuttal letter,
  point-by-point response, reviewer response, 审稿回复, 回复审稿人, 修回信,
  修改说明, 逐条回复. Not for: editing the manuscript tex per the locked
  decisions (that is sci-revise), polishing manuscript prose (sci-polish), cover
  letters (sci-submit), or drawing data figures (sci-draw).
---

# sci-respond — Response-to-Reviewers letter

Write the response letter for a revision round (`manuscript/rN/`). The product
is a standalone `response.tex` → PDF, built on the **bundled template** in this
skill's `assets/response-template/` (the `reviewresponse.sty` suite). Every
response is grounded in the manuscript, the reviews, and the writing-stage
notes — and **self-contained**: the reviewer can judge it without opening the
manuscript.

This skill writes **only the response letter**. It does not touch manuscript
tex (that is `sci-revise`'s job — see Boundary). It writes an issue ledger that
`sci-revise` consumes to make the manuscript edits.

## First principle

> **让审稿人不用回看手稿,也知道改动了什么。**
>
> Serve the reviewer as a reader who will only ever read this one Response
> document and will not flip back to the manuscript.

Every rule derives from this. The load-bearing corollary: **every response must
be self-contained** — carry its own evidence. A response that sends the reviewer
back to the manuscript is a failed response.

## Two decision classes — what the skill decides vs. what the author decides

Not every choice should be pushed to the author. Distinguish:

- **Class A — technical / implementation. The skill decides, does not ask.**
  These have an objectively better answer, and the author often doesn't even
  know the alternative exists. Pushing them to the author is not respect — it's
  offloading technical responsibility.
  - **tex, not Word.** tex gives precise layout; Word cannot. The response is
    written and compiled as tex. If the author insists on Word, generate it via
    pandoc and let the author fix what pandoc cannot place precisely. **不做保姆.**
  - template (the bundled `reviewresponse.sty` suite), cover-page layout, font
    sizes, spacing — the skill picks.
  - Response Figures are non-floating (`\captionof`); redline colors; macro
    choices (`\added`/`\deleted`); compile command.
  - the per-section overview is default-on (one-line opt-out exists, but the
    skill doesn't ask).
- **Class B — domain judgment + risk. The author decides; the skill surfaces
  options and stops.** Only the author knows their claim's footing, time
  budget, advisor's demands, how much this journal matters.
  - for a consequential reviewer comment: **defend / concede / run an experiment
    / cite existing evidence** — the skill presents 2–4 strategies with
    tradeoffs at the checkpoint; the author picks.
  - **claim narrowing vs. holding firm** — author's call.
  - an **ambiguous comment's intent** — the skill asks the author (Intent
    Diagnosis Card), does not guess.
  - **whether this round is worth a heavy rebuttal** — the skill gives its honest
    viability assessment; the author decides.

When Class A and a clean default conflict, the skill picks. When Class B arises,
the skill stops and asks. This is the meta-rule made concrete.

## Three hard rules (govern the response text)

1. **Self-contained (hard constraint).** Every response carries its own evidence
   — a quoted revised sentence, a Response Figure, or the data + a precise
   manuscript location with enough context that the reviewer need not look.
2. **Honesty over embellishment.** Facts as-is. Missing numbers are `[TBD]`,
   never invented. AI inferences tagged `INF:`. No "improves/significant/SOTA"
   without the metric behind it.
3. **Acknowledgement restraint.** Default: no acknowledgement. When warranted,
   one short line at the **end** of the response. Never "We sincerely appreciate
   your meticulous…" on a typo fix.

## Product

- **tex → PDF.** Built on the **bundled** `assets/response-template/`
  (`reviewresponse.sty` + `review_response.tex` + `Reviewers/`). The skill is
  self-contained — it does not depend on a project-root `templates/response/`.
- **Write directly in tex**, inside the reviewresponse environments.
- **Word via pandoc only on author insistence** — and the author fixes what
  pandoc cannot place precisely. The skill does not hand-hold the Word path.
- **sci-respond compiles its own PDF** (it is not sci-typeset's job — that skill
  compiles the *manuscript*).

## Layout & boundaries

```
<project-root>/
  manuscript/
    rN/
      tex/                      ← READ-ONLY: the manuscript under revision
      response/                 ← WRITE: the response letter lives here
        response-rN.tex             (one round per file)
        response-rN.pdf
        response-figures/           (Response Figures, non-floating)
      reviews/                  ← READ: the reviewer comments (raw)
  sci-skills/
    sci-write/                  ← READ: writing-stage notes — the paper's
      claim.md                     thinking, often more important than the
      paper-plan.md                manuscript itself for understanding the
      figN-reading.md              reviews. Read these to grasp the claim,
      terminology-ledger.md        the figure evidence, the term boundaries.
    sci-draw/                   ← READ: figN-report.md (figure evidence,
                                   statistics — grounds for data-backed defense)
    sci-revise/                 ← WRITE (shared): the revision-round state.
      issue-ledger.md              This skill writes the ledger during intake;
      change-log.md                sci-revise reads it to make edits. Co-read/
                                   write of one dir is normal in this family
                                   (sci-write/ is co-owned by write/story/polish).
```

- **Reads `manuscript/rN/tex/`** — the manuscript under revision (sections,
  lines, existing figures), to ground responses.
- **Reads `sci-skills/sci-write/` notes** — `claim.md` (the one-sentence
  argument; the boundary the response must not cross), `paper-plan.md`,
  `figN-reading.md`, `terminology-ledger.md`. These record the paper's thinking
  and are often more useful than the manuscript text for judging an
  underlying concern.
- **Reads `sci-skills/sci-draw/figN-report.md`** — figure evidence and
  statistics, the grounding for data-backed defenses.
- **Reads `manuscript/rN/reviews/`** — the raw reviewer comments.
- **Writes `manuscript/rN/response/`** — the response letter (tex + PDF +
  Response Figures). This is the product.
- **Writes `sci-skills/sci-revise/issue-ledger.md`** — the shared join key;
  `sci-revise` reads it to edit the manuscript. (The directory is shared state
  for the revision round; both skills read/write via its CONTRACT.)

This skill does **not** have its own output directory under `sci-skills/` — like
sci-story and sci-polish, its product goes into `manuscript/`. Only the
revision-round *process state* (`issue-ledger.md`, `change-log.md`) lives in the
shared `sci-skills/sci-revise/`.

## Startup — the revision-round flow

Four phases. Details in `references/workflow.md`; the shape:

1. **Intake.** First sense the grounding — run `scripts/scan_neighbor.py` to
   see which files are present (reviews, manuscript tex, sci-write notes,
   sci-draw figure reports, the issue-ledger) and whether their contract fields
   are complete. Then decompose each review into atomic issues with stable IDs
   (`R1-Q03`). For each: surface comment → **underlying concern** → proposed
   strategy → safe-claim-boundary → evidence anchors. Write to `issue-ledger.md`.
2. **Checkpoint — STOP.** Present the ledger. For Class-B issues (defend /
   concede / experiment / ambiguous intent), surface the options and wait for
   the author. **Nothing is drafted before this pause.** Class-A decisions
   (template, layout, tex) are already made — the author is not asked about them.
3. **Draft.** After the author locks strategies, write `response.tex` directly
   — cover page, overview, per-reviewer responses in the substance-first order.
   Typo/clarification responses use the inline-redline quote block. Response
   Figures are non-floating.
4. **Self-check + compile.** Run `scripts/check_response.py response-rN.tex` for
   the deterministic checks (comment/response pairing, leftover placeholders,
   bare `\textcolor`, acknowledgement count, banned qualifiers, float
   specifiers, cover fields). Then the semantic checks (coverage audit,
   integrity firewall, independent-reviewer read) and compile to PDF in this
   session. Word via pandoc only if the author asked for it.

## Per-response structure — five parts, substance-first

Open with substance, end with thanks (if any). ① facts/data → ② evidence →
③ stance → ④ landing → ⑤ acknowledge (optional, last, default omitted).
Typo/clarify → just ④ as the redline block. Detail in `references/writing-rules.md`.

## Boundary — what this skill is NOT

| Need | Goes to |
|---|---|
| Edit the manuscript tex per the locked decisions (surgical) | **sci-revise** — reads `issue-ledger.md`; default `revision_kind: surgical` |
| A passage the reviewer explicitly asked to polish | **sci-polish** — routed via sci-revise when `revision_kind: polish-needed` |
| Polish manuscript prose outside a revision round | sci-polish |
| Cover letter (first submission / revision) | sci-submit |
| Draw new data figures | sci-draw |
| LaTeX typesetting of the *manuscript* | sci-typeset |

sci-respond writes **only** the response letter.

## References (load on demand)

| File | When to read |
|---|---|
| `references/workflow.md` | Intake, checkpoint protocol, underlying-concern inference, Class-B strategy menu, viability |
| `references/writing-rules.md` | The three hard rules, five-part order, 6 strategies, compression, banned qualifiers |
| `references/latex-response.md` | Bundled template use, `\added`/`\deleted`, non-floating figures, cover page, compile, Word-via-pandoc |
| `references/state-contract.md` | `issue-ledger.md` schema, `change-log.md`, `INF:` anchors, `[TBD]`, safe-claim-boundary |
| `references/self-check.md` | Coverage audit, integrity firewall, independent-reviewer read, final search checklist |
| `docs/design-note.md` | Full design rationale — read when modifying the skill itself |
| `docs/cross-cutting-tricks.md` | Provenance of each adopted trick — read when questioning a rule's origin |

## Status

Design complete (`docs/design-note.md`); this SKILL.md is the executable form.
Sibling `sci-revise` (manuscript editing) is designed alongside — its rules live
in its own SKILL.md; this skill only writes the `revision_kind` field that
drives them.
