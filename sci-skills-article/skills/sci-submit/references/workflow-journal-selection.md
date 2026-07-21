# Workflow B: Journal Selection

> 前提：`hard-constraints.md` 和 `manuscript-meta.md` 已存在。如果不存在，先走对应 workflow 再回来。

## 前置读取

1. **`sci-skills/sci-submit/hard-constraints.md`** → 白名单、黑名单、分区/IF 下限、截止时间 → 第一筛选条件
2. **`sci-skills/sci-submit/manuscript-meta.md`** → 标题、摘要、Keywords → 搜索关键词
3. **`sci-skills/sci-write/claim.md`**（有就读）→ Journal ambition 预估 → 给选刊一个起点（"你觉得这篇够 Nature 吗"——数据驱动阶段已经做过文献对标了）
4. **`sci-skills/sci-submit/journal-shortlist.md`**（如已有）→ 当前候选状态
5. **`sci-skills/sci-submit/submit-history.md`**（如已有）→ 哪些期刊已经投过了、结果如何
6. **`manuscript-meta.md` → Cover Letter Cheat Sheet** → 用户列的要点（背景钩子 + 核心发现）

## 两种入口

### 入口 1：用户有明确目标期刊

用户说"我想投 Nature Energy"→ 不用搜索候选，直接评估这一个期刊。

1. **查数据**：EasyScholar API 查分区/IF/预警 + `data/journal-ratings.json` 查中国科协分级
2. **过约束**：拿 hard-constraints.md 逐条对照：
   - 在白名单里？→ 如果不在但约束要求"只投某几个期刊"，提醒
   - 在黑名单里？→ 立刻提醒冲突
   - 分区/IF 满足硬指标？→ 如果不够，告诉用户差多少
   - 审稿周期在 deadline 前来得及吗？→ 如果来不及，用数据说话
3. **scope 匹配度**：搜索该期刊近期有没有发表过类似主题的论文。有 → 写入 `journal-shortlist.md` 该刊条目的 Cover Letter 材料（供写封面信时用）
4. **给结论**：匹配 / 勉强 / 不匹配，附数据。不匹配时走入口 2。

### 入口 2：用户需要推荐

用户说"帮我看看有哪些期刊可以投"→ 生成候选列表。

## 工具

**EasyScholar（实时）**：

```bash
python3 scripts/query-journal.py "Nature Energy"                # 查一个
python3 scripts/query-journals.py "A" "B" "C" --compact         # 批量查
python3 scripts/query-journals.py --file journals.txt --compact  # 从文件读
```

**中国科协分级目录（离线）**：

```bash
python3 scripts/search-ratings.py "Nature Communications"        # 精确匹配
python3 scripts/search-ratings.py "nano" --fuzzy                 # 模糊匹配
python3 scripts/search-ratings.py --field "材料"                  # 按领域浏览
```

> 两个脚本都在 `scripts/` 下。出问题读 `data/easyscholar-api.md`。

> **源 xlsx**：`data/高质量科技期刊分级目录速查表.xlsx`（用 Excel 直接打开看，也可以编辑更新）。JSON 是用 `scripts/convert-xlsx.py` 从它预转换的——更新 xlsx 后跑一次重新生成。

按以下顺序找候选期刊：

1. **约束展开**：`hard-constraints.md` 的白名单就是第一批候选。如果有"一区 Top"约束 → 用 EasyScholar 查该分区所有期刊
2. **引用链反推**：读手稿的 Reference，看引用最多的是哪些期刊。被引最多的那几个期刊就是你的自然受众
3. **关键词搜索**：用 `manuscript-meta.md` 的 Keywords + Abstract 中的核心术语，搜索近期发表了相关主题论文的期刊
4. **本地分级目录**：从 `data/journal-ratings.json` 按领域筛选 T1/T2 期刊
5. **排除已投过的**：`submit-history.md` 里已经出局的不要再推荐（除非用户明确说再投一次）

## 评分

每个候选期刊过一个简单的四维评估（不要做加权打分——那是自己骗自己）：

| 维度 | 问题 |
|---|---|
| **硬约束** | 满足白名单/分区/IF 要求吗？不满足直接排除。 |
| **scope 匹配** | 这个期刊发过类似主题的论文吗？找到 2-3 篇就是强匹配，0 篇就是弱匹配。 |
| **水平匹配** | 你的工作和这个期刊近期发表的同类论文相比，量级差多少？诚实说——不要安慰剂。 |
| **速度** | desk decision 多快？首轮审稿多久？截止时间前来得及吗？ |

## 生成 `journal-shortlist.md`

不要用 Markdown 表格——表格在终端里渲染稀烂。用层级结构，每个期刊一个 `###` 块。

```markdown
# Journal Shortlist — [manuscript short title]

> 更新日期：YYYY-MM-DD
> 硬约束摘要：[一行概括 hard-constraints.md]

## Tier 1 — Hard Targets（硬性要求 / 冲刺）

### [Journal Name]

**数据**
- 分区：中科院升级版 [X]区 [Top/非Top] | JCR [Q1/Q2]
- IF：[XX.X]（五年 [XX.X]）
- 中国科协：[T1/T2/T3] — [领域名称]
- 预警：[有/无]
- 审稿周期：desk ~[X]周 | 首轮 ~[X]周

**适配**
- scope 匹配：[强/中/弱]
- 水平匹配：[该刊同类论文 vs 你的工作]

**Cover Letter 材料**（选刊时搜 2-4 篇，写 cover letter 时展开）
- [[Author] et al. ([Year])](https://doi.org/...): [一句话 — 你的工作怎么延续这条线]
- [[Author] et al. ([Year])](https://doi.org/...): [一句话]
- ...

**策略**：[为什么投、什么时候投、预期]

**状态**：[待投 / 已投 YYYY-MM-DD / 被拒 YYYY-MM-DD — desk / after review]

### [Journal Name]
...

## Tier 2 — Match（匹配）

...

## Tier 3 — Safety（保底）

...

## Ruled Out

| Journal | Date | Result | Note |
|---|---|---|---|
| [Name] | YYYY-MM-DD | Desk reject | — |
```

## 生成后

1. 把选定的目标期刊写入 `submit-history.md`（如果还没投，状态写"待投"）
2. 如果用户选中了一个期刊准备投 → 回到 SKILL.md 路由表，走 Workflow C（Submission）
3. Cover Letter 的 journal-fit 段从 shortlist 该刊条目下的已搜论文展开，背景钩子和核心发现从 manuscript-meta.md 的 Cheat Sheet 取
