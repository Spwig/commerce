---
template_type: blog_comment_approved
category: Blog
---

# Email Template: blog_comment_approved

## Subject
Bình luận của bạn trên "{{ post_title }}" đã được duyệt - {{ blog_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#f0fdf4">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#059669" align="center">
          ✓ Bình luận đã được duyệt
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Chào {{ commenter_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Tin vui! Bình luận của bạn trên "{{ post_title }}" đã được duyệt và hiện đang hiển thị cho các độc giả khác.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="14px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Bình luận của bạn:
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.6">
              {{ comment_text }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ comment_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Xem bình luận của bạn
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          Chúng tôi sẽ thông báo cho bạn khi ai đó trả lời bình luận của bạn.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ BÌNH LUẬN ĐÃ ĐƯỢC DUYỆT

Chào {{ commenter_name }},

Tin vui! Bình luận của bạn trên "{{ post_title }}" đã được duyệt và hiện đang hiển thị cho các độc giả khác.

BÌNH LUẬN CỦA BẠN:
{{ comment_text }}

Xem bình luận của bạn: {{ comment_url }}

Chúng tôi sẽ thông báo cho bạn khi ai đó trả lời bình luận của bạn.