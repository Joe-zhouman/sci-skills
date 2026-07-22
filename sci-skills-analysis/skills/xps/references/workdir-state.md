# state.json 详解

正文 §工作目录 给了目录树和"第一步跑 `state.py status`"的流程。这里展开 state.json 的完整 schema、字段含义、evidence 追加逻辑、产出物清单。

## state.py —— state.json 的唯一管理者

state.json **不手写编辑**。`scripts/state.py` 四个子命令覆盖所有操作：

| 子命令 | 干什么 |
|---|---|
| `state.py init` | 建工作目录树 + 空 state.json（幂等：已存在不动） |
| `state.py status` | 读 state.json，报告 region 进度 + evidence + 下一步建议 |
| `state.py set-region <label> --status <s>` | 建 region 子目录 + 推进状态（explored→fitting→done，不可逆除非 `--force`） |
| `state.py add-evidence <file> -t <tech> -d <desc> -n <name>` | 复制文件到 evidence/ + 追加到 state.evidence |

工作目录固定 `<cwd>/sci-skills/sci-analysis/xps/`。原子写（temp+rename），崩了不会写坏 state.json。`status` 的 `next_steps` 是启发式提示（claim 缺没、region 卡哪、是否该收尾），非强制——你判断。

report.md 不由 state.py 生成——那是叙事，你按 `references/report-template.md` 写。

## state.json schema

```json
{
  "claim": "证明改性后 Si₃N₄ 成为主要相，Si⁰ 减少",
  "created": "2026-07-22",
  "updated": "2026-07-22",
  "evidence": [
    {
      "technique": "XRD",
      "description": "显示 Si₃N₄ 特征峰 (2θ=33.7°)，与 XPS 中 Si₃N₄ 组分相互印证",
      "source_file": "evidence/xrd_si3n4.png",
      "added": "2026-07-22"
    }
  ],
  "regions": [
    {
      "label": "Si 2p",
      "sub_claim": "Si₃N₄ 为主组分，Si⁰ 微量存在",
      "status": "fitting",
      "dir": "si2p",
      "data_source": "原始数据: 2/2/si2p.txt",
      "nist_ref": "Si₃N₄ 2p₃/₂ ≈ 101.9 eV (Ingo & Zacchetti, High Temp. Sci. 28, 1990)"
    }
  ],
  "comparisons": [
    {
      "label": "Si 2p before vs after cycling",
      "regions": ["si2p_before", "si2p_after"],
      "dir": "comparison"
    }
  ]
}
```

## 字段

- `claim` — 整个分析的叙事核心。每次修改就回到第二阶段重新审视。
- `evidence` — 其他表征手段列表，空数组 = 没有。**每次用户提到新证据，主动追加。**
- `regions` — 已加载/已开始分析的光谱区域。status: `explored` → `fitting` → `done`。
- `comparisons` — 对比图，跨 region 引用。

## 用户提供 evidence 时的处理

用户给图片或描述（TEM、XRD、Raman、EDS 等）：

1. **跑 `state.py add-evidence`**：复制文件到 `evidence/` + 追加到 state.evidence（一条命令搞定，不手写 JSON）。
   ```bash
   python scripts/state.py add-evidence ~/xrd.png -t XRD -d "Si3N4 2theta=33.7" -n xrd_si3n4.png
   ```
2. **问用户**：这个证据说了什么？和 claim 一致吗？把回答记到 evidence entry 的 description（再跑一次 add-evidence 覆盖，或直接问完再追加）。

<HARD-GATE>图片必须复制到 evidence/ 下，不能靠用户文件系统的原始路径——那个路径以后可能不存在。`add-evidence` 强制复制，正为此。</HARD-GATE>

## 产出物清单

每完成一个 region 的拟合，落盘：

| 文件 | 内容 | 干什么用 |
|---|---|---|
| `<dir>/fit_<label>.py` | 可复现脚本 | 别人跑一遍出同样结果 |
| `<dir>/fit_<label>.pdf` | 矢量图 | **拖进 Origin 可编辑**（解组后每个元素都能改） |
| `<dir>/fit_<label>.png` | 位图预览 | 组会直接贴 |
| `<dir>/fit_<label>.csv` | x, y_raw, y1, y2, …, yf | **拖进 Origin 重绘**（数据列齐全） |
| `report.md` | 叙事报告 | claim → 各 region 发现 → evidence 印证 → 局限性 |

Origin 用户两条路：PDF 进去改图（字体/颜色/标注），或 CSV 进去自己重画。两条路不冲突。
