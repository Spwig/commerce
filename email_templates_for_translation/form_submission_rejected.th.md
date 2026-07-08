---
template_type: form_submission_rejected
category: Form Builder
---

# Email Template: form_submission_rejected

## Subject
อัปเดตเกี่ยวกับการส่งแบบฟอร์ม {{ form_name }} ของคุณ

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          อัปเดตเกี่ยวกับการส่งของคุณ
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          สวัสดี {{ submitter_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          ขอบคุณที่ส่งแบบฟอร์ม {{ form_name }} หลังจากตรวจสอบอย่างรอบคอบ เราไม่สามารถอนุมัติการส่งของคุณได้ในขณะนี้
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              รายละเอียดการส่ง:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>แบบฟอร์ม:</strong> {{ form_name }}<br/>
              <strong>ส่งแล้ว:</strong> {{ submission_date }}<br/>
              <strong>ตรวจสอบแล้ว:</strong> {{ rejection_date }}<br/>
              <strong>เลขอ้างอิง #:</strong> {{ submission_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if rejection_reason %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          เหตุผล:
        </mj-text>
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ rejection_reason }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        {% if can_resubmit %}
        <mj-spacer height="30px" />
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" font-weight="bold">
              คุณสามารถส่งอีกครั้งได้
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ resubmit_instructions }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        {% if resubmit_url %}
        <mj-button href="{{ resubmit_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          ส่งอีกครั้ง
        </mj-button>
        <mj-spacer height="10px" />
        {% endif %}

        {% if support_url %}
        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          ติดต่อฝ่ายสนับสนุน
        </mj-button>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          หากคุณมีคำถามเกี่ยวกับการตัดสินใจนี้ กรุณาอย่าลังเลที่จะติดต่อมา
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
อัปเดตเกี่ยวกับการส่งของคุณ

สวัสดี {{ submitter_name }},

ขอบคุณที่ส่งแบบฟอร์ม {{ form_name }} หลังจากตรวจสอบอย่างรอบคอบ เราไม่สามารถอนุมัติการส่งของคุณได้ในขณะนี้

รายละเอียดการส่ง:
- แบบฟอร์ม: {{ form_name }}
- ส่งแล้ว: {{ submission_date }}
- ตรวจสอบแล้ว: {{ rejection_date }}
- เลขอ้างอิง #: {{ submission_id }}

{% if rejection_reason %}
เหตุผล:
{{ rejection_reason }}
{% endif %}

{% if can_resubmit %}
คุณสามารถส่งอีกครั้งได้:
{{ resubmit_instructions }}
{% endif %}

{% if resubmit_url %}ส่งอีกครั้ง: {{ resubmit_url }}{% endif %}
{% if support_url %}ติดต่อฝ่ายสนับสนุน: {{ support_url }}{% endif %}

หากคุณมีคำถามเกี่ยวกับการตัดสินใจนี้ กรุณาอย่าลังเลที่จะติดต่อมา