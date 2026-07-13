# sci-skills-init tests

Test plan (to be run via skill-creator-plus Test loop before deployment):

1. **init on empty dir** — `init_project.py init` in a clean cwd produces the
   full skeleton (manuscript/+v1/contract, sci-skills/ + 3 sibling dirs each
   with .README.md contract, .gitignore, .git). Idempotent: re-run skips all.
2. **init --no-git** — same skeleton, no .git/.
3. **checkup on healthy layout** — exit 0, reports all rounds/siblings, no issues.
4. **checkup with misplaced items** — drop a stray .tex in project root; checkup
   reports it in misplaced-items signal (non-zero exit).
5. **migrate is NOT a subcommand** — `init_project.py migrate` errors with
   "choose from {init, checkup}".

Each contract (.README.md) content is verified by string match on key sections
(manuscript: v/r scheme; sci-draw: figN-report 6 sections; etc.).

TODO: scaffold evals.json + run the full Test loop (gen-eval → init-workspace →
spawn → grade → aggregate) per skill-creator-plus before this skill ships.
