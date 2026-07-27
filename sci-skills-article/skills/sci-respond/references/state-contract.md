# state-contract.md — the revision-round state files

> Read this when writing/reading the issue ledger. Defines the schema for
> `sci-skills/sci-revise/`. sci-respond **writes** the ledger during intake;
> sci-revise **reads** it to make manuscript edits. Co-read/write of one
> directory is normal in this family (sci-write/ is co-owned by write/story/
> polish — same pattern).

## Location — `sci-skills/sci-revise/` (shared, CONTRACT-governed)

All revision-round *process state* lives here:
```
sci-skills/sci-revise/
  issue-ledger.md      ← per-issue join key (sci-respond writes; sci-revise reads)
  change-log.md        ← delta-only audit trail (append-only)
  polish-todo.md       ← large newly-inserted passages needing polish
                         (sci-revise writes; sci-polish reads)
```

This directory is the shared state for the revision round — like `sci-write/`
is the shared state for the writing stage. Neither skill "owns" it exclusively;
both read/write via its CONTRACT. `manuscript/rN/` holds the formal products
(the revised tex, the response letter, the reviews); process metadata lives
here, not in `manuscript/`.

`polish-todo.md` is written by **sci-revise** (it finds large insertions while
editing). Documented here for cross-skill visibility; sci-respond does not write
it. See SKILL.md Boundary.

### What sci-respond reads (not writes) — the writing-stage products
The response is grounded in more than the manuscript. sci-respond **reads**:
- `sci-skills/sci-write/claim.md` — the claim boundary (do not cross)
- `sci-skills/sci-write/paper-plan.md` — figure claims, section status
- `sci-skills/sci-write/figN-reading.md` — figure evidence
- `sci-skills/sci-write/terminology-ledger.md` — term boundaries
- `sci-skills/sci-draw/figN-report.md` — statistics, data source, key findings

These record the paper's thinking and ground the underlying-concern inference
and the data-backed defenses. They are read-only to sci-respond.

---

## issue-ledger.md — schema

Thin index at top + one block per atomic issue. The index is a pointer, not a
dump — never duplicates full content.

### Thin index (top of file)
```
# Issue ledger — r1 (Communications Engineering, COMMSENG-25-0150-T)

round: r1
manuscript: manuscript/rN/tex/   (the version under revision)
viability: PROMISING
status: checkpoint               # intake | checkpoint | drafting | audited | done
reviewers: R1, R2
strategies_locked: no            # set yes after the checkpoint
```

### Per-issue block
```
## R1-Q03
- reviewer: R1
- surface_comment: "Please provide the reference of the thermomechanical
  properties of 316 stainless steel."   (verbatim)
- underlying_concern: provenance of material parameters; are they defensible?
- stance: data-backed defense
- evidence_anchors:
    - PAPER:methods.tex#thermo-params
    - REVIEW:R1:Q03
    - [1] Svahn 2024 (microhardness)
    - INF: supplier-provided E/ν not in a citable source
- safe_claim_boundary: parameters are defensible for this alloy; differences
  vs literature are small and don't move the conclusion. Do not claim supplier
  values are "more accurate" than literature.
- manuscript_action: add citation [1] at the parameter table; note supplier
  source for E/ν.   (routed to sci-revise)
- manuscript_location: manuscript/rN/tex/sections/methods.tex, parameter table
- revision_kind: surgical    # surgical | polish-needed
- safety: proposed           # proposed | approved
- status: draft-ready
```

### Field reference

| Field | Meaning | Values |
|---|---|---|
| `id` | stable join key | `<R>-Q<NN>`; never reused |
| `reviewer` | source | R1, R2, ... (or AE / Editor) |
| `surface_comment` | literal | verbatim quote |
| `underlying_concern` | the doubt behind it | free text (workflow.md §2) |
| `stance` | response strategy | agree&revise / clarify / data-backed defense / concede / partial-disagree / external-reference |
| `evidence_anchors` | what backs it | typed anchors (below) |
| `safe_claim_boundary` | how far the claim can go | free text; operationalizes honesty |
| `manuscript_action` | what sci-revise does | free text; "none" if response-only |
| `manuscript_location` | where | file + line/label; "n/a" if none |
| `revision_kind` | edit type | `surgical` (default) / `polish-needed` |
| `safety` | approval | `proposed` (checkpoint) / `approved` (locked) |
| `status` | workflow | `analyzed` / `draft-ready` / `drafted` / `audited` |

### Evidence anchor prefixes
Every claim traces to a typed anchor. The prefix is provenance:

| Prefix | Meaning |
|---|---|
| `PAPER:<file>#<anchor>` | read from the manuscript |
| `REVIEW:<reviewer>:<field>` | from the reviewer's comment |
| `EXP:<result-or-log>` | from an experiment result/log |
| `CODE:<path>#<symbol>` | from the codebase |
| `USER:<timestamp>` | supplied by the author |
| `INF:<short-id>` | **AI inference** — not hard evidence; labeled |

`INF:` is the cheapest hallucination guard. Inferred claims are `INF:` and the
reader knows; they are not presented as hard evidence.

### `[TBD]` discipline
Missing numeric values the author hasn't supplied → `[TBD]` in the response,
never invented. The ledger's `evidence_anchors` flags these as gaps to fill.

---

## change-log.md — delta-only, append-only

The audit trail. Records what changed and why — never stores current truth.
Append-only; never rewrite.

```
## 2026-07-27 — checkpoint locked
- R1-Q03 stance: clarified → data-backed defense (author chose option 2)
- R1-Q09 stance: partial-disagree → concede (author accepted the limitation)
- R2-Q03 Intent Diagnosis Card; author disambiguated → clarify

## 2026-07-27 — drafting
- R1-Q03 drafted
- R1-Q07 drafted (typo redline)
```

Old entries stay; the ledger points to current state, the log records how it got
there.

---

## polish-todo.md — interface to sci-polish (owned by sci-revise)

Documented here for cross-skill visibility; **sci-revise writes it**. sci-respond
does not.

Entry shape (large newly-inserted passages only):
```
- location: manuscript/r1/tex/sections/results.tex (after \label{fig:contact-area})
  snapshot: "To begin, we would like to clarify that the predicted contact area
             values are theoretical estimates, …"   (~first 120 chars)
  reason: new multi-paragraph mechanics explanation inserted for R1-Q09
  from_issue: R1-Q09
```
- **location** — file + anchor/line/label (sci-polish finds it without reading
  the whole manuscript)
- **snapshot** — opening ~N chars (locate after later shifts); not full text
- **reason + from_issue** — why + traceability

**Minor edits do not go here.** Token swaps, single sentences, typo fixes,
number updates, redlines — all stay out. Only large insertions (≥ one paragraph,
or ~3+ sentences of net-new prose).

---

## Why this structure

- **Stable IDs** are the join key between sci-respond (writes responses) and
  sci-revise (makes edits).
- **Thin index + delta log** separates "current truth" (ledger) from "how it got
  there" (log).
- **`revision_kind`** prevents sci-revise drifting into paragraph rewrites.
- **`safe_claim_boundary` + `INF:` + `[TBD]`** operationalize honesty — not "be
  honest," but "here is exactly how honest, and where."
- **Reading the writing-stage notes** grounds the response in the paper's
  thinking, not just its final text — the underlying concern and the claim
  boundary come from `claim.md` and `figN-reading.md`, which are often clearer
  than the manuscript.
