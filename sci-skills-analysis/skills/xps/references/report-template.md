# report.md Template

收尾时（§3.2）生成的最终叙事报告模板。state.json schema 见 `workdir-state.md`——这份只管报告格式。

```markdown
# XPS Analysis Report — [一句话概括 claim]

**Claim:** [用户在 Step 0 确定的 claim]
**Date:** [分析日期]
**Regions analyzed:** Si 2p, N 1s, Li 1s, …
**Other evidence:** XRD, TEM, EDS, …

---

## 1. 数据与方法

- 仪器 / 数据来源：[如果用户提供了]
- Pass energy：[eV，仪器展宽下限取决于此，影响 FWHM 可比性]
- 平滑方法：[Savitzky-Golay 窗口 X / 未做平滑]
- 校准方法：[C 1s @ 284.8 eV / 内标 Au 4f / 手动偏移 X eV]
- 基线方法：[Shirley / Tougaard / 多项式]（全数据集统一） + 各区域端点
- 峰函数：[Pseudo-Voigt / Voigt]
- RSF 来源：[Scofield 理论值 (C 1s=1.000) / 用户提供仪器 RSF]，是否做 IMFP 修正
- 分析软件：sci-skills-analysis:xps (Python, lmfitxps)

## 2. 各区域结果

### Si 2p

**Sub-claim:** Si₃N₄ 为主组分，Si⁰ 微量存在
**校准偏移：** +0.6 eV（C 1s 实测 284.2 → 参考 284.8）
**基线：** Shirley，端点 107–96 eV

| 化学态 | BE (eV) | FWHM (eV) | 相对面积 (%) | 原子% (RSF校正) | NIST 参考 |
|---|---|---|---|---|---|
| Si₃N₄ | 101.8 ± 0.02 | 2.75 | 58 | 58.5 | 101.9 eV (Ingo & Zacchetti 1990) |
| SiNₓ | 101.1 ± 0.05 | 2.55 | 32 | 31.2 | — |
| Si⁰ | 99.6 ± 0.01 | 1.11 | 7 | 7.1 | 99.3 eV (NIST) |
| SiOₓ | 103.2 ± 0.04 | 1.43 | 3 | 3.2 | 103.4 eV (NIST) |

R² = 0.9987
RSF: Scofield t-RSF, 未做 IMFP 修正
NIST 查询: `lookup_be.py Si --line 2p --range 97 107 --format json`

**解读：** Si₃N₄ 为主要组分（58.5 atom%），SiNₓ 次之（31.2 atom%），微量 Si⁰ 和 SiOₓ。与 claim "Si₃N₄ 为主要相"一致。

## 3. 与其他表征手段的印证

| 手段 | 发现 | 与 XPS 是否一致 | 说明 |
|---|---|---|---|
| XRD | Si₃N₄ 特征峰 (2θ=33.7°) | ✅ 一致 | 独立证实 Si₃N₄ 的存在 |
| EDS | N/Si 原子比 ≈ 1.2 | ✅ 一致 | 接近 Si₃N₄ 的理论比 1.33 |
| TEM | ![TEM 图](evidence/tem_coating.png) | ✅ 一致 | 表面包覆层 ~5 nm，XPS 检测深度匹配 |

## 4. 局限性与注意事项

- C 1s 外来碳校准 @ 284.8 eV 漂移可达 ±0.5 eV（Gengenbach 2022, *Appl. Surf. Sci.* 606, 154855）。本报告如用此方法，峰位绝对值的可靠性受此限制
- 基线灵敏度：[换用 Linear / 多项式基线后面积比例变化 X%，结论在基线选择下稳定 / 不稳定]
- RSF：[Scofield / 用户提供仪器 RSF]，未做 IMFP 修正，原子%为近似值
- RSF 灵敏度：[仪器 RSF 和 Scofield 计算结果差异 X%，结论在 RSF 选择下稳定 / 不稳定]
- R² 与拟合质量：[如 R² < 0.95，说明原因：噪声大 / 化学态连续分散 / 过渡金属卫星峰复杂]
- 过渡金属/稀土的定量精度受卫星峰和多重组态影响，本报告如有此类元素需额外声明

## 5. 结论

[一句话回归 claim]
```

## 关于定量（RSF）

RSF 数据表、公式、Scofield vs Wagner 选择指南见 `references/rsf-quantification.md`。各平台 RSF 获取见 `references/rsf-sources.md`。脚本：`quantify.py`。

核心规则：
- 同一报告内所有元素用同一套 RSF（Scofield 和 Wagner **不互通**）
- 方法部分声明 RSF 来源 + IMFP 修正状态
- 局限性部分声明 RSF 灵敏度（两套 RSF 计算结果差异 + 结论是否稳定）
