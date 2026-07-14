/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Rule Builder - Visual Drag-and-Drop Visibility Rule Editor
 * Follows rules_llm.md: Modular class-based structure
 */

class RuleBuilder {
  constructor() {
    const configEl = document.getElementById('rule-builder-config');
    if (configEl) {
      try {
        this.config = JSON.parse(configEl.textContent);
      } catch (e) {
        this.config = {};
      }
    } else {
      this.config = window.RuleBuilderConfig || {};
    }
    this.groupId = this.config.groupId;
    this.groupName = this.config.groupName || '';
    this.logicOperator = this.config.logicOperator || 'AND';
    this.rulesTree = this.config.initialRulesTree || [];
    this.savedRules = this.config.savedRules || [];
    this.selectedRule = null;
    this.sortableInstances = [];

    // Undo/Redo stack
    this.history = [];
    this.historyIndex = -1;
    this.maxHistorySize = 50;

    // Track unsaved changes
    this.hasUnsavedChanges = false;

    // Popup mode flag
    this.isPopupMode = document
      .querySelector('.rule-builder-container')
      ?.classList.contains('popup-mode');

    this.init();
  }

  init() {
    this.bindEvents();
    this.renderRulesTree();
    this.initSortable();
    this.saveHistoryState();
  }

  // =========================================
  // Event Binding
  // =========================================

  bindEvents() {
    // Group selector
    const groupSelector = document.getElementById('group-selector');
    if (groupSelector) {
      groupSelector.addEventListener('change', e => this.switchGroup(e.target.value));
    }

    // Save button
    const saveBtn = document.getElementById('save-btn');
    if (saveBtn) {
      saveBtn.addEventListener('click', () => this.saveGroup());
    }

    // Undo/Redo buttons
    const undoBtn = document.getElementById('undo-btn');
    const redoBtn = document.getElementById('redo-btn');
    if (undoBtn) undoBtn.addEventListener('click', () => this.undo());
    if (redoBtn) redoBtn.addEventListener('click', () => this.redo());

    // Expand/Collapse all
    const expandAllBtn = document.getElementById('expand-all-btn');
    const collapseAllBtn = document.getElementById('collapse-all-btn');
    if (expandAllBtn) expandAllBtn.addEventListener('click', () => this.expandAllGroups());
    if (collapseAllBtn) collapseAllBtn.addEventListener('click', () => this.collapseAllGroups());

    // Add rule buttons
    const addFirstRuleBtn = document.getElementById('add-first-rule-btn');
    const addRuleBtn = document.getElementById('add-rule-btn');
    if (addFirstRuleBtn) addFirstRuleBtn.addEventListener('click', () => this.showAddRuleModal());
    if (addRuleBtn) addRuleBtn.addEventListener('click', () => this.showAddRuleModal());

    // New group button
    const newGroupBtn = document.getElementById('new-group-btn');
    if (newGroupBtn) {
      newGroupBtn.addEventListener('click', () => this.showNewGroupModal());
    }

    // Logic toggle buttons
    document.querySelectorAll('.logic-toggle').forEach(btn => {
      btn.addEventListener('click', e =>
        this.setLogicOperator(e.target.closest('.logic-toggle').dataset.logic)
      );
    });

    // Group name input
    const groupNameInput = document.getElementById('group-name-input');
    if (groupNameInput) {
      groupNameInput.addEventListener('input', e => {
        this.groupName = e.target.value;
        this.hasUnsavedChanges = true;
        // Sync with info panel
        const infoGroupName = document.getElementById('info-group-name');
        if (infoGroupName) infoGroupName.value = e.target.value;
      });
    }

    // Group active toggle
    const groupActive = document.getElementById('group-active');
    if (groupActive) {
      groupActive.addEventListener('change', () => {
        this.hasUnsavedChanges = true;
      });
    }

    // Preview toggle
    const togglePreviewBtn = document.getElementById('toggle-preview-btn');
    const closePreviewBtn = document.getElementById('close-preview-btn');
    const runPreviewBtn = document.getElementById('run-preview-btn');
    if (togglePreviewBtn) {
      togglePreviewBtn.addEventListener('click', () => this.togglePreview());
    }
    if (closePreviewBtn) {
      closePreviewBtn.addEventListener('click', () => this.hidePreview());
    }
    if (runPreviewBtn) {
      runPreviewBtn.addEventListener('click', () => this.runPreview());
    }

    // Library section toggles
    document.querySelectorAll('.library-section-header').forEach(header => {
      header.addEventListener('click', () => this.toggleLibrarySection(header));
    });

    // Library search
    const librarySearch = document.getElementById('library-search');
    if (librarySearch) {
      librarySearch.addEventListener('input', e => this.filterLibrary(e.target.value));
    }

    // Saved rules search
    const savedRulesSearch = document.getElementById('saved-rules-search');
    if (savedRulesSearch) {
      savedRulesSearch.addEventListener('input', e => this.filterSavedRules(e.target.value));
    }

    // Tab switching
    document.querySelectorAll('.admin-tab-btn').forEach(btn => {
      btn.addEventListener('click', () => this.switchTab(btn.dataset.tab));
    });

    // Modal events
    this.bindModalEvents();

    // Keyboard shortcuts
    document.addEventListener('keydown', e => this.handleKeyboard(e));

    // Warn on unsaved changes
    window.addEventListener('beforeunload', e => {
      if (this.hasUnsavedChanges) {
        e.preventDefault();
        e.returnValue = '';
      }
    });

    // Draggable library items
    this.bindLibraryDragEvents();

    // Info panel sync
    this.bindInfoPanelEvents();
  }

