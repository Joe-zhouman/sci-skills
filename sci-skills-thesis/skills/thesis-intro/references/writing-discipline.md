# Writing discipline — 绪论写作纪律（framing alignment + 数据 baton + 诚实边界）

本 skill 在写每节绪论 prose 前打开本文件。它指导**写时**的纪律——confirmation gate、real-DOI 占位、动词校准、术语 enforce——**不是** pre-write outline。镜像 sci-story 的 `writing-discipline.md` 升尺度到 thesis，并嫁接 dissect 的写后 baton 纪律。

绪论章（`thesis/tex/ch0-intro.tex`）不是单篇 article 的 introduction——它要 callback spine 主线、建论文级研究现状、articulate N 个 narrative gap（每个对应一个正文章）。本文件是写时纪律的完整内容；零依赖。

---

## The per-section confirmation gate（enforces FRAMING ALIGNMENT，非 depth）

**目的**：在每节绪论（研究背景 / 研究现状 / gap articulation / thesis-structure-preview）写完整 prose 之前，回显一个对齐块，停下来等人确认——在最便宜的时机（写之前）暴露 framing 错。

**gate echo**：

- **一段论证**：本节讲什么、在漏斗里哪一段。
- **哪些 gap + 哪些章填**：本节会 articulate 的 narrative gap，每个对应哪个正文章填（章已存在——dissect 已写 chN.tex）。
- **关键术语/假设**：本节用到的核心概念的 canonical form（从 `thesis-terminology-ledger.md` 读），以及你**推断而非被告知**的假设（尤其"gap 是什么""哪个章填哪个 gap"）。

**关键纪律——gate enforce 的是 framing alignment，不是 narrative-craft depth**：

- gate 查"这节讲什么、提哪些 gap、哪些章填"——**framing alignment**。
- gate **不**查"gap 是断层还是空白？研究现状定位准不准？"——那是 **depth**，作者在 gate 上判断的 residual，不是 gate 本身 enforce 的（spec §④ residual）。
- 一个 framing 准但空洞的研究现状能过 gate（若作者工艺判断失准——gap 实际没章填但 agent 填了章号，gate 查不出）。这是 intro 的固有边界，诚实命名（见"诚实边界"节）。

**何时跳过 gate**：核心 gap + 填它的章 + 关键术语都已明确给出、且 framing 无真正歧义时，回显一段论证即可继续。镜像 sci-story 的 gate-skip 条件。**不要为了仪式感硬拦**——gate 是早暴露 framing 错的便宜时机，不是 ceremony。

**与 sci-story gate 的关键区别（升尺度）**：sci-story 的 confirmation gate legitimate 的是 pre-write **叙事 framing**（单篇 article，无 chapter mapping 可 commit）；intro 的 Step 1 gate **commit 结构**——gap→章 cross-reference（章已存在，mapping 可 commit）。这是 sci-story gate 不带的部分——见下一节。

---

## The Step 1 pre-write structural commitment（honest residual，非 outline-then-fill 的 dodge）

**目的**：命名 intro 的 Step 1 confirmation gate commit 的 gap→章 mapping 是**pre-write 结构承诺**——不是 round-1 spec 说的 "framing 提案"（那是 false binary + camouflage），也不是 拆即写 禁的 outline-then-fill。诚实命名 residual。

**真 distinction（不是 round-1 的 false binary）**：

- round-1 spec 称 Step 1 gate 提的是"framing 提案（prose-craft）"，与 Step 3 的"coverage 记录"是两件事，以此 dodge outline-then-fill。aquarius round-1 抓到这是 **false binary + camouflage**：Step 1 的 gate echo "哪些 gap + 哪些章填"——在**章已存在**（dissect 已写 chN.tex）前提下 commit 了一个 gap→章 的**结构性映射**，这是 pre-write 结构承诺，非"framing"。把两者都叫 "framing" 来 dodge 是 camouflage。
- **真 distinction 不是 "framing vs coverage"，是 "pre-write 结构承诺（OK，章已存在）vs pre-write 重构 outline（dissect 禁，逻辑热时该写）"**（spec §② round-2 修）。

**为什么 intro 的 gap→章 不是 outline-then-fill（dissect 的 `_Avoid_`）**：

