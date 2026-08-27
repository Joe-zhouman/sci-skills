"""stdlib tests for check_summary.py — run: python3 test_check_summary.py

check_summary.py is a NEAR-TRIVIAL CONSISTENCY gate (not depth, not a post-polish
invariant — write-time check). Commonality confirmed-footprint + unfilled state are
the genuinely-new content; gap↔Callback bijection is near-trivial-by-construction
(real value = 缺席检测); resolved-how is a write-time self-record. The gate catches:
缺席 (summary-map.md missing / gap without a Callback), 官僚 lapse (fabricated Gap
refs / dangling chapter numbers / pending residual / missing synthesis-tex file).
It does NOT catch depth (an agent can write resolved-how without real prose —
prose-vs-promise, author + eval).
"""
import importlib.util, pathlib, sys, tempfile
HERE = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("check_summary", HERE / "check_summary.py")
check_summary = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_summary)

# --- fixtures ---
# A settled summary-map.md (2 callbacks + 1 commonality) + the gap-map.md it
# cross-references + the chapter-map.md + chapter5.tex (the synthesis tex).
SUMMARY_MAP_SETTLED = """# summary-map.md
> summary 写后 baton (DATA).

synthesis-tex: chapter5.tex

## Callback 1
- gap-ref: Gap 1
- resolved-how: 第 5 章回顾高温条件下的有效性，收束 Gap 1
- status: filled

## Callback 2
- gap-ref: Gap 2
- resolved-how: 第 5 章回顾可解释性贡献，收束 Gap 2
- status: filled

## Commonality 1
- commonality: 两章以统一框架 X 的同一实例化方式处理各自对象
- grounded-in: [Chapter 1 §2 result, Chapter 2 §3 result]
- status: confirmed
"""

GAP_MAP_SETTLED = """# gap-map.md
> intro→summary 交接 baton (DATA).

intro-tex: chapter0.tex

## Gap 1
- gap: 现有方法在高温条件下失效
- filled-by: Chapter 1
- callback-anchor: summary 须回扣高温条件下的有效性
- status: filled

## Gap 2
- gap: 黑箱模型不可解释
- filled-by: Chapter 2
- callback-anchor: summary 须回扣可解释性贡献
- status: filled
"""

CHAPTER_MAP_SETTLED = """# chapter-map.md
> dissect→summary 交接 baton.

## Chapter 1
- role(s): role 1
- papers: [paper-A]
- framework-instantiation: X 框架分析 A
- progression-in: none
- progression-out: 引发 ch2
- tex-file: ch1.tex
- status: written

## Chapter 2
- role(s): role 2
- papers: [paper-B]
- framework-instantiation: X 框架分析 B
- progression-in: ch1 引发
- progression-out: none
- tex-file: ch2.tex
- status: written
"""


def _write_project(summary_map: str = SUMMARY_MAP_SETTLED,
                   gap_map: str = GAP_MAP_SETTLED,
                   chapter_map: str = CHAPTER_MAP_SETTLED,
                   synthesis_tex_name: str = "chapter5.tex") -> tuple[pathlib.Path, pathlib.Path, pathlib.Path, pathlib.Path]:
    """Build a temp project: summary-map.md + gap-map.md + chapter-map.md +
    thesis/tex/<synthesis-tex>. Returns (sm, gm, cm, tex_dir)."""
    root = pathlib.Path(tempfile.mkdtemp())
    sm = root / "sci-skills" / "thesis-summary" / "summary-map.md"
    sm.parent.mkdir(parents=True)
    sm.write_text(summary_map, encoding="utf-8")
    gm = root / "sci-skills" / "thesis-intro" / "gap-map.md"
    gm.parent.mkdir(parents=True)
    gm.write_text(gap_map, encoding="utf-8")
    cm = root / "sci-skills" / "thesis-dissect" / "chapter-map.md"
    cm.parent.mkdir(parents=True)
    cm.write_text(chapter_map, encoding="utf-8")
    tex_dir = root / "thesis" / "tex"
    tex_dir.mkdir(parents=True)
    (tex_dir / synthesis_tex_name).write_text("\\chapter{总结与展望}", encoding="utf-8")
    return sm, gm, cm, tex_dir


def test_passes_on_settled():
    sm, gm, cm, tex_dir = _write_project()
    issues = check_summary.check(sm, gm, cm, tex_dir)
    assert issues == [], f"expected pass, got: {issues}"
    print("test_passes_on_settled: PASS")

def test_fails_on_missing_gap_ref():
    bad = SUMMARY_MAP_SETTLED.replace("- gap-ref: Gap 1\n", "")
    sm, gm, cm, tex_dir = _write_project(summary_map=bad)
    issues = check_summary.check(sm, gm, cm, tex_dir)
    assert any("gap-ref" in i and "Callback 1" in i for i in issues), f"expected gap-ref issue, got: {issues}"
    print("test_fails_on_missing_gap_ref: PASS")

