# sci-skills

零件 + 管理层。不卖全家桶。

## 为什么

科研 skill 赛道已经饱和。每家都在卖全流程。大多数不落盘，大多数不互通。

**我们的赌注：不比质量，比交接面。**

我们做小零件——一个 skill 只管一类产物，只认文件不认其他 skill。换了谁的工具都不崩。我们也做管理层——一个项目经理 skill 搭骨架、写契约、把外部产物翻译成下游能消费的格式。用我们的零件也行，用别人的文献检索也行，用自己 Excel 画的图也行。只要产物落盘符合契约，管线就能跑。

**能跟别人配合的零件，比封闭套件活得久。** 这是我们的生存方式，也是唯一的差异化卖点。

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

## 管线

```
claim.md ──────────── 中心契约 (sci-write Step 0)
  │
  ├─→ sci-draw ───── 图 + 图报告 (conclusion 驱动)
  ├─→ sci-write ──── method / results / conclusion (claim 锚定)
  │                    sup-list.md (SI 公园清单，写作中逐条累积)
  ├─→ sci-story ──── introduction (两段漏斗) / discussion (融合 conclusion) /
  │                    abstract / title / keywords
  ├─→ sci-export ─── md→tex + SI 组装 + 交叉引用检测 / tex→docx
  ├─→ sci-polish ─── 直接改 tex，git 即审计
  └─→ sci-submit ─── 选刊 / 封面信 / 被拒转投 / 投稿追踪
```

## 技能清单

| Skill | 做什么 | 人在哪介入 |
|---|---|---|
| [sci-skills-init](skills/sci-skills-init/) | 搭骨架、写契约、审计布局、迁移外部文件 | 每次迁移目的地确认 |
| [sci-draw](skills/sci-draw/) | 投稿级科研数据图 + 结构化图报告 | 面板方案确定后再画 |
| [sci-write](skills/sci-write/) | Method / Results / Conclusion。图义核查。 | claim.md 确认；paper-plan 确认；图义核查 |
| [sci-story](skills/sci-story/) | Introduction (两段漏斗) / Discussion (融合 Conclusion) / Abstract / Title / Keywords。文献搜索。 | Claim 读取确认；每节确认门；自检 |
| [sci-polish](skills/sci-polish/) | 直接润色 tex。git 即审计。AI 文风反模式。 | git diff 审查 |
| [sci-export](skills/sci-export/) | md→tex (草稿 → 正文)。tex→docx (pandoc)。SI 组装 + 交叉引用检测。 | 模板选择确认 |
| [sci-submit](skills/sci-submit/) | 硬约束 → 选刊 → 封面信 → 被拒转投 → 投稿追踪 | 硬约束采集；封面信逐段确认 |

## 哲学一句话

小零件，大契约。不卖全家桶。能跟别人配合的零件比封闭套件活得久。

## 安装

```bash
git clone -b release git@gitcode.com:Joe-zhouman/sci-skills.git
```

| 分支 | 用途 |
|---|---|
| [`release`](https://gitcode.com/Joe-zhouman/sci-skills/-/tree/release) | 干净分发版，安装用这个 |
| [`master`](https://gitcode.com/Joe-zhouman/sci-skills) | 完整开发历史 |

## 开发

每个 skill 均按 [skill-creator-plus](https://github.com/Joe-zhouman/skill-creator-plus) 流程开发。
