"""run_validation.py -- V1/V2/V3 validation runs and the validation table.

Writes results/*.csv and prints a pass/fail summary. Every number quoted in
course reports must come from these CSVs.

Targets (see DECISIONS.md for the derivation of the S-general ones):
  Geo/D/1  Wq   = rho*(S-1)/(2*(1-rho)), rho = lam*S   [top_script.m, all S]
  Geo/D/1  Lq   = lam*Wq = lam^2*S*(S-1)/(2*(1-lam*S)) [class-code exact]
                = lam^2*(S-1)/(1-lam*S) at S=2         [A1 report formula]
  Geo/Geo/1 Lq  = 2*lam^2/(1-2*lam) (mean service 2)   [A1 Problem 2]

Pass rule: relative error < 1% at 1e7 cycles for lam <= 0.45. lam = 0.49
(rho = 0.98) is a reported-but-informational row: convergence there is known
to need >= 1e8 cycles (A1 measured 8.5% error on Geo/Geo/1 at 1e7, 1% at 1e8).
"""

import csv
import time

import numpy as np

from configs import LAMBDA_SWEEP, SEED, SIM_LENGTHS, geo_d_1, geo_geo_1, \
    pipeline
from network_sim import Network

RESULTS = "results"
PASS_TOL = 0.01


def rel_err(sim, anal):
    if sim == anal:               # covers the 0-vs-0 zero-delay station case
        return 0.0
    return abs(sim - anal) / abs(anal) if anal else float("inf")


def run_net(lam, stations, T, rng):
    net = Network(lam, stations, rng)
    net.run(T)
    return net.metrics(T)


def wq_anal_geo_d_1(lam, S):
    rho = lam * S
    return rho * (S - 1) / (2 * (1 - rho))


def lq_anal_geo_d_1(lam, S):
    return lam * wq_anal_geo_d_1(lam, S)


def lq_anal_a1(lam, S):
    """Assignment 1 report formula: lam^2*(S-1)/(1-lam*S)."""
    return lam * lam * (S - 1) / (1 - lam * S)


def write_csv(path, header, rows):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def validate_geo_d_1(S, rng, table):
    """V1: single-station Geo/D/1 sweep over the course lambda array.

    The sweep is the course array top_script.m uses; it is truncated to
    rho = lam*S < 1, so at S=3 it stops at lam=0.30 (the full array is only
    valid at S=2, where lam=0.49 gives rho=0.98). DECISIONS.md #16."""
    sweep = [lam for lam in LAMBDA_SWEEP if lam * S < 1]
    rows = []
    for T in SIM_LENGTHS:
        for lam in sweep:
            m = run_net(lam, geo_d_1(S), T, rng)["stations"]["Q"]
            wa = wq_anal_geo_d_1(lam, S)
            lc = lq_anal_geo_d_1(lam, S)
            la = lq_anal_a1(lam, S)
            rows.append([T, lam, m["Lq"], lc, la, m["Wq"], wa,
                         m["utilization"], lam * S,
                         rel_err(m["Lq"], lc), rel_err(m["Lq"], la),
                         rel_err(m["Wq"], wa), rel_err(m["utilization"],
                                                       lam * S)])
    write_csv(f"{RESULTS}/validation_geo_d_1_S{S}.csv",
              ["sim_length", "lam", "Lq_sim", "Lq_anal_class", "Lq_anal_a1",
               "Wq_sim", "Wq_anal", "util_sim", "rho_anal",
               "Lq_relerr_class", "Lq_relerr_a1", "Wq_relerr",
               "util_relerr"], rows)
    for r in rows:
        if r[0] == SIM_LENGTHS[-1]:
            T, lam = r[0], r[1]
            status = "pass" if (lam <= 0.45 and r[9] < PASS_TOL) else \
                ("expected-slow" if lam > 0.45 else "FAIL")
            table.append([f"V1 Geo/D/1 S={S} Lq (class-code lam*Wq)", T, lam,
                          r[2], r[3], r[9], status])
            # The A1 report formula lam^2*(S-1)/(1-lam*S) coincides with the
            # class-code result only at S=2 (DECISIONS.md #9); at S=3 its row
            # is kept for the audit but is not a simulator pass/fail.
            if S == 2:
                status = "pass" if (lam <= 0.45 and r[10] < PASS_TOL) else \
                    ("expected-slow" if lam > 0.45 else "FAIL")
            else:
                status = "a1-formula-S2-only"
            table.append([f"V1 Geo/D/1 S={S} Lq (A1 formula)", T, lam,
                          r[2], r[4], r[10], status])
            status = "pass" if (lam <= 0.45 and r[11] < PASS_TOL) else \
                ("expected-slow" if lam > 0.45 else "FAIL")
            table.append([f"V1 Geo/D/1 S={S} Wq (top_script)", T, lam,
                          r[5], r[6], r[11], status])
    return rows


