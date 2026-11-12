# Revenue by Product Category — Violin Plot

**Chart:** [`output/charts/category_revenue_violin.png`](../charts/category_revenue_violin.png)  
**Script:** `scripts/charts/plot_category_revenue_violin.py`  
**Data:** `data/raw/huagou_mall_synthetic_ecommerce.csv`  
**Population:** Completed order lines with `Revenue_CNY > 0`; Jan 2024 – Dec 2025

---

## Why this view

A box plot shows where the middle of each category sits. A violin plot adds the
**density shape**, revealing whether revenue clusters around one price band, spreads
smoothly, or forms several distinct bulges. That matters because the box plot showed
large median and IQR differences but could not show whether each category is one broad
spending profile or several price clusters.

The chart uses the **same 49,327 completed, revenue-bearing lines** and the same
descending-median order as the box plot.

---

## Method

| Item | Value |
|---|---:|
| Completed order lines | 52,445 |
| Excluded: revenue = 0 | 3,118 (5.95%) |
| **Lines plotted** | **49,327** |
| Categories | 8 |
| Density estimate | Gaussian KDE on `log10(Revenue_CNY)` |
| Bandwidth | Silverman’s rule, per category |
| Bandwidth range | 0.070–0.125 log10 units (17.6%–33.2%) |
| Violin width | ∝ density, common scale, equal area |
| Median / quartiles | White dot + dark bar / Q1–Q3 bar |
| Axis | Log-scaled CNY |

The KDE uses a NumPy implementation, so no SciPy dependency was added. Estimating
density in log space respects the positive support and stops the long CNY tail from
dominating the bandwidth. Equal horizontal distances therefore represent equal
**percentage** differences.

**Widths are not sample sizes.** Each violin is scaled to equal area, so Books &
Stationery (1,281 lines) can look as thick as Digital Electronics (15,477 lines).
Thickness encodes density per log10 CNY, not line count.

---

## Category summary

| Category | n | Median | IQR | Q3/Q1 | P95/P50 | Peak density | Main mode | Mode vs median |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 运动户外 · Sports & Outdoors | 5,663 | ¥250.97 | ¥610.21 | 8.06× | 6.84× | 0.640 | ¥693 | +176% |
| 数码电子 · Digital Electronics | 15,477 | ¥228.29 | ¥615.14 | 8.25× | 8.21× | 0.703 | ¥130 | −43% |
| 服饰鞋包 · Fashion & Bags | 8,416 | ¥206.50 | ¥491.85 | 6.45× | 6.94× | 0.718 | ¥726 | +252% |
| 美妆个护 · Beauty & Personal Care | 5,157 | ¥151.86 | ¥292.26 | 6.12× | 5.44× | 0.740 | ¥237 | +56% |
| 食品饮料 · Food & Beverages | 3,251 | ¥125.68 | ¥169.80 | 5.21× | 3.79× | **1.105** | ¥179 | +42% |
| 母婴用品 · Mother & Baby | 1,484 | ¥104.48 | ¥257.76 | 8.33× | **10.83×** | 0.798 | ¥33 | −69% |
| 家居生活 · Home & Living | 8,598 | ¥87.01 | ¥216.57 | 7.77× | 7.49× | 0.734 | ¥21 | −76% |
| 图书文具 · Books & Stationery | 1,281 | ¥49.11 | ¥173.49 | **10.41×** | 10.04× | 0.720 | ¥193 | +292% |

Peak density is measured per log10 CNY and depends on bandwidth, so treat it as a broad
measure of concentration rather than a precise ranking.

---

## Distribution shape and density concentration

**Food & Beverages is the most concentrated distribution.** It has the highest peak
density (1.105), and its main bulge at **¥179** contains 12.3% of its lines within a ±10%
window. The shape is short and thick: a strong central body, a shoulder near ¥57, and a
weak low-end bulge near ¥21 — the closest the dataset comes to a single dominant mode.

