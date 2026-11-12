# Dataset Inspection Report — HuaGou Mall Synthetic E-commerce

**Report date:** 2026-11-12  
**Source:** `data/raw/huagou_mall_synthetic_ecommerce.csv`  
**SHA-256:** `20E741DDE6D89FC523315E76A93334C70025599940C431614A9379F762EEAF78` (unchanged)  
**Scope:** Profile only. No source edits, charts, or dashboard yet.

---

## 1. Snapshot

| Metric | Value |
|---|---:|
| Rows | 60,000 |
| Columns | 27 |
| Distinct orders | 31,804 |
| Distinct customers | 15,000 |
| Distinct products | 500 |
| Date coverage | 2024-01-01 → 2025-12-31 (731 days, no gaps) |
| Grain | One row per order **line**, not per order |
| Encoding / currency | UTF-8 with BOM / CNY |
| All-status revenue | ¥19,368,440.12 |
| Completed revenue | ¥18,222,902.98 (94.09%) |
| All-status profit | ¥4,785,395.94 |
| Completed profit | ¥4,507,434.50 |
| Gross margin | 24.71% (all statuses) |
| Exact duplicate rows | 0 |
| Missing cells | 307 (`Delivery_Days` only, 0.51%) |
| Zero-revenue lines | 7,540 (12.57%) |

---

## 2. Grain and dimensions

The CSV is **order-line-level**: `Order_ID` repeats for each product line in an order.

- 60,000 lines across 31,804 orders → **1.89 lines per order** (median 2, max 5).
- 19,096 orders (60.0%) contain more than one line.
- 86 `(Order_ID, Product_ID)` pairs repeat within an order, with different quantity,
  discount, or rating. There is no line-item ID, so these are separate lines and must
  **not** be dropped as duplicates.
- Order-level attributes (date, status, channel, customer, geography, payment, shipping)
  are consistent within every `Order_ID`.
- `Delivery_Days` varies within 15,315 orders (48.2%) and `Customer_Rating` within
  14,645 orders (46.0%), so those two fields behave like line-level/additive fields,
  not order headers.

**Double-counting risk:** counting rows gives 60,000 "orders" instead of 31,804
(a 1.89× inflation). Order-level tables must be built with
`groupby("Order_ID").agg(...)`, summing revenue/profit/quantity — never by taking the
first row's revenue.

---

## 3. Schema

Types are as read by pandas. `Order_Date` is stored as text and should be parsed as a date.

| # | Column | Type | Unique | Missing | Notes |
|---:|---|---|---:|---:|---|
| 1 | Order_ID | string | 31,804 | 0 | Order key, `HG-######`; repeats per line |
| 2 | Order_Date | string (date) | 731 | 0 | `YYYY-MM-DD`; 2024-01-01 → 2025-12-31 |
| 3 | Order_Status | string | 5 | 0 | Completed, Cancelled, Returned, Awaiting Shipment, Processing |
| 4 | Sales_Channel | string | 4 | 0 | Mobile App, Website, Marketplace, Mini Program |
| 5 | Customer_ID | string | 15,000 | 0 | Customer key, `C-#####` |
| 6 | Customer_Name_CN | string | 8,865 | 0 | Display label only; not unique |
| 7 | Customer_Name_EN | string | 910 | 0 | Display label only; not unique |
| 8 | Phone_Number | int64 | 15,000 | 0 | 1:1 with `Customer_ID`; 11 digits |
| 9 | Customer_Segment | string | 3 | 0 | New, Regular, VIP |
| 10 | City | string | 59 | 0 | Chinese city labels |
| 11 | Province | string | 20 | 0 | Chinese province labels |
| 12 | Region | string | 5 | 0 | East, South, North, West, Central |
| 13 | Product_ID | string | 500 | 0 | Product key, `P-######` |
| 14 | Product_Name_CN | string | 352 | 0 | Display label only; not unique |
| 15 | Product_Name_EN | string | 329 | 0 | 118 EN names map to >1 product ID |
| 16 | Category | string | 8 | 0 | Chinese category labels |
| 17 | Subcategory | string | 32 | 0 | Consistent within its category |
| 18 | Unit_Price_CNY | float | 497 | 0 | List price; constant per product |
| 19 | Quantity | int64 | 5 | 0 | 1–5 units per line |
| 20 | Discount_Percentage | float | 578 | 0 | Percentage points, 0–65 (not a fraction) |
| 21 | Unit_Cost_CNY | float | 492 | 0 | Constant per product |
| 22 | Revenue_CNY | float | 32,873 | 0 | Line revenue after discount |
| 23 | Profit_CNY | float | 21,246 | 0 | Line gross profit; can be negative |
| 24 | Payment_Method | string | 5 | 0 | Alipay, WeChat Pay, UnionPay, Credit Card, Cash on Delivery |
| 25 | Shipping_Method | string | 4 | 0 | Standard Express, Pickup Point, Economy, Same-Day |
| 26 | Delivery_Days | float | 8 | 307 | 0–7; missing for open orders |
| 27 | Customer_Rating | int64 | 5 | 0 | 1–5; present for every status (see caveats) |

