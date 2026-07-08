---
template_type: blog_comment_approved
category: Blog
---

# Email Template: blog_comment_approved

## Subject
“{{ post_title }}”에 대한 귀하의 댓글이 승인되었습니다 - {{ blog_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#f0fdf4">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#059669" align="center">
          ✓ 댓글 승인됨
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          안녕하세요 {{ commenter_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          기쁜 소식입니다! “{{ post_title }}”에 대한 귀하의 댓글이 승인되었으며, 이제 다른 독자들에게도 보입니다.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="14px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              귀하의 댓글:
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.6">
              {{ comment_text }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ comment_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          댓글 보기
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          귀하의 댓글에 대한 답변이 있을 경우 알려드릴 것입니다.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ 댓글 승인됨

안녕하세요 {{ commenter_name }},

기쁜 소식입니다! “{{ post_title }}”에 대한 귀하의 댓글이 승인되었으며, 이제 다른 독자들에게도 보입니다.

귀하의 댓글:
{{ comment_text }}

댓글 보기: {{ comment_url }}

귀하의 댓글에 대한 답변이 있을 경우 알려드릴 것입니다.