---
template_type: hosted_termination_warning
category: License
---

# Email Template: hosted_termination_warning

## Subject
Penting: Penghapusan Data dalam 7 Hari - {{ store_name }}

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
          Peringatan Penghapusan Data
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
          Toko Anda <strong>{{ store_name }}</strong> dan semua data terkait akan dihapus secara permanen pada <strong>{{ termination_date }}</strong>. Tindakan ini tidak dapat dibatalkan.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What You Can Do -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Apa yang Bisa Anda Lakukan
        </mj-text>
        <mj-text font-size="14px">
          Jika Anda ingin mempertahankan data Anda, silakan ekspor data tersebut sebelum tanggal ini atau aktifkan kembali langganan Anda untuk mencegah penghapusan.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Reactivate Subscription" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Peringatan Penghapusan Data - {{ store_name }}

Hai {{ name|default:'there' }},

Toko Anda {{ store_name }} dan semua data terkait akan dihapus secara permanen pada {{ termination_date }}. Tindakan ini tidak dapat dibatalkan.

Apa yang Bisa Anda Lakukan:
Jika Anda ingin mempertahankan data Anda, silakan ekspor data tersebut sebelum tanggal ini atau aktifkan kembali langganan Anda untuk mencegah penghapusan.

Reactivate Subscription: https://spwig.com/account

Butuh bantuan? Hubungi {{ support_email }}