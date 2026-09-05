# thesis-dissect tests

Test plan (run via skill-creator-plus eval loop before deployment):

1. **deterministic coverage + 零丢弃缺席 gate** — `scripts/check_dissect.py` (the gate) +
   `scripts/test_check_dissect.py` (32 stdlib cases, run `python3 test_check_dissect.py`).
   Exit-code contract: 0 = 通过; 1 = issues (each printed).
   Cases covered:

   **coverage 层（v1 原有）**
   - passes on a settled chapter-map.md + its tex files (2 chapters, all fields
     filled, status=written);
   - fails on a missing `framework-instantiation` (field absent);
   - fails on an empty `framework-instantiation` (value = `none`);
   - **passes when ch1 `progression-in=none`** — load-bearing: ch1 has no prior
     chapter, so `none` is the settled value, not a gap
     (`test_ch1_progression_in_none_ok` is the proof);
   - fails on a non-ch1 chapter missing `progression-in` (ch2 set to `none`);
   - **passes when last chapter `progression-out=none`** — load-bearing: the last
     chapter has no next chapter, so `none` is settled, not a gap
     (`test_last_chapter_progression_out_none_ok` is the proof);
   - fails on a non-last chapter missing `progression-out` (ch1 set to `none`);
   - fails on `status=pending` (unsettled — chapter not yet written);
   - fails on `status=stale` (backtrack-spine marked it — coverage must fail,
     dissect can't hand off a stale chapter);
   - fails on a missing tex-file (chapter references `ch1.tex` but it's absent
     from `thesis/tex/`);
   - fails on a missing `tex-file` field (no `- tex-file:` line at all);
   - passes when all referenced tex files exist (no tex-file issues);
   - fails on a missing `chapter-map.md` (dissect not yet run);
   - graceful on a binary/non-utf8 `chapter-map.md` — must not raise, returns
     a UTF-8 issue string.

   **零丢弃缺席 + 章形签名层（v2 新增——用户真实实例反馈的机械防线）**

   用户跑了真实小论文→章节转化，产出"毫无意义的实验报告"：模块合并形同虚设
   （机械拆分 Methods/Results）、章引与讨论缺失、SI 被整体丢弃。v2 的 fixture
   全部升级为合规章形（章引→模块→本章讨论→本章小结）+ 合规 trace（SI/讨论清单
   去向落位），负向用例每次只破坏一处：
   - `test_passes_on_compliant_shape` — 合规基线整体 pass（负向用例的对照）;
   - fails on IMRaD `\section{方法}` + `\section{结果}`（机械拆分形态，实测失败的主形态）;
   - **整标题等值匹配不误伤**——"XX 的合成与表征"类模块标题（干什么的名词化）不报 IMRaD;
   - fails on a missing `paper-X/trace.md`（素材未清点，零丢弃无法审计）;
   - fails on an SI 清单条目去向仍为 `→ pending`（章收尾后不允许残留）;
   - fails on a 讨论素材清单条目缺去向箭头（未落位）;
   - **passes with `无 SI` 声明**——不是每篇论文都有 SI，显式声明替代清单;
   - fails when trace 既无 SI 清单节也无"无 SI"声明;
   - fails on a missing 本章讨论 section（discussion 是每篇论文的精髓，独立成节）;
   - fails when the last section is not 本章小结（收束章问题+递进缺失）;
   - fails on a missing 章引（\chapter 直跳 \section、首节非"引言"）;
   - **passes when the chapter opens with `\section{引言}`**（章引等价节名逃逸口径）;
   - merged papers（同一 paper 出现在两章）→ trace 只查一次（issue 不重复计数）。

2. **the split (spec §⑧, stated honestly)** — coverage/缺席是 deterministic
   (grep-able: chapter-map 字段、trace 清单行的 `→ 去向` 与 `pending` token、tex
   `\section` 标题等值匹配、讨论/小结/章引节存在性), so it earns a runnable stdlib
   test — mirroring spine's justified deviation (deterministic code + verifiable
   outputs). Prose is NOT script-tested: the 拆即写 (dissect-is-write) workflow's
   judgment — in-write restructure grounding (claim-evidence hanging), 三拍顺序
   (干什么→怎么做→做了什么)、讨论按问题组织、章引提问题的质量、SI 并入落点好不好 —
   is evaluated via skill-creator-plus's eval loop + post-module gate, not here.

   **真实实例反馈（eval 证据源）**：本轮 v2 重构的直接动机是用户的真实实例评审
   （三个缺陷：机械拆分/无章引讨论/SI 丢弃）。reference（restructure-discipline.md）
   的章形、素材去向总表、三拍纪律、SI 并入规则由下一轮真实实例（写一章走 post-module
   gate）验收——章形质量、讨论独立性、SI 并入落点是人审项，脚本只防缺席。

3. **decoupling assertions (programmatic)** —
   - grep: zero sibling-skill calls in thesis-dissect source
     (no `from thesis-spine` / `import thesis-…` in `scripts/` or `SKILL.md`;
     the `thesis-spine.md` / `thesis-sources.md` mentions are file-path reads,
     not Python imports);
   - dissect writes `thesis/tex/chN.tex` + `sci-skills/thesis-dissect/chapter-map.md`
     + `sci-skills/thesis-dissect/paper-X/` notes (its own working dir,
     NOT into `thesis-spine/`);
   - dissect reads spine's `thesis-spine.md` (the baton) but never writes it;
     same for `thesis-sources.md` + `template-spec.md` (thesis-init's, read-only).

**Known limitations (documented, not fixed):**

- **IMRaD 词表是整标题等值匹配，不是包含匹配**（escape hatch by design）：`结果与讨论`
  会被 IMRaD 检查拦下，但 `表征与讨论` 这类含"讨论"的混合词不拦 IMRaD 也不算缺讨论节
  （containment 判定"讨论"存在）。极窄的逃逸窗口：一个真机械拆分的章恰好用了含"讨论"
  的节名且不含 IMRaD 全词——真实形态几乎总是"方法/结果"裸词，已覆盖主形态。
- **章引检查是启发式**：`\chapter` 与首个 `\section` 之间实质字符 <80（剥命令/注释后）
  且首节名非"引言"类才拦。模板把章引放 main.tex（章文件无 `\chapter`）时不查章引——
  逃逸方向是"漏报"而非"误报"（不冤枉合规章）。
- **trace 清单行的 schema 依赖**：清单行必须是 `- 条目 → 去向` 格式（去向含 `→` 或
  `->`，`pending` token 拦截）。这是 SKILL.md trace 模板钉死的格式；自由散文式 trace
  不被识别为已落位——保守方向（fail-noisy），不会漏放未落位的条目。
- **markdown code-fence handling（aries round-2）**：`split_chapters` skips `## Chapter N`
  headers inside ``` fences, but `~~~` tilde fences and nested 4-tick fences are NOT
  handled — fires only on out-of-schema maps (the schema is flat field-list markdown,
  dissect never produces code blocks). Conservative direction: fails only on malformed
  input, never false-blocks a valid settled map.
- **tex 注释剥离是 naive 的**（`\%` 保护后按行砍 `%` 起）——verbatim 环境里的 `%` 会被
  误当注释。方向性影响：可能多剥出更短的章引正文（更倾向拦）而非漏拦；gate 消息给出
  明确修复指引，误拦可从消息直接定位。

TODO: scaffold evals.json + run the full eval loop per skill-creator-plus before ship.
