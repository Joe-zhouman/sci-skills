# Restructure discipline — IMRaD→模块化章 写时重构纪律

本 skill 在写章的每个动作前打开本文件。它指导**写时**的 IMRaD→模块化章重构——dissect-by-writing，拆即写——**不是 pre-write outline**。重构活在写的 `thesis/tex/chN.tex` 里，不在单独的 module-map 文件。

一句话：**章 = 章引（提问题）→ 模块链（干什么→怎么做→做了什么）→ 本章讨论（精髓落点）→ 本章小结（收束+递进）**。小论文的 intro、discussion、SI 没有一块是可丢的——丢任何一块，章就退化成实验报告：引言的职责是提问题，discussion 是每篇论文的精髓，SI 只是因为小论文正文篇幅限制才被挤出去（学位论文没有这个限制）。

---

## Table of Contents

- The chapter shape（章形）
- 素材去向总表
- 模块：三拍 + 切片按问题
- 章引怎么写
- 本章讨论怎么写（独立节）
- 本章小结怎么写
- SI 并入规则
- How to restructure IN-WRITE (dissect-by-writing)
- 动词与语态
- Contract-gap handling
- What this reference is NOT
- 跨模块一致性（写完一章后扫一遍）

---

## The chapter shape（章形）

**目的**：把小论文的 IMRaD 序列重构成学位论文章的完整形态。小论文 IMRaD 是"intro→method→results→discussion 各成一段、独立成篇"的叙事；学位论文章不是 IMRaD 的复写，也不是只剩 method-results 对的裸模块链——章有自己的提问题（章引）、自己的综合（本章讨论）、自己的收束（本章小结）。

```latex
\chapter{…}
% 章引：\chapter 之后的无标题引文段（template-spec 对章内结构另有约定则从之）
%   提本章问题 ← 论文 intro 的提问题素材 + spine role question + progression-in
\section{模块 1 标题——干什么的名词化，非 IMRaD 词}
  干什么（提出本模块问题）→ 怎么做（method）→ 做了什么（results，回答暗含在呈现里）
\section{模块 2 …}
  …
\section{本章讨论}   % 独立节——不按模块切块（见"本章讨论怎么写"）
\section{本章小结}   % 短，一段：回答章引问题 + 抛出下一章问题
```

| | 小论文 IMRaD | 学位论文章 |
|---|---|---|
| 组织 | 顺序四段：intro→method→results→discussion | 章引→模块链（method 紧跟对应 results）→本章讨论→本章小结 |
| 单元 | section（method 一整块、results 一整块） | module（question→method→results 三元，原子单元） |
| 提问题 | intro 集中铺陈 | 章引提章问题；每模块开头提模块问题 |
| 解释 | discussion 统一解释 | 本章讨论独立成节（跨模块综合 + 机制 + 文献对比） |
| 收束 | 无（讨论即结尾） | 本章小结：回答章引问题 + 递进到下一章 |
| SI | 因正文篇幅限制挤到 SI | **并入正文**（默认并入，弃用须记理由） |

**模块链**：results → next question → next method → next results → …；一个章 = 章引 + 一串模块 + 讨论 + 小结。章引的问题由模块链回答，本章小结收束这个回答。

---

## 素材去向总表

**目的**：小论文每一块素材都有明确落点——没有任何一块默认丢弃。深读时把每条素材登记进 `paper-X/trace.md`（SI 清单 + 讨论素材清单，见 SKILL.md Step 1.2），写作时逐条落位。

| 小论文素材 | 去向 |
|---|---|
| intro 的提问题部分（问题背景 + 为什么值得答） | **章引** |
| intro 的 thesis 级研究现状综述 | **不搬**——那是 thesis-intro（绪论）的地盘，搬了章引变 mini-绪论 |
| method 对应片段（参数、样本、统计量） | 所答 question 的模块"**怎么做**"——**逐字**，不改数字、不四舍五入、不改测试名称 |
| results + figure/stat 对应片段 | 所答 question 的模块"**做了什么**" |
| discussion：单点机制解释、文献对比 | **本章讨论**（独立节，不塞进模块） |
| discussion：跨模块综合、意义、局限 | **本章讨论** |
| SI：表征数据、对照实验、额外结果 | 对应模块"怎么做/做了什么" |
| SI：支撑章问题的背景 | 章引 |
| SI：支撑解释的内容 | 本章讨论 |
| SI：与本章问题真无关的条目 | 弃用——trace.md 记理由，作者 post-chapter gate 可推翻 |
| 术语 | `thesis-terminology-ledger.md`（canonical form，`source: thesis-dissect`） |

---

## 模块：三拍 + 切片按问题

