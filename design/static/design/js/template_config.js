/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Page Template Configuration Admin UI
 * Card selection, option rendering, trust badge editor, and AJAX save.
 */
(function() {
    'use strict';

    const container = document.getElementById('template-config');
    if (!container) return;

    const saveUrl = container.dataset.saveUrl;
    let checkoutCards = JSON.parse(container.dataset.checkoutCards || '[]');
    let productCards = JSON.parse(container.dataset.productCards || '[]');
    let categoryCards = JSON.parse(container.dataset.categoryCards || '[]');
    let blogPostCards = JSON.parse(container.dataset.blogPostCards || '[]');
    let blogListCards = JSON.parse(container.dataset.blogListCards || '[]');

    let selectedCheckout = container.dataset.currentCheckout;
    let selectedProduct = container.dataset.currentProduct;
    let selectedCategory = container.dataset.currentCategory || 'grid';
    let selectedBlogPost = container.dataset.currentBlogPost || 'classic';
    let selectedBlogList = container.dataset.currentBlogList || 'grid';

    // Current option values (start from resolved options of active template)
    let checkoutOptions = {};
    let productOptions = {};
    let categoryOptions = {};
    let blogPostOptions = {};
    let blogListOptions = {};

    // Initialize with current active options
    const activeCheckout = checkoutCards.find(c => c.key === selectedCheckout);
    if (activeCheckout) checkoutOptions = { ...activeCheckout.resolved_options };

    const activeProduct = productCards.find(c => c.key === selectedProduct);
    if (activeProduct) productOptions = { ...activeProduct.resolved_options };

    const activeCategory = categoryCards.find(c => c.key === selectedCategory);
    if (activeCategory) categoryOptions = { ...activeCategory.resolved_options };

    const activeBlogPost = blogPostCards.find(c => c.key === selectedBlogPost);
    if (activeBlogPost) blogPostOptions = { ...activeBlogPost.resolved_options };

    const activeBlogList = blogListCards.find(c => c.key === selectedBlogList);
    if (activeBlogList) blogListOptions = { ...activeBlogList.resolved_options };

    // === Card Selection ===

    document.querySelectorAll('.template-card').forEach(card => {
        card.addEventListener('click', function() {
            const type = this.dataset.type;
            const key = this.dataset.key;

            // Update selection state
            const container = this.closest('.template-cards');
            container.querySelectorAll('.template-card').forEach(c => {
                c.classList.remove('template-card--active');
                const badge = c.querySelector('.template-card__badge');
                if (badge) badge.innerHTML = '';
            });
            this.classList.add('template-card--active');
            this.querySelector('.template-card__badge').innerHTML =
                '<span class="badge badge--primary">Active</span>';

            if (type === 'checkout') {
                selectedCheckout = key;
                const cardData = checkoutCards.find(c => c.key === key);
                checkoutOptions = cardData ? { ...cardData.resolved_options } : {};
                renderOptions('checkout', key);
            } else if (type === 'product') {
                selectedProduct = key;
                const cardData = productCards.find(c => c.key === key);
                productOptions = cardData ? { ...cardData.resolved_options } : {};
                renderOptions('product', key);
            } else if (type === 'category') {
                selectedCategory = key;
                const cardData = categoryCards.find(c => c.key === key);
                categoryOptions = cardData ? { ...cardData.resolved_options } : {};
                renderOptions('category', key);
            } else if (type === 'blog_post') {
                selectedBlogPost = key;
                const cardData = blogPostCards.find(c => c.key === key);
                blogPostOptions = cardData ? { ...cardData.resolved_options } : {};
                renderOptions('blog_post', key);
            } else if (type === 'blog_list') {
                selectedBlogList = key;
                const cardData = blogListCards.find(c => c.key === key);
                blogListOptions = cardData ? { ...cardData.resolved_options } : {};
                renderOptions('blog_list', key);
            }
        });
    });

    // === Options Rendering ===

    function getCardsAndValues(type) {
        if (type === 'checkout') return { cards: checkoutCards, values: checkoutOptions };
        if (type === 'product') return { cards: productCards, values: productOptions };
        if (type === 'category') return { cards: categoryCards, values: categoryOptions };
        if (type === 'blog_post') return { cards: blogPostCards, values: blogPostOptions };
        if (type === 'blog_list') return { cards: blogListCards, values: blogListOptions };
        return { cards: [], values: {} };
    }

    function renderOptions(type, templateKey) {
        const { cards, values } = getCardsAndValues(type);
        const cardData = cards.find(c => c.key === templateKey);
        if (!cardData) return;

        const schema = cardData.options_schema;
        const gridEl = document.getElementById(`${type}-options-grid`);
        const titleEl = document.getElementById(`${type}-options-title`);
        const panelEl = document.getElementById(`${type}-options`);

        if (!gridEl) return;

        titleEl.textContent = cardData.name + ' Options';
        panelEl.hidden = false;

        // Build options HTML
        const entries = Object.entries(schema);
        if (entries.length === 0) {
            gridEl.innerHTML = '<p style="color: var(--body-quiet-color); font-size: 0.875rem;">No configurable options for this template.</p>';
            return;
        }

        gridEl.innerHTML = entries.map(([key, def]) => {
            const currentValue = values[key] !== undefined ? values[key] : def.default;
            const label = def.label || key;
            const help = def.help || '';
            const optionId = `${type}-opt-${key}`;

            if (def.type === 'bool') {
                const checked = currentValue ? 'checked' : '';
                return `
                    <div class="template-option">
                        <div class="template-option__toggle">
                            <input type="checkbox" id="${optionId}" data-type="${type}" data-key="${key}" ${checked}>
                        </div>
                        <div class="template-option__info">
                            <label class="template-option__label" for="${optionId}">${esc(label)}</label>
                            ${help ? `<p class="template-option__help">${esc(help)}</p>` : ''}
                        </div>
                    </div>
                `;
            } else if (def.type === 'select') {
                const opts = (def.options || []).map(o => {
                    const sel = o === currentValue ? 'selected' : '';
                    return `<option value="${esc(o)}" ${sel}>${esc(o)}</option>`;
                }).join('');
                return `
                    <div class="template-option">
                        <div class="template-option__info" style="width: 100%;">
                            <label class="template-option__label" for="${optionId}">${esc(label)}</label>
                            ${help ? `<p class="template-option__help">${esc(help)}</p>` : ''}
                            <div class="template-option__select">
                                <select id="${optionId}" data-type="${type}" data-key="${key}">
                                    ${opts}
                                </select>
                            </div>
                        </div>
                    </div>
                `;
            }
            return '';
        }).join('');

        // Bind change events
        gridEl.querySelectorAll('input[type="checkbox"]').forEach(input => {
            input.addEventListener('change', function() {
                const optType = this.dataset.type;
                const optKey = this.dataset.key;
                const { values } = getCardsAndValues(optType);
                values[optKey] = this.checked;
            });
        });

        gridEl.querySelectorAll('select').forEach(select => {
            select.addEventListener('change', function() {
                const optType = this.dataset.type;
                const optKey = this.dataset.key;
                const { values } = getCardsAndValues(optType);
                values[optKey] = this.value;
            });
        });
    }

    // === Trust Badge Editor (reusable) ===

    const TRUST_BADGE_ICONS = [
        { value: 'fas fa-lock', label: 'Lock' },
        { value: 'fas fa-shield-alt', label: 'Shield' },
        { value: 'fas fa-shield-halved', label: 'Shield Check' },
        { value: 'fas fa-check-circle', label: 'Check Circle' },
        { value: 'fas fa-certificate', label: 'Certificate' },
        { value: 'fas fa-award', label: 'Award' },
        { value: 'fas fa-medal', label: 'Medal' },
        { value: 'fas fa-star', label: 'Star' },
        { value: 'fas fa-heart', label: 'Heart' },
        { value: 'fas fa-thumbs-up', label: 'Thumbs Up' },
        { value: 'fas fa-credit-card', label: 'Credit Card' },
        { value: 'fas fa-money-bill-wave', label: 'Money' },
        { value: 'fas fa-truck', label: 'Truck' },
        { value: 'fas fa-shipping-fast', label: 'Fast Shipping' },
        { value: 'fas fa-undo', label: 'Returns' },
        { value: 'fas fa-exchange-alt', label: 'Exchange' },
        { value: 'fas fa-headset', label: 'Support' },
        { value: 'fas fa-phone', label: 'Phone' },
        { value: 'fas fa-envelope', label: 'Email' },
        { value: 'fas fa-clock', label: 'Clock' },
        { value: 'fas fa-bolt', label: 'Lightning' },
        { value: 'fas fa-gift', label: 'Gift' },
        { value: 'fas fa-percent', label: 'Percent' },
        { value: 'fas fa-globe', label: 'Globe' },
        { value: 'fas fa-leaf', label: 'Leaf (Eco)' },
        { value: 'fas fa-recycle', label: 'Recycle' },
        { value: 'fas fa-handshake', label: 'Handshake' },
        { value: 'fas fa-user-shield', label: 'User Shield' },
        { value: 'fas fa-infinity', label: 'Infinity' },
        { value: 'fas fa-download', label: 'Download' },
        { value: 'fas fa-key', label: 'Key' },
    ];

    const MAX_BADGES = 6;

    /**
     * Creates a badge editor instance bound to specific DOM elements.
     * @param {Object} opts
     * @param {string} opts.listId - ID of the badge list container
     * @param {string} opts.addBtnId - ID of the add button
     * @param {string} opts.dataKey - dataset key on container (camelCase)
     * @param {string} opts.emptyIcon - icon for empty state
     * @returns {{ badges: Array }} - reference to the badges array
     */
    function createBadgeEditor(opts) {
        let badges = JSON.parse(container.dataset[opts.dataKey] || '[]');
        const listEl = document.getElementById(opts.listId);
        const addBtn = document.getElementById(opts.addBtnId);

        function render() {
            if (!listEl) return;

            if (badges.length === 0) {
                listEl.innerHTML = `
                    <div class="trust-badge-editor__empty">
                        <i class="${opts.emptyIcon || 'fas fa-shield-alt'}"></i>
                        No trust badges configured. Add one below.
                    </div>
                `;
            } else {
                listEl.innerHTML = badges.map((badge, index) => {
                    const iconOptions = TRUST_BADGE_ICONS.map(ic =>
                        `<option value="${esc(ic.value)}" ${ic.value === badge.icon ? 'selected' : ''}>${esc(ic.label)}</option>`
                    ).join('');

                    return `
                        <div class="trust-badge-editor__item" draggable="true" data-index="${index}">
                            <span class="trust-badge-editor__drag" title="Drag to reorder">
                                <i class="fas fa-grip-vertical"></i>
                            </span>
                            <div class="trust-badge-editor__icon-preview">
                                <i class="${esc(badge.icon)}"></i>
                            </div>
                            <select class="trust-badge-editor__icon-select" data-index="${index}">
                                ${iconOptions}
                            </select>
                            <input type="text" class="trust-badge-editor__text-input"
                                   data-index="${index}"
                                   value="${esc(badge.text)}"
                                   placeholder="Badge text..."
                                   maxlength="60">
                            <button type="button" class="trust-badge-editor__remove" data-index="${index}" title="Remove badge">
                                <i class="fas fa-trash-alt"></i>
                            </button>
                        </div>
                    `;
                }).join('');
            }

            if (addBtn) {
                addBtn.disabled = badges.length >= MAX_BADGES;
            }

            bindEvents();
        }

        function bindEvents() {
            if (!listEl) return;

            listEl.querySelectorAll('.trust-badge-editor__icon-select').forEach(select => {
                select.addEventListener('change', function() {
                    const idx = parseInt(this.dataset.index, 10);
                    badges[idx].icon = this.value;
                    const preview = this.closest('.trust-badge-editor__item').querySelector('.trust-badge-editor__icon-preview i');
                    if (preview) preview.className = this.value;
                });
            });

            listEl.querySelectorAll('.trust-badge-editor__text-input').forEach(input => {
                input.addEventListener('input', function() {
                    const idx = parseInt(this.dataset.index, 10);
                    badges[idx].text = this.value;
                });
            });

            listEl.querySelectorAll('.trust-badge-editor__remove').forEach(btn => {
                btn.addEventListener('click', function() {
                    const idx = parseInt(this.dataset.index, 10);
                    badges.splice(idx, 1);
                    render();
                });
            });

            let dragIndex = null;
            listEl.querySelectorAll('.trust-badge-editor__item').forEach(item => {
                item.addEventListener('dragstart', function(e) {
                    dragIndex = parseInt(this.dataset.index, 10);
                    this.classList.add('dragging');
                    e.dataTransfer.effectAllowed = 'move';
                });
                item.addEventListener('dragend', function() {
                    this.classList.remove('dragging');
                    dragIndex = null;
                    listEl.querySelectorAll('.drag-over').forEach(el => el.classList.remove('drag-over'));
                });
                item.addEventListener('dragover', function(e) {
                    e.preventDefault();
                    e.dataTransfer.dropEffect = 'move';
                    listEl.querySelectorAll('.drag-over').forEach(el => el.classList.remove('drag-over'));
                    this.classList.add('drag-over');
                });
                item.addEventListener('dragleave', function() {
                    this.classList.remove('drag-over');
                });
                item.addEventListener('drop', function(e) {
                    e.preventDefault();
                    this.classList.remove('drag-over');
                    const dropIndex = parseInt(this.dataset.index, 10);
                    if (dragIndex === null || dragIndex === dropIndex) return;
                    const [moved] = badges.splice(dragIndex, 1);
                    badges.splice(dropIndex, 0, moved);
                    render();
                });
            });
        }

        if (addBtn) {
            addBtn.addEventListener('click', function() {
                if (badges.length >= MAX_BADGES) return;
                badges.push({ icon: 'fas fa-check-circle', text: '' });
                render();
                const inputs = listEl.querySelectorAll('.trust-badge-editor__text-input');
                if (inputs.length > 0) inputs[inputs.length - 1].focus();
            });
        }

        render();
        return { get badges() { return badges; } };
    }

    // Create badge editors for each section
    const checkoutBadgeEditor = createBadgeEditor({
        listId: 'trust-badge-list',
        addBtnId: 'add-trust-badge',
        dataKey: 'checkoutTrustBadges',
        emptyIcon: 'fas fa-shield-alt',
    });

    const productBadgeEditor = createBadgeEditor({
        listId: 'product-badge-list',
        addBtnId: 'add-product-badge',
        dataKey: 'productTrustBadges',
        emptyIcon: 'fas fa-shopping-bag',
    });

    const digitalBadgeEditor = createBadgeEditor({
        listId: 'digital-badge-list',
        addBtnId: 'add-digital-badge',
        dataKey: 'digitalTrustBadges',
        emptyIcon: 'fas fa-download',
    });

    // === Save ===

    const saveBtns = document.querySelectorAll('.save-config-btn');

    async function handleSave() {
        saveBtns.forEach(btn => {
            btn.disabled = true;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';
        });

        try {
            const resp = await fetch(saveUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrf(),
                },
                body: JSON.stringify({
                    checkout_template: selectedCheckout,
                    checkout_options: checkoutOptions,
                    product_template: selectedProduct,
                    product_options: productOptions,
                    category_template: selectedCategory,
                    category_options: categoryOptions,
                    blog_post_template: selectedBlogPost,
                    blog_post_options: blogPostOptions,
                    blog_list_template: selectedBlogList,
                    blog_list_options: blogListOptions,
                    checkout_trust_badges: checkoutBadgeEditor.badges,
                    product_trust_badges: productBadgeEditor.badges,
                    digital_trust_badges: digitalBadgeEditor.badges,
                }),
            });

            const data = await resp.json();
            showStatus(data.success ? 'success' : 'error', data.message || 'Saved.');
        } catch (err) {
            console.error('Save error:', err);
            showStatus('error', 'Failed to save. Please try again.');
        } finally {
            saveBtns.forEach(btn => {
                btn.disabled = false;
                btn.innerHTML = '<i class="fas fa-save"></i> Save Configuration';
            });
        }
    }

    saveBtns.forEach(btn => btn.addEventListener('click', handleSave));

    // === Utilities ===

    function showStatus(type, message) {
        const el = document.getElementById('save-status');
        const text = document.getElementById('save-status-text');
        if (!el || !text) return;

        el.hidden = false;
        el.className = `template-config__status template-config__status--${type}`;
        text.textContent = message;

        setTimeout(() => { el.hidden = true; }, 4000);
    }

    function getCsrf() {
        // Try meta tag first (works when cookie is HttpOnly)
        const meta = document.querySelector('meta[name="csrf-token"]');
        if (meta) return meta.content;
        // Fallback: hidden input
        const input = document.querySelector('[name="csrfmiddlewaretoken"]');
        if (input) return input.value;
        return '';
    }

    function esc(text) {
        const div = document.createElement('div');
        div.textContent = text || '';
        return div.innerHTML;
    }

    // === Initialize options for current templates ===
    renderOptions('checkout', selectedCheckout);
    renderOptions('product', selectedProduct);
    renderOptions('category', selectedCategory);
    renderOptions('blog_post', selectedBlogPost);
    renderOptions('blog_list', selectedBlogList);
})();
