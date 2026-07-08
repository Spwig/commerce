/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * ContentManager - Manages element content and styles for undo/redo
 * Works alongside StateManager which handles structure/positions
 */

class ContentManager {
    constructor() {
        this.contentSnapshots = new Map(); // elementId -> content history
        this.currentContent = new Map(); // elementId -> current content
        this.subscribers = [];
        this.initialized = false;
    }

    /**
     * Initialize ContentManager
     */
    init() {
        if (this.initialized) return;

        console.log('ContentManager initializing...');
        this.loadCurrentContent();
        this.initialized = true;
        console.log('ContentManager initialized');
    }

    /**
     * Load current content from DOM
     */
    loadCurrentContent() {
        const elements = document.querySelectorAll('[data-element-id]');
        elements.forEach(element => {
            const elementId = element.dataset.elementId;
            this.currentContent.set(elementId, this.extractElementContent(element));
        });
        console.log(`Loaded content for ${this.currentContent.size} elements`);
    }

    /**
     * Load content for a single element
     */
    loadElementContent(elementId) {
        const element = document.querySelector(`[data-element-id="${elementId}"]`);
        if (element) {
            const content = this.extractElementContent(element);
            this.currentContent.set(elementId, content);
            console.log(`Loaded content for element ${elementId}`);
            return content;
        }
        return null;
    }

    /**
     * Extract content from a DOM element
     */
    extractElementContent(element) {
        if (!element) return null;

        const elementType = element.dataset.elementType;
        const content = {};

        // Extract based on element type
        switch (elementType) {
            case 'text':
            case 'heading':
                const textEl = element.querySelector('.text-content, .heading-content, p, h1, h2, h3, h4, h5, h6');
                if (textEl) {
                    content.text = textEl.textContent;
                    content.html = textEl.innerHTML;
                }
                break;

            case 'image':
                const imgEl = element.querySelector('img');
                if (imgEl) {
                    content.src = imgEl.src;
                    content.alt = imgEl.alt;
                    content.width = imgEl.width;
                    content.height = imgEl.height;
                }
                break;

            case 'button':
                const btnEl = element.querySelector('.btn, button');
                if (btnEl) {
                    content.text = btnEl.textContent;
                    content.href = btnEl.href || btnEl.dataset.href;
                    content.target = btnEl.target;
                }
                break;

            case 'container':
                content.layout = element.dataset.layout || 'flex';
                content.gap = element.dataset.gap;
                break;

            case 'hero':
            case 'feature':
                // Complex components might have multiple content pieces
                const title = element.querySelector('.title, h1, h2');
                const subtitle = element.querySelector('.subtitle, p');
                if (title) content.title = title.textContent;
                if (subtitle) content.subtitle = subtitle.textContent;
                break;
        }

        // Extract styles (computed styles that might change)
        const styles = window.getComputedStyle(element);
        content.styles = {
            backgroundColor: styles.backgroundColor,
            color: styles.color,
            fontSize: styles.fontSize,
            fontWeight: styles.fontWeight,
            padding: styles.padding,
            margin: styles.margin,
            border: styles.border,
            borderRadius: styles.borderRadius,
            width: styles.width,
            height: styles.height,
            display: styles.display,
            position: styles.position
        };

        // Extract custom data attributes
        content.attributes = {};
        for (const key in element.dataset) {
            if (key !== 'elementId' && key !== 'elementType') {
                content.attributes[key] = element.dataset[key];
            }
        }

        return {
            elementId: element.dataset.elementId,
            elementType: elementType,
            content: content,
            timestamp: Date.now()
        };
    }

    /**
     * Capture content snapshot for an element
     */
    captureContent(elementId) {
        const element = document.querySelector(`[data-element-id="${elementId}"]`);
        if (!element) {
            console.warn(`Element ${elementId} not found for content capture`);
            return null;
        }

        const snapshot = this.extractElementContent(element);

        // Store in history
        if (!this.contentSnapshots.has(elementId)) {
            this.contentSnapshots.set(elementId, []);
        }

        return snapshot;
    }

    /**
     * Capture all content (for full page snapshot)
     */
    captureAllContent() {
        const snapshot = new Map();
        const elements = document.querySelectorAll('[data-element-id]');

        elements.forEach(element => {
            const elementId = element.dataset.elementId;
            const content = this.extractElementContent(element);
            if (content) {
                snapshot.set(elementId, content);
            }
        });

        return snapshot;
    }

