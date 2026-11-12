# Category → Sub-category Revenue Treemap

**Chart:** [`output/charts/category_revenue_treemap.png`](../charts/category_revenue_treemap.png)  
**Script:** `scripts/charts/plot_category_treemap.py`  
**Data:** `data/raw/huagou_mall_synthetic_ecommerce.csv`  
**Population:** Completed order lines with `Revenue_CNY > 0`; Jan 2024 – Dec 2025

---

## What the chart encodes

| Element | Meaning |
|---|---|
| Outer block | Product `Category` (8 blocks) |
| Inner tile | Product `Subcategory` (32 tiles, four per category) |
| Rectangle **area** | `Revenue_CNY` summed over the population |
| Colour | Parent category; darker tiles are the larger sub-categories within it |
| Label | Sub-category name + revenue + **share of total revenue**, where it fits |

- **Area is proportional to revenue**, so the chart is a part-to-whole view: every
  rectangle's share of the treemap equals its share of the ¥18,222,902.98 total.
- **Percentages are shares of the grand total**, not shares of the parent category.
  Category headers repeat the category revenue and total share.
- **20 of 32 tiles carry both revenue and percentage.** Seven small tiles carry a
  name only; the five tiles too small to letter are reported in the chart footnote
  so their values are still on the page rather than squeezed into illegible text.
- **Excluded:** 3,118 completed lines with `Revenue_CNY = 0` (all have
  `Profit_CNY = 0`). They would add rectangles with no area and distort line-based
  rates, so the analysis retains only the 49,327 revenue-bearing lines.

---

## Headline

**数码电子 (Digital Electronics) is the largest category, and 电脑配件 (Computer
Accessories) is the largest sub-category.**

| Rank | Category | Revenue (CNY) | Share | Cumulative | Lines | Revenue / line |
|---:|---|---:|---:|---:|---:|---:|
| 1 | 数码电子 — Digital Electronics | ¥7,852,159.99 | **43.09%** | 43.09% | 15,477 | ¥507.34 |
| 2 | 服饰鞋包 — Apparel & Bags | ¥3,468,284.80 | 19.03% | 62.12% | 8,416 | ¥412.11 |
| 3 | 运动户外 — Sports & Outdoors | ¥2,867,731.40 | 15.74% | 77.86% | 5,663 | ¥506.40 |
| 4 | 家居生活 — Home & Living | ¥1,592,606.10 | 8.74% | 86.60% | 8,598 | ¥185.23 |
| 5 | 美妆个护 — Beauty & Personal Care | ¥1,334,568.98 | 7.32% | 93.92% | 5,157 | ¥258.79 |
| 6 | 食品饮料 — Food & Beverage | ¥512,405.50 | 2.81% | 96.73% | 3,251 | ¥157.61 |
| 7 | 母婴用品 — Mother & Baby | ¥424,285.81 | 2.33% | 99.06% | 1,484 | ¥285.91 |
| 8 | 图书文具 — Books & Stationery | ¥170,860.40 | 0.94% | 100.00% | 1,281 | ¥133.38 |

Digital Electronics earns **2.3×** the revenue of the next category and accounts for
**43.09%** of all revenue from **31.38%** of the lines. Its higher revenue per line
(¥507 vs ¥369 overall) reflects a more expensive product mix, not simply more orders.

### Largest sub-categories

| Rank | Sub-category | Category | Revenue (CNY) | Share of total | Share of category |
|---:|---|---|---:|---:|---:|
| 1 | 电脑配件 — Computer Accessories | Digital Electronics | ¥2,737,165.84 | **15.02%** | 34.86% |
| 2 | 音频设备 — Audio Equipment | Digital Electronics | ¥2,329,209.32 | 12.78% | 29.66% |
| 3 | 手机配件 — Phone Accessories | Digital Electronics | ¥1,749,779.53 | 9.60% | 22.28% |
| 4 | 男装 — Men's Clothing | Apparel & Bags | ¥1,103,597.24 | 6.06% | 31.82% |
| 5 | 智能设备 — Smart Devices | Digital Electronics | ¥1,036,005.30 | 5.69% | 13.19% |
| 6 | 鞋靴 — Footwear | Apparel & Bags | ¥958,029.59 | 5.26% | 27.62% |
| 7 | 健身用品 — Fitness Equipment | Sports & Outdoors | ¥905,144.30 | 4.97% | 31.56% |
| 8 | 运动服饰 — Activewear | Sports & Outdoors | ¥870,547.96 | 4.78% | 30.36% |
| 9 | 箱包配饰 — Bags & Accessories | Apparel & Bags | ¥859,874.46 | 4.72% | 24.79% |
| 10 | 户外装备 — Outdoor Gear | Sports & Outdoors | ¥721,951.33 | 3.96% | 25.17% |

The three largest Digital sub-categories together produce **¥6.82M — 37.40% of all
revenue — and 86.81% of Digital's revenue**. Computer Accessories alone is equivalent
to **16× the entire Books & Stationery category**.

---

## Concentration

### Category level

