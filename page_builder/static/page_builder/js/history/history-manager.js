/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Enhanced History Manager for Undo/Redo
 * Manages command execution with DOM state tracking
 */

class HistoryManager {
  constructor(options = {}) {
    this.maxSize = options.maxSize || 50; // Increased from 25
    this.undoStack = [];
    this.redoStack = [];
    this.isExecuting = false;
    this.isBulkOperation = false; // Flag to prevent DOM rebuilds during bulk operations
    this.domSnapshot = new DOMSnapshot();
    this.listeners = [];
    this.batchMode = false;
    this.batchCommands = [];

    // Initialize DOM snapshot
    this.domSnapshot.init();

    // Capture initial state after DOM is ready
    this.captureInitialState();
  }

  /**
   * Capture the initial state of the page for the first undo
   */
  captureInitialState() {
    // Use a small delay to ensure DOM is fully loaded
    setTimeout(() => {
      const initialSnapshot = this.domSnapshot.capture();
      console.log('📸 Captured initial page snapshot for history');

      // Store as a special initial state that can be restored
      this._initialSnapshot = initialSnapshot;
    }, 100);
  }

  /**
   * Execute a command with DOM state tracking
   */
  async execute(command, skipSnapshot = false) {
    if (this.isExecuting) {
      console.warn('Command execution already in progress');
      return false;
    }

    // If in batch mode, queue the command
    if (this.batchMode) {
      this.batchCommands.push(command);
      return true;
    }

    this.isExecuting = true;

    try {
      // Take before snapshot
      if (!skipSnapshot) {
        command.beforeSnapshot = this.domSnapshot.capture();
      }

      // Execute the command
      await command.execute();

      // Take after snapshot
      if (!skipSnapshot) {
        command.afterSnapshot = this.domSnapshot.capture();
        console.log('📸 Captured afterSnapshot for command');
      } else {
        console.log('⏭️ Skipping afterSnapshot capture (skipSnapshot=true)');
      }

      // Add to undo stack
      this.undoStack.push(command);

      // Limit stack size
      if (this.undoStack.length > this.maxSize) {
        this.undoStack.shift();
      }

      // Clear redo stack when new action is performed
      this.redoStack = [];

      // Notify listeners
      this.notifyListeners('execute', command);

      return true;
    } catch (error) {
      console.error('Command execution failed:', error);

      // Attempt to restore previous state
      if (command.beforeSnapshot) {
        await this.domSnapshot.restore(command.beforeSnapshot);
      }

      throw error;
    } finally {
      this.isExecuting = false;
      // Update UI after isExecuting is set to false so canUndo() works correctly
      this.updateUI();
    }
  }

  /**
   * Start batch mode for grouping commands
   */
  startBatch(description = 'Batch Operation') {
    this.batchMode = true;
    this.batchCommands = [];
    this.batchDescription = description;
  }

  /**
   * End batch mode and execute all queued commands as one
   */
  async endBatch() {
    if (!this.batchMode) return;

    this.batchMode = false;

    if (this.batchCommands.length > 0) {
      const batchCommand = new BatchCommand(this.batchCommands, this.batchDescription);
      await this.execute(batchCommand);
    }

    this.batchCommands = [];
    this.batchDescription = '';
  }

  /**
   * Undo last command
   */
  async undo() {
    if (!this.canUndo()) {
      // If we have an initial snapshot and nothing in undo stack,
      // restore to initial state
      if (this._initialSnapshot && this.undoStack.length === 0) {
        console.log('🔄 Restoring to initial page state');
        await this.domSnapshot.restore(this._initialSnapshot);
        this.notifyListeners();
        return true;
      }
      return false;
    }

    this.isExecuting = true;

    try {
      const command = this.undoStack.pop();

      // Use snapshot if available, otherwise call undo method
      if (command.beforeSnapshot) {
        await this.domSnapshot.restore(command.beforeSnapshot);

        // Also call the command's undo for API sync
        if (command.undo) {
          await command.undo(true); // true = skip DOM updates
        }
      } else if (command.undo) {
        await command.undo();
      }
      // If no snapshot and no undo method, try initial snapshot
      else if (this.undoStack.length === 0 && this._initialSnapshot) {
        console.log('🔄 No command snapshot, restoring to initial state');
        await this.domSnapshot.restore(this._initialSnapshot);
      }

      // Move to redo stack
      this.redoStack.push(command);

      // Notify listeners
      this.notifyListeners('undo', command);

      return true;
    } catch (error) {
      console.error('Undo failed:', error);
      return false;
    } finally {
      this.isExecuting = false;
      // Update UI after isExecuting is set to false so canRedo() works correctly
      this.updateUI();
    }
  }

