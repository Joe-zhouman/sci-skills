# Spine schema

The baton's schema. spine writes this; check_spine.py gates the 3 structural fields (coverage); umbrella + boundary are depth (human-gated, NOT checked by the script).

## Template (verbatim from spec §thesis-spine.md schema)

```markdown
# thesis-spine.md
> Baton. Settled by the author (depth human-gated). Read by dissect/intro/summary/theory.
> `pending` = AI candidate, NOT author-adopted. A field still marked `pending` is unsettled
> — dissect must not build on an unsettled field.

## Main line (主线)                       ← 串起 N 篇的 thread（结构字段，coverage-gated）
[pending? ] <one sentence: the thread connecting the N papers>

## Unified framework (统一框架)            ← 框架 + 每篇如何实例化它（结构字段，coverage-gated）
[pending? ] <the framework>
            per-paper: how paper-X instantiates it = …

## Inter-chapter progression (章间递进)      ← 研究章角色序列（默认 1:1）（结构字段，coverage-gated）
[pending? ] ordered:
            - role 1: question = …; advances the main line by …
            - role 2: question = …; advances the main line by …

## Thesis-level claim (umbrella)           ← 全篇一句话总贡献（depth-gated，非 coverage）
[pending? ] <one sentence: what the thesis establishes — the 3 structural fields collectively argue it>

## Boundary                                ← thesis-level claim 不 establish 什么（depth-gated，镜像 claim.md）
<where the thesis-level claim stops>

## Intake (per-paper evidence base)         ← spine 读小论文的依据（high-level only）
- paper-A: claim = …; structure = …; how it could fit a main line = …
- paper-B: …

## Cracks flagged (tension-flagging, §⑤)   ← attachment 盲点的 tension（提问非裁决）
- [stage 1 / main line] (a) tension: … (b) evidence: paper-C Fig3 §4.2 → ¬X (c) question: 是否 tension 主线的 X？
  disposition: [fatal → revised | dismissed → reason: …]   ← 作者处置，AI 不参与
- [stage 2 / framework] …

## Alternatives considered                  ← settled 时坍缩的候选（audit trail）
- main line: considered <alt>, rejected because <reason>
```

## 各节职责

| 节 | 归属 | 门 | 装什么 |
|---|---|---|---|
| **Main line** (主线) | product | coverage | 串起 N 篇的 thread（一句话） |
| **Unified framework** (统一框架) | product | coverage | 框架 + 每篇如何实例化（sub-coverage：Intake 每篇都要有实例化行） |
| **Inter-chapter progression** (章间递进) | product | coverage | 研究章角色序列（默认 1:1）；每个角色声明 question + advance（sub-coverage） |
| **Thesis-level claim** (umbrella) | product | **depth** | 全篇一句话总贡献；三结构字段 collectively argue 它（独立 depth-gate，不并入主线） |
| **Boundary** | product | **depth** | umbrella 不 establish 什么（镜像 sci-write claim.md 的 boundary） |
| **Intake** | evidence base | — | spine 读小论文的 high-level 依据（claim + 结构 + 如何串主线） |
| **Cracks flagged** | audit trail | — | tension-flagging：三要素问题 + 作者 disposition（提问非裁决，§⑤） |
| **Alternatives considered** | audit trail | — | settled 时坍缩的候选 + 拒绝理由 |

- **product = 顶部 5 节**（main line / unified framework / inter-chapter progression / thesis-level claim / boundary）= settled 后交下游的接力棒。
- **coverage 门（check_spine.py）只查 3 结构字段**：Main line / Unified framework / Inter-chapter progression 非空 + 各自 sub-coverage + 全文无 `[pending` 残留。**umbrella + boundary 不在 coverage**——它们是 depth，人工 only（spec §门；脚本源码 `STRUCTURAL_FIELDS` 排除 umbrella）。
- **Intake / Cracks / Alternatives = evidence base + audit trail**，与 product 同处一文件——镜像 sci-write claim.md 的 evidence baseline 与 argument 同处一文件（作者读着这个富 baton 做 depth 判断，不是读 chat 上下文）。
