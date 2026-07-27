# writing-rules.md — the response text itself

> Read this when drafting responses (phase 3 of the Startup flow). The three
> hard rules in detail, the five-part order, the strategy taxonomy, and the
> word-level discipline. For the LaTeX macros that implement several of these
> (`\added`, `\deleted`, `\quoteRevision`) see `latex-response.md`.

Every rule here serves the first principle: the reviewer must not have to open
the manuscript. Substance-first, honest, restrained.

---

## The three hard rules (in detail)

### Rule 1 — Self-contained (hard constraint)
Every response carries its own evidence. Concretely, one of these must be true
of each response:
- it quotes the revised manuscript text inline (the redline block for typo /
  clarify responses), **or**
- it shows the data / formula / figure that supports the answer (Response
  Figure / Table, non-floating, beside the text), **or**
- it states the manuscript location precisely (page + line, or section + label)
  **and** gives enough of the relevant content that the reviewer need not look.

Failure mode: "We have addressed this in the revised manuscript (Section X)."
with no further detail. That sends the reviewer to the manuscript — failed
response.

### Rule 2 — Honesty over embellishment
Facts as-is. Specifics:
- **Missing numbers → `[TBD]`.** Never invent a value the author hasn't
  supplied. The author fills `[TBD]` before submission.
- **AI inferences → tagged `INF:`.** Anything the skill inferred (not read from
  paper / review / experiment / code) is labeled `INF:` and visible as
  inference, not hard evidence. The reader knows the provenance.
- **Safe-claim-boundary.** Each issue has a boundary stating how far the claim
  can go given the evidence (from `state-contract.md`). Do not assert beyond it.
- **Banned qualifiers without evidence** (below). No "improves / outperforms /
  significant / robust / SOTA" unless backed by the relevant metric.
- **Plain admission when warranted.** "These predicted values are not
  experimentally validated" is written that way. A dressed-up justification has
  to be defended forever; the plain truth doesn't.

