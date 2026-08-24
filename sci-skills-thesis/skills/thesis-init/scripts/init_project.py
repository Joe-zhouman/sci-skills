#!/usr/bin/env python3
"""init_project.py — sci-skills-thesis 家族项目初始化 / 体检。

手动触发的厚编排入口 thesis-init 的执行载体。一次性干完就退：
不持续运行、不自动推进拆→写链条（那是人手动用各执行 skill）。

两个子命令（都只做确定性机械活）:
    init      在 cwd 建 thesis/（一等产物，按章组织）+ sci-skills/ 共享工作区
              （thesis- 前缀共享文件，与 article 家族共存不碰撞）+ 各兄弟 skill 子目录
              + CONTRACT.md 契约 + 织入所选大学模板包到 thesis/tex/
    checkup   体检：扫描结构，报告 thesis/skill 落盘位置；项目根有错位时发信号

来源 registry 不是脚本子命令——每篇小论文的路径/数据散落各处、需交互判断。
registry 是 agent 流程：init 建占位 thesis-sources.md → agent 逐篇问用户 →
agent 按 schema 写 markdown（全家族导航真相）。

哲学:
- 幂等：重复跑不破坏已有内容。已存在的目录/文件跳过，不覆盖。
- 确定性归脚本，判断性归 agent：init/checkup/模板织入 脚本做；收集来源 registry、
  选模板包、确认项目根 agent 跟用户确认后做。脚本永不写 registry 内容。
- 纯 stdlib，无外部依赖。

用法:
    python init_project.py init [--no-git] [--template <pack>] [--template-dir <path>]
    python init_project.py checkup
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path, PurePath

# 家族顶层目录名 — 与 article 家族共享（同一工作区 sci-skills/，二者共存）
FAMILY_ROOT_NAME = "sci-skills"

# 学位论文一等产物目录（在项目根，按章组织，非审稿轮次）
THESIS_DIR_NAME = "thesis"

# 预建的兄弟 skill 子目录（需要自己输出目录的才预建）。
# thesis-spine / thesis-polish / thesis-typeset 不预建：
#   spine 产顶层共享文件 thesis-spine.md + thesis-terminology-ledger.md（无自己的目录）；
#   polish/typeset 直接在 thesis/tex/ 上原地改 tex，git 留痕（无自己的目录）。
# thesis-init 自己也不预建（entry，scaffold 完即退）。
BROTHER_SKILLS = ["thesis-dissect", "thesis-intro", "thesis-theory", "thesis-summary"]

# 顶层共享文件（放在 sci-skills/ 根，thesis- 前缀避免与 article 家族碰撞）。
# thesis-sources.md 是来源 registry（agent 交互填充，全家族导航真相）。
# thesis-spine.md / thesis-terminology-ledger.md 是占位骨架（spine skill 后续填充）。
SHARED_FILES_PLACEHOLDERS = {
    "thesis-sources.md": "<!-- 来源 registry — thesis-init 交互填充。每篇小论文一条：\n"
        "## paper-A\n- slug: chapter-a\n- paths: [../paper-A/, ../shared-data/]\n"
        "- data_paths: [../paper-A/data/]\n- claim: (dissect 回填)\n-->\n",
    "thesis-spine.md": "<!-- 主线+统一框架+章间递进+thesis级claim — thesis-spine skill 产。占位。 -->\n",
    "thesis-terminology-ledger.md": "<!-- 跨章术语表 — thesis-spine 建，各章/polish 共写。占位。 -->\n",
}

# sci-skills/thesis-README.md 内容（thesis 家族自述 + routing table — thesis- 前缀避免与
# article 家族的 sci-skills/README.md 在共存项目里碰撞）
def _readme_text() -> str:
    lines = [f"# {FAMILY_ROOT_NAME}/\n",
             "The sci-skills family on-disk workspace. Article + thesis families coexist here.\n",
             "## Thesis-family shared files (top-level, thesis- prefixed)\n",
             "- `thesis-sources.md` — source registry (thesis-init fills; all thesis skills read)\n",
             "- `thesis-spine.md` — main line + unified framework (thesis-spine produces)\n",
             "- `thesis-terminology-ledger.md` — cross-chapter terminology\n",
             "## Sibling skill dirs\n"]
    for s in BROTHER_SKILLS:
        lines.append(f"- `{s}/`\n")
    lines.append("\n## Convention\n- Skills read neighbors' on-disk outputs; never import each other.\n"
                 "- thesis-init is the only node that knows all siblings; every other skill knows only files.\n")
    return "".join(lines)


# thesis/ 的契约文案。thesis/ 是项目一等公民（在项目根，不在 sci-skills/ 下）。
# init 只建空目录 + 这份契约 + 织入模板包，**不生成任何 tex 正文内容**——正文由各写章
# skill 产。结构按"章"单维度组织（非审稿轮次）；文件命名遵循所选模板的 template-spec.md，
# **本契约不规定章文件名**——换模板就是换命名约定。
THESIS_CONTRACT = """# thesis/ — 学位论文正文（the thesis, first-class citizen）

