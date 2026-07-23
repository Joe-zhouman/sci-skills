# docx-format.md — Standard DOCX format spec

**Status: stub / TODO.** The standard reference docx and its style rules are
not yet designed. This file is the agreed home for that spec when it's built.
When you (the user) are ready to design the standard docx template, fill this
file in; until then sci-export Mode B falls back to bare pandoc with default
formatting and flags the gap to the user.

## Why this file exists

tex → docx via bare `pandoc main.tex -o out.docx` produces poorly-formatted
output (wrong heading sizes, inconsistent fonts, dropped caption styling). We
don't accept pandoc defaults. Instead we use pandoc with a **reference docx**
(`--reference-doc=references/docx-reference.docx`) that encodes our standard
styles, plus a set of rules this file documents. pandoc is the tool; our
reference docx + rules are the standard.

This is the "按照一规则去生成" approach: pandoc stays as the converter, but its
output is governed by our format, not its defaults.

## To design (when ready)

- [ ] **Reference docx**: build `references/docx-reference.docx` — defines
      heading 1-4 styles, body font + size, caption style, table style,
      reference style (for bibliography), margins, line spacing. This is what
      `--reference-doc` points at.
- [ ] **Style rules**: document the style choices in the reference docx and
      *why* each was chosen (e.g., "heading 2 at 14pt bold because reviewers
      scan section headers at print scale").
- [ ] **Figure handling**: how figures are placed in docx (inline vs floating),
      caption format, how to avoid dropped figures.
- [ ] **Citation rendering**: how `--citeproc` + the bib produces the reference
      list, which citation style, how to handle placeholders.
- [ ] **Equation fallback**: which equations convert cleanly, which need manual
      fixup (pandoc's math → OMML is imperfect on complex equations).
- [ ] **Post-convert checklist**: the machine-checkable + human-eye checks
      (already sketched in sci-export Mode B Step "Post-convert check").

## Related

- The reference docx file itself: `references/docx-reference.docx` (to be
  created alongside filling this spec in).
- sci-export Mode B consumes this file: `skills/sci-export/SKILL.md` → Mode B.
