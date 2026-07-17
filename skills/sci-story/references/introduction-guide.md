# Introduction Guide — 两阶段漏斗

Introduction 不是单层五段——是两段漏斗。第一段从领域收到方向级 gap（"为什么这个方向值得做"）。第二段从方向现状收到研究级 gap（"具体缺什么 + 我们怎么做"）。两段之间靠转折词衔接，不是总结词。

## Stage 1: 领域级漏斗（"为什么这个方向重要"）

```
大背景 (1-2句, ≥3篇引文簇)
  → 小背景 + 现状 (1-3段, 逐级收窄)
  → Prior work (穿插在叙事中, 每个 claim 有出处)
  → Gap (方向级断层)
  → 跳板 (自然过渡到 Stage 2)
```

### Layer 1: 大背景

一句话定调。至少三篇引文从不同角度合力支撑一个 claim——"AI 导致算力暴涨"不能只靠一篇综述，需要算力需求、功耗上升、硬件现状各一篇独立出处。一个具体数字锚定可信度（`500 W cm⁻²`）。

引文策略：见 `literature-search.md` → Layer 1。搜 `[领域关键词] review` 给方向，再用 `[领域关键词] [具体子方向]` 找独立来源。Q1/一区优先。

### Layer 2: 小背景 + 现状

从那个数字逐级收窄到核心概念。归类，不罗列——"Current approaches fall into two categories: [A 类] which [优势] but [局限], and [B 类] which [优势] but [局限]." 每步有引文。

引谁：Q1/一区优先。筛选标准：这篇文献是否代表当前最佳实践？不是就不配出现在这里。Q2 但高度相关的可以引但不要为主。

### Layer 3: Prior work

穿插在叙事中，每个 claim 有出处。不是"Vu 做了什么、Chanda 做了什么"的链表——是论据嵌入叙事。一篇论文可以为一个 claim 提供证据的同时，为另一个 claim 留下缺口。

### Layer 4: Gap（方向级断层）

**Gap 不能多——只找最核心的那个。** 不是"领域有三个问题"，是"三个问题的根源是同一个东西"。所有提到的瓶颈必须能收敛到一句 gap 句子。收不拢 → gap 太多了，删到剩一个。

**写断层，不写空白。** "the wealth of data... remains largely disconnected from actionable design guidance"——不是"没人研究过 TCR"，而是"数据有了但没人把它变成可用的工程指导"。这是结构性的 mismatch，不是文献空白。审稿人无法用"你漏了这篇"怼回来。

Gap 不能模糊（"despite these advances, challenges remain"——什么 challenges?），不能太弱（"there is still room for improvement"——等于没说）。

### Layer 5: 跳板

最后一句是天然跳板——"Transforming... has emerged as a central challenge" → 下一段自然是"谁来填这个缺口"。**不要总结，要转折。**

---

## Stage 2: 研究级漏斗（"具体缺什么 + 我们怎么做"）

```
转折 ("In contrast, ML/DL...")
  → 方向大背景 (ML/DL 在这个领域的应用现状)
  → 小背景 + 现状 (三个具体问题, 每个有引文簇)
  → Prior work (按问题聚类, 不按时序)
  → Gap (研究级断层——比 Stage 1 的 gap 更窄更具体)
  → Present study (框架级预览)
```

### Layer 1: 转折 + 方向大背景

"In contrast, ML/DL..."——不是 "Therefore, we use ML/DL"（那是在乞题），不是 "ML/DL has been applied to TCR"（那是平板叙述）。"In contrast" 把 Stage 1 的结构性缺口和 Stage 2 的方法能力对位——"你缺的东西，这个方法天然能补，但还差一点。"

### Layer 2: 小背景 + 现状

列出 Stage 2 方向的具体问题——不是泛泛的"challenges remain"，是分成可操作的问题簇。比如："(a) material characterization inadequate, (b) black-box uninterpretable, (c) cannot distill reusable insights"。每个问题有引文支撑。

### Layer 3: Prior work

**聚类，不按时序。** 不是"Vu 做了什么。Chanda 做了什么。Feng 做了什么。"——是"材料表征问题（Vu, Zhou, Feng）→ 黑箱问题（Vu, Chanda, Feng）→ insight gap（全体）"。一篇论文可以同时出现在多个问题下——因为它确实可以同时有两个局限。Prior work 的职责不是介绍每篇论文，是归纳这个方向共同的欠缺点。

公平对待。"Although X showed Y, they did not address Z."——不贬低式对比。

引谁：相关性 > 期刊等级。高度相关且审稿人会追问的 Q2 论文必须引。但要是正经 peer-reviewed 期刊，不是 arXiv 预印本或会议摘要冒充的。

### Layer 4: Gap（研究级断层）

比 Stage 1 的 gap 更窄、更具体。**Gap 不能多——只找核心的那个。** "他用了 scikit-learn，你用了 XGBoost"不算 gap。"他用了 XGBoost，你提了一个新算法"才算。不是所有差异都是 gap——只有从 claim 倒推回来、必须填的那个洞才是。

