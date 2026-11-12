"""KDE plot of revenue per completed, revenue-bearing order line.

Uses the identical population as the histogram (completed lines with positive
revenue) and writes a presentation-ready PNG to output/charts/.

The KDE is fitted in log10 space because revenue is strictly positive and heavily
right-skewed. Bandwidth uses Silverman's rule of thumb; no SciPy dependency is
required.
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
OUTPUT_PATH = PROJECT_ROOT / "output" / "charts" / "completed_line_revenue_kde.png"

# --- Data: identical population to the histogram -----------------------------
df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
completed = df[df["Order_Status"] == "Completed"]
zero_revenue_count = int((completed["Revenue_CNY"] == 0).sum())
revenue = completed.loc[completed["Revenue_CNY"] > 0, "Revenue_CNY"]

n = len(revenue)
median = revenue.median()
mean = revenue.mean()
log_revenue = np.log10(revenue.to_numpy())

# --- Bandwidth: Silverman's rule of thumb on log10(revenue) ------------------
std_log = log_revenue.std(ddof=1)
iqr_log = np.subtract(*np.percentile(log_revenue, [75, 25]))
bandwidth = 0.9 * min(std_log, iqr_log / 1.34) * n ** (-0.2)

# --- Gaussian KDE evaluated on a log-spaced grid -----------------------------
grid_log = np.linspace(
    log_revenue.min() - 3 * bandwidth,
    log_revenue.max() + 3 * bandwidth,
    1200,
)


def gaussian_kde_log(values: np.ndarray, grid: np.ndarray, h: float) -> np.ndarray:
    """Gaussian KDE for 1-D data evaluated on a grid (chunked for memory)."""
    density = np.zeros_like(grid)
    normalizer = 1.0 / (len(values) * h * np.sqrt(2.0 * np.pi))
    for start in range(0, len(values), 4096):
        z = (grid[:, None] - values[None, start : start + 4096]) / h
        density += np.exp(-0.5 * z * z).sum(axis=1)
    return density * normalizer


density = gaussian_kde_log(log_revenue, grid_log, bandwidth)
grid_revenue = 10.0**grid_log
peak_revenue = grid_revenue[density.argmax()]

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

ax.fill_between(grid_revenue, density, color="#2B6B7A", alpha=0.14, zorder=2)
ax.plot(grid_revenue, density, color="#2B6B7A", linewidth=2.8, zorder=4)

median_line = ax.axvline(
    median, color="#C8553D", linewidth=2.2, linestyle=(0, (5, 3)), zorder=5
)
mean_line = ax.axvline(
    mean, color="#E9A23B", linewidth=2.2, linestyle=(0, (2, 2)), zorder=5
)

ax.set_xscale("log")
ax.set_xlim(3.45, 7320)
ax.set_ylim(0, density.max() * 1.22)

x_ticks = [5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 7000]
ax.set_xticks(x_ticks)
ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:,.0f}"))
ax.xaxis.set_minor_formatter(FuncFormatter(lambda *_: ""))
ax.minorticks_off()

ax.yaxis.set_major_locator(MultipleLocator(0.1))
ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:.1f}"))

ax.grid(axis="y", color="#DCE5E8", linewidth=0.9, zorder=0)
ax.set_axisbelow(True)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
for side in ("left", "bottom"):
    ax.spines[side].set_color("#AEBCC2")
ax.tick_params(axis="both", which="both", length=0, labelsize=10.5)

ax.set_xlabel("Revenue per order line (CNY, log scale)", fontsize=12.5, labelpad=12)
ax.set_ylabel("Probability density (per log10 CNY)", fontsize=12.5, labelpad=12)

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
    "Completed Order-Line Revenue: Smooth Density View",
    fontsize=21,
    fontweight="bold",
    color="#17313A",
    ha="left",
    va="top",
)
fig.text(
    0.078,
    0.902,
    f"{n:,} lines  |  Gaussian KDE on log10 revenue  |  Silverman h = {bandwidth:.3f} "
    f"(≈{10**bandwidth - 1:.0%} smoothing)  |  peak ≈ ¥{peak_revenue:,.0f}",
    fontsize=11.3,
    color="#52656D",
    ha="left",
    va="top",
)

fig.text(
    0.078,
    0.035,
    f"Same population as the histogram: completed lines with revenue > 0. "
    f"Zero-revenue completed lines excluded ({zero_revenue_count:,}). Area under curve = 1.",
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
print(f"Lines plotted: {n:,} | excluded zero-revenue: {zero_revenue_count:,}")
print(f"Silverman bandwidth (log10): {bandwidth:.6f} ({10**bandwidth - 1:.1%} multiplicative)")
print(f"KDE peak: ¥{peak_revenue:,.2f} | Median: ¥{median:,.2f} | Mean: ¥{mean:,.2f}")
