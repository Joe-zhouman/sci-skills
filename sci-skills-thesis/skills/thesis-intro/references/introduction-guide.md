# Introduction Guide — 论文级两阶段漏斗（N gaps → N chapters）

本 skill 在 Step 1 confirmation gate 打开本文件——指导绪论的漏斗结构与 gap articulation。镜像 sci-story 的 `introduction-guide.md` 升尺度到 thesis，落实 spec §①（Narrative gap）+ §②（gap→章 structural commitment）。

绪论（`thesis/tex/ch0-intro.tex`）不是单篇 article 的 introduction——article 的漏斗收敛到 **1 个 gap → 1 个 response**（同一篇内 Intro→Discussion）；thesis 的漏斗收敛到**主线**（从 `thesis-spine.md`），沿路 articulate **N 个 narrative gap**——每个对应一个正文章（glossary Narrative gap："typically one per body chapter"）。

---

## The thesis-scale funnel（N gaps → N chapters，NOT 1 gap）

**目的**：命名 thesis 漏斗与 article 漏斗的本质区别——N 个 gap，不是 1 个。

| | article (sci-story) | thesis (intro) |
|---|---|---|
| 收敛到 | 1 个 core gap | 主线（从 spine.md） |
| Gap 数 | 1 | N（typically one per body chapter） |
| Gap 对应 | 1 个 response（同篇 Discussion） | N 个正文章（dissect 已写 chN.tex） |
| Gap 类型 | 断层（structural mismatch） | 断层（structural mismatch），thesis-scale |
| 漏斗段数 | 2 段（Stage 1 + Stage 2） | 2 段（Stage 1 + Stage 2），每段 thesis 尺度 |

**关键纪律**：

- **N 个 gap，不是把所有差异堆成一个**。"他用了 scikit-learn，你用了 XGBoost"不算 gap——只有从主线倒推回来、必须填的那个洞才是。每个 gap 对应一个正文章填。
- **gap 是 narrative gap**（研究现状断层——"领域缺什么，正文第 N 章填了什么"），**不是** spine 的 inter-chapter progression role-question（"第 N 章如何推进主线"——结构层，已在 chapter-map.md）。一个 role 可能对应一个 narrative gap，但 framing 不同（spec §①）。
- **主线 narrate 不 re-gate**：主线/框架/umbrella 在 spine 人工门控 settle，intro narrate 不 re-gate（re-gate 冗余，C2 拒）。漏斗是把已 settle 的主线讲成连贯研究方向，不是重新论证主线。

---

## Stage 1: 领域级漏斗（"为什么这个方向重要"）

```
大背景 (1-2句, ≥3篇独立引文从不同角度合力)
  → 小背景 + 现状 (逐级收窄, 一个具体数字锚定)
  → Prior work (穿插在叙事中, 每个 claim 有出处)
  → Gap (方向级断层——框住整篇论文, 非 article 级)
  → 跳板 (转折到 Stage 2, 不是总结)
```

### Layer 1: 大背景

一句话定调。**至少三篇独立来源从不同角度合力支撑一个 claim**——不是一篇综述包打天下，是算力需求、功耗上升、硬件现状各一篇独立出处。一个具体数字锚定可信度（`500 W cm⁻²`）。

引文策略：见 `references/literature-search.md` → Layer 1。搜 `[领域关键词] review` 给方向，再用 `[领域关键词] [具体子方向]` 找独立来源。Q1/一区优先。

**thesis 尺度**：大背景框住**整篇论文**的领域——选能跨 N 章共领域的 umbrella 文献，不是单章领域。

### Layer 2: 小背景 + 现状

从那个数字逐级收窄到核心概念。归类，不罗列——"Current approaches fall into two categories: [A 类] which [优势] but [局限], and [B 类] which [优势] but [局限]." 每步有引文。

引谁：Q1/一区优先。筛选标准：这篇文献是否代表当前最佳实践？不是就不配出现在这里。Q2 但高度相关的可以引但不要为主。

### Layer 3: Prior work

穿插在叙事中，每个 claim 有出处。不是"Vu 做了什么、Chanda 做了什么"的链表——是论据嵌入叙事。一篇论文可以为一个 claim 提供证据的同时，为另一个 claim 留下缺口。

