---
template_type: cart_recovered_thank_you
category: Cart Recovery
---

# Email Template: cart_recovered_thank_you

## Subject
Спасибо за ваш заказ №{{ order_number }} - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 Спасибо за ваш заказ!
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Здравствуйте, {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Мы рады, что вы завершили покупку! Ваш заказ подтвержден, и мы готовим его к отправке.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Сводка заказа
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Номер заказа:</strong> {{ order_number }}<br/>
              <strong>Дата заказа:</strong> {{ order_date }}<br/>
              <strong>Итого:</strong> {{ order_total }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ order_tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Отслеживать заказ
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Что происходит дальше?
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Мы подготовим ваш заказ (обычно в течение 1-2 рабочих дней)<br/>
          2. Вы получите подтверждение доставки с информацией о трекинге<br/>
          3. Ваш заказ будет доставлен по адресу: {{ shipping_address }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" align="center">
              💡 <strong>Знаете ли вы?</strong><br/>
              Вы можете отслеживать свой заказ в любое время в панели управления вашей учетной записи.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Вопросы? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Свяжитесь с нашей службой поддержки</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 СПАСИБО ЗА ВАШ ЗАКАЗ!

Здравствуйте, {{ customer_name }},

Мы рады, что вы завершили покупку! Ваш заказ подтвержден, и мы готовим его к отправке.

СВОДКА ЗАКАЗА:
- Номер заказа: {{ order_number }}
- Дата заказа: {{ order_date }}
- Итого: {{ order_total }}

Отслеживать заказ: {{ order_tracking_url }}

ЧТО ПРОИСХОДИТ ДАЛЕЕ?
1. Мы подготовим ваш заказ (обычно в течение 1-2 рабочих дней)
2. Вы получите подтверждение доставки с информацией о трекинге
3. Ваш заказ будет доставлен по адресу: {{ shipping_address }}

💡 ЗНАЕТЕ ЛИ ВЫ?
Вы можете отслеживать свой заказ в любое время в панели управления вашей учетной записи.

Вопросы? Свяжитесь с нашей службой поддержки: {{ support_url }}

---
Заказ №{{ order_number }} в {{ shop_name }}