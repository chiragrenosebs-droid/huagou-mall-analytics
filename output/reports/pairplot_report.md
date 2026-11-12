# Price, Quantity, Revenue and Profit — Pair Plot

**Chart:** [`output/charts/price_quantity_revenue_profit_pairplot.png`](../charts/price_quantity_revenue_profit_pairplot.png)  
**Script:** `scripts/charts/plot_pairplot.py`  
**Data:** `data/raw/huagou_mall_synthetic_ecommerce.csv`  
**Population:** Completed order lines with `Revenue_CNY > 0`; Jan 2024 – Dec 2025

---

## Why this view

The previous charts examined one variable at a time and then one relationship at a
time. A pair plot puts all four numeric drivers side by side: each **diagonal** shows
the distribution of a single variable, each **lower-triangle panel** shows a pairwise
scatter, and each **upper-triangle panel** reports the **Spearman rank correlation**.
That makes it possible to see which pairs are genuinely linked, which are independent,
and where the apparent trends in profit actually come from.

**49,327 lines** are plotted. The 3,118 completed lines with zero revenue are excluded,
as in Chart 5, because all of them have `Profit_CNY = 0` and would create an artificial
band on every profit axis.

### Handling skew and overplotting

- **Unit price and revenue use log10 axes.** Both are strongly right-skewed (raw skew
  1.62 and 3.45), but their logarithms are almost symmetric (skew 0.01 and 0.06). Log
  axes turn the compressed long tail into a readable spread while keeping zero-revenue
  lines out of the picture.
- **Profit uses `sign(p) × log10(1 + |p|)`.** This single scale shows losses down to
  −¥959.65 and profits up to ¥2,679.10; a plain log axis cannot show negatives and a
  plain linear axis would flatten the typical ¥0–¥200 range.
- **Quantity stays linear and discrete**, shown as five bars on the diagonal.
- **Scatter points are small, semi-transparent and rasterised**, so dense regions darken
  instead of turning into solid blocks while isolated outliers remain visible.
- The diagonal histograms are drawn over 58 bins with median markers; the quantity bars
  are labelled with their share of lines.

---

## Pairwise relationships

| Pair | Spearman ρ | Reading |
|---|---:|---|
| Unit price – Quantity | **+0.004** | No relationship at all |
| Unit price – Revenue | **+0.940** | Very strong, near-linear on log axes |
| Unit price – Profit | **+0.699** | Strong, with a widening fan |
| Quantity – Revenue | **+0.314** | Moderate; each unit multiplies revenue |
| Quantity – Profit | **+0.236** | Weak–moderate; profit rises with units |
| Revenue – Profit | **+0.779** | Strong and broadly proportional |

### Unit price and quantity are independent

The price–quantity panel is a set of horizontal stripes at 1–5 units with no tilt, and
the rank correlation is **+0.004**. Median unit price is essentially flat across
quantities (¥154.01, ¥155.02, ¥154.01, ¥156.16, ¥157.43). Customers do not buy cheaper
items in larger quantities, and there is no volume-based price ladder in the data.

### Price and revenue form a tight diagonal ridge

On log–log axes the price–revenue cloud is a narrow band running from lower left to
upper right (ρ = **+0.940**; Pearson on the logs = 0.936). The width of that band is the
joint effect of quantity and discount: the revenue-to-price ratio has a median of 0.92,
a 5th percentile of 0.69, and a 95th percentile of 2.84. In other words, revenue is
approximately `price × quantity × (1 − discount)`, and the panel makes that mechanical
identity visible. The upper edge of the band is multi-unit baskets; the lower edge is
single units with deep discounts.

### Quantity raises revenue and profit in steps

