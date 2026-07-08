/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Campaign Builder
 * Interactive UI for building loyalty campaigns with journey steps, actions, and conditions
 */

class CampaignBuilder {
    constructor(options) {
        this.journeyStepsField = options.journeyStepsField;
        this.actionsField = options.actionsField;
        this.triggerConditionsField = options.triggerConditionsField;
        this.isJourneyCheckbox = options.isJourneyCheckbox;

        this.journeySteps = [];
        this.actions = [];
        this.triggerConditions = {};

        this.init();
    }

    init() {
        // Load existing data
        this.loadData();

        // Set up event listeners
        this.setupEventListeners();

        // Initial render
        this.render();
    }

    loadData() {
        // Load journey steps
        if (this.journeyStepsField && this.journeyStepsField.value) {
            try {
                this.journeySteps = JSON.parse(this.journeyStepsField.value);
            } catch (e) {
                console.error('Failed to parse journey steps:', e);
                this.journeySteps = [];
            }
        }

        // Load actions
        if (this.actionsField && this.actionsField.value) {
            try {
                this.actions = JSON.parse(this.actionsField.value);
            } catch (e) {
                console.error('Failed to parse actions:', e);
                this.actions = [];
            }
        }

        // Load trigger conditions
        if (this.triggerConditionsField && this.triggerConditionsField.value) {
            try {
                this.triggerConditions = JSON.parse(this.triggerConditionsField.value);
            } catch (e) {
                console.error('Failed to parse trigger conditions:', e);
                this.triggerConditions = {};
            }
        }
    }

    setupEventListeners() {
        // Add journey step button
        const addStepBtn = document.getElementById('add-journey-step');
        if (addStepBtn) {
            addStepBtn.addEventListener('click', () => this.addJourneyStep());
        }

        // Add action button
        const addActionBtn = document.getElementById('add-action');
        if (addActionBtn) {
            addActionBtn.addEventListener('click', () => this.addAction());
        }

        // Add trigger condition button
        const addConditionBtn = document.getElementById('add-trigger-condition');
        if (addConditionBtn) {
            addConditionBtn.addEventListener('click', () => this.addTriggerCondition());
        }
    }

    render() {
        this.renderJourneySteps();
        this.renderActions();
        this.renderTriggerConditions();
    }

    // ============================================
    // Journey Steps Management
    // ============================================

