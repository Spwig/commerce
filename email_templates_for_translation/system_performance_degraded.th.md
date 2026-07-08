---
template_type: system_performance_degraded
category: System Health
---

# Email Template: system_performance_degraded

## Subject
⚠️ ตรวจพบการลดประสิทธิภาพ - {{ affected_area }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ การลดประสิทธิภาพ
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ตรวจพบเวลาตอบสนองที่ช้า
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          การติดตั้ง Spwig ของคุณกำลังประสบกับการลดประสิทธิภาพ
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              ปัญหาประสิทธิภาพ:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>พื้นที่ที่ได้รับผลกระทบ:</strong> {{ affected_area }}<br/>
              <strong>เวลาตอบสนองปัจจุบัน:</strong> <span style="color: #d97706; font-weight: bold;">{{ current_response_time }}ms</span><br/>
              <strong>เวลาตอบสนองปกติ:</strong> {{ normal_response_time }}ms<br/>
              <strong>การลดประสิทธิภาพ:</strong> {{ degradation_percentage }}% ช้าลง<br/>
              <strong>ตรวจพบเมื่อ:</strong> {{ detected_at }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ผลกระทบ:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          สาเหตุที่เป็นไปได้:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ possible_causes }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          เอนด์พอยนต์ที่ช้าที่สุด:
        </mj-text>

        {% for endpoint in slow_endpoints %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="12px">
          <mj-column>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>{{ endpoint.path }}</strong> - {{ endpoint.avg_time }}ms ({{ endpoint.request_count }} คำขอ)
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="8px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          การกระทำที่แนะนำ:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ recommended_actions }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ performance_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          ดูแดชบอร์ดประสิทธิภาพ
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ slow_queries_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          ดูคำสั่งที่ช้า
        </mj-button>

        <mj-spacer height="20px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          เราจะแจ้งให้คุณทราบเมื่อประสิทธิภาพกลับสู่ภาวะปกติ
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ การลดประสิทธิภาพ

ตรวจพบเวลาตอบสนองที่ช้า

การติดตั้ง Spwig ของคุณกำลังประสบกับการลดประสิทธิภาพ

ปัญหาประสิทธิภาพ:
- พื้นที่ที่ได้รับผลกระทบ: {{ affected_area }}
- เวลาตอบสนองปัจจุบัน: {{ current_response_time }}ms
- เวลาตอบสนองปกติ: {{ normal_response_time }}ms
- การลดประสิทธิภาพ: {{ degradation_percentage }}% ช้าลง
- ตรวจพบเมื่อ: {{ detected_at }}

ผลกระทบ:
{{ impact_description }}

สาเหตุที่เป็นไปได้:
{{ possible_causes }}

เอนด์พอยนต์ที่ช้าที่สุด:
{% for endpoint in slow_endpoints %}
{{ endpoint.path }} - {{ endpoint.avg_time }}ms ({{ endpoint.request_count }} คำขอ)
{% endfor %}

การกระทำที่แนะนำ:
{{ recommended_actions }}

ดูแดชบอร์ดประสิทธิภาพ: {{ performance_dashboard_url }}
ดูคำสั่งที่ช้า: {{ slow_queries_url }}

เราจะแจ้งให้คุณทราบเมื่อประสิทธิภาพกลับสู่ภาวะปกติ
