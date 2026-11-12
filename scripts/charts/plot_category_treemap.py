"""Two-level revenue treemap: category -> sub-category.

Level 1 blocks are categories, level 2 tiles are sub-categories, and every
rectangle's area is proportional to completed-order-line Revenue_CNY. A custom
squarified layout keeps tiles close to square; category headers sit in dark
bands, sub-category tiles use lighter tints of the same hue.

Labels are adaptive: name + revenue + share of total where the tile is large
enough, then name only, then a rotated name, and finally a footnote for slices
too small to letter legibly.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Rectangle

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "huagou_mall_synthetic_ecommerce.csv"
OUTPUT_PATH = PROJECT_ROOT / "output" / "charts" / "category_revenue_treemap.png"

# --- Palette -------------------------------------------------------------------
CATEGORY_COLORS = {
    "数码电子": "#2F6B7A",  # teal
    "服饰鞋包": "#A9553F",  # terracotta
    "运动户外": "#5F7D4A",  # green
    "家居生活": "#A9752F",  # amber-brown
    "美妆个护": "#A85A6C",  # rose
    "食品饮料": "#7C7440",  # olive
    "母婴用品": "#4F6F8C",  # slate blue
    "图书文具": "#6E5A7E",  # plum
}
CATEGORY_EN = {
    "数码电子": "Digital Electronics",
    "服饰鞋包": "Apparel & Bags",
    "运动户外": "Sports & Outdoors",
    "家居生活": "Home & Living",
    "美妆个护": "Beauty & Personal Care",
    "食品饮料": "Food & Beverage",
    "母婴用品": "Mother & Baby",
    "图书文具": "Books & Stationery",
}
DARK = "#17313A"
INK = "#243A43"
MUTED = "#5F7178"
FAINT = "#7C8D94"
WHITE = "#FFFFFF"

# Tints applied to a category hue for its sub-category tiles, largest first.
TINTS = [0.10, 0.22, 0.34, 0.44]

# --- Data ----------------------------------------------------------------------
df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
completed = df[df["Order_Status"] == "Completed"]
zero_revenue_count = int((completed["Revenue_CNY"] == 0).sum())
base = completed.loc[completed["Revenue_CNY"] > 0].copy()
total_revenue = float(base["Revenue_CNY"].sum())

category_revenue = (
    base.groupby("Category")["Revenue_CNY"].sum().sort_values(ascending=False)
)
subcategory_revenue = (
    base.groupby(["Category", "Subcategory"])["Revenue_CNY"].sum().sort_values(ascending=False)
)


# --- Squarified treemap (Bruls, Huizing & van Wijk) ----------------------------
def _layout_row(sizes, x, y, dx, dy):
    covered = sum(sizes)
    width = covered / dy
    rects = []
    for size in sizes:
        rects.append((x, y, width, size / width))
        y += size / width
    return rects


def _layout_col(sizes, x, y, dx, dy):
    covered = sum(sizes)
    height = covered / dx
    rects = []
    for size in sizes:
        rects.append((x, y, size / height, height))
        x += size / height
    return rects


def _layout(sizes, x, y, dx, dy):
    return _layout_row(sizes, x, y, dx, dy) if dx >= dy else _layout_col(sizes, x, y, dx, dy)


def _leftover(sizes, x, y, dx, dy):
    covered = sum(sizes)
    if dx >= dy:
        width = covered / dy
        return x + width, y, dx - width, dy
    height = covered / dx
    return x, y + height, dx, dy - height


def _worst_ratio(sizes, x, y, dx, dy):
    return max(max(r[2] / r[3], r[3] / r[2]) for r in _layout(sizes, x, y, dx, dy))


def squarify(values, x, y, dx, dy):
    """Return rectangles whose areas are proportional to `values`."""
    sizes = [float(v) for v in values]
    if not sizes:
        return []
    if len(sizes) == 1:
        return _layout(sizes, x, y, dx, dy)
    index = 1
    while (
        index < len(sizes)
        and _worst_ratio(sizes[:index], x, y, dx, dy)
        >= _worst_ratio(sizes[: index + 1], x, y, dx, dy)
    ):
        index += 1
    current, remaining = sizes[:index], sizes[index:]
    rects = _layout(current, x, y, dx, dy)
    left_x, left_y, left_dx, left_dy = _leftover(current, x, y, dx, dy)
    return rects + squarify(remaining, left_x, left_y, left_dx, left_dy)


# --- Colour helpers ------------------------------------------------------------
def _rgb(hex_color):
    value = hex_color.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def tint(hex_color, amount):
    """Blend a colour with white; amount=0 keeps the base, 1 gives white."""
    base_rgb = _rgb(hex_color)
    return tuple((channel + (255 - channel) * amount) / 255 for channel in base_rgb)


def money(value):
    if value >= 1_000_000:
        return f"¥{value / 1_000_000:.2f}M"
    return f"¥{value / 1_000:.1f}K"


# --- Canvas --------------------------------------------------------------------
FIG_W, FIG_H = 15.8, 9.8
AX_W, AX_H = 14.2, 6.9
DPI = 200

plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Microsoft YaHei", "DejaVu Sans"],
        "axes.unicode_minus": False,
        "figure.facecolor": WHITE,
        "savefig.facecolor": WHITE,
    }
)

fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
ax = fig.add_axes([0.035, 0.150, AX_W / FIG_W, AX_H / FIG_H])
ax.set_xlim(0, AX_W)
ax.set_ylim(0, AX_H)
ax.axis("off")

fig.canvas.draw()
renderer = fig.canvas.get_renderer()
PX_PER_IN = DPI

# --- Geometry ------------------------------------------------------------------
GAP = 0.050        # gap between category blocks
INNER_PAD = 0.070  # padding inside a category block
HEADER_TWO = 0.430
HEADER_ONE = 0.245

cat_values = [float(v) for v in category_revenue.values]
cat_scale = (AX_W * AX_H) / sum(cat_values)
cat_rects = squarify([v * cat_scale for v in cat_values], 0, 0, AX_W, AX_H)

tile_records = []  # (name, rect, category, revenue, share, color)


def measure(text, fontsize, weight="normal"):
    prop = FontProperties(
        family=plt.rcParams["font.sans-serif"], size=fontsize, weight=weight
    )
    width, height, _ = renderer.get_text_width_height_descent(text, prop, ismath=False)
    return width, height


def fit_label(inner_w, inner_h, name, value_text):
    """Pick the richest label variant that fits the tile's pixel box."""
    width_px = inner_w * PX_PER_IN - 8
    height_px = inner_h * PX_PER_IN - 8
    candidates = [
        # name, name size, name weight, value, value size, rotation
        (name, 10.4, "bold", value_text, 9.1, 0),
        (name, 9.4, "bold", value_text, 8.5, 0),
        (name, 8.5, "bold", value_text, 7.7, 0),
        (name, 8.5, "bold", None, 0, 0),
        (name, 7.4, "bold", None, 0, 0),
        (name, 6.5, "normal", None, 0, 90),
    ]
    for label_name, name_size, weight, label_value, value_size, rotation in candidates:
        name_w, name_h = measure(label_name, name_size, weight)
        if rotation == 90:
            # Rotated text: the line length becomes vertical.
            if name_h <= width_px + 1 and name_w <= height_px + 1:
                return {
                    "name": label_name,
                    "name_size": name_size,
                    "weight": weight,
                    "value": None,
                    "value_size": 0,
                    "rotation": 90,
                }
            continue
        if label_value is None:
            if name_w <= width_px and name_h <= height_px:
                return {
                    "name": label_name,
                    "name_size": name_size,
                    "weight": weight,
                    "value": None,
                    "value_size": 0,
                    "rotation": 0,
                }
            continue
        value_w, value_h = measure(label_value, value_size)
        gap = 6.0
        needed_h = name_h + gap + value_h
        if max(name_w, value_w) <= width_px and needed_h <= height_px:
            return {
                "name": label_name,
                "name_size": name_size,
                "weight": weight,
                "value": label_value,
                "value_size": value_size,
                "rotation": 0,
                "name_h": name_h,
                "value_h": value_h,
                "gap": gap,
            }
    return None


