---
name: sci-story
description: >-
  Narrative academic writing — draft Introduction, Discussion, Abstract,
  and Keywords from completed Results and figure reports. Anchored to the
  four-question spine and Introduction-Discussion coherence. Writes tex sections
  directly into manuscript/vN/tex/sections/ (intro.tex, discussion.tex,
  abstract.tex). 写引言、写讨论、写摘要、write introduction, write discussion,
  write abstract. Does not do data-driven Method/Results/Conclusion, does not
  polish prose, does not draw figures, does not produce SI.
---

# sci-story

Write Introduction / Discussion / Abstract / Keywords from completed Results and
the figure warehouse. Every section serves the four-question spine;
Introduction and Discussion are coherent by construction — they're drafted together
with the same spine, not independently. Output is **tex sections written directly
into `manuscript/vN/tex/sections/`** — no md intermediate, no copy step.

## Layout & boundaries

```
<project-root>/
  manuscript/vN/tex/sections/     ← THIS skill writes here: intro.tex, discussion.tex, abstract.tex
  sci-skills/
    sci-draw/                     ← figure warehouse — READ-ONLY: figN-report.md
    sci-write/                    ← READ working notes here
      claim.md                    ← READ: canonical claim (one-sentence argument + gap + evidence)
      paper-plan.md                ← READ: figure list + section progress
      figN-reading.md              ← READ: figure claim corrections
      terminology-ledger.md        ← READ + WRITE (co-owned with sci-write + sci-polish)
  manuscript/vN/tex/sections/
    results.tex                   ← READ: completed Results (evidence baseline for Discussion)
    method.tex                    ← READ: data/sample context for Introduction
    conclusion.tex                ← READ: contribution statement (fused into Discussion)
```

- **Writes tex directly into `manuscript/vN/tex/sections/`.** Introduction/Discussion/Abstract are manuscript sections, written as tex from the start — no md draft, no later move.
- **Reads sci-write's product tex** (`results.tex`, `method.tex`, `conclusion.tex`) plus working notes (`claim.md`, `paper-plan.md`, `figN-reading.md`) from `sci-skills/sci-write/`.
- **Does NOT write to `../sci-draw/`.** Read-only on the figure warehouse.
- **Does NOT produce SI.** SI is sci-write's by-product (results/method overflow). Narrative sections don't carry supplementary material.
- **Reads from disk; never imports code.**

## File contracts

Working notes (read from `sci-skills/sci-write/`):

| File | Produced by | Read by | Schema |
|---|---|---|---|
| `claim.md` | sci-write (Step 0) | this skill, submission stage | one-sentence argument + gap + evidence baseline |
| `paper-plan.md` | sci-write | this skill | fig entries + section status |
| `figN-reading.md` | sci-write (Step 3) | this skill | corrected claim (wins over report) |
| `terminology-ledger.md` | sci-write + sci-polish + this skill | all three | canonical term forms |

Product tex (read from `manuscript/vN/tex/sections/`):

| File | Produced by | Read by |
|---|---|---|
| `results.tex` | sci-write (Step 4) | this skill (evidence baseline for Discussion) |
| `method.tex` | sci-write (Step 5) | this skill (data/sample context for Introduction) |
| `conclusion.tex` | sci-write (Step 5) | this skill (fused into Discussion first paragraph) |

Read-only neighbor:

| File | Source | Read for |
|---|---|---|
| `../sci-draw/figN-report.md` | any figure-maker | Core conclusion, Key findings |

Product tex (written by this skill into `manuscript/vN/tex/sections/`):

| File | Produced by | Read by |
|---|---|---|
| `intro.tex` | this skill (Step 3) | sci-polish, sci-submit |
| `discussion.tex` | this skill (Step 2) | sci-polish, sci-submit |
| `abstract.tex` | this skill (Step 4) | sci-polish, sci-submit |
| `title.tex` | this skill (Step 5) | sci-typeset, sci-submit |
| `keywords.tex` | this skill (Step 6) | sci-submit |

## Startup

Every session starts here:

1. **Locate the manuscript and working notes.** Check `manuscript/vN/tex/sections/`
   for `results.tex` — narrative sections are drafted AFTER completed Results exist.
   If `results.tex` isn't there yet, tell the user: "Results need to be drafted first
   (sci-write produces `results.tex`). Draft the results, then come back." Also
   confirm `sci-skills/sci-write/` exists for working notes (`claim.md`, `paper-plan.md`).

