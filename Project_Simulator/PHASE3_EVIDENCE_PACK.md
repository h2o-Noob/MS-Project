# PHASE3_EVIDENCE_PACK.md -- evidence base for the Phase-3 final report

Prepared 2026-09-06 from the frozen repository. Every number below was
extracted from the named CSV by script in this session; nothing is from
memory. This pack supports report writing; it is not itself report prose.
No em dashes are used anywhere in this file.

## 1. Frozen Repository State

Frozen artifacts (verified by timestamp, none modified after their phase):

| Artifact | Timestamp | State |
|---|---|---|
| `phase2_progress_report.tex` / `.pdf` | 2026-09-06 12:39 | 3 pages, judge-passed, frozen in Phase 3C |
| `results/validation_*.csv` (6 files) | 2026-09-06 09:10 to 09:14 | Phase 3A regenerated set, bit-identical to validated results |
| `results/experiment_e2_pipeline.csv` | 2026-09-06 09:16 | Final E2 dataset |
| `results/experiment_e3_batching.csv` | 2026-09-06 09:08 | Final E3 dataset |
| `results/validation_table.csv` | 2026-09-06 09:14 | 98-row headline table (87 pass, 5 expected-slow, 6 a1-formula-S2-only, 0 FAIL) |
| `figures/*.pdf/.png` (7 + 7) | 2026-09-06 09:10 | Final figures |
| `VERIFICATION.md`, `DECISIONS.md`, `ISSUES.md`, `README.md` | 2026-09-06 05:42 to 09:19 | Frozen docs |

Dataset inventory (row counts counted from the files):

| Dataset | File | Rows | Grid | Lengths | Seed |
|---|---|---|---|---|---|
| V1 Geo/D/1 S=2 | `validation_geo_d_1_S2.csv` | 30 | 10 lambdas x 3 lengths | 1e3, 1e5, 1e7 | 20260922 (sequential shared) |
| V1 Geo/D/1 S=3 | `validation_geo_d_1_S3.csv` | 18 | 6 lambdas x 3 lengths (stability cut at 0.30) | same | same |
| V2 Geo/Geo/1 | `validation_geo_geo_1.csv` | 30 | 10 x 3 | same | same |
| V2 factor-2 | `validation_factor2.csv` | 10 | 10 lambdas at 1e7 | 1e7 | same |
| V3 pipeline | `validation_pipeline_v3.csv` | 50 | 5 runs x 10 checks | 1e3/1e5 at 0.3; 1e7 at 0.1/0.3/0.49 | same |
| E2 | `experiment_e2_pipeline.csv` | 44 | 4 configs (D/Geo x c=1/2) x 10 lambdas + 4 spots at 1e7 | 1e6 + 1e7 spots | CRN [20260922, lam_idx, T] |
| E3 | `experiment_e3_batching.csv` | 20 | 5 B x 2 tau at lambda=0.3, delta=0.5 | 1e6 and 1e7 | CRN [20260922, T] |

Service laws and settings per dataset: V1 deterministic S in {2,3}; V2
geometric mean 2; V3 pipeline Q1 deterministic S1=2, Q2 pass-through (B=1,
tau=0), Q3 geometric mean 2, c=1; E2 Q3 deterministic (duration 2) or
geometric (mean 2), c in {1,2}; E3 Q3 deterministic batch service
ceil(2 + 0.5*(b-1)), B in {1,2,4,8,16}, tau in {2,8}.

No conflicting versions exist: each experiment has exactly one CSV and one
log, and after the Phase 3A code freeze all seven pre-existing CSVs were
regenerated bit-identically (diffed against backups), so the files on disk
are the validated numbers.

## 2. E2 Results

Source for everything in this section: `results/experiment_e2_pipeline.csv`
(44 rows; sweep at 1e6 cycles, CRN so all four configs at a lambda share the
identical external arrival stream; Q1 is deterministic S1=2, Q2 pass-through).

**E2-A: service-variability premium at c=1 (EXPERIMENTAL).** End-to-end
sojourn, deterministic vs geometric Q3 at equal mean 2:

