# Restructure discipline — IMRaD→method-results 写时重构纪律

本 skill 在写每个模块前打开本文件。它指导**写时**的 IMRaD→method-results 重构——dissect-by-writing，拆即写——**不是 pre-write outline**。重构活在写的 `thesis/tex/chN.tex` 里，不在单独的 module-map 文件。

每个模块做一件事：深读对应的小论文片段 → 把它的 IMRaD（intro→method→results→discussion 序列）当场重构成 method-results 对 → 写进 `thesis/tex/chN.tex`。重构不是额外动作——它就是写。

---

## The modular restructure principle

**目的**：把小论文的 IMRaD 序列重构成学位论文正文章的模块化结构。

小论文是 IMRaD——intro→method→results→discussion 各成一段、独立成篇的叙事。学位论文正文章**不是** IMRaD：method 紧跟对应 results（**配对，非 IMRaD 序列**），每个对子是一个 **module**。module = **question→method→results 三元**（原子单元）：

1. **question** — 本模块要答的问题。由**上一模块的 results** 引发（module 1 的 question 由章节开篇 question 引发）。是连接上一模块与本模块的逻辑钩子。
2. **method** — 为了答这个问题做了什么。够复现；统计量、参数、样本量**逐字搬运**自小论文，不改数字、不四舍五入、不改测试名称。
3. **results** — 数据显示什么（答案）。引 figure/stat。

三元是原子单元；模块链起来：results → next question → next method → next results → ...。一个章 = 一串模块。

**关键区别（对照 IMRaD）**：

| | 小论文 IMRaD | 学位论文章节 |
|---|---|---|
| 组织 | 顺序：intro→method→results→discussion | 配对：method 紧跟对应 results |
| 单元 | section（method 一整块、results 一整块）| module（question→method→results 三元）|
| 串联 | discussion 统一解释 | 上一 results 引发下一 question |
| 读者路径 | 读完 method 全部再看 results | 每模块自足：问→做→答 |

**模块的 question 来自哪**：

- **module 1** — 章节开篇 question（spine 的 role 落地：本章要答的核心问题）。
- **module N (N>1)** — 上一模块的 results 引发的新问题（"既然观察到 X，那 Y 吗？"）。
- 列不出 question → 这个模块不该在这（并入上一模块，或它是 contract-gap——见下）。

---

## How to restructure IN-WRITE (dissect-by-writing)

**目的**：每模块通过**写其 tex** 来拆它——拆和写是同一 act（拆即写），不是两步。

**per-module 骨架**：

1. **打开本文件**（你已经在做了）。
2. **深读该模块对应的小论文片段** — 找到答本模块 question 的那部分 method + results（不是整篇论文，是本模块的切片）。
3. **直接写 method-results 对** — 不要先转写小论文的 IMRaD 序列。把答本 question 的 method 拉到对应 results 旁，写进 `thesis/tex/chN.tex`（tex-direct，无 md 中间；Real-DOI placeholder）。
4. **post-module gate** — 模块 tex 写完后，作者审"这个模块的重构（已落在 tex 里）好不好？" 不满意 → 改（逻辑还热）；满意 → 下一模块。

**关键纪律**：

- **重构 IS 写作**。IMRaD→method-results 重构在写的过程中发生——你边写边把 method 拉到 results 旁，不先画 module-map 再填。
- **逻辑热时写**。深读完该模块切片后立即写——逻辑还在工作记忆里。两步（拆笔记→后写章）要重新载入一遍刚捋过的逻辑，浪费且易丢（glossary `_Avoid_: outline-then-fill`）。
- **无 pre-write outline**。不产 `module-map.md` 文件。重构结果活在 `thesis/tex/chN.tex` 里——你写的就是重构。
- **post-module gate ≠ pre-write gate**。gate 在 tex 写完后，不在写前。pre-write gate 必须先有 module-map（= outline），违反拆即写。post-module gate 把判断移到 act 之后——审实现的 prose，不审抽象骨架（镜像 sci-write 的 confirmation gate，post-write 非 pre-write-outline）。

**素材来源——从文件提取，不编造**：

| 需要的内容 | 从哪来 | 怎么用 |
|---|---|---|
| 本模块 question | 上一模块 results（或章节开篇 question）| 三元第一段：写"既然 X，那 Y 吗？" |
| method（参数、样本、统计）| 小论文 method section 对应片段 | 拉到对应 results 旁——**逐字**，不改数字、不四舍五入、不改测试名称 |
| results（figure/stat）| 小论文 results/figures 对应片段 | 三元第三段：写"数据显示 X" + 引 figN + 统计量 |
| 术语 canonical form | `thesis-terminology-ledger.md` | 写时 enforce + extend（新术语标 `source: thesis-dissect`）|