  /**
   * Redo last undone command
   */
  async redo() {
    if (!this.canRedo()) return false;

    console.log('🔄 Redo: Setting isExecuting = true');
    this.isExecuting = true;

    try {
      const command = this.redoStack.pop();
      console.log('📍 Redo command:', {
        description: command.getDescription ? command.getDescription() : 'Unknown',
        hasAfterSnapshot: !!command.afterSnapshot,
        hasExecuteMethod: !!command.execute,
      });

      // Use snapshot if available, otherwise call execute method
      if (command.afterSnapshot) {
        console.log('  ↻ Restoring DOM from afterSnapshot');
        await this.domSnapshot.restore(command.afterSnapshot);

        // Also call the command's execute for API sync
        if (command.execute) {
          console.log('  ↻ Calling execute for API sync (skipDOM=true)');
          await command.execute(true); // true = skip DOM updates
        }
      } else if (command.execute) {
        await command.execute();
      }

      // Move back to undo stack
      this.undoStack.push(command);

      // Notify listeners
      this.notifyListeners('redo', command);

      return true;
    } catch (error) {
      console.error('Redo failed:', error);
      return false;
    } finally {
      this.isExecuting = false;
      // Update UI after isExecuting is set to false so canUndo() works correctly
      this.updateUI();
    }
  }

  /**
   * Undo multiple commands at once
   */
  async undoMultiple(count) {
    console.log('🔄 undoMultiple called:', {
      count: count,
      undoStackLength: this.undoStack.length,
      canProcess: count > 0 && count <= this.undoStack.length,
    });

    if (count <= 0 || count > this.undoStack.length) {
      console.warn('⚠️ Invalid count for undoMultiple:', count);
      return false;
    }

    this.isExecuting = true;
    this.isBulkOperation = true; // Set flag to prevent DOM rebuilds
    console.log('🔒 Setting isExecuting = true, isBulkOperation = true');

    try {
      // Take snapshot before bulk undo
      const beforeBulkSnapshot = this.domSnapshot.capture();
      console.log('📸 Captured bulk operation snapshot');

      console.log(`🔁 Processing ${count} undo operations`);

      // Store the snapshot we want to restore to
      let targetSnapshot = null;
      const commandsToProcess = [];

      // First, collect all commands we'll be undoing (in reverse order)
      for (let i = 0; i < count; i++) {
        commandsToProcess.push(this.undoStack.pop());
      }

      // Process commands and find the target snapshot
      for (let i = 0; i < commandsToProcess.length; i++) {
        const command = commandsToProcess[i];
        const isOldestCommand = i === commandsToProcess.length - 1;

        console.log(`  [${i + 1}/${count}] Processing:`, {
          description: command.getDescription ? command.getDescription() : 'Unknown',
          hasBeforeSnapshot: !!command.beforeSnapshot,
          hasUndoMethod: !!command.undo,
          isOldestCommand: isOldestCommand,
        });

        // Capture the beforeSnapshot from the OLDEST command (last one we process)
        // This is the state we want to restore to - before ALL the operations
        if (isOldestCommand && command.beforeSnapshot) {
          targetSnapshot = command.beforeSnapshot;
          console.log(
            '  📸 Captured target snapshot from oldest command (state before all operations)'
          );
        }

        // Call undo for API sync but skip DOM updates for all commands
        if (command.undo) {
          console.log('  ↻ Calling undo method (skipping DOM)');
          await command.undo(true); // Skip DOM updates for all commands
        } else {
          console.warn('  ⚠️ Command has no undo capability');
        }

        this.redoStack.push(command);
      }

      // After processing all commands, restore the DOM to the target state
      if (targetSnapshot) {
        console.log('  ↻ Restoring DOM to state before all operations');
        await this.domSnapshot.restore(targetSnapshot);
      } else {
        console.warn('  ⚠️ No snapshot available for restoration');
      }

      // Clear bulk operation flag after DOM restoration is complete
      this.isBulkOperation = false;
      console.log('✅ undoMultiple completed successfully, isBulkOperation = false');

      // Notify listeners
      this.notifyListeners('undoMultiple', { count });

      return true;
    } catch (error) {
      console.error('❌ Multiple undo failed:', error);
      this.isBulkOperation = false; // Ensure flag is cleared on error
      return false;
    } finally {
      console.log('🔓 Setting isExecuting = false');
      this.isExecuting = false;
      // Update UI after isExecuting is set to false
      this.updateUI();
    }
  }