| lambda | c1-D sojourn | c1-Geo sojourn | abs diff | rel diff (vs D) | Lq_Q3 (D) | Lq_Q3 (Geo) |
|---|---|---|---|---|---|---|
| 0.05 | 4.057 | 4.142 | 0.085 | 2.1% | 0.0000 | 0.0044 |
| 0.10 | 4.123 | 4.303 | 0.180 | 4.4% | 0.0000 | 0.0183 |
| 0.15 | 4.214 | 4.535 | 0.321 | 7.6% | 0.0000 | 0.0483 |
| 0.20 | 4.332 | 4.835 | 0.503 | 11.6% | 0.0000 | 0.1004 |
| 0.25 | 4.505 | 5.264 | 0.759 | 16.9% | 0.0000 | 0.1889 |
| 0.30 | 4.754 | 5.871 | 1.117 | 23.5% | 0.0000 | 0.3349 |
| 0.35 | 5.157 | 6.919 | 1.761 | 34.2% | 0.0000 | 0.6162 |
| 0.40 | 6.018 | 9.067 | 3.049 | 50.7% | 0.0000 | 1.2185 |
| 0.45 | 8.519 | 15.350 | 6.831 | 80.2% | 0.0000 | 3.0761 |
| 0.49 | 28.823 | 69.151 | 40.329 | 139.9% | 0.0000 | 19.7793 |

The premium grows monotonically with load, from 2.1% to 139.9%. Strength of
wording for the report: exact under the tested paired-arrival configuration
at c=1; do not state it as a universal law.

**E2-B: a second worker absorbs the premium (EXPERIMENTAL).** At
lambda = 0.45 (1e6): c1-Geo 15.350 vs c2-Geo 8.549; c2-Geo minus c1-D =
0.0296 cycles (c1-D = c2-D = 8.5192 identically, since Q3 never queues on
the D curves). At lambda = 0.30 the 1e7 spot rows give c1-Geo 5.8871 vs
c2-Geo 4.7684 against c1-D 4.7517 (residual 0.0167).

**E2-C: deterministic tandem zero queue (STRUCTURAL).** All 22
deterministic-config rows (both c values, all 10 lambdas, sweep and spots)
have Lq_Q3 exactly 0.0. The argument in DECISIONS.md #19 remains valid under
exactly the tested assumptions, restated: (i) a single deterministic server
with S1 = 2 cannot emit two completions closer than 2 cycles (the next
completion is a full service period after the previous dispatch), (ii) the
pass-through batcher adds zero delay (measured Wq_Q2 = 0 and Lq_Q2 = 0 in
every row), so Q3 arrivals are spaced at least 2 cycles apart, and (iii) a
2-cycle deterministic service that starts at cycle t frees the worker during
cycle t+2's service step, which precedes that cycle's dispatch step; the
earliest possible next arrival (t+2) therefore always finds a free or
just-freed worker, so the Q3 queue can never become positive. c = 2 only
adds capacity, so the same holds. This is a proof for the E2 configuration
plus exact measurement (22/22 rows); classify it as STRUCTURAL.

**E2-D: per-node reading (EXPERIMENTAL).** At lambda = 0.45, c1-D:
Lq_Q1 = 2.0346 (matches the standalone Geo/D/1 analytical 2.0250 to 0.37%),
Lq_Q2 = 0, Lq_Q3 = 0, util_Q1 = util_Q3 = 0.9004 (= 2*lambda), throughput
0.4502. All end-to-end delay on the D curves is Q1 queueing plus the fixed
4 cycles of service. At lambda = 0.49 (near saturation, rho_1 = 0.98) the D
and Geo c=1 curves converge upward (28.823 vs 69.151): Q1 becomes the
binding constraint, not Q3.

## 3. E3 Results

Source for everything in this section:
`results/experiment_e3_batching.csv` (20 rows; lambda = 0.3, delta = 0.5,
deterministic batch service ceil(2 + 0.5*(b-1)); CRN [20260922, T] so all
ten configs at a length share the identical arrival stream).

