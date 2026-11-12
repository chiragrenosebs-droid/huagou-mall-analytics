# Category × Month Revenue Heatmap

**Chart:** [`output/charts/category_month_revenue_heatmap.png`](../charts/category_month_revenue_heatmap.png)  
**Script:** `scripts/charts/plot_category_month_heatmap.py`  
**Data:** `data/raw/huagou_mall_synthetic_ecommerce.csv`  
**Population:** 49,327 completed order lines with `Revenue_CNY > 0`; Jan 2024 – Dec 2025

---

## What the chart encodes

| Element | Meaning |
|---|---|
| Row | Product `Category` (8 rows, ordered by total revenue) |
| Column | Calendar month, Jan–Dec (12 columns) |
| Cell **colour** | `Revenue_CNY` summed for that category in that calendar month, **2024 + 2025 combined** |
| Cell **label** | The same value printed in CNY (`K` = thousand, `M` = million) |
| Colour bar | Linear scale from ¥0 to the brightest cell (¥1.12M) |

- Each of the 96 cells is a **two-year calendar-month total**, not a year-specific
  value: January 2024 and January 2025 are summed into the “Jan” column.
- The colour ramp is a **single-hue, monotonically darkening teal**
  (`#F4F8F8` → `#0F2F38`). The scale is **linear**, so colour is proportional to
  absolute revenue and the bright bands are genuinely large amounts, not the output
  of a normalisation trick.
- **Excluded:** 3,118 completed lines with `Revenue_CNY = 0`. They contribute no
  revenue and only dilute line-based rates. Total in the grid: **¥18,222,902.98**.

---

## Why a heatmap suits this question

1. **The data is intrinsically a matrix.** Two categorical dimensions — category and
   month — crossed with one quantitative measure produce 96 values. A heatmap shows
   every one of them in one frame; grouped bars (8 × 12 = 96 bars) or twelve separate
   charts would force the reader to compare across panels that are no longer adjacent.
2. **Position answers “where”, colour answers “how much”.** A reader can find a
   category–month pair by row and column without a legend lookup, then rank it by
   shade. This supports both row scanning (“is this category seasonal?”) and column
   scanning (“which categories peak in November?”).
3. **Colour is pre-attentive.** The June and November columns stand out before any
   number is read. That is exactly the comparative job here: does the seasonal shape
   repeat across categories, or is it category-specific?
4. **A sequential scale is the correct encoding.** Revenue is a one-directional
   magnitude with a meaningful zero, so a sequential ramp is appropriate; there is no
   midpoint that would justify a diverging palette, and hue is not carrying category
   identity, so a single ramp is the simplest correct choice.
5. **Annotation removes the palette's weakness.** Colour is good at ordering and poor
   at precise decoding, so all 96 cells carry their value. The chart works at two
   distances: the shape of the grid at a glance, exact figures on inspection.

---

## The grid at a glance

### Rows — category scale dominates

| Category | Revenue (CNY) | Share | Lines | Revenue / line |
|---|---:|---:|---:|---:|
| 数码电子 — Digital Electronics | ¥7,852,159.99 | **43.09%** | 15,477 | ¥507.34 |
| 服饰鞋包 — Apparel & Bags | ¥3,468,284.80 | 19.03% | 8,416 | ¥412.11 |
| 运动户外 — Sports & Outdoors | ¥2,867,731.40 | 15.74% | 5,663 | ¥506.40 |
| 家居生活 — Home & Living | ¥1,592,606.10 | 8.74% | 8,598 | ¥185.23 |
| 美妆个护 — Beauty & Personal Care | ¥1,334,568.98 | 7.32% | 5,157 | ¥258.79 |
| 食品饮料 — Food & Beverage | ¥512,405.50 | 2.81% | 3,251 | ¥157.61 |
| 母婴用品 — Mother & Baby | ¥424,285.81 | 2.33% | 1,484 | ¥285.91 |
| 图书文具 — Books & Stationery | ¥170,860.40 | 0.94% | 1,281 | ¥133.38 |

### Columns — June and November are a different regime

| Month | Revenue (CNY) | Share | Revenue / day | Index vs 10-month avg |
|---|---:|---:|---:|---:|
| Jan | ¥1,462,709.85 | 8.03% | ¥23,592 | 1.11 |
| Feb | ¥1,312,312.56 | 7.20% | ¥23,023 | 1.00 |
| Mar | ¥1,303,037.62 | 7.15% | ¥21,017 | 0.99 |
| Apr | ¥1,226,179.88 | 6.73% | ¥20,436 | 0.93 |
| May | ¥1,231,645.76 | 6.76% | ¥19,865 | 0.94 |
| **Jun** | **¥2,526,900.12** | **13.87%** | **¥42,115** | **1.92** |
| Jul | ¥1,206,825.58 | 6.62% | ¥19,465 | 0.92 |
| Aug | ¥1,302,539.12 | 7.15% | ¥21,009 | 0.99 |
| Sep | ¥1,322,925.11 | 7.26% | ¥22,049 | 1.01 |
| Oct | ¥1,302,710.61 | 7.15% | ¥21,012 | 0.99 |
| **Nov** | **¥2,555,734.48** | **14.02%** | **¥42,596** | **1.94** |
| Dec | ¥1,469,382.29 | 8.06% | ¥23,700 | 1.12 |

