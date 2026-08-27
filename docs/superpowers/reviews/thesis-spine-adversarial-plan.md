# Existence Audit — thesis-spine spec

**net: -25 lines deletable**

Findings tagged against `docs/superpowers/specs/thesis-spine.md`, read through the design lens (`~/.claude/agents/refs/aquarius-lens-design.md`) + glossary (`docs/superpowers/glossary.md`) + parent spec (`docs/superpowers/specs/thesis-skill-family.md`, authority — not re-audited) + merged foundation (`sci-skills/skills/thesis-init/SKILL.md`, file-contract ground truth).

---

§⑤ para "诚实的边界" (L94): hidden assumption: crack-pointing at architecture level is evidence-grounded and falsifiable "like sci-write's figN-reading." False equivalence. figN-reading compares a prose `Core conclusion` against a rendered PNG — two concrete artifacts, the comparison is "does prose match pixels." crack-pointing compares a framework / main-line / progression claim against paper content — the framework is an abstraction, "does it unify paper C" is a depth judgment, not a fact-check. The spec's own crack example (L89) demonstrates the slide: "ch3 的 results 实际上没引出 ch4 的 question——这个递进是断言的不是挣来的" is a depth verdict (the progression lacks earned-ness) wearing an evidence costume — there is no verifiable fact that proves a chapter-to-chapter progression link is "missing," the link is an argumentative relationship, judged not located. The constraint "crack must anchor to specific evidence (b 项)" does not prevent the slide, because at architecture level the "evidence" IS a depth claim (this paper doesn't fit the framework / this progression isn't earned / this main line doesn't unify). The acceptance check (L193: "crack 条目均含 (a)(b)(c) 三要素") is a format check — a depth verdict with a pointer passes it. **This is the unchallenged premise that could collapse the design.** The layer's "AI assists but doesn't gate depth" claim holds only if "gate" = "auto-reject" (author resolves — true). It fails if "gate" = "influence" (AI frames the candidate as flawed via crack, biasing the author's depth judgment — happens by design). crack-pointing smuggles depth-influence back in, not depth-auto-gating. The parent spec's load-bearing premise (author can judge depth, aquarius #11) is therefore underdefended at this layer: an attachment-blind author's depth judgment is shaped by AI crack framing, and the spec provides no mechanism to filter depth-verdicts-in-costume from honest fact-cracks. Fix: restrict crack-pointing to verifiable-fact cracks (paper C Fig 3 shows ¬X — checkable against the paper) and explicitly exclude relational/depth cracks (progression not earned, framework doesn't unify — these are depth judgments, the author's job, not AI's), OR drop the honest/dishonest boundary claim and acknowledge architecture-level crack-pointing is depth-influence with a stated failure mode. The "dispassionate" label is earned for fact-cracks, not for depth-cracks.

