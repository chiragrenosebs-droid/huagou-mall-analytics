# Discount vs Profit — Scatter Plot

**Chart:** [`output/charts/discount_vs_profit_scatter.png`](../charts/discount_vs_profit_scatter.png)  
**Script:** `scripts/charts/plot_discount_vs_profit_scatter.py`  
**Data:** `data/raw/huagou_mall_synthetic_ecommerce.csv`  
**Population:** Completed order lines with `Revenue_CNY > 0`; Jan 2024 – Dec 2025

---

## Why this view

A scatter plot is the right tool for a two-variable relationship: it preserves every
order line, shows the full profit range, and exposes clusters, outliers, and changes in
spread that a single correlation or average would hide.

**49,327 lines** are plotted. The 3,118 completed lines with zero revenue are excluded
because **all of them have `Profit_CNY = 0`** — including them would draw an artificial
horizontal line at zero across every discount level. Profit is defined as line revenue
after discount minus `Quantity × Unit_Cost_CNY`, before shipping, fees, overhead, or
returns.

### Overplotting and axis choices

- Points are small, semi-transparent teal markers; darker regions mean more overlapping
  lines.
- The y-axis uses a **symlog** scale: linear within ±¥50 and logarithmic beyond. A fully
  linear axis would compress the dense ¥0–¥200 band into a thin strip; a fully
  logarithmic axis cannot show losses.
- An amber line joins the **median profit in 5-percentage-point discount bins** (bins with
  at least 30 lines), and the band spans the interquartile range. This summarises the
  trend without removing the raw points.

---

## Overall relationship

| Statistic | Value |
|---|---:|
| Lines | 49,327 |
| Discount range | 0% – 64.8% |
| Median discount | 12.9% |
| Median profit | ¥30.89 |
| Mean profit | ¥91.38 |
| Loss-making lines | 4,037 (8.18%) |
| Pearson correlation | **−0.253** |
| Spearman rank correlation | **−0.409** |

The relationship is **negative and monotonic**: higher discounts are associated with
lower profit. Spearman is considerably stronger than Pearson because the relationship is
not a straight line — the decline is steady at first, then steepens as discounts pass
about 30%, and the vertical spread collapses at the same time. Discount alone explains
only about **6.4%** of the linear variation in profit (`r² = 0.064`); price, cost, and
quantity still dominate the level of profit on any given line.

The negative sign holds within every product category (Pearson −0.22 to −0.34; Spearman
−0.38 to −0.46), so it is not an artefact of category mix.

---

## Trend by discount band

| Discount | Lines | Median profit | Q1 – Q3 | Loss-making |
|---|---:|---:|---:|---:|
| 0 – 5% | 8,551 | ¥57.70 | ¥22.43 – ¥166.27 | 0.0% |
| 5 – 10% | 10,427 | ¥49.67 | ¥18.57 – ¥143.04 | 0.0% |
| 10 – 15% | 9,149 | ¥38.71 | ¥14.70 – ¥111.71 | 0.0% |
| 15 – 20% | 7,527 | ¥27.59 | ¥9.64 – ¥82.05 | 0.7% |
| 20 – 25% | 5,753 | ¥16.97 | ¥3.78 – ¥58.84 | 12.2% |
| 25 – 30% | 3,661 | ¥9.18 | −¥0.56 – ¥38.76 | 26.9% |
| 30 – 35% | 2,195 | ¥2.60 | −¥8.28 – ¥22.20 | 43.5% |
| 35 – 40% | 1,189 | **−¥2.84** | −¥22.16 – ¥8.34 | 57.4% |
| 40 – 45% | 545 | −¥6.70 | −¥31.61 – ¥2.47 | 68.1% |
| 45 – 50% | 210 | −¥17.29 | −¥53.56 – −¥1.56 | 81.9% |
| 50 – 55% | 83 | −¥26.14 | −¥69.00 – −¥5.42 | 98.8% |
| ≥ 55% | 37 | −¥47.69 | −¥173.02 – −¥12.10 | 100.0% |

- **Median profit is positive up to the 30–35% band** (¥2.60) and turns negative at
  35–40% (−¥2.84). Lines discounted below 20% have a median profit of **¥43.00**, versus
  **¥8.27** at 20% or more.
- **No line below 15% discount is loss-making.** The loss share then rises quickly:
  12.2% at 20–25%, 43.5% at 30–35%, 68.1% at 40–45%, and effectively 100% above 55%.
- **The median profit-margin ratio falls from 32.5%** in the 0–5% band to 3.6% at 30–35%
  and **−45.5%** in the 50–65% band. Margin erosion, not just smaller baskets, drives the
  decline.
- **A minority still profits at high discounts.** About 24% of lines at 40% or more remain
  profitable, usually with small absolute profit; the largest profit above 50% discount
  is only ¥2.36.

The median line in the chart declines by roughly ¥8–11 per 5-point bin through 35%, then
flattens near zero while the loss share keeps rising. The widening gap between the median
line and the upper points at low discounts reflects high-price, high-margin baskets, not
a second trend.

---

## Clusters and shape

