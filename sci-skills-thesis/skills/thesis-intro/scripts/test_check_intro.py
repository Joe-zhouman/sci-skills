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
# A settled gap-map.md (2 gaps) + the chapter-map.md it cross-references + ch0-intro.tex.
GAP_MAP_SETTLED = """# gap-map.md
> intro→summary 交接 baton (DATA).

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
                   intro_tex: str = "\\chapter{绪论}") -> tuple[pathlib.Path, pathlib.Path, pathlib.Path]:
    """Build a temp project: gap-map.md + chapter-map.md + thesis/tex/ch0-intro.tex.
    Returns (gap_map_path, chapter_map_path, tex_dir).
    (check_intro.py only verifies ch0-intro.tex — no chN.tex fixture needed; aquarius plan review.)"""
    root = pathlib.Path(tempfile.mkdtemp())
    gm = root / "sci-skills" / "thesis-intro" / "gap-map.md"
    gm.parent.mkdir(parents=True)
    gm.write_text(gap_map, encoding="utf-8")
    cm = root / "sci-skills" / "thesis-dissect" / "chapter-map.md"
    cm.parent.mkdir(parents=True)
    cm.write_text(chapter_map, encoding="utf-8")
    tex_dir = root / "thesis" / "tex"
    tex_dir.mkdir(parents=True)
    (tex_dir / "ch0-intro.tex").write_text(intro_tex, encoding="utf-8")
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
    (tex_dir / "ch0-intro.tex").write_text("x", encoding="utf-8")
    issues = check_intro.check(gm, cm, tex_dir)
    assert any("不存在" in i or "not exist" in i.lower() for i in issues), f"expected missing issue, got: {issues}"
    print("test_fails_on_missing_gap_map: PASS")

def test_fails_on_missing_ch0_intro_tex():
    """ch0-intro.tex absent from thesis/tex/ → issue (intro didn't produce its tex)."""
    gm, cm, tex_dir = _write_project()
    (tex_dir / "ch0-intro.tex").unlink()
    issues = check_intro.check(gm, cm, tex_dir)
    assert any("ch0-intro.tex" in i for i in issues), f"expected missing-intro-tex issue, got: {issues}"
    print("test_fails_on_missing_ch0_intro_tex: PASS")

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
    (tex_dir / "ch0-intro.tex").write_text("x", encoding="utf-8")
    try:
        issues = check_intro.check(gm, cm, tex_dir)
        assert issues and any("UTF-8" in i or "二进制" in i for i in issues), f"expected graceful, got: {issues}"
    except Exception as e:
        assert False, f"check() raised {type(e).__name__} — must be graceful"
    print("test_graceful_on_binary_gap_map: PASS")

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
    test_fails_on_missing_ch0_intro_tex()
    test_graceful_on_binary_gap_map()
    print("ALL CORE TESTS PASS")
