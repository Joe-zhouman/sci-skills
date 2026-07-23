# 主流 XPS 平台导出两列 TXT 指南

当用户说"我不知道怎么从这个软件里导出数据"时，按平台查本节。所有平台最终都能导出两列 Binding Energy + Counts 的 TXT 或 CSV——不需要特殊格式。

> **官网列在每节末尾**，用于查最新操作。软件 UI 会变，以官网最新文档为准。

---

## Thermo Fisher Avantage

Avantage 是 Thermo Fisher 的 XPS 仪器标配软件（K-Alpha、ESCALAB QXi、Nexsa G2 等）。

### 导出步骤

1. **语言设为英文**（重要）：`Utilities → Preferences → Language → English`，重启软件。中文界面下导出的 Excel 可能格式异常（只有两列、乱码等）。
2. **导出到 Excel**：
   - 在右侧谱图列表中选中要导出的谱图（高亮）
   - `Reporting → Report Options`，在 `Tables` 选项卡勾选 `Peak Table`
   - 点击 `Report to Excel` 生成 Excel 文件
   - 或直接选中谱图 **Ctrl+C 复制，粘贴到空白 Excel** 中（Office 版本过高致 Report 按钮灰色时的 fallback）
3. **整理成两列 TXT**：
   - 打开导出的 Excel，找到目标元素的工作表
   - 只保留 Binding Energy 和 Counts 两列，删除其余行/列
   - 复制到空白 `.txt` 文件，确保数据从第一行开始、无空行、无描述文字

### 常见坑

- **中文界面导出只有两列数据**：切英文界面解决
- **CSV 在 Excel 中打开乱码**：Avantage 导出的 CSV 是 UTF-8 无 BOM，用 Excel 的"数据 → 从文本/CSV"导入，手动指定编码 `65001: Unicode (UTF-8)`，不要直接双击打开

### 官网

- Avantage 产品页：<https://www.thermofisher.com/> → 搜索 "Avantage data system"
- 用户手册和更新需通过 Thermo Fisher 客户门户获取（随仪器授权）

---

## Kratos ESCApe（Shimadzu / Kratos Analytical）

ESCApe 是 Kratos AXIS 系列（Nova、Supra+）的采集+处理+报告一体化软件。数据原生格式为 `.experiment`。

### 导出步骤

1. 在 ESCApe 中打开 `.experiment` 文件
2. 进入 **Data Processing** 模块
3. 在右上角下拉中选择 **ESCA Spectrum**，将谱图从左侧 Data Organiser 拖入处理窗口
4. 在第二个下拉中选择导出方式：
   - **Excel exporter**（ESCApe 1.4+，推荐）→ 导出为 `.xlsx`
   - **VAMAS exporter** → 导出为 `.vms`（可用 `pynxtools-xps` 或 CasaXPS 转成 TXT）
5. 双击 Data Organiser 中的谱图设置输出格式：`Fitted Model`（含拟合数据）/ `Regions`（含量）
6. 选择保存路径，输入文件名，点 **Run**

### 备选：Kratos Excel Add-In

安装 ESCApe 安装目录下的 `KratosExcelAddIn.vsto`，在 Excel 的"数据"选项卡出现 `Experiment` 按钮 → 打开 `.experiment` 文件 → `Import` 把数据点全部复制到 Excel → Excel 另存为 CSV/TXT。

### 常见坑

- ESCApe 没有直接的 TXT 导出——走 Excel 或 VAMAS 再中转
- 导出给 XPSPeak / Origin 用的 TXT：从 Excel 只复制 BE + Counts 两列，粘贴到 `.txt`，确保无表头无空行，数据第一行开始

### 官网

- Shimadzu Kratos 产品线：<https://www.shimadzu.com/an/products/surface-analysis/>
- AC Scientific（Kratos 分销商，含 ESCApe 详细介绍）：<https://www.ac-scientific.com/en/kratos-analytical/escape-data-system/>

---

## PHI MultiPak（ULVAC-PHI / Physical Electronics）

MultiPak 是 PHI 仪器（Quantera、VersaProbe 等）的分析软件，原生格式 `.spe`。

### 导出步骤

1. 在 MultiPak 中打开谱图（`.spe` 文件）
2. **`File → Export To → ASCII`**
3. 保存为 `.csv` 文件

导出的 CSV 直接是两列：Binding Energy（eV）和 Intensity（Counts），无需额外整理。

### 常见坑

- 导出前如有分析标注，先 `File → Save Current File As` 存为新 `.spe`，导出的 CSV 不会保留标注
- 也可以在 MultiPak 中选中数据直接 Ctrl+C 复制，粘贴到 Origin / Excel

### 官网

- ULVAC-PHI MultiPak 产品页：<https://www.ulvac-phi.com/en/products/database-books/phi-multipak/>
- Physical Electronics 官网：<https://www.phi.com/>
- MultiPak 更新需要注册 Club PHI 会员后下载

---

## SPECS SpecsLab Prodigy

SpecsLab Prodigy 是 SPECS 仪器（FlexProbe、ProvenX-PS、ENVIRO 等）的实验控制和数据处理软件。原生格式为 `.sle`（二进制）。

### 导出步骤

