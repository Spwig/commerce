---
template_type: pos_shift_closed_report
category: POS
---

# Email Template: pos_shift_closed_report

## Subject
📊 Отчет о смене: {{ terminal_name }} - {{ shift_date }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Смена закрыта
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Отчет по смене
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Смена закрыта на {{ terminal_name }} пользователем {{ cashier_name }}.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Детали смены:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Терминал:</strong> {{ terminal_name }}<br/>
              <strong>Кассир:</strong> {{ cashier_name }}<br/>
              <strong>Начало:</strong> {{ shift_started }}<br/>
              <strong>Окончание:</strong> {{ shift_ended }}<br/>
              <strong>Продолжительность:</strong> {{ shift_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Итоги продаж:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Общая сумма продаж:</strong> {{ total_sales }}<br/>
              <strong>Транзакции:</strong> {{ transaction_count }}<br/>
              <strong>Проданные товары:</strong> {{ items_sold }}<br/>
              <strong>Средний чек:</strong> {{ average_sale }}<br/>
              <strong>Собранные налоги:</strong> {{ tax_collected }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Распределение платежей:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            {% for payment in payment_methods %}
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ payment.method }}:</strong> {{ payment.amount }} ({{ payment.count }} транзакций)
            </mj-text>
            {% endfor %}
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Проверка наличных:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Начальный остаток:</strong> {{ opening_cash }}<br/>
              <strong>Продажи наличными:</strong> {{ cash_sales }}<br/>
              <strong>Ожидаемые наличные:</strong> {{ expected_cash }}<br/>
              <strong>Посчитанные наличные:</strong> {{ counted_cash }}<br/>
              <strong>Разница:</strong> <span style="color: {{ cash_difference_color }};">{{ cash_difference }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        {% if discrepancy_amount != 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Разница в наличных: {{ discrepancy_amount }}
            </mj-text>
            {% if discrepancy_note %}
            <mj-text font-size="14px" color="#92400e">
              Примечание: {{ discrepancy_note }}
            </mj-text>
            {% endif %}
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ shift_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Просмотреть полный отчет
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 СМЕНА ЗАКРЫТА

Отчет по смене

Смена закрыта на {{ terminal_name }} пользователем {{ cashier_name }}.

ДЕТАЛИ СМЕНЫ:
- Терминал: {{ terminal_name }}
- Кассир: {{ cashier_name }}
- Начало: {{ shift_started }}
- Окончание: {{ shift_ended }}
- Продолжительность: {{ shift_duration }}

ИТОГИ ПРОДАЖ:
- Общая сумма продаж: {{ total_sales }}
- Транзакции: {{ transaction_count }}
- Проданные товары: {{ items_sold }}
- Средний чек: {{ average_sale }}
- Собранные налоги: {{ tax_collected }}

РАСПРЕДЕЛЕНИЕ ПЛАТЕЖЕЙ:
{% for payment in payment_methods %}
{{ payment.method }}: {{ payment.amount }} ({{ payment.count }} транзакций)
{% endfor %}

ПРОВЕРКА НАЛИЧНЫХ:
- Начальный остаток: {{ opening_cash }}
- Продажи наличными: {{ cash_sales }}
- Ожидаемые наличные: {{ expected_cash }}
- Посчитанные наличные: {{ counted_cash }}
- Разница: {{ cash_difference }}

{% if discrepancy_amount != 0 %}
⚠️ РАЗНИЦА В НАЛИЧНЫХ: {{ discrepancy_amount }}
{% if discrepancy_note %}Примечание: {{ discrepancy_note }}{% endif %}
{% endif %}

Просмотреть полный отчет: {{ shift_report_url }}