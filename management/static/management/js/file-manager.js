/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */
(function () {
  'use strict';

  let selectedFile = null;

  function readConfig() {
    const el = document.getElementById('file-manager-config');
    return el ? el.dataset : {};
  }

  function showUploadModal() {
    document.getElementById('uploadModal').classList.add('active');
    document.body.classList.add('admin-modal-body-locked');
  }

  function closeUploadModal() {
    document.getElementById('uploadModal').classList.remove('active');
    document.body.classList.remove('admin-modal-body-locked');
    document.getElementById('uploadForm').reset();
    document.getElementById('selectedFile').classList.add('mgmt-hidden');
    document.getElementById('progressBar').classList.add('mgmt-hidden');
    selectedFile = null;
  }

  function refreshFileList() {
    location.reload();
  }

  async function createFolder() {
    const name = await AdminModal.prompt('Enter folder name:');
    if (name) {
      AdminModal.alert('Folder creation not implemented yet');
    }
  }

  function handleFileSelect(files) {
    if (files.length > 0) {
      selectedFile = files[0];
      document.getElementById('fileName').textContent = selectedFile.name;
      document.getElementById('selectedFile').classList.remove('mgmt-hidden');
    }
  }

  function uploadFile() {
    if (!selectedFile) {
      AdminModal.alert({ message: 'Please select a file first', type: 'warning' });
      return;
    }
    const config = readConfig();
    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('path', config.currentPath || '');
    formData.append('csrfmiddlewaretoken', AdminUtils.getCsrfToken());
    const uploadBtn = document.getElementById('uploadBtn');
    const progressBar = document.getElementById('progressBar');
    uploadBtn.disabled = true;
    progressBar.classList.remove('mgmt-hidden');
    fetch(config.uploadUrl, { method: 'POST', body: formData })
      .then(function (r) {
        return r.json();
      })
      .then(function (data) {
        uploadBtn.disabled = false;
        progressBar.classList.add('mgmt-hidden');
        if (data.success) {
          showMessage('File uploaded successfully!', 'success');
          closeUploadModal();
          setTimeout(refreshFileList, 1000);
        } else {
          showMessage('Upload failed: ' + data.error, 'error');
        }
      })
      .catch(function (error) {
        uploadBtn.disabled = false;
        progressBar.classList.add('mgmt-hidden');
        showMessage('Upload failed: ' + error, 'error');
      });
  }

  async function deleteFile(filePath, fileName) {
    if (
      !(await AdminModal.confirm({
        message: 'Are you sure you want to delete ' + JSON.stringify(fileName) + '?',
        danger: true,
        confirmText: 'Delete',
      }))
    )
      return;
    const config = readConfig();
    fetch(config.deleteUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-CSRFToken': AdminUtils.getCsrfToken(),
      },
      body: 'file_path=' + encodeURIComponent(filePath),
    })
      .then(function (r) {
        return r.json();
      })
      .then(function (data) {
        if (data.success) {
          showMessage('File deleted successfully!', 'success');
          setTimeout(refreshFileList, 1000);
        } else {
          showMessage('Delete failed: ' + data.error, 'error');
        }
      })
      .catch(function (error) {
        showMessage('Delete failed: ' + error, 'error');
      });
  }

  function showMessage(message, type) {
    const container = document.getElementById('messages-container');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message ' + type;
    messageDiv.textContent = message;
    container.appendChild(messageDiv);
    setTimeout(function () {
      if (container.contains(messageDiv)) container.removeChild(messageDiv);
    }, 5000);
  }

  document.addEventListener('click', function (e) {
    const el = e.target.closest('[data-action]');
    if (el) {
      switch (el.dataset.action) {
        case 'show-upload-modal':
          showUploadModal();
          break;
        case 'close-upload-modal':
          closeUploadModal();
          break;
        case 'refresh-file-list':
          refreshFileList();
          break;
        case 'create-folder':
          createFolder();
          break;
        case 'upload-file':
          uploadFile();
          break;
        case 'delete-file':
          deleteFile(el.dataset.path, el.dataset.name);
          break;
      }
      return;
    }
    const modal = document.getElementById('uploadModal');
    if (e.target === modal) {
      closeUploadModal();
    }
  });

  document.addEventListener('DOMContentLoaded', function () {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    if (uploadArea && fileInput) {
      uploadArea.addEventListener('click', function () {
        fileInput.click();
      });
      uploadArea.addEventListener('dragover', function (e) {
        e.preventDefault();
        uploadArea.classList.add('dragover');
      });
      uploadArea.addEventListener('dragleave', function (e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
      });
      uploadArea.addEventListener('drop', function (e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        handleFileSelect(e.dataTransfer.files);
      });
      fileInput.addEventListener('change', function () {
        handleFileSelect(this.files);
      });
    }
  });
})();
