/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Announcement Widget - Frontend JavaScript
 * Handles horizontal scroll, vertical cycle, static rotation,
 * modal display, and dismiss functionality.
 */
(function () {
  'use strict';

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.widget-announcement').forEach(initWidget);
  });

  function initWidget(widget) {
    const displayMode = widget.dataset.displayMode || 'scroll_horizontal';
    const pauseOnHover = widget.dataset.pauseHover !== 'false';

    // Dismiss button
    const ignoreDismiss = widget.dataset.ignoreDismiss === 'true';
    const closeBtn = widget.querySelector('.announcement-close');
    if (closeBtn) {
      closeBtn.addEventListener('click', function (e) {
        e.stopPropagation();
        widget.style.display = 'none';
        const zone = widget.closest('.header-zone--notification');
        if (zone) zone.style.display = 'none';
        if (!ignoreDismiss) {
          try {
            sessionStorage.setItem('announcement_dismissed', '1');
          } catch (err) {
            /* ignore */
          }
        }
      });
      // Check if previously dismissed this session (skip in preview mode)
      if (!ignoreDismiss) {
        try {
          if (sessionStorage.getItem('announcement_dismissed') === '1') {
            widget.style.display = 'none';
            const zone = widget.closest('.header-zone--notification');
            if (zone) zone.style.display = 'none';
            return;
          }
        } catch (err) {
          /* ignore */
        }
      }
    }

    // Setup display mode
    if (reducedMotion || displayMode === 'static') {
      initStaticMode(widget, pauseOnHover);
    } else if (displayMode === 'scroll_horizontal') {
      initHorizontalScroll(widget);
    } else if (displayMode === 'scroll_vertical') {
      initVerticalCycle(widget, pauseOnHover);
    }

    // Setup click handlers for modal/link
    initClickHandlers(widget);
  }

  /**
   * Horizontal scroll: duplicate items for seamless loop.
   * Speed adapts to content width for consistent readability.
   */
  function initHorizontalScroll(widget) {
    const track = widget.querySelector('.announcement-track');
    if (!track) return;

    const items = track.querySelectorAll('.announcement-item');
    if (items.length === 0) return;

    // Single item — no scrolling needed, just show it
    if (items.length === 1) {
      track.style.animation = 'none';
      track.style.justifyContent = 'center';
      return;
    }

    // Duplicate content for seamless scrolling
    items.forEach(function (item) {
      const clone = item.cloneNode(true);
      clone.setAttribute('aria-hidden', 'true');
      track.appendChild(clone);
    });

    // Calculate duration based on content width for consistent speed.
    // The animation scrolls -50% (one full set of original items).
    // We target ~60px/s so text remains readable regardless of item count.
    const pixelsPerSecond = 60;
    const configSpeed = parseFloat(widget.dataset.scrollSpeed);
    const originalWidth = track.scrollWidth / 2; // half = one set of items
    let duration;

    if (configSpeed && items.length <= 2) {
      // For 1-2 items, honour the configured fixed duration
      duration = configSpeed;
    } else {
      // Scale duration to content width
      duration = Math.max(originalWidth / pixelsPerSecond, 10);
    }

    track.style.animationDuration = duration + 's';
  }

  /**
   * Vertical cycle: rotate items one at a time.
   */
  function initVerticalCycle(widget, pauseOnHover) {
    const track = widget.querySelector('.announcement-track');
    if (!track) return;

    const items = track.querySelectorAll('.announcement-item');
    if (items.length <= 1) {
      // Single item - just show it
      if (items[0]) items[0].classList.add('active');
      return;
    }

    let currentIndex = 0;
    let paused = false;
    const duration = (parseFloat(widget.dataset.cycleDuration) || 5) * 1000;

    // Show first item
    items[0].classList.add('active');

    function cycle() {
      if (paused) return;

      const current = items[currentIndex];
      const nextIndex = (currentIndex + 1) % items.length;
      const next = items[nextIndex];

      current.classList.remove('active');
      current.classList.add('exiting');

      next.classList.add('active');

      // Clean up exiting class after transition
      setTimeout(function () {
        current.classList.remove('exiting');
      }, 600);

      currentIndex = nextIndex;
    }

    const intervalId = setInterval(cycle, duration);

    if (pauseOnHover) {
      widget.addEventListener('mouseenter', function () {
        paused = true;
      });
      widget.addEventListener('mouseleave', function () {
        paused = false;
      });
    }

    // Cleanup on page unload
    window.addEventListener('beforeunload', function () {
      clearInterval(intervalId);
    });
  }

  /**
   * Static mode: simple fade rotation.
   */
  function initStaticMode(widget, pauseOnHover) {
    const track = widget.querySelector('.announcement-track');
    if (!track) return;

    const items = track.querySelectorAll('.announcement-item');
    if (items.length <= 1) {
      if (items[0]) items[0].classList.add('active');
      return;
    }

    let currentIndex = 0;
    let paused = false;
    const duration = (parseFloat(widget.dataset.cycleDuration) || 5) * 1000;

    items[0].classList.add('active');

    function rotate() {
      if (paused) return;

      items[currentIndex].classList.remove('active');
      currentIndex = (currentIndex + 1) % items.length;
      items[currentIndex].classList.add('active');
    }

    const intervalId = setInterval(rotate, duration);

    if (pauseOnHover) {
      widget.addEventListener('mouseenter', function () {
        paused = true;
      });
      widget.addEventListener('mouseleave', function () {
        paused = false;
      });
    }

    window.addEventListener('beforeunload', function () {
      clearInterval(intervalId);
    });
  }

  /**
   * Click handlers: modal or direct link navigation.
   */
  function initClickHandlers(widget) {
    const backdrop = document.getElementById('announcement-modal');
    if (!backdrop) return;

    const modalContent = backdrop.querySelector('.announcement-modal-content');
    const closeBtn = backdrop.querySelector('.announcement-modal-close');

    // Close modal handlers
    function closeModal() {
      backdrop.classList.remove('visible');
      document.body.style.overflow = '';
    }

    if (closeBtn) {
      closeBtn.addEventListener('click', closeModal);
    }

    backdrop.addEventListener('click', function (e) {
      if (e.target === backdrop) closeModal();
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && backdrop.classList.contains('visible')) {
        closeModal();
      }
    });

    // Item click handlers — only for modal items
    widget.querySelectorAll('.announcement-item[data-modal-id]').forEach(function (item) {
      item.addEventListener('click', function (e) {
        if (e.target.closest('a')) return; // Let normal links work
        e.preventDefault();
        openModal(item.dataset.modalId, modalContent, backdrop);
      });
    });

    // Also handle modal trigger buttons
    widget.querySelectorAll('.announcement-modal-trigger').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        const announcementId = btn.dataset.announcementId;
        if (announcementId) {
          openModal(announcementId, modalContent, backdrop);
        }
      });
    });
  }

  /**
   * Open announcement modal by fetching detail from API.
   */
  function openModal(announcementId, contentEl, backdrop) {
    if (!contentEl || !backdrop) return;

    // Show loading state
    contentEl.innerHTML = '<div style="text-align:center;padding:2rem;">...</div>';
    backdrop.classList.add('visible');
    document.body.style.overflow = 'hidden';

    fetch('/api/announcements/' + announcementId + '/detail/')
      .then(function (res) {
        return res.json();
      })
      .then(function (data) {
        contentEl.innerHTML = buildModalContent(data);
      })
      .catch(function () {
        contentEl.innerHTML =
          '<p style="text-align:center;padding:2rem;">Could not load announcement.</p>';
      });
  }

  /**
   * Build modal HTML from announcement data.
   */
  function buildModalContent(data) {
    let html = '';

    // Image
    if (data.image_url) {
      if (data.image_display_mode === 'background') {
        html +=
          '<div class="announcement-modal-image-bg" style="background-image:url(' +
          escapeAttr(data.image_url) +
          ');--announcement-overlay-opacity:' +
          data.image_overlay_opacity +
          '">';
        html += '<div class="announcement-modal-overlay-content">';
        html += '<div class="announcement-modal-title">' + data.title + '</div>';
        if (data.body) {
          html += '<div class="announcement-modal-body">' + data.body + '</div>';
        }
        if (data.link_url && data.link_text) {
          html +=
            '<a href="' +
            escapeAttr(data.link_url) +
            '" class="announcement-modal-link-btn">' +
            escapeHtml(data.link_text) +
            '</a>';
        }
        html += '</div></div>';
        return html;
      } else {
        html +=
          '<img src="' +
          escapeAttr(data.image_url) +
          '" alt="" class="announcement-modal-image-banner">';
      }
    }

    // Text content (for banner or no-image mode)
    html += '<div class="announcement-modal-text-content">';
    html += '<div class="announcement-modal-title">' + data.title + '</div>';
    if (data.body) {
      html += '<div class="announcement-modal-body">' + data.body + '</div>';
    }
    if (data.link_url && data.link_text) {
      html +=
        '<a href="' +
        escapeAttr(data.link_url) +
        '" class="announcement-modal-link-btn">' +
        escapeHtml(data.link_text) +
        '</a>';
    }
    html += '</div>';

    return html;
  }

  function escapeHtml(str) {
    if (!str) return '';
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  function escapeAttr(str) {
    if (!str) return '';
    return str
      .replace(/&/g, '&amp;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
  }
})();
