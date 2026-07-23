# 各平台 RSF 获取指南

RSF（相对灵敏度因子）决定从峰面积算原子%时每个元素的权重。不同仪器/软件内置的 RSF 表不同（厂家用理论值+经验校准的混合），**同一套数据用不同 RSF 表算出的原子%能差 10-20%**。

> **加载时机**：Step 0 问完 claim 之后立刻问 RSF。用户不知道 RSF 是什么——正常。把这页的内容翻译成人话告诉他们。

---

## 用户常见情况

### "我不知道什么是 RSF"——外包做实验

研究人员在高校测试中心、第三方平台（e测试、科学指南针、赛默飞应用实验室等）做 XPS，拿到的通常只是数据文件（TXT/CSV/VGD/VMS）——**不含 RSF**。

**问用户三个问题就能锁定 RSF 来源**：

1. "你用哪台仪器测的？"（仪器型号，如 Thermo K-Alpha、Kratos AXIS Supra+、PHI VersaProbe）
2. "测样的人有没有给你导出一个叫'定量结果'或'元素含量'的表格？"（如果有，里面可能含 RSF）
3. "能不能问测试老师要一下灵敏度因子表？就说'我要自己在 Origin 里算原子百分比，需要仪器配套的 RSF 值'——他们听得懂。"

**用户拿到了 RSF 表**（任何格式——CSV/Excel/截图/手抄的数字都行）→ `state.py set-rsf --source user --file <path>`。数字少你手动录成 CSV（三列：Element,Line,RSF），多了让用户发文件。

**用户拿不到** → `state.py set-rsf --source scofield`。Scofield 是普适的理论值。

### "我有原始数据文件，能直接从里面提取 RSF 吗"

**能部分做到。** Avantage 的 `.vgd` 文件内嵌 RSF 表，软件打开后在定量模块能看到。ESCApe 的 `.experiment` 文件同理。但如果你手头没有仪器软件（只有导出的 TXT），从二进制文件里提取 RSF 不现实——直接问测试老师更快。

---

## 各平台速查

### Thermo Fisher Avantage

Avantage 使用 **Scofield 理论 RSF + 仪器传输函数修正**（混合型）。

**用户怎么拿到**：在 Avantage 里打开原始 `.vgd` 文件 → 点 `Quantification` 按钮 → 定量结果窗口里有各元素的 RSF 值 → 截图或导出 Excel。

或者：右键 Periodic Table 图标 → `Edit Sensitivity Factors` → 能看到完整的 RSF 表。

如果用户无法操作 Avantage：告诉用户用 `state.py set-rsf --source scofield`。Avantage 默认用的就是 Scofield 值（加仪器修正），对我们做叙事级定量来说 Scofield 足够接近。

### Kratos ESCApe（Shimadzu / Kratos AXIS）

ESCApe 使用 **Wagner 经验 RSF + Kratos 自定义值**（混合型）。

**用户怎么拿到**：ESCApe → `Data Processing` 模块 → 选择 `ESCA Spectrum` + `Excel exporter` → 导出时勾选 `Regions` → Excel 里含 RSF 列。

或者：ESCApe → `Tools → Sensitivity Factor Library` → 能看到各元素的 RSF。

如果用户无法操作 ESCApe：ESCApe 的 Wagner RSF 和 Scofield 差异不大（~10%），直接用 `state.py set-rsf --source scofield`，在 report 局限性和定量结果旁边注明"RSF 来自 Scofield 理论值，未使用仪器专属 Wagner RSF"。

### PHI MultiPak（ULVAC-PHI）

MultiPak 内置 RSF 库（理论 + 经验混合）。

**用户怎么拿到**：MultiPak 菜单栏右侧有 **Periodic Table 按钮** → 点击 → 按住 Shift + 鼠标左键点击元素 → 弹出窗口显示该元素各轨道的 RSF → 截图。

或者：`File → Export To → ASCII` 导出定量结果时勾选 "Include Sensitivity Factors"。

如果用户无法操作 MultiPak：`state.py set-rsf --source scofield`。PHI 的 RSF 和 Scofield 对主峰（s/p 轨道）非常接近。

### SPECS SpecsLab Prodigy

SpecsLab 使用内置 RSF 库（Scofield + 经验修正）。

**用户怎么拿到**：打开 `.sle` 文件 → `Quantification` 模块 → 定量结果表中有 RSF → 导出。

如果用户无法操作 SpecsLab：`state.py set-rsf --source scofield`。

### Scienta Omicron SES / PEAK

SES 使用内置 RSF（Scofield 值）。

如果用户无法操作：`state.py set-rsf --source scofield`。SES 的定量本来就基于 Scofield。

### CasaXPS

CasaXPS 有多种 RSF 库可选——用户**必须选对**，否则定量结果是错的。

**用户怎么拿到**：CasaXPS → `Options → Elements` → `Sensitivity Factor Library` → 能导出当前库的 RSF 表。

**如果用户用 CasaXPS 处理数据**：问他们用了哪个 RSF 库（"在 Options → Elements 里看到的库名叫什么？"）。通常的库名是 `Scofield`、`Wagner`、或仪器特定库（如 `Kratos Axis Supra`）。

### 特殊平台：科学指南针 / e测试 / 高校测试中心

这些不是仪器软件——是外包服务方。他们会给用户一个 PDF/Excel 报告，里面通常有"元素含量"表。

**告诉用户**："你的测试报告里有没有一列叫'Atomic %'或'原子百分比'？那个表旁边有时候会标注 RSF 来源。如果只有百分比没有 RSF，问测试老师——他们测的时候软件自己用了 RSF，让他们把用的 RSF 值一起给你。"

大多数高校测试老师对"我要自己算原子百分比，需要你们仪器配套的灵敏度因子"这个请求不意外——这是标准需求。如果对方不给，你用 Scofield 算，结果差 10-15%，在论文里如实声明即可。

---

## 拿到了 RSF 之后的处理

### 是一个数字列表（或截图里的数字）

手工录入为 CSV：

```csv
Element,Line,RSF
C,1s,1.000
N,1s,0.477
O,1s,0.780
Si,2p,0.283
```

然后 `state.py set-rsf --source user --file thermo_rsf.csv`。

**关键注意**：RSF 的归一化基准可能不同。Scofield = C 1s = 1.000；Wagner = F 1s = 1.000；Kratos = 可能是别的。同一套拟合数据必须用同一种基准的 RSF——混用基准会造成系统性偏差。用户给的 RSF 表不用做归一化换算，直接用——`quantify.py` 的内部归一化（area/RSF 加和 = 100%）会消掉基准差异。

### 是一个 Excel 导出

用 `pandas.read_excel` 读，提取 Element / Line / RSF 三列，存为 CSV。

### 拿到了但缺某些元素

用户 RSF 里缺的元素 → 用户 RSF 有的用它，缺的用 Scofield 表补。`quantify.py` 当前不支持混合 RSF，需要分两次跑、手动合并，或你把用户 RSF 表 + Scofield 缺的条目合并成一个 CSV 再传入。

---

## 更新路径

各仪器厂家的 RSF 表偶尔更新（新软件版本、新仪器型号）。以厂家最新软件中的表为准。当前（2026）主流版本：

- Avantage: v6.x（Thermo Fisher 客户门户获取）
- ESCApe: v1.4+（Shimadzu Kratos 客户门户获取）
- MultiPak: v9.9+（ULVAC-PHI Club PHI 会员下载）
- CasaXPS: v2.3.25+（<http://www.casaxps.com/berlin/> 获取）
- SpecsLab Prodigy: v100+（<https://www.specs-group.com/> 获取）
