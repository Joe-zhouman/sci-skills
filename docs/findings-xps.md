# XPS Skill 调研 — 现成 skill + 工具链

**调研日期：** 2026-07-22
**目的：** 为 `sci-skills-analysis:xps` skill 的设计收集外部事实。用户原则待定，本文只摆事实不设计。

---

## 1. 现成 skill 调研（核心问题："有没有现成 skill"）

去掉 "claude code" 关键词后（skill 现在是通用标准，agentskills.io），找到 4 个相关 skill。**无一可直接复用为 sci-skills-analysis:xps**——原因如下：

### 1a. `xps-surface-analyzer`（agentskill.sh / @a5c-ai）
- 宣称："advanced XPS analysis for surface composition and chemical state characterization of nanomaterials"
- 实质：**SKILL.md 仅 2.1 KB，单文件，无脚本/无 references**。agentskill.sh 质量分 67/100（Discovery/Implementation/Structure/Expertise 全是 "2"）。
- 不可复用原因：只有泛泛的"做 XPS 分析"口号，无具体管线、无背景扣除方法、无拟合约束规则、无产物文件结构。是占位级 skill。
- 来源：https://agentskill.sh/@a5c-ai/xps-surface-analyzer

### 1b. `raman-fitting`（skillsmp.com / lazyfroglol）
- 实质：**纯过程性知识 SKILL.md，无脚本**。内容是 Raman 峰拟合的流程指引。
- 可借鉴点（结构清晰，XPS 可类比的）：
  - "Critical First Step: Data Exploration"——先验文件格式（分隔符、locale 小数点 `47183,554644`）、数据范围、噪声/基线，再拟合
  - 峰函数选择表：Lorentzian（自然线宽）/ Gaussian（仪器展宽）/ Voigt（最物理）/ Pseudo-Voigt（计算便宜）
  - **拟合失败警告信号**：参数顶到边界、R²<0.5、峰位偏移>50 cm⁻¹、线宽异常(<5 或 >200)、负强度
  - "Do NOT accept poor fits as 'the best possible' without exhausting alternatives"
  - 输出要求：预处理 + 函数+理由 + 参数+不确定度 + R² + 文献对比 + 限制
- 不可直接复用原因：Raman 特化（D/G/2D 峰、cm⁻¹、graphene 文献值），无 XPS 的结合能/RSF/化学态指认逻辑。
- 来源：https://skillsmp.com/creators/lazyfroglol/harness_engineering/skills-raman-fitting

### 1c. `raman-spectroscopy-peak-fitting`（mcpmarket.com）
- 强调 R² + 残差分析、可复现、与文献一致。未拿到正文（mcpmarket 页面未抓全），但从描述看与 1b 同构。
- 来源：https://mcpmarket.com/tools/skills/raman-spectroscopy-peak-fitting

### 1d. `scientific-materials-characterization`（nahisaho/coreclaw-marketplace，GitHub）
- **一个 skill 覆盖 XRD / SEM / TEM / XPS / FTIR / Raman + 材料性质数据库查询**。
- 这是用户 `sci-skills` 哲学（"小零件不卖全家桶"）的**反例**。内容极简：
  - Deliverables: `report.md` + `results/` + `figures/` + `data/` + `logs/process-log.jsonl`
  - Quality Gates: 方法匹配问题、可复现、不确定度显式化、日志可追溯
  - 仅此而已——每个表征技术下**没有**任何特化流程
- 不可复用原因：全家桶 = 每个技术都浅。这正是 sci-skills 拆成 per-technique 小零件要避免的。
- 来源：https://github.com/nahisaho/coreclaw-marketplace/blob/main/coreclaw-skills-hub/skills/scientist/scientific-materials-characterization/SKILL.md

**结论：没有可直接 fork 的 XPS skill。** `raman-fitting` 的**结构骨架**（数据探索→背景→函数选择→约束→验证→失败处理→输出要求）值得借鉴，但内容需全部按 XPS 重写。

---

## 2. XPS Python 工具链（这些是软件，不是 skill）

| 软件 | 性质 | 关键事实 |
|---|---|---|
| `lmfit` | 通用拟合库 | **事实上的拟合底座**。LG4X、KherveFitting 都建在它上面。非 XPS 专属但最稳。 |
| `pynxtools-xps`（FAIRmat） | reader + NeXus 规范 | 读 VAMAS `.vms`/`.npl`（ISO 14976）+ CasaXPS 导出的 TXT。是数据入口的事实标准。 |
| `LG4X`（hidecode221b） | lmfit 的 GUI | 封装 XPS 曲线拟合；Shirley/Tougaard 实现来自 Kane O'Donnell 和 James Mudd。 |
| `KherveFitting` | 全功能 XPS+Raman | 用 `lmfitxps`（专门 XPS 拟合）；多背景法、约束、深度剖析、PCA。商业级的免费替代。 |
| `xps`（PyPI, Kalliecharan 2022） | 小型库 | 参考 Briggs & Seah 1983。维护不活跃。 |
| `spectrochempy` | 通用光谱 | 覆盖更广但非 XPS 专精。 |

