# Adversarial review — thesis-theory（aries）

> 日期：2026-08-27　|　审计者：aries（The Breaker）
> 范围：git ab5a893..0c16917（branch thesis-theory）——`sci-skills-thesis/skills/thesis-theory/`
> 全套（SKILL.md + scripts/check_theory.py + scripts/test_check_theory.py + references ×2 +
> tests/README.md）+ 唯一 foundation 编辑 `sci-skills/skills/thesis-init/scripts/init_project.py`
> 的 `SKILL_DIR_CONTRACTS["thesis-theory"]` placeholder 补全。
> Rounds：R1 boundary / R2 state machine / R4 resource / R5 input / R6 skills（mandatory）。
> **R3 concurrency：deliberately skipped** — 单进程、无共享可变状态、test runner 串行；
> 无 parallel-access 面可打。

## 先决验证

- **shipped tests 在本机跑绿**：`python3 sci-skills-thesis/skills/thesis-theory/scripts/test_check_theory.py`
  → `ALL TESTS PASS (38 tests)`，Python 3.13.13，exit 0。
- **auto-discovery runner 审计**：`sorted(globals().items())` 按 key 排序——key 唯一，
  永不比较 value，callable 比较炸裂路径不存在；无任何非测试 callable 以 `test_` 开头；
  38 个定义、零重名、runner 打印数一致。silent-never-runs 漂移类封死成立。
- **init 编辑**：`python3 …/thesis-init/scripts/test_init.py` 全绿（exit 0），theory 目录在
  测试清单内；CONTRACT 文本区域逐行读过，相对链接（`../../thesis/template-spec.md`）
  与目录几何一致；被删的 registry/dissect-读者旧行与新设计矛盾已消除。
- `__pycache__/` 被 `.gitignore` 覆盖（:2），未入库。

---

## BROKEN（抓到的虫子——都是礼物）

### B1 — 敌意数字串抛 ValueError 穿透「不抛异常」契约 【MEDIUM】

`scripts/check_theory.py:131`（`_header_numbers` 的 `int(label.split()[1])`）、`:140`
（`_single_ref_number` 的 `int(matches[0])`）、`:222`（grounded-in 的 `{int(x) ...}`）

**What I did**：往三个互不相同的入口塞超长数字串（\d+ 贪婪捕获后进 `int()`，撞上
CPython 3.11+ 的 4300 位 str→int 上限）。四条触发路全部复现：
(a) theory-map.md 里 `## Shared <5000位>`；(b) **chapter-map.md 里 `## Chapter <5000位>`
——这是 dissect 产物、theory 自己不写的文件**；(c) shared-ref 值 `Shared <5000位>`；
(d) grounded-in 值内 `<4500位>`。

**What happened**：`ValueError: Exceeds the limit (4300 digits)` 直接冲出 `check()`、
traceback 打脸，脚本 docstring `:154` 明写「不抛异常——问题进列表」被违反。exit code
仍是 1（未处理异常退 1），fail 方向闭合——但调用方看到的是内部栈而不是问题清单，
SKILL.md Step 3 的「打印具体问题」契约破裂。最强矢量是 (b)：**任一上游 skill 的产物
损坏即可把本门砸成栈**，而 chapter-map 的完整性不在 theory 的威胁模型假设内。

**Expected**：超长数字串应解析为「无法解析」走 dangling/malformed 分支进 issue 列表。

**Reproduce**（敌意 chapter-map 一条命令砸穿 theory 的门）：
```bash
PROJ=/tmp/aries-crash && rm -rf $PROJ && mkdir -p $PROJ/sci-skills/thesis-dissect \
  $PROJ/sci-skills/thesis-theory $PROJ/thesis/tex $PROJ/sci-skills
printf '# t\ntheory-tex: chapter1.tex\nextraction-outcome: waived-by-author\n' > $PROJ/sci-skills/thesis-theory/theory-map.md
python3 -c "open('/tmp/aries-crash/sci-skills/thesis-dissect/chapter-map.md','w').write('# cm\n## Chapter '+'7'*5000+'\n')"
printf '# spine' > $PROJ/sci-skills/thesis-spine.md && printf x > $PROJ/thesis/tex/chapter1.tex
python3 /home/joe/Documents/repo/skill/sci-skills/sci-skills-thesis/skills/thesis-theory/scripts/check_theory.py \
  $PROJ/sci-skills/thesis-theory/theory-map.md $PROJ/sci-skills/thesis-dissect/chapter-map.md \
  $PROJ/sci-skills/thesis-spine.md $PROJ/thesis/tex   # → ValueError traceback, exit 1
```

