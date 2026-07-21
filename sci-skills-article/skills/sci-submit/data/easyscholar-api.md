# EasyScholar API 参考

> 脚本在 `scripts/query-journal.py` 和 `scripts/query-journals.py`。以下只在脚本报错或需要了解 API 细节时读。

## 接口

```
GET https://www.easyscholar.cc/open/getPublicationRank?secretKey=<KEY>&publicationName=<URL_ENCODED_NAME>
```

## 认证

`secretKey` 参数，值在 `$EASY_SCHOLAR_API_KEY` 环境变量。若未配：https://www.easyscholar.cc → 登录 → 开放接口 → 获取 SecretKey。

## 速率限制

每秒 ≤2 次。

## 返回

成功 `code=200`，数据在 `data.officialRank.all`。字段只返回有结果的，无则缺省。

## 字段速查

| 字段 | 含义 |
|---|---|
| `sciUp` | 中科院升级版分区 |
| `sciBase` | 中科院基础版分区 |
| `sciUpSmall` | 升级版小类 |
| `sciUpTop` | Top 标记 |
| `sci` | JCR Q1-Q4 |
| `sciif` | SCI IF |
| `sciif5` | 五年 IF |
| `sciwarn` | 中科院预警 |
| `eii` | EI |
| `pku` | 北大核心 |
| `cssci` | CSSCI |
| `cscd` | CSCD |
| `jci` | JCI |
| `ssci` | SSCI |
| `esi` | ESI 学科 |
| `ccf` | CCF |
| `fms` / `utd24` / `ft50` / `ajg` | 商科分级 |
| `swufe` / `cufe` / `fdu` / `sjtu` / ... | 各高校自定义分级（37 个） |

## 错误码

| code | 说明 |
|---|---|
| 200 | 成功 |
| 40002 | Key 错误 |

## `customRank`

用户自定义数据集。`rankInfo` 列出数据集，`rank` 通过 `uuid&&&等级编号` 指向具体等级。一般不需要解析——`officialRank` 已覆盖主流分级。
