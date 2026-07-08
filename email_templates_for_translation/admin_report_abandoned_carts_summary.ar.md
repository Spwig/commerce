---
template_type: admin_report_abandoned_carts_summary
category: Admin Reports
---

# Email Template: admin_report_abandoned_carts_summary

## Subject
📊 تقرير السلات المهجورة - {{ abandoned_count }} سلة ({{ abandoned_value }})

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 تقرير السلات المهجورة
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ملخص تجاهل السلات
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>الفترة:</strong> {{ report_period }}<br/>
              <strong>السلات المهجورة:</strong> {{ abandoned_count }}<br/>
              <strong>قيمة السلات المهجورة:</strong> <span style="font-size: 18px; color: #dc2626;">{{ abandoned_value }}</span><br/>
              <strong>معدل التجاهل:</strong> {{ abandonment_rate }}%<br/>
              <strong>معدل الاستعادة:</strong> {{ recovery_rate }}%
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          الأسباب الرائدة (إذا تم تتبعها):
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ top_reasons }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          عرض التفاصيل
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 تقرير السلات المهجورة

ملخص تجاهل السلات

المؤشرات:
- الفترة: {{ report_period }}
- السلات المهجورة: {{ abandoned_count }}
- قيمة السلات المهجورة: {{ abandoned_value }}
- معدل التجاهل: {{ abandonment_rate }}%
- معدل الاستعادة: {{ recovery_rate }}%

الأسباب الرائدة:
{{ top_reasons }}

عرض التفاصيل: {{ full_report_url }}