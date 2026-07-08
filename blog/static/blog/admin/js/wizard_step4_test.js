/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
    'use strict';

    function init() {
        var dataEl = document.getElementById('wizard-step4-data');
        if (!dataEl) { return; }

        var config;
        try { config = JSON.parse(dataEl.textContent); } catch (e) { return; }

        var t = config.translations || {};
        var urls = config.urls || {};
        var capLabels = t.capabilities || {};

        var testBtn = document.getElementById('test-connection-btn');
        var testStatus = document.getElementById('test-status');
        var testButtonContainer = document.getElementById('test-button-container');
        var testConnectionArea = document.querySelector('.test-connection-area');
        var testResults = document.getElementById('test-results');
        var saveBtn = document.getElementById('save-btn');
        var testResultTitle = document.getElementById('test-result-title');
        var testResultMessage = document.getElementById('test-result-message');
        var testDetails = document.getElementById('test-details');
        var testDetailsBody = document.getElementById('test-details-body');
        var testResultIcon = testResults ? testResults.querySelector('.test-result-icon i') : null;
        var capabilitiesPreview = document.getElementById('capabilities-preview');
        var capabilitiesGrid = document.getElementById('capabilities-grid');

        if (!testBtn) {
            console.error('Test button not found!');
            return;
        }

        var capabilityIcons = {
            'text_posts': 'fa-font',
            'image_posts': 'fa-image',
            'video_posts': 'fa-video',
            'link_preview': 'fa-link',
            'scheduling': 'fa-clock',
            'hashtags': 'fa-hashtag',
            'mentions': 'fa-at',
            'carousel_posts': 'fa-images',
            'stories': 'fa-circle',
            'token_refresh': 'fa-sync'
        };

        var capabilityLabelKeys = {
            'text_posts': 'textPosts',
            'image_posts': 'imagePosts',
            'video_posts': 'videoPosts',
            'link_preview': 'linkPreviews',
            'scheduling': 'scheduling',
            'hashtags': 'hashtags',
            'mentions': 'mentions',
            'carousel_posts': 'carouselPosts',
            'stories': 'stories',
            'token_refresh': 'tokenRefresh'
        };

        testBtn.addEventListener('click', function () {
            testButtonContainer.style.display = 'none';
            testStatus.style.display = 'flex';
            testResults.style.display = 'none';
            capabilitiesPreview.style.display = 'none';
            saveBtn.style.display = 'none';

            var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
            var formData = new FormData();
            formData.append('action', 'test');
            if (csrfToken) { formData.append('csrfmiddlewaretoken', csrfToken.value); }

            fetch(urls.wizardStep4 || '', { method: 'POST', body: formData })
                .then(function (response) { return response.json(); })
                .then(function (result) {
                    testStatus.style.display = 'none';
                    testConnectionArea.style.display = 'none';
                    testResults.style.display = 'block';

                    if (result.success) {
                        testResultIcon.className = 'fas fa-check-circle';
                        testResults.className = 'test-results success';
                        testResultTitle.textContent = t.connectionSuccessful || 'Connection Successful!';
                        testResultMessage.textContent = result.message || (t.credentialsVerified || 'Your credentials were verified successfully.');

                        if (result.details) {
                            testDetails.style.display = 'block';
                            testDetailsBody.innerHTML = '';
                            Object.entries(result.details).forEach(function (entry) {
                                var row = document.createElement('tr');
                                var th = document.createElement('th');
                                var td = document.createElement('td');
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
                                var cap = entry[0];
                                var enabled = entry[1];
                                if (!capabilityIcons[cap]) { return; }
                                var labelKey = capabilityLabelKeys[cap];
                                var label = (capLabels && capLabels[labelKey]) || cap;
                                var item = document.createElement('div');
                                item.className = 'capability-item ' + (enabled ? 'enabled' : 'disabled');
                                var icon1 = document.createElement('i');
                                icon1.className = 'fas ' + capabilityIcons[cap];
                                var span = document.createElement('span');
                                span.textContent = label;
                                var icon2 = document.createElement('i');
                                icon2.className = 'fas ' + (enabled ? 'fa-check-circle status-ok' : 'fa-times-circle status-na');
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
                        testResultMessage.textContent = result.error || result.message || (t.couldNotConnect || 'Could not connect to the social platform.');
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
                    testResultMessage.textContent = error.message || (t.unexpectedError || 'An unexpected error occurred.');
                    testConnectionArea.style.display = 'block';
                    testButtonContainer.style.display = 'block';
                });
        });

        if (saveBtn) {
            saveBtn.addEventListener('click', function () {
                saveBtn.disabled = true;
                var spinner = document.createElement('i');
                spinner.className = 'fas fa-spinner fa-spin';
                saveBtn.innerHTML = '';
                saveBtn.appendChild(spinner);
                saveBtn.appendChild(document.createTextNode(' ' + (t.saving || 'Saving...')));

                var formData = new FormData();
                formData.append('action', 'save');
                var csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
                if (csrfInput) { formData.append('csrfmiddlewaretoken', csrfInput.value); }

                fetch(urls.wizardStep4 || '', { method: 'POST', body: formData })
                    .then(function (response) { return response.json(); })
                    .then(function (result) {
                        if (result.success) {
                            window.location.href = urls.accountChangelist || '';
                        } else {
                            AdminModal.alert({message: result.error || (t.failedToSave || 'Failed to save social connector account.'), type: 'error'});
                            saveBtn.disabled = false;
                            var saveIcon = document.createElement('i');
                            saveIcon.className = 'fas fa-save';
                            saveBtn.innerHTML = '';
                            saveBtn.appendChild(saveIcon);
                            saveBtn.appendChild(document.createTextNode(' ' + (t.saveAndFinish || 'Save & Finish')));
                        }
                    })
                    .catch(function (error) {
                        AdminModal.alert({message: error.message || (t.anErrorOccurred || 'An error occurred while saving.'), type: 'error'});
                        saveBtn.disabled = false;
                        var saveIcon = document.createElement('i');
                        saveIcon.className = 'fas fa-save';
                        saveBtn.innerHTML = '';
                        saveBtn.appendChild(saveIcon);
                        saveBtn.appendChild(document.createTextNode(' ' + (t.saveAndFinish || 'Save & Finish')));
                    });
            });
        }
    }

    document.addEventListener('DOMContentLoaded', init);
}());
