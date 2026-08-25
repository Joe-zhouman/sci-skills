"""stdlib tests for check_dissect.py — run: python3 test_check_dissect.py"""
import importlib.util, pathlib, sys, tempfile
HERE = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("check_dissect", HERE / "check_dissect.py")
check_dissect = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_dissect)

# --- fixtures ---
# A settled chapter-map.md (2 chapters) + the tex files they reference.
SETTLED = """# chapter-map.md
> dissect→summary 交接 baton。

## Chapter 1
- role(s): role 1
- papers: [paper-A]
- framework-instantiation: 本章用 X 框架分析 A
- progression-in: none
- progression-out: ch1 的 results 引发 ch2 的 question
- tex-file: ch1.tex
- status: written

## Chapter 2
- role(s): role 2
- papers: [paper-B]
- framework-instantiation: 本章用 X 框架分析 B
- progression-in: ch1 的 results 引发本章 question
- progression-out: none
- tex-file: ch2.tex
- status: written
"""

def _write_project(content: str, tex_files: dict[str, str] | None = None) -> tuple[pathlib.Path, pathlib.Path]:
    """Build a temp project: chapter-map.md + thesis/tex/<files>. Returns (cm_path, tex_dir)."""
    root = pathlib.Path(tempfile.mkdtemp())
    cm = root / "sci-skills" / "thesis-dissect" / "chapter-map.md"
    cm.parent.mkdir(parents=True)
    cm.write_text(content, encoding="utf-8")
    tex_dir = root / "thesis" / "tex"
    tex_dir.mkdir(parents=True)
    for name, body in (tex_files or {"ch1.tex": "x", "ch2.tex": "x"}).items():
        (tex_dir / name).write_text(body, encoding="utf-8")
    return cm, tex_dir

def test_passes_on_settled():
    cm, tex_dir = _write_project(SETTLED)
    issues = check_dissect.check(cm, tex_dir)
    assert issues == [], f"expected pass, got: {issues}"
    print("test_passes_on_settled: PASS")

def test_fails_on_missing_framework_instantiation():
    bad = SETTLED.replace("- framework-instantiation: 本章用 X 框架分析 A\n", "")
    cm, tex_dir = _write_project(bad)
    issues = check_dissect.check(cm, tex_dir)
    assert any("framework-instantiation" in i for i in issues), f"expected fi issue, got: {issues}"
    print("test_fails_on_missing_framework_instantiation: PASS")

def test_fails_on_empty_framework_instantiation():
    bad = SETTLED.replace("- framework-instantiation: 本章用 X 框架分析 A",
                          "- framework-instantiation: none")
    cm, tex_dir = _write_project(bad)
    issues = check_dissect.check(cm, tex_dir)
    assert any("framework-instantiation" in i and ("空" in i or "empt" in i.lower()) for i in issues), \
           f"expected empty-fi issue, got: {issues}"
    print("test_fails_on_empty_framework_instantiation: PASS")

def test_ch1_progression_in_none_ok():
    """ch1 progression-in=none is OK (not a failure) — ch1 has no prior chapter."""
    cm, tex_dir = _write_project(SETTLED)  # ch1 already has progression-in: none
    issues = check_dissect.check(cm, tex_dir)
    assert not any("progression-in" in i and "Chapter 1" in i for i in issues), \
           f"ch1 progression-in=none must not fail: {issues}"
    print("test_ch1_progression_in_none_ok: PASS")

def test_fails_on_non_ch1_missing_progression_in():
    bad = SETTLED.replace("- progression-in: ch1 的 results 引发本章 question",
                          "- progression-in: none")  # ch2 now has none → fail
    cm, tex_dir = _write_project(bad)
    issues = check_dissect.check(cm, tex_dir)
    assert any("progression-in" in i and "Chapter 2" in i for i in issues), \
           f"ch2 progression-in=none must fail: {issues}"
    print("test_fails_on_non_ch1_missing_progression_in: PASS")

