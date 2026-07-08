---
template_type: subscription_payment_success
category: Subscriptions
---

# Email Template: subscription_payment_success

## Subject
✅ Получен платеж за {{ plan_name }} - {{ shop_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          ✅ Оплата прошла успешно
        </mj-text>
        <mj-text font-size="18px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          Спасибо за ваш платеж
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Payment Details Card -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-wrapper background-color="#f0fdf4" padding="30px" border="2px solid {{ theme.color.success|default:'#10b981' }}" border-radius="12px">
          <mj-section background-color="transparent">
            <mj-column>
              <mj-text font-size="20px" font-weight="600" color="#14532d" align="center" padding-bottom="15px">
                Чек об оплате
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>План:</strong> {{ plan_name }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Сумма оплаты:</strong> {{ amount_paid }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Дата оплаты:</strong> {{ payment_date|date:"F d, Y" }}
              </mj-text>

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Способ оплаты:</strong> {{ payment_method }}
              </mj-text>

              {% if transaction_id %}
              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Номер транзакции:</strong> {{ transaction_id }}
              </mj-text>
              {% endif %}

              <mj-divider border-color="#bbf7d0" border-width="1px" padding="15px 0" />

              <mj-text font-size="14px" color="{{ theme.color.text|default:'#1f2937' }}" padding="5px 0">
                <strong>Дата следующего платежа:</strong> {{ next_billing_date|date:"F d, Y" }}
              </mj-text>
            </mj-column>
          </mj-section>
        </mj-wrapper>
      </mj-column>
    </mj-section>

    <!-- Thank You Message -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding="0 20px" line-height="1.6" align="center">
          Ваша подписка остается активной, и вы продолжаете иметь полный доступ ко всем преимуществам.
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Buttons -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="10px 20px 30px 20px">
      <mj-column>
        <mj-button href="{{ manage_subscription_url }}" background-color="{{ theme.color.info|default:'#3b82f6' }}" color="{{ theme.color.background|default:'#ffffff' }}" font-size="16px" font-weight="600" border-radius="6px" padding="14px 32px">
          Просмотр подписки
        </mj-button>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="15px">
          <a href="{{ download_receipt_url }}" style="color: {{ theme.color.info|default:'#3b82f6' }}; text-decoration: underline;">
            Скачать чек
          </a>
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Support Block -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="12px" color="#9ca3af" align="center">
          Нужна помощь? Свяжитесь с нами по адресу {{ support_email }}
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Spwig Branding Footer -->
    <mj-section padding="15px 0 10px 0" background-color="transparent">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" border-width="1px" padding="0 0 12px 0"></mj-divider>
        <mj-text align="center" padding="0" font-size="11px" color="#9ca3af" line-height="16px">
          <a href="https://spwig.com" style="color: #9ca3af; text-decoration: none; display: inline-flex; align-items: center; gap: 4px;" target="_blank">
            <img src="{{ shop_url }}/static/email_system/img/spwig-favicon.png" alt="Spwig" width="12" height="12" style="vertical-align: middle; display: inline-block;" />
            Powered by Spwig
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✅ Оплата прошла успешно

Спасибо за ваш платеж

ЧЕК ОПЛАТЫ:
План: {{ plan_name }}
Сумма оплаты: {{ amount_paid }}
Дата оплаты: {{ payment_date|date:"F d, Y" }}
Способ оплаты: {{ payment_method }}
{% if transaction_id %}Номер транзакции: {{ transaction_id }}
{% endif %}Дата следующего платежа: {{ next_billing_date|date:"F d, Y" }}

Ваша подписка остается активной, и вы продолжаете иметь полный доступ ко всем преимуществам.

Просмотр подписки: {{ manage_subscription_url }}
Скачать чек: {{ download_receipt_url }}

Нужна помощь? Свяжитесь с нами по адресу {{ support_email }}

---
Powered by Spwig - https://spwig.com