# Phrasebank — framing tactics, in words

> **A phrasebank is not a substitute for deciding what the response is trying
> to do.** Decide the strategy (writing-rules.md §framing-freedom, A–G) first;
> then come here for the words. Loading this before the strategy is decided is
> a misuse — you'll pick a phrase and rationalize a strategy to fit it.

This phrasebank is deliberately **asymmetric**: it collects **framing phrasing**
(how to reframe scope, minimize a limitation, decline an experiment politely),
not honesty phrasing. Honesty doesn't need a phrasebank — state the fact, in
plain words, and you're done. The hard part, the part that needs rehearsed
words, is the framing layer. That's what's here. A small "honesty" appendix at
the end covers only the high-frequency cases that are easy to get wrong (e.g.
correcting a reviewer's misread without implying they didn't read).

Every phrase carries **when to use it** and **the line it must not cross** (the
honesty floor from SKILL.md rule 2). A phrase that requires an untrue statement
is not in this bank.

## How to use this bank — not a fill-in-the-blank

These are **fragments**, not templates. Do not paste them whole. Adapt the
wording to the specific fact of the response; if two responses end up with the
same opener, rewrite one (anti-AI-pattern rule, writing-rules.md rule 3). The
fragments exist to give a non-native or time-pressed author a *starting shape*
that has worked in real accepted letters — they are not a substitute for
judgment.

Provenance: phrases marked *(sample)* come from `assets/Response Letter#1.pdf`
— a real, accepted revision. Those marked *(public)* come from open
peer-review files or writing guides (collected separately). Those marked
*(TBD-accumulate)* are placeholders to fill as the skill is used on real rounds.

---

## A. Reframe claim scope

*Shrink the claim so the reviewer's point lands outside it — without conceding
the claim is wrong.*

- "While [reviewer's broader point] is a valuable direction, our claim in this
  work is specifically scoped to [narrow setting], where [evidence] holds."
  *(TBD-accumulate)*
- "We contend that this [discrepancy / limitation] — [one-line characterization]
  — **does not undermine the core conclusions** of this paper." *(sample, R1-Q4)*
  - *Use when:* the reviewer found a real imprecision, but the central claim
    survives it.
  - *Line:* "core conclusions" must actually survive. If the imprecision
    invalidates the headline claim, this phrase is a lie — use B (concede)
    instead.

## B. Minimize a limitation

*Acknowledge the limitation, then shrink its apparent impact (future work /
low cost / modular extension / inherent to the method).*

- "This [limitation] is [inherent to / a known characteristic of] [method], and
  is discussed in the [Discussion / Limitations] section." *(sample, R1-Q6/R2-Q6)*
  - *Use when:* the limitation is real and unfixable, but legitimately sits
    within the paper's scope boundaries.
- "The costs associated with [fixing it] are **manageable within practical
  engineering contexts**." *(sample, R1-Q6)*
- "[fix] would require [resource]; the **modular design** of our approach allows
  for **systematic extension** to include [it] in future studies." *(sample, R1-Q6)*
- "Our claim is **limited to** [scope], where [evidence] supports [claim]."
  *(public)*
  - *Line:* the limitation must be *stated*, not hidden. Minimizing impact is
    legitimate; pretending it doesn't exist is not.

## C. Selective emphasis

*Lead with the favorable number; bury the weak comparison in a subordinate
clause or move it to SI.*

- "Following this concern, we [ran the comparison / computed X]: [strong number]
  [condition]." — the strong number leads; the qualifier ("under setting Y";
  "for the main metric") follows in a clause. *(sample shape, R2-Q5 "25,200×
  acceleration")*
- "Sec. X **reports** [favorable result]; [weaker result] is provided in
  Supplementary [N] for completeness." *(sample shape, R1-Q11 divert)*
  - *Line:* the weak point must be *answerable* if pressed. You're choosing what
    to highlight, not what to fabricate.

## D. Divert to SI

*Move weak evidence, edge cases, and supplementary validations into the SI,
keeping the main text clean.*

- "For completeness, we have moved [weak/edge content] to Supplementary [Figure
  / Discussion] [N]." *(sample, R1-Q10/Q11)*
- "Considering these results serve as supplementary validations to our core
  predictive findings, we have relocated [them] to Supplementary [N]." *(sample,
  R1-Q11)*
  - *Line:* SI is not a graveyard for disconfirming evidence. Detail moves; a
    result that contradicts the claim does not get hidden in SI.

## E. Fill the gap with an external reference

*When the reviewer exposes a gap, fill it with an existing citation (including
your own preprint) rather than admitting the gap is empty.*

- "To the best of our knowledge, there are no existing [models / works] that
  [address X]. To address this gap, our [ongoing research / preprint] [does Y]."
  *(sample, R1-Q12)*