> **这份文件是契约（contract）。** 本目录是项目的**唯一正式学位论文正文**，按**章**
> 组织（不是审稿轮次）。所有 thesis skill 读它、写它，但都不"拥有"它——正文比任何
> skill 都大。大学模板由 thesis-init 在 init 时织入 `tex/`，**本契约不规定文件命名**
> ——命名遵循所选模板的 `template-spec.md`（tex/ 旁的那份）。working notes 永不落这。

## 目录结构（按章组织）

```
thesis/
  CONTRACT.md              ← 本契约
  tex/                     ← 正文源（init 把所选模板包整体织入这里）
    main.tex               ← preamble + \\input 织入各章
    (各章 .tex)            ← 章文件 / refs / 前置后置页 / config 子目录等——命名遵循 tex 旁的 template-spec.md
  template-spec.md         ← 所选模板的文件命名约定（各 skill 读它对齐命名）
```

**单维度原则：只按"章"组织，不按审稿轮次、不按期刊分顶层目录。**
学位论文是学位答辩的一次性提交作品（非 manuscript 那样的 v1/r1/r2 审稿轮次制）。

## 为什么按章组织、不按审稿轮次

学位论文是**学位答辩的一次性提交作品**——没有"投了被拒改投"的轮次演化。正文按**章**
组织：绪论、共用理论方法、各正文章（每章由一篇小论文重组延伸而来）、总结展望。章的
命名遵循所选大学模板的 `template-spec.md`，**本契约不硬编码章文件名**——换模板就是换
命名约定。

## 模板织入（init 时织好）

与 article 家族不同（article 在投稿时才搬模板），thesis 的大学模板在 **init 时就织入**
`thesis/tex/`——因为学位论文从第一行 tex 起就必须符合校规（.cls / 封面 / 前置后置页 /
盲审格式）。init 把 `templates/thesis/<pack>/` 织入 `tex/`（main.tex + 章骨架），并把
`template-spec.md` 复制到 `thesis/`（本目录，各 skill 读的命名约定）。此后各写章 skill
直接往织好的章文件里写 tex。**本契约不重复模板要求**——模板要什么看 `template-spec.md`
（本目录）和织入 `tex/` 的 `.cls`。

## 为什么在项目根、不在 sci-skills/ 下

正文是**成果**，skill 是**工具**。成果不该塞进工具的子目录。thesis/ 是一等公民，在
项目根，与 sci-skills/ 平级。

## 谁读它 / 谁写它

- **thesis-init**：建 `thesis/` + `tex/`（空）+ 本契约 + 织入模板包。**不写任何 tex 正文**。
- **thesis-spine**：读各章 tex 感知主线，产 `../sci-skills/thesis-spine.md`（不在本目录）。
- **thesis-dissect**：直接写各**正文章** tex 进 `tex/`（拆即写——拆一篇小论文、重组延伸
  成一章，直接落 tex）。产 `chapter-map.md` 在 `../sci-skills/thesis-dissect/`。
- **thesis-intro**：直接写绪论章 tex 进 `tex/`（章文件名按 template-spec.md）。
- **thesis-theory**：直接写共用理论方法章 tex 进 `tex/`。
- **thesis-summary**：直接写总结展望章 tex 进 `tex/`。
- **thesis-polish**：直接在 `tex/*.tex` 上改措辞、claim、术语（git 留痕，无独立产物目录）。
- **thesis-typeset**：直接在 `tex/` 上改排版 / .cls 合规 / 盲审格式（git 留痕）。
- **人**：Zotero 插文献、填封面/前置后置页、改 tex 形式，都是人的活。

