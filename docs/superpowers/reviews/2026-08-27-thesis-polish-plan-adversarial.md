# adversarial plan review — thesis-polish implementation plan (aquarius)

> 目标：`docs/superpowers/plans/2026-08-27-thesis-polish.md`
> 权威：`docs/superpowers/specs/thesis-polish.md`（aquarius round-1 P1-P8 已消解，不重审 spec 级决定）+ `docs/superpowers/reviews/thesis-polish-adversarial-plan.md`（parent review）
> 校准参照：`docs/superpowers/plans/2026-08-27-thesis-theory.md`（已执行合并的家族先例）
> 方法：aquarius-lens-design。只审 plan 层：测试对能否转绿、声明是否对得上盘上真值、每条约束是否有 task 承接。Task 1 矛盾点经实跑验证（plan 自带实现 × plan 自带 fixture），非纸面推断。

---

## 0. Conformance sweep（先报对上的——下游别重复查）

1. **init 零编辑声明属实。** `sci-skills/skills/thesis-init/scripts/init_project.py` L45 逐字明写 "thesis-spine / thesis-polish / thesis-typeset 不预建"，polish 不在 `BROTHER_SKILLS`。Task 8 零 churn 期望 diff 表成立。
2. **三个 verbatim 继承 helper 真实存在且拷贝忠实。** `_fences_balanced` / `_CTRL_RE` / `_sanitize` 与 check_theory.py 盘上版本逐行一致（docstring 本地化在 plan 明示许可内）；正确地**没有**拖走 `_split_sections`/`_field_value`/`_top_level_field`（它们解析 baton `## Entry N` 块，polish 无此结构——rung 判断正确）。
3. **Task 2/3 对 wenqu 无一虚指。** 逐条对盘：em.high/p.uncheck/「致」截断（parse_paperyy.py L3-4）、`reduceAiListInfo=[JSON]` + `originalFragmentInfo{score, sectionContentList}`、`aiScore` 正则、≥80 阈值（parse_paperpass.py L30-45）全部为真。差异处（属性序无关正则 / stdout 契约 / break-vs-flag / 丢弃 simplesimsource 与【模板】过滤）均被 plan 明示为新决定或 named cut，无 "claimed inherited but actually different"。
4. **测试 fixture 忠实于 wenqu 解析的真实报告形状**（单双引号属性、class 多值、JS 赋值前缀 `var`、`\n` 拼接、HTML entity）。
5. **P1-P8 全部落在具体 task step**：P1→Task4 pt2/pt5+assertions；P2→pt2/pt5 run-to-completion；P3→pt2+assertion needle；P4→pt2/pt3 trace.md + Task6 缝合点；P5→Task1 实现+专测+README；P6→Task1 header-name 匹配+专测；P7→Task2/3 docstring 新接口声明；P8→Step3 "BEFORE the review gate"。无 dead letter。
6. **无 rung 违例**：知网 parser 未 stub（Rung 1 尊重）、无 bucketing JSON、无 init/兄弟 skill 编辑、check 范围恰为两项（无缩写首用等 spec 已拒项回流）。
7. **Task 4 其余 assertion needle 均有 Step 1 mandate 对应**（Step 0-5 / trace.md / 再检测 / 冷僻词 / 不篡改 / 此外·然而 / gap-map / untrusted / 检测报告 逐条核过）——例外见 F4。

---

## Findings

### F1 — Task 1 测试对自相矛盾：clean fixture 不 clean（实跑证实，green 阶段必卡）
**Claim**: `TEX_CLEAN` 第 5 行 `\ref{fig:overview}` + `\eqref{eq:model}`，但全 fixture 唯一 label 是 `ch:intro`——"clean" 项目自带两条悬空引用。`test_passes_on_clean` 断言 `issues == []` 必败；`test_eqref_cref` 的负断言（"existing key inside multi-key cref must NOT flag"）也必败（fig:overview 从 fixture 第 5 行就悬空）；`test_variant_in_comment_not_flagged` 的断言被这两条底噪打成 vacuous（区分不出注释排除是否生效）。将 plan 自带实现原样实跑：clean fixture → 3 条 issue。capricorn 逐 task fresh context，green 阶段失败的最近出路是削弱实现——把 gate 改坏。
**Evidence**: plan Task 1 Step 2 fixture vs Step 4 `_REF_RE`/`_LABEL_RE` 实现；实跑输出 `✗ ch0.tex:5 \ref{fig:overview} 悬空` ×2。
**Disposition**: fixture 补 `\label{fig:overview}` + `\label{eq:model}`（两行）。这不是精度问题，是 Step 5 无法转绿的必卡点。

### F2 — ledger fixture 记号行自啮：变体 ⊂ 自身规范形，实现无法对其通过 clean
**Claim**: `LEDGER_SETTLED` 记号行 canonical cell 是单位行的复制粘贴（`$\\mu$m`，应为 `$T(x)$`）——实跑即产生 `✗ ch0.tex:4 变体 T(x) → 应为 $\\mu$m`。且即使改成 `$T(x)$` 仍然自啮：变体 `T(x)` 是规范形 `$T(x)$` 的子串，正确文本必然含规范形 → 必然误报；实现的跳过规则只处理精确等值（`v.lower() != canon.lower()`）。fixture 把 gate 结构上做不到的检查（括号/包壳类记号变体）放进了 clean 基线。
**Evidence**: 实跑（F1 同次）；`_parse_ledger_pairs` 的等值跳过 vs `_variant_pattern` 的子串匹配。
**Disposition**: 二选一：(a) 记号行改可机械执行的形状（如 variants `Tmax / T_max` → `$T_{\max}$`——变体不在规范形内）；(b) 实现加一条跳过 `v in canon` 的对（变体包含于自身规范形 = 永远无法 enforce，跳过是语义正确非掩盖）。(a)+(b) 都做最稳。

