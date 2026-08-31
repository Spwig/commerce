/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/*
 * Campaign Studio visual builder.
 *
 * Adapts page_builder's builder patterns (config.json-driven property panel,
 * drag-from-palette, SortableJS reorder, per-block API persistence) as
 * self-contained code. The canvas applies the shop's theme tokens so blocks
 * render in the merchant's branding while the surrounding chrome stays admin.
 */
(function () {
  'use strict';

  function readJSON(id, fallback) {
    var el = document.getElementById(id);
    if (!el) return fallback;
    try {
      return JSON.parse(el.textContent);
    } catch (e) {
      return fallback;
    }
  }

  var config = readJSON('em-config', {});
  var schemas = readJSON('em-schemas-data', {});
  var initialBlocks = readJSON('em-blocks-data', []);
  var themeTokens = readJSON('em-theme-tokens', {});
  var mergeFields = readJSON('em-merge-fields', []);
  var assets = readJSON('em-assets', {});

  var API = '/api/email-marketing';
  var campaignId = config.campaign_id;

  // The canvas is a Shadow DOM: the host (light DOM) carries the theme tokens
  // (custom properties inherit across the boundary); the shadow loads the shop's
  // theme CSS so blocks render with real branding, isolated from the admin.
  var canvasHost = document.getElementById('em-canvas');
  var canvas = null; // shadow block container, set by initCanvas()
  var emptyState = null; // shadow empty-state, set by initCanvas()
  var propsEmpty = document.getElementById('em-props-empty');
  var propsForm = document.getElementById('em-props-form');
  var saveStatus = document.getElementById('em-save-status');

  var selectedId = null;

  // ---- CSRF ----
  // The CSRF cookie is HttpOnly, so read the token from the {% csrf_token %}
  // hidden input the template renders (fall back to the cookie if readable).
  function csrfToken() {
    var input = document.querySelector('#em-csrf input[name=csrfmiddlewaretoken]');
    if (input && input.value) return input.value;
    var m = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/);
    return m ? decodeURIComponent(m[1]) : '';
  }

  function api(path, method, body) {
    return fetch(API + path, {
      method: method,
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken() },
      body: body ? JSON.stringify(body) : undefined,
    }).then(function (r) {
      if (!r.ok) throw new Error('Request failed: ' + r.status);
      return r.json();
    });
  }

  // ---- Canvas: Shadow DOM host + theme CSS for storefront parity ----
  function initCanvas() {
    var shadow = canvasHost.attachShadow({ mode: 'open' });
    var links = '';
    if (assets.theme_css) links += '<link rel="stylesheet" href="' + assets.theme_css + '">';
    if (assets.canvas_css) links += '<link rel="stylesheet" href="' + assets.canvas_css + '">';
    if (assets.fa_css) links += '<link rel="stylesheet" href="' + assets.fa_css + '">';
    shadow.innerHTML =
      links +
      '<div class="em-canvas-inner" id="em-canvas-inner">' +
      '<div class="em-empty" id="em-empty">' +
      '<i class="fas fa-envelope-open-text"></i>' +
      '<p>Drag blocks here to build your email.</p>' +
      '</div></div>';
    canvas = shadow.getElementById('em-canvas-inner');
    emptyState = shadow.getElementById('em-empty');
  }

  // Theme tokens go on the light-DOM host; inherited custom properties cross the
  // shadow boundary, so the theme CSS + blocks inside resolve them.
  function applyThemeTokens() {
    Object.keys(themeTokens).forEach(function (key) {
      canvasHost.style.setProperty(key, themeTokens[key]);
    });
  }

  // Apply the inherited base (Style) props — background, padding, border — to a
  // block's canvas wrapper, mirroring what the email <mj-section> does, so the
  // canvas preview matches the sent email. Values are the CSS strings the shared
  // editors emit; we parse the same way the serializer does.
  function firstToken(s) {
    return (s || '').trim().split(/\s+/)[0] || '';
  }
  function applyBaseStyle(el, content) {
    content = content || {};
    el.style.background = content.section_bg || '';

    var pad = (content.padding || '')
      .replace(/^padding:\s*/i, '')
      .replace(/;+$/, '')
      .trim();
    el.style.padding = pad || '';

    el.style.border = '';
    el.style.borderRadius = '';
    var b = content.border || '';
    if (b) {
      var w = /border-width:\s*([^;\n]+)/i.exec(b);
      var s = /border-style:\s*([^;\n]+)/i.exec(b);
      var c = /border-color:\s*([^;\n]+)/i.exec(b);
      var r = /border-radius:\s*([^;\n]+)/i.exec(b);
      if (w && s && c) {
        el.style.border = firstToken(w[1]) + ' ' + firstToken(s[1]) + ' ' + firstToken(c[1]);
      } else if (/^\d/.test(b)) {
        el.style.border = b.split(';')[0].trim();
      }
      if (r) el.style.borderRadius = firstToken(r[1]);
    }
  }

  // ---- Rendering blocks into the canvas ----
  function makeWrapper(block) {
    var wrap = document.createElement('div');
    wrap.className = 'em-block-wrapper';
    wrap.dataset.blockId = block.id;
    wrap.dataset.blockType = block.block_type;

    var content = document.createElement('div');
    content.className = 'em-block-content';
    content.innerHTML = block.html;
    applyBaseStyle(content, block.content);
    wrap.appendChild(content);

    var controls = document.createElement('div');
    controls.className = 'em-block-controls';
    controls.innerHTML =
      '<button type="button" class="em-block-handle" title="Drag to reorder"><i class="fas fa-up-down-left-right"></i></button>' +
      '<button type="button" data-block-action="delete" title="Delete"><i class="fas fa-trash"></i></button>';
    wrap.appendChild(controls);

    wrap.addEventListener('click', function (e) {
      if (e.target.closest('[data-block-action]')) return;
      selectBlock(block.id);
    });
    controls.querySelector('[data-block-action="delete"]').addEventListener('click', function () {
      removeBlock(block.id);
    });
    return wrap;
  }

  function renderBlock(block) {
    canvas.appendChild(makeWrapper(block));
    updateEmptyState();
  }

  function replaceBlockHtml(block) {
    var wrap = canvas.querySelector('[data-block-id="' + block.id + '"] .em-block-content');
    if (wrap) {
      wrap.innerHTML = block.html;
      applyBaseStyle(wrap, block.content);
    }
  }

  function updateEmptyState() {
    var has = canvas.querySelector('.em-block-wrapper');
    if (emptyState) emptyState.style.display = has ? 'none' : '';
  }

  // ---- Property panel (schema-driven) ----
  function selectBlock(blockId) {
    selectedId = blockId;
    canvas.querySelectorAll('.em-block-wrapper').forEach(function (w) {
      w.classList.toggle('is-selected', w.dataset.blockId === blockId);
    });
    var wrap = canvas.querySelector('[data-block-id="' + blockId + '"]');
    if (!wrap) return;
    renderProps(wrap.dataset.blockType, blockId);
  }

  function currentContent(blockId) {
    // Pull the latest content off the form inputs.
    var values = {};
    propsForm.querySelectorAll('[data-prop-key]').forEach(function (input) {
      values[input.dataset.propKey] = input.value;
    });
    return values;
  }

  // Tab order + labels for the property panel (mirrors page_builder's tabbed
  // panel). 'content' = block-specific props; 'style' = inherited base props.
  var TAB_ORDER = ['content', 'style'];
  var TAB_LABELS = { content: 'Content', style: 'Style' };

  // Property type -> shared utility editor that attaches via `.attach(el, value)`
  // and round-trips a value (the same editors Page Builder uses). Each spec:
  //   cls   – window global class name
  //   opts  – extra constructor options
  //   extract(a,b) – pull the value to STORE from the callback args
  //   feed(stored) – convert the stored value to what .attach() parses
  // Spacing/Border round-trip a CSS string. Typography must store the settings
  // OBJECT (its CSS string drops defaults and omits colour), so we JSON it and
  // rebuild a CSS declaration for the editor to parse on attach.
  var UTILITY_SPECS = {
    spacing: {
      cls: 'SpacingEditor',
      opts: { mode: 'padding', units: ['px', '%'] },
      extract: function (a, b) {
        return typeof a === 'string' ? a : '';
      },
      feed: function (v) {
        return v;
      },
    },
    border_advanced: {
      cls: 'BorderEditorUtility',
      opts: {},
      extract: function (a, b) {
        return typeof b === 'string' ? b : '';
      },
      feed: function (v) {
        return v;
      },
    },
    typography: {
      cls: 'TypographyEditor',
      opts: {},
      extract: function (a, b) {
        return b && typeof b === 'object' ? JSON.stringify(b) : '';
      },
      feed: function (v) {
        return typographyToCss(v);
      },
    },
  };

  function typographyToCss(stored) {
    if (!stored) return '';
    var s;
    try {
      s = JSON.parse(stored);
    } catch (e) {
      return '';
    }
    var map = {
      fontFamily: 'font-family',
      fontSize: 'font-size',
      fontWeight: 'font-weight',
      fontStyle: 'font-style',
      lineHeight: 'line-height',
      letterSpacing: 'letter-spacing',
      textAlign: 'text-align',
      textTransform: 'text-transform',
      textDecoration: 'text-decoration',
      color: 'color',
    };
    var out = [];
    Object.keys(map).forEach(function (k) {
      var v = s[k];
      if (v && v !== 'inherit' && v !== 'currentColor') out.push(map[k] + ': ' + v);
    });
    return out.join('; ');
  }

  function renderField(container, schema, key, content, blockId) {
    var prop = schema.properties[key];
    var field = document.createElement('div');
    field.className = 'em-prop-field';

    var label = document.createElement('label');
    label.textContent = prop.label || key;
    field.appendChild(label);

    var spec = UTILITY_SPECS[prop.type];
    if (prop.type === 'color' && window.ColorPickerUtility) {
      // Reuse the shared, site-wide colour picker (same one Page Builder,
      // branding and Site Settings use) for cross-admin consistency.
      appendColorControl(field, key, content[key], blockId);
    } else if (PICKER_TYPES[prop.type]) {
      // media / product / link — a modal picker instead of a hand-typed value.
      appendPickerControl(field, key, content[key], blockId, prop.type);
    } else if (spec && window[spec.cls]) {
      appendUtilityControl(field, key, content[key], blockId, spec);
    } else {
      var input = buildInput(prop, key, content[key]);
      input.dataset.propKey = key;
      field.appendChild(input);
      var evt = input.tagName === 'SELECT' ? 'change' : 'input';
      input.addEventListener(
        evt,
        debounce(function () {
          saveBlockContent(blockId);
        }, 350)
      );
      // Text fields get a "merge field" inserter for personalisation.
      if (prop.type === 'string' || prop.type === 'textarea') {
        appendMergeInserter(field, input, blockId);
      }
    }
    container.appendChild(field);
  }

  function insertAtCursor(input, text) {
    var start = input.selectionStart;
    var end = input.selectionEnd;
    if (typeof start === 'number') {
      input.value = input.value.slice(0, start) + text + input.value.slice(end);
      input.focus();
      input.selectionStart = input.selectionEnd = start + text.length;
    } else {
      input.value += text;
    }
  }

  // A small "+ Merge field" dropdown that inserts a [[token]] at the cursor.
  function appendMergeInserter(field, input, blockId) {
    if (!mergeFields.length) return;
    var sel = document.createElement('select');
    sel.className = 'em-merge-insert';
    var def = document.createElement('option');
    def.value = '';
    def.textContent = '+ Merge field';
    sel.appendChild(def);
    mergeFields.forEach(function (f) {
      var o = document.createElement('option');
      o.value = f.key;
      o.textContent = f.label;
      sel.appendChild(o);
    });
    sel.addEventListener('change', function () {
      if (!sel.value) return;
      insertAtCursor(input, '[[' + sel.value + ']]');
      sel.value = '';
      saveBlockContent(blockId);
    });
    field.appendChild(sel);
  }

  // Generic host for the `.attach`-based shared editors (spacing, border, …).
  // The editor injects its own trigger + popup into `host`; the value it emits
  // (a CSS string) is stored on a hidden [data-prop-key] input for saving, and
  // fed back to the editor on attach so it round-trips.
  function appendUtilityControl(field, key, value, blockId, spec) {
    var val =
      value == null ? '' : typeof value === 'object' ? JSON.stringify(value) : String(value);
    var host = document.createElement('div');
    host.className = 'em-util-host';
    var hidden = document.createElement('input');
    hidden.type = 'hidden';
    hidden.dataset.propKey = key;
    hidden.value = val;
    field.appendChild(host);
    field.appendChild(hidden);

    var save = debounce(function () {
      saveBlockContent(blockId);
    }, 350);
    function onCb(a, b) {
      var v = spec.extract(a, b);
      if (!v) return;
      hidden.value = v;
      save();
    }

    var opts = Object.assign({ propertyKey: key, onChange: onCb, onApply: onCb }, spec.opts || {});
    try {
      new window[spec.cls](opts).attach(host, spec.feed(val));
    } catch (e) {
      // Fallback: a plain text input still lets the value be edited/saved.
      var input = document.createElement('input');
      input.type = 'text';
      input.dataset.propKey = key;
      input.value = val;
      field.removeChild(host);
      field.removeChild(hidden);
      field.appendChild(input);
      input.addEventListener('input', save);
    }
  }

  function renderProps(blockType, blockId) {
    var schema = schemas[blockType];
    if (!schema) return;
    propsEmpty.hidden = true;
    propsForm.hidden = false;
    propsForm.innerHTML = '';

    var block = findBlock(blockId);
    var content = (block && block.content) || {};

    // Group property keys by their tab, preserving declaration order.
    var byTab = {};
    Object.keys(schema.properties).forEach(function (key) {
      var tab = schema.properties[key].tab || 'content';
      (byTab[tab] = byTab[tab] || []).push(key);
    });
    var tabs = TAB_ORDER.filter(function (t) {
      return byTab[t] && byTab[t].length;
    });

    // Single tab → render fields directly, no tab bar.
    if (tabs.length <= 1) {
      var only = tabs[0] || 'content';
      (byTab[only] || []).forEach(function (key) {
        renderField(propsForm, schema, key, content, blockId);
      });
      return;
    }

    // Multiple tabs → familiar admin tab bar + panels.
    var bar = document.createElement('div');
    bar.className = 'admin-tabs';
    var panels = {};
    tabs.forEach(function (tab, i) {
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'admin-tab-btn' + (i === 0 ? ' active' : '');
      btn.innerHTML = '<span class="label">' + TAB_LABELS[tab] + '</span>';
      bar.appendChild(btn);

      var panel = document.createElement('div');
      panel.className = 'admin-tab-content em-tab-panel' + (i === 0 ? ' active' : '');
      (byTab[tab] || []).forEach(function (key) {
        renderField(panel, schema, key, content, blockId);
      });
      panels[tab] = panel;

      btn.addEventListener('click', function () {
        bar.querySelectorAll('.admin-tab-btn').forEach(function (b) {
          b.classList.toggle('active', b === btn);
        });
        Object.keys(panels).forEach(function (t) {
          panels[t].classList.toggle('active', t === tab);
        });
      });
    });
    propsForm.appendChild(bar);
    tabs.forEach(function (tab) {
      propsForm.appendChild(panels[tab]);
    });
  }

  // A colour control backed by the shared ColorPickerUtility: swatch + value,
  // an explicit "Not set" empty state, and a clear button. The value lives on a
  // hidden [data-prop-key] input so currentContent() reads it like any field.
  function appendColorControl(field, key, value, blockId) {
    var val = value == null ? '' : String(value);

    var hidden = document.createElement('input');
    hidden.type = 'hidden';
    hidden.dataset.propKey = key;
    hidden.value = val;

    var trigger = document.createElement('button');
    trigger.type = 'button';
    trigger.className = 'em-color-trigger';
    var swatch = document.createElement('span');
    swatch.className = 'em-color-swatch';
    var text = document.createElement('span');
    text.className = 'em-color-value';
    trigger.appendChild(swatch);
    trigger.appendChild(text);

    var clear = document.createElement('button');
    clear.type = 'button';
    clear.className = 'em-color-clear';
    clear.title = 'Clear';
    clear.textContent = '×';

    function paint(v) {
      if (v) {
        swatch.style.background = v;
        swatch.classList.remove('is-empty');
        text.textContent = v;
        clear.hidden = false;
      } else {
        swatch.style.background = '';
        swatch.classList.add('is-empty');
        text.textContent = 'Not set';
        clear.hidden = true;
      }
    }
    function setColor(v) {
      hidden.value = v || '';
      paint(hidden.value);
      saveBlockContent(blockId);
    }
    paint(val);

    trigger.addEventListener('click', function () {
      if (!trigger._picker) {
        trigger._picker = new window.ColorPickerUtility({
          onChange: function (color) {
            setColor(color);
          },
        });
      }
      trigger._picker.open(trigger, hidden.value || '#000000');
    });
    clear.addEventListener('click', function () {
      setColor('');
    });

    var row = document.createElement('div');
    row.className = 'em-color-row';
    row.appendChild(trigger);
    row.appendChild(clear);
    field.appendChild(row);
    field.appendChild(hidden);
  }

  // ---- Pickers (media / product / link) ----
  // Reuse the platform's existing pickers rather than hand-typed fields:
  //  * media   → the global media-library modal (window.selectImageFromLibrary)
  //  * product → page_builder's product-search API (id, name, thumbnail, price)
  //  * link    → page_builder's link-sources API (products/pages/categories/blog)
  // The chosen value lives on a hidden [data-prop-key] input, so currentContent()
  // harvests it exactly like any other field.
  var PICKER_TYPES = { media: 1, product: 1, link: 1, voucher: 1 };
  var PB_API = '/api/page-builder';

  function pbFetch(path) {
    return fetch(PB_API + path, { headers: { 'X-Requested-With': 'XMLHttpRequest' } }).then(
      function (r) {
        if (!r.ok) throw new Error('Request failed: ' + r.status);
        return r.json();
      }
    );
  }

  function labelEl(text) {
    var s = document.createElement('span');
    s.className = 'em-picker-label';
    s.textContent = text || '';
    return s;
  }
  function thumbEl(url, cls) {
    var img = document.createElement('img');
    img.className = cls || 'em-picker-thumb';
    img.src = url;
    img.alt = '';
    img.loading = 'lazy';
    return img;
  }

  function appendPickerControl(field, key, value, blockId, type) {
    var hidden = document.createElement('input');
    hidden.type = 'hidden';
    hidden.dataset.propKey = key;
    hidden.value = value == null ? '' : String(value);

    var trigger = document.createElement('button');
    trigger.type = 'button';
    trigger.className = 'em-picker-trigger';
    var preview = document.createElement('span');
    preview.className = 'em-picker-preview';
    trigger.appendChild(preview);

    var clear = document.createElement('button');
    clear.type = 'button';
    clear.className = 'em-picker-clear';
    clear.title = 'Clear';
    clear.textContent = '×';

    function setVal(v) {
      hidden.value = v || '';
      paint();
      saveBlockContent(blockId);
    }
    function paint() {
      var v = hidden.value;
      preview.innerHTML = '';
      if (!v) {
        var empty = document.createElement('span');
        empty.className = 'em-picker-empty';
        empty.textContent =
          type === 'media'
            ? 'Choose image…'
            : type === 'product'
              ? 'Choose product…'
              : type === 'voucher'
                ? 'Choose a code…'
                : 'Choose link…';
        preview.appendChild(empty);
        clear.hidden = true;
        return;
      }
      clear.hidden = false;
      if (type === 'media') {
        preview.appendChild(thumbEl(v));
        preview.appendChild(labelEl(v.split('/').pop() || v));
      } else if (type === 'link' || type === 'voucher') {
        preview.appendChild(labelEl(v));
      } else if (type === 'product') {
        preview.appendChild(labelEl('Product #' + v));
        pbFetch('/product-search/?ids=' + encodeURIComponent(v))
          .then(function (res) {
            var p = (res.products || [])[0];
            if (!p || hidden.value !== v) return;
            preview.innerHTML = '';
            if (p.thumbnail) preview.appendChild(thumbEl(p.thumbnail));
            preview.appendChild(labelEl(p.name));
          })
          .catch(function () {});
      }
    }
    paint();

    trigger.addEventListener('click', function () {
      if (type === 'media') {
        if (typeof window.selectImageFromLibrary === 'function') {
          window.selectImageFromLibrary(function (m) {
            if (m && m.url) setVal(m.url);
          });
        } else {
          setStatus('Media library unavailable');
        }
      } else if (type === 'product') {
        openProductPicker(function (p) {
          setVal(String(p.id));
        });
      } else if (type === 'link') {
        openLinkPicker(hidden.value, function (url) {
          setVal(url);
        });
      } else if (type === 'voucher') {
        openVoucherPicker(hidden.value, function (code) {
          setVal(code);
        });
      }
    });
    clear.addEventListener('click', function () {
      setVal('');
    });

    var row = document.createElement('div');
    row.className = 'em-picker-row';
    row.appendChild(trigger);
    row.appendChild(clear);
    field.appendChild(row);
    field.appendChild(hidden);
  }

  // A dynamically-created modal reusing the shared admin-modal component.
  function openPickerModal(titleHtml, buildBody) {
    var overlay = document.createElement('div');
    overlay.className = 'admin-modal-overlay em-picker-overlay';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.innerHTML =
      '<div class="admin-modal admin-modal--lg">' +
      '<div class="admin-modal-header">' +
      '<h2 class="admin-modal-title">' +
      titleHtml +
      '</h2>' +
      '<button type="button" class="admin-modal-close" aria-label="Close"><i class="fas fa-times"></i></button>' +
      '</div><div class="admin-modal-body"></div></div>';
    document.body.appendChild(overlay);
    document.body.classList.add('admin-modal-body-locked');
    overlay.classList.add('active');

    function close() {
      overlay.classList.remove('active');
      document.body.classList.remove('admin-modal-body-locked');
      document.removeEventListener('keydown', onKey);
      overlay.remove();
    }
    function onKey(e) {
      if (e.key === 'Escape') close();
    }
    document.addEventListener('keydown', onKey);
    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) close();
    });
    overlay.querySelector('.admin-modal-close').addEventListener('click', close);
    buildBody(overlay.querySelector('.admin-modal-body'), close);
  }

  // A result card: thumbnail (or placeholder) + title + optional meta. All text
  // is set via textContent, so API data can never inject markup.
  function resultCard(opts, onClick) {
    var card = document.createElement('button');
    card.type = 'button';
    card.className = 'em-picker-card';
    if (opts.thumbnail) {
      card.appendChild(thumbEl(opts.thumbnail, 'em-picker-card-thumb'));
    } else {
      var ph = document.createElement('span');
      ph.className = 'em-picker-card-thumb is-empty';
      var icon = document.createElement('i');
      icon.className = opts.icon || 'fas fa-image';
      ph.appendChild(icon);
      card.appendChild(ph);
    }
    var body = document.createElement('span');
    body.className = 'em-picker-card-body';
    var title = document.createElement('span');
    title.className = 'em-picker-card-title';
    title.textContent = opts.title || '';
    body.appendChild(title);
    if (opts.meta) {
      var meta = document.createElement('span');
      meta.className = 'em-picker-card-meta';
      meta.textContent = opts.meta;
      body.appendChild(meta);
    }
    card.appendChild(body);
    card.addEventListener('click', onClick);
    return card;
  }

  function openProductPicker(onSelect) {
    openPickerModal('<i class="fas fa-box"></i> Choose a product', function (body, close) {
      body.innerHTML =
        '<input type="search" class="em-picker-search" placeholder="Search products…">' +
        '<div class="em-picker-results" aria-live="polite"></div>';
      var search = body.querySelector('.em-picker-search');
      var results = body.querySelector('.em-picker-results');

      function render(products) {
        results.innerHTML = '';
        if (!products.length) {
          results.appendChild(labelEl('No products found.'));
          return;
        }
        products.forEach(function (p) {
          results.appendChild(
            resultCard(
              {
                title: p.name,
                meta: (p.price || '') + (p.is_on_sale ? ' · Sale' : ''),
                thumbnail: p.thumbnail,
              },
              function () {
                onSelect(p);
                close();
              }
            )
          );
        });
      }
      function load() {
        pbFetch('/product-search/?search=' + encodeURIComponent(search.value || ''))
          .then(function (res) {
            render(res.products || []);
          })
          .catch(function () {
            results.innerHTML = '';
            results.appendChild(labelEl('Search failed.'));
          });
      }
      search.addEventListener('input', debounce(load, 300));
      load();
      search.focus();
    });
  }

  function openLinkPicker(current, onSelect) {
    openPickerModal('<i class="fas fa-link"></i> Choose a link', function (body, close) {
      body.innerHTML =
        '<div class="em-picker-linkbar">' +
        '<select class="em-picker-type">' +
        '<option value="all">All</option>' +
        '<option value="product">Products</option>' +
        '<option value="page">Pages</option>' +
        '<option value="category">Categories</option>' +
        '<option value="blog">Blog posts</option>' +
        '</select>' +
        '<input type="search" class="em-picker-search" placeholder="Search…">' +
        '</div>' +
        '<div class="em-picker-results" aria-live="polite"></div>' +
        '<div class="em-picker-url">' +
        '<label class="em-picker-url-label">Or paste a URL</label>' +
        '<div class="em-picker-url-row">' +
        '<input type="url" class="em-picker-url-input" placeholder="https://…">' +
        '<button type="button" class="button em-picker-url-apply">Apply</button>' +
        '</div></div>';
      var typeSel = body.querySelector('.em-picker-type');
      var search = body.querySelector('.em-picker-search');
      var results = body.querySelector('.em-picker-results');
      var urlInput = body.querySelector('.em-picker-url-input');
      if (current && /^(https?:|\/|#)/.test(current)) urlInput.value = current;

      function render(data) {
        results.innerHTML = '';
        var any = false;
        ['products', 'pages', 'categories', 'blog_posts'].forEach(function (groupKey) {
          (data[groupKey] || []).forEach(function (item) {
            any = true;
            results.appendChild(
              resultCard(
                { title: item.name || item.title, meta: item.url, thumbnail: item.thumbnail },
                function () {
                  onSelect(item.url);
                  close();
                }
              )
            );
          });
        });
        if (!any) results.appendChild(labelEl('No matches.'));
      }
      function load() {
        pbFetch(
          '/link-sources/?type=' +
            typeSel.value +
            '&search=' +
            encodeURIComponent(search.value || '')
        )
          .then(render)
          .catch(function () {
            results.innerHTML = '';
            results.appendChild(labelEl('Search failed.'));
          });
      }
      typeSel.addEventListener('change', load);
      search.addEventListener('input', debounce(load, 300));
      body.querySelector('.em-picker-url-apply').addEventListener('click', function () {
        var v = urlInput.value.trim();
        if (v) {
          onSelect(v);
          close();
        }
      });
      load();
      search.focus();
    });
  }

  // Voucher picker — select-existing only (creation lives in the vouchers admin).
  // Searches active vouchers via the marketing-gated voucher_search endpoint;
  // a manual-entry field still allows an externally-managed code.
  function openVoucherPicker(current, onSelect) {
    openPickerModal('<i class="fas fa-tag"></i> Choose a discount code', function (body, close) {
      body.innerHTML =
        '<input type="search" class="em-picker-search" placeholder="Search vouchers…">' +
        '<div class="em-picker-results" aria-live="polite"></div>' +
        '<div class="em-picker-url">' +
        '<label class="em-picker-url-label">Or enter a code manually</label>' +
        '<div class="em-picker-url-row">' +
        '<input type="text" class="em-picker-url-input" placeholder="e.g. SAVE10">' +
        '<button type="button" class="button em-picker-url-apply">Apply</button>' +
        '</div></div>';
      var search = body.querySelector('.em-picker-search');
      var results = body.querySelector('.em-picker-results');
      var manual = body.querySelector('.em-picker-url-input');
      if (current) manual.value = current;

      function render(vouchers) {
        results.innerHTML = '';
        if (!vouchers.length) {
          results.appendChild(labelEl('No vouchers found.'));
          return;
        }
        vouchers.forEach(function (v) {
          var meta = [v.summary, v.expiry ? 'Expires ' + v.expiry : ''].filter(Boolean).join(' · ');
          results.appendChild(
            resultCard(
              {
                title: v.code + (v.name ? ' — ' + v.name : ''),
                meta: meta,
                icon: 'fas fa-tag',
              },
              function () {
                onSelect(v.code);
                close();
              }
            )
          );
        });
      }
      function load() {
        api('/vouchers/?search=' + encodeURIComponent(search.value || ''), 'GET')
          .then(function (res) {
            render(res.vouchers || []);
          })
          .catch(function () {
            results.innerHTML = '';
            results.appendChild(labelEl('Search failed.'));
          });
      }
      search.addEventListener('input', debounce(load, 300));
      body.querySelector('.em-picker-url-apply').addEventListener('click', function () {
        var v = manual.value.trim();
        if (v) {
          onSelect(v);
          close();
        }
      });
      load();
      search.focus();
    });
  }

  function buildInput(prop, key, value) {
    var val = value == null ? '' : value;
    if (prop.type === 'select') {
      var sel = document.createElement('select');
      (prop.options || []).forEach(function (opt) {
        var o = document.createElement('option');
        o.value = opt.value;
        o.textContent = opt.label;
        if (opt.value === val) o.selected = true;
        sel.appendChild(o);
      });
      return sel;
    }
    if (prop.type === 'textarea') {
      var ta = document.createElement('textarea');
      ta.value = val;
      return ta;
    }
    var input = document.createElement('input');
    input.type = prop.type === 'color' ? 'color' : prop.type === 'url' ? 'url' : 'text';
    if (prop.type === 'color' && !val) input.value = '#000000';
    else input.value = val;
    return input;
  }

  // ---- State + persistence ----
  var blocks = initialBlocks.slice();

  function findBlock(id) {
    return blocks.filter(function (b) {
      return b.id === id;
    })[0];
  }

  function saveBlockContent(blockId) {
    var content = currentContent(blockId);
    setStatus('Saving…');
    api('/blocks/' + blockId + '/', 'PATCH', { content: content })
      .then(function (res) {
        var idx = blocks.findIndex(function (b) {
          return b.id === blockId;
        });
        if (idx >= 0) blocks[idx] = res.block;
        replaceBlockHtml(res.block);
        setStatus('Saved');
      })
      .catch(function () {
        setStatus('Save failed');
      });
  }

  function addBlock(blockType) {
    setStatus('Adding…');
    api('/blocks/', 'POST', { campaign_id: campaignId, block_type: blockType })
      .then(function (res) {
        blocks.push(res.block);
        renderBlock(res.block);
        selectBlock(res.block.id);
        setStatus('Added');
      })
      .catch(function () {
        setStatus('Failed to add block');
      });
  }

  function removeBlock(blockId) {
    api('/blocks/' + blockId + '/delete/', 'POST', {}).then(function () {
      blocks = blocks.filter(function (b) {
        return b.id !== blockId;
      });
      var wrap = canvas.querySelector('[data-block-id="' + blockId + '"]');
      if (wrap) wrap.remove();
      if (selectedId === blockId) {
        selectedId = null;
        propsForm.hidden = true;
        propsEmpty.hidden = false;
      }
      updateEmptyState();
    });
  }

  function persistOrder() {
    var order = Array.prototype.map.call(
      canvas.querySelectorAll('.em-block-wrapper'),
      function (w) {
        return w.dataset.blockId;
      }
    );
    api('/blocks/reorder/', 'POST', { campaign_id: campaignId, order: order });
  }

  function saveCampaign() {
    setStatus('Saving campaign…');
    api('/campaigns/' + campaignId + '/save/', 'POST', {})
      .then(function () {
        setStatus('Saved to email');
      })
      .catch(function () {
        setStatus('Save failed');
      });
  }

  // ---- Preview (compiled email in an isolated Shadow DOM) ----
  var previewShadow = null;

  function openPreview() {
    setStatus('Rendering preview…');
    api('/campaigns/' + campaignId + '/preview/', 'GET')
      .then(function (res) {
        var host = document.getElementById('em-preview-host');
        if (!previewShadow) previewShadow = host.attachShadow({ mode: 'open' });
        // Shadow DOM isolates the email's styles from the admin (and vice versa);
        // :host reset stops admin fonts/colours inheriting into the preview.
        previewShadow.innerHTML =
          '<style>:host{all:initial;display:block;}</style>' + (res.html || '');
        document.getElementById('em-preview-overlay').classList.add('active');
        document.body.classList.add('admin-modal-body-locked');
        setStatus('');
      })
      .catch(function () {
        setStatus('Preview failed');
      });
  }

  function closePreview() {
    document.getElementById('em-preview-overlay').classList.remove('active');
    document.body.classList.remove('admin-modal-body-locked');
  }

  // ---- Drag from palette ----
  function setupPalette() {
    document.querySelectorAll('.em-palette-item').forEach(function (item) {
      item.addEventListener('dragstart', function (e) {
        e.dataTransfer.setData('text/plain', item.dataset.blockType);
        e.dataTransfer.effectAllowed = 'copy';
        item.classList.add('is-dragging');
      });
      item.addEventListener('dragend', function () {
        item.classList.remove('is-dragging');
      });
      // Click also adds (accessibility / no-drag fallback).
      item.addEventListener('click', function () {
        addBlock(item.dataset.blockType);
      });
    });

    canvas.addEventListener('dragover', function (e) {
      e.preventDefault();
      e.dataTransfer.dropEffect = 'copy';
    });
    canvas.addEventListener('drop', function (e) {
      e.preventDefault();
      var blockType = e.dataTransfer.getData('text/plain');
      if (blockType && schemas[blockType]) addBlock(blockType);
    });
  }

  // ---- Helpers ----
  function debounce(fn, ms) {
    var t;
    return function () {
      var args = arguments,
        self = this;
      clearTimeout(t);
      t = setTimeout(function () {
        fn.apply(self, args);
      }, ms);
    };
  }
  function setStatus(msg) {
    if (saveStatus) saveStatus.textContent = msg;
  }

  // ---- Init ----
  function init() {
    initCanvas();
    applyThemeTokens();
    initialBlocks.forEach(renderBlock);
    updateEmptyState();
    setupPalette();

    if (window.Sortable) {
      window.Sortable.create(canvas, {
        handle: '.em-block-handle',
        draggable: '.em-block-wrapper',
        animation: 150,
        onEnd: persistOrder,
      });
    }

    document.querySelectorAll('[data-action="save"]').forEach(function (btn) {
      btn.addEventListener('click', saveCampaign);
    });
    document.querySelectorAll('[data-action="preview"]').forEach(function (btn) {
      btn.addEventListener('click', openPreview);
    });
    document.querySelectorAll('[data-action="close-preview"]').forEach(function (btn) {
      btn.addEventListener('click', closePreview);
    });
    var overlay = document.getElementById('em-preview-overlay');
    if (overlay) {
      overlay.addEventListener('click', function (e) {
        if (e.target === overlay) closePreview();
      });
    }
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closePreview();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
