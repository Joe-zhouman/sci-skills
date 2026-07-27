# sci-respond — design note

> **Status: design input, not implementation.** This file captures the design
> blueprint extracted from one real, public revision package
> (`assets/Response Letter#1.pdf`, Communications Engineering / Nature
> Communications family) plus the author's stated principles. The SKILL.md is
> **not** written yet. Do not implement against this until the design pass
> settles — but everything here is what the SKILL.md will be built from.
>
> Recorded 2026-07-26. Author principles quoted verbatim where possible.

## Sibling

`sci-revise` (manuscript revision — editing `manuscript/rN/tex/` per the
decisions locked here) is designed alongside. The two are **separate skills**:
response-letter writing and manuscript revision are temporally one-directional
(response strategy first, then revision), produce different artifacts (a
standalone tex document vs. edits to manuscript tex), and have different HITL
rhythms. Their coupling — every change promised in the response must land in the
manuscript — is handled by a shared revision-round state file under
`manuscript/rN/` — resolved to the shared `sci-skills/sci-revise/` directory;
see §7.2), not by merging them into one skill. This is the same argument D4 used
to fold SI into sci-write, run in reverse: SI and results are co-produced, so
they share a skill; response and revision are sequenced, so they stay separate.

---

## 0. Meta-rule — human-in-the-loop is the ceiling

> **实际上再精巧,也不如让人在某个阶段介入。**

Every automated mechanism in this skill — the state contract, the coverage
audit, the integrity firewall, the independent-reviewer rehearsal — is worth
less than handing the right decision back to the human at the right moment. The
skill's job is to **organize information and surface options**, then **stop**.
The decision is always the human's.

This rule grades every other mechanism in this note:

- **Keep** mechanisms that help a human decide better — presenting a complete
  issue ledger, offering 2–4 strategy options with tradeoffs, tagging AI
  inferences as `INF:`, showing a safe-claim-boundary.
- **Cut or demote** mechanisms that decide *for* the human — automatic priority
  scoring, auto-running experiment plans, end-to-end script pipelines that push
  the human out of the loop. These may appear as *suggestions* (clearly labeled),
  never as decisions.

The corollary: when a mechanism's cleverness and a clean human checkpoint
conflict, the checkpoint wins. A dumb pause at the right place beats a smart
pipeline that never stops.

### 0.1 Two decision classes — restraint is selective, not blanket

"克制" does **not** mean "give the user fewer options everywhere." It means
distinguishing two classes of decisions:

- **Class A — technical / implementation. The skill decides, does not ask.**
  These have an objectively better answer; the user often doesn't know the
  alternative exists. Pushing them to the user offloads technical
  responsibility — it is not respect, it is 甩锅.
  - **tex, not Word.** tex gives precise layout; Word cannot. The response is
    tex. If the user insists on Word, generate via pandoc and let the user fix
    what pandoc cannot place precisely. **不做保姆.**
  - template (bundled `reviewresponse.sty`), cover-page layout, font/spacing,
    Response-Figure non-floating, redline colors, macro choices, compile command,
    overview default-on.
- **Class B — domain judgment + risk. The user decides; the skill surfaces
  options and stops.** Only the user knows their claim's footing, time budget,
  advisor's demands, how much this journal matters.
  - defend / concede / run experiment / cite existing evidence — 2–4 strategy
    menu at the checkpoint.
  - claim narrowing vs. holding firm.
  - **how aggressively to frame** (reframe scope, minimize limitation, exploit
    misunderstanding) — risk-dependent, author's call (see §hard-rule-2 and
    writing-rules §framing-freedom).
  - ambiguous comment's intent — the skill asks (Intent Diagnosis Card).
  - whether this round is worth a heavy rebuttal — viability assessment.

