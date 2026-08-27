# Existence Audit — thesis-dissect

> 审查日期：2026-08-26　|　lens: design (aquarius)
> target: `docs/superpowers/specs/thesis-dissect.md`
> parents: `thesis-skill-family.md` + `thesis-spine.md` + `glossary.md`（不重审家族已定决策）

**net: -4 lines deletable** | not Lean — §① load-bearing premise flawed

---

§①: hidden assumption: per-module gate preserves 拆即写. It doesn't. Step 3 produces module-map (question→method→results triples for ALL modules of the chapter) + author gate, BEFORE Step 4 writes any tex (L161-165). That IS outline-then-fill — the very two-step glossary 拆即写 rejects (glossary L79: "Dissect is not two responsibilities forced together (structure-judgment + writing); they are two faces of one act"; `_Avoid_: outline-then-fill`). module-map IS the structural dissection (IMRaD→method-results restructure = breaking the paper into chapter pieces); tex is the prose-level execution of that breakdown. They are separated by a gate, not "two faces of one act." The spec's defense ("per-module same pass", L43/L49/L232) addresses prose-level heat preservation, not the unity-of-dissection-and-writing the glossary requires. Per-module keeps module-4 prose hot while writing module-4; it does not undo that the chapter's structure was already dissected (and cooled) in module-map at Step 3. §Acceptance "module-map.md 是 gate 用、非后写的依据" (L212) is camouflage — the triples ARE the writing basis; calling them "gate 用" doesn't change their function. Real tension the spec doesn't acknowledge: author gate on restructure (needs module-map before writing) vs 拆即写 (no outline-then-fill). Spec claims both; incompatible as designed. Fix: merge Step 3+4 — dissect each module BY writing it (tex + triple recorded together in one act), gate incrementally after each module is written, not before. Or drop the 拆即写 claim and own module-map as a deliberate two-step (contradicts glossary — not recommended).

§②: causal leap: "chN = role position in spine progression" (L52-53) breaks under non-1:1. Merge (roles 1+2 → ch1) makes role 3 → ch2 (not ch3). Split (role 1 → ch1+ch2) makes role 2 → ch3 (not ch2). The formula is stated for 1:1 only; "non-1:1（合并/拆分）在 role→chapter 映射内解决" (L53) hand-waves the actual numbering rule. A reader could implement "chN = role position" literally and produce wrong file names under merge/split. Fix: chN = chapter ordinal in the final sequence (after merges/splits applied), not role position. One line.

§④: missing: fallback-spine silent on consequences when spine is backtracked mid-dissect (some chapters already written). Spec handles the fallback DECISION (L162/L213: "停、flag、作者决定 backtrack-spine / force-bind") but not the cleanup. If ch1+ch2 are written against the old role sequence and paper 3 triggers backtrack-spine (role sequence changes), spec doesn't address: are ch1/ch2 invalidated? renumbered? does chapter-map.md get rewritten? tex files renamed (ch2.tex → ch3.tex)? Already-written chapters built on the old spine would be stale. Missing negative space — the design allows backtrack but doesn't bound its blast radius.

