# thesis-terms tests

1. **deterministic candidate extractor** — `scripts/scan_abbrev.py` +
   `scripts/test_scan_abbrev.py` (10 stdlib cases, run `python3 test_scan_abbrev.py`).
   Exit-code contract: 0 = 成功（含零候选——"无候选 ≠ 无缩写"，AI 补扫兜底）;
   1 = 输入错误（路径不存在/非 UTF-8，stderr 结构化消息）。
   Cases covered:
   - 模式 1 `full (ABBR)` 命中，全称窗口剥前导冠词；
   - 模式 2 定义动词句（denotes / stands for / `TCR:` 冒号形）命中；
   - 模式 3 缩写节行（`ABBR␣␣全称` / `ABBR - 全称` / `ABBR: 全称`）命中；
   - LaTeX 注释里的定义不计（`% TCR (fake)` 拒）；
   - 非缩写括号拒：`(3a)`（数字开头）、`(fig)`（大写不足）、`(Fig)`；
   - **已声明误报类钉死**：大写数字混合材料式 `(Ti3C2Tx)` 过判定成为候选
     （AI 核验滤——候选器宁滥勿缺的口径边界）；
   - 同名同全称去重留首见；同名异全称保留两行（潜在冲突信号，交作者裁决）；
   - 多文件聚合：候选带各自 source；
   - CLI `--format json` 输出对象数组；空文本 exit 0 + "无候选"提示；
   - 不存在的文件 → stderr 结构化错误 + exit 1（agent 可分辨"输入错"vs"无候选"）。

2. **the split (stated honestly)** — scanner 是机械候选器（grep-able：三类正则 +
   ABBR 判定 + 注释剥离，值得 stdlib 测试）；**AI 补扫/核验/查证与作者核验是判断活，
   不可脚本测**。译名质量（"接触热阻" vs "热接触电阻"）靠作者硬门 + 真实实例验收：
   - 验收口径：拿一篇真实小论文跑一轮——① scanner 候选齐全吗（对照人工找的）？
     ② 查证列有依据吗？③ 作者改过的译名落表了吗？④ dissect Step 0 硬门：无锚定表
     停 / 有 pending 停 / settled 放行，各验一次。

3. **decoupling assertions (programmatic)** —
   - grep: zero sibling-skill calls in thesis-terms source（对 spine/dissect 的提及
     是文件/硬停指向，不是调用）；
   - thesis-terms 只写 ledger 的 `## 缩写锚定表` 节（保留 spine seed 主表）+ 自己
     工作目录的 PDF 提取 dump；不写 `thesis/tex/`、不写 spine 产物。

**Known limitations (documented, not fixed):**

- **scanner 漏扫类（by design，AI 补扫兜底）**：反向括号形 `TCR (thermal contact
  resistance)` 不进脚本——括号后内容是真定义还是普通同位语（`XRD (Cu Kα radiation)`）
  歧义过高，误报率不划算；图注/表格内的定义、OCR 噪声、非常规写法同样靠 AI 通读兜底。
- **ABBR 判定的 FP 类**：大写数字混合（Ti3C2Tx）过判定（测试钉死为已声明行为）；
  纯小写缩写风格的领域惯用形（如 "2D"）被拒（首字符须字母）——补扫负责。
- **全称窗口的句界依赖**：`prepare` 按句切行后全称窗口不出句——`e.g.`/`Fig.` 类
  缩写点也被切行，只影响候选窗口不影响判定（无害，测试覆盖多句场景）。
- **译名质量不可脚本测**：查证列的"依据"是 AI 检索的记录，不是真相担保——作者硬门
  是唯一质量闸口（skill Rule 2）。
- **表头避词约束**：锚定表表头不得含 term/variant/canonical 子串（check_polish 的
  enforce 解析器按表头名吸表，误吸会把缩写当变体 enforce，正文中合法的缩写出现全被
  误报）。schema 已钉死表头；改表头前先读 check_polish 的 `_parse_ledger`。

TODO: scaffold evals.json + run the full eval loop per skill-creator-plus before ship.
