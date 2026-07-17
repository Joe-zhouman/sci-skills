# Neighbor contract — 跟图仓库的落盘接口

本 skill 不 import 任何画图工具的代码、不假设图必须由某个 skill 产生。**唯一的耦合面是文件系统**：读邻居目录里落盘的 markdown 和 png，写自己的 markdown。

## 核心解耦原则：图从哪来，无所谓

sci-write 消费的是**文件契约**，不是某个 skill。邻居目录里的 `figN-report.md` 和 `figN.png` 可以来自：

- sci-draw 或任何画图 skill 产出
- 用户用 Excel / Origin / GraphPad / Illustrator 手工做
- 从已发表文献截图（合规前提下）
- 复制粘贴进来

**只要文件落到约定目录、符合下面的 schema，sci-write 就能用。** 本 skill 不追问图的出身，只验证文件存在 + 字段齐。

## 家族顶层布局

```
<project-root>/sci-skills/        ← 家族 namespace（固定名）
  sci-draw/                       ← 约定的"图仓库"目录（名字借 sci-draw 辨识度，
                                    但语义是中性的：图落这儿就行，来源不限）
  sci-write/                      ← 本 skill 的落盘
```

从 `sci-skills/sci-write/` 的视角看，图仓库在 `../sci-draw/`。这个目录名是约定俗成的图仓库位置——**不绑死 sci-draw 这个 skill**。

## 读图仓库的什么

| 邻居文件 | 何时读 | 读什么字段 |
|---|---|---|
| `../sci-draw/figN-report.md` | 图就绪后（scan_neighbor 报告） | 见下表 |
| `../sci-draw/figN.png` | Step 3 图义核查时，喂给识图能力（任何识图工具/识图模型，不绑具体工具） | 整张图 |

**不读** `figN-description.md`（若存在，那是某个画图流程的过程草稿，下游不该依赖）。**不读** `figN.py`（若存在，是实现细节，不稳）。本 skill 只依赖 report + png 两个文件。

## 契约缺口处理（不编、不跳、让人补）

读到 report 时若发现**不满足契约**——缺段（如没有 `Statistical methods`）、字段空（n/test/error type 未填）、格式不符（claim 不是一句话而是整段）：

1. **不编造**缺失内容（不自填 "n=30, t-test" 等——那是 auto-research 的苗头）。
2. **不跳过**该图、不假装它不可用。
3. **停下来，明确列出缺口**，请用户补充：
   > fig1-report.md 缺 `Statistical methods` 段。写 Method/Results 需要这些。请补：用的什么 test？correction？error bar 是 SD/SEM/CI？n=？
4. **用户补的内容落盘**——回写到 report（若用户允许改原图仓库），或记到 `figN-reading.md` 的"契约补充"段。**补充即契约**：补完的字段从此成为该图契约的一部分，后续步骤按完整契约用。

这条贯穿本 skill 对所有外部产物的态度：契约不是单向强制的，而是"发现缺口 → 人补 → 沉淀为契约"的生长过程。本 skill 是契约的执行者和缺口发现者，不是契约的编造者。

## figN-report.md 字段对照

图仓库里的 `figN-report.md` 约定是六段 markdown（`##` 标题）。本 skill 消费时这样映射：

| report 字段 | 本 skill 怎么用 |
|---|---|
| `Core conclusion` | 这张图证明的 conclusion → 写 Results 该图段落的领头句；Step 3 图义核查验的就是这个 |
| `Data source` | 写 Method 的数据描述段 |
| `Chart type & rationale` | 写 Method 时引用"为何选此图"；回答审稿人"为什么这么画" |
| `Statistical methods` | 写 Method 的统计段（test/correction/error bar/n）——逐字搬运，不自创 |
| `Key findings` | 写 Results 的具体观察句；从 observation 到 conclusion 的中间证据 |
| `Journal specs` | 决定正文里图的引用方式（单栏/双栏尺寸影响布局说明） |

**搬运纪律**：统计方法、样本量、误差类型这些**逐字从 report 搬**，不自创、不四舍五入、不"改写得更好看"。数据和统计是事实层，写作是叙事层，两者分明。

## paper-plan.md 的图条目 ↔ report 字段

plan 里每张图的条目（Step 1 起草）用与 report 同名的字段，使 plan→report 是"同一 schema 的 pending→done 演化"：

```
plan 条目字段          ↔  report 字段（drawn 后）
conclusion               ↔  Core conclusion     （sci-draw 证明的就是这个）
claim                    （plan 独有）            —  conclusion 怎么支撑 claim.md，sci-write 的写作责任，不进报告
data-source              ↔  Data source
status                   （plan 独有：pending|drawn|written）
report-ref               （drawn 后填 ../sci-draw/figN-report.md）
```

**两层分工：**
- `conclusion` → sci-draw 的活：拿到数据 + conclusion → 画图，图报告里的 Core conclusion 就是画完后验证过的 conclusion
- `claim` → sci-write 的活：拿到 conclusion → 写正文，解释"这个 conclusion 怎么支撑论文的一句论证"

conclusion 在 plan 阶段是"打算证明的"，在 report 阶段是"图实际证明的"（Core conclusion）。两者可能不一致——这正是 Step 3 图义核查要查的。

## 数据画像的共享

本 skill 在 Step 0 调 figure warehouse 的 `profile_data.py`（借用工具，不是耦合——profile_data 是无副作用的纯函数），把返回 dict 落盘成 `data-profile.json`。

- **本 skill 读 profile**：做科学判断（这数据能支撑哪些 claim、值得做几张图）。
- **画图时**：可读这个 `data-profile.json`，也可自己重跑 `profile_data.py`（幂等，无副作用）。两边不强迫对方读自己的产物。

`data-profile.json` 放在 `sci-write/`（产出者即所有者），不放共享区——因为它是本 skill 的中间产物，figure warehouse 有自己的等价途径。

## external 章节（Introduction/Abstract/Keyword）的交接

这些章节本 skill 不写，paper-plan 标 `status: external`。但**它们续写时要消费本 skill 的产物**，所以交接清单明确：

接手这些章节的 skill（或人）需要读：
- `paper-plan.md` 的全部图条目（claim 清单 = 贡献清单的骨架）
- `results.md` / `discussion.md` / `conclusion.md`（已成稿的正文）
- `../sci-draw/figN-report.md`（图的 evidence）

本 skill 在 Step 7 输出这段交接提示，不主动调任何 skill 去写——人决定何时续写。

## 解耦自检（维护本 skill 时跑）

改完任何文件后确认：

```bash
# 零 import sci-draw 内部模块
grep -rn "from sci-draw\|import sci-draw\|sci_draw" skills/sci-write/
# 应该只在 scripts/scan_neighbor.py 之外无命中（scan_neighbor 也只是读文件，不 import）

# 对 sci-draw 的引用只在"读 ../sci-draw/*-report.md"层面
grep -rn "sci-draw" skills/sci-write/
# 每条命中都应是文件路径引用，不是代码依赖
```

若发现 `import sci-draw.xxx` 或"假设 sci-draw 必须同时在场才能跑"的逻辑，那是耦合漏网，要修。
