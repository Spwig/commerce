---
template_type: blog_subscriber_welcome
category: Blog
---

# Email Template: blog_subscriber_welcome

## Subject
Chào mừng đến với {{ blog_name }}! 🎉

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 Chào mừng đến với {{ blog_name }}!
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Chào {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Cảm ơn bạn đã đăng ký! Chúng tôi rất vui được chia sẻ nội dung mới nhất của chúng tôi với bạn.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="#065f46">
              Điều gì bạn có thể mong đợi:
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.8">
              ✓ Các bài đăng mới sẽ được gửi đến hộp thư của bạn<br/>
              ✓ Nội dung độc quyền chỉ dành cho người đăng ký<br/>
              ✓ {{ publish_frequency }} cập nhật<br/>
              ✓ Không có spam, hủy đăng ký bất kỳ lúc nào
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Bắt đầu đọc:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Xem các bài viết phổ biến nhất của chúng tôi:
        </mj-text>

        <mj-spacer height="15px" />

        {% for post in popular_posts %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column width="30%">
            <mj-image src="{{ post.featured_image }}" alt="{{ post.title }}" border-radius="4px" />
          </mj-column>
          <mj-column width="70%">
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ post.title }}
            </mj-text>
            <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              {{ post.reading_time }} phút đọc
            </mj-text>
            <mj-text font-size="14px">
              <a href="{{ post.url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">Đọc ngay →</a>
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ blog_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Khám phá tất cả các bài viết
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Quản lý đăng ký của bạn: <a href="{{ preferences_url }}">Thay đổi email</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 CHÀO MỪNG ĐẾN VỚI {{ blog_name }}!

Chào {{ subscriber_name }},

Cảm ơn bạn đã đăng ký! Chúng tôi rất vui được chia sẻ nội dung mới nhất của chúng tôi với bạn.

ĐIỀU GÌ BẠN CÓ THỂ MONG ĐỢI:
✓ Các bài đăng mới sẽ được gửi đến hộp thư của bạn
✓ Nội dung độc quyền chỉ dành cho người đăng ký
✓ {{ publish_frequency }} cập nhật
✓ Không có spam, hủy đăng ký bất kỳ lúc nào

BẮT ĐẦU ĐỌC - BÀI VIẾT PHỔ BIẾN:
{% for post in popular_posts %}
- {{ post.title }} ({{ post.reading_time }} phút đọc)
  {{ post.url }}
{% endfor %}

Khám phá tất cả các bài viết: {{ blog_url }}

Quản lý đăng ký của bạn: {{ preferences_url }}