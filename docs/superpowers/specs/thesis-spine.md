# Spec — thesis-spine（提主线+统一框架，写作链起点）

> 设计日期：2026-08-25　|　状态：draft（aquarius 审 round 3 + 用户审）
> 源：brainstorming（本 session；round 1 定 4 点；round 2 修 aquarius load-bearing §⑤ + §⑥；round 3 修 §③——umbrella 复位 depth 桶，消除 round-1 的 §门 自相矛盾）
> **父 spec（权威源）**：`docs/superpowers/specs/thesis-skill-family.md` — 家族设计 single source of truth。本 spec 是其写作链第一个 skill 的细化，**不重述**家族已定的决策（enforcement split 三层 / Load-bearing premise / 落盘文件耦合 / 模板 init 织死 / v1 scope），遇到时指向父 spec。
> 上游 glossary：`docs/superpowers/glossary.md`（6 thesis 术语）
> 镜像范本：`sci-skills-article/skills/sci-write/SKILL.md`（claim.md 硬门 + rung ladder + terminology-ledger + contract-gap + scan_neighbor.py 助手脚本）+ `sci-story/SKILL.md`（gap→response + 每段 confirmation gate）
> aquarius round-1 审：`docs/superpowers/reviews/thesis-spine-adversarial-plan.md`（4 findings，round 2/3 逐条消解——见各 §）

---

## Problem

### 谁痛、何时痛、多痛

父 spec 已命名家族级痛点（§1 主线丢了 / §2 框架和共性 AI 一碰就毁 / §3 正文不能照搬 IMRaD / §4 总结变重复）。thesis-spine 是写作链**起点**，它针对的是其中**一个具体的、卡住全盘的痛点**：

**没有定下来的主线+框架，下游全是在流沙上盖楼。** N 篇小论文各自独立成篇，各有 claim 和叙事线。作者如果直接跳到"逐篇重构成章"（dissect），等于在**没有统一主线和框架**的前提下拆章——拆到总结才发现：各章之间递进不起来、绪论的 gap callback 不回来、统一框架根本没贯穿。父 spec §"如果什么都不做"已点明这是**全盘返工**的根源（"主线没贯通就往下写，写到总结才发现 callback 不起来"）。

thesis-spine 的职责就是**在拆任何一章之前**，把架构级的事定下来：主线（串起 N 篇的 thread）、统一框架（把所有研究统一进一个框架）、章间递进（上章 results 引发下章 question）、thesis 级 claim（umbrella——全篇一句话总贡献，三结构字段 collectively argue 它）+ boundary（claim 不 establish 什么）。定了这些，dissect 才有东西可拆、intro 才有 gap 可 callback、summary 才有共性可提炼。

### 如果什么都不做

作者跳过 spine 直接 dissect。三种后果（都已在父 spec 命名）：
1. **主线缺席** → 拆出来的章是"论文合集"不是"一篇文章"。
2. **框架缺席** → 各章各自为政，没有统一框架贯穿，theory 章无主线可实例化。
3. **递进缺席** → 写到总结才发现 callback 不起来 → **全盘返工**（父 spec §"如果什么都不做"的核心风险）。

文件交接面强制的是 spine.md 的**存在**（dissect 读它，不存在进行不下去）——这是父 spec §②的诚实边界：decoupling 防**缺席**不防**坏**。本 spec 不重述此边界，只落实 spine 这一头：spine.md 必须存在且架构级组件已人工门控 settled，dissect 才有资格开跑。

### 为什么不能让 AI 直接生成主线+框架

父 spec §① + §Load-bearing premise 已定：AI **无法诚实审计架构级 depth**——检查"这个框架够不够高屋建瓴"的 AI，本身会生成它所检查的空洞。所以架构级 depth **只能人工门控**，AI 的作用是辅助（提候选标 `pending` 不自动采纳、拆逻辑、提出作者因投入看不见的 tension）。本 spec 落实这个 split 在 spine 内部的具体形态——**并诚实命名 AI 辅助的 residual 是 depth-influence 而非 depth-gating**（§⑤，aquarius round-1 的 load-bearing finding）。

