# sci-skills

零件 + 管理层。不卖全家桶。

## 为什么

科研 skill 赛道已经饱和。每家都在卖全流程。大多数不落盘，大多数不互通。

**我们的赌注：不比质量，比交接面。**

我们做小零件——一个 skill 只管一类产物，只认文件不认其他 skill。换了谁的工具都不崩。我们也做管理层——一个项目经理 skill 搭骨架、写契约、把外部产物翻译成下游能消费的格式。用我们的零件也行，用别人的文献检索也行，用自己 Excel 画的图也行。只要产物落盘符合契约，管线就能跑。

**能跟别人配合的零件，比封闭套件活得久。** 这是我们的生存方式，也是唯一的差异化卖点。

## 这套 skill 服务于谁

大多数 research-skills 假设了一个优越的默认用户：好学校、好数据、好设备、导师把路指好了。对那种作者，"诚实做科研 + 呈现得好"就是最优策略——他们的工作本身够硬，诚实就足以把它送到位。所以他们的 skill 可以把"诚实"当最高原则。

这套 family **不是**为那个默认用户写的。它服务于处境不优越的作者——学校一般，资源也一般，很多工作只能做到这个水平，因为条件就那样。这不是态度问题，是现实。在这个现实下，"只管诚实"不够：一个诚实地呈现出来的"一般"稿件，会被用强工作的标准去衡量，然后死掉。

所以每个 skill 的目标是**约束下中稿**——在诚实的硬底线之内，用一切合法自由度，给"一般"的工作争取它该有的位置。不是造假（底线是硬的：不编数据、不假引、不"没做说做了"）。但底线之上：**框定是技艺，不是罪过。**
- `sci-submit` 由硬约束（毕业、职称、导师要求）驱动——中稿是显式目标，不是副产品。
- `xps` 把校准 / 基线 / 峰约束当合法的叙事旋钮——同一份数据，旋钮一拧就是另一个讲法。
- `sci-respond` 带 7 种合法框定手法（收窄 claim scope / 弱化 limitation / 引导到 SI / 利用审稿人的误解等等）——Response 的目的是中稿，诚实是地板，不是天花板。

这是黄药师的选择，不是全真教的选择——不是道德差异，是处境差异。名门正派有资本让"实力说话"；桃花岛服务没有退路的人，所以教技艺。武功不差，只是为不同的学生造的。很多 skill 作者避谈这一点；我们摊开讲，因为假装默认用户优越，对真正需要这些工具的人毫无帮助。

## 架构

### Skill 认文件不认 skill

每个 skill 只读写 `sci-skills/` 下的文件。不 import 其他 skill 的代码，不假设其他 skill 存在。换生产者留契约，什么都不用改。任何 agent、任何工具、任何人都能往目录里写，只要按 `CONTRACT.md` 来。

### 以 claim 为锚，不以模板为纲

一份 `claim.md` 贯穿始终。sci-write 建立它——数据校对、文献对标。sci-story 读它写 Introduction 和 Discussion。sci-polish 每处编辑都对回它。sci-submit 从它读期刊野心。每张图是子 claim，每句话服务一句论证。一切围绕 claim。

### 三重解耦

| 层 | 做什么 | 例子 |
|---|---|---|
| 执行 skill | 产出一类制品 | sci-draw → 图；sci-write → method/results/conclusion |
| 文件契约 | 通用交接面 | 每目录一个 `CONTRACT.md`——谁产出、谁消费，只看契约 |
| 项目经理 | 搭台、翻译、巡检 | sci-skills-init 建骨架、迁外部产物、审计落盘 |

### 人介入在硬门

claim 校准。paper-plan 确认。图义核查。每节确认门。自检后才给人看。agent 提案，人拍板。绝不吹嘘全自动——真正的科研从来不是全自动的。

### 场景分治，不一锅端

一个场景一套 skill。场景 A（英文期刊投稿）是今天交付的。场景 B（中文学位论文）、场景 C（基金申请书）是独立场景，各有各的零件和契约。skill 不跨场景——文件契约哲学是唯一的共享 DNA。

### 顶刊当底线，不按目标期刊分级

写到 Nature/Science 的标准，投哪无所谓。求其上者得其中。Introduction 是两段漏斗（领域级 gap → 研究级 gap）。Discussion 第一段融合 Conclusion——几乎所有期刊的公因数。

### 不会干的活外包

自己做零件，不做的外包——但要求外包产物落盘符合契约。sci-skills-init 把外部产物翻译成下游能消费的格式。整个家族是科研产物的 CI/CD 层。

## 技能清单

