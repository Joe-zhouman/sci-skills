# Abstract Guide — 微型论文，最后写

Abstract 是一篇论文的微型版：context → gap → approach → key results → implication。它帮助读者决定这篇论文是否相关、可信、可能重要。

**铁律：Abstract 最后写。** 当 Results 和 Discussion 都稳定之后再写。论证还没稳定就写 Abstract = 写出来必定和正文不一致。

## 微型论文结构

一个段落，内部保持以下 order：

1. **Context / Problem** — 1 句: 为什么这个领域重要？（最宽）
2. **Gap / Bottleneck** — 1 句: 现有方法的不足 / 未解决的问题
3. **Approach** — 1 句: 我们做了什么（方法/策略）
4. **Key results** — 1-2 句: 我们发现什么？（Abstract 里唯一允许的定量信息）
5. **Implication** — 1 句: 这意味着什么？（收回到大图景）

收口顺序: context (宽) → gap → approach → results (窄) → implication (宽)

## 模板变体

### 变体 A: Challenge → Contribution（最常见）

> [Field] is [importance]. However, [bottleneck] remains unresolved. Here, we [approach/tool]. We show that [key result]. Our findings demonstrate [contribution/insight], suggesting [implication].

适用于: 提出了新方法/新工具解决了明确瓶颈的论文。

### 变体 B: Challenge → Insight → Contribution

> [Field] faces the challenge of [gap]. We hypothesized that [insight/hunch]. To test this, we [approach]. We found that [key result], revealing [mechanism/insight]. This provides a [framework/principle] for [implication].

适用于: 发现了一个新的机制/原理/pattern 的论文。

### 变体 C: Multiple contributions

> [Field] is limited by [bottleneck 1] and [bottleneck 2]. Here, we address both by [approach]. First, we show [result 1]. Second, we demonstrate [result 2]. Together, these findings establish [unifying contribution], providing [implication].

适用于: 一个方法同时解决了多个问题的论文。

Variant 选择由论文的论证结构决定——不是你想用哪个，是论文最适合哪个。看不准时用变体 A。

## Abstract 的 drafting 纪律

1. **不引入正文里不存在的内容。** Abstract 里的每个 claim 必须已在 Introduction / Results / Discussion 中出现。Abstract 里出现了一个正文没有的数字/发现/引用 → 必须删。
2. **不过度压缩到失去信息。** "We report new methods for X" 不等于 "We developed a [具体方法] that achieves [具体性能] on [具体任务]"。后者对读者才有信息量。
3. **最后一句要有意义。** 不要以 "These results have important implications" 收尾——implication 到底是什么？
4. **字数/字符在期刊限制内。** Nature 摘要 ~150 词；Nat Comms 摘要 ≤150 词；一般期刊 200-300 词。写之前问期刊的限制。
5. **不列文献在 Abstract 里。** 极少例外（罕见，一般 Abstract 不引文献）。

## 从邻居搬素材

- `intro.md` → gap statement + contribution 语言（Abstract 的 context 和 gap 从这里压缩）
- `results.md` → 主发现的具体内容（Abstract 唯一许可的定量信息来源）
- `discussion.md` → implication 语言（Abstract 的最后一句从这里提炼）
- `conclusion.md` → 二次压缩参考（Conclusion 本身已经压缩了一次 findings）

## 常见失败模式

| 失败 | 为什么错 | 修法 |
|---|---|---|
| Background 太长 | 摘要的 1/3 花在说领域背景——gap 和结果被挤没了 | 砍到 1 句——title 已经说了领域 |
| 只有定性没有定量 | "improved performance" — 多少？ | 加关键数字（"提升了 23%"、"精度达 0.92"） |
| 最后一句是空话 | "implications are discussed" 或者 "has broad applications" | 具体的 implication 是什么、对谁 |
| 写了正文里没有的引用 | Abstract 里出现了新文献 | 砍掉——Abstract 不引新文献 |
| 和 Introduction 第一段重复 | 两段文字几乎一样 | Abstract 更浓缩 |
| 写了 Discussion 还没稳定的结论 | Abstract 写完后 Discussion 改了，Abstract 没跟着改 | 铁律：Abstract 最后写 |
