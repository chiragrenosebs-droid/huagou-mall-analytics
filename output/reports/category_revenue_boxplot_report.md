# Revenue by Product Category — Box Plot

**Chart:** [`output/charts/category_revenue_boxplot.png`](../charts/category_revenue_boxplot.png)  
**Script:** `scripts/charts/plot_category_revenue_box.py`  
**Data:** `data/raw/huagou_mall_synthetic_ecommerce.csv`  
**Population:** Completed order lines with `Revenue_CNY > 0`; Jan 2024 – Dec 2025

---

## Why this view

A box plot is appropriate for comparing a continuous variable across groups because it
summarises the **median, quartiles, spread, and tail behaviour** in one compact view. It
is more robust to extreme revenue values than a mean-and-standard-deviation summary, and
it makes differences in both location and dispersion visible across the eight product
categories.

The chart uses a **log-scaled CNY x-axis**. Revenue spans ¥3.52 to ¥7,105 and remains
right-skewed within every category; a linear axis would compress most boxes into the left
edge and make quartiles hard to compare. Box widths on this axis represent multiplicative
differences, not equal CNY distances. Exact CNY values are provided in the table below.

---

## Method

| Item | Value |
|---|---:|
| Completed order lines | 52,445 |
| Excluded: revenue = 0 | 3,118 (5.95%) |
| **Lines plotted** | **49,327** |
| Product categories | 8 |
| Box | Interquartile range (Q1–Q3) |
| Centre line | Median |
| Whiskers | Furthest values within 1.5 × IQR |
| Points | Potential outliers outside 1.5 × IQR |
| Reference line | Overall median (¥163.84) |

Categories are sorted by **median revenue, highest at the top**, so the ordering is
intentional rather than alphabetical. Both the Chinese source label and an English
translation are shown.

The box plot uses **category-specific fences**. Across the eight categories, 3,015 lines
(6.1% of the plotted population) fall outside their category’s 1.5 × IQR fence. This is
lower than the 4,245 lines (8.6%) flagged by a single overall fence because each category
has its own quartiles.

---

## Category summary

| Category | Lines (n) | Median | Q1 – Q3 | IQR | Whisker range | Potential outliers |
|---|---:|---:|---:|---:|---:|---:|
| 运动户外 · Sports & Outdoors | 5,663 | ¥250.97 | ¥86.48 – ¥696.70 | ¥610.21 | ¥13.62 – ¥1,611.71 | 311 (5.5%) |
| 数码电子 · Digital Electronics | 15,477 | ¥228.29 | ¥84.81 – ¥699.95 | ¥615.14 | ¥14.24 – ¥1,622.56 | 957 (6.2%) |
| 服饰鞋包 · Fashion & Bags | 8,416 | ¥206.50 | ¥90.30 – ¥582.15 | ¥491.85 | ¥20.69 – ¥1,319.02 | 501 (6.0%) |
| 美妆个护 · Beauty & Personal Care | 5,157 | ¥151.86 | ¥57.13 – ¥349.39 | ¥292.26 | ¥9.54 – ¥787.06 | 279 (5.4%) |
| 食品饮料 · Food & Beverages | 3,251 | ¥125.68 | ¥40.32 – ¥210.12 | ¥169.80 | ¥4.77 – ¥464.69 | 176 (5.4%) |
| 母婴用品 · Mother & Baby | 1,484 | ¥104.48 | ¥35.15 – ¥292.90 | ¥257.76 | ¥9.06 – ¥671.87 | 185 (12.5%) |
| 家居生活 · Home & Living | 8,598 | ¥87.01 | ¥31.97 – ¥248.54 | ¥216.57 | ¥9.00 – ¥572.80 | 535 (6.2%) |
| 图书文具 · Books & Stationery | 1,281 | ¥49.11 | ¥18.44 – ¥191.93 | ¥173.49 | ¥3.52 – ¥447.85 | 71 (5.5%) |

All lower fences are negative, so **every flagged outlier is on the high-revenue side**;
there are no low-end outliers by the 1.5 × IQR rule.

---

## Median and IQR differences

- **Top-to-bottom median gap:** Sports & Outdoors (¥250.97) versus Books & Stationery
  (¥49.11) is a **¥201.86 gap — a 5.11× difference** in typical line revenue.
- **Top three categories** — Sports (¥250.97), Digital (¥228.29), and Fashion (¥206.50) —
  sit **¥42.66 to ¥87.13 above** the overall median of ¥163.84 (+26% to +53%). Their
  medians are close to each other; Sports is only ¥22.68 (9.9%) above Digital.
- **Five categories fall below the overall median:** Beauty (¥151.86, −7.3%), Food
  (¥125.68, −23.3%), Mother & Baby (¥104.48, −36.2%), Home & Living (¥87.01, −46.9%), and
  Books & Stationery (¥49.11, −70.0%).
- **Top-to-bottom IQR gap:** Digital (¥615.14) versus Food (¥169.80) is a **¥445.34 gap —
  a 3.62× difference** in the middle 50% of revenue.
