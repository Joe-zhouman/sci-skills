# Workflow F: Hard Constraints & Advisor Management

## 持久化文件

硬约束采集后写入 `sci-submit/hard-constraints.md`，与 `manuscript-meta.md` 并列。`journal-shortlist.md` 的排序以该文件为首要筛选条件。

## 触发条件

首次使用 sci-submit 且 `hard-constraints.md` 不存在时自动触发；用户说有硬性约束时手动触发。

## 核心理念

**人的命运要靠自己争取。** 导师定目标的时候可能不了解实际情况——他上一次亲自投稿是十年前，他不知道这个期刊现在 desk reject 率 70%，他不知道你的方法在这个领域的竞争稿里属于什么量级。你不说，他就不知道。

先尝试讲道理。不是争辩"你错了"——是把数据摆出来，让他自己看到差距。如果讲了没用，再走务实路线：让审稿人替你说"不"。

## 步骤骨架

### Step 1: 提取硬约束

把模糊要求翻译成可验证的量化条件：

| 用户说 | 翻译为 |
|---|---|
| "导师要投 Nature 子刊" | Nature 旗下所有子刊（Nature Materials, Nature Energy, Nature Comms…） |
| "评副教授要 2 篇一区 Top" | 中科院升级版 1 区 + Top 标记，数量 ≥2 |
| "毕业要求一篇 SCI" | SCI 收录期刊，不限分区 |
| "我们组只发一区" | 中科院升级版 1 区（大类或小类） |
| "IF 必须 10 以上" | JCR IF ≥ 10 |
| "学校要求必须发 OA" | 期刊必须为 OA（Gold OA / Hybrid OA，不限制费用） |
| "学校不让发 OA" | 期刊不能为 OA（只投订阅制期刊） |
| "导师不让交版面费" / "我们没钱" | APC ≤ 0（排除所有收 APC 的期刊。注意：OA ≠ 收费——很多 OA 期刊不收 APC，如 Diamond OA 期刊） |
| "Nature Comms 可以，但太贵了" | Nature Comms 在范围内，但 APC > $X 的排除 |

OA 和费用是两码事，别混。OA 是期刊性质（Gold/Hybrid/Diamond），APC 是价格。学校可以要求 OA 但导师不掏钱——那就只能找不收 APC 的 OA 期刊。导师可以愿意付钱但学校不允许 OA——那只能找订阅制期刊。

### Step 2: 现实检验

用手稿的实际质量和硬约束做对比。关键问题：
- 这个工作放到目标期刊的已发表论文旁边，量级够不够？
- 方法新颖度在目标期刊的竞争稿中处于什么位置？
- 有没有硬伤（样本量、机制深度、novelty 类型）？

### Step 3: 据理力争——先尝试跟老板讲道理

现实检验做完，如果发现差距明显——**先别急着走妥协路线。先尝试一句。**

不是说"老板你错了"。是把数据摆出来让他自己看。导师是科学家，科学家认数据。他不了解现实不是因为他不讲理——是因为没人给他看这些。

**帮他准备一段消息。** 不要长篇大论。几行字，每行一个可验证的事实：

> "[老板称呼]，我查了一下 [目标期刊] 最近一年的发表情况——
>
> - 他们去年发了 [N] 篇跟 [你的方向] 相关的文章，平均 IF [X.X]，方法上 [共同特点——比如都是用 DFT + 实验验证 / 都有大规模临床 cohort]
> - 我们的工作 [一句话差异——比如纯模拟 / 样本量 / novelty 类型不一样]
> - 同期另外几本期刊——[Journal B] 和 [Journal C]——最近发了几篇跟我们的路数更接近的工作：[具体例子]
>
> 你觉得是直接投 [目标期刊] 试试，还是先考虑 [B/C] 更合适？"

**为什么这样写**：
- 不评价目标期刊好坏——只列数据
- "你觉得"——不是你在替他做决定，是你在让他做决策
- 给了具体的备选——让他有台阶下

**如果用户不想跟老板说话**——帮他发：

> "我帮你写好了。你复制发给他就行。他回了什么你转给我，我帮你想下一句。"

**老板回了什么**：

| 老板说 | 怎么回 |
|---|---|
| "没事，先投再说" | 不争。进入 Step 4。 |
| "那你觉得哪个合适" | 你已经准备好了——从 shortlist 挑一个，告诉他理由 |
| "先看看吧，我再想想" | 别催。等两天再问。他可能在消化 |
| 没回 | 两天后提醒一次。再没回——口头问。不是逼问，就问一句"上次那个期刊的事你看了吗" |

