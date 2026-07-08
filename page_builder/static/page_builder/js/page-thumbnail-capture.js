/**
 * Page Thumbnail Capture Script
 * Runs inside the preview iframe when loaded with ?capture=1
 * Captures the rendered page using html2canvas and sends it to the parent window.
 */
(function() {
    'use strict';

    // Only run if capture mode is active
    var params = new URLSearchParams(window.location.search);
    if (!params.has('capture')) return;

    // Hide the preview banner for a clean capture
    var banner = document.querySelector('.preview-banner');
    if (banner) banner.style.display = 'none';

    function captureWhenReady() {
        Promise.all([
            document.fonts ? document.fonts.ready : Promise.resolve(),
            waitForImages()
        ]).then(function() {
            // Allow CSS transitions/animations to settle
            setTimeout(doCapture, 800);
        });
    }

    function waitForImages() {
        var images = document.querySelectorAll('img');
        var promises = [];
        images.forEach(function(img) {
            if (!img.complete) {
                promises.push(new Promise(function(resolve) {
                    img.onload = resolve;
                    img.onerror = resolve;
                }));
            }
        });
        // Timeout after 10 seconds even if images haven't loaded
        var timeout = new Promise(function(resolve) { setTimeout(resolve, 10000); });
        return Promise.race([Promise.all(promises), timeout]);
    }

    function doCapture() {
        // Dynamically load html2canvas only when capturing
        var script = document.createElement('script');
        script.src = '/static/core/vendor/js/html2canvas.min.js';
        script.onload = function() {
            html2canvas(document.body, {
                width: 1280,
                height: 960,
                windowWidth: 1280,
                windowHeight: 960,
                scale: 0.5,
                useCORS: true,
                logging: false,
                allowTaint: true,
                backgroundColor: '#ffffff',
            }).then(function(canvas) {
                var dataUrl = canvas.toDataURL('image/png', 0.9);
                if (window.parent !== window) {
                    window.parent.postMessage({
                        type: 'page-thumbnail-captured',
                        imageData: dataUrl
                    }, location.origin);
                }
            }).catch(function(err) {
                console.error('[PageThumbnail] html2canvas capture failed:', err);
                if (window.parent !== window) {
                    window.parent.postMessage({
                        type: 'page-thumbnail-error',
                        error: err.message
                    }, location.origin);
                }
            });
        };
        script.onerror = function() {
            console.error('[PageThumbnail] Failed to load html2canvas');
            if (window.parent !== window) {
                window.parent.postMessage({
                    type: 'page-thumbnail-error',
                    error: 'Failed to load html2canvas'
                }, location.origin);
            }
        };
        document.head.appendChild(script);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', captureWhenReady);
    } else {
        captureWhenReady();
    }
})();
