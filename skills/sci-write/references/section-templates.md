# Section templates — 数据驱动四件套结构

本 skill 写 Method / Results / Conclusion 三章。Introduction / Discussion / Abstract / Keyword 不在本 skill 范围内，由叙事写作阶段处理。

每个模板给"骨架 + 每段的 job + 素材来源"。素材来源指向本 skill 已落盘的文件（data-profile.json / figN-report.md / figN-reading.md），不指向任何外部 skill。

---

## Method

**目的**：让读者相信 claim 的方法基础。不是堆砌步骤——每段回答"为什么读者需要知道这个才能信任 claim？"

**两种写法：**

| | 非方法学论文 | 方法学论文 |
|---|---|---|
| Method 角色 | 支撑 claim——方法不是贡献本身 | Method 是 claim 的一部分——"我们发明了一个新方法" |
| 写作篇幅 | 精简——别人能复现即可 | 详尽——每步解释为什么这样设计、为什么比已有方案好 |
| 三段式 | 每段轻触：做什么 + 为什么这样做 + 怎么连接到 claim | 每段深入：motivation + design + advantage |

**统一三段式（每个子段落的骨架）：**

1. **Motivation** — 为什么需要这个环节？对 claim 有什么贡献？
2. **Mechanism** — 具体做了什么。够别人复现。
3. **Role in claim** — 这个环节的结果怎么支撑 claim？指向哪张图？

如果一段列不出 Role in claim → 这段不该在这。Method 不是操作手册，是 claim 的证据链的上游。

**素材来源——从文件提取，不编造：**

| 需要的内容 | 从哪来 | 怎么用 |
|---|---|---|
| 样本/数据描述 (N, per-group n, 变量, 缺失) | `data-profile.json` | Mechanism 段的开头——别人要知道你的数据长什么样 |
| 统计方法 (test, correction, error bar, n) | 各 `figN-report.md` → `Statistical methods` | Mechanism 段——**逐字搬运**，不改数字、不四舍五入、不改测试名称 |
| 图表方法 (为什么选此图) | 各 `figN-report.md` → `Chart type & rationale` | 非方法学论文可省略；方法学论文放 Role in claim 段 |
| Claim 上下文 | `claim.md` | Motivation 段的指引——"这个方法环节支撑了 claim 的哪个部分？" |

**动词**：过去时、被动或 we。不用 show/demonstrate（那是 Results）。

**不写**：不该出现在 Method 里的东西——不引非方法文献论证"标准做法"（要引走 Real-DOI 占位符）、不分析结果好坏（那是 Results 的活）、不解释发现（那是 Discussion 的活）。"under standard conditions""using routine methods""data were analyzed statistically"——全换掉，写具体。

---

## Results

**目的**：一块一块地构建 claim 的证据。每段 = 一张图的结论 + 这个结论在 claim 里的角色。

**写之前先做 claim→figure 映射**（不是每篇论文都需要全部 rung——只列你有的）：

```
claim.md: In [system], we show [advance] using [approach], supported by [evidence].

figX: [这个图证明了什么 conclusion] → 支撑 claim 的哪一步？
```

列不出第二列的图 → 不进 Results。

**每段模板**：

```
[Topic sentence: 本段 conclusion，过去时]
我们观察到 [具体数据/现象，引用 figN + 统计量]。
[对照/细节——跟什么比、在什么条件下]。
This [supports/demonstrates/establishes] [claim 的哪一环节]。
Fig N, [panel].
```

**关键区别**：Topic sentence 不是"we observed X"——那是细述句。Topic sentence 是"X was Y"——图的结论本身。

**素材**：
- conclusion ← `figN-report.md` 的 `Core conclusion`（以 `figN-reading.md` 的修正版为准）
- 具体观察 ← `figN-report.md` 的 `Key findings`
- 统计量 ← `figN-report.md` 的 `Statistical methods`

**动词校准**: 主结果用 show/demonstrate；趋势级用 suggest/indicate。may/could 不进 Results——那是 Discussion 的动词。

**Results 不做**: 不解释为什么（Discussion）；不引文献对比（Discussion）；不混解释语法。

## Conclusion

**目的**：从 findings 收口。短。不引入新内容。

**结构（一段）：**

1. **贡献声明**: 我们做出了什么。（主 claim，从 paper-plan + Results 提炼）
2. **证据一句话**: 由 [figN 的关键 evidence] 支撑。
3. **局限一句话**: 边界在哪。

**动词**: 主贡献用 show/demonstrate。

**Conclusion 不做**: 不复述 Results 细节；不引入新机制；不出现新引用。

---

## 章节间一致性（写完本 skill 的三章后扫一遍）

- **claim 一致**: Results 的 claim 和 Conclusion 的贡献声明不矛盾。figN-reading.md 的修正版贯穿。
- **术语一致**: 同一变量/方法在三章里用同一个词。建一个术语小账，首次出现锁定，后续复用。
- **统计一致**: 所有章节引到的统计量（n、test、误差类型）和 `figN-report.md` 的 `Statistical methods` 完全一致——逐字校对。
- **figure 引用一致**: Results 引 "Fig 1"，编号一致，不串。
