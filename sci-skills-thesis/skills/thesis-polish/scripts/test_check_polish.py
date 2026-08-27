"""stdlib tests for check_polish.py — run: python3 test_check_polish.py

check_polish.py is a MECHANICAL CONSISTENCY gate: ledger variant residue +
dangling crossref (single direction — unused labels are P5 noise, never reported).
It does NOT check prose quality (depth — human review + eval), does NOT re-run
write-time chain gates (glossary: write-time check, not a post-polish invariant),
does NOT check AIGC score (only re-detection knows). Bounded output (MAX_ISSUES
+ explicit truncation line). Ledger missing → issue + degraded mode (crossref
still checked — polish tolerates half-finished projects, spec §④).
"""
import atexit, codecs, importlib.util, pathlib, shutil, tempfile
HERE = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("check_polish", HERE / "check_polish.py")
check_polish = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_polish)

_ROOTS: list[pathlib.Path] = []
def _new_root() -> pathlib.Path:
    d = pathlib.Path(tempfile.mkdtemp())
    _ROOTS.append(d)
    return d
atexit.register(lambda: [shutil.rmtree(d, ignore_errors=True) for d in _ROOTS])

LEDGER_SETTLED = """# thesis-terminology-ledger.md
> spine seeds; chapters/polish co-write.

| Category | Term / variants | Canonical form | Source | Notes |
|---|---|---|---|---|
| 缩写 | 卷积神经网络 / 卷积网络 / convnet | CNN | thesis-spine | 全文统一 |
| 记号 | Tmax / T_max | $T_{\\max}$ | thesis-theory | 记号统一 |
| 单位 | um | µm | thesis-polish | siunitx: \\si{\\micro\\meter} |
"""

TEX_CLEAN = r"""\chapter{绪论}\label{ch:intro}
\label{fig:overview}\label{eq:model}
本文采用 CNN 方法。
温度记号统一为 $T(x)$，尺度为 $\mu$m 级。
见图~\ref{fig:overview} 与式~\eqref{eq:model}。
"""


def _write_project(ledger: str = LEDGER_SETTLED, texs: dict[str, str] = {"ch0.tex": TEX_CLEAN}):
    """Build temp project: sci-skills/ledger + thesis/tex/*.tex. Returns (ledger, tex_dir)."""
    root = _new_root()
    lg = root / "sci-skills" / "thesis-terminology-ledger.md"
    lg.parent.mkdir(parents=True)
    lg.write_text(ledger, encoding="utf-8")
    td = root / "thesis" / "tex"
    td.mkdir(parents=True)
    for name, body in texs.items():
        (td / name).write_text(body, encoding="utf-8")
    return lg, td


def test_passes_on_clean():
    lg, td = _write_project()
    issues = check_polish.check(td, lg)
    assert issues == [], f"expected pass, got: {issues}"
    print("test_passes_on_clean: PASS")

def test_unused_label_is_not_reported():
    """P5 pin: TEX_CLEAN contains \\label{ch:intro} never \\ref'd — clean pass
    doubles as the unused-label pin (single direction only)."""
    lg, td = _write_project()
    issues = check_polish.check(td, lg)
    assert not any("ch:intro" in i for i in issues), f"unused label must NOT report: {issues}"
    print("test_unused_label_is_not_reported: PASS")

def test_fails_on_cjk_variant_residue():
    bad = TEX_CLEAN + "实验表明卷积神经网络在该任务上表现良好。\n"
    lg, td = _write_project(texs={"ch0.tex": bad})
    issues = check_polish.check(td, lg)
    assert any("ch0.tex:6" in i and "卷积神经网络" in i and "CNN" in i for i in issues), \
        f"expected residue issue with file:line + canonical, got: {issues}"
    print("test_fails_on_cjk_variant_residue: PASS")

