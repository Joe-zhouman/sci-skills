#!/usr/bin/env python3
"""init_project.py — sci-skills 家族项目初始化 / 体检。

手动触发的厚编排入口 article-init 的执行载体。一次性干完就退：
不持续运行、不自动推进日常图→文流程（那是人手动用各执行 skill）。

两个子命令（都只做确定性机械活）:
    init      在 cwd 建 manuscript/ + sci-skills/ 骨架 + git init + .gitignore
    checkup   体检：扫描结构，报告正文/skill 落盘位置；项目根有错位时发信号

迁移不是脚本子命令——老项目结构千变万化、会误判用户文件。迁移是 agent 流程:
    checkup 报错位信号 → 派 Explore agent 读懂内容判断归位 → 跟用户确认 → agent 发 mv

哲学:
- 幂等：重复跑不破坏已有内容。已存在的目录/文件跳过，不覆盖。
- 确定性归脚本，判断性归 agent：init/checkup 脚本做；读懂内容判断归位 Explore 做；
  移动用户文件 agent 跟用户确认后做。脚本永不自动移动用户文件。
- 纯 stdlib，无外部依赖。

用法:
    python init_project.py init [--no-git]
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

# 正文项目目录名（一等公民，在项目根，不在 sci-skills/ 下）
MANUSCRIPT_DIR_NAME = "manuscript"

# 预建的兄弟 skill 子目录（与仓库 skills/ 下的 skill 对齐）。
# 列表随 skill 成熟度演化——只预建需要自己输出目录的 skill。
# sci-polish / sci-typeset 不预建：它们直接在 manuscript/ 里改 tex 文件，零落盘。
# sci-story / sci-export / sci-respond 也不预建：sci-story 读 sci-write 的笔记 + 写 tex
#   进 manuscript/；sci-export 只读 manuscript/ 写副本；sci-respond 把 response 产物写进
#   manuscript/rN/response/（CONTRACT 已预留）。三者都无独立产物目录。
# sci-revise 预建：它是 revision 轮次的**共用过程状态家**（issue-ledger / change-log /
#   polish-todo），sci-respond 写、sci-revise 读/写、sci-polish 读——同 sci-write/ 被三
#   skill 共用一样，通过 CONTRACT 解耦，谁都不"独占"。
BROTHER_SKILLS = ["sci-draw", "sci-write", "sci-submit", "sci-revise"]

# 每个子目录的契约文件内容（CONTRACT.md，点开头=隐藏，给人看，也帮 git 跟踪空目录）。
# 关键定位：**这些 CONTRACT.md 本身就是目录级接口契约**——任何 agent / 任何 skill
# 拿到这份文件，就知道往这个目录放什么、按什么 schema、谁会读。照着契约就能产出
# 合规产物，不需要知道是哪个 skill 在用、不需要 import 任何东西。这是解耦的落地。
# 三件事都说清：这个文件夹代表什么 / 有什么用 / 产物怎么放进来（含 schema + 命名 + 来源）。
SKILL_DIR_CONTRACTS: dict[str, str] = {
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
- `figN.png` — 导出预览（下游图义核查喂给识图能力用——任何识图工具/识图模型，不绑具体工具）
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
    "sci-write": """# sci-write/ — 写作工作笔记（working notes only）

> **这份文件是契约（contract）。** 本目录只放**过程元数据**（working notes），
> 不放正文产物。正文 tex 直接写进 `../../manuscript/vN/tex/`，从不落在这里。

## 这个文件夹是什么
sci-write skill 的**工作笔记区**。存放写作过程中产生的过程元数据：
论文规划接力棒、数据画像、图义核查记录、SI 停车单、术语账本。这些文件**不是正文**，
永远不进 tex，永不成为论文的一部分——它们是写正文时用的脚手架。

