/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  let data = {};

  function init() {
    const dataEl = document.getElementById('design-dashboard-data');
    if (dataEl) {
      try {
        data = JSON.parse(dataEl.textContent);
      } catch (e) {}
    }

    // Animate stat cards on page load
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach(function (card, index) {
      setTimeout(function () {
        card.classList.add('animated');
      }, index * 100);
    });

    // Collapsible workflow sections
    const sectionHeaders = document.querySelectorAll('.section-header');
    sectionHeaders.forEach(function (header) {
      header.addEventListener('click', function () {
        const section = this.parentElement;
        section.classList.toggle('collapsed');
      });
    });

    // Force Light Mode Toggle
    const forceLightModeToggle = document.getElementById('force-light-mode-toggle');
    const forceModeStatus = document.getElementById('force-mode-status');

    if (forceLightModeToggle && !forceLightModeToggle.disabled) {
      forceLightModeToggle.addEventListener('change', function () {
        const forceLightMode = this.checked;
        const toggleRef = this;

        if (forceModeStatus) {
          forceModeStatus.textContent = forceLightMode
            ? (data.translations && data.translations.modeOn) ||
              'On - Dark mode disabled (light theme forced)'
            : (data.translations && data.translations.modeOff) ||
              'Off - Auto (respects system preference)';
        }

        fetch((data.urls && data.urls.toggleForceLightMode) || '', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': AdminUtils.getCsrfToken(),
          },
          body: JSON.stringify({ force_light_mode: forceLightMode }),
        })
          .then(function (response) {
            return response.json();
          })
          .then(function (responseData) {
            if (!responseData.success) {
              console.error('Failed to update force light mode setting:', responseData.error);
              toggleRef.checked = !forceLightMode;
              if (forceModeStatus) {
                forceModeStatus.textContent = !forceLightMode
                  ? (data.translations && data.translations.modeOn) ||
                    'On - Dark mode disabled (light theme forced)'
                  : (data.translations && data.translations.modeOff) ||
                    'Off - Auto (respects system preference)';
              }
            }
          })
          .catch(function (error) {
            console.error('Error updating force light mode setting:', error);
            toggleRef.checked = !forceLightMode;
            if (forceModeStatus) {
              forceModeStatus.textContent = !forceLightMode
                ? (data.translations && data.translations.modeOn) ||
                  'On - Dark mode disabled (light theme forced)'
                : (data.translations && data.translations.modeOff) ||
                  'Off - Auto (respects system preference)';
            }
          });
      });
    }

    document.addEventListener('click', function (e) {
      const btn = e.target.closest('[data-action="export-theme"]');
      if (btn) {
        e.preventDefault();
        AdminModal.alert('Theme export feature coming soon!');
      }
    });
  }

  document.addEventListener('DOMContentLoaded', init);
})();
