/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  let translations = {};

  function init() {
    const dataEl = document.getElementById('loyaltyreward-form-data');
    if (dataEl) {
      try {
        const data = JSON.parse(dataEl.textContent);
        translations = data.translations || {};
      } catch (e) {}
    }

    setTimeout(function () {
      initializePreview();
      checkOverflowConstraints();
    }, 100);
  }

  function checkOverflowConstraints() {
    const previewFloat = document.querySelector('.reward-preview-float');
    if (!previewFloat) {
      return;
    }
    let element = previewFloat.parentElement;
    while (element && element !== document.body) {
      const computed = window.getComputedStyle(element);
      const overflow = computed.overflow;
      const overflowY = computed.overflowY;
      if (overflow !== 'visible' || overflowY !== 'visible') {
        console.log(
          'Overflow constraint on ' +
            element.tagName +
            (element.id ? '#' + element.id : '') +
            ': overflow=' +
            overflow +
            ', overflowY=' +
            overflowY
        );
      }
      element = element.parentElement;
    }
  }

  let imageFieldInterval = null;

  function initializePreview() {
    const nameField = document.querySelector('#id_name');
    const descriptionField = document.querySelector('#id_description');
    const pointsField = document.querySelector('#id_points_cost');
    const iconField = document.querySelector('#id_icon');
    const rewardTypeField = document.querySelector('#id_reward_type');
    const isActiveField = document.querySelector('#id_is_active');
    const featuredField = document.querySelector('#id_featured');

    if (nameField) {
      nameField.addEventListener('input', updatePreview);
    }
    if (descriptionField) {
      descriptionField.addEventListener('input', updatePreview);
    }
    if (pointsField) {
      pointsField.addEventListener('input', updatePreview);
    }
    if (iconField) {
      iconField.addEventListener('change', updatePreview);
      document.addEventListener('searchable-select-change', function (e) {
        if (e.detail && e.detail.select === iconField) {
          updatePreview();
        }
      });
    }
    if (rewardTypeField) {
      rewardTypeField.addEventListener('change', function () {
        updateFieldVisibility();
        updatePreview();
      });
    }
    if (isActiveField) {
      isActiveField.addEventListener('change', updatePreview);
    }
    if (featuredField) {
      featuredField.addEventListener('change', updatePreview);
    }

    updatePreview();
    updateFieldVisibility();

    const imageInput = document.querySelector('input[name="image"]');
    if (imageInput) {
      let lastImageValue = imageInput.value;
      if (imageInput.value) {
        updateImagePreview();
      }
      imageFieldInterval = setInterval(function () {
        if (imageInput.value !== lastImageValue) {
          lastImageValue = imageInput.value;
          updateImagePreview();
        }
      }, 500);
    }
  }

  function updatePreview() {
    const nameField = document.querySelector('#id_name');
    const descriptionField = document.querySelector('#id_description');
    const pointsField = document.querySelector('#id_points_cost');
    const iconField = document.querySelector('#id_icon');
    const rewardTypeField = document.querySelector('#id_reward_type');
    const isActiveField = document.querySelector('#id_is_active');
    const featuredField = document.querySelector('#id_featured');

    const previewName = document.getElementById('preview-name');
    const previewDescription = document.getElementById('preview-description');
    const previewPoints = document.getElementById('preview-points');
    const previewIcon = document.getElementById('preview-icon');
    const previewBadges = document.getElementById('preview-badges');

    if (nameField && previewName) {
      previewName.textContent = nameField.value || translations.newReward || 'New Reward';
    }
    if (descriptionField && previewDescription) {
      previewDescription.textContent =
        descriptionField.value || translations.enterDescription || 'Enter a description...';
    }
    if (pointsField && previewPoints) {
      previewPoints.textContent = pointsField.value || '0';
    }
    if (iconField && previewIcon) {
      previewIcon.className =
        'fas ' + (iconField.value || 'fa-gift') + ' reward-preview-icon-placeholder';
    }

    if (previewBadges) {
      let badgesHTML = '';
      if (rewardTypeField) {
        const typeText = rewardTypeField.options[rewardTypeField.selectedIndex].text;
        const typeValue = rewardTypeField.value;
        let typeClass = 'primary';
        if (typeValue === 'product') {
          typeClass = 'success';
        } else if (typeValue === 'shipping') {
          typeClass = 'info';
        } else if (typeValue === 'experience') {
          typeClass = 'warning';
        }
        badgesHTML +=
          '<span class="reward-preview-badge ' +
          typeClass +
          '">' +
          '<i class="fas fa-tag"></i> ' +
          typeText +
          '</span>';
      }
      if (isActiveField) {
        if (isActiveField.checked) {
          badgesHTML +=
            '<span class="reward-preview-badge success">' +
            '<i class="fas fa-check-circle"></i> ' +
            (translations.active || 'Active') +
            '</span>';
        } else {
          badgesHTML +=
            '<span class="reward-preview-badge error">' +
            '<i class="fas fa-times-circle"></i> ' +
            (translations.inactive || 'Inactive') +
            '</span>';
        }
      }
      if (featuredField && featuredField.checked) {
        badgesHTML +=
          '<span class="reward-preview-badge warning">' +
          '<i class="fas fa-star"></i> ' +
          (translations.featured || 'Featured') +
          '</span>';
      }
      previewBadges.innerHTML = badgesHTML;
    }
  }

  function updateImagePreview() {
    const imageInput = document.querySelector('input[name="image"]');
    const iconField = document.querySelector('#id_icon');
    const previewImageContainer = document.getElementById('preview-image-container');

    if (!previewImageContainer) {
      return;
    }

    if (imageInput && imageInput.value) {
      const imageUrl = imageInput.value;
      let thumbnailUrl = imageUrl;
      if (imageUrl.indexOf('/media/') !== -1) {
        const parts = imageUrl.split('/media/');
        if (parts.length > 1) {
          thumbnailUrl = '/media/thumbnails/medium/' + parts[1];
        }
      }
      const img = document.createElement('img');
      img.src = thumbnailUrl;
      img.className = 'reward-preview-image';
      img.alt = 'Reward image';
      img.onerror = function () {
        this.src = imageUrl;
      };
      previewImageContainer.innerHTML = '';
      previewImageContainer.appendChild(img);
    } else {
      const iconClass = iconField && iconField.value ? iconField.value : 'fa-gift';
      previewImageContainer.innerHTML =
        '<i class="fas ' + iconClass + ' reward-preview-icon-placeholder" id="preview-icon"></i>';
    }
  }

  function updateFieldVisibility() {
    const rewardTypeField = document.querySelector('#id_reward_type');
    if (!rewardTypeField) {
      return;
    }
    const selectedType = rewardTypeField.value;
    const fieldsets = document.querySelectorAll('.module');
    fieldsets.forEach(function (fieldset) {
      const header = fieldset.querySelector('h2');
      if (!header) {
        return;
      }
      const headerText = header.textContent.trim();
      if (
        headerText.indexOf('Discount Configuration') !== -1 ||
        headerText.indexOf('Discount configuration') !== -1
      ) {
        fieldset.style.display = selectedType === 'discount' ? '' : 'none';
      }
      if (
        headerText.indexOf('Product Configuration') !== -1 ||
        headerText.indexOf('Product configuration') !== -1
      ) {
        fieldset.style.display = selectedType === 'product' ? '' : 'none';
      }
    });
  }

  document.addEventListener('DOMContentLoaded', init);
})();
