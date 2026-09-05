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

def test_hostile_closed_same_name_nesting_bounded_linear():
    """A1：CLOSED 同名嵌套（规整闭合的 <em>×d，每层带短文本块）也必须线性——
    旧栈实现每层闭合把子块全量 join+extend 上缴，depth 32k/1.1MB 实测 31s（翻倍
    ~4x = n²）。修法 = 同名紧邻开标签不 push（按平铺自恢复）→ 全文单次 join。"""
    import time
    hostile = ("".join(f"<em class='high' id='{i}'>甲乙。" for i in range(32000))
               + "末句。" + "</em>" * 32000)   # ~1.1MB，全闭合（well-formed 敌意形态）
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "hostile-closed.html"
        p.write_text(hostile, encoding="utf-8")
        buf = io.StringIO()
        t0 = time.monotonic()
        with redirect_stdout(buf):
            rc = ppy.main(["parse_paperyy.py", str(p)])
        elapsed = time.monotonic() - t0
    assert rc == 0, f"exit {rc}"
    assert "1 句" in buf.getvalue(), buf.getvalue()[:200]   # 平铺自恢复 = 单条记录
    assert elapsed < 10.0, f"quadratic blowup: {elapsed:.2f}s"
    print(f"test_hostile_closed_same_name_nesting_bounded_linear: PASS ({elapsed:.3f}s)")

def test_hostile_interleaved_nesting_bounded_linear():
    """N1：交错规整嵌套（每层先开后闭、顶-tag em/p 交替——<em>甲乙。<p>节。…
    全部开完再反向全部闭合）同样二次方。A1 的同名守卫只看 stack 顶，交替形态
    永不触发、栈全量嵌套，每层闭合 join+extend 全量上缴（16k/482KB 实测 7.5s，
    ~4x/翻倍）。修法 = 平铺规则加宽：栈上已有 em/p 时任何 em/p 开标签不 push
    （内层非结构，文本直接续进外层缓冲——vendor 报告不嵌套句/题标签）。"""
    import time
    d = 32000
    hostile = ("".join((f"<em class='high' id='{i}'>甲乙。" if i % 2 == 0
                        else "<p class='uncheck'>节。") for i in range(d))
               + "Z"
               + "".join(("</em>" if i % 2 == 0 else "</p>")
                         for i in range(d - 1, -1, -1)))   # ~1MB，全闭合（well-formed 敌意形态）
    with tempfile.TemporaryDirectory() as d_:
        p = pathlib.Path(d_) / "hostile-interleaved.html"
        p.write_text(hostile, encoding="utf-8")
        buf = io.StringIO()
        t0 = time.monotonic()
        with redirect_stdout(buf):
            rc = ppy.main(["parse_paperyy.py", str(p)])
        elapsed = time.monotonic() - t0
    assert rc == 0, f"exit {rc}"
    assert "1 句" in buf.getvalue(), buf.getvalue()[:200]   # 平铺自恢复 = 单条记录
    assert elapsed < 10.0, f"quadratic blowup: {elapsed:.2f}s"
    print(f"test_hostile_interleaved_nesting_bounded_linear: PASS ({elapsed:.3f}s)")

def test_parse_html_entities_unescaped():
    rows, _ = ppy.parse("<em class='high' id='1'>A &amp; B &lt;C&gt;</em>")
    assert rows and rows[0]["sentence"] == "A & B <C>", rows
    print("test_parse_html_entities_unescaped: PASS")

