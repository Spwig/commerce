---
template_type: hosted_cancellation_confirmation
category: License
---

# Email Template: hosted_cancellation_confirmation

## Subject
Pembatalan Dikonfirmasi - {{ store_name }}

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
    <mj-section background-color="#6b7280" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Pembatalan Dikonfirmasi
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
          Hi {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          Langganan <strong>{{ plan_name }}</strong> Anda telah dibatalkan.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Apa yang Terjadi Selanjutnya
        </mj-text>
        <mj-text font-size="14px">
          Anda akan terus memiliki akses penuh hingga <strong>{{ access_until_date }}</strong>.
        </mj-text>
        <mj-text font-size="14px">
          Setelah itu, data toko Anda akan disimpan selama 30 hari hingga <strong>{{ termination_date }}</strong>.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Additional Info -->
    <mj-section>
      <mj-column>
        <mj-text>
          Jika Anda ingin mengekspor data Anda sebelum akses berakhir, Anda dapat melakukannya dari panel administrasi Anda. Berubah pikiran? Anda dapat mengaktifkan kembali langganan Anda kapan saja.
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
Pembatalan Dikonfirmasi - {{ store_name }}

Hi {{ name|default:'there' }},

Langganan {{ plan_name }} Anda telah dibatalkan.

Apa yang Terjadi Selanjutnya:
- Anda akan terus memiliki akses penuh hingga {{ access_until_date }}.
- Setelah itu, data toko Anda akan disimpan selama 30 hari hingga {{ termination_date }}.

Jika Anda ingin mengekspor data Anda sebelum akses berakhir, Anda dapat melakukannya dari panel administrasi Anda. Berubah pikiran? Anda dapat mengaktifkan kembali langganan Anda kapan saja.

Reactivate Subscription: https://spwig.com/account

Need help? Contact {{ support_email }}