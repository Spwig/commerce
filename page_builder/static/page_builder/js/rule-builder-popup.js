/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

class RuleBuilderPopup {
  constructor(config) {
    this.config = config;
    this.selectedGroupId = config.groupId;
    this.selectedRules = [];
    this.init();
  }

  init() {
    this.bindEvents();
    this.initDragDrop();

    if (this.config.initialRulesTree && this.config.initialRulesTree.children) {
      this.selectedRules = this.config.initialRulesTree.children.filter(c => c.type === 'rule');
      this.updateSelectionInfo();
    }
  }

  bindEvents() {
    // Category toggle
    document.querySelectorAll('.category-header').forEach(header => {
      header.addEventListener('click', e => {
        header.classList.toggle('collapsed');
        const items = header.nextElementSibling;
        if (items) {
          items.classList.toggle('collapsed');
        }
      });
    });

    // Saved group selection
    document.querySelectorAll('.saved-group-item').forEach(item => {
      item.addEventListener('click', () => this.selectGroup(item.dataset.groupId));
    });

    // Clear selection
    document
      .getElementById('btnClearSelection')
      ?.addEventListener('click', () => this.clearSelection());

    // Create new group
    document
      .getElementById('btnCreateNewGroup')
      ?.addEventListener('click', () => this.createNewGroup());

    // Apply rules
    document.getElementById('btnApplyRules')?.addEventListener('click', () => this.applyRules());

    // Close popup buttons (replaces onclick="window.parent.closeRuleBuilderPopup()")
    document.addEventListener('click', e => {
      if (e.target.closest('[data-action="close-rule-popup"]')) {
        if (window.parent && window.parent.closeRuleBuilderPopup) {
          window.parent.closeRuleBuilderPopup();
        } else {
          window.close();
        }
        return;
      }
      // Remove rule card button (replaces inline onclick in addQuickRule innerHTML)
      const removeBtn = e.target.closest('[data-action="remove-rule-card"]');
      if (removeBtn) {
        removeBtn.closest('.rule-preview-card')?.remove();
        this.updateSelectionInfo();
      }
    });
  }

  initDragDrop() {
    // Make quick-add items draggable
    document.querySelectorAll('.quick-rule-item').forEach(item => {
      item.addEventListener('dragstart', e => {
        e.dataTransfer.setData(
          'text/plain',
          JSON.stringify({
            type: 'new_rule',
            ruleType: item.dataset.ruleType,
            category: item.dataset.category,
          })
        );
      });
    });

    // Make canvas a drop target
    const canvas = document.getElementById('canvasContent');
    if (canvas) {
      canvas.addEventListener('dragover', e => {
        e.preventDefault();
        canvas.classList.add('drag-over');
      });

      canvas.addEventListener('dragleave', () => {
        canvas.classList.remove('drag-over');
      });

      canvas.addEventListener('drop', e => {
        e.preventDefault();
        canvas.classList.remove('drag-over');
        this.handleDrop(e);
      });
    }
  }

  handleDrop(e) {
    try {
      const data = JSON.parse(e.dataTransfer.getData('text/plain'));
      if (data.type === 'new_rule') {
        this.addQuickRule(data.ruleType, data.category);
      }
    } catch (err) {
      console.error('Drop error:', err);
    }
  }

  selectGroup(groupId) {
    // Update UI
    document.querySelectorAll('.saved-group-item').forEach(item => {
      item.classList.toggle('selected', item.dataset.groupId === groupId);
    });

    this.selectedGroupId = groupId;

    // Load group data
    fetch(`${this.config.apiUrls.ruleGroups}${groupId}/`)
      .then(r => r.json())
      .then(data => {
        if (data.success && data.group) {
          this.renderGroupPreview(data.group);
          this.updateSelectionInfo();
        }
      })
      .catch(err => console.error('Error loading group:', err));
  }

  renderGroupPreview(group) {
    const canvas = document.getElementById('canvasContent');
    const logicClass = group.logic_operator.toLowerCase();

    let rulesHtml = '';
    if (group.rules && group.rules.length > 0) {
      group.rules.forEach(rule => {
        rulesHtml += `
                    <div class="rule-preview-card" data-rule-id="${rule.id}">
                        <div style="display: flex; align-items: center;">
                            <i class="fas fa-filter" style="margin-right: 8px; color: var(--rb-muted-text);"></i>
                            <strong>${this.escapeHtml(rule.name)}</strong>
                        </div>
                        <div style="margin-top: 4px; font-size: 12px; color: var(--rb-muted-text);">
                            ${this.escapeHtml(rule.rule_type)} ${rule.operator} ${this.escapeHtml(rule.value || '')}
                        </div>
                    </div>
                `;
      });
    }

    canvas.innerHTML = `
            <div class="rule-preview-card group-card ${logicClass}-group">
                <div style="display: flex; align-items: center; margin-bottom: 12px;">
                    <span class="logic-badge ${logicClass}" style="
                        padding: 2px 8px;
                        border-radius: 4px;
                        font-size: 11px;
                        font-weight: 600;
                        background: ${logicClass === 'and' ? '#3b82f6' : '#22c55e'};
                        color: white;
                    ">${group.logic_operator}</span>
                    <strong style="margin-left: 8px;">${this.escapeHtml(group.name)}</strong>
                </div>
                <div class="rules-list">
                    ${rulesHtml || '<p style="color: var(--rb-muted-text); font-size: 12px;">No rules in this group</p>'}
                </div>
            </div>
        `;

    this.selectedRules = group.rules || [];
  }

