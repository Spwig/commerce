/* Promotion Change Form - Product selector, wizard navigation, discount UI */
(function () {
  'use strict';

  // Read translations from JSON data island
  let t = {};
  (function () {
    const el = document.getElementById('promotion-change-form-i18n');
    if (el) {
      try {
        const data = JSON.parse(el.textContent);
        t = data.i18n || {};
      } catch (e) {
        console.error('Failed to parse promotion form translations:', e);
      }
    }
  })();

  class PromotionSelector {
    constructor(type) {
      this.type = type;
      this.availableList = document.getElementById(`${type}-available`);
      this.selectedList = document.getElementById(`${type}-selected`);
      this.searchInput = document.getElementById(`${type}-search`);
      this.hiddenInput = document.getElementById(`hidden-${type}`);
      this.container = document.getElementById(`${type}-selector`);
      this.moveBtn = document.getElementById(`${type}-move-btn`);

      this.availableItems = [];
      this.selectedItems = [];
      this.sortableAvailable = null;
      this.sortableSelected = null;
      this.lastSelectedIndex = null;
      this.selectedCount = 0;

      this.init();
    }

    async init() {
      await this.loadItems();
      this.initSortable();
      if (this.searchInput) {
        this.searchInput.addEventListener('input', () => this.handleSearch());
      }
      if (this.moveBtn) {
        this.moveBtn.addEventListener('click', () => this.moveSelectedItems());
      }
      this.setupMultiSelect();
      this.renderAvailable();
      this.renderSelected();
    }

    async loadItems() {
      try {
        const response = await fetch(`/admin/catalog/promotion/selector-data/${this.type}/`);
        if (!response.ok) throw new Error('Failed to load items');

        const data = await response.json();
        this.availableItems = data.items || [];

        const hiddenValue = this.hiddenInput.value;
        if (hiddenValue) {
          const selectedIds = hiddenValue.split(',').filter(id => id);
          this.selectedItems = this.availableItems.filter(item =>
            selectedIds.includes(item.id.toString())
          );
          this.availableItems = this.availableItems.filter(
            item => !selectedIds.includes(item.id.toString())
          );
        }
      } catch (error) {
        console.error('Error loading items:', error);
        this.showError();
      }
    }

    initSortable() {
      const commonOptions = {
        animation: 150,
        ghostClass: 'sortable-ghost',
        group: this.type,
        onEnd: () => {
          this.updateHiddenInput();
          this.removeEmptyStateIfNeeded();
        },
      };

      this.sortableAvailable = Sortable.create(this.availableList, {
        ...commonOptions,
        sort: false,
      });

      this.sortableSelected = Sortable.create(this.selectedList, commonOptions);
    }

    removeEmptyStateIfNeeded() {
      const emptyState = this.selectedList.querySelector('.selector-empty');
      const actualItems = this.selectedList.querySelectorAll('.selector-item');
      if (emptyState && actualItems.length > 0) {
        emptyState.remove();
      }
    }

    createItemHTML(item) {
      const hasImage = item.thumbnail || item.image;
      const fallbackIcons = {
        categories: 'fa-folder',
        brands: 'fa-copyright',
        collections: 'fa-layer-group',
        products: 'fa-box',
      };

      return `
                <div class="selector-item" data-id="${item.id}" data-name="${item.name.toLowerCase()}">
                    ${
                      hasImage
                        ? `<img src="${item.thumbnail || item.image}" alt="${item.name}" class="item-thumbnail" data-has-fallback>
                         <div class="item-icon" style="display:none;"><i class="fas ${fallbackIcons[this.type]}"></i></div>`
                        : `<div class="item-icon"><i class="fas ${fallbackIcons[this.type]}"></i></div>`
                    }
                    <div class="item-info">
                        <div class="item-name">${item.name}</div>
                        ${item.meta ? `<div class="item-meta">${item.meta}</div>` : ''}
                    </div>
                    <i class="fas fa-grip-vertical drag-handle"></i>
                </div>
            `;
    }

    _attachImageFallbacks(container) {
      container.querySelectorAll('img.item-thumbnail[data-has-fallback]').forEach(function (img) {
        img.addEventListener('error', function () {
          this.style.display = 'none';
          if (this.nextElementSibling) {
            this.nextElementSibling.style.display = 'flex';
          }
        });
      });
    }

    renderAvailable() {
      if (this.availableItems.length === 0) {
        this.availableList.innerHTML = `
                    <div class="selector-empty">
                        <i class="fas fa-inbox"></i>
                        <div>${t.noItemsAvailable}</div>
                    </div>
                `;
        return;
      }

      this.availableList.innerHTML = this.availableItems
        .map(item => this.createItemHTML(item))
        .join('');
      this._attachImageFallbacks(this.availableList);
    }

    renderSelected() {
      if (this.selectedItems.length === 0) {
        this.selectedList.innerHTML = `
                    <div class="selector-empty">
                        <i class="fas fa-hand-pointer"></i>
                        <div>${t.dragItemsHere}</div>
                    </div>
                `;
        return;
      }

      this.selectedList.innerHTML = this.selectedItems
        .map(item => this.createItemHTML(item))
        .join('');
      this._attachImageFallbacks(this.selectedList);
      this.updateHiddenInput();
    }

    handleSearch() {
      const query = this.searchInput.value.toLowerCase().trim();
      const items = this.availableList.querySelectorAll('.selector-item');

      items.forEach(item => {
        const name = item.dataset.name;
        item.style.display = name.includes(query) ? 'flex' : 'none';
      });
    }

    updateHiddenInput() {
      const selectedElements = this.selectedList.querySelectorAll('.selector-item');
      const ids = Array.from(selectedElements).map(el => el.dataset.id);
      this.hiddenInput.value = ids.join(',');
    }

    setupMultiSelect() {
      this.availableList.addEventListener('click', e => {
        const item = e.target.closest('.selector-item');
        if (!item) return;

        const items = Array.from(this.availableList.querySelectorAll('.selector-item'));
        const currentIndex = items.indexOf(item);

        if (e.ctrlKey || e.metaKey) {
          this.toggleItemSelection(item);
        } else if (e.shiftKey && this.lastSelectedIndex !== null) {
          this.selectRange(items, this.lastSelectedIndex, currentIndex);
        } else {
          this.clearSelection();
          this.toggleItemSelection(item);
        }

        this.lastSelectedIndex = currentIndex;
        this.updateMoveButton();
      });

      this.availableList.addEventListener('click', e => {
        if (e.target === this.availableList) {
          this.clearSelection();
          this.updateMoveButton();
        }
      });
    }

    toggleItemSelection(item) {
      item.classList.toggle('selected');
      this.selectedCount += item.classList.contains('selected') ? 1 : -1;
    }

    selectRange(items, startIndex, endIndex) {
      const start = Math.min(startIndex, endIndex);
      const end = Math.max(startIndex, endIndex);

      for (let i = start; i <= end; i++) {
        if (!items[i].classList.contains('selected')) {
          items[i].classList.add('selected');
          this.selectedCount++;
        }
      }
    }

    clearSelection() {
      this.availableList.querySelectorAll('.selector-item.selected').forEach(item => {
        item.classList.remove('selected');
      });
      this.selectedCount = 0;
      this.lastSelectedIndex = null;
    }

    updateMoveButton() {
      if (this.moveBtn) {
        this.moveBtn.disabled = this.selectedCount === 0;
      }
    }

    moveSelectedItems() {
      const selectedItems = Array.from(
        this.availableList.querySelectorAll('.selector-item.selected')
      );
      if (selectedItems.length === 0) return;

      selectedItems.forEach(item => {
        item.classList.remove('selected');
        this.selectedList.appendChild(item);
      });

      this.selectedCount = 0;
      this.lastSelectedIndex = null;
      this.updateMoveButton();
      this.removeEmptyStateIfNeeded();
      this.updateHiddenInput();
    }

    showError() {
      this.availableList.innerHTML = `
                <div class="selector-empty">
                    <i class="fas fa-exclamation-triangle"></i>
                    <div>${t.errorLoadingItems}</div>
                </div>
            `;
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('wizard-form');
    const steps = document.querySelectorAll('.wizard-step');
    const stepIndicators = document.querySelectorAll('.wizard-steps .step');
    const btnPrev = document.getElementById('btn-prev');
    const btnNext = document.getElementById('btn-next');
    const btnSave = document.getElementById('btn-save');

    let currentStep = 1;
    const totalSteps = 5;

    function showStep(step) {
      steps.forEach(s => (s.style.display = 'none'));
      document.querySelector(`.wizard-step[data-step="${step}"]`).style.display = 'block';

      stepIndicators.forEach((indicator, index) => {
        indicator.classList.remove('active', 'completed');
        if (index + 1 < step) {
          indicator.classList.add('completed');
        } else if (index + 1 === step) {
          indicator.classList.add('active');
        }
      });

      btnPrev.style.display = step > 1 ? 'inline-flex' : 'none';
      btnNext.style.display = step < totalSteps ? 'inline-flex' : 'none';
      btnSave.style.display = step === totalSteps ? 'inline-flex' : 'none';

      if (step === totalSteps) {
        updateReview();
      }
    }

    function validateStep(step) {
      let isValid = true;

      if (step === 1) {
        const name = document.getElementById('id_name').value.trim();
        if (!name) {
          showError('name', t.nameRequired);
          isValid = false;
        } else {
          clearError('name');
        }
      }

      if (step === 2) {
        const discountValue = document.getElementById('id_discount_value').value;
        const discountType = document.querySelector('input[name="discount_type"]:checked').value;

        if (!discountValue || parseFloat(discountValue) <= 0) {
          showError('discount_value', t.invalidDiscount);
          isValid = false;
        } else if (discountType === 'percentage_off' && parseFloat(discountValue) > 100) {
          showError('discount_value', t.percentageExceeds100);
          isValid = false;
        } else {
          clearError('discount_value');
        }
      }

      if (step === 3) {
        const startDate = document.getElementById('id_start_date').value;
        if (!startDate) {
          showError('start_date', t.startDateRequired);
          isValid = false;
        } else {
          clearError('start_date');
        }
      }

      return isValid;
    }

    function showError(field, message) {
      const errorEl = document.getElementById(`${field}-error`);
      if (errorEl) {
        errorEl.textContent = message;
        errorEl.style.display = 'block';
      }
      const input = document.getElementById(`id_${field}`);
      if (input) input.classList.add('error');
    }

    function clearError(field) {
      const errorEl = document.getElementById(`${field}-error`);
      if (errorEl) {
        errorEl.textContent = '';
        errorEl.style.display = 'none';
      }
      const input = document.getElementById(`id_${field}`);
      if (input) input.classList.remove('error');
    }

    btnNext.addEventListener('click', function () {
      if (validateStep(currentStep)) {
        currentStep++;
        showStep(currentStep);
      }
    });

    btnPrev.addEventListener('click', function () {
      currentStep--;
      showStep(currentStep);
    });

    const discountCards = document.querySelectorAll('.discount-type-card');
    discountCards.forEach(card => {
      card.addEventListener('click', function () {
        discountCards.forEach(c => c.classList.remove('selected'));
        this.classList.add('selected');
        this.querySelector('input[type="radio"]').checked = true;
        updateDiscountUI();
      });
    });

    function updateDiscountUI() {
      const type = document.querySelector('input[name="discount_type"]:checked').value;
      const prefix = document.getElementById('discount-prefix');
      const suffix = document.getElementById('discount-suffix');
      const help = document.getElementById('discount-help');
      const label = document.getElementById('discount-value-label');

      if (type === 'percentage_off') {
        prefix.style.display = 'none';
        suffix.style.display = 'flex';
        suffix.textContent = '%';
        help.textContent = t.enterPercentageOff;
        label.textContent = t.discountPercentageLabel;
      } else if (type === 'amount_off') {
        prefix.style.display = 'flex';
        prefix.textContent = '$';
        suffix.style.display = 'none';
        help.textContent = t.enterAmountOff;
        label.textContent = t.discountAmountLabel;
      } else {
        prefix.style.display = 'flex';
        prefix.textContent = '$';
        suffix.style.display = 'none';
        help.textContent = t.enterFixedPrice;
        label.textContent = t.salePriceLabel;
      }
      updateDiscountPreview();
    }

    function updateDiscountPreview() {
      const type = document.querySelector('input[name="discount_type"]:checked').value;
      const value = parseFloat(document.getElementById('id_discount_value').value) || 0;
      const displayEl = document.getElementById('discount-display');
      const labelEl = document.getElementById('discount-type-label');
      const exampleEl = document.getElementById('example-price');

      if (value <= 0) {
        displayEl.textContent = '?';
        labelEl.textContent = t.previewWillAppear;
        exampleEl.textContent = '$?';
        return;
      }

      let displayText, labelText, examplePrice;
      const samplePrice = 100;

      switch (type) {
        case 'percentage_off':
          displayText = value + '% OFF';
          labelText = t.percentageOff;
          examplePrice = (samplePrice * (1 - value / 100)).toFixed(2);
          break;
        case 'amount_off':
          displayText = '$' + value.toFixed(2) + ' OFF';
          labelText = t.amountOff;
          examplePrice = Math.max(0, samplePrice - value).toFixed(2);
          break;
        case 'fixed_price':
          displayText = '$' + value.toFixed(2);
          labelText = t.fixedSalePrice;
          examplePrice = value.toFixed(2);
          break;
      }

      displayEl.textContent = displayText;
      labelEl.textContent = labelText;
      exampleEl.textContent = '$' + examplePrice;
    }

    document.getElementById('id_discount_value').addEventListener('input', updateDiscountPreview);

    const targetCards = document.querySelectorAll('.target-type-card');
    targetCards.forEach(card => {
      card.addEventListener('click', function () {
        targetCards.forEach(c => c.classList.remove('selected'));
        this.classList.add('selected');
        this.querySelector('input[type="radio"]').checked = true;
        showSelector(this.dataset.type);
      });
    });

    const selectors = {
      categories: null,
      brands: null,
      collections: null,
      products: null,
    };

    function showSelector(type) {
      document.querySelectorAll('.selector-container').forEach(container => {
        container.style.display = 'none';
      });

      if (type !== 'all') {
        const container = document.getElementById(`${type}-selector`);
        if (container) {
          container.style.display = 'block';
          if (!selectors[type]) {
            selectors[type] = new PromotionSelector(type);
          }
        }
      }
    }

    const initialApplyTo = document.querySelector('input[name="apply_to"]:checked');
    if (initialApplyTo) {
      showSelector(initialApplyTo.value);
    }

    const advancedToggle = document.getElementById('advanced-toggle');
    const advancedSettings = document.getElementById('advanced-settings');

    advancedToggle.addEventListener('click', function () {
      this.classList.toggle('expanded');
      advancedSettings.classList.toggle('show');
    });

    function updateReview() {
      document.getElementById('review-name').textContent =
        document.getElementById('id_name').value || '-';
      const isActive = document.getElementById('id_is_active').checked;
      document.getElementById('review-status').textContent = isActive ? t.active : t.inactive;

      const discountType = document.querySelector('input[name="discount_type"]:checked').value;
      const discountTypeLabels = {
        percentage_off: t.percentageOff,
        amount_off: t.amountOff,
        fixed_price: t.fixedSalePrice,
      };
      document.getElementById('review-discount-type').textContent =
        discountTypeLabels[discountType] || '-';

      const discountValue = document.getElementById('id_discount_value').value;
      let discountDisplay = '-';
      if (discountValue) {
        if (discountType === 'percentage_off') {
          discountDisplay = discountValue + '%';
        } else {
          discountDisplay = '$' + parseFloat(discountValue).toFixed(2);
        }
      }
      document.getElementById('review-discount-value').textContent = discountDisplay;

      const startDate = document.getElementById('id_start_date').value;
      document.getElementById('review-start-date').textContent = startDate
        ? new Date(startDate).toLocaleDateString()
        : '-';

      const endDate = document.getElementById('id_end_date').value;
      document.getElementById('review-end-date').textContent = endDate
        ? new Date(endDate).toLocaleDateString()
        : t.noEndDate;

      const applyTo = document.querySelector('input[name="apply_to"]:checked').value;
      const applyToLabels = {
        all: t.allProducts,
        categories: t.specificCategories,
        brands: t.specificBrands,
        collections: t.specificCollections,
        products: t.specificProducts,
      };
      document.getElementById('review-apply-to').textContent = applyToLabels[applyTo] || '-';

      let selectionText = '-';
      if (applyTo === 'all') {
        selectionText = t.storeWide;
      } else {
        const hiddenInput = document.getElementById(`hidden-${applyTo}`);
        if (hiddenInput && hiddenInput.value) {
          const count = hiddenInput.value.split(',').filter(id => id).length;
          selectionText = count + ' ' + t.selected;
        } else {
          selectionText = t.noneSelected;
        }
      }
      document.getElementById('review-selection').textContent = selectionText;
    }

    form.addEventListener('submit', function (e) {
      for (let i = 1; i <= totalSteps; i++) {
        if (!validateStep(i)) {
          e.preventDefault();
          currentStep = i;
          showStep(currentStep);
          return;
        }
      }
    });

    showStep(1);
    updateDiscountUI();
  });
})();
