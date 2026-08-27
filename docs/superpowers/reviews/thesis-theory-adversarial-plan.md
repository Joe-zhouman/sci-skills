# adversarial plan review — thesis-theory spec (aquarius)

> 目标：`docs/superpowers/specs/thesis-theory.md`
> 权威：`docs/superpowers/specs/thesis-skill-family.md`（父 spec，SSOT）
> 方法：aquarius-lens-design。盘问存在性与忠实性——镜像先例是否真实成立、承重论证是否对得上盘上文件、honesty bookkeeping 是否漏项。
> 一切地面真值均已对盘上文件验证，非凭记忆。

---

## 0. Conformance sweep（先报对上的）

盘问方向全部核过，以下**成立**：

1. **①幕 depth-gate 论证 vs spine schema：成立。** spine spec L142-144 的 Unified framework 字段 = 框架 + per-paper 实例化两行，确无跨章组件枚举。"spine 没做过组件清单 / genuinely-new 结构选择" 对 schema 属实。协议血统（pending + tension-flags + 作者 settle）与 summary ②共性提炼同构，对象区分（method/theory 层 vs 贡献层）在 §⑧ 点破——诚实归属合格。
2. **init placeholder 旧文本描述：逐字准确。** `sci-skills/skills/thesis-init/scripts/init_project.py` L238 引文逐字一致；L247 registry 读行、L251 "thesis-dissect（读本章理论方法，写正文章时引用）" 均如实存在。justification 结构镜像 summary F5 先例且**更强**：旧文本与终局设计是直接矛盾（说 theory 读 registry、dissect 读 theory——均不成立），非 summary 案例的 merely-misdirected。点破不遮掩 ✅。
3. **模板槽位声明：精确。** template-spec.md 逐字含 "chapterN.tex（N 从 0 起：chapter0=绪论，chapter1=理论方法，chapter2+=正文，末章=总结）"；main.tex L16 = `\input{chapter1}   % 共用理论方法`。generic-test 包只织 main.tex + template-spec.md、无 chapterN stub → 痛点 3 "槽位空着、编译不完整" 是真的（`\input` 悬空文件），验收 #3 非空洞测试。
4. **父 spec 内部冲突（registry）：属实。** 交接表 L149 registry 读者="全家族" vs theory 行读列无 registry——named conflict + 采窄侧，与 summary F5 同法且事实核对无误。
5. **aries 硬化清单：真实继承。** shipped check_summary.py 含 utf-8-sig / fence-aware 切分 / hr 关窗（R1）/ 孤 fence 奇偶诊断（B4）/ ANSI 消毒（B5）；"从最硬化版起步" 有盘上依据。summary SKILL.md + references ×2（writing-discipline / synthesis-guide）+ tests/README.md 布局照实引用；"37-test 形态" 计数正确。
6. **归属 §⑧ 无 misattribution。** intro §④ 验证为原文（"intro 只 narrate 不 re-gate…hollow intro 可重写，hollow spine 是全盘坏基座"，intro spec L86），theory 把它应用于写作幕并显式标注不适用于枚举幕——边界自标，比 intro 自己当年多走了一步。
7. **glossary Overlap 清单 term 对齐逐字。** resolver-is-author 区分、`_Avoid_: overlap resolution gate / dedup list`、disposition optional 不 enforce——§③ 与 glossary 完全一致。
8. **trusted guard 覆盖面合规**：读清单全列 UNTRUSTED 且含 theory-map.md 自身（B7 mirror）。
9. **write-time 非 polish 后不变量** 已三处命名（§⑥ tail / 门与 enforcement / Acceptance 诚实边界）——F6 教训零残留。

---

## Findings

### T1 — check_theory.py 第 4 参数 `spine` 零消费者
**Claim**: ⑦ 标题与 Step 3 定死 "四参数：theory-map / chapter-map / spine / tex-dir"，但 §⑥ 检查项 #1-#4 无一读 spine.md。这是从 summary 抄来的形状：check_summary.py 的第 4 参有效是因为 gap-map 承载核心 bijection——theory 这边没有任何检查项用 spine 支撑。Step 0 的 spine-settle 检查到 Step 3 早已 stale（作者理论上可在写作中途回溯重开某字段）。要么参数有活干，要么它是死 surface。
**Evidence**: spec §⑥ items 1-4 vs Step 3 参数表；对照 summary §⑥ item 2（gap↔Callback bijection 吃 gap-map 参数）——同位参数在范本里承重、在这里悬空。
**Severity**: **moderate**（形状抄袭未验各元 earns-keep——正是 summary F3 死 grep 同类病，早于实现期发现成本最低）。
**Disposition**: 二选一并写入 §⑥：(a) 定义其职责——handoff 时复验 spine.md 无 pending 残留（挡作者中途重开框架后 theory-map 变陈的窗口，成本 ~3 行）；(b) 删参改 "三参数：theory-map / chapter-map / tex-dir"。倾向 (a)：time-of-check gap 是真实失败窗口。