**目的**：模块 = question→method→results 三元（原子单元）。合格的模块**先说干什么，再说怎么做，然后才是做了什么**——回答暗含在呈现里。

三拍纪律：

1. **干什么**（模块 tex 的第一句就是它）——本模块答什么问题，1-2 句。模块 1 的 question 由章引引发；模块 N 的 question 由上一模块的 results 引发（"既然观察到 X，那 Y 吗？"）。**写不出这一句 = 切片失败**——回论文重找本模块的问题，不要硬写。
2. **怎么做**——为答这个问题做了什么。够复现；统计量、参数、样本量**逐字搬运**自小论文。共用理论方法**引理论章**（thesis-theory 产物），不整段重抄。
3. **做了什么**——数据显示什么。引 figure/stat；**回答暗含在呈现里**——results 段落收尾时答案已经摆在数据中，不写"综上所述，本节回答了……"式的复述（那是把读者当外人；解释留给本章讨论）。

**切片按问题，不按论文章节**。这是合并真正发生的机制：

- 写模块前先答一句"本模块答什么问题"，然后**只问论文哪里有答它的料**——method 片段可能在 §2.3，results 在 §3.2，一张关键 SI 图是 S5，它们合成同一个模块。
- **论文的章节边界不是模块边界**。照着论文的 Methods/Results 章节顺序转录 = 没有重构（产出的是改了标题的 IMRaD——`check_dissect.py` 的 IMRaD 签名检查会拦）。
- 列不出 question 的模块不该在这：并入上一模块，或它是 contract-gap（见下）。

---

## 章引怎么写

**目的**：提问题——introduction 的核心职责在章这个尺度落地。没有章引，模块链不知道自己为什么在跑。

- **位置**：`\chapter` 之后的无标题引文段（template-spec 对章内结构另有约定则从之），2-4 段，写在模块 1 之前。
- **内容三件**：① 本章要答的问题（spine role question 的落地）；② 为什么这个问题值得答（上一章 results 留下的悬念 = chapter-map 的 progression-in；首章用主线引出）；③ 本章怎么答（一句话路线图：沿模块链预告，可选）。
- **素材**：小论文 intro 里提问题的部分（问题背景 + 为什么值得答），trace.md 章引素材行。
- **不写**：thesis 级研究现状综述（绪论的地盘）；与本章问题无关的领域背景。章引不是 mini-绪论——只铺到"本章问题立得住"为止。

## 本章讨论怎么写（独立节）

**目的**：discussion 是每篇论文的精髓——机制解释、文献对比、意义、局限必须存活。**独立成节，不按模块切块**：很多讨论是多模块的结果放在一起看才有的（跨模块的机理连贯性、与文献的总体对照），切不进任何单个模块。

- **位置**：最后一个模块之后、本章小结之前，`\section{本章讨论}`。
- **内容**：小论文 discussion 的全部素材——机制解释（为什么观察到这个结果）、文献对比（与已发表工作的一致/分歧，每条挂 Real-DOI placeholder）、跨模块综合（各模块结果拼起来的图景）、意义、局限（诚实地写方法边界）。
- **组织**：按问题组织（这个结果为什么如此 → 和文献对得上吗 → 各模块合起来说明什么），不按模块顺序逐条复述——复述是讨论最轻易的写法。
- **来源**：trace.md 讨论素材清单每一条的去向都是这里（或弃用+理由）。

## 本章小结怎么写

**目的**：收束——回答章引的问题，把接力棒递给下一章。

- **位置**：全章最后一节 `\section{本章小结}`，**一段，短**。
- **内容两件**：① 回答章引提出的问题（与章引首尾闭环——章引问了什么，这里就答什么）；② 抛出下一章的问题（= chapter-map 的 progression-out；末章则收束到主线）。
- **不写**：不引入新内容（新解释归本章讨论）；不复述各模块结论（那是论文合集式收尾）；不空喊意义。

---

## SI 并入规则

**目的**：小论文放 SI 是因为正文篇幅有要求、不宜过长；**学位论文没有这个限制**——SI 的绝大部分内容必须并入正文，而不是随转化被丢弃。

- **默认并入**。深读时把 SI 逐条登记进 trace.md 的 SI 清单（条目 + 性质 + 去向），写作时按素材去向总表落位：表征/对照→对应模块；支撑章问题→章引；支撑解释→本章讨论。
- **弃用是例外且须记理由**。某条 SI 与本章问题真无关（常见于：属于另一篇小论文章的内容、期刊格式性内容）→ 去向写"弃用 + 一句理由"，作者 post-chapter gate 可推翻。
- **不编造**。SI 里的 method 缺细节 → 走 contract-gap 流程（停，flag 作者），不脑补参数。
- **SI 图表进章**：并入的 SI 图表按章内图编号正常 `\begin{figure}\caption{...}\label{fig:...}`（编译自动统一编号，spec §图编号由 LaTeX 自动）。

