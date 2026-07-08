---
template_type: system_health_critical
category: System Health
---

# Email Template: system_health_critical

## Subject
🚨 THÔNG BÁO HỆ THỐNG QUAN TRỌNG: {{ metric_name }} - {{ current_value }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          🚨 THÔNG BÁO HỆ THỐNG QUAN TRỌNG
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Yêu cầu Chú ý Ngay
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Một vấn đề quan trọng về sức khỏe hệ thống đã được phát hiện trên cài đặt Spwig của bạn.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              🚨 Vấn đề Quan trọng
            </mj-text>
            <mj-text color="#991b1b">
              <strong>Thống kê:</strong> {{ metric_name }}<br/>
              <strong>Giá trị Hiện tại:</strong> <span style="font-size: 18px; font-weight: bold;">{{ current_value }}</span><br/>
              <strong>Ngưỡng Quan trọng:</strong> {{ critical_threshold }}<br/>
              <strong>Phát hiện:</strong> {{ detected_at }}<br/>
              <strong>Mức độ:</strong> QUAN TRỌNG
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Tác động:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Các Hành động Ngay lập tức Được Yêu cầu:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_actions }}
        </mj-text>

        {% if trend_data %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Xu hướng:
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

        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Cảnh báo Suy giảm Dịch vụ
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              Vấn đề này có thể gây gián đoạn dịch vụ hoặc suy giảm hiệu suất. Hãy giải quyết ngay để tránh ảnh hưởng đến khách hàng.
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ dashboard_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Xem Bảng Điều khiển Hệ thống
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ logs_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Xem Nhật ký Hệ thống
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 THÔNG BÁO HỆ THỐNG QUAN TRỌNG

Yêu cầu Chú ý Ngay

Một vấn đề quan trọng về sức khỏe hệ thống đã được phát hiện trên cài đặt Spwig của bạn.

🚨 VẤN ĐỀ QUAN TRỌNG:
- Thống kê: {{ metric_name }}
- Giá trị Hiện tại: {{ current_value }}
- Ngưỡng Quan trọng: {{ critical_threshold }}
- Phát hiện: {{ detected_at }}
- Mức độ: QUAN TRỌNG

TÁC ĐỘNG:
{{ impact_description }}

CÁC HÀNH ĐỘNG NGAY LẬP TỨC ĐƯỢC YÊU CẦU:
{{ recommended_actions }}

{% if trend_data %}
XU HƯỚNG:
{{ trend_data }}
{% endif %}

⚠️ CẢNH BÁO SUY GIẢM DỊCH VỤ:
Vấn đề này có thể gây gián đoạn dịch vụ hoặc suy giảm hiệu suất. Hãy giải quyết ngay để tránh ảnh hưởng đến khách hàng.

Xem bảng điều khiển hệ thống: {{ dashboard_url }}
Xem nhật ký hệ thống: {{ logs_url }}