**无单一统治性 XPS 库**（不像 scipy 之于统计）。`lmfit` + 手写 Shirley/Tougaard（或 fork LG4X 的实现）是最可控路线。

来源：
- https://github.com/hidecode221b/LG4X
- https://github.com/KherveFitting/KherveFitting
- https://fairmat-nfdi.github.io/pynxtools-xps/reference/vms.html

---

## 3. XPS 分析标准管线（方法论）

基于 HarwellXPS Guru（Mark Isaacs, 2025-08 更新）+ MolSSI 教程：

```
1. 能量校准 / 参照
   - 传统：C 1s 外来碳 284.8 eV（⚠️ 见 §5 致命坑）
   - 现代：用内标峰（如 Au 4f7/2 = 83.96 eV）或已知化学态

2. 背景扣除（同一数据集内必须一致）
   - Linear：历史遗留；聚合物/大带隙材料（峰后背景小步阶）可接受
   - Shirley：S 形迭代，减峰不对称；**新用户最可靠可重复**，推荐通用默认
   - Tougaard：物理意义最强（通用截面法），但**需已知散射性质**才靠谱
   - 规则：多区域分析时全数据集用同一种背景

3. 峰拟合 / 解卷
   - Voigt = 高斯 ⊗ 洛伦兹卷积（物理最正：仪器展宽 ⊗ 自然线宽）
   - GLS（高斯-洛伦兹和）/ GLP（积）= 经验近似
   - 约束：FWHM、位置、面积必须受限，否则过拟合
   - 经验法则：一个峰拆几组分要看化学证据，不能纯靠 R²

4. 定量 / 原子 %
   - 峰面积 ÷ RSF（相对灵敏度因子）
   - RSF 体系：Scofield（常用）vs Wagner——数据集内必须统一一套

5. 化学态指认
   - 对照结合能表：NIST XPS Database（srdata.nist.gov/xps）为权威
   - 例：C 1s → C-C (~284.8) / C-O (~286) / C=O (~288) / O-C=O (~289)
```

来源：
- https://www.harwellxps.guru/xpskb/background-types/
- https://education.molssi.org/python-scripting-experimental/xps_processing.html
- GLS/GLP/Voigt 论文：Applied Surface Science 2018 (doi 10.1002/sia.6079 系)

---

## 4. 文件格式

- **VAMAS `.vms` / `.npl`（ISO 14976）** = 通用交换格式。几乎所有仪器都能导出。`pynxtools-xps` 原生读。
- 厂商私有格式：
  - CasaXPS：`.csl`/`.sle`；可导出 TXT（pynxtools-xps 也支持这种 standalone TXT）
  - PHI MultiPak：ASCII，经 CasaXPS 转 ISO
  - Kratos Vision：`.dset`
  - Thermo Avantage：`.pca`/`.sdat`
- 技能策略：**优先吃 VAMAS**；私有格式让用户先在仪器软件/CasaXPS 导出为 VAMAS 或两列 TXT（BE, counts）。

来源：
- https://fairmat-nfdi.github.io/pynxtools-xps/reference/vms.html
- CasaUserGuide（sssc.usask.ca/documents/CasaUserGuide.pdf）

---

## 5. 可复现性痛点（skill 应拦截的坑）

1. **外来碳 284.8 eV 校准不可靠**（最致命，近年文献共识）
   - Gengenbach 2022, *Applied Surface Science* 606, 154855："C 1s peak of adventitious carbon shows markedly large shifts from the 'recommended' 284.8 eV that basically disqualifies its reliability"
   - "Undressing the myth..." (ResearchGate 358746525)："typical values 284.5/284.8/285.0 eV... use of adventitious carbon in XPS should be discontinued... ISO and ASTM charge referencing guides need to be rewritten"
   - **skill 应做的事**：用外来碳校准时显式警告 + 记录校准值与来源；推荐内标或已知化学态。

2. 背景法不一致（多区域混用 Shirley/Tougaard/linear）→ 定量不可比

3. 无约束拟合 → 过拟合，多拆几个分组分就能"拟合出任何结论"

4. RSF 体系混用（Scofield + Wagner）→ 原子%错误

5. 峰位/化学态指认不对照权威数据库（NIST XPS），凭印象

补充来源（中文，痛点总结）：
- CSDN "XPS数据分析中的四个大坑"（150556637）
- CSDN "XPS数据处理避坑指南"（154469639）

---

## 6. 参考数据库

- **NIST XPS Database**：https://srdata.nist.gov/xps/ —— 结合能权威查询。sagittarius 未抓到正文（WebFetch 在 subagent 里挂了），但这是业界共识的权威库。
- LaShells / XPSgold：商业/社区库，未深入验证。

---

## 7. 待用户定调（用户说"我有一套原则"）

调研到此为止。设计需用户先讲原则，尤其：
1. skill 产物形态（落盘文件 vs 交互 vs 直接出图）
2. 是否复用 sci-draw 的文件契约/Morandi 配色，还是独立
3. 分析判断由谁做（skill 给候选化学态让人选，还是 skill 自己下结论）
4. 边界——哪些不做（深度剖析？成像 XPS？定量由谁负责）
5. 工具链选型（lmfit 自建 vs 封装 pynxtools-xps vs 其他）
