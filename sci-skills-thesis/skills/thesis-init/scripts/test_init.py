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
        # E1: template-spec.md must NOT be duplicated in tex/ (canonical home is thesis/template-spec.md)
        assert not (tex / "template-spec.md").is_file(), "template-spec.md should be at thesis/ not tex/"
        # the chosen template-spec's naming convention is copied into thesis/ (canonical location)
        spec = (cwd / "thesis" / "template-spec.md").read_text()
        assert "chapterN.tex" in spec, "naming convention not in woven spec"
    finally:
        os.chdir(orig)
        shutil.rmtree(cwd, ignore_errors=True)
    print("test_init_weaves_template: PASS")

def test_init_idempotent():
    import tempfile, shutil
    cwd = pathlib.Path(tempfile.mkdtemp())
    orig = pathlib.Path.cwd()
    plugin_root = pathlib.Path(__file__).resolve().parents[3]  # plugin root (same index as test_init_weaves_template)
    os.chdir(cwd)
    try:
        init_project.main(["init", "--no-git", "--template", "generic-test"])
        # snapshot: capture content of a woven file + a contract
        main_tex = (cwd / "thesis" / "tex" / "main.tex").read_text()
        contract = (cwd / "thesis" / "CONTRACT.md").read_text()
        # second run — must not error, must not overwrite existing files
        rc = init_project.main(["init", "--no-git", "--template", "generic-test"])
        assert rc == 0
        # idempotent: existing files unchanged
        assert (cwd / "thesis" / "tex" / "main.tex").read_text() == main_tex
        assert (cwd / "thesis" / "CONTRACT.md").read_text() == contract
    finally:
        os.chdir(orig)
        shutil.rmtree(cwd, ignore_errors=True)
    print("test_init_idempotent: PASS")

def test_checkup_healthy():
    import tempfile, shutil
    cwd = pathlib.Path(tempfile.mkdtemp())
    orig = pathlib.Path.cwd()
    os.chdir(cwd)
    try:
        init_project.main(["init", "--no-git", "--template", "generic-test"])
        rc = init_project.main(["checkup"])
        assert rc == 0, "healthy layout should exit 0"
    finally:
        os.chdir(orig); shutil.rmtree(cwd, ignore_errors=True)
    print("test_checkup_healthy: PASS")

def test_checkup_missing_workspace():
    import tempfile, shutil
    cwd = pathlib.Path(tempfile.mkdtemp())
    orig = pathlib.Path.cwd()
    os.chdir(cwd)
    try:
        rc = init_project.main(["checkup"])  # never init'd
        assert rc != 0, "uninit'd project should exit non-zero"
    finally:
        os.chdir(orig); shutil.rmtree(cwd, ignore_errors=True)
    print("test_checkup_missing_workspace: PASS")

def test_checkup_prints_json():
    """U1: checkup prints a JSON block (for programmatic consumption), mirroring article-init."""
    import io, contextlib, tempfile, shutil
    cwd = pathlib.Path(tempfile.mkdtemp())
    orig = pathlib.Path.cwd()
    os.chdir(cwd)
    try:
        init_project.main(["init", "--no-git", "--template", "generic-test"])
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = init_project.main(["checkup"])
        assert rc == 0, "healthy layout should exit 0"
        out = buf.getvalue()
        assert "--- JSON ---" in out, "checkup must print a JSON block for programmatic consumption"
        assert '"project_root"' in out, "JSON must include project_root"
        assert '"thesis"' in out, "JSON must include thesis state"
        assert '"sci-skills"' in out, "JSON must include sci-skills state"
    finally:
        os.chdir(orig); shutil.rmtree(cwd, ignore_errors=True)
    print("test_checkup_prints_json: PASS")

def test_checkup_reports_misplaced_items():
    """U1: a stray file in project root is reported as a misplaced item + surfaces in JSON."""
    import io, contextlib, tempfile, shutil
    cwd = pathlib.Path(tempfile.mkdtemp())
    orig = pathlib.Path.cwd()
    os.chdir(cwd)
    try:
        init_project.main(["init", "--no-git", "--template", "generic-test"])
        # drop a stray file in project root (not under thesis/ or sci-skills/)
        (cwd / "stray.tex").write_text("% misplaced", encoding="utf-8")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = init_project.main(["checkup"])
        assert rc != 0, "a misplaced item should make checkup exit non-zero"
        out = buf.getvalue()
        assert "stray.tex" in out, "checkup must name the misplaced item in its report"
        assert '"root_candidates"' in out, "JSON must list root_candidates"
    finally:
        os.chdir(orig); shutil.rmtree(cwd, ignore_errors=True)
    print("test_checkup_reports_misplaced_items: PASS")

