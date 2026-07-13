---
name: sci-submit
description: >-
  Scientific manuscript submission campaign manager. Covers the full submission
  lifecycle: reusable metadata, journal selection and ranking, cover letters,
  rejection handling and journal switching, post-submission tracking, and navigating
  hard constraints like advisor demands or tenure requirements. Manually invoke
  this skill when the user says they want to submit a paper (我要投稿), write a
  cover letter, select journals, handle rejection, or track submission status.
  Handles TeX and Markdown output. Not for: response letters to reviewers,
  manuscript polishing (use sci-polish), recommendation letters, or grant proposals.
---

# sci-submit — Submission Campaign Manager

## 第一步：硬性约束——强制前置

**所有后续决策都以硬约束为第一筛选条件。跳过这步直接写 cover letter 等于在真空中做决策。**

用户投文章不是为了投稿——是为了毕业、评职称、满足导师要求、项目结题。但他们不会主动说。在学术等级里，说"导师的目标不现实"等于说自己懒、自己没信心。所以他们习惯了不说。你得让他们说——不要用"硬性约束"这个词，不要扮演中立的助手。去读 `references/conversation-guide.md`，按里面的方式问。

流程：
1. 检查 `sci-skills/sci-submit/hard-constraints.md` 是否存在
2. **不存在** → 读 conversation-guide → 采集 → 写入 `hard-constraints.md`（模板 `references/workflow-constraints.md`）
3. **已存在** → 读取确认

## 核心数据文件

四个文件构成投稿战役的持久状态：

| 文件 | 为什么要有 | 生命周期 |
|---|---|---|
| `hard-constraints.md` | 投文章不是为了投稿——是为了毕业、评职称、满足导师。这些约束决定了你选什么期刊、投递顺序、被拒后坚持还是妥协。写下来，每次决策回来翻一眼，不会跑偏。 | 随处境变化更新 |
| `manuscript-meta.md` | 投稿系统每个 input 框的答案，每个框一块，复制粘贴。外加一份 Cover Letter Cheat Sheet——用关键词和短语列背景钩子和核心发现，AI 读 `writing-tips.md` 帮你写成正式段落。 | 写一次，N 次投稿复用 |
| `submit-history.md` | 投了七八次之后，你记不住第一次投的是哪本、第三次审了多久、第五次的审稿意见说了什么。这个文件帮你记。 | 整个投稿生涯持续更新 |
| `journal-shortlist.md` | 被拒之后最容易犯的错是盲目投下一个。这个文件让你在被拒之前就想好退路，被拒之后直接走下一步。每个期刊旁边存好搜来的该刊论文——写封面信时直接展开，不用重新搜。 | 随被拒和重新评估变化 |

核心理念：**每次投稿系统让你填的东西，90% 都是重复的。** 把这些信息提取一次、存在 `manuscript-meta.md` 里，每次写 cover letter 或填投稿系统时直接调取。

## Startup

每次触发时：

1. 没有 `sci-skills/sci-submit/` → 创建目录
2. **没有 `hard-constraints.md` → 立刻进入硬性约束采集（见上节"第一步"），不得跳过**。这是强制前置步骤。
3. 没有 `manuscript-meta.md` → 进入 **Workflow A**
4. 没有 `submit-history.md` → 创建空模板，询问历史记录
5. 没有 `journal-shortlist.md` → 询问是否需要建立候选列表
6. 读取已有文件，判断当前阶段，选择对应工作流

## 路由表

硬约束已确认后，根据用户意图路由：

| 用户意图 | 工作流 | 细节文件 |
|---|---|---|
| 整理投稿元数据 | **A: Metadata Setup** | `references/workflow-metadata.md` |
| 选期刊 / 比较期刊 / 查分区 | **B: Journal Selection** | `references/workflow-journal-selection.md` |
| 投稿 / 过投稿系统（封面信 + 逐页引导） | **C: Submission** | `references/workflow-cover-letter.md` |
| 被拒 / 改投 / 转投 | **D: Rejection & Switching** | `references/workflow-rejection.md` |
| 投稿后状态 / 催稿 | **E: Post-submission Tracking** | `references/workflow-tracking.md` |
| 收到 proof / 校样校对 | **G: Proof Review** | `references/workflow-proof.md` |
| 约束变化（导师改主意、政策变动等） | 更新 `hard-constraints.md` | `references/workflow-constraints.md` |

## 可用数据源

- **EasyScholar**：`scripts/query-journal.py` 单查，`scripts/query-journals.py` 批量查。实时分区/IF/预警。出问题读 `data/easyscholar-api.md`。
- **中国科协分级目录**：`scripts/search-ratings.py "Nature Communications"` 精确查，`--fuzzy` 模糊，`--field "材料"` 按领域。离线。源 xlsx 在 `data/`，更新后跑 `scripts/convert-xlsx.py`。

## 输出组织

```
project/
├── manuscript/                     ← 正式正文（一等公民，按 v/r 轮次）
│   └── v1/                         ← 当前轮次的稿（tex/figures/ref/）
│       └── tex/main.tex            ← sci-submit 读这里提发现/元数据/打包
└── sci-skills/sci-submit/          ← 投稿产物（本 skill 的家）
    ├── manuscript-meta.md
    ├── hard-constraints.md
    ├── submit-history.md
    ├── journal-shortlist.md
    ├── declarations/               ← 标准声明（COI/Author Contributions/Data Availability）
    └── cover-letter/
        └── <journal-name>-<YYYY-MM-DD>/
            ├── cover-letter.tex
            └── highlights.docx       # Elsevier 需要时生成
```

