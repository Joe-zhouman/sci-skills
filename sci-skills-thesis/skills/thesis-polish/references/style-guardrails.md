# Style guardrails — 机械护栏（overclaim / 诚信线 / 填充短语 / 数字与单位）

Step 2 语体层的机械护栏——结构与三元修完之后逐项过的检查单。它们 refine prose，不推翻策略（诊断次序见 `references/polish-strategy.md` §②）。AI 痕迹的语体判据（三判据 / 翻译腔 / 句式卫生）不在本文件——`references/chinese-register.md`；可用措辞在 `references/phrasebank-zh.md`。

> **Provenance（内化来源，spec §⑦）**：`sci-skills-article/skills/sci-polish/references/style-guardrails.md` 中文版。**移植**：siunitx 规则**逐字**（LaTeX 单位纪律对中文论文同样成立）/ integrity rules / overclaim 表（中文化）/ 填充短语（throat-clearing 的中文对应）。**丢弃**：英文专用项——articles 节、contractions、British spelling、Nature 图注字数与标题字数上限。burstiness / rule-of-three / uniform paragraphs 已在 `references/chinese-register.md` §⑥（AI 初稿特征），不在本文件重复。

---

## ① Overclaim 中文表

除非证据异常强、范围收得很紧，见到即降档（措辞强度对表见 `references/phrasebank-zh.md` §①）：

| 过强 | 降档写法 |
|---|---|
| 证明了 | 表明了 / 证实了（有对照 + 统计时）/ 验证了 |
| 首次提出 / 首次发现 | 据我们所知，尚未见……的报道 |
| 显著提升 | 量化：提升了 X%（附统计检验） |
| 极大 / 深刻 / 全新 | 删，或落具体（具体到指标与幅度） |
| 解决了……问题 | 缓解了 / 改进了（按证据强度选） |
| 广泛适用于 | 适用于……（列条件） |
| 最优 / 国际领先 | 在……基准上优于……（同数据同指标） |
| 国内外首次 / 填补空白 | 据我们所知……（空白表述挂具体检索范围） |

配套：**降档是常规动作，升档几乎从不是**——polish 把过强措辞降到位，不把弱措辞抬上去（抬上去 = 造假主张）。

降档的样子：

- 改写前：本文方法显著优于现有方法，极大地提升了检测效率。
- 改写后：在两个数据集上，本文方法 mAP 为 94.1% 与 91.7%，高于最强基线 2.3 与 3.0 个百分点（表 4，p < 0.05）。

## ② 数字与单位（siunitx 逐字移植）

所有带单位的量必须用 `siunitx`——不写裸文本。中文正文与 siunitx 共存（xeCJK 下 `\qty` 正常工作）；单位符号用正体西文，不写"25 厘米"式混排。

```latex
\usepackage{siunitx}
\sisetup{
  mode = text,
  detect-all,
  input-decimal-markers = {.},
  group-digits = integer,
  group-four-digits = true,
  inter-unit-product = \,,         % thin space, not \cdot
  per-mode = reciprocal,           % m·s⁻¹, not fraction
  exponent-product = \times,
  input-exponent-markers = {e},
  uncertainty-mode = separate,
  range-units = single,
}

% OK:
\qty{25}{\cm}
\qty{3.2e5}{\J\per\mol\per\K}   % → J·mol⁻¹·K⁻¹
\qty{37.0 +- 0.5}{\celsius}
\ang{90}

% Wrong:
25 cm, 3.2 s, 90°, 25cm
```

**Key rules**: per-mode = reciprocal (negative exponent), inter-unit-product = thin space (no `\cdot`), scientific notation with `\times`.

markdown 阶段（无 LaTeX 可用）的单位写法记进 `sci-skills/thesis-terminology-ledger.md`（同一单位同一写法，如 `25 mL` / `400 ℃`），下次编译统一转 siunitx。

## ③ 诚信线

- **不改数据 / 数字**：typo 修正也须作者确认（Step 4 review 面上过目）。
- **不编引用、不升格引用**：原文说"提示"，不引成"证明"（引用照抄，SKILL.md pervasive discipline）。
- **不把关联写成因果**："X 与 Y 相关"不自动变"X 导致 Y"（三元失效表，`references/polish-strategy.md` §③）。
- **不夸大适用范围**：boundary 限定语（"在本实验条件下""就所测样本而言"）补在 claim 旁。

关联写成因果的样子：

- 改写前：两参数呈显著负相关（r = -0.82），说明前一参数抑制了后者。
- 改写后（降档 + 指明待验）：两参数呈显著负相关（r = -0.82，p < 0.01）；与"抑制"解释一致的机理尚待控制实验检验。

AI 边界：语言控制可以，科学造假不行。**允许**——语法与清晰度、重组与降档、术语校对；**不允许**——编造引用或数据、把猜想写成事实的机理、无支撑的新颖性主张。

## ④ 填充短语表（中文）

| 填充 | 处理 |
|---|---|
| 值得注意的是 | 直接说后半句（连接 / 填充的功能判据见 `references/chinese-register.md` §①） |
| 需要指出的是 | 删 |
| 众所周知 | 删，或给引用 |
| 在一定程度上 | 量化（多大程度），或删 |
| 进行了……的研究 | 研究了 |
| 对……进行了分析 | 分析了…… |
| 不言而喻 / 显而易见 | 删（真显然不必说；不显然这是空转） |
| 可以说 | 删，或直接说 |
| 随着……的快速发展 | 删（时间戳套话，直接进问题） |

另：宣告动作而不做动作的句子（"本节将讨论……""下面我们对……进行分析"）→ 直接做。例外：绪论的章安排 roadmap 句（"第 2 章建立……"）是学位论文惯例，保留。

## ⑤ 数字规范（中文数字 vs 阿拉伯数字）

- **正文计量、统计、编号用阿拉伯数字**：25 mL、3 组样本、提升 12%、表 3、图 5、式 (2)；章节编号按 `template-spec.md` 模板惯例。
- **习语与约数用中文数字**："三种方法""几十次""十余年"——语感惯例，不硬转。
- 一句话内不混用两套（"3 种方法中的两种"→ 统一为一套）。
- 单位前的数字一律阿拉伯数字并走 §② 的 siunitx。

对错对照：

- 对：3 组样本、25 mL、第 2 章、表 3；"三种方法"（习语）、"十余年"（约数）。
- 错：三组样本、25 毫升、"3 种方法中的两种"（一句话混两套）。
