/**
 * Spwig Error Reporter
 *
 * Captures JavaScript errors (window.onerror, unhandledrejection) and sends
 * them to the local server for buffering and eventual batch transmission.
 *
 * Configuration is read from data attributes on the <html> element:
 *   data-error-reporting="true|false"
 *   data-error-reporting-js="true|false"
 */
(function() {
    'use strict';

    var htmlEl = document.documentElement;
    var enabled = htmlEl.getAttribute('data-error-reporting') === 'true';
    var jsEnabled = htmlEl.getAttribute('data-error-reporting-js') === 'true';

    if (!enabled || !jsEnabled) return;

    var ERROR_BUFFER = [];
    var MAX_BUFFER = 20;
    var FLUSH_INTERVAL = 30000; // 30 seconds
    var ENDPOINT = '/api/error-reports/js/';
    var SEEN = {};

    function fingerprint(message, source, line) {
        return (message || '') + ':' + (source || '') + ':' + (line || '');
    }

    window.onerror = function(message, source, lineno, colno, error) {
        var fp = fingerprint(message, source, lineno);
        if (SEEN[fp]) return;
        SEEN[fp] = true;

        ERROR_BUFFER.push({
            type: 'error',
            message: String(message || ''),
            source: source || '',
            lineno: lineno || 0,
            colno: colno || 0,
            stack: error && error.stack ? error.stack : '',
            url: window.location.pathname,
            user_agent: navigator.userAgent,
            timestamp: new Date().toISOString()
        });

        if (ERROR_BUFFER.length >= MAX_BUFFER) flushErrors();
    };

    window.addEventListener('unhandledrejection', function(event) {
        var reason = event.reason;
        var message = reason instanceof Error ? reason.message : String(reason || '');
        var stack = reason instanceof Error ? (reason.stack || '') : '';
        var fp = fingerprint(message, 'promise', 0);
        if (SEEN[fp]) return;
        SEEN[fp] = true;

        ERROR_BUFFER.push({
            type: 'unhandledrejection',
            message: message,
            stack: stack,
            url: window.location.pathname,
            user_agent: navigator.userAgent,
            timestamp: new Date().toISOString()
        });

        if (ERROR_BUFFER.length >= MAX_BUFFER) flushErrors();
    });

    function flushErrors() {
        if (ERROR_BUFFER.length === 0) return;

        var batch = ERROR_BUFFER.splice(0, MAX_BUFFER);
        var payload = JSON.stringify({ errors: batch });

        // Use sendBeacon for reliability (survives page unload)
        if (navigator.sendBeacon) {
            var blob = new Blob([payload], { type: 'application/json' });
            navigator.sendBeacon(ENDPOINT, blob);
        } else {
            try {
                var xhr = new XMLHttpRequest();
                xhr.open('POST', ENDPOINT, true);
                xhr.setRequestHeader('Content-Type', 'application/json');
                xhr.send(payload);
            } catch (e) {
                // Silently fail
            }
        }
    }

    setInterval(flushErrors, FLUSH_INTERVAL);
    window.addEventListener('beforeunload', flushErrors);
})();
