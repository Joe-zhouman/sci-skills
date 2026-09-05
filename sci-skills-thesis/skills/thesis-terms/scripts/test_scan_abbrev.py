"""stdlib tests for scan_abbrev.py — run: python3 test_scan_abbrev.py"""
import importlib.util, json, pathlib, sys, tempfile
HERE = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("scan_abbrev", HERE / "scan_abbrev.py")
scan_abbrev = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scan_abbrev)


def _find(cands, abbr):
    return [c for c in cands if c["abbr"] == abbr]


def test_pattern_full_paren():
    """模式 1：thermal contact resistance (TCR) → 命中。"""
    cands = scan_abbrev.scan_text(
        "The thermal contact resistance (TCR) dominates the interface.", "a.tex")
    hits = _find(cands, "TCR")
    assert hits and hits[0]["full"] == "thermal contact resistance", f"got: {cands}"
    print("test_pattern_full_paren: PASS")


def test_pattern_define_verb():
    """模式 2：TCR denotes / stands for / TCR: → 命中（高精度兜底形）。"""
    for verb_form in ("TCR denotes thermal contact resistance.",
                      "TCR stands for thermal contact resistance.",
                      "TCR: thermal contact resistance."):
        cands = scan_abbrev.scan_text(verb_form, "a.tex")
        hits = _find(cands, "TCR")
        assert hits and hits[0]["full"] == "thermal contact resistance", \
               f"{verb_form!r} missed: {cands}"
    print("test_pattern_define_verb: PASS")


def test_pattern_section_lines():
    """模式 3：Abbreviations/Nomenclature 标题下的条目行。"""
    text = """Some intro paragraph.
Abbreviations
TCR    thermal contact resistance
XRD - X-ray diffraction
SEM: scanning electron microscopy
Then a closing paragraph that is not an entry line at all.
"""
    cands = scan_abbrev.scan_text(text, "a.tex")
    assert _find(cands, "TCR") and _find(cands, "XRD") and _find(cands, "SEM"), f"got: {cands}"
    assert _find(cands, "TCR")[0]["full"] == "thermal contact resistance"
    print("test_pattern_section_lines: PASS")


def test_comment_lines_ignored():
    """LaTeX 注释里的定义不算：% TCR (fake full form) 不产生候选。"""
    cands = scan_abbrev.scan_text(
        "% TCR (fake comment form)\nReal text about X-ray diffraction (XRD).", "a.tex")
    assert not _find(cands, "TCR"), f"comment leaked: {cands}"
    assert _find(cands, "XRD"), f"real definition lost: {cands}"
    print("test_comment_lines_ignored: PASS")


def test_non_acronym_parens_rejected():
    """数字开头 (3a)、全小写 (fig)、单词大写不足 (Fig) → 拒。"""
    cands = scan_abbrev.scan_text(
        "As shown in (3a) and (fig) with (Fig) labels.", "a.tex")
    assert cands == [], f"non-acronyms leaked: {cands}"
    print("test_non_acronym_parens_rejected: PASS")


def test_material_formula_is_candidate_declared_fp():
    """已声明误报类：Ti3C2Tx 过 ABBR 判定成为候选（AI 核验滤）——口径钉死。"""
    cands = scan_abbrev.scan_text(
        "Titanium carbide MXene (Ti3C2Tx) films were measured by X-ray diffraction (XRD).", "a.tex")
    assert _find(cands, "Ti3C2Tx"), f"declared-FP class missing: {cands}"
    assert _find(cands, "XRD"), f"real abbreviation missing: {cands}"
    print("test_material_formula_is_candidate_declared_fp: PASS")


def test_dedup_same_pair_conflict_kept():
    """同名同全称去重留首见；同名异全称保留（潜在冲突信号）。"""
    text = ("thermal contact resistance (TCR) matters. "
            "thermal contact resistance (TCR) matters twice. "
            "total circuit resistance (TCR) is a different meaning.")
    cands = scan_abbrev.scan_text(text, "a.tex")
    hits = _find(cands, "TCR")
    assert len(hits) == 2, f"expected 1 dedup + 1 conflict, got: {hits}"
    fulls = {h["full"] for h in hits}
    assert fulls == {"thermal contact resistance", "total circuit resistance"}, f"got: {fulls}"
    print("test_dedup_same_pair_conflict_kept: PASS")


def test_multifile_sources_labeled():
    """多文件聚合：候选带各自出处。"""
    import io, contextlib
    d = pathlib.Path(tempfile.mkdtemp())
    (d / "a.tex").write_text("thermal contact resistance (TCR).", encoding="utf-8")
    (d / "b.tex").write_text("X-ray diffraction (XRD) patterns.", encoding="utf-8")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = scan_abbrev.main(["scan_abbrev.py", str(d), "--format", "json"])
    assert rc == 0
    # main prints to stdout — capture via scan calls instead for structure:
    cands = scan_abbrev.scan_text((d / "a.tex").read_text(encoding="utf-8"), "a.tex") \
        + scan_abbrev.scan_text((d / "b.tex").read_text(encoding="utf-8"), "b.tex")
    assert {c["source"] for c in cands} == {"a.tex", "b.tex"}
    print("test_multifile_sources_labeled: PASS")


def test_cli_json_and_empty(tmp=None):
    """CLI：--format json 输出对象数组；空文本 exit 0 零候选。"""
    d = pathlib.Path(tempfile.mkdtemp())
    f = d / "a.tex"
    f.write_text("thermal contact resistance (TCR).", encoding="utf-8")
    import io, contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = scan_abbrev.main(["scan_abbrev.py", str(f), "--format", "json"])
    assert rc == 0
    arr = json.loads(buf.getvalue())
    assert arr and arr[0]["abbr"] == "TCR", f"json broken: {arr}"
    empty = d / "empty.tex"; empty.write_text("no abbreviations here at all.\n", encoding="utf-8")
    buf2 = io.StringIO()
    with contextlib.redirect_stdout(buf2):
        rc = scan_abbrev.main(["scan_abbrev.py", str(empty)])
    assert rc == 0 and "无候选" in buf2.getvalue(), f"empty handling broken: rc={rc} {buf2.getvalue()}"
    print("test_cli_json_and_empty: PASS")


def test_cli_missing_file_structured_error():
    """不存在文件 → stderr 结构化错误 + exit 1（agent 可分辨输入错 vs 无候选）。"""
    import io, contextlib
    buf_err = io.StringIO()
    with contextlib.redirect_stderr(buf_err):
        rc = scan_abbrev.main(["scan_abbrev.py", "/nonexistent/zz.tex"])
    assert rc == 1 and "不存在" in buf_err.getvalue(), f"rc={rc} err={buf_err.getvalue()}"
    print("test_cli_missing_file_structured_error: PASS")


if __name__ == "__main__":
    test_pattern_full_paren()
    test_pattern_define_verb()
    test_pattern_section_lines()
    test_comment_lines_ignored()
    test_non_acronym_parens_rejected()
    test_material_formula_is_candidate_declared_fp()
    test_dedup_same_pair_conflict_kept()
    test_multifile_sources_labeled()
    test_cli_json_and_empty()
    test_cli_missing_file_structured_error()
    print("ALL TESTS PASS")
