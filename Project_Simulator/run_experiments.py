"""run_experiments.py -- E2: pipeline load response.

E2: end-to-end delay and per-node occupancy vs injection rate, comparing
Q3 service deterministic vs geometric (variability effect in a network,
echoing the 2x single-queue result) and c = 1 vs c = 2 workers.

B = 1, tau = 0 (pass-through batching) so the only difference between curves
is the Q3 service law and worker count.

Common random numbers: at each (lam, T) point every config draws from a
fresh Generator seeded identically with [SEED, lam_idx, T], so all four
configs see the SAME Bernoulli arrival stream at Q1 (its first variate
block) and the Geo configs share the Q3 service block. Q1's trajectory is
therefore identical across configs and the end-to-end differences isolate
Q3 exactly.

Known structural result this experiment exposes (see VERIFICATION.md): with
deterministic S1 = S3 = 2, Q1's departure stream is spaced >= 2 cycles
apart, so a 2-cycle Q3 service never queues: Lq_Q3 = 0 exactly on the D
curves. The Geo curves break that regularity -- that contrast IS the
variability effect.

Simulation length 1e6 cycles for the sweep plus 1e7-cycle spot checks at
lam = 0.3 for convergence evidence. E3 (batching trade-off) is Phase-3 work
and is intentionally not here.
"""

import csv
import time

import numpy as np

from configs import LAMBDA_SWEEP, SEED, pipeline
from network_sim import Network

RESULTS = "results"
SWEEP_LENGTH = 1_000_000
SPOT_LENGTHS = [(0.30, 10_000_000)]   # convergence spot checks (lam, T)
CONFIGS = [("deterministic", 1), ("deterministic", 2),
           ("geometric", 1), ("geometric", 2)]


def main():
    t0 = time.perf_counter()
    cases = [(lam, SWEEP_LENGTH) for lam in LAMBDA_SWEEP] + SPOT_LENGTHS
    rows = []
    for (lam_idx, (lam, T)) in enumerate(cases):
        for (law, c) in CONFIGS:
            rng = np.random.default_rng([SEED, lam_idx, T])
            net = Network(lam, pipeline(q3_law=law, c=c), rng)
            net.run(T)
            m = net.metrics(T)
            st, netm = m["stations"], m["network"]
            rows.append([
                f"c{c}-{'D' if law == 'deterministic' else 'Geo'}", law, c,
                T, lam,
                netm["throughput"],
                netm["W_e2e_sojourn"],
                netm["W_e2e_qwait"],
                st["Q1_admission"]["Lq"],
                st["Q2_batcher"]["Lq"],
                st["Q3_gpu"]["Lq"],
                st["Q1_admission"]["utilization"],
                st["Q3_gpu"]["utilization"],
                st["Q3_gpu"]["mean_batch_fill"],
            ])
        print(f"E2 lam={lam} T={T}: 4 configs done", flush=True)
    with open(f"{RESULTS}/experiment_e2_pipeline.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["config", "q3_law", "c", "sim_length", "lam",
                    "throughput", "W_e2e_sojourn", "W_e2e_qwait",
                    "Lq_Q1", "Lq_Q2", "Lq_Q3", "util_Q1", "util_Q3",
                    "mean_batch_fill"])
        w.writerows(rows)

    print(f"\nE2 written: {len(rows)} rows  [{time.perf_counter() - t0:.0f}s]")
    print("lam=0.45, 1e6 cycles (paired arrivals; differences are pure Q3):")
    for r in rows:
        if abs(r[4] - 0.45) < 1e-9 and r[3] == SWEEP_LENGTH:
            print(f"  {r[0]}: W_e2e_sojourn={r[6]:.3f}  Lq_Q3={r[10]:.4f}  "
                  f"util_Q3={r[12]:.4f}")


if __name__ == "__main__":
    main()
