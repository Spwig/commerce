---
template_type: hosted_subscription_confirmation
category: License
---

# Email Template: hosted_subscription_confirmation

## Subject
Подписка подтверждена - {{ store_name }}

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
    <mj-section background-color="#16a34a" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          Подписка подтверждена!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          Добро пожаловать в Spwig
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
          Спасибо, что подписались! Ваш план <strong>{{ plan_name }}</strong> для <strong>{{ store_name }}</strong> подтвержден.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Plan Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Детали плана
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          План: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Интервал оплаты: {{ billing_interval }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Сумма: {{ currency }}{{ amount }}{% if intro_period %} (вступительная ставка){% endif %}
        </mj-text>
        {% if intro_period %}
        <mj-text font-size="13px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-top="5px" font-style="italic">
          Ваша вступительная ставка применяется на протяжении {{ intro_period }}. После этого ваш план будет возобновлен по тарифу {{ currency }}{{ full_amount }}/{{ billing_interval }}.
        </mj-text>
        {% endif %}
      </mj-column>
    </mj-section>

    <!-- Next Steps -->
    <mj-section>
      <mj-column>
        <mj-text>
          Ваш магазин сейчас настраивается, и вы получите еще одно письмо, когда он будет готов.
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" padding-top="10px">
          Следующая дата оплаты: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Подписка подтверждена!

Здравствуйте, {{ name|default:'there' }},

Спасибо, что подписались! Ваш план {{ plan_name }} для {{ store_name }} подтвержден.

Детали плана:
- План: {{ plan_name }}
- Интервал оплаты: {{ billing_interval }}
- Сумма: {{ currency }}{{ amount }}{% if intro_period %} (вступительная ставка){% endif %}
{% if intro_period %}
Это ваша вступительная ставка на {{ intro_period }}. После этого ваш план будет возобновлен по тарифу {{ currency }}{{ full_amount }}/{{ billing_interval }}.
{% endif %}
Ваш магазин сейчас настраивается, и вы получите еще одно письмо, когда он будет готов.

Следующая дата оплаты: {{ next_billing_date }}

Нужна помощь? Свяжитесь с {{ support_email }}