## 有什么用
- 承载"数据 → 图 → 正文"流水线的**写作阶段过程状态**。
- `paper-plan.md` 是跨 session 的接力棒，记录哪张图画了没、哪节写了没。
- `terminology-ledger.md` 是 sci-write / sci-story / sci-polish **三方共写**的术语账本。

## 文件清单（全是 working notes，非正文）
- `claim.md` — 一句论证 + 证据基线（Step 0，人确认后落盘）。全文的合同。
- `paper-plan.md` — **接力棒**。图清单 + 章节进度。每次回来先读它。
- `data-profile.json` — 数据画像（Step 0 调 profile_data 产出，喂给 Method）。
- `figN-reading.md` — 图义核查记录（Step 3，识图能力独立描述 vs claim 对照）。
- `sup-list.md` — SI 停车单（被砍的图/方法细节/overflow 表格，攒着喂给 si.tex）。
- `terminology-ledger.md` — 术语账本（与 sci-story / sci-polish 共写）。

## 正文 tex 在哪（不在本目录）
Method/Results/Conclusion 的 tex **直接写进 `../../manuscript/vN/tex/sections/`**：
`method.tex` / `results.tex` / `conclusion.tex`。SI 是写作副产品，写进
`../../manuscript/vN/tex/si.tex`（或 `si/`）。**本目录永远不放 tex 正文。**

## 产物怎么进来
- **本 skill 自己产**：上面清单里的 working notes，全由 sci-write 写。
- **从图仓库读**（不复制进来）：sci-write 读 `../sci-draw/figN-report.md` 和 `figN.png`，
  但**不复制进来**——图仓库是图的唯一存放点。
- **人手动**：人可以直接编辑这里的 notes（补术语、改 claim）。

## 谁读它
人（读/改 notes）；sci-story（读 paper-plan + claim + 四章 tex 作为引言/讨论的输入）；
sci-polish（读术语账本）；submission 阶段（读 claim 定期刊层级）。
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
- **从 manuscript/ 读**（不复制）：读 `../../manuscript/v1/`（或当前轮 rN/）的定稿 tex
  提取核心发现/元数据打包投稿，但正文不复制进来——manuscript/ 是正文唯一存放点。
- **人手动**：投稿追踪、期刊反馈等人工内容。

## 谁读它
人；本 skill 在设计中，文件清单会随设计确定后回填。
""",
    "sci-revise": """# sci-revise/ — 修回轮次共用状态（revision-round shared state）

> **这份文件是契约（contract）。** 本目录是 revision 轮次的**过程状态家**，
> 存 issue-ledger / change-log / polish-todo。多个 skill 共读写——同 sci-write/
> 被 write/story/polish 共用一样，通过本契约解耦，谁都不"独占"。
> **不放正文产物**：response letter 落 `../../manuscript/rN/response/`，
> 改后的稿落 `../../manuscript/rN/tex/`；本目录只放过程元数据。

## 这个文件夹是什么
revision 轮次的**共用过程状态区**。名字借 sci-revise skill 的辨识度，但语义中性：
任何处理修回的 skill 都按本契约读写这里。sci-respond 在 intake 阶段写 issue-ledger，
sci-revise 读它去改稿、写回 change-log 和 polish-todo，sci-polish 读 polish-todo。

## 有什么用
- **issue-ledger.md 是 sci-respond ↔ sci-revise 的交接面**：每条审稿意见一个稳定 ID
  （R1-Q03），记录 underlying concern / 策略 / safe-claim-boundary / 落地位置 /
  revision_kind。sci-respond 写，sci-revise 据此改稿。
- **change-log.md** 是 delta-only 审计轨迹（只记变更，不存当前真相）。
- **polish-todo.md** 是 sci-revise → sci-polish 的交接面：大段新插入需 polish 的段落清单。

## 文件清单（全是过程元数据，非正文）
- `issue-ledger.md` — 每条审稿意见一个 block（stable ID + underlying concern + 策略 +
  safe-claim-boundary + evidence_anchors + manuscript_action + revision_kind）。
  sci-respond / sci-revise 共写；schema 见 sci-respond 的 state-contract.md。
