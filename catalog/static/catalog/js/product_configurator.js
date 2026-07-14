/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Product Configurator - Frontend Wizard
 * Vanilla JS, no dependencies. Handles step-by-step configuration,
 * client-side compatibility filtering, real-time pricing, and cart integration.
 */
document.addEventListener('DOMContentLoaded', function () {
  'use strict';

  // =========================================================================
  // State
  // =========================================================================

  const state = {
    productId: null,
    pricingStrategy: 'components_sum',
    basePrice: 0,
    currency: window.__shopCurrency || 'USD',
    slots: [],
    rules: [],
    presets: [],
    selections: {}, // { slotId: [optionId, ...] }
    currentStep: 0, // index into state.slots
    presetId: null,
  };

  // =========================================================================
  // Initialization
  // =========================================================================

  const dataEl = document.getElementById('configurator-data');
  if (!dataEl) return;

  let data;
  try {
    data = JSON.parse(dataEl.textContent);
  } catch (e) {
    console.error('Failed to parse configurator data:', e);
    return;
  }

  state.productId = data.product_id;
  state.pricingStrategy = data.pricing_strategy || 'components_sum';
  state.basePrice = parseFloat(data.base_price) || 0;
  state.currency = data.currency || window.__shopCurrency || 'USD';
  state.slots = data.slots || [];
  state.rules = data.rules || [];
  state.presets = data.presets || [];

  // Apply defaults
  state.slots.forEach(function (slot) {
    state.selections[slot.id] = [];
    (slot.options || []).forEach(function (opt) {
      if (opt.is_default) {
        state.selections[slot.id].push(opt.id);
      }
    });
  });

  // Show presets if available
  if (state.presets.length > 0) {
    renderPresets();
  }

  renderStepNav();
  renderCurrentPanel();
  renderSummary();
  updateNavButtons();

  // =========================================================================
  // Presets
  // =========================================================================

  function renderPresets() {
    const section = document.getElementById('presets-section');
    const grid = document.getElementById('presets-grid');
    if (!section || !grid) return;

    const wrapper = document.getElementById('presets-section-wrapper');
    if (wrapper) wrapper.classList.add('visible');
    grid.innerHTML = '';

    state.presets.forEach(function (preset) {
      const card = document.createElement('div');
      card.className =
        'configurator-preset-card' +
        (preset.is_featured ? ' configurator-preset-card--featured' : '');
      card.dataset.presetId = preset.id;

      let imageHtml;
      if (preset.image_url) {
        imageHtml =
          '<div class="configurator-preset-card__image"><img src="' +
          escapeHtml(preset.image_url) +
          '" alt="' +
          escapeHtml(preset.name) +
          '"></div>';
      } else {
        imageHtml =
          '<div class="configurator-preset-card__image"><i class="fas fa-cogs"></i></div>';
      }

      const badgeHtml = preset.is_featured
        ? '<span class="configurator-preset-card__badge">Featured</span>'
        : '';

      card.innerHTML =
        badgeHtml +
        imageHtml +
        '<div class="configurator-preset-card__name">' +
        escapeHtml(preset.name) +
        '</div>' +
        '<div class="configurator-preset-card__description">' +
        escapeHtml(preset.description || '') +
        '</div>' +
        '<div class="configurator-preset-card__price">' +
        formatPrice(preset.calculated_price) +
        '</div>';

      card.addEventListener('click', function () {
        applyPreset(preset);
      });

      grid.appendChild(card);
    });

    const scratchBtn = document.getElementById('start-scratch');
    if (scratchBtn) {
      scratchBtn.addEventListener('click', function () {
        const w = document.getElementById('presets-section-wrapper');
        if (w) w.classList.remove('visible');
      });
    }
  }

  function applyPreset(preset) {
    state.presetId = preset.id;
    const selections = preset.selections || {};

    // Reset all
    state.slots.forEach(function (slot) {
      state.selections[slot.id] = [];
    });

    // Apply preset selections
    Object.keys(selections).forEach(function (slotIdStr) {
      const slotId = parseInt(slotIdStr);
      const optionIds = selections[slotIdStr];
      if (Array.isArray(optionIds)) {
        state.selections[slotId] = optionIds.map(Number);
      }
    });

    // Hide presets and go to first step
    const wrapper = document.getElementById('presets-section-wrapper');
    if (wrapper) wrapper.classList.remove('visible');

    state.currentStep = 0;
    renderStepNav();
    renderCurrentPanel();
    renderSummary();
    updateNavButtons();

    // Dispatch event for 3D viewer integration
    document.dispatchEvent(
      new CustomEvent('configurator:selection-changed', {
        detail: { selections: JSON.parse(JSON.stringify(state.selections)), presetApplied: true },
      })
    );
  }

  // =========================================================================
  // Step Navigation
  // =========================================================================

  function renderStepNav() {
    const nav = document.getElementById('steps-nav');
    if (!nav) return;
    nav.innerHTML = '';

    state.slots.forEach(function (slot, idx) {
      const step = document.createElement('button');
      step.type = 'button';

      const isActive = idx === state.currentStep;
      const isCompleted =
        state.selections[slot.id] &&
        state.selections[slot.id].length > 0 &&
        idx !== state.currentStep;

      let cls = 'configurator-step';
      if (isActive) cls += ' configurator-step--active';
      else if (isCompleted) cls += ' configurator-step--completed';
      step.className = cls;

      const numberContent = isCompleted ? '<i class="fas fa-check"></i>' : String(idx + 1);
      const icon = slot.icon ? '<i class="' + escapeHtml(slot.icon) + '"></i> ' : '';

      step.innerHTML =
        '<span class="configurator-step__number">' +
        numberContent +
        '</span>' +
        icon +
        escapeHtml(slot.name);

      step.addEventListener('click', function () {
        state.currentStep = idx;
        renderStepNav();
        renderCurrentPanel();
        updateNavButtons();
      });

      nav.appendChild(step);
    });
  }

  // =========================================================================
  // Panel Rendering
  // =========================================================================

  function renderCurrentPanel() {
    const container = document.getElementById('panels-container');
    if (!container) return;
    container.innerHTML = '';

    if (state.slots.length === 0) {
      container.innerHTML =
        '<div class="configurator-empty">' +
        '<div class="configurator-empty__icon"><i class="fas fa-cogs"></i></div>' +
        '<p class="configurator-empty__text">No configuration options available.</p>' +
        '</div>';
      return;
    }

    const slot = state.slots[state.currentStep];
    if (!slot) return;

    const availability = getAvailableOptions(slot.id);

    const panel = document.createElement('div');
    panel.className = 'configurator-panel configurator-panel--active';

    // Header
    const header = document.createElement('div');
    header.className = 'configurator-panel__header';

    const badgeHtml = slot.is_required
      ? '<span class="configurator-panel__badge configurator-panel__badge--required">Required</span>'
      : '<span class="configurator-panel__badge configurator-panel__badge--optional">Optional</span>';

    const icon = slot.icon ? '<i class="' + escapeHtml(slot.icon) + '"></i> ' : '';

    header.innerHTML =
      '<h2 class="configurator-panel__title">' +
      icon +
      escapeHtml(slot.name) +
      badgeHtml +
      '</h2>' +
      (slot.description
        ? '<p class="configurator-panel__description">' + escapeHtml(slot.description) + '</p>'
        : '') +
      (slot.max_selections > 1
        ? '<p class="configurator-panel__selection-info">Select ' +
          slot.min_selections +
          ' to ' +
          slot.max_selections +
          ' options</p>'
        : '');

    panel.appendChild(header);

    // Options grid
    const grid = document.createElement('div');
    grid.className = 'configurator-options';

    const selectedIds = state.selections[slot.id] || [];

    (slot.options || [])
      .sort(function (a, b) {
        return a.sort_order - b.sort_order;
      })
      .forEach(function (option) {
        const isSelected = selectedIds.indexOf(option.id) !== -1;
        const isDisabled = availability.disabled.has(option.id);
        const isOutOfStock = !option.in_stock;

        const card = document.createElement('div');
        let cls = 'configurator-option';
        if (isSelected) cls += ' configurator-option--selected';
        if (isDisabled || isOutOfStock) cls += ' configurator-option--disabled';
        if (option.is_popular && !isSelected) cls += ' configurator-option--popular';
        card.className = cls;
        card.dataset.optionId = option.id;

        // Image
        let imageHtml;
        if (option.product_image) {
          imageHtml =
            '<div class="configurator-option__image"><img src="' +
            escapeHtml(option.product_image) +
            '" alt="' +
            escapeHtml(option.product_name) +
            '" loading="lazy"></div>';
        } else {
          imageHtml = '<div class="configurator-option__image"><i class="fas fa-box"></i></div>';
        }

        // Price
        let priceHtml;
        if (state.pricingStrategy === 'base_plus_adjustments') {
          const adj = parseFloat(option.effective_price) || 0;
          if (adj > 0) {
            priceHtml =
              '<div class="configurator-option__price configurator-option__price--adjustment">+' +
              formatPrice(adj) +
              '</div>';
          } else if (adj < 0) {
            priceHtml =
              '<div class="configurator-option__price configurator-option__price--adjustment">' +
              formatPrice(adj) +
              '</div>';
          } else {
            priceHtml =
              '<div class="configurator-option__price configurator-option__price--adjustment">Included</div>';
          }
        } else {
          priceHtml =
            '<div class="configurator-option__price">' +
            formatPrice(option.effective_price) +
            '</div>';
        }

        // Badges
        const badges = [];
        if (option.is_popular)
          badges.push(
            '<span class="configurator-option__badge configurator-option__badge--popular"><i class="fas fa-star"></i> Popular</span>'
          );
        if (option.is_default)
          badges.push(
            '<span class="configurator-option__badge configurator-option__badge--default">Default</span>'
          );
        if (isOutOfStock)
          badges.push(
            '<span class="configurator-option__badge configurator-option__badge--out-of-stock">Out of Stock</span>'
          );
        if (option.quantity > 1)
          badges.push(
            '<span class="configurator-option__badge configurator-option__badge--qty">&times;' +
              option.quantity +
              '</span>'
          );
        const badgesHtml =
          badges.length > 0
            ? '<div class="configurator-option__badges">' + badges.join('') + '</div>'
            : '';

        // Variant name
        const variantHtml = option.variant_name
          ? '<div class="configurator-option__variant">' +
            escapeHtml(option.variant_name) +
            '</div>'
          : '';

        card.innerHTML =
          imageHtml +
          '<div class="configurator-option__content">' +
          '<div class="configurator-option__name">' +
          escapeHtml(option.product_name) +
          '</div>' +
          variantHtml +
          priceHtml +
          badgesHtml +
          '</div>' +
          '<span class="configurator-option__check"><i class="fas fa-check"></i></span>';

        if (!isDisabled && !isOutOfStock) {
          card.addEventListener('click', function () {
            toggleOption(slot, option.id);
          });
        }

        grid.appendChild(card);
      });

    panel.appendChild(grid);
    container.appendChild(panel);
  }

  function toggleOption(slot, optionId) {
    const selected = state.selections[slot.id] || [];
    const idx = selected.indexOf(optionId);

    if (slot.max_selections === 1) {
      // Single select: replace
      if (idx !== -1) {
        state.selections[slot.id] = [];
      } else {
        state.selections[slot.id] = [optionId];
      }
    } else {
      // Multi select: toggle
      if (idx !== -1) {
        selected.splice(idx, 1);
      } else {
        if (selected.length < slot.max_selections) {
          selected.push(optionId);
        }
      }
      state.selections[slot.id] = selected;
    }

    renderStepNav();
    renderCurrentPanel();
    renderSummary();
    updateNavButtons();

    // Dispatch event for 3D viewer integration
    document.dispatchEvent(
      new CustomEvent('configurator:selection-changed', {
        detail: { selections: JSON.parse(JSON.stringify(state.selections)) },
      })
    );
  }

  // =========================================================================
  // Compatibility Engine
  // =========================================================================

  function getAvailableOptions(targetSlotId) {
    const allOptionIds = new Set();
    const slot = state.slots.find(function (s) {
      return s.id === targetSlotId;
    });
    if (slot) {
      (slot.options || []).forEach(function (o) {
        allOptionIds.add(o.id);
      });
    }

    const requiresSets = [];
    const excludesSet = new Set();

    // Iterate over all selected options in OTHER slots
    state.slots.forEach(function (s) {
      if (s.id === targetSlotId) return;
      const selected = state.selections[s.id] || [];
      selected.forEach(function (selectedOptionId) {
        // Find rules where this is the source_option targeting our slot
        state.rules.forEach(function (rule) {
          if (rule.source_option !== selectedOptionId) return;
          if (rule.target_slot !== targetSlotId) return;

          const compatIds = rule.compatible_option_ids || [];

          if (rule.rule_type === 'requires') {
            requiresSets.push(new Set(compatIds));
          } else if (rule.rule_type === 'excludes') {
            compatIds.forEach(function (id) {
              excludesSet.add(id);
            });
          }
        });
      });
    });

    // Compute available: start with all, intersect requires, subtract excludes
    let available = new Set(allOptionIds);

    if (requiresSets.length > 0) {
      // Intersect all requires sets
      let intersection = new Set(requiresSets[0]);
      for (var i = 1; i < requiresSets.length; i++) {
        intersection = new Set(
          Array.from(intersection).filter(function (id) {
            return requiresSets[i].has(id);
          })
        );
      }
      available = new Set(
        Array.from(available).filter(function (id) {
          return intersection.has(id);
        })
      );
    }

    // Remove excludes
    excludesSet.forEach(function (id) {
      available.delete(id);
    });

    // Build disabled set
    const disabled = new Set();
    allOptionIds.forEach(function (id) {
      if (!available.has(id)) disabled.add(id);
    });

    return { available: available, disabled: disabled };
  }

  // =========================================================================
  // Pricing
  // =========================================================================

  function calculatePrice() {
    let total = 0;

    if (state.pricingStrategy === 'fixed') {
      return state.basePrice;
    }

    if (state.pricingStrategy === 'base_plus_adjustments') {
      total = state.basePrice;
    }

    state.slots.forEach(function (slot) {
      const selected = state.selections[slot.id] || [];
      selected.forEach(function (optionId) {
        const option = findOption(slot.id, optionId);
        if (!option) return;
        const price = parseFloat(option.effective_price) || 0;
        total += price * (option.quantity || 1);
      });
    });

    return total;
  }

  function findOption(slotId, optionId) {
    const slot = state.slots.find(function (s) {
      return s.id === slotId;
    });
    if (!slot) return null;
    return (slot.options || []).find(function (o) {
      return o.id === optionId;
    });
  }

  function formatPrice(amount) {
    const num = parseFloat(amount) || 0;
    return state.currency + ' ' + num.toFixed(2);
  }

  // =========================================================================
  // Summary
  // =========================================================================

  function renderSummary() {
    const slotsContainer = document.getElementById('summary-slots');
    if (slotsContainer) {
      slotsContainer.innerHTML = '';
      state.slots.forEach(function (slot) {
        const div = document.createElement('div');
        div.className = 'configurator-summary__slot';

        const selected = state.selections[slot.id] || [];
        const names = [];
        let slotPrice = 0;

        selected.forEach(function (optionId) {
          const option = findOption(slot.id, optionId);
          if (option) {
            names.push(option.product_name);
            slotPrice += (parseFloat(option.effective_price) || 0) * (option.quantity || 1);
          }
        });

        const valueText = names.length > 0 ? names.join(', ') : '\u2014';
        const valueCls =
          'configurator-summary__slot-value' +
          (names.length === 0 ? ' configurator-summary__slot-value--empty' : '');
        const priceStr =
          names.length > 0
            ? '<div class="configurator-summary__slot-price">' + formatPrice(slotPrice) + '</div>'
            : '';

        div.innerHTML =
          '<span class="configurator-summary__slot-name">' +
          escapeHtml(slot.name) +
          '</span>' +
          '<span class="' +
          valueCls +
          '">' +
          escapeHtml(valueText) +
          priceStr +
          '</span>';

        slotsContainer.appendChild(div);
      });
    }

    // Update totals
    const total = calculatePrice();
    const totalStr = formatPrice(total);

    const summaryTotal = document.getElementById('summary-total');
    if (summaryTotal) summaryTotal.textContent = totalStr;

    const mobileTotal = document.getElementById('mobile-total');
    if (mobileTotal) mobileTotal.textContent = totalStr;

    const sheetTotal = document.getElementById('sheet-total');
    if (sheetTotal) sheetTotal.textContent = totalStr;
  }

  // =========================================================================
  // Navigation
  // =========================================================================

  function updateNavButtons() {
    const backBtn = document.getElementById('btn-back');
    const nextBtn = document.getElementById('btn-next');
    const addBtn = document.getElementById('btn-add-to-cart');

    const isFirst = state.currentStep === 0;
    const isLast = state.currentStep === state.slots.length - 1;

    if (backBtn) backBtn.classList.toggle('btn--hidden', isFirst);
    if (nextBtn) nextBtn.classList.toggle('btn--hidden', isLast);
    if (addBtn) addBtn.classList.toggle('btn--hidden', !isLast);
  }

  // Back button
  const backBtn = document.getElementById('btn-back');
  if (backBtn) {
    backBtn.addEventListener('click', function () {
      if (state.currentStep > 0) {
        state.currentStep--;
        renderStepNav();
        renderCurrentPanel();
        updateNavButtons();
        scrollToWizard();
      }
    });
  }

  // Next button
  const nextBtn = document.getElementById('btn-next');
  if (nextBtn) {
    nextBtn.addEventListener('click', function () {
      // Validate current slot before proceeding
      const slot = state.slots[state.currentStep];
      if (slot && slot.is_required) {
        const selected = state.selections[slot.id] || [];
        if (selected.length < slot.min_selections) {
          showError(
            'Please select at least ' + slot.min_selections + ' option(s) for "' + slot.name + '"'
          );
          return;
        }
      }

      if (state.currentStep < state.slots.length - 1) {
        state.currentStep++;
        renderStepNav();
        renderCurrentPanel();
        updateNavButtons();
        scrollToWizard();
      }
    });
  }

  // Add to Cart buttons (main, summary, mobile)
  ['btn-add-to-cart', 'summary-add-to-cart', 'mobile-add-to-cart', 'sheet-add-to-cart'].forEach(
    function (id) {
      const btn = document.getElementById(id);
      if (btn) {
        btn.addEventListener('click', function () {
          addToCart(btn);
        });
      }
    }
  );

  // =========================================================================
  // Add to Cart
  // =========================================================================

  function addToCart(triggerBtn) {
    // Build configuration payload: { slot_id_str: [option_ids] }
    const configuration = {};
    let hasSelections = false;
    state.slots.forEach(function (slot) {
      const selected = state.selections[slot.id] || [];
      configuration[String(slot.id)] = selected;
      if (selected.length > 0) hasSelections = true;
    });

    if (!hasSelections) {
      showError('Please select at least one option before adding to cart.');
      return;
    }

    // Disable all add-to-cart buttons and show loading
    const allBtns = ['btn-add-to-cart', 'summary-add-to-cart', 'mobile-add-to-cart'];
    const originalContents = {};
    allBtns.forEach(function (id) {
      const btn = document.getElementById(id);
      if (btn) {
        originalContents[id] = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> <span>Adding...</span>';
        btn.disabled = true;
      }
    });

    const csrfToken = getCsrf();

    fetch('/api/cart/add/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify({
        product_id: state.productId,
        quantity: 1,
        configuration: configuration,
        preset_id: state.presetId,
      }),
    })
      .then(function (resp) {
        return resp.json();
      })
      .then(function (data) {
        if (data.success) {
          // Update cart count in header
          const cartCount = document.querySelector('.header__cart-count');
          if (cartCount) {
            cartCount.textContent = data.cart_count;
            cartCount.style.display = 'flex';
          }

          // Open mini-cart
          if (typeof openMiniCart === 'function') {
            openMiniCart(data);
          } else if (window.MiniCart) {
            window.MiniCart.open(data);
          }

          // Success state
          allBtns.forEach(function (id) {
            const btn = document.getElementById(id);
            if (btn) {
              btn.innerHTML = '<i class="fas fa-check"></i> <span>Added!</span>';
            }
          });

          if (typeof showNotification === 'function') {
            showNotification('Configuration added to cart!', 'success');
          }

          setTimeout(function () {
            allBtns.forEach(function (id) {
              const btn = document.getElementById(id);
              if (btn) {
                btn.innerHTML = originalContents[id];
                btn.disabled = false;
              }
            });
          }, 2000);
        } else {
          // Error
          const msg = data.message || data.error || 'Error adding to cart';
          showError(msg);
          allBtns.forEach(function (id) {
            const btn = document.getElementById(id);
            if (btn) {
              btn.innerHTML = originalContents[id];
              btn.disabled = false;
            }
          });
        }
      })
      .catch(function (err) {
        console.error('Add to cart error:', err);
        showError('Network error. Please try again.');
        allBtns.forEach(function (id) {
          const btn = document.getElementById(id);
          if (btn) {
            btn.innerHTML = originalContents[id];
            btn.disabled = false;
          }
        });
      });
  }

  // =========================================================================
  // Utilities
  // =========================================================================

  function getCsrf() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    if (meta && meta.content) return meta.content;
    const el = document.querySelector('[name=csrfmiddlewaretoken]');
    return el ? el.value : '';
  }

  function escapeHtml(str) {
    if (!str) return '';
    const div = document.createElement('div');
    div.textContent = String(str);
    return div.innerHTML;
  }

  function scrollToWizard() {
    // On mobile with bottom sheet active, snap the sheet instead of scrolling
    if (window.__configuratorScrollOverride) {
      window.__configuratorScrollOverride();
      return;
    }
    const nav = document.getElementById('steps-nav');
    if (nav) {
      nav.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  function showError(msg) {
    // Remove existing errors
    const existing = document.querySelectorAll('.configurator-error');
    existing.forEach(function (el) {
      el.remove();
    });

    const container = document.getElementById('panels-container');
    if (!container) return;

    const errorDiv = document.createElement('div');
    errorDiv.className = 'configurator-error';
    errorDiv.innerHTML = '<i class="fas fa-exclamation-circle"></i> ' + escapeHtml(msg);

    container.parentNode.insertBefore(errorDiv, container);

    setTimeout(function () {
      if (errorDiv.parentNode) errorDiv.remove();
    }, 5000);
  }
});
