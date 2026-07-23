# RSF 定量：从峰面积到原子%

正文 report-template 提到"相对面积 % 是半定量的，缺 RSF 校正"。这份文件补上：RSF 数据 + 定量公式 + 怎么用。

> **加载时机**：当需要从峰面积算原子%时读。日常峰位/线形分析不需要。
>
> **怎么帮用户拿到仪器 RSF** → `rsf-sources.md`：各平台 RSF 在哪、外包测试怎么问测试老师、拿到了怎么处理。

## 公式

XPS 定量基本公式（均质样品，忽略弹性散射效应）：

$$\text{Atom\%}_A = \frac{I_A / \text{RSF}_A}{\sum_i I_i / \text{RSF}_i} \times 100\%$$

其中：
- $I_A$ = 元素 A 的峰面积（扣除基线后，来自 `fit.json` 的 `peaks[].amplitude` 积分或组分面积求和）
- $\text{RSF}_A$ = 元素 A 对应轨道的相对灵敏度因子

**严格定量还需要 IMFP 修正**：

$$\text{Atom\%}_A = \frac{I_A / (\text{RSF}_A \cdot \lambda_A)}{\sum_i I_i / (\text{RSF}_i \cdot \lambda_i)} \times 100\%$$

其中 $\lambda$ = 非弹性平均自由程（IMFP），与电子动能相关。常用近似：$\lambda \propto E_{\text{kin}}^{0.6}$（TPP-2M 的经验简化）。

> **本 skill 的策略**：优先让用户提供仪器厂家的 RSF 表（从 XPS 软件导出的），跟你从用户那要 claim 和其他表征证据一样——这是他们的数据，他们仪器配的 RSF 最准。拿不到再 fallback 到 Scofield t-RSF（理论截面）。

## Scofield RSF 表（Al Kα, 1486.6 eV）

归一化到 C 1s = 1.000。数据来源：Scofield, J.H. (1976) *J. Electron Spectrosc. Relat. Phenom.* 8, 129–137，Hartree-Fock-Slater 单电子中心场势计算。

### s 轨道（1s, 2s, 3s…）

| 元素 | 轨道 | Scofield RSF |
|---|---|---|
| Li | 1s | 0.057 |
| Be | 1s | 0.172 |
| B | 1s | 0.405 |
| C | 1s | 1.000 |
| N | 1s | 1.678 |
| O | 1s | 2.930 |
| F | 1s | 4.430 |
| Na | 1s | 8.520 |
| Mg | 2s | 1.047 |
| Al | 2s | 0.935 |
| Si | 2s | 1.074 |
| P | 2s | 1.332 |
| S | 2s | 1.635 |

### p 轨道（2p, 3p…）

| 元素 | 轨道 | Scofield RSF |
|---|---|---|
| Na | 2p | 2.018 |
| Mg | 2p | 2.042 |
| Al | 2p | 1.854 |
| Si | 2p | 2.115 |
| P | 2p | 2.596 |
| S | 2p | 3.153 |
| Cl | 2p | 3.661 |
| K | 2p | 5.070 |
| Ca | 2p | 5.070 |
| Sc | 2p | 6.02 |
| Ti | 2p | 7.12 |
| V | 2p | 8.28 |
| Cr | 2p | 9.51 |
| Mn | 2p | 10.82 |
| Fe | 2p | 12.23 |
| Co | 2p | 13.71 |
| Ni | 2p | 15.32 |
| Cu | 2p | 16.95 |
| Zn | 2p | 18.65 |
| Ga | 2p | ~20.5 |
| Ge | 2p | ~22.5 |

### d 轨道（3d, 4d）

| 元素 | 轨道 | Scofield RSF |
|---|---|---|
| Ga | 3d | 1.89 |
| Ge | 3d | 2.69 |
| As | 3d | 3.55 |
| Se | 3d | 4.47 |
| Br | 3d | 5.44 |
| Rb | 3d | 6.93 |
| Sr | 3d | 7.94 |
| Y | 3d | 9.05 |
| Zr | 3d | 10.14 |
| Nb | 3d | 11.36 |
| Mo | 3d | 12.63 |
| Ru | 3d | 14.29 |
| Rh | 3d | 15.82 |
| Pd | 3d | 17.41 |
| Ag | 3d | 19.03 |
| Cd | 3d | 20.68 |
| In | 3d | 22.41 |
| Sn | 3d | 24.12 |
| Sb | 3d | 25.96 |
| Te | 3d | 27.95 |
| I | 3d | 29.98 |
| Cs | 3d | 33.19 |
| Ba | 3d | 35.42 |
| La | 3d | 37.65 |