  /**
   * Redo multiple commands at once
   */
  async redoMultiple(count) {
    console.log('🔄 redoMultiple called:', {
      count: count,
      redoStackLength: this.redoStack.length,
      canProcess: count > 0 && count <= this.redoStack.length,
    });

    if (count <= 0 || count > this.redoStack.length) {
      console.warn('⚠️ Invalid count for redoMultiple:', count);
      return false;
    }

    this.isExecuting = true;
    this.isBulkOperation = true; // Set flag to prevent DOM rebuilds
    console.log('🔒 Setting isExecuting = true, isBulkOperation = true');

    try {
      console.log(`🔁 Processing ${count} redo operations`);

      // Store the snapshot we want to restore to (from the LAST command)
      let targetSnapshot = null;
      const commandsToRedo = [];

      // First, collect all commands
      for (let i = 0; i < count; i++) {
        commandsToRedo.push(this.redoStack.pop());
      }

      // Find the target snapshot from the LAST command in our collection
      // Since we're redoing in sequence, this gives us the final cumulative state
      const lastCommand = commandsToRedo[commandsToRedo.length - 1];
      if (lastCommand && lastCommand.afterSnapshot) {
        targetSnapshot = lastCommand.afterSnapshot;
        console.log('  📸 Captured target snapshot from last command (final cumulative state)');
      }

      // Process commands in order
      for (let i = 0; i < commandsToRedo.length; i++) {
        const command = commandsToRedo[i];
        console.log(`  [${i + 1}/${count}] Processing:`, {
          description: command.getDescription ? command.getDescription() : 'Unknown',
          hasAfterSnapshot: !!command.afterSnapshot,
          hasExecuteMethod: !!command.execute,
          isLastCommand: i === commandsToRedo.length - 1,
        });

        // Call execute for API sync but skip DOM updates for all commands
        if (command.execute) {
          console.log('  ↻ Calling execute method (skipping DOM)');
          await command.execute(true); // Skip DOM updates for all commands
        } else {
          console.warn('  ⚠️ Command has no execute capability');
        }

        this.undoStack.push(command);
      }

      // After processing all commands, restore the DOM to the target state
      if (targetSnapshot) {
        console.log('  ↻ Restoring DOM to state after all operations');
        await this.domSnapshot.restore(targetSnapshot);
      } else {
        console.warn('  ⚠️ No snapshot available for restoration');
      }

      // Clear bulk operation flag after DOM restoration is complete
      this.isBulkOperation = false;
      console.log('✅ redoMultiple completed successfully, isBulkOperation = false');

      // Notify listeners
      this.notifyListeners('redoMultiple', { count });

      return true;
    } catch (error) {
      console.error('❌ Multiple redo failed:', error);
      this.isBulkOperation = false; // Ensure flag is cleared on error
      return false;
    } finally {
      console.log('🔓 Setting isExecuting = false');
      this.isExecuting = false;
      // Update UI after isExecuting is set to false
      this.updateUI();
    }
  }

  /**
   * Jump to a specific point in history
   */
  async jumpTo(targetIndex) {
    const currentIndex = this.undoStack.length;
    const diff = targetIndex - currentIndex;

    if (diff < 0) {
      return await this.undoMultiple(Math.abs(diff));
    } else if (diff > 0) {
      return await this.redoMultiple(diff);
    }

    return true;
  }

