/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */
(function () {
  'use strict';

  function readConfig() {
    const el = document.getElementById('restore-config');
    return el ? el.dataset : {};
  }

  document.addEventListener('DOMContentLoaded', function () {
    const config = readConfig();

    // restore_confirm.html: confirmation input gate
    const confirmInput = document.getElementById('confirm-input');
    const restoreBtn = document.getElementById('restore-btn');
    const restoreForm = document.getElementById('restore-form');

    if (confirmInput && restoreBtn) {
      confirmInput.addEventListener('input', function () {
        restoreBtn.disabled = this.value.toUpperCase() !== 'RESTORE';
      });
    }

    if (restoreForm) {
      restoreForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        if (confirmInput && confirmInput.value.toUpperCase() !== 'RESTORE') {
          return false;
        }
        const confirmMsg =
          config.msgConfirmRestore ||
          'Are you absolutely sure you want to restore from this backup? This action cannot be undone.';
        if (
          !(await AdminModal.confirm({ message: confirmMsg, danger: true, confirmText: 'Restore' }))
        ) {
          return false;
        }
        if (restoreBtn) {
          restoreBtn.disabled = true;
          restoreBtn.innerHTML =
            '<i class="fas fa-spinner fa-spin"></i> ' +
            (config.msgStartingRestore || 'Starting Restore...');
        }
        restoreForm.submit();
      });
    }

    // restore_list.html: upload area
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('backup-file');

    if (uploadArea && fileInput) {
      uploadArea.addEventListener('click', function () {
        fileInput.click();
      });
      uploadArea.addEventListener('dragover', function (e) {
        e.preventDefault();
        uploadArea.classList.add('dragover');
      });
      uploadArea.addEventListener('dragleave', function () {
        uploadArea.classList.remove('dragover');
      });
      uploadArea.addEventListener('drop', function (e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        if (e.dataTransfer.files.length) {
          fileInput.files = e.dataTransfer.files;
          handleUpload();
        }
      });
      fileInput.addEventListener('change', handleUpload);
    }

    async function handleUpload() {
      if (!fileInput.files.length) return;
      const file = fileInput.files[0];
      const confirmMsg = (config.msgUploadConfirm || 'Upload backup file') + ': ' + file.name + '?';
      if (!(await AdminModal.confirm(confirmMsg))) {
        fileInput.value = '';
        return;
      }
      const formData = new FormData();
      formData.append('backup_file', file);
      formData.append('csrfmiddlewaretoken', AdminUtils.getCsrfToken());
      uploadArea.innerHTML =
        '<i class="fas fa-spinner fa-spin"></i><p>' +
        (config.msgUploading || 'Uploading...') +
        '</p>';
      fetch(config.uploadUrl || window.location.href, { method: 'POST', body: formData })
        .then(function (r) {
          return r.json();
        })
        .then(function (data) {
          if (data.success) {
            location.reload();
          } else {
            AdminModal.alert({
              message:
                (config.msgUploadFailed || 'Upload failed') +
                ': ' +
                (data.error || config.msgUnknown || 'Unknown error'),
              type: 'error',
            });
            location.reload();
          }
        })
        .catch(function (error) {
          console.error('Error:', error);
          AdminModal.alert({ message: config.msgUploadFailed || 'Upload failed', type: 'error' });
          location.reload();
        });
    }
  });
})();
