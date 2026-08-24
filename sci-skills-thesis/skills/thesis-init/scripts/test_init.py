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

import tempfile, shutil

def test_init_builds_skeleton():
    cwd = pathlib.Path(tempfile.mkdtemp())
    orig = pathlib.Path.cwd()
    os.chdir(cwd)
    try:
        rc = init_project.main(["init", "--no-git"])
        assert rc == 0
        # thesis/ first-class artifact — CONTRACT.md MUST be written (the bug aquarius caught)
        assert (cwd / "thesis" / "CONTRACT.md").is_file(), "thesis/CONTRACT.md not written"
        assert (cwd / "thesis" / "tex").is_dir()
        assert (cwd / "thesis" / ".gitignore").is_file(), "thesis/.gitignore not written"
        # shared workspace + thesis- prefixed shared files
        fam = cwd / "sci-skills"
        assert fam.is_dir()
        assert (fam / "thesis-sources.md").is_file()
        assert (fam / "thesis-spine.md").is_file()
        assert (fam / "thesis-terminology-ledger.md").is_file()
        # thesis-README.md (thesis-owned routing table; NOT README.md, which the article
        # family may own in a coexist project — the collision aquarius flagged)
        assert (fam / "thesis-README.md").is_file(), "thesis-README.md not written"
        # init must NOT write a root .gitignore (collides with article family / human's)
        assert not (cwd / ".gitignore").is_file(), "init must not write root .gitignore"
        # brother skill dirs each with a CONTRACT.md
        for s in init_project.BROTHER_SKILLS:
            assert (fam / s / "CONTRACT.md").is_file(), f"missing {s}/CONTRACT.md"
        # spine/polish/typeset do NOT get dirs
        assert not (fam / "thesis-spine").is_dir()
        assert not (fam / "thesis-polish").is_dir()
    finally:
        os.chdir(orig)
        shutil.rmtree(cwd, ignore_errors=True)
    print("test_init_builds_skeleton: PASS")

def test_init_weaves_template():
    import tempfile, shutil
    cwd = pathlib.Path(tempfile.mkdtemp())
    orig = pathlib.Path.cwd()
    # locate the generic-test pack inside the plugin: test_init.py is at
    # sci-skills-thesis/skills/thesis-init/scripts/ → parents[3] = sci-skills-thesis (plugin root)
    # templates/thesis/ ships inside the plugin so it resolves on standalone install too.
    plugin_root = pathlib.Path(__file__).resolve().parents[3]
    pack = plugin_root / "templates" / "thesis" / "generic-test"
    assert pack.is_dir(), f"test pack missing at {pack}"
    os.chdir(cwd)
    try:
        rc = init_project.main(["init", "--no-git", "--template", "generic-test"])
        assert rc == 0
        tex = cwd / "thesis" / "tex"
        assert (tex / "main.tex").is_file(), "main.tex not woven"
        assert (tex / "template-spec.md").is_file(), "template-spec.md not copied"
        # the chosen template-spec's naming convention is copied into thesis/
        spec = (cwd / "thesis" / "template-spec.md").read_text()
        assert "chapterN.tex" in spec, "naming convention not in woven spec"
    finally:
        os.chdir(orig)
        shutil.rmtree(cwd, ignore_errors=True)
    print("test_init_weaves_template: PASS")

if __name__ == "__main__":
    test_constants()
    print("test_constants: PASS")
    test_init_builds_skeleton()
    test_init_weaves_template()
