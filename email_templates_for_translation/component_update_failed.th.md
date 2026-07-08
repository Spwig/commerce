---
template_type: component_update_failed
category: Component Updates
---

# Email Template: component_update_failed

## Subject
❌ การอัปเดตล้มเหลว: {{ component_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ การอัปเดตล้มเหลว
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          การติดตั้งข้อผิดพลาด
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          การอัปเดตสำหรับ {{ component_name }} ไปยังเวอร์ชัน {{ target_version }} ล้มเหลวในการติดตั้ง
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              รายละเอียดความล้มเหลว:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>ส่วนประกอบ:</strong> {{ component_name }}<br/>
              <strong>เวอร์ชันเป้าหมาย:</strong> {{ target_version }}<br/>
              <strong>ล้มเหลวที่:</strong> {{ failed_at }}<br/>
              <strong>รหัสข้อผิดพลาด:</strong> {{ error_code }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ข้อความข้อผิดพลาด:
        </mj-text>

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-family="monospace" color="#991b1b" line-height="1.6">
              {{ error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if error_log %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>บันทึกข้อผิดพลาดทั้งหมด:</strong><br/>
          <code style="font-size: 12px; color: #6b7280;">
            {{ error_log|truncatewords:50 }}
          </code>
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          สิ่งที่ควรทำ:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. ตรวจสอบข้อกำหนดระบบและขึ้นอยู่กับ<br/>
          2. ตรวจสอบบันทึกข้อผิดพลาดสำหรับรายละเอียด<br/>
          3. ลองติดตั้งอีกครั้ง หรือติดต่อฝ่ายสนับสนุน<br/>
          4. ร้านค้าของคุณยังคงทำงานบน {{ current_version }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          ลองติดตั้งอีกครั้ง
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          ติดต่อฝ่ายสนับสนุน
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ การอัปเดตล้มเหลว

ข้อผิดพลาดการติดตั้ง

การอัปเดตสำหรับ {{ component_name }} ไปยังเวอร์ชัน {{ target_version }} ล้มเหลวในการติดตั้ง

รายละเอียดความล้มเหลว:
- ส่วนประกอบ: {{ component_name }}
- เวอร์ชันเป้าหมาย: {{ target_version }}
- ล้มเหลวที่: {{ failed_at }}
- รหัสข้อผิดพลาด: {{ error_code }}

ข้อความข้อผิดพลาด:
{{ error_message }}

{% if error_log %}
บันทึกข้อผิดพลาดทั้งหมด:
{{ error_log|truncatewords:50 }}
{% endif %}

สิ่งที่ควรทำ:
1. ตรวจสอบข้อกำหนดระบบและขึ้นอยู่กับ
2. ตรวจสอบบันทึกข้อผิดพลาดสำหรับรายละเอียด
3. ลองติดตั้งอีกครั้ง หรือติดต่อฝ่ายสนับสนุน
4. ร้านค้าของคุณยังคงทำงานบน {{ current_version }}

ลองติดตั้งอีกครั้ง: {{ retry_url }}
ติดต่อฝ่ายสนับสนุน: {{ support_url }}