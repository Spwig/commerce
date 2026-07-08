---
template_type: admin_report_customer_insights
category: Admin Reports
---

# Email Template: admin_report_customer_insights

## Subject
👥 تقارير العملاء - {{ report_period }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          👥 تقارير العملاء
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          تحليلات العملاء
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>العملاء الإجمالي:</strong> {{ total_customers }}<br/>
              <strong>العملاء الجدد:</strong> {{ new_customers }} ({{ new_customer_rate }}%)<br/>
              <strong>معدل الاحتفاظ:</strong> {{ retention_rate }}%<br/>
              <strong>القيمة المتوسطة للعميل:</strong> {{ avg_clv }}<br/>
              <strong>معدل الشراء المتكرر:</strong> {{ repeat_purchase_rate }}%
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          الإحصائيات:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ insights }}
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
تقارير العملاء

تحليلات العملاء

المؤشرات:
- العملاء الإجمالي: {{ total_customers }}
- العملاء الجدد: {{ new_customers }} ({{ new_customer_rate }}%)
- معدل الاحتفاظ: {{ retention_rate }}%
- القيمة المتوسطة للعميل: {{ avg_clv }}
- معدل الشراء المتكرر: {{ repeat_purchase_rate }}%

الإحصائيات:
{{ insights }}

عرض التقرير الكامل: {{ full_report_url }}