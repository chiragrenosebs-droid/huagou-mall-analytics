"""Histogram of revenue per completed, revenue-bearing order line.

Reads the immutable source CSV, filters to completed lines with positive revenue,
and writes a presentation-ready PNG to output/charts/.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter, MultipleLocator

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "huagou_mall_synthetic_ecommerce.csv"
OUTPUT_PATH = PROJECT_ROOT / "output" / "charts" / "completed_line_revenue_histogram.png"

# --- Data -------------------------------------------------------------------
df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
completed = df[df["Order_Status"] == "Completed"]
zero_revenue_count = int((completed["Revenue_CNY"] == 0).sum())
revenue = completed.loc[completed["Revenue_CNY"] > 0, "Revenue_CNY"]

n = len(revenue)
median = revenue.median()
mean = revenue.mean()
q1, q3 = revenue.quantile([0.25, 0.75])
upper_fence = q3 + 1.5 * (q3 - q1)
outlier_count = int((revenue > upper_fence).sum())

# Logarithmically spaced bins: the data span ~3.5 to ~7,100 CNY and are heavily
# right-skewed. Equal-width bins would collapse most observations into a few bars.
# ~71 bins also matches the Freedman-Diaconis rule applied to log10(revenue).
log_bins = np.logspace(np.log10(revenue.min()), np.log10(revenue.max()), 72)
counts, _ = np.histogram(revenue, bins=log_bins)
max_share = counts.max() / n * 100

# --- Styling ----------------------------------------------------------------
plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
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
fig.subplots_adjust(left=0.078, right=0.975, top=0.845, bottom=0.145)

ax.hist(
    revenue,
    bins=log_bins,
    weights=np.ones(n) / n * 100,
    color="#2B6B7A",
    edgecolor="#FFFFFF",
    linewidth=0.55,
    alpha=0.96,
    zorder=3,
)

median_line = ax.axvline(
    median, color="#C8553D", linewidth=2.3, linestyle=(0, (5, 3)), zorder=5
)
mean_line = ax.axvline(
    mean, color="#E9A23B", linewidth=2.3, linestyle=(0, (2, 2)), zorder=5
)

ax.set_xscale("log")
ax.set_xlim(log_bins[0] * 0.98, log_bins[-1] * 1.03)
ax.set_ylim(0, max_share * 1.45)

x_ticks = [5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 7000]
ax.set_xticks(x_ticks)
ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:,.0f}"))
ax.xaxis.set_minor_formatter(FuncFormatter(lambda *_: ""))
ax.minorticks_off()

ax.yaxis.set_major_locator(MultipleLocator(1))
ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:.0f}%"))

ax.grid(axis="y", color="#DCE5E8", linewidth=0.9, zorder=0)
ax.set_axisbelow(True)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
for side in ("left", "bottom"):
    ax.spines[side].set_color("#AEBCC2")
ax.tick_params(axis="both", which="both", length=0, labelsize=10.5)

ax.set_xlabel("Revenue per order line (CNY, log scale)", fontsize=12.5, labelpad=12)
ax.set_ylabel("Share of completed order lines", fontsize=12.5, labelpad=12)

ax.legend(
    handles=[median_line, mean_line],
    labels=[f"Median  ¥{median:,.0f}", f"Mean  ¥{mean:,.0f}"],
    loc="upper right",
    bbox_to_anchor=(0.985, 0.97),
    frameon=True,
    facecolor="#FFFFFF",
    edgecolor="#D3DDE1",
    framealpha=0.96,
    fontsize=11,
    handlelength=2.4,
    borderpad=0.9,
)

fig.text(
    0.078,
    0.955,
    "Completed Order-Line Revenue Is Strongly Right-Skewed",
    fontsize=21,
    fontweight="bold",
    color="#17313A",
    ha="left",
    va="top",
)
fig.text(
    0.078,
    0.902,
    f"{n:,} completed, revenue-bearing lines  |  median ¥{median:,.2f} vs mean ¥{mean:,.2f}  |  Jan 2024 – Dec 2025",
    fontsize=11.5,
    color="#52656D",
    ha="left",
    va="top",
)

fig.text(
    0.078,
    0.035,
    f"Excludes {zero_revenue_count:,} completed lines with zero revenue. "
    "71 logarithmically spaced bins; x-axis log-scaled; bars show share of lines.",
    fontsize=8.8,
    color="#71838B",
    ha="left",
    va="bottom",
)
fig.text(
    0.975,
    0.035,
    "Source: HuaGou Mall synthetic e-commerce dataset",
    fontsize=8.8,
    color="#71838B",
    ha="right",
    va="bottom",
)

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUTPUT_PATH, dpi=200, facecolor=fig.get_facecolor(), bbox_inches="tight")
plt.close(fig)

print(f"Saved chart: {OUTPUT_PATH}")
print(f"Lines plotted: {n:,}")
print(
    f"Median: ¥{median:,.2f} | Mean: ¥{mean:,.2f} | "
    f"Min: ¥{revenue.min():,.2f} | Max: ¥{revenue.max():,.2f}"
)
print(f"Tukey upper fence: ¥{upper_fence:,.2f} | Lines above: {outlier_count:,}")
print(f"Zero-revenue completed lines excluded: {zero_revenue_count:,}")
