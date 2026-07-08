---
template_type: hosted_suspended
category: License
---

# Email Template: hosted_suspended

## Subject
Toko Ditangguhkan - {{ store_name }}

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
    <mj-section background-color="#dc2626" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Akun Ditangguhkan
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }}
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
          Toko Anda <strong>{{ store_name }}</strong> telah ditangguhkan karena pembayaran yang belum lunas.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What This Means -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Arti dari Ini
        </mj-text>
        <mj-text font-size="14px">
          Toko Anda sekarang berada dalam mode hanya baca -- pelanggan dapat menjelajah tetapi pesanan dinonaktifkan. Data Anda aman dan akan disimpan selama 30 hari.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reactivate -->
    <mj-section>
      <mj-column>
        <mj-text>
          Untuk memulihkan akses penuh, silakan perbarui metode pembayaran Anda dan lunasi sisa utang.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Aktifkan Kembali Toko Anda" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Akun Ditangguhkan - {{ store_name }}

Hai {{ name|default:'there' }},

Toko Anda {{ store_name }} telah ditangguhkan karena pembayaran yang belum lunas.

Arti dari Ini:
Toko Anda sekarang berada dalam mode hanya baca -- pelanggan dapat menjelajah tetapi pesanan dinonaktifkan. Data Anda aman dan akan disimpan selama 30 hari.

Untuk memulihkan akses penuh, silakan perbarui metode pembayaran Anda dan lunasi sisa utang.

Aktifkan Kembali Toko Anda: https://spwig.com/account

Butuh bantuan? Hubungi {{ support_email }}