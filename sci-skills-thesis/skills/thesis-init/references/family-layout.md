# Family layout — depth reference

Read this when modifying the thesis family layout or directory contracts, or
when deciding whether to add a new sibling skill or a new university template
pack. For the execution-time layout (what `init` builds, what `checkup`
reports), see SKILL.md — that's the short version you need on every run. This
file is the "why and how to evolve it" detail.

## Table of Contents

- Why the shared name `sci-skills/`
- Source vs output split
- The directory-contract principle (deeper)
- Per-directory contract overview
- Cross-directory data flow
- Naming conventions
- Evolution rules
- Decoupling self-check

## Why the shared name `sci-skills/`

Analogous to superpowers's `docs/superpowers/` — this is the **family's identity
marker**, not a per-project name. Anyone (human, skill, init script) seeing a
`sci-skills/` directory immediately knows it's the on-disk workspace shared by
both the article family and the thesis family.

The thesis family shares this workspace with the article family by design: a
single project may hold its small papers under `manuscript/` (article family's
first-class artifact) **and** its thesis under `thesis/` (thesis family's
first-class artifact), both reading/writing the same `sci-skills/`. The two
families coexist without one knowing the other's code — they share the
workspace name, nothing more.

Collision is avoided by **prefixing** the thesis family's shared files with
`thesis-`: `thesis-sources.md`, `thesis-spine.md`, `thesis-terminology-ledger.md`,
`thesis-README.md`. The article family's files (`sci-write/terminology-ledger.md`,
`sci-skills/README.md`, etc.) keep their unprefixed names. The prefix is the
collision boundary; the shared dir is the coexistence boundary.

One asymmetry: thesis-init does **not** write a root `.gitignore` (the article
family or the human may own one — writing one would collide). It writes
`thesis/.gitignore` — thesis-scoped LaTeX build products, inside `thesis/`,
never touching anything at the project root.

## Source vs output split

- **Skill source**: in the repo at `skills/<skill-name>/` (SKILL.md / scripts /
  references). For the thesis plugin this lives at
  `sci-skills-thesis/skills/thesis-init/`.
- **Skill output**: in the user's project at `<project-root>/sci-skills/<skill-name>/`
  for working notes, and `<project-root>/thesis/` for the first-class artifact.

Same name, different places. Source is the skill's implementation; output is what
it produces. `init` manages only the output side (the project's `thesis/` and
`sci-skills/`); it never touches the source side.

`thesis/` is the one exception to "output lives under `sci-skills/`" — it sits
at the project root as a first-class citizen, peer to `sci-skills/`. The product
(the thesis) is bigger than the tool (the skill family); the product does not
nest inside the tool's workspace.

## The directory-contract principle (deeper)

Each subdirectory holds a `CONTRACT.md`. **This file is that directory's interface
contract**, not a help doc.

The contract has two audiences, only one of which needs it:

- **Internal skills** (those in the family routing table): they already know the
  schema from their own SKILL.md / references. For them, `CONTRACT.md` is
  redundant — they don't read it.
- **External producers** (unfamiliar skills, manual tools, a human dropping files
  in): they have no internal knowledge of the family. Their only way to learn
  "what shape should my output take?" is to read the contract in the directory.

This is why `CONTRACT.md` must be **visible** (`ls` shows it), not hidden. An
external producer scanning the directory won't know to `cat` a dotfile — if the
contract is invisible, it doesn't exist for them. Visibility = reachability for
the audience that actually needs it.

`CONTRACT.md` is intentionally NOT named `README.md` — that name collides with
the article family's `sci-skills/README.md` in a coexist project (which is why
the thesis routing table is `thesis-README.md`), and with skill-level READMEs
meant for human readers. The name `CONTRACT.md` is semantically unambiguous:
this file is the interface spec for this directory.

- Any agent/skill wanting to produce into the directory reads the contract to
  know what to put there: schema, field names, naming, who reads it.
- No need to know which skill consumes it, no need to import anything — produce
  to the contract, downstream consumes automatically.

**Contract gaps are never fabricated or skipped.** If a producer finds the
contract silent on a case it needs to handle, it stops, lists the gap, and fills
the contract text first (in `SKILL_DIR_CONTRACTS` / `THESIS_CONTRACT` in
`init_project.py`) — then produces to the updated contract. Producing past a gap
means silently inventing a convention nobody else will honor. **Update the
contract in the same act you update the product** — a product whose contract
wasn't updated is an orphan the next skill can't read.

**This is decoupling made real**: contracts live in files, not in code imports.
A brand-new, unfamiliar writing agent reads `thesis-dissect/CONTRACT.md`,
produces to it, and thesis-summary can consume the result — skills are
replaceable as long as the directory contract is honored.

## Per-directory contract overview

