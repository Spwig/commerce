---
template_type: hosted_interval_changed
category: License
---

# Email Template: hosted_interval_changed

## Subject
Обновление оплаты - {{ store_name }}

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
          Обновление оплаты
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
          Здравствуйте,
        </mj-text>
        <mj-text>
          Интервал оплаты вашего плана <strong>{{ plan_name }}</strong> на <strong>{{ store_name }}</strong> был обновлен.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Billing Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Детали оплаты
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          План: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Предыдущий интервал оплаты: {{ old_interval }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Новый интервал оплаты: {{ new_interval }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Следующая дата оплаты: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Additional Info -->
    <mj-section>
      <mj-column>
        <mj-text>
          Ваша подписка остается активной. Вы можете управлять настройками оплаты в любое время через свой аккаунт.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Управление подпиской" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Обновление оплаты - {{ store_name }}

Здравствуйте,

Интервал оплаты вашего плана {{ plan_name }} на {{ store_name }} был обновлен.

Детали оплаты:
- План: {{ plan_name }}
- Предыдущий интервал оплаты: {{ old_interval }}
- Новый интервал оплаты: {{ new_interval }}
- Следующая дата оплаты: {{ next_billing_date }}

Ваша подписка остается активной. Вы можете управлять настройками оплаты в любое время через свой аккаунт.

Управление подпиской: https://spwig.com/account

Нужна помощь? Свяжитесь с {{ support_email }}