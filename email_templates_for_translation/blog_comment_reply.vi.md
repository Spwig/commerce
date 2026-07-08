---
template_type: blog_comment_reply
category: Blog
---

# Email Template: blog_comment_reply

## Subject
 {{ replier_name }} đã trả lời bình luận của bạn trên "{{ post_title }}"

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          💬 Trả lời mới cho bình luận của bạn
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hi {{ commenter_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ replier_name }} đã trả lời bình luận của bạn trên "{{ post_title }}".
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              Bình luận của bạn:
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
              {{ replier_name }} đã trả lời:
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ reply_text }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ reply_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Xem và trả lời
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Không muốn nhận thông báo trả lời? <a href="{{ unsubscribe_url }}">Hủy đăng ký</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
💬 TRẢ LỜI MỚI CHO BÌNH LUẬN CỦA BẠN

Hi {{ commenter_name }},

{{ replier_name }} đã trả lời bình luận của bạn trên "{{ post_title }}".

BÌNH LUẬN CỦA BẠN:
{{ original_comment }}

{{ replier_name }} ĐÃ TRẢ LỜI:
{{ reply_text }}

Xem và trả lời: {{ reply_url }}

Không muốn nhận thông báo trả lời? Hủy đăng ký: {{ unsubscribe_url }}
