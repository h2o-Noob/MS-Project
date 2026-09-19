"""run_e3.py -- E3: batching trade-off.

Grid: B in {1, 2, 4, 8, 16} x tau in {2, 8} at lambda = 0.3, with batch
service gain delta = E3_DELTA (configurable here / via configs): a batch of
size b is served by one worker in ceil(S3 + delta*(b-1)) cycles
(deterministic law, per the E3 specification).

Each grid point runs at BOTH 1e6 and 1e7 cycles (the course
simulation-length device: the knee must survive the longer run). Common
random numbers: every config at a given length reseeds a fresh Generator
with [SEED, T], so all ten configs at that length see the identical
Bernoulli external arrival stream; config-to-config differences are the
batching effect, not arrival noise.

Metrics are the existing course/project definitions; request-level and
batch-level columns are named explicitly. mean_batch_service is the
per-batch mean service duration (busy worker-cycles / dispatched batches).
A per-REQUEST mean service is intentionally NOT emitted: requests weight
batches by size, so it is not derivable from the existing counters and the
per-batch value must not be used in its place (that mismatch produced a
spurious 24% identity residual in the first draft).

Sanity bounds checked after the run (see VERIFICATION.md), per row:
4 <= W_e2e_sojourn - W_e2e_qwait <= 2 + ceil(2 + delta*(B-1)). The lower
bound is S1 + the minimum batch duration (2); the upper is S1 + the
duration of a full-B batch. Sojourn minus summed queue waits IS the
request's total service time, which lies between those durations.
"""

import csv
import time

import numpy as np

from configs import SEED, pipeline
from network_sim import Network

RESULTS = "results"
E3_LAMBDA = 0.3
E3_BS = [1, 2, 4, 8, 16]
E3_TAUS = [2, 8]
E3_DELTA = 0.5          # batching service gain; configurable
E3_LENGTHS = [1_000_000, 10_000_000]


def main():
    t0 = time.perf_counter()
    rows = []
    for T in E3_LENGTHS:
        for B in E3_BS:
            for tau in E3_TAUS:
                rng = np.random.default_rng([SEED, T])
                net = Network(E3_LAMBDA, pipeline(
                    q3_law="deterministic", B=B, tau=tau, delta=E3_DELTA),
                    rng)
                net.run(T)
                m = net.metrics(T)
                st, netm = m["stations"], m["network"]
                q3 = st["Q3_gpu"]
                batch_rate = q3["throughput"] / q3["mean_batch_fill"] \
                    if q3["mean_batch_fill"] else 0.0
                # per-batch mean service duration from existing counters:
                # busy worker-cycles / dispatched batches
                mean_service = q3["utilization"] * 1.0 / batch_rate \
                    if batch_rate else 0.0
                rows.append([
                    B, tau, E3_LAMBDA, E3_DELTA, 2.0, T, SEED,
                    netm["throughput"],
                    batch_rate,
                    netm["W_e2e_sojourn"],
                    netm["W_e2e_qwait"],
                    st["Q1_admission"]["Lq"], st["Q2_batcher"]["Lq"],
                    q3["Lq"],
                    st["Q1_admission"]["utilization"], q3["utilization"],
                    q3["mean_batch_fill"],
                    mean_service,
                ])
            print(f"E3 T={T} B={B}: tau {E3_TAUS} done", flush=True)
    with open(f"{RESULTS}/experiment_e3_batching.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["B", "tau", "lam", "delta", "s_base", "sim_length",
                    "seed", "throughput", "batch_rate", "W_e2e_sojourn",
                    "W_e2e_qwait", "Lq_Q1", "Lq_Q2", "Lq_Q3", "util_Q1",
                    "util_Q3", "mean_batch_fill", "mean_batch_service"])
        w.writerows(rows)

    print(f"\nE3 written: {len(rows)} rows  "
          f"[{time.perf_counter() - t0:.0f}s]")
    print("sanity bounds (all rows): 4 <= sojourn-qwait <= "
          "2+ceil(2+delta*(B-1)); throughput = lam; 1 <= fill <= B")
    import math
    for r in rows:
        svc = r[9] - r[10]
        assert 4.0 - 1e-9 <= svc <= 2.0 + math.ceil(2.0 + r[3] * (r[0] - 1)) \
            + 1e-9, r
        assert 1.0 <= r[16] <= r[0] + 1e-9, r
        assert abs(r[7] - E3_LAMBDA) < 0.01 * E3_LAMBDA, r
    print("all row bounds hold")


if __name__ == "__main__":
    main()