  bindLibraryDragEvents() {
    document.querySelectorAll('.library-item.draggable-item').forEach(item => {
      item.addEventListener('dragstart', e => {
        const dragData = JSON.stringify({
          type: item.dataset.type,
          ruleType: item.dataset.ruleType || null,
          ruleId: item.dataset.ruleId || null,
          logic: item.dataset.logic || null,
        });
        e.dataTransfer.setData('application/x-rule-item', dragData);
        e.dataTransfer.setData('text/plain', dragData);
        e.dataTransfer.effectAllowed = 'copy';
        item.classList.add('dragging');
        document.querySelector('.rule-builder-container')?.classList.add('is-dragging');
      });

      item.addEventListener('dragend', () => {
        item.classList.remove('dragging');
        document.querySelector('.rule-builder-container')?.classList.remove('is-dragging');
      });
    });

    // Drop zone for rule tree
    const ruleTree = document.getElementById('rule-tree');
    if (ruleTree) {
      ruleTree.addEventListener('dragover', e => {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'copy';
        ruleTree.classList.add('drag-over');
      });

      ruleTree.addEventListener('dragleave', e => {
        if (!ruleTree.contains(e.relatedTarget)) {
          ruleTree.classList.remove('drag-over');
        }
      });

      ruleTree.addEventListener('drop', e => {
        e.preventDefault();
        ruleTree.classList.remove('drag-over');

        let rawData = e.dataTransfer.getData('application/x-rule-item');
        if (!rawData) {
          rawData = e.dataTransfer.getData('text/plain');
        }

        if (!rawData || !rawData.startsWith('{')) {
          console.warn('Invalid drop data');
          return;
        }

        try {
          const data = JSON.parse(rawData);
          this.handleLibraryDrop(data);
        } catch (err) {
          console.error('Drop error:', err);
        }
      });
    }
  }

  bindModalEvents() {
    // Add Rule Modal
    const closeAddRuleModal = document.getElementById('close-add-rule-modal');
    const cancelAddRuleBtn = document.getElementById('cancel-add-rule-btn');
    const confirmAddRuleBtn = document.getElementById('confirm-add-rule-btn');

    if (closeAddRuleModal)
      closeAddRuleModal.addEventListener('click', () => this.hideAddRuleModal());
    if (cancelAddRuleBtn) cancelAddRuleBtn.addEventListener('click', () => this.hideAddRuleModal());
    if (confirmAddRuleBtn) confirmAddRuleBtn.addEventListener('click', () => this.confirmAddRule());

    // New Group Modal
    const closeNewGroupModal = document.getElementById('close-new-group-modal');
    const cancelNewGroupBtn = document.getElementById('cancel-new-group-btn');
    const confirmNewGroupBtn = document.getElementById('confirm-new-group-btn');

    if (closeNewGroupModal)
      closeNewGroupModal.addEventListener('click', () => this.hideNewGroupModal());
    if (cancelNewGroupBtn)
      cancelNewGroupBtn.addEventListener('click', () => this.hideNewGroupModal());
    if (confirmNewGroupBtn)
      confirmNewGroupBtn.addEventListener('click', () => this.createNewGroup());

    // Delete Confirmation Modal
    const closeDeleteModal = document.getElementById('close-delete-modal');
    const cancelDeleteBtn = document.getElementById('cancel-delete-btn');
    const confirmDeleteBtn = document.getElementById('confirm-delete-btn');

    if (closeDeleteModal) closeDeleteModal.addEventListener('click', () => this.hideDeleteModal());
    if (cancelDeleteBtn) cancelDeleteBtn.addEventListener('click', () => this.hideDeleteModal());
    if (confirmDeleteBtn) confirmDeleteBtn.addEventListener('click', () => this.confirmDelete());

    // Click outside modal to close
    document.querySelectorAll('.modal-overlay').forEach(overlay => {
      overlay.addEventListener('click', e => {
        if (e.target === overlay) {
          overlay.classList.add('hidden');
        }
      });
    });
  }

  bindInfoPanelEvents() {
    // Sync info panel changes to main state
    const infoGroupName = document.getElementById('info-group-name');
    const infoGroupDescription = document.getElementById('info-group-description');
    const infoLogicOperator = document.getElementById('info-logic-operator');
    const infoGroupActive = document.getElementById('info-group-active');

    if (infoGroupName) {
      infoGroupName.addEventListener('input', e => {
        this.groupName = e.target.value;
        document.getElementById('group-name-input').value = e.target.value;
        this.hasUnsavedChanges = true;
      });
    }

    if (infoGroupDescription) {
      infoGroupDescription.addEventListener('input', () => {
        this.hasUnsavedChanges = true;
      });
    }

    if (infoLogicOperator) {
      infoLogicOperator.addEventListener('change', e => {
        this.setLogicOperator(e.target.value);
      });
    }

    if (infoGroupActive) {
      infoGroupActive.addEventListener('change', e => {
        document.getElementById('group-active').checked = e.target.checked;
        this.hasUnsavedChanges = true;
      });
    }
  }

  // =========================================
  // Rules Tree Rendering
  // =========================================

  renderRulesTree() {
    const container = document.getElementById('rule-tree');
    const emptyState = document.getElementById('rule-tree-empty');
    const addRuleFooter = document.getElementById('add-rule-footer');

    if (!container) return;

    // Clear existing content (except empty state)
    container.querySelectorAll('.rule-card, .nested-group-card').forEach(el => el.remove());

    if (this.rulesTree.length === 0) {
      if (emptyState) emptyState.style.display = 'flex';
      if (addRuleFooter) addRuleFooter.style.display = 'none';
    } else {
      if (emptyState) emptyState.style.display = 'none';
      if (addRuleFooter) addRuleFooter.style.display = 'block';

      const fragment = document.createDocumentFragment();
      this.rulesTree.forEach((item, index) => {
        if (item.type === 'group') {
          fragment.appendChild(this.createGroupElement(item, index));
        } else {
          fragment.appendChild(this.createRuleElement(item, index));
        }
      });
      container.appendChild(fragment);

      // Reinitialize sortable
      this.initSortable();
    }

    // Update rule count badge
    this.updateRuleCount();
  }

