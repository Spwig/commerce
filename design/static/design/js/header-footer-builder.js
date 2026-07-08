/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

// Read builder configuration from JSON data island (CSP-safe)
(function () {
    var configEl = document.getElementById('hf-builder-config');
    if (configEl) {
        try { window.HFBuilderConfig = JSON.parse(configEl.textContent); }
        catch (e) { window.HFBuilderConfig = {}; }
    }
}());

/**
 * Header/Footer Visual Builder
 * Following rules.md: Uses admin theme variables, no inline styles
 * Main builder class for drag-and-drop header/footer editing
 */

/**
 * Widget Property Schemas
 * Schemas are now loaded dynamically from the API endpoint: /api/widget-schemas/
 * JSON schema files are stored at: design/templates/design/widgets/*.json
 * This eliminates ~580 lines of hardcoded JavaScript and makes schemas easier to maintain.
 *
 * Schema structure:
 * {
 *   "type": "widget_type",
 *   "icon": "fa-icon-name",
 *   "label": "Display Name",
 *   "groups": [
 *     {
 *       "id": "group-id",
 *       "title": "Group Title",
 *       "expanded": boolean,
 *       "fields": [
 *         { "key": "config-key", "label": "Label", "type": "text|select|toggle|media|...", "default": value }
 *       ]
 *     }
 *   ]
 * }
 */

// NOTE: Widget schemas are now loaded dynamically from the API: /api/widget-schemas/
// JSON schema files are stored at: design/templates/design/widgets/*.json
// The WIDGET_SCHEMAS constant below is kept as a fallback but is no longer the primary source.
// To modify widget schemas, edit the corresponding .json file, not this JavaScript.

const WIDGET_SCHEMAS = {
    logo: {
        icon: 'fa-image',
        label: 'Logo',
        groups: [
            {
                id: 'general',
                title: 'General Settings',
                expanded: true,
                fields: [
                    { key: 'text', label: 'Logo Text', type: 'text', placeholder: 'Your Brand', help: 'Shown when no image' },
                    { key: 'alt_text', label: 'Alt Text', type: 'text', placeholder: 'Brand logo' }
                ]
            },
            {
                id: 'image',
                title: 'Logo Image',
                expanded: true,
                fields: [
                    { key: 'logo_url', label: 'Logo Image', type: 'media', placeholder: 'Select image' },
                    { key: 'width', label: 'Width', type: 'text', placeholder: 'auto', help: 'e.g., 150px or auto' },
                    { key: 'height', label: 'Height', type: 'text', placeholder: 'auto' }
                ]
            },
            {
                id: 'link',
                title: 'Link Settings',
                expanded: false,
                fields: [
                    { key: 'link_url', label: 'Link URL', type: 'url', default: '/', placeholder: '/' }
                ]
            }
        ]
    },

    menu: {
        icon: 'fa-bars',
        label: 'Menu',
        groups: [
            {
                id: 'source',
                title: 'Menu Source',
                expanded: true,
                fields: [
                    { key: 'menu_id', label: 'Select Menu', type: 'select', dynamicOptions: 'menus', placeholder: 'Choose a menu...' }
                ]
            },
            {
                id: 'display',
                title: 'Display Options',
                expanded: true,
                fields: [
                    {
                        key: 'display_type',
                        label: 'Display Style',
                        type: 'select',
                        options: [
                            { value: 'horizontal', label: 'Horizontal' },
                            { value: 'vertical', label: 'Vertical' },
                            { value: 'dropdown', label: 'Dropdown' },
                            { value: 'mega', label: 'Mega Menu' }
                        ],
                        default: 'horizontal'
                    }
                ]
            }
        ]
    },

    search: {
        icon: 'fa-search',
        label: 'Search',
        groups: [
            {
                id: 'general',
                title: 'General Settings',
                expanded: true,
                fields: [
                    { key: 'placeholder', label: 'Placeholder', type: 'text', default: 'Search...', placeholder: 'Search...' },
                    { key: 'search_url', label: 'Search URL', type: 'url', default: '/search/', placeholder: '/search/' }
                ]
            },
            {
                id: 'autocomplete',
                title: 'Autocomplete',
                expanded: true,
                fields: [
                    { key: 'autocomplete_enabled', label: 'Enable Autocomplete', type: 'toggle', default: true },
                    { key: 'max_results', label: 'Max Results', type: 'number', default: 8, min: 1, max: 20 },
                    { key: 'debounce_ms', label: 'Debounce (ms)', type: 'number', default: 300, min: 100, max: 1000 }
                ]
            },
            {
                id: 'display',
                title: 'Display Options',
                expanded: false,
                fields: [
                    { key: 'show_text', label: 'Show Button Text', type: 'toggle', default: false },
                    { key: 'autofocus', label: 'Autofocus on Load', type: 'toggle', default: false }
                ]
            }
        ]
    },

    cart: {
        icon: 'fa-shopping-cart',
        label: 'Cart',
        groups: [
            {
                id: 'behavior',
                title: 'Behavior',
                expanded: true,
                fields: [
                    {
                        key: 'click_action',
                        label: 'Click Action',
                        type: 'select',
                        options: [
                            { value: 'open_mini_cart', label: 'Open Mini-Cart (Recommended)' },
                            { value: 'link_to_cart', label: 'Go to Cart Page' }
                        ],
                        default: 'open_mini_cart',
                        help: 'Choose what happens when users click the cart button'
                    },
                    { key: 'cart_url', label: 'Cart Page URL', type: 'url', default: '/cart/', placeholder: '/cart/', help: 'URL for cart page (only used when Click Action is "Go to Cart Page")' }
                ]
            },
            {
                id: 'display',
                title: 'Display Options',
                expanded: true,
                fields: [
                    {
                        key: 'icon_style',
                        label: 'Icon Style',
                        type: 'select',
                        options: [
                            { value: 'cart', label: 'Shopping Cart' },
                            { value: 'bag', label: 'Shopping Bag' },
                            { value: 'basket', label: 'Shopping Basket' }
                        ],
                        default: 'cart'
                    },
                    { key: 'show_text', label: 'Show Text Label', type: 'toggle', default: false, help: 'Display "Cart" text next to the icon' },
                    { key: 'text', label: 'Button Text', type: 'text', placeholder: 'Cart', help: 'Custom text label (leave empty for default)' },
                    { key: 'show_total', label: 'Show Cart Total', type: 'toggle', default: false, help: 'Display the cart total amount' }
                ]
            }
        ]
    },

    account: {
        icon: 'fa-user',
        label: 'Account Menu',
        groups: [
            {
                id: 'menu',
                title: 'Menu Source',
                expanded: true,
                fields: [
                    { key: 'menu_id', label: 'Account Menu', type: 'select', dynamicOptions: 'account_menus', placeholder: 'Use default account menu', help: 'Select which menu to display. Leave empty for default.' }
                ]
            },
            {
                id: 'display',
                title: 'Display Options',
                expanded: true,
                fields: [
                    { key: 'show_avatar', label: 'Show Avatar', type: 'toggle', default: false, help: 'Display user avatar when logged in' },
                    { key: 'show_name', label: 'Show Name', type: 'toggle', default: false, help: 'Display username when logged in' },
                    { key: 'show_text', label: 'Show Button Text', type: 'toggle', default: true, help: 'Show text labels on login/register buttons' },
                    { key: 'show_register', label: 'Show Register Link', type: 'toggle', default: true, help: 'Show register button for anonymous users' }
                ]
            }
        ]
    },

    language: {
        icon: 'fa-globe',
        label: 'Language',
        groups: [
            {
                id: 'display',
                title: 'Display Options',
                expanded: true,
                fields: [
                    { key: 'show_flags', label: 'Show Flags', type: 'toggle', default: true },
                    {
                        key: 'display_type',
                        label: 'Display Format',
                        type: 'select',
                        options: [
                            { value: 'code', label: 'Language Code (EN)' },
                            { value: 'native', label: 'Native Name (English)' },
                            { value: 'name', label: 'Translated Name' }
                        ],
                        default: 'code'
                    }
                ]
            }
        ]
    },

    currency: {
        icon: 'fa-dollar-sign',
        label: 'Currency',
        groups: [
            {
                id: 'display',
                title: 'Display Options',
                expanded: true,
                fields: [
                    {
                        key: 'display_style',
                        label: 'Display Style',
                        type: 'select',
                        options: [
                            { value: 'symbol_code', label: 'Symbol + Code ($ USD)' },
                            { value: 'symbol_only', label: 'Symbol Only ($)' },
                            { value: 'code_only', label: 'Code Only (USD)' },
                            { value: 'flag_code', label: 'Flag + Code' },
                            { value: 'flag_name', label: 'Flag + Name' }
                        ],
                        default: 'symbol_code'
                    },
                    { key: 'show_current_only', label: 'Compact Mode', type: 'toggle', default: false, help: 'Show only current currency' },
                    {
                        key: 'dropdown_position',
                        label: 'Dropdown Position',
                        type: 'select',
                        options: [
                            { value: 'bottom', label: 'Bottom' },
                            { value: 'top', label: 'Top' },
                            { value: 'left', label: 'Left' },
                            { value: 'right', label: 'Right' }
                        ],
                        default: 'bottom'
                    },
                    {
                        key: 'button_style',
                        label: 'Button Style',
                        type: 'select',
                        options: [
                            { value: 'outline', label: 'Outline' },
                            { value: 'solid', label: 'Solid' },
                            { value: 'ghost', label: 'Ghost' }
                        ],
                        default: 'outline'
                    }
                ]
            }
        ]
    },

    social: {
        icon: 'fa-share-alt',
        label: 'Social',
        groups: [
            {
                id: 'general',
                title: 'General Settings',
                expanded: true,
                fields: [
                    { key: 'title', label: 'Section Title', type: 'text', placeholder: 'Follow Us' },
                    { key: 'show_text', label: 'Show Labels', type: 'toggle', default: false }
                ]
            },
            {
                id: 'links',
                title: 'Social Links',
                expanded: true,
                singleColumn: true,
                fields: [
                    { key: 'facebook', label: 'Facebook URL', type: 'url', placeholder: 'https://facebook.com/...' },
                    { key: 'twitter', label: 'Twitter/X URL', type: 'url', placeholder: 'https://twitter.com/...' },
                    { key: 'instagram', label: 'Instagram URL', type: 'url', placeholder: 'https://instagram.com/...' },
                    { key: 'youtube', label: 'YouTube URL', type: 'url', placeholder: 'https://youtube.com/...' },
                    { key: 'linkedin', label: 'LinkedIn URL', type: 'url', placeholder: 'https://linkedin.com/...' },
                    { key: 'pinterest', label: 'Pinterest URL', type: 'url', placeholder: 'https://pinterest.com/...' },
                    { key: 'tiktok', label: 'TikTok URL', type: 'url', placeholder: 'https://tiktok.com/...' }
                ]
            }
        ]
    },

    newsletter: {
        icon: 'fa-envelope',
        label: 'Newsletter',
        groups: [
            {
                id: 'content',
                title: 'Content',
                expanded: true,
                fields: [
                    { key: 'title', label: 'Title', type: 'text', default: 'Subscribe to our Newsletter', placeholder: 'Subscribe...' },
                    { key: 'description', label: 'Description', type: 'textarea', placeholder: 'Get updates on new products and promotions...' },
                    { key: 'placeholder', label: 'Email Placeholder', type: 'text', default: 'Enter your email', placeholder: 'Enter your email' },
                    { key: 'button_text', label: 'Button Text', type: 'text', default: 'Subscribe', placeholder: 'Subscribe' }
                ]
            },
            {
                id: 'settings',
                title: 'Settings',
                expanded: false,
                fields: [
                    { key: 'action_url', label: 'Form Action URL', type: 'url', default: '/newsletter/subscribe/', placeholder: '/newsletter/subscribe/' },
                    { key: 'show_privacy', label: 'Show Privacy Link', type: 'toggle', default: true },
                    { key: 'privacy_url', label: 'Privacy Policy URL', type: 'url', default: '/privacy-policy/', placeholder: '/privacy-policy/' }
                ]
            }
        ]
    },

    contact: {
        icon: 'fa-phone',
        label: 'Contact',
        groups: [
            {
                id: 'content',
                title: 'Contact Information',
                expanded: true,
                singleColumn: true,
                fields: [
                    { key: 'title', label: 'Title', type: 'text', placeholder: 'Contact Us' },
                    { key: 'phone', label: 'Phone', type: 'text', placeholder: '+1 (555) 123-4567' },
                    { key: 'email', label: 'Email', type: 'text', placeholder: 'info@example.com' },
                    { key: 'address', label: 'Address', type: 'textarea', placeholder: '123 Main St\nCity, State 12345' },
                    { key: 'hours', label: 'Business Hours', type: 'textarea', placeholder: 'Mon-Fri: 9am-5pm\nSat-Sun: Closed' }
                ]
            },
            {
                id: 'map',
                title: 'Map',
                expanded: false,
                singleColumn: true,
                fields: [
                    { key: 'show_map', label: 'Show Map', type: 'toggle', default: false },
                    { key: 'map_embed', label: 'Map Embed Code', type: 'code', placeholder: '<iframe src="..."></iframe>', language: 'html' }
                ]
            }
        ]
    },

    text: {
        icon: 'fa-align-left',
        label: 'Text',
        groups: [
            {
                id: 'content',
                title: 'Content',
                expanded: true,
                singleColumn: true,
                fields: [
                    { key: 'title', label: 'Title', type: 'text', placeholder: 'Section Title' },
                    { key: 'content', label: 'Content', type: 'textarea', placeholder: 'Enter your text here...', rows: 6 }
                ]
            }
        ]
    },

    links: {
        icon: 'fa-link',
        label: 'Links',
        groups: [
            {
                id: 'content',
                title: 'Settings',
                expanded: true,
                fields: [
                    { key: 'title', label: 'Title', type: 'text', placeholder: 'Quick Links' },
                    {
                        key: 'list_style',
                        label: 'List Style',
                        type: 'select',
                        options: [
                            { value: 'vertical', label: 'Vertical' },
                            { value: 'horizontal', label: 'Horizontal' },
                            { value: 'inline', label: 'Inline' }
                        ],
                        default: 'vertical'
                    }
                ]
            },
            {
                id: 'links',
                title: 'Links',
                expanded: true,
                singleColumn: true,
                fields: [
                    {
                        key: 'links',
                        label: 'Link Items',
                        type: 'array',
                        itemSchema: {
                            text: { label: 'Text', type: 'text', placeholder: 'Link text' },
                            url: { label: 'URL', type: 'url', placeholder: '/page/' },
                            icon: { label: 'Icon', type: 'icon', placeholder: 'fas fa-link' },
                            target: {
                                label: 'Target',
                                type: 'select',
                                options: [
                                    { value: '_self', label: 'Same Window' },
                                    { value: '_blank', label: 'New Window' }
                                ],
                                default: '_self'
                            }
                        }
                    }
                ]
            }
        ]
    },

    payment: {
        icon: 'fa-credit-card',
        label: 'Payment Methods',
        groups: [
            {
                id: 'methods',
                title: 'Payment Methods',
                expanded: true,
                fields: [
                    { key: 'show_visa', label: 'Visa', type: 'toggle', default: true },
                    { key: 'show_mastercard', label: 'Mastercard', type: 'toggle', default: true },
                    { key: 'show_amex', label: 'American Express', type: 'toggle', default: true },
                    { key: 'show_paypal', label: 'PayPal', type: 'toggle', default: true },
                    { key: 'show_apple_pay', label: 'Apple Pay', type: 'toggle', default: false },
                    { key: 'show_google_pay', label: 'Google Pay', type: 'toggle', default: false }
                ]
            }
        ]
    },

    trust_badges: {
        icon: 'fa-shield-alt',
        label: 'Trust Badges',
        groups: [
            {
                id: 'badges',
                title: 'Trust Badges',
                expanded: true,
                fields: [
                    { key: 'show_secure', label: 'Secure Checkout', type: 'toggle', default: true },
                    { key: 'show_guarantee', label: 'Money Back Guarantee', type: 'toggle', default: true },
                    { key: 'show_shipping', label: 'Free Shipping', type: 'toggle', default: true },
                    { key: 'show_support', label: '24/7 Support', type: 'toggle', default: false }
                ]
            }
        ]
    },

    loyalty_balance: {
        icon: 'fa-coins',
        label: 'Loyalty Balance',
        groups: [
            {
                id: 'display',
                title: 'Display Options',
                expanded: true,
                fields: [
                    {
                        key: 'display_style',
                        label: 'Display Style',
                        type: 'select',
                        options: [
                            { value: 'compact', label: 'Compact' },
                            { value: 'detailed', label: 'Detailed' },
                            { value: 'minimal', label: 'Minimal' }
                        ],
                        default: 'compact'
                    },
                    {
                        key: 'button_style',
                        label: 'Button Style',
                        type: 'select',
                        options: [
                            { value: 'outline', label: 'Outline' },
                            { value: 'solid', label: 'Solid' },
                            { value: 'ghost', label: 'Ghost' }
                        ],
                        default: 'outline'
                    },
                    {
                        key: 'icon_style',
                        label: 'Icon Style',
                        type: 'select',
                        options: [
                            { value: 'gift', label: 'Gift' },
                            { value: 'trophy', label: 'Trophy' },
                            { value: 'crown', label: 'Crown' },
                            { value: 'star', label: 'Star' }
                        ],
                        default: 'gift'
                    },
                    { key: 'link_to_dashboard', label: 'Link to Dashboard', type: 'toggle', default: true }
                ]
            }
        ]
    },

    loyalty_tier_badge: {
        icon: 'fa-medal',
        label: 'Loyalty Tier Badge',
        groups: [
            {
                id: 'display',
                title: 'Display Options',
                expanded: true,
                fields: [
                    {
                        key: 'display_style',
                        label: 'Display Style',
                        type: 'select',
                        options: [
                            { value: 'badge', label: 'Badge' },
                            { value: 'name_only', label: 'Name Only' },
                            { value: 'icon_only', label: 'Icon Only' },
                            { value: 'full', label: 'Full (Icon + Name)' }
                        ],
                        default: 'badge'
                    },
                    {
                        key: 'badge_style',
                        label: 'Badge Style',
                        type: 'select',
                        options: [
                            { value: 'solid', label: 'Solid' },
                            { value: 'outline', label: 'Outline' },
                            { value: 'ghost', label: 'Ghost' }
                        ],
                        default: 'solid'
                    },
                    { key: 'link_to_tiers', label: 'Link to Tiers Page', type: 'toggle', default: true },
                    { key: 'show_progress', label: 'Show Progress', type: 'toggle', default: false }
                ]
            }
        ]
    },

    custom: {
        icon: 'fa-code',
        label: 'Custom Widget',
        groups: [
            {
                id: 'content',
                title: 'Custom Content',
                expanded: true,
                singleColumn: true,
                fields: [
                    { key: 'id', label: 'Widget ID', type: 'text', placeholder: 'custom-widget-1', help: 'Unique identifier for CSS/JS targeting' },
                    { key: 'content', label: 'HTML Content', type: 'code', language: 'html', placeholder: '<div>Your custom HTML...</div>' }
                ]
            },
            {
                id: 'scripts',
                title: 'Scripts',
                expanded: false,
                singleColumn: true,
                fields: [
                    { key: 'javascript', label: 'JavaScript', type: 'code', language: 'javascript', placeholder: '// Custom JavaScript code' }
                ]
            }
        ]
    }
};

