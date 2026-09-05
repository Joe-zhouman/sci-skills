---
name: sci-typeset
description: >-
  LaTeX typesetting on our template — fix readability issues in finalized
  manuscript tex: loose pages, stranded headings, oversized tables, "Float too
  large", multi-panel arrangement within a page, sparse Supplementary
  Information structure. Compiles the tex to PDF and visually inspects before
  and after. Use when the user asks to fix layout/typesetting rather than
  wording. Does NOT decide float *strategy* (where floats go document-wide —
  that's journal-orientation, owned by sci-export at template-move time). Does
  NOT touch prose (wording, claims, terminology — that's sci-polish). Triggers
  on: typeset, 排版, layout, float placement, stranded heading, loose page,
  figure too large, compile PDF, LaTeX 排版, 图飘了, 表太宽, 空页.
---

# sci-typeset

LaTeX typesetting on **our template**. The manuscript tex is already written
(sci-write / sci-story) and prose-polished (sci-polish); this skill makes the
*layout* read right — no content changes, only placement and page-filling.

**Readability typesetting only.** Fix what makes a page look wrong: stranded
headings, loose/near-empty pages, floats that overflow their column, oversized
tables, multi-panel figures that don't fit, sparse SI. This skill works on the
**current template** and applies our template's best practices.

**Does NOT decide float *strategy*.** "Where do floats go document-wide?"
(end-of-document / inline / two-phase) is a journal-orientation question —
that's `sci-export`'s job at template-move time. If the user is asking "should
my floats be at the end for this journal?", route to `sci-export`. This skill
only fixes *readability* within whatever strategy the current template uses.

**Does NOT touch prose.** Wording, claims, evidence, terminology, language —
that's `sci-polish`. If a layout problem is actually a content problem (a
paragraph is long because it's saying too much), flag it and route to
`sci-polish`; don't rewrite prose to fix a page-fill.

## Layout & boundaries

```
<project-root>/
  manuscript/vN/tex/             ← THIS skill reads and edits here (or current round)
    sections/*.tex               ← the tex being typeset
    main.tex                    ← preamble / \input wiring (float strategy lives here if any)
  sci-skills/
    sci-draw/                   ← READ-ONLY: figN.png (to regenerate wide figures taller at source)
```

- **Edits `manuscript/vN/tex/` directly.** Same working surface as sci-polish — git is the audit trail, commit messages carry the layout diagnosis.
- **Reads figure source from `../sci-draw/`** only when applying the "regenerate wide figures taller at the source" rule (a too-wide figure is fixed at its source script, not by squeezing in tex).
- **Does NOT write prose.** No edits to wording, claims, terminology. If a layout fix would require changing prose, stop and route to sci-polish.
- **Does NOT move the manuscript into a target journal template.** That's sci-export. This skill typesets on *our* template.

## Startup

Every session starts here:

1. **Locate the manuscript.** Check `manuscript/vN/tex/` (default) or the current round (`manuscript/rN/tex/`). If absent, ask where the tex is. If no tex exists, tell the user: "Typesetting needs finalized tex — draft (sci-write/story) and polish (sci-polish) first."

2. **Check git tracking.** If the manuscript directory isn't under git, remind the user: "Typesetting without git loses the audit trail. `git init` or `git add` the tex first." Same rule as sci-polish — the commit history IS the record.

3. **Compile first.** Run the build (usually `latexmk -pdf` or the template's Makefile) and open the PDF. **Diagnose from the compiled output, not the source.** A stranded heading looks like a stranded heading in the PDF, not in the tex.

4. **Gather the axes:**
   - **Which files** — which tex files / which sections have the issue
   - **What's wrong** — the user's report (loose page / stranded heading / float overflow / oversized table / sparse SI)
   - **Is this actually a prose problem?** If the user says "this page is too empty" but the real issue is a paragraph that's too short — that's sci-polish's job. Flag and route.

## Workflow

### Step 0 — Compile and locate

Build the PDF. Open it. Pinpoint the actual layout failure on the page(s). Don't
trust a description alone — "the figure drifted" means different things; see it.

Load `references/latex-layout.md` — specifically the **typeset scope** sections
(§ Float placement tuning, § Common problems, § Multi-panel figures, §
Supplementary Information, § "Regenerate wide figures taller at the source"
rule). **Skip the export-scope sections** (§ Complete journal reference, §
Strategy summary, § Float at end, § Traditional inline float placement) — those
are journal-strategy, not your concern.

### Step 1 — Diagnose

For each reported issue, classify:

| Problem | Fix location | Notes |
|---|---|---|
| Stranded heading (heading at page bottom, body on next) | tex — `\needspace`, reorder, or pull content up | Don't invent content to fill |
| Loose / near-empty page | tex — float reflow, `\vspace`, or accept (some journals want it) | If it's a real content gap, route to sci-polish |
| "Float too large" warning | source — regenerate the figure/table at appropriate size (see "regenerate wide figures taller" rule) | Fix at `../sci-draw/` source, not by `\resizebox` squeeze |
| Oversized table | tex — `sidewaystable`, `\small`, split into sub-tables, or move to SI | Don't shrink to unreadable |
| Multi-panel figure doesn't fit | tex / source — re-grid the panels, regenerate if needed | |
| Sparse SI (each figure on a page, lots of whitespace) | tex — restructure SI section, group figures | SI structure readability |

**Don't solve a content problem with layout.** If the diagnosis is "this section
is too short, page looks empty" → that's sci-polish (prose) or sci-write (more
content), not typeset. Flag it.

### Step 2 — Fix

Apply fixes in tex. Prefer the **source-fix rule** for figure problems: a figure
that's too wide or too short is regenerated at the right aspect ratio in its
`sci-draw/` source script, not squeezed with `\resizebox` (which rasterizes
text and breaks font sizes — the #1 journal desk-rejection cause, same rule as
sci-draw's five hard rules).

**Compile after each fix.** Don't stack fixes blind — one fix can resolve or
create another. Re-compile, re-open, re-check.

### Step 3 — Visual review

**Mandatory.** Open the recompiled PDF. Walk the affected pages. The fix
should resolve the reported issue without creating new ones (a pulled-up
heading can strand the next one).

### Step 4 — Commit

```bash
git add manuscript/vN/tex/<changed-files>
git commit -m "typeset(<area>): <one-line diagnosis>

- <fix applied, e.g. resolved stranded heading in §3 by ...>
- <source regen if any, e.g. fig2 regenerated wider>
- <remaining issues deferred, if any>"
```

Each typeset round is one commit. `git log -- manuscript/vN/tex/` (shared with
sci-polish's commits) is the layout history.

## Reference index

| File | Open when |
|---|---|
| `references/latex-layout.md` | Every job — but only the **typeset-scope** sections (read the scope note at the top of that file). Skip the export-scope (journal-strategy) sections. |

## Boundaries

| Need | Where |
|---|---|
| Polish wording / claims / terminology | `sci-polish` |
| Decide float strategy for a target journal (floats at end / inline) | `sci-export` (at template-move time) |
| Move tex into a target journal template / convert to docx | `sci-export` |
| Write more content (a section is too short) | `sci-write` / `sci-story` |
| Create or regenerate figures at source | `sci-draw` |
