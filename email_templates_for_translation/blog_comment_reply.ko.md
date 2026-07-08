---
template_type: blog_comment_reply
category: Blog
---

# Email Template: blog_comment_reply

## Subject
💬 {{ replier_name }}가 '{{ post_title }}'에 작성한 댓글에 답변했습니다

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          💬 댓글에 대한 새로운 답변
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          안녕하세요 {{ commenter_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ replier_name }}가 '{{ post_title }}'에 작성한 댓글에 답변했습니다.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              당신의 댓글:
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ original_comment }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="15px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-weight="bold" color="#065f46">
              {{ replier_name }}가 답변했습니다:
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ reply_text }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ reply_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          보기 및 답변
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          답변 알림을 원하지 않으십니까? <a href="{{ unsubscribe_url }}">구독 해지</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
💬 댓글에 대한 새로운 답변

안녕하세요 {{ commenter_name }},

{{ replier_name }}가 '{{ post_title }}'에 작성한 댓글에 답변했습니다.

당신의 댓글:
{{ original_comment }}

{{ replier_name }}가 답변했습니다:
{{ reply_text }}

보기 및 답변: {{ reply_url }}

답변 알림을 원하지 않으십니까? 구독 해지: {{ unsubscribe_url }}

