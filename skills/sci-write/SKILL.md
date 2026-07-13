---
name: sci-write
description: >-
  Data-driven academic manuscript writing for the data-to-conclusion pipeline. Use when the user
  has finished data analysis (or raw data + a research question) and wants to turn figures + findings
  into publication prose: Method, Results, Discussion, Conclusion. Drafts section by section from
  figure reports and a data profile, runs claim-vs-figure consistency checks via the paper-figure
  vision tool, and leaves real-DOI citation placeholders for the user to insert via Zotero/Endnote.
  Sits downstream of a figure-making skill (any tool, any source) and reads its on-disk reports;
  does not draw figures, does not do literature-first chapters (Introduction/Abstract/Keyword are
  marked external). Also trigger on: write results section, write discussion, draft from figures,
  数据写论文, 数据驱动写作, 把图画完写正文, 写结果/讨论/结论.
---

# sci-write — Data-to-Conclusion Manuscript Writing

Turn finished figures + data into publication prose, section by section. Every claim hangs on evidence (a figure, a statistic); every section serves a one-sentence argument.

This skill is the **writing** stage of the data→figure→prose pipeline. It does not draw figures, does not run peer review, does not write Introduction/Abstract/Keyword (those are `external`). It writes **Method, Results, Discussion, Conclusion** — the four data-driven sections whose material lives in your data profile and figure reports.

## Core philosophy (read before any step)

1. **On-disk files are the only coupling surface.** This skill reads neighbor directories' files. It does not import any other skill's code, does not assume any specific figure-making tool is present, and does not call other skills. Figures can come from anywhere — a figure skill, Excel/Origin/Illustrator, a screenshot, a copy-paste. As long as the files land in the agreed directory with the agreed schema, this skill works.

2. **Humans intervene at the key nodes.** No auto-research. The plan is drafted then confirmed by a human before落地. Figure status changes are proposed then confirmed. Claim corrections from figure-reading are suggestions a human approves. This skill proposes; the human decides.

3. **Read neighbors, don't orchestrate them.** This skill marks "fig1 status=pending" in paper-plan and stops. It never triggers a figure-making skill to run. The human sees the pending status and goes to draw the figure (in any tool, any session). When this skill restarts, it scans the neighbor directory and reports what's ready.