- **Top 3 categories = 77.86%** of revenue; **top 5 = 93.92%**.
- The remaining three categories (Food, Baby, Books) share **6.08%** between them.
- Digital Electronics, Apparel and Sports form the commercial core. Home & Living and
  Beauty are meaningful secondary categories; Food, Baby and Books are marginal.
- **Digital and Sports earn almost the same revenue per line** (¥507.34 vs ¥506.40),
  but Digital has **2.7× as many lines**. Apparel is close behind at ¥412.11.

### Sub-category level

- **Top 3 sub-categories = 37.40%**; **top 5 = 49.15%**; **top 10 = 72.83%**.
- The other **22 sub-categories share 27.17%**, and the **bottom 10 share only 4.13%**.
- **14 of 32 sub-categories earn less than ¥300K**, together just **8.35%** of revenue.
- Median sub-category revenue is **¥348,856**; the mean is **¥569,466**, so the
  distribution is pulled right by a handful of large tiles.
- The largest sub-category (¥2.74M) is **232.9×** the smallest (¥11.8K).

The pattern is a classic **Pareto shape**: 10 of 32 sub-categories generate almost
three-quarters of revenue, while the bottom third of tiles is commercially negligible.

### Concentration repeats inside categories

Every category is itself top-heavy, and the top three sub-categories always account
for more than 80% of their category:

| Category | Largest sub-category | Share of category | Top 3 share |
|---|---|---:|---:|
| Digital Electronics | Computer Accessories | 34.9% | 86.8% |
| Apparel & Bags | Men's Clothing | 31.8% | 84.2% |
| Sports & Outdoors | Fitness Equipment | 31.6% | 87.1% |
| Home & Living | Storage & Organisation | 36.6% | 83.8% |
| Beauty & Personal Care | Fragrance | 36.1% | 88.4% |
| Food & Beverage | Grains, Oil & Seasoning | 38.2% | 83.3% |
| Mother & Baby | Toys | 37.4% | 90.5% |
| Books & Stationery | Books | 53.4% | 93.1% |

So the treemap's concentration is **not only a Digital story**. Within almost every
category one or two sub-categories dominate; Digital differs by **scale**, not by
having a uniquely skewed internal mix.

---

## The long tail

- **Books & Stationery is the clearest long tail:** the whole category (¥170.9K,
  0.94%) is smaller than the single largest sub-category by a factor of 16, and its
  smallest tile — 办公文具 (Office Stationery) at **¥11,751.93 (0.06%)** — is almost
  invisible.
- The four smallest sub-categories — 办公文具 ¥11.8K, 学习用品 ¥27.7K,
  创意用品 ¥40.2K, 婴儿护理 ¥40.5K — together contribute **¥120,088.82 (0.66%)**.
- Food & Beverage and Mother & Baby are small overall but not uniformly tiny: their
  leading tiles (粮油调味 ¥195.5K; 玩具 ¥158.6K) are comparable to mid-sized tiles in
  larger categories, while their last tiles drop below ¥80K.
- **The tail is short in revenue terms.** The bottom 10 tiles still sum to 4.13% of
  revenue, and the 14 sub-categories under ¥300K sum to 8.35%. Most of that tail sits
  in the ¥100K–¥300K range, not in the micro-slices; only the last few tiles are
  effectively rounding error.
- All 32 sub-categories are drawn — there is no “Other” bucket. The five slices too
  small to letter are reported in the chart footnote, so the long tail is visible in
  area even where it cannot be labelled.

---

## Reading notes and limitations

- **Area judgments are approximate.** Treemaps are strong for part-to-whole comparison
  and weak for precise ratios; use the tables above for exact figures. Very small
  tiles also exaggerate how little they contribute.
- **Revenue only.** The chart does not encode profit, unit volume or discount. High
  revenue can come from high unit price, high quantity, or both.
- **Line grain.** Each source row is an order line; multiple lines from one order are
  not consolidated, so a single large order can contribute several tiles' worth of
  revenue to one sub-category.
- **Completed orders only.** Cancelled, returned and pending lines are outside the
  population; the 3,118 zero-revenue completed lines are excluded.
- **Synthetic data.** The dataset is simulated for analysis practice; no causal or
  market-share claim about a real retailer is warranted.
- **Different price/quantity mixes.** The categories are not volume-equivalent:
  revenue per line ranges from ¥133 (Books) to ¥507 (Digital), so the treemap reflects
  basket value as well as line counts.

---

## Bottom line

HuaGou Mall's revenue is a **Digital Electronics business with two supporting
categories**. Digital Electronics contributes **43.09%**, and its three largest
sub-categories alone contribute **37.40%** of all revenue; Computer Accessories
(¥2.74M, 15.02%) is the single biggest tile. Apparel (19.03%) and Sports (15.74%)
complete a core that accounts for **77.86%** of revenue. Home, Beauty, Food, Baby and
Books form a thin tail: the entire Books category is under 1%, and the bottom 10
sub-categories together are just 4.13%. The treemap makes the priority obvious —
**protect and grow the Digital, Apparel and Sports core**, and treat the remaining
categories as low-revenue niches rather than equal pillars.