**正文在 `manuscript/v1/`（或当前轮 rN/），不在 `sci-skills/sci-submit/` 下。** sci-submit **读** `../manuscript/` 提发现/元数据/打包投稿，但**不复制正文进来**——正文是 `manuscript/` 的一等公民，sci-submit 只产投稿产物（cover letter/history/meta/declarations）。多轮修回时读对应轮次（v1 首投、r1 第一轮修回…），轮次管理见 `manuscript/.README.md` 契约。

**`declarations/`**：存那些换期刊也不怎么变的东西——标准声明（Elsevier 的 Conflict of Interest、ACS 的 Author Contributions、Data Availability Statement 等）、作者简介、图文摘要……这些内容本质上来自 `manuscript-meta.md`，第一次投稿时生成一次，之后就复用。它们是**投稿产物**（不是正文），放 `sci-skills/sci-submit/declarations/`。如果用户不是第一次投稿，先问有没有现成文件，分门别类放进来。

**Cover letter**：LaTeX 或 DOCX，二选一，放 `sci-skills/sci-submit/cover-letter/<journal-name>-<YYYY-MM-DD>/`。
- **LaTeX**：首投 `assets/cover-letter-template.tex`（带 logo/单位抬头）或 `assets/cover-letter-plain.tex`（纯文字，无 logo，适合贴文本框或不需要机构抬头的期刊）。修回对应 `assets/cover-letter-revision-template.tex` 或 `assets/cover-letter-revision-plain.tex`。先问用户要不要抬头。
- **DOCX**：用户要 DOCX 或没 LaTeX 环境时用 `scripts/generate-cover-letter.py --type first`（首投）或 `--type revision`（修回）。首投传 `--background --findings --journal-fit --audience`，修回传 `--changes --msid`。Times New Roman 11pt，对齐 LaTeX 版。

**Highlights**：Elsevier 要求单独上传文件。`scripts/generate-cover-letter.py --type highlights` 生成 DOCX。内容来自 `manuscript-meta.md` → Highlights，每条 ≤85 字符。

**GTOC / Graphical Abstract**：sci-submit 不画图，但会提醒你准备。规格参考 `data/gtoc-guide.md`。大多数要求单独上传 TIFF/EPS，Elsevier 标准 5:2 比例 1328×531px 300dpi。

**决策文件**：Markdown，直接放 `sci-skills/sci-submit/` 根下。

## 每次流程结束：收尾

每个工作流完成之后，必须做三件事：

### 1. 扫路径，列清单

跑 `ls -laR sci-skills/sci-submit/ assets/ 2>/dev/null`，把输出整理成一个简短的文件清单，告诉用户"本次变更涉及这些文件"：

```
本次创建/更新的文件：
  sci-skills/sci-submit/hard-constraints.md      ← 新建
  sci-skills/sci-submit/manuscript-meta.md       ← 新建
  sci-skills/sci-submit/cover-letter/nano-research-2026-07-03/cover-letter.tex  ← 新建
  assets/cover-letter.docx            ← 新建
```

如果有文件被修改（不是新建），标注 `← 更新`。让用户一眼看清楚这次做了什么。

### 2. 提醒用户：下次怎么继续

> "下次打开这个项目目录，sci-submit 会读到这些文件，从你上次停下的地方继续。不用重新说一遍。"

让用户知道这些文件是持久的，不是一次性的。

### 3. 建议用 git 记录

先问一句："你这个项目用 git 了吗？"

- **已经在用** → 提醒 commit：
  > "建议现在 `git add` 这些文件然后 commit 一下，以后每次投完改完都能回溯。"

- **没用过 git** → 问要不要帮他初始化：
  > "你还没用 git。要不要我帮你 `git init` 然后做第一次 commit？以后每次改投都能看到完整记录，比手动备份靠谱。"

  如果用户同意：
  1. `git init`
  2. 写一个合适的 `.gitignore`（至少排除编译产物 `*.aux *.log *.out *.bbl *.blg`）
  3. `git add -A && git commit -m "sci-submit: initial submission setup"`

- **不知道 git 是什么** → 简短解释 + 引导安装：
  > "git 是一个版本控制工具——简单说就是给文件拍快照的工具。每次投完commit一下，以后随时能回到任何时间点的状态。装一下？Ubuntu 上一条命令就行：`sudo apt install git`。"

  装完之后按"没用过"的流程处理。

## 边界

**sci-submit 不做这些事**（如果用户需要，引导到对应工具）：

| 需求 | 去哪里 |
|---|---|
| 回复审稿人（point-by-point response） | 明确排除。sci-submit 只写到 cover letter 为止 |
| 手稿润色、翻译、排版 | `sci-polish` |
| 科研数据图 | `sci-draw` |
| 模拟审稿 | `academic-paper-reviewer` |
| 完整论文写作流程 | `academic-research-skills:academic-paper` |
| 推荐信、求职信、基金申请书 | 通用写作，不在此技能范围 |

**常见混淆场景**：
- "帮我写一封回复审稿人的信" → 这不是 cover letter，sci-submit 不做。建议用户找专门的 response-letter 工具。
- "帮我润色这段 cover letter 的语言" → 如果只是语言问题，用 `sci-polish`。如果是内容和论证有问题，sci-submit 处理。