  /**
   * Get undo history with descriptions
   */
  getUndoHistory() {
    const history = this.undoStack
      .slice()
      .reverse()
      .map((cmd, index) => ({
        description: cmd.getDescription
          ? cmd.getDescription()
          : `Action ${this.undoStack.length - index}`,
        index: index + 1,
        timestamp: cmd.timestamp || Date.now(),
        hasSnapshot: !!(cmd.beforeSnapshot || cmd.afterSnapshot),
        command: cmd,
      }));
    console.log('📚 Generated undo history:', {
      count: history.length,
      items: history.map(h => ({
        index: h.index,
        description: h.description,
      })),
    });
    return history;
  }

  /**
   * Get redo history with descriptions
   */
  getRedoHistory() {
    const history = this.redoStack
      .slice()
      .reverse()
      .map((cmd, index) => ({
        description: cmd.getDescription ? cmd.getDescription() : `Action ${index + 1}`,
        index: index + 1,
        timestamp: cmd.timestamp || Date.now(),
        hasSnapshot: !!(cmd.beforeSnapshot || cmd.afterSnapshot),
        command: cmd,
      }));
    console.log('📚 Generated redo history:', {
      count: history.length,
      items: history.map(h => ({
        index: h.index,
        description: h.description,
      })),
    });
    return history;
  }

  /**
   * Get combined history
   */
  getFullHistory() {
    const history = [];

    // Add undo items (past)
    this.undoStack.forEach((cmd, index) => {
      history.push({
        type: 'past',
        description: cmd.getDescription ? cmd.getDescription() : `Action ${index + 1}`,
        index: index,
        timestamp: cmd.timestamp || Date.now(),
        command: cmd,
      });
    });

    // Add current state marker
    history.push({
      type: 'current',
      description: 'Current State',
      index: this.undoStack.length,
      timestamp: Date.now(),
    });

    // Add redo items (future)
    this.redoStack
      .slice()
      .reverse()
      .forEach((cmd, index) => {
        history.push({
          type: 'future',
          description: cmd.getDescription ? cmd.getDescription() : `Action ${index + 1}`,
          index: this.undoStack.length + index + 1,
          timestamp: cmd.timestamp || Date.now(),
          command: cmd,
        });
      });

    return history;
  }

  /**
   * Check if can undo
   */
  canUndo() {
    const result = this.undoStack.length > 0 && !this.isExecuting;
    // Only warn if there's an issue
    if (this.undoStack.length > 0 && this.isExecuting) {
      console.warn('⚠️ canUndo: Stack has items but isExecuting is true');
    }
    return result;
  }

  /**
   * Check if can redo
   */
  canRedo() {
    return this.redoStack.length > 0 && !this.isExecuting;
  }

  /**
   * Clear history
   */
  clear() {
    this.undoStack = [];
    this.redoStack = [];
    this.updateUI();
    this.notifyListeners('clear');
  }

  /**
   * Save history to localStorage
   */
  saveToStorage() {
    try {
      const historyData = {
        undoStack: this.undoStack.map(cmd => ({
          type: cmd.constructor.name,
          data: cmd.serialize ? cmd.serialize() : null,
        })),
        redoStack: this.redoStack.map(cmd => ({
          type: cmd.constructor.name,
          data: cmd.serialize ? cmd.serialize() : null,
        })),
      };

      localStorage.setItem('pageBuilderHistory', JSON.stringify(historyData));
      return true;
    } catch (error) {
      console.error('Failed to save history:', error);
      return false;
    }
  }

  /**
   * Load history from localStorage
   */
  loadFromStorage() {
    try {
      const data = localStorage.getItem('pageBuilderHistory');
      if (!data) return false;

      const historyData = JSON.parse(data);

      // This would need command factory to recreate commands
      // For now, just return false
      console.log('History data found but reconstruction not yet implemented');
      return false;
    } catch (error) {
      console.error('Failed to load history:', error);
      return false;
    }
  }

  /**
   * Add listener for history events
   */
  addListener(callback) {
    this.listeners.push(callback);
  }

  /**
   * Remove listener
   */
  removeListener(callback) {
    this.listeners = this.listeners.filter(l => l !== callback);
  }

