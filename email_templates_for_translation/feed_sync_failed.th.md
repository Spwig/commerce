---
template_type: feed_sync_failed
category: Product Feeds
---

# Email Template: feed_sync_failed

## Subject
❌ การซิงค์ {{ feed_name }} ไปยัง {{ platform_name }} ล้มเหลว

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ ซิงค์ล้มเหลว
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ข้อผิดพลาดการซิงค์
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          การซิงค์ {{ feed_name }} ไปยัง {{ platform_name }} ล้มเหลว
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              รายละเอียดความล้มเหลว:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Feed:</strong> {{ feed_name }}<br/>
              <strong>Platform:</strong> {{ platform_name }}<br/>
              <strong>Failed At:</strong> {{ failed_at }}<br/>
              <strong>Error Code:</strong> {{ error_code }}
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

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          สาเหตุทั่วไป:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • ข้อมูล API ไม่ถูกต้องหรือโทเคนหมดอายุ<br/>
          • ปัญหาการเชื่อมต่อเครือข่าย<br/>
          • ขีดจำกัดอัตราการเรียกใช้ API ของแพลตฟอร์มเกิน<br/>
          • รูปแบบ Feed ไม่ตรงตามข้อกำหนดของแพลตฟอร์ม
        </mj-text>

        {% if recommended_action %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              การดำเนินการที่แนะนำ
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ recommended_action }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          ลองซิงค์อีกครั้ง
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          ตรวจสอบการตั้งค่า Feed
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ การซิงค์ล้มเหลว

ข้อผิดพลาดการซิงค์

การซิงค์ {{ feed_name }} ไปยัง {{ platform_name }} ล้มเหลว

รายละเอียดความล้มเหลว:
- Feed: {{ feed_name }}
- Platform: {{ platform_name }}
- Failed At: {{ failed_at }}
- Error Code: {{ error_code }}

ข้อความข้อผิดพลาด:
{{ error_message }}

สาเหตุทั่วไป:
• ข้อมูล API ไม่ถูกต้องหรือโทเคนหมดอายุ
• ปัญหาการเชื่อมต่อเครือข่าย
• ขีดจำกัดอัตราการเรียกใช้ API ของแพลตฟอร์มเกิน
• รูปแบบ Feed ไม่ตรงตามข้อกำหนดของแพลตฟอร์ม

{% if recommended_action %}
การดำเนินการที่แนะนำ:
{{ recommended_action }}
{% endif %}

ลองซิงค์อีกครั้ง: {{ retry_url }}
ตรวจสอบการตั้งค่า Feed: {{ admin_feed_url }}