**动词**：method 用过去时、被动或 we（不用 show/demonstrate，那是 results）；results 主结果用 show/demonstrate，趋势级用 suggest/indicate。may/could 不进模块——本 skill 不写讨论（见"不写"）。

**不写**：

- 不转写小论文的 IMRaD 序列（intro→method→results→discussion 原样搬）——那是论文合集不是章节。
- 不写 pre-write module-map——没有这个文件；重构在 tex 里。
- 不解释 results 的 mechanism（那是讨论，本 skill 不写）。
- 不引文献对比（那是讨论）。
- 不复述 method（method 在本模块内自足；下一模块有新 method 再写）。

---

## Contract-gap handling

**目的**：当小论文的 IMRaD 不能干净映射到 method-results 对——报告 + 作者填，**不是** validation error。

**契约是**：每模块的 question 都该在小论文里能找到答它的 method + results。论文 IMRaD 不干净时，gap 是 fillable hole（contract-gap），不是 fail。镜像 sci-write 的 contract-gap 纪律。

**三种 gap**：

| Gap | 触发 | 处理 |
|---|---|---|
| 无 method section（review / theory paper）| 整篇无 method | **停，flag 作者**："本文无 method——是正文章还是应并入另一章？"作者决定。不静默硬写。 |
| method 散落跨节 | 同一 method 的细节分散在 method、SI、discussion 各处 | **收集到该 method 所答 question 的 module**。把散落片段拉到 module 内。若某 method 细节不答任何 question → **overflow**：park，不硬塞进某模块。 |
| results figure 无对应 method | 某张 figure 在小论文里有 results 但没显式 method | **method 是隐含/标准的**——简述或引文献（Real-DOI placeholder）。**不编造**。 |

**contract-gap 是 fillable hole，不是 validation error**：

- 不 silent-skip（gap 不能跳过不报告）。
- 不 fabricate（无 method 不能编——编出来的 method 是造假，违反 grounding）。
- 不 hard-fail（gap 不让流程停下报错——报告 + 作者填，流程继续其他模块）。

**作者填 gap 的产物**：填进 `thesis/tex/chN.tex` 对应模块（不是单独的 gap 文件）；深读 trace 进 `paper-X/trace.md`；gap 在哪里、作者填了什么 → 审计 trail 在 trace.md。

---

## What this reference is NOT

**这是 pre-write outline 吗？不是。**

本文件指导**写时**的 IMRaD→method-results 重构 act——你**每写一个模块前打开它**，对照纪律当场重构。它**不**产出模块清单、不产 module-map、不在写前规划章节结构。重构结果活在写的 `thesis/tex/chN.tex` 里，不在单独的 map 文件。

**拆即写 (dissect-is-write) 不变量**（load-bearing）：

- **dissection IS writing**——拆小论文和写章节是同一 act 的两面，不是两步。glossary：`_Avoid_: outline-then-fill`。
- **pre-write outline 是 anti-pattern**——任何"先画 module-map 再据 map 写 tex"的两步流程都违反拆即写（父 spec §③"dissect 不分拆+写两步"）。本文件不是那个 outline。
- **gate 在 act 之后**——post-module gate 审已写 tex 的重构，不在写前 gate 抽象骨架（写前 gate 必须先有 outline）。

**边界**：本文件**只**指导写时重构纪律。它不指导：

- paper→role 绑定（那是 SKILL.md Step 1.1 + `paper-X/binding.md`）。
- 章间递进（那是 chapter-map.md 的 progression-in/out）。
- 框架实例化（那是 chapter-map.md 的 framework-instantiation）。
- coverage 机械门（那是 `scripts/check_dissect.py`）。

---

## 跨模块一致性（写完一章后扫一遍）

- **question 链一致**：上一模块 results → 本模块 question → ... → 末模块 results 回答章节开篇 question。任一断链 → 缺模块或 question 错位。
- **method 自足**：每模块 method 够复现答本 question 的实验，不依赖其他模块的 method（除非显式引用）。
- **术语一致**：同一变量/方法在全章用同一词（首次出现锁定，`thesis-terminology-ledger.md` 记 canonical form）。
- **统计一致**：所有模块引到的统计量（n、test、误差类型）和小论文原文**逐字校对**——不改数字、不四舍五入、不改测试名称。
- **figure 引用一致**：模块引 figN，编号一致，不串。
