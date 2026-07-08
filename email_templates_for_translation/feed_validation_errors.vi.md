---
template_type: feed_validation_errors
category: Product Feeds
---

# Email Template: feed_validation_errors

## Subject
⚠️ {{ feed_name }}: Đã tìm thấy {{ error_count }} lỗi xác thực

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Feed Lỗi Xác thực
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Các vấn đề chất lượng dữ liệu được phát hiện
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Đã tìm thấy {{ error_count }} lỗi xác thực{{ error_count|pluralize }} trong {{ feed_name }}. Những vấn đề này có thể ngăn sản phẩm hiển thị trên {{ platform_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Tóm tắt xác thực:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Feed:</strong> {{ feed_name }}<br/>
              <strong>Nền tảng:</strong> {{ platform_name }}<br/>
              <strong>Xác thực:</strong> {{ validated_at }}<br/>
              <strong>Tổng số sản phẩm:</strong> {{ total_products }}<br/>
              <strong>Sản phẩm có lỗi:</strong> {{ affected_products }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Lỗi hàng đầu:
        </mj-text>

        {% for error in top_errors %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" font-weight="bold">
              {{ error.type }}
            </mj-text>
            <mj-text font-size="13px" color="#991b1b">
              {{ error.count }} sản phẩm{{ error.count|pluralize }} bị ảnh hưởng: {{ error.message }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Điều gì cần sửa:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ fix_instructions }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ errors_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Xem tất cả lỗi
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Quản lý Feed
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Sửa các lỗi này để đảm bảo tất cả sản phẩm xuất hiện trên {{ platform_name }}.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ LỖI XÁC THỰC FEED

Các vấn đề chất lượng dữ liệu được phát hiện

Đã tìm thấy {{ error_count }} lỗi xác thực{{ error_count|pluralize }} trong {{ feed_name }}. Những vấn đề này có thể ngăn sản phẩm hiển thị trên {{ platform_name }}.

TÓM TẮT XÁC THỰC:
- Feed: {{ feed_name }}
- Nền tảng: {{ platform_name }}
- Xác thực: {{ validated_at }}
- Tổng số sản phẩm: {{ total_products }}
- Sản phẩm có lỗi: {{ affected_products }}

LỖI HÀNG ĐẦU:
{% for error in top_errors %}
{{ error.type }}: {{ error.count }} sản phẩm{{ error.count|pluralize }} - {{ error.message }}
{% endfor %}

ĐIỀU GÌ CẦN SỬA:
{{ fix_instructions }}

Xem tất cả lỗi: {{ errors_url }}
Quản lý feed: {{ admin_feed_url }}

Sửa các lỗi này để đảm bảo tất cả sản phẩm xuất hiện trên {{ platform_name }}.