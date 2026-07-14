/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Theme Initialization
 *
 * Sets the theme attribute on the html element and handles auto-detection of system theme preference.
 * This script runs synchronously (not deferred) to prevent FOUC (Flash of Unstyled Content).
 *
 * Reads theme from meta[name="admin-theme"] tag set by Django template.
 * Reads CSRF token from meta[name="csrf-token"] tag for theme switching API calls.
 */
(function () {
  'use strict';

  // Read theme from meta tag set by Django template
  const themeMeta = document.querySelector('meta[name="admin-theme"]');
  const theme = themeMeta?.content || 'dark';

  // Set theme attribute for CSS targeting
  document.documentElement.setAttribute('data-theme', theme);

  // Auto-detect system preference if no preference is set and user hasn't manually set theme
  if (
    !document.cookie.includes('admin_theme=') &&
    !localStorage.getItem('user_manually_set_theme') &&
    window.matchMedia
  ) {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    if (prefersDark && theme === 'light') {
      // User prefers dark mode but we're showing light, switch automatically
      const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content || '';
      const switchThemeUrl = document.querySelector('meta[name="switch-theme-url"]')?.content || '';

      if (switchThemeUrl && csrfToken) {
        fetch(switchThemeUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
          },
          body: JSON.stringify({ theme: 'dark' }),
        });
      }
    }
  }
})();
