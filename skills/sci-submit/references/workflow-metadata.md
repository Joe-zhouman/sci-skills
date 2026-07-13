# Workflow A: Metadata Setup

## 触发条件

用户说"帮我把投稿信息整理出来""提取元数据"、首次使用 sci-submit、或 `manuscript-meta.md` 不存在时。

## 核心理念

**投稿系统是一个填表任务，不是一个阅读任务。** `manuscript-meta.md` 不是给你看的文档——是给你贴的原料。

- 好记的字段（作者姓名、标题）不设代码块——留给不好记的（邮箱、ORCID、基金号）
- 一个代码块 = 一个 input 框。不要混。
- CRediT 用 markdown checkbox（`- [ ]` / `- [x]`），用户打开 md 就能打钩

## 步骤

### Step 1: 提取已知信息

读取正文，提取：标题、摘要、关键词、作者列表、单位、基金号。向用户确认。

**正文位置**：`../manuscript/`（项目根的一等公民，按 v/r 轮次组织）。读当前轮次——首投读 `../manuscript/v1/`，修回读 `../manuscript/rN/`。正文可能是 LaTeX 项目（`tex/main.tex` + `figures/` + `ref/`）或单个 `.md`/`.docx`。若 `manuscript/` 不存在或空，问用户正文在哪——不假设。

**薄耦合**：sci-submit 只**读** `../manuscript/`，不复制、不改、不写它。提取的元数据落进本 skill 的 `manuscript-meta.md`，正文本身仍是 `manuscript/` 的。

**⚠️ 作者名单——第一稿就定死。** 拿到作者列表之后，确认之前，问一句：> "这个名单你跟导师确认过了吗？投稿之后调顺序、加人、删人在 revision 阶段极其麻烦，proof 阶段根本不可能。导师最关心的是什么——就是谁排第一个、谁是通讯。你投之前给他看一遍，省得后面改不了。"

作者名字拼写也一样——投稿之后发现拼音错了一个字母，想在 proof 阶段改？可能被编辑拒绝。投稿前一个字一个字确认。

### 如果作者名单非要改——帮他写好给编辑的邮件

有时确实没办法——漏了人、加了实验、有人退出。如果用户说必须改，**不要让他自己写邮件。**

1. **打开 `assets/author-change-email.md`。** 三份模板：未受影响作者（只同意）、被影响作者（同意 + 确认）、通讯作者（请求 + 理由 + 确认全体同意）。每人用自己的邮箱发，CC 通讯。通讯最后发汇总那封。
2. **替用户填好所有 `[brackets]`**——作者姓名、期刊名、MS#、理由。理由从上下文提取，不要写 "per our discussion"——写具体贡献。
3. **提醒用户。** > "发完这批同意邮件之后，以后任何联系编辑的事，让通讯去发。你（一作）发的编辑不认。"

### Step 2: 生成 metadata 文件

照着 `assets/manuscript-meta-template.md` 的结构，复制 Author 块和 Affiliation 块，填入已知信息。写入 `sci-skills/sci-submit/manuscript-meta.md`。

**Affiliations 单独成节，不嵌在 Author 块里。** 地址拆成可粘贴零件：University（块）、School/Department（块）、Address（块）、Postal Code（块）——这些不好记。City 和 Country 不设块——好记。每个地址一个 `### #N`，作者通过 `地址编号 → #1 #2` 引用。一个作者挂多个地址、多个作者共享一个地址都正常——编号只管地址本身。

生成后向用户确认地址编号映射是否正确。

### Step 3: CRediT 分工采集

这是最容易被跳过但最不该跳的一步。流程：

