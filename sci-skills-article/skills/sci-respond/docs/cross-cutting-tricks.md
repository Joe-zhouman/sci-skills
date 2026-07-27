# sci-respond — tricks distilled from 6 rebuttal repos

> **Status: distillation, not decisions.** This is the "take the best of every
> house" extraction from the 6 repos in `_research/rebuttal-writing-skills/repos/`,
> cross-referenced against our `design-note.md`. Each item is graded for adoption.
> Nothing here is implemented — it's the menu to choose from when we write SKILL.md.
>
> Source repos: awesome-rebuttal, Review2Rebuttal, response-skill, paper-rebuttal-skill,
> Meet-Reviewer-2, Rebuttal-Skill. Survey reports at `_research/rebuttal-writing-skills/00-market-survey.md`.

## How to read this

- **🟢 ADOPT** — genuinely fills a gap in our design; high value, low/mid cost.
- **🟡 MAYBE** — interesting but heavy, or overlaps our existing rules; defer or simplify.
- **🔴 DECLINE** — duplicates what we have, or conflicts and we're right (reasons given).
- Each item cites the repo + file:line so you can verify.

The tricks cluster into 5 themes. Within each, the highest-leverage ones are first.

---

## Theme 1 — State contract & the response↔revision coupling

This is the highest-value cluster for us: it directly answers design-note §7's
open question "what lives in the shared `manuscript/rN/` state file?"

### 🟢 Stable issue IDs (e.g. `R1-Q03`) — the coupling backbone
Review2Rebuttal `build_issue_index.py:117` assigns `f"{reviewer_id}-{prefix}-{counters[field]:02d}"`. awesome-rebuttal uses `REVIEW:<reviewer-id>:<field>` anchors (`02_information_collection.md:109-127`). paper-rebuttal-skill's atomic concern ledger uses stable IDs throughout.
**Adopt.** Every reviewer comment gets a stable ID at intake. The ID is the key that sci-respond's response and sci-revise's manuscript edit both reference — it's the literal join column in the shared state. Without it, the coupling is hand-wavy.

### 🟢 Thin index + separate change-ledger (not one fat state file)
paper-rebuttal-skill: `index.md` is a thin pointer (status, file links, current active version) — never duplicates content (`workflow.md:30-31`). The change history lives in a separate `04-human-feedback-revisions_vN.md` that records **only delta** (`workflow.md:107`, template at `:194-220`). Stage versions are **full replacements** (modified + unchanged together), so the reader never reconstructs current state from old+dff (`workflow.md:127`).
**Adopt the split.** Our shared state should separate: (a) *current truth* per issue (full snapshot, readable in isolation), (b) *change log* (delta-only append). Two structures, not one.

### 🟢 Per-issue evidence ledger with "safe claim boundary"
Review2Rebuttal `artifact-schema.md:82-96` + `build_evidence_map.py:17-22`: each issue gets `Paper evidence / Repo evidence / Missing evidence / Safe claim boundary / Risk level`. The safe_claim_boundary() returns one of three constraint levels based on whether paper/code hits exist.
**Adopt.** This operationalizes our "honesty" rule. Instead of "be honest," it's "before answering this issue, your claim is bounded to *this*." Concretely gates what the response can assert. Pairs with our `\added`/`\deleted` — the boundary decides what's allowed to be a confident green statement vs a hedged one.

### 🟢 Evidence-anchor prefixes (`PAPER:` / `REVIEW:` / `EXP:` / `INF:`)
awesome-rebuttal `02_information_collection.md:109-127`. Every claim traces to a typed anchor. The `INF:` prefix is reserved for **AI inferences that are NOT hard evidence** and must be labeled as such.
**Adopt, especially `INF:`.** This is the single cheapest hallucination guard: if the skill inferred it (not read from paper/review/experiment), it's tagged `INF:` and the reader knows. Aligns with our honesty principle.