Revenue and profit both step upward with each additional unit. Median revenue rises
**¥128.82 → ¥258.44 → ¥391.79 → ¥514.92 → ¥666.51** for quantities 1–5, and median
profit rises **¥23.45 → ¥47.21 → ¥73.91 → ¥93.23 → ¥134.96**. Because the median
profit margin is almost constant across quantities (23.8%–25.3%), extra units add profit
roughly in proportion to the extra revenue rather than improving or eroding margin.
Quantity is nevertheless a minor driver overall: **70.4%** of lines are single-unit and
quantity 5 is only **0.98%** of lines and **3.22%** of revenue.

### Revenue and profit are strongly and almost proportionally linked

Profit tracks revenue closely (ρ = **+0.779**), and the relationship is close to a fixed
percentage: the median profit margin is **23.9%**, and the median margin within revenue
bands is remarkably stable at **22.8%–29.4%**. The panel therefore looks like a diagonal
band with a constant vertical offset, not a curve. The scatter around the band is
cost-to-price variation and discount depth, not a separate revenue effect.

### Price lifts profit but widens its range

The price–profit panel is a fan: at low prices profit is tightly clustered near zero,
while at high prices it ranges from large gains to substantial losses. Price correlates
with profit at ρ = **+0.699**, but the fan shape shows that price alone does not
determine profit — unit cost and discount decide where in the fan a line lands.

---

## Patterns and clusters

1. **A multiplicative core.** Revenue ≈ price × quantity × (1 − discount) produces the
   strong diagonal in the price–revenue panel and the stepped columns in the
   quantity–revenue panel. The price–quantity panel is empty of structure, which is
   exactly what makes the other two readable.
2. **Five vertical quantity strips.** In every panel involving quantity, points fall on
   the integers 1–5. The strips are dense at 1–2 units and sparse at 4–5.
3. **A constant-margin band.** Revenue–profit points sit along a slope of roughly one on
   log–log axes, with most lines between 15% and 30% margin. This is the single clearest
   cluster in the matrix.
4. **A loss cloud below zero.** Loss-making lines appear as points under the profit = 0
   reference line in the profit panels. They occur at **every** quantity and across the
   revenue range, but are concentrated at lower revenue: **63%** of the 4,037 loss lines
   have revenue below ¥200.
5. **No high-price–low-quantity cluster.** Expensive items are bought in the same 1–5
   unit pattern as cheap ones; there is no visible premium-basket segment.
6. **The diagonal shapes differ sharply.** Price and revenue are broad, smooth,
   log-normal-like distributions; quantity is a spike at 1; profit is a narrow peak just
   above zero with a long right tail and a small negative shoulder.

---

## Distributions and potential outliers

| Variable | Median | Mean | Range | Shape |
|---|---:|---:|---|---|
| Unit price | ¥154.01 | ¥297.34 | ¥6.96 – ¥1,538.13 | Right-skewed; near log-normal |
| Quantity | 1 | 1.45 | 1 – 5 | Discrete; 70.4% at 1 |
| Revenue | ¥163.84 | ¥369.43 | ¥3.52 – ¥7,105.00 | Strongly right-skewed |
| Profit | ¥30.89 | ¥91.38 | −¥959.65 – ¥2,679.10 | Very right-skewed; 8.18% negative |

- **The mean is not the typical line.** Mean profit (¥91.38) is 2.96× the median
  (¥30.89), and the top decile starts at ¥258. The right tail is real but small.
- **High-revenue outliers:** 360 lines exceed ¥3,000; 1,145 lines (2.3%) sit in the
  ¥2,000+ band. These are high-price, multi-unit, low-discount baskets.
- **High-profit outliers:** 316 lines exceed ¥1,000. Every one of them has a discount of
  **26.2% or less** (median 6.7%), which is consistent with Chart 5.
- **Loss outliers:** 261 lines lose more than ¥100. The worst is **−¥959.65** at 46.1%
  discount, a 3-unit line of a ¥1,299.88 product with a ¥1,020.52 unit cost.
