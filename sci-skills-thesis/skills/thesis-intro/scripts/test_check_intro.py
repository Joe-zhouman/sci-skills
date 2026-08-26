"""stdlib tests for check_intro.py — run: python3 test_check_intro.py

check_intro.py is a NEAR-TRIVIAL CONSISTENCY gate (not a coverage gate, not depth).
gaps ~1:1 derived from chapters by construction → coverage near-trivial.
The gate catches: 缺席 (gap-map.md missing), 官僚 lapse (fabricated chapter numbers,
dangling filled-by, pending residual, missing tex). It does NOT catch depth
(a gap no chapter genuinely fills but with a chapter number written in → passes, is depth).
"""
import importlib.util, pathlib, sys, tempfile
HERE = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("check_intro", HERE / "check_intro.py")
check_intro = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_intro)

# --- fixtures ---
# A settled gap-map.md (2 gaps) + the chapter-map.md it cross-references + chapter0.tex.
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


def _write_project(gap_map: str = GAP_MAP_SETTLED,
                   chapter_map: str = CHAPTER_MAP_SETTLED,
                   intro_tex_name: str = "chapter0.tex") -> tuple[pathlib.Path, pathlib.Path, pathlib.Path]:
    """Build a temp project: gap-map.md + chapter-map.md + thesis/tex/<intro-tex>.
    Returns (gap_map_path, chapter_map_path, tex_dir).
    (check_intro.py reads intro-tex from gap-map.md and verifies that file exists — aries #2.)"""
    root = pathlib.Path(tempfile.mkdtemp())
    gm = root / "sci-skills" / "thesis-intro" / "gap-map.md"
    gm.parent.mkdir(parents=True)
    gm.write_text(gap_map, encoding="utf-8")
    cm = root / "sci-skills" / "thesis-dissect" / "chapter-map.md"
    cm.parent.mkdir(parents=True)
    cm.write_text(chapter_map, encoding="utf-8")
    tex_dir = root / "thesis" / "tex"
    tex_dir.mkdir(parents=True)
    (tex_dir / intro_tex_name).write_text("\\chapter{绪论}", encoding="utf-8")
    return gm, cm, tex_dir


def test_passes_on_settled():
    gm, cm, tex_dir = _write_project()
    issues = check_intro.check(gm, cm, tex_dir)
    assert issues == [], f"expected pass, got: {issues}"
    print("test_passes_on_settled: PASS")

def test_fails_on_missing_gap_field():
    """gap missing the `gap:` field → issue."""
    bad = GAP_MAP_SETTLED.replace("- gap: 现有方法在高温条件下失效\n", "")
    gm, cm, tex_dir = _write_project(gap_map=bad)
    issues = check_intro.check(gm, cm, tex_dir)
    assert any("gap" in i and "Gap 1" in i for i in issues), f"expected gap-field issue, got: {issues}"
    print("test_fails_on_missing_gap_field: PASS")

def test_fails_on_empty_gap():
    """gap field present but empty/none → issue."""
    bad = GAP_MAP_SETTLED.replace("- gap: 现有方法在高温条件下失效",
                                  "- gap: none")
    gm, cm, tex_dir = _write_project(gap_map=bad)
    issues = check_intro.check(gm, cm, tex_dir)
    assert any("gap" in i and "Gap 1" in i for i in issues), f"expected empty-gap issue, got: {issues}"
    print("test_fails_on_empty_gap: PASS")

def test_fails_on_missing_filled_by():
    bad = GAP_MAP_SETTLED.replace("- filled-by: Chapter 1\n", "")
    gm, cm, tex_dir = _write_project(gap_map=bad)
    issues = check_intro.check(gm, cm, tex_dir)
    assert any("filled-by" in i and "Gap 1" in i for i in issues), f"expected filled-by issue, got: {issues}"
    print("test_fails_on_missing_filled_by: PASS")

def test_fails_on_empty_filled_by():
    bad = GAP_MAP_SETTLED.replace("- filled-by: Chapter 1",
                                  "- filled-by: none")
    gm, cm, tex_dir = _write_project(gap_map=bad)
    issues = check_intro.check(gm, cm, tex_dir)
    assert any("filled-by" in i and "Gap 1" in i for i in issues), f"expected empty-filled-by issue, got: {issues}"
    print("test_fails_on_empty_filled_by: PASS")

def test_fails_on_status_pending():
    bad = GAP_MAP_SETTLED.replace("- status: filled\n\n## Gap 2",
                                  "- status: pending\n\n## Gap 2")
    gm, cm, tex_dir = _write_project(gap_map=bad)
    issues = check_intro.check(gm, cm, tex_dir)
    assert any("status" in i and "Gap 1" in i for i in issues), f"expected status issue, got: {issues}"
    print("test_fails_on_status_pending: PASS")

