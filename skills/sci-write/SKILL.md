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
      claim.md                   ← canonical claim (Step 0 — the paper's one-sentence argument)
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
| `claim.md` | this skill (Step 0, after human confirms) | this skill, narrative drafting, submission stage | one-sentence claim + evidence baseline (see Step 0) |
| `paper-plan.md` | this skill (after human confirms) | this skill (baton), human | fig entries + section status (Step 1) |
| `data-profile.json` | this skill (Step 0, via `profile_data`) | this skill (Method) | `profile_data()` return dict as JSON |
| `../sci-draw/figN-report.md` | any figure-maker | this skill (claim/findings/stats) | 6-section markdown (see neighbor-contract ref) |
| `../sci-draw/figN.png` | any figure-maker | this skill (Step 3 → an image-understanding capability) | PNG |
| `figN-reading.md` | this skill (Step 3) | this skill (Results/Discussion) | consistency-check schema (Step 3) |

## Workflow

Steps run in order; each depends on the previous. **Steps 1 and 3 stop for human confirmation** — do not skip those gates.

### Step 0 — Establish the claim (human intervention point)

**This is the hard gate. Everything downstream serves this claim. If the claim is
wrong, every section is waste. If the claim isn't settled, don't draft.**

1. **Receive the human's rough idea.** What do they think the paper argues? One sentence,
   even if vague. "We think X causes Y" / "We built a better Z" / "Our data shows W."

2. **Profile the data.** What can the data actually support? Run `profile_data` (borrow
   from figure warehouse if available). If unavailable, ask the human for key facts
   (N, per-group n, variable semantics, distribution shape). Don't fabricate.

3. **Search the literature.** What claims do comparable papers make? At what journal tier?
   What's the state of the art? This calibrates ambition — you can't claim "first ever"
   if three Nature papers did it last year. Use academic search tools or fall back to
   general search.

4. **Calibrate claim vs. data.** Three outcomes:

   | Data vs. claim | Action |
   |---|---|
   | Data supports the claim | → Write `claim.md`, proceed to Step 1 |
   | Data **doesn't** support | → **Hard stop.** Tell the human: "The data can't support this claim. Options: (a) collect more data, (b) lower the target." Loop until resolved. |
   | Data supports **more** than the claim | → Tell the human: "The data can support a stronger claim. Upgrade?" Human decides. |

   Doing nothing = the paper has no argument = don't write.

5. **Write `claim.md`** after human confirms:

   ```markdown
   # Claim

   **One-sentence argument:**
   In [system/problem], we show [advance] using [approach],
   supported by [evidence], with [boundary].

   **Gap we fill:**
   [One sentence. What didn't exist before, and why not.]

   **Evidence baseline:**
   - [Evidence 1 — figure or statistical support]
   - [Evidence 2]
   - ...

   **Boundary:**
   [Where the claim stops. What this paper does NOT establish.]

   **Journal ambition:**
   [tier estimate based on literature calibration — e.g. "Nature Communications level" / "field top-tier" / "solid specialist journal"]
   ```

   This file is the contract. Figure claims in paper-plan are sub-claims of this
   one-sentence argument. Narrative drafting reads it. Submission reads it for
   journal tier. If the data changes, update this file first.

### Step 1 — Draft paper-plan (human intervention point)

1. Read `claim.md`. Each figure must serve the main claim. Drop any figure that doesn't.

2. Draft a figure list. Each entry has two layers:

   ```
   ## Figure fig1
   - section: <method / results>
   - conclusion: <what this figure itself shows>
   - claim: <how this supports claim.md>
   - data-source: <file or description>
   - status: pending
   - report-ref:
   ```

   `conclusion` 是图自己的答案。`claim` 是"so what"——这个结论对一句论证的支撑。

   **Method 部分和 Results 部分的图，claim 的难度不一样：**

   ```
   Results 图：conclusion 天然就有 → 重点是 claim（对 claim.md 的解释）
             数据跑出来是什么、结论就是什么。
             难在"这个结论怎么支撑整篇论文的论证"——这是解释工作。

   Method 图：  conclusion → claim（先想清楚 conclusion 才有资格谈 claim）
             方法图的 conclusion 不好想——"这张方法图证明了什么？"
             想清楚了 conclusion + claim，这张图才有存在的必要。
             列不出来 → 方法二段文字说清就够了，不需要图。
   ```

   **Method 图自检——更严格：**
   ```
   conclusion: [这张方法图证明了什么？]
        claim: [这个结论怎么支持 claim.md？]
   两个都列不出来 → 砍。只列得出 conclusion 列不出 claim → 砍。
   两个都列得出 → 留。这是 method 图存在的硬门。
   ```

3. **Self-check — 所有图（在给人看之前先跑）：**

   ```
   fig1 [results] conclusion: [数据说了什么]
                  claim: [支撑 claim.md 的哪一步？]
   fig2 [method]  conclusion: [这张方法图证明了什么？]
                  claim: [—]  ← 列不出来 → 砍
   ```

   两张图的 conclusion 相同？→ 合并或砍一张。列不出 claim？→ 砍。
   列得出来但牵强？→ Supplementary。

4. Add a `## Sections` block.

5. **Stop. Show the human.**

### Step 2 — Sense the neighbor (every start / resume)

```bash
python scripts/scan_neighbor.py                  # scans ../sci-draw/*-report.md, compares to paper-plan
python scripts/scan_neighbor.py /abs/sci-skills  # absolute path for testing
```

Reports each figure's status (plan status vs report existence, discrepancies). Propose status changes; the human confirms before anything is written to paper-plan. Sensing is automatic (a read); writing the plan is human-gated.

### Step 3 — Figure-reading consistency check (human intervention point)

**This step verifies the `conclusion` — does the figure actually show what it claims to show?**
`claim` (how this conclusion supports the paper's argument) is connected in Step 4 when writing prose.

For each figure with a ready report:

1. Read `../sci-draw/figN-report.md` → `Core conclusion`. This is what sci-draw proved with this figure. Missing or not one sentence → contract-gap handling.
2. Use an **image-understanding capability** on `../sci-draw/figN.png`, with an audit prompt asking for an independent reader view. **Do not pass the conclusion** — independence is what makes the check honest.
3. Compare: does the figure actually convey the stated conclusion? Where might a reader misread (overlapping error bands, divergent series, non-zero axis start)?
4. Write `figN-reading.md`:
   ```markdown
   # Figure figN — conclusion check
   ## conclusion (from report)
   <figN-report Core conclusion>
   ## figure conveys (independent reader view)
   <vision description>
   ## consistency
   - agree: ...
   - misread risk: ...  (tie to specific visual feature)
   ## conclusion correction
   <narrow / re-draw / add qualifier — human decides>
   ```
5. **Stop. Ask the human.** "Figure-reading found [finding]. Also — as an experienced researcher: does this conclusion hold up? Statistical method right? Would a colleague with different background interpret this differently?" See `references/writing-discipline.md` → 人类判断检查点.

A figure whose conclusion and visual don't match will mislead every reader — catch it here, before prose is built on a false premise. Technical verification catches visual misreads; only the human catches academic judgment errors.

### Step 4 — Write Results

1. Read `claim.md`. Then read each `figN-report.md` (conclusion/findings/stats) +
   `figN-reading.md` (corrected conclusion wins). **Sort figures by their role
   in the claim, not by convention.**

2. Map each figure to how it builds toward the one-sentence argument:

   ```
   claim.md: In [system], we show [advance] using [approach], supported by [evidence].

   fig1 (system validation): proves the platform/method works at all       → 1st rung
   fig2 (main result):     the headliner — which rung of the claim?         → anchor
   fig3 (baseline):        proves this isn't trivially achievable otherwise → stakes
   fig4 (mechanism):        proves it's not a fluke — why it works           → depth
   fig5 (stress test):     proves it doesn't break under [conditions]       → boundary
   ```

   Drop any figure whose role in the claim can't be stated in one sentence.
   Not every paper has all rungs — but every figure that stays has to earn its place.

3. Draft paragraph by paragraph. Each paragraph:

   ```
   [Topic sentence: what this figure's conclusion means for the claim]
   We observed [specific data/phenomenon, citing figN + statistic].
   [Context/comparison detail].
   This supports the claim by [specific role in the one-sentence argument].
   Fig N, [panel].
   ```

   The topic sentence is not "we observed X" — that's for the detail line.
   The topic sentence is "X was Y" — the conclusion the figure defends.

4. **Calibrate verbs to evidence strength** (`show`/`demonstrate` for direct main
   results, `suggest`/`indicate` for trends). Never put `may`/`could` in Results —
   those are Discussion verbs.

5. Run the **confirmation gate**: echo the claim → each figure's role → each
   paragraph's topic sentence as a chain. Get human confirmation. Write `results.md`.

### Step 5 — Write Method + Conclusion

**Method** — make the claim credible by showing HOW we know.

Load `references/section-templates.md` → Method. Every Method sub-section answers three questions:
1. **Motivation** — why does the reader need to know this to trust the claim?
2. **Mechanism** — what we actually did (enough to reproduce).
3. **Role in claim** — where does this connect to the claim and which figure shows the result?

If a paragraph can't answer Role in claim → it doesn't belong in Method.

**Methods paper vs. non-methods paper:**
- Non-methods paper: Method is support. Keep it lean — enough to reproduce, no more.
- Methods paper: Method IS part of the claim. Every design choice needs motivation + advantage over alternatives.

**Data sources:**
- Data description from `data-profile.json` (N, per-group n, variables, missingness).
- Statistical methods **copied verbatim** from each `figN-report.md` `Statistical methods` — don't paraphrase, round, or "improve." Missing field → contract-gap handling.
- Don't fabricate "standard practices" citations. If a method needs a reference, use Real-DOI placeholders.
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