---

## 4. Keys and identifier quality

| Identifier | Distinct | Notes |
|---|---:|---|
| Order_ID | 31,804 | Safe order key; all rows match `HG-\d{6}` |
| Order line | 60,000 | No explicit line ID |
| (Order_ID, Product_ID) | 59,914 | 86 repeated pairs — separate lines, not duplicates |
| Customer_ID | 15,000 | Safe customer key; all rows match `C-\d{5}` |
| Phone_Number | 15,000 | 1:1 with `Customer_ID`; complete, 11 digits |
| Product_ID | 500 | Safe product key; all rows match `P-\d{6}` |
| Customer_Name_EN | 910 | Not a key: up to 42 customers share one name |
| Product_Name_EN | 329 | Not a key: up to 5 product IDs share one name |
| Order_Date | 731 | Daily; every day in the range is present |

- Use `Customer_ID` / `Product_ID` for joins and `nunique()` counts.
- `Phone_Number` is complete and unique per customer but stored as an integer; read it
  as a string in future pipelines to avoid accidental numeric formatting.
- Geography is internally consistent (each city maps to exactly one province, each
  province to exactly one region): 59 cities, 20 provinces, 5 regions. Each
  subcategory likewise belongs to exactly one category.

---

## 5. Missing values, duplicates, and validity

- **Missing:** only `Delivery_Days`, 307 rows (0.51%): 102 Awaiting Shipment, 83
  Processing, 116 Completed, 6 Returned. All Cancelled lines have `Delivery_Days = 0`.
- **Exact duplicates:** none.
- **Repeated order/product pairs:** 86 pairs / 86 extra rows, with genuinely different
  quantities or discounts. Do not deduplicate.
- No blank strings, placeholder tokens, or whitespace anomalies were found.
- Ranges are plausible: quantity 1–5, discount 0–65%, unit price ¥6.96–¥1,538.13,
  unit cost ¥3.98–¥1,020.52, revenue ¥0–¥7,105, profit −¥959.65–¥2,679.10,
  delivery 0–7 days, rating 1–5.

### Zero-revenue lines (important)

7,540 lines (12.57%) have `Revenue_CNY = 0` **and** `Profit_CNY = 0`, while their
price, quantity, and discount are populated.

| Status | Zero-revenue lines | Share of status rows |
|---|---:|---:|
| Completed | 3,118 | 5.95% |
| Cancelled | 2,491 | 58.34% |
| Returned | 1,822 | 58.77% |
| Awaiting Shipment | 65 | 63.73% |
| Processing | 44 | 53.01% |
| **Total** | **7,540** | **12.57%** |

