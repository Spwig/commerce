---
template_type: admin_report_daily_sales
category: Admin Reports
---

# Email Template: admin_report_daily_sales

## Subject
📊 Ежедневный отчет о продажах - {{ report_date }} - {{ total_revenue }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Ежедневный отчет о продажах
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Сводка продаж - {{ report_date }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Общий доход:</strong> <span style="font-size: 20px; font-weight: bold; color: #059669;">{{ total_revenue }}</span><br/>
              <strong>Заказы:</strong> {{ order_count }}<br/>
              <strong>Средний чек:</strong> {{ avg_order_value }}<br/>
              <strong>Коэффициент конверсии:</strong> {{ conversion_rate }}%
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Посетители:</strong> {{ visitor_count }}<br/>
              <strong>Новые клиенты:</strong> {{ new_customers }}<br/>
              <strong>Вернувшиеся клиенты:</strong> {{ returning_customers }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Топ-продукты:
        </mj-text>

        {% for product in top_products %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ product.rank }}. {{ product.name }}</strong> - {{ product.sales }} продаж ({{ product.revenue }})
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
📊 ЕЖЕДНЕВНЫЙ ОТЧЕТ О ПРОДАЖАХ

Сводка продаж - {{ report_date }}

ВЫПОЛНЕНИЕ:
- Общий доход: {{ total_revenue }}
- Заказы: {{ order_count }}
- Средний чек: {{ avg_order_value }}
- Коэффициент конверсии: {{ conversion_rate }}%

TRAFFIC:
- Посетители: {{ visitor_count }}
- Новые клиенты: {{ new_customers }}
- Вернувшиеся клиенты: {{ returning_customers }}

TOP PRODUCTS:
{% for product in top_products %}
{{ product.rank }}. {{ product.name }} - {{ product.sales }} продаж ({{ product.revenue }})
{% endfor %}

Посмотреть полный отчет: {{ full_report_url }}