def test_fails_on_status_unfilled():
    """status=unfilled = contract gap (gap no chapter fills) → must fail."""
    bad = GAP_MAP_SETTLED.replace("- status: filled\n\n## Gap 2",
                                  "- status: unfilled\n\n## Gap 2")
    gm, cm, tex_dir = _write_project(gap_map=bad)
    issues = check_intro.check(gm, cm, tex_dir)
    assert any("status" in i and "Gap 1" in i for i in issues), f"expected unfilled issue, got: {issues}"
    print("test_fails_on_status_unfilled: PASS")

def test_fails_on_pending_residual():
    """A `[pending?` marker anywhere = unsettled candidate → fail (mirror check_spine)."""
    bad = GAP_MAP_SETTLED + "\n## Gap 3\n- gap: [pending? ] TBD\n- filled-by: Chapter 1\n- status: filled\n"
    gm, cm, tex_dir = _write_project(gap_map=bad,
                                     chapter_map=CHAPTER_MAP_SETTLED)
    issues = check_intro.check(gm, cm, tex_dir)
    assert any("pending" in i.lower() for i in issues), f"expected pending issue, got: {issues}"
    print("test_fails_on_pending_residual: PASS")

def test_fails_on_missing_gap_map():
    gm = pathlib.Path(tempfile.mkdtemp()) / "nonexistent.md"
    cm = pathlib.Path(tempfile.mkdtemp()) / "chapter-map.md"
    cm.parent.mkdir(parents=True, exist_ok=True)
    cm.write_text(CHAPTER_MAP_SETTLED, encoding="utf-8")
    tex_dir = pathlib.Path(tempfile.mkdtemp()) / "thesis" / "tex"
    tex_dir.mkdir(parents=True)
    (tex_dir / "chapter0.tex").write_text("x", encoding="utf-8")
    issues = check_intro.check(gm, cm, tex_dir)
    assert any("不存在" in i or "not exist" in i.lower() for i in issues), f"expected missing issue, got: {issues}"
    print("test_fails_on_missing_gap_map: PASS")

def test_fails_on_missing_intro_tex_file():
    """intro-tex field present but the named file absent from thesis/tex/ → issue."""
    gm, cm, tex_dir = _write_project()
    (tex_dir / "chapter0.tex").unlink()
    issues = check_intro.check(gm, cm, tex_dir)
    assert any("chapter0.tex" in i and "不存在" in i for i in issues), f"expected missing-intro-tex issue, got: {issues}"
    print("test_fails_on_missing_intro_tex_file: PASS")

def test_fails_on_missing_intro_tex_field():
    """gap-map.md has no top-level `intro-tex:` field → issue (aries #2)."""
    bad = GAP_MAP_SETTLED.replace("intro-tex: chapter0.tex\n\n## Gap 1", "## Gap 1")
    gm, cm, tex_dir = _write_project(gap_map=bad)
    issues = check_intro.check(gm, cm, tex_dir)
    assert any("intro-tex" in i for i in issues), f"expected missing-intro-tex-field issue, got: {issues}"
    print("test_fails_on_missing_intro_tex_field: PASS")

def test_passes_with_template_named_intro_tex():
    """intro-tex = chapter0.tex (per generic-test template-spec) + that file exists → pass (aries #2: template-derived)."""
    gm, cm, tex_dir = _write_project(intro_tex_name="chapter0.tex")  # GAP_MAP_SETTLED already has intro-tex: chapter0.tex
    issues = check_intro.check(gm, cm, tex_dir)
    assert issues == [], f"template-named intro-tex should pass: {issues}"
    print("test_passes_with_template_named_intro_tex: PASS")

def test_graceful_on_binary_gap_map():
    """Binary/non-utf8 gap-map.md must not raise — graceful issue."""
    root = pathlib.Path(tempfile.mkdtemp())
    gm = root / "sci-skills" / "thesis-intro" / "gap-map.md"
    gm.parent.mkdir(parents=True)
    gm.write_bytes(b"\xff\xfe\x00\x01garbage non-utf8")
    cm = root / "sci-skills" / "thesis-dissect" / "chapter-map.md"
    cm.parent.mkdir(parents=True)
    cm.write_text(CHAPTER_MAP_SETTLED, encoding="utf-8")
    tex_dir = root / "thesis" / "tex"; tex_dir.mkdir(parents=True)
    (tex_dir / "chapter0.tex").write_text("x", encoding="utf-8")
    try:
        issues = check_intro.check(gm, cm, tex_dir)
        assert issues and any("UTF-8" in i or "二进制" in i for i in issues), f"expected graceful, got: {issues}"
    except Exception as e:
        assert False, f"check() raised {type(e).__name__} — must be graceful"
    print("test_graceful_on_binary_gap_map: PASS")

