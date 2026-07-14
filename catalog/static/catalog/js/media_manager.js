/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Media Manager
 * Generic media library modal, image selection, and drag-and-drop reordering
 * Configurable for products, variants, and other entities
 */

class MediaManager {
  constructor(config = {}) {
    // Merge config with defaults
    this.config = {
      entityType: config.entityType || 'product',
      entityId: config.entityId || null,
      gridContainerId: config.gridContainerId || 'product-images-grid',
      hiddenFieldId: config.hiddenFieldId || 'product-images-data',
      addButtonId: config.addButtonId || 'add-media-btn',
      cardClass: config.cardClass || 'product-image-card',
    };

    // Initialize DOM references
    this.imagesGrid = document.getElementById(this.config.gridContainerId);
    this.addMediaBtn = document.getElementById(this.config.addButtonId);
    this.hiddenField = document.getElementById(this.config.hiddenFieldId);
    this.sortable = null;

    this.init();
  }

  init() {
    if (!this.addMediaBtn) return;

    // Initialize Sortable for image reordering
    this.initSortable();

    // Setup button event listeners
    this.addMediaBtn.addEventListener('click', () => this.openModal());

    // Setup delete buttons for existing images
    this.setupDeleteButtons();

    // Setup primary toggle handlers
    this.setupPrimaryToggles();

    // Initialize hidden field with existing images on page load
    this.updateImagePositions();
  }

  initSortable() {
    if (!this.imagesGrid || !window.Sortable) return;

    this.sortable = Sortable.create(this.imagesGrid, {
      animation: 150,
      handle: '.drag-handle',
      ghostClass: 'sortable-ghost',
      onEnd: () => {
        this.updateImagePositions();
      },
    });
  }

  openModal() {
    // Use the global selectMultipleMedia wrapper to open media library
    window.selectMultipleMedia(
      selectedMedia => {
        this.addSelectedImages(selectedMedia);
      },
      {
        fileTypeFilter: 'image',
      }
    );
  }

  addSelectedImages(selectedMedia) {
    if (!selectedMedia || selectedMedia.length === 0) {
      return;
    }

    // Remove "no images" placeholder if it exists
    const placeholder = this.imagesGrid.querySelector('.no-images-placeholder');
    if (placeholder) {
      placeholder.remove();
    }

    // Add new image cards
    selectedMedia.forEach((media, index) => {
      // The media.url already points to medium thumbnail from the modal
      // No need to modify it, just use it directly
      const cardHTML = this.createImageCard({
        id: `new_${Date.now()}_${index}`,
        media_asset_id: media.id,
        thumbnail: media.url, // Already medium thumbnail
        alt_text: media.title || '',
        show_in_gallery: true,
        show_in_listing: true,
        is_primary: false,
      });

      this.imagesGrid.insertAdjacentHTML('beforeend', cardHTML);
    });

    // Re-setup delete buttons and toggles
    this.setupDeleteButtons();
    this.setupPrimaryToggles();

    // Update positions
    this.updateImagePositions();
  }

  createImageCard(image) {
    return `
            <div class="${this.config.cardClass}" data-image-id="${image.id}" data-media-asset-id="${image.media_asset_id}">
                <div class="image-card-header">
                    <i class="fas fa-grip-vertical drag-handle"></i>
                    ${image.is_primary ? '<span class="primary-badge"><i class="fas fa-star"></i> Primary</span>' : ''}
                    <button type="button" class="image-card-delete" data-image-id="${image.id}" aria-label="Delete image">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <div class="image-card-preview">
                    <img src="${image.thumbnail}" alt="${image.alt_text}">
                </div>
                <div class="image-card-details">
                    <div class="form-row">
                        <label for="alt_text_${image.id}">Alt Text</label>
                        <input type="text"
                               id="alt_text_${image.id}"
                               name="image_${image.id}_alt_text"
                               value="${image.alt_text}"
                               class="image-alt-input">
                    </div>
                    <div class="image-card-toggles">
                        <label class="toggle-label" for="image_${image.id}_show_in_gallery">
                            <input type="checkbox"
                                   id="image_${image.id}_show_in_gallery"
                                   name="image_${image.id}_show_in_gallery"
                                   ${image.show_in_gallery ? 'checked' : ''}
                                   class="image-toggle">
                            <span>Show in Gallery</span>
                        </label>
                        <label class="toggle-label" for="image_${image.id}_show_in_listing">
                            <input type="checkbox"
                                   id="image_${image.id}_show_in_listing"
                                   name="image_${image.id}_show_in_listing"
                                   ${image.show_in_listing ? 'checked' : ''}
                                   class="image-toggle">
                            <span>Show in Listing</span>
                        </label>
                        <label class="toggle-label" for="image_${image.id}_is_primary">
                            <input type="checkbox"
                                   id="image_${image.id}_is_primary"
                                   name="image_${image.id}_is_primary"
                                   ${image.is_primary ? 'checked' : ''}
                                   class="image-primary-toggle"
                                   data-image-id="${image.id}">
                            <span>Set as Primary</span>
                        </label>
                    </div>
                </div>
            </div>
        `;
  }

