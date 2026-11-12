# Revenue KDE — Completed Order Lines

**Chart:** [`output/charts/completed_line_revenue_kde.png`](../charts/completed_line_revenue_kde.png)  
**Script:** `scripts/charts/plot_revenue_kde.py`  
**Data:** `data/raw/huagou_mall_synthetic_ecommerce.csv`  
**Population:** Completed order lines with `Revenue_CNY > 0`; Jan 2024 – Dec 2025

---

## Why a KDE is appropriate

`Revenue_CNY` is a continuous, strictly positive monetary variable. A kernel density
estimate (KDE) complements the histogram by estimating a smooth probability density
without forcing observations into fixed bins. It is useful here because:

- it shows the **continuous shape** of revenue — the central mass, shoulders, and tail —
  without bin-edge artefacts;
- it makes the **right skew and heavy tail** visible as a smooth profile rather than a
  series of bars;
- it provides a shape baseline that can later be compared across segments or periods;
- it is less sensitive than a histogram to the exact choice of bin boundaries.

A KDE is **not** a replacement for exact percentile calculations. It is a smoothed
visual summary, not a source of precise probabilities. For thresholds and tail shares,
the underlying line-level data (or an ECDF) should be used.

---

## Method and bandwidth

| Item | Value |
|---|---:|
| Completed order lines | 52,445 |
| Excluded: revenue = 0 | 3,118 (5.95%) |
| **Lines plotted** | **49,327** |
| Completed orders represented | 27,826 |
| Transformation | `log10(Revenue_CNY)` |
| Bandwidth rule | Silverman’s rule of thumb |
| Bandwidth (log10 units) | **0.05779** |
| Multiplicative smoothing width | **≈14.2%** |
| Peak density | 0.6592 per log10 CNY |
| Peak location | **¥145.89** |
| Median | ¥163.84 |
| Mean | ¥369.43 |

Silverman’s rule was applied to log-transformed revenue:

```
h = 0.9 × min(sd(log10 revenue), IQR(log10 revenue) / 1.34) × n^(−1/5)
```

The bandwidth is **0.0578 in log10 units**, corresponding to roughly ±14% in CNY around
a given value. This is a standard, data-driven starting point: large enough to avoid a
noisy curve, small enough to preserve the main shape. The density was evaluated with a
NumPy Gaussian KDE on a 1,200-point log grid; no additional libraries were installed.

### Why model log revenue instead of raw revenue?

Revenue is positive and spans ¥3.52 to ¥7,105, with 77% of lines below ¥500. A raw-scale
KDE would spread density below zero, over-smooth the dense low-value region, and let the
long tail dominate the bandwidth. Fitting in log space respects the positive support and
treats equal *percentage* changes consistently. The fitted density is then plotted back
on a **log-scaled CNY x-axis**.

The y-axis is **probability density per log10 CNY**, not per CNY. The curve integrates to
1 over log10 revenue. The density value itself is therefore a relative shape measure, not
a percentage of lines.

---

## Distribution shape

- **One dominant peak near ¥146.** The density rises sharply through the low hundreds and
  reaches its maximum at ¥145.89, close to the histogram’s densest region (¥127–¥158).
- **Broad central mass.** The curve stays above ~80% of its peak density from roughly
  ¥50 to ¥380, confirming that most completed lines are low-to-mid value.
- **Shallow shoulders, not a strong second cluster.** There are mild local density peaks
  near ¥57, ¥329, and ¥680. Their prominence is limited: the curve undulates rather than
  forming separated high-density islands. These shoulders are consistent with discrete
  product price points and quantity combinations, not necessarily distinct customer
  segments.
- **Long, continuous right tail.** Density decays gradually through ¥1,000–¥3,000 and
  remains non-zero to the observed maximum of ¥7,105. There is no isolated high-value
  mode.
- **Mean above median.** The mean (¥369.43) is 2.25× the median (¥163.84), confirming
  that the tail — not the typical line — drives the average.

The KDE therefore **refines** the histogram’s simpler “unimodal, right-skewed” reading:
one dominant mode, shallow price-related shoulders, and a smooth heavy tail.

---

## Comparison with the histogram

