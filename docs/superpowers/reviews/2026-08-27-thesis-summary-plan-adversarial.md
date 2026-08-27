# adversarial plan review — thesis-summary Implementation Plan (aquarius)

> 目标：`docs/superpowers/plans/2026-08-27-thesis-summary.md`
> 权威：`docs/superpowers/specs/thesis-summary.md`（F1-F6 已消解，user-approved）
> 方法：aquarius-lens-design。盘问存在性与忠实性——plan 是否引入 spec 外设计、是否漏 spec 承重项、镜像先例是否真实成立。
> 一切地面真值均已对盘上文件验证，非凭记忆。

---

## 0. Conformance sweep（先报对上的，省得下面显得全在挑刺）

**spec §⑥ 检查项 ↔ plan 内嵌 check_summary.py：一一对应，无缺无越。**

| spec §⑥ | plan 代码 | 判定 |
|---|---|---|
| #1 无 pending 残留（status 字段制，无 `[pending?` 死 grep——F3）| 无 PENDING_MARKER；pending 由 Callback(filled)/Commonality(confirmed) per-entry status 拦截 | ✅ 忠实 |
| #2 gap↔Callback 双向 bijection | `seen_gap_refs` 双向查：缺席（L540-544）+ 编造 Gap 号 + 重复 | ✅ |
| #3 resolved-how 非空 + status=filled（unfilled fail）| ✅ | ✅ |
| #4 commonality 非空 + grounded-in ≥2 distinct 章 + 章号在 chapter-map + confirmed | ✅（distinct 用 set 解析，防 [Ch1,Ch1] 假两章）| ✅ |
| #5 synthesis-tex 字段存在 + 文件存在 + 绝对路径/`..` 遍历拒绝 | ✅ 守卫先于 is_file 探测（不摸 /etc/passwd 的存在性——顺序正确）| ✅ |
| #6 BOM utf-8-sig / fence-aware 切分 / 不可读文件优雅处理 | ✅ 全部镜像 check_intro.py 已落地形态 | ✅ |

plan 代码有而 spec 测试清单没有的增量（缺席三 baton 的 missing 分支、trailing-title 接受、multi-token gap-ref）均为 check_intro.py 先例的直接镜像（aries #5 = `_filled_by_chapter_num` 多 token→malformed，已验证在盘；aries #1/#2 同源）——非 scope creep。

**数字一致性（盘问方向 2）**：Task 1 测试函数逐一数过 = 14；Task 2 追加 = 11；14+11=25 与 Task 1 Step 4 "(14 tests)"、Task 2 Step 2 "(25 tests)"、tests/README 逐条列出的 25 case、两条 commit message 全对得上。`__main__` runner 扩展块 11 行恰好对应追加的 11 个函数，无漏调。

**F1-F6 忠实性（盘问方向 3）**：
- **F1** ✅ 三处落位（docstring L367-388 / SKILL.md 核心纪律 + P2 assert / tests README §2），genuinely-new 核算逐段分明（confirmed footprint + unfilled 新 / bijection near-trivial-by-construction 真价值缺席 / resolved-how write-time self-record）。frontmatter 的 "coherence LOCK's enforce side" 是 spec 自己的语言（enforce 端），P1 同时钉住 "intro provides data" ——不过度声称 guarantee。
- **F2** ✅ 零残留。全文 7 处 "gate-skip"/"skip" 出现全部是否定或引用语境（constraint F2 / SKILL.md 纪律 3 / writing-discipline 1 / known-cuts）；代码与工作流中无任何实际 skip 条件。前提已验证为真：`sci-skills-article/skills/sci-story/SKILL.md:305` = "**Mandatory. Do not skip.**"；误标化石确实只存在于 `thesis-intro/SKILL.md:219,279`。
- **F3** ✅ 代码无 `[pending?`；plan 中该串仅出现于 known-cuts 声明。正确——check_intro.py 有 PENDING_MARKER（intro 是 spine 表示法），summary 不搬。
- **F5** ✅ 两个依据如实呈现且点破：Task 6 导语明说读清单改写"超出字面邀请"、属 invited-by-design + 点破父 spec 冲突采窄侧；commit message 两依据并现。父 spec 冲突经核对属实（交接表 registry 读者="全家族" vs 写作链 summary 行读列无 registry）——已对 `docs/superpowers/specs/thesis-skill-family.md` 交接表/写作链逐行验证。替换前文本与盘上 placeholder（init_project.py SKILL_DIR_CONTRACTS["thesis-summary"] 块）**逐字一致**。
- **F6** ✅ write-time 在 docstring / SKILL.md P5 assert / tests README 三处命名，并显式给出 polish 后无人重验的对称论证。
- 其余约束：④段不跨 skill 编辑、pre-settle 合法性 named residual、Step 0 不跑兄弟脚本、allowed-tools 缺席、theory-last 指向——均与 spec/父 spec 逐条吻合。

---

## Findings