def test_last_chapter_progression_out_none_ok():
    """last chapter progression-out=none is OK."""
    cm, tex_dir = _write_project(SETTLED)  # ch2 (last) already has progression-out: none
    issues = check_dissect.check(cm, tex_dir)
    assert not any("progression-out" in i and "Chapter 2" in i for i in issues), \
           f"last ch progression-out=none must not fail: {issues}"
    print("test_last_chapter_progression_out_none_ok: PASS")

def test_fails_on_non_last_missing_progression_out():
    bad = SETTLED.replace("- progression-out: ch1 的 results 引发 ch2 的 question",
                          "- progression-out: none")  # ch1 (non-last) now has none → fail
    cm, tex_dir = _write_project(bad)
    issues = check_dissect.check(cm, tex_dir)
    assert any("progression-out" in i and "Chapter 1" in i for i in issues), \
           f"ch1 (non-last) progression-out=none must fail: {issues}"
    print("test_fails_on_non_last_missing_progression_out: PASS")

def test_fails_on_status_pending():
    bad = SETTLED.replace("- tex-file: ch1.tex\n- status: written",
                          "- tex-file: ch1.tex\n- status: pending")
    cm, tex_dir = _write_project(bad)
    issues = check_dissect.check(cm, tex_dir)
    assert any("status" in i and "Chapter 1" in i for i in issues), f"expected status issue, got: {issues}"
    print("test_fails_on_status_pending: PASS")

def test_fails_on_status_stale():
    """stale = backtrack-spine marked it; must fail coverage (not settled)."""
    bad = SETTLED.replace("- tex-file: ch1.tex\n- status: written",
                          "- tex-file: ch1.tex\n- status: stale")
    cm, tex_dir = _write_project(bad)
    issues = check_dissect.check(cm, tex_dir)
    assert any("status" in i and "stale" in i.lower() for i in issues), f"expected stale issue, got: {issues}"
    print("test_fails_on_status_stale: PASS")

def test_fails_on_missing_chapter_map():
    cm = pathlib.Path(tempfile.mkdtemp()) / "nonexistent.md"
    tex_dir = pathlib.Path(tempfile.mkdtemp()) / "thesis" / "tex"
    tex_dir.mkdir(parents=True)
    issues = check_dissect.check(cm, tex_dir)
    assert any("不存在" in i or "not exist" in i.lower() for i in issues), f"expected missing issue, got: {issues}"
    print("test_fails_on_missing_chapter_map: PASS")

def test_graceful_on_binary_file():
    """Binary/non-utf8 chapter-map.md must not raise — graceful issue."""
    root = pathlib.Path(tempfile.mkdtemp())
    cm = root / "sci-skills" / "thesis-dissect" / "chapter-map.md"
    cm.parent.mkdir(parents=True)
    cm.write_bytes(b"\xff\xfe\x00\x01garbage non-utf8")
    tex_dir = root / "thesis" / "tex"; tex_dir.mkdir(parents=True)
    try:
        issues = check_dissect.check(cm, tex_dir)
        assert issues and any("UTF-8" in i or "二进制" in i for i in issues), f"expected graceful, got: {issues}"
    except Exception as e:
        assert False, f"check() raised {type(e).__name__} — must be graceful"
    print("test_graceful_on_binary_file: PASS")

def test_fails_on_missing_tex_file():
    """chapter references ch1.tex but it's absent from thesis/tex/ → coverage issue."""
    cm, tex_dir = _write_project(SETTLED, tex_files={"ch2.tex": "x"})  # ch1.tex missing
    issues = check_dissect.check(cm, tex_dir)
    assert any("ch1.tex" in i and "不存在" in i for i in issues), \
           f"expected missing-tex-file issue, got: {issues}"
    print("test_fails_on_missing_tex_file: PASS")

