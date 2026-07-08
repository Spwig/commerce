---
template_type: component_incompatible_warning
category: Component Updates
---

# Email Template: component_incompatible_warning

## Subject
⚠️ Lỗi Tương thích: {{ component_name }} và {{ conflicting_component }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Lỗi Tương thích
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Xung đột Phiên bản Được Phát hiện
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Một vấn đề tương thích đã được phát hiện giữa các thành phần trong cửa hàng Spwig của bạn.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Chi Tiết Xung Đột:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Thành phần 1:</strong> {{ component_name }} v{{ component_version }}<br/>
              <strong>Thành phần 2:</strong> {{ conflicting_component }} v{{ conflicting_version }}<br/>
              <strong>Phát hiện:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Vấn đề Tương thích:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ incompatibility_description }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#991b1b" font-weight="bold">
              Tác động Có thể xảy ra
            </mj-text>
            <mj-text font-size="14px" color="#991b1b" line-height="1.6">
              {{ impact_description }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Hành động Được Khuyến nghị:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_action }}
        </mj-text>

        {% if compatible_versions %}
        <mj-spacer height="30px" />
        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" font-weight="bold">
              Các Phiên bản Tương thích
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              {{ compatible_versions }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        {% if update_url %}
        <mj-button href="{{ update_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Giải Quyết Xung Đột
        </mj-button>
        <mj-spacer height="10px" />
        {% endif %}

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Liên Hệ Hỗ Trợ
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Cửa hàng của bạn vẫn đang hoạt động, nhưng chúng tôi khuyến nghị bạn giải quyết xung đột này sớm.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ CẢNH BÁO TƯƠNG THÍCH

Xung đột Phiên bản Được Phát hiện

Một vấn đề tương thích đã được phát hiện giữa các thành phần trong cửa hàng Spwig của bạn.

CHI TIẾT XUNG ĐỘT:
- Thành phần 1: {{ component_name }} v{{ component_version }}
- Thành phần 2: {{ conflicting_component }} v{{ conflicting_version }}
- Phát hiện: {{ detected_at }}

VẤN ĐỀ TƯƠNG THÍCH:
{{ incompatibility_description }}

TÁC ĐỘNG CÓ THỂ XẢY RA:
{{ impact_description }}

HÀNH ĐỘNG ĐƯỢC KHUYẾN NGHỊ:
{{ recommended_action }}

{% if compatible_versions %}CÁC PHIÊN BẢN TƯƠNG THÍCH:
{{ compatible_versions }}
{% endif %}

{% if update_url %}Giải quyết xung đột: {{ update_url }}{% endif %}
Liên hệ hỗ trợ: {{ support_url }}

Cửa hàng của bạn vẫn đang hoạt động, nhưng chúng tôi khuyến nghị bạn giải quyết xung đột này sớm.