    renderJourneySteps() {
        const container = document.getElementById('journey-steps-list');
        if (!container) return;

        if (this.journeySteps.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">📍</div>
                    <div class="empty-state-title">No journey steps yet</div>
                    <div class="empty-state-text">Click "Add Step" to create your first journey step</div>
                </div>
            `;
            return;
        }

        container.innerHTML = this.journeySteps.map((step, index) => this.renderJourneyStep(step, index)).join('');

        // Attach event listeners
        this.attachJourneyStepListeners();
    }

    renderJourneyStep(step, index) {
        const stepNumber = step.step || (index + 1);
        const isCollapsed = step._collapsed || false;

        return `
            <div class="journey-step-card ${isCollapsed ? 'collapsed' : ''}" data-step-index="${index}">
                <div class="journey-step-header" data-action="toggle">
                    <div class="journey-step-title">
                        <span class="step-number">${stepNumber}</span>
                        <span class="step-name">Step ${stepNumber}</span>
                    </div>
                    <div class="step-controls">
                        <button type="button" class="step-control-btn" data-action="toggle">
                            ${isCollapsed ? '▼' : '▲'}
                        </button>
                        <button type="button" class="step-control-btn" data-action="edit">✏️</button>
                        <button type="button" class="step-control-btn delete-btn" data-action="delete">🗑️</button>
                    </div>
                </div>
                <div class="journey-step-body">
                    ${this.renderJourneyStepActions(step)}
                    ${this.renderJourneyStepFlow(step, index)}
                </div>
            </div>
        `;
    }

    renderJourneyStepActions(step) {
        const actions = step.actions || [];
        const actionsHtml = actions.map(action => this.renderActionSummary(action)).join('');

        return `
            <div class="step-section">
                <h4>🎯 Actions (${actions.length})</h4>
                ${actionsHtml || '<p style="color: var(--body-quiet-color); font-size: 13px;">No actions configured</p>'}
            </div>
        `;
    }

    renderJourneyStepFlow(step, index) {
        const hasExitConditions = step.exit_conditions && Object.keys(step.exit_conditions).length > 0;
        const hasBranches = step.branches && step.branches.length > 0;
        const hasNextDelay = step.next_step_delay_days !== undefined;

        return `
            <div class="step-section">
                <h4>🔀 Flow Control</h4>
                ${hasExitConditions ? `<p>✓ Exit conditions configured</p>` : ''}
                ${hasBranches ? `<p>✓ ${step.branches.length} branch(es) configured</p>` : ''}
                ${hasNextDelay ? `<p>⏱️ Delay: ${step.next_step_delay_days} day(s)</p>` : ''}
                ${!hasExitConditions && !hasBranches && !hasNextDelay ? '<p style="color: var(--body-quiet-color); font-size: 13px;">No flow control</p>' : ''}
            </div>
        `;
    }

    renderActionSummary(action) {
        const icons = {
            'award_points': '⭐',
            'send_email': '📧',
            'issue_reward': '🎁',
            'add_to_segment': '👥'
        };

        const icon = icons[action.type] || '•';
        const summary = this.getActionSummary(action);

        return `<p>${icon} ${summary}</p>`;
    }

    getActionSummary(action) {
        switch (action.type) {
            case 'award_points':
                return `Award ${action.points || 0} points`;
            case 'send_email':
                return `Send email: ${action.template || 'No template'}`;
            case 'issue_reward':
                return `Issue reward`;
            case 'add_to_segment':
                return `Add to segment`;
            default:
                return action.type;
        }
    }

    attachJourneyStepListeners() {
        const cards = document.querySelectorAll('.journey-step-card');
        cards.forEach(card => {
            const index = parseInt(card.dataset.stepIndex);

            // Toggle collapse
            const toggleBtns = card.querySelectorAll('[data-action="toggle"]');
            toggleBtns.forEach(btn => {
                btn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    this.toggleJourneyStep(index);
                });
            });

            // Edit
            const editBtn = card.querySelector('[data-action="edit"]');
            if (editBtn) {
                editBtn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    this.editJourneyStep(index);
                });
            }

            // Delete
            const deleteBtn = card.querySelector('[data-action="delete"]');
            if (deleteBtn) {
                deleteBtn.addEventListener('click', (e) => {
                    e.stopPropagation();
                    this.deleteJourneyStep(index);
                });
            }
        });
    }

    toggleJourneyStep(index) {
        this.journeySteps[index]._collapsed = !this.journeySteps[index]._collapsed;
        this.renderJourneySteps();
    }

    addJourneyStep() {
        const newStep = {
            step: this.journeySteps.length + 1,
            actions: [],
            next_step_delay_days: 1
        };

        this.showJourneyStepModal(newStep, (step) => {
            this.journeySteps.push(step);
            this.saveJourneySteps();
            this.renderJourneySteps();
        });
    }

    editJourneyStep(index) {
        const step = { ...this.journeySteps[index] };

        this.showJourneyStepModal(step, (updatedStep) => {
            this.journeySteps[index] = updatedStep;
            this.saveJourneySteps();
            this.renderJourneySteps();
        });
    }

    async deleteJourneyStep(index) {
        if (await AdminModal.confirm({ message: 'Are you sure you want to delete this step?', danger: true, confirmText: 'Delete' })) {
            this.journeySteps.splice(index, 1);
            // Re-number steps
            this.journeySteps.forEach((step, i) => {
                step.step = i + 1;
            });
            this.saveJourneySteps();
            this.renderJourneySteps();
        }
    }

    showJourneyStepModal(step, onSave) {
        // Initialize temporary step actions for this modal session
        this._tempStepActions = step.actions ? [...step.actions] : [];

        const modal = this.createModal('Edit Journey Step', this.renderJourneyStepForm(step));

        // Wire up the global add-step-action function
        window.campaignBuilderAddStepAction = () => {
            this.showActionModal({}, (action) => {
                this._tempStepActions.push(action);
                this._renderStepActions(modal);
            });
        };

        // Render existing step actions into the modal
        this._renderStepActions(modal);

        const saveBtn = modal.querySelector('.save-btn');
        saveBtn.addEventListener('click', () => {
            const formData = this.getJourneyStepFormData(modal);
            onSave(formData);
            modal.remove();
        });

        document.body.appendChild(modal);
    }

    renderJourneyStepForm(step) {
        return `
            <div class="builder-form-group">
                <label>Step Number</label>
                <input type="number" name="step" value="${step.step || 1}" min="1" readonly>
            </div>

            <div class="builder-form-group">
                <label>Actions</label>
                <div id="step-actions-list"></div>
                <button type="button" class="button button-small" onclick="window.campaignBuilderAddStepAction()">+ Add Action</button>
            </div>

            <div class="builder-form-group">
                <label>Next Step Delay (days)</label>
                <input type="number" name="next_step_delay_days" value="${step.next_step_delay_days || 1}" min="0">
                <span class="help-text">Days to wait before moving to next step</span>
            </div>

            <div class="builder-form-group">
                <label>
                    <input type="checkbox" name="has_conditions" ${step.conditions ? 'checked' : ''}>
                    Enable Step Conditions
                </label>
                <span class="help-text">Only execute this step if conditions are met</span>
            </div>

            <div class="builder-form-group">
                <label>
                    <input type="checkbox" name="has_branches" ${step.branches && step.branches.length > 0 ? 'checked' : ''}>
                    Enable Branching
                </label>
                <span class="help-text">Send members to different steps based on conditions</span>
            </div>

            <div class="builder-form-group">
                <label>
                    <input type="checkbox" name="has_exit_conditions" ${step.exit_conditions ? 'checked' : ''}>
                    Enable Exit Conditions
                </label>
                <span class="help-text">Exit journey if conditions are met</span>
            </div>
        `;
    }

    getJourneyStepFormData(modal) {
        const form = modal.querySelector('.builder-modal-content');
        const data = {
            step: parseInt(form.querySelector('[name="step"]').value),
            actions: this._tempStepActions || [],
            next_step_delay_days: parseInt(form.querySelector('[name="next_step_delay_days"]').value) || 0
        };

        return data;
    }

    _renderStepActions(modal) {
        const container = modal.querySelector('#step-actions-list');
        if (!container) return;

        if (this._tempStepActions.length === 0) {
            container.innerHTML = '<p style="color: var(--body-quiet-color); font-size: 13px;">No actions configured for this step</p>';
            return;
        }

        container.innerHTML = this._tempStepActions.map((action, index) => {
            const icons = {
                'award_points': '\u2B50',
                'send_email': '\uD83D\uDCE7',
                'issue_reward': '\uD83C\uDF81',
                'add_to_segment': '\uD83D\uDC65'
            };
            const icon = icons[action.type] || '\uD83C\uDFAF';
            const details = this.getActionDetails(action);
            const typeName = action.type.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());

            return `
                <div class="action-item" style="display: flex; align-items: center; gap: 8px; padding: 6px 8px; margin-bottom: 4px; background: var(--darkened-bg); border-radius: 4px;">
                    <span>${icon}</span>
                    <span style="flex: 1;"><strong>${typeName}</strong> - ${details}</span>
                    <button type="button" class="step-control-btn" data-step-action="edit" data-index="${index}" style="cursor: pointer; border: none; background: none;">&#9998;</button>
                    <button type="button" class="step-control-btn delete-btn" data-step-action="delete" data-index="${index}" style="cursor: pointer; border: none; background: none; color: var(--delete-button-bg);">&#128465;</button>
                </div>
            `;
        }).join('');

        // Attach edit/delete listeners for step actions
        container.querySelectorAll('[data-step-action="edit"]').forEach(btn => {
            btn.addEventListener('click', () => {
                const idx = parseInt(btn.dataset.index);
                const action = { ...this._tempStepActions[idx] };
                this.showActionModal(action, (updatedAction) => {
                    this._tempStepActions[idx] = updatedAction;
                    this._renderStepActions(modal);
                });
            });
        });

        container.querySelectorAll('[data-step-action="delete"]').forEach(btn => {
            btn.addEventListener('click', async () => {
                const idx = parseInt(btn.dataset.index);
                if (await AdminModal.confirm({ message: 'Delete this action?', danger: true, confirmText: 'Delete' })) {
                    this._tempStepActions.splice(idx, 1);
                    this._renderStepActions(modal);
                }
            });
        });
    }

    saveJourneySteps() {
        if (this.journeyStepsField) {
            this.journeyStepsField.value = JSON.stringify(this.journeySteps);
        }
    }

    // ============================================
    // Actions Management
    // ============================================

    renderActions() {
        const container = document.getElementById('actions-list');
        if (!container) return;

        if (this.actions.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">🎯</div>
                    <div class="empty-state-title">No actions configured</div>
                    <div class="empty-state-text">Click "Add Action" to define what happens when this campaign triggers</div>
                </div>
            `;
            return;
        }

        container.innerHTML = this.actions.map((action, index) => this.renderAction(action, index)).join('');
        this.attachActionListeners();
    }