---

## Design Rationale

### 核心设计判断（逐条锚定痛点 + brainstorm 已定 + aquarius round 2/3 修正）

#### ① 分级门控 + 回溯（staged gates with backtrack）

**brainstorm 定（Q1）**：三个结构组件按 **主线 → 框架 → 递进** 的依赖顺序逐级提候选 + 人工门控，每级在下一级 build on 它之前 settle；作者可回溯（改前一级 → 重新提下游候选）。thesis 级 claim（umbrella）在三者 settle 后提（Step 4）——总贡献要等结构 firm up 才能定。

**为什么不是"一次提全 + 一次审"**：三件不是独立的——框架 build on 主线，递进 build on 框架。一次性提案意味着 AI 在主线都没定的情况下就猜框架、在框架没定的情况下就猜递进——猜的成分逐级放大，depth 人工门失去焦点。分级强制"先定基座再往上盖"，镜像 sci-write 的 claim-first-then-plan 依赖（claim.md 先于 paper-plan）。

**为什么允许回溯**：作者在审框架时可能发现主线本身有问题（框架提不出来说明主线选错了）。禁止回溯 = 强迫作者在坏主线上硬撑。回溯是诚实的：承认前面定错了，重提下游。回溯后下游候选重新标 `pending`。

**为什么不是"集成提案 + 逐组件门"**（brainstorm 拒绝项）：让作者在已接受的部分上保留未定组件，等于让**基座（主线）在框架之后仍可议价**——破坏"基座先于上层"的依赖纪律。分级 + 回溯更严：上层只能在已 settle 的基座上提。

#### ② 单一富 baton 文件（single rich `thesis-spine.md`）

**brainstorm 定（Q2）**：spine 的 process artifacts（intake map / pending 候选 / tension 记录）和 product（架构级组件 + boundary）**全在 `thesis-spine.md` 一个文件**。不建 spine 工作目录、不建额外 notes 文件。

**为什么**：
1. **父 spec 已定 spine 无目录**（"无文件夹：产顶层共享文件"）。建 notes 文件或目录违反已 merge 的 foundation layout——会 churn 已合并的基础设施。
2. **No Save, No Safe**：process 必须跨 session 落盘。落在 spine.md 里（而非 chat）才安全。
3. **sci-write 的 claim.md 先例**：claim.md 就是"product（一句话 argument + gap + evidence baseline + boundary）+ process（evidence baseline 是提 claim 时的依据）"同处一文件。spine.md 镜像这个形状：product（settled 字段 + boundary）+ evidence base（Intake）+ audit trail（Cracks / Alternatives）同处一文件。作者是**读着这个富 baton 做 depth 判断**的，不是读 chat 上下文（父 spec §①："files-on-disk as the audit surface"）。

**为什么不是"clean baton + 单独 notes 文件"**（brainstorm 拒绝项）：多一个下游无人读的顶层文件，增加维护面，且把"作者审 depth 的审计面"割裂成两个文件。富 baton 让作者一处看全（候选 + 依据 + tension）。

#### ③ thesis 级 claim = umbrella（depth-gated 第 4 项，与父 spec 一致）

**brainstorm 定（Q3，round 1 选 umbrella；round 3 复位——修 aquarius round-1 #2/#3）**：thesis-level claim 是独立于三结构字段的 **umbrella**——全篇一句话总贡献，三结构字段（主线/框架/递进）collectively argue 它。它不是第 4 个 coverage-gated 的结构字段，而是三个结构字段服务的**论断**。

**与父 spec 一致（无偏离）**：父 spec 在 spine.md 内容（L126）+ acceptance（L190）明确把 thesis级claim 列为第 4 个 distinct 项（"主线+统一框架+章间递进+thesis级claim，四者作者确认"），gate（L62/L159）说"三字段非空（coverage 机械）+ 作者确认 depth（人工）"。父 spec 是**coherent** 的："三字段" = 3 结构字段（coverage-gated），thesis级claim = 第 4 项（depth-gated，属"四者 author-confirm"但不属"三字段 coverage"）。本 spec 的 umbrella 即此第 4 项——**对齐父 spec，无偏离。**