def test_ascii_variant_word_boundary():
    """variant 'um' must match standalone 'um' but NOT inside 'columnum'/'nums'."""
    bad_line = TEX_CLEAN + "尺度记作 um 级。\n"
    lg, td = _write_project(texs={"ch0.tex": bad_line})
    issues = check_polish.check(td, lg)
    assert any("`um`" in i for i in issues), f"standalone um must flag: {issues}"
    trap = TEX_CLEAN + "\\newcommand{\\nums}{1} 分组见 \\columnum{2}\n"
    lg, td = _write_project(texs={"ch0.tex": trap})
    issues = check_polish.check(td, lg)
    assert not any("`um`" in i for i in issues), f"um inside a word must NOT flag: {issues}"
    print("test_ascii_variant_word_boundary: PASS")

def test_fails_on_dangling_ref():
    bad = TEX_CLEAN + "见 \\ref{fig:none}。\n"
    lg, td = _write_project(texs={"ch0.tex": bad})
    issues = check_polish.check(td, lg)
    assert any("fig:none" in i and "悬空" in i for i in issues), f"expected dangling ref: {issues}"
    print("test_fails_on_dangling_ref: PASS")

def test_eqref_cref_recognized_and_multikey():
    bad = TEX_CLEAN + "\\eqref{eq:none} 与 \\cref{fig:overview,tab:none}。\n"
    lg, td = _write_project(texs={"ch0.tex": bad})
    issues = check_polish.check(td, lg)
    assert any("eq:none" in i for i in issues), f"eqref must be a ref: {issues}"
    assert any("tab:none" in i for i in issues), f"cref multi-key must check each: {issues}"
    assert not any("fig:overview" in i and "悬空" in i for i in issues), \
        f"existing key inside multi-key cref must NOT flag: {issues}"
    print("test_eqref_cref_recognized_and_multikey: PASS")

def test_variant_in_comment_not_flagged():
    commented = TEX_CLEAN + "% 卷积神经网络注释行\n正文 % 卷积网络 行内注释\n"
    lg, td = _write_project(texs={"ch0.tex": commented})
    issues = check_polish.check(td, lg)
    assert not any("卷积" in i for i in issues), f"comment variants must NOT flag: {issues}"
    print("test_variant_in_comment_not_flagged: PASS")

def test_ref_in_comment_not_flagged():
    commented = TEX_CLEAN + "% \\ref{fig:none} 注释里不查\n"
    lg, td = _write_project(texs={"ch0.tex": commented})
    issues = check_polish.check(td, lg)
    assert not any("fig:none" in i for i in issues), f"comment refs must NOT flag: {issues}"
    print("test_ref_in_comment_not_flagged: PASS")

def test_escaped_percent_keeps_text():
    """50\\% 是字面百分号——其后文本仍受检查（F3：转义不误杀后半行）。"""
    escaped = TEX_CLEAN + "提升达 50\\% 的卷积网络增益。\n"
    lg, td = _write_project(texs={"ch0.tex": escaped})
    issues = check_polish.check(td, lg)
    assert any("卷积网络" in i for i in issues), f"text after \\% must stay checked: {issues}"
    print("test_escaped_percent_keeps_text: PASS")

def test_double_backslash_then_percent_is_comment():
    """\\\\% = 换行命令后接注释——其后文本是注释，不受检查（F3：偶数反斜杠判对）。"""
    nl = TEX_CLEAN + "分组\\\\% 卷积网络注释\n"
    lg, td = _write_project(texs={"ch0.tex": nl})
    issues = check_polish.check(td, lg)
    assert not any("卷积网络" in i for i in issues), f"after \\\\% is comment — must NOT flag: {issues}"
    print("test_double_backslash_then_percent_is_comment: PASS")

def test_ledger_missing_degrades_to_crossref():
    """ledger missing → ONE issue + crossref still checked (spec §④ degraded mode)."""
    bad = TEX_CLEAN + "见 \\ref{fig:none}。\n"
    lg, td = _write_project(texs={"ch0.tex": bad})
    lg.unlink()
    issues = check_polish.check(td, lg)
    assert any("thesis-terminology-ledger" in i and "降级" in i for i in issues), \
        f"expected degraded-mode issue: {issues}"
    assert any("fig:none" in i for i in issues), f"crossref must still run: {issues}"
    print("test_ledger_missing_degrades_to_crossref: PASS")

