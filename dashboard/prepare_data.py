"""Data preparation and verification script for HuaGou Mall Dashboard.

Reads the immutable CSV, validates every metric against output/reports/,
and generates a structured, lightweight dashboard/data.js and dashboard/data.json
for the standalone web dashboard.
"""

import json
from pathlib import Path
import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "huagou_mall_synthetic_ecommerce.csv"
DASHBOARD_DIR = PROJECT_ROOT / "dashboard"
OUTPUT_JS = DASHBOARD_DIR / "data.js"
OUTPUT_JSON = DASHBOARD_DIR / "data.json"

print(f"Loading data from {DATA_PATH}...")
df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df["Year"] = df["Order_Date"].dt.year
df["Month"] = df["Order_Date"].dt.month
df["YearMonth"] = df["Order_Date"].dt.strftime("%Y-%m")

# Verification 1: Overall dataset shape
assert len(df) == 60000, f"Expected 60000 rows, got {len(df)}"
assert df["Order_ID"].nunique() == 31804, f"Expected 31804 orders, got {df['Order_ID'].nunique()}"
assert df["Customer_ID"].nunique() == 15000, f"Expected 15000 customers, got {df['Customer_ID'].nunique()}"
assert df["Product_ID"].nunique() == 500, f"Expected 500 products, got {df['Product_ID'].nunique()}"

# Verification 2: Completed population
completed = df[df["Order_Status"] == "Completed"].copy()
assert len(completed) == 52445, f"Expected 52445 completed lines, got {len(completed)}"
assert completed["Order_ID"].nunique() == 27826, f"Expected 27826 completed orders, got {completed['Order_ID'].nunique()}"

# Verification 3: Revenue-bearing completed population
realized = completed[completed["Revenue_CNY"] > 0].copy()
assert len(realized) == 49327, f"Expected 49327 revenue-bearing completed lines, got {len(realized)}"

total_realized_rev = realized["Revenue_CNY"].sum()
total_realized_prof = realized["Profit_CNY"].sum()
assert abs(total_realized_rev - 18222902.98) < 1.0, f"Revenue mismatch: {total_realized_rev}"
assert abs(total_realized_prof - 4507434.50) < 1.0, f"Profit mismatch: {total_realized_prof}"

med_rev = realized["Revenue_CNY"].median()
mean_rev = realized["Revenue_CNY"].mean()
assert abs(med_rev - 163.84) < 0.05, f"Median revenue mismatch: {med_rev}"
assert abs(mean_rev - 369.43) < 0.05, f"Mean revenue mismatch: {mean_rev}"

# Verification 4: Loss lines & correlations
loss_lines = (realized["Profit_CNY"] < 0).sum()
assert loss_lines == 4037, f"Expected 4037 loss lines, got {loss_lines}"

p_disc_prof = realized["Discount_Percentage"].corr(realized["Profit_CNY"])
s_disc_prof = realized["Discount_Percentage"].rank().corr(realized["Profit_CNY"].rank())
assert abs(p_disc_prof - (-0.253)) < 0.01, f"Pearson mismatch: {p_disc_prof}"
assert abs(s_disc_prof - (-0.409)) < 0.01, f"Spearman mismatch: {s_disc_prof}"

# Verification 5: Pairplot Spearman correlations
s_up_q = realized["Unit_Price_CNY"].rank().corr(realized["Quantity"].rank())
s_up_rev = realized["Unit_Price_CNY"].rank().corr(realized["Revenue_CNY"].rank())
s_up_prof = realized["Unit_Price_CNY"].rank().corr(realized["Profit_CNY"].rank())
s_q_rev = realized["Quantity"].rank().corr(realized["Revenue_CNY"].rank())
s_q_prof = realized["Quantity"].rank().corr(realized["Profit_CNY"].rank())
s_rev_prof = realized["Revenue_CNY"].rank().corr(realized["Profit_CNY"].rank())

