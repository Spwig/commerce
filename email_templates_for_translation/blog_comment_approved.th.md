---
template_type: blog_comment_approved
category: Blog
---

# Email Template: blog_comment_approved

## Subject
ความคิดเห็นของคุณใน "{{ post_title }}" ได้รับการอนุมัติแล้ว - {{ blog_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#f0fdf4">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#059669" align="center">
          ✓ ความคิดเห็นได้รับการอนุมัติ
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          สวัสดี {{ commenter_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          ข่าวดี! ความคิดเห็นของคุณใน "{{ post_title }}" ได้รับการอนุมัติแล้ว และตอนนี้ผู้อ่านคนอื่นสามารถเห็นได้แล้ว
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="14px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              ความคิดเห็นของคุณ:
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.6">
              {{ comment_text }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ comment_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          ดูความคิดเห็นของคุณ
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          เราจะแจ้งคุณเมื่อมีคนตอบกลับความคิดเห็นของคุณ
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ ความคิดเห็นได้รับการอนุมัติ

สวัสดี {{ commenter_name }},

ข่าวดี! ความคิดเห็นของคุณใน "{{ post_title }}" ได้รับการอนุมัติแล้ว และตอนนี้ผู้อ่านคนอื่นสามารถเห็นได้แล้ว

ความคิดเห็นของคุณ:
{{ comment_text }}

ดูความคิดเห็นของคุณ: {{ comment_url }}

เราจะแจ้งคุณเมื่อมีคนตอบกลับความคิดเห็นของคุณ
