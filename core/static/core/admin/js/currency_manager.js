/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Multi-Currency Drag-and-Drop Manager
 *
 * Handles the two-column currency selection interface with drag-and-drop
 * functionality using SortableJS library.
 */

class CurrencyManager {
    constructor() {
        this.availableCurrencies = [];
        this.activeCurrencies = [];
        this.originalActiveCurrencies = [];
        this.defaultCurrency = null;

        this.availableContainer = document.getElementById('available-currencies');
        this.activeContainer = document.getElementById('active-currencies');
        this.searchInput = document.getElementById('currency-search');

        if (this.availableContainer && this.activeContainer) {
            this.init();
        }
    }

    async init() {
        try {
            // Get default currency from the form
            const defaultCurrencySelect = document.querySelector('select[name="default_currency"]');
            if (defaultCurrencySelect) {
                this.defaultCurrency = defaultCurrencySelect.value;
            }

            await this.loadCurrencies();
            this.setupSortable();
            this.setupEventListeners();
            this.renderCurrencies();
        } catch (error) {
            console.error('Currency manager error:', error);
            this.showError('Failed to initialize currency manager: ' + error.message);
        }
    }

    async loadCurrencies() {
        try {
            console.log('Fetching currencies from /api/currencies/...');
            const response = await fetch('/api/currencies/');
            console.log('Response status:', response.status);

            if (!response.ok) {
                const errorText = await response.text();
                console.error('API error response:', errorText);
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const data = await response.json();
            console.log('API response:', data);

            if (!data.success) {
                throw new Error(data.error || 'Unknown error');
            }

            console.log(`Loaded ${data.total} currencies (${data.active_count} active)`);

            // Separate currencies and mark default as protected
            this.availableCurrencies = data.currencies.filter(c => !c.is_active);
            this.activeCurrencies = data.currencies.filter(c => c.is_active);

            // Mark default currency as protected
            this.activeCurrencies.forEach(c => {
                if (c.code === this.defaultCurrency) {
                    c.protected = true;
                }
            });

            this.originalActiveCurrencies = JSON.parse(JSON.stringify(this.activeCurrencies));

            console.log(`Available: ${this.availableCurrencies.length}, Active: ${this.activeCurrencies.length}`);
        } catch (error) {
            console.error('Failed to load currencies:', error);
            // Show error in UI
            this.availableContainer.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-exclamation-triangle" style="color: var(--error-fg);"></i>
                    <p style="color: var(--error-fg);">Failed to load currencies</p>
                    <p style="font-size: 12px;">${error.message}</p>
                </div>
            `;
            throw error;
        }
    }

    setupSortable() {
        // Available currencies - can drag to active
        new Sortable(this.availableContainer, {
            group: {
                name: 'currencies',
                pull: 'clone',
                put: false
            },
            sort: false,
            animation: 150,
            onStart: (evt) => evt.item.classList.add('dragging'),
            onEnd: (evt) => evt.item.classList.remove('dragging')
        });

        // Active currencies - can reorder and remove
        new Sortable(this.activeContainer, {
            group: {
                name: 'currencies',
                pull: false,
                put: true
            },
            animation: 150,
            handle: '.drag-handle',
            onAdd: (evt) => {
                const code = evt.item.dataset.code;
                this.activateCurrency(code);
                this.renderCurrencies();
            },
            onUpdate: () => this.updateCurrencyOrder()
        });
    }

    setupEventListeners() {
        // Search
        this.searchInput.addEventListener('input', (e) => {
            clearTimeout(this.searchTimeout);
            this.searchTimeout = setTimeout(() => {
                this.filterCurrencies(e.target.value);
            }, 300);
        });

        // Save
        document.getElementById('save-currencies').addEventListener('click', () => {
            this.saveCurrencies();
        });

        // Reset
        document.getElementById('reset-currencies').addEventListener('click', () => {
            this.resetCurrencies();
        });

        // Remove button
        this.activeContainer.addEventListener('click', (e) => {
            if (e.target.closest('.remove-btn')) {
                const item = e.target.closest('.currency-item');
                const code = item.dataset.code;
                this.deactivateCurrency(code);
            }
        });
    }

    renderCurrencies() {
        // Render available
        this.availableContainer.innerHTML = '';
        if (this.availableCurrencies.length === 0) {
            this.availableContainer.innerHTML = '<div class="empty-state"><i class="fas fa-check-circle"></i><p>All currencies are active</p></div>';
        } else {
            this.availableCurrencies.forEach(curr => {
                this.availableContainer.appendChild(this.createCurrencyItem(curr, false));
            });
        }

        // Render active
        this.activeContainer.innerHTML = '';
        if (this.activeCurrencies.length === 0) {
            this.activeContainer.innerHTML = '<div class="empty-state"><i class="fas fa-info-circle"></i><p>No active currencies. Drag currencies from the left to activate them.</p></div>';
        } else {
            this.activeCurrencies.forEach(curr => {
                this.activeContainer.appendChild(this.createCurrencyItem(curr, true));
            });
        }

        // Update counts
        document.getElementById('available-count').textContent = `(${this.availableCurrencies.length})`;
        document.getElementById('active-count').textContent = `(${this.activeCurrencies.length})`;
    }

    createCurrencyItem(currency, isActive) {
        const item = document.createElement('div');
        item.className = 'currency-item' + (isActive ? ' active' : '');
        if (currency.protected) {
            item.className += ' protected';
        }
        item.dataset.code = currency.code;
        item.dataset.name = currency.name;
        if (isActive) item.dataset.order = currency.order;

        let html = '';
        if (isActive) {
            html += '<span class="drag-handle"><i class="fas fa-grip-vertical"></i></span>';
        }

        html += `
            <span class="currency-icon">
                ${currency.flag ? `<img src="${currency.flag}" alt="${currency.code}" class="currency-flag">` : '<span class="currency-placeholder">' + currency.code.substring(0,2) + '</span>'}
            </span>
            <div class="currency-info">
                <div class="currency-code">${currency.code}</div>
                <div class="currency-name">${currency.name}</div>
            </div>
        `;

        if (isActive) {
            if (currency.protected) {
                html += '<span class="protected-badge">Default</span>';
            } else {
                html += '<button type="button" class="remove-btn" title="Deactivate"><i class="fas fa-times"></i></button>';
            }
        }

        item.innerHTML = html;
        return item;
    }

    filterCurrencies(searchTerm) {
        const term = searchTerm.toLowerCase().trim();
        if (!term) {
            this.renderCurrencies();
            return;
        }

        const items = this.availableContainer.querySelectorAll('.currency-item');
        items.forEach(item => {
            const code = item.dataset.code.toLowerCase();
            const name = item.dataset.name.toLowerCase();
            item.style.display = (code.includes(term) || name.includes(term)) ? '' : 'none';
        });
    }

    activateCurrency(code) {
        const index = this.availableCurrencies.findIndex(c => c.code === code);
        if (index !== -1) {
            const currency = this.availableCurrencies.splice(index, 1)[0];
            currency.is_active = true;
            currency.order = this.activeCurrencies.length;
            this.activeCurrencies.push(currency);
        }
        this.showSuccess(`${code} activated`);
    }

    deactivateCurrency(code) {
        const index = this.activeCurrencies.findIndex(c => c.code === code);
        if (index !== -1) {
            const currency = this.activeCurrencies[index];

            // Prevent removing protected (default) currency
            if (currency.protected) {
                this.showError(`Cannot deactivate ${code} - it is the default currency. Change the default currency in the Locale tab first.`);
                return;
            }

            this.activeCurrencies.splice(index, 1);
            currency.is_active = false;
            this.availableCurrencies.push(currency);
            this.availableCurrencies.sort((a, b) => a.code.localeCompare(b.code));
            this.showSuccess(`${code} deactivated`);
        }
        this.renderCurrencies();
    }

    updateCurrencyOrder() {
        const items = this.activeContainer.querySelectorAll('.currency-item');
        const newOrder = [];
        items.forEach((item, index) => {
            const code = item.dataset.code;
            const currency = this.activeCurrencies.find(c => c.code === code);
            if (currency) {
                currency.order = index;
                newOrder.push(currency);
            }
        });
        this.activeCurrencies = newOrder;
    }

    async saveCurrencies() {
        const saveBtn = document.getElementById('save-currencies');
        saveBtn.disabled = true;
        saveBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';

        try {
            // Reorder
            const activeCodes = this.activeCurrencies.map(c => c.code);
            await this.apiCall('/api/currencies/reorder/', 'POST', { codes: activeCodes });

            // Activate
            if (activeCodes.length > 0) {
                await this.apiCall('/api/currencies/activate/', 'POST', { codes: activeCodes });
            }

            // Deactivate
            const allCodes = [...this.availableCurrencies, ...this.activeCurrencies].map(c => c.code);
            const deactivateCodes = allCodes.filter(code => !activeCodes.includes(code));
            if (deactivateCodes.length > 0) {
                await this.apiCall('/api/currencies/deactivate/', 'POST', { codes: deactivateCodes });
            }

            this.originalActiveCurrencies = JSON.parse(JSON.stringify(this.activeCurrencies));
            this.showSuccess('Currency configuration saved successfully');

        } catch (error) {
            this.showError('Failed to save currencies: ' + error.message);
        } finally {
            saveBtn.disabled = false;
            saveBtn.innerHTML = '<i class="fas fa-save"></i> Save Currency Configuration';
        }
    }

    async resetCurrencies() {
        if (await AdminModal.confirm({
            message: 'Reset to last saved configuration?',
            danger: true,
            confirmText: 'Reset'
        })) {
            this.activeCurrencies = JSON.parse(JSON.stringify(this.originalActiveCurrencies));
            this.loadCurrencies().then(() => {
                this.renderCurrencies();
                this.showSuccess('Configuration reset');
            });
        }
    }

    async apiCall(url, method, body) {
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCsrfToken()
            },
            body: JSON.stringify(body)
        });

        if (!response.ok) {
            throw new Error('API request failed');
        }

        const data = await response.json();
        if (!data.success) {
            throw new Error(data.error || 'Unknown error');
        }

        return data;
    }

    getCsrfToken() {
        return AdminUtils.getCsrfToken();
    }

    showSuccess(message) {
        this.showMessage(message, 'success');
    }

    showError(message) {
        this.showMessage(message, 'error');
    }

    showMessage(message, type) {
        let messagesDiv = document.querySelector('.messagelist');
        if (!messagesDiv) {
            messagesDiv = document.createElement('ul');
            messagesDiv.className = 'messagelist';
            document.querySelector('.content').insertBefore(messagesDiv, document.querySelector('.content').firstChild);
        }

        const messageItem = document.createElement('li');
        messageItem.className = type;
        messageItem.textContent = message;
        messagesDiv.appendChild(messageItem);

        setTimeout(() => messageItem.remove(), 5000);
    }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('Currency manager: DOM ready');

    const availableContainer = document.getElementById('available-currencies');
    const activeContainer = document.getElementById('active-currencies');
    console.log('Containers found:', {
        available: !!availableContainer,
        active: !!activeContainer
    });

    // Initialize if both containers exist
    if (availableContainer && activeContainer) {
        console.log('Initializing currency manager...');
        window.currencyManager = new CurrencyManager();
    } else {
        console.log('Currency containers not found, skipping initialization');
    }
});
