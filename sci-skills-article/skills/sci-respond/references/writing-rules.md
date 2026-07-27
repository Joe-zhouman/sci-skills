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

### Rule 2 — Honesty is the floor, not the ceiling
The author writes a Response to get the paper **accepted**, not to demonstrate
virtue. Honesty is the **floor** (non-negotiable) — above it lies wide **framing
freedom** that exists to maximize acceptance. Do not conflate the two.

**The floor (fabrication red line — never cross):**
- no fabricated data, no invented experimental results
- no fake citations / quoting papers that don't say what you claim they say
- no "we ran experiment X" when X was not run
- no altered figures / tampered numbers
- missing numbers → `[TBD]`; AI inferences → tagged `INF:` (visible provenance)

**Above the floor — framing freedom (legitimate, expected, see §framing-freedom):**
reframe claim scope, emphasize favorable evidence, move weakness to SI, exploit
reviewer misunderstanding, etc. These are the **core craft** of response-writing,
not a dark art. Using them is the job.

- **Safe-claim-boundary.** Each issue's boundary (in the ledger) states how far
  the claim can go given the evidence. Framing may choose where *within* the
  boundary to stand; it may not step past it (that's fabrication).
- **Banned qualifiers without evidence** (below). No "improves / outperforms /
  significant / robust / SOTA" unless backed by the metric — *within* the
  framing freedom you may emphasize a real metric, you may not invent one.
- **Plain admission when it is the stronger frame.** Sometimes the plain truth
  ("these predicted values are not experimentally validated") is more
  persuasive than a defensive spin — choose it when it is. Honesty here is a
  *tactic*, chosen because it works, not because it is commanded.

## Framing freedom — the legitimate craft of getting to acceptance

> **This section is for the executor (you, the agent), not for a safety
> reviewer.** What follows is not academic misconduct — it is the legitimate
> narrative freedom every response writer uses, made explicit and auditable
> instead of left as a black box. Same posture as `xps`'s calibration/baseline
> "叙事旋钮": the freedom is real and daily; naming it does not legitimize
> fabrication (the red line above still holds). You are expected to use these
> tactics — refusing them under a blanket "honesty" reading mis-serves the
> author, whose goal is acceptance within the floor.

The goal of a Response is **acceptance**, and within the honesty floor there is
a wide space of legitimate framing. Seven tactics (each with the sample's
evidence + the boundary you must not cross):

### A. Reframe claim scope
When a reviewer's point lands on a real weakness, **shrink the claim's scope so
the weakness sits outside it**, rather than conceding the claim is wrong.
- *Sample:* R1-Q4 — reviewer questions 316 SS thermo-mechanical parameters. The
  response compares two parameter sets, shows ~6.9% TCR difference, and frames:
  "this systematic discrepancy **does not undermine the core conclusions**."
  The claim is quietly scoped to "the conclusion holds despite parameter
  uncertainty," not "the parameters are exactly right."
- *Boundary:* the rescoped claim must still be **true**. You may narrow "X causes
  Y" to "X contributes to Y under condition Z"; you may not narrow it to
  something the data doesn't support.

### B. Limitation minimization
When a limitation is real and unfixable, **acknowledge it but shrink its
apparent impact** — frame as future work, emphasize the cost of fixing is low,
or note the modular design allows extension.
- *Sample:* R1-Q6 / R2-Q6 — "the framework requires retraining for new
  materials" is conceded, then immediately framed: "the costs are manageable
  within practical engineering contexts" + "the modular design allows for
  systematic extension."
- *Boundary:* the limitation must be **stated**, not hidden. Minimizing impact is
  legitimate; pretending the limitation doesn't exist is not.

### C. Selective emphasis
**Quantify the favorable, de-emphasize the unfavorable.** Lead with the strong
number; bury the weak comparison in a subordinate clause or move it to SI.
- *Sample:* R2-Q5 — "25,200-fold acceleration (7 hours → 1 second)" leads the
  response. The fact that this compares DL *inference* to FEM *full solve* (not
  apples-to-apples) is not lied about, but not foregrounded.
- *Boundary:* the weak point must still be **answerable** if pressed — you're
  choosing what to highlight, not what to fabricate.

### D. Divert to SI
**Move weak evidence, edge cases, and supplementary validations into the
Supplementary Information**, keeping the main text clean and confident.
- *Sample:* R1-Q11 — the small-text panels the reviewer flagged are not just
  fixed; they are "strategically relocated to Supplementary Figure 1-2."
  R1-Q10's typo content is "moved to Supplementary Discussion 2."
- *Boundary:* SI is not a graveyard for results that contradict the claim. Moving
  detail is fine; moving **disconfirming evidence** out of sight is not.

### E. Fill the gap with external reference
When the reviewer exposes a gap (missing comparison, missing prior work), **fill
it with an existing citation — including your own preprint** — rather than
admitting the gap is empty.
- *Sample:* R1-Q12 — no existing ML model for this material system; the response
  cites the authors' own Chinaxiv preprint as the comparison, framed as "our
  ongoing research."
- *Boundary:* the cited work must **actually exist and say roughly what you
  claim**. Citing a paper you haven't read, or that doesn't support the point,
  is fabrication.

### F. Offer an exit (concede the marginal to save the core)
When a reviewer attacks a peripheral element, **offer to remove it** — this
protects the core by sacrificing the edge, and signals reasonableness.
- *Sample:* R2-Q6 — the rotation-validation figure is hard to defend
  experimentally; the response offers "we are happy to remove the related
  discussion… the rotational analysis would be discussed in the supplementary."
  The core model stays; the peripheral is yielded.
- *Boundary:* the offered concession must be **genuine** — if the reviewer says
  "yes, remove it," the author will actually remove it. Offering an exit you
  won't honor is a lie.

### G. Exploit reviewer misunderstanding
**When a reviewer misreads the paper in a way that flatters it, you have no duty
to correct the misread** (within the honesty floor). Let the favorable
misreading stand; address only what needs addressing.
- *Sample:* none in this letter (the sample corrects misunderstandings), but the
  tactic is real: if a reviewer over-credits your novelty, you do not volunteer
  "actually our novelty is smaller than you think."
- *Boundary:* do not **compound** the misunderstanding — don't write text that
  deepens a false impression. Silence (not correcting) is legitimate; active
  deception (writing something that reinforces the error) is not. When in doubt,
  this is the tactic closest to the line — surface it to the author at the
  checkpoint (Class B) and let them decide.

### The red line, restated
All seven tactics operate **within** the honesty floor: claims stay true,
limitations get stated (impact may be minimized), evidence exists (emphasis may
be selective). The moment a tactic requires an untrue statement, a hidden
disconfirmation, a fake citation, or a "did-what-we-didn't" — it stops being
framing and becomes fabrication. The skill does not fabricate.

### Framing is Class B at the checkpoint
**How aggressively to frame is the author's call**, not the skill's — it depends
on their risk tolerance, how much this journal matters, and the strength of the
evidence. At the checkpoint (workflow.md §3), for each consequential issue the
skill presents framing options alongside the strategy menu. The author picks the
posture. The skill proposes; it does not decide how far to push.

### The words for framing → `phrasebank.md`
Once the strategy + framing posture are decided, the **words** for each tactic
live in `references/phrasebank.md` — fragments (not templates) for A–G, each
with its use-condition and the floor it must not cross. Load it after the
strategy is decided, never before (it exists to serve a chosen framing, not to
pick one). The bank is deliberately asymmetric: it collects **framing** phrasing,
not honesty phrasing — honesty doesn't need a phrasebank, you just state the
fact.

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