**round-1 的 bug（aquarius round-1 #3 抓到，round 3 修）**：round-1 spec §门 把 umbrella 列在 Coverage（机械）下（"umbrella 非空"），与 §③"umbrella 不参与 coverage 计数"自相矛盾。**修正**：umbrella 归 **Depth 桶**（人工 only），不归 Coverage。Coverage 只含 3 结构字段。这样 §③ 与 §门 一致，且与父 spec gate（三字段 coverage + thesis级claim depth）对齐。

**关于 glossary 的诚实归属**：glossary "Architecture-level claim" 列四个（主线/框架/递进/共性提炼），**未单列 thesis级claim**。这是 glossary 与父 spec 的 pre-existing 张力（父 spec 的 spine 第 4 项 = thesis级claim；glossary 的第 4 个 architecture-level claim = 共性提炼，属 summary）。**本 spec 不解决此张力**——spine 产父 spec 定义的 4 项（主线/框架/递进/thesis级claim umbrella），glossary 的 4 个（含共性提炼）是跨 spine+summary 的视图。这是 glossary 与父 spec 之间的事，非 spine spec 的职责，不 overclaim 解决。

**为什么 umbrella 独立而非并入主线**（round-2 collapse 被 round-3 否决）：umbrella 给总贡献一个**独立的 depth-gate**（作者单独确认"这个总贡献 hollow 吗？overclaim 吗？"），与主线（thread，结构）分开门控。主线回答"N 篇怎么串"，umbrella 回答"串起来 establish 了什么"——两者相关但门控点不同。这与父 spec 的"四者 author-confirm"（4 项分别确认）一致；collapse（并入主线）会丢掉这个独立 depth-gate，且偏离父 spec 的显式 4-项枚举。

#### ④ 章间递进 = 角色 + 默认 1:1，dissect 绑定（roles, not paper bindings）

**brainstorm 定（Q4）**：spine 的章间递进列的是**研究章角色（roles）的序列**（默认 1:1，N 篇 → N 个角色），每个角色声明 its question + how it advances the main line。**paper-agnostic**（角色，不是 paper→chapter 绑定）。dissect 在拆即写时把 paper 绑定到角色（chapter-map.md，支持合并/拆分），绑不上 fallback spine。

**为什么 spine 不直接绑 paper→chapter**（brainstorm 拒绝项）：绑 paper→chapter 需要**深读**各篇（拆即写时逻辑最清）——这是 dissect 的职责（父 spec §③ 拆即写）。spine 阶段只做 high-level intake（claim + 结构 + 如何串主线），没深读，绑了也是瞎绑。

**为什么不是"纯抽象递进、无角色"**（brainstorm 拒绝项）：dissect 得到的东西太少，没法 map。角色给 dissect 一个可绑定的骨架（默认 1:1 意味着大部分情况直接绑，少数合并/拆分由深读决定），既不过早绑定、又不让 dissect 从零推断。

**默认 1:1 的来源**：N 篇小论文 → N 个研究章是**最常见**情况（父 spec §Implementation 盘上布局 `paper-A/ paper-B/` 即默认 1:1）。少数合并（多篇共用一个统一框架的侧面 → 一章）或拆分（一篇体量太大 → 多章）由 dissect 深读后决定，chapter-map 支持这两种 non-1:1（父 spec §dissect）。

#### ⑤ tension-flagging（AI 辅助的诚实形态，bounded 在"提问"非"裁决"）

父 spec §① 给 AI 在 depth 层的角色是"从 dispassionate 角度审视指出作者因投入而看不见的裂缝"。本 spec 把它**落地成可执行的具体形态**——并诚实命名其 residual。

**形态：tension-flagging = 向作者提问，永不裁决。** 每个 stage 提完候选后，AI 在 `## Cracks flagged` 加一条，每条是**一个问题**，含三要素：
- **(a) 提出的 tension**：例如"主线说 X 统一了 N 篇"。
- **(b) 触发 tension 的具体证据**：例如"paper C 的 Fig 3 / §4.2 看似 claim ¬X"（anchor 到具体 paper/figure/段落）。
- **(c) 给作者的问题**：例如"paper C 的 ¬X 是否 tension 主线的 X？若 tension 成立，主线是否需修订？"——**问题，不是裁决**。