**Sports & Outdoors is the most diffuse.** It has the lowest peak density (0.640) and the
broadest, flattest body. Its widest point is near **¥693**, far above its ¥251 median,
with secondary bulges near ¥122 and ¥384. This does not mean most lines are near ¥693;
it means revenue is densely packed into a narrow multiplicative band there. Sports has
18.0% of lines in ¥500–1,000 and 16.0% at ¥1,000+, so that high-price cluster creates a
tall density peak even though the median is much lower.

**The mode is not the median in any category.** The white median dot frequently sits on a
slope or in a valley. The largest gaps are Books & Stationery (+292%), Fashion & Bags
(+252%), Sports & Outdoors (+176%), Home & Living (−76%), and Mother & Baby (−69%).
This is a genuine property of price-clustered data: a narrow band of common price points
can have high density per log unit while fewer than half the lines lie above it. The
median answers “what does the middle line look like?”; the mode answers “where is revenue
most densely packed on a multiplicative scale?”

**Concentration around each median** reinforces the pattern. Food & Beverages has the
largest share of lines within ±25% of its median (15.4%), followed by Fashion & Bags
(15.0%) and Beauty & Personal Care (13.4%). Digital Electronics and Books & Stationery
have the smallest (9.1% each), consistent with their broader, multi-bulge profiles.

---

## Spread and multimodality

**Relative spread reorders the categories.** Books & Stationery has the smallest absolute
IQR (¥173.49) but the widest relative IQR — a **10.4×** quartile ratio, from ¥18.44 to
¥191.93 — so it appears long and narrow on a log axis. Food & Beverages is the tightest on
both measures (IQR ¥169.80, Q3/Q1 = 5.21×). Mother & Baby has the longest relative upper
tail: P95 is **10.8×** its median and its maximum (¥5,967.30) is 57.1× its median.

Log-space skew is modest for most categories (between −0.41 and +0.47). The heavy CNY
tails are largely absorbed by the log transform, but Mother & Baby (+0.47) and Digital
Electronics/Fashion & Bags (+0.16 each) retain a right lean, while Food & Beverages
(−0.41) leans left on the log scale.

Using each category’s selected bandwidth and a prominence threshold of 10% of peak
density, **every category has at least two distinct density peaks**:

| Category | Peaks (CNY) | Peaks after 1.5× smoothing |
|---|---|---:|
| Fashion & Bags | 726, 182, 99, 357, 50 | 4 |
| Digital Electronics | 130, 955, 53, 329 | 4 |
| Sports & Outdoors | 693, 122, 384 | 2 |
| Beauty & Personal Care | 237, 57, 486 | 2 |
| Food & Beverages | 179, 57, 21 | 2 |
| Mother & Baby | 33, 137, 774 | 2 |
| Home & Living | 21, 61, 288 | 3 |
| Books & Stationery | 193, 18 | 2 |

The peaks are not an artefact of too little smoothing: increasing the bandwidth by 50%
removes minor bumps but leaves at least two peaks in every category. They are more
consistent with **discrete product price points and basket quantities** than with smooth,
single-peaked spending. The exact number of modes is bandwidth-dependent and should be
read as “lumpy, multi-bulge shape,” not as a precise count of customer segments.

---

## Comparison with the box plot

| Aspect | Box plot | Violin plot |
|---|---|---|
| Main message | Median and IQR differences | Shape, density, and spread |
| Ordering | Descending median | Same descending median |
| Shape | Hidden | Visible bulges and tails |
| Outliers | Individual flagged points | Continuous tail density |
| Axis | Log CNY | Log CNY |
| Sample size | Not encoded | Not encoded (equal-area widths) |

**Agreements**

- Medians and ordering are identical: Sports & Outdoors leads, Books & Stationery trails,
  a 5.11× top-to-bottom median gap.
- The top three categories (Sports, Digital, Fashion) have the widest absolute IQRs, and
  the violin confirms their bodies stretch furthest across the CNY range.
