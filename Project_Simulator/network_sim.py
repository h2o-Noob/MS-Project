"""network_sim.py -- cycle-driven (fixed-increment) queueing-network simulator.

E0240 Project 1: an LLM inference serving pipeline modeled as an open
queueing network. One cycle = one scheduler tick. Time advance is
fixed-increment (L2 s11), the same scheme as the class MATLAB code
single_queue_simulation_geo_d_1.m: every cycle runs
arrival -> service countdown -> dispatch -> counters, in that order, with
same-cycle immediate access (a request arriving to an idle server starts
service in its arrival cycle).

Mapping to the discrete-event simulation components (L2 s10):
  System state          : per-station queues, per-server busy flags, remaining
                          service times / per-cycle completion probabilities
  Simulation clock      : the `cycle` variable, advanced in fixed increments
                          of +1 (no event list is needed: in a slotted model
                          every cycle is a tick, L2 s11 fixed-increment)
  Stat. counters        : occupancy counters (time averages), delay sums,
                          utilization counters, throughput counts (L2 s19-23)
  Initialization routine: Network.__init__ (empty queues, zero counters,
                          routing plan, stability check)
  Timing routine        : the fixed-increment loop in Network.run
  Event routine         : ServiceStation.step / Batcher.step, one call per
                          station per cycle
  Library routine       : numpy default_rng uniform draws; Bernoulli arrivals
                          and geometric service via the inverse-transform
                          tests U <= rate and U <= ps (L3 s12)

Stations:
  ServiceStation : c identical FCFS servers. Every queued job is a "group":
                   a list of requests (t_sys, w_so_far) that share one service
                   completion. A singleton group is one request (Q1, or any
                   single-station config); a multi-request group is a batch
                   (Q3). B=1 batching produces singleton groups.
  Batcher        : FCFS release station (Q2), no service. Releases requests
                   as one group when B have collected or the oldest has waited
                   tau cycles, whichever happens first. B=1 or tau=0 makes it
                   a zero-delay pass-through.

Service laws (s_base = cycles for a single request, delta = extra cycles per
extra request in the batch, batch mean = s_base + delta*(b-1)):
  deterministic : exact countdown of ceil(s_base + delta*(b-1)) -> Geo/D/1
  geometric     : per-cycle completion test U <= 1/mean(b) -> Geo/Geo/1

RNG discipline: one numpy Generator is shared by a whole suite of runs
(Assignment 1 convention). Uniform variates are drawn in fixed 1e6-variate
blocks: one arrival block per Network, one service block per geometric
station, refilled in a fixed order, so every suite run is reproducible.
"""

import math
from collections import deque

import numpy as np


class UniformStream:
    """Chunked U(0,1) stream over a numpy Generator (A1 chunking style)."""

    def __init__(self, rng, chunk=1_000_000):
        self._rng = rng
        self._chunk = chunk
        self._buf = rng.random(chunk)
        self._i = 0

    def next(self):
        i = self._i
        if i == self._chunk:
            self._buf = self._rng.random(self._chunk)
            i = 0
        self._i = i + 1
        return self._buf[i]


