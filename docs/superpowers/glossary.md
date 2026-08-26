# sci-skills Glossary

The canonical domain language for the sci-skills family (sci-draw / sci-write / sci-submit / sci-skills-init / future siblings). Terms here are settled — use them verbatim in all output, never re-ask what's already defined, and never silently use an `_Avoid_` alias.

## Family principles (above the terms — these constrain every design decision)

- **No Save, No Safe.** Important content must land on disk. Conversations and context windows are ephemeral; real research work spans days/weeks/months and must survive across sessions. Anything that lives only in a conversation is unsafe — it can vanish on truncation, summary, or session end. This is why every decision, contract, intermediate state, and artifact in this family is a file (paper-plan, figN-report, figN-reading, manuscript/, hard-constraints, the `CONTRACT.md` contracts, this glossary). **Test for any "important" thing: is it on disk? If not, it's unsafe — write it.** File handoff is also what makes the workflow isomorphic to real work (advisor reads your PDF, editor receives your tex, a collaborator edits your docx) — output flows directly into real processes instead of needing "translation" out of a chat.
- **Three-entry architecture, driven by the capability/price tradeoff.** The family is not "execution skills vs orchestrator" or "decoupled will replace orchestration." It has three distinct entry points, each serving a different model/price regime:
  - **sci-skills-init** — scaffolds the workspace (dirs + contracts + checkup). Mechanical; cheap models do it fine.
  - **Execution skills** (sci-draw / sci-write / sci-submit ...) — each produces one kind of artifact, meshes via directory contracts. Pick the model by task (writing needs strong, plotting-judgment needs strong).
  - **using-sci-skills / auto-research** (a thick-orchestration entry, name is unimportant) — chains multiple skills into an end-to-end flow for the **cheap-model + high-volume** regime. Cheap-but-fast models (e.g. paratera/ds-v4-flash) need "automatic gear-shifting" (变频) baked into the orchestrator to compensate for lower capability — strict checkpoints, fixed stage order, heavier scaffolding. Strong/expensive models don't need this entry; they orchestrate themselves under light contracts at runtime.
  Thick orchestration is **not a transitional form to be replaced** — the capability/price tradeoff is permanent, so cheap models (and thus the thick-orchestration entry that compensates for them) are permanent too. What's deprecated is only **baking orchestration into execution skills** — execution skills stay lightweight and single-purpose so both strong models (using them directly) and the thick-orchestration entry (chaining them) can use the same parts.
- **Contracts over imports.** Skills interconnect via on-disk directory contracts (`CONTRACT.md` per subdirectory, visible so external producers can discover them), never via code imports. A skill producing into a directory follows its contract without knowing which skill consumes it. This is what makes skills independently replaceable — the survival strategy in a crowded ecosystem.
- **Capability over tool.** A skill declares the **capability** it needs, not the specific tool that provides it. sci-write Step 3 needs *image understanding*, not "seed-viz paper-figure" — any vision tool or vision-capable model satisfies it. sci-write reads a *figure warehouse*, not "sci-draw's output" — figures from any source are equal. The manuscript is *the official manuscript*, not "what sci-write produced." Same pattern everywhere: state what capability/source the skill depends on; let the concrete tool be chosen at call time. This is the same shape as Contracts-over-imports (the contract is the stable surface; the implementation is the replaceable surface) — applied to external tools and data sources, not just sibling skills. **Test: does the skill break if its named tool is swapped for an equivalent? If yes, it's hardcoded — abstract to the capability.**

## Terms