- intro 的 Step 1 commit 的是 gap→章 **cross-reference**（指向**已存在**的章，mapping 是 **discovered**——章的 framework-instantiation 是否填该 gap 可从 `chapter-map.md` 查——非 **generated**）。章已存在，mapping 是发现非创造。
- 拆即写 的 `_Avoid_: outline-then-fill` + 父 spec §③ 禁的是 **pre-write 重构 outline**（dissect round-1 的 module-map——**生成**章的内部模块结构，该在逻辑热时写）。intro 的 gap→章 不生成结构，是发现对已有章的对应。
- **所以 intro 的 Step 1 不是 outline-then-fill**——但 **是 pre-write 结构承诺**（commit gap→章，约束 prose），有 residual 要命名，非 round-1 的 clean dodge。

**named residual（不消除）**：

- Step 1 pre-commit gap→章 约束 Step 2 的 prose（"你说 gap X→章 Y，所以 gap-X prose 要 set up 章 Y 的贡献"）。这是 pre-write 结构承诺的代价——prose 被一个 pre-commit 的 mapping 约束。
- **接受的 why**：gap→章 mapping 的"正确性"（章 Y 是否真填 gap X）可 pre-write 从 `chapter-map.md` 的 framework-instantiation 查（不需写 gap prose 才知道），所以 pre-write gate 能早抓"提了 no-chapter-fills 的 gap"——这是早检测价值，值得 pre-commit 的代价。
- **alternative（纯 post-write record，无 pre-commit）丢早检测**——且 gap→章 mapping 本就可 pre-write 查（不像 dissect 的模块重构必须写时才清）。这是相对最优，非 dodge。

**写后记录覆盖 pre-commit**：Step 3 从落盘的 `ch0-intro.tex` 记录 `gap-map.md`——若 Step 1 的 pre-commit mapping 与写出的事实不符，Step 3 以落盘为准（dissect 写后记录纪律：record what landed，非 record what was proposed）。

---

## The Intro↔Summary coherence baton（intro provides DATA，summary enforces the lock）

**目的**：sci-story 有 Intro→Discussion coherence 铁律（skill 内：Intro gap → Discussion 填）。thesis 升尺度为 **Intro↔Summary**（跨 skill）：intro 在 `ch0-intro.tex` 提的每个 gap → summary 必在 `chN-synthesis.tex` callback。

**关键纪律——intro 是 data baton carrier，不是 coherence lock**：

- **intro 提供 DATA**：`gap-map.md` 每 gap 的 `callback-anchor` 字段是 summary 继承的 cross-skill promise（chapter-map.md 不携带，ch0-intro.tex 是 prose 非结构化 promise）。
- **summary enforce LOCK**：coherence lock（summary 必须 callback 每 gap）的 enforcement 是 **summary 的 future `check_summary.py`**（未设计），非 intro 的。intro 提供 data，summary enforce lock（spec §⑦）。
- **不要 overclaim intro 为 "the coherence lock"**——intro 是 data baton carrier，lock enforcer 是 summary。round-1 spec 把 gap-map.md 呈现为 "the lock" 是 overclaim（aquarius §⑦ finding），round-2 修正。

**`gap-map.md` 的真价值 = `callback-anchor` 字段**（spec §①）：

- coverage near-trivial-by-construction（gaps ~1:1 derived from chapters，glossary "typically one per body chapter"）——check_intro.py 的 filled-by cross-ref 只能抓**官僚 lapse**（agent 编造不存在的章号），非真实 coverage failure。
- `callback-anchor` 是 gap-map.md **唯一 genuinely new** cross-skill 内容——summary 继承的 promise，chapter-map.md 不携带。这是 gap-map.md 挣得存在的真正理由，非 coverage 门。

---

## Real-DOI placeholder protocol（真 DOI，不空占位）

**目的**：凡涉及外部文献，每个引用都挂在一个 real-DOI 占位符上——不空 `[CITE:?]`，不编造条目。镜像 sci-write/sci-story。

**纪律**：

1. **调检索 MCP**（academic toolset / `references/literature-search.md` 的优先级）拿到真实文献标识（DOI 等）。
2. **把真实 DOI 落成占位符**——不是空的 `[CITE:?]`，也不是编造的 `.bib` 条目。
3. **最终插入 Zotero 永远由 author 完成**——agent 不生成 `.bib` 条目、不替 author 按插入键。
4. **章级 prior work 走 callback**：正文章（chN.tex）的 prior work 引用，dissect 已用 real-DOI placeholder 落地——intro **复用不重搜**（B3 heuristic 的 callback 路）。
5. **论文级 field positioning 走 search**：umbrella 的领域背景、统一框架的理论根源、框住主线的跨章研究现状——走 `references/literature-search.md` 的 real-DOI 搜索（thesis-scale）。

