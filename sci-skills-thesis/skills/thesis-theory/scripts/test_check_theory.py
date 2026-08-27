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

def test_fails_on_waived_with_overlap_entries():
    """waived-by-author + an Overlap entry → contradiction (mirror the waived+Shared test;
    taurus I1: this branch was load-bearing with zero coverage — deleting it let a waived
    map carrying Overlaps pass silently, because the dangling guard skips on empty
    shared_nums and the vacuous guard only arms under confirmed)."""
    bad = THEORY_MAP_WAIVED.replace("""extraction-outcome: waived-by-author
""", """extraction-outcome: waived-by-author

## Overlap 1
- shared-ref: Shared 1
- theory-§: §2.1
- chapter-ref: Chapter 1
- chapter-§: §3.2
- suggested-disposition: 章内留 brief recap
""")
    tm, cm, sp, tex_dir = _write_project(theory_map=bad)
    issues = check_theory.check(tm, cm, sp, tex_dir)
    assert any("waived" in i.lower() and "Overlap 1" in i for i in issues), \
           f"expected waived-with-overlap issue, got: {issues}"
    print("test_fails_on_waived_with_overlap_entries: PASS")

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
    assert any("grounded-in" in i and ("解析出" in i or "不同章" in i) for i in issues), \
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

def test_fails_on_missing_shared_ref():
    bad = THEORY_MAP_SETTLED.replace("- shared-ref: Shared 1\n", "")
    tm, cm, sp, tex_dir = _write_project(theory_map=bad)
    issues = check_theory.check(tm, cm, sp, tex_dir)
    assert any("shared-ref" in i and "Overlap 1" in i for i in issues), f"expected shared-ref issue, got: {issues}"
    print("test_fails_on_missing_shared_ref: PASS")

def test_fails_on_dangling_shared_ref():
    bad = THEORY_MAP_SETTLED.replace("- shared-ref: Shared 1", "- shared-ref: Shared 9")
    tm, cm, sp, tex_dir = _write_project(theory_map=bad)
    issues = check_theory.check(tm, cm, sp, tex_dir)
    assert any("Shared 9" in i and ("不在" in i or "悬空" in i) for i in issues), \
           f"expected dangling shared-ref issue, got: {issues}"
    print("test_fails_on_dangling_shared_ref: PASS")

def test_fails_on_malformed_shared_ref():
    bad = THEORY_MAP_SETTLED.replace("- shared-ref: Shared 1", "- shared-ref: 某个组件")
    tm, cm, sp, tex_dir = _write_project(theory_map=bad)
    issues = check_theory.check(tm, cm, sp, tex_dir)
    assert any("shared-ref" in i and "无法解析" in i for i in issues), \
           f"expected malformed shared-ref issue, got: {issues}"
    print("test_fails_on_malformed_shared_ref: PASS")

def test_fails_on_overlap_chapter_not_in_chapter_map():
    bad = THEORY_MAP_SETTLED.replace("- chapter-ref: Chapter 1", "- chapter-ref: Chapter 9")
    tm, cm, sp, tex_dir = _write_project(theory_map=bad)
    issues = check_theory.check(tm, cm, sp, tex_dir)
    assert any("Chapter 9" in i and ("不在" in i or "悬空" in i) for i in issues), \
           f"expected dangling chapter-ref issue, got: {issues}"
    print("test_fails_on_overlap_chapter_not_in_chapter_map: PASS")

def test_fails_on_empty_suggested_disposition():
    bad = THEORY_MAP_SETTLED.replace(
        "- suggested-disposition: 章内留 brief recap + cross-ref 第二章",
        "- suggested-disposition: none")
    tm, cm, sp, tex_dir = _write_project(theory_map=bad)
    issues = check_theory.check(tm, cm, sp, tex_dir)
    assert any("suggested-disposition" in i and "Overlap 1" in i for i in issues), \
           f"expected empty-disposition issue, got: {issues}"
    print("test_fails_on_empty_suggested_disposition: PASS")

def test_fails_on_missing_chapter_map():
    tm, cm, sp, tex_dir = _write_project()
    cm.unlink()
    issues = check_theory.check(tm, cm, sp, tex_dir)
    assert any("chapter-map" in i.lower() and "不存在" in i for i in issues), \
           f"expected missing-chapter-map issue, got: {issues}"
    print("test_fails_on_missing_chapter_map: PASS")

def test_fails_on_unreadable_chapter_map():
    tm, cm, sp, tex_dir = _write_project()
    cm.write_bytes(b"\xff\xfe\x00\x01garbage non-utf8")
    issues = check_theory.check(tm, cm, sp, tex_dir)
    assert any("不可读" in i and "cross-ref 跳过" in i for i in issues), \
           f"expected unreadable-chapter-map issue, got: {issues}"
    print("test_fails_on_unreadable_chapter_map: PASS")

