/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/* Revenue Attribution dashboard.
 * Consumes the server payload (all models precomputed) so model flips are
 * instant client-side; date-range changes refetch. Bars + Sankey are custom
 * SVG/CSS (for the FLIP re-order and ribbon flow); the time-series is Chart.js
 * themed to the same validated channel palette. Theme-aware via the admin
 * `admin-theme-changed` event. */
(function () {
  'use strict';
  const root = document.querySelector('.attr-dash');
  if (!root) return;
  const payloadEl = document.getElementById('attr-payload');
  if (!payloadEl) return;

  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  const CH_NAMES = {
    email: 'Email',
    organic_search: 'Organic Search',
    paid_search: 'Paid Search',
    organic_social: 'Organic Social',
    paid_social: 'Paid Social',
    affiliate: 'Affiliate',
    referral: 'Refer a Friend',
    referral_external: 'External Link',
    campaign: 'Campaign',
    loyalty: 'Loyalty',
    direct: 'Direct',
    unknown: 'Unknown',
  };
  const chName = id => CH_NAMES[id] || id;
  const cssVar = id =>
    getComputedStyle(root)
      .getPropertyValue('--ch-' + id)
      .trim() || '#9aa0a6';

  let payload = JSON.parse(payloadEl.textContent);
  let model = payload.active_model;
  let lens = 'attributed';
  let allChannels = [];
  let tsChart = null;

  // ---- formatting ----
  const cur = () => payload.currency || 'USD';
  function money(n) {
    try {
      return new Intl.NumberFormat(undefined, {
        style: 'currency',
        currency: cur(),
        maximumFractionDigits: 0,
      }).format(n || 0);
    } catch (e) {
      return Math.round(n || 0).toLocaleString();
    }
  }
  function moneyK(n) {
    if (Math.abs(n) >= 1000) {
      const v = n / 1000;
      return money(0).replace(/[\d.,]+/, '') + (v >= 100 ? v.toFixed(0) : v.toFixed(1)) + 'k';
    }
    return money(n);
  }

  function channelsFor(m) {
    const map = {};
    (payload.by_model[m] ? payload.by_model[m].channels : []).forEach(c => {
      map[c.channel] = c;
    });
    return map;
  }

  function computeAllChannels() {
    const set = new Set();
    Object.values(payload.by_model).forEach(mb => mb.channels.forEach(c => set.add(c.channel)));
    // stable order: by max revenue across models, then name
    allChannels = [...set].sort((a, b) => {
      const ra = maxRev(a),
        rb = maxRev(b);
      return rb - ra || chName(a).localeCompare(chName(b));
    });
  }
  function maxRev(ch) {
    let m = 0;
    Object.values(payload.by_model).forEach(mb =>
      mb.channels.forEach(c => {
        if (c.channel === ch && c.revenue > m) m = c.revenue;
      })
    );
    return m;
  }

  // ---- count-up tween ----
  function tween(el, to, fmt) {
    if (reduce) {
      el.textContent = fmt(to);
      el.dataset.v = to;
      return;
    }
    const from = parseFloat(el.dataset.v || '0');
    const t0 = performance.now();
    function step(t) {
      const k = Math.min(1, (t - t0) / 600);
      const e = 1 - Math.pow(1 - k, 3);
      el.textContent = fmt(from + (to - from) * e);
      if (k < 1) requestAnimationFrame(step);
      else {
        el.textContent = fmt(to);
        el.dataset.v = to;
      }
    }
    el.dataset.v = to;
    requestAnimationFrame(step);
  }

  // ---- model switcher ----
  const MODEL_DESC = {
    last_non_direct: 'Credit the last non-direct touch',
    first_touch: 'Credit the discovery',
    linear: 'Split evenly',
    time_decay: 'Recent touches win',
    position_based: 'First & last favoured',
  };
  const MODEL_NAME = {
    last_non_direct: 'Last touch',
    first_touch: 'First touch',
    linear: 'Linear',
    time_decay: 'Time decay',
    position_based: 'Position 40/20/40',
  };
  function selectModel(m, focus) {
    model = m;
    const wrap = document.getElementById('attr-models');
    [...wrap.children].forEach((c, i) => {
      const on = payload.models[i] === model;
      c.setAttribute('aria-checked', String(on));
      c.tabIndex = on ? 0 : -1; // roving tabindex for the radiogroup
      if (on && focus) c.focus();
    });
    renderModel();
  }
  function buildModels() {
    const wrap = document.getElementById('attr-models');
    wrap.innerHTML = '';
    payload.models.forEach(m => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'attr-model';
      b.setAttribute('role', 'radio');
      b.setAttribute('aria-checked', String(m === model));
      b.tabIndex = m === model ? 0 : -1;
      b.innerHTML =
        '<div class="m-name">' +
        (MODEL_NAME[m] || m) +
        '</div><div class="m-desc">' +
        (MODEL_DESC[m] || '') +
        '</div>';
      b.addEventListener('click', () => selectModel(m, false));
      wrap.appendChild(b);
    });
    // Arrow-key navigation, per the radiogroup pattern.
    wrap.addEventListener('keydown', e => {
      const keys = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 };
      if (!(e.key in keys)) return;
      e.preventDefault();
      const i = payload.models.indexOf(model);
      const next = (i + keys[e.key] + payload.models.length) % payload.models.length;
      selectModel(payload.models[next], true);
    });
  }

  // ---- KPIs ----
  function renderKpis() {
    tween(document.getElementById('kpi-total'), payload.totals.attributed, money);
    tween(document.getElementById('kpi-orders'), payload.totals.orders, v =>
      Math.round(v).toLocaleString()
    );
    const at = payload.totals.avg_touches;
    document.getElementById('kpi-touches').textContent = at == null ? '—' : Number(at).toFixed(1);
    const recon = document.getElementById('kpi-recon');
    recon.innerHTML = payload.reconciles
      ? '<svg viewBox="0 0 20 20" fill="none"><path d="M4 10.5l4 4 8-9" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>Reconciles to net revenue'
      : '';
    const chans = channelsFor(model);
    const top = Object.values(chans).sort((a, b) => b.revenue - a.revenue)[0];
    if (top) {
      document.getElementById('kpi-top-name').textContent = chName(top.channel);
      document.getElementById('kpi-top-val').textContent =
        Number(top.share).toFixed(1) + '% · ' + moneyK(top.revenue);
      document.getElementById('kpi-top-sw').className = 'sw ch-' + top.channel;
    }
  }

  // ---- channel bars (FLIP re-order) ----
  let barsBuilt = false;
  function renderBars() {
    const wrap = document.getElementById('attr-bars');
    const chans = channelsFor(model);
    const max = Math.max(1, ...allChannels.map(c => (chans[c] ? chans[c].revenue : 0)));
    if (!barsBuilt) {
      allChannels.forEach(c => {
        const row = document.createElement('div');
        row.className = 'bar-row';
        row.dataset.id = c;
        row.innerHTML =
          '<div class="bar-name"><span class="sw ch-' +
          c +
          '"></span>' +
          chName(c) +
          '</div><div class="bar-track"><div class="bar-fill ch-' +
          c +
          '"></div></div><div class="bar-val"><span class="v">—</span><span class="pct"></span></div>';
        wrap.appendChild(row);
      });
      barsBuilt = true;
    }
    const rows = [...wrap.children];
    const first = {};
    rows.forEach(r => (first[r.dataset.id] = r.getBoundingClientRect().top));
    const order = allChannels
      .slice()
      .sort((a, b) => (chans[b] ? chans[b].revenue : 0) - (chans[a] ? chans[a].revenue : 0));
    order.forEach(id => wrap.appendChild(rows.find(r => r.dataset.id === id)));
    if (!reduce) {
      const last = {};
      rows.forEach(r => (last[r.dataset.id] = r.getBoundingClientRect().top));
      rows.forEach(r => {
        const dy = first[r.dataset.id] - last[r.dataset.id];
        if (dy) {
          r.style.transition = 'none';
          r.style.transform = 'translateY(' + dy + 'px)';
        }
      });
      wrap.offsetHeight;
      requestAnimationFrame(() =>
        rows.forEach(r => {
          r.style.transition = 'transform .7s cubic-bezier(.34,1.05,.5,1)';
          r.style.transform = '';
        })
      );
    }
    rows.forEach(r => {
      const c = chans[r.dataset.id];
      const val = c ? c.revenue : 0;
      r.querySelector('.bar-fill').style.width = (val / max) * 100 + '%';
      tween(r.querySelector('.v'), val, money);
      r.querySelector('.pct').textContent = c ? Number(c.share).toFixed(1) + '%' : '0%';
    });
  }

  // ---- time series (Chart.js) ----
  function buildChart() {
    const canvas = document.getElementById('attr-timeseries');
    const ctx = canvas.getContext('2d');
    tsChart = new Chart(ctx, {
      type: 'bar',
      data: { labels: [], datasets: [] },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: reduce ? false : { duration: 500 },
        interaction: { mode: 'index', intersect: false },
        scales: {
          x: { stacked: true, grid: { display: false }, ticks: { maxRotation: 0, autoSkip: true } },
          y: { stacked: true, beginAtZero: true, grid: {}, ticks: {} },
        },
        plugins: { legend: { display: true, position: 'bottom' }, tooltip: {} },
      },
    });
    themeChart();
  }
  function renderChart() {
    if (!tsChart) return;
    const ts = payload.by_model[model] ? payload.by_model[model].timeseries : [];
    const dates = [...new Set(ts.map(r => r.date))].sort();
    const byCh = {};
    ts.forEach(r => {
      (byCh[r.channel] = byCh[r.channel] || {})[r.date] = r.revenue;
    });
    const chans = allChannels.filter(c => byCh[c]);
    tsChart.data.labels = dates.map(d => d.slice(5));
    tsChart.data.datasets = chans.map(c => ({
      label: chName(c),
      data: dates.map(d => byCh[c][d] || 0),
      backgroundColor: cssVar(c),
      borderColor: 'transparent',
      borderWidth: 0,
      borderRadius: 3,
      borderSkipped: false,
      categoryPercentage: 0.7,
      barPercentage: 0.9,
    }));
    tsChart.update();
  }
  function themeChart() {
    if (!tsChart) return;
    const ink = getComputedStyle(root).getPropertyValue('--ink-2').trim();
    const grid = getComputedStyle(root).getPropertyValue('--hair').trim();
    tsChart.options.scales.x.ticks.color = ink;
    tsChart.options.scales.y.ticks.color = ink;
    tsChart.options.scales.y.grid.color = grid;
    tsChart.options.plugins.legend.labels = {
      color: ink,
      boxWidth: 10,
      boxHeight: 10,
      usePointStyle: true,
    };
    tsChart.update('none');
  }

  // ---- sankey ----
  function renderSankey() {
    const el = document.getElementById('attr-sankey');
    const flows = payload.journeys || [];
    if (!flows.length) {
      el.innerHTML = '';
      return;
    }
    const W = 720,
      H = 260,
      padY = 24,
      colW = 118,
      gap = 6;
    const leftT = {},
      rightT = {};
    flows.forEach(f => {
      leftT[f.from] = (leftT[f.from] || 0) + f.revenue;
      rightT[f.to] = (rightT[f.to] || 0) + f.revenue;
    });
    const order = t => Object.keys(t).sort((a, b) => t[b] - t[a]);
    const leftIds = order(leftT),
      rightIds = order(rightT);
    const totL = Object.values(leftT).reduce((a, b) => a + b, 0) || 1;
    const scale = (H - padY * 2 - (Math.max(leftIds.length, rightIds.length) - 1) * gap) / totL;
    function layout(ids, t) {
      let y = padY;
      const pos = {};
      ids.forEach(id => {
        const h = Math.max(6, t[id] * scale);
        pos[id] = { y, h };
        y += h + gap;
      });
      return pos;
    }
    const L = layout(leftIds, leftT),
      R = layout(rightIds, rightT);
    const inf = lens === 'influenced';
    const infMap = {};
    (payload.influenced || []).forEach(r => (infMap[r.channel] = r.influenced_revenue));
    let svg = '<text class="sk-col-label" x="8" y="14">First touch</text>';
    svg +=
      '<text class="sk-col-label" x="' + (W - 8) + '" y="14" text-anchor="end">Converts on</text>';
    const cL = {},
      cR = {};
    leftIds.forEach(id => (cL[id] = L[id].y));
    rightIds.forEach(id => (cR[id] = R[id].y));
    flows
      .slice()
      .sort((a, b) => b.revenue - a.revenue)
      .forEach(f => {
        const h = f.revenue * scale,
          x0 = colW,
          x1 = W - colW;
        const sL = cL[f.from];
        cL[f.from] += h;
        const sR = cR[f.to];
        cR[f.to] += h;
        const mx = (x0 + x1) / 2;
        const c = cssVar(f.from);
        svg +=
          '<path class="sk-ribbon" d="M' +
          x0 +
          ',' +
          sL +
          ' C' +
          mx +
          ',' +
          sL +
          ' ' +
          mx +
          ',' +
          sR +
          ' ' +
          x1 +
          ',' +
          sR +
          ' L' +
          x1 +
          ',' +
          (sR + h) +
          ' C' +
          mx +
          ',' +
          (sR + h) +
          ' ' +
          mx +
          ',' +
          (sL + h) +
          ' ' +
          x0 +
          ',' +
          (sL + h) +
          ' Z" fill="' +
          c +
          '" opacity="' +
          (inf ? 0.16 : 0.42) +
          '"/>';
      });
    leftIds.forEach(id => {
      const n = L[id];
      svg +=
        '<rect x="' +
        (colW - 9) +
        '" y="' +
        n.y +
        '" width="9" height="' +
        n.h +
        '" fill="' +
        cssVar(id) +
        '"/>';
      svg +=
        '<text class="sk-label" x="' +
        (colW - 16) +
        '" y="' +
        (n.y + n.h / 2 + 3.5) +
        '" text-anchor="end">' +
        chName(id) +
        '</text>';
    });
    rightIds.forEach(id => {
      const n = R[id];
      const val = inf && infMap[id] != null ? infMap[id] : rightT[id];
      svg +=
        '<rect x="' +
        (W - colW) +
        '" y="' +
        n.y +
        '" width="9" height="' +
        n.h +
        '" fill="' +
        cssVar(id) +
        '"/>';
      svg +=
        '<text class="sk-label" x="' +
        (W - colW + 16) +
        '" y="' +
        (n.y + n.h / 2 - 1) +
        '">' +
        chName(id) +
        '</text>';
      svg +=
        '<text class="sk-val" x="' +
        (W - colW + 16) +
        '" y="' +
        (n.y + n.h / 2 + 12) +
        '">' +
        moneyK(val) +
        '</text>';
    });
    el.innerHTML = svg;
  }

  // ---- campaigns ----
  function renderCampaigns() {
    const body = document.getElementById('attr-campaigns');
    const card = document.getElementById('attr-campaigns-card');
    const camps = payload.campaigns || [];
    if (!camps.length) {
      card.style.display = 'none';
      return;
    }
    card.style.display = '';
    body.innerHTML = camps
      .map(c => {
        const aov = c.orders ? c.revenue / c.orders : 0;
        return (
          '<tr><td><span class="camp"><span class="sw ch-campaign"></span>' +
          escapeHtml(c.name || c.slug) +
          '</span></td><td class="num">' +
          money(c.revenue) +
          '</td><td class="num">' +
          c.orders +
          '</td><td class="num">' +
          money(aov) +
          '</td></tr>'
        );
      })
      .join('');
  }
  function escapeHtml(s) {
    return String(s).replace(
      /[&<>"]/g,
      c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]
    );
  }

  // ---- lens toggle ----
  document.querySelectorAll('[data-lens]').forEach(b =>
    b.addEventListener('click', () => {
      lens = b.dataset.lens;
      document
        .querySelectorAll('[data-lens]')
        .forEach(x => x.setAttribute('aria-pressed', String(x === b)));
      document.getElementById('attr-lens-note').textContent =
        lens === 'influenced'
          ? 'Influenced: every channel that touched an order, credited its full value — the reach last-click hides (totals exceed 100% by design).'
          : 'First touch on the left, the order on the right.';
      renderSankey();
    })
  );

  // ---- date range ----
  // Full reload so the server renders the correct state (dashboard vs empty)
  // and re-embeds a fresh payload. Model flips stay instant (client-side).
  const rangeSel = document.getElementById('attr-range');
  if (rangeSel) {
    rangeSel.addEventListener('change', () => {
      window.location.search = '?period=' + encodeURIComponent(rangeSel.value);
    });
  }

  // ---- CSV export (current model + period) ----
  const exportBtn = document.getElementById('attr-export');
  if (exportBtn) {
    exportBtn.addEventListener('click', e => {
      e.preventDefault();
      const p = rangeSel ? rangeSel.value : '';
      window.location.href =
        exportBtn.dataset.url +
        '?period=' +
        encodeURIComponent(p) +
        '&model=' +
        encodeURIComponent(model);
    });
  }

  const hasBody = !!document.getElementById('attr-models');

  // ---- theme ----
  document.addEventListener('admin-theme-changed', e => {
    const t = (e.detail && e.detail.theme) || root.dataset.theme;
    if (t) root.dataset.theme = t;
    if (!hasBody) return;
    themeChart();
    renderChart();
    renderSankey();
    renderBars();
  });

  // ---- render orchestration ----
  function renderModel() {
    renderKpis();
    renderBars();
    renderChart();
  }
  function renderAll() {
    computeAllChannels();
    buildModels();
    buildChart();
    renderModel();
    renderSankey();
    renderCampaigns();
    const foot = document.getElementById('attr-foot');
    if (foot && payload.meta && payload.meta.truncated)
      foot.textContent =
        'Large range: showing your active model only. What-if previews are limited above the configured order cap.';
  }

  if (hasBody) renderAll();
})();