  /**
   * Notify all listeners
   */
  notifyListeners(event, data = null) {
    this.listeners.forEach(listener => {
      try {
        listener(event, data);
      } catch (error) {
        console.error('History listener error:', error);
      }
    });
  }

  /**
   * Update UI elements
   */
  updateUI() {
    this.updateButtons();
    this.updateHistoryDropdowns();
    this.updateHistoryPanel();
  }

  /**
   * Update undo/redo buttons
   */
  updateButtons() {
    const undoBtn = document.getElementById('undo-btn');
    const redoBtn = document.getElementById('redo-btn');
    const undoDropdownBtn = document.getElementById('undo-dropdown-btn');
    const redoDropdownBtn = document.getElementById('redo-dropdown-btn');

    // Debug logging
    console.log('🔄 History Manager updating buttons:', {
      canUndo: this.canUndo(),
      canRedo: this.canRedo(),
      undoStackLength: this.undoStack.length,
      redoStackLength: this.redoStack.length,
    });

    if (undoBtn) {
      const canUndo = this.canUndo();
      undoBtn.disabled = !canUndo;
      // Also update CSS classes for styling
      if (canUndo) {
        undoBtn.classList.remove('disabled');
        undoBtn.title = `Undo: ${this.undoStack[this.undoStack.length - 1]?.getDescription?.() || 'Last Action'} (Ctrl+Z)`;
      } else {
        undoBtn.classList.add('disabled');
        undoBtn.title = 'Nothing to undo (Ctrl+Z)';
      }
    }

    if (redoBtn) {
      const canRedo = this.canRedo();
      redoBtn.disabled = !canRedo;
      // Also update CSS classes for styling
      if (canRedo) {
        redoBtn.classList.remove('disabled');
        redoBtn.title = `Redo: ${this.redoStack[this.redoStack.length - 1]?.getDescription?.() || 'Last Action'} (Ctrl+Shift+Z)`;
      } else {
        redoBtn.classList.add('disabled');
        redoBtn.title = 'Nothing to redo (Ctrl+Shift+Z)';
      }
    }

    if (undoDropdownBtn) {
      undoDropdownBtn.disabled = !this.canUndo();
    }

    if (redoDropdownBtn) {
      redoDropdownBtn.disabled = !this.canRedo();
    }
  }

  /**
   * Update history dropdowns
   */
  updateHistoryDropdowns() {
    // Try to update modern timeline first
    const undoTimeline = document.getElementById('undo-history-timeline');
    const redoTimeline = document.getElementById('redo-history-timeline');

    if (undoTimeline || redoTimeline) {
      // Modern UI is present, update will be handled by hover events
      return;
    }

    // Fallback to legacy dropdown update
    const undoList = document.getElementById('undo-history-list');
    if (undoList) {
      const undoHistory = this.getUndoHistory();
      undoList.innerHTML = '';

      undoHistory.forEach(item => {
        const historyItem = document.createElement('div');
        historyItem.className = 'history-item clickable';
        historyItem.innerHTML = `
                    <span class="history-icon">${this.getActionIcon(item.command)}</span>
                    <span class="history-description">${item.description}</span>
                    <span class="history-count" title="Undo ${item.index} action${item.index > 1 ? 's' : ''}">${item.index}</span>
                    ${item.hasSnapshot ? '<span class="history-snapshot-indicator" title="Has state snapshot">💾</span>' : ''}
                `;
        historyItem.dataset.count = item.index;

        // Click to undo to this point
        historyItem.onclick = async e => {
          e.stopPropagation();
          if (item.index > 1 && !(await AdminModal.confirm(`Undo ${item.index} actions?`))) {
            return;
          }
          this.undoMultiple(item.index);
          closeHistoryDropdowns();
        };

        // Hover to preview
        historyItem.onmouseenter = () => {
          this.previewUndo(item.index);
        };
        historyItem.onmouseleave = () => {
          this.clearPreview();
        };

        undoList.appendChild(historyItem);
      });

      if (undoHistory.length === 0) {
        undoList.innerHTML = '<div class="history-empty">No actions to undo</div>';
      }
    }

    // Update redo history
    const redoList = document.getElementById('redo-history-list');
    if (redoList) {
      const redoHistory = this.getRedoHistory();
      redoList.innerHTML = '';

      redoHistory.forEach(item => {
        const historyItem = document.createElement('div');
        historyItem.className = 'history-item';
        historyItem.innerHTML = `
                    <span class="history-description">${item.description}</span>
                    ${item.hasSnapshot ? '<span class="history-snapshot-indicator" title="Has DOM snapshot">📸</span>' : ''}
                `;
        historyItem.dataset.count = item.index;
        historyItem.onclick = () => {
          this.redoMultiple(item.index);
          closeHistoryDropdowns();
        };
        redoList.appendChild(historyItem);
      });

      if (redoHistory.length === 0) {
        redoList.innerHTML = '<div class="history-empty">No actions to redo</div>';
      }
    }
  }

