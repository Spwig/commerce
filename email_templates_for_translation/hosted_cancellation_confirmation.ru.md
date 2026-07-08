---
template_type: hosted_cancellation_confirmation
category: License
---

# Email Template: hosted_cancellation_confirmation

## Subject
Подтверждение отмены - {{ store_name }}

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
          Подтверждение отмены
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
          Здравствуйте, {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          Ваша подписка <strong>{{ plan_name }}</strong> была отменена.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Что будет дальше
        </mj-text>
        <mj-text font-size="14px">
          Вы продолжите пользоваться полным доступом до <strong>{{ access_until_date }}</strong>.
        </mj-text>
        <mj-text font-size="14px">
          После этого данные вашего магазина будут сохранены в течение 30 дней до <strong>{{ termination_date }}</strong>.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Additional Info -->
    <mj-section>
      <mj-column>
        <mj-text>
          Если вы хотите экспортировать данные до окончания доступа, вы можете сделать это через панель администратора. Изменили мнение? Вы можете восстановить подписку в любое время.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url="https://spwig.com/account" text="Восстановить подписку" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Подтверждение отмены - {{ store_name }}

Здравствуйте, {{ name|default:'there' }},

Ваша подписка {{ plan_name }} была отменена.

Что будет дальше:
- Вы продолжите пользоваться полным доступом до {{ access_until_date }}.
- После этого данные вашего магазина будут сохранены в течение 30 дней до {{ termination_date }}.

Если вы хотите экспортировать данные до окончания доступа, вы можете сделать это через панель администратора. Изменили мнение? Вы можете восстановить подписку в любое время.

Восстановить подписку: https://spwig.com/account

Нужна помощь? Свяжитесь с {{ support_email }}