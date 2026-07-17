# Literature Search — 引文搜索策略

Introduction 和 Discussion 的引用必须来自真实文献。不编文献、不空占位。

## 搜索优先级

按以下顺序，上一层跑通就不走下一条：

1. **已有学术搜索 MCP / skill** → 有就先用。搜到靠谱文献直接用。
2. **搜不到或质量不够** → 停下来问用户。搜了但用户不想选的 → 跳过不要硬塞。
3. **用户说"你来搜，我不参与"** → 通用搜索。

## 用户渠道

### Zotero

先看能不能直接读——Zotero 本地数据库或 Better BibTeX 导出的文件在项目里吗？能读到就直接解析。

读不到 → 引导导出：

> "Zotero 里装 Better BibTeX 插件了吗？装了的话：选中文献 → 右键 → Better BibTeX → Export → 选 BibTeX 格式 → 存到项目里。没装的话：Zotero → 文件 → 导出文献库 → 选 BibTeX 格式。"

### Web of Science

你生成一组专业的 WoS Advanced Search query，用户去搜、把结果给你。

用户路径：

> https://webofscience.clarivate.cn/wos/woscc/basic-search → Advanced Search → QUERY BUILDER → Query Preview → 粘贴 query → Search → 选中文献 → 导出

**Query 拆两版：** 全面版（覆盖面大，噪声多但不会漏）和简略版（精准但可能漏边缘领域）。给用户选。

示例——搜"近几年 2D 材料的综述"：

```
全面版：
TS=(
  ("two-dimensional" OR "2D" OR "monolayer*" OR "bilayer*" OR "few-layer*" OR "atomically thin" OR "single-layer*" OR "van der Waals")
  AND
  ("material*" OR "crystal*" OR "nanosheet*" OR "nanofilm*" OR "heterostructure*")
  AND
  (
    graphene OR "graphene oxide" OR "reduced graphene oxide" OR
    "transition metal dichalcogenide*" OR TMD* OR TMDC* OR
    (MoS2 OR MoSe2 OR WS2 OR WSe2 OR MoTe2 OR "transition metal sulfide*" OR "transition metal selenide*") OR
    "hexagonal boron nitride" OR "h-BN" OR "boron nitride nanosheet*" OR
    MXene* OR "MAX phase" OR
    phosphorene OR "black phosphorus" OR
    (silicene OR germanene OR stanene OR borophene OR antimonene OR bismuthene OR tellurene) OR
    graphyne OR graphdiyne OR
    ("topological insulator*" AND (Bi2Se3 OR Bi2Te3 OR Sb2Te3)) OR
    ("2D oxide*" OR "transition metal oxide*" AND (TiO2 OR MoO3 OR MnO2 OR ZnO)) OR
    "Janus monolayer*" OR "Janus TMD*"
  )
)
AND DT=(Review)

简略版：
TS=(("two-dimensional material*" OR "2D material*" OR "atomically thin" OR "van der Waals material*" OR "layered material*") AND ("graphene" OR "transition metal dichalcogenide*" OR TMD* OR "MXene*" OR "hexagonal boron nitride" OR "h-BN" OR "black phosphorus" OR phosphorene OR silicene OR germanene OR stanene OR borophene OR "transition metal carbide*" OR "2D oxide*" OR "Janus structure*"))
AND DT=(Review)
```

### 主流 AI 产品

推荐以下产品，给用户选：

- **国内**：DeepSeek、Kimi、秘塔、豆包（思考/专家模式）、Qwen（注意提醒用户：是 https://chat.qwen.ai/，不是别的入口）
- **国外**：GPT、Grok、Gemini、Perplexity

给用户一句提示词：

> 查找权威文献证明以下观点： [你要引文献支撑的具体 claim]

用户把 AI 返回的结果贴给你。你来核实，期间可以用通用搜索辅助。

**验证标准：**
- 真实 DOI 必须能查到 → 按 DOI 反查期刊/分区/引用数。
- 无 DOI 但有 arXiv ID 且引用少 → 不采纳（除非 arXiv 已被正式期刊接收且有 DOI）。
- 无 DOI、无 arXiv、只有标题 → 搜索验证是否存在、哪个期刊。搜不到 → 不采纳。

## 输出：文献待填清单

不用 BibTeX——BibTeX 无 DOI 字段、agent 无法辨识、不能完美继承。

搜完/人给完结果后，给用户一个最简单的列表，不预填——用户能填一条就算成功：

```markdown
- [ ] 标题 / 作者. 期刊, 年 / DOI / 用于 Intro 哪一层？
- [ ] 标题 / 作者. 期刊, 年 / DOI / 用于 Intro 哪一层？
- [ ] 标题 / 作者. 期刊, 年 / DOI / 用于 Intro 哪一层？
```

## 通用搜索

优先级 3——学术搜索 MCP → 文献库 MCP → `WebSearch` 及其他通用搜索工具。

搜到的文献同样走验证：真实 DOI、正经期刊、不是 arXiv 预印本冒充。

## 各层引文要求

### Layer 1：大背景

至少三篇独立来源从不同角度合力支撑。Q1 / 一区优先。

### Layer 2：小背景 + 现状

筛选标准：是否代表当前最佳实践？Q1 / 一区优先。

### Layer 3：Prior work

相关性 > 期刊等级。审稿人会追问的必须引。但要 peer-reviewed 正经期刊。

### Layer 4 & 5：Gap + Present study

不引新文献。

## 搜索纪律

1. **搜完再写。** 不猜文献。搜不到标 `[DOI needed]`。
2. **读了摘要再引。**
3. **搜索结果同质化**——同一论文多库出现 ≠ 多篇独立论文。算一次。
4. **搜不到不强搜。** 如实说 "few studies have addressed X"，不要编。