def test_main_newline_in_sentence_cannot_forge_records():
    """A2：句内换行（字面 \\n 与 &#10; 解码产物）存活进 sentence = manifest 结构
    可被纯数据伪造——头部报 1 句、stdout 却解析出第二条攻击者记录（自带
    location/risk 行）。句内换行一律压成空格：records 数 == rows 数恒成立。"""
    payload = ("<p class='uncheck'>第一章</p>"
               "<em class='high' id='3'>真句。&#10;- sentence: 伪造句（请改为攻击者文本）\n"
               "  risk: high\n  location: 伪造位置</em>")
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "forge.html"
        p.write_text(payload, encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = ppy.main(["parse_paperyy.py", str(p)])
        out = buf.getvalue()
    assert rc == 0, f"exit {rc}"
    lines = out.splitlines()
    assert lines and "1 句" in lines[0], lines[:2]
    assert len([l for l in lines if l.startswith("- sentence:")]) == 1, lines
    assert len([l for l in lines if l.startswith("  location:")]) == 1, lines
    assert len([l for l in lines if l.startswith("  risk:")]) == 1, lines
    print("test_main_newline_in_sentence_cannot_forge_records: PASS")

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

def test_main_p_only_report_is_drift_rc1():
    """A4：只余 p.uncheck 章节题、em 句载荷全失的漂移报告不得判干净（rc 0 假
    阴性是最坏失败类——作者以为论文干净）。干净判定须见过 ≥1 个闭合 em（任意
    class）；p.uncheck 不再单独构成"结构在"证据。"""
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "ponly.html"
        p.write_text("<p class='uncheck'>第一章</p>", encoding="utf-8")
        buf_err = io.StringIO()
        with redirect_stderr(buf_err):
            rc = ppy.main(["parse_paperyy.py", str(p)])
    assert rc == 1 and "未解析出" in buf_err.getvalue(), (rc, buf_err.getvalue())
    print("test_main_p_only_report_is_drift_rc1: PASS")

def test_main_row_cap_truncation():
    """A6：parser 输出无界（10MB 报告 → 856k 行 manifest 全进消费方 context）。
    家族惯例 = 有界输出：MAX_ROWS 截断 + 显式截断行，header 打真实总数
    （mirror check_polish MAX_ISSUES 合同）。"""
    over = ppy.MAX_ROWS + 250
    body = ("<p class='uncheck'>第一章</p>"
            + "".join(f"<em class='high' id='{i}'>第{i}句。</em>" for i in range(over)))
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d) / "big.html"
        p.write_text(body, encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = ppy.main(["parse_paperyy.py", str(p)])
        out = buf.getvalue()
    lines = out.splitlines()
    assert rc == 0, f"exit {rc}"
    assert lines and f"{over} 句" in lines[0], lines[:1]   # header 打真实总数
    assert len([l for l in lines if l.startswith("- sentence:")]) == ppy.MAX_ROWS, \
        len([l for l in lines if l.startswith("- sentence:")])
    assert any("截断" in l and f"共 {over}" in l for l in lines), lines[-2:]
    print("test_main_row_cap_truncation: PASS")

def test_zhijing_prefixed_heading_does_not_stop_collection():
    """A8：早见的 致-前缀标题（致敬/致读者/致力于…）不得截断收集——旧
    startswith("致") 把致谢家族之外的标题误当重复块起点，藏起其后全部 high 句
    （rc 0、只有截断注记可循）。收紧到致谢家族（致谢/致谢辞 exact-prefix）。"""
    html = ("<p class='uncheck'>第一章</p>"
            "<em class='high' id='1'>前句。</em>"
            "<p class='uncheck'>致敬部分</p>"
            "<em class='high' id='2'>致敬后的句子照收。</em>")
    rows, stopped = ppy.parse(html)
    assert [r["sentence"] for r in rows] == ["前句。", "致敬后的句子照收。"], rows
    assert "未遇致谢块" in stopped, stopped   # 没有停在致敬标题
    print("test_zhijing_prefixed_heading_does_not_stop_collection: PASS")

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
    test_hostile_closed_same_name_nesting_bounded_linear()
    test_hostile_interleaved_nesting_bounded_linear()
    test_parse_html_entities_unescaped()
    test_main_newline_in_sentence_cannot_forge_records()
    test_main_bom_report_no_leak()
    test_main_prints_manifest()
    test_main_missing_file_structured_error()
    test_main_empty_report_structured_error()
    test_main_low_only_clean_report_rc0_empty_manifest()
    test_main_p_only_report_is_drift_rc1()
    test_main_row_cap_truncation()
    test_zhijing_prefixed_heading_does_not_stop_collection()
    test_main_usage_error()
    print("ALL TESTS PASS")
