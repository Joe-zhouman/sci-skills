# 基线扣除细则

正文 §2.3 给了四方法表、命令、和"基线是叙事旋钮"的判断。这里展开端点选择策略和各方法的物理细节。

## 端点怎么选

在峰两侧各找一个"看起来回到基线"的平坦区域。**端点直接决定峰面积——往外扩一点面积就大一点。** 这是另一个旋钮，迭代时可调。每次拟合记录端点选择（bg.json 的 metadata 里已有 `region` 字段）。

## 各方法的物理意义

- **Shirley**：迭代 S 形，假设非弹性散射电子在低动能侧累积。通用默认，绝大多数情况最稳。
- **Tougaard**：通用散射截面卷积，最物理（B=2866 eV², C=1643 eV² 通用参数）。需要散射参数时用，参数不对反而更差。
- **多项式**：取两端外侧点做 polyfit。快速探索用，degree 越高越灵活也越容易过拟合端点。
- **Linear**：两点直线。聚合物、大带隙材料、噪声太大时——这些体系基线本来就平。

## 不同材料该用什么

- **金属**：Shirley 最好（有非弹性散射电子累积）。
- **绝缘体/聚合物**：基线通常很平，Linear 或低次多项式足够。
- **含多个峰的宽区域**：Tougaard 最物理，但需要散射截面参数。

## 端点选错会怎样

端点往外扩 → 峰面积变大 → 原子%变高 → 直接影响结论。这也是为什么它是叙事旋钮：同一个峰，端点选得宽一点，你想强调的那个组分面积就大一点。**用这个自由度时要意识到自己在用它，并在 report 里记录端点。**

> 基线端点和峰面积/峰数的互动关系见 `fitting-strategy.md` 的旋钮影响力排名和残差读数法。

## Tougaard 参数详解

### 本 skill 实际用的参数

`subtract_background.py -m tougaard` 调用 `lmfitxps.backgrounds.tougaard_calculate()`。该函数使用 **4-PIESCS**（四参数非弹性电子散射截面）公式：

$$B_T(E) = \int_{E}^{\infty} \frac{B \cdot T}{(C + C_d \cdot T^2)^2 + D \cdot T^2} \cdot y(E') \, dE'$$

其中 $T = E' - E$（能量差）。

**脚本行为**：
- **B**：从起始值 2866 eV² 开始，**迭代优化**到背景在低 BE 端归零（这是 Tougaard 方法的核心：B 是 scaling factor，不应固定）
- **C, C_d, D**：使用 lmfitxps 的默认值，**拟合过程中固定不变**
- 输出 `bg.json` 的 metadata 不记录 B 的最终值（目前没有暴露——需要时加 `--verbose`）

### lmfitxps 默认参数

lmfitxps 内置两套默认值：

| 函数 | B 起始值 | C | C_d | D | 等价模型 |
|---|---|---|---|---|---|
| `tougaard_calculate()` | 2866 | 1643 | 1 | 1 | 3-PIESCS（D≠0） |
| `TougaardBG`（fitting model） | 2886 | 1643 | 1 | 1 | 同上 |

> **C_d=1, D=1 是什么？** 经典 Tougaard 通用截面是 2-PIESCS（C_d=1, D=0），公式简化为 $B \cdot T/(C + T^2)^2$，其中 B=2866, C=1643。3-PIESCS 加了 D·T² 项（D≠0），对窄能量范围的谱（~30 eV）拟合更好。本 skill 实际跑的是 D=1 的 3-PIESCS。详见 Hesse & Denecke 在 UNIFIT 2011 中的推导。

### 什么时候需要换参数

通用默认值（C=1643, C_d=1, D=1）覆盖绝大多数 XPS 分析场景。以下情况才需要考虑材料专属参数：

- **定量分析精度要求很高**（原子% 误差 < 5%）
- **Tougaard 背景明显不合理**（低 BE 端不归零、形状很怪）
- **换了基线方法后结论反转**（说明基线本身是主要不确定性来源）

如果触发以上情况，按优先级：
1. 先换 Shirley 或 Linear 基线重做（大部分 Tougaard 问题换个方法就解决了）
2. 如果 Tougaard 是唯一合理的物理选择 → 查 Tougaard 1997 论文的材料专属参数

### Tougaard 1997 通用类（Universality Classes）

Tougaard 在 1997 年发现非弹性散射截面可以按材料类型分类——同一类材料用相同的 (C, D) 参数，只有 B 需要按谱拟合。这个概念论文确立了：

| 通用类 | 包含材料 | 论文 |
|---|---|---|
| 通用（Universal） | 所有金属及其氧化物，覆盖 ~90% 的场景 | Tougaard (1989), *Surf. Sci.* 216, 343 |
| 聚合物 | 有机聚合物——独立成类，散射截面形状不同 | Tougaard (1997), *Surf. Interface Anal.* 25, 137 |
| 半导体 | Si, Ge, GaAs 等——介于金属和氧化物之间 | 同上 |

**完整参数表**（各通用类的 C, C_d, D 精确值）：见 Tougaard (1997) *Surf. Interface Anal.* 25, 137–154，DOI: `10.1002/(SICI)1096-9918(199703)25:3<137::AID-SIA230>3.0.CO;2-L`。这篇是 paywalled——如果工作中需要精确参数，通过机构订阅获取。

> **实践中几乎不需要。** 本 skill 做叙事驱动的 XPS 分析，不是计量学级别的定量。通用默认值的误差在大多数论文的图里看不出来。如果审稿人质疑 Tougaard 参数选择，诚实地回答"使用了 lmfitxps 的通用默认值（3-PIESCS, C=1643, C_d=1, D=1, B 迭代优化）"就够了。

### 更新路径

- Tougaard 通用截面原始论文：Tougaard, *Surf. Sci.* 216 (1989) 343
- 通用类论文：Tougaard, *Surf. Interface Anal.* 25 (1997) 137
- 3-PIESCS / 4-PIESCS 方法：Hesse, R. & Denecke, R., UNIFIT 2011 poster, <https://unifit-software.de/poster.htm>
- lmfitxps 实现及默认值：<https://lmfitxps.readthedocs.io/en/latest/static_backgrounds.html>
- 2022 年更新（含 intrinsic excitation）：Gnacadja et al., *Surf. Interface Anal.* (2022), DOI: `10.1002/sia.6749`
