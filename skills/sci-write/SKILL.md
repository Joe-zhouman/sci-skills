---
name: sci-write
description: >-
  Data-driven academic manuscript writing — turn finished figures + data into
  publication prose (Method, Results, Conclusion). Use when the user has data
  and/or figures and wants to draft these three sections: write results, write
  method, write conclusion, draft from figures, claim-evidence mapping, 数据写论文,
  数据驱动写作, 把图画完写正文, 写结果/方法/结论. Drafts section by section from
  figure reports + a data profile, runs claim-vs-figure consistency checks via
  an image-understanding capability (any vision tool or vision-capable model;
  not bound to a specific tool), leaves real-DOI citation placeholders for the
  user to insert via Zotero. Does not draw figures. Introduction, Discussion,
  Introduction, Abstract, Keywords → narrative drafting (external to this skill).
---

# sci-write

Write Method / Results / Conclusion from finished figures + a data
profile. Every claim hangs on evidence (a figure, a statistic); every section
serves a one-sentence argument. Output is **md content drafts**, not the
official manuscript.

## Layout & boundaries

```
<project-root>/
  manuscript/v1/tex/             ← the OFFICIAL manuscript (user owns; this skill does NOT touch it)
  sci-skills/
    sci-draw/                    ← figure warehouse — read ../sci-draw/figN-report.md + figN.png
    sci-write/                   ← THIS skill's home — intermediate products + md drafts
      paper-plan.md              ← baton: figure list + section progress
      data-profile.json          ← data profile (Step 0 produces)
      fig1-reading.md            ← claim-vs-figure consistency check (Step 3)
      method.md results.md       ← md DRAFTS of the three sections
      conclusion.md                (content carriers; human moves into manuscript/v1/tex/ later)
      intro.md discussion.md     ← narrative sections (drafted externally, not by this skill)
      abstract.md                  same directory, different stage
```

- **Does NOT touch `manuscript/`.** md drafts in `sci-write/` are content carriers, not the manuscript. Moving them into `manuscript/v1/tex/` is the human's job (or a future md→tex skill).
- **Does NOT write to `../sci-draw/`.** Read-only on the figure warehouse. Contract gaps are reported to the human (default read-only; write back only if the human permits).
- **Output is always md.** Don't ask "md or tex" — tex is a different skill's concern.

## File contracts

| File | Produced by | Read by | Schema |
|---|---|---|---|
| `paper-plan.md` | this skill (after human confirms) | this skill (baton), human | fig entries + section status (Step 1) |
| `data-profile.json` | this skill (Step 0, via `profile_data`) | this skill (Method) | `profile_data()` return dict as JSON |
| `../sci-draw/figN-report.md` | any figure-maker | this skill (claim/findings/stats) | 6-section markdown (see neighbor-contract ref) |
| `../sci-draw/figN.png` | any figure-maker | this skill (Step 3 → an image-understanding capability) | PNG |
| `figN-reading.md` | this skill (Step 3) | this skill (Results/Discussion) | consistency-check schema (Step 3) |

## Workflow

Steps run in order; each depends on the previous. **Steps 1 and 3 stop for human confirmation** — do not skip those gates.

### Step 0 — Intake & data analysis

1. Receive raw data + research question.
2. Profile the data. If `profile_data` (from the figure warehouse) is available, borrow it as a side-effect-free tool:
   ```bash
   python -c "import json, sys; sys.path.insert(0,'../sci-draw/scripts'); from profile_data import profile_data; json.dump(profile_data('<data-file>'), open('data-profile.json','w'), ensure_ascii=False, indent=2)"
   ```
   If unavailable, ask the human for the key facts (N, per-group n, variable semantics, distribution shape) — don't fabricate.
3. Make a scientific judgment: what claims can this data support, how many figures, what each argues.

### Step 1 — Draft paper-plan  (human intervention point)

1. Draft a figure list. Each entry reuses figure-report field names (plan→report = same schema, pending→done):
   ```
   ## Figure fig1
   - topic: <one-line theme>
   - claim: <what this figure will argue>      # ↔ report Core conclusion
   - data-source: <file or description>         # ↔ report Data source
   - suggested-chart: <recommended chart type>  # ↔ report Chart type
   - status: pending
   - report-ref:                                 # filled when drawn
   ```
   Add a `## Sections` block: Method/Results/Conclusion `pending`, Introduction/Discussion/Abstract/Keyword `story-drafted` (narrative sections, external to this skill).
2. **Stop. Show the human.** Ask them to confirm/edit the claim list (which claims, how many figures, which data each uses). The whole downstream rests on this — a wrong claim wastes every later step; confirming now is far cheaper than discovering it in drafted prose.
3. After confirmation, write `paper-plan.md`.
4. Prompt: "Figures 1–N are pending. Go draw them — any tool, any session. Come back when done. I will not auto-trigger drawing."

### Step 2 — Sense the neighbor (every start / resume)

```bash
python scripts/scan_neighbor.py                  # scans ../sci-draw/*-report.md, compares to paper-plan
python scripts/scan_neighbor.py /abs/sci-skills  # absolute path for testing
```

Reports each figure's status (plan status vs report existence, discrepancies). Propose status changes; the human confirms before anything is written to paper-plan. Sensing is automatic (a read); writing the plan is human-gated.

### Step 3 — Figure-reading consistency check  (human intervention point)

For each figure with a ready report:

