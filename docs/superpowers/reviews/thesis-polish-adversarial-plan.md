# adversarial plan review — thesis-polish spec (aquarius)

> 目标：`docs/superpowers/specs/thesis-polish.md`
> 权威：`docs/superpowers/specs/thesis-skill-family.md`（父 spec，SSOT）+ `docs/superpowers/glossary.md`（AIGC 降率 / 去 AI 味 / 缝合 本 session settle）
> 方法：aquarius-lens-design。盘问存在性与前提——承重论证是否对得上盘上文件、resume/排序/grounding 三条机制声明是否真成立。
> 地面真值全部对盘核对，非凭记忆。

---

## 0. Conformance sweep（先报对上的）

1. **镜像归属 §⑧ 逐条真实。** sci-polish 六件 references 在盘（language-guide / paper-types / phrasebank / section-guide / style-guardrails / writing-strategy），映射无虚指；style-guardrails L65 确有 `| Category | Term / variants | Canonical form | Source | Notes |` 表格先例。
2. **init 零编辑声明属实。** `sci-skills/skills/thesis-init/scripts/init_project.py` 注释块明写 "thesis-spine / thesis-polish / thesis-typeset 不预建"，polish 不在 `BROTHER_SKILLS`。零 churn 断言成立。
3. **wenqu 借鉴有盘上实体。** `aigc-reduce-playbook/scripts/parse_paperpass.py` / `parse_paperyy.py` 存在；杠杆按伤质量排序 + 冷僻词警告在 research doc §7.1 逐字可查。
4. **ledger ripple 入账真实。** spine SKILL.md Step 0 只标 `source: thesis-spine`，确无表格模板——"零 churn 留 cleanup" 的 ripple 是真缺口非假账。
5. **知网推迟有据**（无样例盲写 = 猜格式，Q3b 用户确认），扩展位接口中立声明在案。
6. **glossary 纪律干净**：AIGC 降率 / 去 AI 味 / 缝合 三 term 全程 verbatim，无 `_Avoid_` 别名溜入（重构 / humanizer / 润色 泛称均未乱用）。
7. **UNTRUSTED 报告面处理正确**：风险判断驱动改写 + instruction-like text 是 data + 改写锚回作者自己的小论文原文（损害上限 = 回真实材料），split 是对的。
8. **check 范围 vs 工作流承诺**：职责① 的四个失败类中两个机械（变体残留 / 交叉引用）、两个归 agent + eval（缩写首用显式拒绝有据 / 记号走 agent 对照）——enforcement split 账目自身闭合，不立案。

---

## Findings

### P1 — 结构级 surface 清单无落盘家，撞家族第一原则
**Claim**: Acceptance #4 把结构级断裂的处置验收在 "清单在状态报告"，但 §scope 产物面 = "tex 原地改 + ledger 共写 + git commits，无新文件/目录"——状态报告不是文件，是 chat 输出。surface 清单是**唯一要求作者事后行动**的产物（polish 明确不动结构，作者要拿着清单改章），也是唯一**必然跨 session 存活**的产物（作者改结构从不当场）。glossary 第一原则 No Save, No Safe："anything that lives only in a conversation is unsafe"。dissect/intro/summary/theory 各有 working-notes 文件夹装这类交接物；polish 被父 spec 定为无文件夹（git 留痕），本 spec 把唯一 prose-actionable 输出路由进无文件形态，未 flag 这个张力。
**Evidence**: spec §Acceptance#4 vs §scope 产物面行 vs glossary §Family principles #1；父 spec §skill 文件夹策略（polish 无文件夹）。
**Severity**: **major**——需要设计决定，不是措辞。
**Disposition**: 二选一，都零新文件：(a) 宣布 commit message 是 on-disk 载体（类型① 每章 commit message 逐字携带该章 surface 项，状态报告 = 这份盘上记录的 chat 渲染）；(b) 接受 chat-only 但把 Acceptance #4 验收句降格 + 显式引用 No Save No Safe 说明为何此处豁免（说不通，别选这条）。(a) 便宜且与 "commit message 带诊断" 先例同构。