  createRuleElement(rule, index) {
    const div = document.createElement('div');
    div.className = 'rule-card';
    div.dataset.ruleId = rule.id || `temp-${Date.now()}-${index}`;
    div.dataset.ruleType = rule.rule_type;

    if (rule.id === this.selectedRule?.id) {
      div.classList.add('selected');
    }

    if (!rule.is_active) {
      div.classList.add('disabled');
    }

    const icon = this.getRuleIcon(rule.rule_type);
    const operatorClass = `operator-${rule.operator}`;
    const operatorLabel = this.config.operatorLabels[rule.operator] || rule.operator;
    const typeLabel = this.config.ruleTypeLabels[rule.rule_type] || rule.rule_type;
    const valueDisplay = this.formatRuleValue(rule.value);

    div.innerHTML = `
            <div class="rule-card-drag-handle">
                <i class="fas fa-grip-vertical"></i>
            </div>
            <div class="rule-card-content">
                <div class="rule-card-header">
                    <div class="rule-card-icon">
                        <i class="fas ${icon}"></i>
                    </div>
                    <div class="rule-card-title">
                        <span class="rule-name">${this.escapeHtml(rule.name || 'Unnamed Rule')}</span>
                        <span class="rule-type-badge">${typeLabel}</span>
                    </div>
                </div>
                <div class="rule-card-condition">
                    <span class="condition-type">${typeLabel}</span>
                    <span class="condition-operator ${operatorClass}">${operatorLabel}</span>
                    <span class="condition-value">${valueDisplay}</span>
                </div>
                ${rule.description ? `<div class="rule-card-description">${this.escapeHtml(rule.description)}</div>` : ''}
            </div>
            <div class="rule-card-actions">
                <button class="rule-card-action" data-action="toggle" title="${rule.is_active ? 'Disable Rule' : 'Enable Rule'}">
                    <i class="fas ${rule.is_active ? 'fa-toggle-on' : 'fa-toggle-off'}"></i>
                </button>
                <button class="rule-card-action" data-action="edit" title="Edit Rule">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="rule-card-action rule-card-action-danger" data-action="delete" title="Remove Rule">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            ${!rule.is_active ? '<div class="rule-card-disabled-overlay"><span>Disabled</span></div>' : ''}
        `;

    // Bind events
    div.addEventListener('click', e => {
      if (!e.target.closest('.rule-card-action')) {
        this.selectRule(rule);
      }
    });

    div.querySelectorAll('.rule-card-action').forEach(btn => {
      btn.addEventListener('click', e => {
        e.stopPropagation();
        const action = btn.dataset.action;
        if (action === 'toggle') this.toggleRuleActive(rule);
        else if (action === 'edit') this.editRule(rule);
        else if (action === 'delete') this.showDeleteConfirm(rule);
      });
    });

    return div;
  }

  createGroupElement(group, index) {
    const div = document.createElement('div');
    div.className = 'nested-group-card';
    div.dataset.groupId = group.id || `temp-group-${Date.now()}-${index}`;
    div.dataset.logic = group.logic_operator;

    const rulesCount = (group.rules || []).length;

    div.innerHTML = `
            <div class="nested-group-header">
                <div class="nested-group-drag-handle">
                    <i class="fas fa-grip-vertical"></i>
                </div>
                <div class="nested-group-info">
                    <span class="nested-group-name">${this.escapeHtml(group.name || 'Nested Group')}</span>
                    <span class="logic-badge ${group.logic_operator === 'OR' ? 'logic-or' : ''}">${group.logic_operator}</span>
                    <span class="nested-group-count">${rulesCount} rules</span>
                </div>
                <div class="nested-group-actions">
                    <button class="nested-group-action" data-action="toggle-collapse" title="Expand/Collapse">
                        <i class="fas fa-chevron-down"></i>
                    </button>
                    <button class="nested-group-action" data-action="toggle-logic" title="Toggle AND/OR">
                        <i class="fas fa-random"></i>
                    </button>
                    <button class="nested-group-action" data-action="edit" title="Edit Group">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="nested-group-action nested-group-action-danger" data-action="delete" title="Delete Group">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
            <div class="nested-group-content">
                <div class="nested-group-rules" id="nested-rules-${group.id || index}">
                    <!-- Child rules rendered here -->
                </div>
                <div class="nested-group-dropzone" data-drop-target="group-${group.id || index}">
                    <span><i class="fas fa-plus"></i> Drop rules here</span>
                </div>
            </div>
        `;

    // Render child rules
    const rulesContainer = div.querySelector('.nested-group-rules');
    if (group.rules && group.rules.length > 0) {
      group.rules.forEach((rule, i) => {
        rulesContainer.appendChild(this.createRuleElement(rule, i));
      });
    }

    // Bind events
    div.querySelectorAll('.nested-group-action').forEach(btn => {
      btn.addEventListener('click', e => {
        e.stopPropagation();
        const action = btn.dataset.action;
        if (action === 'toggle-collapse') this.toggleGroupCollapse(div);
        else if (action === 'toggle-logic') this.toggleGroupLogic(group, div);
        else if (action === 'edit') this.editGroup(group);
        else if (action === 'delete') this.showDeleteConfirm(group, true);
      });
    });

    // Drop zone events
    const dropzone = div.querySelector('.nested-group-dropzone');
    if (dropzone) {
      dropzone.addEventListener('dragover', e => {
        e.preventDefault();
        e.stopPropagation();
        dropzone.classList.add('drag-over');
      });

      dropzone.addEventListener('dragleave', () => {
        dropzone.classList.remove('drag-over');
      });

      dropzone.addEventListener('drop', e => {
        e.preventDefault();
        e.stopPropagation();
        dropzone.classList.remove('drag-over');

        const rawData =
          e.dataTransfer.getData('application/x-rule-item') || e.dataTransfer.getData('text/plain');

        if (rawData && rawData.startsWith('{')) {
          try {
            const data = JSON.parse(rawData);
            this.handleLibraryDrop(data, group);
          } catch (err) {
            console.error('Drop error:', err);
          }
        }
      });
    }

    return div;
  }

  // =========================================
  // Sortable Initialization
  // =========================================

  initSortable() {
    // Destroy existing instances
    this.sortableInstances.forEach(instance => instance.destroy());
    this.sortableInstances = [];

    // Main rule tree
    const ruleTree = document.getElementById('rule-tree');
    if (ruleTree) {
      const sortable = new Sortable(ruleTree, {
        group: 'rules',
        animation: 150,
        handle: '.rule-card-drag-handle, .nested-group-drag-handle',
        draggable: '.rule-card, .nested-group-card',
        ghostClass: 'sortable-ghost',
        chosenClass: 'sortable-chosen',
        dragClass: 'sortable-drag',
        filter: '.rule-tree-empty',
        onEnd: evt => this.handleSortEnd(evt),
      });
      this.sortableInstances.push(sortable);
    }

    // Nested group containers
    document.querySelectorAll('.nested-group-rules').forEach(container => {
      const sortable = new Sortable(container, {
        group: 'rules',
        animation: 150,
        handle: '.rule-card-drag-handle',
        draggable: '.rule-card',
        ghostClass: 'sortable-ghost',
        chosenClass: 'sortable-chosen',
        dragClass: 'sortable-drag',
        onEnd: evt => this.handleSortEnd(evt),
      });
      this.sortableInstances.push(sortable);
    });
  }

