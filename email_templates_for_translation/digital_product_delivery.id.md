---
template_type: digital_product_delivery
category: Digital Products
---

# Email Template: digital_product_delivery

## Subject
Produk Digital Anda Siap - Pesanan #{{ order_number }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          Produk Digital Anda Siap!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Main Content -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Hai {{ customer_name }},
        </mj-text>
        <mj-text>
          Terima kasih atas pembelian Anda! Produk digital Anda sekarang siap untuk diunduh.
        </mj-text>
        <mj-text font-weight="bold">
          Pesanan #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Product Details -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          {{ product_name }}
        </mj-text>
        <mj-text color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Versi: {{ product_version }}
        </mj-text>
        <mj-text color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Ukuran File: {{ file_size }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Download Button -->
    <mj-section>
      <mj-column>
        <mj-button href="{{ download_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          Unduh Sekarang
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Important Information -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          <strong>Informasi Penting:</strong>
        </mj-text>
        {% if download_limit %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Anda dapat mengunduh produk ini {{ download_limit }} kali
        </mj-text>
        {% endif %}
        {% if expiration_days %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Tautan unduh akan kedaluwarsa dalam {{ expiration_days }} hari
        </mj-text>
        {% endif %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Simpan email ini untuk referensi di masa depan
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Membutuhkan bantuan? Hubungi tim dukungan kami di {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Produk Digital Anda Siap!

Hai {{ customer_name }},

Terima kasih atas pembelian Anda! Produk digital Anda sekarang siap untuk diunduh.

Pesanan #{{ order_number }}

Produk: {{ product_name }}
Versi: {{ product_version }}
Ukuran File: {{ file_size }}

Unduh produk Anda di sini:
{{ download_url }}

Informasi Penting:
{% if download_limit %}• Anda dapat mengunduh produk ini {{ download_limit }} kali
{% endif %}{% if expiration_days %}• Tautan unduh akan kedaluwarsa dalam {{ expiration_days }} hari
{% endif %}• Simpan email ini untuk referensi di masa depan

Membutuhkan bantuan? Hubungi tim dukungan kami di {{ support_email }}