Full table (T = 1e7; the 1e6 columns agree to the shown precision except
where noted in section 4):

| B | tau | fill | W_soj | W_q | Lq_Q2 | Lq_Q3 | throughput | util_Q3 | svc/batch |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2 | 1.00 | 4.752 | 0.752 | 0.00 | 0.000 | 0.3000 | 0.5999 | 2.000 |
| 1 | 8 | 1.00 | 4.752 | 0.752 | 0.00 | 0.000 | 0.3000 | 0.5999 | 2.000 |
| 2 | 2 | 1.57 | 6.752 | 2.023 | 0.38 | 0.000 | 0.3000 | 0.4906 | 2.574 |
| 2 | 8 | 1.95 | 7.360 | 2.384 | 0.49 | 0.000 | 0.3000 | 0.4536 | 2.953 |
| 4 | 2 | 1.57 | 6.752 | 2.023 | 0.38 | 0.000 | 0.3000 | 0.4906 | 2.574 |
| 4 | 8 | 3.17 | 10.438 | 4.875 | 1.24 | 0.000 | 0.3000 | 0.3224 | 3.409 |
| 8 | 2 | 1.57 | 6.752 | 2.023 | 0.38 | 0.000 | 0.3000 | 0.4906 | 2.574 |
| 8 | 8 | 3.33 | 10.969 | 5.391 | 1.39 | 0.000 | 0.3000 | 0.3063 | 3.400 |
| 16 | 2 | 1.57 | 6.752 | 2.023 | 0.38 | 0.000 | 0.3000 | 0.4906 | 2.574 |
| 16 | 8 | 3.33 | 10.969 | 5.391 | 1.39 | 0.000 | 0.3000 | 0.3063 | 3.400 |

Verified observations (each checked against the CSV in this session):

1. **B = 1 gives the minimum end-to-end sojourn in this grid** (4.752 vs
   6.752 to 10.969). In every tested (B, tau) combination the Q2 waiting
   cost exceeds the Q3 service saving. Observed in this grid; no claim
   outside it, and no optimality statement beyond "in this grid".
2. **tau = 2 makes B >= 2 effectively identical**: the rows for
   B in {4, 8, 16} are identical to B = 2 in every recorded metric
   (verified programmatically, both lengths). The timer binds before the
   batch-size threshold is ever reached, so B is inert.
3. **tau = 8 saturates the batch fill around B = 8**: fill 1.95 (B=2) ->
   3.17 (B=4) -> 3.33 (B=8) -> 3.33 (B=16).
4. **B = 8 and B = 16 are identical in every recorded metric** at both
   lengths (verified programmatically): the threshold is unreachable within
   tau = 8 at lambda = 0.3, so both configs produce the same trajectory.
5. **Throughput stays at lambda throughout**: max |throughput - 0.3| over
   all 20 rows is 0.000178 (0.06% relative). No throughput effect at this
   load; the system is stable everywhere.
6. **The batching knee is a saturation knee between B = 4 and B = 8 at
   tau = 8**, decided from the measurements: fill and delay both flatten
   there (10.438 -> 10.969 -> 10.969). At tau = 2 the curve is flat from
   B = 2 onward. There is no interior delay-minimizing knee: delay rises
   with batching everywhere in this grid while per-batch service grows
   2.000 -> 3.400 and per-worker utilization falls 0.5999 -> 0.3063 (the
   resource-saving side of batching is real; it is the delay side that
   dominates at lambda = 0.3).
7. **Lq_Q3 = 0.000 in all 20 rows**: with deterministic batch durations of
   at most 4 cycles and release spacing lower-bounded by the timer plus an
   arrival, the GPU queue never accumulates. Measured exact; classify as
   empirical with a partial structural argument (weaker than E2-C because
   batch duration depends on fill).

## 4. Convergence Checks

Course methodology (simulation-length comparison), explicitly not a
confidence interval or statistical test.

**E3, 1e6 vs 1e7** (both lengths exist for every grid point):

