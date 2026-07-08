---
template_type: license_trial_welcome
category: License
---

# Email Template: license_trial_welcome

## Subject
Selamat datang di Spwig - Uji Coba Gratis Anda {{ trial_days }} Hari

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
    <mj-section background-color="#059669" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Selamat datang di Spwig!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Uji coba gratis Anda selama {{ trial_days }} hari siap digunakan
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
          Terima kasih telah mencoba <strong>{{ product_name }}</strong>! Uji coba Anda telah diaktifkan dan Anda memiliki <strong>{{ trial_days }} hari</strong> untuk mengeksplorasi segala sesuatu yang ditawarkan Spwig{% if includes_pos %}, termasuk sistem Point of Sale kami{% endif %}.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Token Box -->
    <mj-section background-color="#f0fdf4" padding="25px" border-radius="8px">
      <mj-column>
        <mj-text font-size="12px" color="#065f46" font-weight="bold" align="center">
          TOKEN PEMASANGAN ANDA
        </mj-text>
        <mj-text font-size="14px" font-weight="bold" color="#059669" align="center" font-family="'Courier New', monospace" padding="10px 0" word-break="break-all">
          {{ setup_token }}
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Gunakan token ini saat menginstal untuk mengaktifkan toko uji coba Anda
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
          1. Ikuti panduan pemasangan kami untuk menginstal Spwig di server Anda
        </mj-text>
        <mj-text font-size="14px">
          2. Masukkan token pemasangan Anda saat diminta selama proses instalasi
        </mj-text>
        <mj-text font-size="14px">
          3. Mulailah membangun toko online Anda!
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Setup Guide CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=setup_url text="Lihat Panduan Pemasangan" %}

    <!-- What's Included -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Apa yang Termasuk dalam Uji Coba Anda
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Akses penuh ke semua fitur inti selama {{ trial_days }} hari
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Katalog produk, pesanan, dan manajemen pelanggan
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Kustomisasi tema dan pembuat halaman
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Integrasi penyedia pembayaran dan pengiriman
        </mj-text>
        {% if includes_pos %}
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Sistem Point of Sale (POS)
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Trial Info -->
    <mj-section>
      <mj-column>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Uji coba Anda akan berakhir dalam {{ trial_days }} hari. Ketika Anda siap, upgrade ke lisensi penuh untuk terus menjalankan toko Anda tanpa kehilangan data.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Selamat datang di Spwig!
Uji coba gratis Anda selama {{ trial_days }} hari siap digunakan.

Hai {{ customer_name }},

Terima kasih telah mencoba {{ product_name }}! Uji coba Anda telah diaktifkan dan Anda memiliki {{ trial_days }} hari untuk mengeksplorasi segala sesuatu yang ditawarkan Spwig{% if includes_pos %}, termasuk sistem Point of Sale kami{% endif %}.

TOKEN PEMASANGAN ANDA:
{{ setup_token }}
Gunakan token ini saat menginstal untuk mengaktifkan toko uji coba Anda.

Memulai:
1. Ikuti panduan pemasangan kami untuk menginstal Spwig di server Anda
2. Masukkan token pemasangan Anda saat diminta selama proses instalasi
3. Mulailah membangun toko online Anda!

Lihat Panduan Pemasangan: {{ setup_url }}

Apa yang Termasuk dalam Uji Coba Anda:
- Akses penuh ke semua fitur inti selama {{ trial_days }} hari
- Katalog produk, pesanan, dan manajemen pelanggan
- Kustomisasi tema dan pembuat halaman
- Integrasi penyedia pembayaran dan pengiriman
{% if includes_pos %}- Sistem Point of Sale (POS){% endif %}

Uji coba Anda akan berakhir dalam {{ trial_days }} hari. Ketika Anda siap, upgrade ke lisensi penuh untuk terus menjalankan toko Anda tanpa kehilangan data.

Butuh bantuan? Hubungi {{ support_email }}