    /**
     * Restore content for an element
     */
    restoreContent(elementId, snapshot) {
        if (!snapshot) return false;

        const element = document.querySelector(`[data-element-id="${elementId}"]`);
        if (!element) {
            console.warn(`Element ${elementId} not found for content restore`);
            return false;
        }

        const elementType = element.dataset.elementType;
        const content = snapshot.content;

        // Restore based on element type
        switch (elementType) {
            case 'text':
            case 'heading':
                const textEl = element.querySelector('.text-content, .heading-content, p, h1, h2, h3, h4, h5, h6');
                if (textEl && content.html) {
                    textEl.innerHTML = content.html;
                } else if (textEl && content.text) {
                    textEl.textContent = content.text;
                }
                break;

            case 'image':
                const imgEl = element.querySelector('img');
                if (imgEl) {
                    if (content.src) imgEl.src = content.src;
                    if (content.alt) imgEl.alt = content.alt;
                    if (content.width) imgEl.width = content.width;
                    if (content.height) imgEl.height = content.height;
                }
                break;

            case 'button':
                const btnEl = element.querySelector('.btn, button');
                if (btnEl) {
                    if (content.text) btnEl.textContent = content.text;
                    if (content.href) {
                        if (btnEl.tagName === 'A') {
                            btnEl.href = content.href;
                        } else {
                            btnEl.dataset.href = content.href;
                        }
                    }
                    if (content.target) btnEl.target = content.target;
                }
                break;

            case 'hero':
            case 'feature':
                const title = element.querySelector('.title, h1, h2');
                const subtitle = element.querySelector('.subtitle, p');
                if (title && content.title) title.textContent = content.title;
                if (subtitle && content.subtitle) subtitle.textContent = content.subtitle;
                break;
        }

        // Restore custom data attributes
        if (content.attributes) {
            for (const key in content.attributes) {
                element.dataset[key] = content.attributes[key];
            }
        }

        // Update current content cache
        this.currentContent.set(elementId, snapshot);

        // Notify subscribers
        this.notifySubscribers({
            type: 'CONTENT_RESTORED',
            elementId: elementId,
            content: content
        });

        return true;
    }

    /**
     * Restore all content from a full snapshot
     */
    restoreAllContent(snapshot) {
        if (!snapshot || !(snapshot instanceof Map)) return false;

        let restored = 0;
        snapshot.forEach((content, elementId) => {
            if (this.restoreContent(elementId, content)) {
                restored++;
            }
        });

        console.log(`Restored content for ${restored} elements`);
        return restored > 0;
    }

    /**
     * Update content for an element (for tracking changes)
     */
    updateContent(elementId, newContent) {
        const element = document.querySelector(`[data-element-id="${elementId}"]`);
        if (!element) return false;

        // Capture current state before update
        const beforeSnapshot = this.extractElementContent(element);

        // Store the update
        this.currentContent.set(elementId, {
            ...beforeSnapshot,
            content: { ...beforeSnapshot.content, ...newContent },
            timestamp: Date.now()
        });

        // Notify subscribers
        this.notifySubscribers({
            type: 'CONTENT_UPDATED',
            elementId: elementId,
            before: beforeSnapshot,
            after: this.currentContent.get(elementId)
        });

        return true;
    }

    /**
     * Get current content for an element
     */
    getContent(elementId) {
        return this.currentContent.get(elementId);
    }

    /**
     * Check if content has changed
     */
    hasContentChanged(elementId, snapshot) {
        const current = this.getContent(elementId);
        if (!current || !snapshot) return false;

        return JSON.stringify(current.content) !== JSON.stringify(snapshot.content);
    }

    /**
     * Subscribe to content changes
     */
    subscribe(callback) {
        this.subscribers.push(callback);
        return () => {
            this.subscribers = this.subscribers.filter(sub => sub !== callback);
        };
    }

    /**
     * Notify all subscribers
     */
    notifySubscribers(change) {
        this.subscribers.forEach(callback => {
            try {
                callback(change);
            } catch (error) {
                console.error('Error in content subscriber:', error);
            }
        });
    }

    /**
     * Clear all content data
     */
    clear() {
        this.contentSnapshots.clear();
        this.currentContent.clear();
        console.log('ContentManager cleared');
    }

    /**
     * Get memory usage info
     */
    getMemoryInfo() {
        return {
            currentContentSize: this.currentContent.size,
            snapshotCount: this.contentSnapshots.size,
            totalSnapshots: Array.from(this.contentSnapshots.values()).reduce((sum, arr) => sum + arr.length, 0)
        };
    }
}

// Create global instance
const contentManager = new ContentManager();

// Export for use in other modules
window.contentManager = contentManager;