assert abs(s_up_q - 0.004) < 0.005, f"s_up_q mismatch: {s_up_q}"
assert abs(s_up_rev - 0.940) < 0.005, f"s_up_rev mismatch: {s_up_rev}"
assert abs(s_up_prof - 0.699) < 0.005, f"s_up_prof mismatch: {s_up_prof}"
assert abs(s_q_rev - 0.314) < 0.005, f"s_q_rev mismatch: {s_q_rev}"
assert abs(s_q_prof - 0.236) < 0.005, f"s_q_prof mismatch: {s_q_prof}"
assert abs(s_rev_prof - 0.779) < 0.005, f"s_rev_prof mismatch: {s_rev_prof}"

print("✓ All statistical assertions against output/reports/ PASSED!")

# --- Prepare Chart 1 Data: Revenue Histogram ---
log_bins = np.logspace(np.log10(realized["Revenue_CNY"].min()), np.log10(realized["Revenue_CNY"].max()), 72)
counts, bin_edges = np.histogram(realized["Revenue_CNY"], bins=log_bins)
bin_centers = np.sqrt(bin_edges[:-1] * bin_edges[1:])  # geometric centers for log bins
histogram_data = {
    "bin_edges": bin_edges.tolist(),
    "bin_centers": bin_centers.tolist(),
    "counts": counts.tolist(),
    "shares": (counts / len(realized) * 100).round(3).tolist(),
    "n": len(realized),
    "min": float(realized["Revenue_CNY"].min()),
    "max": float(realized["Revenue_CNY"].max()),
    "median": float(med_rev),
    "mean": float(mean_rev),
    "q1": float(realized["Revenue_CNY"].quantile(0.25)),
    "q3": float(realized["Revenue_CNY"].quantile(0.75)),
    "p95": float(realized["Revenue_CNY"].quantile(0.95)),
    "p99": float(realized["Revenue_CNY"].quantile(0.99)),
}

# --- Prepare Chart 2 Data: Revenue KDE ---
log_rev = np.log10(realized["Revenue_CNY"].to_numpy())
std_log = log_rev.std(ddof=1)
iqr_log = np.subtract(*np.percentile(log_rev, [75, 25]))
bandwidth = 0.9 * min(std_log, iqr_log / 1.34) * (len(realized) ** (-0.2))
grid_log = np.linspace(log_rev.min() - 3 * bandwidth, log_rev.max() + 3 * bandwidth, 250)

def compute_kde(values, grid, h):
    density = np.zeros_like(grid)
    norm = 1.0 / (len(values) * h * np.sqrt(2.0 * np.pi))
    for start in range(0, len(values), 4096):
        z = (grid[:, None] - values[None, start : start + 4096]) / h
        density += np.exp(-0.5 * z * z).sum(axis=1)
    return density * norm

kde_dens = compute_kde(log_rev, grid_log, bandwidth)
grid_rev = 10.0 ** grid_log
kde_data = {
    "grid_rev": grid_rev.round(2).tolist(),
    "density": kde_dens.round(5).tolist(),
    "bandwidth": float(bandwidth),
}

# --- Prepare Chart 3 & 4 Data: Category Box Plot & Violin Data ---
CATEGORY_EN = {
    "运动户外": "Sports & Outdoors",
    "数码电子": "Digital Electronics",
    "服饰鞋包": "Apparel & Bags",
    "美妆个护": "Beauty & Personal Care",
    "食品饮料": "Food & Beverage",
    "母婴用品": "Mother & Baby",
    "家居生活": "Home & Living",
    "图书文具": "Books & Stationery",
}

category_summary = []
category_box_data = {}
category_violin_kde = {}

