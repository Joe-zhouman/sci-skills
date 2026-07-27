# workflow.md — intake, checkpoint, draft orchestration

> Read this when running a revision round. Covers phases 1–2 of the SKILL.md
> Startup flow (intake + issue decomposition + checkpoint). Writing rules:
> `writing-rules.md`. LaTeX mechanics: `latex-response.md`. State schema:
> `state-contract.md`.

The whole flow exists to put the **author at the right Class-B decision point**.
Class-A decisions (template, layout, tex) are already made by the skill and are
not asked. The single checkpoint is where Class-B decisions (defend/concede/
experiment, claim narrowing, ambiguous intent) surface to the author.

---

## 1. Intake

### Read everything that grounds the response
A response is only as good as what it's grounded in. Read, in this order:

1. **The reviews** — `manuscript/rN/reviews/`. Raw text, preserved verbatim.
2. **The writing-stage notes** — `sci-skills/sci-write/`. These record the
   paper's *thinking* and are often more useful than the manuscript text:
   - `claim.md` — the one-sentence argument + evidence baseline + **boundary**.
     The response must not cross this boundary. Read first.
   - `paper-plan.md` — what each figure claims, section status.
   - `figN-reading.md` — the figure/evidence reading (what each figure actually
     shows vs. what was claimed). Grounding for data-backed defense.
   - `terminology-ledger.md` — term boundaries; keeps the response consistent
     with the manuscript's vocabulary.
3. **The figure reports** — `sci-skills/sci-draw/figN-report.md`. Statistics,
   data source, key findings — the evidence for data-backed defenses.
4. **The manuscript** — `manuscript/rN/tex/`. The text under revision; cite its
   sections/lines/figures.

If `claim.md` is absent (the paper wasn't drafted through sci-write), proceed
but flag it — the claim boundary is then inferred from the manuscript, which is
weaker. Ask the author to confirm the claim if a response nears a boundary.

### Completeness preflight
Classify readiness. A missing field can block drafting while analysis proceeds:

| Level | Meaning | Blocks |
|---|---|---|
| `complete` | reviews + manuscript + notes located | nothing |
| `analysis_ready` | enough to decompose; some notes missing | nothing yet, flag gaps |
| `partial` | some reviews missing or manuscript not located | drafting |
| `blocked` | reviews absent | everything — stop and ask |

If `blocked`/`partial`, ask for the smallest missing set. Do not proceed to draft.

### Viability gate — Class B (author decides)
An honest read of the overall picture before decomposing. Not every round is
worth a heavy response.

- **PROMISING** — at least one positive reviewer, concerns addressable. Proceed.
- **BORDERLINE** — scores cluster at the boundary; response is decision-critical.
  Proceed, flag criticality.
- **LOW EXPECTED RETURN** — all reviews below borderline, or core premise
  questioned. **Tell the author honestly before drafting a heavy response.** They
  may choose a lighter revision + resubmit elsewhere. Do not cheerfully draft a
  full response to a hopeless round.

This is honesty at the round level (hard rule 2). The author decides; the skill
surfaces the assessment.

---

## 2. Issue decomposition

Split each review into atomic issues. This is the analysis the checkpoint
presents.

### Stable IDs
`<reviewer>-Q<NN>` (e.g. `R1-Q03`), two-digit zero-padded. The join key —
sci-revise references it; the response cites it; the change-log records it.
Never reuse; dropped issues keep their ID with `status: dropped`.

### Per-issue decomposition
For each atomic issue (schema in `state-contract.md`):

1. **Surface comment** — verbatim quote.
2. **Underlying concern** — the decision-relevant doubt *behind* the wording.
   The most valuable single step. "Add baseline X" → underlying concern is
   "unfair comparison." Address the concern, not the literal ask. Common types:
   correctness/soundness · unfair or missing comparison · cherry-picking ·
   statistical reliability · overclaim/scope · reproducibility ·
   novelty/positioning · clarity (the writing caused a misread).
3. **Evidence that would resolve it** — fact/figure/citation/experiment. If
   none exists in the manuscript, it's a gap (flag; may need sci-revise to add
   content, an `INF:`-tagged inference, or a `[TBD]`).
4. **Proposed strategy** — one of the 6 (`writing-rules.md` §strategy-taxonomy),
   with a default recommendation = lowest-risk strategy that genuinely addresses
   the concern.
