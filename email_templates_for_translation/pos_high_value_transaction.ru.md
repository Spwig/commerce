---
template_type: pos_high_value_transaction
category: POS
---

# Email Template: pos_high_value_transaction

## Subject
💰 Высокодоходная транзакция: {{ transaction_amount }} на {{ terminal_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          💰 Высокодоходная транзакция
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Обработана большая транзакция
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Обработана транзакция в размере {{ transaction_amount }} на {{ terminal_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Детали транзакции:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Сумма:</strong> <span style="font-size: 18px; font-weight: bold; color: #059669;">{{ transaction_amount }}</span><br/>
              <strong>Терминал:</strong> {{ terminal_name }}<br/>
              <strong>Кассир:</strong> {{ cashier_name }}<br/>
              <strong>Время:</strong> {{ transaction_time }}<br/>
              <strong>Номер транзакции:</strong> {{ transaction_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Информация о платеже:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            {% for payment in payment_methods %}
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ payment.method }}</strong>: {{ payment.amount }}
            </mj-text>
            {% endfor %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Сводка товаров:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Всего товаров:</strong> {{ item_count }}<br/>
              <strong>Промежуточный итог:</strong> {{ subtotal }}<br/>
              <strong>Налог:</strong> {{ tax_amount }}<br/>
              <strong>Итого:</strong> {{ transaction_amount }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if customer_info %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Информация о клиенте:
        </mj-text>
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ customer_info }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              Эта уведомление отправляется для всех транзакций, превышающих {{ threshold_amount }}, с целью предотвращения мошенничества и мониторинга.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ transaction_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Просмотреть транзакцию
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ receipt_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Просмотреть чек
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
💰 ВЫСОКОДОХОДНАЯ ТРАНЗАКЦИЯ

Обработана большая транзакция

Обработана транзакция в размере {{ transaction_amount }} на {{ terminal_name }}.

ДЕТАЛИ ТРАНЗАКЦИИ:
- Сумма: {{ transaction_amount }}
- Терминал: {{ terminal_name }}
- Кассир: {{ cashier_name }}
- Время: {{ transaction_time }}
- Номер транзакции: {{ transaction_id }}

Информация о платеже:
{% for payment in payment_methods %}
{{ payment.method }}: {{ payment.amount }}
{% endfor %}

Сводка товаров:
- Всего товаров: {{ item_count }}
- Промежуточный итог: {{ subtotal }}
- Налог: {{ tax_amount }}
- Итого: {{ transaction_amount }}

{% if customer_info %}
Информация о клиенте:
{{ customer_info }}
{% endif %}

Это уведомление отправляется для всех транзакций, превышающих {{ threshold_amount }}, с целью предотвращения мошенничества и мониторинга.

Просмотреть транзакцию: {{ transaction_url }}
Просмотреть чек: {{ receipt_url }}