4. **Real-DOI placeholders, never fabricated citations.** Literature lookup happens inside this skill (via the user's search MCP), but the **final Zotero/Endnote insertion is always done by the human**. The skill leaves placeholders carrying real DOIs it found — never empty `[CITE:?]`, never invented bibliography entries.

5. **Contract gaps → human fills → becomes contract.** When a figure report is missing a field (no statistical methods, no n, claim not one sentence), this skill does not fabricate the missing data and does not skip the figure. It stops, lists the gap, asks the human to fill it. The filled content is written back and becomes part of that figure's contract.

_why_ These five rules are the difference between a writing assistant and an auto-research pipeline. Auto-research fabricates to keep moving; this skill stops and asks. It treats the human as the source of truth for anything that isn't already on disk, and treats on-disk files as the only stable handoff between sessions and between skills.

## If this isn't what you need

- **Draw/revise a figure from data** → use a figure-making skill (e.g. `sci-draw`) — this skill consumes figure reports, it does not produce figures.
- **Polish existing prose / edit / translate** → use a polishing skill — this skill drafts from evidence, it doesn't re-style finished text.
- **Introduction / Abstract / Keyword** → these are `external` to this skill. They need literature-first reasoning and global condensation; mark them in paper-plan and write them elsewhere, reading this skill's outputs as input.
- **Literature search / systematic review** → use a research skill — this skill consumes findings, it doesn't produce a bibliography.

## Workspace: the family namespace

All sci-* skills share one top-level family directory with a fixed, recognizable name — analogous to how `docs/superpowers/` marks that skill family's on-disk presence. This is a **family namespace, not a project namespace**: same name across every project, so anyone (human or skill) recognizing the layout knows immediately where things live.

```
<project-root>/
  manuscript/                  ← the official manuscript (first-class citizen, at project root)
    v1/                        ← original draft (tex project — user owns the form, not this skill)
      tex/ figures/ ref/
  sci-skills/
    sci-draw/                  ← the agreed "figure warehouse" directory.
                                 Figures land here regardless of source.
      fig1-report.md           ← figure report (6-section markdown contract)
      fig1.png                 ← exported preview
      fig1.pdf / fig1.py / ...
    sci-write/                 ← THIS skill's home — intermediate products only
      paper-plan.md            ← baton: figure list + section progress
      data-profile.json        ← data profile (this skill produces)
      fig1-reading.md          ← figure-reading consistency check (per figure)
      method.md                ← md DRAFTS of the four data-driven sections
      results.md                 (content carriers; form doesn't matter here)
      discussion.md              NOT the official manuscript — that's manuscript/.
      conclusion.md              Human moves content from here into manuscript/v1/tex/
                                 (or a future md→tex skill does).
```

**This skill does NOT touch `manuscript/`.** The md files in `sci-write/` are **content drafts**, not the official manuscript. The official manuscript is a first-class citizen at the project root (a LaTeX project the user owns, often arriving from outside). Moving content from these drafts into `manuscript/v1/tex/` is the human's job (or a future independent md→tex skill) — sci-write doesn't write to `manuscript/`, doesn't learn LaTeX project structure, stays a content producer.

From `sci-skills/sci-write/`, the figure warehouse is `../sci-draw/`. If the family root or warehouse directory differs, the human tells this skill where; `scan_neighbor.py` accepts an absolute path.

## File contracts (the only coupling surface)

| File | Produced by | Consumed by | Schema |
|---|---|---|---|
| `paper-plan.md` | this skill (after human confirms draft) | this skill (baton), human (progress) | figure entries + section status (below) |
| `data-profile.json` | this skill (Step 0, via `profile_data`) | this skill (Method); figure-makers may read or re-run | the `profile_data()` return dict as JSON |
| `../sci-draw/figN-report.md` | any figure-maker (out of scope here) | this skill (claim/findings/stats) | 6-section markdown (see neighbor-contract ref) |
| `../sci-draw/figN.png` | any figure-maker | this skill (Step 3, fed to paper-figure) | PNG image |
| `figN-reading.md` | this skill (Step 3) | this skill (Discussion/Results) | consistency-check schema (below) |

This skill **never writes** to `../sci-draw/` — that's the figure warehouse, owned by whatever produced it. Contract gaps are reported to the human; if the human permits a write-back to the report, fine, but default is read-only on the warehouse.

## Output format

**This skill produces md content drafts, always.** The official manuscript is `manuscript/v1/tex/` (a LaTeX project the human owns) — not produced here. md is chosen because: it's easy to diff across revisions, matches the contract files (paper-plan / figN-reading are md), and the form here doesn't matter (content is what counts; the human or a future md→tex skill reshapes it into LaTeX). Don't ask "md or tex" — the answer here is always md; tex is a different skill's concern.

## Workflow (Step 0–7)

Each step depends on the previous. Steps 1 and 3 have **human intervention points** — the skill stops and waits.

### Step 0 — Intake & data analysis

1. Receive raw data + research question.
2. Run a data profile. If `profile_data` (from a figure-making skill like sci-draw) is available, borrow it as a tool — it's a side-effect-free pure function, not a coupling:
   ```bash
   python -c "import json, sys; sys.path.insert(0,'../sci-draw/scripts'); from profile_data import profile_data; json.dump(profile_data('<data-file>'), open('data-profile.json','w'), ensure_ascii=False, indent=2)"
   ```
   If `profile_data` isn't available, ask the human for the key facts (N, per-group n, variable semantics, distribution shape) — don't fabricate.
3. Read the profile and make a **scientific judgment**: what claims can this data support, how many figures are warranted, what does each figure argue.

_why_ The profile is the fact layer; the claim list is the judgment layer. Same data can argue many things — the human-facing claim list (Step 1) is where the scientific argument gets pinned down, not the data itself.

### Step 1 — Draft paper-plan (**human intervention point 1**)

1. Based on the profile, draft a figure list. Each figure entry reuses the figure-report field names so plan→report is "same schema, pending→done":
   ```
   ## Figure fig1
   - topic: <one-line theme>
   - claim: <what this figure will argue>     # ↔ report "Core conclusion"
   - data-source: <file or description>        # ↔ report "Data source"
   - suggested-chart: <recommended chart type> # ↔ report "Chart type"
   - status: pending
   - report-ref:                                # filled when drawn
   ```
   Plus a `## Sections` block marking the four sections `pending` and Introduction/Abstract/Keyword as `external`.
2. **Stop and show the human.** Ask them to confirm or edit the figure list (which claims, how many figures, which data each uses).
3. **After confirmation**, write `paper-plan.md`.
4. Prompt: "Figures 1–N are pending. Go draw them — any tool, any session. Come back when done. I will not auto-trigger drawing."

_why_ The whole downstream rests on this claim list. A wrong claim here wastes every subsequent step. Stopping for confirmation is the cheapest moment to catch a wrong premise — far cheaper than discovering it in drafted prose.

### Step 2 — Sense the neighbor (on every start / resume)

1. Run `scripts/scan_neighbor.py` — scans `../sci-draw/*-report.md`, compares to `paper-plan.md`, reports each figure's status (plan status vs report existence, discrepancies, unclaimed reports).
2. Report to the human: "fig1 ready (report exists), suggest status→drawn; fig2 still pending."
3. **Human confirms** before any status change is written to paper-plan. Sensing is automatic; writing the plan is human-gated.

_why_ Across sessions, the human may forget which figures are done. Auto-sensing the warehouse (a read) is convenient and doesn't violate "don't orchestrate" — sensing ≠ calling. But auto-changing the plan would slide toward auto-research; the human stays the gatekeeper of the baton.

### Step 3 — Figure-reading consistency check (**human intervention point 2**)

For each figure with a ready report:

1. Read `../sci-draw/figN-report.md` → get `Core conclusion` (the claim). **If the claim is missing or not one sentence, apply contract-gap handling** (below) — ask the human, don't fabricate.
2. Call the `paper-figure` vision action (PRO / high effort — this is high-leverage, never use lite) on `../sci-draw/figN.png`. It returns a publication-ready academic description from a reader's perspective — crucially, it does **not** read the claim text, so its description is an independent reader view.
3. This skill compares: description vs claim. Where do they agree? Where might a reader misread (overlapping error bands, a divergent series, an axis that starts non-zero)?
4. Write `figN-reading.md` (schema below) with the comparison and a **soft** claim-correction suggestion.
5. **Stop and ask the human**: "Figure-reading found [discrepancy] between your claim and what the figure conveys. Suggest [narrow claim / re-draw / add a qualifier]. Which?" The human decides; this skill doesn't silently rewrite the claim.

_why_ A typeset-perfect figure can still mislead at the argument level — claim says "A beats B" but the bands overlap so a reader sees "comparable." Catching this before drafting Results/Discussion prevents building prose on a claim readers won't accept. The vision tool's independence from the claim text is what makes the check honest.

### Step 4 — Write Results

1. Read each `figN-report.md` (claim / findings / stats) and `figN-reading.md` (corrected claim — the reading's corrected version wins if there's a correction).
2. Draft by evidence ladder: system validation → main result → baseline → ablation → stress test. Not every paper has all rungs; order by each figure's evidence role.
3. Every claim hangs on evidence (figure + statistic). Calibrate verbs to evidence strength (`show`/`demonstrate` for direct main results, `suggest`/`indicate` for trends, leave `may`/`could` for Discussion).
4. Run the **confirmation gate** (writing-discipline ref) before full prose: echo the one-sentence argument + key terms + assumptions, get human confirmation.
5. Write `results.md` — a **content draft** in `sci-write/`. This is not the official manuscript; the human moves it into `manuscript/v1/tex/` later. So: optimize for content (claims + evidence), don't fuss over LaTeX form here.

_why_ Results is the spine — every other section refers back to it. Drafting it from the figure reports (not from memory, not from a vague sense of "what we found") keeps the prose tethered to evidence. The reading's corrected claim wins because arguing against your own figure is a losing position.

### Step 5 — Write Discussion

1. Extract mechanism / significance / literature comparison / limitations from the findings.
2. Keep observation (Results syntax: `was detected`, `increased`) separate from interpretation (Discussion syntax: `may reflect`, `suggests`). Don't mix.
3. **Literature comparison: run the search MCP, get real DOIs, leave real-DOI placeholders.** Never empty placeholders, never fabricated entries. The human inserts the final Zotero/Endnote citation.
4. Run the confirmation gate; write `discussion.md` (content draft in `sci-write/`).

_why_ Discussion is where papers get rejected for overclaiming or for unsupported mechanisms. The verb discipline (weak verbs for mechanisms) and the real-DOI rule (no invented literature) are the two guards. Marking the literature-comparison honestly — including conflicts with prior work — is what makes it a Discussion and not a sales pitch.

### Step 6 — Write Method + Conclusion

**Method** (pure factual statement, no literature search):
- Data description from `data-profile.json` (N, per-group n, variables, missingness).
- Statistical methods **copied verbatim** from each `figN-report.md`'s `Statistical methods` section — do not paraphrase, round, or "improve." If a field is missing, contract-gap handling.
- Write `method.md` (content draft in `sci-write/`).

**Conclusion** (short, from findings):
- Contribution + one-line evidence + one-line limitation + one-line bounded impact. No new data, no new citations, no mechanisms not already in Discussion.
- Write `conclusion.md` (content draft in `sci-write/`).

_why_ Method's verbatim-copy rule: statistics are facts, prose is narrative — never let narrative instinct alter a number or a test name. Conclusion's "no new anything" rule: it's a capstone, not a fresh argument.

### Step 7 — External handoff (no orchestration)

1. Mark Introduction / Abstract / Keyword as `external` in paper-plan. Do not write them.
2. Tell the human where things stand and what's next — two handoffs, neither orchestrated by this skill:
   - **Content → manuscript**: "Method/Results/Discussion/Conclusion md drafts are at `sci-skills/sci-write/`. These are **content drafts**, not the official manuscript. Move the content into `manuscript/v1/tex/` (or use a future md→tex skill) when ready — that's your call, this skill doesn't touch `manuscript/`."
   - **External chapters**: "Introduction/Abstract/Keyword need literature-first reasoning — start them in a research-oriented skill, reading `sci-skills/sci-write/` + `manuscript/` as input."
3. Update paper-plan section statuses to `written` for the four done sections.

_why_ Those three chapters are written last in practice (you frame the contribution after you know what the contribution actually is — "draw the target after the arrow lands"). They also lean heavily on literature positioning, which is a different mode of work than data-driven drafting. Marking them external keeps this skill honest about its scope.

## Pervasive writing discipline (applies to Steps 4–6)

Not a separate step — runs around every section draft. Full detail in `references/writing-discipline.md`:

- **Confirmation gate** before each section's full prose.
- **Targeted revision** — change only what the human flags, never silent full rewrites.
- **Verb calibration** to evidence strength.
- **Claim must hang on evidence** — else `[evidence needed]` placeholder, not a fabricated claim.
- **Sweep unsupported novelty/universal claims** (`first`, `unprecedented`, `always`).
- **Citation placeholder protocol** — real DOIs, human does final insertion.

## Contract-gap handling (when a figure report doesn't satisfy the contract)

When Step 2/3/4/6 reads a report and finds a missing or malformed field (no `Statistical methods`, empty `n`, claim written as a paragraph instead of one sentence):

1. **Do not fabricate** the missing content (no auto-filling "n=30, t-test").
2. **Do not skip** the figure or pretend it's unusable.
3. **Stop, list the gap explicitly**, ask the human to fill:
   > fig1-report.md is missing `Statistical methods`. Method/Results need this. Please fill: which test? correction? error bar SD/SEM/CI? n=?
4. **Write the filled content back** — to the report (if the human permits editing the warehouse) or to `figN-reading.md`'s "contract supplement" section. **The fill becomes contract**: from here on, that field is part of this figure's agreement; downstream steps use it as canonical.

_why_ This skill is the contract's enforcer and gap-finder, not its fabricator. The contract grows through real collaboration (gap noticed → human fills → it sticks), which is exactly how a trustworthy on-disk record gets built — as opposed to an auto-filled one whose contents no one ever verified.

## Scan neighbor script

```bash
python scripts/scan_neighbor.py                  # default: looks for ../sci-draw/
python scripts/scan_neighbor.py /abs/sci-skills  # absolute path, for testing
```

Pure stdlib, read-only, idempotent. Prints a human-readable status table + JSON. Never modifies paper-plan. See `references/neighbor-contract.md` for the full contract and `scripts/scan_neighbor.py` for the implementation.

## Reference index (load on demand)

| File | When to open |
|---|---|
| `references/writing-discipline.md` | Before drafting any section (confirmation gate, verb calibration, citation protocol, output format) |
| `references/figure-reading.md` | At Step 3 (paper-figure call flow, figN-reading schema, claim-correction handling) |
| `references/section-templates.md` | At Steps 4–6 (Method/Results/Discussion/Conclusion structure + per-paragraph jobs + material source) |
| `references/neighbor-contract.md` | Whenever reading figure warehouse files (field mapping, contract-gap handling, decoupling self-check) |

## Privacy

Do not disclose private local paths, private filenames, unpublished manuscript content, or provenance of private working materials in user-facing replies, generated prose, figure-reading files, or commit messages. Use generic descriptions ("the provided data file"). Reveal exact paths only when the human explicitly asks for an audit trail.

## Decoupling self-check (run after any change to this skill)

```bash
# Zero import of any figure-making skill's internals
grep -rn "from sci-draw\|import sci-draw\|sci_draw\." skills/sci-write/
# Every mention of the figure warehouse should be a file path reference, not a code dependency
grep -rn "sci-draw" skills/sci-write/
# Zero mention of nature-writing or any other writing skill (this skill is self-contained)
grep -rni "nature-writing\|nature_writing" skills/sci-write/
```

If any `import <other-skill>` appears, or logic that assumes another skill must be co-present to function, that's a coupling leak — fix it. Borrowing `profile_data.py` as a side-effect-free tool is allowed; depending on it being present is not (Step 0 falls back to asking the human).
