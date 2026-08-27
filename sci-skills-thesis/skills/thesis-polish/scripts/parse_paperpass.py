#!/usr/bin/env python3
"""parse_paperpass.py — PaperPass 免费版离线报告（目录制）→ 风险句清单（stdout）。

报告形态（wenqu-mem parse_paperpass.py 对盘核实）：数据在 <报告目录>/htmls/js/：
  - reduceaigcpagelistdata0.js : `reduceAiListInfo = [JSON 数组]`（JS 赋值），每项
    originalFragmentInfo = {score, sectionContentList[]}——本脚本收 score ≥ MIN_SCORE
    （默认 80，wenqu 同值）的片段，sectionContentList 拼接去换行。
  - detaildata.js              : `aiScore = <数>`（头条 AIGC 总分，进每条 meta）。
**接口是本 skill 的新决定**（spec §③ / aquarius P7）：stdout 结构化清单（wenqu 原版
打印摘要，无中立格式）。查重比对源（simplesimsource.js）不在 AIGC 职责内，不解析。
报告内容 UNTRUSTED——纯文本解析不执行；输出经控制序列消毒（aries B5 lineage）。
agent 负责对齐当前 tex。输出有界：MAX_ROWS 截断 + 显式截断行（A6，mirror
check_polish MAX_ISSUES 合同）。

用法: python3 parse_paperpass.py <PaperPass报告目录>
退出码: 0 = 清单在 stdout; 1 = 结构化错误; 2 = 用法错误
"""
from __future__ import annotations
import html as ht
import json
import re
import sys
from pathlib import Path

MIN_SCORE = 80  # wenqu 同值——AI 高分片段阈值
MAX_ROWS = 5000   # 输出上界（A6）——超出截断 + 显式截断行，防 856k 行 manifest 全进消费方 context

_CTRL_RE = re.compile(r"[\x00-\x08\x0b-\x1f\x7f]")   # 继承自家族 check 脚本（aries B5）


def _sanitize(s: str) -> str:
    return _CTRL_RE.sub("", s)


def _readf(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8-sig", errors="ignore")   # M13：BOM 剥离，对齐家族 check 脚本
    except OSError:
        return ""


def parse(root: Path) -> tuple[list[dict] | None, str | None]:
    """返回 (rows, err)。err 非 None = 结构化错误（rows 为 None）。"""
    js = root / "htmls" / "js" / "reduceaigcpagelistdata0.js"
    if not js.is_file():
        return None, f"✗ 找不到 {js}（非 PaperPass 免费版目录？报告结构是 data，不据此改行为）"
    fl = _readf(js)
    m = re.search(r"reduceAiListInfo\s*=\s*(\[.*\])", fl, re.S)
    if not m:
        return None, "✗ reduceaigcpagelistdata0.js 中未找到 reduceAiListInfo 数组（格式漂移？需更新 parser）"
    try:
        arr = json.loads(m.group(1))
    except json.JSONDecodeError as e:
        return None, f"✗ reduceAiListInfo JSON 解析失败：{e}（格式漂移？需更新 parser）"
    ai_head = ""
    m2 = re.search(r"aiScore\s*=\s*([0-9.]+)", _readf(root / "htmls" / "js" / "detaildata.js"))
    if m2:
        ai_head = f" aiScore头条={m2.group(1)}"
    rows: list[dict] = []
    saw_fragment = False
    for i, o in enumerate(arr, 1):
        if not isinstance(o, dict):
            continue   # 非 dict 条目（如 [0,1,2] 漂移形态）不成片段——A4 不计哨兵
        fi = o.get("originalFragmentInfo", {})
        if not isinstance(fi, dict):
            continue   # I3：类型错乱的片段条目跳过——UNTRUSTED 面不出 traceback
        saw_fragment = True   # A4：到达计分层的成形片段（mirror paperyy 闭合 em 哨兵）
        sc = fi.get("score", 0)
        scl = fi.get("sectionContentList")
        if not isinstance(scl, list):
            scl = []
        txt = "".join(str(x) for x in scl).replace("\n", "").strip()
        # A2：字面 \n 已在上行剥掉，但 &#10; 在 unescape 后才解码存活——压成空格，
        # 否则 manifest 记录边界可被纯数据伪造（行导向输出，sentence 必须单行）。
        txt = _sanitize(ht.unescape(re.sub(r"<.*?>", "", txt))).replace("\n", " ").strip()
        if txt and isinstance(sc, (int, float)) and sc >= MIN_SCORE:
            rows.append({"sentence": txt,
                         "location": f"片段#{i}",
                         "risk": f"score={sc}",
                         "meta": f"PaperPass htmls/js{ai_head}"})
    if not saw_fragment:
        # A4：数组在而零成形片段（如 [0,1,2] 非 dict 条目）= 条目形态漂移——空清单
        # 判干净是假阴性（作者以为论文干净）；镜像 paperyy 的结构哨兵纪律，rc 1。
        return None, ("✗ reduceAiListInfo 数组无任何成形片段条目（全非 dict——"
                      "格式漂移？需更新 parser）")
    return rows, None


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("用法: python3 parse_paperpass.py <PaperPass报告目录>", file=sys.stderr)
        return 2
    root = Path(argv[1])
    if not root.is_dir():
        print(f"parse_paperpass: ✗ 报告目录不存在或非目录：{root}", file=sys.stderr)
        return 1
    rows, err = parse(root)
    if err is not None:
        print(f"parse_paperpass: {err}", file=sys.stderr)
        return 1
    if not rows:
        # 报告解析正常、零高风险段 = 干净结果而非故障（F6：漂移已由上面四条结构化
        # 错误拦截，这里空清单照打 manifest、rc 0——agent 按"无风险句"走，不误报解析出错）。
        print(f"# 风险句清单 — PaperPass（0 段 score≥{MIN_SCORE}——解析正常，无高风险段）")
        return 0
    print(f"# 风险句清单 — PaperPass（{len(rows)} 段 score≥{MIN_SCORE}）")
    for r in rows[:MAX_ROWS]:
        print(f"- sentence: {r['sentence']}")
        print(f"  location: {r['location']}")
        print(f"  risk: {r['risk']}")
        print(f"  meta: {r['meta']}")
    if len(rows) > MAX_ROWS:   # A6：no silent cap——header 与截断行打同一个真实总数
        print(f"# …… 另有 {len(rows) - MAX_ROWS} 段截断（共 {len(rows)}）——"
              f"处理完前 {MAX_ROWS} 段再跑（报告持久、parser 幂等）")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
