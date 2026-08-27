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

def test_parse_html_entities_unescaped():
    rows, _ = ppy.parse("<em class='high' id='1'>A &amp; B &lt;C&gt;</em>")
    assert rows and rows[0]["sentence"] == "A & B <C>", rows
    print("test_parse_html_entities_unescaped: PASS")

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

def test_main_usage_error():
    rc = ppy.main(["parse_paperyy.py"])
    assert rc == 2, rc
    print("test_main_usage_error: PASS")

if __name__ == "__main__":
    test_parse_collects_high_with_sections_and_stops_at_zhixie()
    test_parse_double_quote_attrs_and_nested_tags()
    test_parse_ansi_stripped()
    test_parse_html_entities_unescaped()
    test_main_prints_manifest()
    test_main_missing_file_structured_error()
    test_main_empty_report_structured_error()
    test_main_usage_error()
    print("ALL TESTS PASS")
