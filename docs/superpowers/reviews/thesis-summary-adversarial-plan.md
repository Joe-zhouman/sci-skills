# Existence Audit — thesis-summary spec

> 审查日期：2026-08-27　|　lens: design (aquarius)
> target: `docs/superpowers/specs/thesis-summary.md`
> parents: `thesis-skill-family.md` + `thesis-spine.md` + `thesis-dissect.md` + `thesis-intro.md`（round-2 修正版）+ `glossary.md`（不重审家族已定决策）
> bar: intro round-2 的两条修正先例——§① "gap-map.md 是 DATA BATON 非 coverage gate / 挣得存在需 genuinely-new accounting" + §⑦ "intro provide data, summary enforce lock"；以及 spine §⑤ residual 命名纪律

**net: -8 lines deletable/consolidable** | not Lean — 无 load-blocking；但 F1/F2/F3（major）应改完 spec 再实现，全是命名与归属级，非结构重设计

---

## Major findings

**F1（major）— summary-map.md 缺 intro-round-2 式"genuinely new content"核算；Callback 段近乎 restatement。**
claim：spec §① 的诚实 residual 已命名 check 的 near-triviality（"不防 agent 编一条 resolved-how 而正文没真收束"，L48），但从未回答 intro §① round-2 被迫回答的那个问题：summary-map.md 挣得存在的字段是什么。逐项看 schema（L133-144）：`gap-ref` 是 gap-map.md Gap N 的镜像键；`resolved-how` 是本 skill 刚写完的 synthesis prose 的一句话复述（从自己的 prose 可派生）；`anchor-in-synthesis` OPTIONAL 不 enforce（镜像 anchor-in-intro 降级，无 audit value）；`status=filled/unfilled` 中 unfilled surface 是真新内容；真正 genuinely new 的是 **Commonality 段**（pending→confirmed 是作者 depth gate 的落盘 footprint，L143-144，全家族此前无处记录）。即 Callback 段的机械价值收缩为一条：防漏记 + 官僚 lapse + unfilled surface——这正是父 spec summary 行强制要求的 coverage 机械载体（"每个 gap 被 callback，coverage 机械"），所以 artifact 站得住，但 spec 把文件 header 标成 "DATA + LOCK-ENFORCEMENT RECORD"（L122），与 intro §⑦ round-1 被 walk back 的 "gap-map.md = the lock" 同一膨胀方向（header 内紧跟的 near-trivial 免责句有自救，但归属段位错了）。check #2 自称 "**lock 的核心检查项**"（L84），其检查对象是 gap-list → entry 的 1:1 计数镜像——gaps 本就 ~1:1 derived from chapters（intro round-2 已 settle 的事实），该计数的 by-construction 近凡性 spec 未像 intro §⑥ 那样点名。
evidence：target L42-48, L84, L120-145（尤其 L122 header 标签 vs L125 免责句）；mirror 先例 intro spec §① L49-53 + §⑥ L102-106。
suggested disposition：在 §① 加一段"挣得存在的真正理由"（intro §① round-2 形态）：Callback 段唯一新状态是 status 面（unfilled contract-gap + 防漏记录）；resolved-how 是 prose 派生记录非兑付证据；Commonality confirmed-footprint 才是 genuinely-new 内容；header 的 "LOCK-ENFORCEMENT RECORD" 收敛为 "coverage-carrier + depth-gate audit footprint"。check #2 补一句 near-trivial-by-construction（gaps derived from chapters）。

**F2（major）— "gate-skip mirror sci-story" 是虚假归属；sci-story 的门无条件。**
claim：spec 三处把 skip 条件归为 sci-story 镜像——§⑧ 直接镜像清单（L98）、Step 1（L152 "framing 无歧义可 skip gate（mirror sci-story gate-skip）"）、eval 项 "gate-skip 条件"（L90/L219）。实查 `sci-skills-article/skills/sci-story/SKILL.md`：confirmation gate 无任何 skip 分支（L175-177 无条件 "run the confirmation gate… Get human confirmation"）；全文唯一 "skip" 是 L90 读邻居文件、以及 L305 "**Mandatory. Do not skip.**"（指 Step 8 Human review，语义相反）。该误标起源于已合并的 `thesis-intro/SKILL.md:218-219/278-279`（"Skip the gate only when… (mirror sci-story gate-skip)"），本轮被第三度复制进 spec + 未来 eval 用例——错误将随实现固化为 SKILL.md 文本和 eval 断言。
evidence：sci-story SKILL.md L175-177 / L305 vs target L98, L152, L219；origin thesis-intro/SKILL.md L218-219, L278-279。
suggested disposition：二选一并全程一致——(a) skip 条件按自身利弊独立论证保留（对镜像是 divergence，明说），或 (b) delete 该条款与 eval 项，①③ framing gate 一律必过。不允许的只有现状：挂 sci-story 名义的三连抄。