/**
 * Common FontAwesome icons for the icon picker
 */
const COMMON_ICONS = {
    'General': [
        'fa-home', 'fa-user', 'fa-cog', 'fa-search', 'fa-bell', 'fa-heart',
        'fa-star', 'fa-check', 'fa-times', 'fa-plus', 'fa-minus', 'fa-edit',
        'fa-trash', 'fa-save', 'fa-download', 'fa-upload', 'fa-share', 'fa-link'
    ],
    'E-commerce': [
        'fa-shopping-cart', 'fa-shopping-bag', 'fa-store', 'fa-tag', 'fa-tags',
        'fa-receipt', 'fa-gift', 'fa-truck', 'fa-shipping-fast', 'fa-box',
        'fa-credit-card', 'fa-wallet', 'fa-dollar-sign', 'fa-percent'
    ],
    'Communication': [
        'fa-envelope', 'fa-phone', 'fa-comment', 'fa-comments', 'fa-paper-plane',
        'fa-inbox', 'fa-reply', 'fa-share-alt', 'fa-bullhorn', 'fa-megaphone'
    ],
    'Social': [
        'fa-facebook', 'fa-twitter', 'fa-instagram', 'fa-linkedin', 'fa-youtube',
        'fa-pinterest', 'fa-tiktok', 'fa-whatsapp', 'fa-telegram', 'fa-discord'
    ],
    'Navigation': [
        'fa-bars', 'fa-chevron-down', 'fa-chevron-up', 'fa-chevron-left', 'fa-chevron-right',
        'fa-arrow-left', 'fa-arrow-right', 'fa-arrow-up', 'fa-arrow-down', 'fa-external-link-alt'
    ],
    'Status': [
        'fa-info-circle', 'fa-exclamation-circle', 'fa-question-circle', 'fa-check-circle',
        'fa-times-circle', 'fa-shield-alt', 'fa-lock', 'fa-unlock', 'fa-eye', 'fa-eye-slash'
    ]
};

/**
 * Widget Property Renderer
 * Generates GUI controls for widget configuration based on schemas
 */
class WidgetPropertyRenderer {
    constructor(builder) {
        this.builder = builder;
        this.currentWidget = null;
        this.dynamicOptions = {};
    }

    /**
     * Main render method - generates full properties panel HTML
     */
    render(widgetData) {
        this.currentWidget = widgetData;
        // Load schema from builder's dynamically loaded schemas (API)
        // Falls back to WIDGET_SCHEMAS constant if API loading failed
        const schema = this.builder.widgetSchemas?.[widgetData.widget_type]
            || WIDGET_SCHEMAS?.[widgetData.widget_type];

        if (!schema) {
            // Fallback to JSON editor for unknown widget types
            return this.renderFallbackEditor(widgetData);
        }

        const config = widgetData.config || {};

        let html = `
            <div class="hfb-widget-header">
                <div class="hfb-widget-icon">
                    <i class="fas ${schema.icon}"></i>
                </div>
                <div class="hfb-widget-details">
                    <h3 class="hfb-widget-title">${this.escapeHtml(widgetData.widget_name)}</h3>
                    <span class="hfb-widget-type">${schema.label}</span>
                </div>
            </div>
        `;

        // Render each property group
        for (const group of schema.groups) {
            html += this.renderPropertyGroup(group, config);
        }

        // Add Device Visibility group
        html += this.renderDeviceVisibilityGroup(widgetData);

        // Add Advanced JSON editor as collapsed section
        html += this.renderAdvancedSection(config);

        // Add action buttons
        html += this.renderActionButtons();

        return html;
    }

    /**
     * Render a collapsible property group
     */
    renderPropertyGroup(group, config) {
        const collapsedClass = group.expanded ? '' : 'collapsed';
        const columnClass = group.singleColumn ? 'single-column' : '';

        let fieldsHtml = '';
        for (const field of group.fields) {
            fieldsHtml += this.renderField(field, config);
        }

        return `
            <div class="bb-property-group ${collapsedClass}" id="group-${group.id}">
                <div class="bb-property-group-header">
                    <i class="fas fa-chevron-down toggle-icon"></i>
                    <h4 class="bb-property-group-title">${group.title}</h4>
                </div>
                <div class="bb-property-group-content ${columnClass}">
                    ${fieldsHtml}
                </div>
            </div>
        `;
    }

    /**
     * Check if a field should be visible based on showWhen condition
     */
    shouldShowField(field, config) {
        if (!field.showWhen) return true;

        for (const [key, expectedValue] of Object.entries(field.showWhen)) {
            const actualValue = config[key] !== undefined ? config[key] : true; // Default true for toggles
            if (actualValue !== expectedValue) {
                return false;
            }
        }
        return true;
    }

    /**
     * Render a single field based on its type
     */
    renderField(field, config) {
        // Check showWhen condition
        const isVisible = this.shouldShowField(field, config);
        const hiddenClass = isVisible ? '' : 'hidden';

        const value = config[field.key] !== undefined ? config[field.key] : (field.default || '');
        const status = this.getPropertyStatus(config, field.key, field.default);
        const fullWidthClass = field.fullWidth ? 'full-width' : '';

        let inputHtml = '';
        switch (field.type) {
            case 'text':
                inputHtml = this.renderTextField(field, value);
                break;
            case 'url':
                inputHtml = this.renderUrlField(field, value);
                break;
            case 'textarea':
                inputHtml = this.renderTextareaField(field, value);
                break;
            case 'code':
                inputHtml = this.renderCodeField(field, value);
                break;
            case 'select':
                inputHtml = this.renderSelectField(field, value);
                break;
            case 'toggle':
                inputHtml = this.renderToggleField(field, value);
                break;
            case 'number':
                inputHtml = this.renderNumberField(field, value);
                break;
            case 'icon':
                inputHtml = this.renderIconField(field, value);
                break;
            case 'media':
                inputHtml = this.renderMediaField(field, value);
                break;
            case 'array':
                inputHtml = this.renderArrayField(field, value);
                break;
            case 'color':
                inputHtml = this.renderColorField(field, value);
                break;
            case 'typography':
                inputHtml = this.renderTypographyField(field, value);
                break;
            default:
                inputHtml = this.renderTextField(field, value);
        }

        // Toggle fields have different layout
        if (field.type === 'toggle') {
            return `
                <div class="bb-property-field status-${status} ${fullWidthClass} ${hiddenClass}" data-property="${field.key}" data-show-when='${field.showWhen ? JSON.stringify(field.showWhen) : ''}'>
                    ${inputHtml}
                </div>
            `;
        }

        return `
            <div class="bb-property-field status-${status} ${fullWidthClass} ${hiddenClass}" data-property="${field.key}" data-show-when='${field.showWhen ? JSON.stringify(field.showWhen) : ''}'>
                <label class="bb-property-label">${field.label}</label>
                ${inputHtml}
                ${field.help ? `<span class="bb-property-help">${field.help}</span>` : ''}
            </div>
        `;
    }

    /**
     * Text input field
     */
    renderTextField(field, value) {
        return `
            <div class="bb-property-input-wrapper">
                <input type="text"
                    class="hfb-input"
                    id="prop-${field.key}"
                    data-property="${field.key}"
                    value="${this.escapeHtml(value)}"
                    placeholder="${field.placeholder || ''}">
                ${this.renderResetButton(field.key)}
            </div>
        `;
    }

    /**
     * URL input field
     */
    renderUrlField(field, value) {
        return `
            <div class="bb-property-input-wrapper">
                <div class="hfb-url-input-wrapper" style="flex: 1;">
                    <input type="text"
                        class="hfb-input"
                        id="prop-${field.key}"
                        data-property="${field.key}"
                        value="${this.escapeHtml(value)}"
                        placeholder="${field.placeholder || ''}">
                </div>
                ${this.renderResetButton(field.key)}
            </div>
        `;
    }

    /**
     * Textarea field
     */
    renderTextareaField(field, value) {
        const rows = field.rows || 3;
        return `
            <div class="bb-property-input-wrapper" style="flex-direction: column; align-items: stretch;">
                <textarea
                    class="hfb-input"
                    id="prop-${field.key}"
                    data-property="${field.key}"
                    rows="${rows}"
                    placeholder="${field.placeholder || ''}"
                    style="resize: vertical; min-height: ${rows * 24}px;">${this.escapeHtml(value)}</textarea>
                <div style="display: flex; justify-content: flex-end; margin-top: 4px;">
                    ${this.renderResetButton(field.key)}
                </div>
            </div>
        `;
    }

    /**
     * Code textarea field
     */
    renderCodeField(field, value) {
        return `
            <div class="bb-property-input-wrapper" style="flex-direction: column; align-items: stretch;">
                <textarea
                    class="hfb-code-textarea"
                    id="prop-${field.key}"
                    data-property="${field.key}"
                    placeholder="${field.placeholder || ''}">${this.escapeHtml(value)}</textarea>
                <div style="display: flex; justify-content: flex-end; margin-top: 4px;">
                    ${this.renderResetButton(field.key)}
                </div>
            </div>
        `;
    }

    /**
     * Select dropdown field
     */
    renderSelectField(field, value) {
        let optionsHtml = '';

        if (field.dynamicOptions) {
            // Load options dynamically
            const options = this.dynamicOptions[field.dynamicOptions] || [];
            optionsHtml = `<option value="">-- ${field.placeholder || 'Select'} --</option>`;
            for (const opt of options) {
                const selected = opt.value == value ? 'selected' : '';
                optionsHtml += `<option value="${opt.value}" ${selected}>${this.escapeHtml(opt.label)}</option>`;
            }
        } else if (field.options) {
            for (const opt of field.options) {
                const selected = opt.value === value ? 'selected' : '';
                optionsHtml += `<option value="${opt.value}" ${selected}>${opt.label}</option>`;
            }
        }

        return `
            <div class="bb-property-input-wrapper">
                <select class="hfb-select" id="prop-${field.key}" data-property="${field.key}">
                    ${optionsHtml}
                </select>
                ${this.renderResetButton(field.key)}
            </div>
        `;
    }

    /**
     * Toggle switch field
     */
    renderToggleField(field, value) {
        const checked = value === true || value === 'true' || value === 1 ? 'checked' : '';
        return `
            <div class="hfb-toggle-field">
                <span class="hfb-toggle-label">${field.label}</span>
                <label class="hfb-toggle-switch">
                    <input type="checkbox" id="prop-${field.key}" data-property="${field.key}" ${checked}>
                    <span class="hfb-toggle-slider"></span>
                </label>
            </div>
        `;
    }

    /**
     * Number input field
     */
    renderNumberField(field, value) {
        const min = field.min !== undefined ? field.min : '';
        const max = field.max !== undefined ? field.max : '';
        return `
            <div class="bb-property-input-wrapper">
                <div class="hfb-number-input-wrapper" style="flex: 1;">
                    <input type="number"
                        class="hfb-input"
                        id="prop-${field.key}"
                        data-property="${field.key}"
                        value="${value}"
                        min="${min}"
                        max="${max}"
                        placeholder="${field.placeholder || ''}">
                    <div class="hfb-number-stepper">
                        <button type="button" class="stepper-up" data-target="prop-${field.key}"><i class="fas fa-chevron-up"></i></button>
                        <button type="button" class="stepper-down" data-target="prop-${field.key}"><i class="fas fa-chevron-down"></i></button>
                    </div>
                </div>
                ${this.renderResetButton(field.key)}
            </div>
        `;
    }

    /**
     * Icon picker field
     */
    renderIconField(field, value) {
        const iconClass = value || '';
        return `
            <div class="hfb-icon-picker-wrapper">
                <div class="hfb-icon-picker-preview" id="icon-preview-${field.key}">
                    ${iconClass ? `<i class="fas ${iconClass}"></i>` : ''}
                </div>
                <input type="hidden" id="prop-${field.key}" data-property="${field.key}" value="${this.escapeHtml(iconClass)}">
                <button type="button" class="hfb-icon-picker-btn" data-target="${field.key}">
                    <i class="fas fa-icons"></i> Choose Icon
                </button>
                ${this.renderResetButton(field.key)}
            </div>
        `;
    }

    /**
     * Media picker field
     */
    renderMediaField(field, value) {
        // Check if this is logo widget with use_site_logo enabled
        const isLogoWidget = this.currentWidget?.widget_type === 'logo';
        const useSiteLogo = this.currentWidget?.config?.use_site_logo !== false;
        const siteLogoData = this.builder.siteLogoData;

        // For logo widget with use_site_logo enabled, show site logo info
        if (isLogoWidget && field.key === 'logo_url' && useSiteLogo && siteLogoData?.has_logo) {
            return `
                <div class="hfb-media-picker-wrapper hfb-site-logo-info">
                    <div class="hfb-media-preview" id="media-preview-${field.key}">
                        <img src="${this.escapeHtml(siteLogoData.logo_url)}" alt="Site Logo">
                    </div>
                    <input type="hidden" id="prop-${field.key}" data-property="${field.key}" value="">
                    <div class="hfb-site-logo-notice">
                        <i class="fas fa-info-circle"></i>
                        <span>Using logo from Site Settings</span>
                    </div>
                </div>
            `;
        }

        const hasImage = value && value.length > 0;
        const isLogoField = isLogoWidget && field.key === 'logo_url';

        return `
            <div class="hfb-media-picker-wrapper" data-is-logo="${isLogoField}">
                <div class="hfb-media-preview" id="media-preview-${field.key}">
                    ${hasImage
                        ? `<img src="${this.escapeHtml(value)}" alt="Preview">`
                        : `<div class="hfb-media-preview-empty">
                            <i class="fas fa-image"></i>
                            <span>No image selected</span>
                           </div>`
                    }
                </div>
                <input type="hidden" id="prop-${field.key}" data-property="${field.key}" value="${this.escapeHtml(value)}">
                <div class="hfb-media-actions">
                    <button type="button" class="hfb-media-btn select" data-target="${field.key}">
                        <i class="fas fa-folder-open"></i> Select
                    </button>
                    ${hasImage ? `
                        <button type="button" class="hfb-media-btn remove" data-target="${field.key}">
                            <i class="fas fa-times"></i>
                        </button>
                    ` : ''}
                </div>
            </div>
        `;
    }

    /**
     * Array field (for links widget)
     */
    renderArrayField(field, value) {
        const items = Array.isArray(value) ? value : [];

        let itemsHtml = '';
        items.forEach((item, index) => {
            itemsHtml += this.renderArrayItem(field, item, index);
        });

        if (items.length === 0) {
            itemsHtml = `<div class="hfb-array-empty">No items added yet</div>`;
        }

        return `
            <div class="hfb-array-editor" id="array-${field.key}" data-property="${field.key}">
                <div class="hfb-array-items">
                    ${itemsHtml}
                </div>
                <button type="button" class="hfb-array-add-btn" data-target="${field.key}">
                    <i class="fas fa-plus"></i> Add Item
                </button>
            </div>
        `;
    }

    /**
     * Render a single array item
     */
    renderArrayItem(field, item, index) {
        let fieldsHtml = '';
        for (const [key, schema] of Object.entries(field.itemSchema)) {
            const value = item[key] || '';
            fieldsHtml += `
                <div class="bb-property-field ${schema.fullWidth ? 'full-width' : ''}">
                    <label class="bb-property-label">${schema.label}</label>
                    ${this.renderArrayItemField(field.key, index, key, schema, value)}
                </div>
            `;
        }

        return `
            <div class="hfb-array-item" data-index="${index}">
                <div class="hfb-array-item-header">
                    <span class="hfb-array-item-drag"><i class="fas fa-grip-vertical"></i></span>
                    <span class="hfb-array-item-number">Item ${index + 1}</span>
                    <div class="hfb-array-item-actions">
                        <button type="button" class="hfb-array-item-btn move-up" title="Move up"><i class="fas fa-chevron-up"></i></button>
                        <button type="button" class="hfb-array-item-btn move-down" title="Move down"><i class="fas fa-chevron-down"></i></button>
                        <button type="button" class="hfb-array-item-btn delete" title="Delete"><i class="fas fa-trash"></i></button>
                    </div>
                </div>
                <div class="hfb-array-item-fields">
                    ${fieldsHtml}
                </div>
            </div>
        `;
    }

    /**
     * Render field within an array item
     */
    renderArrayItemField(arrayKey, index, fieldKey, schema, value) {
        const inputId = `prop-${arrayKey}-${index}-${fieldKey}`;

        switch (schema.type) {
            case 'select':
                let optionsHtml = '';
                for (const opt of (schema.options || [])) {
                    const selected = opt.value === value ? 'selected' : '';
                    optionsHtml += `<option value="${opt.value}" ${selected}>${opt.label}</option>`;
                }
                return `<select class="hfb-select" id="${inputId}" data-array="${arrayKey}" data-index="${index}" data-field="${fieldKey}">${optionsHtml}</select>`;

            case 'icon':
                return `
                    <div class="hfb-icon-picker-wrapper" style="flex: 1;">
                        <div class="hfb-icon-picker-preview" id="icon-preview-${inputId}" style="width: 32px; height: 32px;">
                            ${value ? `<i class="fas ${value}"></i>` : ''}
                        </div>
                        <input type="hidden" id="${inputId}" data-array="${arrayKey}" data-index="${index}" data-field="${fieldKey}" value="${this.escapeHtml(value)}">
                        <button type="button" class="hfb-icon-picker-btn" data-target="${inputId}" style="flex: 1;">
                            <i class="fas fa-icons"></i>
                        </button>
                    </div>
                `;

            case 'url':
                return `
                    <div class="hfb-url-input-wrapper" style="flex: 1;">
                        <input type="text" class="hfb-input" id="${inputId}" data-array="${arrayKey}" data-index="${index}" data-field="${fieldKey}" value="${this.escapeHtml(value)}" placeholder="${schema.placeholder || ''}">
                    </div>
                `;

            default:
                return `<input type="text" class="hfb-input" id="${inputId}" data-array="${arrayKey}" data-index="${index}" data-field="${fieldKey}" value="${this.escapeHtml(value)}" placeholder="${schema.placeholder || ''}">`;
        }
    }

