# Workflow C: Submission — 带你过投稿系统

> 前提：`manuscript-meta.md` + `hard-constraints.md` + `journal-shortlist.md` 至少有一个目标期刊条目。

## 这不是"写封面信"的工作流

这是"陪你走完投稿系统每一步"的工作流。封面信只是其中需要你临时生成的一步。其他步骤——标题、摘要、作者、基金号、推荐审稿人——早就写好了，都在 `manuscript-meta.md` 里。你的工作是：**告诉用户现在该复制哪一块、贴到哪里**。

## 前置准备：写封面信

封面信在投稿系统打开之前写好。写作流程：**读 `references/writing-tips.md` → 从 Cheat Sheet 取素材 → 写成正式段落 → 用户确认**。

### 数据来源

| 需要的内容 | 从哪里取 |
|---|---|
| **核心发现（首选：从落盘正文提）** | `../manuscript/v1/`（或当前 rN/）的正文 + `../sci-skills/sci-draw/figN-report.md` 的 Core conclusion/Key findings。这是家族咬合的价值点——cover letter 的发现不该让用户重抄，直接从正文和图 claim 提炼。 |
| Cheat Sheet（用户补充要点） | `manuscript-meta.md` → Cover Letter Cheat Sheet。落盘正文提不到的（背景钩子、广广吸引力这类叙事性内容）由用户在这里补。 |
| 期刊契合度论文 | `journal-shortlist.md` → 该刊条目下的已搜论文 |
| Manuscript Stats / 声明 / 署名 | `manuscript-meta.md` 对应小节（数据搬运，不涉及写作） |
| 写作风格 & 禁忌 | `references/writing-tips.md`（每次写之前翻一遍） |

### 写作顺序

每写完一段，打印出来给用户看。一段确认了再写下一段——一次性写完全部用户会漏看。

**1. 背景钩子**

读 `references/writing-tips.md` → Background hook。

然后看 Cheat Sheet → 背景钩子。用户列的要点可能是中文、关键词、半成品句子。你的工作是把它们串成一段英文，不添油加醋。固定开头句：`We wish to submit our manuscript entitled "..." for consideration for publication in [Journal Name].`

**写好**：打印 → 用户确认。

**2. 核心发现**

读 `references/writing-tips.md` → Findings summary。

**先从落盘正文提**：读 `../manuscript/v1/`（或当前 rN/）的正文 Results/Conclusion 段，加 `../sci-skills/sci-draw/*-report.md` 的 Core conclusion + Key findings。把提炼出的发现要点**预填进 Cheat Sheet 的核心发现区**，再让用户确认/补充。这避免了用户把已经在正文里的发现再手抄一遍——正文是 source of truth，cover letter 从它派生。

Cheat Sheet → 核心发现（用户确认后的要点）。可能包含定量数据——转成定性表述（"差两倍"不是 "p=0.003"）。一句顶过的独特点放在段尾。

拦截检查：
- p 值 / r 值 → 删，换定性
- "novel" "groundbreaking" "first-ever" → 最多一个
- 两个自然段 → 你写多了，缩到一个

**写好**：打印 → 用户确认。

**3. 期刊契合度**

读 `references/writing-tips.md` → Journal fit。

从 `journal-shortlist.md` → 该刊条目下的已搜论文。不是罗列，是串成叙事：有人做了 A → 有人推到 B → 我们的工作到 C。在叙事里嵌入引用。

**写好**：打印 → 用户确认。这是全信最关键的一段。

**4. 广众吸引力**

谁是这个期刊的读者？他们不是你的细分领域同行——是这份期刊的受众群。从期刊的 Aims & Scope 反推：这个期刊覆盖哪些学科圈？这些圈子的交集在哪里？你的工作对这个交集为什么重要？

一段就够了。不要写成 "This work should interest researchers in..."——通过内容让读者认出自己（见 `references/writing-tips.md` → Background hook）。

**写好**：打印 → 用户确认。

**5. 投稿信息 + 声明 + 署名**

数据搬运，不涉及写作。从 `manuscript-meta.md` 对应小节填入。

不打印确认。

### 写完回头翻

