---
template_type: admin_report_abandoned_carts_summary
category: Admin Reports
---

# Email Template: admin_report_abandoned_carts_summary

## Subject
📊 Báo cáo giỏ hàng bị bỏ rơi - {{ abandoned_count }} giỏ hàng ({{ abandoned_value }})

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Báo cáo giỏ hàng bị bỏ rơi
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Tổng quan giỏ hàng bị bỏ rơi
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Thời kỳ:</strong> {{ report_period }}<br/>
              <strong>Số giỏ hàng bị bỏ rơi:</strong> {{ abandoned_count }}<br/>
              <strong>Giá trị bị bỏ rơi:</strong> <span style="font-size: 18px; color: #dc2626;">{{ abandoned_value }}</span><br/>
              <strong>Tỷ lệ bỏ rơi:</strong> {{ abandonment_rate }}%<br/>
              <strong>Tỷ lệ phục hồi:</strong> {{ recovery_rate }}%
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Lý do hàng đầu (nếu được theo dõi):
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ top_reasons }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Xem chi tiết
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 BÁO CÁO GIỎ HÀNG BỊ BỎ RỜI

Tổng quan giỏ hàng bị bỏ rơi

METRICS:
- Thời kỳ: {{ report_period }}
- Số giỏ hàng bị bỏ rơi: {{ abandoned_count }}
- Giá trị bị bỏ rơi: {{ abandoned_value }}
- Tỷ lệ bỏ rơi: {{ abandonment_rate }}%
- Tỷ lệ phục hồi: {{ recovery_rate }}%

LÝ DO HÀNG ĐẦU:
{{ top_reasons }}

Xem chi tiết: {{ full_report_url }}