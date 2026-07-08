---
template_type: system_health_critical
category: System Health
---

# Email Template: system_health_critical

## Subject
🚨 การแจ้งเตือนระบบสำคัญ: {{ metric_name }} - {{ current_value }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          🚨 การแจ้งเตือนระบบสำคัญ
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ต้องการความสนใจทันที
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          พบปัญหาความเสถียรของระบบสำคัญในระบบ Spwig ของคุณ
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              🚨 ปัญหาสำคัญ
            </mj-text>
            <mj-text color="#991b1b">
              <strong>ตัวชี้วัด:</strong> {{ metric_name }}<br/>
              <strong>ค่าปัจจุบัน:</strong> <span style="font-size: 18px; font-weight: bold;">{{ current_value }}</span><br/>
              <strong>เกณฑ์สำคัญ:</strong> {{ critical_threshold }}<br/>
              <strong>ตรวจพบ:</strong> {{ detected_at }}<br/>
              <strong>ความรุนแรง:</strong> สำคัญ
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ผลกระทบ:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ขั้นตอนที่ต้องดำเนินการทันที:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_actions }}
        </mj-text>

        {% if trend_data %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          แนวโน้ม:
        </mj-text>
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ trend_data }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ การเตือนการลดระดับบริการ
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              ปัญหานี้อาจทำให้เกิดการขัดข้องหรือการลดระดับประสิทธิภาพของบริการ โปรดแก้ไขทันทีเพื่อป้องกันผลกระทบต่อลูกค้า
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ dashboard_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          ดูแดชบอร์ดระบบ
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ logs_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          ดูบันทึกระบบ
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 การแจ้งเตือนระบบสำคัญ

ต้องการความสนใจทันที

พบปัญหาความเสถียรของระบบสำคัญในระบบ Spwig ของคุณ

🚨 ปัญหาสำคัญ:
- ตัวชี้วัด: {{ metric_name }}
- ค่าปัจจุบัน: {{ current_value }}
- เกณฑ์สำคัญ: {{ critical_threshold }}
- ตรวจพบ: {{ detected_at }}
- ความรุนแรง: สำคัญ

ผลกระทบ:
{{ impact_description }}

ขั้นตอนที่ต้องดำเนินการทันที:
{{ recommended_actions }}

{% if trend_data %}
แนวโน้ม:
{{ trend_data }}
{% endif %}

⚠️ การเตือนการลดระดับบริการ:
นี้อาจทำให้เกิดการขัดข้องหรือการลดระดับประสิทธิภาพของบริการ โปรดแก้ไขทันทีเพื่อป้องกันผลกระทบต่อลูกค้า

ดูแดชบอร์ดระบบ: {{ dashboard_url }}
ดูบันทึกระบบ: {{ logs_url }}