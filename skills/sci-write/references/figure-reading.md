# Figure reading — seed-viz paper-figure 调用规范

Step 3 图义核查的操作手册。本 skill 用 seed-viz 的 `paper-figure` action（专门为读科研图设计的通道）从**读者视角**核查"这张图实际传达了什么"，再和 paper-plan 里的 claim 对照。

## 为什么单独有这一步

画图流程（无论哪个工具/skill）通常有**排版审查**（字体、配色、对齐、clipping）——"图做得对不对"。
本 skill 的 Step 3 是**图义核查**——"图传达的结论对不对、读者会不会误读"。

两件事。排版再完美的图，也可能在论证层面误导：claim 说"药 A 优于 B"，但图上 A 和 B 的误差带大量重叠，读者第一眼读出的是"两者相当"。这种 claim↔成图的错位，写作时必须抓住，否则 Results 和 Discussion 会建立在一个读者不接受的 claim 上。

## paper-figure action 是什么

seed-viz 的 `paper-figure`（查源码：`seed-viz/src/tools/paper-figure.ts`）：
- **输入**：1-2 张图（figN.png），可选 extra prompt
- **产出**：一段 publication-ready 的学术图分析（从学术视角完整描述图）
- **默认**：PRO 模型档、high effort（重活，别降到 lite）
- **不读 claim 文本**——它只看图、独立给描述。这是优点：它的描述不被你的 claim 污染，正好用来做独立对照。

## 调用流程（每张 drawn 的图跑一遍）

1. **读 claim**：从 `../sci-draw/figN-report.md` 的 `## Core conclusion` 拿到本图打算证明的 claim。**若该段缺失或不是一句话 claim**，按"契约缺口处理"请用户补充，不编。
2. **调 paper-figure**：把 `../sci-draw/figN.png`（导出的预览图）喂给 seed-viz 的 paper-figure action。extra prompt 建议：
   > Describe what this figure shows from a reader's perspective: the main trend, the comparison, the uncertainty, and any visual impression a reader might form in the first 5 seconds.
3. **对照**：拿 paper-figure 的描述 vs claim，逐条比对：
   - 描述里提到的主趋势，是否就是 claim 说的那个？
   - 描述里的不确定性/重叠/异常，是否被 claim 的强动词（show/demonstrate）掩盖了？
   - 描述里有没有 claim 没提、但读者一定会注意到的特征？（通常是局限或反例）
4. **落盘** `figN-reading.md`（schema 见下）。

## figN-reading.md schema

```markdown
# Figure figN — 图义核查

## claim（来自 report）
<figN-report 的 Core conclusion 原文>

## 图实际传达（来自 seed-viz paper-figure）
<paper-figure action 产的描述段，原样保留>

## 一致性对照
- 一致点: <claim 的哪部分被图清晰支持>
- 差异/误读风险: <claim 的哪部分被弱化、或图读出了 claim 没说的>
  - 具体到图的哪个视觉特征（如"误差带重叠""某组离群点""y 轴起点非 0"）

## claim 修正建议
<若 paper-figure 读出的结论比 claim 更窄/更宽/不同，建议如何改 claim。
 标"人介入点"——是否回改 claim / 重画，由 user 拍板，本 skill 不擅自改 report。>
```

## 人介入点

`figN-reading.md` 的"claim 修正建议"是**软建议**，不是自动改写。落盘后明确问 user：

> 图义核查发现 claim "X" 与成图传达存在 [差异描述]。建议 [改 claim 为 Y / 回 sci-draw 重画 / 接受现状加限定]。你要怎么处理？

user 选了才动。三种处理：
- **改 claim**：更新 paper-plan 该图的 claim + 在 report-ref 处留注。report 在图仓库里、本 skill 默认不直接改它（除非用户明确允许）——修正记录在 `figN-reading.md`，Results 引用时以 reading 的修正版为准。
- **重画**：提示 user 回 sci-draw 重画该图，paper-plan status 改回 pending。
- **加限定**：claim 不改，但在 Results/Discussion 写作时主动加边界说明。

## 不做什么

- **不做排版审查**（字体/配色/对齐）——那是画图流程的活。本步骤只关 claim↔传达。
- **不调 lite 档**——图义核查是高杠杆环节，PRO/high effort 值得。
- **不读 figN-description.md**——那是 maker 草稿，不该影响 reader 视角的独立判断。
- **不擅自改 figN-report.md**——那是图仓库的产物，本 skill 默认只读。修正记录在 figN-reading.md；缺口让人补、不自己编。

## 多图对照（可选）

若一张图有多 panel（a/b/c），paper-figure 接受最多 2 张图。需要时可把整图 + 单 panel 切片分别喂，对照"整体印象 vs 单 panel 细节"是否一致。多数情况整图一次够。
