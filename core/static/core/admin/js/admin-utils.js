/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Admin Utilities Module
 * =====================================
 * Centralized helper functions for Django admin JavaScript
 * Provides utilities for i18n URL building, CSRF token handling, and common patterns
 *
 * Available globally as window.AdminUtils
 * ===================================== */

(function () {
  'use strict';

  const AdminUtils = {
    /**
     * Get language prefix from current URL
     * Dynamically extracts language code without hardcoded language lists
     * Supports both 2-letter codes (en, es, fr) and extended codes (zh-hans)
     *
     * @returns {string} Language prefix like '/en' or '/zh-hans', defaults to '/en' if not found
     *
     * @example
     * // On URL: http://example.com/fr/admin/products/
     * AdminUtils.getLanguagePrefix(); // Returns: '/fr'
     *
     * // On URL: http://example.com/zh-hans/admin/products/
     * AdminUtils.getLanguagePrefix(); // Returns: '/zh-hans'
     */
    getLanguagePrefix() {
      const path = window.location.pathname;
      // Match language code at start of path
      // Pattern: /xx/ or /xx-xx/ (e.g., /en/ or /zh-hans/)
      const match = path.match(/^\/([a-z]{2}(?:-[a-z]+)?)\//);
      return match ? `/${match[1]}` : '/en';
    },

    /**
     * Build admin URL with automatic language prefix
     * Ensures all admin AJAX calls respect Django's i18n URL structure
     *
     * @param {string} path - Path without language prefix (e.g., '/exchange-rates/admin/...')
     * @returns {string} Full URL with language prefix
     *
     * @example
     * // Current URL: http://example.com/fr/admin/...
     * AdminUtils.buildAdminUrl('/exchange-rates/admin/provider/1/sync/');
     * // Returns: '/fr/exchange-rates/admin/provider/1/sync/'
     *
     * AdminUtils.buildAdminUrl('api/currencies/');
     * // Returns: '/fr/api/currencies/'
     */
    buildAdminUrl(path) {
      const langPrefix = this.getLanguagePrefix();
      // Ensure path starts with /
      const cleanPath = path.startsWith('/') ? path : '/' + path;
      return `${langPrefix}${cleanPath}`;
    },

    /**
     * Get CSRF token from multiple sources
     * Tries cookie, meta tag, and hidden input in that order
     *
     * @returns {string} CSRF token or empty string if not found
     *
     * @example
     * fetch(url, {
     *     method: 'POST',
     *     headers: {
     *         'X-CSRFToken': AdminUtils.getCsrfToken(),
     *         'Content-Type': 'application/json'
     *     }
     * });
     */
    getCsrfToken() {
      // Try meta tag first (always available in admin base templates,
      // and works even with CSRF_COOKIE_HTTPONLY=True)
      const metaTag = document.querySelector('meta[name="csrf-token"]');
      if (metaTag && metaTag.content) return metaTag.content;

      // Try hidden input in forms
      const input = document.querySelector('[name="csrfmiddlewaretoken"]');
      if (input) return input.value;

      // Cookie fallback (won't work with CSRF_COOKIE_HTTPONLY=True)
      const token = this.getCookie('csrftoken');
      if (token) return token;

      console.warn('AdminUtils: CSRF token not found');
      return '';
    },

    /**
     * Get cookie value by name
     * Helper function for getCsrfToken and other cookie operations
     *
     * @param {string} name - Cookie name
     * @returns {string|null} Cookie value or null if not found
     *
     * @example
     * const theme = AdminUtils.getCookie('admin_theme');
     */
    getCookie(name) {
      if (!document.cookie) return null;

      const cookies = document.cookie.split(';');
      for (const cookie of cookies) {
        const trimmed = cookie.trim();
        if (trimmed.startsWith(name + '=')) {
          return decodeURIComponent(trimmed.substring(name.length + 1));
        }
      }
      return null;
    },

    /**
     * Build fetch options with CSRF token
     * Convenience method for common AJAX patterns
     *
     * @param {string} method - HTTP method (GET, POST, PUT, DELETE, etc.)
     * @param {object} data - Optional data to send (will be JSON stringified for POST/PUT)
     * @param {object} additionalHeaders - Optional additional headers
     * @returns {object} Fetch options object ready to use
     *
     * @example
     * fetch(url, AdminUtils.buildFetchOptions('POST', {action: 'sync'}));
     *
     * // With custom headers
     * fetch(url, AdminUtils.buildFetchOptions('POST', data, {
     *     'X-Custom-Header': 'value'
     * }));
     */
    buildFetchOptions(method = 'GET', data = null, additionalHeaders = {}) {
      const options = {
        method: method.toUpperCase(),
        headers: {
          'X-CSRFToken': this.getCsrfToken(),
          ...additionalHeaders,
        },
      };

      // Add body for methods that support it
      if (data && ['POST', 'PUT', 'PATCH'].includes(options.method)) {
        if (data instanceof FormData) {
          // Let browser set Content-Type for FormData
          options.body = data;
        } else {
          // JSON data
          options.headers['Content-Type'] = 'application/json';
          options.body = JSON.stringify(data);
        }
      }

      return options;
    },
  };

  // Export to window for global access
  window.AdminUtils = AdminUtils;

  // Log successful loading (can be removed in production)
  console.log('AdminUtils loaded successfully');
})();
