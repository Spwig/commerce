/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */
/**
 * Console Capture — must load synchronously (no defer) before all other scripts.
 * Intercepts console.log/warn/error/info into a circular buffer so the
 * Bug Report Wizard can include console output in reports.
 */
(function() {
    var buffer = [];
    var MAX = 50;
    var original = {
        log: console.log,
        warn: console.warn,
        error: console.error,
        info: console.info
    };

    ['log', 'warn', 'error', 'info'].forEach(function(level) {
        console[level] = function() {
            var args = Array.prototype.slice.call(arguments);
            var message = args.map(function(v) {
                if (v === null) return 'null';
                if (v === undefined) return 'undefined';
                if (typeof v === 'object') {
                    try { return JSON.stringify(v); } catch (e) { return String(v); }
                }
                return String(v);
            }).join(' ');

            buffer.push({
                level: level,
                message: message.substring(0, 500),
                timestamp: new Date().toISOString()
            });
            if (buffer.length > MAX) buffer.shift();

            original[level].apply(console, args);
        };
    });

    window.__spwig_console_buffer = buffer;
    window.__spwig_nav_breadcrumbs = [{
        url: location.href,
        timestamp: new Date().toISOString()
    }];
})();
