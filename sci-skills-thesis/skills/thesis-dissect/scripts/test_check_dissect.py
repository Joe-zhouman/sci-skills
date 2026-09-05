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

# 合规章 tex：章引（实质引文段）→ 模块（干什么的名词化标题）→ 本章讨论 → 本章小结
VALID_TEX = r"""\chapter{薄膜的工艺结晶关系研究}
本章要回答的问题是：哪些工艺参数主导了薄膜的结晶质量。
上一章的结果表明界面层是制约性能的瓶颈，由此把问题推进到本章；
围绕这个问题，本章沿两个模块展开：先回答合成侧的配比问题，再回答表征侧的生长问题，
最后把两块结果放在一起综合讨论，并给出本章的边界。
\section{薄膜的溶液法合成与生长}
本模块要回答的问题是：前驱体配比如何影响结晶质量。
采用溶液法合成……结果显示配比主导晶粒尺寸。
\section{本章讨论}
把各模块的结果放在一起看，机制上……与文献对比一致。
\section{本章小结}
本章回答了章引的问题：配比主导结晶质量；
这引出下一章的问题：界面层如何调控。
"""

# 合规 trace.md（SI 清单 + 讨论素材清单，去向均已落位、无 pending）
def _valid_trace(slug: str) -> str:
    return f"""# {slug} trace
## Claim & main line
- claim: {slug} 证明了配比主导结晶 / advances main line: 推进主线第一步
## IMRaD 地图
- intro → 提问题；methods → 合成与表征；results → 数据；discussion → 机制
## 章引素材
- intro 第二段：问题背景 + 为什么值得答
## SI 清单
- Fig. S1 XRD 表征 → 模块1
- Table S2 对照实验 → 本章讨论
## 讨论素材清单
- 机制解释一段 → 本章讨论
- 文献对比一段 → 本章讨论
"""

def _write_project(
    content: str,
    tex_files: dict[str, str] | None = None,
    traces: dict[str, str] | None = None,
    write_traces: bool = True,
) -> tuple[pathlib.Path, pathlib.Path]:
    """Build a temp project: chapter-map.md + thesis/tex/<files> + paper-X/trace.md.
    Defaults are fully COMPLIANT with the v2 contract (章形 + 零丢弃), so individual
    tests break exactly one thing. traces={slug: body} overrides a trace;
    write_traces=False skips traces entirely. Returns (cm_path, tex_dir)."""
    root = pathlib.Path(tempfile.mkdtemp())
    cm = root / "sci-skills" / "thesis-dissect" / "chapter-map.md"
    cm.parent.mkdir(parents=True)
    cm.write_text(content, encoding="utf-8")
    tex_dir = root / "thesis" / "tex"
    tex_dir.mkdir(parents=True)
    for name, body in (tex_files or {"ch1.tex": VALID_TEX, "ch2.tex": VALID_TEX}).items():
        (tex_dir / name).write_text(body, encoding="utf-8")
    if write_traces:
        for slug in ("paper-A", "paper-B"):
            body = _valid_trace(slug) if traces is None else traces.get(slug, _valid_trace(slug))
            if body is None:
                continue
            d = cm.parent / slug
            d.mkdir(parents=True, exist_ok=True)
            (d / "trace.md").write_text(body, encoding="utf-8")
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

def test_fails_on_absolute_tex_file_path():
    """aries #1: `tex-file: /etc/passwd` (absolute) must NOT pass — it's outside thesis/tex/.
    pathlib discards tex_dir when tf is absolute, defeating the gate."""
    import os
    # /etc/passwd exists on essentially all Linux; if somehow absent, use a known-existing abs path
    target = "/etc/passwd" if os.path.isfile("/etc/passwd") else os.path.abspath(__file__)
    bad = SETTLED.replace("- tex-file: ch1.tex\n", f"- tex-file: {target}\n")
    cm, tex_dir = _write_project(bad)  # tex_dir has ch1.tex + ch2.tex, but tf points at abs path
    issues = check_dissect.check(cm, tex_dir)
    assert any("tex-file" in i and ("绝对" in i or "absolute" in i.lower() or "thesis/tex" in i or "外" in i) for i in issues), \
           f"absolute tex-file path must fail (outside thesis/tex/), got: {issues}"
    print("test_fails_on_absolute_tex_file_path: PASS")

