"""configs.py -- seed, sweep arrays and topology builders.

All validation anchors reproduce Assignment 1 exactly in the single-station
limit: the same engine, one ServiceStation, Bernoulli(lam) arrivals.
"""

from network_sim import Batcher, ServiceStation

SEED = 20260922
# course sweep array, verbatim from top_script.m
LAMBDA_SWEEP = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.49]
# course convergence device: simulation-length sweep (A1 used 1e2..1e8)
SIM_LENGTHS = [1_000, 100_000, 10_000_000]

# pipeline defaults (Phase-1 statement Table 1, validation configuration)
S1 = 2.0        # Q1 deterministic tokenizer service, cycles
S3 = 2.0        # Q3 per-batch service mean base, cycles


def geo_d_1(S=S1):
    """Single Geo/D/1 station (validation anchor, A1 Problem 1)."""
    return [ServiceStation("Q", servers=1, law="deterministic", s_base=S)]


def geo_geo_1(mean=S3):
    """Single Geo/Geo/1 station, geometric service of given mean (A1 P2)."""
    return [ServiceStation("Q", servers=1, law="geometric", s_base=mean)]


def pipeline(q3_law="geometric", c=1, B=1, tau=0, delta=0.0):
    """Q1 admission/tokenize -> Q2 batching scheduler -> Q3 GPU workers.

    Defaults B=1, tau=0 make Q2 a pass-through: the validation configuration
    where the chain must behave like a tandem of single-server stations.
    delta is the batching service gain at Q3: a batch of size b then has
    service law base S3 + delta*(b-1) (deterministic law: duration
    ceil(S3 + delta*(b-1)); geometric law: that mean). delta=0 (default)
    reproduces the validation configuration exactly."""
    return [
        ServiceStation("Q1_admission", servers=1, law="deterministic",
                       s_base=S1),
        Batcher("Q2_batcher", B=B, tau=tau),
        ServiceStation("Q3_gpu", servers=c, law=q3_law, s_base=S3,
                       delta=delta),
    ]
