---
template_type: hosted_provision_complete
category: License
---

# Email Template: hosted_provision_complete

## Subject
Toko Anda Siap - {{ store_name }}

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
          Toko Anda Sudah Aktif!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} siap digunakan oleh Anda
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Hai {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          Berita baik! Toko Spwig Anda <strong>{{ store_name }}</strong> telah disiapkan dan kini sudah aktif. Anda dapat mulai mengatur produk, branding, dan metode pembayaran Anda segera.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Store Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Detail Toko Anda
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          URL Toko: {{ store_url }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Panel Admin: {{ admin_url }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Wilayah: {{ region }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Getting Started -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Panduan Cepat
        </mj-text>
        <mj-text font-size="14px">
          1. Masuk ke panel admin Anda menggunakan email dan kata sandi yang Anda tetapkan saat checkout
        </mj-text>
        <mj-text font-size="14px">
          2. Tambahkan logo dan branding toko Anda di bawah Desain > Pengaturan Tema
        </mj-text>
        <mj-text font-size="14px">
          3. Tambahkan produk pertama Anda di bawah Katalog > Produk
        </mj-text>
        <mj-text font-size="14px">
          4. Atur penyedia pembayaran di bawah Pengaturan > Penyedia Pembayaran
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Admin Panel" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Toko Anda Sudah Aktif!

{{ store_name }} siap digunakan oleh Anda.

Hai {{ name|default:'there' }},

Berita baik! Toko Spwig Anda {{ store_name }} telah disiapkan dan kini sudah aktif. Anda dapat mulai mengatur produk, branding, dan metode pembayaran Anda segera.

Detail Toko Anda:
- URL Toko: {{ store_url }}
- Panel Admin: {{ admin_url }}
- Wilayah: {{ region }}

Panduan Cepat:
1. Masuk ke panel admin Anda menggunakan email dan kata sandi yang Anda tetapkan saat checkout
2. Tambahkan logo dan branding toko Anda di bawah Desain > Pengaturan Tema
3. Tambahkan produk pertama Anda di bawah Katalog > Produk
4. Atur penyedia pembayaran di bawah Pengaturan > Penyedia Pembayaran

Buka Panel Admin: {{ admin_url }}

Butuh bantuan? Hubungi {{ support_email }}