### P2 — Stage A resume 论证在自己的 Step 0 门上断裂
**Claim**: §③ 无落盘清单的 YAGNI 论证承重在 "断点 resume = 重 parse + 对照当前 tex 跳过已消解的风险句"。但 AIGC 阶段是**末尾单 commit**（类型③），中断在阶段中途时：working tree 脏 → Step 0 拒跑 → stash/discard 丢掉的恰是 "已消解" 状态；commit 进去则破 "三类分明" 验收。resume 故事只在 commit 边界成立，而最可能的中断模式恰恰在阶段中途。"git diff 可见已改句" 在 AIGC commit 被后续 per-chapter commit 埋住后也需指名 diff 那个 commit，spec 未说。
**Evidence**: §③ 无落盘清单论证 vs §⑥ 三类 commit（阶段单 commit）+ Step 0 git 检查（非干净拒跑）。
**Severity**: **moderate**。YAGNI 决定本身可能仍然对——报告持久 + parser 幂等使 "从头重跑 Stage A" 便宜——但 spec 写的不是这个机制。
**Disposition**: 改论证不改决定：明说 Stage A run-to-completion，中断 = 丢弃 in-flight diff 重跑（报告还在，重 parse 零成本），"跳过已消解" 机制删掉。YAGNI 站得更稳，因为不再依赖一个假的 resume 故事。

### P3 — Stage A 先于 diagnose：继承纪律被无声悬置
**Claim**: §② 同一段先宣布继承核心纪律 "不许句子润色结构坏的段落（先结构再润句子）"，再安排 Stage A（句子级改写）跑在**任何结构诊断之前**——Stage A 无法知道哪些段落结构坏。freshness 论证支撑的其实只是 "Stage A 先于 **fix**"，不是 "先于 diagnose"：Step 1 是只读的，不移动任何文本，diagnose→Stage A→Step 2 的顺序同样保定位新鲜。glossary 已 settle "报告存在时放最前"，顺序本身不翻案——但 spec 未对纪律冲突置一词，读者以为纪律无例外。
**Evidence**: §② 表格下纪律句 + Stage A 段 vs 工作流 Step 1 只读性质（跑 check + agent 对照，无改写）。
**Severity**: **minor**——一句话的事。
**Disposition**: 不动顺序（glossary 已定），在 §② 或 Stage A 行加半句：Stage A 是先结构后句子纪律的 **named exception**（detector-facing 定位约束），其改写句在 Step 2 语体层被复检（"顺带" 句已有，接上即可）。

### P4 — 缝合句级 grounding 的 named 表面颗粒度不对
**Claim**: §⑤ 句级补写的合法性论证 = "动机句从 spine 递进关系可推导"，grounding 指名 spine/chapter-map。盘上核对：chapter-map.md **一条/章**（dissect spec §③ 定死），字段 `{role(s), papers, framework-instantiation, progression-in, progression-out, tex-file, status}`——**章间**递进，无模块级信息。而缝合断缝是章**内** method-results 模块间的过渡——低于 grounding 表面的颗粒度。"为回答上一模块的 X" 里的 X 是模块级 results，chapter-map 里没有。模块级逻辑最细的盘上记录是 dissect 的 per-paper `trace.md`（claim + IMRaD 结构 + 如何推进主线），**不在 Step 0 读清单里**。glossary 缝合 term 的 "grounded in spine/chapter-map's recorded progression" 承了同一个颗粒度错位——term 定的是分级语义，表面颗粒度是本 spec 的实现事实。
**Evidence**: dissect spec §③（一条/章）vs 本 spec §⑤ + Step 0 读清单（spine + chapter-map，无 paper-X trace）。
**Severity**: **moderate**——grounding 约束是句级补写越界防线的一半；表面空转则防线退化为 "agent 自说自话 grounding"。
**Disposition**: Step 0 读清单加 `thesis-dissect/paper-X/*/trace.md`（只读，零 churn，read-neighbors 许可），grounding 优先级 trace（模块级）→ chapter-map（章级）；或降格声明为 "章级关系 grounding + 模块级由本章 tex 局部推断"——二选一，别让 commit message 里的 "grounding: chapter-map" 指向一个装不下该 grounding 的文件。

### P5 — check #2 的未用 label 方向是噪声发生器
**Claim**: 交叉引用检查的第二个方向 "定义了但从未 `\ref` 的 label" 按 issue 级报。学位论文现实：`ch:`/`sec:` label 每章每节都有、大多合法永不 `\ref`；公式同理。百 label 量级的 thesis 会产出几十条非问题。它抓的 misspelled-ref 场景（label 改名漏改一处 ref）已被方向一（悬空 ref）覆盖。死 label 在 LaTeX 里零编译影响、零读者影响。issue 清单是家族 check 的信用资产（no-raise、bounded、每条 actionable）——混入系统性噪声训练作者略读，赔上的是两条真检查的注意力。
**Evidence**: LaTeX label 使用现实 vs spec §Implementation Notes check #2 + Acceptance #1 "无未用 label"。
**Severity**: **moderate**。
**Disposition**: 删第二方向；或降为独立 info 层（不进 issue 清单、不进 "清零" 验收）。Acceptance #1 同步删 "无未用 label"。

