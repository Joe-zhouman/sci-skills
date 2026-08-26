# Adversarial Test Report — thesis-intro

> 审查日期：2026-08-27 | lens: aries (breaker) | git range: BASE 46b0297 → HEAD f07b7e1
> target: `sci-skills-thesis/skills/thesis-intro/` (SKILL.md + check_intro.py + 3 references + tests) + `sci-skills/skills/thesis-init/scripts/init_project.py` (placeholder edit)
> rounds run: R1 (boundary) · R2 (state-machine / code-fence toggle) · R4 (resource / symlink) · R5 (input / prompt-injection) · R6 (skills/MCP — mandatory). R3 (concurrency) skipped deliberately: check_intro.py is single-threaded, no shared mutable state, no async.

---

## BROKEN (bugs found — celebrate these)

### 1. `check_intro.py:46` — BOM silently drops Gap 1 from ALL checks (MEDIUM)

**What I did**: Wrote a gap-map.md that starts directly with `## Gap 1` (no leading `# comment` line — a plausible minimal form), where Gap 1 is BROKEN (dangling `filled-by: Chapter 999`, which doesn't exist in chapter-map.md), plus a clean Gap 2. Prepended a UTF-8 BOM (U+FEFF, bytes EF BB BF) — as a Windows LaTeX editor (Notepad, TeXstudio) commonly saves.

**What happened**: `split_gaps` regex `^##\s+(Gap\s+\d+)` requires the line to START with `##`. The BOM prefixes the first line as `﻿## Gap 1`, which does not match `^##` → Gap 1 is silently skipped. Its dangling `filled-by: Chapter 999`, its `callback-anchor`, its `status` are ALL never checked. The gate returns exit 0 (PASS) on a gap-map that contains a fabricated chapter number — a silent false-negative in the gate whose entire purpose is catching exactly that.

**Expected**: A BOM should not disable checks for the first gap. Either strip the BOM (`read_text(encoding="utf-8-sig")`) or tolerate it in the header regex.

**Reproduce**:
```bash
python3 -c '
import importlib.util, pathlib, tempfile
HERE = pathlib.Path("sci-skills-thesis/skills/thesis-intro/scripts")
spec = importlib.util.spec_from_file_location("check_intro", HERE/"check_intro.py")
ci = importlib.util.module_from_spec(spec); spec.loader.exec_module(ci)
GM = "﻿" + "## Gap 1\n- gap: x\n- filled-by: Chapter 999\n- status: filled\n- callback-anchor: y\n\n## Gap 2\n- gap: z\n- filled-by: Chapter 1\n- status: filled\n- callback-anchor: w\n"
CM = "## Chapter 1\n- tex-file: ch1.tex\n- status: written\n"
root = pathlib.Path(tempfile.mkdtemp())
gm = root/"gm.md"; gm.write_text(GM, encoding="utf-8")
cm = root/"cm.md"; cm.write_text(CM, encoding="utf-8")
td = root/"tex"; td.mkdir(); (td/"ch0-intro.tex").write_text("x")
print("issues:", ci.check(gm, cm, td))   # []  <- SILENT PASS on dangling Ch999
'
```

**Mitigation note**: The canonical schema in SKILL.md starts gap-map.md with a `# gap-map.md` comment line; when that comment line is present, the BOM lands on it (harmless — Gap 1 parses normally). The finding triggers only when the file starts directly with `## Gap 1`. Severity held at MEDIUM because the consequence (silent false-negative on the gate's core purpose) is serious, and a minimal/human-edited file without the comment is plausible. The same `^##` pattern lives in `_chapter_numbers_in:87` (chapter-map side) — a BOM on a chapter-map.md starting directly with `## Chapter N` would likewise drop that chapter from the valid set (a *false-positive* dangling on a real gap). Family-wide pattern (check_spine / check_dissect use the same `^##` match).

---

### 2. `check_intro.py:157` — Hardcoded `ch0-intro.tex` contradicts template-spec naming (MEDIUM)

**What I did**: Read the shipped `templates/thesis/generic-test/template-spec.md` (the ONLY template pack currently shipped), which states: "章文件：`chapterN.tex`（N 从 0 起：chapter0=绪论…）". So the intro is `chapter0.tex` per the shipped template. Then ran check_intro.py against a project whose intro is correctly named `chapter0.tex` per that template-spec.

**What happened**: `check()` hardcodes `intro_tex = tex_dir / "ch0-intro.tex"` (line 157) and does NOT read template-spec.md. With the intro correctly named `chapter0.tex` (per the shipped template), the gate reports `✗ ch0-intro.tex 不存在` — a FALSE FAILURE. Conversely, if the agent follows SKILL.md Step 2's literal "Write into `thesis/tex/ch0-intro.tex`", the gate passes — but `main.tex` does `\input{chapter0}`, so the intro is NOT compiled into the thesis. Silent breakage in one direction, false failure in the other.

This contradicts the init contract (`init_project.py:108` "本契约不硬编码章文件名——换模板就是换 [template-spec]" + `:131` "thesis-intro：…章文件名按 template-spec.md") and SKILL.md's own file-contract table (line 110/139 "filename per `template-spec.md`"). The sibling `check_dissect.py` is template-agnostic (reads each chapter's `tex-file` from chapter-map.md); intro has no equivalent — it hardcodes.

**Expected**: The intro filename should be template-derived (read from template-spec.md, or recorded in a baton as dissect records `tex-file`), not hardcoded.

**Reproduce**:
```bash
python3 -c '
import importlib.util, pathlib, tempfile
HERE = pathlib.Path("sci-skills-thesis/skills/thesis-intro/scripts")
spec = importlib.util.spec_from_file_location("check_intro", HERE/"check_intro.py")
ci = importlib.util.module_from_spec(spec); spec.loader.exec_module(ci)
GM = "## Gap 1\n- gap: x\n- filled-by: Chapter 1\n- status: filled\n- callback-anchor: y\n"
CM = "## Chapter 1\n- tex-file: chapter1.tex\n- status: written\n"
root = pathlib.Path(tempfile.mkdtemp())
gm = root/"gm.md"; gm.write_text(GM)
cm = root/"cm.md"; cm.write_text(CM)
td = root/"tex"; td.mkdir(); (td/"chapter0.tex").write_text("x")  # correct per shipped template
print("intro=chapter0.tex (per template):", ci.check(gm, cm, td))  # false failure
'
```

---

### 3. `test_check_intro.py` — Taurus honest-gate fix (unreadable chapter-map.md) is UNTESTED (LOW)

**What I did**: The task specifically asked to attack the taurus Important fix (commit 00dcb8f): when chapter-map.md is unreadable, the gate should (a) append a "cross-ref 跳过" issue, (b) continue core checks, (c) exit 1, (d) not double-report. I verified the fix ITSELF works correctly (see SURVIVED #1). But I grepped the test file for any test exercising the unreadable-chapter-map path.

**What happened**: There is NO test for the unreadable-chapter-map case. `tests/README.md` case 18 claims "reports an unreadable chapter-map.md honestly — if chapter-map.md exists but is binary/permission-denied, the gate appends a 'cross-ref 跳过' issue (fails exit 1)". But the actual 18th test function is `test_accepts_gap_headers_with_trailing_title` — unrelated. The README documents a test that does not exist. A future regression that re-introduces the silent-swallow (the exact bug taurus fixed) would be caught by nothing.

**Expected**: A `test_fails_on_unreadable_chapter_map` (binary chapter-map + a gap with a dangling filled-by → the "不可读 / cross-ref 跳过" issue appears, exit 1, core field checks still run).

**Reproduce**:
```bash
grep -niE "不可读|unreadable|cross-ref.*跳过|chapter_map.*binary|binary.*chapter_map" \
  sci-skills-thesis/skills/thesis-intro/scripts/test_check_intro.py
# (no output = no test covers the taurus fix)
```

---

### 4. `SKILL.md:305-307` — Untrusted-content guard omits `thesis-terminology-ledger.md` (LOW)

**What I did**: Read the "Untrusted content" guard (SKILL.md:304-325). It lists as UNTRUSTED: `thesis-sources.md`, `template-spec.md`, small papers, `chapter-map.md`, `thesis/tex/chN.tex`. The guard's own logic for chapter-map.md + chN.tex is: "sibling outputs that PROCESSED untrusted papers — they inherit those papers' content." I cross-checked against the files intro actually READS (Layout & boundaries + Step 0).

**What happened**: intro also reads `thesis-terminology-ledger.md` (Step 0 line 196; co-written, dissect extended it with paper-derived terms). By the guard's own logic, the terminology-ledger is a sibling output that processed untrusted papers (dissect extended it) and inherits their content — yet it is NOT listed in the untrusted set. A hostile paper could inject a "terminology" entry that is actually instruction-like text; the guard doesn't tell the agent to treat ledger entries as data-not-instructions.

**Expected**: Add `thesis-terminology-ledger.md` to the untrusted list (it fits the guard's stated criterion). Note: `thesis-spine.md` is also read but is author-gated architecture (not paper-derived), so treating it as trusted is defensible — not flagged.

**Reproduce**:
```bash
# guard lists these as untrusted:
grep -nE "UNTRUSTED DATA" sci-skills-thesis/skills/thesis-intro/SKILL.md
# terminology-ledger is READ but not listed:
grep -nE "terminology-ledger" sci-skills-thesis/skills/thesis-intro/SKILL.md | grep -i read
```

---

### 5. `check_intro.py:95` — Two-number `filled-by` silently picks the first (LOW)

**What I did**: Wrote `filled-by: Chapter 1 Chapter 999` (Gap 1 → Chapter 1 which exists; the second number 999 does not exist in chapter-map.md).

**What happened**: `_filled_by_chapter_num` uses `re.search(r"chapter\s+(\d+)", val, re.IGNORECASE)` which finds the FIRST match → `Chapter 1` → valid → gate PASSES. The dangling `Chapter 999` is silently ignored. The spec says one gap → one chapter, so a two-number filled-by is malformed; the gate accepts it anyway. (The inverse `Chapter 999 Chapter 1` picks 999 first → correctly fails.) Defense-in-depth gap: a malformed multi-chapter filled-by should be rejected, not silently accept whichever number happens to be first.

**Expected**: Reject a filled-by value containing more than one `Chapter N` token (or anchor the regex to the full value).

**Reproduce**:
```bash
python3 -c '
import importlib.util, pathlib, tempfile
HERE = pathlib.Path("sci-skills-thesis/skills/thesis-intro/scripts")
spec = importlib.util.spec_from_file_location("check_intro", HERE/"check_intro.py")
ci = importlib.util.module_from_spec(spec); spec.loader.exec_module(ci)
GM = "## Gap 1\n- gap: x\n- filled-by: Chapter 1 Chapter 999\n- status: filled\n- callback-anchor: y\n"
CM = "## Chapter 1\n- tex-file: ch1.tex\n- status: written\n"
root = pathlib.Path(tempfile.mkdtemp())
gm = root/"gm.md"; gm.write_text(GM); cm = root/"cm.md"; cm.write_text(CM)
td = root/"tex"; td.mkdir(); (td/"ch0-intro.tex").write_text("x")
print(ci.check(gm, cm, td))  # [] — passes, silently ignoring dangling Ch999
'
```

---

## SURVIVED (attacks that didn't work — code is solid here)

1. **Taurus honest-gate fix WORKS correctly** — the fix itself (the thing finding #3 says is untested) is correct on all four counts. Verified end-to-end:
   - (a) binary chapter-map.md → appends `✗ … 不可读（二进制/权限）— cross-ref 跳过`.
   - (b) core checks CONTINUE — a gap missing `callback-anchor` alongside an unreadable chapter-map produces BOTH issues (the unreadable one + the callback-anchor one).
   - (c) exit 1.
   - (d) NO double-report — missing (`不存在`, via `not chapter_map_path.is_file()`) and unreadable (`不可读`, via the try/except) are separated by the `is_file()` guard. Permission-denied (file exists, `is_file()`=True) reports `不可读`, NOT `不存在`. Clean separation.

2. **No shell footguns** — line-by-line review of `check_intro.py`: no `eval`/`exec`/`subprocess`/`os.system`/`socket`/`urllib`/`requests`/`import os`. Pure stdlib (`re`, `sys`, `pathlib`). No `rm`, no network listeners, no `curl|sh`, no runtime install. The only "execution" is `read_text` + regex. Clean.

3. **Code-fence toggle consistency (aries #2)** — `split_gaps:40-44` and `_chapter_numbers_in:82-86` both toggle on `line.lstrip().startswith("```")`. Both handle unclosed fences identically (drop everything after the opening fence). The plan-review's aries #2 hole (chapter-map side lacked the toggle) is FIXED — `test_ignores_chapter_headers_inside_code_fence` confirms; I verified a `## Chapter 99` inside a closed fence is correctly ignored and a dangling `filled-by: Chapter 99` still fails. An unclosed fence before `## Chapter 99` also correctly drops Ch99 while keeping real chapters before the fence.

4. **No content-driven path traversal** — unlike `check_dissect.py` (which builds `tex_dir / tf_name` from the `tex-file` field and needed the aries #1 traversal fix), `check_intro.py` builds NO path from file content. The only path is `tex_dir / "ch0-intro.tex"` (hardcoded filename — see finding #2 for the naming issue, but no traversal). `gap_map_path` / `chapter_map_path` / `tex_dir` come from CLI argv (operator-controlled), not from untrusted file content. So no untrusted-input path-traversal vector.

5. **Symlink gap-map.md → /etc/passwd** — the gate follows the symlink, reads /etc/passwd, finds no `## Gap N`, reports `✗ gap-map.md 无 \`## Gap N\` 条目`. No file content is echoed into issue strings (verified: no `root:` / `/bin/` leaks). The gate prints only issue summaries, never raw file content. No info leak.

6. **Resource/performance** — 10000 gaps parsed in 0.5s; a 100k-line single gap body in 0.18s. No hang, no memory blowup. No catastrophic regex backtracking (`_field_value` uses a literal-escaped field name + `.*$`, linear). `/dev/zero` symlink (infinite read) not safely testable — see UNTESTED.

7. **Binary/non-UTF-8 gap-map.md** — graceful: catches `UnicodeDecodeError`, returns a UTF-8 issue string, does not crash. `OSError` also caught. `check()` never raises (contract honored).

8. **Boundary values handled correctly** — `## Gap 0` / `## Gap 99999999999999` (no overflow — Python big ints) / leading zeros / lowercase `chapter`/`status` / trailing whitespace / CRLF / trailing-title `(研究背景)` / `Chapter 1 (note)` annotation — all parse or fail-correctly. `Chapter -1` / `Chapter1` (no space) / `## Gap` (no number) / `## Gap 1.5` correctly fail as unparseable. Fields without leading `- ` correctly fail (schema requires `- field: value`).

9. **init_project.py placeholder edit is clean** — `test_init.py` passes (exit 0). The 3-section edit (文件清单 names gap-map.md as baton; 这个文件夹是什么 + 谁读它 reference it) is the faithful mirror of dissect's CONTRACT.md naming chapter-map.md. No syntax issue, idempotent init flow intact (re-ran twice, no breakage).

10. **No harness-override / instruction-echoing in SKILL.md or references** — grepped for `ignore previous`/`disregard`/`override.*harness`/`you are`/`act as`/`system prompt`. The only hit is the guard ITSELF (SKILL.md:316) quoting `"ignore previous instructions"` as an example of data-not-instructions — correct. The 3 references contain prose craft guidance only; no language that could override the harness or that echoes untrusted content verbatim for an agent to obey.

11. **Docstring contradiction (plan-review finding) already fixed** — the plan review flagged a docstring saying "非本 coverage 门" (contradicting "非 coverage gate"). The shipped code says "非本 consistency 门" (check_intro.py:11) — consistent. Not a finding.

---

## UNTESTED (couldn't attack — missing capability)

1. **Prompt injection via agent reading hostile papers/chapters** — the untrusted-content guard (SKILL.md:304-325) is well-written: it lists the untrusted files, names injection patterns ("ignore previous instructions", embedded commands, URLs) as data-not-instructions, forbids running commands/fetching URLs/installing packages/changing behavior on file content, and instructs reporting instruction-like text verbatim + stop. But I cannot actually exercise agent behavior (would need to run the skill against a hostile paper and observe whether the agent obeys injected instructions vs. treats them as data). The guard LOOKS solid; agent-compliance is untestable by me. The conceptual vectors (R6: can a hostile registry `paths` field cause arbitrary file read? can a hostile `template-spec.md` filename cause a path-traversal write?) are mitigated by the guard's "data not instructions" framing + the Write/Read tools not being shells, but agent-judgment-dependent.

2. **`/dev/zero` symlink (infinite-read resource exhaustion)** — a symlink gap-map.md → /dev/zero would cause `read_text` to attempt an unbounded read (memory exhaustion / hang). Not safely testable without risking the sandbox. Vector requires planting a symlink at an operator-controlled CLI path, so it is low-likelihood (the operator chooses the path), but the script has no size guard.

---

## Verdict

**BREAKABLE** — 5 bugs found (2 MEDIUM, 3 LOW), must fix before deploy.

The two MEDIUMs are real consistency-gate failures:
- **#1 (BOM)** silently passes a gap with a fabricated chapter number — the gate's core purpose defeated by a BOM a Windows editor adds.
- **#2 (hardcoded ch0-intro.tex)** either falsely fails a correctly-named intro or silently passes an intro that won't compile into the thesis — contradicts the shipped template-spec and the init contract's "不硬编码章文件名."

The 3 LOWs are defense-in-depth / test-coverage gaps (#3 untested taurus fix, #4 guard omits terminology-ledger, #5 two-number filled-by). The init edit is clean. The taurus fix itself works — it's just untested.

Route: bugs → back to **capricorn** for fixes. The BOM fix is a one-liner (`utf-8-sig` or BOM-tolerant regex); the naming fix needs a design call (read intro name from template-spec, or record it in a baton like dissect's `tex-file`).

Report path: `docs/superpowers/reviews/2026-08-27-thesis-intro-adversarial.md`
