"""Scatter plot of discount percentage versus profit per completed order line.

Uses completed order lines with positive revenue. The y-axis uses a symlog scale so
the dense low-profit region, negative losses, and the high-profit tail are all legible.
Point transparency addresses overplotting; binned medians and IQR bands summarise the
trend without hiding the raw lines.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "huagou_mall_synthetic_ecommerce.csv"
OUTPUT_PATH = PROJECT_ROOT / "output" / "charts" / "discount_vs_profit_scatter.png"

# --- Data: completed, revenue-bearing order lines ----------------------------
df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
completed = df[df["Order_Status"] == "Completed"]
zero_revenue_count = int((completed["Revenue_CNY"] == 0).sum())
base = completed.loc[
    completed["Revenue_CNY"] > 0, ["Discount_Percentage", "Profit_CNY"]
].copy()

# --- Binned summaries: 5-point discount bins with enough lines ---------------
bin_edges = np.arange(0, 70, 5)
base["bin"] = pd.cut(
    base["Discount_Percentage"], bin_edges, right=False, include_lowest=True
)
grouped = base.groupby("bin", observed=True)["Profit_CNY"]
bins = pd.DataFrame(
    {
        "n": grouped.size(),
        "median": grouped.median(),
        "q25": grouped.quantile(0.25),
        "q75": grouped.quantile(0.75),
    }
).reset_index()
bins["centre"] = bins["bin"].apply(lambda interval: interval.mid).astype(float)
bins = bins[bins["n"] >= 30].reset_index(drop=True)

profit_median = base["Profit_CNY"].median()
negative_count = int((base["Profit_CNY"] < 0).sum())
pearson = base["Discount_Percentage"].corr(base["Profit_CNY"])
spearman = base["Discount_Percentage"].rank().corr(base["Profit_CNY"].rank())
max_point = base.loc[base["Profit_CNY"].idxmax()]
min_point = base.loc[base["Profit_CNY"].idxmin()]

# --- Styling ----------------------------------------------------------------
plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Microsoft YaHei", "DejaVu Sans"],
        "axes.unicode_minus": False,
        "axes.edgecolor": "#B9C6CB",
        "axes.labelcolor": "#1B2A33",
        "text.color": "#1B2A33",
        "xtick.color": "#42545C",
        "ytick.color": "#42545C",
        "figure.facecolor": "#FFFFFF",
        "axes.facecolor": "#FFFFFF",
    }
)

fig, ax = plt.subplots(figsize=(14, 8.5), dpi=200)
fig.subplots_adjust(left=0.095, right=0.975, top=0.845, bottom=0.155)

ax.grid(axis="both", color="#DCE5E8", linewidth=0.9, zorder=0)
ax.set_axisbelow(True)

ax.axhline(0, color="#6B7F88", linewidth=1.25, linestyle=(0, (3, 3)), zorder=1)

# Raw lines: small, semi-transparent markers keep the dense core readable while
# still letting isolated high-profit and loss outliers show through.
ax.scatter(
    base["Discount_Percentage"],
    base["Profit_CNY"],
    s=7.5,
    color="#2B6B7A",
    alpha=0.16,
    edgecolors="none",
    rasterized=True,
    zorder=2,
)

# Interquartile band and median line from the 5-point bins.
ax.fill_between(
    bins["centre"],
    bins["q25"],
    bins["q75"],
    color="#E9A23B",
    alpha=0.24,
    linewidth=0,
    zorder=3,
)
ax.plot(
    bins["centre"],
    bins["median"],
    color="#C77A1E",
    linewidth=2.4,
    marker="o",
    markersize=5.0,
    markerfacecolor="#E9A23B",
    markeredgecolor="#FFFFFF",
    markeredgewidth=1.0,
    zorder=4,
)

ax.set_xlim(0, 66)
ax.set_ylim(-1100, 3000)
ax.set_xscale("linear")
ax.set_yscale("symlog", linthresh=50, linscale=1.0, base=10)

x_ticks = [0, 10, 20, 30, 40, 50, 60]
ax.set_xticks(x_ticks)
ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:.0f}"))
ax.xaxis.set_minor_formatter(FuncFormatter(lambda *_: ""))
ax.minorticks_off()
ax.tick_params(axis="x", which="both", length=0, labelsize=10.8)
ax.tick_params(axis="y", which="both", length=0, labelsize=10.5)

y_ticks = [-500, -100, -50, 0, 50, 100, 250, 500, 1000, 2500]
ax.set_yticks(y_ticks)
ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:,.0f}"))
ax.yaxis.set_minor_formatter(FuncFormatter(lambda *_: ""))
ax.minorticks_off()

for side in ("top", "right"):
    ax.spines[side].set_visible(False)
for side in ("left", "bottom"):
    ax.spines[side].set_color("#AEBCC2")

ax.set_xlabel("Discount percentage (%)", fontsize=12.5, labelpad=12)
ax.set_ylabel("Profit per completed order line (CNY, symlog scale)", fontsize=12.5, labelpad=10)

# --- Extreme points ----------------------------------------------------------
ax.annotate(
    f"Max profit  ¥{max_point['Profit_CNY']:,.0f}\n"
    f"{max_point['Discount_Percentage']:.1f}% discount",
    xy=(max_point["Discount_Percentage"], max_point["Profit_CNY"]),
    xytext=(13, 2550),
    fontsize=9.0,
    color="#42545C",
    ha="left",
    va="center",
    arrowprops={"arrowstyle": "-", "color": "#8A9BA2", "linewidth": 0.9},
    bbox={"facecolor": "#FFFFFF", "edgecolor": "none", "alpha": 0.88, "pad": 2.0},
    zorder=6,
)
ax.annotate(
    f"Max loss  −¥{abs(min_point['Profit_CNY']):,.0f}\n"
    f"{min_point['Discount_Percentage']:.1f}% discount",
    xy=(min_point["Discount_Percentage"], min_point["Profit_CNY"]),
    xytext=(53, -760),
    fontsize=9.0,
    color="#42545C",
    ha="left",
    va="center",
    arrowprops={"arrowstyle": "-", "color": "#8A9BA2", "linewidth": 0.9},
    bbox={"facecolor": "#FFFFFF", "edgecolor": "none", "alpha": 0.88, "pad": 2.0},
    zorder=6,
)

# --- Legend ------------------------------------------------------------------
legend_handles = [
    Line2D(
        [0],
        [0],
        marker="o",
        color="none",
        markerfacecolor="#2B6B7A",
        markeredgecolor="none",
        markersize=6.0,
        alpha=0.45,
        label="Completed order line",
    ),
    Line2D(
        [0],
        [0],
        color="#C77A1E",
        linewidth=2.4,
        marker="o",
        markerfacecolor="#E9A23B",
        markeredgecolor="#FFFFFF",
        markersize=5.0,
        label="Median profit (5-point bins)",
    ),
    Patch(facecolor="#E9A23B", alpha=0.24, edgecolor="none", label="Interquartile range"),
    Line2D(
        [0],
        [0],
        color="#6B7F88",
        linewidth=1.25,
        linestyle=(0, (3, 3)),
        label="Break-even (¥0)",
    ),
]
ax.legend(
    handles=legend_handles,
    loc="upper right",
    bbox_to_anchor=(0.985, 0.975),
    frameon=True,
    facecolor="#FFFFFF",
    edgecolor="#DCE5E8",
    framealpha=0.94,
    fontsize=10.0,
    handlelength=2.2,
    labelspacing=0.85,
)

# --- Titles and notes --------------------------------------------------------
fig.text(
    0.06,
    0.955,
    "Higher Discounts Come with Lower, More Compressed Profit",
    fontsize=21,
    fontweight="bold",
    color="#17313A",
    ha="left",
    va="top",
)
fig.text(
    0.06,
    0.902,
    f"Completed, revenue-bearing order lines  |  n = {len(base):,}  |  "
    "darker areas = more overlapping lines  |  y-axis symlog (linear within ±¥50)",
    fontsize=11.3,
    color="#52656D",
    ha="left",
    va="top",
)

fig.text(
    0.06,
    0.055,
    "Amber line = median profit per 5-percentage-point discount bin (bins with n ≥ 30); "
    "shaded band = interquartile range; dashed line = break-even.",
    fontsize=8.6,
    color="#71838B",
    ha="left",
    va="bottom",
)
fig.text(
    0.06,
    0.028,
    f"Zero-revenue completed lines excluded (n = {zero_revenue_count:,}, all with Profit_CNY = 0). "
    "Symlog compresses the axis beyond ±¥50.",
    fontsize=8.6,
    color="#71838B",
    ha="left",
    va="bottom",
)
fig.text(
    0.975,
    0.028,
    "Source: HuaGou Mall synthetic e-commerce dataset",
    fontsize=8.6,
    color="#71838B",
    ha="right",
    va="bottom",
)

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUTPUT_PATH, dpi=200, facecolor=fig.get_facecolor(), bbox_inches="tight")
plt.close(fig)

print(f"Saved chart: {OUTPUT_PATH}")
print(f"Lines: {len(base):,} | median profit: ¥{profit_median:,.2f} | negative: {negative_count:,}")
print(f"Pearson r: {pearson:.3f} | Spearman rho: {spearman:.3f}")
print(f"Max profit: ¥{max_point['Profit_CNY']:,.2f} at {max_point['Discount_Percentage']:.1f}%")
print(f"Max loss:   ¥{min_point['Profit_CNY']:,.2f} at {min_point['Discount_Percentage']:.1f}%")
print("\nBinned medians:")
for row in bins.itertuples():
    print(
        f"{row.bin}: n={row.n:,}, median=¥{row.median:,.2f}, "
        f"Q1=¥{row.q25:,.2f}, Q3=¥{row.q75:,.2f}"
    )
