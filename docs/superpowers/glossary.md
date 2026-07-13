# sci-skills Glossary

The canonical domain language for the sci-skills family (sci-draw / sci-write / future siblings + the future `using-sci-skills` orchestrator). Terms here are settled — use them verbatim in all output, never re-ask what's already defined, and never silently use an `_Avoid_` alias.

## Terms

**Family namespace (`sci-skills/`)**:
The fixed, recognizable top-level directory shared by all sci-* skills, present in every project root. Its name is the family's identity marker (analogous to how `docs/superpowers/` marks that skill family), not a per-project name. Each skill occupies one subdirectory beneath it.
_Avoid_: project folder, workspace root (too generic)

**Manuscript (`manuscript/`, first-class citizen)**:
The project's sole official manuscript, living at the project root (not under `sci-skills/`). It is the **product**; skills are **tools** that serve it. The manuscript is a first-class citizen because it often arrives from outside (Word/Overleaf/a collaborator's project) and is bigger than any one skill. Organized by **review round** (v1 / r1 / r2 ...), single dimension — never by journal or file type.
_Avoid_: the paper (ambiguous — could mean a draft), manuscript.tex (it's a project, often a directory)

**Review round (v1 / rN)**:
The single organizing dimension of `manuscript/`. `v1` = the original submitted draft (one v1 can go to many journals — most submissions are your-paper-your-way). `rN` = the Nth revision after reviewer comments on some journal; each rN is a complete package (revised tex + Response + reviews + revision cover letter). Which journal a v/r was sent to is recorded in `sci-skills/sci-submit/submit-history.md`, NOT in the manuscript directory structure. Changing journals ≠ a new v (templates rarely change); a new v is only for a genuine full template swap (rare, user's call).

**Figure warehouse**:
The agreed directory (conventionally `sci-skills/sci-draw/`, borrowing sci-draw's name for recognizability) where finished figures and their reports land, **regardless of source**. Figures may come from sci-draw, another skill, a manual tool, or a copy-paste. Downstream consumers depend only on the file contract, not on the producing tool.
_Avoid_: sci-draw directory (implies the skill owns it; the directory is neutral storage)

**paper-plan.md**:
The on-disk baton for the writing stage. Holds the figure list (one entry per figure, reusing figure-report field names) and section progress. Produced by sci-write after the human confirms the draft. The only thing that tracks "which figures are pending/drawn/written, which sections are written/external" across sessions.
_Avoid_: outline, task list

**Read neighbors, don't orchestrate**:
A skill may read another skill's on-disk outputs (sense what's ready), but must not trigger another skill to run and must not assume a specific tool produced the outputs. Sensing (a read) is allowed; calling (triggering execution) is reserved for the human or for the future `using-sci-skills` orchestrator.
_Avoid_: coordinate skills, dispatch skills

**Contract gap**:
A condition where an on-disk file (e.g. a figure report) exists but is missing a required field or has a malformed one. Handled by: stop, list the gap, ask the human to fill — never fabricate the missing content, never skip the file. The filled content is written back and becomes part of the contract.
_Avoid_: validation error, schema violation (those imply rejection; a gap is a fillable hole)

**Real-DOI placeholder**:
A citation placeholder carrying a real DOI (or other verifiable identifier) found by the skill's search MCP — never an empty `[CITE:?]`, never a fabricated bibliography entry. The human performs the final Zotero/Endnote insertion from these placeholders.
_Avoid_: citation, reference (too general — these don't specify the real-DOI + human-inserts contract)

**Figure status (`pending` / `drawn` / `written`)**:
The three-state lifecycle of a figure entry in paper-plan.md. `pending` = planned, not yet drawn; `drawn` = report exists in the warehouse; `written` = prose referencing it is drafted.

**Section status (`pending` / `written` / `external`)**:
The lifecycle of a manuscript section. `pending` = not drafted; `written` = on disk; `external` = out of scope for sci-write (Introduction / Abstract / Keyword), handed off to another mode of work.

**figN-reading.md**:
The per-figure consistency-check record produced by sci-write's Step 3. Compares the report's `Core conclusion` against what the `paper-figure` vision action independently reads from the rendered PNG. Holds the soft claim-correction suggestion and any contract supplements.
_Avoid_: figure analysis (ambiguous — could mean the vision tool's output or the comparison)

## Relationships

- A **Family namespace** contains one **Figure warehouse** and one home directory per skill (e.g. `sci-write/`).
- A **paper-plan.md** lists many figure entries, each in a **Figure status**; and many section entries, each in a **Section status**.
- A figure entry's `claim` field ↔ that figure's report `Core conclusion` (plan = intended, report = demonstrated).
- A **figN-reading.md** references exactly one figure report and is consumed by Results/Discussion drafting.
- A **Real-DOI placeholder** appears inside section prose; its final insertion is performed by the human, never by a skill.
- **Read neighbors, don't orchestrate** governs every cross-file/cross-skill interaction in the family.

## Flagged ambiguities

- "sci-draw/" is used two ways: (a) the **Figure warehouse** directory (neutral storage, name borrowed for recognizability), and (b) loosely, "what sci-draw the skill produces." Resolved: when referring to the directory as a contract surface, call it the **Figure warehouse**; reserve "sci-draw" (no slash) for the skill itself.
- "检索" (retrieval/search) was initially treated as out-of-scope for sci-write (reason to offload Introduction). Resolved: search is **in-scope** (the user has a search MCP); what's offloaded is Introduction/Abstract/Keyword for **writing-nature** reasons (global narrative + reverse order), not search reasons. Real-DOI placeholders are produced inside sci-write.
- "Orchestration" was conflated with "coordination." Resolved: **no skill in this family orchestrates others.** Each skill reads neighbors' on-disk outputs, never calls another skill. Cross-skill orchestration is **not a fixed skill** — it's done at runtime by the harness (workflow/loop) or by the human deciding what to run next. `sci-skills-init` is just the skill that happens to do setup (init + checkup), not an "orchestrator layer" above the others. There is no two-layer family structure; all skills are equal, loosely-coupled parts.
- **The real stance: decoupled single-purpose skills (Matt Pocock style) > thick-orchestration skills (superpowers style), and the gap will widen.** Thick orchestration (a skill with a heavy built-in multi-stage process chain) is a hedge against weak models and poor harness — it bakes runtime decisions into compile-time scaffolding. As model capability and harness features (workflow, loop, Explore, MCP) improve, that scaffolding becomes redundant overhead: a strong model under light directory contracts can do at runtime what a thick skill hardcodes. So this family's direction is **lightweight, single-responsibility skills that mesh via directory contracts**, with orchestration deferred to the harness at runtime (workflow/loop) or to the human — never baked into a skill. The earlier framing ("two layers, an orchestrator skill for auto users") is deprecated; it was a transitional thought, not the destination.
- **Why decoupling is a survival strategy, not a tidiness preference.** The research-skills ecosystem is crowded and fragmented — everyone has their own taste in writing style, plotting tools, and workflow. Tightly-coupled "full-suite" skills force all-or-nothing adoption and end up used by no one. This family's bet is the opposite: each skill is an **independently replaceable part** that interconnects via **directory contracts** (the `.README.md` per subdirectory), not via code imports. A user can mix ours with someone else's plotting tool and manual submission — as long as the `sci-skills/` directory contracts are honored, the parts mesh. **A part that cooperates with others beats a self-consistent but closed suite.** This is why the directory `.README.md` files are contracts (any agent/skill producing into a directory follows them without needing to know which skill consumes it), and why "read neighbors, don't orchestrate" is non-negotiable.
