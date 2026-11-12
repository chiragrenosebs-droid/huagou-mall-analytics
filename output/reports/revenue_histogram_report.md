# Revenue Histogram — Completed Order Lines

**Chart:** [`output/charts/completed_line_revenue_histogram.png`](../charts/completed_line_revenue_histogram.png)  
**Script:** `scripts/charts/plot_revenue_histogram.py`  
**Data:** `data/raw/huagou_mall_synthetic_ecommerce.csv`  
**Scope:** Completed order lines with `Revenue_CNY > 0`; Jan 2024 – Dec 2025

---

## Why a histogram is appropriate

`Revenue_CNY` is a continuous monetary variable measured on a ratio scale. A histogram
is the standard first view of a single continuous variable because it shows:

- the **shape** of the distribution (skew, modality, flatness);
- the **centre and spread** of typical values;
- the **tails and outliers** that summary statistics can hide;
- how observations are **concentrated** across revenue bands.

A bar chart is inappropriate here because its categories would be arbitrary bins and it
would imply discrete groups. A box plot would show quartiles and outliers but conceal
the shape and the dominant low-revenue mass. A single mean or median would miss the
defining feature of this variable: a long right tail.

The chart uses **71 logarithmically spaced bins** and a log-scaled x-axis. Revenue spans
¥3.52 to ¥7,105 and 77% of lines fall below ¥500, so equal-width linear bins would
collapse most observations into two or three bars while leaving the tail almost empty.
Log spacing keeps both the dense low end and the high-value tail readable. Bin count is
consistent with the Freedman–Diaconis rule applied to `log10(Revenue_CNY)` (≈71 bins).
Bar height is the share of lines, not a count, so the shape is comparable across samples.

---

## Method and filters

| Item | Value |
|---|---:|
| Completed order lines | 52,445 |
| Excluded: completed lines with revenue = 0 | 3,118 (5.95%) |
| **Lines plotted** | **49,327** |
| Completed orders represented | 27,826 |
| Minimum | ¥3.52 |
| 25th percentile | ¥62.35 |
| Median | ¥163.84 |
| Mean | ¥369.43 |
| 75th percentile | ¥450.45 |
| 95th percentile | ¥1,309.47 |
| 99th percentile | ¥2,682.17 |
| Maximum | ¥7,105.00 |
| Skewness | 3.45 |
| Excess kurtosis | 17.3 |

Zero-revenue completed lines were excluded because they are zeroed financial records,
not genuine ¥0 sales: their price, quantity, and discount fields are populated while
revenue and profit are both 0. Including them would create an artificial spike at zero
and distort every average and percentile. This chart therefore describes **revenue-bearing
completed lines**, not all completed records.

---

## Distribution shape

- **Unimodal and strongly right-skewed.** The dominant mass sits roughly between ¥50 and
  ¥500, with the highest-density bins around **¥127–¥176**. A long, thinning tail extends
  past ¥3,000 to the ¥7,105 maximum.
- **The mean is 2.25× the median** (¥369.43 vs ¥163.84), a direct signal that high-value
  lines pull the average upward. The median is the better "typical line" summary.
- **Heavy-tailed.** Skewness is 3.45 and excess kurtosis is 17.3. Even on a log axis the
  right tail remains visible; on a raw linear axis it would dominate the entire plot.
- **No separate high-revenue cluster.** The tail is continuous rather than a second mode,
  which is consistent with basket-size and product-price variation rather than a distinct
  customer or order segment.

### Concentration by line count

| Revenue band | Share of lines |
|---|---:|
| Under ¥100 | 36.39% |
| ¥100 – <¥500 | 40.52% |
| ¥500 – <¥1,000 | 13.87% |
| ¥1,000 and above | 9.21% |

**76.9% of completed, revenue-bearing lines are below ¥500**, and more than one-third are
below ¥100. The distribution is therefore dominated by small line values, with a small
high-value minority.

### Concentration of revenue

- Lines of ¥1,000+ are 9.21% of lines but contribute **42.17%** of completed line revenue.
- The top 10% of lines by revenue contribute **44.25%** of revenue; the top 1% contribute
  **9.54%**.
- Conversely, 90.79% of lines at or below ¥1,000 contribute 57.83% of revenue.

---

## Outliers

Using the Tukey rule, the upper fence is **¥1,032.60** (`Q3 + 1.5 × IQR`). **4,245 lines
(8.61%)** lie above it. The lower fence is negative, so there are no low-end outliers.

These are not automatically data errors. High-revenue lines are plausible multi-unit,
high-ticket baskets: among lines of ¥1,000+, 68.9% have quantity ≥ 2, versus 29.6% of all
lines. The maximum line is 5 units of a ¥1,463.44 product with a 2.9% discount
(¥7,105.00), which is arithmetically consistent. The chart therefore retains all
observations rather than clipping the tail; any later trimming should be an explicit
business rule.

---

## Key observations supported by the chart

1. **Typical line revenue is low, but the average is misleadingly high.** The mode is
   around ¥130–¥175 and the median is ¥164, while the mean is ¥369. The gap is entirely
   due to the right tail, so reports should lead with the median and show the mean
   alongside it.
2. **Small baskets dominate by count, large baskets dominate by value.** 76.9% of lines
   are under ¥500, yet 42.2% of revenue comes from the 9.2% of lines at ¥1,000+.
   Volume-based and value-based views of this dataset will tell different stories.
3. **Revenue is heavy-tailed but continuous.** The smooth decay after the mode, with no
   secondary bump, suggests a single broad spending distribution rather than distinct
   customer tiers. Outliers are consistent with quantity × price, not inconsistent data.

---

## Limitations

- **Line grain, not order grain.** The unit is the order line. The mean line revenue
  (¥369) is not average order value; completed-order AOV is **¥654.89** because orders
  aggregate 1–5 lines. This chart must not be used to describe order values.
- **Zero-revenue lines are excluded.** The 3,118 excluded completed lines (5.95%) are
  legitimate rows in the source and may represent voided or zeroed transactions. Their
  exclusion changes the mean, percentiles, and apparent mode. Charts using "all completed
  lines" should state the difference.
- **Gross line revenue only.** Revenue is after line discount but before refunds, return
  costs, shipping fees, payment fees, tax, or platform commissions. No net-revenue field
  exists in the dataset.
- **Pooled view.** Two years, all categories, channels, customer segments, and campaign
  periods are combined. The histogram is unconditional and does not explain what drives
  the tail or the low-end mass; segment-specific distributions may differ.
- **Bin and scale sensitivity.** The log x-axis makes bin widths unequal in CNY, and a
  different bin count or linear scale would change the visual impression. Percentile
  statistics are more robust than reading exact heights from the bars.
- **Synthetic data.** Patterns are generated, not observed market behaviour, and should
  not be treated as evidence about real customers.

---

## Bottom line

Completed order-line revenue is a low-valued, unimodal, heavily right-skewed
distribution: half of all lines are at or below ¥164, but a thin high-value tail lifts
the mean to ¥369 and accounts for a disproportionate share of revenue. The histogram is
the right first view because no single summary statistic captures that combination.
