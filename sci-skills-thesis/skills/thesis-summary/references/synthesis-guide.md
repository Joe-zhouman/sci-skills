# Synthesis guide — the three-section funnel (逐 gap 收束 / 共性提炼 / 展望)

Open this file at Steps 1-3 — it guides the synthesis chapter's funnel structure and
craft. It covers WHAT each section contains and HOW to work its material; the gate
protocols and write-time discipline that wrap every section live in
`references/writing-discipline.md` (spec §② + §工作流).

The synthesis chapter is the thesis's closing argument, not a replay: it closes the
intro's gaps, extracts what the chapters collectively establish, and opens what the
spine's Boundary leaves for the future. Chapter conclusions appear only as evidence —
never as a section of their own (spec §②; family spec §4's pain point).

---

## ① 工作总结·逐 gap 收束 (close every gap, in gap-map order)

**The opening restates the settled umbrella.** One short paragraph re-articulates the
settled thesis-level claim from `thesis-spine.md` as the synthesis anchor — sci-story's
fuse-conclusion-into-opening at thesis scale (the claim leads; the narrative follows it).
**Narrate, don't re-gate, don't re-argue** — the spine settled the architecture; ①'s
opening retells it as accomplished, it does not relitigate it (spec §②).

**Then close the gaps one by one, in gap-map.md's order.** Each gap gets one short
paragraph with three moves:

1. **the gap** — restated in the intro's own wording. Read the intro tex (via gap-map.md's
   `intro-tex` field); the closure must answer the gap as the intro raised it, not a
   paraphrase that drifts the promise (spec §工作流 Step 0);
2. **the chapter that fills it** — its contribution, as established (strong verbs; see
   `references/writing-discipline.md` §verb calibration);
3. **result essentials** — cited to the chapter's sections ("Chapter 3 §2"), a result
   highlight. **NOT a chapter replay**: one or two results that carry the closure, not
   the chapter's full finding list.

**Forbidden: per-chapter replay** (逐章复述) — walking the chapters in order and
restating each one's conclusions. That is family spec §4's pain point in its purest
form: the thesis reads as N+2 stacked modules and the spine never reaches the last page.
The gap is the unit, not the chapter; a chapter whose results appear in two different
gap closures is fine, a chapter with its own summary paragraph is not.

**Fallback** (spec §④; SKILL.md rule 6): a gap whose closure doesn't honestly hold →
`status=unfilled` → stop & surface. The author decides: backtrack (dissect 补章 / intro
砍 gap / spine 修主线) or cut the promise. Never write a closure the results don't
support, and never edit a sibling product to make one hold.

---

## ② 共性提炼·创新点归纳 (cross-chapter commonalities under the depth gate)

This is the section AI cannot be trusted alone with — architecture-level claim
(glossary common-extraction). The full gate protocol (pending candidates + tension-flags
+ author settle) is in `references/writing-discipline.md`; this section covers the
extraction and the prose.

**Candidate extraction method**:

1. read `chapter-map.md`'s framework-instantiations **side by side** — how each chapter
   instantiated the unified framework, next to each other;
2. read each chapter's results (via chapter-map.md's `tex-file` → `thesis/tex/chN.tex`);
3. a candidate is a pattern that holds at the **mechanism / method / insight level
   across ≥2 chapters** — NOT "both used X" surface parallelism (see
   writing-discipline.md's tension-flag ①: a similarity label is not a mechanism).

**Per candidate**: one sentence stating the pattern + `grounded-in` — for each grounding
chapter, the specific § + result that grounds it (≥2 distinct chapters; the definitional
floor of "cross-chapter"). Grounding is queried from disk pre-write, which is exactly why
candidates settle **pre-prose** at the depth gate (spec §③): a veto then costs zero
prose churn — a vetoed candidate is dropped before anything is written.

**Prose for each confirmed commonality** — three moves, in order:

1. **the pattern** — stated once, in its own name (a term worth adding to the
   terminology ledger as `source: thesis-summary`);
2. **the per-chapter evidence** — each grounding chapter's § + result, cited like ①'s
   result essentials;
3. **what it means below the umbrella** — the stratum the chapters collectively
   establish that the spine's umbrella alone does not state. A restatement of the
   umbrella is redundancy, not a stratum (tension-flag ③); the confirmed commonality
   must add a level, not echo one.

Only confirmed commonalities get prose. Pending or vetoed candidates appear nowhere in
the synthesis tex.

---

## ③ 展望 (outlook grounded in Boundary / limitation)

**Every outlook item MUST hook a specific spine Boundary or a chapter limitation** — no
free-floating "future work" boilerplate (spec §②; SKILL.md Step 3). Enforcement is eval
+ framing gate (展望 has no baton entry), so the discipline lives here:

**Method**:

1. list spine's Boundary items (what the umbrella does NOT establish — the settled
   perimeter) + each chapter's limitations (from its results/prose, honestly read);
2. propose outlook candidates, each mapped to one hook: which Boundary or which
   limitation it answers;
3. gate echo (the outlook list + each item's hook) → author aligns framing → write
   (framing gate, UNCONDITIONAL — see writing-discipline.md).

**Grounded writing**: each outlook item states (a) what that Boundary/limitation blocks
today — the concrete thing the thesis could not do, and (b) what removing it would
enable — the capability that opens. Not a wish list: "future work could explore X" with
no hook is exactly the boilerplate this section forbids. Hedge the future (有望 / may /
would — verb calibration); a Boundary-hooked speculation stated as a plan reads as a
promise the thesis won't keep.

**Citations**: ③ may cite emerging work that bears on a direction — point-verify a real
DOI via academic search, never fabricate (F4; see writing-discipline.md §real-DOI
boundary). No citation needed is also fine — the outlook can stand on the thesis's own
Boundary.

---

## Chapter naming (synthesis tex, template-derived)

The synthesis tex filename comes from `template-spec.md` — the university template's
convention for the 总结展望 chapter (e.g. `chapter5.tex` on a generic template). It is
recorded in summary-map.md's `synthesis-tex` field and **never hardcoded** by the skill:
`check_summary.py` verifies the named file exists in `thesis/tex/` and rejects absolute
paths / `..` traversal (mirror intro's `intro-tex` / aries #2; spec §⑥ check 5). If
template-spec.md is ambiguous about the synthesis chapter's name, ask the author — do
not guess a convention the template doesn't state.
