#!/usr/bin/env python3
"""init_project.py — sci-skills 家族项目初始化 / 迁移 / 体检。

手动触发的厚编排入口 sci-skills-init 的执行载体。一次性干完三件重活就退：
不持续运行、不自动推进日常图→文流程（那是人手动用各执行 skill）。

三个子命令:
    init      在 cwd 建 sci-skills/ 骨架（预建全部兄弟子目录）+ git init + .gitignore
    migrate   检测老 <root>/sci-draw/（不在 sci-skills/ 下）→ 迁到 sci-skills/sci-draw/
    checkup   体检：扫描当前结构，报告各 skill 落盘是否在正确位置，发现错位提示修正

哲学（与整个家族一致）:
- 幂等：重复跑不破坏已有内容。已存在的目录/文件跳过，不覆盖。
- 不自动改用户数据：migrate 默认 dry-run，要 --apply 才真迁。
- 纯 stdlib，无外部依赖。

用法:
    python init_project.py init [--no-git]
    python init_project.py migrate [--apply]
    python init_project.py checkup
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

# 家族顶层目录名（固定，有辨识度）
FAMILY_ROOT_NAME = "sci-skills"

# 预建的兄弟 skill 子目录（与仓库 skills/ 下的 skill 对齐）。
# 列表随 skill 成熟度演化——只预建设计已定的。sci-polish 待定，暂不预建。
BROTHER_SKILLS = ["sci-draw", "sci-write", "sci-submit"]

# 每个子目录的引导文件内容（.README.md，点开头=隐藏，给人看，也帮 git 跟踪空目录）。
# 关键定位：**这些 .README.md 本身就是目录级接口契约**——任何 agent / 任何 skill
# 拿到这份文件，就知道往这个目录放什么、按什么 schema、谁会读。照着契约就能产出
# 合规产物，不需要知道是哪个 skill 在用、不需要 import 任何东西。这是解耦的落地。
# 三件事都说清：这个文件夹代表什么 / 有什么用 / 产物怎么放进来（含 schema + 命名 + 来源）。
SKILL_DIR_GUIDES: dict[str, str] = {
    "sci-draw": """# sci-draw/ — 图仓库（figure warehouse）

> **这份文件是契约（contract）。** 任何 agent / 任何 skill 往本目录产出图，
> 都必须遵守下面的 schema 和命名。不需要知道下游是谁、不需要 import 任何东西——
> 照契约产出，下游自动能消费。图可以来自任何来源（sci-draw、别的 skill、手工、复制），
> 落到本目录后一律平等。

## 这个文件夹是什么
家族布局里约定的**中性图存储区**。名字借 sci-draw skill 的辨识度，但语义中性：
任何来源的成品图和它们的 report 都落在这里。下游 skill（sci-write 等）只认这里的
文件契约，**不关心图是谁画的、怎么画的**。

## 有什么用
- 存放论文用到的全部 figure 及其结构化 report。
- 作为画图阶段和写作阶段之间的**唯一交接面**：画图的把成品放这，写作的从这读。
- 跨 session 接力：画图可能在一个 session 完成，写作在另一个 session 读这里的文件继续。

## 文件怎么放进来（命名约定）
每张图一组文件，统一 `figN` 前缀（fig1, fig2, ...）：
- `figN-report.md` — **契约文件，下游必读**。六段 markdown：
  `## Core conclusion` / `## Data source` / `## Chart type & rationale` /
  `## Statistical methods` / `## Key findings` / `## Journal specs`
- `figN.png` — 导出预览（下游图义核查喂给 paper-figure 视觉工具用）
- `figN.pdf` — 矢量投稿版
- `figN.py` — 若脚本生成，留可复现脚本（可选）
- `figN-description.md` — 画图过程草稿（可选，下游不读）

## 不同来源怎么落进来
- **sci-draw skill 画的**：它直接按上述命名落到本目录。
- **别的画图 skill**：同样按命名约定落到本目录即可。
- **手工工具**（Excel/Origin/GraphPad/Illustrator）：导出 png/pdf 后，**手动复制到本目录**，
  并手写或让 sci-write 帮你补一份 `figN-report.md`（至少补 Core conclusion 和 Statistical methods）。
- **从已发表文献截图**（合规前提下）：同上，复制进来 + 补 report。
- **复制粘贴**：直接放进本目录，补 report。

不论来源，落到本目录后**一律平等**——下游只验证文件存在 + report 字段齐，不追问出身。

## 谁读它
sci-write（读 report 写正文、读 png 做图义核查）；人（看图、改图）。
""",
    "sci-write": """# sci-write/ — 写作产物（data-driven manuscript）

