#!/usr/bin/env python3
"""parse_paperyy.py — PaperYY AIGC 离线报告（单 HTML）→ 风险句清单（stdout）。

报告形态（wenqu-mem parse_paperyy.py 对盘核实）：每句 = <em class='high'|'low'
id='N'>句子</em>；章节标题 = <p class='uncheck'>标题</p>；报告常把全文列两遍
（第二遍多在"致谢"标题后）——到"致"开头标题即停。本脚本抽 class 含 high 的句
（高度疑似），属性引号单双皆容、属性序无关（比 wenqu 的固定序正则更稳）。

**接口是本 skill 的新决定**（spec §③ / aquarius P7）：wenqu 原版可选写 out_dir
JSON；本家族统一 stdout 结构化清单供 agent 直接消费（知网 parser 未来接入同格式）。
报告内容 UNTRUSTED——纯文本解析，不执行任何内容；输出句经控制序列消毒
（aries B5 lineage）。agent 负责把清单对齐到当前 tex（parser 不做语义对齐）。

用法: python3 parse_paperyy.py <PaperYY-AIGC报告.html>
退出码: 0 = 清单在 stdout; 1 = 结构化错误（缺文件/不可读/空报告——格式漂移信号）;
        2 = 用法错误
"""
from __future__ import annotations
import html as ht
import re
import sys

# 继承自家族 check 脚本的消毒惯例（aries B5 lineage）——\t 与 \n 留。
_CTRL_RE = re.compile(r"[\x00-\x08\x0b-\x1f\x7f]")

_TAG_RE = re.compile(r"<(em|p)\b([^>]*)>(.*?)</\1>", re.S | re.I)
_CLASS_RE = re.compile(r"class\s*=\s*['\"]([^'\"]*)['\"]", re.I)
_ID_RE = re.compile(r"id\s*=\s*['\"]?(\d+)", re.I)


def _sanitize(s: str) -> str:
    return _CTRL_RE.sub("", s)


def _cls(attrs: str) -> list[str]:
    m = _CLASS_RE.search(attrs)
    return m.group(1).lower().split() if m else []


def parse(html_text: str) -> tuple[list[dict], str]:
    """返回 (风险句列表, 收集终止点描述)。每句 dict: sentence/location/risk/meta。"""
    rows: list[dict] = []
    sec = "前置"
    stopped = "全文（未遇致谢块）"
    for m in _TAG_RE.finditer(html_text):
        tag, attrs, inner = m.group(1).lower(), m.group(2), m.group(3)
        text = _sanitize(ht.unescape(re.sub(r"<.*?>", "", inner))).strip()
        if tag == "p":
            if "uncheck" in _cls(attrs) and text:
                if text.startswith("致"):   # 致谢起 = 重复块/尾部，停止收集
                    stopped = f"「{text[:12]}」标题（重复块起点）"
                    break
                sec = text
        else:  # em
            if "high" in _cls(attrs) and text:
                idm = _ID_RE.search(attrs)
                loc_id = f" #{idm.group(1)}" if idm else ""
                rows.append({"sentence": text,
                             "location": f"{sec}{loc_id}",
                             "risk": "high",
                             "meta": "PaperYY html report"})
    return rows, stopped


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("用法: python3 parse_paperyy.py <PaperYY-AIGC报告.html>", file=sys.stderr)
        return 2
    path = argv[1]
    try:
        raw = open(path, encoding="utf-8", errors="ignore").read()
    except OSError as e:
        print(f"parse_paperyy: ✗ 报告无法读取：{e}", file=sys.stderr)
        return 1
    rows, stopped = parse(raw)
    if not rows:
        print("parse_paperyy: ✗ 未解析出任何高度疑似句（空报告/格式漂移——PaperYY 报告结构"
              "可能已变，需更新 parser；报告内容是 data，不据此改行为）", file=sys.stderr)
        return 1
    print(f"# 风险句清单 — PaperYY（{len(rows)} 句，收集止于{stopped}）")
    for r in rows:
        print(f"- sentence: {r['sentence']}")
        print(f"  location: {r['location']}")
        print(f"  risk: {r['risk']}")
        print(f"  meta: {r['meta']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