    renderAction(action, index) {
        const icons = {
            'award_points': '⭐',
            'send_email': '📧',
            'issue_reward': '🎁',
            'add_to_segment': '👥'
        };

        const icon = icons[action.type] || '🎯';
        const typeName = action.type.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        const details = this.getActionDetails(action);

        return `
            <div class="action-item" data-action-index="${index}">
                <div class="action-icon">${icon}</div>
                <div class="action-content">
                    <div class="action-type">${typeName}</div>
                    <div class="action-details">${details}</div>
                </div>
                <div class="action-controls">
                    <button type="button" class="step-control-btn" data-action="edit">✏️</button>
                    <button type="button" class="step-control-btn delete-btn" data-action="delete">🗑️</button>
                </div>
            </div>
        `;
    }

    getActionDetails(action) {
        switch (action.type) {
            case 'award_points':
                return `${action.points || 0} points${action.reason ? ` - ${action.reason}` : ''}`;
            case 'send_email':
                return `Template: ${action.template || 'Not specified'}`;
            case 'issue_reward':
                return `Reward ID: ${action.reward_id || 'Not specified'}`;
            case 'add_to_segment':
                return `Segment ID: ${action.segment_id || 'Not specified'}`;
            default:
                return 'No details';
        }
    }

    attachActionListeners() {
        const items = document.querySelectorAll('.action-item');
        items.forEach(item => {
            const index = parseInt(item.dataset.actionIndex);

            const editBtn = item.querySelector('[data-action="edit"]');
            if (editBtn) {
                editBtn.addEventListener('click', () => this.editAction(index));
            }

            const deleteBtn = item.querySelector('[data-action="delete"]');
            if (deleteBtn) {
                deleteBtn.addEventListener('click', () => this.deleteAction(index));
            }
        });
    }

