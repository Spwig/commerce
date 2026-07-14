/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Media Library JavaScript - Interactive gallery components
 */

class MediaLibrary {
  constructor(options = {}) {
    // Singleton pattern: prevent multiple instances
    // Return early if instance already exists
    if (window.mediaLibraryInstance) {
      console.log('[MediaLibrary] Instance already exists, reusing it');
      // Merge new options if provided
      if (Object.keys(options).length > 0) {
        Object.assign(window.mediaLibraryInstance.options, options);
      }
      return window.mediaLibraryInstance;
    }

    console.log('[MediaLibrary] Creating new instance');
    window.mediaLibraryInstance = this;

    // API URLs (no language prefix - these are outside i18n_patterns)
    this.options = {
      apiUrl: '/api/media/assets/',
      uploadUrl: '/api/media/assets/',
      selectionMode: 'single', // 'single' or 'multiple'
      fileTypeFilter: 'all', // 'image', 'video', or 'all'
      allowedTypes: [
        // Image formats
        'image/jpeg',
        'image/png',
        'image/gif',
        'image/webp',
        'image/svg+xml',
        // Video formats
        'video/mp4',
        'video/webm',
        'video/quicktime',
        'video/x-matroska',
        'video/x-msvideo',
        // 3D model formats
        'model/gltf-binary',
        'model/gltf+json',
        // HDR
        'image/hdr',
      ],
      maxFileSize: 100 * 1024 * 1024, // 100MB for video support
      useUploadQueue: true, // Use the new upload queue manager
      onSelect: null, // Callback function when media is selected
      autoClose: false, // Auto-close modal after selection
      customModal: null, // Existing modal element to render into
      ...options,
    };

    // Apply file type filter to allowed types
    if (this.options.fileTypeFilter === 'image') {
      this.options.allowedTypes = this.options.allowedTypes.filter(type =>
        type.startsWith('image/')
      );
    } else if (this.options.fileTypeFilter === 'video') {
      this.options.allowedTypes = this.options.allowedTypes.filter(type =>
        type.startsWith('video/')
      );
    }

    this.selectedItems = new Set();
    this.mediaDataCache = new Map(); // Store full media data by ID for selection
    this.currentFolder = null;
    this.currentTags = [];
    this.searchQuery = '';
    this.viewMode = localStorage.getItem('mediaLibraryView') || 'grid';
    this.isRecycleBin = false; // Track if we're viewing recycle bin

    // Pagination for lazy loading
    this.nextPageUrl = null;
    this.isLoadingMore = false;
    this.allMediaLoaded = false;

    // Initialize upload queue if enabled
    if (this.options.useUploadQueue && window.UploadQueueManager) {
      this.uploadQueue = new window.UploadQueueManager({
        apiBase: '/api/media',
        maxConcurrent: 2,
      });

      // Set up auto-refresh when uploads complete
      this.uploadQueue.onComplete(() => {
        console.log('All uploads completed, refreshing gallery...');
        this.loadMedia();
      });

      // Set up per-item completion for 3D thumbnail auto-capture
      this.uploadQueue.onUploadComplete = asset => {
        this.handleUploadComplete(asset);
      };
    }

    this.init();
  }

  init() {
    this.setupEventListeners();
    this.applyViewMode();
    // Setup search input if gallery exists on page (not modal)
    // For modals, setupSearchInput() is called in openModal() after modal is created
    this.setupSearchInput();
    // Only load media if there's no existing content
    // Use specific selector to find grid in modal, not old custom modal grid
    const grid =
      document.querySelector('.ml-modal .media-grid') ||
      document.querySelector('.media-gallery .media-grid');
    if (grid && grid.children.length === 0) {
      this.loadMedia();
    }
    this.initializeUploadZone();
  }

  setupEventListeners() {
    // Note: Search input binding is handled in openModal() and setupSearchInput()
    // because the search input only exists after the modal is created

    // Setup scroll listener for infinite loading on standalone gallery page
    // (Modal has its own scroll listener set up in openModal())
    const galleryGrid = document.querySelector('.media-gallery .media-grid');
    if (galleryGrid) {
      galleryGrid.addEventListener(
        'scroll',
        this.debounce(() => {
          const scrollHeight = galleryGrid.scrollHeight;
          const scrollTop = galleryGrid.scrollTop;
          const clientHeight = galleryGrid.clientHeight;

          if (scrollTop + clientHeight >= scrollHeight * 0.8) {
            this.loadMoreMedia();
          }
        }, 200)
      );
    }

    // Folder navigation
    document.addEventListener('click', e => {
      if (e.target.matches('.folder-tree a')) {
        e.preventDefault();
        this.selectFolder(e.target.dataset.folderId);
      }
    });

    // Tag filtering
    document.addEventListener('click', e => {
      if (e.target.matches('.tag-item')) {
        e.preventDefault();
        this.toggleTag(e.target.dataset.tagId);
      }
    });

    // Media item selection with click delay to handle single vs double click
    let clickTimer = null;
    const CLICK_DELAY = 250; // milliseconds to wait before processing single click

    document.addEventListener('click', e => {
      const mediaItem = e.target.closest('.media-item');
      if (mediaItem) {
        // Clear any existing timer
        if (clickTimer) {
          clearTimeout(clickTimer);
          clickTimer = null;
        }

        // Set a timer to handle single click
        clickTimer = setTimeout(() => {
          this.handleMediaSelection(mediaItem, e);
          clickTimer = null;
        }, CLICK_DELAY);
      }
    });

    // Double-click for preview
    document.addEventListener('dblclick', e => {
      const mediaItem = e.target.closest('.media-item');
      if (mediaItem) {
        e.preventDefault();

        // Cancel the single click timer since this is a double-click
        if (clickTimer) {
          clearTimeout(clickTimer);
          clickTimer = null;
        }

        this.showPreview(mediaItem);
      }
    });

    // Long-press for mobile preview (touch devices)
    let touchTimer = null;
    let touchStarted = false;
    const LONG_PRESS_DURATION = 500; // milliseconds

    document.addEventListener('touchstart', e => {
      const mediaItem = e.target.closest('.media-item');
      if (mediaItem) {
        touchStarted = true;

        // Add visual feedback class
        mediaItem.classList.add('touch-press');

        // Set timer for long-press
        touchTimer = setTimeout(() => {
          if (touchStarted) {
            // Trigger preview
            this.showPreview(mediaItem);
            mediaItem.classList.remove('touch-press');
            touchStarted = false;

            // Prevent click event from firing
            e.preventDefault();
          }
        }, LONG_PRESS_DURATION);
      }
    });

    document.addEventListener('touchend', e => {
      const mediaItem = e.target.closest('.media-item');
      if (mediaItem) {
        mediaItem.classList.remove('touch-press');
      }

      // Clear the long-press timer
      if (touchTimer) {
        clearTimeout(touchTimer);
        touchTimer = null;
      }
      touchStarted = false;
    });

    document.addEventListener('touchmove', e => {
      // Cancel long-press if user scrolls
      if (touchTimer) {
        clearTimeout(touchTimer);
        touchTimer = null;
      }
      touchStarted = false;

      const mediaItem = e.target.closest('.media-item');
      if (mediaItem) {
        mediaItem.classList.remove('touch-press');
      }
    });

    // Filter changes
    document.addEventListener('change', e => {
      if (e.target.matches('.filter-select')) {
        this.loadMedia();
      }
    });

    // Modal close
    document.addEventListener('click', e => {
      if (e.target.matches('.modal-close')) {
        this.closeModal();
      } else if (e.target.matches('.media-modal.ml-modal')) {
        // Only close if clicking on the backdrop (not on modal content)
        if (e.target === e.currentTarget) {
          this.closeModal();
        }
      }
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape') {
        this.closeModal();
      }
    });

