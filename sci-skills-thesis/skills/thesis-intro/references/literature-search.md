# Literature Search — 论文级引文搜索策略（B3 heuristic + gray zone at gate）

本 skill 在 Step 1 confirmation gate 打开本文件——决定哪些引文走 callback、哪些走 real-DOI 搜索。镜像 sci-story 的 `literature-search.md` 升尺度到 thesis，落实 spec §③（B3 heuristic，gray zone at gate）。

**thesis 与 article 的关键区别**：article 的 introduction 所有引文都是 search 路径（单篇视角，无章可 callback）；thesis 的绪论有 **N 个正文章已存在**——dissect 已在 chN.tex 落地章级 prior work 的 real-DOI placeholder。intro 的引文因此分两路：**callback**（复用 chN.tex）+ **search**（论文级定位）。

---

## The B3 heuristic（NOT a clean two-way split — gray zone at gate）

**目的**：命名 intro 的引文边界——B3 是 **heuristic**（启发式），非 round-1 spec 呈现的 cleaner-than-reality clean two-way split。诚实命名 gray zone。

文献分两路 **AS A HEURISTIC**：

- **章级 prior work** → **callback** from `thesis/tex/chN.tex`：
  每篇小论文自己的 intro 引用、正文章 engages 的 prior work。dissect 已用 real-DOI placeholder 落地——intro **复用不重搜**。这是"章级 callback"路。
- **论文级 field positioning** → **real-DOI search**：
  umbrella 的领域背景、统一框架的理论根源、框住主线的跨章研究现状——**任何单章都不单独携带**的论文级定位。走本文件下面的搜索优先级。这是"论文级 search"路。
- **gray zone** → **author decides at the confirmation gate**：
  一个 citation 若同时 load-bearing for **both**——一个章的 prior work **和** 论文级 framework positioning。典型例子：**统一框架的理论根源**——常被各章 cite（章级 prior work）又框住主线（论文级 positioning）。归 callback 还是 search？**无 clean decision procedure**。规则"supplement what chapters don't carry" 是 circular——"chapters carry 什么" IS the gray zone。**confirmation gate 是裁决点**——作者在 gate 上判断该 citation 是章级 callback 还是论文级 search。

**诚实命名（aquarius §③ finding，round-2 修）**：

- round-1 spec 呈现 B3 为 clean two-way split 是 overclaim——gray zone 无 clean decision procedure。
- **修正**：B3 是 **heuristic**，非 clean split。gray zone 的 decision procedure 是 confirmation gate 的 author judgment。诚实命名 boundary 是 judgment（heuristic），gate 是裁决点。
- **不要 present B3 为 cleaner than reality**——gray zone 是真的，gate 裁决是真的，两者都诚实说。

---

## Search priority（mirror sci-story，thesis-scaled）

**目的**：论文级 search 路的搜索优先级。镜像 sci-story 的 `literature-search.md`，thesis 尺度。

按以下顺序，上一层跑通就不走下一条：

1. **学术搜索 MCP（academic toolset）** → 有就先用。`search_papers`（返回带 `jcr_quartile`/`cas_quartile`/`impact_factor` 的结构化结果，可按 `min_jcr_quartile` 预筛）；已知 DOI/PMID/arXiv 查详情用 `paper_details`；查期刊档次用 `journal_ranking`。这是首选——比通用搜索更结构化、可预筛分区。
2. **用户渠道（Zotero / WoS / AI 产品）** → MCP 搜不到或质量不够时：
   - **Zotero**：先看能不能直接读（Better BibTeX 导出文件在项目里）；读不到 → 引导 author 导出。
   - **Web of Science**：生成专业 WoS Advanced Search query（全面版 + 简略版给 author 选），author 去搜、把结果给你。
   - **主流 AI 产品**：DeepSeek、Kimi、秘塔、豆包、Qwen（提醒：`https://chat.qwen.ai/`）；GPT、Grok、Gemini、Perplexity。给一句提示词："查找权威文献证明以下观点：[你要引文献支撑的具体 claim]"。author 把结果贴给你，你来核实。
3. **通用搜索** → author 说"你来搜，我不参与"时：`mcp__search__searxng`（SearXNG）+ 其他通用搜索工具。

**验证标准（所有渠道统一）**：

- 真实 DOI 必须能查到 → 按 DOI 反查期刊/分区/引用数。
- 无 DOI 但有 arXiv ID 且引用少 → 不采纳（除非 arXiv 已被正式期刊接收且有 DOI）。
- 无 DOI、无 arXiv、只有标题 → 搜索验证是否存在、哪个期刊。搜不到 → 不采纳。
- **peer-reviewed 正经期刊**，不是 arXiv 预印本冒充、不是会议摘要冒充。

### 输出：统一为 BibTeX

所有渠道搜到的文献，最终统一为 BibTeX 格式落盘。方便 author 通过 Zotero/JabRef/Mendeley 直接导入。给 author 一个 BibTeX 片段 + 一个简单的待确认清单：

```bibtex
@article{smith2024,
  title   = {Title goes here},
  author  = {Smith, J. and Jones, A.},
  journal = {Nature},
  volume  = {628},
  pages   = {123--130},
  year    = {2024},
  doi     = {10.1038/s41586-024-00001-x},
}
```

```markdown
- [ ] Smith 2024 Nature — Layer 1 OK
- [ ] Jones 2023 Science — Layer 1 OK
- [ ] Wang 2022 ACS Nano — Layer 3 OK
```

BibTeX 能填多少填多少——**DOI 和 title 是底线**。author 确认后在 Zotero 里一键导入。**最终插入 Zotero 永远由 author 完成**——agent 不生成 `.bib` 条目、不替 author 按插入键。

