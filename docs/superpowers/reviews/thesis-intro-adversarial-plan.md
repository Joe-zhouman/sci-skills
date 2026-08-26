# Existence Audit — thesis-intro spec

> 审查日期：2026-08-26　|　lens: design (aquarius)
> target: `docs/superpowers/specs/thesis-intro.md`
> parents: `thesis-skill-family.md` + `thesis-spine.md` + `thesis-dissect.md` + `glossary.md`（不重审家族已定决策）
> bar: spine §Load-bearing premise（tension-flagging residual 诚实命名）+ dissect §①（module-map = outline-then-fill，round-2 删 pre-write outline 修正）

**net: -25 lines deletable/consolidable** | not Lean — gap-map.md 作为 coverage baton 是 rationalization，作为 callback-anchor 载体才挣得存在

---

## Load-bearing finding（user Q1）

§① L51 + §⑥ L100: delete: gap-map.md 作为 coverage baton 的正当性是循环 rationalization。因果链：父 spec 列 intro 门"每个 gap→某章填了（coverage 机械可查）"→ intro 必须产可查 artifact → posits "narrative gap ≠ structural role" 以 justify gap-map.md → gap-map.md "satisfies" 门。glossary 本 session settle 的 Narrative gap term 是这 rationalization 的固化。**断裂点**：glossary L91 自承 "Typically one per body chapter"（1:1）。1:1 下 gap→章 从 chapter-map.md 的 role/章 by construction 可派生——check #3（filled-by 存在于 chapter-map.md）查的是**自伤**（作者编造一个不存在的章号），非真实 coverage failure。真实失败（intro 提了一个 no chapter genuinely fills 的 gap，但作者随便填一个章号）是 depth，check 查不出。check #3 是官僚式 lapse 检查，非 coverage。§⑥ "genuinely new value——单看任一 baton 查不出悬空 gap" 是 overclaim：悬空 gap 只能由人工编造产生，intro 的 gaps 本就 derived from chapter-map.md 的章，filled-by 不可能 by construction 悬空。**gap-map.md 挣得存在的是 `callback-anchor` 字段**（intro→summary 的跨 skill promise，chapter-map.md 不携带，ch0-intro.tex 是 prose 非结构化 promise）——这是 genuinely new cross-skill state，不是 coverage mapping。fix：诚实命名——coverage 门 near-trivial-by-construction（gaps derived from chapters），gap-map.md 的 real value 是 callback-anchor baton（summary 继承的 promise），非 coverage gate。镜像 spine §⑤：命名 residual（coverage 门只防缺席/官僚 lapse，不防 depth-level 空头 gap），不 overclaim "genuinely new value"。

## Finding（user Q2）

§② L57: delete: "Step 1 framing 提案（prose-craft）≠ Step 3 coverage 记录" 的二元区分是 false binary。Step 1 confirmation gate echo "(b) 哪些 gap + 哪些章填"（L151）——在**章已存在**的前提下（dissect 已写 chN.tex）commit 了一个 gap→章 的**结构性映射**，这是 pre-write outline，非 "framing"。sci-story 的 confirmation gate legitimate 的是 pre-write **叙事 framing**（单篇 article，无 chapter mapping 可 commit）；intro 的 Step 1 commit **结构**（gap→章），sci-story 的 gate 不 commit 结构。write-then-record（Step 3）诚实（记 what landed），但**不 dodge outline-then-fill**——Step 1 就是 pre-write structural outline（relabeled "framing"），Step 2 fill 它，Step 3 record fill。dissect round-1 的 module-map 就是这个 pattern 的前车（pre-write 结构 outline → gate → fill tex），aquarius round-1 已判为 outline-then-fill。intro 的 Step 1 同构，只是换名 "framing"。fix：诚实命名（镜像 spine §⑤ + dissect §①）——Step 1 是 legitimized pre-write structural outline（sci-story stance applied to structure because chapters exist），非 outline-then-fill 的 dodge。real distinction 不是 "framing vs coverage"，是 "pre-write structure commitment（OK, chapters exist）vs pre-write restructure outline（dissect 禁，逻辑热时该写）"——后者是 拆即写 的 `_Avoid_`，前者不是。当前 §② 的 defense 把两个不同的东西都叫 "framing" 来 dodge，是 camouflage。

## Finding（user Q3）

§③ L63-67: delete: B3 的 clean two-way split framing（"章级 prior work=callback；论文级 field positioning=search"）。gray zone 无 decision procedure：一个 citation 若同时 load-bearing for 一个 chapter 的 prior work **和** thesis-level framework positioning（unified framework 的理论根源常被各章 cite 又框住主线），归 callback 还是 search？规则 "supplement what chapters don't carry"（L67）circular——"chapters carry 什么" IS the gray zone。boundary 实际 collapse 到 confirmation gate 的 author judgment。fix：replace clean-split framing with "heuristic + gate decides gray zone"（镜像 §④ residual 命名），非 clean two-way。当前 §③ 把 B3 呈现为 cleaner than reality。

