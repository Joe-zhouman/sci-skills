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

## Design-blueprint samples

- `Response Letter#1.pdf` — a real, already-public revision package (Nature
  Communications family). The canonical example the skill's document skeleton,
  five-part response order, and 6-strategy taxonomy were extracted from. Design
  was driven by a real revision pass, not speculation.
- `typo-format-1.png`, `typo-format-2.png` — the inline-redline visual contract
  (green `\added`, red `\deleted`+strikethrough, gray unchanged, left vertical
  bar). See `references/latex-response.md` §1.

## Sibling skill

`sci-revise` (manuscript editing) is designed alongside. The two share
revision-round state in `sci-skills/sci-revise/` (`issue-ledger.md`,
`change-log.md`) — co-read/write of one directory via its CONTRACT, same pattern
as `sci-write/` being co-owned by write/story/polish. The `revision_kind` field
in the ledger (set by sci-respond at its checkpoint) drives sci-revise's
surgical-vs-polish-handoff behavior. See `references/state-contract.md`.
