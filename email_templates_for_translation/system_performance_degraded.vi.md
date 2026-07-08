---
template_type: system_performance_degraded
category: System Health
---

# Email Template: system_performance_degraded

## Subject
⚠️ Phát hiện suy giảm hiệu suất - {{ affected_area }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Phát hiện suy giảm hiệu suất
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Thời gian phản hồi chậm được phát hiện
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          Việc cài đặt Spwig của bạn đang trải qua suy giảm hiệu suất.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Vấn đề hiệu suất:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Khu vực bị ảnh hưởng:</strong> {{ affected_area }}<br/>
              <strong>Thời gian phản hồi hiện tại:</strong> <span style="color: #d97706; font-weight: bold;">{{ current_response_time }}ms</span><br/>
              <strong>Thời gian phản hồi bình thường:</strong> {{ normal_response_time }}ms<br/>
              <strong>Suy giảm:</strong> {{ degradation_percentage }}% chậm hơn<br/>
              <strong>Phát hiện:</strong> {{ detected_at }}
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
          Nguyên nhân có thể:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ possible_causes }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Các điểm cuối chậm nhất:
        </mj-text>

        {% for endpoint in slow_endpoints %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ endpoint.path }}</strong> - {{ endpoint.avg_time }}ms ({{ endpoint.request_count }} yêu cầu)
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Các hành động được đề xuất:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_actions }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ performance_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Xem bảng điều khiển hiệu suất
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ slow_queries_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          Xem các truy vấn chậm
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          Chúng tôi sẽ thông báo cho bạn khi hiệu suất trở lại bình thường.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ SUY GIẢM HIỆU SUẤT

Thời gian phản hồi chậm được phát hiện

Việc cài đặt Spwig của bạn đang trải qua suy giảm hiệu suất.

VẤN ĐỀ HIỆU SUẤT:
- Khu vực bị ảnh hưởng: {{ affected_area }}
- Thời gian phản hồi hiện tại: {{ current_response_time }}ms
- Thời gian phản hồi bình thường: {{ normal_response_time }}ms
- Suy giảm: {{ degradation_percentage }}% chậm hơn
- Phát hiện: {{ detected_at }}

TÁC ĐỘNG:
{{ impact_description }}

NGUYÊN NHÂN CÓ THỂ:
{{ possible_causes }}

CÁC ĐIỂM CUỐI CHẬM NHẤT:
{% for endpoint in slow_endpoints %}
{{ endpoint.path }} - {{ endpoint.avg_time }}ms ({{ endpoint.request_count }} yêu cầu)
{% endfor %}

CÁC HÀNH ĐỘNG ĐƯỢC ĐỀ XUẤT:
{{ recommended_actions }}

Xem bảng điều khiển hiệu suất: {{ performance_dashboard_url }}
Xem các truy vấn chậm: {{ slow_queries_url }}

Chúng tôi sẽ thông báo cho bạn khi hiệu suất trở lại bình thường.