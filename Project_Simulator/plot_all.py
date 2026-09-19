"""plot_all.py -- course-convention figures from results/*.csv.

Conventions (Assignment 1 / class MATLAB style): x = injection rate swept,
y = metric, distinct markers per line, labeled axes with units, grid on,
box on, PDF for LaTeX (PNG alongside for quick viewing).

  fig_e1_validation_geo_d_1.png/.pdf     : E1, S=2 occupancy vs injection
                                           rate, sim lengths vs analytical
  fig_e1_validation_geo_d_1_S3.png/.pdf  : E1 companion panel for S=3
  fig_v2_factor2.png/.pdf                : V2, Geo/D/1 vs Geo/Geo/1 at 1e7
  fig_e2_e2e_delay.png/.pdf              : E2, end-to-end delay vs rate
  fig_e2_q3_occupancy.png/.pdf           : E2, Q3 occupancy vs rate
  fig_e2_node_occupancy.png/.pdf         : E2, per-node occupancy (Q1/Q2/Q3)
  fig_e3_batching.png/.pdf               : E3, delay/throughput/fill vs B
"""

import csv
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESULTS = "results"
FIGURES = "figures"
LENGTH_LABEL = {1_000: "$10^3$ cycles", 100_000: "$10^5$ cycles",
                10_000_000: "$10^7$ cycles"}


def read_csv(path):
    with open(path) as f:
        return list(csv.DictReader(f))


def style_axes(ax, ylabel):
    ax.set_xlabel("Injection Rate (packets/cycle)", fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.grid(True, linestyle="--", alpha=0.6)
    # box on is matplotlib's default (all four spines drawn)


def save(fig, name):
    fig.tight_layout()
    fig.savefig(f"{FIGURES}/{name}.pdf")
    fig.savefig(f"{FIGURES}/{name}.png", dpi=200)
    plt.close(fig)
    print(f"saved {FIGURES}/{name}.pdf")


def plot_e1_validation(S=2):
    rows = read_csv(f"{RESULTS}/validation_geo_d_1_S{S}.csv")
    by_len = defaultdict(list)
    for r in rows:
        by_len[int(r["sim_length"])].append(
            (float(r["lam"]), float(r["Lq_sim"])))
    fig, ax = plt.subplots(figsize=(8, 5.2), dpi=300)
    markers = {1_000: ("o", "--"), 100_000: ("s", "-."),
               10_000_000: ("^", "-")}
    for length in sorted(by_len):
        m, ls = markers[length]
        pts = sorted(by_len[length])
        ax.plot([p[0] for p in pts], [p[1] for p in pts], marker=m,
                linestyle=ls, linewidth=1.8, markersize=7,
                label=f"Sim, {LENGTH_LABEL[length]}")
    anal = sorted((float(r["lam"]), float(r["Lq_anal_class"])) for r in rows
                  if int(r["sim_length"]) == 10_000_000)
    ax.plot([p[0] for p in anal], [p[1] for p in anal], "k:", linewidth=2,
            label="Analytical Geo/D/1")
    ax.set_title(f"E1: Geo/D/1 occupancy vs injection rate (S = {S})",
                 fontsize=12, fontweight="bold")
    style_axes(ax, "Average Queue Occupancy (packets)")
    ax.legend(fontsize=10, loc="upper left")
    save(fig, f"fig_e1_validation_geo_d_1{'' if S == 2 else f'_S{S}'}")


def plot_v2_factor2():
    d1 = [(float(r["lam"]), float(r["Lq_sim"]))
          for r in read_csv(f"{RESULTS}/validation_geo_d_1_S2.csv")
          if int(r["sim_length"]) == 10_000_000]
    g1 = [(float(r["lam"]), float(r["Lq_sim"]))
          for r in read_csv(f"{RESULTS}/validation_geo_geo_1.csv")
          if int(r["sim_length"]) == 10_000_000]
    fig, ax = plt.subplots(figsize=(8, 5.2), dpi=300)
    for pts, mk, color, label in [
            (sorted(d1), "o", "tab:blue", "Geo/D/1 sim (S = 2)"),
            (sorted(g1), "s", "tab:red", "Geo/Geo/1 sim (mean S = 2)")]:
        ax.plot([p[0] for p in pts], [p[1] for p in pts], marker=mk,
                color=color, linewidth=2, markersize=7, label=label)
    la1 = sorted((float(r["lam"]), float(r["Lq_anal"]))
                 for r in read_csv(f"{RESULTS}/validation_geo_geo_1.csv")
                 if int(r["sim_length"]) == 10_000_000)
    ax.plot([p[0] for p in la1], [p[1] / 2 for p in la1], "--",
            color="tab:blue", alpha=0.6, label="Geo/D/1 analytical")
    ax.plot([p[0] for p in la1], [p[1] for p in la1], "--",
            color="tab:red", alpha=0.6, label="Geo/Geo/1 analytical (= 2x)")
    ax.set_title("V2: factor-2 relationship, Geo/D/1 vs Geo/Geo/1 ($10^7$ "
                 "cycles)", fontsize=12, fontweight="bold")
    style_axes(ax, "Average Queue Occupancy (packets)")
    ax.legend(fontsize=10, loc="upper left")
    save(fig, "fig_v2_factor2")


def plot_e2(column, fname, title, ylabel):
    rows = read_csv(f"{RESULTS}/experiment_e2_pipeline.csv")
    fig, ax = plt.subplots(figsize=(8, 5.2), dpi=300)
    styles = {"c1-D": ("o", "tab:blue"), "c1-Geo": ("s", "tab:red"),
              "c2-D": ("^", "tab:green"), "c2-Geo": ("d", "tab:purple")}
    for tag in ("c1-D", "c1-Geo", "c2-D", "c2-Geo"):
        pts = sorted((float(r["lam"]), float(r[column])) for r in rows
                     if r["config"] == tag and int(r["sim_length"]) ==
                     1_000_000)
        m, color = styles[tag]
        ax.plot([p[0] for p in pts], [p[1] for p in pts], marker=m,
                color=color, linewidth=2, markersize=7, label=tag)
    ax.set_title(title, fontsize=12, fontweight="bold")
    style_axes(ax, ylabel)
    ax.legend(fontsize=10, loc="upper left")
    save(fig, fname)


def plot_e2_node_occupancy():
    """Per-node occupancy vs injection rate, one panel per node (E2)."""
    rows = read_csv(f"{RESULTS}/experiment_e2_pipeline.csv")
    styles = {"c1-D": ("o", "tab:blue"), "c1-Geo": ("s", "tab:red"),
              "c2-D": ("^", "tab:green"), "c2-Geo": ("d", "tab:purple")}
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.6), dpi=300, sharey=True)
    for ax, col, node in zip(axes, ("Lq_Q1", "Lq_Q2", "Lq_Q3"),
                             ("Q1 admission (Geo/D/1)", "Q2 batcher "
                              "(pass-through)", "Q3 GPU workers")):
        for tag in ("c1-D", "c1-Geo", "c2-D", "c2-Geo"):
            pts = sorted((float(r["lam"]), float(r[col])) for r in rows
                         if r["config"] == tag
                         and int(r["sim_length"]) == 1_000_000)
            m, color = styles[tag]
            ax.plot([p[0] for p in pts], [p[1] for p in pts], marker=m,
                    color=color, linewidth=2, markersize=6, label=tag)
        ax.set_title(node, fontsize=11)
        style_axes(ax, "Average Queue Occupancy (requests)")
    axes[0].legend(fontsize=9, loc="upper left")
    fig.suptitle("E2: per-node queue occupancy vs injection rate (B = 1, "
                 "$10^6$ cycles)", fontsize=12, fontweight="bold")
    save(fig, "fig_e2_node_occupancy")