1. Read `../sci-draw/figN-report.md` → `Core conclusion` (the claim). Missing or not one sentence → contract-gap handling (ask, don't fabricate).
2. Use an **image-understanding capability** (any vision tool or a vision-capable model — not bound to a specific one; see figure-reading ref) at high effort on `../sci-draw/figN.png`, with an audit prompt that asks for an independent reader view (what it conveys / notable features / potential misreads). **Do not pass the claim** — independence is what makes the check honest. The claim comparison is done by this skill, not by the vision step.
3. Compare description vs claim: agree where? where might a reader misread (overlapping error bands, divergent series, non-zero axis start)?
4. Write `figN-reading.md`:
   ```markdown
   # Figure figN — 图义核查
   ## claim (from report)
   <figN-report Core conclusion>
   ## figure conveys (from image-understanding, independent reader view)
   <vision description>
   ## consistency
   - agree: ...
   - misread risk: ...  (tie to specific visual feature)
   ## claim correction suggestion
   <soft suggestion: narrow / re-draw / add qualifier — human decides>
   ```
5. **Stop. Ask the human**: "Figure-reading found [discrepancy]. Suggest [narrow / re-draw / qualifier]. Which?" Never silently rewrite the claim.

A typeset-perfect figure can still mislead at the argument level — claim says "A beats B" but overlapping bands make a reader see "comparable." Catching it here prevents building prose on a claim readers won't accept.

### Step 4 — Write Results

1. Read each `figN-report.md` (claim/findings/stats) + `figN-reading.md` (corrected claim wins if there's a correction).
2. Draft by evidence ladder: system validation → main result → baseline → ablation → stress test. Not every paper has all rungs; order by each figure's evidence role.
3. Every claim hangs on evidence (figure + statistic). Calibrate verbs to evidence strength (`show`/`demonstrate` for direct main results, `suggest`/`indicate` for trends, `may`/`could` reserved for Discussion).
4. Run the **confirmation gate** (writing-discipline ref) before full prose: echo the one-sentence argument + key terms + assumptions; get human confirmation.
5. Write `results.md` (content draft in `sci-write/`, not the manuscript).

### Step 5 — Write Method + Conclusion

**Method** (factual, no literature search):
- Data description from `data-profile.json` (N, per-group n, variables, missingness).
- Statistical methods **copied verbatim** from each `figN-report.md` `Statistical methods` — don't paraphrase, round, or "improve." Missing field → contract-gap handling.
- Write `method.md`.

**Conclusion** (short, from findings):
- Contribution + one-line evidence + one-line limitation + one-line bounded impact. No new data, citations, or mechanisms not already in Discussion.
- Write `conclusion.md`.

Method's verbatim rule: statistics are facts, prose is narrative — never let narrative instinct alter a number or test name.

### Step 6 — External handoff (no orchestration)

1. Mark Introduction/Discussion/Abstract/Keyword `story-drafted` in paper-plan (narrative sections, external to this skill).
2. Two handoffs, neither orchestrated by this skill:
   - **Content → manuscript**: "Method/Results/Conclusion md drafts are at `sci-skills/sci-write/`. They're content drafts, not the manuscript — move content into `manuscript/v1/tex/` when ready."
   - **Narrative chapters**: "Introduction/Discussion/Abstract/Keywords are drafted in a separate stage, reading `sci-skills/sci-write/` + figure warehouse reports and writing `intro.md`, `discussion.md`, `abstract.md` into `sci-skills/sci-write/`."
3. Set the three sections (Method/Results/Conclusion) to `written` in paper-plan.

## Pervasive discipline (Steps 4–5)

Runs around every section draft, not a separate step. Detail in `references/writing-discipline.md`:
- Confirmation gate before each section's full prose.
- Targeted revision — change only what the human flags, never silent full rewrites.
- Verb calibration to evidence strength.
- Claim must hang on evidence — else `[evidence needed]` placeholder, not fabricated.
- Sweep unsupported novelty/universal claims (`first`, `unprecedented`, `always`).
- Real-DOI citation placeholders; human does final Zotero insertion.

## Contract-gap handling

When a report field is missing/malformed (no `Statistical methods`, empty `n`, claim not one sentence):
1. Don't fabricate the missing content.
2. Don't skip the figure.
3. Stop, list the gap, ask the human to fill.
4. Write the filled content back (to the report if the human permits editing the warehouse, else to `figN-reading.md`'s "contract supplement"). **The fill becomes contract** — downstream steps use it as canonical.

Detail and the why in `references/neighbor-contract.md`.

## Reference index

| File | Open when |
|---|---|
| `references/writing-discipline.md` | Before drafting any section (confirmation gate, verb calibration, citation protocol, output format) |
| `references/figure-reading.md` | At Step 3 (image-understanding capability for audit, audit prompt, figN-reading schema, claim-correction handling) |
| `references/section-templates.md` | At Steps 4–5 (Method/Results/Conclusion structure + per-paragraph jobs + material source) |
| `references/neighbor-contract.md` | Whenever reading figure-warehouse files (field mapping, contract-gap handling, decoupling self-check) |

## Privacy

Don't disclose private paths, private filenames, or unpublished manuscript content in user-facing replies, generated prose, figure-reading files, or commit messages. Use generic descriptions ("the provided data file"). Reveal exact paths only when the human asks for an audit trail.

## Decoupling self-check (run after any change to this skill)

```bash
grep -rn "from sci-draw\|import sci-draw\|sci_draw\." skills/sci-write/   # must be empty
grep -rni "nature-writing\|nature_writing" skills/sci-write/             # must be empty
```
Any `import <other-skill>`, or logic assuming another skill must be co-present, is a coupling leak. Borrowing `profile_data.py` as a side-effect-free tool is allowed; depending on its presence is not (Step 0 falls back to asking the human).
