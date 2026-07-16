# Introduction Guide — 漏斗结构 + 段落职责

Introduction 的目的：告诉读者为什么这个工作重要、填了什么 gap、回答了什么 question。
结构是漏斗——从 field 的广泛重要性，逐层收窄到具体 gap，再收窄到本研究。

## 漏斗结构（五层）

**每一层是一个或多个段落。每个段落只有一个 job。**

### Layer 1: 大背景（field stake, 1-2 句）

- job: 为什么这个领域值得关心？一句话定调，至少三篇引文从不同角度合力支撑。
- 引谁: Q1 / 一区优先。一篇综述可以给领域定调，但具体论据需要多篇独立来源——"AI 导致算力暴涨"不能只靠一篇综述，需要算力需求、功耗上升、硬件现状各一篇独立支撑。
- 引文策略: 见 `references/literature-search.md` — 优先学术搜索 MCP，退到通用搜索。

### Layer 2: 小背景 + 现状（bottleneck, 1-3 段）

- job: 当前 SOTA 是什么？共同过不去的坎在哪？归类，不要一个方法一个方法罗列。
- 引谁: Q1 / 一区优先。核心筛选：这篇文献是否代表当前最佳实践？不是就不配出现在 bottleneck 论证里。Q2 但高度相关的——可以引但不要为主。
- 引文策略: 搜 `[子领域] [方法关键词] recent advances`、`[瓶颈关键词] limitation`。
- 正确: "Current approaches fall into two categories: [A 类] which [优势] but [局限], and [B 类] which [优势] but [局限]. Neither addresses [关键瓶颈]."

### Layer 3: Prior work（最直接相关的前人工作）

- job: 跟你正面对话的几个工作——它们做到了什么、留了什么缺口。
- 引谁: 质量不如相关性重要——高度相关且审稿人会追问的必须引。但要是正经 peer-reviewed 期刊，不是 arXiv 预印本或会议摘要冒充的。
- 写法: 公平对待——"Although X showed Y, they did not address Z." 不要贬低式对比。
- 引文策略: 搜 `[具体技术/方法名] [你的问题域]`。搜完读摘要确认真的相关——不要看标题就引。

### Layer 4: Gap（缺口）

- job: 这必须是一句明确的、可验证的 gap statement。不能模糊、不能让读者去猜。
- 写法: "However, [具体问题] remains unresolved." 或 "To date, no study has [具体做了什么]."
- **这是 Introduction 最重要的句子。Discussion 必须回应这个 gap。**
- 误写: gap 只暗示不说（"despite these advances, challenges remain"——什么 challenges?）。
- 误写: gap 太弱（"there is still room for improvement"——等于没说）。

### Layer 5: Present study（本研究）

- job: 我们做了什么、发现了什么、如何填 gap。
- 写法: "Here, we [做了什么]. We found that [主发现]. This [如何填 gap]."
- 不要在此总结 Results 细节；不要预览 Methods。
- 可选: 最后一句简要预告论文结构（仅在期刊惯例要求时——Nature 不要求，专刊有时要求）。

## 段落 drafting 规则

1. **一段一个 message。** 不要在一段里塞 field stake + bottleneck + gap。各层分家。
2. **第一句定调。** 段首句是该段的 claim，后续句支撑它。
3. **一个具体数字锚定可信度。** "500 W cm⁻²"——读者看到这个数字，默认你懂这个领域。没有数字的大背景 = 空洞。数字的来源必须可追溯到 Layer 1-3 的引文。
4. **Gap 写断层，不写空白。** "no one has studied X" → 像你文献没搜够。"the data exists here, the decisions happen there, and nothing connects them" → 你把整条链读通了，知道卡在哪。空白型 gap 会被审稿人用一篇你没搜到的文献怼回来；断层型 gap 说明你不是漏了文献，而是看穿了结构性的 mismatch。
5. **不要"桥段"。** "In this paper, we first..., then we..." 这种论文路线图放在最后一段，且仅当必需时。

## Introduction-Discussion 锁链

写完 Introduction 后必须对回 Discussion，检查：

- Intro gap 说的"X 未解决" → Discussion 是否解释了"我们用 Y 解决了 X"？
- Intro 提到的竞争假说/现有方法局限 → Discussion 是否回应了我们的方法如何不同于/优于它们？
- Intro 提了但 Discussion 没回应的 → 要么补 Discussion，要么删 Intro 的对应句。

见 `writing-discipline.md` 的一致性铁律。

## 常见失败模式