- `data/journal-requirements.md`：目标期刊特殊要求有没漏
- `references/writing-tips.md` → Tone

**输出**：

- **LaTeX**：先问用户要不要机构抬头（logo + 地址）。要 → `assets/cover-letter-template.tex`（首投）/ `assets/cover-letter-revision-template.tex`（修回）。不要 → `assets/cover-letter-plain.tex` / `assets/cover-letter-revision-plain.tex`。填 `{{PLACEHOLDER}}`，用户自己编译。
- **DOCX**：`scripts/generate-cover-letter.py`。首投：`--type first --background "..." --findings "..." --journal-fit "..." --audience "..."`。修回：`--type revision --changes "..." --msid "..."`。`--stats`、`--authors`、`--corresponding`、`--dept`、`--institution`、`--address` 从 `manuscript-meta.md` 对应节贴。\n 分隔多行文本。

路径：`sci-skills/sci-submit/cover-letter/<journal-name>-<YYYY-MM-DD>/cover-letter.tex`（或 `.docx`）

### 前置准备 2：GTOC（目标期刊要求时）

封面信写完之后、打开投稿系统之前，确认要不要 GTOC。查 `data/journal-requirements.md` 或目标期刊 Guide for Authors——关键字 "Graphical Abstract" 或 "TOC Figure"。投稿系统打开后文件上传页第一眼也能看出来：有这个上传槽就是要。

**如果要，现在就做。** 不要等到投稿系统打开、填表填到一半才想起来画图。子流程：

1. **问用户有没有现成的。** "这个期刊要 GTOC，你有现成的图吗？" 有 → 直接用。没有 → 继续。
2. **PPT 手绘。** "用 PPT 画一张，规格在 `data/gtoc-guide.md`（Elsevier 标准 5:2 1328×531px 300dpi）。画完截个图给我看。"
3. **截图来了 → 用识图工具分析。** 检查：缩略尺寸下文字能不能读、视觉流向清不清晰、有没有多 panel 堆叠/文字太多/宽高比不对。
4. **反馈 → 改 → 再截。** 循环到没问题。
5. **画完导出。** TIFF/EPS/PDF/PPTX，300dpi。放 `sci-skills/sci-submit/cover-letter/<journal-name>-<YYYY-MM-DD>/toc-figure.tiff`。

一次做好，换刊改尺寸就能复用。不需要 GTOC 的期刊跳过这一节。

---

## 主流程：引导用户过投稿系统

封面信写好了，GTOC（如需要）画好了，元数据填满了。

### 前置：新手还是老手？

**先问用户**：这个期刊的投稿系统你用过吗？

- **新手 / 第一次投这个期刊** → 走完整逐页引导（下面"典型页面序列"）。
- **老手 / 投过** → "好，元数据都在 `manuscript-meta.md`，封面信在 `cover-letter/`。你自己填，有问题随时问我。填完告诉我，我帮你更新 submit-history。"

不要假设用户是新手——老手被逐页引导会觉得你在浪费他时间。也不要假设是老手——新手没人带会卡在某个页面不知所措。

### 典型页面序列（新手路径）

> "好，准备好了。封面信在 `sci-skills/sci-submit/cover-letter/<journal-name>-<YYYY-MM-DD>/`，GTOC 也在那。元数据都在 `sci-skills/sci-submit/manuscript-meta.md` 里。打开 [期刊名] 的投稿页面，我告诉你在每个页面贴什么。"

逐页引导。一次只说当前这一页。

**Page 1 — Manuscript Files**

> "上传文件。主稿 PDF、图片文件、补充材料——按系统提示逐一上传。GTOC（如果有的话）选 'Graphical Abstract' 上传，不要选 'Figure'。文件名取对，顺序排对。"

**Page 2 — Article Type & Title**

> "选文章类型和填标题。文章类型选 [Research Article / Letter / Review / ...]。标题从 manuscript-meta.md → Title 复制——直接贴。"

**Page 3 — Authors & Affiliations**

> "加作者。manuscript-meta.md → Authors。每人名称、邮箱、单位按顺序填。通讯作者打钩。邮箱从 Email 代码块复制，ORCID 从 ORCID 代码块复制。Affiliations 从 Affiliations 节一个一个地址贴。"