2. **Read the neighbors** (skip any that don't exist; flag missing but don't block):

   From `manuscript/vN/tex/sections/` (sci-write's product tex):
   - `results.tex` — completed Results (the evidence baseline Discussion interprets)
   - `method.tex` — data/sample context for Introduction background
   - `conclusion.tex` — the contribution statement (fused into Discussion's first paragraph)

   From `sci-skills/sci-write/` (working notes):
   - `claim.md` — canonical claim
   - `paper-plan.md` — figure claims, section status
   - `figN-reading.md` — claim corrections (corrected claim wins over report)

   From `../sci-draw/` (*figure warehouse* — read regardless of source):
   - `figN-report.md` — `Core conclusion`, `Key findings`, `Statistical methods`.
     These are the evidence ground truth.

3. **Load or build the terminology ledger.**

   If `terminology-ledger.md` exists → read it, enforce it. Extend with new terms.

   If it doesn't exist → build from figure reports + writing drafts + manuscript
   text. Write to `sci-skills/sci-write/terminology-ledger.md`. Mark new entries
   with source `sci-story`.

## Workflow

### Step 0 — Gather axes + backward reasoning

1. **Paper type** — research / methods / hypothesis / algorithmic / review.
   Default: research.
2. **Target journal** — nature / nat-comms / generic. Default: generic. Affects
   word limits and format, NOT writing quality. Top-journal standards apply
   regardless of target.
3. **Read all neighbor files** — `results.tex`, `conclusion.tex`, `method.tex`
   (from `manuscript/vN/tex/sections/`); `figN-report.md`, `figN-reading.md`,
   `paper-plan.md`, `claim.md` (from working notes). Build the evidence baseline.
4. **Backward reasoning first** (before writing anything):
   - What technical problem do we solve, and why is there no well-established solution?
   - What are the contributions, and what new insight do they bring?
   - How do we use prior methods to lead readers to our challenge and insight?

State axes in one short line before proceeding.

### Step 1 — Read the claim (human intervention point)

**Claim is established upstream, not here.** Read `claim.md` — it was produced
by the data-driven drafting stage (Step 0) and confirmed by the human.
It carries:

- One-sentence argument
- The gap the paper fills (and why no one filled it before)
- Evidence baseline
- Boundary
- Journal ambition estimate

Read it. Trust it. If `claim.md` doesn't exist — stop. Tell the user: "The
claim hasn't been established yet. Run the data-driven drafting stage first —
it profiles the data, searches the literature, and calibrates what the data
can actually support. Come back with `claim.md`."

**Gap 不能多。** "他用了 scikit-learn，你用了 XGBoost"不算 gap。"他用了 XGBoost，
你提了一个新算法"才算。不是所有差异都是 gap——`claim.md` 里已经做了这个筛选。

**Stop. Show the human.** "This is the paper's argument from `claim.md`. Still
right?" If the human changes it, update `claim.md` before proceeding.

### Step 2 — Draft Discussion

Discussion anchors interpretation. Write it first so Introduction knows exactly
what narrative arc it must set up.

**First paragraph: read `conclusion.tex` and fuse it in.** sci-write already wrote
the Conclusion — contribution statement + decisive evidence + boundary. Don't
rewrite it. Take it as-is, merge it as the first paragraph of Discussion. This
is the common denominator across almost all journals.

Load `references/discussion-guide.md`. Structure after the fused Conclusion:

1. **Conclusion (from sci-write)** — contribution statement + decisive evidence + boundary. As-is, don't rewrite, don't expand, don't turn into interpretation.
2. **Opening** — "Our results show [contribution]. This means [interpretation]."
3. **Mechanism** — why this result? Plausible mechanism, hedged. Address rival explanations.
4. **Literature comparison** — align/contrast with prior work. Real-DOI placeholders.
5. **Limitations** — evidence boundaries. Specific, not generic.
6. **Implications** — bounded significance statement.

Before writing full prose, run the **confirmation gate**: echo the fused Conclusion
+ Discussion's one-paragraph argument + key interpretations. Get human confirmation.
Write `manuscript/vN/tex/sections/discussion.tex`.

### Step 3 — Draft Introduction

Load `references/introduction-guide.md` and `references/literature-search.md`.
Also load `references/top-journal-conventions.md` → Introduction: hook forms,
gap signal words, explicit "why this system", contribution sentence patterns.

Introduction is a **two-stage funnel**, not a single five-layer:

**Stage 1 — Domain-level** ("why this direction matters"):
1. 大背景 (1-2 sentences, ≥3 independent citation sources from different angles)
2. 小背景 + 现状 (funnel narrowing from one concrete number to the core concept)
3. Prior work (woven into narrative, each claim has a source)
4. Gap (断层 not 空白 — structural mismatch, not literature gap)
5. 跳板 (natural transition, not a summary)

**Stage 2 — Research-level** ("what's missing + what we did"):
1. 转折 ("In contrast, ML/DL..." — pivot, not conclusion)
2. 小背景 + 现状 (specific problems, clustered by issue)
3. Prior work (clustered by problem, not chronological. Same paper can appear under multiple problems.)
4. Gap (narrower than Stage 1 — what current approaches specifically fail at)
5. Present study (framework-level preview, not mini-Methods)

**Before writing:** search literature per `literature-search.md` — check for academic
MCP tools, fall back to general search. Verify journal quality if possible. Real-DOI
placeholders for all citations.

**Introduction-Discussion coherence check (mandatory):** for every gap/bottleneck in
the Introduction outline, confirm Discussion has a corresponding response. If mismatch,
fix before drafting.

Run the confirmation gate (spine + gap statements + coherence check). Get human
confirmation. Write `manuscript/vN/tex/sections/intro.tex`.

### Step 4 — Draft Abstract

Load `references/abstract-guide.md` and `references/top-journal-conventions.md` →
Abstract: five moves, `However` gap hinge, one hard number, bounded significance.
Abstract is a mini-paper, written last when Discussion and Introduction are stable.

1. Compress the spine into one tight paragraph.
2. Choose template variant (A/B/C) based on the paper's argument structure.
3. No new content — everything must already appear in Introduction, Results,
   or Discussion.

Run the confirmation gate: echo the compressed spine. Get human confirmation.

Write `manuscript/vN/tex/sections/abstract.tex`.

### Step 5 — Title

**Title is the shortest version of the claim.** Abstract compresses the paper;
the title compresses the claim. Read `claim.md` — the title must align with
the one-sentence argument, not drift from it.

Load `references/top-journal-conventions.md` → Title. **Title is the last
thing you finalize.** Abstract and Discussion are stable, now name it.

Pick one of four shapes based on what the claim IS:
1. **Method-led noun phrase** — the claim is a method
2. **Declarative finding** — the claim is a discovery
3. **`System: function` colon form** — the claim is a tool
4. **Gerund/question** — benchmark/Perspective only

Generate 3-5 candidates. Mark the most defensible one.

**Hard rules:**
- No numbers or results — those go in the Abstract.
- One evaluative adjective max: *robust, generalizable, data-driven.* Not *novel, advanced, powerful.*
- Searchable: would a researcher typing keywords find this title?
- Defensible: every word must be backed by data in the manuscript.
- Not grant-style (*Toward...*, *A study of...*) or overbroad (*A new era of...*).

**Self-check:** Title ↔ claim.md — same argument? Title ↔ Abstract —
title more conservative than Abstract → good, more exaggerated → rewrite.

Write to `manuscript/vN/tex/sections/title.tex` (a `\title{...}` line; the human
or sci-typeset wires it into `main.tex`'s preamble). Mark the chosen candidate
in a comment.

### Step 6 — Keywords

From the abstract and title, extract 5-8 keywords. Rules:
- Distinct from title words — keywords are supplementary, not a copy
- Use established field terminology
- No abbreviations unless universally recognized
- Semicolon-separated, sentence case

Write to `manuscript/vN/tex/sections/keywords.tex` (a `\keywords{...}` line,
or whatever the template's keyword macro expects).

### Step 7 — Self-checks

Run both checks before showing the human. Fix issues, don't just flag.

**Check 1 — 故事主线。** 抛开骨架（五层漏斗、六段结构），这篇论文到底讲了一个什么故事？

用最直白的话写出来：
```
背景：[……]下，[……]成了瓶颈。
前人：有人做了[……]、[……]、[……]。
但他们都卡在：[……]。
我们：[……]。
结果我们发现了：[……]。
这意味着：[……]，但限于[……]。
```

如果这段白话文自己读着不对——某个环节断了、逻辑跳了、gap 跟 contribution 对不上——那就是结构有问题。回头修结构，不要修措辞。

**Check 2 — Gap-fill 对齐。** 把 Introduction 里提到的每个 gap 和 bottleneck 列出来，逐条对 Discussion 和 Present study：

```
Intro 提了 gap/bottleneck         →   Discussion/Present study 填了吗？
  "数据与设计脱节"                 →   填了：框架输出设计指导
  "材料表征不足（one-hot）"        →   填了：元素质量分数编码
  "黑箱不可解释"                  →   填了：注意力可视化 + 流形学习
  "不能蒸馏可复用洞见"            →   填了：physicochemical similarity map
```

两条铁律：
- Intro 提了但没填的 gap → 砍掉，或者补 Discussion。
- Discussion 里出现但 Intro 没提的东西 → 要么 Intro 补一句，要么 Discussion 里砍掉。

**修完自检之后**再进 Step 8（Human review）。

### Step 8 — Human review

**Mandatory. Do not skip.**

Show changes with `git diff` across `manuscript/vN/tex/sections/` (the tex this
skill wrote) and `sci-skills/sci-write/terminology-ledger.md`.

Ask explicitly: "Do intro/discussion/abstract look right? Any coherence issues?"

The author owns the argument. Revisions are targeted, not full rewrites.

### Step 9 — Commit

After the human approves:

```bash
git add manuscript/vN/tex/sections/intro.tex \
        manuscript/vN/tex/sections/discussion.tex \
        manuscript/vN/tex/sections/abstract.tex \
        manuscript/vN/tex/sections/title.tex \
        manuscript/vN/tex/sections/keywords.tex \
        sci-skills/sci-write/terminology-ledger.md
git commit -m "story(intro,discussion,abstract): <one-line spine>

- Introduction: funnel from [field stake] to gap [gap]
- Discussion: interprets [main finding], addresses [rival], limited by [boundary]
- Abstract: mini-paper, compressed spine
- Terminology ledger: [new/updated entries if any]"
```

Update `paper-plan.md`: set Introduction, Discussion, Abstract, Keywords to
`story-drafted`.

## Pervasive discipline (Steps 2-4)

Runs around every section draft. Detail in `references/writing-discipline.md`:

- **Four-question spine first.** Every section serves the spine. Can't write the
  spine → don't draft.
- **Confirmation gate** before each section's full prose.
- **Introduction-Discussion coherence.** Intro gap → Discussion must respond.
  Run the consistency check after every Intro draft.
- **Targeted revision** — change only what the human flags, never full rewrite.
- **Verb calibration** — Introduction states contributions with strong verbs
  (we showed/demonstrated); Discussion interprets with weaker verbs (may reflect,
  suggests). Mechanism speculation → weak verbs + boundary statement.
- **Real-DOI citation placeholders.** Search MCP → real DOI → placeholder.
  Human does final Zotero insertion.
- **Sweep unsupported novelty/universal claims.**

## Reference index

| File | Open when |
|---|---|
| `references/writing-discipline.md` | Before drafting any section — confirmation gate, coherence rules, verb calibration, citation protocol |
| `references/top-journal-conventions.md` | Before drafting Introduction and Abstract — hook forms, gap signals, sentence rhythms, tense, transition frequencies |
| `references/literature-search.md` | At Steps 2-3 (Discussion and Introduction) — academic search tool priority, journal quality, layer-by-layer citation requirements |
| `references/discussion-guide.md` | At Step 2 — default structure, coherence check, syntax, failure modes |
| `references/introduction-guide.md` | At Step 3 — funnel structure, paragraph jobs, drafting rules, Intro-Discussion lock chain |
| `references/abstract-guide.md` | At Step 4 — mini-paper structure, template variants, drafting discipline |

## Boundaries

| Need | Where |
|---|---|
| Write Method/Results/Conclusion from data | data-driven drafting — reports observations, not narrative |
| Polish/revise prose | prose polishing — edits manuscript tex directly |
| Create scientific figures | figure creation — produces plots and figure reports |
| Submit manuscript / cover letter | submission management |
| Full systematic lit review | This skill does targeted search for positioning and comparison; a different mode |
