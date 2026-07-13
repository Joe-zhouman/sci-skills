# sci-write tests

Test plan (run via skill-creator-plus Test loop before deployment):

1. **draft paper-plan from raw data** — give a small CSV + research question;
   skill runs profile_data, drafts figure list, stops for human confirm.
   Verify: data-profile.json written, paper-plan.md drafted with fig entries
   (claim/data-source/suggested-chart/status=pending), NOT auto-landed (waits).
2. **scan_neighbor status report** — pre-place fig1-report.md in ../sci-draw/;
   run scan_neighbor.py; verify it reports fig1 ready (suggest drawn), fig2 pending.
3. **write Results from figure reports** — pre-place fig1-report.md + fig1-reading.md;
   skill writes results.md where every claim hangs on a figure/stat, verbs calibrated,
   md draft in sci-write/ (NOT manuscript/ — must not touch manuscript/).

Decoupling assertions (programmatic):
- grep: zero `from sci-draw`/`import sci-draw` in sci-write source
- skill never writes to ../manuscript/ or ../sci-draw/

TODO: scaffold evals.json + run full Test loop per skill-creator-plus before ship.
