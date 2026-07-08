/**
 * Page Thumbnail Trigger Script
 * Runs in admin pages to orchestrate thumbnail capture via a hidden iframe.
 */
window.PageThumbnailCapture = (function() {
    'use strict';

    var captureIframe = null;
    var currentPageId = null;
    var captureTimeout = null;
    var messageHandler = null;

    // Compute admin page builder preview prefix from current URL
    var adminPBPrefix = (function() {
        var match = location.pathname.match(/^\/([a-z]{2}(?:[_-][a-zA-Z]+)?)\//);
        var lang = match ? '/' + match[1] : '';
        return lang + '/admin/page_builder/';
    })();

    function trigger(pageId, pageSlug) {
        if (!pageSlug || !pageId) return;

        // Clean up any existing capture
        cleanup();

        currentPageId = pageId;

        // Create hidden iframe
        captureIframe = document.createElement('iframe');
        captureIframe.style.cssText = 'position:fixed;left:-9999px;top:-9999px;width:1280px;height:960px;border:none;opacity:0;pointer-events:none;z-index:-1;';
        captureIframe.src = adminPBPrefix + 'preview/' + encodeURIComponent(pageSlug) + '/?capture=1';
        document.body.appendChild(captureIframe);

        // Listen for postMessage from capture iframe
        messageHandler = function(event) {
            if (event.origin !== location.origin) return;
            var data = event.data;
            if (!data || !data.type) return;

            if (data.type === 'page-thumbnail-captured' && currentPageId) {
                uploadThumbnail(currentPageId, data.imageData);
                cleanup();
            } else if (data.type === 'page-thumbnail-error') {
                console.warn('[PageThumbnail] Capture failed:', data.error);
                cleanup();
            }
        };
        window.addEventListener('message', messageHandler);

        // Timeout cleanup after 30 seconds
        captureTimeout = setTimeout(function() {
            console.warn('[PageThumbnail] Capture timed out for page', pageId);
            cleanup();
        }, 30000);
    }

    function getCSRFToken() {
        // Read from <meta name="csrf-token"> (set in admin base_site.html)
        var meta = document.querySelector('meta[name="csrf-token"]');
        if (meta) return meta.getAttribute('content');
        // Fallback: try reading from a form input
        var input = document.querySelector('[name=csrfmiddlewaretoken]');
        if (input) return input.value;
        return '';
    }

    function uploadThumbnail(pageId, imageData) {
        fetch('/api/page-builder/page/' + pageId + '/capture-thumbnail/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({ image_data: imageData })
        }).then(function(resp) {
            return resp.json();
        }).then(function(data) {
            if (data.success) {
                updateCardThumbnail(pageId, data.thumbnail_url);
            }
        }).catch(function(err) {
            console.error('[PageThumbnail] Upload failed:', err);
        });
    }

    function updateCardThumbnail(pageId, thumbnailUrl) {
        var checkbox = document.querySelector('.list-row-card input[value="' + pageId + '"]');
        if (!checkbox) return;

        var card = checkbox.closest('.list-row-card');
        if (!card) return;

        var iconDiv = card.querySelector('.list-row-card-icon');
        if (!iconDiv) return;

        // Use DOM API instead of innerHTML to prevent XSS
        var img = document.createElement('img');
        img.src = thumbnailUrl;
        img.alt = 'Page preview';
        img.loading = 'lazy';
        iconDiv.textContent = '';
        iconDiv.appendChild(img);
    }

    function cleanup() {
        if (captureTimeout) {
            clearTimeout(captureTimeout);
            captureTimeout = null;
        }
        if (messageHandler) {
            window.removeEventListener('message', messageHandler);
            messageHandler = null;
        }
        if (captureIframe && captureIframe.parentNode) {
            captureIframe.remove();
            captureIframe = null;
        }
        currentPageId = null;
    }

    /**
     * Queue multiple pages for sequential capture with delay between each.
     * @param {Array} pages - Array of {id, slug} objects
     * @param {number} delay - Milliseconds between captures (default 5000)
     */
    function triggerQueue(pages, delay) {
        if (!pages || !pages.length) return;
        delay = delay || 5000;
        var index = 0;

        function next() {
            if (index >= pages.length) return;
            var page = pages[index++];
            trigger(page.id, page.slug);
            if (index < pages.length) {
                setTimeout(next, delay);
            }
        }

        next();
    }

    return {
        trigger: trigger,
        triggerQueue: triggerQueue,
        cleanup: cleanup
    };
})();
