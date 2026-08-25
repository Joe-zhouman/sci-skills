# Writing discipline

本 skill 的纪律（depth 层 + pending / tension 协议）。零依赖——这里是全部内容，不引用任何外部 skill 的文件。每个结构 stage（主线 / 框架 / 递进 / umbrella）settle 前打开。

## Confirmation gate（每级 settle 前对齐）

每个结构 stage 在 **settle 之前**，先回显一个对齐块，停下来等作者确认：

- **候选**（当前 stage 的 `pending` 候选，一句话）
- **它 build on 什么**（上一级已 settle 的字段——主线 build on Intake；框架 build on 主线；递进 build on 框架；umbrella build on 三结构字段 collectively）
- **tension(s)**（AI 在 `## Cracks flagged` 提的，三要素形态——见下节）
- **给作者的 depth 问题**（一个，只问当前 stage 的 depth）

per-stage depth 问题：
- 主线：thread 够不够 sharp？是真的统摄 N 篇，还是只是一个 label？
- 框架：high-level，还是 hollow？
- 递进：够 insightful，还是只是罗列？
- umbrella：overclaim 超出三字段实际 establish 的？hollow？boundary 诚实吗？

作者三选一：**确认**（删 `pending` 标记，settle）/ **改写**（改候选，重提本级）/ **驳回**（tension 成立 → 回溯上一级，下游重标 `pending`）。下一级只能 build on 已 settle 的字段；未 settle（仍 `pending`）的字段上不提下游候选。

镜像 sci-write 的 confirmation gate（写整章 prose 前先对齐），但 spine 的 gate 是架构级——不是"这段措辞对不对"，是"这个基座值不值得往上盖"。在错误基座上提框架、在错误框架上提递进，是逐级放大的猜测；gate 在最便宜的时机（settle 前）暴露基座错误。

## Tension-flagging（核心，spec §⑤）

AI 在 depth 层的唯一形态：**向作者提问，永不裁决。** 每个 stage 提完候选后，AI 在 `## Cracks flagged` 加一条。每条是**一个问题**，含三要素：

- **(a) tension**：提出的张力。例如"主线说 X 统一了 N 篇"。
- **(b) 具体证据**：触发 tension 的证据，**anchor 到具体 paper / figure / 段落**。例如"paper C 的 Fig 3 / §4.2 看似 claim ¬X"。不接受"论文里似乎有矛盾"这种无锚点的说法。
- **(c) 给作者的问题**：一个问句。例如"paper C 的 ¬X 是否 tension 主线的 X？若 tension 成立，主线是否需修订？"——**问题，不是裁决**。

### 永不裁决（forbidden forms）

以下形态**被禁止**——它们是 depth-gating（AI 裁决 depth）：

- "这个框架很浅 / 不够 high-level"
- "主线不够 sharp"
- "这个递进 weak / 只是罗列"
- "umbrella overclaim 了"（这该是问句，不是断言）

AI 生成它所检查的空洞——裁决"框架够不够深"的 AI，本身会产出看似合理的确认。forbidden 的是裁决 + auto-adopt；tension-flagging 只提问，作者判。

### 作者处置（AI 不参与）

每条 tension 由作者处置，二选一：

- **fatal → revised**：tension 成立，候选被修订（本级重提，或回溯上一级）。
- **dismissed → reason: …**：作者判断 tension 不成立，写明理由。例如"author 判断 ¬X 不 tension，因为 paper C 的 ¬X 是限定条件下的，主线 X 是一般情况"。

disposition 落 `## Cracks flagged` 作 audit trail。dissect / summary 继承的是"**作者知悉该 tension 并处置了**"这一记录，**不是 AI 裁决**。AI 不写 disposition，不替作者选。

### 诚实的 residual（aquarius round-1 load-bearing finding，必须明说）

**tension-flagging 是 depth-INFLUENCE，不是 depth-gating。** AI 决定**提哪些 tension**——这个选择本身就 bias 作者的注意力：attachment-blind 的作者可能被 AI 的 framing 带着走，只看 AI 提的、忽略 AI 没提的。这是**不可消除的 residual**：只要 AI 参与提 tension，就有 framing 影响。本 skill 诚实命名此 residual 为 stated failure mode，**不假装消除**。

