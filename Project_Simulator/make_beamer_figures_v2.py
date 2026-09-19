"""make_beamer_figures_v2.py -- Beamer v2 charts (semantic colors, 1:1 sizes).

Same frozen CSV data as every other figure script; only styling differs.
Semantic palette (matches the deck): teal = deterministic/reference/tau=2,
brick = geometric/variability/tau=8, gray = secondary references, light gray
= short-run curves. Each chart is drawn at the exact physical size it is
placed on the slide (see phase3_presentation_beamer_v2.tex), so figure text
renders at its drawn point size. Vector PDF output.

Outputs: figures/bf2_e1_convergence.pdf, bf2_e2_delay.pdf, bf2_e3_tradeoff.pdf
"""

import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESULTS = "results"
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.edgecolor": "#43484D",
    "axes.linewidth": 0.8,
    "axes.labelcolor": "#1A1A1A",
    "xtick.color": "#43484D",
    "ytick.color": "#43484D",
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
})

TEAL = "#14606B"
BRICK = "#A8492E"
GRAY = "#7A7A7A"
LIGHT = "#B9C4CC"
BRICK_LT = "#C98A74"


def axes_style(ax, xlabel, ylabel):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", color="#E8EAEC", linewidth=0.6)
    ax.set_axisbelow(True)
    ax.set_xlabel(xlabel, fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)


def rd(path):
    with open(os.path.join(RESULTS, path)) as f:
        return list(csv.DictReader(f))


def save(fig, name):
    fig.savefig(os.path.join("figures", f"{name}.pdf"), facecolor="white")
    plt.close(fig)
    print(f"saved figures/{name}.pdf")


def e1():
    rows = rd("validation_geo_d_1_S2.csv")
    by_len = {1_000: [], 100_000: [], 10_000_000: []}
    for r in rows:
        by_len[int(r["sim_length"])].append(
            (float(r["lam"]), float(r["Lq_sim"])))
    fig, ax = plt.subplots(figsize=(3.0, 2.15))
    for length, color, mk, ls, lab in [
            (1_000, LIGHT, "o", "--", "10$^3$ cycles"),
            (100_000, GRAY, "s", "-.", "10$^5$ cycles"),
            (10_000_000, TEAL, "^", "-", "10$^7$ cycles")]:
        pts = sorted(by_len[length])
        ax.plot([p[0] for p in pts], [p[1] for p in pts], color=color,
                marker=mk, linestyle=ls, linewidth=1.6, markersize=4.5,
                label=lab)
    anal = sorted((float(r["lam"]), float(r["Lq_anal_class"])) for r in rows
                  if int(r["sim_length"]) == 10_000_000)
    ax.plot([p[0] for p in anal], [p[1] for p in anal], color="#1A1A1A",
            linestyle=":", linewidth=1.8, label="analytical")
    ax.legend(fontsize=8, frameon=False, loc="upper left", handlelength=1.5,
              borderpad=0.1, labelspacing=0.25)
    axes_style(ax, "Injection rate (packets/cycle)",
               "Average occupancy $L_q$")
    fig.subplots_adjust(left=0.15, bottom=0.245, right=0.98, top=0.97)
    save(fig, "bf2_e1_convergence")


def e2():
    rows = rd("experiment_e2_pipeline.csv")
    fig, ax = plt.subplots(figsize=(4.15, 2.5))
    for tag, color, mk, ls, lw, lab in [
            ("c1-D", TEAL, "o", "-", 1.9, "c=1, deterministic"),
            ("c1-Geo", BRICK, "s", "-", 1.9, "c=1, geometric"),
            ("c2-D", GRAY, "^", "--", 1.3, "c=2, deterministic"),
            ("c2-Geo", BRICK_LT, "d", "--", 1.3, "c=2, geometric")]:
        pts = sorted((float(r["lam"]), float(r["W_e2e_sojourn"])) for r in rows
                     if r["config"] == tag
                     and int(r["sim_length"]) == 1_000_000)
        ax.plot([p[0] for p in pts], [p[1] for p in pts], color=color,
                marker=mk, linestyle=ls, linewidth=lw, markersize=5,
                label=lab)
    # variability gap marker at the quoted load
    ax.axvline(0.45, color="#C8CDD2", linewidth=0.9, linestyle=(0, (2, 2)))
    ax.annotate("gap at \u03bb = 0.45", xy=(0.45, 11.9),
                xytext=(0.13, 14.5), fontsize=9.5, color="#3D434A",
                arrowprops=dict(arrowstyle="-", color="#B0B6BC", lw=0.8))
    ax.legend(fontsize=8.5, frameon=False, loc="upper left", handlelength=1.5,
              borderpad=0.1, labelspacing=0.25)
    axes_style(ax, "Injection rate $\\lambda$ (packets/cycle)",
               "Sojourn (cycles/request)")
    fig.subplots_adjust(left=0.135, bottom=0.21, right=0.985, top=0.97)
    save(fig, "bf2_e2_delay")


def e3():
    rows = rd("experiment_e3_batching.csv")
    fig, axes = plt.subplots(1, 2, figsize=(5.2, 2.35))
    panels = [("W_e2e_sojourn", "Sojourn (cycles/request)"),
              ("mean_batch_fill", "Mean batch fill (requests)")]
    for ax, (col, ylabel) in zip(axes, panels):
        for tau, color, mk, ls, lab in [
                (2, TEAL, "o", "-", "$\\tau$ = 2 cycles"),
                (8, BRICK, "s", "--", "$\\tau$ = 8 cycles")]:
            pts = sorted((float(r["B"]), float(r[col])) for r in rows
                         if int(r["tau"]) == tau
                         and int(r["sim_length"]) == 10_000_000)
            ax.plot([p[0] for p in pts], [p[1] for p in pts], color=color,
                    marker=mk, linestyle=ls, linewidth=1.9, markersize=5.5,
                    label=lab)
        ax.set_xticks([1, 2, 4, 8, 16])
        ax.legend(fontsize=8.5, frameon=False, loc="lower right",
                  handlelength=1.5, borderpad=0.1, labelspacing=0.25)
        axes_style(ax, "Batch size $B$ (requests)", ylabel)
    axes[1].set_ylim(0.9, 3.8)
    fig.subplots_adjust(left=0.085, bottom=0.235, right=0.99, top=0.96,
                        wspace=0.33)
    save(fig, "bf2_e3_tradeoff")


if __name__ == "__main__":
    e1()
    e2()
    e3()
