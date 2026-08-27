"""stdlib tests for parse_paperpass.py — run: python3 test_parse_paperpass.py

PaperPass 目录制报告（htmls/js/）→ stdout 风险句清单（spec §③ 新接口）。
score ≥ MIN_SCORE(80) 才收；aiScore 头条进 meta；UNTRUSTED 纯解析；ANSI 消毒。
"""
import importlib.util, io, json, pathlib, tempfile
from contextlib import redirect_stdout, redirect_stderr
HERE = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("parse_paperpass", HERE / "parse_paperpass.py")
pps = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pps)


def _frag(i: int, score: float, txt: str) -> dict:
    return {"originalFragmentInfo": {"score": score, "sectionContentList": [txt]}}


def _write_report(frags, ai_score="23.5") -> pathlib.Path:
    d = pathlib.Path(tempfile.mkdtemp()) / "PaperPass-免费版-检测报告"
    js = d / "htmls" / "js"
    js.mkdir(parents=True)
    (js / "detaildata.js").write_text(f"var aiScore = {ai_score};\n", encoding="utf-8")
    (js / "reduceaigcpagelistdata0.js").write_text(
        "var reduceAiListInfo = " + json.dumps(frags, ensure_ascii=False) + ";\n", encoding="utf-8")
    return d


def test_parse_score_threshold_and_meta():
    d = _write_report([_frag(1, 95.0, "高分段落。"), _frag(2, 79.9, "低分段落。"), _frag(3, 80.0, "恰好八十。")])
    rows, err = pps.parse(d)
    assert err is None, err
    assert [r["sentence"] for r in rows] == ["高分段落。", "恰好八十。"], rows
    assert rows[0]["risk"] == "score=95.0" and rows[1]["risk"] == "score=80.0", rows
    assert all("PaperPass" in r["meta"] and "23.5" in r["meta"] for r in rows), rows
    print("test_parse_score_threshold_and_meta: PASS")

def test_parse_multiline_fragment_joined():
    d = _write_report([_frag(1, 90, "第一行\n第二行")])
    rows, err = pps.parse(d)
    assert err is None and rows[0]["sentence"] == "第一行第二行", rows
    print("test_parse_multiline_fragment_joined: PASS")

def test_parse_ansi_stripped():
    d = _write_report([_frag(1, 90, "句\x1b[31m子\x1b[0m")])
    rows, err = pps.parse(d)
    assert err is None and "\x1b" not in rows[0]["sentence"], rows
    print("test_parse_ansi_stripped: PASS")

def test_main_prints_manifest():
    d = _write_report([_frag(1, 95.0, "高分段落。")])
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = pps.main(["parse_paperpass.py", str(d)])
    out = buf.getvalue()
    assert rc == 0 and "# 风险句清单" in out and "- sentence: 高分段落。" in out, out
    assert "  risk: score=95.0" in out, out
    print("test_main_prints_manifest: PASS")

def test_main_missing_dir_structured_error():
    buf_err = io.StringIO()
    with redirect_stderr(buf_err):
        rc = pps.main(["parse_paperpass.py", "/nonexistent/dir"])
    assert rc == 1 and "目录" in buf_err.getvalue(), rc
    print("test_main_missing_dir_structured_error: PASS")

def test_main_missing_js_structured_error():
    d = pathlib.Path(tempfile.mkdtemp()) / "fake"
    d.mkdir(parents=True)
    buf_err = io.StringIO()
    with redirect_stderr(buf_err):
        rc = pps.main(["parse_paperpass.py", str(d)])
    assert rc == 1 and "reduceaigcpagelistdata0.js" in buf_err.getvalue(), rc
    print("test_main_missing_js_structured_error: PASS")

def test_main_malformed_json_structured_error():
    d = pathlib.Path(tempfile.mkdtemp()) / "PaperPass-x"
    js = d / "htmls" / "js"
    js.mkdir(parents=True)
    (js / "reduceaigcpagelistdata0.js").write_text("var reduceAiListInfo = [{broken json}];", encoding="utf-8")
    buf_err = io.StringIO()
    with redirect_stderr(buf_err):
        rc = pps.main(["parse_paperpass.py", str(d)])
    assert rc == 1 and ("解析失败" in buf_err.getvalue() or "JSON" in buf_err.getvalue()), rc
    print("test_main_malformed_json_structured_error: PASS")

def test_main_clean_report_rc0_empty_manifest():
    """零 ≥80 片段 = 干净结果非故障（F6）——空 manifest + rc 0。"""
    d = _write_report([_frag(1, 10, "全低分")])
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = pps.main(["parse_paperpass.py", str(d)])
    out = buf.getvalue()
    assert rc == 0 and "0 段" in out and "解析正常" in out, (rc, out)
    print("test_main_clean_report_rc0_empty_manifest: PASS")

def test_main_usage_error():
    assert pps.main(["parse_paperpass.py"]) == 2
    print("test_main_usage_error: PASS")

if __name__ == "__main__":
    test_parse_score_threshold_and_meta()
    test_parse_multiline_fragment_joined()
    test_parse_ansi_stripped()
    test_main_prints_manifest()
    test_main_missing_dir_structured_error()
    test_main_missing_js_structured_error()
    test_main_malformed_json_structured_error()
    test_main_clean_report_rc0_empty_manifest()
    test_main_usage_error()
    print("ALL TESTS PASS")
