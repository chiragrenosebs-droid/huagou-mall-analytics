"""Pair plot of unit price, quantity, revenue and profit for completed order lines.

A corner-style 4x4 matrix on log/signed-log axes:
- diagonal: distribution of each variable,
- lower triangle: pairwise scatter plots,
- upper triangle: Spearman rank correlations.

The transformations keep right-skewed monetary variables readable and allow losses
and large profits to share one axis for profit.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.ticker import FixedFormatter, FixedLocator, FuncFormatter

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "huagou_mall_synthetic_ecommerce.csv"
OUTPUT_PATH = PROJECT_ROOT / "output" / "charts" / "price_quantity_revenue_profit_pairplot.png"

VARIABLES = ["Unit_Price_CNY", "Quantity", "Revenue_CNY", "Profit_CNY"]
SHORT_NAMES = ["Unit price", "Quantity", "Revenue", "Profit"]
AXIS_LABELS = [
    "Unit price (CNY, log)",
    "Quantity (units)",
    "Revenue (CNY, log)",
    "Profit (CNY, signed log)",
]

# --- Data: same population as the other revenue charts -----------------------
df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
completed = df[df["Order_Status"] == "Completed"]
zero_revenue_count = int((completed["Revenue_CNY"] == 0).sum())
base = completed.loc[completed["Revenue_CNY"] > 0, VARIABLES].copy()

# Transformed coordinates used for plotting.
transformed = pd.DataFrame(
    {
        "Unit_Price_CNY": np.log10(base["Unit_Price_CNY"]),
        "Quantity": base["Quantity"].astype(float),
        "Revenue_CNY": np.log10(base["Revenue_CNY"]),
        "Profit_CNY": np.sign(base["Profit_CNY"])
        * np.log10(1 + base["Profit_CNY"].abs()),
    }
)


def profit_transform(value):
    return np.sign(value) * np.log10(1 + abs(value))


# Original-value ticks converted into plotting coordinates.
TICKS = {
    0: (
        [10, 30, 100, 300, 1000],
        [np.log10(v) for v in [10, 30, 100, 300, 1000]],
        [0.62, 3.30],
    ),
    1: ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [0.45, 5.55]),
    2: (
        [10, 30, 100, 300, 1000, 3000],
        [np.log10(v) for v in [10, 30, 100, 300, 1000, 3000]],
        [0.35, 4.00],
    ),
    3: (
        [-1000, -100, 0, 100, 1000],
        [profit_transform(v) for v in [-1000, -100, 0, 100, 1000]],
        [-3.20, 3.55],
    ),
}

ordered = base[VARIABLES]
spearman = ordered.rank().corr()

# --- Styling ----------------------------------------------------------------
plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Microsoft YaHei", "DejaVu Sans"],
        "axes.unicode_minus": False,
        "axes.edgecolor": "#DCE5E8",
        "axes.labelcolor": "#1B2A33",
        "text.color": "#1B2A33",
        "xtick.color": "#42545C",
        "ytick.color": "#42545C",
        "figure.facecolor": "#FFFFFF",
        "axes.facecolor": "#FFFFFF",
    }
)

fig, axes = plt.subplots(4, 4, figsize=(14, 14), dpi=200)
fig.subplots_adjust(left=0.085, right=0.985, top=0.905, bottom=0.115, wspace=0.10, hspace=0.10)

TEAL = "#2B6B7A"
DARK = "#17313A"
AMBER = "#E9A23B"
GREY = "#71838B"

for row in range(4):
    for col in range(4):
        ax = axes[row, col]
        ax.tick_params(axis="both", which="both", length=0, labelsize=9.8)
        for spine in ax.spines.values():
            spine.set_color("#DCE5E8")
            spine.set_linewidth(0.9)

        x_vals, x_positions, x_limits = TICKS[col]
        y_vals, y_positions, y_limits = TICKS[row]
        ax.set_xlim(*x_limits)
        ax.set_ylim(*y_limits)
        ax.set_xticks(x_positions)
        ax.set_yticks(y_positions)
        ax.grid(color="#EBF1F3", linewidth=0.8, zorder=0)
        ax.set_axisbelow(True)

        if row == 3:
            ax.xaxis.set_major_formatter(FixedFormatter([f"{v:,}" for v in x_vals]))
        else:
            ax.tick_params(labelbottom=False)

        if col == 0:
            ax.yaxis.set_major_formatter(FixedFormatter([f"{v:,}" for v in y_vals]))
        else:
            ax.tick_params(labelleft=False)

# --- Diagonal: distributions ------------------------------------------------
for index in range(4):
    ax = axes[index, index]
    values = transformed[VARIABLES[index]].to_numpy()
    x_vals, x_positions, x_limits = TICKS[index]

    if index == 1:  # Quantity is discrete
        counts = base["Quantity"].value_counts().sort_index()
        shares = counts / len(base) * 100
        ax.bar(
            counts.index,
            counts.values,
            width=0.68,
            color=TEAL,
            alpha=0.78,
            edgecolor="#FFFFFF",
            linewidth=0.8,
            zorder=2,
        )
        for quantity, count, share in zip(counts.index, counts.values, shares.values):
            ax.text(
                quantity,
                count * 1.02,
                f"{share:.1f}%",
                ha="center",
                va="bottom",
                fontsize=8.2,
                color="#52656D",
            )
        ax.set_ylim(0, counts.max() * 1.22)
        ax.tick_params(labelleft=False)
    else:
        bins = np.linspace(x_limits[0], x_limits[1], 58)
        counts, _ = np.histogram(values, bins=bins)
        ax.set_ylim(0, counts.max() * 1.14)
        ax.hist(
            values,
            bins=bins,
            color=TEAL,
            alpha=0.78,
            edgecolor="#FFFFFF",
            linewidth=0.25,
            zorder=2,
        )
        median_value = base[VARIABLES[index]].median()
        median_position = (
            profit_transform(median_value) if index == 3 else np.log10(median_value)
        )
        ax.axvline(median_position, color=DARK, linewidth=1.5, zorder=4)
        label = f"median ¥{median_value:,.0f}"
        ax.text(
            0.035,
            0.885,
            label,
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontsize=8.8,
            color=DARK,
            bbox={"facecolor": "#FFFFFF", "edgecolor": "none", "alpha": 0.86, "pad": 1.6},
            zorder=5,
        )
        ax.tick_params(labelleft=False)

    if index == 3:
        ax.axvline(0, color=GREY, linewidth=1.0, linestyle=(0, (3, 3)), zorder=1)

    ax.text(
        0.035,
        0.998,
        SHORT_NAMES[index],
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=11.0,
        fontweight="bold",
        color=DARK,
        bbox={"facecolor": "#FFFFFF", "edgecolor": "none", "alpha": 0.88, "pad": 1.4},
        zorder=6,
    )

# --- Lower triangle: pairwise scatter plots ---------------------------------
for row in range(1, 4):
    for col in range(row):
        ax = axes[row, col]
        ax.scatter(
            transformed[VARIABLES[col]],
            transformed[VARIABLES[row]],
            s=4.6,
            color=TEAL,
            alpha=0.16,
            edgecolors="none",
            rasterized=True,
            zorder=2,
        )
        if row == 3:
            ax.axhline(0, color=GREY, linewidth=1.0, linestyle=(0, (3, 3)), zorder=3)

# --- Upper triangle: rank correlations --------------------------------------
def strength(value):
    absolute = abs(value)
    if absolute >= 0.80:
        return "very strong"
    if absolute >= 0.60:
        return "strong"
    if absolute >= 0.30:
        return "moderate"
    if absolute >= 0.10:
        return "weak"
    return "negligible"


for row in range(4):
    for col in range(row + 1, 4):
        ax = axes[row, col]
        rho = spearman.iloc[row, col]
        colour = TEAL if abs(rho) >= 0.30 else GREY
        ax.text(
            0.5,
            0.56,
            f"{rho:+.2f}",
            transform=ax.transAxes,
            ha="center",
            va="center",
            fontsize=25,
            fontweight="bold",
            color=colour,
        )
        ax.text(
            0.5,
            0.36,
            strength(rho),
            transform=ax.transAxes,
            ha="center",
            va="center",
            fontsize=9.8,
            color="#52656D",
        )
        ax.text(
            0.5,
            0.83,
            "Spearman ρ",
            transform=ax.transAxes,
            ha="center",
            va="center",
            fontsize=8.6,
            color="#8A9BA2",
        )

# --- Axis labels -------------------------------------------------------------
for col in range(4):
    axes[3, col].set_xlabel(AXIS_LABELS[col], fontsize=11.3, labelpad=9)
for row in range(4):
    axes[row, 0].set_ylabel(AXIS_LABELS[row], fontsize=11.3, labelpad=9)

# --- Titles and notes --------------------------------------------------------
fig.text(
    0.06,
    0.978,
    "Price and Quantity Jointly Shape Revenue and Profit",
    fontsize=22,
    fontweight="bold",
    color=DARK,
    ha="left",
    va="top",
)
fig.text(
    0.06,
    0.942,
    f"Completed, revenue-bearing lines  |  n = {len(base):,}  |  "
    "lower triangle: scatter  |  diagonal: distribution  |  upper triangle: Spearman ρ",
    fontsize=10.8,
    color="#52656D",
    ha="left",
    va="top",
)

fig.text(
    0.06,
    0.055,
    "Log10 axes for unit price and revenue; profit uses sign(p) × log10(1 + |p|) so losses and high gains share one scale. "
    "Point transparency and rasterisation handle overplotting.",
    fontsize=8.6,
    color=GREY,
    ha="left",
    va="bottom",
)
fig.text(
    0.06,
    0.028,
    f"Spearman ρ is a rank correlation. Zero-revenue completed lines excluded (n = {zero_revenue_count:,}). "
    "Profit = revenue after discount − quantity × unit cost.",
    fontsize=8.6,
    color=GREY,
    ha="left",
    va="bottom",
)
fig.text(
    0.975,
    0.028,
    "Source: HuaGou Mall synthetic e-commerce dataset",
    fontsize=8.6,
    color=GREY,
    ha="right",
    va="bottom",
)

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUTPUT_PATH, dpi=200, facecolor=fig.get_facecolor(), bbox_inches="tight")
plt.close(fig)

print(f"Saved chart: {OUTPUT_PATH}")
print(f"Lines: {len(base):,}")
print("\nSpearman correlations:")
print(spearman.round(3).to_string())
print("\nQuantity counts:")
print(base["Quantity"].value_counts().sort_index().to_string())
