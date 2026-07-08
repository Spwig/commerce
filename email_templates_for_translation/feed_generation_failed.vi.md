---
template_type: feed_generation_failed
category: Product Feeds
---

# Email Template: feed_generation_failed

## Subject
❌ Việc tạo FEED bị thất bại: {{ feed_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ Việc tạo FEED bị thất bại
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Lỗi tạo
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          FEED sản phẩm {{ feed_name }} đã thất bại do có lỗi.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Chi tiết lỗi:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Feed:</strong> {{ feed_name }}<br/>
              <strong>Thất bại lúc:</strong> {{ failed_at }}<br/>
              <strong>Mã lỗi:</strong> {{ error_code }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Thông báo lỗi:
        </mj-text>

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-family="monospace" color="#991b1b" line-height="1.6">
              {{ error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if error_log %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Lịch sử lỗi:</strong><br/>
          <code style="font-size: 12px; color: #6b7280;">
            {{ error_log|truncatewords:30 }}
          </code>
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Nguyên nhân thường gặp:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Thiếu dữ liệu sản phẩm cần thiết (tiêu đề, giá, hình ảnh)<br/>
          • Định dạng dữ liệu sản phẩm không hợp lệ<br/>
          • Vấn đề kết nối cơ sở dữ liệu<br/>
          • Không gian đĩa hoặc bộ nhớ không đủ
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Thử lại
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Xem cài đặt FEED
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Nếu vấn đề vẫn tồn tại, vui lòng liên hệ với bộ phận hỗ trợ kèm theo mã lỗi {{ error_code }}.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ VIỆC TẠO FEED BỊ THẤT BẠI

Lỗi tạo

FEED sản phẩm {{ feed_name }} đã thất bại do có lỗi.

CHI TIẾT LỖI:
- Feed: {{ feed_name }}
- Thất bại lúc: {{ failed_at }}
- Mã lỗi: {{ error_code }}

THÔNG BÁO LỖI:
{{ error_message }}

{% if error_log %}
LỊCH SỬ LỖI:
{{ error_log|truncatewords:30 }}
{% endif %}

NGUYÊN NHÂN THƯỜNG GẶP:
• Thiếu dữ liệu sản phẩm cần thiết (tiêu đề, giá, hình ảnh)
• Định dạng dữ liệu sản phẩm không hợp lệ
• Vấn đề kết nối cơ sở dữ liệu
• Không gian đĩa hoặc bộ nhớ không đủ

Thử lại: {{ retry_url }}
Xem cài đặt FEED: {{ admin_feed_url }}

Nếu vấn đề vẫn tồn tại, vui lòng liên hệ với bộ phận hỗ trợ kèm theo mã lỗi {{ error_code }}.