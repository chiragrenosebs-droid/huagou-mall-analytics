"""Violin plot of completed order-line revenue by product category.

Compares Revenue_CNY across the eight product categories for completed lines with
positive revenue. Categories are sorted by median revenue (highest at the top).
Densities are estimated in log10 revenue space with a NumPy Gaussian KDE, so the
violin shapes respect the positive, right-skewed nature of revenue.
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
OUTPUT_PATH = PROJECT_ROOT / "output" / "charts" / "category_revenue_violin.png"

CATEGORY_LABELS = {
    "运动户外": "运动户外   Sports & Outdoors",
    "数码电子": "数码电子   Digital Electronics",
    "服饰鞋包": "服饰鞋包   Fashion & Bags",
    "美妆个护": "美妆个护   Beauty & Personal Care",
    "食品饮料": "食品饮料   Food & Beverages",
    "母婴用品": "母婴用品   Mother & Baby",
    "家居生活": "家居生活   Home & Living",
    "图书文具": "图书文具   Books & Stationery",
}

# --- Data: same population as the previous revenue charts --------------------
df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
completed = df[df["Order_Status"] == "Completed"]
zero_revenue_count = int((completed["Revenue_CNY"] == 0).sum())
base = completed.loc[completed["Revenue_CNY"] > 0, ["Category", "Revenue_CNY"]].copy()

overall_median = base["Revenue_CNY"].median()
total_n = len(base)


# --- Gaussian KDE in log10 revenue space -------------------------------------
def gaussian_kde_log(values, grid):
    """Silverman-bandwidth Gaussian KDE evaluated on a fixed log10 grid."""
    n = values.size
    std = values.std(ddof=1)
    iqr = np.subtract(*np.percentile(values, [75, 25]))
    bandwidth = 0.9 * min(std, iqr / 1.34) * n ** (-0.2)

    density = np.zeros_like(grid)
    normaliser = 1.0 / (n * bandwidth * np.sqrt(2 * np.pi))
    for start in range(0, n, 4096):
        block = (grid[:, None] - values[None, start : start + 4096]) / bandwidth
        density += np.exp(-0.5 * block * block).sum(axis=1)
    return density * normaliser, bandwidth


records = []
max_density = 0.0
for category, values in base.groupby("Category")["Revenue_CNY"]:
    log_values = np.log10(values.to_numpy())
    grid = np.linspace(log_values.min(), log_values.max(), 2000)
    density, bandwidth = gaussian_kde_log(log_values, grid)

    records.append(
        {
            "category": category,
            "n": len(values),
            "median": values.median(),
            "q1": values.quantile(0.25),
            "q3": values.quantile(0.75),
            "grid": grid,
            "density": density,
            "bandwidth": bandwidth,
        }
    )
    max_density = max(max_density, float(density.max()))

summary = pd.DataFrame(records).sort_values("median", ascending=False).reset_index(drop=True)
positions = np.arange(len(summary))[::-1]
max_half_width = 0.34

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
        "ytick.color": "#1B2A33",
        "figure.facecolor": "#FFFFFF",
        "axes.facecolor": "#FFFFFF",
    }
)

fig, ax = plt.subplots(figsize=(14, 8.5), dpi=200)
fig.subplots_adjust(left=0.245, right=0.835, top=0.835, bottom=0.155)

for i, position in enumerate(positions):
    if i % 2 == 0:
        ax.axhspan(position - 0.5, position + 0.5, color="#F5F8F9", zorder=0)

ax.axvline(
    overall_median,
    color="#6B7F88",
    linewidth=1.25,
    linestyle=(0, (3, 3)),
    zorder=1,
)

for position, row in zip(positions, summary.itertuples()):
    width = row.density / max_density * max_half_width
    width[0] = width[-1] = 0.0  # close the outline at the observed extremes
    revenue = 10.0 ** row.grid

    ax.fill_between(
        revenue,
        position - width,
        position + width,
        facecolor="#2B6B7A",
        edgecolor="#1F4E5F",
        linewidth=0.9,
        alpha=0.55,
        zorder=2,
    )
    ax.plot(
        revenue,
        np.full(revenue.size, position),
        color="#1F4E5F",
        linewidth=0.6,
        alpha=0.28,
        zorder=2,
    )

    # Quartile span and median marker, drawn on top of the density shape.
    ax.plot(
        [row.q1, row.q3],
        [position, position],
        color="#17313A",
        linewidth=3.0,
        alpha=0.42,
        solid_capstyle="round",
        zorder=4,
    )
    median_width = float(np.interp(np.log10(row.median), row.grid, width))
    ax.plot(
        [row.median, row.median],
        [position - median_width, position + median_width],
        color="#17313A",
        linewidth=1.9,
        zorder=5,
    )
    ax.scatter(
        [row.median],
        [position],
        s=34,
        facecolor="#FFFFFF",
        edgecolor="#17313A",
        linewidth=1.3,
        zorder=6,
    )

ax.set_xscale("log")
ax.set_xlim(3.2, 9500)
ax.set_ylim(-0.65, len(summary) - 0.35)

x_ticks = [5, 10, 20, 50, 100, 200, 500, 1000, 2000, 7000]
ax.set_xticks(x_ticks)
ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:,.0f}"))
ax.xaxis.set_minor_formatter(FuncFormatter(lambda *_: ""))
ax.minorticks_off()
ax.tick_params(axis="x", which="both", length=0, labelsize=10.5)
ax.tick_params(axis="y", which="both", length=0, labelsize=10.2, pad=9)

ax.set_yticks(positions)
ax.set_yticklabels(
    [CATEGORY_LABELS[category] for category in summary["category"]], linespacing=1.1
)
for position, row in zip(positions, summary.itertuples()):
    ax.text(
        -0.0155,
        position - 0.26,
        f"n = {row.n:,}   ·   median ¥{row.median:,.2f}",
        transform=ax.get_yaxis_transform(),
        ha="right",
        va="center",
        fontsize=8.6,
        color="#6B7F88",
    )

ax.grid(axis="x", color="#DCE5E8", linewidth=0.9, zorder=0)
ax.set_axisbelow(True)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
for side in ("left", "bottom"):
    ax.spines[side].set_color("#AEBCC2")

ax.set_xlabel("Revenue per completed order line (CNY, log scale)", fontsize=12.5, labelpad=12)
ax.set_ylabel("Product category", fontsize=12.5, labelpad=10)

legend_handles = [
    Patch(
        facecolor="#2B6B7A",
        edgecolor="#1F4E5F",
        alpha=0.55,
        label="Revenue density (equal-area KDE)",
    ),
    Line2D(
        [0],
        [0],
        color="#17313A",
        linewidth=3.0,
        alpha=0.42,
        label="Quartile range (Q1–Q3)",
    ),
    Line2D(
        [0],
        [0],
        color="#17313A",
        linewidth=1.9,
        marker="o",
        markerfacecolor="#FFFFFF",
        markeredgecolor="#17313A",
        markeredgewidth=1.2,
        markersize=6.0,
        label="Median",
    ),
    Line2D(
        [0],
        [0],
        color="#6B7F88",
        linewidth=1.25,
        linestyle=(0, (3, 3)),
        label=f"Overall median (¥{overall_median:,.0f})",
    ),
]
fig.legend(
    handles=legend_handles,
    loc="center right",
    bbox_to_anchor=(0.995, 0.50),
    frameon=False,
    fontsize=10.2,
    handlelength=2.0,
    labelspacing=1.15,
)

fig.text(
    0.06,
    0.955,
    "Revenue Distribution Varies in Shape and Spread Across Product Categories",
    fontsize=21,
    fontweight="bold",
    color="#17313A",
    ha="left",
    va="top",
)
fig.text(
    0.06,
    0.902,
    f"Completed, revenue-bearing order lines  |  n = {total_n:,}  |  "
    "categories sorted by median  |  KDE on log10 revenue (Silverman bandwidth)",
    fontsize=11.3,
    color="#52656D",
    ha="left",
    va="top",
)

fig.text(
    0.06,
    0.055,
    "Violin thickness is proportional to probability density; each category has equal area. "
    "White dot and dark bar mark the median; horizontal bar spans Q1–Q3.",
    fontsize=8.6,
    color="#71838B",
    ha="left",
    va="bottom",
)
fig.text(
    0.06,
    0.028,
    f"X-axis log-scaled. Zero-revenue completed lines excluded (n = {zero_revenue_count:,}).",
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
print(f"Categories: {len(summary)} | lines: {total_n:,} | overall median: ¥{overall_median:,.2f}")
for row in summary.itertuples():
    print(
        f"{row.category}: n={row.n:,}, median=¥{row.median:,.2f}, "
        f"IQR=¥{row.q3 - row.q1:,.2f}, bandwidth={row.bandwidth:.4f} log10"
    )
