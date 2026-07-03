# LaTeX Layout & Typesetting

Self-contained reference for LaTeX figure/table placement and page layout. When the user asks to fix placement rather than wording — loose pages, stranded headings, float placement, "Float too large", multi-panel arrangement, sparse Supplementary Information — skip the prose axes and use this file directly.

## Complete journal reference

All journal families verified against official templates and guidelines.

### Strategy groups

**Group A: Figures at END of manuscript**

| Journal family | Accepts LaTeX? | Template | Float specifier | Notes |
|---|---|---|---|---|
| **Science 系** (Science, Science Advances, Science Immunology, etc.) | Yes | AAAS LaTeX template (`science.cls`) | `\begin{figure}` (no specifier — at end, not floating) | Template: "not in the middle of the text." `figure*` forbidden. |
| **Nature 系** (Nature, Nature Materials, Nature Comms, etc.) | Yes | Old: `nature.cls` (disables `\includegraphics`). New: `sn-jnl.cls` | Old: captions only at end. New: inline during draft, separate at acceptance. | Initial PDF preferred; LaTeX at revision. |
| **PNAS** | Yes | `pnas-new` class | `\begin{figure}` (no specifier → defaults to `[p]` — one figure per page) | SI: "Each figure should be on its own page." |
| **Cell 系** (Cell, Cell Reports, Cell Systems, etc.) | Yes | `elsarticle` with `endfloat` option | `[tbp]` (standard `elsarticle`), but `endfloat` moves all to end | "Figure titles and legends at end of editable manuscript." |
| **BMC 系** (BMC Genomics, etc.) | Yes | `bmcart` class | `[h!]` | "all figures must be coded at the end of the TeX file and not inline." In `\section*{Figures}` inside `\begin{backmatter}`. |
| **Frontiers 系** | Yes | Official GitHub template | System places at end | Figures uploaded separately; submission system auto-places at end of compiled PDF. |

**Group B: Figures INLINE (near first citation)**

| Journal family | Accepts LaTeX? | Template | Float specifier | Notes |
|---|---|---|---|---|
| **ACS 系** (JACS, Nano Letters, ACS Nano) | Yes | `achemso` class | No specifier (default `[tbp]`) | "place graphics where they make logical sense; production will move them if needed." |
| **RSC 系** (Chemical Science, JMC A, etc.) | Yes | `rsc-article` class | No specifier (default `[tbp]`). `float` package loaded, `[H]` available. | RSC re-typesets in-house — layout is for review only. |
| **IEEE 系** | Yes | `IEEEtran` class | `[!t]` **only** | No `[h]`, no `[b]`, no first-column-on-first-page floats. `figure*` for double-column (top only). Strictest. |
| **Elsevier 系** (non-Cell) | Yes | `elsarticle` class | No specifier or `[htbp]` (default `[tbp]`) | "placed next to the relevant text, rather than at the bottom or top." |
| **OUP 系** (Bioinformatics, NAR) | Yes | `oup-authoring-template` | `[t]` recommended (default `[tbp]`) | Template examples use `\begin{figure}[t]`. |
| **AIP 系** (APL, JAP) | Yes | REVTeX 4.1/4.2 | No specifier or `[t]` / `[b]` / `[p]` | "Figures may be embedded in the text or not (author's choice)." Separate files at revision. |
| **MDPI 系** (Nanomaterials, Sensors, IJMS) | Yes | MDPI template (loads `float`) | Default `[tbp]`; many authors use `[H]` | `[H]` NOT the default but commonly used. Template uses `paracol` — `[H]` avoids cross-column drift. |
| **Taylor & Francis 系** | Yes | `interact` class | **No specifier** (default `[tbp]`) | "You should not normally use optional [htb] location specifiers." Class handles placement. `endfloat` available commented-out. |

**Group C: Two-phase — inline → end upon acceptance**

| Journal family | Accepts LaTeX? | Template | Float specifier | Notes |
|---|---|---|---|---|
| **Wiley 系** (Advanced Materials, Angewandte, Small) | Yes | Standard `article` class | Default `[tbp]` | **Review**: inline. **Upon acceptance**: manually move figures + tables to end of `.tex`. Explicitly: do NOT use `endfloat` package. |

**Group D: Separate upload — NO graphics in LaTeX source**

| Journal family | Accepts LaTeX? | Template | Float specifier | Notes |
|---|---|---|---|---|
| **PLOS 系** (PLOS ONE, PLOS Biology) | Yes — but... | PLOS template | N/A (remove all `\includegraphics`) | DO NOT include graphics in `.tex`. Figures as separate TIFF/EPS uploads. Captions after first citation paragraph or at end. |
| **The Lancet 系** | Yes — but... | `elsarticle` | N/A | Figures as separate vector files (.eps, .ai, .pdf). Lancet redraws all figures in-house. Tables in separate Word doc. |

**Group E: Chinese English-language journals (国内英文期刊)**

