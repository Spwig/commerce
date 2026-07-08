---
template_type: component_security_update
category: Component Updates
---

# Email Template: component_security_update

## Subject
🔒 KHẨN: Cập nhật bảo mật có sẵn cho {{ component_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          🔒 CẬP NHẬT BẢO MẬT CẦN THIẾT
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Bổ丁 Bảo Mật Quan Trọng
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Một lỗ hổng bảo mật đã được phát hiện trong {{ component_name }}. Vui lòng cập nhật ngay lập tức để bảo vệ cửa hàng của bạn.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              ⚠️ Thông Tin Bảo Mật
            </mj-text>
            <mj-text color="#991b1b">
              <strong>Thành phần:</strong> {{ component_name }}<br/>
              <strong>Phiên bản hiện tại:</strong> {{ current_version }}<br/>
              <strong>Phiên bản đã vá:</strong> {{ patched_version }}<br/>
              <strong>Mức độ nghiêm trọng:</strong> {{ severity_level }}<br/>
              <strong>ID CVE:</strong> {{ cve_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Chi tiết lỗ hổng:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ vulnerability_description }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Tác động tiềm tàng:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        {% if mitigation_steps %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              Giảm thiểu tạm thời
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ mitigation_steps }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          Hành động cần thiết: Cài đặt cập nhật ngay lập tức
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ update_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Cài đặt vá bảo mật
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ advisory_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Đọc thông báo bảo mật
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Nếu bạn cần hỗ trợ, vui lòng liên hệ ngay với bộ phận hỗ trợ của Spwig.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔒 CẬP NHẬT BẢO MẬT CẦN THIẾT

Bổ丁 Bảo Mật Quan Trọng

Một lỗ hổng bảo mật đã được phát hiện trong {{ component_name }}. Vui lòng cập nhật ngay lập tức để bảo vệ cửa hàng của bạn.

⚠️ THÔNG TIN BẢO MẬT:
- Thành phần: {{ component_name }}
- Phiên bản hiện tại: {{ current_version }}
- Phiên bản đã vá: {{ patched_version }}
- Mức độ nghiêm trọng: {{ severity_level }}
- ID CVE: {{ cve_id }}

CHI TIẾT LỖ HỔNG:
{{ vulnerability_description }}

TÁC ĐỘNG TIỀM TÀNG:
{{ impact_description }}

{% if mitigation_steps %}
GIẢM THIỂU TẠM THỜI:
{{ mitigation_steps }}
{% endif %}

HÀNH ĐỘNG CẦN THIẾT: CÀI ĐẶT CẬP NHẬT NGAY LẬP TỨC

Cài đặt vá bảo mật: {{ update_url }}
Đọc thông báo bảo mật: {{ advisory_url }}

Nếu bạn cần hỗ trợ, vui lòng liên hệ ngay với bộ phận hỗ trợ của Spwig.