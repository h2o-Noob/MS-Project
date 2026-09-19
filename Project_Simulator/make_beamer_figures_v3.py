"""make_beamer_figures_v3.py -- E3 chart for the v3 Beamer deck.

Same frozen CSV data (experiment_e3_batching.csv); only the batching color
changes: tau = 2 stays teal, tau = 8 switches to the deck's indigo batching
accent (semantic consistency with slide rule colors). Vector PDF.

Output: figures/bf3_e3_tradeoff.pdf
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
INDIGO = "#4A4E8F"


def axes_style(ax, xlabel, ylabel):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", color="#E8EAEC", linewidth=0.6)
    ax.set_axisbelow(True)
    ax.set_xlabel(xlabel, fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)


def main():
    with open(os.path.join(RESULTS, "experiment_e3_batching.csv")) as f:
        rows = list(csv.DictReader(f))
    fig, axes = plt.subplots(1, 2, figsize=(5.7, 2.5))
    panels = [("W_e2e_sojourn", "Sojourn (cycles/request)"),
              ("mean_batch_fill", "Mean batch fill (requests)")]
    for ax, (col, ylabel) in zip(axes, panels):
        for tau, color, mk, ls, lab in [
                (2, TEAL, "o", "-", "$\\tau$ = 2 cycles"),
                (8, INDIGO, "s", "--", "$\\tau$ = 8 cycles")]:
            pts = sorted((float(r["B"]), float(r[col])) for r in rows
                         if int(r["tau"]) == tau
                         and int(r["sim_length"]) == 10_000_000)
            ax.plot([p[0] for p in pts], [p[1] for p in pts], color=color,
                    marker=mk, linestyle=ls, linewidth=1.8, markersize=5.5,
                    label=lab)
        ax.set_xticks([1, 2, 4, 8, 16])
        ax.legend(fontsize=9, frameon=False, loc="lower right",
                  handlelength=1.6, borderpad=0.1, labelspacing=0.25)
        axes_style(ax, "Batch size $B$ (requests)", ylabel)
    fig.subplots_adjust(left=0.09, bottom=0.24, right=0.99, top=0.96,
                        wspace=0.34)
    fig.savefig(os.path.join("figures", "bf3_e3_tradeoff.pdf"),
                facecolor="white")
    plt.close(fig)
    print("saved figures/bf3_e3_tradeoff.pdf")


if __name__ == "__main__":
    main()
