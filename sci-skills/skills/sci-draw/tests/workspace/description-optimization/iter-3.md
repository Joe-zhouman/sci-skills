# Iteration 3 — sci-draw

**Current description:**

> Scientific data visualization for creating publication-quality plots from experimental data. Use when the user asks to create, revise, or audit data-driven figures: statistical plots, bar/box/scatter charts, heatmaps, dose-response curves, survival curves, volcano plots, and multi-panel data layouts. Handles journal formatting, colorblind-safe palettes, and export requirements. Not for: AI-generated or text-to-image artwork (DALL-E, Stable Diffusion), conceptual diagrams or graphical abstracts without quantitative data, architecture/flowchart/network diagrams, interactive web visualizations or dashboards (Bokeh/Plotly HTML apps), or any figure not based on empirical data. Covers Chinese phrasings like 科研数据绘图、论文数据可视化、 统计作图、论文图表、数据可视化.

## Summary

- **Pass rate:** 19/20 queries (95%)
- **Should-trigger:** 9/10 correctly triggered
- **Should-NOT-trigger:** 10/10 correctly stayed silent

## Per-query results

| Pass | Query | Expected | Triggered |
|------|-------|----------|-----------|
| ✓ | 我要画一个基因表达热图，50个基因 x 12个样本，数据在expression_matrix.tsv里。投PNAS，需要colorblind-safe的c... | trigger | 3/3 |
| ✓ | 我论文Figure 1需要四个panel：(a) PCA图显示三组样本的分离，(b) 不同处理组随时间变化的肿瘤体积曲线，(c) 第28天各组的箱线图比较... | trigger | 3/3 |
| ✓ | 我正在写一篇药理学论文，需要画concentration-response曲线。x轴是对数刻度（药物浓度10^-9到10^-3 M），y轴是抑制率百分比。... | trigger | 3/3 |
| ✗ | 我有一组实验数据在 results.csv 里，三组不同处理的细胞存活率，每组8个样本。我投的是Nature，需要画一个publication-ready... | trigger | 1/3 |
| ✓ | 审稿人给了我一堆意见：error bar没标明是SD还是SEM，字体太小看不到，图例遮住了数据点，而且颜色在灰度打印下分不清。figs/figure3_v... | trigger | 2/3 |
| ✓ | I have 5 groups with n=6 each. My PI insists on mean bar charts but I've read... | trigger | 3/3 |
| ✓ | here's my data file at ~/experiment/fig2_data.xlsx — columns are group, time_... | trigger | 3/3 |
| ✓ | 我有一组单细胞RNA-seq数据，想画一个stacked bar chart展示不同cluster在control和treatment组中的细胞比例差异。... | trigger | 3/3 |
| ✓ | 帮我把这组生存分析数据画成Kaplan-Meier曲线。有三个治疗组，需要显示中位生存时间、censoring marks、log-rank检验的p值。f... | trigger | 3/3 |
| ✓ | 我在准备一篇综述论文，需要画一个方法比较的图：四种不同的算法在六个benchmark数据集上的表现。每个数据集一个subpanel，用grouped ba... | trigger | 3/3 |
| ✓ | 帮我用DALL-E生成一张细胞信号通路的机制图，要像Nature Reviews那种风格的，展示PI3K/AKT/mTOR通路的激活过程。 | silent | 0/3 |
| ✓ | I need to create a flowchart showing our clinical trial workflow — from patie... | silent | 0/3 |
| ✓ | 帮我做一个可交互的dashboard来展示我们实验室的实时传感器数据，用Plotly或者Dash，需要能筛选时间和设备类型，数据来自PostgreSQL数据库。 | silent | 1/3 |
| ✓ | 帮我用Stable Diffusion生成一张论文封面的科幻风格图片，主题是量子计算和拓扑量子比特，要有蓝紫色调和几何线条。 | silent | 0/3 |
| ✓ | 帮我把这张扫描的实验记录本图片里的文字OCR出来，里面有表格数据和手写批注。输出成结构化的CSV格式。 | silent | 0/3 |
| ✓ | Can you make an interactive web visualization of our single-cell RNA-seq data... | silent | 0/3 |
| ✓ | I want to design a conference poster for our lab — A0 size, three column layo... | silent | 0/3 |
| ✓ | 我想做一个Graphical Abstract，是一个概念性的示意图展示我们的纳米药物如何通过EPR效应靶向肿瘤细胞，然后在酸性微环境中释放药物。不需要数... | silent | 0/3 |
| ✓ | 能不能帮我画一个神经网络架构图？输入层是256维的embedding，经过三个LSTM隐藏层（128, 64, 32维），最后接一个softmax输出层。... | silent | 0/3 |
| ✓ | 帮我写一个Python脚本，读取多个CSV文件做数据清洗：处理缺失值、标准化数值列、one-hot编码分类变量、合并成一个大的特征矩阵。不需要画图，纯数据... | silent | 0/3 |

## Failing queries

- **did NOT trigger (should have)** — trigger rate 1/3
  > 我有一组实验数据在 results.csv 里，三组不同处理的细胞存活率，每组8个样本。我投的是Nature，需要画一个publication-ready的figure。帮我选个合适的图型，考虑到样本量不大，然后画出来。输出要PDF+PNG，300DPI，单栏宽度。

