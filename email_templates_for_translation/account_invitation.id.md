---
template_type: account_invitation
category: Core E-commerce
---

# Email Template: account_invitation

## Subject
Buat Akun Anda di {{ site_name }}

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
          Anda Diundang!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Buat akun Anda di {{ site_name }}
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
          Kami menyadari bahwa Anda telah berbelanja dengan kami sebagai tamu. Buat akun penuh untuk membuka manfaat seperti pelacakan pesanan, checkout yang lebih cepat, dan penawaran eksklusif.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Order History Summary -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Riwayat Belanja Anda
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Total Pesanan: {{ total_orders }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Total Pengeluaran: {{ total_spent }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Benefits -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Mengapa Membuat Akun?
        </mj-text>
        <mj-text font-size="14px">
          - Lacak pesanan Anda dan lihat riwayat pesanan
        </mj-text>
        <mj-text font-size="14px">
          - Checkout yang lebih cepat dengan detail yang disimpan
        </mj-text>
        <mj-text font-size="14px">
          - Kelola alamat dan preferensi Anda
        </mj-text>
        <mj-text font-size="14px">
          - Akses penawaran dan promosi eksklusif
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=activation_url text="Buat Akun Anda" %}

    <!-- Note -->
    <mj-section>
      <mj-column>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          Tautan ini akan memungkinkan Anda untuk menetapkan kata sandi untuk akun Anda. Riwayat pesanan yang sudah ada akan tetap terjaga.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Anda Diundang untuk Membuat Akun Anda!

Hai {{ customer_name }},

Kami menyadari bahwa Anda telah berbelanja dengan kami sebagai tamu. Buat akun penuh untuk membuka manfaat seperti pelacakan pesanan, checkout yang lebih cepat, dan penawaran eksklusif.

Riwayat Belanja Anda:
- Total Pesanan: {{ total_orders }}
- Total Pengeluaran: {{ total_spent }}

Mengapa Membuat Akun?
- Lacak pesanan Anda dan lihat riwayat pesanan
- Checkout yang lebih cepat dengan detail yang disimpan
- Kelola alamat dan preferensi Anda
- Akses penawaran dan promosi eksklusif

Buat Akun Anda: {{ activation_url }}

Tautan ini akan memungkinkan Anda untuk menetapkan kata sandi untuk akun Anda. Riwayat pesanan yang sudah ada akan tetap terjaga.

Butuh bantuan? Hubungi {{ support_email }}