  handleSortEnd(evt) {
    // Rebuild tree from DOM
    this.rebuildTreeFromDOM();
    this.saveHistoryState();
    this.hasUnsavedChanges = true;
  }

  rebuildTreeFromDOM() {
    const ruleTree = document.getElementById('rule-tree');
    if (!ruleTree) return;

    this.rulesTree = [];

    ruleTree.querySelectorAll(':scope > .rule-card, :scope > .nested-group-card').forEach(el => {
      if (el.classList.contains('rule-card')) {
        const ruleId = el.dataset.ruleId;
        const rule = this.findRuleById(ruleId);
        if (rule) this.rulesTree.push(rule);
      } else if (el.classList.contains('nested-group-card')) {
        const groupId = el.dataset.groupId;
        const group = this.findGroupById(groupId);
        if (group) {
          // Rebuild group's rules from its container
          group.rules = [];
          el.querySelectorAll('.nested-group-rules > .rule-card').forEach(ruleEl => {
            const ruleId = ruleEl.dataset.ruleId;
            const rule = this.findRuleById(ruleId);
            if (rule) group.rules.push(rule);
          });
          this.rulesTree.push(group);
        }
      }
    });
  }

  // =========================================
  // Rule/Group Operations
  // =========================================

  handleLibraryDrop(data, targetGroup = null) {
    if (data.type === 'group') {
      this.addNestedGroup(data.logic, targetGroup);
    } else if (data.type === 'rule') {
      this.addNewRule(data.ruleType, targetGroup);
    } else if (data.type === 'saved-rule') {
      this.addSavedRule(data.ruleId, targetGroup);
    }
  }

  addNewRule(ruleType, targetGroup = null) {
    const typeLabel = this.config.ruleTypeLabels[ruleType] || ruleType;
    const newRule = {
      id: `temp-${Date.now()}`,
      name: `New ${typeLabel} Rule`,
      rule_type: ruleType,
      operator: this.getDefaultOperator(ruleType),
      value: this.getDefaultValue(ruleType),
      is_active: true,
      description: '',
      isNew: true,
    };

    if (targetGroup) {
      if (!targetGroup.rules) targetGroup.rules = [];
      targetGroup.rules.push(newRule);
    } else {
      this.rulesTree.push(newRule);
    }

    this.renderRulesTree();
    this.selectRule(newRule);
    this.saveHistoryState();
    this.hasUnsavedChanges = true;
    this.showToast(this.config.translations.ruleAdded || 'Rule added', 'success');
  }

  addSavedRule(ruleId, targetGroup = null) {
    const savedRule = this.savedRules.find(r => r.id == ruleId);
    if (!savedRule) return;

    // Clone the rule for the tree
    const ruleCopy = { ...savedRule, treeId: `ref-${Date.now()}` };

    if (targetGroup) {
      if (!targetGroup.rules) targetGroup.rules = [];
      targetGroup.rules.push(ruleCopy);
    } else {
      this.rulesTree.push(ruleCopy);
    }

    this.renderRulesTree();
    this.saveHistoryState();
    this.hasUnsavedChanges = true;
    this.showToast(this.config.translations.ruleAdded || 'Rule added', 'success');
  }

  addNestedGroup(logic, parentGroup = null) {
    const newGroup = {
      id: `temp-group-${Date.now()}`,
      type: 'group',
      name: `${logic} Group`,
      logic_operator: logic,
      rules: [],
      is_active: true,
      isNew: true,
    };

    if (parentGroup) {
      if (!parentGroup.rules) parentGroup.rules = [];
      parentGroup.rules.push(newGroup);
    } else {
      this.rulesTree.push(newGroup);
    }

    this.renderRulesTree();
    this.saveHistoryState();
    this.hasUnsavedChanges = true;
    this.showToast('Group added', 'success');
  }

  selectRule(rule) {
    this.selectedRule = rule;

    // Update UI selection
    document.querySelectorAll('.rule-card').forEach(el => {
      el.classList.remove('selected');
      if (el.dataset.ruleId === String(rule.id)) {
        el.classList.add('selected');
      }
    });

    // Show properties panel
    this.renderRuleProperties(rule);
  }

  toggleRuleActive(rule) {
    rule.is_active = !rule.is_active;
    this.renderRulesTree();
    this.saveHistoryState();
    this.hasUnsavedChanges = true;
  }

  editRule(rule) {
    this.selectRule(rule);
    this.switchTab('rule-props');
  }

  showDeleteConfirm(item, isGroup = false) {
    this.pendingDelete = { item, isGroup };

    const message = document.getElementById('delete-confirm-message');
    if (message) {
      message.textContent = isGroup
        ? this.config.translations.deleteGroupConfirm || 'Delete this group and all its rules?'
        : this.config.translations.deleteConfirm || 'Remove this rule from the group?';
    }

    document.getElementById('delete-confirm-modal')?.classList.remove('hidden');
  }

  hideDeleteModal() {
    document.getElementById('delete-confirm-modal')?.classList.add('hidden');
    this.pendingDelete = null;
  }

  confirmDelete() {
    if (!this.pendingDelete) return;

    const { item, isGroup } = this.pendingDelete;

    // Remove from tree
    this.removeFromTree(item, isGroup);

    this.hideDeleteModal();
    this.renderRulesTree();
    this.saveHistoryState();
    this.hasUnsavedChanges = true;
    this.showToast(this.config.translations.ruleRemoved || 'Item removed', 'success');

    // Clear selection if deleted item was selected
    if (this.selectedRule?.id === item.id) {
      this.selectedRule = null;
      this.clearPropertiesPanel();
    }
  }

  removeFromTree(item, isGroup) {
    const removeRecursive = arr => {
      const index = arr.findIndex(i => i.id === item.id);
      if (index > -1) {
        arr.splice(index, 1);
        return true;
      }

      // Check nested groups
      for (const i of arr) {
        if (i.type === 'group' && i.rules) {
          if (removeRecursive(i.rules)) return true;
        }
      }
      return false;
    };

    removeRecursive(this.rulesTree);
  }

  toggleGroupCollapse(groupEl) {
    groupEl.classList.toggle('collapsed');
  }