def test_fails_on_dotdot_tex_file_path():
    """aries #1: `tex-file: ../etc/passwd` traversal must NOT pass."""
    import os
    # _write_project puts tex_dir at root/thesis/tex; ../etc/passwd resolves to root/etc/passwd (likely absent),
    # so use a path that resolves to an existing file outside tex_dir: ../../<something>
    cm, tex_dir = _write_project(SETTLED)
    # craft a tf that traverses out to a file we know exists (the chapter-map.md itself, under sci-skills/thesis-dissect/)
    cm_path = cm
    # tex_dir = root/thesis/tex; cm is at root/sci-skills/thesis-dissect/chapter-map.md → ../../sci-skills/thesis-dissect/chapter-map.md
    bad = SETTLED.replace("- tex-file: ch1.tex\n", "- tex-file: ../../sci-skills/thesis-dissect/chapter-map.md\n")
    cm2, tex_dir2 = _write_project(bad)  # fresh project; the traversal target won't exist there → but absolute test above covers the core
    # Better: test that `..` in parts is rejected regardless of existence
    issues = check_dissect.check(cm2, tex_dir2)
    assert any("tex-file" in i and (".." in i or "外" in i or "traversal" in i.lower() or "thesis/tex" in i) for i in issues), \
           f"`..` traversal tex-file must fail, got: {issues}"
    print("test_fails_on_dotdot_tex_file_path: PASS")

def test_ignores_chapter_headers_inside_code_fence():
    """aries #2: a `## Chapter 99` line inside a ``` block must NOT be parsed as a real chapter."""
    bad = SETTLED + "\n```\n## Chapter 99\n- this is inside a code block\n```\n"
    cm, tex_dir = _write_project(bad)
    issues = check_dissect.check(cm, tex_dir)
    # Chapter 99 is phantom; must not appear in issues, must not shift ch1/ch2 semantics
    assert not any("Chapter 99" in i for i in issues), f"phantom Chapter 99 leaked: {issues}"
    # the real 2 chapters should still pass
    assert issues == [], f"expected pass (2 real chapters, phantom ignored), got: {issues}"
    print("test_ignores_chapter_headers_inside_code_fence: PASS")

# --- v2 防缺席层（章形 + 零丢弃）——本 skill 用户实测三缺陷的机械防线 ---

def test_passes_on_compliant_shape():
    """v2 合规 fixture（章形齐 + trace 清单去向落位）整体 pass——负向用例的基线。"""
    cm, tex_dir = _write_project(SETTLED)
    issues = check_dissect.check(cm, tex_dir)
    assert issues == [], f"expected pass on compliant fixture, got: {issues}"
    print("test_passes_on_compliant_shape: PASS")

def test_fails_on_imrad_section_titles():
    """\\section{方法}+\\section{结果} = 机械拆分 Methods/Results 的 IMRaD 形态 → 必须拦。"""
    imrad_tex = r"""\chapter{替代章}
\section{方法}
做了 A。
\section{结果}
显示了 B。
"""
    cm, tex_dir = _write_project(SETTLED, tex_files={"ch1.tex": imrad_tex, "ch2.tex": VALID_TEX})
    issues = check_dissect.check(cm, tex_dir)
    assert any("IMRaD" in i and "方法" in i for i in issues), f"expected IMRaD issue for 方法, got: {issues}"
    assert any("IMRaD" in i and "结果" in i for i in issues), f"expected IMRaD issue for 结果, got: {issues}"
    print("test_fails_on_imrad_section_titles: PASS")

