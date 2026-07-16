# sci-skills

零件 + 管理层。不卖全家桶。

## 为什么做这个

科研 skill 赛道太卷了。每个人都有自己的文献检索工具、自己的画图工具、自己的写作助手。问题是：它们之间不互通，大多数也不落盘，下一步拿不到上一步的产物。

**我们的赌注：不比覆盖面，比交接面。**

我们做小零件——一个 skill 只管一类产物，互不知道对方存在，换了谁的工具都不崩。我们也做管理层——一个项目经理 skill 负责搭骨架、写契约、把外部产物翻译成下游能消费的格式。用我们的零件也行，用别人的 lit review 也行，用自己 Excel 画的图也行。只要产物落盘、格式对齐，管线就能跑。

**能跟别人配合的零件，比自洽但封闭的套件活得久。** 这是我们在卷王赛道里的生存方式——也是唯一的差异化卖点。

## 包含内容

### 场景 A：英文期刊投稿

| Skill | 做什么 |
|---|---|
| [sci-skills-init](skills/sci-skills-init/) | 项目经理——搭骨架、写目录契约、把外部产物迁移并翻译成契约格式、巡检落盘位置 |
| [sci-draw](skills/sci-draw/) | 投稿级科研数据图 + 图报告（下游 skill 消费的报告文件） |
| [sci-write](skills/sci-write/) | 从图报告 + 数据画像写 Method / Results / Discussion / Conclusion。图义核查。真实 DOI 引用占位 |
| [sci-polish](skills/sci-polish/) | 直接在 tex 文件里润色，git commit 即审计。润色前读 sci-write 产物，不歪曲 claim/evidence |
| [sci-submit](skills/sci-submit/) | 投稿战役管理——硬约束采集、选刊、封面信、被拒转投、投稿后追踪 |

### 场景 B & C

中文学位论文、基金申请书——独立场景，各自的零件和 init。后面再做。

## 怎么工作的

```
项目根目录/
  manuscript/               ← 正式稿件（一等公民）
    v1/tex/                 ← skill 读写这里
  sci-skills/               ← skill 产物区（图报告、草稿、元数据、台账）
    sci-draw/               ← 图仓库（中性——谁画的都行）
    sci-write/              ← 草稿 + paper-plan + terminology-ledger
    sci-submit/             ← 封面信、候选期刊、投稿历史
```

每个子目录有一份 `.README.md` 契约——任何 agent、任何 skill、任何工具都能往里读、往里写，只要按契约来。没人知道文件是谁产的，也没人知道谁会消费。换生产者、换消费者，什么都不用改。契约就是唯一的交接面。

## 理念

- **人说了算。** skill 出草稿，人审查拍板。绝不吹嘘全自动——真正的科研从来不是全自动的。
- **文件是唯一的交接面。** 读邻居的产物可以，import 邻居的代码不行，触发邻居运行更不行。
- **合作优于锁定。** 用我们的零件、混别人的工具、不会干的活外包出去。管理层负责收拾残局。

## 安装

```bash
git clone -b release git@gitcode.com:Joe-zhouman/sci-skills.git
```

| 分支 | 用途 |
|---|---|
| [`release`](https://gitcode.com/Joe-zhouman/sci-skills/-/tree/release) | 干净分发版，安装用这个 |
| [`master`](https://gitcode.com/Joe-zhouman/sci-skills) | 完整开发历史 + 测试记录 |

## 开发

每个 skill 均按 [skill-creator-plus](https://github.com/Joe-zhouman/skill-creator-plus) 测试流程开发（evals → 迭代 → benchmark → 评分）。测试记录在 `skills/*/tests/`。