**Page 4 — Abstract & Keywords**

> "贴摘要：manuscript-meta.md → Abstract。贴关键词：manuscript-meta.md → Keywords。"

**Page 5 — Cover Letter**

> "上传或粘贴封面信。文件：`sci-skills/sci-submit/cover-letter/<journal-name>-<YYYY-MM-DD>/cover-letter.pdf` 或 `.docx`。如果只有文本框，把内容贴进去。"

**Page 6 — Highlights（系统有上传槽或文本框时触发）**

> "Highlights。上传文件 → `highlights.docx`。贴文本框 → 从 manuscript-meta.md → Highlights 逐条贴，每条 ≤85 字符。"

**Page 7 — Funding**

> "贴基金。manuscript-meta.md → Funding。"

**Page 8 — Reviewers**

> "推荐审稿人和回避审稿人。manuscript-meta.md → Recommended Reviewers / Excluded Reviewers。有专用栏位→填栏位；没有→决策树见 Workflow A Step 6。"

**Page 9 — Declarations & Ethics**

> "声明页。Conflict of Interest 从 manuscript-meta.md 贴。Data Availability 贴。医学/生物类 → Ethics & Regulatory 对应声明贴。能勾的勾，要贴的贴。"

**Page 10 — Review & Submit**

> "总览。标题、作者顺序、通讯作者邮箱、基金号——全确认之后，点 Submit。"

---

## 提交后

1. **截图/记录 Manuscript ID**：提交成功后系统会显示一个 Manuscript ID。立刻记下来。
2. **更新 `submit-history.md`**：

```markdown
### YYYY-MM-DD — Submitted to [Journal Name]
- MS#: [Manuscript ID]
- Status: Submitted
```

3. **更新 `journal-shortlist.md`**：该刊状态改为"已投 YYYY-MM-DD"。

4. **告诉用户**：

> "投完了。投稿系统退出前截个图留底，然后关闭就行。接下来的事参考 Workflow E（投稿后追踪）——状态有变化告诉我，我帮你解读。"

---

## 修回投稿（Revision / Resubmission）

走同样的逐页引导流程，但以下几个页面有变化：

- **Cover Letter**：用修回版（简短——只写变更，不重新论证。详见下方 Revision Cover Letter 节）
- **Manuscript Files**：上传修改稿和高亮修改版（track changes 或 marked-up PDF）
- **Response Letter**：上传 Response to Reviewers（sci-submit 不生成这个，用户自己准备）

**不要在这一步调整作者名单。** Revision 阶段加人、删人、调顺序——需要给编辑写书面理由，有些期刊要求所有作者重新签一遍版权协议。审稿周期本来就不短，因为作者名单调整多拖几周不值得。投稿之前就把名单跟导师敲定。

### Revision Cover Letter

长度不超过首投信 1/2。用 `assets/cover-letter-revision-template.tex`（LaTeX）或 `scripts/generate-cover-letter.py --type revision`（DOCX），不要用首投模板。

结构：
1. 致谢审稿意见 + "detailed point-by-point Response Letter accompanies this submission"
2. 非科学变更：格式、作者、基金、数据声明改动（`--changes`，\n 分隔多条）
3. 更新后的 Manuscript Stats
4. "We thank the editor and reviewers for their constructive feedback"

不要重新推销论文——编辑已经知道它是干什么的。

---

## 关键拦截

逐页引导时最容易犯的错：

| 错误 | 拦截 |
|---|---|
| 让用户自己决定贴什么 | 不要——"下一步是填摘要，打开 manuscript-meta.md，Abstract 那段，三击全选，贴到摘要框"。具体到哪个字段、哪个文件。 |
| 一次性说完十页 | 投稿系统一页一页翻的。一次只说当前这一页。 |
| 用户卡住你没发现 | 每个页面贴完之后问一句"贴好了吗？/ 有问题吗？"再翻下一页。 |
| 封面信内容暴露硬约束 | "我为了评职称所以投一区"这种话永远不要出现在封面信里。从 hard-constraints 推立意，但措辞用学术语言。 |
