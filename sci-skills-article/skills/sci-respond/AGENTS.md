# AGENTS.md — for an agent arriving in this directory

You cloned the repo, you're standing in `sci-skills-article/skills/sci-respond/`.
Read this first — it's the entry point, same role `CLAUDE.md` plays at a project
root. After this, you'll know what this is, how to run it, and where everything
lives.

## What this is

**sci-respond** — the Response-to-Reviewers letter skill, part of the
sci-skills article family. Writes the point-by-point response letter (tex → PDF)
for a manuscript revision round (`manuscript/rN/`), grounded in the manuscript,
the reviews, and the writing-stage notes.

This directory is the **skill source**. The product lands in the user's project
at `manuscript/rN/response/`, not here.

## How to install / trigger

- **Install** is handled at the family level (repo-root `install.sh` symlinks
  all skills into `~/.claude/skills/`). This skill ships with the article
  family — no separate install.
- **Trigger (in a project):** the user mentions responding to reviewers,
  revision letter, 修回信, 回复审稿人, point-by-point response, etc. The
  Claude Code loader reads `SKILL.md` (the frontmatter `description` is the
  triggering signal). For other agent runtimes that read AGENTS.md but not
  SKILL.md: invoke the skill by following `SKILL.md`'s Startup flow manually.
- **Prerequisite:** the project must be a sci-skills project — i.e. it has
  `manuscript/` and `sci-skills/` (created by `article-init`). If absent, tell
  the user to run article-init first; this skill does not bootstrap the
  workspace.

## Hard rules — what you must not get wrong

These are the load-bearing invariants. Violating any of them breaks the skill's
output even if the rest is perfect.

- **Tex, not Word.** Write and compile `response.tex`. Word via pandoc only if
  the user insists, and the user fixes what pandoc can't place. 不做保姆 —
  don't offer Word as a peer option.
- **Every response is self-contained.** The reviewer never opens the manuscript.
  Each response carries its own evidence (quoted revised sentence / Response
  Figure / data + precise location). "Addressed in Section X" with no detail =
  failed response.
- **Honesty is the floor, not the ceiling — the goal is acceptance.** No
  fabricated data/results/citations, no did-what-we-didn't. Above the floor,
  framing is craft (reframe scope, minimize limitation, divert to SI, exploit
  misunderstanding). See `references/writing-rules.md` §framing-freedom for
  A–G tactics + the red line.
- **Acknowledgement restraint.** Default: no acknowledgement. When warranted,
  one short line at the **end**. Never "We sincerely appreciate your
  meticulous…" on a typo fix.
- **Stop at the checkpoint.** Do not draft any response before the user locks
  per-issue strategies. The skill's job is to surface options (defend / concede
  / experiment / ambiguous-intent), not to pick. See `references/workflow.md` §3.
- **No cross-reviewer references.** Reviewers may use separate systems and
  can't see each other's sections. If R1 and R2 raise the same concern, answer
  in full in each section — never "see response to Reviewer 1."
- **Response Figures are non-floating.** `\captionof` or `[H]`, never
  `[htbp]`/`figure`/`table` envs. As-is, no drift.
- **This skill writes only the response letter.** It does not touch
  `manuscript/rN/tex/` (that's sci-revise), does not write cover letters
  (sci-submit), does not draw figures (sci-draw). It only writes the
  `revision_kind` field in the issue-ledger that drives sci-revise.

## Where everything lives

```
sci-respond/
├── SKILL.md              ← execution contract (the Claude Code loader reads this)
├── references/           ← load on demand when the flow needs the detail
│   ├── workflow.md         (intake, checkpoint, underlying-concern, viability)
│   ├── writing-rules.md    (3 hard rules, 5-part order, 6 strategies, framing A–G)
│   ├── phrasebank.md       (framing phrasing, + Inbox for collected phrases)
│   ├── latex-response.md   (bundled template, \added/\deleted, non-floating, compile)
│   ├── state-contract.md   (issue-ledger schema, INF: anchors, [TBD], safe-claim-boundary)
│   └── self-check.md       (coverage audit, integrity firewall, independent-reviewer read)
├── scripts/              ← deterministic tools (run them; don't do their work by hand)
│   ├── scan_neighbor.py    (sense grounding before reading individual files)
│   ├── check_response.py   (self-check the drafted response.tex)
│   └── extract_phrases.py  (mine a published letter into the phrasebank Inbox)
├── assets/
│   ├── response-template/  ← bundled LaTeX template suite (reviewresponse.sty)
│   └── samples/            ← published response letters (showcase + phrasebank fuel)
│       ├── INDEX.md          (which letter, which journal, DOI, what it demonstrates)
│       └── Zhou-2025-commeng/  (Communications Engineering, DOI 10.1038/s44172-025-00508-0)
├── tests/                ← script fixtures + skill acceptance checklist
└── docs/                 ← design archive (why each rule exists)
    ├── design-note.md       (full design rationale — read when modifying the skill)
    └── cross-cutting-tricks.md (provenance of adopted tricks, repo + file:line)
```

## Where to read next (decision tree)

- **Running the skill on a revision round?** → `SKILL.md` Startup flow, then
  `references/workflow.md`.
- **Drafting a specific response?** → `references/writing-rules.md` (rules +
  framing) + `references/phrasebank.md` (the words, after strategy is decided).
- **Writing/compiling the tex?** → `references/latex-response.md`.
- **Wondering why a rule exists?** → `docs/design-note.md` (every decision +
  its why, including the framing layer most skills avoid).
- **Modifying or questioning a rule's origin?** → `docs/cross-cutting-tricks.md`
  (provenance: which of the 6 surveyed repos it came from, file:line).

## The phrasebank flywheel (read if you're adding a sample)

When the user publishes a new response letter: drop it as
`assets/samples/<Author>-<Year>-<journal>/` (PDF + text `.md`), add a row to
`assets/samples/INDEX.md`, run `scripts/extract_phrases.py` to mine it into
`references/phrasebank.md` Inbox. The bank grows with use — that's by design,
not a gap to fill by scraping external corpora (those are empty for framing
phrasing).