---

## How to restructure IN-WRITE (dissect-by-writing)

**目的**：每章通过**写其 tex** 来拆它——拆和写是同一 act（拆即写），不是两步。

**章内写作顺序**（逻辑热的顺序）：

1. **打开本文件**（你已经在做了）。
2. **深读全篇**（SKILL.md Step 1.2，含 SI 与 discussion）→ trace.md 登记素材清单（去向先标 `pending`）。
3. **写章引** → 提出章问题（素材：论文 intro 提问题部分 + spine role question + progression-in）。
4. **逐模块：深读该模块的切片 → 直接写三拍**。切片按问题找料（method 片段 + results 片段 + SI 条目），写进 `thesis/tex/chN.tex`（tex-direct，无 md 中间；Real-DOI placeholder）。写完即回填 trace 对应条目的去向（`pending` → 实际落点）。
5. **post-module gate**（每模块 tex 写完后）：①三拍齐吗——干什么在第一句、怎么做够复现、做了什么引证据？②本模块该吸收的 SI 条目吸收了吗？不满意 → 改（逻辑还热）；满意 → 下一模块。
6. **写本章讨论**（独立节，素材=trace 讨论素材清单）→ **写本章小结**（一段，回答章引问题+递进）。
7. **章收尾 gate**：章引问的问题，小结答了吗？trace 清单去向清零了吗（无 `pending`、无裸条目）？

**关键纪律**：

- **重构 IS 写作**。IMRaD→章形重构在写的过程中发生——你边写边把 method 拉到 results 旁、把 discussion 素材聚拢成讨论节，不先画 module-map 再填。
- **逻辑热时写**。深读完切片后立即写——逻辑还在工作记忆里。两步（拆笔记→后写章）要重新载入一遍刚捋过的逻辑，浪费且易丢（glossary `_Avoid_: outline-then-fill`）。
- **无 pre-write outline**。不产 `module-map.md` 文件。重构结果活在 `thesis/tex/chN.tex` 里——你写的就是重构。
- **gate 在 act 之后**。post-module gate 审已写 tex 的重构，不在写前 gate 抽象骨架（写前 gate 必须先有 outline）。

**素材来源——从文件提取，不编造**：

| 需要的内容 | 从哪来 | 怎么用 |
|---|---|---|
| 章问题、章引素材 | spine role question + 论文 intro 提问题部分 | 章引：提问题，铺到"问题立得住"为止 |
| 模块 question | 上一模块 results（或章引） | 三元第一拍："既然 X，那 Y 吗？" |
| method（参数、样本、统计） | 小论文 method 对应片段 + SI 方法条目 | 三元第二拍——**逐字**，不改数字、不四舍五入、不改测试名称；共用方法引理论章 |
| results（figure/stat） | 小论文 results/figures 对应片段 + SI 结果条目 | 三元第三拍：写"数据显示 X" + 引 figN + 统计量；回答暗含呈现 |
| 本章讨论素材 | 小论文 discussion 全部 + trace 讨论素材清单 | 独立节：机制、文献对比（Real-DOI）、综合、局限 |
| 术语 canonical form | `thesis-terminology-ledger.md` | 写时 enforce + extend（新术语标 `source: thesis-dissect`） |

## 动词与语态

- **method**：过去时、被动或 we（不用 show/demonstrate，那是 results）。
- **results**：主结果用 show/demonstrate，趋势级用 suggest/indicate。
- **本章讨论**：机制推断、文献对比用讨论语态（may/could/hedge 允许进这里）；对自家贡献的表述仍用强动词（establishes/shows）；每条文献对比挂 Real-DOI placeholder，不编引文。

---

## Contract-gap handling

**目的**：当小论文的 IMRaD 不能干净映射到目标章形——报告 + 作者填，**不是** validation error。

**契约是**：每模块的 question 都该在小论文（含 SI）里能找到答它的 method + results；章引/讨论该能在 intro/discussion 里找到素材。论文 IMRaD 不干净时，gap 是 fillable hole（contract-gap），不是 fail。镜像 sci-write 的 contract-gap 纪律。

**四种 gap**：