def test_fails_on_malformed_gap_ref():
    bad = SUMMARY_MAP_SETTLED.replace("- gap-ref: Gap 1\n", "- gap-ref: some gap\n")
    sm, gm, cm, tex_dir = _write_project(summary_map=bad)
    issues = check_summary.check(sm, gm, cm, tex_dir)
    assert any("gap-ref" in i and "Callback 1" in i for i in issues), f"expected malformed gap-ref issue, got: {issues}"
    print("test_fails_on_malformed_gap_ref: PASS")

def test_fails_on_multi_gap_ref():
    """gap-ref = 'Gap 1 Gap 2' (two tokens) → malformed (mirror intro aries #5: one gap→one callback)."""
    bad = SUMMARY_MAP_SETTLED.replace("- gap-ref: Gap 1\n", "- gap-ref: Gap 1 Gap 2\n")
    sm, gm, cm, tex_dir = _write_project(summary_map=bad)
    issues = check_summary.check(sm, gm, cm, tex_dir)
    assert any("gap-ref" in i and "Callback 1" in i for i in issues), f"expected multi-gap-ref issue, got: {issues}"
    print("test_fails_on_multi_gap_ref: PASS")

def test_fails_on_empty_resolved_how():
    bad = SUMMARY_MAP_SETTLED.replace("- resolved-how: 第 5 章回顾高温条件下的有效性，收束 Gap 1",
                                      "- resolved-how: none")
    sm, gm, cm, tex_dir = _write_project(summary_map=bad)
    issues = check_summary.check(sm, gm, cm, tex_dir)
    assert any("resolved-how" in i and "Callback 1" in i for i in issues), f"expected empty resolved-how issue, got: {issues}"
    print("test_fails_on_empty_resolved_how: PASS")

def test_fails_on_status_pending_callback():
    bad = SUMMARY_MAP_SETTLED.replace("- status: filled\n\n## Callback 2",
                                      "- status: pending\n\n## Callback 2")
    sm, gm, cm, tex_dir = _write_project(summary_map=bad)
    issues = check_summary.check(sm, gm, cm, tex_dir)
    assert any("status" in i and "Callback 1" in i for i in issues), f"expected status issue, got: {issues}"
    print("test_fails_on_status_pending_callback: PASS")

def test_fails_on_status_unfilled_callback():
    """status=unfilled = fallback trace (callback couldn't be made) → must fail (surface to author)."""
    bad = SUMMARY_MAP_SETTLED.replace("- status: filled\n\n## Callback 2",
                                      "- status: unfilled\n\n## Callback 2")
    sm, gm, cm, tex_dir = _write_project(summary_map=bad)
    issues = check_summary.check(sm, gm, cm, tex_dir)
    assert any("status" in i and "Callback 1" in i for i in issues), f"expected unfilled issue, got: {issues}"
    print("test_fails_on_status_unfilled_callback: PASS")

def test_fails_on_missing_summary_map():
    root = pathlib.Path(tempfile.mkdtemp())
    sm = root / "sci-skills" / "thesis-summary" / "summary-map.md"
    gm = root / "sci-skills" / "thesis-intro" / "gap-map.md"
    gm.parent.mkdir(parents=True)
    gm.write_text(GAP_MAP_SETTLED, encoding="utf-8")
    cm = root / "sci-skills" / "thesis-dissect" / "chapter-map.md"
    cm.parent.mkdir(parents=True)
    cm.write_text(CHAPTER_MAP_SETTLED, encoding="utf-8")
    tex_dir = root / "thesis" / "tex"
    tex_dir.mkdir(parents=True)
    (tex_dir / "chapter5.tex").write_text("x", encoding="utf-8")
    issues = check_summary.check(sm, gm, cm, tex_dir)
    assert any("不存在" in i or "not exist" in i.lower() for i in issues), f"expected missing-summary-map issue, got: {issues}"
    print("test_fails_on_missing_summary_map: PASS")

def test_graceful_on_binary_summary_map():
    root = pathlib.Path(tempfile.mkdtemp())
    sm = root / "sci-skills" / "thesis-summary" / "summary-map.md"
    sm.parent.mkdir(parents=True)
    sm.write_bytes(b"\xff\xfe\x00\x01garbage non-utf8")
    gm = root / "sci-skills" / "thesis-intro" / "gap-map.md"
    gm.parent.mkdir(parents=True)
    gm.write_text(GAP_MAP_SETTLED, encoding="utf-8")
    cm = root / "sci-skills" / "thesis-dissect" / "chapter-map.md"
    cm.parent.mkdir(parents=True)
    cm.write_text(CHAPTER_MAP_SETTLED, encoding="utf-8")
    tex_dir = root / "thesis" / "tex"
    tex_dir.mkdir(parents=True)
    (tex_dir / "chapter5.tex").write_text("x", encoding="utf-8")
    try:
        issues = check_summary.check(sm, gm, cm, tex_dir)
        assert issues and any("UTF-8" in i or "二进制" in i for i in issues), f"expected graceful, got: {issues}"
    except Exception as e:
        assert False, f"check() raised {type(e).__name__} — must be graceful"
    print("test_graceful_on_binary_summary_map: PASS")

