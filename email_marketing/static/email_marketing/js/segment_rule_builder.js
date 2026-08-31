/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/*
 * Segment rule-builder — a visual editor for a Segment's `rules` JSON on the
 * admin change form. Replaces raw JSON editing with condition rows (field /
 * operator / value + match all|any) and a live recipient count. It writes the
 * serialised rules back into the hidden #id_rules field so the admin saves them.
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

  var FIELDS = readJSON('em-rule-fields', []);
  var OP_LABELS = readJSON('em-operator-labels', {});
  var cfg = readJSON('em-segment-config', {});
  if (!FIELDS.length) return;

  var fieldByKey = {};
  FIELDS.forEach(function (f) {
    fieldByKey[f.key] = f;
  });

  var rulesInput = document.getElementById('id_rules');
  if (!rulesInput) return;

  function csrf() {
    var i = document.querySelector('input[name=csrfmiddlewaretoken]');
    return i ? i.value : '';
  }

  function isBooleanField(f) {
    return f.operators.length === 1 && f.operators[0] === 'is_true';
  }

  // Parse the current rules JSON.
  var rules = { match: 'all', conditions: [] };
  try {
    var parsed = JSON.parse(rulesInput.value || '{}');
    if (parsed && typeof parsed === 'object') {
      rules.match = parsed.match === 'any' ? 'any' : 'all';
      rules.conditions = Array.isArray(parsed.conditions) ? parsed.conditions : [];
    }
  } catch (e) {
    /* keep defaults */
  }

  // Hide the raw JSON field's row; the builder replaces it.
  var row =
    rulesInput.closest('.form-row') || rulesInput.closest('.fieldBox') || rulesInput.parentElement;
  if (row) row.style.display = 'none';

  var box = document.createElement('div');
  box.className = 'em-rb';
  box.innerHTML =
    '<div class="em-rb-head">' +
    '<span class="em-rb-title">Audience rules</span>' +
    '<span class="em-rb-count" id="em-rb-count"></span>' +
    '</div>' +
    '<div class="em-rb-match">Match ' +
    '<select id="em-rb-match"><option value="all">all</option><option value="any">any</option></select>' +
    ' of the following conditions:</div>' +
    '<div class="em-rb-conditions" id="em-rb-conditions"></div>' +
    '<button type="button" class="button em-rb-add" id="em-rb-add">+ Add condition</button>';
  if (row && row.parentElement) {
    row.parentElement.insertBefore(box, row);
  } else {
    var form = document.querySelector('#content-main form');
    if (form) form.prepend(box);
  }

  var matchSel = box.querySelector('#em-rb-match');
  matchSel.value = rules.match;
  var condWrap = box.querySelector('#em-rb-conditions');
  var countEl = box.querySelector('#em-rb-count');

  function serialize() {
    var conditions = [];
    condWrap.querySelectorAll('.em-rb-cond').forEach(function (rowEl) {
      var key = rowEl.querySelector('[data-role=field]').value;
      var f = fieldByKey[key];
      if (!f) return;
      var cond = { field: key };
      var opEl = rowEl.querySelector('[data-role=op]');
      cond.op = opEl ? opEl.value : f.operators[0];
      if (!isBooleanField(f)) {
        var valEl = rowEl.querySelector('[data-role=value]');
        var val = valEl ? valEl.value : '';
        if (cond.op === 'in') {
          val = val
            .split(',')
            .map(function (s) {
              return s.trim();
            })
            .filter(Boolean);
        }
        cond.value = val;
      }
      conditions.push(cond);
    });
    var out = { match: matchSel.value, conditions: conditions };
    rulesInput.value = JSON.stringify(out);
    return out;
  }

  var timer;
  function scheduleCount() {
    clearTimeout(timer);
    timer = setTimeout(updateCount, 350);
  }

  function updateCount() {
    var payload = serialize();
    countEl.textContent = 'counting…';
    fetch(cfg.countUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf() },
      body: JSON.stringify({ rules: payload }),
    })
      .then(function (r) {
        return r.ok ? r.json() : Promise.reject();
      })
      .then(function (d) {
        countEl.textContent = d.count + ' matching subscriber' + (d.count === 1 ? '' : 's');
      })
      .catch(function () {
        countEl.textContent = '—';
      });
  }

  function buildOpSelect(f, cond) {
    var sel = document.createElement('select');
    sel.setAttribute('data-role', 'op');
    f.operators.forEach(function (op) {
      var o = document.createElement('option');
      o.value = op;
      o.textContent = OP_LABELS[op] || op;
      sel.appendChild(o);
    });
    if (cond.op) sel.value = cond.op;
    return sel;
  }

  function buildValueInput(f, cond) {
    var el;
    if (f.type === 'select') {
      el = document.createElement('select');
      (f.options || []).forEach(function (o) {
        var opt = document.createElement('option');
        opt.value = o.value;
        opt.textContent = o.label;
        el.appendChild(opt);
      });
      var v = Array.isArray(cond.value) ? cond.value[0] : cond.value;
      if (v) el.value = v;
    } else if (f.type === 'number') {
      el = document.createElement('input');
      el.type = 'number';
      el.value = cond.value != null ? cond.value : '';
    } else if (f.type === 'date') {
      el = document.createElement('input');
      el.type = 'date';
      el.value = cond.value || '';
    } else {
      el = document.createElement('input');
      el.type = 'text';
      el.value = cond.value != null ? cond.value : '';
    }
    el.setAttribute('data-role', 'value');
    return el;
  }

  function addRow(cond) {
    cond = cond || {};
    var f = fieldByKey[cond.field] || FIELDS[0];

    var rowEl = document.createElement('div');
    rowEl.className = 'em-rb-cond';

    var fieldSel = document.createElement('select');
    fieldSel.setAttribute('data-role', 'field');
    FIELDS.forEach(function (ff) {
      var o = document.createElement('option');
      o.value = ff.key;
      o.textContent = ff.label;
      fieldSel.appendChild(o);
    });
    fieldSel.value = f.key;
    rowEl.appendChild(fieldSel);

    var opHolder = document.createElement('span');
    opHolder.className = 'em-rb-op';
    rowEl.appendChild(opHolder);
    var valHolder = document.createElement('span');
    valHolder.className = 'em-rb-val';
    rowEl.appendChild(valHolder);

    var rm = document.createElement('button');
    rm.type = 'button';
    rm.className = 'em-rb-remove';
    rm.setAttribute('aria-label', 'Remove condition');
    rm.textContent = '×';
    rowEl.appendChild(rm);

    function renderFor(fKey, condData) {
      var ff = fieldByKey[fKey];
      opHolder.innerHTML = '';
      valHolder.innerHTML = '';
      if (!isBooleanField(ff)) {
        opHolder.appendChild(buildOpSelect(ff, condData));
        valHolder.appendChild(buildValueInput(ff, condData));
      }
    }
    renderFor(f.key, cond);

    fieldSel.addEventListener('change', function () {
      renderFor(fieldSel.value, {});
      scheduleCount();
    });
    rowEl.addEventListener('input', scheduleCount);
    rowEl.addEventListener('change', scheduleCount);
    rm.addEventListener('click', function () {
      rowEl.remove();
      scheduleCount();
    });

    condWrap.appendChild(rowEl);
  }

  (rules.conditions || []).forEach(addRow);
  box.querySelector('#em-rb-add').addEventListener('click', function () {
    addRow({});
    scheduleCount();
  });
  matchSel.addEventListener('change', scheduleCount);
  updateCount();
})();