### F3 — `(?<!\\)%` 注释剥离在 `\\%` 上判反
**Claim**: lookbehind 只看一个反斜杠。LaTeX 里 `\\`（换行）后的 `%` 是注释起点，`(?<!\\)%` 却判为转义百分号保留后文——偶数反斜杠串全判反。行内注释排除是检查 1 与检查 2 共用的地基，边角误留注释 = 变体/悬空 ref 漏报或误报。
**Evidence**: plan Task 1 `_strip_comment`。
**Severity**: minor（学位论文正文 `\\%` 罕见，但修正免费）。
**Disposition**: `(?<!\\)(?:\\\\)*%`；或 tests/README known-limitation 记一句。

### F4 — Task 4 Step 2 两条 needle 无 Step 1 mandate 对应（assertion 必卡）
**Claim**: assertion 要 `'thesis-typeset' in body`，但 Step 1 的九点 body-must-cover 无一处含该字面（只有 "typeset's territory"）；要 `'杠杆' in body`，九点里只有英文 "Levers ordered / lever"。"pull EXACT content from spec" 救不了后者（spec 有"杠杆排序"但 plan 的九点是操作清单）；前者 spec §后处理链位置确有"两 skill 各自 Step 尾指向对方"，plan 漏抄进 mandate。执行者按九点写完 → Step 2 断言失败 → 即兴补内容。
**Evidence**: Task 4 Step 1 九点 vs Step 2 needle 逐字比对。
**Disposition**: Step 1 九点补两处：pt5 加 "Step 尾指向 `sci-skills-thesis:thesis-typeset`（不 auto-run，spec 后处理链位置）"；pt2/pt5 杠杆措辞用中文"杠杆"。另：两条 assertion 的 P 标签挂错（'P4: structure-level surface named' 实为 P1；'P5: no restructuring' 实为 spec §⑤ 缝合分级）——追踪性修缮，顺手改。

### F5 — Task 8 第一条 decoupling grep 是装饰品
**Claim**: `grep -rnE '^\s*(from|import)\s+thesis-' --include='*.py'` 在合法 Python 里**永不可能匹配**（连字符不是模块名字符）——`DECOUPLING-OK` 无条件打印。真耦合面（subprocess/importlib 拉兄弟脚本）它不覆盖；第二条 grep（SKILL.md/references 点名兄弟 check 脚本）才是承重的。
**Evidence**: plan Task 8 Step 3 vs Python 词法。
**Disposition**: 删第一条；或换成能在真面上命中的形状（grep 兄弟脚本名 `check_theory|check_summary|check_intro|check_spine|check_dissect` 于 `scripts/*.py`）。

### F6 — parse_paperpass "无高分片段" 与 "解析失败" 共用 rc 1，语义混淆
**Claim**: js 找到、JSON 解析成功、零条 ≥80 ——这是**报告正常且论文干净**，plan 自己的消息都承认"这本身是结果"，却仍 rc 1 + stderr。格式漂移已被前三条结构化错误（缺 js / 无 reduceAiListInfo / 坏 JSON）拦住，兜底分支把成功误报为故障：Stage A 的 agent 按 rc≠0 走 parser 故障分支，干净论文被报成解析出错。
**Evidence**: plan Task 3 main 的 no-hits 分支 vs 其自身错误层级。
**Severity**: minor。
**Disposition**: 删 no-hits-error 分支——空清单 rc 0 照打 manifest（`0 段 score≥80`）。PaperYY 的 rc-1-on-empty 性质不同（整个结构零命中 = 漂移可信），保留。

### F7 — 杂项（合并报，逐条一行）
- `§File Structure: shrink: test_check_polish.py "~24 cases"——Step 5 / tests/README / Task 8 三处均 22。说 22。`
- `§Task 2 test_main_prints_manifest: delete: capsys=None 参数——pytest 残留，stdlib 裸调永不传，纯误导。`（顺带：Task 1/Task 2 test 文件顶部 `import sys` 未用。）

---

## 明确不立案的点（查过，别让下游重复查）

- **spec 级 P1-P8 的决定本身**：parent review 已 settle，本 plan 是忠实执行层，逐条落位见 sweep #5。不重审。
- **Task 2/3 与 wenqu 的归因**：sweep #3，全对盘。不立案。
- **`_readf`/`_sanitize` 三脚本各自内联重复**：家族先例即自包含脚本（check_theory/check_summary 同型），提公共模块反生耦合。不立案。
- **`VARIANT_MIN_LEN=2` 滤单字符变体**：噪声守卫正确；单字符记号变体本就不可机械执行（F2 的 (b) 已covers）。不另立案。
- **glossary / specs / plan 本身出现在 Task 8 期望 diff 表**：session 记录白名单，且 "if committed alongside" 措辞已容许其缺席。不立案。
- **Pre-flight 分支名 / base-sha 记录法**：theory-plan 先例同构。不立案。

---

## Verdict

plan 骨架成立：继承归属逐条对盘为真、P1-P8 全落位、无 rung 违例、wenqu 归因干净。挂的是一处**必卡点**（F1+F2 同根：Task 1 的测试对在 green 阶段无法转白——fixture 与实现互为矛盾，实跑证实 3 条幽灵 issue）和四处小账（F3-F7）。F1/F2 必须在 Task 1 Step 5 前修掉，否则 capricorn 最省力的出路是把 gate 改坏——这恰是本 plan 最承重的资产。

**净：约 -8 行可删除（F5 装饰 grep、F6 no-hits 分支、F7 capsys/未用 import），另 F1/F2 fixture 三行补修 + F4 mandate 两处补字 + F3 正则一处。修完即可交付。**
