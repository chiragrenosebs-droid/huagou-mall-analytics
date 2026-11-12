# Unit Price vs Profit — Bubble Plot with Quantity

**Chart:** [`output/charts/price_profit_quantity_bubbles.png`](../charts/price_profit_quantity_bubbles.png)  
**Script:** `scripts/charts/plot_price_profit_bubbles.py`  
**Data:** `data/raw/huagou_mall_synthetic_ecommerce.csv`  
**Population:** Completed order lines with `Revenue_CNY > 0`; Jan 2024 – Dec 2025

---

## How to read the three encoded variables

| Channel | Variable | What it shows |
|---|---|---|
| Horizontal position | `Unit_Price_CNY` | Price of one unit, on a **log10 axis** |
| Vertical position | `Profit_CNY` | Profit for the whole line, on a **symlog axis** |
| Bubble **area** | `Quantity` | Number of units on the line (1–5) |

- **Area, not diameter, is proportional to quantity.** A 2-unit bubble has twice the
  area of a 1-unit bubble, so its diameter is only about 1.41× larger. The size legend
  is the reliable way to read the values; the five levels are 1–5 units.
- **Position is the primary encoding.** Read left-to-right for price and bottom-to-top
  for profit first; bubble size is a secondary, coarser signal.
- **The x-axis is logarithmic.** Prices span ¥6.96–¥1,538, so a linear axis would crush
  80% of lines into the left quarter. Equal horizontal distances are therefore not equal
  CNY differences.
- **The y-axis is symlog** (linear within ±¥50, logarithmic beyond). This keeps the
  dense near-zero region readable while still showing losses down to −¥959.65 and profits
  up to ¥2,679.10. Equal vertical distances are not equal CNY differences.
- **Transparency handles overplotting.** Darker regions contain many overlapping lines.
  Bubbles are drawn from smallest to largest quantity so the rarer 4- and 5-unit bubbles
  stay visible. Opacity also rises slightly with bubble size for legibility; it is **not**
  a fourth variable.
- Each bubble is **one order line**, not one unit and not one order. A 5-unit bubble is
  still a single observation; the encoding does not weight lines by revenue.

**Population:** 49,327 lines. The 3,118 completed zero-revenue lines are excluded because
all have `Profit_CNY = 0` and would form an artificial row on the break-even line.

---

## Overall relationship

| Statistic | Value |
|---|---:|
| Lines | 49,327 |
| Median unit price | ¥154.01 |
| Median profit | ¥30.89 |
| Mean profit | ¥91.38 |
| Loss-making lines | 4,037 (8.18%) |
| Pearson correlation | **+0.649** |
| Spearman rank correlation | **+0.699** |

Profit rises strongly and monotonically with unit price. The rank correlation is higher
than the linear one because the monetary relationship is multiplicative and the spread
widens as price increases. The amber line — median profit by price decile — climbs from
**¥5.31** in the cheapest decile to **¥308.37** in the most expensive one.

| Unit-price band | Lines | Median profit | Q1 – Q3 | Loss share |
|---|---:|---:|---:|---:|
| < ¥25 | 3,345 | ¥4.47 | ¥2.38 – ¥7.62 | 7.3% |
| ¥25 – 50 | 6,248 | ¥9.65 | ¥4.87 – ¥15.76 | 8.2% |
| ¥50 – 100 | 10,164 | ¥17.51 | ¥9.05 – ¥28.61 | 7.9% |
| ¥100 – 200 | 8,857 | ¥32.65 | ¥14.95 – ¥55.21 | 9.9% |
| ¥200 – 400 | 8,732 | ¥65.90 | ¥32.27 – ¥107.60 | 9.3% |
| ¥400 – 800 | 6,299 | ¥139.19 | ¥73.85 – ¥229.56 | 7.3% |
| ¥800 – 1,600 | 5,682 | ¥293.56 | ¥168.03 – ¥451.80 | 5.8% |

The **5th–95th percentile spread** grows from −¥0.68 – ¥16.64 in the cheapest band to
−¥16.17 – ¥1,007.17 in the most expensive. Higher prices lift the median but also widen
the range: expensive lines can be very profitable or lose money.

---

## Visible clusters and patterns

1. **A dense low-price core.** About **40%** of lines have a unit price below ¥100, and
   **95%** of those sit under ¥50 profit. This is the darkest part of the plot.
2. **A rising, widening fan.** At low prices the cloud is thin and close to zero. As
   price increases, the cloud fans upward: the ceiling rises much faster than the floor.
   The fan shape is the dominant visual signature of the chart.
3. **A higher ceiling for larger bubbles.** At any given price, multi-unit bubbles sit
   systematically above single-unit ones. Median profit per line by quantity is
   **¥23.45 → ¥47.21 → ¥73.91 → ¥93.23 → ¥134.96** for 1–5 units. The median
   profit-to-price ratio is **0.207, 0.420, 0.631, 0.802, 1.113** — almost exactly
   proportional to quantity, which is why the largest bubbles reach the top of the fan.
4. **High profit requires both high price and multiple units.** **86.4%** of lines above
   ¥500 profit are multi-unit, and **all 316** lines above ¥1,000 profit have quantity
   2–5. Their median price is ¥1,065.79. A single cheap unit cannot produce a large
   absolute profit.
5. **A loss band below break-even.** Losses appear across the entire price range; the
   loss share is 5.8%–9.9% by price band and does not disappear at high prices. The
   **largest absolute losses** are large bubbles at high prices, where a deep discount
   overwhelms a high unit price.
6. **Vertical striping.** Prices are product-catalogue values (497 distinct prices across
   500 products), so bubbles form faint vertical columns rather than a smooth continuum.
   This is a property of the catalogue, not a behavioural cluster.