    addAction() {
        this.showActionModal({}, (action) => {
            this.actions.push(action);
            this.saveActions();
            this.renderActions();
        });
    }

    editAction(index) {
        const action = { ...this.actions[index] };
        this.showActionModal(action, (updatedAction) => {
            this.actions[index] = updatedAction;
            this.saveActions();
            this.renderActions();
        });
    }

    async deleteAction(index) {
        if (await AdminModal.confirm({ message: 'Are you sure you want to delete this action?', danger: true, confirmText: 'Delete' })) {
            this.actions.splice(index, 1);
            this.saveActions();
            this.renderActions();
        }
    }

    showActionModal(action, onSave) {
        const modal = this.createModal('Configure Action', this.renderActionForm(action));

        const saveBtn = modal.querySelector('.save-btn');
        const typeSelect = modal.querySelector('[name="action_type"]');

        // Update form when type changes
        typeSelect.addEventListener('change', () => {
            const formContainer = modal.querySelector('.action-form-fields');
            formContainer.innerHTML = this.renderActionTypeFields(typeSelect.value, action);
        });

        saveBtn.addEventListener('click', () => {
            const formData = this.getActionFormData(modal);
            onSave(formData);
            modal.remove();
        });

        document.body.appendChild(modal);
    }

    renderActionForm(action) {
        return `
            <div class="builder-form-group">
                <label>Action Type</label>
                <select name="action_type">
                    <option value="">Select action type...</option>
                    <option value="award_points" ${action.type === 'award_points' ? 'selected' : ''}>Award Points</option>
                    <option value="send_email" ${action.type === 'send_email' ? 'selected' : ''}>Send Email</option>
                    <option value="issue_reward" ${action.type === 'issue_reward' ? 'selected' : ''}>Issue Reward</option>
                    <option value="add_to_segment" ${action.type === 'add_to_segment' ? 'selected' : ''}>Add to Segment</option>
                </select>
            </div>
            <div class="action-form-fields">
                ${this.renderActionTypeFields(action.type, action)}
            </div>
        `;
    }

    renderActionTypeFields(type, action) {
        switch (type) {
            case 'award_points':
                return `
                    <div class="builder-form-group">
                        <label>Points</label>
                        <input type="number" name="points" value="${action.points || 0}" min="0" required>
                    </div>
                    <div class="builder-form-group">
                        <label>Reason (optional)</label>
                        <input type="text" name="reason" value="${action.reason || ''}" placeholder="e.g., Birthday bonus">
                    </div>
                `;
            case 'send_email':
                return `
                    <div class="builder-form-group">
                        <label>Email Template</label>
                        <input type="text" name="template" value="${action.template || ''}" placeholder="e.g., loyalty_welcome" required>
                        <span class="help-text">Template code name from email system</span>
                    </div>
                `;
            case 'issue_reward':
                return `
                    <div class="builder-form-group">
                        <label>Reward ID</label>
                        <input type="number" name="reward_id" value="${action.reward_id || ''}" required>
                    </div>
                `;
            case 'add_to_segment':
                return `
                    <div class="builder-form-group">
                        <label>Segment ID</label>
                        <input type="number" name="segment_id" value="${action.segment_id || ''}" required>
                    </div>
                `;
            default:
                return '<p style="color: var(--body-quiet-color);">Select an action type to configure</p>';
        }
    }

