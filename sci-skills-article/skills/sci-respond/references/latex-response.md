# latex-response.md — LaTeX mechanics for the response letter

> Read this when writing/compiling `response.tex`. The bundled template, the
> macros, non-floating figures, the cover page, the compile step, and the
> Word-via-pandoc fallback. Writing rules: `writing-rules.md`.

## 0. The bundled template — Class A (skill decides, not asked)

The skill is self-contained. Its template lives in **this skill's source**:
`assets/response-template/` —
`reviewresponse.sty` + `review_response.tex` + `Reviewers/R1.tex` (+ the
upstream LICENSE, originally by Karl-Ludwig Besser). The response is built from
this bundled suite; the skill does not depend on a project-root `templates/`.

This is a Class-A decision (SKILL.md §two-decision-classes): the author is not
asked which template to use. The skill picks its own.

The suite has gaps this reference documents (and that implementation closes by
extending the bundled `.sty` or layering a local supplement on top).

---

## 1. Inline redline — `\added` / `\deleted`

For typo / clarification responses, the inline-redline quote block. Visual
contract (`assets/typo-format-1.png` + `typo-format-2.png`):

| State | Color | Other markup |
|---|---|---|
| unchanged text | medium gray / blue-gray | none |
| inserted text | **bright green** | none |
| deleted text | **bright red** | red strikethrough |

The shell already exists: `reviewresponse.sty`'s `changes` env (line ~134) is a
`tcolorbox` with `leftrule=1.5em` (the left vertical bar) and `colorchangetext`
body color. What's missing is the two change macros. Implementation adds to the
`.sty` layer:

```latex
\usepackage[normalem]{ulem}  % \sout for strikethrough
\newcommand{\added}[1]{\textcolor{added-green}{#1}}
\newcommand{\deleted}[1]{\textcolor{deleted-red}{\sout{#1}}}
% define added-green / deleted-red in the color palette
```

Usage — structural, not raw `\textcolor`:
```latex
\begin{changes}
Both groups exhibit an \added{Ra} of approximately 0.8 \added{$\mu$}m.
\end{changes}
```
Insert + delete:
```latex
\begin{changes}
...specimens with an \deleted{surface roughness} \added{Ra} of approximately
0.8 \added{$\mu$}m.
\end{changes}
```

Rules: one sentence (the one with the change), leading `...` if partial; no
acknowledgement, no prose — the block IS the answer; color only changed tokens.

### `\quoteRevision` — inline prose quote of a revised sentence
For prose responses quoting a revised sentence: italic + color, black quotes:
```latex
\newcommand{\quoteRevision}[1]{``\textcolor{response-color}{\textit{#1}}''}
```

### Caption-coloring for revised figures/tables
Signal a revised Response Figure/Table by coloring the **caption**, not cells or
internals: `\caption{\textcolor{added-green}{...}}`.

---

## 2. Response Figures / Tables — non-floating (as-is)

**Zero drift.** A Response Figure sits beside the paragraph discussing it
(first principle). This is the *opposite* of manuscript float strategy.

### Default: non-floating + `\captionof`
Do **not** use `figure`/`table` environments. Use center + `\captionof` (from
`caption`), which gives a numbered caption to a non-floating element:
```latex
\usepackage{caption}
\begin{center}
  \includegraphics[width=0.9\linewidth]{response-figures/resp-fig1.pdf}
  \captionof{figure}{Response Fig. 1: ...}
  \label{resp:fig1}
\end{center}
```
Nailed to source location — cannot drift. The only 100% as-is guarantee.

### Fallback: `[H]` (capital) if float-env `\label`/`\ref` linkage is required
```latex
\usepackage{float}
\begin{figure}[H] ... \end{figure}
```
`[H]` forbids drift. Cost: occasional bottom whitespace.

### Forbidden
`[htbp]`, `[t]`, `[p]`, `[h]`, or bare `figure`/`table` — manuscript idioms that
allow drift. Class A: the skill picks non-floating; the author is not asked.

---

## 3. Cover page

Standalone title page, AAAS-supplementary style. Centered, breathing room,
`\clearpage` after. **Three fields only, double-blind safe:**

```latex
\begin{titlepage}
  \centering
  \vspace*{\fill}
  {\Huge Response Letter \#1\par}        % #<rN>  — rN = revision round
  \vspace{1em}
  {\Large for\par}
  \vspace{1em}
  {\large \textit{Full Manuscript Title Here}\par}
  \vspace{1em}
  {\normalsize Manuscript ID: COMMSENG-25-0150-T\par}
  \vspace*{\fill}
  \clearpage
\end{titlepage}
```

- **`#<rN>`** = revision round, matching `manuscript/rN/`.
- **No other fields** — no authors/emails/affiliations/dates/journal. Double-blind
  rules these out; even non-identity fields are noise on a cover whose only job
  is identification. (Global rule enforced by not having those fields.)
- **No Response-Figure ToC** — the reviewer-by-reviewer structure is itself the
  ToC. Add one only if a round carries ≥3 Response Figures AND the author asks.

Cover layout is Class A — the skill picks; the author is not asked about fonts
or spacing.

---

## 4. Compile — sci-respond's own job (Class A)

sci-respond compiles its own `response.tex` → PDF. Not sci-typeset's job.

```bash
pdflatex -interaction=nonstopmode -halt-on-error response-rN.tex
bibtex   response-rN       # only if response uses \printbibliography
pdflatex -interaction=nonstopmode -halt-on-error response-rN.tex
pdflatex -interaction=nonstopmode -halt-on-error response-rN.tex
```
Enough passes for refs/page numbers to stabilize. `-halt-on-error` stops on tex
errors. Visually inspect the PDF before reporting done.

**Re-verify page/line refs after any manuscript edit.** If sci-revise inserts/
deletes manuscript text, every later page/line citation may shift. Page = visual
PDF page; line = margin-printed line (not `.tex` source line). Re-check after the
manuscript settles.

---

## 5. Word via pandoc — only on author insistence (Class A default: tex)

The default is **tex** (precise layout). The author is not asked "tex or Word?"

If the author independently asks for Word (e.g. a co-author needs `.docx`):
```bash
pandoc response-rN.tex -o response-rN.docx
```
- pandoc cannot place every tex construct precisely (the cover page, the
  `tcolorbox` redline block, non-floating figure placement, custom macros).
  **The author fixes what pandoc gets wrong.** The skill does not hand-hold the
  Word path — 不做保姆.
- the tex → PDF remains the canonical artifact; the `.docx` is a convenience
  derivative.

This is the Class-A principle (SKILL.md): tex is objectively better for precise
layout; offering Word as a peer option would offload a technical decision onto
authors who may not know tex is the better choice.

---

## 6. Gap vs the bundled template

| Bundled suite has | Needs adding |
|---|---|
| `\reviewer` + `generalcomment` + `revcomment` + `revresponse` + `changes` envs | **`\added` / `\deleted` macros** (changes shell is there; macros are not) |
| `changes` env with `leftrule=1.5em` | (shell is correct — keep) |
| Sequential single-reviewer structure | **Cover page** env (titlepage) — add to the template |
| biblatex `refsection=section` | **Verify** it gives per-response local numbering; if not, add a local counter |
| | **`\quoteRevision` macro**, non-floating figure guidance |

Implementation extends the bundled `reviewresponse.sty` or layers a local
`sci-respond.sty` supplement on top. Decision deferred to implementation; the
macros and patterns above are the contract.
