---
template_type: system_health_daily_report
category: System Health
---

# Email Template: system_health_daily_report

## Subject
📊 Báo cáo sức khỏe hệ thống hàng ngày - {{ report_date }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#eff6ff">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#1e40af" align="center">
          📊 Báo cáo sức khỏe hệ thống hàng ngày
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Tóm tắt sức khỏe hệ thống
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Báo cáo sức khỏe hàng ngày cho {{ report_date }}.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Trạng thái tổng thể: {{ overall_status }}
        </mj-text>

        <mj-section background-color="{{ status_color }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" color="#ffffff" font-weight="bold" align="center">
              {{ status_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Chỉ số hệ thống:
        </mj-text>

        {% for metric in metrics %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="15px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ metric.name }}
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Current:</strong> {{ metric.current_value }}<br/>
              <strong>Average (24h):</strong> {{ metric.average }}<br/>
              <strong>Peak:</strong> {{ metric.peak }}<br/>
              <strong>Status:</strong> <span style="color: {{ metric.status_color }};">{{ metric.status }}</span>
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        {% if warnings_count > 0 or critical_count > 0 %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Cảnh báo (24h):
        </mj-text>
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Critical:</strong> <span style="color: #dc2626;">{{ critical_count }}</span><br/>
              <strong>Warnings:</strong> <span style="color: #d97706;">{{ warnings_count }}</span><br/>
              <strong>Resolved:</strong> <span style="color: #059669;">{{ resolved_count }}</span>
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Tóm tắt hiệu năng:
        </mj-text>

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Uptime:</strong> {{ uptime_percentage }}%<br/>
              <strong>Avg Response Time:</strong> {{ avg_response_time }}ms<br/>
              <strong>Slow Requests:</strong> {{ slow_requests_count }}<br/>
              <strong>Errors (500):</strong> {{ errors_500_count }}
            </mj-text>
          </mj-column>
        </mj-section>

        {% if recommendations %}
        <mj-spacer height="30px" />
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Khuyến nghị:
        </mj-text>
        <mj-section background-color="#eff6ff" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#1e40af" line-height="1.6">
              {{ recommendations }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-button href="{{ full_report_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Xem báo cáo đầy đủ
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
📊 BÁO CÁO SỨC KHỎE HỆ THỐNG HÀNG NGÀY

Tóm tắt sức khỏe hệ thống

Báo cáo sức khỏe hàng ngày cho {{ report_date }}.

TRẠNG THÁI TỔNG THỂ: {{ overall_status }}
{{ status_message }}

CHỈ SỐ HỆ THỐNG:
{% for metric in metrics %}
{{ metric.name }}:
- Hiện tại: {{ metric.current_value }}
- Trung bình (24 giờ): {{ metric.average }}
- Đỉnh: {{ metric.peak }}
- Trạng thái: {{ metric.status }}

{% endfor %}

{% if warnings_count > 0 or critical_count > 0 %}
CẢNH BÁO (24 GIỜ):
- Tệ: {{ critical_count }}
- Cảnh báo: {{ warnings_count }}
- Đã giải quyết: {{ resolved_count }}
{% endif %}

TÓM TẮT HIỆU NĂNG:
- Thời gian hoạt động: {{ uptime_percentage }}%
- Thời gian phản hồi trung bình: {{ avg_response_time }}ms
- Yêu cầu chậm: {{ slow_requests_count }}
- Lỗi (500): {{ errors_500_count }}

{% if recommendations %}
KHUYẾN NGHỊ:
{{ recommendations }}
{% endif %}

Xem báo cáo đầy đủ: {{ full_report_url }}