/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Log Viewer - Real-time Docker container log monitoring
 *
 * Reads configuration from #log-viewer-config JSON script tag.
 */
(function () {
  'use strict';

  // Read configuration from JSON script tag
  const configElement = document.getElementById('log-viewer-config');
  const DEFAULT_CONFIG = {
    logsApiUrl: '',
    statsApiUrl: '',
    containersApiUrl: '',
    exportApiUrl: '',
    refreshInterval: 5000,
    pageSize: 50,
  };
  let CONFIG = DEFAULT_CONFIG;
  if (configElement) {
    try {
      CONFIG = JSON.parse(configElement.textContent);
    } catch (e) {
      console.error('log-viewer: failed to parse config', e);
    }
  }

  // State
  const state = {
    logs: [],
    offset: 0,
    hasMore: false,
    loading: false,
    autoRefreshTimer: null,
  };

  // DOM Elements
  const elements = {
    logEntries: document.getElementById('log-entries'),
    logCount: document.getElementById('log-count'),
    logSourceInfo: document.getElementById('log-source-info'),
    btnRefresh: document.getElementById('btn-refresh'),
    btnClear: document.getElementById('btn-clear'),
    btnLoadMore: document.getElementById('btn-load-more'),
    autoRefresh: document.getElementById('auto-refresh'),
    filterContainer: document.getElementById('filter-container'),
    filterLevel: document.getElementById('filter-level'),
    filterSearch: document.getElementById('filter-search'),
    filterSource: document.getElementById('filter-source'),
    containerBadges: document.getElementById('container-badges'),
    btnExport: document.getElementById('btn-export'),
    exportMenu: document.getElementById('export-menu'),
    exportDropdown: document.getElementById('export-dropdown'),
    statInfo: document.getElementById('stat-info'),
    statWarning: document.getElementById('stat-warning'),
    statError: document.getElementById('stat-error'),
    statCritical: document.getElementById('stat-critical'),
  };

  // Level CSS class mapping for badges
  const levelClasses = {
    INFO: 'level-badge-info',
    WARNING: 'level-badge-warning',
    ERROR: 'level-badge-error',
    CRITICAL: 'level-badge-critical',
  };

  // Format timestamp
  function formatTimestamp(isoString) {
    const date = new Date(isoString);
    return date.toLocaleString('en-US', {
      month: 'short',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: false,
    });
  }

  // Create log entry element
  function createLogEntry(log) {
    const entry = document.createElement('div');
    entry.className = 'log-entry log-level-' + log.level.toLowerCase();

    const levelClass = levelClasses[log.level] || 'level-badge-default';

    entry.innerHTML = `
            <span class="col-timestamp">${formatTimestamp(log.timestamp)}</span>
            <span class="col-container">${log.container}</span>
            <span class="col-level">
                <span class="level-badge ${levelClass}">
                    ${log.level}
                </span>
            </span>
            <span class="col-message">${escapeHtml(log.message)}</span>
        `;

    return entry;
  }

  // Escape HTML
  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  // Get current filters
  function getFilters() {
    return {
      container: elements.filterContainer.value,
      level: elements.filterLevel.value,
      search: elements.filterSearch.value,
      source: elements.filterSource.value,
    };
  }

  // Fetch logs from API
  async function fetchLogs(append = false) {
    if (state.loading) return;
    state.loading = true;

    if (!append) {
      state.offset = 0;
      elements.logEntries.innerHTML =
        '<div class="log-loading"><i class="fas fa-spinner fa-spin"></i> Loading logs...</div>';
    }

    const filters = getFilters();
    const params = new URLSearchParams({
      container: filters.container,
      level: filters.level,
      search: filters.search,
      source: filters.source,
      limit: CONFIG.pageSize,
      offset: state.offset,
    });

    try {
      const response = await fetch(`${CONFIG.logsApiUrl}?${params}`, {
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
        },
      });

      if (!response.ok) throw new Error('Failed to fetch logs');

      const data = await response.json();

      if (!data.success) throw new Error(data.error || 'Unknown error');

      if (!append) {
        state.logs = data.logs;
        renderLogs();
      } else {
        state.logs = state.logs.concat(data.logs);
        appendLogs(data.logs);
      }

      state.hasMore = data.has_more;
      state.offset += data.count;

      elements.logCount.textContent = state.logs.length;
      elements.logSourceInfo.textContent =
        data.source === 'redis' ? '(from Redis)' : '(from Database)';
      elements.btnLoadMore.classList.toggle('mgmt-hidden', !state.hasMore);
    } catch (error) {
      console.error('Error fetching logs:', error);
      if (!append) {
        elements.logEntries.innerHTML = `<div class="log-error"><i class="fas fa-exclamation-triangle"></i> ${error.message}</div>`;
      }
    } finally {
      state.loading = false;
    }
  }

  // Render all logs
  function renderLogs() {
    elements.logEntries.innerHTML = '';

    if (state.logs.length === 0) {
      elements.logEntries.innerHTML =
        '<div class="log-empty"><i class="fas fa-inbox"></i> No logs found</div>';
      return;
    }

    const fragment = document.createDocumentFragment();
    state.logs.forEach(log => {
      fragment.appendChild(createLogEntry(log));
    });
    elements.logEntries.appendChild(fragment);
  }

  // Append new logs
  function appendLogs(logs) {
    const fragment = document.createDocumentFragment();
    logs.forEach(log => {
      fragment.appendChild(createLogEntry(log));
    });
    elements.logEntries.appendChild(fragment);
  }

  // Fetch and update stats
  async function fetchStats() {
    try {
      const response = await fetch(CONFIG.statsApiUrl, {
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
        },
      });

      if (!response.ok) return;

      const data = await response.json();
      if (!data.success) return;

      const global = data.stats.global || {};
      elements.statInfo.textContent = global.INFO || 0;
      elements.statWarning.textContent = global.WARNING || 0;
      elements.statError.textContent = global.ERROR || 0;
      elements.statCritical.textContent = global.CRITICAL || 0;
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  }

  // Fetch and update container status
  async function fetchContainers() {
    try {
      const response = await fetch(CONFIG.containersApiUrl, {
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
        },
      });

      if (!response.ok) return;

      const data = await response.json();
      if (!data.success) return;

      // Update container badges status
      data.containers.forEach(container => {
        const badge = elements.containerBadges.querySelector(
          `[data-container="${container.name}"]`
        );
        if (badge) {
          badge.classList.remove('running', 'stopped', 'unknown');
          if (container.running) {
            badge.classList.add('running');
          } else if (['unknown', 'not_found', 'error'].includes(container.status)) {
            badge.classList.add('unknown');
          } else {
            badge.classList.add('stopped');
          }
        }
      });
    } catch (error) {
      console.error('Error fetching containers:', error);
    }
  }

  // Start auto-refresh
  function startAutoRefresh() {
    stopAutoRefresh();
    if (elements.autoRefresh.checked) {
      state.autoRefreshTimer = setInterval(() => {
        fetchLogs();
        fetchStats();
      }, CONFIG.refreshInterval);
    }
  }

  // Stop auto-refresh
  function stopAutoRefresh() {
    if (state.autoRefreshTimer) {
      clearInterval(state.autoRefreshTimer);
      state.autoRefreshTimer = null;
    }
  }

  // Clear filters
  function clearFilters() {
    elements.filterContainer.value = '';
    elements.filterLevel.value = '';
    elements.filterSearch.value = '';

    // Remove active class from container badges
    const badges = elements.containerBadges.querySelectorAll('.container-badge');
    badges.forEach(badge => badge.classList.remove('active'));

    fetchLogs();
  }

  // Trigger export download
  function exportLogs(format) {
    const filters = getFilters();
    const params = new URLSearchParams({
      format: format,
      container: filters.container,
      level: filters.level,
      search: filters.search,
      source: filters.source,
    });
    window.location.href = `${CONFIG.exportApiUrl}?${params}`;
    elements.exportMenu.classList.add('mgmt-hidden');
  }

  // Debounce function
  function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }

  // Event listeners
  elements.btnRefresh.addEventListener('click', () => {
    fetchLogs();
    fetchStats();
    fetchContainers();
  });

  elements.btnClear.addEventListener('click', clearFilters);

  elements.btnLoadMore.addEventListener('click', () => {
    fetchLogs(true);
  });

  elements.autoRefresh.addEventListener('change', () => {
    if (elements.autoRefresh.checked) {
      startAutoRefresh();
    } else {
      stopAutoRefresh();
    }
  });

  elements.filterContainer.addEventListener('change', () => fetchLogs());
  elements.filterLevel.addEventListener('change', () => fetchLogs());
  elements.filterSource.addEventListener('change', () => fetchLogs());
  elements.filterSearch.addEventListener(
    'input',
    debounce(() => fetchLogs(), 300)
  );

  // Export dropdown toggle
  elements.btnExport.addEventListener('click', e => {
    e.stopPropagation();
    elements.exportMenu.classList.toggle('mgmt-hidden');
  });

  // Export option click
  elements.exportDropdown.addEventListener('click', e => {
    const option = e.target.closest('.export-option');
    if (!option) return;
    const format = option.dataset.format;
    if (format) {
      exportLogs(format);
    }
  });

  // Close export dropdown on outside click
  document.addEventListener('click', e => {
    if (!elements.exportDropdown.contains(e.target)) {
      elements.exportMenu.classList.add('mgmt-hidden');
    }
  });

  // Container badge click handler
  elements.containerBadges.addEventListener('click', e => {
    const badge = e.target.closest('.container-badge');
    if (!badge) return;

    const container = badge.dataset.container;

    // Toggle active state
    const badges = elements.containerBadges.querySelectorAll('.container-badge');
    badges.forEach(b => b.classList.remove('active'));

    if (elements.filterContainer.value === container) {
      // Deselect if already selected
      elements.filterContainer.value = '';
    } else {
      badge.classList.add('active');
      elements.filterContainer.value = container;
    }

    fetchLogs();
  });

  // Initialize when DOM is ready
  function init() {
    fetchLogs();
    fetchStats();
    fetchContainers();
    startAutoRefresh();

    // Cleanup on page unload
    window.addEventListener('beforeunload', stopAutoRefresh);
  }

  // Run init when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