**Thesis (`thesis/`, first-class citizen)**:
The degree-thesis artifact, living at the project root parallel to `manuscript/` (not under `sci-skills/`). Organized by **chapter** (Ch1 绪论 / Ch2 共用理论方法 / ChN 各小论文重构章 / 总结展望), not by review round — this is what distinguishes it from `manuscript/`. The thesis is the **product**; the thesis skill is a **tool** that serves it. **Input small papers are read, never absorbed** — a thesis skill *reads* `manuscript/vN/` or external paper tex/PDF as intake; it does not move them in or rewrite them. The thesis has its own lifecycle (开题 → 中期 → 盲审 → 答辩), distinct from a manuscript's review-round lifecycle.
_Avoid_: manuscript (that's the journal-paper artifact, organized by review round), the dissertation (too generic)

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
- A **Thesis** is a distinct first-class artifact from a **Manuscript**: organized by chapter (not review round), built by *reading* small papers as intake (not absorbing them), with its own degree-thesis lifecycle. A thesis skill reads `manuscript/vN/` or external papers; it never moves or rewrites them.
- A thesis family is a **sibling family** to the article family, mirroring its compass-file coupling: its own entry skill (`thesis-init`, the only node knowing all siblings) + execution skills that interconnect via `thesis/` directory contracts, not code imports. An **architecture-level claim** (main line / unified framework / progression / common-extraction) is the thesis's analog of an article's citation-level claim — but one stratum higher, and author-articulated not AI-generated.
- A **paper-plan.md** lists many figure entries, each in a **Figure status**; and many section entries, each in a **Section status**.
- A figure entry's `claim` field ↔ that figure's report `Core conclusion` (plan = intended, report = demonstrated).
- A **figN-reading.md** references exactly one figure report and is consumed by Results/Discussion drafting.
- A **Real-DOI placeholder** appears inside section prose; its final insertion is performed by the human, never by a skill.
- **Read neighbors, don't orchestrate** governs every cross-file/cross-skill interaction in the family.

**Compass file (罗盘文件)**:
The on-disk artifacts that couple a skill family without code imports: (a) the entry skill's init script carrying `BROTHER_SKILLS` (the routing table of which skills exist) + `SKILL_DIR_CONTRACTS` (the CONTRACT.md text per shared directory) + the first-class artifact's contract; (b) each shared directory's visible `CONTRACT.md` (the interface spec + on-ramp for outside producers); (c) `family-layout.md` (the depth reference for evolving the family). The entry skill is the **only** node that knows about all siblings; every other skill knows only files. This is "read neighbors, don't orchestrate" made concrete.
_Avoid_: config, index file (too generic), orchestrator (that's a posture, not the file)

**拆即写 (dissect-is-write)**:
The thesis-dissect discipline: when dissecting a small paper into a thesis chapter, the chapter tex is written *in the same pass*, because the logic is already clear at dissection time — separating the two would mean reloading the just-traced logic. Made clean by tex's one-chapter-one-file property. Dissect is not two responsibilities forced together (structure-judgment + writing); they are two faces of one act.
_Avoid_: outline-then-fill (implies separate write step — loses the just-traced logic)

**Architecture-level claim**:
A claim at the thesis's structural level, not the citation level: the **main line (主线)**, the **unified framework (统一框架)**, **inter-chapter progression (章间递进)**, and the **common-extraction (共性提炼)**. These are the failure-prone points where AI generates plausible-but-empty frameworks or invented commonalities. Unlike citation-level claims, an AI **cannot honestly audit these** — checking "is this framework deep or hollow" produces the very shallowness it's checking. So architecture-level claims are **author-articulated, human-gated**: the author grounds them in the actual content of the small papers; AI may propose candidate materials, decompose the logic, and examine from a dispassionate angle (pointing at cracks the author's attachment hides), but **AI never gates architecture-level decisions and never auto-adopts a candidate**. Enforcement = mandatory human review at each critical stage, with files-on-disk as the audit surface (the human reads `spine.md` / `chapter-map.md` / `synthesis.md`, not chat context).
_Avoid_: claim (too general — "claim" is the citation/sentence-level thing; architecture-level is a distinct, higher stratum)

**Citation-level vs architecture-level (the enforcement split)**:
The thesis's claim strata take *different* enforcement by design, in three layers not two. **Citation-level** (a sentence cites a source that must actually support it) is fully *mechanical* — resolve the DOI, fetch the source, locate the passage — so AI/schema hard-gates are legitimate here (tez-atif-dogrulama `allOf` if/then, real-DOI placeholders). **Architecture coverage/grounding** (was a gap filled by a later chapter? is the common-extraction grounded in specific chapter results? does each chapter declare how it instantiates the unified framework?) is *also mechanical* — a script/agent can check these against on-disk files; the spec's own gates live here. **Architecture depth** (is the framework high-level enough? is the common-extraction insightful? is the main line sharp?) is *not mechanical* — an AI gate would generate plausible confirmations of the very shallowness it checks — so it is **human-gated only**, AI assisting (propose candidates marked `pending`, decompose logic, dispassionate crack-pointing). Conflating depth with coverage (letting an AI gate framework depth because it can gate coverage) is the core anti-pattern this family refuses.
_Avoid_: gate, validation (too generic — must always specify which layer)

**Narrative gap (研究现状 gap)**:
The research-status **断层** (structural mismatch, not literature 空白) that thesis-intro articulates in the 绪论 — "what the field lacks that body chapter N fills." Distinct from spine's **inter-chapter progression role-question** ("how does chN advance the main line" — structural, already recorded in chapter-map.md) and from an **architecture-level claim** (depth-gated upstream in thesis-spine.md): a narrative gap is *narrative-craft*, not architecture-depth — its depth is enforced via the per-section confirmation gate + prose eval (not a human architecture-depth gate, because architecture depth was settled in spine and intro only narrates it). intro records each narrative gap **post-write** in `gap-map.md` (the intro→summary baton, mirroring dissect's write-then-record chapter-map.md discipline); thesis-summary callbacks each. Typically one per body chapter. The family spec's intro gate ("每个 gap→某章填了") refers to this.
_Avoid_: gap (too generic — must specify narrative vs structural), research gap (implies literature 空白, the `_Avoid_` of 断层)

**Serves-the-author-first (family stance for the thesis family)**:
A thesis skill is built for **an author who has understanding and thinking about their own work** — not for a novice ("白丁"). It scaffolds the author's own top-tier vision and first-principles reasoning; it does not generate the thinking for someone who hasn't done it. The test: if a skill can't serve the author who built it (please yourself), it can't serve anyone. Direct consequence: AI's role is *assistive* — provide materials, decompose logic, dispassionate examination — never substitute for the author's judgment at architecture-level stages. This stance shapes tone (assume competence, don't hand-hold) and intake (the author brings genuine understanding; the skill doesn't manufacture it).
_Avoid_: beginner-friendly, general-purpose (these pull toward generating-for-a-novice, the opposite of the stance)

## Flagged ambiguities

- "sci-draw/" is used two ways: (a) the **Figure warehouse** directory (neutral storage, name borrowed for recognizability), and (b) loosely, "what sci-draw the skill produces." Resolved: when referring to the directory as a contract surface, call it the **Figure warehouse**; reserve "sci-draw" (no slash) for the skill itself.
- **"gap" in the thesis family's intro gate ("每个 gap→某章填了") was ambiguous.** Two readings: (a) spine's structural progression role-question (already in chapter-map.md, no new artifact) or (b) intro's narrative research-status 断层 (finer-grained, needs its own baton). Resolved: **(b) narrative gap** — intro produces `gap-map.md` (post-write, mirroring dissect's chapter-map.md) + `check_intro.py` greps gap→chapter against chapter-map.md. The structural role-question is a different thing (spine's, coverage-gated via check_spine.py / chapter-map.md). See **Narrative gap**.
- "检索" (retrieval/search) was initially treated as out-of-scope for sci-write (reason to offload Introduction). Resolved: search is **in-scope** (the user has a search MCP); what's offloaded is Introduction/Abstract/Keyword for **writing-nature** reasons (global narrative + reverse order), not search reasons. Real-DOI placeholders are produced inside sci-write.
- "Orchestration" was conflated with "coordination." Resolved (recalibrated): **execution skills do not orchestrate each other** — each reads neighbors' on-disk outputs, never calls another. Cross-skill orchestration lives in a **separate thick-orchestration entry** (`using-sci-skills` / `auto-research` / name-TBD), not baked into execution skills, and not absent either. `sci-skills-init` is just the skill that happens to scaffold the workspace — not an orchestrator, not a "layer above." See the "three-entry architecture" family principle.
- **Decoupled vs thick-orchestration is not "one wins."** Earlier this glossary swung between two wrong extremes: first "two-layer family, orchestrator for auto users" (over-stated the orchestrator), then "decoupled will replace thick orchestration, no orchestrator layer" (over-corrected). The resolved stance: they are **different entries serving different model/price regimes**. Strong models use execution skills directly under light directory contracts (decoupled wins here). Cheap models in high-volume flows use a thick-orchestration entry that gear-shifts for them (orchestration earns its keep here). The capability/price tradeoff is permanent, so both entries are permanent. The only thing truly deprecated is baking orchestration **into execution skills** — that couples parts that should stay replaceable.
- **Why decoupling is a survival strategy, not a tidiness preference.** The research-skills ecosystem is crowded and fragmented — everyone has their own taste in writing style, plotting tools, and workflow. Tightly-coupled "full-suite" skills force all-or-nothing adoption and end up used by no one. This family's bet is the opposite: each skill is an **independently replaceable part** that interconnects via **directory contracts** (the `CONTRACT.md` per subdirectory), not via code imports. A user can mix ours with someone else's plotting tool and manual submission — as long as the `sci-skills/` directory contracts are honored, the parts mesh. **A part that cooperates with others beats a self-consistent but closed suite.** This is why the directory `CONTRACT.md` files are contracts (any agent/skill producing into a directory follows them without needing to know which skill consumes it), and why "read neighbors, don't orchestrate" is non-negotiable.