for cat, sub in realized.groupby("Category"):
    vals = sub["Revenue_CNY"]
    q1, q3 = vals.quantile([0.25, 0.75])
    iqr = q3 - q1
    lf = max(vals.min(), q1 - 1.5 * iqr)
    uf = min(vals.max(), q3 + 1.5 * iqr)
    outliers = vals[(vals < lf) | (vals > uf)]
    
    # KDE for violin
    sub_log = np.log10(vals.to_numpy())
    sub_std = sub_log.std(ddof=1)
    sub_iqr = np.subtract(*np.percentile(sub_log, [75, 25]))
    sub_h = 0.9 * min(sub_std, (sub_iqr / 1.34) if sub_iqr > 0 else sub_std) * (len(vals) ** (-0.2))
    sub_grid = np.linspace(sub_log.min(), sub_log.max(), 100)
    sub_dens = compute_kde(sub_log, sub_grid, sub_h)
    
    cat_info = {
        "category": cat,
        "name_en": CATEGORY_EN.get(cat, cat),
        "n": len(vals),
        "revenue": float(vals.sum()),
        "profit": float(sub["Profit_CNY"].sum()),
        "median": float(vals.median()),
        "q1": float(q1),
        "q3": float(q3),
        "iqr": float(iqr),
        "lower_fence": float(lf),
        "upper_fence": float(uf),
        "min": float(vals.min()),
        "max": float(vals.max()),
        "outlier_count": int(len(outliers)),
    }
    category_summary.append(cat_info)
    
    # Store sampled raw points for violin/box plot representation
    sample_size = min(600, len(vals))
    category_box_data[cat] = {
        "sampled_vals": vals.sample(sample_size, random_state=42).round(2).tolist(),
        "stats": cat_info,
    }
    category_violin_kde[cat] = {
        "grid_rev": (10.0 ** sub_grid).round(2).tolist(),
        "density": sub_dens.round(4).tolist(),
    }

# Sort summary by median descending
category_summary.sort(key=lambda x: x["median"], reverse=True)

# --- Prepare Chart 5 Data: Discount vs Profit ---
bin_edges_disc = np.arange(0, 70, 5)
realized["disc_bin"] = pd.cut(realized["Discount_Percentage"], bin_edges_disc, right=False, include_lowest=True)
grouped_disc = realized.groupby("disc_bin", observed=True)["Profit_CNY"]
disc_bins = []
for b, g in grouped_disc:
    if len(g) >= 30:
        disc_bins.append({
            "mid": float(b.mid),
            "n": int(len(g)),
            "median": float(g.median()),
            "q25": float(g.quantile(0.25)),
            "q75": float(g.quantile(0.75)),
        })

# Sample 3,000 points stratified by discount for clean, fast scatter rendering
scatter_sample = realized.sample(3500, random_state=42)[
    ["Discount_Percentage", "Profit_CNY", "Revenue_CNY", "Category", "Quantity", "Unit_Price_CNY"]
].round(2).to_dict(orient="records")

discount_vs_profit_data = {
    "trend_bins": disc_bins,
    "sample_points": scatter_sample,
    "overall_pearson": float(round(p_disc_prof, 3)),
    "overall_spearman": float(round(s_disc_prof, 3)),
    "loss_count": int(loss_lines),
    "loss_rate": float(round(loss_lines / len(realized) * 100, 2)),
}

# --- Prepare Chart 7 Data: Unit Price vs Profit Bubble Plot ---
realized["price_decile"] = pd.qcut(realized["Unit_Price_CNY"], 10, duplicates="drop")
bubble_trend = []
for dec, g in realized.groupby("price_decile", observed=True):
    bubble_trend.append({
        "x": float(g["Unit_Price_CNY"].median()),
        "median": float(g["Profit_CNY"].median()),
        "n": int(len(g)),
    })

bubble_data = {
    "trend": bubble_trend,
    "sample_bubbles": scatter_sample,  # includes Unit_Price_CNY, Profit_CNY, Quantity, Category
    "spearman": float(round(s_up_prof, 3)),
    "pearson": float(round(realized["Unit_Price_CNY"].corr(realized["Profit_CNY"]), 3)),
}

