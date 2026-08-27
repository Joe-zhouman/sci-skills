"""stdlib tests for check_theory.py — run: python3 test_check_theory.py

check_theory.py is a NEAR-TRIVIAL CONSISTENCY gate (not depth, not a post-polish
invariant — write-time check). Shared confirmed-footprint + extraction-outcome
waived-by-author terminal are the genuinely-new content; the Overlap 段 is the
author's manual-resolution checklist (resolver = the AUTHOR, never enforced).
The gate catches: 缺席 (theory-map.md missing / confirmed-but-empty Shared 段 —
vacuous pass guard), 官僚 lapse (fabricated Shared/chapter refs / dangling
grounded-in / pending residue / missing theory-tex file / spine re-opened
mid-write). It does NOT catch depth (forced/trivial commonality past the author
gate), fabricated § locations, or overlap coverage completeness (absent entries
— write-then-record discipline + eval territory).
"""
import atexit, codecs, importlib.util, pathlib, shutil, sys, tempfile
HERE = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("check_theory", HERE / "check_theory.py")
check_theory = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_theory)

# --- tmpdir cleanup (mirror summary aries B6): mkdtemp roots registered + rmtree'd at exit ---
_ROOTS: list[pathlib.Path] = []
def _new_root() -> pathlib.Path:
    d = pathlib.Path(tempfile.mkdtemp())
    _ROOTS.append(d)
    return d
atexit.register(lambda: [shutil.rmtree(d, ignore_errors=True) for d in _ROOTS])

# --- fixtures ---
# A settled theory-map.md (confirmed mode: 2 Shared + 1 Overlap) + the chapter-map.md
# it cross-references + a settled spine.md + chapter1.tex (the theory tex, init-reserved slot).
THEORY_MAP_SETTLED = """# theory-map.md
> theory 写后 baton (DATA).

theory-tex: chapter1.tex
extraction-outcome: confirmed

## Shared 1
- component: 统一热力学表征框架 T(x)
- grounded-in: [Chapter 1 §2 method, Chapter 2 §3 method]
- instantiates-framework: T(x) 是统一框架 F 的表征层实例化
- status: confirmed

## Shared 2
- component: 跨章实验设计协议 P
- grounded-in: [Chapter 1 §2 method, Chapter 2 §2 method]
- instantiates-framework: P 是 F 的实验验证层实例化
- status: confirmed

## Overlap 1
- shared-ref: Shared 1
- theory-§: §2.1
- chapter-ref: Chapter 1
- chapter-§: §3.2
- suggested-disposition: 章内留 brief recap + cross-ref 第二章
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

SPINE_SETTLED = """# thesis-spine.md
> Baton. Settled by the author.

## Main line (主线)
X 主线串联各章

## Unified framework (统一框架)
框架 F：每章以 F 的一个实例化统一

## Inter-chapter progression (章间递进)
- role 1: question = …; advances the main line by …

## Thesis-level claim (umbrella)
本论文建立 X。

## Boundary
不 establish Y。
"""

THEORY_MAP_WAIVED = """# theory-map.md
> theory 写后 baton (DATA).

