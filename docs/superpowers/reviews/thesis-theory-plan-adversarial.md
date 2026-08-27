# adversarial plan review — thesis-theory implementation plan (aquarius)

> 目标：`docs/superpowers/plans/2026-08-27-thesis-theory.md`
> 权威：`docs/superpowers/specs/thesis-theory.md`（user-approved）；父 spec SSOT。
> 方法：aquarius-lens-design。一切地面真值已对盘上文件验证（init_project.py 逐字比对、
> check_summary.py 全文、35 条测试断言逐条 trace 到 plan 内嵌 check() 的 issue 字符串、
> init CLI flags、template-spec 槽位）。

---

## 0. Conformance sweep（先报对上的）

1. **T1-T6 全部真吸收，非 name-drop。** T1：第 4 参数在 4c 有实体职责（spine `[pending?`
   复验）+ 专属测试 + 显式禁删令。T2：dissect CONTRACT ripple 入账不修（零 churn 与家族
   fossil 同队列）。T3：`extraction-outcome: waived-by-author` 落盘终态 + 合法终态 pass 测试
   + confirmed-vacuous 拦截 + waived-with-entries 矛盾拦截——正是"终态表示非防御 count"的
   形态。T4：表述改为"互不依赖对方产物/无文件依赖"，假命题未迁移进 plan。T5：覆盖完整性
   明示非机械门，4c 注释与 tests/README known limitation 双处落位，且 `disposition:` 不查。
   T6：测试住 `scripts/test_check_theory.py`，tests/ 只放 README——与盘上 summary 布局一致。
2. **18 + 17 = 35 计数准确。** Task 1 十八个测试函数与 `__main__` 列表一一对应；
   Task 2 追加十七个与其 runner 扩展块一一对应；tests/README "35 stdlib cases" 一致。
3. **adapted check() 与继承 helpers 完全兼容（语义级 trace 通过）。**
   `_split_sections`（heading/hr/fence 三重 scoping）、`_field_value`（无前缀 `- ` 字段）、
   `_top_level_field`、`_is_empty`+`_NONE_TOKENS`（保留正确——"none" 充当空值的三个测试依赖它）、
   `_header_numbers`、`_single_ref_number`（0/多匹配返回 None → malformed 分支有测试钉住）、
   `_sanitize`/`_CTRL_RE`、imports（`PurePath`/`re` 在 4c 继续 use，未失锚）。BOM 用 `utf-8-sig`
   读入 ✓。stat-fallback `(OSError, ValueError)` 覆盖 embedded-NUL 的 ValueError（OSError 的
   兄弟类，显式列出）✓。