### f 轨道（4f）

| 元素 | 轨道 | Scofield RSF |
|---|---|---|
| Hf | 4f | 8.41 |
| Ta | 4f | 9.39 |
| W | 4f | 10.48 |
| Ir | 4f | 12.66 |
| Pt | 4f | 13.98 |
| Au | 4f | 17.47 |
| Hg | 4f | 18.80 |
| Tl | 4f | 20.03 |
| Pb | 4f | 21.38 |
| Bi | 4f | 22.72 |

> ⚠️ 上表数值来自多个 XPS 手册交叉验证，但**发表论文前必须在 Scofield (1976) 原文或仪器厂家提供的 RSF 表中复核**。过渡金属和稀土元素（特别是含未填满 d/f 壳层的元素）的定量误差较大——多重组态和卫星峰使得"峰面积"的定义本身就是模糊的。

## 使用方式

### 手动算

从 `fit.json` 中取每个 region 的峰面积加和 → 除以对应轨道的 RSF → 归一化。

### 脚本（待实现）

```bash
python scripts/quantify.py -f si2p/fit.json n1s/fit.json o1s/fit.json -o atom_percent.json
```

输入：多个 `fit.json`（每个代表一个元素/区域），脚本自动：
1. 对每个 region 的峰面积求和
2. 根据 `region_label` 或用户指定的轨道名查 RSF 表
3. 计算原子%，输出带 RSF 和 IMFP 修正标志的结果

## Scofield vs Wagner vs 仪器厂家 RSF

| RSF 来源 | 类型 | 优点 | 缺点 |
|---|---|---|---|
| **Scofield (t-RSF)** | 理论截面 | 普适、可复现、不受仪器限制 | 忽略仪器传输函数、忽略弹性散射各向异性 |
| **Wagner (e-RSF)** | 经验测量 | 含仪器响应、更准（对特定仪器） | 仪器依赖——换台机器不一样 |
| **仪器厂家 RSF** | 经验+理论混合 | 针对你的仪器优化 | 不同厂家的值不互通 |

**本 skill 的优先级：**
1. 用户提供的仪器厂家 RSF（从 XPS 软件导出，最准）
2. 如果用户不知道/拿不到 → Scofield t-RSF（本文件的表）
2. 如果 Scofield 表中没有该元素/轨道 → 查 NIST 或 Scofield (1976) 原文

## 已知局限

1. **Scofield RSF 忽略角分布各向异性**——假定光电子发射各向同性（魔角条件）。实际测量偏离魔角时会有误差。
2. **过渡金属 d 轨道和稀土 f 轨道**定量精度差——复杂的卫星结构使基线扣除和峰面积定义不唯一。这是 XPS 定量的本质限制，不是 RSF 能解决的。
3. **忽略弹性散射**——均质样品假设。纳米颗粒、粗糙表面、层状样品不适用。
4. **IMFP 近似**——TPP-2M 公式本身有不确定性，$E_{\text{kin}}^{0.6}$ 是进一步简化。

在 report.md 的局限性节（§4）必须声明使用了哪套 RSF 和是否做了 IMFP 修正。

## 更新路径

### 补充完整 RSF 表

当前表覆盖常用元素（~70 个 entry）。完整 Scofield 表含所有元素全部轨道（Z=3–100，~400+ entry）。补充方式：
1. 从 Scofield (1976) 原文 JESRP 8, 129–137 提取完整截面数据
2. 或从 XPS 手册（如 PHI Handbook、CasaXPS 内置表）获取
3. 或从公开数据库：<https://xpsdatabase.com/quantitation-rsfs-and-atom-results/> （R.N. King 编制，图片格式，需手动转录）

### 换 Wagner RSF

如果用户提供了 Wagner 经验 RSF（仪器导出），替换上表中的值即可。Wagner RSF 通常归一化到 F 1s = 1.000（而非 C 1s = 1.000），注意归一化基准的差异。

### 参考论文

- Scofield, J.H. (1976) *J. Electron Spectrosc. Relat. Phenom.* 8, 129–137 — 原始截面计算
- Wagner, C.D. et al. (1981) *Surf. Interface Anal.* 3, 211–225 — Wagner 经验 RSF
- Brundle, C.R. & Crist, B.V. (2020) *J. Vac. Sci. Technol. A* 38, 041001 — XPS 定量精度综述
