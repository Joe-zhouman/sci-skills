# Discussion Guide — 解释发现 + 定位贡献 + 锚定 Introduction 的 gap

Discussion 的目的：解释 Results 意味着什么、把发现放回 field 里、说清楚贡献的边界。
Discussion 是 Introduction 中 gap 的答案——Introduction 问"这里有个缺口"，Discussion 答"我们填了，这意味着 X"。

统一写法：**第一段为 Conclusion，后面写 Discussion。** 这是几乎所有期刊的公因数。

## 结构

### 段落 0: Conclusion（从 sci-write 融合，一字不改）

sci-write 已经写了 `conclusion.md`——贡献声明 + 决定性证据 + 边界。Discussion 的第一段原封不动搬过来，不重写、不展开、不改成解释语气。这是几乎所有期刊的公因数。

### 段落 2: Opening — 主发现的解释（不复述 Results）

- job: 回答"主发现意味着什么"，不是复述"我们观察到什么"。
- 写法: "Our results show that [contribution statement]. This [suggests/indicates/demonstrates] [meaning or mechanism]."
- 素材: `results.md` 的主 claim + `figN-report.md` 的 Core conclusion（以 `figN-reading.md` 的修正版为准）。
- 误写: 开头就是 "We observed that X increased by Y% (Fig 1)." —— 那是 Results 的开头，不是 Discussion 的。
- 正确: "Our study provides evidence that [mechanism/insight]. Specifically, the [具体发现] suggests [解释]."

### 段落 3-4: Mechanism（核心机制段）

- job: 为什么会观察到这个？给出合理的机制解释。同时考虑 rival explanations。
- 动词: may / could / might / is consistent with / could be explained by
- 必须做的事: 提到对立的/rival 解释并说明为什么你的解释更可能（或至少被数据支持）。
- 注意: 机制是推测——必须配边界声明（"This interpretation is plausible but has not been directly tested"）。
- 误写: 只给一个解释，不提 rival（审稿人一定会提）。
- 误写: 用 show/demonstrate 来形容未被直接验证的机制。

### 段落 5: Literature comparison（文献对比）

- job: 和已有工作比——一致（aligns with）、延伸（extends）、还是冲突（contrasts with）。
- 引文纪律: 见 `references/literature-search.md` — 优先学术搜索 MCP，退到通用搜索。真实 DOI 占位符，不空占位、不编文献。
- 写法: "Our finding aligns with [Author, DOI:...] who reported [specific result]. We extend this by [specific extension]."
- 冲突: "In contrast to [Author, DOI:...] who found [X], our results show [Y]. This discrepancy may arise from [reason]."
- 不要做的事: 拉一个 "X also found Y, Z also found Y" 的长清单——那不是讨论，那是列举。只比关键、正面对话。

### 段落 6: Limitations（局限）

- job: 你的证据边界在哪。诚实。审稿人会挑的，你自己先说。
- 写法: 每个 limitation 给方向（可能往哪个方向偏）、给补救（未来怎么做可解决）。
- 必含内容:
  - 样本/数据的局限（N 不够、数据来源单一、群体不代表性）
  - 方法/设计的局限（未被控制的变量、可能的混淆）
  - 泛化的边界（"In settings where [条件] does not hold..."）
- 误写: "This study has limitations" 然后不列具体是什么——等于没写。必须是具体可操作的局限。

### 段落 7: Implications / Outlook（影响/展望，可选）

- job: 这意味着什么、下一步。
- 写法: bounded claim。不要画大饼。
- 正确: "Our finding that [X] suggests a path toward [Y application]. Testing [Z hypothesis] in [setting] would be a natural next step."
- 误写: "This work opens new avenues for..." 然后不具体说是什么 avenues。

## Discussion 的语法纪律

- **用解释动词**: may reflect / suggests / indicates / is consistent with / could be explained by / is likely due to
- **不用观察动词**: was detected / increased / showed / achieved —— 那是 Results。
- **时态**: 解释用现在时 ("suggests", "indicates")，回顾具体发现时用过去时 ("we found that...")。
- **段间切换明确**: 从解释段切到局限段、从展望段切到未来的段落时，要有明确的话题转换信号。

## Introduction-Discussion 一致性检查（写完后必跑）

写完 Discussion 全文后，和 Introduction 对一遍：

| Introduction 中的 gap/bottleneck | Discussion 中的回应 | 一致？ |
|---|---|---|
| [Intro 第 N 段: X 未解决] | [Discuss 第 M 段: 我们提供 Y] | yes / no |
| [Intro 提到竞争假说 A] | [Discuss 回应了 A 的不足] | yes / no |
| [Intro 声明贡献 Z] | [Discuss 解释了 Z 的意义] | yes / no |

不一致 → 先修，再继续。这是 sci-story 最核心的质量门槛——不一致的 Introduction 和 Discussion 比没有更糟。

## 常见失败模式

| 失败 | 为什么错 | 修法 |
|---|---|---|
| 开头复述 Results | Discussion 是解释，不是总结 | 砍掉观察性复述，换成"这意味着..." |
| 只给一种解释不提 rival | 审稿人一定提 rival——你先提是 good faith | 加一个 rival explanation + 为什么你的解释更可能 |
| "X also found Y" 清单 | 那不是讨论，是文献堆 | 只比关键：一致→延伸了什么？冲突→为什么？ |
| 局限是空话 | "this study has limitations" 等于没写 | 每个局限给方向+补救 |
| 展望画大饼 | "opens new avenues" 不具体 | 给下一步的具体方向 |
| Intro 的 gap 和 Discussion 的结论对不上 | Introduction 说 A，Discussion 说 B = 论文撕裂 | 回一致性检查，重对齐 |

## 从 writing drafts 搬素材

- `results.md` → 主发现（作为 Discussion 的解释起点）
- `conclusion.md` → 贡献声明 + 局限 + 影响（Discussion 的骨架）
- `figN-report.md` → Core conclusion + Key findings（引证据参考）
- `figN-reading.md` → 修正版 claim（以修正版为准；若发现了误读风险，Discussion 要加对应限定）

Discussion 不能从零写——它解释的"什么"必须已经存在于 Results。如果 Discussion 想要讨论一个 Results 里没有的发现 → 要么补 Results，要么砍 Discussion 的这段解释。
