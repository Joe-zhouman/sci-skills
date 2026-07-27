# sci-respond assets

The skill's bundled resources: the response-letter template suite, plus the
real-sample artifacts used to extract the design.

## response-template/ — the bundled template (self-contained)

The skill's base LaTeX template, **copied into the skill source** so sci-respond
is self-contained (no dependency on a project-root `templates/response/`):

- `review_response.tex` — the document skeleton
- `reviewresponse.sty` — the environment package (`reviewer`, `generalcomment`,
  `revcomment`, `revresponse`, `changes`)
- `Reviewers/R1.tex` — a per-reviewer demo
- `LICENSE` — upstream license (originally by Karl-Ludwig Besser)

The response letter is built from this bundled suite. The skill does not ask the
user which template to use (Class-A decision — see SKILL.md §two-decision-classes).
Gaps the suite has (macros to add at implementation time: `\added`/`\deleted`,
cover-page env, `\quoteRevision`) are documented in
`references/latex-response.md` §6.

## samples/ — the author's published response letters (the flywheel)

Every response letter the author publishes and is willing to share lands here as
`samples/<letter-name>/` — these are **phrasebank fuel**, not just design
blueprints. Each holds:
- `response.pdf` — the authoritative artifact (what was actually sent)
- `response.md` — a text-extracted version (`scripts/extract_phrases.py` greps
  this; the PDF is for humans)
- letter-specific assets (e.g. `typo-format-*.png` for the redline contract)

The flywheel: an accepted letter's framing phrasing gets mined into
`references/phrasebank.md` via `extract_phrases.py`, which makes the next letter
easier to write, which feeds the bank again. Left foot steps on right foot.

Current sample: `samples/response-letter-1/` — a real, public revision package
(Communications Engineering / Nature Communications family,
COMMSENG-25-0150-T). Source of the document skeleton, five-part response order,
6-strategy taxonomy, and the inline-redline visual contract (green `\added`,
red `\deleted`+strikethrough, gray unchanged, left vertical bar — see
`references/latex-response.md` §1).

## Sibling skill

`sci-revise` (manuscript editing) is designed alongside. The two share
revision-round state in `sci-skills/sci-revise/` (`issue-ledger.md`,
`change-log.md`) — co-read/write of one directory via its CONTRACT, same pattern
as `sci-write/` being co-owned by write/story/polish. The `revision_kind` field
in the ledger (set by sci-respond at its checkpoint) drives sci-revise's
surgical-vs-polish-handoff behavior. See `references/state-contract.md`.