- Mother & Baby is a low-median, heavy-tail category in both views: the box plot flags
  12.5% of its lines as potential outliers, and the violin shows this as a long, thin
  upper tail rather than an isolated cluster of dots.
- Food & Beverages is compact in both views, and the violin adds that it is the most
  concentrated around its mode.

**Where the violin adds or corrects the box plot**

- **The box plot hides multimodality.** Digital Electronics looks like one wide box, but
  its violin has major bulges near ¥130 and ¥955 with a trough between them. Fashion &
  Bags shows five peaks. One median glosses over distinct price clusters.
- **Box IQRs are absolute; violin widths reveal relative spread.** Books & Stationery has
  the smallest CNY IQR but the largest relative IQR, so its box looks short while its
  violin looks long.
- **The median can sit away from the density peak.** In a box plot the median is always
  the centre of the box; in the violin it often lies on a slope.
- **Outlier counts mix tail length with sample size.** Digital has the most flagged
  outliers (957), but Mother & Baby and Books & Stationery have the longest relative upper
  tails (P95/P50 ≈ 10–11×).

Neither view shows causality or accounts for product mix, quantity, or discount depth.

---

## Observations supported by the chart

1. **Revenue is price-clustered, not smoothly distributed.** Every category has at least
   two density peaks, and the main mode is never the median.
2. **Food & Beverages is the most concentrated category** — highest peak density, widest
   central body, and the largest share of lines within ±10% of its mode (12.3%).
3. **Sports & Outdoors is the most diffuse high-revenue category** — lowest peak density
   and a broad profile with a dense high-price cluster near ¥693.
4. **Books & Stationery is bimodal and relatively wide**: a low cluster near ¥18 and a
   slightly taller cluster near ¥193, with a 10.4× quartile ratio despite the smallest
   CNY IQR.
5. **Mother & Baby pairs a low main mode (¥33) with the longest relative upper tail**
   (P95/P50 = 10.8×), matching its high box-plot outlier rate.
6. **Higher medians do not imply higher concentration.** The top three median categories
   have some of the lowest peak densities; low-median Food & Beverages is the most
   concentrated.

---

## Limitations

- **Bandwidth sensitivity.** Mode locations and peak heights depend on smoothing. The
  peaks use a consistent rule and a 10% prominence threshold, but they describe the
  smoothed density, not exact population modes.
- **Equal-area scaling.** Violin thickness is density, not sample size; a 1,281-line
  category and a 15,477-line category receive the same visual area.
- **Log-space density.** Thickness is per log10 CNY and is comparable across categories,
  but it is not a count or a percentage.
- **Clipped range.** Each violin is clipped to that category’s observed minimum and
  maximum, so no density is drawn for unobserved revenue.
- **Peaks are not customer segments.** Product price points and multi-unit baskets can
  create modes without any underlying group behaving differently.
- **Line grain and gross revenue.** These are order-line distributions after line
  discount but before refunds, returns, shipping, fees, tax, or commissions. Completed
  AOV is ¥654.89, not the mean line revenue.
- **Excluded zero-revenue lines.** The 3,118 excluded completed lines (5.95%) are real
  rows, likely voided or zeroed transactions.
- **Pooled and unconditional.** Two years, all channels, segments, and campaigns are
  combined; the chart does not control for seasonality or product mix.
- **Synthetic data.** The patterns are generated, not observed market behaviour.

---

## Bottom line

Category differences are not just shifts in level; the shapes differ. Food & Beverages is
compact and highly concentrated around a mode near ¥179. Sports & Outdoors and Digital
Electronics are broad and multi-bulge, with major price clusters well away from their
medians. Books & Stationery is the clearest bimodal case and the most dispersed in
relative terms, despite having the smallest absolute IQR. The box plot remains the better
tool for exact quartiles and outlier counts; the violin is the better tool for seeing
that revenue is clustered, lumpy, and often far from symmetric around its median.