## 不放什么

- 不放 working notes（拆解笔记 / chapter-map / claim 等留 `../sci-skills/thesis-*/`）
- 不放来源 registry（`../sci-skills/thesis-sources.md`）
- 不放主线/术语表（`../sci-skills/thesis-spine.md` / `thesis-terminology-ledger.md`）
- 不按审稿轮次分顶层目录（学位论文是一次性提交作品，非轮次制）

本目录只放**正式学位论文正文本身**，按章组织。
"""

# 每个兄弟子目录的契约文件内容（CONTRACT.md）。关键定位同 article 家族：**这些
# CONTRACT.md 本身就是目录级接口契约**——任何 agent / 任何 skill 拿到这份文件，就知道
# 往这个目录放什么、按什么 schema、谁会读。照着契约就能产出合规产物，不需要知道是哪个
# skill 在用、不需要 import 任何东西。三件事都说清：这个文件夹代表什么 / 有什么用 /
# 产物怎么放进来（含 tex 去哪 + 谁读它）。
SKILL_DIR_CONTRACTS: dict[str, str] = {
    "thesis-dissect": """# thesis-dissect/ — 拆+写正文章工作笔记（working notes only）

> **这份文件是契约（contract）。** 本目录只放**过程元数据**（working notes），
> 不放正文产物。正文章 tex 直接写进 `../../thesis/tex/`，从不落在这里。

## 这个文件夹是什么
thesis-dissect skill 的**工作笔记区**。拆即写——每拆一篇小论文、就重组延伸成一章
学位论文正文。每篇小论文一个 `paper-X/` 子目录，里面放拆解过程笔记。`chapter-map.md`
是跨 session 的接力棒，全家族读。

## 有什么用
- 承载"读小论文 → 重组延伸 → 写正文章"流水线的**拆解阶段过程状态**。
- `chapter-map.md` 记录每篇小论文 → 哪一章、章命名、各章 claim 演化。每次回来先读它。
- 每篇小论文的拆解笔记隔离在 `paper-X/` 子目录里，互不干扰。

## 文件清单（全是 working notes，非正文）
- `chapter-map.md` — **接力棒**。每篇小论文一条：paper_id → slug（章名 token）→
  章文件名（按 `../../thesis/template-spec.md`）→ claim（演化中）。全家族导航。
- `paper-X/` — 该篇小论文的拆解笔记子目录，按三类组织：
  - 章映射（这篇小论文的哪部分进哪一章）
  - 模块重构（小论文的 module 如何重组成 thesis 章）
  - question→claim 记录（小论文的问题如何提炼成 thesis 级 claim）

## 正文 tex 在哪（不在本目录）
正文章 tex **直接写进 `../../thesis/tex/`**（章文件名遵循
`../../thesis/template-spec.md`）。**本目录永远不放 tex 正文。**

## 产物怎么进来
- **本 skill 自己产**：上面清单里的 working notes，全由 thesis-dissect 写。
- **从 `../thesis-sources.md` 读**（不复制进来）：读来源 registry 定位每篇小论文的
  路径和数据，但**不复制进来**——registry 是导航真相，dissect 按它去找源文件。
- **人手动**：人可以直接编辑这里的 notes（补 claim、改章映射）。

## 谁读它
人（读/改 notes）；thesis-spine（读 chapter-map.md 感知各章 claim 和递进）；
thesis-summary（读 chapter-map.md 做共性提炼和 callback）。
""",
    "thesis-intro": """# thesis-intro/ — 绪论章工作笔记（working notes only）

> **这份文件是契约（contract）。** 本目录只放**过程元数据**（working notes），
> 不放正文产物。绪论章 tex 直接写进 `../../thesis/tex/`，从不落在这里。

## 这个文件夹是什么
thesis-intro skill 的**工作笔记区**。写学位论文绪论章（研究背景、研究现状、gap、
论文结构）时的过程笔记。

## 有什么用
- 承载绪论章写作的**过程状态**：gap 怎么提炼、现状怎么组织、绪论如何引出后续各章。
- 跨 session 接力：绪论可能在一个 session 起草、在另一个 session 改。

## 文件清单（全是 working notes，非正文）
具体文件名随 thesis-intro skill 设计定（该 skill 后续计划补）。常见类别：
gap 分析、研究现状综述、绪论结构（引出各章的逻辑）。

