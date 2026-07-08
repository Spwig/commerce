---
template_type: translation_job_failed
category: Translation Service
---

# Email Template: translation_job_failed

## Subject
❌ การแปลล้มเหลว: {{ content_type }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ การแปลล้มเหลว
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ข้อผิดพลาดในการแปล
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          งานแปลจำนวนมากของคุณพบข้อผิดพลาดและไม่สามารถดำเนินการได้
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              รายละเอียดงาน:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Job ID:</strong> {{ job_id }}<br/>
              <strong>Content Type:</strong> {{ content_type }}<br/>
              <strong>Target Languages:</strong> {{ target_languages }}<br/>
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

        {% if partial_completion %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              การแปลบางส่วน
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ items_completed }} ของ {{ total_items }} รายการถูกแปลแล้วก่อนที่จะเกิดข้อผิดพลาด
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          สาเหตุที่พบบ่อย:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • ปัญหาการเชื่อมต่อกับ API บริการแปล<br/>
          • จำนวนเครดิตแปลไม่เพียงพอ<br/>
          • ข้อมูลต้นทางไม่ถูกต้องหรือเสียหาย<br/>
          • คู่ภาษาที่ไม่ได้รับการสนับสนุน
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          การกระทำที่แนะนำ:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. ตรวจสอบการตั้งค่าบริการแปลของคุณ<br/>
          2. ตรวจสอบว่ามีเครดิตแปลที่พร้อมใช้งาน<br/>
          3. ตรวจสอบข้อความข้อผิดพลาดเพื่อหาปัญหาเฉพาะ<br/>
          4. ลองแปลงานอีกครั้ง
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          ลองแปลอีกครั้ง
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ settings_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          ตรวจสอบการตั้งค่า
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          หากปัญหายังคงอยู่ โปรดติดต่อฝ่ายสนับสนุนโดยระบุรหัสข้อผิดพลาด {{ error_code }}.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ การแปลล้มเหลว

ข้อผิดพลาดในการแปล

งานแปลจำนวนมากของคุณพบข้อผิดพลาดและไม่สามารถดำเนินการได้

รายละเอียดงาน:
- Job ID: {{ job_id }}
- Content Type: {{ content_type }}
- Target Languages: {{ target_languages }}
- Failed At: {{ failed_at }}
- Error Code: {{ error_code }}

ข้อความข้อผิดพลาด:
{{ error_message }}

{% if partial_completion %}
การแปลบางส่วน:
{{ items_completed }} ของ {{ total_items }} รายการถูกแปลแล้วก่อนที่จะเกิดข้อผิดพลาด
{% endif %}

สาเหตุที่พบบ่อย:
• ปัญหาการเชื่อมต่อกับ API บริการแปล
• จำนวนเครดิตแปลไม่เพียงพอ
• ข้อมูลต้นทางไม่ถูกต้องหรือเสียหาย
• คู่ภาษาที่ไม่ได้รับการสนับสนุน

การกระทำที่แนะนำ:
1. ตรวจสอบการตั้งค่าบริการแปลของคุณ
2. ตรวจสอบว่ามีเครดิตแปลที่พร้อมใช้งาน
3. ตรวจสอบข้อความข้อผิดพลาดเพื่อหาปัญหาเฉพาะ
4. ลองแปลงานอีกครั้ง

ลองแปลอีกครั้ง: {{ retry_url }}
ตรวจสอบการตั้งค่า: {{ settings_url }}

หากปัญหายังคงอยู่ โปรดติดต่อฝ่ายสนับสนุนโดยระบุรหัสข้อผิดพลาด {{ error_code }}.