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

**目的**：报告观察。每段一个 claim，claim 必挂 evidence（图/统计）。

**结构（evidence ladder，由弱到强排列段落）**：

1. **系统/工作流验证**（若有）— 证明你的系统/流程跑通了。
2. **主结果** — 论文的头条发现。最重要的图放这。
3. **基线对照** — 和已有方法/对照比。
4. **消融/机制** — 拆解为什么 work、哪个组件关键。
5. **泛化/应用**（若有）— 换数据集/场景还成立吗。
6. **压力测试/失败模式** — 边界在哪、什么时候不 work。

不是所有论文都有全部 6 级。按图的实际 evidence 角色排。

**每段模板**：
```
[Topic sentence: 本段 claim，过去时]
我们观察到 [具体数据/现象，引用 figN + 统计量]，[对比/趋势]。
[第二句：进一步细节或对照]。
[Evidence 句：图/统计指向]。Fig N, [panel].
```

**素材**:
- claim ← `figN-report.md` 的 `Core conclusion`（以 `figN-reading.md` 的修正版为准）
- 具体观察 ← `figN-report.md` 的 `Key findings`
- 统计量 ← `figN-report.md` 的 `Statistical methods`

**动词校准**: 主结果用 show/demonstrate；趋势级用 suggest/indicate。机制推测和文献对比不在此（那是 Discussion 的事）。

**Results 不做**: 不解释为什么；不引文献对比；不混 `may reflect` 这类解释语法。Report observations, don't interpret them.

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