def test_fails_on_missing_tex_file_field():
    """chapter has no tex-file field at all → coverage issue."""
    bad = SETTLED.replace("- tex-file: ch1.tex\n", "")
    cm, tex_dir = _write_project(bad)
    issues = check_dissect.check(cm, tex_dir)
    assert any("tex-file" in i and "Chapter 1" in i for i in issues), \
           f"expected missing-tex-file-field issue, got: {issues}"
    print("test_fails_on_missing_tex_file_field: PASS")

def test_passes_when_all_tex_files_exist():
    """all referenced tex files present → no tex-file issues."""
    cm, tex_dir = _write_project(SETTLED, tex_files={"ch1.tex": "\\chapter{A}", "ch2.tex": "\\chapter{B}"})
    issues = check_dissect.check(cm, tex_dir)
    assert not any("tex-file" in i for i in issues), f"unexpected tex-file issue: {issues}"
    print("test_passes_when_all_tex_files_exist: PASS")

def test_chapter_headers_with_trailing_title_accepted():
    """taurus #1: `## Chapter 1 (绪论)` must be parsed, not rejected → 0 chapters.
    The chapter label for issues is still 'Chapter 1'."""
    cm_with_title = SETTLED.replace("## Chapter 1\n", "## Chapter 1 (绪论)\n")
    cm_with_title = cm_with_title.replace("## Chapter 2\n", "## Chapter 2 (方法)\n")
    cm, tex_dir = _write_project(cm_with_title)
    issues = check_dissect.check(cm, tex_dir)
    # must NOT report "no entries"; must pass (settled content, just titled headers)
    assert not any("无" in i and "Chapter" in i for i in issues), \
           f"titled chapter header rejected: {issues}"
    assert issues == [], f"expected pass on titled-header settled map, got: {issues}"
    print("test_chapter_headers_with_trailing_title_accepted: PASS")

def test_graceful_on_unreadable_file():
    """taurus #2: unreadable (chmod 000) chapter-map.md must not raise — graceful issue.
    Covers the except OSError handler. Skip if root (root bypasses perms)."""
    import os
    if os.geteuid() == 0:
        print("test_graceful_on_unreadable_file: SKIP (root bypasses perms)")
        return
    root = pathlib.Path(tempfile.mkdtemp())
    cm = root / "sci-skills" / "thesis-dissect" / "chapter-map.md"
    cm.parent.mkdir(parents=True)
    cm.write_text(SETTLED, encoding="utf-8")
    os.chmod(cm, 0o000)
    tex_dir = root / "thesis" / "tex"; tex_dir.mkdir(parents=True)
    (tex_dir / "ch1.tex").write_text("x"); (tex_dir / "ch2.tex").write_text("x")
    try:
        issues = check_dissect.check(cm, tex_dir)
        assert issues and any("无法读取" in i or "read" in i.lower() or "权限" in i or "permission" in i.lower() for i in issues), \
               f"expected graceful perm issue, got: {issues}"
    except Exception as e:
        assert False, f"check() raised {type(e).__name__} on unreadable file — must be graceful"
    finally:
        os.chmod(cm, 0o644)  # restore so cleanup works
    print("test_graceful_on_unreadable_file: PASS")

if __name__ == "__main__":
    test_passes_on_settled()
    test_fails_on_missing_framework_instantiation()
    test_fails_on_empty_framework_instantiation()
    test_ch1_progression_in_none_ok()
    test_fails_on_non_ch1_missing_progression_in()
    test_last_chapter_progression_out_none_ok()
    test_fails_on_non_last_missing_progression_out()
    test_fails_on_status_pending()
    test_fails_on_status_stale()
    test_fails_on_missing_chapter_map()
    test_graceful_on_binary_file()
    test_fails_on_missing_tex_file()
    test_fails_on_missing_tex_file_field()
    test_passes_when_all_tex_files_exist()
    test_chapter_headers_with_trailing_title_accepted()
    test_graceful_on_unreadable_file()
    print("ALL TESTS PASS")
