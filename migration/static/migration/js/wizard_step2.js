/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  let cfg = {};
  let t = {};

  function init() {
    const el = document.getElementById('step2-data');
    if (el) {
      try {
        const data = JSON.parse(el.textContent);
        cfg = data.config || {};
        t = data.translations || {};
      } catch (e) {}
    }

    const form = document.getElementById('connection-form');
    if (!form) return;

    if (cfg.platform === 'woocommerce' || cfg.platform === 'shopify') {
      form.addEventListener('submit', function (e) {
        const testConnection = document.querySelector('input[name="test_connection"]');
        if (testConnection && testConnection.checked) {
          e.preventDefault();
          testApiConnection();
        } else {
          const btn = document.getElementById('submit-button');
          if (btn) {
            btn.disabled = true;
            btn.innerHTML = '<div class="loading-spinner"></div> ' + (t.saving || 'Saving...');
          }
        }
      });
    }

    form.addEventListener('submit', function (e) {
      if (window.MigrationWizard && !window.MigrationWizard.validateForm('connection-form')) {
        e.preventDefault();
      }
    });
  }

  function getProgressSteps() {
    if (cfg.platform === 'shopify') {
      return [
        t.exchangingCredentials || 'Exchanging credentials for access token',
        t.verifyingAccess || 'Verifying API access',
        t.countingProducts || 'Counting products',
        t.countingCollections || 'Counting collections',
        t.countingCustomers || 'Counting customers',
        t.countingOrders || 'Counting orders',
        t.countingBlogPosts || 'Counting blog posts',
        t.preparingNext || 'Preparing the next step',
      ];
    }
    return [
      t.testingConnection || 'Testing connection...',
      t.verifyingCredentials || 'Verifying API credentials',
      t.countingProducts || 'Counting products',
      t.countingCategories || 'Counting categories',
      t.countingCustomers || 'Counting customers',
      t.countingOrders || 'Counting orders',
      t.countingBlogPosts || 'Counting blog posts',
      t.preparingNext || 'Preparing the next step',
    ];
  }

  function getSuccessSteps() {
    if (cfg.platform === 'shopify') {
      return [
        [1, 'active', t.verifyingAccess || 'Verifying API access'],
        [1, 'success', t.accessVerified || 'API access verified'],
        [2, 'active', t.countingProducts || 'Counting products'],
        [2, 'success', t.productsCountedDone || 'Products counted'],
        [3, 'active', t.countingCollections || 'Counting collections'],
        [3, 'success', t.collectionsCountedDone || 'Collections counted'],
        [4, 'active', t.countingCustomers || 'Counting customers'],
        [4, 'success', t.customersCountedDone || 'Customers counted'],
        [5, 'active', t.countingOrders || 'Counting orders'],
        [5, 'success', t.ordersCountedDone || 'Orders counted'],
        [6, 'active', t.countingBlogPosts || 'Counting blog posts'],
        [6, 'success', t.blogPostsCountedDone || 'Blog posts counted'],
        [7, 'active', t.preparingNext || 'Preparing the next step'],
      ];
    }
    return [
      [1, 'active', t.verifyingCredentials || 'Verifying API credentials'],
      [1, 'success', t.credentialsVerified || 'Credentials verified'],
      [2, 'active', t.countingProducts || 'Counting products'],
      [2, 'success', t.productsCountedDone || 'Products counted'],
      [3, 'active', t.countingCategories || 'Counting categories'],
      [3, 'success', t.categoriesCountedDone || 'Categories counted'],
      [4, 'active', t.countingCustomers || 'Counting customers'],
      [4, 'success', t.customersCountedDone || 'Customers counted'],
      [5, 'active', t.countingOrders || 'Counting orders'],
      [5, 'success', t.ordersCountedDone || 'Orders counted'],
      [6, 'active', t.countingBlogPosts || 'Counting blog posts'],
      [6, 'success', t.blogPostsCountedDone || 'Blog posts counted'],
      [7, 'active', t.preparingNext || 'Preparing the next step'],
    ];
  }

  function buildProgressHTML() {
    const steps = getProgressSteps();
    return steps
      .map(function (label, i) {
        const cls = i === 0 ? 'active' : 'pending';
        const icon =
          i === 0 ? '<div class="loading-spinner"></div>' : '<i class="fas fa-circle"></i>';
        return (
          '<div class="progress-item ' +
          cls +
          '">' +
          '<div class="progress-icon">' +
          icon +
          '</div>' +
          '<div class="progress-text">' +
          label +
          '</div>' +
          '</div>'
        );
      })
      .join('');
  }

  function testApiConnection() {
    const submitButton = document.getElementById('submit-button');
    const originalHTML = submitButton ? submitButton.innerHTML : '';

    const progressBox = document.createElement('div');
    progressBox.id = 'progress-feedback';
    progressBox.className = 'progress-feedback-box';
    progressBox.innerHTML = buildProgressHTML();

    const form = document.getElementById('connection-form');
    form.parentNode.insertBefore(progressBox, form.nextSibling);
    setTimeout(function () {
      progressBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }, 100);

    if (submitButton) {
      submitButton.disabled = true;
      submitButton.innerHTML =
        '<div class="loading-spinner"></div> ' + (t.processing || 'Processing...');
    }

    const formData = new FormData(form);
    const csrf = document.querySelector('[name=csrfmiddlewaretoken]');

    fetch(cfg.testConnectionUrl, {
      method: 'POST',
      body: formData,
      headers: { 'X-CSRFToken': csrf ? csrf.value : '' },
    })
      .then(function (r) {
        return r.json();
      })
      .then(function (data) {
        if (data.success) {
          const firstStepLabel =
            cfg.platform === 'shopify'
              ? t.tokenObtained || 'Access token obtained'
              : t.connectionSuccessful || 'Connection successful';
          updateProgressStep(0, 'success', firstStepLabel);

          const delays = [500, 500, 400, 400, 400, 400, 400];
          const steps = getSuccessSteps();
          let totalDelay = 500;
          steps.forEach(function (step, i) {
            const delay = totalDelay;
            totalDelay += delays[Math.floor(i / 2)] || 400;
            setTimeout(function () {
              updateProgressStep(step[0], step[1], step[2]);
            }, delay);
          });
          setTimeout(function () {
            if (submitButton) {
              submitButton.innerHTML =
                '<div class="loading-spinner"></div> ' + (t.loadingPreview || 'Loading preview...');
            }
            setTimeout(function () {
              form.submit();
            }, 300);
          }, totalDelay);
        } else {
          updateProgressStep(0, 'error', t.connectionFailed || 'Connection failed');
          showConnectionError(
            t.connectionFailed || 'Connection failed',
            data.error || data.message,
            progressBox,
            submitButton,
            originalHTML
          );
        }
      })
      .catch(function (err) {
        updateProgressStep(0, 'error', t.connectionError || 'Connection error');
        showConnectionError(
          t.connectionError || 'Connection error',
          err.message,
          progressBox,
          submitButton,
          originalHTML
        );
      });
  }

  function showConnectionError(title, detail, progressBox, submitButton, originalHTML) {
    const errorBox = document.createElement('div');
    errorBox.className = 'alert-error';
    errorBox.innerHTML =
      '<i class="fas fa-exclamation-circle"></i> <div><strong>' +
      title +
      '</strong><br>' +
      (detail || '') +
      '</div>';
    const wizContent = document.querySelector('.wizard-content');
    if (wizContent) {
      wizContent.insertBefore(errorBox, progressBox);
    }

    const retryBtn = document.createElement('button');
    retryBtn.type = 'button';
    retryBtn.className = 'button';
    retryBtn.style.cssText =
      'margin-top: 12px; display: inline-flex; align-items: center; gap: 6px;';
    retryBtn.innerHTML = '<i class="fas fa-redo"></i> ' + (t.retryConnection || 'Retry Connection');
    retryBtn.addEventListener('click', function () {
      document.querySelectorAll('.alert-error').forEach(function (el) {
        el.remove();
      });
      if (progressBox && progressBox.parentNode) {
        progressBox.remove();
      }
      if (submitButton) {
        submitButton.disabled = false;
        submitButton.innerHTML = originalHTML;
      }
      testApiConnection();
    });
    errorBox.appendChild(retryBtn);

    if (submitButton) {
      submitButton.disabled = false;
      submitButton.innerHTML = originalHTML;
    }
  }

  function updateProgressStep(index, status, text) {
    const items = document.querySelectorAll('#progress-feedback .progress-item');
    const item = items[index];
    if (!item) return;
    item.classList.remove('pending', 'active', 'success', 'error');
    item.classList.add(status);
    const icon = item.querySelector('.progress-icon');
    if (status === 'active') {
      icon.innerHTML = '<div class="loading-spinner"></div>';
    } else if (status === 'success') {
      icon.innerHTML = '<i class="fas fa-check-circle"></i>';
    } else if (status === 'error') {
      icon.innerHTML = '<i class="fas fa-times-circle"></i>';
    }
    if (text) {
      item.querySelector('.progress-text').textContent = text;
    }
  }

  /* ── Shopify Setup Guide Modal ── */

  function initSetupGuide() {
    const overlay = document.getElementById('shopify-setup-guide');
    if (!overlay) return;

    const openBtn = document.getElementById('open-setup-guide');
    const closeBtn = document.getElementById('close-setup-guide');
    const prevBtn = document.getElementById('guide-prev');
    const nextBtn = document.getElementById('guide-next');
    const doneBtn = document.getElementById('guide-done');
    const counterEl = document.getElementById('guide-current-step');
    const steps = overlay.querySelectorAll('.guide-step');
    const totalSteps = steps.length;
    let currentStep = 1;

    function showStep(n) {
      currentStep = n;
      steps.forEach(function (s) {
        s.classList.remove('active');
      });
      const target = overlay.querySelector('[data-guide-step="' + n + '"]');
      if (target) target.classList.add('active');
      if (counterEl) counterEl.textContent = n;
      prevBtn.disabled = n <= 1;
      if (n >= totalSteps) {
        nextBtn.hidden = true;
        doneBtn.hidden = false;
      } else {
        nextBtn.hidden = false;
        doneBtn.hidden = true;
      }
      // Scroll modal body to top when changing steps
      const body = overlay.querySelector('.admin-modal-body');
      if (body) body.scrollTop = 0;
    }

    function openGuide() {
      showStep(1);
      overlay.classList.add('active');
      document.body.classList.add('admin-modal-body-locked');
    }

    function closeGuide() {
      overlay.classList.remove('active');
      document.body.classList.remove('admin-modal-body-locked');
    }

    if (openBtn) openBtn.addEventListener('click', openGuide);
    if (closeBtn) closeBtn.addEventListener('click', closeGuide);
    if (prevBtn)
      prevBtn.addEventListener('click', function () {
        if (currentStep > 1) showStep(currentStep - 1);
      });
    if (nextBtn)
      nextBtn.addEventListener('click', function () {
        if (currentStep < totalSteps) showStep(currentStep + 1);
      });
    if (doneBtn) doneBtn.addEventListener('click', closeGuide);

    // Close on overlay click (outside modal)
    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) closeGuide();
    });

    // Close on Escape key
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && overlay.classList.contains('active')) {
        closeGuide();
      }
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    init();
    initSetupGuide();
  });
})();
