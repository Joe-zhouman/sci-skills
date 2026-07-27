# self-check.md — the audit before sending

> Read this at phase 4 (after drafting, before reporting done). The checks that
> enforce the first principle (self-containment) and the hard rules at the
> document level. None of these auto-approve sending — they surface problems for
> the author to fix (meta-rule: the human decides).

Run all four checks, then compile. **Do not report done until compile + searches
pass in the current session** — a stale "done" from an earlier session doesn't
count.

### Deterministic checks first (run the script)
The mechanical part of the search checklist is a script — run it before the
semantic checks. It catches what a human/agent would miss by eye:

```bash
python scripts/check_response.py manuscript/rN/response/response-rN.tex
```

Reports: comment/response pairing, leftover placeholders (`[TBD]`/TODO/INSERT),
bare `\textcolor` outside `changes`/caption (should be `\added`/`\deleted`),
acknowledgement-phrase count, banned-qualifier hits, float specifiers (must be
non-floating), cover-page fields. Each flagged item is a concrete fix; the
"note" field says what to do. Semantic checks below handle what the script
cannot (coverage intent, tone, self-containment of each response).

---

## 1. Coverage audit — every concern accounted for

Every reviewer comment must map to a response state. No silent dropping.

For each issue in the ledger, its `status` must be one of:
- `drafted` — has a response in the letter
- `covered_by_global` — addressed by the overview / a shared response (cite it)
- `deferred_with_reason` — intentionally not answered, **with a stated reason**
- `needs_user_input` — blocked on the author (flag, don't hide)

The key state is `deferred_with_reason`: you may choose not to answer a concern,
but you must say *why* (in the response or the ledger). Silent omission is the
failure mode — a reviewer whose comment vanished will notice.

**Check:** list every issue ID from every reviewer. Confirm each has a response
state. Any `analyzed`/`draft-ready` without `drafted` or an explicit
`deferred_with_reason` → flag.

Multi-reviewer overlap: if R1 and R2 raised the same concern (merged ID like
`R1-Q03, R2-Q01`), confirm the single response cites both reviewer IDs.

---

## 2. Integrity firewall — banned rebuttal moves

A short, explicit table of moves the response must not make. Check each response
against it; hits get deleted or rewritten. Adapted from Meet-Reviewer-2's
H1–H17 fairness firewall pattern.

| Banned move | Why | Fix |
|---|---|---|
| "The reviewer didn't read carefully" / "As we already stated" | attacks the reviewer, signals defensiveness | restate the point neutrally; the reviewer's misread is your writing's fault to fix |
| speculating about the reviewer's motives | unprofessional, unprovable | address the comment, not the commenter |
| "You misunderstood" as a dismissal | even if true, it's not an answer | clarify the point; if the writing caused the misunderstanding, fix the manuscript |
| attacking the reviewer's tone | escalates | stay on the substance |
| burying the direct answer under background | wastes the reviewer's time | first sentence = the answer |
| overstating the fix ("completely resolved") when it's partial | dishonest | state exactly what was done and what remains |
| hidden placeholders / "will add later" in the final text | not ready to send | replace with real content or `[TBD]` (visible) |
| claiming an experiment was run when it wasn't | fabrication | mark unrun experiments as planned/deferred; use conditional wording |
| manufacturing positive reviewer statements that weren't made | dishonest | quote/paraphrase only what was actually said |

**Check:** scan every response for these patterns. The integrity check is
especially important for the 🔴 core responses, where defensiveness creeps in.

---

## 3. Independent-reviewer read — the self-containment test

This is the operational test of the first principle. Full subagent orchestration
is overkill; a single focused pass suffices.

**The test:** read the response letter *as if you have never seen the original
reviews or the manuscript*. For each response, ask:
- What is the reviewer's concern? (Can you tell from the response alone?)
- What is the answer?
- Is the evidence sufficient to judge the answer without opening the manuscript?
- What's still unclear?

If a response fails any of these — the reviewer would have to flip to the
manuscript — it's not self-contained. Flag it; the author adds the missing
evidence (a Response Figure, the quoted sentence, the data).

This is the cheapest, highest-value check. It directly measures the first
principle. Run it on every response, especially the 🔴 and 🟡 ones.

---

## 4. Final search checklist

Run these searches on the response tex before compile. Each catches a specific
failure mode. (Adapted from response-skill's final search checklist; trimmed to
our scope.)

Search for:
1. **template phrases** — leftover instruction text ("INSERT RESPONSE HERE",
   boilerplate the skill emitted but didn't fill)
2. **placeholder brackets** — `[TBD]`, `[???]`, `<...>` — confirm each `[TBD]` is
   intentional and the author knows to fill it; remove anything else
3. **planning language** — "later", "to be added", "we will", "TODO", "FIXME"
   (conditional "we will add" is fine *only* if the venue allows promised
   revisions; otherwise it's not ready)
4. **stale location citations** — page/line refs that may have shifted if the
   manuscript was edited since the response was drafted (re-verify per
   `latex-response.md` §4)
5. **color inconsistencies** — `\added`/`\deleted` used outside a `changes`
   block, or raw `\textcolor` that should be a macro; Response Figure captions
   colored correctly
6. **over-thanking** — acknowledgements on typo/clarify responses, or
   acknowledgement openers that repeat across responses (rule 3)
7. **banned qualifiers without evidence** — "improves / outperforms /
   significant / robust / SOTA" not backed by a metric in the same response
   (rule 2)

### Acknowledgement-restraint lint (concrete)
For each response, weigh acknowledgement count against the response's weight:
- typo / clarify → 0 acknowledgement sentences (the redline block is the answer)
- data-backed / concede → ≤ 1 short acknowledgement line, at the end
- the canonical failure: any form of "We sincerely appreciate your meticulous…"
  on a non-substantive response → delete

---

## After the checks pass — compile

Once all four checks pass (issues fixed, not just flagged), compile per
`latex-response.md` §4, in this session:
```bash
pdflatex -interaction=nonstopmode -halt-on-error response-rN.tex
# (+ bibtex + 2 more pdflatex passes if bibliography is used)
```
Visually inspect the PDF:
- cover page renders cleanly (3 fields, no identity leakage)
- Response Figures sit beside their discussing paragraph (non-floating, as-is)
- redline colors render (green adds, red strikethrough deletes)
- no overflow, no broken refs

Only then report done. The compiled PDF + the audited ledger are the deliverable.

---

## What these checks do NOT do

- **They do not approve sending.** The author decides. The checks surface
  problems; they don't green-light submission. (Meta-rule.)
- **They do not auto-rank or auto-reorder issues.** The ledger's order is the
  author's. (The P0–P3 scoring from the survey was demoted — it decides for the
  human.)
- **They do not promise the response will satisfy the reviewer.** They promise
  it is self-contained, honest, and restrained. Whether it convinces is beyond a
  skill's scope.
