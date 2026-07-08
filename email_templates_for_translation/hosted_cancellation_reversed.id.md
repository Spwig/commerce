---
template_type: hosted_cancellation_reversed
category: License
---

# Email Template: hosted_cancellation_reversed

## Subject
Pembatalan Dibatalkan - {{ store_name }}

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
          Pembatalan Dibatalkan
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
          Hi there,
        </mj-text>
        <mj-text>
          Permintaan pembatalan Anda untuk <strong>{{ store_name }}</strong> telah dibatalkan. Langganan <strong>{{ plan_name }}</strong> Anda akan terus berjalan seperti biasa — tidak diperlukan tindakan dari Anda.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Subscription Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Detail Langganan
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Plan: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Tanggal Pemotongan Berikutnya: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Additional Info -->
    <mj-section>
      <mj-column>
        <mj-text>
          Toko Anda terus beroperasi secara normal. Pemotongan akan dilanjutkan pada tanggal yang tercantum di atas.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% if admin_url %}
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Your Store" %}
    {% endif %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Pembatalan Dibatalkan - {{ store_name }}

Hi there,

Permintaan pembatalan Anda untuk {{ store_name }} telah dibatalkan. Langganan {{ plan_name }} Anda akan terus berjalan seperti biasa — tidak diperlukan tindakan dari Anda.

Detail Langganan:
- Plan: {{ plan_name }}
- Tanggal Pemotongan Berikutnya: {{ next_billing_date }}

Toko Anda terus beroperasi secara normal. Pemotongan akan dilanjutkan pada tanggal yang tercantum di atas.

{% if admin_url %}Go to Your Store: {{ admin_url }}

{% endif %}Need help? Contact {{ support_email }}