1. **先尝试从手稿提取**——有些期刊在手稿末尾有 Author Contributions 段落。如果能提取到，预填 checkbox（`[x]` 表示有贡献）。
2. **如果手稿里没有**——告诉用户："你的手稿里没有作者贡献声明。CRediT 是很多期刊投稿时的必填项（Elsevier、Springer Nature、ACS 等），现在填好以后每次投稿直接复制。下面我给你每人列了一份清单，你打开 `sci-skills/sci-submit/manuscript-meta.md`，在对应的角色后面把 `[ ]` 改成 `[x]` 就行。"
3. **如果用户不清楚每个角色的含义**——简短解释（不要列 14 个定义，太长了；只说容易混淆的）：
   - *Conceptualization* = 想出这个研究的核心想法
   - *Investigation* = 做实验/跑模拟/收集数据的人
   - *Formal analysis* = 分析数据、做统计的人
   - *Writing — original draft* = 写初稿的人（通常只有一两个）
   - *Writing — review & editing* = 改稿子的人（几乎所有人都有）
   - *Supervision* vs *Project administration*：前者是学术指导（导师），后者是管项目进度和资源
   - 其余角色按字面意思理解即可
4. **用户填完告诉我** → 读回 `manuscript-meta.md`，进入 Step 4。

### Step 4: 合理性审计

拿到填好的 CRediT checklist 后，扫一遍异常：

- 第五作者勾了五个角色，第三作者只有两个 → 提醒用户确认
- 通讯作者没有 Supervision 也没有 Funding acquisition → 可能是漏勾了
- 只有一个人有 Writing — original draft，但有三个人有 Conceptualization → 通常是正常的，但提醒确认
- 有人只勾了 Writing — review & editing → 正常，很多作者确实只参与改稿
- 第一作者没有 Investigation 也没有 Formal analysis → 异常，提醒

**注意**：你不是来挑错的——你是来提醒用户"这个可能不对，你看看"。最终用户说了算。

### Step 5: 生成两种最终格式

用户确认后，把 checkbox 转成两种格式，写回 `manuscript-meta.md` 的每个作者块末尾：

**格式 1 — CRediT statement**（投稿系统 textarea，分号分隔）：

```
[First Author]: Conceptualization, Methodology, Software, Formal analysis, Investigation, Data curation, Visualization, Writing — original draft, Writing — review & editing.
[Second Author]: Investigation, Formal analysis, Validation, Writing — review & editing.
```

**格式 2 — Author Contributions prose**（手稿正文用，首字母缩写）：

```
[A.B.] conceived the study, developed the methodology, performed the experiments, conducted the formal analysis, curated the dataset, prepared all figures, and wrote the original draft. [C.D.] performed the simulations, analysed the results, and contributed to validation and manuscript review. [E.F.] acquired funding, provided resources, and supervised the project. All authors reviewed and approved the manuscript.
```

CRediT → prose 的映射不需要太机械。几个原则：
- 同一个人勾的多个角色合并成自然语言，不要"他做了 A、他做了 B、他做了 C"这样罗列
- 通讯作者通常有 Supervision / Funding acquisition / Resources，对应到 "supervised the project" "acquired funding"
- 末尾总是加一句 "All authors reviewed and approved the manuscript."
- 首字母缩写按期刊惯例：中文姓名是给定名缩写（如 Ming Li → M.L.），但先问用户确认他们领域的惯例

### Step 6: 推荐审稿人

推荐审稿人不是让用户凭空想——帮他找。

**1. 先问用户有没有现成的：**

> "你有没有已经想好的推荐审稿人？有的话姓名、邮箱、单位给我。"

**2. 没有 → 问能不能问导师：**

> "没事。导师知道谁适合审这篇——他比你更了解这个领域的研究组。你方便问他要 3-5 个推荐审稿人吗？一般导师会直接给名单。"

如果用户说导师给了名单 → 填模板。如果用户说"不想问导师"或"导师也不清楚"→ 进入第 3 步。

**3. 从手稿引用里找通讯作者：**

你读手稿的时候已经过了一遍 Reference。现在回头看：哪些参考文献是你最常读的相关论文？这些论文的通讯作者——你熟悉他们的工作，知道他们的水平，他们大概率也懂你的方向。这就够了。

具体操作：
- 从手稿 Reference 中，找出被引用次数最多的 5-8 篇核心论文
- 提取这些论文的通讯作者、单位、邮箱（能搜到的填进去，搜不到的标 `[需要你填]`）
- 列一个候选人列表，按"与被审稿件的匹配度"粗略排序

