/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * GeoIP JavaScript API Client
 *
 * Provides location detection and preference management.
 * Usage: Include this script, then call GeoIP.get(callback).
 */
window.GeoIP = {
  _location: null,
  _callbacks: [],

  get: function (callback) {
    if (this._location) {
      callback(this._location);
      return;
    }

    this._callbacks.push(callback);

    if (this._callbacks.length === 1) {
      this._fetch();
    }
  },

  _fetch: function () {
    const self = this;
    fetch('/api/geoip/v1/resolve/')
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        self._location = data;
        self._callbacks.forEach(function (cb) {
          cb(data);
        });
        self._callbacks = [];
      })
      .catch(function (error) {
        console.error('GeoIP fetch failed:', error);
        self._callbacks.forEach(function (cb) {
          cb({});
        });
        self._callbacks = [];
      });
  },

  setPreference: function (key, value) {
    fetch('/api/geoip/v1/preference/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this._getCSRFToken(),
      },
      body: JSON.stringify({ [key]: value }),
    });
  },

  _getCSRFToken: function () {
    const meta = document.querySelector('meta[name="csrf-token"]');
    if (meta && meta.content) return meta.content;
    const input = document.querySelector('[name=csrfmiddlewaretoken]');
    if (input) return input.value;
    return '';
  },
};
