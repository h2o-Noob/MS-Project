# VERIFICATION.md -- overnight build, Phases 1 and 2

Every check, its numbers, pass/fail, relative error. All numbers come from
the `results/*.csv` produced by the logged runs (seed 20260922, deterministic;
rerunning `python run_validation.py` and `python run_experiments.py`
reproduces every digit). Headline table: `results/validation_table.csv`.

## Review this first (10 lines)

1. Bottom line: **87 checks pass, 0 fail**; 5 rows "expected-slow" (all at
   lambda=0.49, rho=0.98, where 1e7 cycles is known-insufficient), 6 rows
   "a1-formula-S2-only" (see item 2).
2. **One analytical finding (the only surprise):** the A1 report formula
   Lq = lam^2*(S-1)/(1-lam*S) matches this simulator's convention ONLY at
   S=2. At S=3 the sim is exactly 1.5x = S/2 times it (measured ratio
   1.4974..1.5069). Derivation in ISSUES.md #1 says the sim is right and the
   formula is S=2-specific. The course-verbatim top_script Wq formula holds
   for all S and passes everywhere (<0.65%). Please sanity-check the
   derivation before the Phase-2 report uses it.
3. lambda=0.49 at 1e7: 1.09% (Geo/D/1 Lq) and 1.57% (Geo/Geo/1 Lq) error,
   flagged informational per DECISIONS #9 (A1's own data: needs 1e8 for 1%).
4. E2's "D" curves have **exactly zero** Q3 occupancy at every lambda. That
   is a provable resonance (deterministic S1=S3=2: upstream departures are
   >= 2 cycles apart, so a 2-cycle downstream service never queues), not a
   routing bug. DECISIONS #19.
5. E2 uses common random numbers: at each (lambda, length) all four configs
   run the identical arrival stream, so end-to-end differences are exactly
   Q3's effect (c1-D and c2-D e2e are identical by construction). DECISIONS #18.
6. The S=3 V1 sweep stops at lambda=0.30: rho = lam*S < 1 is required, the
   course array's upper end is only valid at S=2. DECISIONS #14.
7. The pass-through Q2 station produces 0-vs-0 checks (zero delay by
   design); rel_err treats identical zeros as pass.