def test_ignores_utf8_bom_in_summary_map():
    """A UTF-8 BOM (Windows editor) must not drop Callback 1 from checks (mirror intro aries #1).
    Callback 1 has a fabricated gap-ref: Gap 999 — with BOM stripped, it must be caught."""
    import codecs
    root = pathlib.Path(tempfile.mkdtemp())
    sm = root / "sci-skills" / "thesis-summary" / "summary-map.md"
    sm.parent.mkdir(parents=True)
    sm.write_bytes(codecs.BOM_UTF8 + b"## Callback 1\n- gap-ref: Gap 999\n- resolved-how: x\n- status: filled\n")
    gm = root / "sci-skills" / "thesis-intro" / "gap-map.md"
    gm.parent.mkdir(parents=True)
    gm.write_text(GAP_MAP_SETTLED, encoding="utf-8")
    cm = root / "sci-skills" / "thesis-dissect" / "chapter-map.md"
    cm.parent.mkdir(parents=True)
    cm.write_text(CHAPTER_MAP_SETTLED, encoding="utf-8")
    tex_dir = root / "thesis" / "tex"
    tex_dir.mkdir(parents=True)
    (tex_dir / "chapter5.tex").write_text("x", encoding="utf-8")
    issues = check_summary.check(sm, gm, cm, tex_dir)
    assert any("Gap 999" in i for i in issues), f"BOM stripped → fabricated Gap 999 must be caught, got: {issues}"
    print("test_ignores_utf8_bom_in_summary_map: PASS")

def test_accepts_entry_headers_with_trailing_title():
    """`## Callback 1 (高温)` (trailing title) must parse — mirrors intro's trailing-title test."""
    titled = SUMMARY_MAP_SETTLED.replace("## Callback 1\n", "## Callback 1 (高温)\n")
    sm, gm, cm, tex_dir = _write_project(summary_map=titled)
    issues = check_summary.check(sm, gm, cm, tex_dir)
    assert issues == [], f"trailing-title header should parse: {issues}"
    print("test_accepts_entry_headers_with_trailing_title: PASS")

def test_fails_on_missing_synthesis_tex_field():
    bad = SUMMARY_MAP_SETTLED.replace("synthesis-tex: chapter5.tex\n\n## Callback 1", "## Callback 1")
    sm, gm, cm, tex_dir = _write_project(summary_map=bad)
    issues = check_summary.check(sm, gm, cm, tex_dir)
    assert any("synthesis-tex" in i for i in issues), f"expected missing-synthesis-tex-field issue, got: {issues}"
    print("test_fails_on_missing_synthesis_tex_field: PASS")

def test_fails_on_missing_synthesis_tex_file():
    sm, gm, cm, tex_dir = _write_project()
    (tex_dir / "chapter5.tex").unlink()
    issues = check_summary.check(sm, gm, cm, tex_dir)
    assert any("chapter5.tex" in i and "不存在" in i for i in issues), f"expected missing-synthesis-tex issue, got: {issues}"
    print("test_fails_on_missing_synthesis_tex_file: PASS")

def test_fails_on_synthesis_tex_path_traversal():
    """synthesis-tex with absolute path or `..` traversal → issue (mirror intro aries re-test).
    synthesis_tex_name is file-content-derived (untrusted) — must not escape thesis/tex/."""
    # absolute path
    bad_abs = SUMMARY_MAP_SETTLED.replace("synthesis-tex: chapter5.tex", "synthesis-tex: /etc/passwd")
    sm, gm, cm, tex_dir = _write_project(summary_map=bad_abs)
    issues = check_summary.check(sm, gm, cm, tex_dir)
    assert any("synthesis-tex" in i and ("之外" in i or "绝对" in i or "traversal" in i.lower()) for i in issues), \
           f"absolute synthesis-tex must be rejected, got: {issues}"
    # relative .. traversal
    bad_rel = SUMMARY_MAP_SETTLED.replace("synthesis-tex: chapter5.tex", "synthesis-tex: ../../../etc/passwd")
    sm, gm, cm, tex_dir = _write_project(summary_map=bad_rel)
    issues = check_summary.check(sm, gm, cm, tex_dir)
    assert any("synthesis-tex" in i and ("之外" in i or "traversal" in i.lower() or ".." in i) for i in issues), \
           f"`..` traversal synthesis-tex must be rejected, got: {issues}"
    print("test_fails_on_synthesis_tex_path_traversal: PASS")

if __name__ == "__main__":
    test_passes_on_settled()
    test_fails_on_missing_gap_ref()
    test_fails_on_malformed_gap_ref()
    test_fails_on_multi_gap_ref()
    test_fails_on_empty_resolved_how()
    test_fails_on_status_pending_callback()
    test_fails_on_status_unfilled_callback()
    test_fails_on_missing_summary_map()
    test_graceful_on_binary_summary_map()
    test_ignores_utf8_bom_in_summary_map()
    test_accepts_entry_headers_with_trailing_title()
    test_fails_on_missing_synthesis_tex_field()
    test_fails_on_missing_synthesis_tex_file()
    test_fails_on_synthesis_tex_path_traversal()
    print("ALL TESTS PASS")