Gap 的粒度决定论文格局。"ML models predict but don't explain, and thermal designers are left with numbers not insights"——不是"预测不够准"（那是在做一个更好的 predictor），是"预测了但没给指导"（那是范式转换）。同样的数据、同样的方法——gap 写窄了整篇论文就窄了。

### Layer 5: Present study

框架级预览，不是 mini-Methods。"First, a material representation strategy... Second, two architectural variants... Beyond prediction, the framework leverages..."——读者知道你要做什么、怎么做、为什么这样做，但不需要知道具体参数。写太多 → 审稿人跳过 Methods。写太少 → 审稿人不确定你做不做得到。

---

## 完整实例（用户真实 Introduction）

### Stage 1（领域级 — "为什么这个方向重要"）

> The rapid advancement of artificial intelligence technologies has exponentially increased the computational power demands of large language models (Li, Hao & Song 2025), driving a sharp rise in hardware power consumption (Chen, Wu, Chan et al. 2023; Huang et al. 2024).

**注**：三篇引文从不同角度（算力需求 / 功耗上升 / 硬件现状）合力支撑一个 claim。一句定调，不铺背景。

> Modern AI accelerators, such as GPUs and TPUs, now operate at heat flux densities exceeding 500 W cm⁻² (Ye et al. 2025), pushing thermal management to the forefront of electronic system design.

**注**：一个具体数字（500 W cm⁻²）锚定整段可信度 —— 从 AI 大势收窄到散热问题。

> In such high-power-density environments, the total thermal resistance along the heat dissipation pathway has become the critical bottleneck (Lee, Henderson, Reip et al. 2022; Yang, Deng, Li et al. 2024). Heat flux must traverse multiple heterogeneous material interfaces, where the thermal contact resistance (TCR), defined as the temperature drop across the interface between two contacting solids, often substantially exceeds the bulk material thermal resistance (Xing, Xu, Song et al. 2022; Wei et al. 2024).

**注**：逐级收窄 —— 散热 → 热阻 → TCR。TCR 的定义嵌在叙事里（不是脚注）。每步有引文。

> TCR is governed by the coupled physics of microscale asperity deformation, mesoscale contact area distribution, and macroscale heat flux conduction. This multi-scale nature places TCR squarely at the intersection of contact mechanics and interfacial heat transfer (Pastewka, Vakis, Aghababaei et al. 2025; Sun et al. 2024).

**注**：解释为什么 TCR 难搞 —— 多尺度物理交叉。为接下来的后果链铺路。

> Excessive TCR leads to localized hotspot temperature spikes (Krishnan & Jain 2023), accelerating electromigration in semiconductor devices (Haghbayan, Miele, Mutlu et al. 2023) and causing thermo-mechanical fatigue (Yu et al. 2024), which directly degrade the computational performance and reliability of CPUs and GPUs.

**注**：三层后果链（hotspot → 电迁移 → 疲劳），每个后果独立引文。从头到尾闭环：AI 算力 → 散热 → TCR → 器件失效。

> Precise prediction and management of TCR is therefore not merely a thermal engineering problem but a task that demands simultaneous reasoning over material chemistry, surface morphology, and multi-physics operating conditions. Yet, in current design practice, the wealth of experimental and simulation data generated across these dimensions remains largely disconnected from actionable design guidance (Meng et al. 2022; Wei et al. 2024).

**注**：【Gap — 断层型】不是 "没人研究过 TCR"，而是 "数据有了但没变成工程指导"。这是结构性的 mismatch，不是文献空白。

> Transforming multi-source interfacial data into structured, reusable engineering insights has therefore emerged as a central challenge for intelligent thermal management.

**注**：【跳板】不是总结，是转折 —— 自然过渡到 "In contrast, ML/DL..."

---

### Stage 2（研究级 — "具体缺什么 + 我们怎么做"）

> In contrast, machine learning and deep learning, as data-driven top-down modeling approaches, leverage their powerful high-dimensional nonlinear mapping capabilities to effectively integrate multi-source experimental and simulation data (Wang et al. 2023).

**注**：【转折】"In contrast" —— 不是 "Therefore"、不是 "In summary"。Stage 1 说数据脱节，Stage 2 说 ML 天然能补。

> In recent years, these methods have garnered increasing attention in the field of thermal management... Vu et al. (2021) applied four ML algorithms to predict TCR at glass–steel interface. Chanda et al. (2019) developed ANN for inverse TCR determination. Feng et al. (2022) investigated TCR of copper under cyclic loading via ANN. Zhou et al. (2025) used CNN for surface morphology → TCR with feature visualization. Zhou et al. (2025) constructed a TCR database with multiple ML algorithms and interpretability analysis. Bouchot et al. (2024) applied ML to friction from third-body morphology. Kelley et al. (2024) predicted elastohydrodynamic film thickness. Marian & Tremmel (2023) identified physics-informed ML as a promising direction.

**注**：7 篇 Prior work 系统梳理，不是按时间排序的链表，而是穿插在叙事中的论据。这里为节省篇幅用摘要式列举——实际写作应融入叙事。

