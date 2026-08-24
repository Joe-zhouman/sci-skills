# template-spec — generic-test (minimal test pack)

> 这份文件是契约（contract）。thesis-init 读它把模板织进 thesis/tex/；各 thesis skill
> 读它对齐文件命名。真实大学模板包（清华 thuthesis 等）按同一 schema 后续收集。

## 这个模板是什么
最小可编译的学位论文模板，用于验证 init 的模板织入机制。用原生 `report` 文档类，
不依赖任何大学 .cls。真实投稿应换成本校模板包（templates/thesis/<school>/）。

## 文件命名约定（各 skill 读这条对齐）
- 章文件：`chapterN.tex`（N 从 0 起：chapter0=绪论，chapter1=理论方法，chapter2+=正文，末章=总结）
- 参考文献：`refs.bib`
- 主文件：`main.tex`（含 preamble + `\input{chapterN}` 织入各章）

## 编译
xelatex main.tex → bibtex main → xelatex main.tex ×2

## 前置/后置页（typeset skill 读这条组织）
- 前置：封面、原创性声明、中英文摘要、目录（本最小包省略，真实包按校规）
- 后置：致谢、攻读成果、作者简介（占位，作者手填）
