"""stdlib tests for init_project.py — run: python3 test_init.py"""
import importlib.util, pathlib, sys, os
HERE = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("init_project", HERE / "init_project.py")
init_project = importlib.util.module_from_spec(spec)
spec.loader.exec_module(init_project)

def test_constants():
    # workspace name shared with article family (coexist in same sci-skills/)
    assert init_project.FAMILY_ROOT_NAME == "sci-skills"
    assert init_project.THESIS_DIR_NAME == "thesis"
    # only the skills that get their own output dir are pre-built
    assert init_project.BROTHER_SKILLS == [
        "thesis-dissect", "thesis-intro", "thesis-theory", "thesis-summary",
    ]
    # spine/polish/typeset/init have NO dir (they write top-level shared files
    # or edit tex in place); verify none of them leaked in
    assert "thesis-spine" not in init_project.BROTHER_SKILLS
    assert "thesis-polish" not in init_project.BROTHER_SKILLS
    # top-level shared files (thesis- prefixed to avoid article-family collision)
    assert "thesis-sources.md" in init_project.SHARED_FILES_PLACEHOLDERS
    assert "thesis-spine.md" in init_project.SHARED_FILES_PLACEHOLDERS
    assert "thesis-terminology-ledger.md" in init_project.SHARED_FILES_PLACEHOLDERS

if __name__ == "__main__":
    test_constants()
    print("test_constants: PASS")
