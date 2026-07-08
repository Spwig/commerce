---
template_type: hosted_payment_failed
category: License
---

# Email Template: hosted_payment_failed

## Subject
Pembayaran Gagal - {{ store_name }}

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
    <mj-section background-color="#d97706" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Masalah Pembayaran
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Tindakan diperlukan untuk {{ store_name }}
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
          Kami tidak dapat memproses pembayaran Anda untuk <strong>{{ plan_name }}</strong>.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payment Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Detail Pembayaran
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Jumlah: {{ currency }}{{ amount }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Rencana: {{ plan_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text>
          {{ retry_info }}. Untuk menghindari gangguan layanan, silakan perbarui metode pembayaran Anda.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Update Payment Method" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Masalah Pembayaran - {{ store_name }}

Hai {{ name|default:'there' }},

Kami tidak dapat memproses pembayaran Anda untuk {{ plan_name }}.

Detail Pembayaran:
- Jumlah: {{ currency }}{{ amount }}
- Rencana: {{ plan_name }}

{{ retry_info }}. Untuk menghindari gangguan layanan, silakan perbarui metode pembayaran Anda.

Perbarui Metode Pembayaran: https://spwig.com/account

Butuh bantuan? Hubungi {{ support_email }}