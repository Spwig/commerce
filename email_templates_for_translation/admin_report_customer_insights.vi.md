---
template_type: admin_report_customer_insights
category: Admin Reports
---

# Email Template: admin_report_customer_insights

## Subject
👥 Thông tin khách hàng - {{ report_period }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          👥 Thông tin khách hàng
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Phân tích khách hàng
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Tổng số khách hàng:</strong> {{ total_customers }}<br/>
              <strong>Khách hàng mới:</strong> {{ new_customers }} ({{ new_customer_rate }}%)<br/>
              <strong>Tỷ lệ giữ chân:</strong> {{ retention_rate }}%<br/>
              <strong>CLV trung bình:</strong> {{ avg_clv }}<br/>
              <strong>Tỷ lệ mua hàng lặp lại:</strong> {{ repeat_purchase_rate }}%
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Thông tin:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ insights }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Xem báo cáo đầy đủ
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
👥 THÔNG TIN KHÁCH HÀNG

Phân tích khách hàng

CHỈ SỐ:
- Tổng số khách hàng: {{ total_customers }}
- Khách hàng mới: {{ new_customers }} ({{ new_customer_rate }}%)
- Tỷ lệ giữ chân: {{ retention_rate }}%
- CLV trung bình: {{ avg_clv }}
- Tỷ lệ mua hàng lặp lại: {{ repeat_purchase_rate }}%

THÔNG TIN:
{{ insights }}

Xem báo cáo đầy đủ: {{ full_report_url }}