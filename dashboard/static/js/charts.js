/**
 * HuaGou Mall E-Commerce Interactive Plotly Charts Engine
 * Implements all 9 analytical charts with responsive theming (Light/Dark mode)
 */

window.HuagouCharts = (function () {
  function checkPlotly(elementId) {
    if (!window.Plotly) {
      const el = document.getElementById(elementId);
      if (el) {
        el.innerHTML = '<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;color:var(--text-muted);font-size:0.88rem;gap:0.5rem;"><span style="font-size:1.5rem;">📊</span><span>Plotly.js is loading from CDN. Please ensure an active internet connection.</span></div>';
      }
      return false;
    }
    return true;
  }

  // Theme styling palette
  function getThemeColors() {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    return {
      isDark,
      paperBg: isDark ? '#111827' : '#FFFFFF',
      plotBg: isDark ? '#111827' : '#FFFFFF',
      text: isDark ? '#F1F5F9' : '#1E293B',
      textMuted: isDark ? '#94A3B8' : '#64748B',
      grid: isDark ? '#1F293D' : '#E2E8F0',
      border: isDark ? '#334155' : '#CBD5E1',
      teal: isDark ? '#38BDF8' : '#0EA5E9',
      tealDark: isDark ? '#0284C7' : '#0F2F38',
      emerald: isDark ? '#34D399' : '#10B981',
      amber: isDark ? '#FBBF24' : '#F59E0B',
      rose: isDark ? '#FB7185' : '#F43F5E',
      purple: isDark ? '#A78BFA' : '#8B5CF6',
      grey: isDark ? '#475569' : '#94A3B8',
      heatScale: isDark
        ? [
            [0.0, '#0B192C'],
            [0.2, '#1E3E62'],
            [0.4, '#005F73'],
            [0.7, '#0A9396'],
            [1.0, '#38BDF8']
          ]
        : [
            [0.0, '#F4F8F8'],
            [0.2, '#D8E9EB'],
            [0.4, '#7FAFB8'],
            [0.7, '#2B6B7A'],
            [1.0, '#0F2F38']
          ]
    };
  }

  function getBaseLayout(title, xTitle = '', yTitle = '') {
    const theme = getThemeColors();
    return {
      title: title ? { text: title, font: { size: 15, color: theme.text, weight: 700 } } : undefined,
      font: { family: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif', color: theme.text },
      paper_bgcolor: theme.paperBg,
      plot_bgcolor: theme.plotBg,
      margin: { l: 55, r: 25, t: 45, b: 45 },
      xaxis: {
        title: xTitle ? { text: xTitle, font: { size: 12, color: theme.textMuted } } : undefined,
        gridcolor: theme.grid,
        zerolinecolor: theme.grid,
        tickfont: { color: theme.textMuted, size: 11 }
      },
      yaxis: {
        title: yTitle ? { text: yTitle, font: { size: 12, color: theme.textMuted } } : undefined,
        gridcolor: theme.grid,
        zerolinecolor: theme.grid,
        tickfont: { color: theme.textMuted, size: 11 }
      },
      hoverlabel: {
        bgcolor: theme.isDark ? '#1E293B' : '#FFFFFF',
        bordercolor: theme.border,
        font: { color: theme.text, size: 12 }
      }
    };
  }

  // --- Overview Tab Charts ---

  function renderMonthlyTrend(elementId, trendData) {
    if (!checkPlotly(elementId) || !trendData || !document.getElementById(elementId)) return;
    const theme = getThemeColors();

    // Group by YearMonth for completed status
    const completedByMonth = {};
    trendData.forEach(d => {
      if (d.Order_Status === 'Completed') {
        completedByMonth[d.YearMonth] = {
          rev: (completedByMonth[d.YearMonth]?.rev || 0) + d.revenue,
          prof: (completedByMonth[d.YearMonth]?.prof || 0) + d.profit,
          orders: (completedByMonth[d.YearMonth]?.orders || 0) + d.orders
        };
      }
    });

    const months = Object.keys(completedByMonth).sort();
    const revs = months.map(m => completedByMonth[m].rev);
    const profs = months.map(m => completedByMonth[m].prof);

    const traceRev = {
      x: months,
      y: revs,
      name: 'Revenue (CNY)',
      type: 'scatter',
      mode: 'lines+markers',
      line: { color: theme.teal, width: 3, shape: 'spline' },
      marker: { size: 6, color: theme.teal },
      fill: 'tozeroy',
      fillcolor: theme.isDark ? 'rgba(56, 189, 248, 0.12)' : 'rgba(14, 165, 233, 0.10)',
      hovertemplate: '<b>%{x}</b><br>Revenue: ¥%{y:,.2f}<extra></extra>'
    };

    const traceProf = {
      x: months,
      y: profs,
      name: 'Gross Profit (CNY)',
      type: 'scatter',
      mode: 'lines+markers',
      line: { color: theme.emerald, width: 2.5, dash: 'dot', shape: 'spline' },
      marker: { size: 5, color: theme.emerald },
      hovertemplate: '<b>%{x}</b><br>Profit: ¥%{y:,.2f}<extra></extra>'
    };

    const layout = getBaseLayout('', 'Month (2024 - 2025)', 'Amount (CNY)');
    layout.legend = { orientation: 'h', y: 1.12, x: 0.0, font: { color: theme.textMuted } };
    layout.annotations = [
      {
        x: '2024-06',
        y: completedByMonth['2024-06']?.rev || 1200000,
        text: '🔥 618 Gala (2024)',
        showarrow: true,
        arrowhead: 2,
        arrowcolor: theme.amber,
        font: { size: 10, color: theme.amber, weight: 700 }
      },
      {
        x: '2024-11',
        y: completedByMonth['2024-11']?.rev || 1300000,
        text: '🛍️ Double 11 (2024)',
        showarrow: true,
        arrowhead: 2,
        arrowcolor: theme.amber,
        font: { size: 10, color: theme.amber, weight: 700 }
      },
      {
        x: '2025-06',
        y: completedByMonth['2025-06']?.rev || 1200000,
        text: '🔥 618 Gala (2025)',
        showarrow: true,
        arrowhead: 2,
        arrowcolor: theme.amber,
        font: { size: 10, color: theme.amber, weight: 700 }
      },
      {
        x: '2025-11',
        y: completedByMonth['2025-11']?.rev || 1300000,
        text: '🛍️ Double 11 (2025)',
        showarrow: true,
        arrowhead: 2,
        arrowcolor: theme.amber,
        font: { size: 10, color: theme.amber, weight: 700 }
      }
    ];

    Plotly.react(elementId, [traceRev, traceProf], layout, { responsive: true, displayModeBar: false });
  }

  function renderCategoryRank(elementId, summaryData) {
    if (!checkPlotly(elementId) || !summaryData || !document.getElementById(elementId)) return;
    const theme = getThemeColors();

    const sorted = [...summaryData].sort((a, b) => a.revenue - b.revenue);
    const labels = sorted.map(d => `${d.category}<br><span style="font-size:10px">${d.name_en}</span>`);
    const revenues = sorted.map(d => d.revenue);
    const profits = sorted.map(d => d.profit);
    const margins = sorted.map(d => ((d.profit / d.revenue) * 100).toFixed(1) + '%');

    const traceRev = {
      y: labels,
      x: revenues,
      name: 'Revenue',
      type: 'bar',
      orientation: 'h',
      marker: { color: theme.teal, opacity: 0.9 },
      text: revenues.map(v => '¥' + (v / 1e6).toFixed(2) + 'M'),
      textposition: 'outside',
      cliponaxis: false,
      hovertemplate: '<b>%{y}</b><br>Revenue: ¥%{x:,.2f}<extra></extra>'
    };

    const traceProf = {
      y: labels,
      x: profits,
      name: 'Gross Profit',
      type: 'bar',
      orientation: 'h',
      marker: { color: theme.emerald, opacity: 0.9 },
      hovertemplate: '<b>%{y}</b><br>Profit: ¥%{x:,.2f}<extra></extra>'
    };

    const layout = getBaseLayout('', 'Amount (CNY)', '');
    layout.barmode = 'group';
    layout.margin.l = 140;
    layout.margin.r = 65;
    layout.legend = { orientation: 'h', y: 1.15, x: 0, font: { color: theme.textMuted } };

    Plotly.react(elementId, [traceRev, traceProf], layout, { responsive: true, displayModeBar: false });
  }

  function renderChannelDonut(elementId, slices) {
    if (!checkPlotly(elementId) || !slices || !document.getElementById(elementId)) return;
    const theme = getThemeColors();

    const channelRev = {};
    slices.forEach(s => {
      channelRev[s.Sales_Channel] = (channelRev[s.Sales_Channel] || 0) + s.realized_rev;
    });

    const labels = Object.keys(channelRev);
    const values = labels.map(l => channelRev[l]);
    const colors = [theme.teal, theme.emerald, theme.amber, theme.purple];

    const trace = {
      labels: labels,
      values: values,
      type: 'pie',
      hole: 0.58,
      marker: { colors: colors },
      textinfo: 'label+percent',
      textposition: 'outside',
      hovertemplate: '<b>%{label}</b><br>Revenue: ¥%{value:,.2f}<br>Share: %{percent}<extra></extra>'
    };

    const layout = getBaseLayout('');
    layout.showlegend = false;
    layout.margin = { l: 20, r: 20, t: 20, b: 20 };
    layout.annotations = [
      {
        text: 'Sales<br>Channels',
        showarrow: false,
        font: { size: 13, weight: 700, color: theme.text }
      }
    ];

    Plotly.react(elementId, [trace], layout, { responsive: true, displayModeBar: false });
  }

  // --- Distribution Tab (Charts 1, 2, 3, 4) ---

  // Chart 1: Revenue Histogram
  function renderRevenueHistogram(elementId, histData, viewMode = 'share') {
    if (!checkPlotly(elementId) || !histData || !document.getElementById(elementId)) return;
    const theme = getThemeColors();

    const yVals = viewMode === 'share' ? histData.shares : histData.counts;
    const yAxisTitle = viewMode === 'share' ? 'Share of Lines (%)' : 'Line Count';

    const trace = {
      x: histData.bin_centers,
      y: yVals,
      type: 'bar',
      marker: {
        color: theme.teal,
        opacity: 0.85,
        line: { color: theme.border, width: 0.5 }
      },
      hovertemplate:
        '<b>Revenue Range:</b> ~¥%{x:,.1f}<br>' +
        (viewMode === 'share' ? 'Share: %{y:.2f}%' : 'Lines: %{y:,}') +
        '<extra></extra>'
    };

    const layout = getBaseLayout(
      'Completed-Line Revenue Histogram (71 Log-Spaced Bins)',
      'Revenue (CNY, Log Scale)',
      yAxisTitle
    );
    layout.xaxis.type = 'log';
    layout.xaxis.tickvals = [5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000];
    layout.xaxis.ticktext = ['¥5', '¥10', '¥20', '¥50', '¥100', '¥200', '¥500', '¥1k', '¥2k', '¥5k'];

    // Reference lines for Median and Mean
    layout.shapes = [
      {
        type: 'line',
        x0: histData.median,
        x1: histData.median,
        y0: 0,
        y1: 1,
        yref: 'paper',
        line: { color: theme.amber, width: 2, dash: 'dash' }
      },
      {
        type: 'line',
        x0: histData.mean,
        x1: histData.mean,
        y0: 0,
        y1: 1,
        yref: 'paper',
        line: { color: theme.rose, width: 2, dash: 'dot' }
      }
    ];

    layout.annotations = [
      {
        x: Math.log10(histData.median),
        y: 1.05,
        xref: 'x',
        yref: 'paper',
        text: `Median: ¥${histData.median.toFixed(2)}`,
        showarrow: false,
        font: { size: 11, color: theme.amber, weight: 600 }
      },
      {
        x: Math.log10(histData.mean),
        y: 1.13,
        xref: 'x',
        yref: 'paper',
        text: `Mean: ¥${histData.mean.toFixed(2)}`,
        showarrow: false,
        font: { size: 11, color: theme.rose, weight: 600 }
      }
    ];

    Plotly.react(elementId, [trace], layout, { responsive: true, displayModeBar: false });
  }

  // Chart 2: Revenue KDE
  function renderRevenueKDE(elementId, kdeData, histData) {
    if (!checkPlotly(elementId) || !kdeData || !document.getElementById(elementId)) return;
    const theme = getThemeColors();

    const trace = {
      x: kdeData.grid_rev,
      y: kdeData.density,
      type: 'scatter',
      mode: 'lines',
      line: { color: theme.teal, width: 3, shape: 'spline' },
      fill: 'tozeroy',
      fillcolor: theme.isDark ? 'rgba(56, 189, 248, 0.18)' : 'rgba(14, 165, 233, 0.15)',
      hovertemplate: 'Revenue: ¥%{x:,.2f}<br>Density: %{y:.4f}<extra></extra>'
    };

    const layout = getBaseLayout('Completed-Line Revenue Density (KDE in Log Space)', 'Revenue (CNY, Log Scale)', 'Density');
    layout.xaxis.type = 'log';
    layout.xaxis.tickvals = [5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000];
    layout.xaxis.ticktext = ['¥5', '¥10', '¥20', '¥50', '¥100', '¥200', '¥500', '¥1k', '¥2k', '¥5k'];

    if (histData) {
      layout.shapes = [
        {
          type: 'line',
          x0: histData.median,
          x1: histData.median,
          y0: 0,
          y1: 1,
          yref: 'paper',
          line: { color: theme.amber, width: 2, dash: 'dash' }
        }
      ];
      layout.annotations = [
        {
          x: Math.log10(histData.median),
          y: 0.95,
          xref: 'x',
          yref: 'paper',
          text: `Median ¥${histData.median.toFixed(2)}`,
          showarrow: true,
          arrowcolor: theme.amber,
          font: { size: 11, color: theme.amber, weight: 600 }
        }
      ];
    }

    Plotly.react(elementId, [trace], layout, { responsive: true, displayModeBar: false });
  }

  // Chart 3: Category Box Plot
  function renderCategoryBoxPlot(elementId, boxData) {
    if (!checkPlotly(elementId) || !boxData || !document.getElementById(elementId)) return;
    const theme = getThemeColors();

    const traces = [];
    const categories = [...boxData.summary]; // already sorted descending by median

    categories.forEach((cat, idx) => {
      const details = boxData.details[cat.category];
      const vals = details ? details.sampled_vals : [cat.q1, cat.median, cat.q3];

      traces.push({
        x: vals,
        name: `${cat.category} · ${cat.name_en}`,
        type: 'box',
        orientation: 'h',
        marker: { color: theme.teal, size: 3, opacity: 0.5 },
        line: { width: 1.5 },
        boxpoints: 'outliers',
        boxmean: true
      });
    });

    const layout = getBaseLayout('Revenue by Product Category — Box Plot', 'Revenue (CNY, Log Scale)', '');
    layout.xaxis.type = 'log';
    layout.xaxis.tickvals = [5, 10, 25, 50, 100, 250, 500, 1000, 2500, 5000];
    layout.xaxis.ticktext = ['¥5', '¥10', '¥25', '¥50', '¥100', '¥250', '¥500', '¥1k', '¥2.5k', '¥5k'];
    layout.showlegend = false;
    layout.margin.l = 175;

    // Overall median reference
    layout.shapes = [
      {
        type: 'line',
        x0: 163.84,
        x1: 163.84,
        y0: 0,
        y1: 1,
        yref: 'paper',
        line: { color: theme.amber, width: 2, dash: 'dash' }
      }
    ];
    layout.annotations = [
      {
        x: Math.log10(163.84),
        y: 1.03,
        xref: 'x',
        yref: 'paper',
        text: 'Overall Median ¥163.84',
        showarrow: false,
        font: { size: 11, color: theme.amber, weight: 600 }
      }
    ];

    Plotly.react(elementId, traces, layout, { responsive: true, displayModeBar: false });
  }

  // Chart 4: Category Violin Plot
  function renderCategoryViolinPlot(elementId, violinData, boxSummary) {
    if (!checkPlotly(elementId) || !violinData || !document.getElementById(elementId)) return;
    const theme = getThemeColors();

    const traces = [];
    const summary = boxSummary || [];

    summary.forEach(cat => {
      const catData = violinData[cat.category];
      if (!catData) return;

      traces.push({
        type: 'violin',
        x: catData.grid_rev,
        y: Array(catData.grid_rev.length).fill(`${cat.category} · ${cat.name_en}`),
        orientation: 'h',
        side: 'positive',
        line: { color: theme.teal, width: 1.5 },
        fillcolor: theme.isDark ? 'rgba(56, 189, 248, 0.25)' : 'rgba(14, 165, 233, 0.25)',
        name: cat.category,
        meanline: { visible: true },
        points: false
      });
    });

    const layout = getBaseLayout('Revenue by Product Category — Violin Density Profiles', 'Revenue (CNY, Log Scale)', '');
    layout.xaxis.type = 'log';
    layout.xaxis.tickvals = [5, 10, 25, 50, 100, 250, 500, 1000, 2500, 5000];
    layout.xaxis.ticktext = ['¥5', '¥10', '¥25', '¥50', '¥100', '¥250', '¥500', '¥1k', '¥2.5k', '¥5k'];
    layout.showlegend = false;
    layout.margin.l = 175;

    Plotly.react(elementId, traces, layout, { responsive: true, displayModeBar: false });
  }

  // --- Relationships Tab (Charts 5, 6, 7) ---

  // Chart 5: Discount vs Profit Scatter Plot
  function renderDiscountScatter(elementId, discData) {
    if (!checkPlotly(elementId) || !discData || !document.getElementById(elementId)) return;
    const theme = getThemeColors();

    const pts = discData.sample_points;
    const xVals = pts.map(p => p.Discount_Percentage);
    const yVals = pts.map(p => p.Profit_CNY);
    const colors = pts.map(p => (p.Profit_CNY < 0 ? theme.rose : theme.teal));

    // Raw points trace
    const tracePoints = {
      x: xVals,
      y: yVals,
      mode: 'markers',
      type: 'scatter',
      marker: {
        size: 4,
        color: colors,
        opacity: 0.45
      },
      name: 'Order Lines',
      hovertemplate: 'Discount: %{x:.1f}%<br>Profit: ¥%{y:,.2f}<extra></extra>'
    };

    // Trendline trace (median in 5% bins)
    const trendX = discData.trend_bins.map(b => b.mid);
    const trendY = discData.trend_bins.map(b => b.median);
    const traceTrend = {
      x: trendX,
      y: trendY,
      mode: 'lines+markers',
      type: 'scatter',
      line: { color: theme.amber, width: 3 },
      marker: { size: 6, color: theme.amber },
      name: 'Binned Median Profit',
      hovertemplate: '<b>Discount Bin %{x}%</b><br>Median Profit: ¥%{y:,.2f}<extra></extra>'
    };

    const layout = getBaseLayout(
      'Discount Percentage vs Profit (Symlog Scale)',
      'Discount Percentage (%)',
      'Gross Profit (CNY)'
    );

    // Break-even line
    layout.shapes = [
      {
        type: 'line',
        x0: 0,
        x1: 65,
        y0: 0,
        y1: 0,
        line: { color: theme.rose, width: 1.5, dash: 'dash' }
      },
      {
        // 30% discount cliff zone shading
        type: 'rect',
        x0: 30,
        x1: 65,
        y0: -1000,
        y1: 0,
        fillcolor: theme.isDark ? 'rgba(251, 113, 133, 0.10)' : 'rgba(244, 63, 94, 0.08)',
        line: { width: 0 }
      }
    ];

    layout.annotations = [
      {
        x: 48,
        y: -150,
        text: '⚠️ Loss-Making Danger Zone (>30% Discount)',
        showarrow: false,
        font: { size: 11, color: theme.rose, weight: 700 }
      },
      {
        x: 60,
        y: 1800,
        text: `Pearson r: ${discData.overall_pearson}<br>Spearman ρ: ${discData.overall_spearman}`,
        showarrow: false,
        bgcolor: theme.paperBg,
        bordercolor: theme.border,
        borderwidth: 1,
        font: { size: 11, color: theme.text }
      }
    ];

    layout.legend = { orientation: 'h', y: 1.1, x: 0, font: { color: theme.textMuted } };

    Plotly.react(elementId, [tracePoints, traceTrend], layout, { responsive: true, displayModeBar: false });
  }

  // Chart 7: Unit Price vs Profit Bubbles
  function renderPriceProfitBubbles(elementId, bubbleData) {
    if (!checkPlotly(elementId) || !bubbleData || !document.getElementById(elementId)) return;
    const theme = getThemeColors();

    const pts = bubbleData.sample_bubbles;
    const xVals = pts.map(p => p.Unit_Price_CNY);
    const yVals = pts.map(p => p.Profit_CNY);
    const quantities = pts.map(p => p.Quantity);
    const sizes = quantities.map(q => q * 3.5 + 4); // bubble area proportional to units

    const traceBubbles = {
      x: xVals,
      y: yVals,
      mode: 'markers',
      type: 'scatter',
      marker: {
        size: sizes,
        color: yVals.map(y => (y < 0 ? theme.rose : theme.teal)),
        opacity: 0.5,
        line: { color: theme.border, width: 0.5 }
      },
      name: 'Order Lines (Bubble = Quantity)',
      text: quantities.map(q => `${q} unit(s)`),
      hovertemplate:
        'Unit Price: ¥%{x:,.2f}<br>' +
        'Profit: ¥%{y:,.2f}<br>' +
        'Quantity: %{text}<extra></extra>'
    };

    // Trend line
    const trendX = bubbleData.trend.map(t => t.x);
    const trendY = bubbleData.trend.map(t => t.median);
    const traceTrend = {
      x: trendX,
      y: trendY,
      mode: 'lines+markers',
      type: 'scatter',
      line: { color: theme.amber, width: 3 },
      marker: { size: 6, color: theme.amber },
      name: 'Decile Median Profit',
      hovertemplate: 'Price Decile ~¥%{x:,.1f}<br>Median Profit: ¥%{y:,.2f}<extra></extra>'
    };

    const layout = getBaseLayout(
      'Unit Price vs Profit (Bubble Size = Quantity 1–5)',
      'Unit Price (CNY, Log Scale)',
      'Gross Profit (CNY)'
    );
    layout.xaxis.type = 'log';
    layout.xaxis.tickvals = [10, 30, 100, 300, 1000];
    layout.xaxis.ticktext = ['¥10', '¥30', '¥100', '¥300', '¥1,000'];

    // Zero-profit line
    layout.shapes = [
      {
        type: 'line',
        x0: 5,
        x1: 2000,
        y0: 0,
        y1: 0,
        line: { color: theme.rose, width: 1.5, dash: 'dash' }
      }
    ];

    layout.annotations = [
      {
        x: Math.log10(15),
        y: 2000,
        text: `Spearman ρ: +${bubbleData.spearman} (Strong Price Multiplier)`,
        showarrow: false,
        bgcolor: theme.paperBg,
        bordercolor: theme.border,
        borderwidth: 1,
        font: { size: 11, color: theme.text }
      }
    ];

    layout.legend = { orientation: 'h', y: 1.1, x: 0, font: { color: theme.textMuted } };

    Plotly.react(elementId, [traceBubbles, traceTrend], layout, { responsive: true, displayModeBar: false });
  }

  // Chart 6: Pair Plot Matrix
  function renderPairPlotMatrix(elementId, pairData) {
    if (!checkPlotly(elementId) || !pairData || !document.getElementById(elementId)) return;
    const theme = getThemeColors();

    const vars = pairData.variables; // [Unit_Price, Quantity, Revenue, Profit]
    const corr = pairData.correlations;

    // We build a heatmap/correlation matrix with Spearman values
    const labels = ['Unit Price', 'Quantity', 'Revenue', 'Profit'];
    const z = [
      [1.0, corr.Unit_Price_CNY.Quantity, corr.Unit_Price_CNY.Revenue_CNY, corr.Unit_Price_CNY.Profit_CNY],
      [corr.Unit_Price_CNY.Quantity, 1.0, corr.Quantity.Revenue_CNY, corr.Quantity.Profit_CNY],
      [corr.Unit_Price_CNY.Revenue_CNY, corr.Quantity.Revenue_CNY, 1.0, corr.Revenue_CNY.Profit_CNY],
      [corr.Unit_Price_CNY.Profit_CNY, corr.Quantity.Profit_CNY, corr.Revenue_CNY.Profit_CNY, 1.0]
    ];

    const textValues = z.map(row => row.map(v => (v >= 0 ? '+' : '') + v.toFixed(3)));

    const trace = {
      z: z,
      x: labels,
      y: labels,
      type: 'heatmap',
      colorscale: [
        [0.0, theme.rose],
        [0.3, theme.paperBg],
        [1.0, theme.teal]
      ],
      zmin: -0.5,
      zmax: 1.0,
      text: textValues,
      texttemplate: '<b>%{text}</b>',
      textfont: { size: 13, color: theme.text },
      hoverongaps: false,
      hovertemplate: '<b>%{y}</b> × <b>%{x}</b><br>Spearman ρ: %{z:.3f}<extra></extra>'
    };

    const layout = getBaseLayout('Pairwise Spearman Correlation Matrix', '', '');
    layout.margin = { l: 90, r: 40, t: 40, b: 60 };

    Plotly.react(elementId, [trace], layout, { responsive: true, displayModeBar: false });
  }

  // --- Composition Tab (Charts 8, 9) ---

  // Chart 8: Category → Subcategory Treemap
  function renderCategoryTreemap(elementId, treemapNodes) {
    if (!checkPlotly(elementId) || !treemapNodes || !document.getElementById(elementId)) return;
    const theme = getThemeColors();

    const ids = treemapNodes.map(n => n.id);
    const labels = treemapNodes.map(n => n.label);
    const parents = treemapNodes.map(n => n.parent);
    const values = treemapNodes.map(n => n.value);

    const trace = {
      type: 'treemap',
      ids: ids,
      labels: labels,
      parents: parents,
      values: values,
      branchvalues: 'total',
      hoverinfo: 'label+value+percent parent+percent root',
      hovertemplate:
        '<b>%{label}</b><br>' +
        'Revenue: ¥%{value:,.2f}<br>' +
        'Share of Parent: %{percentParent:.2%}<br>' +
        'Share of Total: %{percentRoot:.2%}<extra></extra>',
      textinfo: 'label+value+percent parent',
      marker: {
        colorscale: theme.heatScale
      }
    };

    const layout = getBaseLayout('Category → Subcategory Revenue Treemap (Hierarchical)', '', '');
    layout.margin = { l: 15, r: 15, t: 35, b: 15 };

    Plotly.react(elementId, [trace], layout, { responsive: true, displayModeBar: false });
  }

  // Chart 9: Category × Month Revenue Heatmap
  function renderCategoryMonthHeatmap(elementId, heatmapData) {
    if (!checkPlotly(elementId) || !heatmapData || !document.getElementById(elementId)) return;
    const theme = getThemeColors();

    // Format annotations for grid cells
    const annotations = [];
    const categories = heatmapData.categories;
    const categoriesEn = heatmapData.categories_en;
    const months = heatmapData.months;
    const z = heatmapData.z;

    for (let r = 0; r < categories.length; r++) {
      for (let c = 0; c < months.length; c++) {
        const val = z[r][c];
        const formatted = val >= 1e6 ? `¥${(val / 1e6).toFixed(2)}M` : `¥${(val / 1e3).toFixed(0)}K`;
        annotations.push({
          x: months[c],
          y: categoriesEn[r],
          text: formatted,
          font: {
            color: val > 6e5 ? '#FFFFFF' : theme.text,
            size: 10,
            weight: val > 6e5 ? 700 : 500
          },
          showarrow: false
        });
      }
    }

    const trace = {
      z: z,
      x: months,
      y: categoriesEn,
      type: 'heatmap',
      colorscale: theme.heatScale,
      hoverongaps: false,
      hovertemplate: '<b>%{y}</b><br>Month: %{x}<br>Combined Revenue: ¥%{z:,.2f}<extra></extra>'
    };

    const layout = getBaseLayout('Category × Month Revenue Heatmap (2024 + 2025 Combined)', 'Month', '');
    layout.margin.l = 210;
    layout.margin.r = 30;
    layout.margin.b = 50;
    layout.annotations = annotations;

    // Highlight campaigns on June and November
    layout.shapes = [
      {
        type: 'rect',
        xref: 'x',
        yref: 'paper',
        x0: 'May',
        x1: 'Jul',
        y0: 0,
        y1: 1,
        line: { color: theme.amber, width: 2, dash: 'dot' }
      },
      {
        type: 'rect',
        xref: 'x',
        yref: 'paper',
        x0: 'Oct',
        x1: 'Dec',
        y0: 0,
        y1: 1,
        line: { color: theme.amber, width: 2, dash: 'dot' }
      }
    ];

    Plotly.react(elementId, [trace], layout, { responsive: true, displayModeBar: false });
  }

  return {
    renderMonthlyTrend,
    renderCategoryRank,
    renderChannelDonut,
    renderRevenueHistogram,
    renderRevenueKDE,
    renderCategoryBoxPlot,
    renderCategoryViolinPlot,
    renderDiscountScatter,
    renderPriceProfitBubbles,
    renderPairPlotMatrix,
    renderCategoryTreemap,
    renderCategoryMonthHeatmap
  };
})();