7. **Quantity is not confounded with price.** The quantity mix is almost identical in
   every price band — roughly 70% single-unit, 19% two-unit, 7% three-unit, 3% four-unit,
   and 1% five-unit. Price–quantity rank correlation is **+0.004**. Larger bubbles do not
   cluster on the right; their higher profits come from the quantity multiplier, not from
   being attached to more expensive products.

---

## Outliers and what they represent

- **Maximum profit: ¥2,679.10** — 4 units of a ¥1,521.98 product at only 4.3% discount.
  It sits near the top-right corner: the combination of high price, multiple units, and a
  shallow discount.
- **Maximum loss: −¥959.65** — 3 units of a ¥1,299.88 product at 46.1% discount. It sits
  at the bottom-right: high price and multiple units do **not** protect against a deep
  discount.
- **High-profit tail:** 1,539 lines exceed ¥500 profit; 316 exceed ¥1,000. Every line
  above ¥500 has a discount of 34.9% or less (median 7.5%), and every line above ¥1,000
  has a discount of 26.2% or less (median 6.7%).
- **Loss tail:** 261 lines lose more than ¥100. Their median unit price is ¥773.77 —
  much higher than the ¥148.27 median for all loss lines — confirming that the biggest
  losses are expensive, multi-unit baskets sold at deep discounts.
- **The largest bubbles are not the largest outliers.** Quantity 5 accounts for only
  0.98% of lines and 3.22% of revenue; the extreme profits mostly come from 2–4 unit
  baskets at high prices. Quantity lifts the ceiling, but price and discount decide
  whether a line reaches it.

These extremes are mechanically consistent with
`Profit_CNY = Revenue_CNY − Quantity × Unit_Cost_CNY` and are retained rather than
trimmed.

---

## How this differs from the previous scatter plot

**Chart 5 — discount vs profit** answers *“what happens to profit as discount deepens?”*
It shows a negative, moderate relationship (Spearman **−0.409**): median profit falls
from ¥57.70 at 0–5% discount to −¥47.69 above 55%, and discount alone explains about
6.4% of linear profit variation. Its x-axis says nothing about basket value, so it
cannot distinguish a deeply discounted cheap line from a lightly discounted expensive
one.

**The bubble plot** answers a different question: *“where does profit come from?”* It
replaces discount with unit price and adds quantity as bubble size. The relationship
becomes strongly positive (Spearman **+0.699**), and the fan shows that price sets the
scale of profit while quantity lifts the ceiling. The two charts are complementary:

- Chart 5 explains the **vertical spread at a given price**: the loss band and the
  high-discount outliers.
- The bubble plot explains the **level and ceiling**: high-price, multi-unit baskets
  occupy the top of the chart, while cheap single units occupy the bottom.
- The worst loss in the bubble plot is a large bubble at high price — exactly the
  high-discount region Chart 5 identified, but now visible as a specific kind of basket.
- A bubble plot cannot show discount directly, so it should be read alongside Chart 5,
  not as a replacement.

---

## How this differs from the pair plot

The pair plot (Chart 6) shows **pairwise** relationships in separate panels: price–profit,
quantity–profit, and price–quantity. The bubble plot **joins all three in one view**:

- The pair plot reports price–profit ρ = **+0.699** and quantity–profit ρ = **+0.236**;
  the bubble plot shows why quantity looks weak on its own — quantity is independent of
  price and most lines are single-unit — yet strongly lifts profit *within* a price level.
- The pair plot establishes that price and quantity are independent (ρ = **+0.004**); the
  bubble plot makes that visible as the absence of a size gradient from left to right.
- The pair plot also includes revenue, which is almost a deterministic function of price
  and quantity. The bubble plot deliberately drops revenue and uses the two inputs
  instead, exposing the **joint** condition for high profit: high price **and** multiple
  units.
- The bubble plot is therefore the clearest single view of the profit mechanism, while
  the pair plot remains the better tool for checking all pairwise correlations and
  distributions at once.

---

## Limitations

- **Observational and synthetic.** No causal claim is warranted; prices, discounts, and
  quantities are not randomly assigned.
- **Area perception is imperfect.** People underestimate area differences. The five-level
  size legend and the supporting tables are more reliable than visual comparison alone.
- **Overplotting remains severe in the core.** Transparency reveals density but hides
  exact counts; the darkest region contains thousands of near-identical single-unit,
  low-price lines.
- **Transformed axes.** Log price and symlog profit change visual distances. The plot is
  for pattern recognition, not for measuring slopes or percentage changes by eye.
- **Quantity is discrete and coarse.** Only five values exist; the size channel cannot
  represent fractional units or revenue weighting.
- **Discount and unit cost are not encoded.** Two bubbles in the same place can have very
  different discounts and costs. Those variables explain the residual vertical spread
  and the loss band.
- **Line grain, not order grain.** Multiple lines from one order are not netted.
- **Mechanical component.** Profit is revenue minus quantity × unit cost, so part of the
  price–profit association is definitional rather than an independent behavioural finding.
- **Slight opacity variation by size** is present for legibility only; it does not encode
  a variable and should not be read as one.
- **Excluded zero-revenue lines.** 3,118 completed rows with zero revenue and zero profit.

---

## Bottom line

Unit price and quantity together explain the shape of profit: price sets the scale,
quantity lifts the ceiling, and the loss band survives at every price because discount
and unit cost can erase the gain. The bubble plot turns the pairwise correlations from
Chart 6 into one readable mechanism and supplies the basket-value context that Chart 5
lacked. Its central message is simple: **high profit needs an expensive basket with more
than one unit — and a discount shallow enough to keep the margin.**