### T2 — 偏离账本不对称：chapter-map 读列加宽未入账
**Claim**: 父 spec SSOT 双源都把 theory 的读列限定为 thesis-spine.md + 各正文章：theory 行（L163）无 chapter-map，交接表（L152）chapter-map 读者="summary"（明标 "dissect→summary 交接面"）。本 spec 却把 chapter-map 升级为 Step 0 hard-stop 依据 + grounded-in/chapter-ref 章号验证基准——对 compass 文件读面的**实质扩张**。该扩张本身可辩护（机械章号校验离了 canonical 章 registry 不可能，是对父门 "grounding 机械" 的必要落地），但 §偏离 只记了 registry 收窄，对这个加宽只字未提，而结论句写着 "**无偏离需 re-review**"。正是 F5 类 honesty-bookkeeping 缺口——方向相反（收窄入账、加宽逃逸）。
**Evidence**: 父 spec L149/L152/L163 vs 本 spec §④ Step 0 + 交接表 chapter-map 行 "grounded-in/chapter-ref 章号验证基准"；init dissect CONTRACT 占位（L188-189）读者列表同样只有 spine/summary。另注：dissect 侧 CONTRACT 文本的读者行将来也要跟（compass 面的 ripple），更该在账上。
**Severity**: **moderate**。
**Disposition**: §偏离 加一条 named deviation（"chapter-map 读列加宽：交接表读者 summary→+theory，理由 grounding 机械校验需章号基准；采窄侧同理反向适用"）。文字两行，不影响设计本体。

### T3 — 候选全否决 fallback 无终态痕迹：schema 兜不住自己的验收承诺
**Claim**: Step 1 fallback 定了 "候选全否决 → stop & surface 作者裁（裁最小章 / 回溯 spine）"，随后 §防带病推进 自己要求 "各 fallback 路径有落盘痕迹（pending / **无 confirmed 的 surface 记录**）"。但 theory-map schema 里不存在承载这个状态的槽位：Shared 空 + status 全 absent 时 check #2 空转 pass、"settled"、surface 清单为空。且 "裁最小章" 分支力学未定义——Step 2 framing gate 的 echo 输入全部定义在 confirmed 组件之上，零 confirmed 时这一幕谁写、按什么 gate 写、记什么，spec 沉默。对照 sibling 先例：summary 的同类洞有显式终态（Callback `status=unfilled` → contract gap → 落盘痕迹）。theory 反而在**唯一真正可能触发它的分支**上没有等价物。
**Evidence**: 本 spec Step 1 fallback 段 vs §② schema（status 仅 pending/confirmed 两值、无 waived/surface 态）vs 可回退段验收句 vs check §⑥ #2 的空集空转；对照 summary §④ unfilled 形态。
**Severity**: **moderate**。
**Disposition**: 给 fallback 一个显式落盘形态再谈其余：如 Shared 段允许单条 `component: <surface record>` + `status: waived-by-author`（或独立 `## Surface` 段），check 将其识别为合法终态而非 vacuous pass；"裁最小章" 一句话定力学（该模式下 Step 2 gate echo 退化为 (a)(c) 两项 + prose eval 补 depth），否则明确该路径由作者手写、skill 终止。注意家族既定 doctrine（summary review A-查过一条）：不为不可达状态加防御——这里不同，fallback **使它可达**，所以给的不是防御性 count 门而是终态表示。

