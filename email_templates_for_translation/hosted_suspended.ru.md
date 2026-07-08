---
template_type: hosted_suspended
category: License
---

# Email Template: hosted_suspended

## Subject
Магазин приостановлен - {{ store_name }}

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
          Аккаунт приостановлен
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
          Привет, {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          Ваш магазин <strong>{{ store_name }}</strong> был приостановлен из-за неоплаченных счетов.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What This Means -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Что это значит
        </mj-text>
        <mj-text font-size="14px">
          Ваш магазин теперь находится в режиме только для чтения — клиенты могут просматривать товары, но заказы отключены. Ваши данные в безопасности и будут сохранены в течение 30 дней.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reactivate -->
    <mj-section>
      <mj-column>
        <mj-text>
          Чтобы восстановить полный доступ, пожалуйста, обновите способ оплаты и погасите оставшуюся сумму.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Восстановить магазин" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Аккаунт приостановлен - {{ store_name }}

Привет, {{ name|default:'there' }},

Ваш магазин {{ store_name }} был приостановлен из-за неоплаченных счетов.

Что это значит:
Ваш магазин теперь находится в режиме только для чтения — клиенты могут просматривать товары, но заказы отключены. Ваши данные в безопасности и будут сохранены в течение 30 дней.

Чтобы восстановить полный доступ, пожалуйста, обновите способ оплаты и погасите оставшуюся сумму.

Восстановить магазин: https://spwig.com/account

Нужна помощь? Свяжитесь с {{ support_email }}