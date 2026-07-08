---
template_type: pos_cash_discrepancy_alert
category: POS
---

# Email Template: pos_cash_discrepancy_alert

## Subject
⚠️ Ошибка суммы наличных: {{ terminal_name }} - {{ discrepancy_amount }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Обнаружена ошибка суммы наличных
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Предупреждение о расхождении сумм
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          При закрытии смены на {{ terminal_name }} обнаружено расхождение сумм в размере {{ discrepancy_amount }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Детали расхождения:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Терминал:</strong> {{ terminal_name }}<br/>
              <strong>Кассир:</strong> {{ cashier_name }}<br/>
              <strong>Дата смены:</strong> {{ shift_date }}<br/>
              <strong>Длительность смены:</strong> {{ shift_duration }}<br/>
              <strong>Обнаружено:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Счет наличных:
        </mj-text>

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="#92400e">
              <strong>Ожидаемая сумма:</strong> {{ expected_cash }}<br/>
              <strong>Посчитанная сумма:</strong> {{ counted_cash }}<br/>
              <strong>Расхождение:</strong> <span style="font-weight: bold; font-size: 18px;">{{ discrepancy_amount }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Начальный остаток:</strong> {{ opening_cash }}<br/>
              <strong>Продажи наличными:</strong> {{ cash_sales }}<br/>
              <strong>Возвраты наличными:</strong> {{ cash_refunds }}<br/>
              <strong>Выплачено наличными:</strong> {{ cash_paid_out }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if cashier_note %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Примечание кассира:
        </mj-text>
        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              "{{ cashier_note }}"
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Рекомендуемые действия:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Проверьте историю транзакций на наличие ошибок<br/>
          2. Проверьте наличные платежи, не учтенные в системе<br/>
          3. Убедитесь, что подсчет наличных был точным<br/>
          4. Задокументируйте расхождение в примечаниях к смене<br/>
          5. Свяжитесь с кассиром, если это необходимо
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ shift_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Просмотреть отчет по смене
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ transaction_history_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Проверить транзакции
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ ОБНАРУЖЕНО РАСХОЖДЕНИЕ СУММ

Предупреждение о расхождении сумм

При закрытии смены на {{ terminal_name }} обнаружено расхождение сумм в размере {{ discrepancy_amount }}.

Детали расхождения:
- Терминал: {{ terminal_name }}
- Кассир: {{ cashier_name }}
- Дата смены: {{ shift_date }}
- Длительность смены: {{ shift_duration }}
- Обнаружено: {{ detected_at }}

Счет наличных:
- Ожидаемая сумма: {{ expected_cash }}
- Посчитанная сумма: {{ counted_cash }}
- Расхождение: {{ discrepancy_amount }}

BREAKDOWN:
- Начальный остаток: {{ opening_cash }}
- Продажи наличными: {{ cash_sales }}
- Возвраты наличными: {{ cash_refunds }}
- Выплачено наличными: {{ cash_paid_out }}

{% if cashier_note %}
ПРИМЕЧАНИЕ КАССИРА:
"{{ cashier_note }}"
{% endif %}

РЕКОМЕНДУЕМЫЕ ДЕЙСТВИЯ:
1. Проверьте историю транзакций на наличие ошибок
2. Проверьте наличные платежи, не учтенные в системе
3. Убедитесь, что подсчет наличных был точным
4. Задокументируйте расхождение в примечаниях к смене
5. Свяжитесь с кассиром, если это необходимо

Просмотреть отчет по смене: {{ shift_report_url }}
Проверить транзакции: {{ transaction_history_url }}
