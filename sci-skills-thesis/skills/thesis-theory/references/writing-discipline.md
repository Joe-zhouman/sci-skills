# Writing discipline — theory write-time discipline (two gate protocols + honest boundaries)

Open this file before any act — it governs which gate each act runs and what
each enforces: the Step 1 depth human-gate, the Step 2 framing gate, real-DOI
point-verification, terminology canonicalization, write-then-record, the
honest boundary. It is NOT a pre-write outline. Mirrors summary's
`writing-discipline.md`, grafting spine's depth human-gate for the enumeration
act (spec §①; SKILL.md rules 1-2). The extraction craft itself lives in
`references/theory-guide.md`.

The chapter's two acts have different natures, so they run different protocols
— matched, not compromised (spec §①): one gate throughout would either let
enumeration 裸奔 (no depth gate on a genuinely-new selection) or impose
ceremony on writing (re-gating architecture spine and Step 1 already settled).

---

## 1. The two gate protocols (which gate runs where, what each enforces)

### Step 1 enumeration — spine-protocol depth human-gate

Enumerating which theory/method components are genuinely shared across body
chapters is a depth decision AI cannot be trusted alone with — the method-layer
sibling of summary ②'s commonality gate (same protocol lineage from spine,
different object: method/theory 层 vs 贡献层). The protocol:

1. AI proposes component candidates marked `pending` — each = one-sentence
   component + `grounded-in` ≥2 distinct chapters + `instantiates-framework`
   (extraction method: `references/theory-guide.md` §1);
2. each candidate carries **tension-flags** (below) — questions, not verdicts;
3. the **author settles depth** (深刻 shared foundation vs 强行拼接 forced
   splicing): adopt → `confirmed`; veto → replace or drop — nothing is written
   yet, zero prose churn;
4. only after settle does Step 2 write.

