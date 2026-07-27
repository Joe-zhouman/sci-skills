# Samples — public response letters (showcase + phrasebank fuel)

These are **real, accepted response letters** the author has published. Two
purposes, in tension but both served:

1. **Showcase** — proof the skill's stance and framing tactics actually land
   real acceptances. Each entry links the published paper (DOI) so anyone can
   verify the letter worked. For potential users / collaborators evaluating
   whether this skill produces work that survives peer review.
2. **Phrasebank fuel** — each letter is mined by
   `scripts/extract_phrases.py` into `references/phrasebank.md`. The flywheel:
   every accepted letter's framing phrasing thickens the bank, which makes the
   next letter easier, which feeds the bank again.

## Directory naming — citation key

`<Author>-<Year>-<journal-short>/` — the BibTeX-style citation key (e.g.
`Zhou-2025-commeng`). Stable, identifiable, and matches how the paper would be
cited. `journal-short` follows the manuscript-submission prefix when there is
one (COMMSENG → `commeng`); otherwise the journal's common abbreviation.

Each directory holds:
- `response.pdf` — the authoritative response letter (what was actually sent)
- `response.md` — a text-extracted version (`extract_phrases.py` greps this)
- letter-specific assets (redline format images, etc.)

## Index

| Key | Paper | Journal (publisher) | What this letter demonstrates |
|---|---|---|---|
| [`Zhou-2025-commeng/`](Zhou-2025-commeng/) | "What surface characteristics truly affect thermal contact resistance — an interpretability study based on deep learning and CNNs." DOI: [10.1038/s44172-025-00508-0](https://doi.org/10.1038/s44172-025-00508-0) | Communications Engineering (Nature Portfolio), 2025 | A-reframe ("does not undermine the core conclusions" — R1-Q4); B-minimize (limitation as "manageable cost" + "modular design allows extension" — R1-Q6/R2-Q6); D-divert (small-text panels strategically relocated to Supplementary — R1-Q11); E-fill (own Chinaxiv preprint to fill the "no prior ML model" gap — R1-Q12); F-exit ("we are happy to remove" the rotation validation — R2-Q6); honest-but-tactical self-disclosure ("alphabetical order" DenseNet pick, "not experimentally validated" predictions). |

_Add new published letters as a row here when added._
