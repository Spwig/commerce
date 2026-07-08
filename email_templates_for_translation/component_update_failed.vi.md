---
template_type: component_update_failed
category: Component Updates
---

# Email Template: component_update_failed

## Subject
❌ Cập nhật thất bại: {{ component_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#991b1b" align="center">
          ❌ Cập nhật thất bại
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Lỗi cài đặt
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Cập nhật {{ component_name }} lên phiên bản {{ target_version }} đã thất bại trong quá trình cài đặt.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Chi tiết lỗi:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Component:</strong> {{ component_name }}<br/>
              <strong>Target Version:</strong> {{ target_version }}<br/>
              <strong>Failed At:</strong> {{ failed_at }}<br/>
              <strong>Error Code:</strong> {{ error_code }}
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
          <strong>Full Error Log:</strong><br/>
          <code style="font-size: 12px; color: #6b7280;">{{ error_log|truncatewords:50 }}</code>
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Hành động cần thực hiện:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          1. Kiểm tra yêu cầu hệ thống và phụ thuộc<br/>
          2. Xem xét nhật ký lỗi để biết chi tiết<br/>
          3. Thử cài đặt lại hoặc liên hệ hỗ trợ<br/>
          4. Cửa hàng của bạn vẫn đang chạy trên phiên bản {{ current_version }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ retry_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Thử cài đặt lại
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Liên hệ hỗ trợ
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
❌ CẬP NHẬT THẤT BẠI

Lỗi cài đặt

Cập nhật {{ component_name }} lên phiên bản {{ target_version }} đã thất bại trong quá trình cài đặt.

CHI TIẾT LỖI:
- Component: {{ component_name }}
- Target Version: {{ target_version }}
- Failed At: {{ failed_at }}
- Error Code: {{ error_code }}

THÔNG BÁO LỖI:
{{ error_message }}

{% if error_log %}
NHẬT KÝ LỖI HOÀN TOÀN:
{{ error_log|truncatewords:50 }}
{% endif %}

HÀNH ĐỘNG CẦN THỰC HIỆN:
1. Kiểm tra yêu cầu hệ thống và phụ thuộc
2. Xem xét nhật ký lỗi để biết chi tiết
3. Thử cài đặt lại hoặc liên hệ hỗ trợ
4. Cửa hàng của bạn vẫn đang chạy trên phiên bản {{ current_version }}

Thử cài đặt lại: {{ retry_url }}
Liên hệ hỗ trợ: {{ support_url }}