/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Overlay portal + scroll lock.
 *
 * Storefront widgets are rendered into header zones, so any full-screen overlay
 * they own starts life as a descendant of <header class="site-header">. That is
 * unsafe: the header is position:sticky with a z-index, so it forms a stacking
 * context that caps everything inside it at the header's own layer, and any
 * transform / filter / backdrop-filter / will-change / contain on the header or
 * one of its zones makes it the containing block for position:fixed children —
 * which collapses a full-screen overlay into the header strip.
 *
 * mount() relocates the overlay nodes to a body-level root so neither applies.
 * The host div is given the original ancestor's class list, so descendant CSS
 * selectors (`.widget-search .search-form`, ...) keep matching and no
 * stylesheet needs to change.
 */

(function () {
  'use strict';

  if (window.SpwigPortal) {
    return;
  }

  const ROOT_ID = 'spwig-overlay-root';
  let scrollLockCount = 0;
  let savedScrollY = 0;

  // Held in module scope rather than looked up by id each time: page content can
  // claim an id (product reviews and other user-authored HTML render into the
  // document), and adopting a foreign element would hand it control over every
  // overlay's styling — including re-introducing the containing-block trap.
  let portalRoot = null;

  /**
   * The portal root is the last child of <body> and must stay style-free —
   * a transform or z-index here would reintroduce the very trap we're escaping.
   */
  function getRoot() {
    if (portalRoot && portalRoot.isConnected) {
      // Keep it last so it always paints above earlier body content.
      if (portalRoot.parentNode !== document.body || portalRoot.nextSibling) {
        document.body.appendChild(portalRoot);
      }
      return portalRoot;
    }

    // Never adopt an element this module did not create.
    const impostor = document.getElementById(ROOT_ID);
    if (impostor) {
      impostor.removeAttribute('id');
    }

    portalRoot = document.createElement('div');
    portalRoot.id = ROOT_ID;
    document.body.appendChild(portalRoot);
    return portalRoot;
  }

  /**
   * iOS Safari ignores `overflow: hidden` on <body> for touch scrolling, so
   * pin the body instead and restore the scroll offset on release.
   */
  function lockScroll() {
    scrollLockCount += 1;
    if (scrollLockCount > 1) {
      return;
    }
    savedScrollY = window.scrollY || window.pageYOffset || 0;
    document.body.style.position = 'fixed';
    document.body.style.top = '-' + savedScrollY + 'px';
    document.body.style.left = '0';
    document.body.style.right = '0';
    document.body.style.width = '100%';
    document.body.style.overflow = 'hidden';
  }

  function unlockScroll() {
    if (scrollLockCount === 0) {
      return;
    }
    scrollLockCount -= 1;
    if (scrollLockCount > 0) {
      return;
    }
    document.body.style.position = '';
    document.body.style.top = '';
    document.body.style.left = '';
    document.body.style.right = '';
    document.body.style.width = '';
    document.body.style.overflow = '';
    window.scrollTo(0, savedScrollY);
  }

  window.SpwigPortal = {
    /**
     * Move nodes to the body-level portal root.
     *
     * @param {Element[]} nodes    Elements to relocate, in order.
     * @param {string} hostClass   Class list for the host div, so the widget's
     *                             descendant selectors keep matching after the
     *                             move. Pass a hardcoded literal — do NOT pass
     *                             `widget.className`, which carries
     *                             merchant-controlled `css_classes`.
     * @param {Object} [options]   {lockScroll: boolean}
     * @returns {Object|null} handle for unmount()
     */
    mount: function (nodes, hostClass, options) {
      if (!nodes || !nodes.length) {
        return null;
      }
      const opts = options || {};
      const host = document.createElement('div');
      host.className = hostClass || '';
      host.setAttribute('data-spwig-portal', 'true');

      const entries = [];
      nodes.forEach(function (node) {
        if (!node || !node.parentNode) {
          return;
        }
        // A comment marker remembers the exact original slot so unmount()
        // restores DOM order even if siblings changed while open.
        const marker = document.createComment('spwig-portal-placeholder');
        node.parentNode.insertBefore(marker, node);
        entries.push({ node: node, marker: marker });
        host.appendChild(node);
      });

      if (!entries.length) {
        return null;
      }

      getRoot().appendChild(host);

      if (opts.lockScroll) {
        lockScroll();
      }

      return { host: host, entries: entries, locked: !!opts.lockScroll };
    },

    /** Return portaled nodes to their original slots and drop the host. */
    unmount: function (handle) {
      if (!handle) {
        return;
      }
      handle.entries.forEach(function (entry) {
        if (entry.marker && entry.marker.parentNode) {
          entry.marker.parentNode.insertBefore(entry.node, entry.marker);
          entry.marker.parentNode.removeChild(entry.marker);
        }
      });
      if (handle.host && handle.host.parentNode) {
        handle.host.parentNode.removeChild(handle.host);
      }
      if (handle.locked) {
        unlockScroll();
      }
    },

    lockScroll: lockScroll,
    unlockScroll: unlockScroll,
  };
})();