## Finding（user Q4）

§④ + §门 L160: shrink: C3 mostly honest（命名 hollow-研究现状 residual，镜像 spine Load-bearing premise）——但 §门 L160 "Narrative craft（confirmation gate + eval...）" 把 confirmation gate 称作 "narrative craft enforcement" overclaim。confirmation gate enforce 的是 **framing alignment**（这节讲什么、提哪些 gap），非 narrative-craft depth（gap 是断层还是空白、研究现状定位准不准）。depth rides on author judgment at the gate（stated residual §④），非 gate 本身 enforce。minor overclaim；fix：name gate as framing enforcement，depth as author-judged residual（非 gate）。**不是 refusal to admit needed depth gate**——intro 的 depth 与 spine 同构（AI 不能诚实 gate depth，会生成它检查的空洞），且 lower-stakes（intro narrate 已 settle 的架构，非 set 架构；hollow intro 可重写，hollow spine 是全盘坏基座）。intro 不需要它拒绝承认的 depth gate。

## Finding（user Q5）

§sub-decision a L188-190 + §对父spec偏离 L233: honest，无 finding。placeholder 明示"具体文件名随 thesis-intro skill 设计定（该 skill 后续计划补）"——filling it 是 invited completion，mirrors dissect 的 CONTRACT.md 命名 chapter-map.md 先例。~1-string edit to merged thesis-init 非 churn。唯一 implementation note：edit init_project.py 后须 re-run test_init.py 确认无 break（implementation detail，非 existence issue）。

## Finding（new，非 user 点名）

§⑦ L104-105: shrink: "Intro↔Summary coherence lock... 结构化 enforcement 经 gap-map.md callback-anchor 字段" overclaim。gap-map.md 是 DATA BATON（载 callback-anchor promises）；coherence LOCK（summary 必须 callback 每 gap）的 enforcement 是 summary 的 future check_summary.py（未设计），非 intro 的。intro 提供 data，summary enforce lock。§⑦ 把 gap-map.md 呈现为 "the lock"，overclaim intro 在 coherence lock 的角色。fix：shrink to "baton（data）for summary's future lock"，非 "the lock"。folds into load-bearing finding——callback-anchor 是 gap-map.md 唯一 genuinely new 内容，应明说它是 baton-for-summary，不是 coverage gate 或 coherence lock。

## Finding（new，非 user 点名）

schema L138 + check #2 L95: delete: `anchor-in-intro` field。check_intro.py #2 验它 non-empty，不验它 resolves to content in ch0-intro.tex。是 pointer into prose，polish/revision 后 drift，无人 maintain。non-enforced pointer = ceremony。fix：or enforce（grep ch0-intro.tex for the anchor，resolves 才 pass）or delete the field。当前是"non-empty string"检查——纯仪式。

## Finding（secondary shrink）

§关键替代方案 L110-121 + §对父spec偏离 L224-236 + §Acceptance 防带病推进 L204-209: shrink: 3 个 core defense（narrative≠structural / write-then-record≠outline / C3≠depth-gate）各 restated 4-5 次 across these sections。consolidate to once in §Design Rationale + once in §关键替代方案。~12 lines。注：spine/dissect 同样 repetitive（family style），非 intro 独有；轻 finding。

---

## Holds（vote-of-confidence，not re-audited）

- §⑥ coverage 脚本 + stdlib test split（镜像 spine/dissect §⑥/§⑧）——repo 已 justify 的 test deviation 先例，sound。
- §⑤ hybrid 纪律（sci-story confirmation gate + dissect write-then-record）——shape 上 sound，leak 见 §② finding（framing vs structure 的 camouflage），非纪律本身坏。
- §⑧ terminology-ledger 共写——clean one-liner，镜像 sci-write/dissect。
- untrusted-content guard（镜像 spine/dissect）——sound。
- scope 边界（只写绪论、不深读论文、不 re-gate 架构 depth）——clean，对齐父 spec v1。
- 跨 skill 文件交接表——inherited from family，sound。

## Score rationale

Not "Lean. Ship." Load-bearing finding（§①+§⑥）：gap-map.md 作为 coverage baton 是 rationalization——1:1 下 coverage near-trivial-by-construction，real value 是 callback-anchor（summary promise）。spec overclaim coverage 为 "genuinely new value"。§② finding（write-then-record dodge）是 dissect round-1 module-map 问题的变体（pre-write structural outline relabeled "framing"），需诚实命名。§③（B3 clean split）+ §⑦（coherence lock overclaim）+ anchor-in-intro ceremony 是叠加 overclaim。~25 lines 需 delete/reframe（gap-map.md overclaim defense + check #3 overclaim + §② false binary + B3 reframe + §⑦ shrink + anchor-in-intro field + repetition）。无 finding 否定 skill 存在本身——gap-map.md 作为 callback-anchor baton 挣得存在，只是 spec overclaim 了它的 coverage 角色。fix 是诚实命名（镜像 spine §⑤ + dissect §① round-2），非删 skill。