**thesis 尺度（B3 heuristic）**：Layer 3 的 prior work 分两路——章级 callback from chN.tex（dissect 已落地）+ 论文级 real-DOI search。gray zone 在 gate 裁决。见 `references/literature-search.md`。

### Layer 4: Gap（方向级断层）

**Gap 不能多——只找核心的那个。** 不是"领域有三个问题"，是"三个问题的根源是同一个东西"。所有提到的瓶颈必须能收敛到一句 gap 句子。收不拢 → gap 太多了，删到剩一个。

**写断层，不写空白**（见"Gap 写断层，不写空白"节）。

Gap 不能模糊（"despite these advances, challenges remain"——什么 challenges?），不能太弱（"there is still room for improvement"——等于没说）。

**thesis 尺度**：Stage 1 的 gap 框住**整篇论文**的方向（不是 article 的单篇方向）——它要能 umbrella N 个正文章的共同方向。

### Layer 5: 跳板

最后一句是天然跳板——"Transforming... has emerged as a central challenge" → 下一段自然是"谁来填这个缺口"。**不要总结，要转折。**

---

## Stage 2: 研究级漏斗（"具体缺什么 + 我们怎么做"）

```
转折 ("In contrast, ...")
  → 方向大背景 (统一框架/方法在这个领域的应用现状)
  → 小背景 + 现状 (N 个具体问题, 每个有引文簇)
  → Prior work (按问题聚类, 不按时序)
  → Gap (研究级断层——比 Stage 1 更窄更具体)
  → Present study (框架级预览 THESIS 结构: N 章如何集体填 gaps)
```

### Layer 1: 转折 + 方向大背景

"In contrast, ML/DL..."——不是 "Therefore, we use ML/DL"（那是在乞题），不是 "ML/DL has been applied to TCR"（那是平板叙述）。"In contrast" 把 Stage 1 的结构性缺口和 Stage 2 的方法能力对位——"你缺的东西，这个方法天然能补，但还差一点。"

**thesis 尺度**：转折不是"我们用方法 X"，是"主线框架（spine 定的 unified framework）天然能补 Stage 1 的缺口"。

### Layer 2: 小背景 + 现状

列出 Stage 2 方向的具体问题——不是泛泛的"challenges remain"，是分成可操作的问题簇。比如："(a) material characterization inadequate, (b) black-box uninterpretable, (c) cannot distill reusable insights"。每个问题有引文支撑。

**thesis 尺度**：N 个问题簇 typically 对应 N 个正文章——每个问题是一个 narrative gap 的研究现状侧。

### Layer 3: Prior work

**聚类，不按时序。** 不是"Vu 做了什么。Chanda 做了什么。Feng 做了什么。"——是"材料表征问题（Vu, Zhou, Feng）→ 黑箱问题（Vu, Chanda, Feng）→ insight gap（全体）"。一篇论文可以同时出现在多个问题下——因为它确实可以同时有两个局限。Prior work 的职责不是介绍每篇论文，是归纳这个方向共同的欠缺点。

公平对待。"Although X showed Y, they did not address Z."——不贬低式对比。

引谁：相关性 > 期刊等级。高度相关且审稿人会追问的 Q2 论文必须引。但要是正经 peer-reviewed 期刊，不是 arXiv 预印本或会议摘要冒充的。

**thesis 尺度（B3 heuristic）**：章级 prior work callback from chN.tex；论文级 prior work real-DOI search。gray zone 在 gate 裁决。

### Layer 4: Gap（研究级断层）

比 Stage 1 的 gap 更窄、更具体。**Gap 不能多——只找核心的那个。** "他用了 scikit-learn，你用了 XGBoost"不算 gap。"他用了 XGBoost，你提了一个新算法"才算。不是所有差异都是 gap——只有从主线倒推回来、必须填的那个洞才是。

Gap 的粒度决定论文格局。"ML models predict but don't explain, and thermal designers are left with numbers not insights"——不是"预测不够准"（那是在做一个更好的 predictor），是"预测了但没给指导"（那是范式转换）。同样的数据、同样的方法——gap 写窄了整篇论文就窄了。