- **Digital and Sports have almost identical spread:** IQR ¥615.14 versus ¥610.21
  (Digital is only 0.8% wider), despite Digital having nearly three times as many lines.
- **The top three categories are also the widest:** IQRs of ¥610–¥615 (Sports/Digital) and
  ¥491.85 (Fashion) are 27%–59% above the overall IQR of ¥388.10. The remaining categories
  have IQRs of ¥170–¥292.
- **Food is the most compact distribution:** narrowest IQR (¥169.80), with its median
  (¥125.68) almost exactly midway between Q1 (¥40.32) and Q3 (¥210.12).
- **Books has the lowest median but not the narrowest IQR:** its IQR of ¥173.49 is slightly
  wider than Food’s, and its upper whisker stops at ¥447.85.

---

## Variation and potential outliers

- **Outlier rate ranges from 5.4% to 12.5%.** Most categories cluster around 5.4%–6.2%,
  but **Mother & Baby is a clear exception at 12.5%** (185 of 1,484 lines).
- **Mother & Baby has the most extreme high-end tail relative to its median:** its upper
  whisker reaches ¥671.87, but potential outliers extend to **¥5,967.30**. That is more
  than 57× its median of ¥104.48 and explains why its mean (¥285.91) is far above its
  median, even though the median is low.
- **Digital Electronics has the largest number of flagged lines (957),** but this is partly
  a sample-size effect: its 6.2% rate is close to the dataset norm. Home & Living has 535
  outliers from 8,598 lines (6.2%).
- **Upper whiskers differ sharply:** Digital (¥1,622.56), Sports (¥1,611.71), and Fashion
  (¥1,319.02) extend much further than Food (¥464.69) and Books (¥447.85). The chart shows
  this as a long upper tail for the higher-revenue categories.
- **Outliers are potential, not erroneous.** The dataset’s high-revenue lines are
  plausibly high-quantity or high-ticket baskets; the chart flags them by a mechanical
  rule, not by data-quality validation.
- **Boxes overlap substantially.** Even the low-median categories have lines overlapping
  the interquartile ranges of higher categories, so category explains a shift in the
  revenue distribution but does not cleanly segment individual lines.

---

## Observations supported by the chart

1. **Category is associated with a clear shift in typical revenue.** The medians descend
   steadily from Sports & Outdoors (¥251) to Books & Stationery (¥49), a 5.1× range.
2. **The top categories are both higher and more variable.** Sports, Digital, and Fashion
   have the highest medians and the widest boxes; their upper whiskers also extend beyond
   ¥1,300, while Food and Books stop below ¥500.
3. **High-value tails exist in every category.** All flagged points lie above the upper
   whisker, and every category has at least 71 of them. The tail is not confined to the
   expensive top categories.
4. **Mother & Baby is a low-median, heavy-tail category.** Its box sits low, but it has the
   highest outlier rate (12.5%) and an extreme maximum near ¥6,000 — a pattern visible as
   a low median with a dense scatter of high-value dots.
5. **Most categories are right-skewed within the box.** The distance from the median to Q3
   exceeds the distance from Q1 to the median for seven of eight categories; Food is the
   near-symmetric exception.
6. **The category distributions overlap heavily.** The chart supports a “different centres
   and spreads” conclusion, not a claim that categories are cleanly separated.

---

## Limitations

- **Line grain, not order grain.** The unit is the order line. These medians are not
  category-level order values; completed-order AOV is ¥654.89.
- **Zero-revenue completed lines are excluded.** The 3,118 excluded lines (5.95%) are real
  rows, likely voided or zeroed transactions, and could affect category comparisons if
  their exclusion is uneven.
- **Gross line revenue only.** Revenue is after line discount but before refunds, return
  costs, shipping fees, payment fees, tax, or platform commissions.
- **Log axis compresses absolute differences.** A visually wider box represents a larger
  ratio, not a larger CNY gap. The table supplies the actual CNY values.
- **Outlier flags are rule-based.** The 1.5 × IQR definition is conventional, not a
  judgement that a value is invalid. No observations were removed or clipped.
- **Category aggregates hide product mix.** Differences may reflect product price points,
  quantity, discount depth, or channel mix rather than category behaviour itself.
- **Unequal sample sizes.** Digital has 15,477 lines; Books has 1,281. Outlier counts are
  not directly comparable across categories; rates are more informative.
- **Pooled and unconditional.** Two years, all channels, customer segments, and campaign
  periods are combined. The chart does not establish causality or control for seasonality.
- **Synthetic data.** Patterns are generated and should not be treated as real market
  evidence.

---

## Bottom line

Completed order-line revenue differs materially by product category. Sports & Outdoors,
Digital Electronics, and Fashion & Bags combine the highest medians with the widest middle
50%, while Books & Stationery and Food & Beverages sit at the low end with much tighter
distributions. Mother & Baby is the notable low-median, heavy-tail case. The categories
overlap enough that category is a useful descriptive lens, not a clean segmentation of
individual order lines.
