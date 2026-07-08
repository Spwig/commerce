---
template_type: feed_sync_failed
category: Product Feeds
---

# Email Template: feed_sync_failed

## Subject
❌ Đồng bộ {{ feed_name }} đến {{ platform_name }} thất bại

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ Đồng bộ thất bại
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Lỗi đồng bộ
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Không thể đồng bộ {{ feed_name }} đến {{ platform_name }}.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Chi tiết lỗi:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Feed:</strong> {{ feed_name }}<br/>
              <strong>Mặt nền tảng:</strong> {{ platform_name }}<br/>
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

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Nguyên nhân thường gặp:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Thông tin xác thực API không hợp lệ hoặc mã token đã hết hạn<br/>
          • Vấn đề về kết nối mạng<br/>
          • Đã vượt quá giới hạn tốc độ API của nền tảng<br/>
          • Định dạng Feed không đáp ứng yêu cầu của nền tảng
        </mj-text>

        {% if recommended_action %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Hành động được đề xuất
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ recommended_action }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Thử đồng bộ lại
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ admin_feed_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Kiểm tra thiết lập Feed
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ LỖI ĐỒNG BỘ

Lỗi đồng bộ

Không thể đồng bộ {{ feed_name }} đến {{ platform_name }}.

CHI TIẾT LỖI:
- Feed: {{ feed_name }}
- Nền tảng: {{ platform_name }}
- Thất bại lúc: {{ failed_at }}
- Mã lỗi: {{ error_code }}

THÔNG BÁO LỖI:
{{ error_message }}

NGUYÊN NHÂN THƯỜNG GẶP:
• Thông tin xác thực API không hợp lệ hoặc mã token đã hết hạn
• Vấn đề về kết nối mạng
• Đã vượt quá giới hạn tốc độ API của nền tảng
• Định dạng Feed không đáp ứng yêu cầu của nền tảng

{% if recommended_action %}
HÀNH ĐỘNG ĐƯỢC ĐỀ XUẤT:
{{ recommended_action }}
{% endif %}

Thử đồng bộ lại: {{ retry_url }}
Kiểm tra thiết lập Feed: {{ admin_feed_url }}