def test_imrad_check_not_hit_module_titles():
    """整标题等值匹配（非包含）——'XX 的合成与表征'类模块标题不误伤。"""
    cm, tex_dir = _write_project(SETTLED)
    issues = check_dissect.check(cm, tex_dir)
    assert not any("IMRaD" in i for i in issues), f"module title false positive: {issues}"
    print("test_imrad_check_not_hit_module_titles: PASS")

def test_fails_on_missing_trace():
    """paper 的 trace.md 缺失 → 素材未清点，零丢弃无法审计。"""
    cm, tex_dir = _write_project(SETTLED, traces={"paper-A": None})
    issues = check_dissect.check(cm, tex_dir)
    assert any("trace.md" in i and "paper-A" in i for i in issues), \
           f"expected trace-missing issue, got: {issues}"
    print("test_fails_on_missing_trace: PASS")

def test_fails_on_trace_pending_destination():
    """清单条目去向仍为 pending → 章收尾后不允许残留（未落位）。"""
    bad_trace = _valid_trace("paper-A").replace("- Fig. S1 XRD 表征 → 模块1",
                                                "- Fig. S1 XRD 表征 → pending")
    cm, tex_dir = _write_project(SETTLED, traces={"paper-A": bad_trace})
    issues = check_dissect.check(cm, tex_dir)
    assert any("pending" in i and "SI 清单" in i for i in issues), \
           f"expected pending issue, got: {issues}"
    print("test_fails_on_trace_pending_destination: PASS")

def test_fails_on_trace_item_without_destination():
    """清单条目缺去向箭头 → 未落位。"""
    bad_trace = _valid_trace("paper-A").replace("- 机制解释一段 → 本章讨论", "- 机制解释一段")
    cm, tex_dir = _write_project(SETTLED, traces={"paper-A": bad_trace})
    issues = check_dissect.check(cm, tex_dir)
    assert any("讨论素材清单" in i and "缺去向" in i for i in issues), \
           f"expected no-destination issue, got: {issues}"
    print("test_fails_on_trace_item_without_destination: PASS")

def test_passes_with_no_si_declaration():
    """无 SI 的论文：显式'无 SI'声明替代清单 → pass（不是每篇论文都有 SI）。"""
    trace = _valid_trace("paper-A").replace(
        "## SI 清单\n- Fig. S1 XRD 表征 → 模块1\n- Table S2 对照实验 → 本章讨论\n", "无 SI\n")
    cm, tex_dir = _write_project(SETTLED, traces={"paper-A": trace})
    issues = check_dissect.check(cm, tex_dir)
    assert not any("SI" in i and "paper-A" in i for i in issues), \
           f"'无 SI' declaration must pass: {issues}"
    print("test_passes_with_no_si_declaration: PASS")

def test_fails_on_missing_si_section_and_declaration():
    """trace 既无 SI 清单节也无'无 SI'声明 → 拦。"""
    trace = _valid_trace("paper-A").replace(
        "## SI 清单\n- Fig. S1 XRD 表征 → 模块1\n- Table S2 对照实验 → 本章讨论\n", "")
    cm, tex_dir = _write_project(SETTLED, traces={"paper-A": trace})
    issues = check_dissect.check(cm, tex_dir)
    assert any("SI 清单" in i and "paper-A" in i for i in issues), \
           f"expected missing-SI-section issue, got: {issues}"
    print("test_fails_on_missing_si_section_and_declaration: PASS")

def test_fails_on_missing_discussion_section():
    """缺'本章讨论'节 → discussion 精髓丢失，必须拦。"""
    no_disc = VALID_TEX.replace(
        r"\section{本章讨论}" + "\n把各模块的结果放在一起看，机制上……与文献对比一致。\n", "")
    cm, tex_dir = _write_project(SETTLED, tex_files={"ch1.tex": no_disc, "ch2.tex": VALID_TEX})
    issues = check_dissect.check(cm, tex_dir)
    assert any("本章讨论" in i for i in issues), f"expected missing-discussion issue, got: {issues}"
    print("test_fails_on_missing_discussion_section: PASS")