These are not "100% discount" giveaways — a true giveaway would show negative profit
equal to cost. They look like voided/zeroed lines. 1,767 orders are entirely
zero-revenue, and 6,955 orders (21.9%) contain at least one such line. Excluding them
changes line counts, unit volumes, and averages, so the choice must be explicit and
consistent across charts.

---

## 6. Derived-field validation

The financial fields are internally consistent:

```
Revenue_CNY = Unit_Price_CNY × Quantity × (1 − Discount_Percentage / 100)
Profit_CNY  = Revenue_CNY − (Unit_Cost_CNY × Quantity)
```

- Both formulas match within ¥0.01 on all **52,460 revenue-bearing lines**.
- The 7,540 zero-revenue lines do **not** obey the revenue formula; their financials
  were zeroed after calculation. Never recompute revenue from price × quantity for
  these rows without handling them first.
- Six revenue-bearing lines happen to break even exactly (`Profit_CNY = 0`), where
  discounted price equals unit cost.
- `Profit_CNY` is **gross margin**: it excludes shipping income/cost, payment fees,
  platform commissions, returns handling, marketing, tax, and overhead.
- 4,299 revenue-bearing lines (8.19%) have negative margin (min −124.3%), driven by
  discounts of 18.5–65% exceeding the product's markup. This is plausible synthetic
  pricing behaviour, not necessarily an error.

---

## 7. Order status: revenue and profit implications

| Status | Lines | Orders | % of orders | Revenue (CNY) | Profit (CNY) | % of all-status revenue |
|---|---:|---:|---:|---:|---:|---:|
| Completed | 52,445 | 27,826 | 87.49% | 18,222,902.98 | 4,507,434.50 | 94.09% |
| Cancelled | 4,270 | 2,235 | 7.03% | 663,541.77 | 161,030.76 | 3.43% |
| Returned | 3,100 | 1,642 | 5.16% | 457,158.06 | 111,544.64 | 2.36% |
| Awaiting Shipment | 102 | 60 | 0.19% | 13,404.01 | 2,143.61 | 0.07% |
| Processing | 83 | 41 | 0.13% | 11,433.30 | 3,242.43 | 0.06% |
| **Total** | **60,000** | **31,804** | **100%** | **19,368,440.12** | **4,785,395.94** | **100%** |

**Recommended revenue convention**

- **Realized revenue/profit = `Order_Status == "Completed"`** → ¥18,222,902.98 revenue,
  ¥4,507,434.50 profit, 24.74% margin, AOV ¥654.89.
- Treat **Cancelled + Returned** (¥1,120,699.83; 5.79% of all-status revenue) as lost
  sales and exclude from realized totals.
- Treat **Awaiting Shipment + Processing** (¥24,837.31; 0.13%) as open/unrecognized and
  exclude from realized totals as well.
- All-status totals (¥19.37M) are useful only as a gross, pre-cancellation view. State
  which convention every chart/report uses.

**Status caveats**

- Status is consistent within an order (no mixed-status orders).
- **Status does not reliably align with the money fields:** 1,779 Cancelled lines and
  1,278 Returned lines carry positive revenue/profit (3,057 lost lines, ¥1.12M). A
  zero-revenue filter is therefore **not** a valid substitute for a status filter, and
  a status filter does not remove all zeroed rows.
- There is no refund amount, return reason, cancellation timestamp, or negative
  adjustment column. Net-of-refund revenue cannot be calculated; filtering is the only
  defensible approach.
- Open statuses appear throughout the full two-year window (Awaiting Shipment from
  2024-06, Processing from 2024-06), not just at the end. They look stale/synthetic, so
  do not treat them as a live operational backlog.

---

## 8. Analytical caveats and recommendations

### Order-level vs order-line-level

1. Count orders with `nunique(Order_ID)`, never `len(df)`.
2. Build an order table by aggregating lines: sum revenue, profit, and quantity; count
   lines; carry order attributes once. Do not use `.first()` for financial columns.