    getActionFormData(modal) {
        const form = modal.querySelector('.builder-modal-content');
        const type = form.querySelector('[name="action_type"]').value;
        const data = { type };

        switch (type) {
            case 'award_points':
                data.points = parseInt(form.querySelector('[name="points"]').value);
                data.reason = form.querySelector('[name="reason"]').value;
                break;
            case 'send_email':
                data.template = form.querySelector('[name="template"]').value;
                break;
            case 'issue_reward':
                data.reward_id = parseInt(form.querySelector('[name="reward_id"]').value);
                break;
            case 'add_to_segment':
                data.segment_id = parseInt(form.querySelector('[name="segment_id"]').value);
                break;
        }

        return data;
    }

    saveActions() {
        if (this.actionsField) {
            this.actionsField.value = JSON.stringify(this.actions);
        }
    }

    // ============================================
    // Trigger Conditions Management
    // ============================================

    renderTriggerConditions() {
        const container = document.getElementById('trigger-conditions-list');
        if (!container) return;

        const hasConditions = Object.keys(this.triggerConditions).length > 0;

        if (!hasConditions) {
            container.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">⚡</div>
                    <div class="empty-state-title">No trigger conditions</div>
                    <div class="empty-state-text">Campaign will trigger for all eligible members</div>
                </div>
            `;
            return;
        }

        container.innerHTML = Object.entries(this.triggerConditions).map(([key, value]) => {
            return this.renderCondition(key, value);
        }).join('');
    }

    renderCondition(key, value) {
        const label = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        return `
            <div class="condition-item">
                <div class="condition-icon">⚡</div>
                <div class="condition-content">
                    <div class="condition-type">${label}</div>
                    <div class="condition-details">Value: ${value}</div>
                </div>
                <div class="condition-controls">
                    <button type="button" class="step-control-btn delete-btn" onclick="window.campaignBuilderDeleteCondition('${key}')">🗑️</button>
                </div>
            </div>
        `;
    }

    async addTriggerCondition() {
        // Simplified version - just show prompt for now
        const key = await AdminModal.prompt('Condition key (e.g., min_order_amount):');
        if (!key) return;

        const value = await AdminModal.prompt('Condition value:');
        if (value === null) return;

        this.triggerConditions[key] = value;
        this.saveTriggerConditions();
        this.renderTriggerConditions();
    }

    saveTriggerConditions() {
        if (this.triggerConditionsField) {
            this.triggerConditionsField.value = JSON.stringify(this.triggerConditions);
        }
    }

    // ============================================
    // Modal Utilities
    // ============================================

    createModal(title, content) {
        const modal = document.createElement('div');
        modal.className = 'builder-modal';
        modal.innerHTML = `
            <div class="builder-modal-content">
                <div class="builder-modal-header">
                    <h3 class="builder-modal-title">${title}</h3>
                    <button type="button" class="builder-modal-close">×</button>
                </div>
                <div class="builder-modal-body">
                    ${content}
                </div>
                <div class="builder-modal-footer">
                    <button type="button" class="button button-secondary cancel-btn">Cancel</button>
                    <button type="button" class="button save-btn">Save</button>
                </div>
            </div>
        `;

        // Close button
        modal.querySelector('.builder-modal-close').addEventListener('click', () => modal.remove());
        modal.querySelector('.cancel-btn').addEventListener('click', () => modal.remove());

        // Close on backdrop click
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.remove();
            }
        });

        return modal;
    }
}

// Export to window for global access
window.CampaignBuilder = CampaignBuilder;

// Global helper functions (called from rendered HTML)
window.campaignBuilderDeleteCondition = function(key) {
    if (window.campaignBuilderInstance) {
        delete window.campaignBuilderInstance.triggerConditions[key];
        window.campaignBuilderInstance.saveTriggerConditions();
        window.campaignBuilderInstance.renderTriggerConditions();
    }
};
