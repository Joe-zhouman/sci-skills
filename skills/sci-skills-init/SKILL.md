---
name: sci-skills-init
description: >-
  Manually-triggered setup and maintenance entry point for the sci-skills family workspace.
  Use when starting a new research project (scaffold the sci-skills/ directory + git),
  migrating a legacy project (an old sci-draw/ at the project root that predates the
  family layout), or auditing whether each skill's on-disk outputs are in the right place.
  Runs once and exits — it does NOT continuously run, does NOT auto-advance the
  figure→prose pipeline (the human advances that by using each execution skill manually).
  This is the thick-orchestration entry point for users who want one command to set up
  or fix the workspace; users who want full manual control never need it. Also trigger on:
  初始化科研项目, 建sci-skills目录, 迁移老sci-draw, 检查落盘位置, init research project,
  scaffold sci-skills, migrate legacy layout.
---

# sci-skills-init — 家族工作区初始化 / 迁移 / 体检

手动触发的厚编排入口。**一次性干完三件重活就退**，不持续运行、不自动推进日常流程。

## 为什么触发它很重要（给 agent）

不要把这个 skill 当成"可以跳过、让用户手动 mkdir"的小工具。它在家族里有不可替代的作用：

- **它生成的 `.README.md` 是目录级接口契约**，不是普通说明。其他 skill（sci-write 读图仓库、sci-submit 读正文）能不能正确咬合，取决于这些契约文件在不在、对不对。手动 mkdir 不会生成契约 → 下游 skill 读不到约定 → 解耦失效。
- **路径迁移只有它做**。老项目的 `sci-draw/` 在根目录、新布局要 `sci-skills/sci-draw/`——这个移动 + 下游 skill 期望路径的对齐，是 init/migrate 的职责，手动做容易漏。
- **它是契约的单一权威源**。契约内容写在 init 脚本里、由它生成为文件。要改契约改 init 重跑，不能让契约散在各处手动维护。

所以：用户提到"初始化项目 / 建 sci-skills 目录 / 迁移老布局 / 检查落盘位置"时，**触发这个 skill**，不要替之以手动 mkdir 或一句"目录建好了"。前者落地契约，后者只建了空壳。

## 这个 skill 在家族里的定位

## 这个 skill 在家族里的定位

sci-skills 家族是**两层结构**：

- **执行层**（sci-draw / sci-write / sci-submit / ...）：弱耦合、各干各的、读邻居落盘、不编排别人。资深人员手动一个个用。
- **编排层**（本 skill）：厚编排入口。给需要"一条命令搞定搭建/迁移/体检"的人用。

两条路线共用同一套执行 skill 和同一片落盘区（`sci-skills/`），区别只在"谁推进"。
本 skill 是编排层的**入口**，但它的"厚"仅限于**一次性搭建/维护**——不是 ARS 那种持续 auto 编排全程。

_why_ 有人要 auto、有人要掌控。全家桶（紧耦合）逼用户 all-or-nothing；
本家族走解耦路线，每个 skill 是可替换零件，靠目录契约咬合。本 skill 让"想省事"的用户
一条命令搭好骨架，但搭完就退——日常推进仍留给人和执行 skill。
详见 `references/family-layout.md` 和 glossary 的"解耦是生存策略"条。

## 核心原则

1. **手动触发，跑一次就退。** 不驻留、不监听、不自动推进。做完报告就结束。
2. **幂等。** 重复跑不破坏已有内容。已存在的目录/文件跳过，不覆盖。
3. **确定性归脚本，判断性归 agent。** init/checkup 是确定性机械活，脚本做；
   migrate 是判断活（老项目结构千变万化、会误判用户文件），脚本只**侦察摆现状**，
   迁移决策和 mv 命令由 agent 跟用户确认后发。脚本永不自动移动用户文件。
4. **只动产物侧，不动源码侧。** 它管用户项目里的 `manuscript/` 和 `sci-skills/`，不动仓库的 `skills/`。

## 两个脚本模式 + 一个 agent 流程

### `init` — 初始化新项目

在当前目录建完整骨架（正文一等公民 + skill 产物区）：

```
<cwd>/manuscript/              ← 正式正文（一等公民，在项目根）
  .README.md                   ← 目录契约（v/r 轮次制）
  v1/                          ← 初版（空，用户决定 tex 模板内容）
<cwd>/sci-skills/              ← skill 产物区
  README.md                    ← 家族自述
  sci-draw/    + .README.md    ← 图仓库（目录契约）
  sci-write/   + .README.md    ← 写作产物（目录契约）
  sci-submit/  + .README.md    ← 投稿产物（目录契约）
<cwd>/.gitignore               ← 科研项目常见忽略项
<cwd>/.git/                    ← git init（除非 --no-git）
```