8. Engine was speed-tuned after correctness was locked (17.1 -> 6.5 s per
   1e7 single-station run); the class-code cycle order is unchanged
   (DECISIONS #16). The equivalence is now REPOSITORY EVIDENCE:
   `check_conventions.py` transliterates the class MATLAB loop statement
   for statement and matches the engine's integer counters exactly on four
   (S, lam, T) cases over identical arrival sequences (bit-exact = equal
   arrival / occupancy-counter / utilization-counter totals). ALL PASS.
9. Timings on this laptop (Phase-3A rerun): check_conventions.py ~2 s,
   run_validation.py 200 s, run_experiments.py 116 s, run_e3.py 159 s,
   plot_all.py ~15 s. Python 3.14.3, numpy 2.4.2, matplotlib 3.10.8. No
   C++ needed at these lengths. Reproducibility proof: after the Phase-3A
   code changes, all seven pre-existing result CSVs regenerated
   bit-identically (diffed against backups).
10. Run it: `python run_validation.py && python run_experiments.py &&
    python plot_all.py` (see README for the PYTHONPATH caveat on this
    machine).

## V1: single-station Geo/D/1 (validation anchor; engine, one station)

Targets: Wq = rho*(S-1)/(2*(1-rho)) [top_script.m, course-verbatim],
Lq = lam*Wq [class-code exact], Lq_A1 = lam^2*(S-1)/(1-lam*S) [A1 report;
equals the above only at S=2]. Sweep: course array, lengths {1e3, 1e5, 1e7}.
Files: `results/validation_geo_d_1_S2.csv`, `results/validation_geo_d_1_S3.csv`.

| Check (1e7 cycles, lam <= 0.45) | max rel err | verdict |
|---|---|---|
| S=2: Lq vs A1 formula (= class-code at S=2) | 0.75% (at 0.35) | PASS (<1%) |
| S=2: Wq vs top_script formula | 0.65% | PASS |
| S=3: Lq vs lam*Wq | 0.46% | PASS |
| S=3: Wq vs top_script formula | 0.46% | PASS |
| S=3: Lq vs A1 formula | 49.7%..50.7% off (ratio 1.50) | formula out of scope (ISSUES #1) |
| S=2 at lam=0.49: Lq / Wq | 1.09% / 1.05% | expected-slow |

Spot numbers (lam=0.3, 1e7): Lq 0.22603 vs 0.22500; Wq 0.75304 vs 0.75.
Convergence at lam=0.3 (Lq rel err): 7.6% (1e3) -> 1.8% (1e5) -> 0.46% (1e7),
the course's simulation-length device working as expected.

## V2: single-station Geo/Geo/1 (mean service 2) + factor-2

Target: Lq = 2*lam^2/(1-2*lam). File: `results/validation_geo_geo_1.csv`,
`results/validation_factor2.csv`.

| Check (1e7 cycles) | result | verdict |
|---|---|---|
| Lq rel err, lam <= 0.45 | max 0.94% | PASS (<1%) |
| Lq rel err at lam=0.49 | 1.57% | expected-slow |
| factor-2 ratio sim(Geo/Geo/1)/sim(Geo/D/1), lam <= 0.45 | 1.9835..2.0190 | PASS (within 0.95% of 2.0) |
| ratio at lam=0.49 | 1.9474 | expected-slow |

## V3: full pipeline (Q1 Geo/D/1 S1=2 -> Q2 pass-through -> Q3 Geo mean 2, c=1)

Internal-consistency checks only; no network closed forms are claimed
(queueing-network theory lectures are 22/09-01/10, reserved as V4).
File: `results/validation_pipeline_v3.csv`. All rows below at 1e7 cycles.

| Check | max rel err (lam = 0.1, 0.3, 0.49) | verdict |
|---|---|---|
| Flow balance dep/arr = 1, every node | 1.5e-5 | PASS |
| Utilization vs rho_i = lam_i*E[S_i] (Q1: 2*lam, Q3: 2*lam) | 0.10% | PASS |
| W = Lq/lam vs measured Wq, every node | 1.7e-5 | PASS |
| Network L_total = lam*W_e2e_qwait | 5.2e-6 | PASS |
| Network throughput = lam | 0.10% | PASS |

(Per-lambda: utilization and throughput rel err are 0.10% / 0.06% / 0.01%
at lam = 0.1 / 0.3 / 0.49; the flow-balance, W-relation and L_total maxima
are their lam=0.49 values, and at lam <= 0.3 those three are <= 3.3e-7.)

## E3: batching trade-off (Phase 3A)

Grid: B in {1,2,4,8,16} x tau in {2,8} at lambda = 0.3, delta = 0.5
(configurable as `E3_DELTA` in run_e3.py), deterministic batch service
ceil(S3 + delta*(b-1)), S3 = 2. 10 configs x 2 lengths {1e6, 1e7} = 20 rows
in `results/experiment_e3_batching.csv`. Seed 20260922 with CRN seeding
[SEED, T] per length (DECISIONS #21): all ten configs at a length run the
identical external arrival stream. Row-level sanity, all 20 rows hold:
throughput = 0.3 within 1%; 1 <= mean batch fill <= B; and
4 <= W_e2e_sojourn - W_e2e_qwait <= 2 + ceil(2 + delta*(B-1)) (sojourn
minus summed queue waits is the request's total service time, bounded by
the minimum and maximum batch durations). The two lengths agree on
end-to-end sojourn to <= 0.004 cycles across the whole grid.

Results at 1e7 cycles (1e6 agrees to two decimals):

| config | mean fill | W_e2e_sojourn | W_e2e_qwait | util_Q3 |
|---|---|---|---|---|
| B=1 (either tau) | 1.00 | 4.75 | 0.75 | 0.5999 |
| tau=2, B=2..16 | 1.57 | 6.75 | 2.02 | 0.4906 |
| tau=8, B=2 | 1.95 | 7.36 | 2.38 | 0.4536 |
| tau=8, B=4 | 3.17 | 10.44 | 4.87 | 0.3224 |
| tau=8, B=8 and B=16 | 3.33 | 10.97 | 5.39 | 0.3063 |

Measured observations (no trend claimed beyond these):
- **Knee, tau=8:** saturation between B=4 and B=8. Mean fill rises 1.95 ->
  3.17 -> 3.33 and then is flat (B=8 and B=16 rows are literally identical
  in every recorded metric: the batch-size threshold is never reached
  before the timer, so both configs produce the same trajectory). Marginal
  delay cost beyond the knee is also flat (10.97 at both).
- **Knee, tau=2:** flat from B=2 onward (rows for B=2..16 identical): at
  this timer the queue never accumulates to B, so B is inert.
- **Throughput is 0.3 in every row**: at this load batching produces no
  throughput gain; the curves are flat by stability, not by tuning.
- **Delay is minimized at B=1 (no batching) in every configuration of this
  grid** (4.75 vs 6.75 to 10.97). The Q3 service saving is real
  (util_Q3 0.60 -> 0.31 at tau=8) but is smaller than the added Q2 waiting
  cost at lambda = 0.3. With deterministic Q3 service this is consistent
  with E2: deterministic service leaves little variability for batching to
  absorb. No claim is made outside the tested grid.

## E2: pipeline load response (experiments; no analytical targets)

File: `results/experiment_e2_pipeline.csv` (44 runs; sweep at 1e6 cycles,
1e7-cycle spots at lam=0.3; CRN-paired arrivals, DECISIONS #18).

End-to-end sojourn (cycles/request), paired arrival streams:

| lam | c1-D | c2-D | c1-Geo | c2-Geo |
|---|---|---|---|---|
| 0.30 (1e6) | 4.754 | 4.754 | 5.871 | 4.770 |
| 0.45 (1e6) | 8.519 | 8.519 | 15.350 | 8.549 |
| 0.30 (1e7 spot) | 4.752 | 4.752 | 5.887 | 4.768 |

Readings (for the Phase-2/3 reports; every number traceable to the CSV):
- Variability premium at Q3, c=1, lam=0.45: +6.83 cycles e2e (8.52 ->
  15.35) purely from making Q3 geometric at the same mean and the same
  arrival stream: the network echo of the single-queue factor-2 result.
- c=2 absorbs it: c2-Geo is within 0.03 cycles of the all-deterministic
  bound at lam=0.45 (Q3 wait 0.032 cycles).
- The deterministic resonance (DECISIONS #19): Lq_Q3 = 0 exactly on all D
  curves (verified over 1e7 cycles at lam=0.3, 0.45, 0.49).
- Saturation: at lam=0.49 both c1 curves converge upward (28.8 vs 69.2);
  rho_1 = 0.98 is the binding constraint (Q1, not Q3).

## Figures (PDF for LaTeX, PNG for viewing)

`figures/fig_e1_validation_geo_d_1.pdf` and
`fig_e1_validation_geo_d_1_S3.pdf` (E1, S=2 and S=3),
`fig_v2_factor2.pdf` (V2), `fig_e2_e2e_delay.pdf`,
`fig_e2_q3_occupancy.pdf`, `fig_e2_node_occupancy.pdf` (E2, per-node
Q1/Q2/Q3 panels), `fig_e3_batching.pdf` (E3, delay/throughput/fill vs B).
Course plot conventions: x = swept parameter, distinct markers, unit
labels, grid on, PDF.

## Not done (report drafting and V4; deliberately untouched)

Phase-2/Phase-3 report documents, presentation material, V4 network closed
forms (reserved for the 22/09-01/10 lectures), Q4 split node, and any
narrative findings text. E3, the convention-check artifact and all figures
are complete as of Phase 3A.
