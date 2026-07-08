---
template_type: pos_daily_z_report
category: POS
---

# Email Template: pos_daily_z_report

## Subject
📊 Ежедневный Z-отчет - {{ report_date }} - {{ location_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Ежедневный Z-отчет
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Отчет по закрытию дня
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Ежедневный отчет для {{ location_name }} за {{ report_date }}.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Обзор продаж:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Общая сумма продаж:</strong> <span style="font-size: 20px; font-weight: bold; color: #059669;">{{ total_sales }}</span><br/>
              <strong>Транзакции:</strong> {{ transaction_count }}<br/>
              <strong>Проданные товары:</strong> {{ items_sold }}<br/>
              <strong>Средний чек:</strong> {{ average_sale }}<br/>
              <strong>Собранный налог:</strong> {{ tax_collected }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Способы оплаты:
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
          Обзор смен:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Общее число смен:</strong> {{ shift_count }}<br/>
              <strong>Использованные терминалы:</strong> {{ terminal_count }}<br/>
              <strong>Активные кассир:</strong> {{ cashier_count }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% for terminal in terminal_stats %}
        <mj-spacer height="15px" />
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ terminal.name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              Продажи: {{ terminal.sales }} | Транзакции: {{ terminal.transactions }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Корректировки и скидки:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Предоставленные скидки:</strong> {{ discounts_total }}<br/>
              <strong>Выпущенные возвраты:</strong> {{ refunds_total }}<br/>
              <strong>Отмены:</strong> {{ voids_total }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if cash_variance != 0 %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Общая кассовая разница: {{ cash_variance }}
            </mj-text>
            <mj-text font-size="14px" color="#92400e">
              {{ variance_note }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Топ продаваемые товары:
        </mj-text>

        {% for product in top_products %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ product.rank }}. {{ product.name }}</strong> - {{ product.quantity }} продано ({{ product.revenue }})
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Просмотреть полный отчет
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 ЕЖЕДНЕВНЫЙ Z-ОТЧЕТ

Отчет по закрытию дня

Ежедневный отчет для {{ location_name }} за {{ report_date }}.

ОБЗОР ПРОДАЖ:
- Общая сумма продаж: {{ total_sales }}
- Транзакции: {{ transaction_count }}
- Проданные товары: {{ items_sold }}
- Средний чек: {{ average_sale }}
- Собранный налог: {{ tax_collected }}

СПОСОБЫ ОПЛАТЫ:
{% for payment in payment_methods %}
{{ payment.method }}: {{ payment.amount }} ({{ payment.count }} транзакций)
{% endfor %}

ОБЗОР СМЕН:
- Общее число смен: {{ shift_count }}
- Использованные терминалы: {{ terminal_count }}
- Активные кассиры: {{ cashier_count }}

РАЗБИЕНИЕ ПО ТЕРМИНАЛАМ:
{% for terminal in terminal_stats %}
{{ terminal.name }}: {{ terminal.sales }} | {{ terminal.transactions }} транзакций
{% endfor %}

КОРРЕКТИРОВКИ И СКИДКИ:
- Предоставленные скидки: {{ discounts_total }}
- Выпущенные возвраты: {{ refunds_total }}
- Отмены: {{ voids_total }}

{% if cash_variance != 0 %}
⚠️ ОБЩАЯ КАССОВАЯ РАЗНИЦА: {{ cash_variance }}
{{ variance_note }}
{% endif %}

ТОП ПРОДАВАЕМЫЕ ТОВАРЫ:
{% for product in top_products %}
{{ product.rank }}. {{ product.name }} - {{ product.quantity }} продано ({{ product.revenue }})
{% endfor %}

Просмотреть полный отчет: {{ full_report_url }}