# --- Prepare Chart 6 Data: Pairplot ---
pairplot_data = {
    "correlations": {
        "Unit_Price_CNY": {
            "Quantity": float(round(s_up_q, 3)),
            "Revenue_CNY": float(round(s_up_rev, 3)),
            "Profit_CNY": float(round(s_up_prof, 3)),
        },
        "Quantity": {
            "Revenue_CNY": float(round(s_q_rev, 3)),
            "Profit_CNY": float(round(s_q_prof, 3)),
        },
        "Revenue_CNY": {
            "Profit_CNY": float(round(s_rev_prof, 3)),
        },
    },
    "variables": [
        {"key": "Unit_Price_CNY", "label": "Unit Price (CNY)", "min": float(realized["Unit_Price_CNY"].min()), "max": float(realized["Unit_Price_CNY"].max()), "median": float(realized["Unit_Price_CNY"].median())},
        {"key": "Quantity", "label": "Quantity (Units)", "min": 1, "max": 5, "median": float(realized["Quantity"].median())},
        {"key": "Revenue_CNY", "label": "Revenue (CNY)", "min": float(realized["Revenue_CNY"].min()), "max": float(realized["Revenue_CNY"].max()), "median": float(med_rev)},
        {"key": "Profit_CNY", "label": "Profit (CNY)", "min": float(realized["Profit_CNY"].min()), "max": float(realized["Profit_CNY"].max()), "median": float(realized["Profit_CNY"].median())},
    ],
    "sample": realized.sample(1500, random_state=42)[["Unit_Price_CNY", "Quantity", "Revenue_CNY", "Profit_CNY"]].round(2).to_dict(orient="records")
}

# --- Prepare Chart 8 Data: Treemap (Category -> Subcategory) ---
subcat_grouped = realized.groupby(["Category", "Subcategory"]).agg(
    revenue=("Revenue_CNY", "sum"),
    profit=("Profit_CNY", "sum"),
    lines=("Order_ID", "count"),
).reset_index()

treemap_nodes = []
# Grand total node
treemap_nodes.append({
    "id": "Total",
    "label": "All Categories",
    "parent": "",
    "value": float(round(total_realized_rev, 2)),
    "profit": float(round(total_realized_prof, 2)),
    "lines": int(len(realized)),
})

for cat, g in realized.groupby("Category"):
    cat_rev = float(round(g["Revenue_CNY"].sum(), 2))
    cat_prof = float(round(g["Profit_CNY"].sum(), 2))
    treemap_nodes.append({
        "id": cat,
        "label": f"{cat} ({CATEGORY_EN.get(cat, '')})",
        "parent": "Total",
        "value": cat_rev,
        "profit": cat_prof,
        "lines": int(len(g)),
    })

for _, row in subcat_grouped.iterrows():
    treemap_nodes.append({
        "id": f"{row['Category']}-{row['Subcategory']}",
        "label": row["Subcategory"],
        "parent": row["Category"],
        "value": float(round(row["revenue"], 2)),
        "profit": float(round(row["profit"], 2)),
        "lines": int(row["lines"]),
    })

# --- Prepare Chart 9 Data: Category x Month Heatmap ---
heatmap_matrix = []
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
cat_order_by_rev = realized.groupby("Category")["Revenue_CNY"].sum().sort_values(ascending=False).index.tolist()

heat_data = realized.groupby(["Category", "Month"])["Revenue_CNY"].sum().unstack(fill_value=0)
z_values = []
annotations = []
for cat in cat_order_by_rev:
    row_vals = [float(round(heat_data.loc[cat, m], 2)) for m in range(1, 13)]
    z_values.append(row_vals)

heatmap_data = {
    "categories": cat_order_by_rev,
    "categories_en": [f"{c} · {CATEGORY_EN.get(c, '')}" for c in cat_order_by_rev],
    "months": months,
    "z": z_values,
}