**The skill decides Class A; the user decides Class B.** Most over-design
failures come from misclassifying Class A as Class B (asking the user about
things they shouldn't have to decide).

---

## 1. First principle

> **让审稿人不用回看手稿,也知道我改动了什么东西。你替别人考虑,别人就替你考虑。**
>
> Serve the reviewer as a reader who will only ever read this one Response
> document and will not flip back to the manuscript.

This is the design's load-bearing axiom. Every other rule derives from it.

### Three hard rules derived from it

1. **每条 response 必须自包含(self-contained)** — hard constraint, not
   best-effort. Every response — even a one-line typo fix — must carry enough
   evidence (figure / data / quoted original / location of the change) that the
   reviewer can judge it without opening the manuscript. **A response that sends
   the reviewer back to the manuscript is a failed response.** This is the skill's
   acceptance criterion, realized as a self-containment check (a gate, mirroring
   the intake-gate / safety-gate pattern in the rebuttal research).

2. **诚实是底线,不是目标——目标是中稿(Honesty is the floor, not the ceiling;
   the goal is acceptance).** 之前把这写成"诚实优先",是把它误当成最高写作
   原则。其实写 Response 的根本目的是中稿,不是展示诚实。诚实是不可越的**底线**
   (不编造数据/结果/引用、不篡改图表、不"没做说做了"),底线之上有一大片**合法
   框定自由度**(reframe claim 范围、强调有利证据、瑕疵转 SI、利用审稿人误解……)
   服务于中稿。这一层是 Response 写作的核心技艺,跟 xps 的"叙事旋钮"、sci-submit
   的"硬约束驱动中稿"同源。详见 writing-rules.md §framing-freedom(A–G 七类合法
   框定 + 红线)。原来的"诚实优先"措辞保留了它的合理内核——谎言难圆、坦诚有时
   是更强的框定("These predicted values are not experimentally validated" 照实写,
   因为它比辩护更有说服力)——但把它从道德要求降级为底线 + 一种可选策略。
   框定到什么程度是 Class B(作者的风险偏好,见 §0.1)。

3. **致谢克制 + 反 AI 痕迹** — two faces of one rule:
   - **致谢是噪声,不是礼貌。** 认真改稿就是最大的谢意——多余的感谢挤占审稿人
     认知带宽,违背第一性原则(让审稿人最快拿到信息)。**致谢的份量必须匹配
     response 的份量**:typo / 纯澄清类,**一句都不用写**或一句"Fixed, see
     line X"即可,禁止"thank you for your meticulous identification of the
     spelling errors"这种圆滑废话;重型回应(data-backed defense / concede)才
     配得上一句简短致谢,且点到为止。
   - **该出现的致谢也要反 AI 痕迹。** 真要写时,高频措辞必须变化,禁止 cadence
     重复和 rule-of-three。样本 20 条用了 ≥8 种不同致谢开头。与 `humanizer-zh`
     同源。
   - 一句话:**先问"这条要不要致谢",再问"怎么写得不重复"。** 多数 response 的
     答案是"不用"。

### Production format

- **tex → PDF, not docx.** The product is a LaTeX document built on the
  **bundled** `assets/response-template/` suite (`reviewresponse.sty`, copied
  into the skill's source so it is self-contained). Same direction as the
  family's D1 (write/story produce tex directly). The author is migrating from a
  Word→PDF workflow to tex→PDF for editability. Word via pandoc only on author
  insistence — and the author fixes what pandoc cannot place precisely (不做保姆).
- **Write directly in tex**, inside the reviewresponse environments — no markdown
  intermediate, no "draft in plain text then template-fill" two-step. Same
  principle as D1: writing and final format are the same language.

### Layout freedom (Response > manuscript)

Unlike manuscript prose (which must stay disciplined per journal convention), a
Response letter **may** use bold, lists, color, and inline references as visual
aids. All of these serve rule 1 (self-containment): the cheapest way to make a
reviewer see your point is to put it in front of them in the clearest form.
Color-coded change tracking, Response Figure/Table with independent numbering,
inline `[1]` local citations — these are tools, not decoration.

### Format-over-prose for typo / clarification responses

For typo and pure-clarification responses (the lightweight end of the strategy
taxonomy), **prefer structured format over prose paragraphs**. A one-line
clarification should not become a three-sentence paragraph with acknowledgements
— it should be the answer in its clearest form, full stop. This is the positive
face of "acknowledgement restraint": cut the noise (no thanks), then make the
signal maximally legible (format it).

- **Scope:** typo / clarification responses **only**. Heavy responses
  (data-backed defense, concede, partial disagree) still use full prose
  paragraphs, because they carry argument logic that format can't replace.
- **Concrete format — inline redline in a quote block** (confirmed from
  `assets/typo-format-1.png` + `typo-format-2.png`, both Q7). The original
  manuscript sentence is shown as a **block quote** (left gray vertical bar),
  with the change marked **inline** inside that one sentence — no
  Original/Revised labels, no two-column table, no separate stacked blocks:
  | State | Color | Other markup |
  |---|---|---|
  | unchanged original text | medium gray / blue-gray | none |
  | inserted text | **bright green** | none |
  | deleted text | **bright red** | red strikethrough |
  - Insert-only change (typo-format-1): sentence shown once, the added tokens
    (`Ra`, `μ`) colored green inline. ("Both groups exhibit an <green>Ra</green>
    of approximately 0.8 <green>μ</green>m.")
  - Insert + delete change (typo-format-2): same single quote block, deleted
    tokens rendered red with strikethrough, inserted tokens green. ("…specimens
    with an surface ~~<red>surface roughness</red>~~ <green>Ra</green> of
    approximately 0.8 <green>μ</green>m.")
  - Partial quotes use a leading `...` to mark the truncation; only the sentence
    containing the change is quoted, not the whole paragraph.
  - This is Word's track-changes visual convention, **reproduced by hand in
    tex/PDF via color + strikethrough**. It is more compact than bullet lists
    and matches the redline idiom reviewers already know.
  - **No acknowledgement, no explanatory prose** for these — the quote block IS
    the answer. The reviewer reads the colored tokens and understands the
    change. This is "format-over-prose" taken to its limit.
- Canonical anti-pattern to avoid: turning "Ra, μm" into "We sincerely thank the
  reviewer for your meticulous review. The surface roughness value refers to the
  arithmetic mean roughness (Ra), and the unit is microns (μm). We have revised
  the manuscript accordingly."
- **Template gap (extends the §6 table) — partly already there.** The existing
  `changes` environment in `reviewresponse.sty` (line 134) is already a
  `tcolorbox` with **`leftrule=1.5em`** (the left vertical bar = the quote-block
  rail) and `colorchangetext` body color (= the medium gray). So the **shell** of
  the inline-redline quote block already exists. What's missing is the
  **two-state change macros**: an `\added{...}` (bright green, no markup) and a
  `\deleted{...}` (bright red + strikethrough, needs `ulem` or `soul`). The
  sample achieved the look by hand with raw `\textcolor`; the skill should
  promote that to two named macros so responses are written structurally
  (`\added{Ra}` / `\deleted{surface roughness}`) not as raw color commands.
  Implementation choice — extend `reviewresponse.sty` upstream, or layer a
  sci-respond-local `.sty` on top — is deferred, but the macro contract
  (`\added` / `\deleted` over the existing `changes` shell) is fixed.

---

## 2. Document skeleton

Revised from the sample. Two structural changes from the sample's Word layout:
(a) a dedicated **cover page** is added at the front (the sample had none — it
opened on the acknowledgement), and (b) the **opening acknowledgement moves to
the end** (same substance-first principle as the per-response order in §3).

```
Cover page (its own page, \clearpage after)        ← NEW, not in sample
   Response Letter #<rN>     ← rN = revision round (matches manuscript/rN/)
             for
   "full manuscript title"
   manuscript-id             ← double-blind safe: ID has no identity info
   (nothing else — see note)

Major revisions overview       ← author's style, not a journal mandate
   grouped by manuscript section:
   ├─ Structural Adjustments   (section order, new Nomenclature)
   ├─ Results                  (expansions, migrations to SI)
   ├─ Discussion               (simplifications)
   ├─ Methods                  (added detail)
   ├─ Figures                  (redrawn to pub standard)
   ├─ Supplementary Methods    (new content)
   ├─ Supplementary Discussion (new content)
   └─ Text Revisions           (proofreading)

Reviewer #1 / Reviewer #2
   each comment → response (per §3 five-part order, substance-first)

Closing acknowledgement (optional, last)           ← MOVED from front
   one short line, or omitted entirely
```

### Cover page

- **Style:** AAAS-supplementary-materials style — a standalone title page,
  centered, with vertical breathing room above/below. `\clearpage` separates it
  from the body.
- **Three fields only, double-blind safe:** `Response Letter #<rN>` (large) /
  `for` (small, transition word) / the full manuscript title (centered) /
  manuscript-id. Nothing else.
- **`<rN>` = revision round**, matching the `manuscript/rN/` directory (r1 =
  first revision round, r2 = second, …). The sample's "#1" was r1.
- **No other info on the cover.** No authors, no emails, no affiliations, no
  dates, no journal name — double-blind rules these out, and even non-identity
  fields are noise on a cover whose only job is identification (which round,
  which manuscript). The global rule (no real names/ORCiDs/affiliations in
  generated templates) is enforced by simply not having those fields.
- **No Response-Figure table of contents** (the AAAS "Figure S1–SN" list). Its
  value in a Response letter is low — the reviewer-by-reviewer structure is
  itself the table of contents, and a separate figure list duplicates
  information. Same anti-noise principle as acknowledgement restraint. Add one
  only if a round carries ≥3 Response Figures AND the author asks for it; never
  by default.

**Note on the overview:** the per-section grouping after the cover is the
author's personal organization habit, **not** a hard journal requirement.
sci-respond includes it by default, but it must be optional (skippable for minor
revision / short responses).

**Note on the closing acknowledgement:** the sample opened with a generic thanks
paragraph ("Dear Editors and Reviewers, Thank you for…"). The skill revises this
— the opening acknowledgement is dropped; if any thanks is warranted, it appears
as one short line at the very end, or is omitted (default). Same principle as
the per-response acknowledgement (§3, rule 5).

---

## 3. Per-response structure — the five-part pattern

Across the 20 responses in the sample (R1: 14, R2: 6), each follows a five-part
shape — but **not every part is mandatory**, and the order is revised from the
sample. **Open with the substance, end with the thanks (if any).** The sample
opened every response with an acknowledgement; the author has revised this —
acknowledgement moves to the end and becomes optional.

Revised order (substance-first):

| Part | Role | Example (R1-Q4, 316 SS thermo-mechanical props) |
|---|---|---|
| ① Facts / data | state data, give formulas, cite refs — grounded | microhardness from [1], E/ν from supplier, deviation vs [3] |
| ② Evidence | Response Figure / Table supporting the claim | Response Fig 1: contact area / TCR under two parameter sets + relative-diff formula |
| ③ Stance | does this undermine the core conclusion? | "this systematic discrepancy… does not undermine the core conclusions" |
| ④ Landing | where the change landed in the manuscript | (implicit in overview, or explicit "added to Results / Supplementary Discussion 3") |
| ⑤ Acknowledge | "We appreciate/thank the reviewer for…" — **optional, last** | (omitted by default) |

**Why acknowledgement moves to last:** the reviewer opens a response to learn
*what changed and why*, not to be thanked. Substance-first honors the
first-principle (lowest cognitive cost to the reviewer) and the
acknowledgement-restraint hard rule. This is a deliberate revision of the
sample — the sample led with thanks, the skill will not.

**Acknowledgement (⑤) is optional, not generated by default.** The skill does
*not* auto-emit a thanks line. The author adds one only when warranted (heavy
data-backed or concede responses), and even then it is one short line. For
typo / clarification responses (which use the inline-redline quote block, §1.4),
there is no acknowledgement at all — the quote block IS the answer.

**Not every response uses all five parts.** A typo response (R1-Q10) uses only
④ Landing (as the redline quote block). A calculation-heavy response (R2-Q5,
compute efficiency) uses ①②③④, no ⑤. The skill lets the author pick the depth
per response; the only fixed rule is *order* — substance before thanks.

---

## 4. Response strategy taxonomy — 6 types observed

Mapping the 20 responses to strategies (superset of response-skill's 5, with one
extra):

| Strategy | Count | Typical | Trait |
|---|---|---|---|
| **agree & revise** | R1-Q1/Q2/Q3/Q5/Q10/Q11, R2-Q1 | add Nomenclature, trim captions | acknowledge + landing, lightweight |
| **clarify without expanding** | R1-Q7 (roughness defn), R2-Q3 (why DenseNet121) | "Ra, μm", "alphabetical order" | pure-text clarification, sometimes disarmingly honest |
| **data-backed defense** | R1-Q4, R1-Q8, R2-Q5 | Response Fig/Table + formula + quantified error | heavyweight, with figure |
| **concede limitation** | R1-Q6, R1-Q13, R2-Q6 | "needs retraining, but cost is manageable" | step back, write the limit into Discussion |
| **partial disagree** | R1-Q9 (contact-area trend), R2-Q6 (Fig6 rotation) | caveat first, then explain | "theoretically predicted, not experimentally validated" |
| **external reference** | R1-Q12 (vs ML literature) | cite own Chinaxiv preprint | borrow a preprint to fill the gap |

**Core observation:** nearly no response is a bare "agreed, done." Every
response carries evidence or a stance. This is claim-driven + grounded made
concrete at the response layer.

---

## 5. Author's stylistic signatures (confirmed intentional)

These are **not** template prescriptions — they are the author's deliberate
style, and become sci-respond rules:

1. **Acknowledgements are restrained, then varied.** The default is *no*
   acknowledgement — most responses (typo, pure clarification, "fixed, see X")
   need none. When one is warranted (heavy data-backed or concede responses),
   it is short and its opener varies. Anti-AI-pattern discipline applies only
   to the acknowledgements that survive the first cut. Becomes a hard writing
   rule.
2. **Heavy responses carry independently-numbered Response Figures / Tables.**
   Not mixed with manuscript figure numbers. Nat Comms family convention.
3. **Inline `[1]` local citations, not a shared bibliography.** Response-letter
   references are self-contained and locally numbered within each response.
4. **Landing statements frequently point to Supplementary Discussion/Method X.**
   Revision often moves content *into* SI rather than piling it into the main
   text. Consistent with D4 (SI as write's by-product) and D3 (float strategy).
5. **"Give the reviewer an exit" stance** — R2's last response (Fig6 rotation
   validation) offers "we can remove this if you prefer only experimentally
   validated results." Not a hard pushback; a polite, justified, open stance.
6. **Disarmingly honest to the point of self-exposure** — alphabetical-order
   DenseNet pick, unvalidated predictions stated plainly. AI writing defaults to
   embellishment; this is the opposite, on purpose. (See rule 2.)

---

## 6. Gap vs. the bundled template suite

The skill's base template is **bundled in its own `assets/response-template/`**
(`review_response.tex` + `reviewresponse.sty` + `Reviewers/R1.tex`, originally by
Karl-Ludwig Besser, copied into the skill source so it is self-contained — no
dependency on a project-root `templates/response/`). The sample is another fill
of the **same** template family. No second template is authored. But the sample
reveals gaps the bundled template doesn't cover:

| Template has | Sample needs but template lacks |
|---|---|
| `\reviewer` + `generalcomment` + `revcomment` + `revresponse` + `changes` environments | **Major-revisions overview block** (per-section global change list) — author's style, must be addable |
| Sequential single-reviewer structure | **Response Figure / Response Table independent numbering** (separate counter, not shared with manuscript) |
| | **Per-response local references** (`[1]` inline, local to each response, not the manuscript bib) |
| `changes` environment (R1.tex demo uses `\lipsum`) | The sample **doesn't** use `changes` — it writes the change inline in `revresponse`. Decide: keep `changes` for quoted manuscript text, or drop it. |

These gaps are template-extension candidates, to be resolved at implementation
time (extend reviewresponse.sty, or add a sci-respond-local `.sty` that layers on
top — decision deferred).

---

## 7. Resolved design decisions (from the cross-cutting-tricks pass)

The "take the best of every house" extraction (`cross-cutting-tricks.md`,
distilled from 6 rebuttal repos) resolved the major open questions. The
meta-rule (§0) graded each adoption: mechanisms that **help the human decide**
are kept; mechanisms that **decide for the human** are demoted to suggestions or
cut. Full provenance (repo + file:line) lives in `cross-cutting-tricks.md`.

### 7.1 HITL checkpoint — single pause after analysis, before drafting
**Resolved.** Intake → issue decomposition → per-issue strategy selection run in
one pass; the skill then **stops** and shows the author the complete issue
ledger + each issue's proposed strategy + safe-claim-boundary. The author
confirms or adjusts; only then does drafting begin. Not per-stage, not
per-response — one pause at the decision that actually needs a human
(paper-rebuttal-skill `workflow.md:114-117`).

### 7.2 Shared revision-round state — schema and location
**Resolved (draft, pending sci-revise parallel design).**

**Location:** the revision-round process state lives under
**`sci-skills/sci-revise/`** — sci-revise's own working directory, same as every
other product-owning skill in the family (sci-draw/, sci-write/, sci-submit/).
Family convention: multiple skills co-read/write a shared directory is normal
(`sci-skills/sci-write/terminology-ledger.md` is co-owned by write/story/polish;
same pattern here). So sci-respond **writes into** `sci-skills/sci-revise/`,
sci-revise reads + writes, sci-polish reads the polish-todo. One directory, all
revision-round process state. `manuscript/rN/` stays reserved for the formal
product (the revised tex + the response letter + the reviews); process metadata
does not pollute it.

**The response product lives in `manuscript/rN/response/`** (CONTRACT-reserved),
not under `sci-skills/`. sci-respond does **not** get its own output directory —
like sci-story/sci-polish, its product goes into `manuscript/`. Only the
process state (ledger, change-log) lives in the shared `sci-skills/sci-revise/`.

**What sci-respond reads (not writes):** the response is grounded in more than
the manuscript. sci-respond reads the writing-stage products, which record the
paper's *thinking* and are often more useful than the manuscript text for
judging an underlying concern or holding the claim boundary:
- `sci-skills/sci-write/claim.md` — the claim boundary (do not cross)
- `sci-skills/sci-write/paper-plan.md`, `figN-reading.md`, `terminology-ledger.md`
- `sci-skills/sci-draw/figN-report.md` — figure evidence and statistics

**Structure** (two-layer, paper-rebuttal-skill + Review2Rebuttal):

- **`sci-skills/sci-revise/issue-ledger.md`** — thin index + per-issue rows
  (the join key between sci-respond and sci-revise). Stable ID `R1-Q03`
  (Review2Rebuttal `build_issue_index.py:117`). Each row:
  `{id, reviewer, surface_comment, underlying_concern, stance, evidence_anchors[],
  manuscript_action, manuscript_location, revision_kind, safety(proposed|approved), status}`.
  - `revision_kind` ∈ `{surgical, polish-needed}` — see §7.7; this field is how
    sci-respond tells sci-revise (and sci-polish) what kind of edit each issue
    requires.
  - **Thin index only** — status, file links, current active round/version.
    Never duplicates full content (paper-rebuttal-skill `workflow.md:30-31`).
- **`sci-skills/sci-revise/change-log.md`** — delta-only, append-only
  (paper-rebuttal-skill `workflow.md:107`, `:194-220`). The audit trail; never
  the place to store current truth.
- **`sci-skills/sci-revise/polish-todo.md`** — the list of large newly-inserted
  passages that need polishing. See §7.7 for what goes in it (large insertions
  only, not minor edits) and its per-entry shape (location + opening-N-chars
  snapshot).
- **Safe-claim-boundary** per issue (in the ledger) — operationalizes honesty:
  before answering, the claim is bounded to what paper/code evidence supports
  (Review2Rebuttal `build_evidence_map.py:17-22`).
- **`INF:` anchor** — anything the skill inferred (not read from
  paper/review/experiment) is tagged `INF:` and visible as inference, not hard
  evidence (awesome-rebuttal `02_information_collection.md:109-127`). Cheapest
  hallucination guard.
- **`[TBD]`** for any missing numeric value the author hasn't supplied
  (paper-rebuttal-skill `SKILL.md:93`).

### 7.3 Self-containment enforcement — gate at write-time + final audit
**Resolved.** Two layers:
- **At the checkpoint (§7.1):** each issue's row carries evidence_anchors and
  manuscript_location — if either is empty, the issue isn't draft-ready.
- **Final audit before send** — coverage check (every concern mapped to a
  response state, including `deferred_with_reason`; awesome-rebuttal
  `08_strategy_planner.md:341-349`) + integrity firewall (banned rebuttal
  moves — "reviewer didn't read," "you misunderstood," speculating motives —
  hit = delete; adapted from Meet-Reviewer-2 `reviewing-rubric.md:89-112`) +
  independent-reviewer read (a fresh skeptic who has *only* the response letter
  — what's still unclear? This is the operational test of the first principle;
  awesome-rebuttal `18_rebuttal_rehearsal.md`, simplified to a single pass, no
  subagent orchestration).

### 7.4 Writing discipline — adopted rules
- **Substance-first response order (see §3).** First sentence = the answer / the
  facts. Acknowledgement, if any, goes at the *end* of the response and is one
  short line — not generated by default (Rebuttal-Skill `SKILL.md:688-705` for
  the direct-answer-first principle; ordering and optionality are our revision
  of the sample). Positive form of the acknowledgement-restraint hard rule.
- **Manuscript-light by default.** Targeted wording > defensive paragraphs; if
  the added text is rebuttal-only defense, keep it in the response, not the
  manuscript (response-skill `SKILL.md:24-27`, `response-workflow.md:87-88`).
  Bounds sci-revise's amplitude.
- **Cross-reviewer overlap — answer in full, do NOT reference.** ~~The earlier
  "already-covered → cite" adoption (response-skill) is REVERSED.~~ Different
  reviewers may use separate submission systems and cannot see each other's
  responses — a cross-reference ("covered in R1's response, page X") is empty to
  a reviewer who can't see R1's section. So if R1 and R2 raise the same concern,
  answer it **in full in each reviewer's section** (wording may vary, content
  complete in both). The manuscript edit is made once (linked via `parallel_to`
  in the ledger), but each response states it in full. Extends the first
  principle: a response is self-contained — no reliance on the manuscript *or*
  on another reviewer's section.
- **Solution order fuses importance and logic** (workflow.md §2.1; ledger's
  `solution_order` + `depends_on` fields). Importance already carries logic:
  typo/format always last (depend on nothing, affect nothing); "change"
  (claim/experiment) before "fix" (explanation) — the change sets the footing
  the explanation stands on; foundational issues (does claim X hold?) before
  derived ones (application boundary *of* claim X). The ledger's thin index
  carries one `solution_order` checklist the author works top-down. **Work in
  solution order; present point-by-point per reviewer** (journal standard).
  Internal only — avoids rework when a derived answer is settled before its
  foundation.
- **Banned qualifiers without evidence.** "improves/outperforms/significant/
  robust/SOTA" prohibited unless backed by the relevant metric
  (awesome-rebuttal `11_response_writer.md:125-126`).
- **Compression "preserve" list.** When over length, preserve first: direct
  answers, key numbers, comparison controls, uncertainty, claim narrowing,
  manuscript changes, unresolved limitations. Remove first: repeated thanks,
  repeated quotations, generic background (Rebuttal-Skill `SKILL.md:1007-1029`).

### 7.5 LaTeX mechanics — adopted
- **Caption-coloring** for revised figures/tables (color the caption, not cells
  or internals; response-skill `latex-redline-checklist.md:8-9`). Complements
  our `\added`/`\deleted` text redline.
- **`\quoteRevision{...}` macro** for quoting a revised sentence inline in prose
  responses → ```\textcolor{<color>}{\textit{...}}''``` (quote marks stay black;
  response-skill `latex-redline-checklist.md:21-23`).
- **Re-verify all later page/line refs after any manuscript insertion/deletion**
  (response-skill `latex-redline-checklist.md:44-49`). Page = visual PDF page,
  line = margin-printed line, not .tex source. Mandatory whenever sci-revise
  edits the manuscript.
- **Response Figures / Tables are non-floating (as-is, zero drift).** This is
  the opposite of manuscript float strategy. The manuscript (D3) floats figures
  for optimal page usage, because the journal pays for space and the reader
  follows `\ref`. A Response letter does the opposite: a Response Figure must
  sit *beside the paragraph that discusses it*, because the reviewer must not
  flip pages to see it (first principle). So Response Figures never enter
  LaTeX's float queue at all.
  - **Default mechanism:** use a non-floating wrapper + `\captionof` (from the
    `caption` package) instead of the `figure`/`table` environment:
    `\begin{center}\includegraphics[...]{...}\captionof{figure}{Response Fig. 1: ...}\end{center}`.
    The figure is physically nailed to its source location — it cannot drift.
    This is the only 100% as-is guarantee.
  - **Fallback:** if `\label`/`\ref` auto-numbering linkage is required, use the
    `float` package and `[H]` (capital, `\usepackage{float}`) — `[H]` forbids
    drift, stronger than `[h!]`. Cost: occasional bottom-of-page whitespace.
  - **Never** use `[htbp]`, `[t]`, `[p]`, or bare `figure`/`table` environments
    for Response Figures — those are manuscript idioms that allow drift.
  - Template dependency: needs `\usepackage{caption}` (for `\captionof`) and
    optionally `\usepackage{float}` (for the `[H]` fallback). Add to the
    `reviewresponse.sty` layer (§6 template gap) at implementation time.
  - Word made this trivial (manual drag); tex makes it a deliberate discipline —
    the trade for getting tex's editability and the inline-redline format.
- **Compile is sci-respond's own job.** sci-respond compiles its own
  `response.tex` → PDF; it does **not** depend on sci-typeset. sci-typeset
  compiles the *manuscript* (`manuscript/vN/`) — a different document. The
  response letter is sci-respond's product, so compiling it is sci-respond's
  responsibility (each skill owns its own product, per the family's directory
  contracts). Compile command and "enough passes for refs/page numbers to
  stabilize" (`pdflatex -interaction=nonstopmode -halt-on-error`, repeated)
  live in sci-respond's SKILL.md at implementation time.

### 7.6 Demoted by the meta-rule (suggestions, not decisions)
These came out of the survey but are **demoted** because they decide for the
human or push the human out of the loop:
- **P0–P3 priority scoring formula** (Rebuttal-Skill `SKILL.md:457-463`) — at
  most a *suggested* ordering shown at the checkpoint, never an auto-applied
  ranking. The author reorders.
- **19-script artifact pipeline** (Review2Rebuttal) — rejected entirely. We keep
  "write directly in tex" (D1). The *outline-before-draft* discipline is kept as
  structured thought at the checkpoint, not as a separate markdown/script stage.
- **DO NOT RUN experiment category** (Rebuttal-Skill) — kept only as a light
  "don't promise experiments that won't land" reminder, tied to the
  safe-claim-boundary. We don't do experiment planning.

### 7.7 Surgical revision — sci-revise's defining rule (and the sci-polish handoff)

This rule belongs to **sci-revise** (the sibling that edits `manuscript/rN/tex/`
per the issue ledger), but it shapes what sci-respond writes into the ledger, so
it is recorded here too.

> **改手稿时,只改该改的那一处,不要顺手重写整段。**
> When editing the manuscript, change only the specific spot the issue requires.
> Do not rewrite the surrounding paragraph just because it could be "better."

**Why this is a rule (three reasons):**
1. **diff stays readable** — a surgical change is a one- or two-line git diff;
   a paragraph rewrite turns the diff entirely red/green and hides what actually
   changed. The reviewer (and collaborators) need to see the precise change.
2. **no new risk introduced** — rewriting a paragraph invites accidental changes
   to wording that was fine, new inconsistencies, even shifted claim meaning. A
   surgical edit cannot drift the claim.
3. **revision's job is to respond, not to optimize** — you are answering a
   reviewer, not polishing. Untouched text stays untouched. Same posture as
   acknowledgement restraint and manuscript-light (§7.4): do what the reviewer
   asked, nothing more.

**This is what distinguishes sci-revise from sci-polish.** Both edit
`manuscript/rN/tex/` prose, but with opposite defaults:
- **sci-revise** = surgical scalpel. Default edit = the smallest change that
  resolves the issue (often a single `\added`/`\deleted` token, one sentence,
  one number). Driven by the issue ledger.
- **sci-polish** = paragraph-level optimization. Default edit = rework the prose
  for wording/flow/language. Driven by "make this read better," not by a
  reviewer comment. (sci-polish already operates on `r1/tex/` — see its SKILL.md
  line 34 — that's expected and not a conflict.)

**The handoff (the exception the user named):** when a reviewer *explicitly*
flags a language problem or asks for polishing of a passage, that passage's
`revision_kind` is `polish-needed`, not `surgical`. sci-revise does **not**
rewrite that paragraph itself — it hands the passage to **sci-polish** for
paragraph-level work. The exception is narrow: it requires an explicit reviewer
request for language/polishing, not the agent's own judgment that "this could be
written better."

**What this means for sci-respond (the writer of the ledger):** at the
checkpoint (§7.1), each issue's `revision_kind` is set. Default `surgical`. Set
`polish-needed` only when the reviewer's comment is explicitly about language
quality / asks for polishing — and in that case the `manuscript_action` field
should route to sci-polish rather than describe a surgical edit. This tag is the
single field that prevents the agent from drifting into paragraph rewrites
during revision.

### 7.8 polish-todo — large newly-inserted passages (sci-revise → sci-polish)

A second, distinct source of `polish-needed`: **large passages sci-revise
newly inserts or rewrites** while responding to a reviewer (not the reviewer
asking for polish — this is a side-effect of revision itself).

**Why this matters:** surgical edits (a token, a number, one sentence) don't
need polishing — they're too small to drift the manuscript's language
consistency. But a large newly-written paragraph (e.g. the multi-paragraph
mechanics explanation in R1-Q9, or a new limitations block in R1-Q13) is
**first-draft prose that hasn't been smoothed**, and it sits next to polished
text from the original submission. That contrast is visible to the editor and
reviewer. These passages are the "must-do" polish cases — even under the
revision-stage rule "polish only if you must" (see §8 open question), these
qualify.

**The line — large insertions only, minor edits excluded:**
- **Record in polish-todo:** newly-inserted or heavily-rewritten passages above
  a size threshold (rough heuristic: ≥ one full paragraph, or ~3+ sentences of
  net-new prose). These get a `polish-needed` mark + a polish-todo entry.
- **Do NOT record:** token swaps, single-sentence tweaks, typo fixes, number
  updates, `\added`/`\deleted` redlines — the surgical edits. They don't affect
  language consistency; recording them would bloat the todo and burn context for
  no gain.

**polish-todo.md entry shape** (per the user's spec — lightweight, locatable,
no full-text copy):
```
- location: manuscript/r1/tex/sections/results.tex  (after \label{fig:contact-area})
  snapshot: "To begin, we would like to clarify that the predicted contact
             area values are theoretical estimates, …"   (~first 120 chars)
  reason: new multi-paragraph mechanics explanation inserted for R1-Q9
  from_issue: R1-Q09
```
- **location** — file + anchor/line/label, so sci-polish can find it without
  reading the whole manuscript.
- **snapshot** — the opening ~N characters/words of the inserted passage, so
  sci-polish can grep/locate the exact paragraph even after later shifts. **Not
  the full text** — that would duplicate the manuscript and bloat the file.
- **reason + from_issue** — why this needs polish and which reviewer issue it
  came from, for traceability.

**Handoff:** sci-revise writes polish-todo.md as it edits. Whether to actually
run sci-polish on these passages is the **author's call** (meta-rule §0) —
sci-revise surfaces the list, it does not auto-polish. In a revision stage
where "polish only if you must," these large-insertion passages are the ones
that rise to "must"; the author decides the rest.

## 8. Remaining open questions

- **Per-section overview — default on or off?** Author's style says default on;
  minor revisions may not need it. Leaning: default-on with a one-line opt-out.
- **Acknowledgement-restraint check — how enforced concretely?** A lint that
  counts acknowledgement sentences per response and weighs against the response's
  weight (typo/clarify → 0; data-backed/concede → ≤1 short line). "We sincerely
  appreciate your meticulous…" on a typo fix is the canonical failure case.
- **Local citation numbering.** reviewresponse.sty uses biblatex with
  `refsection=section` — does that already give per-response local numbering, or
  does the sample's `[1][2][3]` inline style need a different mechanism? Verify
  against the actual `.sty` behavior before designing.
- **sci-polish revision-mode restraint (deferred — not this round).** When
  sci-polish runs during a revision stage (on polish-todo passages or
  reviewer-requested polish), it should default to **"polish only if you must"**
  — same restraint posture as sci-revise's surgical rule, not a full
  manuscript re-polish. Only passages flagged as must-do (large new insertions,
  explicit reviewer language requests) get touched; everything else is left
  alone. This requires a revision-mode flag/logic in sci-polish itself; deferred
  until sci-polish is revisited. Tracked here so it isn't lost.

---

## 9. What this skill is NOT (boundary)

Mirroring the family's boundary discipline:

| Need | Goes to |
|---|---|
| Edit the manuscript tex per the locked decisions (surgical, per-issue) | **sci-revise** (sibling, not yet designed) — default `revision_kind: surgical` |
| A passage the reviewer explicitly asked to polish (language/wording) | **sci-polish** — sci-revise hands off when `revision_kind: polish-needed` (§7.7) |
| Polish manuscript prose outside a revision round (first-draft polish) | sci-polish |
| Cover letter (first submission / revision) | sci-submit |
| Draw new data figures for the manuscript | sci-draw |
| Simulated peer review / red-team before submission | (not in family yet; research exists in `_research/peer-review-skills/`) |

sci-respond writes **only** the response letter. It does not touch manuscript
tex, does not write cover letters, does not draw figures (it can reference and
inline-existing Response Figures, but creating data figures is sci-draw's job).
