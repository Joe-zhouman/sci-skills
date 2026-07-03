# sci-skills

Claude Code skills for scientific research workflows.

## Philosophy

These skills are tools, not magic. Every workflow is designed for **human-in-the-loop** operation: the skill produces a draft, the human reviews it, and iteration drives quality. We don't pretend anything is fully automated — because real scientific work never is. The human decides when it's good enough.

## About this series

Every skill in this repo is developed following the testing workflow defined by [skill-creator-plus](https://github.com/Joe-zhouman/skill-creator-plus). All test records (evals, iterations, benchmarks, grading) are preserved under each skill's `tests/` directory.

skill-creator-plus mirrors:
- GitHub: <https://github.com/Joe-zhouman/skill-creator-plus>
- Gitee: <https://gitee.com/Joe-zhouman/skill-creator-plus>
- GitCode: <https://gitcode.com/Joe-zhouman/skill-creator-plus>

## Skills

| Skill | Description |
|-------|-------------|
| [sci-draw](skills/sci-draw/) | Publication-quality scientific data visualization — statistical plots, multi-panel figures, heatmaps, dose-response curves, and more |

## Templates

LaTeX templates for manuscript projects — copy what you need into your working directory. `main/` includes a full build pipeline (`make`), cross-reference auto-numbering, and structural best practices from a published paper.

```
templates/
├── cover_letter/
├── main/          ← manuscript + supplementary + build chain
└── response/      ← point-by-point review reply
```

## Structure

Skills live under `skills/<name>/`. Templates live under `templates/`.

## Installation

Two branches are available:

| Branch | Purpose |
|--------|---------|
| [`release`](https://gitcode.com/Joe-zhouman/sci-skills/-/tree/release) | Clean distribution — no test workspace artifacts. **Use this to install skills.** |
| [`master`](https://gitcode.com/Joe-zhouman/sci-skills) | Full development history — includes all test records under `tests/workspace/`. For contributors. |

```bash
git clone -b release git@gitcode.com:Joe-zhouman/sci-skills.git
```
