/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Help System JavaScript Controller
 * Context-aware help with search, categories, and feedback
 */

const HelpSystem = {
  initialized: false,
  currentTopic: null,
  categories: [],
  apiBase: '/api/core',

  /**
   * Get the current UI language from the URL path (e.g., /es/admin/... → 'es')
   */
  getLanguage() {
    const match = window.location.pathname.match(/^\/([a-z]{2}(?:-[a-z]+)?)\//);
    return match ? match[1] : 'en';
  },

  /**
   * Build API URL with language parameter for translation support
   */
  apiUrl(path) {
    const lang = this.getLanguage();
    const separator = path.includes('?') ? '&' : '?';
    return `${this.apiBase}${path}${separator}lang=${lang}`;
  },

  /**
   * Initialize the help system
   */
  init() {
    if (this.initialized) return;

    this.initialized = true;
    this.setupEventListeners();
    this.loadCategories();
    this.loadContextualHelp();
  },

  /**
   * Setup event listeners
   */
  setupEventListeners() {
    // Search input with debounce
    const searchInput = document.getElementById('helpSearchInput');
    if (searchInput) {
      let searchTimeout;
      searchInput.addEventListener('input', e => {
        clearTimeout(searchTimeout);
        const query = e.target.value.trim();

        if (query.length === 0) {
          this.hideSearchResults();
          return;
        }

        if (query.length < 2) return;

        searchTimeout = setTimeout(() => {
          // Progressive enhancement: semantic for 3+ words, keyword for 1-2 words
          const wordCount = query.split(/\s+/).filter(w => w.length > 0).length;
          if (wordCount >= 3) {
            this.semanticSearch(query);
          } else {
            this.searchHelp(query);
          }
        }, 300);
      });
    }

    // Close on escape key
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape') {
        // Close lightbox first if open
        const lightbox = document.querySelector('.help-lightbox');
        if (lightbox) {
          lightbox.remove();
          return;
        }
        const drawer = document.getElementById('helpDrawer');
        if (drawer && drawer.classList.contains('open')) {
          toggleHelpDrawer();
        }
      }
    });

    // Click-to-zoom on help images (event delegation)
    const drawer = document.getElementById('helpDrawer');
    if (drawer) {
      drawer.addEventListener('click', e => {
        if (e.target.classList.contains('help-img')) {
          const overlay = document.createElement('div');
          overlay.className = 'help-lightbox';
          const img = document.createElement('img');
          img.src = e.target.src;
          img.alt = e.target.alt;
          overlay.appendChild(img);
          overlay.addEventListener('click', () => overlay.remove());
          document.body.appendChild(overlay);
        }
      });
    }
  },

  /**
   * Load help categories
   */
  async loadCategories() {
    try {
      const response = await fetch(this.apiUrl('/help/categories/'), {
        method: 'GET',
        headers: this.getHeaders(),
        credentials: 'same-origin', // Include session cookies
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error('API Error:', response.status, errorText);
        throw new Error(`Failed to load categories: ${response.status}`);
      }

      this.categories = await response.json();
      this.renderCategories();
    } catch (error) {
      console.error('Error loading categories:', error);
      this.showError('helpCategories', 'Failed to load help categories. Please refresh the page.');
    }
  },

  /**
   * Load contextual help based on current page
   */
  async loadContextualHelp() {
    try {
      const urlPath = window.location.pathname;
      const response = await fetch(this.apiUrl('/help/topics/contextual/'), {
        method: 'POST',
        headers: this.getHeaders(),
        credentials: 'same-origin',
        body: JSON.stringify({
          url_path: urlPath,
          limit: 5,
        }),
      });

      if (!response.ok) throw new Error('Failed to load contextual help');

      const topics = await response.json();
      this.renderContextualTopics(topics);
    } catch (error) {
      console.error('Error loading contextual help:', error);
      this.showError('helpContextTopics', 'No contextual help available');
    }
  },

  /**
   * Search for help topics
   */
  async searchHelp(query) {
    try {
      this.showLoading('helpSearchResults');
      this.showSearchResults();

      const response = await fetch(this.apiUrl('/help/topics/search/'), {
        method: 'POST',
        headers: this.getHeaders(),
        credentials: 'same-origin',
        body: JSON.stringify({
          query: query,
          limit: 10,
        }),
      });

      if (!response.ok) throw new Error('Search failed');

      const topics = await response.json();

      if (topics.length === 0) {
        this.showNoResults('helpSearchResults');
      } else {
        this.renderTopicsList('helpSearchResults', topics);
      }
    } catch (error) {
      console.error('Error searching help:', error);
      this.showError('helpSearchResults', 'Search failed');
    }
  },

  /**
   * Semantic search for help topics (uses natural language understanding)
   */
  async semanticSearch(query) {
    try {
      this.showLoading('helpSearchResults');
      this.showSearchResults();

      const response = await fetch(this.apiUrl('/help/topics/semantic_search/'), {
        method: 'POST',
        headers: this.getHeaders(),
        credentials: 'same-origin',
        body: JSON.stringify({
          query: query,
          language: this.getLanguage(),
          limit: 10,
        }),
      });

      if (!response.ok) {
        console.warn('Semantic search failed, falling back to keyword search');
        return this.searchHelp(query);
      }

      const data = await response.json();
      const topics = data.results || data;

      if (topics.length === 0) {
        this.showNoResults('helpSearchResults');
      } else {
        this.renderTopicsList('helpSearchResults', topics);
      }
    } catch (error) {
      console.error('Semantic search error:', error);
      this.searchHelp(query); // Fallback to keyword search
    }
  },

  /**
   * Load topic detail
   */
  async loadTopic(slug) {
    try {
      const response = await fetch(this.apiUrl(`/help/topics/${slug}/`), {
        method: 'GET',
        headers: this.getHeaders(),
        credentials: 'same-origin',
      });

      if (!response.ok) throw new Error('Failed to load topic');

      const topic = await response.json();
      this.currentTopic = topic;
      this.renderTopicDetail(topic);
    } catch (error) {
      console.error('Error loading topic:', error);
      this.showError('helpTopicContent', 'Failed to load help topic');
    }
  },

  /**
   * Load topics for a category
   */
  async loadCategoryTopics(categorySlug) {
    try {
      const response = await fetch(this.apiUrl(`/help/categories/${categorySlug}/topics/`), {
        method: 'GET',
        headers: this.getHeaders(),
        credentials: 'same-origin',
      });

      if (!response.ok) throw new Error('Failed to load category topics');

      const topics = await response.json();
      this.renderCategoryTopics(categorySlug, topics);
    } catch (error) {
      console.error('Error loading category topics:', error);
      this.showError('helpCategories', 'Failed to load topics');
    }
  },

  /**
   * Submit feedback
   */
  async submitFeedback(helpful) {
    if (!this.currentTopic) return;

    try {
      const response = await fetch(
        this.apiUrl(`/help/topics/${this.currentTopic.slug}/feedback/`),
        {
          method: 'POST',
          headers: this.getHeaders(),
          credentials: 'same-origin',
          body: JSON.stringify({
            helpful: helpful,
            comment: '',
          }),
        }
      );

      if (!response.ok) throw new Error('Failed to submit feedback');

      // Show comment box if not helpful
      if (!helpful) {
        document.getElementById('helpFeedbackComment').classList.remove('hidden');
      } else {
        this.showFeedbackSuccess();
      }
    } catch (error) {
      console.error('Error submitting feedback:', error);
      AdminModal.alert({ message: 'Failed to submit feedback. Please try again.', type: 'error' });
    }
  },

  /**
   * Submit feedback with comment
   */
  async submitFeedbackComment() {
    if (!this.currentTopic) return;

    const comment = document.getElementById('helpFeedbackText').value.trim();
    if (!comment) return;

    try {
      const response = await fetch(
        this.apiUrl(`/help/topics/${this.currentTopic.slug}/feedback/`),
        {
          method: 'POST',
          headers: this.getHeaders(),
          credentials: 'same-origin',
          body: JSON.stringify({
            helpful: false,
            comment: comment,
          }),
        }
      );

      if (!response.ok) throw new Error('Failed to submit feedback');

      this.showFeedbackSuccess();
      document.getElementById('helpFeedbackText').value = '';
      document.getElementById('helpFeedbackComment').classList.add('hidden');
    } catch (error) {
      console.error('Error submitting feedback:', error);
      AdminModal.alert({ message: 'Failed to submit feedback. Please try again.', type: 'error' });
    }
  },

  /**
   * Render categories grid
   */
  renderCategories() {
    const container = document.getElementById('helpCategories');
    if (!container) return;

    if (this.categories.length === 0) {
      container.innerHTML =
        '<p style="text-align:center;color:var(--text-muted);">No categories available</p>';
      return;
    }

    container.innerHTML = this.categories
      .map(
        cat => `
            <a href="#" class="help-category-card" onclick="HelpSystem.loadCategoryTopics('${cat.slug}'); return false;">
                <i class="${cat.icon} help-category-icon"></i>
                <span class="help-category-name">${this.escapeHtml(cat.name)}</span>
            </a>
        `
      )
      .join('');
  },

  /**
   * Render contextual topics
   */
  renderContextualTopics(topics) {
    const container = document.getElementById('helpContextTopics');
    if (!container) return;

    if (topics.length === 0) {
      const section = document.getElementById('helpContextSection');
      if (section) section.style.display = 'none';
      return;
    }

    this.renderTopicsList('helpContextTopics', topics);
  },

  /**
   * Render topics list
   */
  renderTopicsList(containerId, topics) {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.innerHTML = topics
      .map(topic => {
        const helpfulPercentage = topic.helpfulness_percentage
          ? ` | ${Math.round(topic.helpfulness_percentage)}% helpful`
          : '';

        return `
                <a href="#" class="help-topic-item" onclick="HelpSystem.loadTopic('${topic.slug}'); return false;">
                    <i class="fas fa-file-alt help-topic-icon"></i>
                    <div class="help-topic-content">
                        <h4 class="help-topic-title">${this.escapeHtml(topic.title_i18n_key)}</h4>
                        <div class="help-topic-meta">
                            <span class="help-topic-views">
                                <i class="fas fa-eye"></i>
                                ${topic.view_count}
                            </span>
                            <span>${topic.category_name}</span>
                            ${helpfulPercentage ? `<span>${helpfulPercentage}</span>` : ''}
                        </div>
                    </div>
                </a>
            `;
      })
      .join('');
  },

  /**
   * Render topics list as HTML string (for inline use in topic detail)
   */
  renderTopicsListHTML(topics) {
    return topics
      .map(
        topic => `
            <a href="#" class="help-topic-item" onclick="HelpSystem.loadTopic('${topic.slug}'); return false;">
                <i class="fas fa-file-alt help-topic-icon"></i>
                <div class="help-topic-content">
                    <h4 class="help-topic-title">${this.escapeHtml(topic.title_i18n_key)}</h4>
                    <div class="help-topic-meta">
                        <span class="help-topic-views">
                            <i class="fas fa-eye"></i>
                            ${topic.view_count}
                        </span>
                        <span>${topic.category_name}</span>
                    </div>
                </div>
            </a>
        `
      )
      .join('');
  },

  /**
   * Render topic detail
   */
  renderTopicDetail(topic) {
    // Hide other sections
    document.getElementById('helpContextSection').style.display = 'none';
    document.getElementById('helpCategoriesSection').style.display = 'none';
    document.getElementById('helpSearchSection').classList.add('hidden');

    // Show detail view
    const detailView = document.getElementById('helpTopicDetail');
    detailView.classList.remove('hidden');

    // Render content (convert markdown to HTML)
    const contentContainer = document.getElementById('helpTopicContent');
    contentContainer.innerHTML = `
            <h1>${this.escapeHtml(topic.title_i18n_key)}</h1>
            ${this.renderMarkdown(topic.content_markdown)}
        `;

    // Render related topics
    if (topic.related_topics && topic.related_topics.length > 0) {
      const relatedContainer = document.getElementById('helpRelatedTopics');
      relatedContainer.innerHTML = `
                <h3 class="help-related-title">Related Topics</h3>
                ${this.renderTopicsListHTML(topic.related_topics)}
            `;
    }
  },

  /**
   * Render category topics
   */
  renderCategoryTopics(categorySlug, topics) {
    const category = this.categories.find(c => c.slug === categorySlug);
    if (!category) return;

    // Hide categories, show topics
    const categoriesContainer = document.getElementById('helpCategories');
    const categoryName = category.name;

    categoriesContainer.innerHTML = `
            <button class="help-back-btn" onclick="HelpSystem.showCategories()">
                <i class="fas fa-arrow-left"></i>
                Back to Categories
            </button>
            <h3 style="margin-bottom: 1rem;">${this.escapeHtml(categoryName)}</h3>
            <div class="help-topics-list">
                ${topics
                  .map(
                    topic => `
                    <a href="#" class="help-topic-item" onclick="HelpSystem.loadTopic('${topic.slug}'); return false;">
                        <i class="fas fa-file-alt help-topic-icon"></i>
                        <div class="help-topic-content">
                            <h4 class="help-topic-title">${this.escapeHtml(topic.title_i18n_key)}</h4>
                            <div class="help-topic-meta">
                                <span class="help-topic-views">
                                    <i class="fas fa-eye"></i>
                                    ${topic.view_count}
                                </span>
                            </div>
                        </div>
                    </a>
                `
                  )
                  .join('')}
            </div>
        `;
  },

  /**
   * Show categories view
   */
  showCategories() {
    document.getElementById('helpContextSection').style.display = 'block';
    document.getElementById('helpCategoriesSection').style.display = 'block';
    document.getElementById('helpTopicDetail').classList.add('hidden');
    document.getElementById('helpSearchSection').classList.add('hidden');

    // Reset categories
    this.renderCategories();
  },

  /**
   * Show/hide search results
   */
  showSearchResults() {
    document.getElementById('helpSearchSection').classList.remove('hidden');
    document.getElementById('helpContextSection').style.display = 'none';
    document.getElementById('helpCategoriesSection').style.display = 'none';
  },

  hideSearchResults() {
    document.getElementById('helpSearchSection').classList.add('hidden');
    document.getElementById('helpContextSection').style.display = 'block';
    document.getElementById('helpCategoriesSection').style.display = 'block';
  },

  /**
   * Show loading state
   */
  showLoading(containerId) {
    const container = document.getElementById(containerId);
    if (container) {
      container.innerHTML =
        '<div class="help-loading"><i class="fas fa-spinner fa-spin"></i> Loading...</div>';
    }
  },

  /**
   * Show error message
   */
  showError(containerId, message) {
    const container = document.getElementById(containerId);
    if (container) {
      container.innerHTML = `<p style="text-align:center;color:var(--text-muted);padding:2rem 1rem;">${message}</p>`;
    }
  },

  /**
   * Show no results message
   */
  showNoResults(containerId) {
    const container = document.getElementById(containerId);
    if (container) {
      container.innerHTML =
        '<p style="text-align:center;color:var(--text-muted);padding:2rem 1rem;">No results found. Try different keywords.</p>';
    }
  },

  /**
   * Show feedback success
   */
  showFeedbackSuccess() {
    const feedbackSection = document.querySelector('.help-feedback');
    if (feedbackSection) {
      feedbackSection.innerHTML =
        '<p style="color:#28a745;text-align:center;padding:1rem;">Thank you for your feedback!</p>';
    }
  },

  /**
   * Simple markdown to HTML converter
   */
  renderMarkdown(markdown) {
    if (!markdown) return '';

    // Tables — process before inline formatting to avoid conflicts
    // Split into lines, find consecutive pipe-delimited blocks, convert to HTML tables
    const lines = markdown.split('\n');
    const processed = [];
    let i = 0;

    while (i < lines.length) {
      const line = lines[i].trim();

      // Detect start of a table block (line starts and ends with |)
      if (line.startsWith('|') && line.endsWith('|')) {
        const tableLines = [];
        while (
          i < lines.length &&
          lines[i].trim().startsWith('|') &&
          lines[i].trim().endsWith('|')
        ) {
          tableLines.push(lines[i].trim());
          i++;
        }

        // Need at least header + separator + 1 data row
        if (tableLines.length >= 3) {
          const sepIdx = tableLines.findIndex(r => /^\|[\s\-:|]+\|$/.test(r));
          if (sepIdx !== -1) {
            const parseRow = row =>
              row
                .split('|')
                .slice(1, -1)
                .map(c => c.trim());
            let tableHtml = '<table class="help-table"><thead>';
            for (let h = 0; h < sepIdx; h++) {
              const cells = parseRow(tableLines[h]);
              tableHtml += '<tr>' + cells.map(c => `<th>${c}</th>`).join('') + '</tr>';
            }
            tableHtml += '</thead><tbody>';
            for (let b = sepIdx + 1; b < tableLines.length; b++) {
              const cells = parseRow(tableLines[b]);
              tableHtml += '<tr>' + cells.map(c => `<td>${c}</td>`).join('') + '</tr>';
            }
            tableHtml += '</tbody></table>';
            processed.push(tableHtml);
            continue;
          }
        }
        // Not a valid table — push lines back as-is
        tableLines.forEach(tl => processed.push(tl));
        continue;
      }

      processed.push(lines[i]);
      i++;
    }

    let html = processed.join('\n');

    // Headers
    html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
    html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
    html = html.replace(/^# (.*$)/gim, '<h1>$1</h1>');

    // Bold
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Italic
    html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');

    // Code blocks
    html = html.replace(/```(.*?)```/gs, '<pre><code>$1</code></pre>');

    // Inline code
    html = html.replace(/`(.*?)`/g, '<code>$1</code>');

    // Images (before links — ![alt](url) contains [alt](url) which link regex would match)
    html = html.replace(
      /!\[([^\]]*)\]\(([^)]+)\)/g,
      '<img src="$2" alt="$1" class="help-img" loading="lazy">'
    );

    // Links
    html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>');

    // Lists (unordered)
    html = html.replace(/^\* (.*$)/gim, '<li>$1</li>');
    html = html.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');

    // Paragraphs
    html = html
      .split('\n\n')
      .map(para => {
        if (
          para.startsWith('<h') ||
          para.startsWith('<ul') ||
          para.startsWith('<pre') ||
          para.startsWith('<table')
        ) {
          return para;
        }
        return `<p>${para}</p>`;
      })
      .join('\n');

    return html;
  },

  /**
   * Get request headers
   */
  getHeaders() {
    const csrfToken = this.getCSRFToken();
    return {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrfToken,
    };
  },

  /**
   * Get CSRF token
   */
  getCSRFToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    if (meta && meta.content) return meta.content;
    const input = document.querySelector('[name=csrfmiddlewaretoken]');
    if (input) return input.value;
    return '';
  },

  /**
   * Escape HTML
   */
  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  },
};

// Initialize help system when drawer is opened
document.addEventListener('DOMContentLoaded', () => {
  // Auto-initialize if drawer is already open
  const drawer = document.getElementById('helpDrawer');
  if (drawer && drawer.classList.contains('open')) {
    HelpSystem.init();
  }
});