def test_fails_on_chapter_map_without_entries():
    tm, cm, sp, tex_dir = _write_project(chapter_map="# chapter-map.md\n> 空 baton\n")
    issues = check_theory.check(tm, cm, sp, tex_dir)
    assert any("无任何 ## Chapter N 条目" in i for i in issues), \
           f"expected no-entries issue, got: {issues}"
    print("test_fails_on_chapter_map_without_entries: PASS")

def test_fails_on_missing_spine():
    """spine.md missing → theory's own hard dependency (unified framework skeleton)."""
    tm, cm, sp, tex_dir = _write_project()
    sp.unlink()
    issues = check_theory.check(tm, cm, sp, tex_dir)
    assert any("spine" in i.lower() and "不存在" in i for i in issues), \
           f"expected missing-spine issue, got: {issues}"
    print("test_fails_on_missing_spine: PASS")

def test_fails_on_unreadable_spine():
    tm, cm, sp, tex_dir = _write_project()
    sp.write_bytes(b"\xff\xfe\x00\x01garbage non-utf8")
    issues = check_theory.check(tm, cm, sp, tex_dir)
    assert any("不可读" in i and "spine 复验跳过" in i for i in issues), \
           f"expected unreadable-spine issue, got: {issues}"
    print("test_fails_on_unreadable_spine: PASS")

def test_fails_on_spine_pending_residue():
    """spine re-opened mid-write (`[pending?` marker) → theory-map may be stale —
    the T1 mid-write backtrack window this check exists to close."""
    reopened = SPINE_SETTLED.replace("## Main line (主线)\nX 主线串联各章",
                                     "## Main line (主线)\n[pending? ] 重新斟酌中的主线")
    tm, cm, sp, tex_dir = _write_project(spine=reopened)
    issues = check_theory.check(tm, cm, sp, tex_dir)
    assert any("[pending?" in i and ("重开" in i or "陈旧" in i) for i in issues), \
           f"expected spine-reopened issue, got: {issues}"
    print("test_fails_on_spine_pending_residue: PASS")

def test_fenced_shared_does_not_count():
    """A `## Shared 1` inside a ``` fence must NOT satisfy the confirmed-mode ≥1
    requirement → vacuous-pass guard must fire (pins fence-aware inheritance)."""
    fenced = THEORY_MAP_SETTLED.replace("""## Shared 1
- component: 统一热力学表征框架 T(x)
- grounded-in: [Chapter 1 §2 method, Chapter 2 §3 method]
- instantiates-framework: T(x) 是统一框架 F 的表征层实例化
- status: confirmed

## Shared 2
- component: 跨章实验设计协议 P
- grounded-in: [Chapter 1 §2 method, Chapter 2 §2 method]
- instantiates-framework: P 是 F 的实验验证层实例化
- status: confirmed""", """```
## Shared 1
- component: fenced fake
- grounded-in: [Chapter 1 §2, Chapter 2 §3]
- instantiates-framework: fenced
- status: confirmed
```""")
    tm, cm, sp, tex_dir = _write_project(theory_map=fenced)
    issues = check_theory.check(tm, cm, sp, tex_dir)
    assert any("Shared" in i and ("空" in i or "vacuous" in i.lower()) for i in issues), \
           f"fenced Shared must not count → vacuous guard must fire, got: {issues}"
    print("test_fenced_shared_does_not_count: PASS")

def test_hr_closes_field_window():
    """A standalone `---` hr closes the entry's field window (summary R1 lineage):
    fields after the hr belong to a foreign block and must not substitute the
    entry's own missing fields."""
    hr = THEORY_MAP_SETTLED.replace("""## Shared 1
- component: 统一热力学表征框架 T(x)""", """## Shared 1

---

- component: 统一热力学表征框架 T(x)""")
    tm, cm, sp, tex_dir = _write_project(theory_map=hr)
    issues = check_theory.check(tm, cm, sp, tex_dir)
    assert any("component" in i and "Shared 1" in i for i in issues), \
           f"hr must close the window → Shared 1 component must be missing, got: {issues}"
    print("test_hr_closes_field_window: PASS")

def test_foreign_block_fields_do_not_substitute():
    """A `## 备注` block carrying Shared-shaped fields after Shared 1 must NOT
    substitute Shared 1's own fields (summary B1 lineage: any-level header closes)."""
    foreign = THEORY_MAP_SETTLED.replace("""## Shared 1
- component: 统一热力学表征框架 T(x)
- grounded-in: [Chapter 1 §2 method, Chapter 2 §3 method]
- instantiates-framework: T(x) 是统一框架 F 的表征层实例化
- status: confirmed""", """## Shared 1

## 备注（编辑注记）
- component: 外来块的组件
- grounded-in: [Chapter 1 §2, Chapter 2 §3]
- instantiates-framework: 外来
- status: confirmed""")
    tm, cm, sp, tex_dir = _write_project(theory_map=foreign)
    issues = check_theory.check(tm, cm, sp, tex_dir)
    assert any("component" in i and "Shared 1" in i for i in issues), \
           f"foreign-block fields must not substitute, got: {issues}"
    print("test_foreign_block_fields_do_not_substitute: PASS")