### P6 — normative 表格格式与其引用的先例不一致
**Claim**: §④ 把 ledger 表格格式定为 normative 四列 `Term/variants | Canonical form | Source | Notes`，理由是 "对齐 sci-polish style-guardrails 先例"——先例实际是**五列**（L65 首列 `Category`）。验收测试写 "ledger 表格规范" 未定：header 名是否逐字匹配、列数是否精确、多列容忍否。照四列文本写的 parser 读到先例形状的 ledger（带 Category 列）即 mis-parse——check #1 的地基与它引用的地基不同一。
**Evidence**: 本 spec §④ vs sci-skills-article/skills/sci-polish/references/style-guardrails.md L65。
**Severity**: **minor**。
**Disposition**: 二选一：verbatim 采纳五列；或 normative 行加半句 parse 规则（"按 header 名匹配，允超集列"）。ripple cleanup commit 里顺带 pin 时用哪个形状，此刻定死。

### P7 — Stage A 的 I/O 事实与被镜像的 parser 不符
**Claim**: (a) 工作流与中间格式节说 "报告文件 → parser / 用户给报告文件路径"——`parse_paperpass.py` 的输入是报告**目录**（docstring："解析 PaperPass 免费版离线报告目录"，数据在 htmls/js/），不是单文件。(b) pipeline 说 "parser stdout 结构化输出"——wenqu 双 parser 是写 out_dir JSON 文件，非 stdout。镜像声明（"镜像 wenqu，格式已知"）在 I/O 契约层面不成立：stdout + 中立格式是**新决定**不是镜像，重设计可以，但 spec 把它写成继承事实。
**Evidence**: wenqu-mem/skills/aigc-reduce-playbook/scripts/{parse_paperpass.py,parse_paperyy.py} docstring vs 本 spec §③ pipeline + Step 0。
**Severity**: **minor**——plan 期照抄范本时两处指名打架。
**Disposition**: Step 0 / Stage A 行改 "报告文件（PaperYY）或报告目录（PaperPass）"；stdout 契约显式标为新接口决定（自研 parser，wenqu 只借形态）。

### P8 — 全局替换 commit 落在 review 门之后
**Claim**: 三类 commit 里爆炸半径最大的是类型②（ledger 驱动跨章机械替换——一处在另一语境有别的含义的变体被全局换掉即伤章）。它排在 Step 4，而 mandatory human review 是 Step 3。最需要人看的改动恰好无人再看：Step 4 之后无 review 门，验收即 "check 清零"——机械清零不审替换的语境正确性。
**Evidence**: 工作流 Step 3（review）→ Step 4（commit ② + ledger 回写）顺序 vs §⑥ 三类 commit。
**Severity**: **minor**。
**Disposition**: 术语统一挪进 Step 3 之前（一次 review 盖三类 commit），或 Step 4 明写 commit ② + ledger 回写同受 mandatory review。

---

## 明确不立案的点（查过，别让下游重复查）

- **四职责一 skill**：父 spec aquarius #3 已 settle 为 known v1 simplification，glossary 三 term 是其术语化落地。不重审。
- **中文-only scope**：无隐藏依赖断裂——英文摘要无任何下游 skill 消费，作者手译的术语漂移不进任何机械面；v1 cut 与 typeset 前置页先例同构。不立案。
- **缝合分级边界本身可判性**："补句可修 vs 需动内容" 在诊断时对强模型可判，误判双向可恢复（surface 误报 = 作者烦；句级误判 = diff 审可见）。真正的风险在 grounding 表面（P4），不在判据。不另立案。
- **UNTRUSTED 报告面**：sweep #7，split 正确。不立案。
- **check 两项 vs 工作流承诺**：sweep #8，账目闭合。不立案。
- **polish 新增读 spine/chapter-map/theory-map**：read-neighbors doctrine 本就许可任意读，父 spec 交接表读者列是主要消费者描述非 ACL。不需 deviation 入账。
- **知网扩展位 / ledger 缺失降级不 hard-stop / polish-typeset 无依赖序声明**：均诚实有据。

---

## Verdict

设计本体站得住：四职责的 workflow 落地、双 parser + 中立格式 + 知网扩展位、缝合分级、镜像归属——与父 spec 和 glossary 对表无 overturning，全部事实性声明（init 零编辑 / 六件 references / wenqu 实体 / spine ripple）对盘核实为真。挂的是三处机制声明的承重错误（P1 状态报告无落盘家 / P2 resume 论证自破 / P4 grounding 颗粒度错位）——P1 须在 plan 前落定，P2/P4 是改论证与补一行读清单；P5 删半个检查项；P3/P6/P7/P8 一句话到两行。无一动摇设计骨架。

**净：约 -6 行可删除（P5 半个检查项及其验收 / P2 假 resume 机制句 / P7 镜像措辞），另 P1 一处验收句须改写 + P3 一句补账。待 P1 落定后即可交付。**
