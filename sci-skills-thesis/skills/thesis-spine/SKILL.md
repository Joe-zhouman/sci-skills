---
name: thesis-spine
description: >-
  Thesis writing-chain entry — establish the main line (主线) + unified framework (统一框架)
  + inter-chapter progression (章间递进) + thesis-level claim (umbrella) from N small papers,
  BEFORE any chapter is dissected. Staged depth-gates with backtrack; AI proposes candidates
  marked `pending` (never auto-adopted) and tension-flags (questions, not verdicts); the author
  gates architecture depth (AI cannot honestly audit depth — it generates the shallowness it
  checks). Produces thesis-spine.md (the baton dissect/intro/summary/theory read) + seeds
  thesis-terminology-ledger.md. Reads thesis-sources.md + template-spec.md + the small papers
  (high-level intake only — no deep reading, no tex, no paper→chapter binding; those are
  dissect's job). Triggers: 提主线, 统一框架, 章间递进, thesis spine, 主线框架, thesis-level claim.
---

# thesis-spine

Establish the architecture-level baton — main line (主线), unified framework (统一框架),
inter-chapter progression (章间递进), and thesis-level claim (umbrella) — from N small
papers, **before any chapter is dissected**. Without these, dissect builds on sand: each
chapter is a standalone paper, the chapters don't progress into each other, the intro's gap
can't callback, the summary has no common framework to extract. Output is **`thesis-spine.md`**
(the rich baton dissect / intro / summary / theory read) + a seeded
`thesis-terminology-ledger.md`. There is no tex written here, no paper→chapter binding, no
deep reading — those are dissect's job (拆即写). Run before dissect, after thesis-init.
The author advances the pipeline by invoking each writing skill (read neighbors, don't
orchestrate). This skill serves the author first — the author gates architecture depth; AI
assists, never substitutes for the author's depth judgment.

## Core discipline (state upfront)

This is the family's anti-pattern defense. Four rules, all load-bearing:

1. **AI proposes candidates marked `pending`, never auto-adopts.** A field still marked
   `pending` is unsettled — dissect must not build on it.
2. **AI tension-flags = questions to the author, never verdicts.** Each tension carries three
   elements: (a) the tension, (b) specific evidence (paper / figure / §), (c) a question for
   the author. AI never asserts "this framework is shallow" — that is depth-gating, forbidden.
   Detail in `references/writing-discipline.md`.
3. **The honest residual (state it, don't hide it):** tension-flagging is depth-INFLUENCE, not
   depth-gating. AI deciding which tensions to raise biases the author's attention —
   attachment-blind authors may be led by the framing. This is an irreducible residual, named
   as a stated failure mode, not solved. AI's one real edge over the author is the absence of
   attachment; tension-flagging preserves it without crossing into depth-gating (spec §⑤).
4. **Depth is human-gated only.** Is the main line sharp? framework high-level or hollow?
   progression insightful? umbrella overclaim? AI cannot honestly check these — checking "is
   this framework deep" produces the shallowness it checks. The author gates depth; AI assists.

## Layout & boundaries

```
<project-root>/
  thesis/                            ← thesis artifact (by chapter) — spine does NOT write tex here
  sci-skills/
    thesis-spine.md                  ← THIS skill produces (the rich baton — schema below)
    thesis-terminology-ledger.md     ← THIS skill seeds (cross-chapter terms; chapters/polish co-write)
    thesis-sources.md                ← thesis-init produces; spine reads (paper registry)
    template-spec.md                 ← thesis-init produces; spine reads (chapter-naming convention)
  <small papers>                     ← external; spine reads for high-level intake only
```

Compass-file coupling (罗盘文件) — no skill calls a sibling skill; handoff is via on-disk files.

| File | Produced | Read by | Role (spec §跨 skill 文件交接) |
|---|---|---|---|
| `thesis-spine.md` | spine | dissect / intro / summary / theory | main line + framework + progression + umbrella + boundary (the baton) |
| `thesis-terminology-ledger.md` | spine **seeds** | each chapter / polish (co-write) | cross-chapter term unification (seeded entries `source: thesis-spine`) |
| `thesis-sources.md` *(read)* | thesis-init | spine | source registry (paper_id / paths / slug / claim) |
| `template-spec.md` *(read)* | thesis-init | spine | chapter-naming convention (so progression roles align) |
| small papers *(read)* | external | spine | per-paper claim + IMRaD structure (high-level intake) |
| `scripts/check_spine.py` *(spine's own)* | spine | spine Step 5 | coverage mechanical gate (deterministic; stdlib-tested — assert script, no pytest) |

- **Spine produces top-level `thesis-spine.md` + seeds `thesis-terminology-ledger.md`.** No
  working-notes directory (spec §② — spine is directory-less; a single rich baton holds product
  + Intake + Cracks + Alternatives, mirroring sci-write's claim.md where argument + evidence
  baseline cohabit one file).
- **Does NOT write tex, bind paper→chapter, or deep-read papers.** Deep reading + dissection +
  chapter tex are dissect's job (拆即写). Spine does high-level intake only: claim + IMRaD
  structure + how a paper could fit a main line.
- **`scripts/check_spine.py` is spine's own helper**, living in the plugin source
  (`scripts/check_spine.py`), not the project working dir — does not violate "spine has no
  working directory". Step 5 runs it.
- **Reads `thesis-sources.md` + `template-spec.md` + the small papers.** All read-only; spine
  writes only `thesis-spine.md` + the seeded ledger.

## File contracts

| File | Produced by | Read by | Schema / role |
|---|---|---|---|
| `thesis-spine.md` | this skill (author settles) | dissect, intro, summary, theory | main line + framework + progression + umbrella + boundary + Intake + Cracks + Alternatives — full template in `references/spine-schema.md` |
| `thesis-terminology-ledger.md` | this skill **seeds** | each chapter, polish (co-write) | canonical cross-chapter term forms; seeded entries marked `source: thesis-spine` |
| `thesis-sources.md` | thesis-init | this skill (reads) | paper registry: `paper_id` / `paths` / `slug` / `claim` |
| `template-spec.md` | thesis-init | this skill (reads) | chapter-naming convention (so progression roles align with the template) |
| small papers | external | this skill (reads) | per-paper claim + IMRaD structure (high-level intake) |
| `scripts/check_spine.py` | this skill (plugin source) | this skill (Step 5) | coverage mechanical gate — 3 structural fields, no `pending`, sub-coverage |

## Workflow

Steps run in order; each structural stage depends on the previous (main line → framework →
progression → umbrella). **Steps 1–4 each stop for a depth human-gate** — do not skip those
gates. The umbrella (Step 4) is depth-gated, NOT coverage — `check_spine.py` does not check it
(spec §门).

The baton schema (spec §thesis-spine.md schema; full template in `references/spine-schema.md`):

```markdown
# thesis-spine.md
> Baton. Settled by the author (depth human-gated). Read by dissect/intro/summary/theory.
> `pending` = AI candidate, NOT author-adopted. A field still marked `pending` is unsettled
> — dissect must not build on an unsettled field.

## Main line (主线)                    ← thread connecting the N papers        (structural, coverage-gated)
## Unified framework (统一框架)         ← framework + per-paper instantiation  (structural, coverage-gated)
## Inter-chapter progression (章间递进) ← research-chapter role sequence, 1:1   (structural, coverage-gated)
## Thesis-level claim (umbrella)       ← one-sentence total contribution        (depth-gated, NOT coverage)
## Boundary                            ← what the umbrella does NOT establish   (depth-gated)
## Intake (per-paper evidence base)     ← high-level intake from the small papers
## Cracks flagged                       ← tension-flagging: questions, not verdicts (§⑤)
## Alternatives considered              ← collapsed candidates (audit trail)
```

Product = top 5 sections (main line / unified framework / inter-chapter progression /
thesis-level claim / boundary). Intake / Cracks / Alternatives = evidence base + audit trail
(mirrors sci-write's claim.md where argument + evidence baseline cohabit one file).

### Step 0 — Read the room (startup/resume)

1. Read `thesis-sources.md` (the registry). Missing or empty → **hard stop**: "run
   thesis-init and fill the registry first." (This is the inverse of dissect's spine.md-
   existence boundary — spine cannot intake papers it cannot see.)
2. Read each small paper per the registry `paths` for **high-level intake only**: claim +
   IMRaD structure + how it could fit a main line. Write `## Intake` in spine.md (one line per
   paper). **Tex → Read; PDF → `mcp__extract__analyze_doc` (never Read on PDF — global rule).**
   No deep reading, no paper→chapter binding — those are dissect's job.
3. Read `template-spec.md` (chapter-naming so progression roles align with the template's
   chapter scheme).
4. Seed `thesis-terminology-ledger.md` from cross-paper terms (mark each seeded entry
   `source: thesis-spine`).
5. On resume: if spine.md has settled sections (no `pending`), skip to the first unsettled
   stage. Intake persists, so no re-reading papers.

### Step 1 — Main line (主线 thread)

1. AI proposes main-line candidates, marked `pending`: one-sentence thread connecting the N
   papers, grounded in Intake (spec §工作流).
2. AI tension-flags (Core discipline + `references/writing-discipline.md`).
3. **Stop. Author gates depth** — is the thread sharp? Does it actually unify the N papers, or
   is it just a label?
4. Settled → `## Main line`.

### Step 2 — Unified framework (统一框架)

1. AI proposes framework candidates, marked `pending`, building on the **confirmed** main
   line: the framework + how each paper instantiates it.
2. AI tension-flags.
3. **Stop. Author gates depth** — high-level, or hollow?
4. Settled → `## Unified framework`.
5. **Coverage check (mechanical)**: each paper in Intake declares an instantiation. A paper
   lacking it is a contract gap — ask the author.

### Step 3 — Inter-chapter progression (章间递进)

1. AI proposes progression candidates, marked `pending`: research-chapter **roles** in
   sequence (default 1:1 with N papers). Each role declares its question + how it advances the
   main line. **Paper-agnostic** — roles, NOT paper→chapter bindings (binding is dissect's
   job, 拆即写; spec §④). Dissect binds papers to roles in `chapter-map.md` (supports merge /
   split); bind-miss falls back to spine.
2. AI tension-flags.
3. **Stop. Author gates depth** — is the progression insightful, or just a list?
4. Settled → `## Inter-chapter progression`.
5. **Coverage check (mechanical)**: each role declares advance + question.

### Step 4 — Thesis-level claim (umbrella) + Boundary

1. Now the 3 structural fields are settled. AI proposes the umbrella candidate, marked
   `pending`: one-sentence total contribution that the 3 fields collectively argue (spec §③ —
   umbrella is the depth-gated 4th field, distinct from the 3 coverage-gated structural fields;
   NOT collapsed into the main line, which would lose its independent depth-gate).
2. AI tension-flags — overclaim beyond what the 3 fields establish? hollow?
3. Define `## Boundary` — what the umbrella does NOT establish (mirror sci-write's claim.md
   boundary).
4. **Stop. Author gates depth** — umbrella overclaim? hollow? boundary honest?
5. Settled → `## Thesis-level claim` + `## Boundary`.

### Step 5 — Handoff

1. Run the coverage mechanical gate:
   ```bash
   python scripts/check_spine.py <project>/sci-skills/thesis-spine.md
   ```
   It checks: no `pending` residual + 3 structural fields non-empty + sub-coverage (framework:
   each paper instantiated; progression: each role has advance + question). **The umbrella +
   boundary are NOT checked — they are depth, human-gated** (spec §门; the script source
   confirms — `STRUCTURAL_FIELDS` excludes umbrella).
2. If it passes, spine.md is the settled baton. dissect / intro / summary / theory read it.
3. Point the author to **thesis-dissect** (binds papers to the progression roles, 拆即写). Do
   NOT auto-run it — read neighbors, don't orchestrate.

### Backtrack

At any depth-gate, if the author finds an earlier component wrong (e.g. the framework won't
propose cleanly → the main line is wrong), revise the earlier component and re-propose
downstream. Re-mark downstream candidates `pending` (spec §① — staged gates with backtrack;
forbidding backtrack forces the author to prop up a bad main line).

## Pervasive discipline

Runs around every stage, not a separate step. Detail in `references/writing-discipline.md`:

- **Confirmation gate** before each stage settles — echo the chain (main line → framework →
  progression → umbrella) and get the author's confirmation.
- **Tension-flagging is questions-not-verdicts** + the depth-INFLUENCE stated failure mode
  (spec §⑤): AI deciding which tensions to raise biases the author's attention;
  attachment-blind authors may be led by the framing. Named as a stated failure mode, not
  solved. Forbidden: framing tension-flagging as fact-checking analogous to sci-write's
  `figN-reading` (false equivalence — figN-reading checks prose vs. rendered PNG between two
  concrete artifacts; tension-flagging judges framework abstraction vs. paper content, i.e.
  depth). Tension-flagging's honest subset (checkable cross-consistency facts) overlaps the
  coverage/grounding mechanical layer; its unique value (attachment-blind tension) IS the
  depth-influence, accepted and named.
- **`pending` protocol** — AI proposes candidates marked `pending`, never auto-adopts. A field
  still `pending` is unsettled; dissect must not build on it.
- **Verb calibration** — state contributions with strong verbs (`establishes`, `shows`), hedge
  interpretations (`suggests`, `may`). Don't put hedge verbs in the umbrella's declaration.
- **The honest boundary** (spec §Load-bearing premise) — decoupling prevents ABSENT spines
  (dissect cannot proceed without spine.md), not HOLLOW ones. A hollow spine can pass coverage
  + author confirmation if the author's judgment falters (attachment blind spot + tension
  framing bias can stack). There is no structural mechanism that substitutes for the author's
  depth judgment. Named as a stated failure mode, not overclaimed.

## Reference index

| File | Open when |
|---|---|
| `references/writing-discipline.md` | Before any stage — tension-flagging protocol (3 elements + question-not-verdict), confirmation gate, `pending` protocol, depth-INFLUENCE failure mode, verb calibration |
| `references/spine-schema.md` | The full `thesis-spine.md` template — what each of the 8 sections holds (Main line / Unified framework / Inter-chapter progression / Thesis-level claim / Boundary / Intake / Cracks flagged / Alternatives considered) |

## Privacy

Don't leak private paths, filenames, or unpublished paper content in spine.md's Intake / Cracks
flagged, user-facing replies, or commit messages. Use generic descriptions ("paper-C §4.2");
reveal exact paths only when the author asks for an audit trail.