# --- Draw ----------------------------------------------------------------------
for block, category in zip(cat_rects, category_revenue.index):
    bx, by, bw, bh = block
    x, y = bx + GAP / 2, by + GAP / 2
    w, h = bw - GAP, bh - GAP
    base_color = CATEGORY_COLORS[category]

    header_height = HEADER_TWO if h >= 1.10 else HEADER_ONE
    # Category header band.
    ax.add_patch(
        Rectangle((x, y + h - header_height), w, header_height, facecolor=base_color,
                  edgecolor="none", zorder=4)
    )

    label_x = x + 0.105
    share = category_revenue[category] / total_revenue * 100
    if header_height == HEADER_TWO:
        available_px = (w - 0.20) * PX_PER_IN
        # Prefer a bilingual name; drop English rather than shrink below 9pt.
        line1 = f"{category}   {CATEGORY_EN[category]}"
        size1 = 10.9
        while size1 >= 9.0 and measure(line1, size1, "bold")[0] > available_px:
            size1 -= 0.3
        if measure(line1, size1, "bold")[0] > available_px:
            line1 = category
            size1 = 10.9
        if w >= 2.0:
            line2 = f"{money(category_revenue[category])}  ·  {share:.1f}% of total"
        else:
            line2 = f"{money(category_revenue[category])}  ·  {share:.1f}%"
        size2 = 8.9
        while size2 > 7.6 and measure(line2, size2)[0] > available_px:
            size2 -= 0.2
        ax.text(label_x, y + h - header_height * 0.34, line1, ha="left", va="center",
                fontsize=size1, fontweight="bold", color=WHITE, zorder=5)
        ax.text(label_x, y + h - header_height * 0.72, line2, ha="left", va="center",
                fontsize=size2, color="#EDF3F4", zorder=5)
    else:
        line = f"{category}  {money(category_revenue[category])}  ·  {share:.1f}%"
        available_px = (w - 0.18) * PX_PER_IN
        size1 = 8.4
        while size1 > 6.6 and measure(line, size1, "bold")[0] > available_px:
            size1 -= 0.2
        ax.text(label_x, y + h - header_height * 0.52, line, ha="left", va="center",
                fontsize=size1, fontweight="bold", color=WHITE, zorder=5)

    # Sub-category tiles.
    tx, ty = x + INNER_PAD, y + INNER_PAD
    tw = w - 2 * INNER_PAD
    th = h - header_height - 2 * INNER_PAD
    category_subs = subcategory_revenue.loc[category].sort_values(ascending=False)
    sub_values = [float(v) for v in category_subs.values]
    sub_scale = (tw * th) / sum(sub_values)
    sub_rects = squarify([v * sub_scale for v in sub_values], tx, ty, tw, th)

    for rank, ((sx, sy, sw, sh), subcategory) in enumerate(
        zip(sub_rects, category_subs.index)
    ):
        sub_revenue = float(category_subs[subcategory])
        share = sub_revenue / total_revenue * 100
        fill = tint(base_color, TINTS[min(rank, len(TINTS) - 1)])
        ax.add_patch(
            Rectangle((sx, sy), sw, sh, facecolor=fill, edgecolor=WHITE,
                      linewidth=1.6, zorder=2)
        )
        tile_records.append(
            (category, subcategory, (sx, sy, sw, sh), sub_revenue, share, fill)
        )

        value_text = f"{money(sub_revenue)}  ·  {share:.1f}%"
        label = fit_label(sw, sh, subcategory, value_text)
        if label is None:
            continue
        cx, cy = sx + sw / 2, sy + sh / 2
        text_color = WHITE if rank == 0 else DARK
        if label["rotation"] == 90:
            ax.text(cx, cy, label["name"], ha="center", va="center",
                    fontsize=label["name_size"], fontweight=label["weight"],
                    color=text_color, rotation=90, zorder=3)
        elif label["value"] is None:
            ax.text(cx, cy, label["name"], ha="center", va="center",
                    fontsize=label["name_size"], fontweight=label["weight"],
                    color=text_color, zorder=3)
        else:
            block_h = label["name_h"] + label["gap"] + label["value_h"]
            name_cy = cy + (block_h / 2 - label["name_h"] / 2) / PX_PER_IN
            value_cy = cy - (block_h / 2 - label["value_h"] / 2) / PX_PER_IN
            ax.text(cx, name_cy, label["name"], ha="center", va="center",
                    fontsize=label["name_size"], fontweight=label["weight"],
                    color=text_color, zorder=3)
            ax.text(cx, value_cy, label["value"], ha="center", va="center",
                    fontsize=label["value_size"], color=text_color, alpha=0.82,
                    zorder=3)