def test_orphan_fence_diagnostic():
    """Odd number of ``` lines → explicit orphan-fence diagnostic (summary B4 lineage:
    fail-noisy, not a misleading absence issue)."""
    orphan = THEORY_MAP_SETTLED + "\n```\n## Shared 3\n- component: swallowed\n"
    tm, cm, sp, tex_dir = _write_project(theory_map=orphan)
    issues = check_theory.check(tm, cm, sp, tex_dir)
    assert any("未闭合 code fence" in i for i in issues), \
           f"expected orphan-fence diagnostic, got: {issues}"
    print("test_orphan_fence_diagnostic: PASS")

def test_ansi_sanitized_in_issue_output():
    """Field values echoed into issue lines must be ANSI/control-stripped
    (summary B5 lineage — no terminal title rewriting via forged log lines)."""
    ansi = THEORY_MAP_SETTLED.replace(
        "- grounded-in: [Chapter 1 §2 method, Chapter 2 §3 method]",
        "- grounded-in: [\x1b[31mChapter 1 §2\x1b[0m, Chapter 1 §4]")
    tm, cm, sp, tex_dir = _write_project(theory_map=ansi)
    issues = check_theory.check(tm, cm, sp, tex_dir)
    assert any("grounded-in" in i for i in issues), "expected the grounding issue to fire"
    assert not any("\x1b" in i for i in issues), f"ANSI escape leaked into issue output: {issues}"
    print("test_ansi_sanitized_in_issue_output: PASS")

def test_bad_theory_tex_value_graceful():
    """A theory-tex value that breaks stat (overlong name → OSError [Errno 36]) →
    graceful '值无法检验' issue, never a crash (summary aries B2 stat-fallback
    lineage). NOTE: the task text's fixture was an embedded NUL — on this Python
    (3.13) pathlib's is_file() swallows the ValueError internally (returns False),
    so a NUL value never reaches the stat-fallback branch and the test pinned
    nothing; the overlong name does raise (mirror test_check_summary.py
    test_graceful_on_overlong_synthesis_tex)."""
    bad = THEORY_MAP_SETTLED.replace("theory-tex: chapter1.tex", "theory-tex: " + "a"*5000)
    tm, cm, sp, tex_dir = _write_project(theory_map=bad)
    try:
        issues = check_theory.check(tm, cm, sp, tex_dir)
        assert any("无法检验" in i for i in issues), f"expected graceful value issue, got: {issues}"
    except Exception as e:
        assert False, f"check() raised {type(e).__name__} — must be graceful"
    print("test_bad_theory_tex_value_graceful: PASS")

def test_top_level_fields_ignore_fenced_examples():
    """A fenced example block (schema sample) above the real fields must not supply
    false values (taurus I2: leftmost re.search match on fence lines = false failures
    on legal maps)."""
    fenced_example = THEORY_MAP_SETTLED.replace(
        """theory-tex: chapter1.tex
extraction-outcome: confirmed""",
        """```
theory-tex: chapter9.tex
extraction-outcome: pending
```
theory-tex: chapter1.tex
extraction-outcome: confirmed""")
    tm, cm, sp, tex_dir = _write_project(theory_map=fenced_example)
    issues = check_theory.check(tm, cm, sp, tex_dir)
    assert issues == [], f"fenced example must not poison the real fields, got: {issues}"
    print("test_top_level_fields_ignore_fenced_examples: PASS")

def test_fenced_example_does_not_mask_missing_field():
    """Real extraction-outcome deleted, fenced example remains → the missing-field
    issue must fire (taurus I2 inverted variant: without fence-awareness the fence's
    'confirmed' satisfies the check and the map passes with the real field absent —
    a silent pass)."""
    bad = THEORY_MAP_SETTLED.replace("extraction-outcome: confirmed\n",
                                     "```\nextraction-outcome: confirmed\n```\n")
    tm, cm, sp, tex_dir = _write_project(theory_map=bad)
    issues = check_theory.check(tm, cm, sp, tex_dir)
    assert any("extraction-outcome" in i and "缺" in i for i in issues), \
           f"real field absent must be caught despite the fenced example, got: {issues}"
    print("test_fenced_example_does_not_mask_missing_field: PASS")

if __name__ == "__main__":
    # auto-discovery runner（taurus M4）：按名收集所有 test_* 函数——定义了却没被
    # 手动列表调用的 test 不可能存在（silent-never-runs 漂移类封死）。执行序 =
    # 字母序；每个 test 自建 project，与顺序无关。count 打印防 fixture 静默丢失。
    _tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for _t in _tests:
        _t()
    print(f"ALL TESTS PASS ({len(_tests)} tests)")
