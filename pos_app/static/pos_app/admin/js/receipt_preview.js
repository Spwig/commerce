/* Copyright (c) 2025-2026 Spwig contributors. Licensed under AGPL-3.0. */

/**
 * Receipt Template Admin — Live Preview
 * Updates the receipt mockup in real-time as admin form fields change.
 */
(function () {
  'use strict';

  // Wait for DOM
  document.addEventListener('DOMContentLoaded', function () {
    const preview = document.getElementById('receipt-preview');
    if (!preview) return;

    // Field selectors
    const fields = {
      name: '#id_name',
      paperWidth: '#id_paper_width',
      headerText: '#id_header_text',
      showAddress: '#id_show_store_address',
      customAddress: '#id_custom_address',
      showPhone: '#id_show_store_phone',
      customPhone: '#id_custom_phone',
      showEmail: '#id_show_store_email',
      customEmail: '#id_custom_email',
      taxIdLabel: '#id_tax_id_label',
      taxIdNumber: '#id_tax_id_number',
      businessReg: '#id_business_registration',
      showSku: '#id_show_sku',
      showCashier: '#id_show_cashier',
      showTerminal: '#id_show_terminal_name',
      footerText: '#id_footer_text',
      returnPolicy: '#id_return_policy',
      qrEnabled: '#id_qr_enabled',
      qrUrl: '#id_qr_url',
      qrLabel: '#id_qr_label',
      showPoweredBy: '#id_show_powered_by',
    };

    // Preview element references
    const el = {
      mockup: preview.querySelector('.receipt-mockup'),
      logo: preview.querySelector('.receipt-logo'),
      storeName: preview.querySelector('.receipt-store-name'),
      address: preview.querySelector('.receipt-store-address'),
      phone: preview.querySelector('.receipt-store-phone'),
      email: preview.querySelector('.receipt-store-email'),
      businessInfo: preview.querySelector('.receipt-business-info'),
      cashier: preview.querySelector('.receipt-meta-cashier'),
      terminal: preview.querySelector('.receipt-meta-terminal'),
      skuLines: preview.querySelectorAll('.receipt-item-sku'),
      footer: preview.querySelector('.receipt-footer-text'),
      returnPolicy: preview.querySelector('.receipt-return-policy'),
      qrSection: preview.querySelector('.receipt-qr-section'),
      qrLabel: preview.querySelector('.receipt-qr-label'),
      branding: preview.querySelector('.receipt-branding'),
    };

    // Warehouse defaults (injected from template context)
    const defaults = {
      storeName: preview.dataset.warehouseName || 'Your Store',
      address: preview.dataset.warehouseAddress || '123 Main Street, City',
      phone: preview.dataset.warehousePhone || '+1 555-0123',
      email: preview.dataset.warehouseEmail || 'store@example.com',
    };

    function getVal(selector) {
      const field = document.querySelector(selector);
      if (!field) return '';
      if (field.type === 'checkbox') return field.checked;
      return field.value || '';
    }

    function updatePreview() {
      // Paper width
      const pw = getVal(fields.paperWidth);
      el.mockup.classList.toggle('paper-58', pw === '58');

      // Store name
      const headerText = getVal(fields.headerText);
      el.storeName.textContent = headerText || defaults.storeName;

      // Address
      const showAddr = getVal(fields.showAddress);
      const customAddr = getVal(fields.customAddress);
      el.address.textContent = customAddr || defaults.address;
      el.address.classList.toggle('receipt-hidden', !showAddr);

      // Phone
      const showPhone = getVal(fields.showPhone);
      const customPhone = getVal(fields.customPhone);
      el.phone.textContent = customPhone || defaults.phone;
      el.phone.classList.toggle('receipt-hidden', !showPhone);

      // Email
      const showEmail = getVal(fields.showEmail);
      const customEmail = getVal(fields.customEmail);
      el.email.textContent = customEmail || defaults.email;
      el.email.classList.toggle('receipt-hidden', !showEmail);

      // Business details
      const taxLabel = getVal(fields.taxIdLabel);
      const taxNumber = getVal(fields.taxIdNumber);
      const bizReg = getVal(fields.businessReg);
      const bizParts = [];
      if (taxLabel && taxNumber) bizParts.push(taxLabel + ': ' + taxNumber);
      else if (taxNumber) bizParts.push('Tax ID: ' + taxNumber);
      if (bizReg) bizParts.push('Reg: ' + bizReg);
      el.businessInfo.textContent = bizParts.join(' | ');
      el.businessInfo.classList.toggle('receipt-hidden', bizParts.length === 0);

      // Cashier
      const showCashier = getVal(fields.showCashier);
      el.cashier.classList.toggle('receipt-hidden', !showCashier);

      // Terminal
      const showTerminal = getVal(fields.showTerminal);
      el.terminal.classList.toggle('receipt-hidden', !showTerminal);

      // SKU
      const showSku = getVal(fields.showSku);
      el.skuLines.forEach(function (s) {
        s.classList.toggle('receipt-hidden', !showSku);
      });

      // Footer
      const footerText = getVal(fields.footerText);
      el.footer.textContent = footerText || '';
      el.footer.classList.toggle('receipt-hidden', !footerText);

      // Return policy
      const returnPolicy = getVal(fields.returnPolicy);
      el.returnPolicy.textContent = returnPolicy || '';
      el.returnPolicy.classList.toggle('receipt-hidden', !returnPolicy);

      // QR code
      const qrEnabled = getVal(fields.qrEnabled);
      const qrLabel = getVal(fields.qrLabel);
      el.qrSection.classList.toggle('receipt-hidden', !qrEnabled);
      el.qrLabel.textContent = qrLabel || '';

      // Branding
      const showBranding = getVal(fields.showPoweredBy);
      el.branding.classList.toggle('receipt-hidden', !showBranding);
    }

    // Logo preview — watch for media library widget changes
    function updateLogoPreview() {
      // The media library widget stores the selected asset ID in a hidden input
      const logoInput = document.querySelector('#id_logo');
      const logoPreview = preview.querySelector('.receipt-logo');
      if (!logoInput) return;

      // Check if there's a thumbnail preview in the widget
      const widgetContainer = logoInput.closest('.field-logo, .form-row');
      if (widgetContainer) {
        const thumb = widgetContainer.querySelector('.media-library-preview img, .ml-preview img');
        if (thumb && thumb.src) {
          logoPreview.innerHTML = '<img src="' + thumb.src + '" alt="Logo">';
          logoPreview.classList.remove('receipt-hidden');
          return;
        }
      }

      // No logo selected
      if (logoInput.value) {
        logoPreview.classList.remove('receipt-hidden');
      } else {
        logoPreview.classList.add('receipt-hidden');
      }
    }

    // Bind events to all form fields
    Object.values(fields).forEach(function (selector) {
      const field = document.querySelector(selector);
      if (field) {
        field.addEventListener('input', updatePreview);
        field.addEventListener('change', updatePreview);
      }
    });

    // Watch logo field changes
    const logoField = document.querySelector('#id_logo');
    if (logoField) {
      const observer = new MutationObserver(updateLogoPreview);
      const logoContainer = logoField.closest('.field-logo, .form-row');
      if (logoContainer) {
        observer.observe(logoContainer, { childList: true, subtree: true, attributes: true });
      }
      logoField.addEventListener('change', updateLogoPreview);
    }

    // Initial render
    updatePreview();
    updateLogoPreview();
  });
})();