**作者处置**（AI 不参与）：fatal → 修订候选；dismissed → 记 reason（"author 判断 ¬X 不 tension，因为 paper C 的 ¬X 是限定条件下的，主线 X 是一般情况"）。disposition 落 `## Cracks flagged` 作 audit trail——dissect/summary 继承的是"作者知悉该 tension 并处置了"这一记录，**不是 AI 裁决**。

**诚实的边界（aquarius round-1 的 load-bearing finding，关键）**：

- **tension-flagging 是 depth-INFLUENCE，不是 depth-gating。** AI 决定**提哪些 tension**——这个选择本身就 bias 作者的注意力（attachment-blind 的作者可能被 AI 的 framing 带着走，只看 AI 提的、忽略 AI 没提的）。这是**不可消除的 residual**：只要 AI 参与提 tension，就有 framing 影响。**本 spec 诚实命名此 residual 为 stated failure mode**，不假装消除。
- **与 forbidden 的区分**：forbidden 的是 AI **gate depth**（裁决"这个框架很浅"作为 verdict、或 auto-adopt 候选）。tension-flagging **不裁决、不 auto-adopt**——它提问，作者判。但**提问即影响**，这个 influence 是接受的、命名的、bounded 的。
- **被禁止的形态（aquarius round-1 已纠）**：把 tension-flagging 类比成 sci-write 的 figN-reading（"事实核查"）。**这是 false equivalence**——figN-reading 比较的是 prose vs rendered PNG（两个具体 artifact 之间的事实核查）；tension-flagging 比较的是框架抽象 vs 论文内容（depth 判断）。tension-flagging 的价值**不是事实核查**（事实核查归 coverage/grounding 机械层，父 spec 已有），而是**attachment 的缺席**——AI 对作者的工作没感情，能提作者因投入而看不见的 tension。诚实归属：tension-flagging 的 honest 子集（可核查的 cross-consistency 事实）与 coverage/grounding 机械层**重叠**；它的独有价值（attachment-blind tension）**就是 depth-influence**。本 spec 接受这个 influence 并命名，而非假装它是无害的事实核查。

**为什么仍保留 tension-flagging**（而非 aquarius 的"restrict to facts only"或"drop"）：attachment 是真实的认知盲点（非白丁也有），AI 的 attachment 缺席是它相对作者的**唯一真实 edge**。drop 它 = 放弃这个 edge，让作者独自对抗自己的 attachment blind spot。保留它 + 诚实命名 residual = 在"AI gate depth"（更糟）和"drop 辅助"（放弃 edge）之间取相对最优。这与父 spec §Load-bearing premise 的论证结构一致：alternative（AI gate depth）明确更糟，人工门控 + AI 辅助保留作者否决权，是**设计的固有边界，不是可消除的缺陷**。

#### ⑥ 测试：split——coverage 门用脚本+pytest，prose 用 eval

**brainstorm round 2 定（修 aquarius round-1 #4）**：round 1 一刀切"eval not pytest"——aquarius 指出 spec 自己的 eval cases（pending-check、tension 三要素、coverage 门抓空字段）是**机械可查**的，且 §门说"AI/脚本可门"。机械 enforcement 配机械测试。

**split**（与 enforcement split 同构）：
- **Coverage 门 → `scripts/check_spine.py`（stdlib）+ stdlib pytest**：确定性检查 thesis-spine.md——无 `pending` 残留、3 结构字段非空、framework 每篇实例化、progression 每角色 advance+question。镜像 `thesis-init/scripts/init_project.py` + `test_init.py`（repo 已 justify 的 deviation：确定性代码 + 可验证输出 = 值得 runnable test，skill-creator-plus/testing.md）。脚本住在 plugin `sci-skills-thesis/skills/thesis-spine/scripts/`（skill 自身源码位置，**非**项目 working dir——不违反 §②"spine 无工作目录"）。
- **Prose → eval loop**：候选是否 grounded 不空洞、是否标 `pending` 不 auto-adopt、tension 是否"提问非裁决"+ 具体证据、gate-fires-on-empty 的 agent 行为。主观输出 → eval。

