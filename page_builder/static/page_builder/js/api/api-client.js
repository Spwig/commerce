/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * API Client for Page Builder
 * Centralized API calls with consistent error handling and URL construction
 */

class APIClient {
    constructor() {
        this.baseUrl = '/api';  // API routes are directly under language prefix
        this.csrfToken = null;
        this.language = document.documentElement.lang || 'en';
    }

    /**
     * Initialize the API client
     */
    init() {
        this.csrfToken = this.getCSRFToken();
    }

    /**
     * Get CSRF token from meta tag, form input, or cookie
     */
    getCSRFToken() {
        // Meta tag (works with CSRF_COOKIE_HTTPONLY=True)
        const metaTag = document.querySelector('meta[name="csrf-token"]');
        if (metaTag && metaTag.content) return metaTag.content;

        // Hidden form input
        const tokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
        if (tokenElement) return tokenElement.value;

        // Cookie fallback (won't work with CSRF_COOKIE_HTTPONLY=True)
        const name = 'csrftoken';
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    return decodeURIComponent(cookie.substring(name.length + 1));
                }
            }
        }

        return null;
    }

    /**
     * Build full URL for page builder API
     */
    buildUrl(path) {
        // Remove leading slash if present
        if (path.startsWith('/')) {
            path = path.substring(1);
        }
        // Remove 'api/' prefix if present - we'll add the correct one
        if (path.startsWith('api/')) {
            path = path.substring(4);
        }
        // API routes are at /api/page-builder/ (outside i18n_patterns, no language prefix)
        return `/api/page-builder/${path}`;
    }

    /**
     * Make a fetch request with common headers
     */
    async fetch(url, options = {}) {
        const defaultOptions = {
            headers: {
                'X-CSRFToken': this.csrfToken || this.getCSRFToken(),
                'Accept': 'application/json',
            },
            credentials: 'same-origin'
        };

        // Merge headers
        if (options.headers) {
            options.headers = { ...defaultOptions.headers, ...options.headers };
        } else {
            options.headers = defaultOptions.headers;
        }

        // Add Content-Type for JSON body
        if (options.body && typeof options.body === 'object' && !(options.body instanceof FormData)) {
            options.headers['Content-Type'] = 'application/json';
            options.body = JSON.stringify(options.body);
        }

        // Merge other options
        const finalOptions = { ...defaultOptions, ...options };

        try {
            const response = await fetch(this.buildUrl(url), finalOptions);
            return response;
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    // ==================== Page APIs ====================

    /**
     * Get page data
     */
    async getPage(pageId) {
        return this.fetch(`api/page/${pageId}/`);
    }

    /**
     * Update page
     */
    async updatePage(pageId, data) {
        return this.fetch(`api/page/${pageId}/`, {
            method: 'PATCH',
            body: data
        });
    }

    /**
     * Load page content
     */
    async loadPageContent(pageId) {
        return this.fetch(`api/page/${pageId}/content/`);
    }

    /**
     * Auto-save page (save draft)
     */
    async autoSavePage(pageId) {
        return this.fetch(`api/page/${pageId}/save-draft/`, {
            method: 'POST'
        });
    }

    /**
     * Publish page
     */
    async publishPage(pageId) {
        return this.fetch(`api/page/${pageId}/publish/`, {
            method: 'POST'
        });
    }

    // ==================== Version APIs ====================

    /**
     * Get page versions
     */
    async getPageVersions(pageId) {
        return this.fetch(`api/page/${pageId}/versions/`);
    }

    /**
     * Get specific version
     */
    async getPageVersion(pageId, versionId) {
        return this.fetch(`api/page/${pageId}/versions/${versionId}/`);
    }

    /**
     * Restore version (revert to version)
     */
    async restorePageVersion(pageId, versionId) {
        return this.fetch(`api/page/${pageId}/revert/${versionId}/`, {
            method: 'POST'
        });
    }

    // ==================== Element APIs ====================

    /**
     * Get element data
     */
    async getElement(elementId) {
        return this.fetch(`api/elements/${elementId}/`);
    }

    /**
     * Create element
     */
    async createElement(data) {
        return this.fetch('api/elements/', {
            method: 'POST',
            body: data
        });
    }

    /**
     * Update element
     */
    async updateElement(elementId, data) {
        return this.fetch(`api/elements/${elementId}/`, {
            method: 'PATCH',
            body: data
        });
    }

    /**
     * Delete element
     */
    async deleteElement(elementId) {
        return this.fetch(`api/elements/${elementId}/`, {
            method: 'DELETE'
        });
    }

    /**
     * Duplicate element
     */
    async duplicateElement(elementId) {
        return this.fetch(`api/elements/${elementId}/duplicate/`, {
            method: 'POST'
        });
    }

    /**
     * Move element
     */
    async moveElement(elementId, data) {
        return this.fetch(`api/elements/${elementId}/move/`, {
            method: 'POST',
            body: data
        });
    }

    /**
     * Reorder elements
     */
    async reorderElements(data) {
        return this.fetch('api/elements/reorder/', {
            method: 'POST',
            body: data
        });
    }

    /**
     * Update element content
     */
    async updateElementContent(elementId, content) {
        return this.fetch(`api/elements/${elementId}/content/`, {
            method: 'PATCH',
            body: { content }
        });
    }

    /**
     * Update element styles
     */
    async updateElementStyles(elementId, styles) {
        return this.fetch(`api/elements/${elementId}/styles/`, {
            method: 'PATCH',
            body: { style_overrides: styles }
        });
    }

    // ==================== Template APIs ====================

    /**
     * Get element templates
     */
    async getElementTemplates() {
        return this.fetch('api/templates/elements/');
    }

    /**
     * Get element template
     */
    async getElementTemplate(templateId) {
        return this.fetch(`api/templates/elements/${templateId}/`);
    }

    /**
     * Get page templates
     */
    async getPageTemplates() {
        return this.fetch('api/templates/pages/');
    }

    /**
     * Apply page template
     */
    async applyPageTemplate(pageId, templateId) {
        return this.fetch(`api/page/${pageId}/apply-template/`, {
            method: 'POST',
            body: { template_id: templateId }
        });
    }

    // ==================== Media APIs ====================

    /**
     * Upload media file
     */
    async uploadMedia(file, metadata = {}) {
        const formData = new FormData();
        formData.append('file', file);

        // Add metadata
        Object.keys(metadata).forEach(key => {
            formData.append(key, metadata[key]);
        });

        return this.fetch('api/media/upload/', {
            method: 'POST',
            body: formData
        });
    }

    /**
     * Get media library
     */
    async getMediaLibrary(params = {}) {
        const queryParams = new URLSearchParams(params);
        return this.fetch(`api/media/?${queryParams}`);
    }

    /**
     * Delete media item
     */
    async deleteMedia(mediaId) {
        return this.fetch(`api/media/${mediaId}/`, {
            method: 'DELETE'
        });
    }

    // ==================== Settings APIs ====================

    /**
     * Get builder settings
     */
    async getBuilderSettings() {
        return this.fetch('api/settings/');
    }

    /**
     * Update builder settings
     */
    async updateBuilderSettings(settings) {
        return this.fetch('api/settings/', {
            method: 'PATCH',
            body: settings
        });
    }

    // ==================== Utility APIs ====================

    /**
     * Search elements
     */
    async searchElements(query) {
        return this.fetch(`api/elements/search/?q=${encodeURIComponent(query)}`);
    }

    /**
     * Export page
     */
    async exportPage(pageId, format = 'json') {
        return this.fetch(`api/page/${pageId}/export/?format=${format}`);
    }

    /**
     * Import page
     */
    async importPage(data) {
        return this.fetch('api/page/import/', {
            method: 'POST',
            body: data
        });
    }

    /**
     * Get element hierarchy
     */
    async getElementHierarchy(pageId) {
        return this.fetch(`api/page/${pageId}/hierarchy/`);
    }

    /**
     * Validate page
     */
    async validatePage(pageId) {
        return this.fetch(`api/page/${pageId}/validate/`);
    }

    // ==================== Error Handling ====================

    /**
     * Handle API errors consistently
     */
    handleError(error) {
        console.error('API Error:', error);

        // Show user-friendly error message
        if (window.builderInstance && window.builderInstance.showNotification) {
            let message = 'An error occurred. Please try again.';

            if (error.status === 401) {
                message = 'Your session has expired. Please refresh the page.';
            } else if (error.status === 403) {
                message = 'You do not have permission to perform this action.';
            } else if (error.status === 404) {
                message = 'The requested resource was not found.';
            } else if (error.status === 500) {
                message = 'A server error occurred. Please contact support.';
            } else if (error.message) {
                message = error.message;
            }

            window.builderInstance.showNotification(message, 'error');
        }

        return error;
    }

    /**
     * Parse response and handle errors
     */
    async parseResponse(response) {
        if (!response.ok) {
            let errorData;
            try {
                errorData = await response.json();
            } catch {
                errorData = { detail: 'An error occurred' };
            }

            const error = new Error(errorData.detail || errorData.message || 'Request failed');
            error.status = response.status;
            error.data = errorData;

            throw error;
        }

        try {
            return await response.json();
        } catch {
            return response;
        }
    }
}

// Create singleton instance
const apiClient = new APIClient();

// Export for module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = APIClient;
}

// Make available globally
window.APIClient = APIClient;
window.apiClient = apiClient;

// Initialize on DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => apiClient.init());
} else {
    apiClient.init();
}