def test_checkup_flags_missing_main_tex():
    """Important#1: if thesis/tex/main.tex is missing, checkup flags it (weave integrity).
    main.tex is the universal compile entry point — every pack ships one; its absence
    means the weave didn't complete or the file was deleted."""
    import io, contextlib, tempfile, shutil
    cwd = pathlib.Path(tempfile.mkdtemp())
    orig = pathlib.Path.cwd()
    os.chdir(cwd)
    try:
        init_project.main(["init", "--no-git", "--template", "generic-test"])
        # delete main.tex — simulate incomplete weave / accidental deletion
        (cwd / "thesis" / "tex" / "main.tex").unlink()
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = init_project.main(["checkup"])
        assert rc != 0, "missing main.tex should make checkup exit non-zero"
        out = buf.getvalue()
        assert "main.tex 缺失" in out, "checkup must flag missing main.tex"
    finally:
        os.chdir(orig); shutil.rmtree(cwd, ignore_errors=True)
    print("test_checkup_flags_missing_main_tex: PASS")

def test_checkup_flags_missing_tex_dir():
    """Minor#4: if thesis/tex/ dir itself is missing (partial init), checkup flags it
    instead of silently reporting 'tex 文件: 0'."""
    import io, contextlib, tempfile, shutil
    cwd = pathlib.Path(tempfile.mkdtemp())
    orig = pathlib.Path.cwd()
    os.chdir(cwd)
    try:
        init_project.main(["init", "--no-git", "--template", "generic-test"])
        # remove tex/ dir entirely — simulate partial init / deleted tex/
        shutil.rmtree(cwd / "thesis" / "tex")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = init_project.main(["checkup"])
        assert rc != 0, "missing tex/ dir should make checkup exit non-zero"
        out = buf.getvalue()
        assert "tex/ 缺失" in out, "checkup must flag missing tex/ dir"
    finally:
        os.chdir(orig); shutil.rmtree(cwd, ignore_errors=True)
    print("test_checkup_flags_missing_tex_dir: PASS")

def test_init_skips_symlinks_in_pack():
    """Bug 1 (aries HIGH): a malicious --template-dir pack with a symlinked file
    (leaked_key.tex -> ~/.ssh/id_rsa) must NOT have its target content copied into
    thesis/tex/. shutil.copyfile follows symlinks by default; the fix is to detect
    symlinks in _weave_template and skip them with a warning (a legitimate template
    pack has no symlinks). Covers both file and dir symlinks."""
    import io, contextlib, tempfile, shutil, os
    cwd = pathlib.Path(tempfile.mkdtemp())
    orig = pathlib.Path.cwd()
    # build a malicious pack: legit main.tex + a symlinked FILE + a symlinked DIR,
    # both pointing at a target outside the pack holding secret content
    pack = pathlib.Path(tempfile.mkdtemp())
    secret = pathlib.Path(tempfile.mkdtemp())
    (pack / "main.tex").write_text("% legit", encoding="utf-8")
    (secret / "id_rsa").write_text("SSH-Private-Key-LEAK", encoding="utf-8")
    (secret / "shadow").write_text("root:x:0:0:root", encoding="utf-8")
    os.symlink(secret / "id_rsa", pack / "leaked_key.tex")
    os.symlink(secret, pack / "leaked_dir")
    os.chdir(cwd)
    try:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = init_project.main(["init", "--no-git", "--template-dir", str(pack)])
        assert rc == 0
        tex = cwd / "thesis" / "tex"
        # the legit file is woven
        assert (tex / "main.tex").is_file(), "legit main.tex should be woven"
        # Bug 1: neither the symlinked file NOR its target content is in tex/
        assert not (tex / "leaked_key.tex").is_file(), \
            "symlinked file target content was exfiltrated into tex/ (Bug 1)"
        assert not (tex / "leaked_key.tex").is_symlink(), \
            "symlink itself must not be copied into tex/ either"
        # the symlinked dir is not followed/copied
        assert not (tex / "leaked_dir").is_dir(), \
            "symlinked dir target was recursively copied into tex/ (Bug 1)"
        # the secret content never landed in the project
        assert not (tex / "leaked_key.tex").exists()
        # a warning was issued naming the skipped symlink
        out = buf.getvalue()
        assert "符号链接" in out or "symlink" in out.lower(), \
            "weave must warn about the skipped symlink"
        assert "leaked_key.tex" in out, "warning must name the skipped symlink"
    finally:
        os.chdir(orig)
        shutil.rmtree(cwd, ignore_errors=True)
        shutil.rmtree(pack, ignore_errors=True)
        shutil.rmtree(secret, ignore_errors=True)
    print("test_init_skips_symlinks_in_pack: PASS")