**gray zone at gate**：一个 citation 若同时 load-bearing for 一个章的 prior work **和** 论文级 framework positioning（如统一框架的理论根源）→ 作者在 confirmation gate 裁决 callback 还是 search。B3 是 heuristic，非 clean two-way split（见 `references/literature-search.md`）。

---

## Verb calibration（按叙事强度）

**目的**：claim 强度匹配证据。镜像 sci-story 的动词校准表。

| 强度 | 动词 | 使用场景 |
|---|---|---|
| 强 | show / demonstrate / establish | 绪论陈述 thesis-level 贡献时；陈述"本论文建立了 X" |
| 中 | suggest / indicate / support | 解释框架选择的合理性时 |
| 弱 | may / could / might | 推测影响/未来方向时；陈述前人工作的局限时 |

**绪论用词比 discussion 确定**——绪论陈述"本论文做了什么"是事实（过去时），discussion 风格的机制推测（"这可能意味着 X"）不进绪论。

**不要把 hedge 动词放在 thesis-level claim 的声明里**——绪论陈述 thesis 主贡献用强动词（establishes / shows），不用 may/could。hedging 留给 discussion。镜像 sci-story。

**扫除无支撑的全称断言**：成稿前扫一遍 `first` `unique` `unprecedented` `comprehensive` `complete` `always` `never`。证据真支持才留，否则改成有边界的 claim 或删掉。`significantly` 不出现在结果句。

---

## Terminology enforcement（canonical forms）

**目的**：读 `thesis-terminology-ledger.md`（spine seed + dissect 扩展），enforce canonical forms 在写的 tex 里；extend intro-level 术语。镜像 sci-write/dissect 的共写模式。

**纪律**：

1. **读 ledger**：spine seed 的核心术语 + dissect 扩展的章级术语，写时 enforce canonical form（同一变量/方法在全绪论用同一词）。
2. **extend intro-level 术语**：绪论新引入的术语（论文级 framework 命名、umbrella 概念、跨章统一表述）→ 追加进 ledger，标 `source: thesis-intro`。
3. **不碰 article 家族的 `sci-skills/sci-write/terminology-ledger.md`**——跨家族术语统一 out of scope（父 spec v1 cut）。

---

## The honest boundary（防缺席 + 防官僚 lapse，NOT depth）

**目的**：命名 intro 的固有边界——文件交接 + coverage 门防什么、不防什么。诚实命名，不 overclaim。镜像 spine §⑤ + dissect §诚实边界 + 父 spec §Load-bearing premise。

**防的（结构机制）**：

- **缺席**：`gap-map.md` 不存在 → summary 进行不下去（文件交接面强制）。
- **官僚 lapse**：`check_intro.py` 抓 agent 编造不存在的章号 / filled-by 悬空 / status 残 `pending` / 字段空 / `ch0-intro.tex` 缺。near-trivial-by-construction consistency（gaps derived from chapters，非 spine/dissect 那种"required 结构元素在不在"的 coverage）。

**不防的（author judgment residual）**：

- **depth-level 空头 gap**：一个 gap 实际没章 genuinely fills，但 agent 填了有效章号 → 过 coverage，是 depth failure。check 查不出（§① residual）。
- **framing-accurate-but-hollow 研究现状**：confirmation gate 查 framing alignment（这节讲什么、提哪些 gap、哪些章填），**不**查 depth（gap 是断层还是空白？研究现状定位准不准？）。一个 framing 准但空洞的研究现状能过 gate + coverage（§④ residual）。
- **gap 是空白型而非断层型**：gate 不判 gap 是断层还是空白——那是作者工艺判断（见 `references/introduction-guide.md`）。

**没有任何结构性机制替代作者叙事工艺判断**。confirmation gate 比 spine 的分级 depth-gate **软**——架构 depth（主线/框架/umbrella）已在 spine 人工门控 settle，intro narrate 不 re-gate（re-gate 冗余，C2 拒）；intro 自己的 depth 就是叙事工艺，靠作者判断。命名不消除，不 overclaim。

---

## Privacy

**目的**：不在产出里泄漏私人本地路径、私人文件名、未发表内容。镜像 sci-story。

**纪律**：

- `gap-map.md`、`ch0-intro.tex`、commit message、user-facing replies 里不写私人路径/文件名/未发表 paper 内容。
- 需要提及时用泛称（"paper-C 的 §4.2"、"提供的数据文件"）。
- 仅在 author 明确要审计轨迹时才露具体路径。