def validate_geo_geo_1(rng, table, d1_rows_max):
    """V2: single-station Geo/Geo/1, mean service 2, plus the factor-2
    relationship against V1's Geo/D/1 S=2 rows at the longest length
    (d1_rows_max: [(lam, Lq_sim)] from validate_geo_d_1(2, ...))."""
    rows = []
    for T in SIM_LENGTHS:
        for lam in LAMBDA_SWEEP:
            m = run_net(lam, geo_geo_1(2), T, rng)["stations"]["Q"]
            la = 2 * lam * lam / (1 - 2 * lam)
            rows.append([T, lam, m["Lq"], la, m["Wq"], la / lam,
                         m["utilization"], rel_err(m["Lq"], la)])
            if T == SIM_LENGTHS[-1]:
                status = "pass" if (lam <= 0.45 and rows[-1][7] < PASS_TOL) \
                    else ("expected-slow" if lam > 0.45 else "FAIL")
                table.append(["V2 Geo/Geo/1 Lq (mean 2)", T, lam,
                              m["Lq"], la, rows[-1][7], status])
    f2_rows = []
    d1 = dict(d1_rows_max)
    for r in rows:
        if r[0] == SIM_LENGTHS[-1]:
            ratio = r[2] / d1[r[1]]
            f2_rows.append([r[1], r[2], d1[r[1]], ratio])
            rel = rel_err(ratio, 2.0)
            status = "pass" if (r[1] <= 0.45 and rel < PASS_TOL) else \
                ("expected-slow" if r[1] > 0.45 else "FAIL")
            table.append(["V2 factor-2 ratio Geo/Geo/1 : Geo/D/1",
                          SIM_LENGTHS[-1], r[1], ratio, 2.0, rel, status])
    write_csv(f"{RESULTS}/validation_geo_geo_1.csv",
              ["sim_length", "lam", "Lq_sim", "Lq_anal", "Wq_sim", "Wq_anal",
               "util_sim", "Lq_relerr"], rows)
    write_csv(f"{RESULTS}/validation_factor2.csv",
              ["lam", "Lq_geo_geo_1_sim", "Lq_geo_d_1_sim", "ratio_sim"],
              f2_rows)


def validate_pipeline_v3(rng, table):
    """V3: full pipeline (pass-through Q2) internal-consistency checks:
    per-node flow balance, utilization vs rho_i, W = Lq/lam per node, and
    network-wide L_total vs lam*W_e2e. No network closed forms are claimed
    (queueing-network theory is taught after Phase-1; see DECISIONS.md)."""
    rows = []
    cases = [(lam, T) for T in SIM_LENGTHS for lam in (0.3,)] + \
            [(lam, SIM_LENGTHS[-1]) for lam in (0.1, 0.49)]
    for (lam, T) in cases:
        cfg = pipeline()
        c3 = cfg[2].c
        m = run_net(lam, cfg, T, rng)
        st = m["stations"]
        net = m["network"]
        rho_q1 = lam * 2.0            # Q1 deterministic S1=2
        rho_q3 = lam * 2.0 / c3       # Q3 geometric mean 2, B=1
        checks = []
        for name in st:
            s = st[name]
            arr, dep = s["lam"], s["throughput"]
            checks.append((f"{name} flow balance", dep / arr if arr else 0.0,
                           1.0))
            if "utilization" in s:
                rho = rho_q1 if name.startswith("Q1") else rho_q3
                checks.append((f"{name} utilization", s["utilization"], rho))
            if arr:
                checks.append((f"{name} W=Lq/lam", s["Lq"] / arr, s["Wq"]))
        checks.append(("network L_total vs lam*W_e2e", net["L_total"],
                       net["lam"] * net["W_e2e_qwait"]))
        checks.append(("network throughput", net["throughput"], lam))
        for (label, sim, anal) in checks:
            e = rel_err(sim, anal)
            ok = e < PASS_TOL
            rows.append([T, lam, label, sim, anal, e, "pass" if ok
                         else ("expected-slow" if lam > 0.45 and T ==
                               SIM_LENGTHS[-1] else "FAIL")])
            if T == SIM_LENGTHS[-1]:
                table.append([f"V3 {label}", T, lam, sim, anal, e,
                              "pass" if ok else
                              ("expected-slow" if lam > 0.45 else "FAIL")])
    write_csv(f"{RESULTS}/validation_pipeline_v3.csv",
              ["sim_length", "lam", "check", "simulated", "target",
               "rel_err", "status"], rows)


def main():
    t0 = time.perf_counter()
    rng = np.random.default_rng(SEED)
    table = []
    print(f"Seed {SEED}; lambda sweep {LAMBDA_SWEEP}; lengths {SIM_LENGTHS}")
    print("V1: Geo/D/1, S=2 ...", flush=True)
    s2_rows = validate_geo_d_1(2, rng, table)
    print("V1: Geo/D/1, S=3 ...", flush=True)
    validate_geo_d_1(3, rng, table)
    print("V2: Geo/Geo/1 mean 2 + factor-2 ...", flush=True)
    d1_max = [(r[1], r[2]) for r in s2_rows if r[0] == SIM_LENGTHS[-1]]
    validate_geo_geo_1(rng, table, d1_max)
    print("V3: pipeline flow balance ...", flush=True)
    validate_pipeline_v3(rng, table)

    write_csv(f"{RESULTS}/validation_table.csv",
              ["check", "sim_length", "lam", "simulated", "analytical",
               "rel_err", "status"], table)
    n_fail = sum(1 for r in table if r[6] == "FAIL")
    n_pass = sum(1 for r in table if r[6] == "pass")
    n_slow = sum(1 for r in table if r[6] == "expected-slow")
    print(f"\nValidation table: {n_pass} pass, {n_slow} expected-slow "
          f"(lam=0.49), {n_fail} FAIL  [{time.perf_counter() - t0:.0f}s]")
    for r in table:
        if r[6] == "FAIL":
            print(f"  FAIL: {r[0]} lam={r[2]} sim={r[3]:.6g} "
                  f"anal={r[4]:.6g} rel={r[5]:.3g}")


if __name__ == "__main__":
    main()
