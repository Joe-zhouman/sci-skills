# 数据加载细则

正文 §1.1 给了"先 head 看一眼、统一成两列、自己写解析"的流程。这里展开各格式的具体处理。XPS 本质永远是两列：Binding Energy（高→低，~1100→0 eV）和 Counts。

## 常见格式

- **两列 TXT/CSV**（最常见）：仪器直接导出。分隔符可能是制表符、逗号、空格；可能有表头。`numpy.loadtxt` 或 `pandas.read_csv`。
- **多列 TXT/CSV**：可能含多组数据（不同元素区域、不同样品）。**让用户指认要哪两列，不要自己猜。**
- **Excel `.xlsx`**：`pandas.read_excel`，同样先看 sheet 结构再读。
- **VAMAS `.vms` / `.npl`**：ISO 14976 标准，`pynxtools-xps` 可读。装不上就让用户在仪器软件或 CasaXPS 里导出为两列 TXT。

## 常见坑

- **trailing comma**（MATLAB 导出常见）：每行末尾多个分隔符，`numpy.loadtxt` 的 `invalid_raise=False` 会**静默丢数据**、最后剩 0 列。先 `head` 看到，再 `pandas.read_csv`（自动处理）或读完删掉全空列。
- **编码问题**：非 UTF-8（GBK 等）用 `encoding` 参数指定。
- **小数点问题**：部分欧洲仪器用逗号做小数点（`47183,55`），用 `decimal=','` 或全局替换。

## 输出契约

无论如何，输出统一为（后续所有脚本吃它）：
```json
{"energies": [...], "counts": [...], "metadata": {"source": "..."}}
```
数据长什么样是数据的事，统一成这个格式是你的责任。
