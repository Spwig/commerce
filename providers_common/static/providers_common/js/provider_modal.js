/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Provider Detail Modal
 * =====================
 * Reusable modal for displaying detailed provider information.
 * Works with payment, shipping, email, and exchange rate providers.
 *
 * CSP-safe: No inline styles, no inline event handlers, no innerHTML with external data.
 * i18n-ready: All user-facing strings loaded from a JSON data island (#provider-modal-i18n).
 */

var ProviderModal = (function() {
    'use strict';

    var HIDDEN_CLASS = 'provider-modal-hidden';
    var BODY_LOCKED_CLASS = 'provider-modal-body-locked';

    /* ==========================================================
       i18n
       ========================================================== */

    var modalI18n = {};

    function loadModalI18n() {
        var el = document.getElementById('provider-modal-i18n');
        if (!el) return;
        try { modalI18n = JSON.parse(el.textContent); } catch (e) { /* ignore */ }
    }

    /**
     * Resolve a translated string with optional %(key)s parameter substitution.
     */
    function i18n(key, fallback, params) {
        var str = modalI18n[key] || fallback;
        if (params) {
            Object.keys(params).forEach(function(k) {
                str = str.replace(new RegExp('%\\(' + k + '\\)s', 'g'), String(params[k]));
            });
        }
        return str;
    }

    /* ==========================================================
       DOM helpers
       ========================================================== */

    function makeEl(tag, className, text) {
        var node = document.createElement(tag);
        if (className) node.className = className;
        if (text !== undefined) node.textContent = text;
        return node;
    }

    function makeIcon(faClass) {
        var i = document.createElement('i');
        i.className = 'fas ' + faClass;
        return i;
    }

    /**
     * Sanitise a URL for safe use in href attributes.
     * Only allows http: and https: protocols; returns '#' for anything else
     * (blocks javascript:, data:, vbscript:, etc.).
     */
    function safeUrl(url) {
        if (!url || typeof url !== 'string') return '#';
        var trimmed = url.replace(/^\s+/, '');
        if (/^https?:\/\//i.test(trimmed)) return trimmed;
        if (/^\/[^\/]/.test(trimmed) || trimmed === '/') return trimmed;
        return '#';
    }

    /* ==========================================================
       Brand data
       ========================================================== */

    var PAYMENT_METHOD_BRANDS = {
        'card': [
            { name: 'Visa', logo: 'cards/visa.svg' },
            { name: 'Mastercard', logo: 'cards/mastercard.svg' },
            { name: 'American Express', logo: 'cards/american-express.svg' },
            { name: 'Discover', logo: 'cards/discover.svg' },
            { name: 'JCB', logo: 'cards/jcb.svg' },
            { name: 'UnionPay', logo: 'cards/unionpay.svg' },
            { name: 'Diners Club', logo: 'cards/diners.svg' },
            { name: 'Maestro', logo: 'cards/maestro.svg' },
            { name: 'Cartes Bancaires', logo: 'cards/cartes-bancaires.svg' },
            { name: 'Dankort', logo: 'cards/dankort.svg' },
            { name: 'Elo', logo: 'cards/elo.svg' },
            { name: 'Hipercard', logo: 'cards/hipercard.svg' },
            { name: 'V PAY', logo: 'cards/vpay.svg' },
            { name: 'UATP', logo: 'cards/uatp.svg' }
        ],
        'digital_wallet': [
            { name: 'Apple Pay', logo: 'wallets/apple-pay.svg' },
            { name: 'Google Pay', logo: 'wallets/google-pay.svg' },
            { name: 'Samsung Pay', logo: 'wallets/samsung-pay.svg' },
            { name: 'PayPal', logo: 'alternative/paypal.svg' },
            { name: 'Alipay', logo: 'alternative/alipay.svg' },
            { name: 'Alipay+', logo: 'alternative/alipay-plus.svg' },
            { name: 'WeChat Pay', logo: 'alternative/wechat-pay.svg' },
            { name: 'Amazon Pay', logo: 'alternative/amazon-pay.svg' }
        ],
        'alternative': [
            { name: 'Klarna', logo: 'alternative/klarna.svg' },
            { name: 'Availabill', logo: 'alternative/availabill.svg' },
            { name: 'PowerPay', logo: 'alternative/powerpay.svg' },
            { name: 'CembraPay', logo: 'alternative/cembrapay.svg' },
            { name: 'iDEAL', logo: 'alternative/ideal.svg' },
            { name: 'Giropay', logo: 'alternative/giropay.svg' },
            { name: 'Bancontact', logo: 'alternative/bancontact.svg' },
            { name: 'EPS', logo: 'alternative/eps.svg' },
            { name: 'SEPA', logo: 'alternative/sepa.svg' },
            { name: 'Przelewy24', logo: 'alternative/przelewy24.svg' },
            { name: 'BLIK', logo: 'alternative/blik.svg' },
            { name: 'Swish', logo: 'alternative/swish.svg' },
            { name: 'MobilePay', logo: 'alternative/mobilepay.svg' },
            { name: 'Vipps', logo: 'alternative/vipps.svg' },
            { name: 'Paysafecard', logo: 'alternative/paysafecard.svg' },
            { name: 'Skrill', logo: 'alternative/skrill.svg' },
            { name: 'PostFinance Card', logo: 'alternative/postfinance-card.svg' },
            { name: 'PostFinance Pay', logo: 'alternative/postfinance-pay.svg' },
            { name: 'PostFinance E-Finance', logo: 'alternative/postfinance-efinance.svg' },
            { name: 'TWINT', logo: 'alternative/twint.svg' },
            { name: 'Swisscom Pay', logo: 'alternative/swisscom-pay.svg' },
            { name: 'SwissBilling', logo: 'alternative/swissbilling.svg' },
            { name: 'Reka', logo: 'alternative/reka.svg' },
            { name: 'Boncard', logo: 'alternative/boncard.svg' },
            { name: 'Bonus Card', logo: 'alternative/bonus-card.svg' },
            { name: 'Butterfly Card', logo: 'alternative/butterfly-card.svg' },
            { name: 'Half Fare+', logo: 'alternative/half-fare-plus.svg' },
            { name: 'Lunch Check', logo: 'alternative/lunch-check.svg' },
            { name: 'Migros Giftcard', logo: 'alternative/migros-giftcard.svg' },
            { name: 'Swisspass', logo: 'alternative/swisspass.svg' },
            { name: 'PointsPay', logo: 'alternative/pointspay.svg' },
            { name: 'PayCard', logo: 'alternative/paycard.svg' },
            { name: 'Cryptocurrency', logo: 'alternative/crypto.svg' },
            { name: 'eBill', logo: 'alternative/ebill.svg' },
            { name: 'CRIF', logo: 'alternative/crif.svg' },
            { name: 'MediaMarkt', logo: 'alternative/mediamarkt.svg' }
        ],
        'bank_transfer': [
            { name: 'SEPA', logo: 'alternative/sepa.svg' },
            { name: 'Invoice', logo: 'generic/invoice.svg' },
            { icon: 'fa-university', label: 'Bank Transfer' }
        ],
        'local_methods': [
            { icon: 'fa-globe', label: 'Local Payment Methods' }
        ]
    };

    var FEATURE_LABEL_KEYS = {
        'capture': 'paymentCapture',
        'authorize': 'authorization',
        'refund': 'refunds',
        'partial_refund': 'partialRefunds',
        'webhooks': 'webhookSupport',
        'recurring': 'recurringPayments',
        '3d_secure': 'threeDSecure',
        'multi_currency': 'multiCurrency',
        'save_payment_method': 'savePaymentMethods',
        'subscriptions': 'subscriptions'
    };

    var FEATURE_LABEL_DEFAULTS = {
        'capture': 'Payment Capture',
        'authorize': 'Authorization',
        'refund': 'Refunds',
        'partial_refund': 'Partial Refunds',
        'webhooks': 'Webhook Support',
        'recurring': 'Recurring Payments',
        '3d_secure': '3D Secure',
        'multi_currency': 'Multi-Currency',
        'save_payment_method': 'Save Payment Methods',
        'subscriptions': 'Subscriptions'
    };

    var GLOBAL_POPULAR_METHODS = [
        'Visa', 'Mastercard', 'American Express', 'PayPal',
        'Apple Pay', 'Google Pay', 'Discover', 'UnionPay'
    ];

    var LOCAL_POPULAR_METHODS = {
        'NL': ['iDEAL', 'Bancontact'],
        'DE': ['Giropay', 'SEPA', 'Klarna'],
        'BE': ['Bancontact', 'Klarna'],
        'AT': ['EPS', 'SEPA', 'Klarna'],
        'PL': ['Przelewy24', 'BLIK'],
        'SE': ['Swish', 'Klarna'],
        'NO': ['Vipps'],
        'DK': ['MobilePay', 'Dankort'],
        'FI': ['MobilePay'],
        'CH': ['PostFinance Card', 'PostFinance Pay', 'TWINT'],
        'FR': ['Cartes Bancaires', 'SEPA'],
        'IT': ['SEPA'],
        'ES': ['SEPA'],
        'BR': ['Elo', 'Hipercard'],
        'CN': ['Alipay', 'Alipay+', 'WeChat Pay', 'UnionPay'],
        'JP': ['JCB'],
        'IN': ['UPI'],
        'AU': ['POLi'],
        'GB': ['Klarna'],
        'US': ['Discover', 'Klarna']
    };

    /* ==========================================================
       State
       ========================================================== */

    var currentProviderData = null;
    var carouselInterval = null;
    var currentCarouselPage = 0;
    var touchStartX = 0;
    var touchEndX = 0;
    var resizeTimeout = null;

    /* ==========================================================
       Open / Close
       ========================================================== */

    function open(providerData) {
        currentProviderData = providerData;

        populateHeader(providerData);
        populateDescription(providerData);
        populatePaymentMethods(providerData);
        populateCurrencies(providerData);
        populateFeatures(providerData);
        populateRegions(providerData);
        populateCompliance(providerData);
        populatePricing(providerData);
        populateFooter(providerData);
        populateVersionHistory(providerData);

        var modal = document.getElementById('provider-detail-modal');
        modal.classList.remove(HIDDEN_CLASS);
        setTimeout(function() { modal.classList.add('active'); }, 10);
        document.body.classList.add(BODY_LOCKED_CLASS);
        window.addEventListener('resize', handleResize);
    }

    function close() {
        var modal = document.getElementById('provider-detail-modal');
        modal.classList.remove('active');
        stopCarouselCycle();
        window.removeEventListener('resize', handleResize);

        setTimeout(function() {
            modal.classList.add(HIDDEN_CLASS);
            document.body.classList.remove(BODY_LOCKED_CLASS);
        }, 300);

        currentProviderData = null;
        currentCarouselPage = 0;
    }

    /* ==========================================================
       Resize handler (responsive carousel rebuild)
       ========================================================== */

    function handleResize() {
        if (!currentProviderData) return;
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(function() {
            populatePaymentMethods(currentProviderData);
        }, 300);
    }

    /* ==========================================================
       Populate: Header
       ========================================================== */

    function populateHeader(data) {
        var logoContainer = document.getElementById('modal-provider-logo');
        logoContainer.innerHTML = '';

        if (data.thumbnail_url && safeUrl(data.thumbnail_url) !== '#') {
            var plate = makeEl('div', 'logo-plate');
            plate.setAttribute('data-auto-contrast', '');
            var img = document.createElement('img');
            img.src = safeUrl(data.thumbnail_url);
            img.alt = data.name || '';
            img.loading = 'lazy';
            img.crossOrigin = 'anonymous';
            plate.appendChild(img);
            logoContainer.appendChild(plate);
        } else {
            logoContainer.appendChild(makeIcon('fa-' + getDefaultIcon(data.provider_type)));
        }

        // Name (translate via ManifestI18n if available)
        var name = (typeof ManifestI18n !== 'undefined')
            ? ManifestI18n.translate(data.translations, 'meta.name', data.name)
            : data.name;
        document.getElementById('modal-provider-name').textContent = name;

        // Status badge
        var statusContainer = document.getElementById('modal-provider-status');
        statusContainer.innerHTML = '';

        var badge = makeEl('span', 'status-badge');
        if (data.is_installed) {
            badge.classList.add('status-installed');
            badge.appendChild(makeIcon('fa-check-circle'));
            badge.appendChild(document.createTextNode(' ' + i18n('installed', 'Installed')));
            statusContainer.appendChild(badge);
            if (data.current_version) {
                statusContainer.appendChild(makeEl('span', 'version-badge', 'v' + data.current_version));
            }
        } else {
            badge.classList.add('status-available');
            badge.appendChild(makeIcon('fa-download'));
            badge.appendChild(document.createTextNode(' ' + i18n('available', 'Available')));
            statusContainer.appendChild(badge);
            if (data.latest_version) {
                statusContainer.appendChild(makeEl('span', 'version-badge', 'v' + data.latest_version));
            }
        }
    }

    /* ==========================================================
       Populate: Description
       ========================================================== */

    function populateDescription(data) {
        var desc = (typeof ManifestI18n !== 'undefined')
            ? ManifestI18n.translate(data.translations, 'meta.description', data.description)
            : data.description;
        document.getElementById('modal-provider-description').textContent = desc || '';
    }

    /* ==========================================================
       Helpers
       ========================================================== */

    function getDefaultCountry() {
        return window.shopDefaultCountry || 'US';
    }

    function getItemsPerPage() {
        var width = window.innerWidth;
        if (width <= 480) return 6;
        if (width <= 768) return 8;
        return 12;
    }

    function getDefaultIcon(providerType) {
        var icons = {
            'payment': 'credit-card',
            'shipping': 'truck',
            'email': 'envelope',
            'exchange_rate': 'exchange-alt'
        };
        return icons[providerType] || 'puzzle-piece';
    }

    function getShippingCountries() {
        var dataEl = document.getElementById('shipping-countries-data');
        if (dataEl) {
            try { return JSON.parse(dataEl.textContent) || []; } catch (e) { /* ignore */ }
        }
        return window.merchantShippingCountries || [];
    }

    function getBrandLogosPath() {
        var modal = document.getElementById('provider-detail-modal');
        return (modal && modal.dataset.brandLogosPath) || '/static/providers_common/images/brands/payment_methods/';
    }

    /* ==========================================================
       Brand sorting
       ========================================================== */

    function sortBrandsByPopularity(brands, defaultCountry) {
        var globalPopular = [];
        var localPopular = [];
        var others = [];
        var localMethods = LOCAL_POPULAR_METHODS[defaultCountry] || [];

        brands.forEach(function(brand) {
            if (GLOBAL_POPULAR_METHODS.indexOf(brand.name) !== -1) {
                globalPopular.push(brand);
            } else if (localMethods.indexOf(brand.name) !== -1) {
                localPopular.push(brand);
            } else {
                others.push(brand);
            }
        });

        var sortByPriority = function(a, b, list) {
            var ia = list.indexOf(a.name);
            var ib = list.indexOf(b.name);
            if (ia === -1) return 1;
            if (ib === -1) return -1;
            return ia - ib;
        };

        globalPopular.sort(function(a, b) { return sortByPriority(a, b, GLOBAL_POPULAR_METHODS); });
        localPopular.sort(function(a, b) { return sortByPriority(a, b, localMethods); });

        return globalPopular.concat(localPopular, others);
    }

    /* ==========================================================
       Brand card DOM builder
       ========================================================== */

    function createBrandCard(brand, brandLogosPath) {
        var card = makeEl('div', 'payment-brand-card');
        if (brand.logo) {
            var img = document.createElement('img');
            img.src = brandLogosPath + brand.logo;
            img.alt = brand.name;
            img.title = brand.name;
            card.appendChild(img);
        } else if (brand.icon) {
            var wrapper = makeEl('div', 'payment-brand-icon');
            wrapper.appendChild(makeIcon(brand.icon));
            wrapper.appendChild(makeEl('span', null, brand.label));
            card.appendChild(wrapper);
        }
        return card;
    }

    /* ==========================================================
       Payment methods carousel
       ========================================================== */

    function createPaymentMethodCarousel(brands, brandLogosPath) {
        var itemsPerPage = getItemsPerPage();
        var totalPages = Math.ceil(brands.length / itemsPerPage);

        var container = makeEl('div', 'payment-methods-carousel');
        var track = makeEl('div', 'payment-methods-carousel-track');

        for (var page = 0; page < totalPages; page++) {
            var pageEl = makeEl('div', 'payment-methods-carousel-page');
            var start = page * itemsPerPage;
            var end = Math.min(start + itemsPerPage, brands.length);

            brands.slice(start, end).forEach(function(brand) {
                pageEl.appendChild(createBrandCard(brand, brandLogosPath));
            });
            track.appendChild(pageEl);
        }
        container.appendChild(track);

        if (totalPages > 1) {
            var nav = makeEl('div', 'payment-methods-carousel-nav');

            var prevBtn = makeEl('button', 'carousel-nav-btn carousel-prev');
            prevBtn.appendChild(makeIcon('fa-chevron-left'));
            prevBtn.setAttribute('data-action', 'carousel-prev');
            nav.appendChild(prevBtn);

            var indicators = makeEl('div', 'carousel-indicators');
            for (var idx = 0; idx < totalPages; idx++) {
                var dot = makeEl('button', 'carousel-indicator' + (idx === 0 ? ' active' : ''));
                dot.setAttribute('data-action', 'carousel-goto');
                dot.setAttribute('data-page', String(idx));
                indicators.appendChild(dot);
            }
            nav.appendChild(indicators);

            var nextBtn = makeEl('button', 'carousel-nav-btn carousel-next');
            nextBtn.appendChild(makeIcon('fa-chevron-right'));
            nextBtn.setAttribute('data-action', 'carousel-next');
            nav.appendChild(nextBtn);

            container.appendChild(nav);
            startCarouselCycle(totalPages);
            setupTouchHandlers(container);
        }
        return container;
    }

    function setupTouchHandlers(container) {
        var track = container.querySelector('.payment-methods-carousel-track');
        if (!track) return;
        track.addEventListener('touchstart', function(e) {
            touchStartX = e.changedTouches[0].screenX;
        }, { passive: true });
        track.addEventListener('touchend', function(e) {
            touchEndX = e.changedTouches[0].screenX;
            handleSwipe();
        }, { passive: true });
    }

    function handleSwipe() {
        var diff = touchStartX - touchEndX;
        if (diff > 50) navigateCarousel(1);
        else if (diff < -50) navigateCarousel(-1);
        touchStartX = 0;
        touchEndX = 0;
    }

    function navigateCarousel(direction) {
        var track = document.querySelector('.payment-methods-carousel-track');
        if (!track) return;
        var pages = track.querySelectorAll('.payment-methods-carousel-page');
        var indicators = document.querySelectorAll('.carousel-indicator');
        var total = pages.length;

        stopCarouselCycle();
        currentCarouselPage = (currentCarouselPage + direction + total) % total;
        track.style.transform = 'translateX(-' + (currentCarouselPage * 100) + '%)';
        indicators.forEach(function(ind, i) { ind.classList.toggle('active', i === currentCarouselPage); });
        setTimeout(function() { startCarouselCycle(total); }, 5000);
    }

    function goToCarouselPage(pageIndex) {
        var track = document.querySelector('.payment-methods-carousel-track');
        if (!track) return;
        var indicators = document.querySelectorAll('.carousel-indicator');

        stopCarouselCycle();
        currentCarouselPage = pageIndex;
        track.style.transform = 'translateX(-' + (currentCarouselPage * 100) + '%)';
        indicators.forEach(function(ind, i) { ind.classList.toggle('active', i === currentCarouselPage); });
        setTimeout(function() { startCarouselCycle(indicators.length); }, 5000);
    }

    function startCarouselCycle(totalPages) {
        stopCarouselCycle();
        if (totalPages <= 1) return;
        carouselInterval = setInterval(function() { navigateCarousel(1); }, 4000);
    }

    function stopCarouselCycle() {
        if (carouselInterval) { clearInterval(carouselInterval); carouselInterval = null; }
    }

    /* ==========================================================
       Populate: Payment Methods
       ========================================================== */

    function populatePaymentMethods(data) {
        var section = document.getElementById('modal-payment-methods-section');
        var grid = document.getElementById('modal-payment-methods-grid');

        if (!data.capabilities || !data.capabilities.payment_methods || data.provider_type !== 'payment') {
            section.classList.add(HIDDEN_CLASS);
            return;
        }

        section.classList.remove(HIDDEN_CLASS);
        grid.innerHTML = '';
        currentCarouselPage = 0;
        stopCarouselCycle();

        var brandLogosPath = getBrandLogosPath();
        var defaultCountry = getDefaultCountry();

        var allBrands = [];
        data.capabilities.payment_methods.forEach(function(method) {
            if (PAYMENT_METHOD_BRANDS[method]) {
                allBrands = allBrands.concat(PAYMENT_METHOD_BRANDS[method]);
            }
        });

        var sorted = sortBrandsByPopularity(allBrands, defaultCountry);
        var itemsPerPage = getItemsPerPage();

        if (sorted.length > itemsPerPage) {
            grid.appendChild(createPaymentMethodCarousel(sorted, brandLogosPath));
        } else {
            sorted.forEach(function(brand) {
                grid.appendChild(createBrandCard(brand, brandLogosPath));
            });
        }
    }

    /* ==========================================================
       Populate: Currencies
       ========================================================== */

    function populateCurrencies(data) {
        var section = document.getElementById('modal-currencies-section');
        var list = document.getElementById('modal-currencies-list');

        if (!data.capabilities || !data.capabilities.supported_currencies || data.capabilities.supported_currencies.length === 0) {
            section.classList.add(HIDDEN_CLASS);
            return;
        }

        section.classList.remove(HIDDEN_CLASS);
        list.innerHTML = '';

        var currencies = data.capabilities.supported_currencies;
        currencies.slice(0, 15).forEach(function(c) {
            list.appendChild(makeEl('span', 'currency-pill', c));
        });

        var remaining = currencies.length - 15;
        if (remaining > 0) {
            list.appendChild(makeEl('span', 'currency-pill currency-pill-more',
                i18n('moreCount', '+%(count)s more', { count: remaining })
            ));
        }
    }

    /* ==========================================================
       Populate: Features
       ========================================================== */

    function populateFeatures(data) {
        var section = document.getElementById('modal-features-section');
        var grid = document.getElementById('modal-features-grid');

        if (!data.capabilities || !data.capabilities.features) {
            section.classList.add(HIDDEN_CLASS);
            return;
        }

        section.classList.remove(HIDDEN_CLASS);
        grid.innerHTML = '';

        var features = data.capabilities.features;
        Object.keys(features).forEach(function(key) {
            if (!features[key]) return;

            var item = makeEl('div', 'feature-check-item');
            item.appendChild(makeIcon('fa-check-circle'));

            var i18nKey = FEATURE_LABEL_KEYS[key];
            var fallback = FEATURE_LABEL_DEFAULTS[key]
                || key.replace(/_/g, ' ').replace(/\b\w/g, function(l) { return l.toUpperCase(); });
            item.appendChild(makeEl('span', null, i18nKey ? i18n(i18nKey, fallback) : fallback));

            grid.appendChild(item);
        });
    }

    /* ==========================================================
       Populate: Geographic Coverage
       ========================================================== */

    function populateRegions(data) {
        var section = document.getElementById('modal-regions-section');
        var info = document.getElementById('modal-regions-info');

        if (!data.regions) {
            section.classList.add(HIDDEN_CLASS);
            return;
        }

        section.classList.remove(HIDDEN_CLASS);
        info.innerHTML = '';

        var supported = data.regions.supported || [];
        var restricted = data.regions.restricted || [];
        var notes = data.regions.notes || '';
        var shippingCountries = getShippingCountries();

        var container = makeEl('div', 'region-info');
        var isGlobal = supported.indexOf('global') !== -1 || supported.indexOf('worldwide') !== -1;

        if (isGlobal) {
            var globalBadge = makeEl('div', 'region-badge global');
            globalBadge.appendChild(makeIcon('fa-globe'));
            globalBadge.appendChild(document.createTextNode(' ' + i18n('globalCoverage', 'Global Coverage')));
            container.appendChild(globalBadge);

            if (shippingCountries.length > 0) {
                var unsupported = shippingCountries.filter(function(c) { return restricted.indexOf(c) !== -1; });
                var compat = makeEl('p', 'region-compat');

                if (unsupported.length === 0) {
                    compat.classList.add('success');
                    compat.appendChild(makeIcon('fa-check-circle'));
                    compat.appendChild(document.createTextNode(' ' + i18n(
                        'supportsAllCountries',
                        'Supports all your %(count)s shipping %(noun)s',
                        { count: shippingCountries.length, noun: shippingCountries.length === 1 ? i18n('country', 'country') : i18n('countries', 'countries') }
                    )));
                } else {
                    compat.classList.add('warning');
                    compat.appendChild(makeIcon('fa-exclamation-triangle'));
                    compat.appendChild(document.createTextNode(' ' + i18n(
                        'doesNotSupportCountries',
                        'Does not support %(count)s of your shipping countries',
                        { count: unsupported.length }
                    )));
                }
                container.appendChild(compat);
            }
        } else if (supported.length > 0) {
            if (shippingCountries.length > 0) {
                var supportedShipping = shippingCountries.filter(function(c) {
                    return supported.indexOf(c) !== -1 && restricted.indexOf(c) === -1;
                });
                var unsupportedShipping = shippingCountries.filter(function(c) {
                    return supported.indexOf(c) === -1 || restricted.indexOf(c) !== -1;
                });

                var compatEl = makeEl('p', 'region-compat');
                if (supportedShipping.length > 0) {
                    compatEl.classList.add(unsupportedShipping.length === 0 ? 'success' : 'partial');
                    compatEl.appendChild(makeIcon(unsupportedShipping.length === 0 ? 'fa-check-circle' : 'fa-info-circle'));
                    compatEl.appendChild(document.createTextNode(' ' + i18n(
                        'supportsPartialCountries',
                        'Supports %(supported)s of your %(total)s shipping %(noun)s',
                        {
                            supported: supportedShipping.length,
                            total: shippingCountries.length,
                            noun: shippingCountries.length === 1 ? i18n('country', 'country') : i18n('countries', 'countries')
                        }
                    )));
                } else {
                    compatEl.classList.add('error');
                    compatEl.appendChild(makeIcon('fa-times-circle'));
                    compatEl.appendChild(document.createTextNode(' ' + i18n('doesNotSupportAny', 'Does not support any of your shipping countries')));
                }
                container.appendChild(compatEl);
            }

            var badgesWrap = makeEl('div', 'region-badges');
            supported.slice(0, 20).forEach(function(region) {
                var isShipping = shippingCountries.indexOf(region) !== -1;
                var badge = makeEl('div', 'region-badge' + (isShipping ? ' highlight' : ''));
                badge.appendChild(makeIcon('fa-map-marker-alt'));
                badge.appendChild(document.createTextNode(' ' + region.toUpperCase()));
                badgesWrap.appendChild(badge);
            });
            if (supported.length > 20) {
                badgesWrap.appendChild(makeEl('div', 'region-badge more', '+' + (supported.length - 20) + ' more'));
            }
            container.appendChild(badgesWrap);
        }

        if (notes) {
            container.appendChild(makeEl('p', 'region-notes', notes));
        }

        info.appendChild(container);
    }

    /* ==========================================================
       Populate: Compliance
       ========================================================== */

    function populateCompliance(data) {
        var section = document.getElementById('modal-compliance-section');
        var badges = document.getElementById('modal-compliance-badges');

        if (!data.compliance) {
            section.classList.add(HIDDEN_CLASS);
            return;
        }

        section.classList.remove(HIDDEN_CLASS);
        badges.innerHTML = '';

        if (data.compliance.pci_dss) {
            var pci = makeEl('div', 'compliance-badge');
            pci.appendChild(makeIcon('fa-shield-alt'));
            pci.appendChild(makeEl('span', null, i18n('pciDssCompliant', 'PCI DSS Compliant')));
            badges.appendChild(pci);
        }

        if (data.compliance.certifications && data.compliance.certifications.length > 0) {
            data.compliance.certifications.forEach(function(cert) {
                var b = makeEl('div', 'compliance-badge');
                b.appendChild(makeIcon('fa-certificate'));
                b.appendChild(makeEl('span', null, cert));
                badges.appendChild(b);
            });
        }
    }

    /* ==========================================================
       Populate: Pricing
       ========================================================== */

    function populatePricing(data) {
        var section = document.getElementById('modal-pricing-section');
        var info = document.getElementById('modal-pricing-info');

        if (!data.pricing_info) {
            section.classList.add(HIDDEN_CLASS);
            return;
        }

        section.classList.remove(HIDDEN_CLASS);
        info.innerHTML = '';

        var container = makeEl('div', 'pricing-info');

        if (data.pricing_info.transaction_fee) {
            var txItem = makeEl('div', 'pricing-item');
            txItem.appendChild(makeIcon('fa-percentage'));
            var txContent = document.createElement('div');
            var txLabel = document.createElement('strong');
            txLabel.textContent = i18n('transactionFee', 'Transaction Fee:');
            txContent.appendChild(txLabel);
            txContent.appendChild(makeEl('span', null, data.pricing_info.transaction_fee));
            txItem.appendChild(txContent);
            container.appendChild(txItem);
        }

        if (data.pricing_info.setup_fee) {
            var sfItem = makeEl('div', 'pricing-item');
            sfItem.appendChild(makeIcon('fa-dollar-sign'));
            var sfContent = document.createElement('div');
            var sfLabel = document.createElement('strong');
            sfLabel.textContent = i18n('setupFee', 'Setup Fee:');
            sfContent.appendChild(sfLabel);
            sfContent.appendChild(makeEl('span', null, data.pricing_info.setup_fee));
            sfItem.appendChild(sfContent);
            container.appendChild(sfItem);
        }

        if (data.pricing_info.notes) {
            container.appendChild(makeEl('p', 'pricing-notes', data.pricing_info.notes));
        }

        info.appendChild(container);
    }

    /* ==========================================================
       Populate: Footer
       ========================================================== */

    function populateFooter(data) {
        var actions = document.getElementById('modal-provider-actions');
        actions.innerHTML = '';

        if (data.is_installed) {
            if (data.has_update) {
                var updateBtn = makeEl('button', 'button btn-update');
                updateBtn.setAttribute('data-action', 'update-provider');
                updateBtn.dataset.slug = data.slug || '';
                updateBtn.dataset.version = data.latest_version || '';
                updateBtn.appendChild(makeIcon('fa-sync-alt'));
                updateBtn.appendChild(document.createTextNode(
                    ' ' + i18n('updateTo', 'Update to v%(version)s', { version: data.latest_version || '' })
                ));
                actions.appendChild(updateBtn);
            } else {
                var configLink = document.createElement('a');
                configLink.href = safeUrl(data.configure_url);
                configLink.className = 'button';
                configLink.appendChild(makeIcon('fa-cog'));
                configLink.appendChild(document.createTextNode(' ' + i18n('configure', 'Configure')));
                actions.appendChild(configLink);
            }
        } else {
            var installBtn = makeEl('button', 'button btn-install');
            installBtn.setAttribute('data-action', 'install-provider');
            installBtn.dataset.providerSlug = data.slug || '';
            installBtn.dataset.providerName = data.name || '';
            installBtn.appendChild(makeIcon('fa-download'));
            installBtn.appendChild(document.createTextNode(' ' + i18n('installProvider', 'Install Provider')));
            actions.appendChild(installBtn);
        }

        // Documentation link
        var docsLink = document.getElementById('modal-provider-docs');
        if (data.documentation_url) {
            docsLink.href = safeUrl(data.documentation_url);
            docsLink.classList.remove(HIDDEN_CLASS);
        } else {
            docsLink.classList.add(HIDDEN_CLASS);
        }

        // Website link
        var websiteLink = document.getElementById('modal-provider-website');
        if (data.homepage_url) {
            websiteLink.href = safeUrl(data.homepage_url);
            websiteLink.classList.remove(HIDDEN_CLASS);
        } else {
            websiteLink.classList.add(HIDDEN_CLASS);
        }
    }

    /* ==========================================================
       Version History (collapsible, lazy-loaded)
       ========================================================== */

    function populateVersionHistory(data) {
        var section = document.getElementById('modal-version-history-section');
        var content = document.getElementById('modal-version-history-content');
        if (!section || !content) return;

        // Only show if we have a slug (update-server component)
        if (!data.slug) {
            section.classList.add(HIDDEN_CLASS);
            return;
        }

        section.classList.remove(HIDDEN_CLASS);
        content.classList.add(HIDDEN_CLASS); // Start collapsed

        // Reset toggle icon
        var icon = section.querySelector('.version-history-toggle-icon');
        if (icon) {
            icon.classList.remove('fa-chevron-up');
            icon.classList.add('fa-chevron-down');
        }

        // Reset loading placeholder
        content.innerHTML = '';
        var loadingP = makeEl('p', 'version-history-loading');
        loadingP.appendChild(makeIcon('fa-spinner fa-spin'));
        loadingP.appendChild(document.createTextNode(' ' + i18n('loading', 'Loading...')));
        content.appendChild(loadingP);

        // Mark as not-yet-loaded for lazy fetch on expand
        section.dataset.loaded = 'false';
    }

    function toggleVersionHistory() {
        var section = document.getElementById('modal-version-history-section');
        var content = document.getElementById('modal-version-history-content');
        if (!section || !content) return;

        var icon = section.querySelector('.version-history-toggle-icon');
        var isHidden = content.classList.contains(HIDDEN_CLASS);

        if (isHidden) {
            content.classList.remove(HIDDEN_CLASS);
            if (icon) {
                icon.classList.remove('fa-chevron-down');
                icon.classList.add('fa-chevron-up');
            }

            // Lazy load on first expand
            if (section.dataset.loaded !== 'true' && currentProviderData && currentProviderData.slug) {
                if (typeof VersionHistory !== 'undefined') {
                    VersionHistory.fetch(currentProviderData.slug).then(function(versions) {
                        content.innerHTML = '';
                        content.appendChild(VersionHistory.render(versions));
                        section.dataset.loaded = 'true';
                    }).catch(function() {
                        content.innerHTML = '';
                        content.appendChild(
                            makeEl('p', 'version-history-empty',
                                i18n('errorLoadingVersions', 'Could not load version history.'))
                        );
                    });
                }
            }
        } else {
            content.classList.add(HIDDEN_CLASS);
            if (icon) {
                icon.classList.remove('fa-chevron-up');
                icon.classList.add('fa-chevron-down');
            }
        }
    }

    /* ==========================================================
       Install / Update handlers
       ========================================================== */

    function handleInstall(slug, name) {
        close();
        if (window.installProvider) {
            window.installProvider(slug, name);
        } else {
            console.warn('ProviderModal: installProvider handler not found on page');
        }
    }

    function handleUpdate(slug, version, name) {
        close();
        if (window.updateProvider) {
            window.updateProvider(slug, version, name);
        } else {
            console.warn('ProviderModal: updateProvider handler not found on page');
        }
    }

    /* ==========================================================
       Event listeners (all CSP-safe, delegated)
       ========================================================== */

    // Close on overlay click
    document.addEventListener('click', function(e) {
        if (e.target && e.target.id === 'provider-detail-modal') {
            close();
        }
    });

    // Close on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && currentProviderData) {
            close();
        }
    });

    // Delegated click handler for all data-action elements
    document.addEventListener('click', function(e) {
        var target = e.target.closest('[data-action]');
        if (!target) return;

        var action = target.getAttribute('data-action');
        switch (action) {
            case 'close-provider-modal':
                close();
                break;
            case 'install-provider':
                handleInstall(target.dataset.providerSlug || '', target.dataset.providerName || '');
                break;
            case 'update-provider':
                handleUpdate(target.dataset.slug || '', target.dataset.version || '', currentProviderData ? currentProviderData.name : '');
                break;
            case 'toggle-version-history':
                toggleVersionHistory();
                break;
            case 'carousel-prev':
                navigateCarousel(-1);
                break;
            case 'carousel-next':
                navigateCarousel(1);
                break;
            case 'carousel-goto':
                var page = parseInt(target.dataset.page, 10);
                if (!isNaN(page)) goToCarouselPage(page);
                break;
        }
    });

    // Load i18n strings once DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        loadModalI18n();
    });

    /* ==========================================================
       Public API
       ========================================================== */

    return {
        open: open,
        close: close,
        handleInstall: handleInstall,
        handleUpdate: handleUpdate
    };
})();
