---
template_type: component_update_available
category: Component Updates
---

# Email Template: component_update_available

## Subject
Cập Nhật Có Thể Tải Về: {{ component_name }} v{{ new_version }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📦 Cập Nhật Có Thể Tải Về
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Phiên Bản Mới Có Thể Tải Về
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Một phiên bản mới của {{ component_name }} đã có sẵn cho cửa hàng Spwig của bạn.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Chi Tiết Cập Nhật:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Component:</strong> {{ component_name }}<br/>
              <strong>Phiên Bản Hiện Tại:</strong> {{ current_version }}<br/>
              <strong>Phiên Bản Mới:</strong> {{ new_version }}<br/>
              <strong>Ngày Phát Hành:</strong> {{ release_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Những Điều Mới:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ changelog }}
        </mj-text>

        {% if breaking_changes %}
        <mj-spacer height="20px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Những Thay Đổi Gây Tác Động
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ breaking_changes }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ update_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Cài Đặt Cập Nhật
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          <a href="{{ changelog_url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">
            Xem Toàn Bộ Nhật Ký Thay Đổi
          </a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📦 CẬP NHẬT CÓ THỂ TẢI VỀ

Phiên Bản Mới Có Thể Tải Về

Một phiên bản mới của {{ component_name }} đã có sẵn cho cửa hàng Spwig của bạn.

CHI TIẾT CẬP NHẬT:
- Component: {{ component_name }}
- Phiên Bản Hiện Tại: {{ current_version }}
- Phiên Bản Mới: {{ new_version }}
- Ngày Phát Hành: {{ release_date }}

NHỮNG ĐIỀU MỚI:
{{ changelog }}

{% if breaking_changes %}
⚠️ NHỮNG THAY ĐỔI GÂY TÁC ĐỘNG:
{{ breaking_changes }}
{% endif %}

Cài đặt cập nhật: {{ update_url }}
Xem toàn bộ nhật ký thay đổi: {{ changelog_url }}