- `change-log.md` — delta-only 审计（append-only，不重写）。
- `polish-todo.md` — 大段新插入段落清单（位置 + 开头快照 + 原因 + from_issue）。
  sci-revise 写，sci-polish 读。**零碎改动不进**。

## 正文产物在哪（不在本目录）
- Response letter（tex+PDF+Response Figure）→ `../../manuscript/rN/response/`
- 改后的稿 → `../../manuscript/rN/tex/`
- 审稿意见原文 → `../../manuscript/rN/reviews/`
- **本目录永远不放正文产物。**

## 产物怎么进来
- **sci-respond 写** issue-ledger（intake 阶段）+ change-log。
- **sci-revise 读/写** issue-ledger（据此改稿）+ change-log + polish-todo。
- **sci-polish 读** polish-todo（据此 polish 大段新插入）。
- **人手动**：可直接编辑这里的 notes（改策略、补 boundary）。

## 谁读它
sci-respond（写 ledger）；sci-revise（读 ledger 改稿，写 change-log/polish-todo）；
sci-polish（读 polish-todo）；人（读/改过程状态）。
""",
}

# manuscript/ 的契约文案。manuscript/ 是项目一等公民（在项目根，不在 sci-skills/ 下）。
# init 只建空目录 + 这份契约，**不生成任何 tex 模板内容**——模板高度定制，用户说了算。
# 结构按"审稿轮次"单维度组织（v/r），期刊维度归 sci-submit/submit-history。
MANUSCRIPT_CONTRACT = """# manuscript/ — 正式正文（the manuscript, first-class citizen）

> **这份文件是契约（contract）。** 本目录是项目的**唯一正式正文**，按**审稿轮次**
> 组织。所有 skill 读它、写它，但都不"拥有"它——正文比任何 skill 都大。具体 tex 模板、
> 期刊样式由用户决定，init 不预填任何模板内容，**也不预设任何 float/layout 取向**——
> 排版取向在 typeset/export 阶段才引入。

## 目录结构（v/r 轮次制）

```
manuscript/
  CONTRACT.md              ← 本契约
  v1/                     ← 初版（首投的那套稿，一套投多刊）
    tex/                  ← 正文源（sci-write / sci-story 直接写 tex 进来）
      sections/           ← 分章节 tex（method/results/conclusion/intro/discussion/abstract/...）
      main.tex            ← preamble + \\input 把各章节织起来
      si.tex (或 si/)     ← Supplementary Information（sci-write 的副产品）
      bibliography.bib    ← 参考文献
    figures/              ← 正文的图（从 ../sci-skills/sci-draw/ 复制来，自含可编译）
    (submission/)         ← 编译出的提交版（可选）
  r1/                     ← 第一轮修回（审稿意见到了，改这一轮）
    tex/                  ← 改后的稿（在 v1 基础上改）
    response/             ← point-by-point Response（每条审稿意见→指向正文哪处改了）
    reviews/              ← 审稿意见原文
    revision-cover-letter/← 修回的 cover letter（简短版，不重新推销）
  r2/                     ← 第二轮修回（若有，结构同 r1）
  ...
```

**单维度原则：只按"审稿轮次"组织，不按期刊、不按文件类型分顶层目录。**

## v 和 r 的语义

- **v1 = 初版**。首次投稿的那套稿。**一套 v1 投多个期刊**——绝大多数初审是
  your-paper-your-way，一套模板差不多，只需修修补补。投了哪些期刊、各自什么结果，
  记在 `../sci-skills/sci-submit/submit-history.md`，**不在这里分目录**。
- **rN = 第 N 轮修回**。某期刊给 major/minor revision 后，在 v1（或上一轮 r）基础上
  改出的版本。每个 rN 是一个完整包：改后的稿 + Response + 审稿意见 + revision cover letter。
  这个 rN 是哪个期刊的修回，同样记在 submit-history。
