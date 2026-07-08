---
template_type: hosted_cancellation_reversed
category: License
---

# Email Template: hosted_cancellation_reversed

## Subject
Отмена отозвана - {{ store_name }}

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
          Отмена отозвана
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
          Привет,
        </mj-text>
        <mj-text>
          Ваша заявка на отмену для <strong>{{ store_name }}</strong> была отозвана. Ваша подписка <strong>{{ plan_name }}</strong> будет продолжаться в обычном режиме — от вас не требуется никаких действий.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Subscription Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Детали подписки
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          План: {{ plan_name }}
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
          Ваш магазин продолжает работать в обычном режиме. Оплата будет возобновлена в указанную дату выше.
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
Отмена отозвана - {{ store_name }}

Привет,

Ваша заявка на отмену для {{ store_name }} была отозвана. Ваша подписка {{ plan_name }} будет продолжаться в обычном режиме — от вас не требуется никаких действий.

Детали подписки:
- План: {{ plan_name }}
- Следующая дата оплаты: {{ next_billing_date }}

Ваш магазин продолжает работать в обычном режиме. Оплата будет возобновлена в указанную дату выше.

{% if admin_url %}Перейти в ваш магазин: {{ admin_url }}

{% endif %}Нужна помощь? Свяжитесь с {{ support_email }}