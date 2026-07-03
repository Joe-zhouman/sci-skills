# sci-submit

Submission campaign manager. Not a "write a cover letter" tool — a "survive submitting the same paper fifteen times over eighteen months" tool.

## Why this exists

I submitted one paper over eighteen months. A dozen journals.

Every rejection meant opening the next submission system and re-entering everything: title, abstract, authors, affiliations, funding numbers, keywords, recommended reviewers, excluded reviewers. Then rewriting a cover letter where 90% of the content was identical to the last one — but the journal name changed, so it all had to be rebuilt.

The worst part wasn't the rejection. It was the advisor saying "no worries, next one" — without knowing that filling out one submission form takes forty minutes. Without knowing the things you can't say out loud: that the paper might not be Nature material, that the review timeline is longer than your graduation deadline, that HR doesn't recognize journals from this publisher.

You can't tell your advisor "our work isn't good enough." That doesn't work. In the hierarchy, saying "not good enough" reads as lazy, unconfident, not trying hard enough. You can't tell the big boss "your targets are wrong." You just can't.

So this skill exists. It solves three things:
1. **Write metadata once, paste everywhere** — `manuscript-meta.md` lives in your project. Not for reading — for pasting. Every submission input box maps to one code block. Things you remember get no block, things you don't (email, ORCID, grant numbers) get their own. Triple-click → Ctrl+C → Ctrl+V. Four minutes instead of forty.
2. **Track the campaign** — `submit-history.md` records every attempt, `journal-shortlist.md` manages targets
3. **Navigate hard constraints** — no sugarcoating, no pointless confrontation, just data-driven pragmatism

## Seven workflows

| Scenario | Workflow |
|---|---|
| First use — extract & organize submission metadata | **A: Metadata Setup** |
| Select journals, compare rankings, check tiers | **B: Journal Selection** |
| Submit / guided walkthrough (cover letter + page-by-page) | **C: Submission** |
| Rejected — switch to next journal | **D: Rejection & Switching** |
| Track status, follow up with editors | **E: Post-submission Tracking** |
| Proof review / galley corrections | **G: Proof Review** |
| Advisor demands, tenure requirements, hard constraints | **F: Hard Constraints & Advisor Mgmt** |

## Data sources

- **EasyScholar API**: real-time SCI/CAS分区 rankings, impact factor, early-warning list
- **CSTEE Journal Rating Directory**: offline T1/T2/T3 classifications across 59 fields (local JSON)

## Project structure

```
project/
├── manuscript.tex
├── assets/                     # Reusable submission assets
│   ├── declarations.tex        # Conflict of interest, author contributions, etc.
│   └── author-bios.tex         # Author biographies
└── sci-submit/                 # Decision files
    ├── manuscript-meta.md      # Reusable metadata + cover letter cheat sheet
    ├── hard-constraints.md     # Hard constraints
    ├── submit-history.md       # Full submission timeline
    ├── journal-shortlist.md    # Ranked targets + per-journal cover letter papers
    └── cover-letter/
        └── <journal-name>-<YYYY-MM-DD>/
            └── cover-letter.tex
```

## Human-in-the-loop

This skill is a staff officer, not a ghostwriter. It organizes information, queries data, intercepts common mistakes, and records decisions — but the human calls the shots. You know your field, your advisor, and your situation better than any model ever will.

## Feedback

If you've been through the submission meat grinder too, tell me your scenarios and pain points. This skill evolves because its requirements come from real wounds.