| 失败 | 为什么错 | 修法 |
|---|---|---|
| Opening 是教科书综述 | 审稿人不用你告诉领域基础知识 | 换成 "X is a central challenge because [具体证据]" |
| Gap 没说清楚 | 读者不知道你到底解决了什么 | 把 gap 提炼成一句可验证的句子 |
| 前人工作被贬低 | 扁平化前人 = 制造假 novelty | 用 "Although... showed..." 公平对待 |
| 本研究那段复述了 Results 细节 | Introduction 是预告，不是摘要 | 只写"我们发现了 X"，不写具体数字/p 值 |
| Gap 和 Discussion 对不上 | Introduction 说 A，Discussion 说 B | 回 consistency check，先对齐再落盘 |
| 列了太多前人工作 | Introduction 不是 lit review | 只引和 gap 直接相关的；其余的进 Discussion |

## 从 writing drafts 搬素材

- `paper-plan.md` → 图清单 = 贡献清单的骨架
- `results.md` → 主发现（写 Layer 5 时参考，但不要复述细节）
- `method.md` → 数据/样本背景（写 Layer 5 时可以提一句样本规模）
- `conclusion.md` → 贡献声明（Layer 5 的锚）
- `figN-report.md` → Core conclusion（主 claim 参考）
- `figN-reading.md` → 修正版 claim（以修正版为准）

## 实例：一段五层漏斗

The rapid advancement of artificial intelligence technologies has exponentially increased the computational power demands of large language models (Li, Hao & Song 2025 Dynamic bin packing), driving a sharp rise in hardware power consumption (Chen, Wu, Chan et al. 2023 Survey on AI; Huang et al. 2024 A survey of). Modern AI accelerators, such as graphics processing units (GPUs) and tensor processing units (TPUs), now operate at heat flux densities exceeding 500 W cm⁻² (Ye et al. 2025 Silicon-based package level), pushing thermal management to the forefront of electronic system design. In such high-power-density environments, the total thermal resistance along the heat dissipation pathway has become the critical bottleneck limiting efficient heat transfer from the microprocessor core to external cooling systems (Lee, Henderson, Reip et al. 2022 Flow boiling characteristics; Yang, Deng, Li et al. 2024 Thermal-flow-force-electrical coupling). Heat flux must traverse multiple heterogeneous material interfaces, where the thermal contact resistance (TCR), defined as the temperature drop across the interface between two contacting solids, often substantially exceeds the bulk material thermal resistance under high heat flux conditions (Xing, Xu, Song et al. 2022 Recent advances in; Wei et al. 2024 Thermal interface materials). TCR is governed by the coupled physics of microscale asperity deformation on rough surfaces, mesoscale contact area distribution, and macroscale heat flux conduction. This multi-scale nature places TCR squarely at the intersection of contact mechanics and interfacial heat transfer (Pastewka, Vakis, Aghababaei et al. 2025 Modeling in tribology; Sun et al. 2024 A review of). Excessive TCR leads to localized hotspot temperature spikes (Krishnan & Jain 2023 Transient temperature distribution), accelerating electromigration in semiconductor devices (Haghbayan, Miele, Mutlu et al. 2023 Run-time resource management) and causing timing errors and thermo-mechanical fatigue (Yu et al. 2024 The application of), which directly degrade the computational performance and reliability of CPUs and GPUs. Precise prediction and management of TCR is therefore not merely a thermal engineering problem but a task that demands simultaneous reasoning over material chemistry, surface morphology, and multi-physics operating conditions. Yet, in current design practice, the wealth of experimental and simulation data generated across these dimensions remains largely disconnected from actionable design guidance (Meng et al. 2022 A review of; Wei et al. 2024 Thermal interface materials). Transforming multi-source interfacial data into structured, reusable engineering insights has therefore emerged as a central challenge for intelligent thermal management.

拆解：

- **Layer 1 — 大背景:** "rapid advancement of AI... driving sharp rise in hardware power consumption" → 3 篇引文从算力需求 / 功耗上升 / 硬件现状三个角度合力支撑一个 claim。一个具体数字 (`500 W cm⁻²`) 锚定整段可信度。
- **Layer 2 — 小背景+现状:** "total thermal resistance has become the critical bottleneck → TCR governed by coupled physics" → 从 500 W/cm² 逐级收窄到 TCR 这个概念。每步都有引文。
- **Layer 3 — Prior work:** 整段 10+ 篇引文穿插在叙事中，每个 claim 都有出处——hotspot 有 Krishnan & Jain、electromigration 有 Haghbayan、fatigue 有 Yu。
- **Layer 4 — Gap (断层型):** "the wealth of data... remains largely disconnected from actionable design guidance" — 不是"没人研究过 TCR"，是"数据有了但没人把它变成可用的工程指导"。这是结构性的 mismatch，不是文献空白。审稿人无法用"你漏了这篇"怼回来。
- **Layer 5 — Present study:** 最后一句是天然跳板——"Transforming... has emerged as a central challenge" → 下一句自然是"我们做了 X"。
