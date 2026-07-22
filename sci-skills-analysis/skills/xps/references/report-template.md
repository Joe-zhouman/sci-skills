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
- 校准方法：[C 1s @ 284.8 eV / 内标 Au 4f / 手动偏移 X eV]
- 基线方法：[Shirley / Tougaard / 多项式]（全数据集统一）
- 峰函数：[Gaussian / Pseudo-Voigt / Voigt]
- 分析软件：sci-skills-analysis:xps (Python, lmfit)

## 2. 各区域结果

### Si 2p

| 化学态 | BE (eV) | FWHM (eV) | 相对面积 (%) | NIST 参考 |
|---|---|---|---|---|
| Si₃N₄ | 101.8 | 2.75 | 58 | 101.9 eV (Ingo & Zacchetti 1990) |
| SiNₓ | 101.1 | 2.55 | 32 | — |
| Si⁰ | 99.6 | 1.11 | 7 | 99.3 eV (NIST) |
| SiOₓ | 103.2 | 1.43 | 3 | 103.4 eV (NIST) |

R² = 0.9987

**解读：** Si₃N₄ 为主要组分（58%），SiNₓ 次之（32%），微量 Si⁰ 和 SiOₓ。与 claim "Si₃N₄ 为主要相"一致。

## 3. 与其他表征手段的印证

| 手段 | 发现 | 与 XPS 是否一致 | 说明 |
|---|---|---|---|
| XRD | Si₃N₄ 特征峰 (2θ=33.7°) | ✅ 一致 | 独立证实 Si₃N₄ 的存在 |
| EDS | N/Si 原子比 ≈ 1.2 | ✅ 一致 | 接近 Si₃N₄ 的理论比 1.33 |
| TEM | ![TEM 图](evidence/tem_coating.png) | ✅ 一致 | 表面包覆层 ~5 nm，XPS 检测深度匹配 |

## 4. 局限性与注意事项

- C 1s 校准 @ 284.8 eV 可能漂移（Gengenbach 2022）
- 缺少定量 RSF 校正——相对面积是半定量的

## 5. 结论

[一句话回归 claim]
```

## 关于定量（RSF）

Scofield 和 Wagner 的相对灵敏度因子（RSF）**不互通**。一个数据集内做原子%定量必须用同一套 RSF。本 skill 输出的"相对面积 %"是峰面积比，**没做 RSF 校正**——是半定量的，写论文要在局限性里声明（模板第 4 节已含这条）。要做严格原子%定量，需要拿 RSF（仪器厂家会给，或查 Scofield/Wagner 表）乘到各组分面积上再归一化。
