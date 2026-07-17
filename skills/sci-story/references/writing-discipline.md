# Writing discipline — 叙事写作纪律

本 skill 的写作纪律。零依赖——这里是全部内容，不引用任何外部 skill 的文件。

## 四问脊柱优先

**先有 claim，才有 Introduction。** 一切写作围绕一个核心 claim 展开：gap 是什么，你解决了什么。图的 claim 是大 claim 的小 claim。Introduction 是 claim 的包装。Discussion 是 claim 的回答。没有 claim = 没有故事 = 不要写。

写任何章节前，先写出贯穿全文的四问脊柱：

> (1) 我们解决什么问题？为什么没有已有方案能解决？
> (2) 我们的贡献是什么？
> (3) 为什么我们的方法本质上能 work？
> (4) 我们提供了什么优势和新的洞见？

**Gap 不能多——找最核心的那个。** "他用了 scikit-learn，你用了 XGBoost"不算 gap。"他用了 XGBoost，你提了一个新算法"才算。不是所有差异都是 gap——只有从 claim 倒推回来、必须填的那个洞才是。提的所有问题必须能收敛到一句 gap 句子。收不拢 → gap 太多了，删到剩一个。

写不出脊柱 = 论文还没有论证 = 先解决论证，再写句子。

## 直接写英文，不走中转

**铁的纪律：永远不要先写中文再翻译英文。直接写英文。**

中文和英文的学术表达方式有本质区别——中文学术写作倾向 topic-comment 结构、隐式逻辑连接、长串逗号分句；英文学术写作要求 subject-verb proposition、显式逻辑关系、句间连接词。先写中文再过翻译，相当于把英文的论证骨架硬塞进中文的句法模板里再拆出来——两次变形之后，逻辑线全断。

中文材料（用户的笔记、数据描述、中文草稿）的正确处理方式：读中文 → 提取核心命题 → 直接用英文组织论证。不是"翻译"——是"用英文思考、用英文写"。中文只是信息来源，不是语言模板。

## Introduction-Discussion 一致性铁律

Introduction 和 Discussion 是同一块论证的正反两面：

- Intro gap（"这里有个缺口，前人没填"）→ Discussion 必须填（"我们填了，这意味着 X"）。
- Intro 声称的核心问题必须是 Discussion 解释的核心发现。
- Intro 提出的竞争假说/现有方法的局限 → Discussion 必须回应。
- Intro 没提的 gap → Discussion 不能突然冒出解释（无根之木）。

写完 Introduction 和 Discussion 后，跑两道自检：

**Check 1 — 故事主线。** 抛开骨架，用白话文把论文讲一遍：

```
背景：[……]下，[……]成了瓶颈。
前人：有人做了[……]、[……]、[……]。
但他们都卡在：[……]。
我们：[……]。
结果我们发现了：[……]。
这意味着：[……]，但限于[……]。
```

读一遍。断了、跳了、gap 跟 contribution 对不上 → 结构有问题，回头修结构不修措辞。

**Check 2 — Gap-fill 对齐。** 逐条对照：

```
Intro 提了 gap/bottleneck     →  Discussion/Present study 填了吗？
  "X 未解决"                  →   填了：我们用 Y
  "现有方法在 Z 条件下失效"    →   填了：Z 条件下我们生效，因为 W
```

- Intro 提了但没填 → 砍掉，或补 Discussion。
- Discussion 里出现但 Intro 没铺垫 → 要么 Intro 补一句，要么砍掉。

两条都不通过不落盘。

## Confirmation gate（落盘前对齐）

每个章节在写完整 prose 之前，先回显一个对齐块，停下来等人确认：

- **一句话论证**（最重要，必须回显）
- **plan**：章节类型、目标字数、段落分工（每段一个 job）
- **关键术语**：本节用到的核心概念/方法的规范形式
- **关键假设**：你推断而非被告知的，尤其"gap 是什么""哪个发现是主贡献"
- **至多 2-3 个 targeted 问题**，只问真正模糊、高杠杆的点

什么时候可以跳过 gate：核心 gap + 贡献 + 边界都已明确给出、且没有真正的模糊时。此时回显一句话论证即可继续。

为什么：在错误的假设前提上写完整章节 = 整章废稿 + "这不是我要的"。gate 是在最便宜的时机（写之前）暴露前提错误。

## Targeted revision（不全文重写）

人反馈"这不是我要的"通常是局部的——一个 gap 表述错、一段解释框架错、贡献的定性错。不要默默重写整章：全文重写会破坏本来对的段落，逼人重审一切。

- 只改人指出的段落或 claim，其余逐字保留。
- 若人的反馈确实要求结构改动（重排段落、跨段移动论证），先说清楚、确认新结构，再动。
- 反馈揭示原前提错了 → 回 confirmation gate，别在破前提上补 prose。

## 动词校准（按叙事强度）

| 强度 | 动词 | 使用场景 |
|---|---|---|
| 强 | show / demonstrate / establish | Introduction 陈述贡献时；Discussion 陈述主发现时 |
| 中 | suggest / indicate / support | Discussion 解释机制时 |
| 弱 | may / could / might | Discussion 推测机制/影响时；Introduction 陈述前人工作的局限时 |

Introduction 用词一般比 Discussion 确定——Introduction 陈述"我们做了什么"是事实（过去时），Discussion 陈述"这意味着什么"是解释（现在时 + 情态动词）。

Discussion 的机制推测必须配弱动词——这是推测，不是直接证据。同时配边界声明。

## 段落流（一句话一个 message）

- 一段一个 message。
- 第一句是 topic / claim。
- 后续每句与前一句有明确关系（因果、对照、限定、举例）。
- 模糊时做 reverse outlining：每段提炼一句话，看一句话序列是否成论证链。

## 引用占位符协议（真 DOI，不空占位）

凡涉及外部文献，本 skill 的规矩：

1. **调检索 MCP** 拿到真实文献标识（DOI 等）。
2. **把真实 DOI 落成占位符**，不是空的 `[CITE:?]`，也不是编造的条目。
3. **最终插入 Zotero/Endnote 永远由 user 完成**。agent 不生成 `.bib` 条目、不替 user 按插入键。
4. Introduction 引前人工作走此协议；Discussion 做文献对比走此协议。

## 扫除无支撑的新颖性/全称断言

成稿前扫一遍：`first` `unique` `unprecedented` `comprehensive` `complete` `always` `never` `revolutionary`。
证据真支持才留，否则改成有边界的 claim 或删掉。

## 输出格式（每章节落盘）

每章节落盘时附简短 notes：

1. `Draft:` — 正文。
2. `Section outline:` — 3-7 个 bullet（写整章时）。
3. `Assumptions or missing inputs:` — 只列实质问题。
4. `Intro-Discussion coherence check:` — 仅 Intro 和 Discussion 章节：列出 gap 和对应的解释，确认一致。
5. `To redirect me:` — 一句话请人指名要改的段。

中文笔记输入时：先给英文成稿，再附简短中文说明结构选择。

## 隐私

不在产出（正文、claim-evidence map、commit message）里泄漏私人本地路径、私人文件名、未发表内容。需要提及时用泛称（"提供的数据文件"）。仅在 user 明确要审计轨迹时才露具体路径。