    // View mode switcher
    document.addEventListener('click', e => {
      const btn = e.target.closest('[data-view]');
      if (btn && btn.classList.contains('util-btn')) {
        e.preventDefault();
        this.switchView(btn.dataset.view);
      }
    });

    // Action button handlers
    document.addEventListener('click', e => {
      const actionBtn = e.target.closest('[data-action]');
      if (actionBtn) {
        e.preventDefault();
        const action = actionBtn.dataset.action;
        console.log('[MediaLibrary] Action button clicked:', action);

        switch (action) {
          case 'edit-details':
            this.handleEditDetails();
            break;
          case 'delete':
            this.handleDelete();
            break;
          case 'restore':
            this.handleRestore();
            break;
          case 'permanent-delete':
            this.handlePermanentDelete();
            break;
          case 'select':
            this.handleSelect();
            break;
        }
      }
    });
  }

  switchView(viewMode) {
    this.viewMode = viewMode;
    localStorage.setItem('mediaLibraryView', viewMode);
    this.applyViewMode();

    // Update button states
    document.querySelectorAll('[data-view]').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.view === viewMode);
    });
  }

  applyViewMode() {
    // Use specific selector to find grid in modal, not old custom modal grid
    const grid =
      document.querySelector('.ml-modal .media-grid') ||
      document.querySelector('.media-gallery .media-grid');
    if (!grid) return;

    // Remove all view classes
    grid.classList.remove('view-grid', 'view-small', 'view-list', 'view-large');

    // Apply new view class
    grid.classList.add(`view-${this.viewMode}`);

    // Update view button states
    document.querySelectorAll('[data-view]').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.view === this.viewMode);
    });
  }

  async loadMedia(resetGrid = true) {
    // Determine API endpoint based on recycle bin state
    let apiUrl = this.options.apiUrl;
    if (this.isRecycleBin) {
      apiUrl = '/api/media/assets/deleted/';
    }

    const params = new URLSearchParams();

    // DRF SearchFilter uses 'search' parameter
    if (this.searchQuery) {
      params.append('search', this.searchQuery);
    }

    if (this.currentFolder && !this.isRecycleBin) {
      params.append('folder', this.currentFolder);
    }

    this.currentTags.forEach(tagId => {
      params.append('tags', tagId);
    });

    // Add file type filter if specified
    if (this.options.fileTypeFilter === 'image') {
      params.append('mime_type__startswith', 'image/');
    } else if (this.options.fileTypeFilter === 'video') {
      params.append('mime_type__startswith', 'video/');
    }

    // Add filter parameters
    const filterSelects = document.querySelectorAll('.filter-select');
    filterSelects.forEach(select => {
      if (select.value) {
        params.append(select.name, select.value);
      }
    });

    // Reset pagination state when loading fresh results
    if (resetGrid) {
      this.nextPageUrl = null;
      this.allMediaLoaded = false;
    }

    try {
      this.showLoading();
      console.log('[MediaLibrary] Fetching from:', `${apiUrl}?${params}`);
      const response = await fetch(`${apiUrl}?${params}`);
      console.log('[MediaLibrary] Response status:', response.status);

      const data = await response.json();
      console.log('[MediaLibrary] Response data:', data);

      // Store next page URL for lazy loading
      this.nextPageUrl = data.next || null;
      this.allMediaLoaded = !data.next;

      // Apply client-side filtering for size if needed
      let results = data.results || data;
      console.log('[MediaLibrary] Results count:', results.length);

      const sizeFilter = document.querySelector('.filter-select[name="size"]');
      if (sizeFilter && sizeFilter.value) {
        results = this.filterBySize(results, sizeFilter.value);
      }

      this.renderMediaGrid(results, resetGrid);
    } catch (error) {
      console.error('Error loading media:', error);
      this.showError('Failed to load media items');
    } finally {
      this.hideLoading();
    }
  }

  async loadMoreMedia() {
    if (this.isLoadingMore || this.allMediaLoaded || !this.nextPageUrl) {
      return;
    }

    this.isLoadingMore = true;

    try {
      console.log('[MediaLibrary] Loading more from:', this.nextPageUrl);
      const response = await fetch(this.nextPageUrl);
      const data = await response.json();

      // Update pagination state
      this.nextPageUrl = data.next || null;
      this.allMediaLoaded = !data.next;

      // Apply client-side filtering for size if needed
      let results = data.results || data;
      const sizeFilter = document.querySelector('.filter-select[name="size"]');
      if (sizeFilter && sizeFilter.value) {
        results = this.filterBySize(results, sizeFilter.value);
      }

      // Append new items to grid
      this.renderMediaGrid(results, false);
    } catch (error) {
      console.error('Error loading more media:', error);
      this.showError('Failed to load more items');
    } finally {
      this.isLoadingMore = false;
    }
  }

  filterBySize(items, sizeCategory) {
    return items.filter(item => {
      const size = item.file_size || 0;
      switch (sizeCategory) {
        case 'small':
          return size < 100 * 1024; // < 100KB
        case 'medium':
          return size >= 100 * 1024 && size < 1024 * 1024; // 100KB - 1MB
        case 'large':
          return size >= 1024 * 1024; // > 1MB
        default:
          return true;
      }
    });
  }

  renderMediaGrid(items, clearGrid = true) {
    // IMPORTANT: Use specific selector to find grid in modal, not old custom modal grid
    const grid =
      document.querySelector('.ml-modal .media-grid') ||
      document.querySelector('.media-gallery .media-grid');
    console.log('[MediaLibrary] renderMediaGrid - grid element:', grid);
    if (!grid) {
      console.error('[MediaLibrary] No .media-grid found!');
      return;
    }

    // Only clear grid if explicitly requested (for initial load or search)
    if (clearGrid) {
      grid.innerHTML = '';
    }

    if (items.length === 0 && clearGrid) {
      grid.innerHTML = '<div class="no-results">No media items found</div>';
      return;
    }

    console.log('[MediaLibrary] Rendering', items.length, 'items (clearGrid:', clearGrid, ')');
    items.forEach((item, index) => {
      const mediaItem = this.createMediaItem(item);
      grid.appendChild(mediaItem);
      if (index === 0 && clearGrid) {
        console.log(
          '[MediaLibrary] First item dimensions:',
          mediaItem.offsetWidth,
          'x',
          mediaItem.offsetHeight
        );
      }
    });
    console.log('[MediaLibrary] Grid now has', grid.children.length, 'children');
    console.log('[MediaLibrary] Grid dimensions:', grid.offsetWidth, 'x', grid.offsetHeight);
  }

  createMediaItem(item) {
    const div = document.createElement('div');
    div.className = 'media-item';
    div.dataset.itemId = item.id;

    // Store full item data in cache for later retrieval (e.g., when selecting)
    this.mediaDataCache.set(String(item.id), item);

    // Detect file type
    const isVideo = item.mime_type && item.mime_type.startsWith('video/');
    const is3D = item.mime_type && item.mime_type.startsWith('model/');
    div.dataset.type = isVideo ? 'video' : is3D ? '3d' : 'image';

    const isSelected = this.selectedItems.has(item.id);
    if (isSelected) {
      div.classList.add('selected');
    }

    // Use thumbnail/poster for display - prefer medium thumbnails
    // The API returns: thumbnail_url (small), webp_file (optimized), original_file
    // We need to construct medium and large URLs
    let displayUrl = '';
    if (item.thumbnail_url) {
      // If we have a small thumbnail, derive medium from it
      displayUrl = item.thumbnail_url.replace('_small.webp', '_medium.webp');
    } else if (item.webp_file) {
      displayUrl = item.webp_file;
    } else if (item.thumbnail) {
      displayUrl = item.thumbnail;
    } else if (item.poster_url) {
      displayUrl = item.poster_url;
    } else if (item.display_url) {
      displayUrl = item.display_url;
    } else {
      displayUrl = item.url || '';
    }

    // Build dimensions text - only show if available
    let dimensionsHTML = '';
    if (item.width && item.height) {
      let dimensionsText = `${item.width} × ${item.height}`;
      if (isVideo && item.duration) {
        dimensionsText += ` • ${Math.round(item.duration)}s`;
      }
      dimensionsHTML = `<div class="dimensions">${dimensionsText}</div>`;
    } else if (isVideo && item.duration) {
      dimensionsHTML = `<div class="dimensions">${Math.round(item.duration)}s</div>`;
    }

    // For 3D models, prefer poster_url if available
    const posterUrl = item.poster_url || item.poster_image || '';

    div.innerHTML = `
            <div class="image-container">
                ${
                  is3D
                    ? posterUrl
                      ? `<img src="${posterUrl}" alt="${item.alt_text || item.title}" loading="lazy" draggable="false">
                         <div class="model-badge" title="3D Model"><i class="fas fa-cube"></i></div>`
                      : '<div class="no-image"><i class="fas fa-cube fa-3x"></i></div>'
                    : displayUrl
                      ? `<img src="${displayUrl}" alt="${item.alt_text || item.title}" loading="lazy" draggable="false">
                     ${isVideo ? '<div class="video-indicator">🎬</div>' : ''}`
                      : `<div class="no-image">${isVideo ? '🎬' : '📄'}</div>`
                }
                ${dimensionsHTML}
            </div>
            <div class="info">
                <div class="title" title="${item.title}">${item.title}</div>
                <div class="meta">
                    ${item.mime_type || 'Unknown'} • ${this.formatFileSize(item.file_size || 0)}
                </div>
            </div>
        `;

    return div;
  }

  getThumbnailUrl(mediaData, size) {
    // Look for requested size in thumbnails array
    if (mediaData.thumbnails && Array.isArray(mediaData.thumbnails)) {
      const thumbnail = mediaData.thumbnails.find(t => t.size_preset === size);
      if (thumbnail) {
        return thumbnail.webp_url || thumbnail.url;
      }
    }

    // Fallback chain: try other sizes
    const fallbackSizes = ['large', 'medium', 'small'];
    for (const fallbackSize of fallbackSizes) {
      if (fallbackSize === size) continue; // Skip requested size (already tried)
      const fallback = mediaData.thumbnails?.find(t => t.size_preset === fallbackSize);
      if (fallback) {
        return fallback.webp_url || fallback.url;
      }
    }

    // Last resort: use webp_file or original_file
    return mediaData.webp_file || mediaData.original_file || mediaData.thumbnail_url;
  }

  async fetchMediaDetails(mediaId) {
    // Normalize mediaId (could be int or UUID string)
    const cacheKey = String(mediaId);

    // Check if already in cache
    if (this.mediaDataCache.has(cacheKey)) {
      return this.mediaDataCache.get(cacheKey);
    }

    // Fetch from API (API is outside i18n_patterns, no language prefix)
    try {
      const response = await fetch(`/api/media/assets/${mediaId}/`, {
        credentials: 'same-origin', // Include cookies for authentication
      });
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }
      const data = await response.json();

      // Cache the data using string key
      this.mediaDataCache.set(cacheKey, data);

      return data;
    } catch (error) {
      console.error('[MediaLibrary] Failed to fetch media details:', error);
      return null;
    }
  }

  handleMediaSelection(mediaItem, event) {
    const itemId = mediaItem.dataset.itemId;
    const isCtrlClick = event && (event.ctrlKey || event.metaKey);
    const isShiftClick = event && event.shiftKey;

    if (this.options.selectionMode === 'single' && !isCtrlClick && !isShiftClick) {
      // Clear previous selections
      this.selectedItems.clear();
      document.querySelectorAll('.media-item.selected').forEach(item => {
        item.classList.remove('selected');
      });
    } else if (this.options.selectionMode === 'multiple') {
      // Handle shift-click for range selection
      if (isShiftClick && this.lastSelectedItem) {
        this.selectRange(this.lastSelectedItem, itemId);
        return;
      }

      // If not ctrl/cmd click, clear previous selections
      if (!isCtrlClick && !isShiftClick) {
        this.selectedItems.clear();
        document.querySelectorAll('.media-item.selected').forEach(item => {
          item.classList.remove('selected');
        });
      }
    }

    // Toggle selection
    if (this.selectedItems.has(itemId)) {
      this.selectedItems.delete(itemId);
      mediaItem.classList.remove('selected');
    } else {
      this.selectedItems.add(itemId);
      mediaItem.classList.add('selected');
      this.lastSelectedItem = itemId;
    }

    this.updateSelectionUI();
  }

  selectRange(startId, endId) {
    const items = Array.from(document.querySelectorAll('.media-item'));
    const startIndex = items.findIndex(item => item.dataset.itemId === startId);
    const endIndex = items.findIndex(item => item.dataset.itemId === endId);

    if (startIndex === -1 || endIndex === -1) return;

    const minIndex = Math.min(startIndex, endIndex);
    const maxIndex = Math.max(startIndex, endIndex);

    // Clear current selections
    this.selectedItems.clear();
    document.querySelectorAll('.media-item.selected').forEach(item => {
      item.classList.remove('selected');
    });

    // Select range
    for (let i = minIndex; i <= maxIndex; i++) {
      const item = items[i];
      const itemId = item.dataset.itemId;
      this.selectedItems.add(itemId);
      item.classList.add('selected');
    }

    this.updateSelectionUI();
  }

  updateSelectionUI() {
    const selectedCount = this.selectedItems.size;
    const actionButtons = document.querySelector('.media-actions');

    if (actionButtons) {
      // Update select button
      const selectButton = actionButtons.querySelector('[data-action="select"]');
      if (selectButton) {
        selectButton.disabled = selectedCount === 0;
        selectButton.textContent =
          selectedCount > 0
            ? `Select ${selectedCount} item${selectedCount > 1 ? 's' : ''}`
            : 'Select Items';
      }

      // Update edit details button
      const editButton = actionButtons.querySelector('[data-action="edit-details"]');
      if (editButton) {
        // Enable only when exactly one item is selected
        editButton.disabled = selectedCount !== 1;
      }

      // Update delete button (or restore/permanent delete for recycle bin)
      // Look for both delete and permanent-delete since the action changes
      const deleteButton = actionButtons.querySelector(
        '[data-action="delete"], [data-action="permanent-delete"]'
      );
      if (deleteButton) {
        deleteButton.disabled = selectedCount === 0;
        if (this.isRecycleBin) {
          // In recycle bin, change to permanent delete
          deleteButton.textContent =
            selectedCount > 0
              ? `Permanently Delete ${selectedCount} item${selectedCount > 1 ? 's' : ''}`
              : 'Permanently Delete';
          deleteButton.dataset.action = 'permanent-delete';
        } else {
          // Normal delete (soft delete)
          deleteButton.textContent =
            selectedCount > 0
              ? `Delete ${selectedCount} item${selectedCount > 1 ? 's' : ''}`
              : 'Delete Selected';
          deleteButton.dataset.action = 'delete';
        }
      }

      // Handle restore button for recycle bin
      if (this.isRecycleBin) {
        let restoreButton = actionButtons.querySelector('[data-action="restore"]');
        if (!restoreButton) {
          // Create restore button if it doesn't exist
          restoreButton = document.createElement('button');
          restoreButton.className = 'action-btn primary';
          restoreButton.dataset.action = 'restore';
          actionButtons.insertBefore(restoreButton, deleteButton);
        }
        restoreButton.disabled = selectedCount === 0;
        restoreButton.textContent =
          selectedCount > 0
            ? `Restore ${selectedCount} item${selectedCount > 1 ? 's' : ''}`
            : 'Restore Selected';
        restoreButton.style.display = '';
      } else {
        // Hide restore button when not in recycle bin
        const restoreButton = actionButtons.querySelector('[data-action="restore"]');
        if (restoreButton) {
          restoreButton.style.display = 'none';
        }
      }
    }
  }

  updateToolbar() {
    // Update breadcrumb
    const breadcrumb = document.querySelector('.breadcrumb-item:last-child');
    if (breadcrumb) {
      breadcrumb.textContent = this.isRecycleBin ? 'Recycle Bin' : 'All Files';
    }

    // Disable upload zone in recycle bin
    const uploadZone = document.querySelector('.upload-zone');
    if (uploadZone) {
      uploadZone.style.display = this.isRecycleBin ? 'none' : '';
    }

    // Update any other UI elements based on recycle bin state
    this.updateSelectionUI();
  }

  selectFolder(folderId) {
    // Check if it's recycle bin
    this.isRecycleBin = folderId === 'recycle-bin';
    this.currentFolder = this.isRecycleBin ? null : folderId;

    // Clear selections when switching folders
    this.clearSelection();

    // Update folder UI
    document.querySelectorAll('.folder-tree a').forEach(link => {
      link.classList.remove('active');
    });

    if (folderId) {
      const folderLink = document.querySelector(`[data-folder-id="${folderId}"]`);
      if (folderLink) {
        folderLink.classList.add('active');
      }
    }

    // Update toolbar buttons based on recycle bin state
    this.updateToolbar();

    this.loadMedia();
  }

  toggleTag(tagId) {
    const index = this.currentTags.indexOf(tagId);
    const tagElement = document.querySelector(`[data-tag-id="${tagId}"]`);

    if (index > -1) {
      this.currentTags.splice(index, 1);
      tagElement?.classList.remove('active');
    } else {
      this.currentTags.push(tagId);
      tagElement?.classList.add('active');
    }

    this.loadMedia();
  }

  initializeUploadZone(scope = document) {
    const uploadZone = scope.querySelector('.upload-zone');
    if (!uploadZone) {
      console.log('[MediaLibrary] No upload zone found');
      return;
    }

    console.log('[MediaLibrary] Found upload zone, checking if already bound');
    console.log('[MediaLibrary] Current mlBound value:', uploadZone.dataset.mlBound);

    // Guard against duplicate binding
    if (uploadZone.dataset.mlBound === '1') {
      console.log('[MediaLibrary] Upload zone already bound, skipping');
      return;
    }
    uploadZone.dataset.mlBound = '1';
    console.log('[MediaLibrary] Binding upload zone');

    // Reuse a single hidden input per drop zone
    let fileInput = uploadZone.querySelector('input[type=file].ml-input');
    if (!fileInput) {
      fileInput = document.createElement('input');
      fileInput.type = 'file';
      fileInput.multiple = true;
      fileInput.accept = this.options.allowedTypes.join(',') + ',.glb,.gltf,.hdr';
      fileInput.className = 'ml-input';
      fileInput.style.display = 'none';
      uploadZone.appendChild(fileInput);
      console.log('[MediaLibrary] Created new file input');
    } else {
      console.log('[MediaLibrary] Reusing existing file input');
    }

    // Store file input reference globally for button access
    this.fileInput = fileInput;

    // Click to open file dialog
    uploadZone.addEventListener('click', e => {
      // Don't trigger if clicking on a child interactive element or media item
      if (e.target.closest('button, a, input, .media-item')) return;
      this.fileInput.value = '';
      this.fileInput.click();
    });

    // File selection - only bind once
    fileInput.addEventListener('change', e => {
      console.log('[MediaLibrary] File input change event fired');
      console.log('[MediaLibrary] Files selected:', e.target.files.length);

      if (e.target.files.length > 0) {
        console.log(
          '[MediaLibrary] Files:',
          Array.from(e.target.files).map(f => f.name)
        );
        console.log('[MediaLibrary] Processing files...');
        this.handleFileUpload(Array.from(e.target.files));
      } else {
        console.log('[MediaLibrary] No files selected, skipping upload');
      }
    });

    // Drag and drop with overlay
    const overlay = uploadZone.querySelector('.upload-overlay');

    uploadZone.addEventListener('dragover', e => {
      // Only respond to file drags (from desktop/file system), not element drags from within page
      if (e.dataTransfer.types.includes('Files')) {
        e.preventDefault();
        uploadZone.classList.add('dragover');
        if (overlay) {
          overlay.style.display = 'flex';
        }
      }
    });

    uploadZone.addEventListener('dragleave', e => {
      e.preventDefault();
      // Only hide if leaving the uploadZone itself, not child elements
      if (e.target === uploadZone) {
        uploadZone.classList.remove('dragover');
        if (overlay) {
          overlay.style.display = 'none';
        }
      }
    });

    uploadZone.addEventListener('drop', e => {
      e.preventDefault();
      uploadZone.classList.remove('dragover');
      if (overlay) {
        overlay.style.display = 'none';
      }

      // Only process if actual files were dropped (not just dragging page elements)
      const files = Array.from(e.dataTransfer.files);
      if (files.length > 0) {
        this.handleFileUpload(files);
      }
    });

    // Hide overlay when drag operation ends (including when leaving browser window)
    const hideOverlay = () => {
      uploadZone.classList.remove('dragover');
      if (overlay) {
        overlay.style.display = 'none';
      }
    };

    // Dragend fires when drag operation completes (including outside browser)
    uploadZone.addEventListener('dragend', hideOverlay);

    // Also handle document-level dragleave to catch when drag leaves window
    const documentDragLeaveHandler = e => {
      // Check if drag is leaving the document entirely (e.relatedTarget will be null)
      if (!e.relatedTarget && !e.screenX && !e.screenY) {
        hideOverlay();
      }
    };
    document.addEventListener('dragleave', documentDragLeaveHandler);

    // Store reference for cleanup if needed
    this._documentDragLeaveHandler = documentDragLeaveHandler;
  }

  /**
   * Infer MIME type from file extension when the browser doesn't know it.
   * Browsers often return "" for .glb, .gltf, .hdr files.
   */
  inferMimeType(file) {
    if (file.type) return file.type;
    const ext = file.name.split('.').pop().toLowerCase();
    const extMap = {
      glb: 'model/gltf-binary',
      gltf: 'model/gltf+json',
      hdr: 'image/hdr',
    };
    return extMap[ext] || '';
  }

  /**
   * Called when a single upload completes. Auto-captures thumbnails for 3D models.
   */
  handleUploadComplete(asset) {
    if (!asset) return;
    const mimeType = asset.mime_type || '';
    if (!mimeType.startsWith('model/')) return;

    const glbUrl = asset.original_file;
    const assetId = asset.id;
    if (!glbUrl || !assetId) return;

    console.log(`[MediaLibrary] 3D model uploaded (${assetId}), auto-capturing thumbnail...`);
    this.capture3DThumbnail(assetId, glbUrl);
  }

  /**
   * Load model-viewer web component dynamically (once).
   */
  _loadModelViewer() {
    if (this._modelViewerLoaded) return this._modelViewerLoaded;

    if (customElements.get('model-viewer')) {
      this._modelViewerLoaded = Promise.resolve();
      return this._modelViewerLoaded;
    }

    this._modelViewerLoaded = new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.type = 'module';
      script.src = '/static/configurator_3d/js/vendor/model-viewer.min.js';
      script.onload = () => resolve();
      script.onerror = () => reject(new Error('Failed to load model-viewer'));
      document.head.appendChild(script);
    });
    return this._modelViewerLoaded;
  }

  /**
   * Render a 3D model off-screen and capture a poster thumbnail.
   */
  async capture3DThumbnail(assetId, glbUrl) {
    try {
      await this._loadModelViewer();
      // Wait for custom element to be defined
      await customElements.whenDefined('model-viewer');

      const viewer = document.createElement('model-viewer');
      viewer.setAttribute('src', glbUrl);
      viewer.setAttribute('auto-rotate', '');
      viewer.setAttribute('camera-controls', '');
      viewer.setAttribute('reveal', 'auto');
      viewer.setAttribute('loading', 'eager');
      // Must stay within viewport for IntersectionObserver — use opacity:0 instead of off-screen
      viewer.style.cssText =
        'position:fixed;bottom:0;right:0;width:400px;height:400px;opacity:0;pointer-events:none;z-index:-1;background-color:#f0f0f0;';
      document.body.appendChild(viewer);

      // Wait for model to load
      await new Promise((resolve, reject) => {
        const timeout = setTimeout(() => {
          reject(new Error('model-viewer load timeout'));
        }, 15000);
        viewer.addEventListener(
          'load',
          () => {
            clearTimeout(timeout);
            resolve();
          },
          { once: true }
        );
        viewer.addEventListener(
          'error',
          () => {
            clearTimeout(timeout);
            reject(new Error('model-viewer load error'));
          },
          { once: true }
        );
      });

      // Let the renderer settle
      await new Promise(r => setTimeout(r, 800));

      // Capture screenshot
      const blob = await viewer.toBlob({ mimeType: 'image/png', idealAspect: true });

      // Clean up viewer
      viewer.remove();

      // Upload poster to set_poster endpoint
      const formData = new FormData();
      formData.append('poster', blob, `${assetId}_poster.png`);

      const csrfToken =
        document.querySelector('meta[name="csrf-token"]')?.content ||
        document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
        '';

      const response = await fetch(`/api/media/assets/${assetId}/set_poster/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrfToken },
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        console.log(`[MediaLibrary] 3D thumbnail saved: ${data.poster_url}`);
        // Refresh gallery to show the new thumbnail
        this.loadMedia();
      } else {
        console.error('[MediaLibrary] Failed to save 3D thumbnail:', response.status);
      }
    } catch (err) {
      console.error('[MediaLibrary] Error capturing 3D thumbnail:', err);
      // Silently fail — cube icon fallback will still display
    }
  }

  async handleFileUpload(files) {
    const validFiles = files.filter(file => {
      const mimeType = this.inferMimeType(file);
      if (!this.options.allowedTypes.includes(mimeType)) {
        this.showError(`Invalid file type: ${file.name}`);
        return false;
      }

      if (file.size > this.options.maxFileSize) {
        this.showError(
          `File too large: ${file.name} (max ${Math.round(this.options.maxFileSize / 1024 / 1024)}MB)`
        );
        return false;
      }

      return true;
    });

    if (validFiles.length === 0) return;

    // Use upload queue if available
    if (this.uploadQueue) {
      this.uploadQueue.addToQueue(validFiles);
      // Auto-refresh is handled by the onComplete callback
    } else {
      // Fallback to sequential upload
      for (const file of validFiles) {
        await this.uploadFile(file);
      }
      this.loadMedia();
    }
  }

  async uploadFile(file) {
    const formData = new FormData();
    formData.append('original_file', file);
    formData.append('title', file.name.split('.')[0]);

    if (this.currentFolder) {
      formData.append('folder', this.currentFolder);
    }

    try {
      const progressBar = this.createProgressBar(file.name);

      const response = await fetch(this.options.uploadUrl, {
        method: 'POST',
        body: formData,
        headers: {
          'X-CSRFToken': this.getCSRFToken(),
        },
      });

      const result = await response.json();

      if (response.ok) {
        this.showSuccess(`Uploaded: ${file.name}`);
      } else {
        this.showError(`Upload failed: ${file.name} - ${result.error}`);
      }

      progressBar.remove();
    } catch (error) {
      console.error('Upload error:', error);
      this.showError(`Upload failed: ${file.name}`);
    }
  }

  createProgressBar(filename) {
    const progressContainer = document.createElement('div');
    progressContainer.className = 'upload-progress';
    progressContainer.innerHTML = `
            <div class="progress-label">${filename}</div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: 100%"></div>
            </div>
        `;

    const uploadZone = document.querySelector('.upload-zone');
    uploadZone.appendChild(progressContainer);

    return progressContainer;
  }

  showModal(content) {
    const modal = document.createElement('div');
    modal.className = 'media-modal ml-modal'; // Add unique class to avoid CSS conflicts
    modal.innerHTML = `
            <div class="modal-content" style="width: 1200px !important;">
                <div class="modal-header">
                    <h3 class="modal-title">Media Library</h3>
                    <button class="modal-close">&times;</button>
                </div>
                <div class="modal-body" style="overflow: hidden;">
                    ${content}
                </div>
            </div>
        `;

    document.body.appendChild(modal);
    return modal;
  }

  openModal() {
    // Public API to open media library modal with simplified interface
    const modalContent = `
            <div class="media-gallery" style="grid-template-columns: 1fr;">
                <div class="media-content" style="display: flex; flex-direction: column; max-height: 80vh;">
                    <div class="media-toolbar" style="z-index: 10; background: var(--body-bg, #fff); padding: 15px 0; display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 1px solid var(--border-color, #dee2e6); flex-shrink: 0;">
                        <div class="media-search">
                            <input type="text" class="search-input" placeholder="Search media...">
                        </div>
                        <div class="view-controls" style="display: flex; gap: 5px;">
                            <button class="util-btn" data-view="small" title="Small thumbnails">
                                <i class="fas fa-th"></i>
                            </button>
                            <button class="util-btn active" data-view="grid" title="Medium thumbnails">
                                <i class="fas fa-th-large"></i>
                            </button>
                            <button class="util-btn" data-view="large" title="Large thumbnails">
                                <i class="fas fa-square"></i>
                            </button>
                        </div>
                    </div>
                    <div class="upload-hint" style="margin: 0 0 15px 0; padding: 8px 12px; background: var(--darkened-bg, #f8f9fa); border-radius: 4px; display: flex; align-items: center; justify-content: center; gap: 15px; font-size: 13px; color: var(--body-quiet-color, #666); flex-shrink: 0;">
                        <span>
                            <i class="fas fa-cloud-upload-alt" style="margin-right: 8px; color: var(--primary, #007bff);"></i>
                            Drop files anywhere below to upload • Supported: ${this.options.fileTypeFilter === 'image' ? 'JPG, PNG, GIF, WebP, SVG' : this.options.fileTypeFilter === 'video' ? 'MP4, WebM, MOV' : 'Images, Videos & 3D Models'}
                        </span>
                        <button class="upload-files-btn" type="button" style="background: var(--primary, #007bff); color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; font-size: 12px; white-space: nowrap; display: flex; align-items: center; gap: 6px;">
                            <i class="fas fa-upload"></i> Browse Files
                        </button>
                    </div>
                    <div class="media-actions" style="z-index: 10; background: var(--body-bg, #fff); padding: 10px 0; margin-bottom: 10px; flex-shrink: 0;">
                        <button class="action-btn" data-action="select" disabled>
                            ${this.options.selectionMode === 'multiple' ? 'Select Items' : 'Select Item'}
                        </button>
                    </div>
                    <div class="media-grid-container upload-zone" style="flex: 1; overflow-y: auto; min-height: 400px; position: relative;">
                        <div class="upload-overlay" style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(65, 118, 144, 0.95); display: none; align-items: center; justify-content: center; z-index: 1000; border-radius: 4px; pointer-events: none;">
                            <div style="text-align: center; color: white;">
                                <i class="fas fa-cloud-upload-alt" style="font-size: 64px; margin-bottom: 15px; display: block;"></i>
                                <p style="font-size: 20px; font-weight: 500; margin: 0;">Drop files to upload</p>
                            </div>
                        </div>
                        <div class="media-grid view-grid"></div>
                    </div>
                </div>
            </div>
        `;

    const modal = this.showModal(modalContent);
    this.currentModal = modal;

    // Setup scroll listener for lazy loading
    const gridContainer = modal.querySelector('.media-grid-container');
    if (gridContainer) {
      gridContainer.addEventListener(
        'scroll',
        this.debounce(() => {
          const scrollHeight = gridContainer.scrollHeight;
          const scrollTop = gridContainer.scrollTop;
          const clientHeight = gridContainer.clientHeight;

          // Load more when scrolled to 80% of content
          if (scrollTop + clientHeight >= scrollHeight * 0.8) {
            this.loadMoreMedia();
          }
        }, 200)
      );
    }

    // Wait for DOM to be ready before loading media and initializing upload
    setTimeout(() => {
      console.log('[MediaLibrary] Loading media after modal render...');
      this.loadMedia();
      // Initialize upload zone now that the modal HTML exists
      this.initializeUploadZone(modal);
      // Setup search input now that modal exists
      this.setupSearchInput();

      // Attach click handler to upload button
      const uploadBtn = modal.querySelector('.upload-files-btn');
      if (uploadBtn && this.fileInput) {
        uploadBtn.addEventListener('click', e => {
          e.preventDefault();
          e.stopPropagation();
          this.fileInput.value = ''; // Clear to allow re-upload of same file
          this.fileInput.click();
        });
      }
    }, 100);
  }

  /**
   * Setup search input with AJAX-based filtering
   * Called after modal is created to ensure search input exists in DOM
   * Also works for standalone gallery page where search input exists on load
   */
  setupSearchInput() {
    // Try modal first, then gallery page
    const searchInput =
      document.querySelector('.ml-modal .search-input') ||
      document.querySelector('.media-gallery .search-input');
    if (!searchInput) {
      console.log('[MediaLibrary] No search input found');
      return;
    }

    // Check if already bound to prevent duplicate listeners
    if (searchInput.dataset.mlSearchBound === '1') {
      console.log('[MediaLibrary] Search input already bound, skipping');
      return;
    }
    searchInput.dataset.mlSearchBound = '1';

    // Prevent form submission on Enter key (which would refresh the page)
    searchInput.addEventListener('keydown', e => {
      if (e.key === 'Enter') {
        e.preventDefault();
        // Trigger search immediately on Enter
        this.searchQuery = searchInput.value;
        this.loadMedia();
      }
    });

    // Debounced search on input
    searchInput.addEventListener(
      'input',
      this.debounce(e => {
        console.log('[MediaLibrary] Search input changed:', e.target.value);
        this.searchQuery = e.target.value;
        this.loadMedia();
      }, 300)
    );

    console.log('[MediaLibrary] Search input initialized');
  }

  closeModal() {
    console.log('[MediaLibrary] closeModal called');
    // Use more specific selector to target only our dynamically-created modal
    const modal = document.querySelector('.media-modal.ml-modal');
    console.log('[MediaLibrary] Modal element found:', modal);
    if (modal) {
      console.log('[MediaLibrary] Removing modal from DOM');
      modal.remove();
      console.log('[MediaLibrary] Modal removed');
    } else {
      console.log('[MediaLibrary] No modal element found to remove');
    }

    // Clean up state so next openModal() starts fresh
    this.fileInput = null;
    this.currentModal = null;

    // Auto-close upload queue if there are no active uploads
    if (this.uploadQueue && !this.uploadQueue.hasActiveUploads()) {
      const queueContainer = document.querySelector('.upload-queue-container');
      if (queueContainer) {
        queueContainer.classList.add('hidden');
      }
    }
  }

  showLoading() {
    // Use specific selector to find grid in modal, not old custom modal grid
    const grid =
      document.querySelector('.ml-modal .media-grid') ||
      document.querySelector('.media-gallery .media-grid');
    if (grid) {
      grid.innerHTML = `
                <div class="loading">
                    <div class="spinner"></div>
                    <div>Loading media...</div>
                </div>
            `;
    }
  }

  hideLoading() {
    // Loading is hidden when new content is rendered
  }

  showError(message) {
    this.showNotification(message, 'error');
  }

  showSuccess(message) {
    this.showNotification(message, 'success');
  }

  showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;

    document.body.appendChild(notification);

    setTimeout(() => {
      notification.remove();
    }, 5000);
  }

  getCSRFToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    if (meta && meta.content) return meta.content;
    const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
    return csrfInput ? csrfInput.value : '';
  }

  formatFileSize(bytes) {
    if (bytes === 0) return '0 B';
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return `${(bytes / Math.pow(1024, i)).toFixed(1)} ${sizes[i]}`;
  }

  debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }

  handleEditDetails() {
    const selectedItems = Array.from(this.selectedItems);
    if (selectedItems.length === 0) {
      this.showError('Please select an item to edit');
      return;
    }

    if (selectedItems.length > 1) {
      this.showError('Please select only one item to edit');
      return;
    }

    // Get the media ID
    const mediaId = selectedItems[0];

    // Get current language from URL
    const path = window.location.pathname;
    const langMatch = path.match(/^\/([a-z]{2}(?:-[a-z]{2,4})?)\//);
    const lang = langMatch ? langMatch[1] : 'en';

    // Open the edit page in Django admin
    const editUrl = `/${lang}/admin/media_library/mediaasset/${mediaId}/change/`;
    window.open(editUrl, '_blank');
  }

  async handleDelete() {
    const selectedItems = Array.from(this.selectedItems);
    if (selectedItems.length === 0) {
      this.showError('Please select items to delete');
      return;
    }

    const confirmMsg = this.isRecycleBin
      ? `Are you sure you want to permanently delete ${selectedItems.length} item(s)? This action cannot be undone.`
      : `Are you sure you want to delete ${selectedItems.length} item(s)?`;

    if (!(await AdminModal.confirm({ message: confirmMsg, danger: true, confirmText: 'Delete' }))) {
      return;
    }

    // Get current language from URL
    const endpoint = '/api/media/assets/bulk_operations/';

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCSRFToken(),
        },
        body: JSON.stringify({
          action: this.isRecycleBin ? 'permanent_delete' : 'delete',
          ids: selectedItems,
        }),
      });

      const result = await response.json();

      if (response.ok) {
        this.showSuccess(result.message || 'Items deleted successfully');
        this.selectedItems.clear();
        this.loadMedia();
      } else {
        this.showError(result.error || 'Failed to delete items');
      }
    } catch (error) {
      console.error('Delete error:', error);
      this.showError('Failed to delete items');
    }
  }

  async handleRestore() {
    const selectedItems = Array.from(this.selectedItems);
    if (selectedItems.length === 0) {
      this.showError('Please select items to restore');
      return;
    }

    if (!(await AdminModal.confirm(`Restore ${selectedItems.length} item(s)?`))) {
      return;
    }

    // Get current language from URL
    try {
      const response = await fetch('/api/media/assets/bulk_operations/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCSRFToken(),
        },
        body: JSON.stringify({
          action: 'restore',
          ids: selectedItems,
        }),
      });

      const result = await response.json();

      if (response.ok) {
        this.showSuccess(result.message || 'Items restored successfully');
        this.selectedItems.clear();
        this.loadMedia();
      } else {
        this.showError(result.error || 'Failed to restore items');
      }
    } catch (error) {
      console.error('Restore error:', error);
      this.showError('Failed to restore items');
    }
  }

  handlePermanentDelete() {
    // Permanent delete is the same as delete when in recycle bin
    this.handleDelete();
  }

  handleSelect() {
    console.log('[MediaLibrary] handleSelect called');
    const selectedItems = Array.from(this.selectedItems);
    console.log('[MediaLibrary] Selected items:', selectedItems);

    if (selectedItems.length === 0) {
      console.log('[MediaLibrary] No items selected, showing error');
      this.showError('Please select media items');
      return;
    }

    // Get full media data for selected items
    const selectedData = this.getSelectedMediaData();
    console.log('[MediaLibrary] Selected media data:', selectedData);

    // Call onSelect callback if provided
    if (this.options.onSelect && typeof this.options.onSelect === 'function') {
      console.log('[MediaLibrary] Calling onSelect callback');
      this.options.onSelect(selectedData);
      console.log('[MediaLibrary] onSelect callback completed');
    } else {
      console.log('[MediaLibrary] No onSelect callback provided');
    }

    // Auto-close modal if requested
    if (this.options.autoClose) {
      console.log('[MediaLibrary] Auto-closing modal');
      this.closeModal();
    } else {
      console.log('[MediaLibrary] Not auto-closing (autoClose=false)');
    }
  }

  // Public API methods
  getSelectedItems() {
    return Array.from(this.selectedItems);
  }

  getSelectedMediaData() {
    // Return full media data for selected items from cache
    const selectedIds = this.getSelectedItems();
    const selectedData = [];

    selectedIds.forEach(id => {
      // First try to get from cache (has complete API data)
      const cachedItem = this.mediaDataCache.get(id);
      if (cachedItem) {
        // Build thumbnail URLs from the API data
        const thumbnails = [];
        if (cachedItem.thumbnail_url) {
          // Derive different sizes from thumbnail URL pattern
          const baseUrl = cachedItem.thumbnail_url.replace('_small.webp', '');
          thumbnails.push(
            { preset: 'small', url: cachedItem.thumbnail_url },
            { preset: 'medium', url: `${baseUrl}_medium.webp` },
            { preset: 'large', url: `${baseUrl}_large.webp` }
          );
        }

        // Determine the best display URL
        const displayUrl =
          cachedItem.display_url ||
          cachedItem.webp_file ||
          cachedItem.original_file ||
          cachedItem.url ||
          '';

        selectedData.push({
          id: id,
          title: cachedItem.title || '',
          alt_text: cachedItem.alt_text || '',
          description: cachedItem.description || '',
          url: displayUrl,
          original_url: cachedItem.original_file || cachedItem.url || displayUrl,
          webp_url: cachedItem.webp_file || '',
          thumbnail_url: cachedItem.thumbnail_url || '',
          thumbnails: thumbnails,
          type: cachedItem.mime_type?.startsWith('video/') ? 'video' : 'image',
          mime_type: cachedItem.mime_type || '',
          width: cachedItem.width || null,
          height: cachedItem.height || null,
          file_size: cachedItem.file_size || 0,
        });
      } else {
        // Fallback to DOM extraction if not in cache
        const mediaItem = document.querySelector(`[data-item-id="${id}"]`);
        if (mediaItem) {
          const img = mediaItem.querySelector('img');
          const title = mediaItem.querySelector('.title')?.textContent || '';

          selectedData.push({
            id: id,
            title: title,
            url: img ? img.src : '',
            original_url: img ? img.src : '',
            webp_url: '',
            thumbnail_url: '',
            thumbnails: [],
            type: mediaItem.dataset.type || 'image',
            mime_type: '',
            width: null,
            height: null,
            file_size: 0,
          });
        }
      }
    });

    return selectedData;
  }

  clearSelection() {
    this.selectedItems.clear();
    document.querySelectorAll('.media-item.selected').forEach(item => {
      item.classList.remove('selected');
    });
    this.updateSelectionUI();
  }

  selectItems(itemIds) {
    this.clearSelection();
    itemIds.forEach(id => {
      this.selectedItems.add(id);
      const item = document.querySelector(`[data-item-id="${id}"]`);
      if (item) {
        item.classList.add('selected');
      }
    });
    this.updateSelectionUI();
  }

  async showPreview(mediaItem) {
    // Check if a preview modal already exists and remove it
    const existingModal = document.querySelector('.media-preview-modal');
    if (existingModal) {
      existingModal.remove();
    }

    const itemId = mediaItem.dataset.itemId;
    const mediaType = mediaItem.dataset.type; // 'video', '3d', or 'image'
    const isVideo = mediaType === 'video';
    const is3DModel = mediaType === '3d';

    // Get media data
    const title = mediaItem.querySelector('.title').textContent;
    const imgElement = mediaItem.querySelector('img');
    const mediaUrl = imgElement ? imgElement.getAttribute('src') : '';

    // Get small thumbnail for instant display (already loaded in grid)
    const smallThumbnailUrl = mediaUrl;

    // Determine appropriate preview size based on viewport
    const isMobile = window.innerWidth < 768;
    const previewSize = isMobile ? 'medium' : 'large';

    // Get preview URL from cached data or fetch if needed
    let previewUrl = smallThumbnailUrl; // Fallback
    let useProgressiveLoading = false;

    if (!isVideo && !is3DModel && mediaUrl) {
      // Fetch media details if not cached (for server-rendered items)
      const cachedData = await this.fetchMediaDetails(itemId);
      if (cachedData) {
        // Check if this is an SVG (no thumbnails) or 3D model
        const isSVG = cachedData.mime_type === 'image/svg+xml';
        const has3DModel = cachedData.mime_type && cachedData.mime_type.startsWith('model/');

        if (isSVG) {
          // SVGs have no thumbnails - use original file directly
          previewUrl = cachedData.webp_file || cachedData.original_file || smallThumbnailUrl;
          useProgressiveLoading = false;
        } else if (has3DModel) {
          // 3D models show poster image (handled by template, keep current URL)
          previewUrl = smallThumbnailUrl;
          useProgressiveLoading = false;
        } else {
          // Regular raster images (JPG, PNG, WebP, GIF) - use progressive loading
          previewUrl = this.getThumbnailUrl(cachedData, previewSize);
          useProgressiveLoading = true;
        }
      }
      console.log('[MediaLibrary] Preview URL:', {
        original: mediaUrl,
        previewSize: previewSize,
        previewUrl: previewUrl,
        cached: !!cachedData,
        progressive: useProgressiveLoading,
      });
    }

    // Create preview modal
    const modal = document.createElement('div');
    modal.className = 'media-preview-modal';
    modal.innerHTML = `
            <div class="preview-overlay">
                <div class="preview-header">
                    <h3 class="preview-title">${title}</h3>
                    <div class="preview-controls">
                        <button class="preview-nav prev" title="Previous (←)">‹</button>
                        <button class="preview-nav next" title="Next (→)">›</button>
                        ${
                          !isVideo
                            ? `
                        <button class="preview-zoom-in" title="Zoom In (+)">🔍+</button>
                        <button class="preview-zoom-out" title="Zoom Out (-)">🔍-</button>
                        <button class="preview-zoom-reset" title="Reset Zoom">1:1</button>
                        `
                            : ''
                        }
                        <button class="preview-close" title="Close (Esc)">×</button>
                    </div>
                </div>
                <div class="media-preview-content">
                    ${isVideo ? this.createVideoPreview(itemId) : this.createImagePreview(smallThumbnailUrl, previewUrl, title)}
                </div>
            </div>
        `;

    document.body.appendChild(modal);

    // Trigger progressive image load after modal renders
    if (!isVideo) {
      setTimeout(() => this.loadPreviewImage(modal), 50);
    }

    this.setupPreviewHandlers(modal, itemId);
    this.setupPreviewKeyboardNav(modal);
  }

  createVideoPreview(itemId) {
    // Create video element with error handling
    // Try optimized WebM first, then fallback to MP4
    const videoHtml = `
            <div class="video-preview-container">
                <video controls class="preview-video" id="preview-video-${itemId}">
                    <source src="/api/media/assets/${itemId}/stream/" type="video/webm">
                    <source src="/api/media/assets/${itemId}/stream/?format=mp4" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
                <div class="video-error" style="display: none; padding: 20px; text-align: center; color: var(--error-fg);">
                    <p>Unable to load video. The video may still be processing or the format may not be supported.</p>
                </div>
            </div>
        `;

    // Add error handling after modal is created
    setTimeout(() => {
      const video = document.getElementById(`preview-video-${itemId}`);
      if (video) {
        video.addEventListener('error', e => {
          console.error('Video error:', e);
          const container = video.closest('.video-preview-container');
          const errorDiv = container.querySelector('.video-error');
          if (errorDiv) {
            video.style.display = 'none';
            errorDiv.style.display = 'block';
          }
        });

        // Try to play
        video.play().catch(err => {
          console.log('Autoplay prevented:', err);
        });
      }
    }, 100);

    return videoHtml;
  }

  createImagePreview(smallUrl, previewUrl, altText) {
    return `
            <div class="image-preview-container">
                <img src="${smallUrl}"
                     alt="${altText}"
                     class="preview-image preview-placeholder"
                     data-preview-src="${previewUrl}">
                <div class="preview-loading">
                    <div class="spinner"></div>
                </div>
            </div>
        `;
  }

  loadPreviewImage(modal) {
    const img = modal.querySelector('.preview-image');
    const loading = modal.querySelector('.preview-loading');
    const previewUrl = img ? img.dataset.previewSrc : null;

    if (!previewUrl || !img || !loading) return;

    // Check if preview URL is same as current src (no progressive loading needed)
    const currentSrc = img.getAttribute('src');
    if (previewUrl === currentSrc) {
      // No need to load - already showing the final image
      img.classList.remove('preview-placeholder');
      img.classList.add('preview-loaded');
      loading.style.display = 'none';
      return;
    }

    // Create new Image object to preload
    const previewImage = new Image();

    previewImage.onload = () => {
      // Swap to high-quality preview
      img.src = previewUrl;
      img.classList.remove('preview-placeholder');
      img.classList.add('preview-loaded');
      loading.style.display = 'none';
    };

    previewImage.onerror = () => {
      // Keep placeholder, show error
      loading.innerHTML = '<p class="error">⚠️ Failed to load preview</p>';
      console.error('[MediaLibrary] Failed to load preview:', previewUrl);
    };

    // Start loading
    previewImage.src = previewUrl;
  }

  setupPreviewHandlers(modal, currentItemId) {
    let zoomLevel = 1;

    // Close button
    modal.querySelector('.preview-close').addEventListener('click', () => modal.remove());

    // Click outside to close
    modal.addEventListener('click', e => {
      if (e.target === modal) modal.remove();
    });

    // Navigation
    const items = Array.from(document.querySelectorAll('.media-item'));
    const currentIndex = items.findIndex(item => item.dataset.itemId === currentItemId);

    modal.querySelector('.prev').addEventListener('click', () => {
      if (currentIndex > 0) {
        modal.remove();
        this.showPreview(items[currentIndex - 1]);
      }
    });

    modal.querySelector('.next').addEventListener('click', () => {
      if (currentIndex < items.length - 1) {
        modal.remove();
        this.showPreview(items[currentIndex + 1]);
      }
    });

    // Zoom controls for images
    const zoomIn = modal.querySelector('.preview-zoom-in');
    const zoomOut = modal.querySelector('.preview-zoom-out');
    const zoomReset = modal.querySelector('.preview-zoom-reset');

    if (zoomIn && zoomOut && zoomReset) {
      const img = modal.querySelector('.preview-image');

      zoomIn.addEventListener('click', () => {
        zoomLevel = Math.min(zoomLevel * 1.2, 3);
        img.style.transform = `scale(${zoomLevel})`;
      });

      zoomOut.addEventListener('click', () => {
        zoomLevel = Math.max(zoomLevel / 1.2, 0.5);
        img.style.transform = `scale(${zoomLevel})`;
      });

      zoomReset.addEventListener('click', () => {
        zoomLevel = 1;
        img.style.transform = 'scale(1)';
      });
    }
  }

  setupPreviewKeyboardNav(modal) {
    const handleKeydown = e => {
      switch (e.key) {
        case 'Escape':
          modal.remove();
          document.removeEventListener('keydown', handleKeydown);
          break;
        case 'ArrowLeft':
          modal.querySelector('.prev')?.click();
          break;
        case 'ArrowRight':
          modal.querySelector('.next')?.click();
          break;
      }
    };
    document.addEventListener('keydown', handleKeydown);
  }
}

// Widget for Django admin integration
class MediaLibraryWidget {
  constructor(fieldName, options = {}) {
    this.fieldName = fieldName;
    this.options = options;
    this.init();
  }

  init() {
    const field = document.querySelector(`[name="${this.fieldName}"]`);
    if (!field) return;

    // Create browse button
    const browseBtn = document.createElement('button');
    browseBtn.type = 'button';
    browseBtn.className = 'btn btn-secondary';
    browseBtn.textContent = 'Browse Media Library';

    // Insert after the field
    field.parentNode.insertBefore(browseBtn, field.nextSibling);

    browseBtn.addEventListener('click', () => {
      this.openMediaLibrary();
    });
  }

  openMediaLibrary() {
    const mediaLibrary = new MediaLibrary({
      selectionMode: 'single',
      ...this.options,
    });

    const modalContent = `
            <div class="media-gallery">
                <div class="media-sidebar">
                    <div class="sidebar-section">
                        <h3>Folders</h3>
                        <ul class="folder-tree">
                            <li><a href="#" data-folder-id="">All Files</a></li>
                        </ul>
                    </div>
                    <div class="sidebar-section">
                        <h3>Tags</h3>
                        <div class="tag-cloud"></div>
                    </div>
                </div>
                <div class="media-content">
                    <div class="media-search">
                        <input type="text" class="search-input" placeholder="Search media...">
                    </div>
                    <div class="media-actions">
                        <button class="action-btn" data-action="select" disabled>Select Item</button>
                    </div>
                    <div class="media-grid"></div>
                </div>
            </div>
        `;

    const modal = mediaLibrary.showModal(modalContent);

    // Handle selection
    const selectBtn = modal.querySelector('[data-action="select"]');
    selectBtn.addEventListener('click', () => {
      const selected = mediaLibrary.getSelectedItems();
      if (selected.length > 0) {
        this.selectMedia(selected[0]);
        mediaLibrary.closeModal();
      }
    });

    // Load initial data
    mediaLibrary.loadMedia();
  }

  selectMedia(itemId) {
    const field = document.querySelector(`[name="${this.fieldName}"]`);
    if (field) {
      field.value = itemId;

      // Trigger change event
      field.dispatchEvent(new Event('change', { bubbles: true }));
    }
  }
}

// Auto-initialize for Django admin
document.addEventListener('DOMContentLoaded', () => {
  // Initialize media library if gallery exists
  const gallery = document.querySelector('.media-gallery');
  if (gallery) {
    window.mediaLibrary = new MediaLibrary();
  }

  // Initialize widgets for image fields
  document.querySelectorAll('[data-media-widget]').forEach(element => {
    const fieldName = element.dataset.fieldName;
    new MediaLibraryWidget(fieldName);
  });
});

// Export for use in other scripts
window.MediaLibrary = MediaLibrary;
window.MediaLibraryWidget = MediaLibraryWidget;

// Global convenience wrapper functions for easy media library integration
window.selectImageFromLibrary = function (callback, options = {}) {
  const ml = new MediaLibrary({
    selectionMode: 'single',
    fileTypeFilter: 'image',
    onSelect: selectedMedia => {
      // Return single item for single selection
      callback(selectedMedia[0] || null);
    },
    autoClose: true,
    ...options,
  });
  ml.openModal();
  return ml;
};

window.selectMediaFromLibrary = function (callback, options = {}) {
  const ml = new MediaLibrary({
    selectionMode: 'single',
    onSelect: selectedMedia => {
      // Return single item for single selection
      callback(selectedMedia[0] || null);
    },
    autoClose: true,
    ...options,
  });
  ml.openModal();
  return ml;
};

window.selectMultipleMedia = function (callback, options = {}) {
  console.log('[selectMultipleMedia] Creating MediaLibrary instance with options:', options);
  const ml = new MediaLibrary({
    selectionMode: 'multiple',
    onSelect: selectedMedia => {
      console.log('[selectMultipleMedia] onSelect wrapper called with:', selectedMedia);
      // Return array of selected media
      callback(selectedMedia);
    },
    autoClose: true,
    ...options,
  });
  console.log('[selectMultipleMedia] Opening modal');
  ml.openModal();
  return ml;
};
