---
template_type: admin_report_customer_insights
category: Admin Reports
---

# Email Template: admin_report_customer_insights

## Subject
👥 Инсайты клиентов - {{ report_period }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          👥 Инсайты клиентов
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Информация о клиентах
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Общее количество клиентов:</strong> {{ total_customers }}<br/>
              <strong>Новые клиенты:</strong> {{ new_customers }} ({{ new_customer_rate }}%)<br/>
              <strong>Коэффициент удержания:</strong> {{ retention_rate }}%<br/>
              <strong>Среднее CLV:</strong> {{ avg_clv }}<br/>
              <strong>Доля повторных покупок:</strong> {{ repeat_purchase_rate }}%
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Инсайты:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ insights }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Посмотреть полный отчет
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
👥 ИНСАЙТЫ КЛИЕНТОВ

Информация о клиентах

МЕТРИКИ:
- Общее количество клиентов: {{ total_customers }}
- Новые клиенты: {{ new_customers }} ({{ new_customer_rate }}%)
- Коэффициент удержания: {{ retention_rate }}%
- Среднее CLV: {{ avg_clv }}
- Доля повторных покупок: {{ repeat_purchase_rate }}%

ИНСАЙТЫ:
{{ insights }}

Посмотреть полный отчет: {{ full_report_url }}