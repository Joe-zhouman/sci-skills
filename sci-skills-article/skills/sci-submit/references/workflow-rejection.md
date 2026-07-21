# Workflow D: Rejection & Switching

## 触发条件

被拒。任何一种。

## 先冷静

被拒不等于你的工作不行。期刊的 desk reject 率可以到 50-70%，Nature 系可能更高——编辑手里过一遍，大多数稿子连送审的机会都没有。这不代表你的文章没价值，只代表它没打动这一个编辑。

以下针对三种被拒类型，各自有一条路径。

---

## 类型 1：Desk Reject — 编辑没送审

**含义**：编辑觉得不适合，没送外审。

**最容易犯的错**：急了，什么都不改，立刻投下一个期刊。这最浪费时间。

**应该做的事**：

### 1.1 判断原因

看编辑信里有没有线索。大部分 desk reject 分两类：

- **scope 不匹配**："your manuscript does not fall within the scope of our journal" → 你真的投错了。回到 shortlist 找 scope 匹配度更高的。
- **水平/新颖度不够**："we only publish papers that represent a significant advance" → 要么你的封面信没论证好"为什么这是重大进展"，要么这个期刊定位确实高于你工作的水平。

如果编辑给了具体理由（"we would suggest submitting to a more specialized journal"），记下来——这比你自己猜准确。

### 1.2 回到 shortlist

读取 `journal-shortlist.md`。desk reject 之后不要调高目标期刊的档次（"既然 Nature 拒了那试试 Science"）——那是赌气。往匹配度高的方向走：scope 匹配 > 水平匹配 > 速度。

### 1.3 改封面信，不改手稿

Desk reject 没给审稿意见，所以手稿本身不需要改。但封面信要改——编辑没被打动，说明你的论证方式在这个期刊没奏效。下一封封面信的背景钩子和期刊契合度段重新写。

### 1.4 记录

更新 `submit-history.md` 和 `journal-shortlist.md`。

---

## 类型 2：Reject After Review — 送审了，被拒

**含义**：编辑送了外审，审稿人给了意见，编辑综合判断后拒了。

**这是最有价值的被拒。** 你拿到了同行评审意见——免费的、专业的、针对你工作的反馈。哪怕语气不好，内容一般都有用。

### 2.1 挖掘审稿意见

读完所有审稿意见，分三堆：

| 堆 | 内容 | 动作 |
|---|---|---|
| **可以引用的正面评价** | "interesting approach""novel dataset""well-written" | 摘出来，下次封面信可以用。编辑看到"这篇在 XX 期刊送审过并获得正面评价"是有分量的。 |
| **能改的问题** | 缺实验、分析不够、文献不全 | 改了再投。不改进投下一个期刊，审稿人可能还是同一批人，看到没改会直接拒。 |
| **改不了的问题** | "样本量太小"（但你的体系就这么大）、"跟 XX 的工作比创新不够"（但 XX 那个方向跟你不完全一样） | 下次封面信要提前回应。在期刊契合度段之前加一句——"We acknowledge that [concern]; however, [your counter-argument]"——让编辑看到你已经考虑过了。 |

### 2.2 正面评价怎么用

下一封封面信里，期刊契合度段之后加一个小段：

> "We note that this manuscript received favorable reviews at [Previous Journal] (reviewer comments available upon request), where reviewers highlighted [1-2 specific positive quotes]. We have since [improvement made based on review]."

不需要每次都加这一句——但如果审稿人确实给出了正面评价，这是有力的信号。

### 2.3 改还是不改？

- **同档次换刊** → 先改能改的再投
- **降档投** → 可以少改，但至少修复明确指出的错误
- **急着赶 deadline** → 至少写一个 Response-to-Previous-Reviews 的文档（哪怕新期刊不会看到），这样你自己清楚改了什么、没改什么

### 2.4 记录

更新 `submit-history.md`。把审稿意见的要点记进去——三个月后你不会记得 Reviewer 2 说了什么。

---

## 类型 3：Reject-and-Transfer — 编辑建议转投

**含义**：编辑拒了，但建议你把稿子转到同一个出版社旗下的另一本期刊。

**多数情况下值得考虑。** 编辑不会随便建议 transfer——这说明他们觉得你的工作在这个出版社的生态里是有价值的，只是投的那本不对。

### 3.1 判断是否接受

- **transfer 目标的期刊在 hard-constraints 白名单里吗？** 如果不在，而且硬约束要求"只能投白名单"，那就得跟用户确认。
- **transfer 目标在 shortlist 里吗？** 如果已经评估过且被列为 Tier 2/3，可以直接接受。
- **不懂这个期刊** → 用 `scripts/query-journal.py` 查一下，快速评估。

### 3.2 接受 transfer

大多数投稿系统的 transfer 会保留部分投稿信息——省时间。封面信加一句："This manuscript was previously submitted to [Original Journal] (MS# XXX), and the editor recommended transfer to [New Journal]."

### 3.3 不接受

如果 transfer 目标不满足硬约束，拒绝 transfer，回到 Workflow B 重新选刊。

---

## 三种类型之后的共同步骤

1. **更新 `submit-history.md`**：日期、期刊、Manuscript ID（如有）、决定类型、编辑/审稿人反馈要点
2. **更新 `journal-shortlist.md`**：标记被拒的期刊，如果是从 shortlist 里挑的，移到 Ruled Out
3. **如果有审稿意见**：存到 `sci-skills/sci-submit/` 下，文件名 `<journal-name>-reviews-YYYY-MM-DD.md`
4. **选下一个目标**：从 shortlist 挑，或者如果 shortlist 空了 → Workflow B
5. **走 Workflow C** 写新封面信