  /**
   * Update history panel (if exists)
   */
  updateHistoryPanel() {
    const panel = document.getElementById('history-panel');
    if (!panel) return;

    const history = this.getFullHistory();
    const content = panel.querySelector('.history-timeline');
    if (!content) return;

    content.innerHTML = '';

    history.forEach(item => {
      const entry = document.createElement('div');
      entry.className = `history-entry history-${item.type}`;
      entry.innerHTML = `
                <div class="history-entry-marker"></div>
                <div class="history-entry-content">
                    <div class="history-entry-description">${item.description}</div>
                    <div class="history-entry-time">${new Date(item.timestamp).toLocaleTimeString()}</div>
                </div>
            `;

      if (item.type !== 'current') {
        entry.onclick = () => this.jumpTo(item.index);
      }

      content.appendChild(entry);
    });
  }

  /**
   * Get icon for action type
   */
  getActionIcon(command) {
    if (!command) return '📝';

    const type = command.constructor?.name || command.type || '';
    switch (type) {
      case 'MoveElementCommand':
        return '↔️';
      case 'AddElementCommand':
        return '➕';
      case 'DeleteElementCommand':
        return '🗑️';
      case 'UpdateElementCommand':
        return '✏️';
      case 'BatchCommand':
        return '📦';
      default:
        return '📝';
    }
  }

  /**
   * Preview what will be undone
   */
  previewUndo(count) {
    // Get elements that will be affected
    const affectedElements = this.getAffectedElements(count);

    // Highlight them
    affectedElements.forEach(elementId => {
      const element = document.querySelector(`[data-element-id="${elementId}"]`);
      if (element) {
        element.classList.add('undo-preview');
      }
    });
  }

  /**
   * Clear preview highlights
   */
  clearPreview() {
    document.querySelectorAll('.undo-preview').forEach(el => {
      el.classList.remove('undo-preview');
    });
  }

  /**
   * Get elements affected by undo operations
   */
  getAffectedElements(count) {
    const affected = new Set();

    for (let i = 0; i < Math.min(count, this.undoStack.length); i++) {
      const command = this.undoStack[this.undoStack.length - 1 - i];

      // Extract element IDs based on command type
      if (command.elementId) {
        affected.add(command.elementId);
      }
      if (command.elementIds) {
        command.elementIds.forEach(id => affected.add(id));
      }
      if (command.commands) {
        // Batch command
        command.commands.forEach(cmd => {
          if (cmd.elementId) affected.add(cmd.elementId);
        });
      }
    }

    return Array.from(affected);
  }
}

/**
 * Batch Command for grouping multiple commands
 */
class BatchCommand {
  constructor(commands, description = 'Batch Operation') {
    this.commands = commands;
    this.description = description;
    this.timestamp = Date.now();
  }

  getDescription() {
    return this.description;
  }

  async execute(skipDOM = false) {
    for (const command of this.commands) {
      await command.execute(skipDOM);
    }
  }

  async undo(skipDOM = false) {
    // Undo in reverse order
    for (let i = this.commands.length - 1; i >= 0; i--) {
      await this.commands[i].undo(skipDOM);
    }
  }
}

// Export for module use
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { HistoryManager, BatchCommand };
}

// Make available globally
window.HistoryManager = HistoryManager;
window.BatchCommand = BatchCommand;
