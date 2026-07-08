---
template_type: hosted_payment_failed
category: License
---

# Email Template: hosted_payment_failed

## Subject
Ошибка оплаты - {{ store_name }}

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
          Ошибка оплаты
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Требуется действие для {{ store_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          Привет, {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          Мы не смогли обработать вашу оплату за <strong>{{ plan_name }}</strong>.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payment Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Детали оплаты
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Сумма: {{ currency }}{{ amount }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          План: {{ plan_name }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text>
          {{ retry_info }}. Чтобы избежать прерывания услуги, пожалуйста, обновите способ оплаты.
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
Ошибка оплаты - {{ store_name }}

Привет, {{ name|default:'there' }},

Мы не смогли обработать вашу оплату за {{ plan_name }}.

Детали оплаты:
- Сумма: {{ currency }}{{ amount }}
- План: {{ plan_name }}

{{ retry_info }}. Чтобы избежать прерывания услуги, пожалуйста, обновите способ оплаты.

Обновить способ оплаты: https://spwig.com/account

Нужна помощь? Свяжитесь с {{ support_email }}