**讲通了** → 更新 `hard-constraints.md` 和 `journal-shortlist.md`，按新目标重新走选刊流程。

### Step 4: 讲不通——不匹配时的务实策略

如果老板说了"没事先投再说"——到此为止。不争了。走务实路线。

1. **第一轮**：选 2-3 个审稿快的高端期刊投（Nature Comms 的 desk reject 可能只要 2-4 天，Science Advances 可能 1-2 周）
2. **记录反馈**：每次被拒把编辑理由（如有）写入 `submit-history.md`
3. **准备保底**：在 `journal-shortlist.md` 中预先排好 Tier 2（匹配）和 Tier 3（保底）
4. **无缝切换**：被拒后不浪费时间，直接走 Workflow D 投下一个
5. **积累证据**：被拒几轮之后，拿着编辑反馈和发表数据再回到 Step 3——那时候对话就不一样了。不是"我觉得不行"，是"前三个期刊都 desk reject 了，编辑的理由都是 X，你看要不要调整？"

### Step 5: 写入 `hard-constraints.md`

将量化后的约束写入持久文件，作为 journal-shortlist 排序的第一依据。

## `hard-constraints.md` 模板

```markdown
# Hard Constraints — [manuscript short title]

## Source (约束来源)

| 来源 | 类型 | 截止时间 |
|---|---|---|
| 导师要求 | 期刊范围 | — |
| 评副教授 | 分区 + 数量 | 2027-06 |
| 毕业条件 | 收录 | 2026-12 |

## Quantified Constraints (量化约束)

| # | 约束 | 类型 | 值 | 来源 |
|---|---|---|---|---|
| 1 | 只投 Nature 子刊 | journal-whitelist | Nature Materials, Nature Energy, Nature Comms, ... | 导师 |
| 2 | 中科院升级版 1 区 Top | cas-rank | 1区 + Top | 评职称 |
| 3 | 至少 2 篇 | count | ≥2 | 评职称 |
| 4 | SCI 收录 | indexed-by | SCI | 毕业 |
| 5 | 必须 OA | oa-required | true | 学校 |
| 6 | APC 限额 | apc-max | $3,000 | 导师 |

## OA & Cost Constraints（OA 和费用是两码事）

> 四种常见组合，选一个：

- [ ] **非 OA + 不付钱**——只投订阅制期刊（大多数传统期刊）。最省事。APC = 0。
- [ ] **非 OA + 可以付钱**——订阅制期刊，部分期刊收 page/color charges。APC 不算问题但不能太离谱。
- [ ] **OA + 不付钱**——只投不收 APC 的 OA 期刊（Diamond OA：如 SciPost、Physical Review X、部分学会期刊；或 Hybrid 期刊但选订阅制投稿）。
- [ ] **OA + 可以付钱**——Gold OA 期刊都可以投，APC 上限 $[X]。Nature Comms 约 $6,790 / Science Advances 约 $4,950 / ACS Omega 约 $4,500 / MDPI 约 $1,500-3,000。

APC 上限：$[X,000]（来源：[导师 / 学校报销限额 / 基金预算]）

## Journal Whitelist (必须投的期刊)

- Nature Energy
- Nature Materials
- Nature Communications
- ...（由约束 #1 展开）

## Journal Blacklist (不能投的期刊)

- Scientific Reports（导师明确排除）
- PLOS ONE（学校不认）

## Strategy (不匹配时的策略)

- 第一轮目标：Nature Comms（审稿快，2-4 天 desk decision）
- 如果被拒：积累编辑反馈，必要时和导师沟通调整
- 保底线：确保至少 2 篇在 2027-06 前投中一区 Top
```

## `journal-shortlist.md` 引用方式

shortlist 的 Tier 划分以 `hard-constraints.md` 为首要筛选条件：

```markdown
## Tier 1: Hard Constraints Targets (硬性要求)
<!-- 从 hard-constraints.md 的 Journal Whitelist 展开 -->
| # | Journal | IF | CAS | 审稿周期 | Strategy |
|---|---|---|---|---|---|
| 1 | Nature Energy | 70.1 | 1区Top | 2-4周 desk | 第一枪，大概率 desk reject |
| 2 | Nature Comms | 14.7 | 1区 | 1-3周 desk | 审稿快，让导师看到结果 |

## Tier 2: Realistic Targets (务实选择)
...

## Tier 3: Safety Net (保底)
...
```