| B | tau | |W_soj(1e6) - W_soj(1e7)| | relative |
|---|---|---|---|
| 1 | 2 | 0.0022 | 0.046% |
| 1 | 8 | 0.0022 | 0.046% |
| 2 | 2 | 0.0022 | 0.032% |
| 2 | 8 | 0.0027 | 0.037% |
| 4 | 2 | 0.0022 | 0.032% |
| 4 | 8 | 0.0038 | 0.036% |
| 8 | 2 | 0.0022 | 0.032% |
| 8 | 8 | 0.0023 | 0.021% |
| 16 | 2 | 0.0022 | 0.032% |
| 16 | 8 | 0.0023 | 0.021% |

Maxima over the whole grid and five metrics (sojourn, Q2+Q3 wait, fill,
throughput, utilization): absolute 0.0038, relative 0.29%. Qualitative
conclusions (knee location, B-invariance at tau = 2, delay minimum at B = 1,
flat throughput) are identical at both lengths.

**E2, 1e6 sweep vs 1e7 spots at lambda = 0.3**: sojourn 4.754 vs 4.7517
(c1-D), 5.871 vs 5.8871 (c1-Geo); Lq_Q3 0.3349 vs 0.3403 (c1-Geo). Ordering
and magnitudes agree.

**V1/V2 convergence** (from the validation CSVs, lambda = 0.3, S = 2): Lq
relative error 7.6% (1e3) -> 1.8% (1e5) -> 0.46% (1e7), the course's
length-sweep device working as expected.

## 5. Final Figures

| File | Purpose | Source CSV | Parameters shown | Conclusion supported | Scale/interpretation notes |
|---|---|---|---|---|---|
| `fig_e1_validation_geo_d_1` | E1 validation, S=2 | `validation_geo_d_1_S2.csv` | 10 lambdas, lengths 1e3/1e5/1e7 | convergence onto the analytical Geo/D/1 curve | the 1e3 curve is far off by design (convergence evidence); caption must say so |
| `fig_e1_validation_geo_d_1_S3` | E1 companion, S=3 | `validation_geo_d_1_S3.csv` | 6 lambdas (0.05-0.30), 3 lengths | S=3 agreement with the S-general pair | sweep truncated at 0.30 for stability; the report caption must state this |
| `fig_v2_factor2` | V2 factor-2 check | `validation_geo_d_1_S2.csv` + `validation_geo_geo_1.csv` at 1e7 | 10 lambdas | Geo/Geo/1 = 2 x Geo/D/1 | the Geo/D/1 dashed analytical line is derived as half the Geo/Geo/1 analytical column |
| `fig_e2_e2e_delay` | E2 headline | `experiment_e2_pipeline.csv` (1e6 sweep) | 4 configs x 10 lambdas | variability premium at c=1; c=2 absorbs it | at 0.49 both c=1 curves rise steeply (saturation); do not extrapolate past 0.49 |
| `fig_e2_q3_occupancy` | E2 Q3 queue | same | same | D curves exactly 0; c1-Geo grows to 19.78 | flat-zero D lines are the structural result, not missing data |
| `fig_e2_node_occupancy` | E2 per-node panels | same | Q1/Q2/Q3, shared y | Q1 identical across configs (paired streams), Q2 zero, Q3 split | shared y prevents scale exaggeration |
| `fig_e3_batching` | E3 trade-off | `experiment_e3_batching.csv` (1e7) | 5 B x 2 tau | saturation knee; flat throughput | throughput panel uses fixed ylim (0, 0.45) to avoid autoscale noise; state this if queried |

Minimum figure set for a 4-page final report: `fig_e1_validation_geo_d_1`
(validation), `fig_v2_factor2` (validation), `fig_e2_e2e_delay` (E2
finding), `fig_e3_batching` (E3 finding). Optional if space allows:
`fig_e2_node_occupancy`. `fig_e2_q3_occupancy` is redundant with the node
panels; the S=3 companion figure is optional (its content can be one table
row plus a sentence).

## 6. V4 Status

