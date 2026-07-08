---
template_type: component_rollback_success
category: Component Updates
---

# Email Template: component_rollback_success

## Subject
✓ {{ component_name }} đã được quay lại phiên bản v{{ previous_version }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dbeafe">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          ↩️ Quay lại hoàn tất
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Thành phần đã được khôi phục
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ component_name }} đã được quay lại thành công về phiên bản trước.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Chi tiết quay lại:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Thành phần:</strong> {{ component_name }}<br/>
              <strong>Quay lại từ:</strong> v{{ failed_version }}<br/>
              <strong>Khôi phục đến:</strong> v{{ previous_version }}<br/>
              <strong>Hoàn thành:</strong> {{ completed_at }}<br/>
              <strong>Thời gian:</strong> {{ rollback_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if rollback_reason %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Lý do quay lại:
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ rollback_reason }}
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#065f46" font-weight="bold">
              ✓ Trạng thái cửa hàng
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.6">
              Cửa hàng của bạn hiện đang chạy trên phiên bản ổn định {{ previous_version }}. Tất cả các chức năng nên đã được khôi phục.
            </mj-text>
          </mj-column>
        </mj-section>

        {% if data_restored %}
        <mj-spacer height="20px" />
        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Khôi phục dữ liệu:</strong> {{ data_restoration_message }}
        </mj-text>
        {% endif %}

        {% if next_steps %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Các bước tiếp theo:
        </mj-text>
        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ next_steps }}
        </mj-text>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ component_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Xem chi tiết thành phần
        </mj-button>

        {% if incident_report_url %}
        <mj-spacer height="10px" />
        <mj-button href="{{ incident_report_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Xem báo cáo sự cố
        </mj-button>
        {% endif %}

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Nếu bạn tiếp tục gặp vấn đề, vui lòng liên hệ hỗ trợ.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
↩️ QUAY LẠI HOÀN TẤT

Thành phần đã được khôi phục

{{ component_name }} đã được quay lại thành công về phiên bản trước.

CHI TIẾT QUAY LẠI:
- Thành phần: {{ component_name }}
- Quay lại từ: v{{ failed_version }}
- Khôi phục đến: v{{ previous_version }}
- Hoàn thành: {{ completed_at }}
- Thời gian: {{ rollback_duration }}

{% if rollback_reason %}
LÝ DO QUAY LẠI:
{{ rollback_reason }}
{% endif %}

✓ TRẠNG THÁI CỬA HÀNG:
Cửa hàng của bạn hiện đang chạy trên phiên bản ổn định {{ previous_version }}. Tất cả các chức năng nên đã được khôi phục.

{% if data_restored %}
KHÔI PHỤC DỮ LIỆU: {{ data_restoration_message }}
{% endif %}

{% if next_steps %}
CÁC BƯỚC TIẾP THEO:
{{ next_steps }}
{% endif %}

Xem chi tiết thành phần: {{ component_url }}
{% if incident_report_url %}Xem báo cáo sự cố: {{ incident_report_url }}{% endif %}

Nếu bạn tiếp tục gặp vấn đề, vui lòng liên hệ hỗ trợ.