# HuaGou Mall E-commerce — Data Analysis Portfolio Project

Chart-focused analysis of the synthetic HuaGou Mall e-commerce dataset (China, CNY,
Jan 2024 – Dec 2025).

## Project structure

```
Portfolio Project - 1/
├── data/
│   └── raw/
│       └── huagou_mall_synthetic_ecommerce.csv   # source data (immutable)
├── scripts/
│   └── charts/                                   # chart generation scripts
├── output/
│   ├── charts/                                   # generated PNG charts
│   └── reports/                                  # terminal / text / markdown reports
├── dashboard/                                    # dashboard application (not built yet)
├── docs/
│   └── dataset_inspection.md                     # dataset profile and analytical caveats
└── README.md
```

## Status

- [x] Source CSV located and profiled
- [x] Project scaffolding created
- [x] Dataset inspection report written — see [`docs/dataset_inspection.md`](docs/dataset_inspection.md)
- [x] Chart 1: completed-line revenue histogram
      — [`scripts/charts/plot_revenue_histogram.py`](scripts/charts/plot_revenue_histogram.py)
      — [`output/charts/completed_line_revenue_histogram.png`](output/charts/completed_line_revenue_histogram.png)
      — [`output/reports/revenue_histogram_report.md`](output/reports/revenue_histogram_report.md)
- [x] Chart 2: completed-line revenue KDE
      — [`scripts/charts/plot_revenue_kde.py`](scripts/charts/plot_revenue_kde.py)
      — [`output/charts/completed_line_revenue_kde.png`](output/charts/completed_line_revenue_kde.png)
      — [`output/reports/revenue_kde_report.md`](output/reports/revenue_kde_report.md)
- [x] Chart 3: revenue by product category box plot
      — [`scripts/charts/plot_category_revenue_box.py`](scripts/charts/plot_category_revenue_box.py)
      — [`output/charts/category_revenue_boxplot.png`](output/charts/category_revenue_boxplot.png)
      — [`output/reports/category_revenue_boxplot_report.md`](output/reports/category_revenue_boxplot_report.md)
- [x] Chart 4: revenue by product category violin plot
      — [`scripts/charts/plot_category_revenue_violin.py`](scripts/charts/plot_category_revenue_violin.py)
      — [`output/charts/category_revenue_violin.png`](output/charts/category_revenue_violin.png)
      — [`output/reports/category_revenue_violin_report.md`](output/reports/category_revenue_violin_report.md)
- [x] Chart 5: discount vs profit scatter plot
      — [`scripts/charts/plot_discount_vs_profit_scatter.py`](scripts/charts/plot_discount_vs_profit_scatter.py)
      — [`output/charts/discount_vs_profit_scatter.png`](output/charts/discount_vs_profit_scatter.png)
      — [`output/reports/discount_vs_profit_scatter_report.md`](output/reports/discount_vs_profit_scatter_report.md)
- [x] Chart 6: price, quantity, revenue and profit pair plot
      — [`scripts/charts/plot_pairplot.py`](scripts/charts/plot_pairplot.py)
      — [`output/charts/price_quantity_revenue_profit_pairplot.png`](output/charts/price_quantity_revenue_profit_pairplot.png)
      — [`output/reports/pairplot_report.md`](output/reports/pairplot_report.md)
- [x] Chart 7: unit price vs profit bubble plot (quantity as area)
      — [`scripts/charts/plot_price_profit_bubbles.py`](scripts/charts/plot_price_profit_bubbles.py)
      — [`output/charts/price_profit_quantity_bubbles.png`](output/charts/price_profit_quantity_bubbles.png)
      — [`output/reports/price_profit_quantity_bubbles_report.md`](output/reports/price_profit_quantity_bubbles_report.md)
- [x] Chart 8: category → sub-category revenue treemap
      — [`scripts/charts/plot_category_treemap.py`](scripts/charts/plot_category_treemap.py)
      — [`output/charts/category_revenue_treemap.png`](output/charts/category_revenue_treemap.png)
      — [`output/reports/category_revenue_treemap_report.md`](output/reports/category_revenue_treemap_report.md)
- [x] Chart 9: category × month revenue heatmap
      — [`scripts/charts/plot_category_month_heatmap.py`](scripts/charts/plot_category_month_heatmap.py)
      — [`output/charts/category_month_revenue_heatmap.png`](output/charts/category_month_revenue_heatmap.png)
      — [`output/reports/category_month_revenue_heatmap_report.md`](output/reports/category_month_revenue_heatmap_report.md)
- [ ] Remaining chart scripts
- [x] Dashboard application
      — [`dashboard/index.html`](dashboard/index.html)
      — [`dashboard/prepare_data.py`](dashboard/prepare_data.py)
      — [`dashboard/run_dashboard.py`](dashboard/run_dashboard.py)

## Source data

| Item | Value |
|---|---|
| File | `data/raw/huagou_mall_synthetic_ecommerce.csv` |
| Rows | 60,000 order lines |
| Columns | 27 |
| Grain | Order line (31,804 distinct orders) |
| Encoding | UTF-8 with BOM |
| Period | 2024-01-01 to 2025-12-31 |
| Currency | CNY |

The source file is treated as read-only. SHA-256:
`20E741DDE6D89FC523315E76A93334C70025599940C431614A9379F762EEAF78`

## Tooling

Python 3.14 with pandas 3.0.3 was used for inspection. No other libraries were
installed. Future chart scripts should write PNGs to `output/charts/` and textual
results to `output/reports/`.