**AI NEVER auto-adopts a candidate and NEVER depth-gates.** The mechanical
grounded-in ≥2 distinct chapters catches *invented* sharing (a chapter number
that doesn't exist); it cannot catch *forced/trivial* sharing ("都用了误差
分析" — technically used by all, a shared theoretical foundation for none). The
AI that checks "is this shared foundation genuine?" generated the hollow
candidate — checking depth generates the very shallowness it checks (family
spec §① / Load-bearing premise; SKILL.md rule 1).

### Step 2 writing — per-section framing gate, UNCONDITIONAL

Before each section's prose, echo an alignment block and wait for the author:

- **(a) section structure**: how the confirmed components organize + the
  framework-instantiation opening narrative direction;
- **(b) per-section component allocation**: which sections collect which
  components — the pre-write commitment constrains prose (SKILL.md rule 5);
- **(c) key terms**: canonical forms from `thesis-terminology-ledger.md`, plus
  anything you inferred rather than were told.

The gate enforces **framing alignment** — structure, allocation, terms — NOT
depth (whether the prose genuinely instantiates the framework is
prose-vs-structure, eval + author territory). Writing narrates settled
architecture: intro §④'s narrate-not-re-gate argument applies to the WRITING
act only (framework settled in spine, components in Step 1 — re-gating is
ceremony, spec §①); it does NOT reach the enumeration act, a genuinely-new
selection — the asymmetry is why Act 1 needs the depth human-gate and why a
pure framing gate was rejected.

**UNCONDITIONAL — no gate-skip** (mirror summary F2). A skip saves one echo
round and risks a chapter that drifts from the settled components.

### The tension-flag protocol (questions-not-verdicts)

Each tension-flag on a candidate carries three parts — (a) the tension,
(b) specific evidence (which chapter, which §), (c) **a QUESTION for the
author**. Never a verdict: the AI asks; the author concludes (spine protocol,
spec §工作流 Step 1).

---

## 2. Tension-flag examples for component candidates

Four examples of well-formed tension-flags (the questions the author actually
needs to settle; mirror spine's questions-not-verdicts form):

1. **"Is this a genuine shared theoretical foundation or surface co-use?"** —
   两章都用了 X ≠ 两章共同依赖 X 的同一理论基础. "都用了误差分析" is trivial
   共用 — surface co-use does not lift.
2. **"Is the grounding co-dependence or surface parallelism?"** — a side-by-side
   listing of methods (Chapter 2 used A; Chapter 3 used B; both look alike) is
   surface parallel. Genuine sharing is co-dependence: the chapters lean on the
   same foundation, not merely stand next to it.
3. **"Does the component's instantiation of the framework contradict how a
   grounding chapter actually uses it?"** — the `instantiates-framework`
   sentence ties the component to spine's Unified framework; if a grounding
   chapter's actual usage contradicts that instantiation, the candidate is
   suspect (instantiates-framework 与正文用法矛盾 = 候选可疑).
4. **"Does the component restate the framework or instantiate it?"** — a
   component that merely retells spine's framework in other words adds nothing
   (复述 spine 框架 = 冗余); a confirmed component must instantiate a layer of
   the framework, not echo it.

---

## 3. Real-DOI discipline

The theory chapter cites foundational literature (the theories and methods it
lifts and unifies) — citations are this chapter's ordinary business:

- **point-verify a real DOI via academic search** (the academic toolset) for
  every citation, never fabricate from memory — a foundational citation is
  where a hallucinated reference does maximal damage;
- hang the verified DOI as a **real-DOI placeholder** for the author to insert
  via Zotero — same placeholder format as sci-write/dissect/intro/summary;
- **no citation → no placeholder**. Inventing a citation to "support" a theory
  the chapter unifies is worse than citing nothing (mirror summary F4;
  spec §工作流 Step 2).

---

## 4. Terminology enforcement (the theory chapter is where shared notation gets canonicalized)

Read `thesis-terminology-ledger.md` (spine-seeded + dissect/intro/summary-
extended entries) and enforce canonical forms in the theory tex:

1. **enforce**: existing canonical forms verbatim — same method, same word;
2. **canonicalize**: when two chapters used different notation for the same
   object, the theory chapter picks the canonical form, uses it throughout, and
   records it in the ledger. The Overlap 清单's recap dispositions should point
   chapters at this canonical form;
3. **extend**: shared-theory terms the chapter introduces → append to the
   ledger marked `source: thesis-theory` (mirror sci-write/dissect/intro/
   summary co-write mode, spec §⑦).

---

## 5. Write-then-record (the baton records what landed)

theory-map.md entries are recorded **after** each section's tex lands — record
what landed, not what was proposed (spec §②):

- **overlaps are discovered while writing**: lifting material out of a body
  chapter's method 段 is what surfaces the overlap — record the Overlap entry
  as you go; reconstructing locations after the fact means re-locating them,
  and an absent entry is the absent-class failure the check cannot catch
  (aquarius T5);
- **pre-write settle is the gate**: candidates settle before prose (a veto then
  costs zero prose churn). These are two different acts, both real — the named
  residual (spec §②): pre-settle is legitimate because candidate grounding is
  queryable pre-write from on-disk body chapters (chapter-map + chN.tex); the
  record stays post-write because prose is what landed;
- **a pre-settled candidate dropped while writing** → record what landed +
  surface to the author (do not silently re-point the record at prose that
  isn't there).

---

## 6. Privacy + the honest boundary

**Privacy** (mirror sci-story / summary): no private local paths, private
filenames, or unpublished content in theory-map.md, the theory tex, commit
messages, or user-facing replies. Generic references ("Chapter 3 §2"); exact
paths only on the author's audit-trail request.

**The honest boundary** (spec §门与 enforcement; SKILL.md rule 6):

- the mechanical gate (`check_theory.py` — a near-trivial consistency 门)
  prevents **absence** (missing or illegal `extraction-outcome` /
  confirmed-but-empty Shared 段 / missing theory-tex file) + **官僚 lapse**
  (fabricated Shared or chapter numbers / dangling refs / pending residue) —
  nothing more;
- **depth is not machine-checked**: forced/trivial sharing the author
  wave-throughs at the depth gate passes everything (attachment blindness — the
  Load-bearing premise's inherent boundary); a fabricated § location whose
  section never carried the lifted material passes too (prose-vs-structure —
  eval + author);
- **overlap coverage completeness is not machine-checked**: an entry that was
  never recorded makes the checklist look complete — that absent-class failure
  rides on write-then-record discipline + eval (aquarius T5);
- the gate is a **write-time 检查, not a post-polish invariant** (mirror
  summary F6): after polish edits the theory chapter's prose, nobody
  re-verifies overlap locations against the prose.

Name these plainly; never present the gate as a "coherence guarantee."