**修法方向**：捕包一层有界解析——`def _int(s): return int(s) if len(s) <= 6 else None`
并在三处 `int()` 换用之（None → 按 unparseable 处理）；或把四处 `\d+` 收成 `\d{1,4}`
（章号超过 4 位必为编造）。两个家族 check 脚本共用此形，修完记得入 hardening 队列备注。

### B2 — CommonMark 合法的**带空格水平分割线不关字段窗口**（假通过形状已演示）【LOW】

`scripts/check_theory.py:45` `_SCOPE_TERMINATOR` 只认整行连续分割符（`\*{3,}\s*$` 等）。

**What I did**：entry 里放一个缺全部字段的 `## Shared 1`，随后散文行 +
`* ** *`（CommonMark 规范明列的合法 thematic break），再放四个形状完整的子弹字段。

**What happened**：伪 hr 被当作 continuation，外来四个子弹顶替缺失字段 → **✓ 通过，
exit 0**。同布局换成严格 `***` 即正确关窗 → 4 条缺失 issue。`- - -` 同样泄漏
（也是 CommonMark hr）。渲染视图与门语义分叉：人眼看到 hr 分隔的孤立注记块，门把它们
吃进上一个 entry。真攻击价值≈0（能改 baton 的人直接把字段写进 entry 更省事）——但这恰
是 R1「hr 也关窗口」要封的类，只封了一半。

**Reproduce**：
```bash
cat > /tmp/hrleak.md <<'EOF'
# t
theory-tex: chapter1.tex
extraction-outcome: confirmed

## Shared 1

编辑借用说明（无标题散文块，下一行是 CommonMark 合法 hr）：
* ** *

- component: 借来的组件
- grounded-in: [Chapter 1 §2, Chapter 2 §3]
- instantiates-framework: 借来的
- status: confirmed
EOF
# 通过（应失败）：先按上文造好其余三文件（chapter-map 两章 / spine / chapter1.tex）后跑
python3 <…>/check_theory.py /tmp/hrleak.md <cm> <spine> <texdir>   # exit 0 ✗
```

**修法方向**：分割线允许标记间空格：`(?:-{3,}\s*$|\*(?:\*\s*){2,}$|_(?:_\s*){2,})$` 形态
（保留「bullet 行带内容不误伤」性质——空格只在分割符之间出现）。

### B3 — top-level 字段重复时只读第一个，后继值永不检查（隐藏遍历串ride-through）【LOW】

`scripts/check_theory.py:101-117` `_top_level_field` 返回首个非 fence 匹配即返回。

**What I did**：三个变体。(a) 有效 `theory-tex:` 后追加
`theory-tex: ../../etc/passwd` → **静默通过（n=0）**，遍历串从未被路径守卫看见；
(b) `extraction-outcome:` 出现两次（waived 在前 + confirmed 在下）→ 第一处裁决模式，
第二处纯ignored；(c) 未加 fence 的裸 `extraction-outcome: confirmed` 示例行出现在文件
任意位置（含 entry 尾部注记行）→ 直接充当真字段值。taurus I2 只对 fence 内示例免疫，
**不加 fence 的示例行仍然live**。

**What happened**：(a) 是要点——SKILL.md 承诺「绝对路径与 `..` 遍历拒绝」，重复字段的
孪生兄弟绕过守卫且零诊断。机械后果≈无（该值唯一消费是存在性 stat，无执行面），但守卫
的可承诺性与实现不符。与 taurus M7（重复 `## Shared N` 已 booked）同类不同位：
**header 重复入了账，top-level 字段重复没有**。

