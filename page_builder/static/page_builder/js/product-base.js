/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        // === Variant Data ===
        var variantsData = [];
        try {
            variantsData = JSON.parse(document.getElementById('variants-data').textContent || '[]');
        } catch (e) {
            console.warn('Could not parse variants data:', e);
        }
        const selectedAttributes = {};

        // === Image Gallery ===
        const mainImage = document.getElementById('main-image');
        const zoomResult = document.getElementById('zoom-result');
        const zoomLens = document.getElementById('zoom-lens');
        const zoomContainer = document.getElementById('gallery-zoom');
        const thumbnails = document.querySelectorAll('.product-gallery__thumb');

        // Thumbnail click
        thumbnails.forEach(thumb => {
            thumb.addEventListener('click', function() {
                thumbnails.forEach(t => t.classList.remove('product-gallery__thumb--active'));
                this.classList.add('product-gallery__thumb--active');

                if (mainImage) {
                    mainImage.src = this.dataset.image;
                    mainImage.dataset.zoomSrc = this.dataset.zoom;
                }
            });
        });

        // Image zoom on hover — accounts for object-fit: contain
        if (zoomContainer && mainImage && zoomResult && zoomLens) {
            zoomContainer.addEventListener('mousemove', function(e) {
                const rect = zoomContainer.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;

                // Calculate actual rendered image dimensions (object-fit: contain
                // may leave blank space around the image)
                const nw = mainImage.naturalWidth;
                const nh = mainImage.naturalHeight;
                if (!nw || !nh) return;

                const imgAspect = nw / nh;
                const containerAspect = rect.width / rect.height;
                var rendW, rendH, offX, offY;

                if (imgAspect > containerAspect) {
                    rendW = rect.width;
                    rendH = rect.width / imgAspect;
                    offX = 0;
                    offY = (rect.height - rendH) / 2;
                } else {
                    rendH = rect.height;
                    rendW = rect.height * imgAspect;
                    offX = (rect.width - rendW) / 2;
                    offY = 0;
                }

                // Mouse position relative to the rendered image
                const imgX = x - offX;
                const imgY = y - offY;

                // Hide zoom if cursor is outside the actual image area
                if (imgX < 0 || imgX > rendW || imgY < 0 || imgY > rendH) {
                    zoomLens.style.opacity = '0';
                    zoomResult.style.opacity = '0';
                    return;
                }
                zoomLens.style.opacity = '';
                zoomResult.style.opacity = '';

                // Position lens relative to rendered image, then offset to container
                let lensX = imgX - zoomLens.offsetWidth / 2;
                let lensY = imgY - zoomLens.offsetHeight / 2;
                lensX = Math.max(0, Math.min(lensX, rendW - zoomLens.offsetWidth));
                lensY = Math.max(0, Math.min(lensY, rendH - zoomLens.offsetHeight));

                zoomLens.style.left = (lensX + offX) + 'px';
                zoomLens.style.top = (lensY + offY) + 'px';

                // Zoom ratio and background — use rendered image size, not container
                const zoomSrc = mainImage.dataset.zoomSrc || mainImage.src;
                const ratioX = zoomResult.offsetWidth / zoomLens.offsetWidth;
                const ratioY = zoomResult.offsetHeight / zoomLens.offsetHeight;

                zoomResult.style.backgroundImage = `url('${zoomSrc}')`;
                zoomResult.style.backgroundSize = `${rendW * ratioX}px ${rendH * ratioY}px`;
                zoomResult.style.backgroundPosition = `-${lensX * ratioX}px -${lensY * ratioY}px`;
            });

            zoomContainer.addEventListener('mouseleave', function() {
                zoomLens.style.opacity = '';
                zoomResult.style.opacity = '';
            });
        }

        // === Image Lightbox ===
        const isHeroGallery = !!document.querySelector('.product-hero');

        function buildLightbox() {
            const images = [];
            thumbnails.forEach(thumb => {
                if (thumb.dataset.isVideo === 'true') return;
                images.push({
                    src: thumb.dataset.zoom || thumb.dataset.image,
                    thumbSrc: thumb.querySelector('img') ? thumb.querySelector('img').src : thumb.dataset.image,
                    alt: thumb.getAttribute('aria-label') || ''
                });
            });
            // If no thumbnails, use the main image
            if (images.length === 0 && mainImage) {
                images.push({
                    src: mainImage.dataset.zoomSrc || mainImage.src,
                    thumbSrc: mainImage.src,
                    alt: mainImage.alt || ''
                });
            }
            if (images.length === 0) return null;

            const lightbox = document.createElement('div');
            lightbox.className = 'product-lightbox';
            lightbox.id = 'product-lightbox';

            let thumbsHtml = '';
            if (images.length > 1) {
                thumbsHtml = '<div class="product-lightbox__thumbs">' +
                    images.map((img, i) =>
                        '<button class="product-lightbox__thumb' + (i === 0 ? ' product-lightbox__thumb--active' : '') + '" data-index="' + i + '">' +
                        '<img src="' + img.thumbSrc + '" alt="' + img.alt + '">' +
                        '</button>'
                    ).join('') +
                    '</div>';
            }

            lightbox.innerHTML =
                '<button class="product-lightbox__close" aria-label="Close"><i class="fas fa-times"></i></button>' +
                (images.length > 1 ? '<button class="product-lightbox__nav product-lightbox__nav--prev" aria-label="Previous"><i class="fas fa-chevron-left"></i></button>' : '') +
                '<div class="product-lightbox__image-wrap">' +
                '<img class="product-lightbox__image" src="' + images[0].src + '" alt="' + images[0].alt + '">' +
                '</div>' +
                (images.length > 1 ? '<button class="product-lightbox__nav product-lightbox__nav--next" aria-label="Next"><i class="fas fa-chevron-right"></i></button>' : '') +
                (images.length > 1 ? '<div class="product-lightbox__counter"><span class="product-lightbox__current">1</span> / ' + images.length + '</div>' : '') +
                thumbsHtml;

            document.body.appendChild(lightbox);

            let currentIndex = 0;
            const lbImage = lightbox.querySelector('.product-lightbox__image');
            const lbCounter = lightbox.querySelector('.product-lightbox__current');
            const lbThumbs = lightbox.querySelectorAll('.product-lightbox__thumb');

            function showImage(index) {
                currentIndex = ((index % images.length) + images.length) % images.length;
                lbImage.src = images[currentIndex].src;
                lbImage.alt = images[currentIndex].alt;
                if (lbCounter) lbCounter.textContent = currentIndex + 1;
                lbThumbs.forEach((t, i) => {
                    t.classList.toggle('product-lightbox__thumb--active', i === currentIndex);
                });
            }

            function openLightbox(startIndex) {
                showImage(startIndex || 0);
                lightbox.classList.add('product-lightbox--open');
                document.body.style.overflow = 'hidden';
            }

            function closeLightbox() {
                lightbox.classList.remove('product-lightbox--open');
                document.body.style.overflow = '';
            }

            lightbox.querySelector('.product-lightbox__close').addEventListener('click', closeLightbox);

            const prevBtn = lightbox.querySelector('.product-lightbox__nav--prev');
            const nextBtn = lightbox.querySelector('.product-lightbox__nav--next');
            if (prevBtn) prevBtn.addEventListener('click', () => showImage(currentIndex - 1));
            if (nextBtn) nextBtn.addEventListener('click', () => showImage(currentIndex + 1));

            lbThumbs.forEach(thumb => {
                thumb.addEventListener('click', () => showImage(parseInt(thumb.dataset.index)));
            });

            // Close on backdrop click
            lightbox.addEventListener('click', function(e) {
                if (e.target === lightbox || e.target.classList.contains('product-lightbox__image-wrap')) {
                    closeLightbox();
                }
            });

            // Keyboard navigation
            document.addEventListener('keydown', function(e) {
                if (!lightbox.classList.contains('product-lightbox--open')) return;
                if (e.key === 'Escape') closeLightbox();
                if (e.key === 'ArrowLeft' && images.length > 1) showImage(currentIndex - 1);
                if (e.key === 'ArrowRight' && images.length > 1) showImage(currentIndex + 1);
            });

            function updateImages(newImages) {
                images.length = 0;
                newImages.forEach(img => images.push(img));

                // Update thumbnails
                const thumbsContainer = lightbox.querySelector('.product-lightbox__thumbs');
                if (thumbsContainer) {
                    thumbsContainer.innerHTML = images.map((img, i) =>
                        '<button class="product-lightbox__thumb' + (i === 0 ? ' product-lightbox__thumb--active' : '') + '" data-index="' + i + '">' +
                        '<img src="' + img.thumbSrc + '" alt="' + img.alt + '">' +
                        '</button>'
                    ).join('');
                    thumbsContainer.querySelectorAll('.product-lightbox__thumb').forEach(thumb => {
                        thumb.addEventListener('click', () => showImage(parseInt(thumb.dataset.index)));
                    });
                }

                // Update nav visibility
                const prevNav = lightbox.querySelector('.product-lightbox__nav--prev');
                const nextNav = lightbox.querySelector('.product-lightbox__nav--next');
                if (prevNav) prevNav.style.display = images.length > 1 ? '' : 'none';
                if (nextNav) nextNav.style.display = images.length > 1 ? '' : 'none';

                // Update counter
                const counterEl = lightbox.querySelector('.product-lightbox__counter');
                if (counterEl) {
                    counterEl.style.display = images.length > 1 ? '' : 'none';
                    counterEl.innerHTML = '<span class="product-lightbox__current">1</span> / ' + images.length;
                }
            }

            return { openLightbox, images, updateImages };
        }

        const lightboxInstance = buildLightbox();

        // Open lightbox on main image click
        if (lightboxInstance && zoomContainer) {
            zoomContainer.addEventListener('click', function(e) {
                // Find which image is currently active
                let activeIndex = 0;
                if (mainImage) {
                    const currentSrc = mainImage.dataset.zoomSrc || mainImage.src;
                    const idx = lightboxInstance.images.findIndex(img => img.src === currentSrc);
                    if (idx >= 0) activeIndex = idx;
                }
                lightboxInstance.openLightbox(activeIndex);
            });
        }

        // === Variant Selection ===
        const variantSelector = document.getElementById('variant-selector');
        const selectionMode = variantSelector ? variantSelector.dataset.mode : null;
        const productName = document.querySelector('[data-product-name]')?.dataset.productName || '';

        // Store original product images for resetting gallery
        const originalImages = [];
        thumbnails.forEach(thumb => {
            originalImages.push({
                url: thumb.dataset.image,
                zoom: thumb.dataset.zoom,
                thumbSrc: thumb.querySelector('img') ? thumb.querySelector('img').src : thumb.dataset.image,
            });
        });

        if (selectionMode === 'attributes') {
            // Mode 1: Attribute-based selection

            // Swatch & button click handlers (color swatches + text pills)
            const swatches = document.querySelectorAll('.variant-swatch');
            swatches.forEach(swatch => {
                swatch.addEventListener('click', function() {
                    const attribute = this.dataset.attribute;
                    const value = this.dataset.value;
                    const display = this.dataset.display;

                    // Update selected state within group
                    const group = this.closest('.variant-group__options');
                    group.querySelectorAll('.variant-swatch').forEach(s => {
                        s.classList.remove('variant-swatch--active');
                    });
                    this.classList.add('variant-swatch--active');

                    // Update display text
                    const selectedSpan = document.getElementById('selected-' + attribute);
                    if (selectedSpan) {
                        selectedSpan.textContent = display;
                    }

                    // Store selection
                    selectedAttributes[attribute] = value;

                    // Find matching variant
                    updateAttributeVariant();
                });
            });

            // Dropdown change handlers
            const selects = document.querySelectorAll('.variant-select');
            selects.forEach(sel => {
                sel.addEventListener('change', function() {
                    const attribute = this.dataset.attribute;
                    const option = this.options[this.selectedIndex];
                    if (!option.value) {
                        delete selectedAttributes[attribute];
                    } else {
                        selectedAttributes[attribute] = option.value;
                        const selectedSpan = document.getElementById('selected-' + attribute);
                        if (selectedSpan) selectedSpan.textContent = option.dataset.display;
                    }
                    updateAttributeVariant();
                });
            });

            // Radio change handlers
            const radios = document.querySelectorAll('input[name^="attr-"]');
            radios.forEach(radio => {
                radio.addEventListener('change', function() {
                    const attribute = this.dataset.attribute;
                    const display = this.dataset.display;
                    selectedAttributes[attribute] = this.value;
                    const selectedSpan = document.getElementById('selected-' + attribute);
                    if (selectedSpan) selectedSpan.textContent = display;
                    updateAttributeVariant();
                });
            });
        } else if (selectionMode === 'direct') {
            // Mode 2: Direct variant selection (no attribute mappings)
            const directBtns = document.querySelectorAll('#variant-selector .variant-swatch');

            directBtns.forEach(btn => {
                btn.addEventListener('click', function() {
                    const variantId = parseInt(this.dataset.variantId);
                    const variant = variantsData.find(v => v.id === variantId);
                    if (!variant) return;

                    // Update selected state
                    directBtns.forEach(b => b.classList.remove('variant-swatch--active'));
                    this.classList.add('variant-swatch--active');

                    // Extract short display name
                    let displayName = variant.name;
                    if (productName && displayName.indexOf(productName) === 0) {
                        const suffix = displayName.substring(productName.length).replace(/^\s*[-\u2013\u2014]\s*/, '');
                        if (suffix) displayName = suffix;
                    }

                    // Update label
                    const selectedSpan = document.getElementById('selected-variant');
                    if (selectedSpan) selectedSpan.textContent = displayName;

                    // Apply variant changes
                    applyVariant(variant);
                });
            });
        }

        function updateAttributeVariant() {
            // Find variant that matches all selected attributes
            const matchingVariant = variantsData.find(variant => {
                return Object.keys(selectedAttributes).every(attr => {
                    return variant.attributes[attr] &&
                           variant.attributes[attr].slug === selectedAttributes[attr];
                });
            });

            if (matchingVariant) {
                applyVariant(matchingVariant);
            }
        }

        function applyVariant(variant) {
            // Update price
            const priceEl = document.getElementById('product-price');
            if (priceEl) {
                priceEl.innerHTML = `<span class="price">${variant.price}</span>`;
            }

            // Update SKU
            const skuEl = document.getElementById('product-sku');
            if (skuEl && variant.sku) {
                skuEl.textContent = variant.sku;
            }

            // Swap gallery to variant images
            swapGallery(variant);

            // Store selected variant ID for add to cart
            document.getElementById('add-to-cart').dataset.variantId = variant.id;
        }

        function swapGallery(variant) {
            const thumbsContainer = document.querySelector('.product-gallery__thumbnails');
            const variantImages = variant.images || [];

            if (variantImages.length > 0) {
                // Variant has its own gallery — show those images
                if (mainImage) {
                    mainImage.src = variantImages[0].url;
                    mainImage.dataset.zoomSrc = variantImages[0].url;
                    mainImage.alt = variantImages[0].alt || variant.name;
                }

                // Rebuild thumbnails
                if (thumbsContainer) {
                    thumbsContainer.innerHTML = '';
                    variantImages.forEach((img, idx) => {
                        const btn = document.createElement('button');
                        btn.className = 'product-gallery__thumb' + (idx === 0 ? ' product-gallery__thumb--active' : '');
                        btn.dataset.image = img.url;
                        btn.dataset.zoom = img.url;
                        btn.setAttribute('aria-label', 'View image ' + (idx + 1));

                        const imgEl = document.createElement('img');
                        imgEl.src = img.url;
                        imgEl.alt = img.alt || variant.name + ' - ' + (idx + 1);
                        imgEl.loading = 'lazy';
                        btn.appendChild(imgEl);

                        btn.addEventListener('click', function() {
                            thumbsContainer.querySelectorAll('.product-gallery__thumb').forEach(t => {
                                t.classList.remove('product-gallery__thumb--active');
                            });
                            this.classList.add('product-gallery__thumb--active');
                            if (mainImage) {
                                mainImage.src = this.dataset.image;
                                mainImage.dataset.zoomSrc = this.dataset.zoom;
                            }
                        });

                        thumbsContainer.appendChild(btn);
                    });
                    thumbsContainer.style.display = '';
                }
            } else if (variant.image_url && mainImage) {
                // Single variant image — just swap main image
                mainImage.src = variant.image_url;
                mainImage.dataset.zoomSrc = variant.image_url;
            } else if (originalImages.length > 0 && mainImage) {
                // No variant images — restore original product gallery
                mainImage.src = originalImages[0].url;
                mainImage.dataset.zoomSrc = originalImages[0].zoom;

                if (thumbsContainer) {
                    thumbsContainer.innerHTML = '';
                    originalImages.forEach((img, idx) => {
                        const btn = document.createElement('button');
                        btn.className = 'product-gallery__thumb' + (idx === 0 ? ' product-gallery__thumb--active' : '');
                        btn.dataset.image = img.url;
                        btn.dataset.zoom = img.zoom;
                        btn.setAttribute('aria-label', 'View image ' + (idx + 1));

                        const imgEl = document.createElement('img');
                        imgEl.src = img.thumbSrc;
                        imgEl.alt = productName + ' - ' + (idx + 1);
                        imgEl.loading = 'lazy';
                        btn.appendChild(imgEl);

                        btn.addEventListener('click', function() {
                            thumbsContainer.querySelectorAll('.product-gallery__thumb').forEach(t => {
                                t.classList.remove('product-gallery__thumb--active');
                            });
                            this.classList.add('product-gallery__thumb--active');
                            if (mainImage) {
                                mainImage.src = this.dataset.image;
                                mainImage.dataset.zoomSrc = this.dataset.zoom;
                            }
                        });

                        thumbsContainer.appendChild(btn);
                    });
                }
            }

            // Sync lightbox with current gallery images
            if (lightboxInstance) {
                const newLbImages = [];
                const currentThumbs = document.querySelectorAll('.product-gallery__thumb');
                currentThumbs.forEach(thumb => {
                    if (thumb.dataset.isVideo === 'true') return;
                    newLbImages.push({
                        src: thumb.dataset.zoom || thumb.dataset.image,
                        thumbSrc: thumb.querySelector('img') ? thumb.querySelector('img').src : thumb.dataset.image,
                        alt: thumb.getAttribute('aria-label') || ''
                    });
                });
                if (newLbImages.length === 0 && mainImage) {
                    newLbImages.push({
                        src: mainImage.dataset.zoomSrc || mainImage.src,
                        thumbSrc: mainImage.src,
                        alt: mainImage.alt || ''
                    });
                }
                lightboxInstance.updateImages(newLbImages);
            }
        }

        // === Quantity Selector ===
        const qtyInput = document.getElementById('quantity');
        const qtyDecrease = document.getElementById('qty-decrease');
        const qtyIncrease = document.getElementById('qty-increase');

        if (qtyDecrease && qtyIncrease && qtyInput) {
            qtyDecrease.addEventListener('click', function() {
                const current = parseInt(qtyInput.value) || 1;
                if (current > 1) {
                    qtyInput.value = current - 1;
                }
            });

            qtyIncrease.addEventListener('click', function() {
                const current = parseInt(qtyInput.value) || 1;
                const max = parseInt(qtyInput.max) || 99;
                if (current < max) {
                    qtyInput.value = current + 1;
                }
            });
        }

        // === Product Tabs ===
        const tabButtons = document.querySelectorAll('.product-tabs__tab');
        const tabPanels = document.querySelectorAll('.product-tabs__panel');

        tabButtons.forEach(button => {
            button.addEventListener('click', function() {
                const tabId = this.dataset.tab;

                // Update buttons
                tabButtons.forEach(btn => {
                    btn.classList.remove('product-tabs__tab--active');
                    btn.setAttribute('aria-selected', 'false');
                });
                this.classList.add('product-tabs__tab--active');
                this.setAttribute('aria-selected', 'true');

                // Update panels
                tabPanels.forEach(panel => {
                    panel.classList.remove('product-tabs__panel--active');
                    panel.hidden = true;
                });

                const activePanel = document.getElementById('tab-' + tabId);
                if (activePanel) {
                    activePanel.classList.add('product-tabs__panel--active');
                    activePanel.hidden = false;
                }
            });
        });

        // === Product Accordion ===
        const accordionHeaders = document.querySelectorAll('.product-accordion__header');
        accordionHeaders.forEach(header => {
            header.addEventListener('click', function() {
                const item = this.closest('.product-accordion__item');
                const body = item.querySelector('.product-accordion__body');
                const isOpen = item.classList.contains('product-accordion__item--open');

                if (isOpen) {
                    item.classList.remove('product-accordion__item--open');
                    body.hidden = true;
                    this.setAttribute('aria-expanded', 'false');
                } else {
                    item.classList.add('product-accordion__item--open');
                    body.hidden = false;
                    this.setAttribute('aria-expanded', 'true');
                }
            });
        });

        // === Bundle Items ===
        const bundleItemsDataEl = document.getElementById('bundle-items-data');
        const bundleItemsData = bundleItemsDataEl ? JSON.parse(bundleItemsDataEl.textContent || '[]') : [];
        const isBundle = bundleItemsData.length > 0;

        if (isBundle) {
            // Populate variant dropdowns for bundle items with allow_variant_selection
            bundleItemsData.forEach(bi => {
                if (bi.allow_variant_selection && bi.available_variants.length > 0) {
                    const sel = document.querySelector(
                        `select.bundle-item__variant-select[data-bundle-item-id="${bi.id}"]`
                    );
                    if (sel) {
                        bi.available_variants.forEach(v => {
                            const opt = document.createElement('option');
                            opt.value = v.id;
                            opt.textContent = v.name;
                            sel.appendChild(opt);
                        });
                    }
                }
            });
        }

        function collectBundleSelections() {
            const variantSelections = {};
            const excludedOptionalItems = [];

            bundleItemsData.forEach(bi => {
                // Check optional items
                if (bi.is_optional) {
                    const checkbox = document.querySelector(
                        `.bundle-item__optional input[data-bundle-item-id="${bi.id}"]`
                    );
                    if (checkbox && !checkbox.checked) {
                        excludedOptionalItems.push(bi.id);
                        return;
                    }
                }

                // Check variant selections
                if (bi.allow_variant_selection) {
                    const sel = document.querySelector(
                        `select.bundle-item__variant-select[data-bundle-item-id="${bi.id}"]`
                    );
                    if (sel && sel.value) {
                        variantSelections[bi.id] = parseInt(sel.value);
                    }
                }
            });

            return { variantSelections, excludedOptionalItems };
        }

        function validateBundleSelections() {
            // Check all required variant selections are made
            for (const bi of bundleItemsData) {
                if (!bi.allow_variant_selection) continue;
                // Skip excluded optional items
                if (bi.is_optional) {
                    const cb = document.querySelector(
                        `.bundle-item__optional input[data-bundle-item-id="${bi.id}"]`
                    );
                    if (cb && !cb.checked) continue;
                }
                const sel = document.querySelector(
                    `select.bundle-item__variant-select[data-bundle-item-id="${bi.id}"]`
                );
                if (!sel || !sel.value) {
                    return false;
                }
            }
            return true;
        }

        // === Add to Cart ===
        const addToCartBtn = document.getElementById('add-to-cart');
        const isBookingProduct = !!document.getElementById('booking-form');

        if (addToCartBtn && !isBookingProduct) {
            addToCartBtn.addEventListener('click', function() {
                const productId = this.dataset.productId;
                const variantId = this.dataset.variantId || null;
                const quantity = parseInt(qtyInput?.value) || 1;

                // Bundle validation
                if (isBundle && !validateBundleSelections()) {
                    // Highlight unselected variant dropdowns
                    document.querySelectorAll('.bundle-item__variant-select').forEach(sel => {
                        if (!sel.value) {
                            sel.style.borderColor = 'var(--theme-color-danger, #dc2626)';
                            setTimeout(() => { sel.style.borderColor = ''; }, 3000);
                        }
                    });
                    return;
                }

                // Show loading state
                const originalContent = this.innerHTML;
                this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> <span>Adding...</span>';
                this.disabled = true;

                // Build request body
                const body = {
                    product_id: productId,
                    variant_id: variantId,
                    quantity: quantity
                };

                // Add bundle selections if applicable
                if (isBundle) {
                    const { variantSelections, excludedOptionalItems } = collectBundleSelections();
                    if (Object.keys(variantSelections).length > 0) {
                        body.variant_selections = variantSelections;
                    }
                    if (excludedOptionalItems.length > 0) {
                        body.excluded_optional_items = excludedOptionalItems;
                    }
                }

                // Handle design editor: prepare design before adding to cart
                const addToCartBtn = this;
                const sendAddToCart = function(extraCustomizations) {
                    if (extraCustomizations) {
                        body.customizations = Object.assign(body.customizations || {}, extraCustomizations);
                    }
                    _doAddToCart(addToCartBtn, body, originalContent);
                };

                if (window.DesignEditor && document.getElementById('design-editor')
                    && document.getElementById('design-editor').style.display !== 'none') {
                    window.DesignEditor.prepareForCart()
                        .then(function(data) {
                            sendAddToCart(window.DesignEditor.getCartCustomizations());
                        })
                        .catch(function(err) {
                            addToCartBtn.innerHTML = '<i class="fas fa-times"></i> <span>Design Error</span>';
                            setTimeout(function() {
                                addToCartBtn.innerHTML = originalContent;
                                addToCartBtn.disabled = false;
                            }, 2000);
                        });
                    return;
                }

                // Send AJAX request (no design editor)
                _doAddToCart(this, body, originalContent);
            });
        }

        // Helper function for add-to-cart AJAX
        function _doAddToCart(btn, body, originalContent) {
            fetch('/api/cart/add/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify(body)
                })
                .then(response => response.json())
                .then(data => {
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
                        }

                        // Success state
                        btn.innerHTML = '<i class="fas fa-check"></i> <span>Added!</span>';
                        setTimeout(() => {
                            btn.innerHTML = originalContent;
                            btn.disabled = false;
                        }, 2000);
                    } else {
                        // Error state
                        btn.innerHTML = '<i class="fas fa-times"></i> <span>Error</span>';
                        setTimeout(() => {
                            btn.innerHTML = originalContent;
                            btn.disabled = false;
                        }, 2000);
                    }
                })
                .catch(error => {
                    console.error('Add to cart error:', error);
                    btn.innerHTML = originalContent;
                    btn.disabled = false;
                });
        }

        // CSRF token helper — meta tag (set in base.html) → hidden input
        function getCSRFToken() {
            var meta = document.querySelector('meta[name="csrf-token"]');
            if (meta && meta.content) return meta.content;
            var input = document.querySelector('[name=csrfmiddlewaretoken]');
            if (input) return input.value;
            return '';
        }

        // Express checkout buttons are now dynamically rendered and handled by base.html
        // See initExpressCheckoutButtons() and expressCheckout() in base.html
    });
})();