  toggleGroupLogic(group, groupEl) {
    group.logic_operator = group.logic_operator === 'AND' ? 'OR' : 'AND';
    groupEl.dataset.logic = group.logic_operator;

    const badge = groupEl.querySelector('.logic-badge');
    if (badge) {
      badge.textContent = group.logic_operator;
      badge.classList.toggle('logic-or', group.logic_operator === 'OR');
    }

    this.saveHistoryState();
    this.hasUnsavedChanges = true;
  }

  // =========================================
  // Properties Panel
  // =========================================

  renderRuleProperties(rule) {
    const panel = document.getElementById('rule-properties-panel');
    if (!panel) return;

    const typeLabel = this.config.ruleTypeLabels[rule.rule_type] || rule.rule_type;

    panel.innerHTML = `
            <div class="property-group">
                <label class="property-label">Rule Name</label>
                <input type="text" id="prop-rule-name" class="property-input" value="${this.escapeHtml(rule.name || '')}">
            </div>

            <div class="property-group">
                <label class="property-label">Rule Type</label>
                <div class="property-static">
                    <span class="rule-type-badge">${typeLabel}</span>
                </div>
            </div>

            <div class="property-group">
                <label class="property-label">Operator</label>
                <select id="prop-rule-operator" class="property-select">
                    ${this.renderOperatorOptions(rule)}
                </select>
            </div>

            <div class="property-group">
                <label class="property-label">Value</label>
                ${this.renderValueInput(rule)}
            </div>

            <div class="property-group">
                <label class="property-label">Description</label>
                <textarea id="prop-rule-description" class="property-textarea" rows="3">${this.escapeHtml(rule.description || '')}</textarea>
            </div>

            <div class="property-group">
                <label class="property-checkbox">
                    <input type="checkbox" id="prop-rule-active" ${rule.is_active ? 'checked' : ''}>
                    <span>Rule is active</span>
                </label>
            </div>

            <div class="property-group" style="margin-top: 1.5rem;">
                <button class="btn-primary" id="apply-rule-changes" style="width: 100%;">
                    <i class="fas fa-check"></i> Apply Changes
                </button>
            </div>
        `;

    // Bind events
    document.getElementById('apply-rule-changes')?.addEventListener('click', () => {
      this.applyRuleChanges(rule);
    });
  }

  renderOperatorOptions(rule) {
    const operators = [
      'equals',
      'not_equals',
      'contains',
      'not_contains',
      'greater_than',
      'less_than',
      'in_list',
      'not_in_list',
      'is_true',
      'is_false',
      'between',
      'regex',
    ];

    return operators
      .map(op => {
        const label = this.config.operatorLabels[op] || op;
        const selected = rule.operator === op ? 'selected' : '';
        return `<option value="${op}" ${selected}>${label}</option>`;
      })
      .join('');
  }

  renderValueInput(rule) {
    const ruleType = rule.rule_type;
    const value = rule.value;

    // Boolean types
    if (
      ruleType === 'user_logged_in' ||
      ruleType === 'first_visit' ||
      ruleType === 'has_purchased' ||
      ruleType === 'abandoned_cart' ||
      ruleType === 'wishlist_items' ||
      ruleType === 'business_hours'
    ) {
      return `
                <select id="prop-rule-value" class="property-select">
                    <option value="true" ${value === true || value === 'true' ? 'selected' : ''}>True</option>
                    <option value="false" ${value === false || value === 'false' ? 'selected' : ''}>False</option>
                </select>
            `;
    }

    // Device type
    if (ruleType === 'device_type') {
      return `
                <select id="prop-rule-value" class="property-select">
                    <option value="desktop" ${value === 'desktop' ? 'selected' : ''}>Desktop</option>
                    <option value="mobile" ${value === 'mobile' ? 'selected' : ''}>Mobile</option>
                    <option value="tablet" ${value === 'tablet' ? 'selected' : ''}>Tablet</option>
                </select>
            `;
    }

    // Day of week
    if (ruleType === 'day_of_week') {
      const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
      const valueArr = Array.isArray(value) ? value : value?.values || [];
      return `
                <div class="property-checkbox-group">
                    ${days
                      .map(
                        (day, i) => `
                        <label class="property-checkbox">
                            <input type="checkbox" name="prop-rule-value-day" value="${i + 1}"
                                   ${valueArr.includes(i + 1) || valueArr.includes(String(i + 1)) ? 'checked' : ''}>
                            <span>${day}</span>
                        </label>
                    `
                      )
                      .join('')}
                </div>
            `;
    }

    // Numeric types
    if (
      [
        'cart_value',
        'cart_items',
        'visit_count',
        'page_views',
        'time_on_site',
        'user_lifetime_value',
        'user_order_count',
        'screen_size',
      ].includes(ruleType)
    ) {
      const numValue = typeof value === 'object' ? value.value || '' : value || '';
      return `
                <input type="number" id="prop-rule-value" class="property-input" value="${numValue}">
            `;
    }

    // Default: text input
    const strValue =
      typeof value === 'object'
        ? value.values?.join(', ') || value.display || JSON.stringify(value)
        : value || '';
    return `
            <input type="text" id="prop-rule-value" class="property-input"
                   value="${this.escapeHtml(strValue)}"
                   placeholder="Enter value or comma-separated list">
        `;
  }

  applyRuleChanges(rule) {
    const name = document.getElementById('prop-rule-name')?.value;
    const operator = document.getElementById('prop-rule-operator')?.value;
    const description = document.getElementById('prop-rule-description')?.value;
    const isActive = document.getElementById('prop-rule-active')?.checked;

    // Get value based on rule type
    let value;
    if (rule.rule_type === 'day_of_week') {
      value = {
        values: Array.from(
          document.querySelectorAll('input[name="prop-rule-value-day"]:checked')
        ).map(el => parseInt(el.value)),
      };
    } else {
      const valueInput = document.getElementById('prop-rule-value');
      if (valueInput) {
        if (valueInput.tagName === 'SELECT') {
          value =
            valueInput.value === 'true'
              ? true
              : valueInput.value === 'false'
                ? false
                : valueInput.value;
        } else if (valueInput.type === 'number') {
          value = { value: parseFloat(valueInput.value) || 0 };
        } else {
          // Check if comma-separated list
          const strValue = valueInput.value;
          if (strValue.includes(',')) {
            value = {
              values: strValue
                .split(',')
                .map(s => s.trim())
                .filter(s => s),
            };
          } else {
            value = strValue;
          }
        }
      }
    }

    // Update rule
    rule.name = name;
    rule.operator = operator;
    rule.value = value;
    rule.description = description;
    rule.is_active = isActive;

    this.renderRulesTree();
    this.saveHistoryState();
    this.hasUnsavedChanges = true;
    this.showToast(this.config.translations.ruleUpdated || 'Rule updated', 'success');
  }