# --- Prepare Overview & Filter-Responsive Multi-dimensional Data ---
# Pre-aggregate across filter dimensions (Year, Category, Sales_Channel, Customer_Segment, Order_Status)
slice_grouped = df.groupby(
    ["Year", "Category", "Sales_Channel", "Customer_Segment", "Order_Status"],
    observed=True,
).agg(
    total_rev=("Revenue_CNY", "sum"),
    realized_rev=("Revenue_CNY", lambda s: s[df.loc[s.index, "Order_Status"] == "Completed"].sum()),
    total_prof=("Profit_CNY", "sum"),
    realized_prof=("Profit_CNY", lambda s: s[df.loc[s.index, "Order_Status"] == "Completed"].sum()),
    total_lines=("Order_ID", "count"),
    realized_lines=("Order_ID", lambda s: (df.loc[s.index, "Order_Status"] == "Completed").sum()),
    positive_rev_lines=("Order_ID", lambda s: ((df.loc[s.index, "Order_Status"] == "Completed") & (df.loc[s.index, "Revenue_CNY"] > 0)).sum()),
    loss_lines=("Profit_CNY", lambda s: ((df.loc[s.index, "Order_Status"] == "Completed") & (df.loc[s.index, "Revenue_CNY"] > 0) & (s < 0)).sum()),
    distinct_orders=("Order_ID", "nunique"),
    distinct_customers=("Customer_ID", "nunique"),
    avg_rating=("Customer_Rating", "mean"),
).reset_index()

# Monthly timeline for trend chart (by Year-Month and Channel)
monthly_trend = df.groupby(["YearMonth", "Year", "Month", "Order_Status"]).agg(
    revenue=("Revenue_CNY", "sum"),
    profit=("Profit_CNY", "sum"),
    orders=("Order_ID", "nunique"),
    lines=("Order_ID", "count"),
).reset_index().round(2)

# Global dataset summary packet
summary_packet = {
    "metadata": {
        "name": "HuaGou Mall E-Commerce Analytics",
        "currency": "CNY (¥)",
        "period": "2024-01-01 to 2025-12-31",
        "total_records": 60000,
        "total_orders": 31804,
        "completed_orders": 27826,
        "completed_lines": 52445,
        "revenue_bearing_lines": 49327,
        "realized_revenue": float(round(total_realized_rev, 2)),
        "realized_profit": float(round(total_realized_prof, 2)),
        "realized_margin": float(round(total_realized_prof / total_realized_rev * 100, 2)),
        "loss_lines_count": int(loss_lines),
        "loss_lines_pct": float(round(loss_lines / len(realized) * 100, 2)),
        "aov": float(round(total_realized_rev / 27826, 2)),
    },
    "categories": list(CATEGORY_EN.keys()),
    "category_labels": CATEGORY_EN,
    "channels": sorted(df["Sales_Channel"].unique().tolist()),
    "segments": sorted(df["Customer_Segment"].unique().tolist()),
    "statuses": sorted(df["Order_Status"].unique().tolist()),
    "years": [2024, 2025],
    "chart1_histogram": histogram_data,
    "chart2_kde": kde_data,
    "chart3_box": {
        "categories": [c["category"] for c in category_summary],
        "categories_en": [c["name_en"] for c in category_summary],
        "summary": category_summary,
        "details": category_box_data,
    },
    "chart4_violin": category_violin_kde,
    "chart5_discount_profit": discount_vs_profit_data,
    "chart6_pairplot": pairplot_data,
    "chart7_bubbles": bubble_data,
    "chart8_treemap": treemap_nodes,
    "chart9_heatmap": heatmap_data,
    "monthly_trend": monthly_trend.to_dict(orient="records"),
    "slices": slice_grouped.round(2).to_dict(orient="records"),
}

print("Serializing data to JSON and JS...")
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(summary_packet, f, ensure_ascii=False, indent=2)

with open(OUTPUT_JS, "w", encoding="utf-8") as f:
    f.write("window.HUAGOU_DATA = ")
    json.dump(summary_packet, f, ensure_ascii=False, indent=2)
    f.write(";\n")

print(f"✓ Created {OUTPUT_JSON} ({OUTPUT_JSON.stat().st_size / 1024:.1f} KB)")
print(f"✓ Created {OUTPUT_JS} ({OUTPUT_JS.stat().st_size / 1024:.1f} KB)")
print("Phase 1 data preparation and verification complete!")
