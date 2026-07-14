/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */
/* SEO Dashboard JavaScript */
(function () {
  'use strict';

  const config = document.getElementById('seo-dashboard-config');
  if (!config) return;

  const URLS = {
    coverage: config.dataset.coverageUrl,
    coverageRefresh: config.dataset.coverageRefreshUrl,
    missingItems: config.dataset.missingItemsUrl,
    batchGenerate: config.dataset.batchUrl,
    items: config.dataset.itemsUrl, // contains __CT__ placeholder
    generate: config.dataset.generateUrl, // contains __CT__ and /0/ placeholders
  };
  const CSRF_TOKEN = config.dataset.csrfToken;
  const BATCH_SIZE = 10;

  let generateCancelled = false;
  let drillDownCache = {}; // Cache fetched items per content type

  // ── Initialize on DOM ready ──
  document.addEventListener('DOMContentLoaded', function () {
    initCoverageRing();
    initProgressBars();
    bindEvents();
  });

  // ── Coverage Ring Animation ──
  function initCoverageRing() {
    const fill = document.querySelector('.seo-coverage-ring__fill');
    if (!fill) return;

    const pct = parseFloat(fill.dataset.percentage) || 0;
    const circumference = 326.73;
    const offset = circumference - (pct / 100) * circumference;

    requestAnimationFrame(function () {
      fill.style.strokeDashoffset = offset;
    });
  }

  // ── Progress Bar Animation ──
  function initProgressBars() {
    document.querySelectorAll('.seo-ct-bar__fill').forEach(function (bar) {
      const width = parseFloat(bar.dataset.width) || 0;
      requestAnimationFrame(function () {
        bar.style.width = width + '%';
      });
    });
  }

  // ── Event Bindings ──
  function bindEvents() {
    const refreshBtn = document.getElementById('refreshCoverageBtn');
    if (refreshBtn) {
      refreshBtn.addEventListener('click', refreshCoverage);
    }

    const generateBtn = document.getElementById('generateAllBtn');
    if (generateBtn) {
      generateBtn.addEventListener('click', generateAllMissing);
    }

    const closeModalBtn = document.getElementById('closeModalBtn');
    if (closeModalBtn) {
      closeModalBtn.addEventListener('click', closeModal);
    }

    const cancelBtn = document.getElementById('cancelGenerateBtn');
    if (cancelBtn) {
      cancelBtn.addEventListener('click', function () {
        generateCancelled = true;
        closeModal();
      });
    }

    // Drill-down: content type row clicks
    document.querySelectorAll('.seo-ct-row[data-ct-key]').forEach(function (row) {
      row.addEventListener('click', function (e) {
        // Don't toggle if clicking a button inside the row
        if (e.target.closest('button') || e.target.closest('a')) return;
        toggleDrillDown(row);
      });
    });
  }

  // ══════════════════════════════════════════
  // ── Drill-Down Logic ──
  // ══════════════════════════════════════════

  function toggleDrillDown(row) {
    const ctKey = row.dataset.ctKey;
    const detail = document.querySelector('.seo-ct-detail[data-ct-key="' + ctKey + '"]');
    if (!detail) return;

    const isExpanded = row.classList.contains('expanded');

    if (isExpanded) {
      // Collapse
      row.classList.remove('expanded');
      detail.classList.remove('expanded');
    } else {
      // Expand
      row.classList.add('expanded');
      detail.classList.add('expanded');

      // Load items if not cached
      if (!drillDownCache[ctKey]) {
        loadDrillDownItems(ctKey, detail);
      }
    }
  }

  function loadDrillDownItems(ctKey, container) {
    container.innerHTML =
      '<div class="seo-ct-loading"><i class="fas fa-spinner fa-spin"></i> Loading items...</div>';

    const url = URLS.items.replace('__CT__', ctKey);

    fetch(url)
      .then(function (res) {
        return res.json();
      })
      .then(function (data) {
        if (!data.success) {
          container.innerHTML =
            '<div class="seo-ct-empty">' + (data.error || 'Failed to load') + '</div>';
          return;
        }

        drillDownCache[ctKey] = data.items;
        renderDrillDown(ctKey, container, data.items, 'all');
      })
      .catch(function (err) {
        container.innerHTML = '<div class="seo-ct-empty">Failed to load items.</div>';
      });
  }

  function renderDrillDown(ctKey, container, items, filter) {
    let filtered = items;
    if (filter === 'missing') {
      filtered = items.filter(function (i) {
        return !i.has_both;
      });
    } else if (filter === 'complete') {
      filtered = items.filter(function (i) {
        return i.has_both;
      });
    }

    const missingCount = items.filter(function (i) {
      return !i.has_both;
    }).length;
    const completeCount = items.filter(function (i) {
      return i.has_both;
    }).length;

    let html = '<div class="seo-ct-detail__inner">';

    // Filter tabs
    html += '<div class="seo-items-filter">';
    html +=
      '<button type="button" class="seo-items-filter-btn' +
      (filter === 'all' ? ' active' : '') +
      '" data-filter="all" data-ct="' +
      ctKey +
      '">All (' +
      items.length +
      ')</button>';
    html +=
      '<button type="button" class="seo-items-filter-btn' +
      (filter === 'missing' ? ' active' : '') +
      '" data-filter="missing" data-ct="' +
      ctKey +
      '">Missing (' +
      missingCount +
      ')</button>';
    html +=
      '<button type="button" class="seo-items-filter-btn' +
      (filter === 'complete' ? ' active' : '') +
      '" data-filter="complete" data-ct="' +
      ctKey +
      '">Complete (' +
      completeCount +
      ')</button>';
    html += '</div>';

    if (filtered.length === 0) {
      html += '<div class="seo-ct-empty">No items match this filter.</div>';
    } else {
      html += '<table class="seo-items-table">';
      html += '<thead><tr>';
      html += '<th>Name</th>';
      html += '<th>Meta Title</th>';
      html += '<th>Meta Description</th>';
      html += '<th>Status</th>';
      html += '<th></th>';
      html += '</tr></thead>';
      html += '<tbody>';

      filtered.forEach(function (item) {
        let statusClass, statusLabel;
        if (item.has_both) {
          statusClass = 'complete';
          statusLabel = 'Complete';
        } else if (item.has_title || item.has_description) {
          statusClass = 'partial';
          statusLabel = 'Partial';
        } else {
          statusClass = 'missing';
          statusLabel = 'Missing';
        }

        html += '<tr data-item-id="' + item.id + '" data-ct="' + ctKey + '">';

        // Name with link
        html += '<td class="seo-item-name">';
        if (item.edit_url) {
          html += '<a href="' + escapeHtml(item.edit_url) + '">' + escapeHtml(item.name) + '</a>';
        } else {
          html += escapeHtml(item.name);
        }
        html += '</td>';

        // Meta title
        html +=
          '<td class="seo-item-meta' + (item.meta_title ? '' : ' seo-item-meta--empty') + '">';
        html += item.meta_title ? escapeHtml(item.meta_title) : 'Not set';
        html += '</td>';

        // Meta description
        html +=
          '<td class="seo-item-meta' +
          (item.meta_description ? '' : ' seo-item-meta--empty') +
          '">';
        html += item.meta_description ? escapeHtml(item.meta_description) : 'Not set';
        html += '</td>';

        // Status badge
        html +=
          '<td><span class="seo-status-badge seo-status-badge--' +
          statusClass +
          '">' +
          statusLabel +
          '</span></td>';

        // Generate button
        html += '<td>';
        if (!item.has_both) {
          html +=
            '<button type="button" class="seo-item-generate-btn" data-ct="' +
            ctKey +
            '" data-id="' +
            item.id +
            '">';
          html += '<i class="fas fa-magic"></i> Generate';
          html += '</button>';
        }
        html += '</td>';

        html += '</tr>';
      });

      html += '</tbody></table>';
    }

    html += '</div>';

    container.innerHTML = html;

    // Bind filter tab clicks
    container.querySelectorAll('.seo-items-filter-btn').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        const newFilter = btn.dataset.filter;
        const ct = btn.dataset.ct;
        const parentDetail = container;
        renderDrillDown(ct, parentDetail, drillDownCache[ct], newFilter);
      });
    });

    // Bind per-item generate buttons
    container.querySelectorAll('.seo-item-generate-btn').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.stopPropagation();
        generateSingleItem(btn);
      });
    });
  }

  function generateSingleItem(btn) {
    const ctKey = btn.dataset.ct;
    const itemId = btn.dataset.id;

    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
    btn.classList.add('generating');

    // Build URL from template: replace __CT__ and /0/ placeholder
    const url = URLS.generate.replace('__CT__', ctKey).replace('/0/', '/' + itemId + '/');

    fetch(url, {
      method: 'POST',
      headers: {
        'X-CSRFToken': CSRF_TOKEN,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({}),
    })
      .then(function (res) {
        return res.json();
      })
      .then(function (data) {
        if (data.success) {
          // Update cache
          if (drillDownCache[ctKey]) {
            drillDownCache[ctKey].forEach(function (item) {
              if (String(item.id) === String(itemId)) {
                item.meta_title = data.meta_title;
                item.meta_description = data.meta_description;
                item.has_title = true;
                item.has_description = true;
                item.has_both = true;
              }
            });
          }

          // Update the row in-place
          const tr = btn.closest('tr');
          if (tr) {
            const cells = tr.querySelectorAll('td');
            // Meta title
            if (cells[1]) {
              cells[1].className = 'seo-item-meta';
              cells[1].textContent = data.meta_title;
            }
            // Meta description
            if (cells[2]) {
              cells[2].className = 'seo-item-meta';
              cells[2].textContent = data.meta_description;
            }
            // Status badge
            if (cells[3]) {
              cells[3].innerHTML =
                '<span class="seo-status-badge seo-status-badge--complete">Complete</span>';
            }
            // Remove generate button
            if (cells[4]) {
              cells[4].innerHTML = '';
            }
          }

          // Update the parent row counts
          updateRowCounts(ctKey);
        } else {
          btn.disabled = false;
          btn.innerHTML = '<i class="fas fa-magic"></i> Generate';
          btn.classList.remove('generating');
          AdminModal.alert({
            message: 'Generation failed: ' + (data.error || 'Unknown error'),
            type: 'error',
          });
        }
      })
      .catch(function (err) {
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-magic"></i> Generate';
        btn.classList.remove('generating');
        AdminModal.alert({ message: 'Request failed: ' + err.message, type: 'error' });
      });
  }

  function updateRowCounts(ctKey) {
    // Recalculate from cache
    const items = drillDownCache[ctKey];
    if (!items) return;

    const total = items.length;
    const withBoth = items.filter(function (i) {
      return i.has_both;
    }).length;
    const pct = total > 0 ? Math.round((withBoth / total) * 100) : 0;

    const row = document.querySelector('.seo-ct-row[data-ct-key="' + ctKey + '"]');
    if (!row) return;

    const count = row.querySelector('.seo-ct-count');
    if (count) count.textContent = withBoth + ' / ' + total;

    const barFill = row.querySelector('.seo-ct-bar__fill');
    if (barFill) barFill.style.width = pct + '%';

    const pctEl = row.querySelector('.seo-ct-pct');
    if (pctEl) pctEl.textContent = pct + '%';

    row.dataset.missing = total - withBoth;
  }

  // ══════════════════════════════════════════
  // ── Refresh Coverage ──
  // ══════════════════════════════════════════

  function refreshCoverage() {
    const btn = document.getElementById('refreshCoverageBtn');
    if (!btn) return;

    btn.classList.add('spinning');
    btn.disabled = true;

    // Clear drill-down cache so panels reload fresh data
    drillDownCache = {};

    fetch(URLS.coverageRefresh, {
      method: 'POST',
      headers: {
        'X-CSRFToken': CSRF_TOKEN,
        'Content-Type': 'application/json',
      },
    })
      .then(function (res) {
        return res.json();
      })
      .then(function (data) {
        if (data.success) {
          updateDashboard(data);
        }
      })
      .catch(function (err) {
        console.error('Failed to refresh coverage:', err);
      })
      .finally(function () {
        btn.classList.remove('spinning');
        btn.disabled = false;
      });
  }

  // ── Update Dashboard with Fresh Data ──
  function updateDashboard(data) {
    // Update stat cards
    const statValues = document.querySelectorAll('.seo-stat-card .value');
    if (statValues.length >= 4) {
      statValues[0].textContent = data.total_items;
      statValues[1].textContent = data.with_both;
      statValues[2].textContent = data.missing_any;
    }

    // Update coverage ring
    const pctEl = document.getElementById('overallPct');
    if (pctEl) {
      pctEl.textContent = Math.round(data.overall_percentage) + '%';
    }

    const fill = document.querySelector('.seo-coverage-ring__fill');
    if (fill) {
      const circumference = 326.73;
      const offset = circumference - (data.overall_percentage / 100) * circumference;
      fill.style.strokeDashoffset = offset;
    }

    // Update summary text
    const summaryText = document.getElementById('summaryText');
    if (summaryText) {
      summaryText.textContent =
        Math.round(data.overall_percentage) + '% of your content has complete SEO';
    }

    // Update content type bars (keyed by data-ct-key)
    if (data.content_types) {
      data.content_types.forEach(function (ct) {
        const row = document.querySelector('.seo-ct-row[data-ct-key="' + ct.key + '"]');
        if (!row) return;

        const count = row.querySelector('.seo-ct-count');
        if (count) count.textContent = ct.with_both + ' / ' + ct.total;

        const barFill = row.querySelector('.seo-ct-bar__fill');
        if (barFill) barFill.style.width = ct.percentage + '%';

        const pct = row.querySelector('.seo-ct-pct');
        if (pct) pct.textContent = Math.round(ct.percentage) + '%';

        row.dataset.missing = ct.missing;

        // Collapse and clear any open drill-down for this type
        const detail = document.querySelector('.seo-ct-detail[data-ct-key="' + ct.key + '"]');
        if (detail && detail.classList.contains('expanded')) {
          detail.classList.remove('expanded');
          row.classList.remove('expanded');
          detail.innerHTML = '';
        }
      });
    }

    // Update quality metrics
    if (data.quality) {
      const qualityItems = document.querySelectorAll('.seo-quality-item');
      const qKeys = ['title_too_short', 'title_too_long', 'desc_too_short', 'desc_too_long'];
      qKeys.forEach(function (key, idx) {
        if (qualityItems[idx]) {
          const val = qualityItems[idx].querySelector('.seo-quality-value');
          if (val) val.textContent = data.quality[key];

          qualityItems[idx].classList.remove('seo-quality-item--ok', 'seo-quality-item--warn');
          qualityItems[idx].classList.add(
            data.quality[key] === 0 ? 'seo-quality-item--ok' : 'seo-quality-item--warn'
          );
        }
      });
    }
  }

  // ══════════════════════════════════════════
  // ── Generate All Missing ──
  // ══════════════════════════════════════════

  function generateAllMissing() {
    generateCancelled = false;

    const modal = document.getElementById('generateModal');
    if (modal) modal.style.display = 'flex';

    const progressBar = document.getElementById('generateProgressBar');
    const progressText = document.getElementById('progressText');
    const progressCount = document.getElementById('progressCount');
    const progressLog = document.getElementById('progressLog');

    if (progressBar) progressBar.style.width = '0%';
    if (progressText) progressText.textContent = 'Fetching missing items...';
    if (progressCount) progressCount.textContent = '';
    if (progressLog) progressLog.innerHTML = '';

    const generateBtn = document.getElementById('generateAllBtn');
    if (generateBtn) generateBtn.disabled = true;

    fetch(URLS.missingItems)
      .then(function (res) {
        return res.json();
      })
      .then(function (data) {
        if (!data.success || !data.items || data.items.length === 0) {
          addLog(progressLog, 'No missing items found.', 'success');
          if (progressText) progressText.textContent = 'Complete';
          return;
        }

        const items = data.items;
        const total = items.length;

        if (progressText) progressText.textContent = 'Generating...';
        if (progressCount) progressCount.textContent = '0 / ' + total;

        addLog(progressLog, 'Found ' + total + ' items missing SEO content.');

        processBatches(items, 0, total, progressBar, progressText, progressCount, progressLog);
      })
      .catch(function (err) {
        addLog(progressLog, 'Error: ' + err.message, 'error');
        if (progressText) progressText.textContent = 'Failed';
        if (generateBtn) generateBtn.disabled = false;
      });
  }

  function processBatches(
    items,
    processed,
    total,
    progressBar,
    progressText,
    progressCount,
    progressLog
  ) {
    if (generateCancelled) {
      addLog(progressLog, 'Generation cancelled by user.', 'error');
      if (progressText) progressText.textContent = 'Cancelled';
      var btn = document.getElementById('generateAllBtn');
      if (btn) btn.disabled = false;
      return;
    }

    if (processed >= total) {
      if (progressBar) progressBar.style.width = '100%';
      if (progressText) progressText.textContent = 'Complete!';
      addLog(progressLog, 'All items processed successfully.', 'success');

      // Clear drill-down cache and refresh
      drillDownCache = {};
      refreshCoverage();

      var btn = document.getElementById('generateAllBtn');
      if (btn) btn.disabled = false;
      return;
    }

    const batch = items.slice(processed, processed + BATCH_SIZE);

    fetch(URLS.batchGenerate, {
      method: 'POST',
      headers: {
        'X-CSRFToken': CSRF_TOKEN,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ items: batch }),
    })
      .then(function (res) {
        return res.json();
      })
      .then(function (data) {
        const newProcessed = processed + batch.length;

        if (data.success !== false && data.results) {
          let successes = 0;
          let failures = 0;
          data.results.forEach(function (r) {
            if (r.success) {
              successes++;
            } else {
              failures++;
              addLog(
                progressLog,
                'Failed: ' + r.model_type + ' #' + r.object_id + ' - ' + (r.error || 'Unknown'),
                'error'
              );
            }
          });

          addLog(progressLog, 'Batch: ' + successes + ' generated, ' + failures + ' failed.');
        } else {
          addLog(progressLog, 'Batch failed: ' + (data.error || 'Unknown error'), 'error');
        }

        const pct = Math.round((newProcessed / total) * 100);
        if (progressBar) progressBar.style.width = pct + '%';
        if (progressCount) progressCount.textContent = newProcessed + ' / ' + total;

        processBatches(
          items,
          newProcessed,
          total,
          progressBar,
          progressText,
          progressCount,
          progressLog
        );
      })
      .catch(function (err) {
        addLog(progressLog, 'Request error: ' + err.message, 'error');

        const newProcessed = processed + batch.length;
        const pct = Math.round((newProcessed / total) * 100);
        if (progressBar) progressBar.style.width = pct + '%';
        if (progressCount) progressCount.textContent = newProcessed + ' / ' + total;

        processBatches(
          items,
          newProcessed,
          total,
          progressBar,
          progressText,
          progressCount,
          progressLog
        );
      });
  }

  // ══════════════════════════════════════════
  // ── Helpers ──
  // ══════════════════════════════════════════

  function addLog(container, message, type) {
    if (!container) return;
    const div = document.createElement('div');
    if (type) div.className = 'log-' + type;
    div.textContent = message;
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
  }

  function closeModal() {
    const modal = document.getElementById('generateModal');
    if (modal) modal.style.display = 'none';
  }

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }
})();