def test_init_rejects_traversal_template():
    """Bug 2 (aries MEDIUM): --template is documented as a pack NAME. An absolute path
    (--template /tmp/secret) bypasses PLUGIN_TEMPLATES_DIR (Python Path join-on-absolute
    replaces the base) and a traversal (--template ../../tmp/secret) climbs above the
    plugin; both copy an arbitrary dir into thesis/tex/. The fix: reject --template
    values that aren't a simple name (path separators / absolute / ..)."""
    import io, contextlib, tempfile, shutil, os
    secret = pathlib.Path(tempfile.mkdtemp())
    (secret / "s.txt").write_text("LEAK", encoding="utf-8")
    # both attack shapes for the same containment check
    attacks = [
        str(secret),                       # absolute path
        os.path.relpath(secret),           # relative traversal (../..<secret>)
    ]
    for t in attacks:
        cwd = pathlib.Path(tempfile.mkdtemp())
        orig = pathlib.Path.cwd()
        os.chdir(cwd)
        try:
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = init_project.main(["init", "--no-git", "--template", t])
            out = buf.getvalue()
            # init still succeeds (builds skeleton) — it just refuses the weave
            assert rc == 0, f"--template {t!r} should not crash init"
            assert (cwd / "thesis" / "CONTRACT.md").is_file(), "skeleton must still build"
            # the arbitrary dir must NOT be woven into tex/
            assert not (cwd / "thesis" / "tex" / "s.txt").is_file(), \
                f"--template {t!r} copied an out-of-plugin dir into tex/ (Bug 2)"
            # a warning naming the offending value was printed
            assert "⚠" in out, f"--template {t!r} must emit a warning"
        finally:
            os.chdir(orig)
            shutil.rmtree(cwd, ignore_errors=True)
    shutil.rmtree(secret, ignore_errors=True)
    print("test_init_rejects_traversal_template: PASS")

def test_init_heals_deleted_tex_dir():
    """Bug 3 (aries MEDIUM): tex/ is only created when thesis/ is absent. Delete
    thesis/tex/ + re-run init -> FileNotFoundError at the weave (dst parent missing),
    tex/ never recreated, project un-healable by init alone. init must ensure tex/
    exists in BOTH the exists/absent branches (idempotent heal)."""
    import tempfile, shutil
    cwd = pathlib.Path(tempfile.mkdtemp())
    orig = pathlib.Path.cwd()
    os.chdir(cwd)
    try:
        # first init — succeeds, weaves main.tex into tex/
        rc = init_project.main(["init", "--no-git", "--template", "generic-test"])
        assert rc == 0
        assert (cwd / "thesis" / "tex" / "main.tex").is_file()
        # simulate a corrupted/deleted weave — the natural recovery is to re-run init
        shutil.rmtree(cwd / "thesis" / "tex")
        assert not (cwd / "thesis" / "tex").exists()
        # second init — must NOT crash; must recreate tex/ and re-weave
        rc = init_project.main(["init", "--no-git", "--template", "generic-test"])
        assert rc == 0, "re-init after tex/ deletion must not crash"
        assert (cwd / "thesis" / "tex").is_dir(), "tex/ must be recreated on re-init"
        assert (cwd / "thesis" / "tex" / "main.tex").is_file(), \
            "template must re-weave into the recreated tex/"
    finally:
        os.chdir(orig)
        shutil.rmtree(cwd, ignore_errors=True)
    print("test_init_heals_deleted_tex_dir: PASS")

if __name__ == "__main__":
    test_constants()
    print("test_constants: PASS")
    test_init_builds_skeleton()
    test_init_weaves_template()
    test_init_idempotent()
    test_init_skips_symlinks_in_pack()
    test_init_rejects_traversal_template()
    test_init_heals_deleted_tex_dir()
    test_checkup_healthy()
    test_checkup_missing_workspace()
    test_checkup_prints_json()
    test_checkup_reports_misplaced_items()
    test_checkup_flags_missing_main_tex()
    test_checkup_flags_missing_tex_dir()
