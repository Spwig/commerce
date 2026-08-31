/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/*
 * Journey Builder — a lightweight node/flowchart canvas.
 *
 * No third-party graph library: nodes are absolutely-positioned divs in a
 * pan/zoom "world" layer, edges are bezier <path>s in an SVG layer sharing the
 * same transform. Everything persists through the /api/email-marketing/journeys
 * endpoints. CSP-safe: data arrives via json_script, all behaviour is bound with
 * addEventListener, no inline handlers.
 */
(function () {
  'use strict';

  const API = '/api/email-marketing';
  const NODE_W = 210; // must match .jb-node width in the CSS

  // ---- data in (json_script islands) --------------------------------------
  function readJSON(id, fallback) {
    const el = document.getElementById(id);
    if (!el) return fallback;
    try {
      return JSON.parse(el.textContent);
    } catch (e) {
      return fallback;
    }
  }

  const config = readJSON('jb-config-data', {});
  const campaigns = readJSON('jb-campaigns-data', []);
  const segments = readJSON('jb-segments-data', []);
  const unitChoices = config.unit_choices || [
    { value: 'hours', label: 'hours' },
    { value: 'days', label: 'days' },
  ];

  const state = {
    nodes: readJSON('jb-nodes-data', []),
    edges: readJSON('jb-edges-data', []),
    selected: null,
    pan: { x: 0, y: 0 },
    scale: 1,
    counts: {}, // node_id -> subscribers currently at that node
    invalid: new Set(), // node ids flagged by the last validation
    status: config.status || 'draft',
  };

  // ---- CSRF + fetch --------------------------------------------------------
  function csrfToken() {
    const input = document.querySelector('#jb-csrf input[name=csrfmiddlewaretoken]');
    if (input) return input.value;
    const m = document.cookie.match(/csrftoken=([^;]+)/);
    return m ? m[1] : '';
  }

  async function api(path, method, body) {
    const res = await fetch(API + path, {
      method: method,
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken() },
      body: body ? JSON.stringify(body) : undefined,
    });
    if (!res.ok) throw new Error('API ' + method + ' ' + path + ' -> ' + res.status);
    return res.json();
  }

  function setStatus(text) {
    const el = document.getElementById('jb-save-status');
    if (el) el.textContent = text || '';
  }

  // ---- element refs --------------------------------------------------------
  const wrap = document.getElementById('jb-canvas-wrap');
  const world = document.getElementById('jb-canvas');
  const nodesLayer = document.getElementById('jb-nodes');
  const edgesSvg = document.getElementById('jb-edges');
  const emptyState = document.getElementById('jb-canvas-empty');

  const NODE_META = {
    entry: { icon: 'fas fa-bolt', label: 'Entry' },
    send_email: { icon: 'fas fa-envelope', label: 'Send email' },
    wait_delay: { icon: 'fas fa-clock', label: 'Wait' },
    branch: { icon: 'fas fa-code-branch', label: 'Branch' },
    exit: { icon: 'fas fa-flag-checkered', label: 'Exit' },
  };

  // ---- helpers -------------------------------------------------------------
  function getNode(id) {
    return state.nodes.find(n => n.id === id);
  }

  function campaignName(id) {
    const c = campaigns.find(x => x.id === id);
    return c ? c.name : null;
  }

  function segmentName(id) {
    const s = segments.find(x => x.id === id);
    return s ? s.name : null;
  }

  function nodeSummary(node) {
    const cfg = node.config || {};
    if (node.node_type === 'entry') return config.trigger || 'Journey start';
    if (node.node_type === 'send_email') {
      if (cfg.ab_winner_label) return 'A/B winner: Variant ' + cfg.ab_winner_label;
      if (cfg.ab_test_type === 'content') {
        return 'A/B · ' + (cfg.variant_campaign_ids || []).length + ' emails';
      }
      if (cfg.ab_test_type === 'subject') {
        return 'A/B · ' + (cfg.variant_subjects || []).length + ' subjects';
      }
      return campaignName(cfg.campaign_id) || 'No email chosen';
    }
    if (node.node_type === 'wait_delay') {
      if (!cfg.value) return 'No wait set';
      return 'Wait ' + cfg.value + ' ' + (cfg.unit || 'days');
    }
    if (node.node_type === 'branch') {
      const name = segmentName(cfg.segment_id);
      return name ? 'In segment: ' + name : 'No condition set';
    }
    if (node.node_type === 'exit') return 'Journey ends';
    return '';
  }

  // A node's connector ports in WORLD coordinates, read from the live DOM so
  // edges stay attached whatever a node's rendered height turns out to be.
  function nodePorts(node) {
    const el = nodesLayer.querySelector('[data-node-id="' + node.id + '"]');
    const w = el ? el.offsetWidth : NODE_W;
    const h = el ? el.offsetHeight : 70;
    const x = node.pos_x;
    const y = node.pos_y;
    const ports = { in: { x: x + w / 2, y: y } };
    if (node.node_type === 'branch') {
      ports.yes = { x: x + w * 0.3, y: y + h };
      ports.no = { x: x + w * 0.7, y: y + h };
    } else {
      ports.out = { x: x + w / 2, y: y + h };
    }
    return ports;
  }

  function outPort(node, branch) {
    const ports = nodePorts(node);
    if (node.node_type === 'branch') return branch === 'no' ? ports.no : ports.yes;
    return ports.out;
  }

  // ---- transform (pan/zoom) ------------------------------------------------
  function applyTransform() {
    world.style.transform =
      'translate(' + state.pan.x + 'px,' + state.pan.y + 'px) scale(' + state.scale + ')';
  }

  function screenToWorld(clientX, clientY) {
    const r = wrap.getBoundingClientRect();
    return {
      x: (clientX - r.left - state.pan.x) / state.scale,
      y: (clientY - r.top - state.pan.y) / state.scale,
    };
  }

  // ---- rendering -----------------------------------------------------------
  function bezier(a, b) {
    const dy = Math.max(40, Math.abs(b.y - a.y) / 2);
    return (
      'M ' +
      a.x +
      ' ' +
      a.y +
      ' C ' +
      a.x +
      ' ' +
      (a.y + dy) +
      ' ' +
      b.x +
      ' ' +
      (b.y - dy) +
      ' ' +
      b.x +
      ' ' +
      b.y
    );
  }

  function renderEdges() {
    edgesSvg.innerHTML = '';
    const NS = 'http://www.w3.org/2000/svg';
    state.edges.forEach(edge => {
      const from = getNode(edge.from);
      const to = getNode(edge.to);
      if (!from || !to) return;
      const a = outPort(from, edge.branch);
      const b = nodePorts(to).in;

      const path = document.createElementNS(NS, 'path');
      path.setAttribute('d', bezier(a, b));
      path.setAttribute('class', 'jb-edge jb-edge--' + edge.branch);
      path.setAttribute('data-edge-id', edge.id);
      edgesSvg.appendChild(path);

      if (edge.branch === 'yes' || edge.branch === 'no') {
        const label = document.createElementNS(NS, 'text');
        label.setAttribute('x', (a.x + b.x) / 2);
        label.setAttribute('y', (a.y + b.y) / 2);
        label.setAttribute('class', 'jb-edge-label jb-edge-label--' + edge.branch);
        label.textContent = edge.branch === 'yes' ? 'Yes' : 'No';
        edgesSvg.appendChild(label);
      }

      // An invisible fat hit-path so the thin edge is easy to click to delete.
      const hit = document.createElementNS(NS, 'path');
      hit.setAttribute('d', bezier(a, b));
      hit.setAttribute('class', 'jb-edge-hit');
      hit.setAttribute('data-edge-id', edge.id);
      hit.addEventListener('click', () => removeEdge(edge.id));
      edgesSvg.appendChild(hit);
    });
  }

  function portEl(kind, branch) {
    const p = document.createElement('div');
    p.className = 'jb-port jb-port--' + kind + (branch ? ' jb-port--' + branch : '');
    p.dataset.port = kind; // "in" or "out"
    if (branch) p.dataset.branch = branch;
    return p;
  }

  function renderNode(node) {
    const meta = NODE_META[node.node_type] || { icon: 'fas fa-circle', label: node.node_type };
    const el = document.createElement('div');
    el.className = 'jb-node jb-node--' + node.node_type;
    el.dataset.nodeId = node.id;
    el.style.left = node.pos_x + 'px';
    el.style.top = node.pos_y + 'px';
    if (state.selected === node.id) el.classList.add('is-selected');
    if (state.invalid.has(node.id)) el.classList.add('is-invalid');

    // Live enrollment count — how many subscribers are sitting at this step now.
    const count = state.counts[node.id];
    if (count) {
      const badge = document.createElement('span');
      badge.className = 'jb-node-count';
      badge.title = count + ' subscriber(s) here now';
      badge.textContent = count > 999 ? '999+' : String(count);
      el.appendChild(badge);
    }

    // Input port (all but entry).
    if (node.node_type !== 'entry') el.appendChild(portEl('in'));

    const head = document.createElement('div');
    head.className = 'jb-node-head';
    const icon = document.createElement('i');
    icon.className = meta.icon;
    const title = document.createElement('span');
    title.className = 'jb-node-title';
    title.textContent = meta.label;
    head.appendChild(icon);
    head.appendChild(title);
    el.appendChild(head);

    const summary = document.createElement('div');
    summary.className = 'jb-node-summary';
    summary.textContent = nodeSummary(node);
    el.appendChild(summary);

    // Output port(s).
    if (node.node_type === 'branch') {
      el.appendChild(portEl('out', 'yes'));
      el.appendChild(portEl('out', 'no'));
    } else if (node.node_type !== 'exit') {
      el.appendChild(portEl('out'));
    }

    return el;
  }

  function render() {
    nodesLayer.innerHTML = '';
    state.nodes.forEach(n => nodesLayer.appendChild(renderNode(n)));
    renderEdges();
    emptyState.hidden = state.nodes.length > 1; // >1 because entry always exists
    applyTransform();
  }

  // ---- node create / move / delete ----------------------------------------
  async function createNode(nodeType, worldX, worldY) {
    setStatus('Adding…');
    try {
      const res = await api('/journeys/' + config.journey_id + '/nodes/', 'POST', {
        node_type: nodeType,
        pos_x: Math.round(worldX - NODE_W / 2),
        pos_y: Math.round(worldY - 30),
        config: {},
      });
      state.nodes.push(res.node);
      render();
      selectNode(res.node.id);
      setStatus('Added');
    } catch (e) {
      setStatus("Couldn't add step");
    }
  }

  async function persistPosition(node) {
    try {
      await api('/journeys/nodes/' + node.id + '/', 'PATCH', {
        pos_x: Math.round(node.pos_x),
        pos_y: Math.round(node.pos_y),
      });
    } catch (e) {
      /* position is cosmetic; a failed save isn't worth interrupting the user */
    }
  }

  async function removeNode(id) {
    const node = getNode(id);
    if (!node || node.node_type === 'entry') return;
    setStatus('Removing…');
    try {
      await api('/journeys/nodes/' + id + '/delete/', 'DELETE');
      state.nodes = state.nodes.filter(n => n.id !== id);
      state.edges = state.edges.filter(e => e.from !== id && e.to !== id);
      if (state.selected === id) clearSelection();
      render();
      setStatus('Removed');
    } catch (e) {
      setStatus("Couldn't remove step");
    }
  }

  async function createEdge(fromId, toId, branch) {
    setStatus('Connecting…');
    try {
      const res = await api('/journeys/' + config.journey_id + '/edges/', 'POST', {
        from: fromId,
        to: toId,
        branch: branch,
      });
      // The server replaces any existing edge on this output slot; mirror that.
      state.edges = state.edges.filter(e => !(e.from === fromId && e.branch === branch));
      state.edges.push(res.edge);
      state.invalid = new Set(); // a new connection may resolve a flagged issue
      render();
      setStatus('Connected');
    } catch (e) {
      setStatus("Couldn't connect those steps");
    }
  }

  async function removeEdge(id) {
    try {
      await api('/journeys/edges/' + id + '/delete/', 'DELETE');
      state.edges = state.edges.filter(e => e.id !== id);
      render();
      setStatus('Disconnected');
    } catch (e) {
      setStatus("Couldn't disconnect");
    }
  }

  // ---- selection + config panel -------------------------------------------
  const configEmpty = document.getElementById('jb-config-empty');
  const configForm = document.getElementById('jb-config-form');

  function clearSelection() {
    state.selected = null;
    nodesLayer
      .querySelectorAll('.jb-node.is-selected')
      .forEach(n => n.classList.remove('is-selected'));
    configForm.hidden = true;
    configForm.innerHTML = '';
    configEmpty.hidden = false;
  }

  function selectNode(id) {
    state.selected = id;
    nodesLayer.querySelectorAll('.jb-node').forEach(n => {
      n.classList.toggle('is-selected', n.dataset.nodeId === id);
    });
    renderConfig(getNode(id));
  }

  function fieldRow(labelText, controlEl) {
    const row = document.createElement('div');
    row.className = 'jb-field';
    const label = document.createElement('label');
    label.textContent = labelText;
    row.appendChild(label);
    row.appendChild(controlEl);
    return row;
  }

  function selectControl(options, current, placeholder) {
    const sel = document.createElement('select');
    sel.className = 'jb-select';
    const blank = document.createElement('option');
    blank.value = '';
    blank.textContent = placeholder;
    sel.appendChild(blank);
    options.forEach(o => {
      const opt = document.createElement('option');
      opt.value = o.id !== undefined ? o.id : o.value;
      opt.textContent = o.name !== undefined ? o.name : o.label;
      if (opt.value === current) opt.selected = true;
      sel.appendChild(opt);
    });
    return sel;
  }

  async function saveConfig(node, newConfig) {
    node.config = newConfig;
    setStatus('Saving…');
    try {
      const res = await api('/journeys/nodes/' + node.id + '/', 'PATCH', { config: newConfig });
      node.config = res.node.config;
      state.invalid.delete(node.id); // configuring a step may clear its error
      render();
      selectNode(node.id); // re-open with the sanitised values
      setStatus('Saved');
    } catch (e) {
      setStatus("Couldn't save");
    }
  }

  // The send_email config panel: a single email, or an A/B test (content =
  // different emails, subject = different subject lines). A/B edits only persist
  // once at least two variants are set — saveConfig round-trips the sanitised
  // config, so a partial save would revert to a plain send.
  function renderSendEmail(node, cfg) {
    const AB_LABELS = ['A', 'B', 'C', 'D'];
    const box = document.createElement('div');
    let mode =
      cfg.ab_test_type === 'content' || cfg.ab_test_type === 'subject'
        ? cfg.ab_test_type
        : 'single';

    const typeSel = document.createElement('select');
    typeSel.className = 'jb-select';
    [
      ['single', 'Single email'],
      ['content', 'A/B: different emails'],
      ['subject', 'A/B: different subject lines'],
    ].forEach(function (pair) {
      const o = document.createElement('option');
      o.value = pair[0];
      o.textContent = pair[1];
      if (pair[0] === mode) o.selected = true;
      typeSel.appendChild(o);
    });
    typeSel.addEventListener('change', function () {
      mode = typeSel.value;
      renderMode();
    });
    box.appendChild(fieldRow('Step type', typeSel));

    const modeBox = document.createElement('div');
    box.appendChild(modeBox);
    let rowsBox = null;
    let metricSel = null;
    let baseSel = null;

    function makeMetric() {
      const m = selectControl(
        [
          { id: 'opens', name: 'Open rate' },
          { id: 'clicks', name: 'Click rate' },
        ],
        cfg.ab_metric === 'clicks' ? 'clicks' : 'opens',
        ''
      );
      if (m.options.length && m.options[0].value === '') m.remove(0);
      m.value = cfg.ab_metric === 'clicks' ? 'clicks' : 'opens';
      return m;
    }

    function variantRow(index, value) {
      const wrap = document.createElement('div');
      wrap.className = 'jb-inline-group jb-variant-row';
      const tag = document.createElement('span');
      tag.className = 'jb-variant-tag';
      tag.textContent = AB_LABELS[index];
      wrap.appendChild(tag);
      let control;
      if (mode === 'content') {
        control = selectControl(campaigns, value || '', 'Choose an email…');
      } else {
        control = document.createElement('input');
        control.type = 'text';
        control.className = 'jb-input';
        control.value = value || '';
        control.placeholder = 'Subject line ' + AB_LABELS[index];
      }
      control.classList.add('jb-variant-input');
      control.addEventListener('change', save);
      wrap.appendChild(control);
      return wrap;
    }

    function renderMode() {
      modeBox.innerHTML = '';
      rowsBox = metricSel = baseSel = null;
      if (mode === 'single') {
        const sel = selectControl(campaigns, cfg.campaign_id || '', 'Choose an email…');
        sel.addEventListener('change', function () {
          saveConfig(node, { campaign_id: sel.value });
        });
        modeBox.appendChild(fieldRow('Email to send', sel));
        return;
      }
      if (mode === 'subject') {
        baseSel = selectControl(campaigns, cfg.campaign_id || '', 'Choose the email…');
        baseSel.addEventListener('change', save);
        modeBox.appendChild(fieldRow('Email to send', baseSel));
      }
      rowsBox = document.createElement('div');
      const initial = (mode === 'content' ? cfg.variant_campaign_ids : cfg.variant_subjects) || [];
      const count = Math.max(2, initial.length);
      for (let i = 0; i < count; i++) rowsBox.appendChild(variantRow(i, initial[i]));
      modeBox.appendChild(
        fieldRow(mode === 'content' ? 'Email variants' : 'Subject variants', rowsBox)
      );

      const add = document.createElement('button');
      add.type = 'button';
      add.className = 'button jb-add-variant';
      add.textContent = '+ Add variant';
      add.addEventListener('click', function () {
        const n = rowsBox.querySelectorAll('.jb-variant-row').length;
        if (n < 4) rowsBox.appendChild(variantRow(n, ''));
      });
      modeBox.appendChild(add);

      metricSel = makeMetric();
      metricSel.addEventListener('change', save);
      modeBox.appendChild(fieldRow('Pick the winner by', metricSel));

      if (cfg.ab_winner_label) {
        const note = document.createElement('p');
        note.className = 'jb-config-note';
        const icon = document.createElement('i');
        icon.className = 'fas fa-trophy';
        note.appendChild(icon);
        note.appendChild(
          document.createTextNode(
            ' Winner locked: Variant ' + cfg.ab_winner_label + ' — every new enrollee now gets it.'
          )
        );
        modeBox.appendChild(note);
      }
      renderStats();
    }

    function currentValues() {
      return Array.prototype.map
        .call(rowsBox.querySelectorAll('.jb-variant-input'), function (el) {
          return (el.value || '').trim();
        })
        .filter(Boolean);
    }

    function save() {
      const vals = currentValues();
      if (vals.length < 2) {
        setStatus('Add at least two variants to A/B test');
        return;
      }
      // A subject test needs its base email first, or the server drops the whole
      // config and the re-render would wipe the subjects just typed.
      if (mode === 'subject' && !baseSel.value) {
        setStatus('Choose the email to send first');
        return;
      }
      if (mode === 'content') {
        saveConfig(node, {
          ab_test_type: 'content',
          variant_campaign_ids: vals,
          ab_metric: metricSel.value,
        });
      } else {
        saveConfig(node, {
          ab_test_type: 'subject',
          campaign_id: baseSel.value,
          variant_subjects: vals,
          ab_metric: metricSel.value,
        });
      }
    }

    function renderStats() {
      const s = state.ab && state.ab[node.id];
      if (!s || !s.variants) return;
      const panel = document.createElement('div');
      panel.className = 'jb-ab-stats';
      s.variants.forEach(function (v) {
        const row = document.createElement('div');
        row.className = 'jb-ab-stat-row' + (s.winner === v.label ? ' is-winner' : '');
        row.textContent =
          'Variant ' +
          v.label +
          ' — ' +
          v.recipients +
          ' sent · ' +
          v.open_rate +
          '% opens · ' +
          v.click_rate +
          '% clicks';
        panel.appendChild(row);
      });
      const verdict = document.createElement('div');
      verdict.className = 'jb-ab-verdict';
      if (s.winner) {
        verdict.textContent = 'Winner: Variant ' + s.winner + ' (locked in).';
      } else if (s.confidence != null) {
        verdict.textContent = 'Leading at ' + s.confidence + '% confidence (locks in at 95%).';
      } else {
        verdict.textContent = 'Not enough data yet to pick a winner.';
      }
      panel.appendChild(verdict);
      modeBox.appendChild(panel);
    }

    renderMode();
    return box;
  }

  function renderConfig(node) {
    if (!node) return;
    configEmpty.hidden = true;
    configForm.hidden = false;
    configForm.innerHTML = '';

    const meta = NODE_META[node.node_type];
    const heading = document.createElement('h2');
    heading.className = 'jb-config-title';
    heading.innerHTML = '<i class="' + meta.icon + '"></i> ';
    heading.appendChild(document.createTextNode(meta.label));
    configForm.appendChild(heading);
    const cfg = node.config || {};

    if (node.node_type === 'entry') {
      const p = document.createElement('p');
      p.className = 'jb-config-note';
      p.textContent =
        'Subscribers enter here when: ' + (config.trigger || 'the trigger fires') + '.';
      configForm.appendChild(p);
    } else if (node.node_type === 'send_email') {
      configForm.appendChild(renderSendEmail(node, cfg));
    } else if (node.node_type === 'wait_delay') {
      const num = document.createElement('input');
      num.type = 'number';
      num.min = '0';
      num.className = 'jb-input';
      num.value = cfg.value != null ? cfg.value : 1;
      const unit = selectControl(unitChoices, cfg.unit || 'days', '');
      // (selectControl adds a blank first option; remove it for a required unit)
      if (unit.options.length && unit.options[0].value === '') unit.remove(0);
      const commit = () =>
        saveConfig(node, { value: parseInt(num.value, 10) || 0, unit: unit.value });
      num.addEventListener('change', commit);
      unit.addEventListener('change', commit);
      const group = document.createElement('div');
      group.className = 'jb-inline-group';
      group.appendChild(num);
      group.appendChild(unit);
      configForm.appendChild(fieldRow('Wait for', group));
    } else if (node.node_type === 'branch') {
      const sel = selectControl(segments, cfg.segment_id || '', 'Choose a segment…');
      sel.addEventListener('change', () =>
        saveConfig(node, { condition: 'in_segment', segment_id: sel.value })
      );
      configForm.appendChild(fieldRow('If subscriber is in segment', sel));
      const note = document.createElement('p');
      note.className = 'jb-config-note';
      note.textContent = 'Members follow the Yes path; everyone else follows No.';
      configForm.appendChild(note);
    } else if (node.node_type === 'exit') {
      const p = document.createElement('p');
      p.className = 'jb-config-note';
      p.textContent = 'The journey ends here for the subscriber.';
      configForm.appendChild(p);
    }

    if (node.node_type !== 'entry') {
      const del = document.createElement('button');
      del.type = 'button';
      del.className = 'button jb-delete-node';
      del.innerHTML = '<i class="fas fa-trash"></i> Delete step';
      del.addEventListener('click', () => removeNode(node.id));
      configForm.appendChild(del);
    }
  }

  // ---- interactions: palette drag, node drag, connect, pan/zoom -----------
  let clickAddCount = 0;

  function bindPalette() {
    document.querySelectorAll('.jb-palette-item').forEach(btn => {
      btn.addEventListener('dragstart', e => {
        e.dataTransfer.setData('text/node-type', btn.dataset.nodeType);
        e.dataTransfer.effectAllowed = 'copy';
      });
      // Click also adds (keyboard/accessibility fallback). Cascade each add so
      // repeated clicks don't stack nodes on the exact same spot.
      btn.addEventListener('click', () => {
        const r = wrap.getBoundingClientRect();
        const step = (clickAddCount++ % 6) * 34;
        const p = screenToWorld(r.left + r.width / 2 + step, r.top + r.height / 3 + step);
        createNode(btn.dataset.nodeType, p.x, p.y);
      });
    });

    wrap.addEventListener('dragover', e => {
      e.preventDefault();
      e.dataTransfer.dropEffect = 'copy';
    });
    wrap.addEventListener('drop', e => {
      e.preventDefault();
      const type = e.dataTransfer.getData('text/node-type');
      if (!type) return;
      const p = screenToWorld(e.clientX, e.clientY);
      createNode(type, p.x, p.y);
    });
  }

  // Dragging a node body to reposition; dragging from an output port to connect.
  let drag = null; // { kind: 'node'|'connect', ... }
  let tempPath = null;

  function onPointerDown(e) {
    const portEl = e.target.closest('.jb-port--out');
    const nodeEl = e.target.closest('.jb-node');
    if (portEl && nodeEl) {
      const node = getNode(nodeEl.dataset.nodeId);
      drag = {
        kind: 'connect',
        from: node,
        branch: portEl.dataset.branch || 'default',
      };
      const NS = 'http://www.w3.org/2000/svg';
      tempPath = document.createElementNS(NS, 'path');
      tempPath.setAttribute('class', 'jb-edge jb-edge--temp');
      edgesSvg.appendChild(tempPath);
      e.preventDefault();
      return;
    }
    if (nodeEl && !e.target.closest('.jb-port')) {
      const node = getNode(nodeEl.dataset.nodeId);
      const start = screenToWorld(e.clientX, e.clientY);
      drag = {
        kind: 'node',
        node: node,
        el: nodeEl,
        offset: { x: start.x - node.pos_x, y: start.y - node.pos_y },
        moved: false,
      };
      nodeEl.classList.add('is-dragging');
      e.preventDefault();
      return;
    }
    // Empty canvas → pan.
    if (e.target === wrap || e.target === world || e.target === edgesSvg) {
      drag = { kind: 'pan', start: { x: e.clientX - state.pan.x, y: e.clientY - state.pan.y } };
    }
  }

  function onPointerMove(e) {
    if (!drag) return;
    if (drag.kind === 'node') {
      const p = screenToWorld(e.clientX, e.clientY);
      drag.node.pos_x = p.x - drag.offset.x;
      drag.node.pos_y = p.y - drag.offset.y;
      drag.el.style.left = drag.node.pos_x + 'px';
      drag.el.style.top = drag.node.pos_y + 'px';
      drag.moved = true;
      renderEdges();
    } else if (drag.kind === 'connect') {
      const a = outPort(drag.from, drag.branch);
      const b = screenToWorld(e.clientX, e.clientY);
      tempPath.setAttribute('d', bezier(a, b));
    } else if (drag.kind === 'pan') {
      state.pan.x = e.clientX - drag.start.x;
      state.pan.y = e.clientY - drag.start.y;
      applyTransform();
    }
  }

  function onPointerUp(e) {
    if (!drag) return;
    if (drag.kind === 'node') {
      drag.el.classList.remove('is-dragging');
      if (drag.moved) persistPosition(drag.node);
      else selectNode(drag.node.id);
    } else if (drag.kind === 'connect') {
      if (tempPath) tempPath.remove();
      tempPath = null;
      const targetNode = e.target.closest('.jb-node');
      const inPort = e.target.closest('.jb-port--in');
      if (targetNode && inPort && targetNode.dataset.nodeId !== drag.from.id) {
        createEdge(drag.from.id, targetNode.dataset.nodeId, drag.branch);
      }
    }
    drag = null;
  }

  function bindZoom() {
    wrap.addEventListener(
      'wheel',
      e => {
        e.preventDefault();
        const factor = e.deltaY < 0 ? 1.1 : 0.9;
        const next = Math.min(2, Math.max(0.4, state.scale * factor));
        // Zoom toward the cursor.
        const r = wrap.getBoundingClientRect();
        const cx = e.clientX - r.left;
        const cy = e.clientY - r.top;
        state.pan.x = cx - ((cx - state.pan.x) * next) / state.scale;
        state.pan.y = cy - ((cy - state.pan.y) * next) / state.scale;
        state.scale = next;
        applyTransform();
      },
      { passive: false }
    );
  }

  function fitToView() {
    if (!state.nodes.length) return;
    const xs = state.nodes.map(n => n.pos_x);
    const ys = state.nodes.map(n => n.pos_y);
    const minX = Math.min(...xs) - 40;
    const minY = Math.min(...ys) - 40;
    state.scale = 1;
    state.pan.x = -minX;
    state.pan.y = -minY;
    applyTransform();
  }

  // ---- starters + import / export -----------------------------------------
  function replaceGraph(graph) {
    state.nodes = graph.nodes || [];
    state.edges = graph.edges || [];
    clearSelection();
    render();
    fitToView();
  }

  function hasRealContent() {
    // More than the lone entry node → applying/importing would discard work.
    return state.nodes.filter(n => n.node_type !== 'entry').length > 0;
  }

  const templateOverlay = document.getElementById('jb-template-overlay');
  const templateGrid = document.getElementById('jb-template-grid');
  let templatesLoaded = false;

  async function openTemplates() {
    templateOverlay.classList.add('active');
    if (templatesLoaded) return;
    try {
      const res = await api('/journeys/templates/', 'GET');
      templateGrid.innerHTML = '';
      (res.templates || []).forEach(t => {
        const card = document.createElement('button');
        card.type = 'button';
        card.className = 'jb-template-card';
        const icon = document.createElement('i');
        icon.className = t.icon || 'fas fa-diagram-project';
        const title = document.createElement('span');
        title.className = 'jb-template-card-name';
        title.textContent = t.name;
        const desc = document.createElement('span');
        desc.className = 'jb-template-card-desc';
        desc.textContent = t.description || '';
        card.appendChild(icon);
        card.appendChild(title);
        card.appendChild(desc);
        card.addEventListener('click', () => applyTemplate(t.key));
        templateGrid.appendChild(card);
      });
      templatesLoaded = true;
    } catch (e) {
      templateGrid.textContent = 'Could not load templates.';
    }
  }

  function closeTemplates() {
    templateOverlay.classList.remove('active');
  }

  async function applyTemplate(key) {
    if (
      hasRealContent() &&
      !window.confirm('Start from this template? It replaces the current flow.')
    ) {
      return;
    }
    setStatus('Applying template…');
    try {
      const res = await api('/journeys/' + config.journey_id + '/apply-template/', 'POST', {
        template_key: key,
      });
      replaceGraph(res.graph);
      closeTemplates();
      setStatus(unmatchedNote(res.stats));
    } catch (e) {
      setStatus("Couldn't apply template");
    }
  }

  function unmatchedNote(stats) {
    if (stats && stats.unmatched) {
      return stats.unmatched + ' step(s) need an email or segment';
    }
    return 'Template applied';
  }

  async function exportJourney() {
    setStatus('Exporting…');
    try {
      const res = await fetch(API + '/journeys/' + config.journey_id + '/export/', {
        headers: { 'X-CSRFToken': csrfToken() },
      });
      if (!res.ok) throw new Error('export failed');
      const doc = await res.json();
      const blob = new Blob([JSON.stringify(doc, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      const slug =
        (doc.name || 'journey')
          .replace(/[^a-z0-9]+/gi, '-')
          .replace(/^-+|-+$/g, '')
          .toLowerCase() || 'journey';
      a.download = slug + '.journey.json';
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
      setStatus('Exported');
    } catch (e) {
      setStatus("Couldn't export");
    }
  }

  function triggerImport() {
    if (
      hasRealContent() &&
      !window.confirm('Import a journey file? It replaces the current flow.')
    ) {
      return;
    }
    document.getElementById('jb-import-file').click();
  }

  async function onImportFile(e) {
    const file = e.target.files && e.target.files[0];
    e.target.value = ''; // allow re-importing the same file later
    if (!file) return;
    setStatus('Importing…');
    let doc;
    try {
      doc = JSON.parse(await file.text());
    } catch (err) {
      setStatus('That file is not valid JSON');
      return;
    }
    try {
      const res = await api('/journeys/' + config.journey_id + '/import/', 'POST', { doc: doc });
      replaceGraph(res.graph);
      setStatus(unmatchedNote(res.stats));
    } catch (err) {
      setStatus("That file isn't a Spwig journey");
    }
  }

  // ---- live counts --------------------------------------------------------
  async function refreshStats() {
    try {
      const res = await api('/journeys/' + config.journey_id + '/node-stats/', 'GET');
      state.counts = res.counts || {};
      state.ab = res.ab || {};
      render();
    } catch (e) {
      /* counts are informational — a failed refresh shouldn't disrupt editing */
    }
  }

  // ---- status + validation (Activate gate) --------------------------------
  const statusPill = document.getElementById('jb-status-pill');
  const statusBtn = document.getElementById('jb-status-btn');
  const issuesBar = document.getElementById('jb-issues');
  const issuesList = document.getElementById('jb-issues-list');
  const issuesTitle = document.getElementById('jb-issues-title');

  const STATUS_LABEL = { draft: 'Draft', active: 'Active', paused: 'Paused' };

  function renderStatus() {
    const s = state.status;
    statusPill.textContent = STATUS_LABEL[s] || s;
    statusPill.className = 'jb-status-pill jb-status-pill--' + s;
    if (s === 'active') {
      statusBtn.innerHTML = '<i class="fas fa-pause"></i> Pause';
      statusBtn.classList.remove('btn-success');
    } else {
      statusBtn.innerHTML = '<i class="fas fa-play"></i> Activate';
      statusBtn.classList.add('btn-success');
    }
  }

  function clearInvalid() {
    if (state.invalid.size) {
      state.invalid = new Set();
      render();
    }
  }

  function showIssues(issues) {
    const errors = issues.filter(i => i.level === 'error');
    const warnings = issues.filter(i => i.level === 'warning');
    state.invalid = new Set(issues.filter(i => i.node_id).map(i => i.node_id));

    issuesList.innerHTML = '';
    issues.forEach(issue => {
      const li = document.createElement('li');
      li.className = 'jb-issue jb-issue--' + issue.level;
      const icon = document.createElement('i');
      icon.className =
        issue.level === 'error' ? 'fas fa-circle-exclamation' : 'fas fa-triangle-exclamation';
      const text = document.createElement('span');
      text.textContent = issue.message;
      li.appendChild(icon);
      li.appendChild(text);
      if (issue.node_id) {
        li.classList.add('jb-issue--clickable');
        li.addEventListener('click', () => {
          selectNode(issue.node_id);
          const el = nodesLayer.querySelector('[data-node-id="' + issue.node_id + '"]');
          if (el) el.scrollIntoView({ block: 'center', inline: 'center' });
        });
      }
      issuesList.appendChild(li);
    });

    const parts = [];
    if (errors.length) parts.push(errors.length + ' problem(s) to fix before activating');
    if (warnings.length) parts.push(warnings.length + ' warning(s)');
    issuesTitle.textContent = parts.join(' · ') || 'No issues';
    issuesBar.hidden = false;
    render(); // repaint so invalid nodes get their ring
  }

  function closeIssues() {
    issuesBar.hidden = true;
    clearInvalid();
  }

  async function toggleStatus() {
    const next = state.status === 'active' ? 'paused' : 'active';
    setStatus(next === 'active' ? 'Checking…' : 'Pausing…');
    try {
      const res = await api('/journeys/' + config.journey_id + '/status/', 'POST', {
        status: next,
      });
      if (res.success) {
        state.status = res.status;
        renderStatus();
        closeIssues();
        setStatus(next === 'active' ? 'Journey is live' : 'Journey paused');
      } else if (res.blocked) {
        showIssues(res.issues || []);
        setStatus("Can't activate yet");
      }
    } catch (e) {
      setStatus("Couldn't change status");
    }
  }

  // ---- init ----------------------------------------------------------------
  function init() {
    bindPalette();
    bindZoom();
    wrap.addEventListener('pointerdown', onPointerDown);
    window.addEventListener('pointermove', onPointerMove);
    window.addEventListener('pointerup', onPointerUp);

    const actions = {
      fit: fitToView,
      templates: openTemplates,
      'close-templates': closeTemplates,
      export: exportJourney,
      import: triggerImport,
      'toggle-status': toggleStatus,
      'close-issues': closeIssues,
    };
    Object.keys(actions).forEach(name => {
      document.querySelectorAll('[data-action="' + name + '"]').forEach(btn => {
        btn.addEventListener('click', actions[name]);
      });
    });
    document.getElementById('jb-import-file').addEventListener('change', onImportFile);
    templateOverlay.addEventListener('click', e => {
      if (e.target === templateOverlay) closeTemplates();
    });

    // Click empty canvas to deselect.
    wrap.addEventListener('click', e => {
      if (e.target === wrap || e.target === world || e.target === edgesSvg) clearSelection();
    });

    renderStatus();
    render();
    fitToView();
    refreshStats();
    // Refresh live counts when the tab regains focus (cheap, no polling).
    window.addEventListener('focus', refreshStats);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