### A1 — phrase assertions 漏钉三处 spec 承重承诺
**Claim**: Task 3 Step 2 的 P1-P6 诚实命名断言是真的对应承重点，但 needle 循环 + P 断言整体漏了三个 spec 级承重承诺：(a) spec §④ fallback **不跨 skill 编辑兄弟产物**——decoupling grep（Task 7）只查 import 和"跑兄弟脚本"，查不出"fallback 时直接改 intro/正文"这类措辞漂移；(b) spec Acceptance 3 / 家族痛点 3 的**禁逐章复述**——只在 Task 4 的 synthesis-guide 内容指令里，零程序化钉住；(c) F4 的 **real-DOI 单点查证边界**——writing-discipline 承载但 SKILL.md 断言层完全无 pin（needle 表连 'DOI' 都没有）。
**Evidence**: plan L854-859（needle 列表）、L861-876（P1-P6）；对照 L820（跨 skill 编辑承诺仅在 prose 指令）、L917/L919（复述禁令仅 Task 4）、L907（F4 仅 Task 4）。
**Severity**: **minor**（scorpio 读 prose 能兜住一层；但本家族既定模式就是用便宜的一行 assert 钉承重话术——此处三个都是一句话成本）。
**Suggested disposition**: needle/P 块加三行——`assert '逐章复述' in open('.../references/synthesis-guide.md').read()`；needle 加 `'real-DOI'`、`'never edits sibling'`（或中文等价 '不跨 skill 编辑'）。

### A2 — spec「文件不可读」盲区：gap-map.md 的不可读分支无测试
**Claim**: spec 测试验收的 fail 清单含笼统的「文件不可读」。代码三条 baton 都有处理分支（sm 二进制、cm 不可读、gm 不可读各一段 except），测试却只盖了 sm（test_graceful_on_binary_summary_map）和 cm（test_fails_on_unreadable_chapter_map），gm 的 UnicodeDecodeError/OSError 分支是未测路径。cm 测试还断言了具体降级消息（"grounded-in cross-ref 跳过"），gm 的对称断言不存在。
**Evidence**: 代码分支 plan L497-502（gm）vs L507-512（cm）；测试缺位：Task 1 函数表 L239-295 + Task 2 函数表 L628-744 中无 `test_fails_on_unreadable_gap_map` 类似物。
**Severity**: **minor**。分支极简且 cm 版直接可抄，但不测的分支等于没写的分支——而这是 lock 的 data baton。
**Suggested disposition**: 追加一个镜像 cm 版的 gm 二进制测试（4 行 + __main__ 1 行），README 计数 25→26 同步改。

### A3 — Pre-flight 丢了先例的 base-sha 记录步骤
**Claim**: intro plan 的 Step 0 有 "Record the BASE sha (`git rev-parse --short HEAD`) for the final scorpio/taurus diff range + zero-churn assertion"；summary plan 只有 checkout，Task 7 直接用 `master...HEAD`。分析结论：merge-base 对并发合入 master 免疫，zero-churn 判定实际仍成立，所以这只失守先例一致性，不失守正确性。
**Evidence**: intro plan L57-60 vs 本 plan L54-61、L1075-1077。
**Severity**: **nit**。
**Suggested disposition**: 补一行 rev-parse（纯粹为了 review 阶段 diff range 可复述），或接受差异并明说为何不需要。

### A4 — Task 2 头部自标 "TDD, part 2" 名不副实
**Claim**: 全部跨 baton 实现（bijection/duplicate/fabricated，plan L517-560）在 Task 1 就落了码，Task 2 只补测试——按定义这些测试永远 green-first，不是 red-green TDD。blockquote 里其实诚实承认了（"The Task 1 implementation already contains this logic; these tests pin it"），所以只是标签过度：叫 TDD 会误导执行者去找一个不存在的 failing 步骤。
**Evidence**: plan L65（Task 1 header"TDD"含全部实现）vs L618（Task 2 header "TDD, part 2"）vs L624-628（追认实现先行）。
**Severity**: **nit**。
**Suggested disposition**: 把 Task 2 引语改成 "pinning tests (implementation already in Task 1)"，两秒的事；或不动——诚实已在正文里，标签是装饰。

### 明确不立案的点（查过，别让下游重复查）
- 逐行 bug 候选（_split_sections fence 状态机、BOM strip 走 utf-8-sig 而非 lstrip、PurePath.parts 的 '..' 判定、_single_ref_number 双 token 拒绝、fixture 替换锚点唯一性、woven CONTRACT grep 计数 ≥2、test_init.py existence-only 断言与内容编辑兼容、`init --no-git` CLI 旗标存在）：设计层面全部站得住，运行时归 aries（plan 已把 aries 列 MANDATORY + re-run 规矩）。
- 空条目 summary-map + 空 gap-map 退化为 vacuous pass：上游 check_intro.py 有「无 Gap 条目」守卫挡住，链路上不可达，不加防御是对的（加了才是 ceremony）。
- CONTRACT 读清单未列 intro tex 定位说明：CONTRACT 是工作笔记目录契约，tex 属于 thesis/tex 契约面，不属于本清单粒度——不算缺口。

---

## Verdict

**Lean. Ship.**

零 load-bearing / zero-major。四个 findings 全是 minor×2 + nit×2：无一阻挡实施；A1/A2 若要清，各是几行 assert/test 的顺手工——建议并入实施尾车（capricorn 收尾时顺手），不必为此返工 plan。net 口径：本 plan 无可删冗余（每一节都有 spec 依托），反而是净 +~10 行的可选加固（A1/A2 的 assert/tests）。

裁决一句话：**Lean. Ship.**（A1/A2 顺手带上，不阻塞任何任务。）
