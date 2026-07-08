---
template_type: blog_comment_reply
category: Blog
---

# Email Template: blog_comment_reply

## Subject
「{{ post_title }}」のコメントに{{ replier_name }}が返信しました

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          💬 あなたのコメントへの新しい返信
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          こんにちは {{ commenter_name }}、
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ replier_name }} が 「{{ post_title }}」 のコメントに返信しました。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              あなたのコメント:
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
              {{ replier_name }} が返信しました:
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ reply_text }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ reply_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          見て返信する
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          返信通知を受けたくない場合は <a href="{{ unsubscribe_url }}">退会</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
💬 あなたのコメントへの新しい返信

こんにちは {{ commenter_name }}、

{{ replier_name }} が 「{{ post_title }}」 のコメントに返信しました。

あなたのコメント:
{{ original_comment }}

{{ replier_name }} が返信しました:
{{ reply_text }}

見て返信する: {{ reply_url }}

返信通知を受けたくない場合は、退会: {{ unsubscribe_url }}