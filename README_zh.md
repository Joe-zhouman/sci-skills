# sci-skills

面向科研工作流的 Claude Code 技能集合。

## 核心理念

这些 skill 是工具，不是魔法。每个工作流都围绕**人的介入**设计：skill 产出草稿，人来审查，通过迭代提升质量。我们绝不吹嘘"全自动化流程"——真正的科研工作从来不是全自动的。什么时候算够好，由人说了算。

## 关于本系列

本仓库中的每一个 skill 均严格按照 [skill-creator-plus](https://github.com/Joe-zhouman/skill-creator-plus) 定义的测试流程开发。所有测试记录（evals、迭代、benchmark、评分）均保存在各 skill 的 `tests/` 目录下。

skill-creator-plus 镜像仓库：
- GitHub: <https://github.com/Joe-zhouman/skill-creator-plus>
- Gitee: <https://gitee.com/Joe-zhouman/skill-creator-plus>
- GitCode: <https://gitcode.com/Joe-zhouman/skill-creator-plus>

## 技能列表

| 技能 | 说明 |
|-------|-------------|
| [sci-draw](skills/sci-draw/) | 投稿级科研数据可视化——统计图、多面板组合图、热图、剂量反应曲线等 |

## 模板

LaTeX 稿件模板——直接复制到工作目录即可使用。`main/` 包含完整编译管线（`make`）、交叉引用自动编号和来自已发表论文的结构最佳实践。

```
templates/
├── cover_letter/
├── main/          ← 正文 + 补充材料 + 编译链
└── response/      ← 逐条审稿回复
```

## 目录结构

Skills 位于 `skills/<name>/`。模板位于 `templates/`。

## 安装方式

本仓库提供两个分支：

| 分支 | 用途 |
|--------|---------|
| [`release`](https://gitcode.com/Joe-zhouman/sci-skills/-/tree/release) | 干净分发版，不含测试工件。**安装 skill 请用这个分支。** |
| [`master`](https://gitcode.com/Joe-zhouman/sci-skills) | 完整开发历史，含 `tests/workspace/` 下所有测试记录。供开发者使用。 |

```bash
git clone -b release git@gitcode.com:Joe-zhouman/sci-skills.git
```