def test_ignores_utf8_bom_in_gap_map():
    """A UTF-8 BOM (Windows editor) must not drop Gap 1 from checks (aries #1).
    Gap 1 has a dangling filled-by: Chapter 999 — with BOM stripped, it must be caught."""
    import codecs
    root = pathlib.Path(tempfile.mkdtemp())
    gm = root / "sci-skills" / "thesis-intro" / "gap-map.md"
    gm.parent.mkdir(parents=True)
    # gap-map starting directly with ## Gap 1 (no leading # comment) + BOM
    gm.write_bytes(codecs.BOM_UTF8 + b"## Gap 1\n- gap: x\n- filled-by: Chapter 999\n- callback-anchor: y\n- status: filled\n")
    cm = root / "sci-skills" / "thesis-dissect" / "chapter-map.md"
    cm.parent.mkdir(parents=True)
    cm.write_text("## Chapter 1\n- tex-file: ch1.tex\n- status: written\n", encoding="utf-8")
    tex_dir = root / "thesis" / "tex"; tex_dir.mkdir(parents=True)
    (tex_dir / "chapter0.tex").write_text("x", encoding="utf-8")
    issues = check_intro.check(gm, cm, tex_dir)
    assert any("Chapter 999" in i for i in issues), f"BOM stripped → dangling Ch999 must be caught, got: {issues}"
    print("test_ignores_utf8_bom_in_gap_map: PASS")

def test_fails_on_dangling_filled_by():
    """filled-by = Chapter 9 but chapter-map.md only has ch1-2 → fabricated/dangling → issue."""
    # gap-map references Chapter 9; chapter-map has only ch1-2
    bad = GAP_MAP_SETTLED.replace("- filled-by: Chapter 2\n- callback-anchor",
                                  "- filled-by: Chapter 9\n- callback-anchor")
    gm, cm, tex_dir = _write_project(gap_map=bad)
    issues = check_intro.check(gm, cm, tex_dir)
    assert any("Chapter 9" in i and ("不在" in i or "not in" in i.lower() or "dangling" in i.lower() or "悬空" in i) for i in issues), \
           f"expected dangling-filled-by issue, got: {issues}"
    print("test_fails_on_dangling_filled_by: PASS")

def test_fails_on_missing_chapter_map():
    """chapter-map.md missing → can't cross-ref → issue (dissect hasn't run)."""
    gm, cm, tex_dir = _write_project()
    cm.unlink()
    issues = check_intro.check(gm, cm, tex_dir)
    assert any("chapter-map" in i.lower() and ("不存在" in i or "not exist" in i.lower()) for i in issues), \
           f"expected missing-chapter-map issue, got: {issues}"
    print("test_fails_on_missing_chapter_map: PASS")

def test_fails_on_unreadable_chapter_map():
    """chapter-map.md exists but is binary/non-utf8 → 'cross-ref 跳过' issue + exit 1 (taurus fix, aries #3 untested)."""
    root = pathlib.Path(tempfile.mkdtemp())
    gm = root / "sci-skills" / "thesis-intro" / "gap-map.md"
    gm.parent.mkdir(parents=True)
    gm.write_text(GAP_MAP_SETTLED, encoding="utf-8")
    cm = root / "sci-skills" / "thesis-dissect" / "chapter-map.md"
    cm.parent.mkdir(parents=True)
    cm.write_bytes(b"\xff\xfe\x00\x01garbage non-utf8")
    tex_dir = root / "thesis" / "tex"; tex_dir.mkdir(parents=True)
    (tex_dir / "chapter0.tex").write_text("x", encoding="utf-8")
    issues = check_intro.check(gm, cm, tex_dir)
    assert any("不可读" in i and "cross-ref 跳过" in i for i in issues), f"expected unreadable-chapter-map issue, got: {issues}"
    print("test_fails_on_unreadable_chapter_map: PASS")

def test_fails_on_malformed_filled_by():
    """filled-by = 'some chapter' (no number) → can't cross-ref → issue."""
    bad = GAP_MAP_SETTLED.replace("- filled-by: Chapter 1\n",
                                  "- filled-by: some chapter\n")
    gm, cm, tex_dir = _write_project(gap_map=bad)
    issues = check_intro.check(gm, cm, tex_dir)
    assert any("filled-by" in i and "Gap 1" in i for i in issues), \
           f"expected malformed-filled-by issue, got: {issues}"
    print("test_fails_on_malformed_filled_by: PASS")

