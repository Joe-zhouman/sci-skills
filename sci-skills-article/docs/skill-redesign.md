# Article skill redesign — design note

Status: **implemented (batches 1–4).** Recorded 2026-07-24; implemented 2026-07-23.
This documents a refactor of the article skill family. D1–D5 and migration
tasks 1–7 are done; the SKILL.md files now match this design. Deferred items
(docx standard template, sci-revise skill) are tracked in Open questions.

## Motivation

Two frictions surfaced during use:

1. **md → tex conversion is not smooth and not trustworthy.** md and tex have
   different writing idioms — md leans document-style (bold/italic tags), tex
   is natively paper-oriented (floats, citations, cross-refs, math). The
   `md-pandoc-tex` path converts between two paradigms and loses fidelity.
2. **sci-polish is too heavy.** It owns both prose (wording, structure,
   claim/evidence) and LaTeX layout/typesetting. The two pull in different
   directions and make the skill hard to reason about.

## Decisions

### D1 — Write directly in tex; drop the md intermediate layer

- **sci-write** and **sci-story** produce **tex sections**, not md drafts.
- md survives only as *working notes* (`claim.md`, `paper-plan.md`,
  `terminology-ledger.md`, reading notes) — files that are not part of the
  manuscript and never enter tex.
- `sci-export` Mode 1 (`md → tex`) is retired. There is no conversion step;
  writing and final format are the same language.

_why_ tex compiles to PDF, which is more readable than rendered md. Writing in
the target language removes a lossy translation and an untrustworthy tool
(pandoc) from the critical path.

### D2 — Split sci-polish; introduce sci-typeset

sci-polish is split into a pure-prose skill and a new typesetting skill.

| Skill | Owns | Does NOT own |
|---|---|---|
| **sci-polish** (slimmed) | prose: wording, paragraph/section structure, claim/evidence consistency, terminology ledger, language rules, Chinese-to-English | float placement, layout, template styling |
| **sci-typeset** (new) | LaTeX typesetting best practices on our template: loose pages, stranded headings, oversized tables, compile to PDF | prose content |
| **sci-export** (re-scoped) | moving the finalized tex into a target journal template (optional); tex → docx (optional). On template move, decides float strategy per the journal's convention (end-of-document / inline / per-chapter) | prose, typesetting-best-practice layout |

_why_ prose and typesetting pull in different directions and have different
review surfaces (prose wants `git diff` reading; layout wants visual PDF
inspection). Splitting lets each skill load only its own references and apply
its own review discipline.

### D3 — float placement is a journal-template concern, owned by sci-export

- During write / story / polish, tex uses plain `\input` or minimal figure
  environments with **no placement specifier** (or a placeholder). Authors
  only manage prose and the `\label`/`\ref` reference graph.
- `sci-typeset` works on **our template** and applies our template's best
  practices; it does not decide float *strategy* — only fixes readability
  issues (stranded headings, loose pages, table width) within our template.
- `sci-export`, when moving into a target journal template, decides float
  strategy per that journal's convention (e.g., "floats at end of document").
  This is where "float at end" lives — as a **template orientation**, not a
  global mandatory rule.

_why_ "where do floats go" is a question about the *target container*, not
about the prose. Putting it at the export/typeset boundary means write/story/
polish never have to think about it, and float drift stops being a problem the
prose author chases. "Floats at end" is our default template's orientation;
another journal's template may differ, and export honors that.

### D4 — SI is a by-product of sci-write, not a separate skill

- Supplementary Information (SI) content — large tables, method details,
  extra figures — is produced **by sci-write** alongside results/method, not by
  a dedicated SI skill.
- sci-story (intro/discussion/abstract) does **not** produce SI; narrative
  sections don't carry supplementary material.
- SI lives with the manuscript under `manuscript/v1/` (e.g. a `si/` subdir or
  `si.tex`), produced during the same write pass.

_why_ SI is structurally tied to results/method (it's the overflow of those
sections). Splitting it into its own skill invents a coordination boundary that
doesn't exist in the work — writing results *is* writing SI for the parts
that don't fit the main text.

### D5 — Draft directly in `manuscript/v1/`; drop the `sci-skills/sci-write/` intermediate layer for products

- First-draft tex is written **directly into `manuscript/vN/tex/`**. No
  "draft in `sci-skills/sci-write/` then move into `manuscript/`" two-step.
- `sci-skills/sci-write/` is retained as the **working-notes area only** —
  process metadata that is not part of the manuscript: `claim.md`,
  `paper-plan.md`, `terminology-ledger.md`, reading notes. Product tex never
  lands here.
- This is a first-draft concern. **Revision is a separate skill** (not yet
  designed — see "Open questions"); revision has its own flow and lives in
  `manuscript/rN/`.

_why_ the `sci-skills/sci-write/` → `manuscript/vN/tex/` hop was pure overhead
for first drafts: write produces tex, tex's home is `manuscript/`, so write it
there. The intermediate copy step existed only because products were md (which
had no manuscript home). Once products are tex, the hop is gratuitous. Working
notes stay in `sci-skills/sci-write/` because they're process metadata, not
manuscript content — mixing them into `manuscript/v1/` would pollute the
manuscript directory. Consistent with sci-draw, which keeps its process
artifacts (scripts, reports) under `sci-skills/sci-draw/`.

