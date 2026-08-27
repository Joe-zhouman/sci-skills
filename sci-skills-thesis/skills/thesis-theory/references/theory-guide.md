# Theory guide — the 共用理论方法 chapter (component extraction + framework instantiation)

Open this file at Steps 1-2 — it guides the extraction craft and the chapter's
structure: what a shared component is and how to extract candidates, how the
chapter opens by instantiating spine's unified framework, the method-layer vs
contribution-layer split against summary's 共性提炼, overlap discovery while
writing, the waived minimal chapter. The gate protocols and write-time
discipline that wrap every act live in `references/writing-discipline.md`
(spec §① + §工作流).

The chapter's two failure modes are symmetric (spec Problem 1): a chapter full
of forced/trivial components reads as 方法拼接 with the spine's framework
hollowly instantiated; a chapter that lifts nothing leaves the body chapters'
shared dependencies without a home. The craft is to land between them.

---

## 1. Component extraction method (Step 1)

Read the body chapters' method/theory 段 **side by side** — via chapter-map.md's
`tex-file` field, each `thesis/tex/chN.tex` next to the others. The comparison
IS the method: a shared component is visible only across chapters, never inside
one. All material is thesis-internal (信息流单向收敛: papers → spine/dissect
products → theory works from thesis-internal material; do not re-read the small
papers — dissect already digested them, spec §⑤).

A component candidate = a theory/method that **≥2 chapters GENUINELY depend
on** (a shared foundation) — not surface co-use (writing-discipline.md's
tension-flag ①: 两章都用了 X ≠ 两章共同依赖 X 的同一理论基础).

**Per candidate**, three fields:

1. **component** — one sentence: the shared theoretical basis / experimental
   method (a 共用组件), not a surface similarity label;
2. **grounded-in** — for EACH grounding chapter, the specific § + method that
   grounds it (≥2 distinct chapters, the definitional floor of "shared"; the
   chapter numbers must exist in chapter-map.md). Grounding is queried from
   disk pre-write, which is exactly why candidates settle **pre-prose** at the
   depth gate (writing-discipline.md §1): a veto then costs zero prose churn —
   rejected candidates drop without churn (spec §①);
3. **instantiates-framework** — one sentence tying the component to spine's
   Unified framework (the chapter's organizing skeleton): which layer of the
   framework this component instantiates.

---

## 2. Framework-instantiation narration (Step 2 opening)

The chapter opens by **narrating spine's unified framework** — the settled
architecture retold as the thesis's theoretical floor. **Narrate, do NOT
re-gate** — the framework settled in spine; the opening retells it, it does not
relitigate it (intro §④'s narrate-not-re-gate argument, applied to the writing
act; spec §①).

Then the confirmed components organize under it: **each confirmed component
instantiates one layer of the framework** — its section shows that layer at
work as the shared foundation the body chapters stand on, each grounding
chapter's usage as evidence. A component that cannot be placed under a layer is
a framing question for the author at the gate, not something prose can paper
over.

The chapter must read as **"the theoretical floor every body chapter stands
on,"** not a concatenation of methods: section order follows the framework's
layers (the framing gate's (a) structure echo), not the order components
happened to be extracted in — a chapter ordered by extraction reads as a
methods shelf, which is the 方法拼接 failure mode (spec Problem 1).

---

## 3. Method-vs-contribution layer split (vs summary ②)

theory and summary ② both run spine's depth human-gate on cross-chapter
extraction — but they extract **different objects** (spec §⑧: same protocol
lineage, different object — 同协议新应用, not reuse):

- **theory extracts METHOD/THEORY-layer sharing**: foundations and methods the
  chapters stand ON;
- **summary ② extracts CONTRIBUTION-layer commonalities** (创新点归纳): what
  the chapters collectively ESTABLISH.

Do not duplicate summary's prose here — the theory chapter is upstream
infrastructure, not a claims summary. **If a candidate smells like a
contribution claim** ("the chapters collectively demonstrate X"), it belongs to
summary, not this chapter; if it smells like a foundation ("the chapters all
stand on X"), it belongs here. When the prose collides anyway, that is
prose-layer (author/polish territory) — no structural check (spec §⑤ honest
boundary).

---

## 4. Overlap discovery (while writing each component's section)

Lifting a component out of the body chapters creates the overlap: the same
method now lives in the theory chapter and in each grounding chapter's method
段. **Discovery happens while writing** the component's section — for each
grounding chapter, locate where its method 段 carries the lifted material, and
record **one Overlap entry per (component × chapter-location) pair** (per-pair,
not per-component merged — the author resolves position by position; a clean
checklist, granularity mirrors summary's per-gap Callback):

- `theory-§` — where the lifted material landed in the theory chapter;
- `chapter-ref` + `chapter-§` — the body chapter location carrying the
  overlapped material;
- `suggested-disposition` — a suggestion, never an edit.

**Disposition guidance** (the suggestion's two shapes):

- **章内留 brief recap + cross-ref 第二章** (default) — the chapter keeps a
  brief local orientation and points at the theory chapter for the full
  treatment; readers of one chapter need local orientation, not a detour to
  chapter 1 mid-method;
- **theory 收编章内简化** — when the chapter's treatment is redundant with the
  theory chapter's, the theory chapter absorbs it and the chapter's copy
  shrinks.

**The AUTHOR adjudicates** — record the suggestion, never edit the chapter
(the Overlap 清单's resolver is the AUTHOR: theory writes last, body chapters
are settled, cross-skill editing is rework — aquarius #9 cut; no downstream
skill enforces resolution, spec §③). Record as you go: an overlap located
while writing but recorded later must be re-located, and an unrecorded overlap
is an absent-class failure the check cannot catch (writing-discipline.md §5).

---

## 5. Waived minimal-chapter mode (fallback b)

When all candidates are vetoed / no genuine sharing exists, the author may
adjudicate **裁最小章 (waived)**: `extraction-outcome: waived-by-author` lands
on disk (the author's decision footprint — check_theory.py recognizes it as a
legal terminal, NOT a vacuous pass), and Step 2 writes a
**framework-narration minimal chapter**:

- **narrate the unified framework** + a per-chapter instantiation overview —
  how each body chapter instantiates spine's framework, material spine already
  settled;
- **lift nothing** — no method sections, no Shared entries, no Overlap
  entries: the Shared/Overlap 段 stay empty (legal ONLY under waived;
  confirmed-but-empty is the vacuous-pass guard's target);
- the gate echo **degrades to (a) structure + (c) key terms** — no (b)
  component allocation, because there are no components; prose depth is
  eval + author territory.

The other fork — backtrack spine — stops the skill and leaves pending residue
(an honest non-terminal; spine re-settles, then resume). theory never
restructures the architecture itself; both roads are the author's call
(SKILL.md rule 4).

---

## 6. Chapter naming (theory tex, template-derived)

The theory tex filename comes from `template-spec.md` — the university
template's convention for the 共用理论方法 chapter (the chapter1 slot init
reserved in `main.tex`; 写入顺序 ≠ 阅读顺序). It is recorded in theory-map.md's
`theory-tex` field and **never hardcoded** by the skill: `check_theory.py`
verifies the named file exists in `thesis/tex/` and rejects absolute paths /
`..` traversal (mirror intro's `intro-tex` / summary's `synthesis-tex`). If
template-spec.md is ambiguous about the theory chapter's name, ask the author —
do not guess a convention the template doesn't state.