theory-tex: chapter1.tex
extraction-outcome: waived-by-author
"""


def _write_project(theory_map: str = THEORY_MAP_SETTLED,
                   chapter_map: str = CHAPTER_MAP_SETTLED,
                   spine: str = SPINE_SETTLED,
                   theory_tex_name: str = "chapter1.tex") -> tuple[pathlib.Path, pathlib.Path, pathlib.Path, pathlib.Path]:
    """Build a temp project: theory-map.md + chapter-map.md + thesis-spine.md +
    thesis/tex/<theory-tex>. Returns (tm, cm, sp, tex_dir)."""
    root = _new_root()
    tm = root / "sci-skills" / "thesis-theory" / "theory-map.md"
    tm.parent.mkdir(parents=True)
    tm.write_text(theory_map, encoding="utf-8")
    cm = root / "sci-skills" / "thesis-dissect" / "chapter-map.md"
    cm.parent.mkdir(parents=True)
    cm.write_text(chapter_map, encoding="utf-8")
    sp = root / "sci-skills" / "thesis-spine.md"
    sp.write_text(spine, encoding="utf-8")
    tex_dir = root / "thesis" / "tex"
    tex_dir.mkdir(parents=True)
    (tex_dir / theory_tex_name).write_text("\\chapter{共用理论方法}", encoding="utf-8")
    return tm, cm, sp, tex_dir


def test_passes_on_settled():
    tm, cm, sp, tex_dir = _write_project()
    issues = check_theory.check(tm, cm, sp, tex_dir)
    assert issues == [], f"expected pass, got: {issues}"
    print("test_passes_on_settled: PASS")

def test_passes_on_waived_terminal():
    """waived-by-author + empty Shared/Overlap + theory-tex present = LEGAL terminal
    (the author's 裁最小章 footprint — NOT a vacuous pass; spec §Step 1 fallback / T3)."""
    tm, cm, sp, tex_dir = _write_project(theory_map=THEORY_MAP_WAIVED)
    issues = check_theory.check(tm, cm, sp, tex_dir)
    assert issues == [], f"expected waived terminal to pass, got: {issues}"
    print("test_passes_on_waived_terminal: PASS")

def test_fails_on_missing_extraction_outcome():
    bad = THEORY_MAP_SETTLED.replace("extraction-outcome: confirmed\n", "")
    tm, cm, sp, tex_dir = _write_project(theory_map=bad)
    issues = check_theory.check(tm, cm, sp, tex_dir)
    assert any("extraction-outcome" in i for i in issues), f"expected missing-outcome issue, got: {issues}"
    print("test_fails_on_missing_extraction_outcome: PASS")

def test_fails_on_invalid_extraction_outcome():
    bad = THEORY_MAP_SETTLED.replace("extraction-outcome: confirmed", "extraction-outcome: maybe")
    tm, cm, sp, tex_dir = _write_project(theory_map=bad)
    issues = check_theory.check(tm, cm, sp, tex_dir)
    assert any("extraction-outcome" in i and "maybe" in i for i in issues), f"expected invalid-outcome issue, got: {issues}"
    print("test_fails_on_invalid_extraction_outcome: PASS")

def test_fails_on_confirmed_vacuous_shared():
    """extraction-outcome=confirmed but Shared 段 empty → vacuous-pass guard (T3):
    either ≥1 confirmed component or the waived-by-author terminal — no silent third state."""
    bad = THEORY_MAP_SETTLED.replace("""## Shared 1
- component: 统一热力学表征框架 T(x)
- grounded-in: [Chapter 1 §2 method, Chapter 2 §3 method]
- instantiates-framework: T(x) 是统一框架 F 的表征层实例化
- status: confirmed

## Shared 2
- component: 跨章实验设计协议 P
- grounded-in: [Chapter 1 §2 method, Chapter 2 §2 method]
- instantiates-framework: P 是 F 的实验验证层实例化
- status: confirmed

## Overlap 1
- shared-ref: Shared 1
- theory-§: §2.1
- chapter-ref: Chapter 1
- chapter-§: §3.2
- suggested-disposition: 章内留 brief recap + cross-ref 第二章
""", "")
    tm, cm, sp, tex_dir = _write_project(theory_map=bad)
    issues = check_theory.check(tm, cm, sp, tex_dir)
    assert any("Shared" in i and ("空" in i or "vacuous" in i.lower()) for i in issues), \
           f"expected vacuous-pass guard issue, got: {issues}"
    print("test_fails_on_confirmed_vacuous_shared: PASS")

def test_fails_on_waived_with_shared_entries():
    """waived-by-author + a Shared entry → contradiction: waived = 裁最小章 (no components)."""
    bad = THEORY_MAP_WAIVED.replace("""extraction-outcome: waived-by-author
""", """extraction-outcome: waived-by-author

## Shared 1
- component: 统一热力学表征框架 T(x)
- grounded-in: [Chapter 1 §2 method, Chapter 2 §3 method]
- instantiates-framework: T(x) 是统一框架 F 的表征层实例化
- status: confirmed
""")
    tm, cm, sp, tex_dir = _write_project(theory_map=bad)
    issues = check_theory.check(tm, cm, sp, tex_dir)
    assert any("waived" in i.lower() and "Shared 1" in i for i in issues), \
           f"expected waived-with-entries issue, got: {issues}"
    print("test_fails_on_waived_with_shared_entries: PASS")

def test_fails_on_missing_component():
    bad = THEORY_MAP_SETTLED.replace("- component: 统一热力学表征框架 T(x)\n", "")
    tm, cm, sp, tex_dir = _write_project(theory_map=bad)
    issues = check_theory.check(tm, cm, sp, tex_dir)
    assert any("component" in i and "Shared 1" in i for i in issues), f"expected component issue, got: {issues}"
    print("test_fails_on_missing_component: PASS")

def test_fails_on_empty_instantiates_framework():
    bad = THEORY_MAP_SETTLED.replace(
        "- instantiates-framework: T(x) 是统一框架 F 的表征层实例化",
        "- instantiates-framework: none")
    tm, cm, sp, tex_dir = _write_project(theory_map=bad)
    issues = check_theory.check(tm, cm, sp, tex_dir)
    assert any("instantiates-framework" in i and "Shared 1" in i for i in issues), \
           f"expected instantiates-framework issue, got: {issues}"
    print("test_fails_on_empty_instantiates_framework: PASS")

def test_fails_on_shared_status_pending():
    """status=pending = AI candidate not author-settled → fail (never auto-adopted)."""
    bad = THEORY_MAP_SETTLED.replace("- status: confirmed\n\n## Shared 2", "- status: pending\n\n## Shared 2")
    tm, cm, sp, tex_dir = _write_project(theory_map=bad)
    issues = check_theory.check(tm, cm, sp, tex_dir)
    assert any("status" in i and "Shared 1" in i for i in issues), f"expected pending-status issue, got: {issues}"
    print("test_fails_on_shared_status_pending: PASS")

def test_fails_on_grounding_single_chapter():
    """grounded-in resolving to <2 distinct chapters → not a shared component → issue."""
    bad = THEORY_MAP_SETTLED.replace(
        "- grounded-in: [Chapter 1 §2 method, Chapter 2 §3 method]",
        "- grounded-in: [Chapter 1 §2 method, Chapter 1 §4 method]")
    tm, cm, sp, tex_dir = _write_project(theory_map=bad)
    issues = check_theory.check(tm, cm, sp, tex_dir)
    assert any("grounded-in" in i and ("2" in i or "两" in i) for i in issues), \
           f"expected single-chapter grounding issue, got: {issues}"
    print("test_fails_on_grounding_single_chapter: PASS")

def test_fails_on_dangling_grounded_in():
    bad = THEORY_MAP_SETTLED.replace(
        "- grounded-in: [Chapter 1 §2 method, Chapter 2 §3 method]",
        "- grounded-in: [Chapter 1 §2 method, Chapter 9 §3 method]")
    tm, cm, sp, tex_dir = _write_project(theory_map=bad)
    issues = check_theory.check(tm, cm, sp, tex_dir)
    assert any("Chapter 9" in i and ("不在" in i or "悬空" in i) for i in issues), \
           f"expected dangling grounded-in issue, got: {issues}"
    print("test_fails_on_dangling_grounded_in: PASS")

def test_fails_on_missing_theory_map():
    tm, cm, sp, tex_dir = _write_project()
    tm.unlink()
    issues = check_theory.check(tm, cm, sp, tex_dir)
    assert any("不存在" in i for i in issues), f"expected missing-theory-map issue, got: {issues}"
    print("test_fails_on_missing_theory_map: PASS")

def test_graceful_on_binary_theory_map():
    tm, cm, sp, tex_dir = _write_project()
    tm.write_bytes(b"\xff\xfe\x00\x01garbage non-utf8")
    try:
        issues = check_theory.check(tm, cm, sp, tex_dir)
        assert issues and any("UTF-8" in i or "二进制" in i for i in issues), f"expected graceful, got: {issues}"
    except Exception as e:
        assert False, f"check() raised {type(e).__name__} — must be graceful"
    print("test_graceful_on_binary_theory_map: PASS")

def test_ignores_utf8_bom_in_theory_map():
    """A UTF-8 BOM must not drop the first Shared entry (mirror summary aries B-lineage).
    The BOM-prefixed Shared 1 carries a dangling grounded-in Chapter 9 (with Chapter 1
    also present so the ≥2-distinct floor PASSES and the dangling branch is what fires
    — aquarius A2: single-chapter grounding would short-circuit at the <2 message
    instead of the dangling message)."""
    root = _new_root()
    tm = root / "sci-skills" / "thesis-theory" / "theory-map.md"
    tm.parent.mkdir(parents=True)
    # NOTE: non-ASCII `§` can't live in a bytes literal — same content via .encode()
    tm.write_bytes(codecs.BOM_UTF8
                   + "## Shared 1\n- component: x\n- grounded-in: [Chapter 1 §2, Chapter 9 §3]\n".encode("utf-8")
                   + b"- instantiates-framework: y\n- status: confirmed\n")
    cm = root / "sci-skills" / "thesis-dissect" / "chapter-map.md"
    cm.parent.mkdir(parents=True)
    cm.write_text(CHAPTER_MAP_SETTLED, encoding="utf-8")
    sp = root / "sci-skills" / "thesis-spine.md"
    sp.write_text(SPINE_SETTLED, encoding="utf-8")
    tex_dir = root / "thesis" / "tex"
    tex_dir.mkdir(parents=True)
    (tex_dir / "chapter1.tex").write_text("x", encoding="utf-8")
    issues = check_theory.check(tm, cm, sp, tex_dir)
    assert any("Chapter 9" in i for i in issues), f"BOM stripped → dangling Chapter 9 must be caught, got: {issues}"
    print("test_ignores_utf8_bom_in_theory_map: PASS")

def test_accepts_entry_headers_with_trailing_title():
    titled = THEORY_MAP_SETTLED.replace("## Shared 1\n", "## Shared 1 (热力学基础)\n")
    tm, cm, sp, tex_dir = _write_project(theory_map=titled)
    issues = check_theory.check(tm, cm, sp, tex_dir)
    assert issues == [], f"trailing-title header should parse: {issues}"
    print("test_accepts_entry_headers_with_trailing_title: PASS")

def test_fails_on_missing_theory_tex_field():
    # NOTE: fixture has `extraction-outcome` between theory-tex and ## Shared 1 —
    # the task's original pattern ("theory-tex: ...\n\n## Shared 1") never matched
    # (no-op replace); remove the field line itself instead.
    bad = THEORY_MAP_SETTLED.replace("theory-tex: chapter1.tex\n", "")
    tm, cm, sp, tex_dir = _write_project(theory_map=bad)
    issues = check_theory.check(tm, cm, sp, tex_dir)
    assert any("theory-tex" in i for i in issues), f"expected missing-theory-tex-field issue, got: {issues}"
    print("test_fails_on_missing_theory_tex_field: PASS")

def test_fails_on_missing_theory_tex_file():
    tm, cm, sp, tex_dir = _write_project()
    (tex_dir / "chapter1.tex").unlink()
    issues = check_theory.check(tm, cm, sp, tex_dir)
    assert any("chapter1.tex" in i and "不存在" in i for i in issues), \
           f"expected missing-theory-tex-file issue, got: {issues}"
    print("test_fails_on_missing_theory_tex_file: PASS")

def test_fails_on_theory_tex_path_traversal():
    """theory-tex is file-content-derived (untrusted) — must not escape thesis/tex/
    (mirror summary/intro path guard)."""
    bad_abs = THEORY_MAP_SETTLED.replace("theory-tex: chapter1.tex", "theory-tex: /etc/passwd")
    tm, cm, sp, tex_dir = _write_project(theory_map=bad_abs)
    issues = check_theory.check(tm, cm, sp, tex_dir)
    assert any("theory-tex" in i and ("之外" in i or "绝对" in i or "traversal" in i.lower()) for i in issues), \
           f"absolute theory-tex must be rejected, got: {issues}"
    bad_rel = THEORY_MAP_SETTLED.replace("theory-tex: chapter1.tex", "theory-tex: ../../../etc/passwd")
    tm, cm, sp, tex_dir = _write_project(theory_map=bad_rel)
    issues = check_theory.check(tm, cm, sp, tex_dir)
    assert any("theory-tex" in i and ("之外" in i or "traversal" in i.lower() or ".." in i) for i in issues), \
           f"`..` traversal theory-tex must be rejected, got: {issues}"
    print("test_fails_on_theory_tex_path_traversal: PASS")

if __name__ == "__main__":
    test_passes_on_settled()
    test_passes_on_waived_terminal()
    test_fails_on_missing_extraction_outcome()
    test_fails_on_invalid_extraction_outcome()
    test_fails_on_confirmed_vacuous_shared()
    test_fails_on_waived_with_shared_entries()
    test_fails_on_missing_component()
    test_fails_on_empty_instantiates_framework()
    test_fails_on_shared_status_pending()
    test_fails_on_grounding_single_chapter()
    test_fails_on_dangling_grounded_in()
    test_fails_on_missing_theory_map()
    test_graceful_on_binary_theory_map()
    test_ignores_utf8_bom_in_theory_map()
    test_accepts_entry_headers_with_trailing_title()
    test_fails_on_missing_theory_tex_field()
    test_fails_on_missing_theory_tex_file()
    test_fails_on_theory_tex_path_traversal()
    print("ALL TESTS PASS")