§③ para "glossary 四个 architecture-level claim = spine 三个 + summary 一个" (L69): causal: claims glossary alignment, but spine also produces the umbrella (thesis-level claim), which is NOT in the glossary's enumerated four (main line / unified framework / progression / common-extraction). The umbrella is a 5th architecture-level claim the glossary doesn't list. The "argumentative vs structural" distinction doesn't fix the count — it moves the discrepancy from "3 vs 4" (parent's coverage gate vs acceptance) to "4 vs 5" (glossary's 4 vs spine's 3 structural + umbrella + summary's common-extraction = 5). The reconciliation hides the umbrella from the glossary count to claim alignment, then foregrounds it when claiming the depth gate. Glossary's own enforcement clause ("AI never gates architecture-level decisions") covers the umbrella (it is depth-gated by the author with AI crack-pointing) — so by the glossary's own definition the umbrella IS an architecture-level claim, and the glossary's enumeration of 4 is incomplete. Either update the glossary to enumerate the umbrella as a 5th architecture-level claim (honest), or drop the umbrella (but then spine Step 4 and acceptance "四者作者确认" lose their 4th item, and the parent spec's 3-vs-4 tension returns unresolved). The current form is sleight-of-hand, not clarification.

§门与 enforcement (L166) vs §③ (L67-68): contradiction: §③ says umbrella "不参与机械 coverage 计数" to align with parent spec's "三字段非空" coverage gate. §门与 enforcement says "Coverage（机械，AI/脚本可门）：三结构字段非空 + 各自 sub-coverage + umbrella 非空 + 无 pending 残留" — adds umbrella to coverage, making it 4-field coverage. This contradicts both §③ and the parent spec (family L159: "三字段非空（coverage 机械）"). The spec's own claim "无偏离需 re-review…不改父 spec 任何已定决策" (L211, L213) is false: adding umbrella to the coverage gate changes the parent's "三字段" to "四字段". Pick one: umbrella is coverage-gated (then §③'s "argumentative not structural" distinction is moot and the parent gate must be re-reviewed from 3 to 4 fields — a deviation requiring re-review), or umbrella is NOT coverage-gated (then §门与 enforcement must drop "umbrella 非空" from the coverage line, and the acceptance "umbrella 非空" check at L166/L192 must move to the depth-human-gate column only).

§⑥ (L98-100) vs §门与 enforcement (L166): consensus: "eval loop not pytest" justified by "prose skill, subjective outputs." But the spec's own eval cases — (b) pending-not-auto-adopted, (c) crack-three-elements, (d) coverage-gate-fires — are mechanically checkable (grep for `pending` after run, parse crack entries for three sub-fields, feed a missing-field scenario and verify the gate fires), and §门与 enforcement says "AI/脚本可门" (script can gate). Mechanical gates are pytest-able. The testing choice overgeneralizes: split it — pytest for any shipped coverage/gate script, eval for the prose behavior (candidate groundedness, crack quality). "Eval not pytest" pre-commits to "no gate script" without stating it, while the spec floats "脚本可门" elsewhere. The justification "prose skill 主观输出" is true for the candidate/crack generation, false for the gate mechanics.

---

**Spine-specific design decisions that hold** (not re-audited, noted as vote-of-confidence): §① staged gates + backtrack (dependency chain sound, backtrack honest); §② single rich baton (claim.md precedent apt, respects parent's "no spine folder"); §④ roles + default 1:1 (enables non-1:1 merge/split at dissect, defensible abstraction); scope boundaries (no deep-read, no paper→chapter binding, no tex/chapter-map output, no article-ledger touch — all clean); file-contract claims vs merged `thesis-init/SKILL.md` (spine reads `thesis-sources.md` + `template-spec.md` + small papers, writes `thesis-spine.md` + seeds `thesis-terminology-ledger.md` — all match init's produced placeholders at `sci-skills/skills/thesis-init/SKILL.md` L70, L116-120, L168-189).

**Score rationale**: not "Lean. Ship." The crack-pointing boundary (§⑤) is the load-bearing claim the orchestrator flagged, and it is not holdable as written — the spec's own example violates its own boundary. The umbrella reconciliation (§③) + gate contradiction (§门与 enforcement) compound the issue: the spec claims to resolve the parent's 3-vs-4 tension without deviation, but internally contradicts its own resolution and changes the parent's coverage gate. ~25 lines of spec text (the §⑤ boundary paragraph + figN-reading analogy, the §③ reconciliation paragraphs, the §门与 enforcement umbrella line, the §⑥ testing justification) need removal/replacement before ship.

---

## Round 2 verdict (re-audit of revised spec, 2026-08-25)

**net: -4 lines deletable**

Re-read revised `docs/superpowers/specs/thesis-spine.md` + parent (`thesis-skill-family.md`) + glossary. Verdict per finding, then new issues.

### Finding #1 (§⑤ tension-flagging boundary — load-bearing): GENUINELY RESOLVED.

The round-2 fix honestly bounds the residual:
- figN-reading analogy explicitly rejected (L104, L125) — false equivalence dropped.
- honest subset acknowledged as overlapping coverage/grounding (L104: "honest 子集与 coverage/grounding 机械层重叠") — not claimed as unique value.
- depth-influence named as stated failure mode (L102, L187: "不可消除的 residual... 不假装消除") — not solved, not re-labeled. The spec no longer claims crack-pointing is honest fact-checking; its named value IS the depth-influence.
- "question not verdict" form prevents verdict-FORM (auto-reject / assertion); depth-influence (including verdicts-in-costume) is the accepted residual — NOT claimed to be filtered. §⑤ and §门 (L187) are consistent: non-gating = author disposes; influence = framing bias, accepted + named.
- Pressure-test answers: (a) "name depth-influence as stated failure mode" is an honest bound, not re-labeling — the spec explicitly says it does not solve the influence problem and retains the edge (attachment absence) at the cost of the bias (L106, relative-optimum argument). (b) "question not verdict" holds as a FORM gate (prevents assertion/auto-reject); a verdict-in-costume (question form, depth content) slips through but is accepted as the named residual — not over-claimed. (c) The acceptance check (a)(b)(c)+disposition is a form check; the spec no longer claims it filters depth content.

The load-bearing premise (parent: author can judge depth) is now honestly bounded: author's judgment is the gate; the framing-bias boundary is named as failure mode, not pretended away. This is the resolution round-1 demanded (option b: drop the boundary claim, acknowledge depth-influence as failure mode).

### Finding #2 (§③ umbrella reconciliation): GLOSSARY ISSUE RESOLVED — BUT NEW LOAD-BEARING FALSEHOOD INTRODUCED.

The glossary-incompleteness (5th claim) is genuinely resolved: 主线 = thesis级claim (collapse); glossary 4 = 主线/框架/递进/共性提炼 (spine 3 + summary 1); no 5th claim. ✓

BUT the round-2 fix papers over a real parent-glossary inconsistency with a false "no deviation" claim:

`docs/superpowers/specs/thesis-spine.md:L71`: delete: "父 spec '三字段非空' = 正确" — misattribution. Parent (`thesis-skill-family.md` L190) says "四者作者确认"; L126 lists "主线+统一框架+章间递进+thesis级claim" as 4 spine-produced items. Parent never says "三字段非空" (grep-confirmed: 0 matches for 字段/三字段 in parent). "三字段非空" is the spine's OWN coverage gate (§门 L185), misattributed to the parent. Replace: "三字段非空 is spine's coverage gate (§门), not the parent's; parent's depth acceptance is '四者作者确认' (4 items), satisfied via 主线 double-duty (thread Step 1 + contribution Step 4)."

`docs/superpowers/specs/thesis-spine.md:L72`: delete: "父 spec '四者' = 不精确" — false. Parent is explicit (4 distinct items, L126 "+", L190 "四者"), not imprecise. The spine is choosing the glossary reading, not correcting a parent slip. Replace: "parent's 4-item enumeration (L126/L190) is inconsistent with glossary's 4-claim enumeration (L83: 4th = 共性提炼/summary, not thesis级claim/spine) — spine follows glossary (term authority), collapsing thesis级claim into 主线."

`docs/superpowers/specs/thesis-spine.md:L77 + L241`: delete: "非偏离 / clarification / 不改父 spec 任何已定决策" — overstated. The collapse changes parent's 4-item structure (主线/框架/递进/thesis级claim) to 3 fields (主线 double-duty). Parent L126+L190 explicitly treat 主线 and thesis级claim as distinct (4 items, "+"). The spine's collapse is a DEVIATION (siding with glossary over parent's explicit enumeration), not a clarification. Replace: "deviation from parent L126/L190 (4→3); spine follows glossary (term authority, 主线 covers thesis级claim); parent acceptance functionally satisfied (主线 double-duty: thread at Step 1 + contribution at Step 4); recommend parent re-review to align enumeration with glossary."

ROOT: parent (L126, L190: 4th = thesis级claim, spine product) and glossary (L83: 4th = 共性提炼, summary product) are inconsistent. The spine sides with the glossary silently — defensible (glossary is term authority) — but hides the deviation behind "no deviation" + a false citation. The honest move: declare the deviation, recommend parent re-review. The collapse is defensible; the justification is not.

### Finding #3 (§门 internal contradiction): GENUINELY RESOLVED.

Umbrella is gone from §门 (L184-188: coverage = "3 结构字段非空", no umbrella), schema (L137-170: no umbrella field), and acceptance (L211+: no umbrella check). grep confirms umbrella appears only in §③ (explanatory history) and rejected-alternatives (L122). No residual self-contradiction. ✓

### Finding #4 (§⑥ testing overgeneralization): GENUINELY RESOLVED.

Clean split: deterministic coverage (no pending, 3 fields non-empty, framework per-paper instantiation, progression per-role advance+question) → `scripts/check_spine.py` + stdlib pytest; prose → eval. Coverage gate is genuinely grep-able (parse Intake for paper-IDs, check Unified framework for per-paper lines; parse progression for role entries, check advance+question fields) — no interpretation required. Init precedent verified (`sci-skills/skills/thesis-init/scripts/test_init.py` exists on disk). Script lives in plugin source (`sci-skills-thesis/skills/thesis-spine/scripts/`), not project working dir — §② "spine has no dir" distinction holds (same shape as init's `scripts/`). "gate-fires-on-empty" split is clean: script's deterministic failure (pytest) vs agent's behavior of invoking-and-acting-on-it (eval). No testable surface dodged or over-claimed. ✓

### New issues introduced by round-2

- **Step 4 "main line sharpened late" (L51, L180)**: no gate-ordering problem. Step 1 settles connect-tissue (stable foundation for Step 2/3); Step 4 finalizes contribution (the "title is last" pattern, sci-story precedent). If sharpening reveals a material change, §① backtrack handles it. The main line has two settle points (candidate Step 1, finalized Step 4) — consistent with staged-gate + backtrack, not a contradiction.
- **Collapse loses nothing round-1 valued**: the contribution is still depth-gated (Step 4 sharpen + overclaim/hollow tension-flag), just folded into the 主线 field rather than a separate umbrella field. Round-1's valued items (§④ roles, scope boundaries, file-contract alignment) untouched.

### Score rationale

Not "Lean. Ship." Finding #1 (load-bearing) is genuinely resolved — honest bounding, not re-labeling. Findings #3 and #4 are cleanly resolved. But finding #2, while resolving the glossary-incompleteness, introduces a new load-bearing falsehood: the "no deviation" claim (L71, L72, L77, L241) is backed by a misattribution ("父 spec '三字段非空' = 正确" — parent says no such thing) and papers over a real parent-glossary inconsistency (parent 4th = thesis级claim; glossary 4th = 共性提炼). The collapse is defensible (glossary-aligned, functional output satisfies parent); the justification is not. ~4 lines of false §③ justification need replacement with an honest deviation declaration + parent re-review recommendation.

---

## Round 3 verdict (re-audit of reverted spec, 2026-08-25)

**Lean. Ship.**

Round 3 reverts round-2's collapse (umbrella→主线) back to umbrella = distinct depth-gated 4th field, placed in the depth bucket (not coverage — which was the round-1 self-contradiction). §⑤ (tension-flagging boundary) and §⑥ (testing split) fixes stand unchanged.

### Verification (orchestrator's 5 questions)

**1. Parent coherent under the reading?** YES. Parent says BOTH "三字段非空" (L62, L159 — coverage mechanical, 3 structural fields) AND "四者作者确认" (L190 — depth human, 4 items incl thesis级claim). Two gates on overlapping-but-different sets: coverage = {主线,框架,递进}, depth = {主线,框架,递进,thesis级claim}. Coherent.

> **Round-2 factual error on record**: round-2 finding #2 claimed "Parent never says 三字段非空 (grep-confirmed: 0 matches)" and built its load-bearing verdict on this. FALSE. grep hits L62 + L159 in the parent. Round-2's "delete: misattribution" finding was itself a misattribution — the spine correctly cited the parent, round-2 misread the parent. Round-3 revert corrects the error.

**2. Spec internally consistent?** YES. §③ (L66: umbrella = depth-gated 4th, not in coverage count) ↔ §门 (L183: coverage = 3 structural only, "umbrella 不在此层") ↔ schema (L151: umbrella "depth-gated, 非 coverage") ↔ acceptance (L213/L222/L232: umbrella in depth, not coverage). Round-1 §门 bug (umbrella listed under coverage) — GONE. §门 L183 explicitly excludes umbrella; L184 explicitly includes it in depth.

**3. "No deviation" now TRUE?** YES. Umbrella-as-depth-gated-4th matches parent's explicit 4-item enumeration (L126: "主线+统一框架+章间递进+thesis级claim"; L190: "四者"). Parent's "三字段非空" (L62/L159) = 3 structural coverage; parent's "四者" (L190) = 4 depth-confirmed. Spine produces exactly these 4 with the same gate split. No collapse, no field-count change, no parent decision rewritten.

**4. Glossary tension handling honest?** YES. Glossary L83 enumerates 4 architecture-level claims (主线/框架/递进/共性提炼), omits thesis级claim. Spec L70 + L245 names this as pre-existing glossary-parent tension, attributes it correctly (glossary = cross-spine+summary view including 共性提炼; parent = spine view including thesis级claim), declines to overclaim solving it, follows parent for spine's products. Honest bounding. Round-2's collapse was the dodge — silently absorb umbrella into 主线 to make counts work, then false-claim "no deviation" backed by a misread of the parent. Round-3 revert is the honest move: declare the 4th item, follow the parent, name the glossary gap as upstream business.

**5. New issues from revert?** NONE.
- Step 4 (L178: umbrella proposed after 3 structural fields settle) still holds — total contribution depends on structural firm-up ("title is last" pattern, sci-story precedent).
- Umbrella's depth-gate is meaningfully distinct from main line's: main line checks thread sharpness (Step 1), umbrella checks overclaim/hollow of total contribution (Step 4) — separate failure modes, separate gates. Not redundant ceremony.
- Round-1 values untouched (§① staged gates + backtrack, §② single rich baton, §④ roles + default 1:1, scope boundaries, file-contract alignment with merged `thesis-init/SKILL.md`).

### Score rationale

Lean. Ship. Round 3 corrects round-2's factual error (parent DOES say 三字段非空 — grep L62, L159) and reverts the collapse that deviated from the parent's explicit 4-item enumeration (L126/L190). The spec is now internally consistent (§③ ↔ §门 ↔ schema ↔ acceptance all align on umbrella-in-depth-bucket), genuinely deviation-free (umbrella-as-depth-gated-4th matches parent exactly), and the glossary tension is honestly bounded as pre-existing parent-glossary business with no overclaim. No new load-bearing issue introduced by the revert. The load-bearing premise (parent: author can judge depth) is defended at the right layer (depth is human-gated; AI's residual = depth-influence, named as stated failure mode per §⑤).
