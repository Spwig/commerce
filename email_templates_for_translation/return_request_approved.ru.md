---
template_type: return_request_approved
category: Returns
---

# Email Template: return_request_approved

## Subject
Возврат одобрен - Заказ #{{ order_number }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="{{ theme.color.surface|default:'#f0fdf4' }}">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#166534' }}">
          Возврат одобрен
        </mj-text>
        <mj-text font-size="14px" color="{{ theme.color.text|default:'#166534' }}">
          Заказ #{{ order_number }}
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Здравствуйте, {{ customer_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Ваш запрос на возврат для заказа <strong>#{{ order_number }}</strong> был одобрен.
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Далее:</strong>
        </mj-text>

        <mj-text font-size="15px" line-height="1.8" color="{{ theme.color.text|default:'#4b5563' }}">
          1. Скачайте и распечатайте этикетку возврата ниже<br/>
          2. Упакуйте товары в оригинальную упаковку, если это возможно<br/>
          3. Прикрепите этикетку возврата снаружи упаковки<br/>
          4. Отвезите в ближайшее отделение доставки
        </mj-text>

        {% if return_label_url %}
        <mj-spacer height="20px" />
        <mj-button href="{{ return_label_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Скачать этикетку возврата
        </mj-button>
        {% endif %}

        {% if return_tracking_number %}
        <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>Номер отслеживания возврата:</strong> {{ return_tracking_number }}
        </mj-text>
        {% endif %}

        <mj-section background-color="{{ theme.color.surface|default:'#fffbeb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" line-height="1.6" color="{{ theme.color.text|default:'#92400e' }}">
              <strong>Важно:</strong> Пожалуйста, отправьте возврат в течение 7 дней, чтобы гарантировать оперативную обработку возврата.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          После получения и проверки вашего возврата мы обработаем возврат средств на оригинальный способ оплаты.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Возврат одобрен - Заказ #{{ order_number }}

Здравствуйте, {{ customer_name }},

Ваш запрос на возврат для заказа #{{ order_number }} был одобрен.

Далее:
1. Скачайте и распечатайте этикетку возврата
2. Упакуйте товары в оригинальную упаковку, если это возможно
3. Прикрепите этикетку возврата снаружи упаковки
4. Отвезите в ближайшее отделение доставки

{% if return_label_url %}Скачайте этикетку возврата: {{ return_label_url }}{% endif %}
{% if return_tracking_number %}Номер отслеживания возврата: {{ return_tracking_number }}{% endif %}

Важно: Пожалуйста, отправьте возврат в течение 7 дней, чтобы гарантировать оперативную обработку возврата.

После получения и проверки вашего возврата мы обработаем возврат средств на оригинальный способ оплаты.