---

## Citation support-strength scoring（mirror sci-story）

**目的**：搜到的每篇文献在放进绪论正文之前，先打一个支撑等级。不是"搜到即引用"——搜到的只是候选，打分了才决定用不用、怎么用。镜像 sci-story。

| 等级 | 含义 | 引用策略 |
|---|---|---|
| **strong** | 直接验证了同一个关系/机制/方法，结果支撑你的 claim | 绪论核心段的主力引用（论文级 framework positioning 的主干） |
| **partial** | 支撑了部分，或更窄的条件下成立 | 可以引，但要加限定——"虽然 X 在 Y 条件下成立，本论文扩展到 Z" |
| **background** | 支撑的是领域背景，不是你的具体 claim | 只进 Layer 1-2（大背景、小背景），不进 Layer 3（prior work） |
| **limiting** | 和你的 claim 冲突或缩小了它的范围 | 绪论的研究现状段正面回应——不要假装没看到（"Although X showed Y, ...") |
| **metadata-only** | 标题相关，但没读到摘要/全文 | **不引。** 强制读摘要/全文之后重新打分。读完还是 metadata-only → 不引 |

**partial 和 metadata-only 不能放进核心 argument**——绪论的 thesis 主线 claim 不挂在 partial 证据上。strong 和 background 可以放心用。

打分不需要展示给 author——是你在落盘之前自己的判断。

---

## Layer-by-layer requirements（escalated to thesis scale）

**目的**：绪论的两阶段漏斗里，每层的引文要求。镜像 sci-story 的 layer 要求，thesis 尺度。完整漏斗结构见 `references/introduction-guide.md`——这里只讲引文密度。

### Layer 1：大背景（Stage 1 开篇）

**至少三篇独立来源从不同角度合力支撑一个 claim**——"AI 导致算力暴涨"不能只靠一篇综述，需要算力需求、功耗上升、硬件现状各一篇独立出处。Q1 / 一区二区优先。一个具体数字锚定可信度。

**thesis 尺度**：大背景框住**整篇论文**的领域，不是单篇 article 的领域——要选能跨 N 章共领域的 umbrella 文献。

### Layer 2：小背景 + 现状（Stage 1 + Stage 2）

筛选标准：是否代表当前最佳实践？Q1 / 一区二区优先。Q2 但高度相关的可以引但不要为主。

**thesis 尺度**：Stage 2 的小背景按问题聚类（不是按时序）——每个问题簇有引文支撑。同一篇论文可以出现在多个问题下（因为它确实可以同时有两个局限）。

### Layer 3：Prior work（Stage 1 + Stage 2）

相关性 > 期刊等级。审稿人会追问的必须引。但要是 peer-reviewed 正经期刊，不是 arXiv 预印本或会议摘要冒充。

**thesis 尺度（关键）**：Layer 3 的 prior work 分两路——
- **章级 prior work** → **callback** from chN.tex（dissect 已落地，intro 不重搜）。这些是每篇小论文自己 engages 的前人工作。
- **论文级 prior work** → **real-DOI search**。这些是框住主线、跨章共领域的 prior work，单章不携带。

**gray zone**：统一框架的理论根源常既是某章的 prior work（章级 callback）又是论文级 positioning（search）→ 作者在 gate 裁决。见 B3 heuristic 节。

### Layer 4 & 5：Gap + Present study

**不引新文献**。Gap 是从前面 prior work 推出的断层；Present study 是本论文的框架级预览。

---

## 搜索纪律

1. **搜完再写**。不猜文献。搜不到标 `[DOI needed]`，不空占位。
2. **读了摘要再引**。只看标题引 = 等着审稿人挑出来。
3. **引文数当 tie-breaker，不当支撑证据**。高引 ≠ 结论正确。低引但方法严谨、数据扎实的照引。
4. **搜索结果同质化**——同一论文多库出现 ≠ 多篇独立论文。算一次。
5. **搜不到不强搜**。如实说 "few studies have addressed X"，不要编。
6. **Precision over volume**。每个 layer 3-8 篇是健康的。20 篇是暴饮暴食——读者记不住，审稿人觉得你是在炫耀检索能力而不是在论证。
7. **章级 callback 不重搜**——dissect 已用 real-DOI 落地，intro 复用即。重搜 = 重复 cite + 浪费。

---

## What this reference is NOT

**这是章级 prior work 的搜索指南吗？不是。** 章级 prior work 走 callback from `thesis/tex/chN.tex`——dissect 已用 real-DOI placeholder 落地。intro **复用不重搜**。本文件只指导**论文级 field positioning** 的 real-DOI 搜索。

**这替代了章级 prior work 吗？没有。** 本文件补充论文级定位——单章不单独携带的 umbrella 领域背景、统一框架理论根源、跨章研究现状。这是家族 spec 的**补**语义（spec §③）：intro 补 chapters 不 individually carry 的部分，不替 chapters 做它们已做的。

**B3 是 clean two-way split 吗？不是。** B3 是 **heuristic**——gray zone 无 clean decision procedure，confirmation gate 是裁决点。round-1 spec 呈现的 clean split 是 overclaim（aquarius §③ finding），本文件诚实命名 gray zone。

**check_intro.py 查引文质量吗？不查。** check_intro.py 是 near-trivial consistency 门（gap-map.md 字段 + filled-by cross-ref chapter-map.md + ch0-intro.tex 存在），**不查引文 depth/grounding**（spec §①）。引文是否真支撑 claim、是否 peer-reviewed、是否 gray zone callback vs search——都是作者 gate judgment + prose eval，非脚本。