  addQuickRule(ruleType, category) {
    // Remove empty state if present
    const emptyState = document.getElementById('emptyState');
    if (emptyState) {
      emptyState.remove();
    }

    // Get rule type info
    const categoryInfo = this.config.ruleTypes[category];
    const typeInfo = categoryInfo?.types?.find(t => t.id === ruleType);
    const label = typeInfo?.label || ruleType;

    // Create rule preview
    const canvas = document.getElementById('canvasContent');
    const ruleCard = document.createElement('div');
    ruleCard.className = 'rule-preview-card';
    ruleCard.dataset.ruleType = ruleType;
    ruleCard.dataset.tempId = `temp_${Date.now()}`;

    ruleCard.innerHTML = `
            <div style="display: flex; align-items: center;">
                <i class="${categoryInfo?.icon || 'fas fa-filter'}" style="margin-right: 8px; color: var(--rb-muted-text);"></i>
                <strong>${this.escapeHtml(label)}</strong>
                <button type="button" data-action="remove-rule-card" style="margin-left: auto; background: none; border: none; color: var(--rb-danger); cursor: pointer;">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div style="margin-top: 8px;">
                <select class="operator-select" style="padding: 4px 8px; border: 1px solid var(--rb-border-color); border-radius: 4px; font-size: 12px;">
                    ${this.config.operators.map(op => `<option value="${op.id}">${op.label} (${op.symbol})</option>`).join('')}
                </select>
                <input type="text" class="value-input" placeholder="Value" style="padding: 4px 8px; border: 1px solid var(--rb-border-color); border-radius: 4px; font-size: 12px; margin-left: 8px; width: 150px;">
            </div>
        `;

    canvas.appendChild(ruleCard);
    this.updateSelectionInfo();
  }

  clearSelection() {
    this.selectedGroupId = null;
    this.selectedRules = [];

    document.querySelectorAll('.saved-group-item').forEach(item => {
      item.classList.remove('selected');
    });

    const canvas = document.getElementById('canvasContent');
    canvas.innerHTML = `
            <div class="empty-state" id="emptyState">
                <i class="fas fa-filter"></i>
                <p>${this.config.translations.noRulesSelected}</p>
                <p style="font-size: 12px;">Select a saved group from the left, or drag rules to build a new configuration.</p>
            </div>
        `;

    this.updateSelectionInfo();
  }

  async createNewGroup() {
    const name = await AdminModal.prompt({
      message: 'Enter group name:',
      defaultValue: 'New Rule Group',
    });
    if (!name) return;

    // Create group via API
    fetch(this.config.apiUrls.ruleGroups, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.getCSRFToken(),
      },
      body: JSON.stringify({
        name: name,
        logic_operator: 'AND',
        is_active: true,
      }),
    })
      .then(r => r.json())
      .then(data => {
        if (data.success && data.group) {
          this.selectedGroupId = data.group.id;
          this.renderGroupPreview(data.group);
          this.updateSelectionInfo();

          // Add to sidebar
          const sidebar = document.querySelector('.popup-sidebar-section');
          const newItem = document.createElement('div');
          newItem.className = 'saved-group-item selected';
          newItem.dataset.groupId = data.group.id;
          newItem.innerHTML = `
                    <div class="group-icon">
                        <i class="fas fa-layer-group"></i>
                    </div>
                    <div class="group-info">
                        <div class="group-name">${this.escapeHtml(data.group.name)}</div>
                        <div class="group-meta">${data.group.logic_operator} - 0 rules</div>
                    </div>
                `;
          newItem.addEventListener('click', () => this.selectGroup(data.group.id));
          sidebar.appendChild(newItem);
        }
      })
      .catch(err => {
        console.error('Error creating group:', err);
        AdminModal.alert({ message: this.config.translations.error, type: 'error' });
      });
  }

  applyRules() {
    // Collect current configuration
    const config = {
      groupId: this.selectedGroupId,
      rules: [],
    };

    // Collect rules from canvas
    document.querySelectorAll('.rule-preview-card[data-rule-type]').forEach(card => {
      config.rules.push({
        rule_type: card.dataset.ruleType,
        operator: card.querySelector('.operator-select')?.value || 'equals',
        value: card.querySelector('.value-input')?.value || '',
      });
    });

    // Send to parent window
    if (window.parent && window.parent.applyVisibilityRules) {
      window.parent.applyVisibilityRules(config);
    }
  }

  updateSelectionInfo() {
    const info = document.getElementById('selectionInfo');
    const ruleCards = document.querySelectorAll('.rule-preview-card:not(.group-card)');

    if (this.selectedGroupId) {
      info.textContent = this.config.translations.groupSelected;
    } else if (ruleCards.length > 0) {
      info.textContent = `${ruleCards.length} ${this.config.translations.rulesSelected}`;
    } else {
      info.textContent = this.config.translations.noRulesSelected;
    }
  }

  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  getCSRFToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    if (meta && meta.content) return meta.content;
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
  }
}

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
  const configEl = document.getElementById('rule-builder-popup-config');
  let config;
  if (configEl) {
    try {
      config = JSON.parse(configEl.textContent);
    } catch (e) {
      config = {};
    }
  } else {
    config = window.RuleBuilderPopupConfig || {};
  }
  window.ruleBuilderPopup = new RuleBuilderPopup(config);
});