(Full detail in each directory's own `CONTRACT.md`, generated by `init`.)

| Directory / file | Role | Key contract | Producer | Consumer |
|---|---|---|---|---|
| `thesis/` | the thesis (first-class, by chapter) | `CONTRACT.md` + `template-spec.md` woven at init | dissect, intro, theory, summary (write tex); polish, typeset (edit in place) | human, all skills (read) |
| `thesis/tex/` | prose source (template woven here at init) | naming follows `template-spec.md`, not hardcoded | dissect / intro / theory / summary write chapter tex | polish, typeset edit; human compiles |
| `sci-skills/thesis-sources.md` | source registry (navigation truth) | one entry per small paper: paper_id / paths / data_paths / slug / claim | thesis-init (placeholder) + agent (fills) | all thesis skills |
| `sci-skills/thesis-spine.md` | main line + unified framework + chapter progression + thesis claim (接力棒) | placeholder until spine runs | thesis-spine | dissect, intro, summary, theory |
| `sci-skills/thesis-terminology-ledger.md` | cross-chapter terminology | placeholder until spine builds it | thesis-spine (creates); all chapters + polish (co-write) | polish, all writing skills |
| `sci-skills/thesis-README.md` | thesis-family routing table | lists shared files + sibling dirs | thesis-init | human, any skill landing in `sci-skills/` |
| `sci-skills/thesis-dissect/` | working notes per small paper | `chapter-map.md` + `paper-X/` subdirs | thesis-dissect | thesis-spine, thesis-summary (read `chapter-map.md`) |
| `sci-skills/thesis-intro/` | intro-chapter working notes | file names settle with thesis-intro design | thesis-intro | thesis-spine |
| `sci-skills/thesis-theory/` | ch2 shared-theory working notes | file names settle with thesis-theory design | thesis-theory | thesis-dissect (reads shared theory) |
| `sci-skills/thesis-summary/` | synthesis-chapter working notes | file names settle with thesis-summary design | thesis-summary | thesis-spine |

`thesis-spine`, `thesis-polish`, `thesis-typeset`, and `thesis-init` have **no
pre-built directory** under `sci-skills/`:

- **thesis-spine** produces top-level shared files (`thesis-spine.md` +
  `thesis-terminology-ledger.md`) — it writes to `sci-skills/` root, not a subdir.
- **thesis-polish** edits `thesis/tex/*.tex` in place (prose, terminology, AIGC
  reduction) — git history is the audit trail, no separate output dir.
- **thesis-typeset** edits `thesis/tex/` in place (readability typesetting,
  .cls compliance, compile) — same, no separate dir.
- **thesis-init** is the entry node — it scaffolds and exits, produces nothing
  that needs a persistent dir of its own.

They are absent from the `BROTHER_SKILLS` list (`thesis-dissect`,
`thesis-intro`, `thesis-theory`, `thesis-summary` — the four that carry working
notes and so get a pre-built dir + `CONTRACT.md`).

## Cross-directory data flow

Skills do **not** call each other. They read neighbors' on-disk outputs and
sense what's ready. This is the material basis of "read neighbors, don't
orchestrate."

The writing chain reads through files, not calls:

- **thesis-spine** reads `thesis-sources.md` (registry) + each small paper's
  tex/notes. Produces `thesis-spine.md` (main line + unified framework + chapter
  progression + thesis claim) and creates `thesis-terminology-ledger.md`.
- **thesis-dissect** reads `thesis-spine.md` + `thesis-sources.md` +
  `template-spec.md`. For each small paper: dissects and writes the chapter tex
  **directly into `thesis/tex/`** (拆即写 — dissect-and-write in one pass, no
  separate "split then write" steps). Produces `chapter-map.md` in
  `sci-skills/thesis-dissect/` (the dissect→summary handoff surface).
- **thesis-intro** reads `thesis-spine.md` + `thesis-sources.md` + the body
  chapter tex. Writes the intro chapter tex directly into `thesis/tex/`.
- **thesis-summary** reads `thesis-spine.md` + `chapter-map.md` + the intro tex
  + each body chapter tex. Writes the synthesis chapter tex into `thesis/tex/`.
- **thesis-theory** reads `thesis-spine.md` + each body chapter tex (it runs
  **last** — body chapters must exist so theory can unify their shared theory).
  Writes the shared-theory chapter tex into `thesis/tex/`. Marks overlaps into a
  list for the author to resolve manually — it does not re-edit dissect's product.
- **thesis-polish** reads `thesis-terminology-ledger.md` + edits `thesis/tex/*.tex`
  in place (cross-chapter consistency, AIGC reduction, de-AI-voice). Co-writes
  the terminology ledger. git history is the audit trail.
- **thesis-typeset** reads `template-spec.md` + `thesis/CONTRACT.md` + edits
  `thesis/tex/` in place (readability, .cls compliance, compile). git history.

**tex always lands in `thesis/tex/`**, never in a working-note dir. Chapter
filenames follow `template-spec.md` (the woven spec beside `tex/`), never
hardcoded by a skill. Working-note dirs (`thesis-dissect/`, `thesis-intro/`,
`thesis-theory/`, `thesis-summary/`) hold only process metadata —
`chapter-map.md`, gap analysis, claim records, theory-unification notes.

The four shared files (`thesis-sources.md`, `thesis-spine.md`,
`thesis-terminology-ledger.md`, `thesis-README.md`) plus `chapter-map.md` are
the **entire coupling surface** of the family. No skill imports another; no
skill triggers another to run. thesis-init is the **only node that knows all
siblings** (it carries `BROTHER_SKILLS` + `SKILL_DIR_CONTRACTS` + the
`thesis-README.md` routing table); every other skill knows only files.

Data flow is **not strictly linear** — theory runs last (after body chapters),
intro and summary read body chapters that dissect produced, polish and typeset
run on the finalized tex. The one bidirectionally shared file is
`thesis-terminology-ledger.md` (spine creates it; all chapters + polish
co-write). The one single-producer-single-consumer handoff is `chapter-map.md`
(dissect produces, summary reads).

## Naming conventions

- **Shared files**: `thesis-` prefix (`thesis-sources.md`, `thesis-spine.md`,
  `thesis-terminology-ledger.md`, `thesis-README.md`). The prefix is the
  collision boundary with the article family in the same `sci-skills/` workspace.
- **Chapter filenames**: follow the woven `template-spec.md` — **never hardcoded
  by a skill**. Different schools use different conventions (`chapterN.tex`,
  `chap-0-intro.tex`, thuthesis's own scheme); the template pack declares its
  naming, and each writing skill reads `template-spec.md` to align. Swapping a
  template pack = swapping the naming convention, zero skill code change.
- **`chapter-map.md`**: fixed name, lives in `sci-skills/thesis-dissect/`. It's
  the dissect→summary handoff surface — fixed name so summary can find it without
  configuration.
- **Template packs**: at `sci-skills-thesis/templates/thesis/<school>/` (inside
  the plugin, self-contained on standalone install). Each pack ships a
  `template-spec.md` + `.cls` + blueprint (`main.tex` etc.). The plugin is the
  pack's home — unlike the article family, whose `templates/main/` is a
  repo-root convenience referenced only in CONTRACT prose as a manual-copy
  pointer. The thesis pack is a runtime path dependency (init reads it to weave),
  so it must ship with the plugin.

## Evolution rules

- **Add a new sibling skill**: add it to `BROTHER_SKILLS` and
  `SKILL_DIR_CONTRACTS` in `scripts/init_project.py`, write its `CONTRACT.md`
  contract. Next `init` pre-builds its dir. **Only add skills that need their own
  output directory.** Skills that produce top-level shared files (thesis-spine)
  or edit tex in place (thesis-polish, thesis-typeset) or are entry-exit
  (thesis-init) do **not** get a pre-built dir — they have no persistent output
  location to scaffold.
- **Add a university template pack**: add `templates/thesis/<school>/` with
  `.cls` + blueprint + `template-spec.md`. **No skill code change** — the weave
  mechanism in `init_project.py` is pack-agnostic (it copies whatever the pack
  dir contains into `thesis/tex/`, recursing into subdirs for real packs like
  thuthesis that ship `config/` / `figures/`). This is mechanism vs data
  separation: the mechanism is code (fixed); the packs are data (extensible).
  Adding Tsinghua = adding `templates/thesis/thu/`; adding Zhejiang = adding
  `templates/thesis/zju/`; neither touches `init_project.py`.
- **Change a directory's contract**: edit its `CONTRACT.md` text (in
  `SKILL_DIR_CONTRACTS` for brother dirs, or `THESIS_CONTRACT` for `thesis/`).
  Existing projects get the updated contract retroactively on the next `init`
  run — the script fills missing contracts but never overwrites an existing one,
  so a contract change in an existing project requires the human to delete the
  old `CONTRACT.md` and re-run `init` (or edit it in place). All skills honoring
  the contract adapt automatically.

## Decoupling self-check

After changing any skill, verify it hasn't broken directory contracts:

- Do the files it writes still match the schema declared in the target dir's
  `CONTRACT.md`? (If a skill starts writing a new file, the contract must list it
  — update the contract in the same act.)
- When reading neighbors, does it assume files/fields beyond the contract? (That
  breaks when the neighbor swaps implementations. A skill reading
  `thesis-spine.md` must read only what `thesis-spine.md`'s contract promises —
  not a field that happens to be there today but isn't contracted.)
- Does it hardcode a chapter filename instead of reading `template-spec.md`?
  (That breaks the first time a different school template is used.)
- Does it call a sibling skill? (It must not. Read the neighbor's on-disk
  output; the human advances the pipeline by invoking each skill.)

Contracts are the stable surface; implementations are the variable surface.
Skills evolve independently; contracts don't move → that's what decoupling
means. thesis-init is the only node that knows the full sibling list; every
other skill knows only the files it reads — and that's enough, because the
contracts make the files self-describing.