**4. 交给用户确认：**

> "我在你手稿引用最多的论文里找到这几个通讯作者，都是做跟你相关方向的。你看看哪些合适当审稿人？
>
> 1. [Name], [Affiliation] — 被引 [N] 次，做的 [方向]
> 2. [Name], [Affiliation] — 被引 [N] 次，做的 [方向]
> ...
>
> 需要 3-5 个。你选哪几个？有没有要加的人？"

**5. 用户确认后填模板。** 照着 `assets/manuscript-meta-template.md` 的 Reviewer 结构，每人一个 `### Reviewer #N`。

**6. 投到哪里——决策树：**

推荐审稿人放哪里、放不放，取决于投稿系统和你导师的意图。不要一刀切。

```
投稿系统有没有推荐审稿人栏位？
  ├─ 有 → 填进去。结束。
  └─ 没有 → 导师/老板有没有要求一定要加？
                ├─ 没有要求 → 不加。系统没这个栏位说明编辑不欢迎推荐审稿人。
                └─ 有要求 → 告知用户：
                            "这个投稿系统没有推荐审稿人的专用栏位。Comment 里
                             可以写，但编辑一般不喜欢——在没问你要的地方塞推荐
                             审稿人，容易让人觉得你在试图影响审稿流程。"
                            ↓
                            导师还是坚持要加？
                              ├─ 算了 → 不加。
                              └─ 加 → 填 Comment，简短一句：
                                      "Suggested reviewers: [Name] ([Affiliation],
                                       [Email]); ..."
                                      不写原因，不加解释。接受风险。
```

**话术要点**：
- 不要替用户决定"不加"——导师的权威大于编辑的偏好。告知风险，让用户判断。
- 不要在 Comment 里长篇大论写"为什么推荐这个人"——系统没问，编辑不关心。一行姓名邮箱足矣。
- 回避审稿人的逻辑不同：系统没有排除栏时放 Comment 是标准做法，编辑不会反感。

### Step 7: 回避审稿人

这一步不能只问用户"你有没有要回避的"——需要你主动做功课。

1. **读手稿，反向推**：从手稿的 Introduction 和 Reference 中，找出跟作者做同一方向的研究组。谁在做直接竞争的工作？谁的方法跟作者有争议？谁跟作者导师有过公开的学术分歧？
2. **列一个候选人名单**，向用户确认："我在参考文献里看到这几个组跟你的工作方向相近——[名字] 在 [机构] 也做 [方向]，[名字] 之前发过一篇跟你结论矛盾的论文。这些人需要回避吗？还有没有其他你觉得需要回避的？"
3. **用户确认后**填模板：每人一个 `### Excluded #N`。
4. **提醒投稿策略**："如果系统有专门的 Excluded Reviewers 栏，填在那里。如果没有，放在 Comment 里——理由简短写一句就行（比如 'direct competitor' 或 'known conflict of interest'）。这是 Comment 里唯一建议放的内容。"

### Step 8: 收尾提醒

> "这些数据以后填任何投稿系统都能直接复制粘贴。作者变了、基金加了，告诉我更新就行。"

## 更新时机

- 作者变动 → 更新 Authors / Affiliations / CRediT
- 基金追加 → 更新 Funding
- 手稿大幅修改 → 更新 Abstract / Manuscript Stats
- 换项目 → 新的 manuscript-meta.md

## 特殊领域：医学 / 生物 / 临床伦理声明

模板里的 `## Ethics & Regulatory` 节涵盖了医学和生物类期刊的特殊要求。生成 `manuscript-meta.md` 时：

1. **先问用户**：手稿涉及人类受试者、动物实验、临床试验、细胞系或生物安全吗？如果都不涉及，跳过整节。
2. 如果涉及，打开模板，逐个确认需要的声明，填好 `[placeholders]`。
3. 如果手稿里已经有相关声明 → 提取并填入代码块。
4. 如果有适用的上报指南（CONSORT / PRISMA / STROBE / ARRIVE 等），提醒用户投稿时提交对应的 checklist 附加文件。
