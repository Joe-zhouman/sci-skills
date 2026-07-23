# 峰拟合细则

正文 §2.4 给了峰函数选择和拟合命令。这里展开：peaks.json 结构、怎么设初始值和约束、自旋-轨道分裂双峰、失败排查。

## peaks.json 结构（纯数据，不含方法选择）

```json
{
  "region_label": "Si 2p",
  "energy_range": [107, 97],
  "peaks": [
    {
      "label": "Si3N4",
      "center":        101.8,  "center_range":  [101.2,  102.4],
      "sigma":          1.30,  "sigma_range":   [0.5,    2.5],
      "amplitude":   8000.0,   "amplitude_range": [1000, 20000]
    },
    {
      "label": "SiNx",
      "center":        101.1,  "center_range":  [100.6,  101.6],
      "sigma":          1.20,  "sigma_range":   [0.5,    2.5],
      "amplitude":   3000.0,   "amplitude_range": [500,  15000]
    },
    {
      "label": "Si0",
      "center":        99.60,  "center_range":  [99.0,   100.2],
      "sigma":          0.50,  "sigma_range":   [0.3,    1.5],
      "amplitude":   2000.0,   "amplitude_range": [200,  10000]
    }
  ]
}
```

峰函数不在这里——那是方法选择，走命令行 `--peak-function`，不属于数据文件。

## 怎么设初始值

1. 看扣除基线后的谱，目视有几个"鼓包"。
2. 查 NIST，这些位置对应什么化学态。
3. 每个候选峰设初始值：
   - `center`：峰位（NIST 给的 be_mean）
   - `sigma`：宽度，约 FWHM/2.355
   - `amplitude`：高度（数据里那个峰的 counts）
4. 设约束范围——**这是叙事的关键**：
   - `center_range`：松一点让拟合自己找最优，紧一点锁死在你想要的化学态位置
   - `sigma_range`：0.5–2.5 eV 是 XPS 典型范围
   - `amplitude_range`：必须 > 0

## 自旋-轨道分裂双峰

p、d、f 轨道会分裂成双峰（j–j 耦合），s 轨道不分裂。分裂间距和面积比是物理常数——不随样品变。

遇到分裂轨道，peaks.json 里要**成对放**、约束间距（`center_range` 差值锁死）和面积比（`amplitude_range` 反映比例）。

### 常用双峰参数

数据来源：Moulder et al. *Handbook of XPS* (1992)，NIST SRD 20。物理常数不更新，但完整表以 Handbook 为准。

#### p 轨道：2p₃/₂ + 2p₁/₂，面积比 2:1

| 元素 | 轨道 | 分裂 (eV) | 是否可分辨（实验室 XPS） |
|---|---|---|---|
| Si | 2p | 0.60 | ⚠️ 勉强——峰宽常大于分裂，不分成对拟合不合理 |
| Al | 2p | 0.44 | ✗ 不可分辨——单峰勉强够，分成对更严谨 |
| P | 2p | 0.84 | ⚠️ 勉强 |
| S | 2p | 1.18 | ✓ 可分辨 |
| Cl | 2p | 1.60 | ✓ 可分辨 |
| Sc | 2p | 4.0 | ✓ 清晰可辨 |
| Ti | 2p | 5.54 | ✓ 清晰可辨 |
| V | 2p | 7.5 | ✓ 清晰可辨 |
| Cr | 2p | 8.7 | ✓ 清晰可辨（常按独立峰处理） |
| Mn | 2p | 11.0 | ✓ 清晰可辨（常按独立峰处理） |
| Fe | 2p | 13.1 | ✓ 清晰可辨（常按独立峰处理） |
| Co | 2p | 16.0 | ✓ 常按独立峰处理 |
| Ni | 2p | 17.3 | ✓ 常按独立峰处理 |
| Cu | 2p | 19.8 | ✓ 常按独立峰处理 |
| Zn | 2p | 23.1 | ✓ 常按独立峰处理 |