| Journal | Accepts LaTeX? | Template | Float specifier | Notes |
|---|---|---|---|---|
| **Science Bulletin** (《科学通报》英文版, Elsevier) | Yes | `elsarticle` (no journal-specific `.cls`) | Default `[tbp]` | "Tables/figures should appear near where referenced in text." Science China Press + Elsevier. |
| **Research** (AAAS / CAST) | Yes | SPJ Overleaf template (NOT the same as Science's AAAS template) | `[h]` in template example | Based on `\documentclass[twocolumn]{article}`. Separate figure files at acceptance, similar to AAAS. |
| **Engineering** (中国工程院, Elsevier) | Yes | `elsarticle` (no journal-specific `.cls`) | Default `[tbp]` | Standard Elsevier workflow — separate figure files at acceptance. |
| **Engineered Science** (ES Publisher) | **No dedicated LaTeX template found** | Word template only | — | Contact editorial office (`es@espublisher.com`) for LaTeX policy. DOAJ-indexed (SJR Q1) but primarily Word-based. |

---

## Strategy summary

```
At end (Group A):     Science, Nature, PNAS, Cell, BMC, Frontiers
Inline (Group B):     ACS, RSC, IEEE, Elsevier, OUP, AIP, MDPI, T&F,
                      Science Bulletin, Engineering
Two-phase (Group C):  Wiley
No graphics (Group D): PLOS, Lancet
Word-only (Group E):  Engineered Science
```

## Float at end

For Group A journals (and Wiley upon acceptance).

### Figure pattern

```latex
% === Main text ===
% === References ===
% === Acknowledgements, Declarations ===

\newpage
\section*{Figures}

\begin{figure}[!h]
    \centering
    \includegraphics[width=\textwidth]{fig1.pdf}
    \caption{\textbf{Figure 1. Short title.} Full caption text.}
    \label{fig:fig1}
\end{figure}

\newpage
\begin{figure}[!h]
    \centering
    \includegraphics[width=\textwidth]{fig2.pdf}
    \caption{\textbf{Figure 2. Short title.} Full caption text.}
    \label{fig:fig2}
\end{figure}
```

### Table pattern

Tables are flexible — most templates allow them inline or at end:

```latex
\begin{table}[h]
\centering
\caption{\textbf{Table 1. Short title.} Caption text.}
\label{tab:example}
\begin{tabular}{...}
...
\end{tabular}
\end{table}
```

## Traditional inline float placement

For Group B journals and preprints/camera-ready.

### Float specifiers by template

```
ACS (achemso):      no specifier → default [tbp]
RSC:                no specifier → default [tbp]
IEEE (IEEEtran):    [!t] only — top of page exclusively
Elsevier (elsarticle): no specifier or [htbp] → default [tbp]
OUP:                [t] recommended in template examples
AIP (REVTeX):       [t] / [b] / [p] as needed
MDPI:               default [tbp]; [H] available via float package (commonly used)
T&F (interact):     no specifier — class handles placement
Wiley:              default [tbp] (standard article class)
```

### Float placement tuning

```latex
\renewcommand{\topfraction}{0.9}
\renewcommand{\bottomfraction}{0.9}
\renewcommand{\textfraction}{0.1}
\renewcommand{\floatpagefraction}{0.8}
```

### Common problems

| Problem | Fix |
|---|---|
| Float drifted to float-only page, text half-empty | Reduce `\floatpagefraction` |
| Tall float forced to own page | `[htbp]` or resize |
| Section starts with orphan lines | `\clearpage` before section |
| Stranded heading at page bottom | `\needspace{4\baselineskip}` |
| "Float too large" | Reduce at source; stack panels vertically; last resort `\enlargethispage{2\baselineskip}` |

### Multi-panel figures
- Grid: identical widths, heights follow
- Asymmetric: `minipage` or `subcaption` with explicit width ratios
- Shared axes: align precisely

### Supplementary Information

SI has no format requirements (rare exceptions — a few journals provide SI templates). The pragmatic rule: **figures at the front, one per page. Tables grouped. Then methods, discussion, references.**

Figures are referenced throughout SI text — putting them first means the reader doesn't flip pages. One page per figure = no visual clutter.

```latex
\documentclass{article}
\usepackage[supp,lineno]{naturetex}  % or whatever class the journal needs

\begin{document}
\maketitle
\beginsupplement

\tableofcontents    % auto-generates from \addcontentsline entries
\newpage

% === FIGURES FIRST ===
\section{Supplementary Figures}

\begin{figure}[!h]
    \centering
    \includegraphics[width=\textwidth]{fig_s1.pdf}
    \caption{\textbf{Short title.} Full caption.}
    \label{sup.fig:fig1}
\addcontentsline{toc}{subsection}{\ref{sup.fig:fig1}}  % manual TOC entry
\end{figure}

\clearpage
\begin{figure}[h]
    \centering
    \includegraphics[width=\textwidth]{fig_s2.pdf}
    \caption{\textbf{Short title.} Full caption.}
    \label{sup.fig:fig2}
\addcontentsline{toc}{subsection}{\ref{sup.fig:fig2}}
\end{figure}

% === TABLES GROUPED ===
\newpage
\section{Supplementary Tables}
\begin{table}[h]
\centering
\caption{Table title.}
\label{sup.tab:tab1}
\addcontentsline{toc}{subsection}{\ref{sup.tab:tab1}}
\begin{tabular}{...}
...
\end{tabular}
\end{table}
% Tables are short — several can fit on one page. No forced page breaks needed.

% === METHODS, DISCUSSION, REFERENCES AT END ===
\clearpage
\section{Supplementary Methods}
...
\section{Supplementary Discussion}
...
\printbibliography[title=Supplementary References]
\end{document}
```

Key points:
- Figures at front → easy to find when referenced in later sections
- `\newpage` / `\clearpage` between figures → one per page, clean
- `\addcontentsline{toc}{subsection}{\ref{...}}` → auto-generates hyperlinked TOC so readers can jump directly to any figure
- Tables can share pages (they're short)
- Methods, discussion, references after all figures/tables
- `[!h]` or `[h]` — no float drifting needed; `\clearpage` already controls positioning

### "Regenerate wide figures taller at the source" rule

A very wide, short figure creates awkward page breaks regardless of float settings. Fix at the plotting stage — rotate axes or add vertical context. Never stretch the aspect ratio in LaTeX.
