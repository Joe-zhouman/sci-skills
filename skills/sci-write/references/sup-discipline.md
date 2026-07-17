# Supplementary Information — 写作过程中逐步累积

SI 不是正文写完了再想"还有什么没放"——是在写作过程中被砍下来的内容逐步形成一份清单。正文定稿后，清单→SI 文档。

## 公园清单

写作过程中，每砍掉一件东西，立刻加到 `sci-skills/sci-write/sup-list.md`：

```markdown
# Supplementary Information — 待装入

## 补充图
- [ ] figX — [conclusion] — 原因：[weak claim / 支撑同一 claim 的重复图 / 锦上添花]
- [ ] ...

## 补充方法
- [ ] [方法环节名] — [为什么正文放不下：太长 / 非核心 / 仅特殊情况需要]
- [ ] ...

## 补充表
- [ ] ...

## 补充讨论（不鼓励——绝大多数论文不需要这个）
- [ ] ...

## 补充说明 (Supplementary Note)
- [ ] [Note 标题] — 来源：[Results 段落 / 叙事流放不下] — 摘要：[一句话]
- [ ] ...
```

每次砍东西都追加到这个文件。文件不存在就 create。正文还没定稿就不组装——继续往里堆。

## 哪些东西进 SI

| 来源 | 触发条件 | 动作 |
|---|---|---|
| **科学写作** — paper-plan 自检 | 图的 conclusion 列得出来但 claim 牵强 | 加到"补充图"，标注原因 |
| **科学写作** — paper-plan 自检 | 两张图的结论重叠 | 图保留，另一张标记为"补充图——figX 的验证/补充视角" |
| **科学写作** — Method | 非方法学论文，方法细节正文放不下 | 加到"补充方法"，简述正文留了什么、这里补什么 |
| **科学写作** — Method | 理论推导 / 完整参数列表 / 辅助性 protocol | 加到"补充方法" |
| **科学写作** — Results | 有数据、有结论、但放不进正文叙事流 | 加到"补充图"（如果以图为主）或"补充说明"（如果是文字结果段落） |
| **科学写作** — Results | Results 段落被砍——conclusion 对但不是核心叙事线的必要环节 | 加到"补充说明"——段落级文字，不是图。把原段落的结论转成一段独立叙述 |
| **用户主动** | 用户说"这个放 SI" | 不判断，直接加 |

## 哪些东西**不进** SI

| 不进 | 为什么 |
|---|---|
| 正文里砍掉的弱 claim（conclusion 和 claim 都列不出来） | 直接砍。SI 不是垃圾场。 |
| 正文已经说清的方法 | 不重复——读者不需要在两个地方读同一段 |
| 正文没有的数据、没有的图 | SI 只能用已有的材料——不制造新图新数据 |
| 正文里"因为审稿人可能会问所以先藏着"的东西 | 这种逻辑等于承认正文不完整。把东西放回正文。SI 是溢出，不是避难所。 |

## 组装（si-export 阶段）

正文 tex 编译通过后，读 `sup-list.md`，按以下结构组装 `manuscript/vN/tex/sup.tex`：

```
\beginsupplement
\tableofcontents

% === 补充图在前 ===
\section{Supplementary Figures}
% 每图一页，图来源指向 figN.png/pdf（已经在图仓库）
% caption 来自 figN-report.md 的 Core conclusion

% === 补充表 ===
\section{Supplementary Tables}

% === 补充方法 ===
\section{Supplementary Methods}

% === 补充说明（Results 砍下来的文字结论段落） ===
\section{Supplementary Note}
% 每段一个被砍的 Results 结论，转成独立叙述

% === 补充讨论（如果有——极少） ===
\section{Supplementary Discussion}

% === 补充参考文献 ===
\printbibliography[title=Supplementary References]
```

SI 不独立编译——它是 `main.tex` 的一部分（`\include{sup}`）。
