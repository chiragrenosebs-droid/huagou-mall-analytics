"""Box plot of completed order-line revenue by product category.

Compares Revenue_CNY across the eight product categories for completed lines with
positive revenue. Categories are sorted by median revenue (highest at the top).
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
OUTPUT_PATH = PROJECT_ROOT / "output" / "charts" / "category_revenue_boxplot.png"

CATEGORY_LABELS = {
    "运动户外": "运动户外  Sports & Outdoors",
    "数码电子": "数码电子  Digital Electronics",
    "服饰鞋包": "服饰鞋包  Fashion & Bags",
    "美妆个护": "美妆个护  Beauty & Personal Care",
    "食品饮料": "食品饮料  Food & Beverages",
    "母婴用品": "母婴用品  Mother & Baby",
    "家居生活": "家居生活  Home & Living",
    "图书文具": "图书文具  Books & Stationery",
}

# --- Data: same population as the previous revenue charts --------------------
df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
completed = df[df["Order_Status"] == "Completed"]
zero_revenue_count = int((completed["Revenue_CNY"] == 0).sum())
base = completed.loc[completed["Revenue_CNY"] > 0, ["Category", "Revenue_CNY"]].copy()

overall_median = base["Revenue_CNY"].median()
total_n = len(base)

# --- Category summaries ------------------------------------------------------
rows = []
for category, values in base.groupby("Category")["Revenue_CNY"]:
    q1, q3 = values.quantile([0.25, 0.75])
    iqr = q3 - q1
    lower_fence = q1 - 1.5 * iqr
    upper_fence = q3 + 1.5 * iqr
    rows.append(
        {
            "category": category,
            "n": len(values),
            "median": values.median(),
            "q1": q1,
            "q3": q3,
            "iqr": iqr,
            "lower_fence": lower_fence,
            "upper_fence": upper_fence,
            "outlier_count": int(((values < lower_fence) | (values > upper_fence)).sum()),
        }
    )

summary = pd.DataFrame(rows).sort_values("median", ascending=False).reset_index(drop=True)
positions = np.arange(len(summary))[::-1]
box_data = [
    base.loc[base["Category"] == category, "Revenue_CNY"].to_numpy()
    for category in summary["category"]
]
y_labels = [CATEGORY_LABELS[category] for category in summary["category"]]

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
fig.subplots_adjust(left=0.225, right=0.835, top=0.845, bottom=0.155)

# Subtle alternating row bands improve readability across eight categories.
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

ax.boxplot(
    box_data,
    positions=positions,
    orientation="horizontal",
    widths=0.56,
    patch_artist=True,
    showfliers=False,
    whis=1.5,
    manage_ticks=False,
    medianprops={"color": "#17313A", "linewidth": 2.2},
    whiskerprops={"color": "#42545C", "linewidth": 1.2},
    capprops={"color": "#42545C", "linewidth": 1.2},
    boxprops={
        "facecolor": "#2B6B7A",
        "edgecolor": "#1F4E5F",
        "linewidth": 1.3,
        "alpha": 0.78,
    },
    zorder=3,
)

# Plot potential outliers with a small deterministic jitter so dense points remain
# readable instead of collapsing into a vertical line.
rng = np.random.default_rng(7)
for position, category in zip(positions, summary["category"]):
    row = summary.loc[summary["category"] == category].iloc[0]
    values = base.loc[base["Category"] == category, "Revenue_CNY"].to_numpy()
    outliers = values[
        (values < row["lower_fence"]) | (values > row["upper_fence"])
    ]
    if outliers.size:
        jitter = rng.uniform(-0.11, 0.11, size=outliers.size)
        ax.scatter(
            outliers,
            np.full(outliers.size, position) + jitter,
            s=5.2,
            color="#C8553D",
            alpha=0.36,
            edgecolors="none",
            zorder=2,
        )

ax.set_xscale("log")
ax.set_xlim(3.2, 8500)
ax.set_ylim(-0.65, len(summary) - 0.35)

x_ticks = [5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 7000]
ax.set_xticks(x_ticks)
ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:,.0f}"))
ax.xaxis.set_minor_formatter(FuncFormatter(lambda *_: ""))
ax.minorticks_off()
ax.tick_params(axis="x", which="both", length=0, labelsize=10.5)
ax.tick_params(axis="y", which="both", length=0, labelsize=10.5, pad=9)

ax.set_yticks(positions)
ax.set_yticklabels(y_labels, linespacing=1.15)

ax.grid(axis="x", color="#DCE5E8", linewidth=0.9, zorder=0)
ax.set_axisbelow(True)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
for side in ("left", "bottom"):
    ax.spines[side].set_color("#AEBCC2")

ax.set_xlabel("Revenue per completed order line (CNY, log scale)", fontsize=12.5, labelpad=12)
ax.set_ylabel("Product category", fontsize=12.5, labelpad=10)

legend_handles = [
    Patch(facecolor="#2B6B7A", edgecolor="#1F4E5F", alpha=0.78, label="IQR (Q1–Q3)"),
    Line2D([0], [0], color="#17313A", linewidth=2.2, label="Median"),
    Line2D([0], [0], color="#42545C", linewidth=1.2, label="Whisker (1.5×IQR)"),
    Line2D(
        [0],
        [0],
        marker="o",
        color="none",
        markerfacecolor="#C8553D",
        markeredgecolor="none",
        markersize=5.5,
        alpha=0.7,
        label="Potential outlier",
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
    labelspacing=1.05,
)

fig.text(
    0.06,
    0.955,
    "Revenue Distribution Varies Sharply Across Product Categories",
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
    "categories sorted by median  |  whiskers = 1.5×IQR",
    fontsize=11.3,
    color="#52656D",
    ha="left",
    va="top",
)

fig.text(
    0.06,
    0.055,
    "Box = interquartile range (Q1–Q3); horizontal line = median; whiskers = furthest values within 1.5×IQR; dots = potential outliers.",
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
for _, row in summary.iterrows():
    print(
        f"{row['category']}: n={row['n']:,}, median=¥{row['median']:,.2f}, "
        f"IQR=¥{row['iqr']:,.2f}, outliers={row['outlier_count']:,}"
    )
