---
template_type: digital_product_license_key
category: Digital Products
---

# Email Template: digital_product_license_key

## Subject
Kunci Lisensi Perangkat Lunak Anda - Pesanan #{{ order_number }}

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
    <mj-section background-color="#059669" padding="20px">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          Kunci Lisensi Anda Siap Digunakan
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
          Terima kasih telah membeli {{ product_name }}! Berikut adalah kunci lisensi Anda untuk aktivasi.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Key Box -->
    <mj-section background-color="#f0fdf4" padding="30px" border="2px solid #059669" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          KUNCI LISENSI ANDA
        </mj-text>
        <mj-text font-size="20px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0">
          {{ license_key }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Klik untuk menyalin atau tulis dengan hati-hati
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Details -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" font-weight="bold">
          Detail Lisensi:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Produk: {{ product_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Versi: {{ product_version }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Jenis Lisensi: {{ license_type }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Maksimal Aktivasi: {{ max_activations }} perangkat
        </mj-text>
        {% if is_lifetime %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Validitas: Lisensi Seumur Hidup
        </mj-text>
        {% else %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Valid Sampai: {{ expiration_date }}
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Activation Instructions -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold">
          Cara Mengaktifkan:
        </mj-text>
        <mj-text font-size="14px">
          1. Unduh dan instal perangkat lunak
        </mj-text>
        <mj-text font-size="14px">
          2. Buka aplikasi
        </mj-text>
        <mj-text font-size="14px">
          3. Masukkan kunci lisensi Anda saat diminta
        </mj-text>
        <mj-text font-size="14px">
          4. Klik "Aktifkan" untuk menyelesaikan proses
        </mj-text>
      </mj-column>
    </mj-section>

    {% if download_url %}
    <!-- Download Button -->
    <mj-section>
      <mj-column>
        <mj-button href="{{ download_url }}" background-color="#059669" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" padding="15px 30px" border-radius="6px">
          Unduh Perangkat Lunak
        </mj-button>
      </mj-column>
    </mj-section>
    {% endif %}

    <!-- Important Notice -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.error|default:'#ef4444' }}" font-weight="bold">
          ⚠️ Penting:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Simpan email ini dengan aman - Anda membutuhkan kunci lisensi untuk penginstalan ulang
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Jangan bagikan kunci lisensi Anda dengan orang lain
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          • Anda dapat menonaktifkan perangkat dari dashboard akun Anda
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    <mj-section>
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Membutuhkan bantuan untuk aktivasi? Hubungi {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Kunci Lisensi Anda Siap Digunakan

Hai {{ customer_name }},

Terima kasih telah membeli {{ product_name }}! Berikut adalah kunci lisensi Anda untuk aktivasi.

KUNCI LISENSI ANDA:
{{ license_key }}

Detail Lisensi:
• Produk: {{ product_name }}
• Versi: {{ product_version }}
• Jenis Lisensi: {{ license_type }}
• Maksimal Aktivasi: {{ max_activations }} perangkat
{% if is_lifetime %}• Validitas: Lisensi Seumur Hidup{% else %}• Valid Sampai: {{ expiration_date }}{% endif %}

Cara Mengaktifkan:
1. Unduh dan instal perangkat lunak
2. Buka aplikasi
3. Masukkan kunci lisensi Anda saat diminta
4. Klik "Aktifkan" untuk menyelesaikan proses

{% if download_url %}Unduh Perangkat Lunak: {{ download_url }}

{% endif %}PENTING:
• Simpan email ini dengan aman - Anda membutuhkan kunci lisensi untuk penginstalan ulang
• Jangan bagikan kunci lisensi Anda dengan orang lain
• Anda dapat menonaktifkan perangkat dari dashboard akun Anda

Membutuhkan bantuan untuk aktivasi? Hubungi {{ support_email }}