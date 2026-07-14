/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Debug Panel for StateManager
 * Shows real-time state of elements and their positions
 */

class DebugPanel {
  constructor() {
    this.panel = null;
    this.isVisible = false;
    this.createPanel();
  }

  createPanel() {
    // Create debug panel container
    this.panel = document.createElement('div');
    this.panel.id = 'state-debug-panel';
    this.panel.innerHTML = `
            <div class="debug-panel-header">
                <h3>🐛 StateManager Debug</h3>
                <button id="debug-panel-close">✖</button>
            </div>
            <div class="debug-panel-content">
                <div id="debug-state-tree"></div>
                <div id="debug-last-action"></div>
            </div>
        `;

    // Add styles
    const style = document.createElement('style');
    style.textContent = `
            #state-debug-panel {
                position: fixed;
                top: 60px;
                right: 20px;
                width: 400px;
                max-height: 600px;
                background: white;
                border: 2px solid #333;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                z-index: 10000;
                display: none;
                overflow: hidden;
            }
            #state-debug-panel.visible {
                display: block;
            }
            .debug-panel-header {
                background: #333;
                color: white;
                padding: 10px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .debug-panel-header h3 {
                margin: 0;
                font-size: 14px;
            }
            #debug-panel-close {
                background: none;
                border: none;
                color: white;
                cursor: pointer;
                font-size: 18px;
            }
            .debug-panel-content {
                padding: 10px;
                max-height: 500px;
                overflow-y: auto;
            }
            #debug-state-tree {
                font-family: monospace;
                font-size: 12px;
                line-height: 1.4;
                margin-bottom: 20px;
            }
            .debug-element {
                padding: 2px 0;
                margin-left: 20px;
            }
            .debug-element.root {
                margin-left: 0;
                font-weight: bold;
            }
            .debug-element-id {
                color: #007bff;
            }
            .debug-element-index {
                color: #28a745;
                font-weight: bold;
            }
            .debug-element-type {
                color: #6c757d;
                font-size: 11px;
            }
            #debug-last-action {
                border-top: 1px solid #ddd;
                padding-top: 10px;
                font-size: 12px;
            }
            .debug-action-title {
                font-weight: bold;
                margin-bottom: 5px;
            }
            .debug-action-details {
                color: #495057;
            }
        `;
    document.head.appendChild(style);

    // Add to page
    document.body.appendChild(this.panel);

    // Setup event handlers
    document.getElementById('debug-panel-close').addEventListener('click', () => this.hide());

    // Subscribe to state changes
    if (window.pageStateManager) {
      pageStateManager.subscribe((change, state) => {
        this.updatePanel(change, state);
      });
    }
  }

  show() {
    this.isVisible = true;
    this.panel.classList.add('visible');
    this.updatePanel(null, pageStateManager.getState());
  }

  hide() {
    this.isVisible = false;
    this.panel.classList.remove('visible');
  }

  toggle() {
    if (this.isVisible) {
      this.hide();
    } else {
      this.show();
    }
  }

  updatePanel(change, state) {
    if (!this.isVisible) return;

    console.log('Debug panel updating with change:', change);

    // Get fresh state directly from StateManager to ensure we have current data
    const currentState =
      state || (window.pageStateManager ? window.pageStateManager.getState() : null);
    console.log('Debug panel current state:', currentState);

    // Update state tree
    const treeContainer = document.getElementById('debug-state-tree');
    if (treeContainer && currentState) {
      treeContainer.innerHTML = this.buildStateTree(currentState);
    } else if (!treeContainer) {
      console.error('debug-state-tree element not found');
    }

    // Update last action
    if (change) {
      const actionContainer = document.getElementById('debug-last-action');
      if (actionContainer) {
        actionContainer.innerHTML = `
                    <div class="debug-action-title">Last Action: ${change.type}</div>
                    <div class="debug-action-details">
                        ${this.formatChangeDetails(change)}
                    </div>
                `;
      } else {
        console.error('debug-last-action element not found');
      }
    }
  }

  buildStateTree(state) {
    let html = '<div class="debug-element root">📦 Root Elements</div>';

    // Show root elements with their actual current positions
    state.structure.forEach((elementId, actualIndex) => {
      const element = state.elements[elementId];
      if (element) {
        html += this.buildElementNode(element, actualIndex, 1, state);
      }
    });

    // Show orphaned elements (if any)
    const orphaned = Object.keys(state.elements).filter(id => {
      const element = state.elements[id];
      return !element.parentId && !state.structure.includes(id);
    });

    if (orphaned.length > 0) {
      html += '<div class="debug-element root" style="color: red;">⚠️ Orphaned Elements</div>';
      orphaned.forEach(id => {
        const element = state.elements[id];
        html += this.buildElementNode(element, -1, 1, state);
      });
    }

    return html;
  }