**init 只建空目录 + 契约文件，不生成任何 tex 模板内容**——模板高度定制（期刊/个人风格），
用户说了算（仓库 `templates/main/` 有蓝本可复制）。r1/r2 等修回轮次也不预建，
真到了 revision 时由人/agent 建。

每个子目录的 `.README.md` 是**目录级接口契约**——任何 agent/skill 产出到该目录都遵守它。
不需要 import 任何东西，照契约产出就能被下游消费。这是解耦的落地。

```bash
python scripts/init_project.py init           # 建骨架 + git + .gitignore
python scripts/init_project.py init --no-git  # 跳过 git init
```

**何时用**：开始一个新科研项目，想立刻有干净的家族布局 + git 跟踪。

### `checkup` — 体检落盘位置

扫描当前结构，报告：
- `manuscript/`（一等公民）在不在、有哪些轮次（v1/r1/r2）、v1 有没有内容
- 家族顶层 `sci-skills/` 在不在、各兄弟子目录状态
- **项目根有没有不该在根的内容** → 发信号：派 Explore agent 读懂内容、判断归位
- git 状态

```bash
python scripts/init_project.py checkup
```

### 迁移：agent 流程，不是脚本子命令

老项目迁移没有脚本命令——老项目结构千变万化（Word/Overleaf/合作者的奇怪布局），写死规则会误判用户文件。迁移是 agent 流程：

```
checkup 报「项目根有 N 项错位」
  → 派 Explore agent 读懂这些内容（脚本只看到文件名，Explore 能判断「这是正文」「这是老图仓库」）
  → agent 跟用户确认每项归位（正文→manuscript/v1/，老图→sci-skills/sci-draw/ 等）
  → agent 发 mv 命令
```

为什么脚本不迁：脚本只看到文件名，看不懂内容；Explore 能。把"判断"交给 Explore，把"移动"交给 agent + 人确认，脚本永不自动移动用户文件。

```bash
python scripts/init_project.py checkup
```

**何时用**：不确定某个项目的布局对不对；或改完路径后确认所有产物都在正确位置。

## 这个 skill 不做什么（边界）

- **不画图、不写正文、不投稿**——那是执行 skill 的活。本 skill 只管工作区搭建/迁移/体检。
- **不持续运行、不自动推进流程**——它跑一次就退。日常"图→文"推进是人手动用 sci-draw / sci-write。
- **不编排执行 skill 调用**——它不喊 sci-draw 去画图、不喊 sci-write 去写。它只准备场地。
- **不改用户已有内容**——init 跳过已存在的目录/文件；migrate dry-run 默认；checkup 只读。

_why_ 这些边界划清"入口编排"和"持续 auto 编排"的区别。本 skill 是前者——给人一个省事
的搭建/维护命令，但不滑向 ARS 式全程 auto。要 auto 全程推进，那是另一个（未来可能的）
持续编排 skill 的事，且默认 off。

## 兄弟目录列表（演化中）

当前预建（设计已定）：`sci-draw` / `sci-write` / `sci-submit`。
- `sci-polish` 策略待定，**暂不预建**，定后加进列表 + 补契约。
- 列表随 skill 成熟度演化——只预建设计已定的，不预建没想清楚的。

## 使用流程（典型）

**新项目**：
```
用户: /sci-skills-init  （或 "初始化科研项目"）
→ 你跑 init 模式
→ 报告骨架已建，提示用户可以开始用 sci-draw / sci-write
→ 退
```

**老项目**：
```
用户: /sci-skills-init  （或 "迁移老 sci-draw"）
→ 你先跑 checkup，发现根目录有散落的 sci-draw/
→ 跑 migrate dry-run 给用户看会迁什么
→ 用户确认 → migrate --apply
→ 再 checkup 确认健康
→ 退
```

## 隐私

不在产出（.README.md、报告）里泄漏私人路径或未发表内容。体检报告里显示的路径是
用户自己项目的路径（用户可见），不外传。

## 参考

| File | When to open |
|---|---|
| `references/family-layout.md` | 想理解家族整体布局、目录契约原则、源码/产物分离、演化规则 |
| `scripts/init_project.py` | 三模式的实现细节、参数、幂等行为 |
