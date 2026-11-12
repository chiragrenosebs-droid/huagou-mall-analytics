"""Revenue heatmap: product category (rows) by calendar month (columns).

Each cell is the sum of Revenue_CNY over completed, revenue-bearing order lines,
with 2024 and 2025 summed into the same calendar month. The sequential teal
palette encodes absolute revenue, and every cell is labelled so exact values
remain readable even where the colour is pale.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.ticker import FuncFormatter

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "huagou_mall_synthetic_ecommerce.csv"
OUTPUT_PATH = PROJECT_ROOT / "output" / "charts" / "category_month_revenue_heatmap.png"

CATEGORY_LABELS = {
    "数码电子": "数码电子   Digital Electronics",
    "服饰鞋包": "服饰鞋包   Apparel & Bags",
    "运动户外": "运动户外   Sports & Outdoors",
    "家居生活": "家居生活   Home & Living",
    "美妆个护": "美妆个护   Beauty & Personal Care",
    "食品饮料": "食品饮料   Food & Beverage",
    "母婴用品": "母婴用品   Mother & Baby",
    "图书文具": "图书文具   Books & Stationery",
}
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
DARK = "#17313A"
INK = "#243A43"
MUTED = "#5F7178"
FAINT = "#7C8D94"
WHITE = "#FFFFFF"
BORDER = "#C9D6DA"
AMBER_DARK = "#B06A18"

# Pale sand-free teal ramp: monotonic lightness, readable at the low end.
CMAP = LinearSegmentedColormap.from_list(
    "huagou_teal",
    [
        "#F4F8F8",
        "#D8E9EB",
        "#AFCFD4",
        "#7FAFB8",
        "#4F8B98",
        "#2B6B7A",
        "#1A4B57",
        "#0F2F38",
    ],
)

# --- Data ----------------------------------------------------------------------
df = pd.read_csv(DATA_PATH, encoding="utf-8-sig", parse_dates=["Order_Date"])
completed = df[df["Order_Status"] == "Completed"]
zero_revenue_count = int((completed["Revenue_CNY"] == 0).sum())
base = completed.loc[completed["Revenue_CNY"] > 0].copy()
total_revenue = float(base["Revenue_CNY"].sum())
base["Month"] = base["Order_Date"].dt.month

pivot = base.pivot_table(
    index="Category", columns="Month", values="Revenue_CNY", aggfunc="sum"
).reindex(columns=range(1, 13))
pivot = pivot.fillna(0.0)
pivot = pivot.loc[pivot.sum(axis=1).sort_values(ascending=False).index]

row_totals = pivot.sum(axis=1)
month_totals = pivot.sum(axis=0)
peak_month = int(month_totals.idxmax())
peak_value = float(month_totals.max())

# --- Colour helpers ------------------------------------------------------------
def _linear(channel):
    return channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4


def luminance(rgb):
    r, g, b = (_linear(c) for c in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def cell_text(value):
    if value >= 1_000_000:
        return f"¥{value / 1_000_000:.2f}M"
    if value >= 100_000:
        return f"¥{value / 1_000:.0f}K"
    return f"¥{value / 1_000:.1f}K"


def cbar_text(value, _position):
    if value == 0:
        return "¥0"
    if value >= 1_000_000:
        return f"¥{value / 1_000_000:.1f}M"
    return f"¥{value / 1_000:.0f}K"


# --- Styling -------------------------------------------------------------------
plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Microsoft YaHei", "DejaVu Sans"],
        "axes.unicode_minus": False,
        "figure.facecolor": WHITE,
        "savefig.facecolor": WHITE,
        "axes.labelcolor": INK,
        "text.color": INK,
        "xtick.color": "#42545C",
        "ytick.color": "#42545C",
    }
)

fig = plt.figure(figsize=(15.5, 9.0), dpi=200)
ax = fig.add_axes([0.190, 0.155, 0.640, 0.695])
cax = fig.add_axes([0.846, 0.155, 0.017, 0.695])

norm = Normalize(vmin=0, vmax=float(pivot.values.max()))
mesh = ax.imshow(
    pivot.values,
    cmap=CMAP,
    norm=norm,
    aspect="auto",
    interpolation="nearest",
    origin="upper",
)

ax.set_xticks(range(12))
ax.set_xticklabels(MONTHS, fontsize=11.0)
ax.xaxis.tick_top()
ax.tick_params(axis="x", which="both", length=0, pad=8, top=False,
               labeltop=True, bottom=False, labelbottom=False)
for index, label in enumerate(ax.get_xticklabels()):
    if index + 1 in (6, 11):
        label.set_fontweight("bold")
        label.set_color(AMBER_DARK)

ax.set_yticks(range(len(pivot.index)))
ax.set_yticklabels(
    [CATEGORY_LABELS[category] for category in pivot.index], fontsize=10.2
)
ax.tick_params(axis="y", which="both", length=0, pad=10)

# White cell separators.
ax.set_xticks(np.arange(-0.5, 12, 1), minor=True)
ax.set_yticks(np.arange(-0.5, len(pivot.index), 1), minor=True)
ax.grid(which="minor", color=WHITE, linewidth=2.6)
ax.tick_params(which="minor", length=0)

for spine in ax.spines.values():
    spine.set_color(BORDER)
    spine.set_linewidth(0.9)

ax.set_ylabel("Product category", fontsize=11.4, labelpad=14)

# --- Cell values ---------------------------------------------------------------
for row in range(pivot.shape[0]):
    for column in range(pivot.shape[1]):
        value = float(pivot.iat[row, column])
        rgba = CMAP(norm(value))
        text_color = WHITE if luminance(rgba) < 0.26 else DARK
        ax.text(
            column,
            row,
            cell_text(value),
            ha="center",
            va="center",
            fontsize=8.8,
            color=text_color,
            alpha=0.96,
            zorder=3,
        )

# --- Colorbar -------------------------------------------------------------------
cbar = fig.colorbar(mesh, cax=cax)
cbar.ax.yaxis.set_major_formatter(FuncFormatter(cbar_text))
cbar.set_ticks([0, 250_000, 500_000, 750_000, 1_000_000])
cbar.ax.tick_params(length=0, labelsize=9.4, pad=7, colors="#42545C")
cbar.set_label("Revenue, 2024 + 2025 (CNY)", fontsize=10.6, labelpad=13, color=INK)
cbar.outline.set_edgecolor(BORDER)
cbar.outline.set_linewidth(0.9)

# --- Titles and notes ----------------------------------------------------------
fig.text(
    0.043,
    0.968,
    "June and November Are Revenue Peaks in Every Category",
    fontsize=22.5,
    fontweight="bold",
    color=DARK,
    ha="left",
    va="top",
)
fig.text(
    0.043,
    0.925,
    "Sum of Revenue_CNY by product category and calendar month  |  completed, "
    f"revenue-bearing order lines (n = {len(base):,})  |  2024 and 2025 combined  |  "
    f"total ¥{total_revenue / 1_000_000:.2f}M",
    fontsize=10.8,
    color=MUTED,
    ha="left",
    va="top",
)

fig.text(
    0.043,
    0.088,
    "June and November each carry about 14% of two-year revenue — roughly double the "
    "~7% monthly baseline — and the uplift runs through the whole month, not one day.",
    fontsize=8.7,
    color=FAINT,
    ha="left",
    va="bottom",
)
fig.text(
    0.043,
    0.055,
    "Colour is linear: smaller categories sit at the pale end, so read the printed values "
    f"for exact monthly revenue. Zero-revenue completed lines excluded (n = {zero_revenue_count:,}).",
    fontsize=8.7,
    color=FAINT,
    ha="left",
    va="bottom",
)
fig.text(
    0.043,
    0.024,
    "Source: HuaGou Mall synthetic e-commerce dataset. Months aggregate both calendar years; "
    "no year split is shown.",
    fontsize=8.7,
    color=FAINT,
    ha="left",
    va="bottom",
)

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUTPUT_PATH, dpi=200, facecolor=WHITE, bbox_inches="tight")
plt.close(fig)

# --- Diagnostics ---------------------------------------------------------------
print(f"Saved chart: {OUTPUT_PATH}")
print(f"Lines: {len(base):,} | total revenue: ¥{total_revenue:,.2f} | months: 1-12 "
      f"(2024 + 2025) | categories: {len(pivot)}")
print(f"Peak month: {MONTHS[peak_month - 1]} ¥{peak_value:,.2f}")
print("\nCategory totals:")
for category, value in row_totals.items():
    print(f"  {category:6s} ¥{value:,.2f}  ({value / total_revenue * 100:.2f}%)")
print("\nMonth totals:")
for month, value in month_totals.items():
    print(f"  {MONTHS[month - 1]}  ¥{value:,.2f}  ({value / total_revenue * 100:.2f}%)")
print("\nMatrix (CNY):")
print(pivot.round(2).to_string())