  buildElementNode(element, index, depth, state) {
    const indent = '  '.repeat(depth);
    const hasChildren = element.children && element.children.length > 0;
    const containerSymbol = hasChildren ? '📁' : '📄';

    let html = `
            <div class="debug-element" style="margin-left: ${depth * 20}px;">
                ${containerSymbol} <span class="debug-element-index">[${index}]</span>
                <span class="debug-element-id">#${element.id}</span>
                <span class="debug-element-type">(${element.type})</span>
                ${hasChildren ? `<span style="color: #666; font-size: 11px;"> [${element.children.length} children]</span>` : ''}
            </div>
        `;

    // Add children with their actual current positions
    if (element.children && element.children.length > 0) {
      element.children.forEach((childId, actualChildIndex) => {
        const child = state.elements[childId];
        if (child) {
          html += this.buildElementNode(child, actualChildIndex, depth + 1, state);
        } else {
          html += `
                        <div class="debug-element" style="color: red;">
                            ${indent}  <span class="debug-element-index">[${actualChildIndex}]</span>
                            <span>⚠️ Missing child: ${childId}</span>
                        </div>
                    `;
        }
      });
    }

    return html;
  }

  formatChangeDetails(change) {
    switch (change.type) {
      case 'ELEMENT_MOVED':
        return `
                    Element: ${change.elementId}<br>
                    From: ${change.oldParentId || 'root'}<br>
                    To: ${change.newParentId || 'root'}<br>
                    Index: ${change.newIndex}
                `;
      case 'ELEMENT_ADDED':
        return `
                    Element: ${change.elementId}<br>
                    Parent: ${change.parentId || 'root'}<br>
                    Index: ${change.index}
                `;
      case 'ELEMENT_REMOVED':
        return `
                    Element: ${change.elementId}<br>
                    Parent: ${change.parentId || 'root'}
                `;
      default:
        return JSON.stringify(change, null, 2);
    }
  }
}

// Create global debug panel instance
let debugPanel = null;

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  setTimeout(() => {
    debugPanel = new DebugPanel();

    // Check if debug mode is enabled via query string
    const urlParams = new URLSearchParams(window.location.search);
    const debugEnabled = urlParams.has('debug') || urlParams.has('debug_state');

    // Add keyboard shortcut (Ctrl+Shift+D) only if debug mode is enabled
    if (debugEnabled) {
      document.addEventListener('keydown', e => {
        if (e.ctrlKey && e.shiftKey && e.key === 'D') {
          e.preventDefault();
          debugPanel.toggle();
        }
      });
    }

    if (debugEnabled) {
      // Add debug button to toolbar only if debug mode is enabled
      const toolbar = document.querySelector('.builder-toolbar');
      if (toolbar) {
        const debugBtn = document.createElement('button');
        debugBtn.className = 'btn btn-warning';
        debugBtn.textContent = '🐛 Debug State';
        debugBtn.onclick = () => debugPanel.toggle();
        debugBtn.style.marginLeft = '10px';
        toolbar.appendChild(debugBtn);
      }
      console.log('Debug panel ready! Press Ctrl+Shift+D or click Debug State button');
    } else {
      console.log('Debug panel loaded. Add ?debug or ?debug_state to URL to enable debug button');
    }
  }, 1000);
});

// Export for console access
window.debugPanel = debugPanel;

// Add console debugging helpers
window.dumpState = function () {
  if (!window.pageStateManager) {
    console.error('StateManager not initialized');
    return;
  }

  const state = pageStateManager.getState();
  console.log('=== STATE STRUCTURE ===');
  console.log('Root elements:', state.structure);

  console.log('\n=== ELEMENT HIERARCHY ===');
  state.structure.forEach((elementId, index) => {
    const element = state.elements[elementId];
    if (element) {
      console.log(`[${index}] #${elementId} (${element.type})`);
      if (element.children && element.children.length > 0) {
        element.children.forEach((childId, childIndex) => {
          const child = state.elements[childId];
          if (child) {
            console.log(`  └─[${childIndex}] #${childId} (${child.type})`);
            if (child.children && child.children.length > 0) {
              child.children.forEach((grandchildId, gcIndex) => {
                const grandchild = state.elements[grandchildId];
                if (grandchild) {
                  console.log(`      └─[${gcIndex}] #${grandchildId} (${grandchild.type})`);
                }
              });
            }
          }
        });
      }
    }
  });

  console.log('\n=== PARENT-CHILD MAP ===');
  console.log(state.parentChildMap);

  console.log('\n=== ALL ELEMENTS ===');
  console.table(
    Object.values(state.elements).map(el => ({
      id: el.id,
      type: el.type,
      parent: el.parentId || 'root',
      children: el.children ? el.children.length : 0,
    }))
  );

  return state;
};

console.log('Debug helpers loaded. Use dumpState() to see the current state structure.');
