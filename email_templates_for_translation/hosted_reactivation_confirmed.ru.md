---
template_type: hosted_reactivation_confirmed
category: License
---

# Email Template: hosted_reactivation_confirmed

## Subject
Добро пожаловать обратно! {{ store_name }} снова активна

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
          Добро пожаловать обратно!
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          {{ store_name }} снова активна
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
          Великолепные новости! Ваш магазин <strong>{{ store_name }}</strong> был восстановлен. Ваша подписка <strong>{{ plan_name }}</strong> теперь активна, и ваш магазин возвращается в онлайн.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Reactivation Details -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" padding-bottom="10px">
          Детали восстановления
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          План: {{ plan_name }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Обработано платежа: {{ currency }}{{ amount }}
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Следующая дата оплаты: {{ next_billing_date }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- What Happens Now -->
    <mj-section>
      <mj-column>
        <mj-text>
          Ваш магазин сейчас возвращается в онлайн. Возможно, потребуется несколько минут, чтобы все было полностью восстановлено. После того, как магазин будет доступен, вы сможете зайти по адресу {{ store_url }}.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="Go to Your Store" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
Добро пожаловать обратно! {{ store_name }} снова активна

Здравствуйте,

Великолепные новости! Ваш магазин {{ store_name }} был восстановлен. Ваша подписка {{ plan_name }} теперь активна, и ваш магазин возвращается в онлайн.

Детали восстановления:
- План: {{ plan_name }}
- Обработано платежа: {{ currency }}{{ amount }}
- Следующая дата оплаты: {{ next_billing_date }}

Ваш магазин сейчас возвращается в онлайн. Возможно, потребуется несколько минут, чтобы все было полностью восстановлено. После того, как магазин будет доступен, вы сможете зайти по адресу {{ store_url }}.

Перейти в ваш магазин: {{ admin_url }}

Нужна помощь? Свяжитесь с {{ support_email }}