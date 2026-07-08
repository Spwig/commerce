/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */
/* Social Share Widget - Share intent URLs + API tracking */
(function() {
    'use strict';

    var SHARE_URLS = {
        facebook:  'https://www.facebook.com/sharer/sharer.php?u={url}',
        twitter:   'https://twitter.com/intent/tweet?url={url}&text={title}',
        linkedin:  'https://www.linkedin.com/sharing/share-offsite/?url={url}',
        pinterest: 'https://pinterest.com/pin/create/button/?url={url}&description={title}',
        whatsapp:  'https://wa.me/?text={title}%20{url}',
        telegram:  'https://t.me/share/url?url={url}&text={title}',
        email:     'mailto:?subject={title}&body={url}'
    };

    function getCsrfToken() {
        return window.getCSRFToken ? window.getCSRFToken() : '';
    }

    function initWidgets() {
        document.querySelectorAll('.social-share-widget').forEach(function(widget) {
            if (widget.dataset.initialized) return;
            widget.dataset.initialized = 'true';

            var shareUrl = encodeURIComponent(widget.dataset.shareUrl || window.location.href);
            var shareTitle = encodeURIComponent(widget.dataset.shareTitle || document.title);
            var trackShares = widget.dataset.trackShares === 'true';
            var contentType = widget.dataset.contentType;
            var objectId = widget.dataset.objectId;

            widget.querySelectorAll('.social-share-btn').forEach(function(btn) {
                btn.addEventListener('click', function() {
                    var platform = btn.dataset.platform;
                    var template = SHARE_URLS[platform];
                    if (!template) return;

                    var url = template.replace(/{url}/g, shareUrl).replace(/{title}/g, shareTitle);

                    if (platform === 'email') {
                        window.location.href = url;
                    } else {
                        window.open(url, '_blank', 'width=600,height=400,noopener,noreferrer');
                    }

                    // Visual feedback
                    btn.classList.add('shared');
                    setTimeout(function() { btn.classList.remove('shared'); }, 2000);

                    // Track share via API (fire-and-forget)
                    if (trackShares && contentType && objectId) {
                        var token = getCsrfToken();
                        fetch('/api/social/track/', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRFToken': token
                            },
                            body: JSON.stringify({
                                content_type: contentType,
                                object_id: parseInt(objectId, 10),
                                platform: platform,
                                url: decodeURIComponent(shareUrl)
                            })
                        }).catch(function() { /* silent fail for anonymous users */ });
                    }
                });
            });
        });
    }

    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initWidgets);
    } else {
        initWidgets();
    }
})();
