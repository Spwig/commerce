---
template_type: admin_report_customer_insights
category: Admin Reports
---

# Email Template: admin_report_customer_insights

## Subject
👥 ข้อมูลลูกค้า - {{ report_period }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          👥 ข้อมูลลูกค้า
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ข้อมูลลูกค้า
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>จำนวนลูกค้าทั้งหมด:</strong> {{ total_customers }}<br/>
              <strong>ลูกค้าใหม่:</strong> {{ new_customers }} ({{ new_customer_rate }}%)<br/>
              <strong>อัตราการรักษาลูกค้า:</strong> {{ retention_rate }}%<br/>
              <strong>CLV ค่าเฉลี่ย:</strong> {{ avg_clv }}<br/>
              <strong>อัตราการซื้อซ้ำ:</strong> {{ repeat_purchase_rate }}%
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ข้อมูลเชิงลึก:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ insights }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          ดูรายงานแบบเต็ม
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
👥 ข้อมูลลูกค้า

ข้อมูลลูกค้า

ตัวชี้วัด:
- จำนวนลูกค้าทั้งหมด: {{ total_customers }}
- ลูกค้าใหม่: {{ new_customers }} ({{ new_customer_rate }}%)
- อัตราการรักษาลูกค้า: {{ retention_rate }}%
- CLV ค่าเฉลี่ย: {{ avg_clv }}
- อัตราการซื้อซ้ำ: {{ repeat_purchase_rate }}%

ข้อมูลเชิงลึก:
{{ insights }}

ดูรายงานแบบเต็ม: {{ full_report_url }}