4. **35 条测试断言子串逐条对 plan 内嵌 issue 消息核对：全部命中。** 含三处易错点：
   waived 矛盾消息含 "waived"+"Shared 1" 标签 ✓；orphan-fence 单 ``` 触发奇偶诊断而
   fenced-fake 测试双 fence 平衡不误报 ✓；`_NONE_TOKENS` 使 "none" 触发缺失分支 ✓。
   `test_passes_on_settled` / `test_passes_on_waived_terminal` 全链路零 issue 复核通过。
5. **Task 6 四段旧文引文与磁盘逐字一致**（init_project.py L233-235 / L237-239 /
   L245-248 / L250-251）；sed 范围 L224-252 覆盖整个 contract 块；`--no-git`/
   无 --template 可跑（argparse 验证，镜像 summary-plan 同款命令先例）；sanity grep
   `≥2` 计数实际恰为 2 行 ✓。
6. **template-spec 槽位声明属实**：generic-test/template-spec.md L11
   "chapterN.tex（N 从 0 起：…chapter1=理论方法…）" ——init 预留槽位前提成立。
7. **无 camouflage 词**：Overlap 清单 / enforcement split / Load-bearing premise /
   信息流单向收敛 全为已 settle 家族术语；schema/字段名与 spec §theory-map.md schema 一致。

---

## Findings

### A1 — "helpers 逐字继承"指令把五处 summary 词面残留烤死在源码里，与自己的 taurus 门矛盾
**Claim**: Step 4 只许替换 docstring/constants/check()/main()，"do not 'improve' them" 锁死全部
helpers。但被锁的 helper docstring/注释里有五处点名 summary/intro 工件：
`_top_level_field` docstring（"从 summary-map.md 全文取…（`synthesis-tex: ...`）"——直接描述错文件）、
`_field_value`（示例 "`- gap-ref: ...`"）、`_single_ref_number`（"如 'Gap 1'" + "mirror intro aries #5"）、
`_header_numbers`（"Gap→gap-map"）、`_SCOPE_TERMINATOR` 注释（"那是本规则的 Callback/Commonality 特例"）。
Execution context 又明说 taurus 要查 "copy+adapt left no summary remnants"——按 plan 执行必产出
remnant，按 taurus 修复则违反 plan 指令。这不是 hypothetical：implementer 会卡在两个门的正中间猜。
**Severity**: minor（纯注释/docstring，零行为差；但制造确定性返工循环）。
**Disposition**: Step 4 加一行白名单："helpers 逻辑逐字不动，但 docstring/注释中点名的工件词允许换名
（summary-map.md→theory-map.md、synthesis-tex→theory-tex、gap-ref→shared-ref、Gap N→Shared N、
Callback/Commonality→Shared）"。约 2 行指令。

### A2 — BOM 测试钉错了分支：声称抓"悬空章"，实际靠 `<2 章` 消息里的值回显
**Claim**: `test_ignores_utf8_bom_in_theory_map` fixture 是
`grounded-in: [Chapter 9 §m]`——单章。plan check() 里 `len(nums) < 2` 先命中，发
"`解析出 <2 个不同章…`"，该消息经 `_sanitize(gi)` 回显原始值才让 "Chapter 9" 出现在 issue 里；
悬空分支（`elif … not nums <= chapter_nums`）根本不可达。docstring 却写着
"dangling grounded-in Chapter 9 — with BOM stripped it must be caught"。作为 BOM 金丝雀仍然有效
（不剥 BOM → 无条目解析 → 断言红），但钉住的语义与自称的不符，且不对称于 summary 血统
（镜像版用 `Gap 999` 对着非空 gap-map，走的是真悬空分支）。
**Severity**: minor（测试行为可用、文档句错误、血统不对称）。
**Disposition**: fixture 改两章一悬空：`[Chapter 1 §2, Chapter 9 §3]`——悬空分支真实可达，
"Chapter 9 不在 chapter-map" 成为唯一含该串的 issue，pin 与自述合一。

### A3 — Task 6 第四处编辑的依据张冠李戴：有什么用行的修改依据不在 spec §placeholder 补全里
**Claim**: spec §placeholder 补全只命名了三件事：文件清单补全、读清单改写、谁读它改写。
plan File Structure 与 Task 6 将"小论文→正文章 wording fix in 有什么用"也归入
"bases named in spec §placeholder 补全 / invited-by-design extension"——spec 并未点这一行。
该修本身是对的（旧文本"把各小论文的理论方法统一成一章"与 §⑤ cut 直接矛盾，同 stale 类），
但依据应自立而非借 spec 挂名。连带：Task 6 Step 4 commit message 只列
"the two stale theory-first lines"，静默漏掉它实改的第三处——message 与内容不符。
**Severity**: minor（bookkeeping 精度，非设计问题）。
**Disposition**: File Structure/Task 6 措辞分账：读清单/谁读它的依据 = spec §placeholder 补全；
有什么用行的依据 = §⑤ deliberate cut（旧文本与小论文 cut 直接矛盾）。commit message 点满三处
（one stale registry-read line + one stale reader line + one stale 小论文 wording）。

### A4 — Step 3 的 RED 预期机制写错一半：拷贝模块不可能吐 "extraction-outcome" 类消息
**Claim**: Step 3 解释失败机理："extraction-outcome unknown → missing-outcome issues"——事实是
copy 来的 `check_summary.check()` 里根本没有 extraction-outcome 这个概念，任何输入都不会产生
含该串的消息；RED 实际来自：synthesis-tex 缺失 issue（fixture 只有 theory-tex）、空 Gap 集合
issue、以及多个 assert `any("extraction-outcome"…)` 直接 miss。操作结论（FAIL 即 red、error 也算
red）没问题，但按该解释去核对的 implementer 会找幻影消息。另一个半句 "reads its 2nd arg as
gap-map" 属实 ✓。
**Severity**: nit（叙事精度，不影响执行）。
**Disposition**: 半句改为"copied module has no extraction-outcome/tex-field semantics — asserted
substrings simply miss（加上 summary 自身的 syn-tex/Gap 检查在异位参数上乱报）"。

---

## 明确不立案的点（查过，别让下游重复查）

- **同名 `_split_sections("Shared")`/`("Overlap")` 双切分开销**：O(n) 两遍，家族同型，非问题。
- **Overlap 无 duplicate-pair 去重检查**：逐（组件×章位置）粒度下重复位置合法残留作者侧纪律，
  spec 未要求，加门才是越权。
- **`main()` 退出码/打印无测试**：家族 parity（summary 同样只测 check()），不为单 skill 开新例。
- **`_top_level_field` 对 fence 内容不过滤（理论上 prose 里出现 `theory-tex:` 行会误配）**：
  shipped check_summary.py 同病，家族 fossil，§⑥ 已立"不顺手修"纪律——归 hardening queue。
- ** waived 模式下 Overlap 引用的 Shared 不存在却跳过悬空检查（`elif shared_nums and …`
  truthy guard）**：inherit-from-summary 的守卫形状，fenced-Shared 场景下正确降级，有先例背书。
- **Step 3 SKILL.md 10 条 P-断言 vs 正文大纲逐一核对全部可实现**（含 'no gate-skip'
  正向豁免条款、'[pending?' body 匹配）——无需放宽。
- **测试计数、sed 范围、CLI flags、`grep -c` 恰为 2**：均实测吻合（见 sweep 3/5）。
- **zero-churn 白名单含 docs/session records**：与 summary-plan A3 先例同构，不算开洞。

---

## Verdict

骨架忠实：spec 六项 finding 真吸收、拷贝适配策略与 shipped hardened 基座兼容性经全文 trace 成立、
TDD 序列红绿排列正确、四段 init 引文逐字一致、引脚计数全对。挂的全是词面层与测试语义层精度问题，
无一动摇结构：A1 需一行白名单防确定性 taurus 往返，A2 换一个 fixture 串，A3 分账措辞 + message
补一处，A4 半句纠正。

**净：约 -3 行（A3/A4 措辞压缩）+ 一行白名单新增 + 一个 fixture 串替换。修完即可执行，无须回炉 spec。**
