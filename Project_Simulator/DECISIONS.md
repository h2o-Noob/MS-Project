# DECISIONS.md -- assumptions made during the overnight build (Phases 1-2)

For your morning audit. Each item: what was decided, why, and what to check.
Nothing here tuned the simulator toward any target; validation discrepancies
are in ISSUES.md (one entry, resolved analytically).

1. **Q3 workers serve one BATCH, not one request** (spec conflict resolved).
   The Phase-1 statement says Q3 workers serve "one request"; the overnight
   prompt says "each serving one batch" and E3 needs batch service time
   = ceil(S3 + delta*(B-1)). Implemented: a worker serves one batch; every
   request in the batch shares the batch's service duration and departs when
   it completes. At B=1 (the validation configuration) this reduces exactly
   to the Phase-1 statement's per-request service. Check: agree with this
   framing before the Phase-2 report.

2. **Cycle semantics = class MATLAB code exactly.** Per cycle, per station:
   service countdown -> route completions -> dispatch -> counters, in that
   order, with same-cycle immediate access (a request arriving to an idle
   server starts service in its arrival cycle; occupancy is snapshotted after
   dispatch, excluding in-service requests). Cross-station cascade within one
   cycle: Q1 completions join Q2, Q2 can release, Q3 can start serving the
   batch, all in the same cycle. In the single-station limit this is
   bit-for-bit the class-code order. Check: V1 anchors reproduce A1.