5. **Safe-claim-boundary** — how far the response can go given the evidence.

### Split / merge (within one reviewer)
- **Split** when two concerns in one comment need different evidence.
- **Do NOT merge across reviewers.** Even if R1 and R2 ask the same thing, keep
  them as separate issues (R1-Q03 and R2-Q01). See §2.2 — reviewers may not see
  each other's responses, so each must be answered in full in its own section.

### 2.1 Processing order — by priority, not by appearance (internal)

The **response letter's presentation stays point-by-point** by reviewer (R1's
Q1–Q14, then R2's Q1–Q6) — that is the journal standard and is not changed. But
the **order in which the skill and author work through the issues** is by
priority, not by Q-number. Process heavy/long-lead items first so they don't
block the round:

1. **Heavy / long-lead** — issues needing new computation, new experiment, or a
   claim-narrowing decision. These take time (the author may need to run
   something) and decide the claim's footing. **Process first.** These are the
   Class-B checkpoint decisions.
2. **Medium** — supplementary explanation, added discussion, new citation. No
   new data, but substantive writing. Process after the heavy ones are locked.
3. **Light** — typo, missing unit, formatting, missing reference. Batch these
   for last; they're quick and don't move the argument.

This ordering is internal (how the ledger is worked). The output order remains
point-by-point per reviewer. The two are independent — work in priority order,
present in reviewer order.

### 2.2 Cross-reviewer overlap — answer in full, do not reference

**Never handle a duplicated concern by referencing another reviewer's answer.**
Different reviewers may use separate submission systems, or the system may not
show one reviewer the response addressed to another. An answer like "this is
covered in our response to Reviewer 1 (page X)" is **empty** to a reviewer who
can't see Reviewer 1's section.

- If R1 and R2 raise the same concern, **answer it in full in each reviewer's
  section**. The wording may differ slightly, but the content must be complete
  in both.
- This is consistent with the first principle (every response self-contained):
  a response cannot rely on the manuscript *or* on another reviewer's section.
- The ledger keeps them as separate issues (`R1-Q03`, `R2-Q01`) linked by a
  `parallel_to` field so the skill knows they're the same concern and drafts
  consistent answers — but they are never merged into one response.

---

## 3. The checkpoint — single pause, Class B only

After intake + decomposition (all issues in the ledger, strategies proposed,
boundaries set), **stop**.

### What the author is asked (Class B — their decisions)
- For each **consequential** issue (any `defend`/`concede`/`experiment` stance,
  or where the proposed strategy is contested): a **2–4 strategy menu** with
  tradeoffs. Example for "reviewer wants a new experiment":
  1. run the experiment (highest evidence; cost/risk if negative)
  2. cite existing evidence that addresses it (lower cost; may not satisfy)
  3. concede the limitation and bound the claim (lowest cost; honest)
  Default recommendation is marked, but the author picks.
- **Ambiguous comments** — Intent Diagnosis Card: most-likely + alternative
  interpretation + a **safe response strategy** (wording valid under both). The
  author either disambiguates or accepts the safe strategy.
- **Viability** — if not PROMISING, the assessment is here for the author to act on.
- **`revision_kind`** per issue: `surgical` (default) vs `polish-needed` (only
  when the reviewer explicitly asked to polish that passage).

### What the author is NOT asked (Class A — already decided)
- template, cover-page layout, font/spacing — skill picked.
- tex vs Word — tex. (Word only if the author independently insists, via pandoc.)
- Response Figures non-floating — skill picked.
- overview default-on — skill picked (one-line opt-out exists, not a question).
- issue ordering — the ledger is *suggested* ordering; the author may reorder,
  but the skill does not auto-rank by a scoring formula (that would decide for
  them).

### Hard rule for the skill at the checkpoint
**Do not draft any response text before the author locks strategies.** The
pause is the point. Present the ledger, surface Class-B options, wait.

---

## 4. After the checkpoint — handoff to draft

Once the author locks the ledger:
- strategies are fixed; `issue-ledger.md` is the contract.
- drafting proceeds per-response (`writing-rules.md`, `latex-response.md`).
- after all responses: self-check (`self-check.md`), then compile.

The ledger is frozen for this round — sci-revise reads it as-is. Later changes
are new change-log entries (delta-only), not in-place mutations.
