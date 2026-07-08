---
template_type: blog_comment_reply
category: Blog
---

# Email Template: blog_comment_reply

## Subject
 {{ replier_name }} 回复了你在“{{ post_title }}”的评论

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          💬 你有一条新回复
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          你好 {{ commenter_name }}，
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ replier_name }} 回复了你在“{{ post_title }}”的评论。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              你的评论：
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
              {{ replier_name }} 回复：
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ reply_text }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ reply_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          查看并回复
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          不想接收回复通知？<a href="{{ unsubscribe_url }}">退订</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
💬 新回复到你的评论

你好 {{ commenter_name }}，

{{ replier_name }} 回复了你在“{{ post_title }}”的评论。

你的评论：
{{ original_comment }}

{{ replier_name }} 回复：
{{ reply_text }}

查看并回复：{{ reply_url }}

不想接收回复通知？退订：{{ unsubscribe_url }}