# Workflow E: Post-submission Tracking

## 触发条件

稿件投出去了，用户想知道状态、要不要催、怎么催。

## 投稿后立刻做

更新 `submit-history.md`：

```markdown
### 2026-07-03 — Submitted to Nano Research
- MS#: [待系统分配]
- Cover letter angle: [一句话]
- Status: Submitted
```

系统分配 Manuscript ID 后立刻补上。

---

## 状态解读

不同投稿系统的状态名称不完全一样，但逻辑是通的。以下覆盖最常见的三类系统。

### ScholarOne（Wiley、Springer 等）

| 状态 | 含义 |
|---|---|
| `Awaiting Admin Processing` | 投稿成功，等编辑部处理。一般 1-3 天。 |
| `Awaiting Editor Assignment` | 分配编辑中。别催——这是正常流程。 |
| `With Editor` / `Awaiting AE Assignment` | 编辑已分配或正在找副编辑。可能持续一周。 |
| `Under Review` | 已送审。恭喜——最长的一步开始了。 |
| `Required Reviews Complete` | 审稿意见收齐，等编辑决策。 |
| `Awaiting Decision` / `Decision in Process` | 编辑在做决定。通常几天内出结果。 |

### Editorial Manager（Elsevier、ACS 等）

| 状态 | 含义 |
|---|---|
| `Submitted to Journal` | 投稿成功。 |
| `With Editor` | 编辑评估中（desk check）。如果超过 2 周 → 可能送审了但状态没更新；也可能编辑有积压。 |
| `Under Review` | 已送审。 |
| `Required Reviews Complete` | 审稿意见收齐。 |
| `Decision in Process` | 最让人焦虑的状态——但其实是最快的。通常 2-5 天。 |

### Nature 系（eJP）

| 状态 | 含义 |
|---|---|
| `Manuscript under consideration` | 编辑在看你。包括 desk check 和送审——这个状态什么都可能表示。 |
| `Editor assigned` | 编辑确认。 |
| `Manuscript under review` | 已送审。 |
| `Decision sent` | 结果出了。 |

### 一个重要的心理提醒

`Under Review` 之后的任何状态变化都是好事。状态变了说明有人在工作。状态停了一个月没变——那才是需要关注的。

---

## 催稿时机

先查该期刊的 typical 首轮审稿时间。可以用以下方式：

1. 看期刊官网的 "average time to first decision"
2. 看近期发表论文的投稿-接收时间线（有些期刊会标注 `Received: xxx / Accepted: xxx`）
3. 搜索 `[journal name] review time` — LetPub 和 SciRev 有用户贡献的数据

拿到 typical 时间后：

| 已等待 | 动作 |
|---|---|
| 没到 typical | 等。催稿在这个阶段没有用，可能还让编辑觉得你不懂规矩。 |
| 超过 1.3× | 可以礼貌问一次。部分编辑会推动审稿人。 |
| 超过 2× | 应该催。而且不必太客气——两周内没有实质性回复可以再催。 |
| 超过 3× | 考虑撤回改投。这个期刊的编辑管理可能有问题。 |

特殊情况：
- **急着毕业 / 评职称** → 如果 deadline 在 typical 时间内，投稿前就应该选审稿快的期刊。现在已经投了，可以在投稿后 1-2 周写信说明时间压力（部分编辑会加速处理）。
- **审稿人被放鸽子** → 最常见的原因。催稿帮编辑找到掉队的审稿人。
- **系统里同时出现两个 Under Review** → 审稿轮换——第一个审稿人退出了，换了人。重新计时。

---

## 催稿邮件

**一律由通讯作者邮箱发出。** 一作发的编辑可能不回——投稿系统里登记的通讯邮箱才是编辑认的通信渠道。如果你是一作，把邮件写好，发给通讯让他代发，别自己发。

**不要长篇大论。** 编辑收到催稿邮件、花 10 秒看完、查一下系统、回一句话。你的邮件应该让这 10 秒的使用效率最高。

```
Subject: Inquiry regarding manuscript [MS#]

Dear Editor,

I am writing to inquire about the status of our manuscript entitled
"[Title]" (Manuscript ID: [MS#]), which was submitted to [Journal Name]
on [YYYY-MM-DD].

[选一句：
  — 超过 1.3×: "We understand that the review process requires time."
  — 超过 2×:   "The manuscript has been under review for [N] weeks."
]

We would greatly appreciate any update on its current status.

Thank you for your time and consideration.

Sincerely,
[Your Name]
[Affiliation]
[Email]
```

**关键**：Manuscript ID 放在 Subject 里 — 编辑一眼看到就知道要查哪个稿子。标题和日期放在正文第一句 — 不需要翻邮件历史。不要附加任何解释为什么急着要结果 — 除非确实有硬 deadline 而且愿意跟编辑坦诚说明。

---

## 状态变化时的更新

状态每次变更，更新 `submit-history.md` 里的时间线，比如：

```markdown
### 2026-07-03 — Submitted to Nano Research
- MS#: NARE-2026-01234
- 07-05: With Editor
- 07-08: Under Review
- 09-15: Required Reviews Complete  ← 更新
- 09-20: Decision: Major Revision      ← 更新
```

这样不用翻投稿系统就能看到整个时间线。
