# Project_Simulator -- E0240 Project 1: LLM serving pipeline as a queueing network

Discrete-time (slotted, cycle-driven) queueing-network simulator for an LLM
inference serving pipeline: Q1 admission/tokenize (Geo/D/1, S1=2) -> Q2
batching scheduler (release at B collected or tau waited) -> Q3 GPU workers
(c workers, deterministic or geometric batch service with configurable
batching gain delta). Fixed-increment time advance, exactly the class MATLAB
code's scheme (`single_queue_simulation_geo_d_1.m`); pure Python + numpy +
matplotlib; no SimPy, no other dependencies.

Built: Phases 1 and 2 (engine, V1/V2/V3 validation, E2) plus Phase 3A
(E3 batching experiment, convention-check artifact, completed figures).
NOT yet started: the Phase-2/Phase-3 report documents and V4 (reserved for
the queueing-theory lectures).

## Run (one command each, in this folder)

```bash
python check_conventions.py  # engine vs class-MATLAB transliteration etc. (~2 s)
python run_validation.py     # V1+V2+V3, writes results/*.csv + validation table  (~4 min)
python run_experiments.py    # E2, writes results/experiment_e2_pipeline.csv     (~2 min)
python run_e3.py             # E3, writes results/experiment_e3_batching.csv     (~3 min)
python plot_all.py           # figures/*.pdf + .png (course plot conventions)    (~15 s)
```

Full suite is about 9 to 10 minutes on this laptop. Deterministic: seed
20260922, fixed RNG draw order (DECISIONS.md #8); rerunning reproduces every
number bit-for-bit (verified: all result CSVs regenerate identically).

**Environment note (this machine):** your user PYTHONPATH leaks another
tool's venv and breaks matplotlib imports. If `import matplotlib` fails, run
as `env -u PYTHONPATH python run_validation.py` (Git Bash) or clear PYTHONPATH.

## Files

| File | Purpose |
|---|---|
| `network_sim.py` | Engine: ServiceStation, Batcher, Network (cycle loop). Docstring maps every part to the L2 s10 DES component list. |
| `configs.py` | Seed, course lambda sweep, lengths, topology builders (single-station anchors + pipeline with batching gain delta). |
| `run_validation.py` | V1/V2/V3 + `results/validation_table.csv` (metric \| simulated \| analytical \| rel err \| status). |
| `run_experiments.py` | E2: D vs Geo service, c=1 vs c=2, end-to-end delay + per-node occupancy vs injection rate. |
| `run_e3.py` | E3: batching trade-off, B x tau grid at lambda=0.3, batch service `ceil(S3 + delta*(B-1))`, delta configurable (`E3_DELTA`). |
| `check_conventions.py` | Reproducible convention evidence: bit-exact counters vs a transliteration of the class MATLAB loop, batcher timer corner case, pgf identity. Exits nonzero on mismatch. |
| `plot_all.py` | All figures, Assignment-1 plot conventions (distinct markers, units, grid, PDF). |
| `VERIFICATION.md` | **Read this first**: every check, numbers, pass/fail, plus a 10-line review list at the top. |
| `DECISIONS.md` | Every assumption made across the build, numbered, for your audit. |
| `ISSUES.md` | Validation discrepancies and their resolution. |
| `results/*.csv` | All raw numbers. Every report figure/table must cite these. |
| `figures/*.pdf` | LaTeX-ready figures (PNG twins for quick viewing). |

## Figures

`fig_e1_validation_geo_d_1` (S=2) and `fig_e1_validation_geo_d_1_S3` (E1),
`fig_v2_factor2` (V2), `fig_e2_e2e_delay`, `fig_e2_q3_occupancy`,
`fig_e2_node_occupancy` (E2), `fig_e3_batching` (E3).

## Validation anchors (defaults)

- Single station: Geo/D/1 (S=2 and S=3) and Geo/Geo/1 (mean 2) -- the same
  engine, one station; reproduces Assignment 1 conventions exactly.
- Pipeline: Q1 Geo/D/1 S1=2 -> Q2 pass-through (B=1, tau=0) -> Q3 c=1,
  geometric mean 2.
- Sweep: lam = [0.05:0.05:0.45, 0.49] (course `top_script.m` array), lengths
  {1e3, 1e5, 1e7}; lam=0.49 rows are informational (rho=0.98 converges slowly,
  see DECISIONS.md #9). At S=3 the sweep stops at lam=0.30 (stability,
  DECISIONS.md #14).
- E3 grid: B in {1,2,4,8,16} x tau in {2,8} at lam=0.3, delta=0.5, lengths
  {1e6, 1e7} (DECISIONS.md #20).

## Presentation artifacts

| File | Role |
|---|---|
| `phase3_presentation_beamer_v4.tex` / `.pdf` | **Current final presentation** (11 slides, LaTeX Beamer). Build: `sh build_presentation_beamer.sh` (two pdflatex passes); charts from `make_beamer_figures_v2.py` (E1/E2) and `make_beamer_figures_v3.py` (E3). |
| `phase3_presentation_beamer_v3.tex` / `.pdf`, `_v2`, and `phase3_presentation_beamer.tex` / `.pdf` | Earlier Beamer drafts (serif, pre-footer-cleanup, pre-color-system), superseded. |
| `phase3_presentation_v2.pptx` / `.pdf`, `_v1`, and `phase3_presentation.pptx` / `.pdf` | Historical PowerPoint decks, superseded. |
| `make_beamer_figures_v2.py` / `make_beamer_figures_v3.py` | Beamer charts from the same frozen CSVs (semantic colors). |
| `make_slide_figures.py` / `make_slide_figures_v2.py`, `render_equations.py` | Historical PPTX-era chart and equation-image builders. |