**Reproduce**：settled fixture 末尾追加一行 `theory-tex: ../../etc/passwd` → gate 照常
exit 0，输出中无任何遍历相关字样（对照：单独作为值则被拒）。

**修法方向**：occurrence 计数——同名 top-level 字段 >1 处直接发歧义 issue
（mirror M7 精神：结构歧义必须 fail-noisy 或显式 bookkeeping）。

### B4 — 目录形态参数谎报「不存在」【LOW · cosmetic】

`scripts/check_theory.py:157`（tm 分支；cm/spine 同构分支同理）。

**What I did**：把 tm_path 传成一个存在的**目录**。

**What happened**：报 `✗ … 不存在（theory 未产？跑 thesis-theory）`——文件明明在，
是个目录。诊断语句为假；fail 方向仍正确闭合。作者会被误导去重跑 skill 而不是看错传参。

**Reproduce**：`mkdir /tmp/d && python3 check_theory.py /tmp/d <其余三参>` → 「不存在」。

**修法方向**：一行为差——分支里补 `is_dir()` 时改口「存在但不是文件」。低优先级、
可与 B1 同 commit 顺手带过。

---

## SURVIVED（打不动的地方——这些是真的硬）

逐条列出我实际打过的招：

1. **BOM / BOM-only / 空文件 / 纯空白 / 二进制垃圾 / CRLF 全文** —— 全部优雅降级出干净
   issue 列表或 exit 0 场景照常工作；BOM 首条目不丢（utf-8-sig 路径 + shipped test 双保险）。
2. **Header 伪造全家桶** —— `## Shared 1x`（数字粘连）、`## Shared`（无号）、`##Shared 1`
   （无空格）、`### Shared 1` / `#### Shared 1`（降级级别）、`## Shared ⁷`（上标）、
   `## Ѕhared 1`（西里尔同形字）：七种全部不被认作条目 → **vacuous-pass guard 必然开火**，
   fail-noisy。`## Shared 01` 与 `## Shared 1` 正规化到同一编号，交叉引用两侧一致。
   `## Shared 1 (...) trailing title` 合法接受（shipped test pin）。
3. **status/outcome 伪造** —— `CONFIRMED` / `Waived-By-Author ` 大小写混排按设计接受；
   零宽连接符（conf‌irmed）、CJK 句号（confirmed。）、零宽空格尾（waived-by-author​）
   全部拒绝开火——不可见字符无法伪造 author gate 痕迹。尾随空格/tab 被正规化，无误伤。
4. **ANSI 注入**（esc 序列入 echoed 值）—— `_sanitize` 剥净，shipped test 同时 pin。
5. **U+2028 / NEL / VT 类 Unicode 行分隔符走私**——结构上死路：`splitlines()` 在解析前
   就消费了这些分隔符，伪造尾巴只会变成惰性 junk 行或（若以 `##` 开头）正常的窗口终止符，
   永远到不了输出流。B5 的清洗类即使不覆盖这三个码点也无泄露面。
6. **正则回溯炸弹**——200k 字符冒号陷阱 bait、31MB / 40 万行的巨型 map：后者全流程
   2.54 秒线性完成，前者 0.01 秒。无病态回溯、无挂起、无内存爆炸迹象。