> ...However, their value remains predominantly measured by predictive accuracy, with the deeper question of what engineering insights can be extracted from the learned representations still largely unaddressed.

**注**：【研究级 Gap — 断层型】不是 "预测不准"，而是 "预测了但没给解释"。

> Despite significant advances, their application still faces several critical limitations: (a) inadequate material characterization — existing studies overlook intrinsic material properties (Vu 2021; Zhou 2025; Feng 2022) or use one-hot encoding that lacks physical embedding (Zhou 2025); (b) black-box characteristics — opaque internal parameter interactions hinder interpretation (Vu 2021; Chanda 2019; Feng 2022); (c) inability to distill reusable engineering insights — thermal designers get numerical outputs but no understanding of the dominant physical mechanisms.

**注**：Prior work 按问题聚类，不按时序。同一篇论文出现在多个问题下（Vu 同时在 a 和 b，Zhou 同时在 a 和 c）——因为一篇论文确实可以有多个局限。

> To bridge the gap between data and design guidance, this study introduces an attention-based deep learning framework for TCR prediction that combines elemental-composition-based material encoding with an architecture capable of revealing its internal reasoning.

**注**：【Present study — 一句话总结】"To bridge the gap" 直接回扣 gap。

> First, a material representation strategy grounded in elemental mass fractions embeds chemical identity into a continuous, physically meaningful manifold, enabling generalization beyond previously seen material systems. Second, two architectural variants systematically evaluate how physical prior knowledge shapes feature interaction learning — Model A with explicit prior, Model B with autonomous discovery. Beyond prediction, the framework leverages multi-head attention visualization to trace feature-level reasoning pathways, and manifold learning (t-SNE, UMAP) to reveal the emergent structure of learned representations, automatically constructing a physicochemical similarity map.

**注**：【框架级预览 — 不是 mini-Methods】三个贡献：材料编码（Why）→ 两个变体对比（How we know）→ 可视化解释（So what）。读者知道架构但不知道参数细节。

> The outcome is not merely a high-accuracy prediction tool, but an interpretable framework that provides physically grounded guidance for material selection and thermal interface design in high-power-density electronics.

**注**：【收口】不是 better predictor，是 design guidance framework。Gap 的粒度 = 论文的格局。

---

## Drafting 规则

1. **一段一个 message。** 各层分家，不要塞在一起。
2. **第一句定调。** 段首句是该段的 claim，后续句支撑它。
3. **一个具体数字锚定可信度。** 数字来源可追溯到引文。
4. **Gap 写断层，不写空白。** 断层型 = "数据在这里，决定在那里，没人连接"。空白型 = "没人研究过 X"。断层是结构洞见，空白是文献没搜够。
5. **两段之间用转折词，不用总结词。** "In contrast" / "Despite" / "However"——不是 "In summary" / "Therefore"。
6. **Prior work 按问题聚类，不按时序。** 一篇论文可以出现在多个问题簇下。引文的职责是归纳共同缺口，不是罗列。
7. **公平对待前人。** "Although X showed Y"——不贬低式对比、不制造假 novelty。
8. **Present study 是框架级预览。** 不是 mini-Methods，不是摘要。读者读完应该知道你的架构、为什么这样设计、跟现有方法的本质区别——但不需要知道参数细节。

## 顶刊标准（不区分目标期刊——求其上者得其中）

以下来自 Nature 对 Introduction 的硬要求，但适用于所有期刊：用顶级期刊的逻辑写自己的文章，投到哪里都不吃亏。

- 前 1-2 句必须能跨学科阅读。如果命名的第一个专有名词是一个基因/蛋白/材料名，太窄了。
- 一句不可错过的 gap 铰链句。"However, ... remains unknown" 或其等价形式。
- "Here we show" 的位置：不早于 gap 句、不晚于段落中部。
- 结尾是 bounded significance，不是口号。

## 常见失败模式

| 失败 | 修法 |
|---|---|
| 单段漏斗（Stage 1 直接跳到 Present study） | 加 Stage 2——领域缺口之后必须说已经有什么、还差什么 |
| Gap 是空白型 | 改断层型——不是"没人做过"，是"有人做了但数据和指导之间有结构性断层" |
| Prior work 是链表 | 按问题聚类重写——"同一篇论文可以在不同问题下出现" |
| 两段之前用"In summary"连接 | 改成"In contrast"——转折不是总结 |
| Present study 堆方法细节 | 砍到框架级——架构 + 为什么这样设计 + 跟现有方法的区别 |
| Opening 专有名词太密 | 前两句不用专业术语——Nature 审稿人跨领域，别让他们第一句就放弃 |

## 从 writing drafts 搬素材

- `results.md` → 主发现（写 Present study 时参考）
- `conclusion.md` → 贡献声明（Present study 的锚）
- `method.md` → 数据/样本背景（写研究背景时可以提一句）
- `figN-report.md` / `figN-reading.md` → Core conclusion（主 claim 参考）
- `paper-plan.md` → 图清单 = 贡献清单的骨架
