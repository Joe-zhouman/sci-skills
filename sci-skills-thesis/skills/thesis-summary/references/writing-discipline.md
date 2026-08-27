# Writing discipline — summary write-time discipline (three gate protocols + honest boundaries)

Open this file before writing any section's prose. It governs WRITE-TIME discipline —
which gate each section runs, real-DOI point-verification, verb calibration, terminology
enforcement, write-then-record. It is NOT a pre-write outline. Mirrors intro's
`writing-discipline.md` at thesis scale, grafting spine's depth human-gate protocol for ②
(spec §②; SKILL.md rules 3-5).

The synthesis chapter is not a single article's conclusion — it callbacks every gap the
intro raised (the Intro↔Summary coherence lock's enforce side, spec §①), extracts
cross-chapter commonalities under a depth human-gate, and writes the outlook hooking
spine's Boundary. This file is the complete write-time discipline; zero dependencies.

---

## The three gate protocols (which gate runs where, what each enforces)

The summary's three sections have different natures, so they run different protocols —
matched, not compromised (spec §②). Running one gate throughout would either let ② 裸奔
(no depth gate on an architecture-level claim) or impose ceremony on ①③ (re-gating
already-settled architecture).

### ①③ framing gate — enforces FRAMING ALIGNMENT, not depth

Before ① (工作总结·逐 gap 收束) and ③ (展望) prose is written, echo an alignment block
and wait for the author:

- **an argument**: what this section covers, where it sits in the funnel;
- **a list**: ① — the per-gap closure list (gap → filling chapter → result essentials,
  in gap-map order); ③ — the outlook list + which spine Boundary / which chapter
  limitation each item hooks;
- **key terms**: canonical forms from `thesis-terminology-ledger.md`, plus anything you
  inferred rather than were told.

The gate enforces **framing alignment** — which gaps, closed how; which outlook items,
hooking which Boundary. It does NOT enforce depth (closure wording quality, outlook
reach) — that is author-judged residual (spec §门与 enforcement).

**UNCONDITIONAL — no gate-skip.** Do not import intro's "skip the gate when framing and
terms are unambiguous" condition: its "mirror sci-story gate-skip" attribution is false —
sci-story's gates have no skip condition; its human review says "Mandatory. Do not skip".
① is the lock-critical section; ③'s gate echo is cheap; a skip saves one round and risks
a mis-framed closure chain (spec §工作流 Step 1; F2).

### ② spine depth gate — pending candidates, author settles

② (共性提炼·创新点归纳) is an architecture-level claim (glossary common-extraction) —
the classic AI-destroys-it spot. It runs spine's protocol, not a framing gate:

1. AI proposes commonality candidates marked `pending` (extraction method: see
   `references/synthesis-guide.md` §②);
2. each candidate carries **tension-flags** (below) — questions, not verdicts;
3. the **author settles depth** (深刻 vs 似是而非 — deep vs plausible-but-hollow):
   adopt → `confirmed`; veto → replace or drop, before any prose is written;
4. only after settle does ②'s prose collect the confirmed commonalities.

**AI NEVER auto-adopts a candidate and NEVER gates depth.** The AI that checks "is this
commonality deep?" is the same one that generated the hollow candidate — checking depth
generates the very hollowness it checks (family spec §① / Load-bearing premise;
SKILL.md rule 4).

### The tension-flag protocol (questions-not-verdicts)

Each tension-flag on a candidate carries three parts — (a) the tension, (b) specific
evidence (which chapter, which §), (c) **a QUESTION for the author**. Never a verdict:
the AI asks; the author concludes (spine protocol, spec §工作流 Step 2).

---

## Tension-flag examples for commonality candidates

Three examples of well-formed tension-flags (the questions the author actually needs to
settle; mirror spine's questions-not-verdicts form):

1. **"Is this a cross-chapter mechanism or a similarity label?"** — both chapters used X
   ≠ the two chapters share the same *instantiation* of X. Chapter 1 applies framework X
   to object A and Chapter 2 applies framework X to object B is a similarity label unless
   the shared instantiation itself (the mechanism, not the name) does cross-chapter work.
2. **"Is the grounding surface-parallel or genuine progression?"** — a side-by-side
   listing of results (Chapter 2 did A; Chapter 4 did B; both look alike) is surface
   parallel. A genuine commonality is progressive: the pattern explains why the chapters
   *collectively* land something no single chapter lands.
3. **"Does the commonality restate the umbrella or add a stratum below it?"** — spine's
   umbrella already says the thesis-level claim; a commonality that merely restates it in
   other words is redundancy, not a new stratum. A confirmed commonality must sit *below*
   the umbrella — a stratum the chapters jointly establish that the umbrella alone does
   not state.

Each flag names the chapters/§ it reads evidence from, and ends in a question mark.

---

## Real-DOI boundary (F4)

The deliberate cut (spec §⑤) is the **systematic positioning search pass** — intro's
研究现状 kind of locating sweep. It is NOT the DOI verification discipline:

- ③ (展望) citing emerging work: **point-verify a real DOI via academic search** (the
  academic toolset), never fabricate from memory;
- hang the verified DOI as a real-DOI placeholder for the author to insert via Zotero —
  same placeholder format as sci-write/dissect/intro;
- no citation → no placeholder. The outlook can be pure prose — it is not a literature
  review, and inventing a citation to "support" a future direction is worse than citing
  nothing (spec §工作流 Step 3; F4).

---

## Verb calibration (per-section claim strength)

The three sections make claims of different kinds; verbs must match (spec §⑧, mirror
sci-story):

| Section | Verb strength | Verbs | Why |
|---|---|---|---|
| ① 工作总结 | strong past | 建立 / 表明 / showed / established / demonstrated | The chapters' results are landed facts |
| ② 共性提炼 | strong present | shows / establishes / collectively demonstrates | A confirmed commonality is an established stratum (author-gated) |
| ③ 展望 | hedged future | 有望 / 可能 / may / could / would | Future-facing speculation |

- **①②'s contribution statements carry no hedge** — "本章建立了 X" is a fact about
  landed work; "本论文可能表明了 X" understates what the thesis established.
- **③'s speculation carries no strong verb** — "展望将解决 X" overclaims a future no
  one has landed; "移除该 Boundary 后有望实现 X" is the right strength.

---

## Terminology enforcement (canonical forms)

Read `thesis-terminology-ledger.md` (spine seed + dissect/intro extensions) and enforce
canonical forms in the synthesis tex — the same variable/method gets the same word in
every section (spec §⑦; mirror sci-write/dissect/intro co-write mode):

1. **enforce**: spine/dissect/intro canonical forms, verbatim, across all three sections;
2. **extend**: summary-level terms the synthesis introduces (summary-level unified
   phrasings, the 共性 names) → append to the ledger marked `source: thesis-summary`;
3. **do not touch** the article family's `sci-skills/sci-write/terminology-ledger.md` —
   cross-family term unification is out of scope (family spec v1 cut).

---

## Write-then-record (the baton records what landed)

summary-map.md entries are recorded **after** each section's tex lands — record what
landed, not what was proposed (spec §③):

- **post-write record is the baton**: Callback entries record how the prose actually
  closed each gap; Commonality entries record the confirmed commonalities the prose
  actually collects;
- **pre-write settle is the gate**: ②'s candidates settle before prose (a veto then costs
  zero prose churn). These are two different acts, both real — the named residual (spec
  §③): pre-settle is legitimate because candidate grounding is queryable pre-write from
  chapter-map.md + chapter results; the record stays post-write because prose is what
  landed;
- a settled candidate dropped while writing → record what landed + surface to the author
  (do not silently re-point the record at prose that isn't there).

---

## Privacy + the honest boundary

**Privacy** (mirror sci-story / intro): no private local paths, private filenames, or
unpublished content in summary-map.md, the synthesis tex, commit messages, or
user-facing replies. Use generic references ("Chapter 3 §2"); exact paths only when the
author asks for an audit trail.

**The honest boundary** (spec §门与 enforcement + §① residual; SKILL.md rule 7):

- the mechanical gate (`check_summary.py`) prevents **absence** (a gap with no Callback)
  + **bureaucratic lapse** (fabricated Gap numbers / dangling chapter numbers / pending
  residue) — nothing more;
- **depth is not machine-checked**: a fabricated `resolved-how` whose closure was never
  written passes the gate (prose-vs-promise — author + eval); a 似是而非 commonality the
  author wave-throughs passes everything (attachment blindness — the Load-bearing
  premise's inherent boundary);
- the gate is a **write-time check, not a post-polish invariant** (F6): after polish
  edits synthesis prose, nobody re-verifies resolved-how against the prose — prose
  drifts, re-verification would be fragile ceremony (mirror intro's anchor-in-intro
  demotion).

Name these plainly; never present the gate as a "coherence guarantee."