**为什么 split 而非纯 eval**（mirror sci-write）：sci-write 不 ship coverage 脚本是因为它的门是 interpretive（"每个 figure 的 claim 是否 hang on evidence"——不可 grep）。spine 的 coverage 门是**字面可 grep**（pending 标记 / 字段空 / 每篇实例化行）——比 sci-write 的门更机械，是脚本的更好 fit。机械 enforcement → 机械测试，与 enforcement split 同构，内部一致。

### 关键替代方案与拒绝理由

- **一次提全 + 一次审**：拒绝。破坏依赖顺序，AI 在主线没定时猜框架；depth 门失焦。（§①）
- **clean baton + 单独 notes 文件 / spine 工作目录**：拒绝。违反父 spec"spine 无目录"且 churn 已合并 foundation；割裂作者审 depth 的审计面。（§②）
- **thesis级claim 并入主线（collapse）**：拒绝（round-2 collapse 被 round-3 否决）。丢掉总贡献的独立 depth-gate；偏离父 spec 显式 4-项枚举。umbrella 独立 depth-gated 第 4 项与父 spec 一致。（§③）
- **umbrella 归 coverage 桶**：拒绝（aquarius round-1 #3 抓到，round-3 修）。与 §③"umbrella 不参与 coverage 计数"自相矛盾；umbrella 归 depth 桶，coverage 只含 3 结构字段。（§③ + §门）
- **spine 直接绑 paper→chapter**：拒绝。深读依赖的绑定推到没深读的 spine，违反拆即写。（§④）
- **纯抽象递进、无角色**：拒绝。dissect 得到太少，没法 map。（§④）
- **tension-flagging 类比 figN-reading（事实核查）**：拒绝（aquarius round-1 否决）。false equivalence；honest 子集与 coverage 机械层重叠，独有价值是 depth-influence。（§⑤）
- **AI hard-gate 审架构 depth / 裁决"框架很浅"**：拒绝（父 spec 已定 + §⑤）。AI 无法诚实审计 depth；forbidden 的是裁决+auto-adopt。
- **drop tension-flagging**：拒绝（§⑤）。放弃 AI 唯一真实 edge（attachment 缺席），让作者独自对抗 attachment blind spot。
- **纯 eval 测试（mirror sci-write，无脚本）**：拒绝（§⑥）。spine coverage 门字面可 grep，比 sci-write interpretive 门更机械，配脚本更 fit。
- **pytest 测 prose**：拒绝（§⑥）。prose 主观输出，eval 才对。

---

## Implementation Notes

### thesis-spine.md schema（单一富 baton，落实 §② + §③ umbrella）

```markdown
# thesis-spine.md
> Baton. Settled by the author (depth human-gated). Read by dissect/intro/summary/theory.
> `pending` = AI candidate, NOT author-adopted. A field still marked `pending` is unsettled
> — dissect must not build on an unsettled field.

## Main line (主线)                       ← 串起 N 篇的 thread（结构字段，coverage-gated）
[pending? ] <one sentence: the thread connecting the N papers>

## Unified framework (统一框架)            ← 框架 + 每篇如何实例化它（结构字段，coverage-gated）
[pending? ] <the framework>
            per-paper: how paper-X instantiates it = …

## Inter-chapter progression (章间递进)      ← 研究章角色序列（默认 1:1）（结构字段，coverage-gated）
[pending? ] ordered:
            - role 1: question = …; advances the main line by …
            - role 2: question = …; advances the main line by …

## Thesis-level claim (umbrella)           ← 全篇一句话总贡献（depth-gated，非 coverage）
[pending? ] <one sentence: what the thesis establishes — the 3 structural fields collectively argue it>

## Boundary                                ← thesis-level claim 不 establish 什么（depth-gated，镜像 claim.md）
<where the thesis-level claim stops>

## Intake (per-paper evidence base)         ← spine 读小论文的依据（high-level only）
- paper-A: claim = …; structure = …; how it could fit a main line = …
- paper-B: …

## Cracks flagged (tension-flagging, §⑤)   ← attachment 盲点的 tension（提问非裁决）
- [stage 1 / main line] (a) tension: … (b) evidence: paper-C Fig3 §4.2 → ¬X (c) question: 是否 tension 主线的 X？
  disposition: [fatal → revised | dismissed → reason: …]   ← 作者处置，AI 不参与
- [stage 2 / framework] …

## Alternatives considered                  ← settled 时坍缩的候选（audit trail）
- main line: considered <alt>, rejected because <reason>
```

