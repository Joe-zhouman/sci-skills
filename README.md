# sci-skills

Parts + management for research writing. Not a full suite.

## Why

The research-skills ecosystem is saturated. Everyone sells an end-to-end pipeline. Most
don't leave files on disk. Most don't talk to each other.

**Our bet: don't compete on quality. Compete on the handoff.**

We build small parts — one skill, one artifact. Each knows only files, never other skills.
Replace any part with someone else's tool — nothing breaks. We also build the management
layer: a project manager that scaffolds the workspace, writes file contracts, and translates
external outputs so everything meshes. Use our parts. Use someone else's lit review. Use
your own Excel figures. As long as outputs land on disk conforming to the contract, the
pipeline works.

**A part that cooperates beats a closed suite.** This is our survival strategy — and our
only differentiator.

## Architecture

### Skills know files, not each other

Every skill reads and writes on-disk files in `sci-skills/`. No skill imports another's
code or assumes another's presence. Replace the producer, keep the file contract — nothing
breaks. Any agent, any tool, any human can produce into a directory as long as the
`CONTRACT.md` is honored.

### Claim-driven, not template-driven

A single `claim.md` anchors everything. sci-write establishes it — data vs claim
calibration, literature benchmarking. sci-story reads it to draft Introduction and
Discussion. sci-polish checks every editorial change against it. sci-submit reads
its journal ambition for venue selection. Every figure is a sub-claim. Every section
serves the one-sentence argument.

### Three layers of decoupling

| Layer | What it does | Example |
|---|---|---|
| Execution skills | Produce one kind of artifact | sci-draw → figures; sci-write → method/results/conclusion |
| File contracts | The universal handoff surface | `CONTRACT.md` per directory — any producer, any consumer |
| Project manager | Scaffold, translate, audit | sci-skills-init builds workspace, migrates external outputs |

### Human-in-the-loop at hard gates

Claim calibration. Paper-plan confirmation. Figure-reading check. Every section's
confirmation gate. Self-checks before human review. The agent proposes, the human decides.
No "fully automated" claims — real research never has been.

### Scene-based, not one-size-fits-all

One scene = one skill set. Scene A (English journal submission) is what ships today.
Scene B (Chinese thesis), Scene C (grant proposal) are separate scenes with their own
parts and contracts. Skills don't cross scenes — file-contract philosophy is the
only shared DNA.

### Top-journal floor, not journal-dependent rules

Write to Nature/Science standards regardless of target venue. 求其上者得其中. Introduction
is a two-stage funnel (domain-level gap → research-level gap). Discussion fuses Conclusion
as its first paragraph — the common denominator across almost all journals.

### Outsourcing is by design

We own the parts we do well. We outsource the rest — but require outsourced outputs to
land on disk conforming to file contracts. sci-skills-init translates external outputs
(Word→tex, manual figures→warehouse, others' markdown→paper-plan entries) so downstream
skills can consume them. The family is the CI/CD layer for research outputs.

## Pipeline

```
claim.md ──────────── the central contract (sci-write Step 0)
  │
  ├─→ sci-draw ───── figures + figure reports (conclusion-driven)
  ├─→ sci-write ──── method / results / conclusion (claim-anchored)
  │                    sup-list.md (SI parking, accumulated during writing)
  ├─→ sci-story ──── introduction (two-stage funnel) / discussion (+ fused conclusion) /
  │                    abstract / title / keywords
  ├─→ sci-export ─── md→tex + SI assembly + cross-ref check / tex→docx
  ├─→ sci-polish ─── direct tex editing, git as audit trail
  └─→ sci-submit ─── journal selection, cover letters, submission tracking
```

## Skills

| Skill | Does | Human gates |
|---|---|---|
| [sci-skills-init](skills/sci-skills-init/) | Scaffold workspace, write contracts, audit layout, migrate external files | Every migration destination confirmed |
| [sci-draw](skills/sci-draw/) | Publication-quality figures + structured figure reports | Panel plan approved before drawing |
| [sci-write](skills/sci-write/) | Method / Results / Conclusion from figures + data. Claim-vs-figure consistency. | claim.md confirmed; paper-plan confirmed; figure-reading check |
| [sci-story](skills/sci-story/) | Introduction (two-stage funnel) / Discussion (+ fused conclusion) / Abstract / Title / Keywords. Literature search. | Claim read & confirmed; confirmation gate per section; self-checks |
| [sci-polish](skills/sci-polish/) | Polish tex prose directly. Git as audit trail. AI-prose anti-patterns. | Git diff review |
| [sci-export](skills/sci-export/) | md→tex (drafted content → manuscript). tex→docx (pandoc). SI assembly + cross-ref check. | Template choice confirmed |
| [sci-submit](skills/sci-submit/) | Hard constraints → journal selection → cover letters → rejection handling → submission tracking | Hard constraints collected; cover letter per paragraph confirmed |

## Philosophy in one sentence

小零件，大契约。不卖全家桶。能跟别人配合的零件比封闭套件活得久。

## Installation

```bash
git clone -b release git@gitcode.com:Joe-zhouman/sci-skills.git
```

| Branch | Purpose |
|---|---|
| [`release`](https://gitcode.com/Joe-zhouman/sci-skills/-/tree/release) | Clean distribution — install this |
| [`master`](https://gitcode.com/Joe-zhouman/sci-skills) | Full development history |

## Development

Every skill follows [skill-creator-plus](https://github.com/Joe-zhouman/skill-creator-plus).