### 🟢 Per-issue fields: stance + manuscript action + evidence location + safety
Synthesized from response-skill's "response map" (`response-workflow.md:4-13`: ID, Concern, Answer type, Manuscript action, Evidence location) + Rebuttal-Skill's 4 internal artifacts (`SKILL.md:1258-1276`: concern matrix, experiment ledger, evidence ledger, revision backlog) + paper-rebuttal-skill's `Safety` field on every manuscript revision example (`strategy-generation.md:86`: proposed vs approved).
**Adopt as the shared-state row schema.** Each issue row: `{id, reviewer, surface_comment, underlying_concern, stance, evidence_anchors[], manuscript_action, manuscript_location, safety(proposed|approved), status}`. This is the contract sci-respond writes and sci-revise reads.

### 🟢 `[TBD]` placeholder discipline for missing numbers
paper-rebuttal-skill enforces `[TBD]` for any missing numeric value at every layer (`SKILL.md:93`, `rebuttal-writing.md:51`, `strategy-generation.md:165`).
**Adopt.** Concrete mechanism for honesty: never invent a number the author hasn't supplied. Pairs with awesome-rebuttal's numeric-claim provenance (`11_response_writer.md:107-127`, with a banned-qualifier list: "improves/outperforms/significant/SOTA" without evidence).

### 🟡 Schema doc (artifact-schema.md) — write the contract down
Review2Rebuttal `references/artifact-schema.md` defines allowed values per artifact (e.g. strategy: `accept/defend/clarify/experiment/defer`).
**Maybe.** Right in principle, but our state file is one small file, not a 19-script pipeline. A short field-allowable-values table inline in design-note may suffice; a separate schema doc is overkill until the skill grows.

### 🟡 revision-config.json metadata file
Review2Rebuttal `workspace-structure.md:41-54`: `paper_path, repo_path, venue, year, deadline, has_supplementary`.
**Maybe.** Useful for multi-round, but most of this lives in our family's existing `manuscript-meta.md` (owned by sci-submit). Don't duplicate — check what sci-submit already captures before adding.

---

## Theme 2 — HITL gates: where to stop

Answers design-note §7's open question "where does the HITL checkpoint fire?"

### 🟢 Single checkpoint after analysis, before drafting
paper-rebuttal-skill: stages 0–3 (paper context, issue extraction, evidence decisions, strategy) run **continuously in one pass**; the single pause fires **after strategy, before any response drafting** (`SKILL.md:40-42`, `workflow.md:114-117`). Not per-stage.
**Adopt as our default.** This resolves the open question cleanly: sci-respond runs intake → issue decomp → strategy selection in one pass, then **stops** and shows the author the issue ledger + per-issue proposed strategy + safe-claim-boundaries. Author confirms/adjusts. Only then does drafting begin.

### 🟢 Strategy-before-drafting: 2–4 options + tradeoffs for consequential issues
response-skill `SKILL.md:19-22`: "For ambiguous or consequential comments, first offer 2-4 response strategies with tradeoffs. Default to the lowest-risk strategy that genuinely addresses the concern."
**Adopt.** At the checkpoint, consequential issues (defend vs concede vs experiment) get a menu, not a single pick. This is the decision the author actually needs to make — surface it explicitly.

### 🟢 Underlying-concern inference (surface vs underlying)
Rebuttal-Skill `SKILL.md:230-256`: every comment split into (a) surface text, (b) underlying concern — the decision-relevant doubt, (c) evidence that would resolve it, (d) confidence. Common underlying concerns catalogued. Called "arguably the most valuable single trick."
**Adopt.** This is the analysis the checkpoint gate produces. Reviewer says "add baseline X"; underlying concern is "unfair comparison." The response addresses the concern, not the literal ask. Without this step you answer the wrong question.

### 🟢 Intent Diagnosis Card for ambiguous comments
Rebuttal-Skill `SKILL.md:264-293`: when intent is uncertain, a card with most-likely + alternative interpretation + confidence + **safe response strategy** (wording valid under both interpretations).
**Adopt.** The "safe response strategy" field is the clever part — a response that's correct regardless of which interpretation the reviewer meant. Use when confidence is low.

### 🟡 author-approvals.json gate file
Review2Rebuttal: high-risk `experiment`/`defend` issues skipped unless their IDs are in `responses/author-approvals.json` (`script-usage.md:82`, `SKILL.md:248-255`, 5 trigger conditions).
**Maybe.** The 5 trigger conditions (new experiment, promised analysis, contradicts paper claim, final compile, high-risk) are worth adopting as our gate triggers. A JSON approval file is heavier than we need for a non-script skill — the checkpoint display can carry the same info.

