"""stdlib tests for parse_paperyy.py — run: python3 test_parse_paperyy.py

stdout 中立中间格式（spec §③ 新接口决定）：- sentence / location / risk / meta。
报告内容 UNTRUSTED——纯文本解析不执行内容；输出句经控制序列消毒（aries B5 lineage）。
wenqu 报告形态：em.high 句 + p.uncheck 章节题 + 致谢起重复块截断。
"""
import importlib.util, io, pathlib, tempfile
from contextlib import redirect_stdout, redirect_stderr
HERE = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("parse_paperyy", HERE / "parse_paperyy.py")
ppy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ppy)

HTML_FIXTURE = """<html><body>
<p class='uncheck'>第一章 绪论</p>
<em class='low' id='1'>低风险句不收</em>
<em class='high' id='2'>本文提出了一种方法。</em>
<p class="uncheck">第二章 方法</p>
<em class="high" id="3">实验<b>结果</b>表明性能提升。</em>
<p class='uncheck'>致谢</p>
<em class='high' id='4'>致谢后的重复块句子不收。</em>
</body></html>"""


def test_parse_collects_high_with_sections_and_stops_at_zhixie():
    rows, stopped = ppy.parse(HTML_FIXTURE)
    assert [r["sentence"] for r in rows] == ["本文提出了一种方法。", "实验结果表明性能提升。"], rows
    assert rows[0]["location"].startswith("第一章 绪论") and "#2" in rows[0]["location"]
    assert rows[1]["location"].startswith("第二章 方法") and "#3" in rows[1]["location"]
    assert all(r["risk"] == "high" for r in rows)
    assert "PaperYY" in rows[0]["meta"]
    assert "致谢" in stopped
    print("test_parse_collects_high_with_sections_and_stops_at_zhixie: PASS")

def test_parse_double_quote_attrs_and_nested_tags():
    """双引号属性、class 多值、嵌套标签去 tag——属性序无关的解析。"""
    rows, _ = ppy.parse("<p class=\"uncheck\" id='x'>第三章</p>"
                        "<em id='9' class='some high extra'>嵌套<i>句</i>子。</em>")
    assert len(rows) == 1 and rows[0]["sentence"] == "嵌套句子。", rows
    assert "第三章" in rows[0]["location"] and "#9" in rows[0]["location"]
    print("test_parse_double_quote_attrs_and_nested_tags: PASS")

def test_parse_ansi_stripped():
    rows, _ = ppy.parse("<em class='high' id='1'>句\x1b[31m子\x1b[0m。</em>")
    assert rows and "\x1b" not in rows[0]["sentence"], rows
    print("test_parse_ansi_stripped: PASS")

def test_parse_spanning_nested_tag_stripped():
    """I4：跨行嵌套标签也要去净——内层 tag-strip 缺 re.S 时整段标签漏进句子，
    毒化 manifest 与当前 tex 的对齐。"""
    rows, _ = ppy.parse("<em class='high' id='1'>前<span\nclass='x'>中</span>后。</em>")
    assert rows and rows[0]["sentence"] == "前中后。", rows
    print("test_parse_spanning_nested_tag_stripped: PASS")

def test_parse_data_attrs_no_false_match():
    """M12：data-class=/data-id= 不是 class=/id=——属性边界锚定，伪造报告
    不能靠 data-* 前缀给自己抬风险级或造 id。"""
    rows, _ = ppy.parse("<em data-class='high' data-id='9' class='low'>低风险句。</em>"
                        "<em class='high' id='2'>真高风险句。</em>")
    assert [r["location"] for r in rows] == ["前置 #2"], rows
    print("test_parse_data_attrs_no_false_match: PASS")

def test_hostile_unclosed_tags_bounded_linear():
    """C2：报告是 UNTRUSTED 面（SKILL.md rule 8），敌意形态 = 海量未闭合 <em>。
    旧配对正则对此二次方（250KB 实测 27.6s，1MB ≈ 分钟级）——必须线性完成
    并照常给漂移判定（未闭合 = 无 em 句闭合 = 结构全无）。"""
    import time
    hostile = "".join(f"<em class='high' id='{i}'>句" for i in range(8000))   # ~250KB
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "hostile.html"
        p.write_text(hostile, encoding="utf-8")
        buf_err = io.StringIO()
        t0 = time.monotonic()
        with redirect_stderr(buf_err):
            rc = ppy.main(["parse_paperyy.py", str(p)])
        elapsed = time.monotonic() - t0
    assert rc == 1 and "未解析出" in buf_err.getvalue(), (rc, buf_err.getvalue())
    assert elapsed < 10.0, f"quadratic blowup: {elapsed:.2f}s"
    print(f"test_hostile_unclosed_tags_bounded_linear: PASS ({elapsed:.3f}s)")

