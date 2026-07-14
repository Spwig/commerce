/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * ManifestI18n - Client-side translation for provider manifest content
 * =====================================================================
 *
 * Third-party providers include translations in their manifest.json and use
 * data-i18n attributes in their HTML templates. This module applies those
 * translations based on the current admin language.
 *
 * Fallback chain:
 *   1. Merchant's current admin language
 *   2. Content stays as-is in the developer's default_language
 *
 * Usage (setup instructions):
 *   ManifestI18n.apply(translationsObject);
 *
 * Usage (single string):
 *   var name = ManifestI18n.translate(translationsObject, 'meta.name', comp.name);
 */
const ManifestI18n = (function () {
  'use strict';

  /**
   * Get the current admin interface language.
   * @returns {string} Language code (e.g., 'en', 'fr', 'zh-hans')
   */
  function getAdminLanguage() {
    return document.documentElement.lang || 'en';
  }

  /**
   * Resolve the best matching language strings from translations.
   *
   * The translations object includes a special 'default_language' key that
   * declares the language of the base content (HTML text, manifest name/description).
   * If the admin language matches default_language, no translation is needed.
   * If no translation exists for the admin language, content stays as-is.
   *
   * @param {Object} translations - {"default_language": "fr", "es": {...}, "de": {...}}
   * @returns {Object|null} The best matching language strings, or null if no swap needed
   */
  function _resolve(translations) {
    if (!translations || typeof translations !== 'object') return null;

    const lang = getAdminLanguage();
    const defaultLang = translations.default_language || 'en';

    // If admin language matches the default language, no translation needed
    // (the HTML/base content is already in that language)
    if (lang === defaultLang) return null;

    // Try admin language
    if (translations[lang]) return translations[lang];

    // No match for admin language - content stays as-is (in default_language)
    return null;
  }

  /**
   * Apply data-i18n translations to the current page.
   *
   * Finds all elements with [data-i18n] attributes and replaces their
   * textContent with the translated string for the current admin language.
   * The HTML content is the fallback (in the developer's default language).
   *
   * @param {Object} translations - The manifest.json translations object
   *   with default_language key added by the platform
   */
  function apply(translations) {
    const strings = _resolve(translations);
    if (!strings) return;

    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      const key = el.getAttribute('data-i18n');
      if (key && strings[key] !== undefined) {
        // Use textContent (not innerHTML) for XSS safety
        el.textContent = strings[key];
      }
    });
  }

  /**
   * Translate a single string key from manifest translations.
   *
   * Used for translating provider names/descriptions on browse pages
   * and marketplace cards where data-i18n attributes aren't used.
   *
   * @param {Object} translations - The manifest.json translations object
   * @param {string} key - Translation key (e.g., 'meta.name', 'meta.description')
   * @param {string} fallback - Base content (already in developer's default language)
   * @returns {string} Translated string or fallback
   */
  function translate(translations, key, fallback) {
    const strings = _resolve(translations);
    if (!strings) return fallback;
    return strings[key] || fallback;
  }

  return { apply: apply, translate: translate };
})();

// Auto-initialize from data island if present
document.addEventListener('DOMContentLoaded', function () {
  const el = document.getElementById('manifest-translations');
  if (el && window.ManifestI18n) {
    try {
      ManifestI18n.apply(JSON.parse(el.textContent));
    } catch (e) {
      console.error('ManifestI18n: failed to parse translations', e);
    }
  }
});
