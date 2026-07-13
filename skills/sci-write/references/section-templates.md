# Section templates — 数据驱动四件套结构

本 skill 写 Method / Results / Discussion / Conclusion 四章。Introduction / Abstract / Keyword 不在此（external，外接）。

每个模板给"骨架 + 每段的 job + 素材来源"。素材来源指向本 skill 已落盘的文件（data-profile.json / figN-report.md / figN-reading.md），不指向任何外部 skill。

---

## Method

**目的**：让读者能复现。纯事实陈述，不检索、不叙事。

**结构（每段一个 job）**：

1. **数据来源段**
   - job: 说明数据是什么、从哪来、多少。
   - 素材: `data-profile.json`（样本量 N、每组 n、变量列表、缺失率）。
   - 例: "We analyzed [N] samples from [来源描述]. The dataset contains [变量列表]. Missing data: [率/处理]."

2. **关键变量段**
   - job: 定义每组的含义、每列的语义（连续/分类/序数）、单位。
   - 素材: `data-profile.json` 的 columns 段。
   - 注意: 区分 ID 列 vs 真实变量——ID 被误当连续是经典坑。

3. **统计方法段**
   - job: 每个比较用的什么 test、什么 correction、误差类型、n。
   - 素材: 各 `figN-report.md` 的 `## Statistical methods` 段——**逐字搬运**，不自创。
   - 例: "Group comparisons used [test] with [correction] correction. Error bars represent [SD/SEM/95% CI]. Significance: *p<0.05, **p<0.01. n=[X] per group."

4. **图表方法段（可选）**
   - job: 说明用了什么可视化、为何选（审稿人会问）。
   - 素材: 各 `figN-report.md` 的 `## Chart type & rationale`。

**动词**：Method 几乎全是过去时、被动或 we。不用 show/demonstrate（那是 Results）。

**不写**：不用检索文献"标准做法也用此方法"——若要引，走引用占位符协议（真 DOI）。

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

**动词校准**: 主结果用 show/demonstrate；趋势级用 suggest/indicate；机制推测留到 Discussion。

**Results 不做**: 不解释为什么（那是 Discussion）；不引文献对比（那是 Discussion）；不混 `may reflect` 这类解释语法。

---

## Discussion

**目的**：解释 Results、定位贡献、说局限。**机制解释 + 文献对比，不是 Results 的复述。**

**结构**:

1. **开头：主发现的解释段**
   - job: 不复述结果，回答"这意味着什么"。
   - 例: "Our results [show/demonstrate] that [主发现]. This [suggests/indicates] [机制或意义]."
   - 素材: Results 的主 claim + `figN-reading.md`（图实际传达）。

2. **机制段**（核心）
   - job: 为什么会观察到这个？给出合理机制。
   - 动词: may / could / might（机制推测，配弱动词）。
   - 注意: 机制是推测——必须配"这是 plausible 但未直接验证"的边界。

3. **文献对比段**
   - job: 和已有工作比——一致、延伸、还是冲突？
   - **调检索 MCP 拿真实 DOI**，走引用占位符协议。**不空占位、不编文献。**
   - 例: "Our finding aligns with [Wang2023, DOI:...] who reported [...]. We extend this by [...]."
   - 冲突尤其重要：和文献不一致的地方要说清楚、给解释。

4. **局限段**
   - job: 你的证据边界在哪。
   - 诚实：样本量、数据来源、未控变量、泛化范围。审稿人会挑的，你自己先说。

5. **影响/展望段**（可选）
   - job: 这意味着什么、下一步。
   - 不要过度——bounded claim。

**Discussion 不做**: 不报新数据（那是 Results）；不用 `was detected` 这类观察语法（那是 Results）。

---

## Conclusion

**目的**：从 findings 收口。短。不引入新内容。

**结构**（一段或几段，紧凑）:

1. **贡献声明**: 我们做出了什么。（主 claim，从 paper-plan + Results 提炼）
2. **证据一句话**: 由 [figN 的关键 evidence] 支撑。
3. **局限一句话**: 边界在哪。
4. **影响一句话**: 这意味着什么（bounded，不吹）。

**动词**: 主贡献用 show/demonstrate；影响用 suggest/enable。

**Conclusion 不做**: 不复述 Results 细节；不引入 Discussion 没讨论过的新机制；不出现新引用（引用都在前章已出现）。

---

## 章节间一致性（写完四章后扫一遍）

- **claim 一致**: Results 的 claim、Discussion 的解释、Conclusion 的贡献声明，三者不矛盾。figN-reading.md 的修正版贯穿三章。
- **术语一致**: 同一变量/方法在四章里用同一个词。建一个术语小账，首次出现锁定，后续复用。
- **统计一致**: 所有章节引到的统计量（n、test、误差类型）和 `figN-report.md` 的 `Statistical methods` 完全一致——逐字校对。
- **figure 引用一致**: Results 引 "Fig 1"，Discussion 解释 "Fig 1"，编号一致，不串。