> **这份文件是契约（contract）。** 本目录的产物（paper-plan / data-profile /
> figN-reading / 四章正文）按下面的 schema 落盘。任何读这些文件的 agent/skill
> 按此 schema 解析；任何产这些文件的（当前是 sci-write，未来可能是别的）按此 schema 产出。

## 这个文件夹是什么
sci-write skill 的家。存放数据驱动的写作产物：论文规划接力棒、数据画像、
图义核查记录、四个数据驱动章节（Method/Results/Discussion/Conclusion）的正文。

## 有什么用
- 承载"数据 → 图 → 正文"流水线的**写作阶段**全部输出。
- `paper-plan.md` 是跨 session 的接力棒，记录哪张图画了没、哪节写了没。
- Introduction/Abstract/Keyword **不在这里**（它们标 `external`，由别的模式续写，
  读这里的文件作为输入）。

## 文件清单
- `paper-plan.md` — **接力棒**。图清单（每图 topic/claim/data-source/status）+ 章节进度。
  sci-write Step 1 起草、人确认后落盘；后续每次回来先读它。
- `data-profile.json` — 数据画像。Step 0 由 sci-write 调 profile_data 产出，喂给 Method。
- `figN-reading.md` — 每张图的图义核查记录。Step 3 产出（paper-figure 视觉描述 vs claim 对照）。
- `method.md|tex` / `results.md|tex` / `discussion.md|tex` / `conclusion.md|tex`
  — 四个数据驱动章节。格式（md/tex）每次写前问人。

## 产物怎么进来
- **本 skill 自己产**：paper-plan / data-profile / figN-reading / 四章正文，全由 sci-write 写。
- **从图仓库读**（不复制进来）：sci-write 读 `../sci-draw/figN-report.md` 和 `figN.png`，
  但**不把它们复制进本目录**——图仓库是图的唯一存放点，避免双份不同步。
- **人手动**：人可以直接编辑这里的任何 md/tex（修订、补术语）。

## 谁读它
人（读/改正文）；未来的润色/投稿 skill（读正文做后续）；external 章节续写者
（读 paper-plan + 四章作为 Introduction/Abstract 的输入）。
""",
    "sci-submit": """# sci-submit/ — 投稿产物（submission）

> **这份文件待补全为契约。** sci-submit 设计确定后，本文件补全 schema，
> 成为目录级接口契约（同 sci-draw/、sci-write/ 的性质）。

## 这个文件夹是什么
sci-submit skill 的家。存放投稿相关产物：cover letter、revision response、
workflow-tracking 记录等。

## 有什么用
- 承载"写完正文 → 投稿"阶段的相关文件。
- 跟踪投稿工作流（哪个版本投了哪、审稿意见、修回进度）。

## 文件（按 sci-submit 设计填充）
- cover letter（首投 / 修回）
- response to reviewers
- 投稿追踪记录
- 其他投稿辅助材料

## 产物怎么进来
- **本 skill 自己产**：sci-submit 生成 cover letter / response 等。
- **从 sci-write 读**（不复制）：读 `../sci-write/` 的正文了解论文内容，但正文不复制进来。
- **人手动**：投稿追踪、期刊反馈等人工内容。

## 谁读它
人；本 skill 在设计中，文件清单会随设计确定后回填。
""",
    "sci-polish": """# sci-polish/ — 润色（预留，策略待定）

## 这个文件夹是什么
**预留目录**。sci-polish skill 还在设计中，本文件**不预设其策略**。

## 当前状态
- sci-polish 落盘策略未定（可能直接在 sci-write/ 正文上改 + 靠 git 留痕，
  也可能独立落盘——等你设计确定）。
- 在策略定之前，这个目录可以忽略或删除。

## 等策略定后
- 回填本文件（这个目录是什么 / 有什么用 / 产物怎么进来）。
- 若决定不占独立目录，删掉本目录即可。