## 正文 tex 在哪（不在本目录）
绪论章 tex **直接写进 `../../thesis/tex/`**（章文件名遵循
`../../thesis/template-spec.md`）。**本目录永远不放 tex 正文。**

## 产物怎么进来
- **本 skill 自己产**：working notes，全由 thesis-intro 写。
- **从 `../thesis-sources.md` 读**（不复制）：读来源 registry 定位相关小论文。
- **从 `../thesis-spine.md` 读**（不复制）：读主线和 thesis 级 claim，确保绪论引出主线。

## 谁读它
人（读/改 notes）；thesis-spine（读绪论笔记感知主线是否在绪论正确引出）。
""",
    "thesis-theory": """# thesis-theory/ — 共用理论方法章工作笔记（working notes only）

> **这份文件是契约（contract）。** 本目录只放**过程元数据**（working notes），
> 不放正文产物。共用理论方法章 tex 直接写进 `../../thesis/tex/`，从不落在这里。

## 这个文件夹是什么
thesis-theory skill 的**工作笔记区**。写第二章（共用理论方法——各正文章共同依赖的
理论基础和实验方法）时的过程笔记。

## 有什么用
- 承载共用理论方法章写作的**过程状态**：如何把各小论文的理论方法统一成一章。
- 各正文章（thesis-dissect 产）共用这一章的理论基础——本目录笔记帮统一化决策。

## 文件清单（全是 working notes，非正文）
具体文件名随 thesis-theory skill 设计定（该 skill 后续计划补）。常见类别：
理论统一、方法共用化、各章理论依赖梳理。

## 正文 tex 在哪（不在本目录）
共用理论方法章 tex **直接写进 `../../thesis/tex/`**（章文件名遵循
`../../thesis/template-spec.md`）。**本目录永远不放 tex 正文。**

## 产物怎么进来
- **本 skill 自己产**：working notes，全由 thesis-theory 写。
- **从 `../thesis-sources.md` 读**（不复制）：读来源 registry 定位各小论文的理论方法。
- **从 `../thesis-spine.md` 读**（不复制）：读统一框架，确保本章理论与主线一致。

## 谁读它
人（读/改 notes）；thesis-dissect（读本章理论方法，写正文章时引用）。
""",
    "thesis-summary": """# thesis-summary/ — 总结展望章工作笔记（working notes only）

> **这份文件是契约（contract）。** 本目录只放**过程元数据**（working notes），
> 不放正文产物。总结展望章 tex 直接写进 `../../thesis/tex/`，从不落在这里。

## 这个文件夹是什么
thesis-summary skill 的**工作笔记区**。写末章（总结展望——共性提炼、各章 callback、
展望）时的过程笔记。

## 有什么用
- 承载总结展望章写作的**过程状态**：如何从各正文章提炼共性、如何 callback 各章 claim。
- 总结章是 thesis 级 claim 的收束——本目录笔记帮收束决策。

## 文件清单（全是 working notes，非正文）
具体文件名随 thesis-summary skill 设计定（该 skill 后续计划补）。常见类别：
共性提炼、callback 映射、展望（未来工作/局限）。

## 正文 tex 在哪（不在本目录）
总结展望章 tex **直接写进 `../../thesis/tex/`**（章文件名遵循
`../../thesis/template-spec.md`）。**本目录永远不放 tex 正文。**

## 产物怎么进来
- **本 skill 自己产**：working notes，全由 thesis-summary 写。
- **从 `../thesis-sources.md` 读**（不复制）：读来源 registry 感知全貌。
- **从 `../thesis-spine.md` 读**（不复制）：读 thesis 级 claim，确保总结收束主线。
- **从 `../thesis-dissect/chapter-map.md` 读**（不复制）：读各章 claim 做共性提炼和 callback。