**thesis 尺度**：Stage 2 的 gap 是研究级断层——比 Stage 1 的方向级 gap 更窄。每个 gap 对应一个正文章填（见"Gap → chapter mapping"节）。

### Layer 5: Present study（框架级预览 THESIS 结构）

**thesis 尺度的关键区别（vs article）**：article 的 Present study 是**单篇 paper 的方法预览**（"First, a material representation strategy... Second, two architectural variants..."）；thesis 的 Present study 是**THESIS 章节结构的框架级预览**——N 章如何集体填 N 个 gaps、推进主线。这是 spine.md 的 progression roles 的叙事化。

**不是 mini-Methods**——读者知道 N 章各自做什么、为什么这样组织、跟现有方法的本质区别——但不需要知道每章的参数细节。写太多 → 审稿人跳过正文。写太少 → 审稿人不确定你做不做得到。

**主线 callback**：Present study 要 callback spine.md 的主线（narrate 不 re-gate）——主线是 spine settle 的架构级 claim，Present study 把它讲成"本论文 N 章如何推进主线"。

---

## Gap 写断层，不写空白

**目的**：这是 gap-depth 判断的核心。命名清楚两类 gap 的区别。

- **断层（structural mismatch）**："the wealth of data... remains largely disconnected from actionable design guidance"——数据有了但没人把它变成可用的工程指导。**结构性 mismatch**，不是文献空白。
- **空白（literature gap）**："没人研究过 X"——文献没搜够。

**为什么断层面不能空白菜**：

- 断层**不能**被审稿人用"你漏了这篇"怼回来——因为你说的是"数据有了但没变成指导"，不是"没人做过"。
- 空白**能**被怼——审稿人甩出一篇你没引的论文就破了"没人做过"。
- 断层是结构洞见，空白是文献没搜够。

**Gap depth 是 author-judged residual，非 gate-enforced**（spec §④）：

- confirmation gate 查 **framing alignment**（这节讲什么、提哪些 gap、哪些章填），**不**查 gap 是断层还是空白。
- 判断 gap 是断层还是空白 = **depth**，作者在 gate 上判断的 residual，非 gate 本身 enforce。
- 一个 framing 准但 gap 是空白型的研究现状能过 gate（若作者工艺判断失准）。这是 intro 的固有边界（见 `references/writing-discipline.md` → 诚实边界）。

---

## Gap → chapter mapping（the structural commitment，spec §②）

**目的**：命名 articulating 每个 gap 时的 structural commitment——gap→章 cross-reference。

**纪律**：

- 在漏斗里 articulate 每个 gap 的同时，你 commit 它 → 填它的正文章（discovered cross-reference to existing chapters via `chapter-map.md`）。
- **章已存在**（dissect 已写 chN.tex）——mapping 是 **discovered**（章的 framework-instantiation 是否填该 gap 可从 chapter-map.md 查），非 **generated**。
- 这个 mapping **写后记录**在 `gap-map.md`（Step 3）+ 其 `callback-anchor`（给 summary）。
- **这是 pre-write structural commitment**——约束 prose（"你说 gap X→章 Y，所以 gap-X prose 要 set up 章 Y 的贡献"）。named residual，非 round-1 的 "framing vs coverage" false binary（见 `references/writing-discipline.md` → Step 1 pre-write structural commitment）。

**Narrative goal (NOT enforced by check_intro.py)**：

漏斗的 N 个 gap 应该**集体覆盖**正文章的贡献——一个正文章若填不了任何 articulated gap，在绪论里就是 unmotivated 的。

- **作者应该在 confirmation gate 上处理这个**：要么 articulate 该章填的 gap，要么重新考虑该章是否属于本论文。
- **check_intro.py 不查 chapter→gap（每章是否填了 gap）**——它只查 gap→chapter（每个 gap 有 filled-by + filled-by 章存在于 chapter-map.md）。
- chapter→gap 方向是 **author-judged at the gate**，**不是**机械的"required structural element" coverage check（spec §①：intro 的 gate 是 near-trivial consistency，非 spine/dissect 那种"required 元素在不在"的 coverage）。
- **诚实命名**：不要 overclaim"每章必须填一个 gap"为 enforced requirement——它是 narrative goal，靠作者 gate judgment，非脚本 enforce。round-1 spec 把它当 enforced coverage 是 overclaim（aquarius finding 4），round-2 修正。