| Skill | 做什么 | 人在哪介入 |
|---|---|---|
| [article-init](sci-skills/skills/article-init/) | 搭骨架、写契约、审计布局、迁移外部文件 | 每次迁移目的地确认 |
| [sci-draw](sci-skills/skills/sci-draw/) | 投稿级科研数据图 + 结构化图报告 | 面板方案确定后再画 |
| [sci-write](sci-skills-article/skills/sci-write/) | Method / Results / Conclusion（+ SI 作为副产品），直接写成 tex。图义核查。 | claim.md 确认；paper-plan 确认；图义核查 |
| [sci-story](sci-skills-article/skills/sci-story/) | Introduction (两段漏斗) / Discussion (融合 Conclusion) / Abstract / Title / Keywords。文献搜索。 | Claim 读取确认；每节确认门；自检 |
| [sci-polish](sci-skills-article/skills/sci-polish/) | 直接润色 tex。git 即审计。AI 文风反模式。 | git diff 审查 |
| [sci-typeset](sci-skills-article/skills/sci-typeset/) | 在自家模板上做 LaTeX 排版——修可读性问题（孤页/标题落单/表太大等）+ 编译 PDF | PDF 视觉审查 |
| [sci-export](sci-skills-article/skills/sci-export/) | 把定稿 tex 搬进目标期刊模板（可选，决定 float 策略）；tex→docx（可选）。 | 模板选择 / float 策略确认 |
| [sci-respond](sci-skills-article/skills/sci-respond/) | 修改轮的 Response-to-Reviewers 信（逐条回应）——tex→PDF，诚实底线之上的框定自由度 | 每条 issue 的策略在 checkpoint 锁定；框定姿态由作者拍板 |
| [sci-submit](sci-skills-article/skills/sci-submit/) | 硬约束 → 选刊 → 封面信 → 被拒转投 → 投稿追踪 | 硬约束采集；封面信逐段确认 |

## 管线

```
claim.md ──────────── 中心契约 (sci-write Step 0)
  │
  ├─→ sci-draw ───── 图 + 图报告 (conclusion 驱动)
  ├─→ sci-write ──── method / results / conclusion / SI (tex-direct，claim 锚定)
  ├─→ sci-story ──── introduction / discussion / abstract / title / keywords
  ├─→ sci-polish ─── 直接改 tex，git 即审计
  ├─→ sci-typeset ── 在自家模板上做可读性排版 + 编译 PDF
  ├─→ sci-export ─── (可选) 搬进期刊模板 / tex→docx
  └─→ sci-submit ─── 选刊 / 封面信 / 被拒转投 / 投稿追踪
                     ↓ 审稿意见回来之后
  rN/ ──→ sci-respond ── response-to-reviewers 信 (tex→PDF，诚实底线之上的框定)
          sci-revise ──── 按锁定的 issue-ledger 做外科手术式正文修改
```

## 哲学一句话

小零件，大契约。不卖全家桶。能跟别人配合的零件比封闭套件活得久。

## 安装

| 分支 | 是什么 | 克隆命令 |
|---|---|---|
| [`v1`](https://gitcode.com/Joe-zhouman/sci-skills/-/tree/v1) | **稳定版** — 只修 bug，不破坏现有功能 | `git clone -b v1 git@gitcode.com:Joe-zhouman/sci-skills.git` |
| [`master`](https://gitcode.com/Joe-zhouman/sci-skills) | 尝鲜版 — 最新功能，可能变动 | `git clone -b master git@gitcode.com:Joe-zhouman/sci-skills.git` |

装好后运行 `bash install.sh`（把三个 skill 家族 symlink 到 `~/.claude/skills/`，并配置 Python 环境）。

**xps 不是谁都要用的，没需要可以不安装。** 这条规则对所有环境一样，不预设必须是 Claude Code：

- 没有 XPS 需求 → 跳过 `sci-skills-analysis` 家族，其余功能（写作、绘图、投稿）不受影响
- XPS 专属依赖（`lmfit`、`lmfitxps`、`pyarrow`）是 `pyproject.toml` 里的可选 `xps` extra：`uv sync` 只装共享基础依赖，`uv sync --extra xps` 才带上 XPS
- Claude Code 环境可一步完成：`SKIP_FAMILIES=sci-skills-analysis bash install.sh`（家族 symlink 和 `xps` extra 一起跳过）
- 其他环境：不装 `xps` extra、忽略 `sci-skills-analysis/` 目录，效果相同

## 开发

每个 skill 均按 [skill-creator-plus](https://github.com/Joe-zhouman/skill-creator-plus) 流程开发。