- "We have added a comparative analysis between [our approach] and [the
  cited method], shown in [Figure / Table]." *(sample, R1-Q12 / R2-Q2)*
  - *Line:* the cited work must exist and say roughly what you claim. Citing a
    paper you haven't read is fabrication.

## F. Offer an exit (concede the marginal to save the core)

*When a peripheral element is hard to defend, offer to remove it — this
protects the core by sacrificing the edge, and signals reasonableness.*

- "If the reviewer [prefers / believes that only X should be included], **we
  are happy to remove** [the peripheral element]; [it] would be [moved to
  Supplementary / discussed in the supplement]." *(sample, R2-Q6)*
  - *Line:* the offered concession must be *genuine* — if the reviewer says
    "yes, remove it," the author will actually remove it.

## G. Exploit reviewer misunderstanding (use with care — Class B)

*When a reviewer misreads the paper in a way that flatters it, you have no duty
to correct the misread within the honesty floor. But do not compound it.*

- (No template — by construction this is the tactic closest to the line, and
  the right move is usually *silence*: address only what needs addressing, do
  not volunteer a correction, and do not write text that deepens the false
  impression.)
- *Surface at the checkpoint:* this is always a Class-B decision (workflow.md
  §3). The skill flags it; the author decides whether to leave the favorable
  misreading alone.
  - *Line:* silence (not correcting) is legitimate; active deception (writing
    something that reinforces the error) is not.

---

## Honesty appendix — only the cases that are easy to get wrong

*These are not "framing." They're plain honesty, but the wording is easy to
fumble. Included only because they come up constantly and a wrong phrasing
sounds rude or evasive.*

### Correcting a reviewer's misread without implying they didn't read
- "We apologize for the lack of clarity; the paper currently states [quote]."
  *(public)* — blames the *writing*, not the reader.
- "We clarify that [precise point]. In the submitted paper, [anchor] shows
  [evidence]." *(public)*
- Avoid: "As we already stated…", "The reviewer may have missed…", "Contrary to
  the reviewer's claim…" — these attack the reviewer and signal defensiveness.

### Stating a result that is genuinely weaker than hoped
- "[Result] supports [bounded conclusion]." — "supports," not "proves."
- "These values are theoretical estimates and have not been experimentally
  validated; they should be interpreted with caution." *(sample, R1-Q9)*
  - This honesty is also a *frame* (lowers the weight on a weak data point) —
    but it's honest first, frame second.

### Banned qualifiers (no metric, no use)
"improves / outperforms / significant / robust / SOTA / superior / prove /
guarantee" — unless backed by the specific metric in the same response.

---

## TODO — what this bank still needs

- **Public sources are mostly empty for framing phrasing.** A sweep of open
  resources (GitHub's ~24 `response-to-reviewers` template repos, public
  peer-review files, writing guides) found only **LaTeX skeleton templates** —
  empty `\begin{revcomment}...\end{revresponse}` scaffolds, not wording. The
  open world avoids the framing layer (same avoidance the stance section calls
  out): everyone teaches honesty phrasing, no one teaches "how to make a
  weakness sound small." So this bank does **not** rely on external corpora —
  it relies on the two sources that actually carry framing wording:
  1. **(sample)** — real accepted letters from the author (Response Letter#1
     contributed the R1-Q4/Q6/Q9, R2-Q6 phrases above).
  2. **(TBD-accumulate)** — phrases that worked in real rounds the skill is
     used on. When a framing phrase lands well, add it with provenance. This is
     a living file; it thickens with use, not with scraping.
- **If the author has access to a paid/curated source** (e.g. 科研者之家's
  review reference library, journal-specific phrase collections), those can
  populate this bank faster than accumulation — hand them over and they get
  vetted and merged per category. But the skill does not depend on them.
- Chinese-journal phrasing (中文期刊修改说明话术): currently absent. If the
  author works on Chinese-journal revisions, a 中文 phrasebank section is needed
  — defer until there's a real Chinese round to source from.

---

## Inbox — raw phrases before they're vetted into A–G above

> **This is the low-friction drop zone.** When the author reads a post / a
> colleague's response / a public review file and spots a framing phrase worth
> keeping, drop it here as-is — no categorization, no polishing. Just three
> fields: where it came from, the original wording, and a one-line guess at
> which tactic (A–G) it serves. Every few rounds, the skill (or author) vets
> these and promotes the good ones into the structured sections above; the rest
> get cut. **Don't let a good phrase die because categorizing it is work —
> paste it raw here and sort later.**

Format (loose — just have the three bits):
```
- from: <URL / 论坛帖子 / 同事的信 / 哪本期刊公开的 review>
  original: "<the wording, verbatim, in whatever language>"
  guess: <A-G tactic, or "unclear">
  note: <optional — what situation it fit>
```

<!-- 累积条目贴在下面这个列表里。空着没关系,等刷到再贴。 -->

- _(empty — first entry here)_

