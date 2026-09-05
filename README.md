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

## Who this is for

Most research-skills assume a privileged default: good school, good data, good
equipment, an advisor who mapped the path. For that author, "do honest science
and present it well" **is** the optimal strategy — their work is strong enough
that honesty alone carries it. Their skills can afford to treat honesty as the
top principle.

This family is not written for that default. It is written for the author whose
position is **not** privileged — ordinary school, ordinary resources, work that
sometimes can only be ordinary because that's what the conditions allow. That is
not an attitude problem; it's a reality. And under that reality, "just be
honest" is not enough: an honestly-presented ordinary submission gets judged by
standards set for privileged work, and dies.

So the goal of every skill here is **acceptance under constraint** — getting a
paper accepted (and a thesis defended, a figure approved) within honest limits,
using every legitimate degree of freedom to give ordinary work its fair chance.
Not fabrication (the floor is hard: no invented data, no fake citations, no
did-what-we-didn't). But above that floor: **framing is craft, not sin.**
- `sci-submit` is driven by hard constraints (graduation, title review, advisor
  demands) — acceptance is the explicit target, not a side effect.
- `xps` treats calibration / baseline / peak constraints as legitimate narrative
  knobs — the same data tells different stories depending on how they're set.
- `sci-respond` carries seven legitimate framing tactics (reframe claim scope,
  minimize limitation, divert to SI, exploit reviewer misunderstanding) — the
  response exists to get the paper accepted, and honesty is the floor it stands
  on, not the ceiling it bows to.

This is the 黄药师 choice, not the 全真教 choice — not a moral difference, a
positional one. 名门正派 has the capital to let "实力说话"; 桃花岛 serves people
with no fallback, so it teaches 技艺. The martial art isn't lesser — it's built
for a different student. Many skill authors avoid saying this; we lay it open,
because pretending the default user is privileged serves no one in the actual
target audience.

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
| Project manager | Scaffold, translate, audit | article-init builds workspace, migrates external outputs |

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
land on disk conforming to file contracts. article-init translates external outputs
(Word→tex, manual figures→warehouse, others' markdown→paper-plan entries) so downstream
skills can consume them. The family is the CI/CD layer for research outputs.

## Skills

| Skill | Does | Human gates |
|---|---|---|
| [article-init](sci-skills/skills/article-init/) | Scaffold workspace, write contracts, audit layout, migrate external files | Every migration destination confirmed |
| [sci-draw](sci-skills/skills/sci-draw/) | Publication-quality figures + structured figure reports | Panel plan approved before drawing |
| [sci-write](sci-skills-article/skills/sci-write/) | Method / Results / Conclusion (+ SI as by-product) from figures + data, written directly as tex. Claim-vs-figure consistency. | claim.md confirmed; paper-plan confirmed; figure-reading check |
| [sci-story](sci-skills-article/skills/sci-story/) | Introduction (two-stage funnel) / Discussion (+ fused conclusion) / Abstract / Title / Keywords. Literature search. | Claim read & confirmed; confirmation gate per section; self-checks |
| [sci-polish](sci-skills-article/skills/sci-polish/) | Polish tex prose directly. Git as audit trail. AI-prose anti-patterns. | Git diff review |
| [sci-typeset](sci-skills-article/skills/sci-typeset/) | LaTeX typesetting on our template — readability fixes (loose pages, stranded headings, oversized tables) + compile to PDF | Visual PDF review |
| [sci-export](sci-skills-article/skills/sci-export/) | Move finalized tex into a target journal template (optional, decides float strategy); tex→docx (optional). | Template choice / float strategy confirmed |
| [sci-respond](sci-skills-article/skills/sci-respond/) | Response-to-Reviewers letter (point-by-point) for a revision round — tex→PDF, framing freedom within the honesty floor | Per-issue strategy locked at checkpoint; framing posture is the author's call |
| [sci-submit](sci-skills-article/skills/sci-submit/) | Hard constraints → journal selection → cover letters → rejection handling → submission tracking | Hard constraints collected; cover letter per paragraph confirmed |

## Pipeline

```
claim.md ──────────── the central contract (sci-write Step 0)
  │
  ├─→ sci-draw ───── figures + figure reports (conclusion-driven)
  ├─→ sci-write ──── method / results / conclusion / SI (tex-direct, claim-anchored)
  ├─→ sci-story ──── introduction / discussion / abstract / title / keywords
  ├─→ sci-polish ─── direct tex editing, git as audit trail
  ├─→ sci-typeset ── readability typesetting on our template + compile PDF
  ├─→ sci-export ─── (optional) move into journal template / tex→docx
  └─→ sci-submit ─── journal selection, cover letters, submission tracking
                     ↓ after reviews arrive
  rN/ ──→ sci-respond ── response-to-reviewers letter (tex→PDF, framing within floor)
          sci-revise ──── surgical manuscript edits per the locked issue-ledger
```

## Philosophy in one sentence

小零件，大契约。不卖全家桶。能跟别人配合的零件比封闭套件活得久。

## Installation

| Branch | What | Clone |
|---|---|---|
| [`v1`](https://gitcode.com/Joe-zhouman/sci-skills/-/tree/v1) | **Stable** — bug fixes only, no breaking changes | `git clone -b v1 git@gitcode.com:Joe-zhouman/sci-skills.git` |
| [`master`](https://gitcode.com/Joe-zhouman/sci-skills) | Bleeding edge — latest features, may shift | `git clone -b master git@gitcode.com:Joe-zhouman/sci-skills.git` |

After cloning, run the installer — it symlinks every skill flat into `~/.claude/skills/` (and `~/.zcode/skills/` when present) **and** sets up the Python env. The symlinks are live: repo edits show up in every new session immediately.

```bash
bash install.sh
```

The installer calls `uv sync` to create `.venv/` from the repo-root `pyproject.toml` (shared base: numpy, scipy, matplotlib, pandas, seaborn, python-dateutil, …). Skill scripts self-activate this env via a transparent launcher — agents just run `python scripts/foo.py`, no `uv run` needed. If `uv` isn't installed, the installer warns and skips env setup (install uv: <https://docs.astral.sh/uv/>, then re-run `bash install.sh`).

### Install as Claude Code plugins (marketplace)

Prefer Claude Code's native plugin system over dev symlinks? The repo root carries a `.claude-plugin/marketplace.json` exposing each family as a plugin:

```
/plugin marketplace add Joe-zhouman/sci-skills
/plugin install sci-skills@sci-skills            # scaffolding + sci-draw + thesis templates
/plugin install sci-skills-article@sci-skills    # paper writing chain
/plugin install sci-skills-thesis@sci-skills     # degree-thesis chain
/plugin install sci-skills-analysis@sci-skills   # xps (optional)
```

Marketplace installs **copy** the plugin dir into Claude Code's cache (no live link to your checkout). Each family is self-contained — template packs ship inside their family (`sci-skills/templates/thesis/`, `sci-skills-article/templates/main/`). The one extra step is the XPS env: run `uv sync` inside the installed `sci-skills-analysis` plugin dir (it carries its own `pyproject.toml`); the scripts pick up that `.venv` automatically. Updates: `/plugin marketplace update sci-skills`, then `/plugin update <name>@sci-skills`.

**`xps` is not for everyone — no XPS data, no install.** The rule is the same no matter what agent or setup is doing the install; it does not assume Claude Code:

- **No XPS needs → skip the `sci-skills-analysis` family.** Everything else (writing, figures, submission) works without it.
- The XPS-only deps (`lmfit`, `lmfitxps`, `pyarrow`) are an optional `xps` extra in `pyproject.toml`. A plain `uv sync` installs only the shared base; `uv sync --extra xps` adds XPS.
- Claude Code installs can do both in one shot: `SKIP_FAMILIES=sci-skills-analysis bash install.sh` (skips the family symlink and the `xps` extra together).
- Any other setup: don't install the `xps` extra and ignore the `sci-skills-analysis/` directory — same effect.

### XPS only (lightweight install — no tests, no writing/figure families)

The full repo carries three families and all test files. If all you need is XPS, use a sparse clone and download just the XPS footprint (<2 MB):

```bash
git clone --depth 1 --filter=blob:none --sparse https://gitcode.com/Joe-zhouman/sci-skills.git ~/sci-skills
cd ~/sci-skills
git sparse-checkout set --skip-checks sci-skills-analysis pyproject.toml uv.lock .python-version install.sh
SKIP_FAMILIES="sci-skills sci-skills-article" bash install.sh
```

The third line keeps only the XPS family + env files (`pyproject.toml` / `uv.lock` / `install.sh`); the writing and figure families and all test files never touch your disk. The fourth line skips the other two families' registration and runs `uv sync --extra xps` for you (installs lmfit / lmfitxps / pyarrow into `.venv`). Without `uv`, the installer prints how to get it — install and re-run line four.

Scripts don't care how they're invoked: `scripts/_cli.py` walks up to the repo-root `.venv` and re-execs under it (falling back to the caller's interpreter only if absent), so a plain `python scripts/foo.py` is already in the right env — no `uv run` needed.

Update later: `git -C ~/sci-skills pull && SKIP_FAMILIES="sci-skills sci-skills-article" bash ~/sci-skills/install.sh` (re-run install.sh from inside the repo).

### Submission family only (sci-write / sci-submit etc. — no figures, no XPS)

The mirror case: all you need is the submission pipeline (the `sci-skills-article` family: sci-write / sci-story / sci-polish / sci-typeset / sci-export / sci-respond / sci-submit) and you have no XPS data. Sparse-clone just that family + env files (~8 MB); the core family (article-init / sci-draw), the XPS family and all test files never touch your disk:

```bash
git clone --depth 1 --filter=blob:none --sparse https://gitcode.com/Joe-zhouman/sci-skills.git ~/sci-skills
cd ~/sci-skills
git sparse-checkout set --skip-checks sci-skills-article pyproject.toml uv.lock .python-version install.sh
SKIP_FAMILIES="sci-skills sci-skills-analysis" bash install.sh
```

The third line keeps only the article family + env files; the fourth line skips the other two families' registration and still runs `uv sync` for the shared base deps. Article-family scripts are stdlib-only — they run even without `.venv` (the launcher falls back to the caller's interpreter when it can't find one). If you also want figures, add `sci-skills` on line three and keep only `sci-skills-analysis` on line four.

Offline self-check after install:

```bash
python3 sci-skills-article/skills/sci-submit/scripts/search-ratings.py "Nature Communications"
```

should return T1/T2 hits.

Update later: `git -C ~/sci-skills pull && SKIP_FAMILIES="sci-skills sci-skills-analysis" bash ~/sci-skills/install.sh`.

### Recommended usage for XPS

Don't rely on the skill auto-triggering from a mention of "XPS" in some unrelated session. Per dataset:

1. **Create a fresh folder and put your XPS data in it** — one subfolder per sample/dataset group, so state files (`state.json`) and outputs never mix across samples.
2. **Open your agent session in that folder.**
3. **Manually invoke the skill** (`sci-skills-analysis:xps`) to start processing.

Rebuild the env later (e.g. after `git pull` changed deps):

```bash
uv sync
```

## Development

Every skill follows [skill-creator-plus](https://github.com/Joe-zhouman/skill-creator-plus).