The ten non-peak months average **¥1,314,027** each; June and November run at roughly
**1.9×** that level. Together they carry **¥5,082,634.60 — 27.89% of all revenue** from
two months out of twelve.

---

## Where the colour is intense — and where it is pale

**The single strongest visual signal is horizontal, not vertical.** Revenue spans
**43% (Digital) to 0.94% (Books)**, a 46× difference in row totals, while within-row
months mostly run between 0.7× and 1.7× the row mean (peaks reach 2.1×). So the grid
reads first as “which category”, then as “which month”.

- **Darkest row:** 数码电子 (Digital Electronics). Every cell above ¥500K — eleven of
  them — is in the Digital row, and even its weakest month (Jul, ¥474,733) outshines
  every cell outside that row except Apparel's November peak.
- **Brightest cells:** Digital **Nov ¥1,120,973.78** and Digital **Jun
  ¥1,096,050.84**. They are **1.7×** the third-brightest cell (Digital Dec
  ¥642,386.24) and the only cells above ¥1M.
- **Mid-tones:** Apparel (19.03%) and Sports (15.74%) form a clearly visible second
  and third band; Home (8.74%) and Beauty (7.32%) are mid-pale. Their rows are
  uniform enough that the June/November columns still brighten them noticeably.
- **Pale rows:** Food (2.81%), Baby (2.33%) and Books (0.94%) sit at the light end.
  Books is so pale that colour alone cannot rank its months — this is why the printed
  values matter.
- **Lowest cells:** Books **Sep ¥8,667.18**, Books **Aug ¥9,819.82**, Books **May
  ¥10,131.11**, Books Apr ¥11,163.00 and Books Oct ¥11,597.99. Only eleven of the 96
  cells are below ¥20K, and ten of them are Books.
- **Dynamic range:** the brightest cell is **129×** the dimmest.

This is the main interpretation caveat: **cell intensity mixes category scale with
seasonality**. The chart shows both at once, which is useful for prioritisation, but a
pale Baby cell in June (¥74.4K, its annual peak) is still a peak.

---

## Seasonal patterns

### 1. A shared June + November uplift runs through every row

Both columns are visibly brighter for all eight categories. Measured against each
category's own 12-month mean, peak-month indices run from **1.53× (Sports, Nov) to
2.10× (Baby, Jun)**; every category peaks between those two bounds. The pattern is
calendar-driven, not confined to one product line.

- June + November account for **26.03% (Sports) to 33.34% (Baby)** of each category's
  two-year revenue.
- The uplift repeats in **both years separately**: June is 14.11% of 2024 revenue and
  13.61% of 2025; November is 13.29% and 14.79%. So the peak is a recurring seasonal
  pattern, not a one-off spike confined to a single year.
- November is the larger of the two in four categories (Digital, Apparel, Beauty, Food);
  **Sports, Home, Baby and Books** peak in June instead.

### 2. The peaks are volume-driven, not basket-driven

| Month | Lines | Revenue / line | Mean discount |
|---|---:|---:|---:|
| Jun | 6,967 | ¥362.70 | 15.61% |
| Nov | 6,969 | ¥366.73 | 15.70% |
| Other months (avg.) | ~3,406 | ~¥372 | ~14.4% |

June and November carry about **twice the usual number of order lines**, while revenue
per line stays inside the normal ¥358–¥388 band and discounts are only about **1.1
percentage points** deeper. The bright columns are a traffic/promotion effect, not a
shift to larger baskets.

### 3. The peaks are spread across the month, not a single festival day

Daily revenue in June has a coefficient of variation of **0.44** and November **0.56**,
against **0.32–0.46** in ordinary months. The busiest day-of-month in each carries only
**6.0% (June) and 6.3% (November)** of the month's revenue — elevated versus the 3.3%
a perfectly even month would give, but far from a single-day festival spike. Both months
are lifted throughout, which is why the heatmap needs no day-level breakdown to make its
point.

### 4. A shallow off-season, with July the true trough

- **July is the dimmest month** by revenue (¥1.21M, 6.62%) and by revenue per day
  (¥19,465).
