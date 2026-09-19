# ISSUES.md -- validation discrepancies and their resolution

Rule followed all night: the simulator was never tuned toward a target.
Entries below record every mismatch found, expected vs got, attempts made,
and the resolution.

## 1. V1 S=3: simulated Lq does NOT match the A1 report formula (RESOLVED, formula out of scope)

- **Expected (target as originally specified):** Lq = lam^2*(S-1)/(1-lam*S)
  (Assignment 1 solutions report; also quoted in the Phase-1 statement).
- **Got (1e7 cycles, S=3):** uniformly ~1.5x the formula; ratio
  sim/formula = 1.4974..1.5069 over lam = 0.05..0.30. E.g. lam=0.1:
  simulated 0.04300 vs formula 0.02857.
- **Attempts:** none needed on the code side; no tuning. Instead the target
  itself was re-derived for the class-code slot convention (immediate
  access, occupancy excludes in-service, occupancy snapshot after dispatch):
  the waiting time satisfies the discrete Lindley recursion
  W_{i+1} = max(0, W_i + S - T_{i+1}) with T geometric (one dispatch per
  service period, D_{i+1} = max(D_i + S, A_{i+1})). Its pgf solves in closed
  form: G(z) = (1-lam*S)/(1 - lam*(z^(S-1)+...+1)), so
  E[Wq] = G'(1) = rho*(S-1)/(2*(1-rho)) for ALL S -- exactly the
  course-verbatim top_script.m formula. The occupancy counter counts each
  request once per queued cycle, so Lq = lam*Wq exactly, i.e.
  Lq = lam^2*S*(S-1)/(2*(1-lam*S)). At S=2 this equals the A1 formula
  lam^2*(S-1)/(1-lam*S); at S != 2 the A1 formula differs by the factor S/2.
  A1 only ever verified the formula empirically at S=2 (its CSVs contain no
  S=3 runs), which is consistent with it being S=2-specific.
- **Verification:** (a) the pgf reproduces the S=2 anchor A1 verified to
  <0.1% at 1e8; (b) simulation matches lam*Wq at S=3 to <=0.46% at 1e7
  across the sweep; (c) the same engine matches the course Wq formula at
  both S to <=0.65%.
- **Disposition:** the simulator stands; the A1 Lq formula is recorded as
  S=2-only. Rows are kept in `results/validation_geo_d_1_S3.csv`
  (`Lq_anal_a1`, `Lq_relerr_a1`) and in validation_table.csv with status
  "a1-formula-S2-only" for your audit. Recommendation for Phase-2: quote
  Wq = rho(S-1)/(2(1-rho)) and Lq = lam*Wq as the S-general pair.

## 2. V1 S=3 sweep cannot cover the course array's upper end (RESOLVED, by stability)

- **Expected:** course sweep [0.05:0.05:0.45, 0.49] at S in {2,3}.
- **Got:** Network's stability assert rejects lam >= 1/3 at S=3
  (rho = lam*S >= 1), correctly.
- **Resolution:** S=3 sweep truncated to lam <= 0.30 (rho = 0.90); full
  array retained at S=2 and for V2/E2 (all mean service 2). DECISIONS #14.

## 3. V3 Q2 W = Lq/lam rows reported rel_err = inf on 0 vs 0 (RESOLVED, definition fixed)

- **Expected:** pass-through Q2 has Lq = Wq = 0 by design; the check should
  be trivially satisfied.
- **Got:** first run marked the rows FAIL because rel_err divided by a zero
  target.
- **Resolution:** rel_err returns 0.0 when simulated == target. No
  simulation numbers changed (runs are deterministic; only the status cells
  were regenerated).

## 4. lam=0.49 at 1e7 slightly above the 1% bar (KNOWN, expected, not fixed)

- **Expected (aspirational):** <1% everywhere at 1e7.
- **Got:** 1.09% (Geo/D/1 Lq), 1.05% (Geo/D/1 Wq), 1.57% (Geo/Geo/1 Lq),
  2.63% (factor-2 ratio).
- **Why not "fixed":** rho = 0.98 is critically loaded; convergence at 1e7
  is governed by the long busy periods. A1's own data shows Geo/Geo/1 at
  0.49 is 8.5% off at 1e7 and ~1% at 1e8. Nothing is wrong; the honest
  statement is "1% for lam <= 0.45 at 1e7; 0.49 needs 1e8" (or the C++
  1e8 option from A1 if you ever need it; Python takes ~6-17 s per 1e7 run,
  so 1e8 in Python would be ~10-20 min/run if ever needed).
