---
name: sci-export
description: >-
  导出 / Export — move finalized manuscript tex into a target journal template
  (optional), and/or convert tex to Word (DOCX) for collaborators (optional).
  Manual only, both modes optional — "your paper your way" means many first
  submissions need neither. At template-move time, decides float strategy per
  the target journal's convention (floats at end / inline / two-phase) using the
  journal-orientation reference. Does NOT write prose (sci-polish), does NOT
  typeset for readability (sci-typeset), does NOT assemble SI (sci-write's
  by-product), does NOT do md→tex (drafts are tex from the start now). Triggers
  on: 导出, export, 搬模板, 换期刊模板, tex转Word, tex→docx, 转docx, submit to
  journal template.
---

# sci-export

Two export modes, **both optional and manual**. The finalized tex in
`manuscript/vN/tex/` is the source of truth; this skill produces *external*
artifacts (a journal-specific tex copy, or a docx) — it does not modify the
source manuscript.

**Why both optional:** most journals accept "your paper your way" for first
submission — the manuscript as written (on our template, typeset by
sci-typeset) is enough. You reach for this skill when (a) a journal's
production system requires their template, or (b) a collaborator needs Word.
Revision rounds (`manuscript/rN/`) often need a template move; first drafts
often don't.

## What this skill does NOT do (after re-scope)

- **No md→tex conversion.** Drafts are tex from the start (sci-write / sci-story
  write `.tex` directly into `manuscript/vN/tex/sections/`). The old Mode 1
  (搬运 md 草稿 → tex) is retired.
- **No SI assembly.** SI is sci-write's by-product — it writes
  `manuscript/vN/tex/si.tex` alongside results/method. This skill doesn't
  assemble SI; it may *carry* SI into a target template, but doesn't create it.
- **No prose editing, no readability typesetting.** Route those to sci-polish
  and sci-typeset respectively. This skill only moves/converts finalized tex.

## Layout & boundaries

```
<project-root>/
  manuscript/vN/tex/         ← SOURCE: finalized tex (read-only for this skill)
  manuscript/vN/tex/template-move/   ← TARGET (Mode A): journal-specific tex copy
  manuscript/vN/manuscript.docx     ← TARGET (Mode B): Word output
  templates/main/          ← READ-ONLY: our reference tex blueprint
  sci-skills/sci-typeset/references/latex-layout.md  ← READ: float-strategy reference (export-scope sections)
```

- **Reads `manuscript/vN/tex/` (read-only).** The finalized manuscript is the source; this skill does not edit it.
- **Writes to a copy, not the source.** Mode A writes to
  `manuscript/vN/tex/template-move/` (or a user-named dir) — never overwrites the
  finalized tex. Mode B writes `manuscript/vN/manuscript.docx`.
- **Reads `templates/main/`** as our reference blueprint, and the target journal's
  template when the user provides one.
- **Does not import code. Does not write prose. Does not assemble SI.**

## Startup

1. **Which mode (if either)?** Ask: "Move into a journal template, convert to
   Word, both, or neither? Reminder — most first submissions don't need a
   template move (your-paper-your-way)."
2. **Which round?** `manuscript/v1/` (default) or `manuscript/rN/` (revision).
3. **For Mode A: which target journal?** This determines float strategy. Load
   `sci-skills/sci-typeset/references/latex-layout.md` — read the
   **export-scope** sections only (§ Complete journal reference, § Strategy
   summary, § Float at end, § Traditional inline float placement). The scope
   note at the top of that file partitions which sections are export's.
4. **For Mode A: which template?** Does the user have the target journal's
   template, or build from `templates/main/` and adapt?

## Mode A: move into a target journal template (optional)

Produce a journal-specific tex copy. The finalized tex stays untouched; this
writes to a copy.

### Step 0 — Identify float strategy

From the target journal family (see latex-layout.md export-scope sections),
determine the float strategy:

| Strategy | What it means | Journals |
|---|---|---|
| Floats at END | figures/tables in a `Figures` section at document end, not inline | Science 系, Nature 系 (old), PNAS, Cell 系, BMC 系, Frontiers |
| Inline | floats near first citation, default `[tbp]` | ACS, RSC, Elsevier (non-Cell), OUP, AIP, MDPI, T&F |
| Two-phase | inline for review, move to end at acceptance | Wiley 系 |
| IEEE strict | `[!t]` only, no `[h]`/`[b]` | IEEE |