| Aspect | Histogram | KDE |
|---|---|---|
| Representation | Binned share of lines | Smoothed probability density |
| Peak | Tallest bin ¥127–¥142 (3.21% of lines) | ¥145.89 |
| Detail | Depends on bin edges and count | Depends on bandwidth |
| Low-value mass | Visible as dense bars | Visible as a broad central peak |
| Tail | Sparse bars, harder to read | Smooth decay, easier to see shape |
| Best use | Reading mass within revenue bands | Seeing overall shape and shoulders |

Both views use the **same 49,327 lines**, the same x-limits, ticks, and median/mean
reference lines. Their main conclusions agree: low typical values, a broad low-to-mid
mass, and a disproportionate high-value tail.

Concentration figures from the same underlying lines (not read from the density curve):

| Revenue band | Share of lines |
|---|---:|
| Under ¥100 | 36.39% |
| ¥100 – <¥500 | 40.52% |
| ¥500 – <¥1,000 | 13.87% |
| ¥1,000 and above | 9.21% |

Lines of ¥1,000+ contribute **42.17%** of completed line revenue, and the top 10% of
lines contribute **44.25%**. The KDE’s broad low-value peak and long tail are consistent
with that count-versus-value split.

---

## Outliers and tail behaviour

- The Tukey upper fence is **¥1,032.60**; **4,245 lines (8.61%)** lie above it. The lower
  fence is negative, so there are no low-end outliers.
- High values are retained in the KDE. They are plausible high-ticket, multi-unit baskets:
  68.9% of lines at ¥1,000+ have quantity ≥ 2, versus 29.6% of all lines. The maximum is
  5 units of a ¥1,463.44 product with a 2.9% discount (¥7,105.00).
- The Gaussian kernel gives the fitted curve smooth tails beyond the observed data range.
  Density outside ¥3.52–¥7,105 is an artefact of smoothing, not evidence of unobserved
  revenue.
- The tail is thin but consequential: the top 1% of lines contribute 9.54% of revenue.

---

## Key observations supported by the chart

1. **Typical completed line revenue is modest.** The dominant density peak is near ¥146
   and the median is ¥164; the broad mass sits well below ¥500.
2. **The average is tail-driven.** The mean (¥369) is 2.25× the median (¥164). A single
   “average line value” hides the fact that most lines are much smaller.
3. **The distribution is one broad spending profile, not two distinct populations.**
   Shoulders around ¥57, ¥329, and ¥680 are shallow and are better explained by price and
   quantity structure than by separate customer tiers.
4. **High-value lines matter disproportionately.** Only 9.2% of lines are at ¥1,000+ but
   they generate 42.2% of revenue, so value-based and volume-based views will diverge.

---

## Limitations

- **Bandwidth sensitivity.** A larger bandwidth smooths away the shoulders; a smaller one
  introduces wiggles. Scott’s rule (h ≈ 0.064) gives a nearly identical peak and main
  shape. At roughly 2.5× the selected bandwidth the curve becomes strictly unimodal, so
  the minor shoulders should be treated as indicative rather than definitive.
- **Log-space density.** The y-axis is density per log10 CNY. It cannot be read as a
  percentage of lines, and its height is not comparable to a raw-CNY density.
- **Line grain, not order grain.** The unit is the order line; mean line revenue (¥369) is
  not average order value. Completed-order AOV is **¥654.89**.
- **Zero-revenue lines excluded.** The 3,118 excluded completed lines (5.95%) are real
  source rows, likely voided or zeroed transactions. Their exclusion changes the density,
  mean, and percentiles.
- **Gross line revenue only.** Revenue is after line discount but before refunds, return
  costs, shipping fees, payment fees, tax, or platform commissions.
- **Pooled, unconditional view.** Two years, all categories, channels, customer segments,
  and campaign periods are combined. The KDE does not explain what drives the shape;
  segment-specific densities may differ.
- **Synthetic data.** The patterns are generated, not observed market behaviour.

---

## Bottom line

The KDE confirms the histogram’s central finding: completed order-line revenue is
concentrated at low values, with a dominant peak near ¥146 and a long, revenue-rich tail.
Its advantage is a smooth view of the shape — one broad central mass with shallow
price-related shoulders rather than a simple single spike. It should be paired with the
histogram for mass-by-band reading and with percentile statistics for exact thresholds;
it is a shape tool, not a probability calculator.