### 🟢 "Should we rebut?" viability gate (Stage 0)
Rebuttal-Skill `SKILL.md:117-208`: before planning, classify PROMISING / BORDERLINE / LOW-RETURN. For low-return, provide a resubmission roadmap instead of wasting the rebuttal window.
**Adopt lightly.** Our equivalent: at intake, if reviews are uniformly below borderline + core premise questioned, flag it honestly ("this may not be worth a heavy revision round") rather than cheerfully drafting. Honesty principle again. Don't build the full roadmap — just the honest assessment.

### 🔴 Per-stage pauses
paper-rebuttal-skill explicitly does NOT pause per stage unless asked. We concur — one pause, not five.

---

## Theme 3 — Writing discipline (the response text itself)

### 🟢 Direct-answer-first sentence
Rebuttal-Skill `SKILL.md:688-705`: every major response opens with the direct answer in the first sentence ("Yes. The improvement remains under matched compute."), then evidence, then revision. Strong vs weak example shows why "We thank the reviewer…" is weak.
**Adopt hard.** This is the positive form of our "acknowledgement restraint" rule. First sentence = the answer. Thanks (if any) come after, or not at all. Reinforces self-containment: the reviewer gets the point immediately.

### 🟢 Manuscript-light by default
response-skill `SKILL.md:24-27`: revise the manuscript only where it naturally supports the clarification; prefer targeted wording over defensive paragraphs. "If the added text feels like rebuttal-only defense, keep it in the response letter and remove it from the manuscript" (`response-workflow.md:87-88`).
**Adopt.** Sets revision amplitude. One Discussion sentence > a new experiment, when the paper naturally supports it. Bounds how much sci-revise actually does.

### 🔴 REVERSED — "Already-covered → cite, don't re-edit"
response-skill `SKILL.md:43`: if reviewer 2's concern is already covered by reviewer 1's colored revision, cite that existing revision instead of duplicating the manuscript edit.
**Originally adopted, then REVERSED by the author.** Different reviewers may use
separate submission systems and cannot see each other's responses — a
cross-reference ("covered in R1's response, page X") is **empty** to a reviewer
who can't see R1's section. So duplicated concerns are answered **in full in each
reviewer's section** instead. The manuscript edit itself is made once (linked via
`parallel_to` in the ledger), but each response states it completely. This
extends the first principle: a response is self-contained — no reliance on the
manuscript *or* on another reviewer's section. (Kept here as a record of the
reversal so the reasoning isn't lost.)

### 🟢 Compression rules (ordered removal when over length)
Rebuttal-Skill `SKILL.md:1007-1029`: when over limit, remove in order: repeated thanks → repeated quotations → generic background → adjectives → duplicate responses → low-impact minor comments → impl detail. **Preserve at all costs:** direct answers, key numbers, comparison controls, uncertainty, claim narrowing, manuscript changes, unresolved limitations.
**Adopt.** The "preserve" list is a priority guard that doubles as a writing-values statement. The "remove" order encodes which parts are most expendable — thanks first (matches our restraint rule).

### 🟢 Per-issue `must_avoid` / banned qualifiers
awesome-rebuttal `11_response_writer.md:125-126`: prohibit "improves/outperforms/significant/robust/SOTA" unless supported by the relevant metric. Rebuttal-Skill has 12 anti-patterns (`SKILL.md:1194-1213`), e.g. "treat all criticism as misunderstanding," "bury the direct answer under background."
**Adopt the banned-qualifier list.** Concrete honesty mechanism: no unsubstantiated superlatives. The anti-patterns double as a final-check checklist.

### 🟢 Three-color issue grading (core / misread-risk / trivial)
Meet-Reviewer-2 `review-schema.md:27-37`. Adapted for our use: classify reviewer comments as 🔴 core challenge (needs evidence) / 🟡 misunderstanding (clarify) / 🟢 trivial (fix). The middle category — "paper is fine but writing handed them a gun" — is the insight.
**Adopt.** This triage at intake decides per-issue effort and stance. Distinguishing "they misread" from "the claim is weak" is exactly the underlying-concern inference (Theme 2).