def test_ledger_without_table():
    lg, td = _write_project(ledger="# ledger\n> 只有散文说明，无表格。\n")
    issues = check_polish.check(td, lg)
    assert any("无可解析术语表格" in i for i in issues), f"expected no-table issue: {issues}"
    print("test_ledger_without_table: PASS")

def test_ledger_table_in_fence_ignored():
    fenced = "# ledger\n\n```\n| Category | Term / variants | Canonical form |\n|---|---|---|\n| 缩写 | 卷积神经网络 | CNN |\n```\n"
    lg, td = _write_project(ledger=fenced)
    issues = check_polish.check(td, lg)
    assert any("无可解析术语表格" in i for i in issues), f"fenced table must not count: {issues}"
    print("test_ledger_table_in_fence_ignored: PASS")

def test_orphan_fence_diagnostic():
    orphan = LEDGER_SETTLED + "\n```\n"
    lg, td = _write_project(ledger=orphan)
    issues = check_polish.check(td, lg)
    assert any("未闭合 code fence" in i for i in issues), f"expected orphan-fence diagnostic: {issues}"
    print("test_orphan_fence_diagnostic: PASS")

def test_bom_ledger_still_parsed():
    root = _new_root()
    lg = root / "sci-skills" / "thesis-terminology-ledger.md"
    lg.parent.mkdir(parents=True)
    lg.write_bytes(codecs.BOM_UTF8 + LEDGER_SETTLED.encode("utf-8"))
    td = root / "thesis" / "tex"
    td.mkdir(parents=True)
    bad = TEX_CLEAN + "卷积神经网络残留。\n"
    (td / "ch0.tex").write_text(bad, encoding="utf-8")
    issues = check_polish.check(td, lg)
    assert any("卷积神经网络" in i for i in issues), f"BOM must not drop first table: {issues}"
    print("test_bom_ledger_still_parsed: PASS")

def test_binary_ledger_graceful():
    lg, td = _write_project()
    lg.write_bytes(b"\xff\xfe\x00\x01garbage non-utf8")
    try:
        issues = check_polish.check(td, lg)
        assert any("UTF-8" in i or "二进制" in i for i in issues), f"expected graceful: {issues}"
    except Exception as e:
        assert False, f"check() raised {type(e).__name__} — must be graceful"
    print("test_binary_ledger_graceful: PASS")

def test_binary_tex_graceful():
    lg, td = _write_project()
    (td / "ch0.tex").write_bytes(b"\xff\xfe\x00\x01\xffi\x00garbage")
    try:
        issues = check_polish.check(td, lg)
        assert isinstance(issues, list), "must return a list, never raise"
    except Exception as e:
        assert False, f"check() raised {type(e).__name__} — must be graceful"
    print("test_binary_tex_graceful: PASS")

def test_ansi_stripped_from_issues():
    ansi_ledger = LEDGER_SETTLED.replace("| CNN |", "| CN\x1b[31mN\x1b[0m |")
    lg, td = _write_project(ledger=ansi_ledger,
                            texs={"ch0.tex": TEX_CLEAN + "卷积神经网络残留。\n"})
    issues = check_polish.check(td, lg)
    assert any("卷积神经网络" in i for i in issues), "residue issue must fire"
    assert not any("\x1b" in i for i in issues), f"ANSI leaked into issues: {issues}"
    print("test_ansi_stripped_from_issues: PASS")

def test_separator_row_skipped():
    sep = LEDGER_SETTLED.replace(
        "| 缩写 | 卷积神经网络 / 卷积网络 / convnet | CNN | thesis-spine | 全文统一 |",
        "| 缩写 | 卷积神经网络 / 卷积网络 / convnet | CNN | thesis-spine | 全文统一 |\n|---|---|---|---|---|")
    lg, td = _write_project(ledger=sep)
    issues = check_polish.check(td, lg)
    assert not any("separator" in i.lower() or "CNN | ---" in i for i in issues), \
        f"separator row must not produce a bogus pair: {issues}"
    print("test_separator_row_skipped: PASS")

