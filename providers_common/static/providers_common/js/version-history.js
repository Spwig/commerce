/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Version History Module
 * ======================
 * Shared module for fetching and rendering component version history.
 * Used by both the provider detail modal and component update cards.
 *
 * CSP-safe: No inline styles, no inline event handlers, no innerHTML with external data.
 * i18n-ready: All user-facing strings loaded from a JSON data island (#version-history-i18n).
 */

var VersionHistory = (function() {
    'use strict';

    var cache = {};
    var msgs = {};

    function loadI18n() {
        var el = document.getElementById('version-history-i18n');
        if (!el) return;
        try { msgs = JSON.parse(el.textContent); } catch (e) { /* ignore */ }
    }

    function i18n(key, fallback) {
        return msgs[key] || fallback;
    }

    /* ==========================================================
       DOM helpers
       ========================================================== */

    function makeEl(tag, className, text) {
        var node = document.createElement(tag);
        if (className) node.className = className;
        if (text) node.textContent = text;
        return node;
    }

    /* ==========================================================
       Fetch
       ========================================================== */

    /**
     * Fetch version history from admin endpoint.
     * Returns a Promise resolving to an array of version objects.
     */
    function fetchVersions(slug) {
        if (cache[slug]) {
            return Promise.resolve(cache[slug]);
        }

        var langPrefix = (typeof AdminUtils !== 'undefined' && AdminUtils.getLanguagePrefix)
            ? AdminUtils.getLanguagePrefix()
            : '/' + (document.documentElement.lang || 'en');
        var url = langPrefix + '/admin/component_updates/componentregistry/version-history/' + encodeURIComponent(slug) + '/';

        return fetch(url, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
            credentials: 'same-origin'
        })
        .then(function(r) { return r.json(); })
        .then(function(data) {
            if (data.success && data.versions) {
                cache[slug] = data.versions;
                return data.versions;
            }
            return [];
        });
    }

    /* ==========================================================
       Render
       ========================================================== */

    /**
     * Build DOM for version timeline.
     * Returns a DOM element containing the rendered version list.
     */
    function renderTimeline(versions) {
        var container = makeEl('div', 'version-history-timeline');

        if (!versions || versions.length === 0) {
            container.appendChild(
                makeEl('p', 'version-history-empty', i18n('noVersions', 'No version history available.'))
            );
            return container;
        }

        versions.forEach(function(v) {
            var entry = makeEl('div', 'version-history-entry');

            // Header row: version tag + badges + date
            var header = makeEl('div', 'version-history-header');

            header.appendChild(makeEl('span', 'version-history-tag', 'v' + v.version));

            if (v.security_update) {
                var secBadge = makeEl('span', 'version-history-badge security', i18n('security', 'Security'));
                header.appendChild(secBadge);
            }
            if (v.breaking_changes) {
                var breakBadge = makeEl('span', 'version-history-badge breaking', i18n('breaking', 'Breaking Changes'));
                header.appendChild(breakBadge);
            }

            if (v.published_at) {
                try {
                    var dateStr = new Date(v.published_at).toLocaleDateString(undefined, {
                        year: 'numeric', month: 'short', day: 'numeric'
                    });
                    header.appendChild(makeEl('span', 'version-history-date', dateStr));
                } catch (e) {
                    // Fallback if date parsing fails
                    header.appendChild(makeEl('span', 'version-history-date', v.published_at));
                }
            }

            entry.appendChild(header);

            // Changelog body
            var changelogText = v.changelog || v.release_notes || '';
            if (changelogText) {
                var body = makeEl('div', 'version-history-body');
                var lines = changelogText.split('\n').filter(function(l) { return l.trim(); });

                if (lines.length > 0) {
                    var ul = document.createElement('ul');
                    lines.forEach(function(line) {
                        var li = document.createElement('li');
                        li.textContent = line.replace(/^[-*]\s*/, '');
                        ul.appendChild(li);
                    });
                    body.appendChild(ul);
                }

                entry.appendChild(body);
            }

            container.appendChild(entry);
        });

        return container;
    }

    /* ==========================================================
       Init
       ========================================================== */

    document.addEventListener('DOMContentLoaded', loadI18n);

    return {
        fetch: fetchVersions,
        render: renderTimeline,
        clearCache: function() { cache = {}; }
    };
})();