This is the **journal-orientation decision** — it lives here, not in
sci-typeset (which only does readability on our template). Record the chosen
strategy; it drives Step 1.

### Step 1 — Copy + adapt

1. Copy `manuscript/vN/tex/` → `manuscript/vN/tex/template-move/` (or user-named).
   **Never edit the source `manuscript/vN/tex/`** — the copy is the working surface.
2. Apply the float strategy from Step 0 to the copy:
   - Floats-at-end: gather all `\begin{figure}`/`\begin{table}` into a trailing
     `Figures`/`Tables` section, remove inline placement, rewire `\ref` (labels
     unchanged).
   - Inline: ensure specifiers match the journal family (e.g. IEEE `[!t]` only).
   - Two-phase: leave inline for now; flag that end-move happens at acceptance.
3. Swap the preamble/class to the target journal's template if the user provided
   one; otherwise adapt `templates/main/` preamble.

### Step 2 — Compile the copy

```bash
cd manuscript/vN/tex/template-move && make   # or the journal template's build
```

Compile errors from the template swap → fix in the copy (not the source). Max 3
rounds; beyond that, list errors for the human.

### Step 3 — Verify cross-refs + floats

Open the compiled PDF. Every `\ref{fig:...}`/`\ref{tab:...}` resolves? Floats in
the right place per the strategy? SI (`si.tex`) carried over and still referenced?

### Step 4 — Remind the human

> "Journal-specific tex copy is at `manuscript/vN/tex/template-move/`. The
> finalized source at `manuscript/vN/tex/` is untouched. Float strategy: [chosen].
> Next is yours: Zotero-insert real citations, attach figure files the journal
> requires, final visual check."

## Mode B: tex → docx (optional)

Convert the finalized tex to Word for collaborators. Uses **pandoc + our
reference docx + rules** — not bare `pandoc main.tex -o out.docx` (default
output is poorly formatted). Our rules live in `references/docx-format.md`.

### Prerequisite

`manuscript/vN/tex/` must compile (PDF generates). If it doesn't, the docx will
be broken too — fix the tex first (route to sci-polish / sci-typeset).

### Convert

```bash
pandoc manuscript/vN/tex/main.tex \
  -o manuscript/vN/manuscript.docx \
  --from=latex \
  --to=docx \
  --reference-doc=references/docx-reference.docx \
  --bibliography=manuscript/vN/tex/bibliography.bib \
  --citeproc \
  --resource-path=manuscript/vN/figures/
```

- `--reference-doc` points at our reference docx (defines styles: heading sizes,
  fonts, margins, caption style). This is how we impose our format instead of
  accepting pandoc defaults. See `references/docx-format.md` for how to build /
  maintain the reference docx.
- If the reference docx or `docx-format.md` doesn't exist yet, fall back to bare
  pandoc and flag to the user: "docx is machine-converted with default
  formatting; the standard reference docx isn't set up — see
  `references/docx-format.md` (TODO)."

### Post-convert check

Open `manuscript/vN/manuscript.docx`:
- Title and authors present?
- Figures present (not dropped)?
- Citations rendered (not `?`)?
- Equations intact?
- Styles match our reference docx (heading sizes, etc.)?

Issues → note them in the output to the user.

### Remind

> "Word draft at `manuscript/vN/manuscript.docx`. This is for collaborators;
> the tex remains the source of truth. Don't treat docx as the final manuscript."

## Boundaries

- **Does not write prose.** No wording/claim/terminology changes — route to sci-polish.
- **Does not do readability typesetting.** Loose pages, stranded headings → sci-typeset.
- **Does not assemble SI.** SI is sci-write's by-product; this skill only carries it.
- **Does not do md→tex.** Drafts are tex from the start.
- **Does not modify the finalized source.** Writes to a copy (Mode A) or a new file (Mode B).

## Reference index

| File | Open when |
|---|---|
| `references/docx-format.md` | Mode B — how to build/maintain the reference docx, the style rules pandoc defaults don't give us. *(Currently a stub/TODO — the standard docx template is not yet designed.)* |
| `../sci-typeset/references/latex-layout.md` | Mode A — read the **export-scope** sections only (journal float strategy). The scope note at the top partitions which sections are export's vs typeset's. |

## Privacy

Don't leak private paths or unpublished content in the docx, the template-move
copy, or user-facing output. The docx is meant for collaborators — scrub any
private path comments from tex before converting.
