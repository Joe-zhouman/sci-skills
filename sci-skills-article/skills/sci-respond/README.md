# sci-respond

Response-to-Reviewers letter, for a revision round. Not a "fill in a thank-you template" tool — a "get this paper accepted within the honesty floor" tool.

## Why this exists

I had a paper rejected, then major-revised, then minor-revised, then accepted — across a long stretch where I learned that writing the response letter is nothing like writing the paper.

The paper is written for a reader who *wants* to understand. The response letter is written for a reader who *already doubts you* — a reviewer who spent hours finding weaknesses, and now watches closely whether you actually addressed them or danced around. Every sentence is read adversarially. A response that says "we have addressed this" without showing *exactly* how sends the reviewer straight back to the manuscript to check — and now they're irritated.

And there's the part nobody puts in writing guides. Some of what the reviewer asks for, you genuinely cannot do — the equipment, the time, the sample, the budget isn't there. The honest answer is "we can't, because [reason]." But the honest answer, said wrong, reads as "we did weak work." Said right, the same fact reads as "this is a known boundary of the method, scoped to where the evidence holds." Same truth, different outcome. That gap — between the fact and how the fact lands — is the entire craft of a response letter. Most skills avoid it because it sounds like dishonesty. I needed it spelled out.

So this skill exists. Three things it does:

1. **Every response is self-contained.** The reviewer never has to flip back to the manuscript. Each response carries its own evidence — a quoted revised sentence, a Response Figure beside the text, or the data plus a precise location. A response that sends the reviewer digging is a failed response.
2. **A checkpoint before drafting.** The skill decomposes every reviewer comment into a stable issue ledger, surfaces the underlying concern (not the literal ask), and stops. For each consequential issue it lays out 2–4 strategies with tradeoffs. You pick. Nothing is drafted before you decide — because the decision (defend or concede, narrow the claim or hold firm, run the experiment or cite existing evidence) is the one only you can make.
3. **Framing is craft, within the honesty floor.** No fabricated data, no fake citations, no "we ran experiments we didn't" — the floor is hard. But above the floor: reframe scope, minimize a limitation, divert weakness to SI, exploit a reviewer's favorable misunderstanding. These are legitimate, expected, and the skill teaches them by name (A–G) instead of pretending they don't exist. The goal is acceptance; honesty is the floor it stands on, not the ceiling it bows to.

## Who this is for

Not the author whose position is privileged — good school, good data, an advisor who mapped the path. For them, "present it honestly" is the optimal strategy, because their work is strong enough that honesty alone carries it. Their skills can treat honesty as the top principle.

This skill is for the author whose position is **not** privileged — ordinary school, ordinary resources, work that is sometimes only ordinary because the conditions allow no better. That is not an attitude problem; it is a reality. Under that reality, an honestly-presented ordinary submission gets killed by standards set for stronger work. So every tactic here exists to give ordinary work its fair chance at acceptance, within honest limits. The 黄药师 choice, not the 全真教 — positional, not moral. (See the family README's "Who this is for" section for the longer version.)

## How it works

Four phases per revision round. Details in `SKILL.md` + `references/`.

1. **Intake** — `scripts/scan_neighbor.py` senses the grounding (reviews, manuscript tex, the writing-stage notes from sci-write, the figure reports from sci-draw, the existing issue-ledger) and reports what's present and what's missing. Read its output before reading any individual file.
2. **Issue decomposition + checkpoint** — every reviewer comment gets a stable ID (`R1-Q03`), an underlying concern, a proposed strategy, a safe-claim-boundary. The skill presents the ledger and **stops**. You lock the strategies. Nothing is drafted before this pause.
3. **Draft** — write `response.tex` directly (tex, not Word — precise layout; Word via pandoc only if you insist, and you fix what pandoc can't place). Cover page (three double-blind-safe fields), point-by-point responses in substance-first order (facts → evidence → stance → landing → optional thanks at the end). Typo/clarification responses use inline redline (`\added`/`\deleted`); Response Figures are non-floating (as-is, no drift).
4. **Self-check + compile** — `scripts/check_response.py` runs the deterministic checks (comment/response pairing, leftover placeholders, bare `\textcolor`, acknowledgement count, banned qualifiers, float specifiers, cover fields). Then the semantic checks (coverage audit, integrity firewall, independent-reviewer read). Compile to PDF in the same session.

## The phrasebank flywheel

`references/phrasebank.md` is a living file. The hard part of response-writing — the *framing* phrasing (how to reframe scope, minimize a limitation, decline an experiment politely) — is not in public corpora. A sweep of open resources (GitHub response-template repos, writing guides) found only empty LaTeX skeletons and honesty phrasing; the framing layer is universally avoided. So this bank grows from two real sources:

1. **Your own published response letters** — drop each as `assets/samples/<Author>-<Year>-<journal>/` (PDF + text `.md`). `scripts/extract_phrases.py` mines it for framing phrases (sentence + source + A–G guess) and emits Inbox-ready entries.
2. **Phrases you spot in posts / colleagues' letters / public review files** — paste raw into the Inbox, sort later.

Every accepted letter thickens the bank, which makes the next letter easier, which feeds the bank again. Left foot steps on right foot.

The samples directory (`assets/samples/INDEX.md`) doubles as a **showcase** — each entry links the published paper's DOI so anyone can verify the letter worked. Proof, not claim.

## What this skill is NOT

- **Editing the manuscript tex** per the locked decisions → that is `sci-revise` (surgical edits; this skill only writes the `revision_kind` field that drives it).
- **Polishing manuscript prose** → `sci-polish`.
- **Cover letters** → `sci-submit`.
- **Drawing data figures** → `sci-draw`.

## Status

Design complete (`docs/design-note.md` records every decision and its why, including the framing layer that most skills avoid). Skeleton + scripts + tests + one real sample (`Zhou-2025-commeng` — Communications Engineering, DOI 10.1038/s44172-025-00508-0). The phrasebank is thin until more rounds run through it — by design, it thickens with use.

## Feedback

If you've written response letters under less-than-ideal conditions and hit patterns this skill misses, tell me. The framing tactics and the phrasebank evolve from real rounds, not from guessing what authors need.