3. **Q2 timer semantics.** tau is counted from a request's arrival at Q2
   (waited = current_cycle - arrival_cycle). The B-check runs first (releases
   exactly B); if the oldest has waited >= tau, EVERYTHING still queued is
   released as one partial batch (size < B). B=1 or tau=0 is a zero-delay
   pass-through. With <= 1 arrival/cycle into Q2 (Q1's output), the queue
   never exceeds B at check time, so "release B" and "release all" coincide
   except on timer firings.

4. **Delay Di = queue wait only** (L2 s15: "Di - Delay in queue of i-th
   customer"): time from joining a node's queue to starting service there.
   End-to-end is reported two ways, both CSV-labeled: W_e2e_qwait (sum of the
   three per-node queue waits, course-consistent) and W_e2e_sojourn (arrival
   at Q1 to final departure, includes service; the user-facing number).
   Check: sojourn - qwait = S1 + E[batch service] in steady state.

5. **Occupancy convention** = class code: time-average of the post-dispatch
   queue length, excluding in-service requests. At Q3 the queue holds
   undispatched batches; occupancy counts the REQUESTS waiting in them.
   Utilization at a c-server station = busy worker-cycles / (T*c).

6. **Batch service laws.** Batch of size b has mean service
   s_base + delta*(b-1) (defaults s_base=2, delta=0 tonight; E3 will set
   delta=0.5). Deterministic law: countdown of ceil(...). Geometric law:
   per-cycle completion test U <= 1/mean(b) (L3 s12 ITT), so duration is
   geometric with support {1,2,...} and mean 1/ps -- identical to A1's
   Problem 2 simulator. delta is a config field (configs.py / Station ctor).

7. **S=3 Geo/D/1 occupancy formula (the one analytical finding).** The A1
   report formula Lq = lam^2*(S-1)/(1-lam*S) coincides with the class-code
   convention only at S=2. For the class-code slot model (immediate access,
   occupancy excludes service) the exact results, derived and verified, are:
   Wq = rho*(S-1)/(2*(1-rho)) for ALL S [this is the course-verbatim
   top_script.m formula], and Lq = lam*Wq = lam^2*S*(S-1)/(2*(1-lam*S))
   [exact, because the occupancy counter counts each request once per queued
   cycle]. Evidence: (a) closed-form waiting-time pgf
   G(z) = (1-lam*S)/(1 - lam*(z^(S-1)+...+1)), E[W] = G'(1) = the top_script
   formula, which reproduces the A1-verified S=2 anchor; (b) simulation
   agrees with it at S=3 to <0.3% at 1e6 cycles and <0.1% at 1e7.
   Recommendation: present Lq = lam*Wq and Wq = rho(S-1)/(2(1-rho)) as the
   S-general pair; flag the A1 Lq formula as S=2-specific in Phase-2.

8. **RNG discipline.** One numpy default_rng(SEED=20260922) shared by all
   runs of a script, in a fixed call order (A1 convention). Uniform variates
   drawn in fixed 1e6-variate blocks (arrival block per Network, one service
   block per geometric station). Runs are exactly reproducible by rerunning
   the script; they are NOT bit-identical to the A1 scripts (different draw
   pattern), only distributionally identical conventions.

9. **lam = 0.49 at 1e7 is informational, not a pass/fail row.** At
   rho = 0.98 convergence is slow; A1's own data shows Geo/Geo/1 at 0.49
   8.5% off at 1e7 and 1% only at 1e8. Pass rule: rel err < 1% for
   lam <= 0.45 at 1e7. A C++ 1e8 option (A1's sim_p1.cpp pattern) exists if
   you ever need 0.49 tighter; Python handled 1e7 comfortably (~6-17 s/run).

10. **Naming:** the W = Lq/lam check is called "the W = Lq/lam relation
    (top_script.m convention)" everywhere. It is NOT named "Little's Law" in
    any deliverable until you confirm the Oct lectures taught it (mining
    report: zero hits for "Little" in course material to date).

11. **Scope held per the hard stop:** no E3 code or runs, no report text, no
    README polish beyond run instructions, Q4 split node not built (it adds
    a routing branch; deferred to Phase 3 with V4), V4 left empty for the
    22/09-01/10 queueing lectures.

12. **Dependencies:** stdlib csv instead of pandas (prompt says "Pure Python
    + numpy + matplotlib only"; A1 used pandas but the prompt wins for new
    code). matplotlib Agg backend (headless-safe).

13. **Seed** = 20260922 (the prompt's example value; it is also the Phase-1
    due date, easy to remember in the report).

14. **V1 sweep truncation at S=3.** The course sweep [0.05:0.05:0.45, 0.49]
    is only valid where rho = lam*S < 1; at S=3 it is truncated to
    lam <= 0.30 (rho = 0.90). The full array is kept at S=2 and for all V2
    (mean service 2) and E2 runs. The stability assert in Network.__init__
    raised this; nothing was tuned to dodge it.

15. **E2 run lengths.** V1/V2/V3 use the full 1e7 (validation bar). E2's
    lambda sweep uses 1e6 cycles per point (40 runs) plus 1e7-cycle spot
    checks at lam=0.3 for all four configs, keeping the suite near the
    10-minute target. If you want the E2 sweep at 1e7, change SWEEP_LENGTH
    in run_experiments.py; ~+12 min.

16. **Engine speed.** Station per-cycle work is merged into one step() call
    with pre-built routing closures (no per-cycle type checks) and Bernoulli
    arrivals are drawn as boolean blocks. Semantics are identical to the
    class-code order (item 2); this is purely an interpreter-overhead win
    (1e7 single-station: 17.1 s -> 6.5 s).

17. **Where the mining report and the prompt conflicted:** nothing material.
    The prompt's {1e3, 1e5, 1e7} length sweep (not A1's {1e2..1e8}) is used;
    the "occupancy_counter/simulation_length" time-average, metric
    definitions, formula set, and plot conventions all follow the mining
    report verbatim.

18. **E2 uses common random numbers (CRN).** At each (lam, T) point all four
    configs reseed a fresh Generator with [SEED, lam_idx, T], so every config
    sees the identical Bernoulli arrival stream at Q1 (and the Geo configs
    share the Q3 service block). Q1's trajectory is then identical across
    configs and end-to-end differences are exactly Q3's effect (no run-to-run
    noise, which without CRN produced an ordering artifact like c2-Geo
    edging out c1-D). V1/V2/V3 keep the plain sequential shared-rng
    convention. This is experiment design, not simulator tuning.

19. **Deterministic-tandem resonance (finding, not a bug).** With
    deterministic S1 = S3 = 2 and pass-through batching, Q1's departure
    stream is provably spaced >= 2 cycles apart (one server completes at
    most one request per completion instant, and the next completion is a
    full service period later), so a 2-cycle Q3 service can never queue:
    Lq_Q3 = Wq_Q3 = 0 EXACTLY on the E2 "D" curves, confirmed empirically
    over 1e7 cycles at every lam. The E2 D-vs-Geo contrast is therefore a
    clean measurement of what service variability does to a downstream
    station on the same arrival stream (c1-Geo pays +6.8 cycles e2e at
    lam=0.45). Worth one sentence in the Phase-2 report; do not mistake the
    zero for dead routing.

Phase 3A additions (2026-09-06):

20. **E3 runs each grid point at BOTH 1e6 and 1e7 cycles** (10 configs x 2
    lengths = 20 rows, ~159 s). The knee claim then carries the course's
    own convergence device; measured, the two lengths agree to <= 0.004
    cycles on end-to-end sojourn across the grid.
21. **E3 CRN seeding = [SEED, T]** per length, shared by all ten (B, tau)
    configs at that length (B and tau deliberately NOT in the seed), so
    every config sees the identical external arrival stream. Same rationale
    as #18.
22. **delta plumbed through configs.pipeline(delta=0.0 default).**
    Config-layer only; the engine is untouched in Phase 3A. The default
    reproduces the validation configuration exactly, proven by regenerating
    all seven pre-existing result CSVs bit-identically after the change.
23. **mean_batch_service is the per-BATCH mean** (busy worker-cycles /
    dispatched batches). A per-request mean service column was tried and
    REMOVED: requests weight batches by size, the counter-derived value is
    neither per-batch nor per-request, and using it in a service-time
    identity produced a spurious 24% residual. The identity check is
    replaced by honest bounds: 4 <= sojourn - qwait <= 2 + ceil(2 +
    delta*(B-1)), which hold on all 20 rows. If a per-request service mean
    is ever needed for a report, it requires one new engine counter (not
    added: no current claim needs it).
24. **The E3 knee is defined as the measured saturation point** of the
    fill/delay curves, decided after running, not assumed. Data: tau=8
    saturates between B=4 and B=8 (B=8 and B=16 rows identical in every
    recorded metric); tau=2 is B-invariant from B=2 on. The observation
    that delay is minimized at B=1 across the grid is recorded as-is; no
    parameter was tuned and no benefit was forced.
25. **Evidence hygiene: Option A taken.** `check_conventions.py` added
    (~120 lines): statement-for-statement transliteration of the class
    MATLAB loop driven with the SAME arrival block as the engine
    (bit-exact = equal integer arrival/occupancy/utilization totals over
    identical sequences, 4 cases incl. S=1 and lam=0.49), the batcher
    timer corner case, and the pgf-vs-top_script identity. Exits nonzero
    on mismatch. Its pgf check uses a 1e-8 RELATIVE tolerance: the central
    difference has O(h^2) truncation error that is steep near rho=1 (an
    absolute 1e-9 tolerance failed at lam=0.49 on truncation alone, not on
    any real discrepancy).
26. **Figure completion choices:** E1 S=3 as a companion figure (existing
    S=2 figure kept, both from the same parametrized function); E2 per-node
    occupancy as one 1x3-panel figure with SHARED y-axis (prevents scale
    exaggeration; Q2's identically-zero panel is shown honestly); E3 as one
    1x3-panel figure (sojourn, throughput, fill) with tau distinguished by
    marker + linestyle, and the throughput panel given a FIXED ylim (0,
    0.45) because autoscale on a ~2e-7 range rendered seed-level noise as
    visible swings.
