/**
 * HuaGou Mall E-Commerce Analytics Dashboard - Application Controller
 * Handles filtering, KPI reactivity, theme toggle, and tab routing
 */

document.addEventListener('DOMContentLoaded', function () {
  const data = window.HUAGOU_DATA;
  if (!data) {
    console.error('Dataset not loaded! Check data.js');
    return;
  }

  // State
  const state = {
    theme: localStorage.getItem('huagou_theme') || 'light',
    activeTab: 'overview',
    histView: 'share',
    filters: {
      year: 'all',
      status: 'Completed', // default realized population
      category: 'all',
      channel: 'all',
      segment: 'all'
    }
  };

  // DOM Elements
  const themeToggleBtn = document.getElementById('themeToggleBtn');
  const themeIcon = document.getElementById('themeIcon');
  const themeLabel = document.getElementById('themeLabel');
  const filterForm = document.getElementById('filterForm');
  const resetFiltersBtn = document.getElementById('resetFiltersBtn');
  const filterYear = document.getElementById('filterYear');
  const filterStatus = document.getElementById('filterStatus');
  const filterCategory = document.getElementById('filterCategory');
  const filterChannel = document.getElementById('filterChannel');
  const filterSegment = document.getElementById('filterSegment');
  const filterCountBadge = document.getElementById('filterCountBadge');

  // KPI elements
  const kpiRevenue = document.getElementById('kpiRevenue');
  const kpiRevenueSub = document.getElementById('kpiRevenueSub');
  const kpiProfit = document.getElementById('kpiProfit');
  const kpiProfitSub = document.getElementById('kpiProfitSub');
  const kpiOrders = document.getElementById('kpiOrders');
  const kpiOrdersSub = document.getElementById('kpiOrdersSub');
  const kpiAOV = document.getElementById('kpiAOV');
  const kpiAOVSub = document.getElementById('kpiAOVSub');
  const kpiLoss = document.getElementById('kpiLoss');
  const kpiLossSub = document.getElementById('kpiLossSub');
  const kpiCSAT = document.getElementById('kpiCSAT');

  // Populate Filter Select Options
  function initFilterDropdowns() {
    // Categories
    data.categories.forEach(cat => {
      const opt = document.createElement('option');
      opt.value = cat;
      opt.textContent = `${cat} (${data.category_labels[cat] || cat})`;
      filterCategory.appendChild(opt);
    });

    // Channels
    data.channels.forEach(ch => {
      const opt = document.createElement('option');
      opt.value = ch;
      opt.textContent = ch;
      filterChannel.appendChild(opt);
    });

    // Segments
    data.segments.forEach(seg => {
      const opt = document.createElement('option');
      opt.value = seg;
      opt.textContent = seg + ' Customer';
      filterSegment.appendChild(opt);
    });
  }

  // Theme Management
  function applyTheme(theme) {
    state.theme = theme;
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('huagou_theme', theme);

    if (theme === 'dark') {
      themeIcon.textContent = '☀️';
      themeLabel.textContent = 'Light Mode';
    } else {
      themeIcon.textContent = '🌙';
      themeLabel.textContent = 'Dark Mode';
    }

    // Re-render visible charts for theme synchronization
    renderActiveTabCharts();
  }

  themeToggleBtn.addEventListener('click', () => {
    const nextTheme = state.theme === 'dark' ? 'light' : 'dark';
    applyTheme(nextTheme);
  });

  // Tab Navigation
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabPanels = document.querySelectorAll('.tab-content');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetTab = btn.getAttribute('data-tab');
      state.activeTab = targetTab;

      tabBtns.forEach(b => b.classList.remove('active'));
      tabPanels.forEach(p => p.classList.remove('active'));

      btn.classList.add('active');
      const panel = document.getElementById(`tab-${targetTab}`);
      if (panel) panel.classList.add('active');

      // Trigger Plotly chart rendering
      setTimeout(() => {
        renderActiveTabCharts();
      }, 50);
    });
  });

  // Recalculate KPIs based on filtered slice cubes
  function updateKPIs() {
    let rev = 0;
    let prof = 0;
    let orders = 0;
    let lines = 0;
    let posLines = 0;
    let lossLines = 0;
    let ratingsSum = 0;
    let ratingsCount = 0;

    const isCompletedOnly = state.filters.status === 'Completed';

    data.slices.forEach(row => {
      // Filter conditions
      if (state.filters.year !== 'all' && row.Year !== parseInt(state.filters.year)) return;
      if (state.filters.status !== 'all' && row.Order_Status !== state.filters.status) return;
      if (state.filters.category !== 'all' && row.Category !== state.filters.category) return;
      if (state.filters.channel !== 'all' && row.Sales_Channel !== state.filters.channel) return;
      if (state.filters.segment !== 'all' && row.Customer_Segment !== state.filters.segment) return;

      if (isCompletedOnly) {
        rev += row.realized_rev;
        prof += row.realized_prof;
        lines += row.realized_lines;
      } else {
        rev += row.total_rev;
        prof += row.total_prof;
        lines += row.total_lines;
      }

      orders += row.distinct_orders;
      posLines += row.positive_rev_lines;
      lossLines += row.loss_lines;

      if (row.avg_rating) {
        ratingsSum += row.avg_rating * row.total_lines;
        ratingsCount += row.total_lines;
      }
    });

    const marginPct = rev > 0 ? (prof / rev) * 100 : 0;
    const aov = orders > 0 ? rev / orders : 0;
    const lossPct = posLines > 0 ? (lossLines / posLines) * 100 : 0;
    const avgRating = ratingsCount > 0 ? (ratingsSum / ratingsCount).toFixed(2) : '4.02';

    // Update KPI UI
    kpiRevenue.textContent = `¥${(rev / 1e6).toFixed(2)}M`;
    kpiRevenueSub.textContent = isCompletedOnly ? 'Realized completed sales' : 'Gross (all order statuses)';

    kpiProfit.textContent = `¥${(prof / 1e6).toFixed(2)}M`;
    kpiProfitSub.innerHTML = `<span class="badge ${marginPct >= 20 ? 'badge-emerald' : 'badge-amber'}">${marginPct.toFixed(2)}% margin</span>`;

    kpiOrders.textContent = orders.toLocaleString();
    kpiOrdersSub.textContent = `${lines.toLocaleString()} lines (~${(lines / Math.max(orders, 1)).toFixed(2)} / order)`;

    kpiAOV.textContent = `¥${aov.toFixed(2)}`;
    kpiAOVSub.textContent = 'Revenue / order';

    kpiLoss.textContent = `${lossPct.toFixed(2)}%`;
    kpiLossSub.innerHTML = `<span class="badge ${lossPct > 10 ? 'badge-rose' : 'badge-amber'}">${lossLines.toLocaleString()} loss lines</span>`;

    kpiCSAT.textContent = `★ ${avgRating} / 5.0`;

    // Filter count badge
    let activeFilterCount = 0;
    if (state.filters.year !== 'all') activeFilterCount++;
    if (state.filters.status !== 'Completed') activeFilterCount++;
    if (state.filters.category !== 'all') activeFilterCount++;
    if (state.filters.channel !== 'all') activeFilterCount++;
    if (state.filters.segment !== 'all') activeFilterCount++;

    filterCountBadge.textContent = activeFilterCount > 0 ? `${activeFilterCount} active filters` : 'Default: Realized Completed';
  }

  // Filter Listeners
  filterYear.addEventListener('change', e => {
    state.filters.year = e.target.value;
    updateKPIs();
    renderActiveTabCharts();
  });

  filterStatus.addEventListener('change', e => {
    state.filters.status = e.target.value;
    updateKPIs();
    renderActiveTabCharts();
  });

  filterCategory.addEventListener('change', e => {
    state.filters.category = e.target.value;
    updateKPIs();
    renderActiveTabCharts();
  });

  filterChannel.addEventListener('change', e => {
    state.filters.channel = e.target.value;
    updateKPIs();
    renderActiveTabCharts();
  });

  filterSegment.addEventListener('change', e => {
    state.filters.segment = e.target.value;
    updateKPIs();
    renderActiveTabCharts();
  });

  resetFiltersBtn.addEventListener('click', () => {
    state.filters = {
      year: 'all',
      status: 'Completed',
      category: 'all',
      channel: 'all',
      segment: 'all'
    };
    filterYear.value = 'all';
    filterStatus.value = 'Completed';
    filterCategory.value = 'all';
    filterChannel.value = 'all';
    filterSegment.value = 'all';
    updateKPIs();
    renderActiveTabCharts();
  });

  // Histogram view mode toggle (Share % vs Count)
  const histModeBtns = document.querySelectorAll('.hist-mode-btn');
  histModeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      histModeBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      state.histView = btn.getAttribute('data-mode');
      HuagouCharts.renderRevenueHistogram('chart1_hist', data.chart1_histogram, state.histView);
    });
  });

  // Render Charts based on active tab
  function renderActiveTabCharts() {
    switch (state.activeTab) {
      case 'overview':
        HuagouCharts.renderMonthlyTrend('chart_monthly_trend', data.monthly_trend);
        HuagouCharts.renderCategoryRank('chart_category_rank', data.chart3_box.summary);
        HuagouCharts.renderChannelDonut('chart_channel_donut', data.slices);
        break;

      case 'distribution':
        HuagouCharts.renderRevenueHistogram('chart1_hist', data.chart1_histogram, state.histView);
        HuagouCharts.renderRevenueKDE('chart2_kde', data.chart2_kde, data.chart1_histogram);
        HuagouCharts.renderCategoryBoxPlot('chart3_box', data.chart3_box);
        HuagouCharts.renderCategoryViolinPlot('chart4_violin', data.chart4_violin, data.chart3_box.summary);
        break;

      case 'relationships':
        HuagouCharts.renderDiscountScatter('chart5_scatter', data.chart5_discount_profit);
        HuagouCharts.renderPriceProfitBubbles('chart7_bubbles', data.chart7_bubbles);
        HuagouCharts.renderPairPlotMatrix('chart6_pairplot', data.chart6_pairplot);
        break;

      case 'composition':
        HuagouCharts.renderCategoryTreemap('chart8_treemap', data.chart8_treemap);
        HuagouCharts.renderCategoryMonthHeatmap('chart9_heatmap', data.chart9_heatmap);
        break;

      case 'insights':
        // Static cards and markdown table
        break;
    }
  }

  // Initialize
  initFilterDropdowns();
  applyTheme(state.theme);
  updateKPIs();
  renderActiveTabCharts();
});
