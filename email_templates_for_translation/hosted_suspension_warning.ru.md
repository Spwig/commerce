---
template_type: hosted_suspension_warning
category: License
---

# Email Template: hosted_suspension_warning

## Subject
Действие требуется - {{ store_name }}

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
    <mj-section background-color="#ea580c" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Предупреждение о приостановке
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
          Ваша оплата за <strong>{{ plan_name }}</strong> просрочена. Если вы не устраните проблему к <strong>{{ grace_end_date }}</strong>, ваш магазин будет переведён в режим только для чтения.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What Suspension Means -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Что означает приостановка
        </mj-text>
        <mj-text font-size="14px">
          Если ваш магазин будет приостановлен, он останется виден посетителям, но вы не сможете вносить изменения. Новые заказы будут приостановлены до погашения задолженности.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Resolve -->
    <mj-section>
      <mj-column>
        <mj-text>
          Пожалуйста, обновите способ оплаты, чтобы избежать сбоев в работе вашего магазина.
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
Предупреждение о приостановке - {{ store_name }}

Привет, {{ name|default:'there' }},

Ваша оплата за {{ plan_name }} просрочена. Если вы не устраните проблему к {{ grace_end_date }}, ваш магазин будет переведён в режим только для чтения.

Что означает приостановка:
Если ваш магазин будет приостановлен, он останется виден посетителям, но вы не сможете вносить изменения. Новые заказы будут приостановлены до погашения задолженности.

Пожалуйста, обновите способ оплаты, чтобы избежать сбоев в работе вашего магазина.

Обновить способ оплаты: https://spwig.com/account

Нужна помощь? Свяжитесь с {{ support_email }}