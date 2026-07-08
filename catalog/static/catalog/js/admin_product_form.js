/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Product Admin Form JavaScript
 * Handles tabs, translations, images, and CKEditor integration
 */

(function() {
    'use strict';

    // Initialize window.PRODUCT_ADMIN_CONFIG from JSON island
    (function() {
        var dataEl = document.getElementById('product-admin-config');
        if (dataEl) {
            try {
                var cfg = JSON.parse(dataEl.textContent);
                // Build translationsApiUrl from template
                if (cfg.translationsApiUrlTemplate) {
                    var productId = cfg.productId || '0';
                    cfg.translationsApiUrl = cfg.translationsApiUrlTemplate.replace('/0/', '/' + productId + '/');
                }
                window.PRODUCT_ADMIN_CONFIG = cfg;
            } catch (e) {
                console.error('[Product Admin] Failed to parse config:', e);
            }
        }
    }());

    // Global state
    let translations = {};
    let currentLanguage = null;
    let availableLanguages = [];
    let ckeditorInstances = {};
    let productImages = [];

    // Initialize on DOM ready
    document.addEventListener('DOMContentLoaded', function() {
        // Tab switching handled by global AdminTabs utility
        // Translation management is now handled by the TranslatableFieldWidget system
        // initTranslations(); // DISABLED - using new translation system
        initImageManager();
        initSaveButtons();
        initStickyHeader();
        initProductTypeVisibility();
        initDirtyTracking();
        initErrorScrolling();
        loadProductData();
        initLicenseTemplatePreview();
        initZeroFormsets();
    });

    /**
     * Product Type Conditional Visibility
     * Shows/hides fieldsets and tabs based on selected product type and checkboxes
     */
    function initProductTypeVisibility() {
        const productTypeField = document.getElementById('id_product_type');
        if (!productTypeField) return;

        // Get all type-specific fieldsets
        const bundlePricingFieldset = document.getElementById('bundle-pricing-section');  // Updated to use custom form-card ID
        const giftCardFieldset = document.querySelector('.form-row.field-gift_card_denomination_type')?.closest('.module');
        const customizationFieldset = document.querySelector('.form-row.field-allow_customization')?.closest('.module');

        // Get checkbox fields for conditional tabs
        const isDigitalCheckbox = document.getElementById('id_is_digital');
        const allowCustomizationCheckbox = document.getElementById('id_allow_customization');
        const isSubscriptionEnabledCheckbox = document.getElementById('id_is_subscription_enabled');

        function updateFieldsetVisibility() {
            const selectedType = productTypeField.value;

            // Bundle Pricing - only for bundle products
            if (bundlePricingFieldset) {
                bundlePricingFieldset.style.display = selectedType === 'bundle' ? 'block' : 'none';
            }

            // Gift Card Configuration - only for gift_card products
            if (giftCardFieldset) {
                giftCardFieldset.style.display = selectedType === 'gift_card' ? 'block' : 'none';
            }

            // Customization Configuration - for customizable products (or any product that merchant wants to customize)
            // Show for customizable type, but can also be enabled for other types
            if (customizationFieldset) {
                // Always show for customizable type, keep visible but allow manual collapse for others
                if (selectedType === 'customizable') {
                    customizationFieldset.style.display = 'block';
                    // Expand if it's a details element
                    const details = customizationFieldset.querySelector('details');
                    if (details) details.open = true;
                } else {
                    // Keep visible but allow manual collapse
                    customizationFieldset.style.display = 'block';
                }
            }

            // Physical Attributes - hide for digital, gift_card, and booking
            const physicalFieldset = document.querySelector('.form-row.field-weight')?.closest('.module');
            if (physicalFieldset) {
                physicalFieldset.style.display = ['digital', 'gift_card', 'booking'].includes(selectedType) ? 'none' : 'block';
            }

            // Inventory - hide for digital, gift_card, and booking
            const inventoryFieldset = document.querySelector('.form-row.field-track_inventory')?.closest('.module');
            if (inventoryFieldset) {
                inventoryFieldset.style.display = ['digital', 'gift_card', 'booking'].includes(selectedType) ? 'none' : 'block';
            }
        }

        function updateTabVisibility() {
            const selectedType = productTypeField.value;

            // Get all conditional tabs
            const variationsTab = document.querySelector('.admin-tab-btn[data-tab="variations"]');
            const variationsPanel = document.querySelector('.tab-panel[data-panel="variations"]');
            const bundleTab = document.querySelector('.admin-tab-btn[data-tab="bundle-items"]');
            const bundlePanel = document.querySelector('.tab-panel[data-panel="bundle-items"]');
            const giftCardTab = document.querySelector('.admin-tab-btn[data-tab="gift-card"]');
            const giftCardPanel = document.querySelector('.tab-panel[data-panel="gift-card"]');
            const digitalTab = document.querySelector('.admin-tab-btn[data-tab="digital-assets"]');
            const digitalPanel = document.querySelector('.tab-panel[data-panel="digital-assets"]');
            const customizationTab = document.querySelector('.admin-tab-btn[data-tab="customization"]');
            const customizationPanel = document.querySelector('.tab-panel[data-panel="customization"]');

            // Show/hide Variations tab based on product type
            if (variationsTab && variationsPanel) {
                const showVariations = selectedType === 'variable';
                if (showVariations) {
                    variationsTab.classList.remove('hidden');
                } else {
                    variationsTab.classList.add('hidden');
                    if (variationsPanel.classList.contains('active')) {
                        // Switch to Basic Info tab if Variations tab was active
                        document.querySelector('.admin-tab-btn[data-tab="basic-info"]')?.click();
                    }
                }
            }

            // Show/hide Bundle Items tab based on product type
            if (bundleTab && bundlePanel) {
                const showBundle = selectedType === 'bundle';
                if (showBundle) {
                    bundleTab.classList.remove('hidden');
                } else {
                    bundleTab.classList.add('hidden');
                    if (bundlePanel.classList.contains('active')) {
                        document.querySelector('.admin-tab-btn[data-tab="basic-info"]')?.click();
                    }
                }
            }

            // Show/hide Gift Card tab based on product type
            if (giftCardTab && giftCardPanel) {
                const showGiftCard = selectedType === 'gift_card';
                if (showGiftCard) {
                    giftCardTab.classList.remove('hidden');
                } else {
                    giftCardTab.classList.add('hidden');
                    if (giftCardPanel.classList.contains('active')) {
                        document.querySelector('.admin-tab-btn[data-tab="basic-info"]')?.click();
                    }
                }
            }

            // Show/hide Digital Assets tab based on product type OR is_digital checkbox
            // Gift cards are excluded - they don't need digital asset downloads
            if (digitalTab && digitalPanel) {
                const showDigital = selectedType !== 'gift_card' && (selectedType === 'digital' || (isDigitalCheckbox && isDigitalCheckbox.checked));
                if (showDigital) {
                    digitalTab.classList.remove('hidden');
                } else {
                    digitalTab.classList.add('hidden');
                    if (digitalPanel.classList.contains('active')) {
                        document.querySelector('.admin-tab-btn[data-tab="basic-info"]')?.click();
                    }
                }
            }

            // Show/hide Customization tab based on product type OR allow_customization checkbox
            if (customizationTab && customizationPanel) {
                const showCustomization = selectedType === 'customizable' || (allowCustomizationCheckbox && allowCustomizationCheckbox.checked);
                if (showCustomization) {
                    customizationTab.classList.remove('hidden');
                } else {
                    customizationTab.classList.add('hidden');
                    if (customizationPanel.classList.contains('active')) {
                        document.querySelector('.admin-tab-btn[data-tab="basic-info"]')?.click();
                    }
                }
            }

            // Show/hide Licensing tab based on product type OR is_digital checkbox
            // Gift cards are excluded - they don't need license key management
            const licensingTab = document.querySelector('.admin-tab-btn[data-tab="licensing"]');
            const licensingPanel = document.querySelector('.tab-panel[data-panel="licensing"]');
            if (licensingTab && licensingPanel) {
                const showLicensing = selectedType !== 'gift_card' && (selectedType === 'digital' || (isDigitalCheckbox && isDigitalCheckbox.checked));
                if (showLicensing) {
                    licensingTab.classList.remove('hidden');
                } else {
                    licensingTab.classList.add('hidden');
                    if (licensingPanel.classList.contains('active')) {
                        document.querySelector('.admin-tab-btn[data-tab="basic-info"]')?.click();
                    }
                }
            }

            // Subscriptions tab is always visible (not conditional)
            // No visibility logic needed - it's always shown

            // Show/hide Configuration tab based on product type
            const configurationTab = document.querySelector('.admin-tab-btn[data-tab="configuration"]');
            const configurationPanel = document.querySelector('.tab-panel[data-panel="configuration"]');
            if (configurationTab && configurationPanel) {
                if (selectedType === 'configurable') {
                    configurationTab.classList.remove('hidden');
                } else {
                    configurationTab.classList.add('hidden');
                    if (configurationPanel.classList.contains('active')) {
                        document.querySelector('.admin-tab-btn[data-tab="basic-info"]')?.click();
                    }
                }
            }

            // Show/hide 3D Viewer tab based on product type
            const viewerTab = document.querySelector('.admin-tab-btn[data-tab="3d-viewer"]');
            const viewerPanel = document.querySelector('.tab-panel[data-panel="3d-viewer"]');
            if (viewerTab && viewerPanel) {
                if (selectedType === 'configurable') {
                    viewerTab.classList.remove('hidden');
                } else {
                    viewerTab.classList.add('hidden');
                    if (viewerPanel.classList.contains('active')) {
                        document.querySelector('.admin-tab-btn[data-tab="basic-info"]')?.click();
                    }
                }
            }

            // Show/hide Booking tab based on product type
            const bookingTab = document.querySelector('.admin-tab-btn[data-tab="booking"]');
            const bookingPanel = document.querySelector('.tab-panel[data-panel="booking"]');
            if (bookingTab && bookingPanel) {
                if (selectedType === 'booking') {
                    bookingTab.classList.remove('hidden');
                } else {
                    bookingTab.classList.add('hidden');
                    if (bookingPanel.classList.contains('active')) {
                        document.querySelector('.admin-tab-btn[data-tab="basic-info"]')?.click();
                    }
                }
            }

            // Hide is_digital checkbox when product type inherently sets it
            const isDigitalRow = document.getElementById('is-digital-row');
            if (isDigitalRow) {
                if (selectedType === 'digital' || selectedType === 'gift_card') {
                    isDigitalRow.style.display = 'none';
                } else {
                    isDigitalRow.style.display = '';
                }
            }
        }

        // Initial state
        updateFieldsetVisibility();
        updateTabVisibility();

        // Listen for changes
        productTypeField.addEventListener('change', function() {
            updateFieldsetVisibility();
            updateTabVisibility();
        });

        // Listen for checkbox changes
        if (isDigitalCheckbox) {
            isDigitalCheckbox.addEventListener('change', updateTabVisibility);
        }
        if (allowCustomizationCheckbox) {
            allowCustomizationCheckbox.addEventListener('change', updateTabVisibility);
        }
        if (isSubscriptionEnabledCheckbox) {
            isSubscriptionEnabledCheckbox.addEventListener('change', updateTabVisibility);
        }
    }

    /**
     * License Template Preview
     * Loads sample keys when a license template is selected
     */
    function initLicenseTemplatePreview() {
        const templateSelect = document.getElementById('id_license_template');
        const previewBox = document.getElementById('license-template-preview');
        const patternText = document.getElementById('preview-pattern-text');
        const samplesList = document.getElementById('preview-samples-list');

        if (!templateSelect || !previewBox) return;

        // Load preview when template changes
        templateSelect.addEventListener('change', function() {
            const templateId = this.value;
            if (!templateId) {
                previewBox.style.display = 'none';
                return;
            }
            loadTemplatePreview(templateId);
        });

        // Load preview on page load if template is already selected
        if (templateSelect.value) {
            loadTemplatePreview(templateSelect.value);
        }

        async function loadTemplatePreview(templateId) {
            try {
                const response = await fetch(`/admin/catalog/license-template-preview/${templateId}/`, {
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                    }
                });

                if (!response.ok) {
                    console.error('Failed to load template preview');
                    previewBox.style.display = 'none';
                    return;
                }

                const data = await response.json();

                // Display pattern
                if (patternText) {
                    patternText.textContent = data.pattern || data.display_pattern || '-';
                }

                // Display sample keys
                if (samplesList && data.samples) {
                    samplesList.innerHTML = '';
                    data.samples.forEach(sample => {
                        const li = document.createElement('li');
                        li.innerHTML = `<code class="license-preview-code">${sample}</code>`;
                        li.style.marginBottom = '5px';
                        samplesList.appendChild(li);
                    });
                }

                previewBox.style.display = 'block';
            } catch (error) {
                console.error('Error loading template preview:', error);
                previewBox.style.display = 'none';
            }
        }
    }

    /**
     * Dirty State Tracking
     * Tracks unsaved changes and warns user before leaving page
     */
    function initDirtyTracking() {
        let isDirty = false;
        const form = document.getElementById('product-form');
        if (!form) return;

        // Track all form inputs
        const trackableSelectors = [
            'input[type="text"]',
            'input[type="number"]',
            'input[type="email"]',
            'input[type="checkbox"]',
            'input[type="radio"]',
            'textarea',
            'select'
        ];

        const inputs = form.querySelectorAll(trackableSelectors.join(', '));

        // Mark form as dirty when any input changes
        inputs.forEach(input => {
            input.addEventListener('change', () => {
                if (!isDirty) {
                    isDirty = true;
                    markFormAsDirty();
                }
            });

            // Also track text input in real-time
            if (input.type === 'text' || input.tagName === 'TEXTAREA') {
                input.addEventListener('input', () => {
                    if (!isDirty) {
                        isDirty = true;
                        markFormAsDirty();
                    }
                });
            }
        });

        // Visual indicator
        function markFormAsDirty() {
            // Mark the form element itself so external scripts can detect dirty state
            form.dataset.dirty = 'true';

            const saveButtons = document.querySelectorAll('.submit-row input[type="submit"]');
            saveButtons.forEach(button => {
                if (!button.classList.contains('dirty')) {
                    button.classList.add('dirty');
                }
            });

            // Update header status badge to "Unsaved Changes"
            const badge = document.getElementById('product-status-badge');
            if (badge && !badge.classList.contains('status-unsaved')) {
                badge.className = 'status-badge status-unsaved';
                badge.textContent = 'Unsaved Changes';
            }
        }

        // Warn before leaving with unsaved changes
        window.addEventListener('beforeunload', (e) => {
            if (isDirty) {
                e.preventDefault();
                e.returnValue = ''; // Required for Chrome
            }
        });

        // Clear dirty state on form submit (native submit event)
        form.addEventListener('submit', () => {
            isDirty = false;
            delete form.dataset.dirty;
        });

        // Also clear dirty on save button clicks (capture phase)
        // This handles saveForm() which calls form.submit() — that does NOT fire the submit event
        document.querySelectorAll('button[name="_save"], #save-continue-btn').forEach(btn => {
            btn.addEventListener('click', () => { isDirty = false; }, true);
        });
    }

    /**
     * Auto-scroll to First Error
     * Scrolls to and highlights the first form error after validation
     */
    function initErrorScrolling() {
        // Run on page load to catch server-side validation errors
        const firstError = document.querySelector('.errorlist, .errornote');
        if (firstError) {
            setTimeout(() => {
                firstError.scrollIntoView({
                    behavior: 'smooth',
                    block: 'center'
                });

                // Add highlight animation
                const errorContainer = firstError.closest('.form-row, .inline-related, .tab-panel');
                if (errorContainer) {
                    errorContainer.classList.add('error-highlight');
                    setTimeout(() => {
                        errorContainer.classList.remove('error-highlight');
                    }, 2000);
                }
            }, 300);
        }
    }

    /**
     * Translation Management - REMOVED
     *
     * The custom translation system has been replaced with the standard
     * TranslatableFieldWidget system. Translation buttons now appear next to
     * translatable fields (name, descriptions, SEO fields) and open a modal
     * translation editor.
     *
     * All translation-related code (initTranslations, fetchAvailableLanguages,
     * populateLanguageSelector, initCKEditorForTranslations, loadTranslations,
     * loadLanguageData, saveCurrentLanguageData, saveTranslationsToServer,
     * showTranslationStatus, updateSEOPreview) has been removed.
     */


    /**
     * Image Manager
     */
    function initImageManager() {
        const addImageBtn = document.getElementById('add-image-btn');
        if (addImageBtn) {
            addImageBtn.addEventListener('click', openMediaLibrary);
        }

        // Load existing images if editing
        if (window.PRODUCT_ADMIN_CONFIG.productId) {
            loadProductImages();
        }
    }

    /**
     * Load product images
     */
    async function loadProductImages() {
        // This would fetch from your API
        // For now, placeholder
        try {
            const response = await fetch(`/api/products/${window.PRODUCT_ADMIN_CONFIG.productId}/images/`);
            if (response.ok) {
                productImages = await response.json();
                renderImagesGrid();
            }
        } catch (e) {
            console.error('Failed to load images:', e);
        }
    }

    /**
     * Render images grid
     */
    function renderImagesGrid() {
        const grid = document.getElementById('images-grid');
        if (!grid) return;

        grid.innerHTML = '';

        productImages.forEach((image, index) => {
            const imageItem = document.createElement('div');
            imageItem.className = 'image-item';
            imageItem.draggable = true;
            imageItem.dataset.imageId = image.id;

            imageItem.innerHTML = `
                <img src="${image.thumbnail_url}" alt="${image.alt_text || ''}">
                ${image.is_primary ? '<span class="primary-badge">Primary</span>' : ''}
                <div class="image-actions">
                    <button type="button" data-action="set-primary" data-image-id="${image.id}" title="Set as primary">
                        <i class="fas fa-star"></i>
                    </button>
                    <button type="button" data-action="remove-image" data-image-id="${image.id}" title="Remove">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            `;

            // Drag and drop for reordering
            imageItem.addEventListener('dragstart', handleDragStart);
            imageItem.addEventListener('dragover', handleDragOver);
            imageItem.addEventListener('drop', handleDrop);
            imageItem.addEventListener('dragend', handleDragEnd);

            grid.appendChild(imageItem);
        });
    }

    /**
     * Open media library modal
     */
    function openMediaLibrary() {
        const modal = document.getElementById('media-library-modal');
        if (!modal) return;

        // Load media library content via AJAX
        fetch(window.PRODUCT_ADMIN_CONFIG.mediaLibraryUrl)
            .then(response => response.text())
            .then(html => {
                document.getElementById('media-library-content').innerHTML = html;
                modal.classList.add('active');
            })
            .catch(e => {
                console.error('Failed to load media library:', e);
                AdminModal.alert({message: 'Failed to load media library', type: 'error'});
            });
    }

    /**
     * Close media library modal
     */
    const closeModalBtn = document.getElementById('close-media-modal');
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', function() {
            document.getElementById('media-library-modal').classList.remove('active');
        });
    }

    /**
     * Save Buttons
     */
    function initSaveButtons() {
        // Save and continue
        const saveContinueBtn = document.getElementById('save-continue-btn');
        if (saveContinueBtn) {
            saveContinueBtn.addEventListener('click', function() {
                saveForm(true);
            });
        }
    }

    /**
     * Sticky Header Observer
     * Adds visual feedback when header becomes sticky
     */
    function initStickyHeader() {
        const header = document.querySelector('.product-admin-header');
        if (!header) return;

        let stickyOffsetValue = window.getComputedStyle(header).top || '0px';
        let stickyOffset = parseFloat(stickyOffsetValue) || 0;
        const refreshStickyOffset = () => {
            stickyOffsetValue = window.getComputedStyle(header).top || '0px';
            stickyOffset = parseFloat(stickyOffsetValue) || 0;
        };
        refreshStickyOffset();

        const layoutRail = header.closest('.main-content') || document.querySelector('.main-content');

        // Placeholder prevents layout shift when we switch to fixed positioning
        const placeholder = document.createElement('div');
        placeholder.className = 'product-admin-header-placeholder';
        header.parentNode.insertBefore(placeholder, header);

        let usingFixedFallback = false;

        const updatePlaceholderHeight = () => {
            placeholder.style.height = `${header.offsetHeight}px`;
        };

        const getLayoutBounds = () => {
            const rect = layoutRail?.getBoundingClientRect() || placeholder.getBoundingClientRect();
            const left = Math.max(rect.left, 0);
            const rightEdge = Math.min(rect.right, window.innerWidth);
            const right = Math.max(window.innerWidth - rightEdge, 0);
            return { left, right };
        };

        const applyHorizontalExpansion = () => {
            const { left, right } = getLayoutBounds();
            header.style.setProperty('--sticky-left', `${left}px`);
            header.style.setProperty('--sticky-right', `${right}px`);
        };

        const applyFixedFallback = () => {
            updatePlaceholderHeight();

            header.style.setProperty('--sticky-top', stickyOffsetValue);
            applyHorizontalExpansion();

            usingFixedFallback = true;
        };

        const clearFixedFallback = () => {
            placeholder.style.height = '0px';
            header.style.removeProperty('--sticky-top');
            header.style.removeProperty('--sticky-left');
            header.style.removeProperty('--sticky-right');

            usingFixedFallback = false;
        };

        const refreshFixedFallbackGeometry = () => {
            if (!usingFixedFallback) return;
            updatePlaceholderHeight();
            applyHorizontalExpansion();
        };
        let isCurrentlyStuck = false;

        const setStuckState = (shouldStick) => {
            if (shouldStick === isCurrentlyStuck) return;
            isCurrentlyStuck = shouldStick;

            if (shouldStick) {
                header.classList.add('is-stuck');
                applyFixedFallback();
            } else {
                header.classList.remove('is-stuck');
                clearFixedFallback();
            }
        };

        const getScrollPosition = () =>
            typeof window.scrollY === 'number' ? window.scrollY : window.pageYOffset || 0;

        const getStickyStart = () => placeholder.getBoundingClientRect().top + getScrollPosition() - stickyOffset;
        let stickyStart = getStickyStart();

        const handleScroll = () => {
            const shouldStick = getScrollPosition() >= stickyStart;
            setStuckState(shouldStick);
            if (shouldStick) {
                refreshFixedFallbackGeometry();
            }
        };

        window.addEventListener('scroll', handleScroll, { passive: true });
        window.addEventListener('resize', () => {
            refreshStickyOffset();
            stickyStart = getStickyStart();
            refreshFixedFallbackGeometry();
            handleScroll();
        });

        if ('ResizeObserver' in window) {
            const resizeObserver = new ResizeObserver(() => {
                refreshStickyOffset();
                stickyStart = getStickyStart();
                refreshFixedFallbackGeometry();
                handleScroll();
            });
            resizeObserver.observe(placeholder);
        }

        const sidebar = document.getElementById('sidebar');
        if (sidebar && 'MutationObserver' in window) {
            const mutationObserver = new MutationObserver(() => {
                refreshStickyOffset();
                stickyStart = getStickyStart();
                refreshFixedFallbackGeometry();
                handleScroll();
            });
            mutationObserver.observe(sidebar, { attributes: true, attributeFilter: ['class'] });
        }

        handleScroll();
    }

    /**
     * Save form
     */
    function saveForm(continueEditing = false) {
        // Translation data is now handled by TranslatableFieldWidget system
        // No need to manually save translation data here
        // saveCurrentLanguageData(); // DISABLED
        // document.getElementById('translations-data-field').value = JSON.stringify(translations); // DISABLED

        // Submit form
        const form = document.getElementById('product-form');
        if (continueEditing) {
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = '_continue';
            input.value = '1';
            form.appendChild(input);
        }
        form.submit();
    }

    /**
     * Load product data
     */
    function loadProductData() {
        // Load any additional product data needed
        if (window.PRODUCT_ADMIN_CONFIG.productId) {
            // Data is already loaded through Django template
        }
    }

    /**
     * Drag and Drop for Image Reordering
     */
    let draggedElement = null;

    function handleDragStart(e) {
        draggedElement = this;
        this.style.opacity = '0.5';
        e.dataTransfer.effectAllowed = 'move';
    }

    function handleDragOver(e) {
        if (e.preventDefault) {
            e.preventDefault();
        }
        e.dataTransfer.dropEffect = 'move';
        return false;
    }

    function handleDrop(e) {
        if (e.stopPropagation) {
            e.stopPropagation();
        }

        if (draggedElement !== this) {
            const draggedId = draggedElement.dataset.imageId;
            const targetId = this.dataset.imageId;

            // Reorder in array
            const draggedIndex = productImages.findIndex(img => img.id == draggedId);
            const targetIndex = productImages.findIndex(img => img.id == targetId);

            const [draggedImage] = productImages.splice(draggedIndex, 1);
            productImages.splice(targetIndex, 0, draggedImage);

            renderImagesGrid();
            // Save new order to server
            saveImageOrder();
        }

        return false;
    }

    function handleDragEnd(e) {
        this.style.opacity = '1';
    }

    /**
     * Save image order to server
     */
    async function saveImageOrder() {
        const order = productImages.map(img => img.id);
        // Save to server...
    }

    /**
     * Utility Functions
     */
    function stripHTML(html) {
        const tmp = document.createElement('div');
        tmp.innerHTML = html;
        return tmp.textContent || tmp.innerText || '';
    }

    function escapeHTML(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // Delegated event handlers for image actions (CSP-compliant)
    var imagesGrid = document.getElementById('product-images-grid');
    if (imagesGrid) {
        imagesGrid.addEventListener('click', async function(e) {
            var btn = e.target.closest('[data-action]');
            if (!btn) return;
            var action = btn.dataset.action;
            var imageId = parseInt(btn.dataset.imageId, 10);
            if (action === 'set-primary') {
                productImages.forEach(function(img) {
                    img.is_primary = (img.id === imageId);
                });
                renderImagesGrid();
            } else if (action === 'remove-image') {
                var confirmed = await AdminModal.confirm({ message: 'Are you sure you want to remove this image?', danger: true, confirmText: 'Remove' });
                if (confirmed) {
                    productImages = productImages.filter(function(img) { return img.id !== imageId; });
                    renderImagesGrid();
                }
            }
        });
    }

    // Zero out AJAX-managed formset management form counts
    function initZeroFormsets() {
        document.querySelectorAll('[data-zero-formset]').forEach(function(el) {
            var prefix = el.dataset.zeroFormset;
            var tf = document.querySelector('input[name="' + prefix + '-TOTAL_FORMS"]');
            var inf = document.querySelector('input[name="' + prefix + '-INITIAL_FORMS"]');
            if (tf) { tf.value = '0'; }
            if (inf) { inf.value = '0'; }
        });

        // Sanity check: verify all formset management forms are present
        var formsetPrefixes = [];
        document.querySelectorAll('.js-inline-admin-formset').forEach(function(formset) {
            var id = formset.id;
            if (id && id.endsWith('-group')) {
                var prefix = id.replace('-group', '');
                formsetPrefixes.push(prefix);
            }
        });
        console.log('[Formset Check] Found formset prefixes:', formsetPrefixes);
        formsetPrefixes.forEach(function(prefix) {
            var totalForms = document.querySelector('input[name="' + prefix + '-TOTAL_FORMS"]');
            var initialForms = document.querySelector('input[name="' + prefix + '-INITIAL_FORMS"]');
            if (!totalForms || !initialForms) {
                console.error('[Formset Check] MISSING management form fields for ' + prefix);
            } else {
                console.log('[Formset Check] OK ' + prefix + ' TOTAL=' + totalForms.value + ' INITIAL=' + initialForms.value);
            }
        });
    }

})();
