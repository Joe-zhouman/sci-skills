# sci-skills

Parts + management for research writing. Not a full suite.

## Why this exists

The research-skills ecosystem is crowded. Everyone has their own lit-review tool, their own plotting tool, their own writing assistant. Most of them don't talk to each other. Most don't leave files on disk for the next step to pick up.

**Our bet: don't compete on coverage. Compete on the handoff.**

We build small, focused parts (one skill = one artifact). Each part only knows files, not other skills — replace any part with someone else's tool and nothing breaks. We also build the management layer: a project manager skill that scaffolds the workspace, writes file contracts, and translates external outputs so everything meshes. Use our parts. Use someone else's lit review. Use your own Excel figures. As long as outputs land on disk with the right shape, the pipeline works.

**A part that cooperates beats a closed suite.** This is our survival strategy in a crowded field — and our only real differentiator.

## What's included

### Scene A: English journal submission

| Skill | Does |
|---|---|
| [sci-skills-init](skills/sci-skills-init/) | Project manager — scaffolds the workspace, writes directory contracts, migrates external outputs into contract-compliant files, audits layout |
| [sci-draw](skills/sci-draw/) | Publication-quality figures from experimental data + figure reports that downstream skills read |
| [sci-write](skills/sci-write/) | Data-driven manuscript drafting (Method / Results / Discussion / Conclusion) from figure reports + data profile. Claim-vs-figure consistency checks. Real-DOI citation placeholders |
| [sci-polish](skills/sci-polish/) | Polish manuscript prose directly in tex files. Git commits are the audit trail. Reads sci-write outputs to preserve claim/evidence consistency |
| [sci-submit](skills/sci-submit/) | Submission campaign manager — hard constraints, journal selection, cover letters, rejection handling, post-submission tracking |

### Scene B & C

Chinese thesis and grant proposal — separate scenes with their own parts and init. Coming later.

## How it works

```
Project root/
  manuscript/               ← the official manuscript (first-class citizen)
    v1/tex/                 ← skills read and edit here
  sci-skills/               ← skill outputs (figure reports, drafts, metadata, ledger)
    sci-draw/               ← figure warehouse (neutral — any tool can produce here)
    sci-write/              ← drafts + paper-plan + terminology-ledger
    sci-submit/             ← cover letters, journal shortlists, submission history
```

Each subdirectory has a `.README.md` contract. Any agent, any skill, any tool can read from it and produce into it — as long as the contract is honored. No skill knows who produced the files. No skill knows who will consume them. Replace the producer, swap the consumer, nothing breaks. The contracts are the universal handoff surface.

## Philosophy

- **Human-in-the-loop.** Skills produce drafts. Humans review. No "fully automated" claims — real research never is.
- **Files over imports.** The only coupling surface is the filesystem. Skills read neighbors' outputs; they never import each other's code or trigger each other to run.
- **Cooperation over lock-in.** Use our parts, mix in others, outsource what we don't do well. The management layer handles the rest.

## Installation

```bash
git clone -b release git@gitcode.com:Joe-zhouman/sci-skills.git
```

| Branch | Purpose |
|---|---|
| [`release`](https://gitcode.com/Joe-zhouman/sci-skills/-/tree/release) | Clean distribution — install this |
| [`master`](https://gitcode.com/Joe-zhouman/sci-skills) | Full dev history + test records |

## Development

Every skill follows the [skill-creator-plus](https://github.com/Joe-zhouman/skill-creator-plus) workflow (evals → iterations → benchmark → grading). Test records under `skills/*/tests/`.