    /**
     * Color picker field with utility
     */
    renderColorField(field, value) {
        return `
            <div class="bb-property-input-wrapper">
                <div class="hfb-color-input-wrapper" style="display: flex; align-items: center; gap: 8px; flex: 1;">
                    <input type="text"
                        class="hfb-input hfb-color-input"
                        id="prop-${field.key}"
                        data-property="${field.key}"
                        data-field-type="color"
                        value="${this.escapeHtml(value || '')}"
                        placeholder="${field.placeholder || 'e.g., #000000 or var(--token)'}"
                        style="flex: 1;">
                    <div class="hfb-color-preview"
                         style="width: 32px; height: 32px; border-radius: 4px; border: 1px solid var(--border-color); background: ${value || 'transparent'}; cursor: pointer; flex-shrink: 0;"
                         data-color-trigger="${field.key}"
                         title="Click to open color picker"></div>
                </div>
                ${this.renderResetButton(field.key)}
            </div>
        `;
    }

    /**
     * Typography field with utility editor
     */
    renderTypographyField(field, value) {
        // Parse the value to show a summary - handles both JSON and CSS string formats
        let summary = 'Default';
        if (value) {
            summary = this.parseTypographySummary(value);
        }

        const safeValue = typeof value === 'object' ? JSON.stringify(value) : (value || '');

        return `
            <div class="bb-property-input-wrapper">
                <input type="hidden"
                    id="prop-${field.key}"
                    data-property="${field.key}"
                    data-field-type="typography"
                    value="${this.escapeHtml(safeValue)}">
                <button type="button"
                        class="hfb-typography-trigger hfb-input"
                        data-typography-trigger="${field.key}"
                        style="display: flex; align-items: center; justify-content: space-between; cursor: pointer; width: 100%;">
                    <span class="typography-summary">${summary}</span>
                    <i class="fas fa-font" style="opacity: 0.6;"></i>
                </button>
                ${this.renderResetButton(field.key)}
            </div>
        `;
    }

    /**
     * Parse typography value (JSON or CSS string) and return summary text
     */
    parseTypographySummary(value) {
        if (!value) return 'Default';

        // If it's already an object, use it directly
        if (typeof value === 'object') {
            return this.buildTypographySummaryFromObject(value);
        }

        // Try to parse as JSON first
        try {
            const typo = JSON.parse(value);
            if (typo && typeof typo === 'object') {
                return this.buildTypographySummaryFromObject(typo);
            }
        } catch (e) {
            // Not JSON, check if it's a CSS string
            if (value.includes(':') && value.includes(';')) {
                return this.buildTypographySummaryFromCSS(value);
            }
        }

        return 'Default';
    }

    /**
     * Build summary from typography object
     */
    buildTypographySummaryFromObject(typo) {
        const parts = [];
        if (typo.fontFamily) {
            // Extract just the first font name for display
            const fontName = typo.fontFamily.split(',')[0].replace(/['"]/g, '').replace('var(--theme-typography-font-family-', '').replace(')', '');
            parts.push(fontName);
        }
        if (typo.fontSize) parts.push(typo.fontSize);
        if (typo.fontWeight && typo.fontWeight !== '400') parts.push(typo.fontWeight);
        return parts.join(', ') || 'Default';
    }

    /**
     * Build summary from CSS string (legacy format)
     */
    buildTypographySummaryFromCSS(cssString) {
        const parts = [];

        // Parse font-family
        const fontMatch = cssString.match(/font-family:\s*([^;]+)/);
        if (fontMatch) {
            const fontName = fontMatch[1].split(',')[0].replace(/['"]/g, '').trim();
            parts.push(fontName);
        }

        // Parse font-size
        const sizeMatch = cssString.match(/font-size:\s*([^;]+)/);
        if (sizeMatch) {
            parts.push(sizeMatch[1].trim());
        }

        // Parse font-weight
        const weightMatch = cssString.match(/font-weight:\s*([^;]+)/);
        if (weightMatch && weightMatch[1].trim() !== '400') {
            parts.push(weightMatch[1].trim());
        }

        return parts.join(', ') || 'Default';
    }

    /**
     * Render reset button
     */
    renderResetButton(key) {
        return `
            <button type="button" class="bb-property-reset" data-reset="${key}" title="Reset to default">
                <i class="fas fa-undo"></i>
            </button>
        `;
    }

    /**
     * Render the Advanced JSON editor section
     */
    renderDeviceVisibilityGroup(widgetData) {
        const showMobile = widgetData.show_on_mobile !== false;
        const showTablet = widgetData.show_on_tablet !== false;
        const showDesktop = widgetData.show_on_desktop !== false;

        return `
            <div class="bb-property-group collapsed" id="group-device-visibility">
                <div class="bb-property-group-header">
                    <i class="fas fa-chevron-down toggle-icon"></i>
                    <h4 class="bb-property-group-title">Device Visibility</h4>
                </div>
                <div class="bb-property-group-content single-column">
                    <div class="bb-property-field full-width">
                        <p style="font-size: 0.8rem; color: var(--admin-text-muted, #888); margin: 0 0 0.75rem;">
                            Control which devices display this widget
                        </p>
                        <div style="display: flex; flex-direction: column; gap: 0.5rem;">
                            <label style="display: flex; align-items: center; gap: 0.5rem; cursor: pointer;">
                                <input type="checkbox" id="vis-desktop" ${showDesktop ? 'checked' : ''} class="device-vis-checkbox">
                                <i class="fas fa-desktop" style="width: 20px; text-align: center;"></i>
                                <span>Desktop</span>
                            </label>
                            <label style="display: flex; align-items: center; gap: 0.5rem; cursor: pointer;">
                                <input type="checkbox" id="vis-tablet" ${showTablet ? 'checked' : ''} class="device-vis-checkbox">
                                <i class="fas fa-tablet-alt" style="width: 20px; text-align: center;"></i>
                                <span>Tablet</span>
                            </label>
                            <label style="display: flex; align-items: center; gap: 0.5rem; cursor: pointer;">
                                <input type="checkbox" id="vis-mobile" ${showMobile ? 'checked' : ''} class="device-vis-checkbox">
                                <i class="fas fa-mobile-alt" style="width: 20px; text-align: center;"></i>
                                <span>Mobile</span>
                            </label>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    renderAdvancedSection(config) {
        return `
            <div class="bb-property-group collapsed" id="group-advanced">
                <div class="bb-property-group-header">
                    <i class="fas fa-chevron-down toggle-icon"></i>
                    <h4 class="bb-property-group-title">Advanced (JSON)</h4>
                    <span class="bb-property-group-help">Power users</span>
                </div>
                <div class="bb-property-group-content single-column">
                    <div class="bb-property-field full-width">
                        <label class="bb-property-label">Raw Configuration</label>
                        <textarea id="widget-config-json" class="hfb-code-textarea" rows="8">${JSON.stringify(config, null, 2)}</textarea>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Render action buttons
     */
    renderActionButtons() {
        const translations = this.builder.config.translations || {};
        return `
            <div class="hfb-property-actions">
                <button id="save-widget-config" class="btn btn-primary">
                    <i class="fas fa-save"></i> ${translations.save || 'Save'}
                </button>
                <button id="cancel-widget-config" class="btn btn-secondary">
                    <i class="fas fa-times"></i> ${translations.cancel || 'Cancel'}
                </button>
            </div>
        `;
    }

    /**
     * Fallback editor for unknown widget types
     */
    renderFallbackEditor(widgetData) {
        const config = widgetData.config || {};
        return `
            <div class="hfb-widget-header">
                <div class="hfb-widget-icon">
                    <i class="fas fa-puzzle-piece"></i>
                </div>
                <div class="hfb-widget-details">
                    <h3 class="hfb-widget-title">${this.escapeHtml(widgetData.widget_name)}</h3>
                    <span class="hfb-widget-type">${widgetData.widget_type}</span>
                </div>
            </div>
            <div class="bb-property-group" id="group-config">
                <div class="bb-property-group-header">
                    <i class="fas fa-chevron-down toggle-icon"></i>
                    <h4 class="bb-property-group-title">Configuration</h4>
                </div>
                <div class="bb-property-group-content single-column">
                    <div class="bb-property-field full-width">
                        <label class="bb-property-label">Custom Configuration (JSON)</label>
                        <textarea id="widget-config-json" class="hfb-code-textarea" rows="10">${JSON.stringify(config, null, 2)}</textarea>
                    </div>
                </div>
            </div>
            ${this.renderActionButtons()}
        `;
    }

    /**
     * Get property status (custom, default, or none)
     */
    getPropertyStatus(config, key, defaultValue) {
        const value = config[key];
        if (value !== undefined && value !== null && value !== '') {
            if (value === defaultValue) {
                return 'default';
            }
            return 'custom';
        }
        return 'none';
    }

    /**
     * Collect all values from form controls
     */
    collectFormValues() {
        const config = {};
        const widgetType = this.currentWidget?.widget_type;
        const schema = this.builder.widgetSchemas?.[widgetType] || WIDGET_SCHEMAS?.[widgetType];

        if (!schema) {
            // For unknown types, just parse the JSON
            const jsonTextarea = document.getElementById('widget-config-json');
            if (jsonTextarea) {
                try {
                    return JSON.parse(jsonTextarea.value);
                } catch (e) {
                    console.error('Invalid JSON:', e);
                    return null;
                }
            }
            return {};
        }

        // Collect values from each field
        for (const group of schema.groups) {
            for (const field of group.fields) {
                const element = document.getElementById(`prop-${field.key}`);
                if (!element) continue;

                switch (field.type) {
                    case 'toggle':
                        config[field.key] = element.checked;
                        break;
                    case 'number':
                        config[field.key] = element.value ? parseInt(element.value, 10) : null;
                        break;
                    case 'array':
                        config[field.key] = this.collectArrayValues(field);
                        break;
                    default:
                        config[field.key] = element.value;
                }
            }
        }

        return config;
    }

    /**
     * Collect values from an array field
     */
    collectArrayValues(field) {
        const items = [];
        const container = document.getElementById(`array-${field.key}`);
        if (!container) return items;

        const itemElements = container.querySelectorAll('.hfb-array-item');
        itemElements.forEach((itemEl, index) => {
            const item = {};
            for (const [key, schema] of Object.entries(field.itemSchema)) {
                const input = document.getElementById(`prop-${field.key}-${index}-${key}`);
                if (input) {
                    item[key] = input.value;
                }
            }
            items.push(item);
        });

        return items;
    }

    /**
     * Setup event listeners for all form controls
     */
    setupEventListeners() {
        // Property group toggle
        document.querySelectorAll('.bb-property-group-header').forEach(header => {
            header.addEventListener('click', () => {
                header.closest('.bb-property-group').classList.toggle('collapsed');
            });
        });

        // Number stepper buttons
        document.querySelectorAll('.stepper-up, .stepper-down').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = btn.dataset.target;
                const input = document.getElementById(targetId);
                if (input) {
                    const step = parseInt(input.step) || 1;
                    const min = parseInt(input.min) || -Infinity;
                    const max = parseInt(input.max) || Infinity;
                    let value = parseInt(input.value) || 0;

                    if (btn.classList.contains('stepper-up')) {
                        value = Math.min(max, value + step);
                    } else {
                        value = Math.max(min, value - step);
                    }

                    input.value = value;
                    input.dispatchEvent(new Event('change', { bubbles: true }));
                }
            });
        });

        // Icon picker buttons
        document.querySelectorAll('.hfb-icon-picker-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                this.openIconPicker(btn.dataset.target);
            });
        });

        // Media picker buttons
        document.querySelectorAll('.hfb-media-btn.select').forEach(btn => {
            btn.addEventListener('click', () => {
                this.openMediaPicker(btn.dataset.target);
            });
        });

        document.querySelectorAll('.hfb-media-btn.remove').forEach(btn => {
            btn.addEventListener('click', () => {
                this.removeMedia(btn.dataset.target);
            });
        });

        // Array add buttons
        document.querySelectorAll('.hfb-array-add-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                this.addArrayItem(btn.dataset.target);
            });
        });

        // Array item actions
        document.querySelectorAll('.hfb-array-item-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const item = btn.closest('.hfb-array-item');
                const container = btn.closest('.hfb-array-editor');
                const propertyKey = container?.dataset.property;

                if (btn.classList.contains('delete')) {
                    item.remove();
                    this.reindexArrayItems(propertyKey);
                } else if (btn.classList.contains('move-up')) {
                    const prev = item.previousElementSibling;
                    if (prev && prev.classList.contains('hfb-array-item')) {
                        item.parentNode.insertBefore(item, prev);
                        this.reindexArrayItems(propertyKey);
                    }
                } else if (btn.classList.contains('move-down')) {
                    const next = item.nextElementSibling;
                    if (next && next.classList.contains('hfb-array-item')) {
                        item.parentNode.insertBefore(next, item);
                        this.reindexArrayItems(propertyKey);
                    }
                }
            });
        });

        // Reset buttons
        document.querySelectorAll('.bb-property-reset').forEach(btn => {
            btn.addEventListener('click', () => {
                this.resetProperty(btn.dataset.reset);
            });
        });

        // Live preview updates on input change (debounced)
        let debounceTimer;
        document.querySelectorAll('[data-property]').forEach(input => {
            const eventType = input.type === 'checkbox' ? 'change' : 'input';
            input.addEventListener(eventType, () => {
                // Update showWhen visibility for toggle fields
                if (input.type === 'checkbox') {
                    this.updateShowWhenVisibility(input.dataset.property, input.checked);
                }

                clearTimeout(debounceTimer);
                debounceTimer = setTimeout(() => {
                    this.updateLivePreview();
                }, 300);
            });
        });

        // Initialize utility editors for color and typography fields
        this.initializeUtilities();
    }

    /**
     * Initialize utility editors for color and typography fields
     */
    initializeUtilities() {
        const self = this;

        // Color picker utilities
        document.querySelectorAll('[data-color-trigger]').forEach(trigger => {
            const key = trigger.dataset.colorTrigger;
            const input = document.querySelector(`#prop-${key}`);
            if (!input) return;

            // Initialize ColorPickerUtility if available
            if (window.ColorPickerUtility) {
                const picker = new ColorPickerUtility({
                    propertyKey: key,
                    showOpacity: true,
                    onChange: (color) => {
                        input.value = color;
                        trigger.style.background = color || 'transparent';
                        self.updateLivePreview();
                    }
                });

                // Use our custom trigger instead of letting attach create one
                trigger.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    picker.open(input, input.value);
                });
            } else {
                // Fallback: simple click to edit
                trigger.addEventListener('click', async () => {
                    const color = await AdminModal.prompt({message: 'Enter color (hex, rgb, or CSS variable):', defaultValue: input.value});
                    if (color !== null) {
                        input.value = color;
                        trigger.style.background = color || 'transparent';
                        self.updateLivePreview();
                    }
                });
            }

            // Also update preview when typing in input
            input.addEventListener('input', () => {
                trigger.style.background = input.value || 'transparent';
            });
        });

        // Typography utilities
        document.querySelectorAll('[data-typography-trigger]').forEach(trigger => {
            const key = trigger.dataset.typographyTrigger;
            const input = document.querySelector(`#prop-${key}`);
            if (!input) return;

            // Initialize TypographyEditor if available
            if (window.TypographyEditor) {
                const editor = new TypographyEditor({
                    propertyKey: key,
                    standalone: true,  // Don't create automatic trigger button
                    onChange: (cssString, settings) => {
                        // TypographyEditor passes (css, settings) - we need the settings object as JSON
                        // Note: This is called during live preview, but applySettings() will override
                        const jsonValue = JSON.stringify(settings);
                        input.value = jsonValue;
                        self.updateTypographySummary(trigger, settings);
                        self.updateLivePreview();
                    },
                    onApply: (cssString, settings) => {
                        // onApply is called AFTER applySettings() sets input.value to CSS
                        // So we need to override it here with our JSON format
                        const jsonValue = JSON.stringify(settings);
                        input.value = jsonValue;
                        self.updateTypographySummary(trigger, settings);
                        self.updateLivePreview();
                    }
                });

                // Attach editor to find the input and parse initial value
                editor.attach(input, input.value);

                // Use our custom trigger button
                trigger.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    editor.toggle();
                });
            } else {
                // Fallback: alert user that typography editor is not loaded
                trigger.addEventListener('click', async () => {
                    console.warn('TypographyEditor utility not loaded');
                    // Try to show a simple editing modal or prompt
                    const currentValue = input.value || '{}';
                    const newValue = await AdminModal.prompt({message: 'Edit typography JSON:', defaultValue: currentValue});
                    if (newValue !== null) {
                        try {
                            JSON.parse(newValue); // Validate JSON
                            input.value = newValue;
                            self.updateTypographySummary(trigger, newValue);
                            self.updateLivePreview();
                        } catch (e) {
                            AdminModal.alert({message: 'Invalid JSON format', type: 'error'});
                        }
                    }
                });
            }
        });
    }

    /**
     * Handle property change for live preview
     */
    handlePropertyChange(key, value) {
        // Trigger debounced live preview update
        this.updateLivePreview();
    }

    /**
     * Update typography trigger summary text
     */
    updateTypographySummary(trigger, value) {
        const summary = trigger.querySelector('.typography-summary');
        if (!summary) return;

        summary.textContent = this.parseTypographySummary(value);
    }

    /**
     * Update visibility of fields based on showWhen conditions
     */
    updateShowWhenVisibility(changedProperty, newValue) {
        document.querySelectorAll('[data-show-when]').forEach(field => {
            const showWhenStr = field.dataset.showWhen;
            // Skip empty or whitespace-only strings
            if (!showWhenStr || !showWhenStr.trim()) return;

            try {
                const showWhen = JSON.parse(showWhenStr);
                if (showWhen[changedProperty] !== undefined) {
                    // This field depends on the changed property
                    const shouldShow = showWhen[changedProperty] === newValue;
                    field.classList.toggle('hidden', !shouldShow);

                    // For logo widget, re-render the panel to update site logo display
                    if (changedProperty === 'use_site_logo' && this.currentWidget?.widget_type === 'logo') {
                        // Update the widget config immediately
                        this.currentWidget.config = this.currentWidget.config || {};
                        this.currentWidget.config.use_site_logo = newValue;
                        // Re-render the property panel to show/hide site logo info
                        this.builder.showPropertyPanel(this.currentWidget);
                    }
                }
            } catch (e) {
                // Silently ignore empty or invalid JSON - this is expected for fields without showWhen
                if (showWhenStr.trim().length > 0) {
                    console.warn('Could not parse showWhen condition:', showWhenStr);
                }
            }
        });
    }

    /**
     * Open icon picker modal
     */
    openIconPicker(targetId) {
        // Create modal if it doesn't exist
        let modal = document.getElementById('hfb-icon-modal');
        if (!modal) {
            modal = this.createIconPickerModal();
            document.body.appendChild(modal);
        }

        modal.dataset.target = targetId;
        modal.classList.remove('hidden');

        // Focus search input
        const searchInput = modal.querySelector('.hfb-icon-modal-search input');
        if (searchInput) {
            searchInput.value = '';
            searchInput.focus();
        }
    }

    /**
     * Create icon picker modal
     */
    createIconPickerModal() {
        const modal = document.createElement('div');
        modal.id = 'hfb-icon-modal';
        modal.className = 'hfb-icon-modal hidden';

        let categoriesHtml = '';
        for (const [category, icons] of Object.entries(COMMON_ICONS)) {
            let iconsHtml = '';
            for (const icon of icons) {
                iconsHtml += `<button type="button" class="hfb-icon-item" data-icon="${icon}"><i class="fas ${icon}"></i></button>`;
            }
            categoriesHtml += `
                <div class="hfb-icon-category">
                    <div class="hfb-icon-category-title">${category}</div>
                    <div class="hfb-icon-grid">${iconsHtml}</div>
                </div>
            `;
        }

        modal.innerHTML = `
            <div class="hfb-icon-modal-content">
                <div class="hfb-icon-modal-header">
                    <h3>Choose an Icon</h3>
                    <button type="button" class="preset-close-btn" id="icon-modal-close">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="hfb-icon-modal-search">
                    <input type="text" placeholder="Search icons...">
                </div>
                <div class="hfb-icon-modal-body">
                    ${categoriesHtml}
                </div>
            </div>
        `;

        // Event listeners
        modal.querySelector('#icon-modal-close').addEventListener('click', () => {
            modal.classList.add('hidden');
        });

        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.classList.add('hidden');
            }
        });

        modal.querySelectorAll('.hfb-icon-item').forEach(item => {
            item.addEventListener('click', () => {
                const icon = item.dataset.icon;
                const targetId = modal.dataset.target;
                this.selectIcon(targetId, icon);
                modal.classList.add('hidden');
            });
        });

        // Search functionality
        const searchInput = modal.querySelector('.hfb-icon-modal-search input');
        searchInput.addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase();
            modal.querySelectorAll('.hfb-icon-item').forEach(item => {
                const iconName = item.dataset.icon.toLowerCase();
                item.style.display = iconName.includes(term) ? '' : 'none';
            });
        });

        return modal;
    }

    /**
     * Select an icon
     */
    selectIcon(targetId, icon) {
        const input = document.getElementById(targetId.startsWith('prop-') ? targetId : `prop-${targetId}`);
        const preview = document.getElementById(`icon-preview-${targetId}`) || document.getElementById(`icon-preview-prop-${targetId}`);

        if (input) {
            input.value = icon;
        }

        if (preview) {
            preview.innerHTML = `<i class="fas ${icon}"></i>`;
        }

        this.updateLivePreview();
    }

    /**
     * Open media picker (uses existing media library)
     */
    async openMediaPicker(targetId) {
        const isLogoWidget = this.currentWidget?.widget_type === 'logo';
        const isLogoField = targetId === 'logo_url';

        // Check if media library is available
        if (window.selectImageFromLibrary) {
            window.selectImageFromLibrary(async (selectedMedia) => {
                if (selectedMedia && selectedMedia.url) {
                    this.selectMedia(targetId, selectedMedia.url);

                    // For logo widget, offer to sync to site settings
                    if (isLogoWidget && isLogoField && selectedMedia.id) {
                        const syncToSettings = await AdminModal.confirm(
                            'Would you like to also update the site logo in Site Settings?\n\n' +
                            'This will make this logo the default for all pages.'
                        );
                        if (syncToSettings) {
                            await this.builder.syncLogoToSiteSettings(selectedMedia.id);
                        }
                    }
                }
            }, {
                selectionMode: 'single',
                fileTypeFilter: 'image'
            });
        } else {
            // Fallback to URL prompt
            const url = await AdminModal.prompt('Enter image URL:');
            if (url) {
                this.selectMedia(targetId, url);
            }
        }
    }

    /**
     * Select media
     */
    selectMedia(targetId, url) {
        const input = document.getElementById(`prop-${targetId}`);
        const preview = document.getElementById(`media-preview-${targetId}`);

        if (input) {
            input.value = url;
        }

        if (preview) {
            preview.innerHTML = `<img src="${this.escapeHtml(url)}" alt="Preview">`;
        }

        this.updateLivePreview();
    }

    /**
     * Remove media
     */
    removeMedia(targetId) {
        const input = document.getElementById(`prop-${targetId}`);
        const preview = document.getElementById(`media-preview-${targetId}`);

        if (input) {
            input.value = '';
        }

        if (preview) {
            preview.innerHTML = `
                <div class="hfb-media-preview-empty">
                    <i class="fas fa-image"></i>
                    <span>No image selected</span>
                </div>
            `;
        }

        this.updateLivePreview();
    }

    /**
     * Add array item
     */
    addArrayItem(propertyKey) {
        const widgetType = this.currentWidget?.widget_type;
        const schema = this.builder.widgetSchemas?.[widgetType] || WIDGET_SCHEMAS?.[widgetType];
        if (!schema) return;

        // Find the field schema
        let fieldSchema = null;
        for (const group of schema.groups) {
            for (const field of group.fields) {
                if (field.key === propertyKey && field.type === 'array') {
                    fieldSchema = field;
                    break;
                }
            }
        }

        if (!fieldSchema) return;

        const container = document.getElementById(`array-${propertyKey}`);
        const itemsContainer = container.querySelector('.hfb-array-items');

        // Remove empty message if present
        const emptyMsg = itemsContainer.querySelector('.hfb-array-empty');
        if (emptyMsg) emptyMsg.remove();

        // Create new empty item
        const newItem = {};
        for (const key of Object.keys(fieldSchema.itemSchema)) {
            newItem[key] = '';
        }

        const index = itemsContainer.querySelectorAll('.hfb-array-item').length;
        const itemHtml = this.renderArrayItem(fieldSchema, newItem, index);

        itemsContainer.insertAdjacentHTML('beforeend', itemHtml);

        // Re-setup event listeners for new item
        this.setupArrayItemListeners(propertyKey, index);
    }

    /**
     * Re-index array items after reordering
     */
    reindexArrayItems(propertyKey) {
        const container = document.getElementById(`array-${propertyKey}`);
        if (!container) return;

        const items = container.querySelectorAll('.hfb-array-item');
        items.forEach((item, newIndex) => {
            item.dataset.index = newIndex;
            const numberSpan = item.querySelector('.hfb-array-item-number');
            if (numberSpan) {
                numberSpan.textContent = `Item ${newIndex + 1}`;
            }

            // Update input IDs
            item.querySelectorAll('[data-index]').forEach(input => {
                const oldId = input.id;
                const field = input.dataset.field;
                const newId = `prop-${propertyKey}-${newIndex}-${field}`;
                input.id = newId;
                input.dataset.index = newIndex;

                // Update associated preview elements
                const previewEl = document.getElementById(`icon-preview-${oldId}`);
                if (previewEl) {
                    previewEl.id = `icon-preview-${newId}`;
                }
            });
        });
    }

    /**
     * Setup event listeners for a specific array item
     */
    setupArrayItemListeners(propertyKey, index) {
        const container = document.getElementById(`array-${propertyKey}`);
        const item = container.querySelector(`.hfb-array-item[data-index="${index}"]`);
        if (!item) return;

        // Delete button
        item.querySelector('.hfb-array-item-btn.delete')?.addEventListener('click', () => {
            item.remove();
            this.reindexArrayItems(propertyKey);
        });

        // Move buttons
        item.querySelector('.hfb-array-item-btn.move-up')?.addEventListener('click', () => {
            const prev = item.previousElementSibling;
            if (prev && prev.classList.contains('hfb-array-item')) {
                item.parentNode.insertBefore(item, prev);
                this.reindexArrayItems(propertyKey);
            }
        });

        item.querySelector('.hfb-array-item-btn.move-down')?.addEventListener('click', () => {
            const next = item.nextElementSibling;
            if (next && next.classList.contains('hfb-array-item')) {
                item.parentNode.insertBefore(next, item);
                this.reindexArrayItems(propertyKey);
            }
        });

        // Icon picker
        item.querySelectorAll('.hfb-icon-picker-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                this.openIconPicker(btn.dataset.target);
            });
        });
    }

    /**
     * Reset property to default
     */
    resetProperty(propertyKey) {
        const widgetType = this.currentWidget?.widget_type;
        const schema = this.builder.widgetSchemas?.[widgetType] || WIDGET_SCHEMAS?.[widgetType];
        if (!schema) return;

        // Find the field's default value
        let defaultValue = '';
        for (const group of schema.groups) {
            for (const field of group.fields) {
                if (field.key === propertyKey) {
                    defaultValue = field.default !== undefined ? field.default : '';
                    break;
                }
            }
        }

        const element = document.getElementById(`prop-${propertyKey}`);
        if (element) {
            if (element.type === 'checkbox') {
                element.checked = defaultValue === true;
            } else {
                element.value = defaultValue;
            }
            element.dispatchEvent(new Event('change', { bubbles: true }));
        }
    }

    /**
     * Update live preview using server-rendered templates
     */
    async updateLivePreview() {
        if (this.builder && this.currentWidget) {
            const config = this.collectFormValues();
            if (config) {
                this.currentWidget.config = config;

                // Fetch server-rendered preview for accurate display
                const previewHtml = await this.builder.fetchWidgetPreview(
                    this.currentWidget.widget_type,
                    config
                );

                // Update the widget content in the DOM
                const widgetWrapper = document.querySelector(
                    `.widget-wrapper[data-placement-id="${this.currentWidget.id}"]`
                );
                if (widgetWrapper) {
                    const contentContainer = widgetWrapper.querySelector('.widget-content');
                    if (contentContainer) {
                        contentContainer.innerHTML = previewHtml;
                    }
                }
            }
        }
    }

    /**
     * Load dynamic options (menus, etc.)
     */
    async loadDynamicOptions() {
        try {
            // Load menus
            const menuResponse = await fetch('/api/hf-builder/menus/');
            if (menuResponse.ok) {
                const menus = await menuResponse.json();
                this.dynamicOptions.menus = menus.map(m => ({ value: m.id, label: m.name }));

                // Filter account menus for the account widget
                this.dynamicOptions.account_menus = menus
                    .filter(m => m.location === 'account' || m.slug === 'account-menu')
                    .map(m => ({ value: m.id, label: m.name }));
            }
        } catch (error) {
            console.error('Failed to load dynamic options:', error);
        }
    }

    /**
     * Escape HTML to prevent XSS
     */
    escapeHtml(str) {
        if (str === null || str === undefined) return '';
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }
}