7. **fence 互相作用**——未闭合孤 fence：孤 fence 诊断 + 缺失字段 issue **同时**开火
   （fail-noisy 对）；语言后缀（``` ```python ```）/缩进 marker 在 `_split_sections` /
   `_top_level_field` / `_fences_balanced` 三处共享同一判定，行为完全一致；配平的
   balanced fence 把条目裹进代码块与 markdown 渲染语义一致（渲染器看到的代码块，门也不算
   条目——parser≠renderer 分叉不存在于此类）。
8. **路径攻击**——绝对路径、内嵌 `sub/../secret` 组合全部拒绝；NUL 字节名 / 5000 字符
   超长名经 stat 兜底优雅降级（3.13 pathlib 内吞 ValueError 落 False 也在 except 保护内）；
   tex 目录内符号链接指向外部会通过存在性检查——但该值消费仅限 stat，无读无执行，
   攻击者需要已具备项目写权限才有立足点，无边界被穿越（informational，不建议修）。
9. **CLI 状态机**——settled→0 且打印通过行；问题态→1 且逐条打印；argv[5:] 忽略；
   空 argv[1] 优雅落「不存在」exit 1；tex_dir 参数传文件不炸。除了 B1 的崩溃路径，
   退出码契约全程闭合。
10. **spine 复验**——`[pending?` 子串检测连 fence 内 / 引文内的残留也抓（over-match =
    噪声方向，镜像 check_spine 既有先例，安全侧偏差）。
11. **waived 终态两翼**——waived+Shared、waived+Overlap 矛盾双 guard 都开火
    （taurus I1 补的 Overlap 翼有 shipped test pin）；confirmed-but-empty vacuous guard
    在 outcome 合法时精准武装、outcome 缺失时由 missing-field issue 补位，无缝隙。
12. **R6 层清白**——两份 bundle script 零 eval/exec/subprocess/os.system/pickle/import 
    触点；SKILL.md 仅一处 bash 围栏（Step 3 的 4-argv 门命令），argv 全部结构性路径、
    **无一从文件内容插值**；Untrusted-content 契约覆盖每一个 skill 实际会读的文件
    （spine / chapter-map / chN.tex / template-spec / terminology-ledger / 
    **theory-map.md 自身 on resume**）——summary B7 镜像义务履行完整；没有任何
    「因文件内容改行为/跑命令」的指令性表述。references ×2 与 tests/README 的诚实边界
    陈述（near-trivial 非 depth、coverage 完整性非机械属性、disposition 不 enforce）
    与 spec §⑥ 逐条对得上，无 overclaim。

## UNTESTED（打不了的面——如实申报）

1. **prose 层 prompt-injection 依从性**——敌意 baton 散文能否诱导 agent 违反 Untrusted-content
   契约属行为评估，只有 eval loop 能测（tests/README §3 已明说归 eval）。我审的是文本：
   契约语句存在、覆盖完整、含「report verbatim and stop」升级路径；运行期依从性无法机械证明。
2. **init 流程端到端**——init_project.py 本体只审了 diff 区域文本 + test_init.py 绿灯；
   完整 scaffold 流程不在此 range 的改动面内，未重放。

---

## Verdict

**BREAKABLE — 4 bugs found（1 MEDIUM + 3 LOW），B1 须修后再 deploy**

B1（敌意数字串砸穿不抛异常契约，chapter-map 一条 5000 位章号即可远程触发 traceback）是我
在这轮找到的真礼物：修法一行、面小但脏，且 fail 噪声形态会让下一个调试的人先怀疑自己的
环境再怀疑到这。B2/B3/B4 都是防御纵深级的窗缝——排队可修，不值得单独 blocking。

值得明说的另一半：这座塔在我最想砸塌的承重墙上纹丝没动。header 伪造七连、不可见字符
伪造痕迹、Unicode 行分隔符走私、fence 三 helper 一致性、31MB 资源压强、exit-code
状态机、untrusted 读覆盖完整性——全部站着扛住了。从 check_summary.py 最硬化版起步的
继承决策被验证是对的：39 个攻击点里只有新引入 top-level fence-aware 和既存 int 解析两处
见面不一样。

---
*审计方法记录：R1/R2/R4/R5/R6 checklist 各自先行加载；全部结论出自 /tmp 下临时探针
（probe1–4 + CLI 层双项目），repo 工作树零污染（探针不入库，__pycache__ 已 ignore）。
Sibling check_summary.py 的 `_top_level_field` 同类洞按 orchestrator 指示不算新 finding
（booked for family hardening）。*

---

# Re-test — commit 0394e5f（B1+B4 修复验证，2026-08-27）

> Range 扩至 ab5a893..0394e5f。B2/B3 按 routing 留给 family hardening commit（与
> check_summary.py 同形 carry 同队列）——本次只验证 B1/B4 + 回归面。

## 修复验证（原 B1 四矢量 + B4，全部复跑）

| 矢量 | 修复前 | 修复后 |
|---|---|---|
| B1a 敌意 chapter-map（5000 位章号，CLI one-liner） | ValueError traceback | `✗ …可读但无任何 ## Chapter N 条目 — cross-ref 跳过`，exit 1，零栈 |
| B1b theory-map `## Shared <5000位>` header | ValueError | 条目号从 shared_nums 跳过，无栈（见下方残角） |
| B1c shared-ref `Shared <5000位>` | ValueError | 落 malformed 分支「无法解析单个 Shared 号」，exit 1 |
| B1d grounded-in 内 `<4500位>` | ValueError | walrus 过滤后落 `<2 个不同章` 分支，exit 1 |
| B4 目录形态 tm_path | 谎报「不存在」 | `✗ …存在但不是常规文件（目录？）`——诊断为真 |

`_int` 边界实测：6 位号两侧一致（header/交叉引用同号）→ 干净通过；7 位号 →
malformed issue。cap 选 6 位合理（章号/条目号合法域远小于此）。

## 回归面（coordinator 点名的两处 + 我加的三处）

1. **bounded parse × vacuous guard 交互**——关键澄清：`_split_sections` 的 header
   pattern 仍未封顶（`\d+`），所以**敌意编号条目照常开 entry**，不会被 `_int` 丢出
   components——vacuous guard 的武装条件（components 空）不受影响：`reg-waived-hostile-entry`
   正确开火（waived guard 抓到残留条目）、`reg-hostile-entry-empty-body` 正确开出 4 条
   per-entry 缺失 issue。丢号只发生在 `_header_numbers` 的交叉引用集合侧——设计正确。
2. **`_single_ref_number` 新 None 路径**——落点确认是 malformed-issue 分支
   （「无法解析单个…应为 'Shared N' 格式」），值经 `_sanitize` 回显，无绕过、无误吞。
3. **happy path 无回归**——settled fixture 照常 exit 0；41 个 shipped tests 全绿
   （Python 3.13.13，exit 0），新增三测试（敌意 chapter-map / 敌意 Shared header /
   目录消息 pin）在 auto-discovery 下按名收集。
4. **修复引入的新残角（如实入账，不 blocking）**——`## Shared <5000位>` 若**字段完整**
   且无 Overlap 引用它：条目照常验证、通过（n=0）。修复前该形状是崩溃，修复后是
   静默通过——崩溃换静默，方向正确（fail-silent 仅剩这一个自证垃圾的形状，且「字段
   完整 + 5000 位编号」在真实 baton 里不出现）。属 B1 修法选择（loop-skip 而非 pattern
   封顶 `\d{1,6}`）的已知角落，建议记入 family hardening 队列备注，一行可收
   （把 `_split_sections` 的 pat 也收成 `\d{1,6}` 即与 `_int` 对齐）。issue 行会把
   5000 位数字原样回显进标签——纯数字、无控制符，只是难看，无注入面。
5. **B4 范围确认**——目录分层只在主路径（tm）；cm/spine 目录参数仍报「不存在」措辞。
   coordinator 明示 scoped to primary path，与 cross-ref 依赖的容错语义一致，不复开。

## B2/B3 现状确认

- **B2**（spaced thematic break 不关窗）：复跑 PoC → 仍 n=0 通过，行为未变，
  与「queued for family hardening」的定性一致。
- **B3**（top-level 字段重复 first-wins / 隐藏遍历串）：复跑 → 仍 n=0 静默，行为未变，
  定性一致。

## 最终 Verdict

**SOLID（在 0394e5f）** — B1（MEDIUM）与 B4（LOW）修复经原矢量 + 边界 + 回归五点复测
全部成立，41 tests 绿，无新回归；遗留面 = B2/B3（LOW，已正确入队 family hardening）
+ B1 修法的一个已命名残角（同队列一行备注）。本 skill 可合并；family hardening commit
落地时带走 B2 / B3 / `_split_sections` pattern 封顶 / check_summary.py 同形 carries。
