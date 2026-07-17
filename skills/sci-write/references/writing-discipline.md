# Writing discipline

本 skill 的写作纪律。零依赖——这里是全部内容，不引用任何外部 skill 的文件。

## 直接写英文，不走中转

**铁的纪律：永远不要先写中文再翻译英文。直接写英文。**

中文和英文的学术表达方式有本质区别。中文材料（用户的笔记、数据描述）的正确处理方式：读中文 → 提取核心命题 → 直接用英文组织论证。不是"翻译"——是"用英文思考、用英文写"。

## 一句话论证优先

写任何章节前，先写出贯穿全文的一句话论证：

> 在 [系统/问题] 中，我们 [用 X 方法] [做出 Y 进展]，由 [Z 证据] 支撑，边界是 [W]。

每个章节、每个 figure 必须服务于这句话。写不出这句话 = 论文还没有论证 = 先解决论证，再写句子。

## Confirmation gate（落盘前对齐）

每个章节在**写完整 prose 之前**，先回显一个对齐块，停下来等人确认：

- **一句话论证**（最重要，必须回显）
- **plan**：章节类型、目标字数、段落分工（每段一个 job）
- **关键术语**：本节用到的核心方法/模型/指标的规范形式
- **关键假设**：你推断而非被告知的，尤其"核心贡献是什么""哪个结果领头"
- **至多 2-3 个 targeted 问题**，只问真正模糊、高杠杆的点

什么时候可以跳过 gate：核心 claim + 证据 + 边界都已明确给出、且没有真正的模糊时。此时回显一句话论证即可继续。

为什么：在错误的假设前提上写完整章节 = 整章废稿 + "这不是我要的"。gate 是在最便宜的时机（写之前）暴露前提错误。

## Targeted revision（不全文重写）

人反馈"这不是我要的"通常是局部的——一个 claim 错、一段框架错、领头的成果选错。**不要**默默重写整章：全文重写会破坏本来对的段落，逼人重审一切。

- 只改人指出的段落或 claim，其余逐字保留。
- 若人的反馈确实要求结构改动（重排章节、跨段移动 claim），先说清楚、确认新结构，再动。
- 反馈揭示原前提错了 → 回 confirmation gate，别在破前提上补 prose。

## 动词校准（按证据强度）

| 强度 | 动词 | 需要的证据 |
|---|---|---|
| 强 | show / demonstrate / establish | 直接、可量化的主结果 |
| 中 | suggest / indicate / support | 趋势级、间接、对照 |
| 弱 | may / could / might | 合理但未验证的机制推测 |

强动词配弱证据 = 审稿人挑刺的靶子。弱动词配强证据 = 低估自己的贡献。每句动词都要和它指向的证据强度匹配。

## Claim 必挂 evidence

每个 claim 必须挂着支撑它的 evidence（figure / 统计 / 对照）。没有 evidence 的 claim：

- **不要硬写**。标 `[evidence needed: 具体描述]` 占位，列到"假设与缺失"清单里。
- 这是数据驱动写作的硬规矩——本 skill 不编造结果、机制、样本量、统计量。

## 扫除无支撑的新颖性/全称断言

成稿前扫一遍：`first` `unique` `unprecedented` `comprehensive` `complete` `always` `never` `revolutionary`。
证据真支持才留，否则改成有边界的 claim 或删掉。

## Results 语法纪律

- **Results**：报告观察到的。`was detected` / `increased` / `showed` / `achieved`。过去时为主。
- 不混解释语法（`may reflect` / `suggests`）——解释是 Discussion 的事。
- 同一段里混用两种语法 = 读者分不清哪是事实哪是解释。

## 段落流（一句话一个 message）

- 一段一个 message。
- 第一句是 topic / claim。
- 后续每句与前一句有明确关系（因果、对照、限定、举例）。
- 模糊时做 reverse outlining：每段提炼一句话，看一句话序列是否成论证链。

## 引用占位符协议（真 DOI，不空占位）

凡涉及外部文献，本 skill 的规矩：

1. **调检索 MCP** 拿到真实文献标识（DOI 等）。
2. **把真实 DOI 落成占位符**，不是空的 `[CITE:?]`，也不是编造的条目。
   - md 里：`[DOI: 10.1038/s41586-023-06xxx]` 或 `[CITE: 作者-年份-主题, DOI:...]`
   - tex 里：`\cite{key}`，key 用语义名（如 `wang2023dose`），并在边注/注释里写明 DOI
3. **最终插入 Zotero/Endnote 永远由 user 完成**。agent 不生成 `.bib` 条目、不替 user 按插入键。
4. 成稿阶段：user 在 Zotero 插入 → agent 可回读 Zotero 同步，或 user 手动更新占位符为正式引用。

这条贯穿全文——Results 引方法时、Discussion 做文献对比时、Method 引标准做法时，都按此协议。**不编文献、不空占位、不留模糊。**

## 输出格式（每章节落盘）

每章节落盘时附简短 notes：

1. `Draft:` — 正文。
2. `Section outline:` — 3-7 个 bullet（写整章时）。
3. `Assumptions or missing inputs:` — 只列实质问题，别凑样式 nit。
4. `Claim-evidence map:` — 主要 claim：`Claim: ... | Evidence: ... | Status: supported / needs evidence / inferred`
5. `To redirect me:` — 一句话请人指名要改的段。

中文笔记输入时：先给英文成稿，再附简短中文说明结构选择。

## 隐私

不在产出（正文、报告、claim-evidence map、commit message）里泄漏私人本地路径、私人文件名、未发表内容。需要提及时用泛称（"提供的数据文件"）。仅在 user 明确要审计轨迹时才露具体路径。