## 谁读它
人（读/改 notes）；thesis-spine（读总结笔记感知 thesis 级 claim 是否收束）。
""",
}


# ----------------------------- helpers -----------------------------


def find_project_root(start: Path | None = None) -> Path:
    """项目根 = cwd 或 start。家族布局不强制在 git 根，
    就用调用者所在目录作为项目根。"""
    return Path(start) if start else Path.cwd()


def family_root(project_root: Path) -> Path:
    return project_root / FAMILY_ROOT_NAME


# templates/ live inside the plugin (sci-skills-thesis/templates/thesis/), resolved from
# this script: scripts → thesis-init → skills → sci-skills-thesis (plugin root, parents[3]).
# This keeps the plugin self-contained on standalone install — unlike article's repo-root
# templates/main/ which is a manual-copy pointer in CONTRACT prose only.
PLUGIN_TEMPLATES_DIR = Path(__file__).resolve().parents[3] / "templates" / "thesis"


def _resolve_template_pack(args) -> Path | None:
    """Find the template pack dir to weave. Returns None if user opted out."""
    if args.template_dir:
        d = Path(args.template_dir)
        if not d.is_dir():
            print(f"⚠ --template-dir 不存在: {d}")
            return None
        return d
    if args.template:
        # Bug 2 (aries MEDIUM): --template is documented as a pack NAME. Without
        # containment, an absolute path (--template /tmp/secret) bypasses the base
        # (Python Path join-on-absolute replaces the LHS) and a traversal
        # (--template ../../tmp/secret) climbs above the plugin — both copy an
        # arbitrary dir into thesis/tex/. Reject anything that isn't a simple name:
        # a bare name has PurePath(s).name == s; any path separator / absolute /
        # '..' makes them diverge. Also reject '..' outright (bare ".." has name==".."
        # so the name check alone misses it). PurePath is lexical — no FS access.
        name = args.template
        if PurePath(name).name != name or ".." in PurePath(name).parts:
            print(f"⚠ --template 必须是模板包名（不含路径），got: {name!r}")
            return None
        d = PLUGIN_TEMPLATES_DIR / args.template
        if not d.is_dir():
            print(f"⚠ 模板包不存在: {d}（可用: {', '.join(_available_packs())}）")
            return None
        return d
    packs = _available_packs()
    if len(packs) == 1:
        return PLUGIN_TEMPLATES_DIR / packs[0]
    if not packs:
        print("⚠ 无模板包（templates/thesis/ 为空）。thesis/tex/ 留空，待手动织入。")
        return None
    print(f"⚠ 多个模板包: {', '.join(packs)}。用 --template <name> 指定；本次跳过织入。")
    return None


def _available_packs() -> list[str]:
    if not PLUGIN_TEMPLATES_DIR.is_dir():
        return []
    return sorted(p.name for p in PLUGIN_TEMPLATES_DIR.iterdir() if p.is_dir())


def _weave_template(thesis_tex: Path, pack: Path) -> list[str]:
    """Copy pack contents into thesis/tex/, recursing into subdirs (real packs like
    thuthesis have config/figures subdirs). Idempotent: skip existing files/dirs.

    Symlink guard (aries #1): a malicious --template-dir pack can carry a symlink
    pointing outside itself (e.g. leaked_key.tex -> ~/.ssh/id_rsa). shutil.copyfile
    follows symlinks by default (follow_symlinks=True) and shutil.copytree(symlinks=False)
    follows dir symlinks — both copy the TARGET's content into tex/, which git add && push
    then exfiltrates. A legitimate template pack has no symlinks, so refuse them outright:
    detect is_symlink() BEFORE the is_dir()/is_file() branches (is_dir() follows symlinks
    and would route a symlink-to-dir into copytree) and skip with a warning."""
    report = []
    for src in pack.iterdir():
        if src.name.startswith(".") or src.name == "template-spec.md":
            # dotfiles + template-spec.md skipped: template-spec.md is copied explicitly to
            # thesis/template-spec.md (the canonical skill-facing location) by cmd_init —
            # weaving it here too would duplicate it into tex/. (E1)
            continue
        if src.is_symlink():
            # Bug 1: never follow a symlink in a template pack — its target (which may be
            # ~/.ssh/id_rsa or any file outside the pack) would be copied into tex/ and
            # later exfiltrated via git add && push. Skip the symlink entirely; do NOT copy
            # it as a symlink either (a symlink in tex/ still points at the target).
            report.append(f"  - ⚠ 跳过符号链接 {src.name}（模板包不应含符号链接）")
            continue
        dst = thesis_tex / src.name
        if src.is_dir():
            if dst.exists():
                report.append(f"  - tex/{src.name}/ 已存在（跳过）")
            else:
                shutil.copytree(src, dst)
                report.append(f"  - 织入 tex/{src.name}/")
        else:
            if dst.exists():
                report.append(f"  - tex/{src.name} 已存在（跳过）")
            else:
                shutil.copyfile(src, dst)
                report.append(f"  - 织入 tex/{src.name}")
    return report


# ----------------------------- init -----------------------------


def cmd_init(args: argparse.Namespace) -> int:
    root = find_project_root()
    report: list[str] = [f"init @ {root}"]

    # 0. thesis/ — first-class artifact. Build thesis/ + CONTRACT.md + tex/ (empty for now).
    #    CONTRACT.md written in BOTH branches (idempotent: skip if exists, write if new).
    th = root / THESIS_DIR_NAME
    th_contract = th / "CONTRACT.md"
    if th.exists():
        if not th_contract.exists():
            th_contract.write_text(THESIS_CONTRACT, encoding="utf-8")
            report.append(f"✓ {THESIS_DIR_NAME}/ 已存在，补 CONTRACT.md")
        else:
            report.append(f"✓ {THESIS_DIR_NAME}/ 已存在（跳过）")
    else:
        th.mkdir(parents=True)
        th_contract.write_text(THESIS_CONTRACT, encoding="utf-8")  # write CONTRACT.md (article-init:371 mirror)
        report.append(f"✓ 创建 {THESIS_DIR_NAME}/ + CONTRACT.md")
    # Bug 3 (aries MEDIUM): ensure thesis/tex/ exists in BOTH branches (idempotent).
    # Previously tex/ was created only inside the `else` (thesis/ absent); if thesis/
    # existed but tex/ had been deleted (corrupted weave / mid-run crash), the weave
    # below crashed with FileNotFoundError at copyfile's missing parent, and tex/ was
    # never recreated — the project was un-healable by init alone. mkdir(exist_ok=True)
    # here heals a deleted tex/ on re-run; the `else` branch no longer pre-creates it.
    tex_dir = th / "tex"
    if not tex_dir.exists():
        tex_dir.mkdir(parents=True)
        report.append(f"  - 创建 tex/（补建）")

    # 0b. weave the selected template pack into thesis/tex/ (templates ship inside the plugin,
    #     resolved via parents[3] — self-contained on standalone install). Idempotent.
    pack = _resolve_template_pack(args)
    if pack:
        report.extend(_weave_template(th / "tex", pack))
    # copy template-spec.md to thesis/ (top of thesis/, the skill-facing contract)
    spec_src = pack / "template-spec.md" if pack else None
    spec_dst = th / "template-spec.md"
    if spec_src and spec_src.is_file() and not spec_dst.exists():
        shutil.copyfile(spec_src, spec_dst)
        report.append("  - 织入 thesis/template-spec.md")

    # 1. family root (shared with article family — create if absent, never clobber existing article files)
    fam = family_root(root)
    if not fam.exists():
        fam.mkdir(parents=True)
        report.append(f"✓ 创建 {FAMILY_ROOT_NAME}/")

    # 2. top-level shared files (thesis- prefixed). Skip if exists; never overwrite.
    for name, content in SHARED_FILES_PLACEHOLDERS.items():
        p = fam / name
        if p.exists():
            report.append(f"  - {name} 已存在（跳过）")
        else:
            p.write_text(content, encoding="utf-8")
            report.append(f"  - 创建 {name}")

    # 3. thesis-README.md (thesis-owned routing table — NOT README.md, which the article
    #    family may own in a coexist project; thesis- prefix avoids the collision).
    readme = fam / "thesis-README.md"
    if not readme.exists():
        readme.write_text(_readme_text(), encoding="utf-8")
        report.append("  - 创建 thesis-README.md")

    # 4. brother skill dirs + CONTRACT.md
    for skill in BROTHER_SKILLS:
        sd = fam / skill
        c = sd / "CONTRACT.md"
        if sd.exists():
            if not c.exists() and skill in SKILL_DIR_CONTRACTS:
                c.write_text(SKILL_DIR_CONTRACTS[skill], encoding="utf-8")
                report.append(f"  - {skill}/ 已存在，补 CONTRACT.md")
            else:
                report.append(f"  - {skill}/ 已存在（跳过）")
        else:
            sd.mkdir()
            c.write_text(SKILL_DIR_CONTRACTS.get(skill, f"# {skill}/\n\nReserved.\n"), encoding="utf-8")
            report.append(f"  - 创建 {skill}/ + CONTRACT.md")

    # 5. thesis/.gitignore (thesis-scoped — LaTeX build products). Written INSIDE thesis/,
    #    not at project root, so it never collides with an article-family .gitignore.
    #    Root .gitignore is the human's/article's concern; init does not touch it.
    gi = th / ".gitignore"
    if not gi.exists():
        gi.write_text("\n".join([
            "# LaTeX build products", "*.aux", "*.log", "*.out", "*.toc", "*.bbl", "*.blg",
            "*.fls", "*.fdb_latexmk", "*.synctex.gz", "",
        ]) + "\n", encoding="utf-8")
        report.append("  - 创建 thesis/.gitignore")

    # 6. git init (unless --no-git) — mirror article-init
    if (root / ".git").is_dir():
        report.append("✓ .git/ 已存在（跳过）")
    elif args.no_git:
        report.append("· 跳过 git init（--no-git）")
    else:
        try:
            subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True, text=True)
            report.append("✓ git init")
        except FileNotFoundError:
            report.append("⚠ git 未安装，跳过 git init（请手动 git init）")
        except subprocess.CalledProcessError as e:
            report.append(f"⚠ git init 失败: {e.stderr.strip()}")

    print("\n".join(report))
    return 0


# ----------------------------- checkup helpers -----------------------------


def list_root_candidates(root: Path) -> list[dict]:
    """列出项目根下不在标准位置的内容（thesis/、sci-skills/、.git 之外的东西）。
    浅层扫描，只给 checkup 当"该派 Explore 深查"的信号——**不下结论**这些是什么、
    该进哪。判断（这是不是正文、是不是老图仓库）由 Explore agent 读懂内容后做，
    脚本写死规则会误判用户文件。镜像 article-init 的同名函数，区别仅在标准位置
    名（manuscript/ → thesis/）。
    """
    entries: list[dict] = []
    if root.is_dir():
        for entry in sorted(root.iterdir()):
            if entry.name in {FAMILY_ROOT_NAME, THESIS_DIR_NAME, ".git"}:
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
    """体检：扫描当前结构，报告 thesis/ + sci-skills/ 落盘位置对不对。

    镜像 article-init 的 cmd_checkup：misplaced-items 扫描 + git 状态 + JSON block
    （供程序化消费）。git 未 init 不计入 issues——thesis-init 的 --no-git 是一等选项，
    且 thesis 家族常与 article 共存于已 git 化的仓库；只报告、不报警。
    """
    root = find_project_root()
    fam = family_root(root)
    report: list[str] = [f"checkup @ {root}"]
    issues: list[str] = []
    # TODO: align JSON key with article-init's "family_root_exists" for cross-family consumers
    info: dict = {
        "project_root": str(root),
        "thesis": {},
        "sci-skills": {"present": fam.is_dir()},
        "skills": {},
    }

    # 0. thesis/（一等公民，先报）。checkup verifies weave integrity: tex/ present?
    #    main.tex present? (.cls is informational only — generic-test uses native report
    #    class with none; real packs like thuthesis ship one). template-spec.md present?
    th = root / THESIS_DIR_NAME
    if not th.is_dir():
        issues.append(f"✗ {THESIS_DIR_NAME}/ 不存在。跑 `init` 建它。")
        info["thesis"] = {"present": False}
    else:
        info["thesis"] = {"present": True}
        tex_dir = th / "tex"
        if not tex_dir.is_dir():
            # tex/ dir itself missing — partial init (template weave didn't run / was deleted).
            # Do NOT silently report "tex 文件: 0"; surface the broken weave.
            report.append(f"thesis/   ✓  tex/ ✗ 缺失")
            issues.append(f"⚠ {THESIS_DIR_NAME}/tex/ 缺失（init 未完整跑完？）")
            info["thesis"]["tex_dir"] = False
        else:
            tex_files = list(tex_dir.glob("*.tex"))
            cls_files = sorted(p.name for p in tex_dir.glob("*.cls"))  # informational only
            main_tex = tex_dir / "main.tex"
            info["thesis"].update({
                "tex_dir": True,
                "tex_file_count": len(tex_files),
                "main_tex": main_tex.is_file(),
                "cls_files": cls_files,
            })
            cls_note = ", ".join(cls_files) if cls_files else "(无 — 原生 report 类)"
            report.append(
                f"thesis/   ✓  tex 文件: {len(tex_files)}  "
                f"main.tex: {'✓' if main_tex.is_file() else '✗'}  .cls: {cls_note}"
            )
            # main.tex is the universal compile entry point — every pack ships one; its
            # absence means the weave didn't complete or it was deleted.
            if not main_tex.is_file():
                issues.append(
                    f"⚠ {THESIS_DIR_NAME}/tex/main.tex 缺失（模板未完整织入？）"
                )
        if not (th / "template-spec.md").is_file():
            issues.append(f"⚠ {THESIS_DIR_NAME}/template-spec.md 缺失（模板未织入？）")

    # 1. sci-skills/ 共享工作区
    if not fam.is_dir():
        issues.append(f"✗ {FAMILY_ROOT_NAME}/ 不存在。跑 `init` 建它。")
    else:
        for name in SHARED_FILES_PLACEHOLDERS:
            if not (fam / name).is_file():
                issues.append(f"⚠ {FAMILY_ROOT_NAME}/{name} 缺失")
        if not (fam / "thesis-README.md").is_file():
            issues.append("⚠ sci-skills/thesis-README.md 缺失")
        # 1b. 各兄弟子目录 + CONTRACT.md 状态（表格化，镜像 article-init）
        report.append(f"\n{'skill':<16} {'目录':<8} {'文件数':<8} 状态")
        report.append("-" * 50)
        for skill in BROTHER_SKILLS:
            sd = fam / skill
            if not sd.is_dir():
                report.append(f"{skill:<16} {'—':<8} {'—':<8} 缺失（按需 init）")
                info["skills"][skill] = {"present": False}
                continue
            if not (sd / "CONTRACT.md").is_file():
                issues.append(f"⚠ {FAMILY_ROOT_NAME}/{skill}/CONTRACT.md 缺失")
            files = [p for p in sd.rglob("*") if p.is_file() and p.name != "CONTRACT.md"]
            report.append(
                f"{skill:<16} {'✓':<8} {len(files):<8} {'空' if not files else '有产物'}"
            )
            info["skills"][skill] = {"present": True, "file_count": len(files)}

    # 2. 项目根错位（浅层信号——脚本不下结论这些是什么、该进哪；判断派 Explore）
    root_cands = list_root_candidates(root)
    if root_cands:
        info["root_candidates"] = root_cands
        cand_names = ", ".join(c["name"] for c in root_cands)
        issues.append(
            f"⚠ 项目根有 {len(root_cands)} 项不在 {THESIS_DIR_NAME}/ 或 "
            f"{FAMILY_ROOT_NAME}/ 下（{cand_names}）。派 Explore agent 读懂这些内容、"
            f"判断归位（正文→{THESIS_DIR_NAME}/tex/，老图→{FAMILY_ROOT_NAME}/ 等），"
            "跟用户确认后发 mv。脚本不自动判断、不自动移。"
        )

    # 3. git 状态（只报告，不计入 issues——见 docstring 的 --no-git 说明）
    git_present = (root / ".git").is_dir()
    info["git"] = git_present
    report.append(f"\ngit/   {'✓ 已 git init' if git_present else '· 未 git init（--no-git 或尚未 init）'}")

    report.append("")
    if issues:
        report.append("问题:")
        for it in issues:
            report.append(f"  {it}")
    else:
        report.append("✓ 布局健康。")

    info["issues"] = issues
    print("\n".join(report))
    print("\n--- JSON ---\n" + json.dumps(info, ensure_ascii=False, indent=2))
    return 1 if issues else 0


# ----------------------------- main -----------------------------


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="sci-skills-thesis 家族项目初始化 / 体检。手动触发，跑一次就退。")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_init = sub.add_parser("init", help="建 thesis/ + sci-skills/ 骨架 + 织入模板")
    p_init.add_argument("--no-git", action="store_true")
    p_init.add_argument("--template", default=None, help="模板包名 (templates/thesis/<name>)")
    p_init.add_argument("--template-dir", default=None, help="用户自带 .cls+spec 目录（degraded）")
    p_init.set_defaults(func=cmd_init)
    p_chk = sub.add_parser("checkup", help="体检落盘位置")
    p_chk.set_defaults(func=cmd_checkup)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