### Rule 3 — Acknowledgement restraint + anti-AI-pattern
- **Default: no acknowledgement.** Most responses (typo, clarification, "fixed,
  see X", data-backed) need none. The substance is the thanks.
- **When warranted** (heavy data-backed or concede): one short line, at the
  **end** of the response (part ⑤, after substance).
- **Opener must vary.** If acknowledgements appear across multiple responses,
  their openers differ — no repeated cadence, no rule-of-three. (Same lineage
  as `humanizer-zh`.)
- **Canonical failure:** "We sincerely appreciate your meticulous
  identification of the spelling errors…" on a typo fix. Never.

---

## Five-part order — substance-first

| Part | Role | Mandatory? |
|---|---|---|
| ① Facts / data | state data, formulas, refs — grounded | yes (the substance) |
| ② Evidence | Response Figure / Table (non-floating) | when the response needs a figure/table |
| ③ Stance | does this undermine the core conclusion? | when there's a stance to take |
| ④ Landing | where the change lands in the manuscript | yes (location always stated) |
| ⑤ Acknowledge | one short line | optional, default omitted, **last** |

- **First sentence = the direct answer.** Not "We thank the reviewer…" — the
  answer. "Yes. The improvement holds under matched compute." Then evidence,
  then revision. Thanks (if any) come at the end.
- **Depth is per-response.** Typo/clarify → just ④ as the redline block (no
  prose parts at all). Heavy data-backed → ①②③④, no ⑤. The skill picks the
  depth; the only fixed rule is *order*.

### Typo / clarification responses — format-over-prose
For typo and pure-clarification responses (🟢 trivial, sometimes 🟡
misunderstanding), use the **inline-redline quote block**, not prose:
- the original manuscript sentence as a block quote (left gray vertical bar —
  the existing `changes` environment shell)
- the change marked **inline**: `\added{...}` (bright green) for insertions,
  `\deleted{...}` (bright red + strikethrough) for deletions, unchanged text
  medium-gray
- partial quotes use a leading `...`; only the sentence containing the change
- **no acknowledgement, no explanatory prose** — the quote block IS the answer

See `latex-response.md` for the macros and the exact visual contract.

---

## Strategy taxonomy — 6 types

Mapped to the underlying concern at the checkpoint (`workflow.md` §2). Each
strategy implies a stance and a typical five-part shape:

| Strategy | When | Shape |
|---|---|---|
| **agree & revise** | reviewer is right, easy fix | ④ landing (often redline block); no ①②③ |
| **clarify without expanding** | reviewer misread; paper is fine, writing was ambiguous | ① facts (the clarification); ④ landing (small wording fix). Often 🟡 — fix the ambiguity in the manuscript too |
| **data-backed defense** | reviewer's concern is addressable with existing data | ①②③④ full — show the data/figure, state the stance, give the location |
| **concede limitation** | concern is real but the fix is out of scope | ① acknowledge; ③ stance (bound the claim); ④ landing (write the limit into Discussion). Honest, not defensive |
| **partial disagree** | partly right, partly not | ① caveat first (what's valid), then ②③ the defense of the rest |
| **external reference** | gap in the paper, fillable by citing existing work (incl. own preprint) | ① the reference; ③ why it addresses the concern; ④ where it's now cited |

Nearly no response is a bare "agreed, done." Every response carries evidence or
a stance — claim-driven + grounded at the response layer.

### Decision defaults (which strategy to propose at the checkpoint)
- concern is about framing / scope / positioning → lean **clarify** or
  **manuscript-light agree** (targeted wording, not a new experiment)
- reviewer identified genuine ambiguity in the paper → **direct manuscript edit**
  (agree & revise)
- the explanation would sound defensive if added to the manuscript → keep it in
  the **response only**, don't pollute the manuscript
- concern needs evidence the paper lacks → **data-backed defense** (if evidence
  exists) or **concede** (if it doesn't and can't be added in time)

---

## Word-level discipline

### Manuscript-light by default
Revise the manuscript only where it naturally supports the clarification.
Prefer targeted wording changes over adding defensive paragraphs. If a
Discussion sentence resolves the issue, do not force a new Methods/Experiments
block. If the added text would read as rebuttal-only defense, **keep it in the
response letter** — do not let it leak into the manuscript.

(This bounds `sci-revise`'s amplitude. The actual manuscript editing is
`sci-revise`'s job; this skill only states *what* the response promises.)

### Cross-reviewer overlap — answer in full, do NOT reference
When R1 and R2 raise the same concern, **do not** handle R2's by pointing at R1's
answer ("this is covered in our response to Reviewer 1, page X"). Different
reviewers may use separate submission systems, or the system may not show one
reviewer the response addressed to another — such a cross-reference is **empty**
to a reviewer who can't see the other section.

- Answer the concern **in full in each reviewer's section**. Wording may vary
  slightly; content must be complete in both.
- The manuscript edit itself is made once (sci-revise does it once, referenced
  by both issue IDs via `parallel_to` in the ledger) — but each response section
  states the change in full.
- This extends the first principle: a response is self-contained — it cannot
  rely on the manuscript, **nor on another reviewer's section**.

### Banned qualifiers without evidence
Do not use **improves / outperforms / significant / robust / SOTA / superior**
unless backed by the relevant metric or comparison in the response itself.
Replace with the plain claim + the number.

### Compression — when over length
If a response exceeds its length budget (venue limit, or self-imposed), remove
in this order:
1. repeated acknowledgements (first to go — matches rule 3)
2. repeated quotations of the reviewer
3. generic background / restatement of the paper's contribution
4. adjectives and qualifiers
5. duplicate responses (merge near-identical points)
6. low-impact minor comments (defer to a batched "minor comments" section)
7. implementation detail

**Preserve at all costs:** direct answers, key numbers, comparison controls,
stated uncertainty, claim narrowing, manuscript-change locations, unresolved
limitations.

The "preserve" list doubles as a statement of writing values — these are the
parts that matter.

### Tone — respectful, not obsequious
Respectful of the reviewer's time and expertise; not obsequious. The
posture is "here is the evidence," not "please believe us." Never speculate
about the reviewer's motives, never imply they didn't read carefully. (The
integrity firewall in `self-check.md` catches these.)
