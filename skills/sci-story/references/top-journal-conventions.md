# Top-Journal Conventions — 顶刊实证写作模式

以下提炼自 2025 年 Nature Communications 20 篇 CS/AI 公开文章的实证阅读。不是"应该这样写"——是"顶刊实际这样写了"。投什么期刊无所谓——这些模式是所有好论文的公因数。

## Introduction

### Hook 三种形式

1. **重要性宣告**："The biological brain is remarkable in its ability to..."
2. **定义定调**："Protein engineering is an optimization problem, where..."
3. **领域后障碍**（benchmark 默认）：先说广泛使用 → "Despite its promises, progress is impeded due to the absence of benchmarks."

### Gap 信号词

`However / remains / Unfortunately / underexplored / the scarcity of ... hinder / Without X, Y cannot be ...`

**高级写法：用数字量化稀缺。** "merely 124 (3.0%) have structures in the PDB"——不是"few structures exist"。

### 贡献句

`Here we...` / `In this work, we...`，通常跟 `(Fig. 1)`。多项贡献用 `First... Second... Finally...`。

**关键：让选题理由显式化。** "We chose this model system because..." — 为什么是这个问题、为什么选这个体系。不是默认它是重要的——证明它是重要的。

## Abstract

五步、一段、4-11 句：

1. 为什么重要（现在时）
2. Gap — 几乎永远以 **However** 开头
3. `Here we show/present/introduce X (全名, 缩写), a ... that ...`
4. 一个硬核定量结果（倍数/%/准确率），过去时
5. Significance + 可选链接

不讲过程、不堆数字、最后不吹概念。

## Results

- **小标题是结论句**："CodonTransformer generates DNA sequences with natural-like distributions"——不是 "Experiment 1" 或 "Dataset"。
- **段首先写判断，再写证据**："Interestingly, wt-McbA displayed a tolerance to..." → 然后才是图和数据。
- **数字是 absolute + relative + direction**："from 323.4 to 297.3, an improvement of 8.8%"——不是 "improved performance"。
- **段间推进**：`With [上段结论], we next...` / `To <目的>, we <做了> (Fig. X).`

## 过渡词频率

基于 5 篇文章统计：

```
However     51  ← 转折、开 gap、出意外的主力
Furthermore 22  ← 推进论述（比 Moreover 常用 5.5x）
Therefore   19  ← 因果推理
Notably     16  ← 标记关键发现
In contrast  6
Moreover     4
```

**Notably / Importantly / Interestingly / Surprisingly** 用来标记关键发现，不是每段一个。Overall / In summary 收束一个板块。

## 句法与时态

- 背景/属性 → 现在时
- 做了什么 → 过去时
- 当前含义/图描述 → 现在时
- 叙事和 claim → 主动 `we`
- 方法/设备 → 被动
- **Hedge（may / suggest / likely）只在意义句中用**，不在结果句中用
- **不要用 "significantly"。** Nat Comms 2025 语料中 0 次出现。用 notably / substantially / considerably。

## 体裁差异速查

| | Research | Review | Perspective | Comment |
|---|---|---|---|---|
| 数据 | 自己的图+数字 | 别人文献的综合 | 论证，无实验 | 无 |
| 人称 | `we` + 被动 | `we` + survey | `we/our` | 第一人称 `I` |
| 收口 | Discussion + limits | Conclusions + governance | roadmap | call to action |

sci-story 目前只覆盖 Research。

## Title

**Title 是 claim 的最短版本。** Abstract 压缩了论文；标题压缩了 claim。写标题之前读 `claim.md`——标题的一句子论证必须和它一致，不能漂移。

**四种形状，按 claim 的类型选：**

1. **名词短语、方法主导**（最常见）：claim 是方法 → *AlphaFold prediction of structural ensembles of disordered proteins*
2. **陈述句、卖点是发现**：claim 是发现 → *Dendrites endow artificial neural networks with accurate, robust and parameter-efficient learning*
3. **`System name: function` 冒号式**：claim 是工具 → *CodonTransformer: a multispecies codon optimizer...*
4. **Gerund/question**（benchmark/Perspective 专用）：claim 是标准/比较 → *Benchmarking large language models for...*

**硬规则：**

- 标题不放数字或结果——把数字留给 Abstract。
- 一个限定性形容词预载 claim：*robust*, *generalizable*, *data-driven*。不要 *novel*, *advanced*, *powerful*, *green*, *efficient*——空洞。
- 介词短语链承载"什么 + 怎么 + 在哪"：*...discovery and engineering **with** deep learning **using** CataPro*。
- 能检索——放领域术语。同一个研究员搜关键词能找到这篇论文吗？
- 不只是口号——标题的 claim 数据撑得住才放。
- Grant 式（*Toward …*, *A study of …*）、过度广泛（*A new era of …*）、问句（除非论文真的回答了这个问题）——全砍。

**写完自检：** 标题 ↔ claim.md——同一个 argument？标题 ↔ Abstract——标题比 Abstract 更保守（好）还是更夸张（坏）？不一致 → 改标题，不要改 claim 和 Abstract。标题比 Abstract 更保守是对的——Abstract 具体，标题精准。
