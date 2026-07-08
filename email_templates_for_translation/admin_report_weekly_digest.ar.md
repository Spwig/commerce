---
template_type: admin_report_weekly_digest
category: Admin Reports
---

# Email Template: admin_report_weekly_digest

## Subject
📈 ملخص أسبوعي - {{ week_range }} - {{ total_revenue }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📈 ملخص أسبوعي
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          الأسبوع من {{ week_range }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>الإيرادات:</strong> <span style="font-size: 20px; color: #059669;">{{ total_revenue }}</span> ({{ revenue_change }})<br/>
              <strong>الطلبات:</strong> {{ total_orders }} ({{ orders_change }})<br/>
              <strong>العملاء الجدد:</strong> {{ new_customers }}<br/>
              <strong>قيمة الطلب المتوسطة:</strong> {{ avg_order_value }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          النقاط البارزة:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ highlights }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          عرض التقرير الكامل
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📈 ملخص أسبوعي

الأسبوع من {{ week_range }}

الأداء:
- الإيرادات: {{ total_revenue }} ({{ revenue_change }})
- الطلبات: {{ total_orders }} ({{ orders_change }})
- العملاء الجدد: {{ new_customers }}
- قيمة الطلب المتوسطة: {{ avg_order_value }}

النقاط البارزة:
{{ highlights }}

عرض التقرير الكامل: {{ full_report_url }}