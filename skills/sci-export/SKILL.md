---
name: sci-export
description: >-
  导出 / Export — convert drafted content into manuscript tex, and polished manuscript
  into Word (DOCX) for collaborators. Manual only. 手动触发。md→tex, tex→docx.
---

# sci-export

Two export modes. Both manual — the human decides when content is ready to move.

## Layout & boundaries

```
<project-root>/
  manuscript/
    v1/tex/             ← TARGET: md→tex writes here (sections/ + main.tex)
  sci-skills/
    sci-write/          ← SOURCE: md drafts (intro, discussion, abstract, method, results, conclusion)
  templates/main/       ← READ-ONLY: reference tex blueprint (structure, preamble, Makefile)
```

- **Reads `sci-skills/sci-write/`** — md content drafts.
- **Reads `templates/main/`** — reference tex structure, not a mandatory template.
- **Writes to `manuscript/vN/tex/`** — the human tells you which round (v1 default).
- **Does not write to `sci-skills/`.** Output goes to the manuscript, not to intermediate storage.
- **Does not import code.**

## Startup

1. **Which mode?** Ask: "Export md drafts into manuscript tex, or convert polished tex to Word?"
2. **Which round?** Check `manuscript/v1/`, `manuscript/r1/` etc. Default: `v1`.
3. **Which content?** Read `sci-skills/sci-write/` — which md files exist? Skip what's not there.
4. **Which template?** Read `templates/main/tex/` as reference. Ask user: "Use this as template, or do you have your own?"

## Mode 1: md → tex

Transfer drafted content from `sci-skills/sci-write/` into `manuscript/vN/tex/`.

### Step 0：选择策略

两种策略，问用户选哪个：

| 策略 | 做法 | 适合 |
|---|---|---|
| **模板嵌入** | 复制 `templates/main/tex/` 到 `manuscript/vN/tex/`，把 md 内容按段落嵌入各 tex section 文件 | 从头建的稿 |
| **增量填充** | `manuscript/vN/tex/` 已有骨架，只把 md 对应段落写进已有的 tex 文件 | 已有 tex template、只需补内容 |

### Step 1：按章节搬运

| md 来源 | tex 目标 | 怎么搬 |
|---|---|---|
| `intro.md` | `tex/sections/introduction.tex` | 全文搬。Introduction 已经是漏斗结构，不需要拆。 |
| `method.md` | `tex/sections/method.tex` | 全文搬。Method 的三段式（motivation/mechanism/role）直接对应 tex 结构。 |
| `results.md` | `tex/sections/results.tex` | 按段落拆——每张图一个 subsection。段落首句做 subsection title。 |
| `discussion.md` | `tex/sections/discussion.tex` | 全文搬。第一段已经是 Conclusion，不重复搬。 |
| `abstract.md` | `tex/sections/abstract.tex` | 全文搬，加 `\begin{abstract}` / `\end{abstract}`。 |
| `conclusion.md` | 不单独搬 | Discussion 第一段已融合——不重复搬 `conclusion.md`。 |

**搬运纪律：**
- 把 md 的 markdown 语法转为 LaTeX：`**bold**` → `\textbf{bold}`，`*italic*` → `\textit{italic}`，`Fig N` → `Figure~\ref{fig:figN}`，`[DOI: ...]` → `\cite{key}`（留 placeholder，实际的 bib key 让人填）。
- `\ref{fig:figN}` 的 figN 从 `paper-plan.md` 的图编号取。
- 统计数字不改、术语不改、claim 不改——这是搬运，不是改写。

### Step 2：编译

```bash
cd manuscript/vN/tex && make
```

编译不过 → 报错定位 → 修 → 重新编译。最多三轮。三轮不过 → 把编译错误列给人，人工修。

### Step 3：编译通过后，提醒人

> "md 内容已搬到 `manuscript/vN/tex/`，编译通过。接下来的活是你的：Zotero 插正式引用、调格式、补图表文件。润色时用 polish skill。"

## Mode 2: tex → docx

Convert polished manuscript tex to Word for collaborators who don't use LaTeX.

### 前置

`manuscript/vN/tex/` 必须编译通过（PDF 能生成）。不通过 → 先修。

### 转换

```bash
pandoc manuscript/vN/tex/main.tex \
  -o manuscript/vN/manuscript.docx \
  --from=latex \
  --to=docx \
  --bibliography=manuscript/vN/tex/bibliography.bib \
  --citeproc \
  --resource-path=manuscript/vN/figures/
```

pandoc 不可用 → 提醒安装：`conda install pandoc` 或 `apt install pandoc`。

### 转换后检查

打开 `manuscript/vN/manuscript.docx`，快速扫一遍：
- 标题和作者在不在？
- 图有没有丢？
- 引用有没有变成问号？
- 公式有没有烂掉？

有问题 → 标注，输出时告诉用户。没大问题 → 这就是可以发给合作者的初稿。

### 提醒

> "Word 初稿在 `manuscript/vN/manuscript.docx`。这是机器转换的，格式需要人工调。不要把 docx 当最终稿——最终稿永远在 tex。"

## Boundaries

- **不润色。** 搬运过程中不改进语言——那是 polishing stage 的活。
- **不画图。** 不生成新 figure，不调整 figure 内容。
- **不插正式引用。** DOI placeholder 保持 placeholder 格式——Zotero 插入是人的活。
- **不写内容。** 只搬已有 md，不新写任何段落。

## Privacy

不在 tex 文件和 docx 文件里泄漏私人本地路径。