The course folder still contains exactly the four August lecture decks
(`1_Lecture_11_08_26.pdf` through `4_lecture_20_08_26.pdf`, mtimes 2026-08-25);
no queueing-theory or queueing-network lecture material has appeared. Per the
course timeline in the mining report, those lectures are scheduled for
22/09 to 01/10, which is after today's date (2026-09-06). Therefore: **V4
remains intentionally open.** No network-level analytical validation target
exists yet, none is implemented, and none may be invented for the final
report. The report should present V3 as accounting/flow consistency and may
state that analytical network validation will follow the corresponding
lectures.

## 7. Defensible Limitations

Each limitation corresponds to the actual implementation:

1. **Linear feedforward chain only.** The network routes a linear station
   list with one entry and one exit; splits and feedback are unsupported
   (the Q4 tool-call branch was deferred). No claim about meshed or
   feedback networks is supported.
2. **Single Bernoulli external input, at most one arrival per cycle.** The
   entry station draws one Bernoulli test per cycle; correlated or
   burstier arrival processes are not modeled.
3. **Static batching only.** A batch is closed at release; requests never
   join a running batch (continuous batching is out of scope, as stated in
   Phase 1).
4. **Batch-level service abstraction.** One worker serves one batch, all
   members share the duration, and the batching gain is the configured
   sublinear law S3 + delta*(b-1). No memory/cache/compute contention, no
   preemption, no per-request decode-length heterogeneity inside a batch.