- April and May are the next weakest (6.73% and 6.76%).
- **December and January are mildly elevated** (8.06% and 8.03%) — a small holiday-season
  lift, but less than half the June/November effect. The step down from November to
  December is abrupt (14.02% → 8.06%).
- **September is unremarkable by volume but has the highest revenue per line**
  (¥388.07), so its cell is slightly darker than a pure order-count view would predict.
- **Month length matters a little, not much:** January and December benefit from 31 days
  and February is short. Per day, November (¥42,596) and June (¥42,115) still lead by a
  wide margin, and July remains last, so the seasonal conclusion is robust to the
  calendar artefact.

---

## Category-specific deviations

The shared seasonal shape is strong, but the residuals are informative:

| Category | Peak | Trough | CV of monthly revenue | Reading |
|---|---|---|---:|---|
| 数码电子 — Digital | Nov ¥1,120,974 | Jul ¥474,733 | 0.330 | Largest absolute swing (¥646K peak-to-trough); Nov and Jun nearly tie |
| 服饰鞋包 — Apparel | Nov ¥489,194 | Apr ¥186,455 | 0.327 | Sharpest spring dip (Apr 0.65× its mean); strong Jan/Dec |
| 运动户外 — Sports | Jun ¥380,445 | Feb ¥194,106 | **0.271** | Flattest row; the only large category peaking in June |
| 家居生活 — Home | Jun ¥235,515 | Jul ¥103,974 | 0.338 | Almost a scaled copy of the overall pattern |
| 美妆个护 — Beauty | Nov ¥196,132 | Jul ¥85,391 | 0.322 | Strong November (1.76×); weak July/August |
| 食品饮料 — Food | Nov ¥74,848 | Oct ¥32,418 | 0.332 | Low absolute level; October is its softest month |
| 母婴用品 — Baby | Jun ¥74,403 | **Dec ¥19,348** | **0.486** | Most seasonal row; June 2.10×, Nov 1.90×, then a December collapse (0.55×) |
| 图书文具 — Books | Jun ¥23,745 | Sep ¥8,667 | 0.331 | Second-weakest peak (1.53× in Nov) but uniquely strong December (1.24×) |

Three deviations are worth calling out:

- **Mother & Baby is the most volatile row** (CV 0.486). Its June and November cells are
  the darkest relative to its own baseline, yet December is the palest cell in the entire
  row — consistent with demand being pulled forward into the two promotional months and
  no December gifting tail.
- **Books & Stationery behaves differently at the edges:** it has one of the weakest
  June/November uplifts of any category, but a uniquely strong December (index 1.24; no
  other non-peak month exceeds 1.03). It is also the only row where September, not July,
  is the trough.
- **Sports & Outdoors is the least seasonal** (CV 0.271) and the only sizeable category
  whose June cell is darker than its November cell.

---

## Reading notes and limitations

- **Intensity is not normalised within rows.** The palette encodes absolute CNY, so
  large categories are dark in every month and small categories are pale in every month.
  To read seasonality, compare across a row; to read scale, compare down a column.
- **Two years are collapsed into one calendar.** The chart cannot show year-over-year
  growth, and a category whose 2024 and 2025 patterns differ would show a blended cell.
  Here the June/November peaks appear in both years, so the blend is representative.
- **Months are not day-normalised.** The totals are calendar-month sums; February is
  structurally short. Per-day figures (shown above) leave the same broad ranking — a
  large June/November lead, July last — so the seasonal reading is unaffected.
- **Revenue only.** The chart does not encode profit, units, discount or customer
  counts. The line-level evidence indicates the peaks come from order volume, but that
  is a separate calculation, not something the heatmap itself proves.
- **Order-line grain.** Multiple lines from one order are counted separately, so a
  single large order can lift one cell.
- **Completed orders only.** Cancelled, returned and pending lines are excluded, as are
  the 3,118 zero-revenue completed lines.
- **Synthetic data.** The dataset is simulated for practice; the chart describes this
  file, not a real retailer.

---

## Bottom line

The heatmap shows a **category hierarchy crossed by a common promotional calendar**.
Digital Electronics (43.09%) is dark in every month and supplies both brightest cells
(Nov ¥1.12M, Jun ¥1.10M); Apparel and Sports form a clear second tier; Food, Baby and
Books stay pale regardless of season. Layered on top, **June and November lift every
category by roughly 1.5–2.1×**, together producing 27.89% of two-year revenue, and the
lift is volume-driven and spread across the month rather than concentrated on a single
day. The category-specific signal is mainly in the residuals: Baby is the most
seasonal and falls away in December, Books is the least promotional but has a December
bump, and Sports is the flattest row and the only large category that peaks in June.
