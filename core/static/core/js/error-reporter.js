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
(function () {
  'use strict';

  const htmlEl = document.documentElement;
  const enabled = htmlEl.getAttribute('data-error-reporting') === 'true';
  const jsEnabled = htmlEl.getAttribute('data-error-reporting-js') === 'true';

  if (!enabled || !jsEnabled) return;

  const ERROR_BUFFER = [];
  const MAX_BUFFER = 20;
  const FLUSH_INTERVAL = 30000; // 30 seconds
  const ENDPOINT = '/api/error-reports/js/';
  const SEEN = {};

  function fingerprint(message, source, line) {
    return (message || '') + ':' + (source || '') + ':' + (line || '');
  }

  window.onerror = function (message, source, lineno, colno, error) {
    const fp = fingerprint(message, source, lineno);
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
      timestamp: new Date().toISOString(),
    });

    if (ERROR_BUFFER.length >= MAX_BUFFER) flushErrors();
  };

  window.addEventListener('unhandledrejection', function (event) {
    const reason = event.reason;
    const message = reason instanceof Error ? reason.message : String(reason || '');
    const stack = reason instanceof Error ? reason.stack || '' : '';
    const fp = fingerprint(message, 'promise', 0);
    if (SEEN[fp]) return;
    SEEN[fp] = true;

    ERROR_BUFFER.push({
      type: 'unhandledrejection',
      message: message,
      stack: stack,
      url: window.location.pathname,
      user_agent: navigator.userAgent,
      timestamp: new Date().toISOString(),
    });

    if (ERROR_BUFFER.length >= MAX_BUFFER) flushErrors();
  });

  function flushErrors() {
    if (ERROR_BUFFER.length === 0) return;

    const batch = ERROR_BUFFER.splice(0, MAX_BUFFER);
    const payload = JSON.stringify({ errors: batch });

    // Use sendBeacon for reliability (survives page unload)
    if (navigator.sendBeacon) {
      const blob = new Blob([payload], { type: 'application/json' });
      navigator.sendBeacon(ENDPOINT, blob);
    } else {
      try {
        const xhr = new XMLHttpRequest();
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
