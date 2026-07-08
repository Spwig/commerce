---
template_type: shipping_delayed
category: Shipping
---

# Email Template: shipping_delayed

## Subject
Обновление по вашему заказу #{{ order_number }} - Задержка в доставке

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Обновление по вашему заказу
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Здравствуйте, {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Мы хотели сообщить вам о задержке с вашим заказом. Мы приносим извинения за неудобства и ценим ваше терпение.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Детали заказа:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Номер заказа:</strong> {{ order_number }}<br/>
              <strong>Исходная дата доставки:</strong> {{ original_delivery_date }}<br/>
              <strong>Новая дата доставки:</strong> {{ new_delivery_date }}<br/>
              <strong>Номер отслеживания:</strong> {{ tracking_number }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Причина задержки:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ delay_reason }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Отслеживать ваш заказ
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          Мы работаем над тем, чтобы как можно быстрее доставить ваш заказ. Вы получите еще одно обновление, когда ваша посылка отправится.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Вопросы? <a href="{{ support_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Свяжитесь с нашей службой поддержки</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Обновление по вашему заказу #{{ order_number }}

Здравствуйте, {{ customer_name }},

Мы хотели сообщить вам о задержке с вашим заказом. Мы приносим извинения за неудобства и ценим ваше терпение.

ДЕТАЛИ ЗАКАЗА:
- Номер заказа: {{ order_number }}
- Исходная дата доставки: {{ original_delivery_date }}
- Новая дата доставки: {{ new_delivery_date }}
- Номер отслеживания: {{ tracking_number }}

ПРИЧИНА ЗАДЕРЖКИ:
{{ delay_reason }}

Отслеживать ваш заказ: {{ tracking_url }}

Мы работаем над тем, чтобы как можно быстрее доставить ваш заказ. Вы получите еще одно обновление, когда ваша посылка отправится.

Вопросы? Свяжитесь с нашей службой поддержки: {{ support_url }}

---
Это обновление для заказа #{{ order_number }} в {{ shop_name }}.