### 🟡 Opening summary templates (positive vs critical reviews)
Rebuttal-Skill `SKILL.md:722-738`: two opening-paragraph templates. Critical-review variant avoids manufacturing false praise.
**Maybe.** Our sample's "Major revisions overview" already covers this and is the author's preferred style. Borrow the "don't manufacture positive statements" rule; skip the templates.

### 🟡 Novelty delta table pattern
Rebuttal-Skill `SKILL.md:775-866`: for novelty concerns, a 4-col table (Prior work | Capability/assumption | This paper's difference | Why it matters).
**Maybe.** Domain-specific (ML/conference). Useful as one optional pattern for the "external-reference / positioning" strategy, not a default.

### 🔴 Per-reviewer color assignment
response-skill `latex-redline-checklist.md:5-6` colors per reviewer (R1=red, R2=blue). **We conflict and we're right**: our fixed format uses Word track-changes idiom (green=added, red=deleted) regardless of reviewer — matches what reviewers already know, avoids color-name collisions. Keep our scheme. response-skill's "cite existing revision" (above) is the better solution for multi-reviewer overlap.

---

## Theme 4 — LaTeX / template mechanics

### 🟢 Caption-coloring for revised figures/tables (not cells/internals)
response-skill `latex-redline-checklist.md:8-9`: if a figure/table is revised, color the *caption* to signal it; avoid coloring table cells or figure internals.
**Adopt.** Concrete complement to our `\added`/`\deleted` text redline. For figure changes: `\caption{\textcolor{added-green}{Updated caption.}}`. Keeps the signal on the surface, doesn't fight cell-level coloring.

### 🟢 Italic+color quoted sentence, black quote marks
response-skill `latex-redline-checklist.md:21-23`: ` ``\textcolor{red}{\textit{revised sentence}}'' ` — the quoted manuscript sentence is italic+colored, but the surrounding quote marks stay black.
**Adopt as a macro.** For prose responses (not the typo quote-block) that quote a revised sentence inline: `\quoteRevision{...}` → ```\textcolor{<color>}{\textit{...}}''```. Distinct from the `changes`-block redline (which is for typo/clarify responses).

### 🟢 Re-verify all later page/line refs after any manuscript insertion/deletion
response-skill `latex-redline-checklist.md:44-49`: page = visual PDF page, line = margin-printed manuscript line (not .tex source line). After any insertion/deletion in the manuscript, re-check every later response reference. Visually inspect if extracted-text page boundaries are ambiguous.
**Adopt.** Critical and easy to miss: inserting a paragraph shifts all downstream line numbers. This is a mandatory re-check step whenever sci-revise edits the manuscript — couples back to the shared state (all locations must be re-verified post-edit).

### 🟡 Compile command + "enough passes"
response-skill `latex-redline-checklist.md:33-40`: `pdflatex -interaction=nonstopmode -halt-on-error main.tex`, run enough passes for refs/page numbers to stabilize.
**Maybe.** Our family's sci-typeset already owns compile-to-PDF. sci-respond should compile its own response letter (separate document), but the command details may belong in a shared compile note rather than duplicated here.

### 🟡 Seven-item final search checklist
response-skill `latex-redline-checklist.md:53-62`: search for template phrases, placeholder brackets, "later/to be added", stale page/line cites, color inconsistencies, zh/en mismatches. "Do not report completion until compile + searches run in the current session."
**Adopt (trimmed).** This IS our self-containment check made concrete. Trim zh/en unless we do paired files. The "must run in current session" rule is important — prevents stale "done" claims.

---

## Theme 5 — Self-check / audit before sending

### 🟢 Coverage audit: every concern accounted for, with `deferred_with_reason`
awesome-rebuttal `08_strategy_planner.md:341-349`: every response must account for every reviewer concern; states include `covered / covered_by_minor / covered_by_global / deferred_with_reason / needs_user_input`. You may skip a concern, but you must state why.
**Adopt.** Directly enforces self-containment at the document level: no reviewer comment silently dropped. `deferred_with_reason` is the honest way to not-answer.

### 🟢 Integrity firewall (banned rebuttal moves)
Meet-Reviewer-2 `reviewing-rubric.md:89-112` adapts ACL's H1–H17 illegitimate-critique list as a starred auditable table. For us, the mirror: a table of illegitimate *rebuttal* moves — "reviewer didn't read," "you misunderstood," speculating about motives, attacking tone. Hits get deleted or demoted.
**Adopt.** A short, explicit banned-moves table, checked before send. Concrete guard against the defensive/combative failure mode. Pairs with our honesty + acknowledgement-restraint rules.

### 🟢 Pre-send rehearsal: independent-reviewer lens
awesome-rebuttal `18_rebuttal_rehearsal.md`: simulate reviewer/AC personas reading paper+response in isolation. The **independent_reviewer** (fresh skeptic who never saw the original reviews) is the most valuable — catches blind spots the original panel shared. Advisory only, never approves submission.
**Adopt (simplified).** Full subagent orchestration is overkill. But a single "read this response as a fresh skeptic who only has the response letter — what's still unclear?" pass before send is cheap and directly tests our first principle (self-containment). This is the operational test of "reviewer never opens manuscript."

### 🟡 QA report: 6 sections (Coverage / Unsupported claims / Citation risks / Tone / Contradictions / Open decisions)
Review2Rebuttal `artifact-schema.md:225-241`. The Contradictions check (final wording vs issue file vs experiment feasibility) is the valuable one for our coupling.
**Maybe.** Heavy as a full report. Adopt the *contradictions check* specifically: response promises vs manuscript-revision state must agree. Fold into the final checklist rather than a separate report.

### 🟡 DO NOT RUN / DO NOT DO anti-list
Rebuttal-Skill `SKILL.md:436-455`: explicit category for experiments that don't address the underlying concern, duplicate evidence, or are anxiety-driven.
**Maybe.** Valuable concept (guards against busywork), but our scope is response-writing not experiment-planning. Keep as a light "don't promise experiments that won't land" reminder tied to the safe-claim-boundary.

---

## Distilled adoption list — the short version

If we adopt only ~12 things, these give the most leverage:

| # | Trick | Theme | Why |
|---|---|---|---|
| 1 | Stable issue IDs (`R1-Q03`) | 1 | The response↔revision join key |
| 2 | Thin index + delta-only change log | 1 | Shared-state structure |
| 3 | Per-issue evidence ledger + safe-claim-boundary | 1 | Operationalizes honesty |
| 4 | `INF:` anchor for AI inferences | 1 | Cheapest hallucination guard |
| 5 | Single checkpoint after analysis, before drafting | 2 | Resolves HITL open question |
| 6 | Underlying-concern inference + 2–4 strategy menu | 2 | The decision the author actually makes |
| 7 | Direct-answer-first sentence | 3 | Positive form of acknowledgement-restraint |
| 8 | Manuscript-light (bounds revision); ~~already-covered→cite~~ REVERSED → answer in full per reviewer (reviewers can't see each other's sections) | 3 | Bounds revision; multi-reviewer handled by full duplicate answers, not cross-ref |
| 9 | Compression "preserve" list + banned qualifiers | 3 | Honesty at the word level |
| 10 | Caption-coloring + re-verify page/line after edits | 4 | LaTeX mechanics complements |
| 11 | Coverage audit with `deferred_with_reason` | 5 | No concern silently dropped |
| 12 | Integrity firewall + independent-reviewer pre-send check | 5 | Tests self-containment before send |

## Conflicts where we keep our way

- **Per-reviewer colors** (response-skill) → we keep green/red track-changes idiom. Our way matches reviewer habit, avoids collisions; multi-reviewer overlap handled by "cite existing revision" instead.
- **Two-stage markdown→draft generation** (Review2Rebuttal) → we keep "write directly in tex" (D1-aligned). The *outline-before-draft* discipline is borrowed, but it lives as structured thought, not a separate markdown file.
- **Per-stage HITL pauses** (paper-rebuttal-skill) → we keep single pause after analysis.

## What we already have (confirmed by the survey, not re-adopted)

- tex→PDF direct, no md intermediate (D1)
- inline redline `\added`/`\deleted` over the `changes` shell
- honesty / acknowledgement-restraint / anti-AI-phrasing (our 3 hard rules)
- evidence-linked page/line (PDF, not source)
- 6-strategy taxonomy (richer than most repos' 5)