**F3（major）— §⑥#1 与 schema 的 pending 表示法不一致：现规范下该项是死 grep 或纯重复。**
claim：§⑥ item 1 规定查 "无 `[pending?` 残留（……镜像 check_spine/check_intro）"（L84），但 summary-map schema 从头到尾不用 `[pending? ]` 标记——候选以 `- status: confirmed ← pending → confirmed` 表示（L143-144），Callback 同（L135-136）。若脚本按字面 grep `[pending?`，合规产出的文件永远命中不了（死检查）；若意图实为查 `status: pending` 行，那它已被 #3（status=filled fail）+ #4（status=confirmed fail）完全覆盖（重复项）。测试验收列表的 "pending 残留 fail case"（L218）随之含糊：测哪个表示法？
evidence：target L84 vs L135-136/L143-144；对照 check_intro.py L29（PENDING_MARKER = "[pending?"，其上游 spine/intro schema 确用标记式）。
suggested disposition：schema 二选一定死——要么 Step 2 提候选时行内打 `[pending? ]` 标记（schema 明写，item 1 保留），要么删 item 1、统一由 status 字段表达 candidacy（建议后者：一个表示法一个执行点）。

## Minor findings

**F4（minor）— ③段 real-DOI placeholder 无 search pass，"引了才挂"无取 DOI 的 procedure。**
claim：Step 3 "轻引用：引了才挂 real-DOI placeholder，无专门 search pass（对比 intro 研究现状搜索——deliberate cut）"（L154）；§⑧ 也列 real-DOI 纪律为直接镜像（L98）。但 glossary Real-DOI placeholder 术语定义为"search MCP found 的真实标识符，never an empty [CITE:?]"——无 search pass 时，prose 若真引了文献，agent 要么无源可挂（违反术语定义）、要么现挂现搜（= 未声明的 ad-hoc pass，与 "无专门 search pass" 表述矛盾）。cut 本身成立，缺的是边界说明。
evidence：target L154, L98 vs glossary Real-DOI placeholder 条目。
suggested disposition：加一句明确：展望默认零引用叙事（hedged speculation 不需要支撑面）；若作者点名要引，skill 当场走一次 targeted search MCP 取真 DOI——如此 "无专门 search pass" 改写为 "无批量搜索轮，仅 on-demand 单点检索"。

**F5（minor）— init placeholder 的 registry 行删除超出字面邀请；父 spec handoff 表冲突未处理。**
claim：placeholder 的邀请句只覆盖文件清单补全（init_project.py L267："具体文件名随 thesis-summary skill 设计定（该 skill 后续计划补）"）；spec 计划的三个编辑里 "加 gap-map.md 读行 + 清单命名 summary-map.md" 在邀请射程内，"删 `../thesis-sources.md` registry 感知全貌 行"（L276）不在。删除本身是对的——留着一行假接口比越权编辑更糟，且 §⑤ 信息流单向收敛论证成立、父 spec summary 行读列确未列 registry——但有两处未交代：(a) 对父 spec 偏离节（L226）只引了 summary 行自证，未处理父 spec **handoff 表** `thesis-sources.md | init | 全家族`（父 spec L149）与本 cut 的矛盾；(b) 这是 family 第一次从 placeholder 删行而非填行，"planned expected update 非 churn" 的既有话术不完全适用。
evidence：init_project.py L267（邀请句）/ L276（registry 行）vs target L189, L226; 父 spec L162（summary 行）vs L149（handoff 表）。
suggested disposition：照做三编辑，但对父 spec 偏离节补一句：registry cut 以 summary 行为准，handoff 表 "全家族" 属父 spec 内部张力（summary 行 + handoff 表两处不一致是父 spec 自己的问题），并承认 registry 行删除是非邀请编辑、依据是契约须说真话。

**F6（minor）— lock 是 write-time 门；post-polish 失效面与拒绝 grep-anchor 的理由同构，却只在producer侧被援引。**
claim：§⑧ 升尺度论证用 "绪论可能上个 session 写的、可能被 polish 改过" 论证 enforce 必须落 consumer baton（L99）。属实，但对称事实未被命名：polish 后 process 也改 synthesis prose，而 summary-map.md 的 resolved-how 记录无人重验、check_summary.py 不再跑——lock 是 write-time 断言，非维持的不变量；其漂移暴露面与当初否定 grep-anchor 的 fragility 论证同构（anchor-in-intro 正因此降级）。家族现状是 point-in-time 门，这可接受，但 spec 只在 producer 一侧用了 drift 论证，consumer 侧同类暴露沉默。
evidence：target L99 vs L48（fragility 论证）、L137（anchor-in-synthesis 降级理由同构）；polish/typeset 仅 "感知总结状态"（L169），无重验义务。
suggested disposition：§门 诚实边界加一句：lock 为 write-time 门，polish 改写 synthesis prose 后一致性不再由脚本保证（与 anchor-in-intro 降级同一 fragility 类）——命名即可，无需新机制。

