"""Bubble plot of unit price versus profit, with quantity encoded by bubble area.

Each completed, revenue-bearing order line is one bubble:
- x = unit price (log scale, because prices span two orders of magnitude),
- y = profit per line (symlog, so losses and large gains share one axis),
- bubble area = quantity (1-5 units, proportional).

Transparency, small markers and quantity-ordered drawing keep the dense low-price
region readable while letting larger, rarer multi-unit bubbles stand out.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "huagou_mall_synthetic_ecommerce.csv"
OUTPUT_PATH = PROJECT_ROOT / "output" / "charts" / "price_profit_quantity_bubbles.png"

TEAL = "#2B6B7A"
DARK = "#17313A"
AMBER = "#E9A23B"
AMBER_DARK = "#C77A1E"
GREY = "#6B7F88"

# --- Data: same population as the other charts ---------------------------------
df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
completed = df[df["Order_Status"] == "Completed"]
zero_revenue_count = int((completed["Revenue_CNY"] == 0).sum())
base = completed.loc[
    completed["Revenue_CNY"] > 0,
    ["Unit_Price_CNY", "Quantity", "Profit_CNY", "Discount_Percentage"],
].copy()

# --- Axis helpers --------------------------------------------------------------
BASE_AREA = 12.0  # marker area in points^2 for a single unit

x_ticks = [10, 30, 100, 300, 1000]
y_ticks = [-1000, -300, -100, -50, 0, 50, 100, 300, 1000, 2500]

# Median profit by unit-price decile, used for the amber trend line.
base["price_decile"] = pd.qcut(base["Unit_Price_CNY"], 10, duplicates="drop")
grouped = base.groupby("price_decile", observed=True)
trend = pd.DataFrame(
    {
        "x": grouped["Unit_Price_CNY"].median(),
        "median": grouped["Profit_CNY"].median(),
        "n": grouped.size(),
    }
).reset_index(drop=True)

price_median = base["Unit_Price_CNY"].median()
profit_median = base["Profit_CNY"].median()
profit_mean = base["Profit_CNY"].mean()
loss_count = int((base["Profit_CNY"] < 0).sum())
spearman = base["Unit_Price_CNY"].rank().corr(base["Profit_CNY"].rank())
pearson = base["Unit_Price_CNY"].corr(base["Profit_CNY"])
max_point = base.loc[base["Profit_CNY"].idxmax()]
min_point = base.loc[base["Profit_CNY"].idxmin()]
quantity_counts = base["Quantity"].value_counts().sort_index()

# --- Styling -------------------------------------------------------------------
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

fig, ax = plt.subplots(figsize=(14, 9), dpi=200)
fig.subplots_adjust(left=0.085, right=0.975, top=0.855, bottom=0.145)

ax.grid(axis="both", color="#DCE5E8", linewidth=0.9, zorder=0)
ax.set_axisbelow(True)
ax.axhline(0, color=GREY, linewidth=1.25, linestyle=(0, (3, 3)), zorder=1)

# --- Bubbles: area proportional to quantity, largest drawn last ----------------
# Slightly higher opacity for the rarer large bubbles keeps them legible without
# darkening the crowded single-unit core. Opacity is not an encoded variable.
ALPHA_BY_QUANTITY = {1: 0.15, 2: 0.19, 3: 0.24, 4: 0.29, 5: 0.34}

for quantity in range(1, 6):
    subset = base[base["Quantity"] == quantity]
    ax.scatter(
        subset["Unit_Price_CNY"],
        subset["Profit_CNY"],
        s=BASE_AREA * quantity,
        color=TEAL,
        alpha=ALPHA_BY_QUANTITY[quantity],
        edgecolors="none",
        rasterized=True,
        zorder=2 + quantity * 0.01,
    )

# --- Median trend line ---------------------------------------------------------
ax.plot(
    trend["x"],
    trend["median"],
    color=AMBER_DARK,
    linewidth=2.4,
    marker="o",
    markersize=5.2,
    markerfacecolor=AMBER,
    markeredgecolor="#FFFFFF",
    markeredgewidth=1.0,
    zorder=5,
)

ax.set_xscale("log")
ax.set_yscale("symlog", linthresh=50, linscale=1.0, base=10)
ax.set_xlim(5.5, 1800)
ax.set_ylim(-1100, 3000)

ax.set_xticks(x_ticks)
ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:,.0f}"))
ax.xaxis.set_minor_formatter(FuncFormatter(lambda *_: ""))
ax.minorticks_off()
ax.tick_params(axis="x", which="both", length=0, labelsize=10.8)
ax.tick_params(axis="y", which="both", length=0, labelsize=10.5)

ax.set_yticks(y_ticks)
ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value:,.0f}"))
ax.yaxis.set_minor_formatter(FuncFormatter(lambda *_: ""))
ax.minorticks_off()

for side in ("top", "right"):
    ax.spines[side].set_visible(False)
for side in ("left", "bottom"):
    ax.spines[side].set_color("#AEBCC2")

ax.set_xlabel("Unit price (CNY, log scale)", fontsize=12.5, labelpad=12)
ax.set_ylabel(
    "Profit per completed order line (CNY, symlog scale)", fontsize=12.5, labelpad=10
)

# --- Extreme points ------------------------------------------------------------
ax.annotate(
    f"Max profit  ¥{max_point['Profit_CNY']:,.0f}\n"
    f"{int(max_point['Quantity'])} units at {max_point['Discount_Percentage']:.1f}% discount",
    xy=(max_point["Unit_Price_CNY"], max_point["Profit_CNY"]),
    xytext=(360, 1850),
    fontsize=9.0,
    color="#42545C",
    ha="left",
    va="center",
    arrowprops={"arrowstyle": "-", "color": "#8A9BA2", "linewidth": 0.9},
    bbox={"facecolor": "#FFFFFF", "edgecolor": "none", "alpha": 0.9, "pad": 2.0},
    zorder=7,
)
ax.annotate(
    f"Max loss  −¥{abs(min_point['Profit_CNY']):,.0f}\n"
    f"{int(min_point['Quantity'])} units at {min_point['Discount_Percentage']:.1f}% discount",
    xy=(min_point["Unit_Price_CNY"], min_point["Profit_CNY"]),
    xytext=(520, -620),
    fontsize=9.0,
    color="#42545C",
    ha="left",
    va="center",
    arrowprops={"arrowstyle": "-", "color": "#8A9BA2", "linewidth": 0.9},
    bbox={"facecolor": "#FFFFFF", "edgecolor": "none", "alpha": 0.9, "pad": 2.0},
    zorder=7,
)

# --- Legends -------------------------------------------------------------------
trend_handles = [
    Line2D(
        [0],
        [0],
        color=AMBER_DARK,
        linewidth=2.4,
        marker="o",
        markerfacecolor=AMBER,
        markeredgecolor="#FFFFFF",
        markersize=5.2,
        label="Median profit (price deciles)",
    ),
    Line2D(
        [0],
        [0],
        color=GREY,
        linewidth=1.25,
        linestyle=(0, (3, 3)),
        label="Break-even (¥0)",
    ),
]
trend_legend = ax.legend(
    handles=trend_handles,
    loc="upper left",
    bbox_to_anchor=(0.012, 0.975),
    frameon=True,
    facecolor="#FFFFFF",
    edgecolor="#DCE5E8",
    framealpha=0.95,
    fontsize=9.6,
    handlelength=2.3,
    labelspacing=0.75,
)
ax.add_artist(trend_legend)

size_handles = [
    Line2D(
        [0],
        [0],
        linestyle="none",
        marker="o",
        markersize=np.sqrt(BASE_AREA * quantity),
        markerfacecolor=TEAL,
        markeredgecolor="none",
        alpha=0.55,
        label=f"{quantity} unit" + ("s" if quantity > 1 else ""),
    )
    for quantity in range(1, 6)
]
ax.legend(
    handles=size_handles,
    title="Quantity\nbubble area ∝ units",
    loc="lower left",
    bbox_to_anchor=(0.012, 0.025),
    frameon=True,
    facecolor="#FFFFFF",
    edgecolor="#DCE5E8",
    framealpha=0.95,
    title_fontsize=9.2,
    fontsize=9.2,
    handletextpad=0.9,
    labelspacing=0.55,
    borderpad=0.8,
)

# --- Titles and notes ----------------------------------------------------------
fig.text(
    0.06,
    0.955,
    "Profit Scales With Unit Price — Quantity Lifts the Ceiling",
    fontsize=21,
    fontweight="bold",
    color=DARK,
    ha="left",
    va="top",
)
fig.text(
    0.06,
    0.903,
    f"Completed, revenue-bearing order lines  |  n = {len(base):,}  |  "
    "bubble area ∝ Quantity (1–5 units)  |  log price axis, symlog profit axis",
    fontsize=11.2,
    color="#52656D",
    ha="left",
    va="top",
)

fig.text(
    0.06,
    0.055,
    "Bubble area is proportional to quantity; transparency reveals overlapping lines "
    "(darker = denser). Larger bubbles sit higher at a given price because profit scales with units.",
    fontsize=8.6,
    color="#71838B",
    ha="left",
    va="bottom",
)
fig.text(
    0.06,
    0.028,
    f"Zero-revenue completed lines excluded (n = {zero_revenue_count:,}). "
    "Symlog profit axis is linear within ±¥50 and logarithmic beyond.",
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
print(f"Lines: {len(base):,} | median price: ¥{price_median:,.2f} | median profit: ¥{profit_median:,.2f}")
print(f"Pearson: {pearson:.3f} | Spearman: {spearman:.3f} | loss lines: {loss_count:,} ({(base['Profit_CNY'] < 0).mean() * 100:.2f}%)")
print("Quantity counts:", quantity_counts.to_dict())
print("\nMedian profit by price decile:")
for row in trend.itertuples():
    print(f"  x=¥{row.x:,.2f}  median=¥{row.median:,.2f}  n={row.n:,}")