### T4 — §④ 集合论断写反："不交叉" 三处交集
**Claim**: "（summary 读 spine/chapter-map/gap-map/intro tex/正文；theory 读 spine/chapter-map/正文——不交叉）"——两个集合共享 spine、chapter-map、正文三个成员，字面假命题。真命题是：**互不读对方产物**（summary 的独占物 gap-map/intro-tex/synthesis-tex/summary-map theory 一概不碰；theory 的独占物反之），所以互不 hard-stop、反序合法。结论在这正确表述下依旧成立——但 §④ 是反序合法的唯一论证，Acceptance 引用它，不该由一个 false premise 支撑着走。
**Severity**: **minor**（措辞级，结论存活）。
**Disposition**: "不交叉" 改 "互不依赖对方产物（交集仅共同上游 spine/chapter-map/正文）"。一行 shrink。

### T5 — Acceptance #2 把覆盖完整性写成可验收属性
**Claim**: "Overlap 段**覆盖每条 confirmed 组件的提升位置**；shared-ref/chapter-ref 无悬空"——后半机械可查（#3），前半无任何机制兜底：check 查不出漏记位置，eval 列了 定位真实性（编造 § 位置）却没列 记录完整性（写了没记）。真实失败模式恰是反的：agent 提升了材料但没随写随记 → 作者拿到的手解清单**看似完整** → 漏处直接撞查重。Spec 诚实边界命名了 falseness（编造位置），漏了 absence（缺席条目）——这正是 family 一贯拆分的两类里只报了一类。
**Severity**: **minor**。
**Disposition**: 验收句降格为可查部分；记录完整性挪进 eval（prose 层）并在 §门与 enforcement 诚实边界补半句 "不防提升未记录（overlap 覆盖完整性靠写后纪律 + eval）"。

### T6 — 测试路径与镜像范本不符
**Claim**: "`tests/test_check_theory.py`（stdlib，镜像 summary 37-test 形态）"——盘上 summary 的 37-test 文件住 `scripts/test_check_summary.py`（spine 同型），`tests/` 目录家族里只放 README.md。首例把测试写出 scripts/ 会破 "从 summary 版起步即天然硬化" 的落地路径，plan 期照抄范本时两处指名打架。
**Evidence**: sci-skills-thesis/skills/thesis-summary/{scripts/{check_summary.py,test_check_summary.py}, references/, tests/README.md}; sci-skills-thesis/skills/thesis-spine/scripts/{check_spine.py, test_check_spine.py}.
**Severity**: **nit**。
**Disposition**: `tests/test_check_theory.py` → `scripts/test_check_theory.py`；若有意开创新布局，deviation 入账（没必要）。

---

## 明确不立案的点（查过，别让下游重复查）

- **Overlap per-pair 粒度**（非逐组件合并）：作者逐位置手解 → per-pair checklist 正确，粒度镜像 per-gap 先例，不立案。
- **instantiates-framework 非空作为机械代理**：spec 明说质量归 eval/作者，只查非空——诚实表述，不是把 depth 塞进脚本，不立案。
- **空 Shared vacuous pass 单看本身**：家族 doctrine 拒绝为不可达状态加防御（summary A-review 同题）；本案问题不在防不防，在 fallback 使其**可达**且验收要求落盘痕迹——归 T3 处理，勿重复立案为缺 count 门。
- **ledger 并发共写顺序**：append-only + source tag，序无关正确性，两个写作 skill 任意顺序合流，无需协调点。
- **不读小论文 cut**：父 theory 行读列本就无小论文（"抽各小论文共用 method/theory" 由 chN.tex 承载材料），与 §⑤ 单向收敛同参 summary 先例一致，不需要 deviation 入账。
- **痛点 3 编译断言**：模板包无 stub、`\input{chapter1}` 真悬空——非 overstatement（见 sweep 3）。
- **write-first 拒绝论证 / pre-settle 合法性 / 归属血统链**：对 intro §②、summary §③ 同形，验证忠实。

---

## Verdict

设计本体站得住：混合协议（枚举=depth 门 / 写作=framing gate）经 spine schema 与 summary 先例双验成立，槽位/placeholder/硬化清单等所有**事实性**声明对盘核对无误，falsification 类问题（F1/F2/F3 式 misattribution）零残留。挂的是四处 bookkeeping 与一处力学缺口：T1/T2/T3 为 moderate，须在 plan 前落定；T4/T5 措辞与账目半句；T6 一行。修复总量 ~10 行，无一动摇设计。

**净：约 -10 行可删除（T1 参数行 / T4 短语 / T5-T6 改写压缩）。待 T1-T3 解决后即可交付。**
