/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  function init() {
    const dataEl = document.getElementById('wizard-step4-data');
    if (!dataEl) {
      return;
    }

    let config;
    try {
      config = JSON.parse(dataEl.textContent);
    } catch (e) {
      return;
    }

    const t = config.translations || {};
    const urls = config.urls || {};
    const capLabels = t.capabilities || {};

    const testBtn = document.getElementById('test-connection-btn');
    const testStatus = document.getElementById('test-status');
    const testButtonContainer = document.getElementById('test-button-container');
    const testConnectionArea = document.querySelector('.test-connection-area');
    const testResults = document.getElementById('test-results');
    const saveBtn = document.getElementById('save-btn');
    const testResultTitle = document.getElementById('test-result-title');
    const testResultMessage = document.getElementById('test-result-message');
    const testDetails = document.getElementById('test-details');
    const testDetailsBody = document.getElementById('test-details-body');
    const testResultIcon = testResults ? testResults.querySelector('.test-result-icon i') : null;
    const capabilitiesPreview = document.getElementById('capabilities-preview');
    const capabilitiesGrid = document.getElementById('capabilities-grid');

    if (!testBtn) {
      console.error('Test button not found!');
      return;
    }

    const capabilityIcons = {
      text_posts: 'fa-font',
      image_posts: 'fa-image',
      video_posts: 'fa-video',
      link_preview: 'fa-link',
      scheduling: 'fa-clock',
      hashtags: 'fa-hashtag',
      mentions: 'fa-at',
      carousel_posts: 'fa-images',
      stories: 'fa-circle',
      token_refresh: 'fa-sync',
    };

    const capabilityLabelKeys = {
      text_posts: 'textPosts',
      image_posts: 'imagePosts',
      video_posts: 'videoPosts',
      link_preview: 'linkPreviews',
      scheduling: 'scheduling',
      hashtags: 'hashtags',
      mentions: 'mentions',
      carousel_posts: 'carouselPosts',
      stories: 'stories',
      token_refresh: 'tokenRefresh',
    };

    testBtn.addEventListener('click', function () {
      testButtonContainer.style.display = 'none';
      testStatus.style.display = 'flex';
      testResults.style.display = 'none';
      capabilitiesPreview.style.display = 'none';
      saveBtn.style.display = 'none';

      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
      const formData = new FormData();
      formData.append('action', 'test');
      if (csrfToken) {
        formData.append('csrfmiddlewaretoken', csrfToken.value);
      }

      fetch(urls.wizardStep4 || '', { method: 'POST', body: formData })
        .then(function (response) {
          return response.json();
        })
        .then(function (result) {
          testStatus.style.display = 'none';
          testConnectionArea.style.display = 'none';
          testResults.style.display = 'block';

          if (result.success) {
            testResultIcon.className = 'fas fa-check-circle';
            testResults.className = 'test-results success';
            testResultTitle.textContent = t.connectionSuccessful || 'Connection Successful!';
            testResultMessage.textContent =
              result.message ||
              t.credentialsVerified ||
              'Your credentials were verified successfully.';

            if (result.details) {
              testDetails.style.display = 'block';
              testDetailsBody.innerHTML = '';
              Object.entries(result.details).forEach(function (entry) {
                const row = document.createElement('tr');
                const th = document.createElement('th');
                const td = document.createElement('td');
                th.textContent = entry[0];
                td.textContent = entry[1];
                row.appendChild(th);
                row.appendChild(td);
                testDetailsBody.appendChild(row);
              });
            }

            if (result.capabilities && capabilitiesPreview && capabilitiesGrid) {
              capabilitiesPreview.style.display = 'block';
              capabilitiesGrid.innerHTML = '';
              Object.entries(result.capabilities).forEach(function (entry) {
                const cap = entry[0];
                const enabled = entry[1];
                if (!capabilityIcons[cap]) {
                  return;
                }
                const labelKey = capabilityLabelKeys[cap];
                const label = (capLabels && capLabels[labelKey]) || cap;
                const item = document.createElement('div');
                item.className = 'capability-item ' + (enabled ? 'enabled' : 'disabled');
                const icon1 = document.createElement('i');
                icon1.className = 'fas ' + capabilityIcons[cap];
                const span = document.createElement('span');
                span.textContent = label;
                const icon2 = document.createElement('i');
                icon2.className =
                  'fas ' + (enabled ? 'fa-check-circle status-ok' : 'fa-times-circle status-na');
                item.appendChild(icon1);
                item.appendChild(span);
                item.appendChild(icon2);
                capabilitiesGrid.appendChild(item);
              });
            }

            saveBtn.style.display = 'inline-block';
          } else {
            testResultIcon.className = 'fas fa-times-circle';
            testResults.className = 'test-results error';
            testResultTitle.textContent = t.connectionFailed || 'Connection Failed';
            testResultMessage.textContent =
              result.error ||
              result.message ||
              t.couldNotConnect ||
              'Could not connect to the social platform.';
            testConnectionArea.style.display = 'block';
            testButtonContainer.style.display = 'block';
          }
        })
        .catch(function (error) {
          testStatus.style.display = 'none';
          testConnectionArea.style.display = 'none';
          testResults.style.display = 'block';
          testResultIcon.className = 'fas fa-exclamation-triangle';
          testResults.className = 'test-results error';
          testResultTitle.textContent = t.error || 'Error';
          testResultMessage.textContent =
            error.message || t.unexpectedError || 'An unexpected error occurred.';
          testConnectionArea.style.display = 'block';
          testButtonContainer.style.display = 'block';
        });
    });

    if (saveBtn) {
      saveBtn.addEventListener('click', function () {
        saveBtn.disabled = true;
        const spinner = document.createElement('i');
        spinner.className = 'fas fa-spinner fa-spin';
        saveBtn.innerHTML = '';
        saveBtn.appendChild(spinner);
        saveBtn.appendChild(document.createTextNode(' ' + (t.saving || 'Saving...')));

        const formData = new FormData();
        formData.append('action', 'save');
        const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
        if (csrfInput) {
          formData.append('csrfmiddlewaretoken', csrfInput.value);
        }

        fetch(urls.wizardStep4 || '', { method: 'POST', body: formData })
          .then(function (response) {
            return response.json();
          })
          .then(function (result) {
            if (result.success) {
              window.location.href = urls.accountChangelist || '';
            } else {
              AdminModal.alert({
                message:
                  result.error || t.failedToSave || 'Failed to save social connector account.',
                type: 'error',
              });
              saveBtn.disabled = false;
              const saveIcon = document.createElement('i');
              saveIcon.className = 'fas fa-save';
              saveBtn.innerHTML = '';
              saveBtn.appendChild(saveIcon);
              saveBtn.appendChild(
                document.createTextNode(' ' + (t.saveAndFinish || 'Save & Finish'))
              );
            }
          })
          .catch(function (error) {
            AdminModal.alert({
              message: error.message || t.anErrorOccurred || 'An error occurred while saving.',
              type: 'error',
            });
            saveBtn.disabled = false;
            const saveIcon = document.createElement('i');
            saveIcon.className = 'fas fa-save';
            saveBtn.innerHTML = '';
            saveBtn.appendChild(saveIcon);
            saveBtn.appendChild(
              document.createTextNode(' ' + (t.saveAndFinish || 'Save & Finish'))
            );
          });
      });
    }
  }

  document.addEventListener('DOMContentLoaded', init);
})();