class ServiceStation:
    """c identical FCFS servers serving queued jobs (singleton or batch)."""

    def __init__(self, name, servers=1, law="deterministic", s_base=2.0,
                 delta=0.0):
        if law not in ("deterministic", "geometric"):
            raise ValueError(f"unknown service law: {law}")
        self.name = name
        self.c = servers
        self.law = law
        self._det = law == "deterministic"
        self.s_base = float(s_base)
        self.delta = float(delta)
        self._stream_next = None      # bound UniformStream.next, set by Network
        self.queue = deque()          # items (t_arr, reqs), reqs=[(t_sys, w)]
        self.remaining = [0] * servers
        self.in_service = [None] * servers  # (reqs, ps) per busy server
        self.busy = 0
        # statistical counters (L2 s19-23 definitions)
        self.occ_counter = 0
        self.util_counter = 0
        self.n_arrivals = 0           # requests
        self.n_departures = 0         # requests
        self.delay_sum = 0            # summed queue waits, in cycles
        self.delay_n = 0              # requests dispatched (delay samples)
        self.batch_fill_sum = 0
        self.batch_count = 0

    def enqueue_group(self, t_arr, reqs):
        self.queue.append((t_arr, reqs))
        self.n_arrivals += len(reqs)

    def step(self, cycle, route):
        """One tick: service countdown -> route completions -> dispatch ->
        counters (class-code order, immediate access)."""
        ins = self.in_service
        out = None
        if self._det:
            rem = self.remaining
            for k in range(self.c):
                r = rem[k]
                if r > 0:
                    rem[k] = r - 1
                    if r == 1:
                        if out is None:
                            out = []
                        out.extend(ins[k][0])
                        ins[k] = None
                        self.busy -= 1
        else:
            nxt = self._stream_next
            for k in range(self.c):
                job = ins[k]
                if job is not None and nxt() <= job[1]:
                    if out is None:
                        out = []
                    out.extend(job[0])
                    ins[k] = None
                    self.busy -= 1
        if out:
            self.n_departures += len(out)
            route(cycle, out)
        # dispatch step: idle servers take the head-of-line job
        q = self.queue
        s_base = self.s_base
        delta = self.delta
        for k in range(self.c):
            if ins[k] is None and q:
                t_arr, reqs = q.popleft()
                w = cycle - t_arr
                b = len(reqs)
                reqs = [(ts, w0 + w) for (ts, w0) in reqs]
                if self._det:
                    self.remaining[k] = int(math.ceil(s_base + delta * (b - 1)))
                    ins[k] = (reqs, 0.0)
                else:
                    ins[k] = (reqs, 1.0 / (s_base + delta * (b - 1)))
                self.delay_sum += w * b
                self.delay_n += b
                self.batch_fill_sum += b
                self.batch_count += 1
                self.busy += 1
        # counter step: time-average occupancy (excludes in-service jobs,
        # class-code convention) and busy-server count
        self.occ_counter += len(q)
        self.util_counter += self.busy
        assert self.occ_counter >= 0


class Batcher:
    """Q2 batching scheduler: release at B collected or tau waited, FCFS.

    The B-check runs first (release exactly B); the timer releases everything
    still queued (a partial batch of size < B). tau is counted from the
    request's arrival at this station; tau=0 or B=1 is a pass-through.
    """

    def __init__(self, name, B=1, tau=0):
        if B < 1 or tau < 0:
            raise ValueError("need B >= 1 and tau >= 0")
        self.name = name
        self.B = B
        self.tau = tau
        self.queue = deque()          # items (t_arr, t_sys, w_so_far)
        self.c = 0                    # holds no server
        self.occ_counter = 0
        self.util_counter = 0
        self.n_arrivals = 0
        self.n_departures = 0
        self.delay_sum = 0
        self.delay_n = 0
        self.batch_fill_sum = 0
        self.batch_count = 0

    def enqueue_request(self, t_arr, t_sys, w):
        self.queue.append((t_arr, t_sys, w))
        self.n_arrivals += 1

    def step(self, cycle, route):
        """One tick: no service; release batches, then counters."""
        q = self.queue
        released = None
        while len(q) >= self.B:
            if released is None:
                released = []
            released.append(
                [q.popleft() for _ in range(self.B)])
        if q and cycle - q[0][0] >= self.tau:
            if released is None:
                released = []
            released.append([q.popleft() for _ in range(len(q))])
        if released:
            for grp in released:
                reqs = []
                for (t_arr, t_sys, w) in grp:
                    waited = cycle - t_arr
                    reqs.append((t_sys, w + waited))
                    self.delay_sum += waited
                self.delay_n += len(grp)
                self.n_departures += len(grp)
                self.batch_fill_sum += len(grp)
                self.batch_count += 1
                route(cycle, reqs)
        self.occ_counter += len(q)
        assert self.occ_counter >= 0


