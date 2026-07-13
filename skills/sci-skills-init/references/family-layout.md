# Family layout — sci-skills 家族布局总契约

这份文件是 sci-skills 家族的**布局总契约**。它定义顶层结构、各子目录的角色、
以及"目录引导文件 = 目录级接口契约"这条核心原则。

## 顶层结构

```
<project-root>/sci-skills/        ← 家族 namespace，固定名，有辨识度
  README.md                       ← 家族自述（init 生成）
  sci-draw/                       ← 图仓库（任何来源的图 + report）
  sci-write/                      ← 写作产物（plan/profile/正文/reading）
  sci-submit/                     ← 投稿产物
  (sci-polish/ 待定，暂不预建)
```

## 为什么是固定名 `sci-skills/`

类比 superpowers 的 `docs/superpowers/`——这是**技能家族的身份标记**，不是 project 名。
任何项目里看到 `sci-skills/` 目录，就立刻知道这是这套 skill 家族的落盘区。
人、skill、init 脚本都靠这个固定名定位，不需要配置。

## 源码 vs 产物 分离

- **skill 源码**：在仓库的 `skills/<skill-name>/`（SKILL.md / scripts / references）。
- **skill 产物**：在用户项目的 `<project-root>/sci-skills/<skill-name>/`。

两者同名但位置不同。源码是 skill 的实现，产物是 skill 跑出来的结果。
init 脚本只管产物侧（项目里的 `sci-skills/`），不动源码侧。

## 核心原则：目录引导文件 = 目录级接口契约

每个子目录里有一份 `.README.md`（点开头 = 隐藏，不污染目录，但 git 能跟踪空目录）。
**这份 .README.md 不是普通说明，是该目录的接口契约**：

- 任何 agent / 任何 skill 想往这个目录产出，**读这份契约就知道该放什么**：
  schema、字段名、命名规则、谁会读。
- 不需要知道是哪个 skill 在用、不需要 import 任何东西——照契约产出，下游自动能消费。
- 任何 agent / skill 想消费这个目录的内容，**读这份契约就知道怎么解析**。

**这就是解耦的真正落地**：契约在文件里，不在代码 import 里。一个全新的、素不相识的
画图 agent 读 `sci-draw/.README.md`，照做就能产出 sci-write 能用的图；一个第三方写作
agent 读 `sci-write/.README.md`，照做就能消费图仓库的 report。skill 之间可以互相替换，
只要遵守目录契约。

## 各目录契约概览（详见各目录的 .README.md）

| 目录 | 角色 | 关键契约文件 | 生产者 | 消费者 |
|---|---|---|---|---|
| `sci-draw/` | 图仓库（中性存储） | `figN-report.md`（6 段）+ `figN.png` | 任何来源（skill/手工/复制） | sci-write 等 |
| `sci-write/` | 写作产物 | `paper-plan.md`（图清单+章节状态）、四章正文、`data-profile.json`、`figN-reading.md` | sci-write | 人、润色/投稿 skill |
| `sci-submit/` | 投稿产物 | （设计确定后补） | sci-submit | 人 |

## 跨目录数据流（不复制、只读邻居）

skill 之间**不复制对方的产物**，避免双份不同步。只读邻居：

- sci-write 读 `../sci-draw/figN-report.md` 和 `figN.png`，但**不复制**进 `sci-write/`。
- sci-submit 读 `../sci-write/` 的正文，但不复制。
- 图仓库是图的唯一存放点；写作目录是正文的唯一存放点。

每个 skill 守自己的目录，读邻居的目录，写自己的目录。这是"读邻居不编排"的物质基础。

## 命名约定

- 图：`fig1`, `fig2`, ...（`figN` 前缀贯穿 .py/.md/.pdf/.png/-description.md）。
- 写作章节：`method` / `results` / `discussion` / `conclusion`，扩展名按人选（md 或 tex）。
- 中间产物：`data-profile.json`、`paper-plan.md`、`figN-reading.md`——固定名，跨 skill 互认。

## 演化规则

- **加新兄弟 skill**：把它加进 init 脚本的 `BROTHER_SKILLS` + `SKILL_DIR_GUIDES`，写它的
  `.README.md` 契约。下次 init 就预建它的目录。
- **改某目录契约**：改它的 `.README.md`。所有遵守契约的 skill 自动适配（因为它们读契约，
  不读实现）。
- **sci-polish**：策略待定，暂不预建目录。定后加进列表 + 补契约。

## 解耦自检

任何 skill 改完后确认它**没有破坏目录契约**：
- 它写的文件 schema 是否还匹配目录 `.README.md` 声明的？
- 它读邻居时是否假设了契约之外的文件/字段？（那会让邻居换实现时它崩）

契约是稳定面；实现是可变面。skill 各自演进，契约不动，就解耦。
