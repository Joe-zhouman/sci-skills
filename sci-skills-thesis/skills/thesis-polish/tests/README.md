# thesis-polish tests

Test plan (run via skill-creator-plus eval loop before deployment):

1. **机械检查** — `scripts/check_polish.py` (the gate) +
   `scripts/test_check_polish.py` (29 stdlib cases, run `python3
   test_check_polish.py`). Exit-code contract: 0 = 一致性通过; 1 =
   有 issue（逐条打印）. Two args: `<tex-dir> <ledger>`, defaults
   `thesis/tex` + `sci-skills/thesis-terminology-ledger.md` (relative to
   cwd, i.e. the project root). Two mechanical checks only (spec §④):
   ① ledger enforce — the ledger markdown table's variant→canonical pairs
   (header-name matched, aquarius P6) grep'd across all chapter tex, LaTeX
   comments excluded; ② 交叉引用悬空, single direction
   (`\ref`/`\eqref`/`\autoref`/`\cref`/`\Cref`, comma multi-key included →
   nonexistent `\label`; unused labels are P5 noise, never reported).
   Bounded output: MAX_ISSUES (200) + an explicit truncation line (no
   silent cap; `check()` returns `(issues, total)` so main()'s header and
   the sentinel line print the SAME true total). Explicit call list in
   `__main__` (no auto-discovery — the 29 count below is verified against
   the on-disk functions). All 29 cases, one-by-one:
   - `test_passes_on_clean` — passes on a settled ledger + clean chapter
     tex (variant-free, every ref resolves);
   - `test_unused_label_is_not_reported` — P5 pin: the clean fixture
     itself contains `\label{ch:intro}` never `\ref`'d, so the clean pass
     doubles as the single-direction pin (unused labels are systematic
     noise — ch:/sec:/eq: labels legally never cited);
   - `test_fails_on_cjk_variant_residue` — CJK variant residue flags with
     file:line AND the canonical form in the issue (`卷积神经网络` → CNN);
   - `test_ascii_variant_word_boundary` — ASCII variants match on word
     boundaries: standalone `um` flags, `um` embedded in `columnum`/
     `\nums` does NOT (CJK has no `\b` — substring matching there);
   - `test_fails_on_dangling_ref` — a `\ref` to a nonexistent label flags
     悬空 with file:line;
   - `test_eqref_cref_recognized_and_multikey` — `\eqref` recognized as a
     ref; comma multi-key `\cref{fig:overview,tab:none}` checks EACH key;
     an existing key inside a multi-key cref is NOT flagged;
   - `test_variant_in_comment_not_flagged` — full-line AND inline LaTeX
     comments excluded from the variant scan;
   - `test_ref_in_comment_not_flagged` — comments excluded from the ref
     scan too (`% \ref{fig:none}` not flagged);
   - `test_escaped_percent_keeps_text` — `\%` is a literal percent: text
     after it stays checked (F3 — an escape must not kill the rest of the
     line);
   - `test_double_backslash_then_percent_is_comment` — `\\%` = newline
     command then comment: text after it IS comment (F3 — even-backslash
     counting; the state machine has no lookbehind hole);
   - `test_ledger_missing_degrades_to_crossref` — ledger missing → ONE
     degraded-mode issue + crossref still checked (spec §④ — polish
     tolerates half-finished projects);
   - `test_ledger_without_table` — a prose-only ledger with no parseable
     term table → explicit issue;
   - `test_ledger_table_in_fence_ignored` — a fenced table (example block)
     is NOT ledger data → the no-table issue fires;
   - `test_orphan_fence_diagnostic` — odd ``` count → explicit 未闭合
     code fence diagnostic (fail-noisy: an orphan fence would swallow
     every table after it);
   - `test_bom_ledger_still_parsed` — a UTF-8 BOM does not drop the first
     table out of the checks;
   - `test_binary_ledger_graceful` — binary/non-UTF-8 ledger → graceful
     issue (降级), never a raise;
   - `test_binary_tex_graceful` — binary/non-UTF-8 chapter tex → graceful
     (a list is returned, never a raise);
   - `test_ansi_stripped_from_issues` — ANSI/control sequences in ledger
     values echoed into issue lines are stripped (no terminal-title
     rewrite / log-line forgery surface — aries B5 lineage);
   - `test_ansi_in_tex_ref_key_stripped` — same sanitize discipline on the
     tex side: a `\ref` key carrying an ANSI escape is echoed sanitized
     (I6 — key comes from raw tex bytes, same B5 surface);
   - `test_mismatched_ledger_row_counted_not_silent` — a ledger row whose
     cell count mismatches the header (unescaped `|` in a cell) is NOT
     silently dropped: one summary fail-noisy issue (M8);
   - `test_short_canonical_row_surfaced` — a row with a single-char
     canonical (`λ`-type) is mechanically unenforceable under
     VARIANT_MIN_LEN: one issue surfaces it for author attention instead
     of a silent skip (M10);
   - `test_separator_row_skipped` — direct parser pin (one white-box
     assert, M11): the `|---|---|` separator row yields no bogus pair AND
     counts as neither dropped nor short-canonical;
   - `test_header_name_matching_tolerates_columns` — a FOUR-column ledger
     (no Category) and extra columns both parse — header-NAME matching,
     not column-count matching (aquarius P6);
   - `test_non_term_table_ignored` — a non-term table (header names carry
     no variants/canonical columns) is skipped, not mis-parsed;
   - `test_variant_inside_canonical_skipped` — a variant contained in its
     own canonical (`T` ⊂ `$T(x)$`) is a never-enforceable self-bite pair
     — skipped (F2: correct text necessarily contains the canonical, a
     flag there would always false-fire);
   - `test_truncation_cap` — 250 dangling refs → exactly MAX_ISSUES (200)
     issues + 1 explicit truncation line, and the returned `total` carries
     the TRUE count (250);
   - `test_truncation_header_true_total` — main()'s header prints the true
     total (250), the same number as the sentinel line — not the kept-list
     length (I7);
   - `test_missing_tex_dir` — missing tex-dir → explicit 不存在 issue
     (thesis/tex 未建？先跑写作链);
   - `test_empty_tex_dir` — empty tex-dir (zero .tex files) → explicit
     issue (写作链未产正文？).

2. **报告 parser** — two parsers, both emitting the SAME stdout neutral
   intermediate format (spec §③): a 风险句清单 manifest of
   `- sentence / location / risk / meta`. Report content is UNTRUSTED —
   pure text extraction, nothing executed; output sentences are
   control-sequence-sanitized (aries B5 lineage). Exit codes: 0 = parsed;
   1 = structured error on stderr; 2 = usage.

   - `scripts/parse_paperyy.py` + `test_parse_paperyy.py` (13 stdlib
     cases, run `python3 test_parse_paperyy.py`). PaperYY = ONE offline
     HTML file; the wenqu-verified shape: `em.high` sentences +
     `p.uncheck` section titles + truncation of the repeated block from
     致谢 on. Parsing is a LINEAR tag-token walk (C2 — the old paired
     regex was quadratic on unclosed tags). All 13 cases:
     - `test_parse_collects_high_with_sections_and_stops_at_zhixie` —
       em.high-only collection (low NOT collected), location = section
       title + `#id`, meta carries PaperYY, collection stops at 致谢
       (the repeated block is not harvested);
     - `test_parse_double_quote_attrs_and_nested_tags` — double-quoted
       attributes, multi-value class (`class='some high extra'`), nested
       tags stripped — attribute-order-independent parsing;
     - `test_parse_ansi_stripped` — ANSI stripped from output sentences;
     - `test_parse_spanning_nested_tag_stripped` — a nested tag SPANNING
       a newline is stripped whole (I4 — the tag never enters the text
       buffer under the token walk);
     - `test_parse_data_attrs_no_false_match` — `data-class=`/`data-id=`
       do NOT classify as class/id (attribute-boundary anchored, M12 — a
       crafted report can't inflate its own risk level);
     - `test_hostile_unclosed_tags_bounded_linear` — ~250KB of unclosed
       `<em>` tags completes in bounded linear time (< 10s; the old regex
       measured 19.8s at this size) AND still yields the drift verdict
       (rc 1) — the UNTRUSTED-surface guarantee (C2);
     - `test_parse_html_entities_unescaped` — HTML entities unescaped
       (`A &amp; B &lt;C&gt;` → `A & B <C>`);
     - `test_main_bom_report_no_leak` — a BOM-prefixed report is read
       utf-8-sig; U+FEFF never reaches any sentence/location (M13,
       mirrors the family check scripts' decode);
     - `test_main_prints_manifest` — manifest format on stdout
       (`# 风险句清单` + `- sentence:` / `location:` lines), rc 0;
     - `test_main_missing_file_structured_error` — missing file →
       structured stderr error, rc 1;
     - `test_main_empty_report_structured_error` — a report with NO em/p
       structure at all → 未解析出 structured error, rc 1 (drift);
     - `test_main_low_only_clean_report_rc0_empty_manifest` — an all-low
       (zero high) report is a CLEAN result, not drift: empty manifest +
       rc 0 (C1, F6 — mirrors parse_paperpass; structure seen but zero
       highs is a real post-polish re-detection state);
     - `test_main_usage_error` — no args → rc 2.

   - `scripts/parse_paperpass.py` + `test_parse_paperpass.py` (11 stdlib
     cases, run `python3 test_parse_paperpass.py`). PaperPass = a report
     DIRECTORY (data under `htmls/js/`: `detaildata.js` aiScore headline
     + `reduceaigcpagelistdata0.js` fragment list). All 11 cases:
     - `test_parse_score_threshold_and_meta` — score ≥ MIN_SCORE (80)
       collected (79.9 dropped, the 80.0 boundary kept), risk =
       `score=N`, the aiScore headline carried in every meta;
     - `test_parse_multiline_fragment_joined` — multiline fragment
       content joined into one sentence;
     - `test_parse_ansi_stripped` — ANSI stripped from output sentences;
     - `test_parse_type_confused_fragment_info_skipped` — a fragment
       whose `originalFragmentInfo` is a STRING (type-confused JSON) is
       skipped gracefully — no traceback out of parse() (I3, UNTRUSTED
       surface);
     - `test_parse_nonstring_section_content_type_safe` —
       `sectionContentList` mixing non-string elements is joined via
       `str()`, no TypeError (I3);
     - `test_main_prints_manifest` — manifest format on stdout
       (`- sentence:` / `risk: score=…` lines), rc 0;
     - `test_main_missing_dir_structured_error` — missing directory →
       structured stderr error, rc 1;
     - `test_main_missing_js_structured_error` — a directory without
       `reduceaigcpagelistdata0.js` → structured error naming the file,
       rc 1;
     - `test_main_malformed_json_structured_error` — malformed JSON →
       structured error, rc 1;
     - `test_main_clean_report_rc0_empty_manifest` — zero ≥80 fragments
       = a clean result, NOT a failure: empty manifest (0 段, 解析正常)
       + rc 0 (F6);
     - `test_main_usage_error` — no args → rc 2.

   NOTE: all parser fixtures are CONSTRUCTED (no PII, no real report
   data — SKILL.md Privacy). Real reports may drift from these shapes;
   drift = a parser update task, and the structured-error exit (rc 1) is
   the drift signal, never a silent pass. 知网 = future extension slot: a
   parser joining the same stdout format once a sample report exists (no
   downstream change).

3. **the split (stated honestly)** — check_polish.py is **MECHANICAL
   CONSISTENCY ONLY**:
   - NOT prose quality — depth is human review (Step 4) + eval
     territory;
   - NOT unused labels — single direction only (aquarius P5);
   - NOT a re-run of write-time chain gates — 写作链各 check 脚本 are
     write-time checks, NOT post-polish invariants (glossary Intro↔Summary
     coherence lock; after polish rewrites prose, baton positions drift —
     known and accepted, re-running would only misfire);
   - NOT AIGC score — only re-detection knows (再检测是唯一分数真相);
     AIGC 降了多少分不设机械验收 (spec Acceptance #2).
   What the gate DOES catch: variant residue + dangling crossref + the
   structural failure modes of its two inputs (missing/binary ledger or
   tex, no-table, orphan fence, missing/empty tex-dir). State this
   plainly — do NOT overclaim a "quality guarantee" (SKILL.md's honest
   boundary).

4. **prose is NOT script-tested** — the diagnose-layered workflow's
   judgment is evaluated via skill-creator-plus's eval loop later, not
   here. That judgment includes:
   - **diagnose-layer behavior** — 先结构后句子: a structurally-broken
     paragraph is never sentence-polished; Stage A is the NAMED exception
     (it runs before structural diagnosis so report locations stay fresh)
     and Step 2 re-checks every Stage A sentence at the register layer;
   - **seam grading (缝合分级)** — sentence-level seam → patch grounded
     at matching granularity (`trace.md` → chapter-map → spine);
     structure-level break → surfaced to the author, never restructured;
   - **lever discipline** — levers ordered by quality damage: 回真实材料
     first; quality-destroying levers (换冷僻词 / 同义词轰炸) NEVER chosen;
   - **register calibration** — 此外/然而/综上所述 are standard academic
     connectives, NOT AI tells (not killed); 赋能/闭环-type buzzwords
     killed;
   - **gap-map anchor protection** — callback sentences keep their
     anchors while neighboring text is rewritten;
   - **ledger co-write discipline** — new canonical forms and constraints
     written back at Step 3 with `source: thesis-polish`; no ad-hoc
     per-chapter renames.

5. **decoupling assertions (programmatic)** —
   - grep: `scripts/*.py` contains no sibling check-script names — the
     shared-helper provenance comments say 家族最硬化 check 脚本 (verbatim
     inheritance), never a sibling's filename;
   - grep: SKILL.md + references never name a sibling's script —
     write-time gates are referred to as 写作链各 check 脚本 (zero
     sibling-filename hits).

**Known limitation (honest, mirror thesis-theory tests/README practice):**
the eval loop is prose-judgment, non-deterministic — state plainly, don't
pretend the script covers depth. check_polish.py is mechanical
consistency, not depth (a well-formed but hollow paragraph passes the
gate — human review + eval territory). The parsers were built against
CONSTRUCTED fixtures mirroring the wenqu-verified report shapes; real
reports may drift (the structured-error exit surfaces it). The parsers'
hostile-input guarantees — clean-vs-drift verdict, no-traceback,
bounded-time — are only as good as their hostile-input tests (taurus
review: the two crash paths and the clean-report path were all untested
edges, exactly where constructed fixtures stop covering); 知网 parser is
a future extension slot (needs a sample report). AIGC 降了多少分不设机械
验收 (spec Acceptance #2) — 再检测是唯一分数真相.

TODO: scaffold evals.json + run the full eval loop per skill-creator-plus
before ship (the prose surface).