class Network:
    """Open chain of stations; station 0 receives Bernoulli(lam) arrivals,
    the last station is the system exit. Fixed-increment cycle loop."""

    def __init__(self, lam, stations, rng, chunk=1_000_000):
        if not stations:
            raise ValueError("empty topology")
        if not isinstance(stations[0], ServiceStation):
            raise ValueError("entry station must be a ServiceStation")
        if isinstance(stations[-1], Batcher):
            raise ValueError("exit station must be a ServiceStation")
        self.lam = lam
        self.stations = stations
        self._rng = rng
        self._chunk = chunk
        # arrival variates: fixed-size boolean blocks, U <= lam (L3 s12)
        self._arr_flags = rng.random(chunk) <= lam
        self._arr_i = 0
        for st in stations:
            if isinstance(st, ServiceStation) and not st._det:
                st._stream_next = UniformStream(rng, chunk).next
        # stability: rho_i = lambda_i * E[S_i] < 1. Requests are conserved on
        # the single path, so lambda_i = lam. E[S] <= s_base per request
        # (batching with delta <= s_base only lowers per-request work), so
        # lam*s_base/c is exact at B=1 and an upper bound otherwise.
        for st in stations:
            if isinstance(st, ServiceStation):
                rho = lam * st.s_base / st.c
                if rho >= 1:
                    raise ValueError(
                        f"unstable: rho at {st.name} = {rho:.4g} >= 1 "
                        f"(lambda={lam}, E[S]={st.s_base}, c={st.c})")
        # routing plan: one (station, route) pair; route(cycle, requests)
        # sends completed requests downstream or records system exits
        nst = len(stations)
        self._plan = []
        for i, st in enumerate(stations):
            if i + 1 == nst:
                route = self._exit_route
            else:
                nxt = stations[i + 1]
                if isinstance(nxt, Batcher):
                    def route(cycle, done, nxt=nxt):
                        enq = nxt.enqueue_request
                        for (t_sys, w) in done:
                            enq(cycle, t_sys, w)
                else:
                    def route(cycle, done, nxt=nxt):
                        nxt.enqueue_group(cycle, done)
            self._plan.append((st, route))
        self.e2e_sojourn_sum = 0   # arrival at Q1 -> final departure, cycles
        self.e2e_qwait_sum = 0     # summed per-node queue waits only
        self.n_done = 0
        self._cycle0 = 0           # absolute stamp of run() resumptions

    def _exit_route(self, cycle, done):
        for (t_sys, w) in done:
            self.e2e_sojourn_sum += cycle - t_sys
            self.e2e_qwait_sum += w
        self.n_done += len(done)

    def run(self, T):
        flags = self._arr_flags
        fi = self._arr_i
        chunk = self._chunk
        rng = self._rng
        lam = self.lam
        entry = self.stations[0]
        plan = self._plan
        enq = entry.enqueue_group
        c0 = self._cycle0
        for cycle in range(c0, c0 + T):
            # external arrival routine (Bernoulli, L3 s12)
            if fi == chunk:
                flags = rng.random(chunk) <= lam
                fi = 0
            if flags[fi]:
                enq(cycle, ((cycle, 0),))
            fi += 1
            for (st, route) in plan:
                st.step(cycle, route)
        self._arr_flags = flags
        self._arr_i = fi
        self._cycle0 = c0 + T

    def metrics(self, T):
        """Per-station and network metrics, course definitions (L2 s19-23):
        occupancy and utilization are time averages; delay is (sum Di)/n."""
        rows = {"stations": {}, "network": {}}
        l_total = 0.0
        for st in self.stations:
            lq = st.occ_counter / T
            wq = st.delay_sum / st.delay_n if st.delay_n else 0.0
            m = {"lam": st.n_arrivals / T, "Lq": lq, "Wq": wq,
                 "throughput": st.n_departures / T,
                 "mean_batch_fill": (st.batch_fill_sum / st.batch_count
                                     if st.batch_count else 0.0)}
            if isinstance(st, ServiceStation):
                m["utilization"] = st.util_counter / (T * st.c)
            rows["stations"][st.name] = m
            l_total += lq
        net = rows["network"]
        net["lam"] = self.stations[0].n_arrivals / T
        net["L_total"] = l_total
        net["W_e2e_qwait"] = (self.e2e_qwait_sum / self.n_done
                              if self.n_done else 0.0)
        net["W_e2e_sojourn"] = (self.e2e_sojourn_sum / self.n_done
                                if self.n_done else 0.0)
        net["throughput"] = self.n_done / T
        return rows