def plot_e3():
    """Batching trade-off: delay, throughput and batch fill vs B (E3)."""
    rows = read_csv(f"{RESULTS}/experiment_e3_batching.csv")
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.6), dpi=300)
    tau_style = {2: ("o", "-", "tau = 2 cycles"), 8: ("s", "--",
                                                     "tau = 8 cycles")}
    panels = [("W_e2e_sojourn", "End-to-End Sojourn (cycles/request)"),
              ("throughput", "Throughput (requests/cycle)"),
              ("mean_batch_fill", "Mean Batch Fill (requests/batch)")]
    for ax, (col, ylabel) in zip(axes, panels):
        for tau in (2, 8):
            pts = sorted((float(r["B"]), float(r[col])) for r in rows
                         if int(r["tau"]) == tau
                         and int(r["sim_length"]) == 10_000_000)
            m, ls, label = tau_style[tau]
            ax.plot([p[0] for p in pts], [p[1] for p in pts], marker=m,
                    linestyle=ls, linewidth=2, markersize=7, label=label)
        ax.set_xlabel("Batch Size B (requests)", fontsize=11)
        ax.set_ylabel(ylabel, fontsize=11)
        ax.grid(True, linestyle="--", alpha=0.6)
        ax.set_xticks([1, 2, 4, 8, 16])
    # throughput is flat at lambda here; autoscale on a ~2e-7 range would
    # render seed-level noise as visible swings, so fix the scale
    axes[1].set_ylim(0.0, 0.45)
    axes[0].legend(fontsize=9, loc="lower right")
    fig.suptitle("E3: batching trade-off vs batch size ($\\lambda$ = 0.3, "
                 "$\\delta$ = 0.5, $10^7$ cycles)",
                 fontsize=12, fontweight="bold")
    save(fig, "fig_e3_batching")


def main():
    plot_e1_validation(2)
    plot_e1_validation(3)
    plot_v2_factor2()
    plot_e2("W_e2e_sojourn", "fig_e2_e2e_delay",
            "E2: end-to-end delay vs injection rate (B = 1)",
            "End-to-End Delay (cycles/request)")
    plot_e2("Lq_Q3", "fig_e2_q3_occupancy",
            "E2: GPU-station occupancy vs injection rate (B = 1)",
            "Average Queue Occupancy at Q3 (requests)")
    plot_e2_node_occupancy()
    plot_e3()


if __name__ == "__main__":
    main()