**status=unfilled**：若 gap 无章填 → `gap-map.md` 记 `status=unfilled` → surfaced 给作者（contract gap：要么 thesis 有洞，要么从 intro 砍该 gap）。

---

## Drafting 规则（mirror sci-story）

1. **一段一个 message**。各层分家，不要塞在一起。
2. **第一句定调**。段首句是该段的 claim，后续句支撑它。
3. **一个具体数字锚定可信度**。数字来源可追溯到引文。
4. **Gap 写断层，不写空白**（见上节）。断层型 = "数据在这里，决定在那里，没人连接"。空白型 = "没人研究过 X"。断层是结构洞见，空白是文献没搜够。
5. **两段之间用转折词，不用总结词**。"In contrast" / "Despite" / "However"——不是 "In summary" / "Therefore"。
6. **Prior work 按问题聚类，不按时序**。一篇论文可以出现在多个问题簇下。引文的职责是归纳共同缺口，不是罗列。
7. **公平对待前人**。"Although X showed Y"——不贬低式对比、不制造假 novelty。
8. **Present study 是框架级预览 THESIS 结构**。不是 mini-Methods，不是单篇方法摘要。读者读完应该知道 N 章各自做什么、为什么这样组织、跟现有方法的本质区别——但不需要知道参数细节。
9. **主线 callback**。Present study 要 narrate spine.md 的主线（narrate 非 re-gate）——主线是 spine settle 的架构级 claim。

---

## 顶刊标准（不区分目标期刊——求其上者得其中）

以下来自 Nature 对 Introduction 的硬要求，但适用于所有期刊：用顶级期刊的逻辑写自己的论文，投到哪里都不吃亏。

- 前 1-2 句必须能跨学科阅读。如果命名的第一个专有名词是一个基因/蛋白/材料名，太窄了。
- 一句不可错过的 gap 铰链句。"However, ... remains unknown" 或其等价形式。
- "Here we show" 的位置：不早于 gap 句、不晚于段落中部。
- 结尾是 bounded significance，不是口号。

---

## 常见失败模式（mirror sci-story，thesis-scaled）

| 失败 | 修法 |
|---|---|
| 单段漏斗（Stage 1 直接跳到 Present study） | 加 Stage 2——领域缺口之后必须说已经有什么、还差什么 |
| Gap 是空白型 | 改断层型——不是"没人做过"，是"有人做了但数据和指导之间有结构性断层" |
| Prior work 是链表 | 按问题聚类重写——"同一篇论文可以在不同问题下出现" |
| 两段之前用"In summary"连接 | 改成"In contrast"——转折不是总结 |
| Present study 堆方法细节 | 砍到框架级——N 章结构 + 为什么这样组织 + 跟现有方法的区别（不是单篇方法） |
| Opening 专有名词太密 | 前两句不用专业术语——Nature 审稿人跨领域，别让他们第一句就放弃 |
| Gap 数量与正文章不匹配 | N 个正文章 → typically N 个 narrative gap。多了 → 砍到剩核心；少了 → 有章填不了 articulated gap，回 gate 处理（见 Gap → chapter mapping） |
| Present study 没 callback 主线 | narrate spine.md 的主线（非 re-gate）——主线是架构级 claim，Present study 把它讲成"N 章如何推进主线" |

---

## 从邻居搬素材

- `thesis-spine.md` → 主线 + 框架 + umbrella + progression roles（Present study 的锚；narrate 非 re-gate）
- `chapter-map.md` → 各章 role + papers + framework-instantiation（gap→章 mapping 依据）
- `thesis/tex/chN.tex` → 正文章（callback 章级 prior work + 确认 gap→fill）
- `thesis-terminology-ledger.md` → canonical 术语（写时 enforce + extend）
- `references/literature-search.md` → 引文搜索策略（B3 heuristic + gray zone at gate）
- `references/writing-discipline.md` → 写作纪律（confirmation gate + real-DOI + 诚实边界）
