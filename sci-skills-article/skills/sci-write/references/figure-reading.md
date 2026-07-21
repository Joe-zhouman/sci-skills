# Figure reading — 图义核查操作手册

Step 3 的操作手册。本 skill 用**识图能力**（任何能看图的工具或自带识图的模型都行——不绑具体工具）从**独立读者视角**核查"这张图实际传达了什么"，再和 figN-report 里的 claim 对照。

## 为什么单独有这一步

画图流程（无论哪个工具/skill）通常有**排版审查**（字体、配色、对齐、clipping）——"图做得对不对"。
本 skill 的 Step 3 是**图义核查**——"图传达的结论对不对、读者会不会误读"。

两件事。排版再完美的图，也可能在论证层面误导：claim 说"药 A 优于 B"，但图上 A 和 B 的误差带大量重叠，读者第一眼读出的是"两者相当"。这种 claim↔成图的错位，写作时必须抓住，否则 Results 和 Discussion 会建立在一个读者不接受的 claim 上。

## 用什么识图（不绑工具）

Step 3 需要的是一个**识图能力**：给一张图 + 一段 audit 指令，拿回**独立读者视角**的结构化分析。满足这个的途径有多种，按可用性选：

- **自带识图的模型**（你正在用的模型若支持视觉）：直接给它图 + audit 指令。最直接，无工具依赖。
- **识图 MCP 工具**（如 seed-viz 的 paper-figure 或 general-image）：带 audit 指令作为 extra_prompt 调用。
- **别的视觉工具**：只要能给结构化读者视角分析都行。

**关键约束（无论用哪个）**：
1. **不给 claim 当输入**——独立性是这一步的价值。claim 对照是 sci-write 自己做的（见下），不外包给识图工具/模型。识图工具只负责"读者读到什么"，不知道作者主张什么。
2. **要结构化输出**——audit 模式要的不是"一段成品 prose"，是判断材料（传达了什么 / 显著视觉特征 / 可能误读）。在指令里明确要结构化。
3. **重模型档**——audit 是高杠杆环节，用强模型/高 effort，别图省。

具体怎么写 audit 指令、如果用 seed-viz paper-figure 该怎么调（它现在偏 prose，audit 模式要靠 extra_prompt 驱动），见本 skill 末尾"附录：识图工具调用范例"。**但工具是可选的——核心是 audit 指令本身，任何识图能力配这段指令都行。**

## 调用流程（每张 drawn 的图跑一遍）

1. **读 claim**：从 `../sci-draw/figN-report.md` 的 `## Core conclusion` 拿到本图打算证明的 claim。**若该段缺失或不是一句话 claim**，按"契约缺口处理"请用户补充，不编。
2. **调识图能力（audit 模式，不给 claim）**：把 `../sci-draw/figN.png` 喂给你选定的识图工具/模型，配 audit 指令（见附录）。拿回独立读者的结构化描述。
3. **对照（sci-write 自己做）**：拿识图描述 vs claim，逐条比对：
   - 描述里提到的主趋势，是否就是 claim 说的那个？
   - 描述里的不确定性/重叠/异常，是否被 claim 的强动词（show/demonstrate）掩盖了？
   - 描述里有没有 claim 没提、但读者一定会注意到的特征？（通常是局限或反例）
4. **落盘** `figN-reading.md`（schema 见下）。

## figN-reading.md schema

```markdown
# Figure figN — 图义核查

## claim（来自 report）
<figN-report 的 Core conclusion 原文>

## 图实际传达（来自识图，独立读者视角）
<识图工具/模型产的结构化描述，原样保留——读了什么、显著视觉特征、可能误读>

## 一致性对照（sci-write 自己做的判断）
- 一致点: <claim 的哪部分被图清晰支持>
- 差异/误读风险: <claim 的哪部分被弱化、或图读出了 claim 没说的>
  - 具体到图的哪个视觉特征（如"误差带重叠""某组离群点""y 轴起点非 0"）

## claim 修正建议
<若识图读出的结论比 claim 更窄/更宽/不同，建议如何改 claim。
 标"人介入点"——是否回改 claim / 重画，由 user 拍板，本 skill 不擅自改 report。>
```

## 人介入点

`figN-reading.md` 的"claim 修正建议"是**软建议**，不是自动改写。落盘后明确问 user：

> 图义核查发现 claim "X" 与成图传达存在 [差异描述]。建议 [改 claim 为 Y / 回画图重画 / 接受现状加限定]。你要怎么处理？

user 选了才动。三种处理：
- **改 claim**：更新 paper-plan 该图的 claim + 在 report-ref 处留注。report 在图仓库里、本 skill 默认不直接改它（除非用户明确允许）——修正记录在 `figN-reading.md`，Results 引用时以 reading 的修正版为准。
- **重画**：提示 user 回画图工具重画该图，paper-plan status 改回 pending。
- **加限定**：claim 不改，但在 Results/Discussion 写作时主动加边界说明。

## 不做什么

- **不做排版审查**（字体/配色/对齐）——那是画图流程的活。本步骤只关 claim↔传达。
- **不用弱模型档**——图义核查是高杠杆环节，强模型/高 effort 值得。
- **不读 figN-description.md**——那是 maker 草稿，不该影响 reader 视角的独立判断。
- **不给识图工具 claim**——见上，独立性是价值所在。
- **不擅自改 figN-report.md**——那是图仓库的产物，本 skill 默认只读。修正记录在 figN-reading.md；缺口让人补、不自己编。

## 多 panel 图（可选）

若一张图有多 panel（a/b/c），有的识图工具一次接受多张图。需要时可把整图 + 单 panel 切片分别喂，对照"整体印象 vs 单 panel 细节"是否一致。多数情况整图一次够。

---

## 附录：识图工具调用范例（工具可选，指令是核心）

下面给一个 audit 指令范例。**这段指令是核心——任何识图能力（自带视觉的模型 / paper-figure / general-image / 别的工具）配它都行。** 范例只是示范，不是绑定。

audit 指令（喂给识图工具/模型的 prompt）：

> Analyze this figure as an independent reader. You do NOT know the author's
> claim — analyze purely what is visually there. Report in three sections:
> (1) What the figure conveys at a glance — the main trend/comparison a reader
> would form in the first few seconds.
> (2) Notable visual features — specific elements (overlapping error bands,
> divergent series, non-zero axis start, color choices) and what they imply.
> (3) Potential misreads — any features a reader might interpret differently
> from the author's likely intent, or ambiguities.
> Do NOT assess whether the figure supports any specific claim; describe what
> is visually there.

如果用 **seed-viz paper-figure**：它当前默认偏"写一段 publication prose"，audit 模式靠 extra_prompt 驱动——把上面这段作为 extra_prompt 传入，并明确要三段结构化输出（它若按 prose 默认就会忽略结构要求，所以 extra_prompt 里"Report in three sections"这句要明确）。PRO / high effort。paper-figure 正在被重新设计成更通用的学术图分析能力（audit 模式将更自然），但即使不改，靠 extra_prompt 也能让它进 audit 模式。

如果用 **自带视觉的模型**：直接把图 + 上面指令给它，要结构化输出。最干净、无工具依赖。

如果用 **seed-viz general-image**：同 paper-figure，audit 指令作 extra_prompt，pro/high。general-image 比 paper-figure 更通用（不特化学术图），但 audit 指令能补上学术图需要的关注点（误差带、显著性标注等）。