def test_fails_on_missing_xiaojie_last_section():
    """末节不是'本章小结' → 拦（收束章问题+递进缺失）。"""
    no_xj = VALID_TEX.replace(
        r"\section{本章小结}" + "\n本章回答了章引的问题：配比主导结晶质量；\n这引出下一章的问题：界面层如何调控。\n", "")
    cm, tex_dir = _write_project(SETTLED, tex_files={"ch1.tex": no_xj, "ch2.tex": VALID_TEX})
    issues = check_dissect.check(cm, tex_dir)
    assert any("本章小结" in i and "Chapter 1" in i for i in issues), \
           f"expected missing-xiaojie issue, got: {issues}"
    print("test_fails_on_missing_xiaojie_last_section: PASS")

def test_fails_on_missing_chapter_intro():
    """\\chapter 直跳 \\section（无章引段、首节非'引言'）→ 拦（提问题缺失）。"""
    no_intro = r"""\chapter{薄膜的工艺结晶关系研究}
\section{薄膜的溶液法合成与生长}
本模块要回答的问题是：前驱体配比如何影响结晶质量。
\section{本章讨论}
讨论内容。
\section{本章小结}
小结内容。
"""
    cm, tex_dir = _write_project(SETTLED, tex_files={"ch1.tex": no_intro, "ch2.tex": VALID_TEX})
    issues = check_dissect.check(cm, tex_dir)
    assert any("章引" in i and "Chapter 1" in i for i in issues), \
           f"expected missing-intro issue, got: {issues}"
    print("test_fails_on_missing_chapter_intro: PASS")

def test_chapter_intro_via_yinyan_section_ok():
    """模板用 \\section{引言} 开章 → 视为有章引，不拦（章引等价节名逃逸口径）。"""
    yinyan = r"""\chapter{薄膜的工艺结晶关系研究}
\section{引言}
本章要回答的问题是：哪些工艺参数主导了薄膜的结晶质量。
\section{薄膜的溶液法合成与生长}
本模块要回答的问题是：前驱体配比如何影响结晶质量。
\section{本章讨论}
讨论内容。
\section{本章小结}
小结内容。
"""
    cm, tex_dir = _write_project(SETTLED, tex_files={"ch1.tex": yinyan, "ch2.tex": VALID_TEX})
    issues = check_dissect.check(cm, tex_dir)
    assert not any("章引" in i and "Chapter 1" in i for i in issues), \
           f"'引言' section must satisfy the intro check: {issues}"
    print("test_chapter_intro_via_yinyan_section_ok: PASS")

def test_trace_checked_once_for_merged_papers():
    """非 1:1：同一 paper 出现在两章 → trace 只查一次（issue 不重复计数）。"""
    merged = SETTLED.replace("- papers: [paper-B]", "- papers: [paper-A]")
    cm, tex_dir = _write_project(merged, traces={"paper-A": None})
    issues = check_dissect.check(cm, tex_dir)
    hits = [i for i in issues if "trace.md" in i and "paper-A" in i]
    assert len(hits) == 1, f"paper-A trace issue should be reported once, got: {hits}"
    print("test_trace_checked_once_for_merged_papers: PASS")

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
    test_fails_on_absolute_tex_file_path()
    test_fails_on_dotdot_tex_file_path()
    test_ignores_chapter_headers_inside_code_fence()
    test_passes_on_compliant_shape()
    test_fails_on_imrad_section_titles()
    test_imrad_check_not_hit_module_titles()
    test_fails_on_missing_trace()
    test_fails_on_trace_pending_destination()
    test_fails_on_trace_item_without_destination()
    test_passes_with_no_si_declaration()
    test_fails_on_missing_si_section_and_declaration()
    test_fails_on_missing_discussion_section()
    test_fails_on_missing_xiaojie_last_section()
    test_fails_on_missing_chapter_intro()
    test_chapter_intro_via_yinyan_section_ok()
    test_trace_checked_once_for_merged_papers()
    print("ALL TESTS PASS")