**product = 顶部 5 节**（main line / unified framework / inter-chapter progression / thesis-level claim / boundary）；**Intake / Cracks / Alternatives = evidence base + audit trail**（镜像 claim.md 的 evidence baseline 与 argument 同处一文件）。

### 工作流（落实 §①，5 步，Step 1–4 各一 depth 人工门）

- **Step 0 — Read the room（startup/resume）**：读 `thesis-sources.md`（registry；缺/空 → hard stop，"先跑 thesis-init 填 registry"——dissect 的 spine.md-存在边界的反向）；逐篇读小论文（tex/PDF per registry `paths`）做 **high-level intake only**（claim + IMRaD 结构 + 如何串主线 → 写 `## Intake`）；读 `template-spec.md`（章命名，让递进角色对齐模板）；从跨论文术语 **seed `thesis-terminology-ledger.md`**（标 `source: thesis-spine`）。resume 时若 spine.md 有 settled 节（无 `pending`），跳到第一个未 settle 的 stage。
- **Step 1 — Main line（主线 thread）**：AI 提主线候选（`pending`，串起 N 篇的 thread，grounded in intake）。AI tension-flags。**人工门（depth）** → `## Main line`。
- **Step 2 — Unified framework**：AI 提框架候选（`pending`，build on 主线——框架 + 每篇如何实例化）。AI tension-flags。**人工门（depth）** → `## Unified framework`。**Coverage 查（机械，check_spine.py）**：每篇声明实例化——缺 = contract gap，问作者。
- **Step 3 — Inter-chapter progression**：AI 提递进候选（`pending`——研究章**角色**序列，默认 1:1，每个：its question + how it advances the main line；paper-agnostic）。AI tension-flags。**人工门（depth）** → `## Inter-chapter progression`。**Coverage 查**：每个角色声明 advance + question。
- **Step 4 — Thesis-level claim (umbrella) + Boundary**：现在三结构字段已 settle，AI 提 umbrella 候选（`pending`——一句话总贡献，三结构字段 collectively argue 它）。AI tension-flags（overclaim 超出三字段实际 establish 的？hollow？）。定 `## Boundary`（umbrella 不 establish 什么）。**人工门（depth）** → `## Thesis-level claim` + `## Boundary`。
- **Step 5 — Handoff**：跑 `scripts/check_spine.py`（coverage 机械门：无 `pending` + 3 结构字段非空 + sub-coverage；umbrella 在 depth 桶，不在 coverage）；通过则 spine.md 是 settled baton。指向 **thesis-dissect**（绑 paper 到角色，拆即写）。**不 auto-run**（read neighbors, don't orchestrate）。

### 门与 enforcement（落实 §① + 父 spec §① 的三层 split + §③ umbrella 归 depth + §⑥ split）