> 过渡金属 2p 分裂 ≥~10 eV 时，通常当成两个独立单峰拟合、各自配卫星峰，而非一个自旋-轨道对。只有分裂 <~5 eV 的轻元素 2p 才严格双峰约束。

#### d 轨道：d₅/₂ + d₃/₂，面积比 3:2

| 元素 | 轨道 | 分裂 (eV) | 是否可分辨 |
|---|---|---|---|
| Zr | 3d | 2.4 | ✓ 可分辨 |
| Nb | 3d | 2.7 | ✓ 可分辨 |
| Mo | 3d | 3.13 | ✓ 可分辨 |
| Ru | 3d | 3.98 | ✓ 清晰可辨 |
| Rh | 3d | 4.75 | ✓ 清晰可辨 |
| Pd | 3d | 5.26 | ✓ 清晰可辨 |
| Ag | 3d | 5.99 | ✓ 清晰可辨 |
| Cd | 3d | 6.77 | ✓ 清晰可辨 |
| In | 3d | 7.54 | ✓ 清晰可辨 |
| Sn | 3d | 8.40 | ✓ 清晰可辨 |
| Ta | 4f | 1.91 | ✓ 可分辨 |
| W | 4f | 2.17 | ✓ 可分辨 |
| Ir | 4f | 2.95 | ✓ 可分辨 |
| Pt | 4f | 3.33 | ✓ 可分辨 |
| Au | 4f | 3.67 | ✓ 可分辨 |
| Pb | 4f | 4.84 | ✓ 清晰可辨 |

#### f 轨道：f₇/₂ + f₅/₂，面积比 4:3

| 元素 | 轨道 | 分裂 (eV) | 是否可分辨 |
|---|---|---|---|
| Ce | 4f | 很多组分，不用简单双峰 | — |
| U | 4f | 10.9 | ✓ 清晰可辨 |
| Th | 4f | 9.6 | ✓ 清晰可辨 |

> f 轨道元素（镧系/锕系）XPS 谱通常非常复杂（多重组态、shake-up），这张表只覆盖最常见的几个。镧系元素完整数据以 *Handbook of XPS* 为准。

### 在 peaks.json 中约束双峰

以 Ag 3d 为例，单个双峰约束为两个 peak entry：

```json
{
  "label": "Ag 3d5/2",
  "center": 368.21,
  "center_range": [367.5, 369.0],
  "sigma": 0.80,  "sigma_range": [0.3, 1.5],
  "amplitude": 10000, "amplitude_range": [1000, 50000]
},
{
  "label": "Ag 3d3/2",
  "center": 374.20,
  "center_range": [373.5, 375.0],
  "sigma": 0.80,  "sigma_range": [0.3, 1.5],
  "amplitude": 6667, "amplitude_range": [667, 33333]
}
```

- `center` 差值 = 分裂值（~5.99 eV for Ag 3d），`center_range` 允许 ±0.5 eV 浮动
- `amplitude` 比例 ≈ 3:2（d₅/₂ : d₃/₂），`amplitude_range` 同样按比例设
- **σ 设相同**——同一轨道的两个自旋分量物理上等宽，`sigma_range` 也设相同

### 什么轨道不分裂

s 轨道（C 1s, N 1s, O 1s, F 1s, Na 1s, Mg 2s, Al 2s, Si 2s, P 2s, S 2s 等）——单峰即可。

### 表中没有的元素？用脚本查本地 NIST

上表覆盖了最常见的元素。表中没有的，用本地 NIST 镜像推算：

```bash
python scripts/lookup_be.py <元素> --line <轨道> --split --format json
```

脚本逻辑：从 NIST 本地库中匹配同一篇论文同时报告了两个 j 分量的记录，算 splitting 均值 ± 标准差。至少 3 对匹配才采用 matched-pair 模式，否则降级为 global-mean（精度更低，带 warning）。

