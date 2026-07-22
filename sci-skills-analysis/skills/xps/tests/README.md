# Tests

## 为什么没有数值回归测试

XPS 峰拟合是**强领域性**的——拟合结果完全由具体数据 + 具体参数决定，而"同输入 → 同输出"是 lmfit 确定性优化器（`leastsq`）的基本性质，不需要测试来证明。锁住一个 `R² = 0.9987` 或某个峰位数值：

- **不能证明分析正确**——R² 高不代表峰指认对、约束合理、claim 成立。
- **不能 catch 真正会坏的东西**——脚本接口、数据流契约、CLI 参数。lmfit 的数值输出本身不会"漂移"。
- **是表演性的**——给一个数字镀金，暗示"测过了"，但没测任何有意义的不变量。

所以这个 skill 刻意**不写数值回归测试**。

## 什么测试才有意义（以后可加）

如果以后要加测试，测**接口和数据流的不变量**，不测数值：

- **CLI 契约**：每个脚本缺输入文件 → 返回结构化错误信封（`type`/`subtype`/`param`/`hint`），不抛 traceback；`--format json` 输出可被 `json.loads` 解析。
- **数据流**：load → calibrate → background → find_peaks → fit → export，上一棒的输出 JSON 能被下一棒的 `-d` 吃掉，全程不报错。
- **magic-number 防护**：`fit_peaks --peak-function` 覆盖有效；`peaks.json` 不含 `peak_function` 字段（方法/数据分离）。
- **状态机**：`state.json` 的 region status 流转 `explored → fitting → done`。

`tests/data/` 是历史真实数据（MATLAB 实验、原始谱），不是测试 fixture——别动。