  setupDeleteButtons() {
    this.imagesGrid.querySelectorAll('.image-card-delete').forEach(btn => {
      btn.addEventListener('click', async e => {
        const card = e.target.closest(`.${this.config.cardClass}`);
        if (
          await AdminModal.confirm({
            message: 'Are you sure you want to remove this image?',
            danger: true,
            confirmText: 'Remove',
          })
        ) {
          card.remove();
          this.updateImagePositions();

          // Show placeholder if no images left
          if (this.imagesGrid.querySelectorAll(`.${this.config.cardClass}`).length === 0) {
            this.imagesGrid.innerHTML = `
                            <div class="no-images-placeholder">
                                <i class="fas fa-images"></i>
                                <p>No images added yet</p>
                                <p class="help">Click the button below to add images from your media library</p>
                            </div>
                        `;
          }
        }
      });
    });
  }

  setupPrimaryToggles() {
    this.imagesGrid.querySelectorAll('.image-primary-toggle').forEach(toggle => {
      toggle.addEventListener('change', e => {
        if (e.target.checked) {
          // Uncheck all other primary toggles
          this.imagesGrid.querySelectorAll('.image-primary-toggle').forEach(other => {
            if (other !== e.target) {
              other.checked = false;
              // Remove primary badge from other cards
              const otherCard = other.closest(`.${this.config.cardClass}`);
              const badge = otherCard.querySelector('.primary-badge');
              if (badge) badge.remove();
            }
          });

          // Add primary badge to this card
          const card = e.target.closest(`.${this.config.cardClass}`);
          const header = card.querySelector('.image-card-header');
          if (!header.querySelector('.primary-badge')) {
            const dragHandle = header.querySelector('.drag-handle');
            dragHandle.insertAdjacentHTML(
              'afterend',
              '<span class="primary-badge"><i class="fas fa-star"></i> Primary</span>'
            );
          }
        } else {
          // Remove primary badge
          const card = e.target.closest(`.${this.config.cardClass}`);
          const badge = card.querySelector('.primary-badge');
          if (badge) badge.remove();
        }

        this.updateImagePositions();
      });
    });
  }

  updateImagePositions() {
    const cards = this.imagesGrid.querySelectorAll(`.${this.config.cardClass}`);
    const imagesData = [];

    cards.forEach((card, index) => {
      const imageId = card.dataset.imageId;
      const mediaAssetId = card.dataset.mediaAssetId;
      const altInput = card.querySelector('.image-alt-input');
      const showInGallery = card.querySelector('[name*="_show_in_gallery"]');
      const showInListing = card.querySelector('[name*="_show_in_listing"]');
      const isPrimary = card.querySelector('.image-primary-toggle');

      imagesData.push({
        id: imageId.startsWith('new_') ? null : imageId,
        media_asset_id: mediaAssetId,
        alt_text: altInput ? altInput.value : '',
        show_in_gallery: showInGallery ? showInGallery.checked : true,
        show_in_listing: showInListing ? showInListing.checked : true,
        is_primary: isPrimary ? isPrimary.checked : false,
        position: index,
      });
    });

    // Store in hidden field for form submission
    if (this.hiddenField) {
      this.hiddenField.value = JSON.stringify(imagesData);
    } else {
      console.error(`[MediaManager] Hidden field #${this.config.hiddenFieldId} not found!`);
    }
  }
}

// Initialize for products when DOM is ready (backward compatibility)
document.addEventListener('DOMContentLoaded', () => {
  // Only initialize if product image elements exist
  if (document.getElementById('product-images-grid')) {
    window.productMediaManager = new MediaManager({
      entityType: 'product',
      gridContainerId: 'product-images-grid',
      hiddenFieldId: 'product-images-data',
      addButtonId: 'add-media-btn',
      cardClass: 'product-image-card',
    });
  }
});