- **与 forbidden 的区分**：forbidden 的是 AI **gate depth**（裁决"框架很浅"作为 verdict、或 auto-adopt 候选）。tension-flagging **不裁决、不 auto-adopt**——它提问，作者判。但**提问即影响**，这个 influence 是接受的、命名的、bounded 的。
- **AI 唯一真实 edge = attachment 的缺席**：作者对自己的工作有感情（投入），AI 没有。attachment 是真实的认知盲点（非白丁也有）；AI 的 attachment 缺席是它相对作者的**唯一真实 edge**。tension-flagging 保留这个 edge，不越界进 depth-gating。

### 为什么不 drop / 不 restrict 到 fact-check

- **drop** = 放弃 AI 唯一真实 edge，让作者独自对抗自己的 attachment blind spot。保留它 + 诚实命名 residual = 在"AI gate depth"（更糟）和"drop 辅助"（放弃 edge）之间取相对最优。
- **restrict 到可核查 fact-check** = 与 coverage / grounding 机械层**冗余**（机械层已查 cross-consistency）。tension-flagging 的独有价值**不是事实核查**——是 attachment 的缺席，即 depth-influence 本身。

### figN-reading 类比是 false equivalence（spec §⑤ 已否决，不要重犯）

不要把 tension-flagging 类比成 sci-write 的 figN-reading（"事实核查"）。**这是 false equivalence**：

- **figN-reading** 比较的是 prose vs rendered PNG——**两个具体 artifact 之间**的事实核查（正文说图显示 X，PNG 渲染出来是不是 X）。
- **tension-flagging** 比较的是框架抽象 vs 论文内容——**depth 判断**（这个框架够不够统摄这些论文）。

tension-flagging 的 honest 子集（可核查的 cross-consistency 事实）与 coverage / grounding 机械层**重叠**；它的独有价值（attachment-blind tension）**就是 depth-influence**。本 skill 接受这个 influence 并命名，而非假装它是无害的事实核查。**不要把 tension-flagging 写成 fact-check。**

## `pending` 协议

每个 AI 候选标 `pending`（字段值以 `[pending? ]` 开头）。作者**采纳 = 删掉 `[pending? ]` 标记**。仍标 `pending` 的字段 = 未 settle。

- **从不 auto-adopt**：AI 不替作者删 `pending` 标记，不把候选当已采纳往下走。
- **check_spine.py 在任何 `[pending` 标记上 fail**（Step 5 机械门）——dissect 不可建在 unsettled 字段上。
- 回溯时，下游候选**重新标 `pending`**（上一级改了，下游候选作废重提）。

这是 enforcement split 的落地：coverage 机械门（脚本查 `pending` 残留）+ depth 人工门（作者删标记 = 采纳 = depth 判断）。脚本只查"还有没有 pending"，不查"这个候选对不对"。

## 动词校准（按证据强度）

| 强度 | 动词 | 需要的证据 |
|---|---|---|
| 强 | establishes / shows / demonstrates | 三结构字段 collectively 直接支撑的论断 |
| 中 | suggests / indicates / supports | 趋势级、间接、单篇支撑 |
| 弱 | may / could / might | 合理但未验证的机制推测 |

强动词配弱证据 = 审稿人挑刺的靶子。弱动词配强证据 = 低估贡献。**umbrella 的 declaration 用强动词**（它是总贡献的断言，三字段 collectively argue 它）——不要在 umbrella 里塞 hedge（"may establish" = 不是 umbrella，是猜测）。tension 的 evidence 描述用中性动词；tension 本身是问句，不是断言。

## 诚实的边界（spec §Load-bearing premise）

文件交接（dissect 无 spine.md 进行不下去）防**缺席**，不防**坏**。

- **防缺席**：spine.md 不存在 → dissect 进行不下去 → 硬边界。
- **不防坏**：空洞的 spine 能过 coverage（3 结构字段非空 + 无 pending + sub-coverage）+ 作者确认——**若作者判断力不足**（attachment 盲点 + tension framing bias 叠加），hollow spine 照样 settle，下游照样在流沙上盖楼。

**无结构性机制替代作者判断。** coverage 脚本查不了"框架 hollow 吗""umbrella overclaim 吗"——这些是 depth，人工 only。tension-flagging 帮作者看见盲点，但它的 framing bias 是叠加的 stated failure mode，不是消除。本 skill 诚实命名此边界，**不 overclaim**——不假装 spine settle = spine 好。