def test_header_name_matching_tolerates_columns():
    """P6: a FOUR-column ledger (no Category) and an EXTRA column both parse —
    header-name matching, not column-count matching."""
    four_col = """# ledger
| Term / variants | Canonical form | Source | Notes |
|---|---|---|---|
| 卷积神经网络 | CNN | thesis-spine | ok |
"""
    lg, td = _write_project(ledger=four_col,
                            texs={"ch0.tex": TEX_CLEAN + "卷积神经网络残留。\n"})
    issues = check_polish.check(td, lg)
    assert any("卷积神经网络" in i and "CNN" in i for i in issues), \
        f"four-column must parse via header names: {issues}"
    print("test_header_name_matching_tolerates_columns: PASS")

def test_non_term_table_ignored():
    mixed = LEDGER_SETTLED + "\n| 步骤 | 说明 |\n|---|---|\n| 1 | 干活 |\n"
    lg, td = _write_project(ledger=mixed)
    issues = check_polish.check(td, lg)
    assert not any("干活" in i for i in issues), f"non-term table must not parse: {issues}"
    print("test_non_term_table_ignored: PASS")

def test_variant_inside_canonical_skipped():
    """F2(b)：变体 ⊂ 自身规范形（T ⊂ $T(x)$）= 永不可 enforce 的自啮对——跳过，
    正确文本含规范形不误报。"""
    selfbite = LEDGER_SETTLED + "| 记号 | T | $T(x)$ | thesis-theory | 包壳记号 |\n"
    lg, td = _write_project(ledger=selfbite)  # TEX_CLEAN 含 $T(x)$ ——规范形自身
    issues = check_polish.check(td, lg)
    assert not any("`T`" in i for i in issues), f"self-bite pair must be skipped: {issues}"
    print("test_variant_inside_canonical_skipped: PASS")

def test_truncation_cap():
    """bounded output: 250 dangling refs → exactly MAX_ISSUES issues + 1 truncation line."""
    lines = [TEX_CLEAN] + [f"见 \\ref{{fig:x{i}}}。\n" for i in range(250)]
    lg, td = _write_project(texs={"ch0.tex": "".join(lines)})
    issues = check_polish.check(td, lg)
    assert len(issues) == check_polish.MAX_ISSUES + 1, \
        f"expected {check_polish.MAX_ISSUES + 1} lines (cap + truncation), got {len(issues)}"
    assert any("截断" in i for i in issues), f"truncation line missing: {issues[-3:]}"
    print("test_truncation_cap: PASS")

def test_missing_tex_dir():
    root = _new_root()
    lg = root / "sci-skills" / "thesis-terminology-ledger.md"
    lg.parent.mkdir(parents=True)
    lg.write_text(LEDGER_SETTLED, encoding="utf-8")
    issues = check_polish.check(root / "thesis" / "tex", lg)
    assert any("不存在" in i for i in issues), f"expected missing-dir issue: {issues}"
    print("test_missing_tex_dir: PASS")

def test_empty_tex_dir():
    lg, td = _write_project(texs={})
    issues = check_polish.check(td, lg)
    assert any("无 .tex 文件" in i for i in issues), f"expected empty-dir issue: {issues}"
    print("test_empty_tex_dir: PASS")

if __name__ == "__main__":
    test_passes_on_clean()
    test_unused_label_is_not_reported()
    test_fails_on_cjk_variant_residue()
    test_ascii_variant_word_boundary()
    test_fails_on_dangling_ref()
    test_eqref_cref_recognized_and_multikey()
    test_variant_in_comment_not_flagged()
    test_ref_in_comment_not_flagged()
    test_escaped_percent_keeps_text()
    test_double_backslash_then_percent_is_comment()
    test_ledger_missing_degrades_to_crossref()
    test_ledger_without_table()
    test_ledger_table_in_fence_ignored()
    test_orphan_fence_diagnostic()
    test_bom_ledger_still_parsed()
    test_binary_ledger_graceful()
    test_binary_tex_graceful()
    test_ansi_stripped_from_issues()
    test_separator_row_skipped()
    test_header_name_matching_tolerates_columns()
    test_non_term_table_ignored()
    test_variant_inside_canonical_skipped()
    test_truncation_cap()
    test_missing_tex_dir()
    test_empty_tex_dir()
    print("ALL TESTS PASS")
