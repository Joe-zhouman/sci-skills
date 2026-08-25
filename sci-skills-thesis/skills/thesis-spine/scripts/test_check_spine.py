"""stdlib tests for check_spine.py — run: python3 test_check_spine.py"""
import importlib.util, pathlib, sys, tempfile, os
HERE = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("check_spine", HERE / "check_spine.py")
check_spine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_spine)

# --- fixtures ---
SETTLED = """# thesis-spine.md
> Baton. `pending` = AI candidate, NOT author-adopted.

## Main line (主线)
N 篇小论文统一于 X 框架，共同贡献了 Y。

## Unified framework (统一框架)
the X framework
per-paper: how paper-A instantiates it = 侧视角1
per-paper: how paper-B instantiates it = 侧视角2

## Inter-chapter progression (章间递进)
ordered:
- role 1: question = X 怎么起作用?; advances the main line by 建立 baseline
- role 2: question = X 在 B 条件下?; advances the main line by 拓展 boundary

## Thesis-level claim (umbrella)
本 thesis establish 了 Y（三结构字段 collectively argue 它）。

## Boundary
本 thesis 不 establish Z。

## Intake (per-paper evidence base)
- paper-A: claim = …; structure = IMRaD; how it could fit a main line = 侧视角1
- paper-B: claim = …; structure = IMRaD; how it could fit a main line = 侧视角2

## Cracks flagged (tension-flagging, §⑤)
- [stage 1 / main line] (a) tension: … (b) evidence: … (c) question: …?
  disposition: [dismissed → reason: …]

## Alternatives considered
- main line: considered <alt>, rejected because <reason>
"""

def _write_fixture(content: str) -> pathlib.Path:
    p = pathlib.Path(tempfile.mkdtemp()) / "thesis-spine.md"
    p.write_text(content, encoding="utf-8")
    return p

def test_passes_on_settled_spine():
    issues = check_spine.check(_write_fixture(SETTLED))
    assert issues == [], f"expected pass, got: {issues}"
    print("test_passes_on_settled_spine: PASS")

def test_fails_on_pending_marker():
    bad = SETTLED.replace("## Main line (主线)\nN 篇",
                          "## Main line (主线)\n[pending? ] N 篇")
    issues = check_spine.check(_write_fixture(bad))
    assert any("pending" in i.lower() for i in issues), f"expected pending issue, got: {issues}"
    print("test_fails_on_pending_marker: PASS")

def test_fails_on_empty_structural_field():
    bad = SETTLED.replace("## Main line (主线)\nN 篇小论文统一于 X 框架，共同贡献了 Y。",
                          "## Main line (主线)\n")
    issues = check_spine.check(_write_fixture(bad))
    assert any("main line" in i.lower() and ("空" in i or "empt" in i.lower()) for i in issues), \
           f"expected empty-main-line issue, got: {issues}"
    print("test_fails_on_empty_structural_field: PASS")

def test_fails_on_missing_structural_section():
    bad = SETTLED.replace("## Unified framework (统一框架)\nthe X framework\nper-paper: how paper-A instantiates it = 侧视角1\nper-paper: how paper-B instantiates it = 侧视角2\n",
                          "")
    issues = check_spine.check(_write_fixture(bad))
    assert any("unified framework" in i.lower() for i in issues), f"expected missing-section issue, got: {issues}"
    print("test_fails_on_missing_structural_section: PASS")

def test_ignores_umbrella_and_boundary():
    """Load-bearing: an EMPTY umbrella + EMPTY boundary still passes coverage —
    they are depth (human-gated), NOT coverage. check_spine must not check them."""
    bad = SETTLED.replace("## Thesis-level claim (umbrella)\n本 thesis establish 了 Y（三结构字段 collectively argue 它）。",
                          "## Thesis-level claim (umbrella)\n")  # empty umbrella
    bad = bad.replace("## Boundary\n本 thesis 不 establish Z。",
                      "## Boundary\n")  # empty boundary
    issues = check_spine.check(_write_fixture(bad))
    assert issues == [], f"empty umbrella/boundary must NOT fail coverage (they're depth): {issues}"
    print("test_ignores_umbrella_and_boundary: PASS")

def test_fails_on_missing_per_paper_instantiation():
    """Intake 列了 paper-B 但 Unified framework 无其实例化 → contract gap。"""
    bad = SETTLED.replace("per-paper: how paper-B instantiates it = 侧视角2\n",
                          "")  # paper-B instantiation gone, but still in Intake
    issues = check_spine.check(_write_fixture(bad))
    assert any("paper-B" in i for i in issues), f"expected missing-instantiation issue for paper-B, got: {issues}"
    print("test_fails_on_missing_per_paper_instantiation: PASS")

def test_fails_on_role_missing_advance():
    """progression role 缺 advance → coverage 问题。"""
    bad = SETTLED.replace("advances the main line by 拓展 boundary",
                          "")  # role 2 now has question but no advance
    issues = check_spine.check(_write_fixture(bad))
    assert any("advance" in i.lower() for i in issues), f"expected missing-advance issue, got: {issues}"
    print("test_fails_on_role_missing_advance: PASS")

def test_fails_on_role_missing_question():
    """progression role 缺 question → coverage 问题。"""
    bad = SETTLED.replace("question = X 怎么起作用?;", "")
    issues = check_spine.check(_write_fixture(bad))
    assert any("question" in i.lower() for i in issues), f"expected missing-question issue, got: {issues}"
    print("test_fails_on_role_missing_question: PASS")

if __name__ == "__main__":
    test_passes_on_settled_spine()
    test_fails_on_pending_marker()
    test_fails_on_empty_structural_field()
    test_fails_on_missing_structural_section()
    test_ignores_umbrella_and_boundary()
    test_fails_on_missing_per_paper_instantiation()
    test_fails_on_role_missing_advance()
    test_fails_on_role_missing_question()
    print("ALL TESTS PASS")
