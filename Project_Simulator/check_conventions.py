"""check_conventions.py -- repository evidence for the convention claims.

Three small checks, no dependencies beyond numpy. Exits nonzero on any
mismatch. Run:  env -u PYTHONPATH python check_conventions.py

1. Bit-exactness vs the class MATLAB loop. single_queue_simulation_geo_d_1.m
   is transliterated statement-for-statement below and driven with the SAME
   arrival sequence as the engine: the first T variates of the shared seed's
   first 1e6-variate block, tested U <= lam, which is exactly what
   Network.__init__ draws (network_sim.py:237). "Bit-exact" means here:
   identical integer totals of arrivals, occupancy counter and utilization
   counter over identical arrival sequences, hence identical time-average
   Lq and utilization. (The full trajectories are then identical by
   induction over the per-cycle update, which is the same statement map.)
2. Batcher timer corner (DECISIONS #3): B=3, tau=5 with arrivals at cycles
   0 and 1 must release exactly one partial batch at cycle 5, waits 5 and 4.
3. pgf identity (ISSUES #1): the mean of the class-code waiting-time pgf
   G(z) = (1-lam*S)/(1 - lam*(z^(S-1)+...+1)) equals the top_script.m
   formula rho*(S-1)/(2*(1-rho)), checked by numerical differentiation.
"""

import sys

import numpy as np

from configs import SEED, geo_d_1
from network_sim import Batcher, Network


def matlab_geo_d_1_counters(arrivals, service_time):
    """Statement-for-statement transliteration of the class .m loop."""
    occupancy_counter = 0
    num_arrivals = 0
    utilization_counter = 0
    is_server_busy = 0
    current_occupancy = 0
    remaining_service_time = 0
    for a in arrivals:
        if a:                                   # %% arrival routine
            current_occupancy += 1
            num_arrivals += 1
        if is_server_busy == 1:                 # %% service routine
            remaining_service_time -= 1
            if remaining_service_time == 0:
                is_server_busy = 0
        if is_server_busy == 0 and current_occupancy > 0:   # dispatch
            is_server_busy = 1
            current_occupancy -= 1
            remaining_service_time = service_time
        occupancy_counter += current_occupancy  # %% counters
        if is_server_busy == 1:
            utilization_counter += 1
    return num_arrivals, occupancy_counter, utilization_counter


def check_matlab_equivalence():
    failures = 0
    for (S, lam, T) in [(2, 0.3, 200_000), (3, 0.1, 200_000),
                        (2, 0.49, 100_000), (1, 0.2, 100_000)]:
        arrivals = np.random.default_rng(SEED).random(1_000_000)[:T] <= lam
        ref = matlab_geo_d_1_counters(arrivals, S)
        net = Network(lam, geo_d_1(S), np.random.default_rng(SEED))
        net.run(T)
        st = net.stations[0]
        got = (st.n_arrivals, st.occ_counter, st.util_counter)
        ok = got == ref
        failures += not ok
        print(f"1. MATLAB-equivalence S={S} lam={lam} T={T}: "
              f"engine {got} vs translit {ref} -> "
              f"{'PASS (bit-exact counters)' if ok else 'FAIL'}")
    return failures


def check_batcher_timer():
    out = []
    b = Batcher("q", B=3, tau=5)
    b.enqueue_request(0, 0, 0)
    b.enqueue_request(1, 1, 0)
    for cyc in range(6):
        b.step(cyc, lambda c, reqs: out.append((cyc, list(reqs))))
    ok = out == [(5, [(0, 5), (1, 4)])]
    print(f"2. Batcher B=3 tau=5 corner: releases {out} -> "
          f"{'PASS' if ok else 'FAIL'}")
    return not ok


def check_pgf_identity():
    failures = 0
    for (lam, S) in [(0.3, 2), (0.2, 3), (0.1, 3), (0.49, 2)]:
        h = 1e-6
        g = lambda z: (1 - lam * S) / (1 - lam * sum(z ** k
                                                     for k in range(S)))
        gw = (g(1 + h) - g(1 - h)) / (2 * h)
        top = lam * S * (S - 1) / (2 * (1 - lam * S))
        # central difference carries O(h^2) truncation error, steep at small
        # 1-lam*S, so compare with a relative tolerance
        ok = abs(gw - top) < 1e-8 * max(1.0, abs(top))
        failures += not ok
        print(f"3. pgf E[W] lam={lam} S={S}: {gw:.10f} vs top_script "
              f"{top:.10f} -> {'PASS' if ok else 'FAIL'}")
    return failures


if __name__ == "__main__":
    bad = check_matlab_equivalence() + check_batcher_timer() \
        + check_pgf_identity()
    print("check_conventions:", "ALL PASS" if bad == 0
          else f"{bad} FAILURE(S)")
    sys.exit(1 if bad else 0)