1. **Dense low-discount core.** Most lines sit at 5–20% discount with profit between
   roughly ¥0 and ¥200. This is the darkest region of the chart.
2. **A downward-sloping funnel.** At 0–10% discount, profit ranges from near zero to more
   than ¥500. As discount rises, the vertical spread narrows and the whole cloud moves
   below break-even. High discounts do not just lower the average — they remove the
   possibility of large profit.
3. **Break-even band.** Around 20–40% discount, a visible band of lines sits close to
   ¥0, with increasing density below the dashed break-even line.
4. **High-discount loss cluster.** Above 40%, the cloud is sparse, thin, and mostly
   negative. These lines are also lower-revenue: median revenue falls from ¥186 in the
   0–5% band to ¥73 at 50%+ discount, so absolute losses stay smaller than the largest
   low-discount profits.
5. **No high-profit, high-discount cluster.** Profits above ¥500 occur only at discounts
   of 34.9% or less (median 7.5%, 75th percentile 12.5%).

The vertical spread at low discount is driven by product price and quantity as much as by
discount: a 5% discount on a ¥1,500 item can produce far more profit than a 20% discount
on a ¥50 item. The chart is therefore a **discount–profit association**, not a controlled
discount experiment.

---

## Outliers and extreme lines

- **High-profit outliers:** 1,539 lines (3.1%) exceed ¥500 profit. They are concentrated
  at low discounts and are plausible high-ticket, multi-unit baskets. The maximum is
  **¥2,679.10 at 4.3% discount** — 4 units of a ¥1,521.98 product with a ¥786.76 unit cost
  (Sports & Outdoors).
- **Loss outliers:** 261 lines (0.5%) lose more than ¥100, all at discounts of 25.3% or
  more (median 39.3%). The worst is **−¥959.65 at 46.1% discount** — 3 units of a
  ¥1,299.88 product with a ¥1,020.52 unit cost (Digital Electronics).
- **Profit is right-skewed.** Mean profit (¥91.38) is 2.96× the median (¥30.89), and the
  top 1% of lines exceed ¥818. A handful of expensive baskets pull the average up; the
  typical line earns much less.
- **These extremes are not data errors.** They follow mechanically from high unit prices,
  multiple units, and the cost-to-price ratio. They are retained in the chart and are
  highlighted in the annotations.

---

## Observations supported by the chart

1. **Discount and profit move in opposite directions**, but the relationship is
   heteroscedastic: low discounts allow both large profits and near-zero profit; high
   discounts allow little upside and increasing losses.
2. **The break-even threshold sits around 35% discount** for the median line. Below 15%,
   no line is loss-making; above 55%, essentially every line is.
3. **The loss share accelerates before the median turns negative.** At 20–25% discount the
   median is still +¥16.97, but 12.2% of lines already lose money — the average hides a
   growing loss-making tail.
4. **High profit requires low discount in this dataset.** Every line above ¥500 profit has
   a discount below 35%, and no line above 50% discount earns more than ¥2.36.
5. **Category does not reverse the pattern.** The rank correlation is negative in all
   eight categories, ranging from −0.38 to −0.46.
6. **Discount is not destiny.** Many high-discount lines remain marginally profitable
   because their cost-to-price ratio is low. Discount percentage alone cannot identify
   loss-making lines; unit cost and quantity are required.

---

## Limitations

- **Observational, not causal.** Discounts are not randomly assigned. Products, channels,
  campaigns, and customer segments may differ systematically across discount levels.
- **Discount depth is confounded with basket value.** Median revenue falls as discount
  rises, so absolute profit mixes margin erosion with a shift toward cheaper items. The
  margin figures help separate the two, but do not remove the confounding.
- **Gross line profit only.** Profit is after line discount but before shipping, payment
  fees, returns, overhead, tax, or platform commissions.
- **Line grain, not order grain.** The unit is the order line; totals across lines in one
  order are not netted here.
- **Symlog distorts visual distance.** The axis is linear only within ±¥50 and logarithmic
  beyond, so equal vertical gaps do not represent equal CNY differences. The binned table
  gives exact values.
- **Sparse high-discount tail.** Only 83 lines sit at 50–55% discount and 37 above 55%;
  medians and loss rates there are less stable than in the main body.
- **Bin medians are summaries.** The amber line stops at 50–55% because later bins have
  fewer than 30 lines; the scatter still shows those points.
- **Excluded zero-revenue lines.** The 3,118 excluded rows are real completed records,
  likely voided or zeroed transactions, and all have zero profit.
- **Synthetic data.** The patterns are generated and should not be treated as market
  evidence.

---

## Bottom line

Profit falls as discount rises, but not at a constant rate. Median profit drops from
about ¥58 at 0–5% discount to zero around 35%, while the share of loss-making lines climbs
from 0% below 15% to nearly 100% above 55%. The scatter shows why an average is
insufficient: low-discount lines span a wide profit range, high-discount lines collapse
toward losses, and a small set of high-ticket baskets dominates the upper tail. Discount
is a strong directional signal, but unit cost, price, and quantity determine whether a
given discount is actually profitable.
