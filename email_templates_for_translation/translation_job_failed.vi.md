---
template_type: translation_job_failed
category: Translation Service
---

# Email Template: translation_job_failed

## Subject
❌ Việc dịch thuật thất bại: {{ content_type }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ Việc dịch thuật thất bại
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Lỗi dịch thuật
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Việc dịch thuật theo lô của bạn đã gặp lỗi và không thể hoàn tất.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Chi tiết công việc:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>ID công việc:</strong> {{ job_id }}<br/>
              <strong>Loại nội dung:</strong> {{ content_type }}<br/>
              <strong>Ngôn ngữ đích:</strong> {{ target_languages }}<br/>
              <strong>Thất bại lúc:</strong> {{ failed_at }}<br/>
              <strong>Mã lỗi:</strong> {{ error_code }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Mã lỗi:
        </mj-text>

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" font-family="monospace" color="#991b1b" line-height="1.6">
              {{ error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if partial_completion %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Hoàn thành một phần
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ items_completed }} trong số {{ total_items }} mục đã được dịch thành công trước khi xảy ra lỗi.
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Nguyên nhân thường gặp:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          • Lỗi kết nối API dịch thuật<br/>
          • Thiếu tín dụng dịch thuật<br/>
          • Nội dung nguồn không hợp lệ hoặc bị hỏng<br/>
          • Cặp ngôn ngữ không được hỗ trợ
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Hành động được đề xuất:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Kiểm tra cài đặt dịch thuật của bạn<br/>
          2. Xác nhận tín dụng dịch thuật có sẵn<br/>
          3. Xem xét thông báo lỗi để xác định vấn đề cụ thể<br/>
          4. Thử lại công việc dịch thuật
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Thử lại dịch thuật
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ settings_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Kiểm tra cài đặt
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Nếu vấn đề vẫn tồn tại, vui lòng liên hệ hỗ trợ với mã lỗi {{ error_code }}.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ VIỆC DỊCH THUẬT THẤT BẠI

Lỗi dịch thuật

Việc dịch thuật theo lô của bạn đã gặp lỗi và không thể hoàn tất.

CHI TIẾT CÔNG VIỆC:
- ID công việc: {{ job_id }}
- Loại nội dung: {{ content_type }}
- Ngôn ngữ đích: {{ target_languages }}
- Thất bại lúc: {{ failed_at }}
- Mã lỗi: {{ error_code }}

THÔNG BÁO LỖI:
{{ error_message }}

{% if partial_completion %}
HOÀN THÀNH MỘT PHẦN:
{{ items_completed }} trong số {{ total_items }} mục đã được dịch thành công trước khi xảy ra lỗi.
{% endif %}

NGUYÊN NHÂN THƯỜNG GẶP:
• Lỗi kết nối API dịch thuật
• Thiếu tín dụng dịch thuật
• Nội dung nguồn không hợp lệ hoặc bị hỏng
• Cặp ngôn ngữ không được hỗ trợ

HÀNH ĐỘNG ĐƯỢC ĐỀ XUẤT:
1. Kiểm tra cài đặt dịch thuật của bạn
2. Xác nhận tín dụng dịch thuật có sẵn
3. Xem xét thông báo lỗi để xác định vấn đề cụ thể
4. Thử lại công việc dịch thuật

Thử lại dịch thuật: {{ retry_url }}
Kiểm tra cài đặt: {{ settings_url }}

Nếu vấn đề vẫn tồn tại, vui lòng liên hệ hỗ trợ với mã lỗi {{ error_code }}.