## Resulting skill map

```
article-init      scaffold + directory contracts (no layout orientation preset)
sci-write         data-driven tex sections: method / results / conclusion / SI (by-product)
                  → writes directly into manuscript/vN/tex/; working notes in sci-skills/sci-write/
sci-story         narrative tex sections: intro / discussion / abstract / keywords (no SI)
                  → writes directly into manuscript/vN/tex/
sci-polish        prose only — wording, structure, claim/evidence, terminology, language
sci-typeset       LaTeX typesetting on our template + compile PDF (readability fixes)
sci-export        (optional) move into target journal template / (optional) tex → docx
sci-submit        submission campaign
sci-revise        (TBD — separate skill for revision rounds; not designed yet)
```

Data flow is **one-directional** downstream of polish:
`write/story → polish → typeset → export`. Unlike the write/polish pair (which
co-own `terminology-ledger.md`), typeset and export do not write back — they
consume the finalized tex and produce a formatted artifact. No bidirectional
shared files between typeset/export and the upstream skills.

## Migration tasks (do when implementing — not now)

1. **sci-write** — change output contract from `*.md` to `*.tex` sections,
   written **directly into `manuscript/vN/tex/`** (D1 + D5). Update Layout &
   boundaries, file contracts, every "Output is always md" statement.
   `intro.md`/`discussion.md`/`abstract.md` references that point at narrative
   drafts become `.tex`. `sci-skills/sci-write/` is repurposed as working-notes
   area only (`claim.md`, `paper-plan.md`, `terminology-ledger.md`, reading
   notes); product tex never lands there.
2. **sci-write — SI ownership** (D4). Make SI a by-product of the results/method
   pass, written into `manuscript/vN/` (e.g. `si/` or `si.tex`). Remove any
   notion of a separate SI skill. Confirm sci-story does NOT produce SI.
3. **sci-story** — change output from md to tex, written directly into
   `manuscript/vN/tex/`. (Verify current state first — this skill's SKILL.md
   was not read during this design pass.)
4. **sci-polish** — remove the LaTeX layout/typesetting responsibility:
   - description: drop "Also covers LaTeX layout/typesetting fixes (float
     placement, stranded headings, loose pages)".
   - move `references/latex-layout.md` out of sci-polish (it goes to
     sci-typeset, possibly trimmed since float *strategy* is export's job and
     only readability fixes remain).
   - the "For LaTeX layout requests" branch in Step 2 is removed or rerouted
     to sci-typeset.
5. **sci-typeset** (new) — create. Owns: our-template readability typesetting
   (loose pages, stranded headings, oversized tables), compile-to-PDF. Reads
   finalized tex from `manuscript/vN/tex/`. Inherits the trimmed
   `latex-layout` reference. Does NOT decide float strategy.
6. **sci-export** (re-scope) — drop Mode 1 (`md → tex`). New scope:
   - (optional) move finalized tex into a target journal template, deciding
     float strategy per journal convention.
   - (optional) tex → docx, generated by our rules (not pandoc defaults); we
     define a standard docx format.
   Both modes are manual-trigger and optional — "your paper your way" means
   many first submissions need neither.
7. **article-init** — ensure it does **not** preset a float/layout
   orientation. Layout orientation is introduced at typeset/export time.
   Confirm the scaffold writes tex section stubs directly into
   `manuscript/vN/tex/` (aligned with D5), not into `sci-skills/sci-write/`.
   → **RESOLVED (batch 4):** MANUSCRIPT_CONTRACT now states init does not
   preset float/layout orientation and describes tex-direct authoring
   (sci-write/sci-story write tex into `manuscript/vN/tex/sections/`); the
   sci-write CONTRACT is rewritten as working-notes-only (no tex lands there);
   sci-submit CONTRACT reads manuscript/ (not sci-write notes); the dead
   sci-polish CONTRACT entry is removed; family-layout.md's data-flow,
   naming, and evolution sections updated for the tex-direct model.
   `templates/main/tex/sup.tex` keeps its legacy name (deep blast radius:
   Makefile + naturetex.sty `supp` toggle + ref_converter.py hardcode + all
   `sup.` labels) — new projects use `si.tex`, blueprint copies keep `sup.tex`;
   the contract notes both are the same thing.

## Open questions (resolve at implementation time)

- Does sci-story currently output md or tex? (Not read during this pass.)
  Confirm and align with D1. → **RESOLVED (batch 1):** sci-story now writes tex.
- Exact name for the new docx format spec and where it lives
  (`sci-export/references/docx-format.md`?). → **RESOLVED (batch 3):** lives at
  `sci-export/references/docx-format.md` (stub created; full spec deferred until
  the user designs the standard docx template).
- Whether sci-typeset should own compile-to-PDF, or if that's a shared
  script. (Leaning: typeset owns it, since "typeset" implies producing the
  formatted PDF.) → **RESOLVED (batch 2):** sci-typeset owns compile-to-PDF.
- **sci-revise design is deferred.** A revision-round skill is planned but its
  workflow is not designed yet — the user will do one real revision pass first
  to understand the flow, then design it. Do not spec it speculatively.
