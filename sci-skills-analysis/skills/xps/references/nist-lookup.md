# NIST 结合能查询细则

正文 §1.2 给了查询命令。这里展开：怎么读查询结果、Quality 怎么权衡、什么时候去 live NIST 复核。数据源是 NIST XPS Database (SRD 20)，55,948 条记录，via KherveDB 2019 snapshot。

## 两种输出模式

结果数 > limit（默认 200）时脚本自动进 **summary 模式**：按 (Element, Line, Formula) 分组，每组给 `be_mean`/`be_std`/`be_count`/`be_min`/`be_max`/`top_quality`/`top_author`/`top_journal`。结果数少时是 **raw 模式**：逐条记录，带完整引用。

- 想知道"某个化学态 BE 大概在哪"→ 看 summary 的 `be_mean`，优先 `top_quality=Good` 的组。
- 想要某条具体文献的支持 → 用 `--limit` 拉高或缩小 `--range` 进 raw 模式，看每条的 Author/Journal/Quality。

## 字段怎么用

- `be_mean`：该化学态的 BE 中心，做峰位种子。
- `be_std`：文献间离散度。std 大（>0.5 eV）说明该化学态 BE 本身就模糊（基体效应、荷电不同），峰位约束别卡太死。
- `be_count` (n)：支持该值的记录数。n 大 = 可信；n=1-2 = 孤证，慎用。
- `top_quality`：`Good` > `Adequate`。能用 Good 就别用 Adequate 做关键指认。

## 查询策略

- **先查元素 + 轨道 + 能量范围**（`Si --line 2p --range 97 107`），看这个区域可能有哪些化学态。
- **按化合物查**（`-s Si3N4`）确认目标相的 BE，做硬约束锚点。
- **多元素交叉**：Si₃N₄ 体系同时查 Si 2p 和 N 1s，两边的 BE 要互相印证。

## 基体效应（重要）

NIST 的 BE 来自各种材料体系，**同一化学态在不同基体里能差 0.5–1.0 eV**。查到候选后，优先选与你样品体系最接近的文献，别直接套用无关体系的值。这也是为什么峰位要给 `center_range` 而不是锁死在 `be_mean`。

## 发表前必复核

本地库是 2019 snapshot，不全且不更新。<HARD-GATE>发表论文前必须在 https://srdata.nist.gov/xps/ 用同样的查询条件复核一遍，确认峰位指认有现行文献支持。</HARD-GATE>