⚠️ NIST 数据中两个自旋分量的记录数严重不平衡（e.g. Si 2p3/2 有 738 条 vs 2p1/2 只有 8 条），splitting 推算值是近似值。**表中已有的值以表为准**（来自 Handbook of XPS 的系统测量），脚本用于表中没有的元素或快速验证。

### 查 FWHM 参考值

设 `sigma_range` 时需要知道目标材料的典型 FWHM。用本地 NIST 镜像查：

```bash
python scripts/lookup_be.py Si --line 2p --fwhm --format json       # 某元素某轨道的 FWHM 统计
python scripts/lookup_be.py Si3N4 --fwhm --format json              # 按化合物的 FWHM
```

输出含 mean/std/min/max/median + per-formula top-15 明细 + 材料类型提示。仅 12.6% 的 NIST 记录含 FWHM，数据可能稀疏——此时以本文件的 FWHM 典型范围表为准。

### 更新路径

完整双峰参数以 Moulder et al. *Handbook of X-ray Photoelectron Spectroscopy* (Physical Electronics, 1992) 为准（公认金标准）。NIST SRD 20 也收录了大部分元素的 spin-orbit splitting 数据：<https://srdata.nist.gov/xps/>

## 失败排查

拟合器可能不收敛或给出不合理结果：

- **R² < 0.8**：峰数不对、函数不对、或初始值太离谱
- **参数顶到边界**：约束太紧——放宽 `*_range`
- **某个峰宽度趋近于 0**：这个峰可能不存在，减少峰数
- **残差有系统性结构**（不是随机噪声）：缺了峰、或峰形不对

排查顺序：减少峰数 → 换峰函数 → 放宽约束 → 调整基线端点 → 检查数据质量。**不要接受一个差的拟合然后说"就这样吧"。**

> 以上是单步排查。系统化的迭代策略（先调什么、残差怎么读、什么时候停）见 `references/fitting-strategy.md`。

## FWHM 典型范围

用于设 `sigma_range` 的合理性边界。FWHM = 2.355 × σ。

| 材料类型 | 典型 FWHM (eV) | 原因 |
|---|---|---|
| 纯金属（单晶） | 0.3–0.6 | 窄：高电导、无荷电、无化学态分散 |
| 半导体（Si, Ge 等） | 0.5–0.9 | 窄-中：电导较好 |
| 氧化物/无机绝缘体 | 0.9–1.8 | 中-宽：荷电效应、轻微化学态分散 |
| 聚合物/有机物 | 0.8–1.4 | 中：不同化学环境的 C 轻微重叠 |
| 玻璃/陶瓷 | 1.2–2.5 | 宽：无定形结构、化学态连续分散 |
| 过渡金属氧化物 | 1.5–3.0 | 很宽：多重态分裂（multiplet splitting）、卫星峰 |
| 稀土元素 3d | 2.0–5.0+ | 极宽：复杂多重组态、shake-up/off |

**使用规则**：
- `sigma_range` 设为 `[0.3, 2.5]` 覆盖绝大多数情况
- FWHM < 0.3 eV 在实验室 XPS 几乎不可能（仪器展宽就 ~0.3–0.5 eV）
- 拟合出来 σ 趋近于 0 → 峰不存在，减少峰数
- 同一化学态不同样品间的 FWHM 变化 < 0.2 eV 是正常的，> 0.5 eV 要怀疑拟合是否有问题

> 以上为通用参考。特定化合物/体系的实测 FWHM 用 `lookup_be.py --fwhm` 查本地 NIST 镜像。XPS 仪器的固有展宽（取决于 analyzer pass energy + X 射线线宽）对所有峰施加同一个下限。同一份数据里所有峰的 FWHM 都不应小于仪器展宽。在 report.md 的方法部分注明 pass energy，让读者可以评估仪器展宽的量级。

## 不确定度

lmfit 自动输出每个参数的 ±stderr。report.md 里必须带上——只报峰位不报 ±stderr = 给人"精确无误"的错觉。