def test_fails_on_multi_chapter_filled_by():
    """filled-by = 'Chapter 1 Chapter 999' (two numbers) → malformed → issue (aries #5; spec: one gap→one chapter)."""
    bad = GAP_MAP_SETTLED.replace("- filled-by: Chapter 1\n",
                                  "- filled-by: Chapter 1 Chapter 999\n")
    gm, cm, tex_dir = _write_project(gap_map=bad)
    issues = check_intro.check(gm, cm, tex_dir)
    assert any("filled-by" in i and "Gap 1" in i for i in issues), f"expected multi-chapter filled-by issue, got: {issues}"
    print("test_fails_on_multi_chapter_filled_by: PASS")

def test_ignores_chapter_headers_inside_code_fence():
    """chapter-map.md with `## Chapter 99` inside a code fence → 99 NOT a valid chapter →
    a gap filled-by: Chapter 99 must still fail cross-ref (mirror check_dissect aries #2)."""
    bad_cm = CHAPTER_MAP_SETTLED + "\n```\n## Chapter 99\n- fake\n```\n"
    # gap references Chapter 99 (which is ONLY inside a code fence → must be treated as absent)
    bad_gm = GAP_MAP_SETTLED.replace("- filled-by: Chapter 2\n- callback-anchor",
                                     "- filled-by: Chapter 99\n- callback-anchor")
    gm, cm, tex_dir = _write_project(gap_map=bad_gm, chapter_map=bad_cm)
    issues = check_intro.check(gm, cm, tex_dir)
    assert any("Chapter 99" in i and ("不在" in i or "悬空" in i) for i in issues), \
           f"code-fenced Chapter 99 must NOT count as valid → expected dangling issue, got: {issues}"
    print("test_ignores_chapter_headers_inside_code_fence: PASS")

# (no test_passes_when_all_filled_by_resolve — redundant with test_passes_on_settled,
# which asserts the strictly stronger `issues == []`. aquarius plan review finding.)

def test_fails_on_missing_callback_anchor():
    """gap missing the `callback-anchor:` field → issue (it's the field that earns gap-map.md its existence)."""
    bad = GAP_MAP_SETTLED.replace("- callback-anchor: summary 须回扣高温条件下的有效性\n", "")
    gm, cm, tex_dir = _write_project(gap_map=bad)
    issues = check_intro.check(gm, cm, tex_dir)
    assert any("callback-anchor" in i and "Gap 1" in i for i in issues), f"expected callback-anchor issue, got: {issues}"
    print("test_fails_on_missing_callback_anchor: PASS")

def test_fails_on_empty_callback_anchor():
    """callback-anchor present but empty/none → issue."""
    bad = GAP_MAP_SETTLED.replace("- callback-anchor: summary 须回扣高温条件下的有效性",
                                  "- callback-anchor: none")
    gm, cm, tex_dir = _write_project(gap_map=bad)
    issues = check_intro.check(gm, cm, tex_dir)
    assert any("callback-anchor" in i and "Gap 1" in i for i in issues), f"expected empty callback-anchor issue, got: {issues}"
    print("test_fails_on_empty_callback_anchor: PASS")

def test_accepts_gap_headers_with_trailing_title():
    """`## Gap 1 (研究背景)` (trailing title) must parse — mirrors check_dissect's trailing-title test."""
    titled = GAP_MAP_SETTLED.replace("## Gap 1\n", "## Gap 1 (研究背景)\n")
    gm, cm, tex_dir = _write_project(gap_map=titled)
    issues = check_intro.check(gm, cm, tex_dir)
    assert issues == [], f"trailing-title gap header should parse (not be flagged missing): {issues}"
    print("test_accepts_gap_headers_with_trailing_title: PASS")

if __name__ == "__main__":
    test_passes_on_settled()
    test_fails_on_missing_gap_field()
    test_fails_on_empty_gap()
    test_fails_on_missing_filled_by()
    test_fails_on_empty_filled_by()
    test_fails_on_status_pending()
    test_fails_on_status_unfilled()
    test_fails_on_pending_residual()
    test_fails_on_missing_gap_map()
    test_fails_on_missing_intro_tex_file()
    test_fails_on_missing_intro_tex_field()
    test_passes_with_template_named_intro_tex()
    test_ignores_utf8_bom_in_gap_map()
    test_graceful_on_binary_gap_map()
    test_fails_on_dangling_filled_by()
    test_fails_on_missing_chapter_map()
    test_fails_on_unreadable_chapter_map()
    test_fails_on_malformed_filled_by()
    test_fails_on_multi_chapter_filled_by()
    test_ignores_chapter_headers_inside_code_fence()
    test_fails_on_missing_callback_anchor()
    test_fails_on_empty_callback_anchor()
    test_accepts_gap_headers_with_trailing_title()
    print("ALL TESTS PASS")