def test_parse_html_entities_unescaped():
    rows, _ = ppy.parse("<em class='high' id='1'>A &amp; B &lt;C&gt;</em>")
    assert rows and rows[0]["sentence"] == "A & B <C>", rows
    print("test_parse_html_entities_unescaped: PASS")

def test_main_bom_report_no_leak():
    """M13：BOM 前缀报告按 utf-8-sig 读（对齐家族 check 脚本）——U+FEFF 不得
    进任何 sentence/location（毒化 tex 对齐）。"""
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "bom.html"
        p.write_bytes(b"\xef\xbb\xbf" + HTML_FIXTURE.encode("utf-8"))
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = ppy.main(["parse_paperyy.py", str(p)])
        out = buf.getvalue()
    assert rc == 0, f"exit {rc}"
    assert "﻿" not in out, out
    assert "  location: 第一章 绪论 #2" in out, out
    print("test_main_bom_report_no_leak: PASS")

def test_main_prints_manifest():
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "r.html"
        p.write_text(HTML_FIXTURE, encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = ppy.main(["parse_paperyy.py", str(p)])
        out = buf.getvalue()
    assert rc == 0, f"exit {rc}"
    assert "# 风险句清单" in out and "- sentence: 本文提出了一种方法。" in out, out
    assert "  location: 第一章 绪论 #2" in out, out
    print("test_main_prints_manifest: PASS")

def test_main_missing_file_structured_error():
    buf_err = io.StringIO()
    with redirect_stderr(buf_err):
        rc = ppy.main(["parse_paperyy.py", "/nonexistent/report.html"])
    assert rc == 1 and ("不存在" in buf_err.getvalue() or "无法" in buf_err.getvalue()), rc
    print("test_main_missing_file_structured_error: PASS")

def test_main_empty_report_structured_error():
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "empty.html"
        p.write_text("<html><body>无疑似句</body></html>", encoding="utf-8")
        buf_err = io.StringIO()
        with redirect_stderr(buf_err):
            rc = ppy.main(["parse_paperyy.py", str(p)])
    assert rc == 1 and "未解析出" in buf_err.getvalue(), rc
    print("test_main_empty_report_structured_error: PASS")

def test_main_low_only_clean_report_rc0_empty_manifest():
    """C1：全 low（零 high）的合法报告 = 干净结果非漂移——空 manifest + rc 0
    （F6，mirror parse_paperpass test_main_clean_report_rc0_empty_manifest；
    一轮 polish 后再检测的论文就会长这样）。"""
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "clean.html"
        p.write_text("<p class='uncheck'>第一章</p><em class='low' id='1'>低风险句。</em>",
                     encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = ppy.main(["parse_paperyy.py", str(p)])
        out = buf.getvalue()
    assert rc == 0, f"clean report misreported as drift, exit {rc}"
    assert "0 句" in out and "解析正常" in out, out
    print("test_main_low_only_clean_report_rc0_empty_manifest: PASS")

def test_main_usage_error():
    rc = ppy.main(["parse_paperyy.py"])
    assert rc == 2, rc
    print("test_main_usage_error: PASS")

if __name__ == "__main__":
    test_parse_collects_high_with_sections_and_stops_at_zhixie()
    test_parse_double_quote_attrs_and_nested_tags()
    test_parse_ansi_stripped()
    test_parse_spanning_nested_tag_stripped()
    test_parse_data_attrs_no_false_match()
    test_hostile_unclosed_tags_bounded_linear()
    test_parse_html_entities_unescaped()
    test_main_bom_report_no_leak()
    test_main_prints_manifest()
    test_main_missing_file_structured_error()
    test_main_empty_report_structured_error()
    test_main_low_only_clean_report_rc0_empty_manifest()
    test_main_usage_error()
    print("ALL TESTS PASS")