- **Loss profile:** the typical loss-making line has a median revenue of only ¥123.17, a
  median unit price of ¥148.27, is single-unit (71.8%), and carries a **31.3%** median
  discount. Losses are a discount-and-cost phenomenon, not a low-price phenomenon.
- **Extremes are mechanically plausible.** They follow from high unit prices, multiple
  units, and cost-to-price ratios; the profit identity matches to the cent. They are
  retained rather than trimmed.

---

## How this extends the discount–profit scatter (Chart 5)

Chart 5 showed that profit falls as discount rises (Spearman **−0.409**), with the
median crossing zero near 35% discount. The pair plot places that finding in context:

1. **Discount is one driver among four, and not the strongest correlate of profit
   level.** Profit's rank correlations with revenue (**+0.779**) and price (**+0.699**)
   are larger in magnitude than its correlation with discount (−0.409). Discount shifts
   the *margin*, while price and quantity set the *size* of the basket the margin applies
   to.
2. **The spread in Chart 5 is explained by the other variables.** At a fixed discount,
   Chart 5 showed a wide vertical band of profit. The pair plot shows why: high-price,
   multi-unit baskets can earn hundreds of yuan at the same discount where a cheap
   single-unit line earns a few yuan. Price and quantity are the fan, discount is the
   tilt.
3. **Losses are concentrated where Chart 5 said they would be.** The loss cloud sits at
   high discount and low-to-mid revenue; the typical loss line carries a 31.3% discount.
   High-revenue lines are rarely loss-making (2.0% in the ¥2,000+ band), because their
   absolute margin absorbs the discount.
4. **High profit still requires low discount.** The pair plot reinforces the Chart 5
   ceiling: all 316 lines above ¥1,000 profit have discounts ≤26.2%. No combination of
   high price and high quantity overcomes a deep discount.
5. **The margin signal is visible directly.** Discount correlates −0.563 with the
   profit-to-revenue ratio, while the revenue–profit band stays at a stable 23.9%
   margin. The pair plot therefore separates the two effects Chart 5 mixed: basket size
   (price × quantity) and margin erosion (discount).

---

## Limitations

- **Observational and synthetic.** No causal claim is possible; discounts are not
  randomly assigned and the data are generated.
- **Mechanical correlation.** `Profit_CNY = Revenue_CNY − Quantity × Unit_Cost_CNY`, so
  the revenue–profit and quantity–profit relationships are partly definitional rather
  than independent findings.
- **Unit cost is not in the matrix.** It is the main omitted driver: two lines with the
  same price, quantity and discount can have very different profit.
- **Line grain, not order grain.** Lines from the same order are not aggregated or
  netted.
- **Rank correlations only.** Spearman ρ measures monotonic association, not effect
  size; the log and signed-log axes also change visual distances, so the panels show
  shape rather than linear slope.
- **Discrete quantity.** With only five values, the quantity panels are strips rather
  than clouds, and the quantity correlations are correspondingly coarse.
- **Heavy overplotting remains.** Transparency and rasterisation make density readable
  but do not recover exact counts in the darkest regions; the diagonal and the tables
  above supply the precise figures.
- **Gross line profit only.** Before shipping, fees, returns, overhead, tax, or platform
  commissions.
- **Excluded zero-revenue lines.** 3,118 completed rows with `Revenue_CNY = 0` and
  `Profit_CNY = 0`; including them would add a false horizontal band at zero.

---

## Bottom line

Price and quantity are independent, but together they multiply into revenue, and revenue
carries profit almost proportionally at a stable ~24% margin. That is why the pair plot
is dominated by two strong diagonals — price–revenue (ρ = 0.940) and revenue–profit
(ρ = 0.779) — while price–quantity is flat (ρ = 0.004). The loss-making lines are a
minority (8.18%) concentrated at low-to-mid revenue and high discount, exactly the region
Chart 5 identified. Profit is therefore best read as **basket value × margin**: price and
quantity set the value, discount and unit cost set the margin.