5. **Service laws limited to deterministic and geometric.** Real decode
   lengths can be heavier-tailed; nothing in the package supports other
   laws yet (the engine's law field accepts only these two).
6. **Tick-quantized timing.** Delays are whole cycles with same-cycle
   immediate access; sub-cycle effects do not exist in the model.
7. **No network-level analytical validation yet.** V3 is internal
   accounting and flow consistency; V4 is open pending the lectures.
8. **Single-seed deterministic runs, adequacy by length sweeps.** The
   package contains no replications or intervals by design (course
   convention); robustness evidence is the 1e6-vs-1e7 and cross-config
   agreement quantified in section 4.
9. **Unbounded queues, no admission control.** Requests never time out or
   get shed; saturated behavior (lambda = 0.49) shows growing delay, not
   rejection.
10. **Uncalibrated cycle mapping.** One cycle = one scheduler tick is a
    representative choice (Phase-1 Table 1 flags it as such); no measured
    serving-system calibration is embedded in the results.

## 8. Ranked Findings

Ranked by strength and report value. Category labels are strict:
VALIDATION = simulator matches an analytical result; EXPERIMENTAL = observed
response under the tested grid; STRUCTURAL = implied by the model under
stated assumptions.

1. **VALIDATION.** The engine reproduces the Geo/D/1 anchors: worst
   occupancy error 0.75% (S=2) and 0.46% (S=3) over the stable sweep
   (lambda <= 0.45) at 1e7 cycles, against the S-general pair
   Wq = rho(S-1)/(2(1-rho)), Lq = lambda*Wq. Evidence:
   `validation_geo_d_1_S2.csv`, `validation_geo_d_1_S3.csv`. Strength:
   full quantitative claim permitted (with the lambda=0.49 caveat).
2. **VALIDATION.** Geo/Geo/1 (mean 2) matches 2*lambda^2/(1-2*lambda) with
   worst error 0.94%, and the simulated Geo/Geo/1-to-Geo/D/1 occupancy
   ratio stays within 0.95% of 2 (range 1.9835 to 2.0190). Evidence:
   `validation_geo_geo_1.csv`, `validation_factor2.csv`. Strength: full.
3. **VALIDATION.** The full pipeline passes every internal-consistency
   check: flow balance and network occupancy vs lambda*W within 3.4e-7,
   the W = Lq/lambda relation to machine precision (1.5e-16), utilization
   and throughput within 0.11%. Evidence: `validation_pipeline_v3.csv`.
   Strength: full, for accounting consistency; explicitly not a network
   closed form.
4. **STRUCTURAL.** With deterministic S1 = S3 = 2 and pass-through
   batching, the GPU-station queue is exactly zero (22/22 D rows): the
   proof conditions are stated in section 2 (E2-C). Evidence:
   `experiment_e2_pipeline.csv` + `DECISIONS.md` #19. Strength: full,
   under the stated assumptions only.
5. **EXPERIMENTAL.** Service variability at Q3 is expensive at c=1 and
   cheap at c=2: switching Q3 from deterministic to geometric (same mean,
   same arrival stream) adds 6.831 cycles (80.2%) at lambda = 0.45, c=1,
   and only 0.030 cycles at c=2; the premium grows from 2.1% (lambda=0.05)
   to 139.9% (lambda=0.49). Evidence: `experiment_e2_pipeline.csv`.
   Strength: exact within the tested configuration; phrase as "in the
   tested paired-arrival experiments".
6. **EXPERIMENTAL.** In the E3 grid (lambda = 0.3, delta = 0.5), batching
   saturates: tau = 8 has a fill/delay knee between B = 4 and B = 8 (B = 8
   and B = 16 rows identical), tau = 2 is B-invariant from B = 2 on,
   throughput stays within 0.06% of lambda everywhere, and end-to-end delay
   is minimized at B = 1 in this grid. Evidence:
   `experiment_e3_batching.csv`. Strength: observed in the tested grid
   only; explicitly no "optimal B" statement.

## 9. Recommended Phase-3 Report Story

Four pages, in this order, with the recommended figures:

1. **Problem (about half a page).** LLM serving latency is queueing;
   batch size, wait timer, and worker count are the design knobs.
2. **Model (about three quarters of a page).** The three-station network,
   batch-level Q3 semantics, assumptions, stability condition. Reuse the
   TikZ pipeline diagram (as in Phase 2).
3. **Simulator (about half a page).** Cycle-driven fixed-increment engine,
   DES component mapping, deterministic seed. Keep short; Phase 2 covered
   the "how" in depth.
4. **Validation (about one page).** Findings 1 to 3: the formula pair (with
   the S=3 observation in two sentences), the factor-2 relationship, and
   the network consistency checks. Figures: `fig_e1_validation_geo_d_1`
   and `fig_v2_factor2`; the representative-rows table pattern from
   Phase 2, extended with one V3 row.
5. **E2 finding (about three quarters of a page).** Findings 4 and 5: the
   structural zero-queue result (one short paragraph, assumptions stated)
   and the variability premium with the c=2 absorption. Figure:
   `fig_e2_e2e_delay` (add `fig_e2_node_occupancy` only if space allows).
6. **E3 finding (about half a page).** Finding 6: the trade-off table
   pattern, the saturation knee, and the honest B=1-minimum observation
   with the resource-saving side noted. Figure: `fig_e3_batching`.
7. **Limitations (about a quarter page).** Condense section 7 to five or
   six bullet points; every one must map to the implementation.
8. **Conclusion (about a quarter page).** Validated simulator, two
   experimental findings, V4 open pending lectures.

Do not carry the Phase-2 prose forward verbatim; the "what" report should
lead with findings, not methodology.

## 10. Numerical Traceability

Every number in this pack comes from one of: `results/experiment_e2_pipeline.csv`
(sections 2, 4), `results/experiment_e3_batching.csv` (sections 3, 4),
`results/validation_geo_d_1_S2.csv`, `validation_geo_d_1_S3.csv`,
`validation_geo_geo_1.csv`, `validation_factor2.csv`,
`validation_pipeline_v3.csv`, `validation_table.csv` (sections 1, 4, 8),
`configs.py` and `run_e3.py`/`run_experiments.py` constants (grids, seed,
delta, lengths), or course-timeline facts from `PROJECT1_COURSE_MINING_REPORT.md`
and the `Lecture Slides/` folder listing (section 6). All were recomputed
from the CSVs by script during the preparation of this pack. No values are
remembered, rounded from memory, or invented.

Phase 3 evidence pack complete. Final report drafting not started.