  clearPropertiesPanel() {
    const panel = document.getElementById('rule-properties-panel');
    if (panel) {
      panel.innerHTML = `
                <div class="properties-empty">
                    <i class="fas fa-hand-pointer"></i>
                    <p>Select a rule to edit its properties</p>
                </div>
            `;
    }
  }

  // =========================================
  // Logic Operator
  // =========================================

  setLogicOperator(logic) {
    this.logicOperator = logic;

    // Update toggle buttons
    document.querySelectorAll('.logic-toggle').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.logic === logic);
    });

    // Update badge
    const badge = document.getElementById('logic-badge');
    if (badge) {
      badge.textContent = logic;
      badge.classList.toggle('logic-or', logic === 'OR');
    }

    // Update info panel
    const infoLogic = document.getElementById('info-logic-operator');
    if (infoLogic) infoLogic.value = logic;

    this.hasUnsavedChanges = true;
  }

  // =========================================
  // History (Undo/Redo)
  // =========================================

  saveHistoryState() {
    // Remove future states if we're not at the end
    if (this.historyIndex < this.history.length - 1) {
      this.history = this.history.slice(0, this.historyIndex + 1);
    }

    // Deep clone current state
    const state = JSON.parse(
      JSON.stringify({
        rulesTree: this.rulesTree,
        groupName: this.groupName,
        logicOperator: this.logicOperator,
      })
    );

    this.history.push(state);

    // Limit history size
    if (this.history.length > this.maxHistorySize) {
      this.history.shift();
    } else {
      this.historyIndex++;
    }

    this.updateHistoryButtons();
  }

  undo() {
    if (this.historyIndex > 0) {
      this.historyIndex--;
      this.restoreState(this.history[this.historyIndex]);
      this.updateHistoryButtons();
    }
  }

  redo() {
    if (this.historyIndex < this.history.length - 1) {
      this.historyIndex++;
      this.restoreState(this.history[this.historyIndex]);
      this.updateHistoryButtons();
    }
  }

  restoreState(state) {
    this.rulesTree = JSON.parse(JSON.stringify(state.rulesTree));
    this.groupName = state.groupName;
    this.logicOperator = state.logicOperator;

    document.getElementById('group-name-input').value = this.groupName;
    this.setLogicOperator(this.logicOperator);
    this.renderRulesTree();
    this.hasUnsavedChanges = true;
  }

  updateHistoryButtons() {
    const undoBtn = document.getElementById('undo-btn');
    const redoBtn = document.getElementById('redo-btn');

    if (undoBtn) undoBtn.disabled = this.historyIndex <= 0;
    if (redoBtn) redoBtn.disabled = this.historyIndex >= this.history.length - 1;
  }

  // =========================================
  // Save Group
  // =========================================

  async saveGroup() {
    const saveBtn = document.getElementById('save-btn');
    if (saveBtn) {
      saveBtn.disabled = true;
      saveBtn.innerHTML =
        '<i class="fas fa-spinner fa-spin"></i> <span class="btn-text">Saving...</span>';
    }

    try {
      const groupData = {
        name: this.groupName || 'Unnamed Group',
        description: document.getElementById('info-group-description')?.value || '',
        logic_operator: this.logicOperator,
        is_active: document.getElementById('group-active')?.checked ?? true,
        rules: this.prepareRulesForSave(),
      };

      const url = this.groupId
        ? `${this.config.apiGroupsUrl}${this.groupId}/`
        : this.config.apiGroupsUrl;

      const method = this.groupId ? 'PUT' : 'POST';

      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.config.csrfToken,
        },
        body: JSON.stringify(groupData),
      });

      if (!response.ok) {
        throw new Error('Failed to save group');
      }

      const result = await response.json();

      // Update local state with server response
      if (!this.groupId && result.id) {
        this.groupId = result.id;
        // Update URL without reload
        const newUrl = window.location.pathname.replace(/\/builder\/?$/, `/builder/${result.id}/`);
        window.history.replaceState({}, '', newUrl);
      }

      this.hasUnsavedChanges = false;
      this.showToast(this.config.translations.groupUpdated || 'Group saved', 'success');
    } catch (error) {
      console.error('Save error:', error);
      this.showToast(this.config.translations.error || 'Error saving group', 'error');
    } finally {
      if (saveBtn) {
        saveBtn.disabled = false;
        saveBtn.innerHTML = '<i class="fas fa-save"></i> <span class="btn-text">Save</span>';
      }
    }
  }

  prepareRulesForSave() {
    // Flatten rules with order information
    return this.rulesTree.map((item, index) => {
      if (item.type === 'group') {
        return {
          type: 'nested_group',
          logic_operator: item.logic_operator,
          name: item.name,
          order: index,
          rules: (item.rules || []).map((r, i) => ({
            rule_id: r.id && !String(r.id).startsWith('temp') ? r.id : null,
            rule_type: r.rule_type,
            operator: r.operator,
            value: r.value,
            name: r.name,
            is_active: r.is_active,
            order: i,
          })),
        };
      } else {
        return {
          rule_id: item.id && !String(item.id).startsWith('temp') ? item.id : null,
          rule_type: item.rule_type,
          operator: item.operator,
          value: item.value,
          name: item.name,
          description: item.description,
          is_active: item.is_active,
          order: index,
        };
      }
    });
  }

  // =========================================
  // Modal Management
  // =========================================

  showAddRuleModal() {
    document.getElementById('add-rule-modal')?.classList.remove('hidden');
    document.getElementById('new-rule-name').value = '';
    document.getElementById('new-rule-type').value = 'geo_country';
  }

  hideAddRuleModal() {
    document.getElementById('add-rule-modal')?.classList.add('hidden');
  }

  confirmAddRule() {
    const ruleType = document.getElementById('new-rule-type')?.value;
    const ruleName = document.getElementById('new-rule-name')?.value;

    if (ruleType) {
      this.addNewRule(ruleType);
      // Update name if provided
      if (ruleName && this.rulesTree.length > 0) {
        const newRule = this.rulesTree[this.rulesTree.length - 1];
        if (newRule && !newRule.type) {
          newRule.name = ruleName;
          this.renderRulesTree();
        }
      }
    }

    this.hideAddRuleModal();
  }

  showNewGroupModal() {
    document.getElementById('new-group-modal')?.classList.remove('hidden');
    document.getElementById('create-group-name').value = '';
    document.getElementById('create-group-logic').value = 'AND';
    document.getElementById('create-group-description').value = '';
  }

  hideNewGroupModal() {
    document.getElementById('new-group-modal')?.classList.add('hidden');
  }

  createNewGroup() {
    const name = document.getElementById('create-group-name')?.value || 'New Rule Group';
    const logic = document.getElementById('create-group-logic')?.value || 'AND';
    const description = document.getElementById('create-group-description')?.value || '';

    // Reset builder for new group
    this.groupId = null;
    this.groupName = name;
    this.logicOperator = logic;
    this.rulesTree = [];
    this.history = [];
    this.historyIndex = -1;

    document.getElementById('group-name-input').value = name;
    document.getElementById('info-group-name').value = name;
    document.getElementById('info-group-description').value = description;
    this.setLogicOperator(logic);

    this.renderRulesTree();
    this.saveHistoryState();
    this.hasUnsavedChanges = true;

    this.hideNewGroupModal();
    this.showToast(this.config.translations.groupCreated || 'New group created', 'success');
  }

  // =========================================
  // Preview
  // =========================================

  togglePreview() {
    const panel = document.getElementById('rule-preview-panel');
    if (panel) {
      panel.classList.toggle('hidden');
    }
  }

  hidePreview() {
    document.getElementById('rule-preview-panel')?.classList.add('hidden');
  }

  async runPreview() {
    const resultDiv = document.getElementById('preview-result');
    if (!resultDiv) return;

    resultDiv.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Evaluating...';

    // Build context from form
    const context = {
      user_logged_in: document.getElementById('preview-logged-in')?.value === 'true',
      country: document.getElementById('preview-country')?.value,
      device_type: document.getElementById('preview-device')?.value,
      cart_value: parseFloat(document.getElementById('preview-cart-value')?.value) || 0,
    };

    // Simulate evaluation (in production, this would call the API)
    const result = this.evaluateRulesLocally(context);

    if (result) {
      resultDiv.className = 'preview-result match';
      resultDiv.innerHTML = `
                <i class="fas fa-check-circle"></i>
                <p>${this.config.translations.ruleMatch || 'VISIBLE - All conditions met'}</p>
            `;
    } else {
      resultDiv.className = 'preview-result no-match';
      resultDiv.innerHTML = `
                <i class="fas fa-times-circle"></i>
                <p>${this.config.translations.ruleNoMatch || 'HIDDEN - Conditions not met'}</p>
            `;
    }
  }

  evaluateRulesLocally(context) {
    if (this.rulesTree.length === 0) return true;

    const evaluate = (rules, logic) => {
      const results = rules.map(item => {
        if (item.type === 'group') {
          return evaluate(item.rules || [], item.logic_operator);
        }
        return this.evaluateSingleRule(item, context);
      });

      if (logic === 'AND') {
        return results.every(r => r);
      } else {
        return results.some(r => r);
      }
    };

    return evaluate(this.rulesTree, this.logicOperator);
  }

  evaluateSingleRule(rule, context) {
    if (!rule.is_active) return true; // Inactive rules pass

    const ruleType = rule.rule_type;
    const operator = rule.operator;
    const value = rule.value;

    // Get context value for this rule type
    let contextValue;
    if (ruleType === 'user_logged_in') contextValue = context.user_logged_in;
    else if (ruleType === 'geo_country') contextValue = context.country;
    else if (ruleType === 'device_type') contextValue = context.device_type;
    else if (ruleType === 'cart_value') contextValue = context.cart_value;
    else return true; // Unknown rule types pass

    // Compare
    const targetValue = typeof value === 'object' ? value.value || value.values?.[0] : value;

    switch (operator) {
      case 'equals':
      case 'is_true':
        return contextValue === targetValue || contextValue === true;
      case 'not_equals':
      case 'is_false':
        return contextValue !== targetValue || contextValue === false;
      case 'greater_than':
        return contextValue > targetValue;
      case 'less_than':
        return contextValue < targetValue;
      case 'in_list':
        const list = value.values || [value];
        return list.includes(contextValue);
      case 'not_in_list':
        const notList = value.values || [value];
        return !notList.includes(contextValue);
      default:
        return true;
    }
  }

  // =========================================
  // UI Helpers
  // =========================================

  switchTab(tabId) {
    document.querySelectorAll('.admin-tab-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.tab === tabId);
    });

    document.querySelectorAll('.admin-tab-content').forEach(content => {
      content.classList.toggle('active', content.id === `${tabId}-tab`);
    });
  }

  toggleLibrarySection(header) {
    header.classList.toggle('collapsed');
  }

  filterLibrary(query) {
    const q = query.toLowerCase();
    document.querySelectorAll('.library-item').forEach(item => {
      const text = item.textContent.toLowerCase();
      item.style.display = text.includes(q) ? '' : 'none';
    });
  }

  filterSavedRules(query) {
    const q = query.toLowerCase();
    document.querySelectorAll('#saved-rules .library-item').forEach(item => {
      const text = item.textContent.toLowerCase();
      item.style.display = text.includes(q) ? '' : 'none';
    });
  }

  expandAllGroups() {
    document.querySelectorAll('.nested-group-card').forEach(el => {
      el.classList.remove('collapsed');
    });
  }

  collapseAllGroups() {
    document.querySelectorAll('.nested-group-card').forEach(el => {
      el.classList.add('collapsed');
    });
  }

  async switchGroup(groupId) {
    if (this.hasUnsavedChanges) {
      if (!(await AdminModal.confirm('You have unsaved changes. Switch anyway?'))) {
        // Reset selector
        document.getElementById('group-selector').value = this.groupId || '';
        return;
      }
    }

    if (groupId) {
      window.location.href = window.location.pathname.replace(
        /\/builder\/?\d*\/?$/,
        `/builder/${groupId}/`
      );
    } else {
      window.location.href = window.location.pathname.replace(/\/builder\/?\d*\/?$/, '/builder/');
    }
  }

  updateRuleCount() {
    const countEl = document.getElementById('rule-count');
    if (countEl) {
      const count = this.countRules(this.rulesTree);
      countEl.textContent = count;
    }

    const badge = document.getElementById('rule-count-badge');
    if (badge) {
      badge.style.display = this.rulesTree.length > 0 ? '' : 'none';
    }
  }

  countRules(items) {
    let count = 0;
    items.forEach(item => {
      if (item.type === 'group') {
        count += this.countRules(item.rules || []);
      } else {
        count++;
      }
    });
    return count;
  }

  handleKeyboard(e) {
    // Ctrl/Cmd + Z = Undo
    if ((e.ctrlKey || e.metaKey) && e.key === 'z' && !e.shiftKey) {
      e.preventDefault();
      this.undo();
    }

    // Ctrl/Cmd + Y or Ctrl/Cmd + Shift + Z = Redo
    if ((e.ctrlKey || e.metaKey) && (e.key === 'y' || (e.key === 'z' && e.shiftKey))) {
      e.preventDefault();
      this.redo();
    }

    // Ctrl/Cmd + S = Save
    if ((e.ctrlKey || e.metaKey) && e.key === 's') {
      e.preventDefault();
      this.saveGroup();
    }

    // Delete/Backspace = Delete selected rule
    if ((e.key === 'Delete' || e.key === 'Backspace') && this.selectedRule) {
      // Only if not in an input field
      if (!['INPUT', 'TEXTAREA', 'SELECT'].includes(e.target.tagName)) {
        e.preventDefault();
        this.showDeleteConfirm(this.selectedRule);
      }
    }

    // Escape = Deselect
    if (e.key === 'Escape') {
      this.selectedRule = null;
      document
        .querySelectorAll('.rule-card.selected')
        .forEach(el => el.classList.remove('selected'));
      this.clearPropertiesPanel();

      // Close modals
      document.querySelectorAll('.modal-overlay').forEach(modal => modal.classList.add('hidden'));
    }
  }

  // =========================================
  // Toast Notifications
  // =========================================

  showToast(message, type = 'info') {
    AdminModal.toast(message, type || 'info');
  }

  // =========================================
  // Utility Functions
  // =========================================

  getRuleIcon(ruleType) {
    const icons = {
      geo_country: 'fa-globe',
      geo_region: 'fa-map-marked-alt',
      geo_city: 'fa-city',
      geo_timezone: 'fa-clock',
      user_logged_in: 'fa-user-check',
      user_group: 'fa-users',
      user_segment: 'fa-user-tag',
      user_lifetime_value: 'fa-gem',
      user_order_count: 'fa-shopping-bag',
      device_type: 'fa-mobile-alt',
      browser: 'fa-chrome',
      operating_system: 'fa-laptop',
      screen_size: 'fa-expand',
      connection_speed: 'fa-wifi',
      date_range: 'fa-calendar-alt',
      time_range: 'fa-clock',
      day_of_week: 'fa-calendar-week',
      business_hours: 'fa-store',
      first_visit: 'fa-hand-sparkles',
      visit_count: 'fa-redo',
      page_views: 'fa-eye',
      time_on_site: 'fa-hourglass-half',
      referrer: 'fa-share',
      utm_campaign: 'fa-bullhorn',
      cart_value: 'fa-dollar-sign',
      cart_items: 'fa-shopping-cart',
      has_purchased: 'fa-receipt',
      abandoned_cart: 'fa-cart-arrow-down',
      wishlist_items: 'fa-heart',
      browser_language: 'fa-language',
      selected_language: 'fa-globe-americas',
      selected_currency: 'fa-coins',
    };
    return icons[ruleType] || 'fa-filter';
  }

  getDefaultOperator(ruleType) {
    // Boolean types default to is_true
    if (
      [
        'user_logged_in',
        'first_visit',
        'has_purchased',
        'abandoned_cart',
        'wishlist_items',
        'business_hours',
      ].includes(ruleType)
    ) {
      return 'is_true';
    }

    // Numeric types default to greater_than
    if (
      [
        'cart_value',
        'cart_items',
        'visit_count',
        'page_views',
        'time_on_site',
        'user_lifetime_value',
        'user_order_count',
      ].includes(ruleType)
    ) {
      return 'greater_than';
    }

    // List types default to in_list
    if (['geo_country', 'day_of_week'].includes(ruleType)) {
      return 'in_list';
    }

    return 'equals';
  }

  getDefaultValue(ruleType) {
    // Boolean types
    if (
      [
        'user_logged_in',
        'first_visit',
        'has_purchased',
        'abandoned_cart',
        'wishlist_items',
        'business_hours',
      ].includes(ruleType)
    ) {
      return true;
    }

    // Numeric types
    if (
      [
        'cart_value',
        'cart_items',
        'visit_count',
        'page_views',
        'time_on_site',
        'user_lifetime_value',
        'user_order_count',
      ].includes(ruleType)
    ) {
      return { value: 0 };
    }

    return '';
  }

  formatRuleValue(value) {
    if (value === null || value === undefined) return '-';
    if (typeof value === 'boolean') return value ? 'True' : 'False';
    if (typeof value === 'object') {
      if (value.display) return this.escapeHtml(value.display);
      if (value.values) return this.escapeHtml(value.values.join(', '));
      if (value.value !== undefined) return String(value.value);
      return JSON.stringify(value);
    }
    return this.escapeHtml(String(value));
  }

  findRuleById(id) {
    const findRecursive = items => {
      for (const item of items) {
        if (String(item.id) === String(id)) return item;
        if (item.type === 'group' && item.rules) {
          const found = findRecursive(item.rules);
          if (found) return found;
        }
      }
      return null;
    };
    return findRecursive(this.rulesTree) || this.savedRules.find(r => String(r.id) === String(id));
  }

  findGroupById(id) {
    const findRecursive = items => {
      for (const item of items) {
        if (item.type === 'group' && String(item.id) === String(id)) return item;
        if (item.type === 'group' && item.rules) {
          const found = findRecursive(item.rules);
          if (found) return found;
        }
      }
      return null;
    };
    return findRecursive(this.rulesTree);
  }

  escapeHtml(str) {
    if (!str) return '';
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  window.ruleBuilder = new RuleBuilder();

  // Back button handler (replaces onclick attribute)
  const backBtn = document.getElementById('back-btn');
  if (backBtn && backBtn.dataset.url) {
    backBtn.addEventListener('click', () => {
      window.location.href = backBtn.dataset.url;
    });
  }
});
