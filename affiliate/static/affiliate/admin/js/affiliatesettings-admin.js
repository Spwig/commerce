/**
 * Affiliate Settings Admin
 * Handles the features/steps JSON editor and live preview for the affiliate settings change form.
 * Translations are loaded from a <script type="application/json" id="affiliatesettings-translations"> island.
 */
(function () {
  'use strict';

  // Load translations from JSON island
  let T = {};
  const translationsEl = document.getElementById('affiliatesettings-translations');
  if (translationsEl) {
    try {
      T = JSON.parse(translationsEl.textContent);
    } catch (e) {}
  }

  // Icon choices for the dropdown
  const ICON_CHOICES = [
    { value: 'fas fa-dollar-sign', label: 'Dollar Sign' },
    { value: 'fas fa-clock', label: 'Clock' },
    { value: 'fas fa-chart-bar', label: 'Chart' },
    { value: 'fas fa-chart-line', label: 'Line Chart' },
    { value: 'fas fa-money-bill-wave', label: 'Money' },
    { value: 'fas fa-headset', label: 'Support' },
    { value: 'fas fa-tools', label: 'Tools' },
    { value: 'fas fa-gift', label: 'Gift' },
    { value: 'fas fa-percent', label: 'Percent' },
    { value: 'fas fa-star', label: 'Star' },
    { value: 'fas fa-heart', label: 'Heart' },
    { value: 'fas fa-bolt', label: 'Bolt' },
    { value: 'fas fa-shield-alt', label: 'Shield' },
    { value: 'fas fa-lock', label: 'Lock' },
    { value: 'fas fa-check-circle', label: 'Check Circle' },
    { value: 'fas fa-users', label: 'Users' },
    { value: 'fas fa-globe', label: 'Globe' },
    { value: 'fas fa-rocket', label: 'Rocket' },
    { value: 'fas fa-trophy', label: 'Trophy' },
    { value: 'fas fa-gem', label: 'Gem' },
    { value: 'fas fa-link', label: 'Link' },
    { value: 'fas fa-share-alt', label: 'Share' },
    { value: 'fas fa-envelope', label: 'Email' },
    { value: 'fas fa-mobile-alt', label: 'Mobile' },
    { value: 'fas fa-laptop', label: 'Laptop' },
    { value: 'fas fa-credit-card', label: 'Credit Card' },
    { value: 'fas fa-wallet', label: 'Wallet' },
    { value: 'fas fa-hand-holding-usd', label: 'Hand Holding Money' },
    { value: 'fas fa-piggy-bank', label: 'Piggy Bank' },
    { value: 'fas fa-coins', label: 'Coins' },
  ];

  // Element references - populated in init()
  let heroTitleField, heroSubtitleField, featuresTitleField, featuresField;
  let howItWorksTitleField, stepsField, ctaTitleField, ctaDescriptionField;
  let previewHeroTitle, previewHeroSubtitle, previewFeaturesTitle, previewFeaturesGrid;
  let previewStepsTitle, previewStepsContainer, previewCtaTitle, previewCtaDescription;

  function initElements() {
    heroTitleField = document.getElementById('id_hero_title');
    heroSubtitleField = document.getElementById('id_hero_subtitle');
    featuresTitleField = document.getElementById('id_features_title');
    featuresField = document.getElementById('id_features');
    howItWorksTitleField = document.getElementById('id_how_it_works_title');
    stepsField = document.getElementById('id_steps');
    ctaTitleField = document.getElementById('id_cta_title');
    ctaDescriptionField = document.getElementById('id_cta_description');

    previewHeroTitle = document.getElementById('preview-hero-title');
    previewHeroSubtitle = document.getElementById('preview-hero-subtitle');
    previewFeaturesTitle = document.getElementById('preview-features-title');
    previewFeaturesGrid = document.getElementById('preview-features-grid');
    previewStepsTitle = document.getElementById('preview-steps-title');
    previewStepsContainer = document.getElementById('preview-steps-container');
    previewCtaTitle = document.getElementById('preview-cta-title');
    previewCtaDescription = document.getElementById('preview-cta-description');
  }

  function parseJSON(value) {
    try {
      return JSON.parse(value) || [];
    } catch (e) {
      return [];
    }
  }

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  function createIconSelect(currentValue) {
    const select = document.createElement('select');
    select.className = 'icon-select';
    ICON_CHOICES.forEach(function (choice) {
      const option = document.createElement('option');
      option.value = choice.value;
      option.textContent = choice.label;
      if (choice.value === currentValue) option.selected = true;
      select.appendChild(option);
    });
    return select;
  }

  function createFeatureItem(feature, index) {
    const item = document.createElement('div');
    item.className = 'json-item';
    item.dataset.index = index;

    item.innerHTML =
      '<div class="json-item-header">' +
      '<span class="item-number">' +
      T.feature +
      ' #' +
      (index + 1) +
      '</span>' +
      '<div class="json-item-actions">' +
      '<button type="button" class="move-up-btn" title="' +
      T.moveUp +
      '"><i class="fas fa-arrow-up"></i></button>' +
      '<button type="button" class="move-down-btn" title="' +
      T.moveDown +
      '"><i class="fas fa-arrow-down"></i></button>' +
      '<button type="button" class="delete-btn" title="' +
      T.delete +
      '"><i class="fas fa-trash"></i></button>' +
      '</div>' +
      '</div>' +
      '<div class="json-item-field">' +
      '<label>' +
      T.icon +
      '</label>' +
      '<div class="icon-selector-wrapper">' +
      '<div class="icon-preview"><i class="' +
      (feature.icon || 'fas fa-star') +
      '"></i></div>' +
      '<div class="icon-select-container"></div>' +
      '</div>' +
      '</div>' +
      '<div class="json-item-field">' +
      '<label>' +
      T.title +
      '</label>' +
      '<div class="field-with-translate">' +
      '<input type="text" class="feature-title" value="' +
      escapeHtml(feature.title || '') +
      '">' +
      '<button type="button" class="translate-btn" data-field="features.' +
      index +
      '.title" title="' +
      T.translate +
      '">' +
      '<i class="fas fa-language"></i>' +
      '</button>' +
      '</div>' +
      '</div>' +
      '<div class="json-item-field">' +
      '<label>' +
      T.description +
      '</label>' +
      '<div class="field-with-translate">' +
      '<textarea class="feature-description">' +
      escapeHtml(feature.description || '') +
      '</textarea>' +
      '<button type="button" class="translate-btn" data-field="features.' +
      index +
      '.description" title="' +
      T.translate +
      '">' +
      '<i class="fas fa-language"></i>' +
      '</button>' +
      '</div>' +
      '</div>';

    const iconContainer = item.querySelector('.icon-select-container');
    const iconSelect = createIconSelect(feature.icon || 'fas fa-star');
    iconContainer.appendChild(iconSelect);

    iconSelect.addEventListener('change', function () {
      item.querySelector('.icon-preview i').className = this.value;
      updateFeatures();
    });

    item.querySelector('.feature-title').addEventListener('input', updateFeatures);
    item.querySelector('.feature-description').addEventListener('input', updateFeatures);
    item.querySelector('.delete-btn').addEventListener('click', function () {
      item.remove();
      renumberItems('features');
      updateFeatures();
    });
    item.querySelector('.move-up-btn').addEventListener('click', function () {
      const prev = item.previousElementSibling;
      if (prev && prev.classList.contains('json-item')) {
        item.parentNode.insertBefore(item, prev);
        renumberItems('features');
        updateFeatures();
      }
    });
    item.querySelector('.move-down-btn').addEventListener('click', function () {
      const next = item.nextElementSibling;
      if (next && next.classList.contains('json-item')) {
        item.parentNode.insertBefore(next, item);
        renumberItems('features');
        updateFeatures();
      }
    });
    item.querySelectorAll('.translate-btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        openTranslationEditor(btn.dataset.field, 'text');
      });
    });

    return item;
  }

  function createStepItem(step, index) {
    const item = document.createElement('div');
    item.className = 'json-item';
    item.dataset.index = index;

    item.innerHTML =
      '<div class="json-item-header">' +
      '<span class="item-number">' +
      T.step +
      ' #' +
      (index + 1) +
      '</span>' +
      '<div class="json-item-actions">' +
      '<button type="button" class="move-up-btn" title="' +
      T.moveUp +
      '"><i class="fas fa-arrow-up"></i></button>' +
      '<button type="button" class="move-down-btn" title="' +
      T.moveDown +
      '"><i class="fas fa-arrow-down"></i></button>' +
      '<button type="button" class="delete-btn" title="' +
      T.delete +
      '"><i class="fas fa-trash"></i></button>' +
      '</div>' +
      '</div>' +
      '<div class="json-item-field">' +
      '<label>' +
      T.title +
      '</label>' +
      '<div class="field-with-translate">' +
      '<input type="text" class="step-title" value="' +
      escapeHtml(step.title || '') +
      '">' +
      '<button type="button" class="translate-btn" data-field="steps.' +
      index +
      '.title" title="' +
      T.translate +
      '">' +
      '<i class="fas fa-language"></i>' +
      '</button>' +
      '</div>' +
      '</div>' +
      '<div class="json-item-field">' +
      '<label>' +
      T.description +
      '</label>' +
      '<div class="field-with-translate">' +
      '<textarea class="step-description">' +
      escapeHtml(step.description || '') +
      '</textarea>' +
      '<button type="button" class="translate-btn" data-field="steps.' +
      index +
      '.description" title="' +
      T.translate +
      '">' +
      '<i class="fas fa-language"></i>' +
      '</button>' +
      '</div>' +
      '</div>';

    item.querySelector('.step-title').addEventListener('input', updateSteps);
    item.querySelector('.step-description').addEventListener('input', updateSteps);
    item.querySelector('.delete-btn').addEventListener('click', function () {
      item.remove();
      renumberItems('steps');
      updateSteps();
    });
    item.querySelector('.move-up-btn').addEventListener('click', function () {
      const prev = item.previousElementSibling;
      if (prev && prev.classList.contains('json-item')) {
        item.parentNode.insertBefore(item, prev);
        renumberItems('steps');
        updateSteps();
      }
    });
    item.querySelector('.move-down-btn').addEventListener('click', function () {
      const next = item.nextElementSibling;
      if (next && next.classList.contains('json-item')) {
        item.parentNode.insertBefore(next, item);
        renumberItems('steps');
        updateSteps();
      }
    });
    item.querySelectorAll('.translate-btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        openTranslationEditor(btn.dataset.field, 'text');
      });
    });

    return item;
  }

  function renumberItems(type) {
    const container = document.getElementById(type + '-editor');
    if (!container) return;

    const label = type === 'features' ? T.feature : T.step;
    container.querySelectorAll('.json-item').forEach(function (item, idx) {
      item.dataset.index = idx;
      item.querySelector('.item-number').textContent = label + ' #' + (idx + 1);

      item.querySelectorAll('.translate-btn').forEach(function (btn) {
        const currentField = btn.dataset.field;
        if (currentField) {
          const parts = currentField.split('.');
          if (parts.length === 3) {
            btn.dataset.field = type + '.' + idx + '.' + parts[2];
          }
        }
      });
    });
  }

  async function openTranslationEditor(fieldPath) {
    const objectIdMatch = window.location.pathname.match(/\/(\d+)\/change\//);
    if (!objectIdMatch) {
      AdminModal.alert({ message: T.saveBeforeTranslating, type: 'warning' });
      return;
    }
    const objectId = objectIdMatch[1];
    const modelType = 'affiliate.affiliatesettings';

    const parts = fieldPath.split('.');
    let currentValue = '';
    if (parts.length === 3) {
      const type = parts[0];
      const index = parseInt(parts[1]);
      const field = parts[2];
      const container = document.getElementById(type + '-editor');
      if (container) {
        const items = container.querySelectorAll('.json-item');
        if (items[index]) {
          const inputClass = type === 'features' ? 'feature-' + field : 'step-' + field;
          const input = items[index].querySelector('.' + inputClass);
          if (input) currentValue = input.value;
        }
      }
    }

    if (!currentValue) {
      AdminModal.alert({ message: T.enterTextFirst, type: 'warning' });
      return;
    }

    const endpoints = {
      status: '/api/translation/' + modelType + '/' + objectId + '/' + fieldPath + '/status/',
      translate: '/api/translation/' + modelType + '/' + objectId + '/' + fieldPath + '/translate/',
      save: '/api/translation/' + modelType + '/' + objectId + '/' + fieldPath + '/save/',
    };

    let existingTranslations = {};
    let availableLanguages = [];
    let coverage = {};

    try {
      const statusResponse = await fetch(endpoints.status);
      if (statusResponse.ok) {
        const data = await statusResponse.json();
        existingTranslations = data.translations || {};
        availableLanguages = data.available_languages || [];
        coverage = data.coverage || {};
      }
    } catch (error) {
      console.error('Error loading translations:', error);
    }

    if (availableLanguages.length === 0) {
      AdminModal.alert({ message: T.noLanguagesConfigured, type: 'warning' });
      return;
    }

    const fieldLabel = fieldPath
      .replace(/\./g, ' › ')
      .replace(/_/g, ' ')
      .replace(/\b\w/g, function (l) {
        return l.toUpperCase();
      });

    const modal = document.createElement('div');
    modal.className = 'json-translation-modal';
    modal.style.cssText =
      'position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 10000;';

    modal.innerHTML =
      '<div class="json-translation-content" style="background: var(--body-bg, #fff); color: var(--body-fg, #333); border-radius: 8px; max-width: 700px; width: 90%; max-height: 85vh; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.2); display: flex; flex-direction: column;">' +
      '<div class="json-translation-header" style="padding: 16px 20px; border-bottom: 1px solid var(--hairline-color, #ddd); display: flex; justify-content: space-between; align-items: center;">' +
      '<h3 style="margin: 0; font-size: 16px;"><i class="fas fa-globe"></i> ' +
      T.translate +
      ': ' +
      fieldLabel +
      '</h3>' +
      '<button type="button" class="close-modal" style="background: none; border: none; font-size: 20px; cursor: pointer; padding: 0; color: var(--body-fg, #333);"><i class="fas fa-times"></i></button>' +
      '</div>' +
      '<div class="json-translation-body" style="padding: 20px; overflow-y: auto; flex: 1;">' +
      '<div style="margin-bottom: 16px;">' +
      '<label style="font-weight: 600; display: block; margin-bottom: 6px;">' +
      T.sourceText +
      ':</label>' +
      '<div style="padding: 10px; background: var(--darkened-bg, #f5f5f5); border-radius: 4px; font-size: 13px;">' +
      escapeHtml(currentValue) +
      '</div>' +
      '</div>' +
      '<div style="margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center;">' +
      '<label style="font-weight: 600;">' +
      T.targetLanguages +
      ':</label>' +
      '<span style="font-size: 12px; color: var(--body-quiet-color, #666);">' +
      T.coverage +
      ': ' +
      (coverage.percentage || 0) +
      '%</span>' +
      '</div>' +
      '<div class="languages-list" style="display: flex; flex-direction: column; gap: 10px; max-height: 300px; overflow-y: auto;"></div>' +
      '<div class="translation-message" style="margin-top: 12px;"></div>' +
      '</div>' +
      '<div class="json-translation-footer" style="padding: 16px 20px; border-top: 1px solid var(--hairline-color, #ddd); display: flex; justify-content: flex-end; gap: 10px;">' +
      '<button type="button" class="cancel-btn" style="padding: 8px 16px; border: 1px solid var(--hairline-color, #ddd); background: var(--body-bg, #fff); color: var(--body-fg, #333); cursor: pointer; border-radius: 4px;">' +
      T.cancel +
      '</button>' +
      '<button type="button" class="save-btn" style="padding: 8px 16px; border: 1px solid var(--hairline-color, #ddd); background: var(--body-bg, #fff); color: var(--body-fg, #333); cursor: pointer; border-radius: 4px;" disabled><i class="fas fa-save"></i> ' +
      T.saveEdits +
      '</button>' +
      '<button type="button" class="translate-action-btn" style="padding: 8px 16px; border: none; background: var(--primary, #417690); color: white; cursor: pointer; border-radius: 4px;"><i class="fas fa-language"></i> ' +
      T.translate +
      '</button>' +
      '</div>' +
      '</div>';

    document.body.appendChild(modal);

    const languagesList = modal.querySelector('.languages-list');
    const messageEl = modal.querySelector('.translation-message');
    const saveBtn = modal.querySelector('.save-btn');
    const translateBtn = modal.querySelector('.translate-action-btn');

    availableLanguages.forEach(function (lang) {
      const existingTranslation = existingTranslations[lang.code] || '';
      const isTranslated = !!existingTranslation;

      const langItem = document.createElement('div');
      langItem.style.cssText =
        'padding: 10px; border: 1px solid var(--hairline-color, #ddd); border-radius: 4px; background: var(--darkened-bg, #f8f8f8);' +
        (isTranslated ? ' border-left: 3px solid var(--primary, #417690);' : '');
      langItem.innerHTML =
        '<div style="display: flex; align-items: center; gap: 10px; margin-bottom: ' +
        (isTranslated ? '8px' : '0') +
        ';">' +
        '<input type="checkbox" id="lang_' +
        lang.code +
        '" value="' +
        lang.code +
        '" ' +
        (isTranslated ? '' : 'checked') +
        ' style="width: 16px; height: 16px;">' +
        '<label for="lang_' +
        lang.code +
        '" style="flex: 1; margin: 0; font-weight: 500;">' +
        lang.name +
        (isTranslated
          ? ' <span style="color: var(--primary, #417690); margin-left: 6px; font-size: 11px;"><i class="fas fa-check-circle"></i> ' +
            T.translated +
            '</span>'
          : '') +
        '</label>' +
        '</div>' +
        (isTranslated
          ? '<textarea class="translation-edit" data-lang="' +
            lang.code +
            '" data-original="' +
            escapeHtml(existingTranslation) +
            '" style="width: 100%; padding: 8px; border: 1px solid var(--hairline-color, #ddd); border-radius: 4px; font-size: 13px; min-height: 50px; resize: vertical; box-sizing: border-box;">' +
            escapeHtml(existingTranslation) +
            '</textarea>'
          : '');
      languagesList.appendChild(langItem);
    });

    function updateSaveButton() {
      let hasChanges = false;
      languagesList.querySelectorAll('.translation-edit').forEach(function (textarea) {
        if (textarea.value !== textarea.dataset.original) hasChanges = true;
      });
      saveBtn.disabled = !hasChanges;
      saveBtn.style.opacity = hasChanges ? '1' : '0.6';
    }

    languagesList.querySelectorAll('.translation-edit').forEach(function (textarea) {
      textarea.addEventListener('input', updateSaveButton);
    });

    function closeModal() {
      modal.remove();
    }
    modal.querySelector('.close-modal').addEventListener('click', closeModal);
    modal.querySelector('.cancel-btn').addEventListener('click', closeModal);
    modal.addEventListener('click', function (e) {
      if (e.target === modal) closeModal();
    });

    saveBtn.addEventListener('click', async function () {
      const editedTranslations = {};
      languagesList.querySelectorAll('.translation-edit').forEach(function (textarea) {
        const lang = textarea.dataset.lang;
        if (textarea.value.trim() && textarea.value !== textarea.dataset.original) {
          editedTranslations[lang] = textarea.value.trim();
        }
      });
      if (Object.keys(editedTranslations).length === 0) return;

      saveBtn.disabled = true;
      saveBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> ' + T.saving;

      try {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
        const saveResponse = await fetch(endpoints.save, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
          body: JSON.stringify({ translations: editedTranslations }),
        });

        if (!saveResponse.ok) throw new Error(T.saveFailed);

        const result = await saveResponse.json();
        if (result.success) {
          messageEl.innerHTML =
            '<div style="padding: 10px; background: #d4edda; border-radius: 4px; color: #155724;"><i class="fas fa-check-circle"></i> ' +
            T.savedSuccessfully +
            '</div>';
          result.saved_languages.forEach(function (lang) {
            const textarea = languagesList.querySelector(
              '.translation-edit[data-lang="' + lang + '"]'
            );
            if (textarea) textarea.dataset.original = textarea.value;
          });
          updateSaveButton();
        }
      } catch (error) {
        messageEl.innerHTML =
          '<div style="padding: 10px; background: #f8d7da; border-radius: 4px; color: #721c24;"><i class="fas fa-exclamation-triangle"></i> ' +
          error.message +
          '</div>';
      } finally {
        saveBtn.innerHTML = '<i class="fas fa-save"></i> ' + T.saveEdits;
      }
    });

    translateBtn.addEventListener('click', async function () {
      const selectedLanguages = [];
      languagesList.querySelectorAll('input[type="checkbox"]:checked').forEach(function (cb) {
        selectedLanguages.push(cb.value);
      });

      if (selectedLanguages.length === 0) {
        AdminModal.alert({ message: T.selectLanguage, type: 'warning' });
        return;
      }

      translateBtn.disabled = true;
      translateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> ' + T.translating;
      messageEl.innerHTML =
        '<div style="padding: 10px; background: #e7f3ff; border-radius: 4px; color: #004085;"><i class="fas fa-spinner fa-spin"></i> ' +
        T.processingTranslation +
        '</div>';

      try {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
        const transResponse = await fetch(endpoints.translate, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken },
          body: JSON.stringify({
            text: currentValue,
            languages: selectedLanguages,
            force_immediate: true,
          }),
        });

        const transResult = await transResponse.json();
        if (!transResponse.ok) throw new Error(transResult.error || T.translationFailed);

        if (transResult.success) {
          messageEl.innerHTML =
            '<div style="padding: 10px; background: #d4edda; border-radius: 4px; color: #155724;"><i class="fas fa-check-circle"></i> ' +
            T.translatedTo +
            ' ' +
            transResult.successful_languages.length +
            ' ' +
            T.languages +
            '</div>';

          transResult.successful_languages.forEach(function (lang) {
            const existingTextarea = languagesList.querySelector(
              '.translation-edit[data-lang="' + lang + '"]'
            );
            if (existingTextarea) {
              existingTextarea.value = transResult.translations[lang];
              existingTextarea.dataset.original = transResult.translations[lang];
            } else {
              const checkboxEl = languagesList.querySelector('#lang_' + lang);
              const langItem = checkboxEl ? checkboxEl.closest('div[style]') : null;
              if (langItem) {
                const textarea = document.createElement('textarea');
                textarea.className = 'translation-edit';
                textarea.dataset.lang = lang;
                textarea.dataset.original = transResult.translations[lang];
                textarea.value = transResult.translations[lang];
                textarea.style.cssText =
                  'width: 100%; padding: 8px; border: 1px solid var(--hairline-color, #ddd); border-radius: 4px; font-size: 13px; min-height: 50px; resize: vertical; margin-top: 8px; box-sizing: border-box;';
                textarea.addEventListener('input', updateSaveButton);
                langItem.appendChild(textarea);
                langItem.style.borderLeft = '3px solid var(--primary, #417690)';

                const labelEl = langItem.querySelector('label');
                if (labelEl && !labelEl.querySelector('.fa-check-circle')) {
                  labelEl.innerHTML +=
                    ' <span style="color: var(--primary, #417690); margin-left: 6px; font-size: 11px;"><i class="fas fa-check-circle"></i> ' +
                    T.translated +
                    '</span>';
                }
              }
            }
          });
        }
      } catch (error) {
        messageEl.innerHTML =
          '<div style="padding: 10px; background: #f8d7da; border-radius: 4px; color: #721c24;"><i class="fas fa-exclamation-triangle"></i> ' +
          error.message +
          '</div>';
      } finally {
        translateBtn.disabled = false;
        translateBtn.innerHTML = '<i class="fas fa-language"></i> ' + T.translate;
      }
    });
  }

  function updateFeatures() {
    const container = document.getElementById('features-editor');
    if (!container) return;
    const features = [];
    container.querySelectorAll('.json-item').forEach(function (item) {
      features.push({
        icon: item.querySelector('.icon-select').value,
        title: item.querySelector('.feature-title').value,
        description: item.querySelector('.feature-description').value,
      });
    });
    featuresField.value = JSON.stringify(features);
    updatePreviewFeatures(features);
  }

  function updateSteps() {
    const container = document.getElementById('steps-editor');
    if (!container) return;
    const steps = [];
    container.querySelectorAll('.json-item').forEach(function (item) {
      steps.push({
        title: item.querySelector('.step-title').value,
        description: item.querySelector('.step-description').value,
      });
    });
    stepsField.value = JSON.stringify(steps);
    updatePreviewSteps(steps);
  }

  function updatePreviewFeatures(features) {
    let html = '';
    features.forEach(function (f) {
      if (f.title) {
        html +=
          '<div class="preview-feature-card">' +
          '<div class="feature-icon"><i class="' +
          (f.icon || 'fas fa-star') +
          '"></i></div>' +
          '<h3>' +
          escapeHtml(f.title) +
          '</h3>' +
          '<p>' +
          escapeHtml(f.description) +
          '</p>' +
          '</div>';
      }
    });
    previewFeaturesGrid.innerHTML =
      html ||
      '<p style="text-align:center;color:#999;font-size:11px;">' + T.noFeaturesAdded + '</p>';
  }

  function updatePreviewSteps(steps) {
    let html = '';
    const validSteps = steps.filter(function (s) {
      return s.title;
    });
    validSteps.forEach(function (s, idx) {
      if (idx > 0)
        html += '<div class="preview-step-arrow"><i class="fas fa-chevron-right"></i></div>';
      html +=
        '<div class="preview-step">' +
        '<div class="step-number">' +
        (idx + 1) +
        '</div>' +
        '<h4>' +
        escapeHtml(s.title) +
        '</h4>' +
        (s.description ? '<p>' + escapeHtml(s.description) + '</p>' : '') +
        '</div>';
    });
    previewStepsContainer.innerHTML =
      html ||
      '<p style="text-align:center;color:#999;font-size:11px;width:100%;">' +
        T.noStepsAdded +
        '</p>';
  }

  function initFeaturesEditor() {
    if (!featuresField) return;
    const fieldRow = featuresField.closest('.form-row');
    if (!fieldRow) return;

    const editor = document.createElement('div');
    editor.id = 'features-editor';
    editor.className = 'json-items-editor';

    const features = parseJSON(featuresField.value);
    features.forEach(function (f, idx) {
      editor.appendChild(createFeatureItem(f, idx));
    });

    const addBtn = document.createElement('button');
    addBtn.type = 'button';
    addBtn.className = 'add-item-btn';
    addBtn.innerHTML = '<i class="fas fa-plus"></i> ' + T.addFeature;
    addBtn.addEventListener('click', function () {
      const items = editor.querySelectorAll('.json-item');
      editor.insertBefore(
        createFeatureItem({ icon: 'fas fa-star', title: '', description: '' }, items.length),
        addBtn
      );
      updateFeatures();
    });
    editor.appendChild(addBtn);
    fieldRow.appendChild(editor);
    updatePreviewFeatures(features);
  }

  function initStepsEditor() {
    if (!stepsField) return;
    const fieldRow = stepsField.closest('.form-row');
    if (!fieldRow) return;

    const editor = document.createElement('div');
    editor.id = 'steps-editor';
    editor.className = 'json-items-editor';

    const steps = parseJSON(stepsField.value);
    steps.forEach(function (s, idx) {
      editor.appendChild(createStepItem(s, idx));
    });

    const addBtn = document.createElement('button');
    addBtn.type = 'button';
    addBtn.className = 'add-item-btn';
    addBtn.innerHTML = '<i class="fas fa-plus"></i> ' + T.addStep;
    addBtn.addEventListener('click', function () {
      const items = editor.querySelectorAll('.json-item');
      editor.insertBefore(createStepItem({ title: '', description: '' }, items.length), addBtn);
      updateSteps();
    });
    editor.appendChild(addBtn);
    fieldRow.appendChild(editor);
    updatePreviewSteps(steps);
  }

  function setupLivePreview() {
    if (heroTitleField) {
      heroTitleField.addEventListener('input', function () {
        previewHeroTitle.textContent = this.value || T.heroTitleDefault;
      });
    }
    if (heroSubtitleField) {
      heroSubtitleField.addEventListener('input', function () {
        previewHeroSubtitle.textContent = this.value || T.heroSubtitleDefault;
      });
    }
    if (featuresTitleField) {
      featuresTitleField.addEventListener('input', function () {
        previewFeaturesTitle.textContent = this.value || T.featuresTitleDefault;
      });
    }
    if (howItWorksTitleField) {
      howItWorksTitleField.addEventListener('input', function () {
        previewStepsTitle.textContent = this.value || T.howItWorksTitleDefault;
      });
    }
    if (ctaTitleField) {
      ctaTitleField.addEventListener('input', function () {
        previewCtaTitle.textContent = this.value || T.ctaTitleDefault;
      });
    }
    if (ctaDescriptionField) {
      ctaDescriptionField.addEventListener('input', function () {
        previewCtaDescription.textContent = this.value || T.ctaDescriptionDefault;
      });
    }
  }

  function init() {
    if (!document.getElementById('preview-features-grid')) {
      setTimeout(init, 50);
      return;
    }
    initElements();
    initFeaturesEditor();
    initStepsEditor();
    setupLivePreview();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    setTimeout(init, 0);
  }
})();