3. Use line grain for product, category, discount, and basket-composition analysis.
   Use order grain for AOV, order counts, cancellation/return rates, and customer
   purchase frequency.
4. Keep the 86 repeated order/product pairs; deduplicating loses real quantity and
   discount differences. If a product-level per-order view is needed, aggregate them
   explicitly instead of dropping rows.
5. For per-order rating/delivery summaries, aggregate (mean/max) and label them as
   line-derived; do not merge line-level values onto an order table as if they were
   order headers.

### Revenue and profit

6. Zero-revenue lines should be excluded from revenue, margin, and AOV analysis. They
   materially affect "average line value" and "discount vs revenue" charts. Report the
   exclusion, and keep them separate for volume diagnostics.
7. Report gross vs realized figures explicitly. Cancelled/returned/open orders account
   for 5.92% of all-status revenue.
8. Profit is gross margin only; do not call it net profit. Contribution margin, net
   revenue, and refund-adjusted profit are not computable from this file.
9. Negative-margin lines are real in this synthetic data (deep discounts), so margin
   charts should retain them and annotate rather than clip them.

### Field reliability

10. **Customer_Rating is not reliable post-delivery CSAT.** Ratings exist for Cancelled,
    Processing, and Awaiting Shipment lines, and ratings differ within 46% of orders.
    Restrict satisfaction analysis to Completed lines, aggregate to order grain, and
    state that the rating is synthetic/line-assigned.
11. **Delivery_Days is not operationally meaningful.** All Cancelled lines are 0 days,
    2,695 Completed lines are 0 days, 307 values are missing, and mean delivery is
    ~2.95 days for every shipping method (Same-Day 3.02 vs Economy 2.92). Do not use
    shipping method as a delivery-speed driver.
12. **Names are labels, not keys.** 910 English customer names cover 15,000 customers;
    118 English product names map to multiple product IDs.
13. Cancelled orders combine a rating with zero delivery days, an impossible real-world
    combination — a further reason to filter before satisfaction/delivery charts.

### Time and scope

14. Data is a complete daily calendar (731 days) with balanced years: 2024 = 30,087
    lines, 2025 = 29,913 lines; revenue ¥9.79M vs ¥9.58M.
15. Strong campaign seasonality: June and November order counts roughly double the
    ~1,100/month baseline in both years (Jun 2024: 2,334; Nov 2024: 2,250; Jun 2025:
    2,176; Nov 2025: 2,240). Likely 618 and Double 11 effects. Annotate these months
    and prefer year-over-year comparisons over naive month-over-month growth.
16. Not available: refunds, shipping fees, tax, campaign/promo flags, line IDs, delivery
    dates, or profit components. Do not imply these metrics exist.

---

## 9. Suggested analysis conventions

| Analysis | Grain | Base filter |
|---|---|---|
| Realized revenue / profit / margin | Order line | `Order_Status == "Completed"` and `Revenue_CNY > 0` |
| Gross pre-cancellation view | Order line | No status filter; label as gross |
| Order volume / AOV | Order | Completed (or all orders, labelled) |
| Cancellation / return rate | Order | All orders in denominator; status in numerator |
| Category / product / channel performance | Order line | Completed, positive revenue |
| Discount / margin diagnostics | Order line | Revenue-bearing lines, all statuses (label mix) |
| Customer satisfaction | Order (aggregated) | Completed only |
| Delivery performance | Order line | Completed with non-null `Delivery_Days > 0` |

**Working rules:** parse `Order_Date`; cast IDs and phone to string; keep the raw CSV
read-only; compute all derived flags (`is_zero_revenue`, `is_realized`, `is_lost`,
`is_open`) in scripts rather than editing the source.

---

## 10. Next steps

1. Build charting scripts in `scripts/charts/`, writing PNGs to `output/charts/`.
2. Emit terminal/summary outputs to `output/reports/`.
3. Build the dashboard in `dashboard/` only after the chart set and conventions are
   agreed.

No libraries beyond the existing pandas installation were added for this inspection.