class HeaderFooterBuilder {
    constructor(config) {
        this.config = config;
        this.builderType = config.builderType; // 'header' or 'footer'
        this.templateId = config.templateId;
        this.apiUrl = config.apiUrl;
        this.currentData = null;
        this.selectedWidget = null;
        this.isDragging = false;
        this.currentDevice = 'desktop'; // Track current device view: mobile, tablet, desktop
        this.widgetSchemas = {}; // Widget property schemas loaded from API
        this.siteLogoData = null; // Site logo data from SiteSettings

        console.log('HeaderFooterBuilder initialized:', this.builderType, this.templateId);

        this.init();
    }

    async init() {
        // Initialize UI components
        this.setupEventListeners();
        this.setupTabs();
        this.setupDeviceToggle();
        this.setupTemplateSelector();

        // Fetch all data in parallel (schemas, logo, template, widget library are independent)
        // Also await theme CSS loading (started by hf-css-loader.js on DOMContentLoaded)
        await Promise.all([
            this.loadWidgetSchemas(),
            this.fetchSiteLogo(),
            this.fetchTemplateData(),
            this.loadWidgetLibrary(),
            window.HFCssLoaderReady || Promise.resolve(),
        ]);

        // Render after all data is available
        this.renderPreview();
        this.initializeStatusIndicator();

        console.log('Builder initialization complete');
    }

    /**
     * Fetch site logo data from SiteSettings
     * Used by logo widget to display and sync site logo
     */
    async fetchSiteLogo() {
        try {
            const response = await fetch('/api/hf-builder/site-logo/', {
                headers: {
                    'X-CSRFToken': this.config.csrfToken || document.querySelector('[name=csrfmiddlewaretoken]')?.value || ''
                }
            });
            if (response.ok) {
                this.siteLogoData = await response.json();
                console.log('Site logo data loaded:', this.siteLogoData);
            }
        } catch (error) {
            console.error('Failed to fetch site logo:', error);
            this.siteLogoData = { has_logo: false, logo_url: null };
        }
    }