- **Coverage（机械，`scripts/check_spine.py` + pytest）**：**3 结构字段**非空（主线/框架/递进）+ 各自 sub-coverage（framework: 每篇实例化；progression: 每角色 advance+question）+ **无 `pending` 残留**。对盘上 spine.md 可查。**umbrella 不在此层**（umbrella 是 depth，非机械）。
- **Depth（人工 only）**：主线 thread 够不够 sharp？框架 high-level 还是 hollow？递进够不够 insightful？**umbrella overclaim 吗 / hollow 吗？** AI **不能门**——会生成看似合理的确认。AI 提候选 / 拆逻辑 / tension-flags。**作者门 depth**（含 umbrella + boundary）。
- **tension-flagging 的诚实 residual（§⑤）**：tension-flagging 是 depth-INFLUENCE（AI framing bias 作者注意力），非 depth-gating（作者处置）。stated failure mode：attachment-blind 作者可能被 AI framing 带走。接受 + 命名，不假装消除。
- **诚实边界（父 spec §Load-bearing premise）**：文件交接（dissect 无 spine.md 进行不下去）防**缺席**不防**坏**。空洞 spine 能过 coverage + 作者确认（若作者判断力不足，attachment 盲点 + tension framing bias 叠加）——无结构性机制替代作者判断。诚实命名，不 overclaim。

### 跨 skill 文件交接（落盘文件耦合，无 skill 调 skill）

| 文件 | 产 | 读 | 作用 |
|---|---|---|---|
| `thesis-spine.md` | spine | dissect/intro/summary/theory | 主线+框架+递进+umbrella+boundary（接力棒，§schema）|
| `thesis-terminology-ledger.md` | spine **seed** | 各章/polish 共写 | 跨章术语统一（seeded entries `source: thesis-spine`）|
| `thesis-sources.md` *(读)* | init | spine | 来源 registry（paper_id/paths/slug/claim）|
| `template-spec.md` *(读)* | init | spine | 章命名约定（让递进角色对齐）|
| 小论文 *(读)* | external | spine | 每篇 claim + IMRaD 结构（high-level intake）|
| `scripts/check_spine.py` *(spine 自带)* | spine | spine Step 5 | coverage 机械门（确定性，pytest 测）|

**resume**：每个 session 先读 spine.md——settled（无 `pending`）vs in-flight；从第一个未 settle 的 stage 继续。Intake 落在 spine.md，resume 不重读论文。

### skill 位置 + 脚本

父 spec §插件形态已定：写作链 skill 住 `sci-skills-thesis/skills/`。thesis-spine 是第一个写作 skill——**落地时创建 `sci-skills-thesis` 插件**（foundation 未建，因无写作 skill；thesis-spine 是首个，落地时建插件 + 该插件首个 skill）。调用形如 `sci-skills-thesis:thesis-spine`。

**脚本**：`sci-skills-thesis/skills/thesis-spine/scripts/check_spine.py`（skill 自带源码，非项目 working dir）+ `test_check_spine.py`（stdlib，镜像 init 的 test 模式）。脚本只做 coverage 机械门（3 结构字段），不做 depth（umbrella + boundary 非脚本职责）。

---

## Acceptance

### 痛点是否消除（逐条对 Problem）

1. **主线+框架在拆章前定下来**：作者跑 thesis-spine，在 N 篇小论文基础上分级得到主线/框架/递进/umbrella 候选 + tension，逐级人工拍板落 `thesis-spine.md`。**验收**：`thesis-spine.md` 含主线（thread）+统一框架（每篇实例化）+章间递进（角色序列）+thesis级claim（umbrella）+boundary，`pending` 全清、四者作者确认（对齐父 spec acceptance §1）。
2. **架构 depth 不被 AI 毁**：depth 全程人工门控，AI 候选标 `pending` 不 auto-adopt；tension-flagging 是**提问非裁决** + 具体证据 + attachment 缺席。**验收**：spine.md 无 `pending` 残留且作者签字；tension 条目均含 (a)tension (b)specific evidence (c)question（非裁决）+ disposition（作者处置）。
3. **下游不在流沙上盖楼**：dissect 读 spine.md 才开跑（存在边界）；spine 的递进角色给 dissect 可绑定骨架。**验收**：dissect 的 chapter-map 能 bind paper→role（默认 1:1 + 少数合并/拆分），绑不上 fallback spine。

### 防带病推进机制（诚实边界）

