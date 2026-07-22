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

某些轨道是双峰，只用一个峰拟合是错的：
- Si 2p → 2p₃/₂ + 2p₁/₂，间距 ~0.6 eV，面积比 2:1
- 类似：金属的 p/d/f 轨道多数分裂；C 1s、N 1s、O 1s 不分裂

遇到分裂轨道，peaks.json 里要**成对放**、约束面积比（amplitude_range 反映 2:1）、约束间距。

## 失败排查

拟合器可能不收敛或给出不合理结果：

- **R² < 0.8**：峰数不对、函数不对、或初始值太离谱
- **参数顶到边界**：约束太紧——放宽 `*_range`
- **某个峰宽度趋近于 0**：这个峰可能不存在，减少峰数
- **残差有系统性结构**（不是随机噪声）：缺了峰、或峰形不对

排查顺序：减少峰数 → 换峰函数 → 放宽约束 → 调整基线端点 → 检查数据质量。**不要接受一个差的拟合然后说"就这样吧"。**

## 不确定度

lmfit 自动输出每个参数的 ±stderr。report.md 里必须带上——只报峰位不报 ±stderr = 给人"精确无误"的错觉。