§⑤: yagni: per-paper binding.md mandated for every paper (L79/L149-156). For 1:1 (default, most papers — spec L69 "默认 1:1"), content is near-empty ("paper X → role Y, 1:1, no candidates"), duplicating chapter-map.md's role+papers fields (L131/L141). The audit trail value (pending merge/split candidates + author disposition) is only real for non-1:1. The spec's rejection of "不留 binding 文件" (L83: "丢每篇架构级 depth 审计 trail") assumes every paper has a depth audit worth trailing — for 1:1 there is none. Fix: create binding.md only when non-1:1 is detected; for 1:1, binding is implicit in chapter-map.md. Drops ~4 lines (the mandate framing + the "不留 binding" rejection + the schema line's unconditional placement).

§对父 spec 的偏离: the "无偏离需 re-review" claim (L231) is false. §① per-module gate + module-map IS "dissect+write 两步" — family spec §③ (L64): "dissect 不分拆+写两步". module-map (dissect) → gate → tex (write) is two steps. Flag as deviation from family spec §③ + glossary 拆即写, not "faithful refinement." The spec's own Problem section (L18) warns against "分两步（先拆笔记、再据笔记写章）" then the workflow implements exactly that under the name module-map.

---

## Round 2 — re-audit（2026-08-26）

> lens: design (aquarius) | target: revised `thesis-dissect.md`（round-2 fixes）
> round-1 verdict: §① load-bearing flawed（module-map = outline-then-fill）+ 4 minor。下逐条 re-verify。

**net: -1 line deletable** | §① load-bearing flaw FIXED；no new load-bearing premise。One sharpness gap（resume over-claim，non-load-bearing）。

### Round-1 findings，re-verified

- **§①（load-bearing）— FIXED。** dissect-by-writing：每模块的 tex IS the dissection（IMRaD→method-results 重构在写中发生，非写前规划）；post-module gate 在模块 tex 写完后；无 module-map.md。满足 glossary 拆即写（"two faces of one act"——结构判断 + 写作在 in-write act 中统一，无 separate outline）+ family spec §③（"不分拆+写两步"——无两步）。"too late" 质疑（prose 已写时才 gate）被答：post-module gate 审 restructure 的**realized form**（tex），比 abstract skeleton 更强（skeleton 看似合理、prose 里垮）；reject-cost（prose 作废）镜像 sci-write 每段 confirmation gate，article 家族已接受。无 residual outline-then-fill——trace.md（Step 1.2）记 SOURCE 论文的 IMRaD（reading 产物），非 TARGET restructure（后者 in-write）。§对父 spec 的偏离 "无偏离" claim 对 §① now holds。
- **§② — FIXED。** chN = 应用 merges/splits 后的章序号（非 role 位置）。Well-defined：遍历按 spine role 序，章号按实际产出递增（merge = 并入前一已定章、不递增；split = 产多章、按产出递增）。消解 cascade（merge 1+2→ch1、role 3→ch2；split role 1→ch1+ch2、role 2→ch3）。
- **§④ — FIXED。** backtrack cleanup：受影响已写章标 `stale`（chapter-map.md status）、tex 不自动删、re-run 时提示作者（不静默覆写）、dissect 不跨 skill 改 spine。决策层 coherent。
- **§⑤ — FIXED。** trace.md（每篇、深读）+ binding.md（仅 non-1:1）。module-map 删。Audit trail 充分：trace（source）+ binding（决策）+ chapter-map（章 framework/progression）+ tex（realized restructure）。删 module-map 不丢 audit surface——restructure 在 realized form（tex）+ source trace 可审。

### New finding（round 2）

§Step 0（L153）: hidden assumption: resume logic（"读 chapter-map.md 找已 settle 的章/篇；从第一篇未写的续"）假设中断发生在章边界。chapter-map.md 按**章**粒度记 status（pending/written/stale）；写作按**模块**粒度（§①，Step 1.3）。一章写到一半中断（部分模块已落 chN.tex、章仍 pending）无盘上 marker 标哪些模块已写——resume 定不到续写点。round-1 module-map 本会显示 per-module triples；round-2 删它（对——为拆即写）丢了 per-module resume tracking。**Not load-bearing**（作者每模块 gate 后 in-loop、知停在哪；最坏 = 章从 module 1 重写）。Fix：one line——resume 在章边界；章内中断 = 作者指示续写点（或 chapter-map.md pending 条目带 `last-module-written` 字段）。

### New-premise check（round 2，用户点名三项）

- **contract-gap 检测时机（无 module-map）**：not load-bearing。contract-gap（IMRaD 不干净）是 SOURCE 论文属性，在深读 Step 1.2（trace.md 记 "IMRaD 结构"）浮出，先于 Step 1.3 写。restructure-discipline.md（§⑥）给 in-write 处理。删 module-map 不丢检测——它从不在 module-map 时检测。
- **post-module gate 是否 meaningful（prose 已写）**：not load-bearing——更强非更弱。审 realized prose 里的 restructure > 审 abstract skeleton（skeleton 看着合理、prose 垮）。reject = rewrite（作者是 gate）。镜像 sci-write。
- **"no deviation" claim（§对父 spec 的偏离）**：now holds。§①（round-1 false claim）已正；§⑧（stdlib test）是唯一 acknowledged deviation，spine/init 先例已 justify。

### Verdict

§① load-bearing flaw genuinely fixed。dissect-by-writing 满足 glossary 拆即写 + family spec §③——结构判断与写作 in-write 统一，无 pre-write outline，post-module gate 在 act 之后不割裂。无新 load-bearing premise（contract-gap 时机、gate meaningfulness、deviation claim 均验过）。One non-load-bearing sharpness gap（resume over-claim，round-2 删 module-map 的直接后果，one-line fix）。Round-1 的 "false no-deviation claim" 已消解。