# --- Titles and notes ----------------------------------------------------------
fig.text(0.035, 0.960, "Digital Electronics Drives 43% of Revenue",
         fontsize=23, fontweight="bold", color=DARK, ha="left", va="top")
fig.text(
    0.035, 0.902,
    "Category  →  sub-category revenue treemap   |   completed, revenue-bearing order lines "
    f"(n = {len(base):,})   |   rectangle area ∝ Revenue_CNY   |   share = % of "
    f"{money(total_revenue)} total",
    fontsize=10.8, color=MUTED, ha="left", va="top",
)

fig.text(
    0.035, 0.098,
    "Colour identifies the parent category; darker tiles are the larger sub-categories within it. "
    "Tile labels show revenue and share of total revenue where space allows.",
    fontsize=8.6, color=FAINT, ha="left", va="bottom",
)
fig.text(
    0.035, 0.066,
    "Unlabelled slices — 图书文具: 图书 ¥91.2K (0.50%), 创意用品 ¥40.2K (0.22%), "
    "学习用品 ¥27.7K (0.15%), 办公文具 ¥11.8K (0.06%); 母婴用品: 婴儿护理 ¥40.5K (0.22%).",
    fontsize=8.6, color=FAINT, ha="left", va="bottom",
)
fig.text(
    0.035, 0.034,
    f"Zero-revenue completed lines excluded (n = {zero_revenue_count:,}; all Profit_CNY = 0). "
    "Source: HuaGou Mall synthetic e-commerce dataset.",
    fontsize=8.6, color=FAINT, ha="left", va="bottom",
)

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(OUTPUT_PATH, dpi=DPI, facecolor=WHITE, bbox_inches="tight")
plt.close(fig)

# --- Diagnostics ---------------------------------------------------------------
print(f"Saved chart: {OUTPUT_PATH}")
print(f"Lines: {len(base):,} | categories: {len(category_revenue)} | "
      f"sub-categories: {len(subcategory_revenue)} | total: ¥{total_revenue:,.2f}")
print(f"Tile count: {len(tile_records)}")
for category in category_revenue.index:
    print(f"\n{category}  {money(category_revenue[category])}  "
          f"{category_revenue[category] / total_revenue * 100:.2f}%")
    for cat, sub, (sx, sy, sw, sh), rev, share, _ in tile_records:
        if cat != category:
            continue
        print(f"  {sub:6s} {sw:5.2f} x {sh:5.2f} in   {money(rev):>9s}  {share:5.2f}%")