| Gap | 触发 | 处理 |
|---|---|---|
| 无 method section（review / theory paper） | 整篇无 method | **停，flag 作者**："本文无 method——是正文章还是应并入另一章？"作者决定。不静默硬写。 |
| method 散落跨节 | 同一 method 的细节分散在 method、SI、discussion 各处 | **收集到该 method 所答 question 的 module**。把散落片段拉到 module 内。若某 method 细节不答任何 question → **overflow**：park，不硬塞进某模块。 |
| results figure 无对应 method | 某张 figure 有 results 但没显式 method | **method 是隐含/标准的**——简述或引文献（Real-DOI placeholder）。**不编造**。 |
| intro/discussion 缺失或贫瘠（letter / 短文） | 章引或讨论无素材可提 | **停，flag 作者**："本文 intro/discussion 不足以撑章引/讨论——素材从哪来？"作者决定（如：从上一章结果引申）。不空转硬写。 |

**contract-gap 是 fillable hole，不是 validation error**：

- 不 silent-skip（gap 不能跳过不报告）。
- 不 fabricate（无 method 不能编——编出来的 method 是造假，违反 grounding）。
- 不 hard-fail（gap 不让流程停下报错——报告 + 作者填，流程继续其他模块）。

**作者填 gap 的产物**：填进 `thesis/tex/chN.tex` 对应位置（不是单独的 gap 文件）；深读 trace 进 `paper-X/trace.md`；gap 在哪里、作者填了什么 → 审计 trail 在 trace.md。

---

## What this reference is NOT

**这是 pre-write outline 吗？不是。**

本文件指导**写时**的 IMRaD→章形重构 act——你**每写一个章内动作前打开它**，对照纪律当场重构。它**不**产出模块清单、不产 module-map、不在写前规划章节结构。重构结果活在写的 `thesis/tex/chN.tex` 里，不在单独的 map 文件。

**trace.md 的素材清单 ≠ outline**。SI 清单、讨论素材清单是**来源索引**（每条素材登记"是什么 + 去向"），保证零丢弃可审计——它们不包含章节骨架、不预写任何 prose。章的结构和叙事仍在写 tex 时当场发生（拆即写不破坏）。outline-then-fill 是"先画结构再填内容"；素材清单是"先点清料再动手"——前者被禁，后者是深读的本职。

**拆即写 (dissect-is-write) 不变量**（load-bearing）：

- **dissection IS writing**——拆小论文和写章节是同一 act 的两面，不是两步。glossary：`_Avoid_: outline-then-fill`。
- **pre-write outline 是 anti-pattern**——任何"先画 module-map 再据 map 写 tex"的两步流程都违反拆即写（父 spec §③"dissect 不分拆+写两步"）。本文件不是那个 outline。
- **gate 在 act 之后**——post-module gate 审已写 tex 的重构，不在写前 gate 抽象骨架（写前 gate 必须先有 outline）。

**边界**：本文件**只**指导写时重构纪律。它不指导：

- paper→role 绑定（那是 SKILL.md Step 1.1 + `paper-X/binding.md`）。
- 章间递进（那是 chapter-map.md 的 progression-in/out——本文件的章引/小结**落地**它们，不定义它们）。
- 框架实例化（那是 chapter-map.md 的 framework-instantiation）。
- coverage 机械门（那是 `scripts/check_dissect.py`）。
- spine 的层界：spine 只定大问题与每章问题；**模块的问题链与叙事线由本 skill 深读论文时自己长出来**，不回 spine 要，也不替 spine 定。

---

## 跨模块一致性（写完一章后扫一遍）

- **章引↔小结闭环**：章引提的问题，本章小结明确回答；小结抛出的问题 = chapter-map 的 progression-out。
- **question 链一致**：上一模块 results → 本模块 question → ... → 末模块 results 汇入本章讨论的综合。任一断链 → 缺模块或 question 错位。
- **method 自足**：每模块 method 够复现答本 question 的实验，不依赖其他模块的 method（除非显式引用）。
- **术语一致**：同一变量/方法在全章用同一词（首次出现锁定，`thesis-terminology-ledger.md` 记 canonical form）。
- **缩写锚定**：缩写首次出现写"规范中文（ABBR）"（取自 ledger 缩写锚定表的 settled 行），其后用规范中文或缩写——**禁止即兴新译**（"热接触电阻"类错误 = 未锚定的即兴翻译；thermal contact resistance 是接触热阻，不是电阻）。
- **统计一致**：所有模块引到的统计量（n、test、误差类型）和小论文原文**逐字校对**——不改数字、不四舍五入、不改测试名称。
- **figure 引用一致**：模块引 figN，编号一致，不串（并入的 SI 图表同样入账）。
- **去向清零**：trace.md 的 SI 清单与讨论素材清单无 `pending`、无裸条目——每条要么已并入（落点可查），要么弃用有理由。