    /**
     * Sync a logo to site settings
     * @param {string} assetId - Media asset UUID to set as site logo
     */
    async syncLogoToSiteSettings(assetId) {
        try {
            const response = await fetch('/api/hf-builder/site-logo/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.config.csrfToken || document.querySelector('[name=csrfmiddlewaretoken]')?.value || ''
                },
                body: JSON.stringify({ asset_id: assetId })
            });
            const data = await response.json();
            if (data.success) {
                this.siteLogoData = { ...this.siteLogoData, has_logo: true, logo_url: data.logo_url };
                this.showNotification('Site logo updated successfully', 'success');
                return true;
            } else {
                this.showNotification(data.error || 'Failed to update site logo', 'error');
                return false;
            }
        } catch (error) {
            console.error('Failed to sync logo to site settings:', error);
            this.showNotification('Failed to update site logo', 'error');
            return false;
        }
    }

    setupEventListeners() {
        // Draft/Publish buttons
        const saveDraftBtn = document.getElementById('save-draft-btn');
        const publishBtn = document.getElementById('publish-btn');
        const discardBtn = document.getElementById('discard-btn');

        if (saveDraftBtn) {
            saveDraftBtn.addEventListener('click', () => this.saveDraft());
        }

        if (publishBtn) {
            publishBtn.addEventListener('click', () => this.publish());
        }

        if (discardBtn) {
            discardBtn.addEventListener('click', () => this.discardDraft());
        }

        // Legacy save button (if exists, for backwards compatibility)
        const saveBtn = document.getElementById('save-btn');
        if (saveBtn) {
            saveBtn.addEventListener('click', () => this.saveDraft());
        }

        // Preset gallery
        const presetBtn = document.getElementById('preset-btn');
        const presetModal = document.getElementById('preset-modal');
        const presetCloseBtn = document.getElementById('preset-close-btn');

        if (presetBtn) {
            presetBtn.addEventListener('click', () => this.openPresetGallery());
        }

        if (presetCloseBtn) {
            presetCloseBtn.addEventListener('click', () => this.closePresetGallery());
        }

        if (presetModal) {
            presetModal.addEventListener('click', (e) => {
                if (e.target === presetModal) {
                    this.closePresetGallery();
                }
            });
        }

        // Widget search
        const searchInput = document.getElementById('widget-search');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => this.filterWidgets(e.target.value));
        }
    }

    setupDeviceToggle() {
        const deviceToggles = document.querySelectorAll('.device-toggle');
        const canvasFrame = document.getElementById('canvas-frame');

        deviceToggles.forEach(toggle => {
            toggle.addEventListener('click', () => {
                // Remove active from all
                deviceToggles.forEach(t => t.classList.remove('active'));
                // Add active to clicked
                toggle.classList.add('active');

                // Update canvas size
                const device = toggle.dataset.device;
                canvasFrame.classList.remove('mobile-preview', 'tablet-preview', 'desktop-preview');
                canvasFrame.classList.add(`${device}-preview`);

                // Store current device and re-render preview to show/hide zones
                this.currentDevice = device;
                this.renderPreview();
            });
        });
    }

    setupTemplateSelector() {
        const selector = document.getElementById('template-selector');
        if (selector) {
            selector.addEventListener('change', (e) => {
                const newId = e.target.value;
                const newUrl = window.location.pathname.replace(/\/\d+\//, `/${newId}/`);
                window.location.href = newUrl;
            });
        }
    }

    setupTabs() {
        const tabButtons = document.querySelectorAll('.admin-tab-btn');
        const tabContents = document.querySelectorAll('.admin-tab-content');

        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                const tabName = button.dataset.tab;

                // Remove active class from all tabs
                tabButtons.forEach(btn => btn.classList.remove('active'));
                tabContents.forEach(content => content.classList.remove('active'));

                // Add active class to clicked tab
                button.classList.add('active');
                const targetTab = document.getElementById(`${tabName}-tab`);
                if (targetTab) {
                    targetTab.classList.add('active');
                }
            });
        });
    }

    showZoneConfig(primaryZone) {
        // Switch to zone config tab
        document.querySelector('.admin-tab-btn[data-tab="zone-config"]')?.click();

        const content = document.getElementById('zone-config-content');
        if (!content) return;

        // Special handling for notification zone
        if (primaryZone === 'notification') {
            const config = this.currentData.notification_zone_config || {};
            content.innerHTML = this.renderNotificationZoneConfigPanel(config);
            this.setupNotificationZoneConfigListeners();
            return;
        }

        const zoneConfig = this.currentData.zone_overrides?.[primaryZone] || this.getDefaultZoneConfig(primaryZone);

        content.innerHTML = this.renderZoneConfigPanel(primaryZone, zoneConfig);

        // Setup event listeners for zone config controls
        this.setupZoneConfigListeners(primaryZone);
    }

    renderNotificationZoneConfigPanel(config) {
        const displayMode = config.display_mode || 'scroll_horizontal';
        const scrollSpeed = config.scroll_speed ?? 20;
        const cycleDuration = config.cycle_duration ?? 5;
        const dismissible = config.dismissible ?? true;
        const pauseOnHover = config.pause_on_hover ?? true;

        return `
            <div class="zone-config-section">
                <div class="zone-config-header">
                    <h3 class="zone-config-title">
                        <i class="fas fa-bullhorn"></i>
                        Notification Zone
                    </h3>
                </div>

                <p class="zone-config-help" style="color: var(--admin-text-muted); font-size: 0.85rem; margin: 0 0 1rem;">
                    Displays active announcements above the header. Content is managed in
                    <a href="${HFBuilderConfig.announcementsUrl}" target="_blank" style="color: var(--admin-primary);">Announcements</a>.
                </p>

                <div class="zone-config-row">
                    <label class="zone-config-label">
                        <i class="fas fa-toggle-on" style="width: 18px;"></i>
                        Enabled
                    </label>
                    <label class="hfb-toggle-switch">
                        <input type="checkbox" id="nz-enabled" ${this.currentData.enable_notification_zone !== false ? 'checked' : ''}>
                        <span class="hfb-toggle-slider"></span>
                    </label>
                </div>

                <div class="zone-config-row">
                    <label class="zone-config-label">
                        <i class="fas fa-exchange-alt" style="width: 18px;"></i>
                        Display Mode
                    </label>
                    <select id="nz-display-mode" class="zone-config-select" style="flex: 1; padding: 6px 8px; border-radius: 6px; border: 1px solid var(--admin-border-color); background: var(--admin-surface); color: var(--admin-text);">
                        <option value="scroll_horizontal" ${displayMode === 'scroll_horizontal' ? 'selected' : ''}>Horizontal Scroll</option>
                        <option value="scroll_vertical" ${displayMode === 'scroll_vertical' ? 'selected' : ''}>Vertical Cycle</option>
                        <option value="static" ${displayMode === 'static' ? 'selected' : ''}>Static</option>
                    </select>
                </div>

                <div class="zone-config-row">
                    <label class="zone-config-label">
                        <i class="fas fa-tachometer-alt" style="width: 18px;"></i>
                        Scroll Speed
                    </label>
                    <div style="flex: 1; display: flex; align-items: center; gap: 8px;">
                        <input type="range" id="nz-scroll-speed" min="5" max="60" value="${scrollSpeed}"
                               class="zone-config-slider" style="flex: 1;">
                        <span class="zone-config-slider-value" id="nz-scroll-speed-value">${scrollSpeed}s</span>
                    </div>
                </div>

                <div class="zone-config-row">
                    <label class="zone-config-label">
                        <i class="fas fa-clock" style="width: 18px;"></i>
                        Cycle Duration
                    </label>
                    <div style="flex: 1; display: flex; align-items: center; gap: 8px;">
                        <input type="range" id="nz-cycle-duration" min="2" max="30" value="${cycleDuration}"
                               class="zone-config-slider" style="flex: 1;">
                        <span class="zone-config-slider-value" id="nz-cycle-duration-value">${cycleDuration}s</span>
                    </div>
                </div>

                <div class="zone-config-row">
                    <label class="zone-config-label">
                        <i class="fas fa-times-circle" style="width: 18px;"></i>
                        Dismissible
                    </label>
                    <label class="hfb-toggle-switch">
                        <input type="checkbox" id="nz-dismissible" ${dismissible ? 'checked' : ''}>
                        <span class="hfb-toggle-slider"></span>
                    </label>
                </div>

                <div class="zone-config-row">
                    <label class="zone-config-label">
                        <i class="fas fa-pause-circle" style="width: 18px;"></i>
                        Pause on Hover
                    </label>
                    <label class="hfb-toggle-switch">
                        <input type="checkbox" id="nz-pause-hover" ${pauseOnHover ? 'checked' : ''}>
                        <span class="hfb-toggle-slider"></span>
                    </label>
                </div>

                <div style="margin-top: 1rem;">
                    <button class="btn btn-primary" id="save-nz-config" style="width: 100%;">
                        <i class="fas fa-check"></i> Apply Changes
                    </button>
                </div>
            </div>
        `;
    }

    setupNotificationZoneConfigListeners() {
        // Slider value display updates
        const scrollSpeedSlider = document.getElementById('nz-scroll-speed');
        if (scrollSpeedSlider) {
            scrollSpeedSlider.addEventListener('input', (e) => {
                document.getElementById('nz-scroll-speed-value').textContent = `${e.target.value}s`;
            });
        }

        const cycleDurationSlider = document.getElementById('nz-cycle-duration');
        if (cycleDurationSlider) {
            cycleDurationSlider.addEventListener('input', (e) => {
                document.getElementById('nz-cycle-duration-value').textContent = `${e.target.value}s`;
            });
        }

        // Save button
        const saveBtn = document.getElementById('save-nz-config');
        if (saveBtn) {
            saveBtn.addEventListener('click', () => {
                this.saveNotificationZoneConfig();
            });
        }
    }

    saveNotificationZoneConfig() {
        const enabled = document.getElementById('nz-enabled')?.checked ?? true;
        const displayMode = document.getElementById('nz-display-mode')?.value || 'scroll_horizontal';
        const scrollSpeed = parseInt(document.getElementById('nz-scroll-speed')?.value || '20', 10);
        const cycleDuration = parseInt(document.getElementById('nz-cycle-duration')?.value || '5', 10);
        const dismissible = document.getElementById('nz-dismissible')?.checked ?? true;
        const pauseOnHover = document.getElementById('nz-pause-hover')?.checked ?? true;

        this.currentData.enable_notification_zone = enabled;
        this.currentData.notification_zone_config = {
            display_mode: displayMode,
            scroll_speed: scrollSpeed,
            cycle_duration: cycleDuration,
            dismissible: dismissible,
            pause_on_hover: pauseOnHover
        };

        // Re-render preview to show/hide notification zone
        this.renderPreview();
        this.updateStatusIndicator('draft');
    }

    getDefaultZoneConfig(zoneName = 'main-header') {
        // Header zone defaults using theme zone tokens
        const headerZoneDefaults = {
            'top-bar': {
                height: 36,
                background: { type: "theme", value: "var(--theme-header-zones-top-bar-background, var(--theme-color-background-secondary))" },
                text_color: { type: "theme", value: "var(--theme-header-zones-top-bar-text-color, var(--theme-color-text-muted))" },
                visibility: { mobile: false, tablet: true, desktop: true },
                spacing: { padding: "var(--theme-header-zones-top-bar-padding-y, var(--theme-space-2)) 0", margin: "0" }
            },
            'main-header': {
                height: 70,
                background: { type: "theme", value: "var(--theme-header-zones-main-header-background, var(--theme-color-surface))" },
                text_color: { type: "theme", value: "var(--theme-header-zones-main-header-text-color, var(--theme-color-text))" },
                visibility: { mobile: true, tablet: true, desktop: true },
                spacing: { padding: "var(--theme-header-zones-main-header-padding-y, var(--theme-space-4)) 0", margin: "0" },
                sticky: true,
                shadow_on_scroll: true
            },
            'bottom-bar': {
                height: 50,
                background: { type: "theme", value: "var(--theme-header-zones-bottom-bar-background, var(--theme-color-background-secondary))" },
                text_color: { type: "theme", value: "var(--theme-header-zones-bottom-bar-text-color, var(--theme-color-text))" },
                visibility: { mobile: false, tablet: true, desktop: true },
                spacing: { padding: "var(--theme-header-zones-bottom-bar-padding-y, var(--theme-space-3)) 0", margin: "0" }
            },
            'mega-menu-bar': {
                height: 60,
                background: { type: "theme", value: "var(--theme-header-zones-mega-menu-bar-background, var(--theme-color-background-secondary))" },
                text_color: { type: "theme", value: "var(--theme-header-zones-mega-menu-bar-text-color, var(--theme-color-text))" },
                visibility: { mobile: false, tablet: false, desktop: true },
                spacing: { padding: "var(--theme-header-zones-mega-menu-bar-padding-y, var(--theme-space-4)) 0", margin: "0" }
            }
        };

        // Footer zone defaults using theme zone tokens
        const footerZoneDefaults = {
            'top': {
                height: 80,
                background: { type: "theme", value: "var(--theme-footer-zones-top-background, transparent)" },
                text_color: { type: "theme", value: "var(--theme-footer-text-color, var(--theme-color-text-inverse))" },
                visibility: { mobile: true, tablet: true, desktop: true },
                spacing: { padding: "var(--theme-footer-zones-top-padding-y, var(--theme-space-12)) 0", margin: "0" }
            },
            'main': {
                height: 200,
                background: { type: "theme", value: "var(--theme-footer-zones-main-background, transparent)" },
                text_color: { type: "theme", value: "var(--theme-footer-text-color, var(--theme-color-text-inverse))" },
                visibility: { mobile: true, tablet: true, desktop: true },
                spacing: { padding: "var(--theme-footer-zones-main-padding-y, var(--theme-space-8)) 0", margin: "0" }
            },
            'bottom': {
                height: 60,
                background: { type: "theme", value: "var(--theme-footer-zones-bottom-background, rgba(0, 0, 0, 0.2))" },
                text_color: { type: "theme", value: "var(--theme-footer-text-color, var(--theme-color-text-inverse))" },
                visibility: { mobile: true, tablet: true, desktop: true },
                spacing: { padding: "var(--theme-footer-zones-bottom-padding-y, var(--theme-space-6)) 0", margin: "0" }
            },
            'bottom-bar': {
                height: 60,
                background: { type: "theme", value: "var(--theme-footer-zones-bottom-background, rgba(0, 0, 0, 0.2))" },
                text_color: { type: "theme", value: "var(--theme-footer-text-color, var(--theme-color-text-inverse))" },
                visibility: { mobile: true, tablet: true, desktop: true },
                spacing: { padding: "var(--theme-footer-zones-bottom-padding-y, var(--theme-space-6)) 0", margin: "0" }
            }
        };

        // Default for footer columns (col-1, col-2, section-1, etc.)
        const footerColumnDefault = {
            height: 'auto',
            background: { type: "theme", value: "var(--theme-footer-zones-main-background, transparent)" },
            text_color: { type: "theme", value: "var(--theme-footer-text-color, var(--theme-color-text-inverse))" },
            visibility: { mobile: true, tablet: true, desktop: true },
            spacing: { padding: "var(--theme-space-4, 1rem)", margin: "0" }
        };

        // Determine which default to use based on zone name and builder type
        let zoneOverrides;

        if (this.builderType === 'footer') {
            // Check for specific footer zones first
            if (footerZoneDefaults[zoneName]) {
                zoneOverrides = footerZoneDefaults[zoneName];
            } else if (zoneName.startsWith('col-') || zoneName.startsWith('section-') || zoneName === 'single') {
                zoneOverrides = footerColumnDefault;
            } else {
                zoneOverrides = footerZoneDefaults['main'];
            }
        } else {
            // Header zones
            zoneOverrides = headerZoneDefaults[zoneName] || headerZoneDefaults['main-header'];
        }

        return {
            enabled: true,
            height: zoneOverrides.height || 70,
            full_width: false,
            visibility: zoneOverrides.visibility || { mobile: true, tablet: true, desktop: true },
            background: zoneOverrides.background || { type: "theme", value: "var(--theme-header-zones-main-header-background, var(--theme-color-surface))" },
            text_color: zoneOverrides.text_color || null,
            border_bottom: { color: "var(--theme-color-border)", size: 1 },
            sticky: zoneOverrides.sticky || false,
            sticky_background: null,
            glass_effect: 0,
            collapse_on_scroll: false,
            spacing: zoneOverrides.spacing || { padding: "var(--theme-space-4, 1rem) 0", margin: "0" },
            shadow_on_scroll: zoneOverrides.shadow_on_scroll || false
        };
    }

    renderZoneConfigPanel(primaryZone, config) {
        const zoneName = primaryZone.replace('-', ' ').replace('_', ' ');

        return `
            <div class="zone-config-section">
                <div class="zone-config-header">
                    <h3 class="zone-config-title">
                        <i class="fas fa-layer-group"></i>
                        ${zoneName.charAt(0).toUpperCase() + zoneName.slice(1)}
                    </h3>
                </div>

                <!-- Basic Layout -->
                <div class="zone-config-row">
                    <label class="zone-config-label">
                        <i class="fas fa-arrows-alt-v"></i> Height
                    </label>
                    <div style="display: flex; align-items: center; gap: 0.5rem;">
                        <input type="range"
                               class="zone-config-slider"
                               id="zone-height"
                               min="40"
                               max="200"
                               value="${config.height || 70}"
                               data-config="height">
                        <span class="zone-config-slider-value" id="zone-height-value">${config.height || 70}px</span>
                    </div>
                </div>

                <!-- Device Visibility -->
                <div class="zone-config-row">
                    <label class="zone-config-label">
                        <i class="fas fa-eye"></i> Device Visibility
                    </label>
                    <div class="device-visibility-group">
                        <button class="device-visibility-btn ${config.visibility?.mobile !== false ? 'active' : ''}"
                                data-device="mobile">
                            <i class="fas fa-mobile-alt"></i>
                            <span>Mobile</span>
                        </button>
                        <button class="device-visibility-btn ${config.visibility?.tablet !== false ? 'active' : ''}"
                                data-device="tablet">
                            <i class="fas fa-tablet-alt"></i>
                            <span>Tablet</span>
                        </button>
                        <button class="device-visibility-btn ${config.visibility?.desktop !== false ? 'active' : ''}"
                                data-device="desktop">
                            <i class="fas fa-desktop"></i>
                            <span>Desktop</span>
                        </button>
                    </div>
                </div>

                <!-- Full Width Toggle -->
                <div class="zone-config-row">
                    <div class="zone-checkbox-wrapper">
                        <input type="checkbox"
                               class="zone-checkbox"
                               id="zone-full-width"
                               ${config.full_width ? 'checked' : ''}
                               data-config="full_width">
                        <label class="zone-checkbox-label" for="zone-full-width">
                            <i class="fas fa-arrows-alt-h"></i> Full Width Container
                        </label>
                    </div>
                </div>

                <!-- Sticky Header -->
                <div class="zone-config-row">
                    <div class="zone-checkbox-wrapper">
                        <input type="checkbox"
                               class="zone-checkbox"
                               id="zone-sticky"
                               ${config.sticky ? 'checked' : ''}
                               data-config="sticky">
                        <label class="zone-checkbox-label" for="zone-sticky">
                            <i class="fas fa-thumbtack"></i> Sticky Header
                        </label>
                    </div>
                </div>

                <!-- Advanced Options -->
                <div class="zone-advanced-toggle" id="advanced-toggle">
                    <span style="font-weight: 500; font-size: 0.875rem;">
                        <i class="fas fa-cog"></i> Advanced Design
                    </span>
                    <i class="fas fa-chevron-down"></i>
                </div>
                <div class="zone-advanced-content" id="advanced-content">

                    <!-- Border Bottom -->
                    <div class="zone-config-row">
                        <label class="zone-config-label">Border Bottom Size</label>
                        <div style="display: flex; align-items: center; gap: 0.5rem;">
                            <input type="range"
                                   class="zone-config-slider"
                                   id="zone-border-size"
                                   min="0"
                                   max="10"
                                   value="${config.border_bottom?.size || 1}"
                                   data-config="border_bottom.size">
                            <span class="zone-config-slider-value" id="zone-border-size-value">${config.border_bottom?.size || 1}px</span>
                        </div>
                    </div>

                    <!-- Glass Effect -->
                    <div class="zone-config-row">
                        <label class="zone-config-label">Glass Effect (Blur)</label>
                        <div style="display: flex; align-items: center; gap: 0.5rem;">
                            <input type="range"
                                   class="zone-config-slider"
                                   id="zone-glass"
                                   min="0"
                                   max="20"
                                   value="${config.glass_effect || 0}"
                                   data-config="glass_effect">
                            <span class="zone-config-slider-value" id="zone-glass-value">${config.glass_effect || 0}px</span>
                        </div>
                    </div>

                    <!-- Collapse on Scroll -->
                    <div class="zone-config-row">
                        <div class="zone-checkbox-wrapper">
                            <input type="checkbox"
                                   class="zone-checkbox"
                                   id="zone-collapse"
                                   ${config.collapse_on_scroll ? 'checked' : ''}
                                   data-config="collapse_on_scroll">
                            <label class="zone-checkbox-label" for="zone-collapse">
                                <i class="fas fa-compress-alt"></i> Collapse on Scroll
                            </label>
                        </div>
                    </div>

                    <!-- Shadow on Scroll -->
                    <div class="zone-config-row">
                        <div class="zone-checkbox-wrapper">
                            <input type="checkbox"
                                   class="zone-checkbox"
                                   id="zone-shadow"
                                   ${config.shadow_on_scroll ? 'checked' : ''}
                                   data-config="shadow_on_scroll">
                            <label class="zone-checkbox-label" for="zone-shadow">
                                <i class="fas fa-circle-notch"></i> Shadow on Scroll
                            </label>
                        </div>
                    </div>
                </div>

                ${this.builderType === 'header' && primaryZone === 'main-header' ? `
                <!-- Mobile Menu Settings (header main-header zone only) -->
                <div class="zone-advanced-toggle" id="mobile-settings-toggle" style="margin-top: 1rem;">
                    <span style="font-weight: 500; font-size: 0.875rem;">
                        <i class="fas fa-mobile-alt"></i> Mobile Settings
                    </span>
                    <i class="fas fa-chevron-down"></i>
                </div>
                <div class="zone-advanced-content" id="mobile-settings-content">
                    <div class="zone-config-row">
                        <label class="zone-config-label">
                            <i class="fas fa-bars" style="width: 18px;"></i>
                            Hamburger Position
                        </label>
                        <select id="hamburger-position" class="zone-config-select" style="flex: 1; padding: 6px 8px; border-radius: 6px; border: 1px solid var(--admin-border-color); background: var(--admin-surface); color: var(--admin-text);">
                            <option value="left" ${(this.currentData.mobile_menu_position || 'right') === 'left' ? 'selected' : ''}>Left</option>
                            <option value="right" ${(this.currentData.mobile_menu_position || 'right') === 'right' ? 'selected' : ''}>Right</option>
                        </select>
                    </div>
                </div>
                ` : ''}

                <!-- Save Button -->
                <div style="margin-top: 1.5rem;">
                    <button class="btn btn-primary" id="save-zone-config" style="width: 100%;">
                        <i class="fas fa-save"></i> Save Zone Configuration
                    </button>
                </div>
            </div>
        `;
    }

    setupZoneConfigListeners(primaryZone) {
        // Height slider
        const heightSlider = document.getElementById('zone-height');
        const heightValue = document.getElementById('zone-height-value');
        if (heightSlider && heightValue) {
            heightSlider.addEventListener('input', (e) => {
                heightValue.textContent = e.target.value + 'px';
            });
        }

        // Border size slider
        const borderSlider = document.getElementById('zone-border-size');
        const borderValue = document.getElementById('zone-border-size-value');
        if (borderSlider && borderValue) {
            borderSlider.addEventListener('input', (e) => {
                borderValue.textContent = e.target.value + 'px';
            });
        }

        // Glass effect slider
        const glassSlider = document.getElementById('zone-glass');
        const glassValue = document.getElementById('zone-glass-value');
        if (glassSlider && glassValue) {
            glassSlider.addEventListener('input', (e) => {
                glassValue.textContent = e.target.value + 'px';
            });
        }

        // Device visibility buttons
        const deviceButtons = document.querySelectorAll('.device-visibility-btn');
        deviceButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                btn.classList.toggle('active');
            });
        });

        // Advanced toggle
        const advancedToggle = document.getElementById('advanced-toggle');
        const advancedContent = document.getElementById('advanced-content');
        if (advancedToggle && advancedContent) {
            advancedToggle.addEventListener('click', () => {
                advancedToggle.classList.toggle('active');
                advancedContent.classList.toggle('active');
            });
        }

        // Mobile settings toggle (main-header zone only)
        const mobileToggle = document.getElementById('mobile-settings-toggle');
        const mobileContent = document.getElementById('mobile-settings-content');
        if (mobileToggle && mobileContent) {
            mobileToggle.addEventListener('click', () => {
                mobileToggle.classList.toggle('active');
                mobileContent.classList.toggle('active');
            });
        }

        // Save button
        const saveBtn = document.getElementById('save-zone-config');
        if (saveBtn) {
            saveBtn.addEventListener('click', () => {
                this.saveZoneConfig(primaryZone);
            });
        }
    }

    async saveZoneConfig(primaryZone) {
        const config = {
            height: parseInt(document.getElementById('zone-height')?.value || 70),
            full_width: document.getElementById('zone-full-width')?.checked || false,
            sticky: document.getElementById('zone-sticky')?.checked || false,
            visibility: {
                mobile: document.querySelector('.device-visibility-btn[data-device="mobile"]')?.classList.contains('active') !== false,
                tablet: document.querySelector('.device-visibility-btn[data-device="tablet"]')?.classList.contains('active') !== false,
                desktop: document.querySelector('.device-visibility-btn[data-device="desktop"]')?.classList.contains('active') !== false,
            },
            border_bottom: {
                color: "var(--theme-color-border)",
                size: parseInt(document.getElementById('zone-border-size')?.value || 1)
            },
            glass_effect: parseInt(document.getElementById('zone-glass')?.value || 0),
            collapse_on_scroll: document.getElementById('zone-collapse')?.checked || false,
            shadow_on_scroll: document.getElementById('zone-shadow')?.checked || false,
        };

        try {
            // Update zone_overrides in the template
            if (!this.currentData.zone_overrides) {
                this.currentData.zone_overrides = {};
            }
            this.currentData.zone_overrides[primaryZone] = config;

            // Build save payload
            const savePayload = {
                zone_overrides: this.currentData.zone_overrides
            };

            // Save hamburger position if on main-header zone
            if (primaryZone === 'main-header') {
                const hamburgerSelect = document.getElementById('hamburger-position');
                if (hamburgerSelect) {
                    savePayload.mobile_menu_position = hamburgerSelect.value;
                    this.currentData.mobile_menu_position = hamburgerSelect.value;
                }
            }

            // Save to server
            const response = await fetch(this.apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.config.csrfToken,
                },
                body: JSON.stringify(savePayload)
            });

            if (!response.ok) {
                throw new Error('Failed to save zone configuration');
            }

            // Reload template to reflect changes
            await this.loadTemplate();

            this.showSuccess('Zone configuration saved successfully');
        } catch (error) {
            console.error('Error saving zone config:', error);
            this.showError('Failed to save zone configuration');
        }
    }

    showSuccess(message) {
        // Simple success notification (can be enhanced later)
        AdminModal.toast(message, 'success');
    }

    /**
     * Show notification message
     * @param {string} message - Message to display
     * @param {string} type - 'success', 'error', or 'info'
     */
    showNotification(message, type = 'info') {
        AdminModal.toast(message, type || 'info');
    }

    async loadWidgetSchemas() {
        try {
            if (!this.config.schemaUrl) {
                console.warn('No schemaUrl configured, using fallback JSON editor');
                return;
            }

            console.log('Loading widget schemas from:', this.config.schemaUrl);

            const response = await fetch(this.config.schemaUrl);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            // DRF returns data directly (success indicated by HTTP 200)
            if (data.schemas) {
                this.widgetSchemas = data.schemas;
                console.log('Widget schemas loaded:', Object.keys(this.widgetSchemas).length, 'schemas');
            }

        } catch (error) {
            console.error('Error loading widget schemas:', error);
            // Don't show error to user - fallback to JSON editor will work
        }
    }

    /**
     * Fetch server-rendered widget preview
     * Uses actual Django templates for accurate preview
     */
    async fetchWidgetPreview(widgetType, config) {
        try {
            const response = await fetch('/api/hf-builder/widget-preview/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.config.csrfToken
                },
                body: JSON.stringify({
                    widget_type: widgetType,
                    config: config || {}
                })
            });

            if (response.ok) {
                const data = await response.json();
                return data.html;
            }
        } catch (error) {
            console.error('Widget preview fetch failed:', error);
        }

        // Fallback to client-side preview on error
        return this.renderWidgetPreviewFallback({ widget_type: widgetType, config });
    }

    /**
     * Fetch template data only (no rendering).
     * Used during init() for parallel loading with other data sources.
     */
    async fetchTemplateData() {
        try {
            const response = await fetch(this.apiUrl, {
                method: 'GET',
                headers: {
                    'X-CSRFToken': this.config.csrfToken,
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            this.currentData = data[this.builderType];
        } catch (error) {
            console.error('Error loading template:', error);
            this.showError(this.config.translations.error + ': ' + error.message);
        }
    }

    /**
     * Load template data and re-render preview.
     * Used after widget add/delete/reorder operations.
     */
    async loadTemplate() {
        try {
            const response = await fetch(this.apiUrl, {
                method: 'GET',
                headers: {
                    'X-CSRFToken': this.config.csrfToken,
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            this.currentData = data[this.builderType];
            this.renderPreview();

            // Initialize status indicator from loaded data
            this.initializeStatusIndicator();

        } catch (error) {
            console.error('Error loading template:', error);
            this.showError(this.config.translations.error + ': ' + error.message);
        }
    }

    async loadWidgetLibrary() {
        try {
            console.log('Loading widget library from:', this.config.widgetLibraryUrl);

            const response = await fetch(this.config.widgetLibraryUrl);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            console.log('Widget library loaded:', data);

            this.renderWidgetLibrary(data.widgets);

        } catch (error) {
            console.error('Error loading widgets:', error);
            this.showError('Failed to load widget library');
        }
    }

    renderWidgetLibrary(widgets) {
        const container = document.getElementById('widget-library');
        if (!container) return;

        container.innerHTML = '';

        // Group widgets by category
        const categories = {
            'Navigation': ['logo', 'menu', 'search'],
            'Shop': ['cart', 'account', 'currency', 'language'],
            'Content': ['text', 'links', 'newsletter', 'contact', 'site_variable'],
            'Social': ['social'],
            'Other': ['payment', 'trust_badges', 'custom']
        };

        Object.entries(categories).forEach(([categoryName, widgetTypes]) => {
            const categoryWidgets = {};

            // Collect widgets for this category
            widgetTypes.forEach(type => {
                if (widgets[type]) {
                    categoryWidgets[type] = widgets[type];
                }
            });

            // Only render if we have widgets
            if (Object.keys(categoryWidgets).length > 0) {
                const categoryEl = this.createWidgetCategory(categoryName, categoryWidgets);
                container.appendChild(categoryEl);
            }
        });
    }

    createWidgetCategory(name, widgets) {
        const category = document.createElement('div');
        category.className = 'widget-category';

        const header = document.createElement('div');
        header.className = 'category-header';
        header.innerHTML = `
            <i class="category-icon fas fa-cube"></i>
            <span class="category-title">${name}</span>
            <i class="category-toggle fas fa-chevron-down"></i>
        `;

        const widgetsContainer = document.createElement('div');
        widgetsContainer.className = 'category-widgets';

        Object.entries(widgets).forEach(([type, widgetList]) => {
            widgetList.forEach(widget => {
                const card = this.createWidgetCard(widget);
                widgetsContainer.appendChild(card);
            });
        });

        // Toggle collapse
        header.addEventListener('click', () => {
            header.classList.toggle('collapsed');
        });

        category.appendChild(header);
        category.appendChild(widgetsContainer);

        return category;
    }

    createWidgetCard(widget) {
        const card = document.createElement('div');
        card.className = 'widget-card';
        card.draggable = true;
        card.dataset.widgetId = widget.id;
        card.dataset.widgetType = widget.type;

        // Icon mapping
        const iconMap = {
            'logo': 'fa-image',
            'menu': 'fa-bars',
            'search': 'fa-search',
            'cart': 'fa-shopping-cart',
            'account': 'fa-user',
            'social': 'fa-share-alt',
            'text': 'fa-align-left',
            'links': 'fa-link',
            'newsletter': 'fa-envelope',
            'contact': 'fa-phone',
        };

        const icon = iconMap[widget.type] || 'fa-cube';

        card.innerHTML = `
            <div class="widget-icon">
                <i class="fas ${icon}"></i>
            </div>
            <div class="widget-info">
                <div class="widget-name">${widget.name}</div>
                <div class="widget-description">${widget.type_display}</div>
            </div>
        `;

        // Drag events
        card.addEventListener('dragstart', (e) => {
            this.isDragging = true;
            document.body.classList.add('is-dragging-widget');  // Global drag state for CSS
            e.dataTransfer.effectAllowed = 'copy';
            e.dataTransfer.setData('text/plain', JSON.stringify({
                widgetId: widget.id,
                widgetType: widget.type,
                widgetName: widget.name,
            }));
            card.classList.add('dragging');
        });

        card.addEventListener('dragend', () => {
            this.isDragging = false;
            document.body.classList.remove('is-dragging-widget');  // Remove global drag state
            card.classList.remove('dragging');
        });

        return card;
    }

    renderPreview() {
        const preview = document.getElementById('preview-content');
        if (!preview || !this.currentData) return;

        // Theme and brand CSS are loaded and scoped by hf-css-loader.js (awaited in init)

        // Use zone_layouts from template data if available, otherwise fall back to old method
        let zones = [];
        if (this.currentData.zone_layouts) {
            // NEW: Build zones from zone_layouts structure
            zones = this.getZonesFromLayouts(this.currentData.zone_layouts);
        } else {
            // FALLBACK: Old method for backward compatibility
            if (this.builderType === 'header') {
                zones = this.getHeaderZones(this.currentData.layout_type);
            } else {
                zones = this.getFooterZones(this.currentData.layout_type, this.currentData.column_count);
            }
        }

        // Build the preview HTML with preset class for theme CSS
        const layoutClass = `hf-${this.builderType}-${this.currentData.layout_type}`;
        const presetClass = `header-preset-${this.currentData.layout_type}`;
        let html = `<div class="hf-${this.builderType}-container ${layoutClass} ${presetClass}">`;

        // Notification zone indicator (header only, above all zones)
        if (this.builderType === 'header') {
            const nzEnabled = this.currentData.enable_notification_zone ?? true;
            if (nzEnabled) {
                html += `
                    <div class="hf-primary-zone header-zone header-zone--notification hf-notification-zone" data-primary-zone="notification">
                        <button class="zone-config-btn" data-primary-zone="notification" title="Configure notification zone">
                            <i class="fas fa-cog"></i>
                        </button>
                        <div class="hf-notification-preview">
                            <i class="fas fa-bullhorn"></i>
                            <span>Announcement Bar &mdash; Displays active announcements</span>
                        </div>
                    </div>`;
            }
        }

        // Get primary zones for grouping
        const primaryZones = this.getPrimaryZonesFromLayout();
        let currentPrimaryZone = null;

        // Determine device visibility key for filtering
        const deviceVisibilityKey = this.currentDevice === 'mobile' ? 'show_on_mobile'
            : this.currentDevice === 'tablet' ? 'show_on_tablet'
            : 'show_on_desktop';

        // Track if we've injected the hamburger toggle for mobile preview
        let hamburgerInjected = false;
        const menuPosition = this.currentData.mobile_menu_position || 'right';

        zones.forEach(zone => {
            const allZoneWidgets = this.currentData.zones[zone] || [];
            // Filter widgets by device visibility
            const zoneWidgets = allZoneWidgets.filter(w => w[deviceVisibilityKey] !== false);
            const isEmpty = zoneWidgets.length === 0;

            // Determine primary zone (e.g., "main-header" from "main-header_left")
            const primaryZone = zone.includes('_') ? zone.split('_')[0] : zone;

            // If we're entering a new primary zone, add the primary zone wrapper
            if (primaryZone !== currentPrimaryZone) {
                if (currentPrimaryZone !== null) {
                    html += `</div>`; // Close previous primary zone
                }
                currentPrimaryZone = primaryZone;

                // Get zone overrides (only merchant customizations, not full config)
                // Base styling comes from .header-preset-{type} .header-zone--{zone} CSS classes
                const zoneOverrides = this.currentData.zone_overrides?.[primaryZone] || {};
                const zoneStyles = this.buildZoneStyles(zoneOverrides);
                const fullWidth = zoneOverrides.full_width ? 'true' : 'false';

                // Map primary zone name to CSS class (e.g., "top-bar" -> "header-zone--top-bar")
                const zoneClass = `header-zone header-zone--${primaryZone}`;

                html += `
                    <div class="hf-primary-zone ${zoneClass}" data-primary-zone="${primaryZone}" data-full-width="${fullWidth}"${zoneStyles ? ` style="${zoneStyles}"` : ''}>
                        <button class="zone-config-btn" data-primary-zone="${primaryZone}" title="Configure ${primaryZone}">
                            <i class="fas fa-cog"></i>
                        </button>
                `;

                // Inject hamburger toggle at start of main-header zone (left position) for mobile preview
                if (this.builderType === 'header' && this.currentDevice === 'mobile' && primaryZone === 'main-header' && menuPosition === 'left' && !hamburgerInjected) {
                    html += `
                        <div class="hf-mobile-toggle-preview" style="display: flex; align-items: center; justify-content: center; width: 40px; height: 40px; flex-shrink: 0; color: inherit; font-size: 1.1rem;">
                            <i class="fas fa-bars"></i>
                        </div>
                    `;
                    hamburgerInjected = true;
                }
            }

            html += `
                <div class="hf-zone ${isEmpty ? 'empty' : ''}" data-zone="${zone}">
                    <span class="zone-label">${zone.replace('_', ' ').replace('-', ' ')}</span>
            `;

            if (isEmpty) {
                html += `
                    <div class="widget-drop-zone" data-zone="${zone}">
                        <i class="fas fa-plus-circle" title="Drop widgets here"></i>
                        <span>Drop widgets here</span>
                    </div>
                `;
            } else {
                // Render widgets in this zone
                zoneWidgets.forEach(widget => {
                    html += this.renderWidget(widget);
                });
            }

            html += `</div>`;
        });

        // Inject hamburger toggle at end of main-header zone (right position) for mobile preview
        if (this.builderType === 'header' && this.currentDevice === 'mobile' && !hamburgerInjected) {
            html += `
                <div class="hf-mobile-toggle-preview" style="display: flex; align-items: center; justify-content: center; width: 40px; height: 40px; flex-shrink: 0; color: inherit; font-size: 1.1rem;">
                    <i class="fas fa-bars"></i>
                </div>
            `;
        }

        // Close last primary zone
        if (currentPrimaryZone !== null) {
            html += `</div>`;
        }

        html += `</div>`;
        preview.innerHTML = html;

        // Lightweight: setup zone config buttons immediately (just a few click handlers)
        this.setupZoneConfigButtons();

        // Defer heavy DOM setup to after browser paints the preview
        requestAnimationFrame(() => {
            this.setupDropZones();
            this.fetchServerPreviews();
        });
    }

    /**
     * Fetch server-rendered previews for widgets that need dynamic data
     * (widgets with data-needs-server-preview="true")
     */
    async fetchServerPreviews() {
        const widgetsNeedingPreview = document.querySelectorAll('[data-needs-server-preview="true"]');

        for (const widgetEl of widgetsNeedingPreview) {
            const wrapper = widgetEl.closest('.widget-wrapper');
            if (!wrapper) continue;

            const placementId = wrapper.dataset.placementId;
            const widgetData = this.findWidgetByPlacementId(placementId);
            if (!widgetData) continue;

            try {
                const previewHtml = await this.fetchWidgetPreview(widgetData.widget_type, widgetData.config);
                const contentEl = wrapper.querySelector('.widget-content');
                if (contentEl) {
                    contentEl.innerHTML = previewHtml;
                }
            } catch (error) {
                console.error('Error fetching server preview for widget:', placementId, error);
            }
        }
    }

    /**
     * Find widget data by placement ID
     */
    findWidgetByPlacementId(placementId) {
        if (!this.currentData || !this.currentData.zones) return null;

        // Convert to string for comparison (dataset values are always strings)
        const idStr = String(placementId);

        for (const [zoneName, widgets] of Object.entries(this.currentData.zones)) {
            const widget = widgets.find(w => String(w.id) === idStr);
            if (widget) return widget;
        }
        return null;
    }

    getZonesFromLayouts(zoneLayouts) {
        /**
         * Converts zone_layouts structure to flat zone list
         * Example: {"top-bar": ["left", "right"], "main-header": ["left", "center", "right"]}
         * Returns: ["top-bar_left", "top-bar_right", "main-header_left", "main-header_center", "main-header_right"]
         * Filters zones based on current device visibility settings
         */
        const zones = [];
        for (const [primaryZone, subZones] of Object.entries(zoneLayouts)) {
            // Check if this primary zone is enabled
            const zoneConfig = this.currentData.zone_overrides?.[primaryZone];
            if (zoneConfig && zoneConfig.enabled === false) {
                continue; // Skip disabled zones
            }

            // Check device visibility
            if (zoneConfig && zoneConfig.visibility) {
                const isVisible = zoneConfig.visibility[this.currentDevice];
                if (isVisible === false) {
                    console.log(`Hiding zone ${primaryZone} on ${this.currentDevice}`);
                    continue; // Skip zones not visible on current device
                }
            }

            for (const subZone of subZones) {
                zones.push(`${primaryZone}_${subZone}`);
            }
        }
        return zones;
    }

    getPrimaryZonesFromLayout() {
        // Use zone_layouts if available
        if (this.currentData.zone_layouts) {
            return Object.keys(this.currentData.zone_layouts);
        }

        // FALLBACK: Return list of primary zones based on layout
        if (this.builderType === 'header') {
            const layouts = {
                'classic': ['main-header'],
                'boutique': ['top-bar', 'main-header', 'bottom-bar'],
                'minimal': ['main-header'],
                'mega': ['top-bar', 'main-header', 'mega-menu-bar'],
                'promotional': ['top-bar', 'main-header', 'bottom-bar'],
                'split': ['top-bar', 'main-header'],
                'custom': ['main-header'],
            };
            return layouts[this.currentData.layout_type] || ['main-header'];
        } else {
            return ['footer-primary'];
        }
    }

    // Theme and brand CSS injection is handled by hf-css-loader.js with proper scoping

    buildZoneStyles(zoneOverrides) {
        /**
         * Builds inline styles from zone overrides only.
         * Only outputs styles for properties that merchant has explicitly customized.
         * Base styling comes from .header-preset-{type} .header-zone--{zone} CSS classes.
         *
         * @param {Object} zoneOverrides - Only the properties merchant has overridden
         * @returns {string} Inline style string for overrides only
         */
        if (!zoneOverrides || Object.keys(zoneOverrides).length === 0) {
            return '';
        }

        const styles = [];
        const zoneConfig = zoneOverrides; // Alias for compatibility with existing code

        // Background color/image
        if (zoneConfig.background) {
            if (zoneConfig.background.type === 'theme') {
                // Theme variable reference
                styles.push(`background: ${zoneConfig.background.value}`);
            } else if (zoneConfig.background.type === 'color') {
                // Solid color
                styles.push(`background-color: ${zoneConfig.background.value}`);
            } else if (zoneConfig.background.type === 'gradient') {
                // Gradient
                styles.push(`background: ${zoneConfig.background.value}`);
            } else if (zoneConfig.background.type === 'image') {
                // Background image
                styles.push(`background-image: url(${zoneConfig.background.value})`);
                styles.push(`background-size: cover`);
                styles.push(`background-position: center`);
            }
        }

        // Text color
        if (zoneConfig.text_color) {
            if (zoneConfig.text_color.type === 'theme') {
                styles.push(`color: ${zoneConfig.text_color.value}`);
            } else if (zoneConfig.text_color.type === 'color') {
                styles.push(`color: ${zoneConfig.text_color.value}`);
            }
        }

        // Height
        if (zoneConfig.height) {
            styles.push(`min-height: ${zoneConfig.height}px`);
        }

        // Sticky height (stored as CSS variable for scroll behavior)
        if (zoneConfig.sticky && zoneConfig.sticky_height) {
            styles.push(`--sticky-height: ${zoneConfig.sticky_height}px`);
        }

        // Collapse height (stored as CSS variable for scroll behavior)
        if (zoneConfig.collapse_on_scroll && zoneConfig.collapse_height !== undefined) {
            styles.push(`--collapse-height: ${zoneConfig.collapse_height}px`);
        }

        // Padding from spacing
        if (zoneConfig.spacing?.padding) {
            styles.push(`padding: ${zoneConfig.spacing.padding}`);
        }

        // Margin from spacing
        if (zoneConfig.spacing?.margin) {
            styles.push(`margin: ${zoneConfig.spacing.margin}`);
        }

        // Border top
        if (zoneConfig.border_top) {
            const borderSize = zoneConfig.border_top.size || 0;
            const borderColor = zoneConfig.border_top.color || 'var(--theme-color-border)';
            if (borderSize > 0) {
                styles.push(`border-top: ${borderSize}px solid ${borderColor}`);
            }
        }

        // Border bottom
        if (zoneConfig.border_bottom) {
            const borderSize = zoneConfig.border_bottom.size || 0;
            const borderColor = zoneConfig.border_bottom.color || 'var(--theme-color-border)';
            if (borderSize > 0) {
                styles.push(`border-bottom: ${borderSize}px solid ${borderColor}`);
            }
        }

        // Full width
        if (zoneConfig.full_width) {
            styles.push(`width: 100%`);
        }

        return styles.join('; ');
    }

    setupZoneConfigButtons() {
        const configButtons = document.querySelectorAll('.zone-config-btn');
        configButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const primaryZone = btn.dataset.primaryZone;
                this.showZoneConfig(primaryZone);
            });
        });
    }

    getHeaderZones(layoutType) {
        // Define zone layouts matching the model's get_default_zone_layouts()
        const zoneLayouts = {
            'classic': {
                "top-bar": ["left", "right"],
                "main-header": ["left", "center", "right"]
            },
            'boutique': {
                "top-bar": ["full"],
                "main-header": ["center"],
                "bottom-bar": ["full"]
            },
            'minimal': {
                "main-header": ["left", "right"]
            },
            'mega': {
                "top-bar": ["left", "right"],
                "main-header": ["left", "center", "right"],
                "mega-menu-bar": ["full"]
            },
            'promotional': {
                "top-bar": ["full"],
                "main-header": ["left", "center", "right"],
                "bottom-bar": ["full"]
            },
            'split': {
                "top-bar": ["left", "right"],
                "main-header": ["left", "center", "right"]
            },
            'custom': {
                "main-header": ["left", "center", "right"]
            },
        };

        // Get layout structure or default to classic
        const layout = zoneLayouts[layoutType] || zoneLayouts['classic'];

        // Flatten to zone IDs (e.g., "main-header_left")
        return this.getZonesFromLayouts(layout);
    }

    getFooterZones(layoutType, columnCount = 4) {
        if (layoutType === 'simple') {
            return ['single'];
        } else if (layoutType === 'columns') {
            const zones = [];
            for (let i = 1; i <= columnCount; i++) {
                zones.push(`col-${i}`);
            }
            return zones;
        } else if (layoutType === 'stacked') {
            return ['section-1', 'section-2', 'section-3', 'bottom-bar'];
        }
        return ['col-1', 'col-2', 'col-3', 'col-4'];
    }

    renderWidget(widget) {
        // Use fallback for initial render (fast, synchronous)
        // Server-rendered preview is fetched later for property updates
        const widgetHTML = this.renderWidgetPreviewFallback(widget);

        return `
            <div class="widget-wrapper" data-placement-id="${widget.id}">
                <span class="widget-type-label">${widget.widget_type}</span>
                <div class="widget-controls">
                    <button class="control-btn edit-btn" title="Edit">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="control-btn move-btn" title="Move">
                        <i class="fas fa-arrows-alt"></i>
                    </button>
                    <button class="control-btn delete-btn" title="Delete">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
                <div class="widget-content">
                    ${widgetHTML}
                </div>
            </div>
        `;
    }

    /**
     * Fallback client-side widget preview (used when server preview fails)
     */
    renderWidgetPreviewFallback(widget) {
        const config = widget.config || {};
        const isMobile = this.currentDevice === 'mobile';

        switch (widget.widget_type) {
            case 'logo':
                // Check if using site logo (default: true)
                const useSiteLogo = config.use_site_logo !== false;
                const siteLogoAvailable = this.siteLogoData?.has_logo && this.siteLogoData?.logo_url;

                // Priority: 1. Site logo (if enabled and available), 2. Custom logo_url, 3. Fallback text
                let logoContent;
                if (useSiteLogo && siteLogoAvailable) {
                    logoContent = `<img src="${this.siteLogoData.logo_url}" alt="${config.alt_text || 'Logo'}" class="logo-image">`;
                } else if (config.logo_url) {
                    logoContent = `<img src="${config.logo_url}" alt="${config.alt_text || 'Logo'}" class="logo-image">`;
                } else {
                    logoContent = `<span class="logo-text">${config.text || 'Logo'}</span>`;
                }

                return `
                    <div class="widget-logo">
                        ${logoContent}
                    </div>
                `;

            case 'menu':
                if (isMobile) {
                    // On mobile, nav menu is hidden (hamburger replaces it)
                    return `
                        <nav class="widget-menu" style="opacity: 0.4; font-size: 11px; font-style: italic; text-align: center;">
                            <span>Menu (via hamburger)</span>
                        </nav>
                    `;
                }
                return `
                    <nav class="widget-menu">
                        <ul class="menu-list menu-horizontal">
                            <li class="menu-item"><a href="#" class="menu-link">Home</a></li>
                            <li class="menu-item"><a href="#" class="menu-link">Shop</a></li>
                            <li class="menu-item"><a href="#" class="menu-link">About</a></li>
                            <li class="menu-item"><a href="#" class="menu-link">Contact</a></li>
                        </ul>
                    </nav>
                `;

            case 'search':
                if (isMobile) {
                    // On mobile, search shows as icon-only trigger
                    return `
                        <div class="widget-search">
                            <button type="button" class="search-mobile-trigger" style="background: none; border: none; padding: 8px; cursor: pointer; color: inherit; font-size: 1.1rem;">
                                <i class="fas fa-search"></i>
                            </button>
                        </div>
                    `;
                }
                return `
                    <div class="widget-search">
                        <form class="search-form">
                            <div class="search-container">
                                <div class="search-input-wrapper">
                                    <input type="search" placeholder="${config.placeholder || 'Search...'}" class="search-input">
                                    <button type="submit" class="search-button">
                                        <i class="fas fa-search"></i>
                                    </button>
                                </div>
                            </div>
                        </form>
                    </div>
                `;

            case 'cart':
                return `
                    <div class="widget-cart">
                        <a href="#" class="cart-link">
                            <div class="cart-icon-wrapper">
                                <i class="fas fa-shopping-cart"></i>
                                ${config.show_count !== false ?
                                    '<span class="cart-count">0</span>' :
                                    ''
                                }
                            </div>
                            ${!isMobile && config.show_total !== false ?
                                '<span class="cart-text">Cart</span>' :
                                ''
                            }
                        </a>
                    </div>
                `;

            case 'account':
                return `
                    <div class="widget-account">
                        <div class="account-links">
                            <a href="#" class="account-link">
                                <i class="fas fa-user"></i>
                                ${!isMobile ? '<span class="account-name">Account</span>' : ''}
                            </a>
                        </div>
                    </div>
                `;

            case 'language':
                if (isMobile) {
                    // On mobile, show globe icon + language code (matches frontend mobile behavior)
                    return `
                        <div class="widget-language">
                            <button type="button" class="language-mobile-trigger" style="display: inline-flex; align-items: center; gap: 4px; background: none; border: none; padding: 8px; cursor: pointer; color: inherit; font-size: 0.85rem;">
                                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                    <circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/>
                                    <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
                                </svg>
                                <span style="font-weight: 500;">EN</span>
                            </button>
                        </div>
                    `;
                }
                return `
                    <div class="widget-language">
                        <select class="language-select">
                            <option>EN</option>
                            <option>ES</option>
                            <option>FR</option>
                        </select>
                    </div>
                `;

            case 'currency':
                if (isMobile) {
                    // On mobile, show currency symbol only (compact mode)
                    return `
                        <div class="widget-currency">
                            <button type="button" class="currency-button" style="display: inline-flex; align-items: center; gap: 4px; background: none; border: none; padding: 8px; cursor: pointer; color: inherit; font-size: 0.85rem;">
                                <span class="currency-symbol">$</span>
                            </button>
                        </div>
                    `;
                }
                return `
                    <div class="widget-currency">
                        <button type="button" class="currency-button" style="display: inline-flex; align-items: center; gap: 6px; background: none; border: 1px solid currentColor; border-radius: 4px; padding: 4px 10px; cursor: pointer; color: inherit; font-size: 0.85rem; opacity: 0.8;">
                            <span class="currency-symbol">$</span>
                            <span class="currency-code">USD</span>
                        </button>
                    </div>
                `;

            case 'social':
                return `
                    <div class="widget-social">
                        <a href="#" class="social-link"><i class="fab fa-facebook"></i></a>
                        <a href="#" class="social-link"><i class="fab fa-twitter"></i></a>
                        <a href="#" class="social-link"><i class="fab fa-instagram"></i></a>
                    </div>
                `;

            case 'text':
                return `
                    <div class="widget-text">
                        <p>${config.text || 'Sample text'}</p>
                    </div>
                `;

            case 'links':
                return `
                    <div class="widget-links">
                        <ul class="links-list">
                            <li><a href="#">Link 1</a></li>
                            <li><a href="#">Link 2</a></li>
                            <li><a href="#">Link 3</a></li>
                        </ul>
                    </div>
                `;

            case 'newsletter':
                return `
                    <div class="widget-newsletter">
                        <form class="newsletter-form">
                            <input type="email" placeholder="Your email" class="newsletter-input">
                            <button type="submit" class="newsletter-btn">Subscribe</button>
                        </form>
                    </div>
                `;

            case 'contact':
                return `
                    <div class="widget-contact">
                        <i class="fas fa-phone"></i>
                        <span>${config.phone || '+1 (555) 123-4567'}</span>
                    </div>
                `;

            case 'site_variable':
                // Map variable names to readable labels for fallback
                const variableLabels = {
                    'site_name': 'Store Name',
                    'site_tagline': 'Tagline',
                    'site_url': 'Website URL',
                    'admin_email': 'Admin Email',
                    'support_email': 'Support Email',
                    'phone_number': 'Phone Number',
                    'full_address': 'Full Address',
                    'address_line_1': 'Street Address',
                    'city': 'City',
                    'state_province': 'State/Province',
                    'postal_code': 'Postal Code',
                    'country': 'Country',
                    'facebook_url': 'Facebook URL',
                    'twitter_url': 'Twitter/X URL',
                    'instagram_url': 'Instagram URL',
                    'linkedin_url': 'LinkedIn URL',
                    'default_currency': 'Currency Code',
                    'default_language': 'Language Code'
                };
                const variable = config.variable || 'site_name';
                const varLabel = variableLabels[variable] || variable;

                // Build inline styles from config
                let siteVarStyles = '';
                if (config.text_color) {
                    siteVarStyles += `color: ${config.text_color};`;
                }
                if (config.typography) {
                    try {
                        const typo = typeof config.typography === 'string' ? JSON.parse(config.typography) : config.typography;
                        if (typo.fontFamily) siteVarStyles += `font-family: ${typo.fontFamily};`;
                        if (typo.fontSize) siteVarStyles += `font-size: ${typo.fontSize};`;
                        if (typo.fontWeight) siteVarStyles += `font-weight: ${typo.fontWeight};`;
                        if (typo.lineHeight) siteVarStyles += `line-height: ${typo.lineHeight};`;
                        if (typo.letterSpacing) siteVarStyles += `letter-spacing: ${typo.letterSpacing};`;
                    } catch (e) {}
                }

                // Show icon if configured
                let iconBefore = '';
                let iconAfter = '';
                if (config.show_icon && config.icon) {
                    const iconHtml = `<i class="${config.icon} site-variable-icon"></i>`;
                    if (config.icon_position === 'after') {
                        iconAfter = iconHtml;
                    } else {
                        iconBefore = iconHtml;
                    }
                }

                // For fallback, show loading indicator - actual value loaded via server preview
                return `
                    <div class="widget-site-variable" data-variable="${variable}" data-needs-server-preview="true" style="${siteVarStyles}">
                        ${iconBefore}
                        <span class="site-variable-text site-variable-loading">${varLabel}...</span>
                        ${iconAfter}
                    </div>
                `;

            default:
                return `
                    <div class="widget-${widget.widget_type}">
                        <strong>${widget.widget_name || widget.widget_type}</strong>
                    </div>
                `;
        }
    }

    setupDropZones() {
        const dropZones = document.querySelectorAll('.hf-zone');

        dropZones.forEach(zone => {
            zone.addEventListener('dragover', (e) => {
                // Skip visual feedback during Sortable.js reordering
                if (document.body.classList.contains('is-reordering-widget')) {
                    return;
                }
                e.preventDefault();
                e.dataTransfer.dropEffect = 'copy';
                zone.classList.add('drag-over');
            });

            zone.addEventListener('dragleave', (e) => {
                zone.classList.remove('drag-over');
            });

            zone.addEventListener('drop', (e) => {
                e.preventDefault();
                e.stopPropagation(); // Prevent event bubbling
                zone.classList.remove('drag-over');

                // Skip if this is a Sortable.js reordering operation
                if (document.body.classList.contains('is-reordering-widget')) {
                    return;
                }

                const data = e.dataTransfer.getData('text/plain');
                if (!data) return;

                // Validate data looks like JSON before parsing
                if (!data.trim().startsWith('{')) {
                    return;
                }

                try {
                    const widgetData = JSON.parse(data);

                    // Validate this is widget data from sidebar, not Sortable.js
                    if (!widgetData.widgetId) {
                        return;
                    }

                    const zoneName = zone.dataset.zone;
                    this.addWidgetToZone(widgetData, zoneName);
                } catch (error) {
                    console.error('Error processing drop:', error);
                }
            });
        });

        // Setup widget control buttons
        this.setupWidgetControls();

        // Create insert zones between existing widgets for precise positioning
        this.createWidgetInsertZones();

        // Initialize Sortable.js for widget reordering via move button
        this.setupZoneSortables();
    }

    setupWidgetControls() {
        // Widget wrapper click - select widget and show properties
        document.querySelectorAll('.widget-wrapper').forEach(wrapper => {
            wrapper.addEventListener('click', (e) => {
                // Don't trigger if clicking on control buttons
                if (e.target.closest('.widget-controls')) return;

                e.stopPropagation();
                const placementId = wrapper.dataset.placementId;
                this.editWidget(placementId);
            });
        });

        // Edit buttons
        document.querySelectorAll('.edit-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const wrapper = btn.closest('.widget-wrapper');
                const placementId = wrapper.dataset.placementId;
                this.editWidget(placementId);
            });
        });

        // Delete buttons
        document.querySelectorAll('.delete-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.stopPropagation();
                const wrapper = btn.closest('.widget-wrapper');
                const placementId = wrapper.dataset.placementId;
                this.deleteWidget(placementId);
            });
        });
    }

    /**
     * Create insert zones between existing widgets for precise drop positioning.
     * These zones are hidden by default and only appear when dragging a widget.
     */
    createWidgetInsertZones() {
        // Only create insert zones for non-empty zones
        const zones = document.querySelectorAll('.hf-zone:not(.empty)');

        zones.forEach(zone => {
            const widgets = zone.querySelectorAll('.widget-wrapper');
            if (widgets.length === 0) return;

            // Insert zone BEFORE first widget (position 0)
            this.createInsertZone(zone, 0, widgets[0], false);

            // Insert zone AFTER each widget
            widgets.forEach((widget, index) => {
                this.createInsertZone(zone, index + 1, widget, true);
            });
        });
    }

    /**
     * Create a single insert zone element with drop handlers
     */
    createInsertZone(zone, position, referenceWidget, insertAfter) {
        const insertZone = document.createElement('div');
        insertZone.className = 'hf-widget-insert-zone';
        insertZone.dataset.zone = zone.dataset.zone;
        insertZone.dataset.position = position;
        insertZone.innerHTML = '<span class="insert-indicator">Drop here</span>';

        // Setup drop handlers - only respond to new widget drops, not Sortable.js reordering
        insertZone.addEventListener('dragover', (e) => {
            // Skip if we're reordering existing widgets
            if (document.body.classList.contains('is-reordering-widget')) {
                return;
            }
            e.preventDefault();
            e.dataTransfer.dropEffect = 'copy';
            insertZone.classList.add('drag-over');
        });

        insertZone.addEventListener('dragleave', () => {
            insertZone.classList.remove('drag-over');
        });

        insertZone.addEventListener('drop', (e) => {
            e.preventDefault();
            e.stopPropagation();
            insertZone.classList.remove('drag-over');

            // Skip if we're reordering existing widgets (Sortable.js handles that)
            if (document.body.classList.contains('is-reordering-widget')) {
                return;
            }

            const data = e.dataTransfer.getData('text/plain');
            if (!data) return;

            // Validate data looks like JSON before parsing (must start with {)
            if (!data.trim().startsWith('{')) {
                console.log('Insert zone: ignoring non-JSON drop data');
                return;
            }

            try {
                const widgetData = JSON.parse(data);
                // Validate it has the expected structure
                if (!widgetData.widgetId) {
                    console.log('Insert zone: drop data missing widgetId');
                    return;
                }
                const zoneName = insertZone.dataset.zone;
                const pos = parseInt(insertZone.dataset.position);
                this.addWidgetToZoneAtPosition(widgetData, zoneName, pos);
            } catch (error) {
                console.error('Error processing drop on insert zone:', error);
            }
        });

        // Insert into DOM
        if (insertAfter) {
            referenceWidget.insertAdjacentElement('afterend', insertZone);
        } else {
            zone.insertBefore(insertZone, referenceWidget);
        }
    }

    /**
     * Add a widget to a zone at a specific position
     */
    async addWidgetToZoneAtPosition(widgetData, zoneName, position) {
        console.log('Adding widget to zone at position:', widgetData, zoneName, position);

        try {
            const response = await fetch('/api/hf-builder/widget-placement/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.config.csrfToken,
                },
                body: JSON.stringify({
                    widget_id: widgetData.widgetId,
                    zone: zoneName,
                    order: position,
                    [this.builderType + '_id']: this.templateId,
                })
            });

            if (!response.ok) {
                throw new Error('Failed to add widget');
            }

            await this.loadTemplate();
        } catch (error) {
            console.error('Error adding widget at position:', error);
            this.showError('Failed to add widget');
        }
    }

    /**
     * Initialize Sortable.js for widget reordering within zones
     */
    setupZoneSortables() {
        // Clean up existing sortables
        if (this.zoneSortables) {
            this.zoneSortables.forEach(s => s.destroy());
        }
        this.zoneSortables = [];

        // Check if Sortable is available
        if (typeof Sortable === 'undefined') {
            console.warn('Sortable.js not loaded - widget reordering disabled');
            return;
        }

        // Initialize Sortable on ALL zones (including empty) so widgets can be moved between them
        const zones = document.querySelectorAll('.hf-zone');

        zones.forEach(zone => {
            const sortable = new Sortable(zone, {
                animation: 150,
                group: 'hf-widgets',  // Allow moving between zones
                handle: '.move-btn',  // Only drag via move button
                ghostClass: 'hf-widget-ghost',
                chosenClass: 'hf-widget-chosen',
                dragClass: 'hf-widget-drag',
                filter: '.hf-widget-insert-zone, .zone-label, .widget-drop-zone',  // Don't drag these
                draggable: '.widget-wrapper',

                onStart: (evt) => {
                    document.body.classList.add('is-reordering-widget');
                    evt.item.classList.add('is-moving');
                },

                onEnd: async (evt) => {
                    document.body.classList.remove('is-reordering-widget');
                    evt.item.classList.remove('is-moving');

                    const fromZone = evt.from.dataset.zone;
                    const toZone = evt.to.dataset.zone;
                    const placementId = parseInt(evt.item.dataset.placementId);

                    // Check if widget moved to a different zone
                    if (fromZone !== toZone) {
                        // Widget moved between zones
                        // Get all widgets in the destination zone (after the move)
                        const toZoneEl = evt.to;
                        const widgets = toZoneEl.querySelectorAll('.widget-wrapper');

                        // Calculate the correct widget index (not DOM index)
                        let newOrder = 0;
                        Array.from(widgets).forEach((w, idx) => {
                            if (w === evt.item) {
                                newOrder = idx;
                            }
                        });

                        // Update zone and order for the moved widget
                        await this.moveWidgetToZone(placementId, toZone, newOrder);
                    } else {
                        // Widget reordered within same zone
                        const zoneEl = evt.to;
                        const widgets = zoneEl.querySelectorAll('.widget-wrapper');
                        const placements = Array.from(widgets).map((w, idx) => ({
                            id: parseInt(w.dataset.placementId),
                            order: idx
                        }));
                        await this.updateWidgetOrder(placements);
                    }
                }
            });

            this.zoneSortables.push(sortable);
        });
    }

    /**
     * Update widget order via API after drag-and-drop reordering
     * @param {Array} placements - Array of {id, order} objects matching API format
     */
    async updateWidgetOrder(placements) {
        try {
            const response = await fetch('/api/hf-builder/widget-placement/reorder/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.config.csrfToken,
                },
                body: JSON.stringify({
                    placements: placements
                })
            });

            if (!response.ok) {
                throw new Error('Failed to reorder widgets');
            }

            // Reload to sync state
            await this.loadTemplate();
        } catch (error) {
            console.error('Error reordering widgets:', error);
            this.showError('Failed to reorder widgets');
        }
    }

    /**
     * Move a widget to a different zone
     * @param {number} placementId - The widget placement ID
     * @param {string} newZone - The target zone name
     * @param {number} newOrder - The new order position in the target zone
     */
    async moveWidgetToZone(placementId, newZone, newOrder) {
        try {
            const response = await fetch(`/api/hf-builder/widget-placement/${placementId}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.config.csrfToken,
                },
                body: JSON.stringify({
                    zone: newZone,
                    order: newOrder
                })
            });

            if (!response.ok) {
                throw new Error('Failed to move widget');
            }

            // Reload to sync state
            await this.loadTemplate();
        } catch (error) {
            console.error('Error moving widget:', error);
            this.showError('Failed to move widget');
        }
    }

    editWidget(placementId) {
        // Find the widget data
        let widgetData = null;
        for (const zone in this.currentData.zones) {
            const widget = this.currentData.zones[zone].find(w => w.id == placementId);
            if (widget) {
                widgetData = widget;
                break;
            }
        }

        if (!widgetData) return;

        // Show properties panel
        this.showPropertiesPanel(widgetData);
    }

    async showPropertiesPanel(widgetData) {
        // Switch to the widget properties tab
        const widgetTabBtn = document.querySelector('.admin-tab-btn[data-tab="widget-props"]');
        if (widgetTabBtn) {
            widgetTabBtn.click();
        }

        const panel = document.getElementById('properties-panel');
        if (!panel) return;

        // Mark the selected widget visually
        document.querySelectorAll('.widget-wrapper').forEach(w => w.classList.remove('selected'));
        const selectedWrapper = document.querySelector(`.widget-wrapper[data-placement-id="${widgetData.id}"]`);
        if (selectedWrapper) {
            selectedWrapper.classList.add('selected');
        }

        this.selectedWidget = widgetData;

        // Initialize property renderer if not already done
        if (!this.propertyRenderer) {
            this.propertyRenderer = new WidgetPropertyRenderer(this);
        }

        // Load dynamic options (menus, etc.) for select fields
        await this.propertyRenderer.loadDynamicOptions();

        // Render the properties panel using the new renderer
        const html = this.propertyRenderer.render(widgetData);
        panel.innerHTML = html;

        // Setup event listeners for all controls
        this.propertyRenderer.setupEventListeners();

        // Setup save/cancel handlers
        document.getElementById('save-widget-config')?.addEventListener('click', () => {
            this.saveWidgetConfig(widgetData.id);
        });

        document.getElementById('cancel-widget-config')?.addEventListener('click', () => {
            this.clearWidgetSelection();
        });
    }

    clearWidgetSelection() {
        // Deselect widgets visually
        document.querySelectorAll('.widget-wrapper').forEach(w => w.classList.remove('selected'));
        this.selectedWidget = null;

        // Reset the properties panel
        const panel = document.getElementById('properties-panel');
        if (panel) {
            panel.innerHTML = `
                <div class="hf-properties-empty">
                    <i class="fas fa-hand-pointer"></i>
                    <p>Select a widget to edit its properties</p>
                </div>
            `;
        }
    }

    async saveWidgetConfig(placementId) {
        try {
            let config;

            // Use property renderer to collect values if available
            if (this.propertyRenderer) {
                config = this.propertyRenderer.collectFormValues();
                if (config === null) {
                    // collectFormValues returns null on JSON parse error
                    this.showError('Invalid JSON in configuration');
                    return;
                }
            } else {
                // Fallback to JSON textarea
                const configTextarea = document.getElementById('widget-config-json');
                if (!configTextarea) return;
                config = JSON.parse(configTextarea.value);
            }

            // Collect device visibility settings
            const savePayload = { override_config: config };
            const visDesktop = document.getElementById('vis-desktop');
            const visTablet = document.getElementById('vis-tablet');
            const visMobile = document.getElementById('vis-mobile');
            if (visDesktop) savePayload.show_on_desktop = visDesktop.checked;
            if (visTablet) savePayload.show_on_tablet = visTablet.checked;
            if (visMobile) savePayload.show_on_mobile = visMobile.checked;

            const response = await fetch(`/api/hf-builder/widget-placement/${placementId}/`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.config.csrfToken,
                },
                body: JSON.stringify(savePayload)
            });

            if (!response.ok) {
                throw new Error('Failed to update widget configuration');
            }

            // Reload template to refresh preview
            await this.loadTemplate();

            // Show success feedback
            this.clearWidgetSelection();

        } catch (error) {
            console.error('Error saving widget config:', error);
            this.showError('Failed to save widget configuration: ' + error.message);
        }
    }

    async deleteWidget(placementId) {
        if (!await AdminModal.confirm({
            message: this.config.translations.confirmDelete || 'Are you sure you want to remove this widget?',
            danger: true,
            confirmText: 'Remove'
        })) {
            return;
        }

        try {
            const response = await fetch(`/api/hf-builder/widget-placement/${placementId}/`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.config.csrfToken,
                }
            });

            if (!response.ok) {
                throw new Error('Failed to delete widget');
            }

            // Reload template
            await this.loadTemplate();

        } catch (error) {
            console.error('Error deleting widget:', error);
            this.showError('Failed to delete widget');
        }
    }

    async addWidgetToZone(widgetData, zoneName) {
        console.log('Adding widget to zone:', widgetData, zoneName);

        try {
            // Call API to create widget placement
            const response = await fetch('/api/hf-builder/widget-placement/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.config.csrfToken,
                },
                body: JSON.stringify({
                    widget_id: widgetData.widgetId,
                    zone: zoneName,
                    order: 0,
                    [this.builderType + '_id']: this.templateId,
                })
            });

            if (!response.ok) {
                throw new Error('Failed to add widget');
            }

            const result = await response.json();
            console.log('Widget added:', result);

            // Reload template data and re-render
            await this.loadTemplate();

        } catch (error) {
            console.error('Error adding widget:', error);
            this.showError('Failed to add widget');
        }
    }

    /**
     * Save current state as draft (not live)
     */
    async saveDraft() {
        const saveDraftBtn = document.getElementById('save-draft-btn');
        if (!saveDraftBtn) return;

        const originalText = saveDraftBtn.innerHTML;
        saveDraftBtn.innerHTML = `<i class="fas fa-spinner fa-spin"></i> Saving...`;
        saveDraftBtn.disabled = true;

        try {
            const response = await fetch(this.apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.config.csrfToken,
                },
                body: JSON.stringify(this.currentData)
            });

            if (!response.ok) {
                throw new Error('Save failed');
            }

            const result = await response.json();

            // Update status indicator to show draft
            this.updateStatusIndicator('draft');

            saveDraftBtn.innerHTML = `<i class="fas fa-check"></i> Saved!`;

            setTimeout(() => {
                saveDraftBtn.innerHTML = originalText;
                saveDraftBtn.disabled = false;
            }, 2000);

        } catch (error) {
            console.error('Save error:', error);
            this.showError('Failed to save draft');
            saveDraftBtn.innerHTML = originalText;
            saveDraftBtn.disabled = false;
        }
    }

    /**
     * Publish current draft to make it live
     */
    async publish() {
        const publishBtn = document.getElementById('publish-btn');
        if (!publishBtn) return;

        const originalText = publishBtn.innerHTML;
        publishBtn.innerHTML = `<i class="fas fa-spinner fa-spin"></i> Publishing...`;
        publishBtn.disabled = true;

        try {
            // First save the current draft
            await this.saveDraftSilent();

            // Then publish
            const response = await fetch(`${this.apiUrl}publish/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.config.csrfToken,
                }
            });

            if (!response.ok) {
                throw new Error('Publish failed');
            }

            const result = await response.json();

            // Update status indicator to show live
            this.updateStatusIndicator('published');

            publishBtn.innerHTML = `<i class="fas fa-check"></i> Published!`;

            setTimeout(() => {
                publishBtn.innerHTML = originalText;
                publishBtn.disabled = false;
            }, 2000);

        } catch (error) {
            console.error('Publish error:', error);
            this.showError('Failed to publish');
            publishBtn.innerHTML = originalText;
            publishBtn.disabled = false;
        }
    }

    /**
     * Silent draft save (no UI feedback) - used before publish
     */
    async saveDraftSilent() {
        const response = await fetch(this.apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.config.csrfToken,
            },
            body: JSON.stringify(this.currentData)
        });

        if (!response.ok) {
            throw new Error('Save failed');
        }

        return response.json();
    }

    /**
     * Discard draft changes and revert to published state
     */
    async discardDraft() {
        // Confirm with user
        if (!await AdminModal.confirm({
            message: 'Discard all unpublished changes and revert to the live version?',
            danger: true,
            confirmText: 'Discard'
        })) {
            return;
        }

        const discardBtn = document.getElementById('discard-btn');
        if (!discardBtn) return;

        const originalText = discardBtn.innerHTML;
        discardBtn.innerHTML = `<i class="fas fa-spinner fa-spin"></i> Discarding...`;
        discardBtn.disabled = true;

        try {
            const response = await fetch(`${this.apiUrl}discard/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.config.csrfToken,
                }
            });

            if (!response.ok) {
                throw new Error('Discard failed');
            }

            const result = await response.json();

            // Reload the template data from server
            await this.loadTemplate();
            this.renderCanvas();

            // Update status indicator to show live
            this.updateStatusIndicator('published');

            discardBtn.innerHTML = originalText;
            discardBtn.disabled = true; // Keep disabled since no changes now

        } catch (error) {
            console.error('Discard error:', error);
            this.showError('Failed to discard changes');
            discardBtn.innerHTML = originalText;
            discardBtn.disabled = false;
        }
    }

    /**
     * Update the status indicator in the toolbar
     * @param {string} status - 'draft' or 'published'
     */
    updateStatusIndicator(status) {
        const badge = document.getElementById('status-badge');
        const discardBtn = document.getElementById('discard-btn');

        if (!badge) return;

        if (status === 'draft') {
            badge.className = 'hfb-status-badge hfb-status-draft';
            badge.innerHTML = `
                <i class="fas fa-pencil-alt"></i>
                <span class="status-text">Draft (not live)</span>
            `;
            // Enable discard button
            if (discardBtn) {
                discardBtn.disabled = false;
            }
        } else {
            badge.className = 'hfb-status-badge hfb-status-published';
            badge.innerHTML = `
                <i class="fas fa-check-circle"></i>
                <span class="status-text">Live</span>
            `;
            // Disable discard button
            if (discardBtn) {
                discardBtn.disabled = true;
            }
        }
    }

    /**
     * Initialize status indicator from loaded data
     */
    initializeStatusIndicator() {
        const hasUnpublishedChanges = this.currentData?.has_unpublished_changes;
        this.updateStatusIndicator(hasUnpublishedChanges ? 'draft' : 'published');
    }

    // Legacy method for backwards compatibility
    async saveTemplate() {
        return this.saveDraft();
    }

    async openPresetGallery() {
        const modal = document.getElementById('preset-modal');
        if (!modal) return;

        modal.classList.remove('hidden');

        try {
            const response = await fetch(this.config.presetGalleryUrl);
            const data = await response.json();

            this.renderPresets(data.presets);
        } catch (error) {
            console.error('Error loading presets:', error);
        }
    }

    closePresetGallery() {
        const modal = document.getElementById('preset-modal');
        if (modal) {
            modal.classList.add('hidden');
        }
    }

    renderPresets(presets) {
        const grid = document.getElementById('preset-grid');
        if (!grid) return;

        if (!presets || presets.length === 0) {
            grid.innerHTML = `<p style="text-align: center; color: #6b7280;">${this.config.translations.noPresets}</p>`;
            return;
        }

        grid.innerHTML = presets.map(preset => `
            <div class="preset-card" data-preset-id="${preset.id}">
                <div class="preset-preview">
                    ${preset.preview_image ?
                        `<img src="${preset.preview_image}" alt="${preset.name}">` :
                        '<i class="fas fa-image"></i>'
                    }
                </div>
                <div class="preset-info">
                    <div class="preset-name">${preset.name}</div>
                    <div class="preset-description">${preset.description || ''}</div>
                    ${preset.category ?
                        `<span class="preset-category-badge">${preset.category}</span>` :
                        ''
                    }
                </div>
            </div>
        `).join('');

        // Add click handlers
        grid.querySelectorAll('.preset-card').forEach(card => {
            card.addEventListener('click', () => {
                const presetId = card.dataset.presetId;
                this.clonePreset(presetId);
            });
        });
    }

    async clonePreset(presetId) {
        console.log('Cloning preset:', presetId);

        try {
            // Show loading state
            const saveBtn = document.getElementById('save-btn');
            if (saveBtn) {
                saveBtn.innerHTML = `<i class="fas fa-spinner fa-spin"></i> ${this.config.translations.loading || 'Loading...'}`;
                saveBtn.disabled = true;
            }

            // Call clone API
            const cloneUrl = `/api/hf-builder/presets/${this.builderType}/${presetId}/clone/`;
            const response = await fetch(cloneUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.config.csrfToken,
                },
                body: JSON.stringify({
                    name: `My ${this.builderType.charAt(0).toUpperCase() + this.builderType.slice(1)}`
                })
            });

            const result = await response.json();

            if (!response.ok) {
                console.error('Clone error response:', result);
                throw new Error(result.error || 'Failed to clone preset');
            }

            console.log('Preset cloned:', result);

            // Close modal
            this.closePresetGallery();

            // Redirect to the new header/footer builder
            const newUrl = `/en/theme/${this.builderType}/${result.id}/builder/`;
            window.location.href = newUrl;

        } catch (error) {
            console.error('Error cloning preset:', error);
            this.showError('Failed to clone preset. Please try again.');

            // Restore save button
            const saveBtn = document.getElementById('save-btn');
            if (saveBtn) {
                saveBtn.innerHTML = `<i class="fas fa-save"></i> ${this.config.translations.save || 'Save'}`;
                saveBtn.disabled = false;
            }
        }
    }

    filterWidgets(searchTerm) {
        const cards = document.querySelectorAll('.widget-card');
        const term = searchTerm.toLowerCase();

        cards.forEach(card => {
            const name = card.querySelector('.widget-name').textContent.toLowerCase();
            const type = card.querySelector('.widget-description').textContent.toLowerCase();

            if (name.includes(term) || type.includes(term)) {
                card.style.display = '';
            } else {
                card.style.display = 'none';
            }
        });
    }

    showError(message) {
        // Simple error display - could be enhanced
        AdminModal.alert({message: message, type: 'error'});
    }
}

// CSS loading is handled by hf-css-loader.js (loaded before this file)

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Config is parsed early by hf-css-loader.js (loaded before this file)
    var config = window.HFBuilderConfig || {};

    // Apply force light mode to preview (honors merchant's theme setting)
    if (config && config.forceLightMode) {
        var previewEl = document.getElementById('preview-content');
        if (previewEl) { previewEl.setAttribute('data-theme', 'light'); }
    }

    if (config && config.builderType) {
        // CSS loading is handled by hf-css-loader.js (loaded before this file)
        window.headerFooterBuilder = new HeaderFooterBuilder(config);
    }

    // Back button — navigate to URL stored in data-url attribute
    var backBtn = document.getElementById('back-btn');
    if (backBtn && backBtn.dataset.url) {
        backBtn.addEventListener('click', function() {
            window.location.href = backBtn.dataset.url;
        });
    }
});