SpecsLab Prodigy 支持导出为 **`.xy` ASCII 文件**（制表符分隔文本），导出时提供八个选项：

| 选项 | 建议 |
|---|---|
| Counts Per Second | Yes（用 CPS 而非原始计数） |
| Kinetic Energy Axis | No（用 Binding Energy） |
| Separate Scan Data | No（合并扫描） |
| Separate Channel Data | No |
| External Channel Data | 按需 |
| Transmission Function | No |
| Asymmetry Recalculation | No |
| Error Bar | No |

导出后得到 `.xy` 文件，头几行是采集参数（以 `#` 开头），后面是两列数据（BE + Counts）。用 `pandas.read_csv` 读时加 `comment='#'` 跳过头部即可，或用文本编辑器手动删掉头部只留两列。

也支持导出 **VAMAS `.vms`** 格式，可中转 CasaXPS 再导出 TXT。

### 常见坑

- `.xy` 文件带参数头，不是零行开始的纯两列——用 `comment='#'` 跳过
- SPECSlab Prodigy 可免费安装在个人电脑上离线处理数据，不必在仪器电脑上导出

### 官网

- SPECS SpecsLab Prodigy：<https://www.specs-group.com/specs/products/detail/prodigy>
- SPECSGROUP 官网：<https://www.specs-group.com/>

---

## Scienta Omicron — PEAK（当前）/ SES（旧版）

Scienta Omicron 的当前软件叫 **PEAK**（通过客户门户分发），旧版 SES 仍在使用中。

### SES（旧版）导出步骤

1. 在 SES 软件中打开谱图
2. 导出为 **plain text**（`.txt`）格式——SES 的标准文本导出
3. 注意：SES `.txt` 是角分辨数据格式，不是简单两列——需要用工具提取：
   - **`pynxtools-xps`**（Python）：`ScientaTXTParser` 读 `.txt` 并转为标准两列
   - **pranabdas/xps**（网页工具）：上传 SES `.txt`，沿角度维度积分，输出 BE vs Intensity 两列

### PEAK（当前）导出步骤

PEAK 软件通过 Scienta Omicron 客户门户分发，导出功能的具体操作随版本更新。以客户门户中的最新用户手册为准。

### 备选：导出为 Igor Binary Wave（`.ibw`）

SES/PEAK 都可以导出 `.ibw`（Igor Pro 波形格式），`pynxtools-xps` 可以读取。

### 官网

- Scienta Omicron 官网：<https://scientaomicron.com/>
- PEAK 软件下载需登录客户门户（Customer Portal）
- `pynxtools-xps` Scienta 支持：<https://fairmat-nfdi.github.io/pynxtools-xps/reference/scienta.html>

---

## CasaXPS（通用处理软件，跨平台中转站）

CasaXPS 是 XPS 领域最通用的数据处理软件，**能读几乎所有仪器的原生格式**，也是最好的格式转换工具。

### 导出两列 TXT 步骤

1. 在 CasaXPS 中打开数据（`.vms` 或仪器原生文件）
2. 激活目标谱图所在的显示窗格（单击选中）
3. 点击工具栏 **Clipboard Export** 按钮（剪贴板图标）
4. 弹出剪贴板选择对话框，含 BE、KE、CPS、组分、背景、包络等列
5. 选需要的列（至少 BE + Spectral CPS），**Save as TAB-spaced ASCII file**（制表符分隔文本）

### 导入外部 TXT 转 VAMAS

如果手头只有 TXT 数据想用 CasaXPS 处理：
- `File → Convert` → 选择 `.txt` 文件
- 确保 TXT 是干净两列（BE + Counts），无空行无表头
- 自动转换为 `.vms` 标准格式

### 常见坑

- "Failed to write VAMAS file" → TXT 文件有空行或未正确保存（0 KB），修复后重试
- 同一批样品的所有谱图放一个文件夹下，Convert 时一起选

### 官网

- CasaXPS 官网：<http://www.casaxps.com/>
- 下载（试用版）：<http://www.casaxps.com/berlin/>
- 大量教程视频在 YouTube 搜 "CasaXPS"
- 联系购买：neal@casaxps.com

---

## 速查表

| 平台 | 原生格式 | 最快导出路径 | 到两列 TXT 的工作量 |
|---|---|---|---|
| Thermo Avantage | `.vgd` | Ctrl+C 复制谱图 → 粘贴到 Excel → 只留两列 → 存 TXT | 2 分钟 |
| Kratos ESCApe | `.experiment` | Excel exporter → 只留两列 → 存 TXT | 2 分钟 |
| PHI MultiPak | `.spe` | `File → Export To → ASCII` → 直接得 CSV | 10 秒 |
| SPECS SpecsLab | `.sle` | 导出 `.xy` → `comment='#'` 读或用文本编辑器删头部 | 1 分钟 |
| Scienta Omicron | `.txt` / `.ibw` | 导出 `.txt` → `pynxtools-xps` 提取两列 | 5 分钟（需脚本） |
| CasaXPS | `.vms` | Clipboard Export → Save as TAB-spaced ASCII | 30 秒 |

**实在搞不定**：让用户在仪器软件或 CasaXPS 里把数据导出为两列 TXT/CSV 发给你。所有平台都能做到，这是最低公共出口。
