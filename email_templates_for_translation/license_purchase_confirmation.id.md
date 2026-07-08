---
template_type: license_purchase_confirmation
category: License
---

# Email Template: license_purchase_confirmation

## Subject
Lisensi Spwig Anda - Pesanan #{{ order_number }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Terima kasih atas pembelian Anda!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Pesanan #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Hai {{ customer_name }},
        </mj-text>
        <mj-text>
          Pembelian Anda atas <strong>{{ product_name }}</strong> telah selesai. Di bawah ini Anda akan menemukan kunci lisensi dan token pengaturan untuk memulai.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Order Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Ringkasan Pesanan
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Produk: {{ product_name }}{% if includes_pos %} (termasuk POS){% endif %}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Jumlah: {{ price }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Nomor Pesanan: {{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- License Key Box -->
    <mj-section background-color="#eff6ff" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#1e40af" font-weight="bold" align="center">
          KUNCI LISENSI ANDA
        </mj-text>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" align="center" font-family="'Courier New', monospace" padding="10px 0">
          {{ license_key }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Simpan kunci ini - Anda membutuhkannya untuk penginstalan ulang
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Token Box -->
    <mj-section background-color="#f0fdf4" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          TOKEN PENGATURAN ANDA
        </mj-text>
        <mj-text font-size="14px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0" word-break="break-all">
          {{ setup_token }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Gunakan token ini saat penginstalan untuk mengaktifkan toko Anda
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Memulai
        </mj-text>
        <mj-text font-size="14px">
          1. Ikuti panduan pengaturan kami untuk menginstal Spwig di server Anda
        </mj-text>
        <mj-text font-size="14px">
          2. Masukkan token pengaturan Anda saat diminta selama penginstalan
        </mj-text>
        <mj-text font-size="14px">
          3. Toko Anda akan diaktifkan secara otomatis
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Guide CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=setup_url text="Lihat Panduan Pengaturan" %}

    {% if activation_url %}
    <!-- Guest Account Activation -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px 20px 10px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Buat Akun Anda
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="5px">
          Tetapkan kata sandi untuk mengelola lisensi Anda, mengakses unduhan, dan menerima pembaruan.
        </mj-text>
      </mj-column>
    </mj-section>
    {% include 'email_system/mjml_components/cta_button.mjml' with url=activation_url text="Buat Akun Anda" %}
    {% endif %}

    <!-- Important Notice -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.warning|default:'#d97706' }}" font-weight="bold">
          Penting:
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Simpan email ini dengan aman - email ini berisi kunci lisensi dan token pengaturan Anda untuk referensi di masa depan. Jangan bagikan kredensial ini dengan orang lain.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Terima kasih atas pembelian Anda!

Pesanan #{{ order_number }}

Hai {{ customer_name }},

Pembelian Anda atas {{ product_name }} telah selesai. Di bawah ini Anda akan menemukan kunci lisensi dan token pengaturan untuk memulai.

Ringkasan Pesanan:
- Produk: {{ product_name }}{% if includes_pos %} (termasuk POS){% endif %}
- Jumlah: {{ price }}
- Nomor Pesanan: {{ order_number }}

KUNCI LISENSI ANDA:
{{ license_key }}
Simpan kunci ini - Anda membutuhkannya untuk penginstalan ulang.

TOKEN PENGATURAN ANDA:
{{ setup_token }}
Gunakan token ini saat penginstalan untuk mengaktifkan toko Anda.

Memulai:
1. Ikuti panduan pengaturan kami untuk menginstal Spwig di server Anda
2. Masukkan token pengaturan Anda saat diminta selama penginstalan
3. Toko Anda akan diaktifkan secara otomatis

Lihat Panduan Pengaturan: {{ setup_url }}
{% if activation_url %}
Buat Akun Anda:
Tetapkan kata sandi untuk mengelola lisensi Anda, mengakses unduhan, dan menerima pembaruan.
{{ activation_url }}
{% endif %}

PENTING:
Simpan email ini dengan aman - email ini berisi kunci lisensi dan token pengaturan Anda untuk referensi di masa depan. Jangan bagikan kredensial ini dengan orang lain.

Butuh bantuan? Hubungi {{ support_email }}