- **改投别刊 ≠ 新 v**。换期刊通常不换模板（your-paper-your-way），改投只是"把同一个
  v/r 再投给下一个期刊"，投稿行为记 history。**只有真的要换一套全新模板时**，
  用户才手动开 v2（罕见），那是用户的事，不是 init 预设的。

## 什么时候建 r1/r2

init **只建 v1/**，不预建 r1/r2。rN 在**真到了那轮 revision 时**由人建——
sci-respond skill 触发时若 rN 不存在会提示人先建（没有审稿意见就建空 r1 没意义）。
建 rN 时照上面的结构：`tex/`（改后的稿）+ `response/`（sci-respond 产的 Response letter）
+ `reviews/`（审稿意见原文）+ `revision-cover-letter/`（修回 cover letter，sci-submit 产）。

## 为什么在项目根、不在 sci-skills/ 下

正文是**成果**，skill 是**工具**。成果不该塞进工具的子目录。而且正文经常**从外部来**
（别处写好的 Word/Overleaf/合作者的项目），是独立的一等公民，skill 都来服务它。

## 放什么（用户决定具体形式）

常见 LaTeX 项目（仅供参考，**不强制**；sci-skills-article 插件的 `templates/main/` 有成熟蓝本可复制）：
- `tex/main.tex` — preamble + `\\input` 织起各章节（main.tex 用 `\\input{sections/method}` 织入分章）
- `tex/sections/*.tex` — 各章节正文（sci-write / sci-story 直接写进这里）
- `tex/si.tex`（或 `tex/si/`）— Supplementary Information（sci-write 副产品）
  - 蓝本 `templates/main/tex/sup.tex` 文件名仍叫 `sup.tex`——那是历史命名，语义同 si。
    新项目用 `si.tex`；复用蓝本时按蓝本名即可，不影响合同。
- `figures/figN.png` — 正文的图（从 `../sci-skills/sci-draw/` 复制来，保证正文项目自含可独立编译）
- `ref/bibliography.bib` — 参考文献（用户用 Zotero/Endnote 维护，最终插入是人的活）
- `Makefile` / `.gitignore` — 编译链 + 忽略中间产物（可选）

**正文项目要自含**——能独立编译、能打包投稿。图从图仓库**复制**进 figures/，不要软链
（软链跨机器/打包会断）。

## 谁读它 / 谁写它

- **sci-write**：直接写 Method/Results/Conclusion tex 进 `v1/tex/sections/`，
  副产品 SI 进 `v1/tex/si.tex`。**没有 md 草稿中间层**——tex 从一开始就写在这里。
- **sci-story**：直接写 Introduction/Discussion/Abstract/Keywords tex 进 `v1/tex/sections/`。
- **sci-polish**：直接在 `v1/tex/sections/*.tex` 上改措辞、claim、术语（git 留痕）。
- **sci-typeset**：直接在 `v1/tex/` 上改排版可读性（loose page / stranded heading / 表太宽）。
- **sci-export**：**只读不写源**——把定稿 tex 复制进 `v1/tex/template-move/` 搬期刊模板，
  或生成 `v1/manuscript.docx`。源 `v1/tex/` 对它是只读。
- **sci-submit**：读 v1/（或当前轮 rN/）提"核心发现/元数据/打包投稿"。
- **人**：Zotero 插文献、改 tex 形式、换模板，都是人的活。修订轮 rN 的设计待
  sci-revise skill 设计后补。
- **init**：只建 `manuscript/` + `v1/` + 本契约，不写任何 tex 内容，不预设排版取向。

## 不放什么

- 不放 sci-write 的 working notes（claim/paper-plan/figN-reading 等，留 `../sci-skills/sci-write/`）
- 不放画图中间产物（留在 `../sci-skills/sci-draw/`，只把成品图复制进 figures/）
- 不放投稿产物（cover letter/history 等留在 `../sci-skills/sci-submit/`）
- 不按期刊分顶层目录（期刊维度归 submit-history）

本目录只放**正式正文本身**，按轮次组织。
"""

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

    # 0. manuscript/ —— 一等公民，最先建（在 skill 产物目录之前）。
    #    只建空 manuscript/ + v1/ + 契约 CONTRACT.md，不生成任何 tex 模板内容。
    ms_dir = root / MANUSCRIPT_DIR_NAME
    ms_contract = ms_dir / "CONTRACT.md"
    if ms_dir.exists():
        if not ms_contract.exists():
            ms_contract.write_text(MANUSCRIPT_CONTRACT, encoding="utf-8")
            report.append(f"✓ {MANUSCRIPT_DIR_NAME}/ 已存在，补 CONTRACT.md 契约")
        else:
            report.append(f"✓ {MANUSCRIPT_DIR_NAME}/ 已存在（跳过）")
    else:
        ms_dir.mkdir(parents=True)
        ms_contract.write_text(MANUSCRIPT_CONTRACT, encoding="utf-8")
        # v1/ 是初版目录；只建空目录 + 留个 git 跟踪文件，不预填 tex 内容
        v1 = ms_dir / "v1"
        v1.mkdir(exist_ok=True)
        (v1 / ".gitkeep").write_text("", encoding="utf-8")
        report.append(f"✓ 创建 {MANUSCRIPT_DIR_NAME}/ + v1/ + CONTRACT.md 契约")

    # 1. 家族顶层
    if fam.exists():
        report.append(f"✓ {fam.name}/ 已存在（跳过创建）")
    else:
        fam.mkdir(parents=True)
        report.append(f"✓ 创建 {fam.name}/")

    # 2. 预建兄弟子目录 + CONTRACT.md（点开头=隐藏；给人看的契约文件，
    #    说明这个目录归谁、放什么；也帮 git 跟踪空目录。比 .gitkeep 有意义。）
    for skill in BROTHER_SKILLS:
        skill_dir = fam / skill
        contract = skill_dir / "CONTRACT.md"
        if skill_dir.exists():
            if not contract.exists() and skill in SKILL_DIR_CONTRACTS:
                # 目录在但缺契约文件 → 补一份（不覆盖已有内容）
                contract.write_text(SKILL_DIR_CONTRACTS[skill], encoding="utf-8")
                report.append(f"  - {skill}/ 已存在，补 CONTRACT.md")
            else:
                report.append(f"  - {skill}/ 已存在（跳过）")
        else:
            skill_dir.mkdir()
            contract_text = SKILL_DIR_CONTRACTS.get(
                skill, f"# {skill}/\n\nReserved for the {skill} skill.\n"
            )
            contract.write_text(contract_text, encoding="utf-8")
            report.append(f"  - 创建 {skill}/ + CONTRACT.md")

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


# ----------------------------- checkup helpers -----------------------------


def list_root_candidates(root: Path) -> list[dict]:
    """列出项目根下不在标准位置的内容（manuscript/、sci-skills/、.git 之外的东西）。
    浅层扫描，只给 checkup 当"该派 Explore 深查"的信号——**不下结论**这些是什么、
    该进哪。判断（这是不是正文、是不是老图仓库）由 Explore agent 读懂内容后做，
    脚本写死规则会误判用户文件。
    """
    entries: list[dict] = []
    if root.is_dir():
        for entry in sorted(root.iterdir()):
            if entry.name in {FAMILY_ROOT_NAME, MANUSCRIPT_DIR_NAME, ".git"}:
                continue
            if entry.name.startswith("."):
                continue
            if entry.is_dir():
                n_files = sum(1 for _ in entry.rglob("*") if _.is_file())
                entries.append({"name": entry.name + "/", "type": "dir", "files": n_files})
            else:
                entries.append({"name": entry.name, "type": "file", "size": entry.stat().st_size})
    return entries


# ----------------------------- checkup -----------------------------


def cmd_checkup(args: argparse.Namespace) -> int:
    """体检：扫描当前结构，报告正文 + 各 skill 落盘位置对不对。"""
    root = find_project_root()
    fam = family_root(root)
    report: list[str] = [f"checkup @ {root}"]
    issues: list[str] = []
    info: dict = {
        "project_root": str(root),
        "manuscript": {},
        "family_root_exists": fam.is_dir(),
        "skills": {},
    }

    # 0. manuscript/（一等公民，先报）
    ms_dir = root / MANUSCRIPT_DIR_NAME
    if not ms_dir.is_dir():
        issues.append(
            f"⚠ {MANUSCRIPT_DIR_NAME}/ 不存在。正文是一等公民——跑 `init` 建它 + v1/。"
        )
        info["manuscript"] = {"present": False}
    else:
        # 列出 v1/r1/r2... 轮次目录
        rounds = sorted(
            d.name for d in ms_dir.iterdir()
            if d.is_dir() and (d.name == "v1" or d.name.startswith("r"))
        )
        # v1 有没有真内容（非 .gitkeep / CONTRACT.md）
        v1_files = [
            p for p in (ms_dir / "v1").rglob("*")
            if p.is_file() and p.name not in {".gitkeep", "CONTRACT.md"}
        ] if (ms_dir / "v1").is_dir() else []
        report.append(
            f"manuscript/   ✓  轮次: {', '.join(rounds) if rounds else '(无)'}  "
            f"v1内容: {len(v1_files)} 文件"
        )
        info["manuscript"] = {
            "present": True, "rounds": rounds, "v1_file_count": len(v1_files),
        }
        if not v1_files:
            issues.append(
                f"⚠ {MANUSCRIPT_DIR_NAME}/v1/ 还是空的。"
                "把正文（tex/figures/bib）放进去，或从 sci-skills-article 插件的 templates/main/ 复制蓝本。"
            )

    # 0b. 项目根是否有不该在根的内容（浅层信号，深度判断派 Explore）
    root_cands = list_root_candidates(root)
    if root_cands:
        info["root_candidates"] = root_cands
        cand_names = ", ".join(c["name"] for c in root_cands)
        issues.append(
            f"⚠ 项目根有 {len(root_cands)} 项不在 {MANUSCRIPT_DIR_NAME}/ 或 "
            f"{FAMILY_ROOT_NAME}/ 下（{cand_names}）。派 Explore agent 读懂这些内容、"
            f"判断归位（正文→{MANUSCRIPT_DIR_NAME}/v1/，老图→{FAMILY_ROOT_NAME}/sci-draw/ 等），"
            "跟用户确认后发 mv。脚本不自动判断、不自动移。"
        )

    # 1. 家族顶层在不在
    if not fam.is_dir():
        issues.append(
            f"✗ {FAMILY_ROOT_NAME}/ 不存在。本项目还没初始化——跑 `init_project.py init`。"
        )
        report.append("")
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
            if p.is_file() and p.name != "CONTRACT.md"
        ]
        report.append(
            f"{skill:<12} {'✓':<8} {len(files):<8} {'空' if not files else '有产物'}"
        )
        info["skills"][skill] = {"present": True, "file_count": len(files)}

    # 3. git 状态
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


# ----------------------------- main -----------------------------


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="sci-skills 家族项目初始化 / 迁移 / 体检。手动触发，跑一次就退。",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="建 sci-skills/ 骨架 + git + .gitignore")
    p_init.add_argument("--no-git", action="store_true", help="跳过 git init")
    p_init.set_defaults(func=cmd_init)

    p_chk = sub.add_parser("checkup", help="体检落盘位置 + 报错位信号")
    p_chk.set_defaults(func=cmd_checkup)

    args = parser.parse_args(argv[1:])
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