- **可回退**：作者审框架时发现主线问题能回溯改主线 → 重提下游。**验收**：回溯后下游候选重新标 `pending`。
- **诚实边界**：decoupling 防**缺席**（spine.md 不存在 dissect 进行不下去）非**坏**（空洞 spine 能过门）——质量只靠 depth 人工门，依赖作者判断力；tension-flagging 的 framing bias 是叠加的 stated failure mode。**验收**：spec §门与 enforcement 明确命名此边界 + §⑤ 命名 tension residual，不 overclaim（对齐父 spec §Load-bearing premise）。
- **无 skill 调 skill**：所有跨 skill 交接经文件。**验收**：grep spine 无对兄弟 skill 的调用。
- **enforcement split 落地**：coverage 机械门（`check_spine.py` + pytest，**3 结构字段**+sub-coverage+无 pending）；depth 人工门（**含 umbrella + boundary**）。**验收**：两层各有归属，无 depth 用 AI auto-gate；umbrella 归 depth 桶非 coverage（§门 与 §③ 一致）；tension-flagging 是提问非裁决，不滑向 depth verdict。

### scope 边界（对齐父 spec v1）

- **spine 不深读论文**：high-level intake only（claim + 结构 + 如何串主线）；深读 + 拆 + 写章是 dissect。**验收**：spine 不产 `thesis/tex/*.tex`，不产 `chapter-map.md`（dissect 产）。
- **spine 不绑 paper→chapter**：列角色，dissect 绑定。**验收**：spine.md 递进节是角色序列，无 paper→chapter 绑定。
- **跨家族术语统一 out of scope**（父 spec v1 cut）：spine seed 的是 `thesis-terminology-ledger.md`，与 article 的 `sci-skills/sci-write/terminology-ledger.md` 独立。**验收**：spine 不碰 article ledger。

### 测试验收

- **`check_spine.py` + `test_check_spine.py`**：在 settled spine.md 上 pass；在含 `pending` / 空结构字段 / 缺实例化 / 缺 advance+question 的 spine.md 上 fail（stdlib assert，镜像 init test 模式）。**注意**：check_spine.py 只查 3 结构字段（coverage）；umbrella/boundary 空不在 check_spine.py 范围（属 depth，人工门）。
- **eval loop**（prose）：给定多论文 intake，spine 提 grounded 不空洞候选、标 `pending` 不 auto-adopt、tension 提问非裁决 + 具体证据、gate-fires-on-empty 行为。

### 对父 spec 的偏离

**无偏离需 re-review**。本 spec 是忠实细化：
- **单一富 baton**（§②）尊重父 spec"spine 无目录"且按 handoff 开放问题扩展 spine.md 内容——非偏离。
- **umbrella = depth-gated 第 4 项**（§③）**与父 spec 一致**——父 spec spine.md 内容（L126）+ acceptance（L190）明确把 thesis级claim 列为第 4 个 distinct 项，gate（L62/L159）"三字段 coverage + thesis级claim depth"。本 spec umbrella 即此第 4 项，归 depth 桶。round-1 把 umbrella 错放 coverage 桶（aquarius round-1 #3 抓到），round-3 修正归 depth——现 §门 与 §③ 一致，与父 spec 一致。
- **角色 + 默认 1:1**（§④）匹配父 spec dissect 的 chapter-map merge/split 支持。
- **tension-flagging**（§⑤）落实父 spec §① 的"AI 辅助 dispassionate 审视"，并诚实命名 residual 为 depth-influence（父 spec §Load-bearing premise 的具体落地，非偏离）。
- **coverage 脚本 + pytest**（§⑥）沿用 repo 已 justify 的 test deviation（init 已先例），非新偏离。
- **无 init 变更**（spine 无目录、单文件、无新共享文件）→ **不 churn 已合并 foundation**。

**glossary 与父 spec 的 pre-existing 张力**（非本 spec 引入，不 overclaim 解决）：glossary "Architecture-level claim" 列四个（主线/框架/递进/共性提炼），未单列 thesis级claim；父 spec spine 第 4 项 = thesis级claim。两者视图不同（glossary 是跨 spine+summary 视图，父 spec 是 spine 视图）。本 spec 产父 spec 定义的 spine 4 项；glossary 的对齐是 glossary 与父 spec 之间的事。
