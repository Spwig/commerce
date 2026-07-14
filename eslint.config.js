/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

// ESLint flat config (ESLint 9+)
import js from '@eslint/js';
import tsPlugin from '@typescript-eslint/eslint-plugin';
import tsParser from '@typescript-eslint/parser';
import globals from 'globals';

export default [
  js.configs.recommended,
  {
    files: ['**/*.{js,jsx,ts,tsx}'],
    languageOptions: {
      ecmaVersion: 2021,
      sourceType: 'module',
      parser: tsParser,
      globals: {
        // Standard browser + service-worker environment (fetch, setTimeout,
        // navigator, self, IntersectionObserver, MutationObserver, etc.).
        ...globals.browser,
        ...globals.serviceworker,
        ...globals.worker,
        // Node globals (build tooling / eslint config files).
        ...globals.node,
        // Django/common globals.
        django: 'readonly',
        jQuery: 'readonly',
        $: 'readonly',
        // Project-wide singletons attached to `window` by core JS bundles.
        AdminModal: 'readonly',
        AdminUtils: 'readonly',
        AdminTabs: 'readonly',
        AdminListFilters: 'readonly',
        AdminToast: 'readonly',
        AddressAutocomplete: 'readonly',
        AddElementCommand: 'readonly',
        MoveElementCommand: 'readonly',
        ColorPickerUtility: 'readonly',
        HelpSystem: 'readonly',
        ManifestI18n: 'readonly',
        ProviderConfirm: 'readonly',
        ProviderModal: 'readonly',
        ShadowEditor: 'readonly',
        TypographyEditor: 'readonly',
        UnitSelectorUtility: 'readonly',
        UploadQueueManager: 'readonly',
        VersionHistory: 'readonly',
        applyFilters: 'readonly',
        formatNumber: 'readonly',
        pageStateManager: 'readonly',
        translationHtmlEditor: 'readonly',
        translationTextEditor: 'readonly',
        FIELD_TYPES: 'readonly',
        // Localised UI-string dictionaries injected by Django templates.
        UI_STRINGS: 'readonly',
        FB_TRANSLATIONS: 'readonly',
        // Django JavaScriptCatalog helpers.
        gettext: 'readonly',
        ngettext: 'readonly',
        interpolate: 'readonly',
        pluralidx: 'readonly',
        // Vendor libraries loaded via <script> tags (not npm-imported).
        Chart: 'readonly', // chart.js
        Sortable: 'readonly', // SortableJS
        fabric: 'readonly', // fabric.js
        L: 'readonly', // leaflet
        monaco: 'readonly', // monaco editor
        flatpickr: 'readonly',
        ClassicEditor: 'readonly', // ckeditor
        RevolutCheckout: 'readonly', // revolut payments
        ApplePaySession: 'readonly',
        html2canvas: 'readonly',
        URLify: 'readonly', // Django admin slugify helper
        define: 'readonly', // AMD/RequireJS loader
        // Editor / builder utility singletons.
        AdminLinkSelector: 'readonly',
        BackgroundEditor: 'readonly',
        BorderEditorUtility: 'readonly',
        CampaignBuilder: 'readonly',
        contentManager: 'readonly',
        DeleteElementCommand: 'readonly',
        DOMSnapshot: 'readonly',
        HFBuilderConfig: 'readonly',
        HistoryManager: 'readonly',
        MediaLibrary: 'readonly',
        MediaManager: 'readonly',
        ProductInfiniteScroll: 'readonly',
        SearchAutocomplete: 'readonly',
        SpacingEditor: 'readonly',
        TranslationEditor: 'readonly',
        UpdateElementCommand: 'readonly',
        // Callable helpers exposed by inline templates / other modules.
        closeHistoryDropdowns: 'readonly',
        deselectAllElements: 'readonly',
        executeQuery: 'readonly',
        formatCurrency: 'readonly',
        initVisualBuilder: 'readonly',
        openMiniCart: 'readonly',
        openPageSettings: 'readonly',
        addToCart: 'readonly',
        showNotification: 'readonly',
        toggleHelpDrawer: 'readonly',
        updateBulkActionUI: 'readonly',
      },
    },
    plugins: {
      '@typescript-eslint': tsPlugin,
    },
    rules: {
      'no-unused-vars': 'warn',
      'no-console': 'off', // Allow console in development
      semi: ['error', 'always'],
      quotes: ['error', 'single', { avoidEscape: true }],
      'prefer-const': 'warn',
      'no-var': 'warn',
      // Empty blocks are often intentional (empty catch, placeholder callbacks).
      'no-empty': ['error', { allowEmptyCatch: true }],
      // Widespread pre-ES6 patterns in the older admin JS. Left as warnings so
      // new code doesn't drift, but existing code doesn't block CI.
      'no-case-declarations': 'warn',
      'no-redeclare': 'warn',
      'no-useless-escape': 'warn',
      'no-prototype-builtins': 'warn',
    },
  },
  {
    ignores: [
      'node_modules/',
      'staticfiles/',
      'shop_venv/',
      '.archive/',
      '**/vendor/',
      '**/ckeditor5/',
      '**/*.min.js',
      'pos_app/dist/',
      'pos_app/frontend_build/',
      'pos_app/frontend/node_modules/',
      'pos_app/frontend_build/',
      '**/migrations/*',
    ],
  },
];
