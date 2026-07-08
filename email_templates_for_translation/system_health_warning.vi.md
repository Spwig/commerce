---
template_type: system_health_warning
category: System Health
---

# Email Template: system_health_warning

## Subject
⚠️ Cảnh báo sức khỏe hệ thống: {{ metric_name }} - {{ current_value }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Cảnh báo sức khỏe hệ thống
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Vượt ngưỡng cảnh báo
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Một chỉ số sức khỏe hệ thống đã vượt ngưỡng cảnh báo trên cài đặt Spwig của bạn.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Chi tiết cảnh báo:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Chỉ số:</strong> {{ metric_name }}<br/>
              <strong>Giá trị hiện tại:</strong> <span style="color: #d97706; font-weight: bold;">{{ current_value }}</span><br/>
              <strong>Ngưỡng cảnh báo:</strong> {{ warning_threshold }}<br/>
              <strong>Ngưỡng nghiêm trọng:</strong> {{ critical_threshold }}<br/>
              <strong>Phát hiện:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Tác động tiềm tàng:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Các hành động được khuyến nghị:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_actions }}
        </mj-text>

        {% if trend_data %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Phân tích xu hướng:
        </mj-text>
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              {{ trend_data }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              💡 Yêu cầu hành động: Mặc dù chưa nghiêm trọng, nhưng xử lý cảnh báo này ngay bây giờ có thể ngăn ngừa các vấn đề dịch vụ trong tương lai.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Xem bảng điều khiển hệ thống
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ metrics_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Xem chỉ số chi tiết
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ CẢNH BÁO SỨC KHỎE HỆ THỐNG

Vượt ngưỡng cảnh báo

Một chỉ số sức khỏe hệ thống đã vượt ngưỡng cảnh báo trên cài đặt Spwig của bạn.

CHI TIẾT CẢNH BÁO:
- Chỉ số: {{ metric_name }}
- Giá trị hiện tại: {{ current_value }}
- Ngưỡng cảnh báo: {{ warning_threshold }}
- Ngưỡng nghiêm trọng: {{ critical_threshold }}
- Phát hiện: {{ detected_at }}

TÁC ĐỘNG TIỀM TÀNG:
{{ impact_description }}

CÁC HÀNH ĐỘNG ĐƯỢC KHUYÊN NGHỊ:
{{ recommended_actions }}

{% if trend_data %}
PHÂN TÍCH XU HƯỚNG:
{{ trend_data }}
{% endif %}

💡 YÊU CẦU HÀNH ĐỘNG: Mặc dù chưa nghiêm trọng, nhưng xử lý cảnh báo này ngay bây giờ có thể ngăn ngừa các vấn đề dịch vụ trong tương lai.

Xem bảng điều khiển hệ thống: {{ dashboard_url }}
Xem chỉ số chi tiết: {{ metrics_url }}