## Holds（vote-of-confidence，not re-audited）

- **enforcement split ①②③（user Q2 主线）**：站得住。②common-extraction 是 glossary 明列 architecture-level claim（depth 人工门合法必要）；①③ narrate 已 settle 架构（spine settle umbrella/Boundary，intro settle gap-data），re-gate 冗余论证与 intro §④ C3 同构且更干净——各段配门非装饰，是三层 split 的忠实内部落地。②的门用单次 depth gate 非 spine 四级 staged：正确，一级 claim class 不需要依赖序 staging（"staged" 措辞借用了 spine 词汇，无害）。
- **③ pre-settle vs 写后记录（user Q2 次线）**：不是 false binary。判据与 intro §② 不同侧：共性候选 grounding 可 pre-write 查证（chapter-map framework-instantiations + 各章 results 都在盘上），故 pre-settle 合法；弃选时以落盘为准并 surface（L70）——named residual 成立，非 dodge。共性候选是 generated 非 discovered，但走的正是 architecture-depth pre-write 人工门的 spine 血统（spine 整个 baton 都 pre-prose settle），无 outline-then-fill 问题（那是 dissect 的 in-write 重构禁令，另一码事）。
- **⑤ scope cuts（user Q4）**：不深读小论文 sound（dissect 已消化，再摄入是重复；单向收敛成立）；registry cut 见 F5（cut 对、论证缺一角）；展望无文献搜索见 F4（cut 对、DOI procedure 缺一角）。无隐藏代价大到翻案的程度。
- **§⑧ sci-story 归属主体（user Q3）**：诚实。fuse-claim-into-opening 实证核对无误（sci-story SKILL.md L161-163 fuse conclusion.tex 进 Discussion 首段，target 映射为 umbrella 复述，自称 "thesis 版" 合适）；verb calibration（L346-348）/per-section gate/targeted revision 均真实存在；②无 sci-story 对应物 by construction（单篇 Discussion 无跨章共性可提），血统归 spine 是 honest attribution。仅 F2（gate-skip）一处误标。升尺度变形段的 consumer-baton 论证主体成立（F6 指其 un-named 的对称盲点）。
- **check #1-#6 对 check_intro.py 先例的忠实度（user Q5 主体）**：高。#5 path guard、#6 BOM utf-8-sig / code-fence aware 切分 / 不可读处理全部实证存在于 check_intro.py（L174-178 traversal 拒绝、L116 utf-8-sig、L32-57 + L83-98 fence-aware）——mirror claim 不是空头支票。#2 双向查、#3/#4 字段门形态均与 #filled-by/status 先例同型。grounded-in 多章号解析是对 aries #5 单章号拒绝的正确反向（注意别盲拷 `_filled_by_chapter_num`）。2 附加观察不算 finding：summary 不跑兄弟脚本、以解析 gap-map 做 cross-ref——与 check_intro.py 只抽 chapter_nums 不验 chapter settlement 完全同构，precedent-consistent（可选加固：check_summary 反正要解析 gap-map.md，顺手验其无 pending/unfilled，一行的事；非缺陷）。resume/Step 0 hard-stop（含 stale 章 stop）与 dissect backtrack 语义衔接正确。写作链序 summary→theory 无交互问题（commonality grounding 不涉 theory 章）。
- **glossary 对齐**：Narrative gap（summary callbacks each）/ common-extraction / enforcement split 三术语使用 verbatim 无生造词；声称的无新术语成立。

## Score rationale

not Lean，亦无 load-bearing finding。与 intro round-1 相比，本 spec 是四份 sibling spec 里出生时最干净的：near-triviality residual、anchor 降级、fallback 形态、模板派生命名这些前任被抓过的坑都预付了。剩下的是三类账：F1 是缺席的诚实核算段（artifact 存活，加一段即可）；F2 是三连虚假归属（family 会第三次把不存在的 sci-story 条款固化进 SKILL.md + eval，必须在本 spec 拦住）；F3 是会让 check/test 写错对象的双表示法含糊。F4-F6 各一句话补丁。净删量约 -8（F2 skip 条款 ×3 处 ≈ -4、F3 去重或统一表示法 ≈ -2、F1 相关收拢 ≈ -2）；其余 patch 是增写非删。

**总裁决：接近 Lean，不 ship 现稿——F1/F2/F3（major）改入 spec 再进实现；无 load-blocking，其余 minor 随实现消化。**