Owner: sci-polish（设计确定后）。
""",
}

# 科研项目常见忽略项（init 时写入 .gitignore）
GITIGNORE_LINES = [
    "# Python",
    "__pycache__/",
    "*.py[cod]",
    "*.egg-info/",
    ".venv/",
    "venv/",
    "",
    "# Data (large / regenerable — 按需调整)",
    "*.csv.gz",
    "*.parquet",
    "",
    "# OS / editor",
    ".DS_Store",
    "Thumbs.db",
    ".idea/",
    ".vscode/",
    "",
    "# sci-skills intermediate (按需保留或忽略)",
    "*.png.tmp",
]


# ----------------------------- helpers -----------------------------


def find_project_root(start: Path | None = None) -> Path:
    """项目根 = cwd 或 start。家族布局不强制在 git 根，
    就用调用者所在目录作为项目根。"""
    return Path(start) if start else Path.cwd()


def family_root(project_root: Path) -> Path:
    return project_root / FAMILY_ROOT_NAME


def is_git_repo(path: Path) -> bool:
    return (path / ".git").is_dir()


def has_gitignore(path: Path) -> bool:
    return (path / ".gitignore").is_file()


# ----------------------------- init -----------------------------


def cmd_init(args: argparse.Namespace) -> int:
    root = find_project_root()
    fam = family_root(root)
    report: list[str] = []

    # 1. 家族顶层
    if fam.exists():
        report.append(f"✓ {fam.name}/ 已存在（跳过创建）")
    else:
        fam.mkdir(parents=True)
        report.append(f"✓ 创建 {fam.name}/")

    # 2. 预建兄弟子目录 + .README.md（点开头=隐藏；给人看的引导文件，
    #    说明这个目录归谁、放什么；也帮 git 跟踪空目录。比 .gitkeep 有意义。）
    for skill in BROTHER_SKILLS:
        skill_dir = fam / skill
        guide = skill_dir / ".README.md"
        if skill_dir.exists():
            if not guide.exists() and skill in SKILL_DIR_GUIDES:
                # 目录在但缺引导文件 → 补一份（不覆盖已有内容）
                guide.write_text(SKILL_DIR_GUIDES[skill], encoding="utf-8")
                report.append(f"  - {skill}/ 已存在，补 .README.md")
            else:
                report.append(f"  - {skill}/ 已存在（跳过）")
        else:
            skill_dir.mkdir()
            guide_text = SKILL_DIR_GUIDES.get(
                skill, f"# {skill}/\n\nReserved for the {skill} skill.\n"
            )
            guide.write_text(guide_text, encoding="utf-8")
            report.append(f"  - 创建 {skill}/ + .README.md")

    # 3. .gitignore
    if has_gitignore(root):
        report.append("✓ .gitignore 已存在（不覆盖，建议手动核对忽略项）")
    else:
        (root / ".gitignore").write_text(
            "\n".join(GITIGNORE_LINES) + "\n", encoding="utf-8"
        )
        report.append("✓ 创建 .gitignore")

    # 4. git init
    if is_git_repo(root):
        report.append("✓ .git/ 已存在（跳过 git init）")
    elif args.no_git:
        report.append("· 跳过 git init（--no-git）")
    else:
        try:
            subprocess.run(
                ["git", "init"], cwd=root, check=True,
                capture_output=True, text=True,
            )
            report.append("✓ git init")
        except FileNotFoundError:
            report.append("⚠ git 未安装，跳过 git init（请手动 git init）")
        except subprocess.CalledProcessError as e:
            report.append(f"⚠ git init 失败: {e.stderr.strip()}")

    # 5. 写一份 family-layout 自述（让任何人/skill 进来秒懂布局）
    readme = fam / "README.md"
    if not readme.exists():
        readme.write_text(
            f"# {FAMILY_ROOT_NAME}/\n\n"
            "The sci-skills family on-disk workspace. Each subdirectory is one skill's home.\n"
            "Figures, prose, plans — all live under here. See the skill's own SKILL.md for what it reads/writes.\n\n"
            "## Subdirectories\n"
            + "\n".join(f"- `{s}/` — " for s in BROTHER_SKILLS)
            + "\n\n## Convention\n"
            "- Skills read neighbors' on-disk outputs; they never import each other's code.\n"
            "- Figures (in `sci-draw/`) can come from any source — a skill, a manual tool, a copy-paste.\n"
            "- The human advances the pipeline; nothing auto-runs.\n",
            encoding="utf-8",
        )
        report.append(f"✓ {FAMILY_ROOT_NAME}/README.md")

    print(f"init @ {root}\n" + "\n".join(report))
    return 0


# ----------------------------- migrate -----------------------------


def find_legacy_sci_draw(root: Path) -> Path | None:
    """检测老的 <root>/sci-draw/（不在 sci-skills/ 下）。
    返回老路径或 None。"""
    legacy = root / "sci-draw"
    if legacy.is_dir() and legacy != family_root(root) / "sci-draw":
        # 确认它不是 sci-skills/sci-draw（即它真在根下）
        try:
            legacy.relative_to(root)
        except ValueError:
            return None
        # 排除它就是 family_root/sci-draw 的情况（已在上面的 != 判断里）
        return legacy
    return None


def cmd_migrate(args: argparse.Namespace) -> int:
    root = find_project_root()
    legacy = find_legacy_sci_draw(root)
    target = family_root(root) / "sci-draw"

    if legacy is None:
        print(f"migrate @ {root}\n✓ 没有检测到老的 sci-draw/（在项目根、不在 sci-skills/ 下）。无需迁移。")
        return 0

    report = [f"migrate @ {root}", f"检测到老的 sci-draw/ → {legacy.relative_to(root)}"]
    report.append(f"  目标位置 → {target.relative_to(root)}")

    # 冲突检查：目标已存在
    if target.exists():
        report.append(
            f"⚠ 目标 {target.relative_to(root)} 已存在。不会自动合并。"
            "请手动决定：保留哪一个、或合并内容后删旧的。"
        )
        print("\n".join(report))
        return 1

    # 列出将迁移的内容
    files = sorted(p for p in legacy.rglob("*") if p.is_file())
    report.append(f"  将迁移 {len(files)} 个文件")

    if not args.apply:
        report.append("\n[dry-run] 加 --apply 真正执行迁移。迁移 = mv 老目录到新位置。")
        print("\n".join(report))
        return 0

    # 真迁
    target.parent.mkdir(parents=True, exist_ok=True)
    legacy.rename(target)
    report.append(f"✓ 已迁移 → {target.relative_to(root)}")
    report.append("  提示：若 git 跟踪了老路径，请 git add -A 提交这次重命名。")
    print("\n".join(report))
    return 0


# ----------------------------- checkup -----------------------------


def cmd_checkup(args: argparse.Namespace) -> int:
    """体检：扫描当前结构，报告各 skill 落盘位置对不对。"""
    root = find_project_root()
    fam = family_root(root)
    report: list[str] = [f"checkup @ {root}"]
    issues: list[str] = []
    info: dict = {"project_root": str(root), "family_root_exists": fam.is_dir(), "skills": {}}

    # 1. 家族顶层在不在
    if not fam.is_dir():
        issues.append(
            f"✗ {FAMILY_ROOT_NAME}/ 不存在。本项目还没初始化——跑 `init_project.py init`。"
        )
        report.extend(issues)
        print("\n".join(report))
        info["issues"] = issues
        print("\n--- JSON ---\n" + json.dumps(info, ensure_ascii=False, indent=2))
        return 1

    # 2. 各兄弟子目录状态
    report.append(f"\n{'skill':<12} {'目录':<8} {'文件数':<8} 状态")
    report.append("-" * 50)
    for skill in BROTHER_SKILLS:
        skill_dir = fam / skill
        if not skill_dir.is_dir():
            report.append(f"{skill:<12} {'—':<8} {'—':<8} 缺失（按需 init）")
            info["skills"][skill] = {"present": False}
            continue
        files = [
            p for p in skill_dir.rglob("*")
            if p.is_file() and p.name != ".README.md"
        ]
        report.append(
            f"{skill:<12} {'✓':<8} {len(files):<8} {'空' if not files else '有产物'}"
        )
        info["skills"][skill] = {"present": True, "file_count": len(files)}

    # 3. 错位检测：项目根下是否有散落的 skill 目录（不在 sci-skills/ 下）
    scattered: list[str] = []
    if root.is_dir():
        for entry in root.iterdir():
            if entry.is_dir() and entry.name in BROTHER_SKILLS:
                if not _is_subpath(entry, fam):
                    scattered.append(entry.name)
    if scattered:
        for name in scattered:
            issues.append(
                f"⚠ {name}/ 散落在项目根（不在 {FAMILY_ROOT_NAME}/ 下）。"
                f"跑 `init_project.py migrate --apply` 迁到 {FAMILY_ROOT_NAME}/{name}/。"
            )
        info["scattered"] = scattered

    # 4. git 状态
    if not is_git_repo(root):
        issues.append("⚠ 项目未 git init。建议 git init 跟踪产物演化。")
        info["git"] = False
    else:
        info["git"] = True

    report.append("")
    if issues:
        report.append("问题:")
        for it in issues:
            report.append(f"  {it}")
    else:
        report.append("✓ 布局健康，无错位。")

    info["issues"] = issues
    print("\n".join(report))
    print("\n--- JSON ---\n" + json.dumps(info, ensure_ascii=False, indent=2))
    return 1 if issues else 0


def _is_subpath(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


# ----------------------------- main -----------------------------


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="sci-skills 家族项目初始化 / 迁移 / 体检。手动触发，跑一次就退。",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="建 sci-skills/ 骨架 + git + .gitignore")
    p_init.add_argument("--no-git", action="store_true", help="跳过 git init")
    p_init.set_defaults(func=cmd_init)

    p_mig = sub.add_parser("migrate", help="迁移老 sci-draw/ 到 sci-skills/sci-draw/")
    p_mig.add_argument("--apply", action="store_true", help="真正执行（默认 dry-run）")
    p_mig.set_defaults(func=cmd_migrate)

    p_chk = sub.add_parser("checkup", help="体检落盘位置")
    p_chk.set_defaults(func=cmd_checkup)

    args = parser.parse_args(argv[1:])
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
