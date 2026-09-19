# E0240 Project 1 -- Complete Source Archive (for teammates)

This is the complete editable/source archive for our E0240 Project 1:
a queueing-network simulator for an LLM inference serving pipeline,
plus all three phase reports, the final presentation, results, figures,
and the documents that explain how everything was built and verified.

## Final deliverables

- Phase-1 report: `Phase1/phase1_final_report.pdf`
- Phase-2 progress report: `Phase2/phase2_progress_report.pdf`
- Phase-3 final report: `Phase3/phase3_final_report.pdf`
- Phase-3 final presentation: `Phase3/phase3_presentation_beamer_v4.pdf`

Use `phase3_presentation_beamer_v4.pdf` as the final presentation.
Earlier PPTX and Beamer versions are historical and are not final
deliverables (they remain only in the original working repository).

## Where the source code is

`Project_Simulator/` is the main simulator. The engine is
`network_sim.py`; the experiment drivers are `run_validation.py` (V1/V2/V3
validation), `run_experiments.py` (E2), and `run_e3.py` (E3 batching).
`plot_all.py` regenerates the report figures, and `check_conventions.py`
re-runs the verification evidence (engine-vs-MATLAB equivalence, batcher
corner case, pgf identity). Python and TEX sources are included, so
everything can be inspected and edited.

## Where the results are

`Project_Simulator/results/` has all result CSVs:
`validation_table.csv`, `validation_geo_d_1_S2.csv`,
`validation_geo_d_1_S3.csv`, `validation_geo_geo_1.csv`,
`validation_factor2.csv`, `validation_pipeline_v3.csv`,
`experiment_e2_pipeline.csv`, `experiment_e3_batching.csv`, plus the two
run logs. Every number quoted in the reports and presentation comes from
these files.

## Where the figures are

`Project_Simulator/figures/` has the report-ready PDF figures and their
PNG twins, plus the three Beamer chart PDFs (`bf2_*`, `bf3_*`) that the
presentation source includes. `plot_all.py` regenerates the report
figures from the results CSVs.

## Important documents

- `README.md`: run guide and file map for the simulator folder.
- `VERIFICATION.md`: every validation check with numbers and pass/fail.
- `DECISIONS.md`: all modeling assumptions, numbered, with reasons.
- `ISSUES.md`: discrepancies found during the build and their resolution.
- `PHASE3_EVIDENCE_PACK.md`: the audited numerical evidence base.
- `Course_Context/`: the course mining report, the class MATLAB files the
  engine mirrors, and the course sample-project list.

## Reproduction

From `Project_Simulator/` (Python 3 with numpy and matplotlib):

```bash
python check_conventions.py  # convention checks (~2 s)
python run_validation.py     # V1+V2+V3 validation suite (~4 min)
python run_experiments.py    # E2 experiment (~2 min)
python run_e3.py             # E3 batching experiment (~3 min)
python plot_all.py           # report figures (~15 s)
```

To rebuild the presentation PDF (LaTeX with lmodern, beamer, booktabs,
tex-gyre fonts):

```bash
pdflatex phase3_presentation_beamer_v4.tex   # run twice
```

or use `build_presentation_beamer.sh`. Fixed seed 20260922; rerunning
the suite regenerates every reported number.

## Source map

- Phase 1: `Phase1/` (final PDF + TEX; in the original repository these
  are `Project_Phase1/phase1_v4.pdf` and `phase1_problem_statement.tex`)
- Phase 2: `Phase2/`
- Phase 3 report and presentation: `Phase3/`
- Simulator: `Project_Simulator/`
- Results: `Project_Simulator/results/`
- Figures: `Project_Simulator/figures/`
- Evidence: `PHASE3_EVIDENCE_PACK.md` and the verification documents

## Current status

- Phase 1: complete.
- Phase 2 report: complete.
- Phase 3 final report: complete.
- Final Beamer presentation: complete.
- V4 (network-level analytical validation): pending the corresponding
  course material, as stated in the reports.

## Historical versions

The original repository also keeps older presentation versions
(`phase3_presentation.pptx/.pdf`, `_v1`, `_v2`, and Beamer v1 to v3) and
PPTX-era builders. They are deliberately excluded here to avoid
confusing them with the final deliverables.

## Human action

The group-member line on the title pages is still the placeholder
"[Name (SR No.)]". Replace or remove it before submission; no real
names are included in this archive.
