/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.btn-sync').forEach(function (btn) {
      btn.addEventListener('click', function () {
        const accountId = this.dataset.accountId;
        const icon = this.querySelector('i');
        const self = this;

        icon.classList.add('fa-spin');
        self.disabled = true;

        fetch(AdminUtils.buildAdminUrl('/admin/product-feeds/admin/' + accountId + '/sync/'), {
          method: 'POST',
          headers: {
            'X-CSRFToken': AdminUtils.getCsrfToken(),
            'Content-Type': 'application/json',
          },
        })
          .then(function (response) {
            return response.json();
          })
          .then(function (data) {
            if (data.success) {
              window.location.reload();
            } else {
              AdminModal.alert({
                message: 'Sync failed: ' + (data.error || 'Unknown error'),
                type: 'error',
              });
              icon.classList.remove('fa-spin');
              self.disabled = false;
            }
          })
          .catch(function (error) {
            console.error('Error:', error);
            icon.classList.remove('fa-spin');
            self.disabled = false;
          });
      });
    });
  });
})();
